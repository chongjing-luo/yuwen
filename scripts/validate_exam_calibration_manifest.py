#!/usr/bin/env python3
"""Validate the SG-EXAM-CAL candidate manifest against current files."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "Data/2008-2024·（四川）语文高考真题"
MANIFEST = ROOT / "work/knowledge/_meta/exam_calibration_manifest.json"

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
    return h.hexdigest()

def main() -> int:
    d=json.loads(MANIFEST.read_text(encoding="utf8"))
    errors=[]; warnings=[]
    if d.get("paper_count") != 34: errors.append("paper_count must be 34")
    if d.get("exam_count") != 17: errors.append("exam_count must be 17")
    if len(d.get("records",[])) != 17: errors.append("records must contain 17 exams")
    seen=[]
    for rec in d.get("records",[]):
        eid=rec.get("exam_id"); seen.append(eid)
        if rec.get("structural_validation") != "passed": errors.append(f"{eid}: structural validation not passed")
        expected=rec.get("expected_question_ids",[])
        if len(expected) != rec.get("top_level_question_count"): errors.append(f"{eid}: expected ID denominator mismatch")
        for role, r in rec.get("document_roles",{}).items():
            pdf=ROOT / r["local_pdf"]; md=ROOT / r["mineru_full_md"]
            if not pdf.exists(): errors.append(f"{eid}/{role}: missing PDF")
            if not md.exists(): errors.append(f"{eid}/{role}: missing full.md")
            if pdf.exists() and sha256(pdf) != r.get("pdf_sha256"): errors.append(f"{eid}/{role}: PDF hash mismatch")
        if rec.get("review_warnings"): warnings.extend([f"{eid}: {x}" for x in rec["review_warnings"]])
    if len(set(seen)) != 17: errors.append("exam IDs are not unique")
    report={"schema_version":"exam-calibration-validation-0.1","calibration_id":d.get("calibration_id"),"result":"passed" if not errors else "failed","errors":errors,"warnings":warnings,"checks":{"pair_count":not any("count" in x or "records" in x for x in errors),"raw_hashes":not any("hash" in x for x in errors),"structural_validation":not any("structural" in x for x in errors),"denominators":not any("denominator" in x for x in errors)}}
    out=ROOT/"work/knowledge/_meta/validation_reports/exam_calibration_validation.json"
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if not errors else 1

if __name__ == "__main__": raise SystemExit(main())
