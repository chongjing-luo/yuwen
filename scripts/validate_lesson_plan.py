#!/usr/bin/env python3
"""Validate a G1 lesson-plan candidate or approved lock.

This validator checks deterministic structure, lineage, and coverage.  The
owner review remains responsible for literary quality and curricular judgment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zlib
from collections import Counter
from datetime import datetime
from pathlib import Path

from lesson_identity import LESSON_ID_PATTERN, check_lesson_id_registry
from validate_lesson_evidence import has_pending_classroom_boundary
from validate_lesson_evidence import validate as validate_lesson_evidence

ROOT = Path(__file__).resolve().parents[1]
NODE_IDS = {f"K{i}" for i in range(1, 6)} | {f"U{i}" for i in range(1, 9)} | {f"J{i}" for i in range(1, 8)}
KNOWLEDGE_STATUSES = {"must_teach", "retrieve_prior", "teacher_reserve", "defer"}
LOGIC_COMPONENTS = {
    "entry",
    "context",
    "text_development",
    "knowledge_formation",
    "student_experience",
    "discussion",
    "synthesis_retrieval",
    "assessment_evidence",
    "transfer",
    "exam_link",
    "contemporary_link",
}
CORE_LOGIC_NODES = {"K1", "K2", "U8", "J4"}
KP_ID_PATTERN = re.compile(r"KP-CARD-[A-Z0-9-]+-\d{3}")
LESSON_PLAN_LOCK_FIELDS = {
    "schema_version", "lesson_id", "author_id", "lesson_plan",
    "evidence_manifest", "owner_approval", "contract", "status",
}
LESSON_PLAN_CANDIDATE_FIELDS = {
    "schema_version", "lesson_id", "author_id", "lesson_plan",
    "evidence_manifest", "contract", "status",
}
BOUND_FILE_FIELDS = {"path", "sha256"}
CONTRACT_FIELDS = {
    "mechanism_nodes", "total_minutes", "closing_mode", "objective_framework", "objectives",
    "knowledge_items", "knowledge_clusters", "work_interpretation", "questions",
    "overall_teaching_logic", "stages", "claim_boundary",
}
OBJECTIVE_FIELDS = {
    "id", "kind", "dimensions", "statement", "kid_refs", "mechanism_nodes",
    "minimum_evidence", "high_quality_evidence", "failure_signal", "recurrence",
}
OBJECTIVE_FRAMEWORK_FIELDS = {"status", "reason", "objective_refs"}
OBJECTIVE_DIMENSIONS = {
    "language_use": "语言建构与运用",
    "thinking": "思维发展与提升",
    "aesthetic": "审美鉴赏与创造",
    "culture": "文化传承与理解",
    "moral_education": "立德树人与价值形成",
    "reality_transfer": "现实迁移与实践",
}
MANDATORY_OBJECTIVE_DIMENSIONS = {"language_use", "moral_education", "reality_transfer"}
KNOWLEDGE_FIELDS = {
    "kid", "statement", "status", "source_ref", "kp_ids", "stage_refs",
    "mastery_evidence", "mechanism_nodes", "defer_reason",
}
KNOWLEDGE_CLUSTER_FIELDS = {"id", "name", "organizing_basis", "rationale", "kid_refs"}
WORK_INTERPRETATION_ROLES = {
    "central_meaning": "作品主旨或核心观点",
    "expressive_intent": "作者、叙述者或抒情主体的表达意图/作品表达指向",
    "emotional_organization": "情感基调、情感变化或态度语调组织",
}
WORK_INTERPRETATION_FIELDS = {
    "status", "kid_refs", "evidence_boundary", "not_applicable_reason",
}
QUESTION_FIELDS = {
    "id", "text", "rationale", "objective_refs", "kid_refs", "stage_refs",
    "recovery_stage_refs", "mechanism_nodes",
}
OVERALL_LOGIC_FIELDS = {"text", "stage_refs", "mechanism_nodes", "components"}
LOGIC_COMPONENT_FIELDS = {"status", "reason", "stage_refs"}
STAGE_FIELDS = {
    "id", "name", "entry_reason", "text_scope", "objective_refs", "kid_refs",
    "initial_method", "student_change", "student_experience", "teacher_role", "evidence",
    "transition_reason",
}
OWNER_APPROVAL_FIELDS = {
    "schema_version", "lesson_id", "reviewer_id", "author_id", "decision", "reviewed_at",
    "approval_event_id", "approval_source", "verification_mode", "authentication_boundary",
    "lesson_plan_path", "lesson_plan_sha256", "approval_statement",
    "lesson_plan_contract_sha256", "evidence_manifest_sha256", "standard_version",
    "resolved_issues",
}
OWNER_APPROVAL_STRING_FIELDS = OWNER_APPROVAL_FIELDS - {"resolved_issues"}


def _reject_unknown_fields(value: object, allowed: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label}必须为对象")
        return
    for field in sorted(set(value) - allowed):
        errors.append(f"{label}含未知字段: {field}")


def canonical_json_sha256(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_bound_file(entry: object, label: str, root: Path, errors: list[str]) -> Path | None:
    if not isinstance(entry, dict):
        return None
    path_value = str(entry.get("path") or "").strip()
    expected = str(entry.get("sha256") or "").strip()
    if not path_value:
        errors.append(f"{label}缺path")
        return None
    if len(expected) != 64:
        errors.append(f"{label}缺合法SHA-256")
        return None
    raw_path = Path(path_value)
    if raw_path.is_absolute():
        errors.append(f"{label}必须使用项目根相对路径")
        return None
    path = _resolve(root, path_value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label}路径越出项目根: {path_value}")
        return None
    if not path.is_file():
        errors.append(f"{label}文件不存在: {path_value}")
        return None
    if _sha256(path) != expected:
        errors.append(f"{label}哈希与当前文件不一致: {path_value}")
    return path


def _check_nodes(nodes: list, label: str, errors: list[str]) -> None:
    if not nodes:
        errors.append(f"{label}未绑定机制节点")
    for node in nodes:
        if node not in NODE_IDS:
            errors.append(f"{label}含非法机制节点: {node}")


def _duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    return {value for value in values if value in seen or seen.add(value)}


def _validate_document(
    lock: dict,
    root: Path,
    *,
    candidate: bool,
    verify_receipt: bool,
    candidate_path: Path | None = None,
    lock_path: Path | None = None,
) -> tuple[list[str], dict]:
    errors: list[str] = []
    contract = lock.get("contract") or {}
    objectives = contract.get("objectives") or []
    knowledge = contract.get("knowledge_items") or []
    stages = contract.get("stages") or []
    stats = {"objectives": len(objectives), "knowledge_items": len(knowledge), "stages": len(stages)}

    if candidate:
        if lock.get("schema_version") != "lesson-plan-candidate.v1":
            errors.append("schema_version必须为lesson-plan-candidate.v1")
        for unknown_field in sorted(set(lock) - LESSON_PLAN_CANDIDATE_FIELDS):
            errors.append(f"lesson_plan_candidate含未知字段: {unknown_field}")
        if lock.get("status") != "candidate_owner_review":
            errors.append("lesson_plan_candidate状态必须为candidate_owner_review")
    else:
        if lock.get("schema_version") != "lesson-plan-lock.v1":
            errors.append("schema_version必须为lesson-plan-lock.v1")
        for unknown_field in sorted(set(lock) - LESSON_PLAN_LOCK_FIELDS):
            errors.append(f"lesson_plan_lock含未知字段: {unknown_field}")
        if lock.get("status") != "approved":
            errors.append("lesson_plan_lock状态不是approved")
    lesson_id_value = lock.get("lesson_id")
    lesson_id = lesson_id_value.strip() if isinstance(lesson_id_value, str) else ""
    if not lesson_id:
        errors.append("lesson_id必须为非空字符串")
    elif not LESSON_ID_PATTERN.fullmatch(lesson_id):
        errors.append("lesson_id格式非法；正式课须使用LES-{册代码}-{课文代码}-{两位序号}")
    author_value = lock.get("author_id")
    author_id = author_value.strip() if isinstance(author_value, str) else ""
    if not author_id:
        errors.append("author_id必须为非空字符串")
    elif author_value != author_id:
        errors.append("author_id不得含首尾空白")

    plan_entry = lock.get("lesson_plan") or {}
    evidence_entry = lock.get("evidence_manifest") or {}
    approval_entry = {} if candidate else lock.get("owner_approval") or {}
    _reject_unknown_fields(plan_entry, BOUND_FILE_FIELDS, "lesson_plan引用", errors)
    _reject_unknown_fields(evidence_entry, BOUND_FILE_FIELDS, "evidence_manifest引用", errors)
    if not candidate:
        _reject_unknown_fields(approval_entry, BOUND_FILE_FIELDS, "owner_approval引用", errors)
    _reject_unknown_fields(contract, CONTRACT_FIELDS, "contract", errors)
    objective_framework_for_fields = contract.get("objective_framework") or {}
    if isinstance(objective_framework_for_fields, dict):
        for dimension_id, decision in objective_framework_for_fields.items():
            _reject_unknown_fields(
                decision,
                OBJECTIVE_FRAMEWORK_FIELDS,
                f"objective_framework.{dimension_id}",
                errors,
            )
    for index, objective in enumerate(objectives):
        _reject_unknown_fields(objective, OBJECTIVE_FIELDS, f"objectives[{index}]", errors)
    for index, item in enumerate(knowledge):
        _reject_unknown_fields(item, KNOWLEDGE_FIELDS, f"knowledge_items[{index}]", errors)
    for index, cluster in enumerate(contract.get("knowledge_clusters") or []):
        _reject_unknown_fields(
            cluster,
            KNOWLEDGE_CLUSTER_FIELDS,
            f"knowledge_clusters[{index}]",
            errors,
        )
    work_interpretation_for_fields = contract.get("work_interpretation") or {}
    if isinstance(work_interpretation_for_fields, dict):
        for role_id, decision in work_interpretation_for_fields.items():
            if isinstance(decision, dict):
                _reject_unknown_fields(
                    decision,
                    WORK_INTERPRETATION_FIELDS,
                    f"work_interpretation.{role_id}",
                    errors,
                )
    for index, question in enumerate(contract.get("questions") or []):
        _reject_unknown_fields(question, QUESTION_FIELDS, f"questions[{index}]", errors)
    logic_for_fields = contract.get("overall_teaching_logic") or {}
    _reject_unknown_fields(logic_for_fields, OVERALL_LOGIC_FIELDS, "overall_teaching_logic", errors)
    for component_id, decision in (logic_for_fields.get("components") or {}).items():
        _reject_unknown_fields(
            decision,
            LOGIC_COMPONENT_FIELDS,
            f"overall_teaching_logic.components.{component_id}",
            errors,
        )
    for index, stage in enumerate(stages):
        _reject_unknown_fields(stage, STAGE_FIELDS, f"stages[{index}]", errors)
    plan_path = _check_bound_file(plan_entry, "lesson_plan", root, errors)
    evidence_path = _check_bound_file(evidence_entry, "evidence_manifest", root, errors)
    approval_path = None if candidate else _check_bound_file(approval_entry, "owner_approval", root, errors)
    if plan_path and plan_path.is_file():
        try:
            plan_path.relative_to((root / "work/teaching").resolve())
        except ValueError:
            errors.append("lesson_plan必须位于work/teaching正式课程树")
        expected_meta = plan_path.parent / "_meta"
        if evidence_path and evidence_path.parent != expected_meta:
            errors.append("evidence_manifest必须位于同一课目录的_meta")
        if approval_path and approval_path.parent != expected_meta:
            errors.append("owner_approval必须位于同一课目录的_meta")
        try:
            plan_text = plan_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"lesson_plan不是可读UTF-8 Markdown: {exc}")
        else:
            normalized = "".join(character for character in plan_text if not character.isspace())
            headings = [line for line in plan_text.splitlines() if line.lstrip().startswith("#")]
            if len(normalized) < 300 or len(headings) < 4:
                errors.append("lesson_plan最低有效内容不足（至少300个非空白字符与4个标题）")
            else:
                folded = normalized.casefold()
                encoded = folded.encode("utf-8")
                unique_characters = len(set(folded))
                dominant_share = Counter(folded).most_common(1)[0][1] / len(folded)
                compression_ratio = len(zlib.compress(encoded, level=9)) / len(encoded)
                if (
                    unique_characters < 30
                    or dominant_share > 0.4
                    or (len(folded) >= 1000 and compression_ratio < 0.08)
                ):
                    errors.append("lesson_plan低熵，疑似重复字符占位")
        if candidate and candidate_path is not None:
            resolved_candidate_path = (
                candidate_path if candidate_path.is_absolute() else root / candidate_path
            ).resolve()
            expected_candidate_path = expected_meta / "lesson_plan_candidate.json"
            if resolved_candidate_path != expected_candidate_path:
                errors.append("lesson_plan_candidate必须位于同一课目录的_meta并使用规定文件名")
        if not candidate:
            expected_lock_path = expected_meta / "lesson_plan_lock.json"
            if lock_path is not None:
                resolved_lock_path = (
                    lock_path if lock_path.is_absolute() else root / lock_path
                ).resolve()
                if resolved_lock_path != expected_lock_path:
                    errors.append("lesson_plan_lock必须位于同一课目录的_meta并使用规定文件名")
            expected_candidate_path = expected_meta / "lesson_plan_candidate.json"
            if not expected_candidate_path.is_file():
                errors.append("缺少同课lesson_plan_candidate.json，不能证明正式锁来自已预检候选")
            else:
                try:
                    submitted_candidate = json.loads(
                        expected_candidate_path.read_text(encoding="utf-8")
                    )
                except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                    errors.append(f"同课lesson_plan_candidate无法读取: {exc}")
                else:
                    candidate_errors, _ = validate_candidate(
                        submitted_candidate,
                        root=root,
                        candidate_path=expected_candidate_path,
                    )
                    errors.extend(
                        f"同课lesson_plan_candidate无效: {error}"
                        for error in candidate_errors
                    )
                    for field in (
                        "lesson_id",
                        "author_id",
                        "lesson_plan",
                        "evidence_manifest",
                        "contract",
                    ):
                        if submitted_candidate.get(field) != lock.get(field):
                            errors.append(f"正式锁与已预检候选不一致: {field}")
    check_lesson_id_registry(
        lesson_id,
        plan_path.parent if plan_path is not None else None,
        root,
        errors,
    )

    # G1 cannot turn an invalid G0 manifest into an approved lesson plan merely
    # by copying its current hash.  Re-run the upstream gate on the bound file.
    evidence_kp_ids: set[str] = set()
    evidence_kp_ids_by_source: dict[str, set[str]] = {}
    evidence_knowledge_source_ids: set[str] = set()
    if evidence_path and evidence_path.is_file():
        try:
            evidence_manifest = json.loads(evidence_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"G0上游无效: evidence_manifest无法读取: {exc}")
        else:
            upstream_errors, _ = validate_lesson_evidence(
                evidence_manifest,
                root=root,
                manifest_path=evidence_path,
            )
            errors.extend(f"G0上游无效: {error}" for error in upstream_errors)
            if evidence_manifest.get("lesson_id") != lesson_id:
                errors.append("G0上游无效: evidence_manifest lesson_id与G1不一致")
            for source in evidence_manifest.get("knowledge_sources") or []:
                source_id = str(source.get("source_id") or "").strip()
                if source_id:
                    evidence_knowledge_source_ids.add(source_id)
                    evidence_kp_ids_by_source.setdefault(source_id, set())
                source_value = str(source.get("path") or "").strip()
                source_path = _resolve(root, source_value).resolve() if source_value else None
                if source_path and source_path.is_file():
                    try:
                        source_kps = set(KP_ID_PATTERN.findall(source_path.read_text(encoding="utf-8")))
                        evidence_kp_ids |= source_kps
                        if source_id:
                            evidence_kp_ids_by_source[source_id] |= source_kps
                    except (OSError, UnicodeError):
                        pass

    _check_nodes(contract.get("mechanism_nodes") or [], "contract", errors)
    objective_ids = [str(item.get("id") or "") for item in objectives]
    knowledge_ids = [str(item.get("kid") or "") for item in knowledge]
    stage_ids = [str(item.get("id") or "") for item in stages]
    for label, ids in (("目标", objective_ids), ("KID", knowledge_ids), ("阶段", stage_ids)):
        if not ids or any(not value for value in ids):
            errors.append(f"{label}ID为空或清单为空")
        for duplicate in sorted(_duplicates(ids)):
            errors.append(f"{label}ID重复: {duplicate}")
    objective_set, knowledge_set, stage_set = set(objective_ids), set(knowledge_ids), set(stage_ids)
    knowledge_status_by_id = {
        str(item.get("kid") or ""): item.get("status")
        for item in knowledge
    }

    knowledge_clusters = contract.get("knowledge_clusters")
    if not isinstance(knowledge_clusters, list) or not knowledge_clusters:
        errors.append("知识簇knowledge_clusters必须为非空数组")
        knowledge_clusters = []
    cluster_ids: list[str] = []
    clustered_kids: list[str] = []
    for index, cluster in enumerate(knowledge_clusters):
        if not isinstance(cluster, dict):
            errors.append(f"知识簇[{index}]必须为对象")
            continue
        cluster_id = str(cluster.get("id") or "").strip()
        cluster_ids.append(cluster_id)
        label = cluster_id or f"[{index}]"
        if not cluster_id:
            errors.append(f"知识簇{label}的ID为空")
        for field, field_label in (
            ("name", "名称"),
            ("organizing_basis", "组织依据"),
            ("rationale", "聚合理由"),
        ):
            if not str(cluster.get(field) or "").strip():
                errors.append(f"知识簇{label}缺{field_label}")
        kid_refs = cluster.get("kid_refs")
        if not (
            isinstance(kid_refs, list)
            and kid_refs
            and all(isinstance(kid, str) and kid.strip() for kid in kid_refs)
        ):
            errors.append(f"知识簇{label}必须引用至少一个有效KID")
            kid_refs = []
        if len(kid_refs) != len(set(kid_refs)):
            errors.append(f"知识簇{label}内部KID重复")
        for kid in kid_refs:
            clustered_kids.append(kid)
            if kid not in knowledge_set:
                errors.append(f"知识簇{label}引用不存在的KID: {kid}")
    for duplicate in sorted(_duplicates(cluster_ids)):
        if duplicate:
            errors.append(f"知识簇ID重复: {duplicate}")
    cluster_membership = Counter(clustered_kids)
    for kid in sorted(knowledge_set - set(clustered_kids)):
        errors.append(f"知识全账KID未归入知识簇: {kid}")
    for kid, count in sorted(cluster_membership.items()):
        if kid in knowledge_set and count > 1:
            errors.append(f"知识全账KID重复归入多个知识簇: {kid}")

    work_interpretation = contract.get("work_interpretation")
    if not isinstance(work_interpretation, dict):
        errors.append("作品整体解释work_interpretation必须为对象")
        work_interpretation = {}
    missing_roles = set(WORK_INTERPRETATION_ROLES) - set(work_interpretation)
    extra_roles = set(work_interpretation) - set(WORK_INTERPRETATION_ROLES)
    for role_id in sorted(missing_roles):
        errors.append(f"作品整体解释缺少裁决: {WORK_INTERPRETATION_ROLES[role_id]}")
    for role_id in sorted(extra_roles):
        errors.append(f"作品整体解释含未知裁决: {role_id}")
    for role_id, decision in work_interpretation.items():
        if role_id not in WORK_INTERPRETATION_ROLES or not isinstance(decision, dict):
            continue
        label = WORK_INTERPRETATION_ROLES[role_id]
        status = decision.get("status")
        kid_refs = decision.get("kid_refs")
        if not isinstance(kid_refs, list) or any(
            not isinstance(kid, str) or not kid.strip() for kid in kid_refs
        ):
            errors.append(f"作品整体解释“{label}”的kid_refs必须为字符串数组")
            kid_refs = []
        if len(kid_refs) != len(set(kid_refs)):
            errors.append(f"作品整体解释“{label}”的kid_refs重复")
        if status == "included":
            if not str(decision.get("evidence_boundary") or "").strip():
                errors.append(f"作品整体解释“{label}”已纳入但缺证据边界")
            if not kid_refs:
                errors.append(f"作品整体解释“{label}”已纳入但没有知识全账KID")
            if str(decision.get("not_applicable_reason") or "").strip():
                errors.append(f"作品整体解释“{label}”已纳入却填写不适用理由")
            for kid in kid_refs:
                if kid not in knowledge_set:
                    errors.append(f"作品整体解释“{label}”引用不存在的KID: {kid}")
                elif knowledge_status_by_id.get(kid) not in {"must_teach", "retrieve_prior"}:
                    errors.append(
                        f"作品整体解释“{label}”引用非课堂范围KID {kid}: "
                        f"{knowledge_status_by_id.get(kid)}"
                    )
        elif status == "not_applicable":
            if not str(decision.get("not_applicable_reason") or "").strip():
                errors.append(f"作品整体解释“{label}”判为不适用但没有文体理由")
            if kid_refs:
                errors.append(f"作品整体解释“{label}”判为不适用却仍引用KID")
        else:
            errors.append(f"作品整体解释“{label}”的status非法")

    total_minutes = contract.get("total_minutes")
    if not isinstance(total_minutes, (int, float)) or isinstance(total_minutes, bool) or total_minutes <= 0:
        errors.append("contract.total_minutes必须为正数")
    if not str(contract.get("closing_mode") or "").strip():
        errors.append("contract.closing_mode为空")

    objective_framework = contract.get("objective_framework")
    if not isinstance(objective_framework, dict):
        errors.append("目标六向审计objective_framework必须为对象")
        objective_framework = {}
    missing_dimensions = set(OBJECTIVE_DIMENSIONS) - set(objective_framework)
    extra_dimensions = set(objective_framework) - set(OBJECTIVE_DIMENSIONS)
    for dimension_id in sorted(missing_dimensions):
        errors.append(f"目标六向审计缺少方向: {OBJECTIVE_DIMENSIONS[dimension_id]}")
    for dimension_id in sorted(extra_dimensions):
        errors.append(f"目标六向审计含未知方向: {dimension_id}")

    framework_refs_by_dimension: dict[str, set[str]] = {}
    for dimension_id, decision in objective_framework.items():
        if dimension_id not in OBJECTIVE_DIMENSIONS or not isinstance(decision, dict):
            continue
        label = OBJECTIVE_DIMENSIONS[dimension_id]
        status = decision.get("status")
        if status not in {"included", "not_primary"}:
            errors.append(f"目标六向审计{label}的status非法")
        if not str(decision.get("reason") or "").strip():
            errors.append(f"目标六向审计{label}缺取舍理由")
        refs = decision.get("objective_refs")
        if not isinstance(refs, list) or any(
            not isinstance(ref, str) or not ref.strip() for ref in refs
        ):
            errors.append(f"目标六向审计{label}的objective_refs必须为字符串数组")
            refs = []
        if len(refs) != len(set(refs)):
            errors.append(f"目标六向审计{label}的objective_refs重复")
        framework_refs_by_dimension[dimension_id] = set(refs)
        if status == "included" and not refs:
            errors.append(f"目标六向审计{label}已纳入但没有目标落点")
        if status == "not_primary" and refs:
            errors.append(f"目标六向审计{label}不单列却仍引用目标")
        if dimension_id in MANDATORY_OBJECTIVE_DIMENSIONS and status != "included":
            errors.append(f"{label}必须纳入目标，不得判为不单列")
        for oid in refs:
            if oid not in objective_set:
                errors.append(f"目标六向审计{label}引用不存在的目标: {oid}")

    objective_dimensions_by_id: dict[str, set[str]] = {}
    for objective in objectives:
        oid = objective.get("id", "?")
        if objective.get("kind") not in {"literacy", "reality_transfer"}:
            errors.append(f"目标{oid}的kind非法")
        dimensions = objective.get("dimensions")
        if not (
            isinstance(dimensions, list)
            and dimensions
            and all(isinstance(dimension, str) and dimension.strip() for dimension in dimensions)
        ):
            errors.append(f"目标{oid}必须标注至少一个六向目标维度")
            dimensions = []
        if len(dimensions) != len(set(dimensions)):
            errors.append(f"目标{oid}的dimensions重复")
        objective_dimensions_by_id[str(oid)] = set(dimensions)
        for dimension_id in dimensions:
            if dimension_id not in OBJECTIVE_DIMENSIONS:
                errors.append(f"目标{oid}含非法目标维度: {dimension_id}")
        if len(str(objective.get("statement") or "").strip()) < 20:
            errors.append(f"目标{oid}陈述过短或为空")
        _check_nodes(objective.get("mechanism_nodes") or [], f"目标{oid}", errors)
        for field in ("minimum_evidence", "high_quality_evidence", "failure_signal", "recurrence"):
            if not str(objective.get(field) or "").strip():
                errors.append(f"目标{oid}缺{field}")
        objective_kid_refs = objective.get("kid_refs")
        if not (
            isinstance(objective_kid_refs, list)
            and objective_kid_refs
            and all(isinstance(kid, str) and kid.strip() for kid in objective_kid_refs)
        ):
            errors.append(f"目标{oid}必须绑定至少一个有效KID")
            objective_kid_refs = []
        for kid in objective_kid_refs:
            if kid not in knowledge_set:
                errors.append(f"目标{oid}引用不存在的KID: {kid}")
            elif knowledge_status_by_id.get(kid) not in {"must_teach", "retrieve_prior"}:
                errors.append(
                    f"目标{oid}绑定非课堂范围KID {kid}: {knowledge_status_by_id.get(kid)}"
                )

    for dimension_id, refs in framework_refs_by_dimension.items():
        if dimension_id not in OBJECTIVE_DIMENSIONS:
            continue
        label = OBJECTIVE_DIMENSIONS[dimension_id]
        for oid in refs:
            if oid in objective_set and dimension_id not in objective_dimensions_by_id.get(oid, set()):
                errors.append(f"目标六向审计{label}引用目标{oid}，但该目标未标此维度")
    for oid, dimensions in objective_dimensions_by_id.items():
        for dimension_id in dimensions:
            if dimension_id in OBJECTIVE_DIMENSIONS and oid not in framework_refs_by_dimension.get(
                dimension_id, set()
            ):
                errors.append(
                    f"目标{oid}标注{OBJECTIVE_DIMENSIONS[dimension_id]}，但六向审计未引用该目标"
                )

    teachable_kids: set[str] = set()
    for item in knowledge:
        kid = item.get("kid", "?")
        status = item.get("status")
        if status not in KNOWLEDGE_STATUSES:
            errors.append(f"KID {kid}的status非法: {status}")
        if not str(item.get("statement") or "").strip():
            errors.append(f"KID {kid}缺准确陈述")
        if not str(item.get("source_ref") or "").strip():
            errors.append(f"KID {kid}缺source_ref")
        _check_nodes(item.get("mechanism_nodes") or [], f"KID {kid}", errors)
        refs = item.get("stage_refs") or []
        for stage_id in refs:
            if stage_id not in stage_set:
                errors.append(f"KID {kid}引用不存在的阶段: {stage_id}")
        if status in {"must_teach", "retrieve_prior"}:
            teachable_kids.add(kid)
            if not refs:
                errors.append(f"必教/旧知KID没有阶段落点: {kid}")
            if not str(item.get("mastery_evidence") or "").strip():
                errors.append(f"必教/旧知KID缺掌握证据: {kid}")
            kp_ids = item.get("kp_ids")
            if not (
                isinstance(kp_ids, list)
                and kp_ids
                and all(isinstance(kp, str) and kp.strip() for kp in kp_ids)
            ):
                errors.append(f"必教/旧知KID缺kp_ids机器映射: {kid}")
                kp_ids = []
            for kp_id in kp_ids:
                if kp_id not in evidence_kp_ids:
                    errors.append(f"KID {kid}的{kp_id}未解析到G0知识源")
            source_id = str(item.get("source_ref") or "").split("#", 1)[0]
            if source_id not in evidence_knowledge_source_ids:
                errors.append(f"KID {kid}的source_ref未指向G0知识源: {source_id}")
            else:
                source_kps = evidence_kp_ids_by_source.get(source_id, set())
                for kp_id in kp_ids:
                    if kp_id not in source_kps:
                        errors.append(f"KID {kid}的{kp_id}不属于source_ref指定知识源: {source_id}")
                source_ref = str(item.get("source_ref") or "")
                fragment = source_ref.split("#", 1)[1].strip() if "#" in source_ref else ""
                if fragment.startswith("KP-") and fragment not in kp_ids:
                    errors.append(f"KID {kid}的source_ref片段未绑定本KID kp_ids: {fragment}")
        elif refs:
            errors.append(f"KID {kid}为{status}却进入课堂阶段")
        if status == "defer" and not str(item.get("defer_reason") or "").strip():
            errors.append(f"KID {kid}的defer缺理由")

    covered_objectives: set[str] = set()
    covered_kids: set[str] = set()
    stage_refs_by_kid: dict[str, set[str]] = {}
    stage_joint_responsibility: dict[tuple[str, str], set[str]] = {}
    for stage in stages:
        sid = stage.get("id", "?")
        objective_refs = stage.get("objective_refs") or []
        kid_refs = stage.get("kid_refs") or []
        if not objective_refs:
            errors.append(f"阶段{sid}没有目标责任")
        if not kid_refs:
            errors.append(f"阶段{sid}没有知识责任")
        for oid in objective_refs:
            if oid not in objective_set:
                errors.append(f"阶段{sid}引用不存在的目标: {oid}")
            covered_objectives.add(oid)
        for kid in kid_refs:
            stage_refs_by_kid.setdefault(str(kid), set()).add(str(sid))
            if kid not in knowledge_set:
                errors.append(f"阶段{sid}引用不存在的KID: {kid}")
            elif knowledge_status_by_id.get(kid) not in {"must_teach", "retrieve_prior"}:
                errors.append(f"阶段{sid}引用非课堂范围KID: {kid}")
            covered_kids.add(kid)
        for oid in objective_refs:
            for kid in kid_refs:
                stage_joint_responsibility.setdefault((oid, kid), set()).add(sid)
        for field in (
            "name",
            "entry_reason",
            "text_scope",
            "initial_method",
            "student_change",
            "student_experience",
            "teacher_role",
            "evidence",
            "transition_reason",
        ):
            if not str(stage.get(field) or "").strip():
                errors.append(f"阶段{sid}缺{field}")
    for oid in sorted(objective_set - covered_objectives):
        errors.append(f"目标未进入任何阶段: {oid}")
    for kid in sorted(teachable_kids - covered_kids):
        errors.append(f"必教/旧知KID未被阶段落实覆盖: {kid}")

    knowledge_stage_refs = {
        str(item.get("kid") or ""): set(item.get("stage_refs") or [])
        for item in knowledge
    }
    for kid in sorted(knowledge_set):
        declared_refs = knowledge_stage_refs.get(kid, set())
        actual_refs = stage_refs_by_kid.get(kid, set())
        if declared_refs != actual_refs:
            only_declared = sorted(declared_refs - actual_refs)
            only_actual = sorted(actual_refs - declared_refs)
            errors.append(
                f"KID {kid}的stage_refs与阶段责任不一致: "
                f"仅knowledge_items={only_declared}; 仅stages={only_actual}"
            )
    for objective in objectives:
        oid = str(objective.get("id") or "")
        objective_kids = objective.get("kid_refs")
        for kid in objective_kids if isinstance(objective_kids, list) else []:
            if oid not in objective_set or kid not in knowledge_set:
                continue
            common_stages = (
                stage_joint_responsibility.get((oid, kid), set())
                & knowledge_stage_refs.get(kid, set())
            )
            if not common_stages:
                errors.append(f"目标{oid}与KID {kid}没有共同阶段责任")

    questions = contract.get("questions") or []
    question_ids = [str(question.get("id") or "").strip() for question in questions]
    if any(not question_id for question_id in question_ids):
        errors.append("贯穿问题ID为空")
    for duplicate in sorted(_duplicates(question_ids)):
        if duplicate:
            errors.append(f"贯穿问题ID重复: {duplicate}")
    for question in questions:
        qid = question.get("id", "?")
        if not str(question.get("text") or "").strip():
            errors.append(f"贯穿问题{qid}文本为空")
        if not str(question.get("rationale") or "").strip():
            errors.append(f"贯穿问题{qid}缺统摄理由")
        _check_nodes(question.get("mechanism_nodes") or [], f"贯穿问题{qid}", errors)
        question_objective_refs = question.get("objective_refs") or []
        question_kid_refs = question.get("kid_refs") or []
        if not question_objective_refs:
            errors.append(f"贯穿问题{qid}没有目标责任")
        if not question_kid_refs:
            errors.append(f"贯穿问题{qid}没有知识责任")
        for oid in question_objective_refs:
            if oid not in objective_set:
                errors.append(f"贯穿问题{qid}引用不存在的目标: {oid}")
        for kid in question_kid_refs:
            if kid not in knowledge_set:
                errors.append(f"贯穿问题{qid}引用不存在的KID: {kid}")
            elif knowledge_status_by_id.get(kid) not in {"must_teach", "retrieve_prior"}:
                errors.append(f"贯穿问题{qid}引用非课堂范围KID: {kid}")
        question_stage_refs = question.get("stage_refs") or []
        if not question_stage_refs:
            errors.append(f"贯穿问题{qid}没有阶段落点")
        for sid in question_stage_refs:
            if sid not in stage_set:
                errors.append(f"贯穿问题{qid}引用不存在的阶段: {sid}")
        recovery_stage_refs = question.get("recovery_stage_refs") or []
        if not recovery_stage_refs:
            errors.append(f"贯穿问题{qid}没有最终回收阶段")
        for sid in recovery_stage_refs:
            if sid not in stage_set:
                errors.append(f"贯穿问题{qid}回收于不存在的阶段: {sid}")
            elif sid not in question_stage_refs:
                errors.append(f"贯穿问题{qid}的回收阶段未列入问题阶段链: {sid}")

    logic = contract.get("overall_teaching_logic") or {}
    if len(str(logic.get("text") or "").strip()) < 80:
        errors.append("整体教学逻辑须为连续完整论证，当前为空或过短")
    logic_nodes = set(logic.get("mechanism_nodes") or [])
    _check_nodes(list(logic_nodes), "整体教学逻辑", errors)
    missing_nodes = CORE_LOGIC_NODES - logic_nodes
    if missing_nodes:
        errors.append(f"整体教学逻辑缺核心机制节点: {sorted(missing_nodes)}")
    logic_stage_refs = set(logic.get("stage_refs") or [])
    if logic_stage_refs != stage_set:
        errors.append("整体教学逻辑的stage_refs必须完整覆盖阶段落实")
    components = logic.get("components") or {}
    for component_id in sorted(LOGIC_COMPONENTS - set(components)):
        errors.append(f"整体教学逻辑缺少组成裁决: {component_id}")
    for component_id, decision in components.items():
        if component_id not in LOGIC_COMPONENTS:
            errors.append(f"整体教学逻辑含未知组成: {component_id}")
            continue
        status = decision.get("status")
        if status not in {"included", "not_applicable", "deferred"}:
            errors.append(f"整体教学逻辑组成{component_id}状态非法")
        refs = decision.get("stage_refs") or []
        if status == "included" and not refs:
            errors.append(f"整体教学逻辑组成{component_id}已纳入但没有阶段落点")
        if status != "included" and not str(decision.get("reason") or "").strip():
            errors.append(f"整体教学逻辑组成{component_id}未纳入但没有理由")
        for sid in refs:
            if sid not in stage_set:
                errors.append(f"整体教学逻辑组成{component_id}引用不存在的阶段: {sid}")

    boundary = str(contract.get("claim_boundary") or "")
    if not has_pending_classroom_boundary(boundary):
        errors.append("claim_boundary必须明确声明效果待真实课堂/试教验证")

    if not candidate and verify_receipt and approval_path and approval_path.is_file():
        try:
            receipt = json.loads(approval_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"owner_approval无法读取: {exc}")
        else:
            _reject_unknown_fields(receipt, OWNER_APPROVAL_FIELDS, "owner_approval", errors)
            if not isinstance(receipt, dict):
                return sorted(set(errors)), stats
            for field in sorted(OWNER_APPROVAL_STRING_FIELDS):
                if not isinstance(receipt.get(field), str):
                    errors.append(f"owner_approval {field}必须为字符串")
            if not isinstance(receipt.get("resolved_issues"), list):
                errors.append("owner_approval resolved_issues必须为数组")
            if receipt.get("schema_version") != "g1-owner-approval.v1":
                errors.append("owner_approval schema_version错误")
            if receipt.get("lesson_id") != lesson_id:
                errors.append("owner_approval lesson_id与锁不一致")
            if receipt.get("decision") != "approved":
                errors.append("所有者未批准当前教案")
            if receipt.get("author_id") != author_id:
                errors.append("owner_approval author_id与锁不一致")
            reviewer_value = receipt.get("reviewer_id")
            reviewer_id = reviewer_value.strip() if isinstance(reviewer_value, str) else ""
            if not reviewer_id:
                errors.append("owner_approval reviewer_id为空")
            elif reviewer_value != reviewer_id:
                errors.append("owner_approval reviewer_id不得含首尾空白")
            receipt_author_value = receipt.get("author_id")
            receipt_author_id = (
                receipt_author_value.strip() if isinstance(receipt_author_value, str) else ""
            )
            if reviewer_id and reviewer_id == receipt_author_id:
                errors.append("审核者不能与作者相同")
            if receipt.get("lesson_plan_path") != plan_entry.get("path"):
                errors.append("审核的教案路径与锁不一致")
            if receipt.get("lesson_plan_sha256") != plan_entry.get("sha256"):
                errors.append("审核的教案哈希与当前锁不一致")
            if receipt.get("evidence_manifest_sha256") != evidence_entry.get("sha256"):
                errors.append("审核的证据清单哈希与当前锁不一致")
            if receipt.get("lesson_plan_contract_sha256") != canonical_json_sha256(contract):
                errors.append("审核的教案机器合同哈希与当前合同不一致")
            standard_version = receipt.get("standard_version")
            if not isinstance(standard_version, str) or not standard_version.strip():
                errors.append("owner_approval缺standard_version")
            reviewed_at_value = receipt.get("reviewed_at")
            reviewed_at = reviewed_at_value.strip() if isinstance(reviewed_at_value, str) else ""
            if not reviewed_at:
                errors.append("owner_approval缺reviewed_at")
            else:
                try:
                    parsed_reviewed_at = datetime.fromisoformat(reviewed_at.replace("Z", "+00:00"))
                except ValueError:
                    parsed_reviewed_at = None
                if parsed_reviewed_at is None or parsed_reviewed_at.tzinfo is None or parsed_reviewed_at.utcoffset() is None:
                    errors.append("owner_approval reviewed_at必须是带时区的ISO 8601时间")
            approval_event_id = receipt.get("approval_event_id")
            if not isinstance(approval_event_id, str) or not approval_event_id.strip():
                errors.append("owner_approval approval_event_id为空")
            approval_source = receipt.get("approval_source")
            if not isinstance(approval_source, str) or not approval_source.strip():
                errors.append("owner_approval approval_source为空")
            if receipt.get("verification_mode") != "external_review_gate":
                errors.append("owner_approval verification_mode必须为external_review_gate")
            authentication_value = receipt.get("authentication_boundary")
            authentication_boundary = authentication_value if isinstance(authentication_value, str) else ""
            if not authentication_boundary.strip() or not (
                ("不认证" in authentication_boundary or "只验证" in authentication_boundary)
                and "人工核验" in authentication_boundary
            ):
                errors.append("owner_approval authentication_boundary未声明本地验证与外部人工身份核验边界")
            approval_value = receipt.get("approval_statement")
            approval_statement = approval_value if isinstance(approval_value, str) else ""
            current_plan_sha = str(plan_entry.get("sha256") or "")
            if not current_plan_sha or current_plan_sha not in approval_statement:
                errors.append("owner_approval approval_statement未包含当前教案哈希")

    return sorted(set(errors)), stats


def validate(
    lock: dict,
    root: Path = ROOT,
    verify_receipt: bool = True,
    lock_path: Path | None = None,
) -> tuple[list[str], dict]:
    """Validate a formal G1 lock; a bound owner receipt is always required."""
    return _validate_document(
        lock,
        root,
        candidate=False,
        verify_receipt=verify_receipt,
        lock_path=lock_path,
    )


def validate_candidate(
    candidate: dict,
    root: Path = ROOT,
    candidate_path: Path | None = None,
) -> tuple[list[str], dict]:
    """Precheck the exact plan/contract/evidence combination before owner review."""
    return _validate_document(
        candidate,
        root,
        candidate=True,
        verify_receipt=False,
        candidate_path=candidate_path,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lock", nargs="?", type=Path, help="正式G1 lesson_plan_lock.json")
    parser.add_argument("--candidate", type=Path, help="待所有者审核的lesson_plan_candidate.json")
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    if bool(args.lock) == bool(args.candidate):
        parser.error("请提供一个正式lock路径，或使用--candidate提供一个候选路径")
    source_path = args.candidate or args.lock
    try:
        document = json.loads(source_path.read_text(encoding="utf-8"))
        errors, stats = (
            validate_candidate(document, root=args.root, candidate_path=args.candidate)
            if args.candidate
            else validate(document, root=args.root, lock_path=args.lock)
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    for error in errors:
        print(f"[error] {error}")
    if errors:
        gate_name = "G1候选合同预检" if args.candidate else "G1教案门"
        print(f"{gate_name}失败：{len(errors)}项")
        return 1
    if args.candidate:
        print(
            "G1候选合同预检通过："
            f"目标{stats['objectives']} / 知识{stats['knowledge_items']} / 阶段{stats['stages']}；"
            "状态仍为待所有者审核，不构成G1批准"
        )
        return 0
    print(
        "G1教案血缘门通过："
        f"目标{stats['objectives']} / 知识{stats['knowledge_items']} / 阶段{stats['stages']}；"
        "本地验证器不认证人类身份，所有者真实性须由外部review gate核验"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
