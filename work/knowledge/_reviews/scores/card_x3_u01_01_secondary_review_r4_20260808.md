---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-01-SECONDARY-R4"
deliverable_id: "CARD-X3-U01-01"
artifact_version: "0.2.1"
artifact_sha256: "075b2626ba164353290c12f484e69df54c46ebba1b5daf36532cf4122380918a"
review_round: 4
reviewer: "independent_secondary_x3_u01_01_r4"
review_role: "secondary"
reviewed_at: "2026-08-08T21:11:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-210836+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "4dc6499fe789642c1f75d2e77a605fccb52497c5fff16758bc03b72ec4aefc63"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-210836+0800.json"
validator_archive_report_sha256: "4dc6499fe789642c1f75d2e77a605fccb52497c5fff16758bc03b72ec4aefc63"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "6ddd582d73d42f544e17db4d25a041ceb5d7c6545a161e33d0185fba05a0cf13"
validator_result: "passed"
decision: "rework"
---

# CARD-X3-U01-01 v0.2.1 独立第二复审 R4

## 1. 输入锁定与独立性

本轮从当前最终候选快照重新开始，只依据当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、来源与 Artifact 注册表、canonical 学生教材/单元任务/现行课标载体、共享账本和 validator 机械报告复核；不读取或复用旧报告，不修改卡片、账本、validator 或状态迁移。

| 对象 | 最终快照绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md`；v0.2.1；SHA `075b2626ba164353290c12f484e69df54c46ebba1b5daf36532cf4122380918a`；状态 `linted` |
| 正文/学习提示 Artifact | `ART-PKG-X3-001-PDF`；SHA `419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；canonical 物理页6—11，切分页1—6 |
| U01任务 Artifact | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；canonical 物理页25—26，切分页1—2 |
| 现行课标 Artifact | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| validator | `VAL-20260808-210836+0800`；`passed`；0 errors；`hash_verification=true` |

结构计数为 2 个正文子文本、16/16 KP、15/15 EV；EV 类型为 F=1、Q=12、M=2、D=1。卡片版本与 ledger 均为 `0.2.1`，ID、状态、路径和 Source 链一致。

## 2. 独立证据与边界核查

- 《氓》与《离骚》（节选）的正文、导语、学习提示、U01任务、现行课标、M0、纵向 `N/A` 和教师用书 `edition_match=unknown` 均分层登记。正文页2—5、学习提示页6、任务页1—2和课标页25—27/46均可回查。
- EV-001—011、EV-013—015的 Source、canonical Artifact、locator、短引文和 `verified` 元数据均适配当前载体。EV-014 当前已改为课标水平4-3原文，物理页46的引文“能结合作品的具体内容，阐释作品的情感、形象、主题和思想内涵，能对作品的表现手法作出自己的评论”逐字命中；没有把该引文用于判定本卡完整学业质量等级。
- 但 **EV-012 的 locator 错误**：该行写作“PDF物理页26；切分页2；任务四”。实际渲染 `ART-PKG-X3-005-PDF` 的切分页1（对应 canonical 物理页25）完整承载“写一篇不少于800字的鉴赏文章……编一本《古典诗词鉴赏集》”；切分页2（物理页26）已开始“第二单元”，不承载该短引。MinerU `content_list_v2` 同样将任务四放在 page index 0，将“第二单元”放在 page index 1。
- 因此 KP-016 虽有 EV-010、EV-011、EV-012 三项引用，但其中 EV-012 的 Claim—EV—locator 闭合暂未完成；该问题属于证据定位硬门 R02，不重复计为 KP 字段缺失 R05。
- M0 行保持 `N/A | M0 | N/A`，没有真题小问、答案/评分或教材—真题闭合证据，不升级为 M1—M3。教师用书缺源仅作为 D 边界声明，不消费未登记教师用书意见。

