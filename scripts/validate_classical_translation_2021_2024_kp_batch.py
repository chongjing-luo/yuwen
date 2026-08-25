#!/usr/bin/env python3
"""Validate the 2021--2024 classical-translation candidate batch."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "work/knowledge/exams/workbench/kp_batches/classical_translation_2021_2024.jsonl"
REPORT = ROOT / "work/knowledge/_meta/classical_translation_2021_2024_kp_batch_validation_20260809.json"
EXPECTED_COUNTS = {2021: 1, 2022: 1, 2023: 1, 2024: 2}
EXPECTED_NODES = {
    "GK-NCA-2021-Q013-TOP",
    "GK-NCA-2022-Q013-TOP",
    "GK-NCA-2023-Q013-TOP",
    "GK-NCA-2024-Q013-1",
    "GK-NCA-2024-Q013-2",
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def main() -> int:
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    errors: list[str] = []
    actual = Counter(row.get("year") for row in rows)
    node_ids = {row.get("exam_node_id") for row in rows}
    if len(rows) != sum(EXPECTED_COUNTS.values()):
        errors.append(f"row_count={len(rows)} expected={sum(EXPECTED_COUNTS.values())}")
    if dict(actual) != EXPECTED_COUNTS:
        errors.append(f"year_counts={dict(actual)} expected={EXPECTED_COUNTS}")
    if node_ids != EXPECTED_NODES:
        errors.append(f"node_ids={sorted(node_ids)} expected={sorted(EXPECTED_NODES)}")
    for row in rows:
        node = row.get("exam_node_id")
        if row.get("response_form") != "free_response_translation":
            errors.append(f"{node}: wrong response form")
        if row.get("analysis_scope") != "shared_top_level_analysis_segment":
            errors.append(f"{node}: shared analysis scope not declared")
        if row.get("answer_candidate") is not None or row.get("answer_candidate_method") != "free_response_not_auto_extracted":
            errors.append(f"{node}: free-response answer was auto-extracted")
        if "【答案】" in (row.get("knowledge_evidence_excerpt") or ""):
            errors.append(f"{node}: adjacent answer marker leaked into evidence excerpt")
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
        if row.get("answer_candidate_status") != "free_response_candidate_source":
            errors.append(f"{node}: unexpected candidate status")
        if row.get("manual_review_gate") != "free_response_answer_and_scoring_review_required":
            errors.append(f"{node}: missing free-response review gate")
        if row.get("source_authority_status") != "unverified_local_provided":
            errors.append(f"{node}: authority status was upgraded unexpectedly")
    result = {
        "schema_version": "classical-translation-2021-2024-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "row_count": len(rows),
        "year_counts": dict(actual),
        "errors": errors,
        "checks": {
            "coverage": len(rows) == sum(EXPECTED_COUNTS.values()) and dict(actual) == EXPECTED_COUNTS and node_ids == EXPECTED_NODES,
            "traceability": not any("missing" in error or "hash mismatch" in error for error in errors),
            "free_response_gate": not any("auto-extracted" in error or "review gate" in error for error in errors),
            "shared_scope_gate": not any("shared analysis scope" in error for error in errors),
            "m0_boundary": not any("mapping boundary" in error for error in errors),
            "answer_marker_boundary": not any("answer marker" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
