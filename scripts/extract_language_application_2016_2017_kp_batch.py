#!/usr/bin/env python3
"""Extract stable 2016--2017 language-application candidate nodes.

Q7--Q11 are independent, visibly scored nodes in both papers.  This batch
records task-level candidate evidence only; it does not promote third-party
analysis answers or create textbook mappings.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from extract_word_pronunciation_kp_batch import body

ROOT = Path(__file__).resolve().parents[1]
SLICE_DIR = ROOT / "work/knowledge/高考分析"
OUT_DIR = SLICE_DIR / "kp_batches"
OUT_JSONL = OUT_DIR / "language_application_2016_2017.jsonl"
OUT_MD = OUT_DIR / "language_application_2016_2017.md"
EXPECTED_SUBTYPES = {
    "idiom_usage": 2,
    "sentence_error": 2,
    "discourse_connective_selection": 2,
    "completion": 2,
    "constructed_language_response": 2,
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def subtype(year: int, question_id: int) -> str:
    if question_id == 7:
        return "idiom_usage"
    if question_id == 8:
        return "sentence_error"
    if question_id == 9:
        return "discourse_connective_selection"
    if question_id == 10:
        return "completion"
    return "constructed_language_response"


def action(subtype_name: str) -> str:
    return {
        "idiom_usage": "结合语境辨析成语意义、感情色彩和使用对象",
        "sentence_error": "识别句子成分、搭配和逻辑关系并判断病句",
        "discourse_connective_selection": "依据语意衔接和逻辑关系选择恰当词语",
        "completion": "依据语段结构、语意和逻辑补写连贯语句",
        "constructed_language_response": "把图示/推断要求转化为准确、简明、连贯的表达",
    }[subtype_name]


def evidence(text: str, subtype_name: str) -> tuple[str, list[str]]:
    if not text:
        return "", []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = {
        "idiom_usage": ("成语", "熟语", "词语使用"),
        "sentence_error": ("语病", "病句", "句子"),
        "discourse_connective_selection": ("词语", "衔接", "连贯", "关联词"),
        "completion": ("补写", "语意完整", "连贯", "逻辑严密"),
        "constructed_language_response": ("语言表达", "推断", "构思", "准确", "连贯"),
    }[subtype_name]
    selected = [line for line in lines if any(marker in line for marker in markers + ("考点", "能力层级", "试题分析"))]
    joined = " ".join(selected[:8])
    levels: list[str] = []
    for match in re.finditer(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined):
        value = match.group(1)
        if value not in levels:
            levels.append(value)
    return joined, levels


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("year") in {2016, 2017} and row.get("question_type_l2") == "language_application" and row.get("question_id") in {7, 8, 9, 10, 11}:
                rows.append(row)
    return sorted(rows, key=lambda row: (row["year"], row["question_id"], row["response_node_id"]))


def make_record(row: dict) -> dict:
    sub = subtype(row["year"], row["question_id"])
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    excerpt, levels = evidence(analysis, sub)
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "LANGUAGE-APPLICATION-2016-2017",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": row.get("question_type_l2"),
        "candidate_subtype": sub,
        "response_form": "selected_response" if row["question_id"] in {7, 8, 9} else "language_expression_free_response",
        "analysis_scope": "question_segment_with_possible_related_context",
        "candidate_atomic_exam_point": {
            "idiom_usage": "成语语境使用辨析",
            "sentence_error": "病句结构与语意辨析",
            "discourse_connective_selection": "语段衔接与关联词语使用",
            "completion": "语句补写与语意连贯",
            "constructed_language_response": "图示转述或推断评价中的简明、准确表达",
        }[sub],
        "candidate_ability_action": action(sub),
        "candidate_basis": "独立题号、题干任务、分值和解析候选中的题型/考点线索；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None,
        "answer_candidate_method": "language_application_not_auto_extracted",
        "answer_candidate_status": "candidate_source_without_authoritative_answer",
        "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": row.get("answer_source_status"),
        "source_authority_status": "unverified_local_provided",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": excerpt,
        "ability_level_candidates": levels,
        "subskill_candidates": {
            "idiom_usage": ["语境义", "感情色彩", "使用对象", "搭配限制"],
            "sentence_error": ["成分残缺", "搭配不当", "结构混乱", "逻辑关系"],
            "discourse_connective_selection": ["语意衔接", "逻辑关系", "关联词语"],
            "completion": ["语段结构", "语意连贯", "内容贴切", "逻辑严密"],
            "constructed_language_response": ["信息转换", "推断边界", "简明准确", "语言连贯"],
        }[sub],
        "manual_review_gate": "language_application_answer_and_scoring_review_required",
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "答案/评分独立核验、OCR边界复核与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "LANGUAGE-APPLICATION-2016-2017"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 语言文字运用稳定小问候选批次（2016—2017）",
        "",
        "> 本批次覆盖两套新课标Ⅲ卷中独立稳定的 Q7—Q11，共 10 条节点。选择题答案、补写和开放表达均不自动转录；2017 Q9/Q11 的 OCR 疑点随源记录保留。",
        "",
        "| 年份 | 节点 | 子类型 | 分值 | 作答形式 | 候选动作 | 审核门 |",
        "|---:|---|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | `{row['candidate_subtype']}` | "
            f"{row['score_candidate'] or 'N/A'} | `{row['response_form']}` | {row['candidate_ability_action']} | `{row['manual_review_gate']}` |"
        )
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；子类型分布：" + "、".join(f"{k}={v}" for k, v in sorted(Counter(row['candidate_subtype'] for row in rows).items())) + "。",
        "- `answer_candidate` 全部为空；解析中出现“答案”仅表示本地解析候选存在，不表示官方答案或评分标准已核验。",
        "",
        "## 复核规则",
        "",
        "1. 选择题须回看空白卷选项、独立答案来源和评分口径；自由作答须另行登记答案示例与评分点。",
        "2. 2017 Q9/Q11 的 OCR/水印疑点不能静默修订，需先完成 PDF 视觉复核。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/高考分析/kp_batches/language_application_2016_2017.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/language_application_2016_2017.md` |",
        "| 生成脚本 | `scripts/extract_language_application_2016_2017_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = [make_record(row) for row in load_nodes()]
    if len(rows) != 10:
        raise SystemExit(f"expected 10 nodes, got {len(rows)}")
    actual = Counter(row["candidate_subtype"] for row in rows)
    if dict(actual) != EXPECTED_SUBTYPES:
        raise SystemExit(f"unexpected subtype counts: {dict(actual)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "LANGUAGE-APPLICATION-2016-2017", "record_count": len(rows), "subtype_counts": dict(actual)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
