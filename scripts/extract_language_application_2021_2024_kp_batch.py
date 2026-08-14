#!/usr/bin/env python3
"""Extract 2021--2024 language-application candidate nodes.

The newer national-paper language section has stable Q17--Q21 nodes.  This
batch keeps their distinct task forms while treating all answer material as
unverified candidate evidence and retaining the 2024 Q21 authority gap.
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
OUT_JSONL = OUT_DIR / "language_application_2021_2024.jsonl"
OUT_MD = OUT_DIR / "language_application_2021_2024.md"

SUBTYPES = {
    (year, qid): subtype_name
    for year in (2021, 2022, 2023, 2024)
    for qid, subtype_name in {
        17: "lexical_or_idiom_usage",
        18: "sequence_selection" if year == 2021 else "sentence_error" if year == 2022 else "sentence_revision" if year == 2023 else "sentence_splitting",
        19: "sentence_error" if year == 2021 else "rhetoric_identification" if year in (2022, 2024) else "sentence_expansion",
        20: "completion" if year in (2021, 2022) else "commentary_expression" if year == 2023 else "sentence_revision",
        21: "rhetoric_effect" if year == 2021 else "rhetoric_identification" if year == 2022 else "explanatory_expression" if year == 2023 else "summary_or_application",
    }.items()
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def atomic_point(subtype_name: str) -> str:
    return {
        "lexical_or_idiom_usage": "词语/成语语境意义和使用辨析",
        "sequence_selection": "语句衔接与语意连贯",
        "sentence_error": "病句结构与语意辨析",
        "sentence_revision": "语句修改与准确、连贯表达",
        "sentence_splitting": "长句改写为短句与信息分层",
        "rhetoric_identification": "修辞手法辨析与表达效果",
        "sentence_expansion": "仿写补写与句式、语意保持",
        "completion": "语句补写与语段逻辑",
        "commentary_expression": "简洁流畅的评论表达",
        "rhetoric_effect": "修辞表达效果分析",
        "explanatory_expression": "面向对象的成语讲解与说明",
        "summary_or_application": "保留必要信息的简明概括",
    }[subtype_name]


def action(subtype_name: str) -> str:
    return {
        "lexical_or_idiom_usage": "结合上下文辨析词语/成语意义、感情色彩和搭配",
        "sequence_selection": "依据语段结构和语意逻辑选择衔接语句",
        "sentence_error": "识别成分、搭配、逻辑或指代问题并修改/判断",
        "sentence_revision": "保持原意，调整语序和词语使表达准确流畅",
        "sentence_splitting": "拆分长句并重组信息层次，保持原意",
        "rhetoric_identification": "辨析修辞方式并说明其语境表达效果",
        "sentence_expansion": "保持内容和句式关系完成仿写或补写",
        "completion": "依据上下文补写内容贴切、逻辑严密的语句",
        "commentary_expression": "提炼观点并用限定字数作简洁评论",
        "rhetoric_effect": "结合语境分析拟人等修辞的表达效果",
        "explanatory_expression": "面向小学生准确、流畅地讲解成语",
        "summary_or_application": "筛选必要信息并压缩为简明得体的自述",
    }[subtype_name]


def evidence(text: str, subtype_name: str) -> tuple[str, list[str]]:
    if not text:
        return "", []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = ("考点", "能力层级", "试题分析", "语言表达", "衔接", "语病", "修辞", "补写", "成语", "缩写", "评论", "仿照", "改成")
    selected = [line for line in lines if any(marker in line for marker in markers)]
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
            key = (row.get("year"), row.get("question_id"))
            if row.get("question_type_l2") == "language_application" and key in SUBTYPES:
                rows.append(row)
    return sorted(rows, key=lambda row: (row["year"], row["question_id"], row["response_node_id"]))


def make_record(row: dict) -> dict:
    sub = SUBTYPES[(row["year"], row["question_id"])]
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    excerpt, levels = evidence(analysis, sub)
    upstream = row.get("answer_source_status")
    if upstream == "missing":
        status = "candidate_source_without_answer_text_authority_missing" if analysis else "missing_analysis_source"
        gate = "source_authority_missing"
    else:
        status = "candidate_source_without_authoritative_answer"
        gate = "language_application_answer_and_scoring_review_required"
    selected_response = sub in {"lexical_or_idiom_usage", "sequence_selection", "sentence_error", "rhetoric_identification"}
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "LANGUAGE-APPLICATION-2021-2024",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": row.get("question_type_l2"),
        "candidate_subtype": sub,
        "response_form": "selected_response" if selected_response else "language_expression_free_response",
        "analysis_scope": "question_segment_with_possible_related_context",
        "candidate_atomic_exam_point": atomic_point(sub),
        "candidate_ability_action": action(sub),
        "candidate_basis": "稳定题号、题干任务、分值和解析候选中的语言运用考点线索；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None,
        "answer_candidate_method": "language_application_not_auto_extracted",
        "answer_candidate_status": status,
        "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": upstream,
        "source_authority_status": "missing" if upstream == "missing" else "unverified_local_provided",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": excerpt,
        "ability_level_candidates": levels,
        "subskill_candidates": ["语境判断", "信息组织", "逻辑衔接", "简明准确", "修辞/句式运用"],
        "manual_review_gate": gate,
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "答案/评分独立核验、题面边界复核与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "LANGUAGE-APPLICATION-2021-2024"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 语言文字运用小问候选批次（2021—2024）",
        "",
        "> 本批次覆盖全国甲卷 2021—2024 的 Q17—Q21，共 20 条稳定节点。答案与评分均不自动转录；2024 Q21 的来源权威缺口保持 `source_authority_missing`。",
        "",
        "| 年份 | 节点 | 子类型 | 分值 | 作答形式 | 候选动作 | 审核门 |",
        "|---:|---|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | `{row['candidate_subtype']}` | "
            f"{row['score_candidate'] or 'N/A'} | `{row['response_form']}` | {row['candidate_ability_action']} | `{row['manual_review_gate']}` |"
        )
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；权威缺失门禁：{counts.get('candidate_source_without_answer_text_authority_missing', 0)}；其余未核验解析候选：{counts.get('candidate_source_without_authoritative_answer', 0)}。",
        "- `answer_candidate` 全部为空；解析中出现“答案”仅表示候选源存在，不表示官方答案或评分标准已核验。",
        "",
        "## 复核规则",
        "",
        "1. 逐题回看空白卷题干、材料和选项；开放题另外登记答案示例、评分点和字数/修辞限制。",
        "2. 2024 Q21 权威来源缺失时，不得用解析示例替代官方答案或评分标准。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/高考分析/kp_batches/language_application_2021_2024.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/language_application_2021_2024.md` |",
        "| 生成脚本 | `scripts/extract_language_application_2021_2024_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = [make_record(row) for row in load_nodes()]
    if len(rows) != 20:
        raise SystemExit(f"expected 20 nodes, got {len(rows)}")
    if set((row["year"], row["question_id"]) for row in rows) != set(SUBTYPES):
        raise SystemExit("coverage mismatch for 2021--2024 Q17--Q21")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "LANGUAGE-APPLICATION-2021-2024", "record_count": len(rows), "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
