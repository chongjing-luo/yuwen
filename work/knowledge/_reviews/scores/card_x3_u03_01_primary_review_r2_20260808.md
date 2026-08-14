---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U03-01-R2-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U03-01"
artifact_version: "0.2.1"
artifact_sha256: "e17a5c2a81610374797f720064ffa35560fd417e5b845e6a400c9d78c70f6f5a"
review_round: 2
reviewer: "independent_primary_x3_u03_01_r2"
review_role: "primary"
reviewed_at: "2026-08-08T23:55:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "7c80ccebaf12391d985078862787a0bbb887d7ae59471814610ac6533a055e71"
validator_run_id: "VAL-20260808-234943+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u03_01_rework_post_u03_03_validation_20260808.json"
validator_report_sha256: "21974ac83bc6af7aa16b0ee86cd9ada7a84ade4c24215e5a97fca0cf82f9e0e3"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "61a9837f48c20f85bd1f1bc04f8950ca510939afa02ea5bc40e61b01950ef503"
---

# CARD-X3-U03-01 v0.2.1 修订后的独立主审 R2

## 1. 输入锁定与状态一致性

本轮以 v0.2.1 修订快照重新进行独立主审，重点回归上一轮两项 P1：KP-011 的人物动作归属，以及教材学习提示与项目建议的分层；仅依据当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、课9《陈情表》《项脊轩志》及导语/学习提示、U03单元研习任务、现行课标、共享账本和指定 validator 报告复核。不修改卡片、ledger、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U03-01.md`；v0.2.1；SHA `e17a5c2a81610374797f720064ffa35560fd417e5b845e6a400c9d78c70f6f5a`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `7c80ccebaf12391d985078862787a0bbb887d7ae59471814610ac6533a055e71`；CARD-X3-U03-01 为 v0.2.1/`linted`，含 `REWORK linted→linted` 记录 |
| 课9 canonical | `ART-PKG-X3-011-PDF`；SHA `c39d21aa9ebabe1870de3d2f4b5d07676217214ec24d846d7cdf5eec9b3c8b8e`；导语物理页74、两文正文物理页75—78、学习提示物理页79 |
| U03任务 canonical | `ART-PKG-X3-015-PDF`；SHA `e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；物理页90—91 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群8物理页29—30、学业质量4-3物理页46 |
| validator | `VAL-20260808-234943+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `21974ac83bc6af7aa16b0ee86cd9ada7a84ade4c24215e5a97fca0cf82f9e0e3` |

卡片 front matter 的 `status: linted`、`reviewers: []`、正文状态说明与 ledger 的 v0.2.1/`linted` 一致；状态元数据不触发 R08。

## 2. 覆盖、证据与返工回归核验

- 卡片覆盖 U03 导语、课9两篇正文和学习提示：导语物理页74/切页1，《陈情表》物理页75—77/切页2—4，《项脊轩志》物理页77—78/切页4—5，学习提示物理页79/切页6；U03任务物理页90—91；课标任务群8物理页29—30、学业质量4-3物理页46。
- `20/20` KP 均有唯一 ID、合法主维度（仅“人文/语言”）、冻结知识类型、四层主归属、判定理由、证据 ID 和置信状态；`20/20` EV 均为单值 `Q/F/M/D`（Q=16、F=1、M=2、D=1）。
- P1-A 已关闭：KP-CARD-X3-U03-01-011 现明确区分“母亲以指叩门”与“祖母持象笏至”，不再写成“祖母叩门赠象笏”；EV-009 的 canonical locator 为物理页78/切页5，能够回查两组连续正文动作、对话和遗迹细节。
- P1-B 已关闭：§8.1 现在只保留教材学习提示对两文情感结构、平淡语言和表文得体的概括；“重点语言观察”已移入 §8.3“本项目教学建议”，并明确“不冒充教材要求或教师用书意见”，同时保留教材 EV 回链。
- 导语关于魏晋至明代六篇散文、反复诵读/涵泳/梳理/评点，课文关于李密的祖孙处境、征召两难、表文得体，《项脊轩志》的空间、家变、亲情细节、后记和枇杷树，及任务一至四、任务群8和4-3定位，均可回到绑定的 canonical PDF。
- 高考栏严格保持 `N/A / M0 / N/A`，纵向关系合法保持 N/A；教师用书 `edition_match=unknown`，未消费未登记教师用书、网络解析、外部训诂或未经逐小问核验的真题。

## 3. Claim—Evidence 回归与剩余风险

上一轮人物动作错误已被正文准确回查：母亲的“以指叩门扉”与祖母“持一象笏至”在物理页78分别出现；当前 KP-011 的表述与 EV-009 的页位及相关 EV-011 学习提示职责一致。§8.1/§8.3 已完成规范教材提示、项目建议和教师用书边界的分层，未再把项目清单冒充教材结论。

其余 20 条 EV 的 Source、Artifact、locator、短引、支撑关系和 `verified` 元数据闭合。少数复合 Claim 使用代表性短引或跨页 locator，但均可在正确 canonical PDF 的声明页位回查，不形成独立 P2 缺陷。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | KP-011 的母亲/祖母动作归属已按 canonical 正文修正；两文题名、作者、人物、事件、文体和课标术语均一致。 |
| R02 | 否 | `20/20` EV 均有适配 Source、canonical Artifact、可解析 locator、短引和 `verified` 状态；KP-011 修订后的 Claim 可由物理页78正文回查。 |
| R03 | 否 | 导语、两篇正文、学习提示、U03任务、课标、20个KP、教学模块、M0和纵向N/A齐全，无合编文本漏项。 |
| R04 | 否 | 教材学习提示仅保留规范栏目可支持的概括；语言观察清单和结构线等内容明确放在“本项目教学建议”，不冒充教材或教师用书结论。 |
| R05 | 否 | 20/20 KP 均具备合法维度、受控知识类型、四层归属、判定理由、有效证据和置信状态。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，未引用未登记真题、答案或评分资料，也未声称 M1—M3 直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课9教材包、U03任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、20 KP、20 EV、版本、路径和 SHA 一致；validator 哈希校验通过。 |
| R09 | 否 | 使用现行课标任务群8“中华传统文化经典研习”和物理页29—30，未改写任务群名称或把任务群当固定课型/教法。 |
| R10 | 否 | 人文/语言双线按古代散文、文体语言、文化观念和表达活动展开，未机械铺满四项核心素养，也未把学业质量4-3当作单课等级或题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 上轮人物动作张冠李戴和教材提示/项目建议混写均已修复；本轮未发现新的关键事实、证据、边界或版本缺陷。 |
| P2 | 0 | 本轮未发现独立的非阻断性缺陷；现有复合 Claim 的短引和页位均可回查。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.5 | 20/20 EV 的来源、canonical Artifact、物理/切页、短引和验证状态闭合；KP-011 回归定位已复核。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两篇正文、人物动作、古代散文术语、任务群8和4-3定位准确；开放解释均保留边界。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 导语/两文/提示、20/20 KP、20/20 EV、任务/课标/M0模块齐全。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文与语言双线覆盖伦理处境、亲情记忆、文体得体、空间叙事、骈散/章法/评点和真实表达。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、任务群8、学业质量4-3定位和 M0 边界均合规。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方 accepted 目标时合法使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 教材提示、教师用书边界和项目建议已分层；比较、评点、词类活用和书信路径可直接备课。 |
| **合计** | **100** | **85** | **98.5** | **总分及七维单项均达标；R01—R10 全部未触发。** |

## 7. 主审决定

**决定：`pass`；总分 `98.5/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U03-01` v0.2.1/SHA `e17a5c2a81610374797f720064ffa35560fd417e5b845e6a400c9d78c70f6f5a` 通过本轮独立主审，可与同一 SHA 的独立第二复审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、validator 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U03-01.md`；v0.2.1；SHA `e17a5c2a81610374797f720064ffa35560fd417e5b845e6a400c9d78c70f6f5a`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `7c80ccebaf12391d985078862787a0bbb887d7ae59471814610ac6533a055e71`；CARD-X3-U03-01 为 `linted`/`REWORK`。
- validator：`work/knowledge/_meta/validation_reports/x3_u03_01_rework_post_u03_03_validation_20260808.json`；运行 ID `VAL-20260808-234943+0800`；SHA `21974ac83bc6af7aa16b0ee86cd9ada7a84ade4c24215e5a97fca0cf82f9e0e3`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-011-PDF`=`c39d21aa9ebabe1870de3d2f4b5d07676217214ec24d846d7cdf5eec9b3c8b8e`；`ART-PKG-X3-015-PDF`=`e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填该值。
