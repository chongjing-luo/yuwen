#!/usr/bin/env python3
"""Build the frozen observation manifest from the contract rubric table."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUBRICS = ROOT / "work/knowledge/_meta/rubrics.json"
OUT = ROOT / "work/knowledge/_meta/rubric_observations_2.0-textbook-eval-1.json"


def main() -> int:
    source = json.loads(RUBRICS.read_text(encoding="utf-8"))
    observations: list[dict] = []
    for item_type, rubric in source["rubrics"].items():
        # The evaluation candidate only applies this manifest to the three
        # textbook artifact families.  Exam rubrics remain provisional.
        if item_type not in {"knowledge_card", "unit_graph", "book_summary"}:
            continue
        for dimension in rubric["dimensions"]:
            checkpoints = list(dimension["checkpoints"])
            weight = dimension["weight"]
            # Equal checkpoint weights are frozen unless an item-specific
            # manifest explicitly overrides them before review is sealed.
            per_checkpoint = weight / len(checkpoints)
            for ordinal, checkpoint in enumerate(checkpoints, 1):
                observations.append(
                    {
                        "observation_id": f"OBS-{item_type}-{dimension['id']}-{ordinal:02d}",
                        "item_type": item_type,
                        "dimension_id": dimension["id"],
                        "dimension_name": dimension["name"],
                        "checkpoint": checkpoint,
                        "checkpoint_weight": per_checkpoint,
                        "scope_query": f"{item_type}.{dimension['id']}.{checkpoint}",
                        "applicability": "all items unless a registered N/A constraint applies",
                        "pass_count_rule": "binary checkpoint observation; 1=pass, 0=fail",
                        "evidence_required": True,
                        "na_replacement": None,
                    }
                )

    replacements = [
        {
            "replacement_id": "NA-CARD-VERTICAL-01",
            "item_type": "knowledge_card",
            "dimension_id": "vertical",
            "trigger": "no_reliable_relation",
            "replaces": [
                "已登记候选目标与核查范围",
                "已说明不存在可靠关系的文本/状态理由",
                "源 KP、关系、目标、双方证据均使用结构化 N/A",
                "未强造关系且依赖边界、重开条件明确",
            ],
            "points": [2, 2, 2, 2],
        },
        {
            "replacement_id": "NA-UNIT-PREV-01",
            "item_type": "unit_graph",
            "dimension_id": "progression",
            "trigger": "no_reliable_relation",
            "replaces": ["候选范围", "无边理由", "结构化 N/A", "不强造及重开条件"],
            "points": [2, 1, 1, 1],
        },
        {
            "replacement_id": "NA-UNIT-NEXT-01",
            "item_type": "unit_graph",
            "dimension_id": "progression",
            "trigger": "future_locked",
            "replaces": ["候选范围", "无边理由", "结构化 N/A", "不强造及重开条件"],
            "points": [2, 1, 1, 1],
        },
    ]
    manifest = {
        "schema_version": "2.0-textbook-eval-1",
        "manifest_id": "rubric-observations-2.0-textbook-eval-1",
        "rubric_source": "work/knowledge/_meta/rubrics.json",
        "scope": ["knowledge_card", "unit_graph", "book_summary"],
        "rounding": {"mode": "ROUND_HALF_UP", "increment": "0.5", "arithmetic": "decimal_fixed_point"},
        "observations": observations,
        "na_replacements": replacements,
        "integrity_rules": [
            "claim/evidence and observation manifests are sealed before DG3",
            "N/A removes only the relation fact denominator, never the whole dimension",
            "failed_ids and evidence_refs remain immutable after review sealing",
        ],
    }
    OUT.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(observations)} observations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

