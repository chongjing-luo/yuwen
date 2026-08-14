#!/usr/bin/env python3
"""Validate answer-clean candidate derivatives without opening answer gates."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract"
REPORT = ROOT / "work/knowledge/_meta/answer_clean_candidate_validation_20260809.json"


def sha(text: str | None) -> str | None:
    if not text:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    exam_reports: list[dict] = []
    for base in sorted(EXTRACT.iterdir()):
        index = base / "answers/answer_index.jsonl"
        output = base / "answers/answer_clean_candidates.jsonl"
        if not index.exists():
            continue
        source_rows = rows(index)
        clean_rows = rows(output) if output.exists() else []
        eid = base.name
        if len(source_rows) != len(clean_rows):
            errors.append(f"{eid}: clean rows={len(clean_rows)} source rows={len(source_rows)}")
        source_by_q = {int(r["question_id"]): r for r in source_rows}
        clean_by_q = {int(r["question_id"]): r for r in clean_rows if str(r.get("question_id", "")).isdigit()}
        if set(source_by_q) != set(clean_by_q):
            errors.append(f"{eid}: question coverage mismatch")
        for qid, source in source_by_q.items():
            row = clean_by_q.get(qid)
            if not row:
                continue
            cid = f"{eid}-Q{qid:03d}"
            raw = source.get("answer_text") or ""
            if row.get("source_answer_text_sha256") != sha(raw):
                errors.append(f"{cid}: raw source hash mismatch")
            if row.get("question_excerpt_sha256") != sha(row.get("question_excerpt")):
                errors.append(f"{cid}: question hash mismatch")
            if row.get("analysis_excerpt_sha256") != sha(row.get("analysis_excerpt")):
                errors.append(f"{cid}: analysis hash mismatch")
            if row.get("answer_candidate_sha256") != sha(row.get("answer_candidate_text")):
                errors.append(f"{cid}: answer candidate hash mismatch")
            if row.get("answer_candidate_prefix_removed_sha256") != sha(row.get("answer_candidate_prefix_removed")):
                errors.append(f"{cid}: removed prefix hash mismatch")
            prefix = row.get("answer_candidate_prefix_removed") or ""
            candidate = row.get("answer_candidate_text") or ""
            if prefix:
                if not raw.strip().startswith(prefix.strip()):
                    errors.append(f"{cid}: removed prefix is not a source prefix")
                if candidate and raw.strip()[len(prefix):].strip() != candidate:
                    errors.append(f"{cid}: marker-free candidate does not reconstruct source remainder")
            if row.get("solution_excerpt_sha256") != sha(row.get("solution_excerpt")):
                errors.append(f"{cid}: solution excerpt hash mismatch")
            if row.get("answer_key_excerpt_sha256") != sha(row.get("answer_key_excerpt")):
                errors.append(f"{cid}: answer key excerpt hash mismatch")
            if row.get("compound_source_status") == "explicit_compound_question_blocks":
                boundaries = row.get("compound_source_boundaries") or []
                if len(boundaries) != 1 or len(boundaries[0].get("sections", [])) != 2:
                    errors.append(f"{cid}: compound source boundary metadata incomplete")
                else:
                    if boundaries[0]["sections"][0].get("source_question_id") != qid:
                        errors.append(f"{cid}: compound first section question id mismatch")
                    for section in boundaries[0]["sections"]:
                        start = int(section.get("source_offset_start", -1))
                        end = int(section.get("source_offset_end", -1))
                        if start < 0 or end < start or end > len(raw):
                            errors.append(f"{cid}: compound source offsets invalid")
                        elif section.get("source_excerpt_sha256") != sha(raw[start:end]):
                            errors.append(f"{cid}: compound source excerpt hash mismatch")
                if row.get("compound_alignment_status") == "resolved_derived_boundary":
                    review = row.get("compound_alignment_review") or {}
                    if review.get("review_status") != "resolved_in_derived_layer":
                        errors.append(f"{cid}: resolved compound alignment missing review status")
                    if not review.get("evidence"):
                        errors.append(f"{cid}: resolved compound alignment missing evidence")
            if row.get("compound_alignment_status") == "linked_child_section":
                interval = row.get("compound_source_interval") or {}
                if row.get("candidate_status") != "missing":
                    errors.append(f"{cid}: linked child compound section unexpectedly has answer candidate")
                if not row.get("compound_parent_answer_pair_id") or not interval.get("source_excerpt_sha256"):
                    errors.append(f"{cid}: linked child compound metadata incomplete")
            manual_boundary = row.get("manual_boundary") or {}
            if manual_boundary.get("status") == "resolved_in_derived_layer":
                marker = str(manual_boundary.get("marker") or "")
                start = int(manual_boundary.get("source_offset_start", -1))
                end = int(manual_boundary.get("source_offset_end", -1))
                if not marker or raw[start:end].strip() != marker.strip():
                    errors.append(f"{cid}: derived answer boundary marker/offset mismatch")
                if manual_boundary.get("source_answer_text_sha256") != sha(raw):
                    errors.append(f"{cid}: derived answer boundary source hash mismatch")
                if manual_boundary.get("source_prefix_sha256") != sha(raw[:start]):
                    errors.append(f"{cid}: derived answer boundary prefix hash mismatch")
                for field in ("source_question_segment", "source_analysis_segment"):
                    target = manual_boundary.get(field)
                    if not target or not (ROOT / str(target)).exists():
                        errors.append(f"{cid}: derived answer boundary provenance missing: {field}")
                if row.get("cleaning_status") != "derived_answer_boundary_without_analysis":
                    errors.append(f"{cid}: derived answer boundary cleaning status mismatch")
                if row.get("marker_separation_status") != "derived_answer_boundary_with_nested_answer_key":
                    errors.append(f"{cid}: derived answer boundary separation status mismatch")
            if row.get("scoring_status") != "not_available_as_official":
                errors.append(f"{cid}: scoring gate changed")
            if row.get("mapping_level") != "M0" or row.get("kp_id") != "N/A":
                errors.append(f"{cid}: mapping gate changed")
            external = row.get("external_reference_candidate")
            if external and not (ROOT / str(external)).exists():
                errors.append(f"{cid}: external reference candidate path missing")
            if external and row.get("external_reference_status") not in {
                "available_unverified_partial", "available_unverified_full_candidate",
                "available_unverified_single_candidate"
            }:
                errors.append(f"{cid}: external reference status invalid")
            local_reference = row.get("local_reference_candidate")
            if local_reference and not (ROOT / str(local_reference)).exists():
                errors.append(f"{cid}: local reference candidate path missing")
            if local_reference and row.get("local_reference_status") != "available_unverified_local_analysis_candidate":
                errors.append(f"{cid}: local reference status invalid")
            marker_inventory = row.get("marker_inventory") or []
            if row.get("cleaning_status", "").startswith("explicit_analysis"):
                if not row.get("question_excerpt") or not row.get("analysis_excerpt"):
                    errors.append(f"{cid}: explicit split missing excerpt")
                if not any(m.get("kind") == "analysis" for m in marker_inventory):
                    errors.append(f"{cid}: explicit split missing analysis marker")
            if row.get("cleaning_status") == "missing" and raw:
                errors.append(f"{cid}: nonempty raw marked missing")
            if row.get("marker_separation_status") in {"nested_analysis_unresolved", "nested_answer_unresolved"}:
                warnings.append(f"{cid}: nested marker requires manual review")
            if row.get("cleaning_status") in {"unbounded_answer_field", "answer_marker_without_analysis_boundary"}:
                warnings.append(f"{cid}: no safe question/analysis boundary")
        exam_reports.append({"exam_id": eid, "source_rows": len(source_rows), "clean_rows": len(clean_rows)})
    result = {
        "schema_version": "answer-clean-candidate-validation-0.1",
        "result": "passed" if not errors else "failed",
        "errors": errors,
        "warnings": warnings,
        "exams": exam_reports,
        "checks": {
            "source_coverage": not any("coverage" in e or "clean rows" in e for e in errors),
            "hashes": not any("hash mismatch" in e for e in errors),
            "authority_gate": not any("gate" in e for e in errors),
        },
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
