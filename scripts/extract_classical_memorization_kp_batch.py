#!/usr/bin/env python3
"""Extract conservative candidate records for classical memorization items."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from extract_word_pronunciation_kp_batch import body

ROOT = Path(__file__).resolve().parents[1]
SLICE_DIR = ROOT / "work/knowledge/exams/workbench"
OUT_DIR = SLICE_DIR / "kp_batches"
OUT_JSONL = OUT_DIR / "classical_memorization_2009_2015.jsonl"
OUT_MD = OUT_DIR / "classical_memorization_2009_2015.md"
EXPECTED_COUNTS = {2009: 2, 2010: 2, 2011: 2, 2012: 2, 2013: 1, 2014: 1, 2015: 1}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def memorization_evidence(text: str) -> tuple[str, str | None]:
    """Keep only task-specific memorization evidence from mixed segments."""
    if not text:
        return "", None
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = ("默写常见的名句名篇", "记忆性默写", "名句名篇默写", "名篇名句")
    selected = [line for line in lines if any(marker in line for marker in markers)]
    joined = " ".join(selected[:5])
    match = re.search(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined)
    return joined, match.group(1) if match else None


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-SC-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2009 <= row.get("year", 0) <= 2015 and row.get("question_type_l2") == "classical_memorization":
                rows.append(row)
    return sorted(rows, key=lambda row: (row["year"], row["response_node_id"]))


def make_record(row: dict) -> dict:
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    evidence, level = memorization_evidence(analysis)
    upstream_status = row.get("answer_source_status")
    if upstream_status == "missing":
        status = "candidate_source_without_answer_text_authority_missing" if analysis else "missing_analysis_source"
        gate = "source_authority_missing"
    elif analysis:
        status = "fill_in_candidate_source"
        gate = "fill_in_answer_and_scoring_review_required"
    else:
        status = "missing_analysis_source"
        gate = "answer_source_missing"
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "CLASSICAL-MEMORIZATION-2009-2015",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": row.get("question_type_l2"),
        "response_form": "fill_in_classical_memorization",
        "candidate_atomic_exam_point": "名篇名句理解性默写与规范书写",
        "candidate_ability_action": "根据语境/提示回忆并准确书写名句名篇",
        "candidate_basis": "题型标签、题干任务和解析候选中的默写考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None,
        "answer_candidate_method": "fill_in_answer_not_auto_extracted",
        "answer_candidate_status": status,
        "analysis_contains_answer_marker": "【答案】" in analysis or "答案" in analysis,
        "upstream_answer_source_status": upstream_status,
        "source_authority_status": "missing" if upstream_status == "missing" else "unverified_local_provided",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": evidence,
        "ability_level_candidate": level,
        "subskill_candidates": ["语境提示回忆", "字形规范书写"] if analysis else [],
        "manual_review_gate": gate,
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "默写答案/评分独立核验与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "CLASSICAL-MEMORIZATION-2009-2015"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 名篇名句默写小问级知识点候选批次（2009—2015）",
        "",
        "> 本批次只登记默写任务、来源和候选考点，不把解析中的填空答案自动确认为官方答案；所有记录保持 `M0 / kp_id=N/A`。",
        "",
        "| 年份 | 节点 | 解析状态 | 源中有答案标记 | 能力层级候选 | 审核门 |",
        "|---:|---|---|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | `{row['answer_candidate_status']}` | `{str(row['analysis_contains_answer_marker']).lower()}` | `{row['ability_level_candidate'] or 'N/A'}` | `{row['manual_review_gate']}` |")
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；默写解析源：{counts.get('fill_in_candidate_source', 0)}；2013 年权威缺失：{counts.get('candidate_source_without_answer_text_authority_missing', 0)}。",
        "- `analysis_contains_answer_marker` 只表示源文本出现“答案”字样，不表示答案已核验；`answer_candidate` 全部保持空值。",
        "",
        "## 复核规则",
        "",
        "1. 逐页核对题干、篇目、上下句边界、限选数量、分值和 OCR/水印疑点。",
        "2. 独立登记规范答案、易错字、通假字和评分规则；不得把解析示例直接当官方答案。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/exams/workbench/kp_batches/classical_memorization_2009_2015.jsonl` |",
        "| 本报告 | `work/knowledge/exams/workbench/kp_batches/classical_memorization_2009_2015.md` |",
        "| 生成脚本 | `scripts/extract_classical_memorization_kp_batch.py` |",
        "",
    ]
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
    print(json.dumps({"batch": "CLASSICAL-MEMORIZATION-2009-2015", "record_count": len(rows), "year_counts": dict(actual), "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
