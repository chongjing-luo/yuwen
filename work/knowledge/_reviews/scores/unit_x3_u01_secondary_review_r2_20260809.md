---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X3-U01-SECONDARY-R2"
deliverable_id: "UNIT-X3-U01"
artifact_version: "0.2.2"
artifact_sha256: "34e6f0fed8a102843c81524f55add86917be584b2ad647a47358d16602ae86ab"
review_round: 2
reviewer: "independent_secondary_unit_x3_u01_r2"
review_role: "secondary"
reviewed_at: "2026-08-09T02:24:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "551802207634ae5eaaaf5de058362bd973b321d08be4168bcc008c6229433957"
validator_run_id: "VAL-20260809-022241+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u01_unit_final_pre_review_v022_20260809.json"
validator_report_sha256: "cd5998129e0da0b1ef85c4368fbed0e71b946d5217696e4c540da7cbaae9bdae"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "98d1c0ba91cbaa62faf9b96ef5a9ec92dee6e409c2bc43ae65b436468ebc6c34"
---

# UNIT-X3-U01 v0.2.2 独立第二复审 R2

## 1. 输入锁定与独立性

本轮只依据 v0.2.2 图谱、四张当前 `accepted` 上游卡、冻结的 `2.0-textbook` rubric/taxonomy、共享 ledger 和指定 validator 独立复核；不复用旧 SHA 的结论，不修改图谱、上游卡、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修下册/units/UNIT-X3-U01.md`；v0.2.2；SHA `34e6f0fed8a102843c81524f55add86917be584b2ad647a47358d16602ae86ab`；状态 `linted` |
| `CARD-X3-U01-01` | v0.2.1；`accepted`；SHA `48b418867024c97179db6f13a1e120938197d97bfe0db9467db24d531f5df9d6` |
| `CARD-X3-U01-02` | v0.2.2；`accepted`；SHA `6b133b93f37ddbd22dc5e21eed7bdb9eb7c0bc6d923e24b7c8e3ae74fb4da0a9` |
| `CARD-X3-U01-03` | v0.2.5；`accepted`；SHA `50e07df1126e83534832b704e270baa0e2ff9ae679cfab54d7022dd4e53c0873` |
| `CARD-X3-U01-04` | v0.2.5；`accepted`；SHA `b274580dde4e276d2b4fcce3ec003761451b8cc853af7e212dcb3506e54dd49c` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `551802207634ae5eaaaf5de058362bd973b321d08be4168bcc008c6229433957`；图谱条目 v0.2.2/`linted`，四卡均为 `accepted` |
| validator | `VAL-20260809-022241+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `cd5998129e0da0b1ef85c4368fbed0e71b946d5217696e4c540da7cbaae9bdae` |

图谱文件、ledger 最后迁移记录和四张上游卡的实际文件 SHA 均逐一复算一致。validator 的外部真题、教师用书等 warning 是项目边界提示，不构成本图谱错误。

## 2. 覆盖、结构与回链复核

- 四张 accepted 卡的 KP 数为 `16+16+16+17=65`。对图谱中的完整 ID、范围写法和斜线压缩写法独立展开后，任务、双维度节点和关系语义区覆盖 `65/65` KP；无漏项、重复或跨卡混淆。此前仅列索引的 `KP-CARD-X3-U01-02-001` 已进入 `L-U01-06`，任务二中的 `KP-01-016/KP-02-016` 也已改为完整稳定 ID。
- 图谱包含 6 个人文节点、6 个语言节点、4 个单元任务和 11 条关系；所有节点和任务均能回查 Card/KP/EV 或 canonical 任务包。关系均有稳定 `REL-ID`、双方 KP 和 EV 入口。
- 11 个关系类型均属于 taxonomy 允许集合：`比较/迁移/组成/例证`。关系中的婚恋叙事、主体价值、山河/城市空间、盛衰记忆和鉴赏程序迁移均保留文本语境差异，不把开放的文学解释改写成单一结论。
- 4 项任务均定位到 `SRC-PKG-X3-005`/`ART-PKG-X3-005-PDF` 物理页 25—26，并给出能力动作、成果和评价证据；项目化的比较表、研讨、鉴赏写作和合作编集要求与教材任务原文分层。

## 3. 双维度、综合关系与证据边界

人文线覆盖诗歌源流、婚恋悲剧、人格操守与忧患、山河城市空间、繁华与盛衰及当代阅读责任；语言线覆盖体式、比兴/意象、叙事对话、复沓典故/声音、鉴赏表达程序及文言诗歌语言梳理。各节点均保留上游 Card/KP/EV 入口，未把项目建议冒充教材原文。

关系表逐条给出源/目标 KP、受控关系、共性或差异及证据。`REL-01/03/04/05/06/07/10` 是受语境约束的文学比较，`REL-02/08/09` 是鉴赏/语言方法迁移，`REL-11` 只表示任务成果链的组成。证据范围覆盖相应两端，未发现关系 ID、类型或目标 KP 断链。

## 4. 高考、纵向关系与教师用书边界

