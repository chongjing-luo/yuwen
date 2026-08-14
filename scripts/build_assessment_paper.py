#!/usr/bin/env python3
"""组卷器（S8 环节）：从 blueprint + item_bank 同源生成学生卷与教师卷（含评分量规）。

同源纪律（P-11）：学生卷只含 in_student_paper 条目；真题参照条目只进教师卷
「变式题库」附录，并保留全部溯源字段。

用法：python3 scripts/build_assessment_paper.py <blueprint.json> [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "work/knowledge/assessment/item_bank.jsonl"


def load_bank() -> dict[str, dict]:
    return {item["item_id"]: item for item in (json.loads(l) for l in BANK_PATH.read_text(encoding="utf-8").splitlines() if l.strip())}


def build_student_paper(blueprint: dict, bank: dict) -> str:
    lines = [f"# {blueprint['title']}（学生卷）", ""]
    lines.append(f"满分 {blueprint['total_score']} 分 · 建议 {blueprint['total_minutes']} 分钟 · 闭卷")
    lines.append("")
    lines.append("作答说明：简答题按论证质量而非立场给分；引用诗句为证时，注明哪些是诗里写出的、哪些是你的推断。")
    lines.append("")
    number = 0
    for entry in blueprint["items"]:
        item = bank[entry["bank_ref"]]
        if not entry.get("in_student_paper", True):
            continue
        number += 1
        lines.append(f"## 第 {number} 题（{item['type']} · {item['score']} 分）")
        lines.append("")
        lines.append(item["stem"])
        lines.append("")
        if item.get("normal_path"):
            lines.append(f"*如果一时没有想法：{item['normal_path']}*")
            lines.append("")
    lines.append("---")
    lines.append("交卷后：错题订正在订正栏完成，错字回炉；订正痕迹会计入你的学习记录。")
    lines.append("")
    return "\n".join(lines)


def build_teacher_paper(blueprint: dict, bank: dict) -> str:
    lines = [f"# {blueprint['title']}（教师卷与评分量规）", ""]
    lines.append(f"- 蓝图：{blueprint['blueprint_id']}")
    scope = blueprint.get("scope", {})
    lines.append(f"- 单元：{scope.get('unit_ref')}；知识卡：{', '.join(scope.get('card_refs', []))}")
    lines.append(f"- 课程数据：{scope.get('lesson_ref')}")
    lines.append(f"- 关联作业：{scope.get('homework_ref')}（间隔检索，K3）")
    lines.append("")
    lines.append("## KP 权重与依据")
    lines.append("")
    lines.append("| KP | 权重 | 依据 |")
    lines.append("|---|---|---|")
    for w in blueprint["kp_weights"]:
        lines.append(f"| {w['kp_id']} | {w['weight']} | {w['basis']} |")
    lines.append("")
    number = 0
    for entry in blueprint["items"]:
        item = bank[entry["bank_ref"]]
        if not entry.get("in_student_paper", True):
            continue
        number += 1
        lines.append(f"## 第 {number} 题（{item['type']} · {item['score']} 分）{item['item_id']}")
        lines.append("")
        lines.append(f"- **KP**：{', '.join(item.get('kp_ids', []))}")
        if item.get("expected_evidence"):
            lines.append(f"- **预期证据**：{item['expected_evidence']}")
        lines.append(f"- **正常反例路径**：{item.get('normal_path', '—')}")
        lines.append("- **评分点**：")
        for point in item.get("scoring_points", []):
            lines.append(f"  - {point['score']} 分：{point['point']}")
        lines.append("")
    lines.append("## 评分原则")
    lines.append("")
    for principle in blueprint.get("scoring_principles", []):
        lines.append(f"- {principle}")
    lines.append("")
    ref_items = [bank[e["bank_ref"]] for e in blueprint["items"] if not e.get("in_student_paper", True)]
    if ref_items:
        lines.append("## 变式题库（真题参照，不进学生卷）")
        lines.append("")
        for item in ref_items:
            lines.append(f"### {item['item_id']}（{item['exam_id']} {item['year']} · {item['type']}）")
            lines.append("")
            lines.append(f"- 题干摘录：{item['stem']}")
            lines.append(f"- KP 候选（M0 未映射）：{item.get('kp_candidate', '—')}")
            lines.append(f"- 原题路径：`{item.get('prompt_source', '—')}`")
            lines.append(f"- 解析 SHA-256：`{item.get('analysis_source_sha256', '—')}`")
            lines.append(f"- 使用说明：{item.get('usage_note', '—')}")
            lines.append("")
    lines.append("## 边界声明")
    lines.append("")
    lines.append(blueprint.get("claim_boundary", ""))
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blueprint")
    parser.add_argument("--out-dir")
    args = parser.parse_args()

    bp_path = Path(args.blueprint)
    if not bp_path.is_absolute():
        bp_path = ROOT / bp_path
    blueprint = json.loads(bp_path.read_text(encoding="utf-8"))
    bank = load_bank()

    for entry in blueprint["items"]:
        if entry["bank_ref"] not in bank:
            print(f"[error] 题库中不存在: {entry['bank_ref']}")
            return 1

    out_dir = Path(args.out_dir) if args.out_dir else bp_path.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    student = out_dir / f"学生卷_{blueprint['blueprint_id']}.md"
    teacher = out_dir / f"教师卷与评分量规_{blueprint['blueprint_id']}.md"
    student.write_text(build_student_paper(blueprint, bank), encoding="utf-8")
    teacher.write_text(build_teacher_paper(blueprint, bank), encoding="utf-8")
    print(f"学生卷 → {student}")
    print(f"教师卷与评分量规 → {teacher}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
