from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.validate_meng_v6_page_audit import audit_sha256, build_bundle, inspect_pptx, validate_audit_document


_ARTIFACT_TEMP = tempfile.TemporaryDirectory(prefix="meng_v6_audit_", dir=Path(__file__).resolve().parents[1])
ARTIFACT_DIR = Path(_ARTIFACT_TEMP.name)


def fixture_files() -> dict[str, Path]:
    pptx = ARTIFACT_DIR / "main.pptx"
    docx = ARTIFACT_DIR / "teacher.docx"
    slide_render = ARTIFACT_DIR / "slide-1.png"
    doc_render = ARTIFACT_DIR / "doc-1.png"
    doc_render_receipt = ARTIFACT_DIR / "doc-1-render.json"
    pagination_pdf = ARTIFACT_DIR / "teacher.pdf"
    pagination_receipt = ARTIFACT_DIR / "teacher-pagination.json"
    character_manifest_path = ARTIFACT_DIR / "characters.json"
    teacher_line = "请把退出条放进收集袋。"
    with zipfile.ZipFile(pptx, "w") as package:
        package.writestr(
            "ppt/presentation.xml",
            '<p:presentation xmlns:p="urn:p" xmlns:r="urn:r"><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst></p:presentation>',
        )
        package.writestr(
            "ppt/_rels/presentation.xml.rels",
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/></Relationships>',
        )
        package.writestr("ppt/slides/slide1.xml", '<p:sld xmlns:p="urn:p" show="1"><p:cSld><p:sp><p:txBody>V6_PAGE_ID:N001 V6_ASSET_IDS:</p:txBody></p:sp></p:cSld></p:sld>')
    with zipfile.ZipFile(docx, "w") as package:
        package.writestr(
            "word/document.xml",
            f'<w:document xmlns:w="urn:w"><w:body><w:p><w:r><w:t>V6_REGION:E_END#teacher_line::{teacher_line}::V6_END_REGION</w:t></w:r></w:p></w:body></w:document>',
        )
    slide_render.write_bytes(b"slide-render-v1")
    doc_render.write_bytes(b"doc-render-v1")
    create_one_page_pdf(pagination_pdf)
    pagination_receipt.write_text(json.dumps({
        "check_type": "docx_pagination", "source_sha256": file_digest(docx),
        "pdf_sha256": file_digest(pagination_pdf), "page_count": 1,
        "renderer": "fixture-pdf-writer-v1", "renderer_parameters": {"paper": "A4"},
    }, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    doc_render_receipt.write_text(json.dumps({
        "check_type": "document_page_render", "pagination_pdf_sha256": file_digest(pagination_pdf),
        "doc_page_index": 1, "render_sha256": file_digest(doc_render),
        "renderer": "fixture-page-render-v1", "renderer_parameters": {"dpi": 150},
    }, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    characters = []
    for character in ("W01", "M01"):
        for stage in ("T", "A", "B", "C"):
            characters.append({
                "character_version": f"{character}-{stage}",
                "views": ["front", "side", "back", "three_quarter"],
                "clothing_id": f"{character[0]}_C{stage}", "hairstyle_id": f"{character[0]}_H{stage}",
                "clothing_colors": ["#CBBE9E", "#78806B"] if character == "W01" and stage == "T" else [],
                "hair_color": "#2B2723" if character == "W01" else "#282521",
                "facial_anchor_id": f"{character}_FACE_V1", "silhouette_anchor_id": f"{character}_BODY_V1",
                "prop_ids": [],
                "proportion": {
                    "head_to_body_ratio": 6.5 if character == "W01" else 6.7,
                    "shared_frame_height": 1.00 if character == "W01" else 1.06,
                },
            })
    character_manifest_path.write_text(json.dumps({
        "schema_version": "1.0", "style_id": "warm-handdrawn-low-saturation-v1", "characters": characters,
        "clothing_color_anchors": {
            "W_CT": ["#CBBE9E", "#78806B"], "W_CA": ["#C7B58F", "#68745C", "#8A6650"],
            "W_CB": ["#B9A27F", "#687064"], "W_CC": ["#918675", "#5F6867"],
            "M_CT": ["#8A806D", "#686157"], "M_CA": ["#766B5B", "#575147", "#695542"],
            "M_CB": ["#6C6255", "#514C45"], "M_CC": ["#5C554C", "#494641"],
        },
        "shared_frame_proportions": [{"pair": f"W01-{stage}/M01-{stage}", "ratio": "1.00:1.06"} for stage in ("T", "A", "B", "C")],
    }, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    return {
        "pptx": pptx, "docx": docx, "slide_render": slide_render, "doc_render": doc_render,
        "pagination_pdf": pagination_pdf, "pagination_receipt": pagination_receipt,
        "doc_render_receipt": doc_render_receipt,
        "character_manifest": character_manifest_path,
        "teacher_line": teacher_line,
    }


def create_one_page_pdf(path: Path) -> None:
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << >> /Contents 4 0 R >>",
        b"<< /Length 0 >>\nstream\n\nendstream",
    ]
    payload = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, body in enumerate(objects, start=1):
        offsets.append(len(payload))
        payload.extend(f"{index} 0 obj\n".encode("ascii"))
        payload.extend(body)
        payload.extend(b"\nendobj\n")
    xref = len(payload)
    payload.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    payload.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        payload.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    payload.extend(f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii"))
    path.write_bytes(bytes(payload))


def two_asset_pptx(path: Path, first: Path, second: Path) -> list[dict]:
    with zipfile.ZipFile(path, "w") as package:
        package.writestr("ppt/presentation.xml", '<p:presentation xmlns:p="urn:p" xmlns:r="urn:r"><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst></p:presentation>')
        package.writestr("ppt/_rels/presentation.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/></Relationships>')
        package.writestr("ppt/slides/slide1.xml", '<p:sld xmlns:p="urn:p"><p:cSld>V6_PAGE_ID:N001 V6_ASSET_IDS:A_M,A_W V6_ASSET_RELATIONSHIPS:A_W@rId7,A_M@rId8</p:cSld></p:sld>')
        package.writestr("ppt/slides/_rels/slide1.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/w.png"/><Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/m.png"/></Relationships>')
        package.writestr("ppt/media/w.png", first.read_bytes())
        package.writestr("ppt/media/m.png", second.read_bytes())
    return inspect_pptx(path)[0]["media_bindings"]


def configure_two_asset_release(document: dict, stem: str) -> tuple[dict, list[dict]]:
    first = ARTIFACT_DIR / f"{stem}-w.png"
    second = ARTIFACT_DIR / f"{stem}-m.png"
    pptx = ARTIFACT_DIR / f"{stem}.pptx"
    first.write_bytes(f"{stem}-w".encode("utf-8"))
    second.write_bytes(f"{stem}-m".encode("utf-8"))
    bindings = two_asset_pptx(pptx, first, second)
    release = document["final_release"]
    artifact = release["release_artifact_manifest"]["artifacts"][0]
    artifact["source_path"] = str(pptx)
    artifact["source_sha256"] = file_digest(pptx)
    artifact["file_observation"]["observed_source_sha256"] = file_digest(pptx)
    occurrence = release["slide_occurrence_inventory"][0]
    occurrence["embedded_asset_ids"] = ["A_M", "A_W"]
    occurrence["media_sha256"] = sorted([file_digest(first), file_digest(second)])
    occurrence["media_bindings"] = bindings
    occurrence["image_relationship_count"] = 2
    approved = release["approved_visual_assets_manifest"]
    approved["assets"] = [
        {"asset_id": "A_W", "source_path": str(first), "source_sha256": file_digest(first),
         "character_versions": ["W01-A"], "status": "approved"},
        {"asset_id": "A_M", "source_path": str(second), "source_sha256": file_digest(second),
         "character_versions": ["M01-A"], "status": "approved"},
    ]
    approved["page_bindings"][0].update({
        "status": "approved_to_use", "poem_evidence_refs": ["N001#unique_function"],
        "allowed_facts": ["人物在场"], "forbidden_inferences": ["不得越界"],
        "no_image_alternative": "保留原诗", "asset_ids": ["A_M", "A_W"],
        "character_versions": ["M01-A", "W01-A"],
    })
    return occurrence, bindings


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(value: object) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def gate(gate_id: str, status: str = "pass", code: str | None = None) -> dict:
    return {
        "gate_id": gate_id,
        "gate_status": status,
        "evidence_refs": [] if status == "pending" else [f"E_END#{gate_id}"],
        "failure_code": code,
        "reviewer": None if status == "pending" else "audit-reviewer",
        "reviewed_at": None if status == "pending" else "2026-08-13T08:00:00+08:00",
    }


def structure_review() -> dict:
    return {
        "scope": "structure_only",
        "self_review": {"status": "pass", "reviewer": "designer", "reviewed_at": "2026-08-13T08:00:00+08:00", "defect_ids": []},
        "student_reception": {"status": "pass", "reviewer": "student-reviewer", "reviewed_at": "2026-08-13T08:10:00+08:00", "defect_ids": []},
        "visual": {"status": "pass", "reviewer": "visual-reviewer", "reviewed_at": "2026-08-13T08:20:00+08:00", "defect_ids": []},
        "consensus": "passed",
        "adjudication": None,
    }


def legacy_page(number: int) -> dict:
    page_id = f"S{number:03d}"
    return {
        "node_id": page_id,
        "page_id": page_id,
        "node_type": "page",
        "audit_scope": "learning_page",
        "learning_unit": "LEGACY_UNIT",
        "owner_event_id": None,
        "unit_role": "澄清",
        "supporting_move": "朗读",
        "prerequisite": "学生已经看见本页所引原诗",
        "epistemic_status": "文本明写",
        "unique_function": f"诊断旧页{page_id}的原有功能",
        "student_input": "本页原诗",
        "student_action": {"actor": "每名学生", "action": "圈画", "object": "关键字", "duration_seconds": 20, "artifact": "一处圈画"},
        "voice_coverage": {"all_have_entry": True, "independent_entry": "先独立圈画", "selection_method": "随机抽取并允许补充"},
        "listener_task": {"task": "核对同伴所引原句", "artifact": "补记一处差异", "reuse": "章末回读时修订"},
        "observable_change": {"before": "未定位", "after": "已定位", "criterion": "能指出原句"},
        "artifact_location": "教材旁批",
        "previous_relation": "承接整章初读",
        "next_relation": "进入章末回读",
        "deletion_loss": "失去对原句的定位证据",
        "merge_test": {"result": "cannot_merge", "cannot_merge_reason": "需保持原句远距可读"},
        "channel_split": {"screen": "原诗", "teacher": "追问", "worksheet": "旁批位置"},
        "framework_cost": "不新增术语",
        "primary_visual_duty": "原文批注",
        "secondary_visual": "章序定位",
        "time_value": {"minutes": 1, "irreplaceable_gain": "形成原句定位"},
        "content_elements": [{"element_id": "function", "kind": "function", "source_field": "unique_function"}],
        "legacy_student_visible": number != 1,
        "review_status": structure_review(),
        "gates": [gate(f"G{i}") for i in range(1, 7)],
    }


def current_page(legacy_ids: list[str]) -> dict:
    function = "让学生提交退出条，保存仍未解决的问题"
    return {
        "node_id": "N001",
        "page_id": "N001",
        "node_type": "page",
        "audit_scope": "learning_page",
        "execution_order": 1,
        "release_status": "final",
        "learning_unit": "E_END",
        "owner_event_id": None,
        "unit_role": "收束",
        "supporting_move": "书写",
        "prerequisite": "已经完成全文终读与知识收纳",
        "epistemic_status": "课堂生成",
        "unique_function": function,
        "student_input": "全文终读后的个人理解",
        "student_action": {"actor": "每名学生", "action": "写下", "object": "一项理解和一个问题", "duration_seconds": 90, "artifact": "退出条"},
        "voice_coverage": {"all_have_entry": True, "independent_entry": "每人独立书写", "selection_method": "全员交付"},
        "listener_task": {"task": "听取两份匿名退出条并核对自己的差异", "artifact": "一处补记", "reuse": "课后修订"},
        "observable_change": {"before": "理解未保存", "after": "形成一项判断和一个问题", "criterion": "退出条可核验"},
        "artifact_location": "退出条",
        "previous_relation": "调用全文终读形成的判断",
        "next_relation": "交付给终端事件用于课后诊断",
        "deletion_loss": "无法获得每名学生的课后诊断入口",
        "merge_test": {"result": "cannot_merge", "cannot_merge_reason": "需要独立安静书写和交付"},
        "channel_split": {"screen": "一句任务", "teacher": "等待并收取", "worksheet": "退出条书写区"},
        "framework_cost": "不新增概念",
        "primary_visual_duty": "活动界面",
        "secondary_visual": "交付位置提示",
        "time_value": {"minutes": 2, "irreplaceable_gain": "获得全员可保存诊断"},
        "next_use_refs": [{
            "target_event_id": "E_END",
            "source_artifact_field": "artifact_location",
            "target_input_field": "inputs[0]",
            "expected_use": "交付并形成课后诊断材料",
        }],
        "legacy_source_refs": legacy_ids,
        "inherited_functions": [
            {"legacy_id": item, "element_id": "function", "target_field": "unique_function"}
            for item in legacy_ids
        ],
        "review_status": structure_review(),
        "gates": [gate(f"G{i}") for i in range(1, 7)],
    }


def terminal_event() -> dict:
    return {
        "node_id": "E_END",
        "event_id": "E_END",
        "node_type": "event",
        "audit_scope": "learning_event",
        "execution_order": 2,
        "batch": "final",
        "implemented": True,
        "inputs": [{
            "source_node_id": "N001",
            "source_artifact_field": "artifact_location",
            "input_field": "inputs[0]",
        }],
        "actions": ["学生交付退出条"],
        "artifacts": ["退出条"],
        "observable_change": {"before": "未保存", "after": "已交付", "criterion": "收集位置可核验"},
        "artifact_locations": ["班级收集袋"],
        "next_uses": [],
        "carrier_ids": [],
        "owner_page_ids": ["N001"],
        "other_channel_refs": ["SCRIPT:E_END"],
        "gate_4": gate("G4"),
        "gate_5": gate("G5"),
        "evidence_refs": ["N001#artifact_location"],
        "legacy_source_refs": [],
        "inherited_functions": [],
        "release_status": "final",
        "terminal_sink": True,
        "terminal_use": {
            "final_artifact": "退出条",
            "recipient_or_owner": "教师与学生本人",
            "post_class_use": "教师诊断问题，学生保留继续阅读的入口",
            "artifact_location": "班级收集袋或学生学习档案",
            "delivery_evidence_refs": ["N001#artifact_location"],
            "no_further_classroom_call_reason": "全课最后一个学习事件",
        },
        "review_status": structure_review(),
    }


def valid_freeze_document() -> dict:
    legacy = [legacy_page(i) for i in range(1, 128)]
    legacy_ids = [item["page_id"] for item in legacy]
    page = current_page(legacy_ids)
    event = terminal_event()
    effective_legacy_hash = digest(legacy)
    target_hash = digest(page["unique_function"])
    audit_hash = digest(page)
    closures = []
    for legacy_id in legacy_ids:
        mapping = [{"element_id": "function", "target_ref": "page:N001", "target_field": "unique_function"}]
        closures.append({
            "legacy_id": legacy_id,
            "based_on_effective_hash": effective_legacy_hash,
            "decision": "保留",
            "decision_status": "final",
            "target_refs": ["page:N001"],
            "legacy_content_elements": [{"element_id": "function", "kind": "function", "source_field": "unique_function"}],
            "required_carry_forward": ["function"],
            "forbidden_reappearance_signatures": [],
            "element_mappings": mapping,
            "coverage_result": "complete",
            "decision_evidence": ["N001#unique_function"],
            "initial_failure_codes": [],
            "closed_failure_codes": [],
            "initial_defect_ids": [],
            "closed_defect_ids": [],
            "defect_closures": [],
            "target_field_sha256": target_hash,
            "element_mapping_sha256": digest(mapping),
            "current_audit_node_sha256": audit_hash,
            "closure_status": "closed",
            "closure_evidence_refs": ["N001#unique_function"],
            "review_status": {"status": "pass", "reviewer": "legacy-reviewer"},
        })

    seal_base = {
        "seal_id": "SEAL_ALL",
        "source_path": "scripts/meng_v6/audit/all.json",
        "legacy_ids": legacy_ids,
        "source_sha256": digest(legacy),
        "legacy_event_evidence_sha256": digest([]),
        "author_id": "legacy-auditor",
        "reviewer_ids": ["student-reviewer", "visual-reviewer"],
        "review_evidence": [{"legacy_id": item, "gate_refs": [f"{item}#gates"]} for item in legacy_ids],
        "sealed_at": "2026-08-13T09:00:00+08:00",
    }
    seal = {**seal_base, "seal_hash": digest(seal_base)}
    manifest = {
        "pages": [{"node_id": "N001", "execution_order": 1, "module": "final"}],
        "events": [{"node_id": "E_END", "execution_order": 2, "module": "final"}],
        "g5_edges": [{"source_node_id": "N001", "target_event_id": "E_END"}],
    }
    merge_source = digest({"structure_manifest": manifest, "current_release_audit": {"pages": [page], "events": [event]}})
    deletion_source = digest({
        "legacy_effective_view": legacy, "legacy_disposition_closure": closures,
        "current_release_audit": {"pages": [page], "events": [event]},
    })
    merge_receipt_path = ARTIFACT_DIR / "merge-scan.json"
    deletion_receipt_path = ARTIFACT_DIR / "deletion-scan.json"
    merge_receipt_path.write_text(json.dumps({"check_type": "lossless_merge", "source_state_sha256": merge_source, "results": []}, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    deletion_receipt_path.write_text(json.dumps({"check_type": "deletion_signatures", "source_state_sha256": deletion_source, "results": []}, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    result = {
        "schema_version": "2.0",
        "audit_version": "6.0-page-function-audit",
        "document_status": "structure_frozen",
        "claim_boundary": "desktop_design_scaffold_only",
        "legacy_initial_audit": legacy,
        "legacy_event_evidence": [],
        "defect_registry": [],
        "initial_audit_seals": [seal],
        "seal_amendments": [],
        "legacy_effective_view": copy.deepcopy(legacy),
        "effective_legacy_hash": effective_legacy_hash,
        "legacy_disposition_closure": closures,
        "structure_manifest": manifest,
        "declared_node_inventory": copy.deepcopy(manifest),
        "source_graph_inventory": copy.deepcopy(manifest),
        "structure_assembly_snapshot": copy.deepcopy(manifest),
        "current_release_audit": {"pages": [page], "events": [event]},
        "global_checks": {
            "lossless_merge_candidates": [], "lossless_merge_receipt_path": str(merge_receipt_path),
            "lossless_merge_scan_sha256": file_digest(merge_receipt_path),
            "lossless_merge_scan_source_sha256": merge_source, "deletion_signature_hits": [],
            "deletion_scan_receipt_path": str(deletion_receipt_path), "deletion_scan_sha256": file_digest(deletion_receipt_path),
            "deletion_scan_source_sha256": deletion_source,
        },
    }
    result["structure_audit_bundle"] = build_bundle("structure_audit_bundle", {
        "structure_manifest": result["structure_manifest"],
        "current_release_audit": result["current_release_audit"],
        "legacy_effective_view": result["legacy_effective_view"],
        "legacy_disposition_closure": result["legacy_disposition_closure"],
    })
    return result


def add_release_evidence(document: dict) -> dict:
    result = copy.deepcopy(document)
    result["document_status"] = "release_ready"
    files = fixture_files()
    slide_inventory = [{
        "occurrence_ref": "PPT_MAIN:1",
        "artifact_id": "PPT_MAIN",
        "physical_index": 1,
        "page_id": "N001",
        "hidden": False,
        "reachable_from_start": True,
        "projected": True,
        "official_entry_id": "ENTRY_MAIN",
        "render_path": str(files["slide_render"]),
        "render_sha256": file_digest(files["slide_render"]),
        "embedded_asset_ids": [],
        "media_sha256": [],
        "media_bindings": [],
        "notes_event_ids": [],
        "image_relationship_count": 0,
    }]
    doc_inventory = [{"artifact_id": "DOC_TEACHER", "doc_page_index": 1, "source_sha256": file_digest(files["docx"]), "render_path": str(files["doc_render"]), "render_sha256": file_digest(files["doc_render"]), "render_receipt_path": str(files["doc_render_receipt"]), "render_receipt_sha256": file_digest(files["doc_render_receipt"]), "render_renderer": "fixture-page-render-v1", "render_renderer_parameters": {"dpi": 150}, "content_refs": ["E_END"]}]
    channels = [{
        "channel_ref": "SCRIPT:E_END",
        "channel_type": "teacher_spoken",
        "source_artifact_id": "DOC_TEACHER",
        "source_path": str(files["docx"]),
        "source_sha256": file_digest(files["docx"]),
        "field_or_region": "E_END#teacher_line",
        "content_sha256": hashlib.sha256(files["teacher_line"].encode("utf-8")).hexdigest(),
        "student_exposure_order": 2,
        "owner_event_id": "E_END",
        "exposure_status": "scripted",
        "exposure_evidence_refs": ["E_END#actions"],
    }]
    approved_visual_assets_manifest = {
        "schema_version": "1.0",
        "character_reference_manifest_path": str(files["character_manifest"]),
        "character_reference_manifest_sha256": file_digest(files["character_manifest"]),
        "assets": [],
        "page_bindings": [{
            "page_id": "N001", "status": "no_image_required", "primary_visual_duty": "活动界面",
            "instructional_gain": "保留安静书写与交付空间", "no_image_reason": "人物图会挤压任务和书写空间",
        }],
    }
    approved_visual_assets_hash = audit_sha256(approved_visual_assets_manifest)
    observer_records = [
        {"observer_id": "v-observer-1", "observed_at": "2026-08-13T06:30:00+08:00", "render_sha256": file_digest(files["slide_render"]), "primary_object_first": True, "recognized_core": "退出条任务", "misreading": None},
        {"observer_id": "v-observer-2", "observed_at": "2026-08-13T06:31:00+08:00", "render_sha256": file_digest(files["slide_render"]), "primary_object_first": True, "recognized_core": "独立书写并交付", "misreading": None},
    ]
    observer_receipts = []
    for index, observer_record in enumerate(observer_records, start=1):
        receipt_path = ARTIFACT_DIR / f"observer-{index}.json"
        receipt_path.write_text(json.dumps(observer_record, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        observer_receipts.append({**observer_record, "receipt_path": str(receipt_path), "receipt_sha256": file_digest(receipt_path)})
    artifact_manifest = {
        "artifacts": [
            {"artifact_id": "PPT_MAIN", "type": "pptx", "source_path": str(files["pptx"]), "page_count": 1, "source_sha256": file_digest(files["pptx"]), "render_manifest_sha256": digest([{"occurrence_ref": "PPT_MAIN:1", "render_sha256": file_digest(files["slide_render"])}]), "approved_assets_manifest_sha256": approved_visual_assets_hash, "official_entries": ["ENTRY_MAIN"], "file_observation": {"parser": "pptx-parser-v1", "observed_source_sha256": file_digest(files["pptx"]), "observed_page_count": 1}},
            {"artifact_id": "DOC_TEACHER", "type": "docx", "source_path": str(files["docx"]), "page_count": 1, "source_sha256": file_digest(files["docx"]), "render_manifest_sha256": digest([{"doc_page_index": 1, "render_sha256": file_digest(files["doc_render"])}]), "pagination_pdf_path": str(files["pagination_pdf"]), "pagination_pdf_sha256": file_digest(files["pagination_pdf"]), "pagination_receipt_path": str(files["pagination_receipt"]), "pagination_receipt_sha256": file_digest(files["pagination_receipt"]), "pagination_renderer": "fixture-pdf-writer-v1", "pagination_renderer_parameters": {"paper": "A4"}, "official_entries": [], "file_observation": {"parser": "docx-render-parser-v1", "observed_source_sha256": file_digest(files["docx"]), "observed_page_count": 1}},
        ]
    }
    current_manifest = {
        "structure_manifest": copy.deepcopy(result["structure_manifest"]),
        "slide_occurrence_inventory": copy.deepcopy(slide_inventory),
        "document_page_inventory": copy.deepcopy(doc_inventory),
        "other_channel_inventory": copy.deepcopy(channels),
        "release_artifact_manifest": copy.deepcopy(artifact_manifest),
    }
    release_bundle = build_bundle("release_audit_bundle", {
        "structure_audit_bundle": result["structure_audit_bundle"],
        "release_artifact_manifest": artifact_manifest,
        "slide_occurrence_inventory": slide_inventory,
        "document_page_inventory": doc_inventory,
        "other_channel_inventory": channels,
        "current_manifest": current_manifest,
    })
    release_bundle_hash = release_bundle["bundle_sha256"]
    records = [
        {"review_id": "R1", "review_type": "student_occurrence", "object_key": "PPT_MAIN:1", "revision": 1,
         "previous_ledger_hash": None, "supersedes_review_id": None, "status": "pass", "defect_ids": [],
         "reviewer_id": "student-final", "reviewed_at": "2026-08-13T11:00:00+08:00",
         "release_audit_bundle_sha256": release_bundle_hash,
         "simulated_seen": "退出条任务", "simulated_heard": "教师朗读任务", "simulated_activity_participation": "独立书写并交付",
         "possible_understanding": "能保存一项理解", "possible_misunderstanding": "可能写得笼统", "possible_gain": "形成课后诊断入口"},
        {"review_id": "R2", "review_type": "visual_slide", "object_key": "PPT_MAIN:1", "revision": 1,
         "previous_ledger_hash": None, "supersedes_review_id": None, "status": "pass", "defect_ids": [],
         "reviewer_id": "visual-final", "reviewed_at": "2026-08-13T11:05:00+08:00",
         "release_audit_bundle_sha256": release_bundle_hash,
         "source_artifact_sha256": file_digest(files["pptx"]), "render_sha256": file_digest(files["slide_render"]),
         "approved_assets_manifest_sha256": approved_visual_assets_hash, "render_evidence_refs": ["PPT_MAIN#render-1"],
         "visual_findings": "原诗与任务先被识别，未见角色漂移",
         "illustration_evidence": {"status": "no_image_required", "page_binding_ref": "N001", "instructional_gain": "保留安静书写与交付空间"},
         "three_second_observations": observer_receipts},
        {"review_id": "R3", "review_type": "visual_document_page", "object_key": "DOC_TEACHER:1", "revision": 1,
         "previous_ledger_hash": None, "supersedes_review_id": None, "status": "pass", "defect_ids": [],
         "reviewer_id": "visual-final", "reviewed_at": "2026-08-13T11:10:00+08:00",
         "release_audit_bundle_sha256": release_bundle_hash,
         "source_artifact_sha256": file_digest(files["docx"]), "render_sha256": file_digest(files["doc_render"]),
         "render_evidence_refs": ["DOC_TEACHER#render-1"], "visual_findings": "分页清楚，无截断"},
        {"review_id": "R4", "review_type": "student_event", "object_key": "E_END", "revision": 1,
         "previous_ledger_hash": None, "supersedes_review_id": None, "status": "pass", "defect_ids": [],
         "reviewer_id": "student-final", "reviewed_at": "2026-08-13T11:15:00+08:00",
         "release_audit_bundle_sha256": release_bundle_hash,
         "ordered_carrier_occurrence_refs": [], "other_channel_evidence_refs": ["SCRIPT:E_END"],
         "simulated_seen": "退出条页面", "simulated_heard": "教师交付指令", "simulated_activity_participation": "全员提交",
         "possible_understanding": "知道自己仍有何疑问", "possible_misunderstanding": "可能只复述结论", "possible_gain": "问题得到保存"},
    ]
    previous_hash = None
    for record in records:
        record["previous_ledger_hash"] = previous_hash
        record["record_hash"] = digest(record)
        previous_hash = record["record_hash"]

    release_ledger = {
        "records": records,
        "release_defect_registry": [],
        "release_defect_closures": [],
    }
    effective_review_view = copy.deepcopy(records)
    closure_summary = {"closed_p0_p1_p2_ids": [], "open_p0_p1_p2_count": 0}
    scorecard = {
        "total_score": 100,
        "dimensions": [
            {"dimension": "文本、教材和认识边界", "score": 20, "maximum": 20, "evidence_refs": ["N001#unique_function"]},
            {"dimension": "学生接收连续性与问题时机", "score": 20, "maximum": 20, "evidence_refs": ["E_END#inputs"]},
            {"dimension": "页面必要性与因果闭合", "score": 20, "maximum": 20, "evidence_refs": ["N001#merge_test"]},
            {"dimension": "参与覆盖、倾听、追问和修订", "score": 15, "maximum": 15, "evidence_refs": ["N001#voice_coverage"]},
            {"dimension": "语文质地、体验和课堂剧本", "score": 15, "maximum": 15, "evidence_refs": ["E_END#actions"]},
            {"dimension": "视觉、插图与跨文件实施质量", "score": 10, "maximum": 10, "evidence_refs": ["PPT_MAIN#source_sha256"]},
        ],
    }
    attestation = build_bundle("release_attestation", {
        "release_audit_bundle": release_bundle,
        "release_review_ledger": release_ledger,
        "effective_release_review_view": effective_review_view,
        "final_defect_closure_summary": closure_summary,
        "final_scorecard": scorecard,
    })
    result["final_release"] = {
        "release_audit_bundle": release_bundle,
        "release_audit_bundle_sha256": release_bundle_hash,
        "release_artifact_manifest": artifact_manifest,
        "approved_visual_assets_manifest": approved_visual_assets_manifest,
        "slide_occurrence_inventory": slide_inventory,
        "document_page_inventory": doc_inventory,
        "other_channel_inventory": channels,
        "physical_assembly_snapshot": {"artifacts": copy.deepcopy(artifact_manifest["artifacts"]), "slides": copy.deepcopy(slide_inventory), "documents": copy.deepcopy(doc_inventory)},
        "current_manifest": current_manifest,
        "release_review_ledger": release_ledger,
        "effective_release_review_view": effective_review_view,
        "final_defect_closure_summary": closure_summary,
        "final_scorecard": scorecard,
        "release_attestation": attestation,
    }
    detector_configuration = {
        "text": "normalized-exact-v1", "asset": "sha256-and-semantic-v1",
        "layout": "render-layout-v1", "event": "event-marker-v1",
    }
    release_scan_state = {
        "office_sources": [
            {"artifact_id": item["artifact_id"], "type": item["type"], "source_sha256": item["source_sha256"], "page_count": item["page_count"], "byte_count": item.get("byte_count")}
            for item in artifact_manifest["artifacts"]
        ],
        "slide_renders": [{"occurrence_ref": "PPT_MAIN:1", "render_sha256": file_digest(files["slide_render"])}],
        "document_renders": [{"artifact_id": "DOC_TEACHER", "doc_page_index": 1, "render_sha256": file_digest(files["doc_render"])}],
        "other_channels": [{
            "channel_ref": channels[0]["channel_ref"], "source_sha256": channels[0]["source_sha256"],
            "field_or_region": channels[0]["field_or_region"], "content_sha256": channels[0]["content_sha256"],
            "student_exposure_order": channels[0]["student_exposure_order"], "owner_event_id": channels[0]["owner_event_id"],
        }],
        "approved_assets_manifest_sha256": approved_visual_assets_hash,
        "forbidden_reappearance_signatures": [],
        "detector_configuration": detector_configuration,
    }
    scan_receipt = {
        "check_type": "release_deletion_signatures", "source_state_sha256": digest(release_scan_state),
        "detector_configuration_sha256": digest(detector_configuration), "results": [],
    }
    scan_receipt_path = ARTIFACT_DIR / "release-deletion-scan.json"
    scan_receipt_path.write_text(json.dumps(scan_receipt, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    result["final_release"]["release_deletion_scan"] = {
        "detector_configuration": detector_configuration, "source_state_sha256": digest(release_scan_state),
        "receipt_path": str(scan_receipt_path), "receipt_sha256": file_digest(scan_receipt_path),
    }
    return result


def codes(document: dict, mode: str = "freeze") -> set[str]:
    return {item["code"] for item in validate_audit_document(document, mode=mode)}


def reseal_legacy(document: dict) -> None:
    seal = document["initial_audit_seals"][0]
    seal["source_sha256"] = digest(document["legacy_initial_audit"])
    seal["legacy_event_evidence_sha256"] = digest(document["legacy_event_evidence"])
    seal["seal_hash"] = digest({key: value for key, value in seal.items() if key != "seal_hash"})


def refresh_effective_legacy(document: dict) -> None:
    document["legacy_effective_view"] = copy.deepcopy(document["legacy_initial_audit"])
    document["effective_legacy_hash"] = digest(document["legacy_effective_view"])
    for closure in document["legacy_disposition_closure"]:
        closure["based_on_effective_hash"] = document["effective_legacy_hash"]


def refresh_target_closures(document: dict) -> None:
    page = document["current_release_audit"]["pages"][0]
    for closure in document["legacy_disposition_closure"]:
        closure["target_field_sha256"] = digest(page["unique_function"])
        closure["current_audit_node_sha256"] = digest(page)


def make_legacy_carrier(document: dict) -> None:
    page = document["legacy_initial_audit"][0]
    page["audit_scope"] = "event_carrier"
    page["owner_event_id"] = "LE_OPEN"
    page["gates"][3] = gate("G4", "na")
    page["gates"][3]["evidence_refs"] = ["LE_OPEN#gate_4"]
    page["gates"][4] = gate("G5", "na")
    page["gates"][4]["evidence_refs"] = ["LE_OPEN#gate_5"]
    document["legacy_event_evidence"] = [{
        "legacy_event_id": "LE_OPEN",
        "learning_unit": "LEGACY_UNIT",
        "carrier_ids": ["S001"],
        "inputs": ["旧页原文"],
        "actions": ["持续显示并听读"],
        "artifacts": ["停顿句"],
        "observable_change": {"before": "未定位", "after": "已定位", "criterion": "能指出停顿处"},
        "next_use_evidence": ["S002#student_input"],
        "gate_4": gate("G4"),
        "gate_5": gate("G5"),
        "reviewer_ids": ["legacy-event-student", "legacy-event-visual"],
        "reviewed_at": "2026-08-13T08:30:00+08:00",
    }]
    reseal_legacy(document)


class ThreeLayerAuditTests(unittest.TestCase):
    def test_valid_freeze_document_passes(self):
        self.assertEqual([], validate_audit_document(valid_freeze_document(), mode="freeze"))

    def test_legacy_ids_are_exactly_s001_to_s127(self):
        doc = valid_freeze_document()
        doc["legacy_initial_audit"].pop()
        self.assertIn("LEGACY_ID_SET_INVALID", codes(doc))

    def test_seal_hash_and_source_hash_are_tamper_evident(self):
        doc = valid_freeze_document()
        doc["legacy_initial_audit"][0]["unique_function"] = "tampered"
        self.assertIn("LEGACY_SEAL_SOURCE_HASH_MISMATCH", codes(doc))
        doc = valid_freeze_document()
        doc["initial_audit_seals"][0]["seal_hash"] = "0" * 64
        self.assertIn("LEGACY_SEAL_HASH_MISMATCH", codes(doc))

    def test_seal_requires_two_independent_reviewers(self):
        doc = valid_freeze_document()
        doc["initial_audit_seals"][0]["reviewer_ids"] = ["same", "same"]
        self.assertIn("LEGACY_SEAL_REVIEWERS_INVALID", codes(doc))

    def test_legacy_initial_audit_rejects_deferred(self):
        doc = valid_freeze_document()
        doc["legacy_initial_audit"][0]["gates"][4]["gate_status"] = "deferred"
        self.assertIn("LEGACY_DEFERRED_FORBIDDEN", codes(doc))

    def test_failed_legacy_page_cannot_be_retained(self):
        doc = valid_freeze_document()
        doc["legacy_initial_audit"][0]["gates"][1] = gate("G2", "fail", "G2_FUNCTION_DUPLICATE")
        reseal_legacy(doc)
        refresh_effective_legacy(doc)
        self.assertIn("DISPOSITION_KEEP_FAILED_LEGACY", codes(doc))

    def test_all_initial_failures_and_p0_p2_defects_must_close(self):
        doc = valid_freeze_document()
        doc["defect_registry"] = [{"defect_id": "D1", "severity": "P1", "object_ref": "S001", "reviewer_id": "r"}]
        doc["legacy_initial_audit"][0]["review_status"]["student_reception"]["defect_ids"] = ["D1"]
        self.assertIn("DISPOSITION_DEFECT_SET_MISMATCH", codes(doc))

    def test_effective_view_amendment_new_defect_becomes_authoritative(self):
        doc = valid_freeze_document()
        seal_hash = doc["initial_audit_seals"][0]["seal_hash"]
        amendment = {
            "amendment_id": "A-DEFECT", "target_seal_id": "SEAL_ALL", "previous_effective_hash": seal_hash,
            "claim_pointer": "S001#review_status.student_reception.defect_ids", "old_claim": [], "new_claim": ["D_EFFECTIVE"],
            "reason": "补录审查发现", "evidence_refs": ["S001#review_status"], "author_id": "fixer",
            "reviewer_ids": ["r1", "r2"], "reviewed_at": "2026-08-13T10:00:00+08:00",
        }
        amendment["amendment_hash"] = digest(amendment)
        doc["seal_amendments"] = [amendment]
        doc["legacy_effective_view"][0]["review_status"]["student_reception"]["defect_ids"] = ["D_EFFECTIVE"]
        doc["effective_legacy_hash"] = digest(doc["legacy_effective_view"])
        for closure in doc["legacy_disposition_closure"]:
            closure["based_on_effective_hash"] = doc["effective_legacy_hash"]
        self.assertIn("LEGACY_DEFECT_REGISTRY_MISMATCH", codes(doc))

    def test_closed_defect_id_without_detailed_closure_is_rejected(self):
        doc = valid_freeze_document()
        doc["defect_registry"] = [{
            "defect_id": "D1", "severity": "P1", "object_ref": "S001", "reviewer_id": "student-reviewer",
            "claim": "活动覆盖虚假", "evidence_refs": ["S001#voice_coverage"],
        }]
        doc["legacy_initial_audit"][0]["review_status"]["student_reception"]["defect_ids"] = ["D1"]
        reseal_legacy(doc)
        refresh_effective_legacy(doc)
        closure = doc["legacy_disposition_closure"][0]
        closure["initial_defect_ids"] = ["D1"]
        closure["closed_defect_ids"] = ["D1"]
        closure["defect_closures"] = []
        self.assertIn("DISPOSITION_DEFECT_CLOSURE_INVALID", codes(doc))

    def test_delete_is_only_decision_allowed_without_targets(self):
        doc = valid_freeze_document()
        closure = doc["legacy_disposition_closure"][0]
        closure["decision"] = "合并"
        closure["target_refs"] = []
        self.assertIn("DISPOSITION_TARGET_RULE_INVALID", codes(doc))
        closure["decision"] = "删除"
        closure["target_refs"] = ["page:N001"]
        self.assertIn("DISPOSITION_TARGET_RULE_INVALID", codes(doc))

    def test_move_cannot_hide_g2_g3_g4_or_g6_failure(self):
        doc = valid_freeze_document()
        doc["legacy_initial_audit"][0]["gates"][2] = gate("G3", "fail", "G3_ACTION_VAGUE")
        doc["legacy_disposition_closure"][0]["decision"] = "移动"
        reseal_legacy(doc)
        refresh_effective_legacy(doc)
        self.assertIn("DISPOSITION_MOVE_GATE_INVALID", codes(doc))

    def test_target_must_have_reciprocal_lineage(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["pages"][0]["legacy_source_refs"].remove("S001")
        self.assertIn("DISPOSITION_LINEAGE_MISMATCH", codes(doc))

    def test_changed_target_field_invalidates_closed_disposition(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["pages"][0]["unique_function"] = "changed"
        self.assertIn("DISPOSITION_TARGET_HASH_STALE", codes(doc))

    def test_seal_reviewers_must_be_independent_of_author(self):
        doc = valid_freeze_document()
        doc["initial_audit_seals"][0]["reviewer_ids"][0] = "legacy-auditor"
        self.assertIn("LEGACY_SEAL_REVIEWERS_INVALID", codes(doc))

    def test_legacy_carrier_can_only_borrow_same_sealed_legacy_event(self):
        doc = valid_freeze_document()
        make_legacy_carrier(doc)
        self.assertNotIn("LEGACY_EVENT_EVIDENCE_INVALID", codes(doc))
        doc["legacy_event_evidence"][0]["carrier_ids"] = []
        self.assertIn("LEGACY_EVENT_OWNER_MISMATCH", codes(doc))
        doc = valid_freeze_document()
        make_legacy_carrier(doc)
        doc["legacy_initial_audit"][0]["owner_event_id"] = "E_END"
        reseal_legacy(doc)
        self.assertIn("LEGACY_EVENT_OWNER_MISMATCH", codes(doc))

    def test_amendment_chain_must_be_linear_and_independently_reviewed(self):
        doc = valid_freeze_document()
        seal_hash = doc["initial_audit_seals"][0]["seal_hash"]
        amendment = {
            "amendment_id": "A1", "target_seal_id": "SEAL_ALL", "previous_effective_hash": seal_hash,
            "claim_pointer": "S001#unique_function", "old_claim": "旧", "new_claim": "新",
            "reason": "事实性纠错", "evidence_refs": ["S001#unique_function"], "author_id": "fixer",
            "reviewer_ids": ["r1", "r2"], "reviewed_at": "2026-08-13T10:00:00+08:00",
        }
        amendment["amendment_hash"] = digest(amendment)
        doc["seal_amendments"] = [amendment]
        doc["effective_legacy_hash"] = amendment["amendment_hash"]
        for closure in doc["legacy_disposition_closure"]:
            closure["based_on_effective_hash"] = amendment["amendment_hash"]
        self.assertNotIn("LEGACY_AMENDMENT_CHAIN_INVALID", codes(doc))
        doc["seal_amendments"][0]["previous_effective_hash"] = "0" * 64
        self.assertIn("LEGACY_AMENDMENT_CHAIN_INVALID", codes(doc))
        doc = valid_freeze_document()
        amendment["previous_effective_hash"] = seal_hash
        amendment["reviewer_ids"] = ["fixer", "r2"]
        amendment["amendment_hash"] = digest({key: value for key, value in amendment.items() if key != "amendment_hash"})
        doc["seal_amendments"] = [amendment]
        self.assertIn("LEGACY_AMENDMENT_REVIEWERS_INVALID", codes(doc))

    def test_disposition_requires_decision_specific_target_counts(self):
        doc = valid_freeze_document()
        doc["legacy_disposition_closure"][0]["decision"] = "保留"
        doc["legacy_disposition_closure"][0]["target_refs"] = ["page:N001", "event:E_END"]
        self.assertIn("DISPOSITION_TARGET_RULE_INVALID", codes(doc))

    def test_student_visible_visual_defect_cannot_close_event_only(self):
        doc = valid_freeze_document()
        closure = doc["legacy_disposition_closure"][0]
        closure["decision"] = "重写"
        closure["target_refs"] = ["event:E_END"]
        closure["legacy_content_elements"] = [{"element_id": "function", "kind": "visual"}]
        closure["element_mappings"] = [{"element_id": "function", "target_ref": "event:E_END", "target_field": "observable_change"}]
        closure["element_mapping_sha256"] = digest(closure["element_mappings"])
        closure["target_field_sha256"] = digest(doc["current_release_audit"]["events"][0]["observable_change"])
        closure["current_audit_node_sha256"] = digest(doc["current_release_audit"]["events"][0])
        self.assertIn("DISPOSITION_PAGE_TARGET_REQUIRED", codes(doc))

    def test_deletion_reappearance_blocks_freeze(self):
        doc = valid_freeze_document()
        doc["global_checks"]["deletion_signature_hits"] = [{"legacy_id": "S001", "signature": "deleted-text"}]
        self.assertIn("DISPOSITION_DELETION_REAPPEARED", codes(doc))

    def test_deletion_cannot_close_without_inventory_signatures_and_review(self):
        doc = valid_freeze_document()
        closure = doc["legacy_disposition_closure"][0]
        closure.update({
            "decision": "删除", "target_refs": [], "legacy_content_elements": [],
            "required_carry_forward": [], "element_mappings": [], "forbidden_reappearance_signatures": [],
        })
        self.assertIn("DISPOSITION_DELETION_EVIDENCE_INVALID", codes(doc))

    def test_mapping_to_missing_target_field_cannot_close(self):
        doc = valid_freeze_document()
        closure = doc["legacy_disposition_closure"][0]
        closure["element_mappings"][0]["target_field"] = "NO_SUCH_FIELD"
        closure["element_mapping_sha256"] = digest(closure["element_mappings"])
        closure["target_field_sha256"] = digest(None)
        self.assertIn("DISPOSITION_TARGET_FIELD_MISSING", codes(doc))


class CurrentGraphTests(unittest.TestCase):
    def test_manifest_audit_declared_reachable_and_assembly_sets_must_match(self):
        for field in ("declared_node_inventory", "source_graph_inventory", "structure_assembly_snapshot"):
            with self.subTest(field=field):
                doc = valid_freeze_document()
                doc[field]["pages"] = []
                self.assertIn("CURRENT_INVENTORY_SET_MISMATCH", codes(doc))

    def test_declared_but_unreachable_node_is_rejected(self):
        doc = valid_freeze_document()
        doc["declared_node_inventory"]["events"].append({"node_id": "E_ORPHAN", "execution_order": 3})
        self.assertIn("CURRENT_DECLARED_ORPHAN", codes(doc))

    def test_event_audit_cannot_be_omitted(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["events"] = []
        self.assertIn("CURRENT_AUDIT_SET_MISMATCH", codes(doc))

    def test_carrier_and_event_owner_must_be_bidirectional(self):
        doc = valid_freeze_document()
        page = doc["current_release_audit"]["pages"][0]
        page["audit_scope"] = "event_carrier"
        page["owner_event_id"] = "E_END"
        page["gates"][3]["gate_status"] = "na"
        page["gates"][4]["gate_status"] = "na"
        self.assertIn("CURRENT_CARRIER_OWNER_MISMATCH", codes(doc))

    def test_learning_page_cannot_use_na(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["pages"][0]["gates"][3]["gate_status"] = "na"
        self.assertIn("CURRENT_NA_MISUSE", codes(doc))

    def test_current_carrier_na_must_reference_owning_event_gate(self):
        doc = valid_freeze_document()
        page = doc["current_release_audit"]["pages"][0]
        event = doc["current_release_audit"]["events"][0]
        page["audit_scope"] = "event_carrier"
        page["owner_event_id"] = event["event_id"]
        event["carrier_ids"] = [page["page_id"]]
        page["gates"][3] = gate("G4", "na")
        page["gates"][4] = gate("G5", "na")
        page["gates"][3]["evidence_refs"] = []
        page["gates"][4]["evidence_refs"] = []
        self.assertIn("CURRENT_CARRIER_EVENT_EVIDENCE_INVALID", codes(doc))

        page["gates"][3]["evidence_refs"] = [f"{event['event_id']}#gate_4"]
        page["gates"][4]["evidence_refs"] = [f"{event['event_id']}#gate_5"]
        self.assertNotIn("CURRENT_CARRIER_EVENT_EVIDENCE_INVALID", codes(doc))

    def test_g5_edges_must_be_strictly_forward_and_acyclic(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["events"][0]["execution_order"] = 1
        self.assertIn("CURRENT_G5_ORDER_INVALID", codes(doc))

    def test_exactly_one_maximum_terminal_event_is_required(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["events"][0]["terminal_sink"] = False
        self.assertIn("CURRENT_TERMINAL_INVALID", codes(doc))
        doc = valid_freeze_document()
        del doc["current_release_audit"]["events"][0]["terminal_use"]["delivery_evidence_refs"]
        self.assertIn("CURRENT_TERMINAL_USE_INVALID", codes(doc))

    def test_freeze_rejects_pending_deferred_provisional_and_fail(self):
        for status in ("pending", "deferred", "fail"):
            with self.subTest(status=status):
                doc = valid_freeze_document()
                doc["current_release_audit"]["pages"][0]["gates"][4]["gate_status"] = status
                if status == "fail":
                    doc["current_release_audit"]["pages"][0]["gates"][4]["failure_code"] = "G5_OUTPUT_ORPHAN"
                self.assertIn("CURRENT_GATE_OPEN", codes(doc))

    def test_current_learning_page_requires_full_function_contract(self):
        for field in ("prerequisite", "student_action", "voice_coverage", "listener_task", "observable_change",
                      "artifact_location", "next_use_refs", "merge_test", "primary_visual_duty", "time_value"):
            with self.subTest(field=field):
                doc = valid_freeze_document()
                del doc["current_release_audit"]["pages"][0][field]
                refresh_target_closures(doc)
                self.assertIn("CURRENT_PAGE_CONTRACT_INVALID", codes(doc))

    def test_current_event_requires_full_input_action_artifact_contract(self):
        doc = valid_freeze_document()
        del doc["current_release_audit"]["events"][0]["observable_change"]
        self.assertIn("CURRENT_EVENT_CONTRACT_INVALID", codes(doc))

    def test_current_page_rejects_empty_or_false_participation_semantics(self):
        doc = valid_freeze_document()
        page = doc["current_release_audit"]["pages"][0]
        page["voice_coverage"]["all_have_entry"] = False
        page["student_action"]["action"] = ""
        page["observable_change"]["after"] = page["observable_change"]["before"]
        refresh_target_closures(doc)
        self.assertIn("CURRENT_PAGE_CONTRACT_INVALID", codes(doc))

    def test_structure_consensus_cannot_override_failed_reviews(self):
        doc = valid_freeze_document()
        review = doc["current_release_audit"]["pages"][0]["review_status"]
        for key in ("self_review", "student_reception", "visual"):
            review[key]["status"] = "fail"
            review[key]["defect_ids"] = [f"X-{key}"]
        review["consensus"] = "passed"
        refresh_target_closures(doc)
        self.assertIn("AUDIT_REVIEW_CONSENSUS_INVALID", codes(doc))

    def test_frontstage_rejects_design_language(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["pages"][0]["student_visible_text"] = "今天建立理解链，进行接收审计"
        refresh_target_closures(doc)
        self.assertIn("CURRENT_FRONTSTAGE_LEAK", codes(doc))

    def test_g5_page_edge_and_event_input_must_be_reciprocal(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["events"][0]["inputs"] = []
        self.assertIn("CURRENT_G5_LINK_MISMATCH", codes(doc))
        doc = valid_freeze_document()
        doc["structure_manifest"]["g5_edges"] = []
        doc["declared_node_inventory"]["g5_edges"] = []
        doc["source_graph_inventory"]["g5_edges"] = []
        doc["structure_assembly_snapshot"]["g5_edges"] = []
        self.assertIn("CURRENT_G5_LINK_MISMATCH", codes(doc))

    def test_stage_allows_honest_g5_deferred_until_target_is_implemented(self):
        doc = valid_freeze_document()
        page = doc["current_release_audit"]["pages"][0]
        page["gates"][4] = gate("G5", "deferred")
        page["gates"][4].update({"target_event_id": "E_END", "target_batch": "final", "expected_use": "交付并形成课后诊断材料"})
        page["release_status"] = "provisional"
        doc["current_release_audit"]["events"][0]["implemented"] = False
        refresh_target_closures(doc)
        self.assertNotIn("CURRENT_DEFERRED_INVALID", codes(doc, mode="stage"))
        doc["current_release_audit"]["events"][0]["implemented"] = True
        self.assertIn("CURRENT_DEFERRED_NOT_RESOLVED", codes(doc, mode="stage"))

    def test_terminal_event_cannot_declare_further_classroom_use(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["events"][0]["next_uses"] = [{"target_event_id": "E_LATER"}]
        self.assertIn("CURRENT_TERMINAL_USE_INVALID", codes(doc))


class FinalReleaseTests(unittest.TestCase):
    def test_valid_release_document_passes(self):
        self.assertEqual([], validate_audit_document(add_release_evidence(valid_freeze_document()), mode="release"))

    def test_release_requires_physical_and_channel_evidence(self):
        self.assertIn("RELEASE_EVIDENCE_MISSING", codes(valid_freeze_document(), mode="release"))

    def test_slide_occurrences_are_a_bijection_but_doc_pages_need_no_n_id(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["slide_occurrence_inventory"].append(copy.deepcopy(doc["final_release"]["slide_occurrence_inventory"][0]))
        self.assertIn("RELEASE_SLIDE_BIJECTION_INVALID", codes(doc, mode="release"))
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["document_page_inventory"][0]["page_id"] = "N001"
        self.assertIn("RELEASE_DOC_PAGE_ID_FORBIDDEN", codes(doc, mode="release"))

    def test_pretrial_release_forbids_observed_channel_claim(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["other_channel_inventory"][0]["exposure_status"] = "observed"
        self.assertIn("RELEASE_OBSERVED_BEFORE_TRIAL", codes(doc, mode="release"))

    def test_review_sets_must_cover_projected_slides_events_and_doc_pages(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["release_review_ledger"]["records"] = []
        self.assertIn("RELEASE_REVIEW_SET_MISMATCH", codes(doc, mode="release"))

    def test_review_defect_ids_and_registry_are_bidirectionally_equal(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["release_review_ledger"]["records"][0]["defect_ids"] = ["RD1"]
        self.assertIn("RELEASE_DEFECT_REGISTRY_MISMATCH", codes(doc, mode="release"))

    def test_scripted_channel_requires_real_source_identity_and_owner(self):
        doc = add_release_evidence(valid_freeze_document())
        channel = doc["final_release"]["other_channel_inventory"][0]
        del channel["content_sha256"]
        self.assertIn("RELEASE_SCRIPT_EVIDENCE_MISSING", codes(doc, mode="release"))
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["other_channel_inventory"][0]["owner_event_id"] = "E_MISSING"
        self.assertIn("RELEASE_CHANNEL_OWNER_MISMATCH", codes(doc, mode="release"))

    def test_release_reviews_cannot_reuse_designer_or_each_other(self):
        doc = add_release_evidence(valid_freeze_document())
        for record in doc["final_release"]["release_review_ledger"]["records"]:
            record["reviewer_id"] = "designer"
            record["reviewed_at"] = "2026-08-13T11:00:00+08:00"
            record["release_audit_bundle_sha256"] = "a" * 64
        doc["final_release"]["release_audit_bundle_sha256"] = "a" * 64
        self.assertIn("RELEASE_REVIEW_INDEPENDENCE_INVALID", codes(doc, mode="release"))

    def test_release_ledger_revision_chain_cannot_fork_or_skip(self):
        doc = add_release_evidence(valid_freeze_document())
        ledger = doc["final_release"]["release_review_ledger"]
        ledger["records"][0].update({"record_hash": "1" * 64, "reviewer_id": "student-final", "reviewed_at": "2026-08-13T11:00:00+08:00", "release_audit_bundle_sha256": "a" * 64})
        duplicate = copy.deepcopy(ledger["records"][0])
        duplicate.update({"review_id": "R5", "revision": 3, "supersedes_review_id": "R1", "previous_ledger_hash": "1" * 64, "record_hash": "2" * 64})
        ledger["records"].append(duplicate)
        doc["final_release"]["release_audit_bundle_sha256"] = "a" * 64
        self.assertIn("RELEASE_LEDGER_CHAIN_INVALID", codes(doc, mode="release"))

    def test_release_p0_p2_defects_need_exactly_one_current_verified_closure(self):
        doc = add_release_evidence(valid_freeze_document())
        ledger = doc["final_release"]["release_review_ledger"]
        ledger["records"][0]["defect_ids"] = ["RD1"]
        ledger["release_defect_registry"] = [{
            "defect_id": "RD1", "severity": "P1", "object_ref": "PPT_MAIN:1", "review_record_ref": "R1",
            "claim": "活动无全员入口", "evidence_refs": ["PPT_MAIN#1"], "reviewer_id": "student-final",
            "discovered_at": "2026-08-13T11:00:00+08:00", "source_state_sha256": "c" * 64,
        }]
        ledger["release_defect_closures"] = []
        doc["final_release"]["final_defect_closure_summary"] = {"closed_p0_p1_p2_ids": [], "open_p0_p1_p2_count": 0}
        self.assertIn("RELEASE_DEFECT_CLOSURE_INVALID", codes(doc, mode="release"))

    def test_empty_artifact_manifest_and_unknown_hidden_page_are_rejected(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["release_artifact_manifest"]["artifacts"] = []
        self.assertIn("RELEASE_ARTIFACT_MANIFEST_INVALID", codes(doc, mode="release"))
        doc = add_release_evidence(valid_freeze_document())
        unknown = copy.deepcopy(doc["final_release"]["slide_occurrence_inventory"][0])
        unknown.update({"occurrence_ref": "PPT_MAIN:2", "physical_index": 2, "page_id": "N999", "hidden": True, "projected": False})
        doc["final_release"]["slide_occurrence_inventory"].append(unknown)
        self.assertIn("RELEASE_SLIDE_BIJECTION_INVALID", codes(doc, mode="release"))

    def test_unknown_review_type_and_status_break_ledger(self):
        doc = add_release_evidence(valid_freeze_document())
        record = doc["final_release"]["release_review_ledger"]["records"][0]
        record["review_type"] = "unknown"
        record["status"] = "banana"
        record["record_hash"] = digest({key: value for key, value in record.items() if key != "record_hash"})
        self.assertIn("RELEASE_LEDGER_CHAIN_INVALID", codes(doc, mode="release"))

    def test_release_bundle_and_attestation_are_independently_recomputed(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["release_audit_bundle"]["bundle_sha256"] = "0" * 64
        doc["final_release"]["release_audit_bundle_sha256"] = "0" * 64
        self.assertIn("AUDIT_BUNDLE_HASH_MISMATCH", codes(doc, mode="release"))
        doc = add_release_evidence(valid_freeze_document())
        del doc["final_release"]["release_attestation"]
        self.assertIn("AUDIT_BUNDLE_MISSING", codes(doc, mode="release"))

    def test_visual_release_evidence_requires_office_render_asset_hashes(self):
        doc = add_release_evidence(valid_freeze_document())
        artifact = doc["final_release"]["release_artifact_manifest"]["artifacts"][0]
        del artifact["source_sha256"]
        del artifact["approved_assets_manifest_sha256"]
        self.assertIn("RELEASE_ARTIFACT_MANIFEST_INVALID", codes(doc, mode="release"))
        doc = add_release_evidence(valid_freeze_document())
        visual = next(item for item in doc["final_release"]["release_review_ledger"]["records"] if item["review_type"] == "visual_slide")
        del visual["render_sha256"]
        self.assertIn("RELEASE_VISUAL_REVIEW_INVALID", codes(doc, mode="release"))

    def test_visual_review_becomes_stale_when_asset_or_source_changes(self):
        doc = add_release_evidence(valid_freeze_document())
        artifact = doc["final_release"]["release_artifact_manifest"]["artifacts"][0]
        artifact["approved_assets_manifest_sha256"] = "0" * 64
        self.assertIn("RELEASE_VISUAL_REVIEW_STALE", codes(doc, mode="release"))
        doc = add_release_evidence(valid_freeze_document())
        visual_doc = next(item for item in doc["final_release"]["release_review_ledger"]["records"] if item["review_type"] == "visual_document_page")
        visual_doc["source_artifact_sha256"] = "0" * 64
        self.assertIn("RELEASE_VISUAL_REVIEW_STALE", codes(doc, mode="release"))

    def test_slide_review_must_bind_current_render(self):
        doc = add_release_evidence(valid_freeze_document())
        visual = next(item for item in doc["final_release"]["release_review_ledger"]["records"] if item["review_type"] == "visual_slide")
        visual["render_sha256"] = "0" * 64
        self.assertIn("RELEASE_VISUAL_REVIEW_STALE", codes(doc, mode="release"))

    def test_decorative_image_without_task_card_or_three_second_test_is_rejected(self):
        doc = add_release_evidence(valid_freeze_document())
        occurrence = doc["final_release"]["slide_occurrence_inventory"][0]
        occurrence["embedded_asset_ids"] = ["DECORATIVE_01"]
        visual = next(item for item in doc["final_release"]["release_review_ledger"]["records"] if item["review_type"] == "visual_slide")
        visual["visual_findings"] = "画面好看"
        visual["three_second_observations"] = []
        self.assertIn("RELEASE_VISUAL_FUNCTION_GAIN_INVALID", codes(doc, mode="release"))
        self.assertIn("RELEASE_THREE_SECOND_TEST_INVALID", codes(doc, mode="release"))

    def test_visual_duty_gain_and_character_manifest_must_match_across_layers(self):
        doc = add_release_evidence(valid_freeze_document())
        binding = doc["final_release"]["approved_visual_assets_manifest"]["page_bindings"][0]
        binding["primary_visual_duty"] = "动作小景"
        visual = next(item for item in doc["final_release"]["release_review_ledger"]["records"] if item["review_type"] == "visual_slide")
        visual["illustration_evidence"]["instructional_gain"] = "好看"
        self.assertIn("RELEASE_VISUAL_FUNCTION_GAIN_INVALID", codes(doc, mode="release"))
        doc = add_release_evidence(valid_freeze_document())
        del doc["final_release"]["approved_visual_assets_manifest"]["character_reference_manifest_sha256"]
        self.assertIn("RELEASE_CHARACTER_MANIFEST_INVALID", codes(doc, mode="release"))

    def test_actual_missing_office_file_cannot_be_self_attested(self):
        doc = add_release_evidence(valid_freeze_document())
        artifact = doc["final_release"]["release_artifact_manifest"]["artifacts"][0]
        artifact["source_path"] = "/definitely/not/present/main.pptx"
        artifact["source_sha256"] = "1" * 64
        artifact["file_observation"] = {"parser": "self-report", "observed_source_sha256": "1" * 64, "observed_page_count": 1}
        self.assertIn("RELEASE_PHYSICAL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_doc_page_source_and_render_manifest_must_match_artifact(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["document_page_inventory"][0]["source_sha256"] = "c" * 64
        self.assertIn("RELEASE_DOCUMENT_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_independent_file_observation_blocks_unreported_physical_slide(self):
        doc = add_release_evidence(valid_freeze_document())
        artifact = doc["final_release"]["release_artifact_manifest"]["artifacts"][0]
        artifact["file_observation"]["observed_page_count"] = 2
        self.assertIn("RELEASE_PHYSICAL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_pptx_ooxml_page_id_must_match_inventory(self):
        doc = add_release_evidence(valid_freeze_document())
        occurrence = doc["final_release"]["slide_occurrence_inventory"][0]
        occurrence["page_id"] = "N999"
        self.assertIn("RELEASE_PHYSICAL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_pptx_ooxml_hidden_state_must_match_inventory(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["slide_occurrence_inventory"][0]["hidden"] = True
        self.assertIn("RELEASE_PHYSICAL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_pptx_ooxml_notes_events_must_match_inventory(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["slide_occurrence_inventory"][0]["notes_event_ids"] = ["E_END"]
        self.assertIn("RELEASE_PHYSICAL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_pptx_ooxml_asset_markers_must_match_inventory(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["slide_occurrence_inventory"][0]["embedded_asset_ids"] = ["A_SCENE"]
        self.assertIn("RELEASE_PHYSICAL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_fake_defect_closure_with_unchanged_state_is_rejected(self):
        doc = add_release_evidence(valid_freeze_document())
        ledger = doc["final_release"]["release_review_ledger"]
        record = ledger["records"][0]
        record["defect_ids"] = ["RD1"]
        object_hash = digest(doc["final_release"]["slide_occurrence_inventory"][0])
        ledger["release_defect_registry"] = [{
            "defect_id": "RD1", "severity": "P1", "object_ref": "PPT_MAIN:1", "review_record_ref": "R1",
            "claim": "活动无全员入口", "evidence_refs": ["PPT_MAIN#slide_1"], "reviewer_id": "student-final",
            "discovered_at": "2026-08-13T11:00:00+08:00", "source_state_sha256": object_hash,
        }]
        ledger["release_defect_closures"] = [{
            "defect_id": "RD1", "fix_refs": ["PPT_MAIN#slide_1"], "before_sha256": object_hash,
            "after_sha256": object_hash, "original_reviewer_id": "student-final", "reviewer_verification_status": "pass",
            "reviewed_at": "2026-08-13T12:00:00+08:00", "closure_status": "closed", "verified_source_state_sha256": object_hash,
        }]
        doc["final_release"]["final_defect_closure_summary"] = {"closed_p0_p1_p2_ids": ["RD1"], "open_p0_p1_p2_count": 0}
        self.assertIn("RELEASE_DEFECT_CLOSURE_INVALID", codes(doc, mode="release"))

    def test_scorecard_dimension_names_and_evidence_are_fixed(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["final_scorecard"]["dimensions"][0]["dimension"] = "x"
        doc["final_release"]["final_scorecard"]["dimensions"][0]["evidence_refs"] = ["NONEXISTENT#field"]
        self.assertIn("RELEASE_SCORECARD_INVALID", codes(doc, mode="release"))

    def test_scorecard_reference_must_resolve_to_real_field(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["final_scorecard"]["dimensions"][0]["evidence_refs"] = ["N001#NO_SUCH_FIELD"]
        self.assertIn("RELEASE_SCORECARD_INVALID", codes(doc, mode="release"))

    def test_student_event_review_must_cover_owned_channels_and_carriers(self):
        doc = add_release_evidence(valid_freeze_document())
        review = next(item for item in doc["final_release"]["release_review_ledger"]["records"] if item["review_type"] == "student_event")
        review["other_channel_evidence_refs"] = []
        self.assertIn("RELEASE_STUDENT_EVENT_LINK_MISMATCH", codes(doc, mode="release"))

    def test_global_scan_receipts_are_required_for_freeze(self):
        doc = valid_freeze_document()
        doc["global_checks"] = {}
        self.assertIn("CURRENT_GLOBAL_CHECKS_MISSING", codes(doc))

    def test_canonical_paths_use_posix_separators(self):
        from scripts.validate_meng_v6_page_audit import audit_sha256
        self.assertEqual(audit_sha256({"source_path": "stage/teacher.docx"}),
                         audit_sha256({"source_path": "stage\\teacher.docx"}))

    def test_workspace_external_paths_are_rejected(self):
        from scripts.validate_meng_v6_page_audit import resolve_source_path
        self.assertIsNone(resolve_source_path("/etc/hosts"))

    def test_observer_receipt_must_be_readable_current_and_chronological(self):
        doc = add_release_evidence(valid_freeze_document())
        visual = next(item for item in doc["final_release"]["release_review_ledger"]["records"] if item["review_type"] == "visual_slide")
        visual["three_second_observations"][0]["receipt_path"] = "/definitely/not/present.json"
        visual["three_second_observations"][0]["observed_at"] = "2099-01-01T00:00:00Z"
        self.assertIn("RELEASE_OBSERVER_PROVENANCE_INVALID", codes(doc, mode="release"))

    def test_global_scan_receipt_becomes_stale_after_structure_change(self):
        doc = valid_freeze_document()
        doc["current_release_audit"]["pages"][0]["unique_function"] = "changed after scan"
        refresh_target_closures(doc)
        self.assertIn("CURRENT_GLOBAL_CHECKS_STALE", codes(doc))

    def test_character_reference_manifest_must_be_a_real_complete_file(self):
        doc = add_release_evidence(valid_freeze_document())
        manifest = doc["final_release"]["approved_visual_assets_manifest"]
        manifest["character_reference_manifest_path"] = "/definitely/not/present/characters.json"
        self.assertIn("RELEASE_CHARACTER_MANIFEST_INVALID", codes(doc, mode="release"))

    def test_approved_asset_cannot_be_self_attested_without_a_real_file(self):
        doc = add_release_evidence(valid_freeze_document())
        release = doc["final_release"]
        release["approved_visual_assets_manifest"]["assets"] = [{
            "asset_id": "A_SCENE", "source_path": "/definitely/not/present/scene.png",
            "source_sha256": "a" * 64, "character_versions": ["W01-A"], "status": "approved",
        }]
        self.assertIn("RELEASE_APPROVED_ASSET_INVALID", codes(doc, mode="release"))

    def test_two_approved_asset_ids_cannot_reuse_the_same_file_hash(self):
        doc = add_release_evidence(valid_freeze_document())
        asset_path = ARTIFACT_DIR / "shared-asset.png"
        asset_path.write_bytes(b"same-file")
        doc["final_release"]["approved_visual_assets_manifest"]["assets"] = [
            {"asset_id": asset_id, "source_path": str(asset_path), "source_sha256": file_digest(asset_path),
             "character_versions": [version], "status": "approved"}
            for asset_id, version in (("A_W", "W01-A"), ("A_M", "M01-A"))
        ]
        self.assertIn("RELEASE_APPROVED_ASSET_INVALID", codes(doc, mode="release"))

    def test_pptx_media_hashes_must_equal_bound_approved_asset_hashes(self):
        doc = add_release_evidence(valid_freeze_document())
        occurrence = doc["final_release"]["slide_occurrence_inventory"][0]
        occurrence["media_sha256"] = ["a" * 64]
        self.assertIn("RELEASE_MEDIA_ASSET_MISMATCH", codes(doc, mode="release"))

    def test_every_approved_asset_must_be_bound_and_embedded(self):
        doc = add_release_evidence(valid_freeze_document())
        asset_path = ARTIFACT_DIR / "unused-approved.png"
        asset_path.write_bytes(b"unused-approved")
        doc["final_release"]["approved_visual_assets_manifest"]["assets"] = [{
            "asset_id": "A_UNUSED", "source_path": str(asset_path),
            "source_sha256": file_digest(asset_path), "character_versions": ["W01-A"], "status": "approved",
        }]
        self.assertIn("RELEASE_MEDIA_ASSET_MISMATCH", codes(doc, mode="release"))

    def test_declared_asset_relationship_id_cannot_be_swapped(self):
        doc = add_release_evidence(valid_freeze_document())
        occurrence, bindings = configure_two_asset_release(doc, "two-rel")
        occurrence["media_bindings"] = copy.deepcopy(bindings)
        occurrence["media_bindings"][0]["relationship_id"], occurrence["media_bindings"][1]["relationship_id"] = occurrence["media_bindings"][1]["relationship_id"], occurrence["media_bindings"][0]["relationship_id"]
        self.assertIn("RELEASE_PHYSICAL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_declared_asset_media_target_cannot_be_swapped(self):
        doc = add_release_evidence(valid_freeze_document())
        occurrence, bindings = configure_two_asset_release(doc, "two-target")
        occurrence["media_bindings"] = copy.deepcopy(bindings)
        occurrence["media_bindings"][0]["media_target"], occurrence["media_bindings"][1]["media_target"] = occurrence["media_bindings"][1]["media_target"], occurrence["media_bindings"][0]["media_target"]
        self.assertIn("RELEASE_PHYSICAL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_task_card_character_versions_must_match_bound_assets(self):
        doc = add_release_evidence(valid_freeze_document())
        binding = doc["final_release"]["approved_visual_assets_manifest"]["page_bindings"][0]
        binding.update({
            "status": "approved_to_use", "poem_evidence_refs": ["N001#unique_function"],
            "allowed_facts": ["人物在场"], "forbidden_inferences": ["不得越界"],
            "no_image_alternative": "保留原诗", "asset_ids": [], "character_versions": ["W01-A"],
        })
        self.assertIn("RELEASE_ILLUSTRATION_TASK_CARD_INVALID", codes(doc, mode="release"))

    def test_scripted_channel_must_read_the_bound_office_source_region(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["other_channel_inventory"][0]["field_or_region"] = "E_MISSING#teacher_line"
        self.assertIn("RELEASE_CHANNEL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_student_exposure_order_must_be_unique_and_follow_event_order(self):
        doc = add_release_evidence(valid_freeze_document())
        release = doc["final_release"]
        second = copy.deepcopy(release["other_channel_inventory"][0])
        second["channel_ref"] = "SCRIPT:E_END_2"
        release["other_channel_inventory"].append(second)
        doc["current_release_audit"]["events"][0]["other_channel_refs"].append("SCRIPT:E_END_2")
        self.assertIn("RELEASE_CHANNEL_ORDER_INVALID", codes(doc, mode="release"))

    def test_channel_content_hash_cannot_be_reused_after_script_text_changes(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["other_channel_inventory"][0]["content_sha256"] = "a" * 64
        self.assertIn("RELEASE_CHANNEL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_channel_type_must_be_one_of_the_supported_real_channels(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["other_channel_inventory"][0]["channel_type"] = "telepathy"
        self.assertIn("RELEASE_SCRIPT_EVIDENCE_MISSING", codes(doc, mode="release"))

    def test_channel_type_must_match_its_physical_source_medium(self):
        doc = add_release_evidence(valid_freeze_document())
        doc["final_release"]["other_channel_inventory"][0]["channel_type"] = "audio"
        self.assertIn("RELEASE_CHANNEL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_docx_pagination_requires_a_real_render_receipt(self):
        doc = add_release_evidence(valid_freeze_document())
        artifact = doc["final_release"]["release_artifact_manifest"]["artifacts"][1]
        artifact["pagination_pdf_path"] = "/definitely/not/present/teacher.pdf"
        self.assertIn("RELEASE_DOCUMENT_PAGINATION_INVALID", codes(doc, mode="release"))

    def test_docx_pagination_receipt_cannot_bind_another_source(self):
        doc = add_release_evidence(valid_freeze_document())
        artifact = doc["final_release"]["release_artifact_manifest"]["artifacts"][1]
        receipt_path = ARTIFACT_DIR / "wrong-pagination-source.json"
        receipt_path.write_text(json.dumps({
            "check_type": "docx_pagination", "source_sha256": "a" * 64,
            "pdf_sha256": artifact["pagination_pdf_sha256"], "page_count": 1,
            "renderer": artifact["pagination_renderer"],
            "renderer_parameters": artifact["pagination_renderer_parameters"],
        }, sort_keys=True), encoding="utf-8")
        artifact["pagination_receipt_path"] = str(receipt_path)
        artifact["pagination_receipt_sha256"] = file_digest(receipt_path)
        self.assertIn("RELEASE_DOCUMENT_PAGINATION_INVALID", codes(doc, mode="release"))

    def test_document_page_render_receipt_must_bind_pagination_pdf_and_page_index(self):
        doc = add_release_evidence(valid_freeze_document())
        page = doc["final_release"]["document_page_inventory"][0]
        page["render_receipt_path"] = "/definitely/not/present/doc-page-render.json"
        self.assertIn("RELEASE_DOCUMENT_RENDER_PROVENANCE_INVALID", codes(doc, mode="release"))

    def test_release_deletion_scan_must_bind_final_office_channels_assets_and_detectors(self):
        doc = add_release_evidence(valid_freeze_document())
        del doc["final_release"]["release_deletion_scan"]
        self.assertIn("RELEASE_DELETION_SCAN_INVALID", codes(doc, mode="release"))

    def test_inspect_pptx_uses_presentation_order_not_slide_filenames(self):
        path = ARTIFACT_DIR / "ordered.pptx"
        with zipfile.ZipFile(path, "w") as package:
            package.writestr(
                "ppt/presentation.xml",
                '<p:presentation xmlns:p="urn:p" xmlns:r="urn:r"><p:sldIdLst><p:sldId id="256" r:id="rId2"/><p:sldId id="257" r:id="rId1"/></p:sldIdLst></p:presentation>',
            )
            package.writestr(
                "ppt/_rels/presentation.xml.rels",
                '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide2.xml"/></Relationships>',
            )
            package.writestr("ppt/slides/slide1.xml", '<p:sld xmlns:p="urn:p"><p:cSld>V6_PAGE_ID:N001 V6_ASSET_IDS:</p:cSld></p:sld>')
            package.writestr("ppt/slides/slide2.xml", '<p:sld xmlns:p="urn:p"><p:cSld>V6_PAGE_ID:N002 V6_ASSET_IDS:</p:cSld></p:sld>')
        self.assertEqual(["N002", "N001"], [item["page_ids"][0] for item in inspect_pptx(path)])

    def test_inspect_pptx_separately_reads_hidden_notes_assets_and_media(self):
        path = ARTIFACT_DIR / "ooxml-facts.pptx"
        media = b"approved-scene-bytes"
        with zipfile.ZipFile(path, "w") as package:
            package.writestr("ppt/presentation.xml", '<p:presentation xmlns:p="urn:p" xmlns:r="urn:r"><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst></p:presentation>')
            package.writestr("ppt/_rels/presentation.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/></Relationships>')
            package.writestr("ppt/slides/slide1.xml", '<p:sld xmlns:p="urn:p" show="0"><p:cSld>V6_PAGE_ID:N001 V6_ASSET_IDS:A_SCENE V6_ASSET_RELATIONSHIPS:A_SCENE@rId2</p:cSld></p:sld>')
            package.writestr("ppt/slides/_rels/slide1.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/image1.png"/></Relationships>')
            package.writestr("ppt/notesSlides/notesSlide1.xml", '<p:notes xmlns:p="urn:p">V6_EVENT_ID:E_END</p:notes>')
            package.writestr("ppt/media/image1.png", media)
        observed = inspect_pptx(path)[0]
        self.assertTrue(observed["hidden"])
        self.assertEqual(["E_END"], observed["notes_event_ids"])
        self.assertEqual(["A_SCENE"], observed["asset_ids"])
        self.assertEqual([hashlib.sha256(media).hexdigest()], observed["media_sha256"])
        self.assertEqual("A_SCENE", observed["media_bindings"][0]["asset_id"])

    def test_inspect_pptx_reads_hidden_flag_from_presentation_slide_id(self):
        path = ARTIFACT_DIR / "presentation-hidden.pptx"
        with zipfile.ZipFile(path, "w") as package:
            package.writestr("ppt/presentation.xml", '<p:presentation xmlns:p="urn:p" xmlns:r="urn:r"><p:sldIdLst><p:sldId id="256" r:id="rId1" show="0"/></p:sldIdLst></p:presentation>')
            package.writestr("ppt/_rels/presentation.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/></Relationships>')
            package.writestr("ppt/slides/slide1.xml", '<p:sld xmlns:p="urn:p"><p:cSld>V6_PAGE_ID:N001 V6_ASSET_IDS:</p:cSld></p:sld>')
        self.assertTrue(inspect_pptx(path)[0]["hidden"])

    def test_malformed_pptx_returns_a_stable_physical_source_failure(self):
        doc = add_release_evidence(valid_freeze_document())
        artifact = doc["final_release"]["release_artifact_manifest"]["artifacts"][0]
        malformed = ARTIFACT_DIR / "malformed.pptx"
        with zipfile.ZipFile(malformed, "w") as package:
            package.writestr("ppt/presentation.xml", "<not-closed")
            package.writestr("ppt/_rels/presentation.xml.rels", "<Relationships/>")
        artifact["source_path"] = str(malformed)
        artifact["source_sha256"] = file_digest(malformed)
        artifact["file_observation"]["observed_source_sha256"] = file_digest(malformed)
        self.assertIn("RELEASE_PHYSICAL_SOURCE_MISMATCH", codes(doc, mode="release"))

    def test_character_reference_rejects_wrong_frozen_anchor_values(self):
        doc = add_release_evidence(valid_freeze_document())
        manifest_path = ARTIFACT_DIR / "wrong-character-anchor.json"
        original_path = Path(doc["final_release"]["approved_visual_assets_manifest"]["character_reference_manifest_path"])
        manifest = json.loads(original_path.read_text(encoding="utf-8"))
        manifest["characters"][0]["proportion"]["head_to_body_ratio"] = -100
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        approved = doc["final_release"]["approved_visual_assets_manifest"]
        approved["character_reference_manifest_path"] = str(manifest_path)
        approved["character_reference_manifest_sha256"] = file_digest(manifest_path)
        self.assertIn("RELEASE_CHARACTER_MANIFEST_INVALID", codes(doc, mode="release"))

    def test_character_reference_rejects_wrong_clothing_and_hairstyle_anchors(self):
        doc = add_release_evidence(valid_freeze_document())
        manifest_path = ARTIFACT_DIR / "wrong-costume-anchor.json"
        original_path = Path(doc["final_release"]["approved_visual_assets_manifest"]["character_reference_manifest_path"])
        manifest = json.loads(original_path.read_text(encoding="utf-8"))
        manifest["characters"][0]["clothing_id"] = "LATER_DYNASTY_COSTUME"
        manifest["characters"][0]["hairstyle_id"] = "FANTASY_CROWN"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        approved = doc["final_release"]["approved_visual_assets_manifest"]
        approved["character_reference_manifest_path"] = str(manifest_path)
        approved["character_reference_manifest_sha256"] = file_digest(manifest_path)
        self.assertIn("RELEASE_CHARACTER_MANIFEST_INVALID", codes(doc, mode="release"))


if __name__ == "__main__":
    unittest.main()
