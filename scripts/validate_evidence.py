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
import os
import re
import sys
from pathlib import Path

NODES = {f"K{i}" for i in range(1, 6)} | {f"U{i}" for i in range(1, 9)} | {f"J{i}" for i in range(1, 8)}
SHA_RE = re.compile(r"^[0-9a-f]{16,64}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
BAD_ERROR_TYPES = {"粗心", "马虎", "不认真", "态度问题"}
PREFIX = {"obs": "OBS-", "grd": "GRD-", "mr": "MR-", "ref": "REF-", "pr": "PR-"}

REQUIRED = {
    "obs": [
        "id", "date", "lesson_id", "lesson_version_sha", "g4_audit_lock_sha256",
        "host_release_event_id", "host_release_source", "node", "signal", "value", "source",
    ],
    "grd": ["id", "date", "class_id", "student_id", "homework_id", "item_id", "kp_id", "score", "max_score", "node"],
    "mr": ["date", "class_id", "student_id", "source", "kp_id", "score", "max_score"],
    "ref": ["id", "date", "lesson_id", "lesson_version_sha", "node", "evidence_ref", "phenomenon", "cause", "revision_target"],
    "pr": ["id", "trigger_evidence", "node", "change_type", "draft", "target_standard", "status"],
}


def validate_row(
    row: dict,
    etype: str,
    line_no: int,
    host_release_registry: dict | None = None,
    current_g4_audit_lock: dict | None = None,
    current_g4_audit_lock_sha256: str | None = None,
) -> list[str]:
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

    if etype == "obs":
        audit_sha = str(row.get("g4_audit_lock_sha256") or "")
        if audit_sha and not SHA256_RE.fullmatch(audit_sha):
            errors.append(f"{where}: g4_audit_lock_sha256 非合法SHA-256")
        current_sha = str(current_g4_audit_lock_sha256 or "")
        if not isinstance(current_g4_audit_lock, dict) or not SHA256_RE.fullmatch(current_sha):
            errors.append(f"{where}: 缺当前G4 audit_lock文件及其实哈希")
        else:
            if current_g4_audit_lock.get("schema_version") != "audit-lock.v1":
                errors.append(f"{where}: 当前G4 audit_lock schema_version错误")
            if current_g4_audit_lock.get("status") != "awaiting_host_release":
                errors.append(f"{where}: 当前G4 audit_lock状态错误")
            if current_g4_audit_lock.get("lesson_id") != row.get("lesson_id"):
                errors.append(f"{where}: 当前G4 audit_lock lesson_id不匹配")
            if current_sha != audit_sha:
                errors.append(f"{where}: 当前G4锁哈希与OBS/宿主放行对象不匹配")
        release_source = row.get("host_release_source")
        if not isinstance(release_source, dict):
            errors.append(f"{where}: host_release_source 必须为结构化宿主事件引用")
            release_source = {}
        else:
            for field in sorted(set(release_source) - {"locator", "record_sha256"}):
                errors.append(f"{where}: host_release_source 含未知字段 {field}")
        locator = str(release_source.get("locator") or "")
        record_sha = str(release_source.get("record_sha256") or "")
        if "://" not in locator or len(locator) < 16:
            errors.append(f"{where}: host_release_source.locator 不可追溯")
        if not SHA256_RE.fullmatch(record_sha):
            errors.append(f"{where}: host_release_source.record_sha256 非合法SHA-256")

        event_id = str(row.get("host_release_event_id") or "")
        registry_events = (
            host_release_registry.get("events") or {}
            if isinstance(host_release_registry, dict)
            and host_release_registry.get("schema_version") == "external-host-release-registry.v1"
            else {}
        )
        event = registry_events.get(event_id)
        if not isinstance(event, dict) or event.get("verified_by_host") is not True:
            errors.append(f"{where}: 缺已核验的宿主放行事件 {event_id or '?'}")
        else:
            expected = {
                "decision": "released",
                "lesson_id": row.get("lesson_id"),
                "g4_audit_lock_sha256": audit_sha,
                "locator": locator,
                "record_sha256": record_sha,
            }
            for field, expected_value in expected.items():
                if event.get(field) != expected_value:
                    errors.append(f"{where}: 宿主放行事件字段不匹配 {field}")

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


def load_external_host_release_registry(
    path: Path,
    project_root: Path,
) -> tuple[dict | None, list[str]]:
    """Load a host-owned release registry and reject project self-attestation."""
    errors: list[str] = []
    resolved = path.resolve()
    try:
        resolved.relative_to(project_root.resolve())
    except ValueError:
        pass
    else:
        return None, ["宿主放行事件注册表必须位于项目目录之外"]
    try:
        registry = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"宿主放行事件注册表无法读取: {exc}"]
    if registry.get("schema_version") != "external-host-release-registry.v1":
        errors.append("宿主放行事件注册表schema_version错误")
    if not isinstance(registry.get("events"), dict):
        errors.append("宿主放行事件注册表events必须为对象")
    return registry, errors


