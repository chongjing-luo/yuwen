#!/usr/bin/env python3
"""Validate the 2013 cross-source candidate comparison layer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers"
OUT = BASE / "reference_answer_candidate_comparison.jsonl"
LOCAL = BASE / "local_analysis_candidates.jsonl"
EXTERNAL = BASE / "reference_answer_candidates.jsonl"
MAIN = BASE / "answer_index.jsonl"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidate_comparison_GK-SC-2013_20260809.json"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_comparison_validation_2013_20260809.json"
EXPECTED_MAIN_SHA256 = "489ba22579be29b0426db2ece4732bc83bc850a903ca8d513c192a510a74289a"
ALLOWED = {
    "textually_consistent_unverified",
    "format_equivalent_unverified",
    "local_mixed_analysis_no_explicit_answer",
    "ocr_or_format_difference_requires_review",
    "text_difference_requires_review",
    "format_or_label_difference_requires_review",
    "coverage_difference_requires_review",
    "both_sources_missing",
}


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []
    required = (OUT, LOCAL, EXTERNAL, MAIN, RECEIPT)
    for path in required:
        if not path.exists():
            errors.append(f"missing required file: {path}")
    rows = load(OUT) if OUT.exists() else []
    local = {int(row["question_id"]): row for row in load(LOCAL)} if LOCAL.exists() else {}
    external = {int(row["question_id"]): row for row in load(EXTERNAL)} if EXTERNAL.exists() else {}
    if [row.get("question_id") for row in rows] != list(range(1, 22)):
        errors.append("comparison coverage/order must be Q1..Q21")
    if len({row.get("comparison_id") for row in rows}) != len(rows):
        errors.append("duplicate comparison_id")
    for row in rows:
        qid = row.get("question_id")
        cid = row.get("comparison_id", "?")
        if row.get("comparison_status") not in ALLOWED:
            errors.append(f"{cid}: unknown comparison status")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{cid}: scoring gate escaped")
        if (row.get("mapping_level"), row.get("kp_id")) != ("M0", "N/A"):
            errors.append(f"{cid}: mapping gate escaped")
        if row.get("adjudication") != "not_adjudicated":
            errors.append(f"{cid}: comparison was silently adjudicated")
        if qid in local and row.get("local_candidate_id") != local[qid].get("candidate_id"):
            errors.append(f"{cid}: local candidate link mismatch")
        if qid in external and row.get("external_candidate_id") != external[qid].get("candidate_id"):
            errors.append(f"{cid}: external candidate link mismatch")
        evidence = row.get("evidence") or {}
        local_text = (local.get(qid) or {}).get("candidate_text") or ""
        external_text = (external.get(qid) or {}).get("answer_candidate_text") or ""
        if bool(row.get("local_candidate_available")) != bool(local_text):
            errors.append(f"{cid}: local availability mismatch")
        if bool(row.get("external_candidate_available")) != bool(external_text):
            errors.append(f"{cid}: external availability mismatch")
        if evidence.get("exact_text_match") != bool(local_text and external_text and local_text == external_text):
            errors.append(f"{cid}: exact match mismatch")
        if row.get("comparison_status") == "both_sources_missing" and (local_text or external_text):
            errors.append(f"{cid}: both-missing status has candidate text")
        if evidence.get("local_candidate_sha256") not in {None, (local.get(qid) or {}).get("candidate_text_sha256")}:
            errors.append(f"{cid}: local hash link mismatch")
        if evidence.get("external_candidate_sha256") not in {None, (external.get(qid) or {}).get("answer_candidate_sha256")}:
            errors.append(f"{cid}: external hash link mismatch")
    main_sha = sha_bytes(MAIN.read_bytes()) if MAIN.exists() else None
    if main_sha != EXPECTED_MAIN_SHA256:
        errors.append(f"main answer index hash changed: {main_sha}")
    if MAIN.exists():
        main_rows = load(MAIN)
        missing = [r for r in main_rows if r.get("question_id") in range(1, 22) and not (r.get("answer_text") or "") and r.get("answer_status") in {"missing", "N/A"}]
        if len(missing) != 21:
            errors.append(f"main answer index missing gate changed: {len(missing)}")
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8")) if RECEIPT.exists() else {}
    if receipt.get("inputs", {}).get("main_answer_index", {}).get("sha256") != main_sha:
        errors.append("receipt main-index hash does not match current index")
    result = {
        "schema_version": "reference-answer-candidate-comparison-validation-2013-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "errors": errors,
        "checks": {
            "coverage": [row.get("question_id") for row in rows] == list(range(1, 22)),
            "candidate_links": not any("link mismatch" in e for e in errors),
            "authority_and_scoring_gate": not any("gate escaped" in e for e in errors),
            "no_silent_adjudication": not any("silently adjudicated" in e for e in errors),
            "main_answer_index_unchanged": not any("main answer index" in e or "receipt main-index" in e for e in errors),
            "m0_gate": not any("mapping gate" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
