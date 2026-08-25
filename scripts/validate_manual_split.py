#!/usr/bin/env python3
"""人工切题验收器（agent 产物的门禁）：逐字保真 + 结构一致。

检查一份 PAPER 目录（agent 手动切割后的 questions/）：
1. **覆盖率（防丢内容）**：full.md 每一非空行（规范化空白后）必须出现在
   某个 questions/*.md 或 boilerplate.md 中；缺失即 FAIL；
2. **无凭空内容（防幻觉）**：题目文件中每一行（剥离标题行与标记）必须来自
   full.md（规范化后），多出的行即疑似 agent 改写/补写；
3. 结构：questions.jsonl 与 Q*.md 一一对应；命名 Q{NN}_{type}.md；题型在受控词表内；
4. 台账补算：content_sha256 / chars 由本脚本写入（agent 不做哈希）。

用法：python3 scripts/validate_manual_split.py <PAPER 目录>
退出码：0 通过；1 失败（覆盖率/凭空内容/结构任一不过）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPES = {
    "modern_reading", "modern_reading_argumentative", "modern_reading_practical",
    "modern_reading_literary", "reading_general", "classical_reading",
    "poetry_appreciation", "memorization", "language_use", "writing",
    "whole_book_reading", "culture_knowledge", "unknown",
}
# 标记行（题目文件里允许的格式行，不参与逐字比对）
MARK_RE = re.compile(r"^(# |【|〉|>|\[OCR\?\])")


def norm(line: str) -> str:
    return re.sub(r"[\s\u3000]+", "", line)


def content_lines(text: str) -> set[str]:
    out = set()
    for line in text.splitlines():
        n = norm(line)
        if n:
            out.add(n)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paper_dir")
    args = ap.parse_args()
    d = Path(args.paper_dir)
    if not d.is_absolute():
        d = ROOT / d

    full = next(d.glob("mineru_result/*/full.md"), None)
    qdir = d / "questions"
    ledger_f = d / "questions.jsonl"
    if full is None or not qdir.is_dir() or not ledger_f.exists():
        print(f"[error] {d.name}: 缺 full.md / questions/ / questions.jsonl")
        return 1

    src_lines = content_lines(full.read_text(encoding="utf-8"))
    out_lines: set[str] = set()
    qfiles = sorted(qdir.glob("Q*.md"))
    boiler = d / "boilerplate.md"
    if boiler.exists():
        out_lines |= content_lines(boiler.read_text(encoding="utf-8"))

    errors = []
    for qf in qfiles:
        text = qf.read_text(encoding="utf-8")
        for line in text.splitlines():
            if MARK_RE.match(line):
                continue
            n = norm(line)
            if n:
                out_lines.add(n)

    missing = src_lines - out_lines          # 丢内容
    invented = {l for l in out_lines - src_lines if len(l) >= 8}  # 凭空/改写（短行容忍标点差）

    if missing:
        errors.append(f"覆盖率缺失 {len(missing)} 行（源文件有而产物无）")
        for l in sorted(missing)[:5]:
            print(f"  [missing] {l[:50]}")
    if invented:
        errors.append(f"疑似凭空/改写 {len(invented)} 行（产物有而源文件无）")
        for l in sorted(invented)[:5]:
            print(f"  [invented?] {l[:50]}")

    # 结构与台账
    ledger = [json.loads(l) for l in ledger_f.read_text(encoding="utf-8").splitlines() if l.strip()]
    ledger_files = {r.get("qfile") for r in ledger}
    actual_files = {f"questions/{f.name}" for f in qfiles}
    if ledger_files != actual_files:
        errors.append(f"台账与文件不一致: 仅台账 {sorted(ledger_files - actual_files)} / 仅文件 {sorted(actual_files - ledger_files)}")
    for r in ledger:
        if r.get("question_type") not in TYPES:
            errors.append(f"{r.get('question_id')}: 题型非法 {r.get('question_type')!r}")
    if not re.fullmatch(r"PAPER-[A-Z0-9]+-\d{4}", ledger[0]["question_id"].rsplit("-Q", 1)[0]) if ledger else False:
        errors.append("question_id 前缀非法")

    # 补算哈希与字数（机器侧，agent 不做）
    for r in ledger:
        qf = d / r["qfile"]
        if qf.exists():
            raw = qf.read_text(encoding="utf-8")
            r["content_sha256"] = hashlib.sha256(raw.encode()).hexdigest()
            r["chars"] = len(raw)
            r.setdefault("type_evidence", "manual")
    ledger_f.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in ledger) + "\n", encoding="utf-8")

    if errors:
        for e in errors:
            print(f"[error] {e}")
        print(f"人工切题验收 FAIL：{d.name}")
        return 1
    print(f"人工切题验收 PASS：{d.name}（{len(qfiles)} 题，覆盖 {len(src_lines)} 行零缺失零改写）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
