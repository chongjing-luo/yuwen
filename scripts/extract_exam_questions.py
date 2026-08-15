#!/usr/bin/env python3
"""试卷题目结构抽取器（organize 配方：MinerU full.md → questions.jsonl + paper.json）。

结构层抽取（候选级，非知识断言）：
- 大节：`## 一、现代文阅读（36分）` → section（名/分值）
- 小节：`## （一）论述类文本阅读（本题共3小题，9分）` → 题数与分值
- 题号：行首 `1.` / `1、`
- 首行标题用于卷身份自校验（paper.json.identity_check）
page_ref 用 md 行锚（md:L{n}）；status=candidate；语义题型待 curate 阶段细化。

用法：python3 scripts/extract_exam_questions.py <PAPER 目录> [...]
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SECTION_RE = re.compile(r"^##\s+[一二三四五六七八九十]+、(.+?)(?:（(\d+)分）)?\s*$")
SUB_RE = re.compile(r"^##\s+（[一二三四五六七八九十]+）(.+?)(?:（本题共(\d+)小题[，,](\d+)分）)?\s*$")
Q_RE = re.compile(r"^(\d{1,2})[.．、]\s*(.*)")

TYPE_MAP = [
    (r"论述类文本", "modern_reading_argumentative"),
    (r"实用类文本", "modern_reading_practical"),
    (r"文学类文本|文学文本", "modern_reading_literary"),
    (r"现代文阅读", "modern_reading"),
    (r"文言文", "classical_reading"),
    (r"古代诗歌|诗歌鉴赏", "poetry_appreciation"),
    (r"名篇名句默写|默写", "memorization"),
    (r"语言文字运用", "language_use"),
    (r"写作|作文", "writing"),
]


def map_type(name: str) -> str:
    for pat, t in TYPE_MAP:
        if re.search(pat, name):
            return t
    return "unknown"


def extract(paper_dir: Path) -> tuple[list[dict], dict]:
    full = next(paper_dir.glob("mineru_result/*/full.md"), None)
    if full is None:
        raise FileNotFoundError(f"{paper_dir.name}: 无 full.md")
    md_sha = hashlib.sha256(full.read_bytes()).hexdigest()
    lines = full.read_text(encoding="utf-8").splitlines()

    title = next((l.lstrip("# ").strip() for l in lines[:5] if l.startswith("#")), "")
    questions = []
    section = sub = None
    for i, line in enumerate(lines, 1):
        ms = SECTION_RE.match(line)
        if ms:
            section = {"name": ms.group(1), "points": ms.group(2)}
            sub = None
            continue
        mb = SUB_RE.match(line)
        if mb:
            sub = {"name": mb.group(1), "n": mb.group(2), "points": mb.group(3)}
            continue
        mq = Q_RE.match(line)
        if mq and (section or sub):
            context = (sub or section)
            questions.append({
                "question_id": None,  # 下方按卷前缀填充
                "question_type": map_type(context["name"]),
                "section": section["name"] if section else None,
                "subsection": context["name"],
                "declared_count": int(sub["n"]) if sub and sub["n"] else None,
                "stem_excerpt": mq.group(2)[:60],
                "page_ref": f"md:L{i}",
                "source_sha256": md_sha,
                "status": "candidate",
            })

    m = re.match(r"PAPER-([A-Z0-9]+)-(\d{4})", paper_dir.name)
    prefix = f"PAPER-{m.group(1)}-{m.group(2)}-Q"
    for i, q in enumerate(questions, 1):
        q["question_id"] = f"{prefix}{i:02d}"

    meta = {
        "paper_id": f"PAPER-{m.group(1)}-{m.group(2)}",
        "title": title,
        "year": int(m.group(2)),
        "authority": "S1待核验",
        "answer_source_status": "candidate",
        "answer_note": "解析卷（S3 第三方）在采集库中，未核验——题-KP 维持 M0",
        "full_md": str(full.relative_to(ROOT)),
        "full_md_sha256": md_sha,
        "question_count": len(questions),
        "identity_check": {"declared_title": title, "expected_paper": paper_dir.name.split("_")[0]},
        "status": "candidate",
    }
    return questions, meta


def main() -> int:
    targets = [Path(a) if Path(a).is_absolute() else ROOT / a for a in sys.argv[1:]]
    if not targets:
        print("用法: extract_exam_questions.py <PAPER 目录> [...]")
        return 1
    for t in targets:
        qs, meta = extract(t)
        (t / "questions.jsonl").write_text(
            "\n".join(json.dumps(q, ensure_ascii=False) for q in qs) + "\n", encoding="utf-8")
        (t / "paper.json").write_text(
            json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"{t.name}: {len(qs)} 题 / {meta['title'][:30]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
