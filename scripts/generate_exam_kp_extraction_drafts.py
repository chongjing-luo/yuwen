#!/usr/bin/env python3
"""Generate conservative exam response-node / knowledge-point draft records.

This is the first EKP pass after structural extraction.  It creates one
top-level response node per stable question and records explicit candidate
subquestion counts, ability-action hints and provenance.  It never invents a
KP link: every row is M0 with KP_ID=N/A until a reviewed small-question node
and an accepted textbook KP have bidirectional evidence.
"""
from __future__ import annotations

import json, re, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "work/knowledge/_meta"
OUT = ROOT / "work/knowledge/exams/workbench"

ACTION = {
    "word_pronunciation": "辨析字音",
    "orthography": "辨析字形",
    "word_usage": "辨析词语使用",
    "sentence_grammar": "辨析病句",
    "modern_reading_informational": "筛选并分析现代文信息",
    "ancient_vocab": "解释文言实词",
    "ancient_function_words": "辨析文言虚词意义和用法",
    "ancient_text_content": "概括分析文言文内容",
    "ancient_reading": "理解分析文言文",
    "classical_translation": "翻译文言句子",
    "poetry_appreciation": "鉴赏古代诗歌",
    "classical_memorization": "识记并默写名篇名句",
    "literary_reading": "分析鉴赏文学类文本",
    "practical_reading": "分析实用类文本",
    "language_application": "完成语言文字运用任务",
    "summary_or_application": "概括或完成应用表达",
    "practical_or_expansion": "完成应用表达或扩写",
    "sentence_expansion": "扩展或仿写句子",
    "parallelism_or_practical": "完成修辞或应用表达",
    "summary": "概括信息",
    "completion": "补写语句",
    "topic_writing": "根据材料完成写作",
}
EXAM_POINT = {
    "word_pronunciation": "现代汉语普通话字音辨析",
    "orthography": "现代汉字字形辨析",
    "word_usage": "词语/熟语语境使用辨析",
    "sentence_grammar": "病句结构与语意辨析",
    "modern_reading_informational": "现代文信息筛选、概括与推断",
    "ancient_vocab": "文言实词语境释义",
    "ancient_function_words": "文言虚词意义和用法辨析",
    "ancient_text_content": "文言文内容概括与分析",
    "ancient_reading": "文言文断句、文化常识与内容理解",
    "classical_translation": "文言句子翻译",
    "poetry_appreciation": "古代诗歌形象、情感与表达手法鉴赏",
    "classical_memorization": "名篇名句理解性默写",
    "literary_reading": "文学类文本形象、结构、语言与主题鉴赏",
    "practical_reading": "实用类文本信息与表达目的分析",
    "language_application": "语言文字运用中的衔接、补写、辨析与表达",
    "summary_or_application": "信息概括与应用表达",
    "practical_or_expansion": "应用写作或语句扩展",
    "sentence_expansion": "仿写、扩写与修辞表达",
    "parallelism_or_practical": "修辞组织与应用表达",
    "summary": "材料信息压缩与概括",
    "completion": "语句补写与语意连贯",
    "topic_writing": "材料作文立意、构思与书面表达",
}

def clean_body(path: Path) -> str:
    text = path.read_text(encoding="utf8", errors="replace")
    return text.split("---\n\n", 2)[-1].strip()

def candidate_subquestions(body: str) -> dict:
    markers = re.findall(r"(?<!\d)[（(]\s*([1-9][0-9]?)\s*[）)]", body)
    scores = re.findall(r"[（(]\s*(\d+)\s*分\s*[）)]", body)
    choice_group = bool(re.search(r"任选|选一|限选|两题", body))
    return {
        "explicit_subquestion_marker_count": len(markers),
        "explicit_subquestion_labels": markers[:20],
        "score_candidates": [int(x) for x in scores[:10]],
        "choice_group_candidate": choice_group,
        "decomposition_status": "top_level_only",
    }

