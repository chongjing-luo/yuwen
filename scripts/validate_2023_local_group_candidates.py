#!/usr/bin/env python3
"""Validate the explicit-group split of 2023 local analysis candidates."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers"
INPUT = BASE / "local_analysis_candidates.jsonl"
OUT = BASE / "local_analysis_group_candidates.jsonl"
REPORT = ROOT / "work/knowledge/_meta/local_group_candidate_validation_2023_20260809.json"
GROUPS = {1: 3, 2: 3, 3: 3, 4: 6, 5: 6, 6: 6, 7: 9, 8: 9, 9: 9, 14: 15, 15: 15, 17: 21, 18: 21, 19: 21, 20: 21, 21: 21}


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []
    rows = load(OUT) if OUT.exists() else []
    source = {int(r["question_id"]): r for r in load(INPUT)} if INPUT.exists() else {}
    ids = [r.get("question_id") for r in rows]
    if ids != list(range(1, 23)):
        errors.append(f"coverage/order={ids}")
    if len({r.get("candidate_id") for r in rows}) != len(rows):
        errors.append("duplicate candidate_id")
    for row in rows:
        qid = int(row.get("question_id", -1))
        cid = row.get("candidate_id", "?")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{cid}: scoring gate escaped")
        if (row.get("mapping_level"), row.get("kp_id")) != ("M0", "N/A"):
            errors.append(f"{cid}: M0 gate escaped")
        if row.get("source_authority_status") != "unverified_local_provided":
            errors.append(f"{cid}: authority gate escaped")
        text = row.get("candidate_text") or ""
        if row.get("candidate_text_sha256") != (sha(text) if text else None):
            errors.append(f"{cid}: candidate hash mismatch")
        source_qid = row.get("source_group_question_id")
        if qid in GROUPS:
            if source_qid != GROUPS[qid]:
                errors.append(f"{cid}: source group mismatch")
            src = source.get(source_qid) or {}
            if row.get("source_group_candidate_id") != src.get("candidate_id"):
                errors.append(f"{cid}: source group candidate link mismatch")
            if row.get("source_group_candidate_text_sha256") != src.get("candidate_text_sha256"):
                errors.append(f"{cid}: source group text hash mismatch")
            if not text:
                errors.append(f"{cid}: explicit group split has empty candidate")
        elif qid in {10, 11, 12, 13, 16}:
            if row.get("candidate_status") != "candidate_mixed_analysis" or text:
                errors.append(f"{cid}: unresolved mixed-analysis boundary changed")
        elif qid == 22:
            if row.get("candidate_status") != "candidate_writing_artifact":
                errors.append(f"{cid}: writing artifact boundary changed")
        else:
            errors.append(f"{cid}: unexpected question classification")
        segment = ROOT / str(row.get("source_analysis_segment", ""))
        if not segment.exists():
            errors.append(f"{cid}: source segment missing")
    result = {
        "schema_version": "local-group-candidate-validation-2023-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "errors": errors,
        "checks": {
            "coverage": ids == list(range(1, 23)),
            "group_boundaries": not any("group" in e for e in errors),
            "hashes": not any("hash" in e for e in errors),
            "authority_and_scoring_gate": not any("gate escaped" in e for e in errors),
            "source_traceability": not any("source segment" in e or "candidate link" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
