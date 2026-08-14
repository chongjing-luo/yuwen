#!/usr/bin/env python3
"""Build conservative M0 candidate records from 2018--2020 Q8/Q9 tasks."""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "work/knowledge/高考分析/kp_batches/language_application_tasks_split_2018_2020.json"
OUT_DIR = ROOT / "work/knowledge/高考分析/kp_batches"
OUT_JSONL = OUT_DIR / "language_application_tasks_2018_2020.jsonl"
OUT_MD = OUT_DIR / "language_application_tasks_2018_2020.md"


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def source_body(path: Path) -> str:
    return path.read_text(encoding="utf-8").split("---\n\n", 1)[1].strip()


def action(subtype: str) -> tuple[str, list[str]]:
    values = {
        "pragmatic_register": ("依据交际对象、场合和语体修改不得体表达", ["谦敬语", "书面语体", "交际场合"]),
        "diagram_conversion": ("读取图示关系并转换为完整连贯的文字", ["图文转换", "信息组织", "连贯表达"]),
        "completion": ("依据上下文逻辑和句式照应补写语段", ["语意连贯", "逻辑衔接", "句式照应"]),
        "summary": ("提取新闻时间、主体、事件和结果并压缩表达", ["新闻要素", "信息筛选", "简洁表达"]),
    }
    return values[subtype]


def make_record(row: dict) -> dict:
    parent_path = ROOT / row["parent_source"]
    parent_text = source_body(parent_path)
    act, skills = action(row["candidate_subtype"])
    warnings = ["派生任务边界未替代官方小问定位；父题总分不分摊。"]
    if row["year"] == 2020 and row["question_id"] == 8:
        warnings.append("父题保留 OCR/排版残片‘11’，需人工回看 PDF。")
    if row.get("source_image_paths"):
        warnings.append("图示原图链路已保留，需人工复核图中信息与题干边界。")
    return {
        "schema_version": "exam-kp-candidate-task-batch-0.1",
        "batch_id": "LANGUAGE-APPLICATION-TASKS-2018-2020",
        "exam_node_id": f"{row['exam_id']}-Q{row['question_id']:03d}-{row['task_code']}",
        "parent_exam_node_id": f"{row['exam_id']}-Q{row['question_id']:03d}-TOP",
        "exam_id": row["exam_id"],
        "year": row["year"],
        "question_id": row["question_id"],
        "task_code": row["task_code"],
        "task_label": row["task_label"],
        "task_kind": row["task_kind"],
        "question_type_l1": "language_use",
        "question_type_l2": "language_application",
        "candidate_subtype": row["candidate_subtype"],
        "response_form": "constructed_response",
        "analysis_scope": "derived_task_with_parent_question_context",
        "task_decomposition_status": "derived_boundary_candidate",
        "candidate_atomic_exam_point": {
            "pragmatic_register": "语言得体与语体选择",
            "diagram_conversion": "图文转换与连贯表达",
            "completion": "语句补写与语意连贯",
            "summary": "新闻压缩与信息概括",
        }[row["candidate_subtype"]],
        "candidate_ability_action": act,
        "candidate_basis": "题干任务形式和可逆任务边界；非正式知识点，不替代教材 KP",
        # Use the parent question body for retrieval context.  The derived
        # wrapper is intentionally excluded so its boundary declaration is
        # never mistaken for exam wording.
        "prompt_excerpt": re.sub(r"\s+", " ", parent_text)[:1600],
        "task_source": row["task_source"],
        "parent_source": row["parent_source"],
        "parent_source_sha256": row["parent_sha256"],
        "source_pdf": row["source_pdf"],
        "source_mineru_md": row["source_mineru_md"],
        "source_clean_md": row["source_clean_md"],
        "source_image_paths": row.get("source_image_paths", []),
        "task_source_sha256": row["task_sha256"],
        "answer_candidate": None,
        "answer_candidate_method": "language_application_task_not_auto_extracted",
        "answer_candidate_status": "candidate_source_without_authoritative_answer",
        "score_candidate": None,
        "score_question_total": row["question_total"],
        "score_status": "question_total_only_not_allocated",
        "ability_level_candidates": [],
        "subskill_candidates": skills,
        "manual_review_gate": "task_answer_and_scoring_review_required",
        "source_warnings": warnings,
        "ocr_status": "suspected_ocr_or_watermark_noise" if row["year"] == 2020 and row["question_id"] == 8 else "inherited_parent_review",
        "kp_id": "N/A",
        "mapping_level": "M0",
        "review_status": "candidate_only",
        "kp_mapping_status": "not_started",
        "na_reason": "任务答案/官方评分和教材KP双向证据尚未闭合。",
    }


def render(rows: list[dict]) -> str:
    lines = [
        "---",
        'schema_version: "exam-kp-candidate-task-batch-0.1"',
        'batch_id: "LANGUAGE-APPLICATION-TASKS-2018-2020"',
        'status: "candidate_only"',
        'mapping_status: "M0_only"',
        "---",
        "",
        "# 2018—2020 语言文字运用 Q8/Q9 任务候选批次",
        "",
        "> 本批次将 2018—2020 Q8/Q9 按稳定任务边界派生为 14 个候选任务节点（每个题干/解析各有一个可逆文件）。父题原文不变；答案、评分和教材 KP 映射均不自动生成，全部保持 M0。",
        "",
        "| 年份 | 节点 | 子类型 | 父题总分 | 任务分值 | 题干任务源 | 审核门 |",
        "|---:|---|---|---:|---|---|---|",
    ]
    for row in rows:
        lines.append(f"| {row['year']} | `{row['exam_node_id']}` | `{row['candidate_subtype']}` | {row['score_question_total']} | `N/A` | [[{row['task_source']}|派生任务]] | `{row['manual_review_gate']}` |")
    lines += [
        "",
        "## 审核边界",
        "",
        "1. 任务文件保留完整父题上下文，只增加边界声明；不能替代父题清洗源。",
        "2. 2018 Q008 的五处修改、2019/2020 Q008 的三个空是候选任务单位，不把解析中的修订/补写文本写入答案字段。",
        "3. Q009 是单一压缩或图文转换任务；图示、OCR 和水印疑点按源字段保留。",
        "4. 只有题文—官方答案/评分—教材 KP 三方闭合后，才允许升级 M1 以上。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| 任务切分清单 | `work/knowledge/高考分析/kp_batches/language_application_tasks_split_2018_2020.json` |",
        "| JSONL | `work/knowledge/高考分析/kp_batches/language_application_tasks_2018_2020.jsonl` |",
        "| 本报告 | `work/knowledge/高考分析/kp_batches/language_application_tasks_2018_2020.md` |",
        "| 切分脚本 | `scripts/split_language_application_tasks_2018_2020.py` |",
        "| 生成脚本 | `scripts/extract_language_application_tasks_2018_2020_kp_batch.py` |",
        "| 验证报告 | `work/knowledge/_meta/language_application_tasks_2018_2020_kp_batch_validation_20260809.json` |",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    unit_rows = [row for row in manifest["records"] if row["source_role"] == "question"]
    rows = [make_record(row) for row in unit_rows]
    if len(rows) != 14:
        raise SystemExit(f"expected 14 question task records, got {len(rows)}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    OUT_MD.write_text(render(rows), encoding="utf-8")
    print(json.dumps({"batch": "LANGUAGE-APPLICATION-TASKS-2018-2020", "record_count": len(rows), "subtype_counts": dict(Counter(row["candidate_subtype"] for row in rows))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
