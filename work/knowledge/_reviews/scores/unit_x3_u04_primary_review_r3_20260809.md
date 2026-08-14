---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X3-U04-R3-PRIMARY-INDEPENDENT"
deliverable_id: "UNIT-X3-U04"
artifact_version: "0.2.7"
artifact_sha256: "07aafd5068ef4eeaaebb66278edce6fd2e7c810cfc09e87e08b3a898a462f720"
review_round: 3
reviewer: "independent_primary_unit_x3_u04_r3"
review_role: "primary"
reviewed_at: "2026-08-09T02:15:56+08:00"
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
report_sha256: "f67be1667c22bde2865a0c00e209393972ef51023d6dbf301570d6ec5bef0eb2"
---

# UNIT-X3-U04 v0.2.7 独立主审 R3

## 1. 锁定对象与上游门禁

本轮从当前快照重新独立复核 U04 单元图谱，不复用 v0.2.6 结论，不修改图谱、上游卡、ledger、validator 或状态迁移。采用冻结的 `2.0-textbook` 单元图谱量表：总分门槛 88，七维最低分 `22/16/12/12/8/8/4`。

| 对象 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修下册/units/UNIT-X3-U04.md`；v0.2.7；SHA `07aafd5068ef4eeaaebb66278edce6fd2e7c810cfc09e87e08b3a898a462f720`；状态 `linted` |
| 上游卡01 | `CARD-X3-U04-01` v0.2.1，ledger `accepted`，post SHA `7919991d1737f5cbdcca0c67341aa42119a22a6f5b6cb240274bda3f12b9c15b` |
| 上游卡02 | `CARD-X3-U04-02` v0.2.1，ledger `accepted`，post SHA `3864d8bdd7b533d23355c4259602d4d91d2ab7d7fa49b10aaa71d78a2ae982f0` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `207f842128b29dcbe3cffc261688ff54db2d0a65c366102abcdda21218da6a5b`；U04 条目为 v0.2.7/`linted`，路径、source_ids、upstream_card_ids 与图谱一致 |
| validator | `VAL-20260809-021456+0800`；`work/knowledge/_meta/validation_reports/x3_u04_unit_final_pre_review_v027_20260809.json`；SHA `9b11c0853be1b61db3d61a896659d4dcd92c88e4678fbed3e94fcbed152a0baa`；`passed`、0 errors、`hash_verification=true` |

两张上游卡均为当前 ledger 的 `accepted` 版本，且图谱 §1 中的两个 post SHA 与 ledger、实际文件 SHA 一致。图谱仅声明并消费已登记的任务包和现行 2020 修订课标；未将教师用书、未登记真题或网络解析当作上游事实。

## 2. 结构、覆盖与双维度复核

- 上游卡 KP 数量为 `24+30=54`；§1.1 逐一列出两卡全部稳定 `KP-CARD-X3-U04-*`，独立展开为 `54/54`，无漏项、重复或跨卡混淆。两卡综合入口均列明 H-U04-05/L-U04-05；此前仅列索引的 9 个 KP 已进入语义节点或关系。
- 5 个人文节点和 5 个语言节点均有稳定 ID、来源 Card/KP 与 EV 回链。人文线覆盖求真、理论—事实、科学史文化传统、探索者位置和文章/模型谱系；语言线覆盖科学论著论证链、科学史叙述链、准确与通俗表达、读写修订程序和课标/学业质量边界。
- 6 个单元任务均有 `SRC-PKG-X3-018`、`ART-PKG-X3-018-PDF` 及物理页 114—115 定位，写出能力动作、学习成果、评价证据和对应 KP/EV；任务评价设计没有冒充教材原文。
- 14 条 `REL-UNIT-X3-U04-*` 均有稳定 ID、受控 taxonomy 类型、双方 KP 和 EV 入口。REL-09 目标为史料辨析 `KP-CARD-X3-U04-02-021`，并挂 `EV-CARD-X3-U04-02-005`、`012`；REL-14 的目标 KP-006—016 与 EV-003—016 范围一致。v0.2.7 的 REL-03 进一步将自然选择的渐进变异机制与盖天/浑天的实践—结构讨论分开表述，并明确不可混同。

## 3. 综合关系、M0 与边界复核

14 条关系的受控类型计数为：比较 7、迁移 3、前提 2、组成 1、例证 1；未发现 taxonomy 之外的关系类型。各关系均写出共性、差异或迁移/前提理由，并以双方 KP/EV 回链。REL-03 现在明确：自然选择强调微小、连续变异的逐步积累；盖天/浑天段讨论观测、历法等实践效用及宇宙结构解释局限，二者只能作受边界的比较，不能混同为同一机制。REL-05/07 是阅读程序迁移，不是教材顺序；REL-09 落到史料原话—作者转述—评价词的 KP-021，而非多媒介 KP-025；REL-10/11 的主题比较保留语境边界；REL-12 是任务成果链的组成关系；REL-13/14 只作文本组织层面的比较/前提判断。

高考栏保持结构化 `N/A | M0 | N/A`，明确尚未登记“真题题文—答案/评分—教材 KP”逐小问闭合证据，未将科学说明、科学史、长句、论证或多媒介的一般题型相似性升级为 M1—M3。前序/后续递进均保留带 `na_reason` 的 N/A；教师用书维持 `edition_match=unknown`，不消费缺失版本意见。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两张 accepted 卡、三篇正文及导语范围、U04 任务和课标边界均可回到 canonical 来源；REL-03 的比较边界已明确，未发现关键事实错误或张冠李戴。 |
| R02 | 否 | 54/54 KP、5 H、5 L、6 TASK、14 REL 均有适配的 Card/KP/EV 或任务来源；人文解释和关系陈述保留多处文本证据与语境限制。REL-03、REL-09 的目标与证据已按语义对齐。 |
| R03 | 否 | 上游清单、逐项 KP 索引、任务拆解、双维度节点、关系、M0、纵向 N/A、Issue 和自检模块齐全。 |
| R04 | 否 | 教材正文/学习提示、卡片解释、任务原文、课标边界、项目评价和单元综合分层清楚；未把研究解释或外部材料冒充规范结论。 |
| R05 | 否 | 两卡全部 54 个 KP 均被索引并进入节点、任务或关系入口；新增 9 个 KP 已有语义节点/关系承载，无孤立 KP。 |
| R06 | 否 | 高考仅保留合法结构化 M0，未引用未登记真题、答案或评分资料，也未建立越级 M1—M3 边。 |
| R07 | 否 | 两张上游卡均为 `accepted`，图谱 §1 post SHA 与当前卡文件和 ledger 一致；任务包、课标 artifact 已登记并验证。 |
| R08 | 否 | 图谱版本、路径、卡/KP/EV/TASK/REL ID、数量、SHA、ledger 条目和 validator 绑定一致；REL-03、REL-09 与 REL-14 的 KP/EV 范围均已同步。 |
| R09 | 否 | 使用现行 2020 修订课标的任务群 12、学业质量 4-3 定位，未改写任务群名称或把课标定位固化为教法/达成水平。 |
| R10 | 否 | 人文与语言双维度按三篇文本和 U04 任务实际展开，未机械铺满四项核心素养，也未将学业质量水平当作题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键覆盖缺失、非法关系类型、未验收上游、M0 越级、教师用书混入、版本漂移或上游 SHA 断链。 |
| P2 | 0 | 未发现影响检索和复核的非阻断缺陷；REL-03 的比较边界、REL-09 目标/证据、REL-14 范围、计数和新增 KP 入口均已对齐。 |

## 6. 单元图谱诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 2/2 accepted 卡、54/54 KP、6/6 任务、5 H/5 L 和 14/14 REL 均有稳定入口；§1.1 入口与新增 9 KP 已对齐。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **19.0** | 14 条关系均有受控类型、共性/差异或迁移理由和双方证据；REL-03 的机制边界、REL-09 的目标/证据已精确化，其他宽范围引用仍采取保守扣 1 分。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | 5 个 H 与 5 个 L 节点覆盖科学精神、模型史、论证结构、表达媒介、修订程序和课标边界，均可回链 Card/KP/EV。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 6 项任务均有物理页 114—115、能力动作、成果、评价边界和上游 KP/EV 入口。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | `N/A | M0 | N/A`、双向证据缺口和禁止越级条件写明；未以题型相似性制造映射。 |
| 前后递进 | 10 | 8 | **10.0** | 缺少双方 accepted 逐边证据时使用有理由的前/后 N/A，未强造跨单元关系。 |
| 可读性与检索性 | 5 | 4 | **5.0** | §1.1 完整索引、任务/双维度/关系表、M0、Issue 和版本自检齐全；REL-03/09/14 修订后的范围可直接复核。 |
| **合计** | **100** | **88** | **99.0** | **总分及七维单项均达标；R01—R10 全部未触发。** |

## 7. 独立主审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `UNIT-X3-U04` v0.2.7/SHA `07aafd5068ef4eeaaebb66278edce6fd2e7c810cfc09e87e08b3a898a462f720` 通过独立主审，可进入同一 SHA 的独立第二复审。本报告只闭合主审，不写回 ledger 或执行 `accepted` 状态迁移；图谱、任一上游卡、canonical artifact、validator、rubric/taxonomy 或版本绑定变化时，本报告失效并须按新 SHA 全量复审。

## 8. 可复现绑定与报告校验

- 图谱：`work/knowledge/选择性必修下册/units/UNIT-X3-U04.md`；v0.2.7；SHA `07aafd5068ef4eeaaebb66278edce6fd2e7c810cfc09e87e08b3a898a462f720`。
- accepted 上游 post SHA：`CARD-X3-U04-01=7919991d1737f5cbdcca0c67341aa42119a22a6f5b6cb240274bda3f12b9c15b`；`CARD-X3-U04-02=3864d8bdd7b533d23355c4259602d4d91d2ab7d7fa49b10aaa71d78a2ae982f0`。
- canonical 课标 artifact：`ART-CURR-2020-PDF`，SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；U04 任务 artifact `ART-PKG-X3-018-PDF` 已登记并验证。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `207f842128b29dcbe3cffc261688ff54db2d0a65c366102abcdda21218da6a5b`。
- validator：`work/knowledge/_meta/validation_reports/x3_u04_unit_final_pre_review_v027_20260809.json`；run `VAL-20260809-021456+0800`；SHA `9b11c0853be1b61db3d61a896659d4dcd92c88e4678fbed3e94fcbed152a0baa`；`passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。
