#!/usr/bin/env python3
"""Schema plus semantic validation for DG2 claim/constraint registers."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = {
    "claim": ROOT / "work/knowledge/_meta/schemas/claim_register.schema.json",
    "constraint": ROOT / "work/knowledge/_meta/schemas/constraint_register.schema.json",
}


def validate(payload: dict, kind: str, schema: dict | None = None) -> list[str]:
    if kind not in SCHEMAS:
        return [f"unknown register kind: {kind}"]
    schema = schema or json.loads(SCHEMAS[kind].read_text(encoding="utf-8"))
    errors = [error.message for error in Draft202012Validator(schema).iter_errors(payload)]
    if kind == "claim":
        seen = set()
        for claim in payload.get("claims", []):
            key = (claim.get("claim_id"), claim.get("target_id"), claim.get("field_path"))
            if key in seen:
                errors.append(f"duplicate formal claim key: {key}")
            seen.add(key)
            if claim.get("formal") and not claim.get("na") and not claim.get("evidence_refs"):
                errors.append(f"formal claim has empty denominator evidence_refs: {claim.get('claim_id')}")
            if claim.get("formal") and claim.get("claim_class") == "I" and len(claim.get("evidence_refs", [])) < 2:
                errors.append(f"I claim requires two evidence refs: {claim.get('claim_id')}")
            if claim.get("na") and claim.get("evidence_refs") and claim.get("na", {}).get("status") not in {
                "not_applicable", "permitted_unavailable", "future_locked", "no_reliable_relation"
            }:
                errors.append(f"invalid N/A status: {claim.get('claim_id')}")
    else:
        seen = set()
        for constraint in payload.get("constraints", []):
            cid = constraint.get("constraint_id")
            if cid in seen:
                errors.append(f"duplicate constraint_id: {cid}")
            seen.add(cid)
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("kind", choices=sorted(SCHEMAS))
    parser.add_argument("register", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.register.read_text(encoding="utf-8"))
        errors = validate(payload, args.kind)
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    result = {"schema_version": "claim-constraint-validator-0.1", "result": "passed" if not errors else "failed", "errors": errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())

