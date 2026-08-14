#!/usr/bin/env python3
"""Validate the partial 2024 reference-answer candidate layer."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers"
OUT = BASE / "reference_answer_candidates.jsonl"
MAIN_INDEX = BASE / "answer_index.jsonl"
PDF = ROOT / "Data/reference/gaokao/pdf/2024/2024_NCA_answer.pdf"
MD = ROOT / "Data/reference/gaokao/mineru_result/2024_NCA_answer/full.md"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2024_20260809.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip()] if OUT.exists() else []
    ids = sorted(int(r.get("question_id", -1)) for r in rows)
    if ids != list(range(1, 10)):
        errors.append(f"coverage={ids}, expected 1..9")
    if len({r.get("candidate_id") for r in rows}) != len(rows):
        errors.append("duplicate candidate_id")
    pdf_sha = sha_bytes(PDF.read_bytes()) if PDF.exists() else None
    md_sha = sha_bytes(MD.read_bytes()) if MD.exists() else None
    for row in rows:
        cid = row.get("candidate_id", "?")
        text = row.get("answer_candidate_text") or ""
        excerpt = row.get("source_group_excerpt") or ""
        if row.get("source_authority_status") != "unverified_local_provided":
            errors.append(f"{cid}: authority escaped unverified boundary")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{cid}: scoring status changed")
        if row.get("mapping_level") != "M0" or row.get("kp_id") != "N/A":
            errors.append(f"{cid}: mapping status changed")
        if row.get("answer_candidate_sha256") != sha_bytes(text.encode("utf-8")):
            errors.append(f"{cid}: answer hash mismatch")
        if row.get("source_group_excerpt_sha256") != sha_bytes(excerpt.encode("utf-8")):
            errors.append(f"{cid}: source excerpt hash mismatch")
        if re.sub(r"\s+", "", text) not in re.sub(r"\s+", "", excerpt):
            errors.append(f"{cid}: candidate text not contained in source group")
        if row.get("source_pdf_sha256") != pdf_sha:
            errors.append(f"{cid}: PDF hash mismatch")
        if row.get("source_mineru_md_sha256") != md_sha:
            errors.append(f"{cid}: MinerU hash mismatch")
        forbidden_values = {row.get("candidate_status"), row.get("source_authority_status"), row.get("source_status"), row.get("answer_source_status"), row.get("scoring_status"), row.get("mapping_level"), row.get("kp_id")}
        if any(label in forbidden_values for label in ("official_verified", "M1", "M2", "M3")):
            errors.append(f"{cid}: forbidden official/mapping label")
    main_rows = [json.loads(line) for line in MAIN_INDEX.read_text(encoding="utf-8").splitlines() if line.strip()] if MAIN_INDEX.exists() else []
    main_missing = [r for r in main_rows if r.get("question_id") in range(1, 23) and not (r.get("answer_text") or "") and r.get("answer_status") in {"missing", "N/A"}]
    if len(main_missing) != 22:
        errors.append(f"main answer index missing gate changed: {len(main_missing)}")
    result = {
        "schema_version": "reference-answer-candidate-validation-2024-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "main_index_missing_rows": len(main_missing),
        "errors": errors,
        "checks": {
            "partial_coverage": ids == list(range(1, 10)),
            "source_hashes": not any("hash mismatch" in e for e in errors),
            "authority_gate": not any("authority" in e or "official" in e for e in errors),
            "main_index_unchanged_gate": not any("main answer index" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
