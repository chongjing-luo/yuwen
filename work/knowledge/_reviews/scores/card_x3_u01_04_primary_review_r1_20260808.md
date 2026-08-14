---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-04-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-04"
artifact_version: "0.2.0"
artifact_sha256: "61e77df4f932be95abe0ad664f887f15179b1d837535c7d1d1dad281655ef2a1"
review_round: 1
reviewer: "independent_primary_x3_u01_04_r1"
review_role: "primary"
reviewed_at: "2026-08-08T22:15:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "1c0a9d7cc2e5f0b4f1df37cbe36d3b2906c1983e104be353466f8a57b0d8599d"
validator_run_id: "VAL-20260808-221001+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-221001+0800.json"
validator_report_sha256: "4ca0b6569bc9562543c2843075cf75b0f56e8c36588a92fc9f00c3c1ee3a1301"
validator_result: "passed"
decision: "rework"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "3500bdb1a1bb96bd72ae97675336087a8c044bc208c9ae0996fc90a57c95692e"
---

# CARD-X3-U01-04 v0.2.0 独立主审 R1

## 1. 输入锁定与状态一致性

本轮从指定的 v0.2.0 快照重新开始，仅使用当前卡片、冻结 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 课4教材、U01 单元任务、现行课标、共享账本和 validator 归档报告；不修改卡片、账本、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.0；SHA `61e77df4f932be95abe0ad664f887f15179b1d837535c7d1d1dad281655ef2a1`；front matter 状态 `linted` |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `1c0a9d7cc2e5f0b4f1df37cbe36d3b2906c1983e104be353466f8a57b0d8599d`；CARD-X3-U01-04 为 v0.2.0/`linted`，`REBUILD drafted→linted` |
| 学生教材 canonical | `ART-PKG-X3-004-PDF`；SHA `b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；物理页22—24、切分页1—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；学业质量4-3物理页46 |
| validator | `VAL-20260808-221001+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `4ca0b6569bc9562543c2843075cf75b0f56e8c36588a92fc9f00c3c1ee3a1301` |

卡片 front matter、正文自述、ledger 状态和 REBUILD transition 一致；当前为 `linted`，尚未进入 `accepted`，状态元数据本身不触发 R08。

## 2. 覆盖、事实与证据复核

- 当前卡片有 2 个正文子文本、17 个原子 KP、16 个 EV；EV 类型为 Q=12、F=1、M=2、D=1，均为单值 Q/F/M/D。所有 KP 均具主维度、知识类型、四层归属、判定理由、证据 ID 和置信状态。
- canonical 课4物理页22为《望海潮》，物理页23—24为《扬州慢》序、正文、注释和学习提示；U01任务物理页25/切页1承载任务一至四；课标任务群5在物理页25—26，学业质量4-3在物理页46。
- 《望海潮》的东南形胜、三吴钱塘、怒涛、市井、湖山、羌管、菱歌、高牙与凤池结句，均可在物理页22连续回查；《扬州慢》序的雪霁/荠麦/萧条/戍角/黍离，正文的春风十里、废池乔木、清角空城、杜牧典故和红药结尾，均可在物理页23—24回查。
- 学习提示 EV-007—008 正确支持“城市对象”“承平盛世/劫后孤城”、铺叙、以点带面、虚实相间、今昔对比、杜牧想象与声韵；任务 EV-009—013 正确支持研讨、比较、虚实/意象探究和800字鉴赏集；课标 EV-014—015 和 M0/N/A 边界合规。

## 3. 阻断性发现与非阻断问题

### P1-A：EV-001 Claim—Artifact 不闭合

EV-001 的 Claim 写为“课4正文、学习提示和任务的来源边界”，但 Source/Artifact 仅绑定 `SRC-PKG-X3-004`/`ART-PKG-X3-004-PDF`，locator 也只有教材物理页22—24；U01任务属于 `SRC-PKG-X3-005`/`ART-PKG-X3-005-PDF`，并未被该 EV 覆盖。短引“‘望海潮’‘扬州慢’及其正文、学习提示均位于本canonical课文包；正式引文回到PDF”也只承担课文包标题/正文/学习提示范围，不能独立承担“任务”边界。该行当前不能闭合正式 Claim，且 KP-001 引用它。

修复方式：将 Claim 收窄为课4教材正文/学习提示范围并保留 Q，任务边界改由 EV-010—013 支撑；或将它拆/改为 D 边界证据，并同时绑定 `SRC-PKG-X3-005`/`ART-PKG-X3-005-PDF` 及任务 locator。回归时同步检查 KP-001。

### P1-B：§8.1 把项目操作混入教材学习提示

§8.1 标题为“教材学习提示”，但内容写入“制作‘城市空间—时间视角—意象/声音—典故—情绪’证据表”和具体比较操作。canonical 学习提示确实要求比较两首词的城市对象、盛衰、铺叙/虚实、今昔和声韵，并要求诵读体会；它没有明示制作该证据表，也没有规定该项目化记录格式。该混写使规范教材提示与本项目教学建议边界不清，触发 R04。

修复方式：§8.1 只保留可由 EV-007—008 逐字支持的教材提示；证据表、四列表、比较步骤和评价留痕移到 §8.3，并显式标为本项目建议。

