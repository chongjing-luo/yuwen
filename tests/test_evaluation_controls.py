from __future__ import annotations

import importlib.util
import json
import hashlib
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_script(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / filename)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_content_sha_ignores_lifecycle_status_and_key_order():
    mod = load_script("content_sha256", "content_sha256.py")
    fixture = ROOT / "tests/fixtures/content_sha256"
    base = mod.content_sha256(fixture / "base.md")
    assert base == mod.content_sha256(fixture / "status_changed.md")
    assert base == mod.content_sha256(fixture / "key_order_changed.md")
    assert base != mod.content_sha256(fixture / "body_changed.md")
    crlf = fixture / "tmp_crlf.md"
    crlf.write_bytes((fixture / "base.md").read_bytes().replace(b"\n", b"\r\n"))
    try:
        assert base == mod.content_sha256(crlf)
    finally:
        crlf.unlink()
    base_text = (fixture / "base.md").read_text(encoding="utf-8")
    for label, changed in {
        "version": base_text.replace('"0.1.0"', '"0.1.1"'),
        "kp": base_text.replace("KP-ID", "KP-ID-CHANGED"),
        "evidence": base_text.replace("证据", "引文"),
        "quote": base_text.replace("正式主张", "修改后的正式主张"),
    }.items():
        changed_path = fixture / f"tmp_{label}_changed.md"
        changed_path.write_text(changed, encoding="utf-8")
        try:
            assert base != mod.content_sha256(changed_path), label
        finally:
            changed_path.unlink()
    with pytest.raises(mod.ContentShaError):
        mod.content_sha256(fixture / "no_lifecycle.md")
    template = ROOT / "dev/knowledge-extraction-foundation/04_execution/evaluation_artifact_template_2.0-textbook-eval-1.md"
    assert len(mod.content_sha256(template)) == 64


def _all_observations(item_type: str) -> list[dict]:
    rubrics = json.loads((ROOT / "work/knowledge/_meta/rubrics.json").read_text(encoding="utf-8"))["rubrics"]
    result = []
    for dim in rubrics[item_type]["dimensions"]:
        weight = dim["weight"] / len(dim["checkpoints"])
        result.extend(
            {
                "dimension_id": dim["id"],
                "checkpoint": checkpoint,
                "checkpoint_weight": weight,
                "applicable_count": 2,
                "pass_count": 1,
                "failed_ids": ["DEF-1"],
                "evidence_refs": ["EV-1"],
            }
            for checkpoint in dim["checkpoints"]
        )
    return result


def test_fixed_score_recalculates_half_point_and_requires_complete_denominator():
    mod = load_script("score_rubric_fixed", "score_rubric_fixed.py")
    result = mod.score({"item_type": "knowledge_card", "observations": _all_observations("knowledge_card")})
    assert result["total_score"] == "50.0"
    assert all(d["score"] == str(round(float(d["weight"]) / 2, 1)) for d in result["dimensions"])
    broken = _all_observations("knowledge_card")[:-1]
    with pytest.raises(ValueError, match="missing checkpoints"):
        mod.score({"item_type": "knowledge_card", "observations": broken})


def test_fixed_score_rejects_unexplained_zero_over_zero():
    mod = load_script("score_rubric_fixed", "score_rubric_fixed.py")
    observations = _all_observations("knowledge_card")
    observations[0]["applicable_count"] = 0
    observations[0]["pass_count"] = 0
    with pytest.raises(ValueError, match="allowed na_status"):
        mod.score({"item_type": "knowledge_card", "observations": observations})


def test_observation_manifest_covers_all_three_textbook_rubrics():
    manifest = json.loads((ROOT / "work/knowledge/_meta/rubric_observations_2.0-textbook-eval-1.json").read_text(encoding="utf-8"))
    rubrics = json.loads((ROOT / "work/knowledge/_meta/rubrics.json").read_text(encoding="utf-8"))["rubrics"]
    observed = {(o["item_type"], o["dimension_id"], o["checkpoint"]) for o in manifest["observations"]}
    for item_type in ("knowledge_card", "unit_graph", "book_summary"):
        for dim in rubrics[item_type]["dimensions"]:
            for checkpoint in dim["checkpoints"]:
                assert (item_type, dim["id"], checkpoint) in observed


