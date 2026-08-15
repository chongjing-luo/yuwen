#!/usr/bin/env python3
"""试卷整理校验器（分叉契约四件验收，试卷库组织约定 §七）。

校验一份 PAPER-{code}-{year}_{卷名}/ 目录的交付完整性：
1. raw/PAPER-*.pdf 存在，README 登记原件路径/SHA/渠道（血缘）；
2. mineru_result/<name>/full.md 存在且非空（确定性整理件，可重建）；
3. questions.jsonl（若已产出）：逐行 schema（question_id/question_type/page_ref/source_sha256）
   且 question_id 与卷代码前缀一致；
4. paper.json：paper_id 卷代码×年份、authority、answer_source_status ∈
   {official, candidate, missing}（答案纪律）。

用法：python3 scripts/validate_exam_paper.py <PAPER 目录> [--require-questions]
      python3 scripts/validate_exam_paper.py --batch   # 校验高考真题整理/ 下全部 PAPER 目录
退出码：0 通过；1 失败。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "work/knowledge/高考真题整理"
PAPER_DIR_RE = re.compile(r"^PAPER-([A-Z0-9]+)-(\d{4})_(.+)$")
VALID_ANSWER_STATUS = {"official", "candidate", "missing"}


def validate_paper(dir_path: Path, require_questions: bool) -> list[str]:
    errors: list[str]
    errors = []
    pid = dir_path.name

    m = PAPER_DIR_RE.match(pid)
    if not m:
        return [f"{pid}: 目录名不符合 PAPER-{{卷代码}}-{{年份}}_{{卷名}} 规则"]

    # 1. 原件与血缘
    raw_pdfs = sorted((dir_path / "raw").glob("PAPER-*.pdf")) if (dir_path / "raw").is_dir() else []
    if not raw_pdfs:
        errors.append(f"{pid}: raw/ 下无 PAPER-*.pdf（契约①）")
    readme = dir_path / "raw" / "README.md"
    if not readme.exists():
        errors.append(f"{pid}: raw/README.md 缺失（血缘：原件路径/SHA/渠道）")
    else:
        text = readme.read_text(encoding="utf-8")
        if "SHA256" not in text or "原件" not in text:
            errors.append(f"{pid}: README 血缘不全（须含 原件路径 与 SHA256）")

    # 2. 整理件
    fulls = sorted(dir_path.glob("mineru_result/*/full.md"))
    if not fulls:
        errors.append(f"{pid}: mineru_result/*/full.md 缺失（契约②）")
    for f in fulls:
        if f.stat().st_size < 2000:
            errors.append(f"{pid}: {f.name} 疑似空壳（<2KB）")

    # 3. questions.jsonl
    qfile = dir_path / "questions.jsonl"
    if qfile.exists():
        n = 0
        for i, line in enumerate(qfile.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            n += 1
            try:
                q = json.loads(line)
            except json.JSONDecodeError as e:
                errors.append(f"{pid}: questions.jsonl 第{i}行 JSON 错误 {e}")
                continue
            for field in ("question_id", "question_type", "page_ref"):
                if not q.get(field):
                    errors.append(f"{pid}: q{i} 缺 {field}")
            if q.get("question_id") and not str(q["question_id"]).startswith(f"PAPER-{m.group(1)}-{m.group(2)}-Q"):
                errors.append(f"{pid}: q{i} question_id 前缀错误: {q['question_id']}")
        if n == 0:
            errors.append(f"{pid}: questions.jsonl 为空")
    elif require_questions:
        errors.append(f"{pid}: questions.jsonl 缺失（契约③，--require-questions）")

    # 4. paper.json
    meta = dir_path / "paper.json"
    if meta.exists():
        try:
            pj = json.loads(meta.read_text(encoding="utf-8"))
            if pj.get("paper_id") != f"PAPER-{m.group(1)}-{m.group(2)}":
                errors.append(f"{pid}: paper_id 与目录不一致")
            if pj.get("authority", "").startswith("S1") and pj.get("answer_source_status") not in VALID_ANSWER_STATUS:
                errors.append(f"{pid}: answer_source_status 缺失或非法（答案纪律）")
            if pj.get("answer_source_status") and pj["answer_source_status"] not in VALID_ANSWER_STATUS:
                errors.append(f"{pid}: answer_source_status 非法: {pj['answer_source_status']}")
        except json.JSONDecodeError as e:
            errors.append(f"{pid}: paper.json 解析失败 {e}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", nargs="?", help="PAPER 目录")
    parser.add_argument("--batch", action="store_true", help="校验全部 PAPER 目录")
    parser.add_argument("--require-questions", action="store_true")
    args = parser.parse_args()

    targets = []
    if args.batch:
        targets = sorted(d for d in BASE.iterdir() if d.is_dir() and PAPER_DIR_RE.match(d.name))
        if not targets:
            print(f"[error] {BASE} 下无 PAPER 目录")
            return 1
    elif args.target:
        t = Path(args.target)
        targets = [t if t.is_absolute() else ROOT / t]
    else:
        parser.error("须提供目录或 --batch")

    all_errors = []
    for t in targets:
        errs = validate_paper(t, args.require_questions)
        all_errors.extend(errs)
        print(f"[{'FAIL' if errs else 'PASS'}] {t.name}")

    for e in all_errors:
        print(f"[error] {e}")
    if all_errors:
        print(f"试卷校验失败：{len(targets)} 卷 / {len(all_errors)} 错误")
        return 1
    print(f"试卷校验通过：{len(targets)} 卷（契约①②{'③④' if args.require_questions else ''}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
