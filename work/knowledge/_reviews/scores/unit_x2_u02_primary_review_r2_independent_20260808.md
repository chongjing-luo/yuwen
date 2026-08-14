---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X2-U02-R2-PRIMARY-INDEPENDENT"
deliverable_id: "UNIT-X2-U02"
artifact_version: "0.2.2"
artifact_sha256: "cec71ccef119e98c4d1b601bc2f9bf8d960f784ce494aab0dd42a5fc177019be"
review_round: 2
reviewer: "independent_primary_x2_u02_r2"
review_role: "primary"
reviewed_at: "2026-08-08T18:07:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-180309+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/unit_x2_u02_graph_validation_rework2.json"
validator_report_sha256: "02f61f5cc6dbfa4bc54e42eb1c9d3e9044d9c43b1dd5971cec3904d7e6706eaf"
validator_result: "passed"
decision: "pass"
---

# UNIT-X2-U02 v0.2.2 独立主审 R2

## 1. 锁定对象与独立性

- 本轮只审查当前 `work/knowledge/选择性必修中册/units/UNIT-X2-U02.md` v0.2.2，当前 SHA-256 为 `cec71ccef119e98c4d1b601bc2f9bf8d960f784ce494aab0dd42a5fc177019be`；本报告绑定新版本，不将旧 SHA 的评审结论作为当前输入。
- 采用冻结 `2.0-textbook` 单元图谱量表：总分门槛 88，七维门槛依次为 22/16/12/12/8/8/4。Rubric、taxonomy、validator 绑定在页眉。
- 当前 ledger 条目为 `linted / v0.2.2 / root`；本报告只写入独立主审记录，不修改图谱正文、`deliverables.jsonl` 或 transition。

| 上游卡 | 版本/状态 | 当前 SHA-256 |
|---|---|---|
| `CARD-X2-U02-01` | 0.2.0 / accepted | `117a68f1d16f55a252fca4b27177976dd062fd60213a4f474d25ee3d9add4b03` |
| `CARD-X2-U02-02` | 0.2.0 / accepted | `4eb92ade64987dfaf8cc140d6aced084accec4b00ad3af3da010582e2cb26c9a` |
| `CARD-X2-U02-03` | 0.2.1 / accepted | `edea1395617d133b653c1a1d0379985b9564839496312f0acbdc3a9173a2e27c` |

## 2. Validator、来源与结构复算

`VAL-20260808-180309+0800` 结果为 `passed`；contracts、deliverables、existing_outputs、registry_links、rubrics、taxonomy 六类检查均为 0 errors，hash verification=true。当前 canonical 依赖为：

