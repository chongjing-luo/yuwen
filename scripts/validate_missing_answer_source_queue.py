#!/usr/bin/env python3
"""Validate the conservative missing-answer-source review queue."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERTICAL = ROOT / "work/knowledge/高考分析/GK-SC-2013-response_nodes_vertical_slice.jsonl"
INDEX = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/answer_index.jsonl"
QUEUE = ROOT / "work/knowledge/高考分析/EXAM-MISSING-SOURCE-REVIEW-QUEUE-20260809.jsonl"
REPORT = ROOT / "work/knowledge/_meta/missing_answer_source_queue_validation_20260809.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []
    required = [VERTICAL, INDEX, QUEUE]
    missing = [str(p.relative_to(ROOT)) for p in required if not p.exists()]
    if missing:
        errors.extend(f"missing input: {p}" for p in missing)
    if errors:
        result = {"schema_version": "exam-missing-answer-source-queue-validation-0.1", "result": "failed", "errors": errors}
        REPORT.parent.mkdir(parents=True, exist_ok=True)
        REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    vertical = rows(VERTICAL)
    index = rows(INDEX)
    queue = rows(QUEUE)
    expected = {r["response_node_id"]: r for r in vertical if r.get("answer_source_status") == "missing"}
    ids = [r.get("response_node_id") for r in queue]
    if len(queue) != 23:
        errors.append(f"queue row count={len(queue)}, expected 23")
    if len(ids) != len(set(ids)):
        errors.append("duplicate response_node_id")
    if set(ids) != set(expected):
        errors.append("queue coverage differs from vertical missing-source nodes")
    index_by_qid = {int(r["question_id"]): r for r in index}
    for row in queue:
        node_id = row.get("response_node_id", "?")
        source = expected.get(node_id)
        if source is None:
            continue
        if row.get("exam_id") != "GK-SC-2013":
            errors.append(f"{node_id}: exam_id changed")
        if row.get("mapping_level") != "M0" or row.get("kp_id") != "N/A":
            errors.append(f"{node_id}: non-M0 mapping")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{node_id}: scoring gate changed")
        if any(value in {"official_verified", "M1", "M2", "M3"} for value in row.values() if isinstance(value, str)):
            errors.append(f"{node_id}: forbidden authority/mapping label")
        qid = int(row.get("question_id", -1))
        indexed = index_by_qid.get(qid, {})
        if indexed.get("answer_status") != "missing" or indexed.get("source_status") != "missing":
            errors.append(f"{node_id}: main answer index no longer explicitly missing")
        if row.get("question_source") != source.get("source_question_segment"):
            errors.append(f"{node_id}: question source link mismatch")
        if row.get("analysis_source") != source.get("source_analysis_segment"):
            errors.append(f"{node_id}: analysis source link mismatch")
        for key in ("question_source", "analysis_source", "source_pdf", "source_mineru_md"):
            value = row.get(key)
            if not value or not (ROOT / value).exists():
                errors.append(f"{node_id}: missing traceable path {key}")
    result = {
        "schema_version": "exam-missing-answer-source-queue-validation-0.1",
        "result": "passed" if not errors else "failed",
        "queue_rows": len(queue),
        "vertical_missing_nodes": len(expected),
        "errors": errors,
        "inputs": {str(path.relative_to(ROOT)): sha(path) for path in required},
        "checks": {
            "coverage": len(queue) == 23 and set(ids) == set(expected),
            "unique_ids": len(ids) == len(set(ids)),
            "m0_boundary": not any("M0" in error or "gate changed" in error for error in errors),
            "main_index_explicit_missing": not any("main answer index" in error for error in errors),
            "source_traceability": not any("source" in error or "path" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
