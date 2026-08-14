#!/usr/bin/env python3
"""Validate the isolated 2009 Q1--Q6 third-party candidate layer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/answers"
SOURCE_DIR = ROOT / "Data/reference/gaokao/external/2009_gaokao_answer"
OUT = BASE / "reference_answer_candidates.jsonl"
MAIN_INDEX = BASE / "answer_index.jsonl"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2009_20260809.json"
EXPECTED = {1: "D", 2: "C", 3: "D", 4: "C", 5: "（1）D；（2）A；（3）A", 6: "（1）B；（2）B；（3）B；（4）①大概用来治理天下国家的人，不再都从学校中产生。②我们虽然为它即将推行而感到高兴并且庆幸，但又担心后来的人不能继承我的思想，于是推究它的意义来告诉后来的人。"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip()] if OUT.exists() else []
    ids = [int(row.get("question_id", -1)) for row in rows]
    expected_ids = list(EXPECTED)
    if ids != expected_ids:
        errors.append(f"coverage={ids}, expected {expected_ids}")
    required = {
        "source_page": SOURCE_DIR / "scdfz_source.html",
        "source_pdf": SOURCE_DIR / "scdfz_answer.pdf",
        "source_gaokao_snapshot": SOURCE_DIR / "source.html",
    }
    for row in rows:
        cid = row.get("candidate_id", "?")
        qid = int(row.get("question_id", -1))
        text = row.get("answer_candidate_text") or ""
        excerpt = row.get("source_group_excerpt") or ""
        if text != EXPECTED.get(qid):
            errors.append(f"{cid}: candidate text mismatch")
        if row.get("answer_candidate_sha256") != sha_text(text):
            errors.append(f"{cid}: answer hash mismatch")
        if row.get("source_group_excerpt_sha256") != sha_text(excerpt):
            errors.append(f"{cid}: excerpt hash mismatch")
        if qid == 6:
            # Q6 is intentionally bounded at the source's “参考译文：” marker;
            # the long reference translation must not be mistaken for an
            # answer/scoring candidate excerpt.
            if not excerpt.startswith("答案："):
                errors.append(f"{cid}: Q6 excerpt does not start at 答案：")
            if "参考译文：" in excerpt:
                errors.append(f"{cid}: Q6 excerpt swallowed reference translation")
        for key, value in {
            "source_authority_status": "unverified_third_party_reprint",
            "source_status": "unverified_third_party_reprint",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "candidate_status": "candidate_unverified",
            "source_registry_id": "SRC-GK-2009-SC-DFZ-JYEEO-ANSWER-CANDIDATE",
        }.items():
            if row.get(key) != value:
                errors.append(f"{cid}: conservative gate changed: {key}")
        for key, path in required.items():
            if not path.exists() or row.get(f"{key}_sha256") != sha(path):
                errors.append(f"{cid}: {key} path/hash mismatch")
        if any(value in {"official_verified", "M1", "M2", "M3"} for value in row.values() if isinstance(value, str)):
            errors.append(f"{cid}: forbidden official/mapping label")
    if MAIN_INDEX.exists():
        errors.append("main answer index unexpectedly present")
    result = {
        "schema_version": "reference-answer-candidate-validation-2009-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "source_hashes": {path.name: sha(path) for path in required.values() if path.exists()},
        "main_index_present": MAIN_INDEX.exists(),
        "errors": errors,
        "checks": {
            "partial_coverage": ids == expected_ids,
            "source_hashes": not any("hash" in error or "path" in error for error in errors),
            "authority_gate": not any("gate" in error or "official" in error for error in errors),
            "main_index_unchanged_gate": not MAIN_INDEX.exists(),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
