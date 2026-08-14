---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-04-R2-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-04"
artifact_version: "0.2.1"
artifact_sha256: "a4d71896e6ecc3a3f0694dacb9b3c0378b8842bd15e5abe9b1d7c035ca8f27be"
review_round: 2
reviewer: "independent_primary_x3_u01_04_r2"
review_role: "primary"
reviewed_at: "2026-08-08T22:20:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "1d6be0814b9ac617ffb839b50f1781212c7776670f4a69522089a169414e9f68"
validator_run_id: "VAL-20260808-221510+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-221510+0800.json"
validator_report_sha256: "b7be568f406ca63e6e1d946ae1934de2d95a118aee594642d582bdd035e668b9"
validator_result: "passed"
decision: "rework"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "d5ea2727cbc5d2321d124fefceb1c705cc9c6a51525697440d0df63d4bc73db7"
---

# CARD-X3-U01-04 v0.2.1 重新独立主审 R2

## 1. 输入锁定与状态一致性

本轮从 v0.2.1 返工快照重新开始，仅使用当前卡片、冻结 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 课4教材、U01任务、现行课标、共享账本和指定 validator 归档报告；不修改卡片、账本、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.1；SHA `a4d71896e6ecc3a3f0694dacb9b3c0378b8842bd15e5abe9b1d7c035ca8f27be`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `1d6be0814b9ac617ffb839b50f1781212c7776670f4a69522089a169414e9f68`；CARD-X3-U01-04 为 v0.2.1/`linted`，记录 `REWORK linted→linted` |
| 课4 canonical | `ART-PKG-X3-004-PDF`；SHA `b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；物理页22—24、切分页1—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；学业质量4-3物理页46 |
| validator | `VAL-20260808-221510+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `b7be568f406ca63e6e1d946ae1934de2d95a118aee594642d582bdd035e668b9` |

卡片 front matter、正文状态说明、ledger 版本和 REWORK transition 一致；当前为 `linted`，尚未进入 `accepted`。状态元数据本身不触发 R08。

## 2. 回归覆盖与已修复项

- 当前卡片仍有 2 个正文子文本、17 个 KP、16 个 EV；EV 类型 Q=12、F=1、M=2、D=1，均为单值 Q/F/M/D。17/17 KP 均有主维度、知识类型、四层归属、判定理由、证据 ID 和置信状态。
- 课4物理页22为《望海潮》，物理页23—24为《扬州慢》序/正文/注释/学习提示；U01任务物理页25/切页1；课标任务群5在物理页25—26、4-3在物理页46。正文事实、页码、典故、任务和课标短引均可回查。
- 上轮两项 P1 已修复：EV-001 已收窄为纯教材标题范围；§8.1 已只保留教材学习提示直接支持的城市对象、盛衰、铺叙/虚实、今昔、杜牧想象和声韵诵读。EV-003 已补齐《望海潮》连续原文 span；KP-017 已收窄为教材直接任务并在判定理由中将过程留痕标为项目建议。
- M0/N/A、高考边界、纵向 N/A 和教师用书 `edition_match=unknown` 均保持规范。

## 3. 新发现：学习提示证据 ID 错挂（P1）

当前多个明确来自学习提示的主张仍引用 `EV-CARD-X3-U01-04-009`，但 EV-009 是 U01 **任务一**“今天，我们为什么读古诗词”研讨证据，不是课4学习提示。具体包括：

- §2“盛世与劫后对照”行把学习提示主张挂到 EV-009；有效证据应为 EV-007。
- §3“两词的城市书写比较”与“诵读与声韵”两行均挂 EV-009；形式/声韵主张应由 EV-008 支撑。
- KP-007（铺叙、以点带面、虚实相间）和 KP-015（两词比较策略）均只挂 EV-009；应分别改挂 EV-008 或 EV-007+008。

这些 ID 均存在，因此不是文件/ID 断链（R08 不触发），但当前行的唯一证据来自任务一，不能承担学习提示中的形式、盛衰和声韵 Claim；该 Claim—Evidence—Source 链未闭合，并再次混淆任务与学习提示来源边界。建议统一核对所有 `EV-009` 引用：保留任务一研讨主张的 EV-009，其余学习提示主张改回 EV-007/008，并重跑证据链接检查。

