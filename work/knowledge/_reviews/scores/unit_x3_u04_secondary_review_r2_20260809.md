---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X3-U04-SECONDARY-R2"
deliverable_id: "UNIT-X3-U04"
artifact_version: "0.2.7"
artifact_sha256: "07aafd5068ef4eeaaebb66278edce6fd2e7c810cfc09e87e08b3a898a462f720"
review_round: 2
reviewer: "independent_secondary_unit_x3_u04_r2"
review_role: "secondary"
reviewed_at: "2026-08-09T02:16:01+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "207f842128b29dcbe3cffc261688ff54db2d0a65c366102abcdda21218da6a5b"
validator_run_id: "VAL-20260809-021456+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u04_unit_final_pre_review_v027_20260809.json"
validator_report_sha256: "9b11c0853be1b61db3d61a896659d4dcd92c88e4678fbed3e94fcbed152a0baa"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "6318f8d8d49e9dc1a82bfa7fa36d7ff802b76651a16df499b6c1aa9f3c50c70d"
---

# UNIT-X3-U04 v0.2.7 独立第二复审 R2

## 1. 输入锁定与独立性

本轮只依据 v0.2.7 图谱、两张当前 `accepted` 上游卡、冻结的 `2.0-textbook` rubric/taxonomy、共享 ledger 和指定 validator 独立复核；不复用旧 SHA 的结论，不修改图谱、上游卡、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修下册/units/UNIT-X3-U04.md`；v0.2.7；SHA `07aafd5068ef4eeaaebb66278edce6fd2e7c810cfc09e87e08b3a898a462f720`；状态 `linted` |
| `CARD-X3-U04-01` | v0.2.1；`accepted`；SHA `7919991d1737f5cbdcca0c67341aa42119a22a6f5b6cb240274bda3f12b9c15b` |
| `CARD-X3-U04-02` | v0.2.1；`accepted`；SHA `3864d8bdd7b533d23355c4259602d4d91d2ab7d7fa49b10aaa71d78a2ae982f0` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `207f842128b29dcbe3cffc261688ff54db2d0a65c366102abcdda21218da6a5b`；图谱条目 v0.2.7/`linted`，上游两卡为 `accepted` |
| validator | `VAL-20260809-021456+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `9b11c0853be1b61db3d61a896659d4dcd92c88e4678fbed3e94fcbed152a0baa` |

图谱文件、ledger 最后迁移记录和两张上游卡的实际文件 SHA 均逐一复算一致。validator 的外部真题/教师用书等 warning 是项目边界提示，不构成本图谱错误。

## 2. 覆盖、结构与回链复核

- 两张 accepted 卡的 KP 数为 `24+30=54`。对图谱中的完整 ID、范围写法和斜线压缩写法独立展开后，语义区（任务、双维度节点、关系）覆盖 `54/54` KP；无未知、重复或跨卡混淆。此前补入的 9 个 KP（01-001/003/023/024、02-001/003/004/005/030）均有节点或关系承载，不再只是索引项。
- 图谱包含 5 个人文节点、5 个语言节点、6 个单元任务和 14 条关系；所有节点和任务均能回查 Card/KP/EV 或 canonical 任务包。关系 `REL-UNIT-X3-U04-09` 已使用与“史料原话—作者转述—评价词”相符的目标 `KP-CARD-X3-U04-02-021` 及 `EV-005/012`；`REL-14` 的源 KP-003—005、目标 KP-006—016 与 EV-003—016 范围一致。
- 14 个 `REL-ID` 唯一，关系类型均属于 taxonomy 允许集合：`比较/迁移/前提/组成/例证`。v0.2.7 的 REL-03 已把自然选择的渐进变异机制与盖天/浑天的实践—结构讨论分开表述，未再把“局限”错误归到两文共同结论。
- 6 项任务均定位到 `SRC-PKG-X3-018`/`ART-PKG-X3-018-PDF` 物理页 114—115，并给出能力动作、成果和评价证据；项目化评价要求与教材任务原文分层。

## 3. 双维度、综合关系与证据边界

人文线覆盖科学求真、理论—事实、科学史文化传统、探索者位置和文章/模型谱系；语言线覆盖科学论著论证、科学史叙述、准确与通俗表达、读写修订程序及课标/学业质量边界。节点和关系均保留正文、学习提示、任务与课标的来源层级，没有把单元综合改写成教材新增事实。

关系表逐条给出源/目标 KP、受控关系、共性或差异及 EV 入口。`REL-05/07` 是阅读程序迁移，`REL-09` 是科学表达与史料辨析的比较，`REL-10/11` 保留主题和认识程序的语境差异，`REL-12` 只表示任务成果链的组成，`REL-13/14` 只作导语分组和模型谱系的文本组织关系。没有把科学论著与科学史的材料、历史对象或结论强行等同。

## 4. 高考、纵向关系与教师用书边界

