#!/usr/bin/env python3
"""answers.jsonl 答案层门禁（candidate 级）。

校验每卷的 answers.jsonl：
  1. 覆盖：与 questions.jsonl 的 question_id 一一对应（不多不少，含 missing:true 的行）；
  2. answer_type ∈ {objective, subjective}；
  3. 客观题 answer 须为字母组合（A-H，可含逗号/全角；五选二到 E、断句涂黑标号到 H）或 missing；
  4. missing:true 的行 answer 须为空串且 note 非空；
  5. source_basis 必填（标注答案来源与权威级，如"解析卷（S3 candidate）"）；
  6. excerpt 必填（答案定位摘录，客观题至少 10 字，防凭空编造）。
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "work/knowledge/exams/papers"
OBJ_RE = re.compile(r"^[A-H][A-H,，、\s]*$")


def validate(paper_dir: Path) -> tuple[bool, list[str]]:
    errs = []
    qj = paper_dir / "questions.jsonl"
    aj = paper_dir / "answers.jsonl"
    if not qj.exists():
        return False, [f"{paper_dir.name}: 缺 questions.jsonl"]
    if not aj.exists():
        return False, [f"{paper_dir.name}: 缺 answers.jsonl"]

    qids = [json.loads(l)["question_id"] for l in qj.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = []
    for i, line in enumerate(aj.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            errs.append(f"{paper_dir.name}: 第{i}行 JSON 解析失败: {e}")

    aids = [r.get("question_id", "") for r in rows]
    missing = set(qids) - set(aids)
    extra = set(aids) - set(qids)
    if missing:
        errs.append(f"{paper_dir.name}: 缺答案行 {sorted(missing)[:5]}（共{len(missing)}）")
    if extra:
        errs.append(f"{paper_dir.name}: 凭空答案行 {sorted(extra)[:5]}")

    for r in rows:
        qid = r.get("question_id", "?")
        at = r.get("answer_type", "")
        if at not in ("objective", "subjective"):
            errs.append(f"{paper_dir.name}: {qid} answer_type 非法: {at!r}")
        ans = r.get("answer", "")
        if r.get("missing", False):
            if ans != "":
                errs.append(f"{paper_dir.name}: {qid} missing 行 answer 须空串")
            if not r.get("note", "").strip():
                errs.append(f"{paper_dir.name}: {qid} missing 行须带 note")
        else:
            if not ans.strip():
                errs.append(f"{paper_dir.name}: {qid} answer 为空（应标 missing:true）")
            elif at == "objective" and not OBJ_RE.match(ans.strip()):
                errs.append(f"{paper_dir.name}: {qid} 客观题答案非字母组合: {ans!r}")
            if len(r.get("excerpt", "")) < 10:
                errs.append(f"{paper_dir.name}: {qid} excerpt 不足10字（防凭空）")
        if not r.get("source_basis", "").strip():
            errs.append(f"{paper_dir.name}: {qid} source_basis 必填")
    return (not errs), errs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("targets", nargs="*")
    ap.add_argument("--batch", action="store_true")
    args = ap.parse_args()
    dirs = [Path(t) for t in args.targets] if args.targets else sorted(
        p for p in BASE.iterdir() if p.is_dir() and p.name.startswith("PAPER-"))
    tp, tf, all_errs = 0, 0, []
    for d in dirs:
        ok, errs = validate(d)
        if ok:
            tp += 1
            if not args.batch:
                print(f"[PASS] {d.name}")
        else:
            tf += 1
            all_errs.extend(errs)
            if not args.batch:
                for e in errs:
                    print(f"[FAIL] {e}")
    if args.batch:
        for e in all_errs:
            print(f"[FAIL] {e}")
        print(f"答案层校验：PASS {tp} 卷 / FAIL {tf} 卷")
    return 0 if tf == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
