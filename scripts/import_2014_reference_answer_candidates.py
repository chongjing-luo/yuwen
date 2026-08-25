#!/usr/bin/env python3
"""Register the clear Q1--Q9 portion of a watermarked 2014 answer image."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014"
SOURCE_DIR = ROOT / "Data/reference/gaokao/external/2014_gaokao_answer"
HTML = SOURCE_DIR / "source.html"
IMAGE = SOURCE_DIR / "page1.jpg"
OUT = BASE / "answers/reference_answer_candidates.jsonl"
REPORT = ROOT / "work/knowledge/exams/workbench/EXAM-REFERENCE-ANSWER-CANDIDATES-2014.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidates_2014_20260809.json"
ANSWERS = {1: "A", 2: "D", 3: "D", 4: "B", 5: "C", 6: "C", 7: "D", 8: "B", 9: "B"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def main() -> int:
    if not HTML.exists() or not IMAGE.exists():
        raise SystemExit("missing 2014 source HTML/image")
    html_sha, image_sha = sha(HTML), sha(IMAGE)
    rows = []
    for qid, answer in ANSWERS.items():
        excerpt = f"Q{qid}: {answer} (transcribed from the Q1-Q9 answer row in page1.jpg)"
        rows.append({
            "schema_version": "exam-reference-answer-candidate-0.2",
            "candidate_id": f"GK-SC-2014-Q{qid:03d}-GAOKAO-IMAGE-CANDIDATE",
            "exam_id": "GK-SC-2014",
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": "candidate_unverified",
            "candidate_scope": "third_party_watermarked_answer_image_q1_q9",
            "source_authority_status": "unverified_third_party_reprint",
            "source_registry_id": "SRC-GK-2014-SC-GAOKAO-IMAGE-ANSWER-CANDIDATE",
            "source_status": "unverified_third_party_reprint",
            "answer_source_status": "external_partial_candidate",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "candidate_content_type": "answer_candidate_short",
            "answer_candidate_text": answer,
            "answer_candidate_sha256": sha_text(answer),
            "source_group_excerpt": excerpt,
            "source_group_excerpt_sha256": sha_text(excerpt),
            "source_image": rel(IMAGE),
            "source_image_sha256": image_sha,
            "source_page": rel(HTML),
            "source_page_sha256": html_sha,
            "source_url": "https://www.gaokao.com/e/20140421/5354d5009d452.shtml",
            "source_answer_index": rel(BASE / "answers/answer_index.jsonl"),
            "review_status": "needs_independent_review",
            "notes": [
                "高考网转载的中学学科网水印答案图；仅登记图像清晰覆盖的 Q1-Q9。",
                "Q10-Q18 图像页已失链，Q19-Q21 另有页面但本批次不登记；未用搜索摘要补缺。",
                "候选不等于官方答案，不提供官方评分标准。",
            ],
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")
    missing = list(range(10, 22))
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-reference-answer-candidate-0.2"\n'
        'status: "candidate_only_partial"\n'
        'authority_status: "unverified_third_party_reprint"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2014 四川卷答案候选（Q1—Q9）\n\n"
        "> 来源为高考网转载的中学学科网带水印答案图。当前仅图像清晰覆盖 Q1—Q9；Q10—Q18 的分页图已失链，保持缺失，不从搜索结果或本地解析推答案。\n\n"
        f"- 候选题号：`{list(ANSWERS)}`；缺失题号：`{missing}`。\n"
        f"- 来源页：`{rel(HTML)}`（SHA-256 `{html_sha}`）。\n"
        f"- 答案图：`{rel(IMAGE)}`（SHA-256 `{image_sha}`）。\n"
        f"- 派生 JSONL：`{rel(OUT)}`。\n",
        encoding="utf-8",
    )
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-receipt-0.2",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-SC-2014-20260809",
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "exam_id": "GK-SC-2014",
        "source_registry_id": "SRC-GK-2014-SC-GAOKAO-IMAGE-ANSWER-CANDIDATE",
        "source_authority_status": "unverified_third_party_reprint",
        "coverage": {"candidate_questions": list(ANSWERS), "missing_questions": missing},
        "inputs": {"html": {"path": rel(HTML), "sha256": html_sha}, "image": {"path": rel(IMAGE), "sha256": image_sha}},
        "output": {"path": rel(OUT), "sha256": sha(OUT), "rows": len(rows)},
        "report": {"path": rel(REPORT), "sha256": sha(REPORT)},
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "candidate_questions": list(ANSWERS), "missing_questions": missing,
                      "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
