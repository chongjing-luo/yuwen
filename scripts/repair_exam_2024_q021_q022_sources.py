#!/usr/bin/env python3
"""Restore the located 2024 Q021/Q022 candidate-analysis sources.

The first pass created placeholder analysis segments for Q021/Q022 even
though the MinerU content list contains the complete local analysis text.
This repair only rewrites derived Markdown/JSONL/index layers.  The source
PDFs, MinerU ``full.md`` files and their content lists are read-only.

The recovered analysis remains a local, unverified candidate source.  It is
never promoted to an official answer or scoring artifact and all mappings
stay ``M0 / kp_id=N/A``.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

from repair_visual_boundary_contamination import (
    EXTRACT,
    KP,
    ROOT,
    read_frontmatter,
    replace_frontmatter,
    split_markdown,
)


EXAM_ID = "GK-NCA-2024"
EXAM_ROOT = EXTRACT / EXAM_ID
QUESTION_CLEAN = EXAM_ROOT / "clean_md/question.md"
ANALYSIS_CLEAN = EXAM_ROOT / "clean_md/analysis.md"
QUESTION_CONTENT = ROOT / (
    "Data/2008-2024·（四川）语文高考真题/mineru_result/"
    "2024年高考语文试卷（全国甲卷）（空白卷）/"
    "639eab33-30b9-46f3-bdab-7d8b7db39758_content_list_v2.json"
)
ANALYSIS_CONTENT = ROOT / (
    "Data/2008-2024·（四川）语文高考真题/mineru_result/"
    "2024年高考语文试卷（全国甲卷）（解析卷）/"
    "2e0e6001-e4c3-47de-b928-c98e388189c9_content_list_v2.json"
)
ANALYSIS_RAW = ROOT / (
    "Data/2008-2024·（四川）语文高考真题/mineru_result/"
    "2024年高考语文试卷（全国甲卷）（解析卷）/full.md"
)

NOTE_Q21 = (
    "独立 PDF/MinerU 内容列表复核：Q021 题干止于第9页正文；"
    "‘## 四、作文（60分）’是 Q022 起始标题，已从 Q021 派生正文截断。"
)
NOTE_ANALYSIS = (
    "独立 PDF/MinerU 内容列表复核：恢复解析卷第17—20页的 Q021/Q022 "
    "本地解析候选；第21页仅为推广广告，未纳入。该内容不是官方答案或评分标准。"
)


def sha(text: str) -> str:
    return hashlib.sha256(text.strip().encode("utf-8")).hexdigest()


def clean_body(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    # Both clean_md files have a metadata/link preamble followed by the body.
    return text.split("\n> 清洗副本。", 1)[-1].split("\n\n", 1)[-1]


def extract_between(body: str, start: str, end: str | None = None) -> str:
    pos = body.find(start)
    if pos < 0:
        raise ValueError(f"missing source marker: {start}")
    out = body[pos:]
    if end is not None:
        stop = out.find(end)
        if stop < 0:
            raise ValueError(f"missing end marker: {end}")
        out = out[:stop]
    return out.strip() + "\n"


def content_blocks(path: Path, selections: dict[int, Iterable[int]]) -> tuple[list[str], dict[str, object]]:
    pages = json.loads(path.read_text(encoding="utf-8"))
    blocks: list[str] = []
    bbox: dict[str, object] = {}
    for page_index, indices in selections.items():
        page = pages[page_index]
        for index in indices:
            item = page[index - 1]
            block_id = f"P{page_index + 1}-B{index}"
            blocks.append(block_id)
            if "bbox" in item:
                bbox[block_id] = item["bbox"]
    return blocks, bbox


def rewrite_segment(path: Path, body: str, *, updates: dict[str, object]) -> str:
    old = path.read_text(encoding="utf-8")
    header, links, _ = split_markdown(old)
    for key, value in updates.items():
        header = replace_frontmatter(header, key, value)
    header = replace_frontmatter(header, "segment_clean_sha256", sha(body))
    path.write_text(header + "\n" + links + "\n---\n\n" + body, encoding="utf-8")
    return sha(body)


def update_ledger_rows(
    role: str,
    qid: int,
    *,
    clean_sha: str,
    raw_text: str | None,
    raw_hash: str | None,
    body: str,
    page_start: int,
    page_end: int,
    page_index_start: int,
    page_index_end: int,
    blocks: list[str],
    bbox: dict[str, object],
    raw_line_start: int,
    raw_line_end: int,
    note: str,
    boundary_status: str,
) -> int:
    changed = 0
    for filename in (f"questions-{role}.jsonl", "questions.jsonl"):
        path = EXAM_ROOT / "ledger" / filename
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        file_changed = False
        for row in rows:
            if row.get("canonical_question_id") != f"{EXAM_ID}-Q{qid:03d}" or row.get("source_role") != role:
                continue
            row["source_pdf_page_start"] = page_start
            row["source_pdf_page_end"] = page_end
            row["source_pdf_page_index_start"] = page_index_start
            row["source_pdf_page_index_end"] = page_index_end
            row["source_block_ids"] = blocks
            row["source_bbox_json"] = bbox
            row["source_locator_status"] = "page_level_fallback"
            row["segment_clean_sha256"] = clean_sha
            row["source_clean_md"] = row.get("source_clean_md")
            row["raw_line_start"] = raw_line_start
            row["raw_line_end"] = raw_line_end
            row["boundary_status"] = boundary_status
            row["boundary_note"] = note
            row["clean_text"] = body.strip()
            if raw_text is not None:
                row["raw_text"] = raw_text
            if raw_hash is not None:
                row["raw_segment_sha256"] = raw_hash
            if role == "analysis":
                # The content list now gives a stable candidate segment.
                row["segmentation_status"] = "pilot_segmented"
                row["type_confidence"] = 0.95
                row["review_status"] = "needs_manual_review"
            file_changed = True
        if file_changed:
            path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
            changed += 1
    return changed


def update_nodes(
    q21_sha: str,
    q22_sha: str,
    a21_sha: str,
    a22_sha: str,
    q21_blocks: list[str],
    q22_blocks: list[str],
    note: str,
) -> dict[str, int]:
    counts = {"vertical": 0, "top_level": 0, "batches": 0}
    vertical_path = KP / f"{EXAM_ID}-response_nodes_vertical_slice.jsonl"
    rows = [json.loads(line) for line in vertical_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        qid = int(row.get("question_id", -1))
        if qid not in (21, 22):
            continue
        row["segment_clean_sha256"] = q21_sha if qid == 21 else q22_sha
        row["source_block_ids"] = q21_blocks if qid == 21 else q22_blocks
        # Q021's derived prompt is now trimmed; Q022 was already bounded.
        if qid == 21:
            row["boundary_status"] = "boundary_reviewed_trimmed"
            row["boundary_note"] = NOTE_Q21
            row["prompt_cleaning_actions"] = list(dict.fromkeys(
                row.get("prompt_cleaning_actions", []) + [NOTE_Q21]
            ))
            row["source_warnings"] = [
                x for x in row.get("source_warnings", [])
                if "没有可定位题文/答案源" not in str(x)
            ]
        # The recovered analysis is a candidate source, not an official key.
        row["answer_source_status"] = "candidate_unverified"
        row["review_status"] = "needs_manual_review"
        row["content_acceptance"] = "conditional_review"
        counts["vertical"] += 1
    vertical_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    top_path = KP / "exam_response_nodes_top_level.jsonl"
    rows = [json.loads(line) for line in top_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    for row in rows:
        rid = row.get("response_node_id")
        if rid == f"{EXAM_ID}-Q021-TOP":
            row["segment_clean_sha256"] = q21_sha
            row["source_block_ids"] = q21_blocks
            row["prompt_excerpt"] = extract_between(clean_body(QUESTION_CLEAN), "21.下面", "\n## 四、作文").strip()
            row["review_status"] = "needs_manual_review"
            counts["top_level"] += 1
        elif rid == f"{EXAM_ID}-Q022-TOP":
            row["segment_clean_sha256"] = q22_sha
            row["source_block_ids"] = q22_blocks
            row["prompt_excerpt"] = extract_between(clean_body(QUESTION_CLEAN), "22.阅读", None).split("\n资料提供形式", 1)[0].strip()
            row["review_status"] = "needs_manual_review"
            counts["top_level"] += 1
    top_path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    for batch_name in ("language_application_2021_2024.jsonl", "topic_writing_2016_2024.jsonl"):
        path = KP / "kp_batches" / batch_name
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        changed = False
        for row in rows:
            rid = str(row.get("exam_node_id", ""))
            if rid == f"{EXAM_ID}-Q021-TOP" or rid == f"{EXAM_ID}-Q022-TOP":
                qid = int(rid.split("-Q", 1)[1].split("-", 1)[0])
                row["analysis_source_sha256"] = a21_sha if qid == 21 else a22_sha
                row["source_warnings"] = [
                    x for x in row.get("source_warnings", [])
                    if "没有可定位题文/答案源" not in str(x)
                ]
                if NOTE_ANALYSIS not in row["source_warnings"]:
                    row["source_warnings"].append(NOTE_ANALYSIS)
                changed = True
        if changed:
            path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
            counts["batches"] += 1
    return counts


def main() -> int:
    q_body_all = clean_body(QUESTION_CLEAN)
    a_body_all = clean_body(ANALYSIS_CLEAN)
    q21_body = extract_between(q_body_all, "21.下面", "\n## 四、作文（60分）")
    q22_body = extract_between(q_body_all, "22.阅读", None).split("\n资料提供形式", 1)[0].strip() + "\n"
    a21_body = extract_between(a_body_all, "21. 下面", "\n## 四、作文（60分）")
    a22_body = extract_between(a_body_all, "22. 阅读", None)
    if "\n资料提供形式" in a22_body:
        a22_body = a22_body.split("\n资料提供形式", 1)[0].rstrip() + "\n"

    # The preserved raw span includes the printed next-section heading on the
    # same page; the derived body is trimmed before that heading.
    q21_blocks, q21_bbox = content_blocks(QUESTION_CONTENT, {8: range(7, 10)})
    q22_blocks, q22_bbox = content_blocks(QUESTION_CONTENT, {8: range(10, 12), 9: range(1, 4)})
    a21_blocks, a21_bbox = content_blocks(ANALYSIS_CONTENT, {16: range(10, 17), 17: range(1, 9)})
    a22_blocks, a22_bbox = content_blocks(ANALYSIS_CONTENT, {17: range(9, 18), 18: range(2, 13), 19: range(2, 7)})

    raw_lines = ANALYSIS_RAW.read_text(encoding="utf-8").splitlines()
    a21_raw = "\n".join(raw_lines[443:470])
    a22_raw = "\n".join(raw_lines[471:521])
    q_raw_lines = (ROOT / (
        "Data/2008-2024·（四川）语文高考真题/mineru_result/"
        "2024年高考语文试卷（全国甲卷）（空白卷）/full.md"
    )).read_text(encoding="utf-8").splitlines()
    q21_raw = "\n".join(q_raw_lines[202:207])
    q22_raw = "\n".join(q_raw_lines[208:217])

    q21_path = EXAM_ROOT / "segments/question/Q021.md"
    q22_path = EXAM_ROOT / "segments/question/Q022.md"
    a21_path = EXAM_ROOT / "segments/analysis/Q021.md"
    a22_path = EXAM_ROOT / "segments/analysis/Q022.md"
    q21_sha = rewrite_segment(q21_path, q21_body, updates={
        "source_pdf_page_end": 9, "source_pdf_page_index_end": 8,
        "source_block_ids": q21_blocks, "source_bbox_json": q21_bbox,
        "raw_segment_sha256": sha(q21_raw), "raw_line_end": 208,
        "boundary_status": "boundary_reviewed_trimmed",
        "boundary_note": NOTE_Q21,
    })
    q22_sha = rewrite_segment(q22_path, q22_body, updates={
        "source_pdf_page_start": 9, "source_pdf_page_end": 10,
        "source_pdf_page_index_start": 8, "source_pdf_page_index_end": 9,
        "source_block_ids": q22_blocks, "source_bbox_json": q22_bbox,
        "raw_line_start": 209, "raw_line_end": 218,
        "boundary_status": "boundary_reviewed",
        "boundary_note": "独立 PDF/MinerU 内容列表复核：Q022 题干止于空白卷第10页要求末尾，未纳入解析卷广告内容。",
    })
    a21_sha = rewrite_segment(a21_path, a21_body, updates={
        "source_pdf_page_start": 17, "source_pdf_page_end": 18,
        "source_pdf_page_index_start": 16, "source_pdf_page_index_end": 17,
        "printed_page_no_start": 17, "printed_page_no_end": 18,
        "source_block_ids": a21_blocks, "source_bbox_json": a21_bbox,
        "source_locator_status": "page_level_fallback", "segment_clean_sha256": sha(a21_body),
        "raw_segment_sha256": sha(a21_raw), "cleaning_status": "pilot_cleaned",
        "segmentation_status": "pilot_segmented", "type_confidence": 0.95,
        "review_status": "needs_manual_review", "raw_line_start": 444,
        "raw_line_end": 471, "boundary_status": "boundary_reviewed",
        "boundary_note": NOTE_ANALYSIS,
    })
    a22_sha = rewrite_segment(a22_path, a22_body, updates={
        "source_pdf_page_start": 18, "source_pdf_page_end": 20,
        "source_pdf_page_index_start": 17, "source_pdf_page_index_end": 19,
        "printed_page_no_start": 18, "printed_page_no_end": 20,
        "source_block_ids": a22_blocks, "source_bbox_json": a22_bbox,
        "source_locator_status": "page_level_fallback", "segment_clean_sha256": sha(a22_body),
        "raw_segment_sha256": sha(a22_raw), "cleaning_status": "pilot_cleaned",
        "segmentation_status": "pilot_segmented", "type_confidence": 0.95,
        "review_status": "needs_manual_review", "raw_line_start": 472,
        "raw_line_end": 521, "boundary_status": "boundary_reviewed",
        "boundary_note": NOTE_ANALYSIS,
    })

    ledger_counts = {
        "q21_question": update_ledger_rows("question", 21, clean_sha=q21_sha,
            raw_text=q21_raw, raw_hash=sha(q21_raw), body=q21_body, page_start=9,
            page_end=9, page_index_start=8, page_index_end=8, blocks=q21_blocks,
            bbox=q21_bbox, raw_line_start=203, raw_line_end=208, note=NOTE_Q21,
            boundary_status="boundary_reviewed_trimmed"),
        "q22_question": update_ledger_rows("question", 22, clean_sha=q22_sha,
            raw_text=q22_raw, raw_hash=sha(q22_raw), body=q22_body, page_start=9,
            page_end=10, page_index_start=8, page_index_end=9, blocks=q22_blocks,
            bbox=q22_bbox, raw_line_start=209, raw_line_end=218,
            note="独立 PDF/MinerU 内容列表复核：Q022 题干止于空白卷第10页要求末尾，未纳入解析卷广告内容。",
            boundary_status="boundary_reviewed"),
        "q21_analysis": update_ledger_rows("analysis", 21, clean_sha=a21_sha,
            raw_text=a21_raw, raw_hash=sha(a21_raw), body=a21_body, page_start=17,
            page_end=18, page_index_start=16, page_index_end=17, blocks=a21_blocks,
            bbox=a21_bbox, raw_line_start=444, raw_line_end=471,
            note=NOTE_ANALYSIS, boundary_status="boundary_reviewed"),
        "q22_analysis": update_ledger_rows("analysis", 22, clean_sha=a22_sha,
            raw_text=a22_raw, raw_hash=sha(a22_raw), body=a22_body, page_start=18,
            page_end=20, page_index_start=17, page_index_end=19, blocks=a22_blocks,
            bbox=a22_bbox, raw_line_start=472, raw_line_end=521,
            note=NOTE_ANALYSIS, boundary_status="boundary_reviewed"),
    }

    nodes = update_nodes(q21_sha, q22_sha, a21_sha, a22_sha, q21_blocks, q22_blocks, NOTE_ANALYSIS)
    report = {
        "status": "repaired_2024_q021_q022_sources",
        "question": {"Q021": {"sha256": q21_sha, "blocks": q21_blocks},
                     "Q022": {"sha256": q22_sha, "blocks": q22_blocks}},
        "analysis": {"Q021": {"sha256": a21_sha, "blocks": a21_blocks},
                     "Q022": {"sha256": a22_sha, "blocks": a22_blocks}},
        "ledger_rows_updated": ledger_counts,
        "nodes_updated": nodes,
        "raw_sources_preserved": True,
        "answer_authority": "candidate_unverified_local_analysis_only",
        "mapping_status": "M0_only",
    }
    out = ROOT / "work/knowledge/_meta/validation_reports/exam_2024_q021_q022_source_repair.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
