---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U03-03-R2-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U03-03"
artifact_version: "0.2.1"
artifact_sha256: "ec394cc0e7c0b1f3a9354baad3123a06265a6f057423a8e3c00869e017869b4c"
review_round: 2
reviewer: "independent_primary_x3_u03_03_r2"
review_role: "primary"
reviewed_at: "2026-08-09T04:15:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "5f81e5db423aa2b3e6b989f0cf7eecd1f3f5f5bf4bd3e81e270ed13c183c7fc5"
validator_run_id: "VAL-20260809-004003+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u03_03_rework_validation_20260809.json"
validator_report_sha256: "5c08782f4f73cb238cb08de16e6c130282c84c4f904bcd9a52c0173f83862939"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "b5afc40c616c579b46dc97194da0122c6a83dbc50e5e8153646646bc67522dfa"
---

# CARD-X3-U03-03 v0.2.1 独立主审 R2

## 1. 输入锁定与独立性

本轮以 v0.2.1 修订快照重新独立复核，重点回归上一轮教材学习提示/项目建议边界、人称代词证据、课标短引和传统观念讨论边界；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U03-03.md`；v0.2.1；SHA `ec394cc0e7c0b1f3a9354baad3123a06265a6f057423a8e3c00869e017869b4c`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `5f81e5db423aa2b3e6b989f0cf7eecd1f3f5f5bf4bd3e81e270ed13c183c7fc5`；CARD-X3-U03-03 为 v0.2.1/`linted`，含 `REWORK linted→linted` 记录 |
| 课文 canonical | `ART-PKG-X3-013-PDF`；SHA `e5143a84416821bb521ca59683999d86009d91d60ad7dbfa22820eec4272a297`；正文物理页86—87、学习提示物理页87 |
| U03任务 canonical | `ART-PKG-X3-015-PDF`；SHA `e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；物理页90—91 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群8物理页29—30、学业质量4-3物理页46 |
| validator | `VAL-20260809-004003+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `5c08782f4f73cb238cb08de16e6c130282c84c4f904bcd9a52c0173f83862939` |

卡片 `status: linted`、`reviewers: []`、版本记录与 ledger 一致。本报告只记录主审，不执行状态迁移。

## 2. 修订回归核验

- §8.1 现在只保留教材学习提示直接支持的因事明理、叙事说理、婉而多讽、对举/类比及人称代词归纳；结构链、代词操作清单等研究性操作已移入 §8.3 并明确为项目建议，R04 已关闭。
- EV-012 已补全学习提示给出的第一、第二、第三人称代词例项及“从课文或之前学过文章找实例”的要求，KP-012 的三类归纳 Claim 具备完整短引。
- EV-017 已补足课标任务群8中“阅读作品应写出内容提要和阅读感受”“撰写评论”连续短引，KP-018 的课标正式主张闭合。
- KP-015 已收窄为说明“顺木之天”、烦令扰民和官戒的历史语境与现实启示；对可能边界的回应明确为本项目建议，不再冒充任务一硬要求。

覆盖复核：`1/1` 子文本、`18/18` KP、`18/18` EV 均有唯一 ID、合法主维度、受控知识类型、四层主归属、判定理由和证据回链；EV 类型为单值 `Q/F/M/D`。正文物理页86—87、学习提示87、任务90—91、课标任务群8/学业质量4-3页位正确。教师用书为 `edition_match=unknown`，高考保持 `N/A / M0 / N/A`，纵向关系保持有理由的 `N/A`。

## 3. Claim—Evidence 复核

《种树郭橐驼传》的命名与职业、顺木之天、他植者反面、官理类比、烦令扰民及官戒由 EV-002—008 闭合；学习提示的寓意、叙事说理、对举类比、传记结构、现实针对性和人称代词由 EV-009—012 闭合；U03任务和课标由 EV-013—018 闭合。

本轮重点确认修订未制造新来源错配：KP-014 的评点依据同时使用本文学习提示和任务二，但不把任务操作写成教材提示；KP-016 的词类活用仅回链任务三；KP-017 的书信表达仅回链任务四。18/18 EV 的 locator、短引、支撑关系和核验状态闭合，未发现新的事实、证据粒度、边界或版本缺陷。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、作者、人物、种树操作、官理寓意、学习提示术语和课标术语均与 canonical 来源一致。 |
| R02 | 否 | 18/18 EV 均有适配 Source、Artifact、可解析 locator、短引和 `verified` 状态；EV-012/017 已补全相关子主张。 |
| R03 | 否 | 1个正文子文本、学习提示、U03任务、课标、18个KP、18条EV、教学/M0/纵向模块齐全。 |
| R04 | 否 | 教材学习提示、任务、课标、教师用书缺源和项目建议已分层；§8.1不再含项目化结构/代词操作清单。 |
| R05 | 否 | 18/18 KP 均有合法主维度、受控知识类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，没有未登记真题、答案或评分资料或越级映射。 |
| R07 | 否 | 正式内容只消费登记并核验的课文、任务和现行课标 Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、18 KP、18 EV、版本、路径和 SHA 绑定一致；v0.2.1 REWORK记录闭合。 |
| R09 | 否 | 使用现行课标任务群8和学业质量4-3定位，未改写任务群名称或把质量描述当课型/难度。 |
| R10 | 否 | 人文/语言双线按文本需要展开，未机械铺满核心素养，未把学业质量4-3当作单课完整等级。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 学习提示/项目建议分层、代词证据、课标短引和传统观念讨论边界均已修复；无关键事实或版本硬错。 |
| P2 | 0 | 本轮未发现独立的非阻断性缺陷；修订项逐一闭合。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **25.0** | 18/18 EV 的来源、canonical Artifact、物理/切页、短引和状态闭合；EV-012、EV-017修订已回归通过。 |
| 事实与术语准确性 | 20 | 18 | **19.5** | 正文人物、种树原则、官理讽喻、传记/叙事说理、人称代词和课标术语准确。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 1/1子文本、18/18 KP、18/18 EV及任务/课标/M0/纵向/教学模块齐全。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线覆盖顺应天性、以爱为害、烦令扰民、官戒和求实；语言线覆盖叙事说理、对举类比、婉讽和代词梳理。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 四层主归属、理由、任务群8、学业质量4-3和M0/N/A边界完整。 |
| 纵向贯通 | 8 | 6 | **8.0** | 无双方可核验的纵向 KP 关系时合法使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 三类提示和项目建议分离；结构链、评点、代词梳理、文化讨论和书信任务可直接备课。 |
| **合计** | **100** | **85** | **99.0** | **总分及七维单项达到冻结门槛；R01—R10全部未触发。** |

## 7. 独立主审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U03-03` v0.2.1/SHA `ec394cc0e7c0b1f3a9354baad3123a06265a6f057423a8e3c00869e017869b4c` 通过本轮独立主审，可与同一 SHA 的独立第二复审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、canonical Artifact、validator、ledger 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U03-03.md`；v0.2.1；SHA `ec394cc0e7c0b1f3a9354baad3123a06265a6f057423a8e3c00869e017869b4c`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `5f81e5db423aa2b3e6b989f0cf7eecd1f3f5f5bf4bd3e81e270ed13c183c7fc5`。
- validator：`work/knowledge/_meta/validation_reports/x3_u03_03_rework_validation_20260809.json`；run `VAL-20260809-004003+0800`；SHA `5c08782f4f73cb238cb08de16e6c130282c84c4f904bcd9a52c0173f83862939`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：课文 `ART-PKG-X3-013-PDF`=`e5143a84416821bb521ca59683999d86009d91d60ad7dbfa22820eec4272a297`；U03任务 `ART-PKG-X3-015-PDF`=`e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；现行课标 `ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填该值。