### 非阻断 P2

- `KP-017`/“诵读与表达迁移”写“成果需保留引文、提纲、反馈和修订”，任务原文直接要求研讨、比较/探究、800字文章和合作编集，并未明示必须保存这些过程留痕。应标为项目建议或收窄为教材直接成果。
- EV-003 的短引为代表性城市铺陈片段，足以支持核心主张但未逐项展开所有空间/生活细部；回归时可补连续 span 或收窄复合 Claim。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | 两词题名、作者、词句、城市/历史事实、注释、页码和课标术语均与 canonical 载体一致。 |
| R02 | **是** | EV-001 的正式 Claim 同时要求教材和任务边界，但其 Artifact/locator/短引不含任务来源，需证主张缺适配来源。 |
| R03 | 否 | 两个正文子文本、学习提示、任务、课标、原子 KP、教学模块、M0 和纵向 N/A 均存在。 |
| R04 | **是** | §8.1 将项目证据表和具体比较操作写成教材学习提示，规范来源与项目建议边界混写。 |
| R05 | 否 | 17/17 KP 形式字段齐全且均有主层级、映射理由和至少一条有效证据；KP-017 的过程留痕仅为 P2。 |
| R06 | 否 | 高考表严格保持 `M0/N/A`，未挂未登记真题、答案或评分资料，也未声称 M1—M3。 |
| R07 | 否 | 正式内容只消费已登记并核验的课4教材、U01任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、账本、版本、状态、ID、数量和 Source/Artifact 链一致；validator 哈希校验通过。 |
| R09 | 否 | 使用现行课标任务群“文学阅读与写作”“语言积累、梳理与探究”，没有改写任务群名称或将其当固定课型。 |
| R10 | 否 | 未机械铺满四项核心素养，学业质量4-3仅作定位，不作为单课等级或题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误或不可恢复损坏。 |
| P1 | 2 | `P1-EV001-BOUNDARY`：EV-001 将课文 Artifact 当作同时覆盖任务边界；`P1-SEC81-MIX`：§8.1 将项目证据表/比较操作写成教材学习提示。 |
| P2 | 2 | `P2-KP017-PROCESS`：任务未明示的过程留痕写成任务成果；`P2-EV003-SPAN`：复合城市铺陈 Claim 可进一步补连续 span 或收窄。 |

## 6. 2.0-textbook 诊断评分

因 R02/R04 与两项 P1 硬门触发，正式验收分记为 `N/A`；以下分数仅用于返工定位，不能替代放行结论。

| 维度 | 权重 | 门槛 | 诊断得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 18.5 | 15/16 EV 的来源、页位和短引闭合；EV-001 混源，EV-003 的复合 span 稍压缩。 |
| 事实与术语准确性 | 20 | 18 | 19.0 | 两词文本事实、城市背景、典故、体式和课标术语准确；来源栏目混写扣分。 |
| 字段完整与知识粒度 | 15 | 12 | 14.5 | 2 子文本、17 KP、16 EV、任务/课标/M0 模块齐全；KP-017 过程要求需收窄。 |
| 双维度与母题质量 | 15 | 12 | 14.0 | 盛世/劫后、城市记忆、铺叙、虚实、今昔、声音和典故形成双线；个别复合 Claim 需加固。 |
| 四层与高考映射 | 10 | 8 | 9.5 | 四层理由和 M0 边界清楚；未建立真题双向证据。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前无双方 accepted 目标，使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 5.0 | 证据链建议可操作，但 §8.1 教材提示与项目建议混写，来源分层未过。 |
| **诊断合计** | **100** | **85** | **88.5** | **仅供返工优先级；硬门触发，不能作为合格分数。** |

## 7. 返工与主审决定

1. 修正 EV-001：收窄至课4教材正文/学习提示，或拆成 D 并绑定任务 Artifact；同步核对 KP-001 和 §1 的任务边界证据。
2. 重写 §8.1：只保留学习提示直接支持的城市对象、盛衰、铺叙/虚实、今昔、声韵和诵读；证据表、比较步骤和过程评价移至 §8.3，明确为项目建议。
3. 收窄 KP-017/“诵读与表达迁移”的任务成果 Claim，或把引文、提纲、反馈、修订显式降为项目建议；按需补齐 EV-003 的连续 span。
4. 升版并重算卡片 SHA、更新 ledger transition、重跑 validator，再以新 SHA 进行独立主审和第二复审；当前 SHA 不得进入 `accepted` 或被单元图谱正式消费。

**主审决定：`rework`。** 当前 `CARD-X3-U01-04` v0.2.0/SHA `61e77df4f932be95abe0ad664f887f15179b1d837535c7d1d1dad281655ef2a1` 未通过独立主审。本报告不执行任何状态迁移。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.0；SHA `61e77df4f932be95abe0ad664f887f15179b1d837535c7d1d1dad281655ef2a1`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `1c0a9d7cc2e5f0b4f1df37cbe36d3b2906c1983e104be353466f8a57b0d8599d`；CARD-X3-U01-04 为 `linted`/`REBUILD`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-221001+0800.json`；SHA `4ca0b6569bc9562543c2843075cf75b0f56e8c36588a92fc9f00c3c1ee3a1301`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-004-PDF`=`b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填。
