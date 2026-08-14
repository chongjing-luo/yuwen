---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-U03-01-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X2-U03-01"
artifact_version: "0.2.1"
artifact_sha256: "c414d994a5e21f741637ef6d848b01c8ae7eefafbdaa3821e5097ceb9ef1b432"
review_round: 1
reviewer: "independent_primary_x2_u03_01_r1"
review_role: "primary"
reviewed_at: "2026-08-08T18:32:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-182442+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/x2_u03_cards_validation_bind.json"
validator_report_sha256: "87860bde69eb6b3217161542595b312d8005e6de570b0df891defd3424423e8f"
validator_result: "passed"
decision: "pass"
---

# CARD-X2-U03-01 v0.2.1 独立主审 R1

## 1. 锁定对象与范围

- 本轮只审当前 `work/knowledge/选择性必修中册/cards/CARD-X2-U03-01.md` v0.2.1，SHA-256 为 `c414d994a5e21f741637ef6d848b01c8ae7eefafbdaa3821e5097ceb9ef1b432`；不复用旧版判断。
- 量表为冻结 `2.0-textbook` 知识卡量表（总分门槛 85；七维门槛 21/18/12/12/8/6/5）。当前 ledger 为 `linted / v0.2.1 / root`，本报告不修改卡片、账本或验证归档。

| 来源 | canonical Artifact / SHA | 覆盖 |
|---|---|---|
| 教材包 | `ART-PKG-X2-011-PDF` / `a32687c5561efa28c5d1924a75f6762dae2dc605e9921915b6095141220182d4` | 导语物理页86；《屈原列传》物理页87—90；学习提示物理页91 |
| U03 任务 | `ART-PKG-X2-014-PDF` / `0479f6c8ba0eec387251220f76e97014c14d27787e992e557eef30eadffb82cb` | 物理页104—105，切分页1—2 |
| 现行课标 | `ART-CURR-2020-PDF` / `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` | 任务群8及学业质量定位 |

## 2. 结构与证据复核

`VAL-20260808-182442+0800` 为 `passed`，六类检查均 0 errors，hash verification=true。本卡结构为 1 个正文子文本、16 个 KP、19 个 EV（Q/F/M/D 单值类型），并含课标、任务、教学提示、纵向 N/A 和高考 M0 模块。正文史实、屈原与《离骚》关系、渔父对话、太史公曰、任务年表/史传探究和课标定位总体有 canonical locator。

人工 Claim—Evidence 复核未发现硬性证据错配。v0.2.1 已将 KP-003 的“博闻强志……入则与王图议国事……出则接遇宾客”绑定到 `EV-CARD-X2-U03-01-003`，并将 KP-004 的上官大夫进谗、宪令草稿和“王怒而疏屈平”绑定到 `EV-CARD-X2-U03-01-004`；KP-013 的投江细节也由 `EV-CARD-X2-U03-01-010` 显式支撑。其余 KP/EV、材料边界、M0、N/A 与教师用书 `unknown` 分层清楚。

## 3. R01—R10 硬性检查

| 代码 | 触发？ | 结论 |
|---|---|---|
| R01 | 否 | 题名、作者、屈原身份、历史事件和史家评价均与规范页86—91一致。 |
| R02 | 否 | v0.2.1 的 KP-003、KP-004 已绑定适配的 EV-003/004，Claim—EV 闭合。 |
| R03 | 否 | 1 个正文子文本、学习提示、任务、课标、纵向、高考和三类教学提示模块齐全。 |
| R04 | 否 | 正文、栏目、课标、任务和项目建议分层；未将外部史料或 MinerU 派生文本冒充规范来源。 |
| R05 | 否 | 所有原子 KP 均有能覆盖其完整主张的有效证据 ID；KP-013 的投江细节亦已显式补证。 |
| R06 | 否 | 高考仅为 M0，未引用未登记真题或声称直接衔接。 |
| R07 | 否 | 仅消费已登记学生教材、任务包和现行课标。 |
| R08 | 否 | 当前卡内 ID、版本、数量和路径结构一致；问题是两处语义证据绑定，不是数量/版本断链。 |
| R09 | 否 | 使用现行任务群“中华传统文化经典研习/思辨性阅读与表达”，未改写任务群名称。 |
| R10 | 否 | 未机械铺满核心素养，学业质量保持定位而非完整水平判定。 |

## 4. 量表评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.5 | 19/19 EV 均有 canonical locator，KP-003/004/013 的正文主张与适配证据已闭合。 |
| 事实与术语准确性 | 20 | 18 | 20.0 | 史传书目信息、屈原史实、《离骚》评说和课标术语准确。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 1 个正文子文本、16 KP、19 EV、任务/课标/教学模块完整，KP 原子化且文本特异。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 历史现场、人格选择、史家情感与叙议结合均有母题；语言/人文双线扎实，保守扣 0.5 给少量复合解释的压缩表达。 |
| 四层与高考映射 | 10 | 8 | 10.0 | KP 层级和理由齐全，课标 M 可定位，高考 M0 边界清楚。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前无双方 accepted 目标时合法保持 N/A。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | 年表、人物短评和“史实—语言—史家评价”路径可操作；证据链已满足正式备课前的复核要求。 |
| **合计** | **100** | **85** | **98.5** | 未触发 R01—R10，满足各维度门槛。 |

## 5. P0/P1/P2 与决定

| 等级 | 数量 | 说明 |
|---|---:|---|
| P0 | 0 | 无来源伪造、重大事实错误或不可恢复损坏。 |
| P1 | 0 | v0.2.1 已修正 KP-003/004 证据适配并补足 KP-013 投江细节证据。 |
| P2 | 0 | 未发现需要阻断接受的可选问题。 |

**主审决定：`pass`。** 当前 v0.2.1/SHA 可进入下一阶段校准/闭环。

## 6. 可复现信息

- 卡片：`work/knowledge/选择性必修中册/cards/CARD-X2-U03-01.md`，v0.2.1，SHA `c414d994a5e21f741637ef6d848b01c8ae7eefafbdaa3821e5097ceb9ef1b432`。
- Validator：`VAL-20260808-182442+0800`，`passed`，0 errors；报告 `work/knowledge/_meta/validation_reports/archive/x2_u03_cards_validation_bind.json`，SHA `87860bde69eb6b3217161542595b312d8005e6de570b0df891defd3424423e8f`。
- Rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 分母：1 个正文子文本、16 KP、19 EV；高考 1 行 M0；纵向 1 行 N/A。
