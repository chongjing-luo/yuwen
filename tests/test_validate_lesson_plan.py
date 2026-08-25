from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_validate_lesson_evidence import _manifest as build_evidence_manifest  # noqa: E402
from validate_lesson_plan import canonical_json_sha256, validate, validate_candidate  # noqa: E402


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _write(path: Path, content: bytes | str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, bytes):
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    return path


def _contract() -> dict:
    components = {}
    for component_id in (
        "entry",
        "context",
        "text_development",
        "knowledge_formation",
        "student_experience",
        "discussion",
        "synthesis_retrieval",
        "assessment_evidence",
        "transfer",
        "exam_link",
        "contemporary_link",
    ):
        if component_id in {"exam_link", "contemporary_link"}:
            components[component_id] = {
                "status": "not_applicable",
                "reason": "未找到可靠且不可替代的材料，不进入课堂前台。",
                "stage_refs": [],
            }
        else:
            components[component_id] = {
                "status": "included",
                "reason": "承担本课完整理解链中的必要功能。",
                "stage_refs": ["P0"],
            }
    return {
        "mechanism_nodes": ["K1", "K2", "U8", "J4"],
        "total_minutes": 5,
        "closing_mode": "回到全文完成个人末答，并安排一周后闭卷回取。",
        "objective_framework": {
            "language_use": {
                "status": "included",
                "reason": "以原文复述、证据表达和修订构成本课语言实践基座。",
                "objective_refs": ["O1"],
            },
            "thinking": {
                "status": "included",
                "reason": "辨认叙事推进并依据证据修订判断。",
                "objective_refs": ["O1"],
            },
            "aesthetic": {
                "status": "not_primary",
                "reason": "本夹具不模拟文学审美目标，审计后不单列。",
                "objective_refs": [],
            },
            "culture": {
                "status": "not_primary",
                "reason": "本夹具的文化事实进入知识全账，审计后不单列能力目标。",
                "objective_refs": [],
            },
            "moral_education": {
                "status": "included",
                "reason": "依据人物处境形成尊重证据与责任边界的判断。",
                "objective_refs": ["O1"],
            },
            "reality_transfer": {
                "status": "included",
                "reason": "把证据判断迁移到课堂之外的真实表达。",
                "objective_refs": ["O1"],
            },
        },
        "objectives": [
            {
                "id": "O1",
                "kind": "reality_transfer",
                "dimensions": ["language_use", "thinking", "moral_education", "reality_transfer"],
                "statement": "学生能够依据原文关键语句说明人物经历怎样逐步展开，形成尊重事实与责任边界的判断，并把有证据的表达迁移到真实生活。",
                "kid_refs": ["K01"],
                "mechanism_nodes": ["K1", "U8"],
                "minimum_evidence": "个人末答引用至少一处原文，并说明一次现实判断。",
                "high_quality_evidence": "能解释前后变化、修订首答，并区分文本事实与现实迁移。",
                "failure_signal": "只写结论标签或价值口号而没有原文依据。",
                "recurrence": "一周后闭卷回取。",
            }
        ],
        "knowledge_items": [
            {
                "kid": "K01",
                "statement": "关键语句在全文叙事推进中承担转折作用。",
                "status": "must_teach",
                "source_ref": "SRC-CARD#KP-CARD-TEST-01-001",
                "kp_ids": ["KP-CARD-TEST-01-001"],
                "stage_refs": ["P0"],
                "mastery_evidence": "指出原句并说明前后变化。",
                "mechanism_nodes": ["K1", "K2"],
            },
            {
                "kid": "K02",
                "statement": "超出本课负荷的完整体裁史。",
                "status": "defer",
                "source_ref": "SRC-REFERENCE#p2",
                "stage_refs": [],
                "mastery_evidence": "",
                "defer_reason": "留到专题复习，避免本课过载。",
                "mechanism_nodes": ["K5"],
            },
        ],
        "knowledge_clusters": [
            {
                "id": "KC1",
                "name": "沿人物经历看见叙事转折",
                "organizing_basis": "依照本篇人物经历和叙事推进聚合课堂知识。",
                "rationale": "K01只有放回前后动作关系，学生才能从人物标签走向有证据的解释。",
                "kid_refs": ["K01"],
            },
            {
                "id": "KC2",
                "name": "本课不展开的体裁史边界",
                "organizing_basis": "按本课负荷和后续专题关系收纳defer知识。",
                "rationale": "完整体裁史不帮助当前文本理解，单列边界以免混入课堂主线。",
                "kid_refs": ["K02"],
            },
        ],
        "work_interpretation": {
            "central_meaning": {
                "status": "included",
                "kid_refs": ["K01"],
                "evidence_boundary": "依据全文动作次序作文本分析，不推断作者未明说的心理事实。",
                "not_applicable_reason": "",
            },
            "expressive_intent": {
                "status": "included",
                "kid_refs": ["K01"],
                "evidence_boundary": "表述为作品的表达指向，不冒充可直接证明的作者心理动机。",
                "not_applicable_reason": "",
            },
            "emotional_organization": {
                "status": "included",
                "kid_refs": ["K01"],
                "evidence_boundary": "只依据文本次序和语调变化作合理解释。",
                "not_applicable_reason": "",
            },
        },
        "questions": [
            {
                "id": "Q1",
                "text": "这段经历为什么会一步步走到这里？",
                "rationale": "该问题需要从初读判断、逐处存证到全文校准，能够共同牵引目标O1和知识K01。",
                "objective_refs": ["O1"],
                "kid_refs": ["K01"],
                "stage_refs": ["P0"],
                "recovery_stage_refs": ["P0"],
                "mechanism_nodes": ["J4"],
            }
        ],
        "overall_teaching_logic": {
            "text": "课堂从学生对人物处境的第一感受进入，在必要背景帮助下回到原文，沿叙事推进逐处形成知识；学生先留下判断，再在讨论、教师校准和同伴证据中修订，最后重新通读全文、闭卷回取知识并说明理解如何变化。高考和新闻经检索后没有不可替代价值，因此不进入前台。",
            "stage_refs": ["P0"],
            "mechanism_nodes": ["K1", "K2", "U8", "J4"],
            "components": components,
        },
        "stages": [
            {
                "id": "P0",
                "name": "沿着原文看见变化",
                "entry_reason": "学生只有人物标签，须先回到原文动作次序建立共同证据。",
                "text_scope": "全文关键动作句及其前后关系。",
                "objective_refs": ["O1"],
                "kid_refs": ["K01"],
                "initial_method": "首读生成、逐句细读、同伴比较、教师后置校准和个人修订。",
                "student_change": "从标签判断走向有原文根据的解释。",
                "student_experience": "先保留自己的判断，再在原词和同伴追问中看见理解发生变化。",
                "teacher_role": "在学生生成后补充必要背景并校准证据边界。",
                "evidence": "首答、讨论记录与个人末答形成可见修订链。",
                "transition_reason": "完成全文证据积累后才能重新整体化。",
            }
        ],
        "claim_boundary": "课堂证据状态：未采集；学生掌握、理解与享受均待真实试教验证。",
    }


