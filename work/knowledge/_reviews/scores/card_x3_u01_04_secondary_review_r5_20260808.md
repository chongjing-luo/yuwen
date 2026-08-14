---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-04-SECONDARY-R5"
deliverable_id: "CARD-X3-U01-04"
artifact_version: "0.2.5"
artifact_sha256: "6d9fa909fa4002e5417258ee4c23b9d62f9d994090ec0fddadfcf7b7cb003291"
review_round: 5
reviewer: "independent_secondary_x3_u01_04_r5"
review_role: "secondary"
reviewed_at: "2026-08-08T22:31:00+08:00"
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
report_sha256: "05740dbc795884e828ca4d4510331097597c2d00719cf7a6af81badaadf67a17"
---

# CARD-X3-U01-04 v0.2.5 元数据一致性返工后的独立第二复审 R5

## 1. 输入锁定与独立性

本轮重新锁定 v0.2.5 当前快照，使用冻结 `2.0-textbook` rubric/taxonomy、canonical课4教材、U01任务包、现行课标、Source/Artifact注册表、共享账本和指定 validator 归档报告，独立复核内容回归与生命周期元数据；不修改卡片、ledger、validator 或状态迁移。v0.2.5声明为G4后的元数据一致性返工，正文证据内容应与已复审的v0.2.4保持一致。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.5；SHA `6d9fa909fa4002e5417258ee4c23b9d62f9d994090ec0fddadfcf7b7cb003291`；front matter 状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-004-PDF`；SHA `b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；《望海潮》物理页22、切分页1；《扬州慢》物理页23—24、切分页2—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；任务物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群定位物理页25—26、学业质量4-3物理页46 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `69abe22f4656f50259cb269e8934a58bd96d1b65ac848bcf84e0e0ba311bcb44`；CARD-X3-U01-04 为 v0.2.5/`linted` |
| validator | `VAL-20260808-223730+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `704c2b46c19d80b9d0c64d2fc9e48025398986f53e64cdedce672b6dfc218e98` |

## 2. 内容回归与状态一致性

- 当前结构为 `2/2` 正文子文本、`17/17` KP、`17/17` EV；主维度仍仅为“人文/语言”，知识类型仍为冻结枚举“事实/概念/程序/策略/解释”，EV仍为单值 `Q/F/M/D`（Q=13、F=1、M=2、D=1）。
- 课4 canonical 页位未漂移：《望海潮》物理页22/切页1，《扬州慢》物理页23—24/切页2—3；学习提示物理页24/切页3；U01任务物理页25/切页1；课标学业质量4-3物理页46。正文、注释、学习提示、任务和教师用书缺源边界与v0.2.4复审绑定一致。
- EV-001仍是纯教材标题范围；EV-003为《望海潮》连续正文；EV-005为《扬州慢》正文；EV-006 locator为注释d—j；EV-017支撑孙何身份/赠词对象；KP-010/011/013/014均保留正文EV-005与注释EV-006；KP-016及诗词鉴赏证据链同时挂接任务三EV-011和EV-012。
- 第8.1节只陈述教材学习提示，第8.3节单独标注项目建议；过程留痕和修订没有写成教材任务要求。高考栏保持 `M0/N/A`，纵向关系保持有理由的 `N/A`，教师用书 `edition_match=unknown`。
- **生命周期状态一致性**：front matter 为 `status: linted`，正文明确“v0.2.5为G4后元数据一致性返工候选，待双人复审”；ledger记录 v0.2.4/G4 `accepted` 后 v0.2.5 `REWORK` 从 `accepted → linted`，`pre_sha256` 为 `b676772fb0486d1a82622abaadaa8e475eff75839879e425ea82898ed58be513`，`post_sha256` 为当前卡片SHA `6d9fa909fa4002e5417258ee4c23b9d62f9d994090ec0fddadfcf7b7cb003291`。卡片 version、ledger version/status/transition、validator hash verification 与当前快照一致，旧 accepted 状态未残留为当前状态。

## 3. R01—R10 判定

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两首词题名、作者、正文事实、城市与人物信息、典故和课标4-3引文均与canonical载体一致。 |
| R02 | 否 | `17/17` EV均有可解析Source/Artifact/locator/短引；正文、注释、学习提示和任务三两项探究均已显式回链。 |
| R03 | 否 | 两个正文子文本、学习提示、单元任务、课标、原子KP、M0、纵向和三类教学提示模块均存在。 |
| R04 | 否 | 正文、学习提示、任务、课标M、教师用书D和项目建议已分层；过程留痕未写成教材要求。 |
| R05 | 否 | `17/17` KP均具备合法维度、知识类型、四层主归属、判定理由和证据；EV均为单值Q/F/M/D。 |
| R06 | 否 | 高考保持结构化M0/N/A，未引用未登记真题、答案或评分资料，也未声称M1—M3直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课4教材、U01任务包和现行课标canonical Artifact。 |
| R08 | 否 | 卡片 version/SHA、ledger transition/status、Source/Artifact ID、KP/EV数量、路径和指定 validator 绑定一致。 |
| R09 | 否 | 使用现行课标“文学阅读与写作”“语言积累、梳理与探究”及物理页46的4-3，未改写任务群名称或把质量描述当课型。 |
| R10 | 否 | 未机械铺满四项核心素养，也未将学业质量4-3当作单课完整等级或题目难度标签。 |

## 4. P0/P1/P2

`P0/P1/P2 = 0/0/0`。

本轮未发现关键事实错误、错页或不可定位引文、非法枚举、版本/状态断链、M0越权、字段缺失、来源职责混写或教师用书误引。v0.2.5仅进行元数据一致性返工，内容回归与生命周期绑定均通过。

## 5. 2.0-textbook 量规评分

| 维度 | 权重 | 门槛 | 得分 | 复核依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 25.0 | `17/17` EV的来源、canonical页位和短引可回查；正文、注释、学习提示和任务三两项探究均闭合。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两词事实、城市/人物/典故、学习提示、课标术语和元数据边界准确；对少数研究性跨句概括作保守校准扣0.5。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | `2/2`正文子文本、`17/17` KP、`17/17` EV、任务/课标/教学/M0/N/A模块完整。 |
| 双维度与母题质量 | 15 | 12 | 15.0 | 人文/语言覆盖城市盛衰、战争记忆、铺叙、虚实、声韵、典故和炼字，文本差异保留充分。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标4-3定位和M0不确定性均清楚。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方accepted逐边证据时合法保持有理由的N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | §8.1/§8.3已分层，过程留痕已明确为项目建议，城市比较和任务探究路径可直接用于备课。 |
| **合计** | **100** | **85** | **99.5** | R01—R10及P0/P1/P2均通过。 |

## 6. 元数据返工后的独立第二复审决定

**决定：`pass`。** 当前 `CARD-X3-U01-04` v0.2.5/SHA `6d9fa909fa4002e5417258ee4c23b9d62f9d994090ec0fddadfcf7b7cb003291` 通过元数据一致性返工后的独立第二复审，可与同一最终SHA的主审结果配对进入后续流程。当前 ledger 状态仍为 `linted`，而非上一版本的 `accepted`；本报告不执行状态迁移。卡片、canonical Artifact、validator、账本或版本绑定任一变化均使本报告失效，须按新SHA复审。

## 7. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.5；SHA `6d9fa909fa4002e5417258ee4c23b9d62f9d994090ec0fddadfcf7b7cb003291`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `69abe22f4656f50259cb269e8934a58bd96d1b65ac848bcf84e0e0ba311bcb44`；v0.2.5 transition 为 `accepted → linted`/`REWORK`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-223730+0800.json`；SHA `704c2b46c19d80b9d0c64d2fc9e48025398986f53e64cdedce672b6dfc218e98`；结果 `passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-004-PDF`=`b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 报告 SHA-256按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 值置空后对canonical报告字节求SHA，再回填该值；另行记录实际文件SHA。
