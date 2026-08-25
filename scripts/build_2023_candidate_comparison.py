#!/usr/bin/env python3
"""Compare 2023 local group candidates with the partial EOL snapshot."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM_ID = "GK-NCA-2023"
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract" / EXAM_ID
LOCAL = BASE / "answers/local_analysis_group_candidates.jsonl"
EXTERNAL = BASE / "answers/reference_answer_candidates.jsonl"
OUT = BASE / "answers/reference_answer_candidate_comparison.jsonl"
REPORT = ROOT / "work/knowledge/exams/workbench/EXAM-REFERENCE-ANSWER-CANDIDATE-COMPARISON-2023.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidate_comparison_GK-NCA-2023_20260809.json"


def sha(text: str | None) -> str | None:
    return hashlib.sha256(text.encode("utf-8")).hexdigest() if text else None


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def compact(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    return re.sub(r"[\s，,。；;：:、．.（）()【】「」‘’“”《》!?！？\-—_]+", "", text)


def preview(text: str) -> str | None:
    return re.sub(r"\s+", " ", text).strip()[:120] if text else None


def summary(text: str) -> dict:
    return {"sha256": sha(text), "compact_sha256": sha(compact(text)), "char_count": len(text), "preview": preview(text)}


def main() -> int:
    if not LOCAL.exists() or not EXTERNAL.exists():
        raise SystemExit("missing local group or external candidate layer")
    local_rows = {int(r["question_id"]): r for r in (json.loads(x) for x in LOCAL.read_text(encoding="utf-8").splitlines() if x.strip())}
    external_rows = {int(r["question_id"]): r for r in (json.loads(x) for x in EXTERNAL.read_text(encoding="utf-8").splitlines() if x.strip())}
    if sorted(local_rows) != list(range(1, 23)):
        raise SystemExit(f"local coverage mismatch: {sorted(local_rows)}")
    if sorted(external_rows) != [1, 2, 3, 6, 7, 8, 9, 10]:
        raise SystemExit(f"external coverage mismatch: {sorted(external_rows)}")
    rows: list[dict] = []
    for qid in range(1, 23):
        local = local_rows[qid]
        external = external_rows.get(qid)
        local_text = local.get("candidate_text") or ""
        external_text = (external or {}).get("answer_candidate_text") or ""
        exact = bool(local_text and external_text and local_text == external_text)
        compact_match = bool(local_text and external_text and compact(local_text) == compact(external_text))
        if qid == 22 and local.get("candidate_status") == "candidate_writing_artifact":
            status = "writing_artifact_no_external"
            notes = ["本地‘例文’材料保留为写作边界，不是评分标准；外部候选也未覆盖。"]
        elif local_text and external_text:
            status = "textually_consistent_unverified" if exact or compact_match else "text_difference_requires_review"
            notes = ["本地共享答案块与中国教育在线第三方候选可进行文本比较；一致不等于官方核验。"]
        elif external_text and not local_text:
            status = "local_mixed_analysis_no_explicit_answer"
            notes = ["外部候选存在，但本地题段没有独立答案文本；不从本地分析段反推。"]
        elif local_text:
            status = "external_source_missing_local_candidate_only"
            notes = ["本地候选存在，但外部快照未覆盖该题；不得把本地候选升级为官方答案。"]
        else:
            status = "external_missing_local_mixed_analysis"
            notes = ["外部候选未覆盖，且本地仅有混合解析文本；答案状态保持缺失。"]
        rows.append({
            "schema_version": "exam-reference-answer-candidate-comparison-0.1",
            "comparison_id": f"{EXAM_ID}-Q{qid:03d}-CANDIDATE-COMPARISON",
            "exam_id": EXAM_ID,
            "question_id": qid,
            "comparison_status": status,
            "adjudication": "not_adjudicated",
            "local_candidate_id": local.get("candidate_id"),
            "external_candidate_id": (external or {}).get("candidate_id"),
            "local_candidate_source": rel(LOCAL),
            "external_candidate_source": rel(EXTERNAL) if external else None,
            "local_candidate_available": bool(local_text),
            "external_candidate_available": bool(external_text),
            "local_candidate": summary(local_text),
            "external_candidate": summary(external_text),
            "evidence": {
                "exact_text_match": exact,
                "compact_text_match": compact_match,
                "local_candidate_sha256": local.get("candidate_text_sha256"),
                "external_candidate_sha256": (external or {}).get("answer_candidate_sha256"),
            },
            "source_authority_status": {
                "local": local.get("source_authority_status"),
                "external": (external or {}).get("source_authority_status"),
            },
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "review_status": "needs_manual_review" if status not in {"textually_consistent_unverified", "external_missing_local_mixed_analysis", "writing_artifact_no_external"} else "candidate_only",
            "difference_notes": notes,
            "notes": [
                "比对层仅记录两个未核验候选层的关系，不构成答案裁决、官方评分标准或知识点证据。",
                "主答案索引、原始 PDF、MinerU full.md、清洗稿和题目切片均未修改。",
            ],
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["comparison_status"]] = counts.get(row["comparison_status"], 0) + 1
    report_lines = [
        "---",
        'schema_version: "exam-reference-answer-candidate-comparison-0.1"',
        'status: "candidate_only_cross_source_comparison"',
        'authority_status: "both_sources_unverified"',
        'coverage: "GK-NCA-2023 Q1-Q22; external Q1-Q3,Q6-Q10"',
        'scoring_status: "not_available_as_official"',
        'mapping_status: "M0 | kp_id=N/A"',
        "---",
        "",
        "# 2023 全国甲卷答案候选交叉比对",
        "",
        "> 本报告比较本地解析共享答案块切分层与中国教育在线第三方答案快照。外部来源只覆盖 Q1—Q3、Q6—Q10；其余题号不使用搜索摘要或解析推断补齐。文本一致不等于官方核验。",
        "",
        f"- 本地切分候选：`{rel(LOCAL)}`，Q1—Q22。",
        f"- 外部候选：`{rel(EXTERNAL)}`，Q1—Q3、Q6—Q10。",
        f"- 比对 JSONL：`{rel(OUT)}`；共 {len(rows)} 条。",
        "- 判定计数：" + ", ".join(f"`{key}`={value}" for key, value in counts.items()) + "。",
        "",
        "## 逐题比对",
        "",
        "| 题号 | 本地候选 | 外部候选 | 证据 | 判定 |",
        "|---:|---|---|---|---|",
    ]
    for row in rows:
        evidence = row["evidence"]
        evidence_text = "exact" if evidence["exact_text_match"] else "compact" if evidence["compact_text_match"] else "—"
        report_lines.append(f"| {row['question_id']} | {(row['local_candidate']['preview'] or '—').replace('|', '／')} | {(row['external_candidate']['preview'] or '—').replace('|', '／')} | `{evidence_text}` | `{row['comparison_status']}` |")
    report_lines += [
        "",
        "## 使用边界",
        "",
        "1. Q1—Q3、Q4—Q6、Q7—Q9、Q14—Q15、Q17—Q21 的本地共享答案块仅按显式题号切分，源块题号归属和边界哈希均保留。",
        "2. Q10—Q13、Q16 的本地字段无可安全分离答案，未从解析文字反推；Q22 的‘例文’不是评分标准。",
        "3. 外部快照缺失题号保持缺失；所有记录保持 `not_available_as_official`、`M0 / kp_id=N/A`。",
    ]
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    receipt = {
        "schema_version": "exam-reference-answer-candidate-comparison-receipt-0.1",
        "receipt_id": "EXAM-REFERENCE-ANSWER-CANDIDATE-COMPARISON-GK-NCA-2023-20260809",
        "generated_at": now_text(),
        "exam_id": EXAM_ID,
        "inputs": {
            "local": {"path": rel(LOCAL), "sha256": file_sha(LOCAL)},
            "external": {"path": rel(EXTERNAL), "sha256": file_sha(EXTERNAL)},
        },
        "output": {"path": rel(OUT), "sha256": file_sha(OUT), "rows": len(rows)},
        "report": {"path": rel(REPORT), "sha256": file_sha(REPORT)},
        "counts": counts,
        "source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "部分外部候选只用于可追溯比对；不把文本一致升级为官方答案或评分标准。",
    }
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "counts": counts, "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