def test_review_binding_rejects_role_overlap_and_accepts_independent_reviews():
    mod = load_script("review_binding", "validate_review_binding_manifest.py")
    schema = json.loads((ROOT / "dev/knowledge-extraction-foundation/04_execution/review_binding_manifest_schema_candidate_20260808_014300.json").read_text(encoding="utf-8"))
    def review(role, reviewer, path, sha):
        return {
            "role": role,
            "reviewer": reviewer,
            "path": path,
            "sha256": sha,
            "decision": "pass",
            "total_score": 92,
            "dimension_scores": {"evidence": 25},
            "hard_rejections": [],
            "p0": 0,
            "p1": 0,
            "p2": 0,
            "sealed_at": "2026-08-09T10:00:00+08:00",
        }
    manifest = {
        "binding_version": "2.0-textbook-eval-1",
        "deliverable_id": "CARD-X3-U01-02",
        "artifact_version": "0.2.2",
        "contract_version": "2.0-textbook",
        "rubric_interpretation_version": "2.0-textbook-eval-1",
        "content_sha256": "a" * 64,
        "pre_merge_file_sha256": "b" * 64,
        "claim_register_sha256": "c" * 64,
        "rubric_sha256": "d" * 64,
        "observation_manifest_sha256": "e" * 64,
        "upstream_snapshot_sha256": "f" * 64,
        "batch_manifest_sha256": "0" * 64,
        "validator_run_id": "VAL-20260809-100000+0800",
        "primary_review": review("primary", "alice", "primary.json", "1" * 64),
        "secondary_review": review("secondary", "bob", "secondary.json", "2" * 64),
        "dg3_decision": "pass",
    }
    assert mod.validate(manifest, schema) == []
    manifest["secondary_review"]["reviewer"] = "alice"
    assert "reviewers must be distinct" in " ".join(mod.validate(manifest, schema))


def test_claim_constraint_and_binding_fixtures_have_positive_negative_examples():
    fixture_dir = ROOT / "work/knowledge/_meta/validation_fixtures/evaluation"
    for name, schema_name in (
        ("claim_register", "claim_register.schema.json"),
        ("constraint_register", "constraint_register.schema.json"),
    ):
        schema = json.loads((ROOT / "work/knowledge/_meta/schemas" / schema_name).read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema)
        valid = json.loads((fixture_dir / f"{name}.valid.json").read_text(encoding="utf-8"))
        invalid = json.loads((fixture_dir / f"{name}.invalid.json").read_text(encoding="utf-8"))
        assert list(validator.iter_errors(valid)) == []
        assert list(validator.iter_errors(invalid))
    binding_mod = load_script("review_binding_fixtures", "validate_review_binding_manifest.py")
    binding_schema = json.loads((ROOT / "dev/knowledge-extraction-foundation/04_execution/review_binding_manifest_schema_candidate_20260808_014300.json").read_text(encoding="utf-8"))
    valid_binding = json.loads((fixture_dir / "review_binding.valid.json").read_text(encoding="utf-8"))
    invalid_binding = json.loads((fixture_dir / "review_binding.invalid.json").read_text(encoding="utf-8"))
    assert binding_mod.validate(valid_binding, binding_schema) == []
    assert binding_mod.validate(invalid_binding, binding_schema)

    receipt_schema = json.loads((ROOT / "work/knowledge/_meta/schemas/dg4_receipt.schema.json").read_text(encoding="utf-8"))
    receipt = {
        "schema_version": "2.0-textbook-eval-1",
        "deliverable_id": "CARD-X3-U01-02",
        "artifact_version": "0.2.2",
        "content_sha256": "a" * 64,
        "pre_merge_file_sha256": "b" * 64,
        "post_merge_file_sha256": "c" * 64,
        "content_sha_unchanged": True,
        "whitelist_diff": [{"path": "status", "category": "front_matter.status", "allowed": True}],
        "review_refs": ["primary.json", "secondary.json"],
        "transition_id": "TR-CARD-X3-U01-02-G4",
        "validator_run_id": "VAL-20260809-100000+0800",
        "impact_items": [],
    }
    assert list(Draft202012Validator(receipt_schema).iter_errors(receipt)) == []
    receipt["content_sha_unchanged"] = False
    assert list(Draft202012Validator(receipt_schema).iter_errors(receipt))


