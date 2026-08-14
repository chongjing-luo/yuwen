---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U03-04-R2-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U03-04"
artifact_version: "0.2.1"
artifact_sha256: "5c2d645511d28566f36ae378c1e6b0b90cbc9274fe39dc7b8878d4cfb7ff6e2c"
review_round: 2
reviewer: "independent_primary_x3_u03_04_r2"
review_role: "primary"
reviewed_at: "2026-08-09T00:55:00+08:00"
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
report_sha256: "703bdaa2952b9c25ba3f53f84e43198bd3d040d5f21b9ac022966c408a884ea5"
---

# CARD-X3-U03-04 v0.2.1 独立主审 R2

## 1. 输入锁定与独立性

本轮从 v0.2.1 新 SHA 重新完整复核，不沿用 v0.2.0 的分数、R/P 或决定。依据为当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、课文与 U03 单元研习任务 canonical PDF、现行课标、共享 ledger 和指定 validator；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U03-04.md`；v0.2.1；SHA `5c2d645511d28566f36ae378c1e6b0b90cbc9274fe39dc7b8878d4cfb7ff6e2c`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `b5852a2f1d60f242cfbed8926a80c06ff43505d53045b552e207442cda4c01f6`；CARD-X3-U03-04 为 v0.2.1/`linted`，REWORK transition 已有完整 `post_sha256` |
| 课文 canonical | `ART-PKG-X3-014-PDF`；SHA `826744528e58ad0703801ae2f50dc73bf169d0ba57bdf7099e4eabd4ab988964`；母本物理页88—89，切分 PDF 第1—2页 |
| U03任务 canonical | `ART-PKG-X3-015-PDF`；SHA `e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；母本物理页90—91，切分 PDF 第1—2页 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群8物理页29—30，学业质量4-3物理页46 |
| validator | `VAL-20260809-005005+0800`；`work/knowledge/_meta/validation_reports/x3_u03_04_rework_validation_20260809.json`；`passed`、0 errors、`hash_verification=true`；报告 SHA `21200720d7870ee0a0bff852e19a9afcb8e59edd6367f41db20e348c988e566e` |

卡片 front matter 与 ledger 的 ID、路径、版本、owner、source_ids 和状态一致；`reviewers: []` 仍表示本报告只记录审查，不执行 DG4 状态迁移。

## 2. canonical 页位、修订回归与覆盖

- 课文 PDF 两页均已核对：第1页为标题、作者、题下注、旧说/疑问、送子湖口、寺僧扣石和夜游起段（母本物理页88、印刷页83）；第2页为声源判断、周景王/魏庄子典故、结论和完整学习提示（母本物理页89、印刷页84）。水印不改变正文和栏目事实，正式证据仍回到 canonical PDF。
- U03 任务 PDF 两页均已核对：物理页90—91（印刷页85—86）覆盖文化观念讨论、骈散/章法/评点、词类活用和书信写作；课文包、任务包职责没有混写。
- 课标 canonical 物理页29—30（印刷页21—22）确认任务群8目标、内容提要/阅读感受/评论和教学提示；物理页46（印刷页38）确认学业质量4-3，只作能力定位。
- `18/18` KP 与 `17/17` EV 均有稳定 ID、受控枚举、判定理由和证据回链；EV 类型为单值 `Q/F/M/D`。正文、学习提示、任务、课标及教师用书缺失边界均已分层。
- v0.2.1 回归探针通过：项目化“旧说—疑问—出游—实地观察—声源判断—求真结论”及语言观察只出现在 §8.3，并明确为项目建议；§8.1 只保留 EV-008—010 的教材学习提示；KP-015 收窄为文本求真态度与历史语境，现代延伸标为项目建议；EV-015 已包含课标“内容提要和阅读感受”。

## 3. Claim—Evidence 独立复核

正文关键事实均可在 canonical 页位逐项回查：旧说与“余尤疑之”（EV-003）、送子和寺僧扣石及夜泊绝壁（EV-004）、栖鹘/鹳鹤/噌吰的听觉场景（EV-005）、石穴与中流大石声源（EV-006）、典故和“事不目见耳闻，而臆断其有无”（EV-007）。学习提示 EV-008—010 准确覆盖游记缘由—见闻—感想、绘声文字、求真辨伪、情趣理趣、格局和诵读。任务 EV-011—014 与课标 EV-015—016 分别承担任务群和课程标准定位；EV-017 明确教师用书未登记及外部解释边界。

