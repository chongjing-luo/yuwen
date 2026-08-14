---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U04-01-SECONDARY-R1"
deliverable_id: "CARD-X3-U04-01"
artifact_version: "0.2.1"
artifact_sha256: "51e4601579ab0033e14fced1a0b0edb0001789bf240378933a02b9ca7e2fe5ea"
review_round: 1
reviewer: "independent_secondary_x3_u04_01_r1"
review_role: "secondary"
reviewed_at: "2026-08-09T01:24:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "26e5895e32afb3ed0b925de0ec173ce3290f8b60f717c80f792402fa4155a152"
validator_run_id: "VAL-20260809-011930+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u04_02_rework_validation_20260809.json"
validator_report_sha256: "655d84576d4290d7794fd4ee3f36d137636b875d6df1d21c0af5f514e0b8a4f1"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "fd64abfec0d0a681ebac4b3872b390ae6e4f8632fc7b653e845722fc1bb055d1"
---

# CARD-X3-U04-01 v0.2.1 独立第二复审 R1

## 1. 输入锁定与独立性

本轮独立复核当前 U04-01 v0.2.1 重工快照，不沿用旧版本分数、R/P 或决定；不审查同一执行者重建的 U04-02。依据为当前卡片、冻结 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、U04 课文与单元研习任务 canonical PDF、现行课标、共享 ledger 和指定 validator；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U04-01.md`；v0.2.1；SHA `51e4601579ab0033e14fced1a0b0edb0001789bf240378933a02b9ca7e2fe5ea`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `26e5895e32afb3ed0b925de0ec173ce3290f8b60f717c80f792402fa4155a152`；CARD-X3-U04-01 为 v0.2.1/`linted`，含 REBUILD 与 REWORK transition |
| 课文 canonical | `ART-PKG-X3-016-PDF`；SHA `caf521e8179246b851d8f0ba7c63ef9edd50e8a6585bd0ea030786880e43358b`；母本物理页92—105、切分 PDF 第1—14页 |
| U04任务 canonical | `ART-PKG-X3-018-PDF`；SHA `b27a8a9de0b7062a7e1031dfdf89f8ff261c7c28c00c72b7174d39c4f88b79e3`；母本物理页114—115、切分 PDF 第1—2页 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群12物理页33—34（印刷页25—26），学业质量4-3物理页46 |
| validator | `VAL-20260809-011930+0800`；报告 `work/knowledge/_meta/validation_reports/x3_u04_02_rework_validation_20260809.json`；`passed`、0 errors、`hash_verification=true`；报告 SHA `655d84576d4290d7794fd4ee3f36d137636b875d6df1d21c0af5f514e0b8a4f1` |

卡片 front matter、ledger 的 ID、路径、版本、owner、source_ids 和状态一致；`reviewers: []` 表明本报告只记录第二复审，不执行 DG4 状态迁移。

## 2. canonical 页位、覆盖与修订回归

- 课文切分 PDF 14 页覆盖母本物理页92—105：导语在页92；《自然选择的证明》在页93—98；《宇宙的边疆》在页99—104；学习提示在页105。三项 `SUBTEXT` 均有稳定 ID，导语未被误计为正文。
- U04 任务 PDF 两页覆盖物理页114—115（切分页1—2），卡片准确分层记录概念/观点/事实表、长句、提要、多媒介、跨学科研习和文章修改；没有把任务产出冒充正文事实。
- 课标任务群12实际为官方 PDF 物理页33—34（印刷页25—26），学业质量统一为4-3物理页46；卡片没有把物理页25—27的任务群5—6误作任务群12。质量描述只作能力定位，未判定完整水平。
- 独立复算得到 `3/3` 子文本、`24/24` KP、`23/23` EV；KP/EV ID连续且无重复。EV 类型为单值 `Q=19、F=0、M=2、D=2`（书目信息由 Q/D 的教材边界覆盖），没有 `Q/F/M/D` 混合值；主维度仅为人文/语言，知识类型仅为六枚受控类型。
- 当前有效绑定全部为4-3；版本历史中 0.2.0 的“4-2”仅是历史变更记录，0.2.1 REWORK 已明确统一为4-3，不构成当前绑定漂移。

## 3. Claim—Evidence、双维度与边界复核

人文线覆盖科学探索与求真、自然选择的变异—竞争—适应解释、宇宙尺度与人的位置、怀疑与想象、跨学科研习；语言线覆盖事实—规律—结论链、科学论证、术语关系、长句结构、渐进论证、科普空间推进、准确与通俗表达、提要/图表/读书报告。两线均回到正文、学习提示或任务 EV，没有机械铺满四项核心素养。

正文关键事实可逐项回查：导语科学探索与文章分组（EV-002—003）、达尔文变异/自然选择/物种与变种/渐进作用/例证/地理分布（EV-004—010）、萨根怀疑想象/光年/星系尺度/地球回返（EV-011—014）。学习提示 EV-015 明确事实—规律—结论、逻辑和两种文体比较；任务 EV-016—020 分别承担概念表格、长句、提要/多媒介、跨学科报告和修改；课标 EV-021/022 分别承担任务群12与质量4-3。

解释类 KP（如 KP-005、007、010、015—017）至少有两处适配文本/栏目证据；任务程序类 KP 明确标为教材任务操作，不冒充正文。教师用书保持 `edition_match=unknown`，外部科学史、网络解析和未登记真题不进入正式证据。纵向关系有理由使用 `N/A`；高考栏严格为 `N/A | M0 | N/A`，没有教材 EV 越级映射。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、作者、三子文本、达尔文与萨根正文事实、学习提示和任务内容均与 canonical 页位一致。 |
| R02 | 否 | `23/23` EV 均有适配 Source/Artifact、可解析 locator、短引和 verified 状态；需双证的解释 KP 有足够正文或栏目证据。 |
| R03 | 否 | 3个子文本、学习提示、U04任务、课标、24 KP、23 EV、三类教学提示、纵向和高考模块齐全。 |
| R04 | 否 | 导语、正文、学习提示、任务、课标、教师用书缺源与项目建议分层；历史版本的4-2只在版本记录中出现。 |
| R05 | 否 | `24/24` KP 均具合法主维度、六枚受控知识类型、四层主归属、判定理由和有效证据。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`；未登记真题、答案或评分资料不进入映射，也未把一般题型相似性升级为 M1—M3。 |
| R07 | 否 | 正式内容只消费登记、核验的 U04 课文包、任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、子文本/KP/EV 数量、版本、路径和 REWORK post-SHA 绑定一致；validator hash verification=true。 |
| R09 | 否 | 使用现行任务群12和正确物理页33—34、质量4-3页46，未改写任务群名称或把任务群/质量描述固化为课型或难度。 |
| R10 | 否 | 人文/语言双线按科学论著和科普文本实际需要展开，未机械套用四项核心素养，也未判定单卡完整学业质量水平。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键事实/证据缺失、非法枚举、边界混写、版本漂移、页位错误或高考越权。 |
| P2 | 0 | 未发现独立的非阻断性缺陷；历史4-2仅在版本记录中保留，当前4-3绑定闭合。 |

