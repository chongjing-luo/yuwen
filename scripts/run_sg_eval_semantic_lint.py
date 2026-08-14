#!/usr/bin/env python3
"""Run the machine portion of SG-EVAL semantic lint on a trial package.

Manual checks stay explicitly ``not_checked``.  A successful command therefore
does not turn DG1/DG2 into a pass; it only proves the automatic subset and
updates the batch report with that distinction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
TRIAL = ROOT / "work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01"
LIFECYCLE_START = "<!-- lifecycle-metadata:start -->"
LIFECYCLE_END = "<!-- lifecycle-metadata:end -->"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def parse_frontmatter(text: str) -> dict:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.startswith("---\n"):
        raise ValueError("missing front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing front matter closing marker")
    data = yaml.safe_load(text[4:end])
    if not isinstance(data, dict):
        raise ValueError("front matter is not an object")
    return data


def table_lint(text: str) -> list[str]:
    """Check contiguous Markdown tables for stable column counts."""
    lines = text.splitlines()
    errors: list[str] = []
    i = 0
    table_count = 0
    while i + 1 < len(lines):
        header = lines[i].strip()
        separator = lines[i + 1].strip()
        if not (header.startswith("|") and header.endswith("|") and separator.startswith("|") and "---" in separator):
            i += 1
            continue
        table_count += 1
        expected = len(header.split("|")[1:-1])
        if expected == 0:
            errors.append(f"line {i+1}: empty table header")
            i += 1
            continue
        j = i + 2
        while j < len(lines):
            row = lines[j].strip()
            if not row.startswith("|") or not row.endswith("|"):
                break
            actual = len(row.split("|")[1:-1])
            if actual != expected:
                errors.append(f"line {j+1}: table columns={actual}, expected={expected}")
            j += 1
        i = j
    if table_count == 0:
        errors.append("no Markdown table found")
    return errors


def evidence_lint(text: str, claim_path: Path, allow_scoped_short_refs: bool = False) -> list[str]:
    evidence_rows = set(re.findall(r"^\|\s*(EV-[A-Z0-9][A-Z0-9-]*)\s*\|", text, re.MULTILINE))
    referenced = set(re.findall(r"EV-[A-Z0-9][A-Z0-9-]*", text))
    missing = sorted(
        x for x in referenced
        if x not in evidence_rows and not (allow_scoped_short_refs and re.fullmatch(r"EV-\d{3}", x))
    )
    try:
        claims = json.loads(claim_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"claim register unreadable: {exc}"]
    for claim in claims.get("claims", []):
        for ev in claim.get("evidence_refs", []):
            if ev not in evidence_rows and not (allow_scoped_short_refs and re.fullmatch(r"EV-\d{3}", ev)):
                missing.append(f"claim:{ev}")
    return sorted(set(missing))


def ledger_map() -> dict[str, dict]:
    path = ROOT / "work/knowledge/_meta/deliverables.jsonl"
    return {r["deliverable_id"]: r for r in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())}


def register_schema_errors(claim_path: Path, constraint_path: Path) -> list[str]:
    errors: list[str] = []
    for path, schema_name in ((claim_path, "claim_register.schema.json"), (constraint_path, "constraint_register.schema.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            schema = json.loads((ROOT / "work/knowledge/_meta/schemas" / schema_name).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{display(path)}: unreadable register/schema: {exc}")
            continue
        errors.extend(f"{display(path)}: {error.message}" for error in Draft202012Validator(schema).iter_errors(payload))
    return errors


def check_one(artifact: dict, rows: dict[str, dict]) -> tuple[dict, list[str], list[str]]:
    did = artifact["deliverable_id"]
    path = ROOT / artifact["snapshot_path"]
    if not path.exists():
        path = Path(artifact["snapshot_path"])
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    front = parse_frontmatter(text)
    row = rows[did]
    front_id = front.get("card_id", front.get("unit_id"))
    metadata_ok = front_id == did and front.get("status") == row.get("status") and front.get("version") == row.get("version") and front.get("reviewers", []) == row.get("reviewers", [])
    lifecycle_ok = text.count(LIFECYCLE_START) == 1 and text.count(LIFECYCLE_END) == 1
    table_errors = table_lint(text)
    claim_path = ROOT / artifact["claim_register_path"]
    if not claim_path.exists():
        claim_path = Path(artifact["claim_register_path"])
    ev_errors = evidence_lint(text, claim_path, allow_scoped_short_refs=artifact.get("artifact_type") == "unit_graph")
    constraint_path = ROOT / artifact["constraint_register_path"]
    if not constraint_path.exists():
        constraint_path = Path(artifact["constraint_register_path"])
    schema_errors = register_schema_errors(claim_path, constraint_path)
    checks = [
        {"check_id": "SL-LIFECYCLE-UNIQUE", "domain": "version_history", "mode": "automatic", "result": "pass" if lifecycle_ok else "fail", "message": "Exactly one lifecycle-metadata block is present.", "evidence_refs": [display(path)]},
        {"check_id": "SL-MARKDOWN-TABLES", "domain": "markdown_table", "mode": "automatic", "result": "pass" if not table_errors else "fail", "message": "Markdown table column-count scan.", "evidence_refs": [display(path)] if not table_errors else table_errors, "owner": "semantic-lint"},
        {"check_id": "SL-FRONT-LEDGER-AUTO", "domain": "front_matter_ledger", "mode": "automatic", "result": "pass" if metadata_ok else "fail", "message": "Front matter ID/status/version/reviewer comparison.", "evidence_refs": [display(path)]},
        {"check_id": "SL-CLAIM-EV-REFS", "domain": "claim_kp_ev", "mode": "automatic", "result": "pass" if not ev_errors else "fail", "message": "Machine scan that referenced EV IDs resolve to evidence rows.", "evidence_refs": [display(claim_path)] if not ev_errors else ev_errors},
        {"check_id": "SL-REGISTERS-SCHEMA", "domain": "claim_kp_ev", "mode": "automatic", "result": "pass" if not schema_errors else "fail", "message": "Claim and Constraint registers validate against their versioned JSON Schemas.", "evidence_refs": [display(claim_path), display(constraint_path)] if not schema_errors else schema_errors},
        {"check_id": "SL-CLAIM-KP-EV", "domain": "claim_kp_ev", "mode": "manual_required", "result": "not_checked", "message": "Formal Claim classification, locator precision and denominator sealing remain human checks.", "evidence_refs": [], "owner": "trial-reviewer"},
        {"check_id": "SL-Q-LOCATOR", "domain": "q_locator", "mode": "manual_required", "result": "not_checked", "message": "Q quote span and canonical locator visual verification remain human checks.", "evidence_refs": [], "owner": "trial-reviewer"},
        {"check_id": "SL-M0-NA", "domain": "m0_na", "mode": "manual_required", "result": "not_checked", "message": "M0/N/A semantics remain human checks.", "evidence_refs": [], "owner": "trial-reviewer"},
        {"check_id": "SL-TEACHING-PROMPT", "domain": "teaching_prompt", "mode": "manual_required", "result": "not_checked", "message": "Teaching-prompt boundary remains a human check.", "evidence_refs": [], "owner": "trial-reviewer"},
    ]
    report = {"schema_version": "2.0-textbook-eval-1", "deliverable_id": did, "artifact_version": row["version"], "result": "blocked", "checks": checks, "warnings": ["Automatic lint does not close manual DG1/DG2 checks."]}
    return report, errors + table_errors + ev_errors + schema_errors + ([] if metadata_ok else ["front matter/ledger mismatch"]), schema_errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--trial-dir", type=Path, default=TRIAL)
    args = parser.parse_args()
    trial = args.trial_dir
    manifest_path = trial / "dg0_snapshot_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    rows = ledger_map()
    all_errors: list[str] = []
    reports = []
    all_schema_errors: list[str] = []
    for artifact in manifest["artifacts"]:
        report, errors, schema_errors = check_one(artifact, rows)
        out = trial / "semantic_lint" / f"{artifact['deliverable_id']}.json"
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        reports.append((artifact["deliverable_id"], report, errors))
        all_errors.extend(f"{artifact['deliverable_id']}: {e}" for e in errors)
        all_schema_errors.extend(f"{artifact['deliverable_id']}: {e}" for e in schema_errors)
    batch_path = trial / "batch_report.json"
    batch = json.loads(batch_path.read_text(encoding="utf-8"))
    auto_result = "pass" if not all_errors else "fail"
    batch["automatic_checks"] = [x for x in batch["automatic_checks"] if x["check_id"] not in {"AUTO-CLAIM-CONSTRAINT-SCHEMA", "AUTO-SEMANTIC-LINT"}]
    batch["automatic_checks"].extend([
        {"check_id": "AUTO-CLAIM-CONSTRAINT-SCHEMA", "result": "pass" if not all_schema_errors else "fail", "message": "Claim and constraint registers passed JSON Schema validation before this lint run." if not all_schema_errors else "Claim or constraint register failed JSON Schema validation."},
        {"check_id": "AUTO-SEMANTIC-LINT", "result": auto_result, "message": "Markdown tables, lifecycle block, front matter/ledger and EV references."},
    ])
    batch["result"] = "blocked" if not all_errors else "red"
    batch["warnings"] = ["Manual checks are not validator passes; DG0-DG2 remain blocked."]
    batch_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run = {
        "schema_version": "sg-eval-semantic-lint-run-0.1",
        "trial_batch_id": manifest["trial_batch_id"],
        "result": "passed" if not all_errors else "failed",
        "reports": [{"deliverable_id": did, "path": display(trial / "semantic_lint" / f"{did}.json"), "sha256": sha256_file(trial / "semantic_lint" / f"{did}.json"), "errors": errors} for did, _, errors in reports],
        "errors": all_errors,
        "schema_errors": all_schema_errors,
        "created_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
    }
    run_path = trial / "semantic_lint_run.json"
    run_path.write_text(json.dumps(run, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(run, ensure_ascii=False, indent=2))
    return 0 if not all_errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
