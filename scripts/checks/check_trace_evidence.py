#!/usr/bin/env python3
"""反样板自证检查（机制节点 U2/U4/U7；原则 P-17/P-19/P-28）。

设计字段被填了默认模板串 = 未落实。本检查识别课程数据中来自
scripts/meng_v66/lesson.js `contract()` 的已知默认样板：页面作者若没有为
该页覆写，字段值仍是与 literary_object 无关或仅做名词替换的通用句——
这类"自我陈述"不能作为原则已落实的证据。

样板模式与 lesson.js 的同步由 tests/test_check_trace_evidence.py 保证：
lesson.js 默认串若变更，测试失败并提醒更新本文件模式。

用法：
  python3 scripts/checks/check_trace_evidence.py --lesson-js scripts/meng_v66/lesson.js
  python3 scripts/checks/check_trace_evidence.py --lesson-json snapshot.json
退出码：0（发现只报告）；--strict 时发现即 1。
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# 与 scripts/meng_v66/lesson.js contract() 默认值一一对应；
# 带 literary_object/artifact 插值的用正则，固定句用全等。
BOILERPLATE_PATTERNS: dict[str, re.Pattern | tuple] = {
    "unique_difficulty": re.compile(r"^学生容易看见“.+”，却不能把它准确接回人物和前后故事。$"),
    "prior_input": re.compile(r"^学生已经完成前页任务，手中保留与“.+”有关的原词或初稿。$"),
    "previous_page_input": re.compile(r"^学生已经完成前页任务，手中保留与“.+”有关的原词或初稿。$"),
    "first_person_reception": re.compile(r"^我刚才面对“.+”，留下了.+；我能用原词说清自己新增或修正的理解。$"),
    "adjacent_counterproof": re.compile(r"^相邻页不同时处理“.+”；合并会挤掉必要首答、校准或故事回接。$"),
}
BOILERPLATE_EXACT: dict[str, str] = {
    "info_state": "首答前只给原诗、必要字面和一个自然问题；解释、分类、关系与代表答案在学生首稿后出现。",
    "participation_path": "个人先形成；需要交流时并行同桌或四人轮说；全班只公开少量有差异材料。",
    "teacher_role": "准确释词、引用真实回答、追问原词、后置归纳并守住解释边界。",
    "wait_contract": "逐字稿内有首答等待、限定反馈和本人修订的明确时间。",
    "feedback_revision": "学生依据原词、同伴追问或教师校准，亲自保留、补充、改写或撤回初稿。",
    "normal_counterexample": "想不起、无新增、已经准确、不同意或暂时沉默均有诚实完成路径，不要求伪造改变。",
    "story_return": "页面结束前由一句自然复述回到谁做了什么、人物处境怎样变化以及故事推进到哪里。",
}
BOILERPLATE_FAILURE_SIGNALS = [
    "学生只能复述活动手续，不能复述诗意",
    "首答前已经看见完成关系或答案",
    "产物在后页没有真实消费者",
]
PLACEHOLDER_RE = re.compile(
    r"(?:TODO|TBD|FIXME|待填写|待补充|此处填写|根据实际情况|具体内容)",
    re.IGNORECASE,
)
ELLIPSIS_ONLY_RE = re.compile(r"^[\s….]+$")


def _placeholder_values(value, path: str):
    if isinstance(value, str):
        if PLACEHOLDER_RE.search(value) or ELLIPSIS_ONLY_RE.fullmatch(value):
            yield path, value
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from _placeholder_values(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _placeholder_values(item, f"{path}.{key}" if path else str(key))


def load_lesson(lesson_js: str | None, lesson_json: str | None) -> dict:
    if bool(lesson_js) == bool(lesson_json):
        raise SystemExit("必须且只能提供 --lesson-js 或 --lesson-json 之一")
    if lesson_json:
        return json.loads(Path(lesson_json).read_text(encoding="utf-8"))
    result = subprocess.run(
        ["node", "-e", "console.log(JSON.stringify(require(process.argv[1])))", str(Path(lesson_js).resolve())],
        capture_output=True,
        text=True,
        check=True,
        cwd=ROOT,
    )
    return json.loads(result.stdout)


def scan_lesson(lesson: dict) -> list[dict]:
    findings: list[dict] = []
    is_v2 = str(lesson.get("schema_version") or "").startswith("2.")
    for page in lesson.get("pages") or []:
        pid = page.get("page_id", "?")
        for field, pattern in BOILERPLATE_PATTERNS.items():
            value = page.get(field)
            if isinstance(value, str) and pattern.match(value):
                findings.append({"page_id": pid, "field": field, "kind": "pattern", "value": value})
        for field, exact in BOILERPLATE_EXACT.items():
            value = page.get(field)
            if isinstance(value, str) and value == exact:
                findings.append({"page_id": pid, "field": field, "kind": "exact", "value": value})
        signals = page.get("failure_signals")
        if isinstance(signals, list) and [s for s in signals if isinstance(s, str)] == BOILERPLATE_FAILURE_SIGNALS:
            findings.append({"page_id": pid, "field": "failure_signals", "kind": "exact_list", "value": signals})
        if is_v2:
            for field, value in _placeholder_values(page, ""):
                findings.append({"page_id": pid, "field": field, "kind": "placeholder", "value": value})
    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lesson-js", help="课程数据 Node 模块路径（如 scripts/meng_v66/lesson.js）")
    parser.add_argument("--lesson-json", help="课程数据 JSON 快照路径")
    parser.add_argument("--strict", action="store_true", help="发现样板即返回非零")
    parser.add_argument("--json-out", help="发现清单 JSON 输出路径")
    args = parser.parse_args()

    lesson = load_lesson(args.lesson_js, args.lesson_json)
    findings = scan_lesson(lesson)
    pages = lesson.get("pages") or []
    flagged_pages = {f["page_id"] for f in findings}

    print(f"扫描 {len(pages)} 页，样板自证发现 {len(findings)} 处，涉及 {len(flagged_pages)} 页")
    for finding in findings:
        print(f"  [boilerplate] {finding['page_id']}.{finding['field']}: {finding['value'][:60]}")
    if findings:
        print("说明：这些字段仍为 contract() 默认模板串，不能作为原则已落实的证据（见 P-28/A-01）；")
        print("应逐页改写为针对本页困难与文本的具体陈述，或在该页省略默认填充。")
    if args.json_out:
        path = Path(args.json_out)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(findings, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if (findings and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
