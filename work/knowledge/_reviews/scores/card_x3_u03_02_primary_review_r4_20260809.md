---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U03-02-R4-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U03-02"
artifact_version: "0.2.5"
artifact_sha256: "eb45259d09293e4fa46a86c3665075ffbba9ee04ef5c7f0a6a45c7ad61d580c5"
review_round: 4
reviewer: "independent_primary_x3_u03_02_r4"
review_role: "primary"
reviewed_at: "2026-08-09T00:40:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "6c73ae0d81312eb2a85deb399665aa8b9e953ef17be682c18db78ecbf0c0df7c"
validator_run_id: "VAL-20260809-002353+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u03_02_rework_r5_validation_20260809.json"
validator_report_sha256: "a6ac7c8ade540b805cdb57ec220b144660b7a06e5a33b83d4107dd2aefe90c85"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "c91bdf9becec4f6c3d03e192438d0db67b772aea7d89530cdef12ab0ac1b1a4b"
---

# CARD-X3-U03-02 v0.2.5 独立主审 R4

## 1. 输入锁定与状态一致性

本轮针对 v0.2.5 新快照重新进行独立主审，仅依据当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、两篇课文及学习提示、U03 单元研习任务、现行课标、共享账本和指定 validator 报告复核；不复用 v0.2.0—v0.2.3 的分数或结论，不修改卡片、ledger、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U03-02.md`；v0.2.5；SHA `eb45259d09293e4fa46a86c3665075ffbba9ee04ef5c7f0a6a45c7ad61d580c5`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `6c73ae0d81312eb2a85deb399665aa8b9e953ef17be682c18db78ecbf0c0df7c`；CARD-X3-U03-02 为 v0.2.5/`linted`，含连续 REWORK transition 记录 |
| 课文 canonical | `ART-PKG-X3-012-PDF`；SHA `917f0c9ca10a16f08040da4c286028b70f3d7b056a51ac8d60f10c0882dcabea`；两文正文物理页80—84、学习提示物理页85 |
| U03任务 canonical | `ART-PKG-X3-015-PDF`；SHA `e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；物理页90—91 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群8物理页29—30、学业质量4-3物理页46 |
| validator | `VAL-20260809-002353+0800`；`work/knowledge/_meta/validation_reports/x3_u03_02_rework_r5_validation_20260809.json`；`passed`、0 errors、`hash_verification=true`；报告 SHA `a6ac7c8ade540b805cdb57ec220b144660b7a06e5a33b83d4107dd2aefe90c85` |

卡片 front matter 的 `status: linted`、`reviewers: []` 与 ledger 的版本和状态一致。ledger 中 v0.2.1 的 G4 已明确标记 withdrawn，之后的重工链最终闭合至 v0.2.5；历史版本不作为本轮证据或结论。

## 2. 覆盖、证据与修订复核

- 卡片覆盖 U03 课10两篇正文、学习提示、U03 单元研习任务和现行课标：`《兰亭集序》`物理页80—81/切页1—2，`《归去来兮辞并序》`物理页82—84/切页3—5，学习提示物理页85/切页6，任务物理页90—91，课标任务群8物理页29—30、学业质量4-3物理页46。
- `22/22` KP 均有唯一 ID、合法主维度（仅“人文/语言”）、冻结知识类型（事实/概念/程序/策略/解释/价值辨析）、四层主归属、判定理由、证据 ID 和置信状态；`22/22` EV 均为单值 `Q/F/M/D`（Q=18、F=1、M=2、D=1）。
- EV-002—011 覆盖两篇正文的作者、场景、处境、结构、自然意象和生命感悟；EV-012—016 只承担学习提示；EV-017—020 只承担 U03任务；EV-021—022 只承担课标任务群8与学业质量4-3；EV-001 单独承担来源/教师用书边界。来源职责分离，正式证据回到 canonical PDF。
- 逐条复核连续修订项：§8.1 不再包含任务二“归途—归舍—归园—归田—归尽”路线；该路线仅在 §8.3 标为任务二来源的项目建议；EV-014 短引已收窄为课文学习提示物理页85的实际原文；KP-014 只将路线归因于任务二，KP-016 改为“学习提示对两文的并置概括与任务二”操作化。未发现同类残留。
- 两文的“雅集—乐—痛—古今”与“序—归途—归舍—归园—归田—归尽”结构、对偶阅读、骈散/章法/评点、词类活用和书信写作均有教材或任务证据；高考栏保持 `N/A / M0 / N/A`，纵向关系保持有理由的 `N/A`，教师用书 `edition_match=unknown`。

## 3. Claim—Evidence 与边界复核

