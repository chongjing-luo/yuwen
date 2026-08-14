#!/usr/bin/env python3
"""Extract conservative candidate records for 2016--2024 practical reading."""
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
OUT_JSONL = OUT_DIR / "practical_reading_2016_2024.jsonl"
OUT_MD = OUT_DIR / "practical_reading_2016_2024.md"
EXPECTED_COUNTS = {2016: 4, 2017: 3, 2018: 1, 2019: 1, 2020: 1, 2021: 3, 2022: 3, 2023: 3, 2024: 3}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def practical_evidence(text: str) -> tuple[str, list[str]]:
    if not text:
        return "", []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = ("筛选并整合", "分析概括", "归纳内容要点", "概括中心意思", "分析和评价", "本题考查学生")
    selected = [line.split("【答案】", 1)[0].strip() for line in lines if any(marker in line for marker in markers)]
    joined = " ".join(selected[:8])
    levels = []
    for match in re.finditer(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined):
        value = match.group(1)
        if value not in levels:
            levels.append(value)
    return joined, levels


def action_candidate(prompt: str) -> str:
    text = prompt or ""
    if "概括" in text or "作用" in text or "意义" in text:
        return "筛选材料信息并概括事实、作用或意义"
    if "评价" in text or "理解和分析" in text:
        return "结合材料内容判断信息并评价论证或表达"
    if "图" in text or "梳理" in text:
        return "整合图文材料并核对结构、流程或关系"
    return "筛选、整合并分析实用类材料信息"


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2016 <= row.get("year", 0) <= 2024 and row.get("question_type_l2") == "practical_reading":
                rows.append(row)
    return sorted(rows, key=lambda row: (row["year"], row["response_node_id"]))


def make_record(row: dict) -> dict:
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    evidence, levels = practical_evidence(analysis)
    status = "practical_candidate_source" if analysis else "missing_analysis_source"
    gate = "practical_answer_and_evidence_review_required" if analysis else "answer_source_missing"
    upstream_status = row.get("upstream_answer_source_status") or row.get("answer_source_status") or "unknown"
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "PRACTICAL-READING-2016-2024",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": row.get("question_type_l2"),
        "response_form": "practical_reading_response",
        "analysis_scope": "question_segment_with_possible_related_context",
        "candidate_atomic_exam_point": "实用类文本信息筛选、分析、概括与评价",
        "candidate_ability_action": action_candidate(row.get("prompt_excerpt")),
        "candidate_basis": "题型标签、题干任务和解析候选中的实用类阅读考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None,
        "answer_candidate_method": "practical_response_not_auto_extracted",
        "answer_candidate_status": status,
        "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": upstream_status,
        "source_authority_status": "unverified_local_provided" if upstream_status != "missing" else "missing",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": evidence,
        "ability_level_candidates": levels,
        "subskill_candidates": ["信息筛选", "图文整合", "概括分析", "评价推断"],
        "manual_review_gate": gate,
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "实用类阅读答案/评分独立核验与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---", 'schema_version: "exam-kp-candidate-batch-0.1"', 'batch_id: "PRACTICAL-READING-2016-2024"',
        'status: "candidate_only"', 'mapping_status: "M0_only"', "---", "",
        "# 实用类文本阅读小问级知识点候选批次（2016—2024）", "",
        "> 本批次覆盖实用类材料的信息筛选、图文整合、概括分析和评价推断。图表/图文题只保留题干与原始 PDF 链路，不对图示或 OCR 疑点做语义补写；答案/评分不自动抽取，所有记录保持 `M0 / kp_id=N/A`。", "",
        "| 年份 | 节点 | 分值 | 解析状态 | 候选作答动作 | 审核门 |", "|---:|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | {row['score_candidate'] or 'N/A'} | `{row['answer_candidate_status']}` | {row['candidate_ability_action']} | `{row['manual_review_gate']}` |")
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines += ["", "## 统计", "", f"- 总节点：{len(rows)}；实用类解析候选源：{counts.get('practical_candidate_source', 0)}；缺少解析源：{counts.get('missing_analysis_source', 0)}。", "- `analysis_scope=question_segment_with_possible_related_context` 表示解析段可能携带同组关联题上下文；结论不得跨小问复制。", "- `answer_candidate` 全部保持空值，解析中出现“答案”字样不表示答案已核验。", "", "## 复核规则", "", "1. 逐页核对材料、图表、题干、选项、题号、分值和 OCR/水印疑点。", "2. 将材料原文证据、图表结构、作答要点和评分点分栏登记；不能把解析结论直接当官方答案。", "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。", "", "| 产物 | 路径 |", "|---|---|", "| JSONL | `work/knowledge/高考分析/kp_batches/practical_reading_2016_2024.jsonl` |", "| 本报告 | `work/knowledge/高考分析/kp_batches/practical_reading_2016_2024.md` |", "| 生成脚本 | `scripts/extract_practical_reading_2016_2024_kp_batch.py` |", ""]
    return "\n".join(lines)


def main() -> int:
    rows = [make_record(row) for row in load_nodes()]
    if len(rows) != sum(EXPECTED_COUNTS.values()):
        raise SystemExit(f"expected {sum(EXPECTED_COUNTS.values())} nodes, got {len(rows)}")
    actual = Counter(row["year"] for row in rows)
    if dict(actual) != EXPECTED_COUNTS:
        raise SystemExit(f"unexpected year counts: {dict(actual)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "PRACTICAL-READING-2016-2024", "record_count": len(rows), "year_counts": dict(actual), "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
