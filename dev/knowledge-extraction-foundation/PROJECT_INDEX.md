# Knowledge Extraction Foundation — Project Index

- Task slug: `knowledge-extraction-foundation`
- Objective: 先完成教材侧正式知识卡、单元图谱和册级总表的可审计生产与锁定，再解锁高考试卷处理。
- Canonical execution baseline: `../../work/语文备课系统_知识点提取研究计划.md`
- Architecture/design reference: `../../docs/superpowers/specs/2026-08-05-curriculum-mineru-work-integration-design.md`
- User approval recorded: 2026-08-07 已批准“先教材，再试卷”的阶段顺序与冻结教材契约；V2.4 评价解释层与前向 cutover 仍待用户/协调者批准。

## Current execution snapshot (2026-08-09)

- 教材门禁已通过：`TEXTBOOK-LOCK-2.0-textbook`，81 张卡、28 份图谱、5 份册表，`114/114 accepted`。
- 当前阶段已切换为 `SG-EXAM-CAL-2008-2024`，但仍为 `candidate_structural_freeze`；题文—答案/评分—教材 KP 三方证据闭合前全部保持 `M0 / kp_id=N/A`。
- 当前状态回执：`../../work/knowledge/高考分析/SG-EXAM-CAL-STATUS-20260809.md`；Luna 补充交接：`05_task_packets/LUNA_HANDOFF_ADDENDUM_20260809.md`。
- 答案/解析候选清洗派生层：`../../work/knowledge/高考分析/EXAM-ANSWER-CLEAN-CANDIDATES-20260809.md`；机器校验：`../../work/knowledge/_meta/answer_clean_candidate_validation_20260809.json`。
- 答案/解析清洗人工队列：`../../work/knowledge/高考分析/EXAM-ANSWER-CLEAN-REVIEW-QUEUE-20260809.md`。
- 显式缺失答案源复核队列：`../../work/knowledge/高考分析/EXAM-MISSING-SOURCE-REVIEW-QUEUE-20260809.md`；机器校验：`../../work/knowledge/_meta/missing_answer_source_queue_validation_20260809.json`。
- 清洗层回执：`../../work/knowledge/_reviews/receipts/exam_answer_clean_candidates_20260809.json`。
- 6 条旧 `drafted` ledger 项审计：`../../work/knowledge/_reviews/EXAM-LEGACY-DRAFT-AUDIT-20260809.md`；均保留为历史候选，不进入当前试卷分母或下游消费。
- `SG-EVAL` 机器控制件：`../../scripts/content_sha256.py`、`../../scripts/validate_review_binding_manifest.py`、`../../scripts/score_rubric_fixed.py`；观察量表、Claim/Constraint Schema、DG4 receipt、semantic lint、能力矩阵和 warning register 已登记在 `../../work/knowledge/_meta/`。
- `SG-EVAL` 机器控制回执（候选、未激活）：`../../work/knowledge/_meta/sg_eval_machine_controls_20260809.json`；记录文件 SHA 与 10 项聚焦回归测试通过结果；全量测试当前为 67 passed，但尚未生成 `cutover_batch_id`。
- `SG-EVAL` 代表件试运行计划：`../../work/knowledge/_reviews/SG-EVAL-TRIAL-PLAN-20260809.md`；选定双文本卡、特殊内容卡和单元图，但仍等待协调者批准与只读 snapshot。
- `SG-EVAL` 只读试运行包已生成：`../../work/knowledge/_reviews/trials/TRIAL-SG-EVAL-20260809-01/README.md`；snapshot integrity 通过，Claim/Constraint/semantic-lint Schema 通过，但 DG0 因协调者/角色未分配而阻断，DG1/DG2 未放行。
- `SG-METHOD` 协议已登记但未激活：`../../work/knowledge/_reviews/SG-METHOD-PROTOCOL-20260809.md`；配置为 `blocked/pending_new_source`，真实 Gold、观察和教师查询尚未运行。
- `SG-METHOD` Schema/模板：`../../work/knowledge/_meta/schemas/sg_method_*.schema.json`、`../../work/knowledge/_meta/sg_method_observation_template.json`、`../../work/knowledge/_meta/sg_method_gold_record_template.json`；计分器：`../../scripts/score_sg_method_metrics.py`。
- `SG-METHOD` 合成正/负夹具仅用于回归计分边界：`../../work/knowledge/_meta/validation_fixtures/sg_method_observation.*.json`；不得当作真实评估结果。
- `SG-METHOD` 机器控制回执：`../../work/knowledge/_meta/sg_method_machine_controls_20260809.json`；9 项聚焦回归测试通过，全量回归 69 passed，真实评估仍为 `not_run`。
- 最近一次只读审查已把封存样本、Gold/查询 SHA、角色去重、固定标签全集、零分母分层诊断和 `F1=0` 边界纳入计分器；这轮修正不改变 canonical 教材内容，也未生成真实方法通过结果。
- 审查—修正记录：`../../work/knowledge/_reviews/SG-METHOD-REVIEW-20260809.md`；明确保留“无真实留出 Gold/教师观察”的限制。
- 试运行自动 semantic lint 已实际执行并通过：lifecycle 唯一性、Markdown 表列数、front matter/ledger、短证据引用和 Claim/Constraint Schema 均为 automatic `pass`；人工检查仍明确为 `not_checked`。
- 2024 部分参考答案候选：`../../work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2024.md`；校验：`../../work/knowledge/_meta/reference_answer_candidate_validation_2024_20260809.json`。
- 2024 独立完整第三方候选：`../../work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2024-MEIPIAN.md`；校验：`../../work/knowledge/_meta/reference_answer_candidate_validation_2024_meipian_20260809.json`。
- 2016 Q006 独立第三方候选：`../../work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2016-Q006.md`；校验：`../../work/knowledge/_meta/reference_answer_candidate_validation_2016_q006_20260809.json`。
- 下面的“Out of scope until `TEXTBOOK-LOCK`”是阶段启动时的历史边界，不能覆盖本快照中的当前阶段。

