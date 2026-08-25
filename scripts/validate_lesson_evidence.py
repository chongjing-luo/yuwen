#!/usr/bin/env python3
"""Validate the G0 evidence manifest for one Chinese lesson.

The validator enforces provenance and honest gaps (K1/U6/J7).  It does not
judge whether a literary interpretation is good; that remains a review gate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader

from lesson_identity import LESSON_ID_PATTERN, check_lesson_id_registry, resolve_metadata_course
from repository_source_policy import reference_is_available

ROOT = Path(__file__).resolve().parents[1]
NODE_IDS = {f"K{i}" for i in range(1, 6)} | {f"U{i}" for i in range(1, 9)} | {f"J{i}" for i in range(1, 8)}
SHA256_LENGTH = 64
CANONICAL_PENDING_CLASSROOM_BOUNDARY = (
    "课堂证据状态：未采集；学生掌握、理解与享受均待真实试教验证。"
)
PENDING_CLASSROOM_RE = re.compile(
    r"(?:待|未|尚未|仍待).{0,12}(?:课堂|试教)|(?:课堂|试教).{0,12}(?:待|未|尚无|为空)"
)
PROHIBITED_CLASSROOM_SUCCESS_RE = re.compile(
    r"(?:学生.{0,8}(?:已经|已).{0,10}(?:学懂|学会|掌握|享受)|"
    r"(?:课堂|试教).{0,8}(?:已经|已).{0,8}(?:完成|验证|证明))"
)
NEGATED_CLAIM_RE = re.compile(r"(?:不声称|不得声称|不能断言).{0,40}(?:[。；]|$)")
MANIFEST_FIELDS = {
    "schema_version", "lesson_id", "mechanism_nodes", "normative_sources",
    "derived_sources", "knowledge_sources", "knowledge_gap_reason",
    "evidence_dossier", "claim_boundary",
}
NORMATIVE_SOURCE_FIELDS = {"source_id", "role", "authority", "path", "sha256"}
DERIVED_SOURCE_FIELDS = {
    "source_id", "role", "path", "sha256", "derived_from_source_id", "derived_from_sha256",
}
KNOWLEDGE_SOURCE_FIELDS = {"source_id", "path", "sha256"}
BOUND_FILE_FIELDS = {"path", "sha256"}


def _reject_unknown_fields(value: object, allowed: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{label}必须为对象")
        return
    for field in sorted(set(value) - allowed):
        errors.append(f"{label}含未知字段: {field}")


def has_pending_classroom_boundary(value: object, *, canonical: bool = True) -> bool:
    """Require the controlled pending-classroom declaration for new locks.

    A free-text regex can detect some bad claims but cannot exclude paraphrased
    contradictions.  G0-G4 therefore use one controlled governance value; the
    loose branch exists only so legacy v1 data remains readable outside strict
    mode.
    """
    text = str(value or "")
    if canonical:
        return text.strip() == CANONICAL_PENDING_CLASSROOM_BOUNDARY
    assertions = NEGATED_CLAIM_RE.sub("", text)
    return bool(PENDING_CLASSROOM_RE.search(text)) and not PROHIBITED_CLASSROOM_SUCCESS_RE.search(assertions)


def _resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _check_file(entry: dict, label: str, root: Path, errors: list[str]) -> Path | None:
    path_value = str(entry.get("path") or "").strip()
    expected = str(entry.get("sha256") or "").strip()
    if not path_value:
        errors.append(f"{label}缺path")
        return None
    if len(expected) != SHA256_LENGTH:
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
    if not path.is_file() and not path.exists() and reference_is_available(root, path_value):
        return None
    if not path.is_file():
        errors.append(f"{label}文件不存在: {path_value}")
        return None
    if _sha256(path) != expected:
        errors.append(f"{label}的SHA-256不匹配: {path_value}")
    return path


def validate(
    manifest: dict,
    root: Path = ROOT,
    manifest_path: Path | None = None,
) -> tuple[list[str], dict]:
    errors: list[str] = []
    normative = manifest.get("normative_sources") or []
    derived = manifest.get("derived_sources") or []
    knowledge = manifest.get("knowledge_sources") or []
    stats = {
        "normative_sources": len(normative),
        "derived_sources": len(derived),
        "knowledge_sources": len(knowledge),
    }

    if manifest.get("schema_version") != "lesson-evidence.v1":
        errors.append("schema_version必须为lesson-evidence.v1")
    for unknown_field in sorted(set(manifest) - MANIFEST_FIELDS):
        errors.append(f"evidence_manifest含未知字段: {unknown_field}")
    lesson_id_value = manifest.get("lesson_id")
    lesson_id = lesson_id_value.strip() if isinstance(lesson_id_value, str) else ""
    if not lesson_id:
        errors.append("lesson_id必须为非空字符串")
    elif not LESSON_ID_PATTERN.fullmatch(lesson_id):
        errors.append("lesson_id格式非法；正式课须使用LES-{册代码}-{课文代码}-{两位序号}")
    course_dir = None
    if manifest_path is not None:
        course_dir = resolve_metadata_course(
            manifest_path,
            root,
            required_name="evidence_manifest.json",
            label="evidence_manifest",
            errors=errors,
        )
    check_lesson_id_registry(lesson_id, course_dir, root, errors)

    nodes = manifest.get("mechanism_nodes") or []
    if not nodes:
        errors.append("mechanism_nodes为空（新产物须绑定K/U/J节点）")
    for node in nodes:
        if node not in NODE_IDS:
            errors.append(f"mechanism_nodes含非法节点: {node}")

    source_ids: set[str] = set()
    normative_by_id: dict[str, dict] = {}
    roles: set[str] = set()
    for index, source in enumerate(normative):
        label = f"normative_sources[{index}]"
        _reject_unknown_fields(source, NORMATIVE_SOURCE_FIELDS, label, errors)
        source_id = str(source.get("source_id") or "").strip()
        if not source_id:
            errors.append(f"{label}缺source_id")
        elif source_id in source_ids:
            errors.append(f"source_id重复: {source_id}")
        else:
            source_ids.add(source_id)
            normative_by_id[source_id] = source
        role = str(source.get("role") or "").strip()
        roles.add(role)
        if source.get("authority") != "S1":
            errors.append(f"{label}不是S1规范源")
        path_value = str(source.get("path") or "")
        if role in {"textbook", "curriculum_standard"} and Path(path_value).suffix.lower() != ".pdf":
            errors.append(f"{label}的{role}必须回到PDF规范原件")
        source_path = _check_file(source, label, root, errors)
        if source_path and role in {"textbook", "curriculum_standard"}:
            payload = source_path.read_bytes()
            if len(payload) < 16 or not payload.startswith(b"%PDF"):
                errors.append(f"{label}规范PDF内容无效（须有PDF签名且非空壳）")
            else:
                try:
                    reader = PdfReader(source_path, strict=False)
                    page_count = len(reader.pages)
                except Exception as exc:  # pypdf exposes several parse exception types
                    errors.append(f"{label}规范PDF无法解析: {type(exc).__name__}")
                else:
                    if page_count < 1:
                        errors.append(f"{label}规范PDF没有可读页面")

    for required_role in ("textbook", "curriculum_standard"):
        if required_role not in roles:
            errors.append(f"normative_sources缺少{required_role} PDF规范源")

    if not derived:
        errors.append("derived_sources为空（G0须有至少一个可检索派生源）")
    for index, source in enumerate(derived):
        label = f"derived_sources[{index}]"
        _reject_unknown_fields(source, DERIVED_SOURCE_FIELDS, label, errors)
        source_id = str(source.get("source_id") or "").strip()
        if not source_id:
            errors.append(f"{label}缺source_id")
        elif source_id in source_ids:
            errors.append(f"source_id重复: {source_id}")
        else:
            source_ids.add(source_id)
        if not str(source.get("role") or "").strip():
            errors.append(f"{label}缺role")
        source_path = _check_file(source, label, root, errors)
        if source_path and source_path.stat().st_size < 20:
            errors.append(f"{label}派生源内容不足")
        parent_id = str(source.get("derived_from_source_id") or "").strip()
        parent = normative_by_id.get(parent_id)
        if parent is None:
            errors.append(f"{label}未绑定已登记的上游规范源")
        elif source.get("derived_from_sha256") != parent.get("sha256"):
            errors.append(f"{label}的上游规范源哈希与登记值不一致")

    for index, source in enumerate(knowledge):
        label = f"knowledge_sources[{index}]"
        _reject_unknown_fields(source, KNOWLEDGE_SOURCE_FIELDS, label, errors)
        source_id = str(source.get("source_id") or "").strip()
        if not source_id:
            errors.append(f"{label}缺source_id")
        elif source_id in source_ids:
            errors.append(f"source_id重复: {source_id}")
        else:
            source_ids.add(source_id)
        source_path = _check_file(source, label, root, errors)
        if source_path and source_path.stat().st_size < 30:
            errors.append(f"{label}知识源内容不足")

    if not knowledge and not str(manifest.get("knowledge_gap_reason") or "").strip():
        errors.append("knowledge_sources为空且未说明知识库缺口（K1）")

    dossier = manifest.get("evidence_dossier")
    if not isinstance(dossier, dict):
        errors.append("evidence_dossier缺失")
    else:
        _reject_unknown_fields(dossier, BOUND_FILE_FIELDS, "evidence_dossier", errors)
        dossier_path = _check_file(dossier, "evidence_dossier", root, errors)
        if dossier_path:
            try:
                dossier_text = dossier_path.read_text(encoding="utf-8")
            except (OSError, UnicodeError) as exc:
                errors.append(f"evidence_dossier不是可读UTF-8文本: {exc}")
            else:
                normalized = "".join(character for character in dossier_text if not character.isspace())
                headings = [line for line in dossier_text.splitlines() if line.lstrip().startswith("#")]
                if len(normalized) < 120 or len(headings) < 2:
                    errors.append("证据档案最低有效内容不足（至少120个非空白字符与2个标题）")
                elif len(set(normalized.casefold())) < 20 or len(set(normalized.casefold())) / len(normalized) < 0.05:
                    errors.append("证据档案低熵，疑似重复字符占位")

    boundary = str(manifest.get("claim_boundary") or "")
    if not boundary.strip():
        errors.append("claim_boundary为空")
    elif not has_pending_classroom_boundary(boundary):
        errors.append("claim_boundary必须明确声明效果待真实课堂/试教验证（J7）")
    return sorted(set(errors)), stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        errors, stats = validate(manifest, root=args.root, manifest_path=args.manifest)
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    for error in errors:
        print(f"[error] {error}")
    if errors:
        print(f"G0证据门失败：{len(errors)}项")
        return 1
    print(
        "G0证据门通过："
        f"规范源{stats['normative_sources']} / 派生源{stats['derived_sources']} / 知识源{stats['knowledge_sources']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
