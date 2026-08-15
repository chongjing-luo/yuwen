#!/usr/bin/env python3
"""证据层记录校验器（L4 · 设计方案 §6 S6/S7/S8/S9 跳门禁）。

校验 OBS/GRD/MR/REF/PR 五类 jsonl：
1. 必填字段与类型；id 前缀匹配类型；
2. node ∈ 20 机制节点（OBS/GRD/REF 必填；PR 必填）；
3. lesson_version_sha 为 16+ 位 hex（OBS/REF）；
4. score ∈ [0, max_score]，max_score > 0（GRD/MR）；
5. error_type 若非空不得为"粗心/马虎"类不可操作词；
6. REF.evidence_ref / PR.trigger_evidence 非空；
7. PR.change_type 枚举合法，draft.enforcement 每项有 type。

用法：python3 scripts/validate_evidence.py <file.jsonl> --type obs|grd|mr|ref|pr
退出码：0 通过；1 有错误行。synthetic 数据只准在 tests/fixtures/（本脚本不限制路径，
写入真实 _classes 目录前由人保证真实性——P-12）。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

NODES = {f"K{i}" for i in range(1, 6)} | {f"U{i}" for i in range(1, 9)} | {f"J{i}" for i in range(1, 8)}
SHA_RE = re.compile(r"^[0-9a-f]{16,64}$")
BAD_ERROR_TYPES = {"粗心", "马虎", "不认真", "态度问题"}
PREFIX = {"obs": "OBS-", "grd": "GRD-", "mr": "MR-", "ref": "REF-", "pr": "PR-"}

REQUIRED = {
    "obs": ["id", "date", "lesson_id", "lesson_version_sha", "node", "signal", "value", "source"],
    "grd": ["id", "date", "class_id", "student_id", "homework_id", "item_id", "kp_id", "score", "max_score", "node"],
    "mr": ["date", "class_id", "student_id", "source", "kp_id", "score", "max_score"],
    "ref": ["id", "date", "lesson_id", "lesson_version_sha", "node", "evidence_ref", "phenomenon", "cause", "revision_target"],
    "pr": ["id", "trigger_evidence", "node", "change_type", "draft", "target_standard", "status"],
}


def validate_row(row: dict, etype: str, line_no: int) -> list[str]:
    errors = []
    where = row.get("id", f"line{line_no}")

    for field in REQUIRED[etype]:
        if field not in row or row[field] in (None, "", []):
            errors.append(f"{where}: 缺必填字段 {field}")

    if etype in PREFIX and "id" in row:  # mr 的 id 可选（存量 analyze_mastery 兼容）
        if not str(row.get("id", "")).startswith(PREFIX[etype]):
            errors.append(f"{where}: id 前缀应为 {PREFIX[etype]}")

    if etype in ("obs", "grd", "ref", "pr"):
        if row.get("node") not in NODES:
            errors.append(f"{where}: node 非法: {row.get('node')!r}（须为 K1-K5/U1-U8/J1-J7）")

    if etype in ("obs", "ref"):
        sha = str(row.get("lesson_version_sha", ""))
        if sha and not SHA_RE.match(sha):
            errors.append(f"{where}: lesson_version_sha 非 16+ hex")

    if etype in ("grd", "mr"):
        score, mx = row.get("score"), row.get("max_score")
        if isinstance(score, (int, float)) and isinstance(mx, (int, float)):
            if mx <= 0 or score < 0 or score > mx:
                errors.append(f"{where}: score/max_score 非法 ({score}/{mx})")
        et = row.get("error_type")
        if et in BAD_ERROR_TYPES:
            errors.append(f"{where}: error_type 不可操作: {et}")

    if etype == "ref" and isinstance(row.get("evidence_ref"), list) and not row["evidence_ref"]:
        errors.append(f"{where}: evidence_ref 为空")

    if etype == "pr":
        if row.get("change_type") not in {"new", "modify", "retire"}:
            errors.append(f"{where}: change_type 非法")
        draft = row.get("draft") or {}
        for en in draft.get("enforcement") or []:
            if not isinstance(en, dict) or not en.get("type"):
                errors.append(f"{where}: draft.enforcement 条目缺 type")
        if not row.get("trigger_evidence"):
            errors.append(f"{where}: trigger_evidence 为空（收敛准入：无触发证据不收）")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument("--type", required=True, choices=list(PREFIX))
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"[error] 文件不存在: {path}")
        return 1

    all_errors, count = [], 0
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        count += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            all_errors.append(f"line{i}: JSON 解析失败 {exc}")
            continue
        all_errors.extend(validate_row(row, args.type, i))

    for e in all_errors:
        print(f"[error] {e}")
    if all_errors:
        print(f"证据校验失败：{count} 行 / {len(all_errors)} 错误")
        return 1
    print(f"证据校验通过：{count} 行（{args.type}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
