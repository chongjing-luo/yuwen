# `SG-EVAL` 试运行批次计划

- 试运行批次：`TRIAL-SG-EVAL-20260809-01`
- 状态：`snapshot_created_dg0_blocked`
- 机器计划：`work/knowledge/_meta/sg_eval_trial_batch_plan_20260809.json`
- 执行回执：`work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01/snapshot_receipt.json`

## 选择的三个代表件

1. `CARD-X1-U01-02`：双文本卡（《长征胜利万岁》《大战中的插曲》）。
2. `CARD-B1-U05-01`：特殊内容卡（整本书阅读《乡土中国》）。
3. `UNIT-X1-U01`：单元图谱，用于验证卡—KP—任务回链和关系无边替代观察项。

## 执行边界

- 这三件当前都是历史 `accepted` 产物，不能直接用新候选规则覆盖其正文或写回历史 SHA。
- 试运行必须先做只读 snapshot，再在 snapshot 工作区补齐 Claim、Constraint、Observation、两份独立 Review Binding 和 DG4 receipt。
- 没有协调者批准、两审封存和 DG4 receipt 前，批次不计为 green，也不产生 `cutover_batch_id`。
- 任何 M0、N/A 或教师用书 `edition_match=unknown` 均按候选规则保留结构化边界，不得用试运行填补证据缺口。

## 当前执行结果

- snapshot integrity：`pass`；canonical 三件文件 SHA 未变化。
- `DG0`：`blocked_coordinator_or_roles`；协调者、生产者、主审和二审尚未登记。
- `DG1`：`blocked`；人工 semantic lint 和 Claim 封存未完成。
- `DG2`：`blocked`；当前 Claim 文件只是 `formal=false` 机器盘点，不能作为正式分母。

## 试运行完成定义

- DG0—DG4 每件均有可核验 receipt；自动 errors=0，人工必检全部有结果。
- 主审和二审绑定相同 content/claim/rubric/observation/upstream SHA，角色、文件和评审者独立。
- 两审各自达到试运行门槛（≥92 且全部单项达标），R01—R10、P0/P1/P2 清零。
- 第三人仅凭 review package 复算 Claim 分母、七维分数、双审结论和 DG4 白名单。
