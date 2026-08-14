#!/usr/bin/env python3
"""Submit acquired Gaokao paper/answer PDFs to MinerU and materialize results.

This is deliberately separate from ``batch_mineru.py`` because exam artifacts
are not textbook split packages and must not alter the fixed 144-package
registry.  Results are written to ``Data/reference/gaokao/mineru_result`` and
the corpus manifest/registry receives only lineage metadata.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import mineru_client as mc  # noqa: E402


BASE = ROOT / "Data" / "reference" / "gaokao"
PDF_DIR = BASE / "pdf"
RESULT_DIR = BASE / "mineru_result"
MANIFEST = BASE / "manifest.json"
REGISTRY_DIR = BASE / "registry"


def pdfs() -> list[Path]:
    return sorted(p for p in PDF_DIR.glob("*/*.pdf") if not p.name.startswith(("debug", "out")))


def manifest_rows() -> dict[str, dict]:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {r.get("local_pdf"): r for r in data.get("records", []) if r.get("local_pdf")}


def poll(batch_id: str, interval: int = 15, timeout: int = 7200) -> list[dict]:
    waited = 0
    while waited <= timeout:
        status, _, payload = mc._req("GET", f"/api/v4/extract-results/batch/{batch_id}")
        if isinstance(payload, dict):
            data = payload.get("data", payload)
            results = data.get("extract_result") or data.get("results") or data.get("extract_results") or []
            if results:
                states = [r.get("state") or r.get("status") for r in results]
                print(f"poll {batch_id[:10]} t={waited}s states={states}", flush=True)
                if all(s in ("done", "failed") for s in states):
                    return results
        time.sleep(interval)
        waited += interval
    raise TimeoutError(f"MinerU batch {batch_id} timed out")


def extract_result(result: dict, by_name: dict[str, Path]) -> tuple[str, str | None]:
    name = result.get("file_name", "")
    state = result.get("state") or result.get("status")
    url = result.get("full_zip_url")
    if state != "done" or not url:
        return name, f"state={state}; {result.get('err_msg', '')[:300]}"
    source = by_name.get(name)
    if source is None:
        return name, "MinerU returned an unknown file name"
    target = RESULT_DIR / source.stem
    target.parent.mkdir(parents=True, exist_ok=True)
    if (target / "full.md").exists():
        return name, None
    cache_dir = Path(tempfile.mkdtemp(prefix="gaokao-mineru-zips-"))
    zip_path = cache_dir / f"{source.stem}.zip"
    temp_target = RESULT_DIR / f".{source.stem}.part"
    try:
        mc.download(url, str(zip_path))
        if temp_target.exists():
            shutil.rmtree(temp_target)
        temp_target.mkdir(parents=True)
        with zipfile.ZipFile(zip_path) as archive:
            bad = archive.testzip()
            if bad:
                raise RuntimeError(f"ZIP CRC failure: {bad}")
            archive.extractall(temp_target)
        os.replace(temp_target, target)
    except Exception as exc:
        if temp_target.exists():
            shutil.rmtree(temp_target)
        return name, str(exc)[:300]
    finally:
        shutil.rmtree(cache_dir, ignore_errors=True)
    return name, None


def update_manifest(rows: dict[str, dict], results: list[dict]) -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_pdf = {r.get("local_pdf"): r for r in data.get("records", [])}
    for result in results:
        name = result.get("file_name", "")
        source = next((p for p in pdfs() if p.name == name), None)
        if source is None:
            continue
        row = by_pdf.get(str(source.relative_to(ROOT)))
        if not row:
            continue
        row["mineru_state"] = result.get("state") or result.get("status")
        row["mineru_result_dir"] = str((RESULT_DIR / source.stem).relative_to(ROOT)) if row["mineru_state"] == "done" else None
        row["mineru_error"] = result.get("err_msg")
        row["mineru_processed_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    temp = MANIFEST.with_suffix(".json.part")
    temp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temp, MANIFEST)


def sync_registry() -> None:
    """Copy MinerU lineage into the separate Gaokao artifact registry."""
    artifact_path = REGISTRY_DIR / "artifacts.jsonl"
    if not artifact_path.exists():
        return
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_pdf = {r.get("local_pdf"): r for r in manifest.get("records", [])}
    by_source = {f"SRC-GK-{r.get('year')}-{r.get('paper_code')}-{str(r.get('document_role', '')).upper()}": r
                 for r in manifest.get("records", [])}
    rows = []
    for line in artifact_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        source = by_source.get(row.get("source_id")) or by_pdf.get(row.get("local_path"))
        if source:
            row["local_path"] = source.get("local_pdf") or source.get("local_html")
            row["page_count"] = source.get("pdf_page_count")
            row["byte_size"] = source.get("byte_size")
            row["sha256"] = source.get("sha256")
            row["original_url"] = source.get("original_url")
            row["status"] = source.get("status")
            row["mineru_state"] = source.get("mineru_state")
            row["mineru_result_dir"] = source.get("mineru_result_dir")
            row["mineru_full_md"] = (str(Path(source["mineru_result_dir"]) / "full.md")
                                      if source.get("mineru_result_dir") else None)
            row["mineru_processed_at"] = source.get("mineru_processed_at")
        rows.append(row)
    temp = artifact_path.with_suffix(".jsonl.part")
    temp.write_text("\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    os.replace(temp, artifact_path)
    source_path = REGISTRY_DIR / "sources.jsonl"
    if source_path.exists():
        source_rows = []
        for line in source_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            source_row = json.loads(line)
            source = by_source.get(source_row.get("source_id"))
            if source:
                # EOL is a third-party reproduction; no S3 row is promoted to
                # a verified canonical artifact merely by downloading it.
                source_row["canonical_artifact_id"] = None
                source_row["metadata_status"] = "acquired_unverified" if source.get("status") == "acquired" else source.get("status")
            source_rows.append(source_row)
        source_tmp = source_path.with_suffix(".jsonl.part")
        source_tmp.write_text("\n".join(json.dumps(r, ensure_ascii=False, sort_keys=True) for r in source_rows) + "\n", encoding="utf-8")
        os.replace(source_tmp, source_path)


def repair_manifest_from_result_dirs() -> None:
    """Recover lineage after an interrupted/partial manifest rewrite."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    changed = False
    for row in data.get("records", []):
        local_pdf = row.get("local_pdf")
        if not local_pdf and row.get("status") == "acquired":
            candidate = PDF_DIR / str(row.get("year")) / f"{row.get('year')}_{row.get('paper_code')}_{row.get('document_role')}.pdf"
            if candidate.exists():
                row["local_pdf"] = str(candidate.relative_to(ROOT))
                local_pdf = row["local_pdf"]
                changed = True
        if not local_pdf:
            continue
        pdf_path = ROOT / local_pdf
        if pdf_path.exists() and not row.get("pdf_page_count"):
            info = subprocess.run(["/usr/bin/pdfinfo", str(pdf_path)], capture_output=True, text=True, check=True).stdout
            pages = next((int(line.split(":", 1)[1]) for line in info.splitlines() if line.startswith("Pages:")), None)
            row["pdf_page_count"] = pages
            row["byte_size"] = pdf_path.stat().st_size
            digest = hashlib.sha256()
            with pdf_path.open("rb") as handle:
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
            row["sha256"] = digest.hexdigest()
            changed = True
        if row.get("mineru_state") == "done":
            continue
        stem = Path(local_pdf).stem
        result_dir = RESULT_DIR / stem
        if (result_dir / "full.md").exists():
            row["mineru_state"] = "done"
            row["mineru_result_dir"] = str(result_dir.relative_to(ROOT))
            row["mineru_full_md"] = str((result_dir / "full.md").relative_to(ROOT))
            row["mineru_repaired_from_existing_result"] = True
            changed = True
    if changed:
        temp = MANIFEST.with_suffix(".json.part")
        temp.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        os.replace(temp, MANIFEST)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=20, help="maximum PDFs per MinerU batch")
    parser.add_argument("--sync-only", action="store_true", help="only sync manifest fields into registry")
    args = parser.parse_args()
    if args.sync_only:
        repair_manifest_from_result_dirs()
        sync_registry()
        print("高考 artifact registry 已同步 MinerU 血缘", flush=True)
        return 0
    paths = pdfs()
    if not paths:
        print("没有待处理 PDF")
        return 0
    # Keep already materialized results out of the upload batch.
    pending = [p for p in paths if not (RESULT_DIR / p.stem / "full.md").exists()]
    print(f"PDF 总数 {len(paths)}；待提交 {len(pending)}", flush=True)
    all_results: list[dict] = []
    for start in range(0, len(pending), args.limit):
        batch_paths = pending[start : start + args.limit]
        files = [{"path": str(p), "name": p.name} for p in batch_paths]
        batch_id, _ = mc.submit(files, extra={"language": "ch", "enable_formula": True, "enable_table": True, "model_version": "pipeline"})
        if not batch_id:
            raise RuntimeError("MinerU submission returned no batch_id")
        print(f"submitted {len(files)} PDFs batch_id={batch_id}", flush=True)
        results = poll(batch_id)
        by_name = {p.name: p for p in batch_paths}
        ok = 0
        for result in results:
            name, error = extract_result(result, by_name)
            if error:
                print(f"FAILED {name}: {error}", flush=True)
            else:
                ok += 1
                print(f"DONE {name}", flush=True)
        all_results.extend(results)
        print(f"batch complete {ok}/{len(results)}", flush=True)
    update_manifest(manifest_rows(), all_results)
    sync_registry()
    print(f"完成：{len(all_results)} 个 MinerU 结果已登记", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
