---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-01-SECONDARY-R5"
deliverable_id: "CARD-X3-U01-01"
artifact_version: "0.2.1"
artifact_sha256: "4c638872a3b04947faea60d7f06d680e36f2653dca0a9f20a98f6b2a048f6c03"
review_round: 5
reviewer: "independent_secondary_x3_u01_01_r5"
review_role: "secondary"
reviewed_at: "2026-08-08T21:14:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-211128+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "05fac06425823cf936112cec348bd2f2a94c70cb15597846443568031b425b0f"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-211128+0800.json"
validator_archive_report_sha256: "05fac06425823cf936112cec348bd2f2a94c70cb15597846443568031b425b0f"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "75cb4448ae4fea46a3c6c9d98998cf8cf272f8929d6ab88ad190964fb93e07f4"
validator_result: "passed"
decision: "pass"
---

# CARD-X3-U01-01 v0.2.1 独立第二复审 R5

## 1. 输入锁定与独立性

本轮依据当前 v0.2.1 快照重新独立复核，不读取或复用旧报告、旧 SHA、旧分数或旧 R/P 结论；只使用当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、来源与 Artifact 注册表、canonical 学生教材/单元任务/现行课标载体、共享账本和 validator 报告。本轮不修改卡片、账本、validator 或状态迁移。

| 对象 | 最终快照绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md`；v0.2.1；SHA `4c638872a3b04947faea60d7f06d680e36f2653dca0a9f20a98f6b2a048f6c03`；状态 `linted` |
| 正文/学习提示 Artifact | `ART-PKG-X3-001-PDF`；SHA `419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；canonical 物理页6—11、切分页1—6 |
| U01任务 Artifact | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；canonical 物理页25—26、切分页1—2 |
| 现行课标 Artifact | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| validator | `VAL-20260808-211128+0800`；`passed`；0 errors；`hash_verification=true` |

当前结构计数为 2 个正文子文本、16/16 KP、15/15 EV；EV 类型为 F=1、Q=11、M=2、D=1。卡片 front matter 与 ledger 均为 v0.2.1，ID、状态、路径、owner 和 Source 链一致。

## 2. 全量页码、证据与边界核验

- `ART-PKG-X3-001-PDF` 的导语为物理页6/切页1，《氓》为物理页7—8/切页2—3，《离骚》（节选）为物理页8—10/切页3—5，学习提示为物理页11/切页6。EV-001—008 的短引均能在所声明范围回查。
- `ART-PKG-X3-005-PDF` 的任务一、二、三、四均在 canonical 物理页25/切页1；切页2/物理页26已进入“第二单元”。当前 EV-009、EV-010、EV-011、EV-012 均已登记为物理页25/切页1，且 MinerU `full.md` 与 `content_list_v2` 的任务文本一致。EV-011（虚实/意象/意境）和 EV-012（800字鉴赏文章/《古典诗词鉴赏集》）的 locator 本轮均通过。
- 现行课标 EV-013 的任务群5定位在物理页25—27，逐字支持“感受形象、品味语言、体验情感”“撰写文学评论”等要求；EV-014 的学业质量4-3逐字定位在物理页46，短引与 canonical 原文一致。卡片明确只作能力边界定位，不据此判定完整学业质量等级。
- 15/15 EV 均有可解析 Source、canonical Artifact、locator、短引文、支撑关系和 `verified` 元数据。16/16 KP 均有主维度、受控类型、四层主归属、判定理由、有效 EV 和置信状态；解释型 KP 使用适配的多条证据或同一连续原文段，不把开放母题冒充教材唯一答案。
- 教师用书采用 D 型边界声明，`edition_match=unknown`，未用缺失来源补写正文或象征解释；纵向栏为有理由的 `N/A`；高考栏保留结构化 `M0`，不伪造 M1—M3 真题映射。

## 3. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两篇课文题名、作者/出处、诗句事实、正文边界、任务要求和课标引文均与 canonical 载体一致。 |
| R02 | 否 | 15/15 EV 的 Source/Artifact/locator/短引/状态可复核；任务四 EV-012 已修正为物理页25/切页1，课标 EV-014 已定位到物理页46。 |
| R03 | 否 | 2 个正文子文本、导语、学习提示、U01 任务、课标、教师用书边界、M0 和纵向 N/A 模块齐全。 |
| R04 | 否 | 正文、学习提示、任务原文、课标 M 定位和项目建议分层；研究性母题明确为依据教材证据的概括，不宣称教材唯一答案。 |
| R05 | 否 | 16/16 KP 均具有主维度、知识类型、四层归属、判定理由、有效证据和置信状态。 |
| R06 | 否 | 未登记真题小问—答案/评分—教材 KP 的闭合证据；高考栏只保留结构化 `M0`。 |
| R07 | 否 | 仅消费已验收教材包、U01任务包、现行课标和注册表，无未验收上游依赖。 |
| R08 | 否 | 卡片、ledger 和状态迁移均为 v0.2.1；Card/KP/EV/Subtext/Source/Artifact 数量、ID、路径和链接闭合。 |
| R09 | 否 | 使用现行课标版本及规范任务群名称“文学阅读与写作”“语言积累、梳理与探究”，未改写任务群或当固定课型。 |
| R10 | 否 | 人文/语言双维度围绕文本需要展开，未机械铺满四项核心素养，也未把学业质量水平当作单课难度标签。 |

## 4. P0/P1/P2

`P0/P1/P2 = 0/0/0`。本轮未发现来源伪造、关键事实错误、Claim—EV 断裂、版本漂移、M0越权或独立的字段/表达阻断项。

## 5. 2.0-textbook 量规评分

| 维度 | 权重 | 门槛 | 得分 |
|---|---:|---:|---:|
| 证据链与可追溯性 | 25 | 21 | 24.5 |
| 事实与术语准确性 | 20 | 18 | 19.5 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 |
| 双维度与母题质量 | 15 | 12 | 14.5 |
| 四层与高考映射 | 10 | 8 | 10.0 |
| 纵向贯通 | 8 | 6 | 8.0 |
| 教学可用性与表达 | 7 | 5 | 7.0 |
| **合计** | **100** | **85** | **98.5** |

证据链小幅保守扣分用于反映短引中以省略号压缩连续原文及 D 型教师用书缺源声明的可复核边界；不构成硬门缺陷。所有维度均达到门槛。

## 6. 独立第二复审 R5 决定

**决定：`pass`。** 当前 `CARD-X3-U01-01` v0.2.1/SHA `4c638872a3b04947faea60d7f06d680e36f2653dca0a9f20a98f6b2a048f6c03` 达到独立第二复审门槛，可与同一最终 SHA 的主审结果配对进入后续流程。当前 ledger 状态仍为 `linted`；本报告不执行状态迁移。卡片、canonical Artifact、validator、账本或版本绑定发生任何变化，均使本报告失效并需重新复审。

## 7. 可复现绑定

- latest validator：`VAL-20260808-211128+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `05fac06425823cf936112cec348bd2f2a94c70cb15597846443568031b425b0f`；归档运行报告 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-211128+0800.json` SHA 同为 `05fac06425823cf936112cec348bd2f2a94c70cb15597846443568031b425b0f`。
- ledger binding：`work/knowledge/_meta/deliverables.jsonl` SHA `75cb4448ae4fea46a3c6c9d98998cf8cf272f8929d6ab88ad190964fb93e07f4`；状态仍为 `linted`，本报告不执行状态迁移。
- canonical Artifact SHA：`ART-PKG-X3-001-PDF`=`419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