def _lock(tmp_path: Path) -> dict:
    plan = _write(
        tmp_path / "work/teaching/lesson/教案.md",
        """# 《测试课文》教案

## 一、证据基础与课程位置

本课以教材原文和课程标准为规范依据，解析文本只用于定位。学生已有借助注释理解句意的经验，但容易跳过动作次序直接套用人物标签，因此需要把叙事推进、语言证据和理解修订连在一起。

## 二、教学目标与知识清单

目标是使学生能够依据关键语句说明人物经历怎样逐步展开，并完成一次有证据的修订。必教知识K01指向知识卡中的叙事转折知识点；完整体裁史作为K02延后，不进入本课前台以避免负荷失衡。

## 三、整体教学逻辑

课堂从学生对人物处境的第一感受进入，在必要背景帮助下回到原文，沿叙事推进逐处形成知识。学生先留下个人判断，再在同伴追问与教师后置校准中修订；全文证据积累完成后重新通读，并用个人末答回收贯穿问题。

## 四、阶段落实

第一阶段沿原文动作建立首答，学生圈出动作并按顺序复述。第二步比较不同复述中的证据，教师只追问原词位置。第三步让学生用另一颜色补入遗漏动作，形成可见修订，并把产物带到全文收束。

## 五、评价、负荷与边界

最低证据是个人末答至少引用一处原文；高质量证据能够解释前后变化并说明修订理由。若学生只写人物标签而无原文依据，则回到动作次序。完整母版五分钟，最终回到全文完成个人末答；课堂证据尚未采集，不声称学生已经学会或享受。
""",
    )
    evidence_manifest = build_evidence_manifest(tmp_path)
    evidence = _write(
        tmp_path / "work/teaching/lesson/_meta/evidence_manifest.json",
        json.dumps(evidence_manifest, ensure_ascii=False, indent=2),
    )
    contract = _contract()
    candidate = {
        "schema_version": "lesson-plan-candidate.v1",
        "lesson_id": "LES-TEST-01",
        "author_id": "lesson-author-agent",
        "lesson_plan": {"path": str(plan.relative_to(tmp_path)), "sha256": _sha(plan)},
        "evidence_manifest": {"path": str(evidence.relative_to(tmp_path)), "sha256": _sha(evidence)},
        "contract": contract,
        "status": "candidate_owner_review",
    }
    _write(
        tmp_path / "work/teaching/lesson/_meta/lesson_plan_candidate.json",
        json.dumps(candidate, ensure_ascii=False, indent=2),
    )
    receipt = {
        "schema_version": "g1-owner-approval.v1",
        "lesson_id": "LES-TEST-01",
        "reviewer_id": "project-owner",
        "author_id": "lesson-author-agent",
        "decision": "approved",
        "reviewed_at": "2026-08-20T15:00:00+08:00",
        "approval_event_id": "USER-MSG-20260820-150000",
        "approval_source": "conversation:user",
        "verification_mode": "external_review_gate",
        "authentication_boundary": "本地验证器只验证回执结构与血缘，不认证人类身份；真实所有者须由宿主对话记录人工核验。",
        "lesson_plan_path": str(plan.relative_to(tmp_path)),
        "lesson_plan_sha256": _sha(plan),
        "approval_statement": f"批准当前教案SHA-256 {_sha(plan)} 进入G1。",
        "lesson_plan_contract_sha256": canonical_json_sha256(contract),
        "evidence_manifest_sha256": _sha(evidence),
        "standard_version": "procedure-0.2",
        "resolved_issues": [],
    }
    receipt_path = _write(
        tmp_path / "work/teaching/lesson/_meta/G1_owner_approval.json",
        json.dumps(receipt, ensure_ascii=False, indent=2),
    )
    return {
        "schema_version": "lesson-plan-lock.v1",
        "lesson_id": "LES-TEST-01",
        "author_id": "lesson-author-agent",
        "lesson_plan": {"path": str(plan.relative_to(tmp_path)), "sha256": _sha(plan)},
        "evidence_manifest": {"path": str(evidence.relative_to(tmp_path)), "sha256": _sha(evidence)},
        "owner_approval": {"path": str(receipt_path.relative_to(tmp_path)), "sha256": _sha(receipt_path)},
        "contract": contract,
        "status": "approved",
    }


