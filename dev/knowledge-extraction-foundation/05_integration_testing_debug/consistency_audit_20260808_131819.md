# Consistency Audit — knowledge-extraction-foundation

- Date: 2026-08-08 13:18 +0800
- Triggered by: 用户要求“再次制定更好的方案，确定评估标准”
- Audit scope: V2.4 主计划、冻结教材契约、评价解释层、动态账本、旧执行文档、validator 能力与 `SG-EVAL` 切换条件
- Plan SHA-256 after audit amendment: `ebed21847466c0204e2f970defd01c9ed09cd00cc61509d645eec69f2aa7d5e6`
- Evaluation candidate SHA-256: `73b2bb5da0723c62e1072939f41a37d8b1719cf1a96c09770e6182cb0b209a6f`
- Cutover checklist SHA-256: `18cedcbbe2124ac9a4c913a1926e723b967c04ee3c28412f60e13862e7dc51ae`
- Dynamic snapshot: `VAL-20260808-132004+0800`, passed, 0 errors, 3 acknowledged warnings; 68/114 textbook deliverables accepted (`48/81` cards, `18/28` graphs, `2/5` book summaries). This snapshot is evidence only, not part of the fixed plan.

## Documents read

- `work/语文备课系统_知识点提取研究计划.md`
- `dev/knowledge-extraction-foundation/PROJECT_INDEX.md`
- `docs/superpowers/specs/2026-08-05-curriculum-mineru-work-integration-design.md`
- `dev/knowledge-extraction-foundation/04_execution/implementation_spec_20260806_010616.md`
- `dev/knowledge-extraction-foundation/04_execution/first_throughput_evidence_20260806_013226.md`
- `dev/knowledge-extraction-foundation/04_execution/calibration_throughput_20260806_061159.md`
- `dev/knowledge-extraction-foundation/04_execution/contract_freeze_20260807.md`
- `dev/knowledge-extraction-foundation/04_execution/action_plan_20260807_130647.md`
- `dev/knowledge-extraction-foundation/04_execution/task_checklist_20260807_130647.md`
- `dev/knowledge-extraction-foundation/04_execution/implementation_log_20260807_130647.md`
- `dev/knowledge-extraction-foundation/04_execution/evaluation_freeze_candidate_20260808_014300.md`
- `dev/knowledge-extraction-foundation/04_execution/evaluation_cutover_checklist_20260808_014300.md`
- `dev/knowledge-extraction-foundation/04_execution/review_binding_manifest_schema_candidate_20260808_014300.json`
- `dev/knowledge-extraction-foundation/05_task_packets/V24_EXECUTION_AND_EVALUATION_PROPOSAL_20260807.md`
- `dev/knowledge-extraction-foundation/05_task_packets/V24_EVIDENCE_ACCEPTANCE_ADDENDUM_20260807.md`
- `dev/knowledge-extraction-foundation/05_task_packets/V24_RUBRIC_OBSERVATION_ADDENDUM_20260807.md`
- `dev/knowledge-extraction-foundation/05_integration_testing_debug/consistency_audit_20260807_193400.md`
- `work/knowledge/_meta/rubrics.json`
- `work/knowledge/_meta/taxonomy.yaml`
- `work/knowledge/_meta/schemas/review.schema.json`
- `work/knowledge/_meta/deliverables.jsonl`
- `work/knowledge/_meta/validation_reports/latest.json`
- `work/knowledge/_reviews/scores/g2_review_summary_20260807.md`

## Automated checks

| Check | Result |
|---|---|
| Indexed artifact existence | Canonical files exist; the invalid compound G2 pointer was corrected during this audit. |
| Dev admission | pass: 1/1 task workspace has `PROJECT_INDEX.md`. |
| Archive reverse import | pass: no active `scripts/` or `tests/` Python import from `_archive`. |
| Required acceptance sections | pass: V2.4 contains DoD, A/B/C evaluation, six product rubrics, DG/SG gates, rework and cutover rules. |
| Architecture diagrams | overall dependency flow exists; the other five diagram classes are neither supplied nor individually marked N/A. Non-blocking for current Markdown production, but still a documentation contradiction. |
| Validator snapshot | `VAL-20260808-132004+0800`, result `passed`, 0 errors, 3 warnings. The warnings concern deferred external/exam sources, unknown TB2 edition match and the still-unfrozen exam contract. |
| Cutover readiness | 11/35 checklist items complete; 24/35 pending. Result: `not ready to cut over`. |
| Health dashboard | exit 0: 21/21 tests, 0 dangling references, 1/1 dev compliance, no blocking gates; M6 invariant fork skipped because no canonical invariant-family declaration exists. |

Exact health command:

```text
python /home/ubuntu/.agents/skills/agentic-project-scaffold/scripts/health_dashboard.py --src-dir . --source-glob 'scripts/*.py' --source-glob 'tests/*.py' --tests-cmd 'python -m unittest discover -s tests -v' --dev-dir dev
```

## Contradictions

