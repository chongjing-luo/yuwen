#!/usr/bin/env python3
"""Register the partial 2023 National A answer snapshot as candidates.

The locally acquired China Education Online artifact is a third-party
reproduction.  Its MinerU text exposes only Q1--Q3, Q6--Q10; this script
records exactly that partial coverage and does not invent Q4/Q5 or Q11--Q22.
It never creates or edits the main answer index, source PDF, or MinerU output.
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
PDF = ROOT / "Data/reference/gaokao/pdf/2023/2023_NCA_answer.pdf"
HTML = ROOT / "Data/reference/gaokao/html/2023/answer.html"
FULL = ROOT / "Data/reference/gaokao/mineru_result/2023_NCA_answer/full.md"
OUT = BASE / "answers/reference_answer_candidates.jsonl"
REPORT = ROOT / "work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2023.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidates_GK-NCA-2023_20260809.json"

QIDS = [1, 2, 3, 6, 7, 8, 9, 10]


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def group(text: str, start: str, end: str | None = None) -> str:
    match = re.search(start + (rf"(.*?)(?={end})" if end else r"(.*)$"), text, re.S | re.M)
    if not match:
        raise RuntimeError(f"source answer block not found: {start}")
    value = match.group(0).strip()
    if not value:
        raise RuntimeError(f"empty source answer block: {start}")
    return value


def build_groups(text: str) -> dict[int, tuple[str, str]]:
    groups: dict[int, tuple[str, str]] = {}
    g13 = group(text, r"^1\.C 2\.C 3\.B\s*$")
    for qid, answer in ((1, "C"), (2, "C"), (3, "B")):
        groups[qid] = (answer, g13)
    g6 = group(text, r"^6\.", r"\n\n\(三\)")
    groups[6] = (g6.split(".", 1)[1].strip(), g6)
    g7 = group(text, r"^\(三\).*?7\.C\s*$", r"\n8\.")
    groups[7] = ("C", g7)
    g8 = group(text, r"^8\.", r"\n9\.")
    groups[8] = (g8.split(".", 1)[1].strip(), g8)
    g9 = group(text, r"^9\.", r"\n\n## 二、")
    groups[9] = (g9.split(".", 1)[1].strip(), g9)
    g10 = group(text, r"^\(一\) 文言文阅读 .*?10\.BDG[。.]?\s*$")
    groups[10] = ("BDG", g10)
    if sorted(groups) != QIDS:
        raise RuntimeError(f"unexpected candidate coverage: {sorted(groups)}")
    return groups


def main() -> int:
    for path in (PDF, HTML, FULL):
        if not path.exists():
            raise SystemExit(f"missing source artifact: {path}")
    raw = FULL.read_text(encoding="utf-8")
    groups = build_groups(raw)
    pdf_sha = sha_bytes(PDF.read_bytes())
    html_sha = sha_bytes(HTML.read_bytes())
    full_sha = sha_bytes(FULL.read_bytes())
    rows: list[dict] = []
    for qid in QIDS:
        candidate, excerpt = groups[qid]
        rows.append({
            "schema_version": "exam-reference-answer-candidate-0.2",
            "candidate_id": f"{EXAM_ID}-Q{qid:03d}-EOL-ANSWER",
            "exam_id": EXAM_ID,
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": "candidate_unverified",
            "candidate_scope": "third_party_eol_partial_q1_q3_q6_q10",
            "source_authority_status": "unverified_third_party_reprint",
            "source_registry_id": "SRC-GK-2023-NCA-ANSWER",
            "source_status": "unverified_third_party_reprint",
            "answer_source_status": "external_partial_candidate",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "candidate_content_type": "reference_answer_candidate",
            "answer_candidate_text": candidate,
            "answer_candidate_sha256": sha_text(candidate),
            "source_group_excerpt": excerpt,
            "source_group_excerpt_sha256": sha_text(excerpt),
            "source_pdf": rel(PDF),
            "source_pdf_sha256": pdf_sha,
            "source_html": rel(HTML),
            "source_html_sha256": html_sha,
            "source_mineru_md": rel(FULL),
            "source_mineru_md_sha256": full_sha,
            "source_url": "https://gaokao.eol.cn/shiti/yw/202306/t20230613_2439481.shtml",
            "source_answer_index": rel(BASE / "answers/answer_index.jsonl"),
            "review_status": "needs_independent_review",
            "notes": [
                "中国教育在线第三方转载快照；registry authenticity_status=unverified。",
                "MinerU full.md 仅提供 Q1—Q3、Q6—Q10；Q4/Q5/Q11—Q22 未见独立候选，保持缺失。",
                "本候选层不改变主 answer_index，不标记 official_verified，也不生成官方评分标准。",
            ],
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    missing = [qid for qid in range(1, 23) if qid not in QIDS]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-reference-answer-candidate-0.2"\n'
        'status: "candidate_only_partial"\n'
        'authority_status: "unverified_third_party_reprint"\n'
        'coverage: "GK-NCA-2023 Q1-Q3, Q6-Q10"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2023 全国甲卷参考答案候选（部分）\n\n"
        "> 来源是中国教育在线第三方转载快照。当前 MinerU `full.md` 只暴露 Q1—Q3、Q6—Q10；其余题号明确保留缺失，不用搜索摘要或本地解析反推。该层不修改主答案索引，不提供官方评分标准。\n\n"
        f"- 候选题号：`{QIDS}`；缺失题号：`{missing}`。\n"
        f"- PDF：`{rel(PDF)}`，SHA-256 `{pdf_sha}`。\n"
        f"- HTML：`{rel(HTML)}`，SHA-256 `{html_sha}`。\n"
        f"- MinerU：`{rel(FULL)}`，SHA-256 `{full_sha}`。\n"
        f"- 派生 JSONL：`{rel(OUT)}`。\n",
        encoding="utf-8",
    )
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-receipt-0.2",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-NCA-2023-20260809",
        "generated_at": now_text(),
        "exam_id": EXAM_ID,
        "source_registry_id": "SRC-GK-2023-NCA-ANSWER",
        "source_authority_status": "unverified_third_party_reprint",
        "coverage": {"candidate_questions": QIDS, "missing_questions": missing},
        "inputs": {
            "pdf": {"path": rel(PDF), "sha256": pdf_sha},
            "html": {"path": rel(HTML), "sha256": html_sha},
            "mineru_full_md": {"path": rel(FULL), "sha256": full_sha},
        },
        "output": {"path": rel(OUT), "sha256": sha_bytes(OUT.read_bytes()), "rows": len(rows)},
        "report": {"path": rel(REPORT), "sha256": sha_bytes(REPORT.read_bytes())},
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "第三方答案快照仅作部分候选；未覆盖题号保持缺失，不从候选文本推导官方答案或评分标准。",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "candidate_questions": QIDS, "missing_questions": missing, "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