def _candidate(tmp_path: Path) -> dict:
    lock = _lock(tmp_path)
    receipt_path = tmp_path / lock["owner_approval"]["path"]
    receipt_path.unlink()
    return {
        "schema_version": "lesson-plan-candidate.v1",
        "lesson_id": lock["lesson_id"],
        "author_id": lock["author_id"],
        "lesson_plan": lock["lesson_plan"],
        "evidence_manifest": lock["evidence_manifest"],
        "contract": lock["contract"],
        "status": "candidate_owner_review",
    }


def test_valid_lesson_plan_lock_passes(tmp_path: Path):
    errors, stats = validate(_lock(tmp_path), root=tmp_path)
    assert errors == []
    assert stats["objectives"] == 1
    assert stats["knowledge_items"] == 2
    assert stats["stages"] == 1


def test_valid_candidate_contract_prechecks_without_owner_receipt(tmp_path: Path):
    errors, stats = validate_candidate(_candidate(tmp_path), root=tmp_path)

    assert errors == []
    assert stats == {"objectives": 1, "knowledge_items": 2, "stages": 1}


def test_g1_requires_text_specific_knowledge_clusters(tmp_path: Path):
    candidate = _candidate(tmp_path)
    del candidate["contract"]["knowledge_clusters"]

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("知识簇" in error for error in errors)


def test_every_knowledge_item_has_exactly_one_primary_cluster(tmp_path: Path):
    candidate = _candidate(tmp_path)
    clusters = candidate["contract"]["knowledge_clusters"]
    clusters[0]["kid_refs"] = ["K01", "K02"]

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("KID重复归入多个知识簇: K02" in error for error in errors)


def test_knowledge_cluster_coverage_cannot_omit_deferred_items(tmp_path: Path):
    candidate = _candidate(tmp_path)
    candidate["contract"]["knowledge_clusters"].pop()

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("KID未归入知识簇: K02" in error for error in errors)


def test_g1_requires_a_complete_work_interpretation_audit(tmp_path: Path):
    candidate = _candidate(tmp_path)
    del candidate["contract"]["work_interpretation"]

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("作品整体解释" in error for error in errors)


def test_each_included_work_interpretation_must_bind_a_teachable_kid_and_boundary(
    tmp_path: Path,
):
    candidate = _candidate(tmp_path)
    central_meaning = candidate["contract"]["work_interpretation"]["central_meaning"]
    central_meaning["kid_refs"] = ["K02"]
    central_meaning["evidence_boundary"] = ""

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("作品主旨或核心观点”已纳入但缺证据边界" in error for error in errors)
    assert any("作品主旨或核心观点”引用非课堂范围KID K02" in error for error in errors)


