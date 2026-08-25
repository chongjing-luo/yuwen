from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from test_validate_lesson_lineage import _chain  # noqa: E402
from validate_lesson_audit import validate_audit_lock as _validate_audit_lock  # noqa: E402
from validate_lesson_plan import canonical_json_sha256  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, value: dict | str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) if isinstance(value, dict) else value
    path.write_text(text, encoding="utf-8")
    return path


def _audit_lock(tmp_path: Path) -> dict:
    config_source = ROOT / "work/principles/enforcement_config.json"
    registry_text = (ROOT / "work/principles/registry.yaml").read_text(encoding="utf-8")
    registry = yaml.safe_load(registry_text) or {}
    standard_version = str((registry.get("meta") or {}).get("standard_version") or "")
    assert standard_version.startswith("STANDARD-")
    _write(
        tmp_path / "work/principles/enforcement_config.json",
        config_source.read_text(encoding="utf-8"),
    )
    _, materials_lock = _chain(tmp_path)
    meta = tmp_path / "work/teaching/lesson/_meta"
    materials_path = _write(meta / "materials_lock.json", materials_lock)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    frozen_artifacts_sha256 = canonical_json_sha256(manifest["artifacts"])

    standard_snapshot = _write(
        meta / f"reviews/{standard_version}.yaml",
        registry_text,
    )
    frozen_config = _write(
        meta / f"reviews/enforcement_config.{standard_version}.json",
        config_source.read_text(encoding="utf-8"),
    )
    report = {
        "schema_version": "audit-report.v1",
        "lesson_id": "LES-TEST-01",
        "materials_lock_sha256": _sha(materials_path),
        "frozen_artifacts_sha256": frozen_artifacts_sha256,
        "standard_version": standard_version,
        "standard_registry_sha256": _sha(standard_snapshot),
        "enforcement_config_sha256": _sha(frozen_config),
        "machine_checks": [
            {"name": "g0-g3-lineage", "exit_code": 0},
            {"name": "lesson-schema-strict", "exit_code": 0},
            {"name": "principle-checks", "exit_code": 0},
        ],
        "review_rounds": [
            {"round_id": "R1", "frozen_artifacts_sha256": frozen_artifacts_sha256, "open_severities": ["P3"]},
            {"round_id": "R2", "frozen_artifacts_sha256": frozen_artifacts_sha256, "open_severities": ["P3"]},
        ],
        "findings": [],
        "p3_risks": [
            {
                "category": "office_rendering",
                "statement": "结构校验不能证明Office真实渲染没有错位或溢出。",
                "verification_plan": "在目标教室设备打开并逐页截图复核后只追加结果。",
            },
            {
                "category": "classroom_pacing",
                "statement": "桌面时间盒不能证明真实课堂节奏与等待时长合宜。",
                "verification_plan": "试教时记录各事件实耗与学生停顿并据证据回教。",
            },
            {
                "category": "learning_effect",
                "statement": "尚无学生作品证明掌握、理解或享受已经真实发生。",
                "verification_plan": "采集首答末答、退出条和延迟回取数据后再判断。",
            },
        ],
        "claim_boundary": "课堂证据状态：未采集；学生掌握、理解与享受均待真实试教验证。",
    }
    report_path = _write(meta / "reviews/audit_report.json", report)

    review_entries = []
    for role, reviewer_id in (("visual", "visual-reviewer"), ("student_reception", "student-reviewer")):
        receipt = {
            "schema_version": "audit-review.v1",
            "lesson_id": "LES-TEST-01",
            "role": role,
            "reviewer_id": reviewer_id,
            "review_event_id": f"REVIEW-EVENT-{role}",
            "review_source": {
                "locator": f"host-review://2026-08-20/{role}",
                "record_sha256": hashlib.sha256(f"host-event:{role}".encode()).hexdigest(),
            },
            "verification_mode": "external_review_gate",
            "authentication_boundary": "本地JSON只验证结构与血缘，不认证审查者身份；真实审查事件由外部记录人工核验。",
            "author_ids": ["lesson-author-agent", "design-author-agent", "materials-author-agent"],
            "decision": "pass",
            "reviewed_at": "2026-08-20T18:00:00+08:00",
            "materials_lock_sha256": _sha(materials_path),
            "frozen_artifacts_sha256": frozen_artifacts_sha256,
            "standard_version": standard_version,
            "standard_registry_sha256": _sha(standard_snapshot),
            "enforcement_config_sha256": _sha(frozen_config),
            "defect_ids": [],
            "owner_approval_trace": {
                "checked": True,
                "event_id": "USER-MSG-20260820-150000",
                "boundary": "只复核外部人工回执引用；本地验证器不认证人类身份。",
            },
        }
        receipt_path = _write(meta / f"reviews/{role}_review.json", receipt)
        review_entries.append({"role": role, "path": str(receipt_path.relative_to(tmp_path)), "sha256": _sha(receipt_path)})

    return {
        "schema_version": "audit-lock.v1",
        "lesson_id": "LES-TEST-01",
        "author_ids": ["lesson-author-agent", "design-author-agent", "materials-author-agent"],
        "materials_lock": {"path": str(materials_path.relative_to(tmp_path)), "sha256": _sha(materials_path)},
        "standard_snapshot": {
            "version": standard_version,
            "path": str(standard_snapshot.relative_to(tmp_path)),
            "sha256": _sha(standard_snapshot),
            "registry_sha256": _sha(standard_snapshot),
            "frozen_at": "2026-08-20T17:30:00+08:00",
            "enforcement_config": {
                "path": str(frozen_config.relative_to(tmp_path)),
                "sha256": _sha(frozen_config),
            },
        },
        "audit_report": {"path": str(report_path.relative_to(tmp_path)), "sha256": _sha(report_path)},
        "reviews": review_entries,
        "frozen_artifacts_sha256": frozen_artifacts_sha256,
        "status": "awaiting_host_release",
        "claim_boundary": "课堂证据状态：未采集；学生掌握、理解与享受均待真实试教验证。",
    }


