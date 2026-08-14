---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-04-SECONDARY-R3"
deliverable_id: "CARD-X3-U01-04"
artifact_version: "0.2.2"
artifact_sha256: "aedcd64c718d098255a1b2ab06937a103d5ffec949909c36364d5bc4d073ff31"
review_round: 3
reviewer: "independent_secondary_x3_u01_04_r3"
review_role: "secondary"
reviewed_at: "2026-08-08T22:22:01+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "4ab9c4c2f0d8b27ccb854a4552dfd7f56d95622bfc8bf8ee4d500b32f43c38af"
validator_run_id: "VAL-20260808-222015+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-222015+0800.json"
validator_report_sha256: "611f61099c363efd1419f3a91ae0cd9acc2aa805fb8b99577b991d10c0626056"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "5d456175ff36b198bf54f40ba128037ded19178aab0155fd46397d85f37638c2"
---

# CARD-X3-U01-04 v0.2.2 独立第二复审 R3

## 1. 输入锁定与独立性

本轮重新锁定 v0.2.2 当前快照，独立复核卡片、canonical 学生教材、U01 任务包、现行课标、Source/Artifact 绑定、共享账本和指定 validator 归档报告；不修改卡片、ledger、validator 或状态迁移。重点回归上一轮第3节过程留痕、学习提示/任务来源和注释 Claim—Evidence 回链问题。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.2；SHA `aedcd64c718d098255a1b2ab06937a103d5ffec949909c36364d5bc4d073ff31`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-004-PDF`；SHA `b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；《望海潮》物理页22、切分页1；《扬州慢》物理页23—24、切分页2—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；任务物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群定位物理页25—26、学业质量4-3物理页46 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `4ab9c4c2f0d8b27ccb854a4552dfd7f56d95622bfc8bf8ee4d500b32f43c38af`；CARD-X3-U01-04 为 v0.2.2/`linted` |
| validator | `VAL-20260808-222015+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `611f61099c363efd1419f3a91ae0cd9acc2aa805fb8b99577b991d10c0626056` |

## 2. 内容、证据与边界复核

- 卡片覆盖 `2/2` 正文子文本：《望海潮》物理页22/切页1，《扬州慢》物理页23—24/切页2—3；学习提示位于物理页24/切页3；U01任务一至四在任务包物理页25/切页1；课标学业质量4-3在物理页46。
- `17/17` KP均有唯一ID、合法主维度（仅“人文/语言”）、冻结知识类型（事实/概念/程序/策略/解释）、四层主归属、判定理由、证据ID和置信状态；`17/17` EV均为单值 `Q/F/M/D`（Q=13、F=1、M=2、D=1）。
- 上一轮硬性问题均已关闭：EV-001仍是纯教材标题 Claim；EV-003为《望海潮》连续正文 span；§8.1只保留教材学习提示原意；第3节已将过程留痕明确为项目建议；EV-017补充《望海潮》孙何/赠词对象注释，扬州相关 KP 已显式回链 EV-006。
- 课4正文、注释和学习提示事实总体准确。EV-004—006分别支持《扬州慢》序、正文今昔/结尾及杜牧典故注释；EV-007—008支持两词城市对象、盛衰对照、形式入口和声韵；EV-009—013支持任务一至四；EV-014—015支持课标任务群5与学业质量4-3。
- **P2-正文回链粒度**：KP-010、KP-011、KP-013的证据现已增加 EV-006，但其正文引用“春风十里”“胡马窥江”“杜郎俊赏”等仍未同时显式挂接承载这些诗句的 EV-005；KP-014仍只挂学习提示 EV-007/008，而 Claim 直接引用“二十四桥、冷月、红药、年年知为谁生”，应补挂 EV-005。当前均可在物理页24回查，属于证据回链维护项而非事实或页码硬错。
- **P2-注释 locator 粒度**：EV-006 当前 locator 为物理页24/切页3/注释 g—j，能够覆盖杜牧典故，但 KP-010/011依赖的“春风十里”注释 d 与“胡马窥江”注释 e 不在该 locator/短引中；建议将 EV-006 扩为 d—j 或新增适配 EV。该项与上述正文回链可合并处理。
- 高考模块严格保持 `M0/N/A`，纵向关系为有理由的 `N/A`；教师用书 `edition_match=unknown`，没有用缺源教师用书补写城市史、政治寓意或唯一象征义。

## 3. R01—R10 判定

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两首词题名、作者、正文事实、城市与人物信息、典故和课标4-3引文均与canonical载体一致。 |
| R02 | 否 | `17/17` EV均有可解析Source/Artifact/locator/短引；剩余正文/注释回链是可维护的粒度问题，未造成关键Claim不可定位。 |
| R03 | 否 | 两个正文子文本、学习提示、单元任务、课标、原子KP、M0、纵向和三类教学提示模块均存在。 |
| R04 | 否 | 正文、学习提示、任务、课标M、教师用书D和项目建议已分层；过程留痕已标为项目建议。 |
| R05 | 否 | `17/17` KP均具备合法维度、知识类型、四层主归属、判定理由和证据；EV均为单值Q/F/M/D。 |
| R06 | 否 | 高考保持结构化M0/N/A，未引用未登记真题、答案或评分资料，也未声称M1—M3直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课4教材、U01任务包和现行课标canonical Artifact。 |
| R08 | 否 | 卡片、账本、Source/Artifact、KP/EV数量、路径和指定版本SHA一致；v0.2.2 transition 的 pre/post SHA 与当前卡片一致。 |
| R09 | 否 | 使用现行课标“文学阅读与写作”“语言积累、梳理与探究”及物理页46的4-3，未改写任务群名称或把质量描述当课型。 |
| R10 | 否 | 未机械铺满四项核心素养，也未将学业质量4-3当作单课完整等级或题目难度标签。 |

## 4. P0/P1/P2

`P0/P1/P2 = 0/0/2`。

- **P2-01（正文 Claim 回链）**：KP-010、KP-011、KP-013建议同时挂接 EV-005；KP-014建议挂接 EV-005，以使正文短语与正文 EV 显式闭合。
- **P2-02（注释 locator）**：EV-006 的 g—j locator/短引未覆盖 KP-010、KP-011所依赖的注释 d/e；建议扩展为 d—j 或新建适配 EV。

无P0/P1；EV-001、§8.1、过程留痕和EV-017修订均已通过回归核验。

## 5. 2.0-textbook 量规评分

| 维度 | 权重 | 门槛 | 得分 | 复核依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | `17/17` EV的来源、canonical页位和短引可回查；部分扬州正文/注释子短语尚未显式补齐EV-005或EV-006 d/e回链，扣1.0。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两词事实、城市/人物/典故、学习提示和课标术语准确；仅对证据粒度作保守扣0.5。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | `2/2`正文子文本、`17/17` KP、`17/17` EV、任务/课标/教学/M0/N/A模块完整。 |
| 双维度与母题质量 | 15 | 12 | 15.0 | 人文/语言覆盖城市盛衰、战争记忆、铺叙、虚实、声韵、典故和炼字，文本差异保留充分。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标4-3定位和M0不确定性均清楚。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方accepted逐边证据时合法保持有理由的N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | §8.1/§8.3已分层，过程留痕已明确为项目建议，城市比较路径可直接用于备课。 |
| **合计** | **100** | **85** | **98.5** | R01—R10及P0/P1均通过；P2为非阻断性证据维护建议。 |

## 6. 独立第二复审决定

**决定：`pass`。** 当前 `CARD-X3-U01-04` v0.2.2/SHA `aedcd64c718d098255a1b2ab06937a103d5ffec949909c36364d5bc4d073ff31` 通过本轮独立第二复审，可与同一最终SHA的主审结果配对进入后续流程。当前 ledger 状态仍为 `linted`；本报告不执行状态迁移。建议在进入G4前处理两项P2并重新核对报告绑定；卡片、canonical Artifact、validator、账本或版本绑定任一变化均使本报告失效，须按新SHA复审。

## 7. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.2；SHA `aedcd64c718d098255a1b2ab06937a103d5ffec949909c36364d5bc4d073ff31`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `4ab9c4c2f0d8b27ccb854a4552dfd7f56d95622bfc8bf8ee4d500b32f43c38af`；CARD-X3-U01-04 为 v0.2.2/`linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-222015+0800.json`；SHA `611f61099c363efd1419f3a91ae0cd9acc2aa805fb8b99577b991d10c0626056`；结果 `passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-004-PDF`=`b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 报告 SHA-256按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 值置空后对canonical报告字节求SHA，再回填该值；另行记录实际文件SHA。
