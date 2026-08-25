#!/usr/bin/env python3
"""Validate the three-layer page-function audit for the 《氓》 V6 lesson.

The validator is deliberately side-effect free.  It treats the V5 diagnosis as
sealed evidence, the V5→V6 disposition as a separate closure, and the current
V6 structure as a fresh audit.  Physical PPTX/DOCX occurrences are accepted
only in release mode, after the structure has frozen.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import posixpath
import subprocess
import sys
import unicodedata
import zipfile
from datetime import datetime, timezone
from xml.etree import ElementTree
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


MODES = {"stage", "freeze-candidate", "freeze", "release"}
DOCUMENT_STATUSES = {
    "legacy_skeleton_pending_review", "structure_in_progress", "structure_frozen", "release_ready",
}
LEGACY_IDS = {f"S{number:03d}" for number in range(1, 128)}
LEGACY_AUDIT_SCOPES = {"pending", "learning_page", "event_carrier"}
GATE_IDS = {f"G{number}" for number in range(1, 7)}
GATE_STATUSES = {"pending", "pass", "fail", "deferred", "na"}
DECISIONS = {"保留", "合并", "移动", "重写", "删除"}
OPEN_STATUSES = {"pending", "deferred", "fail"}
UNIT_ROLES = {"输入", "体验", "澄清", "生成", "交流", "质询", "修订", "收束", "转场"}
EPISTEMIC_STATUSES = {"文本明写", "教材解释", "合理推断", "现代延伸", "课堂生成"}
PRIMARY_VISUAL_DUTIES = {
    "题名", "全文/章内整读", "原文批注", "文本比较/关系图", "动作小景",
    "意象点景", "活动界面", "现场共创", "信息路标",
}
REFERENCE_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*#[^#\s].+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
BUNDLE_COMPONENTS = {
    "structure_audit_bundle": (
        "structure_manifest", "current_release_audit", "legacy_effective_view", "legacy_disposition_closure",
    ),
    "release_audit_bundle": (
        "structure_audit_bundle", "release_artifact_manifest", "slide_occurrence_inventory",
        "document_page_inventory", "other_channel_inventory", "current_manifest",
    ),
    "release_attestation": (
        "release_audit_bundle", "release_review_ledger", "effective_release_review_view",
        "final_defect_closure_summary", "final_scorecard",
    ),
}
WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
V5_SNAPSHOT_PATH = "work/teaching/选择性必修下册/氓/06_氓_V5课程数据快照.json"
V5_BASELINE_MANIFEST_PATH = "work/teaching/选择性必修下册/氓/_v6_stage/baseline_manifest.json"
V5_SNAPSHOT_SHA256 = "23c920fc5e511f5e9cc1d8400efdb3b371d35b50f185e0bc7858e790c38631c3"
V6_AUDIT_INDEX_PATH = "scripts/meng_v6/audit/index.json"
SKELETON_BATCHES = (
    ("A", 1, 16, "隐藏导航、封面、导入、三问、首次听读、最小支架"),
    ("B1", 17, 27, "第一章及章内活动"),
    ("B2", 28, 39, "模块承接、第二章及章内活动"),
    ("B3", 40, 50, "第三章及章内活动"),
    ("B4", 51, 62, "模块承接、第四章及章内活动"),
    ("B5", 63, 73, "第五章及章内活动"),
    ("B6", 74, 85, "模块承接、第六章及章内活动"),
    ("C1", 86, 95, "全文回读、初读修订、问题一"),
    ("C2", 96, 101, "问题二"),
    ("C3", 102, 112, "问题三、责任/阻力、第一章回看"),
    ("C4", 113, 116, "婚姻圆桌"),
    ("D", 117, 127, "知识检索、收纳、终读、退出条"),
)


def diagnostic(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def canonical_sha256(value: Any) -> str:
    """Hash the canonical JSON representation used by the audit fixtures."""
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def normalize_canonical(value: Any, *, field: str | None = None) -> Any:
    """Normalize text and unordered audit sets without hiding semantic order."""
    if isinstance(value, str):
        normalized = unicodedata.normalize("NFC", value.replace("\r\n", "\n").replace("\r", "\n"))
        if field and (field.endswith("path") or field.endswith("_path")):
            normalized = normalized.replace("\\", "/")
            path = Path(normalized)
            if path.is_absolute():
                try:
                    normalized = path.resolve().relative_to(WORKSPACE_ROOT).as_posix()
                except ValueError:
                    normalized = f"__OUTSIDE_WORKSPACE__/{path.name}"
        return normalized
    if isinstance(value, dict):
        return {
            normalize_canonical(str(key)): normalize_canonical(item, field=str(key))
            for key, item in value.items()
            if key not in {"generated_at", "absolute_cache_path"}
        }
    if isinstance(value, list):
        normalized = [normalize_canonical(item) for item in value]
        if field in {
            "legacy_ids", "reviewer_ids", "defect_ids", "closed_p0_p1_p2_ids", "legacy_source_refs",
        }:
            return sorted(normalized, key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True))
        return normalized
    return value


def audit_sha256(value: Any) -> str:
    return canonical_sha256(normalize_canonical(value))


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json_receipt(path_value: Any) -> tuple[dict[str, Any] | None, str | None]:
    path = resolve_source_path(path_value)
    if path is None:
        return None, None
    try:
        return json.loads(path.read_text(encoding="utf-8")), file_sha256(path)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None, None


def parse_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(timezone.utc)
    except ValueError:
        return None


def resolve_source_path(value: Any) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    path = Path(value.replace("\\", "/"))
    if not path.is_absolute():
        path = WORKSPACE_ROOT / path
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(WORKSPACE_ROOT)
        return resolved
    except (OSError, RuntimeError):
        return None
    except ValueError:
        return None


def inspect_pptx(path: Path) -> list[dict[str, Any]]:
    """Read V6 slide identity, notes events and asset bindings from OOXML."""
    with zipfile.ZipFile(path) as package:
        package_names = set(package.namelist())
        presentation_name = "ppt/presentation.xml"
        presentation_rels_name = "ppt/_rels/presentation.xml.rels"
        if presentation_name not in package_names or presentation_rels_name not in package_names:
            raise KeyError("PPTX presentation order relationships are missing")
        rel_root = ElementTree.fromstring(package.read(presentation_rels_name))
        rel_targets = {
            relation.attrib.get("Id"): posixpath.normpath(posixpath.join("ppt", relation.attrib.get("Target", "")))
            for relation in list(rel_root)
        }
        presentation_root = ElementTree.fromstring(package.read(presentation_name))
        ordered_slides: list[tuple[str, bool]] = []
        for element in presentation_root.iter():
            if element.tag.rsplit("}", 1)[-1] != "sldId":
                continue
            relationship_id = next(
                (value for key, value in element.attrib.items() if key.endswith("}id") or key == "r:id"),
                None,
            )
            if relationship_id is not None:
                visible = not any(
                    key.rsplit("}", 1)[-1] == "show" and str(value).lower() in {"0", "false", "off"}
                    for key, value in element.attrib.items()
                )
                ordered_slides.append((relationship_id, visible))
        names = [
            rel_targets[rid] for rid, _ in ordered_slides
            if rid in rel_targets and "/slides/" in rel_targets[rid]
        ]
        if (len(names) != len(ordered_slides) or len(names) != len(set(names))
                or any(name not in package_names for name in names)):
            raise KeyError("PPTX presentation order is invalid")
        observations: list[dict[str, Any]] = []
        for physical_index, (name, (_, presentation_visible)) in enumerate(zip(names, ordered_slides), start=1):
            payload = package.read(name).decode("utf-8", errors="replace")
            slide_root = ElementTree.fromstring(package.read(name))
            slide_visible = not any(
                key.rsplit("}", 1)[-1] == "show" and str(value).lower() in {"0", "false", "off"}
                for key, value in slide_root.attrib.items()
            )
            page_ids = re.findall(r"V6_PAGE_ID:([Nn]\d{3})", payload)
            asset_markers = re.findall(r"V6_ASSET_IDS:([A-Za-z0-9_,.-]*)", payload)
            asset_ids = sorted([] if not asset_markers or not asset_markers[0] else asset_markers[0].split(","))
            relationship_markers = re.findall(r"V6_ASSET_RELATIONSHIPS:([A-Za-z0-9_.,@-]*)", payload)
            asset_relationships = {}
            for marker in ([] if not relationship_markers or not relationship_markers[0] else relationship_markers[0].split(",")):
                asset_id, separator, relationship_id = marker.partition("@")
                if not separator or asset_id in asset_relationships.values() or relationship_id in asset_relationships:
                    raise KeyError("PPTX asset relationship marker is invalid")
                asset_relationships[relationship_id] = asset_id
            rel_path = f"ppt/slides/_rels/{Path(name).name}.rels"
            notes_event_ids: list[str] = []
            image_relationships = 0
            media_sha256: list[str] = []
            media_bindings: list[dict[str, str]] = []
            if rel_path in package.namelist():
                rel_root = ElementTree.fromstring(package.read(rel_path))
                for relation in list(rel_root):
                    rel_type = str(relation.attrib.get("Type", ""))
                    target = str(relation.attrib.get("Target", ""))
                    if rel_type.endswith("/image"):
                        image_relationships += 1
                        media_name = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
                        if media_name not in package_names:
                            raise KeyError(f"missing image relationship target: {media_name}")
                        media_hash = hashlib.sha256(package.read(media_name)).hexdigest()
                        media_sha256.append(media_hash)
                        media_bindings.append({
                            "asset_id": asset_relationships.get(str(relation.attrib.get("Id", "")), ""),
                            "relationship_id": str(relation.attrib.get("Id", "")),
                            "media_target": media_name,
                            "media_sha256": media_hash,
                        })
                    if rel_type.endswith("/notesSlide"):
                        notes_name = posixpath.normpath(posixpath.join(posixpath.dirname(name), target))
                        if notes_name not in package_names:
                            raise KeyError(f"missing notes relationship target: {notes_name}")
                        notes_payload = package.read(notes_name).decode("utf-8", errors="replace")
                        notes_event_ids.extend(re.findall(r"V6_EVENT_ID:([A-Za-z][A-Za-z0-9_]*)", notes_payload))
            if set(asset_relationships.values()) != set(asset_ids) or any(not item.get("asset_id") for item in media_bindings):
                raise KeyError("PPTX asset IDs do not map one-to-one to image relationships")
            observations.append({
                "physical_index": physical_index,
                "page_ids": page_ids,
                "hidden": not (presentation_visible and slide_visible),
                "notes_event_ids": notes_event_ids,
                "asset_ids": asset_ids,
                "media_sha256": sorted(media_sha256),
                "media_bindings": sorted(media_bindings, key=lambda item: item["relationship_id"]),
                "image_relationship_count": image_relationships,
            })
        return observations


def inspect_office_region(path: Path, artifact_type: str, field_or_region: Any) -> str | None:
    """Extract one explicitly marked student-exposure region from a real source."""
    if not isinstance(field_or_region, str) or not field_or_region:
        return None
    try:
        if artifact_type == "docx":
            with zipfile.ZipFile(path) as package:
                root = ElementTree.fromstring(package.read("word/document.xml"))
                text = "".join(root.itertext())
        elif artifact_type == "pptx":
            with zipfile.ZipFile(path) as package:
                parts = [
                    ElementTree.fromstring(package.read(name))
                    for name in sorted(package.namelist())
                    if (name.startswith("ppt/slides/slide") or name.startswith("ppt/notesSlides/notesSlide"))
                    and name.endswith(".xml")
                ]
                text = "".join("".join(part.itertext()) for part in parts)
        else:
            text = path.read_text(encoding="utf-8")
    except (OSError, KeyError, UnicodeDecodeError, zipfile.BadZipFile, ElementTree.ParseError):
        return None
    marker = f"V6_REGION:{field_or_region}::"
    start = text.find(marker)
    if start < 0:
        return None
    start += len(marker)
    end = text.find("::V6_END_REGION", start)
    if end < 0 or text.find(marker, end + 1) >= 0:
        return None
    content = unicodedata.normalize("NFC", text[start:end].replace("\r\n", "\n").replace("\r", "\n"))
    return content if content.strip() else None


def inspect_channel_content_hash(path: Path, artifact_type: str, field_or_region: Any) -> str | None:
    if artifact_type == "audio":
        if field_or_region != "__WHOLE_FILE__":
            return None
        return file_sha256(path)
    content = inspect_office_region(path, artifact_type, field_or_region)
    return hashlib.sha256(content.encode("utf-8")).hexdigest() if content is not None else None


def release_deletion_source_state(
    artifact_manifest: Any,
    slides: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    channels: list[dict[str, Any]],
    approved_assets: Any,
    signatures: list[Any],
    detector_configuration: Any,
) -> dict[str, Any]:
    artifacts = as_list(artifact_manifest.get("artifacts")) if isinstance(artifact_manifest, dict) else []
    return {
        "office_sources": [
            {
                "artifact_id": item.get("artifact_id"), "type": item.get("type"),
                "source_sha256": item.get("source_sha256"), "page_count": item.get("page_count"),
                "byte_count": item.get("byte_count"),
            }
            for item in artifacts if isinstance(item, dict)
        ],
        "slide_renders": [
            {"occurrence_ref": item.get("occurrence_ref"), "render_sha256": item.get("render_sha256")}
            for item in slides
        ],
        "document_renders": [
            {
                "artifact_id": item.get("artifact_id"), "doc_page_index": item.get("doc_page_index"),
                "render_sha256": item.get("render_sha256"),
            }
            for item in documents
        ],
        "other_channels": [
            {
                "channel_ref": item.get("channel_ref"), "source_sha256": item.get("source_sha256"),
                "field_or_region": item.get("field_or_region"), "content_sha256": item.get("content_sha256"),
                "student_exposure_order": item.get("student_exposure_order"),
                "owner_event_id": item.get("owner_event_id"),
            }
            for item in channels
        ],
        "approved_assets_manifest_sha256": audit_sha256(approved_assets) if isinstance(approved_assets, dict) else None,
        "forbidden_reappearance_signatures": signatures,
        "detector_configuration": detector_configuration,
    }


def pdf_page_count(path: Path) -> int | None:
    try:
        result = subprocess.run(
            ["pdfinfo", str(path)], check=True, capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None
    match = re.search(r"^Pages:\s*(\d+)\s*$", result.stdout, re.MULTILINE)
    return int(match.group(1)) if match else None


def build_bundle(bundle_type: str, components: dict[str, Any]) -> dict[str, Any]:
    names = BUNDLE_COMPONENTS[bundle_type]
    component_hashes = [
        {"component_name": name, "component_sha256": audit_sha256(components[name])}
        for name in names
    ]
    body = {"bundle_schema_version": 1, "bundle_type": bundle_type, "components": component_hashes}
    return {**body, "bundle_sha256": audit_sha256(body)}


def validate_bundle(bundle: Any, bundle_type: str, sources: dict[str, Any], path: str) -> list[dict[str, str]]:
    if not isinstance(bundle, dict):
        return [diagnostic("AUDIT_BUNDLE_MISSING", path, f"{bundle_type} is missing")]
    required_names = BUNDLE_COMPONENTS[bundle_type]
    if any(name not in sources for name in required_names):
        return [diagnostic("AUDIT_BUNDLE_COMPONENT_MISSING", path, "required bundle source component is missing")]
    expected = build_bundle(bundle_type, sources)
    if bundle != expected:
        return [diagnostic("AUDIT_BUNDLE_HASH_MISMATCH", path, "bundle does not match independently canonicalized source components")]
    return []


def derive_legacy_effective_view(document: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Apply reviewed amendments to a copy-like JSON round trip of sealed pages."""
    view = json.loads(json.dumps(as_list(document.get("legacy_initial_audit")), ensure_ascii=False))
    by_id = dict_index(view, "page_id")
    errors: list[dict[str, str]] = []
    for index, amendment in enumerate(as_list(document.get("seal_amendments"))):
        if not isinstance(amendment, dict):
            continue
        pointer = str(amendment.get("claim_pointer", ""))
        if "#" not in pointer:
            errors.append(diagnostic("LEGACY_AMENDMENT_POINTER_INVALID", f"seal_amendments[{index}].claim_pointer", "claim pointer must use legacy-id#field"))
            continue
        legacy_id, field_path = pointer.split("#", 1)
        target: Any = by_id.get(legacy_id)
        parts = [part for part in field_path.split(".") if part]
        for part in parts[:-1]:
            if isinstance(target, dict):
                target = target.get(part)
            else:
                target = None
                break
        if not parts or not isinstance(target, dict) or parts[-1] not in target or target.get(parts[-1]) != amendment.get("old_claim"):
            errors.append(diagnostic("LEGACY_AMENDMENT_POINTER_INVALID", f"seal_amendments[{index}].claim_pointer", "amendment old claim does not match the effective view"))
            continue
        target[parts[-1]] = amendment.get("new_claim")
    return view, errors


