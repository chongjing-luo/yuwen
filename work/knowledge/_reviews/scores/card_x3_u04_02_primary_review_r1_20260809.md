---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U04-02-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U04-02"
artifact_version: "0.2.1"
artifact_sha256: "fa8b52811e99beb4903c1c68f1ed5a34e6df7ec0dab7efbb439dc2bac15aaf58"
review_round: 1
reviewer: "independent_primary_x3_u04_02_r1"
review_role: "primary"
reviewed_at: "2026-08-09T01:25:00+08:00"
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
report_sha256: "f80c91d12527373b5c23dec7bf9f07f6eda5d8fbad9cfd10bca3911efc0ea2f1"
---

# CARD-X3-U04-02 v0.2.1 独立主审 R1

## 1. 输入锁定与独立性

本轮只审 `CARD-X3-U04-02` 当前 v0.2.1 快照，不能替代对 U04-01 的审查，也不复用未绑定版本的旧分数或结论。依据为当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、课文和 U04 单元研习任务 canonical PDF、现行课标、共享 ledger 及指定 validator；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U04-02.md`；v0.2.1；SHA `fa8b52811e99beb4903c1c68f1ed5a34e6df7ec0dab7efbb439dc2bac15aaf58`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `26e5895e32afb3ed0b925de0ec173ce3290f8b60f717c80f792402fa4155a152`；CARD-X3-U04-02 为 v0.2.1/`linted`，含完整 REWORK `post_sha256` |
| 课文 canonical | `ART-PKG-X3-017-PDF`；SHA `c255f8ef560113f68ef2ada826c4f43ce05b07447c80a9105befd5b05d43f4e1`；母本物理页106—113，切分 PDF 第1—8页；学习提示在物理页113/切分页8 |
| U04任务 canonical | `ART-PKG-X3-018-PDF`；SHA `b27a8a9de0b7062a7e1031dfdf89f8ff261c7c28c00c72b7174d39c4f88b79e3`；母本物理页114—115，切分 PDF 第1—2页 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffeae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群12物理页33—34/印刷页25—26，学业质量4-3物理页46 |
| validator | `VAL-20260809-011930+0800`；报告 `work/knowledge/_meta/validation_reports/x3_u04_02_rework_validation_20260809.json`；`passed`、0 errors、`hash_verification=true`；报告 SHA `655d84576d4290d7794fd4ee3f36d137636b875d6df1d21c0af5f514e0b8a4f1` |

卡片 front matter 与 ledger 的 ID、路径、版本、owner、source_ids 和状态一致。`reviewers: []` 保持不变，表示本报告只记录主审，不执行 DG4 或 `accepted` 状态迁移。

## 2. canonical 页位、覆盖与来源分层

- 课文 canonical PDF 的物理页106—113已逐页核对：正文覆盖“天圆地方”、宣夜说、盖天说、浑天说、太初历争论、扬雄/王充/葛洪/何承天等论辩、祖暅观测校验、政治宗教边界及历史影响；学习提示物理页113要求梳理三说基本观点、贡献、关系和发展过程，并形成科学文化判断。
- U04 任务 canonical PDF 的物理页114—115已核对：任务一要求梳理概念—观点—事实表格并分析自然科学论著长句；任务二要求写提要和制作多媒介介绍；任务三要求跨学科研习、读书报告及“吟于口、待于时、求于友”的修改过程；“文章修改”覆盖立意、材料、结构、语言。
- 课标 canonical 的任务群12物理页33—34支持研习自然科学/社会科学论文和著作、内容提要/读书笔记、概括归纳推理实证、结构与论证逻辑；物理页46的学业质量4-3只作为“依据具体内容评论表现形式、提出看法或质疑并准确表达”的能力定位，不被改写为本课完整等级。
- `30/30` KP、`28/28` EV 均有唯一 ID、合法主维度、受控知识类型、四层主归属、判定理由和证据回链；EV 类型均为单值 `Q/F/M/D`，核验状态为 `verified`。正文、学习提示、任务、课标、教师用书缺失声明和项目建议分层清楚。
- 教师用书 `edition_match=unknown`；高考栏保持结构化 `N/A / M0 / N/A`，没有消费未登记真题、答案、评分或外部天文学考证。

## 3. Claim—Evidence 独立复核

课文事实链由 EV-003—016 闭合：开篇的中西参照与浑盖之争、天圆地方及曾子解释、宣夜说的无限空间和功能局限、盖天说的模型/勾股测算/历法价值与结构错误、浑天说及太初历实际检验、扬雄的八方面批驳、王充—葛洪—何承天的水中出没论辩、诸说蜂起与朱熹仪器观点、祖暅“稽之典经……校之以仪象，覆之以晷漏”的观测—仪器校验程序，以及政治/宗教未成为学术裁决依据和结尾影响概括，均可回查 canonical 物理页106—113。

学习提示与任务主张由 EV-017—025 闭合，课标任务群及学业质量定位由 EV-026—027 闭合，EV-001/028 负责来源、教师用书与外部材料边界。复核确认复合 Claim 未把作者解释写成教材逐字事实：KP-005、007、008、012、013、016—018、020 属有文本约束的解释或价值辨析；KP-019、021—028 属学习提示/任务支撑的阅读与表达程序；KP-029—030 属课标定位。30 个 KP 的主维度、知识类型、四层归属和判定理由均与其 EV 适配，未发现错引、越页或来源职责漂移。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、关增建、三种宇宙模型、太初历、争论人物、祖暅引文、学习提示和任务内容均与 canonical 来源一致。 |
| R02 | 否 | `28/28` EV 均有适配 Source、canonical Artifact、可解析物理/切分页 locator、短引、支撑关系和 `verified` 状态；30 个 KP 的正式主张均可回链。 |
| R03 | 否 | 单一正文子文本、学习提示、U04任务、课标、30 KP、28 EV、三类教学模块、纵向和高考模块均齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标、教师用书缺失声明和项目建议分层；没有把教师用书、网络解析、外部天文学考证或 MinerU 辅助文本冒充教材事实。 |
| R05 | 否 | `30/30` KP 均具有合法主维度（人文/语言）、受控知识类型、四层主归属、判定理由和有效证据；没有孤立 KP。 |
| R06 | 否 | 高考关系严格保持 `M0/N/A`；未登记逐小问真题—答案/评分—教材 KP 双向闭合证据，未建立 M1—M3。 |
| R07 | 否 | 正式内容只消费已登记、已核验的课文包、U04任务包和现行课标 canonical Artifact；教师用书缺源没有被替代性消费。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、30 KP、28 EV、版本、路径、REWORK post-SHA 和 validator 绑定一致；validator `hash_verification=true`。 |
| R09 | 否 | 使用现行课标任务群12“科学与文化论著研习”和正确页位，学业质量统一定位4-3并明确“不判定完整水平”，未将课标改写为课型或难度。 |
| R10 | 否 | 人文/语言双线围绕科学史求真、模型比较、证据校验、概念梳理、长句、提要、多媒介和修改展开；未机械铺满核心素养或给本课贴完整学业质量等级。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键覆盖缺失、非法枚举、Claim—Evidence 断链、边界混写、版本漂移、高考越权或课标硬错。 |
| P2 | 0 | 本轮未发现影响检索、回查或备课使用的非阻断缺陷；所有已登记边界均有明确声明。 |

## 6. `2.0-textbook` 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **24.5** | `28/28` EV 均有 canonical Artifact、物理/切页、短引、支撑关系和核验状态；复合 Claim 可回查，少量跨页复合证据采用页段范围，保守扣0.5。 |
| 事实与术语准确性 | 20 | 18 | **20.0** | 三说模型、历法裁决、论辩人物、祖暅校验程序、任务群12和4-3边界均准确；未发现事实或术语错配。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | `1/1`正文子文本、`30/30` KP、`28/28` EV以及任务/课标/M0/纵向/教学模块齐全，KP覆盖文本特异内容和可操作阅读程序。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线覆盖宇宙模型竞争、观测求真、学术共同体和历史影响；语言线覆盖科学史结构、概念比较、史料引述、证据链和表达任务，课标/任务与正文边界清楚，保守扣0.5。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 每个 KP 有四层主归属及理由；课标定位、`M0/N/A`治理和禁止越级边界完整。 |
| 纵向贯通 | 8 | 6 | **8.0** | 当前没有双方 `accepted` KP/EV 可供逐边核验，按契约以有理由的 `N/A` 处理，不强造递进。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 模型—证据—局限表格、时间线、长句拆解、提要、多媒介和修改链均可直接备课；教材提示、项目建议和教师用书缺源严格分离。 |
| **合计** | **100** | **85** | **99.0** | **总分及七维均过冻结门槛；R01—R10全未触发，P0/P1/P2=0/0/0。** |

## 7. 独立主审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

`CARD-X3-U04-02` v0.2.1/SHA `fa8b52811e99beb4903c1c68f1ed5a34e6df7ec0dab7efbb439dc2bac15aaf58` 通过本轮独立主审，可与同一绑定的独立第二复审配对进入 DG4。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、canonical Artifact、validator、rubric/taxonomy 或版本绑定变化时，本报告立即失效，须按新 SHA 全量复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U04-02.md`；v0.2.1；SHA `fa8b52811e99beb4903c1c68f1ed5a34e6df7ec0dab7efbb439dc2bac15aaf58`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `26e5895e32afb3ed0b925de0ec173ce3290f8b60f717c80f792402fa4155a152`；CARD-X3-U04-02 为 `linted`/`REWORK`。
- validator：`work/knowledge/_meta/validation_reports/x3_u04_02_rework_validation_20260809.json`；运行 `VAL-20260809-011930+0800`；SHA `655d84576d4290d7794fd4ee3f36d137636b875d6df1d21c0af5f514e0b8a4f1`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：课文 `ART-PKG-X3-017-PDF`=`c255f8ef560113f68ef2ada826c4f43ce05b07447c80a9105befd5b05d43f4e1`；U04任务 `ART-PKG-X3-018-PDF`=`b27a8a9de0b7062a7e1031dfdf89f8ff261c7c28c00c72b7174d39c4f88b79e3`；现行课标 `ART-CURR-2020-PDF`=`7a187079f1fffeae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：保持该字段为空时，对 canonical 报告字节求 SHA-256，再将所得值回填；回填不改变该计算范围。
