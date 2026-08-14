---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-04-SECONDARY-R1"
deliverable_id: "CARD-X3-U01-04"
artifact_version: "0.2.0"
artifact_sha256: "61e77df4f932be95abe0ad664f887f15179b1d837535c7d1d1dad281655ef2a1"
review_round: 1
reviewer: "independent_secondary_x3_u01_04_r1"
review_role: "secondary"
reviewed_at: "2026-08-08T22:14:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "1c0a9d7cc2e5f0b4f1df37cbe36d3b2906c1983e104be353466f8a57b0d8599d"
validator_run_id: "VAL-20260808-221001+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-221001+0800.json"
validator_report_sha256: "4ca0b6569bc9562543c2843075cf75b0f56e8c36588a92fc9f00c3c1ee3a1301"
validator_result: "passed"
decision: "rework"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "6b3a0284f0a001d6eee18c203d8f0e04b86c00cfc97a061976385637037c0e2a"
---

# CARD-X3-U01-04 v0.2.0 独立第二复审 R1

## 1. 输入锁定与独立性

本轮重新锁定当前 v0.2.0 快照，独立复核卡片、canonical 学生教材、U01 任务包、现行课标、Source/Artifact 绑定、共享账本和指定 validator 归档报告；不修改卡片、ledger、validator 或状态迁移。重点核对课4物理页22—24、U01任务物理页25、课标学业质量4-3物理页46，以及学习提示与本项目建议的栏目边界。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.0；SHA `61e77df4f932be95abe0ad664f887f15179b1d837535c7d1d1dad281655ef2a1`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-004-PDF`；SHA `b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；《望海潮》物理页22、切分页1；《扬州慢》物理页23—24、切分页2—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；任务物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群定位物理页25—26、学业质量4-3物理页46 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `1c0a9d7cc2e5f0b4f1df37cbe36d3b2906c1983e104be353466f8a57b0d8599d`；CARD-X3-U01-04 为 v0.2.0/`linted` |
| validator | `VAL-20260808-221001+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `4ca0b6569bc9562543c2843075cf75b0f56e8c36588a92fc9f00c3c1ee3a1301` |

## 2. 内容、证据与边界复核

- 卡片覆盖 `2/2` 正文子文本：《望海潮》物理页22/切页1，《扬州慢》物理页23—24/切页2—3；学习提示位于物理页24/切页3；U01任务一至四在任务包物理页25/切页1；课标学业质量4-3在物理页46。
- `17/17` KP均有唯一ID、合法主维度（仅“人文/语言”）、冻结知识类型（事实/概念/程序/策略/解释）、四层主归属、判定理由、证据ID和置信状态；`16/16` EV类型为单值 `Q/F/M/D`（Q=12、F=1、M=2、D=1）。
- 《望海潮》的城市总览、空间铺陈、市场与生活、钱塘潮、孙何仪仗及结句，可在canonical物理页22逐项回查；《扬州慢》序、正文今昔对比、战争创伤、声响、杜牧典故和结尾红药，可在物理页23—24逐项回查。课文注释对高牙、凤池、胡马、杜牧诗句等提供了相应说明。
- 学习提示 EV-007—008准确记录“一写承平盛世，一写劫后孤城”、铺叙/点面/虚实、今昔对比、杜牧想象和声韵；任务 EV-009—013分别支持研讨、比较、意象/意境或虚实探究、800字鉴赏文章与鉴赏集；课标 EV-014—015分别支持任务群5和学业质量4-3定位。
- **P1-边界1（EV-001）**：EV-001的 Claim 写为“课4正文、学习提示和任务的来源边界”，但 Source/Artifact 仅为 `SRC-PKG-X3-004`/`ART-PKG-X3-004-PDF`，locator仅物理页22—24，短引“‘望海潮’‘扬州慢’及其正文、学习提示均位于本canonical课文包；正式引文回到PDF”也不是教材正文/栏目原文，不能独立支持其中的“任务”边界。应将 Claim 收窄为课文包标题/正文/学习提示范围，或另以任务 Artifact 支撑任务边界，并按图例改用适当的 D/Q 类型。
- **P1-边界2（§8.1）**：“教材学习提示”栏写入“制作‘城市空间—时间视角—意象/声音—典故—情绪’证据表”等项目操作。canonical学习提示要求理解两词的城市对象、盛衰对照、铺叙/虚实、今昔和声韵并在诵读中体会，但没有直接规定制作该证据表；该操作应移至§8.3并标为本项目建议。
- **P2-过程留痕**：KP-017与“诵读与表达迁移”把“成果需保留引文、提纲、反馈和修订”写成U01任务要求；任务原文直接要求研讨、比较、探究、写不少于800字鉴赏文章和合作编集，并未明示必须保留这些过程档案。应收窄为教材直接成果，或将留痕明确降为项目建议。
- **P2-证据粒度**：KP-008的“孙何”身份以及少数含注释/典故的复合Claim主要依赖整页 locator，EV-003/006短引未逐项展开所有解释性子短语；正文事实可回查，不构成P1，但后续可补最小连续 span或拆分Claim。
- 高考模块严格保持 `M0/N/A`，未挂未登记真题、答案或评分资料；纵向关系为有理由的 `N/A`；教师用书 `edition_match=unknown`，没有用缺源教师用书补写城市史、政治寓意或唯一象征义。

## 3. R01—R10 判定

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两首词题名、作者、正文事实、城市与人物信息、典故和课标4-3引文均与canonical载体一致，未发现关键事实错误。 |
| R02 | **是** | EV-001的正式Claim同时要求课文包和任务边界，但其Source/Artifact/locator不含任务，且Q短引并非规范教材原文；该Claim—EV—来源链未闭合。KP-017过程留痕和少数复合短引另列为非阻断加固项。 |
| R03 | 否 | 两个正文子文本、学习提示、单元任务、课标、原子KP、M0、纵向和三类教学提示模块均存在。 |
| R04 | **是** | EV-001把项目来源边界说明写成Q（教材正文/栏目原文）；§8.1又把项目证据表操作写入教材学习提示栏，规范教材提示与项目建议边界混写。 |
| R05 | 否 | `17/17` KP均具备合法维度、知识类型、四层主归属、判定理由和证据；EV均为单值Q/F/M/D，未见非法枚举。 |
| R06 | 否 | 高考保持结构化M0/N/A，未引用未登记真题、答案或评分资料，也未声称M1—M3直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课4教材、U01任务包和现行课标canonical Artifact。 |
| R08 | 否 | 卡片、账本、Source/Artifact、KP/EV数量、路径和指定版本SHA一致；问题是Claim/栏目语义，不是文件或ID断链。 |
| R09 | 否 | 使用现行课标“文学阅读与写作”“语言积累、梳理与探究”及物理页46的4-3，未改写任务群名称或把质量描述当课型。 |
| R10 | 否 | 未机械铺满四项核心素养，也未将学业质量4-3当作单课完整等级或题目难度标签。 |

## 4. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误或不可恢复损坏。 |
| P1 | 2 | `P1-EV001-BOUNDARY`：EV-001的Q类型、课文包Artifact与包含“任务边界”的Claim不匹配；`P1-SEC81-MIX`：§8.1将项目证据表操作写成教材学习提示。 |
| P2 | 2 | `P2-KP017-PROCESS`：任务直接成果与项目过程留痕未分层；`P2-SPAN-ANNOTATION`：少数含注释/典故的复合Claim短引未逐项展开全部子短语。 |

## 5. 2.0-textbook 诊断评分

因 R02/R04 与两项 P1 硬门未通过，正式验收分记为 `N/A`；以下为返工定位用诊断分，不替代合格性判断。

| 维度 | 权重 | 门槛 | 诊断得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 18.5 | `15/16` EV的canonical页位与短引基本可回查；EV-001的Claim/Artifact/类型职责不闭合，少数复合Claim的解释性span偏压缩。 |
| 事实与术语准确性 | 20 | 18 | 18.5 | 两词事实、体式、城市/人物/典故和课标术语总体准确；EV-001把项目边界写成Q，且§8.1规范来源标签不严。 |
| 字段完整与知识粒度 | 15 | 12 | 14.5 | 双正文、17 KP、16 EV、任务/课标/M0模块齐全；KP-017过程要求和少数复合Claim尚需收窄。 |
| 双维度与母题质量 | 15 | 12 | 14.0 | 人文/语言覆盖城市盛衰、战争记忆、铺叙、虚实、声韵、典故和炼字；个别解释依赖宽locator，扣分。 |
| 四层与高考映射 | 10 | 8 | 9.5 | 四层理由、课标4-3定位和M0边界合规；当前无真题双向证据。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无可靠相邻accepted目标时使用有理由的N/A。 |
| 教学可用性与表达 | 7 | 5 | 5.0 | 城市比较和原句—形式—情绪路径可用，但§8.1项目操作混入教材提示，来源分层未过。 |
| **诊断合计** | **100** | **85** | **88.0** | 仅用于返工优先级；R02/R04硬门触发，不能作为放行分数。 |

## 6. 返工建议与独立第二复审决定

1. 修正 EV-001：将 Claim 收窄为课4教材包的标题/正文/学习提示范围，保留Q时使用实际教材短引；任务边界由 EV-009—013 和 `ART-PKG-X3-005-PDF` 单独支撑，或将整个边界 Claim 改为有适配来源的D。
2. 严格拆分 §8.1 与 §8.3：§8.1只保留canonical学习提示直接支持的城市对象、盛衰对照、铺叙/虚实、今昔、杜牧想象和声韵诵读；“制作证据表”移至§8.3并明确为项目建议。
3. 将 KP-017 的“保留引文、提纲、反馈和修订”降为项目建议或收窄为教材直接成果；同时补齐KP-008等少数复合Claim的最小连续span/注释引文。
4. 升版并重算卡片SHA、更新ledger transition、重跑validator，再以新SHA进行独立主审和第二复审；当前SHA不得进入 `accepted` 或被单元图谱正式消费。

**决定：`rework`。** 当前 `CARD-X3-U01-04` v0.2.0/SHA `61e77df4f932be95abe0ad664f887f15179b1d837535c7d1d1dad281655ef2a1` 未通过本轮独立第二复审。报告不执行任何状态迁移。

## 7. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-04.md`；v0.2.0；SHA `61e77df4f932be95abe0ad664f887f15179b1d837535c7d1d1dad281655ef2a1`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `1c0a9d7cc2e5f0b4f1df37cbe36d3b2906c1983e104be353466f8a57b0d8599d`；CARD-X3-U01-04 为 v0.2.0/`linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-221001+0800.json`；SHA `4ca0b6569bc9562543c2843075cf75b0f56e8c36588a92fc9f00c3c1ee3a1301`；结果 `passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-004-PDF`=`b67fc3a2e059f7d2e46b986b8cce2072f82f97d387e8317bc41eca71d884a052`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256`按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 值置空后对canonical报告字节求SHA，再回填该值；另行记录实际文件SHA。