def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict, tuple, set)):
        return bool(value)
    return True


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def dict_index(items: Iterable[Any], key: str) -> dict[str, dict[str, Any]]:
    return {
        str(item[key]): item
        for item in items
        if isinstance(item, dict) and nonempty(item.get(key))
    }


def resolve_field_reference(reference: Any, objects: dict[str, Any]) -> Any:
    if not isinstance(reference, str) or "#" not in reference:
        return None
    object_id, field_path = reference.split("#", 1)
    current: Any = objects.get(object_id)
    for part in field_path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return None
    return current


def references_resolve(references: Any, objects: dict[str, Any]) -> bool:
    refs = as_list(references)
    return bool(refs) and all(nonempty(resolve_field_reference(reference, objects)) for reference in refs)


def duplicates(values: Iterable[Any]) -> set[Any]:
    return {value for value, count in Counter(values).items() if count > 1}


def node_sets(inventory: Any) -> tuple[set[str], set[str]]:
    if not isinstance(inventory, dict):
        return set(), set()
    pages = {
        str(item.get("node_id"))
        for item in as_list(inventory.get("pages"))
        if isinstance(item, dict) and nonempty(item.get("node_id"))
    }
    events = {
        str(item.get("node_id"))
        for item in as_list(inventory.get("events"))
        if isinstance(item, dict) and nonempty(item.get("node_id"))
    }
    return pages, events


