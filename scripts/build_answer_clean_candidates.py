#!/usr/bin/env python3
"""Build a conservative, reversible answer/analysis split layer.

The upstream answer_index files are read-only source derivatives for this
operation.  This script never promotes a local analysis to an official key,
never creates scoring points, and never changes M0 mapping fields.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract"
REPORT = ROOT / "work/knowledge/高考分析/EXAM-ANSWER-CLEAN-CANDIDATES-20260809.md"
REVIEW_QUEUE = ROOT / "work/knowledge/高考分析/EXAM-ANSWER-CLEAN-REVIEW-QUEUE-20260809.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_answer_clean_candidates_20260809.json"
COMPOUND_RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_answer_compound_alignment_GK-NC3-2016_20260809.json"
ANSWER_BOUNDARY_RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_answer_boundary_GK-NC3-2020-Q002_20260809.json"
REFERENCE_2024 = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/reference_answer_candidates.jsonl"
REFERENCE_2024_MEIPIAN = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/reference_answer_candidates_meipian.jsonl"
REFERENCE_2016_Q006 = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers/reference_answer_candidates_q006_gzywtk.jsonl"
LOCAL_REFERENCE_2016_Q006 = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers/reference_answer_candidates_q006_local_analysis.jsonl"
REFERENCE_2013 = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/reference_answer_candidates.jsonl"

ANALYSIS_RE = re.compile(
    r"(?:^|\n)\s*(?:【\s*(?:分析|解析)\s*】|(?:分析|解析)\s*[:：])"
)
ANSWER_RE = re.compile(
    # MinerU frequently preserves a heading prefix (``## 【解答】`` or
    # ``### 答案：``).  The prefix is formatting, not evidence of a new
    # question, so allow it while retaining the exact marker text.
    r"(?:^|\n)\s*(?:#{1,6}\s*)?(?:【\s*(?:参考)?(?:答案|解答)\s*】|(?:参考)?(?:答案|解答)\s*[:：]|解答\s*】)"
)


def sha(text: str | None) -> str | None:
    if not text:
        return None
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def marker_info(text: str) -> list[dict[str, object]]:
    found: list[dict[str, object]] = []
    for kind, pattern in (("analysis", ANALYSIS_RE), ("answer", ANSWER_RE)):
        for match in pattern.finditer(text):
            found.append({"kind": kind, "marker": match.group(0).strip(), "start": match.start(), "end": match.end()})
    return sorted(found, key=lambda x: (int(x["start"]), str(x["kind"])))


def first_stop(text: str, start: int) -> int:
    """Return the first explicit end-of-analysis/section marker after start."""
    stops: list[int] = []
    for pattern in (
        r"\n\s*(?:【\s*点评\s*】|点评\s*】)",
        r"\n\s*##\s+",
    ):
        match = re.search(pattern, text[start:])
        if match:
            stops.append(start + match.start())
    return min(stops) if stops else len(text)


def answer_stop(text: str, start: int) -> int:
    """Return a conservative end for an answer/solution excerpt.

    Sample essays and translated answers often begin with a Markdown title
    (``## 金山银山不如绿水青山``).  Treating every heading as a stop would
    silently discard the actual candidate.  For an answer block, stop at an
    explicit review/commentary marker or at the next numbered exam section;
    answer-key markers are handled separately by ``marker_info``.
    """
    stops: list[int] = []
    for pattern in (
        r"\n\s*(?:#{1,6}\s*)?(?:【\s*点评\s*】|点评\s*】)",
        r"\n\s*#{1,6}\s+[一二三四五六七八九十]+\s*[、.．]",
    ):
        match = re.search(pattern, text[start:])
        if match:
            stops.append(start + match.start())
    return min(stops) if stops else len(text)


def detect_compound_blocks(text: str, analyses: list[dict[str, object]], answers: list[dict[str, object]]) -> tuple[str, list[dict[str, object]]]:
    """Detect an explicit next-section heading inside one answer-index field.

    This is a source-alignment warning, not a semantic split or answer
    inference.  It is intentionally conservative: only a second analysis
    marker plus a visible Markdown section heading after the first answer
    block qualifies.
    """
    if len(analyses) < 2 or not answers:
        return "single_question_block", []
    first_answer = next((m for m in answers if int(m["start"]) >= int(analyses[0]["end"])), None)
    if not first_answer:
        return "single_question_block", []
    after_first = first_stop(text, int(first_answer["end"]))
    # Skip the local answer heading itself (often ``## 答案：``); only a
    # subsequent section heading can indicate a compound question field.
    search_base = min(len(text), after_first + 1)
    match = re.search(r"\n\s*##\s*[一二三四五六七八九十]+[、.．][^\n]*\n", text[search_base:])
    if not match:
        return "single_question_block", []
    start = search_base + match.start()
    marker = text[start:search_base + match.end()].strip()
    next_question_id = None
    next_q = re.search(r"\n\s*(\d{1,2})[．.]", text[search_base + match.end():])
    if next_q:
        next_question_id = int(next_q.group(1))
    sections = [
        {"ordinal": 1, "source_question_id": None, "source_offset_start": 0, "source_offset_end": start, "source_excerpt_sha256": sha(text[:start])},
        {"ordinal": 2, "source_question_id": next_question_id, "source_offset_start": start, "source_offset_end": len(text), "source_excerpt_sha256": sha(text[start:])},
    ]
    return "explicit_compound_question_blocks", [{"boundary_marker": marker, "sections": sections}]


def classify_unbounded_field(raw: str) -> tuple[str, str | None, str | None]:
    """Classify marker-free answer fields without asserting official content."""
    stripped = raw.strip()
    if len(stripped) <= 24 and "\n" not in stripped:
        return "short_option_candidate", None, stripped or None
    match = re.match(
        r"^(?:##\s*)?\d+\s*[.．]\s*(?:[（(]\s*\d+\s*分\s*[）)])\s*",
        stripped,
    )
    if match:
        body = stripped[match.end():].strip()
        return "scoring_placeholder_only" if not body else "answer_scoring_excerpt_no_marker", match.group(0), body or None
    return "unbounded_raw_candidate", None, stripped or None


def process_exam(base: Path) -> tuple[dict, list[dict]]:
    index = base / "answers" / "answer_index.jsonl"
    candidates_path = base / "answers" / "answer_candidates.jsonl"
    output = base / "answers" / "answer_clean_candidates.jsonl"
    index_rows = read_jsonl(index)
    candidate_rows = {int(r["question_id"]): r for r in read_jsonl(candidates_path) if str(r.get("question_id", "")).isdigit()}
    rows: list[dict] = []
    counts: Counter[str] = Counter()
    for source in index_rows:
        qid = int(source["question_id"])
        raw = source.get("answer_text") or ""
        markers = marker_info(raw)
        analyses = [m for m in markers if m["kind"] == "analysis"]
        answers = [m for m in markers if m["kind"] == "answer"]
        compound_status, compound_meta = detect_compound_blocks(raw, analyses, answers)
        if compound_meta:
            compound_meta[0]["sections"][0]["source_question_id"] = qid
        analysis = analyses[0] if analyses else None
        answer = next((m for m in answers if not analysis or int(m["start"]) >= int(analysis["end"])), None)
        question_excerpt = None
        analysis_excerpt = None
        answer_excerpt = None
        answer_prefix = None
        content_shape = None
        solution_excerpt = None
        answer_key_excerpt = None
        answer_marker = None
        answer_key_marker = None
        if analysis:
            astart = int(analysis["start"])
            question_excerpt = raw[:astart].rstrip()
            aend = int(answer["start"]) if answer else len(raw)
            analysis_excerpt = raw[astart:aend].strip()
            if answer:
                answer_marker = str(answer["marker"])
                answer_end = answer_stop(raw, int(answer["end"]))
                later_answers = [m for m in answers if int(m["start"]) > int(answer["end"])]
                key = next((m for m in later_answers if "答案" in str(m["marker"])), None)
                if key:
                    answer_key_marker = str(key["marker"])
                    solution_excerpt = raw[int(answer["end"]):int(key["start"])].strip()
                    key_end = answer_stop(raw, int(key["end"]))
                    answer_key_excerpt = raw[int(key["end"]):key_end].strip()
                else:
                    solution_excerpt = raw[int(answer["end"]):answer_end].strip()
                answer_excerpt = answer_key_excerpt or solution_excerpt or None
            cleaning_status = "explicit_analysis_boundary_with_answer_marker" if answer else "explicit_analysis_boundary_no_answer_marker"
        elif answer:
            # Without an analysis boundary we do not pretend that the prefix is
            # question-only; preserve it as an unbounded source excerpt.
            answer_marker = str(answer["marker"])
            answer_end = answer_stop(raw, int(answer["end"]))
            later_answers = [m for m in answers if int(m["start"]) > int(answer["end"])]
            key = next((m for m in later_answers if "答案" in str(m["marker"])), None)
            if key:
                answer_key_marker = str(key["marker"])
                solution_excerpt = raw[int(answer["end"]):int(key["start"])].strip()
                key_end = answer_stop(raw, int(key["end"]))
                answer_key_excerpt = raw[int(key["end"]):key_end].strip()
                answer_excerpt = answer_key_excerpt or solution_excerpt or None
            else:
                answer_excerpt = raw[int(answer["end"]):answer_end].strip()
                solution_excerpt = answer_excerpt
            cleaning_status = "answer_marker_without_analysis_boundary"
        elif raw:
            upstream = candidate_rows.get(qid, {})
            content_shape, answer_prefix, answer_excerpt = classify_unbounded_field(raw)
            if content_shape == "unbounded_raw_candidate":
                answer_excerpt = upstream.get("answer_candidate_text") or raw
            cleaning_status = "unbounded_answer_field"
        else:
            cleaning_status = "missing"
        status = "candidate_unverified" if raw else "missing"
        external_reference_path = None
        external_reference_status = None
        external_reference_candidates: list[str] = []
        local_reference_candidate = None
        local_reference_status = None
        if base.name == "GK-NCA-2024":
            if 1 <= qid <= 9 and REFERENCE_2024.exists():
                external_reference_candidates.append(rel(REFERENCE_2024))
            if 1 <= qid <= 22 and REFERENCE_2024_MEIPIAN.exists():
                external_reference_candidates.append(rel(REFERENCE_2024_MEIPIAN))
            if external_reference_candidates:
                # Prefer the full-coverage independent source for the legacy
                # singular field while retaining the partial candidate path.
                external_reference_path = external_reference_candidates[-1]
                external_reference_status = (
                    "available_unverified_full_candidate"
                    if REFERENCE_2024_MEIPIAN.exists() and 1 <= qid <= 22
                    else "available_unverified_partial"
                )
        elif base.name == "GK-SC-2013" and 1 <= qid <= 20 and REFERENCE_2013.exists():
            external_reference_path = rel(REFERENCE_2013)
            external_reference_status = "available_unverified_partial"
            external_reference_candidates.append(external_reference_path)
        elif base.name == "GK-NC3-2016" and qid == 6 and REFERENCE_2016_Q006.exists():
            external_reference_path = rel(REFERENCE_2016_Q006)
            external_reference_status = "available_unverified_single_candidate"
            external_reference_candidates.append(external_reference_path)
            if LOCAL_REFERENCE_2016_Q006.exists():
                local_reference_candidate = rel(LOCAL_REFERENCE_2016_Q006)
                local_reference_status = "available_unverified_local_analysis_candidate"
        safe_answer_key_separation = bool(
            analysis and answer and not (len(analyses) - 1)
            and len(answers) == 2 and answer_key_marker
            and int(answers[1]["start"]) > int(answer["end"])
        )
        if compound_status == "explicit_compound_question_blocks":
            marker_separation_status = "compound_source_block_requires_alignment"
        elif safe_answer_key_separation:
            marker_separation_status = "explicit_answer_key_separated"
        elif len(analyses) > 1:
            marker_separation_status = "nested_analysis_unresolved"
        elif len(answers) > 1:
            marker_separation_status = "nested_answer_unresolved"
        else:
            marker_separation_status = "single_or_no_nested_marker"
        row = {
            "schema_version": "answer-clean-candidate-0.1",
            "answer_pair_id": source.get("answer_pair_id"),
            "exam_id": source.get("exam_id"),
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": status,
            "cleaning_status": cleaning_status,
            "source_authority_status": "unverified_local_provided" if raw else "missing",
            "source_status": source.get("source_status", "missing"),
            "answer_source_status": source.get("source_status", "missing"),
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "source_answer_index": rel(index),
            "source_answer_bundle": source.get("answer_bundle_path"),
            "external_reference_candidate": external_reference_path,
            "external_reference_status": external_reference_status,
            "external_reference_candidates": external_reference_candidates,
            "local_reference_candidate": local_reference_candidate,
            "local_reference_status": local_reference_status,
            "source_answer_text_sha256": sha(raw),
            "raw_answer_text_length": len(raw),
            "question_excerpt": question_excerpt,
            "question_excerpt_sha256": sha(question_excerpt),
            "analysis_excerpt": analysis_excerpt,
            "analysis_excerpt_sha256": sha(analysis_excerpt),
            "answer_marker": answer_marker,
            "solution_excerpt": solution_excerpt,
            "solution_excerpt_sha256": sha(solution_excerpt),
            "answer_key_marker": answer_key_marker,
            "answer_key_excerpt": answer_key_excerpt,
            "answer_key_excerpt_sha256": sha(answer_key_excerpt),
            "answer_candidate_text": answer_excerpt,
            "answer_candidate_sha256": sha(answer_excerpt),
            "answer_candidate_prefix_removed": answer_prefix,
            "answer_candidate_prefix_removed_sha256": sha(answer_prefix),
            "content_shape": content_shape or "marker_bounded_candidate",
            "marker_inventory": markers,
            "nested_analysis_marker_count": max(0, len(analyses) - 1),
            "nested_answer_marker_count": max(0, len(answers) - 1),
            "marker_separation_status": marker_separation_status,
            "compound_source_status": compound_status,
            "compound_source_boundaries": compound_meta,
            "review_status": "needs_manual_review",
            "notes": [
                "本层仅为可逆派生清洗，不是官方答案或评分标准。",
                "原 answer_index、解析 PDF、MinerU full.md 和题目双链保持不变。",
            ],
        }
        if compound_status == "explicit_compound_question_blocks":
            row["notes"].append("explicit_next_section_heading_detected; answer_index_alignment_requires_manual_review")
        elif analysis and answer and (len(analyses) > 1 or len(answers) > 1) and not safe_answer_key_separation:
            row["notes"].append("nested_markers_remain_in_answer_excerpt_review_required")
        if not analysis and raw:
            row["notes"].append("no_safe_question_analysis_boundary; raw candidate retained")
        if external_reference_path:
            if external_reference_status == "available_unverified_full_candidate":
                row["notes"].append("external_full_reference_candidate_available; main answer status remains missing")
            else:
                row["notes"].append("external_partial_reference_candidate_available; main answer status remains missing")
        if local_reference_candidate:
            row["notes"].append("local_analysis_reference_candidate_available; same解析来源 family; main answer status remains missing")
        rows.append(row)
    alignments = annotate_reviewed_compound_blocks(base, rows)
    answer_boundary_resolutions = annotate_reviewed_answer_boundaries(base, rows)
    counts = Counter(str(row.get("cleaning_status")) for row in rows)
    if rows:
        output.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    elif output.exists():
        output.unlink()
    return {
        "exam_id": base.name,
        "index_rows": len(index_rows),
        "output": rel(output) if output.exists() else None,
        "status_counts": dict(counts),
        "candidate_rows": rows,
        "compound_alignments": alignments,
        "answer_boundary_resolutions": answer_boundary_resolutions,
    }, rows


def annotate_reviewed_compound_blocks(base: Path, rows: list[dict]) -> list[dict]:
    """Record a human-reviewed source boundary without creating an answer.

    The 2016 NC3 parser put the Q5 solution field and the following Q6
    question in one upstream record.  The explicit ``## 四、实用类文本阅读``
    heading is a deterministic boundary; the vertical-slice receipt supplies
    an independent page/structure check.  We keep both source hashes and only
    annotate the reversible derived layer.
    """
    if base.name != "GK-NC3-2016":
        return []
    by_q = {int(row["question_id"]): row for row in rows}
    resolutions: list[dict] = []
    for parent in rows:
        if parent.get("compound_source_status") != "explicit_compound_question_blocks":
            continue
        boundaries = parent.get("compound_source_boundaries") or []
        if len(boundaries) != 1:
            continue
        sections = boundaries[0].get("sections") or []
        if len(sections) != 2 or any(section.get("source_question_id") is None for section in sections):
            continue
        first, second = sections
        child = by_q.get(int(second["source_question_id"]))
        if not child:
            continue
        review = {
            "review_id": "EXAM-ANSWER-COMPOUND-GK-NC3-2016-Q005-Q006-20260809",
            "review_status": "resolved_in_derived_layer",
            "decision": "Q005 source ends immediately before the explicit next-section heading; Q006 is linked to the remaining source interval. No Q006 answer is inferred.",
            "boundary_marker": boundaries[0].get("boundary_marker"),
            "evidence": [
                "work/knowledge/_reviews/receipts/exam_vertical_GK-NC3-2016_20260809.json",
                "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers/answer_index.jsonl",
            ],
        }
        parent["compound_alignment_status"] = "resolved_derived_boundary"
        parent["compound_alignment_review"] = review
        parent["notes"].append("manual_reviewed_compound_boundary; Q005/Q006 derived alignment recorded")
        child["compound_alignment_status"] = "linked_child_section"
        child["compound_parent_answer_pair_id"] = parent.get("answer_pair_id")
        child["compound_parent_question_id"] = int(first["source_question_id"])
        child["compound_source_interval"] = {
            "source_offset_start": int(second["source_offset_start"]),
            "source_offset_end": int(second["source_offset_end"]),
            "source_excerpt_sha256": second.get("source_excerpt_sha256"),
            "parent_source_answer_text_sha256": parent.get("source_answer_text_sha256"),
        }
        child["compound_alignment_review"] = review
        child["notes"].append("linked_to_reviewed_compound_parent; answer remains missing")
        resolutions.append({
            "parent_answer_pair_id": parent.get("answer_pair_id"),
            "child_answer_pair_id": child.get("answer_pair_id"),
            "boundary_marker": boundaries[0].get("boundary_marker"),
            "sections": sections,
            "parent_source_answer_text_sha256": parent.get("source_answer_text_sha256"),
            "decision": review["decision"],
        })
    return resolutions


def annotate_reviewed_answer_boundaries(base: Path, rows: list[dict]) -> list[dict]:
    """Record the safe answer boundary in the 2020 Q002 mixed source field.

    The local解析 field contains the Q002 prompt followed by ``【解答】``
    and a later ``答案：`` key, but no explicit ``【分析】`` marker.  The
    first marker is therefore sufficient to bound the solution candidate, but
    not sufficient to manufacture a question/analysis split.  This annotation
    keeps the raw prefix untouched, records both marker offsets and hashes,
    and explicitly states that the later key is nested within Q002.
    """
    if base.name != "GK-NC3-2020":
        return []
    row = next((item for item in rows if int(item.get("question_id", 0)) == 2), None)
    if not row:
        return []
    index = base / "answers" / "answer_index.jsonl"
    source_rows = read_jsonl(index)
    source = next((item for item in source_rows if int(item.get("question_id", 0)) == 2), None)
    raw = (source or {}).get("answer_text") or ""
    if not raw:
        return []
    markers = row.get("marker_inventory") or []
    primary = next((m for m in markers if m.get("kind") == "answer" and "解答" in str(m.get("marker"))), None)
    key = next((m for m in markers if m.get("kind") == "answer" and "答案" in str(m.get("marker"))), None)
    if not primary or not key:
        return []
    start = int(primary["start"])
    end = int(primary["end"])
    if start < 0 or end <= start or raw[start:end].strip() != str(primary["marker"]).strip():
        raise ValueError("GK-NC3-2020-Q002: answer marker offset mismatch")
    question_segment = base / "segments" / "question" / "Q002.md"
    analysis_segment = base / "segments" / "analysis" / "Q002.md"
    if not question_segment.exists() or not analysis_segment.exists():
        raise FileNotFoundError("GK-NC3-2020-Q002: question/analysis provenance segment missing")
    review = {
        "review_id": "EXAM-ANSWER-BOUNDARY-GK-NC3-2020-Q002-20260809",
        "review_status": "resolved_in_derived_layer",
        "decision": (
            "The first explicit `【解答】` marker starts the Q002 solution candidate. "
            "The later `答案：` marker is an answer-key marker nested within the same Q002 field. "
            "Because no `【分析】` marker is present, no question/analysis excerpt is inferred."
        ),
        "marker": str(primary["marker"]),
        "answer_key_marker": str(key["marker"]),
        "source_offset_start": start,
        "source_offset_end": end,
        "answer_key_offset_start": int(key["start"]),
        "answer_key_offset_end": int(key["end"]),
        "source_answer_text_sha256": sha(raw),
        "source_prefix_sha256": sha(raw[:start]),
        "source_solution_interval_sha256": sha(raw[start:]),
        "source_question_segment": rel(question_segment),
        "source_question_segment_sha256": sha_file(question_segment),
        "source_analysis_segment": rel(analysis_segment),
        "source_analysis_segment_sha256": sha_file(analysis_segment),
        "evidence": [
            rel(index),
            rel(question_segment),
            rel(analysis_segment),
            "work/knowledge/_reviews/receipts/exam_vertical_GK-NC3-2020_20260809.json",
        ],
        "scoring_status": "not_available_as_official",
        "mapping_level": "M0",
        "kp_id": "N/A",
    }
    row["cleaning_status"] = "derived_answer_boundary_without_analysis"
    row["marker_separation_status"] = "derived_answer_boundary_with_nested_answer_key"
    row["answer_boundary_status"] = "resolved_in_derived_layer"
    row["manual_boundary"] = review
    row["notes"].append(
        "manual_reviewed_derived_answer_boundary; first 解答 marker bounds candidate, nested 答案 marker retained; no analysis split inferred"
    )
    return [review]


def render(reports: list[dict]) -> str:
    total: Counter[str] = Counter()
    total_rows = 0
    lines = [
        "---",
        'schema_version: "answer-clean-candidate-0.1"',
        'status: "candidate_only"',
        'scoring_status: "not_available_as_official"',
        'mapping_status: "M0 | kp_id=N/A"',
        "---",
        "",
        "# 2008—2024 答案/解析候选清洗派生层",
        "",
        "> 该层只按源字段中明确出现的分析/解析/解答/答案标记切分题干、分析与候选答案。不能安全切分的行保留为 unbounded；不修改原答案索引，不生成评分标准，不宣称官方性。",
        "",
    ]
    for report in reports:
        total.update(report["status_counts"])
        total_rows += report["index_rows"]
        total["compound_source_blocks"] += sum(
            1 for row in report["candidate_rows"]
            if row.get("compound_source_status") == "explicit_compound_question_blocks"
        )
    lines.append(f"- 覆盖索引行：{total_rows}；明确分析边界且有答案标记：{total['explicit_analysis_boundary_with_answer_marker']}；明确分析边界但无答案标记：{total['explicit_analysis_boundary_no_answer_marker']}；派生答案边界（无分析标记）：{total['derived_answer_boundary_without_analysis']}；其余保留未界定：{total['unbounded_answer_field'] + total['answer_marker_without_analysis_boundary'] + total['missing']}。")
    lines.append(f"- 检出明确跨题复合源段：{total['compound_source_blocks']} 条；已记录分段偏移、题号和 SHA-256，未将缺失答案补入索引。")
    lines.append("- 已登记两类派生边界回执：2020 Q002 的嵌套答案标记边界，以及 2008 全卷答案字段范围；两者均不改变原始答案索引或答案权威性。")
    lines += [
        "- 全部记录固定 `scoring_status=not_available_as_official`、`mapping_level=M0`、`kp_id=N/A`。",
        "- 每条记录保留原答案字段 SHA-256、标记清单、派生字段哈希和 `source_answer_index` 双链。",
        "",
        "| 试卷 | 索引行数 | 显式分析+答案 | 显式分析无答案 | 派生答案边界 | 未界定/缺失 | 输出 |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for report in reports:
        c = report["status_counts"]
        lines.append(
            f"| {report['exam_id']} | {report['index_rows']} | {c.get('explicit_analysis_boundary_with_answer_marker', 0)} | "
            f"{c.get('explicit_analysis_boundary_no_answer_marker', 0)} | {c.get('derived_answer_boundary_without_analysis', 0)} | "
            f"{c.get('unbounded_answer_field', 0) + c.get('answer_marker_without_analysis_boundary', 0) + c.get('missing', 0)} | `{report['output'] or 'N/A'}` |"
        )
    lines += [
        "",
        "## 放行限制",
        "",
        "1. `answer_candidate_text` 只是本地候选；`答案`/`解答`标签不是权威来源证明。",
        "2. 嵌套标记、OCR 异文、题干与解析混入的行必须人工复核；不能把分析内容当评分点。",
        "3. 独立答案与评分来源、题目定位、教材 KP 双向证据和独立复审均完成前，继续保持 M0。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| 执行脚本 | `scripts/build_answer_clean_candidates.py` |",
        "| 校验脚本 | `scripts/validate_answer_clean_candidates.py` |",
        "",
    ]
    return "\n".join(lines)


def render_review_queue(reports: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "answer-clean-review-queue-0.1"',
        'status: "manual_review_required"',
        'scoring_status: "not_available_as_official"',
        'mapping_status: "M0 | kp_id=N/A"',
        "---",
        "",
        "# 答案/解析候选清洗人工复核队列（2008—2024）",
        "",
        "> 该队列只列出机器无法证明边界或发现嵌套标记的记录。复核只能在派生层写回；不得修改 `answer_index.jsonl`、PDF、MinerU `full.md` 或把本地解析升格为官方答案/评分标准。",
        "",
        "| 记录 | 清洗状态 | 嵌套分析 | 嵌套答案 | 原文长度 | 复核重点 |",
        "|---|---|---:|---:|---:|---|",
    ]
    count = 0
    for report in reports:
        for row in report["candidate_rows"]:
            status = str(row.get("cleaning_status"))
            nested_a = int(row.get("nested_analysis_marker_count", 0))
            nested_k = int(row.get("nested_answer_marker_count", 0))
            unresolved_nested = row.get("marker_separation_status") in {
                "nested_analysis_unresolved", "nested_answer_unresolved"
            } or (
                row.get("marker_separation_status") == "compound_source_block_requires_alignment"
                and row.get("compound_alignment_status") != "resolved_derived_boundary"
            )
            marker_free_shape_is_safe = row.get("content_shape") in {
                "short_option_candidate", "answer_scoring_excerpt_no_marker", "scoring_placeholder_only"
            }
            needs = status in {
                "explicit_analysis_boundary_no_answer_marker",
                "answer_marker_without_analysis_boundary",
                "missing",
            } or (status == "unbounded_answer_field" and not marker_free_shape_is_safe) or unresolved_nested
            if not needs:
                continue
            count += 1
            reason = []
            if unresolved_nested:
                reason.append("嵌套/复合源段需确认段落归属")
            if status == "explicit_analysis_boundary_no_answer_marker":
                reason.append("无明确答案标记")
            if status == "answer_marker_without_analysis_boundary":
                reason.append("答案标记前缺分析边界")
            if status == "unbounded_answer_field" and not marker_free_shape_is_safe:
                reason.append("原答案字段无可用边界")
            if status == "missing":
                if (
                    row.get("exam_id") == "GK-NCA-2024"
                    and 1 <= int(row.get("question_id", 0)) <= 22
                    and (REFERENCE_2024.exists() or REFERENCE_2024_MEIPIAN.exists())
                ) or (
                    row.get("exam_id") == "GK-SC-2013"
                    and 1 <= int(row.get("question_id", 0)) <= 20
                    and REFERENCE_2013.exists()
                ) or (
                    row.get("exam_id") == "GK-NC3-2016"
                    and int(row.get("question_id", 0)) == 6
                    and REFERENCE_2016_Q006.exists()
                ):
                    if (
                        row.get("exam_id") == "GK-NCA-2024"
                        and REFERENCE_2024_MEIPIAN.exists()
                    ):
                        reason.append("主索引缺失；已有外部完整候选，需独立核验")
                    elif (
                        row.get("exam_id") == "GK-NC3-2016"
                        and int(row.get("question_id", 0)) == 6
                        and REFERENCE_2016_Q006.exists()
                    ):
                        if LOCAL_REFERENCE_2016_Q006.exists():
                            reason.append("主索引缺失；已有本地解析切片与外部单题候选，需独立核验")
                        else:
                            reason.append("主索引缺失；已有外部单题候选，需独立核验")
                    else:
                        reason.append("主索引缺失；已有外部部分候选，需独立核验")
                else:
                    reason.append("答案源显式缺失")
            ident = f"{row['exam_id']}-Q{int(row['question_id']):03d}"
            lines.append(
                f"| `{ident}` | `{status}` | {nested_a} | {nested_k} | {row['raw_answer_text_length']} | "
                f"{'；'.join(reason)} |"
            )
    lines += [
        "",
        f"- 队列记录数：{count}。明确的答案/分析切分记录不列入本队列，但仍保持 `candidate_unverified`。",
        "- 复核完成后必须重跑 `python scripts/validate_answer_clean_candidates.py`、`python scripts/audit_exam_answer_scoring_sources.py`、`python scripts/validate_exam_vertical_slices.py` 和 `python scripts/validate_knowledge_base.py`。",
        "",
    ]
    return "\n".join(lines)


def needs_manual_review(row: dict) -> bool:
    status = str(row.get("cleaning_status"))
    unresolved_nested = row.get("marker_separation_status") in {
        "nested_analysis_unresolved", "nested_answer_unresolved"
    } or (
        row.get("marker_separation_status") == "compound_source_block_requires_alignment"
        and row.get("compound_alignment_status") != "resolved_derived_boundary"
    )
    safe_marker_free_shape = row.get("content_shape") in {
        "short_option_candidate", "answer_scoring_excerpt_no_marker", "scoring_placeholder_only"
    }
    return status in {
        "explicit_analysis_boundary_no_answer_marker",
        "answer_marker_without_analysis_boundary",
        "missing",
    } or (status == "unbounded_answer_field" and not safe_marker_free_shape) or unresolved_nested


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", type=Path, default=REPORT)
    args = parser.parse_args()
    reports: list[dict] = []
    for base in sorted(EXTRACT.iterdir()):
        if not base.is_dir():
            continue
        report, _ = process_exam(base)
        reports.append(report)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(render(reports), encoding="utf-8")
    REVIEW_QUEUE.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_QUEUE.write_text(render_review_queue(reports), encoding="utf-8")
    queue_count = sum(1 for report in reports for row in report["candidate_rows"] if needs_manual_review(row))
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "answer-clean-candidate-receipt-0.1",
        "receipt_id": "EXAM-ANSWER-CLEAN-2008-2024-20260809",
        "generated_at": now_text(),
        "status": "candidate_only",
        "indexed_rows": sum(report["index_rows"] for report in reports),
        "clean_outputs": [report["output"] for report in reports if report["output"]],
        "report": rel(args.report),
        "report_sha256": sha_file(args.report),
        "review_queue": rel(REVIEW_QUEUE),
        "review_queue_sha256": sha_file(REVIEW_QUEUE),
        "review_queue_rows": queue_count,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "raw_source_mutation": False,
        "policy": "仅按显式源标记和可验证字段边界生成派生候选；不得将本地解析或答案字段升级为官方答案/评分材料。",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    compound_resolutions = [
        alignment
        for report in reports
        for alignment in report.get("compound_alignments", [])
    ]
    if compound_resolutions:
        COMPOUND_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        COMPOUND_RECEIPT.write_text(json.dumps({
            "schema_version": "exam-answer-compound-alignment-receipt-0.1",
            "receipt_id": "EXAM-ANSWER-COMPOUND-GK-NC3-2016-Q005-Q006-20260809",
            "generated_at": now_text(),
            "status": "resolved_in_derived_layer",
            "source_mutation": False,
            "scoring_status": "not_available_as_official",
            "mapping_status": "M0 | kp_id=N/A",
            "resolutions": compound_resolutions,
            "policy": "仅确认源字段的题号/偏移边界；不从 Q005 复合字段推断 Q006 答案，不修改原始答案索引、PDF 或 MinerU full.md。",
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    answer_boundary_resolutions = [
        resolution
        for report in reports
        for resolution in report.get("answer_boundary_resolutions", [])
    ]
    if answer_boundary_resolutions:
        ANSWER_BOUNDARY_RECEIPT.parent.mkdir(parents=True, exist_ok=True)
        ANSWER_BOUNDARY_RECEIPT.write_text(json.dumps({
            "schema_version": "exam-answer-boundary-receipt-0.1",
            "receipt_id": "EXAM-ANSWER-BOUNDARY-GK-NC3-2020-Q002-20260809",
            "generated_at": now_text(),
            "status": "resolved_in_derived_layer",
            "source_mutation": False,
            "scoring_status": "not_available_as_official",
            "mapping_status": "M0 | kp_id=N/A",
            "resolutions": answer_boundary_resolutions,
            "policy": (
                "仅在可见 `解答` 标记处记录候选答案边界；嵌套 `答案` 标记仍属于同一题，"
                "不把缺失的 `分析` 边界补成事实，不修改原始答案索引、PDF 或 MinerU full.md。"
            ),
        }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(reports, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