- 高考栏保持结构化 `N/A | M0 | N/A`，明确尚未登记可逐小问核验的真题题文—答案/评分—教材 KP 闭合证据；不把科学说明、科学史、长句、论证或多媒介的一般题型相似性升级为 M1—M3。
- 前、后单元均为带 `na_reason` 的 `N/A`：当前没有双方 `accepted` KP/EV 的逐边核验，不以单元排列或主题相似性臆造递进。
- 教师用书为 `edition_match=unknown`；图谱不消费未登记教师用书意见、网络解析或外部科学史考证。

## 5. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两张 accepted 卡、三篇正文/导语、任务和课标边界均可回到已登记来源，未见关键事实错误。 |
| R02 | 否 | 54/54 KP、5 H、5 L、6 TASK、14 REL 均有 Card/KP/EV 或任务来源；关系证据和语境边界足以支撑单元级综合。 |
| R03 | 否 | 上游清单、全量 KP 索引、任务、双维度节点、关系、M0、纵向 N/A、Issue 和版本记录齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标、项目评价、外部材料边界和单元综合分层清楚。 |
| R05 | 否 | 54/54 KP 均保留上游主维度、类型、层级和 EV 入口，并进入语义节点、任务或关系。 |
| R06 | 否 | 高考严格保持 M0；没有未登记真题、答案/评分资料或越级映射。 |
| R07 | 否 | 两张上游卡均为 `accepted`，且实际文件 SHA、图谱 §1 和 ledger G4 post-SHA 一致。 |
| R08 | 否 | 图谱/卡/KP/EV/TASK/REL 的 ID、数量、版本、路径、SHA 和状态链闭合。 |
| R09 | 否 | 使用现行课标任务群 12 和学业质量 4-3 的正确定位，未改写任务群名称或把课标等级当作达成标签。 |
| R10 | 否 | 人文/语言双线按文本与任务需要展开，未机械铺满核心素养，也未把学业质量水平当作题目难度。 |

## 6. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键覆盖缺失、非法关系类型、未验收上游、M0 越级、教师用书混入、版本漂移或 SHA 断链。 |
| P2 | 0 | v0.2.7 已关闭上一轮发现的 REL-09 目标/证据错配和 REL-03 语义过宽问题；当前未发现新的非阻断缺陷。 |

## 7. `2.0-textbook` unit_graph 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 2/2 accepted 卡、54/54 KP、6/6 任务、5 H/5 L、14/14 REL 均有稳定入口；上游和图谱 SHA 逐一复算。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **19.0** | 14 条受控关系均写明共性/差异或迁移理由；REL-03、REL-09 和 REL-14 的语义/范围修订均已闭合，宽范围证据表达保守扣 1 分。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | 5 H、5 L 覆盖科学精神、模型史、论证结构、表达媒介、修订程序和课标边界。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 6 项任务均有 canonical 页位、能力动作、成果、评价边界及 KP/EV 入口。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | M0/N/A、双向证据缺口和禁止越级条件清楚，无题型相似性越级。 |
| 前后递进 | 10 | 8 | **10.0** | 缺少双方 accepted 逐边证据时使用有理由的 N/A，未强造递进。 |
| 可读性与检索性 | 5 | 4 | **4.5** | §1.1 全量索引、任务/双维度/关系表、M0、Issue 和版本记录齐全；范围和斜线压缩写法仍需回看上游卡，保守扣 0.5 分。 |
| **合计** | **100** | **88** | **98.5** | **总分及七维单项均达标；R01—R10 全部未触发。** |

## 8. 独立第二复审决定

**决定：`pass`；总分 `98.5/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

`UNIT-X3-U04` v0.2.7/SHA `07aafd5068ef4eeaaebb66278edce6fd2e7c810cfc09e87e08b3a898a462f720` 通过本轮独立第二复审，可与同一 SHA 的独立主审配对进入 G4。图谱当前仍为 `linted`，本报告不执行状态迁移；图谱、任一上游卡、canonical Artifact、validator、rubric/taxonomy 或 ledger 绑定变化均使本报告失效并须按新 SHA 复审。

## 9. 可复现绑定与报告校验

- 图谱：`work/knowledge/选择性必修下册/units/UNIT-X3-U04.md`；v0.2.7；SHA `07aafd5068ef4eeaaebb66278edce6fd2e7c810cfc09e87e08b3a898a462f720`。
- accepted 上游 post-SHA：`CARD-X3-U04-01=7919991d1737f5cbdcca0c67341aa42119a22a6f5b6cb240274bda3f12b9c15b`；`CARD-X3-U04-02=3864d8bdd7b533d23355c4259602d4d91d2ab7d7fa49b10aaa71d78a2ae982f0`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `207f842128b29dcbe3cffc261688ff54db2d0a65c366102abcdda21218da6a5b`。
- validator：`work/knowledge/_meta/validation_reports/x3_u04_unit_final_pre_review_v027_20260809.json`；run `VAL-20260809-021456+0800`；SHA `9b11c0853be1b61db3d61a896659d4dcd92c88e4678fbed3e94fcbed152a0baa`；`passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。
