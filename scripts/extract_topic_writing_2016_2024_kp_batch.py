#!/usr/bin/env python3
"""Extract conservative candidate records for 2016--2024 writing tasks."""
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
OUT_JSONL = OUT_DIR / "topic_writing_2016_2024.jsonl"
OUT_MD = OUT_DIR / "topic_writing_2016_2024.md"
EXPECTED_COUNTS = {year: 1 for year in range(2016, 2025)}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def writing_evidence(text: str) -> tuple[str, list[str]]:
    if not text:
        return "", []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = ("考查‘写作’", "考查“写作”", "作文", "审题立意", "本题考查学生")
    selected = [line.split("【答案】", 1)[0].strip() for line in lines if any(marker in line for marker in markers)]
    joined = " ".join(selected[:8])
    levels = []
    for match in re.finditer(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined):
        if match.group(1) not in levels:
            levels.append(match.group(1))
    return joined, levels


def action_candidate(prompt: str) -> str:
    text = prompt or ""
    if "以“" in text and "为题" in text:
        return "围绕题目审题立意、构思并完成规范写作"
    if "材料" in text or "漫画" in text or "诗" in text:
        return "理解材料寓意，选择角度立意并组织文章"
    return "审题立意、组织结构并完成书面表达"


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2016 <= row.get("year", 0) <= 2024 and row.get("question_type_l2") == "topic_writing":
                rows.append(row)
    return sorted(rows, key=lambda row: row["year"])


def make_record(row: dict) -> dict:
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    excerpt, levels = writing_evidence(analysis)
    status = "writing_candidate_source" if analysis else "missing_analysis_source"
    gate = "writing_answer_and_scoring_review_required" if analysis else "answer_source_missing"
    upstream_status = row.get("upstream_answer_source_status") or row.get("answer_source_status") or "unknown"
    return {
        "schema_version": "exam-kp-candidate-batch-0.1", "batch_id": "TOPIC-WRITING-2016-2024",
        "exam_node_id": row["response_node_id"], "exam_id": row["exam_id"], "year": row["year"],
        "question_id": row["question_id"], "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"), "question_type_l2": row.get("question_type_l2"),
        "response_form": "extended_writing", "analysis_scope": "top_level_exam_segment_with_possible_unrelated_context",
        "candidate_atomic_exam_point": "材料/命题作文审题立意、构思与规范表达",
        "candidate_ability_action": action_candidate(row.get("prompt_excerpt")),
        "candidate_basis": "题型标签、题干任务和解析候选中的写作考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"), "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"), "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None, "answer_candidate_method": "writing_response_not_auto_extracted",
        "answer_candidate_status": status, "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": upstream_status,
        "source_authority_status": "unverified_local_provided" if upstream_status != "missing" else "missing",
        "score_candidate": row.get("score"), "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": excerpt, "ability_level_candidates": levels,
        "subskill_candidates": ["审题立意", "材料分析", "结构组织", "规范表达"],
        "manual_review_gate": gate, "source_warnings": row.get("source_warnings", []), "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A", "mapping_level": "M0", "review_status": "candidate_only",
        "na_reason": "作文答案/评分独立核验与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = ["---", 'schema_version: "exam-kp-candidate-batch-0.1"', 'batch_id: "TOPIC-WRITING-2016-2024"', 'status: "candidate_only"', 'mapping_status: "M0_only"', "---", "", "# 材料/命题作文小问级知识点候选批次（2016—2024）", "", "> 作文属于长篇自由作答。本批次只登记题干任务、来源和候选写作动作，不生成范文、立意答案或评分结论；所有记录保持 `M0 / kp_id=N/A`。", "", "| 年份 | 节点 | 分值 | 解析状态 | 候选作答动作 | 审核门 |", "|---:|---|---:|---|---|---|"]
    for row in rows:
        lines.append(f"| {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | {row['score_candidate'] or 'N/A'} | `{row['answer_candidate_status']}` | {row['candidate_ability_action']} | `{row['manual_review_gate']}` |")
    lines += ["", "## 复核规则", "", "1. 逐页核对材料、题目、写作要求、字数、文体和分值。", "2. 独立登记材料寓意、可接受立意范围、评分等级和样文来源；不得把网络解析意见当官方评分。", "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。", "", "| 产物 | 路径 |", "|---|---|", "| JSONL | `work/knowledge/exams/workbench/kp_batches/topic_writing_2016_2024.jsonl` |", "| 本报告 | `work/knowledge/exams/workbench/kp_batches/topic_writing_2016_2024.md` |", "| 生成脚本 | `scripts/extract_topic_writing_2016_2024_kp_batch.py` |", ""]
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
    print(json.dumps({"batch": "TOPIC-WRITING-2016-2024", "record_count": len(rows), "year_counts": dict(actual)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
