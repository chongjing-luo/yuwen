#!/usr/bin/env python3
"""Extract conservative candidate records for 2021--2024 translation tasks.

The national-甲卷 records use a shared Q13 analysis segment for the two
translation sentences.  This batch keeps that scope explicit and never
turns a reference translation in an analysis PDF into an official answer or
scoring point.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from extract_word_pronunciation_kp_batch import body

ROOT = Path(__file__).resolve().parents[1]
SLICE_DIR = ROOT / "work/knowledge/高考分析"
OUT_DIR = SLICE_DIR / "kp_batches"
OUT_JSONL = OUT_DIR / "classical_translation_2021_2024.jsonl"
OUT_MD = OUT_DIR / "classical_translation_2021_2024.md"
EXPECTED_COUNTS = {2021: 1, 2022: 1, 2023: 1, 2024: 2}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def translation_evidence(text: str) -> tuple[str, str | None]:
    """Keep task/ability markers only; do not copy reference translations."""
    if not text:
        return "", None
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = (
        "翻译成现代汉语",
        "理解并翻译文中句子",
        "翻译文言文",
        "翻译文中的句子",
        "理解并翻译文言文句子",
    )
    selected = [line.split("【答案】", 1)[0].strip() for line in lines if any(marker in line for marker in markers)]
    ability_lines = [line for line in lines if "能力层级" in line and "翻译" in line]
    joined = " ".join((selected + ability_lines)[:4])
    match = re.search(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined)
    return joined, match.group(1) if match else None


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-NCA-202[1-4]-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2021 <= row.get("year", 0) <= 2024 and row.get("question_type_l2") == "classical_translation":
                rows.append(row)
    return sorted(rows, key=lambda row: (row["year"], row["response_node_id"]))


def make_record(row: dict) -> dict:
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    evidence, level = translation_evidence(analysis)
    upstream_status = row.get("upstream_answer_source_status") or row.get("answer_source_status") or "unknown"
    if analysis:
        status = "free_response_candidate_source"
        gate = "free_response_answer_and_scoring_review_required"
    else:
        status = "missing_analysis_source"
        gate = "answer_source_missing"
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "CLASSICAL-TRANSLATION-2021-2024",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": row.get("question_type_l2"),
        "response_form": "free_response_translation",
        "analysis_scope": "shared_top_level_analysis_segment",
        "candidate_atomic_exam_point": "文言文句子翻译",
        "candidate_ability_action": "理解句意，识别关键实词/虚词/句式并准确翻译",
        "candidate_basis": "题型标签、题干任务和解析候选中的翻译考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None,
        "answer_candidate_method": "free_response_not_auto_extracted",
        "answer_candidate_status": status,
        "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": upstream_status,
        "source_authority_status": "unverified_local_provided" if upstream_status != "missing" else "missing",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": evidence,
        "ability_level_candidate": level,
        "subskill_candidates": ["关键实词虚词释义", "句式识别", "语意连贯转换"],
        "manual_review_gate": gate,
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "自由作答答案/评分独立核验与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "CLASSICAL-TRANSLATION-2021-2024"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 文言文翻译小问级知识点候选批次（2021—2024）",
        "",
        "> 本批次覆盖 2021—2024 全国甲卷 Q13。2021—2023 为题目级节点（每题含两句），2024 已有两个小问节点；共享解析段仅作为证据来源，不自动生成官方译文或评分点。所有记录保持 `M0 / kp_id=N/A`。",
        "",
        "| 年份 | 节点 | 分值 | 解析状态 | 候选考点 | 审核门 |",
        "|---:|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | {row['score_candidate'] or 'N/A'} | `{row['answer_candidate_status']}` | {row['candidate_atomic_exam_point']} | `{row['manual_review_gate']}` |"
        )
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；解析候选源：{counts.get('free_response_candidate_source', 0)}；缺少解析源：{counts.get('missing_analysis_source', 0)}。",
        "- `answer_candidate` 全部保持空值；解析中出现“答案”字样不表示答案或评分点已核验。",
        "",
        "## 复核规则",
        "",
        "1. 逐页核对题干、横线句、分值和 OCR/水印疑点；2021—2023 的两句不能臆拆分值。",
        "2. 独立登记译文候选、关键词采分点、句式处理和评分标准；不得把解析示例直接当官方评分。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/高考分析/kp_batches/classical_translation_2021_2024.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/classical_translation_2021_2024.md` |",
        "| 生成脚本 | `scripts/extract_classical_translation_2021_2024_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = [make_record(row) for row in load_nodes()]
    if len(rows) != sum(EXPECTED_COUNTS.values()):
        raise SystemExit(f"expected {sum(EXPECTED_COUNTS.values())} nodes, got {len(rows)}")
    actual = Counter(row["year"] for row in rows)
    if dict(actual) != EXPECTED_COUNTS:
        raise SystemExit(f"unexpected year counts: {dict(actual)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(
        json.dumps(
            {
                "batch": "CLASSICAL-TRANSLATION-2021-2024",
                "record_count": len(rows),
                "year_counts": dict(actual),
                "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
