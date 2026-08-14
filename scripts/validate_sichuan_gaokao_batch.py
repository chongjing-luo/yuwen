#!/usr/bin/env python3
"""Validate question-level extraction for one or more Sichuan papers.

This validator is intentionally separate from the 2008 calibration validator:
2009--2015 have different section maps and several analysis PDFs interleave
answers with question text.  It checks traceability and top-level coverage as
hard gates, while treating answer presence and fine-grained taxonomy as
review fields rather than silently claiming completeness.
"""
from __future__ import annotations

import argparse, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "Data" / "2008-2024·（四川）语文高考真题"
OUT = CORPUS / "exam_extract"
EXPECTED_COUNTS = {**{y: 21 for y in range(2008, 2016)}, **{y: 12 for y in range(2016, 2018)},
                   **{y: 10 for y in range(2018, 2021)}, **{y: 22 for y in range(2021, 2025)}}

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def validate(year: int, *, check_answers: bool = False) -> dict:
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    rows = [r for r in manifest["records"] if int(r["year"]) == year]
    exam_id = f"GK-{rows[0]['paper_code']}-{year}" if rows else f"GK-SC-{year}"
    base = OUT / exam_id
    errors: list[str] = []
    warnings: list[str] = []
    expected = list(range(1, EXPECTED_COUNTS.get(year, 21) + 1))
    if len(rows) != 2:
        errors.append(f"manifest records={len(rows)}, expected 2")
    role_rows = {r["document_role"]: r for r in rows}
    all_rows = []
    for role in ("question", "analysis"):
        row = role_rows.get(role)
        if not row:
            errors.append(f"missing manifest role {role}")
            continue
        raw = ROOT / row["mineru_full_md"]
        clean = base / "clean_md" / f"{role}.md"
        ledger = base / "ledger" / f"questions-{role}.jsonl"
        if not raw.exists(): errors.append(f"missing raw full.md: {raw}")
        if not clean.exists(): errors.append(f"missing clean md: {clean}")
        if not ledger.exists(): errors.append(f"missing ledger: {ledger}")
        if clean.exists():
            text = clean.read_text(encoding="utf-8")
            m = re.search(r'^raw_sha256: "([0-9a-f]{64})"$', text, re.M)
            if raw.exists() and (not m or m.group(1) != sha256(raw)):
                errors.append(f"raw hash mismatch: {role}")
            for marker in ("资料提供形式", "雪山学社", "XSWK21", "低价正版教辅"):
                if marker in text: errors.append(f"advertisement marker remains in clean {role}: {marker}")
            if "/home/ubuntu/" in text: errors.append(f"absolute link in clean {role}")
        rows_q = [json.loads(x) for x in ledger.read_text(encoding="utf-8").splitlines() if x.strip()] if ledger.exists() else []
        all_rows.extend(rows_q)
        got = sorted({int(x.get("question_id")) for x in rows_q})
        if got != expected: errors.append(f"{role} question ids={got}, expected 1..21")
        if len(rows_q) != len(expected): errors.append(f"{role} ledger rows={len(rows_q)}, expected {len(expected)}")
        segdir = base / "segments" / role
        segs = sorted(segdir.glob("Q*.md")) if segdir.exists() else []
        if len(segs) != len(expected): errors.append(f"{role} segment files={len(segs)}, expected {len(expected)}")
        for seg in segs:
            st = seg.read_text(encoding="utf-8")
            if "/home/ubuntu/" in st: errors.append(f"absolute link in {seg}")
            for marker in ("清洗整卷", "原始 MinerU", "原始 PDF"):
                if marker not in st: errors.append(f"missing {marker}: {seg}")
            body = st.split("---\n\n", 2)[-1].strip()
            m = re.search(r'^segment_clean_sha256: "([0-9a-f]{64})"$', st, re.M)
            if not m or sha256_text(body) != m.group(1): errors.append(f"segment hash mismatch: {seg}")
            if "missing_source_marker" in st:
                warnings.append(f"source marker missing; PDF review required: {seg.name}")
    # Material links are required for the four reading groups; Q18--20 and
    # Q21 prompts remain separately reviewable because formats vary by year.
    mats = sorted((base / "materials").glob("MAT-*.md")) if (base / "materials").exists() else []
    if len(mats) < (5 if year >= 2016 else 4): errors.append(f"materials={len(mats)}, expected at least {5 if year >= 2016 else 4}")
    for row in all_rows:
        mid = row.get("material_id")
        if mid and not (base / "materials" / f"{mid}.md").exists(): errors.append(f"missing material {mid}")
        if float(row.get("type_confidence", 0)) < 0.90:
            warnings.append(f"low type confidence Q{row.get('question_id')}")
    types = {row.get("question_type_l1") for row in all_rows}
    for needed in ("language_use", "objective_choice", "reading_subjective", "writing"):
        if needed not in types: warnings.append(f"taxonomy missing {needed}")
    if not (base / "review" / "exceptions.jsonl").exists(): errors.append("missing exceptions log")
    answer_checks = {"artifacts_present": None, "index_coverage": None, "missing_source_explicit": None}
    if check_answers:
        answer_bundle = base / "answers" / "answer_bundle.md"
        answer_index = base / "answers" / "answer_index.jsonl"
        answer_checks["artifacts_present"] = answer_bundle.exists() and answer_index.exists()
        if not answer_bundle.exists() or not answer_index.exists():
            errors.append("missing answer bundle or answer index")
        else:
            answer_rows = [json.loads(x) for x in answer_index.read_text(encoding="utf-8").splitlines() if x.strip()]
            expected_answer_count = EXPECTED_COUNTS.get(year, 21)
            got_answer_ids = sorted(int(r.get("question_id")) for r in answer_rows)
            answer_checks["index_coverage"] = len(answer_rows) == expected_answer_count and got_answer_ids == list(range(1, expected_answer_count + 1))
            if not answer_checks["index_coverage"]:
                errors.append(f"answer index rows/ids={len(answer_rows)}/{got_answer_ids}, expected {expected_answer_count}/1..{expected_answer_count}")
            missing_rows = sum(1 for r in answer_rows if r.get("answer_status") == "missing" or r.get("source_status") == "missing")
            answer_checks["missing_source_explicit"] = missing_rows == len(answer_rows)
            if missing_rows:
                warnings.append(f"answer source missing explicitly for {missing_rows}/{len(answer_rows)} questions")
    report = {"schema_version": "exam-extract-validation-0.2", "exam_id": exam_id,
              "year": year, "result": "passed" if not errors else "failed",
              "errors": errors, "warnings": warnings,
              "checks": {"raw_hashes": not any("hash" in x for x in errors),
                          "question_coverage": not any("question ids" in x or "ledger rows" in x or "segment files" in x for x in errors),
                          "provenance": not any("link" in x or "marker" in x for x in errors),
                          "materials": not any("materials" in x or "material " in x for x in errors),
                          "segment_hashes": not any("segment hash" in x for x in errors),
                          "answers": answer_checks}}
    path = base / "review" / f"validation-{year}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, action="append", required=True)
    ap.add_argument("--check-answers", action="store_true", help="also require answer bundle/index contract and report explicit missing-source rows")
    args = ap.parse_args()
    failed = False
    for year in args.year:
        report = validate(year, check_answers=args.check_answers)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        failed |= report["result"] != "passed"
    return 1 if failed else 0

if __name__ == "__main__":
    raise SystemExit(main())
