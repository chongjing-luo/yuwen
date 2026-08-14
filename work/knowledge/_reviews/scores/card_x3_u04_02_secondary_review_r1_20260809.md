---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U04-02-SECONDARY-R1"
deliverable_id: "CARD-X3-U04-02"
artifact_version: "0.2.1"
artifact_sha256: "fa8b52811e99beb4903c1c68f1ed5a34e6df7ec0dab7efbb439dc2bac15aaf58"
review_round: 1
reviewer: "independent_secondary_x3_u04_02_r1"
review_role: "secondary"
reviewed_at: "2026-08-09T01:27:00+08:00"
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
report_sha256: "634fb7a9ceec69598f822b2e621199e2c83256948e00f314b806901ec6329732"
---

# CARD-X3-U04-02 v0.2.1 独立第二复审 R1

## 1. 输入锁定与独立性

本轮基于当前 U04-02 v0.2.1 快照独立复核，不沿用旧版本分数、R/P 或决定；不修改卡片、ledger、validator 或状态迁移。核验对象为课14《天文学上的旷世之争》、U04 单元研习任务、现行课标、冻结 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表及指定 validator。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U04-02.md`；v0.2.1；SHA `fa8b52811e99beb4903c1c68f1ed5a34e6df7ec0dab7efbb439dc2bac15aaf58`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `26e5895e32afb3ed0b925de0ec173ce3290f8b60f717c80f792402fa4155a152`；CARD-X3-U04-02 为 v0.2.1/`linted`，REBUILD 与 REWORK transition 闭合 |
| 课文 canonical | `ART-PKG-X3-017-PDF`；SHA `c255f8ef560113f68ef2ada826c4f43ce05b07447c80a9105befd5b05d43f4e1`；母本物理页106—113、切分 PDF 第1—8页，学习提示在物理页113 |
| U04任务 canonical | `ART-PKG-X3-018-PDF`；SHA `b27a8a9de0b7062a7e1031dfdf89f8ff261c7c28c00c72b7174d39c4f88b79e3`；母本物理页114—115、切分 PDF 第1—2页 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群12物理页33—34（印刷页25—26），学业质量4-3物理页46 |
| validator | `VAL-20260809-011930+0800`；`work/knowledge/_meta/validation_reports/x3_u04_02_rework_validation_20260809.json`；`passed`、0 errors、`hash_verification=true`；报告 SHA `655d84576d4290d7794fd4ee3f36d137636b875d6df1d21c0af5f514e0b8a4f1` |

卡片 front matter 与 ledger 的 ID、路径、owner、source_ids、版本和状态一致；`reviewers: []` 保持不变，本报告不执行 DG4 或 `accepted` 状态迁移。

## 2. 覆盖、页位与枚举核验

- 课文 canonical 物理页106—113覆盖天圆地方、宣夜说、盖天说、浑天说、太初历争论、扬雄/王充/葛洪/何承天论辩、诸说蜂起、祖暅观测校验、政治宗教边界和历史影响；学习提示物理页113覆盖三说基本观点/贡献/关系及科学文化判断。
- 任务 canonical 物理页114—115覆盖概念—观点—事实表格、自然科学论著长句、约200字提要、多媒介介绍、跨学科研习、读书报告、“吟于口/待于时/求于友”和文章修改。
- 课标任务群12实际位于官方 PDF 物理页33—34（印刷页25—26）；学业质量使用4-3物理页46，仅作能力定位。卡片未误用物理页25—27的任务群5—6，且当前有效绑定无4-2。
- 独立复算：`30/30` KP、`28/28` EV，ID连续、无重复、无孤立；所有 KP 主维度仅为“人文/语言”，知识类型仅为事实、概念、程序、策略、解释、价值辨析；EV 类型均为单值 `Q/F/M/D`，且均为 `verified`。
- 正文、学习提示、任务、课标、项目建议和教师用书缺失边界分层；教师用书 `edition_match=unknown`；纵向为有理由的 `N/A`，高考保持 `N/A | M0 | N/A`，不消费未登记真题、答案、评分或外部天文学考证。

## 3. Claim—Evidence 与双维度复核

正文 EV-003—016 闭合开篇浑盖之争、天圆地方修补、宣夜无限空间与局限、盖天模型/测算/实践价值、浑天说与太初历检验、扬雄批驳、王充—葛洪—何承天论辩、诸说/朱熹、祖暅校验、政治宗教边界及历史影响。学习提示 EV-017—018、任务 EV-019—025、课标 EV-026—027、边界 EV-001/028 的来源职责清楚，短引和物理/切分页可回查。

人文线覆盖宇宙模型竞争、观测求真、学术共同体与历史影响；语言线覆盖科学史时间/因果结构、概念比较、史料引用、证据链、评价性语言、长句、表格、提要、多媒介和修订。解释/价值辨析 KP-005、007、008、012、013、016—018、020均有适配的两处或以上正文/栏目证据；任务程序 KP-019、021—028 与课标 KP-029—030 未冒充正文事实。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、关增建、三种宇宙模型、太初历、争论人物、祖暅引文、学习提示和任务内容均与 canonical 来源一致。 |
| R02 | 否 | `28/28` EV 均有适配 Source/Artifact、可解析物理/切页 locator、短引、支撑关系和 verified 状态；正式 KP 主张可回链。 |
| R03 | 否 | 1个正文子文本、学习提示、U04任务、课标、30 KP、28 EV、教学提示、纵向和高考模块齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标、项目建议和教师用书缺源分层清楚；MinerU 仅作辅助，未冒充规范事实。 |
| R05 | 否 | `30/30` KP 均有合法主维度、六枚受控类型、四层主归属、判定理由和有效证据。 |
| R06 | 否 | 高考严格保持 `M0/N/A`，无未登记真题双向证据或 M1—M3 越级。 |
| R07 | 否 | 正式内容仅消费登记、核验的课文、任务和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、KP/EV 数量、版本、路径、REWORK post-SHA 与 validator 绑定闭合。 |
| R09 | 否 | 使用现行任务群12物理页33—34和质量4-3物理页46，未改写任务群或将质量描述当课型/难度。 |
| R10 | 否 | 人文/语言双线按科学史论著实际需要展开，未机械铺满核心素养或判定本课完整学业质量等级。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键覆盖/证据缺失、非法枚举、边界混写、版本漂移、课标页位错误或高考越权。 |
| P2 | 0 | 未发现影响检索、回查或备课使用的独立非阻断缺陷。 |

## 6. `2.0-textbook` 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **24.5** | `28/28` EV 均有 canonical Artifact、物理/切页、短引、支撑关系和核验状态；少量跨页复合证据采用页段范围，保守扣0.5。 |
| 事实与术语准确性 | 20 | 18 | **20.0** | 三种模型、历法裁决、论辩人物、祖暅校验、任务群12和质量4-3边界均准确。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | `1/1`正文子文本、`30/30` KP、`28/28` EV及任务/课标/M0/纵向/教学模块齐全，KP文本特异。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线覆盖模型竞争、求真和历史影响；语言线覆盖结构、概念、史料、证据链和表达任务，保守扣0.5。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 四层主归属与理由、课标定位和 M0/N/A 治理完整。 |
| 纵向贯通 | 8 | 6 | **8.0** | 缺少双方 accepted KP/EV 时合法使用有理由的 `N/A`。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 模型—证据—局限表格、长句、提要、多媒介和修订链可直接备课，来源边界清楚。 |
| **合计** | **100** | **85** | **99.0** | **总分及七维均过冻结门槛；R01—R10全未触发。** |

## 7. 独立第二复审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U04-02` v0.2.1/SHA `fa8b52811e99beb4903c1c68f1ed5a34e6df7ec0dab7efbb439dc2bac15aaf58` 通过本轮独立第二复审，可与同一绑定的独立主审配对进入 DG4。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、canonical Artifact、validator、rubric/taxonomy 或版本绑定变化时，本报告失效并须按新 SHA 全量复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U04-02.md`；v0.2.1；SHA `fa8b52811e99beb4903c1c68f1ed5a34e6df7ec0dab7efbb439dc2bac15aaf58`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `26e5895e32afb3ed0b925de0ec173ce3290f8b60f717c80f792402fa4155a152`；CARD-X3-U04-02 为 v0.2.1/`linted`、REWORK transition 已闭合。
- validator：`work/knowledge/_meta/validation_reports/x3_u04_02_rework_validation_20260809.json`；run `VAL-20260809-011930+0800`；SHA `655d84576d4290d7794fd4ee3f36d137636b875d6df1d21c0af5f514e0b8a4f1`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：课文 `ART-PKG-X3-017-PDF`=`c255f8ef560113f68ef2ada826c4f43ce05b07447c80a9105befd5b05d43f4e1`；U04任务 `ART-PKG-X3-018-PDF`=`b27a8a9de0b7062a7e1031dfdf89f8ff261c7c28c00c72b7174d39c4f88b79e3`；现行课标 `ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填该值。
