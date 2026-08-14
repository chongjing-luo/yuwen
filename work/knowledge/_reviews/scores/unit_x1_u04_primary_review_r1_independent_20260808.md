---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X1-U04-R1-PRIMARY-INDEPENDENT"
deliverable_id: "UNIT-X1-U04"
artifact_version: "0.2.0"
artifact_sha256: "c2a7ebf19d8681f612a78c146b914a66601a10bdc4abbf04cdef320615226de2"
review_round: 1
reviewer: "independent_primary_u04_r1"
review_role: "primary"
reviewed_at: "2026-08-08T16:10:18+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-160630+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "a337f2f6e7391de8f48fbd29a45a34ab63c56d81631d66805d3ff3dd82c8535a"
validator_result: "passed"
decision: "rework"
---

# UNIT-X1-U04 v0.2.0 独立主审 R1

## 1. 锁定对象与复核范围

- 本轮只审查 `UNIT-X1-U04` v0.2.0，目标文件为 `work/knowledge/选择性必修上册/units/UNIT-X1-U04.md`，当前 SHA 为 `c2a7ebf19d8681f612a78c146b914a66601a10bdc4abbf04cdef320615226de2`；未修改正文。
- 复核材料为该版本正文、`CARD-X1-U04-01` 当前 `accepted` 卡、教材专题 canonical artifact、现行课标 artifact 和指定 validator；不把旧版本评审结论作为本轮证据。

| 上游卡 | 版本/状态 | 当前 SHA-256 |
|---|---|---|
| `CARD-X1-U04-01` | 0.3.0 / accepted | `0a500cb3543974c6ac3d7cde61e9af0d09f56115bcef510b913ff836d022aebc` |

