#!/usr/bin/env python3
"""Extract conservative candidate records for 2009--2015 literary reading."""
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
OUT_JSONL = OUT_DIR / "literary_reading_2009_2015.jsonl"
OUT_MD = OUT_DIR / "literary_reading_2009_2015.md"
EXPECTED_COUNTS = {year: 4 for year in range(2009, 2016)}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def literary_evidence(text: str) -> tuple[str, list[str]]:
    if not text:
        return "", []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    markers = ("鉴赏文学作品", "分析作品结构", "归纳内容要点", "概括作品主题", "重要语句", "形象", "思想内容", "创意的解读", "价值判断")
    selected = [line for line in lines if any(marker in line for marker in markers)]
    joined = " ".join(selected[:10])
    levels = []
    for match in re.finditer(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined):
        value = match.group(1)
        if value not in levels:
            levels.append(value)
    return joined, levels


def action_candidate(prompt: str) -> str:
    text = prompt or ""
    if "标题" in text or "作用" in text:
        return "结合内容与结构分析标题/段落/细节作用"
    if "赏析" in text or "句子" in text or "细节" in text or "形象" in text:
        return "结合文本证据赏析语言、形象与表达效果"
    if "情感" in text or "主旨" in text or "思想" in text:
        return "筛选文本证据并概括情感、主旨或价值判断"
    if "思考" in text or "赞成" in text or "理解" in text:
        return "基于文本证据进行开放性阐释并说明理由"
    return "理解文本并筛选、概括文学作品信息"


def load_nodes() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("GK-SC-*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if 2009 <= row.get("year", 0) <= 2015 and row.get("question_type_l2") == "literary_reading":
                rows.append(row)
    return sorted(rows, key=lambda row: (row["year"], row["response_node_id"]))


def make_record(row: dict) -> dict:
    analysis_path = ROOT / row["source_analysis_segment"] if row.get("source_analysis_segment") else None
    analysis = body(analysis_path)
    evidence, levels = literary_evidence(analysis)
    upstream_status = row.get("answer_source_status")
    if upstream_status == "missing":
        status = "candidate_source_without_answer_text_authority_missing" if analysis else "missing_analysis_source"
        gate = "source_authority_missing"
    elif analysis:
        status = "literary_candidate_source"
        gate = "literary_answer_and_scoring_review_required"
    else:
        status = "missing_analysis_source"
        gate = "answer_source_missing"
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "LITERARY-READING-2009-2015",
        "exam_node_id": row["response_node_id"],
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": row.get("question_type_l2"),
        "response_form": "literary_reading_response",
        "analysis_scope": "question_segment_with_possible_related_context",
        "candidate_atomic_exam_point": "文学作品形象、语言、结构、主题与鉴赏表达",
        "candidate_ability_action": action_candidate(row.get("prompt_excerpt")),
        "candidate_basis": "题型标签、题干任务和解析候选中的文学阅读考点描述；非正式知识点",
        "prompt_excerpt": row.get("prompt_excerpt"),
        "prompt_source": row.get("source_question_segment"),
        "prompt_source_pdf": row.get("source_pdf"),
        "analysis_source": row.get("source_analysis_segment"),
        "analysis_source_sha256": digest(analysis) if analysis else None,
        "answer_candidate": None,
        "answer_candidate_method": "literary_response_not_auto_extracted",
        "answer_candidate_status": status,
        "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": upstream_status,
        "source_authority_status": "missing" if upstream_status == "missing" else "unverified_local_provided",
        "score_candidate": row.get("score"),
        "score_status": row.get("score_allocation_status", row.get("score_basis")),
        "knowledge_evidence_excerpt": evidence,
        "ability_level_candidates": levels,
        "subskill_candidates": ["形象鉴赏", "语言品味", "结构作用", "主题概括", "开放探究"],
        "manual_review_gate": gate,
        "source_warnings": row.get("source_warnings", []),
        "ocr_status": row.get("ocr_status"),
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "na_reason": "文学阅读答案/评分独立核验与教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "LITERARY-READING-2009-2015"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 文学类文本阅读小问级知识点候选批次（2009—2015）",
        "",
        "> 本批次覆盖小说/散文阅读中的形象、语言、结构、主题和开放探究。老解析段可能携带同组关联上下文，因此不自动生成答案或评分点；所有记录保持 `M0 / kp_id=N/A`。",
        "",
        "| 年份 | 节点 | 分值 | 解析状态 | 候选作答动作 | 审核门 |",
        "|---:|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['year']} | `{row['exam_node_id']}` [[{row['prompt_source']}|题干]] | {row['score_candidate'] or 'N/A'} | `{row['answer_candidate_status']}` | {row['candidate_ability_action']} | `{row['manual_review_gate']}` |")
    counts = Counter(row["answer_candidate_status"] for row in rows)
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；文学阅读解析候选源：{counts.get('literary_candidate_source', 0)}；2013 年权威缺失：{counts.get('candidate_source_without_answer_text_authority_missing', 0)}。",
        "- `analysis_scope=question_segment_with_possible_related_context` 表示题目段可能含同组关联上下文；解析结论不得跨小问复制。",
        "- `answer_candidate` 全部保持空值，解析中出现“答案”字样不表示答案已核验。",
        "",
        "## 复核规则",
        "",
        "1. 逐页核对文本、材料、题干、选项、分值和 OCR/水印疑点。",
        "2. 按小问分别登记文本证据、作答要点、评分点和解析来源；共享上下文不得替代小问证据。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL | `work/knowledge/高考分析/kp_batches/literary_reading_2009_2015.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/literary_reading_2009_2015.md` |",
        "| 生成脚本 | `scripts/extract_literary_reading_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = [make_record(row) for row in load_nodes()]
    if len(rows) != 28:
        raise SystemExit(f"expected 28 nodes, got {len(rows)}")
    actual = Counter(row["year"] for row in rows)
    if dict(actual) != EXPECTED_COUNTS:
        raise SystemExit(f"unexpected year counts: {dict(actual)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "LITERARY-READING-2009-2015", "record_count": len(rows), "year_counts": dict(actual), "status_counts": dict(Counter(row["answer_candidate_status"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
