#!/usr/bin/env python3
"""Extract the first small-question knowledge-point candidate batch.

Scope: the old-Sichuan word-pronunciation top-level items from 2008--2015.
The output distinguishes a real answer excerpt from a mere analysis-segment
presence.  It never changes vertical-slice nodes and never creates a textbook
mapping.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLICE_DIR = ROOT / "work/knowledge/高考分析"
OUT_DIR = SLICE_DIR / "kp_batches"
OUT_JSONL = OUT_DIR / "word_pronunciation_2008_2015.jsonl"
OUT_MD = OUT_DIR / "word_pronunciation_2008_2015.md"
TARGET_YEARS = set(range(2008, 2016))


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def body(path: Path | None) -> str:
    if not path or not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    return text.split("---\n\n", 2)[-1].strip()


def answer_candidate(text: str) -> tuple[str | None, str]:
    if not text:
        return None, "analysis_source_absent"
    # Keep the exact answer token only; no normalization or correctness claim.
    match = re.search(r"(?:^|\n)\s*(?:【答案】|答案\s*[:：])\s*([A-DＡ-Ｄ])", text)
    if not match:
        return None, "analysis_has_no_explicit_answer_marker"
    value = match.group(1).translate(str.maketrans("ＡＢＣＤ", "ABCD"))
    return value, "explicit_answer_marker"


def knowledge_evidence(text: str) -> tuple[str, str | None, list[str]]:
    if not text:
        return "", None, []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    evidence: list[str] = []
    for line in lines:
        if any(marker in line for marker in ("考点", "能力层级", "试题分析", "字音题的考查", "涉及多音字", "形声字")):
            evidence.append(line)
        if len(evidence) >= 5:
            break
    joined = " ".join(evidence)
    level = None
    match = re.search(r"能力层级(?:为|：|:)?\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined)
    if match:
        level = match.group(1)
    subskills = []
    for term in ("多音字", "形声字", "形近字", "同音字", "习惯性误读", "方言字", "统读字", "难读字"):
        if term in text:
            subskills.append(term)
    return joined, level, subskills


def load_target_nodes() -> list[dict]:
    nodes: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-SC-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("year") in TARGET_YEARS and row.get("question_type_l2") == "word_pronunciation":
                nodes.append(row)
    return sorted(nodes, key=lambda row: row["year"])


def make_record(row: dict) -> dict:
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    answer, answer_method = answer_candidate(analysis)
    evidence, level, subskills = knowledge_evidence(analysis)
    upstream_status = row.get("answer_source_status")
    if upstream_status == "missing":
        if answer_method == "explicit_answer_marker":
            status = "candidate_text_present_authority_missing"
        elif analysis:
            status = "candidate_source_without_answer_text_authority_missing"
        else:
            status = "missing_analysis_source"
        gate = "source_authority_missing"
    elif answer_method == "explicit_answer_marker":
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
        "batch_id": "WORD-PRONUNCIATION-2008-2015",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": row.get("question_type_l2"),
        "candidate_atomic_exam_point": "现代汉语普通话常用字字音识记与辨析",
        "candidate_ability_action": "辨析字音并判断选项正误",
        "candidate_basis": "题型标签、题干任务和解析候选中的考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": answer,
        "answer_candidate_method": answer_method,
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


def render(records: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "WORD-PRONUNCIATION-2008-2015"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 字音辨析小问级知识点候选批次（2008—2015）",
        "",
        "> 本批次只把题型和解析中的考点描述整理成候选字段。`candidate_answer_present` 仍是本地解析候选，不是官方答案；没有显式答案标记的解析段不被补写。",
        "",
        "| 年份 | 节点 | 候选答案 | 答案状态 | 候选考点 | 能力层级 | 审核门 |",
        "|---:|---|---|---|---|---|---|",
    ]
    for record in records:
        question_link = f"[[{record['prompt_source']}|题干]]"
        answer = record["answer_candidate"] or "N/A"
        point = record["candidate_atomic_exam_point"]
        lines.append(f"| {record['year']} | `{record['exam_node_id']}` {question_link} | `{answer}` | `{record['answer_candidate_status']}` | {point} | `{record['ability_level_candidate'] or 'N/A'}` | `{record['manual_review_gate']}` |")
    counts: dict[str, int] = {}
    for record in records:
        counts[record["answer_candidate_status"]] = counts.get(record["answer_candidate_status"], 0) + 1
    lines += [
        "",
        "## 批次统计",
        "",
        f"- 总节点：{len(records)}。",
        f"- 显式候选答案（未核验来源）：{counts.get('candidate_answer_present', 0)}；权限缺失但文本有答案：{counts.get('candidate_text_present_authority_missing', 0)}；解析源存在但无答案标记：{counts.get('candidate_source_without_answer_text', 0)}；分析源缺失：{counts.get('missing_analysis_source', 0)}。",
        "- 所有记录保持 `M0 / kp_id=N/A`；`knowledge_evidence_excerpt` 仅为候选证据摘录。",
        "",
        "## 复核顺序",
        "",
        "1. 先逐页回看题干 PDF，确认加点字、音标和 OCR 异文。",
        "2. 再核对解析候选的答案字母与题干选项；没有独立来源时标为 `candidate_unverified`。",
        "3. 将“多音字、形声字、习惯性误读”等子技能作为候选标签，不直接等同教材 KP。",
        "4. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/高考分析/kp_batches/word_pronunciation_2008_2015.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/word_pronunciation_2008_2015.md` |",
        "| 生成脚本 | `scripts/extract_word_pronunciation_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    records = [make_record(row) for row in load_target_nodes()]
    if len(records) != 8:
        raise SystemExit(f"expected 8 word-pronunciation nodes, got {len(records)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(record, ensure_ascii=False) for record in records) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(records), encoding="utf-8")
    counts: dict[str, int] = {}
    for record in records:
        counts[record["answer_candidate_status"]] = counts.get(record["answer_candidate_status"], 0) + 1
    print(json.dumps({"batch": "WORD-PRONUNCIATION-2008-2015", "record_count": len(records), "status_counts": counts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
