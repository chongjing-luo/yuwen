#!/usr/bin/env python3
"""Record the PDF-verified correction for 2024 Q004 option B.

The raw OCR prompt is intentionally retained.  Only the derived extraction
prompt is repaired, with the PDF page/bbox recorded as review evidence.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "work/knowledge/高考分析/GK-NCA-2024-response_nodes_vertical_slice.jsonl"
CORRECTION = (
    "B. 中国古建筑大木构架剖面示意图展示了几种不同位置、不同尺寸的柱，"
    "这些柱子中，立于地面的立柱比较容易发生糟朽残损的情况。"
)
NOTE = (
    "Q004 选项 B：原始 MinerU/OCR 段缺失；2026-08-09 对原始 PDF 第4页视觉回溯确认完整文字，"
    "仅修复 prompt_text/prompt_text_for_extraction/prompt_excerpt，prompt_text_raw 保持原样。"
)

rows = []
for line in PATH.read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    if row.get("response_node_id") == "GK-NCA-2024-Q004-TOP":
        raw = row["prompt_text_raw"]
        # Keep the raw OCR string immutable; replace only the missing option
        # span in the three derived prompt fields.
        old = "比较容易发生糟朽残损的情况。"
        repaired = CORRECTION
        for key in ("prompt_text", "prompt_text_for_extraction", "prompt_excerpt"):
            text = row[key]
            if old in text:
                text = text.replace(old, repaired, 1)
            elif "\nC." in text and "B." in text:
                # Defensive path for a future OCR variant with no orphan line.
                before, after = text.split("\nC.", 1)
                text = before.rstrip() + "\n" + repaired + "\nC." + after
            row[key] = text
        actions = row.setdefault("prompt_cleaning_actions", [])
        if NOTE not in actions:
            actions.append(NOTE)
        row["source_warnings"] = list(dict.fromkeys(row.get("source_warnings", []) + [NOTE]))
        row["ocr_status"] = "suspected_ocr_or_watermark_noise"
        row["ocr_note"] = NOTE
        row["evidence_ids"] = list(dict.fromkeys(row.get("evidence_ids", []) + [
            "EV-EXAM-GK-NCA-2024-Q004-TOP-PDF-VISUAL-20260809"
        ]))
        row["pdf_visual_review"] = {
            "status": "confirmed",
            "source_pdf": row["source_pdf"],
            "page_index": 3,
            "printed_page": 4,
            "bbox": [50, 581, 538, 712],
            "note": "选项 B 完整文字由 PDF 视觉确认；不据此改写 prompt_text_raw。",
        }
        row["content_acceptance"] = "conditional_review"
    rows.append(row)
PATH.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
print(json.dumps({"status": "repaired", "question": "GK-NCA-2024-Q004", "raw_preserved": True}, ensure_ascii=False))
