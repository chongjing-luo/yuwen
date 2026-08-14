#!/usr/bin/env python3
"""Snapshot an independent Q006 answer candidate for 2016 NC3.

The local 2016 answer bundle has a reviewed cross-question boundary and keeps
Q006 missing.  This script registers a third-party page's Q006 candidate in a
separate layer without mutating that bundle, the source PDF, or MinerU output.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
URL = "https://www.gzywtk.com/sjbrow/1881-4.html"
HTML_OUT = ROOT / "Data/reference/gaokao/html/2016/answer_gzywtk_1881-4.html"
OUT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers/reference_answer_candidates_q006_gzywtk.jsonl"
REPORT = ROOT / "work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2016-Q006.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidate_GK-NC3-2016-Q006_20260809.json"
LOCAL_REGISTRY = ROOT / "Data/reference/gaokao/external/2016_gzywtk_answer/registry_entry.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def fetch() -> bytes:
    response = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=40)
    response.raise_for_status()
    data = response.content
    if len(data) < 1000 or b"1881-4" not in data:
        raise RuntimeError("unexpected GZYWTK response")
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_bytes(data)
    return data


def extract_q006(data: bytes) -> str:
    soup = BeautifulSoup(data, "html.parser")
    content = soup.select_one(".content")
    if content is None:
        raise RuntimeError(".content not found")
    text = content.get_text("\n", strip=False)
    text = re.sub(r"\n[ \t]*\n+", "\n", text)
    required = ["答B给3分", "坚持独立思考", "天下兴亡", "匹夫有责"]
    markers = list(re.finditer(r"【答案】", text))
    if len(markers) < 2:
        raise RuntimeError(f"expected at least two answer markers, found {len(markers)}")
    # The page concatenates several answer groups.  Select the block by its
    # content guard rather than assuming a fixed marker ordinal.
    for marker in markers:
        start = marker.end()
        analysis = re.search(r"【解析】", text[start:])
        if analysis is None:
            continue
        excerpt = text[start:start + analysis.start()].strip()
        if all(term in excerpt for term in required):
            return excerpt
    raise RuntimeError(f"Q006 excerpt failed content guard: {required}")


def main() -> int:
    data = fetch()
    excerpt = extract_q006(data)
    html_sha = sha_bytes(data)
    row = {
        "schema_version": "exam-reference-answer-candidate-0.2",
        "candidate_id": "GK-NC3-2016-Q006-GZYWTK-ANSWER",
        "exam_id": "GK-NC3-2016",
        "question_id": 6,
        "source_role": "answer_scoring_candidate",
        "candidate_status": "candidate_unverified",
        "candidate_scope": "third_party_gzywtk_q006",
        "source_authority_status": "unverified_third_party_reprint",
        "source_registry_id": "SRC-GK-2016-NC3-GZYWTK-Q006-ANSWER",
        "source_status": "unverified_third_party_reprint",
        "answer_source_status": "external_single_question_candidate",
        "scoring_status": "not_available_as_official",
        "mapping_level": "M0",
        "kp_id": "N/A",
        "candidate_content_type": "reference_answer_candidate",
        "answer_candidate_text": excerpt,
        "answer_candidate_sha256": sha_text(excerpt),
        "source_group_excerpt": excerpt,
        "source_group_excerpt_sha256": sha_text(excerpt),
        "source_html": rel(HTML_OUT),
        "source_html_sha256": html_sha,
        "source_url": URL,
        "source_answer_index": "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers/answer_index.jsonl",
        "review_status": "needs_independent_review",
        "notes": [
            "一苇轩第三方试卷题库页面；内容为参考答案候选，不是已核验官方答案或评分标准。",
            "Q006 在本地 answer_index 仍保持 N/A；本层不从 Q005 复合字段推断 Q006。",
            "候选文本覆盖 Q006 的四个小问，需与独立来源和 PDF 逐题复核。",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
    LOCAL_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    LOCAL_REGISTRY.write_text(json.dumps({
        "source_id": "SRC-GK-2016-NC3-GZYWTK-Q006-ANSWER",
        "source_kind": "gaokao_answer_candidate",
        "document_role": "answer",
        "source_level": "S3",
        "metadata_status": "acquired_unverified",
        "authenticity_status": "unverified",
        "publisher_or_channel": "一苇轩（第三方试卷题库）",
        "title": "2016年高考语文试题（全国新课标III）内容",
        "scope": "GK-NC3-2016 Q006候选答案",
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
        'status: "candidate_only_single_question"\n'
        'authority_status: "unverified_third_party_reprint"\n'
        'coverage: "GK-NC3-2016 Q006"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2016 全国卷Ⅲ Q006 参考答案候选（一苇轩）\n\n"
        "> 一苇轩第三方题库页面提供 Q006 四个小问的参考答案候选。该层不修改本地复合答案边界，不把候选升级为官方答案或评分标准。\n\n"
        f"- 来源：`{URL}`\n- HTML 快照：`{rel(HTML_OUT)}`\n- HTML SHA-256：`{html_sha}`\n- 候选 JSONL：`{rel(OUT)}`\n- 本地注册项：`{rel(LOCAL_REGISTRY)}`\n",
        encoding="utf-8",
    )
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-receipt-0.2",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-NC3-2016-Q006-GZYWTK-20260809",
        "exam_id": "GK-NC3-2016",
        "question_id": 6,
        "source_registry_id": "SRC-GK-2016-NC3-GZYWTK-Q006-ANSWER",
        "source_authority_status": "unverified_third_party_reprint",
        "source_url": URL,
        "source_html": rel(HTML_OUT),
        "source_html_sha256": html_sha,
        "coverage": {"candidate_questions": [6]},
        "output": rel(OUT),
        "output_sha256": sha_bytes(OUT.read_bytes()),
        "report": rel(REPORT),
        "report_sha256": sha_bytes(REPORT.read_bytes()),
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "compound_alignment_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": 1, "html_sha256": html_sha, "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
