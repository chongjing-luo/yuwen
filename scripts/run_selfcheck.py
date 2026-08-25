#!/usr/bin/env python3
"""全局自检统一入口（yuwen-selfcheck 机制的执行体）。

依次执行：注册库自检 → 存放契约 → 原则体系映射 → 全部课程链与课程数据底线检查 → 全量 pytest →
备课方法节点覆盖汇总，并按系统对象与两本账写入 work/evaluation/reports/selfcheck_<日期>.md。

用法：python3 scripts/run_selfcheck.py [--skip-tests] [--lesson-js PATH --name ID]
退出码：0 全部通过；1 存在失败。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts/checks"))

from validate_principle_registry import build_report, load_registry, validate  # noqa: E402

REPORT_DIR = ROOT / "work/evaluation/reports"
L4_RECORD_TYPES = {
    "observations.jsonl": "OBS",
    "grading.jsonl": "GRD",
    "mastery_ledger.jsonl": "MR",
    "reflections.jsonl": "REF",
}


def run(cmd: list[str], cwd: Path = ROOT) -> tuple[int, str]:
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    output = "\n".join(line for line in (result.stdout + result.stderr).splitlines() if "Warning" not in line)
    return result.returncode, output.strip()


def summarize_classroom_evidence(root: Path = ROOT) -> dict:
    """Count current L4 records without creating or editing classroom evidence."""
    classes = root / "work/teaching/_classes"
    counts: dict[str, int] = {}
    files: list[str] = []
    if not classes.is_dir():
        return {"total_records": 0, "by_type": {}, "files": []}
    for path in sorted(classes.rglob("*")):
        if not path.is_file():
            continue
        record_type = L4_RECORD_TYPES.get(path.name)
        if record_type:
            count = sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
        elif path.parent.name == "proposals" and path.name.startswith("PR-") and path.suffix == ".json":
            record_type, count = "PR", 1
        elif path.parent.name == "reflections" and path.name.startswith("REF-") and path.suffix == ".json":
            record_type, count = "REF", 1
        else:
            continue
        if count:
            counts[record_type] = counts.get(record_type, 0) + count
            files.append(path.relative_to(classes).as_posix())
    return {
        "total_records": sum(counts.values()),
        "by_type": dict(sorted(counts.items())),
        "files": files,
    }


def discover_lesson_dirs(root: Path = ROOT) -> list[Path]:
    """Find every lesson directory that has any G0-G4 chain artifact."""
    teaching = root / "work/teaching"
    if not teaching.is_dir():
        return []
    lesson_dirs: set[Path] = set()
    for name in (
        "evidence_manifest.json",
        "G1_owner_approval.json",
        "lesson_plan_lock.json",
        "design_lock.json",
        "materials_lock.json",
        "audit_lock.json",
    ):
        for path in teaching.rglob(f"_meta/{name}"):
            lesson_dirs.add(path.parent.parent)
    for path in teaching.rglob("_meta/**/host_release*.json"):
        meta_dir = next((parent for parent in path.parents if parent.name == "_meta"), None)
        if meta_dir:
            lesson_dirs.add(meta_dir.parent)
    for path in teaching.rglob("materials/**/*"):
        if path.is_file():
            lesson_dirs.add(path.parent.parent if path.parent.name == "materials" else next(
                ancestor for ancestor in path.parents if ancestor.name == "materials"
            ).parent)
    for suffix in ("*.pptx", "*.docx"):
        for path in teaching.rglob(suffix):
            if not path.is_file():
                continue
            materials_ancestor = next((parent for parent in path.parents if parent.name == "materials"), None)
            lesson_dirs.add(materials_ancestor.parent if materials_ancestor else path.parent)
    for path in teaching.rglob("_meta/reviews/*"):
        if path.is_file():
            lesson_dirs.add(path.parent.parent.parent)
    for name in ("lesson.json", "教学设计.md", "教案.md"):
        for path in teaching.rglob(name):
            lesson_dirs.add(path.parent)
    return sorted(lesson_dirs, key=lambda path: path.as_posix())


def inspect_lesson_chain(lesson_dir: Path, root: Path = ROOT) -> tuple[bool, str]:
    """Inspect the first available G0-G4 object and reject gate skipping (P-11/J7)."""
    import json

    from validate_lesson_evidence import validate as validate_evidence
    from validate_lesson_audit import load_external_review_registry, validate_audit_lock
    from validate_lesson_lineage import validate_design_lock, validate_materials_lock
    from validate_lesson_plan import validate as validate_plan
    from validate_lesson_schema import validate as validate_schema

    meta = lesson_dir / "_meta"
    local_host_release_files = sorted(meta.rglob("host_release*.json")) if meta.is_dir() else []
    if local_host_release_files:
        return False, "项目内禁止宿主放行凭证：" + "、".join(
            path.name for path in local_host_release_files
        )
    evidence_path = meta / "evidence_manifest.json"
    plan_lock_path = meta / "lesson_plan_lock.json"
    design_lock_path = meta / "design_lock.json"
    materials_lock_path = meta / "materials_lock.json"
    audit_lock_path = meta / "audit_lock.json"
    owner_approval_path = meta / "G1_owner_approval.json"
    lesson_plan_path = lesson_dir / "教案.md"
    lesson_json_path = lesson_dir / "lesson.json"
    teaching_design_path = lesson_dir / "教学设计.md"
    material_files = sorted(
        path for path in (lesson_dir / "materials").rglob("*") if path.is_file()
    ) if (lesson_dir / "materials").is_dir() else []
    root_office_files = sorted(
        path for path in lesson_dir.iterdir()
        if path.is_file() and path.suffix.lower() in {".pptx", ".docx"}
    )
    review_files = [path for path in (meta / "reviews").glob("*") if path.is_file()] if (meta / "reviews").is_dir() else []
    downstream = [
        path
        for path in (
            owner_approval_path,
            lesson_json_path,
            teaching_design_path,
            design_lock_path,
            materials_lock_path,
            audit_lock_path,
            *material_files,
            *root_office_files,
            *review_files,
        )
        if path.exists()
    ]

    if not evidence_path.exists():
        other_objects = [path for path in downstream if path != lesson_plan_path]
        if lesson_plan_path.exists() and not other_objects:
            return True, "发现S2人读教案草案但G0未建立；不得进入G1及下游（无下游，诚实停止）"
        if downstream:
            return False, "发现下游产物但G0/G1不存在：绕过G1（" + "、".join(path.name for path in downstream) + "）"
        return True, "未发现新三阶段候选，跳过血缘抽查"

    try:
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return False, f"G0证据清单无法读取: {exc}"
    evidence_errors, _ = validate_evidence(
        evidence,
        root=root,
        manifest_path=evidence_path,
    )
    if evidence_errors:
        return False, "G0失败：" + "；".join(evidence_errors)

    if not plan_lock_path.exists():
        if downstream:
            return False, "G0存在但发现下游产物：绕过G1（" + "、".join(path.name for path in downstream) + "）"
        return True, "G0通过；G1待所有者审核；下游为空（诚实停止）"

    try:
        plan_lock = json.loads(plan_lock_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return False, f"G1教案锁无法读取: {exc}"
    plan_errors, _ = validate_plan(plan_lock, root=root, lock_path=plan_lock_path)
    if plan_errors:
        return False, "G1失败：" + "；".join(plan_errors)

    design_present = teaching_design_path.exists()
    lesson_present = lesson_json_path.exists()
    design_lock_present = design_lock_path.exists()
    if design_present != lesson_present:
        missing = teaching_design_path.name if not design_present else lesson_json_path.name
        return False, "G2候选不完整，缺：" + missing
    if design_lock_present and not (design_present and lesson_present):
        missing = [path.name for path in (teaching_design_path, lesson_json_path) if not path.exists()]
        return False, "G2锁存在但内容产物不完整，缺：" + "、".join(missing)
    if not design_present and not lesson_present and not design_lock_present:
        g3_or_g4 = [path for path in (*material_files, materials_lock_path, audit_lock_path, *review_files) if path.exists()]
        if g3_or_g4:
            return False, "发现G3/G4产物但G2不存在：绕过G2（" + "、".join(path.name for path in g3_or_g4) + "）"
        return True, "G0/G1通过；G2尚未开始"

    if design_present and lesson_present and not design_lock_present:
        g3_or_g4 = [path for path in (*material_files, materials_lock_path, audit_lock_path, *review_files) if path.exists()]
        if g3_or_g4:
            return False, "G2候选未锁定却发现G3/G4产物：绕过G2（" + "、".join(path.name for path in g3_or_g4) + "）"
        try:
            lesson = json.loads(lesson_json_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            return False, f"G2候选无法读取: {exc}"
        schema_errors, _, _ = validate_schema(lesson, strict=True, root=root)
        if schema_errors:
            return False, "G2候选失败：" + "；".join(schema_errors)
        return True, "G0/G1通过；G2候选schema通过，尚待独立审查与design lock（诚实停止）"

    try:
        lesson = json.loads(lesson_json_path.read_text(encoding="utf-8"))
        design_lock = json.loads(design_lock_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return False, f"G2对象无法读取: {exc}"
    schema_errors, _, _ = validate_schema(lesson, strict=True, root=root)
    design_errors = validate_design_lock(design_lock, root=root)
    if schema_errors or design_errors:
        return False, "G2失败：" + "；".join(schema_errors + design_errors)

    if not materials_lock_path.exists():
        orphan_g3_or_g4 = [path for path in (*material_files, audit_lock_path, *review_files) if path.exists()]
        if orphan_g3_or_g4:
            return False, "G3产物不完整或G4绕门（" + "、".join(path.name for path in orphan_g3_or_g4) + "）"
        return True, "G0/G1/G2通过；G3尚未开始"
    try:
        materials_lock = json.loads(materials_lock_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return False, f"G3物料锁无法读取: {exc}"
    materials_errors = validate_materials_lock(materials_lock, root=root)
    if materials_errors:
        return False, "G3失败：" + "；".join(materials_errors)
    if not audit_lock_path.exists():
        if review_files:
            return False, "发现G4审查对象但audit_lock不存在（" + "、".join(path.name for path in review_files) + "）"
        return True, "G0—G3血缘通过；G4尚未开始"
    try:
        audit_lock = json.loads(audit_lock_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return False, f"G4终审锁无法读取: {exc}"
    registry_path = os.environ.get("YUWEN_EXTERNAL_REVIEW_REGISTRY")
    external_registry = None
    if registry_path:
        external_registry, registry_errors = load_external_review_registry(Path(registry_path), root=root)
        if registry_errors:
            return False, "G4外部审查事件注册表失败：" + "；".join(registry_errors)
    audit_errors = validate_audit_lock(
        audit_lock,
        root=root,
        external_review_registry=external_registry,
    )
    if audit_errors:
        return False, "G4失败：" + "；".join(audit_errors)
    return True, "G0—G4血缘与独立双审冻结锁通过；G4本地终审候选结构已验；待宿主放行；真实课堂仍待试教"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-tests", action="store_true")
    parser.add_argument("--lesson-js", help="可选：额外检查一个legacy课程Node模块")
    parser.add_argument("--name", help="与--lesson-js配套的课程标识")
    parser.add_argument("--report-path", type=Path, help="可选报告路径（测试/隔离运行使用）")
    args = parser.parse_args()

    sections: list[tuple[str, bool | None, str]] = []

    # 1. 注册库
    errors, warnings = validate(load_registry())
    ok = not errors
    detail = "\n".join([f"[error] {e}" for e in errors] + [f"[warn] {w}" for w in warnings])
    principle_count = len(load_registry().get("principles", []))
    sections.append(("原则注册库自检", ok, detail or f"{principle_count} 原则 / 20 节点 / 0 错误"))

    # 1a. 规范根、重要路径与当前操作文件不得漂回旧目录。
    storage_code, storage_output = run([
        sys.executable,
        "scripts/checks/validate_storage_layout.py",
    ])
    sections.append(("存放契约与重要路径", storage_code == 0, storage_output))

    # 1b. 教学方法内部：46条法条的设计视图必须恰好分区，并映射当前目标框架。
    map_code, map_output = run([
        sys.executable,
        "scripts/checks/validate_principle_system_map.py",
        "--map", "work/methodology/lesson-preparation/原则体系.md",
        "--canonical", "work/methodology/lesson-preparation/备课基本原则.md",
        "--registry", "work/principles/registry.yaml",
    ])
    sections.append(("原则体系映射", map_code == 0, map_output))

    # 1c. 唯一规程、手册六字段及skill→MM引用图；S0资料规则不强绑K/U/J。
    governance_code, governance_output = run([
        sys.executable,
        "scripts/checks/validate_operational_governance.py",
    ])
    sections.append(("操作治理引用图", governance_code == 0, governance_output))

    # 1d. 遍历全部候选链；允许在真实所有者审核前诚实停止，禁止只抽查固定课例。
    lesson_dirs = discover_lesson_dirs(ROOT)
    for lesson_dir in lesson_dirs:
        chain_ok, chain_detail = inspect_lesson_chain(lesson_dir)
        label = lesson_dir.relative_to(ROOT / "work/teaching").as_posix()
        sections.append((f"课程血缘（{label}）", chain_ok, chain_detail))

    # 2. 对每个现行lesson.json执行通用原则检查；legacy仅在显式传参时附加。
    lesson_jsons = [path / "lesson.json" for path in lesson_dirs if (path / "lesson.json").is_file()]
    if lesson_jsons:
        for lesson_json in lesson_jsons:
            label = lesson_json.parent.relative_to(ROOT / "work/teaching").as_posix().replace("/", "-")
            code, output = run([
                "python3", "scripts/checks/run_principle_checks.py",
                "--lesson-json", str(lesson_json), "--name", label,
            ])
            sections.append((f"课程数据底线检查（{label}）", code == 0, output))
    else:
        sections.append(("课程数据底线检查（跳过）", True, "未发现现行lesson.json；教案候选不得用历史数据替代"))
    if args.lesson_js:
        legacy_name = args.name or Path(args.lesson_js).stem
        code, output = run([
            "python3", "scripts/checks/run_principle_checks.py",
            "--lesson-js", args.lesson_js, "--name", legacy_name,
        ])
        sections.append((f"legacy课程数据底线检查（{legacy_name}）", code == 0, output))

    # 3. 全量测试（pytest + node）
    if args.skip_tests:
        sections.append(("全量测试（pytest）", None, "（--skip-tests 未执行，不计为通过）"))
        sections.append(("node 测试", None, "（--skip-tests 未执行，不计为通过）"))
    else:
        # pytest.ini already contains -q; clear configured addopts so this
        # explicit -q retains the numeric summary instead of becoming -qq.
        code, output = run(["python3", "-m", "pytest", "-o", "addopts=", "-q"])
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

    # 4. 当前备课方法工作框架的节点覆盖
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
    sections.append(("备课方法节点覆盖（candidate框架）", True, "\n".join(coverage_lines)))

    # 汇总报告（两本账）
    has_failures = any(ok is False for _, ok, _ in sections)
    has_skips = any(ok is None for _, ok, _ in sections)
    all_ok = not has_failures and not has_skips
    lines = [f"# 全局自检报告 {date.today()}", "", f"标准版本：{registry['meta']['standard_version']}", ""]
    lines.append("## 桌面账（设计条件）")
    lines.append("")
    for name, ok, detail in sections:
        icon = "✅" if ok is True else "❌" if ok is False else "⏭️"
        lines.append(f"### {icon} {name}")
        lines.append("")
        for line in detail.splitlines():
            lines.append(f"    {line}")
        lines.append("")
    lines.append("## 课堂账（效果证据）")
    lines.append("")
    classroom = summarize_classroom_evidence(ROOT)
    if classroom["total_records"] == 0:
        classroom_status = "课堂账为空，待真实试教"
        lines.append("- 状态：**空——当前L4无记录**（两本账纪律，P-12）。全部桌面通过仅证明设计条件具备。")
        lines.append("- 待采集信号见 `scripts/checks/run_principle_checks.py` 报告的 classroom_account。")
    else:
        classroom_status = f"课堂账已有{classroom['total_records']}条L4记录，效果结论须逐条引用"
        type_counts = "、".join(f"{kind} {count}" for kind, count in classroom["by_type"].items())
        lines.append(f"- 状态：**已有真实记录待逐条解释**；共{classroom['total_records']}条（{type_counts}）。")
        lines.append("- 本自检只读计数，不修改、不汇总替代原始L4，也不据数量宣称学生已学会或享受。")
        lines.append("- 涉及文件：" + "、".join(f"`{path}`" for path in classroom["files"]))
    lines.append("")
    report_path = args.report_path or (REPORT_DIR / f"selfcheck_{date.today()}.md")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")

    for name, ok, detail in sections:
        status = "PASS" if ok is True else "FAIL" if ok is False else "SKIP"
        print(f"[{status}] {name}")
    print(f"\n报告 → {report_path}")
    if all_ok:
        conclusion = "全部通过（桌面账）"
    elif has_failures and any(ok is None for _, ok, _ in sections):
        conclusion = "存在失败项且部分检查未执行，不构成全量通过"
    elif has_failures:
        conclusion = "存在失败项"
    else:
        conclusion = "部分检查未执行，不构成全量通过"
    print(f"结论：{conclusion}；{classroom_status}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
