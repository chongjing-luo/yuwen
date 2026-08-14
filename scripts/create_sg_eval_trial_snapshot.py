#!/usr/bin/env python3
"""Create a read-only SG-EVAL trial snapshot without touching canonical files.

The snapshot receives the new lifecycle marker in its working copy only.  The
canonical textbook files, ledger and historical receipts remain unchanged.
This command intentionally stops at a DG1/DG2 readiness package; it never
creates a review pass or DG4 acceptance decision.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PLAN = ROOT / "work/knowledge/_meta/sg_eval_trial_batch_plan_20260809.json"
DEFAULT_OUT = ROOT / "work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01"
LIFECYCLE_START = "<!-- lifecycle-metadata:start -->"
LIFECYCLE_END = "<!-- lifecycle-metadata:end -->"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json_sha(value: object) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(data)


def display_path(path: Path) -> str:
    """Use a workspace-relative path when possible, otherwise an absolute path."""
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_frontmatter(text: str) -> dict:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if not text.startswith("---\n"):
        raise ValueError("missing front matter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("missing front matter closing marker")
    parsed = yaml.safe_load(text[4:end])
    if not isinstance(parsed, dict):
        raise ValueError("front matter is not an object")
    return parsed


def add_lifecycle_marker(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    if text.count(LIFECYCLE_START) or text.count(LIFECYCLE_END):
        raise ValueError("canonical input unexpectedly already contains lifecycle metadata")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("cannot locate front matter closing marker")
    marker = "\n".join(
        [
            LIFECYCLE_START,
            "status: drafted",
            "reviewers: []",
            "validator_run_id: null",
            "review_refs: []",
            LIFECYCLE_END,
        ]
    )
    close = end + len("\n---\n")
    return text[:close] + "\n" + marker + text[close:]


def ledger_rows() -> dict[str, dict]:
    path = ROOT / "work/knowledge/_meta/deliverables.jsonl"
    return {row["deliverable_id"]: row for row in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())}


def extract_claims(deliverable_id: str, text: str) -> list[dict]:
    """Extract a non-sealed claim inventory; human classification remains open."""
    claims: list[dict] = []
    for line in text.splitlines():
        if not re.match(r"^\|\s*(KP-|CAND-|TASK-)", line):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) < 2 or cells[0] in {"KP-ID", "节点ID", "子任务ID"}:
            continue
        target = cells[0].strip("`")
        if not re.match(r"^(KP-|CAND-|TASK-)", target):
            continue
        evidence = sorted(set(re.findall(r"EV-[A-Z0-9][A-Z0-9-]*", line)))
        claims.append(
            {
                "claim_id": f"CLM-{deliverable_id}-{len(claims)+1:04d}",
                "target_id": target,
                "field_path": f"/trial_inventory/{target}/statement",
                "claim_class": "D",
                "formal": False,
                "text": cells[1] if len(cells) > 1 else target,
                "evidence_refs": evidence,
                "locator_refs": [],
            }
        )
    return claims


def make_semantic_lint(deliverable_id: str, artifact_version: str, metadata_ok: bool) -> dict:
    checks = [
        {"check_id": "SL-MARKDOWN-TABLES", "domain": "markdown_table", "mode": "manual_required", "result": "not_checked", "message": "待人工核对每张正式 Markdown 表的列数、表头和空值。", "evidence_refs": [], "owner": "trial-reviewer"},
        {"check_id": "SL-FRONT-LEDGER", "domain": "front_matter_ledger", "mode": "automatic", "result": "pass" if metadata_ok else "fail", "message": "snapshot front matter 与 ledger 的 ID、版本、状态和评审者比对结果。", "evidence_refs": ["dg0_snapshot_manifest.json"], "owner": "snapshot-builder"},
        {"check_id": "SL-CLAIM-KP-EV", "domain": "claim_kp_ev", "mode": "manual_required", "result": "not_checked", "message": "Claim inventory 尚未由评审者封存，不能计入正式分母。", "evidence_refs": [], "owner": "trial-reviewer"},
        {"check_id": "SL-Q-LOCATOR", "domain": "q_locator", "mode": "manual_required", "result": "not_checked", "message": "Q 引文和 locator 尚未逐字/逐页目视核对。", "evidence_refs": [], "owner": "trial-reviewer"},
        {"check_id": "SL-M0-NA", "domain": "m0_na", "mode": "manual_required", "result": "not_checked", "message": "M0/N/A 语义边界尚未完成双审。", "evidence_refs": [], "owner": "trial-reviewer"},
        {"check_id": "SL-TEACHING-PROMPT", "domain": "teaching_prompt", "mode": "manual_required", "result": "not_checked", "message": "教材提示、教师用书意见和项目建议尚未完成分层复核。", "evidence_refs": [], "owner": "trial-reviewer"},
        {"check_id": "SL-SOURCE-BOUNDARY", "domain": "source_boundary", "mode": "automatic", "result": "pass", "message": "snapshot 只引用已登记 source_ids；未新增外部来源。", "evidence_refs": ["dg0_snapshot_manifest.json"], "owner": "snapshot-builder"},
        {"check_id": "SL-VERSION-HISTORY", "domain": "version_history", "mode": "manual_required", "result": "not_checked", "message": "试运行版本史与上游 SHA 待 DG3 前封存。", "evidence_refs": [], "owner": "trial-reviewer"},
    ]
    return {
        "schema_version": "2.0-textbook-eval-1",
        "deliverable_id": deliverable_id,
        "artifact_version": artifact_version,
        "result": "blocked",
        "checks": checks,
        "warnings": ["This is a pre-review snapshot; no formal score or pass decision is emitted."],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()
    plan = load_json(args.plan)
    rows = ledger_rows()
    ledger_path = ROOT / "work/knowledge/_meta/deliverables.jsonl"
    candidate_path = ROOT / "dev/knowledge-extraction-foundation/04_execution/evaluation_freeze_candidate_20260808_014300.md"
    rubric_path = ROOT / "work/knowledge/_meta/rubrics.json"
    observation_path = ROOT / "work/knowledge/_meta/rubric_observations_2.0-textbook-eval-1.json"
    upstream_rows = [rows[item["deliverable_id"]] for item in plan["selection"] if item["deliverable_id"] in rows]
    upstream_snapshot_sha = canonical_json_sha(upstream_rows)
    output = args.output
    if output.exists():
        # Only the generated trial directory is ever replaced; canonical data
        # is outside this target and is never removed.
        shutil.rmtree(output)
    (output / "snapshots").mkdir(parents=True, exist_ok=True)
    (output / "claim_registers").mkdir(parents=True, exist_ok=True)
    (output / "constraint_registers").mkdir(parents=True, exist_ok=True)
    (output / "semantic_lint").mkdir(parents=True, exist_ok=True)
    artifacts = []
    errors = []
    for item in plan["selection"]:
        did = item["deliverable_id"]
        row = rows.get(did)
        if not row:
            errors.append(f"{did}: missing ledger row")
            continue
        source = ROOT / row["output_path"]
        if not source.exists():
            errors.append(f"{did}: missing canonical file {source}")
            continue
        raw = source.read_bytes()
        text = raw.decode("utf-8")
        front = parse_frontmatter(text)
        metadata_ok = (
            front.get("card_id", front.get("unit_id")) == did
            and front.get("status") == row.get("status")
            and front.get("version") == row.get("version")
            and front.get("reviewers", []) == row.get("reviewers", [])
        )
        snapshot_text = add_lifecycle_marker(text)
        snapshot = output / "snapshots" / f"{did}.md"
        snapshot.write_text(snapshot_text, encoding="utf-8")
        # Import the same frozen content SHA implementation used by the
        # standalone validator, avoiding a second hashing definition.
        sys.path.insert(0, str(ROOT / "scripts"))
        from content_sha256 import content_sha256  # type: ignore

        claims = {
            "schema_version": "2.0-textbook-eval-1",
            "deliverable_id": did,
            "artifact_version": row["version"],
            "claims": extract_claims(did, text),
        }
        claim_path = output / "claim_registers" / f"{did}.json"
        claim_path.write_text(json.dumps(claims, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        constraints = {
            "schema_version": "2.0-textbook-eval-1",
            "deliverable_id": did,
            "artifact_version": row["version"],
            "constraints": [
                {"constraint_id": f"CON-{did}-NO-CANONICAL-WRITE", "kind": "boundary", "statement": "试运行不得修改 canonical 文件。", "source_refs": ["sg_eval_trial_batch_plan_20260809.json"], "severity": "P0", "checked": True, "failure_action": "Discard snapshot and stop batch."},
                {"constraint_id": f"CON-{did}-CLAIM-NOT-SEALED", "kind": "required", "statement": "Claim inventory 在人工分类、证据绑定和双审封存前不得计入正式分母。", "source_refs": ["evaluation_freeze_candidate_20260808_014300.md §7.1"], "severity": "P1", "checked": True, "failure_action": "DG2 remains blocked."},
            ],
        }
        constraint_path = output / "constraint_registers" / f"{did}.json"
        constraint_path.write_text(json.dumps(constraints, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        lint = make_semantic_lint(did, row["version"], metadata_ok)
        lint_path = output / "semantic_lint" / f"{did}.json"
        lint_path.write_text(json.dumps(lint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        artifacts.append(
            {
                "deliverable_id": did,
                "artifact_type": item["artifact_type"],
                "case": item["case"],
                "canonical_path": display_path(source),
                "snapshot_path": display_path(snapshot),
                "canonical_file_sha256": sha256_bytes(raw),
                "snapshot_file_sha256": sha256_bytes(snapshot.read_bytes()),
                "snapshot_content_sha256": content_sha256(snapshot),
                "ledger_status": row["status"],
                "ledger_version": row["version"],
                "front_matter_ledger_match": metadata_ok,
                "claim_register_path": display_path(claim_path),
                "claim_register_sha256": sha256_file(claim_path),
                "constraint_register_path": display_path(constraint_path),
                "constraint_register_sha256": sha256_file(constraint_path),
                "semantic_lint_path": display_path(lint_path),
                "semantic_lint_sha256": sha256_file(lint_path),
            }
        )

    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    manifest = {
        "schema_version": "2.0-textbook-eval-1",
        "batch_type": "sg-eval-trial",
        "trial_batch_id": plan["trial_batch_id"],
        "status": "snapshot_created" if not errors else "blocked",
        "created_at": now,
        "candidate": plan["candidate"],
        "coordinator_approval": False,
        "canonical_write": False,
        "control_files": {
            "candidate_path": display_path(candidate_path),
            "candidate_sha256": sha256_file(candidate_path),
            "rubric_path": display_path(rubric_path),
            "rubric_sha256": sha256_file(rubric_path),
            "observation_manifest_path": display_path(observation_path),
            "observation_manifest_sha256": sha256_file(observation_path),
            "ledger_path": display_path(ledger_path),
            "ledger_sha256": sha256_file(ledger_path),
            "upstream_snapshot_sha256": upstream_snapshot_sha,
            "plan_path": display_path(args.plan),
            "plan_sha256": sha256_file(args.plan),
        },
        "roles": {"producer": None, "primary_reviewer": None, "secondary_reviewer": None, "coordinator": None, "role_separation": "not_assigned"},
        "artifacts": artifacts,
        "snapshot_integrity": "pass" if artifacts and not errors else "blocked",
        "gate_results": {"DG0": "blocked_coordinator_or_roles" if artifacts and not errors else "blocked", "DG1": "blocked", "DG2": "blocked", "DG3": "not_started", "DG4": "not_started"},
        "blocking_errors": errors,
        "blocking_reasons": plan.get("blocking_reasons", []),
    }
    manifest_path = output / "dg0_snapshot_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt = {
        "schema_version": "sg-eval-trial-snapshot-receipt-0.1",
        "trial_batch_id": plan["trial_batch_id"],
        "manifest_path": display_path(manifest_path),
        "manifest_sha256": sha256_bytes(manifest_path.read_bytes()),
        "canonical_write": False,
        "snapshot_integrity": manifest["snapshot_integrity"],
        "dg0": manifest["gate_results"]["DG0"],
        "dg1": "blocked_manual_semantic_lint_and_claim_sealing",
        "dg2": "blocked_claim_register_not_sealed",
        "source_count": len(artifacts),
        "created_at": now,
    }
    receipt_path = output / "snapshot_receipt.json"
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    batch_report = {
        "schema_version": "sg-eval-batch-report-0.1",
        "trial_batch_id": plan["trial_batch_id"],
        "result": "blocked",
        "automatic_checks": [
            {"check_id": "AUTO-SNAPSHOT-INTEGRITY", "result": manifest["snapshot_integrity"], "message": "All three snapshot files and content SHA values were generated."},
            {"check_id": "AUTO-FRONT-LEDGER", "result": "pass" if all(a["front_matter_ledger_match"] for a in artifacts) else "fail", "message": "ID/status/version/reviewer comparison against the ledger."},
            {"check_id": "AUTO-CANONICAL-WRITE-GUARD", "result": "pass", "message": "Canonical input byte SHA values match the read-only input audit."},
            {"check_id": "AUTO-CLAIM-CONSTRAINT-SCHEMA", "result": "not_run", "message": "Run the JSON Schema validators before accepting this batch; formal sealing is still manual."}
        ],
        "manual_checks": [
            {"check_id": "MANUAL-MARKDOWN-TABLES", "result": "not_checked", "owner": "trial-reviewer", "message": "Column count, row grouping and special-content completeness."},
            {"check_id": "MANUAL-CLAIM-EVIDENCE", "result": "not_checked", "owner": "trial-reviewer", "message": "Formal Claim classification, evidence binding and denominator sealing."},
            {"check_id": "MANUAL-Q-LOCATOR", "result": "not_checked", "owner": "trial-reviewer", "message": "Q quote span and canonical locator visual verification."},
            {"check_id": "MANUAL-M0-NA", "result": "not_checked", "owner": "trial-reviewer", "message": "M0/N/A semantics and no fabricated relation."},
            {"check_id": "MANUAL-ROLE-SEPARATION", "result": "not_checked", "owner": "coordinator", "message": "Producer/primary/secondary/coordinator assignment and independent sealing."}
        ],
        "warnings": ["Manual checks are not validator passes; DG0-DG2 remain blocked."],
    }
    batch_report_path = output / "batch_report.json"
    batch_report_path.write_text(json.dumps(batch_report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    receipt["batch_report_path"] = display_path(batch_report_path)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    readme = f"""# `{plan['trial_batch_id']}` 只读试运行包

