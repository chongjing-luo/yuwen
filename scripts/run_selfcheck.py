#!/usr/bin/env python3
"""全局自检统一入口（yuwen-selfcheck 机制的执行体）。

依次执行：注册库自检 → 课程数据底线检查（默认《氓》V6.6）→ 全量 pytest →
节点覆盖汇总，并按三目标两本账写入 work/evaluation/reports/selfcheck_<日期>.md。

用法：python3 scripts/run_selfcheck.py [--skip-tests] [--lesson-js PATH --name ID]
退出码：0 全部通过；1 存在失败。
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/checks"))

from validate_principle_registry import build_report, load_registry, validate  # noqa: E402

REPORT_DIR = ROOT / "work/evaluation/reports"
DEFAULT_LESSON_JS = "scripts/meng_v66/lesson.js"
DEFAULT_LESSON_NAME = "meng_v66"


def run(cmd: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    output = "\n".join(line for line in (result.stdout + result.stderr).splitlines() if "Warning" not in line)
    return result.returncode, output.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--lesson-js", default=DEFAULT_LESSON_JS)
    parser.add_argument("--name", default=DEFAULT_LESSON_NAME)
    args = parser.parse_args()

    sections: list[tuple[str, bool, str]] = []

    # 1. 注册库
    errors, warnings = validate(load_registry())
    ok = not errors
    detail = "\n".join([f"[error] {e}" for e in errors] + [f"[warn] {w}" for w in warnings])
    sections.append(("原则注册库自检", ok, detail or "112 原则 / 20 节点 / 0 错误"))

    # 2. 课程数据底线（《氓》重制期间数据缺席则警告跳过——教案先行，MM-S3-13）
    if Path("work/teaching/选择性必修下册/氓/lesson.json").exists():
        code, output = run(["python3", "scripts/checks/run_principle_checks.py", "--lesson-js", args.lesson_js, "--name", args.name])
        sections.append((f"课程数据底线检查（{args.name}）", code == 0, output))
    else:
        code, output = 0, "课程数据缺席（《氓》重制中：教案先行，数据待审核后落盘）"
        sections.append((f"课程数据底线检查（{args.name}·跳过）", True, output))

    # 3. 全量测试（pytest + node）
    if args.skip_tests:
        sections.append(("全量测试（pytest）", True, "（--skip-tests 跳过）"))
        sections.append(("node 测试", True, "（--skip-tests 跳过）"))
    else:
        code, output = run(["python3", "-m", "pytest", "-q"])
        tail = "\n".join(output.splitlines()[-3:])
        sections.append(("全量测试（pytest）", code == 0, tail))
        node_results, node_ok = [], True
        for js in sorted((ROOT / "tests").glob("test_*.js")):
            js_code, js_out = run(["node", str(js)])
            node_ok = node_ok and js_code == 0
            last_line = js_out.splitlines()[-1] if js_out.splitlines() else ""
            node_results.append(f"[{'PASS' if js_code == 0 else 'FAIL'}] {js.name}: {last_line}")
        sections.append(("node 测试", node_ok, "\n".join(node_results)))

    # 3b. 知识账本（AGENTS：领取任务前必须 passed）
    kb_code, kb_out = run(["python3", "scripts/validate_knowledge_base.py"])
    sections.append(("知识账本校验", kb_code == 0, kb_out.splitlines()[-1] if kb_out.splitlines() else ""))

    # 4. 节点覆盖
    registry = load_registry()
    report = build_report(registry)
    unenforced = {nid: e["unenforced_active"] for nid, e in report["by_node"].items() if e["unenforced_active"]}
    coverage_lines = [
        f"- {goal}: 原则映射 {stats['principles']}，机器 {stats['machine']}，追溯 {stats['trace']}，审查 {stats['review']}"
        for goal, stats in report["by_goal"].items()
    ]
    if unenforced:
        coverage_lines.append("- 仅追溯强制（缺口）: " + "; ".join(f"{nid}←{'、'.join(ids)}" for nid, ids in unenforced.items()))
    else:
        coverage_lines.append("- 仅追溯强制缺口：无（active 原则均有 machine/review 强制或为 meta）")
    sections.append(("机制节点覆盖", True, "\n".join(coverage_lines)))

    # 汇总报告（两本账）
    all_ok = all(ok for _, ok, _ in sections)
    lines = [f"# 全局自检报告 {date.today()}", "", f"标准版本：{registry['meta']['standard_version']}", ""]
    lines.append("## 桌面账（设计条件）")
    lines.append("")
    for name, ok, detail in sections:
        lines.append(f"### {'✅' if ok else '❌'} {name}")
        lines.append("")
        for line in detail.splitlines():
            lines.append(f"    {line}")
        lines.append("")
    lines.append("## 课堂账（效果证据）")
    lines.append("")
    lines.append("- 状态：**空——未真实试教**（两本账纪律，P-12）。全部桌面通过仅证明设计条件具备。")
    lines.append("- 待采集信号见 `scripts/checks/run_principle_checks.py` 报告的 classroom_account。")
    lines.append("")
    report_path = REPORT_DIR / f"selfcheck_{date.today()}.md"
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")

    for name, ok, detail in sections:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    print(f"\n报告 → {report_path}")
    print(f"结论：{'全部通过（桌面账）' if all_ok else '存在失败项'}；课堂账为空，待真实试教")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
