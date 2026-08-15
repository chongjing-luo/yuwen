#!/usr/bin/env python3
"""catalog 生成器（最小版，设计方案 §3.8 目录层）。

从各真相源生成实体总目录 work/knowledge/_meta/catalog.jsonl，并由目录生成
人读视图（INDEX.md 等）。视图是派生物：永不手工编辑，重建即得。

真相源（扫描顺序）：
  1. _meta/deliverables.jsonl    —— L1 策展物（卡片/图谱/册表/试卷分析…）
  2. assessment/item_bank.jsonl  —— 题库条目 IB-*
  3. assessment/blueprint_*.json —— 蓝图 BP-*
  4. assessment/ 下构建产物      —— 学生卷/教师卷（L3，type=derived）
  5. work/teaching/ 的实体       —— lesson.json(LES)/homework_package(HW)
  6. work/manuals/S*.md          —— 手册（MANUAL-S*）
  7. work/knowledge/materials/   —— 素材 MAT-*（现为空）

用法：
  python3 scripts/build_catalog.py                 # 重建 catalog + 视图
  python3 scripts/build_catalog.py --check         # 校验路径可解析 + 零消费体检
退出码：--check 时路径悬空或扫描失败返回 1。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOW = ROOT / "work/knowledge"
TEACH = ROOT / "work/teaching"
MANUALS = ROOT / "work/manuals"
CATALOG = KNOW / "_meta/catalog.jsonl"
INDEX = KNOW / "INDEX.md"

BOOK_NAME = {"B1": "必修上册", "B2": "必修下册", "X1": "选择性必修上册", "X2": "选择性必修中册", "X3": "选择性必修下册"}


def book_of(entity_id: str) -> str:
    m = re.match(r"^(?:CARD|UNIT|BOOK)-([B X]\d)", entity_id.replace(" ", ""))
    return BOOK_NAME.get(m.group(1), "") if m else ""


def row(entity_id, etype, title, path, *, status="active", authority="", tags=None, summary=""):
    tags = tags or []
    book = book_of(entity_id)
    if book and book not in tags:
        tags = [book] + tags
    return {
        "id": entity_id, "type": etype, "title": title,
        "path": str(Path(path).relative_to(ROOT)) if isinstance(path, Path) else path,
        "status": status, "authority": authority, "tags": tags,
        "updated": str(date.today()), "summary": summary,
        "last_consumed": None,
    }


def scan_deliverables(rows, errors):
    ledger = KNOW / "_meta/deliverables.jsonl"
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        d = json.loads(line)
        out = ROOT / d["output_path"]
        if not out.exists():
            errors.append(f"deliverable 路径悬空: {d['deliverable_id']} -> {d['output_path']}")
            continue
        title = out.stem
        tags = [d.get("deliverable_type", "")]
        rows.append(row(d["deliverable_id"], d.get("deliverable_type", "deliverable"), title, out,
                        status=d.get("status", ""), tags=[t for t in tags if t],
                        summary=f"{d.get('deliverable_type','')}（账本状态 {d.get('status','')}）"))


def scan_assessment(rows, errors):
    bank = KNOW / "assessment/item_bank.jsonl"
    if bank.exists():
        for line in bank.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            it = json.loads(line)
            tags = [it["type"]] + ([f"来源{it['year']}"] if it.get("year") else [])
            if it.get("candidate_status") == "candidate_only_M0":
                tags.append("M0未映射")
            rows.append(row(it["item_id"], "exam_item", it["type"], bank, tags=tags,
                            summary=it.get("stem", "")[:40]))
    for bp in sorted((KNOW / "assessment").glob("blueprint_*.json")):
        data = json.loads(bp.read_text(encoding="utf-8"))
        rows.append(row(data["blueprint_id"], "assessment_blueprint", data["title"], bp,
                        tags=["命题"], summary=data.get("claim_boundary", "")[:40]))
    for derived in sorted((KNOW / "assessment").glob("学生卷_*.md")) + sorted((KNOW / "assessment").glob("教师卷*.md")):
        rows.append(row(f"ART-{derived.stem[:40]}", "derived_document", derived.stem, derived,
                        status="derived", tags=["L3派生"], summary="组卷器产物（可再生）"))


def scan_teaching(rows, errors):
    for lesson in sorted(TEACH.rglob("lesson.json")):
        data = json.loads(lesson.read_text(encoding="utf-8"))
        rows.append(row(data.get("lesson_id", lesson.stem), "lesson", data.get("lesson_title", lesson.stem), lesson,
                        tags=["L2", "课程数据"],
                        summary=f"{len(data.get('pages', []))} 页 / {data.get('target_natural_minutes', '?')} 分钟"))
    for hw in sorted(TEACH.rglob("homework_package.json")):
        data = json.loads(hw.read_text(encoding="utf-8"))
        rows.append(row(data.get("homework_id", hw.stem), "homework_package", data.get("homework_id", hw.stem), hw,
                        tags=["L2", "作业"],
                        summary=f"{len(data.get('items', []))} 题"))
    for shared in sorted(TEACH.rglob("_shared/**/*.md")) + sorted(TEACH.rglob("_shared/**/*.json")):
        rows.append(row(f"SHARED-{shared.stem[:30]}", "shared_contract", shared.stem, shared,
                        tags=["共享规格"], summary=shared.stem))


def scan_manuals(rows):
    for manual in sorted(MANUALS.glob("S*.md")):
        m = re.match(r"^(S\d)", manual.stem)
        if not m:
            continue
        rows.append(row(f"MANUAL-{m.group(1)}", "manual", manual.stem.replace("-", "—"), manual,
                        tags=["手册"], summary="操作手册（规则的家）"))


def scan_materials(rows):
    for mat in sorted((KNOW / "materials").glob("MAT-*.md")):
        rows.append(row(mat.stem.split("_")[0], "material", mat.stem, mat, tags=["素材"],
                        summary=mat.stem))


def build():
    rows, errors = [], []
    scan_deliverables(rows, errors)
    scan_assessment(rows, errors)
    scan_teaching(rows, errors)
    scan_manuals(rows)
    scan_materials(rows)
    seen = set()
    deduped = []
    for r in rows:
        if r["id"] in seen:
            continue
        seen.add(r["id"])
        deduped.append(r)
    return deduped, errors


def render_index(rows):
    lines = ["# INDEX（生成物——由 scripts/build_catalog.py 重建，勿手工编辑）", ""]
    by_type: dict[str, list] = {}
    for r in rows:
        by_type.setdefault(r["type"], []).append(r)
    for etype in sorted(by_type):
        lines.append(f"## {etype}（{len(by_type[etype])}）")
        lines.append("")
        lines.append("| ID | 标题 | 状态 | 权威 | 摘要 |")
        lines.append("|---|---|---|---|---|")
        for r in sorted(by_type[etype], key=lambda x: x["id"]):
            lines.append(f"| {r['id']} | {r['title'][:30]} | {r['status'] or '—'} | {r['authority'] or '—'} | {r['summary'][:40]} |")
        lines.append("")
    lines.append(f"> 共 {len(rows)} 实体 · 生成于 {date.today()} · 路径解析规则见 docs/architecture/ID解析表.md")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="只校验不写盘")
    args = parser.parse_args()

    rows, errors = build()
    for e in errors:
        print(f"[error] {e}")

    if args.check:
        missing = [r["id"] for r in rows if not (ROOT / r["path"]).exists()]
        never_used = sum(1 for r in rows if r["last_consumed"] is None)
        print(f"catalog 校验：{len(rows)} 实体 / 路径悬空 {len(missing)} / 未消费 {never_used}（首建全部未消费属正常）")
        for mid in missing:
            print(f"[error] 路径不可解析: {mid}")
        return 1 if (errors or missing) else 0

    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    with open(CATALOG, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    INDEX.write_text(render_index(rows), encoding="utf-8")
    never_used = sum(1 for r in rows if r["last_consumed"] is None)
    print(f"catalog：{len(rows)} 实体 → {CATALOG.relative_to(ROOT)}")
    print(f"视图 → {INDEX.relative_to(ROOT)}；未消费 {never_used}（首建属正常，后续由消费登记更新）")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
