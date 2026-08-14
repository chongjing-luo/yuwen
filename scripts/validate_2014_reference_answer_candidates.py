#!/usr/bin/env python3
"""Validate the isolated 2014 Q1--Q9 image candidate layer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/answers"
SOURCE_DIR = ROOT / "Data/reference/gaokao/external/2014_gaokao_answer"
OUT = BASE / "reference_answer_candidates.jsonl"
MAIN_INDEX = BASE / "answer_index.jsonl"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2014_20260809.json"
EXPECTED = {1: "A", 2: "D", 3: "D", 4: "B", 5: "C", 6: "C", 7: "D", 8: "B", 9: "B"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip()] if OUT.exists() else []
    ids = sorted(int(r.get("question_id", -1)) for r in rows)
    if ids != list(EXPECTED):
        errors.append(f"coverage={ids}, expected {list(EXPECTED)}")
    html, image = SOURCE_DIR / "source.html", SOURCE_DIR / "page1.jpg"
    for row in rows:
        cid = row.get("candidate_id", "?")
        qid = int(row.get("question_id", -1))
        text = row.get("answer_candidate_text") or ""
        excerpt = row.get("source_group_excerpt") or ""
        if text != EXPECTED.get(qid): errors.append(f"{cid}: answer transcription mismatch")
        if row.get("answer_candidate_sha256") != sha_text(text): errors.append(f"{cid}: answer hash mismatch")
        if row.get("source_group_excerpt_sha256") != sha_text(excerpt): errors.append(f"{cid}: excerpt hash mismatch")
        for key, expected in {"source_authority_status": "unverified_third_party_reprint", "scoring_status": "not_available_as_official", "mapping_level": "M0", "kp_id": "N/A"}.items():
            if row.get(key) != expected: errors.append(f"{cid}: {key} gate changed")
        if row.get("source_image_sha256") != sha(image) or row.get("source_page_sha256") != sha(html): errors.append(f"{cid}: source hash mismatch")
    if MAIN_INDEX.exists():
        main_rows = [json.loads(line) for line in MAIN_INDEX.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(main_rows) != 21 or any((r.get("answer_text") or "") for r in main_rows): errors.append("main answer index gate changed")
    result = {"schema_version": "reference-answer-candidate-validation-2014-0.1", "result": "passed" if not errors else "failed", "rows": len(rows), "main_index_present": MAIN_INDEX.exists(), "errors": errors, "checks": {"partial_coverage": ids == list(EXPECTED), "source_hashes": not any("hash" in e for e in errors), "authority_gate": not any("gate" in e for e in errors), "main_index_unchanged_gate": "main answer index gate changed" not in errors}}
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