专题 canonical artifact 为 `ART-PKG-X1-015-PDF`（SHA `4e6f19fea374f135e0bebda89fe5e8f0e25082c19731e31b8b337f4eed21c6af`），课标为 `ART-CURR-2020-PDF`（SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`）。

## 2. validator 与结构复算

`VAL-20260808-160630+0800` 为 `passed`，contracts、deliverables、existing_outputs、registry_links、rubrics、taxonomy 六类检查均为 0 errors，且 hash verification 为 true。机器检查不能替代下列语义复核。

- 上游卡 1/1、专题正文子文本 1/1、单元任务 3/3、KP 13/13；§1.1 的完整连续 KP-ID 均可在上游卡解析。
- 人文节点 4 个、语言节点 6 个，REL 6 条且 REL-ID 唯一；关系值为 `比较/深化/组成/迁移`，均在冻结受控词表内。
- 展开 §3—§5 的 KP 来源后，13/13 KP 至少进入 H/L 节点或关系；M0 行首列为结构化 `N/A`，前序/后续均在无双方 accepted KP/EV 时保持 `N/A`。

## 3. Claim—Evidence 与 canonical 语义核验

- H-001 至 H-004 覆盖谬误识别与传播责任、袁滋/过于执的“线索准确—推理有效性”边界、虚拟论敌与公共表达、文学反常表达与逻辑辨析边界。当前版本已明确熊友兰是被过于执误判的对象，也未把两案写成“相同线索”。
- L-001 至 L-006 覆盖谬误四类、前提—推理—结论结构、隐含前提、排除/反证/归谬法、虚拟论敌和“逻辑链—辩论—驳论文”迁移；各节点均有 Card/KP/EV 回链。
- 绝大多数任务短引与 `ART-PKG-X1-015-PDF` 可命中：任务1第一条推理原文、任务2隐含前提句、任务3议论文章/辩论/800字驳论文均可定位。`“使用间接论证——排除法、反证法和归谬法……”` 的省略号可解释为省略后半句，前段连续 substring 命中。
- **发现任务1第二条教材原文短引不命中 canonical**：图谱 §2（当前文件第41行）写为 `“辨析下列说法中的逻辑错误。”`；`ART-PKG-X1-015-PDF` 规范物理页100、切分页3的原文是 `“任务2：辨析日常语言表达中的逻辑错误。”`。图谱所引“下列说法”并不存在于该 canonical span，不能以页码定位为逐字引文。
- 另一个需一并校正的 exact-span 细节是图谱任务2写 `“在论证中引入虚拟论敌”`，canonical 物理页103、切分页6的标题为 `“在论证中引入‘虚拟论敌’”`；若保留教材原文短引，应保留内层引号，或明确将其改为不带引号的项目标签。

## 4. 硬性否决项

| 代码 | 触发？ | 证据/说明 |
|---|---|---|
| R01 | 否 | 题名、逻辑术语、袁滋/过于执主体、熊友兰被误判、四类谬误、任务和课标版本均与 canonical/accepted 卡一致。 |
| R02 | **是** | §2 将不存在于 canonical 的 `“辨析下列说法中的逻辑错误。”` 标为教材原文短引；任务2另有内层引号丢失的 exact-span 问题。至少一条 Q 引文不可逐字定位，必须升版修复并重新双审。 |
| R03 | 否 | 卡清单、子文本、任务、H/L 节点、REL、M0、前后序、Issue 和覆盖复算模块齐全。 |
| R04 | 否 | 教材栏目、项目评价、教师用书缺源、高考 M0 与项目建议边界分层；§8.1 明确无独立学习提示。 |
| R05 | 否 | 上游 13 个 KP 均有合法主维度、类型、层级、理由、证据和置信状态；图谱仅回链，不重写为无证 KP。 |
| R06 | 否 | 高考侧仅为结构化 M0，未引用未登记真题或宣称直接衔接。 |
| R07 | 否 | 唯一上游卡为 ledger `accepted`，版本和 SHA 与图谱 §1 一致。 |
| R08 | 否 | 当前文件版本、上游版本/SHA、13 KP、6 REL 及 Card/KP/EV/TASK/CAND ID 一致；本轮缺陷是 Q 短引内容，不是 ID/版本断链。 |
| R09 | 否 | 使用现行课标“语言积累、梳理与探究”及对应核心素养，未改写任务群或当作固定课型。 |
| R10 | 否 | 仅对接语言建构与运用、思维发展与提升，未机械铺满四素养，也未消费学业质量等级。 |

## 5. 七维评分（诊断性，不能抵消 R02）

| 维度 | 权重 | 单项门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 1/1 accepted 卡、1/1 子文本、13/13 KP、3/3 任务；无重漏。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **20.0** | 4 H + 6 L 节点和 6 条受控关系均有文本特异性证据；两案主体/线索边界正确。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | H/L 结构完整，逻辑、推理、论证、虚拟论敌和公共表达均有交叉回链。 |
| 单元任务拆解 | 15 | 12 | **10.0** | 三任务的动作、成果和页码完整，但教材原文短引检查点因任务1第二条 Q 不可定位而不通过。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | 合法 M0，未越级映射；N/A 理由和解锁条件完整。 |
| 前后递进 | 10 | 8 | **10.0** | 无双方 accepted 逐边证据时保持 N/A，未虚构递进。 |
| 可读性与检索性 | 5 | 4 | **5.0** | §1.1、§9 索引、稳定 ID、REL 和 Issue 入口齐全。 |
| **合计** | **100** | **88** | **95.0** | 总分虽超过 88，但 R02 和 P1 仍阻断 G4。 |

## 6. P0/P1/P2 与决定

| 等级 | 数量 | 说明 |
|---|---:|---|
| P0 | 0 | 无关键事实倒置、来源造假、上游依赖断裂或不可恢复错误。 |
| P1 | **1** | `P1-UNIT-X1-U04-TASK-Q-EXACT-SPAN`：任务1第二条教材原文短引不在 `ART-PKG-X1-015-PDF` canonical；任务2标题内引号丢失应在同一修订中校正。 |
| P2 | 0 | 未发现独立于该 Q 引文缺陷的非核心问题。 |

**主审决定：`rework`。** 生产者应至少将任务1第二条短引改为 canonical 的 `“辨析日常语言表达中的逻辑错误。”`（或完整保留“任务2：”），并修正/明确任务2“虚拟论敌”的内层引号；升版、重算 SHA、复跑 validator 后，须对新 SHA 从零进行主审和独立二审。旧 v0.2.0 评审在内容修改后全部失效。

## 7. 可复现信息

- 被评版本/哈希：`UNIT-X1-U04 v0.2.0 / c2a7ebf19d8681f612a78c146b914a66601a10bdc4abbf04cdef320615226de2`
- validator：`VAL-20260808-160630+0800`；报告 SHA `a337f2f6e7391de8f48fbd29a45a34ab63c56d81631d66805d3ff3dd82c8535a`
- 量表：`2.0-textbook`；rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`
- taxonomy SHA：`13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`
