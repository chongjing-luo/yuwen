#!/usr/bin/env python3
"""Build the auditable SG-EXAM-CAL candidate manifest.

The manifest freezes counts and structural provenance only.  It deliberately
does not promote local PDFs or third-party analyses to official sources and it
does not create M1/M2 mappings.
"""
from __future__ import annotations

import hashlib, json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "Data/2008-2024·（四川）语文高考真题"
OUT = ROOT / "work/knowledge/_meta"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf8"))
    expectations = json.loads((ROOT / "work/knowledge/exams/_meta/exam_expectations_2008_2024.json").read_text(encoding="utf8"))
    rows = []
    for year in range(2008, 2025):
        recs = [r for r in manifest["records"] if int(r["year"]) == year]
        if not recs:
            raise SystemExit(f"missing manifest records for {year}")
        paper_code = recs[0]["paper_code"]
        exam_id = f"GK-{paper_code}-{year}"
        validation = CORPUS / "exam_extract" / exam_id / "review" / f"validation-{year}.json"
        if not validation.exists() and year == 2008:
            validation = CORPUS / "exam_extract" / exam_id / "review/validation.json"
        report = json.loads(validation.read_text(encoding="utf8")) if validation.exists() else {"result": "missing"}
        role_data = {}
        for role in ("question", "analysis"):
            r = next((x for x in recs if x["document_role"] == role), None)
            if not r:
                raise SystemExit(f"{year}: missing {role} record")
            role_data[role] = {
                "artifact_id": r["artifact_id"],
                "local_pdf": r["local_pdf"],
                "mineru_full_md": r["mineru_full_md"],
                "pdf_page_count": r["pdf_page_count"],
                "pdf_sha256": r["sha256"],
                "source_level": r["source_level"],
                "authenticity_status": r["authenticity_status"],
            }
        expected_count = int(expectations["top_level_question_count_by_year"][str(year)])
        warnings = report.get("warnings", [])
        rows.append({
            "exam_id": exam_id,
            "year": year,
            "paper_code": paper_code,
            "sichuan_relation": recs[0]["sichuan_relation"],
            "top_level_question_count": expected_count,
            "expected_question_ids": list(range(1, expected_count + 1)),
            "document_roles": role_data,
            "derived_output_root": f"Data/2008-2024·（四川）语文高考真题/exam_extract/{exam_id}",
            "validation_report": str(validation.relative_to(ROOT)) if validation.exists() else None,
            "structural_validation": report.get("result", "missing"),
            "review_warnings": warnings,
            "answer_status": "candidate_unverified_local_analysis_only",
            "scoring_status": "missing_official_scoring_artifact",
        })
    data = {
        "schema_version": "exam-calibration-manifest-0.1",
        "calibration_id": "SG-EXAM-CAL-2008-2024",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "scope": "2008-2024 四川适用语文高考配对卷",
        "source_boundary": "unverified_local_provided",
        "freeze_status": "candidate_structural_freeze",
        "paper_count": 34,
        "exam_count": 17,
        "role_policy": {"question": "canonical_question_text_candidate", "analysis": "answer_analysis_candidate", "answer_scoring_candidate": "not_available_as_official"},
        "small_question_policy": "top_level IDs are frozen first; subquestion/response nodes are separately derived and must not be inferred from top-level count",
        "locator_policy": "page_level_fallback until manual PDF bbox adjudication",
        "m_mapping_policy": "M0 unless stable small-question ID and bidirectional evidence are verified",
        "known_missing_source_markers": expectations["known_missing_source_markers"],
        "vertical_calibration_slices": ["GK-SC-2008", "GK-SC-2013", "GK-NC3-2016", "GK-NCA-2024"],
        "supplemental_structural_slices": ["GK-SC-2009", "GK-SC-2010", "GK-SC-2011", "GK-SC-2012", "GK-SC-2014", "GK-SC-2015"],
        "blocking_conditions": ["official/source authenticity verification incomplete", "official answer/scoring artifacts unavailable", "manual PDF/OCR adjudication incomplete"],
        "records": rows,
    }
    target = OUT / "exam_calibration_manifest.json"
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf8")
    print(json.dumps({"path": str(target.relative_to(ROOT)), "exam_count": len(rows), "paper_count": 34, "status": data["freeze_status"]}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