def test_claim_constraint_validator_catches_composite_duplicates():
    mod = load_script("claim_constraint", "validate_claim_constraint_registers.py")
    valid = json.loads((ROOT / "work/knowledge/_meta/validation_fixtures/evaluation/claim_register.valid.json").read_text(encoding="utf-8"))
    duplicate = json.loads(json.dumps(valid))
    duplicate["claims"].append(json.loads(json.dumps(duplicate["claims"][0])))
    errors = mod.validate(duplicate, "claim")
    assert any("duplicate formal claim key" in error for error in errors)


def test_sg_method_schema_templates_and_fixtures():
    schema = json.loads((ROOT / "work/knowledge/_meta/schemas/sg_method_observation.schema.json").read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    fixture_dir = ROOT / "work/knowledge/_meta/validation_fixtures"
    for name in ("sg_method_observation.valid.json", "sg_method_observation.zero_denominator.json", "sg_method_observation.unsupported_claim.json"):
        value = json.loads((fixture_dir / name).read_text(encoding="utf-8"))
        assert list(validator.iter_errors(value)) == [], name
    missing_label_dimension = json.loads((fixture_dir / "sg_method_observation.valid.json").read_text(encoding="utf-8"))
    missing_label_dimension["deliverables"][0]["labels"].pop("four_layer")
    assert list(validator.iter_errors(missing_label_dimension))
    template = json.loads((ROOT / "work/knowledge/_meta/sg_method_observation_template.json").read_text(encoding="utf-8"))
    assert list(validator.iter_errors(template)) == []
    gold_schema = json.loads((ROOT / "work/knowledge/_meta/schemas/sg_method_gold_record.schema.json").read_text(encoding="utf-8"))
    gold_template = json.loads((ROOT / "work/knowledge/_meta/sg_method_gold_record_template.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(gold_schema).iter_errors(gold_template)) == []
    config_schema = json.loads((ROOT / "work/knowledge/_meta/schemas/sg_method_config.schema.json").read_text(encoding="utf-8"))
    config = json.loads((ROOT / "work/knowledge/_meta/sg_method_config_20260809.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(config_schema).iter_errors(config)) == []
    query_schema = json.loads((ROOT / "work/knowledge/_meta/schemas/sg_method_query_manifest.schema.json").read_text(encoding="utf-8"))
    query_manifest = json.loads((ROOT / "work/knowledge/_meta/sg_method_query_manifest_20260809.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(query_schema).iter_errors(query_manifest)) == []


def test_sg_method_metrics_have_positive_and_negative_boundaries():
    mod = load_script("score_sg_method_metrics", "score_sg_method_metrics.py")
    config = json.loads((ROOT / "work/knowledge/_meta/sg_method_config_20260809.json").read_text(encoding="utf-8"))
    config["bootstrap"]["iterations"] = 25
    fixture_dir = ROOT / "work/knowledge/_meta/validation_fixtures"
    positive = json.loads((fixture_dir / "sg_method_observation.valid.json").read_text(encoding="utf-8"))
    result = mod.main_score(positive, config)
    assert result["metric_status"] == "passed"
    assert result["status"] == "blocked"
    assert result["query_set_check"]["valid"]
    assert result["point_estimates"]["unsupported_claim_rate"]["value"] == 0

    # A complete synthetic control record can pass only after every provenance gate is satisfied.
    eligible = json.loads(json.dumps(positive))
    card_seed = eligible["deliverables"][0]
    graph_seed = eligible["deliverables"][1]
    rows = []
    for deliverable_id, book_code, material_type, seed in (
        ("CARD-X1-U01-02", "X1", "card", card_seed),
        ("CARD-B1-U05-01", "B1", "card", card_seed),
        ("UNIT-X1-U01", "X1", "unit_graph", graph_seed),
        ("BOOK-X1", "X1", "book_summary", graph_seed),
    ):
        row = json.loads(json.dumps(seed))
        row.update({"deliverable_id": deliverable_id, "book_code": book_code, "material_type": material_type, "gold_id": f"GOLD-{deliverable_id}", "gold_sha256": "a" * 64})
        rows.append(row)
    for index in range(10):
        row = json.loads(json.dumps(card_seed))
        row.update({"deliverable_id": f"CARD-SYN-{index:02d}", "book_code": "B1", "material_type": "card", "gold_id": f"GOLD-CARD-SYN-{index:02d}", "gold_sha256": "a" * 64})
        rows.append(row)
    for index in range(3):
        row = json.loads(json.dumps(graph_seed))
        row.update({"deliverable_id": f"UNIT-SYN-{index:02d}", "book_code": "X1", "material_type": "unit_graph", "gold_id": f"GOLD-UNIT-SYN-{index:02d}", "gold_sha256": "a" * 64})
        rows.append(row)
    eligible["deliverables"] = rows
    eligible["gold_control"] = {
        "sealed": True,
        "manifest_sha256": "b" * 64,
        "annotator_a": "gold-a",
        "annotator_b": "gold-b",
        "adjudicator": "gold-adjudicator",
        "krippendorff_alpha": 0.9,
        "kp_pair_f1": 0.9,
        "contamination_status": "clean",
    }
    config["status"] = "pilot"
    config["sampling"]["selection_status"] = "sealed"
    config["sampling"]["candidate_ids"] = [row["deliverable_id"] for row in rows]
    config["gold_manifest_sha256"] = "b" * 64
    config["query_manifest_sha256"] = hashlib.sha256((ROOT / "work/knowledge/_meta/sg_method_query_manifest_20260809.json").read_bytes()).hexdigest()
    config["roles"] = {
        "gold_annotator_a": "gold-a",
        "gold_annotator_b": "gold-b",
        "adjudicator": "gold-adjudicator",
        "query_evaluators": ["eval-syn"],
        "external_teachers": ["teacher-1", "teacher-2", "teacher-3"],
    }
    result = mod.main_score(eligible, config)
    assert result["metric_status"] == "passed"
    assert result["status"] == "passed"
    assert result["sampling_check"]["valid"]
    assert result["gold_control_check"]["valid"]
    assert result["role_check"]["valid"]

    assert mod.f1(0, 1, 1)["f1"] == {"value": 0.0, "status": "computed", "reason": None}

    blocked_config = json.loads(json.dumps(config))
    blocked_config["status"] = "blocked"
    blocked = mod.main_score(eligible, blocked_config)
    assert blocked["metric_status"] == "passed"
    assert blocked["status"] == "blocked"
    assert blocked["eligibility"]["eligible"] is False

    zero = json.loads((fixture_dir / "sg_method_observation.zero_denominator.json").read_text(encoding="utf-8"))
    zero_result = mod.main_score(zero, config)
    assert zero_result["point_estimates"]["key_fact_recall"]["status"] == "N/A"
    assert zero_result["bootstrap"]["status"] == "N/A"
    assert zero_result["metric_status"] == "blocked"
    assert zero_result["status"] == "blocked"

    unsupported = json.loads((fixture_dir / "sg_method_observation.unsupported_claim.json").read_text(encoding="utf-8"))
    unsupported_result = mod.main_score(unsupported, config)
    assert unsupported_result["point_estimates"]["unsupported_claim_rate"]["value"] == 1
    assert unsupported_result["gates"]["unsupported_claim_rate"] is False
    assert unsupported_result["gates"]["teachers"] is False

    incomplete = json.loads(json.dumps(positive))
    incomplete["queries"][0]["completed"] = False
    incomplete["queries"][0]["fact_evidence_correct"] = True
    incomplete_result = mod.main_score(incomplete, config)
    assert any("cannot be fact/evidence correct" in error for error in incomplete_result["semantic_errors"])
    assert incomplete_result["gates"]["semantic_integrity"] is False

    overcount = json.loads(json.dumps(positive))
    overcount["deliverables"][0]["claim_evidence"] = {"correct": 2, "total": 1}
    overcount_result = mod.main_score(overcount, config)
    assert any("correct exceeds total" in error for error in overcount_result["semantic_errors"])

    duplicate_teacher = json.loads(json.dumps(positive))
    duplicate_teacher["teachers"][1]["evaluator_id"] = duplicate_teacher["teachers"][0]["evaluator_id"]
    duplicate_teacher_result = mod.main_score(duplicate_teacher, config)
    assert any("duplicate teacher" in error for error in duplicate_teacher_result["semantic_errors"])
