#!/usr/bin/env python3
"""Validate the deterministic knowledge-extraction foundation.

Purpose: validate one work/knowledge tree and emit one machine-readable report.
Input: a knowledge root containing _meta registries, contracts, and templates.
Output: one JSON validation report plus a concise console summary.
Side effects: atomically replaces only the requested validation report.
Errors: exit 1 for validation failures and 2 for unreadable contracts/inputs.
Split trigger: semantic content review must live in a separate review tool.
"""

import argparse
import hashlib
import json
import os
import sys
import tempfile
from collections import Counter
from datetime import datetime
from pathlib import Path


TASK_GROUPS = (
    "整本书阅读与研讨",
    "当代文化参与",
    "跨媒介阅读与交流",
    "语言积累、梳理与探究",
    "文学阅读与写作",
    "思辨性阅读与表达",
    "实用性阅读与交流",
    "中华传统文化经典研习",
    "中国革命传统作品研习",
    "中国现当代作家作品研习",
    "外国作家作品研习",
    "科学与文化论著研习",
    "汉字汉语专题研讨",
    "中华传统文化专题研讨",
    "中国革命传统作品专题研讨",
    "中国现当代作家作品专题研讨",
    "跨文化专题研讨",
    "学术论著专题研讨",
)
EXPECTED_DELIVERABLE_COUNTS = {
    "knowledge_card": 81,
    "unit_graph": 28,
    "book_summary": 5,
    "exam_analysis": 4,
    "exam_kp_mapping": 1,
    "global_map": 1,
}
REQUIRED_TEMPLATES = {
    "knowledge_card_v2.md",
    "unit_graph_v2.md",
    "book_summary_v2.md",
    "exam_analysis_v2.md",
    "exam_kp_mapping_v2.md",
    "global_map_v2.md",
    "review_score_v2.md",
    "unit_brief_v2.md",
    "agent_task_packet.md",
}
REQUIRED_SCHEMAS = {
    "source.schema.json",
    "artifact.schema.json",
    "source_relation.schema.json",
    "split_manifest.schema.json",
    "deliverable.schema.json",
    "knowledge_card.schema.json",
    "evidence.schema.json",
    "review.schema.json",
}


def load_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def load_jsonl(path):
    records = []
    with Path(path).open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSON: {exc.msg}") from exc
    return records


def _duplicates(values):
    counts = Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def validate_taxonomy(taxonomy):
    errors = []
    names = tuple(item.get("name") for item in taxonomy.get("task_groups", []))
    numbers = tuple(item.get("number") for item in taxonomy.get("task_groups", []))
    if names != TASK_GROUPS or numbers != tuple(range(1, 19)):
        errors.append("任务群必须严格等于课标18个规范名称及1—18编号")
    if taxonomy.get("contract_status") != "candidate":
        errors.append("G2前taxonomy contract_status必须为candidate")
    statuses = taxonomy.get("deliverable_statuses", [])
    if len(statuses) != len(set(statuses)):
        errors.append("deliverable_statuses存在重复值")
    transitions = taxonomy.get("status_transitions", {})
    for source, targets in transitions.items():
        if source not in statuses:
            errors.append(f"状态机起点不在受控状态中: {source}")
        for target in targets:
            if target not in statuses:
                errors.append(f"状态机终点不在受控状态中: {source}->{target}")
    if taxonomy.get("quality_descriptor_policy", {}).get("forbidden") is None:
        errors.append("缺少学业质量水平禁用边界")
    return errors


def validate_rubrics(rubrics):
    errors = []
    required_types = set(EXPECTED_DELIVERABLE_COUNTS)
    actual_types = set(rubrics.get("rubrics", {}))
    if actual_types != required_types:
        errors.append(f"量表类型不完整: expected={sorted(required_types)}, actual={sorted(actual_types)}")
    for artifact_type, rubric in rubrics.get("rubrics", {}).items():
        dimensions = rubric.get("dimensions", [])
        total = sum(item.get("weight", 0) for item in dimensions)
        if total != 100:
            errors.append(f"{artifact_type}量表权重合计为{total}，必须为100")
        for dimension in dimensions:
            checkpoint_total = sum(dimension.get("checkpoints", {}).values())
            if checkpoint_total != dimension.get("weight"):
                errors.append(
                    f"{artifact_type}.{dimension.get('id')}检查点合计{checkpoint_total}"
                    f"不等于维度权重{dimension.get('weight')}"
                )
            if dimension.get("minimum", 0) > dimension.get("weight", 0):
                errors.append(f"{artifact_type}.{dimension.get('id')}单项门槛超过权重")
    return errors