def test_work_interpretation_cannot_redefine_the_kid_statement(tmp_path: Path):
    candidate = _candidate(tmp_path)
    central_meaning = candidate["contract"]["work_interpretation"]["central_meaning"]
    central_meaning["statement"] = "另写一份可能与KID漂移的作品主旨。"

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any(
        "work_interpretation.central_meaning含未知字段: statement" in error
        for error in errors
    )


def test_not_applicable_work_interpretation_requires_a_reason_and_no_kid(
    tmp_path: Path,
):
    candidate = _candidate(tmp_path)
    emotion = candidate["contract"]["work_interpretation"]["emotional_organization"]
    emotion.update(
        {
            "status": "not_applicable",
            "not_applicable_reason": "",
            "kid_refs": ["K01"],
        }
    )

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("情感基调、情感变化或态度语调组织”判为不适用但没有文体理由" in error for error in errors)
    assert any("情感基调、情感变化或态度语调组织”判为不适用却仍引用KID" in error for error in errors)


def test_g1_requires_a_complete_six_direction_objective_audit(tmp_path: Path):
    candidate = _candidate(tmp_path)
    del candidate["contract"]["objective_framework"]["culture"]

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("目标六向审计" in error for error in errors)


def test_g1_requires_language_moral_and_reality_objective_directions(tmp_path: Path):
    candidate = _candidate(tmp_path)
    candidate["contract"]["objective_framework"] = {
        "language_use": {
            "status": "not_primary",
            "reason": "错误样例：没有设置语言实践目标。",
            "objective_refs": [],
        },
        "thinking": {
            "status": "not_primary",
            "reason": "本课不单列思维目标。",
            "objective_refs": [],
        },
        "aesthetic": {
            "status": "not_primary",
            "reason": "本课不单列审美目标。",
            "objective_refs": [],
        },
        "culture": {
            "status": "not_primary",
            "reason": "文化事实进入知识全账。",
            "objective_refs": [],
        },
        "moral_education": {
            "status": "not_primary",
            "reason": "错误样例：没有设置育人价值目标。",
            "objective_refs": [],
        },
        "reality_transfer": {
            "status": "not_primary",
            "reason": "错误样例：没有设置现实迁移目标。",
            "objective_refs": [],
        },
    }

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("语言建构与运用必须纳入目标" in error for error in errors)
    assert any("立德树人与价值形成必须纳入目标" in error for error in errors)
    assert any("现实迁移与实践必须纳入目标" in error for error in errors)


def test_objective_dimensions_and_framework_refs_must_be_bidirectionally_aligned(tmp_path: Path):
    candidate = _candidate(tmp_path)
    candidate["contract"]["objectives"][0]["dimensions"].remove("moral_education")
    candidate["contract"]["objectives"][0]["dimensions"].append("culture")

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any(
        "立德树人与价值形成引用目标O1，但该目标未标此维度" in error
        for error in errors
    )
    assert any(
        "目标O1标注文化传承与理解，但六向审计未引用该目标" in error
        for error in errors
    )


def test_every_objective_must_declare_at_least_one_framework_dimension(tmp_path: Path):
    candidate = _candidate(tmp_path)
    candidate["contract"]["objectives"][0]["dimensions"] = []

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("目标O1必须标注至少一个六向目标维度" in error for error in errors)


def test_candidate_cannot_claim_approved_or_released(tmp_path: Path):
    candidate = _candidate(tmp_path)
    candidate["status"] = "released"

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("candidate_owner_review" in error for error in errors)


def test_candidate_file_must_live_in_the_same_lesson_meta_directory(tmp_path: Path):
    candidate = _candidate(tmp_path)
    rogue_path = _write(
        tmp_path / "rogue/lesson_plan_candidate.json",
        json.dumps(candidate, ensure_ascii=False),
    )

    errors, _ = validate_candidate(candidate, root=tmp_path, candidate_path=rogue_path)

    assert any("lesson_plan_candidate必须位于同一课目录的_meta" in error for error in errors)


def test_formal_g1_still_requires_a_real_owner_receipt(tmp_path: Path):
    lock = _lock(tmp_path)
    (tmp_path / lock["owner_approval"]["path"]).unlink()

    errors, _ = validate(lock, root=tmp_path)

    assert any("owner_approval文件不存在" in error for error in errors)


def test_formal_g1_requires_the_prechecked_candidate_file(tmp_path: Path):
    lock = _lock(tmp_path)
    (tmp_path / "work/teaching/lesson/_meta/lesson_plan_candidate.json").unlink()

    errors, _ = validate(lock, root=tmp_path)

    assert any("缺少同课lesson_plan_candidate" in error for error in errors)


