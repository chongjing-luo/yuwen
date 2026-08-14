#!/usr/bin/env python3
"""Create reversible task-unit Markdown files for 2018--2020 Q8/Q9.

The upstream Q008/Q009 segments are never rewritten.  The derived files keep
the complete parent context and add only a declared task boundary, so a
reviewer can always walk back to the original cleaned segment, MinerU output,
PDF and (when present) source image.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAM_ROOT = ROOT / "Data/2008-2024·（四川）语文高考真题"
OUT = ROOT / "work/knowledge/高考分析/kp_batches/language_application_tasks_split_2018_2020.json"

TARGETS = {
    (2018, 8): {
        "question_total": 4,
        "subtype": "pragmatic_register",
        "task_kind": "appropriateness_edit",
        "slots": [
            ("1", "不得体用语①“教书”", "题干五处修改任务中的第一处候选边界；词语出现在父题原文。"),
            ("2", "不得体用语②“光临”", "题干五处修改任务中的第二处候选边界；词语出现在父题原文。"),
            ("3", "不得体用语③“惠赠”", "题干五处修改任务中的第三处候选边界；词语出现在父题原文。"),
            ("4", "不得体用语④“先睹为快”", "题干五处修改任务中的第四处候选边界；词语出现在父题原文。"),
            ("5", "不得体用语⑤“快来了”", "题干五处修改任务中的第五处候选边界；词语出现在父题原文。"),
        ],
    },
    (2018, 9): {
        "question_total": 6,
        "subtype": "diagram_conversion",
        "task_kind": "diagram_to_prose",
        "slots": [("1", "整题图文转换任务", "单一作答任务；四种反应的图示作为不可替代的材料整体保留。")],
    },
    (2019, 8): {
        "question_total": 6,
        "subtype": "completion",
        "task_kind": "fill_blanks",
        "slots": [
            ("1", "补写空①", "题干明确标出的第一处补写空；保留语段上下文。"),
            ("2", "补写空②", "题干明确标出的第二处补写空；保留语段上下文。"),
            ("3", "补写空③", "题干明确标出的第三处补写空；保留语段上下文。"),
        ],
    },
    (2019, 9): {
        "question_total": 5,
        "subtype": "summary",
        "task_kind": "news_compression",
        "slots": [("1", "整题新闻压缩任务", "单一作答任务；时间、地点、事件和结果均属于同一题干边界。")],
    },
    (2020, 8): {
        "question_total": 6,
        "subtype": "completion",
        "task_kind": "fill_blanks",
        "slots": [
            ("1", "补写空①", "题干明确标出的第一处补写空；保留语段上下文。"),
            ("2", "补写空②", "题干明确标出的第二处补写空；保留语段上下文。"),
            ("3", "补写空③", "题干明确标出的第三处补写空；保留语段上下文。"),
        ],
    },
    (2020, 9): {
        "question_total": 5,
        "subtype": "summary",
        "task_kind": "news_compression",
        "slots": [("1", "整题新闻压缩任务", "单一作答任务；会议、政策与投资结果属于同一题干边界。")],
    },
}


def digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_parent(path: Path) -> tuple[dict[str, str], str]:
    text = path.read_text(encoding="utf-8")
    if "---\n\n" not in text:
        raise ValueError(f"missing front matter separator: {path}")
    front, body = text.split("---\n\n", 1)
    values: dict[str, str] = {}
    for line in front.removeprefix("---\n").splitlines():
        match = re.match(r"([A-Za-z0-9_]+):\s*(.*)$", line.strip())
        if not match:
            continue
        value = match.group(2).strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1]
        values[match.group(1)] = value
    return values, body.strip()


def image_sources(body: str, mineru_md: str) -> list[str]:
    """Resolve image links from the parent body against its MinerU folder."""
    mineru = ROOT / mineru_md if mineru_md else None
    paths: list[str] = []
    for filename in re.findall(r"images/([A-Za-z0-9._-]+\.(?:jpg|jpeg|png))", body, flags=re.I):
        if mineru:
            candidate = mineru.parent / "images" / filename
            if candidate.exists():
                paths.append(candidate.relative_to(ROOT).as_posix())
                continue
        paths.append(f"images/{filename}")
    return list(dict.fromkeys(paths))


def render(
    year: int,
    qid: int,
    role: str,
    code: str,
    label: str,
    basis: str,
    task: dict,
    parent: Path,
    parent_values: dict[str, str],
    parent_body: str,
) -> str:
    exam_id = parent_values.get("exam_id", f"GK-NC3-{year}")
    parent_rel = parent.relative_to(ROOT).as_posix()
    images = image_sources(parent_body, parent_values.get("source_mineru_md", ""))
    warnings = ["该文件为可逆任务边界派生，不承载独立官方页级定位。"]
    if year == 2020 and qid == 8:
        warnings.append("父题清洗文本保留 OCR/排版残片“11”；不得静默删除或解释。")
    if images:
        warnings.append("父题含图示；图像路径和 MinerU 原图链路必须人工复核。")
    node_id = f"{exam_id}-Q{qid:03d}-{code}"
    lines = [
        "---",
        'schema_version: "exam-question-task-0.1"',
        f'canonical_question_id: "{exam_id}-Q{qid:03d}"',
        f'response_node_id: "{node_id}"',
        f'exam_id: "{exam_id}"',
        f"question_id: {qid}",
        f'task_code: "{code}"',
        f'task_label: "{label}"',
        f'task_kind: "{task["task_kind"]}"',
        f'candidate_subtype: "{task["subtype"]}"',
        f'source_role: "{role}"',
        'question_type_l1: "language_use"',
        'question_type_l2: "language_application"',
        'derivation_status: "derived_task_boundary"',
        f'parent_segment: "{parent_rel}"',
        f'parent_segment_sha256: "{digest(parent_body)}"',
        f'source_pdf: "{parent_values.get("source_pdf", "")}"',
        f'source_mineru_md: "{parent_values.get("source_mineru_md", "")}"',
        f'source_clean_md: "{parent_values.get("source_clean_md", "")}"',
        f'source_image_paths: {json.dumps(images, ensure_ascii=False)}',
        f'source_pdf_page_start: {parent_values.get("source_pdf_page_start", "null")}',
        f'source_pdf_page_end: {parent_values.get("source_pdf_page_end", "null")}',
        'locator_status: "inherited_parent_page_level_fallback"',
        'review_status: "needs_manual_review"',
        "---",
        "",
        f"# 派生任务单元：{label}",
        "",
        f"- 任务边界依据：{basis}",
        f"- 原始父题：[[{parent_rel}|Q{qid:03d} 父题段]]",
        f"- 原始 MinerU：[[{parent_values.get('source_mineru_md', '')}|full.md]]",
        f"- 原始 PDF：[[{parent_values.get('source_pdf', '')}|PDF]]",
        f"- 清洗整卷：[[{parent_values.get('source_clean_md', '')}|clean.md]]",
        f"- 对应父题解析/题干：[[{parent_rel}|{role} 父题]]",
    ]
    if images:
        lines.append("- 图示原图：" + "；".join(f"[[{path}|{Path(path).name}]]" for path in images))
    lines += [
        "- 本文件只增加任务边界声明，完整父题正文如下；父题、解析、答案包均未修改。",
        "",
        "## 父题全文（保留上下文）",
        "",
        parent_body,
        "",
        "## 派生边界与风险",
        "",
        f"- `task_code={code}`；父题总分={task['question_total']} 分；本文件不臆造任务单元分值。",
        "- " + "\n- ".join(warnings),
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    records: list[dict] = []
    for (year, qid), task in TARGETS.items():
        for role in ("question", "analysis"):
            parent = EXAM_ROOT / f"exam_extract/GK-NC3-{year}/segments/{role}/Q{qid:03d}.md"
            values, parent_body = split_parent(parent)
            for code, label, basis in task["slots"]:
                out = parent.parent / "subquestions" / f"Q{qid:03d}-{code}.md"
                out.parent.mkdir(parents=True, exist_ok=True)
                out.write_text(render(year, qid, role, code, label, basis, task, parent, values, parent_body), encoding="utf-8")
                records.append({
                    "exam_id": values.get("exam_id", f"GK-NC3-{year}"),
                    "year": year,
                    "question_id": qid,
                    "task_code": code,
                    "task_label": label,
                    "task_kind": task["task_kind"],
                    "candidate_subtype": task["subtype"],
                    "question_total": task["question_total"],
                    "source_role": role,
                    "task_source": out.relative_to(ROOT).as_posix(),
                    "parent_source": parent.relative_to(ROOT).as_posix(),
                    "parent_sha256": digest(parent_body),
                    "task_sha256": digest(out.read_text(encoding="utf-8").split("---\n\n", 1)[1].strip()),
                    "source_pdf": values.get("source_pdf", ""),
                    "source_mineru_md": values.get("source_mineru_md", ""),
                    "source_clean_md": values.get("source_clean_md", ""),
                    "source_image_paths": image_sources(parent_body, values.get("source_mineru_md", "")),
                    "boundary_basis": basis,
                })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"schema_version": "exam-language-task-split-0.1", "status": "candidate", "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"record_count": len(records), "task_unit_count": len(records) // 2, "manifest": str(OUT.relative_to(ROOT))}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
