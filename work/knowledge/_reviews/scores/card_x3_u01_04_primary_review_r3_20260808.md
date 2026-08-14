---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-04-R3-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-04"
artifact_version: "0.2.2"
artifact_sha256: "aedcd64c718d098255a1b2ab06937a103d5ffec949909c36364d5bc4d073ff31"
review_round: 3
reviewer: "independent_primary_x3_u01_04_r3"
review_role: "primary"
reviewed_at: "2026-08-08T22:25:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "4ab9c4c2f0d8b27ccb854a4552dfd7f56d95622bfc8bf8ee4d500b32f43c38af"
validator_run_id: "VAL-20260808-222015+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-222015+0800.json"
validator_report_sha256: "611f61099c363efd1419f3a91ae0cd9acc2aa805fb8b99577b991d10c0626056"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "56f7e8af35882842e9036bd786b823e1404ae677757095b6833b2ba39781b604"
---

# CARD-X3-U01-04 v0.2.2 重新独立主审 R3

## 1. 输入锁定与状态一致性

本轮对 v0.2.2 返工快照重新进行独立主审，仅使用当前卡片、冻结 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 课4教材、U01任务、现行课标、共享账本和指定 validator 归档报告；不修改卡片、账本、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.2；SHA `aedcd64c718d098255a1b2ab06937a103d5ffec949909c36364d5bc4d073ff31`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `4ab9c4c2f0d8b27ccb854a4552dfd7f56d95622bfc8bf8ee4d500b32f43c38af`；CARD-X3-U01-04 为 v0.2.2/`linted`，记录 `REWORK linted→linted` |
| 课4 canonical | `ART-PKG-X3-004-PDF`；SHA `b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；物理页22—24、切分页1—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；学业质量4-3物理页46 |
| validator | `VAL-20260808-222015+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `611f61099c363efd1419f3a91ae0cd9acc2aa805fb8b99577b991d10c0626056` |

卡片 front matter、正文状态说明、ledger 版本和 REWORK transition 一致；当前为 `linted`，未进入 `accepted`。状态元数据不触发 R08。

## 2. 覆盖与回归核验

- 当前卡片含 2 个正文子文本、17 个 KP、17 个 EV；EV 类型为 Q=13、F=1、M=2、D=1，均为单值 Q/F/M/D。17/17 KP 均有主维度、知识类型、四层归属、判定理由、证据 ID 和置信状态。
- canonical 课4物理页22为《望海潮》，物理页23—24为《扬州慢》序/正文/注释/学习提示；U01任务物理页25/切页1；课标任务群5在物理页25—26、4-3在物理页46。诗词事实、典故、任务和课标短引均可回查。
- 上轮问题均完成回归：EV-001 保持纯教材标题范围；EV-003 为连续完整《望海潮》原文；§8.1 只保留学习提示原意；§3 过程留痕已明确为项目建议；形式/声韵/盛衰比较均已从任务一 EV-009 改回学习提示 EV-007/008；EV-017 补充孙何注释并由 KP-008 回链，扬州相关 KP 显式回链 EV-006。
- 高考严格为 `M0/N/A`，纵向关系为有理由的 N/A，教师用书 `edition_match=unknown`；未消费未登记真题或教师用书意见。

## 3. Claim—Evidence 复核与剩余 P2

《望海潮》的城市空间、市场生活、钱塘潮、孙何仪仗和结句由 EV-003、EV-017 支撑；《扬州慢》的序、今昔对照、战争创伤、号角、杜牧典故和红药结尾由 EV-004—006 支撑；学习提示的城市对象/盛衰、铺叙/点面/虚实、今昔、杜牧想象和声韵由 EV-007—008 支撑；任务 EV-009—013 与课标 EV-014—015 的职责已分离。

唯一保留的非阻断粒度问题是 **KP-002 证据回链偏窄**：其 Claim 同时包含两词作者、城市表现对象、历史处境和情绪方向，但证据 ID 仍为 `EV-002`（题名/作者 F）与 `EV-009`（任务一研讨 Q）。EV-009 不承担城市对象或盛衰判断；应补挂学习提示 EV-007（必要时 EV-008），或收窄 KP-002 Claim 至题名/作者。卡片其他章节已有 EV-007/008，故这是局部 P2，不构成全卡证据缺失或硬拒绝。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | 两词题名、作者、正文事实、城市/人物信息、典故和课标引文与 canonical 载体一致。 |
| R02 | 否 | 17/17 EV 均有适配 Source、Artifact、locator 和短引；KP-002 的局部窄回链列为 P2，其他正式主张均闭合。 |
| R03 | 否 | 两个正文子文本、学习提示、任务、课标、原子 KP、教学模块、M0 和纵向 N/A 齐全。 |
| R04 | 否 | 教材学习提示、研究性概括、项目建议和任务证据已经分层；过程留痕明确为项目建议。 |
| R05 | 否 | 17/17 KP 字段齐全且均有至少一条有效证据；KP-002 有作者证据，城市子主张回链可作 P2 加固。 |
| R06 | 否 | 高考严格保持 `M0/N/A`，未引用未登记真题、答案或评分资料。 |
| R07 | 否 | 只消费已登记并核验的课4教材、U01任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、版本、状态、数量、ID、路径和 SHA 一致；validator 哈希校验通过。 |
| R09 | 否 | 使用现行课标任务群名称和4-3定位，没有改写任务群或把质量描述当课型。 |
| R10 | 否 | 未机械铺满四项核心素养，4-3仅作能力定位。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误或不可恢复损坏。 |
| P1 | 0 | EV-001、§8.1、EV-009错挂和过程留痕边界均已修复。 |
| P2 | 1 | `P2-KP002-CITY-LINK`：KP-002 应补挂 EV-007/008，或收窄 Claim；不阻断其余证据链。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | 17/17 EV 均有 canonical 页位、来源和短引；仅 KP-002 有局部证据回链偏窄。 |
| 事实与术语准确性 | 20 | 18 | 20.0 | 两词事实、典故、页码、任务和课标术语准确。 |
| 字段完整与知识粒度 | 15 | 12 | 14.5 | 2子文本、17 KP、17 EV、任务/课标/M0模块完整；KP-002需补粒度。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 城市盛衰、战争记忆、铺叙、虚实、今昔、声韵和典故双线清楚。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标4-3和 M0 边界合规。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方 accepted 目标时合法使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 三类提示分离，比较和原句—形式—城市情绪路径可直接用于备课。 |
| **合计** | **100** | **85** | **98.0** | **总分及七维单项均达标，R01—R10 全部未触发。** |

## 7. 主审决定

**决定：`pass`；总分 `98.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/1`。**

当前 `CARD-X3-U01-04` v0.2.2/SHA `aedcd64c718d098255a1b2ab06937a103d5ffec949909c36364d5bc4d073ff31` 通过本轮独立主审。当前状态仍为 `linted`，本报告不写回 `accepted`、不修改 ledger、不执行状态迁移；第二复审应以同一 SHA 复核，KP-002 的 P2 建议可在配对前一并加固。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.2；SHA `aedcd64c718d098255a1b2ab06937a103d5ffec949909c36364d5bc4d073ff31`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `4ab9c4c2f0d8b27ccb854a4552dfd7f56d95622bfc8bf8ee4d500b32f43c38af`；版本 `0.2.2`、状态 `linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-222015+0800.json`；SHA `611f61099c363efd1419f3a91ae0cd9acc2aa805fb8b99577b991d10c0626056`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-004-PDF`=`b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填。
