#!/usr/bin/env python3
"""Validate the isolated 2024 local-analysis candidate layer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024"
FULL = ROOT / "Data/2008-2024·（四川）语文高考真题/mineru_result/2024年高考语文试卷（全国甲卷）（解析卷）/full.md"
OUT = BASE / "answers/reference_answer_candidates_local_analysis.jsonl"
MAIN = BASE / "answers/answer_index.jsonl"
MEIPIAN = BASE / "answers/reference_answer_candidates_meipian.jsonl"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2024_local_analysis_20260809.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str | None) -> str | None:
    return None if text is None else sha_bytes(text.encode("utf-8"))


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []
    rows = read_jsonl(OUT) if OUT.exists() else []
    ids = sorted(int(row.get("question_id", -1)) for row in rows)
    if ids != list(range(1, 23)):
        errors.append(f"coverage={ids}, expected 1..22")
    if len({row.get("candidate_id") for row in rows}) != len(rows):
        errors.append("duplicate candidate_id")
    raw = FULL.read_text(encoding="utf-8") if FULL.exists() else ""
    full_sha = sha_bytes(FULL.read_bytes()) if FULL.exists() else None
    for row in rows:
        qid = row.get("question_id")
        cid = row.get("candidate_id", "?")
        candidate = row.get("answer_candidate_text") or ""
        section = row.get("source_answer_section") or {}
        start = int(section.get("offset_start", -1))
        end = int(section.get("offset_end", -1))
        excerpt = section.get("excerpt") or ""
        if row.get("candidate_status") != "candidate_unverified":
            errors.append(f"{cid}: candidate status escaped")
        if row.get("source_authority_status") != "unverified_local_provided":
            errors.append(f"{cid}: authority escaped")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{cid}: scoring gate changed")
        if row.get("mapping_level") != "M0" or row.get("kp_id") != "N/A":
            errors.append(f"{cid}: mapping gate changed")
        if row.get("answer_candidate_sha256") != sha_text(candidate):
            errors.append(f"{cid}: candidate hash mismatch")
        if row.get("source_mineru_md_sha256") != full_sha:
            errors.append(f"{cid}: MinerU hash mismatch")
        if start < 0 or end < start or end > len(raw):
            errors.append(f"{cid}: source offsets invalid")
        else:
            if raw[start:end].strip() != excerpt:
                errors.append(f"{cid}: source excerpt/offset mismatch")
            if section.get("excerpt_sha256") != sha_text(excerpt):
                errors.append(f"{cid}: source excerpt hash mismatch")
        analysis = row.get("source_analysis_excerpt")
        if row.get("source_analysis_excerpt_sha256") != sha_text(analysis):
            errors.append(f"{cid}: analysis excerpt hash mismatch")
        if not (row.get("external_comparison") or {}).get("third_party_candidate_id"):
            errors.append(f"{cid}: missing third-party comparison")
        forbidden = {row.get(field) for field in ("candidate_status", "source_authority_status", "source_status", "answer_source_status", "scoring_status", "mapping_level", "kp_id")}
        if forbidden.intersection({"official_verified", "M1", "M2", "M3"}):
            errors.append(f"{cid}: forbidden authority/mapping value")
        if qid in (1, 2) and row.get("candidate_extraction_method") != "derived_from_analysis_conclusion":
            errors.append(f"{cid}: Q1/Q2 derivation method missing")
        if qid == 16:
            counts = row.get("q16_duplicate_symbol_counts") or {}
            # Counts are stored in the source section metadata by the recovery
            # script; two occurrences of each symbol document the duplication.
            if counts and any(counts.get(symbol) != 2 for symbol in "①②③④⑤⑥"):
                errors.append(f"{cid}: Q16 duplicate symbol counts not all 2")
            if "o崖" not in candidate:
                errors.append(f"{cid}: Q16 OCR observation absent")
            if row.get("candidate_extraction_method") != "explicit_answer_marker_with_duplicate_payload_normalized":
                errors.append(f"{cid}: Q16 normalization method missing")
        if qid == 22 and row.get("candidate_content_type") != "writing_model_essay_candidate":
            errors.append(f"{cid}: Q22 writing-artifact label missing")
    main_rows = read_jsonl(MAIN) if MAIN.exists() else []
    if len(main_rows) != 22 or any((row.get("answer_status") not in {"N/A", "missing"}) or row.get("answer_text") for row in main_rows):
        errors.append("main answer_index gate changed")
    third_rows = read_jsonl(MEIPIAN) if MEIPIAN.exists() else []
    if sorted(int(row.get("question_id", -1)) for row in third_rows) != list(range(1, 23)):
        errors.append("third-party comparison layer missing full coverage")
    result = {
        "schema_version": "reference-answer-candidate-validation-2024-local-analysis-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "main_index_rows": len(main_rows),
        "errors": errors,
        "checks": {
            "coverage": ids == list(range(1, 23)),
            "source_hashes_and_offsets": not any("hash" in error or "offset" in error or "excerpt" in error for error in errors),
            "authority_gate": not any("authority" in error or "scoring" in error or "mapping" in error or "forbidden" in error for error in errors),
            "main_index_unchanged_gate": not any("main answer_index" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
