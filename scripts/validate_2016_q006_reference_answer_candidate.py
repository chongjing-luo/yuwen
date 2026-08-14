#!/usr/bin/env python3
"""Validate the isolated 2016 NC3 Q006 candidate layer."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers"
OUT = BASE / "reference_answer_candidates_q006_gzywtk.jsonl"
MAIN = BASE / "answer_index.jsonl"
HTML = ROOT / "Data/reference/gaokao/html/2016/answer_gzywtk_1881-4.html"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2016_q006_20260809.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(value: str) -> str:
    return re.sub(r"\s+", "", value)


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip()] if OUT.exists() else []
    if len(rows) != 1 or rows[0].get("question_id") != 6:
        errors.append("expected exactly one Q006 candidate row")
    html_sha = sha_bytes(HTML.read_bytes()) if HTML.exists() else None
    for row in rows:
        cid = row.get("candidate_id", "?")
        text = row.get("answer_candidate_text") or ""
        excerpt = row.get("source_group_excerpt") or ""
        if row.get("exam_id") != "GK-NC3-2016" or row.get("question_id") != 6:
            errors.append(f"{cid}: exam/question mismatch")
        for field, expected in {
            "candidate_status": "candidate_unverified",
            "source_authority_status": "unverified_third_party_reprint",
            "source_status": "unverified_third_party_reprint",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
        }.items():
            if row.get(field) != expected:
                errors.append(f"{cid}: {field} escaped safe value")
        if row.get("answer_candidate_sha256") != sha_bytes(text.encode("utf-8")):
            errors.append(f"{cid}: answer hash mismatch")
        if row.get("source_group_excerpt_sha256") != sha_bytes(excerpt.encode("utf-8")):
            errors.append(f"{cid}: excerpt hash mismatch")
        if compact(text) not in compact(excerpt):
            errors.append(f"{cid}: candidate not contained in excerpt")
        if row.get("source_html_sha256") != html_sha:
            errors.append(f"{cid}: HTML hash mismatch")
        for term in ("答B给3分", "坚持独立思考", "天下兴亡", "匹夫有责"):
            if term not in text:
                errors.append(f"{cid}: Q006 content guard missing {term}")
        forbidden = {row.get("candidate_status"), row.get("source_authority_status"), row.get("source_status"), row.get("answer_source_status"), row.get("scoring_status"), row.get("mapping_level"), row.get("kp_id")}
        if any(label in forbidden for label in ("official_verified", "M1", "M2", "M3")):
            errors.append(f"{cid}: forbidden authority/mapping value")

    main_rows = [json.loads(line) for line in MAIN.read_text(encoding="utf-8").splitlines() if line.strip()] if MAIN.exists() else []
    q6 = next((r for r in main_rows if r.get("question_id") == 6), None)
    if not q6 or q6.get("answer_status") != "N/A" or (q6.get("answer_text") or ""):
        errors.append("main Q006 answer index gate changed")
    result = {
        "schema_version": "reference-answer-candidate-validation-2016-q006-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "main_q006_status": q6.get("answer_status") if q6 else None,
        "errors": errors,
        "checks": {
            "single_question_coverage": len(rows) == 1 and rows[0].get("question_id") == 6 if rows else False,
            "source_hashes": not any("hash mismatch" in e for e in errors),
            "authority_gate": not any("authority" in e or "forbidden" in e for e in errors),
            "main_index_unchanged_gate": not any("main Q006" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
