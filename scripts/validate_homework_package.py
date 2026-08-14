#!/usr/bin/env python3
"""作业包校验器（机制节点 K1/K3/K5/U3/U7/U8；原则 N-02 及 S7 环节出口）。

检查一份 homework_package.json：
1. 结构与字段完整（item_id 唯一、分层合法、每题 kp_ids/预期证据/反馈触发/反例路径非空）；
2. K3/N-02：必含闭卷检索题；U8：必含迁移变式题；
3. K5/U5：必做时长与总时长不超过 max_total_time_minutes；
4. K1：kp_ids 与 kp_scope 全部解析到知识卡的真实 KP；scope 内 KP 被覆盖或在 deferred 有理由；
5. page_refs 解析到课程数据真实页；
6. U1/P-07：题干（学生可见）不含前台禁词；
7. P-12：claim_boundary 存在且声明桌面/课堂边界。

用法：
  python3 scripts/validate_homework_package.py <homework_package.json> [--report OUT.json]
退出码：0 通过；1 失败。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALID_TIERS = {"巩固", "迁移", "延伸"}
VALID_MODES = {"闭卷检索", "开卷回证", "应用"}
KP_ID_PATTERN = re.compile(r"KP-CARD-[A-Z0-9-]+-\d{3}")


def load_lesson_page_ids(lesson_js: str | None) -> set[str] | None:
    if not lesson_js:
        return None
    result = subprocess.run(
        ["node", "-e", "const l=require(process.argv[1]);console.log(JSON.stringify(l.pages.map(p=>p.page_id)))", str((ROOT / lesson_js).resolve())],
        capture_output=True,
        text=True,
        check=True,
        cwd=ROOT,
    )
    return set(json.loads(result.stdout))


def card_kp_ids(card_path: Path) -> set[str]:
    return set(KP_ID_PATTERN.findall(card_path.read_text(encoding="utf-8")))


def validate(package: dict, package_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    def err(msg):
        errors.append(msg)

    for field in ("schema_version", "homework_id", "lesson_ref", "kp_scope", "items", "max_total_time_minutes", "claim_boundary"):
        if field not in package:
            err(f"缺少顶层字段: {field}")
    if errors:
        return errors, warnings

    items = package["items"]
    if not items:
        err("items 为空")

    # 1. 结构
    seen_ids: set[str] = set()
    for item in items:
        iid = item.get("item_id", "?")
        if iid in seen_ids:
            err(f"{iid}: item_id 重复")
        seen_ids.add(iid)
        if item.get("tier") not in VALID_TIERS:
            err(f"{iid}: tier 非法: {item.get('tier')!r}")
        if item.get("retrieval_mode") not in VALID_MODES:
            err(f"{iid}: retrieval_mode 非法: {item.get('retrieval_mode')!r}")
        for field in ("prompt", "expected_evidence", "feedback_trigger", "normal_path"):
            if not str(item.get(field) or "").strip():
                err(f"{iid}: {field} 为空（预期证据/反馈触发/反例路径是 U3/U7 的落点字段）")
        if not item.get("kp_ids"):
            err(f"{iid}: kp_ids 为空（K1：每题必须绑定知识点）")
        if not item.get("page_refs"):
            err(f"{iid}: page_refs 为空（作业应回链课堂落点）")
        if not isinstance(item.get("time_budget_minutes"), int) or item["time_budget_minutes"] <= 0:
            err(f"{iid}: time_budget_minutes 必须为正整数")

    # 2. 机制底线
    modes = {i.get("retrieval_mode") for i in items}
    tiers = {i.get("tier") for i in items}
    if "闭卷检索" not in modes:
        err("N-02/K3：作业包必须包含至少一道闭卷检索题（检索练习效应）")
    if "迁移" not in tiers:
        err("U8：作业包必须包含至少一道迁移变式题（理解第四层）")
    if "巩固" not in tiers:
        err("K3：作业包应包含巩固层（当日核心 KP 的闭卷激活）")

    # 3. 时长负担
    consolidation = sum(i["time_budget_minutes"] for i in items if i.get("tier") == "巩固")
    transfers = [i["time_budget_minutes"] for i in items if i.get("tier") == "迁移"]
    required = consolidation + (min(transfers) if transfers else 0)
    total = sum(i["time_budget_minutes"] for i in items)
    max_total = package["max_total_time_minutes"]
    if required > max_total:
        err(f"必做时长 {required} 分钟超过上限 {max_total}（K5/U5 负荷预算）")
    if total > max_total and "选做" not in json.dumps(package.get("tiers", {}), ensure_ascii=False):
        err(f"总时长 {total} 分钟超过上限 {max_total}，且未标注选做分层")
    package["__required_time"] = required
    package["__total_time"] = total

    # 4. KP 解析与覆盖
    knowledge_dir = ROOT / "work/knowledge"
    all_card_kps: set[str] = set()
    lesson_ref = package["lesson_ref"]
    for ref in lesson_ref.get("card_refs", []) + [c.get("card_id") for c in lesson_ref.get("cross_book_refs", []) if isinstance(c, dict)]:
        matches = list(knowledge_dir.glob(f"*/cards/{ref}.md"))
        if not matches:
            err(f"知识卡不存在: {ref}")
            continue
        all_card_kps |= card_kp_ids(matches[0])
    for item in items:
        for kp in item.get("kp_ids", []):
            if kp not in all_card_kps:
                err(f"{item.get('item_id')}: kp_id 未解析到知识卡: {kp}")
    scope = package["kp_scope"]
    scope_kps = scope.get("kp_ids", [])
    deferred = {d.get("kp_id") for d in scope.get("deferred", []) if isinstance(d, dict)}
    for kp in scope_kps:
        if kp not in all_card_kps:
            err(f"kp_scope 包含未解析 KP: {kp}")
    covered = {kp for i in items for kp in i.get("kp_ids", [])}
    for kp in scope_kps:
        if kp not in covered and kp not in deferred:
            err(f"kp_scope 的 {kp} 既无作业覆盖也无 defer 理由")
    for d in scope.get("deferred", []):
        if not str(d.get("reason") or "").strip():
            err(f"deferred 项 {d.get('kp_id')} 缺理由")

    # 5. 页引用
    page_ids = load_lesson_page_ids(lesson_ref.get("lesson_js"))
    if page_ids is not None:
        for item in items:
            for ref in item.get("page_refs", []):
                if ref not in page_ids:
                    err(f"{item.get('item_id')}: page_ref 不在课程数据中: {ref}")
    elif lesson_ref.get("lesson_js"):
        err(f"课程数据不存在: {lesson_ref.get('lesson_js')}")

    # 6. 前台禁词
    config_path = ROOT / "work/principles/enforcement_config.json"
    banned: list[str] = []
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        banned = config.get("frontstage_banned_v6", []) + config.get("frontstage_banned_v5", [])
    for item in items:
        text = f"{item.get('prompt', '')}\n{item.get('normal_path', '')}"
        for word in banned:
            if word in text:
                err(f"{item.get('item_id')}: 学生可见文字含后台词「{word}」")

    # 7. 诚实边界
    boundary = package.get("claim_boundary", "")
    if "课堂" not in boundary or "桌面" not in boundary:
        warnings.append("claim_boundary 应同时声明桌面设计与待课堂验证（两本账）")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", help="homework_package.json 路径")
    parser.add_argument("--report")
    args = parser.parse_args()

    package_path = Path(args.package)
    if not package_path.is_absolute():
        package_path = ROOT / package_path
    package = json.loads(package_path.read_text(encoding="utf-8"))
    errors, warnings = validate(package, package_path)

    for warning in warnings:
        print(f"[warn] {warning}")
    for error in errors:
        print(f"[error] {error}")
    if errors:
        print(f"作业包校验失败：{len(errors)} 错误")
        return 1
    print(
        f"作业包校验通过：{len(package['items'])} 题 / 必做 {package.get('__required_time')} 分钟 / "
        f"全部 {package.get('__total_time')} 分钟（上限 {package['max_total_time_minutes']}）"
    )
    if args.report:
        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"errors": errors, "warnings": warnings}, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
