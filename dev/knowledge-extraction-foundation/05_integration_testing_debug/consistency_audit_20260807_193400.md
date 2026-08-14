# Consistency Audit — knowledge-extraction-foundation

- Date: 2026-08-07 19:34 +0800
- Triggered by: 用户要求重新制定更好的方案并冻结后续评估标准
- Audit scope: 教材阶段执行基线、冻结契约、当前账本、评审协议及 G-TB 后真题边界
- Current machine baseline: `VAL-20260807-192837+0800`，`passed`，0 errors，3 warnings；账本为 31/81 卡、13/28 图、0/5 册表 `accepted`

## Documents read

- `work/语文备课系统_知识点提取研究计划.md`（V2.3）
- `dev/knowledge-extraction-foundation/PROJECT_INDEX.md`
- `docs/superpowers/specs/2026-08-05-curriculum-mineru-work-integration-design.md`
- `dev/knowledge-extraction-foundation/04_execution/implementation_spec_20260806_010616.md`
- `dev/knowledge-extraction-foundation/04_execution/first_throughput_evidence_20260806_013226.md`
- `dev/knowledge-extraction-foundation/04_execution/calibration_throughput_20260806_061159.md`
- `dev/knowledge-extraction-foundation/04_execution/contract_freeze_20260807.md`
- `dev/knowledge-extraction-foundation/04_execution/action_plan_20260807_130647.md`
- `dev/knowledge-extraction-foundation/04_execution/task_checklist_20260807_130647.md`
- `dev/knowledge-extraction-foundation/04_execution/implementation_log_20260807_130647.md`
- `work/knowledge/_reviews/scores/g2_review_summary_20260807.md`
- `work/knowledge/_reviews/issues/validator_gap_followups_20260807.md`
- `work/knowledge/_meta/rubrics.json`
- `work/knowledge/_meta/schemas/review.schema.json`
- `work/knowledge/_meta/schemas/deliverable.schema.json`
- `work/knowledge/_meta/deliverables.jsonl`
- `work/knowledge/_meta/validation_reports/latest.json`

## Automated checks

| Check | Result |
|---|---|
| Broken pointers | 1 failure：`PROJECT_INDEX.md` 第41行的 `_reviews/scores/g2_review_summary_20260807.md` 按索引目录解析不存在；真实文件在 `../../work/knowledge/_reviews/scores/` |
| Active artifact existence | 其余索引中的 active artifact 均存在 |
| Dev admission | pass：1/1 task workspace 有 `PROJECT_INDEX.md` |
| Archive reverse import | pass：`scripts/`、`tests/` 无 `_archive` 引用 |
| Required acceptance sections | pass：V2.3 有 DoD、产物量表、门禁和返工规则 |
| Architecture diagram classes | overall flow 存在；其余五类未提供，也未逐类写明 N/A，记录为非教材生产阻断项 |
| Health dashboard | pass；精确命令：`python /home/ubuntu/.agents/skills/agentic-project-scaffold/scripts/health_dashboard.py --src-dir . --source-glob 'scripts/*.py' --source-glob 'tests/*.py' --tests-cmd 'python -m unittest discover -s tests -v' --dev-dir dev`；21/21 tests，0 dangling refs，exit 0 |
| Invariant fork | skipped：项目没有 `AGENTS.md` 中的 canonical invariant-family 声明 |

## Contradictions

