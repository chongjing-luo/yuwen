# `TRIAL-SG-EVAL-20260809-01` 只读试运行包

- 输入计划：`work/knowledge/_meta/sg_eval_trial_batch_plan_20260809.json`
- DG0 manifest：`work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01/dg0_snapshot_manifest.json`
- snapshot 回执：`work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01/snapshot_receipt.json`
- batch report：`work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01/batch_report.json`（自动检查与人工检查分栏）
- 当前判定：`snapshot_integrity=pass`；`DG0=blocked_coordinator_or_roles`；`DG1=blocked`；`DG2=blocked`。

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
python scripts/content_sha256.py work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01/snapshots/CARD-X1-U01-02.md
python scripts/validate_claim_constraint_registers.py claim work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01/claim_registers/CARD-X1-U01-02.json
python scripts/validate_claim_constraint_registers.py constraint work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01/constraint_registers/CARD-X1-U01-02.json
python scripts/run_sg_eval_semantic_lint.py --trial-dir work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01
pytest -q tests/test_evaluation_controls.py
```
