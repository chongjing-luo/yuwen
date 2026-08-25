#!/usr/bin/env python3
"""Validate the first word-pronunciation candidate KP batch."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "work/knowledge/exams/workbench/kp_batches/word_pronunciation_2008_2015.jsonl"
REPORT = ROOT / "work/knowledge/_meta/word_pronunciation_kp_batch_validation_20260809.json"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text.split("---\n\n", 2)[-1].strip()


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    if len(rows) != 8:
        errors.append(f"row_count={len(rows)} expected=8")
    years = [row.get("year") for row in rows]
    if years != list(range(2008, 2016)):
        errors.append(f"years={years} expected=2008..2015")
    for row in rows:
        node = row.get("exam_node_id")
        for field in ("candidate_atomic_exam_point", "candidate_ability_action", "kp_id", "mapping_level", "manual_review_gate"):
            if field not in row:
                errors.append(f"{node}: missing {field}")
        if row.get("kp_id") != "N/A" or row.get("mapping_level") != "M0":
            errors.append(f"{node}: mapping boundary escaped M0")
        question = row.get("prompt_source")
        if not question or not (ROOT / question).exists():
            errors.append(f"{node}: question source missing")
        pdf = row.get("prompt_source_pdf")
        if not pdf or not (ROOT / pdf).exists():
            errors.append(f"{node}: PDF source missing")
        analysis = row.get("analysis_source")
        if analysis:
            path = ROOT / analysis
            if not path.exists():
                errors.append(f"{node}: analysis source missing")
            else:
                text = source_body(path)
                if row.get("analysis_source_sha256") != digest(text):
                    errors.append(f"{node}: analysis hash mismatch")
        elif row.get("analysis_source_sha256") is not None:
            errors.append(f"{node}: absent analysis source has hash")
        if row.get("upstream_answer_source_status") == "missing" and row.get("manual_review_gate") != "source_authority_missing":
            errors.append(f"{node}: authority-missing source not gated")
        if row.get("answer_candidate") and row.get("answer_candidate_status") == "candidate_text_present_authority_missing" and row.get("upstream_answer_source_status") != "missing":
            errors.append(f"{node}: authority conflict state inconsistent")
    result = {
        "schema_version": "word-pronunciation-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "row_count": len(rows),
        "errors": errors,
        "checks": {
            "coverage": len(rows) == 8 and years == list(range(2008, 2016)),
            "traceability": not any("source missing" in error or "hash mismatch" in error for error in errors),
            "m0_boundary": not any("mapping boundary" in error for error in errors),
            "authority_gate": not any("gated" in error or "inconsistent" in error for error in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
