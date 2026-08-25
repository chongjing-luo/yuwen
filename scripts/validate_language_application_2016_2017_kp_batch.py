#!/usr/bin/env python3
"""Validate the stable 2016--2017 language-application batch."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from repository_source_policy import reference_is_available

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "work/knowledge/exams/workbench/kp_batches/language_application_2016_2017.jsonl"
REPORT = ROOT / "work/knowledge/_meta/language_application_2016_2017_kp_batch_validation_20260809.json"
EXPECTED_SUBTYPES = {
    "idiom_usage": 2,
    "sentence_error": 2,
    "discourse_connective_selection": 2,
    "completion": 2,
    "constructed_language_response": 2,
}
EXPECTED_NODES = {f"GK-NC3-{year}-Q{qid:03d}-TOP" for year in (2016, 2017) for qid in range(7, 12)}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def main() -> int:
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    errors: list[str] = []
    subtypes = Counter(row.get("candidate_subtype") for row in rows)
    nodes = {row.get("exam_node_id") for row in rows}
    if len(rows) != 10:
        errors.append(f"row_count={len(rows)} expected=10")
    if dict(subtypes) != EXPECTED_SUBTYPES:
        errors.append(f"subtype_counts={dict(subtypes)} expected={EXPECTED_SUBTYPES}")
    if nodes != EXPECTED_NODES:
        errors.append(f"node_ids={sorted(nodes)} expected={sorted(EXPECTED_NODES)}")
    for row in rows:
        node = row.get("exam_node_id")
        if row.get("question_type_l2") != "language_application":
            errors.append(f"{node}: wrong source type")
        if row.get("answer_candidate") is not None or row.get("answer_candidate_method") != "language_application_not_auto_extracted":
            errors.append(f"{node}: answer was auto-extracted")
        if row.get("kp_id") != "N/A" or row.get("mapping_level") != "M0":
            errors.append(f"{node}: mapping boundary escaped M0")
        if row.get("analysis_scope") != "question_segment_with_possible_related_context":
            errors.append(f"{node}: related-context scope not declared")
        if row.get("manual_review_gate") != "language_application_answer_and_scoring_review_required":
            errors.append(f"{node}: review gate not retained")
        for key in ("prompt_source", "prompt_source_pdf", "analysis_source"):
            path = row.get(key)
            if not path or not reference_is_available(ROOT, path):
                errors.append(f"{node}: missing {key}")
        analysis = ROOT / row["analysis_source"]
        if analysis.exists() and row.get("analysis_source_sha256") != digest(source_body(analysis)):
            errors.append(f"{node}: analysis hash mismatch")
    result = {
        "schema_version": "language-application-2016-2017-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "row_count": len(rows),
        "subtype_counts": dict(subtypes),
        "node_ids": sorted(nodes),
        "errors": errors,
        "checks": {
            "coverage": len(rows) == 10 and dict(subtypes) == EXPECTED_SUBTYPES and nodes == EXPECTED_NODES,
            "traceability": not any("missing" in error or "hash mismatch" in error for error in errors),
            "answer_gate": not any("auto-extracted" in error for error in errors),
            "m0_boundary": not any("mapping boundary" in error for error in errors),
            "review_gate": not any("review gate" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