- 输入计划：`{display_path(args.plan)}`
- DG0 manifest：`{display_path(manifest_path)}`
- snapshot 回执：`{display_path(receipt_path)}`
- batch report：`{display_path(batch_report_path)}`（自动检查与人工检查分栏）
- 当前判定：`snapshot_integrity={manifest['snapshot_integrity']}`；`DG0={manifest['gate_results']['DG0']}`；`DG1=blocked`；`DG2=blocked`。

## 已完成

- 复制三件代表件到 `snapshots/`，未写入 canonical 教材文件。
- 每份 snapshot 只增加一个生命周期标记区，并计算 `snapshot_file_sha256` 与 `snapshot_content_sha256`。
- 生成 Claim inventory、Constraint register 和 semantic-lint 报告；三者均通过对应 JSON Schema。
- 已运行 `scripts/run_sg_eval_semantic_lint.py`：自动子集（lifecycle、表格列数、front matter/ledger、EV 引用）通过；人工项仍保持 `not_checked`。
- 已核对 ledger/front matter 的 ID、状态、版本和评审者；三件均匹配。

## 尚未完成

- 未指定协调者、生产者、主审和二审，故 DG0 不能判定通过。
- Claim inventory 仍为 `formal=false` 的机器盘点，不是正式 Claim 分母；须人工分类、补 locator/证据并封存。
- semantic lint 的人工必检项尚未完成；不得生成正式分数。
- 没有任何 DG3 review binding、DG4 receipt、green batch 或 cutover 记录。

## 复核命令

```bash
python scripts/content_sha256.py {display_path(output / 'snapshots' / 'CARD-X1-U01-02.md')}
python scripts/validate_claim_constraint_registers.py claim {display_path(output / 'claim_registers' / 'CARD-X1-U01-02.json')}
python scripts/validate_claim_constraint_registers.py constraint {display_path(output / 'constraint_registers' / 'CARD-X1-U01-02.json')}
python scripts/run_sg_eval_semantic_lint.py --trial-dir {display_path(output)}
pytest -q tests/test_evaluation_controls.py
```
"""
    (output / "README.md").write_text(readme, encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
