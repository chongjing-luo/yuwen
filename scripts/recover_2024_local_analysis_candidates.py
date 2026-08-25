#!/usr/bin/env python3
"""Recover a conservative local candidate layer from the 2024 analysis PDF.

The source is a locally supplied ``解析卷``.  It is useful for locating answer
payloads, but it is not an official answer key or scoring rubric.  This script
therefore writes only a derived JSONL/report/receipt layer and never mutates
the source PDF, MinerU ``full.md``, question segments, or ``answer_index``.

The parser deliberately records three awkward cases instead of silently
repairing them:

* Q1/Q2 are derived from the explicit ``故选`` conclusion in their analysis;
  the preceding answer line only contains ``3. B``.
* Q16 has two ``【答案】`` markers and a duplicated answer payload containing
  an OCR fragment (``o崖``).  The first payload is retained as the candidate;
  the duplicate and OCR observations are recorded as metadata.
* Q22 contains a model essay followed by writing guidance.  It is labelled as
  a writing artifact and is never treated as a scoring standard.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "Data/2008-2024·（四川）语文高考真题"
EXAM_ID = "GK-NCA-2024"
BASE = CORPUS / "exam_extract" / EXAM_ID
FULL = CORPUS / "mineru_result/2024年高考语文试卷（全国甲卷）（解析卷）/full.md"
PDF = CORPUS / "2024年高考语文试卷（全国甲卷）（解析卷）.pdf"
MEIPIAN = BASE / "answers/reference_answer_candidates_meipian.jsonl"
OUT = BASE / "answers/reference_answer_candidates_local_analysis.jsonl"
REPORT = ROOT / "work/knowledge/exams/workbench/EXAM-REFERENCE-ANSWER-CANDIDATES-2024-LOCAL-ANALYSIS.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidates_local_analysis_GK-NCA-2024_20260809.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str | None) -> str | None:
    if text is None:
        return None
    return sha_bytes(text.encode("utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def collapse_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def compact(text: str) -> str:
    # Used only for comparison diagnostics, never for replacing source text.
    return re.sub(r"[\s，。；：、．.（）()【】「」‘’“”《》:;!?！？\-—_]+", "", text)


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf'(?m)^{re.escape(key)}:\s*"([^"]+)"$', text)
    return match.group(1) if match else None


def load_rows(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def question_starts(text: str) -> dict[int, int]:
    starts: dict[int, int] = {}
    for match in re.finditer(r"(?m)^\s*(\d{1,2})\s*[.．]", text):
        qid = int(match.group(1))
        if 1 <= qid <= 22 and qid not in starts:
            starts[qid] = match.start()
    missing = sorted(set(range(1, 23)) - set(starts))
    if missing:
        raise RuntimeError(f"question starts missing: {missing}")
    return starts


def answer_markers(text: str) -> list[re.Match[str]]:
    return list(re.finditer(r"【答案】", text))


def analysis_markers(text: str) -> list[re.Match[str]]:
    return list(re.finditer(r"【解析】", text))


def analysis_boundary_start(text: str, marker: re.Match[str]) -> int:
    """Include a preceding Markdown heading in the analysis boundary.

    MinerU emits both ``【解析】`` and ``## 【解析】``.  The latter would
    otherwise leave a stray ``##`` at the end of the answer excerpt.
    """
    prefix = text[max(0, marker.start() - 3):marker.start()]
    return marker.start() - 3 if prefix == "## " else marker.start()


def numbered_segments(block: str, qids: list[int]) -> dict[int, str]:
    """Split a compact answer block such as ``4.C5...6...`` by question id."""
    matches: list[tuple[int, int, int]] = []
    for qid in qids:
        match = re.search(rf"(?<!\d){qid}\s*[.．]", block)
        if not match:
            raise RuntimeError(f"answer number {qid} not found in block: {block[:100]!r}")
        matches.append((qid, match.start(), match.end()))
    matches.sort(key=lambda item: item[1])
    result: dict[int, str] = {}
    for idx, (qid, start, end) in enumerate(matches):
        stop = matches[idx + 1][1] if idx + 1 < len(matches) else len(block)
        candidate = block[end:stop].strip()
        if not candidate:
            raise RuntimeError(f"empty candidate for Q{qid}")
        result[qid] = candidate
    return result


def analysis_excerpt(text: str, qid: int) -> tuple[str | None, str]:
    """Return the analysis excerpt and extraction boundary label."""
    # Numbered detailed headings are stable for Q1-Q15.
    heading = re.search(rf"(?m)^##\s+【{qid}题详解】", text)
    if heading:
        starts = [m.start() for m in re.finditer(r"(?m)^##\s+【\d+题详解】", text) if m.start() > heading.start()]
        stop = min(starts) if starts else len(text)
        return text[heading.start():stop].strip(), "numbered_analysis_heading"

    # Q16, Q21, Q22 use an unnumbered ``【详解】`` marker.  The surrounding
    # section headings are used as hard boundaries.
    section = {16: ("【解析】", "## 三、语言文字运用"), 21: ("【解析】", "## 四、作文"), 22: ("【解析】", "资料提供形式：")}
    if qid in section:
        start_marker, end_marker = section[qid]
        # Q16's first解析 marker is the one immediately after the Q14-15
        # analysis; Q21/Q22 likewise use their local section marker.
        if qid == 16:
            start = text.find(start_marker, text.find("## （三）名篇名句默写"))
        elif qid == 21:
            start = text.find(start_marker, text.find("21."))
        else:
            start = text.find(start_marker, text.find("22."))
        if start >= 0:
            stop = text.find(end_marker, start)
            if stop < 0:
                stop = len(text)
            return text[start:stop].strip(), "unnumbered_analysis_marker"
    return None, "analysis_excerpt_not_found"


def build_source_blocks(text: str) -> tuple[dict[int, dict], dict[int, str]]:
    """Build source answer sections and candidate payloads for Q1-Q22."""
    answers = answer_markers(text)
    analyses = analysis_markers(text)
    if len(answers) != 9 or len(analyses) != 9:
        raise RuntimeError(f"unexpected marker count answers={len(answers)} analyses={len(analyses)}")

    # The first analysis marker belongs to Q1-Q3.  The following eight answer
    # sections are Q4-6, Q7-9, Q10-13, Q14-15, Q16, Q17-20, Q21 and Q22.
    groups: list[tuple[list[int], int, int]] = [
        ([4, 5, 6], 0, 1),
        ([7, 8, 9], 1, 2),
        ([10, 11, 12, 13], 2, 3),
        ([14, 15], 3, 4),
        ([16], 4, 5),
        ([17, 18, 19, 20], 6, 6),
        ([21], 7, 7),
        ([22], 8, 8),
    ]
    payloads: dict[int, str] = {}
    sections: dict[int, dict] = {}

    # Q1-Q3 have no leading 【答案】 marker.  Their local answer area is the
    # Q3 answer line plus the analysis conclusions.  Q1/Q2 are derived from
    # ``故选C/D`` and Q3 is explicitly ``3. B``.
    first_analysis_start = analysis_boundary_start(text, analyses[0])
    q3_answer_area_start = text.find("3. B")
    if q3_answer_area_start < 0 or q3_answer_area_start > first_analysis_start:
        raise RuntimeError("Q1-Q3 answer area not found")
    q3_area = text[q3_answer_area_start:first_analysis_start].strip()
    payloads[3] = "B"
    for qid, letter in ((1, "C"), (2, "D")):
        payloads[qid] = letter
    source = {
        "start": q3_answer_area_start,
        "end": first_analysis_start,
        "marker": None,
        "excerpt": q3_area,
        "boundary_status": "derived_from_analysis_conclusion_for_q1_q2_and_explicit_q3_key",
    }
    for qid in (1, 2, 3):
        sections[qid] = dict(source)

    # Explicit answer sections.
    for qids, answer_idx, analysis_idx in groups:
        marker = answers[answer_idx]
        analysis_start = analysis_boundary_start(text, analyses[analysis_idx])
        end = analysis_start
        if answer_idx == 8:
            # Q22 answer block ends at its own analysis marker (analyses[8]).
            end = analysis_start
        raw_section = text[marker.start():end].strip()
        body = text[marker.end():end].strip()
        if qids == [16]:
            # The second marker is immediately followed by the actual payload.
            duplicate_markers = list(re.finditer(r"【答案】", body))
            if not duplicate_markers:
                raise RuntimeError("Q16 duplicate answer marker not found")
            payload_start = duplicate_markers[-1].end()
            duplicate_payload = body[payload_start:].strip()
            # The answer list itself repeats every ①-⑥ item.  Keep the first
            # occurrence of each numbered item, while preserving the complete
            # duplicated payload in metadata for auditability.
            symbols = "①②③④⑤⑥"
            first_positions: dict[str, int] = {}
            all_positions: dict[str, list[int]] = {}
            for symbol in symbols:
                positions = [m.start() for m in re.finditer(rf"{symbol}\s*[.．]", duplicate_payload)]
                if not positions:
                    raise RuntimeError(f"Q16 answer symbol {symbol} missing")
                all_positions[symbol] = positions
                first_positions[symbol] = positions[0]
            all_marker_positions = sorted(
                position for positions in all_positions.values() for position in positions
            )
            pieces: list[str] = []
            for symbol in symbols:
                start_symbol = first_positions[symbol]
                following = [position for position in all_marker_positions if position > start_symbol]
                stop = following[0] if following else len(duplicate_payload)
                pieces.append(duplicate_payload[start_symbol:stop].strip())
            candidate = " ".join(pieces).strip()
            duplicate_tail = duplicate_payload
            payloads[16] = candidate
            sections[16] = {
                "start": marker.start(),
                "end": end,
                "marker": "【答案】",
                "excerpt": raw_section,
                "boundary_status": "explicit_answer_marker_with_duplicate_answer_payload",
                "duplicate_marker_count": len(duplicate_markers) + 1,
                "duplicate_tail": duplicate_tail,
                "duplicate_payload_sha256": sha_text(duplicate_payload),
                "duplicate_symbol_counts": {symbol: len(all_positions[symbol]) for symbol in symbols},
            }
            continue
        if qids in ([21], [22]):
            target_qid = qids[0]
            payloads[target_qid] = body
            sections[target_qid] = {
                "start": marker.start(),
                "end": end,
                "marker": "【答案】",
                "excerpt": raw_section,
                "boundary_status": "explicit_answer_marker_model_essay" if target_qid == 22 else "explicit_answer_marker_free_text_answer",
            }
            continue
        parsed = numbered_segments(body, qids)
        for qid, candidate in parsed.items():
            payloads[qid] = candidate
            sections[qid] = {
                "start": marker.start(),
                "end": end,
                "marker": "【答案】",
                "excerpt": raw_section,
                "boundary_status": "explicit_answer_marker_numbered_group",
            }
    if sorted(payloads) != list(range(1, 23)):
        raise RuntimeError(f"payload coverage mismatch: {sorted(payloads)}")
    return sections, payloads


def compare(local: str, third: dict, qid: int) -> dict:
    external = third.get("answer_candidate_text") or ""
    result = {
        "third_party_candidate_id": third.get("candidate_id"),
        "third_party_source": third.get("source_html"),
        "exact_text_match": local == external,
        "compact_text_match": compact(local) == compact(external),
        "local_text_sha256": sha_text(local),
        "third_party_text_sha256": third.get("answer_candidate_sha256"),
        "adjudication": "unresolved",
        "notes": [],
    }
    if qid == 22:
        result["adjudication"] = "not_comparable_writing_artifact"
        result["notes"].append("本地候选为解析卷例文答案块，美篇候选为作文审题/写作指导；两者均非评分细则。")
    elif qid == 12 and local != external:
        result["adjudication"] = "conflict_requires_independent_verification"
        result["notes"].append("本地解析卷显式给出 A；美篇第三方候选给出 C，形成选项冲突。")
    elif qid in (8, 9) and not result["compact_text_match"]:
        result["adjudication"] = "ocr_or_format_difference_requires_review"
        result["notes"].append("本地解析切片出现数字/圈码 OCR 差异（如 `(3)` 或 `1` 与 `③/①`），未静默修复。")
    elif qid == 16 and not result["compact_text_match"]:
        result["adjudication"] = "ocr_or_format_difference_requires_review"
        result["notes"].extend(["本地答案串①—⑥均有重复，候选已去重保留首份并登记完整重复 payload。", "本地 OCR 含疑似‘o崖’残片，美篇候选为‘砯崖’。"])
    elif result["exact_text_match"] or result["compact_text_match"]:
        result["adjudication"] = "textually_consistent_unverified"
    else:
        result["adjudication"] = "text_difference_requires_review"
        result["notes"].append("两份候选文本存在格式、标点或表述差异，未作静默裁决。")
    return result


def main() -> int:
    raw = FULL.read_text(encoding="utf-8")
    sections, payloads = build_source_blocks(raw)
    third_rows = {int(row["question_id"]): row for row in load_rows(MEIPIAN)}
    if sorted(third_rows) != list(range(1, 23)):
        raise RuntimeError("Meipian candidate layer is not full Q1-Q22")

    rows: list[dict] = []
    for qid in range(1, 23):
        segment = BASE / f"segments/analysis/Q{qid:03d}.md"
        segment_text = segment.read_text(encoding="utf-8") if segment.exists() else ""
        analysis, analysis_method = analysis_excerpt(raw, qid)
        candidate = payloads[qid]
        sec = sections[qid]
        row = {
            "schema_version": "exam-reference-answer-candidate-0.3",
            "candidate_id": f"{EXAM_ID}-Q{qid:03d}-LOCAL-ANALYSIS-ANSWER",
            "exam_id": EXAM_ID,
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": "candidate_unverified",
            "candidate_scope": "local_analysis_full_q1_q22",
            "source_authority_status": "unverified_local_provided",
            "source_status": "unverified_local_provided",
            "answer_source_status": "local_analysis_full_candidate",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "candidate_content_type": "writing_model_essay_candidate" if qid == 22 else "reference_answer_candidate",
            "candidate_extraction_method": (
                "derived_from_analysis_conclusion" if qid in (1, 2)
                else "explicit_answer_marker_with_duplicate_payload_normalized" if qid == 16
                else "explicit_answer_marker_model_essay" if qid == 22
                else "explicit_answer_marker_numbered_group"
            ),
            "answer_candidate_text": candidate,
            "answer_candidate_sha256": sha_text(candidate),
            "source_answer_section": {
                "path": rel(FULL),
                "offset_start": sec["start"],
                "offset_end": sec["end"],
                "excerpt": sec["excerpt"],
                "excerpt_sha256": sha_text(sec["excerpt"]),
                "boundary_status": sec["boundary_status"],
            },
            "source_analysis_excerpt": analysis,
            "source_analysis_excerpt_sha256": sha_text(analysis),
            "analysis_extraction_method": analysis_method,
            "source_segment": rel(segment),
            "source_segment_sha256": sha_bytes(segment.read_bytes()) if segment.exists() else None,
            "source_segment_clean_sha256": frontmatter_value(segment_text, "segment_clean_sha256"),
            "source_pdf": rel(PDF),
            "source_pdf_sha256": sha_bytes(PDF.read_bytes()),
            "source_mineru_md": rel(FULL),
            "source_mineru_md_sha256": sha_bytes(FULL.read_bytes()),
            "source_answer_index": rel(BASE / "answers/answer_index.jsonl"),
            "external_comparison": compare(candidate, third_rows[qid], qid),
            "review_status": "needs_cross_source_adjudication",
            "notes": [
                "解析卷是本地提供的未核验候选来源，不是官方答案或评分标准。",
                "本候选层不修改主 answer_index、PDF、MinerU full.md 或题目切片；知识点映射保持 M0 / kp_id=N/A。",
                "Q1/Q2 从各自解析末尾‘故选’恢复，原始答案区仅显式出现 Q3 的‘3. B’。" if qid in (1, 2) else "",
                "Q16 原始答案区有重复答案标记与重复①—⑥ payload；候选去重保留首份并登记完整重复 payload。" if qid == 16 else "",
                "Q22 原始答案区是例文，配套解析是写作指导；不得当作评分细则。" if qid == 22 else "",
            ],
        }
        if qid == 16:
            row["q16_duplicate_marker_count"] = sec.get("duplicate_marker_count")
            row["q16_duplicate_tail"] = sec.get("duplicate_tail")
            row["q16_duplicate_symbol_counts"] = sec.get("duplicate_symbol_counts")
            row["q16_ocr_observations"] = ["o崖（疑似‘砯崖’的 OCR/版面残片）"]
        rows.append(row)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    conflicts = [
        row for row in rows
        if row["external_comparison"]["adjudication"] in {"conflict_requires_independent_verification", "ocr_or_format_difference_requires_review"}
    ]
    consistent = sum(row["external_comparison"]["adjudication"] == "textually_consistent_unverified" for row in rows)
    report_lines = [
        "---",
        'schema_version: "exam-reference-answer-candidate-0.3"',
        'status: "candidate_only_local_analysis"',
        'authority_status: "unverified_local_provided"',
        'coverage: "GK-NCA-2024 Q1-Q22"',
        'scoring_status: "not_available_as_official"',
        'mapping_status: "M0 | kp_id=N/A"',
        "---",
        "",
        "# 2024 全国甲卷本地解析答案候选层",
        "",
        "> 本层从解析卷 MinerU `full.md` 恢复答案区和解析区的可定位候选，仅供与美篇第三方候选做结构/文本比对。任何候选均未达到官方答案或评分标准门槛；主 `answer_index.jsonl` 仍保持 22 条 `N/A`。",
        "",
        f"- 本地候选：22 条（Q1—Q22）；与美篇文本一致（未核验）：{consistent} 条。",
        f"- 需重点复核：{len(conflicts)} 条（Q8/Q9 圈码 OCR、Q12 选项冲突、Q16 OCR/重复串）；Q22 为写作材料，不参与答案一致性判断。",
        f"- 源 MinerU：`{rel(FULL)}`，SHA-256 `{sha_bytes(FULL.read_bytes())}`。",
        f"- 源 PDF：`{rel(PDF)}`，SHA-256 `{sha_bytes(PDF.read_bytes())}`。",
        f"- 派生 JSONL：`{rel(OUT)}`。",
        "",
        "## 逐题比对",
        "",
        "| 题号 | 本地候选摘要 | 美篇候选摘要 | 判定 |",
        "|---:|---|---|---|",
    ]
    for row in rows:
        local = collapse_space(row["answer_candidate_text"])
        external = collapse_space(third_rows[row["question_id"]].get("answer_candidate_text") or "")
        if len(local) > 90:
            local = local[:87] + "…"
        if len(external) > 90:
            external = external[:87] + "…"
        report_lines.append(f"| {row['question_id']} | {local.replace('|', '／')} | {external.replace('|', '／')} | `{row['external_comparison']['adjudication']}` |")
    report_lines += [
        "",
        "## 边界和异常",
        "",
        "- Q1/Q2：原始答案区只有 Q3 的 `3. B`；Q1=C、Q2=D 仅由对应解析末尾 `故选C/D` 派生，不能写回主答案索引。",
        "- Q4—Q21：按显式 `【答案】`—`【解析】` 区间登记；答案文本与解析文本分开保存并保留源偏移/哈希。",
        "- Q12：本地解析卷给出 A，美篇候选给出 C；这是实质选项冲突，必须独立核验，不能多数表决。",
        "- Q16：有两个 `【答案】` 标记，①—⑥答案串均重复；候选去重保留首份，登记完整重复 payload 与疑似 `o崖` OCR 残片。",
        "- Q22：本地答案区为例文，美篇对应区为作文审题/写作指导；两者均不构成评分标准。",
        "",
        "## 使用限制",
        "",
        "1. `candidate_unverified` 不等于官方答案；`scoring_status` 固定为 `not_available_as_official`。",
        "2. 未取得独立命题机构/考试机构答案与评分材料前，不从文本一致性推导权威性。",
        "3. 所有题目的教材映射继续保持 `M0 / kp_id=N/A`。",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    receipt = {
        "schema_version": "exam-reference-answer-candidate-receipt-0.3",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-NCA-2024-LOCAL-ANALYSIS-20260809",
        "generated_at": now_text(),
        "exam_id": EXAM_ID,
        "status": "candidate_only_local_analysis",
        "source_authority_status": "unverified_local_provided",
        "coverage": {"candidate_questions": list(range(1, 23)), "writing_artifact_questions": [22], "boundary_derived_questions": [1, 2], "conflict_questions": [12], "ocr_review_questions": [8, 9, 16]},
        "source_pdf": rel(PDF),
        "source_pdf_sha256": sha_bytes(PDF.read_bytes()),
        "source_mineru_md": rel(FULL),
        "source_mineru_md_sha256": sha_bytes(FULL.read_bytes()),
        "output": rel(OUT),
        "output_sha256": sha_bytes(OUT.read_bytes()),
        "report": rel(REPORT),
        "report_sha256": sha_bytes(REPORT.read_bytes()),
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "本地解析卷仅作为候选层；不覆盖原始 OCR、不提升来源权威、不写回主答案索引。",
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT), "review_questions": [8, 9, 12, 16]}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
