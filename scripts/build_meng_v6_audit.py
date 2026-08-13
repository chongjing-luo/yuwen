#!/usr/bin/env python3
"""Build the pending S001-S127 V6 legacy-audit skeleton from the V5.3 snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = PROJECT_ROOT / "work" / "备课" / "选择性必修下册" / "氓"
STAGE_DIR = LESSON_DIR / "_v6_stage"
SNAPSHOT_PATH = LESSON_DIR / "06_氓_V5课程数据快照.json"
JSON_OUTPUT = STAGE_DIR / "05_氓_V6逐页功能审计.json"
MARKDOWN_OUTPUT = STAGE_DIR / "05_氓_V6逐页功能审计.md"
AUDIT_SOURCE_DIR = PROJECT_ROOT / "scripts" / "meng_v6" / "audit"
INDEX_OUTPUT = AUDIT_SOURCE_DIR / "index.json"


@dataclass(frozen=True)
class Batch:
    batch_id: str
    start: int
    end: int
    content: str

    @property
    def range_label(self) -> str:
        return f"S{self.start:03d}—S{self.end:03d}"


BATCHES = (
    Batch("A", 1, 16, "隐藏导航、封面、导入、三问、首次听读、最小支架"),
    Batch("B1", 17, 27, "第一章及章内活动"),
    Batch("B2", 28, 39, "模块承接、第二章及章内活动"),
    Batch("B3", 40, 50, "第三章及章内活动"),
    Batch("B4", 51, 62, "模块承接、第四章及章内活动"),
    Batch("B5", 63, 73, "第五章及章内活动"),
    Batch("B6", 74, 85, "模块承接、第六章及章内活动"),
    Batch("C1", 86, 95, "全文回读、初读修订、问题一"),
    Batch("C2", 96, 101, "问题二"),
    Batch("C3", 102, 112, "问题三、责任/阻力、第一章回看"),
    Batch("C4", 113, 116, "婚姻圆桌"),
    Batch("D", 117, 127, "知识检索、收纳、终读、退出条"),
)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def serialized_sha256(value: Any) -> str:
    return hashlib.sha256(json_text(value).encode("utf-8")).hexdigest()


def batch_for(number: int) -> Batch:
    matches = [batch for batch in BATCHES if batch.start <= number <= batch.end]
    if len(matches) != 1:
        raise ValueError(f"legacy page S{number:03d} does not belong to exactly one batch")
    return matches[0]


def pending_gate(gate_id: str) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "gate_status": "pending",
        "evidence_refs": [],
        "failure_code": None,
        "reviewer": None,
        "reviewed_at": None,
    }


def pending_review() -> dict[str, Any]:
    record = {"status": "pending", "reviewer": None, "reviewed_at": None, "defect_ids": []}
    return {
        "scope": "legacy_initial_diagnosis",
        "self_review": dict(record),
        "student_reception": dict(record),
        "visual": dict(record),
        "consensus": "pending",
        "adjudication": None,
    }


def page_skeletons(snapshot: dict[str, Any], snapshot_sha256: str) -> list[dict[str, Any]]:
    slides = snapshot.get("slides")
    if not isinstance(slides, list):
        raise ValueError("V5 snapshot has no slide list")
    expected_ids = [f"S{number:03d}" for number in range(1, 128)]
    actual_ids = [slide.get("id") for slide in slides if isinstance(slide, dict)]
    if actual_ids != expected_ids:
        raise ValueError("legacy source must cover ordered S001-S127 exactly once")
    forbidden_conclusions = {
        "decision", "decision_status", "closure_status", "closure_evidence_refs",
        "target_refs", "closed_failure_codes", "closed_defect_ids",
    }
    if any(forbidden_conclusions & set(slide) for slide in slides):
        raise ValueError("V5 snapshot contains a prefilled audit conclusion")

    pages: list[dict[str, Any]] = []
    for number, slide in enumerate(slides, start=1):
        batch = batch_for(number)
        page_id = f"S{number:03d}"
        diagnosis_path = f"scripts/meng_v6/audit/{batch.batch_id}_initial.json"
        disposition_path = f"scripts/meng_v6/audit/{batch.batch_id}_disposition.json"
        pages.append({
            "node_id": page_id,
            "page_id": page_id,
            "node_type": "page",
            "audit_scope": "pending",
            "owner_event_id": None,
            "source_order": number,
            "source_snapshot_path": "work/备课/选择性必修下册/氓/06_氓_V5课程数据快照.json",
            "source_snapshot_sha256": snapshot_sha256,
            "source_module": slide.get("module"),
            "source_phase": slide.get("phase"),
            "source_kind": slide.get("kind"),
            "source_title": slide.get("title") or slide.get("original") or slide.get("kind"),
            "source_visible_text": slide.get("visible", ""),
            "source_minutes": slide.get("minutes"),
            "legacy_student_visible": slide.get("kind") != "teacher_index",
            "batch_id": batch.batch_id,
            "batch_range": batch.range_label,
            "batch_content": batch.content,
            "initial_diagnosis_source": diagnosis_path,
            "disposition_source": disposition_path,
            "content_elements": [
                {"element_id": "visible_text", "kind": "text", "source_field": "source_visible_text"},
                {"element_id": "page_function", "kind": "function", "source_field": "source_title"},
                {"element_id": "layout_identity", "kind": "layout", "source_field": "source_kind"},
            ],
            "gates": [pending_gate(f"G{gate}") for gate in range(1, 7)],
            "review_status": pending_review(),
        })
    return pages


def build_stage_document(
    pages: list[dict[str, Any]],
    snapshot_sha256: str,
    index_sha256: str,
    *,
    document_status: str = "legacy_skeleton_pending_review",
) -> dict[str, Any]:
    empty_inventory = {"pages": [], "events": [], "g5_edges": []}
    return {
        "schema_version": "2.0",
        "audit_version": "6.0-page-function-audit",
        "document_status": document_status,
        "claim_boundary": "desktop_design_scaffold_only",
        "legacy_source": {
            "path": "work/备课/选择性必修下册/氓/06_氓_V5课程数据快照.json",
            "sha256": snapshot_sha256,
            "index_path": "scripts/meng_v6/audit/index.json",
            "index_sha256": index_sha256,
        },
        "legacy_initial_audit": pages,
        "pages": pages,
        "legacy_event_evidence": [],
        "defect_registry": [],
        "initial_audit_seals": [],
        "seal_amendments": [],
        "legacy_effective_view": pages,
        "effective_legacy_hash": canonical_sha256(pages),
        "legacy_disposition_closure": [],
        "structure_manifest": empty_inventory,
        "declared_node_inventory": empty_inventory,
        "source_graph_inventory": empty_inventory,
        "structure_assembly_snapshot": empty_inventory,
        "current_release_audit": {"pages": [], "events": []},
        "global_checks": {},
    }


def render_markdown(pages: list[dict[str, Any]], snapshot_sha256: str) -> str:
    lines = [
        "# 《氓》V6逐页功能审计｜旧版127页待审骨架",
        "",
        "> 状态：待审，不代表保留、删除或关闭。这里只导入V5.3的稳定事实，未声称V6课堂材料已经完成，更未声称学生已经学会。",
        "",
        f"- 旧页：127页（S001—S127）",
        f"- 来源快照SHA-256：`{snapshot_sha256}`",
        "- 审计状态：全部六门与三方审查均为`pending`",
        "- 旧`experience/thought/learning`模板字段未导入为V6证据",
        "",
        "## 十二个审计批次",
        "",
        "| 批次 | 范围 | 内容 | 初诊源 | 处置源 |",
        "|---|---|---|---|---|",
    ]
    for batch in BATCHES:
        lines.append(
            f"| {batch.batch_id} | {batch.range_label} | {batch.content} | "
            f"`scripts/meng_v6/audit/{batch.batch_id}_initial.json` | "
            f"`scripts/meng_v6/audit/{batch.batch_id}_disposition.json` |"
        )
    lines.extend([
        "",
        "## 旧页稳定事实清单",
        "",
        "| 旧ID | 批次 | 模块 | 阶段 | 页型 | 标题 | 可见性 | 旧时长 | 六门 | 三方审查 |",
        "|---|---|---|---|---|---|---|---:|---|---|",
    ])
    for page in pages:
        title = str(page.get("source_title", "")).replace("|", "｜").replace("\n", " ")
        lines.append(
            f"| {page['page_id']} | {page['batch_id']} | {page['source_module']} | "
            f"{page['source_phase']} | {page['source_kind']} | {title} | "
            f"{'学生可见' if page['legacy_student_visible'] else '教师隐藏'} | "
            f"{page['source_minutes']} | pending×6 | pending×3 |"
        )
    lines.extend([
        "",
        "## 逐页可见文字核对",
        "",
        "> 本节展示旧PPT每页导入骨架的完整可见文字，供人工判断页面功能、认知负荷与前台语言；它不是V6拟保留内容。",
        "",
    ])
    for page in pages:
        lines.extend([
            f"### {page['page_id']}｜{str(page.get('source_title', '')).replace(chr(10), ' ')}",
            "",
            f"- 可见性：{'学生可见' if page['legacy_student_visible'] else '教师隐藏'}",
            "- 学生可见文字：",
            "",
        ])
        visible_lines = str(page.get("source_visible_text", "")).splitlines() or [""]
        lines.extend(f"> {line}" if line else ">" for line in visible_lines)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def batch_documents(pages: list[dict[str, Any]], snapshot_sha256: str) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    sources: dict[str, dict[str, Any]] = {}
    index_batches = []
    for batch in BATCHES:
        batch_pages = [page for page in pages if page["batch_id"] == batch.batch_id]
        initial = {
            "schema_version": "1.0", "batch_id": batch.batch_id, "range": batch.range_label,
            "source_snapshot_sha256": snapshot_sha256, "status": "pending_review", "pages": batch_pages,
        }
        disposition = {
            "schema_version": "1.0", "batch_id": batch.batch_id, "range": batch.range_label,
            "based_on_initial_sha256": serialized_sha256(initial), "status": "not_started", "closures": [],
        }
        initial_path = AUDIT_SOURCE_DIR / f"{batch.batch_id}_initial.json"
        disposition_path = AUDIT_SOURCE_DIR / f"{batch.batch_id}_disposition.json"
        initial_relative = initial_path.relative_to(PROJECT_ROOT).as_posix()
        disposition_relative = disposition_path.relative_to(PROJECT_ROOT).as_posix()
        sources[initial_relative] = initial
        sources[disposition_relative] = disposition
        index_batches.append({
            "batch_id": batch.batch_id, "range": batch.range_label, "content": batch.content,
            "initial_source": initial_relative,
            "initial_sha256": serialized_sha256(initial),
            "disposition_source": disposition_relative,
            "disposition_sha256": serialized_sha256(disposition),
            "page_count": len(batch_pages),
        })
    index = {
        "schema_version": "1.0", "source_snapshot_sha256": snapshot_sha256,
        "page_count": len(pages), "legacy_ids": [page["page_id"] for page in pages],
        "batches": index_batches,
    }
    return index, sources


def write_outputs(snapshot: dict[str, Any], snapshot_sha256: str) -> None:
    pages = page_skeletons(snapshot, snapshot_sha256)
    index, sources = batch_documents(pages, snapshot_sha256)
    index_sha256 = serialized_sha256(index)
    document = build_stage_document(
        pages,
        snapshot_sha256,
        index_sha256,
        document_status="legacy_skeleton_pending_review",
    )
    markdown = render_markdown(pages, snapshot_sha256)

    AUDIT_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    STAGE_DIR.mkdir(parents=True, exist_ok=True)
    for relative_path, source in sources.items():
        (PROJECT_ROOT / relative_path).write_text(json_text(source), encoding="utf-8")
    INDEX_OUTPUT.write_text(json_text(index), encoding="utf-8")
    JSON_OUTPUT.write_text(json_text(document), encoding="utf-8")
    MARKDOWN_OUTPUT.write_text(markdown, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("stage",), default="stage")
    return parser.parse_args()


def main() -> int:
    parse_args()
    snapshot = json.loads(SNAPSHOT_PATH.read_text(encoding="utf-8"))
    snapshot_sha256 = file_sha256(SNAPSHOT_PATH)
    write_outputs(snapshot, snapshot_sha256)
    print(f"AUDIT_SKELETON_OK pages=127 batches={len(BATCHES)} output={JSON_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
