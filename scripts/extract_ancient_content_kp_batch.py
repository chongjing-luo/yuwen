#!/usr/bin/env python3
"""Extract candidate records for 2009--2015 classical-text content tasks."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from extract_word_pronunciation_kp_batch import answer_candidate, body

ROOT = Path(__file__).resolve().parents[1]
SLICE_DIR = ROOT / "work/knowledge/高考分析"
OUT_DIR = SLICE_DIR / "kp_batches"
OUT_JSONL = OUT_DIR / "ancient_content_2009_2015.jsonl"
OUT_MD = OUT_DIR / "ancient_content_2009_2015.md"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def content_evidence(text: str) -> tuple[str, str | None, list[str]]:
    """Keep only evidence lines that identify the content-summary task.

    Some legacy analysis segments contain adjacent Q8--Q11 commentary.  A
    whole-segment scan can therefore import Q8's ability level into Q11.  The
    task-specific markers below are deliberately narrow and preserve an empty
    evidence field when no such marker is present.
    """
    if not text:
        return "", None, []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = ("筛选文中的信息", "归纳内容要点", "概括中心意思", "内容概括", "信息筛选")
    selected = [line for line in lines if any(marker in line for marker in markers)]
    joined = " ".join(selected[:5])
    match = re.search(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined)
    return joined, (match.group(1) if match else None), []


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-SC-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2009 <= row.get("year", 0) <= 2015 and row.get("question_type_l2") == "ancient_text_content":
                rows.append(row)
    return sorted(rows, key=lambda row: row["year"])


def make_record(row: dict) -> dict:
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    answer, method = answer_candidate(analysis)
    evidence, level, subskills = content_evidence(analysis)
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
        "batch_id": "ANCIENT-CONTENT-2009-2015",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": row.get("question_type_l2"),
        "candidate_atomic_exam_point": "文言文信息筛选、归纳内容要点与概括",
        "candidate_ability_action": "理解文本并筛选信息、归纳内容要点",
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
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "ANCIENT-CONTENT-2009-2015"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 文言文内容概括/信息筛选小问级知识点候选批次（2009—2015）",
        "",
        "> 本批次只登记题型、题干任务与解析候选中的能力/考点线索。解析候选不等同官方答案或评分标准，所有记录保持 `M0 / kp_id=N/A`。",
        "",
        "| 年份 | 节点 | 候选答案 | 状态 | 候选考点 | 能力层级 | 审核门 |",
        "|---:|---|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | `{row['answer_candidate'] or 'N/A'}` | `{row['answer_candidate_status']}` | {row['candidate_atomic_exam_point']} | `{row['ability_level_candidate'] or 'N/A'}` | `{row['manual_review_gate']}` |")
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；解析源存在但无显式答案标记：{counts.get('candidate_source_without_answer_text', 0)}；2013 年权威缺失门禁：{counts.get('candidate_source_without_answer_text_authority_missing', 0)}。",
        "- 2013 年题型已由选择题转为主观概括题；本批次不把解析中的概括示例自动登记为评分答案。",
        "",
        "## 复核规则",
        "",
        "1. 逐页核对文言原文、设问边界、分值和 OCR/水印疑点。",
        "2. 将答案示例、评分点与能力描述分栏登记；没有独立评分材料时保持未核验。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/高考分析/kp_batches/ancient_content_2009_2015.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/ancient_content_2009_2015.md` |",
        "| 生成脚本 | `scripts/extract_ancient_content_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = [make_record(row) for row in load_nodes()]
    if len(rows) != 7:
        raise SystemExit(f"expected 7 nodes, got {len(rows)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "ANCIENT-CONTENT-2009-2015", "record_count": len(rows), "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
