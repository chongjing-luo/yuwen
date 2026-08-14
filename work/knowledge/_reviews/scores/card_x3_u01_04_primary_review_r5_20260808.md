---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-04-R5-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-04"
artifact_version: "0.2.5"
artifact_sha256: "6d9fa909fa4002e5417258ee4c23b9d62f9d994090ec0fddadfcf7b7cb003291"
review_round: 5
reviewer: "independent_primary_x3_u01_04_r5"
review_role: "primary"
reviewed_at: "2026-08-08T22:40:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "69abe22f4656f50259cb269e8934a58bd96d1b65ac848bcf84e0e0ba311bcb44"
validator_run_id: "VAL-20260808-223730+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-223730+0800.json"
validator_report_sha256: "704c2b46c19d80b9d0c64d2fc9e48025398986f53e64cdedce672b6dfc218e98"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "679af381383ba1561277e3e5eb16a7c1f27306e61e59c2c2dbd82934054df15a"
---

# CARD-X3-U01-04 v0.2.5 元数据一致性返工后的独立主审 R5

## 1. 输入锁定与状态一致性

本轮对 v0.2.5 元数据一致性返工候选重新进行独立主审，仅使用当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 课4教材、U01任务、现行课标、共享账本和指定 validator 归档报告；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.5；SHA `6d9fa909fa4002e5417258ee4c23b9d62f9d994090ec0fddadfcf7b7cb003291`；front matter 状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `69abe22f4656f50259cb269e8934a58bd96d1b65ac848bcf84e0e0ba311bcb44`；CARD-X3-U01-04 为 v0.2.5/`linted`，当前过渡为 `REWORK accepted→linted` |
| 课4 canonical | `ART-PKG-X3-004-PDF`；SHA `b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；物理页22—24、切分页1—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；学业质量4-3物理页46 |
| validator | `VAL-20260808-223730+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `704c2b46c19d80b9d0c64d2fc9e48025398986f53e64cdedce672b6dfc218e98` |

卡片 front matter 的 `status: linted`、`reviewers: []` 与正文状态说明“v0.2.5 为 G4 后的元数据一致性返工候选，待双人复审”一致；ledger 同样为 v0.2.5/`linted`。历史上的 v0.2.4 G4 `accepted` 记录被明确保留为历史过渡，不代表当前状态，不触发 R08。

## 2. 覆盖、内容与回归核验

- 当前卡片含 2 个正文子文本、17 个 KP、17 个 EV；EV 类型为 Q=13、F=1、M=2、D=1，均为单值 `Q/F/M/D`。17/17 KP 均有主维度、知识类型、四层归属、判定理由、证据 ID 和置信状态。
- canonical 课4物理页22为《望海潮》，物理页23—24为《扬州慢》序/正文/注释/学习提示；U01任务物理页25/切页1；课标任务群5在物理页25—26、学业质量4-3在物理页46。文本事实、典故、任务和课标短引均可回查。
- 本轮返工目标是元数据一致性，而非内容重写：front matter、正文状态、ledger 版本/状态、`reviewers: []` 和 G4 后 `REWORK accepted→linted` 过渡已相互一致；前轮证据加固仍保留，包括 KP-002 的 EV-007/008、扬州正文 KP 的 EV-005、EV-006 注释 d—j、EV-017 孙何注释，以及 KP-016 对任务三 EV-011/012 的回链。
- 高考严格为 `M0/N/A`，纵向关系为有理由的 `N/A`，教师用书 `edition_match=unknown`；未消费未登记真题、答案、评分资料或教师用书意见。

## 3. Claim—Evidence 复核与剩余风险

《望海潮》的城市空间、市场生活、钱塘潮、孙何仪仗和结句由 EV-003、EV-017 支撑；《扬州慢》的序、今昔对照、战争创伤、号角、杜牧典故和红药结尾由 EV-004—006 支撑；学习提示的城市对象/盛衰、铺叙/点面/虚实、今昔、杜牧想象和声韵由 EV-007—008 支撑；任务 EV-009—013 与课标 EV-014—015 的职责已分离。KP-016 的“原句—形式—城市状态/情绪—主题判断”证据链同时回链任务三意象/意境 EV-011 与虚实 EV-012。

