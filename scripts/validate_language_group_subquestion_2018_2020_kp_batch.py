#!/usr/bin/env python3
"""Validate 2018--2020 language-group subquestion split and candidate batch."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "work/knowledge/exams/workbench/kp_batches/language_group_subquestion_split_2018_2020.json"
BATCH = ROOT / "work/knowledge/exams/workbench/kp_batches/language_group_subquestion_2018_2020.jsonl"
REPORT = ROOT / "work/knowledge/_meta/language_group_subquestion_2018_2020_kp_batch_validation_20260809.json"
EXPECTED_NODES = {f"GK-NC3-{year}-Q007-{code}" for year in (2018, 2019, 2020) for code in ("1", "2", "3")}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"records": []}
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    manifest_rows = manifest.get("records", [])
    nodes = {row.get("exam_node_id") for row in rows}
    if len(manifest_rows) != 9:
        errors.append(f"manifest_count={len(manifest_rows)} expected=9")
    if len(rows) != 9:
        errors.append(f"row_count={len(rows)} expected=9")
    if nodes != EXPECTED_NODES:
        errors.append(f"node_ids={sorted(nodes)} expected={sorted(EXPECTED_NODES)}")
    if {row.get("question_source") for row in manifest_rows}.__len__() != 9:
        errors.append("manifest question sources are not unique")
    for item in manifest_rows:
        for key in ("question_source", "analysis_source", "parent_question_source", "parent_analysis_source"):
            path = item.get(key)
            if not path or not (ROOT / path).exists():
                errors.append(f"manifest: missing {key}={path}")
        if item.get("question_source") and (ROOT / item["question_source"]).exists() and item.get("question_sha256") != digest(source_body(ROOT / item["question_source"])):
            errors.append(f"manifest: question hash mismatch {item['question_source']}")
        if item.get("analysis_source") and (ROOT / item["analysis_source"]).exists() and item.get("analysis_sha256") != digest(source_body(ROOT / item["analysis_source"])):
            errors.append(f"manifest: analysis hash mismatch {item['analysis_source']}")
    for row in rows:
        node = row.get("exam_node_id")
        if row.get("answer_candidate") is not None or row.get("answer_candidate_method") != "language_group_not_auto_extracted":
            errors.append(f"{node}: answer was auto-extracted")
        if row.get("kp_id") != "N/A" or row.get("mapping_level") != "M0":
            errors.append(f"{node}: mapping boundary escaped M0")
        if row.get("analysis_scope") != "derived_subquestion_with_parent_group_context":
            errors.append(f"{node}: wrong analysis scope")
        if row.get("score_candidate") is not None or row.get("score_status") != "group_total_only_not_allocated":
            errors.append(f"{node}: subquestion score was invented")
        for key in ("prompt_source", "analysis_source", "prompt_source_parent", "analysis_source_parent", "prompt_source_pdf"):
            path = row.get(key)
            if not path or not (ROOT / path).exists():
                errors.append(f"{node}: missing {key}")
        analysis = ROOT / row["analysis_source"]
        if analysis.exists() and row.get("analysis_source_sha256") != digest(source_body(analysis)):
            errors.append(f"{node}: analysis hash mismatch")
    result = {
        "schema_version": "language-group-subquestion-2018-2020-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "manifest_count": len(manifest_rows),
        "row_count": len(rows),
        "node_ids": sorted(nodes),
        "errors": errors,
        "checks": {
            "coverage": len(manifest_rows) == 9 and len(rows) == 9 and nodes == EXPECTED_NODES,
            "split_traceability": not any("manifest" in error or "missing" in error or "hash mismatch" in error for error in errors),
            "answer_gate": not any("auto-extracted" in error for error in errors),
            "score_gate": not any("score was invented" in error for error in errors),
            "m0_boundary": not any("mapping boundary" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
