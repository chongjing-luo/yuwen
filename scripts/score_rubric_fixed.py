#!/usr/bin/env python3
"""Recalculate 2.0-textbook-eval-1 observations with Decimal arithmetic."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUBRICS = ROOT / "work/knowledge/_meta/rubrics.json"

ALLOWED_NA = {"not_applicable", "permitted_unavailable", "future_locked", "no_reliable_relation"}


def half(value: Decimal) -> Decimal:
    return value.quantize(Decimal("0.5"), rounding=ROUND_HALF_UP)


def score(payload: dict) -> dict:
    item_type = payload.get("item_type")
    rubric = json.loads(RUBRICS.read_text(encoding="utf-8"))["rubrics"].get(item_type)
    if not rubric:
        raise ValueError(f"unknown item_type: {item_type}")
    supplied = payload.get("observations")
    if not isinstance(supplied, list) or not supplied:
        raise ValueError("observations must be a non-empty array")

    dimensions: dict[str, dict] = {}
    for dim in rubric["dimensions"]:
        dimensions[dim["id"]] = {
            "name": dim["name"],
            "weight": Decimal(str(dim["weight"])),
            "minimum": Decimal(str(dim["minimum"])),
            "checkpoints": set(dim["checkpoints"]),
            "score": Decimal("0"),
            "observations": [],
        }
    seen: set[tuple[str, str]] = set()
    errors: list[str] = []
    for obs in supplied:
        dim_id, checkpoint = obs.get("dimension_id"), obs.get("checkpoint")
        key = (str(dim_id), str(checkpoint))
        if key in seen:
            errors.append(f"duplicate observation {dim_id}/{checkpoint}")
            continue
        seen.add(key)
        if dim_id not in dimensions or checkpoint not in dimensions[dim_id]["checkpoints"]:
            errors.append(f"unknown checkpoint {dim_id}/{checkpoint}")
            continue
        try:
            applicable = int(obs["applicable_count"])
            passed = int(obs["pass_count"])
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"{dim_id}/{checkpoint}: invalid counts ({exc})")
            continue
        if applicable < 0 or passed < 0 or passed > applicable:
            errors.append(f"{dim_id}/{checkpoint}: require 0 <= pass_count <= applicable_count")
            continue
        weight = Decimal(str(obs.get("checkpoint_weight", "0")))
        if weight <= 0:
            errors.append(f"{dim_id}/{checkpoint}: checkpoint_weight must be positive")
            continue
        evidence = obs.get("evidence_refs", [])
        failed_ids = obs.get("failed_ids", [])
        if not isinstance(evidence, list) or not isinstance(failed_ids, list):
            errors.append(f"{dim_id}/{checkpoint}: evidence_refs/failed_ids must be arrays")
            continue
        if applicable == 0:
            na = obs.get("na_status")
            replacement = obs.get("replacement_score")
            if na not in ALLOWED_NA:
                errors.append(f"{dim_id}/{checkpoint}: 0/0 requires an allowed na_status")
                continue
            if replacement is None:
                errors.append(f"{dim_id}/{checkpoint}: 0/0 requires replacement_score")
                continue
            checkpoint_score = Decimal(str(replacement))
            if checkpoint_score < 0 or checkpoint_score > weight:
                errors.append(f"{dim_id}/{checkpoint}: replacement_score outside checkpoint weight")
                continue
        else:
            if "na_status" in obs or "replacement_score" in obs:
                errors.append(f"{dim_id}/{checkpoint}: N/A fields cannot accompany applicable observations")
                continue
            checkpoint_score = weight * Decimal(passed) / Decimal(applicable)
        dimensions[dim_id]["score"] += checkpoint_score
        dimensions[dim_id]["observations"].append(
            {
                "checkpoint": checkpoint,
                "applicable_count": applicable,
                "pass_count": passed,
                "score": str(half(checkpoint_score)),
                "failed_ids": failed_ids,
                "evidence_refs": evidence,
            }
        )
    for dim_id, dim in dimensions.items():
        missing = dim["checkpoints"] - {o["checkpoint"] for o in dim["observations"]}
        if missing:
            errors.append(f"{dim_id}: missing checkpoints: {', '.join(sorted(missing))}")
    if errors:
        raise ValueError("; ".join(errors))

    output_dimensions = []
    total = Decimal("0")
    for dim_id, dim in dimensions.items():
        rounded = half(dim["score"])
        total += rounded
        output_dimensions.append(
            {
                "dimension_id": dim_id,
                "name": dim["name"],
                "score": str(rounded),
                "weight": str(dim["weight"]),
                "minimum": str(dim["minimum"]),
                "passed_minimum": rounded >= dim["minimum"],
                "observations": dim["observations"],
            }
        )
    total = half(total)
    return {
        "schema_version": "2.0-textbook-eval-1",
        "item_type": item_type,
        "total_score": str(total),
        "total_threshold": str(rubric["total_threshold"]),
        "passed_total": total >= Decimal(str(rubric["total_threshold"])),
        "dimensions": output_dimensions,
        "arithmetic": "Decimal + ROUND_HALF_UP(0.5)",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("observations", type=Path, help="JSON payload with item_type and observations")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    try:
        result = score(json.loads(args.observations.read_text(encoding="utf-8")))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