## Scope

In scope:

- 144 个教材解析源包及其载体、页码映射账本；
- 120 行交付账本：114 项教材核心交付 + 6 项 `SG-TB` 后暂定交付；
- 候选 V2 Schema、受控词表、评分量表和模板；
- 自动校验器及一条真实记录的首通验证；
- 供教材阶段执行者使用的运行与交接说明。
- 首轮校准吞吐的 10 张卡 + 5 张图已完成历史 G2（V2.4 命名为 `SG-CAL`）双评；另补齐 U06-03/04 以解除完整性阻断。

Out of scope until `TEXTBOOK-LOCK`:

- 高考试卷清洗、切分、分类、答案对齐、EKP 提取和真题映射；
- 对尚未取得的高考评价体系、初中教材、四川政策和真题作事实性补写；
- 改写或迁移现有 3 张样卡和 1 份样板图谱。

In scope for the current textbook phase:

- 81 张教材知识卡、28 份单元图谱和 5 份册级总表的分批生产、评审和验收；
- `SG-CAL` 历史校准、`SG-EVAL` 评价切换、`DG0–DG4`、`SG-UNIT/SG-REC/SG-BOOK/SG-METHOD/SG-TB` 门禁；
- 教材来源链、课标版本、教师用书 `edition_match` 和教材侧问题清单的治理。

## Artifact registry

