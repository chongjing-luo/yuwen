---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-01-SECONDARY-R1"
deliverable_id: "CARD-X3-U01-01"
artifact_version: "0.2.0"
artifact_sha256: "acca68281bb932deab7b06db04ae7ab41d50bde04a6a19343d3d8b6a1a18306c"
review_round: 1
reviewer: "independent_secondary_x3_u01_01_r1"
review_role: "secondary"
reviewed_at: "2026-08-08T21:00:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-205806+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "b014b2146714512c6877922c36fcd493ca34055c8f70458c8b487b28571fcb5b"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-205806+0800.json"
validator_archive_report_sha256: "b014b2146714512c6877922c36fcd493ca34055c8f70458c8b487b28571fcb5b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "01cb8097b62863811410df023eda38137f19ceb8dcaa5bd0c424207a59b54189"
validator_result: "passed"
decision: "pass"
---

# CARD-X3-U01-01 v0.2.0 独立第二复审 R1

## 1. 输入锁定与独立性

本轮只依据最终快照中的当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、来源与 Artifact 注册表、canonical 学生教材/单元任务/现行课标载体、共享账本和 validator 机械报告独立复核；不修改卡片、账本、validator 报告或状态迁移。

| 对象 | 最终快照绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md`；v0.2.0；SHA `acca68281bb932deab7b06db04ae7ab41d50bde04a6a19343d3d8b6a1a18306c`；状态 `linted` |
| 学生教材 Artifact | `ART-PKG-X3-001-PDF`；SHA `419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；正文物理页7—10、切分页2—5；`ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；U01任务物理页25—26 |
| 现行课标 Artifact | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| validator | `VAL-20260808-205806+0800`；`passed`；0 errors；`hash_verification=true` |

独立计数为 2/2 正文子文本、16/16 KP、15/15 EV；EV 类型为 F=1、Q=12、M=2、D=1。卡片同时分层登记单元导语、学习提示、U01任务、现行课标、教师用书缺源声明、高考 `M0` 与纵向 `N/A`。

## 2. 内容、证据与边界复核

- 两个正文子文本完整覆盖《氓》（物理页7—8，切分页2—3）和《离骚》（节选）（物理页8—10，切分页3—5）；导语、学习提示、U01任务和课标未被伪装成正文事实。
- 15/15 EV 均登记适配的 Source、canonical Artifact、可解析 locator、物理页/切分页、短引文和 `verified` 元数据。正文、学习提示、任务和课标证据之间的职责边界清楚。
- 16/16 KP 均有主维度、受控知识类型、四层主归属、判定理由、有效 EV 和置信状态。解释型 KP-005、KP-008、KP-011 等没有把研究性母题写成教材唯一答案；跨文本比较也保留了《氓》叙事与《离骚》骚体抒情的差异。
- 课标任务群5“文学阅读与写作”的定位与现行课标物理页25—27相符，涵盖古今中外诗歌阅读、感受形象/品味语言/体验情感、从语言/构思/形象/意蕴/情感等角度欣赏作品以及文学评论和写作要求。
- EV-014 的“能结合具体文本内容概括、阐释并用证据表达判断”是对课标能力要求的压缩概括，不宜作为课标逐字 exact quote。其定位有来源、有边界且卡片明确不据此判定完整学业质量等级，因此扣少量证据/术语分，不升级为 P1。
- 高考栏保持结构化 `M0`，未以题型相似性伪造真题闭合映射；纵向栏给出有理由的 `N/A`。教师用书 `edition_match=unknown`，且未消费缺源意见补写教材事实。

## 3. R01—R10 与 P0/P1/P2

| 代码 | 触发 | 独立结论 |
|---|---|---|
| R01 | 否 | 《氓》《离骚》的题名、作者/出处、正文事实、学习提示和任务引文均可回查到 canonical 载体。 |
| R02 | 否 | 15/15 EV 均有适配 Source/Artifact、locator 和短引；解释型 KP 有正文、栏目或任务证据，且未把开放解读冒充原文。 |
| R03 | 否 | 2 个正文子文本、导语、学习提示、U01任务、课标、教师用书边界、M0 和纵向 N/A 模块齐全，无合编漏项。 |
| R04 | 否 | 正文、学习提示、任务、课标与项目建议分层；“香草美人”、人物处境和跨文本母题均标为有依据的研究性概括，不宣称唯一答案。 |
| R05 | 否 | 16/16 KP 具备主维度、知识类型、四层归属、判定理由、证据和置信状态。 |
| R06 | 否 | 未登记真题小问—答案/评分—教材 KP 的闭合证据；高考栏仅保留 `M0`。 |
| R07 | 否 | 仅消费已核验学生教材、U01任务包和现行课标；教师用书缺源未被越权使用。 |
| R08 | 否 | 卡片版本、subtext/KP/EV计数、跨源页码、Source/Artifact、M0/N/A 及当前卡片和 ledger SHA 绑定闭合。 |
| R09 | 否 | 任务群名称使用现行课标的“文学阅读与写作”和“语言积累、梳理与探究”，未改写或混淆任务群。 |
| R10 | 否 | 人文/语言双维度围绕《氓》《离骚》的文本需要展开，未机械铺满核心素养，也未将学业质量当成单课难度标签。 |

P0/P1/P2：`0/0/0`。

## 4. 2.0-textbook 量规评分

| 维度 | 权重 | 门槛 | 得分 |
|---|---:|---:|---:|
| 证据链与可追溯性 | 25 | 21 | 24.0 |
| 事实与术语准确性 | 20 | 18 | 19.5 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 |
| 双维度与母题质量 | 15 | 12 | 14.5 |
| 四层与高考映射 | 10 | 8 | 9.5 |
| 纵向贯通 | 8 | 6 | 8.0 |
| 教学可用性与表达 | 7 | 5 | 6.5 |
| **合计** | **100** | **85** | **97.0** |

各维度均达到门槛。主要扣分仅来自 EV-014 的课标能力概括语未明确标注为 paraphrase/exact quote 边界，以及在没有已验收教师用书和真题闭合映射时保持保守表述。

## 5. 独立第二复审 R1 决定

**决定：`pass`。** 当前 `CARD-X3-U01-01` v0.2.0/SHA `acca68281bb932deab7b06db04ae7ab41d50bde04a6a19343d3d8b6a1a18306c` 达到独立第二复审门槛，可与同一最终 SHA 的主审结果配对进入后续流程。卡片、canonical Artifact、validator、账本或版本绑定发生任何变化，均使本报告失效并需重新复审。当前 ledger 状态仍为 `linted`；本报告不执行状态迁移。

## 6. 可复现绑定

- latest validator：`VAL-20260808-205806+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `b014b2146714512c6877922c36fcd493ca34055c8f70458c8b487b28571fcb5b`；归档运行报告 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-205806+0800.json` SHA 同为 `b014b2146714512c6877922c36fcd493ca34055c8b487b28571fcb5b`。
- ledger/deliverables binding：`work/knowledge/_meta/deliverables.jsonl` SHA `01cb8097b62863811410df023eda38137f19ceb8dcaa5bd0c424207a59b54189`；当前 ledger 状态仍为 `linted`，本报告不执行状态迁移。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
