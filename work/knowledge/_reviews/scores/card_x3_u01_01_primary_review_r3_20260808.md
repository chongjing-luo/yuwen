---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-01-R3-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-01"
artifact_version: "0.2.1"
artifact_sha256: "e9a1d9b9092cd8226cdd7c216d272983f94c035e82e18e9c4b42abed55d83062"
review_round: 3
reviewer: "independent_primary_x3_u01_01_r3"
review_role: "primary"
reviewed_at: "2026-08-08T21:45:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "754e7e236e39d0dfb5df5923cebf5016bf1e027ffb6977c7990560691a618b8a"
validator_run_id: "VAL-20260808-210639+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "3b635c5597d0bd12dd6c8266a80948dff59d5a9c7ec081e6fdaf4d8ce794bd4c"
validator_result: "passed"
decision: "rework"
---

# CARD-X3-U01-01 v0.2.1 独立主审 R3

## 1. 输入锁定与独立性

本轮重新读取当前卡片、冻结的 `2.0-textbook` knowledge_card rubric/taxonomy、Source/Artifact 注册表、canonical 学生教材、U01 单元任务和现行课标，并独立复核 Claim—Evidence 关系；不复用上一轮分数或结论，不修改卡片、账本、validator 或状态。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md`；v0.2.1；SHA `e9a1d9b9092cd8226cdd7c216d272983f94c035e82e18c9c4b42abed55d83062`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-001-PDF`；SHA `419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；6页；物理页6—11、切分页1—6 |
| 单元任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；2页；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；66页 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `754e7e236e39d0dfb5df5923cebf5016bf1e027ffb6977c7990560691a618b8a`；CARD-X3-U01-01 为 v0.2.1 / `linted` |
| validator | `VAL-20260808-210639+0800`；`passed`；0 errors；`hash_verification=true`；报告 SHA `3b635c5597d0bd12dd6c8266a80948dff59d5a9c7ec081e6fdaf4d8ce794bd4c` |

## 2. 独立复核结果

### 2.1 已修复项

- `KP-CARD-X3-U01-01-014` 当前主维度为 `语言`，符合冻结 taxonomy 的 `knowledge_dimensions=[人文, 语言]`；上一轮的非法“思维”值已消除。
- `EV-CARD-X3-U01-01-004` 已补齐“士也罔极，二三其德”“信誓旦旦，不思其反”“反是不思，亦已焉哉”，可闭合 KP-005、KP-006 的相关 Claim—Evidence span。
- `EV-CARD-X3-U01-01-014` 已改为课标 canonical 原文：“能结合作品的具体内容，阐释作品的情感、形象、主题和思想内涵，能对作品的表现手法作出自己的评论。”并保留“不据此判定完整水平”的边界。
- 卡片 front matter、账本及 transition 均为 v0.2.1，卡片 SHA 与 ledger transition 的 `post_sha256` 一致；数量为 2/2 正文子文本、16/16 KP、15/15 EV。

### 2.2 仍未闭合的证据定位

`EV-CARD-X3-U01-01-014` 的短引现在逐字对应课标，但 locator 仍登记为 `PDF物理页44`。在绑定的 canonical `ART-CURR-2020-PDF`（66页、SHA `7a187...`）中，逐字短引实际位于 **PDF物理页46（印刷页38）**；物理页44（印刷页36）没有该 `4-3` 文学鉴赏描述，而是水平1—2、1—3、1—4描述。故该直接引文不能按当前 locator 回查，触发证据链硬门；建议改为 `PDF物理页46；印刷页38；4-3 学业质量描述`，并重新核验。

其他 canonical 引文和页码复核未发现新的关键事实错误：EV-001—008 的教材导语、正文、学习提示，EV-009—012 的U01任务，EV-013 的课标任务群5短引均可在所登记页位回查；EV-015 的教师用书缺源声明与 `edition_match=unknown` 边界一致。

## 3. R01—R10 与 P0/P1/P2

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 《氓》《离骚》题名、作者/出处、诗句、学习提示、任务事实与 canonical 载体一致。 |
| R02 | **是** | EV-014 的逐字引文与课标内容一致，但其物理页 locator 错一页，当前不能按登记 locator 回查；修正为物理页46后可复核。 |
| R03 | 否 | 两个正文子文本、导语、学习提示、U01任务、课标、M0/N/A、教师用书边界及证据表模块齐全。 |
| R04 | 否 | 课标直接引文已改为原文并保留能力边界；教材提示、项目建议和缺源声明分层。 |
| R05 | 否 | 16/16 KP 均有合法主维度、类型、四层归属、理由、证据和置信状态。 |
| R06 | 否 | 高考栏保留 `M0`，没有把题型相似性升级为直接衔接，也未引用未登记真题。 |
| R07 | 否 | 仅消费已登记并核验的学生教材包、任务包和现行课标。 |
| R08 | 否 | 当前卡片 front matter、账本 version/transition、ID、数量和 SHA 绑定一致；EV-014 是单条 locator 错误，不是版本或跨文件 ID 断链。 |
| R09 | 否 | 使用现行课标规范任务群名称，未把任务群当固定课型或教法。 |
| R10 | 否 | 未机械铺满四项核心素养，也未把学业质量水平当作单课难度标签。 |

`P0/P1/P2 = 0/1/0`。唯一 P1 为 EV-014 locator 错误；它属于局部可修复的 R02 硬门缺陷。

## 4. knowledge_card 量表诊断分

因 R02 硬门尚未通过，以下为定位返工成本的诊断分，不替代合格性判断。

| 维度 | 权重 | 门槛 | 诊断得分 | 复核依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 22.5 | 15/15 EV均有Source/Artifact/短引与验证元数据；EV-014逐字内容正确但物理页错一页，定位项扣分。 |
| 事实与术语准确性 | 20 | 18 | 19.0 | 教材事实、课标术语、M0和边界准确；EV-014页位错误使可复查性略降。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2/2子文本、16/16 KP、15/15 EV和十个必备模块齐全，原子粒度可消费。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文/语言双线覆盖源流、处境、人格、比兴、意象、节奏与比较；KP-014已归入合法语言维度。 |
| 四层与高考映射 | 10 | 8 | 9.5 | 各KP均有四层与理由；高考明确M0，未制造真题映射。 |
| 纵向贯通 | 8 | 6 | 8.0 | 对尚未完成同版本双审的相邻卡保持有理由的N/A。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | 教材提示、教师用书缺源、本项目建议分离；任务成果和证据表可操作。 |
| **合计** | **100** | **85** | **95.0** | 质量内容达到诊断门槛，但不能抵消 R02 硬门失败。 |

## 5. 返工与决定

只需完成以下最小修复：

1. 将 EV-014 locator 从 `PDF物理页44` 改为 canonical `ART-CURR-2020-PDF` 的 `PDF物理页46`（可同时记录印刷页38、4-3描述），逐字复核短引；
2. 重新计算卡片 SHA，更新 ledger transition/绑定，重跑 validator；
3. 以新 SHA 重新进行 primary/secondary 双审。本报告绑定当前 e9a1d9…，修订后即失效。

**主审决定：`rework`。** 当前卡片不得进入 `accepted` 或被单元图谱正式消费；完成 locator 修复并通过新一轮同 SHA 双审后再行验收。

## 6. 可复现绑定

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md`；v0.2.1；SHA `e9a1d9b9092cd8226cdd7c216d272983f94c035e82e18c9c4b42abed55d83062`。
- 学生教材 canonical：`ART-PKG-X3-001-PDF` SHA `419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；单元任务 canonical：`ART-PKG-X3-005-PDF` SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；课标 canonical：`ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- ledger：`work/knowledge/_meta/deliverables.jsonl` SHA `754e7e236e39d0dfb5df5923cebf5016bf1e027ffb6977c7990560691a618b8a`。
- validator：`VAL-20260808-210639+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `3b635c5597d0bd12dd6c8266a80948dff59d5a9c7ec081e6fdaf4d8ce794bd4c`；结果 `passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
