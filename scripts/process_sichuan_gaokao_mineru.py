#!/usr/bin/env python3
"""Run MinerU on the supplied 2008--2024 Sichuan Gaokao PDF corpus.

The source directory is intentionally independent from the rejected EOL batch
under ``Data/reference/gaokao``.  The two duplicate/alternate files documented
in the corpus README are retained but excluded from the main upload set.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "Data" / "2008-2024·（四川）语文高考真题"
RESULT_DIR = CORPUS / "mineru_result"
MANIFEST = CORPUS / "manifest.json"
LOG = CORPUS / "mineru_run.jsonl"
sys.path.insert(0, str(ROOT / "scripts"))
import mineru_client as mc  # noqa: E402


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_info(path: Path) -> tuple[int | None, int]:
    import subprocess

    result = subprocess.run(["/usr/bin/pdfinfo", str(path)], capture_output=True, text=True, check=True)
    pages = next((int(x.split(":", 1)[1].strip()) for x in result.stdout.splitlines()
                  if x.startswith("Pages:")), None)
    text = subprocess.run(["/usr/bin/pdftotext", "-layout", str(path), "-"],
                          capture_output=True, text=True, check=True).stdout
    return pages, len(text.strip())


def is_excluded(path: Path) -> bool:
    name = path.name
    return name.endswith("（空白卷）(1).pdf") or name.endswith("（空白卷）(1).PDF")


def role_for(name: str) -> str:
    return "question" if "空白卷" in name else "analysis"


def year_for(name: str) -> int:
    m = re.match(r"(20\d{2})年", name)
    if not m:
        raise ValueError(f"cannot infer year from {name}")
    return int(m.group(1))


def code_for(year: int, name: str) -> str:
    if year <= 2015:
        return "SC"
    if year <= 2020:
        return "NC3"
    return "NCA"


def files() -> list[Path]:
    return sorted((p for p in CORPUS.glob("*.pdf") if not is_excluded(p)),
                  key=lambda p: (year_for(p.name), role_for(p.name), p.name))


def make_rows() -> list[dict[str, Any]]:
    rows = []
    for path in files():
        year = year_for(path.name)
        pages, text_chars = pdf_info(path)
        role = role_for(path.name)
        stem = path.stem
        rows.append({
            "artifact_id": f"ART-SC-GK-{year}-{code_for(year, path.name)}-{role.upper()}",
            "year": year,
            "paper_code": code_for(year, path.name),
            "paper_title": path.name,
            "document_role": role,
            "sichuan_relation": (
                "四川省自主命题" if year <= 2015 else
                "四川适用全国卷Ⅲ" if year <= 2020 else "四川适用全国甲卷"
            ),
            "source_level": "unverified_local_provided",
            "authenticity_status": "unverified",
            "status": "acquired",
            "local_pdf": str(path.relative_to(ROOT)),
            "byte_size": path.stat().st_size,
            "sha256": digest(path),
            "pdf_page_count": pages,
            "pdf_text_chars": text_chars,
            "scan_only": text_chars == 0,
            "excluded_from_main_batch": False,
            "mineru_state": "pending",
            "mineru_result_dir": str((RESULT_DIR / stem).relative_to(ROOT)),
            "mineru_full_md": str((RESULT_DIR / stem / "full.md").relative_to(ROOT)),
            "mineru_error": None,
        })
    return rows


def write_manifest(rows: list[dict[str, Any]], *, run_state: str) -> None:
    extra_files = []
    for path in sorted(CORPUS.glob("*.pdf")):
        if not is_excluded(path):
            continue
        pages, _ = pdf_info(path)
        duplicate = "2018年" in path.name
        extra_files.append({
            "local_pdf": str(path.relative_to(ROOT)),
            "sha256": digest(path),
            "pdf_page_count": pages,
            "disposition": "excluded_duplicate" if duplicate else "excluded_unverified_alternate",
            "reason": ("与无(1)后缀主版本字节级重复" if duplicate else "与主版本不同且页数较少，疑似不完整；未运行MinerU"),
        })
    data = {
        "schema_version": "sichuan-gaokao-mineru-1.0",
        "corpus_path": str(CORPUS.relative_to(ROOT)),
        "corpus_path_absolute": str(CORPUS),
        "coverage": "2008-2024",
        "run_state": run_state,
        "extra_files": extra_files,
        "updated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "selection_rule": "exclude exact duplicate 2018 blank (1) and alternate 2017 blank (1); preserve originals",
        "records": rows,
    }
    tmp = MANIFEST.with_suffix(".json.part")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(tmp, MANIFEST)


def log(event: dict[str, Any]) -> None:
    event = {"time": time.strftime("%Y-%m-%dT%H:%M:%S%z"), **event}
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n")


def poll(batch_id: str, interval: int, timeout: int) -> list[dict[str, Any]]:
    waited = 0
    while waited <= timeout:
        _, _, payload = mc._req("GET", f"/api/v4/extract-results/batch/{batch_id}")
        if isinstance(payload, dict):
            data = payload.get("data", payload)
            results = data.get("extract_result") or data.get("results") or data.get("extract_results") or []
            if results:
                states = [r.get("state") or r.get("status") for r in results]
                print(f"poll {batch_id[:12]} t={waited}s states={states}", flush=True)
                if all(state in ("done", "failed") for state in states):
                    return results
        time.sleep(interval)
        waited += interval
    raise TimeoutError(f"batch {batch_id} timed out after {timeout}s")


def safe_extract(zip_path: Path, target: Path) -> None:
    target = target.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"ZIP CRC failure: {bad}")
        for member in archive.infolist():
            destination = (target / member.filename).resolve()
            if destination != target and target not in destination.parents:
                raise RuntimeError(f"unsafe ZIP member: {member.filename}")
        archive.extractall(target)


def materialize(result: dict[str, Any], by_name: dict[str, Path]) -> tuple[str, str | None]:
    name = result.get("file_name", "")
    source = by_name.get(name)
    state = result.get("state") or result.get("status")
    url = result.get("full_zip_url")
    if source is None:
        return name, "unknown file returned by MinerU"
    if state != "done" or not url:
        return name, f"state={state}; {result.get('err_msg', '')[:300]}"
    target = RESULT_DIR / source.stem
    if (target / "full.md").exists() and (target / "layout.json").exists():
        return name, None
    cache = Path(tempfile.mkdtemp(prefix="sichuan-gaokao-mineru-"))
    zip_path = cache / f"{source.stem}.zip"
    temp_target = RESULT_DIR / f".{source.stem}.part"
    try:
        mc.download(url, str(zip_path))
        if temp_target.exists():
            shutil.rmtree(temp_target)
        temp_target.mkdir(parents=True)
        safe_extract(zip_path, temp_target)
        if not (temp_target / "full.md").exists():
            raise RuntimeError("MinerU ZIP has no full.md")
        os.replace(temp_target, target)
    except Exception as exc:
        if temp_target.exists():
            shutil.rmtree(temp_target)
        return name, str(exc)[:300]
    finally:
        shutil.rmtree(cache, ignore_errors=True)
    return name, None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=6, help="PDFs per MinerU batch")
    parser.add_argument("--interval", type=int, default=15, help="poll interval seconds")
    parser.add_argument("--timeout", type=int, default=7200, help="batch timeout seconds")
    parser.add_argument("--prepare-only", action="store_true", help="write manifest without uploading")
    args = parser.parse_args()

    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    rows = make_rows()
    write_manifest(rows, run_state="prepared")
    print(f"selected {len(rows)} PDFs; excluded duplicate/alternate files by README rule", flush=True)
    if args.prepare_only:
        return 0
    by_path = {r["local_pdf"]: r for r in rows}
    pending = [p for p in files() if not (RESULT_DIR / p.stem / "full.md").exists()]
    print(f"pending {len(pending)} PDFs", flush=True)
    for start in range(0, len(pending), args.limit):
        batch_paths = pending[start : start + args.limit]
        batch_no = start // args.limit + 1
        print(f"submit batch {batch_no}: {len(batch_paths)} PDFs", flush=True)
        log({"event": "submit", "batch_no": batch_no, "files": [p.name for p in batch_paths]})
        files_payload = [{"path": str(p), "name": p.name} for p in batch_paths]
        try:
            batch_id, _ = mc.submit(files_payload, extra={
                "language": "ch", "enable_formula": True, "enable_table": True,
                "model_version": "pipeline",
            })
            if not batch_id:
                raise RuntimeError("MinerU returned no batch id")
            results = poll(batch_id, args.interval, args.timeout)
        except Exception as exc:
            print(f"batch {batch_no} failed: {exc}", flush=True)
            for path in batch_paths:
                by_path[str(path.relative_to(ROOT))]["mineru_state"] = "failed"
                by_path[str(path.relative_to(ROOT))]["mineru_error"] = str(exc)[:300]
            write_manifest(rows, run_state="partial_failed")
            log({"event": "batch_failed", "batch_no": batch_no, "error": str(exc)[:500]})
            continue
        by_name = {p.name: p for p in batch_paths}
        for result in results:
            name, error = materialize(result, by_name)
            source = by_name.get(name)
            if source is None:
                continue
            row = by_path[str(source.relative_to(ROOT))]
            row["mineru_state"] = "done" if error is None else "failed"
            row["mineru_error"] = error
            row["mineru_batch_id"] = batch_id
            row["mineru_processed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            print(f"{'DONE' if error is None else 'FAILED'} {name}{': ' + error if error else ''}", flush=True)
            log({"event": "result", "batch_id": batch_id, "file": name,
                 "state": row["mineru_state"], "error": error})
        write_manifest(rows, run_state="running")
    failed = [r for r in rows if r["mineru_state"] != "done"]
    write_manifest(rows, run_state="complete" if not failed else "partial_failed")
    print(f"completed={len(rows)-len(failed)} failed={len(failed)} manifest={MANIFEST}", flush=True)
    return 0 if not failed else 2


if __name__ == "__main__":
    raise SystemExit(main())
