---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X2-U03-FINAL-PRIMARY"
deliverable_id: "UNIT-X2-U03"
artifact_version: "0.2.0"
artifact_sha256: "ef198aa567ab0dd31596aee371c763ca4d17e2c6a3bb7f649e277b3d59b1d2dc"
review_round: 1
reviewer: "independent_primary_unit_x2_u03_final"
review_role: "primary"
reviewed_at: "2026-08-08T19:18:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "46ccc5a8a4213e5a1a1c26fd04d709a7bbf40675daf907b996f705ec39ea7a21"
validator_run_id: "VAL-20260808-190644+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "090a949289c3b185b08bbcfb0c3252b19a6dcdd05a0a305fcbc18dbf2cfd76db"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/x2_u03_unit_validation_20260808_g2.json"
validator_archive_report_sha256: "29e0c6bd8e3bc1379bf4277761f0cb83d164c80ff8d01efbc4eca7b5aeb839b0"
validator_result: "passed"
decision: "pass"
---

# UNIT-X2-U03 v0.2.0 独立主审

## 1. 锁定对象、量表与上游门禁

本轮只审当前 `work/knowledge/选择性必修中册/units/UNIT-X2-U03.md`，不复用旧图谱结论，不修改图谱、上游卡、账本或 validator 归档。当前版本包含 KP-001 节点命名收敛为 `CAND-H-X2-U03-001` 的同步修订；采用冻结 `2.0-textbook` 单元图谱量表：总分门槛88，七维门槛22/16/12/12/8/8/4。

| 上游卡 | 版本/ledger状态 | 图谱锁定 post-merge SHA |
|---|---|---|
| `CARD-X2-U03-01` | v0.2.3 / accepted | `0d6a0e46d3a2ec0521eff31d363a63de3b3914336d4a47921756114b05bb5ce4` |
| `CARD-X2-U03-02` | v0.2.4 / accepted | `74459ad46c63cdd78b74c6d4d5434ba8cb157e228f29a38e3435b9498a2f49f6` |
| `CARD-X2-U03-03` | v0.2.4 / accepted | `6ee9e835dded3cb1a47aae0481735d94eb2d9cac63e379ed445ec99d1902b035` |

三张卡的版本、accepted 状态、图谱 §1 SHA 与当前文件实算一致；当前消费4个正文子文本、47个 KP。canonical 包/任务/课标 SHA 均已在图谱 §1 登记并与注册表一致。

## 2. Validator 与结构复算

`VAL-20260808-190644+0800` 为 `passed`，contracts、deliverables、existing_outputs、registry_links、rubrics、taxonomy 均 0 errors，hash verification=true。归档 G2 报告同样已绑定。

人工复算确认：4 H 节点、2 L 节点、5 项任务、5 条单元关系、1 行结构化 M0、前序/后续各1行合法 N/A；47/47 KP 均至少进入一个节点或任务，并有 Card/KP/EV 入口。节点和任务明确区分上游卡研究性解释、单元综合和项目评价，不冒充教材原文。

## 3. 节点、任务、关系与边界核验

- 人文节点 H-001—H-004 覆盖证据边界/历史现场、屈原、苏武、两篇史论；每节点均回链相应 Card/KP/EV，文化议题没有脱离文本另造结论。
- 语言节点 L-001—L-002 覆盖史传/史论文体比较、叙议/对比/铺陈、文言句式、名词作状语、背诵和读写迁移；语言活动与人文节点相互连接。
- 5 项任务均有 canonical 物理页/切分页、能力动作、学习成果、评价证据和上游 KP 回链；任务原文、项目评价、学生产出和外部资料边界分层。
- 5 条关系均为受控“比较/迁移”类型，源/目标、差异或迁移理由和双向 Card/KP/EV 证据可回查。图谱 §1.1 的要求是每个 KP 列至少一个节点/任务入口及直接 EV 回链；KP-005 当前列出 EV-004，而节点 H-003 的 EV-002—011 范围包含 EV-005，故整体回链闭合；若未来需要逐 KP 全证据展开，可把 EV-005补入索引作为可选增强，不构成当前否决。
- 高考栏保持结构化 `N/A | M0 | N/A | N/A`，不把题型相似性升级为 M1—M3；前序/后续在无双方 accepted 目标证据时合法保持 N/A。
- 三张卡均未取得同版教师用书，`edition_match=unknown`；图谱不消费教师用书意见，也不以缺源填补正文解释。课外史料和学生拟写短评均单独标注身份。

