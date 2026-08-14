#!/usr/bin/env python3
"""Extract the remaining 2009--2015 language-task candidate nodes.

This deliberately closes the six uncovered vertical nodes without turning
answers embedded in legacy analysis pages into authoritative answer records.
The output is a traceable, M0-only handoff for later manual review.
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
OUT_JSONL = OUT_DIR / "remaining_language_2009_2015.jsonl"
OUT_MD = OUT_DIR / "remaining_language_2009_2015.md"
TARGET_TYPES = {"sentence_segmentation", "summary_or_application"}
EXPECTED_COUNTS = {"sentence_segmentation": 3, "summary_or_application": 3}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def remaining_evidence(type_name: str, text: str) -> tuple[str, list[str]]:
    """Extract only task-relevant descriptive lines, never answer text."""
    if not text:
        return "", []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if type_name == "sentence_segmentation":
        markers = ("断句", "文言断句", "虚词", "句式", "语气", "标志")
        ability_markers = ("能力层级", "考点", "试题分析", "考查")
    else:
        markers = ("语言表达", "访谈", "说明性文字", "宣传语", "比喻", "简明", "连贯", "得体", "表达运用")
        ability_markers = ("能力层级", "考点", "试题分析", "考查")
    selected = [line for line in lines if any(marker in line for marker in markers + ability_markers)]
    joined = " ".join(selected[:8])
    levels: list[str] = []
    for match in re.finditer(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined):
        value = match.group(1)
        if value not in levels:
            levels.append(value)
    return joined, levels


def action_candidate(type_name: str, prompt: str) -> str:
    text = prompt or ""
    if type_name == "sentence_segmentation":
        return "依据文言句意、虚词/句式和语气标志划分分句"
    if "访谈" in text:
        return "围绕交往目的设计递进、简明、得体的访谈问题"
    if "说明性文字" in text or "字形演变" in text:
        return "从图表筛选特征并写成准确、简明、连贯的说明"
    if "宣传语" in text or "比喻" in text:
        return "紧扣宣传目的并运用比喻拟写简洁、有号召力的宣传语"
    return "依据材料和表达要求组织简明、连贯、得体的语言"


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-SC-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2009 <= row.get("year", 0) <= 2015 and row.get("question_type_l2") in TARGET_TYPES:
                if row.get("question_type_l2") == "sentence_segmentation" and row.get("question_id") != 12:
                    continue
                if row.get("question_type_l2") == "summary_or_application" and row.get("question_id") != 19:
                    continue
                if row.get("year") not in {2013, 2014, 2015}:
                    continue
                rows.append(row)
    return sorted(rows, key=lambda row: (row["question_type_l2"], row["year"], row["response_node_id"]))


def make_record(row: dict) -> dict:
    type_name = row["question_type_l2"]
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    evidence, levels = remaining_evidence(type_name, analysis)
    upstream_status = row.get("answer_source_status")
    if upstream_status == "missing":
        status = "candidate_source_without_answer_text_authority_missing" if analysis else "missing_analysis_source"
        gate = "source_authority_missing"
    elif analysis:
        status = "remaining_language_candidate_source"
        gate = "remaining_language_answer_and_scoring_review_required"
    else:
        status = "missing_analysis_source"
        gate = "answer_source_missing"
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "REMAINING-LANGUAGE-2009-2015",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": type_name,
        "response_form": "language_expression_free_response" if type_name == "summary_or_application" else "constructed_text_structural_response",
        "analysis_scope": "question_segment_with_possible_related_context",
        "candidate_atomic_exam_point": (
            "文言文断句：依据句意、虚词、句式和语气标志划分分句"
            if type_name == "sentence_segmentation"
            else "信息概括与应用表达：访谈问题、说明性文字或宣传语"
        ),
        "candidate_ability_action": action_candidate(type_name, row.get("prompt_excerpt")),
        "candidate_basis": "题型标签、题干任务和解析候选中的语言/结构考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None,
        "answer_candidate_method": "remaining_language_not_auto_extracted",
        "answer_candidate_status": status,
        "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": upstream_status,
        "source_authority_status": "missing" if upstream_status == "missing" else "unverified_local_provided",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": evidence,
        "ability_level_candidates": levels,
        "subskill_candidates": (
            ["文言句意理解", "虚词/句式识别", "语气标志", "分句边界判断"]
            if type_name == "sentence_segmentation"
            else ["信息筛选", "结构组织", "简明连贯", "语言得体", "修辞运用"]
        ),
        "manual_review_gate": gate,
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "答案/评分独立核验与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "REMAINING-LANGUAGE-2009-2015"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 剩余语言表达与文言断句小问级知识点候选批次（2013—2015）",
        "",
        "> 本批次补齐 2013—2015 的 3 个文言断句节点和 3 个信息概括/应用表达节点。解析中可能含示例答案，但不自动转录；所有记录保持 `M0 / kp_id=N/A`。",
        "",
        "| 题型 | 年份 | 节点 | 分值 | 上游状态 | 候选作答动作 | 审核门 |",
        "|---|---:|---|---:|---|---|---|",
    ]
    for type_name in sorted({row["question_type_l2"] for row in rows}):
        for row in [item for item in rows if item["question_type_l2"] == type_name]:
            lines.append(
                f"| `{type_name}` | {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | "
                f"{row['score_candidate'] or 'N/A'} | `{row['answer_candidate_status']}` | {row['candidate_ability_action']} | "
                f"`{row['manual_review_gate']}` |"
            )
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；2013 年权威缺失门禁：{counts.get('candidate_source_without_answer_text_authority_missing', 0)}；其余解析候选：{counts.get('remaining_language_candidate_source', 0)}。",
        "- `answer_candidate` 全部保持空值；`analysis_contains_answer_marker=true` 只表示解析中出现答案段，不表示答案已核验。",
        "",
        "## 复核规则",
        "",
        "1. 文言断句逐页核对原文、断线范围、断句数和句意；信息概括/应用题逐页核对材料、图表、字数、修辞和表达要求。",
        "2. 将答案示例、解析思路与评分点分栏登记；没有独立官方答案/评分材料时保持未核验。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/高考分析/kp_batches/remaining_language_2009_2015.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/remaining_language_2009_2015.md` |",
        "| 生成脚本 | `scripts/extract_remaining_language_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = [make_record(row) for row in load_nodes()]
    if len(rows) != sum(EXPECTED_COUNTS.values()):
        raise SystemExit(f"expected {sum(EXPECTED_COUNTS.values())} nodes, got {len(rows)}")
    actual = Counter(row["question_type_l2"] for row in rows)
    if dict(actual) != EXPECTED_COUNTS:
        raise SystemExit(f"unexpected type counts: {dict(actual)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "REMAINING-LANGUAGE-2009-2015", "record_count": len(rows), "type_counts": dict(actual), "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
