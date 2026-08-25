#!/usr/bin/env python3
"""生成阅读组视图（人读聚合层，2026-08-17 方案②裁决）。

目的：切题产物按题拆分、材料整篇归组内第一题（单一归属），单题文件不自足；
本脚本在其上生成"组视图"——每个共享材料的题组聚合为一个可读文件
（材料 + 组内各题题目区按卷面顺序），不改动题目文件与三层账本。

组规则：
  1. 题文件含【材料】区 → 开新组；
  2. 无【材料】的题归入当前组，当且仅当与组内上一题 section 相同（分节变化必断组）；
  3. 卷首连续无材料题（语用单题）不构成组，跳过（单题文件本自足）。

产出：`<卷目录>/groups/G{组号}_Q{首}-{尾}_{组名}.md`；重跑幂等（先清空 groups/）。
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "work/knowledge/exams/papers"

MATERIAL_RE = re.compile(r"^【材料】")
QUESTION_RE = re.compile(r"^【题目】")
TITLE_RE = re.compile(r"^# ")


def split_qfile(text: str) -> tuple[str, str]:
    """返回 (材料区行, 题目区行)；无材料时材料区为空串。"""
    lines = text.splitlines()
    material, question, mode = [], [], None
    for line in lines:
        if MATERIAL_RE.match(line.strip()):
            mode = "m"; continue
        if QUESTION_RE.match(line.strip()):
            mode = "q"; question.append(line); continue
        if TITLE_RE.match(line):
            continue  # 题文件自身标题不入视图
        (material if mode == "m" else question if mode == "q" else []).append(line)
    return "\n".join(material).strip("\n"), "\n".join(question).strip("\n")


def build_paper(paper_dir: Path) -> int:
    qj = paper_dir / "questions.jsonl"
    if not qj.exists():
        return 0
    entries = [json.loads(l) for l in qj.read_text(encoding="utf-8").splitlines() if l.strip()]
    groups, cur = [], None
    for e in entries:
        qf = paper_dir / e["qfile"]
        if not qf.exists():
            continue
        material, question = split_qfile(qf.read_text(encoding="utf-8"))
        sec = e.get("section", "")
        if material:
            cur = {"material": material, "items": [(e, question)], "section": sec}
            groups.append(cur)
        elif cur and cur["items"] and cur["items"][-1][0].get("section", "") == sec:
            cur["items"].append((e, question))
        else:
            cur = None  # 无材料且不接续：独立题，不成组
    # 只保留 2 题以上的组（单题带材料的组其题文件已含材料，无需视图）
    groups = [g for g in groups if len(g["items"]) >= 2]

    out = paper_dir / "groups"
    if out.exists():
        for f in out.glob("G*.md"):
            f.unlink()
    out.mkdir(exist_ok=True)
    paper_id = paper_dir.name.split("_")[0]
    for i, g in enumerate(groups, 1):
        first, last = g["items"][0][0], g["items"][-1][0]
        def qnum(e):
            n = str(e["num"]).zfill(2)
            return f"{n}{e['question_id'][-1]}" if e["question_id"][-1] in "AB" else n
        name = (first.get("section") or first.get("question_type", "")).strip()
        name = re.sub(r"[\\/:*?\"<>|\s]+", "_", name)[:30]
        lines = [f"# {paper_id} 第{first['num']}-{last['num']}题组（{name}）", ""]
        lines += ["【材料】", g["material"], ""]
        for e, question in g["items"]:
            lines.append(question)
            lines.append("")
        (out / f"G{i:02d}_Q{qnum(first)}-Q{qnum(last)}_{name}.md").write_text(
            "\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return len(groups)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("targets", nargs="*")
    args = ap.parse_args()
    dirs = [Path(t) for t in args.targets] if args.targets else sorted(
        p for p in BASE.iterdir() if p.is_dir() and p.name.startswith("PAPER-"))
    total = 0
    for d in dirs:
        n = build_paper(d)
        total += n
    print(f"组视图生成完毕：{len(dirs)} 卷共 {total} 个组 → 各卷 groups/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
