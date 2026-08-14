---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X3-U02-SECONDARY-R2"
deliverable_id: "UNIT-X3-U02"
artifact_version: "0.2.2"
artifact_sha256: "464bba3a461fdb07f0d4fbcc95157f27c3ebaa4afa59a505c6df29f45214e83f"
review_round: 2
reviewer: "independent_secondary_unit_x3_u02_r2"
review_role: "secondary"
reviewed_at: "2026-08-09T02:30:29+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "3d039ba22e89c780673ffe404114b945937939ac7b8321ebfb7b36f1271e93f4"
validator_run_id: "VAL-20260809-022936+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u02_unit_final_pre_review_v022_20260809.json"
validator_report_sha256: "0d31570ae63630cbedbdd0313c5b255e8c690a7318e8fb5339e06a8d4201c59e"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "b9f16a71f290ba88cc040b801bc162b7ae26d448446ee31229827d7de1da23b3"
---

# UNIT-X3-U02 v0.2.2 独立第二复审 R2

## 1. 输入锁定与独立性

本轮只依据 v0.2.2 图谱、四张当前 `accepted` 上游卡、冻结的 `2.0-textbook` rubric/taxonomy、共享 ledger 和指定 validator 独立复核；不复用旧 SHA 的结论，不修改图谱、上游卡、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修下册/units/UNIT-X3-U02.md`；v0.2.2；SHA `464bba3a461fdb07f0d4fbcc95157f27c3ebaa4afa59a505c6df29f45214e83f`；状态 `linted` |
| `CARD-X3-U02-01` | v0.2.0；`accepted`；SHA `f0814040c695ef9d65b7ddca2b5d8f837e044f85a597ae7a7bfd58da5b8a91b4` |
| `CARD-X3-U02-02` | v0.2.0；`accepted`；SHA `1ad573c3d1cfb97876d604970e55129ca18e10e3147c08703bde6f43755c0715` |
| `CARD-X3-U02-03` | v0.2.1；`accepted`；SHA `a86827411ce824d72546d98c0e2f9a72dad2e6480f6dca828d2159f71d7c9c78` |
| `CARD-X3-U02-04` | v0.2.1；`accepted`；SHA `c56d5511b1a7cd58efc4ab4827b63bb979a6fac48c4b688f719630c3905c3fa7` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `3d039ba22e89c780673ffe404114b945937939ac7b8321ebfb7b36f1271e93f4`；图谱条目 v0.2.2/`linted`，四卡均为 `accepted` |
| validator | `VAL-20260809-022936+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `0d31570ae63630cbedbdd0313c5b255e8c690a7318e8fb5339e06a8d4201c59e` |

图谱文件、ledger 最后迁移记录和四张上游卡的实际文件 SHA 均逐一复算一致。validator 的外部真题、教师用书等 warning 是项目边界提示，不构成本图谱错误。

## 2. 覆盖、结构与回链复核

- 四张 accepted 卡的 KP 数为 `19+18+19+18=74`。对图谱中的完整 ID、范围写法和斜线压缩写法独立展开后，任务、双维度节点和关系语义区覆盖 `74/74` KP；无漏项、重复或跨卡混淆。v0.2.2 已将原先仅出现在 §1.1 索引的 13 个 KP 补入 H/L 语义节点，并保持完整 Card/KP-ID。
- 图谱包含 5 个人文节点、5 个语言节点、4 个单元任务和 12 条关系；所有节点和任务均能回查 Card/KP/EV 或 canonical 任务包。关系均有稳定 `REL-ID`、双方 KP 和 EV 入口。
- 12 个关系类型均属于 taxonomy 允许集合：`比较/迁移/组成`。关系分别处理普通民众与权力、乡土共同体、贫困伦理、记忆时代、文体语言和共同鉴赏程序，未把跨文体相似性升级为教材事实。
- 4 项任务均定位到 `SRC-PKG-X3-010`/`ART-PKG-X3-010-PDF` 物理页 72—73，并给出能力动作、成果和评价证据；项目化的比较、研讨、语言札记和交流修订要求与教材任务原文分层。

## 3. 双维度、综合关系与证据边界

人文线覆盖普通民众处境、乡土风俗与共同体、尊严伦理与命运、记忆消逝与时代变化、现代文学审美与当代阅读；语言线覆盖现代小说、现代诗歌、散文/秦腔场面、话剧台词动作及共同语言鉴赏证据链。新增边界、题名/作者、阿Q艺术手法、诗歌结尾和山村记忆 KP 均已放入匹配节点，并有对应 EV。

关系表逐条给出源/目标 KP、受控关系、共性或差异及证据。`REL-001`—`REL-007`、`REL-009` 是保留文体语境的比较，`REL-008/010` 是阅读程序迁移，`REL-011/012` 只表示任务成果链组成。证据范围覆盖相应两端，没有发现关系 ID、类型或目标 KP 断链。

## 4. 高考、纵向关系与教师用书边界