def load_current_g4_audit_lock(
    path: Path,
    project_root: Path,
) -> tuple[dict | None, str | None, list[str]]:
    """Load the exact project G4 object that a host release event names."""
    errors: list[str] = []
    resolved = path.resolve()
    try:
        relative = resolved.relative_to(project_root.resolve())
    except ValueError:
        return None, None, ["当前G4 audit_lock必须位于项目目录内"]
    if relative.name != "audit_lock.json" or relative.parent.name != "_meta":
        errors.append("当前G4对象必须是课程_meta/audit_lock.json")
    if len(relative.parts) < 4 or relative.parts[:2] != ("work", "teaching"):
        errors.append("当前G4 audit_lock必须位于work/teaching课程树")
    try:
        payload = resolved.read_bytes()
        lock = json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, None, errors + [f"当前G4 audit_lock无法读取: {exc}"]
    if not isinstance(lock, dict):
        errors.append("当前G4 audit_lock必须为对象")
        return None, None, errors
    import hashlib

    return lock, hashlib.sha256(payload).hexdigest(), errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file")
    parser.add_argument("--type", required=True, choices=list(PREFIX))
    parser.add_argument(
        "--host-release-registry",
        type=Path,
        default=os.environ.get("YUWEN_EXTERNAL_HOST_RELEASE_REGISTRY"),
        help="项目目录外、由宿主提供的external-host-release-registry.v1",
    )
    parser.add_argument(
        "--audit-lock",
        type=Path,
        help="OBS对应的当前项目work/teaching/<课>/_meta/audit_lock.json",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"[error] 文件不存在: {path}")
        return 1

    host_release_registry = None
    current_g4_audit_lock = None
    current_g4_audit_lock_sha256 = None
    all_errors, count = [], 0
    if args.type == "obs":
        if args.host_release_registry:
            host_release_registry, registry_errors = load_external_host_release_registry(
                args.host_release_registry,
                Path(__file__).resolve().parents[1],
            )
            all_errors.extend(registry_errors)
        else:
            all_errors.append("OBS缺项目外宿主放行事件注册表；S6默认失败关闭")
        if args.audit_lock:
            (
                current_g4_audit_lock,
                current_g4_audit_lock_sha256,
                audit_lock_errors,
            ) = load_current_g4_audit_lock(
                args.audit_lock,
                Path(__file__).resolve().parents[1],
            )
            all_errors.extend(audit_lock_errors)
        else:
            all_errors.append("OBS缺当前项目G4 audit_lock；S6默认失败关闭")
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        count += 1
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            all_errors.append(f"line{i}: JSON 解析失败 {exc}")
            continue
        all_errors.extend(
            validate_row(
                row,
                args.type,
                i,
                host_release_registry=host_release_registry,
                current_g4_audit_lock=current_g4_audit_lock,
                current_g4_audit_lock_sha256=current_g4_audit_lock_sha256,
            )
        )

    for e in all_errors:
        print(f"[error] {e}")
    if all_errors:
        print(f"证据校验失败：{count} 行 / {len(all_errors)} 错误")
        return 1
    print(f"证据校验通过：{count} 行（{args.type}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
