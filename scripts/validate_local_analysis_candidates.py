#!/usr/bin/env python3
"""Validate local-analysis-only candidate derivatives without opening answer gates."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract"
REPORT = ROOT / "work/knowledge/_meta/local_analysis_candidate_validation_20260809.json"
EXAM_ID = "GK-SC-2013"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def segment_hash(path: Path) -> str | None:
    text = path.read_text(encoding="utf-8")
    match = re.search(r'(?m)^segment_clean_sha256:\s*"([0-9a-f]{64})"$', text)
    return match.group(1) if match else None


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    path = EXTRACT / EXAM_ID / "answers/local_analysis_candidates.jsonl"
    errors: list[str] = []
    warnings: list[str] = []
    rows = load(path) if path.exists() else []
    expected = list(range(1, 22))
    got = sorted(int(row.get("question_id", -1)) for row in rows)
    if got != expected:
        errors.append(f"question_ids={got}, expected=1..21")
    ids = [row.get("candidate_id") for row in rows]
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate_id")
    for row in rows:
        cid = row.get("candidate_id", "?")
        if row.get("source_authority_status") != "unverified_local_provided":
            errors.append(f"{cid}: source authority escaped local-unverified boundary")
        if row.get("answer_source_status") != "missing_separate_answer_bundle":
            errors.append(f"{cid}: answer source status changed")
        if row.get("scoring_status") != "not_available_as_official":
            errors.append(f"{cid}: scoring status escaped conservative boundary")
        if row.get("mapping_level") != "M0" or row.get("kp_id") != "N/A":
            errors.append(f"{cid}: non-M0 mapping")
        source = ROOT / str(row.get("source_analysis_segment", ""))
        if not source.exists():
            errors.append(f"{cid}: source analysis segment missing")
            continue
        for field in ("source_analysis_pdf", "source_analysis_mineru_md", "source_clean_md"):
            target = row.get(field)
            if target and not (ROOT / str(target)).exists():
                errors.append(f"{cid}: missing provenance file {field}")
        if row.get("source_segment_file_sha256") != digest(source.read_text(encoding="utf-8")):
            errors.append(f"{cid}: source segment file hash mismatch")
        front_hash = segment_hash(source)
        if not front_hash or row.get("source_segment_clean_sha256") != front_hash:
            errors.append(f"{cid}: source segment clean hash mismatch")
        candidate = row.get("candidate_text") or ""
        if row.get("candidate_text_sha256") != (digest(candidate) if candidate else None):
            errors.append(f"{cid}: candidate text hash mismatch")
        analysis = row.get("analysis_excerpt") or ""
        if row.get("analysis_excerpt_sha256") != (digest(analysis) if analysis else None):
            errors.append(f"{cid}: analysis excerpt hash mismatch")
        if row.get("candidate_status") == "candidate_mixed_analysis" and not analysis:
            errors.append(f"{cid}: mixed candidate lacks preserved analysis excerpt")
        if row.get("manual_boundary", {}).get("status") == "split_on_explicit_source_marker":
            question = row.get("question_excerpt") or ""
            if not question:
                errors.append(f"{cid}: manual split lacks question excerpt")
            if row.get("question_excerpt_sha256") != digest(question):
                errors.append(f"{cid}: question excerpt hash mismatch")
            marker = row.get("manual_boundary", {}).get("marker") or ""
            if marker and not analysis.startswith(marker):
                errors.append(f"{cid}: analysis excerpt does not start at recorded marker")
            original_hash = row.get("manual_boundary", {}).get("original_mixed_excerpt_sha256")
            if not original_hash:
                errors.append(f"{cid}: manual split lacks original excerpt hash")
        if row.get("candidate_status") == "missing":
            warnings.append(f"{cid}: no extractable candidate text")
        if (row.get("candidate_kind") == "analysis_excerpt_without_explicit_answer_marker"
                and row.get("manual_boundary", {}).get("status") != "split_on_explicit_source_marker"):
            warnings.append(f"{cid}: candidate may mix question and analysis")
        if any(label in json.dumps(row, ensure_ascii=False) for label in ("official_verified", "M1", "M2", "M3")):
            errors.append(f"{cid}: forbidden official/mapping label in candidate row")
    result = {
        "schema_version": "exam-local-analysis-candidate-validation-0.1",
        "exam_id": EXAM_ID,
        "result": "passed" if not errors else "failed",
        "rows": len(rows),
        "errors": errors,
        "warnings": warnings,
        "checks": {
            "question_coverage": got == expected,
            "unique_ids": len(ids) == len(set(ids)),
            "source_traceability": not any("source" in e for e in errors),
            "hashes": not any("hash mismatch" in e for e in errors),
            "authority_gate": not any("authority" in e or "official" in e for e in errors),
            "m0_boundary": not any("non-M0" in e or "mapping" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
