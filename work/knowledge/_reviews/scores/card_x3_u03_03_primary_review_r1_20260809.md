---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U03-03-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U03-03"
artifact_version: "0.2.0"
artifact_sha256: "ef8f093069f82d20a76f4bbe37ae83fa97230c7145b8116e493068a9839ab4af"
review_round: 1
reviewer: "independent_primary_x3_u03_03_r1"
review_role: "primary"
reviewed_at: "2026-08-09T00:20:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "fa02ca45bb9ad1313963d12687a34c9b64df722eb09d9361e95b9ab78a34fd56"
validator_run_id: "VAL-20260809-000644+0800"
validator_report: "work/knowledge/_meta/validation_reports/post_receipt_validation_20260809.json"
validator_report_sha256: "c1e252ab893264459d6d36f747fafd5d44ad3ad4443c51f4d3bdb5bf24614943"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "60898758c85f71970f6ff43cb898c70544476a13218a332ce9af646d7248d897"
---

# CARD-X3-U03-03 v0.2.0 独立主审 R1

## 1. 输入锁定与独立性

本轮仅依据当前卡片、登记的 canonical Artifact、U03 单元研习任务、现行课标、冻结 `2.0-textbook` rubric/taxonomy、共享 ledger 和 validator 归档报告独立复核；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U03-03.md`；v0.2.0；SHA `ef8f093069f82d20a76f4bbe37ae83fa97230c7145b8116e493068a9839ab4af`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `fa02ca45bb9ad1313963d12687a34c9b64df722eb09d9361e95b9ab78a34fd56`；CARD-X3-U03-03 为 v0.2.0/`linted`，含 `REBUILD drafted→linted` 记录 |
| 课文 canonical | `ART-PKG-X3-013-PDF`；SHA `e5143a84416821bb521ca59683999d86009d91d60ad7dbfa22820eec4272a297`；正文物理页86—87、学习提示物理页87（切分页1—2） |
| U03任务 canonical | `ART-PKG-X3-015-PDF`；SHA `e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；物理页90—91（切分页1—2） |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群8物理页29—30、学业质量4-3物理页46 |
| validator | `VAL-20260809-000644+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `c1e252ab893264459d6d36f747fafd5d44ad3ad4443c51f4d3bdb5bf24614943` |

卡片 `status: linted`、`reviewers: []`、正文尚未完成评审的状态说明与 ledger 一致。本报告只记录主审，不执行状态迁移。

## 2. 覆盖、事实与证据回链

- `1/1` 正文子文本、`18/18` KP、`18/18` EV 均有唯一稳定 ID、合法主维度（“人文/语言”）、受控知识类型、四层主归属、判定理由、证据 ID 和核验状态；EV 类型为单值 `Q/F/M/D`。
- canonical 页位独立复算：正文物理页86—87/切页1—2，学习提示物理页87/切页2；U03任务物理页90—91/切页1—2；课标任务群8物理页29—30，学业质量4-3物理页46。
- 正文证据闭合人物外貌与命名、种树职业和成果、“顺木之天”原则、郭橐驼与他植者的正反对照、烦令扰民、养人术与官戒；学习提示证据闭合传记结构、叙事说理、对举类比、现实针对性和人称代词梳理。任务与课标证据职责分层，无外部解析或教师用书内容混入。
- 高考栏严格保持 `N/A / M0 / N/A`，纵向关系保持有理由的 `N/A`；教师用书为透明的 `edition_match=unknown`，未登记真题、答案/评分资料不进入正式映射。

## 3. Claim—Evidence 复核与风险判断

《种树郭橐驼传》正文与学习提示的关键事实均可回查：郭橐驼“病偻”而得名、以种树为业（物理页86）；“顺木之天”及根培土筑操作、他植者过少或过多的照料（物理页86）；“木之性日以离”“虽曰爱之，其实害之”（物理页86—87）；“移之官理”、烦令扰民和“传其事以为官戒”（物理页87）。

KP-012 的三类人称代词直接来自学习提示，卡片明确要求结合语境判断指代；KP-015、KP-016 与 U03 任务的评点、词类活用梳理职责相符；KP-017 的书信表达由任务四及“说真话，抒真情”栏目支撑。KP-018 对任务群8和学业质量4-3作定位并明确不判定完整水平。未发现事实错误、证据断链、教材/项目建议混写或高考越级。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、作者、人物、种树操作、官理寓意、学习提示术语和课标术语均与 canonical 来源一致。 |
| R02 | 否 | 18/18 EV 均有适配 Source、Artifact、可解析 locator、短引和 `verified` 状态；需证的 KP 均有正文、提示、任务或课标来源。 |
| R03 | 否 | 1个正文子文本、学习提示、U03任务、课标、18个KP、18条EV、教学/M0/纵向模块齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标 M、教师用书缺源声明和项目建议分层清楚；未将研究性概括冒充规范来源结论。 |
| R05 | 否 | 18/18 KP 均有合法主维度、受控知识类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，没有未登记真题、答案或评分资料，也未声称 M1—M3 直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课文、U03任务和现行课标 Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、18 KP、18 EV、版本、路径和 SHA 绑定一致；状态仍为 `linted`。 |
| R09 | 否 | 使用现行课标任务群8“中华传统文化经典研习”和学业质量4-3定位，未改写任务群名称或把质量描述当课型/难度。 |
| R10 | 否 | 人文/语言双线按文本需要展开，未机械铺满核心素养，未把学业质量4-3当作单课完整等级。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键事实错误、关键证据缺失、非法枚举、边界混写、版本漂移或高考越权。 |
| P2 | 0 | 未发现独立的非阻断性缺陷；代表性短引均有正确 locator 和适配主张，项目建议已明确标注。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **24.5** | 18/18 EV 的来源、canonical Artifact、物理/切页、短引和状态闭合；复合 Claim 均可回查。 |
| 事实与术语准确性 | 20 | 18 | **19.5** | 正文人物、种树原则、官理讽喻、传记/叙事说理、人称代词和课标术语准确。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 1/1子文本、18/18 KP、18/18 EV、任务/课标/M0/纵向及教学模块齐全。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线覆盖顺应天性、以爱为害、烦令扰民和官戒；语言线覆盖叙事说理、对举类比、婉讽和代词梳理。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 四层主归属、理由、任务群8、学业质量4-3和M0/N/A边界完整。 |
| 纵向贯通 | 8 | 6 | **8.0** | 当前无双方可核验的纵向 KP 关系，合法使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 教材提示、教师用书边界和项目建议分离；结构链、评点、代词梳理和文化讨论可直接备课。 |
| **合计** | **100** | **85** | **98.5** | **总分及七维单项达到冻结门槛；R01—R10全部未触发。** |

## 7. 独立主审决定

**决定：`pass`；总分 `98.5/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U03-03` v0.2.0/SHA `ef8f093069f82d20a76f4bbe37ae83fa97230c7145b8116e493068a9839ab4af` 通过本轮独立主审，可与同一 SHA 的独立第二复审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、canonical Artifact、validator、ledger 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U03-03.md`；v0.2.0；SHA `ef8f093069f82d20a76f4bbe37ae83fa97230c7145b8116e493068a9839ab4af`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `fa02ca45bb9ad1313963d12687a34c9b64df722eb09d9361e95b9ab78a34fd56`。
- validator：`work/knowledge/_meta/validation_reports/post_receipt_validation_20260809.json`；run `VAL-20260809-000644+0800`；SHA `c1e252ab893264459d6d36f747fafd5d44ad3ad4443c51f4d3bdb5bf24614943`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：课文 `ART-PKG-X3-013-PDF`=`e5143a84416821bb521ca59683999d86009d91d60ad7dbfa22820eec4272a297`；U03任务 `ART-PKG-X3-015-PDF`=`e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；现行课标 `ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填该值。