- 高考栏保持结构化 `N/A | M0 | N/A`，明确尚未登记可逐小问核验的真题题文—答案/评分—教材 KP 闭合证据；不把人物、环境、叙述语言、意象、舞台动作或比较题型相似性升级为 M1—M3。
- 前、后单元均为带 `na_reason` 的 `N/A`：当前没有双方 `accepted` KP/EV 的逐边核验，不以单元排列或主题相似性臆造递进。
- 教师用书为 `edition_match=unknown`；图谱不消费未登记教师用书意见、网络解析或外部文学史考证。

## 5. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 四张 accepted 卡、七篇现代文学文本/导语、任务和课标边界均可回到已登记来源，未见关键事实错误。 |
| R02 | 否 | 74/74 KP、5 H、5 L、4 TASK、12 REL 均有适配 Card/KP/EV 或任务来源；综合保留不同文体和时代语境。 |
| R03 | 否 | 上游清单、全量 KP 索引、任务、双维度节点、关系、M0、纵向 N/A、Issue 和版本记录齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标、项目评价、外部材料边界和单元综合分层清楚。 |
| R05 | 否 | 74/74 KP 均保留上游主维度、类型、层级和 EV 入口，并进入语义节点、任务或关系。 |
| R06 | 否 | 高考严格保持 M0；没有未登记真题、答案/评分资料或越级映射。 |
| R07 | 否 | 四张上游卡均为 `accepted`，且实际文件 SHA、图谱 §1 和 ledger post-SHA 一致。 |
| R08 | 否 | 图谱/卡/KP/EV/TASK/REL 的 ID、数量、版本、路径、SHA 和状态链闭合；13 个孤立 KP 已在 v0.2.2 补入语义节点。 |
| R09 | 否 | 使用现行课标任务群 10 和学业质量 4-3 的正确定位，未改写任务群名称或把课标等级当作达成标签。 |
| R10 | 否 | 人文/语言双线按七篇现代文学文本和 U02 任务需要展开，未机械铺满核心素养，也未把学业质量水平当作题目难度。 |

## 6. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键覆盖缺失、非法关系类型、未验收上游、M0 越级、教师用书混入、版本漂移或 SHA 断链。 |
| P2 | 0 | v0.2.2 已关闭 13 个仅索引 KP 的语义孤立问题；当前未发现新的非阻断缺陷。 |

## 7. `2.0-textbook` unit_graph 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 4/4 accepted 卡、74/74 KP、4/4 任务、5 H/5 L、12/12 REL 均有稳定入口；上游和图谱 SHA 逐一复算。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **19.0** | 12 条受控关系均写明共性/差异或程序迁移；多文本范围证据采用保守扣 1 分。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | 5 H、5 L 覆盖普通民众、乡土共同体、时代记忆、四类文体及共同鉴赏程序。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 4 项任务均有 canonical 页位、能力动作、成果、评价边界及 KP/EV 入口。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | M0/N/A、双向证据缺口和禁止越级条件清楚，无题型相似性越级。 |
| 前后递进 | 10 | 8 | **10.0** | 缺少双方 accepted 逐边证据时使用有理由的 N/A，未强造递进。 |
| 可读性与检索性 | 5 | 4 | **4.5** | §1.1 全量索引、任务/双维度/关系表、M0、Issue 和版本记录齐全；范围和斜线压缩写法仍需回看上游卡，保守扣 0.5 分。 |
| **合计** | **100** | **88** | **98.5** | **总分及七维单项均达标；R01—R10 全部未触发。** |

## 8. 独立第二复审决定

**决定：`pass`；总分 `98.5/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

`UNIT-X3-U02` v0.2.2/SHA `464bba3a461fdb07f0d4fbcc95157f27c3ebaa4afa59a505c6df29f45214e83f` 通过本轮独立第二复审，可与同一 SHA 的独立主审配对进入 G4。图谱当前仍为 `linted`，本报告不执行状态迁移；图谱、任一上游卡、canonical Artifact、validator、rubric/taxonomy 或 ledger 绑定变化均使本报告失效并须按新 SHA 复审。

## 9. 可复现绑定与报告校验

- 图谱：`work/knowledge/选择性必修下册/units/UNIT-X3-U02.md`；v0.2.2；SHA `464bba3a461fdb07f0d4fbcc95157f27c3ebaa4afa59a505c6df29f45214e83f`。
- accepted 上游 post-SHA：`CARD-X3-U02-01=f0814040c695ef9d65b7ddca2b5d8f837e044f85a597ae7a7bfd58da5b8a91b4`；`CARD-X3-U02-02=1ad573c3d1cfb97876d604970e55129ca18e10e3147c08703bde6f43755c0715`；`CARD-X3-U02-03=a86827411ce824d72546d98c0e2f9a72dad2e6480f6dca828d2159f71d7c9c78`；`CARD-X3-U02-04=c56d5511b1a7cd58efc4ab4827b63bb979a6fac48c4b688f719630c3905c3fa7`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `3d039ba22e89c780673ffe404114b945937939ac7b8321ebfb7b36f1271e93f4`。
- validator：`work/knowledge/_meta/validation_reports/x3_u02_unit_final_pre_review_v022_20260809.json`；run `VAL-20260809-022936+0800`；SHA `0d31570ae63630cbedbdd0313c5b255e8c690a7318e8fb5339e06a8d4201c59e`；`passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。
