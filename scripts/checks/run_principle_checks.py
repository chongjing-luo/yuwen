#!/usr/bin/env python3
"""注册表驱动的通用原则检查执行器。

从 work/principles/registry.yaml 读取声明，对一份课程数据执行当前可在
数据层完成的 machine_check（前台禁词、时间盒守恒、三问在场、总时长恒等、
反样板），并校验 enforcement_config.json 作为禁词唯一真源的形状完整性
（旧链校验器归档后，词表不再有第二份拷贝可漂移）。

本执行器不替代 validate_meng_v6_page_audit.py 等重型校验器；它提供的是
「任何课程数据都可跑」的通用底线检查 + 两本账报告框架（桌面账/课堂账）。

用法：
  python3 scripts/checks/run_principle_checks.py --lesson-js scripts/meng_v66/lesson.js --name meng_v66
退出码：0 全部通过；1 存在失败（样板发现默认不失败，--strict 时失败——
这符合收敛规则：新检查进入下一标准版本，不追溯否决当前候选）。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "work/principles/registry.yaml"
CONFIG_PATH = ROOT / "work/principles/enforcement_config.json"
DEFAULT_REPORT_DIR = ROOT / "work/evaluation/reports"

# enforcement_config.json 的禁词键。旧链校验器（validate_meng_v5/v6_lesson_package）
# 归档后，本配置是禁词唯一真源，由 validate_lesson_schema.py 与本执行器共同消费；
# 此处只做形状完整性检查，防止键缺失、空词表或词条重复。
CONFIG_TOKEN_KEYS = ("frontstage_banned_v5", "first_view_banned_v5", "note_banned_v5", "frontstage_banned_v6")

# 课堂账信号清单（S6 试教观察表采集；未试教前为空——两本账纪律）
CLASSROOM_SIGNALS = [
    "主动开口率与自愿发言面（J1/J3）",
    "首答阶段非空白抽样率（U1）",
    "个人末答抽样正确率、修订痕迹率（U3/U8）",
    "自发回读与课后仍谈论作品（J4）",
    "沉默/想不起学生真实完成率（U7）",
    "实际完成耗时 vs 预算偏差（U5）",
    "单元测评 KP 掌握率与延迟保持率（K1/K3）",
]


def load_lesson(lesson_js: str) -> dict:
    result = subprocess.run(
        ["node", "-e", "console.log(JSON.stringify(require(process.argv[1])))", str(Path(lesson_js).resolve())],
        capture_output=True,
        text=True,
        check=True,
        cwd=ROOT,
    )
    return json.loads(result.stdout)


def check_config_drift(config: dict) -> list[str]:
    errors: list[str] = []
    for key in CONFIG_TOKEN_KEYS:
        words = config.get(key)
        if not isinstance(words, list) or not words:
            errors.append(f"词表缺失或为空：enforcement_config.json[{key}]")
            continue
        if not all(isinstance(w, str) and w.strip() for w in words):
            errors.append(f"词表含非字符串或空白词条：enforcement_config.json[{key}]")
        duplicates = sorted({w for w in words if words.count(w) > 1})
        if duplicates:
            errors.append(f"词表重复词条 {duplicates}：enforcement_config.json[{key}]")
    return errors


def frontstage_texts(page: dict) -> list[str]:
    texts: list[str] = []
    for key in ("title", "frontstage"):
        value = page.get(key)
        if isinstance(value, str):
            texts.append(value)
        elif isinstance(value, list):
            texts.extend(v for v in value if isinstance(v, str))
    return texts


def run_checks(lesson: dict, config: dict, strict: bool) -> dict:
    results: dict[str, dict] = {}
    pages = lesson.get("pages") or []
    banned = config.get("frontstage_banned_v6", []) + config.get("frontstage_banned_v5", [])

    leaks = [
        {"page_id": p.get("page_id"), "word": word, "context": text[:60]}
        for p in pages
        for text in frontstage_texts(p)
        for word in banned
        if word in text
    ]
    results["frontstage_banned"] = {"ok": not leaks, "findings": leaks[:50], "count": len(leaks)}

    timebox_errors = []
    for p in pages:
        script = p.get("script") or {}
        boxes = script.get("timeboxes") or []
        if not boxes:
            continue
        total = sum(b.get("seconds", 0) for b in boxes)
        expected = (p.get("minutes") or 0) * 60
        if total != expected:
            timebox_errors.append({"page_id": p.get("page_id"), "sum": total, "expected": expected})
    results["timebox_conservation"] = {"ok": not timebox_errors, "findings": timebox_errors}

    questions = lesson.get("three_questions") or []
    results["three_questions_present"] = {"ok": len(questions) >= 1 and all(bool(q) for q in questions), "count": len(questions)}

    total_minutes = sum(p.get("minutes") or 0 for p in pages)
    target = lesson.get("target_natural_minutes")
    results["total_minutes"] = {
        "ok": target is None or total_minutes == target,
        "sum": total_minutes,
        "target": target,
    }

    from check_trace_evidence import scan_lesson  # 同目录模块

    boilerplate = scan_lesson(lesson)
    results["boilerplate_trace"] = {
        "ok": not boilerplate,
        "strict": strict,
        "count": len(boilerplate),
        "pages": sorted({f["page_id"] for f in boilerplate}),
        "note": "样板发现默认不判失败（收敛规则：新检查进入下一标准版本）",
    }
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lesson-js", required=True, help="课程数据 Node 模块路径")
    parser.add_argument("--name", required=True, help="课程标识（用于报告命名）")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    args = parser.parse_args()

    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    lesson = load_lesson(args.lesson_js)

    drift_errors = check_config_drift(config)
    checks = run_checks(lesson, config, args.strict)

    failed = [k for k, v in checks.items() if not v["ok"] and (k != "boilerplate_trace" or args.strict)]
    report = {
        "date": str(date.today()),
        "lesson": args.name,
        "standard_version": registry.get("meta", {}).get("standard_version"),
        "config_drift": drift_errors,
        "checks": checks,
        "failed": failed + drift_errors,
        "classroom_account": {"status": "空——未真实试教（两本账纪律，P-12）", "signals_to_collect": CLASSROOM_SIGNALS},
    }

    report_dir = Path(args.report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    out = report_dir / f"principle_checks_{args.name}.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    for error in drift_errors:
        print(f"[error] {error}")
    for name, result in checks.items():
        status = "PASS" if result["ok"] else ("FINDINGS" if name == "boilerplate_trace" else "FAIL")
        extra = f"（{result.get('count', result.get('sum', ''))}）" if result.get("count") else ""
        print(f"[{status}] {name}{extra}")
    print(f"报告已写入 {out}")
    print(f"课堂账：{report['classroom_account']['status']}")

    return 1 if (failed or drift_errors) else 0


if __name__ == "__main__":
    sys.exit(main())
