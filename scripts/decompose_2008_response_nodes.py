#!/usr/bin/env python3
"""Derive the 2008 calibration paper's 24 response nodes and score ledger."""
from __future__ import annotations
import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008"
OUT=ROOT/"work/knowledge/exams/workbench"

def body(path): return (ROOT/path).read_text(encoding="utf8").split("---\n\n",2)[-1].strip()

def split_parts(text):
    # Keep the marker with each part and avoid treating option labels A/B/C/D
    # as response nodes.
    matches=list(re.finditer(r"(?<!\d)[（(]\s*([1-9][0-9]?)\s*[）)]",text))
    if not matches: return []
    out=[]
    for i,m in enumerate(matches): out.append((m.group(1),text[m.start():(matches[i+1].start() if i+1<len(matches) else len(text))].strip()))
    return out

def main()->int:
    rows=[json.loads(x) for x in (BASE/"ledger/questions-question.jsonl").read_text(encoding="utf8").splitlines() if x.strip()]
    by_q={int(r["question_id"]):r for r in rows}; nodes=[]
    score_map={**{q:3 for q in range(1,11)},11:[4,6],12:[2,6],13:[5,5],14:4,15:6,16:6,17:6,18:4,19:6,20:5,21:60}
    for q in range(1,22):
        r=by_q[q]; text=body(r["segment_path"]); parts=split_parts(text)
        if q in (11,12):
            for idx,(label,part) in enumerate(parts[:2]):
                node_code=f"{label}"; score=score_map[q][idx]
                nodes.append(make_node(r,q,node_code,part,score,"response_nodes_derived"))
        elif q==13:
            # The two numbered branches are alternatives, not two scored
            # questions; preserve both as a single choice_group.
            for label,part in parts[:2]:
                nodes.append(make_node(r,q,f"CHOICE-{label}",part,5,"response_nodes_derived",choice_group=True))
        else:
            nodes.append(make_node(r,q,"TOP",text,int(score_map[q]),"response_nodes_derived"))
    total=sum(n["score"] for n in nodes if n["subquestion_code"] not in ("CHOICE-2",))
    # The choice group contributes max 5, not both branches.
    total=sum(n["score"] for n in nodes if not (n["question_id"]==13 and n["subquestion_code"]=="CHOICE-2"))
    report={"schema_version":"exam-response-node-validation-0.1","exam_id":"GK-SC-2008","response_node_count":len(nodes),"choice_group_count":1,"choice_branch_count":2,"score_total":total,"expected_score_total":150,"result":"passed" if len(nodes)==24 and total==150 else "failed","errors":[] if len(nodes)==24 and total==150 else ["response node or score total mismatch"]}
    jsonl=OUT/"EXAM-2008-SC-response_nodes.jsonl"; jsonl.write_text("\n".join(json.dumps(n,ensure_ascii=False) for n in nodes)+"\n",encoding="utf8")
    md=["---","schema_version: \"exam-response-node-0.1\"","exam_id: \"GK-SC-2008\"","status: \"calibration_derived\"","mapping_status: \"M0_only\"","---","","# 2008 四川卷作答节点校准","","| 节点 | 题段 | 分值 | 任选组 | 提示摘要 |","|---|---|---:|---|---|"]
    for n in nodes: md.append(f"| {n['response_node_id']} | [[{n['source_question_segment']}|Q{n['question_id']:03d}]] | {n['score']} | {'是' if n['choice_group'] else '否'} | {n['prompt_excerpt'][:100].replace('|','／')} |")
    md += ["","## 复算","",f"- 作答节点：{len(nodes)}（预期24）","- 任选组：1组，2个分支，计分取一支","- 总分：150（12+9+9+23+22+15+60）","- 所有四层/四翼/情境/KP均保持N/A或M0，待人工评分标准与教材双向证据。"]
    (OUT/"EXAM-2008-SC-response_nodes.md").write_text("\n".join(md)+"\n",encoding="utf8")
    (ROOT/"work/knowledge/_meta/validation_reports/exam_2008_response_nodes.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(report,ensure_ascii=False))
    return 0 if report["result"]=="passed" else 1

def make_node(r,q,code,prompt,score,status,choice_group=False):
    return {"response_node_id":f"GK-SC-2008-Q{q:03d}-{code}","exam_id":"GK-SC-2008","question_id":q,"subquestion_code":code,"score":score,"source_question_segment":r["segment_path"],"source_pdf":r["source_pdf"],"source_mineru_md":r["source_mineru_md"],"source_clean_md":r["source_clean_md"],"source_pdf_page_index_start":r["source_pdf_page_index_start"],"source_pdf_page_index_end":r["source_pdf_page_index_end"],"source_locator_status":r["source_locator_status"],"prompt_excerpt":prompt[:500],"choice_group":choice_group,"decomposition_status":status,"four_layer":"N/A","four_wings":"N/A","context_type":"N/A","ability_action":"N/A","atomic_exam_point":"N/A","answer_source_status":"candidate_unverified","evidence_id":f"EV-EXAM-GK-SC-2008-Q{q:03d}-{code}-SOURCE","kp_id":"N/A","mapping_level":"M0","na_reason":"校准阶段仅拆解作答节点；答案/评分和教材KP双向证据尚未核验。"}

if __name__=="__main__": raise SystemExit(main())
