#!/usr/bin/env python3
"""Extract candidate records for 2009--2015 poetry-appreciation tasks."""
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
OUT_JSONL = OUT_DIR / "poetry_appreciation_2009_2015.jsonl"
OUT_MD = OUT_DIR / "poetry_appreciation_2009_2015.md"
EXPECTED_COUNTS = {year: 2 for year in range(2009, 2016)}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def poetry_evidence(text: str) -> tuple[str, list[str]]:
    """Extract task markers only; answer/analysis text remains unverified."""
    if not text:
        return "", []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = ("鉴赏文学作品", "评价文学作品", "分析概括作者", "炼字", "思想内容", "表达技巧")
    selected = [line for line in lines if any(marker in line for marker in markers)]
    joined = " ".join(selected[:8])
    levels = []
    for match in re.finditer(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined):
        value = match.group(1)
        if value not in levels:
            levels.append(value)
    return joined, levels


def action_candidate(prompt: str) -> str:
    text = prompt or ""
    if any(term in text for term in ("情感", "心境", "志向")):
        return "结合诗句/意象分析诗歌情感与作者态度"
    if any(term in text for term in ("形象", "人物")):
        return "结合诗句概括诗歌形象特征"
    if any(term in text for term in ("字", "赏析", "表达效果", "手法")):
        return "结合语境赏析炼字、句子或表达技巧"
    return "结合全诗分析形象、语言、技巧或情感"


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-SC-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2009 <= row.get("year", 0) <= 2015 and row.get("question_type_l2") == "poetry_appreciation":
                rows.append(row)
    return sorted(rows, key=lambda row: (row["year"], row["response_node_id"]))


def make_record(row: dict) -> dict:
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    evidence, levels = poetry_evidence(analysis)
    upstream_status = row.get("answer_source_status")
    if upstream_status == "missing":
        status = "candidate_source_without_answer_text_authority_missing" if analysis else "missing_analysis_source"
        gate = "source_authority_missing"
    elif analysis:
        status = "poetry_candidate_source"
        gate = "poetry_answer_and_scoring_review_required"
    else:
        status = "missing_analysis_source"
        gate = "answer_source_missing"
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "POETRY-APPRECIATION-2009-2015",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": row.get("question_type_l2"),
        "response_form": "free_response_poetry_appreciation",
        "analysis_scope": "shared_top_level_analysis_segment",
        "candidate_atomic_exam_point": "古诗词形象、语言、表达技巧与思想情感鉴赏",
        "candidate_ability_action": action_candidate(row.get("prompt_excerpt")),
        "candidate_basis": "题型标签、题干任务和解析候选中的鉴赏考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None,
        "answer_candidate_method": "poetry_free_response_not_auto_extracted",
        "answer_candidate_status": status,
        "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": upstream_status,
        "source_authority_status": "missing" if upstream_status == "missing" else "unverified_local_provided",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": evidence,
        "ability_level_candidates": levels,
        "subskill_candidates": ["炼字炼句", "意象与情感", "表达技巧", "形象概括"],
        "manual_review_gate": gate,
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "诗歌简答答案/评分独立核验与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "POETRY-APPRECIATION-2009-2015"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 古诗词鉴赏小问级知识点候选批次（2009—2015）",
        "",
        "> 本批次覆盖炼字、形象、情感和表达技巧等自由作答小问。解析源常按顶层题目共享，因此仅登记题干任务和候选考点，不自动生成答案或评分点；所有记录保持 `M0 / kp_id=N/A`。",
        "",
        "| 年份 | 节点 | 分值 | 解析状态 | 候选作答动作 | 审核门 |",
        "|---:|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | {row['score_candidate'] or 'N/A'} | `{row['answer_candidate_status']}` | {row['candidate_ability_action']} | `{row['manual_review_gate']}` |")
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；共享解析候选源：{counts.get('poetry_candidate_source', 0)}；2013 年权威缺失：{counts.get('candidate_source_without_answer_text_authority_missing', 0)}。",
        "- `analysis_scope=shared_top_level_analysis_segment` 表示同一解析段可能服务同题两小问；不能把段内任一结论直接归给单个小问。",
        "- `answer_candidate` 全部保持空值；解析中出现“答案”字样也不表示答案已核验。",
        "",
        "## 复核规则",
        "",
        "1. 逐页核对诗文、设问、分值、材料边界和 OCR/水印疑点。",
        "2. 按小问分别登记诗句证据、作答要点、评分点和解析来源；共享解析段不得跨小问复制结论。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/高考分析/kp_batches/poetry_appreciation_2009_2015.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/poetry_appreciation_2009_2015.md` |",
        "| 生成脚本 | `scripts/extract_poetry_appreciation_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = [make_record(row) for row in load_nodes()]
    if len(rows) != 14:
        raise SystemExit(f"expected 14 nodes, got {len(rows)}")
    actual = Counter(row["year"] for row in rows)
    if dict(actual) != EXPECTED_COUNTS:
        raise SystemExit(f"unexpected year counts: {dict(actual)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "POETRY-APPRECIATION-2009-2015", "record_count": len(rows), "year_counts": dict(actual), "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
