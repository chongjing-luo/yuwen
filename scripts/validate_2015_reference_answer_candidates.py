#!/usr/bin/env python3
"""Validate the isolated 2015 third-party answer-candidate layer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/answers"
SOURCE_DIR = ROOT / "Data/reference/gaokao/external/2015_gaokao_answer"
OUT = BASE / "reference_answer_candidates.jsonl"
MAIN_INDEX = BASE / "answer_index.jsonl"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2015_20260809.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def main() -> int:
    errors: list[str] = []
    rows = [json.loads(line) for line in OUT.read_text(encoding="utf-8").splitlines() if line.strip()] if OUT.exists() else []
    ids = sorted(int(r.get("question_id", -1)) for r in rows)
    if ids != list(range(1, 22)):
        errors.append(f"coverage={ids}, expected 1..21")
    if len({r.get("candidate_id") for r in rows}) != len(rows):
        errors.append("duplicate candidate_id")
    expected_short = {1: "D", 2: "A", 3: "A", 4: "B", 5: "C", 6: "B", 7: "C", 8: "B", 9: "B", 15: "AD"}
    required = [SOURCE_DIR / "answer_source.txt", SOURCE_DIR / "source.html", SOURCE_DIR / "answer_bundle.zip"]
    required += list(SOURCE_DIR.glob("*.doc"))
    hashes = {p.name: sha(p) for p in required if p.exists()}
    for row in rows:
        cid = row.get("candidate_id", "?")
        text = row.get("answer_candidate_text") or ""
        excerpt = row.get("source_group_excerpt") or ""
        for key, expected in {
            "source_authority_status": "unverified_third_party_reprint",
            "source_status": "unverified_third_party_reprint",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
        }.items():
            if row.get(key) != expected:
                errors.append(f"{cid}: {key} escaped conservative boundary")
        if row.get("candidate_status") != "candidate_unverified":
            errors.append(f"{cid}: candidate status changed")
        qid = int(row.get("question_id", -1))
        if qid in expected_short and text != expected_short[qid]:
            errors.append(f"{cid}: compact answer {text!r} != registered source transcription {expected_short[qid]!r}")
        if row.get("answer_candidate_sha256") != sha_text(text):
            errors.append(f"{cid}: answer hash mismatch")
        if row.get("source_group_excerpt_sha256") != sha_text(excerpt):
            errors.append(f"{cid}: excerpt hash mismatch")
        for key, path in (("source_text", SOURCE_DIR / "answer_source.txt"),
                          ("source_html", SOURCE_DIR / "source.html"),
                          ("source_zip", SOURCE_DIR / "answer_bundle.zip")):
            if not path.exists() or row.get(f"{key}_sha256") != sha(path):
                errors.append(f"{cid}: {key} path/hash mismatch")
        doc = next(SOURCE_DIR.glob("*.doc"), None)
        if not doc or row.get("source_doc_sha256") != sha(doc):
            errors.append(f"{cid}: source_doc path/hash mismatch")
        if row.get("source_line_start", 0) > row.get("source_line_end", 0):
            errors.append(f"{cid}: invalid source line interval")
        forbidden = {"official_verified", "M1", "M2", "M3"}
        scalar_values = {value for value in row.values() if isinstance(value, str)}
        if forbidden.intersection(scalar_values):
            errors.append(f"{cid}: forbidden official/mapping label")

    # Main answer index is intentionally absent for this year.  If a future
    # run creates it, every row must still remain explicitly missing here.
    if MAIN_INDEX.exists():
        main_rows = [json.loads(line) for line in MAIN_INDEX.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(main_rows) != 21 or any((r.get("answer_text") or "") for r in main_rows):
            errors.append("main answer index gate changed")
    result = {
        "schema_version": "reference-answer-candidate-validation-2015-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "source_hashes": hashes,
        "main_index_present": MAIN_INDEX.exists(),
        "errors": errors,
        "checks": {
            "full_candidate_coverage": ids == list(range(1, 22)),
            "source_hashes": not any("hash" in e or "path" in e for e in errors),
            "authority_gate": not any("boundary" in e or "official" in e for e in errors),
            "main_index_unchanged_gate": "main answer index gate changed" not in errors,
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