def main() -> int:
    calibration = json.loads((META / "exam_calibration_manifest.json").read_text(encoding="utf8"))
    all_nodes=[]; reports=[]
    draft_dir=OUT / "exam_drafts"
    draft_dir.mkdir(parents=True, exist_ok=True)
    for rec in calibration["records"]:
        exam_id=rec["exam_id"]
        root=ROOT / rec["derived_output_root"]
        qledger=root / "ledger/questions-question.jsonl"
        aledger=root / "ledger/questions-analysis.jsonl"
        qrows=[json.loads(x) for x in qledger.read_text(encoding="utf8").splitlines() if x.strip()]
        arows={int(json.loads(x)["question_id"]):json.loads(x) for x in aledger.read_text(encoding="utf8").splitlines() if x.strip()}
        md=[]
        md.extend(["---", "schema_version: \"exam-analysis-draft-0.2\"", f"exam_id: \"{exam_id}\"", "status: \"candidate_structural\"", f"calibration_id: \"{calibration['calibration_id']}\"", "source_status: \"unverified_local_provided\"", "mapping_status: \"M0_only\"", "decomposition_scope: \"top_level_question_nodes\"", f"generated_at: \"{time.strftime('%Y-%m-%dT%H:%M:%S%z')}\"", "---", "", f"# 真题知识点抽取草稿：{exam_id}", "", "> 本稿只完成稳定顶层题号、题型、材料、页级定位和能力动作候选。未把题型相似性写成教材KP映射；所有关系均为 M0。", "", "## 顶层题目节点", "", "| 节点 | 题段 | section | 题型 | 页码 | 材料 | 子问候选 | 能力动作候选 | 映射 |", "|---|---|---|---|---:|---|---:|---|---|"])
        missing=[]
        for row in qrows:
            qid=int(row["question_id"]); qkey=f"Q{qid:03d}"; seg=ROOT/row["segment_path"]; body=clean_body(seg)
            sub=candidate_subquestions(body)
            if row.get("segmentation_status") == "missing_source_marker": missing.append(qid)
            node_id=f"{exam_id}-Q{qid:03d}-TOP"
            arow=arows.get(qid,{})
            node={
                "response_node_id":node_id,"exam_id":exam_id,"year":rec["year"],"paper_code":rec["paper_code"],
                "question_id":qid,"subquestion_code":"TOP","source_question_segment":row["segment_path"],
                "source_analysis_segment":arow.get("segment_path"),"source_pdf":row["source_pdf"],"source_mineru_md":row["source_mineru_md"],
                "source_clean_md":row["source_clean_md"],"source_pdf_page_index_start":row.get("source_pdf_page_index_start"),"source_pdf_page_index_end":row.get("source_pdf_page_index_end"),
                "source_locator_status":row.get("source_locator_status"),"source_block_ids":row.get("source_block_ids",[]),
                "section_id":row.get("section_id"),"question_type_l1":row.get("question_type_l1"),"question_type_l2":row.get("question_type_l2"),
                "material_id":row.get("material_id"),"prompt_excerpt":body[:500],"ability_action_candidate":ACTION.get(row.get("question_type_l2"),"待人工核定"),
                "four_layer":"N/A","four_wings":"N/A","context_type":"N/A","atomic_exam_point":"N/A",
                "atomic_exam_point_candidate":EXAM_POINT.get(row.get("question_type_l2"),"待人工核定"),
                "candidate_basis":"题型配置与题段首轮文本；须在真实小问拆解和评分标准复核后确认",
                "score":"N/A","score_candidates":sub["score_candidates"],"explicit_subquestion_labels":sub["explicit_subquestion_labels"],
                "explicit_subquestion_marker_count":sub["explicit_subquestion_marker_count"],"choice_group_candidate":sub["choice_group_candidate"],
                "decomposition_status":"missing_source_marker" if row.get("segmentation_status")=="missing_source_marker" else "top_level_only",
                "answer_source_status":"candidate_unverified","evidence_id":f"EV-EXAM-{exam_id}-Q{qid:03d}-SOURCE",
                "kp_id":"N/A","mapping_level":"M0","na_reason":"尚未完成小问级人工拆解、答案/评分核验和教材KP双向证据；题型/动作候选不构成映射。",
                "review_status":"needs_pdf_review" if row.get("segmentation_status")=="missing_source_marker" else "needs_manual_review",
                "segment_clean_sha256":row.get("segment_clean_sha256"),
            }
            all_nodes.append(node)
            md.append(f"| {node_id} | [[{row['segment_path']}|{qkey}]] | {row.get('section_id','N/A')} | `{row.get('question_type_l2','N/A')}` | {row.get('source_pdf_page_start','N/A')}–{row.get('source_pdf_page_end','N/A')} | {row.get('material_id') or 'N/A'} | {sub['explicit_subquestion_marker_count']} | {node['ability_action_candidate']} | `M0 / N/A` |")
        md += ["", "## 结构与映射边界", "", f"- 顶层题目节点：{len(qrows)}；期望分母：{rec['top_level_question_count']}。", f"- 子问候选标记仅供人工复核，不能直接当作作答节点；当前全部 `decomposition_status=top_level_only`（缺失题号除外）。", f"- 缺失源标记：{missing or '无'}。", "- 只有稳定小问、官方/可核验答案或评分来源及教材KP双向证据齐备后，才允许 M1/M2/M3；否则保持 M0。", ""]
        target=draft_dir/f"{exam_id}.md"; target.write_text("\n".join(md)+"\n",encoding="utf8")
        reports.append({"exam_id":exam_id,"node_count":len(qrows),"expected_count":rec["top_level_question_count"],"missing_source_marker_questions":missing,"draft_path":str(target.relative_to(ROOT))})
    jsonl=OUT/"exam_response_nodes_top_level.jsonl"
    jsonl.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in all_nodes)+"\n",encoding="utf8")
    report_path=OUT/"EXAM-KP-EXTRACTION-DRAFT-REPORT.md"
    lines=["---","schema_version: \"exam-kp-extraction-draft-report-0.1\"","status: \"candidate_structural\"",f"calibration_id: \"{calibration['calibration_id']}\"",f"node_count: {len(all_nodes)}","mapping_status: \"M0_only\"","---","","# 高考知识点抽取首轮草稿回执","","> 本批次完成 2008—2024 的顶层题目节点提取。它是 EKP 的结构化首轮，不等于小问级知识点完成，也不建立教材—真题确定性映射。","","| Exam | 顶层节点 | 期望 | 缺失源标记 | 草稿 |","|---|---:|---:|---|---|"]
    for x in reports: lines.append(f"| {x['exam_id']} | {x['node_count']} | {x['expected_count']} | {x['missing_source_marker_questions'] or '无'} | [[{x['draft_path']}|打开]] |")
    lines += ["","## 已完成的垂直切片","","- 2008：已拆出 24 个作答节点，包含 1 个任选组/2 个分支，并复算总分 150；见 `EXAM-2008-SC-response_nodes.jsonl` 与对应验证报告。","- 2009—2012、2014—2015：各完成逐页 PDF 视觉复核和独立回执；2009/2010 文件名与PDF首页‘解析’标签冲突已显式保留。","- 2013：已拆出 23 个保守作答节点，复算总分 150；独立复核回执登记 OCR 与答案来源缺口。","- 2016：已拆出 27 个节点，按阅读二选一校正后复算 150；图示题保留图片源路径。","- 2017：已拆出 23 个保守作答节点，复算总分 150；Q6 保留为单一 5 分节点，Q11 的 OCR 残片显式标记；已完成逐页 PDF 视觉复核与独立视觉回执。","- 2018：已建立 10 个顶层保守作答节点，按卷面 Q1—Q10 总分复算 150；Q7 内部无稳定独立分值，暂不虚拆，并已完成逐页 PDF 视觉复核。","- 2019：已建立 10 个顶层保守作答节点，按卷面 Q1—Q10 总分复算 150；漫画材料保留图像源路径，并已完成逐页 PDF 视觉复核。","- 2020：已建立 10 个顶层保守作答节点，按卷面 Q1—Q10 总分复算 150；Q8 页码/OCR 残片已显式隔离，并已完成逐页 PDF 视觉复核。","- 2021—2023：各生成 22 个保守作答节点，逐页完成 PDF 视觉复核并复算 150；语言文字运用组总分保留在组首节点，未虚构小问分值。","- 2024：已生成 25 个保守作答节点，翻译/默写按稳定分值拆分；Q4 OCR缺字、Q6边界与缺失答案源显式登记。","","## 下一步人工批次","","1. 进入全部年份答案/评分来源核验，仍将非官方解析标记为 `candidate_unverified`。","2. 对已稳定的小问节点补登记四层、四翼、情境、能力动作和原子考点，所有直接引文回看 PDF。","3. 仅在题文—答案/评分—教材KP三方证据闭合后建立 M1/M2 映射；其余继续保持 M0。","4. 再将 2018 Q7、2019—2023 各题组及其他尚未稳定的组内节点细化为真实作答节点。"]
    report_path.write_text("\n".join(lines)+"\n",encoding="utf8")
    print(json.dumps({"node_count":len(all_nodes),"exam_count":len(reports),"jsonl":str(jsonl.relative_to(ROOT)),"report":str(report_path.relative_to(ROOT))},ensure_ascii=False))
    return 0

if __name__ == "__main__": raise SystemExit(main())
