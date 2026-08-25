#!/usr/bin/env python3
"""Split only explicit numbered answer groups in the 2023 local layer.

The source analysis segments sometimes place a shared answer block in the
last question of a group (for example Q1--Q3 in Q003).  This derivative
re-presents those visible numbered payloads at question level, retaining the
group source and boundary hash.  It never infers an answer from prose and
does not modify the generic local layer or the main answer index.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM_ID = "GK-NCA-2023"
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract" / EXAM_ID
INPUT = BASE / "answers/local_analysis_candidates.jsonl"
OUT = BASE / "answers/local_analysis_group_candidates.jsonl"
REPORT = ROOT / "work/knowledge/exams/workbench/EXAM-LOCAL-GROUP-CANDIDATES-2023.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_local_group_candidates_GK-NCA-2023_20260809.json"

GROUPS = {
    3: [1, 2, 3],
    6: [4, 5, 6],
    9: [7, 8, 9],
    15: [14, 15],
    21: [17, 18, 19, 20, 21],
}


def sha(text: str | None) -> str | None:
    return hashlib.sha256(text.encode("utf-8")).hexdigest() if text else None


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def split_numbered(text: str, qids: list[int]) -> dict[int, str]:
    matches: list[tuple[int, int, int]] = []
    for qid in qids:
        found = re.search(rf"(?<!\d){qid}\s*[.．]\s*", text)
        if not found:
            raise RuntimeError(f"explicit answer number Q{qid} not found in {text[:160]!r}")
        matches.append((qid, found.start(), found.end()))
    matches.sort(key=lambda item: item[1])
    result: dict[int, str] = {}
    for idx, (qid, start, end) in enumerate(matches):
        stop = matches[idx + 1][1] if idx + 1 < len(matches) else len(text)
        payload = text[end:stop].strip()
        if not payload:
            raise RuntimeError(f"empty explicit payload for Q{qid}")
        result[qid] = payload
    return result


def bounded_group_text(qid: int, text: str) -> tuple[str, str | None]:
    if qid == 6:
        marker = "【解析】"
        pos = text.find(marker)
        return (text[:pos].rstrip(), marker) if pos >= 0 else (text, None)
    if qid == 9:
        marker = "\n\n本题考查"
        pos = text.find(marker)
        return (text[:pos].rstrip(), marker) if pos >= 0 else (text, None)
    return text.strip(), None


def main() -> int:
    if not INPUT.exists():
        raise SystemExit(f"missing local candidate layer: {INPUT}")
    source_rows = {int(row["question_id"]): row for row in load(INPUT)}
    if sorted(source_rows) != list(range(1, 23)):
        raise SystemExit(f"local layer coverage mismatch: {sorted(source_rows)}")
    derived: dict[int, dict] = {}
    for source_qid, qids in GROUPS.items():
        source = source_rows[source_qid]
        text = source.get("candidate_text") or ""
        if not text:
            raise SystemExit(f"group source Q{source_qid} has no explicit candidate text")
        bounded, marker = bounded_group_text(source_qid, text)
        payloads = split_numbered(bounded, qids)
        for qid, payload in payloads.items():
            derived[qid] = {
                "schema_version": "exam-local-analysis-group-candidate-0.1",
                "candidate_id": f"{EXAM_ID}-Q{qid:03d}-LOCAL-GROUP-ANALYSIS",
                "exam_id": EXAM_ID,
                "question_id": qid,
                "source_role": "answer_scoring_candidate",
                "candidate_status": "candidate_unverified",
                "candidate_kind": "answer_excerpt_from_explicit_numbered_group",
                "candidate_extraction_method": "explicit_numbered_group_split",
                "candidate_text": payload,
                "candidate_text_sha256": sha(payload),
                "source_group_question_id": source_qid,
                "source_group_candidate_id": source.get("candidate_id"),
                "source_group_candidate_text_sha256": source.get("candidate_text_sha256"),
                "source_group_boundary_marker": marker,
                "source_group_bounded_text_sha256": sha(bounded),
                "source_analysis_segment": source.get("source_analysis_segment"),
                "source_analysis_pdf": source.get("source_analysis_pdf"),
                "source_analysis_mineru_md": source.get("source_analysis_mineru_md"),
                "source_clean_md": source.get("source_clean_md"),
                "source_segment_file_sha256": source.get("source_segment_file_sha256"),
                "source_segment_clean_sha256": source.get("source_segment_clean_sha256"),
                "source_answer_bundle": source.get("source_answer_bundle"),
                "source_answer_index": source.get("source_answer_index"),
                "source_authority_status": "unverified_local_provided",
                "answer_source_status": "missing_separate_answer_bundle",
                "scoring_status": "not_available_as_official",
                "mapping_level": "M0",
                "kp_id": "N/A",
                "review_status": "needs_manual_review",
                "manual_boundary": {
                    "status": "split_on_explicit_numbered_group",
                    "source_group_question_id": source_qid,
                    "question_ids_in_group": qids,
                    "boundary_marker": marker,
                },
                "notes": [
                    "仅按本地解析候选中显式题号/分小问边界切分；未从解释性文字推断答案。",
                    "共享答案块原始归属保留为 source_group_question_id；本层不修改原始解析段、主答案索引或 PDF。",
                    "候选仍是未核验本地解析来源，不是官方答案或评分标准。",
                ],
            }
    for qid in range(1, 23):
        if qid in derived:
            continue
        source = source_rows[qid]
        text = source.get("candidate_text") or ""
        if qid == 22 and text:
            status = "candidate_writing_artifact"
            kind = "writing_model_or_example_artifact"
            candidate = text
        else:
            status = "candidate_mixed_analysis"
            kind = "analysis_excerpt_without_explicit_answer_marker"
            candidate = ""
        derived[qid] = {
            "schema_version": "exam-local-analysis-group-candidate-0.1",
            "candidate_id": f"{EXAM_ID}-Q{qid:03d}-LOCAL-GROUP-ANALYSIS",
            "exam_id": EXAM_ID,
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": status,
            "candidate_kind": kind,
            "candidate_extraction_method": "preserved_unresolved_local_segment",
            "candidate_text": candidate,
            "candidate_text_sha256": sha(candidate),
            "source_group_question_id": qid,
            "source_group_candidate_id": source.get("candidate_id"),
            "source_group_candidate_text_sha256": source.get("candidate_text_sha256"),
            "source_group_boundary_marker": None,
            "source_group_bounded_text_sha256": source.get("candidate_text_sha256"),
            "source_analysis_segment": source.get("source_analysis_segment"),
            "source_analysis_pdf": source.get("source_analysis_pdf"),
            "source_analysis_mineru_md": source.get("source_analysis_mineru_md"),
            "source_clean_md": source.get("source_clean_md"),
            "source_segment_file_sha256": source.get("source_segment_file_sha256"),
            "source_segment_clean_sha256": source.get("source_segment_clean_sha256"),
            "source_answer_bundle": source.get("source_answer_bundle"),
            "source_answer_index": source.get("source_answer_index"),
            "source_authority_status": "unverified_local_provided",
            "answer_source_status": "missing_separate_answer_bundle",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "review_status": "needs_manual_review",
            "manual_boundary": {"status": "not_resolved"},
            "notes": [
                "未发现可安全切分的独立答案标记；保留原候选/混合解析边界，不作答案推断。",
                "Q22 的‘例文’保留为写作材料，不作为评分标准。" if qid == 22 else "",
            ],
        }
    rows = [derived[qid] for qid in range(1, 23)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["candidate_status"]] = counts.get(row["candidate_status"], 0) + 1
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-local-analysis-group-candidate-0.1"\n'
        'status: "candidate_only_group_split"\n'
        'authority_status: "unverified_local_provided"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2023 全国甲卷本地解析共享答案块切分层\n\n"
        "> 仅对解析卷候选中明确出现的共享题号答案块做可逆切分：Q003→Q1—Q3、Q006→Q4—Q6、Q009→Q7—Q9、Q015→Q14—Q15、Q021→Q17—Q21。Q10—Q13、Q16 和作文材料边界继续保留未解决。\n\n"
        f"- 输出：`{rel(OUT)}`；记录数 {len(rows)}。\n"
        f"- 状态计数：{counts}。\n"
        "- 所有记录保持 `unverified_local_provided`、`not_available_as_official`、`M0 / kp_id=N/A`。\n",
        encoding="utf-8",
    )
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-local-group-candidate-receipt-0.1",
        "receipt_id": "EXAM-LOCAL-GROUP-CANDIDATES-GK-NCA-2023-20260809",
        "generated_at": now_text(),
        "exam_id": EXAM_ID,
        "input": {"path": rel(INPUT), "sha256": sha(INPUT.read_text(encoding="utf-8"))},
        "output": {"path": rel(OUT), "sha256": sha(OUT.read_text(encoding="utf-8")), "rows": len(rows)},
        "group_sources": {str(k): v for k, v in GROUPS.items()},
        "counts": counts,
        "source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "counts": counts, "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
