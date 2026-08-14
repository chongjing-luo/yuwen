#!/usr/bin/env python3
"""Clean and split one or more Sichuan Gaokao MinerU outputs.

This is deliberately a conservative first-pass processor.  It never edits a
MinerU ``full.md`` or a source PDF.  It creates a clean copy, question-level
segments, an answer/analysis bundle, and a traceable JSONL ledger.  OCR
uncertainties are recorded, not silently corrected.

The 2008 run is the calibration slice.  Later years can be run with the same
script after the taxonomy and review gate are accepted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "Data" / "2008-2024·（四川）语文高考真题"
OUT = CORPUS / "exam_extract"

NOISE_LINE = re.compile(r"^\s*(?:1|7|Z|V|N|Q|不X|不x)\s*$")
QSTART = re.compile(r"^\s*#{0,2}\s*(\d{1,2})\s*[.．、]\s*(.*)$")
SECTION = re.compile(r"^\s*(?:#{1,3}\s*)?([一二三四五六七八九十]+)[、．.]\s*(?:（|\()")
ANSWER_TITLE = re.compile(r"参考答案")
AD_TITLE = re.compile(r"资料提供形式")
VOLUME_TITLE = re.compile(r"^\s*#{0,3}\s*第(?:I|II|III|Ⅰ|Ⅱ|Ⅲ|1|2)卷(?:\s*[（(].*)?\s*$")

TYPE_MAP: dict[int, tuple[str, str]] = {
    1: ("language_use", "word_pronunciation"),
    2: ("language_use", "idiom_usage"),
    3: ("language_use", "sentence_error"),
    4: ("language_use", "sequence"),
    5: ("objective_choice", "modern_reading_informational"),
    6: ("objective_choice", "modern_reading_informational"),
    7: ("objective_choice", "modern_reading_informational"),
    8: ("objective_choice", "ancient_vocab"),
    9: ("objective_choice", "ancient_text_evidence"),
    10: ("objective_choice", "ancient_text_content"),
    11: ("reading_subjective", "classical_translation"),
    12: ("reading_subjective", "poetry_appreciation"),
    13: ("memorization", "classical_memorization"),
    14: ("reading_subjective", "literary_reading"),
    15: ("reading_subjective", "literary_reading"),
    16: ("reading_subjective", "meaning_explanation"),
    17: ("reading_subjective", "structure_effect"),
    18: ("language_use", "summary"),
    19: ("language_use", "completion"),
    20: ("language_use", "metaphor_series"),
    21: ("writing", "topic_writing"),
}

# Year-specific structure.  The 2008 map above remains the calibration map;
# these maps make the 2009--2015 old-Sichuan papers explicit instead of
# silently inheriting 2008's taxonomy.  The question count is intentionally
# top-level (Q13's two alternatives and multi-blank responses are not new
# questions).
EXAM_CONFIGS: dict[int, dict[str, Any]] = {
    **{y: {
        "question_ids": list(range(1, 22)),
        "section_map": {**{n: "一" for n in range(1, 5)}, **{n: "二" for n in range(5, 8)},
                        **{n: "三" for n in range(8, 11)}, **{n: "四" for n in range(11, 14)},
                        **{n: "五" for n in range(14, 18)}, **{n: "六" for n in range(18, 21)}, 21: "七"},
        "type_map": {
            1: ("language_use", "word_pronunciation"), 2: ("language_use", "orthography"),
            3: ("language_use", "word_usage"), 4: ("language_use", "sentence_grammar"),
            5: ("objective_choice", "modern_reading_informational"), 6: ("objective_choice", "modern_reading_informational"),
            7: ("objective_choice", "modern_reading_informational"), 8: ("objective_choice", "ancient_vocab"),
            9: ("objective_choice", "ancient_function_words"), 10: ("objective_choice", "ancient_text_content"),
            11: ("reading_subjective", "classical_translation"), 12: ("reading_subjective", "poetry_appreciation"),
            13: ("memorization", "classical_memorization"), 14: ("reading_subjective", "literary_reading"),
            15: ("reading_subjective", "literary_reading"), 16: ("reading_subjective", "literary_reading"),
            17: ("reading_subjective", "literary_reading"), 18: ("language_use", "summary"),
            19: ("language_use", "sentence_expansion"), 20: ("language_use", "parallelism_or_practical"),
            21: ("writing", "topic_writing"),
        },
        "material_groups": [("01", 5, 7), ("02", 8, 11), ("03", 12, 12), ("04", 14, 17)],
    } for y in range(2009, 2013)},
    **{y: {
        "question_ids": list(range(1, 22)),
        "section_map": {**{n: "一" for n in range(1, 5)}, **{n: "二" for n in range(5, 8)},
                        **{n: "三" for n in range(8, 10)}, **{n: "四" for n in range(10, 15)},
                        **{n: "五" for n in range(15, 19)}, **{n: "六" for n in range(19, 21)}, 21: "七"},
        "type_map": {
            1: ("language_use", "word_pronunciation"), 2: ("language_use", "orthography"),
            3: ("language_use", "word_usage"), 4: ("language_use", "sentence_grammar"),
            5: ("objective_choice", "modern_reading_informational"), 6: ("objective_choice", "modern_reading_informational"),
            7: ("objective_choice", "modern_reading_informational"), 8: ("objective_choice", "ancient_vocab"),
            9: ("objective_choice", "ancient_function_words"), 10: ("reading_subjective", "classical_translation"),
            11: ("reading_subjective", "ancient_text_content"), 12: ("reading_subjective", "sentence_segmentation"),
            13: ("reading_subjective", "poetry_appreciation"), 14: ("memorization", "classical_memorization"),
            15: ("reading_subjective", "literary_reading"), 16: ("reading_subjective", "literary_reading"),
            17: ("reading_subjective", "literary_reading"), 18: ("reading_subjective", "literary_reading"),
            19: ("language_use", "summary_or_application"), 20: ("language_use", "practical_or_expansion"),
            21: ("writing", "topic_writing"),
        },
        "material_groups": [("01", 5, 7), ("02", 8, 12), ("03", 13, 13), ("04", 15, 18)],
    } for y in range(2013, 2016)},
    **{y: {
        "question_ids": list(range(1, 13)),
        "section_map": ({1: "一", 2: "一", 3: "二", 4: "二", 5: "三", 6: "四", **{n: "五" for n in range(7, 12)}, 12: "六"}
                        if y == 2016 else
                        {1: "一", 2: "一", 3: "一", 4: "二", 5: "二", 6: "二", **{n: "三" for n in range(7, 12)}, 12: "四"}),
        "type_map": ({1: ("objective_choice", "modern_reading_informational"), 2: ("objective_choice", "ancient_text_content"),
                      3: ("reading_subjective", "poetry_appreciation"), 4: ("memorization", "classical_memorization"),
                      5: ("reading_subjective", "literary_reading"), 6: ("reading_subjective", "practical_reading"),
                      **{n: ("language_use", "language_application") for n in range(7, 12)}, 12: ("writing", "topic_writing")}
                     if y == 2016 else
                     {1: ("objective_choice", "modern_reading_informational"), 2: ("reading_subjective", "literary_reading"),
                      3: ("reading_subjective", "practical_reading"), 4: ("objective_choice", "ancient_text_content"),
                      5: ("reading_subjective", "poetry_appreciation"), 6: ("memorization", "classical_memorization"),
                      **{n: ("language_use", "language_application") for n in range(7, 12)}, 12: ("writing", "topic_writing")}),
        "material_groups": [("01", 1, 1), ("02", 2, 2), ("03", 3, 3), ("04", 5, 5), ("05", 6, 6)],
    } for y in range(2016, 2018)},
    **{y: {
        "question_ids": list(range(1, 11)),
        "section_map": {**{n: "一" for n in range(1, 4)}, **{n: "二" for n in range(4, 7)}, **{n: "三" for n in range(7, 10)}, 10: "四"},
        "type_map": {1: ("objective_choice", "modern_reading_informational"), 2: ("reading_subjective", "literary_reading"),
                     3: ("reading_subjective", "practical_reading"), 4: ("objective_choice", "ancient_text_content"),
                     5: ("reading_subjective", "poetry_appreciation"), 6: ("memorization", "classical_memorization"),
                     7: ("language_use", "language_application"), 8: ("language_use", "language_application"),
                     9: ("language_use", "language_application"), 10: ("writing", "topic_writing")},
        "material_groups": [("01", 1, 1), ("02", 2, 2), ("03", 3, 3), ("04", 4, 4), ("05", 5, 5)],
    } for y in range(2018, 2021)},
    **{y: {
        "question_ids": list(range(1, 23)),
        "section_map": {**{n: "一" for n in range(1, 10)}, **{n: "二" for n in range(10, 17)}, **{n: "三" for n in range(17, 22)}, 22: "四"},
        "type_map": {**{n: ("objective_choice", "modern_reading_informational") for n in (1, 2, 3)},
                     **{n: ("reading_subjective", "practical_reading") for n in (4, 5, 6)},
                     **{n: ("reading_subjective", "literary_reading") for n in (7, 8, 9)},
                     **{n: ("objective_choice", "ancient_reading") for n in (10, 11, 12)},
                     13: ("reading_subjective", "classical_translation"), 14: ("objective_choice", "poetry_appreciation"),
                     15: ("reading_subjective", "poetry_appreciation"), 16: ("memorization", "classical_memorization"),
                     **{n: ("language_use", "language_application") for n in range(17, 22)}, 22: ("writing", "topic_writing")},
        "material_groups": [("01", 1, 3), ("02", 4, 6), ("03", 7, 9), ("04", 10, 13), ("05", 14, 15)],
    } for y in range(2021, 2025)},
}

SECTION_MAP: dict[int, str] = {
    **{n: "一" for n in range(1, 5)},
    **{n: "二" for n in range(5, 8)},
    **{n: "三" for n in range(8, 11)},
    **{n: "四" for n in range(11, 14)},
    **{n: "五" for n in range(14, 18)},
    **{n: "六" for n in range(18, 21)},
    21: "七",
}

MATERIAL_MAP: dict[int, str | None] = {
    5: "MAT-2008-SC-01", 6: "MAT-2008-SC-01", 7: "MAT-2008-SC-01",
    8: "MAT-2008-SC-02", 9: "MAT-2008-SC-02", 10: "MAT-2008-SC-02",
    11: "MAT-2008-SC-02", 12: "MAT-2008-SC-03",
    14: "MAT-2008-SC-04", 15: "MAT-2008-SC-04", 16: "MAT-2008-SC-04",
    17: "MAT-2008-SC-04", 18: "MAT-2008-SC-05",
}

SUSPICIOUS = (
    "郑波", "握得", "仲足", "苏武《念奴娇", "屋舍伊然", "第ⅡI卷",
    "擢得", "仰足", "市景", "时先", "关与宜人", "源脱水雾", "激伦清光",
    "水寥花", "碗蜒", "井说说", "先阴如箭", "很关", "生活。 人", "变成石油的过程中，其自身的损耗",
)
PRINT_TYPO_CANDIDATES = {
    "郑波", "市景", "时先", "关与宜人", "源脱水雾", "激伦清光", "水寥花", "碗蜒",
    "先阴如箭", "很关",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def norm(text: str) -> str:
    return re.sub(r"\s+", "", text).replace("／", "/")


def flatten_text(value: Any) -> list[str]:
    out: list[str] = []
    if isinstance(value, dict):
        if isinstance(value.get("content"), str):
            out.append(value["content"])
        if isinstance(value.get("text"), str):
            out.append(value["text"])
        for v in value.values():
            if isinstance(v, (dict, list)):
                out.extend(flatten_text(v))
    elif isinstance(value, list):
        for v in value:
            out.extend(flatten_text(v))
    return out


def layout_pages(layout_path: Path) -> list[dict[str, Any]]:
    data = json.loads(layout_path.read_text(encoding="utf-8"))
    pages = []
    for idx, page in enumerate(data.get("pdf_info", [])):
        blocks = page.get("preproc_blocks", [])
        texts = []
        for block in blocks:
            texts.extend(flatten_text(block))
        pages.append({
            "pdf_page_index": idx,
            "printed_page_no": idx + 1 if idx < 6 else None,
            "text": "\n".join(t for t in texts if t),
            "block_ids": [f"P{idx + 1}-B{b.get('index')}" for b in blocks if b.get("index") is not None],
            "bboxes": {f"P{idx + 1}-B{b.get('index')}": b.get("bbox") for b in blocks if b.get("index") is not None},
        })
    return pages


def find_page_starts(raw_lines: list[str], pages: list[dict[str, Any]]) -> tuple[dict[int, int], list[dict[str, Any]]]:
    starts: dict[int, int] = {}
    audit: list[dict[str, Any]] = []
    cursor = 0
    for page in pages:
        page_norm = norm(page["text"])
        candidates = [norm(x) for x in page["text"].splitlines() if len(norm(x)) >= 12]
        anchor = candidates[0] if candidates else ""
        found = None
        matched = False
        if anchor:
            for i in range(cursor, len(raw_lines)):
                if anchor[:24] in norm(raw_lines[i]):
                    found = i
                    matched = True
                    break
        if found is None and page_norm:
            # A fallback for OCR line wrapping: use a distinctive 16-char token.
            token = page_norm[:16]
            for i in range(cursor, len(raw_lines)):
                if token in norm("".join(raw_lines[i:i + 3])):
                    found = i
                    matched = True
                    break
        if found is None:
            found = cursor
        starts[page["pdf_page_index"]] = found
        cursor = found + 1
        audit.append({"pdf_page_index": page["pdf_page_index"], "raw_line_start": found + 1,
                      "anchor": anchor[:80], "status": "matched" if matched else "fallback"})
    return starts, audit


def page_for_line(line_no: int, starts: dict[int, int]) -> int:
    active = 0
    for page, start in sorted(starts.items(), key=lambda x: x[1]):
        if line_no >= start:
            active = page
        else:
            break
    return active


def question_spans(lines: list[str], *, stop_at_answer: bool = False,
                   expected_ids: list[int] | None = None) -> list[dict[str, Any]]:
    """Find top-level question starts in OCR text.

    Old Sichuan scans frequently put Q3/Q4 or Q6/Q7 in one OCR line and may
    drop a marker entirely.  A global regex therefore produces false markers
    from years, scores and advertisements.  We walk the expected sequence and
    accept inline markers only when they are the next expected ID; a missing Q4
    is inferred from the next option block and explicitly flagged in the span.
    """
    limit = expected_ids or list(range(1, 22))
    starts: list[tuple[int, int, int, str]] = []
    # Ignore front-matter instructions whose numbered bullets otherwise look
    # exactly like Q1/Q2.  The first section heading is a stable old-paper
    # anchor even when the Roman-volume heading is OCR-damaged.
    cursor = next((i + 1 for i, line in enumerate(lines)
                   if re.match(r"^\s*#{0,3}\s*一\s*[、．.]", line)), 0)
    for expected in limit:
        found: tuple[int, int, str] | None = None
        marker = re.compile(rf"(?<!\d)({expected})\s*(?:[.．、)](?!\d)|(?=根据|下列|把第|阅读|用斜线|简要|请))")
        line_marker = re.compile(rf"^\s*#{{0,3}}\s*({expected})\s*[.．、)]")
        for i in range(cursor, len(lines)):
            if stop_at_answer and ANSWER_TITLE.search(lines[i]):
                break
            m = line_marker.search(lines[i]) or marker.search(lines[i])
            if m:
                found = (i, m.start(), "explicit")
                break
        if found is None and expected == 6:
            # 2012 blank OCR renders the Q6 marker as ``0.``.
            for i in range(cursor, len(lines)):
                if re.search(r"(?<!\d)0\s*[.．、]\s*(?:下列|以下)", lines[i]):
                    found = (i, re.search(r"(?<!\d)0\s*[.．、]", lines[i]).start(), "ocr_zero_for_six")
                    break
        if found is None and expected == 4 and 3 in [x[1] for x in starts]:
            # 2011 blank Q4 has no printed number: after Q3's D option, the
            # next A option begins the missing question.
            q3 = next(x for x in starts if x[1] == 3)
            d_seen = bool(re.search(r"D\s*[、.]", lines[q3[0]]))
            for i in range(q3[0] + 1, len(lines)):
                if re.search(r"(?:^|\s)D\s*[、.]", lines[i]):
                    d_seen = True
                if d_seen and re.match(r"^\s*A\s*[、.]", lines[i]):
                    found = (i, 0, "inferred_missing_marker")
                    break
        if found is None:
            continue
        starts.append((found[0], expected, found[1], found[2]))
        cursor = found[0]
    # retain first occurrence for each ID; answer/解析 sections often repeat
    # the question paper and must not replace the primary question span.
    unique: list[tuple[int, int, int, str]] = []
    seen: set[int] = set()
    for item in starts:
        if item[1] not in seen:
            unique.append(item)
            seen.add(item[1])
    spans = []
    for pos, (start, q, offset, detection) in enumerate(unique):
        end = unique[pos + 1][0] if pos + 1 < len(unique) else len(lines)
        next_item = unique[pos + 1] if pos + 1 < len(unique) else None
        # Interstitial material for the next big question lies between the
        # previous numbered question and the next numbered question.  Stop at
        # the next section heading so Q4/Q7/Q10/Q13/Q17/Q20 do not absorb the
        # following passage or卷面说明.
        for i in range(start + 1, end):
            if AD_TITLE.search(lines[i]):
                end = i
                break
            if stop_at_answer and ANSWER_TITLE.search(lines[i]):
                end = i
                break
            if SECTION.match(lines[i]) or VOLUME_TITLE.match(lines[i]):
                end = i
                break
        if next_item is not None and next_item[0] == start:
            # Two top-level markers share one OCR line (e.g. Q6/Q7).  Keep
            # the prefix with the earlier question and the suffix with the
            # later one.
            prefix = lines[start][offset:next_item[2]] if offset <= next_item[2] else lines[start][offset:]
            text = prefix.strip()
        else:
            text = "\n".join(lines[start:end]).strip()
        if detection in ("explicit", "ocr_zero_for_six") and offset > 0:
            # Keep the complete OCR line in the preceding span only when this
            # is the first marker; for inline Q4/Q7 split at the marker.
            text = "\n".join([lines[start][offset:]] + lines[start + 1:end]).strip()
        spans.append({"question_id": q, "line_start": start, "line_end": end,
                      "text": text, "detection": detection})
    return spans


def clean_source(raw_lines: list[str], pages: list[dict[str, Any]], starts: dict[int, int]) -> tuple[list[str], list[dict[str, Any]], dict[int, int]]:
    events: list[dict[str, Any]] = []
    clean: list[str] = []
    clean_page: dict[int, int] = {}
    ad_seen = False
    ad_pages = {
        p["pdf_page_index"] for p in pages
        if any(marker in p["text"] for marker in ("资料提供形式", "雪山学社", "XSWK21", "低价正版教辅"))
    }
    ad_page_has_inline_marker: dict[int, bool] = {}
    for raw_no, raw in enumerate(raw_lines):
        page = page_for_line(raw_no, starts)
        ad_page_has_inline_marker[page] = ad_page_has_inline_marker.get(page, False) or any(
            marker in raw for marker in ("资料提供形式", "雪山学社", "XSWK21", "低价正版教辅")
        )
    ad_started_pages: set[int] = set()
    for raw_no, raw in enumerate(raw_lines):
        page = page_for_line(raw_no, starts)
        text = raw.rstrip()
        if page in ad_pages:
            if AD_TITLE.search(text) or any(marker in text for marker in ("雪山学社", "XSWK21", "低价正版教辅")):
                ad_started_pages.add(page)
            if page in ad_started_pages or not ad_page_has_inline_marker.get(page, False):
                if not ad_seen:
                    events.append({"action": "isolate_advertisement", "raw_line_start": raw_no + 1,
                                   "reason": "layout page is outside printed exam or promotional marker"})
                    ad_seen = True
                continue
        if AD_TITLE.search(text):
            if not ad_seen:
                events.append({"action": "isolate_advertisement", "raw_line_start": raw_no + 1,
                               "reason": "layout page is outside printed exam or promotional marker"})
                ad_seen = True
            continue
        if NOISE_LINE.match(text):
            events.append({"action": "remove_noise_line", "raw_line_start": raw_no + 1,
                           "raw_text": text, "reason": "isolated watermark/page-number OCR residue"})
            continue
        if text.strip() == "第ⅡI卷":
            events.append({"action": "normalize_heading", "raw_line_start": raw_no + 1,
                           "raw_text": text, "clean_text": "第II卷", "reason": "OCR mixed Roman numeral"})
            text = text.replace("第ⅡI卷", "第II卷")
        # Remove isolated watermark characters that MinerU sometimes appends
        # to an otherwise valid line (for example ``... 1 Z`` or ``... 不X``).
        # Tokens are removed only when whitespace-delimited; embedded digits or
        # letters in legitimate words are never touched.
        inline = re.sub(r"(?<=\s)(?:1|7|Z|V|N|Q|不X|不x)(?=\s|$|[①②③④⑤⑥])", "", text)
        inline = re.sub(r"(?<=[。！？：；，、])(?:1|7|Z|V|N|Q)(?=$|[①②③④⑤⑥\s])", "", inline)
        inline = re.sub(r"[ \t]{2,}", " ", inline).rstrip()
        if inline != text:
            events.append({"action": "remove_inline_noise", "raw_line_start": raw_no + 1,
                           "raw_text": text, "clean_text": inline,
                           "reason": "whitespace-delimited watermark/page-number OCR residue"})
            text = inline
        if text.strip():
            clean_page[len(clean)] = page
        clean.append(text)
    # Keep page markers out of the content parser but put them into the clean MD.
    return clean, events, clean_page


def add_page_markers(lines: list[str], starts: dict[int, int]) -> list[str]:
    # The clean copy already records page mapping in the ledger.  Page comments
    # are inserted only at known raw boundaries where a line survives cleaning.
    return lines


def clean_page_for_line(line_no: int, clean_page: dict[int, int]) -> int:
    """Return the nearest page assignment for a clean-copy line index."""
    if line_no in clean_page:
        return clean_page[line_no]
    prior = [n for n in clean_page if n <= line_no]
    return clean_page[max(prior)] if prior else 0


def source_links(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def frontmatter(meta: dict[str, Any]) -> str:
    return "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in meta.items()) + "\n---\n\n"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def record_exceptions(text: str, *, source_role: str, source_md: str, qid: int | None = None) -> list[dict[str, Any]]:
    rows = []
    for token in SUSPICIOUS:
        for m in re.finditer(re.escape(token), text):
            printed_typo = token in PRINT_TYPO_CANDIDATES
            rows.append({"source_role": source_role, "source_md": source_md, "question_id": qid,
                         "token": token, "char_offset": m.start(),
                         "status": "source_print_typo_candidate" if printed_typo else "needs_review",
                         "rule": ("保留原卷字样；疑似原卷印刷/题面问题，不能按OCR静默改正" if printed_typo else "OCR candidate; raw text retained and no silent correction")})
    return rows


def build_answer_index(answer_text: str, *, exam_id: str, raw_path: Path, pdf_path: Path,
                       question_ids: list[int] | None = None) -> list[dict[str, Any]]:
    """Create a stable per-question answer/analysis pointer without asserting authority."""
    objective: dict[int, str] = {}
    for m in re.finditer(r"(?<!\d)(\d{1,2})\s*[.．、]\s*([A-D])", answer_text):
        qid, choice = int(m.group(1)), m.group(2)
        if 1 <= qid <= 10:
            objective[qid] = choice
    lines = answer_text.splitlines()
    section_headings = {}
    section_positions = []
    for line in lines:
        m = re.match(r"^\s*#{1,3}\s*([一二三四五六七八九十]+)[、．.]", line)
        if m:
            section_headings.setdefault(m.group(1), line.strip())
    for i, line in enumerate(lines):
        m = re.match(r"^\s*#{1,3}\s*([一二三四五六七八九十]+)[、．.]", line)
        if m:
            section_positions.append((i, m.group(1)))
    anchors: dict[int, int] = {}
    for i, line in enumerate(lines):
        m = re.match(r"^\s*#{0,2}\s*(\d{1,2})\s*[.．、)]\s*(?:（|\()", line)
        if m and 1 <= int(m.group(1)) <= 21:
            anchors.setdefault(int(m.group(1)), i)
    rows = []
    for qid in (question_ids or list(range(1, 22))):
        if qid in objective:
            text = objective[qid]
            answer_section = "一" if qid <= 4 else "二" if qid <= 7 else "三"
            anchor = section_headings.get(answer_section, f"参考答案§{answer_section}")
            analysis = None
            section_id = answer_section
        elif qid in anchors:
            start = anchors[qid]
            following = [i for n, i in anchors.items() if i > start]
            end = min(following) if following else len(lines)
            for i in range(start + 1, end):
                if SECTION.match(lines[i]) or VOLUME_TITLE.match(lines[i]):
                    end = i
                    break
            text = "\n".join(lines[start:end]).strip()
            text = re.sub(r"\s*(?:#{0,2}\s*)?[一二三四五六七八九十]+、[（(]\s*\d+分[）)]\s*$", "", text).rstrip()
            anchor = lines[start].strip()
            analysis = text
            prior_sections = [sec for pos, sec in section_positions if pos <= start]
            section_id = SECTION_MAP.get(qid, prior_sections[-1] if prior_sections else None)
        else:
            text = ""
            anchor = None
            analysis = None
            section_id = None
        rows.append({
            "answer_pair_id": f"{exam_id}-Q{qid:03d}",
            "exam_id": exam_id,
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "source_status": "unverified_local_provided",
            "answer_status": "candidate_unverified" if text else "N/A",
            "answer_text": text,
            "analysis_text": analysis,
            "analysis_status": "not_present_in_source_bundle" if analysis is None else "candidate_unverified",
            "answer_anchor": anchor,
            "answer_section_id": section_id,
            "source_mineru_md": source_links(raw_path),
            "source_pdf": source_links(pdf_path),
            "answer_bundle_path": source_links(OUT / exam_id / "answers" / "answer_bundle.md"),
            "review_status": "needs_source_verification",
        })
    return rows


def process_record(record: dict[str, Any], *, force: bool = False) -> dict[str, Any]:
    year = int(record["year"])
    cfg = EXAM_CONFIGS.get(year, {"question_ids": list(range(1, 22)), "section_map": SECTION_MAP, "type_map": TYPE_MAP,
                                  "material_groups": []})
    paper_code = record["paper_code"]
    exam_id = f"GK-{paper_code}-{year}"
    role = record["document_role"]
    raw_path = ROOT / record["mineru_full_md"]
    pdf_path = ROOT / record["local_pdf"]
    result_dir = raw_path.parent
    pages = layout_pages(result_dir / "layout.json")
    raw_text = raw_path.read_text(encoding="utf-8", errors="replace")
    raw_lines = raw_text.splitlines()
    starts, page_audit = find_page_starts(raw_lines, pages)
    clean_lines, clean_events, clean_page = clean_source(raw_lines, pages, starts)
    clean_text = "\n".join(clean_lines).strip() + "\n"
    base = OUT / exam_id
    clean_rel = base / "clean_md" / f"{role}.md"
    clean_abs = ROOT / clean_rel
    clean_meta = {
        "schema_version": "exam-clean-0.1",
        "exam_id": exam_id,
        "year": year,
        "paper_code": paper_code,
        "source_role": role,
        "cleaning_status": "pilot_cleaned",
        "raw_full_md": source_links(raw_path),
        "source_pdf": source_links(pdf_path),
        "raw_sha256": sha256_file(raw_path),
        "clean_sha256": sha256_text(clean_text),
        "mineru_page_count": len(pages),
        "printed_exam_page_count": sum(1 for p in pages if p["printed_page_no"] is not None),
        "ad_pages_isolated": [p["pdf_page_index"] + 1 for p in pages
                              if any(marker in p["text"] for marker in ("资料提供形式", "雪山学社", "XSWK21", "低价正版教辅"))],
    }
    body = (frontmatter(clean_meta) +
            f"原始 MinerU：[[{source_links(raw_path)}|full.md]] ；原始 PDF：[[{source_links(pdf_path)}|PDF]]\n\n" +
            "> 清洗副本。原始 `full.md` 不改写；疑似 OCR 错字保留并登记到 `exceptions.jsonl`。\n\n" +
            clean_text)
    if force or not clean_abs.exists():
        write(clean_abs, body)

    # Parse both the raw question portion and the clean question portion.
    raw_spans = question_spans(raw_lines, stop_at_answer=(role == "analysis"), expected_ids=cfg["question_ids"])
    clean_spans = question_spans(clean_lines, stop_at_answer=(role == "analysis"), expected_ids=cfg["question_ids"])
    raw_by_q = {x["question_id"]: x for x in raw_spans}
    clean_by_q = {x["question_id"]: x for x in clean_spans}
    segment_rows: list[dict[str, Any]] = []
    material_rows: list[dict[str, Any]] = []
    qroot = base / "segments" / role

    # Materials are independent retrievable objects.  The 2008 calibration
    # slice has five stable stimuli; later years may add/merge materials after
    # manual review rather than inheriting these hard-coded boundaries.
    if role == "question" and year == 2008:
        section_line = {}
        for i, line in enumerate(clean_lines):
            m = SECTION.match(line)
            if m:
                section_line[m.group(1)] = i
        material_ranges = {
            "MAT-2008-SC-01": (section_line.get("二", 0), clean_by_q.get(5, {"line_start": len(clean_lines)})["line_start"]),
            "MAT-2008-SC-02": (section_line.get("三", 0), clean_by_q.get(8, {"line_start": len(clean_lines)})["line_start"]),
            "MAT-2008-SC-03": (clean_by_q.get(12, {"line_start": 0})["line_start"], clean_by_q.get(13, {"line_start": len(clean_lines)})["line_start"]),
            "MAT-2008-SC-04": (section_line.get("五", 0), clean_by_q.get(14, {"line_start": len(clean_lines)})["line_start"]),
            "MAT-2008-SC-05": (clean_by_q.get(18, {"line_start": 0})["line_start"] + 1, clean_by_q.get(19, {"line_start": len(clean_lines)})["line_start"]),
        }
        q12_start = material_ranges["MAT-2008-SC-03"][0]
        poem_start = next((i for i in range(q12_start, material_ranges["MAT-2008-SC-03"][1]) if clean_lines[i].lstrip().startswith("## [")), q12_start)
        poem_end = next((i for i in range(poem_start + 1, material_ranges["MAT-2008-SC-03"][1]) if re.match(r"^\s*[（(]1[）)]", clean_lines[i])), material_ranges["MAT-2008-SC-03"][1])
        material_ranges["MAT-2008-SC-03"] = (poem_start, poem_end)
        for material_id, (mstart, mend) in material_ranges.items():
            mtext = "\n".join(clean_lines[mstart:mend]).strip()
            if not mtext:
                continue
            pstart = clean_page_for_line(mstart, clean_page)
            pend = clean_page_for_line(max(mstart, mend - 1), clean_page)
            mrel = base / "materials" / f"{material_id}.md"
            mabs = ROOT / mrel
            mmeta = {
                "schema_version": "exam-material-0.1",
                "material_id": material_id,
                "exam_id": exam_id,
                "source_role": "question_material",
                "material_kind": "stimulus",
                "source_pdf": source_links(pdf_path),
                "source_mineru_md": source_links(raw_path),
                "source_clean_md": source_links(clean_abs),
                "source_pdf_page_start": pstart + 1,
                "source_pdf_page_end": pend + 1,
                "source_block_ids": [bid for p in pages if p["pdf_page_index"] in range(pstart, pend + 1) for bid in p["block_ids"]],
                "source_bbox_json": {bid: p["bboxes"].get(bid) for p in pages if p["pdf_page_index"] in range(pstart, pend + 1) for bid in p["block_ids"]},
                "source_locator_status": "page_level_fallback",
                "material_clean_sha256": sha256_text(mtext),
                "review_status": "needs_manual_review",
            }
            mbody = frontmatter(mmeta) + f"- 清洗整卷：[[{source_links(clean_abs)}|question.md]]\n- 原始 MinerU：[[{source_links(raw_path)}|full.md]]\n- 原始 PDF：[[{source_links(pdf_path)}|PDF]]\n\n---\n\n{mtext}\n"
            if force or not mabs.exists():
                write(mabs, mbody)
            material_rows.append({**mmeta, "material_path": source_links(mabs), "clean_text": mtext})

    # Generic material extraction for 2009--2015.  Boundaries are deliberately
    # conservative: begin at the nearest section/reading heading before the
    # first linked question and end at the next linked question.  This keeps
    # stimuli retrievable without pretending OCR gives exact paragraph boxes.
    if role == "question" and year != 2008 and cfg.get("material_groups"):
        heading_re = re.compile(r"^\s*#{0,3}\s*[一二三四五六七八九十]+\s*[、．.]\s*")
        for gid, lo, hi in cfg["material_groups"]:
            if lo not in clean_by_q:
                continue
            start_q = clean_by_q[lo]["line_start"]
            next_q = min((clean_by_q[n]["line_start"] for n in cfg["question_ids"] if n > hi and n in clean_by_q), default=len(clean_lines))
            mstart = next((i for i in range(start_q, -1, -1) if heading_re.match(clean_lines[i]) or "阅读下面" in clean_lines[i]), start_q)
            mend = next_q
            mtext = "\n".join(clean_lines[mstart:mend]).strip()
            if not mtext:
                continue
            pstart = clean_page_for_line(mstart, clean_page)
            pend = clean_page_for_line(max(mstart, mend - 1), clean_page)
            mat_id = f"MAT-{year}-SC-{gid}"
            mrel = base / "materials" / f"{mat_id}.md"
            mabs = ROOT / mrel
            mmeta = {
                "schema_version": "exam-material-0.1", "material_id": mat_id,
                "exam_id": exam_id, "source_role": "question_material", "material_kind": "stimulus",
                "source_pdf": source_links(pdf_path), "source_mineru_md": source_links(raw_path),
                "source_clean_md": source_links(clean_abs), "source_pdf_page_start": pstart + 1,
                "source_pdf_page_end": pend + 1, "source_locator_status": "page_level_fallback",
                "material_clean_sha256": sha256_text(mtext), "review_status": "needs_manual_review",
                "linked_question_ids": [f"{exam_id}-Q{n:03d}" for n in cfg["question_ids"] if lo <= n <= hi],
            }
            mbody = frontmatter(mmeta) + f"- 清洗整卷：[[{source_links(clean_abs)}|question.md]]\n- 原始 MinerU：[[{source_links(raw_path)}|full.md]]\n- 原始 PDF：[[{source_links(pdf_path)}|PDF]]\n\n---\n\n{mtext}\n"
            if force or not mabs.exists():
                write(mabs, mbody)
            material_rows.append({**mmeta, "material_path": source_links(mabs), "clean_text": mtext})

    for qid in cfg["question_ids"]:
        missing_marker = qid not in clean_by_q
        if missing_marker:
            # Do not manufacture text when the OCR layer omits a top-level
            # marker (2022 Q6 and 2024 analysis Q21 are known examples).  A
            # canonical placeholder preserves the expected ID and routes the
            # item to PDF/manual review.
            c = {"line_start": 0, "line_end": 0,
                 "text": f"[{exam_id}-Q{qid:03d}：MinerU 文本层未出现可定位题号/题文，需回看原始 PDF]"}
        else:
            c = clean_by_q[qid]
        r = raw_by_q.get(qid, {"text": "", "line_start": None, "line_end": None})
        typel1, typel2 = cfg["type_map"].get(qid, ("uncertain", "uncertain"))
        section = cfg["section_map"].get(qid, "unknown")
        page_start = clean_page_for_line(c["line_start"], clean_page)
        page_end = clean_page_for_line(max(c["line_start"], c["line_end"] - 1), clean_page)
        page_slice = list(range(page_start, page_end + 1))
        block_ids: list[str] = []
        bboxes: dict[str, Any] = {}
        for p in pages:
            if p["pdf_page_index"] in page_slice:
                block_ids.extend(p["block_ids"])
                bboxes.update(p["bboxes"])
        qkey = f"Q{qid:03d}"
        seg_rel = qroot / f"{qkey}.md"
        seg_abs = ROOT / seg_rel
        canonical = f"{exam_id}-{qkey}"
        blank_link = base / "segments" / "question" / f"{qkey}.md"
        analysis_link = base / "segments" / "analysis" / f"{qkey}.md"
        answer_link = base / "answers" / "answer_bundle.md"
        seg_meta = {
            "schema_version": "exam-question-0.1",
            "canonical_question_id": canonical,
            "exam_id": exam_id,
            "question_id": qid,
            "source_role": role,
            "section_id": section,
            "question_type_l1": typel1,
            "question_type_l2": typel2,
            "material_id": (f"MAT-{year}-SC-{next((gid for gid, lo, hi in cfg.get('material_groups', []) if lo <= qid <= hi), None)}"
                            if next((gid for gid, lo, hi in cfg.get('material_groups', []) if lo <= qid <= hi), None) else None),
            "source_pdf": source_links(pdf_path),
            "source_mineru_md": source_links(raw_path),
        "source_clean_md": source_links(clean_abs),
            "source_pdf_page_start": page_start + 1,
            "source_pdf_page_end": page_end + 1,
            "source_pdf_page_index_start": page_start,
            "source_pdf_page_index_end": page_end,
            "printed_page_no_start": pages[page_start]["printed_page_no"],
            "printed_page_no_end": pages[page_end]["printed_page_no"],
            "source_block_ids": block_ids,
            "source_bbox_json": bboxes,
            "source_locator_status": "page_level_fallback",
            "segment_clean_sha256": sha256_text(c["text"]),
            "raw_segment_sha256": sha256_text(r["text"]),
            "cleaning_status": "pilot_cleaned",
            "segmentation_status": "missing_source_marker" if missing_marker else "pilot_segmented",
            "type_confidence": 0.0 if missing_marker else 0.95,
            "review_status": "needs_pdf_review" if missing_marker else "needs_manual_review",
            "related_question_ids": [f"{exam_id}-Q{n:03d}" for n in cfg["question_ids"]
                                      if (next((gid for gid, lo, hi in cfg.get('material_groups', []) if lo <= n <= hi), None)
                                          == next((gid for gid, lo, hi in cfg.get('material_groups', []) if lo <= qid <= hi), None)) and n != qid],
            "raw_line_start": (r.get("line_start") or 0) + 1,
            "raw_line_end": r.get("line_end") or 0,
        }
        links = (f"- 清洗整卷：[[{source_links(clean_abs)}|{role}.md]]\n"
                 f"- 原始 MinerU：[[{source_links(raw_path)}|full.md]]\n"
                 f"- 原始 PDF：[[{source_links(pdf_path)}|PDF]]\n")
        if role == "question":
            links += f"- 对应解析卷题目：[[{source_links(analysis_link)}|解析卷 {qkey}]]\n"
        else:
            answer_index_link = base / "answers" / "answer_index.jsonl"
            links += f"- 对应空白卷题目：[[{source_links(blank_link)}|空白卷 {qkey}]]\n- 答案/解析：[[{source_links(answer_link)}|答案解析汇总]]\n- 逐题答案索引：[[{source_links(answer_index_link)}|answer_index.jsonl]]\n"
        mat_group = next((gid for gid, lo, hi in cfg.get("material_groups", []) if lo <= qid <= hi), None)
        if mat_group:
            mat_id = f"MAT-{year}-SC-{mat_group}"
            mat_path = base / "materials" / f"{mat_id}.md"
            links += f"- 阅读材料：[[{source_links(mat_path)}|{mat_id}]]\n"
        seg_body = frontmatter(seg_meta) + links + "\n---\n\n" + c["text"].strip() + "\n"
        if force or not seg_abs.exists():
            write(seg_abs, seg_body)
        row = dict(seg_meta)
        row.update({"segment_path": source_links(seg_abs), "raw_text": r["text"], "clean_text": c["text"]})
        segment_rows.append(row)

    # The analysis answer bundle is intentionally separate from question text.
        if role == "analysis":
            seg_meta["answer_index_path"] = source_links(base / "answers" / "answer_index.jsonl")
        answer_start = next((i for i, line in enumerate(clean_lines) if ANSWER_TITLE.search(line)), None)
        if answer_start is not None:
            answer_lines = clean_lines[answer_start:]
            answer_clean = "\n".join(answer_lines).strip() + "\n"
            ans_rel = base / "answers" / "answer_bundle.md"
            ans_meta = {
                "schema_version": "exam-answer-0.1",
                "exam_id": exam_id,
                "source_role": "answer_scoring_candidate",
                "source_status": "unverified_local_provided",
                "raw_full_md": source_links(raw_path),
                "source_pdf": source_links(pdf_path),
                "answer_clean_sha256": sha256_text(answer_clean),
                "review_status": "needs_source_verification",
            }
            ans_body = frontmatter(ans_meta) + f"原始解析 MinerU：[[{source_links(raw_path)}|full.md]]；原始 PDF：[[{source_links(pdf_path)}|PDF]]\n\n" + answer_clean
            if force or not (ROOT / ans_rel).exists():
                write(ROOT / ans_rel, ans_body)
            answer_index = build_answer_index(answer_clean, exam_id=exam_id, raw_path=raw_path, pdf_path=pdf_path,
                                              question_ids=cfg["question_ids"])
            write(ROOT / base / "answers" / "answer_index.jsonl", "\n".join(json.dumps(r, ensure_ascii=False) for r in answer_index) + "\n")

    exceptions = list(clean_events)
    for row in segment_rows:
        exceptions.extend(record_exceptions(row["raw_text"], source_role=role, source_md=source_links(raw_path), qid=row["question_id"]))
    if role == "analysis":
        answer_file = base / "answers" / "answer_bundle.md"
        if (ROOT / answer_file).exists():
            exceptions.extend(record_exceptions((ROOT / answer_file).read_text(encoding="utf-8"), source_role="answer_scoring_candidate", source_md=source_links(raw_path), qid=None))
    for row in exceptions:
        row.setdefault("exam_id", exam_id)
    return {
        "exam_id": exam_id, "year": year, "paper_code": paper_code, "source_role": role,
        "raw_full_md": source_links(raw_path), "source_pdf": source_links(pdf_path),
        "raw_sha256": sha256_file(raw_path), "clean_sha256": sha256_text(clean_text),
        "raw_line_count": len(raw_lines), "clean_line_count": len(clean_lines),
        "mineru_page_count": len(pages), "question_count": len(segment_rows),
        "question_ids": [x["question_id"] for x in segment_rows],
        "page_audit": page_audit, "clean_events": clean_events,
        "segment_rows": segment_rows, "exceptions": exceptions,
        "material_rows": material_rows,
    }


def write_indexes(result: dict[str, Any], *, force: bool = False) -> None:
    base = OUT / result["exam_id"]
    ledger_rel = base / "ledger" / f"questions-{result['source_role']}.jsonl"
    rows = result["segment_rows"]
    write(ROOT / ledger_rel, "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    exc_rel = base / "review" / f"exceptions-{result['source_role']}.jsonl"
    write(ROOT / exc_rel, "\n".join(json.dumps(r, ensure_ascii=False) for r in result["exceptions"]) + ("\n" if result["exceptions"] else ""))
    page_rel = base / "ledger" / f"pages-{result['source_role']}.json"
    write(ROOT / page_rel, json.dumps({"exam_id": result["exam_id"], "page_audit": result["page_audit"]}, ensure_ascii=False, indent=2) + "\n")
    mat_rel = base / "ledger" / "materials.jsonl"
    write(ROOT / mat_rel, "\n".join(json.dumps(r, ensure_ascii=False) for r in result.get("material_rows", [])) + ("\n" if result.get("material_rows") else ""))
    # Indexes contain links only; canonical question text remains in segments/.
    by_type: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in rows:
        by_type.setdefault((row["question_type_l1"], row["question_type_l2"]), []).append(row)
    for (l1, l2), group in sorted(by_type.items()):
        rel = base / "by_type" / l1 / f"{l2}.md"
        content = f"# {result['exam_id']} · {l1} · {l2}\n\n"
        content += "> 题型归并索引只保存双链，不复制题目正文。\n\n"
        content += "| 题号 | 题目文件 | 解析文件 | 页码 | 置信度 |\n|---|---|---|---:|---:|\n"
        for row in group:
            q = f"Q{row['question_id']:03d}"
            qlink = source_links(ROOT / base / "segments" / "question" / f"{q}.md")
            alink = source_links(ROOT / base / "segments" / "analysis" / f"{q}.md")
            content += f"| {q} | [[{qlink}|空白卷]] | [[{alink}|解析卷]] | {row['source_pdf_page_start']}–{row['source_pdf_page_end']} | {row['type_confidence']:.2f} |\n"
        write(ROOT / rel, content)
    report_rel = base / "review" / "segmentation_report.md"
    report = f"# {result['exam_id']} 题目级分割试点报告\n\n"
    report += f"- 来源角色：`{result['source_role']}`\n- 题目编号覆盖：{result['question_ids']}\n- 本角色题目数：{result['question_count']}\n"
    report += f"- MinerU 页数：{result['mineru_page_count']}；原始行数：{result['raw_line_count']}；清洗行数：{result['clean_line_count']}\n"
    report += f"- 原始 `full.md`：[[{result['raw_full_md']}|full.md]]\n- 原始 PDF：[[{result['source_pdf']}|PDF]]\n\n"
    report += "## 当前门禁\n\n"
    report += "- [x] 原始 full.md 未改写；清洗副本另存。\n- [x] 题卷与解析卷分层；答案/评分单独成 bundle。\n- [x] 题目与清洗稿、MinerU、PDF 双链可回溯。\n"
    if result["source_role"] == "analysis":
        report += "- [x] 解析卷已生成逐题 `answer_index.jsonl`；答案来源仍为未核验候选。\n"
    else:
        report += "- [x] 解析卷对应文件与逐题 `answer_index.jsonl` 已生成。\n"
    report += "- [x] 当前记录显式标记 `source_locator_status=page_level_fallback`，不冒充题级精确 bbox。\n"
    report += "- [ ] OCR 疑似错字逐条人工仲裁。\n- [ ] 2008 空白卷与解析卷页码/版块抽检全部签字。\n- [ ] 通过校准门后批量扩展 2009—2024。\n"
    write(ROOT / report_rel, report)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, action="append", help="year(s), default 2008")
    ap.add_argument("--force", action="store_true", help="overwrite generated derived files")
    args = ap.parse_args()
    years = set(args.year or [2008])
    manifest = json.loads((CORPUS / "manifest.json").read_text(encoding="utf-8"))
    selected = [r for r in manifest["records"] if int(r["year"]) in years]
    if not selected:
        raise SystemExit("no manifest records selected")
    combined: list[dict[str, Any]] = []
    for r in sorted(selected, key=lambda x: (x["year"], x["document_role"])):
        result = process_record(r, force=args.force)
        write_indexes(result, force=args.force)
        combined.append(result)
        print(f"{result['exam_id']} {result['source_role']}: {result['question_count']} questions, {len(result['exceptions'])} review events")
    # Write the combined per-exam ledgers independently when several years are
    # selected in one invocation (the old pilot wrote only the first exam).
    for exam_id in sorted({x["exam_id"] for x in combined}):
        group = [x for x in combined if x["exam_id"] == exam_id]
        base = OUT / exam_id
        all_questions = [row for result in group for row in result["segment_rows"]]
        all_exceptions = [row for result in group for row in result["exceptions"]]
        all_pages = {result["source_role"]: result["page_audit"] for result in group}
        write(ROOT / base / "ledger" / "questions.jsonl", "\n".join(json.dumps(r, ensure_ascii=False) for r in all_questions) + "\n")
        write(ROOT / base / "review" / "exceptions.jsonl", "\n".join(json.dumps(r, ensure_ascii=False) for r in all_exceptions) + "\n")
        write(ROOT / base / "ledger" / "pages.json", json.dumps({"exam_id": exam_id, "roles": all_pages}, ensure_ascii=False, indent=2) + "\n")
    audit = {
        "schema_version": "exam-extract-audit-0.1",
        "years": sorted(years),
        "runs": [{"exam_id": x["exam_id"], "source_role": x["source_role"], "question_count": x["question_count"], "raw_sha256": x["raw_sha256"], "clean_sha256": x["clean_sha256"]} for x in combined],
        "status": "pilot_generated",
    }
    write(OUT / "pilot_audit.json", json.dumps(audit, ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
