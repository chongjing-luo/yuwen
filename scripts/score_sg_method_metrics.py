#!/usr/bin/env python3
"""Compute SG-METHOD point estimates and clustered bootstrap intervals.

This script scores only pre-adjudicated numeric observations.  It never creates
Gold annotations or treats an empty denominator as 100%; empty inputs are
reported as ``N/A`` and the overall run remains blocked/not_run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import statistics
from pathlib import Path
from typing import Iterable

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "work/knowledge/_meta/sg_method_config_20260809.json"
SCHEMA = ROOT / "work/knowledge/_meta/schemas/sg_method_observation.schema.json"
QUERY_MANIFEST = ROOT / "work/knowledge/_meta/sg_method_query_manifest_20260809.json"
QUERY_SCHEMA = ROOT / "work/knowledge/_meta/schemas/sg_method_query_manifest.schema.json"
LABEL_DIMENSIONS = ("primary_dimension", "knowledge_type", "four_layer")


def ratio(numerator: int, denominator: int) -> dict:
    if denominator == 0:
        return {"value": None, "numerator": numerator, "denominator": denominator, "status": "N/A", "reason": "zero denominator"}
    return {"value": numerator / denominator, "numerator": numerator, "denominator": denominator, "status": "computed"}


def f1(tp: int, fp: int, fn: int) -> dict:
    precision = ratio(tp, tp + fp)
    recall = ratio(tp, tp + fn)
    if precision["value"] is None or recall["value"] is None:
        value = None
        status = "N/A"
        reason = "zero denominator"
    elif precision["value"] + recall["value"] == 0:
        value = 0.0
        status = "computed"
        reason = None
    else:
        value = 2 * precision["value"] * recall["value"] / (precision["value"] + recall["value"])
        status = "computed"
        reason = None
    return {"precision": precision, "recall": recall, "f1": {"value": value, "status": status, "reason": reason}, "tp": tp, "fp": fp, "fn": fn}


def aggregate(rows: Iterable[dict], label_universe: dict[str, list[str]] | None = None) -> dict:
    rows = list(rows)
    def sum_pair(field: str) -> tuple[int, int]:
        return sum(r[field]["matched"] for r in rows), sum(r[field]["gold"] for r in rows)
    facts = sum_pair("facts")
    tasks = sum_pair("tasks")
    kp = {key: sum(r["kp"][key] for r in rows) for key in ("tp", "fp", "fn")}
    claims_correct = sum(r["claim_evidence"]["correct"] for r in rows)
    claims_total = sum(r["claim_evidence"]["total"] for r in rows)
    quotes_correct = sum(r["quotes"]["correct"] for r in rows)
    quotes_total = sum(r["quotes"]["total"] for r in rows)
    rel = {key: sum(r["relations"][key] for r in rows) for key in ("tp", "fp", "fn")}
    unsupported = sum(r["unsupported_claims"]["count"] for r in rows)
    asserted = sum(r["unsupported_claims"]["total"] for r in rows)
    label_scores_by_dimension = {}
    label_universe = label_universe or {dimension: [] for dimension in LABEL_DIMENSIONS}
    for dimension in LABEL_DIMENSIONS:
        scores = []
        observed_labels = {label for r in rows for label in r["labels"][dimension]}
        label_names = label_universe.get(dimension) or sorted(observed_labels)
        for label in label_names:
            counts = {key: sum(r["labels"][dimension].get(label, {}).get(key, 0) for r in rows) for key in ("tp", "fp", "fn")}
            metric = f1(**counts)
            if metric["f1"]["value"] is not None:
                scores.append(metric["f1"]["value"])
        label_scores_by_dimension[dimension] = ratio(sum(scores), len(scores)) if scores else {"value": None, "numerator": 0, "denominator": 0, "status": "N/A", "reason": f"no {dimension} label observations"}
    label_scores = [score["value"] for score in label_scores_by_dimension.values() if score["value"] is not None]
    return {
        "deliverable_count": len(rows),
        "key_fact_recall": ratio(facts[0], facts[1]),
        "task_recall": ratio(tasks[0], tasks[1]),
        "kp": f1(**kp),
        "claim_evidence_accuracy": ratio(claims_correct, claims_total),
        "quote_locator_accuracy": ratio(quotes_correct, quotes_total),
        "relation_precision": ratio(rel["tp"], rel["tp"] + rel["fp"]),
        "relation_diagnostic": f1(**rel),
        "unsupported_claim_rate": ratio(unsupported, asserted),
        "label_macro_f1": ratio(sum(label_scores), len(label_scores)) if label_scores else {"value": None, "numerator": 0, "denominator": 0, "status": "N/A", "reason": "no label observations"},
        "label_macro_f1_by_dimension": label_scores_by_dimension,
    }


def percentile(values: list[float], p: float) -> float | None:
    if not values:
        return None
    values = sorted(values)
    index = (len(values) - 1) * p
    low, high = int(index), min(int(index) + 1, len(values) - 1)
    return values[low] + (values[high] - values[low]) * (index - low)


def bootstrap(rows: list[dict], iterations: int, seed: int, label_universe: dict[str, list[str]] | None = None) -> dict:
    strata: dict[tuple[str, str], list[dict]] = {}
    for row in rows:
        strata.setdefault((row["book_code"], row["material_type"]), []).append(row)
    if not rows or not strata:
        return {"iterations": iterations, "seed": seed, "unit": "deliverable", "status": "N/A", "reason": "no deliverable observations"}
    rng = random.Random(seed)
    values = {"kp_precision": [], "kp_recall": [], "kp_f1": [], "label_macro_f1": []}
    invalid_iterations = 0
    for _ in range(iterations):
        sample = [rng.choice(group) for group in strata.values() for _ in range(len(group))]
        aggregate_sample = aggregate(sample, label_universe)
        metric = aggregate_sample["kp"]
        sample_values = {
            "kp_precision": metric["precision"]["value"],
            "kp_recall": metric["recall"]["value"],
            "kp_f1": metric["f1"]["value"],
            "label_macro_f1": aggregate_sample["label_macro_f1"]["value"],
        }
        if any(value is None for value in sample_values.values()):
            invalid_iterations += 1
            continue
        for name in values:
            values[name].append(sample_values[name])
    if invalid_iterations:
        return {
            "iterations": iterations,
            "seed": seed,
            "unit": "deliverable",
            "status": "N/A",
            "reason": "one or more bootstrap resamples had a zero denominator",
            "invalid_iterations": invalid_iterations,
        }
    return {
        "iterations": iterations,
        "seed": seed,
        "unit": "deliverable",
        "status": "computed",
        "valid_iterations": len(values["kp_f1"]),
        "strata": [f"{book}:{material}" for book, material in sorted(strata)],
        "stratum_sizes": {f"{book}:{material}": len(group) for (book, material), group in sorted(strata.items())},
        "intervals_95": {name: {"lower": percentile(vals, 0.025), "upper": percentile(vals, 0.975)} for name, vals in values.items()},
        "note": "Stratified within book_code × material_type; same card KP are not independent samples.",
    }


def query_metrics(queries: list[dict]) -> dict:
    if not queries:
        return {"status": "N/A", "reason": "no query observations"}
    completed = sum(bool(q["completed"]) for q in queries)
    correct = sum(bool(q["completed"] and q["fact_evidence_correct"]) for q in queries)
    under = sum(q["seconds"] <= 120 for q in queries)
    seconds = [q["seconds"] for q in queries]
    return {
        "status": "computed",
        "count": len(queries),
        "unique_query_ids": len({q["query_id"] for q in queries}),
        "completion": ratio(completed, len(queries)),
        "fact_evidence_accuracy": ratio(correct, len(queries)),
        "under_120_seconds": ratio(under, len(queries)),
        "median_seconds": statistics.median(seconds),
        "p90_seconds": percentile(seconds, 0.9),
    }


def teacher_metrics(teachers: list[dict]) -> dict:
    if not teachers:
        return {"status": "N/A", "reason": "no external teacher observations"}
    scores = [t["usable_score"] for t in teachers]
    return {"status": "computed", "count": len(teachers), "median_usable_score": statistics.median(scores), "serious_error_count": sum(t["serious_error"] for t in teachers)}


def _query_set_check(queries: list[dict], config: dict) -> dict:
    """Check that observations cover the frozen 12-query manifest exactly."""
    manifest_bytes = QUERY_MANIFEST.read_bytes()
    manifest = json.loads(manifest_bytes.decode("utf-8"))
    manifest_schema = json.loads(QUERY_SCHEMA.read_text(encoding="utf-8"))
    manifest_schema_errors = [error.message for error in Draft202012Validator(manifest_schema).iter_errors(manifest)]
    expected = [q["query_id"] for q in manifest["queries"]]
    observed = [q["query_id"] for q in queries]
    missing = sorted(set(expected) - set(observed))
    unexpected = sorted(set(observed) - set(expected))
    duplicates = sorted({qid for qid in observed if observed.count(qid) > 1})
    manifest_ids = [q["query_id"] for q in manifest["queries"]]
    manifest_duplicates = sorted({qid for qid in manifest_ids if manifest_ids.count(qid) > 1})
    target_ids = sorted({artifact_id for query in manifest["queries"] for artifact_id in query["target_artifact_ids"]})
    candidate_ids = set(config["sampling"].get("candidate_ids") or [])
    manifest_sha_match = bool(config.get("query_manifest_sha256")) and config.get("query_manifest_sha256") == hashlib.sha256(manifest_bytes).hexdigest()
    return {
        "valid": set(observed) == set(expected) and not missing and not unexpected and not duplicates,
        "manifest_frozen": manifest.get("frozen") is True,
        "manifest_schema_valid": not manifest_schema_errors,
        "manifest_schema_errors": manifest_schema_errors,
        "manifest_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
        "manifest_query_ids_unique": not manifest_duplicates,
        "manifest_sha_match": manifest_sha_match,
        "target_artifact_ids": target_ids,
        "target_artifacts_in_candidate_set": set(target_ids) <= candidate_ids,
        "expected_count": len(expected),
        "observed_count": len(observed),
        "missing": missing,
        "unexpected": unexpected,
        "duplicates": duplicates,
        "manifest_duplicates": manifest_duplicates,
    }


def _semantic_checks(observation: dict, label_universe: dict[str, list[str]] | None = None) -> list[str]:
    """Checks not expressible as JSON Schema without making the schema unwieldy."""
    errors: list[str] = []
    deliverable_ids = [row["deliverable_id"] for row in observation["deliverables"]]
    if len(deliverable_ids) != len(set(deliverable_ids)):
        errors.append("duplicate deliverable_id")
    query_ids = [row["query_id"] for row in observation["queries"]]
    if len(query_ids) != len(set(query_ids)):
        errors.append("duplicate query_id")
    for row in observation["deliverables"]:
        for field in ("facts", "tasks"):
            if row[field]["matched"] > row[field]["gold"]:
                errors.append(f"{row['deliverable_id']} {field}.matched exceeds gold")
        if row["unsupported_claims"]["count"] > row["unsupported_claims"]["total"]:
            errors.append(f"{row['deliverable_id']} unsupported claim count exceeds total")
        for field in ("claim_evidence", "quotes"):
            if row[field]["correct"] > row[field]["total"]:
                errors.append(f"{row['deliverable_id']} {field}.correct exceeds total")
        for dimension in LABEL_DIMENSIONS:
            if not row["labels"].get(dimension):
                errors.append(f"{row['deliverable_id']} has no {dimension} label observations")
            if label_universe:
                missing_labels = sorted(set(label_universe[dimension]) - set(row["labels"].get(dimension, {})))
                if missing_labels:
                    errors.append(f"{row['deliverable_id']} missing {dimension} label categories: {', '.join(missing_labels)}")
    for query in observation["queries"]:
        if not query["completed"] and query["fact_evidence_correct"]:
            errors.append(f"{query['query_id']} cannot be fact/evidence correct when incomplete")
    teacher_ids = [teacher["evaluator_id"] for teacher in observation["teachers"]]
    if len(teacher_ids) != len(set(teacher_ids)):
        errors.append("duplicate teacher evaluator_id")
    return errors


def _per_deliverable_diagnostics(rows: list[dict], label_universe: dict[str, list[str]] | None) -> list[dict]:
    diagnostics = []
    for row in rows:
        metrics = aggregate([row], label_universe)
        statuses = {
            "key_fact_recall": metrics["key_fact_recall"]["status"],
            "task_recall": metrics["task_recall"]["status"],
            "kp_precision": metrics["kp"]["precision"]["status"],
            "kp_recall": metrics["kp"]["recall"]["status"],
            "kp_f1": metrics["kp"]["f1"]["status"],
            "label_macro_f1": metrics["label_macro_f1"]["status"],
            "claim_evidence_accuracy": metrics["claim_evidence_accuracy"]["status"],
            "quote_locator_accuracy": metrics["quote_locator_accuracy"]["status"],
            "relation_precision": metrics["relation_precision"]["status"],
            "unsupported_claim_rate": metrics["unsupported_claim_rate"]["status"],
        }
        for dimension, metric in metrics["label_macro_f1_by_dimension"].items():
            statuses[f"label_macro_f1:{dimension}"] = metric["status"]
        diagnostics.append({
            "deliverable_id": row["deliverable_id"],
            "book_code": row["book_code"],
            "material_type": row["material_type"],
            "metrics": metrics,
            "statuses": statuses,
            "zero_denominator_metrics": sorted(name for name, status in statuses.items() if status == "N/A"),
        })
    return diagnostics


def _stratum_point_estimates(rows: list[dict], label_universe: dict[str, list[str]] | None) -> dict[str, dict]:
    strata: dict[str, list[dict]] = {}
    for row in rows:
        key = f"{row['book_code']}:{row['material_type']}"
        strata.setdefault(key, []).append(row)
    return {key: {"deliverable_count": len(group), "metrics": aggregate(group, label_universe)} for key, group in sorted(strata.items())}


def _sampling_check(observation: dict, config: dict) -> dict:
    sampling = config["sampling"]
    rows = observation["deliverables"]
    ids = [row["deliverable_id"] for row in rows]
    card_types = {"card", "knowledge_card"}
    unit_types = {"unit_graph", "unit"}
    book_types = {"book_summary", "book"}
    counts = {
        "card": sum(row["material_type"] in card_types for row in rows),
        "unit_graph": sum(row["material_type"] in unit_types for row in rows),
        "book_summary": sum(row["material_type"] in book_types for row in rows),
    }
    expected = {
        "card": sampling["card_count"],
        "unit_graph": sampling["unit_graph_count"],
        "book_summary": sampling["book_summary_count"],
    }
    candidate_ids = sampling.get("candidate_ids") or []
    return {
        "sealed": sampling.get("selection_status") == "sealed",
        "counts": counts,
        "expected_counts": expected,
        "counts_match": counts == expected,
        "candidate_count": len(candidate_ids),
        "candidate_ids_match": set(candidate_ids) == set(ids) and len(candidate_ids) == len(ids),
        "valid": sampling.get("selection_status") == "sealed" and counts == expected and set(candidate_ids) == set(ids) and len(candidate_ids) == len(ids),
    }


def _gold_control_check(observation: dict, config: dict) -> dict:
    gold = observation.get("gold_control") or {}
    required = {"sealed", "manifest_sha256", "annotator_a", "annotator_b", "adjudicator", "krippendorff_alpha", "kp_pair_f1", "contamination_status"}
    complete = required <= set(gold)
    role_values = [gold.get("annotator_a"), gold.get("annotator_b"), gold.get("adjudicator")]
    roles_distinct = len(set(role_values)) == 3 and all(role_values)
    sha_match = bool(config.get("gold_manifest_sha256")) and gold.get("manifest_sha256") == config.get("gold_manifest_sha256")
    missing_deliverable_gold = sorted(row["deliverable_id"] for row in observation["deliverables"] if not row.get("gold_id") or not row.get("gold_sha256"))
    return {
        "complete": complete,
        "sealed": gold.get("sealed") is True,
        "roles_distinct": roles_distinct,
        "alpha_pass": gold.get("krippendorff_alpha", -1) >= 0.80,
        "kp_pair_f1_pass": gold.get("kp_pair_f1", -1) >= 0.85,
        "contamination_clean": gold.get("contamination_status") == "clean",
        "sha_match": sha_match,
        "missing_deliverable_gold": missing_deliverable_gold,
        "valid": complete and gold.get("sealed") is True and roles_distinct and gold.get("krippendorff_alpha", -1) >= 0.80 and gold.get("kp_pair_f1", -1) >= 0.85 and gold.get("contamination_status") == "clean" and sha_match and not missing_deliverable_gold,
    }


def _role_check(observation: dict, config: dict) -> dict:
    roles = config["roles"]
    query_ids = [query["evaluator_id"] for query in observation["queries"]]
    teacher_ids = [teacher["evaluator_id"] for teacher in observation["teachers"]]
    configured_queries = roles.get("query_evaluators", [])
    configured_teachers = roles.get("external_teachers", [])
    gold_roles = {roles.get("gold_annotator_a"), roles.get("gold_annotator_b"), roles.get("adjudicator")} - {None}
    distinct_observers = len(teacher_ids) == len(set(teacher_ids))
    return {
        "query_roles_match": bool(query_ids) and set(query_ids) == set(configured_queries),
        "teacher_roles_match": set(teacher_ids) == set(configured_teachers) and len(teacher_ids) == len(configured_teachers),
        "observer_ids_distinct": distinct_observers,
        "gold_roles_configured": len(gold_roles) == 3,
        "no_gold_observer_overlap": not (gold_roles & (set(query_ids) | set(teacher_ids))),
        "no_query_teacher_overlap": not (set(query_ids) & set(teacher_ids)),
        "valid": bool(query_ids) and set(query_ids) == set(configured_queries) and set(teacher_ids) == set(configured_teachers) and len(teacher_ids) == len(configured_teachers) and distinct_observers and len(gold_roles) == 3 and not (gold_roles & (set(query_ids) | set(teacher_ids))) and not (set(query_ids) & set(teacher_ids)),
    }


def main_score(observation: dict, config: dict) -> dict:
    rows = observation["deliverables"]
    label_universe = config.get("label_universe")
    point = aggregate(rows, label_universe)
    per_deliverable = _per_deliverable_diagnostics(rows, label_universe)
    query = query_metrics(observation["queries"])
    teachers = teacher_metrics(observation["teachers"])
    query_set = _query_set_check(observation["queries"], config)
    semantic_errors = _semantic_checks(observation, label_universe)
    for diagnostic in per_deliverable:
        if diagnostic["zero_denominator_metrics"]:
            semantic_errors.append(f"{diagnostic['deliverable_id']} has zero denominators in: {', '.join(diagnostic['zero_denominator_metrics'])}")
    sampling = _sampling_check(observation, config)
    gold = _gold_control_check(observation, config)
    roles = _role_check(observation, config)
    thresholds = config["thresholds"]
    metric_gates = {
        "key_fact_task_recall": point["key_fact_recall"]["value"] == thresholds["key_fact_task_recall"] and point["task_recall"]["value"] == thresholds["key_fact_task_recall"],
        "kp_precision": (point["kp"]["precision"]["value"] or -1) >= thresholds["kp_precision"],
        "kp_recall": (point["kp"]["recall"]["value"] or -1) >= thresholds["kp_recall"],
        "kp_f1": (point["kp"]["f1"]["value"] or -1) >= thresholds["kp_f1"],
        "label_macro_f1": (point["label_macro_f1"]["value"] or -1) >= thresholds["label_macro_f1"],
        "claim_evidence_accuracy": point["claim_evidence_accuracy"]["value"] == thresholds["claim_evidence_accuracy"],
        "quote_locator_accuracy": point["quote_locator_accuracy"]["value"] == thresholds["quote_locator_accuracy"],
        "relation_precision": (point["relation_precision"]["value"] or -1) >= thresholds["relation_precision"],
        "unsupported_claim_rate": point["unsupported_claim_rate"]["value"] == thresholds["unsupported_claim_rate"],
        "queries": query.get("status") == "computed" and query_set["valid"] and query["count"] == 12 and (query["completion"]["value"] or -1) >= thresholds["query_completion"] and (query["fact_evidence_accuracy"]["value"] or -1) >= thresholds["query_fact_evidence_accuracy"] and query["under_120_seconds"]["numerator"] >= thresholds["query_under_120_seconds"],
        "teachers": teachers.get("status") == "computed" and len(observation["teachers"]) >= 3 and teachers["median_usable_score"] >= thresholds["teacher_usability_median"] and teachers["serious_error_count"] == thresholds["teacher_serious_error_count"],
    }
    if semantic_errors:
        metric_gates["semantic_integrity"] = False
    else:
        metric_gates["semantic_integrity"] = True
    metric_status = "passed" if all(metric_gates.values()) else "blocked"
    eligibility_reasons = []
    if observation["status"] != "complete":
        eligibility_reasons.append(f"observation status is {observation['status']}")
    if config["status"] not in {"pilot", "passed"}:
        eligibility_reasons.append(f"config status is {config['status']}")
    if not sampling["valid"]:
        eligibility_reasons.append("sampling is not sealed or does not match 12 cards + 4 unit graphs + 1 book summary")
    if not gold["valid"]:
        eligibility_reasons.append("Gold is not sealed/independent/clean or Gold manifest SHA does not match")
    if not roles["valid"]:
        eligibility_reasons.append("observed evaluator IDs do not match configured independent roles")
    if not query_set["manifest_schema_valid"] or not query_set["manifest_frozen"] or not query_set["manifest_query_ids_unique"] or not query_set["manifest_sha_match"] or not query_set["target_artifacts_in_candidate_set"]:
        eligibility_reasons.append("fixed query manifest is not frozen, hashed, unique, or candidate-bound")
    overall_status = "passed" if metric_status == "passed" and not eligibility_reasons else "blocked"
    return {
        "schema_version": "sg-method-metrics-0.1",
        "method_id": observation["method_id"],
        "status": overall_status,
        "metric_status": metric_status,
        "point_estimates": point,
        "stratum_point_estimates": _stratum_point_estimates(rows, label_universe),
        "per_deliverable": per_deliverable,
        "bootstrap": bootstrap(rows, config["bootstrap"]["iterations"], config["bootstrap"]["seed"], label_universe),
        "query_metrics": query,
        "query_set_check": query_set,
        "teacher_metrics": teachers,
        "sampling_check": sampling,
        "gold_control_check": gold,
        "role_check": roles,
        "gates": metric_gates,
        "semantic_errors": semantic_errors,
        "eligibility": {"eligible": not eligibility_reasons, "reasons": eligibility_reasons},
        "denominator_rule": "N/A + reason for zero denominators; no 0/0 is converted to 100%.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("observation", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    observation = json.loads(args.observation.read_text(encoding="utf-8"))
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(observation)]
    if errors:
        parser.error("observation schema errors: " + "; ".join(errors))
    result = main_score(observation, config)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