def test_formal_lock_file_must_live_in_the_same_lesson_meta_directory(tmp_path: Path):
    lock = _lock(tmp_path)
    rogue_path = _write(
        tmp_path / "rogue/lesson_plan_lock.json",
        json.dumps(lock, ensure_ascii=False),
    )

    errors, _ = validate(lock, root=tmp_path, lock_path=rogue_path)

    assert any("lesson_plan_lock必须位于同一课目录的_meta" in error for error in errors)


def test_contract_change_invalidates_older_owner_receipt(tmp_path: Path):
    lock = _lock(tmp_path)
    lock["contract"]["closing_mode"] = "改为另一种尚未获批的收束方式。"

    errors, _ = validate(lock, root=tmp_path)

    assert any("教案机器合同哈希" in error for error in errors)


def test_owner_receipt_must_bind_current_plan_hash(tmp_path: Path):
    lock = _lock(tmp_path)
    receipt_path = tmp_path / lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["lesson_plan_sha256"] = "0" * 64
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    lock["owner_approval"]["sha256"] = _sha(receipt_path)
    errors, _ = validate(lock, root=tmp_path)
    assert any("审核的教案哈希" in error for error in errors)


def test_owner_receipt_rejects_unknown_release_claim_fields(tmp_path: Path):
    lock = _lock(tmp_path)
    receipt_path = tmp_path / lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["status"] = "released"
    receipt["host_release"] = {"confirmed": True}
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    lock["owner_approval"]["sha256"] = _sha(receipt_path)

    errors, _ = validate(lock, root=tmp_path)

    assert any("owner_approval含未知字段: status" in error for error in errors)
    assert any("owner_approval含未知字段: host_release" in error for error in errors)


def test_uncovered_objective_is_rejected(tmp_path: Path):
    lock = _lock(tmp_path)
    extra = dict(lock["contract"]["objectives"][0])
    extra["id"] = "O3"
    lock["contract"]["objectives"].append(extra)
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("目标未进入任何阶段" in error and "O3" in error for error in errors)


def test_must_teach_kid_without_stage_is_rejected(tmp_path: Path):
    lock = _lock(tmp_path)
    lock["contract"]["knowledge_items"][0]["stage_refs"] = []
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("必教/旧知KID没有阶段落点" in error for error in errors)


def test_knowledge_item_stage_refs_must_match_inverse_stage_responsibility(tmp_path: Path):
    candidate = _candidate(tmp_path)
    contract = candidate["contract"]
    contract["stages"].append(
        {
            "id": "P1",
            "name": "全文回看与收纳",
            "entry_reason": "局部证据已形成，需要回到全文检查理解。",
            "text_scope": "全文及首尾关系。",
            "objective_refs": ["O1"],
            "kid_refs": ["K01"],
            "initial_method": "学生重新通读并修订首答，教师只追问证据。",
            "student_change": "从局部判断走向全文解释。",
            "student_experience": "看见自己的首答被全文证据修订。",
            "teacher_role": "组织回看并校准证据边界。",
            "evidence": "引用全文证据的个人修订稿。",
            "transition_reason": "全文理解完成后进入收束。",
        }
    )
    contract["overall_teaching_logic"]["stage_refs"].append("P1")
    # K01在阶段P1实际承担责任，但knowledge_items仍只声明P0。
    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("KID K01的stage_refs与阶段责任不一致" in error for error in errors)


def test_stage_requires_realization_fields_instead_of_a_duplicate_implementation_map(tmp_path: Path):
    candidate = _candidate(tmp_path)
    del candidate["contract"]["stages"][0]["initial_method"]

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("阶段P0缺initial_method" in error for error in errors)


def test_duplicate_implementation_map_is_not_part_of_the_contract(tmp_path: Path):
    candidate = _candidate(tmp_path)
    candidate["contract"]["implementation_map"] = [
        {
            "objective_refs": ["O1"],
            "kid_refs": ["K01"],
            "stage_refs": ["P0"],
            "initial_method": "重复抄写阶段中的教法。",
            "evidence": "重复抄写阶段中的证据。",
        }
    ]

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("contract含未知字段: implementation_map" in error for error in errors)


