#!/usr/bin/env python3
"""Validate the 2016--2024 informational-reading candidate batch."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "work/knowledge/exams/workbench/kp_batches/modern_informational_2016_2024.jsonl"
REPORT = ROOT / "work/knowledge/_meta/modern_informational_2016_2024_kp_batch_validation_20260809.json"
EXPECTED_COUNTS = {2016: 3, 2017: 3, 2018: 1, 2019: 1, 2020: 1, 2021: 3, 2022: 3, 2023: 3, 2024: 3}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def main() -> int:
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    errors: list[str] = []
    actual = Counter(row.get("year") for row in rows)
    if len(rows) != sum(EXPECTED_COUNTS.values()):
        errors.append(f"row_count={len(rows)} expected={sum(EXPECTED_COUNTS.values())}")
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
            if not path or not (ROOT / path).exists():
                errors.append(f"{node}: missing {key}")
        analysis = row.get("analysis_source")
        if analysis:
            path = ROOT / analysis
            if not path.exists():
                errors.append(f"{node}: analysis source missing")
            elif row.get("analysis_source_sha256") != digest(source_body(path)):
                errors.append(f"{node}: analysis hash mismatch")
        if row.get("answer_candidate_status") != "objective_candidate_source":
            errors.append(f"{node}: unexpected candidate status")
        if row.get("manual_review_gate") != "objective_answer_and_evidence_review_required":
            errors.append(f"{node}: missing objective review gate")
    result = {
        "schema_version": "modern-informational-2016-2024-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "row_count": len(rows),
        "year_counts": dict(actual),
        "errors": errors,
        "checks": {
            "coverage": len(rows) == sum(EXPECTED_COUNTS.values()) and dict(actual) == EXPECTED_COUNTS,
            "traceability": not any("missing" in error or "hash mismatch" in error for error in errors),
            "objective_gate": not any("auto-extracted" in error or "review gate" in error for error in errors),
            "related_scope_gate": not any("related-context scope" in error for error in errors),
            "m0_boundary": not any("mapping boundary" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