def _external_registry(lock: dict, tmp_path: Path) -> dict:
    events = {}
    for entry in lock.get("reviews") or []:
        review_path = tmp_path / entry["path"]
        review = json.loads(review_path.read_text(encoding="utf-8"))
        source = review.get("review_source") if isinstance(review.get("review_source"), dict) else {}
        event_id = str(review.get("review_event_id") or "")
        events[event_id] = {
            "verified_by_host": True,
            "role": review.get("role"),
            "reviewer_id": review.get("reviewer_id"),
            "locator": source.get("locator"),
            "record_sha256": source.get("record_sha256"),
            "decision": review.get("decision"),
            "materials_lock_sha256": review.get("materials_lock_sha256"),
            "frozen_artifacts_sha256": review.get("frozen_artifacts_sha256"),
            "standard_registry_sha256": review.get("standard_registry_sha256"),
            "enforcement_config_sha256": review.get("enforcement_config_sha256"),
        }
    return {
        "schema_version": "external-review-registry.v1",
        "standard_snapshot": {
            "version": lock["standard_snapshot"]["version"],
            "registry_sha256": lock["standard_snapshot"]["registry_sha256"],
            "enforcement_config_sha256": lock["standard_snapshot"]["enforcement_config"]["sha256"],
        },
        "events": events,
    }


def validate_audit_lock(lock: dict, root: Path) -> list[str]:
    return _validate_audit_lock(
        lock,
        root=root,
        external_review_registry=_external_registry(lock, root),
    )


def test_valid_generic_g4_audit_lock_passes(tmp_path: Path):
    assert validate_audit_lock(_audit_lock(tmp_path), root=tmp_path) == []


