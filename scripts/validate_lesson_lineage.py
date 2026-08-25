#!/usr/bin/env python3
"""Validate G2 design locks and G3 materials locks for lesson preparation."""
from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import zipfile
from datetime import datetime
from xml.etree import ElementTree
from pathlib import Path

from validate_lesson_plan import validate as validate_lesson_plan
from validate_lesson_schema import validate as validate_lesson_schema

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_MATERIAL_ROLES = {"pptx", "screenplay", "learning_sheet", "board_plan"}
CONTENT_TYPES_NS = "http://schemas.openxmlformats.org/package/2006/content-types"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
PRESENTATION_NS = "http://schemas.openxmlformats.org/presentationml/2006/main"
DRAWING_NS = "http://schemas.openxmlformats.org/drawingml/2006/main"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
OFFICE_DOCUMENT_REL = f"{OFFICE_REL_NS}/officeDocument"
SLIDE_REL = f"{OFFICE_REL_NS}/slide"
IMAGE_REL = f"{OFFICE_REL_NS}/image"
SLIDE_CONTENT_TYPE = "application/vnd.openxmlformats-officedocument.presentationml.slide+xml"
DESIGN_LOCK_FIELDS = {
    "schema_version", "lesson_id", "author_id", "lesson_plan_lock",
    "lesson_plan_sha256", "teaching_design", "lesson_data", "owner_approval",
    "validation", "status",
}
DESIGN_APPROVAL_FIELDS = {
    "schema_version", "lesson_id", "reviewer_id", "author_id", "decision",
    "reviewed_at", "approval_event_id", "approval_source", "verification_mode",
    "authentication_boundary", "teaching_design_path", "teaching_design_sha256",
    "lesson_data_sha256", "lesson_plan_lock_sha256", "approval_statement",
    "standard_version", "resolved_issues",
}
MATERIALS_LOCK_FIELDS = {"schema_version", "lesson_id", "author_id", "design_lock", "manifest", "status"}
MATERIALS_MANIFEST_FIELDS = {"schema_version", "lesson_id", "source_design_lock_sha256", "artifacts"}
ARTIFACT_FIELDS = {"role", "path", "sha256"}


def _image_payload_matches(content_type: str, payload: bytes) -> bool:
    if content_type == "image/png":
        return payload.startswith(b"\x89PNG\r\n\x1a\n")
    if content_type in {"image/jpeg", "image/jpg"}:
        return payload.startswith(b"\xff\xd8\xff")
    if content_type == "image/gif":
        return payload.startswith((b"GIF87a", b"GIF89a"))
    if content_type == "image/bmp":
        return payload.startswith(b"BM")
    if content_type in {"image/tiff", "image/tif"}:
        return payload.startswith((b"II*\x00", b"MM\x00*"))
    if content_type == "image/webp":
        return len(payload) >= 12 and payload.startswith(b"RIFF") and payload[8:12] == b"WEBP"
    if content_type == "image/svg+xml":
        try:
            root = ElementTree.fromstring(payload)
        except ElementTree.ParseError:
            return False
        return root.tag.rsplit("}", 1)[-1] == "svg"
    if content_type in {"image/x-emf", "image/emf"}:
        return len(payload) >= 44 and payload[:4] == b"\x01\x00\x00\x00"
    if content_type in {"image/x-wmf", "image/wmf"}:
        return payload.startswith((b"\xd7\xcd\xc6\x9a", b"\x01\x00\x09\x00"))
    return False


