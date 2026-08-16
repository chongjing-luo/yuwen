#!/usr/bin/env python3
"""通用课程数据校验器（lesson_schema v1.0；机制节点 K1/K2/K4 + 页面合同底线）。

课文无关：任何 lesson.js（Node 模块）或 lesson JSON 都可校验。这是
N-01（教级知识清单以知识卡为准）的机器强制——课程数据不再允许脱离
知识库自说自话。

检查：
1. 顶层：schema_version / lesson_id / book_unit.card_refs / text_contract(源路径+sha) /
   three_questions≥1 / kp_scope / pages≥1 / claim_boundary（两本账）；
2. K1：card_refs 与 kp_scope.kp_ids 解析到真实知识卡；deferred 有理由；
3. K4：relations（若存在）的 card_id 解析；
4. 页面：18 项合同字段非空；unique_difficulty 等追溯字段非样板（复用
   check_trace_evidence）；script.timeboxes 秒和 == minutes*60；branches ≥ 2；
   next_use 非空；literary_object 三形态锚定 canonical_lines（K2：行串/行数组/
   非行对象 kind 声明）；
5. U1/P-07：frontstage 与 title 过前台禁词；
6. 汇总样板发现数（默认不判失败——收敛规则：样板清零是 STANDARD-1.0 对
   新候选的要求，对存量数据作为缺口报告）。

用法：python3 scripts/validate_lesson_schema.py (--lesson-js PATH | --lesson-json PATH) [--strict]
退出码：0 通过；1 失败（--strict 时样板也判失败）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KP_ID_PATTERN = re.compile(r"KP-CARD-[A-Z0-9-]+-\d{3}")

PAGE_REQUIRED_FIELDS = [
    "page_id", "title", "minutes", "literary_object", "unique_difficulty",
    "unique_function", "information_state", "student_action", "artifact",
    "next_use", "normal_counterexample", "first_person_reception",
    "deletion_loss", "story_return",
]

# 机制节点全集（work/evaluation/三目标实现机制.md 的 20 节点）
NODE_IDS = {f"K{i}" for i in range(1, 6)} | {f"U{i}" for i in range(1, 9)} | {f"J{i}" for i in range(1, 8)}

# literary_object 非行对象的合法类别（K2）：行锚定之外，页面确以非诗对象为主时
# 必须显式声明类别，不许自由散文冒充行锚定。
NON_POEM_KINDS = {"student_products", "full_poem_voice", "cultural_knowledge", "question_set", "mixed"}


def _line_anchored(obj: str, canonical: list[str]) -> bool:
    return any(obj in line or line in obj for line in canonical)


def literary_object_error(pid: str, obj, canonical: list[str]) -> str | None:
    """K2 情境锚定三形态：行串（含多行拼接串）/ 行数组 / 非行对象声明。"""
    if obj is None or obj == "" or obj == []:
        return None  # 缺字段由 PAGE_REQUIRED_FIELDS 检查报告
    if isinstance(obj, str):
        if not _line_anchored(obj, canonical):
            return f"{pid}: literary_object「{obj}」不在 canonical_lines 内（K2 情境锚定）"
        return None
    if isinstance(obj, list):
        bad = [x for x in obj if not (isinstance(x, str) and _line_anchored(x, canonical))]
        if bad:
            return f"{pid}: literary_object 数组含未锚定项（K2）: {bad[:2]}"
        return None
    if isinstance(obj, dict):
        if obj.get("kind") not in NON_POEM_KINDS:
            return f"{pid}: literary_object.kind 非法（K2）: {obj.get('kind')!r}，合法类别: {sorted(NON_POEM_KINDS)}"
        scope = obj.get("scope")
        if scope is not None and scope != "full_poem":
            return f"{pid}: literary_object.scope 仅支持 full_poem（K2）: {scope!r}"
        lines = obj.get("lines")
        if lines is not None and not (
            isinstance(lines, list) and bool(lines)
            and all(isinstance(x, str) and _line_anchored(x, canonical) for x in lines)
        ):
            return f"{pid}: literary_object.lines 须为非空且逐项锚定 canonical_lines（K2）"
        return None
    return f"{pid}: literary_object 类型非法（K2）: {type(obj).__name__}"


def load_lesson(lesson_js: str | None, lesson_json: str | None) -> dict:
    if bool(lesson_js) == bool(lesson_json):
        raise SystemExit("必须且只能提供 --lesson-js 或 --lesson-json 之一")
    if lesson_json:
        return json.loads((ROOT / lesson_json if not Path(lesson_json).is_absolute() else Path(lesson_json)).read_text(encoding="utf-8"))
    result = subprocess.run(
        ["node", "-e", "console.log(JSON.stringify(require(process.argv[1])))", str((ROOT / lesson_js).resolve())],
        capture_output=True, text=True, check=True, cwd=ROOT,
    )
    return json.loads(result.stdout)


def resolve_card(card_id: str) -> Path | None:
    matches = list((ROOT / "work/knowledge").glob(f"*/cards/{card_id}*.md"))
    return matches[0] if matches else None


def card_kp_ids(card_path: Path) -> set[str]:
    return set(KP_ID_PATTERN.findall(card_path.read_text(encoding="utf-8")))


def validate(lesson: dict, strict: bool) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict = {"pages": 0, "boilerplate": 0, "kp_scope": 0, "deferred": 0}

    for field in ("schema_version", "lesson_id", "book_unit", "text_contract", "three_questions", "kp_scope", "pages", "claim_boundary"):
        if field not in lesson:
            errors.append(f"缺少顶层字段: {field}")
    if errors:
        return errors, warnings, stats

    if len(lesson["three_questions"]) < 1:
        errors.append("three_questions 为空（J4：三问是全课叙事悬念）")

    # 1b. 教学目标（全课指导：先于 pages 存在，每条可归因、可取证）
    objectives = lesson.get("objectives") or []
    if not objectives:
        errors.append("objectives 为空（教学目标是全课指导，必须显式声明——目标先行）")
    seen_obj_ids = set()
    for i, obj in enumerate(objectives):
        oid = obj.get("id", f"#{i}")
        if oid in seen_obj_ids:
            errors.append(f"objective {oid}: id 重复")
        seen_obj_ids.add(oid)
        if not (obj.get("dimension") or "").strip():
            errors.append(f"objective {oid}: 缺 dimension（素养维度）")
        if len((obj.get("statement") or "").strip()) < 20:
            errors.append(f"objective {oid}: statement 过短或为空（不得以抽象套话充当目标）")
        for node in obj.get("nodes") or []:
            if node not in NODE_IDS:
                errors.append(f"objective {oid}: 机制节点非法: {node}")
        if not (obj.get("nodes") or []):
            errors.append(f"objective {oid}: 未绑定机制节点（准入法庭）")
        if not (obj.get("evidence_pages") or []):
            errors.append(f"objective {oid}: 未声明证据页（目标必须可取证）")

    # 1. 文本契约
    contract = lesson["text_contract"]
    for field in ("source_path", "source_sha256", "canonical_lines"):
        if not contract.get(field):
            errors.append(f"text_contract.{field} 为空（P-02/P-11：原文必须有唯一可信源绑定）")
    if contract.get("source_path"):
        source = ROOT / contract["source_path"]
        if not source.exists():
            errors.append(f"text_contract.source_path 不存在: {contract['source_path']}")
        elif contract.get("source_sha256"):
            actual = hashlib.sha256(source.read_bytes()).hexdigest()
            if actual != contract["source_sha256"]:
                errors.append("text_contract.source_sha256 与实际文件不匹配（原文漂移）")

    # 1c. 过程品质（享受不单列目标，作为全课过程品质显式声明——三目标之 J 的安放处）
    pq = lesson.get("process_quality") or {}
    if not (pq.get("statement") or "").strip() or len(pq.get("statement", "").strip()) < 20:
        errors.append("process_quality 缺失或过短（享受是过程品质不是单独目标，必须显式声明由什么承载）")
    pq_nodes = pq.get("nodes") or []
    if not pq_nodes:
        errors.append("process_quality 未绑定 J 类机制节点")
    for node in pq_nodes:
        if node not in {f"J{i}" for i in range(1, 8)}:
            errors.append(f"process_quality 节点须为 J 族（过程品质）: {node}")

    # 2. K1 知识绑定
    card_kps: set[str] = set()
    for card_id in lesson["book_unit"].get("card_refs", []):
        card = resolve_card(card_id)
        if card is None:
            errors.append(f"card_ref 无法解析: {card_id}")
        else:
            card_kps |= card_kp_ids(card)
    unit_ref = lesson["book_unit"].get("unit_ref")
    if unit_ref and not list((ROOT / "work/knowledge").glob(f"*/units/{unit_ref}*.md")):
        errors.append(f"unit_ref 无法解析: {unit_ref}")
    scope = lesson["kp_scope"]
    for kp in scope.get("kp_ids", []):
        if kp not in card_kps:
            errors.append(f"kp_scope 的 {kp} 未解析到引用卡片")
    stats["kp_scope"] = len(scope.get("kp_ids", []))
    for deferred in scope.get("deferred", []):
        if not str(deferred.get("reason") or "").strip():
            errors.append(f"deferred 项 {deferred.get('kp_id')} 缺理由")
    stats["deferred"] = len(scope.get("deferred", []))
    if not scope.get("kp_ids"):
        errors.append("kp_scope.kp_ids 为空（K1/N-01：教什么必须以知识卡界定）")

    # 3. K4 关系边
    for relation in lesson.get("relations") or []:
        if not resolve_card(relation.get("card_id", "")):
            errors.append(f"relations 的 card_id 无法解析: {relation.get('card_id')}")
        if not str(relation.get("relation") or "").strip():
            errors.append("relations 项缺 relation 说明")

    # 4. 页面合同
    sys.path.insert(0, str(ROOT / "scripts/checks"))
    from check_trace_evidence import scan_lesson  # noqa: E402

    pages = lesson["pages"]
    stats["pages"] = len(pages)
    page_ids = {p.get("page_id") for p in pages}

    # 教学目标的交叉校验（需 card_kps 与 page_ids）
    for obj in lesson.get("objectives") or []:
        oid = obj.get("id", "?")
        for kp in obj.get("kp_refs") or []:
            if kp not in card_kps:
                errors.append(f"objective {oid}: kp_ref 未解析到引用卡片: {kp}")
        for pid in obj.get("evidence_pages") or []:
            if pid not in page_ids:
                errors.append(f"objective {oid}: 证据页不存在: {pid}")
    findings = scan_lesson(lesson)
    stats["boilerplate"] = len(findings)
    canonical = contract.get("canonical_lines") or []
    config_path = ROOT / "work/principles/enforcement_config.json"
    banned: list[str] = []
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        banned = config.get("frontstage_banned_v6", []) + config.get("frontstage_banned_v5", [])

    for page in pages:
        pid = page.get("page_id", "?")
        for field in PAGE_REQUIRED_FIELDS:
            value = page.get(field)
            if isinstance(value, str) and not value.strip() or value is None or value == []:
                errors.append(f"{pid}: 缺页面合同字段 {field}")
        script = page.get("script") or {}
        boxes = script.get("timeboxes") or []
        if boxes:
            total = sum(b.get("seconds", 0) for b in boxes)
            expected = (page.get("minutes") or 0) * 60
            if total != expected:
                errors.append(f"{pid}: 时间盒 {total}s ≠ {expected}s")
        if len(script.get("branches") or []) < 2:
            errors.append(f"{pid}: script.branches < 2（P-08：必须有回应分支）")
        if canonical:
            err = literary_object_error(pid, page.get("literary_object"), canonical)
            if err:
                errors.append(err)
        for text in [page.get("title", "")] + [t for t in (page.get("frontstage") or []) if isinstance(t, str)]:
            for word in banned:
                if word in text:
                    errors.append(f"{pid}: 前台含后台词「{word}」")

    if findings and strict:
        errors.append(f"样板自证 {len(findings)} 处（--strict 判失败；见 check_trace_evidence 报告）")
    elif findings:
        warnings.append(f"样板自证 {len(findings)} 处：STANDARD-1.0 要求新候选清零（存量数据作为缺口报告）")

    boundary = lesson.get("claim_boundary", "")
    if "课堂" not in boundary and "试教" not in boundary:
        errors.append("claim_boundary 未声明课堂边界（P-12）")
    return errors, warnings, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--lesson-js")
    group.add_argument("--lesson-json")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    lesson = load_lesson(args.lesson_js, args.lesson_json)
    errors, warnings, stats = validate(lesson, args.strict)

    for warning in warnings:
        print(f"[warn] {warning}")
    for error in errors:
        print(f"[error] {error}")
    if errors:
        print(f"课程数据校验失败：{len(errors)} 错误")
        return 1
    print(f"课程数据校验通过：{stats['pages']} 页 / KP {stats['kp_scope']} 条（defer {stats['deferred']}）/ 样板 {stats['boilerplate']} 处")
    return 0


if __name__ == "__main__":
    sys.exit(main())
