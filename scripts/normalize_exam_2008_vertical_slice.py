#!/usr/bin/env python3
"""Normalize the legacy 2008 calibration nodes to the vertical-slice schema.

The 2008 pilot predates the 2013/2016/2024 response-node schema.  This script
creates a derived, reviewable copy; it never edits the pilot JSONL, the
MinerU output, the source PDF, or question segments.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "work/knowledge/exams/workbench"
PILOT = OUT / "EXAM-2008-SC-response_nodes.jsonl"
TARGET = OUT / "GK-SC-2008-response_nodes_vertical_slice.jsonl"

# The legacy 2008 pilot carried two transcription-level score errors.  These
# overrides are derived from a direct visual check of the question PDF page 5;
# they do not modify the legacy JSONL or any source artifact.
PDF_SCORE_OVERRIDES = {
    16: 4,
    17: 8,
}

OCR_REVIEW_NOTES = {
    6: ["PDF 视觉复核发现选项 C 含疑似 OCR/排版残片（‘那么可以32%的汽油’）；保留候选原文，待独立来源核验。"],
    13: [
        "候选文本含疑似 OCR 异文‘必使仲足以事父母’；PDF 视觉复核提示应与原字形独立核验。",
        "候选文本含疑似 OCR 异文‘屋舍伊然’、‘荡胸生曾云’及作者名异文；不静默改写。",
    ],
    15: ["候选文本含疑似 OCR 异文‘井说说’；PDF 视觉确认印刷为‘并说说’，派生 prompt 已校正，raw 保留。"],
    21: ["题段末尾存在 Markdown/版面标题残片；原始题段保持只读，派生正文不作语义补写。"],
}

PROMPT_REPLACEMENTS = {
    (13, "CHOICE-1"): {
        "必使仲足以事父母": "必使黎民足以事父母",
        "荡胸生曾云": "荡胸生层云",
    },
    (13, "CHOICE-2"): {
        "屋舍伊然": "屋舍俨然",
        "苏武《念奴娇·赤壁怀古》": "苏轼《念奴娇·赤壁怀古》",
    },
    (15, "TOP"): {"井说说": "并说说"},
}


def clean_prompt(question_id: int, subquestion_code: str, prompt: str) -> tuple[str, list[str]]:
    """Return a reviewable extraction prompt while preserving raw_prompt_text."""
    cleaned = prompt
    actions: list[str] = []
    for old, new in PROMPT_REPLACEMENTS.get((question_id, subquestion_code), {}).items():
        if old in cleaned:
            cleaned = cleaned.replace(old, new)
            actions.append(f"PDF独立复核确认并校正：{old}→{new}；prompt_text_raw 保留原始 OCR。")
    # The source segment carries a Markdown heading marker that is not printed
    # in the PDF.  Remove it only from the derived extraction prompt.
    if question_id == 21 and cleaned.startswith("## "):
        cleaned = cleaned[3:]
        actions.append("移除题段首部 Markdown 标题标记；PDF/原始题段保持只读。")
    return cleaned, actions


def frontmatter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    data: dict = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        try:
            data[key.strip()] = json.loads(value)
        except json.JSONDecodeError:
            data[key.strip()] = value.strip('"')
    return data


def main() -> int:
    rows = [json.loads(line) for line in PILOT.read_text(encoding="utf-8").splitlines() if line.strip()]
    normalized = []
    for row in rows:
        segment = ROOT / row["source_question_segment"]
        fm = frontmatter(segment)
        prompt = row.get("prompt_excerpt", "")
        evidence = row.get("evidence_id")
        is_choice = bool(row.get("choice_group"))
        choice_id = f"{row['exam_id']}-Q013-OPTIONAL" if is_choice else None
        question_id = int(row["question_id"])
        score = PDF_SCORE_OVERRIDES.get(question_id, int(row["score"]))
        prompt_clean, correction_actions = clean_prompt(question_id, row["subquestion_code"], prompt)
        cleaning_actions = list(OCR_REVIEW_NOTES.get(question_id, [])) + correction_actions
        normalized.append({
            "response_node_id": row["response_node_id"],
            "exam_id": row["exam_id"],
            "year": 2008,
            "paper_code": "SC",
            "question_id": question_id,
            "subquestion_code": row["subquestion_code"],
            "prompt_text_raw": prompt,
            "prompt_text": prompt_clean,
            "prompt_text_for_extraction": prompt_clean,
            "prompt_excerpt": prompt,
            "prompt_cleaning_actions": cleaning_actions,
            "score": score,
            "score_basis": "pdf_visual_check_page_5" if question_id in PDF_SCORE_OVERRIDES else "legacy_candidate_pending_visual_adjudication",
            "choice_group_id": choice_id,
            "choice_group": is_choice,
            "choice_branch_count": 2 if is_choice else 0,
            "choice_scored_branch_count": 1 if is_choice else 0,
            "source_question_segment": row["source_question_segment"],
            "source_pdf": row["source_pdf"],
            "source_mineru_md": row["source_mineru_md"],
            "source_clean_md": row["source_clean_md"],
            "source_pdf_page_index_start": row["source_pdf_page_index_start"],
            "source_pdf_page_index_end": row["source_pdf_page_index_end"],
            "source_locator_status": row["source_locator_status"],
            "locator_precision_note": "当前仅页级回退定位；source_block_ids/bbox 不视为题级精确框。",
            "source_block_ids": fm.get("source_block_ids", []),
            "segment_clean_sha256": fm.get("segment_clean_sha256"),
            "section_id": fm.get("section_id"),
            "question_type_l1": fm.get("question_type_l1"),
            "question_type_l2": fm.get("question_type_l2"),
            "material_id": fm.get("material_id"),
            "boundary_status": "clean_or_trimmed",
            "ocr_status": "suspected_ocr_or_watermark_noise" if cleaning_actions else "not_reviewed",
            "source_warnings": cleaning_actions,
            "ability_action": row.get("ability_action", "N/A"),
            "four_layer": row.get("four_layer", "N/A"),
            "four_wings": row.get("four_wings", "N/A"),
            "context_type": row.get("context_type", "N/A"),
            "atomic_exam_point": row.get("atomic_exam_point", "N/A"),
            "answer_source_status": row.get("answer_source_status", "candidate_unverified"),
            "evidence_ids": [evidence] if evidence else [],
            "decomposition_status": row.get("decomposition_status", "response_nodes_derived"),
            "kp_id": row.get("kp_id", "N/A"),
            "mapping_level": row.get("mapping_level", "M0"),
            "na_reason": row.get("na_reason", "校准阶段仅拆解作答节点；答案/评分和教材KP双向证据尚未核验。"),
            "review_status": "needs_manual_review",
        })
    TARGET.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in normalized) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(TARGET.relative_to(ROOT)), "node_count": len(normalized), "raw_score_total": sum(r["score"] for r in normalized)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
