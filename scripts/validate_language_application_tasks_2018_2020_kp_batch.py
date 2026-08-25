#!/usr/bin/env python3
"""Validate reversible 2018--2020 Q8/Q9 task derivatives and M0 gates."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "work/knowledge/exams/workbench/kp_batches/language_application_tasks_split_2018_2020.json"
BATCH = ROOT / "work/knowledge/exams/workbench/kp_batches/language_application_tasks_2018_2020.jsonl"
REPORT = ROOT / "work/knowledge/_meta/language_application_tasks_2018_2020_kp_batch_validation_20260809.json"
EXPECTED_UNITS = {
    (2018, 8): {"1", "2", "3", "4", "5"},
    (2018, 9): {"1"},
    (2019, 8): {"1", "2", "3"},
    (2019, 9): {"1"},
    (2020, 8): {"1", "2", "3"},
    (2020, 9): {"1"},
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 1)[1].strip()


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {"records": []}
    records = manifest.get("records", [])
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    q_records = [r for r in records if r.get("source_role") == "question"]
    if len(records) != 28:
        errors.append(f"manifest_count={len(records)} expected=28 (14 task units × question/analysis)")
    if len(q_records) != 14:
        errors.append(f"question_manifest_count={len(q_records)} expected=14")
    if len(rows) != 14:
        errors.append(f"batch_count={len(rows)} expected=14")
    actual = {}
    for r in q_records:
        actual.setdefault((r.get("year"), r.get("question_id")), set()).add(r.get("task_code"))
    if actual != EXPECTED_UNITS:
        errors.append(f"task_units={actual} expected={EXPECTED_UNITS}")
    for item in records:
        for key in ("task_source", "parent_source", "source_pdf", "source_mineru_md", "source_clean_md"):
            path = item.get(key)
            if not path or not (ROOT / path).exists():
                errors.append(f"manifest: missing {key}={path}")
        task_path = ROOT / item["task_source"] if item.get("task_source") else None
        parent_path = ROOT / item["parent_source"] if item.get("parent_source") else None
        if task_path and task_path.exists() and item.get("task_sha256") != digest(body(task_path)):
            errors.append(f"manifest: task hash mismatch {item['task_source']}")
        if parent_path and parent_path.exists() and item.get("parent_sha256") != digest(body(parent_path)):
            errors.append(f"manifest: parent hash mismatch {item['parent_source']}")
        if item.get("year") == 2018 and item.get("question_id") == 8 and item.get("source_role") == "question":
            # The five configured units are lexical boundaries, not answers;
            # still require each cited source token to occur in the parent.
            label = item.get("task_label", "")
            token = label.split("“", 1)[1].split("”", 1)[0] if "“" in label and "”" in label else ""
            if token and parent_path and parent_path.exists() and token not in body(parent_path):
                errors.append(f"manifest: 2018 Q008 boundary token missing: {token}")
        for image in item.get("source_image_paths", []):
            if not (ROOT / image).exists():
                errors.append(f"manifest: missing image={image}")
    for row in rows:
        node = row.get("exam_node_id")
        if row.get("answer_candidate") is not None or row.get("answer_candidate_method") != "language_application_task_not_auto_extracted":
            errors.append(f"{node}: answer was auto-extracted")
        if row.get("score_candidate") is not None or row.get("score_status") != "question_total_only_not_allocated":
            errors.append(f"{node}: task score was invented")
        if row.get("kp_id") != "N/A" or row.get("mapping_level") != "M0":
            errors.append(f"{node}: mapping boundary escaped M0")
        for key in ("task_source", "parent_source", "source_pdf", "source_mineru_md", "source_clean_md"):
            path = row.get(key)
            if not path or not (ROOT / path).exists():
                errors.append(f"{node}: missing {key}")
        task_path = ROOT / row["task_source"]
        if task_path.exists() and row.get("task_source_sha256") != digest(body(task_path)):
            errors.append(f"{node}: task hash mismatch")
        parent_path = ROOT / row["parent_source"]
        if parent_path.exists() and row.get("parent_source_sha256") != digest(body(parent_path)):
            errors.append(f"{node}: parent hash mismatch")
        if row.get("year") == 2020 and row.get("question_id") == 8 and "OCR" not in " ".join(row.get("source_warnings", [])):
            errors.append(f"{node}: 2020 Q008 OCR warning was dropped")
    result = {
        "schema_version": "language-application-tasks-2018-2020-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "manifest_count": len(records),
        "question_manifest_count": len(q_records),
        "batch_count": len(rows),
        "errors": errors,
        "checks": {
            "coverage": len(records) == 28 and len(q_records) == 14 and len(rows) == 14 and actual == EXPECTED_UNITS,
            "split_traceability": not any("manifest" in e or "missing" in e or "hash mismatch" in e for e in errors),
            "answer_gate": not any("answer was auto-extracted" in e for e in errors),
            "score_gate": not any("score was invented" in e for e in errors),
            "m0_boundary": not any("mapping boundary" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
