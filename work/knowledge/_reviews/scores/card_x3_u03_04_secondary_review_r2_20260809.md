---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U03-04-SECONDARY-R2"
deliverable_id: "CARD-X3-U03-04"
artifact_version: "0.2.1"
artifact_sha256: "5c2d645511d28566f36ae378c1e6b0b90cbc9274fe39dc7b8878d4cfb7ff6e2c"
review_round: 2
reviewer: "independent_secondary_x3_u03_04_r2"
review_role: "secondary"
reviewed_at: "2026-08-09T05:10:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "b5852a2f1d60f242cfbed8926a80c06ff43505d53045b552e207442cda4c01f6"
validator_run_id: "VAL-20260809-005005+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u03_04_rework_validation_20260809.json"
validator_report_sha256: "21200720d7870ee0a0bff852e19a9afcb8e59edd6367f41db20e348c988e566e"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "92ef47ccdbd8121313695b6c31148eda95782419279d1bb94302bb26600081ea"
---

# CARD-X3-U03-04 v0.2.1 独立第二复审 R2

## 1. 输入锁定与独立性

本轮基于 v0.2.1 重工快照独立复核，重点检查教材学习提示/项目建议分层、KP-015、EV-015、证据类型、M0/N/A 和教师用书边界；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U03-04.md`；v0.2.1；SHA `5c2d645511d28566f36ae378c1e6b0b90cbc9274fe39dc7b8878d4cfb7ff6e2c`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `b5852a2f1d60f242cfbed8926a80c06ff43505d53045b552e207442cda4c01f6`；CARD-X3-U03-04 为 v0.2.1/`linted`，含 `REWORK linted→linted` 记录 |
| 课文 canonical | `ART-PKG-X3-014-PDF`；SHA `826744528e58ad0703801ae2f50dc73bf169d0ba57bdf7099e4eabd4ab988964`；正文物理页88—89、学习提示物理页89 |
| U03任务 canonical | `ART-PKG-X3-015-PDF`；SHA `e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；物理页90—91 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群8物理页29—30、学业质量4-3物理页46 |
| validator | `VAL-20260809-005005+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `21200720d7870ee0a0bff852e19a9afcb8e59edd6367f41db20e348c988e566e` |

卡片 `status: linted`、`reviewers: []` 与版本记录和 ledger 一致。本报告只记录第二复审，不执行状态迁移。

## 2. 修订回归核验

- §8.1 已严格回到 EV-008—010 的教材学习提示：游记缘由、见闻、感想、求真辨伪、目见耳闻、绘声文字、情趣理趣和诵读体会；证据链表、拟声/典故观察和现代类比已移至 §8.3 并明确为项目建议。
- KP-015 已收窄为以质疑旧说、亲身探访、目见耳闻讨论历史语境与求真态度；“现代延伸”只在判定理由中标为项目建议，不再写成任务一的教材硬要求。
- EV-015 已补全课标任务群8的“阅读作品应写出内容提要和阅读感受”“撰写评论”短引，KP-018 的课标 Claim 闭合；类型仍为单值 `M`。
- 全表 EV 类型复核为单值 `Q/F/M/D`；M0 表保持 `N/A | M0 | N/A`，纵向关系为有理由的 `N/A`；教师用书 `edition_match=unknown`，外部地质考证未进入正式教材证据。

覆盖复核：`1/1` 子文本、`18/18` KP、`17/17` EV 均有唯一 ID、合法主维度、受控知识类型、四层主归属、判定理由和证据回链；正文物理页88—89、学习提示89、任务90—91和课标页位正确。

## 3. Claim—Evidence 复核

《石钟山记》的旧说与疑问、寺僧扣石、父子夜泊、鸟鸣浪涌、噌吰/窾坎镗鞳声源、周景王/魏庄子典故及“目见耳闻不可臆断”由 EV-002—007 闭合；学习提示由 EV-008—010 闭合；任务与课标由 EV-011—016 闭合。KP-015 的正式主张与任务一和课文求真证据相适配，EV-015 的短引覆盖 KP-018 全部课标子主张。

本轮未发现事实错误、证据粒度不足、Q/F/M/D混用、教材/项目建议边界混写、M0越级或教师用书误引。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、作者、出游事实、声音描写、前人说法、求真结论、学习提示和课标术语均与 canonical 来源一致。 |
| R02 | 否 | 17/17 EV 均有适配 Source、Artifact、可解析 locator、短引和 `verified` 状态；EV-015已闭合KP-018课标主张。 |
| R03 | 否 | 1个正文子文本、学习提示、U03任务、课标、18个KP、17条EV、教学/M0/纵向模块齐全。 |
| R04 | 否 | 教材学习提示、任务、课标、教师用书缺源和项目建议已分层；§8.1无项目化证据链或现代延伸。 |
| R05 | 否 | 18/18 KP 均有合法主维度、受控知识类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，没有未登记真题、答案或评分资料或越级映射。 |
| R07 | 否 | 正式内容仅消费登记并核验的课文、任务和现行课标 Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、18 KP、17 EV、版本、路径和 SHA 绑定一致；REWORK记录闭合。 |
| R09 | 否 | 使用现行课标任务群8和学业质量4-3定位，未改写任务群名称或把质量描述当课型/难度。 |
| R10 | 否 | 人文/语言双线按文本需要展开，未机械铺满核心素养，未把学业质量4-3当作单课完整等级。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 教材提示/项目建议分层、KP-015边界和EV-015短引均已修复；无关键事实或版本硬错。 |
| P2 | 0 | 本轮未发现独立的非阻断性缺陷；修订项逐一闭合。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **25.0** | 17/17 EV 的来源、canonical Artifact、物理/切页、短引和状态闭合；EV-015完整覆盖课标 Claim。 |
| 事实与术语准确性 | 20 | 18 | **19.5** | 正文旧说、夜游、声音、典故、求真辨伪、游记/绘声术语和课标定位准确。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 1/1子文本、18/18 KP、17/17 EV、任务/课标/M0/纵向/教学模块齐全。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线覆盖质疑旧说、亲身探访、目见耳闻和求实；语言线覆盖游记结构、绘声、典故、情趣理趣和评点。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 四层主归属、理由、任务群8、学业质量4-3和M0/N/A边界完整。 |
| 纵向贯通 | 8 | 6 | **8.0** | 无双方可核验纵向KP关系时合法使用有理由的N/A。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 教材提示、教师用书边界和项目建议分离；证据链表、绘声评点、求真讨论可直接备课。 |
| **合计** | **100** | **85** | **99.0** | **总分及七维单项达到冻结门槛；R01—R10全部未触发。** |

## 7. 独立第二复审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U03-04` v0.2.1/SHA `5c2d645511d28566f36ae378c1e6b0b90cbc9274fe39dc7b8878d4cfb7ff6e2c` 通过本轮独立第二复审，可与同一 SHA 的独立主审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、canonical Artifact、validator、ledger 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U03-04.md`；v0.2.1；SHA `5c2d645511d28566f36ae378c1e6b0b90cbc9274fe39dc7b8878d4cfb7ff6e2c`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `b5852a2f1d60f242cfbed8926a80c06ff43505d53045b552e207442cda4c01f6`。
- validator：`work/knowledge/_meta/validation_reports/x3_u03_04_rework_validation_20260809.json`；run `VAL-20260809-005005+0800`；SHA `21200720d7870ee0a0bff852e19a9afcb8e59edd6367f41db20e348c988e566e`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：课文 `ART-PKG-X3-014-PDF`=`826744528e58ad0703801ae2f50dc73bf169d0ba57bdf7099e4eabd4ab988964`；U03任务 `ART-PKG-X3-015-PDF`=`e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；现行课标 `ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填该值。
