#!/usr/bin/env python3
"""原则修订提案准入器（回流边 ②：PR → 注册库，设计方案 §7 中环）。

按收敛规则§四检查一份 PR-*.json 提案：
1. trigger_evidence 非空且引用的 REF/OBS/GRD 记录存在（同一目录或指定 --evidence-dir）；
2. node ∈ 20 机制节点；
3. change_type 合法；new/modify 必须有 draft.title/statement + enforcement（每项 type ∈
   machine_check/design_trace/review_gate/meta，machine_check 须给 rule）；
4. target_standard 必须为"下一版本"（不允许就地改当前 STANDARD——不追溯否决）。

通过后可用 --emit 在提案旁生成注册库条目草稿（yaml 片段，人工审阅后并入
work/principles/registry.yaml；本工具不直接改注册库——注册库变更走人工+校验器）。

用法：
  python3 scripts/admit_pr.py <PR-xxx.json> [--evidence-dir DIR] [--emit]
退出码：0 准入通过；1 拒收（原因列出）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NODES = {f"K{i}" for i in range(1, 6)} | {f"U{i}" for i in range(1, 9)} | {f"J{i}" for i in range(1, 8)}
ENFORCED_TYPES = {"machine_check", "design_trace", "review_gate", "meta"}


def load_evidence_ids(evidence_dir: Path) -> set[str]:
    ids: set[str] = set()
    for f in evidence_dir.rglob("*.jsonl"):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(row.get("id"), str):
                ids.add(row["id"])
    return ids


def admit(pr: dict, evidence_ids: set[str]) -> tuple[list[str], list[str]]:
    errors, notes = [], []
    where = pr.get("id", "?")

    triggers = pr.get("trigger_evidence") or []
    if not triggers:
        errors.append(f"{where}: trigger_evidence 为空——收敛准入：无触发证据不收")
    missing = [t for t in triggers if t not in evidence_ids]
    if missing:
        errors.append(f"{where}: 触发证据不存在: {missing}（证据须先落 L4）")

    if pr.get("node") not in NODES:
        errors.append(f"{where}: node 非法: {pr.get('node')!r}")

    if pr.get("change_type") not in {"new", "modify", "retire"}:
        errors.append(f"{where}: change_type 非法")

    if pr.get("change_type") in {"new", "modify"}:
        draft = pr.get("draft") or {}
        for field in ("title", "statement"):
            if not str(draft.get(field) or "").strip():
                errors.append(f"{where}: draft.{field} 为空")
        enforcement = draft.get("enforcement") or []
        if not enforcement:
            errors.append(f"{where}: draft.enforcement 为空——理念必须落强制方式（准入法庭）")
        for i, en in enumerate(enforcement):
            if en.get("type") not in ENFORCED_TYPES:
                errors.append(f"{where}: enforcement[{i}].type 非法: {en.get('type')!r}")
            if en.get("type") == "machine_check" and not (en.get("rule") or "").strip():
                errors.append(f"{where}: enforcement[{i}] machine_check 缺 rule")

    std = str(pr.get("target_standard") or "")
    if "next" not in std.lower() and "下一" not in std:
        errors.append(f"{where}: target_standard 必须是下一版本（不追溯否决当前 STANDARD）")

    if pr.get("status") not in {"proposed", "admitted", "rejected"}:
        notes.append(f"{where}: status 置为 proposed")

    return errors, notes


def emit_yaml(pr: dict) -> str:
    draft = pr.get("draft", {})
    enforcement = "\n".join(
        f"      - {{type: {en['type']}"
        + (f", rule: {en['rule']}" if en.get("rule") else "")
        + (f", gate: {en['gate']}" if en.get("gate") else "")
        + (f", fields: [{', '.join(en['fields'])}]}" if en.get("fields") else "")
        + "}"
        for en in draft.get("enforcement", [])
    )
    return f"""# 注册库条目草稿（由 {pr['id']} 生成，人工审阅后并入 registry.yaml）
  - id: <分配ID>
    title: {draft.get('title', '')}
    statement: "{draft.get('statement', '')}"
    domain: 通用
    stages: [待定]
    nodes: [{pr.get('node', '')}]
    anchor: {{doc: <触发反思文件>, heading: <待补>}}
    enforcement:
{enforcement}
    status: proposed
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("proposal")
    parser.add_argument("--evidence-dir", default=str(ROOT / "work/teaching/_classes"))
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()

    pr_path = Path(args.proposal)
    if not pr_path.is_absolute():
        pr_path = ROOT / pr_path
    pr = json.loads(pr_path.read_text(encoding="utf-8"))

    evidence_ids = load_evidence_ids(Path(args.evidence_dir))
    if not evidence_ids:
        print(f"[warn] 证据目录无任何记录（{args.evidence_dir}）——触发证据将全部判不存在")

    errors, notes = admit(pr, evidence_ids)
    for n in notes:
        print(f"[note] {n}")
    for e in errors:
        print(f"[error] {e}")

    if errors:
        print(f"提案拒收：{len(errors)} 项不符合收敛准入")
        return 1

    if args.emit:
        out = pr_path.with_suffix(".registry.yaml")
        out.write_text(emit_yaml(pr), encoding="utf-8")
        print(f"准入通过；注册库条目草稿 → {out}")
    else:
        print("提案准入通过（可 --emit 生成注册库条目草稿；并入注册库须人工+校验器）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