def gate_index(owner: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(owner, dict):
        return {}
    return dict_index(as_list(owner.get("gates")), "gate_id")


def review_defect_ids(review: Any) -> set[str]:
    result: set[str] = set()
    if not isinstance(review, dict):
        return result
    for key in ("self_review", "student_reception", "visual"):
        record = review.get(key)
        if isinstance(record, dict):
            result.update(str(item) for item in as_list(record.get("defect_ids")))
    return result


def validate_gate_collection(
    owner: Any,
    path: str,
    expected: set[str],
    *,
    legacy: bool = False,
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    gates = as_list(owner.get("gates")) if isinstance(owner, dict) else []
    ids = [item.get("gate_id") for item in gates if isinstance(item, dict)]
    if set(ids) != expected or len(ids) != len(expected):
        errors.append(diagnostic("AUDIT_GATE_SET_INVALID", f"{path}.gates", "gate set is incomplete or duplicated"))
    for index, gate in enumerate(gates):
        gate_path = f"{path}.gates[{index}]"
        if not isinstance(gate, dict):
            errors.append(diagnostic("AUDIT_GATE_INVALID", gate_path, "gate must be an object"))
            continue
        status = gate.get("gate_status")
        if status not in GATE_STATUSES:
            errors.append(diagnostic("AUDIT_GATE_STATUS_INVALID", f"{gate_path}.gate_status", "unknown gate status"))
        if legacy and status == "deferred":
            errors.append(diagnostic("LEGACY_DEFERRED_FORBIDDEN", gate_path, "sealed legacy diagnosis cannot defer to V6"))
        if status == "fail" and not nonempty(gate.get("failure_code")):
            errors.append(diagnostic("AUDIT_FAILURE_CODE_MISSING", f"{gate_path}.failure_code", "failed gate needs a failure code"))
        if status == "pending":
            if as_list(gate.get("evidence_refs")) or nonempty(gate.get("reviewer")) or nonempty(gate.get("reviewed_at")):
                errors.append(diagnostic("AUDIT_PENDING_HAS_EVIDENCE", gate_path, "pending gate cannot claim completed evidence"))
        elif status in {"pass", "fail", "deferred", "na"}:
            refs = gate.get("evidence_refs")
            if not isinstance(refs, list):
                errors.append(diagnostic("AUDIT_EVIDENCE_INVALID", f"{gate_path}.evidence_refs", "evidence refs must be a list"))
            elif status not in {"deferred", "na"} and not refs:
                errors.append(diagnostic("AUDIT_EVIDENCE_MISSING", f"{gate_path}.evidence_refs", "completed gate needs evidence"))
            for ref_index, reference in enumerate(as_list(refs)):
                if not isinstance(reference, str) or not REFERENCE_RE.fullmatch(reference):
                    errors.append(diagnostic("AUDIT_EVIDENCE_INVALID", f"{gate_path}.evidence_refs[{ref_index}]", "use ID#field evidence refs"))
    return errors


def validate_review(review: Any, path: str, strict: bool) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if not isinstance(review, dict):
        return [diagnostic("AUDIT_REVIEW_INVALID", path, "review status must be an object")]
    records: list[dict[str, Any]] = []
    for key in ("self_review", "student_reception", "visual"):
        record = review.get(key)
        if not isinstance(record, dict):
            errors.append(diagnostic("AUDIT_REVIEW_INVALID", f"{path}.{key}", "review record is missing"))
            continue
        records.append(record)
        if record.get("status") not in {"pending", "pass", "fail"}:
            errors.append(diagnostic("AUDIT_REVIEW_INVALID", f"{path}.{key}.status", "unknown review status"))
        elif record.get("status") in {"pass", "fail"} and (
            not nonempty(record.get("reviewer")) or not nonempty(record.get("reviewed_at"))
        ):
            errors.append(diagnostic("AUDIT_REVIEW_INVALID", f"{path}.{key}", "completed review needs identity and time"))
    completed = [str(item.get("reviewer")) for item in records if item.get("status") in {"pass", "fail"}]
    if len(completed) != len(set(completed)):
        errors.append(diagnostic("AUDIT_REVIEW_NOT_INDEPENDENT", path, "the three review roles need distinct identities"))
    student = review.get("student_reception", {})
    visual = review.get("visual", {})
    statuses = [item.get("status") for item in records]
    disagreement = {student.get("status"), visual.get("status")} == {"pass", "fail"}
    adjudication = review.get("adjudication")
    adjudicated_status: str | None = None
    if disagreement and isinstance(adjudication, dict):
        adjudicator = adjudication.get("reviewer")
        if (adjudication.get("status") in {"pass", "fail"}
                and nonempty(adjudicator) and adjudicator not in set(completed)
                and nonempty(adjudication.get("reviewed_at"))
                and nonempty(adjudication.get("reason"))
                and as_list(adjudication.get("evidence_refs"))):
            adjudicated_status = str(adjudication.get("status"))
        else:
            errors.append(diagnostic("AUDIT_ADJUDICATION_INVALID", f"{path}.adjudication", "adjudication needs a fresh reviewer, reason, time and evidence"))
    if disagreement and adjudicated_status is None:
        expected_consensus = "blocked_for_adjudication"
    elif adjudicated_status is not None:
        expected_consensus = "passed" if adjudicated_status == "pass" else "failed"
    elif any(status == "pending" for status in statuses) or len(statuses) != 3:
        expected_consensus = "pending"
    elif any(status == "fail" for status in statuses):
        expected_consensus = "failed"
    else:
        expected_consensus = "passed"
    if review.get("consensus") != expected_consensus:
        errors.append(diagnostic("AUDIT_REVIEW_CONSENSUS_INVALID", f"{path}.consensus", "consensus must be mechanically derived from independent records"))
    if strict and expected_consensus != "passed":
        errors.append(diagnostic("CURRENT_REVIEW_OPEN", f"{path}.consensus", "freeze/release needs passed consensus"))
    return errors


def validate_legacy_layer(document: dict[str, Any], mode: str) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    legacy = as_list(document.get("legacy_initial_audit"))
    skeleton_status = document.get("document_status") == "legacy_skeleton_pending_review"
    if (skeleton_status or document.get("pages") is not None) and document.get("pages") != legacy:
        errors.append(diagnostic("LEGACY_PAGE_VIEW_MISMATCH", "pages", "top-level pages must be the exact derived view of legacy_initial_audit"))
    elif "pages" not in document and (
        skeleton_status
        or (mode == "stage" and len(legacy) == 127 and not current_nodes(document)[0] and not current_nodes(document)[1])
    ):
        errors.append(diagnostic("LEGACY_PAGE_VIEW_MISMATCH", "pages", "Task 3 skeleton requires the exact derived pages view"))
    legacy_ids = [item.get("page_id") for item in legacy if isinstance(item, dict)]
    if set(legacy_ids) != LEGACY_IDS or len(legacy_ids) != 127:
        errors.append(diagnostic("LEGACY_ID_SET_INVALID", "legacy_initial_audit", "legacy audit must cover S001-S127 exactly once"))
    by_id = dict_index(legacy, "page_id")
    legacy_events = dict_index(as_list(document.get("legacy_event_evidence")), "legacy_event_id")
    for index, page in enumerate(legacy):
        path = f"legacy_initial_audit[{index}]"
        errors.extend(validate_gate_collection(page, path, GATE_IDS, legacy=True))
        errors.extend(validate_review(page.get("review_status") if isinstance(page, dict) else None, f"{path}.review_status", strict=False))
        if isinstance(page, dict):
            elements = as_list(page.get("content_elements"))
            if not elements or any(
                not isinstance(element, dict)
                or not {"element_id", "kind", "source_field"}.issubset(element)
                or not nonempty(element.get("element_id"))
                or element.get("kind") not in {"function", "text", "visual", "layout", "event", "student_reception"}
                or str(element.get("source_field")) not in page
                for element in elements
            ):
                errors.append(diagnostic("LEGACY_CONTENT_INVENTORY_INVALID", f"{path}.content_elements", "sealed legacy page needs a source-grounded content-element inventory"))
            scope = page.get("audit_scope")
            if scope not in LEGACY_AUDIT_SCOPES:
                errors.append(diagnostic("LEGACY_AUDIT_SCOPE_INVALID", f"{path}.audit_scope", "legacy page audit scope is invalid"))
            na_gates = {gate_id for gate_id, item in gate_index(page).items() if item.get("gate_status") == "na"}
            if na_gates:
                owner_id = str(page.get("owner_event_id"))
                owner = legacy_events.get(owner_id)
                if scope != "event_carrier" or not na_gates.issubset({"G4", "G5"}):
                    errors.append(diagnostic("LEGACY_NA_MISUSE", f"{path}.gates", "only legacy carrier G4/G5 may use na"))
                elif owner is None or page.get("page_id") not in as_list(owner.get("carrier_ids")):
                    errors.append(diagnostic("LEGACY_EVENT_OWNER_MISMATCH", f"{path}.owner_event_id", "legacy carrier must borrow its same-layer event"))
                else:
                    for gate_id in na_gates:
                        event_gate = owner.get("gate_4" if gate_id == "G4" else "gate_5")
                        expected_ref = f"{owner_id}#{'gate_4' if gate_id == 'G4' else 'gate_5'}"
                        if not isinstance(event_gate, dict) or event_gate.get("gate_status") != "pass" or expected_ref not in as_list(gate_index(page)[gate_id].get("evidence_refs")):
                            errors.append(diagnostic("LEGACY_EVENT_EVIDENCE_INVALID", f"{path}.{gate_id}", "legacy carrier na needs the owning legacy event's passed gate"))

    for index, event in enumerate(as_list(document.get("legacy_event_evidence"))):
        path = f"legacy_event_evidence[{index}]"
        if not isinstance(event, dict):
            errors.append(diagnostic("LEGACY_EVENT_EVIDENCE_INVALID", path, "legacy event must be an object"))
            continue
        required_event_fields = {
            "legacy_event_id", "learning_unit", "carrier_ids", "inputs", "actions", "artifacts",
            "observable_change", "next_use_evidence", "gate_4", "gate_5", "reviewer_ids", "reviewed_at",
        }
        if not required_event_fields.issubset(event):
            errors.append(diagnostic("LEGACY_EVENT_EVIDENCE_INVALID", path, "legacy event evidence is incomplete"))
        reviewers = [str(item) for item in as_list(event.get("reviewer_ids"))]
        if len(reviewers) != 2 or len(set(reviewers)) != 2:
            errors.append(diagnostic("LEGACY_EVENT_EVIDENCE_INVALID", f"{path}.reviewer_ids", "legacy event needs two independent reviewers"))
        for gate_name in ("gate_4", "gate_5"):
            gate = event.get(gate_name)
            if not isinstance(gate, dict) or gate.get("gate_status") not in {"pass", "fail"}:
                errors.append(diagnostic("LEGACY_EVENT_EVIDENCE_INVALID", f"{path}.{gate_name}", "legacy event gate must be independently reviewed"))
        for carrier_id in as_list(event.get("carrier_ids")):
            carrier = by_id.get(str(carrier_id))
            if carrier is None or carrier.get("audit_scope") != "event_carrier" or carrier.get("owner_event_id") != event.get("legacy_event_id"):
                errors.append(diagnostic("LEGACY_EVENT_OWNER_MISMATCH", f"{path}.carrier_ids", "legacy event and carriers must reference each other"))

    seals = as_list(document.get("initial_audit_seals"))
    sealed_ids: list[str] = []
    for index, seal in enumerate(seals):
        path = f"initial_audit_seals[{index}]"
        if not isinstance(seal, dict):
            errors.append(diagnostic("LEGACY_SEAL_INVALID", path, "seal must be an object"))
            continue
        ids = [str(item) for item in as_list(seal.get("legacy_ids"))]
        sealed_ids.extend(ids)
        reviewers = [str(item) for item in as_list(seal.get("reviewer_ids"))]
        if len(reviewers) != 2 or len(set(reviewers)) != 2 or str(seal.get("author_id")) in set(reviewers):
            errors.append(diagnostic("LEGACY_SEAL_REVIEWERS_INVALID", f"{path}.reviewer_ids", "seal needs two independent reviewers"))
        source = [item for item in legacy if isinstance(item, dict) and item.get("page_id") in set(ids)]
        if len(source) != len(ids) or seal.get("source_sha256") != canonical_sha256(source):
            errors.append(diagnostic("LEGACY_SEAL_SOURCE_HASH_MISMATCH", f"{path}.source_sha256", "sealed legacy source changed or coverage is invalid"))
        sealed_events = [
            event for event in as_list(document.get("legacy_event_evidence"))
            if isinstance(event, dict) and set(as_list(event.get("carrier_ids"))) & set(ids)
        ]
        if seal.get("legacy_event_evidence_sha256") != canonical_sha256(sealed_events):
            errors.append(diagnostic("LEGACY_SEAL_EVENT_HASH_MISMATCH", f"{path}.legacy_event_evidence_sha256", "seal must bind same-layer legacy event evidence"))
        seal_body = {key: value for key, value in seal.items() if key != "seal_hash"}
        if seal.get("seal_hash") != canonical_sha256(seal_body):
            errors.append(diagnostic("LEGACY_SEAL_HASH_MISMATCH", f"{path}.seal_hash", "seal hash does not match its canonical body"))
        evidence_ids = {
            item.get("legacy_id") for item in as_list(seal.get("review_evidence")) if isinstance(item, dict)
        }
        if evidence_ids != set(ids):
            errors.append(diagnostic("LEGACY_SEAL_EVIDENCE_SET_MISMATCH", f"{path}.review_evidence", "every sealed legacy page needs review evidence"))
    if mode in {"freeze-candidate", "freeze", "release"} and (set(sealed_ids) != LEGACY_IDS or len(sealed_ids) != 127):
        errors.append(diagnostic("LEGACY_SEAL_COVERAGE_INVALID", "initial_audit_seals", "frozen legacy diagnosis must be sealed exactly once"))

    # Amendments are append-only: one linear predecessor chain, two reviewers,
    # and a self-authenticating hash.  The effective-view producer may consume
    # their payload later; this validator prevents silent seal replacement.
    amendments = as_list(document.get("seal_amendments"))
    amendments_by_seal: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in amendments:
        if isinstance(item, dict):
            amendments_by_seal[str(item.get("target_seal_id"))].append(item)
    seal_hashes = {str(item.get("seal_id")): str(item.get("seal_hash")) for item in seals if isinstance(item, dict)}
    for seal_id, chain in amendments_by_seal.items():
        expected_previous = seal_hashes.get(seal_id)
        seen_hashes: set[str] = set()
        for index, amendment in enumerate(chain):
            path = f"seal_amendments[{index}]"
            reviewers = [str(item) for item in as_list(amendment.get("reviewer_ids"))]
            if len(reviewers) != 2 or len(set(reviewers)) != 2 or str(amendment.get("author_id")) in set(reviewers):
                errors.append(diagnostic("LEGACY_AMENDMENT_REVIEWERS_INVALID", f"{path}.reviewer_ids", "amendment needs two independent reviewers"))
            if amendment.get("previous_effective_hash") != expected_previous:
                errors.append(diagnostic("LEGACY_AMENDMENT_CHAIN_INVALID", f"{path}.previous_effective_hash", "amendment chain is broken or forked"))
            body = {key: value for key, value in amendment.items() if key != "amendment_hash"}
            amendment_hash = str(amendment.get("amendment_hash"))
            if amendment_hash != canonical_sha256(body) or amendment_hash in seen_hashes:
                errors.append(diagnostic("LEGACY_AMENDMENT_HASH_INVALID", f"{path}.amendment_hash", "amendment hash is invalid or repeated"))
            seen_hashes.add(amendment_hash)
            expected_previous = amendment_hash

    defects = dict_index(as_list(document.get("defect_registry")), "defect_id")
    relevant_defects: dict[str, set[str]] = defaultdict(set)
    for defect_id, defect in defects.items():
        if defect.get("severity") in {"P0", "P1", "P2"} and defect.get("object_ref") in LEGACY_IDS:
            relevant_defects[str(defect.get("object_ref"))].add(defect_id)
    effective_view, effective_errors = derive_legacy_effective_view(document)
    errors.extend(effective_errors)
    if document.get("legacy_effective_view") != effective_view:
        errors.append(diagnostic("LEGACY_EFFECTIVE_VIEW_MISMATCH", "legacy_effective_view", "effective view must be derived from sealed baseline plus linear amendments"))
    if document.get("effective_legacy_hash") != audit_sha256(effective_view):
        errors.append(diagnostic("LEGACY_EFFECTIVE_HASH_MISMATCH", "effective_legacy_hash", "effective legacy hash must be recomputed from the derived view"))
    effective_by_id = dict_index(effective_view, "page_id")
    for legacy_id, page in effective_by_id.items():
        review_ids = review_defect_ids(page.get("review_status"))
        registered_ids = relevant_defects.get(legacy_id, set())
        if not review_ids.issubset(set(defects)) or review_ids != registered_ids:
            errors.append(diagnostic("LEGACY_DEFECT_REGISTRY_MISMATCH", f"legacy:{legacy_id}", "effective-view P0-P2 review defects and registry must match"))
    return errors


def validate_stage_skeleton_sources(document: dict[str, Any], mode: str) -> list[dict[str, str]]:
    """Rebuild the pending Task 3 view from independently read, immutable sources."""
    valid_current_pages, valid_current_events = current_nodes(document)
    empty_current = not valid_current_pages and not valid_current_events
    task3_shape = len(as_list(document.get("legacy_initial_audit"))) == 127 and empty_current
    if mode != "stage" or not (
        document.get("document_status") == "legacy_skeleton_pending_review" or task3_shape
    ):
        return []

    problems: list[str] = []

    def load_json(relative_path: str, label: str) -> tuple[dict[str, Any] | None, Path | None]:
        path = resolve_source_path(relative_path)
        if path is None:
            problems.append(f"{label}文件不存在或越出工作区")
            return None, None
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            problems.append(f"{label}不是可读UTF-8 JSON")
            return None, path
        if not isinstance(value, dict):
            problems.append(f"{label}顶层必须是对象")
            return None, path
        return value, path

    source = document.get("legacy_source")
    if not isinstance(source, dict):
        return [diagnostic(
            "LEGACY_STAGE_SOURCE_MISMATCH", "legacy_source",
            "Task 3骨架必须绑定V5快照、基线清单、索引和24个批次源",
        )]
    if source.get("path") != V5_SNAPSHOT_PATH or source.get("index_path") != V6_AUDIT_INDEX_PATH:
        problems.append("总表来源路径不是冻结的V5快照与V6审计索引")

    snapshot, snapshot_path = load_json(V5_SNAPSHOT_PATH, "V5课程快照")
    baseline, _ = load_json(V5_BASELINE_MANIFEST_PATH, "V5基线清单")
    index, index_path = load_json(V6_AUDIT_INDEX_PATH, "V6审计索引")
    if snapshot is None or snapshot_path is None or baseline is None or index is None or index_path is None:
        return [diagnostic(
            "LEGACY_STAGE_SOURCE_MISMATCH", "legacy_source",
            "; ".join(problems),
        )]

    snapshot_hash = file_sha256(snapshot_path)
    if snapshot_hash != V5_SNAPSHOT_SHA256:
        problems.append("实际V5课程快照不等于冻结SHA-256")
    baseline_files = as_list(baseline.get("files"))
    baseline_matches = [
        item for item in baseline_files
        if isinstance(item, dict) and item.get("path") == V5_SNAPSHOT_PATH
    ]
    if (baseline.get("file_count") != len(baseline_files) or len(baseline_matches) != 1
            or baseline_matches[0].get("sha256") != snapshot_hash):
        problems.append("V5基线清单没有唯一、正确绑定实际课程快照")
    if source.get("sha256") != snapshot_hash:
        problems.append("总表legacy_source.sha256与实际课程快照不一致")

    index_hash = file_sha256(index_path)
    if source.get("index_sha256") != index_hash:
        problems.append("总表legacy_source.index_sha256与实际索引文件不一致")
    if index.get("source_snapshot_sha256") != snapshot_hash:
        problems.append("索引没有绑定实际V5课程快照")

    slides = snapshot.get("slides")
    expected_ids = [f"S{number:03d}" for number in range(1, 128)]
    if (not isinstance(slides, list) or len(slides) != 127
            or [item.get("id") for item in slides if isinstance(item, dict)] != expected_ids):
        problems.append("实际V5课程快照没有按序完整覆盖S001—S127")
        slides = []

    expected_batch_specs = [
        {
            "batch_id": batch_id,
            "range": f"S{start:03d}—S{end:03d}",
            "content": content,
            "initial_source": f"scripts/meng_v6/audit/{batch_id}_initial.json",
            "disposition_source": f"scripts/meng_v6/audit/{batch_id}_disposition.json",
            "page_count": end - start + 1,
        }
        for batch_id, start, end, content in SKELETON_BATCHES
    ]
    index_batches = as_list(index.get("batches"))
    if (index.get("schema_version") != "1.0" or index.get("page_count") != 127
            or index.get("legacy_ids") != expected_ids or len(index_batches) != len(expected_batch_specs)):
        problems.append("V6审计索引的版本、页集或批次数量错误")

    expected_pages: list[dict[str, Any]] = []
    merged_initial_pages: list[dict[str, Any]] = []
    for spec, batch_tuple in zip(expected_batch_specs, SKELETON_BATCHES):
        batch_id, start, end, content = batch_tuple
        matching = [item for item in index_batches if isinstance(item, dict) and item.get("batch_id") == batch_id]
        if len(matching) != 1:
            problems.append(f"批次{batch_id}在索引中缺失或重复")
            continue
        indexed = matching[0]
        if any(indexed.get(field) != spec[field] for field in spec):
            problems.append(f"批次{batch_id}的范围、内容、路径或页数与冻结合同不一致")
        initial, initial_path = load_json(spec["initial_source"], f"批次{batch_id}初诊源")
        disposition, disposition_path = load_json(spec["disposition_source"], f"批次{batch_id}处置源")
        if initial is None or initial_path is None or disposition is None or disposition_path is None:
            continue
        initial_hash = file_sha256(initial_path)
        disposition_hash = file_sha256(disposition_path)
        if indexed.get("initial_sha256") != initial_hash or indexed.get("disposition_sha256") != disposition_hash:
            problems.append(f"批次{batch_id}源文件SHA-256与索引不一致")
        if initial.get("schema_version") != "1.0" or initial.get("batch_id") != batch_id:
            problems.append(f"批次{batch_id}初诊源身份错误")
        if (initial.get("range") != spec["range"] or initial.get("source_snapshot_sha256") != snapshot_hash
                or initial.get("status") != "pending_review"):
            problems.append(f"批次{batch_id}初诊源不是待审且未正确绑定快照")
        if (disposition.get("schema_version") != "1.0" or disposition.get("batch_id") != batch_id
                or disposition.get("range") != spec["range"] or disposition.get("status") != "not_started"
                or disposition.get("closures") != [] or disposition.get("based_on_initial_sha256") != initial_hash):
            problems.append(f"批次{batch_id}处置源预填结论或未绑定实际初诊源")

        initial_pages = as_list(initial.get("pages"))
        if len(initial_pages) != spec["page_count"]:
            problems.append(f"批次{batch_id}初诊页数错误")
        merged_initial_pages.extend(initial_pages)
        if slides:
            for number in range(start, end + 1):
                slide = slides[number - 1]
                page_id = f"S{number:03d}"
                diagnosis_path = spec["initial_source"]
                disposition_source = spec["disposition_source"]
                review_record = {"status": "pending", "reviewer": None, "reviewed_at": None, "defect_ids": []}
                expected_pages.append({
                    "node_id": page_id,
                    "page_id": page_id,
                    "node_type": "page",
                    "audit_scope": "pending",
                    "owner_event_id": None,
                    "source_order": number,
                    "source_snapshot_path": V5_SNAPSHOT_PATH,
                    "source_snapshot_sha256": snapshot_hash,
                    "source_module": slide.get("module"),
                    "source_phase": slide.get("phase"),
                    "source_kind": slide.get("kind"),
                    "source_title": slide.get("title") or slide.get("original") or slide.get("kind"),
                    "source_visible_text": slide.get("visible", ""),
                    "source_minutes": slide.get("minutes"),
                    "legacy_student_visible": slide.get("kind") != "teacher_index",
                    "batch_id": batch_id,
                    "batch_range": f"S{start:03d}—S{end:03d}",
                    "batch_content": content,
                    "initial_diagnosis_source": diagnosis_path,
                    "disposition_source": disposition_source,
                    "content_elements": [
                        {"element_id": "visible_text", "kind": "text", "source_field": "source_visible_text"},
                        {"element_id": "page_function", "kind": "function", "source_field": "source_title"},
                        {"element_id": "layout_identity", "kind": "layout", "source_field": "source_kind"},
                    ],
                    "gates": [
                        {
                            "gate_id": f"G{gate}", "gate_status": "pending", "evidence_refs": [],
                            "failure_code": None, "reviewer": None, "reviewed_at": None,
                        }
                        for gate in range(1, 7)
                    ],
                    "review_status": {
                        "scope": "legacy_initial_diagnosis",
                        "self_review": dict(review_record),
                        "student_reception": dict(review_record),
                        "visual": dict(review_record),
                        "consensus": "pending",
                        "adjudication": None,
                    },
                })

    if expected_pages and merged_initial_pages != expected_pages:
        problems.append("12个初诊源合并后与实际V5快照派生骨架不一致")
    aggregate = document.get("legacy_initial_audit")
    if expected_pages and aggregate != expected_pages:
        problems.append("聚合总表与实际V5快照及24个批次源不一致")
    if document.get("pages") != aggregate or document.get("legacy_effective_view") != aggregate:
        problems.append("pages或legacy_effective_view不是初诊骨架的严格镜像")
    if problems:
        return [diagnostic(
            "LEGACY_STAGE_SOURCE_MISMATCH", "legacy_source",
            "; ".join(dict.fromkeys(problems)),
        )]
    return []


def current_nodes(document: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    audit = document.get("current_release_audit")
    if not isinstance(audit, dict):
        return [], []
    return (
        [item for item in as_list(audit.get("pages")) if isinstance(item, dict)],
        [item for item in as_list(audit.get("events")) if isinstance(item, dict)],
    )


def validate_learning_page_contract(page: dict[str, Any], path: str) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    required_scalar = {
        "node_id", "page_id", "node_type", "audit_scope", "execution_order", "release_status",
        "learning_unit", "unit_role", "prerequisite", "epistemic_status", "unique_function",
        "student_input", "artifact_location", "previous_relation", "next_relation", "deletion_loss",
        "framework_cost", "primary_visual_duty", "legacy_source_refs", "inherited_functions",
    }
    list_fields = {"legacy_source_refs", "inherited_functions"}
    missing = [
        field for field in required_scalar
        if field not in page or (field not in list_fields and not nonempty(page.get(field)))
        or (field in list_fields and not isinstance(page.get(field), list))
    ]
    if page.get("node_id") != page.get("page_id") or page.get("node_type") != "page":
        missing.append("node_id/page_id/node_type")
    if page.get("unit_role") not in UNIT_ROLES:
        missing.append("unit_role")
    if page.get("epistemic_status") not in EPISTEMIC_STATUSES:
        missing.append("epistemic_status")
    if page.get("primary_visual_duty") not in PRIMARY_VISUAL_DUTIES:
        missing.append("primary_visual_duty")
    object_contracts = {
        "student_action": {"actor", "action", "object", "duration_seconds", "artifact"},
        "voice_coverage": {"all_have_entry", "independent_entry", "selection_method"},
        "listener_task": {"task", "artifact", "reuse"},
        "observable_change": {"before", "after", "criterion"},
        "merge_test": {"result", "cannot_merge_reason"},
        "channel_split": {"screen", "teacher", "worksheet"},
        "time_value": {"minutes", "irreplaceable_gain"},
    }
    for field, members in object_contracts.items():
        value = page.get(field)
        if not isinstance(value, dict) or not members.issubset(value):
            missing.append(field)
            continue
        for member in members:
            member_value = value.get(member)
            if field == "voice_coverage" and member == "all_have_entry":
                if member_value is not True:
                    missing.append(field)
            elif field == "student_action" and member == "duration_seconds":
                if not isinstance(member_value, (int, float)) or member_value <= 0:
                    missing.append(field)
            elif field == "time_value" and member == "minutes":
                if not isinstance(member_value, (int, float)) or member_value <= 0:
                    missing.append(field)
            elif not nonempty(member_value):
                missing.append(field)
        if field == "observable_change" and value.get("before") == value.get("after"):
            missing.append(field)
        if field == "merge_test" and value.get("result") != "cannot_merge":
            missing.append(field)
    refs = page.get("next_use_refs")
    if not isinstance(refs, list) or not refs:
        missing.append("next_use_refs")
    else:
        for ref in refs:
            if not isinstance(ref, dict) or not {
                "target_event_id", "source_artifact_field", "target_input_field", "expected_use",
            }.issubset(ref) or any(not nonempty(ref.get(field)) for field in (
                "target_event_id", "source_artifact_field", "target_input_field", "expected_use",
            )):
                missing.append("next_use_refs")
                break
    if missing:
        errors.append(diagnostic("CURRENT_PAGE_CONTRACT_INVALID", path, f"page function contract is incomplete: {sorted(set(missing))}"))
    frontstage_values = [
        page.get("student_visible_text"), page.get("screen_content"),
        page.get("channel_split", {}).get("screen") if isinstance(page.get("channel_split"), dict) else None,
    ]
    frontstage_text = json.dumps(frontstage_values, ensure_ascii=False)
    banned = ("学生角色", "设计意图", "硬门", "接收审计", "理解链", "知识碎片", "不填表", "不概括")
    hits = [item for item in banned if item in frontstage_text]
    if hits:
        errors.append(diagnostic("CURRENT_FRONTSTAGE_LEAK", path, f"student frontstage contains design-language leakage: {hits}"))
    return errors


def validate_learning_event_contract(event: dict[str, Any], path: str) -> list[dict[str, str]]:
    required = {
        "node_id", "event_id", "node_type", "audit_scope", "execution_order", "inputs", "actions",
        "artifacts", "observable_change", "artifact_locations", "next_uses", "carrier_ids", "owner_page_ids",
        "gate_4", "gate_5", "evidence_refs", "legacy_source_refs", "inherited_functions", "release_status",
        "terminal_sink", "terminal_use", "review_status", "batch", "implemented",
    }
    invalid = [field for field in required if field not in event or event.get(field) is None]
    if event.get("node_id") != event.get("event_id") or event.get("node_type") != "event" or event.get("audit_scope") != "learning_event":
        invalid.append("node/event identity")
    for field in ("inputs", "actions", "artifacts", "artifact_locations", "owner_page_ids", "evidence_refs"):
        if not isinstance(event.get(field), list) or not event.get(field) or any(not nonempty(item) for item in event.get(field)):
            invalid.append(field)
    change = event.get("observable_change")
    if (not isinstance(change, dict) or not {"before", "after", "criterion"}.issubset(change)
            or any(not nonempty(change.get(field)) for field in ("before", "after", "criterion"))
            or change.get("before") == change.get("after")):
        invalid.append("observable_change")
    if invalid:
        return [diagnostic("CURRENT_EVENT_CONTRACT_INVALID", path, f"learning event contract is incomplete: {sorted(set(invalid))}")]
    return []


def target_lookup(pages: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    result = {f"page:{item.get('node_id')}": item for item in pages if nonempty(item.get("node_id"))}
    result.update({f"event:{item.get('node_id')}": item for item in events if nonempty(item.get("node_id"))})
    return result


def validate_dispositions(document: dict[str, Any], mode: str) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    legacy = dict_index(as_list(document.get("legacy_effective_view")), "page_id")
    pages, events = current_nodes(document)
    targets = target_lookup(pages, events)
    evidence_objects = {str(item.get("node_id")): item for item in pages}
    evidence_objects.update({str(item.get("node_id")): item for item in events})
    evidence_objects.update(legacy)
    defects = dict_index(as_list(document.get("defect_registry")), "defect_id")
    effective_hash = document.get("effective_legacy_hash")
    closures = as_list(document.get("legacy_disposition_closure"))
    closure_ids = [item.get("legacy_id") for item in closures if isinstance(item, dict)]
    if mode in {"freeze-candidate", "freeze", "release"} and (set(closure_ids) != LEGACY_IDS or len(closure_ids) != 127):
        errors.append(diagnostic("DISPOSITION_SET_INVALID", "legacy_disposition_closure", "every legacy page needs exactly one closure"))
    for index, closure in enumerate(closures):
        if not isinstance(closure, dict):
            errors.append(diagnostic("DISPOSITION_INVALID", f"legacy_disposition_closure[{index}]", "closure must be an object"))
            continue
        path = f"legacy_disposition_closure[{index}]"
        legacy_id = str(closure.get("legacy_id"))
        decision = closure.get("decision")
        refs = [str(item) for item in as_list(closure.get("target_refs"))]
        if decision not in DECISIONS:
            errors.append(diagnostic("DISPOSITION_DECISION_INVALID", f"{path}.decision", "unknown disposition"))
        exact_one = decision in {"保留", "移动"}
        if ((decision == "删除" and refs) or (decision != "删除" and not refs)
                or (exact_one and len(refs) != 1)):
            errors.append(diagnostic("DISPOSITION_TARGET_RULE_INVALID", f"{path}.target_refs", "only deletion has zero targets"))
        source = legacy.get(legacy_id, {})
        failed = {
            str(item.get("failure_code"))
            for item in gate_index(source).values()
            if item.get("gate_status") == "fail"
        }
        if decision == "保留" and failed:
            errors.append(diagnostic("DISPOSITION_KEEP_FAILED_LEGACY", f"{path}.decision", "a failed legacy page cannot be retained"))
        if decision == "移动":
            blocked = {
                gate_id for gate_id, gate in gate_index(source).items()
                if gate_id in {"G2", "G3", "G4", "G6"} and gate.get("gate_status") == "fail"
            }
            if blocked:
                errors.append(diagnostic("DISPOSITION_MOVE_GATE_INVALID", f"{path}.decision", "moving cannot hide a structural or learning failure"))
        expected_defects = {
            defect_id for defect_id, defect in defects.items()
            if defect.get("severity") in {"P0", "P1", "P2"} and defect.get("object_ref") == legacy_id
        }
        if set(as_list(closure.get("initial_failure_codes"))) != failed or set(as_list(closure.get("closed_failure_codes"))) != failed:
            errors.append(diagnostic("DISPOSITION_FAILURE_SET_MISMATCH", path, "initial and closed failure sets must equal the sealed diagnosis"))
        if set(as_list(closure.get("initial_defect_ids"))) != expected_defects or set(as_list(closure.get("closed_defect_ids"))) != expected_defects:
            errors.append(diagnostic("DISPOSITION_DEFECT_SET_MISMATCH", path, "all sealed P0-P2 defects must close exactly once"))
        mappings = as_list(closure.get("element_mappings"))
        defect_closures = [item for item in as_list(closure.get("defect_closures")) if isinstance(item, dict)]
        closure_ids = [str(item.get("defect_id")) for item in defect_closures]
        if set(closure_ids) != expected_defects or duplicates(closure_ids):
            errors.append(diagnostic("DISPOSITION_DEFECT_CLOSURE_INVALID", f"{path}.defect_closures", "each effective P0-P2 defect needs exactly one detailed closure"))
        for defect_closure in defect_closures:
            defect_id = str(defect_closure.get("defect_id"))
            defect = defects.get(defect_id, {})
            method = defect_closure.get("closure_method")
            required_common = {
                "defect_id", "closure_method", "before_evidence_refs", "after_evidence_refs",
                "original_reviewer_id", "reviewer_verification_status", "reviewed_at",
            }
            valid = (
                required_common.issubset(defect_closure)
                and references_resolve(defect_closure.get("before_evidence_refs"), evidence_objects)
                and references_resolve(defect_closure.get("after_evidence_refs"), evidence_objects)
                and defect_closure.get("original_reviewer_id") == defect.get("reviewer_id")
                and defect_closure.get("reviewer_verification_status") == "pass"
                and nonempty(defect_closure.get("reviewed_at"))
            )
            if decision == "删除":
                valid = valid and method == "deletion_absence" and defect_closure.get("target_ref") is None and defect_closure.get("target_field") is None
                checks = document.get("global_checks", {})
                valid = (valid and nonempty(defect_closure.get("scan_result_sha256"))
                         and SHA256_RE.fullmatch(str(defect_closure.get("scan_result_sha256"))) is not None
                         and defect_closure.get("scan_result_sha256") == checks.get("deletion_scan_sha256")
                         and not as_list(checks.get("deletion_signature_hits")))
            else:
                target_ref = str(defect_closure.get("target_ref"))
                target_field = str(defect_closure.get("target_field"))
                target = targets.get(target_ref)
                mapped_fields = {
                    (str(item.get("target_ref")), str(item.get("target_field")))
                    for item in mappings if isinstance(item, dict)
                }
                valid = (valid and method == "target_fix" and (target_ref, target_field) in mapped_fields
                         and target is not None and target_field in (target or {}) and nonempty((target or {}).get(target_field)))
                valid = valid and defect_closure.get("target_field_sha256") == audit_sha256((target or {}).get(target_field))
                valid = valid and defect_closure.get("element_mapping_sha256") == audit_sha256(mappings)
                valid = valid and defect_closure.get("current_audit_node_sha256") == audit_sha256(target)
            if not valid:
                errors.append(diagnostic("DISPOSITION_DEFECT_CLOSURE_INVALID", f"{path}.defect_closures[{defect_id}]", "defect closure must prove target repair or global deletion absence with original-reviewer verification"))
        if mode in {"freeze-candidate", "freeze", "release"}:
            if closure.get("based_on_effective_hash") != effective_hash:
                errors.append(diagnostic("DISPOSITION_EFFECTIVE_HASH_STALE", f"{path}.based_on_effective_hash", "closure is not based on the current effective legacy view"))
            if closure.get("decision_status") != "final" or closure.get("closure_status") != "closed":
                errors.append(diagnostic("DISPOSITION_OPEN", path, "freeze/release rejects provisional or open closure"))
        mapped_targets = [targets.get(ref) for ref in refs]
        if any(item is None for item in mapped_targets):
            errors.append(diagnostic("DISPOSITION_TARGET_MISSING", f"{path}.target_refs", "target does not exist in current audit"))
        for ref, target in zip(refs, mapped_targets):
            if target is None:
                continue
            if legacy_id not in as_list(target.get("legacy_source_refs")):
                errors.append(diagnostic("DISPOSITION_LINEAGE_MISMATCH", f"{path}.target_refs", "target lacks reciprocal legacy lineage"))
        page_target_count = sum(1 for ref in refs if ref.startswith("page:"))
        page_required = (
            bool(source.get("legacy_student_visible"))
            or any(item.get("kind") in {"text", "visual", "layout", "student_reception"}
                   for item in as_list(closure.get("legacy_content_elements")) if isinstance(item, dict))
            or any(defects.get(defect_id, {}).get("category") in {"frontstage", "visual", "student_reception"}
                   for defect_id in expected_defects)
        )
        if decision in {"合并", "重写"} and page_required and page_target_count == 0:
            errors.append(diagnostic("DISPOSITION_PAGE_TARGET_REQUIRED", f"{path}.target_refs", "student-visible/frontstage defects need a current page target"))
        source_elements = as_list(source.get("content_elements"))
        if closure.get("legacy_content_elements") != source_elements:
            errors.append(diagnostic("DISPOSITION_CONTENT_INVENTORY_MISMATCH", f"{path}.legacy_content_elements", "closure cannot rewrite or empty the sealed legacy element inventory"))
        source_element_ids = {
            str(item.get("element_id")) for item in source_elements if isinstance(item, dict)
        }
        if set(as_list(closure.get("required_carry_forward"))) - source_element_ids:
            errors.append(diagnostic("DISPOSITION_COVERAGE_INCOMPLETE", f"{path}.required_carry_forward", "carry-forward elements must come from the sealed inventory"))
        mapped_elements = {str(item.get("element_id")) for item in mappings if isinstance(item, dict)}
        required = {str(item) for item in as_list(closure.get("required_carry_forward"))}
        if decision != "删除" and (closure.get("coverage_result") != "complete" or not required.issubset(mapped_elements)):
            errors.append(diagnostic("DISPOSITION_COVERAGE_INCOMPLETE", path, "all required legacy elements need target mappings"))
        inherited_pairs = {
            (str(item.get("legacy_id")), str(item.get("element_id")), str(item.get("target_field")))
            for target in mapped_targets if target is not None
            for item in as_list(target.get("inherited_functions")) if isinstance(item, dict)
        }
        mapping_pairs = {
            (legacy_id, str(item.get("element_id")), str(item.get("target_field")))
            for item in mappings if isinstance(item, dict)
        }
        if decision != "删除" and not mapping_pairs.issubset(inherited_pairs):
            errors.append(diagnostic("DISPOSITION_LINEAGE_MISMATCH", f"{path}.element_mappings", "target inherited-functions fields must reciprocate every mapped element"))
        if decision != "删除" and mappings:
            values: list[Any] = []
            for mapping in mappings:
                if not isinstance(mapping, dict):
                    continue
                target = targets.get(str(mapping.get("target_ref")))
                field_name = str(mapping.get("target_field"))
                if target is not None and field_name in target and nonempty(target.get(field_name)):
                    values.append(target.get(field_name))
                else:
                    errors.append(diagnostic("DISPOSITION_TARGET_FIELD_MISSING", f"{path}.element_mappings", "mapped target field must exist and be non-empty"))
            field_value: Any = values[0] if len(values) == 1 else values
            if closure.get("target_field_sha256") != canonical_sha256(field_value):
                errors.append(diagnostic("DISPOSITION_TARGET_HASH_STALE", f"{path}.target_field_sha256", "mapped target field changed after closure"))
            if closure.get("element_mapping_sha256") != canonical_sha256(mappings):
                errors.append(diagnostic("DISPOSITION_MAPPING_HASH_STALE", f"{path}.element_mapping_sha256", "element mapping changed after closure"))
            audit_target = targets.get(refs[0]) if refs else None
            if audit_target is not None and closure.get("current_audit_node_sha256") != canonical_sha256(audit_target):
                errors.append(diagnostic("DISPOSITION_AUDIT_HASH_STALE", f"{path}.current_audit_node_sha256", "current audit node changed after closure"))
        if decision == "删除":
            signatures = as_list(closure.get("forbidden_reappearance_signatures"))
            if as_list(closure.get("legacy_content_elements")) == [] or not signatures:
                errors.append(diagnostic("DISPOSITION_DELETION_EVIDENCE_INVALID", path, "deletion needs inventoried legacy elements and forbidden reappearance signatures"))
            for signature in signatures:
                if not isinstance(signature, dict) or not {
                    "signature_type", "normalizer", "detector", "scan_scope", "signature_sha256",
                }.issubset(signature) or signature.get("signature_type") not in {"text", "asset", "layout", "event"}:
                    errors.append(diagnostic("DISPOSITION_DELETION_EVIDENCE_INVALID", f"{path}.forbidden_reappearance_signatures", "deletion signature contract is incomplete"))
            review = closure.get("review_status")
            if not isinstance(review, dict) or review.get("status") != "pass" or not nonempty(review.get("reviewer")):
                errors.append(diagnostic("DISPOSITION_DELETION_EVIDENCE_INVALID", f"{path}.review_status", "deletion needs independent closure review"))
    return errors


def validate_current_layer(document: dict[str, Any], mode: str) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    strict = mode in {"freeze-candidate", "freeze", "release"}
    pages, events = current_nodes(document)
    page_by_id = dict_index(pages, "node_id")
    event_by_id = dict_index(events, "node_id")
    audit_sets = (set(page_by_id), set(event_by_id))
    manifest_sets = node_sets(document.get("structure_manifest"))
    if audit_sets != manifest_sets:
        errors.append(diagnostic("CURRENT_AUDIT_SET_MISMATCH", "current_release_audit", "current page/event audit must equal the structure manifest"))
    for field in ("declared_node_inventory", "source_graph_inventory", "structure_assembly_snapshot"):
        if node_sets(document.get(field)) != manifest_sets:
            errors.append(diagnostic("CURRENT_INVENTORY_SET_MISMATCH", field, "structure, declaration, reachability and assembly sets must match"))
    declared_sets = node_sets(document.get("declared_node_inventory"))
    graph_sets = node_sets(document.get("source_graph_inventory"))
    if not declared_sets[0].issubset(graph_sets[0]) or not declared_sets[1].issubset(graph_sets[1]):
        errors.append(diagnostic("CURRENT_DECLARED_ORPHAN", "declared_node_inventory", "declared source node is unreachable"))

    all_nodes = {**page_by_id, **event_by_id}
    orders = [item.get("execution_order") for item in all_nodes.values()]
    if any(not isinstance(item, int) for item in orders) or duplicates(orders):
        errors.append(diagnostic("CURRENT_EXECUTION_ORDER_INVALID", "current_release_audit", "execution order must be unique integers"))

    for index, page in enumerate(pages):
        path = f"current_release_audit.pages[{index}]"
        errors.extend(validate_learning_page_contract(page, path))
        errors.extend(validate_gate_collection(page, path, GATE_IDS))
        errors.extend(validate_review(page.get("review_status"), f"{path}.review_status", strict))
        scope = page.get("audit_scope")
        gates = gate_index(page)
        if scope not in {"learning_page", "event_carrier"}:
            errors.append(diagnostic("CURRENT_SCOPE_INVALID", f"{path}.audit_scope", "unknown page audit scope"))
        if scope == "learning_page":
            if nonempty(page.get("owner_event_id")):
                errors.append(diagnostic("CURRENT_CARRIER_OWNER_MISMATCH", f"{path}.owner_event_id", "learning page cannot borrow an event owner"))
            if any(item.get("gate_status") == "na" for item in gates.values()):
                errors.append(diagnostic("CURRENT_NA_MISUSE", f"{path}.gates", "learning page must pass its own six gates"))
        if scope == "event_carrier":
            owner_id = str(page.get("owner_event_id"))
            owner = event_by_id.get(owner_id)
            if owner is None or page.get("node_id") not in as_list(owner.get("carrier_ids")):
                errors.append(diagnostic("CURRENT_CARRIER_OWNER_MISMATCH", f"{path}.owner_event_id", "carrier and owner event must reference each other"))
            for gate_id, gate in gates.items():
                status = gate.get("gate_status")
                if gate_id in {"G4", "G5"}:
                    if status not in {"na", "pass"}:
                        errors.append(diagnostic("CURRENT_CARRIER_GATE_INVALID", f"{path}.{gate_id}", "carrier G4/G5 must borrow with na or pass independently"))
                    elif status == "na" and owner is not None:
                        event_field = "gate_4" if gate_id == "G4" else "gate_5"
                        expected_ref = f"{owner_id}#{event_field}"
                        event_gate = owner.get(event_field)
                        if (not isinstance(event_gate, dict)
                                or event_gate.get("gate_status") not in {"pass", "deferred"}
                                or expected_ref not in as_list(gate.get("evidence_refs"))):
                            errors.append(diagnostic(
                                "CURRENT_CARRIER_EVENT_EVIDENCE_INVALID", f"{path}.{gate_id}",
                                "carrier na must cite its owning event's concrete G4/G5 field",
                            ))
                elif status == "na":
                    errors.append(diagnostic("CURRENT_NA_MISUSE", f"{path}.{gate_id}", "only carrier G4/G5 may use na"))
        if strict and (page.get("release_status") != "final" or any(item.get("gate_status") != "pass" for item in gates.values() if not (scope == "event_carrier" and item.get("gate_id") in {"G4", "G5"} and item.get("gate_status") == "na"))):
            errors.append(diagnostic("CURRENT_GATE_OPEN", path, "freeze/release rejects pending, deferred, provisional or failed current pages"))
        if scope == "learning_page" and not as_list(page.get("legacy_source_refs")):
            errors.append(diagnostic("CURRENT_LINEAGE_MISSING", f"{path}.legacy_source_refs", "current learning page needs reverse legacy lineage"))

    for index, event in enumerate(events):
        path = f"current_release_audit.events[{index}]"
        errors.extend(validate_learning_event_contract(event, path))
        for gate_name in ("gate_4", "gate_5"):
            gate = event.get(gate_name)
            if not isinstance(gate, dict) or gate.get("gate_status") not in GATE_STATUSES:
                errors.append(diagnostic("CURRENT_EVENT_GATE_INVALID", f"{path}.{gate_name}", "event needs an independent gate record"))
            elif strict and gate.get("gate_status") != "pass":
                errors.append(diagnostic("CURRENT_GATE_OPEN", f"{path}.{gate_name}", "event gate is open"))
        if strict and event.get("release_status") != "final":
            errors.append(diagnostic("CURRENT_GATE_OPEN", f"{path}.release_status", "event is provisional"))
        for carrier_id in as_list(event.get("carrier_ids")):
            carrier = page_by_id.get(str(carrier_id))
            if carrier is None or carrier.get("audit_scope") != "event_carrier" or carrier.get("owner_event_id") != event.get("node_id"):
                errors.append(diagnostic("CURRENT_CARRIER_OWNER_MISMATCH", f"{path}.carrier_ids", "event carrier link is not reciprocal"))

    edges = as_list(document.get("structure_manifest", {}).get("g5_edges")) if isinstance(document.get("structure_manifest"), dict) else []
    adjacency: dict[str, set[str]] = defaultdict(set)
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(diagnostic("CURRENT_G5_EDGE_INVALID", f"structure_manifest.g5_edges[{index}]", "edge must be an object"))
            continue
        source_id = str(edge.get("source_node_id"))
        target_id = str(edge.get("target_event_id"))
        source = all_nodes.get(source_id)
        target = event_by_id.get(target_id)
        if source is None or target is None or not isinstance(source.get("execution_order"), int) or not isinstance(target.get("execution_order"), int) or source.get("execution_order") >= target.get("execution_order"):
            errors.append(diagnostic("CURRENT_G5_ORDER_INVALID", f"structure_manifest.g5_edges[{index}]", "G5 edge must point strictly forward to an event"))
        adjacency[source_id].add(target_id)

    edge_pairs = {(str(item.get("source_node_id")), str(item.get("target_event_id"))) for item in edges if isinstance(item, dict)}
    for page in pages:
        page_id = str(page.get("node_id"))
        page_order = page.get("execution_order")
        g5 = gate_index(page).get("G5", {})
        next_uses = as_list(page.get("next_use_refs"))
        if g5.get("gate_status") == "deferred":
            if mode != "stage" or page.get("release_status") != "provisional" or any(
                not nonempty(g5.get(field)) for field in ("target_event_id", "target_batch", "expected_use")
            ):
                errors.append(diagnostic("CURRENT_DEFERRED_INVALID", f"page:{page_id}#G5", "deferred G5 needs target, batch, expected use and provisional status"))
            else:
                target = event_by_id.get(str(g5.get("target_event_id")))
                if target is None or target.get("batch") != g5.get("target_batch"):
                    errors.append(diagnostic("CURRENT_DEFERRED_INVALID", f"page:{page_id}#G5", "deferred target does not exist in the declared batch"))
                elif target.get("implemented"):
                    errors.append(diagnostic("CURRENT_DEFERRED_NOT_RESOLVED", f"page:{page_id}#G5", "implemented target requires pass/final or fail/orphan"))
            continue
        if g5.get("gate_status") != "pass":
            continue
        for next_use in next_uses:
            if not isinstance(next_use, dict):
                continue
            target_id = str(next_use.get("target_event_id"))
            target = event_by_id.get(target_id)
            matching_input = False
            if target is not None:
                for event_input in as_list(target.get("inputs")):
                    if (isinstance(event_input, dict)
                            and event_input.get("source_node_id") == page_id
                            and event_input.get("source_artifact_field") == next_use.get("source_artifact_field")
                            and event_input.get("input_field") == next_use.get("target_input_field")):
                        matching_input = True
                        break
            if (page_id, target_id) not in edge_pairs or not matching_input or target is None or (
                isinstance(page_order, int) and isinstance(target.get("execution_order"), int)
                and page_order >= target.get("execution_order")
            ):
                errors.append(diagnostic("CURRENT_G5_LINK_MISMATCH", f"page:{page_id}#next_use_refs", "page edge and target event input must match by field and order"))
        if not next_uses:
            errors.append(diagnostic("CURRENT_G5_LINK_MISMATCH", f"page:{page_id}#next_use_refs", "passed page G5 needs a structured forward use"))
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        cyclic = any(visit(target) for target in adjacency.get(node, set()))
        visiting.remove(node)
        visited.add(node)
        return cyclic

    if any(visit(node) for node in list(all_nodes)):
        errors.append(diagnostic("CURRENT_G5_CYCLE", "structure_manifest.g5_edges", "G5 graph must be acyclic"))

    terminals = [item for item in events if item.get("terminal_sink") is True]
    max_order = max((item.get("execution_order") for item in all_nodes.values() if isinstance(item.get("execution_order"), int)), default=None)
    honest_empty_stage = mode == "stage" and not all_nodes
    if honest_empty_stage:
        pass
    elif len(terminals) != 1 or terminals[0].get("execution_order") != max_order:
        errors.append(diagnostic("CURRENT_TERMINAL_INVALID", "current_release_audit.events", "exactly one terminal event must be last"))
    elif as_list(terminals[0].get("next_uses")) or set(terminals[0].get("terminal_use", {})) < {
        "final_artifact", "recipient_or_owner", "post_class_use", "artifact_location",
        "delivery_evidence_refs", "no_further_classroom_call_reason",
    } or not all(nonempty(terminals[0].get("terminal_use", {}).get(field)) for field in (
        "final_artifact", "recipient_or_owner", "post_class_use", "artifact_location",
        "delivery_evidence_refs", "no_further_classroom_call_reason",
    )):
        errors.append(diagnostic("CURRENT_TERMINAL_USE_INVALID", "current_release_audit.events", "terminal event needs real delivery and preservation evidence"))
    return errors


def validate_release(document: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    release = document.get("final_release")
    if not isinstance(release, dict):
        return [diagnostic("RELEASE_EVIDENCE_MISSING", "final_release", "release needs physical artifacts, channels and reviews")]
    required = {
        "release_artifact_manifest", "slide_occurrence_inventory", "document_page_inventory",
        "other_channel_inventory", "physical_assembly_snapshot", "current_manifest", "release_review_ledger",
    }
    if not required.issubset(release):
        errors.append(diagnostic("RELEASE_EVIDENCE_MISSING", "final_release", "release evidence bundle is incomplete"))
    slides = [item for item in as_list(release.get("slide_occurrence_inventory")) if isinstance(item, dict)]
    documents = [item for item in as_list(release.get("document_page_inventory")) if isinstance(item, dict)]
    channels = [item for item in as_list(release.get("other_channel_inventory")) if isinstance(item, dict)]
    manifest_pages, manifest_events = node_sets(document.get("structure_manifest"))
    artifact_manifest = release.get("release_artifact_manifest")
    approved_assets = release.get("approved_visual_assets_manifest")
    approved_assets_hash = audit_sha256(approved_assets) if isinstance(approved_assets, dict) else None
    page_asset_bindings = dict_index(as_list(approved_assets.get("page_bindings")), "page_id") if isinstance(approved_assets, dict) else {}
    approved_asset_records = dict_index(as_list(approved_assets.get("assets")), "asset_id") if isinstance(approved_assets, dict) else {}
    approved_asset_ids = {
        asset_id for asset_id, item in approved_asset_records.items() if item.get("status") == "approved"
    }
    character_manifest_path = resolve_source_path(
        approved_assets.get("character_reference_manifest_path") if isinstance(approved_assets, dict) else None
    )
    character_manifest, character_manifest_file_sha256 = read_json_receipt(
        approved_assets.get("character_reference_manifest_path") if isinstance(approved_assets, dict) else None
    )
    required_character_versions = {
        f"{character}-{stage}" for character in ("W01", "M01") for stage in ("T", "A", "B", "C")
    }
    expected_clothing_ids = {
        f"W01-{stage}": f"W_C{stage}" for stage in ("T", "A", "B", "C")
    } | {
        f"M01-{stage}": f"M_C{stage}" for stage in ("T", "A", "B", "C")
    }
    expected_hairstyle_ids = {
        f"W01-{stage}": f"W_H{stage}" for stage in ("T", "A", "B", "C")
    } | {
        f"M01-{stage}": f"M_H{stage}" for stage in ("T", "A", "B", "C")
    }
    expected_clothing_colors = {
        "W_CT": ["#CBBE9E", "#78806B"], "W_CA": ["#C7B58F", "#68745C", "#8A6650"],
        "W_CB": ["#B9A27F", "#687064"], "W_CC": ["#918675", "#5F6867"],
        "M_CT": ["#8A806D", "#686157"], "M_CA": ["#766B5B", "#575147", "#695542"],
        "M_CB": ["#6C6255", "#514C45"], "M_CC": ["#5C554C", "#494641"],
    }
    character_versions = dict_index(as_list((character_manifest or {}).get("characters")), "character_version")
    required_views = {"front", "side", "back", "three_quarter"}
    character_manifest_valid = (
        character_manifest_path is not None
        and isinstance(character_manifest, dict)
        and character_manifest.get("schema_version") == "1.0"
        and character_manifest.get("style_id") == "warm-handdrawn-low-saturation-v1"
        and character_manifest_file_sha256 == (approved_assets or {}).get("character_reference_manifest_sha256")
        and set(character_versions) == required_character_versions
        and all(
            required_views.issubset(set(as_list(item.get("views"))))
            and item.get("clothing_id") == expected_clothing_ids.get(character_version)
            and item.get("hairstyle_id") == expected_hairstyle_ids.get(character_version)
            and item.get("hair_color") == ("#2B2723" if character_version.startswith("W01-") else "#282521")
            and item.get("facial_anchor_id") == f"{character_version.split('-', 1)[0]}_FACE_V1"
            and item.get("silhouette_anchor_id") == f"{character_version.split('-', 1)[0]}_BODY_V1"
            and isinstance(item.get("prop_ids"), list)
            and isinstance(item.get("proportion"), dict)
            and item.get("proportion", {}).get("head_to_body_ratio")
            == (6.5 if character_version.startswith("W01-") else 6.7)
            and item.get("proportion", {}).get("shared_frame_height")
            == (1.00 if character_version.startswith("W01-") else 1.06)
            for character_version, item in character_versions.items()
        )
        and character_manifest.get("clothing_color_anchors") == expected_clothing_colors
        and isinstance(character_manifest.get("shared_frame_proportions"), list)
        and {
            (str(item.get("pair")), str(item.get("ratio")))
            for item in character_manifest.get("shared_frame_proportions") if isinstance(item, dict)
        } == {(f"W01-{stage}/M01-{stage}", "1.00:1.06") for stage in ("T", "A", "B", "C")}
    )
    if (not isinstance(approved_assets, dict)
            or approved_assets.get("schema_version") != "1.0"
            or not character_manifest_valid
            or duplicates(
                item.get("asset_id") for item in as_list(approved_assets.get("assets")) if isinstance(item, dict)
            )
            or duplicates(
                item.get("page_id") for item in as_list(approved_assets.get("page_bindings")) if isinstance(item, dict)
            )):
        errors.append(diagnostic("RELEASE_CHARACTER_MANIFEST_INVALID", "final_release.approved_visual_assets_manifest", "approved assets must bind a readable complete W01/M01 character-reference manifest and unique assets/pages"))
    approved_asset_hashes: dict[str, str] = {}
    for asset_id, asset in approved_asset_records.items():
        asset_path = resolve_source_path(asset.get("source_path"))
        versions = set(str(item) for item in as_list(asset.get("character_versions")))
        if (asset.get("status") != "approved"
                or asset_path is None
                or file_sha256(asset_path) != asset.get("source_sha256")
                or SHA256_RE.fullmatch(str(asset.get("source_sha256"))) is None
                or not versions.issubset(required_character_versions)
                or not versions):
            errors.append(diagnostic("RELEASE_APPROVED_ASSET_INVALID", f"approved_asset:{asset_id}", "approved assets need real files, recomputed hashes and valid character versions"))
            continue
        approved_asset_hashes[asset_id] = str(asset.get("source_sha256"))
    if duplicates(approved_asset_hashes.values()):
        errors.append(diagnostic("RELEASE_APPROVED_ASSET_INVALID", "final_release.approved_visual_assets_manifest.assets", "different approved asset IDs cannot reuse identical file hashes"))
    artifacts = dict_index(as_list(artifact_manifest.get("artifacts")), "artifact_id") if isinstance(artifact_manifest, dict) else {}
    physical_artifacts = {str(item.get("artifact_id")) for item in slides} | {str(item.get("artifact_id")) for item in documents}
    occurrence_artifacts = (
        {str(item.get("artifact_id")) for item in slides}
        | {str(item.get("artifact_id")) for item in documents}
        | {str(item.get("source_artifact_id")) for item in channels}
    )
    if (not artifacts or occurrence_artifacts != set(artifacts)
            or any(
                artifact.get("type") in {"pptx", "docx"} and artifact_id not in physical_artifacts
                for artifact_id, artifact in artifacts.items()
            )):
        errors.append(diagnostic("RELEASE_ARTIFACT_MANIFEST_INVALID", "final_release.release_artifact_manifest", "artifact manifest must enumerate exactly every physical inventory source"))
    for artifact_id, artifact in artifacts.items():
        artifact_type = artifact.get("type")
        office_artifact = artifact_type in {"pptx", "docx"}
        if (artifact_type not in {"pptx", "docx", "text", "audio"}
                or not isinstance(artifact.get("official_entries"), list)
                or not nonempty(artifact.get("source_path"))
                or SHA256_RE.fullmatch(str(artifact.get("source_sha256"))) is None
                or (office_artifact and (
                    not isinstance(artifact.get("page_count"), int) or artifact.get("page_count") < 1
                    or SHA256_RE.fullmatch(str(artifact.get("render_manifest_sha256"))) is None
                ))
                or (not office_artifact and artifact.get("page_count") != 0)):
            errors.append(diagnostic("RELEASE_ARTIFACT_MANIFEST_INVALID", f"artifact:{artifact_id}", "artifact type and official entries are required"))
        if artifact.get("type") == "pptx" and SHA256_RE.fullmatch(str(artifact.get("approved_assets_manifest_sha256"))) is None:
            errors.append(diagnostic("RELEASE_ARTIFACT_MANIFEST_INVALID", f"artifact:{artifact_id}.approved_assets_manifest_sha256", "PPTX must bind approved assets and character versions"))
        observation = artifact.get("file_observation")
        if (not isinstance(observation, dict) or not nonempty(observation.get("parser"))
                or observation.get("observed_source_sha256") != artifact.get("source_sha256")
                or (office_artifact and observation.get("observed_page_count") != artifact.get("page_count"))
                or (not office_artifact and observation.get("observed_byte_count") != artifact.get("byte_count"))):
            errors.append(diagnostic("RELEASE_PHYSICAL_SOURCE_MISMATCH", f"artifact:{artifact_id}.file_observation", "independent parser observation must match the declared source and page count"))
        source_path = resolve_source_path(artifact.get("source_path"))
        if source_path is None or file_sha256(source_path) != artifact.get("source_sha256"):
            errors.append(diagnostic("RELEASE_PHYSICAL_SOURCE_MISMATCH", f"artifact:{artifact_id}.source_path", "release validator must read the actual Office source and recompute its SHA-256"))
        elif artifact.get("type") == "pptx":
            try:
                actual_slides = inspect_pptx(source_path)
                declared_occurrences = sorted(
                    (item for item in slides if item.get("artifact_id") == artifact_id),
                    key=lambda item: item.get("physical_index", 0),
                )
                declared_fact = [{
                    "physical_index": item.get("physical_index"),
                    "page_ids": [item.get("page_id")],
                    "hidden": item.get("hidden"),
                    "notes_event_ids": as_list(item.get("notes_event_ids")),
                    "asset_ids": sorted(str(value) for value in as_list(item.get("embedded_asset_ids"))),
                    "media_sha256": sorted(str(value) for value in as_list(item.get("media_sha256"))),
                    "media_bindings": sorted(
                        ({key: value.get(key) for key in ("asset_id", "relationship_id", "media_target", "media_sha256")}
                         for value in as_list(item.get("media_bindings")) if isinstance(value, dict)),
                        key=lambda value: str(value.get("relationship_id")),
                    ),
                    "image_relationship_count": item.get("image_relationship_count", 0),
                } for item in declared_occurrences]
                if (len(actual_slides) != artifact.get("page_count")
                        or actual_slides != declared_fact
                        or any(len(item.get("page_ids", [])) != 1 for item in actual_slides)):
                    errors.append(diagnostic("RELEASE_PHYSICAL_SOURCE_MISMATCH", f"artifact:{artifact_id}", "actual PPTX slide count/hidden flags differ from the physical inventory"))
            except (OSError, zipfile.BadZipFile, KeyError, AttributeError, ElementTree.ParseError):
                errors.append(diagnostic("RELEASE_PHYSICAL_SOURCE_MISMATCH", f"artifact:{artifact_id}", "PPTX source cannot be independently parsed"))
    occurrence_refs = [item.get("occurrence_ref") for item in slides]
    artifact_indices = [(item.get("artifact_id"), item.get("physical_index")) for item in slides]
    artifact_pages = [(item.get("artifact_id"), item.get("page_id")) for item in slides]
    slide_ids = {str(item.get("page_id")) for item in slides}
    if (duplicates(occurrence_refs) or duplicates(artifact_indices) or duplicates(artifact_pages)
            or not slide_ids.issubset(manifest_pages)
            or {str(item.get("page_id")) for item in slides if item.get("projected")} != manifest_pages):
        errors.append(diagnostic("RELEASE_SLIDE_BIJECTION_INVALID", "final_release.slide_occurrence_inventory", "official PPTX occurrences must map physical slides and page IDs bijectively"))
    for artifact_id, artifact in artifacts.items():
        if artifact.get("type") == "pptx":
            indices = sorted(int(item.get("physical_index")) for item in slides if item.get("artifact_id") == artifact_id and isinstance(item.get("physical_index"), int))
            if indices != list(range(1, len(indices) + 1)) or ("page_count" in artifact and artifact.get("page_count") != len(indices)):
                errors.append(diagnostic("RELEASE_SLIDE_BIJECTION_INVALID", f"artifact:{artifact_id}", "PPTX physical indices and declared page count must be contiguous and equal"))
            render_entries = [
                {"occurrence_ref": item.get("occurrence_ref"), "render_sha256": item.get("render_sha256")}
                for item in slides if item.get("artifact_id") == artifact_id
            ]
            if (any(SHA256_RE.fullmatch(str(item.get("render_sha256"))) is None for item in render_entries)
                    or artifact.get("render_manifest_sha256") != audit_sha256(render_entries)
                    or artifact.get("approved_assets_manifest_sha256") != approved_assets_hash):
                errors.append(diagnostic("RELEASE_PPT_RENDER_BINDING_MISMATCH", f"artifact:{artifact_id}", "PPTX must bind every current slide render and the current approved asset/character manifest"))
            for occurrence in (item for item in slides if item.get("artifact_id") == artifact_id):
                render_path = resolve_source_path(occurrence.get("render_path"))
                if render_path is None or file_sha256(render_path) != occurrence.get("render_sha256"):
                    errors.append(diagnostic("RELEASE_PPT_RENDER_BINDING_MISMATCH", f"occurrence:{occurrence.get('occurrence_ref')}.render_path", "slide render hash must be recomputed from the actual rendered file"))
            official_entries = set(as_list(artifact.get("official_entries")))
            for occurrence in (item for item in slides if item.get("artifact_id") == artifact_id):
                projected_expected = (
                    occurrence.get("official_entry_id") in official_entries
                    and occurrence.get("reachable_from_start") is True
                    and occurrence.get("hidden") is False
                )
                if occurrence.get("projected") is not projected_expected:
                    errors.append(diagnostic("RELEASE_VISIBILITY_DERIVATION_INVALID", f"occurrence:{occurrence.get('occurrence_ref')}", "projected must derive from official entry, reachability and hidden state"))
                embedded_assets = set(str(item) for item in as_list(occurrence.get("embedded_asset_ids")))
                declared_media_hashes = sorted(str(item) for item in as_list(occurrence.get("media_sha256")))
                declared_media_bindings = [
                    item for item in as_list(occurrence.get("media_bindings")) if isinstance(item, dict)
                ]
                expected_media_hashes = sorted(
                    approved_asset_hashes[asset_id] for asset_id in embedded_assets if asset_id in approved_asset_hashes
                )
                if (declared_media_hashes != expected_media_hashes
                        or len(declared_media_hashes) != occurrence.get("image_relationship_count", 0)
                        or set(str(item.get("asset_id")) for item in declared_media_bindings) != embedded_assets
                        or len(declared_media_bindings) != len(embedded_assets)
                        or any(
                            item.get("media_sha256") != approved_asset_hashes.get(str(item.get("asset_id")))
                            or SHA256_RE.fullmatch(str(item.get("media_sha256"))) is None
                            or not nonempty(item.get("relationship_id"))
                            or not nonempty(item.get("media_target"))
                            for item in declared_media_bindings
                        )):
                    errors.append(diagnostic("RELEASE_MEDIA_ASSET_MISMATCH", f"occurrence:{occurrence.get('occurrence_ref')}", "PPTX image relationship media must equal the page-bound approved asset files"))
                binding = page_asset_bindings.get(str(occurrence.get("page_id")))
                page_audit = next((item for item in current_nodes(document)[0] if item.get("node_id") == occurrence.get("page_id")), None)
                if binding is None or binding.get("status") not in {"approved_to_use", "no_image_required"}:
                    errors.append(diagnostic("RELEASE_ILLUSTRATION_TASK_CARD_INVALID", f"occurrence:{occurrence.get('occurrence_ref')}", "every slide needs an approved visual task-card decision"))
                elif binding.get("status") == "no_image_required":
                    if (embedded_assets or not nonempty(binding.get("no_image_reason")) or not nonempty(binding.get("instructional_gain"))
                            or binding.get("primary_visual_duty") != (page_audit or {}).get("primary_visual_duty")):
                        errors.append(diagnostic("RELEASE_VISUAL_FUNCTION_GAIN_INVALID", f"occurrence:{occurrence.get('occurrence_ref')}", "no-image decision needs a functional gain and no embedded scene assets"))
                else:
                    bound_assets = set(str(item) for item in as_list(binding.get("asset_ids")))
                    required_card_fields = {
                        "page_id", "status", "primary_visual_duty", "instructional_gain", "poem_evidence_refs",
                        "allowed_facts", "forbidden_inferences", "no_image_alternative", "asset_ids", "character_versions",
                    }
                    if (not required_card_fields.issubset(binding) or not nonempty(binding.get("instructional_gain"))
                            or binding.get("instructional_gain").strip() in {"好看", "美观", "装饰", "更好看"}
                            or binding.get("primary_visual_duty") != (page_audit or {}).get("primary_visual_duty")
                            or not as_list(binding.get("poem_evidence_refs")) or not as_list(binding.get("allowed_facts"))
                            or not as_list(binding.get("forbidden_inferences")) or as_list(binding.get("forbidden_inferences")) == ["无"]
                            or not nonempty(binding.get("no_image_alternative"))
                            or embedded_assets != bound_assets or not embedded_assets.issubset(approved_asset_ids)
                            or set(str(item) for item in as_list(binding.get("character_versions")))
                            != {
                                str(version)
                                for asset_id in bound_assets
                                for version in as_list(approved_asset_records.get(asset_id, {}).get("character_versions"))
                            }):
                        errors.append(diagnostic("RELEASE_ILLUSTRATION_TASK_CARD_INVALID", f"occurrence:{occurrence.get('occurrence_ref')}", "embedded assets must match a complete approved task card and approved asset set"))
    all_embedded_assets = {
        str(asset_id) for occurrence in slides for asset_id in as_list(occurrence.get("embedded_asset_ids"))
    }
    all_bound_assets = {
        str(asset_id)
        for binding in page_asset_bindings.values()
        if binding.get("status") == "approved_to_use"
        for asset_id in as_list(binding.get("asset_ids"))
    }
    if approved_asset_ids != all_embedded_assets or approved_asset_ids != all_bound_assets:
        errors.append(diagnostic("RELEASE_MEDIA_ASSET_MISMATCH", "final_release.approved_visual_assets_manifest.assets", "approved assets, task-card bindings and actual PPTX image markers must be exactly equal"))
    if any("page_id" in item for item in documents):
        errors.append(diagnostic("RELEASE_DOC_PAGE_ID_FORBIDDEN", "final_release.document_page_inventory", "DOCX pagination must not mint structural Nxxx IDs"))
    doc_keys = [(item.get("artifact_id"), item.get("doc_page_index")) for item in documents]
    if (duplicates(doc_keys)
            or any(not isinstance(item.get("doc_page_index"), int) or item.get("doc_page_index") < 1 for item in documents)
            or any(SHA256_RE.fullmatch(str(item.get("source_sha256"))) is None
                   or SHA256_RE.fullmatch(str(item.get("render_sha256"))) is None for item in documents)):
        errors.append(diagnostic("RELEASE_DOCUMENT_INVENTORY_INVALID", "final_release.document_page_inventory", "document page keys must be unique positive integers"))
    for artifact_id, artifact in artifacts.items():
        if artifact.get("type") == "docx":
            pages_for_artifact = sorted(
                (item for item in documents if item.get("artifact_id") == artifact_id),
                key=lambda item: item.get("doc_page_index", 0),
            )
            render_entries = [
                {"doc_page_index": item.get("doc_page_index"), "render_sha256": item.get("render_sha256")}
                for item in pages_for_artifact
            ]
            if (len(pages_for_artifact) != artifact.get("page_count")
                    or any(item.get("source_sha256") != artifact.get("source_sha256") for item in pages_for_artifact)
                    or artifact.get("render_manifest_sha256") != audit_sha256(render_entries)):
                errors.append(diagnostic("RELEASE_DOCUMENT_SOURCE_MISMATCH", f"artifact:{artifact_id}", "DOCX pages and renders must bind the current source artifact"))
            for document_page in pages_for_artifact:
                render_path = resolve_source_path(document_page.get("render_path"))
                if render_path is None or file_sha256(render_path) != document_page.get("render_sha256"):
                    errors.append(diagnostic("RELEASE_DOCUMENT_SOURCE_MISMATCH", f"artifact:{artifact_id}.page:{document_page.get('doc_page_index')}", "document render hash must be recomputed from the actual rendered page"))
            pagination_path = resolve_source_path(artifact.get("pagination_pdf_path"))
            pagination_hash = artifact.get("pagination_pdf_sha256")
            pagination_receipt, pagination_receipt_hash = read_json_receipt(artifact.get("pagination_receipt_path"))
            expected_pagination_receipt = {
                "check_type": "docx_pagination",
                "source_sha256": artifact.get("source_sha256"),
                "pdf_sha256": pagination_hash,
                "page_count": artifact.get("page_count"),
                "renderer": artifact.get("pagination_renderer"),
                "renderer_parameters": artifact.get("pagination_renderer_parameters"),
            }
            if (pagination_path is None
                    or SHA256_RE.fullmatch(str(pagination_hash)) is None
                    or file_sha256(pagination_path) != pagination_hash
                    or pdf_page_count(pagination_path) != artifact.get("page_count")
                    or not nonempty(artifact.get("pagination_renderer"))
                    or not isinstance(artifact.get("pagination_renderer_parameters"), dict)
                    or pagination_receipt != expected_pagination_receipt
                    or pagination_receipt_hash != artifact.get("pagination_receipt_sha256")):
                errors.append(diagnostic("RELEASE_DOCUMENT_PAGINATION_INVALID", f"artifact:{artifact_id}", "DOCX physical page count must be independently bound to a real rendered PDF receipt"))
            for document_page in pages_for_artifact:
                render_receipt, render_receipt_hash = read_json_receipt(document_page.get("render_receipt_path"))
                expected_render_receipt = {
                    "check_type": "document_page_render",
                    "pagination_pdf_sha256": pagination_hash,
                    "doc_page_index": document_page.get("doc_page_index"),
                    "render_sha256": document_page.get("render_sha256"),
                    "renderer": document_page.get("render_renderer"),
                    "renderer_parameters": document_page.get("render_renderer_parameters"),
                }
                if (not nonempty(document_page.get("render_renderer"))
                        or not isinstance(document_page.get("render_renderer_parameters"), dict)
                        or render_receipt != expected_render_receipt
                        or render_receipt_hash != document_page.get("render_receipt_sha256")):
                    errors.append(diagnostic("RELEASE_DOCUMENT_RENDER_PROVENANCE_INVALID", f"artifact:{artifact_id}.page:{document_page.get('doc_page_index')}", "each page render must bind the current pagination PDF, page index, renderer and parameters"))
    if release.get("physical_assembly_snapshot") != {"artifacts": as_list(artifact_manifest.get("artifacts")) if isinstance(artifact_manifest, dict) else [], "slides": slides, "documents": documents}:
        errors.append(diagnostic("RELEASE_PHYSICAL_SNAPSHOT_MISMATCH", "final_release.physical_assembly_snapshot", "physical snapshot must be independently equal to inventories"))
    expected_manifest = {
        "structure_manifest": document.get("structure_manifest"),
        "slide_occurrence_inventory": slides,
        "document_page_inventory": documents,
        "other_channel_inventory": channels,
        "release_artifact_manifest": artifact_manifest,
    }
    if release.get("current_manifest") != expected_manifest:
        errors.append(diagnostic("RELEASE_CURRENT_MANIFEST_MISMATCH", "final_release.current_manifest", "final manifest must bind structure and all physical channels"))
    channel_refs = {str(item.get("channel_ref")) for item in channels}
    events_by_id = dict_index(current_nodes(document)[1], "node_id")
    event_orders = {
        event_id: item.get("execution_order") for event_id, item in events_by_id.items()
        if isinstance(item.get("execution_order"), int)
    }
    exposure_orders = [item.get("student_exposure_order") for item in channels]
    ordered_channels = sorted(
        (item for item in channels if isinstance(item.get("student_exposure_order"), int)),
        key=lambda item: item.get("student_exposure_order"),
    )
    if (len(ordered_channels) != len(channels)
            or duplicates(exposure_orders)
            or any(
                event_orders.get(str(left.get("owner_event_id")), -1)
                > event_orders.get(str(right.get("owner_event_id")), -1)
                for left, right in zip(ordered_channels, ordered_channels[1:])
            )):
        errors.append(diagnostic("RELEASE_CHANNEL_ORDER_INVALID", "final_release.other_channel_inventory", "channel exposure orders must be unique and preserve owning-event execution order"))
    for index, channel in enumerate(channels):
        if channel.get("exposure_status") == "observed":
            errors.append(diagnostic("RELEASE_OBSERVED_BEFORE_TRIAL", f"final_release.other_channel_inventory[{index}]", "desktop release can claim scripted exposure only"))
        required_channel_fields = {
            "channel_ref", "channel_type", "source_artifact_id", "source_path", "source_sha256",
            "field_or_region", "content_sha256", "student_exposure_order", "owner_event_id",
            "exposure_status", "exposure_evidence_refs",
        }
        allowed_channel_types = {"teacher_spoken", "worksheet_region", "board", "audio", "other"}
        if channel.get("exposure_status") == "scripted" and (
            not required_channel_fields.issubset(channel)
            or any(not nonempty(channel.get(field)) for field in required_channel_fields - {"exposure_evidence_refs"})
            or not as_list(channel.get("exposure_evidence_refs"))
            or channel.get("channel_type") not in allowed_channel_types
        ):
            errors.append(diagnostic("RELEASE_SCRIPT_EVIDENCE_MISSING", f"final_release.other_channel_inventory[{index}]", "scripted channel needs a real script reference"))
        if (SHA256_RE.fullmatch(str(channel.get("source_sha256"))) is None
                or SHA256_RE.fullmatch(str(channel.get("content_sha256"))) is None):
            errors.append(diagnostic("RELEASE_SCRIPT_EVIDENCE_MISSING", f"final_release.other_channel_inventory[{index}]", "channel source and content hashes must be SHA-256"))
        artifact = artifacts.get(str(channel.get("source_artifact_id")))
        source_path = resolve_source_path(channel.get("source_path"))
        channel_type = str(channel.get("channel_type"))
        allowed_artifact_types_by_channel = {
            "teacher_spoken": {"docx", "pptx", "text"},
            "worksheet_region": {"docx", "pptx", "text"},
            "board": {"text"},
            "audio": {"audio"},
            "other": {"docx", "pptx", "text", "audio"},
        }
        content_hash = inspect_channel_content_hash(
            source_path, str((artifact or {}).get("type")), channel.get("field_or_region")
        ) if source_path is not None and artifact is not None else None
        if (artifact is None
                or (artifact or {}).get("type") not in allowed_artifact_types_by_channel.get(channel_type, set())
                or source_path is None
                or source_path != resolve_source_path(artifact.get("source_path"))
                or channel.get("source_sha256") != artifact.get("source_sha256")
                or content_hash is None
                or channel.get("content_sha256") != content_hash):
            errors.append(diagnostic("RELEASE_CHANNEL_SOURCE_MISMATCH", f"final_release.other_channel_inventory[{index}]", "scripted channel must bind a readable exact region in its current source artifact"))
        owner = events_by_id.get(str(channel.get("owner_event_id")))
        if owner is None or channel.get("channel_ref") not in as_list(owner.get("other_channel_refs")):
            errors.append(diagnostic("RELEASE_CHANNEL_OWNER_MISMATCH", f"final_release.other_channel_inventory[{index}].owner_event_id", "channel and event must reference each other"))
    _, events = current_nodes(document)
    for index, event in enumerate(events):
        if set(as_list(event.get("other_channel_refs"))) - channel_refs:
            errors.append(diagnostic("RELEASE_CHANNEL_OWNER_MISMATCH", f"current_release_audit.events[{index}].other_channel_refs", "event references a missing channel"))

    release_scan = release.get("release_deletion_scan")
    legacy_signatures = [
        signature
        for closure in as_list(document.get("legacy_disposition_closure"))
        if isinstance(closure, dict)
        for signature in as_list(closure.get("forbidden_reappearance_signatures"))
    ]
    detector_configuration = (release_scan or {}).get("detector_configuration") if isinstance(release_scan, dict) else None
    release_scan_state = release_deletion_source_state(
        artifact_manifest, slides, documents, channels, approved_assets, legacy_signatures, detector_configuration,
    )
    scan_receipt, scan_receipt_hash = read_json_receipt(
        release_scan.get("receipt_path") if isinstance(release_scan, dict) else None
    )
    expected_scan_receipt = {
        "check_type": "release_deletion_signatures",
        "source_state_sha256": audit_sha256(release_scan_state),
        "detector_configuration_sha256": audit_sha256(detector_configuration),
        "results": [],
    }
    if (not isinstance(release_scan, dict)
            or not isinstance(detector_configuration, dict)
            or set(detector_configuration) != {"text", "asset", "layout", "event"}
            or any(not nonempty(value) for value in detector_configuration.values())
            or release_scan.get("source_state_sha256") != expected_scan_receipt["source_state_sha256"]
            or release_scan.get("receipt_sha256") != scan_receipt_hash
            or scan_receipt != expected_scan_receipt):
        errors.append(diagnostic("RELEASE_DELETION_SCAN_INVALID", "final_release.release_deletion_scan", "release deletion scan must bind final Office, renders, channels, approved assets, signatures and all detector classes"))

    ledger = release.get("release_review_ledger")
    records = [item for item in as_list(ledger.get("records")) if isinstance(item, dict)] if isinstance(ledger, dict) else []
    bundle_hash = release.get("release_audit_bundle_sha256")
    record_by_id = dict_index(records, "review_id")
    tails: dict[tuple[Any, Any, Any], dict[str, Any]] = {}
    valid_chain = True
    seen_record_hashes: set[str] = set()
    previous_record_hash: str | None = None
    for record in records:
        key = (record.get("release_audit_bundle_sha256"), record.get("review_type"), record.get("object_key"))
        required_review_fields = {
            "review_id", "review_type", "object_key", "revision", "previous_ledger_hash",
            "supersedes_review_id", "release_audit_bundle_sha256", "status", "defect_ids",
            "reviewer_id", "reviewed_at", "record_hash",
        }
        if (not required_review_fields.issubset(record)
                or record.get("release_audit_bundle_sha256") != bundle_hash
                or record.get("review_type") not in {"student_occurrence", "visual_slide", "visual_document_page", "student_event"}
                or record.get("status") not in {"pending", "pass", "fail"}
                or not nonempty(record.get("reviewer_id")) or not nonempty(record.get("reviewed_at"))):
            valid_chain = False
        if record.get("previous_ledger_hash") != previous_record_hash:
            valid_chain = False
        body = {field: value for field, value in record.items() if field != "record_hash"}
        if record.get("record_hash") != canonical_sha256(body) or record.get("record_hash") in seen_record_hashes:
            valid_chain = False
        seen_record_hashes.add(str(record.get("record_hash")))
        previous_record_hash = str(record.get("record_hash"))
        previous = tails.get(key)
        if previous is None:
            if record.get("revision") != 1 or record.get("supersedes_review_id") is not None:
                valid_chain = False
        else:
            if record.get("revision") != previous.get("revision", 0) + 1 or record.get("supersedes_review_id") != previous.get("review_id"):
                valid_chain = False
        tails[key] = record
    if len(record_by_id) != len(records) or not valid_chain:
        errors.append(diagnostic("RELEASE_LEDGER_CHAIN_INVALID", "final_release.release_review_ledger.records", "ledger must be one append-only hash chain with linear revisions"))
    tail_records = list(tails.values())
    expected_effective_view = json.loads(json.dumps(tail_records, ensure_ascii=False))
    if release.get("effective_release_review_view") != expected_effective_view:
        errors.append(diagnostic("RELEASE_EFFECTIVE_REVIEW_VIEW_MISMATCH", "final_release.effective_release_review_view", "effective review view must contain exactly each ledger chain tail"))
    current_keys = {(item.get("review_type"), item.get("object_key")) for item in tail_records if item.get("status") == "pass"}
    expected_keys = (
        {("student_occurrence", item.get("occurrence_ref")) for item in slides if item.get("projected")}
        | {("visual_slide", item.get("occurrence_ref")) for item in slides}
        | {("visual_document_page", f"{item.get('artifact_id')}:{item.get('doc_page_index')}") for item in documents}
        | {("student_event", event_id) for event_id in manifest_events}
    )
    if not expected_keys.issubset(current_keys):
        errors.append(diagnostic("RELEASE_REVIEW_SET_MISMATCH", "final_release.release_review_ledger.records", "reviews must cover every projected occurrence, event and document page"))
    structure_reviewers = {
        str(record.get("reviewer"))
        for node in [*current_nodes(document)[0], *current_nodes(document)[1]]
        for record in (
            node.get("review_status", {}).get("self_review", {}),
            node.get("review_status", {}).get("student_reception", {}),
            node.get("review_status", {}).get("visual", {}),
        ) if isinstance(record, dict) and nonempty(record.get("reviewer"))
    }
    student_reviewers = {str(item.get("reviewer_id")) for item in tail_records if item.get("review_type") in {"student_occurrence", "student_event"}}
    visual_reviewers = {str(item.get("reviewer_id")) for item in tail_records if item.get("review_type") in {"visual_slide", "visual_document_page"}}
    if (structure_reviewers & (student_reviewers | visual_reviewers)) or student_reviewers & visual_reviewers:
        errors.append(diagnostic("RELEASE_REVIEW_INDEPENDENCE_INVALID", "final_release.release_review_ledger.records", "final student and visual reviewers must be independent from designers and each other"))
    for record in tail_records:
        if record.get("review_type") in {"student_occurrence", "student_event"}:
            required_simulation = {"simulated_seen", "simulated_heard", "simulated_activity_participation", "possible_understanding", "possible_misunderstanding", "possible_gain"}
            if not required_simulation.issubset(record) or any(not nonempty(record.get(field)) for field in required_simulation):
                errors.append(diagnostic("RELEASE_STUDENT_REVIEW_INVALID", f"review:{record.get('review_id')}", "student simulation must say what is seen, heard, done, understood, misunderstood and gained"))
            if record.get("review_type") == "student_event":
                event = events_by_id.get(str(record.get("object_key")))
                expected_carriers = []
                if event is not None:
                    for carrier_id in as_list(event.get("carrier_ids")):
                        expected_carriers.extend(
                            item.get("occurrence_ref") for item in slides
                            if item.get("page_id") == carrier_id and item.get("projected")
                        )
                expected_carriers.sort(key=lambda ref: next(
                    (item.get("physical_index", 0) for item in slides if item.get("occurrence_ref") == ref), 0
                ))
                expected_channels = sorted(
                    str(item.get("channel_ref")) for item in channels
                    if item.get("owner_event_id") == record.get("object_key") and item.get("exposure_status") == "scripted"
                )
                if (event is None
                        or as_list(record.get("ordered_carrier_occurrence_refs")) != expected_carriers
                        or sorted(str(item) for item in as_list(record.get("other_channel_evidence_refs"))) != expected_channels):
                    errors.append(diagnostic("RELEASE_STUDENT_EVENT_LINK_MISMATCH", f"review:{record.get('review_id')}", "student-event review must cover exactly its projected carriers and reciprocal scripted channels"))
        if record.get("review_type") in {"visual_slide", "visual_document_page"}:
            required_visual = {"source_artifact_sha256", "render_sha256", "render_evidence_refs", "visual_findings"}
            if (not required_visual.issubset(record)
                    or SHA256_RE.fullmatch(str(record.get("source_artifact_sha256"))) is None
                    or SHA256_RE.fullmatch(str(record.get("render_sha256"))) is None
                    or not as_list(record.get("render_evidence_refs")) or not nonempty(record.get("visual_findings"))):
                errors.append(diagnostic("RELEASE_VISUAL_REVIEW_INVALID", f"review:{record.get('review_id')}", "visual review must bind current Office source, render and findings"))
            object_key = str(record.get("object_key"))
            if record.get("review_type") == "visual_slide":
                occurrence = next((item for item in slides if item.get("occurrence_ref") == object_key), None)
                artifact = artifacts.get(str((occurrence or {}).get("artifact_id")))
                if (occurrence is None or artifact is None
                        or record.get("source_artifact_sha256") != artifact.get("source_sha256")
                        or record.get("render_sha256") != occurrence.get("render_sha256")
                        or record.get("approved_assets_manifest_sha256") != artifact.get("approved_assets_manifest_sha256")):
                    errors.append(diagnostic("RELEASE_VISUAL_REVIEW_STALE", f"review:{record.get('review_id')}", "slide review is stale against current Office source or approved asset/character manifest"))
                illustration = record.get("illustration_evidence")
                binding = page_asset_bindings.get(str((occurrence or {}).get("page_id")))
                observations = [item for item in as_list(record.get("three_second_observations")) if isinstance(item, dict)]
                observer_ids = [str(item.get("observer_id")) for item in observations]
                review_time = parse_timestamp(record.get("reviewed_at"))
                observation_receipts_valid = True
                for observation in observations:
                    receipt, receipt_hash = read_json_receipt(observation.get("receipt_path"))
                    expected_receipt = {
                        key: observation.get(key) for key in (
                            "observer_id", "observed_at", "render_sha256", "primary_object_first",
                            "recognized_core", "misreading",
                        )
                    }
                    observed_time = parse_timestamp(observation.get("observed_at"))
                    if (receipt != expected_receipt or receipt_hash != observation.get("receipt_sha256")
                            or observed_time is None or review_time is None or observed_time > review_time
                            or observed_time > datetime.now(timezone.utc)):
                        observation_receipts_valid = False
                if (not isinstance(illustration, dict)
                        or illustration.get("status") not in {"approved_to_use", "no_image_required"}
                        or illustration.get("page_binding_ref") != (occurrence or {}).get("page_id")
                        or illustration.get("status") != (binding or {}).get("status")
                        or illustration.get("instructional_gain") != (binding or {}).get("instructional_gain")):
                    errors.append(diagnostic("RELEASE_VISUAL_FUNCTION_GAIN_INVALID", f"review:{record.get('review_id')}.illustration_evidence", "visual review must verify the page-specific instructional gain"))
                if (len(observations) != 2 or len(set(observer_ids)) != 2
                        or record.get("reviewer_id") in set(observer_ids)
                        or any(item.get("primary_object_first") is not True
                               or not nonempty(item.get("recognized_core"))
                               or nonempty(item.get("misreading"))
                               or not nonempty(item.get("observed_at"))
                               or not nonempty(item.get("receipt_path"))
                               or item.get("render_sha256") != record.get("render_sha256")
                               or SHA256_RE.fullmatch(str(item.get("receipt_sha256"))) is None
                               for item in observations)):
                    errors.append(diagnostic("RELEASE_THREE_SECOND_TEST_INVALID", f"review:{record.get('review_id')}.three_second_observations", "two fresh observers must first see the poem/task, recognize the core, and report no new misreading"))
                elif not observation_receipts_valid:
                    errors.append(diagnostic("RELEASE_OBSERVER_PROVENANCE_INVALID", f"review:{record.get('review_id')}.three_second_observations", "observer records must match readable receipts for the current render and precede review"))
            else:
                artifact_id, _, page_index = object_key.rpartition(":")
                document_page = next((item for item in documents if item.get("artifact_id") == artifact_id and str(item.get("doc_page_index")) == page_index), None)
                artifact = artifacts.get(artifact_id)
                if (document_page is None or artifact is None
                        or record.get("source_artifact_sha256") != artifact.get("source_sha256")
                        or record.get("render_sha256") != document_page.get("render_sha256")):
                    errors.append(diagnostic("RELEASE_VISUAL_REVIEW_STALE", f"review:{record.get('review_id')}", "document review is stale against current source or rendered page"))
            if record.get("review_type") == "visual_slide" and SHA256_RE.fullmatch(str(record.get("approved_assets_manifest_sha256"))) is None:
                errors.append(diagnostic("RELEASE_VISUAL_REVIEW_INVALID", f"review:{record.get('review_id')}", "slide visual review must bind approved asset/character manifest"))
    review_defects = {str(defect_id) for item in records for defect_id in as_list(item.get("defect_ids"))}
    registry = dict_index(as_list(ledger.get("release_defect_registry")), "defect_id") if isinstance(ledger, dict) else {}

    def release_object_state(object_ref: str) -> Any:
        occurrence = next((item for item in slides if item.get("occurrence_ref") == object_ref), None)
        if occurrence is not None:
            return occurrence
        event = events_by_id.get(object_ref)
        if event is not None:
            return event
        if ":" in object_ref:
            artifact_id, _, page_index = object_ref.rpartition(":")
            document_page = next((
                item for item in documents
                if item.get("artifact_id") == artifact_id and str(item.get("doc_page_index")) == page_index
            ), None)
            if document_page is not None:
                return document_page
        channel = next((item for item in channels if item.get("channel_ref") == object_ref), None)
        return channel
    if review_defects != set(registry):
        errors.append(diagnostic("RELEASE_DEFECT_REGISTRY_MISMATCH", "final_release.release_review_ledger", "review defect IDs and release registry must be bidirectionally equal"))
    registry_links_valid = all(
        isinstance(defect, dict)
        and {
            "defect_id", "severity", "object_ref", "review_record_ref", "claim", "evidence_refs",
            "reviewer_id", "discovered_at", "source_state_sha256",
        }.issubset(defect)
        and defect.get("severity") in {"P0", "P1", "P2", "P3"}
        and nonempty(defect.get("object_ref")) and nonempty(defect.get("claim"))
        and as_list(defect.get("evidence_refs"))
        and SHA256_RE.fullmatch(str(defect.get("source_state_sha256"))) is not None
        and release_object_state(str(defect.get("object_ref"))) is not None
        and defect.get("review_record_ref") in record_by_id
        and defect_id in as_list(record_by_id.get(str(defect.get("review_record_ref")), {}).get("defect_ids"))
        and defect.get("reviewer_id") == record_by_id.get(str(defect.get("review_record_ref")), {}).get("reviewer_id")
        for defect_id, defect in registry.items()
    )
    if not registry_links_valid:
        errors.append(diagnostic("RELEASE_DEFECT_REGISTRY_MISMATCH", "final_release.release_review_ledger.release_defect_registry", "registry must point back to the immutable discovering review"))
    closures = [item for item in as_list(ledger.get("release_defect_closures")) if isinstance(item, dict)] if isinstance(ledger, dict) else []
    valid_closures: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for closure in closures:
        defect = registry.get(str(closure.get("defect_id")))
        required_closure_fields = {
            "defect_id", "fix_refs", "before_sha256", "after_sha256", "original_reviewer_id",
            "reviewer_verification_status", "reviewed_at", "closure_status", "verified_source_state_sha256",
        }
        if (defect is not None and required_closure_fields.issubset(closure)
                and as_list(closure.get("fix_refs"))
                and SHA256_RE.fullmatch(str(closure.get("before_sha256"))) is not None
                and SHA256_RE.fullmatch(str(closure.get("after_sha256"))) is not None
                and closure.get("before_sha256") == defect.get("source_state_sha256")
                and closure.get("after_sha256") != closure.get("before_sha256")
                and closure.get("original_reviewer_id") == defect.get("reviewer_id")
                and closure.get("reviewer_verification_status") == "pass"
                and nonempty(closure.get("reviewed_at")) and closure.get("closure_status") == "closed"
                and closure.get("verified_source_state_sha256") == closure.get("after_sha256")
                and closure.get("after_sha256") == audit_sha256(release_object_state(str(defect.get("object_ref"))))):
            valid_closures[str(closure.get("defect_id"))].append(closure)
    p0_p2 = {defect_id for defect_id, defect in registry.items() if defect.get("severity") in {"P0", "P1", "P2"}}
    closed_ids = {defect_id for defect_id in p0_p2 if len(valid_closures.get(defect_id, [])) == 1}
    summary = release.get("final_defect_closure_summary")
    if (closed_ids != p0_p2 or not isinstance(summary, dict)
            or set(as_list(summary.get("closed_p0_p1_p2_ids"))) != p0_p2
            or summary.get("open_p0_p1_p2_count") != 0):
        errors.append(diagnostic("RELEASE_DEFECT_CLOSURE_INVALID", "final_release.final_defect_closure_summary", "every P0-P2 defect needs exactly one current original-reviewer-verified closure"))

    # Final evidence is a forward-only chain: candidate sources → release
    # bundle → append-only reviews/closures → attestation.  Recompute each
    # layer rather than accepting a producer's self-reported digest.
    errors.extend(validate_bundle(release.get("release_audit_bundle"), "release_audit_bundle", {
        "structure_audit_bundle": document.get("structure_audit_bundle"),
        "release_artifact_manifest": artifact_manifest,
        "slide_occurrence_inventory": slides,
        "document_page_inventory": documents,
        "other_channel_inventory": channels,
        "current_manifest": release.get("current_manifest"),
    }, "final_release.release_audit_bundle"))
    if isinstance(release.get("release_audit_bundle"), dict) and bundle_hash != release.get("release_audit_bundle", {}).get("bundle_sha256"):
        errors.append(diagnostic("AUDIT_BUNDLE_HASH_MISMATCH", "final_release.release_audit_bundle_sha256", "ledger bundle binding must equal recomputed release bundle"))

    scorecard = release.get("final_scorecard")
    dimension_names = (
        "文本、教材和认识边界", "学生接收连续性与问题时机", "页面必要性与因果闭合",
        "参与覆盖、倾听、追问和修订", "语文质地、体验和课堂剧本", "视觉、插图与跨文件实施质量",
    )
    dimension_maxima = [20, 20, 20, 15, 15, 10]
    if not isinstance(scorecard, dict) or len(as_list(scorecard.get("dimensions"))) != 6:
        errors.append(diagnostic("RELEASE_SCORECARD_INVALID", "final_release.final_scorecard", "scorecard needs six fixed dimensions"))
    else:
        dimensions = scorecard.get("dimensions")
        computed_total = 0
        pages_by_id, event_objects = current_nodes(document)
        evidence_objects: dict[str, Any] = {str(item.get("node_id")): item for item in pages_by_id}
        evidence_objects.update({str(item.get("node_id")): item for item in event_objects})
        evidence_objects.update({artifact_id: artifact for artifact_id, artifact in artifacts.items()})
        evidence_objects.update({str(item.get("channel_ref")): item for item in channels})
        for index, (dimension, maximum, dimension_name) in enumerate(zip(dimensions, dimension_maxima, dimension_names)):
            evidence_refs = as_list(dimension.get("evidence_refs")) if isinstance(dimension, dict) else []
            evidence_valid = True
            for reference in evidence_refs:
                if not isinstance(reference, str) or not REFERENCE_RE.fullmatch(reference):
                    evidence_valid = False
                    break
                object_id, field_path = reference.split("#", 1)
                current: Any = evidence_objects.get(object_id)
                for part in field_path.split("."):
                    if isinstance(current, dict) and part in current:
                        current = current[part]
                    else:
                        current = None
                        break
                if not nonempty(current):
                    evidence_valid = False
                    break
            if (not isinstance(dimension, dict) or dimension.get("dimension") != dimension_name
                    or dimension.get("maximum") != maximum
                    or not isinstance(dimension.get("score"), (int, float))
                    or dimension.get("score") < maximum * 0.9 or dimension.get("score") > maximum
                    or not evidence_refs or not evidence_valid):
                errors.append(diagnostic("RELEASE_SCORECARD_INVALID", f"final_release.final_scorecard.dimensions[{index}]", "each dimension must meet its 90% floor with evidence"))
                continue
            computed_total += dimension.get("score")
        if scorecard.get("total_score") != computed_total or computed_total < 95:
            errors.append(diagnostic("RELEASE_SCORECARD_INVALID", "final_release.final_scorecard.total_score", "total must be mechanically summed and at least 95"))
    errors.extend(validate_bundle(release.get("release_attestation"), "release_attestation", {
        "release_audit_bundle": release.get("release_audit_bundle"),
        "release_review_ledger": ledger,
        "effective_release_review_view": release.get("effective_release_review_view"),
        "final_defect_closure_summary": summary,
        "final_scorecard": scorecard,
    }, "final_release.release_attestation"))
    return errors


def validate_audit_document(document: Any, mode: str = "stage") -> list[dict[str, str]]:
    if mode not in MODES:
        return [diagnostic("AUDIT_MODE_INVALID", "mode", f"invalid mode: {mode}")]
    if not isinstance(document, dict):
        return [diagnostic("AUDIT_DOCUMENT_INVALID", "$", "audit document must be an object")]
    errors: list[dict[str, str]] = []
    if document.get("schema_version") != "2.0" or document.get("audit_version") != "6.0-page-function-audit":
        errors.append(diagnostic("AUDIT_VERSION_INVALID", "schema_version", "expected schema 2.0 and V6 page-function audit"))
    status = document.get("document_status")
    if status not in DOCUMENT_STATUSES:
        errors.append(diagnostic("AUDIT_DOCUMENT_STATUS_INVALID", "document_status", "document status must be a fixed V6 lifecycle value"))
    if document.get("claim_boundary") != "desktop_design_scaffold_only":
        errors.append(diagnostic("AUDIT_CLAIM_BOUNDARY_INVALID", "claim_boundary", "audit may claim desktop design evidence only"))
    current_audit = document.get("current_release_audit")
    valid_current_pages, valid_current_events = current_nodes(document)
    honest_empty_current = not valid_current_pages and not valid_current_events
    if not isinstance(current_audit, dict):
        errors.append(diagnostic("CURRENT_AUDIT_CONTAINER_INVALID", "current_release_audit", "current audit must be an object"))
    else:
        for field in ("pages", "events"):
            values = current_audit.get(field)
            if not isinstance(values, list) or any(not isinstance(item, dict) for item in values):
                errors.append(diagnostic(
                    "CURRENT_AUDIT_NODE_TYPE_INVALID", f"current_release_audit.{field}",
                    "current audit node arrays must contain objects only",
                ))
    legacy_items = as_list(document.get("legacy_initial_audit"))
    if mode == "stage" and honest_empty_current and len(legacy_items) == 127 and status != "legacy_skeleton_pending_review":
        errors.append(diagnostic(
            "AUDIT_DOCUMENT_STATUS_SHAPE_INVALID", "document_status",
            "an empty current structure with 127 legacy pages is the Task 3 legacy skeleton",
        ))
    if status == "legacy_skeleton_pending_review" and mode != "stage":
        errors.append(diagnostic("AUDIT_DOCUMENT_STATUS_MODE_INVALID", "document_status", "legacy skeleton is valid only in stage mode"))
    if status == "release_ready" and mode != "release":
        errors.append(diagnostic("AUDIT_DOCUMENT_STATUS_MODE_INVALID", "document_status", "release_ready is valid only in release mode"))
    required = {
        "document_status", "claim_boundary",
        "legacy_initial_audit", "legacy_event_evidence", "defect_registry", "initial_audit_seals",
        "seal_amendments", "effective_legacy_hash", "legacy_disposition_closure", "structure_manifest",
        "declared_node_inventory", "source_graph_inventory", "structure_assembly_snapshot",
        "current_release_audit", "global_checks",
    }
    for field in sorted(required - set(document)):
        errors.append(diagnostic("AUDIT_REQUIRED_FIELD", field, "top-level field is missing"))
    errors.extend(validate_stage_skeleton_sources(document, mode))
    errors.extend(validate_legacy_layer(document, mode))
    errors.extend(validate_dispositions(document, mode))
    errors.extend(validate_current_layer(document, mode))
    if mode in {"freeze-candidate", "freeze", "release"}:
        errors.extend(validate_bundle(document.get("structure_audit_bundle"), "structure_audit_bundle", {
            "structure_manifest": document.get("structure_manifest"),
            "current_release_audit": document.get("current_release_audit"),
            "legacy_effective_view": document.get("legacy_effective_view"),
            "legacy_disposition_closure": document.get("legacy_disposition_closure"),
        }, "structure_audit_bundle"))
    checks = document.get("global_checks")
    if mode in {"freeze-candidate", "freeze", "release"}:
        required_checks = {
            "lossless_merge_candidates", "lossless_merge_scan_sha256", "lossless_merge_scan_source_sha256",
            "deletion_signature_hits", "deletion_scan_sha256", "deletion_scan_source_sha256",
        }
        if (not isinstance(checks, dict) or not required_checks.issubset(checks)
                or any(SHA256_RE.fullmatch(str(checks.get(field))) is None for field in (
                    "lossless_merge_scan_sha256", "lossless_merge_scan_source_sha256",
                    "deletion_scan_sha256", "deletion_scan_source_sha256",
                ))):
            errors.append(diagnostic("CURRENT_GLOBAL_CHECKS_MISSING", "global_checks", "freeze/release requires merge and deletion scan receipts bound to their source state"))
        else:
            merge_source = audit_sha256({
                "structure_manifest": document.get("structure_manifest"),
                "current_release_audit": document.get("current_release_audit"),
            })
            deletion_source = audit_sha256({
                "legacy_effective_view": document.get("legacy_effective_view"),
                "legacy_disposition_closure": document.get("legacy_disposition_closure"),
                "current_release_audit": document.get("current_release_audit"),
            })
            merge_receipt, merge_receipt_hash = read_json_receipt(checks.get("lossless_merge_receipt_path"))
            deletion_receipt, deletion_receipt_hash = read_json_receipt(checks.get("deletion_scan_receipt_path"))
            expected_merge = {
                "check_type": "lossless_merge", "source_state_sha256": merge_source,
                "results": as_list(checks.get("lossless_merge_candidates")),
            }
            expected_deletion = {
                "check_type": "deletion_signatures", "source_state_sha256": deletion_source,
                "results": as_list(checks.get("deletion_signature_hits")),
            }
            if (checks.get("lossless_merge_scan_source_sha256") != merge_source
                    or checks.get("deletion_scan_source_sha256") != deletion_source
                    or merge_receipt != expected_merge or merge_receipt_hash != checks.get("lossless_merge_scan_sha256")
                    or deletion_receipt != expected_deletion or deletion_receipt_hash != checks.get("deletion_scan_sha256")):
                errors.append(diagnostic("CURRENT_GLOBAL_CHECKS_STALE", "global_checks", "global scan receipts must be readable and bind current structure, closures and exact results"))
        if isinstance(checks, dict) and as_list(checks.get("lossless_merge_candidates")):
            errors.append(diagnostic("CURRENT_LOSSLESS_MERGE_REMAINS", "global_checks.lossless_merge_candidates", "mergeable current pages block freeze"))
        if isinstance(checks, dict) and as_list(checks.get("deletion_signature_hits")):
            errors.append(diagnostic("DISPOSITION_DELETION_REAPPEARED", "global_checks.deletion_signature_hits", "deleted content reappeared elsewhere"))
    if mode == "release":
        errors.extend(validate_release(document))
    return errors


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="UTF-8 three-layer audit JSON")
    parser.add_argument("--mode", choices=tuple(sorted(MODES)), default="stage")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        document = json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"AUDIT_INPUT_ERROR\t{args.input}\t{error}", file=sys.stderr)
        return 2
    errors = validate_audit_document(document, mode=args.mode)
    if errors:
        for error in errors:
            print(f"{error['code']}\t{error['path']}\t{error['message']}", file=sys.stderr)
        print(f"AUDIT_FAILED errors={len(errors)} mode={args.mode}", file=sys.stderr)
        return 1
    pages, events = current_nodes(document)
    print(f"AUDIT_OK pages={len(pages)} events={len(events)} mode={args.mode}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