18 个 KP 的主维度、知识类型、四层主归属、理由与证据均相互适配。KP-005/009—014 的结构、绘声、典故、情趣理趣和评点程序属于有证据约束的文本解释/操作化；KP-015—018 的任务与课标陈述未冒充正文事实。复合 Claim 使用代表性短引并给出 canonical 物理页和切分页，未发现错引、越页或来源职责漂移。纵向关系合法保留有理由的 `N/A`；高考栏严格保持 `M0/N/A`，未引用未登记真题、答案或评分资料。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、苏轼作者、元丰七年出游事实、旧说、夜游声源、典故、结尾判断和学习提示均与 canonical 一致。 |
| R02 | 否 | `17/17` EV 均有适配 Source、canonical Artifact、可解析 locator、短引和 `verified` 状态；正文与提示的解释主张有相应文本依据，未发现缺证的正式主张。 |
| R03 | 否 | 单一正文子文本、学习提示、U03任务、课标、18 KP、17 EV、三类教学提示、纵向和高考模块齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标、教师用书缺失声明和项目建议分层清楚；没有将外部考证、网络解析或 OCR 结果冒充规范教材结论。 |
| R05 | 否 | `18/18` KP 均具合法主维度、受控知识类型、四层主归属、判定理由和有效证据。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`；未登记真题和答案不进入映射，也未把一般题型相似性升级为 M1—M3。 |
| R07 | 否 | 正式内容只消费已登记、已核验的学生课文包、U03任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、KP/EV 数量、版本、路径、post-SHA 与 validator 绑定一致；REWORK transition 闭合。 |
| R09 | 否 | 使用现行课标任务群8“中华传统文化经典研习”和正确物理页，未改写任务群名称或将任务群固化为课型/教法。 |
| R10 | 否 | 人文/语言双线围绕求真辨伪、游记绘声、评点与语言梳理展开；未机械铺满四项核心素养，也未把学业质量4-3判作单课完整水平。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 未发现关键事实错误、关键证据缺失、非法枚举、边界混写、版本漂移或高考越权。 |
| P2 | 0 | v0.2.1 已关闭 §8.1/§8.3 边界、KP-015 现代延伸边界和 EV-015 课标短引问题；当前无开放非阻断缺陷。 |

## 6. `2.0-textbook` 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **24.5** | `17/17` EV 的来源、canonical Artifact、物理/切页、短引、支撑关系和核验状态闭合；复合 Claim 均给出可回查页位。 |
| 事实与术语准确性 | 20 | 18 | **19.5** | 题名、人物、游记事实、声音/典故解释、任务群8和学业质量4-3边界准确。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | `1/1`正文子文本、`18/18` KP、`17/17` EV、任务/课标/M0/纵向/教学模块齐全，知识点文本特异。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线覆盖质疑旧说、实地探访、目见耳闻和求实；语言线覆盖结构、绘声、典故、情趣理趣与评点。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 四层归属和理由、任务群8、学业质量定位及 M0/N/A 治理完整。 |
| 纵向贯通 | 8 | 6 | **8.0** | 当前无双方可核验的跨课 KP 关系，按契约以有理由的 `N/A` 处理。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 教材提示、教师用书边界、项目建议严格分离；证据链、声音评点、求真讨论均可直接备课。 |
| **合计** | **100** | **85** | **98.5** | **七维均过线；R01—R10 全未触发，P0/P1/P2=0/0/0。** |

## 7. 独立主审决定

**决定：`pass`；总分 `98.5/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

`CARD-X3-U03-04` v0.2.1/SHA `5c2d645511d28566f36ae378c1e6b0b90cbc9274fe39dc7b8878d4cfb7ff6e2c` 通过本轮独立主审，可与同一绑定的独立第二复审配对进入 DG4。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、canonical Artifact、validator、rubric/taxonomy 或版本绑定变化时，本报告立即失效，须按新 SHA 全量复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U03-04.md`；v0.2.1；SHA `5c2d645511d28566f36ae378c1e6b0b90cbc9274fe39dc7b8878d4cfb7ff6e2c`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `b5852a2f1d60f242cfbed8926a80c06ff43505d53045b552e207442cda4c01f6`；CARD-X3-U03-04 为 `linted`/`REWORK`。
- validator：`work/knowledge/_meta/validation_reports/x3_u03_04_rework_validation_20260809.json`；运行 `VAL-20260809-005005+0800`；SHA `21200720d7870ee0a0bff852e19a9afcb8e59edd6367f41db20e348c988e566e`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：课文 `ART-PKG-X3-014-PDF`=`826744528e58ad0703801ae2f50dc73bf169d0ba57bdf7099e4eabd4ab988964`；U03任务 `ART-PKG-X3-015-PDF`=`e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；现行课标 `ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：保持该字段为空时，对 canonical 报告字节求 SHA-256，再将所得值回填；回填不改变该计算范围。
