#!/usr/bin/env python3
"""Validate the 2023 local-vs-partial-external comparison layer."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers"
LOCAL = BASE / "local_analysis_group_candidates.jsonl"
EXTERNAL = BASE / "reference_answer_candidates.jsonl"
OUT = BASE / "reference_answer_candidate_comparison.jsonl"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_comparison_validation_2023_20260809.json"
EXTERNAL_QIDS = [1, 2, 3, 6, 7, 8, 9, 10]
ALLOWED = {
    "textually_consistent_unverified",
    "external_source_missing_local_candidate_only",
    "local_mixed_analysis_no_explicit_answer",
    "external_missing_local_mixed_analysis",
    "writing_artifact_no_external",
    "text_difference_requires_review",
}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compact(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"[\s，,。；;：:、．.（）()【】「」‘’“”《》!?！？\-—_]+", "", text)


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []
    rows = load(OUT) if OUT.exists() else []
    local = {int(r["question_id"]): r for r in load(LOCAL)} if LOCAL.exists() else {}
    external = {int(r["question_id"]): r for r in load(EXTERNAL)} if EXTERNAL.exists() else {}
    ids = [r.get("question_id") for r in rows]
    if ids != list(range(1, 23)):
        errors.append(f"comparison coverage/order={ids}")
    if sorted(local) != list(range(1, 23)):
        errors.append("local group candidate coverage is not Q1..Q22")
    if sorted(external) != EXTERNAL_QIDS:
        errors.append(f"external coverage={sorted(external)}, expected={EXTERNAL_QIDS}")
    if len({r.get("comparison_id") for r in rows}) != len(rows):
        errors.append("duplicate comparison_id")
    for row in rows:
        qid = int(row.get("question_id", -1))
        cid = row.get("comparison_id", "?")
        status = row.get("comparison_status")
        if status not in ALLOWED:
            errors.append(f"{cid}: unknown comparison status")
        if row.get("adjudication") != "not_adjudicated":
            errors.append(f"{cid}: silently adjudicated")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{cid}: scoring gate escaped")
        if (row.get("mapping_level"), row.get("kp_id")) != ("M0", "N/A"):
            errors.append(f"{cid}: M0 gate escaped")
        local_text = (local.get(qid) or {}).get("candidate_text") or ""
        external_text = (external.get(qid) or {}).get("answer_candidate_text") or ""
        evidence = row.get("evidence") or {}
        if evidence.get("exact_text_match") != bool(local_text and external_text and local_text == external_text):
            errors.append(f"{cid}: exact evidence mismatch")
        if evidence.get("compact_text_match") != bool(local_text and external_text and compact(local_text) == compact(external_text)):
            errors.append(f"{cid}: compact evidence mismatch")
        if bool(row.get("local_candidate_available")) != bool(local_text):
            errors.append(f"{cid}: local availability mismatch")
        if bool(row.get("external_candidate_available")) != bool(external_text):
            errors.append(f"{cid}: external availability mismatch")
        if row.get("local_candidate_id") != (local.get(qid) or {}).get("candidate_id"):
            errors.append(f"{cid}: local link mismatch")
        if row.get("external_candidate_id") != (external.get(qid) or {}).get("candidate_id"):
            errors.append(f"{cid}: external link mismatch")
    result = {
        "schema_version": "reference-answer-candidate-comparison-validation-2023-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "errors": errors,
        "checks": {
            "coverage": ids == list(range(1, 23)),
            "candidate_links": not any("link mismatch" in e for e in errors),
            "evidence": not any("evidence mismatch" in e for e in errors),
            "no_silent_adjudication": not any("silently adjudicated" in e for e in errors),
            "authority_and_scoring_gate": not any("gate escaped" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
