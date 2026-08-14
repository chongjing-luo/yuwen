#!/usr/bin/env python3
"""Validate the six remaining language-task candidate records."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "work/knowledge/高考分析/kp_batches/remaining_language_2009_2015.jsonl"
REPORT = ROOT / "work/knowledge/_meta/remaining_language_kp_batch_validation_20260809.json"
EXPECTED_COUNTS = {"sentence_segmentation": 3, "summary_or_application": 3}
EXPECTED_NODES = {f"GK-SC-{year}-Q012-TOP" for year in (2013, 2014, 2015)} | {f"GK-SC-{year}-Q019-TOP" for year in (2013, 2014, 2015)}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def main() -> int:
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    errors: list[str] = []
    actual = Counter(row.get("question_type_l2") for row in rows)
    node_ids = {row.get("exam_node_id") for row in rows}
    if len(rows) != 6:
        errors.append(f"row_count={len(rows)} expected=6")
    if dict(actual) != EXPECTED_COUNTS:
        errors.append(f"type_counts={dict(actual)} expected={EXPECTED_COUNTS}")
    if node_ids != EXPECTED_NODES:
        errors.append(f"node_ids={sorted(node_ids)} expected={sorted(EXPECTED_NODES)}")
    for row in rows:
        node = row.get("exam_node_id")
        if row.get("answer_candidate") is not None or row.get("answer_candidate_method") != "remaining_language_not_auto_extracted":
            errors.append(f"{node}: answer was auto-extracted")
        if row.get("kp_id") != "N/A" or row.get("mapping_level") != "M0":
            errors.append(f"{node}: mapping boundary escaped M0")
        if row.get("analysis_scope") != "question_segment_with_possible_related_context":
            errors.append(f"{node}: related-context scope not declared")
        for key in ("prompt_source", "prompt_source_pdf"):
            path = row.get(key)
            if not path or not (ROOT / path).exists():
                errors.append(f"{node}: missing {key}")
        analysis = row.get("analysis_source")
        if not analysis:
            errors.append(f"{node}: missing analysis source field")
        else:
            path = ROOT / analysis
            if not path.exists():
                errors.append(f"{node}: analysis source missing")
            elif row.get("analysis_source_sha256") != digest(source_body(path)):
                errors.append(f"{node}: analysis hash mismatch")
        if row.get("year") == 2013 and row.get("manual_review_gate") != "source_authority_missing":
            errors.append(f"{node}: 2013 authority-missing source not gated")
        if row.get("year") in {2014, 2015} and row.get("manual_review_gate") != "remaining_language_answer_and_scoring_review_required":
            errors.append(f"{node}: review gate not retained")
    result = {
        "schema_version": "remaining-language-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "row_count": len(rows),
        "type_counts": dict(actual),
        "node_ids": sorted(node_ids),
        "errors": errors,
        "checks": {
            "coverage": len(rows) == 6 and dict(actual) == EXPECTED_COUNTS and node_ids == EXPECTED_NODES,
            "traceability": not any("missing" in error or "hash mismatch" in error for error in errors),
            "answer_gate": not any("auto-extracted" in error for error in errors),
            "m0_boundary": not any("mapping boundary" in error for error in errors),
            "authority_gate": not any("not gated" in error or "gate not retained" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