| # | Class | Documents / lines | Mismatch | Proposed resolution | Status |
|---:|---|---|---|---|---|
| 1 | stale state / progress | V2.3 L26–38、L1036；`deliverables.jsonl`；latest validator | 同一主计划表格仍写 28/81、11/28，正文和页尾写 31/81、13/28；静态方案混入会持续过期的实时计数。 | 主计划只保留目标分母和“账本为唯一真相”；实时计数移到一个机器生成的 `current_snapshot`，每批只引用 `run_id + snapshot hash`。 | flagged—阻断 V2.4 批准 |
| 2 | stale lifecycle statement | V2.3 L134–138；账本当前记录 | B1 U01 三卡和图谱仍被称为 `draft_existing`，实际上已 `accepted`。 | 改为“历史试产件已返修并锁定”，历史问题移入实施日志，不能继续充当当前状态。 | flagged—本轮修正 |
| 3 | stale queue / stage docs | V2.3 L1029–1031；task checklist L16–24；implementation log 最后条目 | 主计划仍给出 U04→U05 队列，清单仍写 20/81、8/28 和 B2 U01–U03；当前已到 B2 U06–U08。 | 只在动态批次清单维护下一队列；追加当前 checkpoint，旧日志保持只读历史。 | flagged—本轮修正 |
| 4 | terminology / gate collision | V2.3 L657–667 与 L796–828、L861–908 | `G1/G2/G3` 同时表示“交付物结构/证据/双审门”和“项目基础/校准/单元门”，执行者无法唯一解释“通过 G2”。 | 两层门禁分命名空间：交付物生命周期用 `DG0–DG4`；项目阶段用 `SG-F/SG-CAL/SG-UNIT/SG-REC/SG-TB/SG-EXAM/SG-REL`。 | flagged—阻断 V2.4 批准 |
| 5 | dependency graph | V2.3 L703–724 对比 L9、L443、L894–922 | 图中校准冻结后教材与真题分叉并行，违反“教材全部锁定后才启动真题”的硬约束。 | 重画为：教材卡→单元图→诵读卡/册表→`SG-TB`→真题来源治理/解构→映射→全局图。 | flagged—阻断后续分派 |
| 6 | review coverage | V2.3 L19、L40、L664–667 对比 L614–621、L673 | 批次闭环和写回门要求同 SHA 双审，但卡片规则又只对必检集及 25% 抽样二审；未抽中卡无法闭合通用 G3/G4。当前执行事实上对新卡全量双审。 | 教材 81 卡统一为 100% 主审 + 100% 第二复审；删除教材阶段抽样分支。若以后恢复抽样，另定义“单审写回门”。 | flagged—阻断验收口径 |
| 7 | data contract / batch | V2.3 L617–620、L638–655、L661；`deliverable.schema.json` L6–21 | 抽样、重大缺陷率和 G0 都依赖 `batch_id`，但 deliverable schema/账本没有该字段，120 行当前均无 `batch_id`。 | 教材当前先使用独立 `batch_manifest`；V3 再把 `batch_id` 纳入 schema 并由 validator 强制。全量双审可移除当前抽样对 batch_id 的依赖。 | flagged—阻断可复现抽样 |
| 8 | review contract / hash | V2.3 L40、L653、L661–665；`review.schema.json` L6–20；gap follow-up | 方案要求目标 SHA、量表 SHA、batch、validator run 绑定；review schema 不含这些字段且 `additionalProperties=false`，基础 validator 也不校验评审失效。 | V3 review schema 强制 `artifact_sha256/rubric_sha256/batch_id/validation_run_id/checkpoint_results`；当前用完整 Markdown 前言和协调者人工 hash 锁定，明确是临时控制。 | flagged—高风险工具债 |
| 9 | scoring reproducibility | V2.3 L498–513、L599–610；`rubrics.json`；现有 0.5 分评审记录 | 计划声称检查点二元、等权复算；冻结 rubric 多为 5 分粗检查点，实际评审直接给 19.5、14.5 等半分，无法由二元检查点唯一复算。 | 不改权重/门槛的前提下，补一份评分解释协议：每个粗检查点拆为可观察子项并保存分子/分母；评分脚本复算。协议冻结前不得宣称分数完全可复现。 | flagged—阻断“确定评估标准” |
| 10 | validator claim vs capability | V2.3 L767–790 对比 L653 和 gap follow-up | F3 最低检查项声称能拦 Markdown 列数、页码越界、claim type、QD、review hash 等，但已知 gap 明确这些未被 validator 强制。 | 把 F3 分成“已自动化/人工必检/V3 待自动化”三栏；绿灯报告不得把人工项计为 validator 通过。 | flagged—阻断错误安全感 |
| 11 | exam scope / denominator | V2.3 L72、L90、L583、L912–920；`rubrics.json` exam mapping checkpoint；账本 | 目标已改为 17 年配对卷，但映射门槛仍写“四份已验收真题/四卷小问”，账本仍只有4个 `exam_analysis`。 | G-TB 前把高考量表标为 provisional；G-TB 后创建 17 年 deliverable manifest，重新校准真题 schema/rubric，再冻结 `exam-contract`。 | flagged—教材阶段可延后，SG-TB 后阻断 |
| 12 | pre/post-lock scope | V2.3 L729–740 对比 L896、L912–922 | 教材 Phase F1 的验收条件要求真题、答案、评分资料完整登记，但同文又禁止 G-TB 前进行这项来源治理。 | 拆为 `F-TB`（教材/课标/TB2）与 `F-EXAM`（原卷/答案/评分材料，SG-TB 后）；前者不得因后者未完成而失败。 | flagged—阻断阶段定义 |
| 13 | upstream semantics | V2.3 L445–454 对比 L610、L678、L942 | 全局图声明直接上游仅 5 册表+映射表，量表又要求 81 卡/28 图“上游”全部纳入，直接与传递血缘混用。 | 明确：直接上游=5 册表+映射；传递血缘=81 卡+28 图+真题；分别计算 direct dependency 与 transitive lineage。 | flagged—G阶段前修正 |
| 14 | status vocabulary | V2.3 L21、L651、L684；`deliverable.schema.json` L12 | 方案把 `blocked` 当批次/产物状态，但 deliverable 状态枚举没有 `blocked`。 | 明确 `blocked` 只属于 batch/gate，不写入 deliverable；产物使用 `drafted/review_required` 并附 blocker。若要入账本则升版 schema。 | flagged—本轮修正 |
| 15 | execution mode | action plan §3 对比 V2.3 L852–860、L954–980 | 行动计划写 `serial_single_agent`，主计划冻结后允许按独立单元并行且 WIP≤3。 | 改为 hybrid：共享注册表/同一文件串行单写；不同单元生产与独立评审可并行；协调者独占 G4 写回。 | flagged—本轮修正 |
| 16 | metric measurability | V2.3 L479–494、L638–649；当前 Markdown 产物 | “需证主张总数”“核心结论”“正式主张”等分母没有唯一机器口径，0/0 也未定义，100% 指标无法稳定复算。 | 冻结 claim inventory：Q/F/I/M/R/E/D 的每个正式目标各有 Claim-ID；覆盖率以 Claim-ID 去重计数；0/0 记 N/A 且不得用于绿灯替代必检项。 | flagged—阻断项目级 KPI |
| 17 | stale approval / broken index | `PROJECT_INDEX.md` L36–44；V2.3 L1–15；index L41 | requirements/architecture 仍沿用 2026-08-06 approval，但主计划已在 2026-08-07 升为 V2.3；G2 summary 路径也写错。 | V2.4 候选期间将对应 approval 置为 pending；修正 G2 summary 为 `../../work/knowledge/_reviews/scores/g2_review_summary_20260807.md`，用户确认后再批准。 | flagged—阻断基线宣布 approved |

## Recommended resolution order

1. **先修执行控制面：** #1、#3、#4、#5、#6、#12、#14、#15、#17。
2. **再冻结评估解释协议：** #7、#8、#9、#10、#16。权重与总分门槛可不变，但检查点必须能复算。
3. **教材继续生产：** 以当前 31/81 卡、13/28 图为快照，B2 U06→U07→U08；每个单元按卡全量双审→协调者 G4→图谱全量双审→协调者 G4。
4. **整册闭环：** B1 先补 `CARD-B1-REC-01` 后生成 `BOOK-B1`；B2 完成 U06–U08 和诵读卡后生成 `BOOK-B2`；选必三册按同一垂直切片推进。
5. **G-TB 后另冻真题契约：** 先解决 #11，再允许任何正式真题解构或映射。

## Summary

- Total contradictions: 17
- Resolved in this audit: 0（本技能只审计，不修改 owning-stage 文档）
- Flagged: 17
- Blocking V2.4 approval: yes
- Blocking current already领取的单卡证据整理: no；单卡仍可按冻结 `2.0-textbook` 和人工双审继续
- Blocking new batch扩容、抽样验收或高考启动: yes

