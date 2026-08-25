#!/usr/bin/env python3
"""Register a conservative 2015 Sichuan answer-candidate layer.

The downloaded attachment is a third-party New Oriental teaching-group
document linked by gaokao.com.  It contains answers and explanations, not an
exam-authority key or scoring rubric.  This importer only derives bounded
question excerpts; it never edits the main answer index or source PDFs.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015"
SOURCE_DIR = ROOT / "Data/reference/gaokao/external/2015_gaokao_answer"
SOURCE_TEXT = SOURCE_DIR / "answer_source.txt"
SOURCE_HTML = SOURCE_DIR / "source.html"
SOURCE_ZIP = SOURCE_DIR / "answer_bundle.zip"
SOURCE_DOC = next(SOURCE_DIR.glob("*.doc"), None)
OUT = BASE / "answers/reference_answer_candidates.jsonl"
REPORT = ROOT / "work/knowledge/exams/workbench/EXAM-REFERENCE-ANSWER-CANDIDATES-2015.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidates_2015_20260809.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def lines(text: str, start: int, end: int) -> str:
    return "\n".join(text.splitlines()[start - 1:end]).strip()


def answer_line(text: str, number: int) -> tuple[str, str]:
    pattern = rf"(?m)^\s*{number}[．.、]\s*([A-E])"
    match = re.search(pattern, text)
    if not match:
        raise RuntimeError(f"answer marker not found for Q{number}")
    answer = match.group(1)
    return answer, match.group(0).strip()


def row(qid: int, candidate: str, excerpt: str, *, content_type: str,
        source_lines: list[int], notes: list[str]) -> dict:
    return {
        "schema_version": "exam-reference-answer-candidate-0.2",
        "candidate_id": f"GK-SC-2015-Q{qid:03d}-GAOKAO-CANDIDATE",
        "exam_id": "GK-SC-2015",
        "question_id": qid,
        "source_role": "answer_scoring_candidate",
        "candidate_status": "candidate_unverified",
        "candidate_scope": "third_party_gaokao_com_answer_attachment",
        "source_authority_status": "unverified_third_party_reprint",
        "source_registry_id": "SRC-GK-2015-SC-GAOKAO-ANSWER-CANDIDATE",
        "source_status": "unverified_third_party_reprint",
        "answer_source_status": "external_candidate",
        "scoring_status": "not_available_as_official",
        "mapping_level": "M0",
        "kp_id": "N/A",
        "candidate_content_type": content_type,
        "answer_candidate_text": candidate,
        "answer_candidate_sha256": sha_text(candidate),
        "source_group_excerpt": excerpt,
        "source_group_excerpt_sha256": sha_text(excerpt),
        "source_line_start": source_lines[0],
        "source_line_end": source_lines[1],
        "source_html": rel(SOURCE_HTML),
        "source_html_sha256": sha(SOURCE_HTML),
        "source_zip": rel(SOURCE_ZIP),
        "source_zip_sha256": sha(SOURCE_ZIP),
        "source_doc": rel(SOURCE_DOC) if SOURCE_DOC else None,
        "source_doc_sha256": sha(SOURCE_DOC) if SOURCE_DOC else None,
        "source_text": rel(SOURCE_TEXT),
        "source_text_sha256": sha(SOURCE_TEXT),
        "source_url": "https://www.gaokao.com/e/20150613/557bec4d3943a.shtml",
        "attachment_url": "https://files.eduuu.com/ohr/2015/06/13/163913_557bec3147bf1.zip",
        "source_answer_index": rel(BASE / "answers/answer_index.jsonl"),
        "review_status": "needs_independent_review",
        "notes": notes,
    }


def main() -> int:
    required = [SOURCE_TEXT, SOURCE_HTML, SOURCE_ZIP]
    if SOURCE_DOC:
        required.append(SOURCE_DOC)
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise SystemExit("missing source artifacts: " + ", ".join(missing))
    text = SOURCE_TEXT.read_text(encoding="utf-8-sig")
    rows: list[dict] = []

    # Q1--Q7 each have a compact answer marker in the source document.
    marker_positions = list(re.finditer(r"(?m)^\s*答案[:：]\s*([A-E]+)", text))
    if len(marker_positions) < 7:
        raise RuntimeError(f"expected at least 7 compact answer markers, got {len(marker_positions)}")
    for qid, match in enumerate(marker_positions[:7], start=1):
        candidate = match.group(1)
        line_no = text[:match.start()].count("\n") + 1
        excerpt = match.group(0).strip()
        rows.append(row(qid, candidate, excerpt, content_type="answer_candidate_short",
                        source_lines=[line_no, line_no],
                        notes=["第三方教研组答案/解析附件；仅作候选，不是考试机构发布的官方答案。",
                               "答案行与解析相邻，未将解释字段升级为评分标准。"]))

    # Q8/Q9 are compact answer lines prefixed by their question number.
    for qid, line_no in ((8, 83), (9, 89)):
        candidate, marker = answer_line(text, qid)
        excerpt = lines(text, line_no, line_no)
        rows.append(row(qid, candidate, excerpt, content_type="answer_candidate_short",
                        source_lines=[line_no, line_no],
                        notes=["第三方答案/解析混合段中的题号答案标记；未视为官方答案。" ]))

    groups = {
        10: (97, 103, "translation_answer_candidate", lines(text, 99, 102)),
        11: (104, 107, "scoring_point_guidance_candidate", lines(text, 105, 107)),
        12: (109, 112, "answer_and_translation_candidate", lines(text, 111, 112)),
        13: (114, 126, "response_guidance_candidate", lines(text, 121, 126)),
        14: (129, 146, "memorization_answer_candidate", lines(text, 138, 145)),
        15: (158, 165, "answer_and_explanation_candidate", "AD"),
        16: (167, 170, "reference_answer_candidate", lines(text, 169, 170)),
        17: (172, 179, "reference_answer_candidate", lines(text, 173, 179)),
        18: (181, 185, "reference_answer_candidate", lines(text, 183, 185)),
        19: (188, 191, "response_guidance_candidate", lines(text, 189, 191)),
        20: (193, 195, "response_guidance_candidate", lines(text, 194, 195)),
        21: (198, 209, "essay_prompt_and_guidance_not_scoring", lines(text, 204, 209)),
    }
    for qid, (start, end, content_type, candidate) in groups.items():
        notes = ["来源包含答案、解析、参考答案或示例；候选层不等于官方评分标准。",
                 "题文与候选来源通过 source_line_start/source_line_end 保持可回溯。"]
        if qid == 21:
            notes += ["Q21 仅登记作文题目与审题指导；没有可接受的统一作文答案或评分标准。"]
        if qid in {13, 19, 20}:
            notes += ["该题记录主要是作答指导/示例，不得当作唯一标准答案。"]
        rows.append(row(qid, candidate, lines(text, start, end), content_type=content_type,
                        source_lines=[start, end], notes=notes))

    rows.sort(key=lambda x: x["question_id"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    missing_q = [q for q in range(1, 22) if q not in {r["question_id"] for r in rows}]
    pdf = ROOT / "Data/reference/gaokao/pdf/2015/2015_SC_answer.pdf"
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-reference-answer-candidate-0.2"\n'
        'status: "candidate_only"\n'
        'authority_status: "unverified_third_party_reprint"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2015 四川卷答案/解析候选层\n\n"
        "> 来源为高考网转载页链接的新东方教研组 DOC 附件。Q1—Q20 有答案、参考答案或作答指导候选；Q21 仅有作文审题指导。来源未经考试机构独立核验，不能称为官方答案或评分标准。\n\n"
        f"- 候选覆盖：`{[r['question_id'] for r in rows]}`；显式缺失：`{missing_q}`。\n"
        f"- 来源页：`{rel(SOURCE_HTML)}`（SHA-256 `{sha(SOURCE_HTML)}`）。\n"
        f"- 附件：`{rel(SOURCE_ZIP)}`（SHA-256 `{sha(SOURCE_ZIP)}`）；DOC：`{rel(SOURCE_DOC) if SOURCE_DOC else 'N/A'}`。\n"
        f"- 转文本派生：`{rel(SOURCE_TEXT)}`（SHA-256 `{sha(SOURCE_TEXT)}`）。\n"
        f"- 现有中国教育在线答案 PDF `Data/reference/gaokao/pdf/2015/2015_SC_answer.pdf` 仅为汇总包装页，不作为本候选答案内容。\n"
        f"- 派生 JSONL：`{rel(OUT)}`。\n",
        encoding="utf-8",
    )
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-receipt-0.2",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-SC-2015-20260809",
        "generated_at": now_text(),
        "exam_id": "GK-SC-2015",
        "source_registry_id": "SRC-GK-2015-SC-GAOKAO-ANSWER-CANDIDATE",
        "source_authority_status": "unverified_third_party_reprint",
        "coverage": {"candidate_questions": [r["question_id"] for r in rows], "missing_questions": missing_q},
        "inputs": {p.name: {"path": rel(p), "sha256": sha(p)} for p in required},
        "output": {"path": rel(OUT), "sha256": sha(OUT), "rows": len(rows)},
        "report": {"path": rel(REPORT), "sha256": sha(REPORT)},
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "第三方答案/解析附件只登记为候选；作文指导、示例和解析不得升级为官方评分标准。",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "candidate_questions": [r["question_id"] for r in rows],
                      "missing_questions": missing_q, "output": rel(OUT), "report": rel(REPORT),
                      "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