def validate_deliverables(deliverables, known_source_ids, taxonomy):
    errors = []
    ids = [item.get("deliverable_id") for item in deliverables]
    known_ids = set(ids)
    for duplicate in _duplicates(ids):
        errors.append(f"重复deliverable_id: {duplicate}")
    paths = [item.get("output_path") for item in deliverables]
    for duplicate in _duplicates(paths):
        errors.append(f"重复output_path: {duplicate}")
    counts = Counter(item.get("deliverable_type") for item in deliverables)
    if dict(counts) != EXPECTED_DELIVERABLE_COUNTS:
        errors.append(f"120项交付恒等式失败: {dict(counts)}")
    allowed_statuses = set(taxonomy.get("deliverable_statuses", []))
    for item in deliverables:
        deliverable_id = item.get("deliverable_id", "<missing>")
        if item.get("schema_version") != "2.0-candidate":
            errors.append(f"{deliverable_id} schema_version非法")
        if item.get("status") not in allowed_statuses:
            errors.append(f"{deliverable_id} status非法: {item.get('status')}")
        for source_id in item.get("source_ids", []):
            if source_id not in known_source_ids:
                errors.append(f"{deliverable_id}引用不存在Source: {source_id}")
        for upstream_id in item.get("upstream_deliverable_ids", []):
            if upstream_id not in known_ids:
                errors.append(f"{deliverable_id}引用不存在上游: {upstream_id}")
            if upstream_id == deliverable_id:
                errors.append(f"{deliverable_id}不得依赖自身")
    return errors


def _sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def validate_registry_links(project_root, sources, artifacts, relations, manifests, verify_hashes=True):
    errors = []
    root = Path(project_root)
    source_ids = [item.get("source_id") for item in sources]
    artifact_ids = [item.get("artifact_id") for item in artifacts]
    source_set, artifact_set = set(source_ids), set(artifact_ids)
    for duplicate in _duplicates(source_ids):
        errors.append(f"重复source_id: {duplicate}")
    for duplicate in _duplicates(artifact_ids):
        errors.append(f"重复artifact_id: {duplicate}")

    package_sources = [item for item in sources if item.get("source_kind") == "textbook_package"]
    audience_counts = Counter(item.get("audience") for item in package_sources)
    if len(package_sources) != 144 or audience_counts != {"student": 113, "teacher": 31}:
        errors.append(f"144源包恒等式失败: total={len(package_sources)}, audiences={dict(audience_counts)}")

    canonical_by_source = Counter(item.get("source_id") for item in artifacts if item.get("is_canonical"))
    for source in sources:
        source_id = source.get("source_id")
        canonical_id = source.get("canonical_artifact_id")
        if canonical_by_source[source_id] != 1:
            errors.append(f"{source_id} canonical Artifact数量为{canonical_by_source[source_id]}，必须为1")
        if canonical_id not in artifact_set:
            errors.append(f"{source_id} canonical Artifact不存在: {canonical_id}")
        elif not any(
            item.get("artifact_id") == canonical_id
            and item.get("source_id") == source_id
            and item.get("is_canonical")
            and item.get("authenticity_status") == "verified"
            for item in artifacts
        ):
            errors.append(f"{source_id} canonical Artifact未通过verified绑定检查")

    for artifact in artifacts:
        artifact_id = artifact.get("artifact_id", "<missing>")
        if artifact.get("source_id") not in source_set:
            errors.append(f"{artifact_id}引用不存在Source: {artifact.get('source_id')}")
        derived_from = artifact.get("derived_from")
        if derived_from and derived_from not in artifact_set:
            errors.append(f"{artifact_id} derived_from不存在: {derived_from}")
        local_path = root / artifact.get("local_path", "")
        if not local_path.is_file():
            errors.append(f"{artifact_id}文件不存在: {artifact.get('local_path')}")
            continue
        if local_path.stat().st_size != artifact.get("byte_size"):
            errors.append(f"{artifact_id}文件大小变化")
        if verify_hashes and _sha256(local_path) != artifact.get("sha256"):
            errors.append(f"{artifact_id} SHA-256变化")
        if local_path.suffix == ".json":
            try:
                load_json(local_path)
            except (OSError, json.JSONDecodeError) as exc:
                errors.append(f"{artifact_id} JSON不可解析: {exc}")

    relation_ids = [item.get("relation_id") for item in relations]
    for duplicate in _duplicates(relation_ids):
        errors.append(f"重复relation_id: {duplicate}")
    for relation in relations:
        for field in ("source_id_from", "source_id_to"):
            if relation.get(field) not in source_set:
                errors.append(f"{relation.get('relation_id')} {field}不存在: {relation.get(field)}")

    if len(manifests) != 144:
        errors.append(f"split_manifest数量为{len(manifests)}，必须为144")
    for manifest in manifests:
        split_id = manifest.get("split_id", "<missing>")
        if manifest.get("master_artifact_id") not in artifact_set:
            errors.append(f"{split_id} master_artifact_id不存在")
        if manifest.get("split_artifact_id") not in artifact_set:
            errors.append(f"{split_id} split_artifact_id不存在")
        expected_pages = manifest.get("original_page_end", 0) - manifest.get("original_page_start", 0) + 1
        if expected_pages != manifest.get("split_page_count") or not manifest.get("page_count_check"):
            errors.append(f"{split_id}页数恒等式失败")
        if manifest.get("mapping_verification_status") != "verified":
            errors.append(f"{split_id}页码映射未verified")
    return errors


