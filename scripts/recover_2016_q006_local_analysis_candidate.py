#!/usr/bin/env python3
"""Recover the Q006 answer block from its already-separated local segment.

The 2016 answer index lost Q006 when the upstream解析 field crossed the Q005
boundary.  The reviewed ``segments/analysis/Q006.md`` still contains a
separate, explicit ``【解答】`` block.  This script snapshots that block as a
local candidate and compares it with the existing third-party candidate.  It
never mutates ``answer_index.jsonl``, PDFs, MinerU output, or question text.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016"
SEGMENT = BASE / "segments/analysis/Q006.md"
MAIN = BASE / "answers/answer_index.jsonl"
THIRD_PARTY = BASE / "answers/reference_answer_candidates_q006_gzywtk.jsonl"
OUT = BASE / "answers/reference_answer_candidates_q006_local_analysis.jsonl"
REPORT = ROOT / "work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATE-RECOVERY-2016-Q006.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidate_recovery_GK-NC3-2016-Q006_20260809.json"
VALIDATION = ROOT / "work/knowledge/_meta/reference_answer_candidate_validation_2016_q006_local_20260809.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(text: str) -> str:
    return sha_bytes(text.encode("utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def now_text() -> str:
    return datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds")


def frontmatter_value(text: str, key: str) -> str | None:
    match = re.search(rf'(?m)^{re.escape(key)}:\s*"([^"]+)"$', text)
    return match.group(1) if match else None


def extract_answer(text: str) -> tuple[str, str, str]:
    start_marker = "【解答】"
    end_marker = "【点评】"
    start = text.index(start_marker) + len(start_marker)
    end = text.index(end_marker, start)
    block = text[start:end].strip()
    if not block:
        raise RuntimeError("Q006 local analysis answer block is empty")
    return block, start_marker, end_marker


def load_third_party() -> dict:
    rows = [json.loads(line) for line in THIRD_PARTY.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 1 or rows[0].get("question_id") != 6:
        raise RuntimeError("expected exactly one third-party Q006 candidate")
    return rows[0]


def compact(text: str) -> str:
    return re.sub(r"[\s，。；：、．.（）()①②③④（）]", "", text)


def main() -> int:
    segment_text = SEGMENT.read_text(encoding="utf-8")
    candidate, answer_marker, end_marker = extract_answer(segment_text)
    third = load_third_party()
    third_text = third.get("answer_candidate_text") or ""
    required = ["答B给3分", "坚持独立思考", "天下兴亡", "匹夫有责"]
    if any(term not in candidate for term in required):
        raise RuntimeError("local Q006 candidate failed content guard")
    comparison = {
        "third_party_candidate_id": third.get("candidate_id"),
        "exact_text_match": candidate == third_text,
        "compact_text_match": compact(candidate) == compact(third_text),
        "local_sha256": sha_text(candidate),
        "third_party_sha256": third.get("answer_candidate_sha256"),
        "shared_content_guards": {term: term in candidate and term in third_text for term in required},
        "differences": [
            "本地解析切片含分小问换行与标点；第三方候选将小问答案压为连续段落。",
            "本地切片在第（3）小问后保留孤立‘1人’残片，第三方候选未保留；该残片按 OCR/版面污染处理。",
            "本地切片为‘爱国主义传统’，第三方候选为‘爱国注意传统’，存在文字差异，不能静默裁决。",
        ],
    }
    row = {
        "schema_version": "exam-reference-answer-candidate-0.2",
        "candidate_id": "GK-NC3-2016-Q006-LOCAL-ANALYSIS-ANSWER",
        "exam_id": "GK-NC3-2016",
        "question_id": 6,
        "source_role": "answer_scoring_candidate",
        "candidate_status": "candidate_unverified",
        "candidate_scope": "local_analysis_segment_q006",
        "source_authority_status": "unverified_local_provided",
        "source_status": "unverified_local_provided",
        "answer_source_status": "local_analysis_segment_candidate",
        "scoring_status": "not_available_as_official",
        "mapping_level": "M0",
        "kp_id": "N/A",
        "candidate_content_type": "recovered_reference_answer_candidate",
        "answer_candidate_text": candidate,
        "answer_candidate_sha256": sha_text(candidate),
        "source_segment": rel(SEGMENT),
        "source_segment_sha256": sha_bytes(SEGMENT.read_bytes()),
        "source_segment_clean_sha256": frontmatter_value(segment_text, "segment_clean_sha256"),
        "source_pdf": "Data/2008-2024·（四川）语文高考真题/2016年高考语文试卷（新课标Ⅲ卷）（解析卷）.pdf",
        "source_mineru_md": "Data/2008-2024·（四川）语文高考真题/mineru_result/2016年高考语文试卷（新课标Ⅲ卷）（解析卷）/full.md",
        "source_answer_index": rel(MAIN),
        "answer_marker": answer_marker,
        "end_marker": end_marker,
        "external_comparison": comparison,
        "review_status": "needs_cross_source_adjudication",
        "notes": [
            "候选从已独立切出的 Q006 解析段恢复；不从 Q005 复合字段推断。",
            "该切片与本地解析 PDF 同源，不是独立权威来源；仅作为第三方候选的结构/文本交叉证据。",
            "主 answer_index Q006 仍保持 N/A；不得把本候选当作官方答案或评分标准。",
        ],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-reference-answer-candidate-0.2"\n'
        'status: "candidate_only_local_recovery"\n'
        'authority_status: "unverified_local_provided"\n'
        'coverage: "GK-NC3-2016 Q006"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2016 全国卷Ⅲ Q006 本地解析切片恢复候选\n\n"
        "> Q006 的 `answer_index` 仍为空；本文件只从已单独切出的解析段恢复候选答案，并与一苇轩候选做文本差异记录。两者均未达到官方答案/评分标准门槛。\n\n"
        f"- 本地解析切片：`{rel(SEGMENT)}`\n"
        f"- 切片 SHA-256：`{sha_bytes(SEGMENT.read_bytes())}`\n"
        f"- 恢复候选：`{rel(OUT)}`\n"
        f"- 对照候选：`{rel(THIRD_PARTY)}`\n"
        f"- 精确文本一致：`{str(comparison['exact_text_match']).lower()}`；去空白/标点后一致：`{str(comparison['compact_text_match']).lower()}`\n\n"
        "## 差异与边界\n\n"
        "- 本地切片保留分小问换行和一个疑似 OCR/版面残片 `1人`。\n"
        "- 本地切片写作“爱国主义传统”，第三方候选写作“爱国注意传统”；差异暂不裁决。\n"
        "- 主索引、原始 PDF、MinerU `full.md` 均未修改；知识点映射继续保持 M0。\n",
        encoding="utf-8",
    )
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-recovery-receipt-0.1",
        "receipt_id": "EXAM-REFERENCE-ANSWER-RECOVERY-GK-NC3-2016-Q006-20260809",
        "generated_at": now_text(),
        "status": "candidate_only_local_recovery",
        "source_mutation": False,
        "answer_index_mutation": False,
        "source_segment": rel(SEGMENT),
        "source_segment_sha256": sha_bytes(SEGMENT.read_bytes()),
        "output": rel(OUT),
        "output_sha256": sha_bytes(OUT.read_bytes()),
        "report": rel(REPORT),
        "report_sha256": sha_bytes(REPORT.read_bytes()),
        "comparison": comparison,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "本地解析切片仅作候选；同源切片与第三方转载的文本一致不等于官方核验，不写回主答案索引。",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidate": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT), "comparison": comparison}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
