---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-U04-02-R2-SECONDARY-FINAL"
deliverable_id: "CARD-X2-U04-02"
artifact_version: "0.3.0"
artifact_sha256: "5680a0b3b9080be9d2ea0ac573ecb331d2ee7a05baf7f6f72a77a34fb4cf31b7"
review_round: 2
reviewer: "independent_secondary_x2_u04_02_final_r2"
review_role: "secondary"
reviewed_at: "2026-08-08T19:55:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-194012+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6"
validator_archive_sha256: "07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6"
ledger_sha256: "82778a8a230aa5e662c6c2bce6ab368448c14eb67c8ccfd6765f965587acb321"
validator_result: "passed"
decision: "pass"
---

# CARD-X2-U04-02 v0.3.0 独立第二复审 R2

## 1. 输入锁定与独立性

本轮只依据当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、来源与 Artifact 注册表、canonical 学生教材/任务/课标载体、共享账本和 validator 机械报告独立复核；未读取或复用主审报告、主审分数或主审缺陷结论，也未修改卡片、账本、deliverable 或状态。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修中册/cards/CARD-X2-U04-02.md`；v0.3.0；SHA `5680a0b3b9080be9d2ea0ac573ecb331d2ee7a05baf7f6f72a77a34fb4cf31b7`；状态 `linted` |
| 课13正文/学习提示 Artifact | `ART-PKG-X2-016-PDF`；7页；SHA `3e000c3958b8ee35f567a05abe700d134bd64d53b1ab2224be6e7517ccc98d59`；canonical 物理页122—128，切分页1—7 |
| U04导语/任务 Artifact | `ART-PKG-X2-015-PDF`；16页；SHA `388cd404624d7ee079316dc15273e383409eb738aee523e8bee70adc681cd0bd`；导语物理页106；`ART-PKG-X2-017-PDF`；2页；SHA `b3a30d48ce56c2de0f52cfcfc3eb55c938afc080148cc3329302154457735c48`；任务物理页129—130 |
| 课标 Artifact | `ART-CURR-2020-PDF`；66页；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| validator | `VAL-20260808-194012+0800`；`passed`；0 errors；`hash_verification=true` |

独立计数为 4/4 正文子文本、16/16 KP、23/23 EV；EV 类型为 Q=17、F=4、M=1、D=1。四首诗、学习提示、U04 导语、单元任务和课标边界分开登记；新增 EV-020—023 提供《迷娘》《致大海》《自己之歌》正文独立 Q 节点，解释型 KP-003、KP-006、KP-007、KP-011 均达到独立双证。

## 2. 内容、证据与边界复核

- 四个正文子文本完整覆盖《迷娘》（之一）、《致大海》、《自己之歌》（节选）和《树和天空》；学习提示、U04 单元任务和现行课标不伪装成正文。
- 23/23 EV 的 Source、canonical Artifact、物理页/切分页和短引均可解析。EV-003 已回链 U04 导语 X2-015 物理页106；EV-004、006—008、011—013 回链课13学习提示 X2-016 物理页128；EV-009、014—017 回链任务包 X2-017 物理页129—130；正文 EV-020—023 的页码与诗句逐项命中。
- 16/16 KP 具有主维度、受控知识类型、四层主归属、判定理由、有效证据和置信状态。解释型 KP-003 由《迷娘》正文反复呼告/学习提示构成双证；KP-006 由《致大海》正文形象与学习提示象征定位构成双证；KP-007 由正文情绪—历史—结尾节点与学习提示构成双证；KP-011 由《自己之歌》正文铺陈、学习提示和任务形式定位构成双证。
- 课标任务群11及学业质量使用现行 2020 修订版；EV-018 使用物理页44/印刷页36 QD-2-3 的逐字引文，仅作能力定位，不判定完整水平。
- 高考栏保持 `M0`，纵向栏保持有理由的 `N/A`，教师用书 `edition_match=unknown` 且未消费缺源意见。

## 3. R01—R10 与 P0/P1/P2

| 代码 | 触发 | 独立结论 |
|---|---|---|
| R01 | 否 | 四首诗题名、作者、诗句、学习提示事实、任务要求和引文均与 canonical 载体一致。 |
| R02 | 否 | 23/23 EV 均有适配 Source/Artifact、可解析 locator 和逐字短引；四个解释型 KP 均有至少两处独立正文/栏目/任务证据，课标 QD 引文可定位。 |
| R03 | 否 | 4 个正文子文本、学习提示、U04 任务、课标、M0、纵向 N/A 与教师用书边界模块齐全，无合编漏项。 |
| R04 | 否 | 诗歌正文、学习提示、任务包、课标和项目建议分层；开放意象只作为教材列出的可能主题，不冒充唯一答案。 |
| R05 | 否 | 16/16 KP 具备主维度、知识类型、四层归属、映射理由和有效 EV；正文与任务双证均有稳定回链。 |
| R06 | 否 | 未登记真题；高考栏仅保留结构化 `M0`，不作直接衔接。 |
| R07 | 否 | 仅消费已核验学生教材包、U04 导语/任务包和现行课标，未使用未验收上游。 |
| R08 | 否 | 卡片 v0.3.0、4 subtexts、16 KP、23 EV、跨源页码、Source/Artifact、M0/N/A 和当前 SHA/ledger 绑定闭合。 |
| R09 | 否 | 使用“外国作家作品研习”及现行 2020 修订课标，未改写任务群名称或将其当固定课型。 |
| R10 | 否 | 人文/语言双线按诗歌文本需要展开，未机械铺满四项核心素养，也未把学业质量当作单课难度标签。 |

P0/P1/P2：`0/0/0`。

## 4. 2.0-textbook knowledge_card 量规评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **25.0** | 23/23 EV 的来源、Artifact、页码/切分页和短引闭合；课13四首诗、学习提示、导语、任务和课标均有回链。 |
| 事实与术语准确性 | 20 | 18 | **20.0** | 作者、诗作、放逐背景、体式/节奏、任务群11和 QD-2-3 均准确，事实与研究解释边界清晰。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 4 subtexts、16 KP、四诗学习提示、任务二/三、课标、教师用书/M0/N/A 模块完整；正文节点可检索。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 文化多样性、自由/主体、人与自然与意象、象征、节奏、改写双线并置；开放解读和学生表达边界明确。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 每个 KP 有层级和理由；课标定位及 M0 不越级，未伪造真题证据。 |
| 纵向贯通 | 8 | 6 | **7.0** | 在无双方 accepted 且逐边可核验目标时保持带理由 N/A，避免强造关系。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 朗读、意象图谱、形式比较、诗歌改写和申论成果均可操作；教师用书缺源、开放主题和 M0 边界明确。 |
| **合计** | **100** | **85** | **98.5** | 各维度均达到门槛。 |

## 5. 独立第二复审决定

**决定：`pass`。** 当前 `CARD-X2-U04-02` v0.3.0/SHA `5680a0b3b9080be9d2ea0ac573ecb331d2ee7a05baf7f6f72a77a34fb4cf31b7` 可与同 SHA 的另一份评审配对进入后续 G4。卡片、canonical Artifact、validator、账本或版本绑定发生任何变化，均使本报告失效并需重新复审。

## 6. 可复现绑定

- latest validator：`VAL-20260808-194012+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6`；归档运行报告 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-194012+0800.json` SHA `07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6`。
- ledger/deliverables binding：`work/knowledge/_meta/deliverables.jsonl` SHA `82778a8a230aa5e662c6c2bce6ab368448c14eb67c8ccfd6765f965587acb321`；当前 ledger 记录的卡片状态仍为 `linted`，本报告不执行状态迁移。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