《兰亭集序》的修禊雅集、由乐入思、死生感喟、否定“一死生/齐彭殇”和古今读者收束由 EV-002—006 支撑；《归去来兮辞并序》的序辞关系、辞官缘由、归途归舍、归园归田和归尽天命态度由 EV-007—011 支撑；学习提示的生命哲理、情理交融、骈偶押韵、淡雅自然和对偶阅读由 EV-012—016 支撑；任务 EV-017—020 与课标 EV-021—022 的职责分离。

§8.1 只保留课文学习提示可直接回查的阅读方向；§8.3 另列结构路线、语言观察和当代价值讨论，并明确为本项目教学建议。KP-014 的路线来源和 KP-016 的比较操作化均已按实际 Source 分层；EV-014 的短引不再把任务内容伪装成学习提示。没有发现关键事实错误、短引错页、无适配来源、非法枚举或教材/项目/课标边界混写。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | 两文题名、作者、文体、正文事实、学习提示、U03任务和课标术语与绑定 canonical 载体一致；未发现关键事实错误。 |
| R02 | 否 | `22/22` EV 均绑定已登记 Source、canonical Artifact、可解析 locator、适配短引和 `verified` 状态；EV-014 已收窄为物理页85实际原文，任务路线由 EV-018 独立承载。 |
| R03 | 否 | 两个正文子文本、学习提示、U03任务、课标、22个KP、教学模块、M0和纵向N/A齐全，无合编文本漏项。 |
| R04 | 否 | v0.2.5 已将教材学习提示、任务事实、课标映射、教师用书缺失声明和项目建议分层；§8.1 不承载任务二路线或项目化观察清单。 |
| R05 | 否 | `22/22` KP 均具备合法主维度、受控知识类型、四层归属、判定理由、有效证据和置信状态。 |
| R06 | 否 | 高考栏保持结构化 `M0/N/A`，未引用未登记真题、答案或评分资料，也未声称 M1—M3 直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课文包、U03任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、22 KP、22 EV、版本、路径、post-SHA 和 validator 绑定一致；`hash_verification=true`。 |
| R09 | 否 | 使用现行课标任务群8“中华传统文化经典研习”和物理页29—30，未改写任务群名称或把任务群当固定课型/教法。 |
| R10 | 否 | 人文/语言双线按古代散文、文体语言、文化观念和表达活动展开，未机械铺满四项核心素养，也未把学业质量4-3当作单课等级或题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键事实错误、证据断链、教材/项目边界混写、非法枚举、版本漂移或高考越权。 |
| P2 | 0 | v0.2.0—v0.2.4 发现的来源粒度和边界问题均已在 v0.2.5 修复；当前无开放的非阻断缺陷。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 复核依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | `22/22` EV 均有 canonical Source/Artifact、物理/切页、适配短引、支撑关系和核验元数据；EV-014已与任务路线分离。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两文事实、古代散文术语、任务群8、学业质量4-3和教材/项目边界均准确。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2/2正文子文本、22/22 KP、22/22 EV、学习提示/任务/课标/M0/N/A模块齐全。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文与语言双线覆盖雅集生命意识、出仕归隐、序辞文体、对偶、章法、自然意象和真实表达；开放解释保留文本边界。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 各 KP 的四层主归属及理由、课标任务群8、学业质量4-3定位和 M0 边界均合规。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前无双方 accepted 目标时合法使用有理由的 N/A，不虚造递进关系。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | §8.1/§8.3分层清晰，结构线、评点和书信任务可直接用于备课；来源修订项已闭合。 |
| **合计** | **100** | **85** | **98.0** | **总分与七维单项均达到冻结 rubric 门槛。** |

## 7. 主审决定

**决定：`pass`；总分 `98.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U03-02` v0.2.5 / SHA `eb45259d09293e4fa46a86c3665075ffbba9ee04ef5c7f0a6a45c7ad61d580c5` 通过本轮独立主审，可与同一 SHA 的独立第二复审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、canonical Artifact 或 validator 绑定变化时，本报告失效并须按新 SHA 从头复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U03-02.md`；v0.2.5；SHA `eb45259d09293e4fa46a86c3665075ffbba9ee04ef5c7f0a6a45c7ad61d580c5`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `6c73ae0d81312eb2a85deb399665aa8b9e953ef17be682c18db78ecbf0c0df7c`；CARD-X3-U03-02 为 `linted`/`REWORK`。
- validator：`work/knowledge/_meta/validation_reports/x3_u03_02_rework_r5_validation_20260809.json`；运行 `VAL-20260809-002353+0800`；SHA `a6ac7c8ade540b805cdb57ec220b144660b7a06e5a33b83d4107dd2aefe90c85`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-012-PDF`=`917f0c9ca10a16f08040da4c286028b70f3d7b056a51ac8d60f10c0882dcabea`；`ART-PKG-X3-015-PDF`=`e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填该值。