## 4. R01—R10 硬性检查

| 代码 | 触发？ | 结论 |
|---|---|---|
| R01 | 否 | 上游四正文、历史人物、史论结论、任务与课标术语均与 canonical/accepted 来源一致。 |
| R02 | 否 | 47/47 KP、4 H/2 L 节点、5 任务和5关系均有可定位 Card/KP/EV 或任务证据；综合解释有充分来源。 |
| R03 | 否 | 上游清单、正文子文本、KP索引、任务、H/L节点、关系、M0、纵向、Issue和覆盖自检齐全。 |
| R04 | 否 | 教材原文、上游研究性解释、单元综合、项目评价、外部材料和教师用书缺源分层。 |
| R05 | 否 | 47/47 KP 至少进入节点或任务且有层级/证据入口；无孤立 KP。 |
| R06 | 否 | 仅保留合法结构化 M0，无未登记真题、答案或评分 Artifact。 |
| R07 | 否 | 3/3 上游卡均为 ledger accepted，版本与图谱 post-merge SHA 一致。 |
| R08 | 否 | 图谱版本、上游版本/SHA、Card/KP/EV/TASK/节点/关系 ID 与数量一致；validator hash verification=true。 |
| R09 | 否 | 使用现行课标任务群名称，未改写或把任务群当固定教法。 |
| R10 | 否 | 未机械铺满核心素养或给单元贴完整学业质量水平标签。 |

## 5. 单元图谱量表评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | 24.5 | 3/3 accepted卡、4/4正文子文本、47/47 KP、5/5任务和节点/任务 EV 入口闭合；KP-005全证据展开属于可选索引增强。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | 19.0 | H/L 节点和5条受控关系有共性、差异与迁移边界；保守扣1分给单元级综合的宽泛表达。 |
| 人文与语言双维度结构 | 15 | 12 | 15.0 | 4 H+2 L覆盖历史议题、文体语言和读写活动，交叉迁移清晰。 |
| 单元任务拆解 | 15 | 12 | 15.0 | 5/5任务有原文定位、能力动作、成果、评价和 KP 回链。 |
| 高考衔接及证据 | 10 | 8 | 10.0 | M0 与不确定性边界明确，未越级映射。 |
| 前后递进 | 10 | 8 | 10.0 | 无双方 accepted 目标时保持 N/A，不以单元顺序强造递进。 |
| 可读性与检索性 | 5 | 4 | 5.0 | 上游清单、47项索引、任务表、节点/关系表、M0、Issue和复算表齐全。 |
| **合计** | **100** | **88** | **98.5** | 总分及各维度门槛均通过。 |

## 6. P0/P1/P2 与决定

| 等级 | 数量 | 说明 |
|---|---:|---|
| P0 | 0 | 无来源伪造、关键事实错误或不可恢复损坏。 |
| P1 | 0 | 上游门禁、覆盖、证据回链、任务、关系、M0/N/A和教师用书边界均闭合。 |
| P2 | 0 | KP-005 的全 EV 展开可作为后续检索增强，但图谱已按“至少一个直接 EV 回链”契约闭合。 |

**主审决定：`pass`。** 当前 v0.2.0/SHA 可进入独立第二复审；二审须绑定同一版本/同一 SHA，且总分差≤5、单维差≤2 后方可进入 G4。若图谱或上游卡变更，必须重算 SHA 并重审。

## 7. 可复现信息

- 图谱：`work/knowledge/选择性必修中册/units/UNIT-X2-U03.md`；v0.2.0；SHA `ef198aa567ab0dd31596aee371c763ca4d17e2c6a3bb7f649e277b3d59b1d2dc`。
- Validator：`VAL-20260808-190644+0800`；latest report SHA `090a949289c3b185b08bbcfb0c3252b19a6dcdd05a0a305fcbc18dbf2cfd76db`；archive G2 `work/knowledge/_meta/validation_reports/archive/x2_u03_unit_validation_20260808_g2.json` SHA `29e0c6bd8e3bc1379bf4277761f0cb83d164c80ff8d01efbc4eca7b5aeb839b0`。
- Ledger SHA `46ccc5a8a4213e5a1a1c26fd04d709a7bbf40675daf907b996f705ec39ea7a21`；rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