- `ART-PKG-X2-007-PDF` SHA `88f8f162f5cf46e9c5d4474d208fafe6de16c0d290624623a3063ba4cf637616`；
- `ART-PKG-X2-008-PDF` SHA `24081913e2ee0fa8e2d1b899b0a9476bcbfc9afa708088293893c413ac6cb316`；
- `ART-PKG-X2-009-PDF` SHA `32977e3de9ddca86adfd8935ff01a3150a55f17ba15e9c0e5e95d54febf8cb9b`；
- 共用任务 `ART-PKG-X2-010-PDF` SHA `3d90ed6a9b2af696231f54c44a6ba991a42cccc02125bd6c3fdbd425830fe1ab`；
- 现行课标 `ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。

人工复算如下：

- 上游卡 3/3、正文子文本 6/6、上游 KP 46/46；按 §1.1 连续范围展开，三卡全部进入至少一个人文或语言节点，并在任务或 REL 中有入口，未见重复纳入。
- v0.2.2 新增并显式纳入卡01/卡03 的材料边界 KP-001：`CAND-L-X2-U02-006` 现在以卡01/02/03 的边界 KP 为证据化阅读入口，覆盖声明与节点索引一致。
- 人文节点 5 个、语言节点 7 个、人文—语言交叉节点 2 个、单元关系 9 条；关系类型均为冻结 taxonomy 的“比较/深化/组成/迁移”，ID 唯一且两端可回链。
- 任务分支 5/5 全覆盖：革命意义讨论、两文批注本、报告文学札记、小说人物典型性分析、红色作品集；任务原文定位统一到物理页 85/切分页 1。
- 高考栏为唯一结构化 `M0`，没有未登记真题小问、答案或评分资料；前序/后续保持有理由的 `N/A`；教师用书缺源与外部作品集材料仍按开放条件处理。

## 3. Claim—Evidence、综合语义与边界

- 图谱明确把 CAND/REL 标为上游证据基础上的单元级综合，不冒充教材原文。人文线覆盖纪念与公共记忆、制度性压迫、人民与新生活及证据化革命文化继承；语言线覆盖纪念性散文、报告文学、革命题材小说的形式—价值中介，以及批注、札记、人物分析和合作作品集的读写链。
- `CAND-H-X2-U02-001—005` 均回到三张 accepted 卡的 KP/EV 与任务包；制度压迫、人道与历史希望回链卡02正文，人物与环境典型性回链卡03，纪念与写作责任回链卡01。新增/修正的材料边界 KP-001 只作为证据化阅读入口，不生成新的教材知识点。
- `CAND-L-X2-U02-001—007` 将形式观察、证据记录、回应异议和修订转为可操作任务；没有把项目评价短语冒充教材原文。`CAND-L-X2-U02-006` 对边界 KP 的纳入使“材料—判断—待核问题”链条与三卡正式证据边界更完整。
- REL-001—009 均写出源/目标、关系类型、共性/差异或迁移理由及双端证据。例如 REL-001 保留纪念性散文与报告文学的文体差异，REL-002 从制度揭露深化到人民行动，REL-006—008 将比较、札记、人物分析和作品集任务作为迁移而非题目等价。
- 任务三允许后续汇集课外材料，但图谱已将外部材料注册列为开放条件；当前消费范围仍限于三张卡和任务包。M0、纵向 N/A 与教师用书 `unknown` 均有明确解锁条件，不构成缺失掩盖。

## 4. R01—R10 硬性检查

| 代码 | 触发？ | 证据/说明 |
|---|---|---|
| R01 | 否 | 三张卡、六个正文子文本、任务包和课标 Artifact/页码与 canonical 注册一致；无关键事实或关系端点张冠李戴。 |
| R02 | 否 | 46/46 KP、5 项任务、14 个 CAND 节点和 9 条 REL 均有 Card/KP/EV、任务或课标入口；新增 KP-001 边界入口有明确来源，正式综合主张可定位。 |
| R03 | 否 | 卡清单、正文子文本、任务、H/L/HL 节点、REL、M0、纵向、Issue 与覆盖自检模块齐全。 |
| R04 | 否 | 教材原文、上游卡研究性解释、项目评价、外部材料待注册项和课标定位分层；CAND/REL 未冒充规范教材结论。 |
| R05 | 否 | 46 个上游 KP 按连续范围展开均进入至少一个 H/L 节点；v0.2.2 进一步把卡01/卡03 的材料边界 KP-001 纳入 `CAND-L-X2-U02-006`，覆盖声明与实际索引闭合。 |
| R06 | 否 | 高考只保留合法结构化 M0，未引用未登记真题、答案或评分资料，也未把一般题型相似性升级为 M1—M3。 |
| R07 | 否 | 3/3 上游卡均为 ledger `accepted`，版本和 SHA 与图谱 §1 一致；未消费未验收卡。 |
| R08 | 否 | 图谱 v0.2.2、3 个上游版本/SHA、Card/KP/EV/TASK/CAND/REL ID、数量和路径一致；validator hash verification=true。 |
| R09 | 否 | 仅继承现行课标任务群与卡片中的受控名称，未改写任务群名称或把任务群当固定课型/教法。 |
| R10 | 否 | 未机械铺满核心素养或给单元贴完整学业质量水平；M0、纵向 N/A、教师用书 unknown 和外部材料 open 边界透明。 |

结论：`R01—R10 全部为否`。

## 5. 单元图谱量表评分

| 维度 | 权重 | 单项门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | 25.0 | 3/3 accepted 卡、6/6 正文子文本、46/46 KP、5/5 任务和稳定范围索引均闭合；v0.2.2 已补入卡01/卡03 KP-001 材料边界入口。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | 19.0 | 5 H、7 L、2 HL 节点与 9 条受控 REL 有共性、差异和迁移边界；少数“革命文化继承/公共责任”属于较宽的单元综合，虽有任务与卡证据，保守扣 1.0。 |
| 人文与语言双维度结构 | 15 | 12 | 15.0 | 人文线覆盖记忆、制度、人和新生活，语言线覆盖三类文体、形式功能、证据化读写；HL 节点明确不新增 KP，材料边界入口已补齐。 |
| 单元任务拆解 | 15 | 12 | 15.0 | 5/5 任务均有 canonical 原文定位、能力动作、上游回链、成果和项目评价；课内材料与课外材料边界写明。 |
| 高考衔接及证据 | 10 | 8 | 10.0 | 结构化 M0、N/A 和 G-TB 解锁条件清楚；没有越级映射。 |
| 前后递进 | 10 | 8 | 10.0 | 前序、后续无双方 accepted 逐边证据时保持 N/A，未以单元顺序或宽泛主题强造递进。 |
| 可读性与检索性 | 5 | 4 | 5.0 | 卡清单、连续 KP 索引、任务表、H/L/HL 节点表、REL 表、M0、Issue 和覆盖自检齐全，新增边界入口可检索。 |
| **合计** | **100** | **88** | **99.0** | 总分及七维单项门槛均达标。 |

## 6. P0/P1/P2 与决定

| 等级 | 数量 | 说明 |
|---|---:|---|
| P0 | 0 | 无来源伪造、关键事实错误、硬性依赖断裂或不可恢复综合错误。 |
| P1 | 0 | 上游 accepted 绑定、46/46 KP 覆盖、Claim—Evidence、REL 双端、任务 5/5、M0 和 N/A 均闭合；材料边界 KP-001 已纳入节点。 |
| P2 | 0 | 宽泛综合命题已通过 CAND 标识、证据和边界降级；外部材料与教师用书待办均显式列入 Issue，不影响当前验收。 |

**主审决定：`pass`。** 当前 v0.2.2/SHA 可进入独立第二复审；若图谱、上游卡或 canonical Artifact 变更，必须按新绑定重新计算 SHA 并重审。二审需绑定同一版本/同一 SHA，且总分差不超过 5、单维差不超过 2 后方可进入 G4。

## 7. 可复现信息

- 被评图谱：`work/knowledge/选择性必修中册/units/UNIT-X2-U02.md`，v0.2.2，SHA `cec71ccef119e98c4d1b601bc2f9bf8d960f784ce494aab0dd42a5fc177019be`。
- Validator：`VAL-20260808-180309+0800`，`passed`，0 errors；报告 `work/knowledge/_meta/validation_reports/archive/unit_x2_u02_graph_validation_rework2.json`，SHA `02f61f5cc6dbfa4bc54e42eb1c9d3e9044d9c43b1dd5971cec3904d7e6706eaf`。
- Rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 分母：3 张 accepted 上游卡、6 个正文子文本、46 KP、5 个任务分支、5 H/7 L/2 HL 节点、9 条 REL、1 行结构化 M0、前序/后续各 1 行合法 N/A。
