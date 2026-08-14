#!/usr/bin/env python3
"""Validate the isolated 2010 third-party answer-candidate layer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/answers"
SOURCE_DIR = ROOT / "Data/reference/gaokao/external/2010_gaokao_answer"
OUT = BASE / "reference_answer_candidates.jsonl"
MAIN_INDEX = BASE / "answer_index.jsonl"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2010_20260809.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip()] if OUT.exists() else []
    ids = [int(row.get("question_id", -1)) for row in rows]
    expected = [1, 2, 4, 8, 9]
    if ids != expected:
        errors.append(f"coverage={ids}, expected {expected}")
    expected_answers = {1: "C", 2: "D", 4: "C", 8: "A", 9: "B"}
    required = [SOURCE_DIR / "source.html", SOURCE_DIR / "answer_bundle.rar",
                SOURCE_DIR / "四川语文答案.doc", SOURCE_DIR / "answer_source.txt"]
    for row in rows:
        cid = row.get("candidate_id", "?")
        qid = int(row.get("question_id", -1))
        text = row.get("answer_candidate_text") or ""
        excerpt = row.get("source_group_excerpt") or ""
        for key, value in {
            "source_authority_status": "unverified_third_party_reprint",
            "source_status": "unverified_third_party_reprint",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "candidate_status": "candidate_unverified",
        }.items():
            if row.get(key) != value:
                errors.append(f"{cid}: {key} escaped conservative boundary")
        if text != expected_answers.get(qid):
            errors.append(f"{cid}: answer {text!r} != {expected_answers.get(qid)!r}")
        if row.get("answer_candidate_sha256") != sha_text(text):
            errors.append(f"{cid}: answer hash mismatch")
        if row.get("source_group_excerpt_sha256") != sha_text(excerpt):
            errors.append(f"{cid}: excerpt hash mismatch")
        for key, path in {
            "source_html": SOURCE_DIR / "source.html",
            "source_rar": SOURCE_DIR / "answer_bundle.rar",
            "source_doc": SOURCE_DIR / "四川语文答案.doc",
            "source_text": SOURCE_DIR / "answer_source.txt",
        }.items():
            if not path.exists() or row.get(f"{key}_sha256") != sha(path):
                errors.append(f"{cid}: {key} path/hash mismatch")
        if row.get("source_line_start", 0) > row.get("source_line_end", 0):
            errors.append(f"{cid}: invalid source line interval")
        if any(value in {"official_verified", "M1", "M2", "M3"} for value in row.values() if isinstance(value, str)):
            errors.append(f"{cid}: forbidden official/mapping label")
    if MAIN_INDEX.exists():
        errors.append("main answer index unexpectedly present")
    result = {
        "schema_version": "reference-answer-candidate-validation-2010-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "source_hashes": {p.name: sha(p) for p in required if p.exists()},
        "main_index_present": MAIN_INDEX.exists(),
        "errors": errors,
        "checks": {
            "partial_coverage": ids == expected,
            "source_hashes": not any("hash" in error or "path" in error for error in errors),
            "authority_gate": not any("boundary" in error or "official" in error for error in errors),
            "main_index_unchanged_gate": not MAIN_INDEX.exists(),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
