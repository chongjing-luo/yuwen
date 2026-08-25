#!/usr/bin/env python3
"""Repair the single derived JSONL row updated with Q011 image metadata."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "work/knowledge/exams/workbench/GK-NC3-2016-response_nodes_vertical_slice.jsonl"
BAD = '"na_reason": "校准切片仅完成作答节点与分值结构；review_status":'
GOOD = '"na_reason": "校准切片仅完成作答节点与分值结构；", "review_status":'

lines = PATH.read_text(encoding="utf-8").splitlines()
fixed = []
for line in lines:
    if '"response_node_id": "GK-NC3-2016-Q011-TOP"' in line:
        line = line.replace(BAD, GOOD, 1)
    fixed.append(line)
for line in fixed:
    if '"response_node_id": "GK-NC3-2016-Q011-TOP"' in line:
        import json
        json.loads(line)
PATH.write_text("\n".join(fixed) + "\n", encoding="utf-8")
print("repaired", PATH)
