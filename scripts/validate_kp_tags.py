#!/usr/bin/env python3
"""kp_tags.jsonl 考点标注门禁（题目语义 curate 层）。

校验每卷的 kp_tags.jsonl：
  1. 覆盖：与 questions.jsonl 的 question_id 一一对应（不多不少）；
  2. 词表受控：exam_points ⊆ _kp_vocab.yaml；
  3. 每题 1-4 个考点；
  4. kp_ids 可解析（存在于 deliverables.jsonl 的 CARD-* 集合）；
  5. mapping_level 仅允许 M0（M1+ 需答案核验与双向证据，禁止批量生成）；
  6. 兜底考点（综合学习）必须带非空 note。
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = ROOT / "work/knowledge/exams/papers"
VOCAB = BASE / "_kp_vocab.yaml"
DELIV = ROOT / "work/knowledge/_meta/deliverables.jsonl"

FALLBACK = "综合学习"


def load_vocab() -> set[str]:
    import yaml
    data = yaml.safe_load(VOCAB.read_text(encoding="utf-8"))
    return set(data["exam_points"].keys())


def load_cards() -> set[str]:
    cards = set()
    if DELIV.exists():
        for line in DELIV.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            did = r.get("deliverable_id", "")
            if did.startswith("CARD-"):
                cards.add(did)
    return cards


def validate(paper_dir: Path, vocab: set[str], cards: set[str]) -> tuple[bool, list[str]]:
    errs = []
    qj = paper_dir / "questions.jsonl"
    kt = paper_dir / "kp_tags.jsonl"
    if not qj.exists():
        return False, [f"{paper_dir.name}: 缺 questions.jsonl"]
    if not kt.exists():
        return False, [f"{paper_dir.name}: 缺 kp_tags.jsonl"]

    qids = [json.loads(l)["question_id"] for l in qj.read_text(encoding="utf-8").splitlines() if l.strip()]
    tags = []
    for i, line in enumerate(kt.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            tags.append(json.loads(line))
        except json.JSONDecodeError as e:
            errs.append(f"{paper_dir.name}: kp_tags.jsonl 第{i}行 JSON 解析失败: {e}")

    tids = [t.get("question_id", "") for t in tags]
    missing = set(qids) - set(tids)
    extra = set(tids) - set(qids)
    if missing:
        errs.append(f"{paper_dir.name}: 缺标注 {sorted(missing)[:5]}{'…' if len(missing) > 5 else ''}（共{len(missing)}题）")
    if extra:
        errs.append(f"{paper_dir.name}: 凭空标注 {sorted(extra)[:5]}")

    for t in tags:
        qid = t.get("question_id", "?")
        eps = t.get("exam_points", [])
        if not isinstance(eps, list) or not (1 <= len(eps) <= 4):
            errs.append(f"{paper_dir.name}: {qid} 考点数须 1-3，得 {eps}")
            continue
        bad = [e for e in eps if e not in vocab]
        if bad:
            errs.append(f"{paper_dir.name}: {qid} 考点不在词表: {bad}")
        if len(eps) == 1 and eps[0] == FALLBACK and not t.get("note", "").strip():
            errs.append(f"{paper_dir.name}: {qid} 兜底考点「{FALLBACK}」须带 note 说明")
        kp = t.get("kp_ids", [])
        if not isinstance(kp, list):
            errs.append(f"{paper_dir.name}: {qid} kp_ids 须为数组")
        else:
            badkp = [k for k in kp if k not in cards]
            if badkp:
                errs.append(f"{paper_dir.name}: {qid} kp_ids 不可解析: {badkp}")
        if t.get("mapping_level", "M0") != "M0":
            errs.append(f"{paper_dir.name}: {qid} mapping_level 批量产出仅允许 M0")
    return (not errs), errs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("targets", nargs="*", help="卷目录（缺省=全部 PAPER-*）")
    ap.add_argument("--batch", action="store_true", help="批处理模式：汇总输出")
    args = ap.parse_args()

    vocab = load_vocab()
    cards = load_cards()
    dirs = [Path(t) for t in args.targets] if args.targets else sorted(
        p for p in BASE.iterdir() if p.is_dir() and p.name.startswith("PAPER-"))

    total_pass, total_fail, all_errs = 0, 0, []
    for d in dirs:
        ok, errs = validate(d, vocab, cards)
        if ok:
            total_pass += 1
            if not args.batch:
                print(f"[PASS] {d.name}")
        else:
            total_fail += 1
            all_errs.extend(errs)
            if not args.batch:
                for e in errs:
                    print(f"[FAIL] {e}")
    if args.batch:
        for e in all_errs:
            print(f"[FAIL] {e}")
        print(f"考点标注校验：PASS {total_pass} 卷 / FAIL {total_fail} 卷")
    return 0 if total_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
