---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-01-R5-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-01"
artifact_version: "0.2.1"
artifact_sha256: "4c638872a3b04947faea60d7f06d680e36f2653dca0a9f20a98f6b2a048f6c03"
review_round: 5
reviewer: "independent_primary_x3_u01_01_r5"
review_role: "primary"
reviewed_at: "2026-08-08T22:00:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "75cb4448ae4fea46a3c6c9d98998cf8cf272f8929d6ab88ad190964fb93e07f4"
validator_run_id: "VAL-20260808-211128+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "05fac06425823cf936112cec348bd2f2a94c70cb15597846443568031b425b0f"
validator_result: "passed"
decision: "pass"
---

# CARD-X3-U01-01 v0.2.1 独立主审 R5

## 1. 输入锁定与独立性

本轮重新读取当前最终候选卡片、冻结 `2.0-textbook` knowledge_card rubric/taxonomy、Source/Artifact 注册表、canonical 学生教材、U01 单元任务和现行课标，并独立复核全量 Claim—Evidence 关系；不复用旧版分数或结论，不修改卡片、账本、validator 或状态。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md`；v0.2.1；SHA `4c638872a3b04947faea60d7f06d680e36f2653dca0a9f20a98f6b2a048f6c03`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-001-PDF`；SHA `419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；6页；物理页6—11、切分页1—6 |
| 单元任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；2页；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；66页 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `75cb4448ae4fea46a3c6c9d98998cf8cf272f8929d6ab88ad190964fb93e07f4`；CARD-X3-U01-01 为 v0.2.1 / `linted` |
| validator | `VAL-20260808-211128+0800`；`passed`；0 errors；`hash_verification=true`；报告 SHA `05fac06425823cf936112cec348bd2f2a94c70cb15597846443568031b425b0f` |

## 2. 内容、证据与页码复核

- 卡片覆盖 2/2 正文子文本（《氓》《离骚》（节选））、单元导语、学习提示、U01 单元任务和现行课标；教材包物理页6—11/切分页1—6、任务包物理页25—26/切分页1—2的分割映射与 canonical 注册表一致。
- 15/15 EV 均有适配 Source、canonical Artifact、locator、短引文、支撑关系和 `verified` 元数据；16/16 KP 均有合法主维度、受控类型、四层归属、判定理由、证据ID和置信状态。
- EV-004 的完整诗句已闭合 KP-005/006：包含“士也罔极，二三其德”“信誓旦旦，不思其反”“反是不思，亦已焉哉”。
- EV-009—012 当前均定位到 `ART-PKG-X3-005-PDF` 的 **PDF物理页25；切分页1**。canonical 任务包切分页1完整包含任务一至任务四；相关短引分别对应古诗词当代价值研讨、《氓》与《孔雀东南飞》比较、虚实/意象探究和800字鉴赏文章/鉴赏集，页码收窄正确。
- EV-013 的任务群5定位为课标物理页25—27；EV-014 定位为课标物理页46、学业质量4-3。canonical 物理页46逐字包含“能结合作品的具体内容，阐释作品的情感、形象、主题和思想内涵，能对作品的表现手法作出自己的评论。”，与短引一致；卡片明确不据此判定单课完整水平。
- `KP-CARD-X3-U01-01-014` 主维度为 `语言`，符合冻结 taxonomy 的 `knowledge_dimensions=[人文, 语言]`；卡片 front matter、账本 transition/post-SHA 和 validator 快照一致。
- 人文/语言双线、三类语文活动、文学阅读与写作任务群、M0高考边界、纵向N/A理由及教师用书 `edition_match=unknown` 均分层表达；未把学生教材提示或项目建议冒充教师用书意见，也未把潜在题型冒充真题衔接。

轻微扣分仅针对少数综合性 KP 以代表性短引配合较宽正文 locator，以及 `quality_descriptor_refs` 保持空数组并通过 EV-014说明能力边界；不构成硬门缺陷或证据断链。

## 3. R01—R10 与 P0/P1/P2

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、作者/出处、正文事实、学习提示、U01任务和课标短引均与 canonical 载体一致。 |
| R02 | 否 | 15/15 EV 均可按 Source/Artifact/locator 回查；EV-004与KP-005/006 span闭合，EV-009—012物理页25正确，EV-014为物理页46逐字引文。 |
| R03 | 否 | 正文子文本、导语、学习提示、单元任务、课标、M0/N/A、教师用书边界、原子KP和证据表模块齐全。 |
| R04 | 否 | 教材事实、研究性概括、课标映射、项目建议和缺源声明分层；开放解释未写成教材唯一结论。 |
| R05 | 否 | 16/16 KP 均具合法主维度、受控类型、四层归属、判定理由、有效证据和置信状态。 |
| R06 | 否 | 高考栏保持 `M0`，未引用未登记真题、答案或评分资料，未声称直接衔接。 |
| R07 | 否 | 仅消费已登记并核验的学生教材包、任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片/账本版本 v0.2.1、ID、数量、路径、Source/Artifact 和 SHA 绑定一致；无断链。 |
| R09 | 否 | 使用现行课标规范任务群名称和三类语文活动，未把任务群改写为固定课型或教法。 |
| R10 | 否 | 未机械铺满四项核心素养，未将学业质量描述当作单课/知识点难度等级。 |

`P0/P1/P2 = 0/0/0`。

## 4. knowledge_card 量表评分

| 维度 | 权重 | 门槛 | 得分 | 复核依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | 15/15 EV 均有 canonical Source/Artifact、页位、短引、支撑关系和核验元数据；EV-004、EV-009—012、EV-014关键页位均闭合。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 书目信息、文本事实、现行课标术语、教材/项目/教师用书边界准确。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2/2 子文本、16/16 KP、15/15 EV、十个必备模块、M0和N/A均齐全，KP原子化适合检索。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文与语言双线覆盖源流、婚姻处境、人格理想、比兴、意象、节奏、跨文本比较和当代阅读；未使用非法维度。 |
| 四层与高考映射 | 10 | 8 | 9.5 | 各KP有四层主归属及理由，高考M0和不确定性边界清晰。 |
| 纵向贯通 | 8 | 6 | 8.0 | 在相邻卡尚未完成同版本双审时，使用有理由的N/A，不虚造递进关系。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | 教材学习提示、教师用书缺源、本项目建议明确分离；任务成果和证据表支持课堂使用与复查。 |
| **合计** | **100** | **85** | **97.0** | 总分及各维度均达到冻结 rubric 门槛。 |

## 5. 主审决定

**决定：`pass`。** 当前 `CARD-X3-U01-01` v0.2.1 / SHA `4c638872…` 通过独立主审：R01—R10 全否、P0/P1/P2=`0/0/0`、总分97.0且七维均过门槛。该 `pass` 仅闭合主审评审，不执行账本状态迁移；须与同一最终 SHA 的独立第二复审配对，并由协调者完成后续状态写回。

若卡片、账本、canonical Artifact 或 validator 绑定发生任何变化，本报告即失效并需以新 SHA 重审。

## 6. 可复现绑定

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md`；v0.2.1；SHA `4c638872a3b04947faea60d7f06d680e36f2653dca0a9f20a98f6b2a048f6c03`。
- 学生教材 canonical：`ART-PKG-X3-001-PDF` SHA `419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；单元任务 canonical：`ART-PKG-X3-005-PDF` SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；课标 canonical：`ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- ledger：`work/knowledge/_meta/deliverables.jsonl` SHA `75cb4448ae4fea46a3c6c9d98998cf8cf272f8929d6ab88ad190964fb93e07f4`。
- validator：`VAL-20260808-211128+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `05fac06425823cf936112cec348bd2f2a94c70cb15597846443568031b425b0f`；结果 `passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
