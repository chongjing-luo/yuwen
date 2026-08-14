#!/usr/bin/env python3
"""Extract candidate records for old-paper language-expression tasks."""
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
OUT_JSONL = OUT_DIR / "language_expression_2009_2015.jsonl"
OUT_MD = OUT_DIR / "language_expression_2009_2015.md"
TARGET_TYPES = {"sentence_expansion", "summary", "parallelism_or_practical", "practical_or_expansion"}
EXPECTED_COUNTS = {"sentence_expansion": 4, "summary": 4, "parallelism_or_practical": 4, "practical_or_expansion": 3}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def expression_evidence(text: str) -> tuple[str, list[str]]:
    if not text:
        return "", []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = ("语言表达", "扩展语句", "压缩语段", "仿写", "修辞", "概括", "表达运用", "能力层级")
    selected = [line for line in lines if any(marker in line for marker in markers)]
    joined = " ".join(selected[:8])
    levels = []
    for match in re.finditer(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined):
        value = match.group(1)
        if value not in levels:
            levels.append(value)
    return joined, levels


def action_candidate(type_name: str, prompt: str) -> str:
    text = prompt or ""
    if type_name == "summary":
        return "筛选材料信息并压缩、概括为限定形式"
    if "仿照" in text or "续写" in text or "补写" in text:
        return "保持句式/语意关系并运用指定修辞完成仿写"
    if "感激" in text or "人际关系" in text or "名著" in text:
        return "结合语境组织简明、连贯、得体的应用表达"
    return "依据要求组织语言并完成修辞/扩展表达"


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-SC-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2009 <= row.get("year", 0) <= 2015 and row.get("question_type_l2") in TARGET_TYPES:
                rows.append(row)
    return sorted(rows, key=lambda row: (row["question_type_l2"], row["year"], row["response_node_id"]))


def make_record(row: dict) -> dict:
    type_name = row["question_type_l2"]
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    evidence, levels = expression_evidence(analysis)
    upstream_status = row.get("answer_source_status")
    if upstream_status == "missing":
        status = "candidate_source_without_answer_text_authority_missing" if analysis else "missing_analysis_source"
        gate = "source_authority_missing"
    elif analysis:
        status = "language_expression_candidate_source"
        gate = "language_expression_answer_and_scoring_review_required"
    else:
        status = "missing_analysis_source"
        gate = "answer_source_missing"
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "LANGUAGE-EXPRESSION-2009-2015",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": type_name,
        "response_form": "language_expression_free_response",
        "analysis_scope": "question_segment_with_possible_related_context",
        "candidate_atomic_exam_point": "语言文字表达中的概括、扩展、仿写、修辞与应用表达",
        "candidate_ability_action": action_candidate(type_name, row.get("prompt_excerpt")),
        "candidate_basis": "题型标签、题干任务和解析候选中的语言表达考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None,
        "answer_candidate_method": "language_expression_not_auto_extracted",
        "answer_candidate_status": status,
        "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": upstream_status,
        "source_authority_status": "missing" if upstream_status == "missing" else "unverified_local_provided",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": evidence,
        "ability_level_candidates": levels,
        "subskill_candidates": ["信息压缩", "句式仿写", "修辞运用", "应用表达", "语言得体"],
        "manual_review_gate": gate,
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "语言表达答案/评分独立核验与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "LANGUAGE-EXPRESSION-2009-2015"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 语言文字综合表达小问级知识点候选批次（2009—2015）",
        "",
        "> 本批次合并概括、仿写、修辞和应用表达等自由作答题。只登记题干任务与候选考点，不自动生成答案或评分点；所有记录保持 `M0 / kp_id=N/A`。",
        "",
        "| 题型 | 年份 | 节点 | 分值 | 解析状态 | 候选作答动作 | 审核门 |",
        "|---|---:|---|---:|---|---|---|",
    ]
    for type_name in sorted({row["question_type_l2"] for row in rows}):
        for row in [item for item in rows if item["question_type_l2"] == type_name]:
            lines.append(f"| `{type_name}` | {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | {row['score_candidate'] or 'N/A'} | `{row['answer_candidate_status']}` | {row['candidate_ability_action']} | `{row['manual_review_gate']}` |")
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；语言表达解析候选源：{counts.get('language_expression_candidate_source', 0)}；权威缺失节点：{counts.get('candidate_source_without_answer_text_authority_missing', 0)}。",
        "- `answer_candidate` 全部保持空值，解析中出现“答案”字样不表示答案已核验。",
        "",
        "## 复核规则",
        "",
        "1. 逐页核对材料、题干、字数/句式/修辞要求、分值和 OCR/水印疑点。",
        "2. 独立登记信息要点、表达结构、修辞实现与评分点；不能把解析示例直接当官方答案。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/高考分析/kp_batches/language_expression_2009_2015.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/language_expression_2009_2015.md` |",
        "| 生成脚本 | `scripts/extract_language_expression_kp_batch.py` |",
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
    print(json.dumps({"batch": "LANGUAGE-EXPRESSION-2009-2015", "record_count": len(rows), "type_counts": dict(actual), "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
