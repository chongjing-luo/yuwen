#!/usr/bin/env python3
"""Propagate the explicit missing-answer status into 2013 response nodes."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "work/knowledge/exams/workbench/GK-SC-2013-response_nodes_vertical_slice.jsonl"
note = (
    "2013 四川卷当前没有可核验答案/评分源；中国教育在线答案链接在来源登记中为 404。"
    "结构切片通过不等于答案完成，保持 M0/KP_ID=N/A。"
)
rows = []
for line in path.read_text(encoding="utf-8").splitlines():
    row = json.loads(line)
    row["answer_source_status"] = "missing"
    row["evidence_ids"] = list(dict.fromkeys(row.get("evidence_ids", []) + [
        f"EV-EXAM-GK-SC-2013-Q{int(row['question_id']):03d}-ANSWER-SOURCE-MISSING"
    ]))
    row["source_warnings"] = list(dict.fromkeys(row.get("source_warnings", []) + [note]))
    row["review_status"] = "needs_manual_review"
    row["content_acceptance"] = "conditional_review"
    rows.append(row)
path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
print(json.dumps({"status": "marked_missing", "exam_id": "GK-SC-2013", "nodes": len(rows)}, ensure_ascii=False))
