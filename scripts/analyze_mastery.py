#!/usr/bin/env python3
"""学情诊断分析器（机制节点 K1/K3/K4 的第四站闭环；S8 环节）。

读取 mastery ledger（JSONL，每行一次 KP 掌握观测）：
  {"date": "2026-09-10", "class_id": "高2026级3班", "student_id": "S01",
   "source": {"type": "homework|quiz|observation", "ref": "HW-MENG-V66-01/HW-02"},
   "kp_id": "KP-CARD-X3-U01-01-004", "score": 2, "max_score": 2,
   "error_type": "现代义干扰"}   // error_type 可选

产出：
- per-KP 掌握率与样本量；低于阈值的 KP 生成回教建议（绑回知识卡与作业/试卷条目）；
- per-学生画像（薄弱 KP 列表）；
- markdown 热图报告。

诚实纪律（P-12）：ledger 只收真实课堂/作业数据；本脚本不生成演示数据，
格式验证用例在 tests 中使用明确标注 synthetic 的数据。

用法：python3 scripts/analyze_mastery.py <ledger.jsonl> [--threshold 0.6] [--out OUT.md]
退出码：0 正常；1 ledger 无有效观测或 kp_id 无法解析。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KP_ID_PATTERN = re.compile(r"^KP-CARD-([A-Z0-9]+)-U(\d+)-(\d+)-(\d{3})$")
CARD_PATH_PATTERN = re.compile(r"^CARD-[A-Z0-9]+-U\d+-\d+$")


def resolve_card(kp_id: str) -> Path | None:
    match = KP_ID_PATTERN.match(kp_id)
    if not match:
        return None
    card_id = f"CARD-{match.group(1)}-U{match.group(2)}-{match.group(3)}"
    matches = list((ROOT / "work/knowledge").glob(f"*/cards/{card_id}*.md"))
    return matches[0] if matches else None


def load_entries(ledger_path: Path) -> list[dict]:
    entries = []
    for line_number, line in enumerate(ledger_path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        entry = json.loads(line)
        problems = []
        for field in ("date", "class_id", "student_id", "kp_id"):
            if not entry.get(field):
                problems.append(field)
        source = entry.get("source") or {}
        if not source.get("type") or not source.get("ref"):
            problems.append("source")
        if not isinstance(entry.get("score"), (int, float)) or not isinstance(entry.get("max_score"), (int, float)) or entry["max_score"] <= 0:
            problems.append("score/max_score")
        if entry["score"] < 0 or entry["score"] > entry["max_score"]:
            problems.append("score 超出 [0, max_score]")
        if problems:
            raise ValueError(f"ledger 第 {line_number} 行缺字段或非法: {problems}: {line[:80]}")
        if resolve_card(entry["kp_id"]) is None:
            raise ValueError(f"ledger 第 {line_number} 行 kp_id 无法解析到知识卡: {entry['kp_id']}")
        entries.append(entry)
    return entries


def analyze(entries: list[dict], threshold: float) -> dict:
    kp_stats: dict[str, dict] = defaultdict(lambda: {"earned": 0.0, "max": 0.0, "n": 0, "students": set(), "error_types": defaultdict(int)})
    student_stats: dict[str, dict] = defaultdict(lambda: {"earned": 0.0, "max": 0.0, "kp_rates": defaultdict(list)})
    for entry in entries:
        kp = kp_stats[entry["kp_id"]]
        kp["earned"] += entry["score"]
        kp["max"] += entry["max_score"]
        kp["n"] += 1
        kp["students"].add(entry["student_id"])
        if entry.get("error_type"):
            kp["error_types"][entry["error_type"]] += 1
        student = student_stats[entry["student_id"]]
        student["earned"] += entry["score"]
        student["max"] += entry["max_score"]
        student["kp_rates"][entry["kp_id"]].append(entry["score"] / entry["max_score"])

    for kp_id, stats in kp_stats.items():
        stats["rate"] = stats["earned"] / stats["max"] if stats["max"] else 0.0
        stats["reteach"] = stats["rate"] < threshold
        stats["card"] = resolve_card(kp_id)
        stats["error_types"] = dict(stats["error_types"])
    for sid, stats in student_stats.items():
        stats["rate"] = stats["earned"] / stats["max"] if stats["max"] else 0.0
        stats["kp_rates"] = {kp: sum(v) / len(v) for kp, v in stats["kp_rates"].items()}
    return {"kp": dict(kp_stats), "students": dict(student_stats), "threshold": threshold, "n": len(entries)}


def render_markdown(analysis: dict, class_id: str | None) -> str:
    lines = ["# KP 掌握热图与回教建议", ""]
    lines.append(f"- 观测数：{analysis['n']}；阈值：掌握率 < {analysis['threshold']:.0%} 触发回教")
    if class_id:
        lines.append(f"- 班级：{class_id}")
    lines.append("")
    lines.append("## 按 KP")
    lines.append("")
    lines.append("| KP | 掌握率 | 观测 | 覆盖学生 | 主要错因 | 建议 |")
    lines.append("|---|---|---|---|---|---|")
    for kp_id, stats in sorted(analysis["kp"].items()):
        errors = "、".join(f"{k}×{v}" for k, v in sorted(stats["error_types"].items(), key=lambda x: -x[1])) or "—"
        advice = "**回教**（绑回知识卡，见下）" if stats["reteach"] else "维持；下轮间隔检索"
        lines.append(f"| {kp_id} | {stats['rate']:.0%} | {stats['n']} | {len(stats['students'])} | {errors} | {advice} |")
    lines.append("")
    reteach = [(kp_id, s) for kp_id, s in analysis["kp"].items() if s["reteach"]]
    if reteach:
        lines.append("## 回教建议")
        lines.append("")
        for kp_id, stats in reteach:
            card = stats["card"]
            lines.append(f"- **{kp_id}**（掌握率 {stats['rate']:.0%}，错因 {stats['error_types'] or '未标注'}）→ 回到 `{card.relative_to(ROOT) if card else '?'}`；重走该 KP 的课堂首答—校准—个人末答循环，并安排下次作业闭卷检索（K3）。")
        lines.append("")
    lines.append("## 按学生（薄弱 KP）")
    lines.append("")
    for sid, stats in sorted(analysis["students"].items()):
        weak = [kp for kp, rate in stats["kp_rates"].items() if rate < analysis["threshold"]]
        lines.append(f"- {sid}：总体 {stats['rate']:.0%}；薄弱 {('、'.join(sorted(weak)) or '无')}")
    lines.append("")
    lines.append("---")
    lines.append("数据来源：真实作业/测验/观察记录（mastery ledger）；未含任何桌面推造数据。")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger")
    parser.add_argument("--threshold", type=float, default=0.6)
    parser.add_argument("--out")
    args = parser.parse_args()

    ledger_path = Path(args.ledger)
    if not ledger_path.is_absolute():
        ledger_path = ROOT / ledger_path
    if not ledger_path.exists():
        print(f"[error] ledger 不存在: {ledger_path}（新建台账请按 docstring 格式逐行追加真实观测）")
        return 1
    try:
        entries = load_entries(ledger_path)
    except ValueError as exc:
        print(f"[error] {exc}")
        return 1
    if not entries:
        print("[error] ledger 无有效观测")
        return 1

    analysis = analyze(entries, args.threshold)
    report = render_markdown(analysis, class_id=entries[0].get("class_id"))
    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"报告 → {out_path}")
    else:
        print(report)
    reteach_count = sum(1 for s in analysis["kp"].values() if s["reteach"])
    print(f"分析完成：{len(analysis['kp'])} 个 KP / {len(analysis['students'])} 名学生 / 回教触发 {reteach_count} 项")
    return 0


if __name__ == "__main__":
    sys.exit(main())
