---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X1-U04-R2-PRIMARY-INDEPENDENT"
deliverable_id: "UNIT-X1-U04"
artifact_version: "0.2.1"
artifact_sha256: "5bb3601eb05962829c65604cecaf4b2a38c2b7a1f98db757db806f17b9013531"
review_round: 2
reviewer: "independent_primary_u04_r2"
review_role: "primary"
reviewed_at: "2026-08-08T16:14:06+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-161305+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "887cf09301f78b0ea5633d306f95c5b8b2134ab9c99e35a3298d949e07818ea3"
validator_result: "passed"
decision: "pass"
---

# UNIT-X1-U04 v0.2.1 独立主审 R2

## 1. 锁定对象与复核范围

- 本轮从当前正文和 canonical/accepted 上游材料重新开始，只绑定 `UNIT-X1-U04` v0.2.1，目标文件为 `work/knowledge/选择性必修上册/units/UNIT-X1-U04.md`，SHA 为 `5bb3601eb05962829c65604cecaf4b2a38c2b7a1f98db757db806f17b9013531`。
- v0.2.1 仅在任务短引和版本记录处有内容变更；本报告不复用 v0.2.0 评审结论。正文未再修改。

| 上游卡 | 版本/状态 | 当前 SHA-256 |
|---|---|---|
| `CARD-X1-U04-01` | 0.3.0 / accepted | `0a500cb3543974c6ac3d7cde61e9af0d09f56115bcef510b913ff836d022aebc` |

专题 canonical artifact 为 `ART-PKG-X1-015-PDF`（SHA `4e6f19fea374f135e0bebda89fe5e8f0e25082c19731e31b8b337f4eed21c6af`），课标为 `ART-CURR-2020-PDF`（SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`）。

## 2. validator 与结构复算

`VAL-20260808-161305+0800` 结果为 `passed`，六类检查均为 0 errors，hash verification 为 true。本轮人工复算：

- 上游卡 1/1、专题正文子文本 1/1、单元任务 3/3、KP 13/13；§1.1 的完整连续 KP-ID 均可在 accepted 卡解析。
- 人文节点 4 个、语言节点 6 个、REL 6 条且 REL-ID 唯一；关系值为 `比较/深化/组成/迁移`，全部在冻结受控词表内。
- 展开 §3—§5 的 KP 来源后，13/13 KP 至少进入 H/L 节点或关系；M0 行首列为结构化 `N/A`，前序/后续在无双方 accepted KP/EV 时保持 `N/A`。
- v0.2.1 版本史、自检和正文 SHA 均已同步，未把本次正文修订写入上游卡或 ledger。

## 3. Claim—Evidence 与 canonical 语义核验

- H-001—H-004 覆盖谬误识别与传播责任、袁滋/过于执的“线索准确—推理有效性”边界、虚拟论敌与公共表达、文学反常表达与逻辑辨析边界。熊友兰仍是被过于执误判的对象，两个案例未被写成相同线索。
- L-001—L-006 覆盖谬误四类、前提—推理—结论结构、隐含前提、排除/反证/归谬法、虚拟论敌和“逻辑链—辩论—驳论文”迁移；各节点均有 Card/KP/EV 回链。
- 任务1第一条推理引文与任务1第二条 `“辨析日常语言表达中的逻辑错误。”` 均逐字命中 `ART-PKG-X1-015-PDF`；任务2隐含前提句逐字命中，间接论证短引的前缀连续命中且 `……` 明示省略后半句；任务2定位说明恢复了 `“虚拟论敌”` 内层引号；任务3三条短引均命中。
- REL-001—006 的两端 KP/任务和证据理由闭合，未将一般“逻辑/议论文”邻接写成跨单元递进；项目评价和 `edition_match=unknown` 保持边界分层。

## 4. 硬性否决项

| 代码 | 触发？ | 证据/说明 |
|---|---|---|
| R01 | 否 | 题名、逻辑术语、袁滋/过于执主体、熊友兰被误判、四类谬误、任务和课标版本均与 canonical/accepted 卡一致。 |
| R02 | 否 | §2 任务 Q 均可在 canonical artifact 定位；任务1短引已改为“辨析日常语言表达中的逻辑错误”，任务2保留“虚拟论敌”内层引号；解释型 Claim 有适配 Card/KP/EV。 |
| R03 | 否 | 卡清单、子文本、任务、H/L 节点、REL、M0、前后序、Issue 和覆盖复算模块齐全。 |
| R04 | 否 | 教材栏目、项目评价、教师用书缺源、高考 M0 与项目建议边界分层；§8.1 明确无独立学习提示。 |
| R05 | 否 | 上游 13 个 KP 均具主维度、受控类型、四层归属、判定理由、有效证据和置信状态。 |
| R06 | 否 | 高考侧仅为结构化 M0，未引用未登记真题或宣称直接衔接。 |
| R07 | 否 | 唯一上游卡为 ledger `accepted`，版本和 SHA 与图谱 §1 一致。 |
| R08 | 否 | 当前 v0.2.1、上游版本/SHA、13 KP、6 REL 及 Card/KP/EV/TASK/CAND ID 一致；版本史明确旧 SHA 失效。 |
| R09 | 否 | 使用现行课标“语言积累、梳理与探究”及对应核心素养，未改写任务群或当作固定课型。 |
| R10 | 否 | 仅对接语言建构与运用、思维发展与提升，未机械铺满四素养，也未消费学业质量等级。 |

## 5. 七维评分

| 维度 | 权重 | 单项门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 1/1 accepted 卡、1/1 子文本、13/13 KP、3/3 任务；无重漏。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **20.0** | 4 H + 6 L 节点与 6 条受控关系均有文本特异性证据，未新增脱证结论。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | H/L 结构完整，逻辑、推理、论证、虚拟论敌和公共表达均有交叉回链。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 三任务均有 canonical 原文短引、规范页码、能力动作、成果和项目评价分层。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | 合法 M0，未越级映射；N/A 理由和解锁条件完整。 |
| 前后递进 | 10 | 8 | **10.0** | 无双方 accepted 逐边证据时保持 N/A，未虚构递进。 |
| 可读性与检索性 | 5 | 4 | **5.0** | §1.1、§9 索引、稳定 ID、REL、Issue 和版本记录齐全。 |
| **合计** | **100** | **88** | **100.0** | 总分及各单项门槛均通过。 |

## 6. P0/P1/P2 与决定

| 等级 | 数量 | 说明 |
|---|---:|---|
| P0 | 0 | 无关键事实错误、来源造假、依赖断裂或不可恢复错误。 |
| P1 | 0 | 任务 Q exact span、13/13 KP、Claim—EV、REL、M0 和版本血缘均已闭合。 |
| P2 | 0 | 未发现独立于已修复引文问题的非核心缺陷。 |

**主审决定：`pass`。** 当前 v0.2.1/SHA 可进入同 SHA 的独立二审；只有在二审总分差≤5、单维差≤2 且 R/P 判断一致后，方可执行 G4。正文再次修改会使本报告失效，须重新计算 SHA 并从零审查。

## 7. 可复现信息

- 被评版本/哈希：`UNIT-X1-U04 v0.2.1 / 5bb3601eb05962829c65604cecaf4b2a38c2b7a1f98db757db806f17b9013531`
- validator：`VAL-20260808-161305+0800`；报告 SHA `887cf09301f78b0ea5633d306f95c5b8b2134ab9c99e35a3298d949e07818ea3`
- 量表：`2.0-textbook`；rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`
- taxonomy SHA：`13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`
