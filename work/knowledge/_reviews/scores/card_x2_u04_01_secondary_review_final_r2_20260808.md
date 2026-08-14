---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-U04-01-R2-SECONDARY-FINAL"
deliverable_id: "CARD-X2-U04-01"
artifact_version: "0.3.0"
artifact_sha256: "f582983378a104cfda4eeecfb5ca4ebd0e59a33d28bfc32e3ecf4aed381d1281"
review_round: 2
reviewer: "independent_secondary_x2_u04_01_final_r2"
review_role: "secondary"
reviewed_at: "2026-08-08T19:48:00+08:00"
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

# CARD-X2-U04-01 v0.3.0 独立第二复审 R2

## 1. 输入锁定与独立性

本轮只依据当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、来源与 Artifact 注册表、canonical 学生教材/任务/课标载体、共享账本和 validator 机械报告独立复核；未读取或复用主审报告、主审分数或主审缺陷结论，也未修改卡片、账本、deliverable 或状态。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修中册/cards/CARD-X2-U04-01.md`；v0.3.0；SHA `f582983378a104cfda4eeecfb5ca4ebd0e59a33d28bfc32e3ecf4aed381d1281`；状态 `linted` |
| 正文/导语 Artifact | `ART-PKG-X2-015-PDF`；16页；SHA `388cd404624d7ee079316dc15273e383409eb738aee523e8bee70adc681cd0bd`；canonical 物理页106—121，切分页1—16 |
| 单元任务 Artifact | `ART-PKG-X2-017-PDF`；2页；SHA `b3a30d48ce56c2de0f52cfcfc3eb55c938afc080148cc3329302154457735c48`；canonical 物理页129—130，切分页1—2 |
| 课标 Artifact | `ART-CURR-2020-PDF`；66页；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| validator | `VAL-20260808-194012+0800`；`passed`；0 errors；`hash_verification=true` |

独立计数为 1/1 正文子文本、15/15 KP、23/23 EV；EV 类型为 Q=19、F=1、M=2、D=1。正文/导语边界为物理页106—121，任务包与课标另行登记；KP-004 的脚注补证、KP-005/006/013 的解释双证、课标 QD-2-3 exact quote 和各 Source/Artifact—locator 绑定均已逐项回看。

## 2. 内容、证据与边界复核

- 《玩偶之家》（节选）第三幕为唯一正文子文本；导语、学习提示、U04 任务和现行课标分层登记，未将项目建议或外部剧评写成教材事实。
- 15/15 KP 均具有主维度、受控知识类型、四层主归属、判定理由、有效证据和置信状态。解释型 KP-005、KP-006、KP-008、KP-013 均由至少两处相互独立的正文节点承担不同前提；KP-004 的“借款/伪造签名”由物理页107脚注 EV-023 补足，危机场面由 EV-004 支撑。
- 23/23 EV 的 Source、canonical Artifact、物理页/切分页和短引均可解析。EV-011/012 已分别收窄到实际登记的舞台提示、钥匙和关门动作；EV-020/021/022 分别补足自保逻辑、占有式“饶恕”话语和“奇迹中的奇迹”条件—剧终关门声。
- 课标任务群11及学业质量使用现行 2020 修订版；EV-018 使用物理页44/印刷页36 QD-2-3 的逐字引文，仅作能力定位，不判定完整水平。
- 高考栏保持 `M0`，纵向栏保持有理由的 `N/A`，教师用书 `edition_match=unknown` 且未消费缺源意见。

## 3. R01—R10 与 P0/P1/P2

| 代码 | 触发 | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、作者、幕次、剧情事实、娜拉/海尔茂行动及引文与 canonical 载体一致；脚注中的借款与伪造签名已单独核验。 |
| R02 | 否 | 23/23 EV 均有适配 Source/Artifact、可解析 locator 和逐字短引；解释型 KP 已达到独立双证，课标 QD 引文可定位。 |
| R03 | 否 | 单一正文子文本、导语、学习提示、U04 任务、课标、M0、纵向 N/A 与教师用书边界模块齐全。 |
| R04 | 否 | 正文事实、学习提示、课标定位、项目建议及教师用书缺源声明分层；未把研究解释冒充教材或课标结论。 |
| R05 | 否 | 15/15 KP 具备主维度、知识类型、四层归属、映射理由和有效 EV；KP-004/005/006/013 的关键解释链已闭合。 |
| R06 | 否 | 未登记真题；高考栏仅保留结构化 `M0`，不作直接衔接。 |
| R07 | 否 | 仅消费已核验的学生教材包、U04任务包和现行课标，未使用未验收上游。 |
| R08 | 否 | 卡片 v0.3.0、15 KP、23 EV、1 subtext、Source/Artifact、页码、M0/N/A 和当前 SHA/ledger 绑定闭合。 |
| R09 | 否 | 使用“外国作家作品研习”及现行 2020 修订课标，未改写任务群名称或将其当固定课型。 |
| R10 | 否 | 人文/语言双线按文本需要展开，未机械铺满四项核心素养，也未把学业质量当作单课难度标签。 |

P0/P1/P2：`0/0/0`。

## 4. 2.0-textbook knowledge_card 量规评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **25.0** | 23/23 EV 的来源、Artifact、三套页码/切分页和短引闭合；解释型 KP 双证，课标 exact quote 可回查。 |
| 事实与术语准确性 | 20 | 18 | **20.0** | 作品、人物、第三幕事件链、现行课标术语和事实/解释边界均准确。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 1 subtext、15 KP、导语/正文/提示/任务/课标/教师用书/M0/N/A 模块完整，文本特异性清楚。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 家庭权力、主体责任和开放结局与戏剧事件、对话、舞台物件双线并置；研究性母题明确保留解释边界。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 每个 KP 有层级和理由；课标定位及 M0 不越级，未伪造真题证据。 |
| 纵向贯通 | 8 | 6 | **7.0** | 在无双方 accepted 且逐边可核验目标时保持带理由 N/A，避免强造关系。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 三类提示分离；证据表、事件链、人物言行和修订成果可操作；教师用书缺源和 M0 边界明确。 |
| **合计** | **100** | **85** | **98.5** | 各维度均达到门槛。 |

## 5. 独立第二复审决定

**决定：`pass`。** 当前 `CARD-X2-U04-01` v0.3.0/SHA `f582983378a104cfda4eeecfb5ca4ebd0e59a33d28bfc32e3ecf4aed381d1281` 可与同 SHA 的另一份评审配对进入后续 G4。卡片、canonical Artifact、validator、账本或版本绑定发生任何变化，均使本报告失效并需重新复审。

## 6. 可复现绑定

- latest validator：`VAL-20260808-194012+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6`；归档运行报告 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-194012+0800.json` SHA `07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6`。
- ledger/deliverables binding：`work/knowledge/_meta/deliverables.jsonl` SHA `82778a8a230aa5e662c6c2bce6ab368448c14eb67c8ccfd6765f965587acb321`；当前 ledger 记录的卡片状态仍为 `linted`，本报告不执行状态迁移。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