| Artifact family | Active artifact | Status | Result | Approval |
|---|---|---|---|---|
| `01-requirements` | `../../work/语文备课系统_知识点提取研究计划.md` | candidate | V2.4 human-readable baseline; SHA `ebed2184...` | pending V2.4 approval |
| `03-architecture` | `../../work/语文备课系统_知识点提取研究计划.md` §3–§8 | candidate | DG/SG contracts and dependency path defined | pending V2.4 approval |
| `04-implementation-spec` | `04_execution/implementation_spec_20260806_010616.md` | complete | implemented | approved 2026-08-06 |
| `04-first-throughput-evidence` | `04_execution/first_throughput_evidence_20260806_013226.md` | complete | passed | approved 2026-08-06 |
| `04-calibration-throughput` | `04_execution/calibration_throughput_20260806_061159.md` | complete | 10 cards + 5 graphs; G2 passed | coordinator merged 2026-08-07 |
| `04-g2-review` | `04_execution/contract_freeze_20260807.md` + `../../work/knowledge/_reviews/scores/g2_review_summary_20260807.md` | complete | 15 calibration items ≥92 from both roles; R01–R10/P0/P1/P2=0 | approved 2026-08-07 |
| `04-action-plan` | `04_execution/action_plan_20260807_130647.md` | legacy-active | pre-cutover `2.0-textbook` in-flight only; do not use as V2.4 status source | approved 2026-08-07 |
| `04-task-checklist` | `04_execution/task_checklist_20260807_130647.md` | legacy-active | timestamped history; dynamic counts/queue superseded by ledger + manifest | coordinator 2026-08-07 |
| `04-implementation-log` | `04_execution/implementation_log_20260807_130647.md` | active | textbook execution log | coordinator 2026-08-07 |
| `04-evaluation-freeze` | `04_execution/evaluation_freeze_candidate_20260808_014300.md` | candidate/not-active | `2.0-textbook-eval-1`; SHA `73b2bb5d...` | pending V2.4 approval and cutover |
| `04-evaluation-cutover` | `04_execution/evaluation_cutover_checklist_20260808_014300.md` | pending | 25/35 complete; 10/35 pending | machine controls and read-only trial package added; trial/cutover still blocked |
| `05-consistency-audit` | `05_integration_testing_debug/consistency_audit_20260808_131819.md` | complete | 11 contradictions: 6 resolved, 5 flagged; V2.4 activation blocked | audit 2026-08-08 |

## Open questions and blockers

- 高考评价体系官方原件、初中关联依据、四川用卷政策及 2023—2026 真题/答案/评分材料尚未完整登记；基础设施只创建入口和缺失状态。
- `TB2` 与必修下学生教材的版次配套关系仍为 `unknown`，不得提前标成已验证。
- 教材 Schema、词表和量表已通过 G2 冻结为 `2.0-textbook`；后续契约变化必须创建新版本并重新评估。
- `2.0-textbook-eval-1` 仍为 candidate；24 项 cutover 准备未完成，暂无可证明新旧边界的 `cutover_batch_id`。
- 本轮已补齐 content SHA、review binding validator、Claim/Constraint Schema、71 项观察量表、Decimal 计分器、semantic lint 模板、能力矩阵、warning register 和 DG4 receipt Schema；这些文件只支持前向试运行，不等于候选已激活。
- SG-METHOD 计分器明确区分 `metric_status` 与总体 `status`；零分母为 `N/A`，固定查询必须恰好覆盖 12 条，少于 3 名外部教师或当前配置 `blocked` 均不能放行。
- U06 校准图曾只覆盖2/4上游卡，现已补齐 CARD-B1-U06-03/04 并重建为4/4；旧缺口已关闭。

## Change impact assessment

- Affected downstream stages: `SG-EVAL`、教材新批次、`SG-METHOD/SG-TB`、真题契约和全局发布。
- Suggested action: 已领取件按冻结 `2.0-textbook` 闭环；新领取和 WIP 扩展先冻结批次 manifest，完成 24 项 cutover 准备与两个连续绿色试运行批次。
- Approval reset: V2.4 与 `2.0-textbook-eval-1` 均保持 pending/not-active；教材锁定后试卷阶段已解锁为 `SG-EXAM-CAL`，但仍是 candidate structural freeze，未进入正式答案/评分或 M1+ 映射放行。
