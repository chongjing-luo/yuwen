---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-04-SECONDARY-R2"
deliverable_id: "CARD-X3-U01-04"
artifact_version: "0.2.1"
artifact_sha256: "a4d71896e6ecc3a3f0694dacb9b3c0378b8842bd15e5abe9b1d7c035ca8f27be"
review_round: 2
reviewer: "independent_secondary_x3_u01_04_r2"
review_role: "secondary"
reviewed_at: "2026-08-08T22:16:29+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "1d6be0814b9ac617ffb839b50f1781212c7776670f4a69522089a169414e9f68"
validator_run_id: "VAL-20260808-221510+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-221510+0800.json"
validator_report_sha256: "b7be568f406ca63e6e1d946ae1934de2d95a118aee594642d582bdd035e668b9"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "4c4c00f04d9bd8dfebb59e4338dfed7e5e90c195c90c24763221b9fcaf65155c"
---

# CARD-X3-U01-04 v0.2.1 独立第二复审 R2

## 1. 输入锁定与独立性

本轮重新锁定 v0.2.1 当前快照，独立复核卡片、canonical 学生教材、U01 任务包、现行课标、Source/Artifact 绑定、共享账本和指定 validator 归档报告；不修改卡片、ledger、validator 或状态迁移。重点回归上一轮 EV-001、EV-003、§8.1 和 KP-017 边界问题，并检查新版本的 Claim—Evidence 闭合度。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.1；SHA `a4d71896e6ecc3a3f0694dacb9b3c0378b8842bd15e5abe9b1d7c035ca8f27be`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-004-PDF`；SHA `b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；《望海潮》物理页22、切分页1；《扬州慢》物理页23—24、切分页2—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；任务物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群定位物理页25—26、学业质量4-3物理页46 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `1d6be0814b9ac617ffb839b50f1781212c7776670f4a69522089a169414e9f68`；CARD-X3-U01-04 为 v0.2.1/`linted` |
| validator | `VAL-20260808-221510+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `b7be568f406ca63e6e1d946ae1934de2d95a118aee594642d582bdd035e668b9` |

## 2. 回归核验与当前内容

- 卡片覆盖 `2/2` 正文子文本：《望海潮》物理页22/切页1，《扬州慢》物理页23—24/切页2—3；学习提示位于物理页24/切页3；U01任务一至四在任务包物理页25/切页1；课标学业质量4-3在物理页46。
- `17/17` KP均有唯一ID、合法主维度（仅“人文/语言”）、冻结知识类型（事实/概念/程序/策略/解释）、四层主归属、判定理由、证据ID和置信状态；`16/16` EV均为单值 `Q/F/M/D`（Q=12、F=1、M=2、D=1）。
- **EV-001已修复**：当前 Claim 收窄为“课4正文子文本范围与标题”，短引仅为教材中实际出现的“望海潮”“扬州慢”，不再把任务边界写入课文包 Q 证据；任务边界由 EV-009—013 单独支撑。
- **EV-003已加固**：当前为《望海潮》正文连续最小原文 span，东南形胜、城市铺陈、生活图景、孙何仪仗和结句均可在canonical物理页22回查。EV-004—006覆盖《扬州慢》序、正文今昔对比/结尾和杜牧典故注释；EV-007—008准确支持学习提示的城市对象、盛衰对照、铺叙/虚实、今昔和声韵。
- **§8.1与§8.3已分层**：§8.1只保留学习提示直接支持的城市对象、盛衰对照、形式入口和声韵诵读；项目四列表操作仅在§8.3出现并明确为项目建议。
- **KP-017已收窄**：KP-017现在只写研讨、比较、800字鉴赏文章和合作编集；“过程留痕属于本项目建议”已写入判定理由。但第3节“诵读与表达迁移”仍有“成果应保留引文、提纲、反馈和修订”的项目过程语句，未明确标为项目建议，列为P2维护项。
- 正文、注释和学习提示事实总体准确；高考表严格保持 `M0/N/A`，纵向关系为有理由的 `N/A`；教师用书 `edition_match=unknown`，没有用缺源教师用书补写城市史、政治寓意或唯一象征义。

## 3. 剩余 Claim—Evidence 维护项

- **P2-过程边界**：第3节语言/形式维度中的“成果应保留引文、提纲、反馈和修订”不属于任务包物理页25的明示成果要求；应移到§8.3并加项目层标签，或删除“应保留”措辞。
- **P2-注释证据回链**：KP-008（孙何身份）、KP-010（“春风十里”杜牧典故）、KP-011（胡马进犯背景）、KP-013（杜牧四项典故）在判定理由中依赖课文注释，但当前证据ID主要挂 EV-003/005/007/008，未显式挂接包含注释g—j的 EV-006。EV-006自身短引已正确，建议补挂以使 Claim—Evidence 粒度闭合；当前页位和正文事实仍可回查，不构成P1。

## 4. R01—R10 判定

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两首词题名、作者、正文事实、城市与人物信息、典故和课标4-3引文均与canonical载体一致。 |
| R02 | 否 | `16/16` EV均有可解析Source/Artifact/locator/短引；EV-001职责已收窄、EV-003连续原文已补齐，剩余注释回链是非阻断维护项。 |
| R03 | 否 | 两个正文子文本、学习提示、单元任务、课标、原子KP、M0、纵向和三类教学提示模块均存在。 |
| R04 | 否 | 正文、学习提示、任务、课标M、教师用书D和项目建议已分层；第3节残留的过程留痕属于局部表达维护，不足以构成栏目级混写。 |
| R05 | 否 | `17/17` KP均具备合法维度、知识类型、四层主归属、判定理由和证据；EV均为单值Q/F/M/D。 |
| R06 | 否 | 高考保持结构化M0/N/A，未引用未登记真题、答案或评分资料，也未声称M1—M3直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课4教材、U01任务包和现行课标canonical Artifact。 |
| R08 | 否 | 卡片、账本、Source/Artifact、KP/EV数量、路径和指定版本SHA一致；v0.2.1 transition 的 pre/post SHA 与当前卡片一致。 |
| R09 | 否 | 使用现行课标“文学阅读与写作”“语言积累、梳理与探究”及物理页46的4-3，未改写任务群名称或把质量描述当课型。 |
| R10 | 否 | 未机械铺满四项核心素养，也未将学业质量4-3当作单课完整等级或题目难度标签。 |

## 5. P0/P1/P2

`P0/P1/P2 = 0/0/2`。

- **P2-01（过程边界）**：第3节残留“成果应保留引文、提纲、反馈和修订”，应标为项目建议或删除任务要求语气。
- **P2-02（注释回链粒度）**：KP-008、KP-010、KP-011、KP-013的判定理由使用了课文注释信息，建议显式补挂EV-006；这属于可维护证据粒度问题，不影响正文、页码或事实验收。

无P0/P1；上一轮 EV-001、§8.1 和 KP-017 的硬性边界问题已关闭。

## 6. 2.0-textbook 量规评分

| 维度 | 权重 | 门槛 | 得分 | 复核依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | `16/16` EV的来源、canonical页位和短引可回查；四个依赖注释的KP尚未显式回链EV-006，扣1.0。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两词事实、城市/人物/典故、学习提示和课标术语准确；过程留痕语气与少量注释回链保守扣0.5。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | `2/2`正文子文本、`17/17` KP、`16/16` EV、任务/课标/教学/M0/N/A模块完整。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文/语言覆盖城市盛衰、战争记忆、铺叙、虚实、声韵、典故和炼字，文本差异保留充分。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标4-3定位和M0不确定性均清楚。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方accepted逐边证据时合法保持有理由的N/A。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | §8.1/§8.3已分层，城市比较路径可直接用于备课；第3节过程留痕尚需明确项目层，扣0.5。 |
| **合计** | **100** | **85** | **97.5** | R01—R10及P0/P1均通过；P2为非阻断性维护建议。 |

## 7. 独立第二复审决定

**决定：`pass`。** 当前 `CARD-X3-U01-04` v0.2.1/SHA `a4d71896e6ecc3a3f0694dacb9b3c0378b8842bd15e5abe9b1d7c035ca8f27be` 通过本轮独立第二复审，可与同一最终SHA的主审结果配对进入后续流程。当前 ledger 状态仍为 `linted`；本报告不执行状态迁移。建议在进入G4前处理两项P2并重新核对报告绑定；卡片、canonical Artifact、validator、账本或版本绑定任一变化均使本报告失效，须按新SHA复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.1；SHA `a4d71896e6ecc3a3f0694dacb9b3c0378b8842bd15e5abe9b1d7c035ca8f27be`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `1d6be0814b9ac617ffb839b50f1781212c7776670f4a69522089a169414e9f68`；CARD-X3-U01-04 为 v0.2.1/`linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-221510+0800.json`；SHA `b7be568f406ca63e6e1d946ae1934de2d95a118aee594642d582bdd035e668b9`；结果 `passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-004-PDF`=`b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 报告 SHA-256按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 值置空后对canonical报告字节求SHA，再回填该值；另行记录实际文件SHA。
