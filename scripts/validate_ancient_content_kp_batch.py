#!/usr/bin/env python3
"""Validate the ancient-content candidate batch."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from repository_source_policy import reference_is_available

ROOT = Path(__file__).resolve().parents[1]
BATCH = ROOT / "work/knowledge/exams/workbench/kp_batches/ancient_content_2009_2015.jsonl"
REPORT = ROOT / "work/knowledge/_meta/ancient_content_kp_batch_validation_20260809.json"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def main() -> int:
    rows = [json.loads(line) for line in BATCH.read_text(encoding="utf-8").splitlines() if line.strip()] if BATCH.exists() else []
    errors: list[str] = []
    if len(rows) != 7:
        errors.append(f"row_count={len(rows)} expected=7")
    years = sorted(row.get("year") for row in rows)
    if years != list(range(2009, 2016)):
        errors.append(f"years={years} expected=2009..2015")
    for row in rows:
        node = row.get("exam_node_id")
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
        "schema_version": "ancient-content-kp-batch-validation-0.1",
        "result": "passed" if not errors else "failed",
        "row_count": len(rows),
        "years": years,
        "errors": errors,
        "checks": {
            "coverage": len(rows) == 7 and years == list(range(2009, 2016)),
            "traceability": not any("missing" in error or "hash mismatch" in error for error in errors),
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
