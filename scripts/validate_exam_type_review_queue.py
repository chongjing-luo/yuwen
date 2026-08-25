#!/usr/bin/env python3
"""Validate the cross-year exam type review queue."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from repository_source_policy import reference_is_available

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "work/knowledge/exams/workbench/exam_type_review_queue.jsonl"
TYPE_DIR = ROOT / "work/knowledge/exams/workbench/type_review_queue"
REPORT = ROOT / "work/knowledge/_meta/exam_type_review_queue_validation_20260809.json"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def wikilink(path: str | None, label: str) -> str:
    return f"[[{path}|{label}]]" if path else "N/A"


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in QUEUE.read_text(encoding="utf-8").splitlines() if line.strip()] if QUEUE.exists() else []
    source_rows: dict[str, dict] = {}
    for path in ROOT.joinpath("work/knowledge/exams/workbench").glob("*-response_nodes_vertical_slice.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                source = json.loads(line)
                source_rows[source["response_node_id"]] = source
    if len(rows) != 359:
        errors.append(f"queue rows={len(rows)} expected=359")
    ids = [row.get("queue_id") for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate queue_id")
    for row in rows:
        required = ("queue_id", "exam_node_id", "question_type_l2", "candidate_atomic_exam_point", "prompt_sha256", "kp_id", "mapping_level", "manual_review_gate")
        for field in required:
            if field not in row:
                errors.append(f"{row.get('queue_id')}: missing {field}")
        source_row = source_rows.get(row.get("exam_node_id"))
        if not source_row:
            errors.append(f"{row.get('queue_id')}: source vertical node missing")
        else:
            source_prompt = source_row.get("prompt_text_for_extraction") or source_row.get("prompt_text") or source_row.get("prompt_text_raw") or ""
            if row.get("prompt_sha256") != digest(source_prompt):
                errors.append(f"{row.get('queue_id')}: prompt hash mismatch")
        if row.get("mapping_level") != "M0" or row.get("kp_id") != "N/A":
            errors.append(f"{row.get('queue_id')}: mapping boundary escaped M0")
        for field, label in (
            ("source_question_segment", "question segment"),
            ("source_clean_md", "clean copy"),
            ("source_mineru_md", "raw MinerU"),
            ("source_pdf", "raw PDF"),
        ):
            source = row.get(field)
            if not source or not reference_is_available(ROOT, source):
                errors.append(f"{row.get('queue_id')}: missing {label} source")
        if row.get("answer_source_status") == "missing" and row.get("manual_review_gate") != "answer_source_missing":
            errors.append(f"{row.get('queue_id')}: missing answer not gated")
    types = sorted({row.get("question_type_l2") for row in rows})
    missing_type_files = [name for name in types if not (TYPE_DIR / f"{name}.md").exists()]
    errors.extend(f"missing type queue file: {name}" for name in missing_type_files)
    type_documents = {
        name: (TYPE_DIR / f"{name}.md").read_text(encoding="utf-8")
        for name in types
        if (TYPE_DIR / f"{name}.md").exists()
    }
    for row in rows:
        type_document = type_documents.get(row.get("question_type_l2"), "")
        for field, label in (
            ("source_question_segment", "题干"),
            ("source_clean_md", "清洗稿"),
            ("source_mineru_md", "原始 MinerU"),
            ("source_pdf", "原始 PDF"),
        ):
            expected_link = wikilink(row.get(field), label)
            if expected_link not in type_document:
                errors.append(f"{row.get('queue_id')}: type page missing {label} link")
    result = {
        "schema_version": "exam-type-review-queue-validation-0.1",
        "result": "passed" if not errors else "failed",
        "queue_rows": len(rows),
        "type_count": len(types),
        "errors": errors,
        "checks": {
            "row_count": len(rows) == 359,
            "unique_ids": len(ids) == len(set(ids)),
            "m0_boundary": not any("mapping boundary" in error for error in errors),
            "source_traceability": not any("missing " in error and " source" in error for error in errors),
            "type_page_traceability": not any("type page missing" in error for error in errors),
            "type_files": not missing_type_files,
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
