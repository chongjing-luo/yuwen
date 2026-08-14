#!/usr/bin/env python3
"""原则注册库自检。

校验 work/principles/registry.yaml：
1. ID 唯一且符合命名模式；
2. 每条原则映射至少一个合法机制节点，或声明 role=meta 并给出理由；
3. 每个机制节点被至少一条原则覆盖（planned 单列）；
4. source_anchor 指向的文档存在，且 heading 逐行真实存在（人读权威文本与机器源不漂移）；
5. enforcement 类型合法；machine_check 引用的 checker 文件存在；
6. 机制节点名称与《三目标实现机制》文档标题一致（两文件互为镜像）；
7. 输出理念覆盖报告（按节点 × 强制方式统计——理念贯彻成为可度量指标）。

用法：python3 scripts/checks/validate_principle_registry.py [--report OUT.md]
退出码：0 通过；1 存在错误。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "work/principles/registry.yaml"
MECHANISM_DOC = ROOT / "work/evaluation/三目标实现机制.md"

ID_PATTERN = re.compile(r"^(P|A|M|V|N)-[A-Z0-9]{2,3}$")
VALID_DOMAINS = {"通用", "语文"}
VALID_STAGES = {f"S{i}" for i in range(1, 10)}
VALID_ENFORCEMENT_TYPES = {"machine_check", "design_trace", "review_gate", "meta"}
GOAL_OF_PREFIX = {"K": "知识学习", "U": "能够学懂", "J": "享受学习"}


def load_registry():
    with open(REGISTRY_PATH, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_headings(doc_path: Path) -> set[str]:
    headings = set()
    for raw in doc_path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if line.startswith("#"):
            headings.add(line)
    return headings


def validate(registry: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    principles = registry.get("principles") or []
    nodes = registry.get("nodes") or {}

    if not principles:
        errors.append("principles 为空")
        return errors, warnings
    if not nodes:
        errors.append("nodes 为空")
        return errors, warnings

    # 1. ID 唯一与模式
    ids = [p.get("id") for p in principles]
    duplicates = {i for i in ids if ids.count(i) > 1}
    if duplicates:
        errors.append(f"ID 重复: {sorted(duplicates)}")
    for pid in ids:
        if not pid or not ID_PATTERN.match(pid):
            errors.append(f"ID 命名非法: {pid!r}（应为 P-01 / A-T03 / M-02 / V-05 / N-01 形式）")

    # 2. 机制节点合法 + meta 规则
    node_ids = set(nodes)
    for p in principles:
        pid = p.get("id")
        mapped = p.get("nodes") or []
        unknown = set(mapped) - node_ids
        if unknown:
            errors.append(f"{pid}: 引用未定义机制节点 {sorted(unknown)}")
        is_meta = p.get("role") == "meta"
        if is_meta:
            if mapped:
                errors.append(f"{pid}: role=meta 不应再映射节点")
            if not (p.get("justification") or "").strip():
                errors.append(f"{pid}: role=meta 必须给出 justification")
        elif not mapped:
            errors.append(f"{pid}: 必须映射至少一个机制节点，或声明 role=meta（准入规则）")

        # 域与环节
        if p.get("domain") not in VALID_DOMAINS:
            errors.append(f"{pid}: domain 非法: {p.get('domain')!r}")
        bad_stages = set(p.get("stages") or []) - VALID_STAGES
        if bad_stages:
            errors.append(f"{pid}: stages 非法: {sorted(bad_stages)}")
        if not (p.get("title") or "").strip() or not (p.get("statement") or "").strip():
            errors.append(f"{pid}: title/statement 不能为空")
        if p.get("status", "active") not in {"active", "planned", "retired"}:
            errors.append(f"{pid}: status 非法: {p.get('status')!r}")

        # 5. enforcement
        for idx, en in enumerate(p.get("enforcement") or []):
            etype = en.get("type")
            if etype not in VALID_ENFORCEMENT_TYPES:
                errors.append(f"{pid}.enforcement[{idx}]: type 非法: {etype!r}")
                continue
            if etype == "machine_check":
                checker = en.get("checker")
                if not checker:
                    errors.append(f"{pid}.enforcement[{idx}]: machine_check 必须给 checker")
                elif en.get("status") != "planned" and not (ROOT / checker).exists():
                    errors.append(f"{pid}.enforcement[{idx}]: checker 不存在: {checker}")
                if not (en.get("rule") or "").strip():
                    errors.append(f"{pid}.enforcement[{idx}]: machine_check 必须给 rule")
            elif etype == "design_trace":
                if not en.get("fields"):
                    errors.append(f"{pid}.enforcement[{idx}]: design_trace 必须给 fields")
            elif etype == "review_gate":
                if not (en.get("gate") or "").strip():
                    errors.append(f"{pid}.enforcement[{idx}]: review_gate 必须给 gate")
        if not (p.get("enforcement") or []):
            errors.append(f"{pid}: enforcement 为空（理念必须以 machine/trace/review/meta 之一进入管线）")

    # 3. 节点覆盖
    active_map: dict[str, list[str]] = {nid: [] for nid in node_ids}
    planned_map: dict[str, list[str]] = {nid: [] for nid in node_ids}
    for p in principles:
        if p.get("status") == "retired":
            continue
        target = planned_map if p.get("status") == "planned" else active_map
        for nid in p.get("nodes") or []:
            if nid in target:  # 未知节点已单独报错
                target[nid].append(p["id"])
    for nid in sorted(node_ids):
        if not active_map[nid] and not planned_map[nid]:
            errors.append(f"机制节点 {nid} 无任何原则覆盖")
        elif not active_map[nid]:
            warnings.append(f"机制节点 {nid} 仅有 planned 原则 {planned_map[nid]}，机器/审查强制尚未落地")

    # 4/6. 锚点与机制文档镜像
    anchor_docs: dict[str, set[str]] = {}
    for p in principles:
        pid = p.get("id")
        anchor = p.get("anchor") or {}
        doc = anchor.get("doc")
        heading = anchor.get("heading")
        if not doc or not heading:
            errors.append(f"{pid}: anchor 缺 doc/heading")
            continue
        doc_path = ROOT / doc
        if not doc_path.exists():
            errors.append(f"{pid}: anchor 文档不存在: {doc}")
            continue
        if doc not in anchor_docs:
            anchor_docs[doc] = load_headings(doc_path)
        if heading not in anchor_docs[doc]:
            errors.append(f"{pid}: anchor heading 在 {doc} 中不存在: {heading!r}")

    if MECHANISM_DOC.exists():
        mech_headings = load_headings(MECHANISM_DOC)
        for nid, spec in nodes.items():
            name = spec.get("name")
            goal = spec.get("goal")
            if not any(name in h for h in mech_headings):
                errors.append(f"节点 {nid} 名称「{name}」未出现在《三目标实现机制》标题中（镜像漂移）")
            if goal not in GOAL_OF_PREFIX.values():
                errors.append(f"节点 {nid}: goal 非法: {goal!r}")
            if nid[0] not in GOAL_OF_PREFIX or GOAL_OF_PREFIX[nid[0]] != goal:
                errors.append(f"节点 {nid}: 前缀与 goal 不一致")
    else:
        errors.append(f"机制文档不存在: {MECHANISM_DOC}")

    return errors, warnings


def build_report(registry: dict) -> dict:
    principles = registry["principles"]
    nodes = registry["nodes"]
    by_node: dict[str, dict] = {}
    for nid, spec in nodes.items():
        by_node[nid] = {
            "name": spec["name"],
            "goal": spec["goal"],
            "principles": [],
            "machine": 0,
            "trace": 0,
            "review": 0,
            "meta": 0,
            "unenforced_active": [],
        }
    goal_stats = {g: {"principles": 0, "machine": 0, "trace": 0, "review": 0} for g in GOAL_OF_PREFIX.values()}
    for p in principles:
        if p.get("status") == "retired":
            continue
        kinds = {e["type"] for e in p.get("enforcement") or []}
        for nid in p.get("nodes") or []:
            entry = by_node[nid]
            entry["principles"].append(p["id"])
            entry["machine"] += int("machine_check" in kinds)
            entry["trace"] += int("design_trace" in kinds)
            entry["review"] += int("review_gate" in kinds)
            entry["meta"] += int("meta" in kinds)
            if p.get("status") == "active" and not (kinds & {"machine_check", "review_gate"}):
                entry["unenforced_active"].append(p["id"])
            goal = nodes[nid]["goal"]
            goal_stats[goal]["principles"] += 1
            goal_stats[goal]["machine"] += int("machine_check" in kinds)
            goal_stats[goal]["trace"] += int("design_trace" in kinds)
            goal_stats[goal]["review"] += int("review_gate" in kinds)
    meta_count = sum(1 for p in principles if p.get("role") == "meta")
    return {
        "total_principles": len(principles),
        "meta_principles": meta_count,
        "by_node": by_node,
        "by_goal": goal_stats,
    }


def render_markdown(report: dict) -> str:
    lines = ["# 理念覆盖报告", "", f"原则总数：{report['total_principles']}（其中 meta {report['meta_principles']} 条）", ""]
    lines += ["## 按机制节点", "", "| 节点 | 名称 | 目标 | 原则数 | 机器 | 追溯 | 审查 | 仅追溯强制（缺口） |", "|---|---|---|---|---|---|---|---|"]
    for nid, entry in report["by_node"].items():
        gap = "、".join(entry["unenforced_active"]) or "—"
        lines.append(
            f"| {nid} | {entry['name']} | {entry['goal']} | {len(entry['principles'])} | {entry['machine']} | {entry['trace']} | {entry['review']} | {gap} |"
        )
    lines += ["", "## 按目标", "", "| 目标 | 原则映射数 | 有机器检查 | 有设计追溯 | 有审查门 |", "|---|---|---|---|---|"]
    for goal, stats in report["by_goal"].items():
        lines.append(f"| {goal} | {stats['principles']} | {stats['machine']} | {stats['trace']} | {stats['review']} |")
    lines += [
        "",
        "「仅追溯强制」列为 active 但既无 machine_check 也无 review_gate 的原则——理念贯彻缺口清单，应优先补审查门或机器检查。",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", help="覆盖报告 Markdown 输出路径")
    parser.add_argument("--json", help="覆盖报告 JSON 输出路径")
    args = parser.parse_args()

    registry = load_registry()
    errors, warnings = validate(registry)
    report = build_report(registry)

    for warning in warnings:
        print(f"[warn] {warning}")
    if errors:
        for error in errors:
            print(f"[error] {error}")
        print(f"注册库校验失败：{len(errors)} 错误 / {len(warnings)} 警告")
        return 1

    if args.report:
        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_markdown(report), encoding="utf-8")
        print(f"覆盖报告已写入 {path}")
    if args.json:
        path = Path(args.json)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"覆盖报告(JSON)已写入 {path}")

    print(f"注册库校验通过：{report['total_principles']} 条原则 / 20 机制节点 / {len(warnings)} 警告")
    return 0


if __name__ == "__main__":
    sys.exit(main())
