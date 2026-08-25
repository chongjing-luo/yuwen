from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts/checks"))

from validate_operational_governance import SKILL_STAGE, validate  # noqa: E402


def _write_valid_tree(root: Path) -> None:
    procedure = root / "work/methodology/lesson-preparation/语文备课操作规程.md"
    procedure.parent.mkdir(parents=True)
    procedure.write_text(
        "---\nstatus: active\nscope: 单篇语文课备课的唯一操作方法\n---\n# 规程\n",
        encoding="utf-8",
    )
    manuals = root / "work/methodology/manuals"
    manuals.mkdir(parents=True)
    for stage in range(10):
        (manuals / f"S{stage}-测试手册.md").write_text(
            "\n".join(
                [
                    f"# S{stage}",
                    "",
                    f"### MM-S{stage}-01 测试规则",
                    "- 优先级：P0",
                    "- 条件：需要时",
                    "- 动作：执行动作",
                    "- 判据：检查通过",
                    "- 出处：K1",
                    "- 预期信号：留下证据",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    for skill, stage in SKILL_STAGE.items():
        skill_file = root / f".agents/skills/{skill}/SKILL.md"
        skill_file.parent.mkdir(parents=True)
        skill_file.write_text(
            "\n".join(
                [
                    "---",
                    f"name: {skill}",
                    "description: 测试",
                    "---",
                    f"服务机制节点：K1。执行依据：MM-S{stage}-01。",
                    "",
                ]
            ),
            encoding="utf-8",
        )
    support_skill = root / ".agents/skills/yuwen-grill-decisions"
    (support_skill / "agents").mkdir(parents=True)
    (support_skill / "SKILL.md").write_text(
        "\n".join(
            [
                "---",
                "name: yuwen-grill-decisions",
                "description: 测试",
                "metadata:",
                "  project-governance:",
                "    status: active",
                "    role: decision_support",
                "    reads: [confirmed_intent, candidate_proposal]",
                "    writes: [chat_decision_summary]",
                "    authority_refs:",
                "      - AGENTS.md",
                "      - docs/architecture/项目设计方案.md",
                "      - work/evaluation/convergence.md",
                "    gate: explicit_confirmation",
                "    evidence_hook: fact_recommendation_decision_separation",
                "---",
                "# 测试",
                "",
            ]
        ),
        encoding="utf-8",
    )
    (support_skill / "agents/openai.yaml").write_text(
        "policy:\n  allow_implicit_invocation: false\n",
        encoding="utf-8",
    )
    registry = root / "work/principles/registry.yaml"
    registry.parent.mkdir(parents=True)
    registry.write_text(
        "\n".join(
            [
                "meta:",
                '  standard_version: "STANDARD-1.1-candidate"',
                '  standard_status: "candidate"',
                '  based_on: "STANDARD-1.0"',
                '  owner_approval: "pending"',
                "principles: []",
                "",
            ]
        ),
        encoding="utf-8",
    )


def test_valid_operational_governance_tree_passes(tmp_path: Path):
    _write_valid_tree(tmp_path)

    errors, stats = validate(tmp_path)

    assert errors == []
    assert stats["manual_entries"] == 10
    assert stats["stage_skills"] == len(SKILL_STAGE)
    assert stats["support_skills"] == 1


def test_decision_support_skill_requires_explicit_policy_and_chat_only_output(tmp_path: Path):
    _write_valid_tree(tmp_path)
    skill_dir = tmp_path / ".agents/skills/yuwen-grill-decisions"
    policy = skill_dir / "agents/openai.yaml"
    policy.write_text(
        policy.read_text(encoding="utf-8").replace("false", "true"),
        encoding="utf-8",
    )
    skill_file = skill_dir / "SKILL.md"
    skill_file.write_text(
        skill_file.read_text(encoding="utf-8").replace(
            "writes: [chat_decision_summary]",
            "writes: [project_files]",
        ),
        encoding="utf-8",
    )

    errors, _ = validate(tmp_path)

    assert any("yuwen-grill-decisions必须为explicit-only" in error for error in errors)
    assert any("yuwen-grill-decisions输出合同必须仅为chat_decision_summary" in error for error in errors)


def test_decision_support_skill_requires_governance_contract_and_authorities(tmp_path: Path):
    _write_valid_tree(tmp_path)
    skill_file = tmp_path / ".agents/skills/yuwen-grill-decisions/SKILL.md"
    skill_file.write_text(
        skill_file.read_text(encoding="utf-8").replace(
            "      - work/evaluation/convergence.md\n",
            "",
        ),
        encoding="utf-8",
    )

    errors, _ = validate(tmp_path)

    assert any("yuwen-grill-decisions缺治理依据: work/evaluation/convergence.md" in error for error in errors)


def test_manual_entry_requires_all_six_fields_and_mechanism_node(tmp_path: Path):
    _write_valid_tree(tmp_path)
    manual = tmp_path / "work/methodology/manuals/S3-测试手册.md"
    manual.write_text(
        manual.read_text(encoding="utf-8")
        .replace("- 判据：检查通过\n", "")
        .replace("- 出处：K1", "- 出处：P-01"),
        encoding="utf-8",
    )

    errors, _ = validate(tmp_path)

    assert any("MM-S3-01缺字段: 判据" in error for error in errors)
    assert any("MM-S3-01出处未绑定机制节点" in error for error in errors)


def test_s0_data_rules_do_not_require_lesson_goal_nodes(tmp_path: Path):
    _write_valid_tree(tmp_path)
    manual = tmp_path / "work/methodology/manuals/S0-测试手册.md"
    manual.write_text(
        manual.read_text(encoding="utf-8").replace("- 出处：K1", "- 出处：数据治理契约"),
        encoding="utf-8",
    )
    skill = tmp_path / ".agents/skills/yuwen-intake/SKILL.md"
    skill.write_text(
        skill.read_text(encoding="utf-8").replace("服务机制节点：K1。", "执行数据治理契约。"),
        encoding="utf-8",
    )

    errors, _ = validate(tmp_path)

    assert not any("MM-S0-01出处未绑定机制节点" in error for error in errors)
    assert not any("yuwen-intake未声明服务的机制节点" in error for error in errors)


def test_stage_skill_requires_real_same_stage_manual_reference(tmp_path: Path):
    _write_valid_tree(tmp_path)
    skill = tmp_path / ".agents/skills/yuwen-design-lesson/SKILL.md"
    skill.write_text(
        skill.read_text(encoding="utf-8").replace("MM-S3-01", "MM-S4-99"),
        encoding="utf-8",
    )

    errors, _ = validate(tmp_path)

    assert any("yuwen-design-lesson未引用本阶段MM-S3" in error for error in errors)
    assert any("MM-S4-99不存在" in error for error in errors)


def test_canonical_procedure_must_be_active(tmp_path: Path):
    _write_valid_tree(tmp_path)
    procedure = tmp_path / "work/methodology/lesson-preparation/语文备课操作规程.md"
    procedure.write_text(
        procedure.read_text(encoding="utf-8").replace("status: active", "status: candidate"),
        encoding="utf-8",
    )

    errors, _ = validate(tmp_path)

    assert any("唯一操作规程status必须为active" in error for error in errors)


def test_candidate_standard_must_be_named_and_marked_honestly(tmp_path: Path):
    _write_valid_tree(tmp_path)
    registry = tmp_path / "work/principles/registry.yaml"
    registry.write_text(
        registry.read_text(encoding="utf-8")
        .replace("STANDARD-1.1-candidate", "STANDARD-1.0")
        .replace('owner_approval: "pending"', 'owner_approval: "approved"'),
        encoding="utf-8",
    )

    errors, _ = validate(tmp_path)

    assert any("candidate标准名必须以-candidate结尾" in error for error in errors)
    assert any("candidate标准的owner_approval必须为pending" in error for error in errors)