def _resolve(root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else root / path


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bound_file(entry: dict, label: str, root: Path, errors: list[str]) -> Path | None:
    value = str(entry.get("path") or "").strip()
    expected = str(entry.get("sha256") or "").strip()
    if not value:
        errors.append(f"{label}缺path")
        return None
    if len(expected) != 64:
        errors.append(f"{label}缺合法SHA-256")
        return None
    raw_path = Path(value)
    if raw_path.is_absolute():
        errors.append(f"{label}必须使用项目根相对路径")
        return None
    path = _resolve(root, value).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        errors.append(f"{label}路径越出项目根: {value}")
        return None
    if not path.is_file():
        errors.append(f"{label}文件不存在: {value}")
        return None
    if _sha256(path) != expected:
        errors.append(f"{label}哈希与当前文件不一致: {value}")
    return path


def _validate_design_approval(
    receipt: dict,
    lock: dict,
    approval_path: Path,
    root: Path,
) -> list[str]:
    errors: list[str] = []
    missing = sorted(DESIGN_APPROVAL_FIELDS - set(receipt))
    unknown = sorted(set(receipt) - DESIGN_APPROVAL_FIELDS)
    if missing:
        errors.append(f"G2所有者审批回执缺字段: {missing}")
    if unknown:
        errors.append(f"G2所有者审批回执含未知字段: {unknown}")
    if receipt.get("schema_version") != "g2-owner-approval.v1":
        errors.append("G2所有者审批回执schema_version必须为g2-owner-approval.v1")
    if receipt.get("lesson_id") != lock.get("lesson_id"):
        errors.append("G2所有者审批回执lesson_id与design_lock不一致")
    author_id = str(receipt.get("author_id") or "").strip()
    reviewer_id = str(receipt.get("reviewer_id") or "").strip()
    if not author_id or author_id != str(lock.get("author_id") or "").strip():
        errors.append("G2所有者审批回执author_id与设计作者不一致")
    if not reviewer_id:
        errors.append("G2所有者审批回执reviewer_id为空")
    elif reviewer_id.casefold() == author_id.casefold():
        errors.append("G2审批者不得与设计作者相同")
    if receipt.get("decision") != "approved":
        errors.append("G2所有者审批回执decision必须为approved")
    reviewed_at = str(receipt.get("reviewed_at") or "").strip()
    try:
        parsed_time = datetime.fromisoformat(reviewed_at)
    except ValueError:
        parsed_time = None
    if parsed_time is None or parsed_time.tzinfo is None:
        errors.append("G2所有者审批回执reviewed_at必须为带时区ISO 8601时间")
    for field in ("approval_event_id", "approval_source", "authentication_boundary", "standard_version"):
        if not str(receipt.get(field) or "").strip():
            errors.append(f"G2所有者审批回执{field}为空")
    if receipt.get("verification_mode") != "external_review_gate":
        errors.append("G2所有者审批回执verification_mode必须为external_review_gate")
    if not isinstance(receipt.get("resolved_issues"), list):
        errors.append("G2所有者审批回执resolved_issues必须为数组")

    design_binding = lock.get("teaching_design") or {}
    lesson_binding = lock.get("lesson_data") or {}
    g1_binding = lock.get("lesson_plan_lock") or {}
    if receipt.get("teaching_design_path") != design_binding.get("path"):
        errors.append("G2所有者审批回执未绑定当前教学设计路径")
    if receipt.get("teaching_design_sha256") != design_binding.get("sha256"):
        errors.append("G2所有者审批回执未绑定当前教学设计哈希")
    if receipt.get("lesson_data_sha256") != lesson_binding.get("sha256"):
        errors.append("G2所有者审批回执未绑定当前课程数据")
    if receipt.get("lesson_plan_lock_sha256") != g1_binding.get("sha256"):
        errors.append("G2所有者审批回执未绑定当前G1锁")
    statement = str(receipt.get("approval_statement") or "")
    if str(design_binding.get("sha256") or "") not in statement:
        errors.append("G2所有者审批声明未包含当前教学设计哈希")
    expected_parent = (_resolve(root, str(g1_binding.get("path") or "")).resolve()).parent
    if approval_path.parent != expected_parent:
        errors.append("G2所有者审批回执必须位于同一课_meta目录")
    return errors


def _pptx_ooxml_error(path: Path) -> str | None:
    """Return why a PPTX is not a minimally coherent OPC/PresentationML tree."""
    required = {
        "[Content_Types].xml",
        "_rels/.rels",
        "ppt/presentation.xml",
        "ppt/_rels/presentation.xml.rels",
    }
    if not zipfile.is_zipfile(path):
        return "不是ZIP包"
    try:
        with zipfile.ZipFile(path) as package:
            members = set(package.namelist())
            missing = required - members
            if missing:
                return f"缺少OPC核心成员{sorted(missing)}"
            try:
                content_types = ElementTree.fromstring(package.read("[Content_Types].xml"))
                root_relationships = ElementTree.fromstring(package.read("_rels/.rels"))
                presentation = ElementTree.fromstring(package.read("ppt/presentation.xml"))
                presentation_relationships = ElementTree.fromstring(package.read("ppt/_rels/presentation.xml.rels"))
            except ElementTree.ParseError as exc:
                return f"核心XML不可解析: {exc}"
            if content_types.tag != f"{{{CONTENT_TYPES_NS}}}Types":
                return "[Content_Types].xml根命名空间错误"
            overrides = {
                item.get("PartName"): item.get("ContentType")
                for item in content_types.findall(f"{{{CONTENT_TYPES_NS}}}Override")
            }
            defaults = {
                item.get("Extension"): item.get("ContentType")
                for item in content_types.findall(f"{{{CONTENT_TYPES_NS}}}Default")
            }
            if defaults.get("rels") != "application/vnd.openxmlformats-package.relationships+xml":
                return "缺rels默认ContentType"
            if overrides.get("/ppt/presentation.xml") != (
                "application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"
            ):
                return "缺少presentation主部件ContentType"
            if root_relationships.tag != f"{{{PACKAGE_REL_NS}}}Relationships":
                return "根关系文件命名空间错误"
            office_relationships = [
                item
                for item in root_relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
                if item.get("Type") == OFFICE_DOCUMENT_REL
            ]
            if not any(item.get("Target") == "ppt/presentation.xml" for item in office_relationships):
                return "根关系未指向ppt/presentation.xml"
            if any(item.get("TargetMode") not in (None, "Internal") for item in office_relationships):
                return "根officeDocument关系不得使用External TargetMode"
            if presentation.tag != f"{{{PRESENTATION_NS}}}presentation":
                return "presentation.xml根命名空间错误"
            slide_ids = presentation.findall(
                f"{{{PRESENTATION_NS}}}sldIdLst/{{{PRESENTATION_NS}}}sldId"
            )
            if not slide_ids:
                return "presentation没有任何slide引用"
            rel_map = {
                item.get("Id"): (item.get("Type"), item.get("Target"), item.get("TargetMode"))
                for item in presentation_relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
            }
            visible_objects = 0
            for slide_id in slide_ids:
                rel_id = slide_id.get(f"{{{OFFICE_REL_NS}}}id")
                rel_type, target, target_mode = rel_map.get(rel_id, (None, None, None))
                if rel_type != SLIDE_REL or not target:
                    return f"slide引用{rel_id!r}没有合法关系"
                if target_mode not in (None, "Internal"):
                    return f"slide关系不得使用External TargetMode: {rel_id!r}"
                member = posixpath.normpath(posixpath.join("ppt", target))
                if not member.startswith("ppt/") or member not in members:
                    return f"slide关系目标不存在: {target}"
                if overrides.get(f"/{member}") != SLIDE_CONTENT_TYPE:
                    return f"slide部件ContentType错误或缺失: {member}"
                try:
                    slide_root = ElementTree.fromstring(package.read(member))
                except ElementTree.ParseError as exc:
                    return f"slide XML不可解析: {exc}"
                if slide_root.tag != f"{{{PRESENTATION_NS}}}sld":
                    return f"slide根命名空间错误: {member}"
                visible_objects += sum(
                    1 for node in slide_root.findall(f".//{{{DRAWING_NS}}}t")
                    if str(node.text or "").strip()
                )
                rels_member = posixpath.join(
                    posixpath.dirname(member),
                    "_rels",
                    posixpath.basename(member) + ".rels",
                )
                slide_rel_map: dict[str, tuple[str | None, str | None, str | None]] = {}
                if rels_member in members:
                    try:
                        slide_relationships = ElementTree.fromstring(package.read(rels_member))
                    except ElementTree.ParseError as exc:
                        return f"slide关系XML不可解析: {rels_member}: {exc}"
                    if slide_relationships.tag != f"{{{PACKAGE_REL_NS}}}Relationships":
                        return f"slide关系文件命名空间错误: {rels_member}"
                    if any(
                        item.get("TargetMode") not in (None, "Internal")
                        for item in slide_relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
                    ):
                        return f"slide部件关系不得使用External TargetMode: {rels_member}"
                    slide_rel_map = {
                        item.get("Id"): (item.get("Type"), item.get("Target"), item.get("TargetMode"))
                        for item in slide_relationships.findall(f"{{{PACKAGE_REL_NS}}}Relationship")
                    }
                for picture in slide_root.findall(f".//{{{PRESENTATION_NS}}}pic"):
                    blip = picture.find(f".//{{{DRAWING_NS}}}blip")
                    if blip is None:
                        # An empty <p:pic/> is only a placeholder, not visible content.
                        continue
                    rel_id = blip.get(f"{{{OFFICE_REL_NS}}}embed") if blip is not None else None
                    rel_type, target, target_mode = slide_rel_map.get(rel_id, (None, None, None))
                    if rel_type != IMAGE_REL or not target or target_mode not in (None, "Internal"):
                        return f"图片对象缺内部image关系: {member}"
                    media_member = posixpath.normpath(posixpath.join(posixpath.dirname(member), target))
                    if not media_member.startswith("ppt/media/"):
                        return f"图片关系目标必须位于ppt/media: {media_member}"
                    if media_member not in members or package.getinfo(media_member).file_size <= 0:
                        return f"图片媒体部件不存在或为空: {media_member}"
                    extension = posixpath.splitext(media_member)[1].lstrip(".").lower()
                    content_type = overrides.get(f"/{media_member}") or defaults.get(extension)
                    if not str(content_type or "").startswith("image/"):
                        return f"图片媒体部件缺image ContentType: {media_member}"
                    if not _image_payload_matches(str(content_type), package.read(media_member)):
                        return f"图片媒体部件签名与ContentType不匹配: {media_member}"
                    visible_objects += 1
            if visible_objects == 0:
                return "全部slide没有可见文本或图片"
    except (OSError, KeyError, zipfile.BadZipFile) as exc:
        return str(exc)
    return None


def validate_design_lock(
    lock: dict,
    root: Path = ROOT,
    enforcement_config: dict | None = None,
) -> list[str]:
    errors: list[str] = []
    if lock.get("schema_version") != "design-lock.v1":
        errors.append("design_lock schema_version必须为design-lock.v1")
    for unknown_field in sorted(set(lock) - DESIGN_LOCK_FIELDS):
        errors.append(f"design_lock含未知字段: {unknown_field}")
    lesson_id = str(lock.get("lesson_id") or "").strip()
    if not lesson_id:
        errors.append("design_lock lesson_id为空")
    if lock.get("status") != "validated":
        errors.append("design_lock状态不是validated")
    if lock.get("author_id") in (None, ""):
        errors.append("design_lock author_id为空")
    elif not isinstance(lock.get("author_id"), str) or not lock["author_id"].strip():
        errors.append("design_lock author_id必须为非空字符串")

    g1_path = _bound_file(lock.get("lesson_plan_lock") or {}, "lesson_plan_lock", root, errors)
    teaching_design_path = _bound_file(lock.get("teaching_design") or {}, "teaching_design", root, errors)
    lesson_data_path = _bound_file(lock.get("lesson_data") or {}, "lesson_data", root, errors)
    approval_path = _bound_file(lock.get("owner_approval") or {}, "G2所有者审批回执", root, errors)
    if g1_path and g1_path.parent.name == "_meta":
        lesson_dir = g1_path.parent.parent
        try:
            lesson_dir.relative_to((root / "work/teaching").resolve())
        except ValueError:
            errors.append("design_lock课程必须位于work/teaching正式课程树")
        if teaching_design_path and teaching_design_path.parent != lesson_dir:
            errors.append("teaching_design必须位于同一课目录")
        if lesson_data_path and lesson_data_path.parent != lesson_dir:
            errors.append("lesson_data必须位于同一课目录")
    elif g1_path:
        errors.append("lesson_plan_lock必须位于同一课_meta目录")
    design_text = ""
    if teaching_design_path and teaching_design_path.is_file():
        try:
            design_text = teaching_design_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            errors.append(f"teaching_design无法读取: {exc}")
        else:
            if not design_text.strip():
                errors.append("teaching_design为空")
            normalized = "".join(character for character in design_text if not character.isspace())
            headings = [line for line in design_text.splitlines() if line.lstrip().startswith("#")]
            nonblank_lines = [line for line in design_text.splitlines() if line.strip()]
            if (
                len(normalized) < 120
                or len(set(normalized.casefold())) < 20
                or len(headings) < 3
                or len(nonblank_lines) < 6
            ):
                errors.append(
                    "teaching_design最低有效内容不足：至少120个非空白字符、3个Markdown标题、6行内容"
                )

    if g1_path and g1_path.is_file():
        try:
            g1_lock = json.loads(g1_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"G1教案锁无法读取: {exc}")
        else:
            upstream_errors, _ = validate_lesson_plan(
                g1_lock,
                root=root,
                lock_path=g1_path,
            )
            errors.extend(f"G1上游无效: {error}" for error in upstream_errors)
            if g1_lock.get("lesson_id") != lesson_id:
                errors.append("design_lock lesson_id与G1不一致")
            if lock.get("lesson_plan_sha256") != (g1_lock.get("lesson_plan") or {}).get("sha256"):
                errors.append("design_lock lesson_plan_sha256与G1不一致")

    if approval_path and approval_path.is_file():
        try:
            approval = json.loads(approval_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"G2所有者审批回执无法读取: {exc}")
        else:
            if not isinstance(approval, dict):
                errors.append("G2所有者审批回执必须为JSON对象")
            else:
                errors.extend(_validate_design_approval(approval, lock, approval_path, root))

    validation = lock.get("validation") or {}
    if validation.get("validator") != "validate_lesson_schema.py":
        errors.append("design_lock未登记通用课程数据验证器")
    if validation.get("strict") is not True or validation.get("passed") is not True:
        errors.append("design_lock必须绑定strict且passed的G2验证")

    if lesson_data_path and lesson_data_path.is_file():
        try:
            lesson_data = json.loads(lesson_data_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"lesson_data无法读取: {exc}")
        else:
            if lesson_data.get("lesson_id") != lesson_id:
                errors.append("lesson_data lesson_id与design_lock不一致")
            schema_errors, _, _ = validate_lesson_schema(
                lesson_data,
                strict=True,
                root=root,
                enforcement_config=enforcement_config,
            )
            errors.extend(f"课程数据无效: {error}" for error in schema_errors)
            if design_text:
                required_anchors = [lesson_id] + [
                    str(page.get("page_id") or "").strip()
                    for page in lesson_data.get("pages") or []
                    if str(page.get("page_id") or "").strip()
                ]
                missing_anchors = [anchor for anchor in required_anchors if anchor not in design_text]
                if missing_anchors:
                    errors.append(f"teaching_design未锚定同源lesson/page ID: {missing_anchors}")
    return sorted(set(errors))


def validate_materials_lock(
    lock: dict,
    root: Path = ROOT,
    enforcement_config: dict | None = None,
) -> list[str]:
    errors: list[str] = []
    if lock.get("schema_version") != "materials-lock.v1":
        errors.append("materials_lock schema_version必须为materials-lock.v1")
    for unknown_field in sorted(set(lock) - MATERIALS_LOCK_FIELDS):
        errors.append(f"materials_lock含未知字段: {unknown_field}")
    lesson_id = str(lock.get("lesson_id") or "").strip()
    if not lesson_id:
        errors.append("materials_lock lesson_id为空")
    if lock.get("status") != "built":
        errors.append("materials_lock状态不是built")
    if lock.get("author_id") in (None, ""):
        errors.append("materials_lock author_id为空")
    elif not isinstance(lock.get("author_id"), str) or not lock["author_id"].strip():
        errors.append("materials_lock author_id必须为非空字符串")

    design_path = _bound_file(lock.get("design_lock") or {}, "design_lock", root, errors)
    manifest_path = _bound_file(lock.get("manifest") or {}, "manifest", root, errors)
    design_sha = (lock.get("design_lock") or {}).get("sha256")
    lesson_dir: Path | None = None
    if design_path:
        if design_path.parent.name != "_meta":
            errors.append("design_lock必须位于同一课_meta目录")
        else:
            lesson_dir = design_path.parent.parent
    if lesson_dir and manifest_path:
        if manifest_path.parent != lesson_dir / "materials":
            errors.append("manifest必须位于同一课目录的materials子目录")
        root_office_files = [
            path for path in lesson_dir.iterdir()
            if path.is_file() and path.suffix.lower() in {".pptx", ".docx"}
        ]
        if root_office_files:
            errors.append("课目录根部不得存在未入manifest的PPTX/DOCX")

    source_page_ids: list[str] = []
    canonical_lines: list[str] = []
    if design_path and design_path.is_file():
        try:
            design_lock = json.loads(design_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"G2设计锁无法读取: {exc}")
        else:
            errors.extend(
                f"G2上游无效: {error}"
                for error in validate_design_lock(
                    design_lock,
                    root=root,
                    enforcement_config=enforcement_config,
                )
            )
            if design_lock.get("lesson_id") != lesson_id:
                errors.append("materials_lock lesson_id与G2不一致")
            lesson_data_value = str((design_lock.get("lesson_data") or {}).get("path") or "")
            lesson_data_path = _resolve(root, lesson_data_value).resolve() if lesson_data_value else None
            if lesson_data_path and lesson_data_path.is_file():
                try:
                    source_lesson = json.loads(lesson_data_path.read_text(encoding="utf-8"))
                except (OSError, UnicodeError, json.JSONDecodeError):
                    source_lesson = {}
                source_page_ids = [
                    str(page.get("page_id") or "").strip()
                    for page in source_lesson.get("pages") or []
                    if str(page.get("page_id") or "").strip()
                ]
                canonical_lines = [
                    str(line).strip()
                    for line in (source_lesson.get("text_contract") or {}).get("canonical_lines") or []
                    if str(line).strip()
                ]

    if manifest_path and manifest_path.is_file():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            errors.append(f"materials manifest无法读取: {exc}")
        else:
            if manifest.get("schema_version") != "lesson-materials-manifest.v1":
                errors.append("materials manifest schema_version错误")
            for unknown_field in sorted(set(manifest) - MATERIALS_MANIFEST_FIELDS):
                errors.append(f"materials manifest含未知字段: {unknown_field}")
            if manifest.get("lesson_id") != lesson_id:
                errors.append("materials manifest lesson_id与锁不一致")
            if manifest.get("source_design_lock_sha256") != design_sha:
                errors.append("materials manifest未绑定当前design_lock哈希")
            roles: list[str] = []
            artifact_paths: list[tuple[int, str, Path]] = []
            for index, artifact in enumerate(manifest.get("artifacts") or []):
                for unknown_field in sorted(set(artifact) - ARTIFACT_FIELDS):
                    errors.append(f"artifact[{index}]含未知字段: {unknown_field}")
                role = str(artifact.get("role") or "").strip()
                roles.append(role)
                artifact_path = _bound_file(artifact, f"artifact[{index}]({role or '?'})", root, errors)
                if artifact_path:
                    artifact_paths.append((index, role, artifact_path.resolve()))
                    if artifact_path.stat().st_size == 0:
                        errors.append(f"artifact[{index}]({role or '?'})物料文件为空")
                    if role in {"screenplay", "learning_sheet", "board_plan"}:
                        if artifact_path.suffix.lower() != ".md":
                            errors.append(f"artifact[{index}]({role})必须为Markdown文本")
                        try:
                            material_text = artifact_path.read_text(encoding="utf-8")
                        except (OSError, UnicodeError) as exc:
                            errors.append(f"artifact[{index}]({role})不是可读UTF-8文本: {exc}")
                        else:
                            normalized = "".join(character for character in material_text if not character.isspace())
                            thresholds = {"screenplay": 200, "learning_sheet": 100, "board_plan": 80}
                            headings = [line for line in material_text.splitlines() if line.lstrip().startswith("#")]
                            if (
                                len(normalized) < thresholds[role]
                                or len(set(normalized.casefold())) < 15
                                or not headings
                            ):
                                errors.append(
                                    f"artifact[{index}]({role})文本物料内容不足：最低有效内容不足"
                                )
                            if role == "screenplay":
                                missing_pages = [page_id for page_id in source_page_ids if page_id not in material_text]
                                if missing_pages:
                                    errors.append(
                                        f"artifact[{index}](screenplay)未逐页锚定lesson页面: {missing_pages}"
                                    )
                                for marker in ("教师", "学生", "等待", "回应", "切页"):
                                    if marker not in material_text:
                                        errors.append(
                                            f"artifact[{index}](screenplay)缺真实剧本要素: {marker}"
                                        )
                            elif canonical_lines and not any(
                                (line[:4] if len(line) >= 4 else line) in material_text
                                for line in canonical_lines
                            ):
                                errors.append(f"artifact[{index}]({role})未锚定教材原文")
                if lesson_dir and artifact_path:
                    try:
                        artifact_path.relative_to(lesson_dir / "materials")
                    except ValueError:
                        errors.append(
                            f"artifact[{index}]({role or '?'})必须位于同一课目录的materials子目录"
                        )
                if role == "pptx" and artifact_path and artifact_path.is_file():
                    pptx_error = _pptx_ooxml_error(artifact_path)
                    if pptx_error:
                        errors.append(f"PPTX不是有效OOXML包（{pptx_error}）: {artifact.get('path')}")
            for duplicate in sorted({role for role in roles if roles.count(role) > 1}):
                errors.append(f"artifact role重复: {duplicate}")
            path_values = [path for _, _, path in artifact_paths]
            for duplicate_path in sorted({path for path in path_values if path_values.count(path) > 1}):
                duplicate_roles = [role for _, role, path in artifact_paths if path == duplicate_path]
                errors.append(f"多个物料角色不得共用同一文件: {duplicate_roles}")
            artifact_hashes = [
                str(artifact.get("sha256") or "")
                for artifact in manifest.get("artifacts") or []
                if str(artifact.get("sha256") or "")
            ]
            for duplicate_hash in sorted({value for value in artifact_hashes if artifact_hashes.count(value) > 1}):
                duplicate_roles = [
                    str(artifact.get("role") or "?")
                    for artifact in manifest.get("artifacts") or []
                    if artifact.get("sha256") == duplicate_hash
                ]
                errors.append(f"多个物料角色不得使用相同内容哈希: {duplicate_roles}")
            if lesson_dir and (lesson_dir / "materials").is_dir():
                registered_paths = {path for _, _, path in artifact_paths}
                actual_material_files = {
                    path.resolve()
                    for path in (lesson_dir / "materials").rglob("*")
                    if path.is_file() and (manifest_path is None or path.resolve() != manifest_path.resolve())
                }
                unregistered = sorted(actual_material_files - registered_paths)
                if unregistered:
                    errors.append(
                        "materials目录含未登记文件: "
                        + "、".join(path.relative_to(lesson_dir).as_posix() for path in unregistered)
                    )
            for role in sorted(REQUIRED_MATERIAL_ROLES - set(roles)):
                errors.append(f"materials manifest缺少必需物料角色: {role}")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("kind", choices=("design", "materials"))
    parser.add_argument("lock", type=Path)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        lock = json.loads(args.lock.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    errors = validate_design_lock(lock, args.root) if args.kind == "design" else validate_materials_lock(lock, args.root)
    for error in errors:
        print(f"[error] {error}")
    if errors:
        print(f"{args.kind}锁验证失败：{len(errors)}项")
        return 1
    print(f"{args.kind}锁验证通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