def test_objective_kid_relationship_requires_a_shared_stage_and_map_row(tmp_path: Path):
    lock = _lock(tmp_path)
    contract = lock["contract"]

    second_objective = dict(contract["objectives"][0])
    second_objective.update({"id": "O3", "kid_refs": ["K03"]})
    contract["objectives"].append(second_objective)

    second_kid = dict(contract["knowledge_items"][0])
    second_kid.update({"kid": "K03", "stage_refs": ["P0"]})
    contract["knowledge_items"].append(second_kid)
    contract["knowledge_items"][0]["stage_refs"] = ["P1"]

    contract["stages"][0]["objective_refs"] = ["O1"]
    contract["stages"][0]["kid_refs"] = ["K03"]
    contract["stages"].append(
        {
            "id": "P1",
            "name": "回到全文完成校准",
            "entry_reason": "局部证据已经形成，需要把分散发现重新组织为全文解释。",
            "text_scope": "全文及首尾照应处。",
            "objective_refs": ["O3"],
            "kid_refs": ["K01"],
            "initial_method": "比较首答与末答中的证据变化并重新通读全文。",
            "student_change": "从局部发现走向全文解释。",
            "student_experience": "在重新通读中听见局部发现汇成完整意义。",
            "teacher_role": "追问证据并帮助学生校准边界。",
            "evidence": "形成引用全文证据的个人修订稿。",
            "transition_reason": "完成校准后才能进入最终收束。",
        }
    )
    contract["overall_teaching_logic"]["stage_refs"] = ["P0", "P1"]

    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)

    assert any("目标O1与KID K01没有共同阶段责任" in error for error in errors)


def test_objective_cannot_bind_deferred_or_teacher_reserve_knowledge(tmp_path: Path):
    candidate = _candidate(tmp_path)
    contract = candidate["contract"]
    contract["objectives"][0]["kid_refs"] = ["K02"]
    contract["knowledge_items"][1]["stage_refs"] = ["P0"]
    contract["stages"][0]["kid_refs"] = ["K02"]

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("目标O1绑定非课堂范围KID K02" in error for error in errors)


def test_deferred_or_teacher_reserve_knowledge_cannot_enter_classroom_stages(tmp_path: Path):
    candidate = _candidate(tmp_path)
    contract = candidate["contract"]
    contract["knowledge_items"][1]["stage_refs"] = ["P0"]
    contract["stages"][0]["kid_refs"].append("K02")

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("KID K02为defer却进入课堂阶段" in error for error in errors)
    assert any("阶段P0引用非课堂范围KID: K02" in error for error in errors)


def test_defer_requires_reason(tmp_path: Path):
    lock = _lock(tmp_path)
    lock["contract"]["knowledge_items"][1]["defer_reason"] = ""
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("defer缺理由" in error for error in errors)


def test_overall_logic_requires_full_course_component_decisions(tmp_path: Path):
    lock = _lock(tmp_path)
    del lock["contract"]["overall_teaching_logic"]["components"]["context"]
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("整体教学逻辑缺少组成裁决" in error and "context" in error for error in errors)


def test_author_cannot_approve_own_plan(tmp_path: Path):
    lock = _lock(tmp_path)
    receipt_path = tmp_path / lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["reviewer_id"] = receipt["author_id"]
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    lock["owner_approval"]["sha256"] = _sha(receipt_path)
    errors, _ = validate(lock, root=tmp_path)
    assert any("审核者不能与作者相同" in error for error in errors)


def test_author_cannot_self_approve_by_padding_the_reviewer_id(tmp_path: Path):
    lock = _lock(tmp_path)
    receipt_path = tmp_path / lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["reviewer_id"] = receipt["author_id"] + " "
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    lock["owner_approval"]["sha256"] = _sha(receipt_path)

    errors, _ = validate(lock, root=tmp_path)

    assert any("审核者不能与作者相同" in error for error in errors)


def test_kp_ids_must_belong_to_the_same_g0_source_as_source_ref(tmp_path: Path):
    lock = _lock(tmp_path)
    evidence_path = tmp_path / lock["evidence_manifest"]["path"]
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    other_card = _write(
        tmp_path / "work/knowledge/other-card.md",
        "# 另一知识源\n\nKP-CARD-TEST-02-001：另一条知识。",
    )
    evidence["knowledge_sources"].append(
        {
            "source_id": "SRC-OTHER",
            "path": str(other_card.relative_to(tmp_path)),
            "sha256": _sha(other_card),
        }
    )
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False, indent=2), encoding="utf-8")
    lock["evidence_manifest"]["sha256"] = _sha(evidence_path)
    lock["contract"]["knowledge_items"][0]["source_ref"] = "SRC-OTHER#KP-CARD-TEST-01-001"

    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)

    assert any("不属于source_ref指定知识源" in error for error in errors)


def test_g1_rejects_low_entropy_plan_body(tmp_path: Path):
    lock = _lock(tmp_path)
    plan_path = tmp_path / lock["lesson_plan"]["path"]
    plan_path.write_text(
        "# 标题一\n\n## 标题二\n\n### 标题三\n\n#### 标题四\n\n" + "甲" * 340,
        encoding="utf-8",
    )
    lock["lesson_plan"]["sha256"] = _sha(plan_path)
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("lesson_plan低熵" in error for error in errors)


