---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U04-01-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U04-01"
artifact_version: "0.2.1"
artifact_sha256: "51e4601579ab0033e14fced1a0b0edb0001789bf240378933a02b9ca7e2fe5ea"
review_round: 1
reviewer: "independent_primary_x3_u04_01_r1"
review_role: "primary"
reviewed_at: "2026-08-09T01:35:00+08:00"
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
report_sha256: "41853e55df4711ac39ec3615a1d8ffaea6e796a3a394d6807d5f095dc09b193b"
---

# CARD-X3-U04-01 v0.2.1 独立主审 R1

## 1. 输入锁定与独立性

本轮以 `CARD-X3-U04-01` v0.2.1 的独立快照复核，不修改卡片、ledger、validator 或状态迁移。重点检查三篇子文本边界、科学论著任务群定位、24个KP/23条EV、M0与教师用书缺失治理，以及上一版学业质量定位修订是否已经生效。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U04-01.md`；v0.2.1；SHA `51e4601579ab0033e14fced1a0b0edb0001789bf240378933a02b9ca7e2fe5ea`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `26e5895e32afb3ed0b925de0ec173ce3290f8b60f717c80f792402fa4155a152`；CARD-X3-U04-01 为 v0.2.1/`linted` |
| 课文 canonical | `ART-PKG-X3-016-PDF`；SHA `caf521e8179246b851d8f0ba7c63ef9edd50e8a6585bd0ea030786880e43358b`；母本物理页92—105 |
| U04任务 canonical | `ART-PKG-X3-018-PDF`；SHA `b27a8a9de0b7062a7e1031dfdf89f8ff261c7c28c00c72b7174d39c4f88b79e3`；母本物理页114—115 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群12物理页33—34、学业质量4-3物理页46 |
| validator | `VAL-20260809-011930+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `655d84576d4290d7794fd4ee3f36d137636b875d6df1d21c0af5f514e0b8a4f1` |

卡片状态、版本、上游哈希和 `reviewers: []` 一致。本报告只记录独立主审，不执行状态迁移。

## 2. 覆盖与结构复核

- `3/3` 子文本已列明：U04导语、达尔文《自然选择的证明》、萨根《宇宙的边疆》；课文物理页92—105、U04任务物理页114—115均可回链。
- `24/24` KP均有唯一ID、主维度、受控知识类型、四层归属、判定理由和有效EV；主维度仅为“人文/语言”。
- `23/23` EV均有单值 `Q/F/M/D` 类型、Source、Artifact、locator、短引、支撑关系及核验状态；任务、学习提示、正文、课标和缺源边界分层。
- 课标主任务群准确为“科学与文化论著研习”（任务群12）物理页33—34；学业质量为4-3物理页46，仅作能力定位，不判定完整水平。
- 课标物理页25—27的任务群5—6说明被明确排除，未误挂为任务群12；教师用书为 `edition_match=unknown`；高考采用 `N/A / M0 / N/A`。

## 3. Claim—Evidence 复核

《自然选择的证明》的变异、自然选择、竞争、渐进变异、例证、地理分布和特创论局限由 EV-004—010 闭合；《宇宙的边疆》的尺度推进、光年、星系、地球家园和怀疑/想象由 EV-011—014 闭合。学习提示的事实—规律—结论、文体和语言比较由 EV-015 闭合；U04任务的概念/观点/事实表、长句、提要、多媒介、读书报告和修改由 EV-016—020 闭合；课标和教师用书边界由 EV-021—023 闭合。

KP-005/007/010/015/016/017使用连续正文证据形成解释链，未把课文科学内容扩展成外部科学史或现代科学结论。KP-020将“证据校准”标明为项目边界建议，未伪装成任务原文。KP-024明确4-3仅为能力定位。未发现正文事实、EV类型、页位或来源错配。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 作品题名、作者、科学论证与科普内容均与canonical正文和学习提示一致。 |
| R02 | 否 | 23/23 EV均具适配来源、Artifact、可解析物理页/切分页、短引与核验状态；解释型KP有连续文本证据。 |
| R03 | 否 | 3个子文本、导语、学习提示、U04任务、课标、24 KP、23 EV及教学/M0/边界模块齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标、教师用书缺源和项目建议分层；无外部科学史冒充教材事实。 |
| R05 | 否 | 24/24 KP均有合法主维度、受控类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考关系保持结构化M0，未登记真题、答案或评分映射，也未越级为M1—M3。 |
| R07 | 否 | 正式主张只消费登记并核验的教材包、U04任务包和现行课标。 |
| R08 | 否 | 卡片、ledger、23 EV、24 KP、版本、路径和SHA绑定一致；validator通过。 |
| R09 | 否 | 使用现行课标任务群12规范名称和正确页位，未将任务群5—6物理页25—27误作本卡课标。 |
| R10 | 否 | 人文/语言按文本需要展开，未机械铺满核心素养，未把4-3当作单课完整等级。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 未发现影响课标定位、证据闭合、KP覆盖、M0或教师用书边界的关键缺陷。 |
| P2 | 0 | 版本记录中曾出现的4-2页位已在v0.2.1明确改为4-3；当前正文、EV和front matter均一致，本轮无需返工。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **24.5** | 23/23 EV均有来源、canonical Artifact、物理/切页、短引和verified状态；解释型KP均有相邻正文证据。 |
| 事实与术语准确性 | 20 | 18 | **19.5** | 科学论著/科普术语、任务群12、学业质量4-3和教材边界准确；当前修订已关闭旧4-2定位。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 3/3子文本、24/24 KP、23/23 EV、任务、课标、教学、M0和版本模块齐全。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线覆盖求真、探索、尺度与人的位置；语言线覆盖概念、逻辑、长句、科普表达、摘要与多媒介。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 四层归属和理由完整，M0/N/A边界无越级映射，课标定位准确。 |
| 纵向贯通 | 8 | 6 | **8.0** | 当前无同版本、双向核验的跨册KP关系，使用有理由的N/A而非臆造递进。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 教材提示、教师用书缺源和项目建议分离；概念—事实—规律—结论、长句、提要和报告任务可直接备课。 |
| **合计** | **100** | **85** | **98.5** | **总分及七维单项均达到冻结门槛；R01—R10未触发。** |

## 7. 独立主审决定

**决定：`pass`；总分 `98.5/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U04-01` v0.2.1/SHA `51e4601579ab0033e14fced1a0b0edb0001789bf240378933a02b9ca7e2fe5ea` 通过独立主审，可与同一SHA的独立第二复审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、canonical Artifact、validator或版本绑定变化时，本报告失效并须按新SHA复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U04-01.md`；v0.2.1；SHA `51e4601579ab0033e14fced1a0b0edb0001789bf240378933a02b9ca7e2fe5ea`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `26e5895e32afb3ed0b925de0ec173ce3290f8b60f717c80f792402fa4155a152`。
- validator：`work/knowledge/_meta/validation_reports/x3_u04_02_rework_validation_20260809.json`；run `VAL-20260809-011930+0800`；SHA `655d84576d4290d7794fd4ee3f36d137636b875d6df1d21c0af5f514e0b8a4f1`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：课文 `ART-PKG-X3-016-PDF`=`caf521e8179246b851d8f0ba7c63ef9edd50e8a6585bd0ea030786880e43358b`；U04任务 `ART-PKG-X3-018-PDF`=`b27a8a9de0b7062a7e1031dfdf89f8ff261c7c28c00c72b7174d39c4f88b79e3`；现行课标 `ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对canonical报告字节求SHA-256，再回填该值。
