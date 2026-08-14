#!/usr/bin/env python3
"""Validate the isolated Meipian 2024 candidate layer."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers"
OUT = BASE / "reference_answer_candidates_meipian.jsonl"
MAIN_INDEX = BASE / "answer_index.jsonl"
HTML = ROOT / "Data/reference/gaokao/html/2024/answer_meipian_552rdrkt.html"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2024_meipian_20260809.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip()] if OUT.exists() else []
    ids = sorted(int(r.get("question_id", -1)) for r in rows)
    if ids != list(range(1, 23)):
        errors.append(f"coverage={ids}, expected 1..22")
    if len({r.get("candidate_id") for r in rows}) != len(rows):
        errors.append("duplicate candidate_id")
    html_sha = sha_bytes(HTML.read_bytes()) if HTML.exists() else None
    for row in rows:
        cid = row.get("candidate_id", "?")
        qid = int(row.get("question_id", -1))
        text = row.get("answer_candidate_text") or ""
        excerpt = row.get("source_group_excerpt") or ""
        if row.get("source_authority_status") != "unverified_third_party_reprint":
            errors.append(f"{cid}: authority escaped unverified boundary")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{cid}: scoring status changed")
        if row.get("mapping_level") != "M0" or row.get("kp_id") != "N/A":
            errors.append(f"{cid}: mapping status changed")
        if row.get("answer_candidate_sha256") != sha_bytes(text.encode("utf-8")):
            errors.append(f"{cid}: answer hash mismatch")
        if row.get("source_group_excerpt_sha256") != sha_bytes(excerpt.encode("utf-8")):
            errors.append(f"{cid}: source excerpt hash mismatch")
        if compact(text) not in compact(excerpt):
            errors.append(f"{cid}: candidate text not contained in source excerpt")
        if row.get("source_html_sha256") != html_sha:
            errors.append(f"{cid}: HTML hash mismatch")
        if row.get("candidate_content_type") != ("writing_guidance_candidate" if qid == 22 else "reference_answer_candidate"):
            errors.append(f"{cid}: content type mismatch")
        forbidden = {row.get("candidate_status"), row.get("source_authority_status"), row.get("source_status"), row.get("answer_source_status"), row.get("scoring_status"), row.get("mapping_level"), row.get("kp_id")}
        if any(label in forbidden for label in ("official_verified", "M1", "M2", "M3")):
            errors.append(f"{cid}: forbidden official/mapping label")
        if row.get("source_url") != "https://www.meipian.cn/552rdrkt":
            errors.append(f"{cid}: source URL mismatch")

    main_rows = [json.loads(line) for line in MAIN_INDEX.read_text(encoding="utf-8").splitlines() if line.strip()] if MAIN_INDEX.exists() else []
    main_missing = [r for r in main_rows if r.get("question_id") in range(1, 23) and not (r.get("answer_text") or "") and r.get("answer_status") in {"missing", "N/A"}]
    if len(main_missing) != 22:
        errors.append(f"main answer index missing gate changed: {len(main_missing)}")
    result = {
        "schema_version": "reference-answer-candidate-validation-2024-meipian-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "main_index_missing_rows": len(main_missing),
        "errors": errors,
        "checks": {
            "full_coverage": ids == list(range(1, 23)),
            "source_hashes": not any("hash mismatch" in e for e in errors),
            "authority_gate": not any("authority" in e or "official" in e for e in errors),
            "main_index_unchanged_gate": not any("main answer index" in e for e in errors),
            "q22_guidance_label": all(r.get("candidate_content_type") == "writing_guidance_candidate" for r in rows if r.get("question_id") == 22),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