def test_long_structured_chinese_plan_is_not_rejected_only_for_a_low_unique_character_ratio(
    tmp_path: Path,
):
    candidate = _candidate(tmp_path)
    plan_path = tmp_path / candidate["lesson_plan"]["path"]
    real_long_plan = (
        Path(__file__).resolve().parents[1]
        / "work/teaching/必修上册/沁园春长沙/教案.md"
    )
    plan_path.write_text(real_long_plan.read_text(encoding="utf-8"), encoding="utf-8")
    candidate["lesson_plan"]["sha256"] = _sha(plan_path)

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert not any("lesson_plan低熵" in error for error in errors)


def test_g1_rejects_unknown_classroom_account_field(tmp_path: Path):
    lock = _lock(tmp_path)
    lock["classroom_account"] = {"status": "学生已经掌握"}
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("lesson_plan_lock含未知字段: classroom_account" in error for error in errors)


def test_owner_trace_fields_and_timezone_are_required(tmp_path: Path):
    lock = _lock(tmp_path)
    receipt_path = tmp_path / lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["reviewer_id"] = ""
    receipt["reviewed_at"] = "2026-08-20 15:00:00"
    receipt["approval_event_id"] = ""
    receipt["approval_source"] = ""
    receipt["verification_mode"] = ""
    receipt["authentication_boundary"] = ""
    receipt["approval_statement"] = "批准"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    lock["owner_approval"]["sha256"] = _sha(receipt_path)
    errors, _ = validate(lock, root=tmp_path)
    assert any("reviewer_id为空" in error for error in errors)
    assert any("reviewed_at必须是带时区" in error for error in errors)
    assert any("approval_event_id为空" in error for error in errors)
    assert any("approval_source为空" in error for error in errors)
    assert any("verification_mode" in error for error in errors)
    assert any("authentication_boundary" in error for error in errors)
    assert any("approval_statement未包含当前教案哈希" in error for error in errors)


def test_g1_recursively_rejects_invalid_g0_manifest(tmp_path: Path):
    lock = _lock(tmp_path)
    evidence_path = tmp_path / lock["evidence_manifest"]["path"]
    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    evidence["normative_sources"] = [
        source for source in evidence["normative_sources"] if source["role"] != "curriculum_standard"
    ]
    evidence_path.write_text(json.dumps(evidence, ensure_ascii=False), encoding="utf-8")
    lock["evidence_manifest"]["sha256"] = _sha(evidence_path)
    receipt_path = tmp_path / lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["evidence_manifest_sha256"] = _sha(evidence_path)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    lock["owner_approval"]["sha256"] = _sha(receipt_path)
    errors, _ = validate(lock, root=tmp_path)
    assert any("G0上游无效" in error and "curriculum_standard" in error for error in errors)


def test_g1_bound_paths_must_be_project_relative(tmp_path: Path):
    lock = _lock(tmp_path)
    lock["lesson_plan"]["path"] = str((tmp_path / lock["lesson_plan"]["path"]).resolve())
    errors, _ = validate(lock, root=tmp_path)
    assert any("lesson_plan必须使用项目根相对路径" in error for error in errors)


def test_g1_metadata_must_stay_with_same_lesson(tmp_path: Path):
    lock = _lock(tmp_path)
    original = tmp_path / lock["lesson_plan"]["path"]
    other = _write(tmp_path / "work/teaching/other/教案.md", original.read_text(encoding="utf-8"))
    lock["lesson_plan"]["path"] = str(other.relative_to(tmp_path))
    receipt_path = tmp_path / lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["lesson_plan_path"] = lock["lesson_plan"]["path"]
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    lock["owner_approval"]["sha256"] = _sha(receipt_path)
    errors, _ = validate(lock, root=tmp_path)
    assert any("必须位于同一课目录" in error for error in errors)


def test_g1_claim_boundary_must_state_classroom_evidence_is_pending(tmp_path: Path):
    lock = _lock(tmp_path)
    lock["contract"]["claim_boundary"] = "课堂效果仍待真实试教记录；但学生已经全部学懂并享受，试教已经完成。"
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("待真实课堂/试教验证" in error for error in errors)


def test_g1_files_must_live_under_formal_teaching_tree(tmp_path: Path):
    lock = _lock(tmp_path)
    original_plan = tmp_path / lock["lesson_plan"]["path"]
    original_evidence = tmp_path / lock["evidence_manifest"]["path"]
    original_approval = tmp_path / lock["owner_approval"]["path"]
    rogue_plan = _write(tmp_path / "rogue/lesson/教案.md", original_plan.read_text(encoding="utf-8"))
    rogue_evidence = _write(
        tmp_path / "rogue/lesson/_meta/evidence_manifest.json",
        original_evidence.read_text(encoding="utf-8"),
    )
    approval = json.loads(original_approval.read_text(encoding="utf-8"))
    approval["lesson_plan_path"] = str(rogue_plan.relative_to(tmp_path))
    rogue_approval = _write(
        tmp_path / "rogue/lesson/_meta/G1_owner_approval.json",
        json.dumps(approval, ensure_ascii=False, indent=2),
    )
    lock["lesson_plan"] = {"path": str(rogue_plan.relative_to(tmp_path)), "sha256": _sha(rogue_plan)}
    lock["evidence_manifest"] = {"path": str(rogue_evidence.relative_to(tmp_path)), "sha256": _sha(rogue_evidence)}
    lock["owner_approval"] = {"path": str(rogue_approval.relative_to(tmp_path)), "sha256": _sha(rogue_approval)}
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("必须位于work/teaching正式课程树" in error for error in errors)


