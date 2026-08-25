#!/usr/bin/env python3
"""通用课程数据校验器（legacy v1/v2.0/v2.1兼容；strict放行绑定G1的v2.2—v2.6）。

课文无关：任何 lesson.js（Node 模块）或 lesson JSON 都可校验。这是
N-01（教级知识清单以知识卡为准）的机器强制——课程数据不再允许脱离
知识库自说自话。

检查：
1. 顶层：schema_version / lesson_id / book_unit.card_refs / text_contract(源路径+sha) /
   three_questions为字符串列表（可为空）/ kp_scope / pages≥1 / claim_boundary（两本账）；
   strict模式另验证G1合同哈希、范围、顺序、总时长和收束方式；
2. K1：card_refs 与 kp_scope.kp_ids 解析到真实知识卡；deferred 有理由；
3. K4：relations（若存在）的 card_id 解析；
4. 页面：18 项合同字段非空；v2页面绑定stage/objective/KID并覆盖G1范围；
   v2.1另校验知识分页、受控活动、学生体验、教学版式和完整逐页剧本；
   v2.2把前台元素、信息状态和台词时序结构化，确保S4可唯一复原B0/B1/B2；
   v2.3增加课堂事件类型及其条件合同，不再为讲授、叙述、朗读和沉静虚构学生任务；
   v2.4以语义场景、内容对象、关系、显示约束和排版操作替代封闭版式家族，
   并显式校验共视、分时、连续锚点、层级和动态密度判断；
   v2.5增加教材优先的视觉来源档案与逐信息状态物理画面蓝图，使S4无需
   重新决定上屏内容、构图关系、配图资格和视觉来源；
   v2.6增加页面呈现角色，区分标题、导航、章节（子标题）、主干、支撑、
   活动、作品反馈、总结与作业；支撑页另须形成触发—返回闭环；
   定位结构页PG01—PG03不得为通过合同伪挂目标、KID或知识负载；
   unique_difficulty 等追溯字段非样板（复用
   check_trace_evidence）；script.timeboxes 秒和 == minutes*60；branches ≥ 2；
   next_use 非空；literary_object 三形态锚定 canonical_lines（K2：行串/行数组/
   非行对象 kind 声明）；
5. U1/P-07：frontstage 与 title 过前台禁词；
6. 汇总样板发现数（默认不判失败——收敛规则：样板清零是 STANDARD-1.0 对
   新候选的要求，对存量数据作为缺口报告）。

用法：python3 scripts/validate_lesson_schema.py (--lesson-js PATH | --lesson-json PATH) [--strict]
退出码：0 通过；1 失败（--strict 时样板也判失败）。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

from validate_lesson_evidence import has_pending_classroom_boundary

ROOT = Path(__file__).resolve().parents[1]
KP_ID_PATTERN = re.compile(r"KP-CARD-[A-Z0-9-]+-\d{3}")

PAGE_REQUIRED_FIELDS = [
    "page_id", "title", "minutes", "literary_object", "unique_difficulty",
    "unique_function", "information_state", "student_action", "artifact",
    "next_use", "normal_counterexample", "first_person_reception",
    "deletion_loss", "story_return",
]

# A-01: sixteen per-page contract fields plus two cross-page budgets.  These
# are mandatory for v2; legacy v1 remains readable only outside strict mode.
V2_PAGE_CONTRACT_FIELDS = [
    "previous_page_input",
    "unique_difficulty",
    "unique_function",
    "first_view_contract",
    "information_state",
    "student_action",
    "artifact",
    "real_wait",
    "bounded_feedback",
    "visible_revision",
    "next_use",
    "normal_counterexample",
    "visual_role",
    "first_person_reception",
    "deletion_loss",
    "continuous_increment",
    "attention_budget",
    "story_return",
]
V2_PAGE_STRING_FIELDS = set(V2_PAGE_CONTRACT_FIELDS) - {"student_action"}
V2_TOP_LEVEL_FIELDS = {
    "schema_version", "lesson_id", "lesson_plan_binding", "lesson_plan_scope",
    "book_unit", "text_contract", "three_questions", "objectives", "kp_scope",
    "relations", "pages", "claim_boundary", "target_natural_minutes",
    "visual_source_profile",
}
V2_BINDING_FIELDS = {"path", "sha256"}
V2_SCOPE_FIELDS = {
    "objective_ids", "knowledge_ids", "deferred_ids", "question_ids",
    "stage_ids", "contract_sha256", "total_minutes", "closing_mode",
}
V2_BOOK_UNIT_FIELDS = {"card_refs", "unit_ref"}
V2_TEXT_CONTRACT_FIELDS = {"source_path", "source_sha256", "canonical_lines"}
V2_OBJECTIVE_FIELDS = {"id", "dimension", "statement", "kp_refs", "nodes", "evidence_pages"}
V2_KP_SCOPE_FIELDS = {"kp_ids", "deferred"}
V2_DEFERRED_FIELDS = {"kp_id", "reason"}
V2_RELATION_FIELDS = {"card_id", "relation"}
V20_PAGE_FIELDS = set(V2_PAGE_CONTRACT_FIELDS) | {
    "page_id", "stage_id", "objective_ids", "lesson_kids", "title", "minutes",
    "literary_object", "next_use_ref", "script", "frontstage",
}
V2_NEXT_USE_FIELDS = {"kind", "target_id", "use"}
V20_SCRIPT_FIELDS = {"teacher_spoken", "timeboxes", "branches"}
V2_TIMEBOX_FIELDS = {"label", "seconds"}
V22_TIMEBOX_FIELDS = V2_TIMEBOX_FIELDS | {"segment_ids"}
V2_BRANCH_FIELDS = {"kind", "response"}
V2_LITERARY_OBJECT_FIELDS = {"kind", "scope", "lines"}

V21_PAGE_FIELDS = (V20_PAGE_FIELDS - {"frontstage"}) | {
    "knowledge_payload", "activity_contract", "student_experience", "slide_design",
}
V21_KNOWLEDGE_PAYLOAD_FIELDS = {"kid", "scope", "page_role"}
V21_ACTIVITY_FIELDS = {
    "primary_type", "secondary_types", "teacher_move_types", "learner_action_types",
    "participation_type", "artifact_type", "sensory_channel_types", "feedback_types",
    "selection_reason", "knowledge_fit", "experience_fit",
}
V23_ACTIVITY_FIELDS = V21_ACTIVITY_FIELDS | {"event_type"}
V21_EXPERIENCE_FIELDS = {"perceives", "thinks", "possible_feeling", "does", "understands"}
V21_SLIDE_DESIGN_FIELDS = {
    "layout_type", "frontstage_elements", "spatial_plan", "information_hierarchy",
    "reveal_sequence", "layout_rationale",
}
V22_SLIDE_DESIGN_FIELDS = V21_SLIDE_DESIGN_FIELDS | {"information_states"}
V24_SLIDE_DESIGN_FIELDS = {
    "semantic_unit", "organizing_intention", "content_object_types",
    "semantic_relations", "display_constraints", "layout_operations",
    "co_view_groups", "must_stage", "priority_layers", "continuity_anchor",
    "density_judgment", "boundary_rationale", "frontstage_elements",
    "information_states", "information_hierarchy", "reveal_sequence",
    "layout_rationale",
}
V25_SLIDE_DESIGN_FIELDS = V24_SLIDE_DESIGN_FIELDS | {"physical_screens"}
V26_SLIDE_DESIGN_FIELDS = V25_SLIDE_DESIGN_FIELDS | {
    "presentation_role", "role_rationale", "support_link",
}
V26_SUPPORT_LINK_FIELDS = {"trigger", "source_ref", "return_ref", "return_use"}
V25_VISUAL_PROFILE_FIELDS = {
    "strategy", "source_artifacts", "palette", "image_style", "shape_language",
    "typography_tone", "consistency_rules", "fact_boundary",
}
V25_VISUAL_SOURCE_FIELDS = {
    "asset_id", "path", "sha256", "role", "usage_boundary",
}
V25_PALETTE_FIELDS = {"role", "hex", "source_basis"}
V25_VISUAL_STRATEGIES = {"textbook_first", "text_type_only", "hybrid"}
V25_PHYSICAL_SCREEN_FIELDS = {
    "screen_id", "state_id", "visible_element_ids", "screen_function",
    "composition_blueprint", "reading_path", "spatial_proportions", "image_plan",
    "script_segment_refs",
}
V25_IMAGE_PLAN_FIELDS = {
    "decision", "function", "derivation_mode", "asset_refs", "content_brief",
    "style_brief", "placement", "visual_weight", "appearance_timing",
    "fact_boundary",
}
V25_IMAGE_DECISIONS = {"required", "optional", "forbidden"}
V25_DERIVATION_MODES = {
    "direct_textbook_asset", "textbook_visual_derivation", "text_type_fallback", "none",
}
V22_FRONTSTAGE_ELEMENT_FIELDS = {"id", "text", "role"}
V22_INFORMATION_STATE_FIELDS = {"id", "visible_element_ids", "enter_trigger"}
V24_SEMANTIC_RELATION_FIELDS = {"type", "element_ids", "rationale"}
V24_CO_VIEW_GROUP_FIELDS = {"id", "element_ids", "rationale"}
V24_MUST_STAGE_FIELDS = {"element_ids", "rationale"}
V24_PRIORITY_LAYER_FIELDS = {"level", "element_ids", "rationale"}
V24_DENSITY_FIELDS = {"semantic_completeness", "readability_focus", "decision"}
V24_DENSITY_DECISIONS = {"retain_as_page"}
V22_FRONTSTAGE_ROLES = {"content", "prompt", "material", "student_work", "calibration", "feedback"}
V22_STATE_TRIGGERS = {
    "page_enter", "after_instruction", "after_prior_artifact_retrieved",
    "after_primary_artifact_committed", "after_secondary_artifact_committed",
    "after_peer_response", "after_calibration",
}
V23_STATE_TRIGGERS = V22_STATE_TRIGGERS | {"after_student_response"}
V22_TRIGGER_RANK = {
    "page_enter": 0,
    "after_instruction": 1,
    "after_prior_artifact_retrieved": 1,
    "after_primary_artifact_committed": 2,
    "after_peer_response": 3,
    "after_secondary_artifact_committed": 3,
    "after_calibration": 4,
}
V23_TRIGGER_RANK = V22_TRIGGER_RANK | {"after_student_response": 2}
V21_SCRIPT_FIELDS = {
    "transition_spoken", "teacher_spoken", "student_process", "expected_responses",
    "branches", "feedback_spoken", "observable_evidence", "cut_spoken", "timeboxes",
}
V22_SCRIPT_FIELDS = V21_SCRIPT_FIELDS | {"script_segments"}
V22_SCRIPT_SEGMENT_FIELDS = {"id", "state_id", "kind", "enter_trigger", "text"}
V22_SCRIPT_KINDS = {"transition", "task", "wait", "calibration", "feedback", "cut"}
V23_SCRIPT_KINDS = V22_SCRIPT_KINDS | {"instruction", "narration", "reading", "summary"}
EVENT_REQUIREMENT_IDS = {
    "task", "wait", "expected_responses", "branches", "artifact",
    "feedback", "revision", "normal_counterexample",
}
LEGACY_EVENT_REQUIREMENTS = EVENT_REQUIREMENT_IDS
CATEGORY_REGISTRY_PATH = Path("work/methodology/lesson-preparation/教学设计类别注册表.json")

# 课程数据可用的备课机制节点全集（并非项目通用准入标签）
NODE_IDS = {f"K{i}" for i in range(1, 6)} | {f"U{i}" for i in range(1, 9)} | {f"J{i}" for i in range(1, 8)}

# literary_object 非行对象的合法类别（K2）：行锚定之外，页面确以非诗对象为主时
# 必须显式声明类别，不许自由散文冒充行锚定。
NON_POEM_KINDS = {
    "student_products", "full_poem_voice", "cultural_knowledge", "question_set",
    "lesson_orientation", "mixed",
}


def _line_anchored(obj: str, canonical: list[str]) -> bool:
    return any(obj in line or line in obj for line in canonical)


def _nonempty_string_list(value: object) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and bool(item.strip()) for item in value)
    )


def _string_list(value: object) -> bool:
    return isinstance(value, list) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


def canonical_information_state(
    frontstage_elements: list[dict], information_states: list[dict]
) -> str:
    """Return the only supported prose projection of v2.2 element states."""
    element_text = {
        str(item.get("id") or ""): str(item.get("text") or "").strip()
        for item in frontstage_elements
        if isinstance(item, dict)
    }
    parts: list[str] = []
    prior: set[str] = set()
    for index, state in enumerate(information_states):
        if not isinstance(state, dict):
            continue
        state_id = str(state.get("id") or f"B{index}")
        trigger = str(state.get("enter_trigger") or "")
        visible_ids = state.get("visible_element_ids") or []
        newly_visible = [item for item in visible_ids if item not in prior]
        texts = [element_text.get(item, item) for item in newly_visible]
        label = "可见" if index == 0 else "新增可见"
        parts.append(f"{state_id}（{trigger}）{label}：" + "｜".join(texts))
        prior.update(visible_ids)
    return "；".join(parts) + "。"


def _minimum_effective_text(value: object, minimum: int = 8, unique_minimum: int = 4) -> bool:
    """Reject empty, one-character, and repeated-character contract fillers."""
    if not isinstance(value, str):
        return False
    normalized = re.sub(r"[\s\W_]", "", value, flags=re.UNICODE)
    return len(normalized) >= minimum and len(set(normalized.casefold())) >= unique_minimum


def _normalize_source_anchor(value: str) -> str:
    """Normalize MinerU inline footnote markers without changing canonical classroom text."""
    without_sup_notes = re.sub(
        r"<sup\b[^>]*>.*?</sup>", "", value, flags=re.IGNORECASE | re.DOTALL
    )
    return re.sub(r"\s+", "", without_sup_notes)


def _reject_unknown_fields(value: object, allowed: set[str], label: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        return
    for unknown_field in sorted(set(value) - allowed):
        errors.append(f"{label}含未知字段: {unknown_field}")


def _registered_ids(registry: dict, field: str) -> set[str]:
    values = registry.get(field)
    if not isinstance(values, list):
        return set()
    return {
        str(item.get("id"))
        for item in values
        if isinstance(item, dict) and isinstance(item.get("id"), str) and item.get("id").strip()
    }


def _load_category_registry(
    root: Path,
    errors: list[str],
    *,
    require_event_types: bool = False,
    require_semantic_layout: bool = False,
    require_presentation_roles: bool = False,
) -> dict:
    path = root / CATEGORY_REGISTRY_PATH
    if not path.is_file():
        errors.append(f"v2.1缺教学设计类别注册表: {CATEGORY_REGISTRY_PATH}")
        return {}
    try:
        registry = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        errors.append(f"教学设计类别注册表不可读: {exc}")
        return {}
    if registry.get("schema_version") != "teaching-design-category-registry.v1":
        errors.append("教学设计类别注册表schema_version非法")
    required_lists = (
        "activity_types", "teacher_move_types", "learner_action_types",
        "participation_types", "artifact_types", "sensory_channel_types",
        "feedback_types", "layout_types", "knowledge_page_roles",
    )
    if require_event_types:
        required_lists = ("event_types",) + required_lists
    if require_semantic_layout:
        required_lists = required_lists + (
            "content_object_types", "semantic_relation_types",
            "display_constraint_types", "layout_operation_types",
        )
    if require_presentation_roles:
        required_lists = required_lists + ("presentation_role_types",)
    for field in required_lists:
        value = registry.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"教学设计类别注册表.{field}必须为非空列表")
    id_list_fields = tuple(field for field in required_lists if field != "knowledge_page_roles")
    for field in id_list_fields:
        ids = [
            item.get("id") for item in registry.get(field) or [] if isinstance(item, dict)
        ]
        if len(ids) != len(set(ids)):
            errors.append(f"教学设计类别注册表.{field}存在重复ID")
    for index, event in enumerate(registry.get("event_types") or []):
        if not isinstance(event, dict):
            continue
        requires = event.get("requires")
        if not _string_list(requires):
            errors.append(f"教学设计类别注册表.event_types[{index}].requires必须为字符串列表")
            continue
        unknown_requirements = set(requires) - EVENT_REQUIREMENT_IDS
        if unknown_requirements:
            errors.append(
                f"教学设计类别注册表.event_types[{index}].requires含未知合同项: "
                f"{sorted(unknown_requirements)}"
            )
        if not isinstance(event.get("allows_no_primary_activity"), bool):
            errors.append(
                f"教学设计类别注册表.event_types[{index}].allows_no_primary_activity必须为布尔值"
            )
    return registry


def _registered_string_list(
    value: object,
    allowed: set[str],
    label: str,
    errors: list[str],
    *,
    allow_empty: bool = False,
) -> list[str]:
    valid_shape = _string_list(value) if allow_empty else _nonempty_string_list(value)
    if not valid_shape:
        qualifier = "字符串列表" if allow_empty else "非空字符串列表"
        errors.append(f"{label}必须为{qualifier}")
        return []
    result = list(value)
    if len(result) != len(set(result)):
        errors.append(f"{label}不得含重复ID")
    for item in result:
        if item not in allowed:
            errors.append(f"{label}含未注册ID: {item}")
    return result


def _layout_rationale_effective(value: object) -> bool:
    if not _minimum_effective_text(value, minimum=14, unique_minimum=6):
        return False
    assert isinstance(value, str)
    pedagogic_cues = (
        "学生", "原文", "证据", "首答", "比较", "阅读", "观察", "注意",
        "知识", "动作", "修订", "译述", "关系", "揭示", "思考", "理解",
    )
    return any(cue in value for cue in pedagogic_cues)


def literary_object_error(pid: str, obj, canonical: list[str]) -> str | None:
    """K2 情境锚定三形态：行串（含多行拼接串）/ 行数组 / 非行对象声明。"""
    if obj is None or obj == "" or obj == []:
        return None  # 缺字段由 PAGE_REQUIRED_FIELDS 检查报告
    if isinstance(obj, str):
        if not _line_anchored(obj, canonical):
            return f"{pid}: literary_object「{obj}」不在 canonical_lines 内（K2 情境锚定）"
        return None
    if isinstance(obj, list):
        bad = [x for x in obj if not (isinstance(x, str) and _line_anchored(x, canonical))]
        if bad:
            return f"{pid}: literary_object 数组含未锚定项（K2）: {bad[:2]}"
        return None
    if isinstance(obj, dict):
        if obj.get("kind") not in NON_POEM_KINDS:
            return f"{pid}: literary_object.kind 非法（K2）: {obj.get('kind')!r}，合法类别: {sorted(NON_POEM_KINDS)}"
        scope = obj.get("scope")
        if scope is not None and scope != "full_poem":
            return f"{pid}: literary_object.scope 仅支持 full_poem（K2）: {scope!r}"
        lines = obj.get("lines")
        if lines is not None and not (
            isinstance(lines, list) and bool(lines)
            and all(isinstance(x, str) and _line_anchored(x, canonical) for x in lines)
        ):
            return f"{pid}: literary_object.lines 须为非空且逐项锚定 canonical_lines（K2）"
        return None
    return f"{pid}: literary_object 类型非法（K2）: {type(obj).__name__}"


def load_lesson(lesson_js: str | None, lesson_json: str | None) -> dict:
    if bool(lesson_js) == bool(lesson_json):
        raise SystemExit("必须且只能提供 --lesson-js 或 --lesson-json 之一")
    if lesson_json:
        return json.loads((ROOT / lesson_json if not Path(lesson_json).is_absolute() else Path(lesson_json)).read_text(encoding="utf-8"))
    result = subprocess.run(
        ["node", "-e", "console.log(JSON.stringify(require(process.argv[1])))", str((ROOT / lesson_js).resolve())],
        capture_output=True, text=True, check=True, cwd=ROOT,
    )
    return json.loads(result.stdout)


def resolve_card(card_id: str, root: Path = ROOT) -> Path | None:
    matches = list((root / "work/knowledge").glob(f"*/cards/{card_id}*.md"))
    return matches[0] if matches else None


def card_kp_ids(card_path: Path) -> set[str]:
    return set(KP_ID_PATTERN.findall(card_path.read_text(encoding="utf-8")))


def validate(
    lesson: dict,
    strict: bool,
    root: Path = ROOT,
    enforcement_config: dict | None = None,
) -> tuple[list[str], list[str], dict]:
    errors: list[str] = []
    warnings: list[str] = []
    stats: dict = {"pages": 0, "boilerplate": 0, "kp_scope": 0, "deferred": 0}

    for field in ("schema_version", "lesson_id", "book_unit", "text_contract", "three_questions", "kp_scope", "pages", "claim_boundary"):
        if field not in lesson:
            errors.append(f"缺少顶层字段: {field}")
    if errors:
        return errors, warnings, stats

    structural_fields = {
        "book_unit": dict,
        "text_contract": dict,
        "kp_scope": dict,
        "pages": list,
    }
    for field, expected_type in structural_fields.items():
        if not isinstance(lesson[field], expected_type):
            errors.append(f"顶层字段{field}必须为{expected_type.__name__}")
    if not _string_list(lesson["three_questions"]):
        errors.append("three_questions必须为字符串列表；本课不设贯穿问题时使用空列表")
    if isinstance(lesson.get("pages"), list) and (
        not lesson["pages"] or not all(isinstance(page, dict) for page in lesson["pages"])
    ):
        errors.append("pages必须为非空对象列表")
    if errors:
        return errors, warnings, stats

    schema_version = str(lesson.get("schema_version") or "")
    is_v2 = schema_version in {"2.0", "2.1", "2.2", "2.3", "2.4", "2.5", "2.6"}
    is_v21 = schema_version == "2.1"
    is_v22 = schema_version == "2.2"
    is_v23 = schema_version == "2.3"
    is_v24 = schema_version == "2.4"
    is_v25 = schema_version == "2.5"
    is_v26 = schema_version == "2.6"
    is_v25_plus = is_v25 or is_v26
    is_v24_plus = is_v24 or is_v25_plus
    is_v23_plus = is_v23 or is_v24_plus
    is_v22_plus = is_v22 or is_v23_plus
    is_v21_plus = is_v21 or is_v22_plus
    if strict and not is_v22_plus:
        errors.append("strict只接受v2.2—v2.6课程数据：schema_version必须为2.2、2.3、2.4、2.5或2.6并绑定经所有者批准的G1教案锁")
    category_registry = (
        _load_category_registry(
            root,
            errors,
            require_event_types=is_v23_plus,
            require_semantic_layout=is_v24_plus,
            require_presentation_roles=is_v26,
        )
        if is_v21_plus else {}
    )
    approved_contract: dict | None = None
    approved_stage_ids: set[str] = set()
    approved_stage_order: list[str] = []
    approved_teachable_kids: set[str] = set()
    approved_kid_to_kps: dict[str, set[str]] = {}
    approved_objective_to_kps: dict[str, set[str]] = {}
    approved_stage_to_objectives: dict[str, set[str]] = {}
    approved_stage_to_kids: dict[str, set[str]] = {}
    visual_source_asset_ids: set[str] = set()
    if is_v2:
        for unknown_field in sorted(set(lesson) - V2_TOP_LEVEL_FIELDS):
            errors.append(f"v2含未知顶层字段: {unknown_field}")
        if is_v25_plus:
            visual_profile = lesson.get("visual_source_profile")
            if not isinstance(visual_profile, dict):
                errors.append("v2.5+缺visual_source_profile（教材视觉来源与风格边界）")
                visual_profile = {}
            _reject_unknown_fields(
                visual_profile, V25_VISUAL_PROFILE_FIELDS,
                "visual_source_profile", errors,
            )
            strategy = str(visual_profile.get("strategy") or "").strip()
            if strategy not in V25_VISUAL_STRATEGIES:
                errors.append(f"visual_source_profile.strategy非法: {strategy}")
            visual_sources = visual_profile.get("source_artifacts")
            if not isinstance(visual_sources, list) or not all(
                isinstance(item, dict) for item in visual_sources
            ):
                errors.append("visual_source_profile.source_artifacts必须为对象列表")
                visual_sources = []
            if strategy in {"textbook_first", "hybrid"} and not visual_sources:
                errors.append(f"visual_source_profile.strategy={strategy}时必须登记教材视觉来源资产")
            visual_asset_id_list: list[str] = []
            for index, source_artifact in enumerate(visual_sources):
                label = f"visual_source_profile.source_artifacts[{index}]"
                _reject_unknown_fields(
                    source_artifact, V25_VISUAL_SOURCE_FIELDS, label, errors
                )
                asset_id = str(source_artifact.get("asset_id") or "").strip()
                if not re.fullmatch(r"[A-Z][A-Z0-9-]{1,31}", asset_id):
                    errors.append(f"{label}.asset_id格式非法: {asset_id}")
                visual_asset_id_list.append(asset_id)
                for field in ("role", "usage_boundary"):
                    if not _minimum_effective_text(
                        source_artifact.get(field), minimum=8, unique_minimum=4
                    ):
                        errors.append(f"{label}.{field}最低有效内容不足")
                source_path_value = str(source_artifact.get("path") or "").strip()
                source_path = Path(source_path_value)
                if source_path.is_absolute():
                    errors.append(f"{label}.path必须使用项目根相对路径")
                else:
                    source_path = (root / source_path).resolve()
                    try:
                        source_path.relative_to(root.resolve())
                    except ValueError:
                        errors.append(f"{label}.path越出项目根")
                        source_path = root / "__invalid_visual_source__"
                if not source_path_value or not source_path.is_file():
                    errors.append(f"视觉来源资产不存在: {source_path_value}")
                else:
                    expected_sha = str(source_artifact.get("sha256") or "").strip()
                    actual_sha = hashlib.sha256(source_path.read_bytes()).hexdigest()
                    if expected_sha != actual_sha:
                        errors.append(f"视觉来源资产sha256与实际文件不一致: {asset_id}")
            if len(visual_asset_id_list) != len(set(visual_asset_id_list)):
                errors.append("visual_source_profile.source_artifacts.asset_id重复")
            visual_source_asset_ids = set(visual_asset_id_list)

            palette = visual_profile.get("palette")
            if not isinstance(palette, list) or not palette or not all(
                isinstance(item, dict) for item in palette
            ):
                errors.append("visual_source_profile.palette必须为非空对象列表")
                palette = []
            palette_roles: list[str] = []
            for index, color in enumerate(palette):
                label = f"visual_source_profile.palette[{index}]"
                _reject_unknown_fields(color, V25_PALETTE_FIELDS, label, errors)
                role = str(color.get("role") or "").strip()
                palette_roles.append(role)
                if not role:
                    errors.append(f"{label}.role为空")
                if not re.fullmatch(r"[0-9A-Fa-f]{6}", str(color.get("hex") or "")):
                    errors.append(f"{label}.hex必须为6位十六进制色值")
                if not _minimum_effective_text(
                    color.get("source_basis"), minimum=6, unique_minimum=3
                ):
                    errors.append(f"{label}.source_basis最低有效内容不足")
            if len(palette_roles) != len(set(palette_roles)):
                errors.append("visual_source_profile.palette.role重复")
            for field in (
                "image_style", "shape_language", "typography_tone", "fact_boundary"
            ):
                if not _minimum_effective_text(
                    visual_profile.get(field), minimum=14, unique_minimum=6
                ):
                    errors.append(f"visual_source_profile.{field}最低有效内容不足")
            if not _nonempty_string_list(visual_profile.get("consistency_rules")):
                errors.append("visual_source_profile.consistency_rules必须为非空字符串列表")
        binding = lesson.get("lesson_plan_binding")
        scope_projection = lesson.get("lesson_plan_scope")
        if not isinstance(binding, dict):
            errors.append("v2课程数据缺lesson_plan_binding（G1教案锁）")
        if not isinstance(scope_projection, dict):
            errors.append("v2课程数据缺lesson_plan_scope（G1范围投影）")
        _reject_unknown_fields(binding, V2_BINDING_FIELDS, "lesson_plan_binding", errors)
        _reject_unknown_fields(scope_projection, V2_SCOPE_FIELDS, "lesson_plan_scope", errors)
        _reject_unknown_fields(lesson.get("book_unit"), V2_BOOK_UNIT_FIELDS, "book_unit", errors)
        _reject_unknown_fields(lesson.get("text_contract"), V2_TEXT_CONTRACT_FIELDS, "text_contract", errors)
        _reject_unknown_fields(lesson.get("kp_scope"), V2_KP_SCOPE_FIELDS, "kp_scope", errors)
        for index, deferred in enumerate((lesson.get("kp_scope") or {}).get("deferred") or []):
            _reject_unknown_fields(deferred, V2_DEFERRED_FIELDS, f"kp_scope.deferred[{index}]", errors)
        for index, objective in enumerate(lesson.get("objectives") or []):
            _reject_unknown_fields(objective, V2_OBJECTIVE_FIELDS, f"objectives[{index}]", errors)
        for index, relation in enumerate(lesson.get("relations") or []):
            _reject_unknown_fields(relation, V2_RELATION_FIELDS, f"relations[{index}]", errors)
        if isinstance(binding, dict):
            lock_path_value = str(binding.get("path") or "").strip()
            lock_sha = str(binding.get("sha256") or "").strip()
            lock_path = Path(lock_path_value)
            if lock_path.is_absolute():
                errors.append("lesson_plan_binding.path必须使用项目根相对路径")
                lock_path = root / "__invalid_absolute_binding__"
            else:
                lock_path = (root / lock_path).resolve()
                try:
                    lock_path.relative_to(root.resolve())
                except ValueError:
                    errors.append("lesson_plan_binding.path越出项目根")
                    lock_path = root / "__invalid_escaped_binding__"
            if not lock_path_value or not lock_path.is_file():
                errors.append(f"lesson_plan_binding.path不存在: {lock_path_value}")
            elif hashlib.sha256(lock_path.read_bytes()).hexdigest() != lock_sha:
                errors.append("lesson_plan_binding.sha256与当前G1锁不一致")
            else:
                try:
                    plan_lock = json.loads(lock_path.read_text(encoding="utf-8"))
                    from validate_lesson_plan import validate as validate_lesson_plan  # noqa: E402

                    upstream_errors, _ = validate_lesson_plan(plan_lock, root=root)
                except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                    errors.append(f"G1上游无效: {exc}")
                else:
                    errors.extend(f"G1上游无效: {error}" for error in upstream_errors)
                    if plan_lock.get("lesson_id") != lesson.get("lesson_id"):
                        errors.append("lesson_id与G1教案锁不一致")
                    approved_contract = plan_lock.get("contract") or {}

        if approved_contract is not None and isinstance(scope_projection, dict):
            approved_objectives = approved_contract.get("objectives") or []
            approved_knowledge = approved_contract.get("knowledge_items") or []
            approved_questions = approved_contract.get("questions") or []
            approved_stages = approved_contract.get("stages") or []
            approved_stage_order = [item.get("id") for item in approved_stages]
            approved_stage_ids = set(approved_stage_order)
            approved_stage_to_objectives = {
                str(item.get("id")): set(item.get("objective_refs") or [])
                for item in approved_stages
            }
            approved_stage_to_kids = {
                str(item.get("id")): set(item.get("kid_refs") or [])
                for item in approved_stages
            }
            approved_teachable_kids = {
                item.get("kid")
                for item in approved_knowledge
                if item.get("status") in {"must_teach", "retrieve_prior"}
            }
            approved_kid_to_kps = {
                str(item.get("kid")): set(item.get("kp_ids") or [])
                for item in approved_knowledge
                if item.get("status") in {"must_teach", "retrieve_prior"}
            }
            approved_objective_to_kps = {
                str(item.get("id")): set().union(*(
                    approved_kid_to_kps.get(str(kid), set())
                    for kid in item.get("kid_refs") or []
                ))
                for item in approved_objectives
            }
            expected_scope = {
                "objective_ids": {item.get("id") for item in approved_objectives},
                "knowledge_ids": approved_teachable_kids,
                "deferred_ids": {item.get("kid") for item in approved_knowledge if item.get("status") == "defer"},
                "question_ids": {item.get("id") for item in approved_questions},
            }
            for field, expected in expected_scope.items():
                actual = set(scope_projection.get(field) or [])
                if actual != expected:
                    errors.append(f"lesson_plan_scope.{field}与G1教案漂移: 期望{sorted(expected)}，实际{sorted(actual)}")
            if list(scope_projection.get("stage_ids") or []) != approved_stage_order:
                errors.append(
                    "lesson_plan_scope.stage_ids与G1阶段顺序漂移: "
                    f"期望{approved_stage_order}，实际{list(scope_projection.get('stage_ids') or [])}"
                )
            from validate_lesson_plan import canonical_json_sha256  # noqa: E402

            expected_contract_sha = canonical_json_sha256(approved_contract)
            if scope_projection.get("contract_sha256") != expected_contract_sha:
                errors.append("lesson_plan_scope.contract_sha256与G1教案合同漂移")
            expected_total_minutes = approved_contract.get("total_minutes")
            if scope_projection.get("total_minutes") != expected_total_minutes:
                errors.append(
                    "lesson_plan_scope.total_minutes与G1教案漂移: "
                    f"期望{expected_total_minutes}，实际{scope_projection.get('total_minutes')}"
                )
            expected_closing_mode = approved_contract.get("closing_mode")
            if scope_projection.get("closing_mode") != expected_closing_mode:
                errors.append("lesson_plan_scope.closing_mode与G1教案漂移")

            approved_objective_map = {item.get("id"): item for item in approved_objectives}
            lesson_objective_map = {item.get("id"): item for item in lesson.get("objectives") or []}
            for oid, objective in approved_objective_map.items():
                current = lesson_objective_map.get(oid)
                if current is None:
                    errors.append(f"G2缺少G1目标: {oid}")
                elif current.get("statement") != objective.get("statement"):
                    errors.append(f"目标陈述漂移: {oid}")
                elif set(current.get("kp_refs") or []) != approved_objective_to_kps.get(str(oid), set()):
                    errors.append(f"G1批准的KID→KP映射漂移: 目标{oid}")
            if set(lesson_objective_map) != set(approved_objective_map):
                errors.append("G2目标ID集合与G1不一致")
            approved_question_texts = [item.get("text") for item in approved_questions]
            if lesson.get("three_questions") != approved_question_texts:
                errors.append("贯穿问题漂移：three_questions与G1批准文本不一致")

    # 1b. 教学目标（全课指导：先于 pages 存在，每条可归因、可取证）
    objectives = lesson.get("objectives") or []
    if not isinstance(objectives, list):
        errors.append("objectives必须为对象列表")
        objectives = []
    if not objectives:
        errors.append("objectives 为空（教学目标是全课指导，必须显式声明——目标先行）")
    seen_obj_ids = set()
    for i, obj in enumerate(objectives):
        if not isinstance(obj, dict):
            errors.append(f"objective #{i}: 必须为对象")
            continue
        oid = obj.get("id", f"#{i}")
        if oid in seen_obj_ids:
            errors.append(f"objective {oid}: id 重复")
        seen_obj_ids.add(oid)
        if not (obj.get("dimension") or "").strip():
            errors.append(f"objective {oid}: 缺 dimension（素养维度）")
        if len((obj.get("statement") or "").strip()) < 20:
            errors.append(f"objective {oid}: statement 过短或为空（不得以抽象套话充当目标）")
        for node in obj.get("nodes") or []:
            if node not in NODE_IDS:
                errors.append(f"objective {oid}: 机制节点非法: {node}")
        if not (obj.get("nodes") or []):
            errors.append(f"objective {oid}: 未绑定当前备课目标框架的机制节点")
        if not (obj.get("evidence_pages") or []):
            errors.append(f"objective {oid}: 未声明证据页（目标必须可取证）")

    # 1. 文本契约
    contract = lesson["text_contract"]
    for field in ("source_path", "source_sha256", "canonical_lines"):
        if not contract.get(field):
            errors.append(f"text_contract.{field} 为空（P-02/P-11：原文必须有唯一可信源绑定）")
    canonical_values = contract.get("canonical_lines")
    if is_v2 and not _nonempty_string_list(canonical_values):
        errors.append("canonical_lines必须为非空字符串列表")
        canonical_values = []
    if is_v2 and isinstance(canonical_values, list):
        normalized_lines = [re.sub(r"\s+", "", line) for line in canonical_values if isinstance(line, str)]
        if any(len(line) < 2 for line in normalized_lines):
            errors.append("canonical_lines每项归一化后至少含2个字符")
        if len(normalized_lines) != len(set(normalized_lines)):
            errors.append("canonical_lines不得含重复原文行")
    if contract.get("source_path"):
        source_value = Path(contract["source_path"])
        if source_value.is_absolute():
            errors.append("text_contract.source_path必须使用项目根相对路径")
            source = root / "__invalid_absolute_source__"
        else:
            source = (root / source_value).resolve()
            try:
                source.relative_to(root.resolve())
            except ValueError:
                errors.append("text_contract.source_path越出项目根")
                source = root / "__invalid_escaped_source__"
        if not source.exists():
            errors.append(f"text_contract.source_path 不存在: {contract['source_path']}")
        elif contract.get("source_sha256"):
            source_bytes = source.read_bytes()
            actual = hashlib.sha256(source_bytes).hexdigest()
            if actual != contract["source_sha256"]:
                errors.append("text_contract.source_sha256 与实际文件不匹配（原文漂移）")
            try:
                source_text = source_bytes.decode("utf-8")
            except UnicodeDecodeError as exc:
                errors.append(f"text_contract.source_path不是可核对UTF-8文本: {exc}")
            else:
                normalized_source = _normalize_source_anchor(source_text)
                if is_v2:
                    missing_lines = [
                        line for line in canonical_values or []
                        if _normalize_source_anchor(str(line)) not in normalized_source
                    ]
                    if missing_lines:
                        errors.append(f"canonical_lines未出现在绑定文本源: {missing_lines[:2]}")

    # 2. K1 知识绑定
    card_kps: set[str] = set()
    for card_id in lesson["book_unit"].get("card_refs", []):
        card = resolve_card(card_id, root=root)
        if card is None:
            errors.append(f"card_ref 无法解析: {card_id}")
        else:
            card_kps |= card_kp_ids(card)
    unit_ref = lesson["book_unit"].get("unit_ref")
    if unit_ref and not list((root / "work/knowledge").glob(f"*/units/{unit_ref}*.md")):
        errors.append(f"unit_ref 无法解析: {unit_ref}")
    scope = lesson["kp_scope"]
    for kp in scope.get("kp_ids", []):
        if kp not in card_kps:
            errors.append(f"kp_scope 的 {kp} 未解析到引用卡片")
    stats["kp_scope"] = len(scope.get("kp_ids", []))
    for deferred in scope.get("deferred", []):
        if not str(deferred.get("reason") or "").strip():
            errors.append(f"deferred 项 {deferred.get('kp_id')} 缺理由")
    stats["deferred"] = len(scope.get("deferred", []))
    if not scope.get("kp_ids"):
        errors.append("kp_scope.kp_ids 为空（K1/N-01：教什么必须以知识卡界定）")
    if is_v2 and approved_contract is not None:
        approved_kps = set().union(*approved_kid_to_kps.values()) if approved_kid_to_kps else set()
        actual_kps = set(scope.get("kp_ids") or [])
        if actual_kps != approved_kps:
            errors.append(
                f"G1批准的KID→KP映射漂移: 期望{sorted(approved_kps)}，实际{sorted(actual_kps)}"
            )

    # 3. K4 关系边
    for relation in lesson.get("relations") or []:
        if not resolve_card(relation.get("card_id", ""), root=root):
            errors.append(f"relations 的 card_id 无法解析: {relation.get('card_id')}")
        if not str(relation.get("relation") or "").strip():
            errors.append("relations 项缺 relation 说明")

    # 4. 页面合同
    sys.path.insert(0, str(ROOT / "scripts/checks"))
    from check_trace_evidence import scan_lesson  # noqa: E402

    pages = lesson["pages"]
    stats["pages"] = len(pages)
    page_id_list = [p.get("page_id") for p in pages]
    page_ids = set(page_id_list)
    page_positions = {
        page_id: index
        for index, page_id in enumerate(page_id_list)
        if isinstance(page_id, str) and page_id.strip()
    }
    for duplicate in sorted(
        {value for value in page_id_list if value is not None and page_id_list.count(value) > 1},
        key=str,
    ):
        errors.append(f"page_id重复: {duplicate}")
    page_objective_ids: set[str] = set()
    page_lesson_kids: set[str] = set()
    page_stage_ids: set[str] = set()
    last_stage_position = -1
    approved_objective_ids = {
        item.get("id") for item in (approved_contract or {}).get("objectives") or []
    }
    stage_positions = {stage_id: index for index, stage_id in enumerate(approved_stage_order)}

    # 教学目标的交叉校验（需 card_kps 与 page_ids）
    for obj in lesson.get("objectives") or []:
        oid = obj.get("id", "?")
        for kp in obj.get("kp_refs") or []:
            if kp not in card_kps:
                errors.append(f"objective {oid}: kp_ref 未解析到引用卡片: {kp}")
        for pid in obj.get("evidence_pages") or []:
            if pid not in page_ids:
                errors.append(f"objective {oid}: 证据页不存在: {pid}")
    findings = scan_lesson(lesson)
    stats["boilerplate"] = len(findings)
    canonical = contract.get("canonical_lines") or []
    banned: list[str] = []
    if enforcement_config is not None:
        config = enforcement_config
        banned = config.get("frontstage_banned_v6", []) + config.get("frontstage_banned_v5", [])
    else:
        config_path = root / "work/principles/enforcement_config.json"
        if config_path.exists():
            config = json.loads(config_path.read_text(encoding="utf-8"))
            banned = config.get("frontstage_banned_v6", []) + config.get("frontstage_banned_v5", [])

    for page in pages:
        pid = page.get("page_id", "?")
        if not isinstance(pid, str) or not pid.strip():
            errors.append("页面page_id必须为非空字符串")
        minutes = page.get("minutes")
        if not isinstance(minutes, (int, float)) or isinstance(minutes, bool) or minutes <= 0:
            errors.append(f"{pid}: minutes必须为正数")
        if is_v2:
            _reject_unknown_fields(
                page,
                V21_PAGE_FIELDS if is_v21_plus else V20_PAGE_FIELDS,
                f"{pid}: 页面",
                errors,
            )
            _reject_unknown_fields(page.get("next_use_ref"), V2_NEXT_USE_FIELDS, f"{pid}: next_use_ref", errors)
            _reject_unknown_fields(
                page.get("script"),
                V22_SCRIPT_FIELDS if is_v22_plus else (V21_SCRIPT_FIELDS if is_v21 else V20_SCRIPT_FIELDS),
                f"{pid}: script",
                errors,
            )
            if isinstance(page.get("literary_object"), dict):
                _reject_unknown_fields(
                    page["literary_object"],
                    V2_LITERARY_OBJECT_FIELDS,
                    f"{pid}: literary_object",
                    errors,
                )
            stage_id = page.get("stage_id")
            if stage_id not in approved_stage_ids:
                errors.append(f"{pid}: stage_id未获G1批准: {stage_id}")
            else:
                page_stage_ids.add(stage_id)
                stage_position = stage_positions[stage_id]
                if stage_position < last_stage_position:
                    errors.append(f"{pid}: 页面阶段顺序倒灌，{stage_id}出现在已推进阶段之后")
                last_stage_position = max(last_stage_position, stage_position)

            v26_presentation_role = str(
                ((page.get("slide_design") or {}).get("presentation_role") or "")
                if isinstance(page.get("slide_design"), dict)
                else ""
            ).strip()
            is_structural_page = is_v26 and v26_presentation_role in {
                "PG01", "PG02", "PG03",
            }
            objective_ids = page.get("objective_ids")
            lesson_kids = page.get("lesson_kids")
            if is_structural_page:
                if not _string_list(objective_ids):
                    errors.append(f"{pid}: 定位结构页objective_ids必须为字符串列表")
                    objective_ids = []
                elif objective_ids:
                    errors.append(f"{pid}: 定位结构页不得伪挂objective_ids")
                if not _string_list(lesson_kids):
                    errors.append(f"{pid}: 定位结构页lesson_kids必须为字符串列表")
                    lesson_kids = []
                elif lesson_kids:
                    errors.append(f"{pid}: 定位结构页不得伪挂lesson_kids")
            else:
                if not _nonempty_string_list(objective_ids):
                    errors.append(f"{pid}: objective_ids必须为非空字符串列表")
                    objective_ids = []
                if not _nonempty_string_list(lesson_kids):
                    errors.append(f"{pid}: lesson_kids必须为非空字符串列表")
                    lesson_kids = []
            for oid in objective_ids:
                if oid not in approved_objective_ids:
                    errors.append(f"{pid}: objective_id未获G1批准: {oid}")
                else:
                    page_objective_ids.add(oid)
                    if stage_id in approved_stage_ids and oid not in approved_stage_to_objectives.get(str(stage_id), set()):
                        errors.append(f"{pid}: objective_id不属于获批阶段{stage_id}: {oid}")
            for kid in lesson_kids:
                if kid not in approved_teachable_kids:
                    errors.append(f"{pid}: lesson_kid未获G1批准为必教/旧知: {kid}")
                else:
                    page_lesson_kids.add(kid)
                    if stage_id in approved_stage_ids and kid not in approved_stage_to_kids.get(str(stage_id), set()):
                        errors.append(f"{pid}: lesson_kid不属于获批阶段{stage_id}: {kid}")

            event_requirements = LEGACY_EVENT_REQUIREMENTS
            event_allows_no_primary = False
            event_type = ""
            if is_v21_plus:
                payload = page.get("knowledge_payload")
                if is_structural_page:
                    if not isinstance(payload, list) or not all(
                        isinstance(item, dict) for item in payload
                    ):
                        errors.append(f"{pid}: 定位结构页knowledge_payload必须为对象列表")
                        payload = []
                    elif payload:
                        errors.append(f"{pid}: 定位结构页不得伪造knowledge_payload")
                elif not isinstance(payload, list) or not payload or not all(
                    isinstance(item, dict) for item in payload
                ):
                    errors.append(f"{pid}: knowledge_payload必须为非空对象列表")
                    payload = []
                payload_kids: set[str] = set()
                page_roles = set(category_registry.get("knowledge_page_roles") or [])
                for index, item in enumerate(payload):
                    _reject_unknown_fields(
                        item,
                        V21_KNOWLEDGE_PAYLOAD_FIELDS,
                        f"{pid}: knowledge_payload[{index}]",
                        errors,
                    )
                    kid = str(item.get("kid") or "").strip()
                    scope_text = item.get("scope")
                    page_role = str(item.get("page_role") or "").strip()
                    if not kid:
                        errors.append(f"{pid}: knowledge_payload[{index}].kid为空")
                    else:
                        payload_kids.add(kid)
                    if not _minimum_effective_text(scope_text, minimum=10, unique_minimum=5):
                        errors.append(f"{pid}: knowledge_payload[{index}].scope最低有效内容不足")
                    if page_role not in page_roles:
                        errors.append(f"{pid}: knowledge_payload[{index}].page_role未注册: {page_role}")
                if payload_kids != set(lesson_kids):
                    errors.append(
                        f"{pid}: knowledge_payload与lesson_kids不一致: "
                        f"payload={sorted(payload_kids)} lesson_kids={sorted(set(lesson_kids))}"
                    )

                activity = page.get("activity_contract")
                if not isinstance(activity, dict):
                    errors.append(f"{pid}: activity_contract必须为对象")
                    activity = {}
                _reject_unknown_fields(
                    activity,
                    V23_ACTIVITY_FIELDS if is_v23_plus else V21_ACTIVITY_FIELDS,
                    f"{pid}: activity_contract",
                    errors,
                )
                if is_v23_plus:
                    event_type = str(activity.get("event_type") or "").strip()
                    event_map = {
                        str(item.get("id")): item
                        for item in category_registry.get("event_types") or []
                        if isinstance(item, dict)
                    }
                    event_definition = event_map.get(event_type)
                    if event_definition is None:
                        errors.append(f"{pid}: activity_contract.event_type未注册: {event_type}")
                        event_requirements = LEGACY_EVENT_REQUIREMENTS
                    else:
                        event_requirements = set(event_definition.get("requires") or [])
                        event_allows_no_primary = bool(
                            event_definition.get("allows_no_primary_activity")
                        )
                activity_ids = _registered_ids(category_registry, "activity_types")
                teacher_ids = _registered_ids(category_registry, "teacher_move_types")
                learner_ids = _registered_ids(category_registry, "learner_action_types")
                participation_ids = _registered_ids(category_registry, "participation_types")
                artifact_ids = _registered_ids(category_registry, "artifact_types")
                sensory_ids = _registered_ids(category_registry, "sensory_channel_types")
                feedback_ids = _registered_ids(category_registry, "feedback_types")
                primary_type = str(activity.get("primary_type") or "").strip()
                if primary_type:
                    if primary_type not in activity_ids:
                        errors.append(f"{pid}: activity_contract.primary_type未注册: {primary_type}")
                elif not (is_v23_plus and event_allows_no_primary):
                    errors.append(f"{pid}: activity_contract.primary_type未注册: {primary_type}")
                secondary_types = _registered_string_list(
                    activity.get("secondary_types"), activity_ids,
                    f"{pid}: activity_contract.secondary_types", errors, allow_empty=True,
                )
                if primary_type and primary_type in secondary_types:
                    errors.append(f"{pid}: 主辅活动类别重复: {primary_type}")
                _registered_string_list(
                    activity.get("teacher_move_types"), teacher_ids,
                    f"{pid}: activity_contract.teacher_move_types", errors,
                )
                _registered_string_list(
                    activity.get("learner_action_types"), learner_ids,
                    f"{pid}: activity_contract.learner_action_types", errors,
                )
                participation_type = str(activity.get("participation_type") or "").strip()
                if participation_type not in participation_ids:
                    errors.append(f"{pid}: activity_contract.participation_type未注册: {participation_type}")
                artifact_type = str(activity.get("artifact_type") or "").strip()
                if artifact_type:
                    if artifact_type not in artifact_ids:
                        errors.append(f"{pid}: activity_contract.artifact_type未注册: {artifact_type}")
                elif not (is_v23_plus and "artifact" not in event_requirements):
                    errors.append(f"{pid}: activity_contract.artifact_type未注册: {artifact_type}")
                _registered_string_list(
                    activity.get("sensory_channel_types"), sensory_ids,
                    f"{pid}: activity_contract.sensory_channel_types", errors,
                )
                _registered_string_list(
                    activity.get("feedback_types"), feedback_ids,
                    f"{pid}: activity_contract.feedback_types", errors,
                    allow_empty=is_v23_plus and "feedback" not in event_requirements,
                )
                for field in ("selection_reason", "knowledge_fit", "experience_fit"):
                    if not _minimum_effective_text(activity.get(field), minimum=16, unique_minimum=7):
                        errors.append(f"{pid}: activity_contract.{field}最低有效内容不足")
                selection_reason = str(activity.get("selection_reason") or "")
                if "本页真正的断点是" in selection_reason and "所以以" in selection_reason:
                    errors.append(f"{pid}: activity_contract.selection_reason仍是统一生成模板")
                knowledge_fit = str(activity.get("knowledge_fit") or "")
                if "页面只通过" in knowledge_fit and "处理这些内容" in knowledge_fit:
                    errors.append(f"{pid}: activity_contract.knowledge_fit仍是统一生成模板")
                experience_fit = str(activity.get("experience_fit") or "")
                if (
                    "学生先感到" in experience_fit
                    and "再围绕" in experience_fit
                    and "体验不靠统一表态制造" in experience_fit
                ):
                    errors.append(f"{pid}: activity_contract.experience_fit仍是统一生成模板")

                experience = page.get("student_experience")
                if not isinstance(experience, dict):
                    errors.append(f"{pid}: student_experience必须为对象")
                    experience = {}
                _reject_unknown_fields(experience, V21_EXPERIENCE_FIELDS, f"{pid}: student_experience", errors)
                for field in V21_EXPERIENCE_FIELDS:
                    if not _minimum_effective_text(experience.get(field), minimum=12, unique_minimum=6):
                        errors.append(f"{pid}: student_experience.{field}最低有效内容不足")

                slide_design = page.get("slide_design")
                if not isinstance(slide_design, dict):
                    errors.append(f"{pid}: slide_design必须为对象")
                    slide_design = {}
                _reject_unknown_fields(
                    slide_design,
                    (
                        V26_SLIDE_DESIGN_FIELDS
                        if is_v26
                        else V25_SLIDE_DESIGN_FIELDS
                        if is_v25
                        else V24_SLIDE_DESIGN_FIELDS
                        if is_v24
                        else V22_SLIDE_DESIGN_FIELDS
                        if is_v22_plus
                        else V21_SLIDE_DESIGN_FIELDS
                    ),
                    f"{pid}: slide_design",
                    errors,
                )
                if not is_v24_plus:
                    layout_ids = _registered_ids(category_registry, "layout_types")
                    layout_type = str(slide_design.get("layout_type") or "").strip()
                    if layout_type not in layout_ids:
                        errors.append(f"{pid}: slide_design.layout_type未注册: {layout_type}")
                frontstage_elements = slide_design.get("frontstage_elements")
                state_ids: set[str] = set()
                state_trigger_by_id: dict[str, str] = {}
                has_calibration_elements = False
                if is_v22_plus:
                    allowed_state_triggers = (
                        V23_STATE_TRIGGERS if is_v23_plus else V22_STATE_TRIGGERS
                    )
                    trigger_rank = V23_TRIGGER_RANK if is_v23_plus else V22_TRIGGER_RANK
                    if not isinstance(frontstage_elements, list) or not frontstage_elements or not all(
                        isinstance(item, dict) for item in frontstage_elements
                    ):
                        errors.append(f"{pid}: slide_design.frontstage_elements必须为非空对象列表")
                        frontstage_elements = []
                    element_ids: list[str] = []
                    element_roles: dict[str, str] = {}
                    element_texts: dict[str, str] = {}
                    for index, item in enumerate(frontstage_elements):
                        _reject_unknown_fields(
                            item,
                            V22_FRONTSTAGE_ELEMENT_FIELDS,
                            f"{pid}: frontstage_elements[{index}]",
                            errors,
                        )
                        element_id = str(item.get("id") or "").strip()
                        element_text = str(item.get("text") or "").strip()
                        element_role = str(item.get("role") or "").strip()
                        if not re.fullmatch(r"E\d{2}", element_id):
                            errors.append(f"{pid}: frontstage_elements[{index}].id必须为E两位数字")
                        element_ids.append(element_id)
                        if not _minimum_effective_text(element_text, minimum=2, unique_minimum=2):
                            errors.append(f"{pid}: frontstage_elements[{index}].text最低有效内容不足")
                        if element_role not in V22_FRONTSTAGE_ROLES:
                            errors.append(f"{pid}: frontstage_elements[{index}].role非法: {element_role}")
                        element_roles[element_id] = element_role
                        element_texts[element_id] = element_text
                    has_calibration_elements = "calibration" in set(element_roles.values())
                    if len(element_ids) != len(set(element_ids)):
                        errors.append(f"{pid}: frontstage_elements.id重复")

                    states = slide_design.get("information_states")
                    if not isinstance(states, list) or not states or not all(isinstance(item, dict) for item in states):
                        errors.append(f"{pid}: slide_design.information_states必须为非空对象列表")
                        states = []
                    first_seen: set[str] = set()
                    ordered_state_ids: list[str] = []
                    for index, state in enumerate(states):
                        _reject_unknown_fields(
                            state,
                            V22_INFORMATION_STATE_FIELDS,
                            f"{pid}: information_states[{index}]",
                            errors,
                        )
                        state_id = str(state.get("id") or "").strip()
                        expected_state_id = f"B{index}"
                        if state_id != expected_state_id:
                            errors.append(f"{pid}: information_states[{index}].id应为{expected_state_id}")
                        ordered_state_ids.append(state_id)
                        trigger = str(state.get("enter_trigger") or "").strip()
                        state_trigger_by_id[state_id] = trigger
                        if trigger not in allowed_state_triggers:
                            errors.append(f"{pid}: information_states[{index}].enter_trigger非法: {trigger}")
                        if index == 0 and trigger != "page_enter":
                            errors.append(f"{pid}: B0必须由page_enter进入")
                        visible_ids = state.get("visible_element_ids")
                        if not _nonempty_string_list(visible_ids):
                            errors.append(f"{pid}: information_states[{index}].visible_element_ids必须为非空字符串列表")
                            visible_ids = []
                        if len(visible_ids) != len(set(visible_ids)):
                            errors.append(f"{pid}: information_states[{index}].visible_element_ids重复")
                        for element_id in visible_ids:
                            if element_id not in set(element_ids):
                                errors.append(f"{pid}: information_states[{index}]引用未知元素: {element_id}")
                        if index == 0:
                            for element_id in visible_ids:
                                if element_roles.get(element_id) in {"calibration", "feedback"}:
                                    errors.append(f"{pid}: calibration元素不得在B0可见: {element_id}")
                                text = element_texts.get(element_id, "")
                                if text and text not in str(page.get("first_view_contract") or ""):
                                    errors.append(f"{pid}: B0元素未进入first_view_contract: {element_id}")
                        newly_visible = set(visible_ids) - first_seen
                        if trigger in {"page_enter", "after_instruction", "after_prior_artifact_retrieved"}:
                            for element_id in newly_visible:
                                if element_roles.get(element_id) in {"calibration", "feedback"}:
                                    errors.append(f"{pid}: 答案性元素首次可见过早: {element_id}")
                        first_seen.update(visible_ids)
                    state_ids = set(ordered_state_ids)
                    missing_elements = set(element_ids) - first_seen
                    if missing_elements:
                        errors.append(f"{pid}: 前台元素从未进入任何信息状态: {sorted(missing_elements)}")
                    if is_v24_plus:
                        if is_v26:
                            presentation_role = str(
                                slide_design.get("presentation_role") or ""
                            ).strip()
                            presentation_role_ids = _registered_ids(
                                category_registry, "presentation_role_types"
                            )
                            if presentation_role not in presentation_role_ids:
                                errors.append(
                                    f"{pid}: slide_design.presentation_role未注册: "
                                    f"{presentation_role}"
                                )
                            if not _minimum_effective_text(
                                slide_design.get("role_rationale"),
                                minimum=16,
                                unique_minimum=7,
                            ):
                                errors.append(
                                    f"{pid}: slide_design.role_rationale最低有效内容不足"
                                )

                            support_link = slide_design.get("support_link")
                            if presentation_role == "PG05":
                                if not isinstance(support_link, dict):
                                    errors.append(f"{pid}: 支撑页缺support_link触发—返回合同")
                                else:
                                    _reject_unknown_fields(
                                        support_link,
                                        V26_SUPPORT_LINK_FIELDS,
                                        f"{pid}: support_link",
                                        errors,
                                    )
                                    for field in ("trigger", "return_use"):
                                        if not _minimum_effective_text(
                                            support_link.get(field),
                                            minimum=12,
                                            unique_minimum=6,
                                        ):
                                            errors.append(
                                                f"{pid}: support_link.{field}最低有效内容不足"
                                            )
                                    source_ref = str(
                                        support_link.get("source_ref") or ""
                                    ).strip()
                                    return_ref = str(
                                        support_link.get("return_ref") or ""
                                    ).strip()
                                    current_position = page_positions.get(pid, -1)
                                    if source_ref != "lesson_entry":
                                        if source_ref not in page_ids:
                                            errors.append(
                                                f"{pid}: support_link.source_ref不存在: {source_ref}"
                                            )
                                        elif page_positions.get(source_ref, current_position) >= current_position:
                                            errors.append(
                                                f"{pid}: support_link.source_ref必须指向此前页面或lesson_entry"
                                            )
                                    if return_ref not in page_ids:
                                        errors.append(
                                            f"{pid}: support_link.return_ref不存在: {return_ref}"
                                        )
                                    elif page_positions.get(return_ref, current_position) <= current_position:
                                        errors.append(
                                            f"{pid}: support_link.return_ref必须指向后续页面"
                                        )
                            elif support_link is not None:
                                errors.append(f"{pid}: 非支撑页不得填写support_link")

                        semantic_text_requirements = {
                            "semantic_unit": (8, 5),
                            "organizing_intention": (16, 7),
                            "boundary_rationale": (16, 7),
                        }
                        for field, (minimum, unique_minimum) in semantic_text_requirements.items():
                            if not _minimum_effective_text(
                                slide_design.get(field),
                                minimum=minimum,
                                unique_minimum=unique_minimum,
                            ):
                                errors.append(f"{pid}: slide_design.{field}最低有效内容不足")

                        content_object_ids = _registered_ids(
                            category_registry, "content_object_types"
                        )
                        display_constraint_ids = _registered_ids(
                            category_registry, "display_constraint_types"
                        )
                        layout_operation_ids = _registered_ids(
                            category_registry, "layout_operation_types"
                        )
                        semantic_relation_ids = _registered_ids(
                            category_registry, "semantic_relation_types"
                        )
                        _registered_string_list(
                            slide_design.get("content_object_types"),
                            content_object_ids,
                            f"{pid}: slide_design.content_object_types",
                            errors,
                        )
                        _registered_string_list(
                            slide_design.get("display_constraints"),
                            display_constraint_ids,
                            f"{pid}: slide_design.display_constraints",
                            errors,
                        )
                        _registered_string_list(
                            slide_design.get("layout_operations"),
                            layout_operation_ids,
                            f"{pid}: slide_design.layout_operations",
                            errors,
                        )
                        if is_v26:
                            role_object_requirements = {
                                "PG01": {"CO09"},
                                "PG02": {"CO09"},
                                "PG03": {"CO09"},
                                "PG04": {"CO01", "CO02"},
                                "PG05": {"CO03", "CO05"},
                                "PG06": {"CO04"},
                                "PG07": {"CO06", "CO07"},
                                "PG08": {"CO08"},
                                "PG09": {"CO04"},
                            }
                            required_objects = role_object_requirements.get(
                                presentation_role, set()
                            )
                            actual_objects = set(
                                slide_design.get("content_object_types") or []
                            )
                            if presentation_role in {"PG01", "PG02", "PG03"} and (
                                actual_objects != {"CO09"}
                            ):
                                errors.append(
                                    f"{pid}: 定位结构页只能登记CO09课题与路径定位"
                                )
                            elif required_objects and not (
                                required_objects & actual_objects
                            ):
                                errors.append(
                                    f"{pid}: {presentation_role}缺少匹配内容对象，"
                                    f"至少需要{sorted(required_objects)}之一"
                                )

                        relations = slide_design.get("semantic_relations")
                        if not isinstance(relations, list) or not relations or not all(
                            isinstance(item, dict) for item in relations
                        ):
                            errors.append(
                                f"{pid}: slide_design.semantic_relations必须为非空对象列表"
                            )
                            relations = []
                        for index, relation in enumerate(relations):
                            label = f"{pid}: semantic_relations[{index}]"
                            _reject_unknown_fields(
                                relation, V24_SEMANTIC_RELATION_FIELDS, label, errors
                            )
                            relation_type = str(relation.get("type") or "").strip()
                            if relation_type not in semantic_relation_ids:
                                errors.append(f"{label}.type未注册: {relation_type}")
                            relation_elements = relation.get("element_ids")
                            if not _nonempty_string_list(relation_elements) or len(relation_elements) < 2:
                                errors.append(f"{label}.element_ids至少含两个元素")
                                relation_elements = []
                            for element_id in relation_elements:
                                if element_id not in set(element_ids):
                                    errors.append(f"{label}.element_ids引用未知元素: {element_id}")
                            if not _minimum_effective_text(
                                relation.get("rationale"), minimum=14, unique_minimum=6
                            ):
                                errors.append(f"{label}.rationale最低有效内容不足")

                        co_view_groups = slide_design.get("co_view_groups")
                        if not isinstance(co_view_groups, list) or not co_view_groups or not all(
                            isinstance(item, dict) for item in co_view_groups
                        ):
                            errors.append(
                                f"{pid}: slide_design.co_view_groups必须为非空对象列表"
                            )
                            co_view_groups = []
                        co_view_ids: list[str] = []
                        visible_sets = [
                            set(state.get("visible_element_ids") or [])
                            for state in states
                            if isinstance(state, dict)
                        ]
                        for index, group in enumerate(co_view_groups):
                            label = f"{pid}: co_view_groups[{index}]"
                            _reject_unknown_fields(
                                group, V24_CO_VIEW_GROUP_FIELDS, label, errors
                            )
                            group_id = str(group.get("id") or "").strip()
                            if not re.fullmatch(r"G\d{2}", group_id):
                                errors.append(f"{label}.id必须为G两位数字")
                            co_view_ids.append(group_id)
                            group_elements = group.get("element_ids")
                            if not _nonempty_string_list(group_elements):
                                errors.append(f"{label}.element_ids必须为非空字符串列表")
                                group_elements = []
                            for element_id in group_elements:
                                if element_id not in set(element_ids):
                                    errors.append(f"{label}.element_ids引用未知元素: {element_id}")
                            if group_elements and not any(
                                set(group_elements).issubset(visible) for visible in visible_sets
                            ):
                                errors.append(f"{label}未在任何信息状态中真正共视")
                            if not _minimum_effective_text(
                                group.get("rationale"), minimum=14, unique_minimum=6
                            ):
                                errors.append(f"{label}.rationale最低有效内容不足")
                        if len(co_view_ids) != len(set(co_view_ids)):
                            errors.append(f"{pid}: co_view_groups.id重复")

                        first_state_index: dict[str, int] = {}
                        for state_index, state in enumerate(states):
                            for element_id in state.get("visible_element_ids") or []:
                                first_state_index.setdefault(element_id, state_index)
                        must_stage = slide_design.get("must_stage")
                        if not isinstance(must_stage, list) or not all(
                            isinstance(item, dict) for item in must_stage
                        ):
                            errors.append(f"{pid}: slide_design.must_stage必须为对象列表")
                            must_stage = []
                        for index, staged in enumerate(must_stage):
                            label = f"{pid}: must_stage[{index}]"
                            _reject_unknown_fields(
                                staged, V24_MUST_STAGE_FIELDS, label, errors
                            )
                            staged_elements = staged.get("element_ids")
                            if not _nonempty_string_list(staged_elements):
                                errors.append(f"{label}.element_ids必须为非空字符串列表")
                                staged_elements = []
                            for element_id in staged_elements:
                                if element_id not in set(element_ids):
                                    errors.append(f"{label}.element_ids引用未知元素: {element_id}")
                                elif first_state_index.get(element_id, 0) == 0:
                                    errors.append(f"{label}声明分时元素却在B0已经可见: {element_id}")
                            if not _minimum_effective_text(
                                staged.get("rationale"), minimum=14, unique_minimum=6
                            ):
                                errors.append(f"{label}.rationale最低有效内容不足")

                        layers = slide_design.get("priority_layers")
                        if not isinstance(layers, list) or not layers or not all(
                            isinstance(item, dict) for item in layers
                        ):
                            errors.append(
                                f"{pid}: slide_design.priority_layers必须为非空对象列表"
                            )
                            layers = []
                        layered_elements: list[str] = []
                        for index, layer in enumerate(layers):
                            label = f"{pid}: priority_layers[{index}]"
                            _reject_unknown_fields(
                                layer, V24_PRIORITY_LAYER_FIELDS, label, errors
                            )
                            expected_level = f"L{index + 1}"
                            if layer.get("level") != expected_level:
                                errors.append(f"{label}.level应为{expected_level}")
                            layer_elements = layer.get("element_ids")
                            if not _nonempty_string_list(layer_elements):
                                errors.append(f"{label}.element_ids必须为非空字符串列表")
                                layer_elements = []
                            layered_elements.extend(layer_elements)
                            for element_id in layer_elements:
                                if element_id not in set(element_ids):
                                    errors.append(f"{label}.element_ids引用未知元素: {element_id}")
                            if not _minimum_effective_text(
                                layer.get("rationale"), minimum=12, unique_minimum=5
                            ):
                                errors.append(f"{label}.rationale最低有效内容不足")
                        if set(layered_elements) != set(element_ids) or len(layered_elements) != len(
                            set(layered_elements)
                        ):
                            errors.append(
                                f"{pid}: priority_layers必须恰好覆盖全部前台元素且不得重复"
                            )

                        continuity_anchor = slide_design.get("continuity_anchor")
                        if not _nonempty_string_list(continuity_anchor):
                            errors.append(
                                f"{pid}: slide_design.continuity_anchor必须为非空元素ID列表"
                            )
                            continuity_anchor = []
                        for element_id in continuity_anchor:
                            if element_id not in set(element_ids):
                                errors.append(
                                    f"{pid}: continuity_anchor引用未知元素: {element_id}"
                                )
                            elif not all(element_id in visible for visible in visible_sets):
                                errors.append(
                                    f"{pid}: continuity_anchor必须出现在每个信息状态: {element_id}"
                                )

                        density = slide_design.get("density_judgment")
                        if not isinstance(density, dict):
                            errors.append(f"{pid}: slide_design.density_judgment必须为对象")
                            density = {}
                        _reject_unknown_fields(
                            density, V24_DENSITY_FIELDS,
                            f"{pid}: density_judgment", errors,
                        )
                        for field in ("semantic_completeness", "readability_focus"):
                            if not _minimum_effective_text(
                                density.get(field), minimum=16, unique_minimum=7
                            ):
                                errors.append(
                                    f"{pid}: density_judgment.{field}最低有效内容不足；"
                                    "不得用固定条数或字数代替语义完整与可读性判断"
                                )
                        if density.get("decision") not in V24_DENSITY_DECISIONS:
                            errors.append(
                                f"{pid}: density_judgment.decision必须为retain_as_page"
                            )
                        if is_v25_plus:
                            physical_screens = slide_design.get("physical_screens")
                            if not isinstance(physical_screens, list) or not physical_screens or not all(
                                isinstance(item, dict) for item in physical_screens
                            ):
                                errors.append(
                                    f"{pid}: slide_design.physical_screens必须为非空对象列表"
                                )
                                physical_screens = []
                            state_map = {
                                str(state.get("id") or ""): list(state.get("visible_element_ids") or [])
                                for state in states
                                if isinstance(state, dict)
                            }
                            script_segments = (page.get("script") or {}).get("script_segments") or []
                            segment_ids_by_state: dict[str, list[str]] = {}
                            all_segment_ids: set[str] = set()
                            for segment in script_segments:
                                if not isinstance(segment, dict):
                                    continue
                                segment_id = str(segment.get("id") or "").strip()
                                segment_state = str(segment.get("state_id") or "").strip()
                                all_segment_ids.add(segment_id)
                                segment_ids_by_state.setdefault(segment_state, []).append(segment_id)
                            screen_state_ids: list[str] = []
                            for index, screen in enumerate(physical_screens):
                                label = f"{pid}: physical_screens[{index}]"
                                _reject_unknown_fields(
                                    screen, V25_PHYSICAL_SCREEN_FIELDS, label, errors
                                )
                                state_id = str(screen.get("state_id") or "").strip()
                                screen_state_ids.append(state_id)
                                expected_state_id = f"B{index}"
                                if state_id != expected_state_id:
                                    errors.append(f"{label}.state_id应为{expected_state_id}")
                                expected_screen_id = f"{pid}-{state_id}"
                                if screen.get("screen_id") != expected_screen_id:
                                    errors.append(f"{label}.screen_id应为{expected_screen_id}")
                                visible = screen.get("visible_element_ids")
                                if not _nonempty_string_list(visible):
                                    errors.append(f"{label}.visible_element_ids必须为非空字符串列表")
                                    visible = []
                                if list(visible) != state_map.get(state_id, []):
                                    errors.append(
                                        f"{label}.visible_element_ids必须与对应信息状态完全一致"
                                    )
                                for field in (
                                    "screen_function", "composition_blueprint", "reading_path",
                                    "spatial_proportions",
                                ):
                                    if not _minimum_effective_text(
                                        screen.get(field), minimum=14, unique_minimum=6
                                    ):
                                        errors.append(f"{label}.{field}最低有效内容不足")
                                image_plan = screen.get("image_plan")
                                if not isinstance(image_plan, dict):
                                    errors.append(f"{label}.image_plan必须为对象")
                                    image_plan = {}
                                _reject_unknown_fields(
                                    image_plan, V25_IMAGE_PLAN_FIELDS,
                                    f"{label}.image_plan", errors,
                                )
                                decision = str(image_plan.get("decision") or "").strip()
                                if decision not in V25_IMAGE_DECISIONS:
                                    errors.append(f"{label}.image_plan.decision非法: {decision}")
                                derivation_mode = str(
                                    image_plan.get("derivation_mode") or ""
                                ).strip()
                                if derivation_mode not in V25_DERIVATION_MODES:
                                    errors.append(
                                        f"{label}.image_plan.derivation_mode非法: {derivation_mode}"
                                    )
                                asset_refs = image_plan.get("asset_refs")
                                if not _string_list(asset_refs):
                                    errors.append(
                                        f"{label}.image_plan.asset_refs必须为字符串列表"
                                    )
                                    asset_refs = []
                                if len(asset_refs) != len(set(asset_refs)):
                                    errors.append(f"{label}.image_plan.asset_refs不得重复")
                                for asset_ref in asset_refs:
                                    if asset_ref not in visual_source_asset_ids:
                                        errors.append(
                                            f"{label}.image_plan.asset_refs引用未知视觉资产: {asset_ref}"
                                        )
                                if decision == "required" and (
                                    not asset_refs or derivation_mode == "none"
                                ):
                                    errors.append(
                                        f"{label}: required画面必须引用视觉来源并声明派生方式"
                                    )
                                if decision == "forbidden" and (
                                    asset_refs or derivation_mode != "none"
                                ):
                                    errors.append(f"{label}: forbidden画面不得引用图片资产")
                                for field in (
                                    "function", "content_brief", "style_brief", "placement",
                                    "visual_weight", "appearance_timing", "fact_boundary",
                                ):
                                    if not _minimum_effective_text(
                                        image_plan.get(field), minimum=10, unique_minimum=5
                                    ):
                                        errors.append(
                                            f"{label}.image_plan.{field}最低有效内容不足"
                                        )
                                segment_refs = screen.get("script_segment_refs")
                                if not _nonempty_string_list(segment_refs):
                                    errors.append(
                                        f"{label}.script_segment_refs必须为非空字符串列表"
                                    )
                                    segment_refs = []
                                unknown_segment_refs = set(segment_refs) - all_segment_ids
                                if unknown_segment_refs:
                                    errors.append(
                                        f"{label}.script_segment_refs引用未知片段: "
                                        f"{sorted(unknown_segment_refs)}"
                                    )
                                if list(segment_refs) != segment_ids_by_state.get(state_id, []):
                                    errors.append(
                                        f"{label}.script_segment_refs必须恰好覆盖该状态的剧本片段"
                                    )
                            if screen_state_ids != list(state_map):
                                errors.append(
                                    f"{pid}: physical_screens必须按顺序恰好覆盖全部信息状态"
                                )
                    canonical_state = canonical_information_state(frontstage_elements, states)
                    if str(page.get("information_state") or "").strip() != canonical_state:
                        errors.append(f"{pid}: information_state与结构化信息状态不一致")
                elif not _nonempty_string_list(frontstage_elements):
                    errors.append(f"{pid}: slide_design.frontstage_elements必须为非空字符串列表")
                required_design_text_fields = (
                    ("information_hierarchy", "reveal_sequence")
                    if is_v24_plus
                    else ("spatial_plan", "information_hierarchy", "reveal_sequence")
                )
                for field in required_design_text_fields:
                    if not _minimum_effective_text(slide_design.get(field), minimum=14, unique_minimum=6):
                        errors.append(f"{pid}: slide_design.{field}最低有效内容不足")
                if not _layout_rationale_effective(slide_design.get("layout_rationale")):
                    errors.append(f"{pid}: 版式理由必须说明教学作用，不能以美观、清晰或大气代替")
        if is_v23_plus:
            conditional_page_fields = {
                "artifact", "real_wait", "bounded_feedback", "visible_revision",
                "normal_counterexample",
            }
            required_page_fields = (
                set(PAGE_REQUIRED_FIELDS) | set(V2_PAGE_CONTRACT_FIELDS)
            ) - conditional_page_fields
            requirement_to_field = {
                "artifact": "artifact",
                "wait": "real_wait",
                "feedback": "bounded_feedback",
                "revision": "visible_revision",
                "normal_counterexample": "normal_counterexample",
            }
            required_page_fields.update(
                field
                for requirement, field in requirement_to_field.items()
                if requirement in event_requirements
            )
            for field in sorted(required_page_fields):
                value = page.get(field)
                if isinstance(value, str) and not value.strip() or value is None or value == []:
                    errors.append(f"{pid}: v2.3+事件合同缺 {field}")
            required_string_fields = required_page_fields & V2_PAGE_STRING_FIELDS
            for field in sorted(required_string_fields):
                if not isinstance(page.get(field), str) or not page[field].strip():
                    errors.append(f"{pid}: {field}必须为非空字符串")
                elif not _minimum_effective_text(page[field]):
                    errors.append(f"{pid}: {field}最低有效内容不足，不能用单字或低信息填充")
        else:
            for field in PAGE_REQUIRED_FIELDS:
                value = page.get(field)
                if isinstance(value, str) and not value.strip() or value is None or value == []:
                    errors.append(f"{pid}: 缺页面合同字段 {field}")
            if is_v2:
                for field in V2_PAGE_CONTRACT_FIELDS:
                    value = page.get(field)
                    if isinstance(value, str) and not value.strip() or value is None or value == []:
                        errors.append(f"{pid}: v2十八字段合同缺 {field}")
                for field in V2_PAGE_STRING_FIELDS:
                    if not isinstance(page.get(field), str) or not page[field].strip():
                        errors.append(f"{pid}: {field}必须为非空字符串")
                    elif not _minimum_effective_text(page[field]):
                        errors.append(f"{pid}: {field}最低有效内容不足，不能用单字或低信息填充")
        if is_v2:
            if not _nonempty_string_list(page.get("student_action")):
                errors.append(f"{pid}: student_action必须为非空字符串列表")
            else:
                for index, action in enumerate(page["student_action"]):
                    if not _minimum_effective_text(action):
                        errors.append(f"{pid}: student_action[{index}]最低有效内容不足")
            next_use_ref = page.get("next_use_ref")
            if not isinstance(next_use_ref, dict):
                errors.append(f"{pid}: next_use_ref必须为结构化前向消费")
            else:
                next_kind = next_use_ref.get("kind")
                target_id = str(next_use_ref.get("target_id") or "").strip()
                use = str(next_use_ref.get("use") or "").strip()
                if next_kind not in {"page", "closure", "assessment"}:
                    errors.append(f"{pid}: next_use_ref.kind非法")
                if not _minimum_effective_text(use):
                    errors.append(f"{pid}: next_use_ref.use最低有效内容不足")
                current_index = page_id_list.index(pid) if pid in page_id_list else -1
                if next_kind == "page":
                    if target_id not in page_ids:
                        errors.append(f"{pid}: next_use_ref目标页不存在: {target_id}")
                    elif page_id_list.index(target_id) <= current_index:
                        errors.append(f"{pid}: next_use_ref必须指向后续页面: {target_id}")
                elif next_kind == "closure":
                    if current_index != len(page_id_list) - 1 or target_id != "lesson_closure":
                        errors.append(f"{pid}: closure只允许最后一页指向lesson_closure")
                elif next_kind == "assessment":
                    if not target_id:
                        errors.append(f"{pid}: assessment next_use_ref缺target_id")
                    else:
                        if target_id not in approved_objective_ids:
                            errors.append(f"{pid}: assessment目标未获G1批准: {target_id}")
                        errors.append(
                            f"{pid}: v2尚未注册可核验的assessment消费者，"
                            "不得用目标ID冒充真实后用对象"
                        )
        raw_script = page.get("script")
        if not isinstance(raw_script, dict):
            errors.append(f"{pid}: script必须为对象")
            script = {}
        else:
            script = raw_script
        script_segment_ids_for_timeboxes: list[str] = []
        if is_v21_plus:
            required_script_text_fields = {
                "transition_spoken", "student_process", "feedback_spoken",
                "observable_evidence", "cut_spoken",
            }
            if is_v23_plus:
                required_script_text_fields = {"student_process"}
                if "feedback" in event_requirements:
                    required_script_text_fields.add("feedback_spoken")
                if (
                    "artifact" in event_requirements
                    or "expected_responses" in event_requirements
                ):
                    required_script_text_fields.add("observable_evidence")
            for field in required_script_text_fields:
                if field not in script:
                    errors.append(f"{pid}: script缺{field}")
                elif not _minimum_effective_text(script.get(field), minimum=12, unique_minimum=6):
                    errors.append(f"{pid}: script.{field}最低有效内容不足")
            expected_responses = script.get("expected_responses")
            expected_responses_required = (
                not is_v23_plus or "expected_responses" in event_requirements
            )
            if expected_responses_required and not _nonempty_string_list(expected_responses):
                errors.append(f"{pid}: script.expected_responses必须为非空字符串列表")
            elif expected_responses is not None and not _string_list(expected_responses):
                errors.append(f"{pid}: script.expected_responses必须为字符串列表")
            elif isinstance(expected_responses, list):
                for index, response in enumerate(expected_responses):
                    if not _minimum_effective_text(response, minimum=6, unique_minimum=4):
                        errors.append(f"{pid}: script.expected_responses[{index}]最低有效内容不足")
            if is_v22_plus:
                segments = script.get("script_segments")
                if not isinstance(segments, list) or not segments or not all(isinstance(item, dict) for item in segments):
                    errors.append(f"{pid}: script.script_segments必须为非空对象列表")
                    segments = []
                segment_ids: list[str] = []
                segment_kinds: list[str] = []
                segment_kind_positions: dict[str, list[int]] = {}
                spoken_projection_parts: list[str] = []
                for index, segment in enumerate(segments):
                    _reject_unknown_fields(
                        segment,
                        V22_SCRIPT_SEGMENT_FIELDS,
                        f"{pid}: script_segments[{index}]",
                        errors,
                    )
                    segment_id = str(segment.get("id") or "").strip()
                    expected_segment_id = f"S{index + 1:02d}"
                    if segment_id != expected_segment_id:
                        errors.append(f"{pid}: script_segments[{index}].id应为{expected_segment_id}")
                    segment_ids.append(segment_id)
                    state_id = str(segment.get("state_id") or "").strip()
                    if state_id not in state_ids:
                        errors.append(f"{pid}: script_segments[{index}]引用未知状态: {state_id}")
                    kind = str(segment.get("kind") or "").strip()
                    allowed_script_kinds = V23_SCRIPT_KINDS if is_v23_plus else V22_SCRIPT_KINDS
                    if kind not in allowed_script_kinds:
                        errors.append(f"{pid}: script_segments[{index}].kind非法: {kind}")
                    segment_kinds.append(kind)
                    segment_kind_positions.setdefault(kind, []).append(index)
                    trigger = str(segment.get("enter_trigger") or "").strip()
                    if trigger not in allowed_state_triggers:
                        errors.append(f"{pid}: script_segments[{index}].enter_trigger非法: {trigger}")
                    if kind in {"calibration", "feedback"} and trigger in {
                        "page_enter", "after_instruction", "after_prior_artifact_retrieved",
                    }:
                        errors.append(f"{pid}: calibration片段不得早于首份产物提交: {segment_id}")
                    if (
                        kind == "calibration"
                        and state_id in state_trigger_by_id
                        and state_trigger_by_id[state_id] != trigger
                    ):
                        errors.append(f"{pid}: calibration片段与信息状态触发不一致: {segment_id}")
                    state_trigger = state_trigger_by_id.get(state_id)
                    if (
                        state_trigger in trigger_rank
                        and trigger in trigger_rank
                        and trigger_rank[trigger] < trigger_rank[state_trigger]
                    ):
                        errors.append(f"{pid}: script_segments[{index}]片段早于所绑定状态: {segment_id}")
                    if not _minimum_effective_text(segment.get("text"), minimum=6, unique_minimum=4):
                        errors.append(f"{pid}: script_segments[{index}].text最低有效内容不足")
                    spoken_projection_kinds = {"task", "calibration"}
                    if is_v23_plus:
                        spoken_projection_kinds |= {
                            "instruction", "narration", "reading", "summary",
                        }
                    if kind in spoken_projection_kinds:
                        spoken_projection_parts.append(str(segment.get("text") or ""))
                if len(segment_ids) != len(set(segment_ids)):
                    errors.append(f"{pid}: script_segments.id重复")
                script_segment_ids_for_timeboxes = segment_ids
                required_segment_kinds = {"transition", "task", "wait", "feedback", "cut"}
                if is_v23_plus:
                    required_segment_kinds = {
                        kind
                        for kind in ("task", "wait", "feedback")
                        if kind in event_requirements
                    }
                for required_kind in required_segment_kinds:
                    if required_kind not in segment_kinds:
                        errors.append(f"{pid}: script_segments缺{required_kind}片段")
                for index, kind in enumerate(segment_kinds):
                    if kind == "task" and (
                        index + 1 >= len(segment_kinds) or segment_kinds[index + 1] != "wait"
                    ):
                        errors.append(
                            f"{pid}: task片段后必须紧接真实wait: {segment_ids[index]}"
                        )
                for state_id, state_trigger in state_trigger_by_id.items():
                    if state_id == "B0":
                        continue
                    if not any(
                        str(segment.get("state_id") or "") == state_id
                        and str(segment.get("enter_trigger") or "") == state_trigger
                        for segment in segments
                    ):
                        errors.append(
                            f"{pid}: 信息状态没有同触发剧本事件: {state_id}/{state_trigger}"
                        )
                if has_calibration_elements and "calibration" not in segment_kinds:
                    errors.append(f"{pid}: 存在calibration元素但缺校准台词片段")
                compact_spoken = re.sub(r"\s+", "", str(script.get("teacher_spoken") or ""))
                compact_projection = re.sub(r"\s+", "", "".join(spoken_projection_parts))
                if compact_projection != compact_spoken:
                    projection_label = (
                        "讲授/叙述/朗读/任务/校准/总结片段"
                        if is_v23_plus else "task/calibration片段"
                    )
                    errors.append(f"{pid}: {projection_label}未按原顺序完整投影teacher_spoken")
                wait_positions = segment_kind_positions.get("wait", [])
                calibration_positions = segment_kind_positions.get("calibration", [])
                if calibration_positions and (
                    not wait_positions or min(calibration_positions) <= min(wait_positions)
                ):
                    errors.append(f"{pid}: calibration片段必须位于wait之后")
        if is_v2 and not isinstance(script.get("teacher_spoken"), str):
            errors.append(f"{pid}: script.teacher_spoken必须为非空字符串")
        elif is_v2 and not script.get("teacher_spoken", "").strip():
            errors.append(f"{pid}: script.teacher_spoken必须为非空字符串")
        elif is_v2 and not _minimum_effective_text(script.get("teacher_spoken"), minimum=12, unique_minimum=5):
            errors.append(f"{pid}: script.teacher_spoken最低有效内容不足")
        boxes = script.get("timeboxes") or []
        if is_v2 and not boxes:
            errors.append(f"{pid}: v2 script.timeboxes为空，无法证明真实等待与时间守恒")
        if boxes and not isinstance(boxes, list):
            errors.append(f"{pid}: script.timeboxes必须为对象列表")
            boxes = []
        if boxes:
            total = 0
            boxes_valid = True
            for index, box in enumerate(boxes):
                if not isinstance(box, dict):
                    errors.append(f"{pid}: timebox[{index}]必须为对象")
                    boxes_valid = False
                    continue
                if is_v2:
                    _reject_unknown_fields(
                        box,
                        V22_TIMEBOX_FIELDS if is_v22_plus else V2_TIMEBOX_FIELDS,
                        f"{pid}: timebox[{index}]",
                        errors,
                    )
                if not isinstance(box.get("label"), str) or not box["label"].strip():
                    errors.append(f"{pid}: timebox[{index}].label为空")
                    boxes_valid = False
                seconds = box.get("seconds")
                if not isinstance(seconds, (int, float)) or isinstance(seconds, bool) or seconds <= 0:
                    errors.append(f"{pid}: timebox[{index}].seconds必须为正数")
                    boxes_valid = False
                else:
                    total += seconds
                if is_v22_plus and not _nonempty_string_list(box.get("segment_ids")):
                    errors.append(f"{pid}: timebox[{index}].segment_ids必须为非空字符串列表")
            expected = minutes * 60 if isinstance(minutes, (int, float)) and not isinstance(minutes, bool) else None
            if boxes_valid and expected is not None and total != expected:
                errors.append(f"{pid}: 时间盒 {total}s ≠ {expected}s")
            if is_v22_plus:
                allocated_segment_ids = [
                    segment_id
                    for box in boxes
                    if isinstance(box, dict) and isinstance(box.get("segment_ids"), list)
                    for segment_id in box["segment_ids"]
                    if isinstance(segment_id, str)
                ]
                if allocated_segment_ids != script_segment_ids_for_timeboxes:
                    errors.append(f"{pid}: timeboxes必须按顺序完整分配script_segments")
        branches = script.get("branches") or []
        if not isinstance(branches, list):
            errors.append(f"{pid}: script.branches必须为对象列表")
            branches = []
        branches_required = not is_v23_plus or "branches" in event_requirements
        if branches_required and len(branches) < 2:
            errors.append(f"{pid}: script.branches < 2（P-08：必须有回应分支）")
        branch_kinds: list[str] = []
        for index, branch in enumerate(branches):
            if not isinstance(branch, dict):
                errors.append(f"{pid}: branch[{index}]必须为对象")
                continue
            if is_v2:
                _reject_unknown_fields(branch, V2_BRANCH_FIELDS, f"{pid}: branch[{index}]", errors)
            kind = str(branch.get("kind") or "").strip()
            response = str(branch.get("response") or "").strip()
            if not kind:
                errors.append(f"{pid}: branch[{index}].kind为空")
            else:
                branch_kinds.append(kind)
                if is_v2 and not _minimum_effective_text(kind, minimum=2, unique_minimum=2):
                    errors.append(f"{pid}: branch[{index}].kind最低有效内容不足")
            if not response:
                errors.append(f"{pid}: branch[{index}].response为空")
            elif is_v2 and not _minimum_effective_text(response, minimum=6, unique_minimum=4):
                errors.append(f"{pid}: branch[{index}].response最低有效内容不足")
        if len(branch_kinds) != len(set(branch_kinds)):
            errors.append(f"{pid}: 分支kind重复，不能证明不同学生反应的应对")
        if canonical:
            err = literary_object_error(pid, page.get("literary_object"), canonical)
            if err:
                errors.append(err)
        frontstage_values = page.get("frontstage") or []
        if is_v21_plus and isinstance(page.get("slide_design"), dict):
            frontstage_values = page["slide_design"].get("frontstage_elements") or []
        normalized_frontstage: list[str] = []
        for item in frontstage_values:
            if isinstance(item, str):
                normalized_frontstage.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                normalized_frontstage.append(item["text"])
        for text in [page.get("title", "")] + normalized_frontstage:
            for word in banned:
                if word in text:
                    errors.append(f"{pid}: 前台含后台词「{word}」")

    if is_v2 and approved_contract is not None:
        for stage_id in approved_stage_order:
            if stage_id not in page_stage_ids:
                errors.append(f"G1阶段未被任何页面落实: {stage_id}")
        for oid in sorted(approved_objective_ids - page_objective_ids):
            errors.append(f"G1目标未被任何页面落实: {oid}")
        for kid in sorted(approved_teachable_kids - page_lesson_kids):
            errors.append(f"G1必教/旧知KID未被任何页面落实: {kid}")
        expected_total_minutes = approved_contract.get("total_minutes")
        actual_total_minutes = sum(
            page.get("minutes") for page in pages
            if isinstance(page.get("minutes"), (int, float)) and not isinstance(page.get("minutes"), bool)
        )
        if actual_total_minutes != expected_total_minutes:
            errors.append(
                f"pages总分钟数与G1 total_minutes漂移: 期望{expected_total_minutes}，实际{actual_total_minutes}"
            )

    if findings and strict:
        errors.append(f"样板自证 {len(findings)} 处（--strict 判失败；见 check_trace_evidence 报告）")
    elif findings:
        warnings.append(f"样板自证 {len(findings)} 处：STANDARD-1.0 要求新候选清零（存量数据作为缺口报告）")

    boundary = lesson.get("claim_boundary", "")
    if not has_pending_classroom_boundary(boundary, canonical=is_v2):
        errors.append("claim_boundary必须明确声明效果待真实课堂/试教验证（P-12）")
    return errors, warnings, stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--lesson-js")
    group.add_argument("--lesson-json")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    lesson = load_lesson(args.lesson_js, args.lesson_json)
    errors, warnings, stats = validate(lesson, args.strict, root=ROOT)

    for warning in warnings:
        print(f"[warn] {warning}")
    for error in errors:
        print(f"[error] {error}")
    if errors:
        print(f"课程数据校验失败：{len(errors)} 错误")
        return 1
    print(f"课程数据校验通过：{stats['pages']} 页 / KP {stats['kp_scope']} 条（defer {stats['deferred']}）/ 样板 {stats['boilerplate']} 处")
    return 0


if __name__ == "__main__":
    sys.exit(main())
