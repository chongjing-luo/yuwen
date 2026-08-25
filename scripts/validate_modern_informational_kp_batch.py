#!/usr/bin/env python3
"""Validate the modern informational-reading candidate batch."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from repository_source_policy import reference_is_available

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "work/knowledge/exams/workbench/kp_batches/modern_informational_2009_2015.jsonl"
REPORT = ROOT / "work/knowledge/_meta/modern_informational_kp_batch_validation_20260809.json"
EXPECTED_COUNTS = {year: 3 for year in range(2009, 2016)}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def main() -> int:
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    errors: list[str] = []
    actual = Counter(row.get("year") for row in rows)
    if len(rows) != 21:
        errors.append(f"row_count={len(rows)} expected=21")
    if dict(actual) != EXPECTED_COUNTS:
        errors.append(f"year_counts={dict(actual)} expected={EXPECTED_COUNTS}")
    for row in rows:
        node = row.get("exam_node_id")
        if row.get("response_form") != "objective_informational_reading":
            errors.append(f"{node}: wrong response form")
        if row.get("analysis_scope") != "question_segment_with_possible_related_context":
            errors.append(f"{node}: related-context scope not declared")
        if row.get("answer_candidate") is not None or row.get("answer_candidate_method") != "objective_answer_not_auto_extracted":
            errors.append(f"{node}: objective answer was auto-extracted")
        if row.get("kp_id") != "N/A" or row.get("mapping_level") != "M0":
            errors.append(f"{node}: mapping boundary escaped M0")
        for key in ("prompt_source", "prompt_source_pdf"):
            path = row.get(key)
            if not path or not reference_is_available(ROOT, path):
                errors.append(f"{node}: missing {key}")
        analysis = row.get("analysis_source")
        if analysis:
            path = ROOT / analysis
            if not path.exists():
                errors.append(f"{node}: analysis source missing")
            elif row.get("analysis_source_sha256") != digest(source_body(path)):
                errors.append(f"{node}: analysis hash mismatch")
        if row.get("upstream_answer_source_status") == "missing" and row.get("manual_review_gate") != "source_authority_missing":
            errors.append(f"{node}: authority-missing source not gated")
    result = {
        "schema_version": "modern-informational-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "row_count": len(rows),
        "year_counts": dict(actual),
        "errors": errors,
        "checks": {
            "coverage": len(rows) == 21 and dict(actual) == EXPECTED_COUNTS,
            "traceability": not any("missing" in error or "hash mismatch" in error for error in errors),
            "objective_gate": not any("auto-extracted" in error for error in errors),
            "m0_boundary": not any("mapping boundary" in error for error in errors),
            "authority_gate": not any("not gated" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