def test_question_ids_must_be_nonempty_and_unique(tmp_path: Path):
    lock = _lock(tmp_path)
    lock["contract"]["questions"].append(dict(lock["contract"]["questions"][0]))
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("贯穿问题ID重复" in error for error in errors)


def test_guiding_questions_are_optional_when_the_text_sequence_is_the_main_line(tmp_path: Path):
    candidate = _candidate(tmp_path)
    candidate["contract"]["questions"] = []

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert not any("贯穿问题为空" in error for error in errors)
    assert errors == []


def test_question_must_have_at_least_one_stage_anchor(tmp_path: Path):
    lock = _lock(tmp_path)
    lock["contract"]["questions"][0]["stage_refs"] = []
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("贯穿问题Q1没有阶段落点" in error for error in errors)


def test_guiding_question_must_name_what_it_integrates_and_where_it_is_recovered(tmp_path: Path):
    candidate = _candidate(tmp_path)
    question = candidate["contract"]["questions"][0]
    question["objective_refs"] = []
    question["kid_refs"] = []
    question["recovery_stage_refs"] = []

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("贯穿问题Q1没有目标责任" in error for error in errors)
    assert any("贯穿问题Q1没有知识责任" in error for error in errors)
    assert any("贯穿问题Q1没有最终回收阶段" in error for error in errors)


def test_g1_rejects_single_character_human_lesson_plan(tmp_path: Path):
    lock = _lock(tmp_path)
    plan_path = tmp_path / lock["lesson_plan"]["path"]
    plan_path.write_text("x", encoding="utf-8")
    lock["lesson_plan"]["sha256"] = _sha(plan_path)
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("lesson_plan最低有效内容不足" in error for error in errors)


def test_g1_teachable_kid_must_bind_real_kp_from_knowledge_source(tmp_path: Path):
    lock = _lock(tmp_path)
    item = lock["contract"]["knowledge_items"][0]
    item["kp_ids"] = ["KP-CARD-NOT-IN-EVIDENCE-999"]
    errors, _ = validate(lock, root=tmp_path, verify_receipt=False)
    assert any("未解析到G0知识源" in error for error in errors)


def test_lesson_id_must_use_the_registered_les_format(tmp_path: Path):
    candidate = _candidate(tmp_path)
    candidate["lesson_id"] = "LES-B1-QYC-X"

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("lesson_id格式非法" in error for error in errors)


def test_same_lesson_id_cannot_resolve_to_two_course_directories(tmp_path: Path):
    candidate = _candidate(tmp_path)
    _write(
        tmp_path / "work/teaching/other-course/_meta/lesson_plan_candidate.json",
        json.dumps(
            {
                "schema_version": "lesson-plan-candidate.v1",
                "lesson_id": candidate["lesson_id"],
            },
            ensure_ascii=False,
        ),
    )

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("lesson_id解析到多个课程目录" in error for error in errors)


def test_one_course_directory_cannot_claim_two_lesson_ids(tmp_path: Path):
    candidate = _candidate(tmp_path)
    _write(
        tmp_path / "work/teaching/lesson/lesson.json",
        json.dumps({"lesson_id": "LES-OTHER-01"}, ensure_ascii=False),
    )

    errors, _ = validate_candidate(candidate, root=tmp_path)

    assert any("同一课程目录登记了多个lesson_id" in error for error in errors)


def test_owner_receipt_requires_real_string_fields_and_issue_array(tmp_path: Path):
    lock = _lock(tmp_path)
    receipt_path = tmp_path / lock["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["reviewer_id"] = ["project-owner"]
    receipt["approval_source"] = {"kind": "conversation"}
    receipt["resolved_issues"] = "没有问题"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False), encoding="utf-8")
    lock["owner_approval"]["sha256"] = _sha(receipt_path)

    errors, _ = validate(lock, root=tmp_path)

    assert any("owner_approval reviewer_id必须为字符串" in error for error in errors)
    assert any("owner_approval approval_source必须为字符串" in error for error in errors)
    assert any("owner_approval resolved_issues必须为数组" in error for error in errors)
