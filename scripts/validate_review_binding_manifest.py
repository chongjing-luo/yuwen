#!/usr/bin/env python3
"""Validate the companion review-binding manifest and independence guards."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "dev/knowledge-extraction-foundation/04_execution/review_binding_manifest_schema_candidate_20260808_014300.json"


def validate(manifest: dict, schema: dict | None = None) -> list[str]:
    schema = schema or json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(manifest)]
    primary = manifest.get("primary_review", {})
    secondary = manifest.get("secondary_review", {})
    if primary.get("reviewer") == secondary.get("reviewer"):
        errors.append("primary and secondary reviewers must be distinct")
    if primary.get("path") == secondary.get("path"):
        errors.append("primary and secondary review paths must be distinct")
    if primary.get("sha256") == secondary.get("sha256"):
        errors.append("primary and secondary review files must have distinct SHA values")
    if manifest.get("dg3_decision") == "pass":
        for role, review in (("primary", primary), ("secondary", secondary)):
            if review.get("decision") != "pass":
                errors.append(f"DG3 pass requires {role} decision=pass")
            if review.get("hard_rejections"):
                errors.append(f"DG3 pass requires {role} hard_rejections=[]")
            if any(review.get(code, 0) for code in ("p0", "p1", "p2")):
                errors.append(f"DG3 pass requires {role} P0/P1/P2=0")
    if manifest.get("primary_review", {}).get("role") != "primary":
        errors.append("primary_review.role must be primary")
    if manifest.get("secondary_review", {}).get("role") != "secondary":
        errors.append("secondary_review.role must be secondary")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--schema", type=Path, default=SCHEMA)
    args = parser.parse_args()
    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
        errors = validate(manifest, schema)
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    result = {"schema_version": "review-binding-validator-0.1", "result": "passed" if not errors else "failed", "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

