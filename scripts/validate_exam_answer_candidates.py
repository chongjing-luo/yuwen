#!/usr/bin/env python3
"""Validate the reversible answer-candidate derivatives."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract"
REPORT = ROOT / "work/knowledge/_meta/exam_answer_candidate_validation_20260809.json"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_exam(base: Path) -> dict:
    index = base / "answers" / "answer_index.jsonl"
    candidate_file = base / "answers" / "answer_candidates.jsonl"
    errors: list[str] = []
    if not index.exists():
        if candidate_file.exists():
            errors.append("candidate file exists without answer index")
        return {"exam_id": base.name, "index_present": False, "candidate_present": False, "rows": 0, "errors": errors}
    if not candidate_file.exists():
        errors.append("candidate file missing")
        return {"exam_id": base.name, "index_present": True, "candidate_present": False, "rows": 0, "errors": errors}
    source_rows = load(index)
    candidate_rows = load(candidate_file)
    if len(source_rows) != len(candidate_rows):
        errors.append(f"row_count={len(candidate_rows)} expected={len(source_rows)}")
    for number, (source, candidate) in enumerate(zip(source_rows, candidate_rows), 1):
        if source.get("answer_pair_id") != candidate.get("answer_pair_id"):
            errors.append(f"row {number}: answer_pair_id mismatch")
        raw = source.get("answer_text") or ""
        text = candidate.get("answer_candidate_text") or ""
        if candidate.get("raw_answer_text_sha256") != (digest(raw) if raw else None):
            errors.append(f"row {number}: raw answer hash mismatch")
        if candidate.get("answer_candidate_sha256") != (digest(text) if text else None):
            errors.append(f"row {number}: candidate hash mismatch")
        if raw and candidate.get("candidate_status") != "candidate_unverified":
            errors.append(f"row {number}: non-empty raw answer was not retained as candidate")
        if not raw and candidate.get("candidate_status") != "missing":
            errors.append(f"row {number}: empty raw answer not marked missing")
        if candidate.get("scoring_status") != "not_available_as_official":
            errors.append(f"row {number}: scoring status escaped conservative boundary")
    return {
        "exam_id": base.name,
        "index_present": True,
        "candidate_present": True,
        "rows": len(candidate_rows),
        "errors": errors,
    }


def main() -> int:
    reports = [validate_exam(base) for base in sorted(EXTRACT.iterdir()) if base.is_dir()]
    errors = [f"{report['exam_id']}: {error}" for report in reports for error in report["errors"]]
    result = {
        "schema_version": "exam-answer-candidate-validation-0.1",
        "result": "passed" if not errors else "failed",
        "exam_count": len(reports),
        "candidate_file_count": sum(1 for report in reports if report["candidate_present"]),
        "candidate_row_count": sum(report["rows"] for report in reports),
        "errors": errors,
        "years": reports,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