## 6. `2.0-textbook` 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **24.5** | `23/23` EV 的来源、canonical Artifact、物理/切页、短引和 verified 状态闭合；复合 Claim 均给出可回查页位。 |
| 事实与术语准确性 | 20 | 18 | **19.5** | 三篇材料范围、达尔文/萨根事实、术语关系、任务群12和质量4-3页位准确；历史4-2仅作版本记录。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | `3/3`子文本、`24/24` KP、`23/23` EV、任务/课标/M0/纵向/教学模块齐全，KP具有文本特异性。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线覆盖求真、自然选择、宇宙尺度与探索；语言线覆盖论证、科普结构、长句和成果表达。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 四层归属和理由、任务群12、质量4-3定位以及 M0/N/A 治理完整。 |
| 纵向贯通 | 8 | 6 | **8.0** | 无双方可核验的跨课 KP 关系时合法使用有理由的 `N/A`。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 教材学习提示、教师用书边界和项目建议分离；概念表、长句、提要和报告任务可直接备课。 |
| **合计** | **100** | **85** | **98.5** | **总分及七维单项达到冻结门槛；R01—R10全部未触发。** |

## 7. 独立第二复审决定

**决定：`pass`；总分 `98.5/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U04-01` v0.2.1/SHA `51e4601579ab0033e14fced1a0b0edb0001789bf240378933a02b9ca7e2fe5ea` 通过本轮独立第二复审，可与同一绑定的独立主审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、canonical Artifact、validator、ledger、rubric/taxonomy 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U04-01.md`；v0.2.1；SHA `51e4601579ab0033e14fced1a0b0edb0001789bf240378933a02b9ca7e2fe5ea`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `26e5895e32afb3ed0b925de0ec173ce3290f8b60f717c80f792402fa4155a152`；CARD-X3-U04-01 为 v0.2.1/`linted`、REWORK transition 已闭合。
- validator：`work/knowledge/_meta/validation_reports/x3_u04_02_rework_validation_20260809.json`；run `VAL-20260809-011930+0800`；SHA `655d84576d4290d7794fd4ee3f36d137636b875d6df1d21c0af5f514e0b8a4f1`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：课文 `ART-PKG-X3-016-PDF`=`caf521e8179246b851d8f0ba7c63ef9edd50e8a6585bd0ea030786880e43358b`；U04任务 `ART-PKG-X3-018-PDF`=`b27a8a9de0b7062a7e1031dfdf89f8ff261c7c28c00c72b7174d39c4f88b79e3`；现行课标 `ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填该值。
