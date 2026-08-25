#!/usr/bin/env python3
"""Validate the 2021--2024 language-application candidate batch."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from repository_source_policy import reference_is_available

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "work/knowledge/exams/workbench/kp_batches/language_application_2021_2024.jsonl"
REPORT = ROOT / "work/knowledge/_meta/language_application_2021_2024_kp_batch_validation_20260809.json"
EXPECTED_NODES = {f"GK-NCA-{year}-Q{qid:03d}-TOP" for year in (2021, 2022, 2023, 2024) for qid in range(17, 22)}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def main() -> int:
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    errors: list[str] = []
    nodes = {row.get("exam_node_id") for row in rows}
    if len(rows) != 20:
        errors.append(f"row_count={len(rows)} expected=20")
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
        expected_gate = "source_authority_missing" if row.get("year") == 2024 and row.get("question_id") == 21 else "language_application_answer_and_scoring_review_required"
        if row.get("manual_review_gate") != expected_gate:
            errors.append(f"{node}: gate={row.get('manual_review_gate')} expected={expected_gate}")
        for key in ("prompt_source", "prompt_source_pdf", "analysis_source"):
            path = row.get(key)
            if not path or not reference_is_available(ROOT, path):
                errors.append(f"{node}: missing {key}")
        analysis_path = ROOT / row["analysis_source"]
        if analysis_path.exists() and row.get("analysis_source_sha256") != digest(source_body(analysis_path)):
            errors.append(f"{node}: analysis hash mismatch")
        if row.get("year") == 2024 and row.get("question_id") == 21 and row.get("upstream_answer_source_status") != "missing":
            errors.append(f"{node}: expected upstream authority gap")
    result = {
        "schema_version": "language-application-2021-2024-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "row_count": len(rows),
        "node_ids": sorted(nodes),
        "errors": errors,
        "checks": {
            "coverage": len(rows) == 20 and nodes == EXPECTED_NODES,
            "traceability": not any("missing" in error or "hash mismatch" in error for error in errors),
            "answer_gate": not any("auto-extracted" in error for error in errors),
            "m0_boundary": not any("mapping boundary" in error for error in errors),
            "authority_gate": not any("gate=" in error or "authority gap" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
