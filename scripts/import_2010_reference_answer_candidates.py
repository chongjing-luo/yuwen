#!/usr/bin/env python3
"""Derive conservative 2010 Sichuan answer candidates from the DOC text.

Only explicit ``故答案为``/``故选`` markers are retained.  Missing or
unbounded question answers are not inferred from the local analysis PDF.
"""
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010"
SOURCE_DIR = ROOT / "Data/reference/gaokao/external/2010_gaokao_answer"
TEXT = SOURCE_DIR / "answer_source.txt"
HTML = SOURCE_DIR / "source.html"
RAR = SOURCE_DIR / "answer_bundle.rar"
DOC = SOURCE_DIR / "四川语文答案.doc"
OUT = BASE / "answers/reference_answer_candidates.jsonl"
REPORT = ROOT / "work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2010.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidates_2010_20260809.json"
REGISTRY_ENTRY = SOURCE_DIR / "registry_entry.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def main() -> int:
    required = [TEXT, HTML, RAR, DOC]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise SystemExit("missing source artifacts: " + ", ".join(missing))
    source = TEXT.read_text(encoding="utf-8")
    rows: list[dict] = []
    marker_re = re.compile(r"(?ms)^\s*(\d+)[、.]\s*(?:解析|A项).*?(?=故(?:答案为|选)\s*([A-E]+))")
    for match in marker_re.finditer(source):
        qid = int(match.group(1))
        answer = match.group(2)
        if qid not in {1, 2, 4, 8, 9}:
            continue
        excerpt = match.group(0).strip()
        line_start = source[:match.start()].count("\n") + 1
        line_end = source[:match.end()].count("\n") + 1
        rows.append({
            "schema_version": "exam-reference-answer-candidate-0.2",
            "candidate_id": f"GK-SC-2010-Q{qid:03d}-GAOKAO-CANDIDATE",
            "exam_id": "GK-SC-2010",
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": "candidate_unverified",
            "candidate_scope": "third_party_gaokao_com_answer_attachment",
            "source_authority_status": "unverified_third_party_reprint",
            "source_registry_id": "SRC-GK-2010-SC-GAOKAO-ANSWER-CANDIDATE",
            "source_status": "unverified_third_party_reprint",
            "answer_source_status": "external_candidate",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "candidate_content_type": "answer_candidate_short",
            "answer_candidate_text": answer,
            "answer_candidate_sha256": sha_text(answer),
            "source_group_excerpt": excerpt,
            "source_group_excerpt_sha256": sha_text(excerpt),
            "source_line_start": line_start,
            "source_line_end": line_end,
            "source_html": rel(HTML),
            "source_html_sha256": sha(HTML),
            "source_rar": rel(RAR),
            "source_rar_sha256": sha(RAR),
            "source_doc": rel(DOC),
            "source_doc_sha256": sha(DOC),
            "source_text": rel(TEXT),
            "source_text_sha256": sha(TEXT),
            "source_url": "https://www.gaokao.com/e/20100513/4beba0aa4a96d.shtml",
            "attachment_url": "https://files.eduuu.com/ohr/2010/06/12/145336_4c132ef00dce2.rar",
            "source_answer_index": rel(BASE / "answers/answer_index.jsonl"),
            "review_status": "needs_independent_review",
            "notes": [
                "高考网第三方答案附件；仅作候选，不是考试机构发布的官方答案。",
                "仅保留文档中显式‘故答案为/故选’标记；缺失题号不由解析文本推断。",
            ],
        })
    rows.sort(key=lambda row: row["question_id"])
    ids = [row["question_id"] for row in rows]
    if ids != [1, 2, 4, 8, 9]:
        raise RuntimeError(f"unexpected explicit coverage: {ids}")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    missing_q = [qid for qid in range(1, 22) if qid not in ids]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-reference-answer-candidate-0.2"\n'
        'status: "candidate_only_partial"\n'
        'authority_status: "unverified_third_party_reprint"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2010 四川卷答案候选（明确标记部分）\n\n"
        "> 来源为高考网转载页链接的第三方 RAR/DOC 附件。仅登记文档中有明确‘故答案为/故选’标记的 Q1、Q2、Q4、Q8、Q9；其余题号保持缺失，不由混合题文/解析推断。\n\n"
        f"- 候选题号：`{ids}`；显式缺失：`{missing_q}`。\n"
        f"- 来源页：`{rel(HTML)}`（SHA-256 `{sha(HTML)}`）。\n"
        f"- RAR：`{rel(RAR)}`（SHA-256 `{sha(RAR)}`）；DOC：`{rel(DOC)}`（SHA-256 `{sha(DOC)}`）。\n"
        f"- 转文本派生：`{rel(TEXT)}`（SHA-256 `{sha(TEXT)}`）。\n"
        f"- 派生 JSONL：`{rel(OUT)}`；主答案索引未创建、未修改。\n",
        encoding="utf-8",
    )
    entry = {
        "source_id": "SRC-GK-2010-SC-GAOKAO-ANSWER-CANDIDATE",
        "artifact_id": "ART-GK-2010-SC-GAOKAO-ANSWER-CANDIDATE",
        "document_role": "answer_candidate",
        "source_kind": "gaokao_answer_candidate",
        "publisher_or_channel": "高考网转载/第三方附件",
        "original_url": "https://www.gaokao.com/e/20100513/4beba0aa4a96d.shtml",
        "attachment_url": "https://files.eduuu.com/ohr/2010/06/12/145336_4c132ef00dce2.rar",
        "authenticity_status": "unverified",
        "status": "acquired_unverified_candidate_partial",
        "local_path": rel(SOURCE_DIR),
        "candidate_jsonl": rel(OUT),
        "coverage": "GK-SC-2010 Q1, Q2, Q4, Q8, Q9 explicit answer markers; other question numbers missing",
        "relation": {"type": "answer_candidate_of", "target_source_id": "SRC-GK-2010-SC-QUESTION", "status": "candidate_only"},
        "source_hashes": {p.name: sha(p) for p in required},
        "policy": "第三方附件只作候选转录；不视为官方答案或评分标准。",
    }
    REGISTRY_ENTRY.write_text(json.dumps(entry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-receipt-0.2",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-SC-2010-20260809",
        "generated_at": now_text(),
        "exam_id": "GK-SC-2010",
        "source_registry_id": entry["source_id"],
        "source_authority_status": "unverified_third_party_reprint",
        "coverage": {"candidate_questions": ids, "missing_questions": missing_q},
        "inputs": {p.name: {"path": rel(p), "sha256": sha(p)} for p in required},
        "output": {"path": rel(OUT), "sha256": sha(OUT), "rows": len(rows)},
        "report": {"path": rel(REPORT), "sha256": sha(REPORT)},
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "仅从明确答案标记建立候选；不补缺失题号、不生成官方评分标准。",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "candidate_questions": ids, "missing_questions": missing_q,
                      "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
