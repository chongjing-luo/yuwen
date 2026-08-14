#!/usr/bin/env python3
"""Build a cross-year, question-type review queue from vertical slices.

The queue is a derived planning layer.  It extracts no official answers and
does not create textbook mappings.  Every record remains ``M0 / kp_id=N/A``;
the type label is only a candidate atomic exam-point description for manual
review.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLICE_DIR = ROOT / "work/knowledge/高考分析"
OUT_JSONL = SLICE_DIR / "exam_type_review_queue.jsonl"
OUT_DIR = SLICE_DIR / "type_review_queue"
OUT_REPORT = SLICE_DIR / "EXAM-TYPE-KP-REVIEW-QUEUE-20260809.md"

TYPE_POINT = {
    "word_pronunciation": "现代汉语普通话字音辨析",
    "orthography": "现代汉字字形辨析",
    "word_usage": "词语/熟语语境使用辨析",
    "idiom_usage": "成语语境使用辨析",
    "sentence_error": "病句结构与语意辨析",
    "sentence_grammar": "病句结构与语意辨析",
    "sequence": "语句衔接与语意连贯",
    "summary": "材料信息压缩与概括",
    "summary_or_application": "信息概括与应用表达",
    "completion": "语句补写与语意连贯",
    "sentence_expansion": "仿写、扩写与修辞表达",
    "parallelism_or_practical": "修辞组织与应用表达",
    "practical_or_expansion": "应用写作或语句扩展",
    "metaphor_series": "修辞辨析与表达效果",
    "modern_reading_informational": "现代文信息筛选、概括与推断",
    "ancient_vocab": "文言实词语境释义",
    "ancient_function_words": "文言虚词意义和用法辨析",
    "ancient_text_content": "文言文内容概括与分析",
    "ancient_text_evidence": "文言文信息筛选与证据判断",
    "ancient_reading": "文言文断句、文化常识与内容理解",
    "sentence_segmentation": "文言文句读与断句",
    "classical_translation": "文言句子翻译",
    "poetry_appreciation": "古代诗歌形象、情感与表达手法鉴赏",
    "classical_memorization": "名篇名句理解性默写",
    "literary_reading": "文学类文本形象、结构、语言与主题鉴赏",
    "meaning_explanation": "文学文本词句含义与表达效果",
    "structure_effect": "文学文本结构作用与表达效果",
    "practical_reading": "实用类文本信息、结构与表达目的分析",
    "topic_writing": "材料作文立意、构思与书面表达",
    "language_application": "语言文字运用中的衔接、补写、辨析与表达",
}


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def compact(text: str, limit: int = 600) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if len(text) <= limit else text[:limit].rstrip() + "…"


def gate_for(row: dict) -> str:
    if row.get("answer_source_status") == "missing":
        return "answer_source_missing"
    if row.get("ocr_status") == "suspected_ocr_or_watermark_noise":
        return "ocr_or_watermark_review"
    if row.get("content_acceptance") == "conditional_review":
        return "conditional_content_review"
    if row.get("decomposition_status") != "response_nodes_derived":
        return "decomposition_review"
    return "candidate_ready_for_manual_kp_review"


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(SLICE_DIR.glob("*-response_nodes_vertical_slice.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def build_record(row: dict) -> dict:
    point = TYPE_POINT.get(row.get("question_type_l2"), "待人工核定的原子考点")
    prompt = row.get("prompt_text_for_extraction") or row.get("prompt_text") or row.get("prompt_text_raw") or ""
    node_id = row["response_node_id"]
    qtype = row.get("question_type_l2") or "unclassified"
    source_question = row.get("source_question_segment")
    source_analysis = row.get("source_analysis_segment")
    gate = gate_for(row)
    return {
        "schema_version": "exam-type-review-queue-0.1",
        "queue_id": f"QUEUE-{qtype}-{node_id}",
        "exam_node_id": node_id,
        "exam_id": row.get("exam_id"),
        "year": row.get("year"),
        "question_id": row.get("question_id"),
        "subquestion_code": row.get("subquestion_code"),
        "question_type_l1": row.get("question_type_l1"),
        "question_type_l2": qtype,
        "candidate_atomic_exam_point": point,
        "candidate_basis": "question_type_l2 plus extracted prompt; not a confirmed knowledge point",
        "prompt_excerpt": compact(prompt),
        "prompt_sha256": sha256_text(prompt),
        "score": row.get("score"),
        "score_allocation_status": row.get("score_allocation_status"),
        "answer_source_status": row.get("answer_source_status"),
        "source_question_segment": source_question,
        "source_analysis_segment": source_analysis,
        "source_pdf": row.get("source_pdf"),
        "source_mineru_md": row.get("source_mineru_md"),
        "source_clean_md": row.get("source_clean_md"),
        "material_id": row.get("material_id"),
        "source_locator_status": row.get("source_locator_status"),
        "ocr_status": row.get("ocr_status"),
        "content_acceptance": row.get("content_acceptance"),
        "decomposition_status": row.get("decomposition_status"),
        "manual_review_gate": gate,
        "four_layer": "N/A",
        "four_wings": "N/A",
        "context_type": "N/A",
        "kp_id": "N/A",
        "mapping_level": "M0",
        "na_reason": "题型候选尚未完成小问级答案/评分与教材KP双向证据核验。",
        "review_status": "queue_only",
    }


def wikilink(path: str | None, label: str) -> str:
    return f"[[{path}|{label}]]" if path else "N/A"


def render_type(type_name: str, rows: list[dict]) -> str:
    point = TYPE_POINT.get(type_name, "待人工核定")
    lines = [
        "---",
        'schema_version: "exam-type-review-queue-0.1"',
        f'type: "{type_name}"',
        'mapping_status: "M0_only"',
        "---",
        "",
        f"# 题型清洗队列：{type_name}",
        "",
        f"> 候选原子考点：{point}。此描述只由题型和题干推断，不能替代小问级答案/评分复核，也不构成教材映射。",
        "",
        "| 节点 | 年份 | 题段 | 清洗稿 | 原始来源 | 解析源 | 分值 | 答案源 | 审核门 |",
        "|---|---:|---|---|---|---|---:|---|---|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['exam_node_id']}` | {row.get('year','N/A')} | "
            f"{wikilink(row.get('source_question_segment'), '题干')} | "
            f"{wikilink(row.get('source_clean_md'), '清洗稿')} | "
            f"{wikilink(row.get('source_mineru_md'), '原始 MinerU')}<br>"
            f"{wikilink(row.get('source_pdf'), '原始 PDF')} | "
            f"{wikilink(row.get('source_analysis_segment'), '解析候选')} | "
            f"{row.get('score','N/A')} | `{row.get('answer_source_status','N/A')}` | "
            f"`{row['manual_review_gate']}` |"
        )
    lines += [
        "",
        "## 人工核验字段",
        "",
        "- 先回看题段、清洗稿、原始 MinerU 与原始 PDF，确认小问边界和 OCR/水印疑点。",
        "- 再回看解析候选；答案与评分点分开记录，不能把解析段落整体作为答案。",
        "- 最后再检查教材 KP 的双向证据；没有闭合证据时保持 `M0 / kp_id=N/A`。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    rows = [build_record(row) for row in load_rows()]
    rows.sort(key=lambda row: (row["question_type_l2"], row.get("year") or 0, row["exam_node_id"]))
    OUT_JSONL.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["question_type_l2"]].append(row)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for type_name, type_rows in grouped.items():
        (OUT_DIR / f"{type_name}.md").write_text(render_type(type_name, type_rows), encoding="utf-8")
    counts = Counter(row["question_type_l2"] for row in rows)
    gates = Counter(row["manual_review_gate"] for row in rows)
    lines = [
        "---",
        'schema_version: "exam-type-review-queue-0.1"',
        'status: "candidate_queue"',
        'mapping_status: "M0_only"',
        f"node_count: {len(rows)}",
        "---",
        "",
        "# 跨年度题型—知识点人工清洗队列",
        "",
        "> 输入为 2008—2024 垂直切片的 359 个作答节点。队列按 `question_type_l2` 归并；每个题型页面显式保留题干、清洗稿、原始 MinerU、原始 PDF 和解析候选（如有）的双链。它不修改上游，不宣称官方答案，不建立教材 KP 映射。",
        "",
        f"- 作答节点：{len(rows)}；题型数：{len(grouped)}。",
        f"- 候选答案源：{sum(row.get('answer_source_status') == 'candidate_unverified' for row in rows)}；明确缺失：{sum(row.get('answer_source_status') == 'missing' for row in rows)}。",
        "",
        "> 补充批次说明：2018—2020 Q8/Q9 的 14 个任务单元已另行登记于 `kp_batches/language_application_tasks_2018_2020.jsonl`，不重复并入本 359 条顶层作答队列；其题干/解析派生文件、父题哈希和 M0 门禁见对应批次报告。",
        "",
        "## 审核门分布",
        "",
        "| 审核门 | 数量 | 处理含义 |",
        "|---|---:|---|",
        f"| `candidate_ready_for_manual_kp_review` | {gates.get('candidate_ready_for_manual_kp_review', 0)} | 可进入小问级答案/评分与教材 KP 对照，但仍保持 M0 |",
        f"| `ocr_or_watermark_review` | {gates.get('ocr_or_watermark_review', 0)} | 先处理 OCR/水印疑点，不得静默改写 |",
        f"| `conditional_content_review` | {gates.get('conditional_content_review', 0)} | 先完成 PDF/边界条件复核 |",
        f"| `answer_source_missing` | {gates.get('answer_source_missing', 0)} | 补来源或显式保持缺失 |",
        f"| `decomposition_review` | {gates.get('decomposition_review', 0)} | 先稳定小问边界 |",
        "",
        "## 题型汇总",
        "",
        "| 题型 | 节点数 | 候选考点描述 | 队列文件 |",
        "|---|---:|---|---|",
    ]
    for type_name in sorted(grouped):
        lines.append(f"| `{type_name}` | {counts[type_name]} | {TYPE_POINT.get(type_name, '待人工核定')} | [[work/knowledge/高考分析/type_review_queue/{type_name}.md|打开]] |")
    lines += [
        "",
        "## 放行规则",
        "",
        "1. 题段、清洗稿、原始 MinerU、原始 PDF 和解析候选（如有）定位一致，才允许进入小问级知识点草拟。",
        "2. 评分只能记录为题面候选或官方评分；没有独立评分材料时保持未核验。",
        "3. `candidate_atomic_exam_point` 只是检索标签；`atomic_exam_point`、四层、四翼和教材 KP 关系仍不得写入正式节点。",
        "4. 只有题文—答案/评分—教材 KP 三方证据闭合，才允许从 M0 升级 M1 以上。",
        "",
        "| 产物 | 路径 |",
        "|---|---|",
        "| JSONL 队列 | `work/knowledge/高考分析/exam_type_review_queue.jsonl` |",
        "| 题型目录 | `work/knowledge/高考分析/type_review_queue/` |",
        "| 生成脚本 | `scripts/build_exam_type_review_queue.py` |",
        "",
    ]
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"node_count": len(rows), "type_count": len(grouped), "gates": dict(gates), "report": str(OUT_REPORT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