- 高考栏保持结构化 `N/A | M0 | N/A`，明确尚未登记可逐小问核验的真题题文—答案/评分—教材 KP 闭合证据；不把古诗词情感、意象、典故、比较或鉴赏的一般题型相似性升级为 M1—M3。
- 前、后单元均为带 `na_reason` 的 `N/A`：当前没有双方 `accepted` KP/EV 的逐边核验，不以单元排列或主题相似性臆造递进。
- 教师用书为 `edition_match=unknown`；图谱不消费未登记教师用书意见、网络解析或外部文学史考证。

## 5. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 四张 accepted 卡、七篇诗歌/导语、任务和课标边界均可回到已登记来源，未见关键事实错误。 |
| R02 | 否 | 65/65 KP、6 H、6 L、4 TASK、11 REL 均有适配 Card/KP/EV 或任务来源；文学综合保留文本证据与语境限制。 |
| R03 | 否 | 上游清单、全量 KP 索引、任务、双维度节点、关系、M0、纵向 N/A、Issue 和版本记录齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标、项目评价、外部材料边界和单元综合分层清楚。 |
| R05 | 否 | 65/65 KP 均保留上游主维度、类型、层级和 EV 入口，并进入语义节点、任务或关系。 |
| R06 | 否 | 高考严格保持 M0；没有未登记真题、答案/评分资料或越级映射。 |
| R07 | 否 | 四张上游卡均为 `accepted`，且实际文件 SHA、图谱 §1 和 ledger post-SHA 一致。 |
| R08 | 否 | 图谱/卡/KP/EV/TASK/REL 的 ID、数量、版本、路径、SHA 和状态链闭合；任务二裸 KP 已在 v0.2.2 修正。 |
| R09 | 否 | 使用现行课标任务群 5 等已登记定位和学业质量 4-3 边界，未改写任务群名称或把课标等级当作达成标签。 |
| R10 | 否 | 人文/语言双线按七篇诗歌和 U01 任务需要展开，未机械铺满核心素养，也未把学业质量水平当作题目难度。 |

## 6. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键覆盖缺失、非法关系类型、未验收上游、M0 越级、教师用书混入、版本漂移或 SHA 断链。 |
| P2 | 0 | v0.2.2 已关闭裸 KP 和 KP-02-001 语义孤立问题；当前未发现新的非阻断缺陷。 |

## 7. `2.0-textbook` unit_graph 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 4/4 accepted 卡、65/65 KP、4/4 任务、6 H/6 L、11/11 REL 均有稳定入口；上游和图谱 SHA 逐一复算。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **19.0** | 11 条受控关系均写明共性/差异、例证或程序迁移；证据范围对多文本综合采用保守扣 1 分。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | 6 H、6 L 覆盖诗歌源流、婚恋/历史记忆、体式、意象、叙事和鉴赏表达。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 4 项任务均有 canonical 页位、能力动作、成果、评价边界及 KP/EV 入口。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | M0/N/A、双向证据缺口和禁止越级条件清楚，无题型相似性越级。 |
| 前后递进 | 10 | 8 | **10.0** | 缺少双方 accepted 逐边证据时使用有理由的 N/A，未强造递进。 |
| 可读性与检索性 | 5 | 4 | **4.5** | §1.1 全量索引、任务/双维度/关系表、M0、Issue 和版本记录齐全；范围和斜线压缩写法仍需回看上游卡，保守扣 0.5 分。 |
| **合计** | **100** | **88** | **98.5** | **总分及七维单项均达标；R01—R10 全部未触发。** |

## 8. 独立第二复审决定

**决定：`pass`；总分 `98.5/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

`UNIT-X3-U01` v0.2.2/SHA `34e6f0fed8a102843c81524f55add86917be584b2ad647a47358d16602ae86ab` 通过本轮独立第二复审，可与同一 SHA 的独立主审配对进入 G4。图谱当前仍为 `linted`，本报告不执行状态迁移；图谱、任一上游卡、canonical Artifact、validator、rubric/taxonomy 或 ledger 绑定变化均使本报告失效并须按新 SHA 复审。

## 9. 可复现绑定与报告校验

- 图谱：`work/knowledge/选择性必修下册/units/UNIT-X3-U01.md`；v0.2.2；SHA `34e6f0fed8a102843c81524f55add86917be584b2ad647a47358d16602ae86ab`。
- accepted 上游 post-SHA：`CARD-X3-U01-01=48b418867024c97179db6f13a1e120938197d97bfe0db9467db24d531f5df9d6`；`CARD-X3-U01-02=6b133b93f37ddbd22dc5e21eed7bdb9eb7c0bc6d923e24b7c8e3ae74fb4da0a9`；`CARD-X3-U01-03=50e07df1126e83534832b704e270baa0e2ff9ae679cfab54d7022dd4e53c0873`；`CARD-X3-U01-04=b274580dde4e276d2b4fcce3ec003761451b8cc853af7e212dcb3506e54dd49c`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `551802207634ae5eaaaf5de058362bd973b321d08be4168bcc008c6229433957`。
- validator：`work/knowledge/_meta/validation_reports/x3_u01_unit_final_pre_review_v022_20260809.json`；run `VAL-20260809-022241+0800`；SHA `cd5998129e0da0b1ef85c4368fbed0e71b946d5217696e4c540da7cbaae9bdae`；`passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。