本轮未发现 P0/P1/P2 缺陷。少数复合 Claim 使用物理页级或注释段级宽 locator，但均有连续短引、正确 Artifact 和可回查正文，不构成证据缺失、错源或状态阻断；后续若进入更细粒度图谱，可再拆分 locator，不影响本轮通过。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | 两词题名、作者、正文事实、城市/人物信息、典故、任务和课标引文与 canonical 载体一致。 |
| R02 | 否 | 17/17 EV 均有适配 Source、Artifact、locator 和短引；复合 Claim 的宽 locator 仍可由短引定位，未形成关键主张不可追溯。 |
| R03 | 否 | 两个正文子文本、学习提示、任务、课标、原子 KP、教学模块、M0 和纵向 N/A 齐全。 |
| R04 | 否 | 教材学习提示、任务证据、研究性概括、课标定位、教师用书边界和项目建议已分层；过程留痕没有冒充教材要求。 |
| R05 | 否 | 17/17 KP 字段齐全，均有合法维度、类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考严格保持 `M0/N/A`，未引用未登记真题、答案或评分资料，也未把题型相似性升级为直接映射。 |
| R07 | 否 | 正式内容只消费已登记并核验的课4教材、U01任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、版本、状态、reviewers、数量、ID、路径和 SHA 一致；历史 G4→REWORK 过渡有明确记录，validator 哈希校验通过。 |
| R09 | 否 | 使用现行课标任务群名称和4-3定位，没有改写任务群或把学业质量描述当作单课等级。 |
| R10 | 否 | 未机械铺满四项核心素养，课标4-3仅作能力边界定位。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 元数据状态、reviewers、正文声明和 ledger 过渡已一致；证据职责与教材/任务边界问题均已修复。 |
| P2 | 0 | 未发现会影响后续消费的非阻断性缺陷；宽 locator 仅为可选的进一步细化项。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.5 | 17/17 EV 均有 canonical 页位、来源和短引；少数复合 Claim 的 locator 较宽但可回查。 |
| 事实与术语准确性 | 20 | 18 | 20.0 | 两词事实、典故、页码、任务和课标术语准确。 |
| 字段完整与知识粒度 | 15 | 12 | 14.5 | 2子文本、17 KP、17 EV、任务/课标/M0模块完整；仅保留宽 locator 的轻微粒度扣分。 |
| 双维度与母题质量 | 15 | 12 | 15.0 | 城市盛衰、战争记忆、铺叙、虚实、今昔、声韵和典故双线清楚。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标4-3和 M0 边界合规。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方 accepted 目标时合法使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 三类提示分离，比较和“原句—形式—城市情绪—判断”路径可直接用于备课。 |
| **合计** | **100** | **85** | **99.0** | **总分及七维单项均达标，R01—R10 全部未触发。** |

## 7. 主审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U01-04` v0.2.5/SHA `6d9fa909fa4002e5417258ee4c23b9d62f9d994090ec0fddadfcf7b7cb003291` 通过本轮独立主审。当前状态仍为 `linted`，本报告不写回 `accepted`、不修改 ledger、不执行状态迁移；后续第二复审应绑定本轮列出的同一组 SHA，并在双审完成前保持 `linted`。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.5；SHA `6d9fa909fa4002e5417258ee4c23b9d62f9d994090ec0fddadfcf7b7cb003291`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `69abe22f4656f50259cb269e8934a58bd96d1b65ac848bcf84e0e0ba311bcb44`；版本 `0.2.5`、状态 `linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-223730+0800.json`；SHA `704c2b46c19d80b9d0c64d2fc9e48025398986f53e64cdedce672b6dfc218e98`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-004-PDF`=`b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填该值。
