#!/usr/bin/env python3
"""Validation gate for the Sichuan Gaokao extraction calibration slice."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "Data" / "2008-2024·（四川）语文高考真题"
OUT = CORPUS / "exam_extract"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def frontmatter_value(text: str, key: str) -> str | None:
    """Read a simple quoted/scalar frontmatter value without adding a YAML dependency."""
    match = re.search(rf'(?m)^{re.escape(key)}:\s*(?:"([^"]*)"|([^\n]+))$', text)
    if not match:
        return None
    return (match.group(1) or match.group(2) or "").strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, default=2008)
    args = ap.parse_args()
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    rows = [r for r in manifest["records"] if int(r["year"]) == args.year]
    errors: list[str] = []
    warnings: list[str] = []
    if len(rows) != 2:
        errors.append(f"manifest role count={len(rows)}, expected 2")
    exam_id = f"GK-{rows[0]['paper_code']}-{args.year}" if rows else f"GK-UNKNOWN-{args.year}"
    base = OUT / exam_id
    expected = list(range(1, 22)) if args.year in (2008, 2015) else None
    role_rows = {}
    for row in rows:
        role = row["document_role"]
        role_rows[role] = row
        raw = ROOT / row["mineru_full_md"]
        clean = base / "clean_md" / f"{role}.md"
        if not raw.exists(): errors.append(f"missing raw full.md: {raw}")
        if not clean.exists(): errors.append(f"missing clean md: {clean}")
        if clean.exists():
            text = clean.read_text(encoding="utf-8")
            m = re.search(r'^raw_sha256: "([0-9a-f]{64})"$', text, flags=re.M)
            if raw.exists() and (not m or sha256(raw) != m.group(1)):
                errors.append(f"raw hash changed or missing clean anchor: {raw}")
            for marker in ("资料提供形式", "雪山学社", "XSWK21", "低价正版教辅"):
                if marker in text:
                    errors.append(f"advertisement marker remains in {clean}: {marker}")
            if "/home/ubuntu/" in text:
                errors.append(f"absolute workspace link in {clean}")
        ledger = base / "ledger" / "questions.jsonl"
        if not ledger.exists():
            errors.append(f"missing question ledger: {ledger}")
    question_ledger = base / "ledger" / "questions.jsonl"
    question_rows = [json.loads(x) for x in question_ledger.read_text(encoding="utf-8").splitlines() if x.strip()] if question_ledger.exists() else []
    if expected is not None:
        got = sorted({r["question_id"] for r in question_rows if r.get("source_role") == "question"})
        if got != expected:
            errors.append(f"question id set={got}, expected={expected}")
        got_analysis = sorted({r["question_id"] for r in question_rows if r.get("source_role") == "analysis"})
        if got_analysis != expected:
            errors.append(f"analysis question id set={got_analysis}, expected={expected}")
    for role in ("question", "analysis"):
        segdir = base / "segments" / role
        files = sorted(segdir.glob("Q*.md")) if segdir.exists() else []
        if len(files) != 21:
            errors.append(f"{role} segment count={len(files)}, expected 21")
        for path in files:
            text = path.read_text(encoding="utf-8")
            for marker in ("原始 MinerU", "原始 PDF", "清洗整卷"):
                if marker not in text:
                    errors.append(f"missing provenance link {marker}: {path}")
            if "/home/ubuntu/" in text:
                errors.append(f"absolute workspace link in {path}")
            body = text.split("---\n\n", 2)[-1].strip()
            m = re.search(r'^segment_clean_sha256: "([0-9a-f]{64})"$', text, flags=re.M)
            if not m or sha256_text(body) != m.group(1):
                errors.append(f"segment hash mismatch: {path}")
            if role == "analysis" and "参考答案" in body:
                errors.append(f"answer section leaked into analysis question segment: {path}")
    answers = base / "answers" / "answer_bundle.md"
    answer_state = None
    if not answers.exists():
        errors.append("missing answer bundle")
    else:
        answer_text = answers.read_text(encoding="utf-8")
        answer_state = (
            frontmatter_value(answer_text, "answer_status")
            or frontmatter_value(answer_text, "source_status")
        )
        # A deliberate missing-source placeholder is valid evidence of a gap;
        # it must not be forced to contain a fake/empty reference-answer heading.
        explicit_missing = answer_state == "missing" and (
            "没有可核验的答案" in answer_text
            or "答案/评分材料缺失" in answer_text
            or "blocked_missing_source" in answer_text
        )
        if not explicit_missing and "参考答案" not in answer_text:
            errors.append("answer bundle has no reference-answer anchor")
        if explicit_missing:
            warnings.append("answer bundle is an explicit missing-source placeholder; no answer/scoring claim is made")
    answer_index = base / "answers" / "answer_index.jsonl"
    answer_rows = [json.loads(x) for x in answer_index.read_text(encoding="utf-8").splitlines() if x.strip()] if answer_index.exists() else []
    if len(answer_rows) != 21 or sorted(r.get("question_id") for r in answer_rows) != list(range(1, 22)):
        errors.append(f"answer index rows={len(answer_rows)}, expected one row for Q001-Q021")
    materials = base / "ledger" / "materials.jsonl"
    mcount = len([x for x in materials.read_text(encoding="utf-8").splitlines() if x.strip()]) if materials.exists() else 0
    # Material cardinality is source-specific.  The historical 2008 pilot has
    # five material records; the 2013 slice has four.  Other years are checked
    # for non-empty, hash-valid records but are not forced into the 2008 shape.
    expected_material_count = {2008: 5, 2013: 4}.get(args.year)
    if mcount == 0:
        errors.append("material ledger is empty")
    elif expected_material_count is not None and mcount != expected_material_count:
        errors.append(f"material count={mcount}, expected {expected_material_count} for {args.year} calibration")
    if materials.exists():
        for line in materials.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            material = json.loads(line)
            path = ROOT / material["material_path"]
            if not path.exists():
                errors.append(f"missing material target: {path}")
                continue
            body = path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()
            if sha256_text(body) != material["material_clean_sha256"]:
                errors.append(f"material hash mismatch: {path}")
    exc = base / "review" / "exceptions.jsonl"
    if not exc.exists() or not exc.read_text(encoding="utf-8").strip():
        errors.append("no cleaning/OCR exception log")
    report = {
        "schema_version": "exam-extract-validation-0.1",
        "exam_id": exam_id,
        "result": "passed" if not errors else "failed",
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "manifest_roles": len(rows) == 2,
            "raw_hashes": not any("raw hash changed" in e for e in errors),
            "clean_advertisement_isolation": not any("advertisement marker" in e for e in errors),
            "question_coverage": not any("question id set" in e or "segment count" in e for e in errors),
            "provenance_links": not any("provenance link" in e or "absolute workspace link" in e for e in errors),
            "segment_hashes": not any("segment hash mismatch" in e or "answer section leaked" in e for e in errors),
            "answer_bundle": not any("answer bundle" in e for e in errors),
            "answer_index": not any("answer index" in e for e in errors),
            "materials": not any("material" in e for e in errors),
            "exception_log": not any("exception log" in e for e in errors),
        },
        "answer_state": answer_state,
        "material_count": mcount,
        "expected_material_count": expected_material_count,
    }
    path = base / "review" / "validation.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
