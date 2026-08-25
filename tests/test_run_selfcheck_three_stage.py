from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from run_selfcheck import (  # noqa: E402
    discover_lesson_dirs,
    inspect_lesson_chain,
    summarize_classroom_evidence,
)
from test_validate_lesson_audit import _audit_lock, _external_registry  # noqa: E402


ROOT = Path(__file__).resolve().parents[1]


def test_qyc_chain_reports_honest_g2_owner_review_stop():
    ok, detail = inspect_lesson_chain(ROOT / "work/teaching/必修上册/沁园春长沙", root=ROOT)
    assert ok
    assert "G0/G1通过" in detail
    assert "G2候选schema通过" in detail
    assert "design lock" in detail
    assert "诚实停止" in detail


def test_downstream_artifact_without_g1_is_rejected(tmp_path: Path):
    lesson_dir = tmp_path / "work/teaching/测试册/测试课"
    lesson_dir.mkdir(parents=True)
    (lesson_dir / "lesson.json").write_text("{}", encoding="utf-8")
    ok, detail = inspect_lesson_chain(lesson_dir, root=tmp_path)
    assert not ok
    assert "绕过G1" in detail


def test_global_discovery_finds_every_lesson_with_chain_artifacts(tmp_path: Path):
    first = tmp_path / "work/teaching/册一/课一"
    second = tmp_path / "work/teaching/册二/课二"
    (first / "_meta").mkdir(parents=True)
    second.mkdir(parents=True)
    (first / "_meta/evidence_manifest.json").write_text("{}", encoding="utf-8")
    (second / "lesson.json").write_text("{}", encoding="utf-8")
    assert discover_lesson_dirs(tmp_path) == [first, second]


def test_global_discovery_finds_orphan_owner_receipt_and_materials_manifest(tmp_path: Path):
    owner_only = tmp_path / "work/teaching/册一/孤立回执"
    manifest_only = tmp_path / "work/teaching/册二/孤立物料"
    (owner_only / "_meta").mkdir(parents=True)
    (manifest_only / "materials").mkdir(parents=True)
    (owner_only / "_meta/G1_owner_approval.json").write_text("{}", encoding="utf-8")
    (manifest_only / "materials/manifest.json").write_text("{}", encoding="utf-8")
    assert discover_lesson_dirs(tmp_path) == [owner_only, manifest_only]


def test_global_discovery_finds_bare_lesson_plan_and_custom_manifest(tmp_path: Path):
    plan_only = tmp_path / "work/teaching/册一/只有教案"
    custom_manifest = tmp_path / "work/teaching/册二/自定义物料清单"
    plan_only.mkdir(parents=True)
    (custom_manifest / "materials").mkdir(parents=True)
    (plan_only / "教案.md").write_text("# 教案", encoding="utf-8")
    (custom_manifest / "materials/custom-manifest.json").write_text("{}", encoding="utf-8")
    assert discover_lesson_dirs(tmp_path) == [plan_only, custom_manifest]


def test_bare_plan_with_unlocked_pptx_is_not_an_honest_stop(tmp_path: Path):
    lesson_dir = tmp_path / "work/teaching/册一/越级课件"
    (lesson_dir / "materials").mkdir(parents=True)
    (lesson_dir / "教案.md").write_text("# 教案", encoding="utf-8")
    (lesson_dir / "materials/越级课件.pptx").write_bytes(b"not-a-pptx")
    assert discover_lesson_dirs(tmp_path) == [lesson_dir]
    ok, detail = inspect_lesson_chain(lesson_dir, root=tmp_path)
    assert not ok
    assert "绕过G1" in detail


def test_bare_plan_with_root_level_office_files_is_not_an_honest_stop(tmp_path: Path):
    lesson_dir = tmp_path / "work/teaching/册一/根目录越级物料"
    lesson_dir.mkdir(parents=True)
    (lesson_dir / "教案.md").write_text("# 教案", encoding="utf-8")
    (lesson_dir / "课件.pptx").write_bytes(b"not-a-pptx")
    (lesson_dir / "学习单.docx").write_bytes(b"not-a-docx")
    assert discover_lesson_dirs(tmp_path) == [lesson_dir]
    ok, detail = inspect_lesson_chain(lesson_dir, root=tmp_path)
    assert not ok
    assert "绕过G1" in detail


def test_valid_g4_chain_reports_local_candidate_not_release(
    tmp_path: Path,
    monkeypatch,
):
    lock = _audit_lock(tmp_path)
    lesson_dir = tmp_path / "work/teaching/lesson"
    audit_lock_path = lesson_dir / "_meta/audit_lock.json"
    audit_lock_path.write_text(
        json.dumps(lock, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    registry_path = tmp_path.parent / f"{tmp_path.name}_external_review_registry.json"
    registry_path.write_text(
        json.dumps(_external_registry(lock, tmp_path), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    monkeypatch.setenv("YUWEN_EXTERNAL_REVIEW_REGISTRY", str(registry_path))

    ok, detail = inspect_lesson_chain(lesson_dir, root=tmp_path)

    assert ok
    assert "G4本地终审候选结构已验；待宿主放行" in detail
    assert "G4已放行" not in detail


def test_project_local_host_release_file_is_rejected(tmp_path: Path):
    lesson_dir = tmp_path / "work/teaching/册一/伪宿主放行"
    (lesson_dir / "_meta").mkdir(parents=True)
    (lesson_dir / "教案.md").write_text("# 教案", encoding="utf-8")
    (lesson_dir / "_meta/host_release.json").write_text(
        json.dumps({"status": "released"}, ensure_ascii=False),
        encoding="utf-8",
    )
    assert discover_lesson_dirs(tmp_path) == [lesson_dir]
    ok, detail = inspect_lesson_chain(lesson_dir, root=tmp_path)
    assert not ok
    assert "项目内禁止宿主放行凭证" in detail


def test_project_local_nested_host_release_receipt_is_rejected(tmp_path: Path):
    lesson_dir = tmp_path / "work/teaching/册一/嵌套伪宿主放行"
    reviews = lesson_dir / "_meta/reviews"
    reviews.mkdir(parents=True)
    (lesson_dir / "教案.md").write_text("# 教案", encoding="utf-8")
    (reviews / "host_release_receipt.json").write_text(
        json.dumps({"status": "released"}, ensure_ascii=False),
        encoding="utf-8",
    )

    ok, detail = inspect_lesson_chain(lesson_dir, root=tmp_path)

    assert not ok
    assert "项目内禁止宿主放行凭证" in detail


def test_classroom_account_is_empty_only_when_l4_has_no_records(tmp_path: Path):
    classes = tmp_path / "work/teaching/_classes"
    classes.mkdir(parents=True)
    (classes / "README.md").write_text("说明", encoding="utf-8")

    summary = summarize_classroom_evidence(tmp_path)

    assert summary["total_records"] == 0
    assert summary["by_type"] == {}


def test_classroom_account_reports_existing_l4_without_modifying_it(tmp_path: Path):
    class_dir = tmp_path / "work/teaching/_classes/高一1班"
    class_dir.mkdir(parents=True)
    observations = class_dir / "observations.jsonl"
    observations.write_text('{"id":"OBS-1"}\n\n{"id":"OBS-2"}\n', encoding="utf-8")
    mastery = class_dir / "mastery_ledger.jsonl"
    mastery.write_text('{"id":"MR-1"}\n', encoding="utf-8")
    before = observations.read_bytes()

    summary = summarize_classroom_evidence(tmp_path)

    assert summary["total_records"] == 3
    assert summary["by_type"] == {"MR": 1, "OBS": 2}
    assert observations.read_bytes() == before
