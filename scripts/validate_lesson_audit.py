#!/usr/bin/env python3
"""Validate the generic G4 independent-audit lock for one lesson.

This gate revalidates the frozen G3 lineage and checks that visual and student-
reception review receipts bind the same artifacts and standard snapshot.  It
cannot authenticate a human from local JSON alone; that external review-gate
boundary must be stated in each receipt and checked against the host record.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

from validate_lesson_lineage import validate_materials_lock
from validate_lesson_evidence import has_pending_classroom_boundary
from validate_lesson_plan import canonical_json_sha256

ROOT = Path(__file__).resolve().parents[1]
CHECKS_DIR = ROOT / "scripts/checks"
sys.path.insert(0, str(CHECKS_DIR))

from run_principle_checks import check_config_drift, run_checks  # noqa: E402
from validate_principle_registry import validate as validate_principle_registry  # noqa: E402

REVIEW_ROLES = {"visual", "student_reception"}
REQUIRED_MACHINE_CHECKS = {"g0-g3-lineage", "lesson-schema-strict", "principle-checks"}
SEVERITIES = {"P0", "P1", "P2", "P3"}
NODE_IDS = {f"K{i}" for i in range(1, 6)} | {f"U{i}" for i in range(1, 9)} | {f"J{i}" for i in range(1, 8)}
P3_RISK_CATEGORIES = {"office_rendering", "classroom_pacing", "learning_effect"}
SHA256_RE = re.compile(r"[0-9a-f]{64}")
AUDIT_LOCK_FIELDS = {
    "schema_version", "lesson_id", "author_ids", "materials_lock",
    "standard_snapshot", "audit_report", "reviews", "frozen_artifacts_sha256",
    "status", "claim_boundary",
}
STANDARD_SNAPSHOT_FIELDS = {
    "version", "path", "sha256", "registry_sha256", "frozen_at", "enforcement_config",
}
BOUND_FILE_FIELDS = {"path", "sha256"}
AUDIT_REPORT_FIELDS = {
    "schema_version", "lesson_id", "materials_lock_sha256", "frozen_artifacts_sha256",
    "standard_version", "standard_registry_sha256", "enforcement_config_sha256",
    "machine_checks", "review_rounds", "findings", "p3_risks", "claim_boundary",
}
MACHINE_CHECK_FIELDS = {"name", "exit_code"}
REVIEW_ROUND_FIELDS = {"round_id", "frozen_artifacts_sha256", "open_severities"}
FINDING_FIELDS = {"defect_id", "severity", "status"}
P3_RISK_FIELDS = {"category", "statement", "verification_plan"}
REVIEW_ENTRY_FIELDS = {"role", "path", "sha256"}
AUDIT_REVIEW_FIELDS = {
    "schema_version", "lesson_id", "role", "reviewer_id", "review_event_id",
    "review_source", "verification_mode", "authentication_boundary", "author_ids",
    "decision", "reviewed_at", "materials_lock_sha256", "frozen_artifacts_sha256",
    "standard_version", "standard_registry_sha256", "enforcement_config_sha256",
    "defect_ids", "owner_approval_trace",
}
REVIEW_SOURCE_FIELDS = {"locator", "record_sha256"}
OWNER_APPROVAL_TRACE_FIELDS = {"checked", "event_id", "boundary"}
EXTERNAL_REGISTRY_FIELDS = {"schema_version", "standard_snapshot", "events"}
EXTERNAL_STANDARD_FIELDS = {"version", "registry_sha256", "enforcement_config_sha256"}
EXTERNAL_EVENT_FIELDS = {
    "verified_by_host", "role", "reviewer_id", "locator", "record_sha256", "decision",
    "materials_lock_sha256", "frozen_artifacts_sha256", "standard_registry_sha256",
    "enforcement_config_sha256",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _resolve_bound(root: Path, value: str, label: str, errors: list[str]) -> Path | None:
    raw = Path(value)
    if not value:
        errors.append(f"{label}缺path")
        return None
    if raw.is_absolute():
        errors.append(f"{label}必须使用项目根相对路径")
        return None
    path = (root / raw).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label}路径越出项目根: {value}")
        return None
    return path


def _bound_file(entry: dict, label: str, root: Path, errors: list[str]) -> Path | None:
    value = str(entry.get("path") or "").strip()
    expected = str(entry.get("sha256") or "").strip()
    path = _resolve_bound(root, value, label, errors)
    if len(expected) != 64:
        errors.append(f"{label}缺合法SHA-256")
        return path
    if path is None:
        return None
    if not path.is_file():
        errors.append(f"{label}文件不存在: {value}")
        return None
    if _sha256(path) != expected:
        errors.append(f"{label}哈希与当前文件不一致: {value}")
    return path


def _load_json(path: Path, label: str, errors: list[str]) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"{label}无法读取: {exc}")
        return None


def _timezone_ok(value: object) -> bool:
    text = str(value or "").strip()
    if not text:
        return False
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


def _reject_unknown_fields(
    value: object,
    allowed: set[str],
    label: str,
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label}必须为对象")
        return
    for field in sorted(set(value) - allowed):
        errors.append(f"{label}含未知字段: {field}")


def validate_audit_lock(
    lock: dict,
    root: Path = ROOT,
    external_review_registry: dict | None = None,
) -> list[str]:
    errors: list[str] = []
    if lock.get("schema_version") != "audit-lock.v1":
        errors.append("audit_lock schema_version必须为audit-lock.v1")
    lesson_id = str(lock.get("lesson_id") or "").strip()
    if not lesson_id:
        errors.append("audit_lock lesson_id为空")
    for unknown_field in sorted(set(lock) - AUDIT_LOCK_FIELDS):
        errors.append(f"audit_lock含未知字段: {unknown_field}")
    if lock.get("status") != "awaiting_host_release":
        errors.append("本地G4只能到awaiting_host_release，不得自行声明released")
    author_ids = {str(value).strip() for value in lock.get("author_ids") or [] if str(value).strip()}
    if not author_ids:
        errors.append("audit_lock author_ids为空")
    boundary = str(lock.get("claim_boundary") or "")
    if not has_pending_classroom_boundary(boundary):
        errors.append("audit_lock claim_boundary必须明确声明效果待真实课堂/试教验证")

    materials_entry = lock.get("materials_lock") or {}
    _reject_unknown_fields(materials_entry, BOUND_FILE_FIELDS, "materials_lock引用", errors)
    materials_path = _bound_file(materials_entry, "materials_lock", root, errors)
    expected_reviews_dir: Path | None = None
    if materials_path:
        if materials_path.parent.name != "_meta":
            errors.append("materials_lock必须位于同一课_meta目录")
        else:
            expected_reviews_dir = materials_path.parent / "reviews"
    standard_entry = lock.get("standard_snapshot") or {}
    _reject_unknown_fields(standard_entry, STANDARD_SNAPSHOT_FIELDS, "standard_snapshot", errors)
    frozen_config_entry = standard_entry.get("enforcement_config") or {}
    _reject_unknown_fields(
        frozen_config_entry,
        BOUND_FILE_FIELDS,
        "standard_snapshot.enforcement_config",
        errors,
    )
    frozen_config_path = _bound_file(
        frozen_config_entry,
        "standard_snapshot.enforcement_config",
        root,
        errors,
    )
    if expected_reviews_dir and frozen_config_path and frozen_config_path.parent != expected_reviews_dir:
        errors.append("standard_snapshot.enforcement_config必须位于同一课_meta/reviews")
    frozen_config: dict | None = None
    if frozen_config_path and frozen_config_path.is_file():
        frozen_config = _load_json(frozen_config_path, "冻结enforcement_config", errors)
        if frozen_config is not None:
            errors.extend(
                f"冻结原则配置无效: {error}"
                for error in check_config_drift(frozen_config)
            )
    frozen_artifacts_sha = str(lock.get("frozen_artifacts_sha256") or "")
    materials_lock: dict | None = None
    manifest: dict | None = None
    expected_content_authors: set[str] = set()
    upstream_owner_event_id = ""
    lesson_for_principles: dict | None = None
    if materials_path and materials_path.is_file():
        materials_lock = _load_json(materials_path, "G3 materials_lock", errors)
        if materials_lock is not None:
            errors.extend(
                f"G3上游无效: {error}"
                for error in validate_materials_lock(
                    materials_lock,
                    root=root,
                    enforcement_config=frozen_config,
                )
            )
            if materials_lock.get("lesson_id") != lesson_id:
                errors.append("audit_lock lesson_id与G3不一致")
            materials_author_id = str(materials_lock.get("author_id") or "").strip()
            if materials_author_id:
                expected_content_authors.add(materials_author_id)
            manifest_value = str((materials_lock.get("manifest") or {}).get("path") or "")
            manifest_path = _resolve_bound(root, manifest_value, "materials manifest", errors)
            if manifest_path and manifest_path.is_file():
                manifest = _load_json(manifest_path, "materials manifest", errors)
            design_value = str((materials_lock.get("design_lock") or {}).get("path") or "")
            design_path = _resolve_bound(root, design_value, "design_lock", errors)
            if design_path and design_path.is_file():
                design_lock = _load_json(design_path, "design_lock", errors)
                design_author_id = str((design_lock or {}).get("author_id") or "").strip()
                if design_author_id:
                    expected_content_authors.add(design_author_id)
                g1_value = str((design_lock or {}).get("lesson_plan_lock", {}).get("path") or "")
                g1_path = _resolve_bound(root, g1_value, "lesson_plan_lock", errors)
                if g1_path and g1_path.is_file():
                    g1_lock = _load_json(g1_path, "lesson_plan_lock", errors)
                    upstream_author_id = str((g1_lock or {}).get("author_id") or "").strip()
                    if upstream_author_id:
                        expected_content_authors.add(upstream_author_id)
                    approval_value = str((g1_lock or {}).get("owner_approval", {}).get("path") or "")
                    approval_path = _resolve_bound(root, approval_value, "owner_approval", errors)
                    if approval_path and approval_path.is_file():
                        approval = _load_json(approval_path, "owner_approval", errors)
                        upstream_owner_event_id = str((approval or {}).get("approval_event_id") or "").strip()
                lesson_value = str((design_lock or {}).get("lesson_data", {}).get("path") or "")
                lesson_path = _resolve_bound(root, lesson_value, "lesson_data", errors)
                if lesson_path and lesson_path.is_file():
                    lesson = _load_json(lesson_path, "lesson_data", errors)
                    if lesson is not None:
                        lesson_for_principles = lesson
    if expected_content_authors and author_ids != expected_content_authors:
        errors.append(
            "audit_lock author_ids必须精确覆盖S2/S3/S4内容作者: "
            f"期望{sorted(expected_content_authors)}，实际{sorted(author_ids)}"
        )
    if manifest is not None:
        actual_freeze = canonical_json_sha256(manifest.get("artifacts") or [])
        if frozen_artifacts_sha != actual_freeze:
            errors.append("冻结物料哈希与当前G3 manifest不一致")

    standard_path = _bound_file(standard_entry, "standard_snapshot", root, errors)
    if expected_reviews_dir and standard_path and standard_path.parent != expected_reviews_dir:
        errors.append("standard_snapshot必须位于同一课_meta/reviews")
    standard_version = str(standard_entry.get("version") or "").strip()
    if not standard_version:
        errors.append("standard_snapshot.version为空")
    registry_sha256 = str(standard_entry.get("registry_sha256") or "").strip()
    if not SHA256_RE.fullmatch(registry_sha256):
        errors.append("standard_snapshot.registry_sha256必须为合法SHA-256")
    if not _timezone_ok(standard_entry.get("frozen_at")):
        errors.append("standard_snapshot.frozen_at必须为带时区ISO 8601时间")
    if standard_path and standard_path.is_file():
        try:
            standard_text = standard_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"standard_snapshot无法读取: {exc}")
        else:
            if not standard_text.strip():
                errors.append("standard_snapshot为空")
            else:
                try:
                    frozen_registry = yaml.safe_load(standard_text)
                except yaml.YAMLError as exc:
                    errors.append(f"standard_snapshot结构无法解析: {exc}")
                    frozen_registry = None
                if not isinstance(frozen_registry, dict):
                    errors.append("standard_snapshot结构必须是完整原则注册库对象")
                else:
                    frozen_meta = frozen_registry.get("meta") or {}
                    if frozen_meta.get("standard_version") != standard_version:
                        errors.append("standard_snapshot内容未绑定声明的标准版本")
                    if set((frozen_registry.get("nodes") or {}).keys()) != NODE_IDS:
                        errors.append("standard_snapshot结构未完整冻结20个机制节点")
                    if not isinstance(frozen_registry.get("principles"), list) or not frozen_registry["principles"]:
                        errors.append("standard_snapshot结构未冻结原则清单")
                    try:
                        principle_errors, _ = validate_principle_registry(
                            frozen_registry,
                            check_external_references=False,
                        )
                    except (AttributeError, KeyError, TypeError, ValueError) as exc:
                        errors.append(f"冻结原则注册库无效: 结构触发{type(exc).__name__}")
                    else:
                        errors.extend(
                            f"冻结原则注册库无效: {error}"
                            for error in principle_errors
                        )
                if registry_sha256 and registry_sha256 != _sha256(standard_path):
                    errors.append("standard_snapshot.registry_sha256与冻结注册库文件不一致")
    if lesson_for_principles is not None:
        if frozen_config is None:
            errors.append("G4缺冻结enforcement_config，不能按冻结标准复验")
        else:
            principle_results = run_checks(lesson_for_principles, frozen_config, strict=True)
            for check_name, result in principle_results.items():
                if not result.get("ok"):
                    errors.append(f"G4原则检查未通过: {check_name}")

    report_path = _bound_file(lock.get("audit_report") or {}, "audit_report", root, errors)
    if expected_reviews_dir and report_path and report_path.parent != expected_reviews_dir:
        errors.append("audit_report必须位于同一课_meta/reviews")
    report = _load_json(report_path, "audit_report", errors) if report_path and report_path.is_file() else None
    if report is not None:
        _reject_unknown_fields(report, AUDIT_REPORT_FIELDS, "audit_report", errors)
        if report.get("schema_version") != "audit-report.v1":
            errors.append("audit_report schema_version错误")
        if report.get("lesson_id") != lesson_id:
            errors.append("audit_report lesson_id与锁不一致")
        if report.get("materials_lock_sha256") != materials_entry.get("sha256"):
            errors.append("audit_report未绑定当前materials_lock")
        if report.get("frozen_artifacts_sha256") != frozen_artifacts_sha:
            errors.append("audit_report未绑定当前冻结物料")
        if report.get("standard_version") != standard_version:
            errors.append("audit_report标准版本与冻结快照不一致")
        if report.get("standard_registry_sha256") != registry_sha256:
            errors.append("audit_report未绑定冻结原则注册库哈希")
        if report.get("enforcement_config_sha256") != frozen_config_entry.get("sha256"):
            errors.append("audit_report未绑定冻结执行配置哈希")
        p3_risks = report.get("p3_risks")
        if not isinstance(p3_risks, list) or not all(isinstance(item, dict) for item in p3_risks):
            errors.append("audit_report.p3_risks必须结构化覆盖Office真实渲染、课堂节奏、学习效果")
            p3_risks = []
        risk_categories = {str(item.get("category") or "").strip() for item in p3_risks}
        if risk_categories != P3_RISK_CATEGORIES:
            errors.append("audit_report.p3_risks必须完整覆盖Office真实渲染、课堂节奏、学习效果三类风险")
        for item in p3_risks:
            _reject_unknown_fields(item, P3_RISK_FIELDS, "audit_report.p3_risks条目", errors)
            category = str(item.get("category") or "?")
            statement = str(item.get("statement") or "").strip()
            verification_plan = str(item.get("verification_plan") or "").strip()
            if len(statement) < 12 or len(verification_plan) < 12:
                errors.append(f"audit_report.p3_risks[{category}]缺明确风险或验证计划")
        machine_checks = report.get("machine_checks") or []
        for index, item in enumerate(machine_checks):
            _reject_unknown_fields(item, MACHINE_CHECK_FIELDS, f"audit_report.machine_checks[{index}]", errors)
        check_names = {item.get("name") for item in machine_checks}
        for name in sorted(REQUIRED_MACHINE_CHECKS - check_names):
            errors.append(f"audit_report缺机器检查: {name}")
        for item in machine_checks:
            if item.get("exit_code") != 0:
                errors.append(f"audit_report机器检查未通过: {item.get('name')}")
        review_rounds = report.get("review_rounds") or []
        if len(review_rounds) < 2:
            errors.append("audit_report必须保存最终候选至少两轮非阻断复审")
        final_round_ids = [str(item.get("round_id") or "").strip() for item in review_rounds[-2:]]
        if len(final_round_ids) == 2 and (
            not all(final_round_ids) or len(set(final_round_ids)) != 2
        ):
            errors.append("最终两轮复审轮次ID必须不同且非空")
        for round_item in review_rounds[-2:]:
            _reject_unknown_fields(round_item, REVIEW_ROUND_FIELDS, "audit_report.review_rounds条目", errors)
            if round_item.get("frozen_artifacts_sha256") != frozen_artifacts_sha:
                errors.append(f"复审轮{round_item.get('round_id', '?')}未绑定当前冻结物料")
            severities = set(round_item.get("open_severities") or [])
            for severity in severities:
                if severity not in SEVERITIES:
                    errors.append(f"复审轮{round_item.get('round_id', '?')}严重度非法: {severity!r}")
            if severities - {"P3"}:
                errors.append(f"复审轮{round_item.get('round_id', '?')}仍含P0/P1/P2")
        for finding in report.get("findings") or []:
            _reject_unknown_fields(finding, FINDING_FIELDS, "audit_report.findings条目", errors)
            severity = finding.get("severity")
            if severity not in SEVERITIES:
                errors.append(f"audit_report缺陷{finding.get('defect_id', '?')}严重度非法: {severity!r}")
        open_blockers = [
            item.get("defect_id", "?")
            for item in report.get("findings") or []
            if item.get("severity") in {"P0", "P1", "P2"} and item.get("status") != "closed"
        ]
        if open_blockers:
            errors.append(f"audit_report仍有开放P0/P1/P2: {open_blockers}")
        report_boundary = str(report.get("claim_boundary") or "")
        if not has_pending_classroom_boundary(report_boundary):
            errors.append("audit_report必须明确声明效果待真实课堂/试教验证")

    roles: list[str] = []
    reviewers: list[str] = []
    review_event_ids: list[str] = []
    for index, entry in enumerate(lock.get("reviews") or []):
        _reject_unknown_fields(entry, REVIEW_ENTRY_FIELDS, f"review引用[{index}]", errors)
        role = str(entry.get("role") or "").strip()
        roles.append(role)
        review_path = _bound_file(entry, f"review[{index}]({role or '?'})", root, errors)
        if expected_reviews_dir and review_path and review_path.parent != expected_reviews_dir:
            errors.append(f"review[{index}]必须位于同一课_meta/reviews")
        review = _load_json(review_path, f"review[{index}]", errors) if review_path and review_path.is_file() else None
        if review is None:
            continue
        _reject_unknown_fields(review, AUDIT_REVIEW_FIELDS, f"review[{index}]", errors)
        if review.get("schema_version") != "audit-review.v1":
            errors.append(f"review[{index}] schema_version错误")
        if review.get("lesson_id") != lesson_id:
            errors.append(f"review[{index}] lesson_id与锁不一致")
        if review.get("role") != role or role not in REVIEW_ROLES:
            errors.append(f"review[{index}]角色非法或与登记不一致: {role}")
        reviewer_id = str(review.get("reviewer_id") or "").strip()
        reviewers.append(reviewer_id)
        if not reviewer_id:
            errors.append(f"review[{index}] reviewer_id为空")
        if reviewer_id in author_ids:
            errors.append(f"review[{index}]审查者不能是内容作者: {reviewer_id}")
        review_event_id = str(review.get("review_event_id") or "").strip()
        review_event_ids.append(review_event_id)
        if len(review_event_id) < 8:
            errors.append(f"review[{index}] review_event_id为空")
        review_source = review.get("review_source")
        if not isinstance(review_source, dict):
            errors.append(f"review[{index}] review_source必须为结构化外部事件引用")
            review_source = {}
        else:
            _reject_unknown_fields(
                review_source,
                REVIEW_SOURCE_FIELDS,
                f"review[{index}].review_source",
                errors,
            )
        source_locator = str(review_source.get("locator") or "").strip()
        source_record_sha = str(review_source.get("record_sha256") or "").strip()
        if "://" not in source_locator or len(source_locator) < 16:
            errors.append(f"review[{index}] review_source.locator不可追溯")
        if not SHA256_RE.fullmatch(source_record_sha):
            errors.append(f"review[{index}] review_source.record_sha256非法")
        registry_events = (
            external_review_registry.get("events") or {}
            if isinstance(external_review_registry, dict)
            and external_review_registry.get("schema_version") == "external-review-registry.v1"
            else {}
        )
        verified_event = registry_events.get(review_event_id)
        if not isinstance(verified_event, dict) or verified_event.get("verified_by_host") is not True:
            errors.append(f"review[{index}]缺宿主外部审查事件核验: {review_event_id or '?'}")
        else:
            expected_event = {
                "role": role,
                "reviewer_id": reviewer_id,
                "locator": source_locator,
                "record_sha256": source_record_sha,
                "decision": "pass",
                "materials_lock_sha256": materials_entry.get("sha256"),
                "frozen_artifacts_sha256": frozen_artifacts_sha,
                "standard_registry_sha256": registry_sha256,
                "enforcement_config_sha256": frozen_config_entry.get("sha256"),
            }
            for field, expected_value in expected_event.items():
                if verified_event.get(field) != expected_value:
                    errors.append(f"review[{index}]宿主核验事件字段不匹配: {field}")
        if review.get("verification_mode") != "external_review_gate":
            errors.append(f"review[{index}] verification_mode必须为external_review_gate")
        authentication_boundary = str(review.get("authentication_boundary") or "")
        if not (
            "不认证" in authentication_boundary
            and "人工核验" in authentication_boundary
        ):
            errors.append(f"review[{index}] authentication_boundary未声明本地不认证与外部人工核验")
        review_authors = {str(value).strip() for value in review.get("author_ids") or [] if str(value).strip()}
        if review_authors != author_ids:
            errors.append(f"review[{index}] author_ids与锁不一致")
        if review.get("decision") != "pass":
            errors.append(f"review[{index}]未通过")
        if not _timezone_ok(review.get("reviewed_at")):
            errors.append(f"review[{index}] reviewed_at必须为带时区ISO 8601时间")
        if review.get("materials_lock_sha256") != materials_entry.get("sha256"):
            errors.append(f"review[{index}]未绑定当前materials_lock")
        if review.get("frozen_artifacts_sha256") != frozen_artifacts_sha:
            errors.append(f"review[{index}]未绑定当前冻结物料")
        if review.get("standard_version") != standard_version:
            errors.append(f"review[{index}]标准版本漂移")
        if review.get("standard_registry_sha256") != registry_sha256:
            errors.append(f"review[{index}]未绑定冻结原则注册库哈希")
        if review.get("enforcement_config_sha256") != frozen_config_entry.get("sha256"):
            errors.append(f"review[{index}]未绑定冻结执行配置哈希")
        if review.get("defect_ids"):
            errors.append(f"review[{index}] pass回执仍含未清缺陷")
        trace = review.get("owner_approval_trace") or {}
        _reject_unknown_fields(
            trace,
            OWNER_APPROVAL_TRACE_FIELDS,
            f"review[{index}].owner_approval_trace",
            errors,
        )
        if trace.get("checked") is not True or not str(trace.get("event_id") or "").strip():
            errors.append(f"review[{index}]未复核外部所有者批准引用")
        elif upstream_owner_event_id and trace.get("event_id") != upstream_owner_event_id:
            errors.append(f"review[{index}]所有者批准事件引用与G1不一致")
        trace_boundary = str(trace.get("boundary") or "")
        if "不认证" not in trace_boundary or "人工" not in trace_boundary:
            errors.append(f"review[{index}]未声明本地身份认证边界")

    for duplicate in sorted({role for role in roles if roles.count(role) > 1}):
        errors.append(f"审查角色重复: {duplicate}")
    for role in sorted(REVIEW_ROLES - set(roles)):
        errors.append(f"G4缺少独立审查角色: {role}")
    nonempty_reviewers = [value for value in reviewers if value]
    if len(nonempty_reviewers) != len(set(nonempty_reviewers)):
        errors.append("视觉与学生接收审查必须由不同审查者完成")
    nonempty_events = [value for value in review_event_ids if value]
    if len(nonempty_events) != len(set(nonempty_events)):
        errors.append("视觉与学生接收审查必须绑定不同review_event_id")
    if isinstance(external_review_registry, dict):
        _reject_unknown_fields(
            external_review_registry,
            EXTERNAL_REGISTRY_FIELDS,
            "宿主外部审查事件注册表",
            errors,
        )
        host_standard = external_review_registry.get("standard_snapshot") or {}
        _reject_unknown_fields(
            host_standard,
            EXTERNAL_STANDARD_FIELDS,
            "宿主登记的冻结标准",
            errors,
        )
        expected_host_standard = {
            "version": standard_version,
            "registry_sha256": registry_sha256,
            "enforcement_config_sha256": frozen_config_entry.get("sha256"),
        }
        if host_standard != expected_host_standard:
            errors.append("宿主登记的冻结标准哈希不匹配")
        for event_id, event in (external_review_registry.get("events") or {}).items():
            _reject_unknown_fields(
                event,
                EXTERNAL_EVENT_FIELDS,
                f"宿主核验事件[{event_id}]",
                errors,
            )
    return sorted(set(errors))


def load_external_review_registry(path: Path, root: Path = ROOT) -> tuple[dict | None, list[str]]:
    """Load a host-supplied registry; project-contained self-attestations fail closed."""
    errors: list[str] = []
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        pass
    else:
        return None, ["外部审查事件注册表必须位于项目目录之外，由宿主提供"]
    try:
        registry = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return None, [f"外部审查事件注册表无法读取: {exc}"]
    if registry.get("schema_version") != "external-review-registry.v1":
        errors.append("外部审查事件注册表schema_version错误")
    _reject_unknown_fields(registry, EXTERNAL_REGISTRY_FIELDS, "外部审查事件注册表", errors)
    if not isinstance(registry.get("events"), dict):
        errors.append("外部审查事件注册表events必须为对象")
    return registry, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lock", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument(
        "--external-event-registry",
        type=Path,
        default=os.environ.get("YUWEN_EXTERNAL_REVIEW_REGISTRY"),
        help="宿主提供、且位于项目目录外的外部审查事件注册表",
    )
    args = parser.parse_args()
    try:
        lock = json.loads(args.lock.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    registry, registry_errors = (
        load_external_review_registry(args.external_event_registry, root=args.root)
        if args.external_event_registry
        else (None, ["缺宿主外部审查事件注册表；G4默认失败关闭"])
    )
    errors = registry_errors + validate_audit_lock(
        lock,
        root=args.root,
        external_review_registry=registry,
    )
    for error in errors:
        print(f"[error] {error}")
    if errors:
        print(f"G4终审锁失败：{len(errors)}项")
        return 1
    print("G4本地终审候选通过：G0—G3有效 / 双审材料齐全 / 冻结物料一致；待宿主外部放行，不得声明released")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
