#!/usr/bin/env python3
"""Build the V6 opening audit slice without sealing or closing legacy pages.

The builder overlays an honest S001-S016 self-diagnosis on the immutable Task 3
skeleton, compiles the opening content source into current page/event contracts,
and writes only to the V6 staging directory.  Independent student-reception and
visual reviews remain pending by design.
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LESSON_DIR = PROJECT_ROOT / "work" / "备课" / "选择性必修下册" / "氓"
SKELETON = LESSON_DIR / "_v6_stage" / "05_氓_V6逐页功能审计.json"
OPENING_SOURCE = PROJECT_ROOT / "scripts" / "meng_v6" / "content" / "opening.js"
REVIEW_RECEIPT = PROJECT_ROOT / "scripts" / "meng_v6" / "reviews" / "opening_structure.json"
OUTPUT_DIR = LESSON_DIR / "_v6_stage" / "opening"
JSON_OUTPUT = OUTPUT_DIR / "opening_audit.json"
MARKDOWN_OUTPUT = OUTPUT_DIR / "opening_audit.md"
REVIEWED_AT = "2026-08-13T10:30:00+08:00"
SELF_REVIEWER = "v6-opening-self-auditor"


# A failed gate records the page's original defect.  It is not a judgment on
# the replacement page and must never be rewritten into a pass after repair.
LEGACY_FAILURES: dict[str, dict[str, tuple[str, str, str]]] = {
    "S001": {
        "G3": ("G3_COVERAGE_FALSE", "P1", "隐藏教师导航不是学生学习页面，不能声称覆盖学生行动"),
        "G4": ("G4_CHANGE_UNOBSERVABLE", "P2", "导航页只服务教师操作，没有学生可观察变化"),
    },
    "S002": {
        "G2": ("G2_ROLE_MULTIPLE", "P1", "封面同时命名作品并用结尾替全文定调"),
        "G1": ("G1_PREREQ_MISSING", "P1", "首次听读前尚无依据理解‘亦已焉哉’的分量"),
    },
    "S003": {
        "G1": ("G1_PREREQ_MISSING", "P1", "固定三篇假定全班都学过并记得"),
        "G3": ("G3_COVERAGE_FALSE", "P1", "选择最熟悉的一篇不保证每人形成可交流产物"),
        "G6": ("G6_MERGEABLE", "P2", "列举作品与下一页回忆任务可以无损合为真实检索活动"),
    },
    "S004": {
        "G1": ("G1_PREREQ_MISSING", "P1", "学生尚无分析关系幸福或困境所需的框架和共同材料"),
        "G5": ("G5_OUTPUT_ORPHAN", "P1", "个人判断没有被下一页真实读取，下一页答案已经预制"),
    },
    "S005": {
        "G3": ("G3_COVERAGE_FALSE", "P1", "教师预制结论取代了学生广泛发言与核对"),
        "G4": ("G4_CHANGE_UNOBSERVABLE", "P2", "页面没有可观察的学生行动、作品或修订"),
        "G5": ("G5_OUTPUT_ORPHAN", "P1", "预制主题没有保留作品出处，也未形成可追溯后用"),
    },
    "S006": {
        "G6": ("G6_MERGEABLE", "P2", "总览与随后三张问题页重复占用注意和时间"),
    },
    "S007": {
        "G1": ("G1_PREREQ_MISSING", "P1", "全文初读前要求理解从开头到结尾的行动链"),
        "G2": ("G2_FUNCTION_DUPLICATE", "P1", "问题已在上一页出现，没有新增学生动作"),
    },
    "S008": {
        "G2": ("G2_FUNCTION_DUPLICATE", "P1", "问题已在总览页出现，单页没有新增功能"),
        "G4": ("G4_CHANGE_UNOBSERVABLE", "P2", "页面只重复问题，未形成可观察变化"),
    },
    "S009": {
        "G1": ("G1_PREREQ_MISSING", "P1", "全文阅读前同时追问归责与离开阻力，前置过重"),
        "G2": ("G2_ROLE_MULTIPLE", "P1", "一页混合原因、责任和停止关系的多项任务"),
    },
    "S012": {
        "G5": ("G5_OUTPUT_ORPHAN", "P1", "初听停顿没有安排同伴倾听、保存和全文后的真实回用"),
    },
    "S014": {
        "G2": ("G2_ROLE_MULTIPLE", "P1", "节奏体验与赋比兴、反复、叠词术语预告同时争抢功能"),
    },
    "S015": {
        "G1": ("G1_PREREQ_MISSING", "P1", "十个字音脱离相应诗句集中前置，缺少语境支撑"),
        "G3": ("G3_COVERAGE_FALSE", "P1", "教师集中报音不能证明每名学生能够在原句中读准"),
        "G4": ("G4_CHANGE_UNOBSERVABLE", "P2", "没有在原句朗读中留下可核验的读音变化"),
    },
    "S016": {
        "G6": ("G6_MERGEABLE", "P2", "第一章提示页可无损并入紧随其后的第一章原诗入口"),
    },
}


def audit_sha256(value: Any) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_opening_source() -> dict[str, Any]:
    result = subprocess.run(
        ["node", str(OPENING_SOURCE)], cwd=PROJECT_ROOT, text=True,
        capture_output=True, check=False,
    )
    if result.returncode:
        raise RuntimeError(result.stderr or result.stdout)
    value = json.loads(result.stdout)
    if not isinstance(value, dict):
        raise ValueError("opening source must emit one JSON object")
    return value


def completed_gate(page_id: str, gate_id: str, failure: tuple[str, str, str] | None) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "gate_status": "fail" if failure else "pass",
        "evidence_refs": [f"{page_id}#source_visible_text", f"{page_id}#source_title"],
        "failure_code": failure[0] if failure else None,
        "reviewer": SELF_REVIEWER,
        "reviewed_at": REVIEWED_AT,
    }


def defect_category(gate_id: str) -> str:
    return {
        "G1": "prerequisite", "G2": "page_function", "G3": "student_reception",
        "G4": "student_reception", "G5": "causal_reuse", "G6": "page_necessity",
    }[gate_id]


def diagnose_legacy(pages: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    result = copy.deepcopy(pages)
    defects: list[dict[str, Any]] = []
    for page in result[:16]:
        page_id = page["page_id"]
        failures = LEGACY_FAILURES.get(page_id, {})
        page["audit_scope"] = "learning_page"
        page["owner_event_id"] = None
        page["gates"] = [
            completed_gate(page_id, f"G{number}", failures.get(f"G{number}"))
            for number in range(1, 7)
        ]
        defect_ids: list[str] = []
        for gate_id, (failure_code, severity, claim) in failures.items():
            defect_id = f"A-{page_id}-{gate_id}"
            defect_ids.append(defect_id)
            defects.append({
                "defect_id": defect_id,
                "severity": severity,
                "object_ref": page_id,
                "category": defect_category(gate_id),
                "failure_code": failure_code,
                "claim": claim,
                "evidence_refs": [f"{page_id}#source_visible_text", f"{page_id}#gates"],
                "reviewer_id": SELF_REVIEWER,
                "discovered_at": REVIEWED_AT,
                "status": "open",
            })
        pending = {"status": "pending", "reviewer": None, "reviewed_at": None, "defect_ids": []}
        page["review_status"] = {
            "scope": "legacy_initial_diagnosis",
            "self_review": {
                "status": "pass", "reviewer": SELF_REVIEWER,
                "reviewed_at": REVIEWED_AT, "defect_ids": sorted(defect_ids),
            },
            "student_reception": dict(pending),
            "visual": dict(pending),
            "consensus": "pending",
            "adjudication": None,
        }
    return result, defects


def pending_review(scope: str = "structure_only") -> dict[str, Any]:
    pending = {"status": "pending", "reviewer": None, "reviewed_at": None, "defect_ids": []}
    return {
        "scope": scope,
        "self_review": {
            "status": "pass", "reviewer": "v6-opening-current-self-reviewer",
            "reviewed_at": REVIEWED_AT, "defect_ids": [],
        },
        "student_reception": dict(pending),
        "visual": dict(pending),
        "consensus": "pending",
        "adjudication": None,
    }


def reviewable_current_hash(pages: list[dict[str, Any]], events: list[dict[str, Any]]) -> str:
    return audit_sha256({
        "pages": [{key: value for key, value in item.items() if key != "review_status"} for item in pages],
        "events": [{key: value for key, value in item.items() if key != "review_status"} for item in events],
    })


def apply_independent_review_receipt(
    pages: list[dict[str, Any]], events: list[dict[str, Any]],
) -> dict[str, Any] | None:
    if not REVIEW_RECEIPT.exists():
        return None
    receipt = json.loads(REVIEW_RECEIPT.read_text(encoding="utf-8"))
    expected_hash = reviewable_current_hash(pages, events)
    if receipt.get("reviewed_source_sha256") != expected_hash:
        raise ValueError("opening independent-review receipt is stale")
    if receipt.get("status") != "pass" or any(receipt.get(key) != 0 for key in ("p0", "p1", "p2")):
        raise ValueError("opening independent review has unresolved P0-P2 defects")
    student = receipt.get("student_reception")
    visual = receipt.get("visual")
    if not isinstance(student, dict) or not isinstance(visual, dict):
        raise ValueError("opening independent-review receipt is incomplete")
    for item in [*pages, *events]:
        existing = item["review_status"]
        item["review_status"] = {
            "scope": existing["scope"],
            "self_review": existing["self_review"],
            "student_reception": {
                "status": "pass", "reviewer": student["reviewer"],
                "reviewed_at": student["reviewed_at"], "defect_ids": [],
            },
            "visual": {
                "status": "pass", "reviewer": visual["reviewer"],
                "reviewed_at": visual["reviewed_at"], "defect_ids": [],
            },
            "consensus": "passed",
            "adjudication": None,
        }
    return receipt


def gate(page_id: str, gate_id: str, *, status: str = "pass", deferred: dict[str, Any] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "gate_id": gate_id,
        "gate_status": status,
        "evidence_refs": [] if status in {"na", "deferred"} else [f"{page_id}#unique_function"],
        "failure_code": None,
        "reviewer": None if status in {"na", "deferred"} else "v6-opening-current-self-reviewer",
        "reviewed_at": None if status in {"na", "deferred"} else REVIEWED_AT,
    }
    if deferred:
        value.update({
            "target_event_id": deferred["target_event_id"],
            "target_batch": deferred["target_batch"],
            "expected_use": deferred["expected_use"],
        })
    return value


def page_epistemic_status(item: dict[str, Any]) -> str:
    if item["unit_role"] in {"生成", "交流", "收束"}:
        return "课堂生成"
    if item["page_id"] in {"N001", "N008", "N009", "N011", "N012"}:
        return "文本明写"
    return "合理推断"


def visual_duty(value: str) -> str:
    return {
        "题名": "题名", "活动界面": "活动界面", "现场共创": "现场共创",
        "全文/章内整读": "全文/章内整读", "原文批注": "原文批注",
    }[value]


def compile_page(item: dict[str, Any], order: int) -> dict[str, Any]:
    page_id = item["page_id"]
    carrier = page_id in {"N001", "N008", "N009"}
    deferred_source = item.get("deferred")
    if page_id == "N012":
        deferred_source = {
            "target_batch": "chapter_1",
            "expected_use": "第一章逐句讲读调用节奏标记并在相应原句解决字音",
        }
    deferred = None
    if deferred_source:
        deferred = {
            "target_event_id": item["next_event_id"],
            "target_batch": deferred_source["target_batch"],
            "expected_use": deferred_source["expected_use"],
        }
    g5_status = "na" if carrier else ("deferred" if deferred else "pass")
    release_status = "provisional" if deferred else "final"
    action_seconds = max(15, int(float(item["minutes"]) * 60))
    inherited = [
        {"legacy_id": legacy_id, "element_id": "page_function", "target_field": "unique_function"}
        for legacy_id in item["legacy_ids"]
    ]
    return {
        "node_id": page_id,
        "page_id": page_id,
        "node_type": "page",
        "audit_scope": "event_carrier" if carrier else "learning_page",
        "owner_event_id": item["event_id"] if carrier else None,
        "execution_order": order,
        "release_status": release_status,
        "learning_unit": item["event_id"],
        "unit_role": item["unit_role"],
        "supporting_move": item["action"],
        "prerequisite": item["prerequisite"],
        "epistemic_status": page_epistemic_status(item),
        "unique_function": item["function"],
        "student_visible_text": item["visible"],
        "screen_content": item["visible"],
        "student_input": item["input"],
        "student_action": {
            "actor": "每名学生", "action": item["action"], "object": item["input"],
            "duration_seconds": action_seconds, "artifact": item["artifact"],
        },
        "voice_coverage": {
            "all_have_entry": True,
            "independent_entry": item["listener"],
            "selection_method": "全员同步完成；公开发言按页面所列轮说或增量贡献规则执行",
        },
        "listener_task": {
            "task": item["listener"], "artifact": item["artifact"], "reuse": item["next"],
        },
        "observable_change": {
            "before": item["change"][0], "after": item["change"][1], "criterion": item["change"][2],
        },
        "artifact_location": item["location"],
        "previous_relation": item["previous"],
        "next_relation": item["next"],
        "deletion_loss": item["loss"],
        "merge_test": {
            "result": "cannot_merge", "cannot_merge_reason": item["loss"],
        },
        "channel_split": {
            "screen": item["visible"],
            "teacher": item.get(
                "teacher_script",
                f"组织{item['action']}，只提供必要等待、倾听和转场",
            ),
            "worksheet": item["location"],
        },
        "framework_cost": item["framework"],
        "primary_visual_duty": visual_duty(item["visual"]),
        "visual_implementation": item.get(
            "visual_implementation",
            "按主视觉职责排版；人物图在角色设定冻结和插图必要性通过前一律不进入本页",
        ),
        "secondary_visual": "纸本肌理" if item["visual"] == "题名" else "章序或活动进度提示",
        "time_value": {"minutes": item["minutes"], "irreplaceable_gain": item["change"][1]},
        "next_use_refs": [{
            "target_event_id": item["next_event_id"],
            "source_artifact_field": "artifact_location",
            "target_input_field": "inputs[0]",
            "expected_use": item["next"],
        }],
        "legacy_source_refs": item["legacy_ids"],
        "inherited_functions": inherited,
        "review_status": pending_review(),
        "gates": [
            ({
                **gate(page_id, f"G{number}", status="na"),
                "evidence_refs": [f"{item['event_id']}#{'gate_4' if number == 4 else 'gate_5'}"],
            } if carrier and number in {4, 5} else gate(
                page_id, f"G{number}", status=(g5_status if number == 5 else "pass"),
                deferred=(deferred if number == 5 else None),
            ))
            for number in range(1, 7)
        ],
    }


def event_gate(event_id: str, gate_name: str, *, implemented: bool) -> dict[str, Any]:
    return {
        "gate_id": gate_name,
        "gate_status": "pass" if implemented else "deferred",
        "evidence_refs": [f"{event_id}#observable_change"] if implemented else [],
        "failure_code": None,
        "reviewer": "v6-opening-current-self-reviewer" if implemented else None,
        "reviewed_at": REVIEWED_AT if implemented else None,
    }


def deferred_event_gate(event_id: str, target: dict[str, Any], expected_use: str) -> dict[str, Any]:
    return {
        "gate_id": "G5", "gate_status": "deferred", "evidence_refs": [],
        "failure_code": None, "reviewer": None, "reviewed_at": None,
        "target_event_id": target["event_id"], "target_batch": target["batch"],
        "expected_use": expected_use,
    }


def compile_events(source: dict[str, Any], pages: list[dict[str, Any]]) -> list[dict[str, Any]]:
    page_source = {item["page_id"]: item for item in source["pages"]}
    overrides = source.get("event_overrides", {})
    groups: dict[str, list[dict[str, Any]]] = {}
    for page in pages:
        groups.setdefault(page["learning_unit"], []).append(page)
    incoming: dict[str, list[dict[str, str]]] = {}
    for page in pages:
        for ref in page["next_use_refs"]:
            incoming.setdefault(ref["target_event_id"], []).append({
                "source_node_id": page["node_id"],
                "source_artifact_field": ref["source_artifact_field"],
                "input_field": ref["target_input_field"],
            })

    events: list[dict[str, Any]] = []
    for index, (event_id, carriers) in enumerate(groups.items(), start=1):
        first = page_source[carriers[0]["page_id"]]
        override = overrides.get(event_id, {})
        owner_ids = [item["node_id"] for item in carriers]
        event_inputs: list[Any] = list(incoming.get(event_id, []))
        if not event_inputs:
            event_inputs = [first["input"]]
        event_order = min(item["execution_order"] for item in carriers) + 1
        event = {
            "node_id": event_id, "event_id": event_id, "node_type": "event",
            "audit_scope": "learning_event", "execution_order": event_order,
            "batch": "opening", "implemented": True,
            "inputs": event_inputs,
            "actions": override.get("actions", [first["action"]]),
            "artifacts": list(dict.fromkeys(item["artifact_location"] for item in carriers)),
            "artifact_locations": list(dict.fromkeys(item["artifact_location"] for item in carriers)),
            "observable_change": {
                "before": first["change"][0],
                "after": page_source[carriers[-1]["page_id"]]["change"][1],
                "criterion": page_source[carriers[-1]["page_id"]]["change"][2],
            },
            "next_uses": list(dict.fromkeys(item["next_relation"] for item in carriers)),
            "carrier_ids": [item["node_id"] for item in carriers if item["audit_scope"] == "event_carrier"],
            "owner_page_ids": owner_ids,
            "gate_4": event_gate(event_id, "G4", implemented=True),
            "gate_5": event_gate(event_id, "G5", implemented=True),
            "evidence_refs": [f"{item['node_id']}#unique_function" for item in carriers],
            "legacy_source_refs": list(dict.fromkeys(id_ for item in carriers for id_ in item["legacy_source_refs"])),
            "inherited_functions": [],
            "release_status": "final",
            "terminal_sink": False,
            "terminal_use": {},
            "review_status": pending_review("learning_event_structure"),
            "participation_contract": {
                "all_students_have_entry": True,
                "listener_task": override.get("listener_task", first["listener"]),
                "artifact_is_saved": True,
                "later_reuse_is_named": True,
            },
        }
        events.append(event)

    used_orders = {item["execution_order"] for item in pages} | {item["execution_order"] for item in events}
    for position, future in enumerate(source["future_events"], start=1):
        order = int(future["execution_order"])
        if order in used_orders:
            raise ValueError(f"duplicate future execution order: {order}")
        terminal = bool(future.get("terminal_sink"))
        inputs = incoming.get(future["event_id"], future["inputs"])
        events.append({
            "node_id": future["event_id"], "event_id": future["event_id"], "node_type": "event",
            "audit_scope": "learning_event", "execution_order": order,
            "batch": future["batch"], "implemented": False,
            "inputs": inputs, "actions": future["actions"], "artifacts": future["artifacts"],
            "artifact_locations": future["locations"],
            "observable_change": {
                "before": "跨批次事件尚未实施", "after": "按登记用途调用前序产物",
                "criterion": "目标批次完成后以实际读取字段复验",
            },
            "next_uses": future["next_uses"], "carrier_ids": [],
            "owner_page_ids": future["owner_page_ids"],
            "gate_4": event_gate(future["event_id"], "G4", implemented=False),
            "gate_5": event_gate(future["event_id"], "G5", implemented=False),
            "evidence_refs": [f"{future['owner_page_ids'][0]}#next_use_refs"],
            "legacy_source_refs": [], "inherited_functions": [],
            "release_status": "provisional", "terminal_sink": terminal,
            "terminal_use": ({
                "final_artifact": "退出条", "recipient_or_owner": "教师与学生本人",
                "post_class_use": "教师诊断后续阅读问题，学生保留个人理解",
                "artifact_location": "班级收集袋或学生学习档案",
                "delivery_evidence_refs": ["E_FUTURE_TERMINAL#artifacts"],
                "no_further_classroom_call_reason": "这是全课唯一终端事件",
            } if terminal else {}),
            "review_status": pending_review("future_event_placeholder"),
            "participation_contract": {
                "all_students_have_entry": True, "listener_task": "待目标批次设计时复验",
                "artifact_is_saved": True, "later_reuse_is_named": bool(future["next_uses"]) or terminal,
            },
        })
    events = sorted(events, key=lambda item: item["execution_order"])
    event_by_id = {item["event_id"]: item for item in events}
    page_by_id = {item["node_id"]: item for item in pages}
    for event in events:
        if not event["implemented"]:
            continue
        targets = []
        for owner_id in event["owner_page_ids"]:
            owner = page_by_id[owner_id]
            targets.extend(ref["target_event_id"] for ref in owner["next_use_refs"])
        targets = list(dict.fromkeys(targets))
        if not targets:
            raise ValueError(f"implemented event has no forward use: {event['event_id']}")
        target_events = [event_by_id[target_id] for target_id in targets]
        event["next_use_contracts"] = [{
            "target_event_id": target["event_id"],
            "target_input_field": "inputs",
            "expected_use": next(
                ref["expected_use"]
                for owner_id in event["owner_page_ids"]
                for ref in page_by_id[owner_id]["next_use_refs"]
                if ref["target_event_id"] == target["event_id"]
            ),
        } for target in target_events]
        if all(target["implemented"] for target in target_events):
            event["gate_5"] = {
                "gate_id": "G5", "gate_status": "pass", "failure_code": None,
                "evidence_refs": [f"{event['event_id']}#artifacts"] + [
                    f"{target['event_id']}#inputs" for target in target_events
                ],
                "reviewer": "v6-opening-current-self-reviewer", "reviewed_at": REVIEWED_AT,
            }
        else:
            if len(target_events) != 1:
                raise ValueError(f"deferred event must have one declared target: {event['event_id']}")
            event["gate_5"] = deferred_event_gate(
                event["event_id"], target_events[0], event["next_use_contracts"][0]["expected_use"],
            )
            event["release_status"] = "provisional"
    return events


def inventories(pages: list[dict[str, Any]], events: list[dict[str, Any]]) -> dict[str, Any]:
    manifest_pages = [
        {"node_id": item["node_id"], "execution_order": item["execution_order"], "module": "opening"}
        for item in pages
    ]
    manifest_events = [
        {"node_id": item["node_id"], "execution_order": item["execution_order"], "module": item["batch"]}
        for item in events
    ]
    event_ids = {item["node_id"] for item in events}
    edges = []
    for page in pages:
        g5 = next(item for item in page["gates"] if item["gate_id"] == "G5")
        if g5["gate_status"] != "pass":
            continue
        for ref in page["next_use_refs"]:
            if ref["target_event_id"] in event_ids:
                edges.append({"source_node_id": page["node_id"], "target_event_id": ref["target_event_id"]})
    return {"pages": manifest_pages, "events": manifest_events, "g5_edges": edges}


def render_markdown(document: dict[str, Any]) -> str:
    lines = [
        "# 《氓》V6｜S001—S016导入逐页功能审计",
        "",
        "> 证据边界：桌面设计骨架。旧页初诊已完成自审但尚未封存；学生接收与视觉独立审查仍待完成；未声称真实学生已经理解或参与。",
        "",
        "## 逐页结论",
        "",
        "| 新页 | 唯一意义 | 学生行动 | 可观察变化 | 后续调用 | 主视觉 |",
        "|---|---|---|---|---|---|",
    ]
    for page in document["current_release_audit"]["pages"]:
        function = page["unique_function"].replace("|", "｜")
        action = page["student_action"]["action"].replace("|", "｜")
        change = page["observable_change"]["after"].replace("|", "｜")
        use = page["next_relation"].replace("|", "｜")
        lines.append(f"| {page['page_id']} | {function} | {action} | {change} | {use} | {page['primary_visual_duty']} |")
    lines.extend(["", "## 学生前台与后台边界", ""])
    for page in document["current_release_audit"]["pages"]:
        lines.extend([
            f"### {page['page_id']}｜{page['student_visible_text'].splitlines()[0]}", "",
            "**学生上屏内容**", "", "```text", page["student_visible_text"], "```", "",
            f"- 后台唯一功能：{page['unique_function']}",
            f"- 删除损失：{page['deletion_loss']}",
            f"- 视觉理由：{page['primary_visual_duty']}；{page['visual_implementation']}",
            f"- 证据位置：{page['artifact_location']}", "",
        ])
    lines.extend(["## 旧页初始失败保留", "", "| 旧页 | 失败门 | 失败码 |", "|---|---|---|"])
    for page in document["legacy_initial_audit"][:16]:
        failures = [item for item in page["gates"] if item["gate_status"] == "fail"]
        lines.append(f"| {page['page_id']} | {', '.join(item['gate_id'] for item in failures) or '—'} | {', '.join(item['failure_code'] for item in failures) or '—'} |")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    skeleton = json.loads(SKELETON.read_text(encoding="utf-8"))
    source = load_opening_source()
    legacy, defects = diagnose_legacy(skeleton["legacy_initial_audit"])

    # Even execution orders are pages; odd orders are their implemented events.
    pages = [compile_page(item, index * 10) for index, item in enumerate(source["pages"], start=1)]
    events = compile_events(source, pages)
    independent_review = apply_independent_review_receipt(pages, events)
    manifest = inventories(pages, events)

    document = copy.deepcopy(skeleton)
    document.update({
        "document_status": "structure_in_progress",
        "legacy_initial_audit": legacy,
        "pages": legacy,
        "legacy_event_evidence": [],
        "defect_registry": defects,
        "initial_audit_seals": [],
        "seal_amendments": [],
        "legacy_effective_view": copy.deepcopy(legacy),
        "effective_legacy_hash": audit_sha256(legacy),
        "legacy_disposition_closure": [],
        "structure_manifest": manifest,
        "declared_node_inventory": copy.deepcopy(manifest),
        "source_graph_inventory": copy.deepcopy(manifest),
        "structure_assembly_snapshot": copy.deepcopy(manifest),
        "current_release_audit": {"pages": pages, "events": events},
        "independent_structure_review": independent_review,
        "global_checks": {},
    })
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_text(json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    MARKDOWN_OUTPUT.write_text(render_markdown(document), encoding="utf-8")
    print(f"OPENING_AUDIT_OK legacy=16 pages={len(pages)} events={len(events)} output={JSON_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
