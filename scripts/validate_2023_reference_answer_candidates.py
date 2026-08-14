#!/usr/bin/env python3
"""Validate the partial 2023 third-party answer candidate layer."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers"
OUT = BASE / "reference_answer_candidates.jsonl"
MAIN = BASE / "answer_index.jsonl"
REPORT = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2023_20260809.json"
EXPECTED = [1, 2, 3, 6, 7, 8, 9, 10]
PDF = ROOT / "Data/reference/gaokao/pdf/2023/2023_NCA_answer.pdf"
HTML = ROOT / "Data/reference/gaokao/html/2023/answer.html"
FULL = ROOT / "Data/reference/gaokao/mineru_result/2023_NCA_answer/full.md"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []
    rows = load(OUT) if OUT.exists() else []
    ids = [r.get("question_id") for r in rows]
    if ids != EXPECTED:
        errors.append(f"coverage/order={ids}, expected={EXPECTED}")
    if len({r.get("candidate_id") for r in rows}) != len(rows):
        errors.append("duplicate candidate_id")
    for row in rows:
        cid = row.get("candidate_id", "?")
        text = row.get("answer_candidate_text") or ""
        if row.get("source_authority_status") != "unverified_third_party_reprint":
            errors.append(f"{cid}: authority escaped unverified boundary")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{cid}: scoring status escaped")
        if (row.get("mapping_level"), row.get("kp_id")) != ("M0", "N/A"):
            errors.append(f"{cid}: mapping gate escaped")
        if row.get("answer_candidate_sha256") != sha_bytes(text.encode("utf-8")):
            errors.append(f"{cid}: candidate hash mismatch")
        for field, expected in (("source_pdf", PDF), ("source_html", HTML), ("source_mineru_md", FULL)):
            path = ROOT / str(row.get(field, ""))
            hash_field = {"source_pdf": "source_pdf_sha256", "source_html": "source_html_sha256", "source_mineru_md": "source_mineru_md_sha256"}[field]
            if path != expected:
                errors.append(f"{cid}: {field} path mismatch")
            elif not path.exists() or row.get(hash_field) != sha_bytes(path.read_bytes()):
                errors.append(f"{cid}: {field} hash mismatch")
        if not row.get("source_group_excerpt"):
            errors.append(f"{cid}: missing source group excerpt")
    if MAIN.exists():
        main_rows = load(MAIN)
        # The 2023 exam did not previously have an answer index; if one is
        # introduced later, this validator must not silently accept answers.
        if main_rows:
            nonempty = [r for r in main_rows if (r.get("answer_text") or "")]
            if nonempty:
                errors.append("main answer index contains nonempty text unexpectedly")
    result = {
        "schema_version": "reference-answer-candidate-validation-2023-0.1",
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "expected_candidate_questions": EXPECTED,
        "missing_questions": [qid for qid in range(1, 23) if qid not in EXPECTED],
        "errors": errors,
        "checks": {
            "partial_coverage": ids == EXPECTED,
            "source_hashes": not any("hash" in e for e in errors),
            "authority_gate": not any("authority" in e or "scoring" in e or "mapping" in e for e in errors),
            "no_unexpected_main_answer": not any("main answer index" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
