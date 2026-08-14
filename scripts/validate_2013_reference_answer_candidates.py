#!/usr/bin/env python3
"""Validate the 2013 third-party answer-image candidate layer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers"
OUT = BASE / "reference_answer_candidates.jsonl"
MAIN_INDEX = BASE / "answer_index.jsonl"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2013_20260809.json"


def sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip()] if OUT.exists() else []
    ids = sorted(int(r.get("question_id", -1)) for r in rows)
    if ids != list(range(1, 21)):
        errors.append(f"coverage={ids}, expected 1..20")
    if len({r.get("candidate_id") for r in rows}) != len(rows):
        errors.append("duplicate candidate_id")
    source_hashes: dict[str, str] = {}
    for row in rows:
        cid = row.get("candidate_id", "?")
        text = row.get("answer_candidate_text") or ""
        image = ROOT / str(row.get("source_image", ""))
        gallery = ROOT / str(row.get("source_gallery_html", ""))
        if row.get("source_authority_status") != "unverified_third_party_reprint":
            errors.append(f"{cid}: authority escaped unverified boundary")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{cid}: scoring status changed")
        if row.get("mapping_level") != "M0" or row.get("kp_id") != "N/A":
            errors.append(f"{cid}: mapping status changed")
        if row.get("answer_candidate_sha256") != sha_bytes(text.encode("utf-8")):
            errors.append(f"{cid}: answer hash mismatch")
        if not image.exists() or row.get("source_image_sha256") != sha_bytes(image.read_bytes()):
            errors.append(f"{cid}: source image hash/path mismatch")
        if not gallery.exists() or row.get("source_gallery_html_sha256") != sha_bytes(gallery.read_bytes()):
            errors.append(f"{cid}: gallery html hash/path mismatch")
        source_hashes[str(image)] = row.get("source_image_sha256")
    main_rows = [json.loads(line) for line in MAIN_INDEX.read_text(encoding="utf-8").splitlines() if line.strip()] if MAIN_INDEX.exists() else []
    main_missing = [r for r in main_rows if r.get("question_id") in range(1, 22) and not (r.get("answer_text") or "") and r.get("answer_status") in {"missing", "N/A"}]
    if len(main_missing) != 21:
        errors.append(f"main answer index missing gate changed: {len(main_missing)}")
    result = {
        "schema_version": "reference-answer-candidate-validation-2013-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "main_index_missing_rows": len(main_missing),
        "errors": errors,
        "checks": {
            "partial_coverage": ids == list(range(1, 21)),
            "source_hashes": not any("hash" in e for e in errors),
            "authority_gate": not any("authority" in e or "official" in e for e in errors),
            "main_index_unchanged_gate": not any("main answer index" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
