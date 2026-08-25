#!/usr/bin/env python3
"""Apply PDF-reviewed derived-prompt corrections for 2008 Q004/Q008-Q010."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "work/knowledge/exams/workbench/GK-SC-2008-response_nodes_vertical_slice.jsonl"
notes = {
    4: "Q004：PDF 第1页视觉回溯确认四组序列；prompt_text_raw 保留 OCR 数字/括号缺损，派生提示规范化。",
    8: "Q008：PDF 第3页视觉回溯确认‘立擢湜为左参议’；prompt_text_raw 保留‘立握得’，派生提示修正。",
    9: "Q009：PDF 第3页视觉回溯确认‘郑濂’、‘湜，字仲持’；prompt_text_raw 保留 OCR 异文，派生提示修正。",
    10: "Q010：PDF 第3页视觉回溯完成四项复核；未对未确定字词作静默改写。",
}
q4_old = "⑥做到自尊、自爱、自强、自律 A. 3 6 4 5 2 B. ③ 5 2 ③ 4 C. 5 ② 6 4 3 D. ⑤③① ② ④ 6"
q4_new = "⑥做到自尊、自爱、自强、自律\n\nA. ③⑥①④⑤②  B. ③⑤①②③④  C. ⑤②①⑥④③  D. ⑤③①②④⑥"
replacements = {
    8: [("立握得", "立擢湜")],
    9: [("郑波全家", "郑濂全家"), ("湜，宇仲持", "湜，字仲持")],
}
rows = []
for line in PATH.read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    q = int(row.get("question_id", -1))
    if q in notes:
        for key in ("prompt_text", "prompt_text_for_extraction", "prompt_excerpt"):
            text = row[key]
            if q == 4:
                if q4_old in text:
                    text = text.replace(q4_old, q4_new, 1)
            else:
                for old, new in replacements.get(q, []):
                    text = text.replace(old, new)
            row[key] = text
        actions = row.setdefault("prompt_cleaning_actions", [])
        if notes[q] not in actions:
            actions.append(notes[q])
        row["source_warnings"] = list(dict.fromkeys(row.get("source_warnings", []) + [notes[q]]))
        row["ocr_status"] = "suspected_ocr_or_watermark_noise"
        row["ocr_note"] = notes[q]
        row["evidence_ids"] = list(dict.fromkeys(row.get("evidence_ids", []) + [
            f"EV-EXAM-GK-SC-2008-Q{q:03d}-PDF-VISUAL-20260809"
        ]))
        row["pdf_visual_review"] = {
            "status": "confirmed",
            "source_pdf": row["source_pdf"],
            "page_index": 0 if q == 4 else 2,
            "printed_page": 1 if q == 4 else 3,
            "note": notes[q],
        }
        row["content_acceptance"] = "conditional_review"
    rows.append(row)
PATH.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
print(json.dumps({"status": "repaired", "questions": [4, 8, 9, 10], "raw_preserved": True}, ensure_ascii=False))
