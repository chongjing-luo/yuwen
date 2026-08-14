#!/usr/bin/env python3
"""Validate the recovered local-analysis Q006 candidate without opening gates."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016"
SEGMENT = BASE / "segments/analysis/Q006.md"
OUT = BASE / "answers/reference_answer_candidates_q006_local_analysis.jsonl"
THIRD = BASE / "answers/reference_answer_candidates_q006_gzywtk.jsonl"
MAIN = BASE / "answers/answer_index.jsonl"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2016_q006_local_20260809.json"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip()] if OUT.exists() else []
    if len(rows) != 1 or rows[0].get("question_id") != 6:
        errors.append("expected one local Q006 candidate")
    segment_text = SEGMENT.read_text(encoding="utf-8") if SEGMENT.exists() else ""
    segment_sha = sha(SEGMENT.read_bytes()) if SEGMENT.exists() else None
    clean_match = re.search(r'(?m)^segment_clean_sha256:\s*"([0-9a-f]{64})"$', segment_text)
    clean_sha = clean_match.group(1) if clean_match else None
    for row in rows:
        cid = row.get("candidate_id", "?")
        text = row.get("answer_candidate_text") or ""
        for field, expected in {
            "candidate_status": "candidate_unverified",
            "source_authority_status": "unverified_local_provided",
            "source_status": "unverified_local_provided",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
        }.items():
            if row.get(field) != expected:
                errors.append(f"{cid}: {field} escaped safe value")
        if row.get("answer_candidate_sha256") != sha(text.encode("utf-8")):
            errors.append(f"{cid}: candidate hash mismatch")
        if row.get("source_segment_sha256") != segment_sha:
            errors.append(f"{cid}: segment hash mismatch")
        if row.get("source_segment_clean_sha256") != clean_sha:
            errors.append(f"{cid}: segment clean hash mismatch")
        if "【解答】" not in segment_text or "【点评】" not in segment_text:
            errors.append(f"{cid}: explicit answer boundary absent in source segment")
        for term in ("答B给3分", "坚持独立思考", "天下兴亡", "匹夫有责"):
            if term not in text:
                errors.append(f"{cid}: content guard missing {term}")
        comparison = row.get("external_comparison") or {}
        if not comparison.get("third_party_candidate_id") or not comparison.get("differences"):
            errors.append(f"{cid}: cross-source comparison incomplete")
    if not THIRD.exists():
        errors.append("third-party Q006 candidate missing")
    main_rows = [json.loads(line) for line in MAIN.read_text(encoding="utf-8").splitlines() if line.strip()] if MAIN.exists() else []
    q6 = next((row for row in main_rows if row.get("question_id") == 6), None)
    if not q6 or q6.get("answer_status") != "N/A" or q6.get("answer_text"):
        errors.append("main Q006 answer index gate changed")
    result = {
        "schema_version": "reference-answer-candidate-validation-2016-q006-local-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "errors": errors,
        "checks": {
            "single_question_coverage": len(rows) == 1 and rows[0].get("question_id") == 6 if rows else False,
            "source_hashes": not any("hash" in error for error in errors),
            "authority_gate": not any("safe value" in error or "candidate" in error and "missing" in error for error in errors),
            "main_index_unchanged_gate": not any("main Q006" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