def test_g4_requires_both_independent_review_roles(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    lock["reviews"] = [item for item in lock["reviews"] if item["role"] != "student_reception"]
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("student_reception" in error for error in errors)


def test_g4_reviewer_cannot_be_content_author(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    review_path = tmp_path / lock["reviews"][0]["path"]
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["reviewer_id"] = "lesson-author-agent"
    review_path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
    lock["reviews"][0]["sha256"] = _sha(review_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("审查者不能是内容作者" in error for error in errors)


def test_g4_cannot_release_with_open_p0_p1_p2(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    report_path = tmp_path / lock["audit_report"]["path"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["findings"] = [{"defect_id": "D1", "severity": "P1", "status": "open"}]
    report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    lock["audit_report"]["sha256"] = _sha(report_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("仍有开放P0/P1/P2" in error for error in errors)


def test_g4_freeze_invalidates_when_artifact_manifest_changes(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    materials_path = tmp_path / lock["materials_lock"]["path"]
    materials = json.loads(materials_path.read_text(encoding="utf-8"))
    manifest_path = tmp_path / materials["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["artifacts"][0]["sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("G3上游无效" in error or "冻结物料" in error for error in errors)


def test_g4_reviews_must_stay_in_same_lesson_meta(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    review_path = tmp_path / lock["reviews"][0]["path"]
    other = _write(
        tmp_path / "work/teaching/other/_meta/reviews/visual_review.json",
        json.loads(review_path.read_text(encoding="utf-8")),
    )
    lock["reviews"][0] = {
        "role": "visual",
        "path": str(other.relative_to(tmp_path)),
        "sha256": _sha(other),
    }
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("必须位于同一课_meta/reviews" in error for error in errors)


def test_g4_requires_two_final_nonblocking_review_rounds(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    report_path = tmp_path / lock["audit_report"]["path"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["review_rounds"] = report["review_rounds"][:1]
    report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    lock["audit_report"]["sha256"] = _sha(report_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("至少两轮" in error for error in errors)


def test_g4_author_list_must_include_upstream_lesson_author(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    lock["author_ids"] = ["some-other-author"]
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("精确覆盖S2/S3/S4内容作者" in error for error in errors)


def test_g4_owner_trace_boundary_requires_both_local_nonauthentication_and_human_review(tmp_path: Path):
    for boundary in ("外部人工回执已复核。", "本地验证器不认证身份。"):
        lock = _audit_lock(tmp_path)
        review_path = tmp_path / lock["reviews"][0]["path"]
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["owner_approval_trace"]["boundary"] = boundary
        review_path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
        lock["reviews"][0]["sha256"] = _sha(review_path)
        errors = validate_audit_lock(lock, root=tmp_path)
        assert any("本地身份认证边界" in error for error in errors)


def test_g4_final_review_round_ids_must_be_distinct(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    report_path = tmp_path / lock["audit_report"]["path"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["review_rounds"][1]["round_id"] = report["review_rounds"][0]["round_id"]
    report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    lock["audit_report"]["sha256"] = _sha(report_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("复审轮次ID必须不同" in error for error in errors)


def test_g4_claim_boundary_cannot_assert_classroom_success(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    lock["claim_boundary"] = "课堂效果仍待真实试教记录；但学生已经全部学懂并享受，试教已经完成。"
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("待真实课堂/试教验证" in error for error in errors)


def test_g4_finding_severity_must_be_strict_enum(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    report_path = tmp_path / lock["audit_report"]["path"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["findings"] = [{"defect_id": "D1", "severity": "P1 ", "status": "open"}]
    report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    lock["audit_report"]["sha256"] = _sha(report_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("严重度非法" in error for error in errors)


def test_g4_standard_snapshot_must_be_nonempty_and_bind_version(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    standard_path = tmp_path / lock["standard_snapshot"]["path"]
    standard_path.write_text("", encoding="utf-8")
    lock["standard_snapshot"]["sha256"] = _sha(standard_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("standard_snapshot为空" in error for error in errors)


def test_g4_report_requires_explicit_p3_risks(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    report_path = tmp_path / lock["audit_report"]["path"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    del report["p3_risks"]
    report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    lock["audit_report"]["sha256"] = _sha(report_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("p3_risks" in error for error in errors)


def test_g4_reviews_require_external_event_trace_and_identity_boundary(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    review_path = tmp_path / lock["reviews"][0]["path"]
    review = json.loads(review_path.read_text(encoding="utf-8"))
    for field in ("review_event_id", "review_source", "verification_mode", "authentication_boundary"):
        review.pop(field)
    review_path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
    lock["reviews"][0]["sha256"] = _sha(review_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("review_event_id" in error for error in errors)
    assert any("review_source" in error for error in errors)
    assert any("verification_mode" in error for error in errors)
    assert any("authentication_boundary" in error for error in errors)


def test_g4_rejects_one_character_standard_snapshot(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    standard_path = tmp_path / lock["standard_snapshot"]["path"]
    standard_path.write_text("X", encoding="utf-8")
    lock["standard_snapshot"].update(version="X", sha256=_sha(standard_path))
    report_path = tmp_path / lock["audit_report"]["path"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["standard_version"] = "X"
    report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    lock["audit_report"]["sha256"] = _sha(report_path)
    for entry in lock["reviews"]:
        review_path = tmp_path / entry["path"]
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["standard_version"] = "X"
        review_path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
        entry["sha256"] = _sha(review_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("standard_snapshot" in error and "结构" in error for error in errors)


def test_g4_rejects_opaque_review_source_and_unverified_events(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    for entry in lock["reviews"]:
        review_path = tmp_path / entry["path"]
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["review_event_id"] = "x0" if review["role"] == "visual" else "x1"
        review["review_source"] = "x"
        review_path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
        entry["sha256"] = _sha(review_path)
    errors = _validate_audit_lock(lock, root=tmp_path)
    assert any("review_source必须为结构化外部事件引用" in error for error in errors)
    assert any("缺宿主外部审查事件核验" in error for error in errors)


def test_g4_p3_risks_must_cover_three_explicit_residual_categories(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    report_path = tmp_path / lock["audit_report"]["path"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["p3_risks"] = ["x"]
    report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    lock["audit_report"]["sha256"] = _sha(report_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("Office真实渲染、课堂节奏、学习效果" in error for error in errors)


def test_g4_host_registry_must_match_review_event_fields(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    registry = _external_registry(lock, tmp_path)
    first_event = next(iter(registry["events"].values()))
    first_event["record_sha256"] = "0" * 64
    errors = _validate_audit_lock(lock, root=tmp_path, external_review_registry=registry)
    assert any("宿主核验事件字段不匹配: record_sha256" in error for error in errors)


def test_local_g4_object_cannot_claim_released_status(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    lock["status"] = "released"
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("本地G4只能到awaiting_host_release" in error for error in errors)


def test_g4_uses_frozen_enforcement_config_not_live_config(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    live_config_path = tmp_path / "work/principles/enforcement_config.json"
    live_config = json.loads(live_config_path.read_text(encoding="utf-8"))
    live_config["frontstage_banned_v6"].append("沿着原文")
    live_config_path.write_text(json.dumps(live_config, ensure_ascii=False), encoding="utf-8")
    errors = validate_audit_lock(lock, root=tmp_path)
    assert not any("G4原则检查未通过: frontstage_banned" in error for error in errors)


def test_g4_rejects_unknown_classroom_account_claim(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    lock["classroom_account"] = {"status": "verified", "mastery": "学生已经全部掌握。"}
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("audit_lock含未知字段: classroom_account" in error for error in errors)


def test_g4_reviews_must_be_independent_from_s3_and_s4_authors(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    review_path = tmp_path / lock["reviews"][0]["path"]
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["reviewer_id"] = "design-author-agent"
    review_path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
    lock["reviews"][0]["sha256"] = _sha(review_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("审查者不能是内容作者: design-author-agent" in error for error in errors)


def test_audit_report_and_reviews_reject_local_release_claim_fields(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    report_path = tmp_path / lock["audit_report"]["path"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["status"] = "released"
    report["host_release"] = {"confirmed": True}
    report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    lock["audit_report"]["sha256"] = _sha(report_path)
    review_path = tmp_path / lock["reviews"][0]["path"]
    review = json.loads(review_path.read_text(encoding="utf-8"))
    review["host_release_confirmed"] = True
    review_path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
    lock["reviews"][0]["sha256"] = _sha(review_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("audit_report含未知字段: status" in error for error in errors)
    assert any("review[0]含未知字段: host_release_confirmed" in error for error in errors)


def test_g4_rejects_structurally_shrunk_principle_registry(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    standard_path = tmp_path / lock["standard_snapshot"]["path"]
    shrunk = {
        "meta": {"standard_version": "STANDARD-1.0"},
        "nodes": {node: {} for node in ({f"K{i}" for i in range(1, 6)} | {f"U{i}" for i in range(1, 9)} | {f"J{i}" for i in range(1, 8)})},
        "principles": [{}],
    }
    import yaml
    standard_path.write_text(yaml.safe_dump(shrunk, allow_unicode=True), encoding="utf-8")
    lock["standard_snapshot"]["sha256"] = _sha(standard_path)
    lock["standard_snapshot"]["registry_sha256"] = _sha(standard_path)
    report_path = tmp_path / lock["audit_report"]["path"]
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report["standard_registry_sha256"] = _sha(standard_path)
    report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
    lock["audit_report"]["sha256"] = _sha(report_path)
    for entry in lock["reviews"]:
        review_path = tmp_path / entry["path"]
        review = json.loads(review_path.read_text(encoding="utf-8"))
        review["standard_registry_sha256"] = _sha(standard_path)
        review_path.write_text(json.dumps(review, ensure_ascii=False), encoding="utf-8")
        entry["sha256"] = _sha(review_path)
    errors = validate_audit_lock(lock, root=tmp_path)
    assert any("冻结原则注册库无效" in error for error in errors)


def test_frozen_registry_validation_does_not_read_live_documents(tmp_path: Path, monkeypatch):
    lock = _audit_lock(tmp_path)
    validator = _validate_audit_lock.__globals__["validate_principle_registry"]
    monkeypatch.setitem(validator.__globals__, "ROOT", tmp_path / "missing-live-root")
    monkeypatch.setitem(validator.__globals__, "MECHANISM_DOC", tmp_path / "missing-live-mechanism.md")

    errors = validate_audit_lock(lock, root=tmp_path)

    assert not any("冻结原则注册库无效" in error for error in errors)


def test_host_review_events_must_bind_current_candidate_and_standard_hashes(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    registry = _external_registry(lock, tmp_path)
    first_event = next(iter(registry["events"].values()))
    first_event["materials_lock_sha256"] = "0" * 64
    first_event["frozen_artifacts_sha256"] = "0" * 64
    first_event["standard_registry_sha256"] = "0" * 64
    first_event["enforcement_config_sha256"] = "0" * 64
    errors = _validate_audit_lock(lock, root=tmp_path, external_review_registry=registry)
    assert any("宿主核验事件字段不匹配: materials_lock_sha256" in error for error in errors)
    assert any("宿主核验事件字段不匹配: frozen_artifacts_sha256" in error for error in errors)
    assert any("宿主核验事件字段不匹配: standard_registry_sha256" in error for error in errors)
    assert any("宿主核验事件字段不匹配: enforcement_config_sha256" in error for error in errors)


def test_host_registry_must_bind_exact_frozen_standard_hashes(tmp_path: Path):
    lock = _audit_lock(tmp_path)
    registry = _external_registry(lock, tmp_path)
    registry["standard_snapshot"]["enforcement_config_sha256"] = "0" * 64
    errors = _validate_audit_lock(lock, root=tmp_path, external_review_registry=registry)
    assert any("宿主登记的冻结标准哈希不匹配" in error for error in errors)
