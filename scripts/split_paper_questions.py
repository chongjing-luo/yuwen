#!/usr/bin/env python3
"""试卷切割与格式清理器（organize 配方核心步：full.md → 每题一文件 + by_type 视图）。

清理规则【保守，只做确定性变换】：
  1. 文档顶部卷务模板段（注意事项/考生注意/绝密★启用前/本试卷共…）不入题目；
  2. 行内合并的选项拆分：一行内出现 ≥2 个 "A./B./C./D." 锚点 → 在每个锚点前断行；
  3. 空 Trojan 行（纯符号/页码）剔除；
  4. 不修词、不猜字——存疑保留原文（S3 纪律）。

输出：
  questions/Q{n:02d}_{type}.md —— 题目全文（含选项与随题材料）
  questions.jsonl 更新 —— 附加 qfile / content_sha256 / line_span
  by_type/{type}.md —— 全库题型视图（生成物）
用法：python3 scripts/split_paper_questions.py <PAPER 目录> [...] | --all
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "work/knowledge/高考真题整理"

SECTION_RE = re.compile(r"^##\s+[一二三四五六七八九十]+[、．.\s]\s*(.+?)(?:[（(]?(\d+)分[）)])?\s*$")
SUB_RE = re.compile(r"^##\s+[（(][一二三四五六七八九十]+[)）]\s*(.+?)(?:[（(]本题共(\d+)小题[，,](\d+)分[）)])?\s*$")
Q_RE = re.compile(r"^(\d{1,2})[.．、]\s*(.*)")
OPTION_ANCHOR = re.compile(r"(?<=[^\d])[ ]?([A-D])[.．]\s")
BOILER_RE = re.compile(r"^(注意事项|考生注意|绝密|本试卷共|考试结束后|答卷前|答题前|第\s*\d+\s*页|共\s*\d+\s*页|语文\s*$|\(共|\（共)")
TYPE_MAP = [
    (r"论述类文本", "modern_reading_argumentative"), (r"实用类文本", "modern_reading_practical"),
    (r"文学类文本|文学文本", "modern_reading_literary"), (r"现代文阅读", "modern_reading"),
    (r"古代诗文阅读|古代诗文", "classical_reading"), (r"文言文", "classical_reading"),
    (r"古代诗歌|诗歌鉴赏|诗词鉴赏", "poetry_appreciation"),
    (r"名篇名句默写|默写|名句", "memorization"),
    (r"语言文字运用|表达运用|语言运用|积累与运用|积累运用", "language_use"),
    (r"古代文学常识|文学常识|文化常识", "culture_knowledge"),
    (r"整本书阅读|名著阅读", "whole_book_reading"),
    (r"论述类|非连续性文本", "modern_reading"),
    (r"写作|作文|表达与交流", "writing"),
    (r"^阅读$|^一 阅读|阅读理解", "reading_general"),
]


METADATA_NAME = re.compile(r"^[\s（(0-9０-９，,。．.每小题共分大题本题目*★～~—－-]*$")

CONTENT_TYPE_RULES = [
    (r"阅读下面[的]?(文字|材料|作品|文章?)|阅读下文", "modern_reading"),
    (r"阅读下面的文言文|文言文阅读", "classical_reading"),
    (r"阅读下面这首|古代诗歌阅读|这首词|这首诗", "poetry_appreciation"),
    (r"补写出?下列|空缺部分|默写", "memorization"),
    (r"写一?篇文章|不少于\s*\d+\s*字|作文", "writing"),
    (r"阅读下面的(文字|材料|作品)", "modern_reading"),
    (r"论述类文本", "modern_reading_argumentative"),
    (r"实用类文本", "modern_reading_practical"),
    (r"文学类文本|文学文本", "modern_reading_literary"),
    (r"语言文字运用|成语|病句|标点|衔接|词语", "language_use"),
    (r"整本书阅读|名著", "whole_book_reading"),
    (r"文学常识|文化常识", "culture_knowledge"),
]


def clean_section_name(name: str) -> str:
    """剥离节名里的分值/小题数元数据（格式清理）。"""
    cleaned = re.sub(r"[（(][^（）()]*?(?:分|小题)[^（）()]*?[）)]", "", name)
    cleaned = re.sub(r"本大题[^，。]*?[，。]?", "", cleaned)
    cleaned = re.sub(r"[\d０-９]+\s*分", "", cleaned)
    return cleaned.strip(" 、．.，,") or name.strip()


def is_metadata_name(name: str) -> bool:
    if METADATA_NAME.match(name):
        return True
    cleaned = clean_section_name(name)
    return not re.search(r"[\u4e00-\u9fa5]{2}", cleaned)


def map_type(name: str) -> str:
    if is_metadata_name(name):
        return ""
    for pat, t in TYPE_MAP:
        if re.search(pat, name):
            return t
    return ""


def classify_by_content(text: str) -> str:
    head = text[:160]
    for pat, t in CONTENT_TYPE_RULES:
        if re.search(pat, head):
            return t
    return ""


MIDLINE_Q = re.compile(r"(?<=[。；！？)）])\s*(\d{1,2})[.．、]\s*(?=[^\s\d])")
OPT_SPLIT = re.compile(r'(?<=[。；）)（）\s])([A-D])[.．][\u3000 ]?')


def logical_lines(body: list[str]) -> list[str]:
    """OCR 修复三步（保守）：
    ① 断字合并：单独一行 A-D 与下一行 . 开头 → 合并；
    ② 行中题号切分：句读后跟 "N." → 断为新行（题界被合并行吞掉的主因）；
    ③ 行中选项切分：句读/括号后跟 "A." → 断行。"""
    merged = []
    i = 0
    while i < len(body):
        line = body[i].strip()
        if re.fullmatch(r"[A-D]", line) and i + 1 < len(body):
            nxt = body[i + 1].lstrip()
            if nxt.startswith((".", "．", "、")):
                merged.append(line + nxt)
                i += 2
                continue
        merged.append(line)
        i += 1
    out = []
    for line in merged:
        if not line:
            continue
        parts_q = [p for p in MIDLINE_Q.split(line) if p]
        if len(parts_q) >= 2:
            # split 带捕获组：[前段, N1, 中段, N2, 后段…] → 重组成 "N. 中段" 行
            rebuilt = [parts_q[0]]
            for j in range(1, len(parts_q) - 1, 2):
                rebuilt.append(parts_q[j] + ". " + parts_q[j + 1])
            if len(parts_q) % 2 == 0:
                rebuilt.append(parts_q[-1])
            line_out = rebuilt
        else:
            line_out = [line]
        for ln in line_out:
            parts_o = [p for p in OPT_SPLIT.split(ln) if p]
            if len(parts_o) >= 3:
                reb = [parts_o[0]]
                for j in range(1, len(parts_o) - 1, 2):
                    reb.append(parts_o[j] + ". " + parts_o[j + 1])
                if len(parts_o) % 2 == 0:
                    reb.append(parts_o[-1])
                out.extend(reb)
            else:
                out.append(ln)
    return out


def clean_question_lines(lines: list[str]) -> list[str]:
    out = []
    for line in lines:
        stripped = line.strip()
        if not stripped or BOILER_RE.match(stripped):
            continue
        out.append(stripped)
    return out


def split_paper(paper_dir: Path) -> tuple[int, list[str]]:
    full = next(paper_dir.glob("mineru_result/*/full.md"), None)
    if full is None:
        return 0, [f"{paper_dir.name}: 无 full.md"]
    pid = paper_dir.name.split("_")[0]
    lines = full.read_text(encoding="utf-8").splitlines()

    # 跳过首个分节前的卷务模板
    first_section = next((i for i, l in enumerate(lines) if SECTION_RE.match(l) or SUB_RE.match(l)), 0)
    body = logical_lines(lines[first_section:])

    questions = []  # (num, start_idx, section, subsection, type)
    section = sub = None
    header_idx = 0
    pending_preamble = ""
    for i, line in enumerate(body):
        ms = SECTION_RE.match(line)
        if ms:
            section = {"name": ms.group(1)}
            sub = None
            header_idx, pending_preamble = i, ""
            continue
        mb = SUB_RE.match(line)
        if mb:
            sub = {"name": mb.group(1)}
            header_idx, pending_preamble = i, ""
            continue
        mq = Q_RE.match(line)
        if mq and (section or sub):
            ctx = sub or section
            first_after_header = not questions or questions[-1]["idx"] < header_idx
            if first_after_header:
                pending_preamble = "\n".join(body[header_idx + 1:i])
            questions.append({"num": int(mq.group(1)), "idx": i, "section": section["name"] if section else "",
                              "subsection": ctx["name"], "qtype": map_type(ctx["name"]),
                              "preamble": pending_preamble if first_after_header else ""})

    errors, qdir, material_fragments = [], paper_dir / "questions", []
    if qdir.exists():
        for f in qdir.glob("Q*.md"):
            f.unlink()
    qdir.mkdir(exist_ok=True)

    # 第一遍：切片 + 内容判型
    records = []
    for qi, q in enumerate(questions):
        end = questions[qi + 1]["idx"] if qi + 1 < len(questions) else len(body)
        cleaned = clean_question_lines(body[q["idx"]:end])
        if not cleaned:
            errors.append(f"{pid}: Q{q['num']:02d} 清理后为空")
            continue
        content = "\n".join(cleaned)
        records.append({
            "q": q, "cleaned": cleaned, "content": content,
            "qtype": q["qtype"] or classify_by_content(content) or "",
            "evidence": "section_name" if q["qtype"] else ("content_keyword" if classify_by_content(content) else ""),
            "span": [first_section + q["idx"] + 1, first_section + end],
        })

    # 第二遍：节内传播——同节已判题型 / 节前导材料（阅读材料开头含"阅读下面的文言文"等强信号）补齐
    from itertools import groupby
    for _, grp in groupby(records, key=lambda r: (r["q"]["section"], r["q"]["subsection"])):
        grp = list(grp)
        known = {r["qtype"] for r in grp if r["qtype"]}
        if len(known) == 1:
            fill = known.pop()
        else:
            preamble = next((r["q"].get("preamble", "") for r in grp if r["q"].get("preamble")), "")
            fill = classify_by_content(preamble) if preamble else ""
        if fill:
            for r in grp:
                if not r["qtype"]:
                    r["qtype"] = fill
                    r["evidence"] = r["evidence"] or "preamble_or_section_propagation"

    ledger = []
    for rec in records:
        q, cleaned, content = rec["q"], rec["cleaned"], rec["content"]
        qtype = rec["qtype"] or "unknown"
        sub_display = clean_section_name(q["subsection"]) if q["subsection"] else (clean_section_name(q["section"]) if q["section"] else "")
        fname = f"Q{q['num']:02d}_{qtype}.md"
        (qdir / fname).write_text(
            f"# {pid} 第{q['num']}题（{sub_display}）\n\n" + content + "\n", encoding="utf-8")
        if qtype == "writing" and q["num"] > 3:
            material_fragments.append(cleaned)
            continue
        ledger.append({
            "question_id": f"{pid}-Q{q['num']:02d}", "num": q["num"],
            "question_type": qtype,
            "section": clean_section_name(q["section"]) if q["section"] else "",
            "subsection": sub_display,
            "type_evidence": rec["evidence"] or "none",
            "qfile": f"questions/{fname}",
            "content_sha256": hashlib.sha256(content.encode()).hexdigest(),
            "line_span": rec["span"],
            "chars": len(content),
        })

    if material_fragments and ledger:
        last = ledger[-1]
        if last["question_type"] == "writing":
            qf = paper_dir / last["qfile"]
            frag = "\n\n【作文材料（整理保留）】\n" + "\n".join("\n".join(c) for c in material_fragments)
            with open(qf, "a", encoding="utf-8") as fh:
                fh.write(frag)
            last["material_fragments_merged"] = len(material_fragments)
    (paper_dir / "questions.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in ledger) + "\n", encoding="utf-8")
    return len(ledger), errors


def rebuild_by_type():
    bt = BASE / "by_type"
    if bt.exists():
        for f in bt.glob("*.md"):
            f.unlink()
    bt.mkdir(exist_ok=True)
    index = defaultdict(list)
    for d in sorted(BASE.iterdir()):
        if not (d.is_dir() and d.name.startswith("PAPER-")):
            continue
        qf = d / "questions.jsonl"
        if not qf.exists():
            continue
        for line in qf.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            q = json.loads(line)
            index[q["question_type"]].append(f"{q['question_id']}｜{d.name}｜{q.get('chars', 0)} 字")
    for t, items in sorted(index.items()):
        (bt / f"{t}.md").write_text(
            f"# {t}（{len(items)} 题，生成物勿手编）\n\n" + "\n".join(items) + "\n", encoding="utf-8")
    return {t: len(v) for t, v in index.items()}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("targets", nargs="*")
    ap.add_argument("--all", action="store_true")
    args = ap.parse_args()
    papers = sorted(BASE.iterdir()) if args.all else [ROOT / t for t in args.targets]
    papers = [p for p in papers if p.is_dir() and p.name.startswith("PAPER-")]
    total, all_err = 0, []
    for p in papers:
        n, errs = split_paper(p)
        total += n
        all_err.extend(errs)
        if errs:
            print(f"⚠️ {p.name}: {n} 题 / {len(errs)} 异常")
    stats = rebuild_by_type() if args.all else None
    print(f"切割完成：{len(papers)} 卷 / {total} 题")
    if stats:
        print("题型分布:", dict(sorted(stats.items(), key=lambda kv: -kv[1])))
    for e in all_err[:20]:
        print(f"  [warn] {e}")
    return 1 if all_err else 0


if __name__ == "__main__":
    sys.exit(main())
