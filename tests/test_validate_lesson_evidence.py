from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from pypdf import PdfWriter

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_lesson_evidence import validate  # noqa: E402


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, content: bytes | str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    return path


def _write_pdf(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    writer = PdfWriter()
    writer.add_blank_page(width=100, height=100)
    with path.open("wb") as stream:
        writer.write(stream)
    return path


def _manifest(tmp_path: Path) -> dict:
    textbook = _write_pdf(tmp_path / "Data/textbook.pdf")
    standard = _write_pdf(tmp_path / "Data/curriculum.pdf")
    extract = _write(tmp_path / "Data/textbook_extract/full.md", "# 教材解析\n\n氓之蚩蚩，抱布贸丝。这里保留可核对的原文定位。")
    card = _write(tmp_path / "work/knowledge/card.md", "# 知识卡\n\nKP-CARD-TEST-01-001：关键语句推动叙事转折。")
    dossier = _write(
        tmp_path / "work/teaching/TR-TEST.md",
        """# 文本研究与证据档案

## 规范事实

教材原文、课程标准与篇目位置分别回到登记的PDF核验，不把解析文本冒充规范原件。研究档案记录每项材料的用途和解释边界。

## 裸读与证据

沿“氓之蚩蚩，抱布贸丝”观察动作次序、叙事推进和人物关系，不预先套入人物标签。关键解释必须能够指出原文位置，并区分文本事实、合理推论与现实迁移。

## 学习困难与知识候选

学生可能直接概括人物品质而跳过动作证据，因此候选知识要求先复述动作，再说明前后关系变化。课堂效果尚无证据，留待真实试教观察。
""",
    )
    return {
        "schema_version": "lesson-evidence.v1",
        "lesson_id": "LES-TEST-01",
        "mechanism_nodes": ["K1", "U6", "J7"],
        "normative_sources": [
            {
                "source_id": "SRC-TEXTBOOK",
                "role": "textbook",
                "authority": "S1",
                "path": str(textbook.relative_to(tmp_path)),
                "sha256": _sha(textbook),
            },
            {
                "source_id": "SRC-STANDARD",
                "role": "curriculum_standard",
                "authority": "S1",
                "path": str(standard.relative_to(tmp_path)),
                "sha256": _sha(standard),
            },
        ],
        "derived_sources": [
            {
                "source_id": "SRC-EXTRACT",
                "role": "textbook_extract",
                "path": str(extract.relative_to(tmp_path)),
                "sha256": _sha(extract),
                "derived_from_source_id": "SRC-TEXTBOOK",
                "derived_from_sha256": _sha(textbook),
            }
        ],
        "knowledge_sources": [
            {
                "source_id": "SRC-CARD",
                "path": str(card.relative_to(tmp_path)),
                "sha256": _sha(card),
            }
        ],
        "evidence_dossier": {
            "path": str(dossier.relative_to(tmp_path)),
            "sha256": _sha(dossier),
        },
        "claim_boundary": "课堂证据状态：未采集；学生掌握、理解与享受均待真实试教验证。",
    }


def test_valid_evidence_manifest_passes(tmp_path: Path):
    errors, stats = validate(_manifest(tmp_path), root=tmp_path)
    assert errors == []
    assert stats == {"normative_sources": 2, "derived_sources": 1, "knowledge_sources": 1}


def test_g0_rejects_unregistered_lesson_id_format(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["lesson_id"] = "BAD-ID"

    errors, _ = validate(manifest, root=tmp_path)

    assert any("lesson_id格式非法" in error for error in errors)


def test_g0_manifest_must_live_in_the_lesson_meta_directory(tmp_path: Path):
    manifest = _manifest(tmp_path)
    rogue_path = _write(
        tmp_path / "rogue/evidence_manifest.json",
        json.dumps(manifest, ensure_ascii=False),
    )

    errors, _ = validate(manifest, root=tmp_path, manifest_path=rogue_path)

    assert any("evidence_manifest必须位于课程目录的_meta" in error for error in errors)


def test_g0_rejects_same_lesson_id_in_two_course_directories(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest_path = _write(
        tmp_path / "work/teaching/book/lesson/_meta/evidence_manifest.json",
        json.dumps(manifest, ensure_ascii=False),
    )
    _write(
        tmp_path / "work/teaching/other/lesson/_meta/lesson_plan_candidate.json",
        json.dumps(
            {"schema_version": "lesson-plan-candidate.v1", "lesson_id": manifest["lesson_id"]},
            ensure_ascii=False,
        ),
    )

    errors, _ = validate(manifest, root=tmp_path, manifest_path=manifest_path)

    assert any("lesson_id解析到多个课程目录" in error for error in errors)


def test_requires_textbook_and_curriculum_pdf_roots(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["normative_sources"] = [manifest["normative_sources"][0]]
    errors, _ = validate(manifest, root=tmp_path)
    assert any("curriculum_standard" in error for error in errors)


def test_detects_file_hash_drift(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["evidence_dossier"]["sha256"] = "0" * 64
    errors, _ = validate(manifest, root=tmp_path)
    assert any("SHA-256不匹配" in error for error in errors)


def test_derived_source_must_bind_normative_parent(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["derived_sources"][0]["derived_from_sha256"] = "0" * 64
    errors, _ = validate(manifest, root=tmp_path)
    assert any("上游规范源哈希" in error for error in errors)


def test_knowledge_source_or_explicit_gap_is_required(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["knowledge_sources"] = []
    errors, _ = validate(manifest, root=tmp_path)
    assert any("knowledge_sources为空" in error for error in errors)

    manifest["knowledge_gap_reason"] = "本课知识卡尚未建立，G1不得把候选知识冒充accepted卡片。"
    errors, _ = validate(manifest, root=tmp_path)
    assert not any("knowledge_sources为空" in error for error in errors)


def test_cli_fixture_is_json_serializable(tmp_path: Path):
    json.dumps(_manifest(tmp_path), ensure_ascii=False)


def test_bound_source_paths_must_be_project_relative(tmp_path: Path):
    manifest = _manifest(tmp_path)
    source = manifest["normative_sources"][0]
    source["path"] = str((tmp_path / source["path"]).resolve())
    errors, _ = validate(manifest, root=tmp_path)
    assert any("必须使用项目根相对路径" in error for error in errors)


def test_claim_boundary_must_state_classroom_evidence_is_still_pending(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["claim_boundary"] = "课堂效果仍待真实试教记录；但学生已经全部学懂并享受，试教已经完成。"
    errors, _ = validate(manifest, root=tmp_path)
    assert any("待真实课堂/试教验证" in error for error in errors)


def test_claim_boundary_rejects_paraphrased_classroom_success_contradiction(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["claim_boundary"] = (
        "课堂效果仍待真实试教；但全体学生现在均能准确理解文本并乐在其中，试讲工作已经收官。"
    )
    errors, _ = validate(manifest, root=tmp_path)
    assert any("claim_boundary" in error for error in errors)


def test_derived_source_requires_role(tmp_path: Path):
    manifest = _manifest(tmp_path)
    del manifest["derived_sources"][0]["role"]
    errors, _ = validate(manifest, root=tmp_path)
    assert any("derived_sources[0]缺role" in error for error in errors)


def test_g0_rejects_empty_or_fake_source_content(tmp_path: Path):
    manifest = _manifest(tmp_path)
    for entry in (
        manifest["normative_sources"]
        + manifest["derived_sources"]
        + manifest["knowledge_sources"]
        + [manifest["evidence_dossier"]]
    ):
        path = tmp_path / entry["path"]
        path.write_bytes(b"")
        entry["sha256"] = _sha(path)
    errors, _ = validate(manifest, root=tmp_path)
    assert any("规范PDF内容无效" in error for error in errors)
    assert any("派生源内容不足" in error for error in errors)
    assert any("知识源内容不足" in error for error in errors)
    assert any("证据档案最低有效内容不足" in error for error in errors)


def test_g0_rejects_pdf_signature_shell_that_cannot_be_parsed(tmp_path: Path):
    manifest = _manifest(tmp_path)
    for entry in manifest["normative_sources"]:
        path = tmp_path / entry["path"]
        path.write_bytes(b"%PDF" + b"x" * 12)
        entry["sha256"] = _sha(path)
    manifest["derived_sources"][0]["derived_from_sha256"] = manifest["normative_sources"][0]["sha256"]
    errors, _ = validate(manifest, root=tmp_path)
    assert any("无法解析" in error or "没有可读页面" in error for error in errors)


def test_g0_requires_at_least_one_derived_source(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["derived_sources"] = []
    errors, _ = validate(manifest, root=tmp_path)
    assert any("derived_sources为空" in error for error in errors)


def test_g0_rejects_low_entropy_evidence_dossier(tmp_path: Path):
    manifest = _manifest(tmp_path)
    dossier = tmp_path / manifest["evidence_dossier"]["path"]
    dossier.write_text("# 标题一\n\n## 标题二\n\n" + "甲" * 140, encoding="utf-8")
    manifest["evidence_dossier"]["sha256"] = _sha(dossier)
    errors, _ = validate(manifest, root=tmp_path)
    assert any("低熵" in error for error in errors)


def test_g0_rejects_unknown_classroom_account_field(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["classroom_account"] = {"status": "学生已经掌握"}
    errors, _ = validate(manifest, root=tmp_path)
    assert any("未知字段: classroom_account" in error for error in errors)


def test_g0_bound_entries_reject_nested_release_claims(tmp_path: Path):
    manifest = _manifest(tmp_path)
    manifest["evidence_dossier"]["host_release"] = {"status": "released"}

    errors, _ = validate(manifest, root=tmp_path)

    assert any("evidence_dossier含未知字段: host_release" in error for error in errors)
