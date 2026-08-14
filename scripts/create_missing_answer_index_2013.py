#!/usr/bin/env python3
"""Create an explicit, non-fabricated missing-answer index for 2013."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
base = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013"
out = base / "answers/answer_index.jsonl"
rows = []
for q in range(1, 22):
    rows.append({
        "answer_pair_id": f"GK-SC-2013-Q{q:03d}",
        "exam_id": "GK-SC-2013",
        "question_id": q,
        "source_role": "answer_scoring_candidate",
        "source_status": "missing",
        "answer_status": "missing",
        "answer_text": "",
        "analysis_text": None,
        "analysis_status": "not_present_in_source_bundle",
        "answer_anchor": None,
        "answer_section_id": None,
        "source_mineru_md": None,
        "source_pdf": None,
        "answer_bundle_path": "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/answer_bundle.md",
        "evidence_ids": [f"EV-EXAM-GK-SC-2013-Q{q:03d}-ANSWER-SOURCE-MISSING"],
        "review_status": "blocked_missing_source",
    })
out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
print(json.dumps({"status": "created", "path": str(out), "rows": len(rows)}, ensure_ascii=False))
