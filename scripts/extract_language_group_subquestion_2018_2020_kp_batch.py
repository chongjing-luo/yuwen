#!/usr/bin/env python3
"""Build M0 candidate records from the derived 2018--2020 Q7 subquestions."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPLIT_MANIFEST = ROOT / "work/knowledge/exams/workbench/kp_batches/language_group_subquestion_split_2018_2020.json"
OUT_DIR = ROOT / "work/knowledge/exams/workbench/kp_batches"
OUT_JSONL = OUT_DIR / "language_group_subquestion_2018_2020.jsonl"
OUT_MD = OUT_DIR / "language_group_subquestion_2018_2020.md"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 2)[-1].strip()


def subtype_action(name: str) -> tuple[str, str, list[str]]:
    values = {
        "idiom_usage": ("成语语境使用辨析", "结合语境辨析成语意义、感情色彩和搭配", ["语境义", "感情色彩", "搭配限制"]),
        "lexical_usage": ("词语语境使用辨析", "结合语境辨析近义词意义和搭配", ["语境义", "词语辨析", "搭配"]),
        "sequence_selection": ("语句衔接与语意连贯", "依据上下文逻辑和叙述对象选择衔接语句", ["语意衔接", "逻辑关系", "指代一致"]),
        "sentence_error": ("病句结构与语意辨析", "识别句式杂糅、搭配和成分问题并判断修改", ["句式杂糅", "搭配不当", "成分赘余"]),
        "completion": ("语句补写与语意连贯", "依据语段结构和上下文补写内容贴切的语句", ["语段结构", "语意连贯", "逻辑严密"]),
    }
    return values[name]


def evidence(text: str) -> tuple[str, list[str]]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    selected = [line for line in lines if any(marker in line for marker in ("考点", "能力层级", "试题分析", "成语", "词语", "衔接", "语病", "补写", "语段"))]
    joined = " ".join(selected[:8])
    levels: list[str] = []
    for match in re.finditer(r"能力层级(?:为|：|:)\s*([\u4e00-\u9fffA-Za-z0-9]+)", joined):
        if match.group(1) not in levels:
            levels.append(match.group(1))
    return joined, levels


def make_record(row: dict) -> dict:
    question_source = ROOT / row["question_source"]
    analysis_source = ROOT / row["analysis_source"]
    question = source_body(question_source)
    analysis = source_body(analysis_source)
    point, action, skills = subtype_action(row["candidate_subtype"])
    excerpt, levels = evidence(analysis)
    year = row["year"]
    return {
        "schema_version": "exam-kp-candidate-batch-0.1",
        "batch_id": "LANGUAGE-GROUP-SUBQUESTION-2018-2020",
        "exam_node_id": f"{row['exam_id']}-Q007-{row['subquestion_code']}",
        "parent_exam_node_id": f"{row['exam_id']}-Q007-TOP",
        "exam_id": row["exam_id"],
        "year": year,
        "question_id": 7,
        "subquestion_code": row["subquestion_code"],
        "question_type_l1": "language_use",
        "question_type_l2": "language_application",
        "candidate_subtype": row["candidate_subtype"],
        "response_form": "selected_response",
        "analysis_scope": "derived_subquestion_with_parent_group_context",
        "group_decomposition_status": "derived_boundary_candidate",
        "candidate_atomic_exam_point": point,
        "candidate_ability_action": action,
        "candidate_basis": "父题 Q007 的可逆小问边界、题干任务和解析候选考点；非正式知识点",
        "prompt_excerpt": question[:1200],
        "prompt_source": row["question_source"],
        "prompt_source_parent": row["parent_question_source"],
        "prompt_source_pdf": f"Data/2008-2024·（四川）语文高考真题/{year}年高考语文试卷（新课标Ⅲ卷）（空白卷）.pdf",
        "analysis_source": row["analysis_source"],
        "analysis_source_parent": row["parent_analysis_source"],
        "analysis_source_sha256": digest(analysis),
        "answer_candidate": None,
        "answer_candidate_method": "language_group_not_auto_extracted",
        "answer_candidate_status": "candidate_source_without_authoritative_answer",
        "analysis_contains_answer_marker": "答案" in analysis,
        "upstream_answer_source_status": "candidate_unverified",
        "source_authority_status": "unverified_local_provided",
        "score_candidate": None,
        "score_group_total": row["group_total"],
        "score_status": "group_total_only_not_allocated",
        "knowledge_evidence_excerpt": excerpt,
        "ability_level_candidates": levels,
        "subskill_candidates": skills,
        "manual_review_gate": "group_subquestion_answer_and_scoring_review_required",
        "source_warnings": ["分值仅登记父题 Q007 组总分；小问分值未从卷面独立核验，禁止均分或臆分。"],
        "ocr_status": "inherited_parent_review",
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "kp_mapping_status": "not_started",
        "na_reason": "小问答案/评分、分值分配和教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-batch-0.1"',
        'batch_id: "LANGUAGE-GROUP-SUBQUESTION-2018-2020"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 2018—2020 语言文字运用组题小问候选批次",
        "",
        "> 本批次把 2018—2020 Q7 组题拆成 9 个可逆小问文件。父题组总分保留，但小问分值不臆分；每条记录链接父题段、派生题干、派生解析、MinerU 和 PDF，答案全部不自动抽取。",
        "",
        "| 年份 | 节点 | 子类型 | 父题总分 | 小问分值 | 题干源 | 审核门 |",
        "|---:|---|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['year']} | `{row['exam_node_id']}` | `{row['candidate_subtype']}` | {row['score_group_total']} | `N/A` | [[{row['prompt_source']}|派生题干]] | `{row['manual_review_gate']}` |")
    lines += [
        "",
        "## 统计",
        "",
        f"- 总节点：{len(rows)}；年份分布：" + "、".join(f"{year}={sum(row['year']==year for row in rows)}" for year in (2018, 2019, 2020)) + "。",
        "- 小问分值全部保持 `N/A`；父题组总分分别为 2018=20、2019=9、2020=9，仅作为上游总分提示。",
        "",
        "## 复核规则",
        "",
        "1. 先逐页核对父题组边界和小问编号，再独立登记小问分值；不能用父题总分平均分配。",
        "2. 派生 Markdown 只用于定位和人工复核，不替代父题原始清洗源，也不承担独立官方页级定位。",
        "3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| 小问切分清单 | `work/knowledge/exams/workbench/kp_batches/language_group_subquestion_split_2018_2020.json` |",
        "| JSONL | `work/knowledge/exams/workbench/kp_batches/language_group_subquestion_2018_2020.jsonl` |",
        "| 本报告 | `work/knowledge/exams/workbench/kp_batches/language_group_subquestion_2018_2020.md` |",
        "| 切分脚本 | `scripts/split_language_group_subquestions_2018_2020.py` |",
        "| 生成脚本 | `scripts/extract_language_group_subquestion_2018_2020_kp_batch.py` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    manifest = json.loads(SPLIT_MANIFEST.read_text(encoding="utf-8"))
    rows = [make_record(row) for row in manifest["records"]]
    if len(rows) != 9:
        raise SystemExit(f"expected 9 records, got {len(rows)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "LANGUAGE-GROUP-SUBQUESTION-2018-2020", "record_count": len(rows), "subtype_counts": dict(Counter(row["candidate_subtype"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
