#!/usr/bin/env python3
"""Read-only validation of lesson-operation authority and references."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
NODE_RE = re.compile(r"(?<![A-Z0-9])(?:K[1-5]|U[1-8]|J[1-7])(?![A-Z0-9])")
MM_RE = re.compile(r"\bMM-S([0-9])-\d{2,}\b")
ENTRY_RE = re.compile(r"^### (MM-S([0-9])-\d{2,})\s+.+$", re.MULTILINE)
FIELDS = ("优先级", "条件", "动作", "判据", "出处", "预期信号")

SKILL_STAGE = {
    "yuwen-intake": 0,
    "yuwen-organize": 0,
    "yuwen-curate": 0,
    "yuwen-catalog": 0,
    "yuwen-plan-unit": 1,
    "yuwen-author-lesson-plan": 2,
    "yuwen-research-text": 2,
    "yuwen-design-lesson": 3,
    "yuwen-build-materials": 4,
    "yuwen-audit-lesson": 5,
    "yuwen-trial-observation": 6,
    "yuwen-design-homework": 7,
    "yuwen-grade-feedback": 7,
    "yuwen-author-assessment": 8,
    "yuwen-diagnose-learning": 8,
    "yuwen-reflect-lesson": 9,
}

SUPPORT_SKILL_CONTRACTS = {
    "yuwen-grill-decisions": {
        "role": "decision_support",
        "authorities": {
            "AGENTS.md",
            "docs/architecture/项目设计方案.md",
            "work/evaluation/convergence.md",
        },
        "writes": ["chat_decision_summary"],
        "gate": "explicit_confirmation",
    }
}


def _frontmatter(text: str) -> dict:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    value = yaml.safe_load(text[4:end])
    return value if isinstance(value, dict) else {}


def _manual_entries(path: Path) -> list[tuple[str, int, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(ENTRY_RE.finditer(text))
    entries = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        entries.append((match.group(1), int(match.group(2)), text[match.start():end]))
    return entries


def validate(root: Path = ROOT) -> tuple[list[str], dict[str, int]]:
    errors: list[str] = []
    procedure_path = root / "work/methodology/lesson-preparation/语文备课操作规程.md"
    if not procedure_path.is_file():
        errors.append("唯一操作规程不存在")
    else:
        meta = _frontmatter(procedure_path.read_text(encoding="utf-8"))
        if meta.get("status") != "active":
            errors.append("唯一操作规程status必须为active")
        if "唯一" not in str(meta.get("scope") or ""):
            errors.append("唯一操作规程scope必须明确唯一性")

    manuals_dir = root / "work/methodology/manuals"
    manual_ids: set[str] = set()
    entry_count = 0
    for stage in range(10):
        paths = sorted(manuals_dir.glob(f"S{stage}-*.md"))
        if len(paths) != 1:
            errors.append(f"S{stage}手册应且仅应有一份，实际{len(paths)}份")
            continue
        entries = _manual_entries(paths[0])
        if not entries:
            errors.append(f"{paths[0].name}没有MM条目")
        for mm_id, declared_stage, block in entries:
            entry_count += 1
            if declared_stage != stage:
                errors.append(f"{mm_id}与手册阶段S{stage}不一致")
            if mm_id in manual_ids:
                errors.append(f"MM条目重复: {mm_id}")
            manual_ids.add(mm_id)
            values: dict[str, str] = {}
            for field in FIELDS:
                match = re.search(rf"^- {re.escape(field)}：(.*)$", block, re.MULTILINE)
                if not match or not match.group(1).strip():
                    errors.append(f"{mm_id}缺字段: {field}")
                else:
                    values[field] = match.group(1).strip()
            # K/U/J are lesson-preparation goal coordinates.  S0 is the data
            # axis and is governed by provenance/catalog contracts instead.
            if stage > 0 and "出处" in values and not NODE_RE.search(values["出处"]):
                errors.append(f"{mm_id}出处未绑定机制节点")

    for skill, stage in SKILL_STAGE.items():
        path = root / ".agents/skills" / skill / "SKILL.md"
        if not path.is_file():
            errors.append(f"阶段skill不存在: {skill}")
            continue
        text = path.read_text(encoding="utf-8")
        refs = {match.group(0) for match in MM_RE.finditer(text)}
        if not any(ref.startswith(f"MM-S{stage}-") for ref in refs):
            errors.append(f"{skill}未引用本阶段MM-S{stage}条目")
        for ref in sorted(refs - manual_ids):
            errors.append(f"{skill}引用的{ref}不存在")
        if stage > 0 and not NODE_RE.search(text):
            errors.append(f"{skill}未声明服务的机制节点")

    for skill, expected in SUPPORT_SKILL_CONTRACTS.items():
        skill_dir = root / ".agents/skills" / skill
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.is_file():
            errors.append(f"支持skill不存在: {skill}")
            continue
        meta = _frontmatter(skill_path.read_text(encoding="utf-8"))
        if meta.get("name") != skill:
            errors.append(f"{skill}的frontmatter name必须与目录名一致")
        governance = (meta.get("metadata") or {}).get("project-governance")
        if not isinstance(governance, dict):
            errors.append(f"{skill}缺project-governance合同")
            continue
        if governance.get("status") != "active":
            errors.append(f"{skill}治理合同status必须为active")
        if governance.get("role") != expected["role"]:
            errors.append(f"{skill}治理职责必须为{expected['role']}")
        if not isinstance(governance.get("reads"), list) or not governance["reads"]:
            errors.append(f"{skill}读取合同不能为空")
        if governance.get("writes") != expected["writes"]:
            errors.append(f"{skill}输出合同必须仅为chat_decision_summary")
        actual_authorities = set(governance.get("authority_refs") or [])
        for authority in sorted(expected["authorities"] - actual_authorities):
            errors.append(f"{skill}缺治理依据: {authority}")
        if governance.get("gate") != expected["gate"]:
            errors.append(f"{skill}放行条件必须为explicit_confirmation")
        if not str(governance.get("evidence_hook") or "").strip():
            errors.append(f"{skill}质量证据挂钩不能为空")
        policy_path = skill_dir / "agents/openai.yaml"
        if not policy_path.is_file():
            errors.append(f"{skill}缺explicit-only调用策略")
        else:
            try:
                policy_doc = yaml.safe_load(policy_path.read_text(encoding="utf-8")) or {}
            except yaml.YAMLError as exc:
                errors.append(f"{skill}调用策略无法解析: {exc}")
            else:
                allow_implicit = (policy_doc.get("policy") or {}).get("allow_implicit_invocation")
                if allow_implicit is not False:
                    errors.append(f"{skill}必须为explicit-only")

    registry_path = root / "work/principles/registry.yaml"
    if not registry_path.is_file():
        errors.append("原则注册库不存在")
    else:
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8")) or {}
        meta = registry.get("meta") or {}
        version = str(meta.get("standard_version") or "")
        status = meta.get("standard_status")
        if status not in {"active", "candidate"}:
            errors.append("原则标准standard_status必须为active或candidate")
        elif status == "candidate":
            if not version.endswith("-candidate"):
                errors.append("candidate标准名必须以-candidate结尾")
            if not str(meta.get("based_on") or "").startswith("STANDARD-"):
                errors.append("candidate标准必须声明based_on")
            if meta.get("owner_approval") != "pending":
                errors.append("candidate标准的owner_approval必须为pending")
        elif version.endswith("-candidate"):
            errors.append("active标准名不得以-candidate结尾")

    return errors, {
        "manual_entries": entry_count,
        "stage_skills": len(SKILL_STAGE),
        "support_skills": len(SUPPORT_SKILL_CONTRACTS),
        "manual_ids": len(manual_ids),
    }


def main() -> int:
    errors, stats = validate(ROOT)
    if errors:
        for error in errors:
            print(f"[error] {error}")
        print(f"操作治理校验失败：{len(errors)}错误")
        return 1
    print(
        "操作治理校验通过："
        f"{stats['manual_entries']}条MM / {stats['stage_skills']}个阶段skill / "
        f"{stats['support_skills']}个支持skill / 唯一规程active"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
