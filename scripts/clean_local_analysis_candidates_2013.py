#!/usr/bin/env python3
"""Split only explicit question/analysis boundaries in the 2013 local layer.

This is a reversible derivative edit.  It never edits the PDF, MinerU output,
cleaned full卷, answer index, source status, scoring status, or mapping gate.
The five boundaries below are visible text markers in the already-derived
segments; no answer is inferred.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/local_analysis_candidates.jsonl"

# Marker is the first text that is clearly commentary/analysis rather than the
# question body.  The text before it is retained as question_excerpt exactly.
BOUNDARIES = {
    3: "## 做，不考虑别人的意见。",
    10: "【签客】",
    11: "【解析】",
    13: "为修辞手法的鉴赏上面，题干明确了颈联所用修辞手法为对比，",
    21: "只揭露社会阴暗面，愤世嫉俗，发牢骚，导致立意不高，甚至立意不当。",
}


def sha(text: str | None) -> str | None:
    if not text:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> int:
    rows = [json.loads(line) for line in PATH.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = []
    for row in rows:
        qid = int(row["question_id"])
        marker = BOUNDARIES.get(qid)
        if not marker or row.get("candidate_status") != "candidate_mixed_analysis":
            continue
        original = row.get("analysis_excerpt") or ""
        pos = original.find(marker)
        if pos <= 0:
            raise SystemExit(f"Q{qid:03d}: explicit boundary not found: {marker!r}")
        question_excerpt = original[:pos].rstrip()
        analysis_excerpt = original[pos:].lstrip()
        row["question_excerpt"] = question_excerpt
        row["question_excerpt_sha256"] = sha(question_excerpt)
        row["analysis_excerpt"] = analysis_excerpt
        row["analysis_excerpt_sha256"] = sha(analysis_excerpt)
        row["manual_boundary"] = {
            "status": "split_on_explicit_source_marker",
            "marker": marker,
            "original_mixed_excerpt_sha256": sha(original),
        }
        row.setdefault("notes", []).extend([
            "manual_boundary_split",
            "题干与解析按源段中明确可见标记分离；未推断答案。",
        ])
        changed.append(qid)
    if changed != [3, 10, 11, 13, 21]:
        raise SystemExit(f"unexpected changed questions: {changed}")
    PATH.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    print(json.dumps({"updated": changed, "output": str(PATH.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
