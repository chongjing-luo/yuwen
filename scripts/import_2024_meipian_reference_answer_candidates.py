#!/usr/bin/env python3
"""Snapshot and register the independent Meipian 2024 answer candidate.

This is deliberately an isolated third-party candidate layer.  It never
modifies the source PDF/MinerU outputs or the main ``answer_index.jsonl``.
Q22 is an essay-analysis/writing-guidance excerpt rather than a model essay or
official scoring rubric and is labelled accordingly.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
URL = "https://www.meipian.cn/552rdrkt"
HTML_OUT = ROOT / "Data/reference/gaokao/html/2024/answer_meipian_552rdrkt.html"
OUT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/reference_answer_candidates_meipian.jsonl"
REPORT = ROOT / "work/knowledge/exams/workbench/EXAM-REFERENCE-ANSWER-CANDIDATES-2024-MEIPIAN.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidates_meipian_GK-NCA-2024_20260809.json"
LOCAL_REGISTRY = ROOT / "Data/reference/gaokao/external/2024_meipian_answer/registry_entry.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def fetch_snapshot() -> tuple[bytes, str]:
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=40)
    response.raise_for_status()
    data = response.content
    if len(data) < 1000 or b"552rdrkt" not in data:
        raise RuntimeError("Meipian response is unexpectedly small or not the requested page")
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_bytes(data)
    return data, response.encoding or "utf-8"


def article_text(data: bytes, encoding: str) -> str:
    soup = BeautifulSoup(data.decode(encoding, errors="replace"), "html.parser")
    section = soup.select_one("article section")
    if section is None:
        raise RuntimeError("Meipian article section not found")
    # The article body is HTML-escaped inside the section.  Unescape once,
    # then turn its literal <br>/<h3> tags into stable plain-text boundaries.
    text = html.unescape(section.get_text("", strip=False))
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.I)
    text = text.replace("<h3>", "").replace("</h3>", "\n")
    return text.strip()


def numbered_region(text: str, qid: int, next_qid: int | None, start_at: int = 0) -> tuple[str, int, int]:
    # Q16 in this page is rendered as ``16 ①`` (without a full stop), while
    # the other numbered answers normally use ``16.``.  Accept that one
    # unambiguous answer prefix without broadening the match to prose.
    pattern = re.compile(rf"(?<!\d){qid}(?:[.．]|(?=\s+[①（(]))\s*")
    match = pattern.search(text, start_at)
    if not match:
        raise RuntimeError(f"answer start for Q{qid} not found")
    end = len(text)
    if next_qid is not None:
        next_match = re.compile(rf"(?<!\d){next_qid}(?:[.．]|(?=\s+[①（(]))\s*").search(text, match.end())
        if next_match:
            end = next_match.start()
    return text[match.end():end].strip(), match.start(), end


def build_groups(text: str) -> dict[int, tuple[str, str]]:
    """Return qid -> (candidate text, shared source answer excerpt)."""
    # Each answer group ends at its following explicit 【解析】 marker.  The
    # first group is split into Q1-3 and Q4-6 by the second marker.
    answer_markers = [m for m in re.finditer(r"【答案】", text)]
    parse_marker = re.search(r"【解析】", text)
    if len(answer_markers) < 2 or parse_marker is None:
        raise RuntimeError("expected answer/analysis markers not found")

    groups: dict[int, tuple[str, str]] = {}

    # Q1-Q3: first answer marker through the first analysis marker.
    g13_start = answer_markers[0].end()
    g13_end = parse_marker.start()
    g13 = text[g13_start:g13_end].strip()
    for qid, next_qid in ((1, 2), (2, 3), (3, None)):
        candidate, _, _ = numbered_region(g13, qid, next_qid)
        groups[qid] = (candidate, g13)

    # Q4-Q6, Q7-Q9, Q10-Q13, Q14-Q16, Q17-Q20 are answer lines followed by
    # an analysis marker.  Locate the numbered start after each preceding
    # section rather than relying on fragile fixed offsets.
    # Q16 is separated from Q14-Q15 by its own analysis block.
    specs = [(4, 6), (7, 9), (10, 13), (14, 15), (16, 16), (17, 20)]
    cursor = g13_end
    for first, last in specs:
        start_match = re.search(
            rf"(?m)^\s*{first}(?:[.．]|(?=\s+[①（(]))\s*", text[cursor:]
        )
        if not start_match:
            raise RuntimeError(f"answer group Q{first}-Q{last} not found")
        start = cursor + start_match.start()
        analysis_match = re.search(r"【解析】", text[start:])
        if not analysis_match:
            raise RuntimeError(f"analysis boundary after Q{first}-Q{last} not found")
        end = start + analysis_match.start()
        shared = text[start:end].strip()
        for qid in range(first, last + 1):
            next_qid = qid + 1 if qid < last else None
            candidate, _, _ = numbered_region(shared, qid, next_qid)
            groups[qid] = (candidate, shared)
        cursor = start + analysis_match.end()

    # Q21 has a second explicit 【答案】 marker after the Q17-Q20 analysis.
    q21_marker = answer_markers[1]
    q21_analysis = re.search(r"【解析】", text[q21_marker.end():])
    if not q21_analysis:
        raise RuntimeError("Q21 analysis boundary not found")
    q21_end = q21_marker.end() + q21_analysis.start()
    q21 = text[q21_marker.end():q21_end].strip()
    groups[21] = (q21, q21)

    # Q22 is intentionally a guidance candidate, not a claimed answer.
    q22_marker = re.search(r"【22题】", text)
    if not q22_marker:
        raise RuntimeError("Q22 marker not found")
    q22 = text[q22_marker.end():].strip()
    groups[22] = (q22, q22)
    if sorted(groups) != list(range(1, 23)):
        raise RuntimeError(f"unexpected coverage: {sorted(groups)}")
    return groups


def main() -> int:
    data, encoding = fetch_snapshot()
    page_text = article_text(data, encoding)
    groups = build_groups(page_text)
    html_sha = sha_bytes(data)
    rows: list[dict] = []
    for qid in range(1, 23):
        candidate, excerpt = groups[qid]
        content_type = "writing_guidance_candidate" if qid == 22 else "reference_answer_candidate"
        rows.append({
            "schema_version": "exam-reference-answer-candidate-0.2",
            "candidate_id": f"GK-NCA-2024-Q{qid:03d}-MEIPIAN-ANSWER",
            "exam_id": "GK-NCA-2024",
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": "candidate_unverified",
            "candidate_scope": "third_party_meipian_q1_q22",
            "source_authority_status": "unverified_third_party_reprint",
            "source_registry_id": "SRC-GK-2024-NCA-MEIPIAN-ANSWER",
            "source_status": "unverified_third_party_reprint",
            "answer_source_status": "external_writing_guidance_candidate" if qid == 22 else "external_full_candidate",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "candidate_content_type": content_type,
            "answer_candidate_text": candidate,
            "answer_candidate_sha256": sha_text(candidate),
            "source_group_excerpt": excerpt,
            "source_group_excerpt_sha256": sha_text(excerpt),
            "source_html": rel(HTML_OUT),
            "source_html_sha256": html_sha,
            "source_url": URL,
            "source_answer_index": "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/answer_index.jsonl",
            "review_status": "needs_independent_review",
            "notes": [
                "美篇第三方转载/解析页面；未证明为教育部或命题机构官方答案。",
                "本候选层不改变主 answer_index 的 22 条 missing，不提供官方评分标准。",
                "Q22 仅为作文审题与写作指导候选，不是范文或评分细则。" if qid == 22 else "候选文本需与独立来源交叉核验后才能用于研究。",
            ],
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    LOCAL_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_REGISTRY.write_text(json.dumps({
        "source_id": "SRC-GK-2024-NCA-MEIPIAN-ANSWER",
        "source_kind": "gaokao_answer_candidate",
        "document_role": "answer",
        "source_level": "S3",
        "metadata_status": "acquired_unverified",
        "authenticity_status": "unverified",
        "publisher_or_channel": "美篇（第三方转载/解析）",
        "title": "2024全国甲卷语文参考答案及详解（第18期）",
        "scope": "GK-NCA-2024 Q1-Q22；Q22为作文写作指导候选",
        "original_url": URL,
        "local_html": rel(HTML_OUT),
        "html_sha256": html_sha,
        "candidate_jsonl": rel(OUT),
        "acquired_at": now_text(),
        "copyright_note": "仅作内部研究；原始内容版权归发布方/转载方所有",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-reference-answer-candidate-0.2"\n'
        'status: "candidate_only_full_coverage"\n'
        'authority_status: "unverified_third_party_reprint"\n'
        'coverage: "GK-NCA-2024 Q1-Q22"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2024 全国甲卷参考答案候选（美篇独立第三方来源）\n\n"
        "> 页面为美篇第三方转载/解析，已保存原始 HTML 快照。该层仅供独立核验，不改变主 `answer_index.jsonl` 的 22 条 `missing`，不提供官方答案或评分标准。Q22 是作文审题/写作指导，不是范文。\n\n"
        f"- 来源：`{URL}`\n- HTML 快照：`{rel(HTML_OUT)}`\n- HTML SHA-256：`{html_sha}`\n- 候选 JSONL：`{rel(OUT)}`（22 条，Q1—Q22）\n- 本地注册项：`{rel(LOCAL_REGISTRY)}`\n",
        encoding="utf-8",
    )
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-receipt-0.2",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-NCA-2024-MEIPIAN-20260809",
        "exam_id": "GK-NCA-2024",
        "source_registry_id": "SRC-GK-2024-NCA-MEIPIAN-ANSWER",
        "source_authority_status": "unverified_third_party_reprint",
        "source_url": URL,
        "source_html": rel(HTML_OUT),
        "source_html_sha256": html_sha,
        "coverage": {"candidate_questions": list(range(1, 23)), "writing_guidance_questions": [22]},
        "output": rel(OUT),
        "output_sha256": sha_bytes(OUT.read_bytes()),
        "report": rel(REPORT),
        "report_sha256": sha_bytes(REPORT.read_bytes()),
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "html_sha256": html_sha, "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
