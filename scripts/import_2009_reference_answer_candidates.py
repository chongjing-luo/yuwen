#!/usr/bin/env python3
"""Derive a conservative 2009 Sichuan answer-candidate layer.

The independent page is hosted on a Sichuan provincial website, but the
embedded PDF identifies Jyeoo as its author and is not an examination-authority
release.  Therefore only explicit answer keys for Q1--Q6 are imported as
third-party candidates; model responses for subjective questions stay in the
source snapshot and are not treated as scoring standards.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009"
SOURCE_DIR = ROOT / "Data/reference/gaokao/external/2009_gaokao_answer"
HTML = SOURCE_DIR / "scdfz_source.html"
PDF = SOURCE_DIR / "scdfz_answer.pdf"
GAOKAO_HTML = SOURCE_DIR / "source.html"
MANIFEST = SOURCE_DIR / "acquisition_manifest.json"
OUT = BASE / "answers/reference_answer_candidates.jsonl"
REPORT = ROOT / "work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2009.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidates_2009_20260809.json"
REGISTRY_ENTRY = SOURCE_DIR / "registry_entry.json"
SOURCES = ROOT / "Data/reference/gaokao/registry/sources.jsonl"
ARTIFACTS = ROOT / "Data/reference/gaokao/registry/artifacts.jsonl"
RELATIONS = ROOT / "Data/reference/gaokao/registry/source_relations.jsonl"

SOURCE_ID = "SRC-GK-2009-SC-DFZ-JYEEO-ANSWER-CANDIDATE"
ARTIFACT_ID = "ART-GK-2009-SC-DFZ-JYEEO-ANSWER-CANDIDATE"
PAGE_URL = "https://www.scdfz.org.cn/scyx/scgkt/2000nyh/yw/content_19900"
PDF_URL = "https://www.scdfz.org.cn/Upload/main/ContentManage/Article/File/201906061738078672.pdf"
GAOKAO_URL = "https://www.gaokao.com/e/20090611/4b8bcafdad195.shtml"

# These are transcriptions of explicit keys in the independent page's answer
# section.  Q5/Q6 retain subquestion boundaries; no local analysis is used to
# fill any missing question number.
EXPECTED: dict[int, str] = {
    1: "D",
    2: "C",
    3: "D",
    4: "C",
    5: "（1）D；（2）A；（3）A",
    6: "（1）B；（2）B；（3）B；（4）①大概用来治理天下国家的人，不再都从学校中产生。②我们虽然为它即将推行而感到高兴并且庆幸，但又担心后来的人不能继承我的思想，于是推究它的意义来告诉后来的人。",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def source_text() -> str:
    soup = BeautifulSoup(HTML.read_text(encoding="utf-8", errors="replace"), "html.parser")
    content = soup.select_one("div.conTxt")
    if content is None:
        raise RuntimeError("scdfz page content container missing")
    text = content.get_text("\n", strip=True)
    marker = "参考答案与试题解析"
    if marker not in text:
        raise RuntimeError("answer-section marker missing")
    return text[text.index(marker):]


def question_blocks(text: str) -> dict[int, str]:
    matches = list(re.finditer(r"(?m)^(1[0-3]|[1-9])．", text))
    blocks: dict[int, str] = {}
    for idx, match in enumerate(matches):
        qid = int(match.group(1))
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        blocks[qid] = text[match.start():end].strip()
    return blocks


def candidate_excerpt(block: str, qid: int) -> str:
    if qid <= 4:
        match = re.search(r"故选：([A-D])。", block)
        if not match:
            raise RuntimeError(f"Q{qid}: explicit 故选 marker missing")
        return match.group(0)
    if qid == 5:
        match = re.search(r"答案：\s*（1）D\s*（2）A\s*（3）A", block)
        if not match:
            raise RuntimeError("Q5: explicit subanswer block missing")
        return match.group(0)
    # Keep only the explicit answer block and the two translation responses.
    # The reprint uses both full-width and ASCII punctuation and its wording
    # ends with “后来的人”, not the classical “来者”; slicing at the stable
    # “参考译文：” marker avoids brittle wording-dependent regexes and keeps
    # the excerpt from swallowing the long reference translation.
    answer_start = block.find("答案：")
    answer_end = block.find("参考译文：", answer_start + 1)
    if answer_start < 0 or answer_end < 0:
        raise RuntimeError("Q6: explicit answer/translation boundary missing")
    short_block = block[answer_start:answer_end].strip()
    expected_prefix = "答案："
    expected_tokens = ("（1）B", "（2）B", "（3）B", "（4）")
    if not short_block.startswith(expected_prefix) or any(token not in short_block for token in expected_tokens):
        raise RuntimeError("Q6: explicit subanswer block missing")
    return short_block


def append_registry(path: Path, key: str, row: dict) -> None:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.exists() else []
    if any(existing.get(key) == row.get(key) for existing in rows):
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> int:
    required = [HTML, PDF, GAOKAO_HTML, MANIFEST]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("missing source artifacts: " + ", ".join(missing))
    text = source_text()
    blocks = question_blocks(text)
    if sorted(blocks)[:6] != [1, 2, 3, 4, 5, 6]:
        raise RuntimeError(f"unexpected answer section question blocks: {sorted(blocks)}")

    rows: list[dict] = []
    for qid, answer in EXPECTED.items():
        excerpt = candidate_excerpt(blocks[qid], qid)
        if qid <= 4:
            if excerpt != f"故选：{answer}。":
                raise RuntimeError(f"Q{qid}: source key mismatch: {excerpt!r}")
        else:
            # The source uses line breaks and full-width punctuation; compare
            # the explicit subanswer tokens rather than normalized prose.
            expected_tokens = re.findall(r"（[1-4]）[ABCD]", answer)
            if any(token not in excerpt for token in expected_tokens):
                raise RuntimeError(f"Q{qid}: source subanswer mismatch")
        start = text.index(blocks[qid])
        end = start + len(blocks[qid])
        rows.append({
            "schema_version": "exam-reference-answer-candidate-0.2",
            "candidate_id": f"GK-SC-2009-Q{qid:03d}-SCDFZ-JYEEO-CANDIDATE",
            "exam_id": "GK-SC-2009",
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": "candidate_unverified",
            "candidate_scope": "third_party_answer_analysis_reprint_q1_q6",
            "source_authority_status": "unverified_third_party_reprint",
            "source_registry_id": SOURCE_ID,
            "source_status": "unverified_third_party_reprint",
            "answer_source_status": "external_partial_candidate",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "candidate_content_type": "answer_candidate_short" if qid <= 4 else "answer_candidate_subquestion_key",
            "answer_candidate_text": answer,
            "answer_candidate_sha256": sha_text(answer),
            "source_group_excerpt": excerpt,
            "source_group_excerpt_sha256": sha_text(excerpt),
            "source_text_start": start,
            "source_text_end": end,
            "source_page": rel(HTML),
            "source_page_sha256": sha(HTML),
            "source_pdf": rel(PDF),
            "source_pdf_sha256": sha(PDF),
            "source_gaokao_snapshot": rel(GAOKAO_HTML),
            "source_gaokao_snapshot_sha256": sha(GAOKAO_HTML),
            "source_url": PAGE_URL,
            "source_pdf_url": PDF_URL,
            "source_answer_index": None,
            "review_status": "needs_independent_review",
            "notes": [
                "页面由四川省地方志工作办公室网站转载，但嵌入 PDF 元数据作者为菁优网；不视为命题/考试机构官方答案。",
                "仅保留页面答案解析中明确的 Q1-Q6 答案键；Q7-Q12 的主观题示例答案、Q13 作文指导不进入本候选 JSONL。",
                "候选不等于官方答案，不提供官方评分标准；教材映射保持 M0 / kp_id=N/A。",
            ],
        })

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    missing_q = list(range(7, 22))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-reference-answer-candidate-0.2"\n'
        'status: "candidate_only_partial"\n'
        'authority_status: "unverified_third_party_reprint"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2009 四川卷答案候选（Q1—Q6）\n\n"
        "> 来源为四川省地方志工作办公室网站转载页面及其嵌入 PDF；PDF 元数据作者为菁优网。页面同时含 Q7—Q12 主观题示例答案和 Q13 作文指导，但这些内容未进入候选答案键层，不能替代评分标准。\n\n"
        f"- 候选题号：`{list(EXPECTED)}`；本层未登记题号：`{missing_q}`。\n"
        f"- 页面：`{rel(HTML)}`（SHA-256 `{sha(HTML)}`）。\n"
        f"- PDF：`{rel(PDF)}`（SHA-256 `{sha(PDF)}`）。\n"
        f"- 高考网对照快照：`{rel(GAOKAO_HTML)}`（仅用于来源发现，不作为答案内容）。\n"
        f"- 派生 JSONL：`{rel(OUT)}`；主答案索引未创建、未修改。\n",
        encoding="utf-8",
    )
    entry = {
        "source_id": SOURCE_ID,
        "artifact_id": ARTIFACT_ID,
        "document_role": "answer_candidate",
        "source_kind": "gaokao_answer_candidate",
        "publisher_or_channel": "四川省地方志工作办公室网站转载/菁优网解析 PDF",
        "original_url": PAGE_URL,
        "pdf_url": PDF_URL,
        "authenticity_status": "unverified",
        "status": "acquired_unverified_candidate_partial",
        "local_path": rel(SOURCE_DIR),
        "candidate_jsonl": rel(OUT),
        "coverage": "GK-SC-2009 Q1-Q6 explicit answer keys; Q7-Q12 model responses and Q13 writing guidance remain outside candidate key layer",
        "relation": {"type": "answer_candidate_of", "target_source_id": "SRC-GK-2009-SC-QUESTION", "status": "candidate_only"},
        "source_hashes": {"scdfz_source.html": sha(HTML), "scdfz_answer.pdf": sha(PDF), "gaokao_source.html": sha(GAOKAO_HTML), "acquisition_manifest.json": sha(MANIFEST)},
        "policy": "省级网站转载内容与第三方解析 PDF 只作候选转录；不视为官方答案或评分标准。",
    }
    REGISTRY_ENTRY.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    append_registry(SOURCES, "source_id", {
        "canonical_artifact_id": ARTIFACT_ID,
        "copyright_note": "仅作内部研究；原始内容版权归发布方/命题机构所有",
        "document_role": "answer_candidate",
        "metadata_status": "acquired_unverified_candidate_partial",
        "publisher_or_channel": "四川省地方志工作办公室网站转载/菁优网解析 PDF",
        "scope": "2009四川卷语文；Q1-Q6答案键候选，Q7-Q12主观示例与Q13作文指导不进入答案键",
        "source_id": SOURCE_ID,
        "source_kind": "gaokao_answer_candidate",
        "source_level": "S3",
        "title": "2009四川卷语文答案候选（省级网站转载/菁优网解析）",
    })
    append_registry(ARTIFACTS, "artifact_id", {
        "acquired_at": now_text(),
        "artifact_id": ARTIFACT_ID,
        "artifact_role": "answer_candidate",
        "authenticity_status": "unverified",
        "byte_size": PDF.stat().st_size,
        "carrier_type": "网页快照/嵌入 PDF/候选 JSONL",
        "derived_from": rel(HTML),
        "error": "页面内容为第三方解析转载；未作为官方答案或评分标准",
        "html_byte_size": HTML.stat().st_size,
        "html_sha256": sha(HTML),
        "image_urls": [],
        "is_canonical": False,
        "local_path": rel(PDF),
        "mineru_full_md": None,
        "mineru_processed_at": None,
        "mineru_result_dir": None,
        "original_url": PAGE_URL,
        "page_count": 32,
        "sha256": sha(PDF),
        "source_id": SOURCE_ID,
        "status": "acquired_unverified_candidate_partial",
        "transform": "省级网站 HTML/PDF 快照；Q1-Q6 显式答案键候选抽取",
    })
    append_registry(RELATIONS, "relation_id", {
        "relation_id": "REL-GK-2009-SC-DFZ-JYEEO-ANSWER-CANDIDATE",
        "relation_status": "candidate_only",
        "relation_type": "answer_candidate_of",
        "source_id_from": SOURCE_ID,
        "source_id_to": "SRC-GK-2009-SC-QUESTION",
    })
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-receipt-0.2",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-SC-2009-20260809",
        "generated_at": now_text(),
        "exam_id": "GK-SC-2009",
        "source_registry_id": SOURCE_ID,
        "source_authority_status": "unverified_third_party_reprint",
        "coverage": {"candidate_questions": list(EXPECTED), "missing_questions": missing_q},
        "inputs": {p.name: {"path": rel(p), "sha256": sha(p)} for p in required},
        "output": {"path": rel(OUT), "sha256": sha(OUT), "rows": len(rows)},
        "report": {"path": rel(REPORT), "sha256": sha(REPORT)},
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "仅从独立转载页面中明确答案键建立候选；不补缺失题号、不生成官方评分标准。",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "candidate_questions": list(EXPECTED), "missing_questions": missing_q, "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