## 3. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两篇课文的题名、作者/出处、诗句事实、页码范围和任务事实与 canonical 载体一致；EV-012 是 locator 问题，不是关键事实张冠李戴。 |
| R02 | **是** | EV-012 声明的物理页26/切页2不承载任务四短引；正式 Claim—EV—locator 链因此未达到全量可复现。 |
| R03 | 否 | 2 个正文子文本、导语、学习提示、任务包、课标、教师用书边界、M0和纵向 N/A 模块齐全。 |
| R04 | 否 | 教材正文/学习提示、任务原文、课标 M 定位和项目建议分层；开放母题明确为研究性概括，未冒充教材唯一答案。 |
| R05 | 否 | 16/16 KP 均有主维度、知识类型、四层归属、判定理由、置信状态和 EV-ID；EV-012 错页按 R02 处理。 |
| R06 | 否 | 高考栏保持结构化 `M0`，未登记或声称任何 M1—M3 真题衔接。 |
| R07 | 否 | 仅消费已验收的教材、任务包、现行课标和注册表，不使用未验收下游成果。 |
| R08 | 否 | 当前卡 front matter、ledger 和状态迁移均为 v0.2.1；稳定 ID、数量、路径和 Source/Artifact 链无结构断链。 |
| R09 | 否 | 使用现行课标版本和受控任务群名称“文学阅读与写作”“语言积累、梳理与探究”，没有改写成固定课型。 |
| R10 | 否 | 人文/语言双维度按文本需要展开；学业质量仅作能力定位，未机械铺满四项核心素养或贴完整等级。 |

## 4. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、重大事实错误、不可恢复损坏或大面积证据崩溃。 |
| P1 | **1** | `P1-EVIDENCE-LOCATOR-EV012`：任务四的完整短引在 canonical 任务切分页1/物理页25，卡片却登记切分页2/物理页26；需修正 locator 后重新计算 SHA。 |
| P2 | 0 | 未发现独立于 EV-012 定位硬门的结构、M0、版本或字段缺陷。 |

## 5. 2.0-textbook 诊断性评分

R02 为硬性否决，正式验收分数记为 `N/A`；以下数值仅用于返工优先级诊断，不能抵消 R02/P1。

| 维度 | 权重 | 门槛 | 诊断得分 |
|---|---:|---:|---:|
| 证据链与可追溯性 | 25 | 21 | 23.5 |
| 事实与术语准确性 | 20 | 18 | 20.0 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 |
| 双维度与母题质量 | 15 | 12 | 14.5 |
| 四层与高考映射 | 10 | 8 | 10.0 |
| 纵向贯通 | 8 | 6 | 8.0 |
| 教学可用性与表达 | 7 | 5 | 7.0 |
| **诊断合计** | **100** | **85** | **98.0** |

## 6. 独立第二复审 R4 决定

**正式决定：`rework`。** 当前 v0.2.1/SHA `075b2626ba164353290c12f484e69df54c46ebba1b5daf36532cf4122380918a` 不得进入 `accepted`、G4 或被 U01 单元图谱正式消费。最小返工是将 EV-012 locator 改为 `PDF物理页25；切分页1`，修正版本记录并产生新 SHA，复跑 validator 后，再由主审和独立第二复审对新 SHA 从零复核。除该证据定位问题外，EV-014、M0、教师用书 unknown、KP/EV 数量和版本绑定均已通过本轮核查。

## 7. 可复现绑定

- latest validator：`VAL-20260808-210836+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `4dc6499fe789642c1f75d2e77a605fccb52497c5fff16758bc03b72ec4aefc63`；归档报告 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-210836+0800.json` SHA 同为 `4dc6499fe789642c1f75d2e77a605fccb52497c5fff16758bc03b72ec4aefc63`。
- ledger binding：`work/knowledge/_meta/deliverables.jsonl` SHA `6ddd582d73d42f544e17db4d25a041ceb5d7c6545a161e33d0185fba05a0cf13`；当前状态仍为 `linted`，本报告不执行状态迁移。
- canonical Artifact SHA：`ART-PKG-X3-001-PDF`=`419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
