from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts/create_sg_eval_trial_snapshot.py"
    spec = importlib.util.spec_from_file_location("create_sg_eval_trial_snapshot", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_lint_module():
    path = ROOT / "scripts/run_sg_eval_semantic_lint.py"
    spec = importlib.util.spec_from_file_location("run_sg_eval_semantic_lint", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_trial_snapshot_is_read_only_and_gates_unassigned_roles(tmp_path):
    module = load_module()
    plan = ROOT / "work/knowledge/_meta/sg_eval_trial_batch_plan_20260809.json"
    output = tmp_path / "trial"
    # Invoke the CLI entry point through a subprocess-like argv replacement.
    import sys

    old_argv = sys.argv
    sys.argv = ["create_sg_eval_trial_snapshot.py", "--plan", str(plan), "--output", str(output)]
    try:
        assert module.main() == 0
    finally:
        sys.argv = old_argv
    manifest = json.loads((output / "dg0_snapshot_manifest.json").read_text(encoding="utf-8"))
    assert manifest["snapshot_integrity"] == "pass"
    assert manifest["gate_results"]["DG0"] == "blocked_coordinator_or_roles"
    assert manifest["gate_results"]["DG1"] == "blocked"
    assert manifest["gate_results"]["DG2"] == "blocked"
    assert len(manifest["artifacts"]) == 3
    batch_report = json.loads((output / "batch_report.json").read_text(encoding="utf-8"))
    schema = json.loads((ROOT / "work/knowledge/_meta/schemas/sg_eval_batch_report.schema.json").read_text(encoding="utf-8"))
    assert list(Draft202012Validator(schema).iter_errors(batch_report)) == []
    for artifact in manifest["artifacts"]:
        canonical = ROOT / artifact["canonical_path"]
        assert hashlib.sha256(canonical.read_bytes()).hexdigest() == artifact["canonical_file_sha256"]
        assert (output / "snapshots" / f"{artifact['deliverable_id']}.md").exists()


def test_semantic_lint_runner_passes_automatic_subset_and_keeps_manual_block(tmp_path):
    creator = load_module()
    linter = load_lint_module()
    plan = ROOT / "work/knowledge/_meta/sg_eval_trial_batch_plan_20260809.json"
    output = tmp_path / "trial"
    import sys

    old_argv = sys.argv
    sys.argv = ["create_sg_eval_trial_snapshot.py", "--plan", str(plan), "--output", str(output)]
    try:
        assert creator.main() == 0
    finally:
        sys.argv = old_argv
    old_argv = sys.argv
    sys.argv = ["run_sg_eval_semantic_lint.py", "--trial-dir", str(output)]
    try:
        assert linter.main() == 0
    finally:
        sys.argv = old_argv
    run = json.loads((output / "semantic_lint_run.json").read_text(encoding="utf-8"))
    assert run["result"] == "passed"
    batch = json.loads((output / "batch_report.json").read_text(encoding="utf-8"))
    auto = {item["check_id"]: item["result"] for item in batch["automatic_checks"]}
    assert auto["AUTO-SEMANTIC-LINT"] == "pass"
    assert all(item["result"] == "not_checked" for item in batch["manual_checks"])


def test_semantic_lint_table_negative_is_detected():
    linter = load_lint_module()
    errors = linter.table_lint("| A | B |\n|---|---|\n| only-one |\n")
    assert errors and "expected=2" in errors[0]
