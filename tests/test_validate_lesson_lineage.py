from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from test_validate_lesson_schema_lineage import _lesson as build_v2_lesson  # noqa: E402
from validate_lesson_lineage import validate_design_lock, validate_materials_lock  # noqa: E402


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _write_pptx(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr(
            "[Content_Types].xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
</Types>""",
        )
        archive.writestr(
            "_rels/.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "ppt/presentation.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst>
</p:presentation>""",
        )
        archive.writestr(
            "ppt/_rels/presentation.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide1.xml"/>
</Relationships>""",
        )
        archive.writestr(
            "ppt/slides/slide1.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"><p:cSld><p:spTree><p:sp><p:txBody><a:p><a:r><a:t>沿着原文看变化</a:t></a:r></a:p></p:txBody></p:sp></p:spTree></p:cSld></p:sld>""",
        )
    return path


def _chain(tmp_path: Path) -> tuple[dict, dict]:
    lesson = build_v2_lesson(tmp_path)
    g1_path = tmp_path / "work/teaching/lesson/_meta/lesson_plan_lock.json"
    g1 = json.loads(g1_path.read_text(encoding="utf-8"))
    teaching_design = _write(
        tmp_path / "work/teaching/lesson/教学设计.md",
        """# LES-TEST-01 教学设计

## T01 页面功能合同

学生先听见“氓之蚩蚩，抱布贸丝”，独立圈出动作并按顺序复述；这一页只保存首答，不提前给出人物结论。

## 课堂事件链

教师提出动作顺序问题，静默等待六十秒；学生留下个人复述后，同伴只追问原词依据，再用另一颜色完成可见修订。

## 时间、分支与证据

五分钟依次用于首答、同伴追问和个人修订。沉默时回到动词，越界概括时回到原句；最终产物是一条带原词的修订复述，供下一页取回。
""",
    )
    lesson_data = _write(
        tmp_path / "work/teaching/lesson/lesson.json",
        json.dumps(lesson, ensure_ascii=False, indent=2),
    )
    design_approval = {
        "schema_version": "g2-owner-approval.v1",
        "lesson_id": "LES-TEST-01",
        "reviewer_id": "project-owner",
        "author_id": "design-author-agent",
        "decision": "approved",
        "reviewed_at": "2026-08-22T12:00:00+08:00",
        "approval_event_id": "G2-OWNER-TEST-01",
        "approval_source": "conversation:test:explicit-design-approval",
        "verification_mode": "external_review_gate",
        "authentication_boundary": "本地验证器只验证回执结构与血缘，不认证人类身份；真实所有者身份须由宿主对话记录人工核验。",
        "teaching_design_path": str(teaching_design.relative_to(tmp_path)),
        "teaching_design_sha256": _sha(teaching_design),
        "lesson_data_sha256": _sha(lesson_data),
        "lesson_plan_lock_sha256": _sha(g1_path),
        "approval_statement": f"项目所有者明确批准当前教学设计Markdown {_sha(teaching_design)} 与同源课程数据进入G2。",
        "standard_version": "STANDARD-TEST",
        "resolved_issues": [],
    }
    design_approval_path = _write(
        tmp_path / "work/teaching/lesson/_meta/G2_owner_approval.json",
        json.dumps(design_approval, ensure_ascii=False, indent=2),
    )
    design_lock = {
        "schema_version": "design-lock.v1",
        "lesson_id": "LES-TEST-01",
        "author_id": "design-author-agent",
        "lesson_plan_lock": {"path": str(g1_path.relative_to(tmp_path)), "sha256": _sha(g1_path)},
        "lesson_plan_sha256": g1["lesson_plan"]["sha256"],
        "teaching_design": {"path": str(teaching_design.relative_to(tmp_path)), "sha256": _sha(teaching_design)},
        "lesson_data": {"path": str(lesson_data.relative_to(tmp_path)), "sha256": _sha(lesson_data)},
        "owner_approval": {"path": str(design_approval_path.relative_to(tmp_path)), "sha256": _sha(design_approval_path)},
        "validation": {"validator": "validate_lesson_schema.py", "strict": True, "passed": True},
        "status": "validated",
    }
    design_lock_path = _write(
        tmp_path / "work/teaching/lesson/_meta/design_lock.json",
        json.dumps(design_lock, ensure_ascii=False, indent=2),
    )

    artifacts = []
    for role, filename in (
        ("pptx", "课件.pptx"),
        ("screenplay", "逐屏真实剧本.md"),
        ("learning_sheet", "学习单.md"),
        ("board_plan", "板书设计.md"),
    ):
        artifact_path = tmp_path / f"work/teaching/lesson/materials/{filename}"
        text_materials = {
            "screenplay": """# T01 逐屏真实剧本

教师：请先沿动作顺序说清眼前发生了什么，不急着评价人物。

学生独立圈画“抱、贸”等动作并写下一句话。教师保持安静，真实等待六十秒，只巡视不提示答案。

学生可能回应一：只说“他来求婚”。教师追问：哪个动作支持你的判断？请把原词放回句子里。

学生可能回应二：暂时沉默。教师回应：先只圈出你看见的动作，按先后读一遍。

教师邀请两名学生比较复述，学生用另一颜色补入遗漏动作，留下可见修订。

切页：我们把这条修订后的复述带到下一处文字，看看关系是否仍按同样方式发展。
""",
            "learning_sheet": """# 学习单：沿动作进入原文

## T01 我的首答

请阅读“氓之蚩蚩，抱布贸丝”，按发生顺序圈出动作，再用一句话复述。暂时不评价人物，只保存你的第一遍理解。

## 同伴追问后的修订

同伴只问：你的判断依据是哪一个原词？请用另一颜色补入遗漏动作，并写明自己的理解发生了什么变化。
""",
            "board_plan": """# 板书设计

## T01 动作推进

氓之蚩蚩，抱布贸丝

抱布 → 贸丝 → 来意待证

首答：按顺序复述

追问：依据哪个原词

修订：补入遗漏动作，保留疑问进入下一句

版面中心保留动作箭头，左侧记录学生首答，右侧以另一颜色写修订；结尾只圈出仍待下一句验证的“来意”，不提前写人物品质结论。
""",
        }
        artifact = _write_pptx(artifact_path) if role == "pptx" else _write(artifact_path, text_materials[role])
        artifacts.append({"role": role, "path": str(artifact.relative_to(tmp_path)), "sha256": _sha(artifact)})
    manifest = {
        "schema_version": "lesson-materials-manifest.v1",
        "lesson_id": "LES-TEST-01",
        "source_design_lock_sha256": _sha(design_lock_path),
        "artifacts": artifacts,
    }
    manifest_path = _write(
        tmp_path / "work/teaching/lesson/materials/manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2),
    )
    materials_lock = {
        "schema_version": "materials-lock.v1",
        "lesson_id": "LES-TEST-01",
        "author_id": "materials-author-agent",
        "design_lock": {"path": str(design_lock_path.relative_to(tmp_path)), "sha256": _sha(design_lock_path)},
        "manifest": {"path": str(manifest_path.relative_to(tmp_path)), "sha256": _sha(manifest_path)},
        "status": "built",
    }
    return design_lock, materials_lock


def test_valid_design_and_materials_locks_pass(tmp_path: Path):
    design_lock, materials_lock = _chain(tmp_path)
    assert validate_design_lock(design_lock, root=tmp_path) == []
    assert validate_materials_lock(materials_lock, root=tmp_path) == []


def test_design_lock_requires_current_owner_approval(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    del design_lock["owner_approval"]
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("所有者审批" in error or "owner_approval" in error for error in errors)


def test_design_owner_approval_must_bind_current_markdown(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    receipt_path = tmp_path / design_lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["teaching_design_sha256"] = "0" * 64
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    design_lock["owner_approval"]["sha256"] = _sha(receipt_path)
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("审批回执未绑定当前教学设计" in error for error in errors)


def test_design_author_cannot_self_approve_g2(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    receipt_path = tmp_path / design_lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["reviewer_id"] = receipt["author_id"]
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    design_lock["owner_approval"]["sha256"] = _sha(receipt_path)
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("审批者不得与设计作者相同" in error for error in errors)


def test_plan_change_invalidates_design_lock(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    plan = tmp_path / "work/teaching/lesson/教案.md"
    plan.write_text(plan.read_text(encoding="utf-8") + "修改", encoding="utf-8")
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("G1" in error or "lesson_plan" in error for error in errors)


def test_design_change_invalidates_materials_lock(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    lesson_data = tmp_path / "work/teaching/lesson/lesson.json"
    lesson_data.write_text('{"lesson_id":"LES-CHANGED"}', encoding="utf-8")
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("G2" in error or "lesson_data" in error for error in errors)


def test_artifact_hash_drift_is_rejected(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    artifact = tmp_path / "work/teaching/lesson/materials/课件.pptx"
    artifact.write_text("changed", encoding="utf-8")
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("artifact" in error and "哈希" in error for error in errors)


def test_required_material_roles_cannot_be_omitted(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["artifacts"] = [item for item in manifest["artifacts"] if item["role"] != "screenplay"]
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("screenplay" in error for error in errors)


def test_design_lock_cannot_self_report_invalid_lesson_as_passed(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    lesson_data = tmp_path / design_lock["lesson_data"]["path"]
    lesson_data.write_text('{"lesson_id":"LES-TEST-01"}', encoding="utf-8")
    design_lock["lesson_data"]["sha256"] = _sha(lesson_data)
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("课程数据无效" in error for error in errors)


def test_design_chain_cannot_be_relocated_outside_formal_teaching_tree(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    for field, target in (
        ("lesson_plan_lock", "rogue/lesson/_meta/lesson_plan_lock.json"),
        ("teaching_design", "rogue/lesson/教学设计.md"),
        ("lesson_data", "rogue/lesson/lesson.json"),
    ):
        source = tmp_path / design_lock[field]["path"]
        relocated = _write(tmp_path / target, source.read_text(encoding="utf-8"))
        design_lock[field] = {"path": str(relocated.relative_to(tmp_path)), "sha256": _sha(relocated)}
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("必须位于work/teaching正式课程树" in error for error in errors)


def test_empty_teaching_design_is_rejected(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    design_path = tmp_path / design_lock["teaching_design"]["path"]
    design_path.write_text("", encoding="utf-8")
    design_lock["teaching_design"]["sha256"] = _sha(design_path)
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("teaching_design为空" in error for error in errors)


def test_pptx_role_requires_real_ooxml_package(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    pptx_path.write_text("not a pptx package", encoding="utf-8")
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("PPTX不是有效OOXML包" in error for error in errors)


def test_two_named_zip_members_do_not_make_a_real_pptx(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    with zipfile.ZipFile(pptx_path, "w") as archive:
        archive.writestr("[Content_Types].xml", "<Types/>")
        archive.writestr("ppt/presentation.xml", "<p:presentation/>")
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("PPTX不是有效OOXML包" in error for error in errors)


def test_each_referenced_slide_requires_slide_content_type(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    replacement = pptx_path.with_suffix(".replacement")
    with zipfile.ZipFile(pptx_path) as source, zipfile.ZipFile(replacement, "w") as target:
        for member in source.namelist():
            payload = source.read(member)
            if member == "[Content_Types].xml":
                payload = payload.replace(
                    b'<Override PartName="/ppt/slides/slide1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n',
                    b"",
                )
            target.writestr(member, payload)
    replacement.replace(pptx_path)
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("slide部件ContentType" in error for error in errors)


def test_pptx_requires_relationships_default_content_type(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    replacement = pptx_path.with_suffix(".replacement")
    with zipfile.ZipFile(pptx_path) as source, zipfile.ZipFile(replacement, "w") as target:
        for member in source.namelist():
            payload = source.read(member)
            if member == "[Content_Types].xml":
                payload = payload.replace(
                    b'<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n',
                    b"",
                )
            target.writestr(member, payload)
    replacement.replace(pptx_path)
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("rels默认ContentType" in error for error in errors)


def test_external_slide_relationship_is_rejected(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    replacement = pptx_path.with_suffix(".replacement")
    with zipfile.ZipFile(pptx_path) as source, zipfile.ZipFile(replacement, "w") as target:
        for member in source.namelist():
            payload = source.read(member)
            if member == "ppt/_rels/presentation.xml.rels":
                payload = payload.replace(b'Target="slides/slide1.xml"', b'Target="slides/slide1.xml" TargetMode="External"')
            target.writestr(member, payload)
    replacement.replace(pptx_path)
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("slide关系不得使用External TargetMode" in error for error in errors)


def test_external_root_office_document_relationship_is_rejected(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    replacement = pptx_path.with_suffix(".replacement")
    with zipfile.ZipFile(pptx_path) as source, zipfile.ZipFile(replacement, "w") as target:
        for member in source.namelist():
            payload = source.read(member)
            if member == "_rels/.rels":
                payload = payload.replace(b'Target="ppt/presentation.xml"', b'Target="ppt/presentation.xml" TargetMode="External"')
            target.writestr(member, payload)
    replacement.replace(pptx_path)
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("根officeDocument关系不得使用External TargetMode" in error for error in errors)


def test_lineage_bound_paths_must_be_project_relative(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    design_lock["lesson_data"]["path"] = str(
        (tmp_path / design_lock["lesson_data"]["path"]).resolve()
    )
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("lesson_data必须使用项目根相对路径" in error for error in errors)


def test_design_files_must_stay_with_same_lesson(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    original = tmp_path / design_lock["lesson_data"]["path"]
    other = _write(tmp_path / "work/teaching/other/lesson.json", original.read_text(encoding="utf-8"))
    design_lock["lesson_data"] = {"path": str(other.relative_to(tmp_path)), "sha256": _sha(other)}
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("lesson_data必须位于同一课目录" in error for error in errors)


def test_materials_manifest_must_stay_with_same_lesson(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    original = tmp_path / materials_lock["manifest"]["path"]
    other = _write(
        tmp_path / "work/teaching/other/materials/manifest.json",
        original.read_text(encoding="utf-8"),
    )
    materials_lock["manifest"] = {
        "path": str(other.relative_to(tmp_path)),
        "sha256": _sha(other),
    }
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("manifest必须位于同一课目录" in error for error in errors)


def test_material_artifacts_must_stay_with_same_lesson(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    screenplay = next(item for item in manifest["artifacts"] if item["role"] == "screenplay")
    original = tmp_path / screenplay["path"]
    other = _write(
        tmp_path / "work/teaching/other/materials/逐屏真实剧本.md",
        original.read_text(encoding="utf-8"),
    )
    screenplay.update(path=str(other.relative_to(tmp_path)), sha256=_sha(other))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("artifact" in error and "必须位于同一课目录" in error for error in errors)


def test_material_roles_require_distinct_nonempty_files(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    empty = _write(tmp_path / "work/teaching/lesson/materials/empty.bin", "")
    for artifact in manifest["artifacts"]:
        if artifact["role"] != "pptx":
            artifact.update(path=str(empty.relative_to(tmp_path)), sha256=_sha(empty))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("多个物料角色不得共用同一文件" in error for error in errors)
    assert any("物料文件为空" in error for error in errors)


def test_text_material_roles_require_markdown_with_minimum_content(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for artifact in manifest["artifacts"]:
        if artifact["role"] == "screenplay":
            tiny = _write(tmp_path / "work/teaching/lesson/materials/tiny.md", "x")
            artifact.update(path=str(tiny.relative_to(tmp_path)), sha256=_sha(tiny))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("文本物料内容不足" in error for error in errors)


def test_human_readable_design_rejects_single_character_placeholder(tmp_path: Path):
    design_lock, _ = _chain(tmp_path)
    design_path = tmp_path / design_lock["teaching_design"]["path"]
    design_path.write_text("x", encoding="utf-8")
    design_lock["teaching_design"]["sha256"] = _sha(design_path)
    errors = validate_design_lock(design_lock, root=tmp_path)
    assert any("teaching_design最低有效内容不足" in error for error in errors)


def test_all_text_material_roles_reject_ten_character_garbage(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for index, artifact in enumerate(manifest["artifacts"]):
        if artifact["role"] != "pptx":
            garbage = _write(
                tmp_path / f"work/teaching/lesson/materials/garbage-{index}.md",
                "abcdefghij",
            )
            artifact.update(path=str(garbage.relative_to(tmp_path)), sha256=_sha(garbage))
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert sum("最低有效内容不足" in error for error in errors) >= 3


def test_pptx_requires_at_least_one_visible_slide_object(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    replacement = pptx_path.with_suffix(".replacement")
    with zipfile.ZipFile(pptx_path) as source, zipfile.ZipFile(replacement, "w") as target:
        for member in source.namelist():
            payload = source.read(member)
            if member == "ppt/slides/slide1.xml":
                payload = b'<?xml version="1.0" encoding="UTF-8"?><p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree/></p:cSld></p:sld>'
            target.writestr(member, payload)
    replacement.replace(pptx_path)
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("没有可见文本或图片" in error for error in errors)


def test_slide_level_external_relationship_is_rejected(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    replacement = pptx_path.with_suffix(".replacement")
    with zipfile.ZipFile(pptx_path) as source, zipfile.ZipFile(replacement, "w") as target:
        for member in source.namelist():
            target.writestr(member, source.read(member))
        target.writestr(
            "ppt/slides/_rels/slide1.xml.rels",
            """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId9" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="https://example.invalid/image.png" TargetMode="External"/>
</Relationships>""",
        )
    replacement.replace(pptx_path)
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("slide部件关系不得使用External TargetMode" in error for error in errors)


def test_empty_picture_element_does_not_count_as_visible_content(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    replacement = pptx_path.with_suffix(".replacement")
    with zipfile.ZipFile(pptx_path) as source, zipfile.ZipFile(replacement, "w") as target:
        for member in source.namelist():
            payload = source.read(member)
            if member == "ppt/slides/slide1.xml":
                payload = b'<?xml version="1.0" encoding="UTF-8"?><p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:cSld><p:spTree><p:pic/></p:spTree></p:cSld></p:sld>'
            target.writestr(member, payload)
    replacement.replace(pptx_path)
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("没有可见文本或图片" in error for error in errors)


def test_material_roles_cannot_share_identical_bytes(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    source = tmp_path / next(item for item in manifest["artifacts"] if item["role"] == "screenplay")["path"]
    for artifact in manifest["artifacts"]:
        if artifact["role"] in {"learning_sheet", "board_plan"}:
            target = tmp_path / artifact["path"]
            target.write_bytes(source.read_bytes())
            artifact["sha256"] = _sha(target)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("多个物料角色不得使用相同内容哈希" in error for error in errors)


def test_design_and_materials_locks_require_stage_authors(tmp_path: Path):
    design_lock, materials_lock = _chain(tmp_path)
    del design_lock["author_id"]
    del materials_lock["author_id"]
    assert any("author_id为空" in error for error in validate_design_lock(design_lock, root=tmp_path))
    assert any("author_id为空" in error for error in validate_materials_lock(materials_lock, root=tmp_path))


def test_design_and_materials_stage_authors_must_be_strings(tmp_path: Path):
    design_lock, materials_lock = _chain(tmp_path)
    design_lock["author_id"] = {"claimed": "designer"}
    materials_lock["author_id"] = ["materials-author"]
    assert any("author_id必须为非空字符串" in error for error in validate_design_lock(design_lock, root=tmp_path))
    assert any("author_id必须为非空字符串" in error for error in validate_materials_lock(materials_lock, root=tmp_path))


def test_image_relationship_cannot_point_to_non_media_xml_part(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    manifest_path = tmp_path / materials_lock["manifest"]["path"]
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    pptx = next(item for item in manifest["artifacts"] if item["role"] == "pptx")
    pptx_path = tmp_path / pptx["path"]
    replacement = pptx_path.with_suffix(".replacement")
    with zipfile.ZipFile(pptx_path) as source, zipfile.ZipFile(replacement, "w") as target:
        for member in source.namelist():
            payload = source.read(member)
            if member == "ppt/slides/slide1.xml":
                payload = b'''<?xml version="1.0" encoding="UTF-8"?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:cSld><p:spTree><p:pic><p:blipFill><a:blip r:embed="rImg"/></p:blipFill></p:pic></p:spTree></p:cSld></p:sld>'''
            target.writestr(member, payload)
        target.writestr(
            "ppt/slides/_rels/slide1.xml.rels",
            '''<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rImg" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../presentation.xml"/></Relationships>''',
        )
    replacement.replace(pptx_path)
    pptx["sha256"] = _sha(pptx_path)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
    materials_lock["manifest"]["sha256"] = _sha(manifest_path)

    errors = validate_materials_lock(materials_lock, root=tmp_path)

    assert any("图片关系目标必须位于ppt/media" in error for error in errors)


def test_unregistered_file_in_materials_directory_is_rejected(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    _write_pptx(tmp_path / "work/teaching/lesson/materials/未审课件.pptx")
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("materials目录含未登记文件" in error for error in errors)


def test_g3_lock_rejects_unknown_classroom_account_field(tmp_path: Path):
    _, materials_lock = _chain(tmp_path)
    materials_lock["classroom_account"] = {"status": "学生已经掌握"}
    errors = validate_materials_lock(materials_lock, root=tmp_path)
    assert any("materials_lock含未知字段: classroom_account" in error for error in errors)