### 非阻断 P2

§3“诵读与表达迁移”仍写“成果应保留引文、提纲、反馈和修订”，虽 KP-017 判定理由已说明过程留痕属于项目建议，但该描述行没有明确的项目层标签。建议补写“本项目建议”或收窄到任务原文直接成果，以消除局部语气不一致。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | 两词题名、作者、正文事实、城市/人物信息、典故和课标引文均与 canonical 载体一致。 |
| R02 | **是** | §2/§3、KP-007、KP-015 的学习提示 Claim 错挂任务一 EV-009，当前唯一证据不适配正式主张。 |
| R03 | 否 | 两个正文子文本、学习提示、任务、课标、原子 KP、三类教学模块、M0 和纵向 N/A 齐全。 |
| R04 | **是** | 将任务一 EV-009 当作学习提示形式/声韵/盛衰证据，造成任务与教材学习提示边界混淆。 |
| R05 | 否 | 17/17 KP 字段完整；错挂证据可通过改 ID 修复，尚未形成全卡 KP 无有效证据。 |
| R06 | 否 | 高考严格保持 `M0/N/A`，未引用未登记真题、答案或评分资料。 |
| R07 | 否 | 只消费已登记并核验的课4教材、U01任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、版本、状态、数量、ID 和路径一致；问题是证据职责错挂，不是链接不存在。 |
| R09 | 否 | 使用现行任务群名称和物理页46学业质量定位，没有改写课标或把质量描述当课型。 |
| R10 | 否 | 未机械铺满四项核心素养，4-3仅作能力定位。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误或不可恢复损坏。 |
| P1 | 1 | `P1-EV009-MISLINK`：学习提示/形式/声韵 Claim 及 KP-007、KP-015 错挂任务一 EV-009，应改回 EV-007/008。 |
| P2 | 1 | `P2-SEC3-PROCESS-TONE`：描述行仍以任务要求语气写过程留痕，虽 KP-017 理由已标项目建议。 |

## 6. 2.0-textbook 诊断评分

因 R02/R04 与 P1 硬门触发，正式验收分记为 `N/A`；以下分数仅用于返工定位。

| 维度 | 权重 | 门槛 | 诊断得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 19.0 | 绝大多数 EV、页位和 span 已闭合；5处学习提示 Claim 错挂 EV-009，需逐项改链。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两词事实、典故、页码、任务和课标术语准确；扣分仅来自证据职责错挂。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2子文本、17 KP、16 EV、任务/课标/M0模块完整；KP-017主张已收窄。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 城市盛衰、战争记忆、铺叙、虚实、今昔、声韵和典故结构清楚。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标4-3和 M0 边界合规。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方 accepted 目标时使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 6.0 | §8.1已分层且项目建议可用；过程留痕描述仍需加标签。 |
| **诊断合计** | **100** | **85** | **92.0** | 仅供返工定位；R02/R04硬门触发，不能作为放行分数。 |

## 7. 返工与主审决定

1. 全面核对 EV-009 引用：EV-009 只保留任务一研讨；§2“盛世与劫后”、§3两行、KP-007 和 KP-015 改用 EV-007/008，并检查相关 Claim 的最小适配证据。
2. 将“成果应保留引文、提纲、反馈和修订”显式标为本项目建议，或删去未由任务原文承担的过程要求。
3. 升版并重算卡片 SHA、更新 ledger transition、重跑 validator，再以新 SHA 进行独立主审和第二复审；当前 SHA 不得进入 `accepted` 或被单元图谱正式消费。

**主审决定：`rework`。** 当前 `CARD-X3-U01-04` v0.2.1/SHA `a4d71896e6ecc3a3f0694dacb9b3c0378b8842bd15e5abe9b1d7c035ca8f27be` 未通过重新独立主审。本报告不执行任何状态迁移。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.1；SHA `a4d71896e6ecc3a3f0694dacb9b3c0378b8842bd15e5abe9b1d7c035ca8f27be`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `1d6be0814b9ac617ffb839b50f1781212c7776670f4a69522089a169414e9f68`；状态 `linted`、transition `REWORK`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-221510+0800.json`；SHA `b7be568f406ca63e6e1d946ae1934de2d95a118aee594642d582bdd035e668b9`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-004-PDF`=`b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填。
