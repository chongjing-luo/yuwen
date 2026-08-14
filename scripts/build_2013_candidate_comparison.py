#!/usr/bin/env python3
"""Build a conservative cross-source comparison layer for GK-SC-2013.

The two inputs are already-derived candidate layers: a third-party Sina image
transcription and a locally supplied analysis PDF.  This script records what
can be compared, what is missing, and what needs adjudication.  It never
promotes either source, writes the main answer index, or edits source files.
"""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM_ID = "GK-SC-2013"
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract" / EXAM_ID
LOCAL = BASE / "answers/local_analysis_candidates.jsonl"
EXTERNAL = BASE / "answers/reference_answer_candidates.jsonl"
MAIN = BASE / "answers/answer_index.jsonl"
OUT = BASE / "answers/reference_answer_candidate_comparison.jsonl"
REPORT = ROOT / "work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATE-COMPARISON-2013.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidate_comparison_GK-SC-2013_20260809.json"

EXPECTED_MAIN_SHA256 = "489ba22579be29b0426db2ece4732bc83bc850a903ca8d513c192a510a74289a"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def load(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def compact(text: str) -> str:
    """Comparison-only form; source text is never replaced by this form."""
    text = unicodedata.normalize("NFKC", text)
    # NFKC turns full-width punctuation into ASCII, so keep both forms.
    return re.sub(r"[\s，,。；;：:、．.（）()【】「」‘’“”《》!?！？\-—_]+", "", text)


def option_form(text: str) -> str:
    """Normalize only the short A/B/C/D answer shape for diagnostics."""
    value = unicodedata.normalize("NFKC", text).strip().upper()
    return re.sub(r"[^A-D]", "", value)


def summarize(text: str) -> dict:
    return {
        "sha256": sha_text(text) if text else None,
        "compact_sha256": sha_text(compact(text)) if text else None,
        "char_count": len(text),
        "preview": re.sub(r"\s+", " ", text).strip()[:120] if text else None,
    }


MANUAL_NOTES: dict[int, tuple[str, list[str]]] = {
    1: ("textually_consistent_unverified", ["本地解析候选与新浪图像候选均为 B；一致不等于官方核验。"]),
    2: ("format_equivalent_unverified", ["本地写作 A.，新浪写作 A；仅作选项标点归一诊断。"]),
    3: ("local_mixed_analysis_no_explicit_answer", ["本地 Q003 只有混合解析/题干边界，没有显式答案标记；不从解析推断 B。"]),
    4: ("format_equivalent_unverified", ["本地写作小写 c，新浪写作大写 C；仅作大小写归一诊断。"]),
    5: ("textually_consistent_unverified", ["两层候选均为 B；来源均未核验。"]),
    6: ("textually_consistent_unverified", ["两层候选均为 C；来源均未核验。"]),
    7: ("textually_consistent_unverified", ["两层候选均为 D；来源均未核验。"]),
    8: ("textually_consistent_unverified", ["两层候选均为 D；未据一致性升级权威。"]),
    9: ("format_equivalent_unverified", ["本地写作 C.，新浪写作 C；仅作选项标点归一诊断。"]),
    10: ("local_mixed_analysis_no_explicit_answer", ["本地 Q010 没有独立答案候选，只有混合解析文本；不从解析段概括答案。"]),
    11: ("local_mixed_analysis_no_explicit_answer", ["本地 Q011 没有独立答案候选，只有混合解析文本；不从解析段概括答案。"]),
    12: ("textually_consistent_unverified", ["两层候选的断句文本一致；仍不是官方答案或评分材料。"]),
    13: ("local_mixed_analysis_no_explicit_answer", ["本地 Q013 没有独立答案候选，只有混合解析文本；不从解析段概括答案。"]),
    14: ("format_equivalent_unverified", ["两层默写答案去空白/标点后相同；保留本地分词空格差异。"]),
    15: ("textually_consistent_unverified", ["两层候选均为 C、E；来源均未核验。"]),
    16: ("ocr_or_format_difference_requires_review", ["本地候选含‘由，河’疑似 OCR/版面残片；去标点后与新浪候选一致，未静默修复。"]),
    17: ("text_difference_requires_review", ["存在‘坚韧的较量/坚韧较量’、‘和/与’、‘慌恐/惶恐’及‘沉重的思考/沉重思考’等差异，不能静默裁决。"]),
    18: ("text_difference_requires_review", ["两层示例答案长度和措辞明显不同；本地文本含 OCR 疑似字形，不能视为同一答案。"]),
    19: ("format_or_label_difference_requires_review", ["本地带‘示例’前缀且缺标点，新浪为带问号的三问文本；需人工确认边界与原文。"]),
    20: ("coverage_difference_requires_review", ["本地候选只到示例二且有断句/OCR差异，新浪候选另含示例三；不得把外部更长文本写回本地候选。"]),
    21: ("both_sources_missing", ["Q021 作文在两层候选中均无独立答案；作文材料/指导不等于评分标准。"]),
}


def classify(qid: int, local: dict | None, external: dict | None) -> dict:
    local_text = (local or {}).get("candidate_text") or ""
    external_text = (external or {}).get("answer_candidate_text") or ""
    local_kind = (local or {}).get("candidate_kind")
    exact = bool(local_text and external_text and local_text == external_text)
    compact_match = bool(local_text and external_text and compact(local_text) == compact(external_text))
    option_match = bool(local_text and external_text and option_form(local_text) == option_form(external_text) and len(option_form(local_text)) == 1)
    status, notes = MANUAL_NOTES[qid]
    return {
        "comparison_id": f"{EXAM_ID}-Q{qid:03d}-CANDIDATE-COMPARISON",
        "schema_version": "exam-reference-answer-candidate-comparison-0.1",
        "exam_id": EXAM_ID,
        "question_id": qid,
        "comparison_status": status,
        "adjudication": "not_adjudicated",
        "local_candidate_id": (local or {}).get("candidate_id"),
        "external_candidate_id": (external or {}).get("candidate_id"),
        "local_candidate_kind": local_kind,
        "local_candidate_available": bool(local_text),
        "external_candidate_available": bool(external_text),
        "local_candidate_source": rel(BASE / "answers/local_analysis_candidates.jsonl") if local else None,
        "external_candidate_source": rel(BASE / "answers/reference_answer_candidates.jsonl") if external else None,
        "local_candidate": summarize(local_text),
        "external_candidate": summarize(external_text),
        "evidence": {
            "exact_text_match": exact,
            "compact_text_match": compact_match,
            "option_form_match": option_match,
            "local_candidate_sha256": (local or {}).get("candidate_text_sha256"),
            "external_candidate_sha256": (external or {}).get("answer_candidate_sha256"),
        },
        "difference_notes": notes,
        "source_authority_status": {
            "local": (local or {}).get("source_authority_status"),
            "external": (external or {}).get("source_authority_status"),
        },
        "scoring_status": "not_available_as_official",
        "mapping_level": "M0",
        "kp_id": "N/A",
        "review_status": "needs_manual_review" if status not in {"textually_consistent_unverified", "format_equivalent_unverified", "both_sources_missing"} else "candidate_only",
        "notes": [
            "比对层只记录候选之间的可追溯关系，不构成答案裁决、官方评分标准或知识点证据。",
            "新浪图像为带水印的第三方转载；本地解析卷为未核验本地来源。",
            "主 answer_index、原始 PDF、MinerU full.md 与题目切片均未修改。",
        ],
    }


def main() -> int:
    for path in (LOCAL, EXTERNAL, MAIN):
        if not path.exists():
            raise SystemExit(f"missing required source: {path}")
    main_sha = sha_bytes(MAIN.read_bytes())
    if main_sha != EXPECTED_MAIN_SHA256:
        raise SystemExit(f"main answer index changed unexpectedly: {main_sha}")
    local_rows = {int(r["question_id"]): r for r in load(LOCAL)}
    external_rows = {int(r["question_id"]): r for r in load(EXTERNAL)}
    if sorted(local_rows) != list(range(1, 22)):
        raise SystemExit(f"local coverage mismatch: {sorted(local_rows)}")
    if sorted(external_rows) != list(range(1, 21)):
        raise SystemExit(f"external coverage mismatch: {sorted(external_rows)}")
    rows = [classify(qid, local_rows.get(qid), external_rows.get(qid)) for qid in range(1, 22)]
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")

    counts: dict[str, int] = {}
    for row in rows:
        counts[row["comparison_status"]] = counts.get(row["comparison_status"], 0) + 1
    report_lines = [
        "---",
        'schema_version: "exam-reference-answer-candidate-comparison-0.1"',
        'status: "candidate_only_cross_source_comparison"',
        'authority_status: "both_sources_unverified"',
        'coverage: "GK-SC-2013 Q1-Q21; external Q1-Q20; local Q1-Q21"',
        'scoring_status: "not_available_as_official"',
        'mapping_status: "M0 | kp_id=N/A"',
        "---",
        "",
        "# 2013 四川卷答案候选交叉比对",
        "",
        "> 本报告只比较两个未核验候选层：带水印的新浪图像转录与本地解析卷候选。文本一致不等于官方核验；本层不修改主 `answer_index.jsonl`，不生成评分标准，也不升级教材知识点映射。",
        "",
        f"- 本地候选：`{rel(LOCAL)}`，Q1—Q21；新浪候选：`{rel(EXTERNAL)}`，Q1—Q20。",
        f"- 主答案索引 SHA-256：`{main_sha}`（固定门禁，21 条仍为 missing）。",
        f"- 比对 JSONL：`{rel(OUT)}`；共 {len(rows)} 条。",
        "- 判定计数：" + ", ".join(f"`{key}`={value}" for key, value in counts.items()) + "。",
        "",
        "## 逐题比对",
        "",
        "| 题号 | 本地候选 | 新浪候选 | 比对证据 | 判定 |",
        "|---:|---|---|---|---|",
    ]
    for row in rows:
        local_preview = (row["local_candidate"]["preview"] or "—").replace("|", "／")
        external_preview = (row["external_candidate"]["preview"] or "—").replace("|", "／")
        evidence = row["evidence"]
        evidence_text = "exact" if evidence["exact_text_match"] else "compact" if evidence["compact_text_match"] else "option" if evidence["option_form_match"] else "—"
        report_lines.append(f"| {row['question_id']} | {local_preview} | {external_preview} | `{evidence_text}` | `{row['comparison_status']}` |")
    report_lines += [
        "",
        "## 使用边界",
        "",
        "1. Q3、Q10、Q11、Q13 的本地字段是混合解析文本，未从解析内容反推答案。",
        "2. Q16—Q20 的差异保留为待复核事项；OCR、示例标签、答案长度差异均未静默修复。",
        "3. Q21 两层均没有独立答案；作文示例或写作指导不得替代评分标准。",
        "4. 所有记录保持 `scoring_status=not_available_as_official`、`mapping_level=M0`、`kp_id=N/A`。",
    ]
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    receipt = {
        "schema_version": "exam-reference-answer-candidate-comparison-receipt-0.1",
        "receipt_id": "EXAM-REFERENCE-ANSWER-CANDIDATE-COMPARISON-GK-SC-2013-20260809",
        "generated_at": now_text(),
        "status": "candidate_only_cross_source_comparison",
        "exam_id": EXAM_ID,
        "coverage": {"comparison_questions": list(range(1, 22)), "local_questions": list(local_rows), "external_questions": list(external_rows), "external_missing": [21]},
        "inputs": {
            "local": {"path": rel(LOCAL), "sha256": sha_bytes(LOCAL.read_bytes())},
            "external": {"path": rel(EXTERNAL), "sha256": sha_bytes(EXTERNAL.read_bytes())},
            "main_answer_index": {"path": rel(MAIN), "sha256": main_sha},
        },
        "output": {"path": rel(OUT), "sha256": sha_bytes(OUT.read_bytes()), "rows": len(rows)},
        "report": {"path": rel(REPORT), "sha256": sha_bytes(REPORT.read_bytes())},
        "counts": counts,
        "source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "候选交叉比对仅用于人工复核排队；一致性不等于官方核验，不把第三方答案或本地解析提升为评分标准。",
    }
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT), "counts": counts}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
