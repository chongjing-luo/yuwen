#!/usr/bin/env python3
"""Repair the PDF-reviewed derived boundaries for 2016/2024 Q006.

The blank-paper Q006 segments had already been trimmed, but their ledgers and
top-level indexes still carried the old page/hash metadata.  The analysis
segments also retained the next question/reading section.  This script only
updates derived Markdown/JSONL layers; PDFs, MinerU ``full.md`` and raw text
fields remain unchanged.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Callable

from repair_visual_boundary_contamination import (
    EXTRACT,
    KP,
    ROOT,
    read_frontmatter,
    replace_frontmatter,
    split_markdown,
)


def sha(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def keep_all(block: str) -> bool:
    return True


def keep_2016_analysis(block: str) -> bool:
    """Keep Q006 answer blocks through the final review paragraph on P17."""
    if block.startswith(("P14-", "P15-", "P16-")):
        return True
    if block.startswith("P17-B"):
        try:
            return int(block.split("-B", 1)[1]) <= 20
        except ValueError:
            return False
    return False


def keep_2024_analysis(block: str) -> bool:
    """Keep Q006 analysis through P7-B5; P7-B6 is the next-section heading."""
    if block.startswith(("P5-", "P6-")):
        return True
    if block.startswith("P7-B"):
        try:
            return int(block.split("-B", 1)[1]) <= 5
        except ValueError:
            return False
    return False


def trim_segment(
    path: Path,
    marker: str,
    *,
    keep_block: Callable[[str], bool],
    page_end: int,
    page_index_end: int,
    raw_line_end: int,
    note: str,
) -> tuple[str, dict[str, object], str]:
    text = path.read_text(encoding="utf-8")
    header, links, body = split_markdown(text)
    fm = read_frontmatter(text)
    if marker in body:
        cleaned = body.split(marker, 1)[0].rstrip() + "\n"
    elif fm.get("boundary_status") == "boundary_reviewed_trimmed":
        cleaned = body.rstrip() + "\n"
    else:
        raise ValueError(f"{path}: boundary marker not found")

    blocks = [str(x) for x in (fm.get("source_block_ids", []) or []) if keep_block(str(x))]
    bbox = {
        str(k): v
        for k, v in (fm.get("source_bbox_json", {}) or {}).items()
        if keep_block(str(k))
    }
    header = replace_frontmatter(header, "source_pdf_page_end", page_end)
    header = replace_frontmatter(header, "source_pdf_page_index_end", page_index_end)
    header = replace_frontmatter(header, "source_block_ids", blocks)
    header = replace_frontmatter(header, "source_bbox_json", bbox)
    header = replace_frontmatter(header, "raw_line_end", raw_line_end)
    header = replace_frontmatter(header, "segment_clean_sha256", sha(cleaned))
    header = replace_frontmatter(header, "boundary_status", "boundary_reviewed_trimmed")
    header = replace_frontmatter(header, "boundary_note", note)
    path.write_text(header + "\n" + links + "\n---\n\n" + cleaned, encoding="utf-8")
    result = {
        "path": str(path.relative_to(ROOT)),
        "clean_sha256": sha(cleaned),
        "source_block_count": len(blocks),
        "page_end": page_end,
        "page_index_end": page_index_end,
    }
    return sha(cleaned), result, cleaned.strip()


def update_ledgers(
    exam_id: str,
    question_sha: str,
    analysis_sha: str,
    *,
    question_body: str,
    question_blocks: Callable[[str], bool],
    question_page_end: int,
    question_page_index_end: int,
    question_raw_line_end: int,
    analysis_blocks: Callable[[str], bool],
    analysis_page_end: int,
    analysis_page_index_end: int,
    analysis_raw_line_end: int,
    marker: str,
    note: str,
) -> dict[str, int]:
    counts = {"question": 0, "analysis": 0}
    ledger_dir = EXTRACT / exam_id / "ledger"
    for role, clean_sha, keep_block, page_end, page_index_end, raw_line_end in (
        ("question", question_sha, question_blocks, question_page_end, question_page_index_end, question_raw_line_end),
        ("analysis", analysis_sha, analysis_blocks, analysis_page_end, analysis_page_index_end, analysis_raw_line_end),
    ):
        for filename in (f"questions-{role}.jsonl", "questions.jsonl"):
            path = ledger_dir / filename
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            changed = False
            for row in rows:
                if row.get("canonical_question_id") != f"{exam_id}-Q006" or row.get("source_role") != role:
                    continue
                row["segment_clean_sha256"] = clean_sha
                row["clean_text"] = row.get("clean_text", "").split(marker, 1)[0].rstrip()
                row["source_pdf_page_end"] = page_end
                row["source_pdf_page_index_end"] = page_index_end
                if "printed_page_no_end" in row and role == "question":
                    row["printed_page_no_end"] = page_end
                row["source_block_ids"] = [x for x in row.get("source_block_ids", []) if keep_block(str(x))]
                row["source_bbox_json"] = {
                    k: v for k, v in (row.get("source_bbox_json", {}) or {}).items() if keep_block(str(k))
                }
                row["raw_line_end"] = raw_line_end
                row["boundary_status"] = "boundary_reviewed_trimmed"
                row["boundary_note"] = note
                changed = True
            if changed:
                path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
                counts[role] += 1
    return counts


def update_nodes(
    exam_id: str,
    question_sha: str,
    *,
    question_body: str,
    question_blocks: Callable[[str], bool],
    question_page_index_end: int,
    note: str,
) -> dict[str, int]:
    counts = {"vertical": 0, "top_level": 0}
    vertical = KP / f"{exam_id}-response_nodes_vertical_slice.jsonl"
    rows = [json.loads(line) for line in vertical.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        if row.get("question_id") != 6:
            continue
        row["segment_clean_sha256"] = question_sha
        row["source_pdf_page_index_end"] = question_page_index_end
        if "source_block_ids" in row:
            row["source_block_ids"] = [x for x in row.get("source_block_ids", []) if question_blocks(str(x))]
        row["boundary_status"] = "boundary_reviewed_trimmed"
        row["boundary_note"] = note
        actions = row.setdefault("prompt_cleaning_actions", [])
        if note not in actions:
            actions.append(note)
        counts["vertical"] += 1
    vertical.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    top = KP / "exam_response_nodes_top_level.jsonl"
    rows = [json.loads(line) for line in top.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        if row.get("response_node_id") != f"{exam_id}-Q006-TOP":
            continue
        row["segment_clean_sha256"] = question_sha
        row["source_pdf_page_index_end"] = question_page_index_end
        row["source_block_ids"] = [x for x in row.get("source_block_ids", []) if question_blocks(str(x))]
        row["prompt_excerpt"] = question_body
        row["boundary_status"] = "boundary_reviewed_trimmed"
        row["boundary_note"] = note
        counts["top_level"] += 1
    top.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    return counts


def update_practical_batch(exam_id: str, analysis_sha: str, note: str) -> int:
    path = KP / "kp_batches/practical_reading_2016_2024.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = 0
    for row in rows:
        if not str(row.get("exam_node_id", "")).startswith(f"{exam_id}-Q006"):
            continue
        row["analysis_source_sha256"] = analysis_sha
        warnings = row.setdefault("source_warnings", [])
        if note not in warnings:
            warnings.append(note)
        changed += 1
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    return changed


def update_exam_draft(exam_id: str, old_range: str, new_range: str) -> bool:
    path = KP / f"exam_drafts/{exam_id}.md"
    text = path.read_text(encoding="utf-8")
    needle = f"| {exam_id}-Q006-TOP |"
    lines = text.splitlines()
    changed = False
    for i, line in enumerate(lines):
        if line.startswith(needle) and f"| {old_range} |" in line:
            lines[i] = line.replace(f"| {old_range} |", f"| {new_range} |", 1)
            changed = True
    if changed:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return changed or any(line.startswith(needle) and f"| {new_range} |" in line for line in lines)


def main() -> int:
    results: list[dict[str, object]] = []

    configs = [
        {
            "exam_id": "GK-NC3-2016",
            "marker": "## 五、语言文字运用（20分）",
            "note": "独立 PDF 复核：Q006 正文止于空白卷印刷第11页；第12页‘五、语言文字运用’为下一节标题。解析卷仅保留至 Q006 答案末尾。",
            "q_path": EXTRACT / "GK-NC3-2016/segments/question/Q006.md",
            "a_path": EXTRACT / "GK-NC3-2016/segments/analysis/Q006.md",
            "q_keep": lambda b: not b.startswith("P12-"),
            "a_keep": keep_2016_analysis,
            "q_end": 11,
            "q_idx": 10,
            "q_raw": 247,
            "a_end": 17,
            "a_idx": 16,
            "a_raw": 440,
            "draft_old": "9–12",
            "draft_new": "9–11",
        },
        {
            "exam_id": "GK-NCA-2024",
            "marker": "## （三）文学类文本同读（本题共3小题，15分）",
            "note": "独立 PDF 复核：Q006 正文/解析止于实用类文本第6题；‘（三）文学类文本’及其后内容不属于 Q006。",
            "q_path": EXTRACT / "GK-NCA-2024/segments/question/Q006.md",
            "a_path": EXTRACT / "GK-NCA-2024/segments/analysis/Q006.md",
            "q_keep": lambda b: not b.startswith("P6-"),
            "a_keep": keep_2024_analysis,
            "q_end": 5,
            "q_idx": 4,
            "q_raw": 70,
            "a_end": 7,
            "a_idx": 6,
            "a_raw": 157,
            "draft_old": "4–6",
            "draft_new": "4–5",
        },
    ]

    for cfg in configs:
        q_sha, q_result, q_body = trim_segment(
            cfg["q_path"], cfg["marker"], keep_block=cfg["q_keep"],
            page_end=cfg["q_end"], page_index_end=cfg["q_idx"], raw_line_end=cfg["q_raw"], note=cfg["note"])
        a_sha, a_result, _ = trim_segment(
            cfg["a_path"], cfg["marker"], keep_block=cfg["a_keep"],
            page_end=cfg["a_end"], page_index_end=cfg["a_idx"], raw_line_end=cfg["a_raw"], note=cfg["note"])
        ledgers = update_ledgers(
            cfg["exam_id"], q_sha, a_sha, question_body=q_body,
            question_blocks=cfg["q_keep"], question_page_end=cfg["q_end"], question_page_index_end=cfg["q_idx"], question_raw_line_end=cfg["q_raw"],
            analysis_blocks=cfg["a_keep"], analysis_page_end=cfg["a_end"], analysis_page_index_end=cfg["a_idx"], analysis_raw_line_end=cfg["a_raw"],
            marker=cfg["marker"], note=cfg["note"])
        nodes = update_nodes(cfg["exam_id"], q_sha, question_body=q_body, question_blocks=cfg["q_keep"], question_page_index_end=cfg["q_idx"], note=cfg["note"])
        batch = update_practical_batch(cfg["exam_id"], a_sha, cfg["note"])
        draft = update_exam_draft(cfg["exam_id"], cfg["draft_old"], cfg["draft_new"])
        results.append({"exam_id": cfg["exam_id"], "question": q_result, "analysis": a_result, "ledgers": ledgers, "nodes": nodes, "practical_batch_rows": batch, "exam_draft_updated": draft})

    report = ROOT / "work/knowledge/_meta/validation_reports/exam_q006_boundary_repair.json"
    report.write_text(json.dumps({"status": "repaired_q006_boundaries", "results": results, "raw_preserved": True}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "repaired_q006_boundaries", "results": results, "raw_preserved": True}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
