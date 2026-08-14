#!/usr/bin/env python3
"""Validate the conservative top-level EKP draft records."""
from __future__ import annotations
import hashlib, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NODE_FILE=ROOT/"work/knowledge/高考分析/exam_response_nodes_top_level.jsonl"

def main()->int:
    nodes=[json.loads(x) for x in NODE_FILE.read_text(encoding="utf8").splitlines() if x.strip()]
    errors=[]; warnings=[]
    expected={**{y:21 for y in range(2008,2016)},**{y:12 for y in range(2016,2018)},**{y:10 for y in range(2018,2021)},**{y:22 for y in range(2021,2025)}}
    by_exam={}
    for n in nodes:
        by_exam.setdefault(n["exam_id"],[]).append(n)
        for field in ("response_node_id","exam_id","question_id","source_question_segment","source_pdf","source_clean_md","ability_action_candidate","decomposition_status","kp_id","mapping_level","na_reason"):
            if field not in n: errors.append(f"{n.get('response_node_id')}: missing {field}")
        if n.get("mapping_level") != "M0" or n.get("kp_id") != "N/A": errors.append(f"{n.get('response_node_id')}: non-M0 draft mapping")
        if not (ROOT/n["source_question_segment"]).exists(): errors.append(f"{n.get('response_node_id')}: missing question segment")
        if not (ROOT/n["source_pdf"]).exists(): errors.append(f"{n.get('response_node_id')}: missing source PDF")
        if n.get("decomposition_status") == "missing_source_marker": warnings.append(f"{n['response_node_id']}: source marker missing")
    for eid, rows in by_exam.items():
        year=int(eid.rsplit('-',1)[-1]); count=expected.get(year)
        ids=sorted(n["question_id"] for n in rows)
        if count is None or ids != list(range(1,count+1)): errors.append(f"{eid}: question denominator mismatch {ids}")
        if len(rows)!=count: errors.append(f"{eid}: node count {len(rows)} != {count}")
    if len(by_exam)!=17: errors.append(f"exam count {len(by_exam)} != 17")
    report={"schema_version":"exam-kp-extraction-validation-0.1","result":"passed" if not errors else "failed","node_count":len(nodes),"exam_count":len(by_exam),"errors":errors,"warnings":warnings,"checks":{"m0_boundary":not any('non-M0' in x for x in errors),"provenance":not any('missing source' in x for x in errors),"denominators":not any('denominator' in x or 'node count' in x for x in errors)}}
    path=ROOT/"work/knowledge/_meta/validation_reports/exam_kp_extraction_validation.json"
    path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if not errors else 1

if __name__ == "__main__": raise SystemExit(main())