| # | Class | Documents / lines | Mismatch | Proposed resolution | Status |
|---:|---|---|---|---|---|
| 1 | stale approval | `PROJECT_INDEX.md` L36–42 vs V2.4 header and §6.18 | Index still called the 2026-08-06 requirements/architecture baseline approved and the old action plan active, while V2.4 explicitly remains candidate until user approval and `SG-EVAL`. | Reset V2.4 requirements/architecture approval to pending; index the evaluation candidate and cutover checklist; retain old plan only as pre-cutover legacy control. | resolved in `PROJECT_INDEX.md` |
| 2 | terminology / execution mode | old action plan §3–5 and checklist vs V2.4 §6.14–§7.6 | Lower historical documents use `G2/G3/G3R/G-TB` and `serial_single_agent`; V2.4 uses `DG0–DG4`, `SG-*` and hybrid WIP=2. | Do not rewrite historical logs; mark the old action plan/checklist `legacy-active/pre-cutover`, then create a new cutover batch manifest using only DG/SG names. | resolved at authority/index layer; manifest remains item 6 |
| 3 | stale dynamic state | checklist L14–21, implementation log vs ledger snapshot | Legacy checklist stores `20/81`, `8/28`, old owners and an obsolete next queue; ledger now reports `48/81`, `18/28`, `2/5`. V2.4 forbids dynamic progress in fixed norms. | Treat old counts as timestamped history; all new target assignment must derive from ledger SHA + validator run + batch manifest. | resolved at authority/index layer |
| 4 | missing cutover control package | cutover checklist B–F | Claim/constraint Schema, observation manifest, deterministic scorer, content-SHA tool, semantic-lint contract, DG4 receipt, capability matrix and most negative fixtures do not yet exist. | Implement the 24 pending checklist items, then run three representative DG0–DG4 pilots and two consecutive green batches. | flagged — blocks `SG-EVAL` |
| 5 | review binding gap | `review.schema.json`; binding candidate; V2.4 §6.3/§6.18 | Frozen review Schema cannot record content/claim/rubric/upstream/batch SHA; the companion binding Schema exists but has no validated positive/negative packages. | Keep the frozen review Schema unchanged; validate and activate the companion manifest only through the all-at-once cutover. | flagged — blocks reproducible DG3/DG4 |
| 6 | missing batch boundary | V2.4 §6.16/§6.18; filesystem scan | No active batch manifest or `cutover_batch_id` was found, so current in-flight scope and old/new rule boundary are not machine-provable. | Before new intake, freeze a legacy in-flight manifest; after pilots, register one unique cutover batch. | flagged — blocks WIP expansion |
| 7 | denominator terminology | implementation spec / project index vs V2.4 §2.1 | Older docs called all 120 ledger rows “core deliverables”; V2.4 correctly defines 114 textbook core items plus 6 post-textbook provisional rows. | Canonical wording: ledger=120; textbook `SG-TB` denominator=114; post-`SG-TB` provisional rows=6. | resolved in `PROJECT_INDEX.md`; old implementation evidence remains historical |
| 8 | broken pointer | `PROJECT_INDEX.md` G2 row | `_reviews/scores/g2_review_summary_20260807.md` did not resolve relative to the index directory; actual file is under `../../work/knowledge/...`. | Replace with the real task-root-relative path. | resolved in `PROJECT_INDEX.md` |
| 9 | method-measurement reproducibility | V2.4 former §6.17 and evaluation candidate former §13 | KP semantic matching, bootstrap resampling unit, Gold agreement and query timing were underspecified; two teachers were too few for final usability closure. | Added blind dual Gold + adjudication preconditions, alpha/F1 agreement thresholds, one-to-one KP matching, deliverable-cluster bootstrap, an explicit 11/12 query timer and a minimum of 3 independent teachers. | resolved in plan/candidate |
| 10 | evaluation contamination | V2.4 §6.17; evaluation candidate §13 | All 81 card files already exist, so the current sealed set is not a truly prospective blind holdout. | Keep the current label “sealed evaluation set”, publish the contamination boundary, and reserve external-generalization claims for a future unseen source or contract. | flagged — accepted scope limit; blocks generalization claim only |
| 11 | architecture completeness | architecture reference and V2.4 dependency diagram | Only the overall flow/dependency diagram is present; data flow, sequence, state, deployment and user-flow classes are not individually present or marked N/A. | Before closure, add the useful state/data-flow diagrams and explicitly mark genuinely irrelevant classes N/A with reasons. | flagged — non-blocking for `SG-EVAL`, blocking final scaffold closure |

## Quality decision

The V2.4 design is materially better than the old execution plan and is suitable as the candidate baseline. Its evaluation standard is now conceptually determinate:

1. A layer: any structural/evidence/SHA/source/R/P failure means no formal score and immediate rework.
2. B layer: frozen product weights and thresholds, computed from pre-registered observations rather than reviewer impression.
3. C layer: method validity measured on a sealed set with explicit Gold, matching, resampling, query timing and teacher-usability rules.

It is **not yet operationally frozen**. The correct disposition is:

```text
V2.4 plan quality: candidate-approved-for-user-review
2.0-textbook-eval-1 runtime state: not-active
new-rule WIP expansion: blocked
pre-cutover in-flight closure under 2.0-textbook: allowed
exam work: blocked_by_textbook
```

## Recommended resolution order

1. User/coordinator approves the V2.4 direction, forward-only cutover and full dual-review cost.
2. Freeze the exact legacy in-flight scope and stop new intake; `PROJECT_INDEX` authority/status cleanup is already complete.
3. Implement Claim/constraint, observation, scorer, semantic lint, content SHA, review binding and DG4 receipt with positive/negative fixtures.
4. Run one dual-text card, one special-content card and one unit graph through DG0–DG4; have a third party reproduce the result from the package alone.
5. Require two consecutive green pilot batches; record the unique `cutover_batch_id`; then activate `2.0-textbook-eval-1`.
6. Continue textbook vertical slices under the active rule; close `SG-METHOD`, then `SG-TB`; only then create and calibrate the 17-year exam contract.

## Summary

- Contradictions: 11
- Resolved in this audit: 6
- Flagged: 5
- Blocking current old-rule in-flight review: no
- Blocking V2.4 activation / WIP expansion: yes
- Blocking exam work: yes, independently enforced by `SG-TB`
