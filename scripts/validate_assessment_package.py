#!/usr/bin/env python3
"""命题组卷校验器（机制节点 K1/K3/K4/U6；S8 环节出口）。

校验 blueprint + item_bank：
1. 蓝图 items 全部解析到题库；学生卷题目与题型分布（count/score）一致；总分守恒；
2. K1：kp_weights 的每个 KP 被至少一道学生卷题目覆盖；题目 kp_ids 解析到知识卡；
3. K3：测评是知识四站闭环的第三站——蓝图必须引用 lesson_ref 与 homework_ref；
4. U6：每道学生卷主观题的 scoring_points 分值合计 == 题分；评分原则含解释分层要求；
5. 真题参照条目（candidate_only_M0）不得进入学生卷，且必须有 prompt_source 与 sha 溯源；
6. U1/P-07：学生卷题干不含前台禁词；
7. P-12：claim_boundary 声明桌面/课堂两本账。

用法：python3 scripts/validate_assessment_package.py <blueprint.json>
退出码：0 通过；1 失败。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANK_PATH = ROOT / "work/knowledge/assessment/item_bank.jsonl"
KP_ID_PATTERN = re.compile(r"KP-CARD-[A-Z0-9-]+-\d{3}")


def load_bank() -> dict[str, dict]:
    bank = {}
    for line in BANK_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            bank[item["item_id"]] = item
    return bank


def card_kp_ids(card_id: str) -> set[str]:
    matches = list((ROOT / "work/knowledge").glob(f"*/cards/{card_id}*.md"))
    if not matches:
        return set()
    return set(KP_ID_PATTERN.findall(matches[0].read_text(encoding="utf-8")))


def validate(blueprint: dict, bank: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for field in ("blueprint_id", "kp_weights", "type_distribution", "items", "total_score", "total_minutes", "claim_boundary"):
        if field not in blueprint:
            errors.append(f"缺少顶层字段: {field}")
    if errors:
        return errors, warnings

    # 1. 解析与守恒
    student_items: list[dict] = []
    for entry in blueprint["items"]:
        ref = entry.get("bank_ref")
        item = bank.get(ref)
        if item is None:
            errors.append(f"题库中不存在: {ref}")
            continue
        merged = {**item, "in_student_paper": entry.get("in_student_paper", True)}
        if merged["in_student_paper"]:
            if "score" not in merged or "time_minutes" not in merged:
                errors.append(f"{ref}: 进入学生卷的题目必须有 score 与 time_minutes")
            else:
                student_items.append(merged)

    for dist in blueprint["type_distribution"]:
        count = sum(1 for i in student_items if i["type"] == dist["type"])
        if count != dist["count"]:
            errors.append(f"题型 {dist['type']}：分布要求 {dist['count']} 题，学生卷实际 {count} 题")
        score = sum(i["score"] for i in student_items if i["type"] == dist["type"])
        if score != dist["score"]:
            errors.append(f"题型 {dist['type']}：分布要求 {dist['score']} 分，学生卷实际 {score} 分")
    total = sum(i["score"] for i in student_items)
    if total != blueprint["total_score"]:
        errors.append(f"总分不守恒：学生卷合计 {total}，蓝图声明 {blueprint['total_score']}")
    total_time = sum(i["time_minutes"] for i in student_items)
    if total_time > blueprint["total_minutes"]:
        errors.append(f"答题时长 {total_time} 分钟超过蓝图 {blueprint['total_minutes']} 分钟")

    # 2. KP 覆盖与解析
    scope = blueprint.get("scope", {})
    card_kps: set[str] = set()
    for card_id in scope.get("card_refs", []):
        kps = card_kp_ids(card_id)
        if not kps:
            errors.append(f"知识卡不存在或无 KP: {card_id}")
        card_kps |= kps
    for weight in blueprint["kp_weights"]:
        if weight["kp_id"] not in card_kps:
            errors.append(f"kp_weights 的 {weight['kp_id']} 未解析到范围知识卡")
        if not str(weight.get("basis") or "").strip():
            errors.append(f"kp_weights 的 {weight['kp_id']} 缺 weight 依据（K1：权重须来自图谱或语料统计）")
        if weight["kp_id"] not in {kp for i in student_items for kp in i.get("kp_ids", [])}:
            errors.append(f"kp_weights 的 {weight['kp_id']} 无学生卷题目覆盖")
    for item in student_items:
        for kp in item.get("kp_ids", []):
            if kp not in card_kps:
                errors.append(f"{item['item_id']}: kp_id 超出蓝图范围: {kp}")

    # 3. 四站闭环引用
    if not scope.get("lesson_ref"):
        errors.append("蓝图必须引用 lesson_ref（测评回收是四站闭环第三站，K3）")
    if not scope.get("homework_ref"):
        errors.append("蓝图必须引用 homework_ref（与作业检索构成间隔排程，K3）")

    # 4. 评分量规
    for item in student_items:
        points = item.get("scoring_points") or []
        if not points:
            errors.append(f"{item['item_id']}: 缺 scoring_points")
            continue
        if sum(p["score"] for p in points) != item["score"]:
            errors.append(f"{item['item_id']}: scoring_points 合计 {sum(p['score'] for p in points)} ≠ 题分 {item['score']}")
    principles = json.dumps(blueprint.get("scoring_principles", []), ensure_ascii=False)
    if "分层" not in principles and "推断" not in principles:
        errors.append("scoring_principles 须包含解释分层要求（U6：推断写成诗写须可检出）")

    # 5. 真题参照纪律
    for entry in blueprint["items"]:
        item = bank.get(entry.get("bank_ref"))
        if item is None:
            continue
        if item.get("candidate_status") == "candidate_only_M0":
            if entry.get("in_student_paper", True):
                errors.append(f"{item['item_id']}: candidate_only 条目不得进入学生卷（M0 未映射且无官方答案核验）")
            if not item.get("prompt_source") or not item.get("analysis_source_sha256"):
                errors.append(f"{item['item_id']}: 真题参照缺 prompt_source/sha256 溯源")

    # 6. 前台禁词
    config_path = ROOT / "work/principles/enforcement_config.json"
    banned: list[str] = []
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        banned = config.get("frontstage_banned_v6", []) + config.get("frontstage_banned_v5", [])
    for item in student_items:
        for word in banned:
            if word in item.get("stem", ""):
                errors.append(f"{item['item_id']}: 题干含后台词「{word}」")

    # 7. 诚实边界
    boundary = blueprint.get("claim_boundary", "")
    if "课堂" not in boundary and "施测" not in boundary:
        errors.append("claim_boundary 未声明待真实施测（P-12）")

    if not any(i.get("normal_path") for i in student_items):
        warnings.append("学生卷题目建议配 normal_path（U7：反例路径同样适用于测验）")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("blueprint")
    args = parser.parse_args()

    bp_path = Path(args.blueprint)
    if not bp_path.is_absolute():
        bp_path = ROOT / bp_path
    blueprint = json.loads(bp_path.read_text(encoding="utf-8"))
    errors, warnings = validate(blueprint, load_bank())

    for warning in warnings:
        print(f"[warn] {warning}")
    for error in errors:
        print(f"[error] {error}")
    if errors:
        print(f"命题包校验失败：{len(errors)} 错误")
        return 1
    student_count = sum(1 for e in blueprint["items"] if e.get("in_student_paper", True))
    print(f"命题包校验通过：学生卷 {student_count} 题 / 总分 {blueprint['total_score']} / {blueprint['total_minutes']} 分钟")
    return 0


if __name__ == "__main__":
    sys.exit(main())