def validate_contract_files(knowledge_root):
    errors = []
    root = Path(knowledge_root)
    schema_dir = root / "_meta" / "schemas"
    template_dir = root / "_templates"
    actual_schemas = {path.name for path in schema_dir.glob("*.json")}
    actual_templates = {path.name for path in template_dir.glob("*.md")}
    for missing in sorted(REQUIRED_SCHEMAS - actual_schemas):
        errors.append(f"缺少Schema: {missing}")
    for missing in sorted(REQUIRED_TEMPLATES - actual_templates):
        errors.append(f"缺少模板: {missing}")
    for path in schema_dir.glob("*.json"):
        try:
            schema = load_json(path)
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Schema不可解析 {path.name}: {exc}")
            continue
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            errors.append(f"{path.name}不是JSON Schema 2020-12")
    return errors


def validate_existing_outputs(project_root, deliverables):
    errors = []
    root = Path(project_root)
    for item in deliverables:
        status = item.get("status")
        if status == "draft_existing":
            path = item.get("legacy_path")
            if not path or not (root / path).is_file():
                errors.append(f"{item.get('deliverable_id')} legacy_path不存在")
        elif status not in {"planned"}:
            path = item.get("output_path")
            if not path or not (root / path).is_file():
                errors.append(f"{item.get('deliverable_id')}状态为{status}但output_path不存在")
    return errors


def _write_json_atomic(path, payload):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def run_validation(project_root, report_path, verify_hashes=True):
    root = Path(project_root).resolve()
    knowledge_root = root / "work" / "knowledge"
    meta = knowledge_root / "_meta"
    taxonomy = load_json(meta / "taxonomy.yaml")
    rubrics = load_json(meta / "rubrics.json")
    sources = load_jsonl(meta / "sources.jsonl")
    artifacts = load_jsonl(meta / "artifacts.jsonl")
    relations = load_jsonl(meta / "source_relations.jsonl")
    manifests = load_jsonl(meta / "split_manifest.jsonl")
    deliverables = load_jsonl(meta / "deliverables.jsonl")

    checks = {
        "taxonomy": validate_taxonomy(taxonomy),
        "rubrics": validate_rubrics(rubrics),
        "deliverables": validate_deliverables(deliverables, {item["source_id"] for item in sources}, taxonomy),
        "registry_links": validate_registry_links(root, sources, artifacts, relations, manifests, verify_hashes),
        "contracts": validate_contract_files(knowledge_root),
        "existing_outputs": validate_existing_outputs(root, deliverables),
    }
    errors = [error for group in checks.values() for error in group]
    now = datetime.now().astimezone()
    report = {
        "run_id": now.strftime("VAL-%Y%m%d-%H%M%S%z"),
        "run_at": now.isoformat(),
        "command": " ".join(sys.argv),
        "project_root": str(root),
        "result": "passed" if not errors else "failed",
        "hash_verification": verify_hashes,
        "counts": {
            "sources": len(sources),
            "artifacts": len(artifacts),
            "source_relations": len(relations),
            "split_mappings": len(manifests),
            "deliverables": len(deliverables),
            "accepted_deliverables": sum(item.get("status") == "accepted" for item in deliverables),
        },
        "checks": {name: {"result": "passed" if not group else "failed", "error_count": len(group)} for name, group in checks.items()},
        "errors": errors,
        "warnings": [
            "外部评价体系、初中依据、四川政策和四年真题尚未完整登记",
            "TB2与B2的edition_match仍为unknown",
            "契约状态为candidate，须经G2校准后冻结",
        ],
    }
    _write_json_atomic(report_path, report)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--report", default=None)
    parser.add_argument("--skip-hash-check", action="store_true")
    args = parser.parse_args()
    root = Path(args.project_root).resolve()
    report_path = Path(args.report) if args.report else root / "work/knowledge/_meta/validation_reports/latest.json"
    try:
        report = run_validation(root, report_path, verify_hashes=not args.skip_hash_check)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"result": "error", "message": str(exc)}, ensure_ascii=False))
        return 2
    print(
        json.dumps(
            {
                "result": report["result"],
                "run_id": report["run_id"],
                "errors": len(report["errors"]),
                "report": str(report_path),
            },
            ensure_ascii=False,
        )
    )
    return 0 if report["result"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
