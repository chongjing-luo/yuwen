#!/usr/bin/env python3
"""Extract candidate KP evidence for three stable old-paper language tasks."""
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from extract_word_pronunciation_kp_batch import answer_candidate, body, knowledge_evidence

ROOT = Path(__file__).resolve().parents[1]
SLICE_DIR = ROOT / "work/knowledge/exams/workbench"
OUT_DIR = SLICE_DIR / "kp_batches"
OUT_JSONL = OUT_DIR / "core_language_use_2009_2015.jsonl"
OUT_MD = OUT_DIR / "core_language_use_2009_2015.md"
TARGET_TYPES = {
    "orthography": ("现代汉字字形辨析", "辨析字形"),
    "word_usage": ("词语/熟语语境使用辨析", "辨析词语使用"),
    "sentence_grammar": ("病句结构与语意辨析", "辨析病句"),
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_nodes() -> list[dict]:
    nodes: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-SC-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2009 <= row.get("year", 0) <= 2015 and row.get("question_type_l2") in TARGET_TYPES:
                nodes.append(row)
    return sorted(nodes, key=lambda row: (row["question_type_l2"], row["year"]))


def make_record(row: dict) -> dict:
    type_name = row["question_type_l2"]
    point, action = TARGET_TYPES[type_name]
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    answer, method = answer_candidate(analysis)
    evidence, level, subskills = knowledge_evidence(analysis)
    upstream_status = row.get("answer_source_status")
    if upstream_status == "missing":
        status = "candidate_text_present_authority_missing" if answer else ("candidate_source_without_answer_text_authority_missing" if analysis else "missing_analysis_source")
        gate = "source_authority_missing"
    elif answer:
        status = "candidate_answer_present"
        gate = "manual_answer_and_pdf_review"
    elif analysis:
        status = "candidate_source_without_answer_text"
        gate = "answer_source_extraction_required"
    else:
        status = "missing_analysis_source"
        gate = "answer_source_missing"
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "CORE-LANGUAGE-USE-2009-2015",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": type_name,
        "candidate_atomic_exam_point": point,
        "candidate_ability_action": action,
        "candidate_basis": "题型标签、题干任务和解析候选中的考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": answer,
        "answer_candidate_method": method,
        "answer_candidate_status": status,
        "upstream_answer_source_status": upstream_status,
        "source_authority_status": "missing" if upstream_status == "missing" else "unverified_local_provided",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": evidence,
        "ability_level_candidate": level,
        "subskill_candidates": subskills,
        "manual_review_gate": gate,
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "答案/评分独立核验与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["question_type_l2"]].append(row)
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "CORE-LANGUAGE-USE-2009-2015"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 字形、词语、病句小问级知识点候选批次（2009—2015）",
        "",
        "> 本批次按三种题型合并处理。候选答案来自本地解析源，不能视为官方答案或评分标准；没有显式答案标记时保持缺口。",
        "",
        "| 题型 | 年份 | 节点 | 候选答案 | 状态 | 候选考点 | 审核门 |",
        "|---|---:|---|---|---|---|---|",
    ]
    for type_name in sorted(grouped):
        for row in sorted(grouped[type_name], key=lambda item: item["year"]):
            lines.append(f"| `{type_name}` | {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | `{row['answer_candidate'] or 'N/A'}` | `{row['answer_candidate_status']}` | {row['candidate_atomic_exam_point']} | `{row['manual_review_gate']}` |")
    lines += [
        "",
        "## 统计",
        "",
    ]
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines.append(f"- 总节点：{len(rows)}；显式候选答案：{counts.get('candidate_answer_present', 0)}；权威状态缺失但文本有答案：{counts.get('candidate_text_present_authority_missing', 0)}；无答案标记解析源：{counts.get('candidate_source_without_answer_text', 0)}。")
    lines += [
        "- 全部记录保持 `M0 / kp_id=N/A`。",
        "- 2013 年有解析文本但答案权威状态仍为 `missing` 的节点被单独置于 `source_authority_missing`，不得当作已核验答案。",
        "",
        "## 复核规则",
        "",
        "1. 逐页核对题干选项、标记字词和 OCR。",
        "2. 将解析的答案字母、解析理由和评分信息分栏登记。",
        "3. 只有独立来源和教材 KP 双向证据闭合后，才允许升级映射。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/exams/workbench/kp_batches/core_language_use_2009_2015.jsonl` |",
        "| 本报告 | `work/knowledge/exams/workbench/kp_batches/core_language_use_2009_2015.md` |",
        "| 生成脚本 | `scripts/extract_core_language_use_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = [make_record(row) for row in load_nodes()]
    if len(rows) != 21:
        raise SystemExit(f"expected 21 nodes, got {len(rows)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "CORE-LANGUAGE-USE-2009-2015", "record_count": len(rows), "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
