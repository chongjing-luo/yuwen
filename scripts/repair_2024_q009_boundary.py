#!/usr/bin/env python3
"""Trim the PDF-reviewed next-section contamination from 2024 Q009.

Only derived segment/index layers are changed.  The original PDF, MinerU
``full.md`` and each vertical node's ``prompt_text_raw`` remain untouched.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from repair_visual_boundary_contamination import (
    ROOT,
    KP,
    EXTRACT,
    read_frontmatter,
    replace_frontmatter,
    split_markdown,
)

EXAM_ID = "GK-NCA-2024"
SEGMENT_MARKER = "## 二、古代诗文阅读（34分）"
NOTE = "独立 PDF 复核：Q009 正文/解析止于文学类文本第9题；‘二、古代诗文阅读’及其后内容归入 Q010 起，不并入 Q009。"


def sha(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def trim_segment(path: Path, *, trim_page: bool) -> tuple[str, dict]:
    text = path.read_text(encoding="utf-8")
    header, links, body = split_markdown(text)
    if SEGMENT_MARKER in body:
        cleaned = body.split(SEGMENT_MARKER, 1)[0].rstrip() + "\n"
    elif read_frontmatter(text).get("boundary_status") == "boundary_reviewed_trimmed":
        cleaned = body.rstrip() + "\n"
    else:
        raise ValueError(f"{path}: boundary marker not found")
    fm = read_frontmatter(text)
    blocks = list(fm.get("source_block_ids", []) or [])
    if trim_page:
        blocks = [x for x in blocks if not str(x).startswith("P7-")]
        bbox = {k: v for k, v in (fm.get("source_bbox_json", {}) or {}).items() if not str(k).startswith("P7-")}
        header = replace_frontmatter(header, "source_pdf_page_end", 6)
        header = replace_frontmatter(header, "source_pdf_page_index_end", 5)
        header = replace_frontmatter(header, "printed_page_no_end", 6)
        header = replace_frontmatter(header, "raw_line_end", 130)
        header = replace_frontmatter(header, "source_block_ids", blocks)
        header = replace_frontmatter(header, "source_bbox_json", bbox)
    header = replace_frontmatter(header, "segment_clean_sha256", sha(cleaned))
    header = replace_frontmatter(header, "boundary_status", "boundary_reviewed_trimmed")
    header = replace_frontmatter(header, "boundary_note", NOTE)
    path.write_text(header + "\n" + links + "\n---\n\n" + cleaned, encoding="utf-8")
    return sha(cleaned), {"path": str(path.relative_to(ROOT)), "clean_sha256": sha(cleaned), "blocks": blocks}


def update_ledger(role: str, clean_sha: str, *, trim_page: bool) -> int:
    changed = 0
    for filename in (f"questions-{role}.jsonl", "questions.jsonl"):
        path = EXTRACT / EXAM_ID / "ledger" / filename
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        file_changed = 0
        for row in rows:
            if row.get("canonical_question_id") != f"{EXAM_ID}-Q009" or row.get("source_role") != role:
                continue
            row["segment_clean_sha256"] = clean_sha
            row["clean_text"] = row.get("clean_text", "").split(SEGMENT_MARKER, 1)[0].rstrip()
            if trim_page:
                row["source_pdf_page_end"] = 6
                row["source_pdf_page_index_end"] = 5
                row["printed_page_no_end"] = 6
                row["source_block_ids"] = [x for x in row.get("source_block_ids", []) if not str(x).startswith("P7-")]
                row["source_bbox_json"] = {k: v for k, v in (row.get("source_bbox_json", {}) or {}).items() if not str(k).startswith("P7-")}
            row["boundary_status"] = "boundary_reviewed_trimmed"
            row["boundary_note"] = NOTE
            file_changed += 1
        path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
        changed += file_changed
    return changed


def update_node_files(question_sha: str, analysis_sha: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    question_segment = EXTRACT / EXAM_ID / "segments/question/Q009.md"
    question_body = split_markdown(question_segment.read_text(encoding="utf-8"))[2].strip()
    vertical = KP / f"{EXAM_ID}-response_nodes_vertical_slice.jsonl"
    rows = [json.loads(line) for line in vertical.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = 0
    for row in rows:
        if row.get("response_node_id") != f"{EXAM_ID}-Q009-TOP":
            continue
        row["segment_clean_sha256"] = question_sha
        row["source_pdf_page_index_end"] = 5
        row["source_block_ids"] = [x for x in row.get("source_block_ids", []) if not str(x).startswith("P7-")]
        row["prompt_excerpt"] = question_body
        row["boundary_status"] = "boundary_reviewed_trimmed"
        row["boundary_note"] = NOTE
        row.setdefault("prompt_cleaning_actions", []).append(NOTE)
        row["prompt_cleaning_actions"] = list(dict.fromkeys(row["prompt_cleaning_actions"]))
        changed += 1
    vertical.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    counts["vertical"] = changed

    top = KP / "exam_response_nodes_top_level.jsonl"
    rows = [json.loads(line) for line in top.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = 0
    for row in rows:
        if row.get("response_node_id") != f"{EXAM_ID}-Q009-TOP":
            continue
        row["segment_clean_sha256"] = question_sha
        row["source_pdf_page_index_end"] = 5
        row["source_block_ids"] = [x for x in row.get("source_block_ids", []) if not str(x).startswith("P7-")]
        row["prompt_excerpt"] = question_body
        row["boundary_status"] = "boundary_reviewed_trimmed"
        row["boundary_note"] = NOTE
        changed += 1
    top.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    counts["top_level"] = changed

    batch = KP / "kp_batches/literary_reading_2016_2024.jsonl"
    rows = [json.loads(line) for line in batch.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = 0
    for row in rows:
        if row.get("exam_node_id") != f"{EXAM_ID}-Q009-TOP":
            continue
        row["analysis_source_sha256"] = analysis_sha
        row["source_warnings"] = list(dict.fromkeys(row.get("source_warnings", []) + [NOTE]))
        changed += 1
    batch.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    counts["literary_batch"] = changed
    return counts


def update_exam_draft() -> bool:
    path = KP / "exam_drafts/GK-NCA-2024.md"
    text = path.read_text(encoding="utf-8")
    old = "| GK-NCA-2024-Q009-TOP | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q009.md|Q009]] | 一 | `literary_reading` | 6–7 | MAT-2024-SC-03 | 0 | 分析鉴赏文学类文本 | `M0 / N/A` |"
    new = old.replace("| 6–7 |", "| 6–6 |")
    if old in text:
        path.write_text(text.replace(old, new, 1), encoding="utf-8")
        return True
    return "| GK-NCA-2024-Q009-TOP |" in text and "| 6–6 |" in text


def main() -> int:
    q_path = EXTRACT / EXAM_ID / "segments/question/Q009.md"
    a_path = EXTRACT / EXAM_ID / "segments/analysis/Q009.md"
    q_sha, q_result = trim_segment(q_path, trim_page=True)
    a_sha, a_result = trim_segment(a_path, trim_page=False)
    ledger_q = update_ledger("question", q_sha, trim_page=True)
    ledger_a = update_ledger("analysis", a_sha, trim_page=False)
    counts = update_node_files(q_sha, a_sha)
    draft = update_exam_draft()
    result = {
        "status": "repaired_2024_q009_boundary",
        "question": q_result,
        "analysis": a_result,
        "ledger_question_rows": ledger_q,
        "ledger_analysis_rows": ledger_a,
        "updated_nodes": counts,
        "updated_exam_draft": draft,
        "raw_preserved": True,
    }
    report = ROOT / "work/knowledge/_meta/validation_reports/exam_2024_q009_boundary_repair.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
