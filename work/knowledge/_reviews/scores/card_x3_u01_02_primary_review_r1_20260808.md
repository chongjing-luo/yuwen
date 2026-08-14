---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-02-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-02"
artifact_version: "0.2.0"
artifact_sha256: "e445ecd610fbd7165d4cf192a4006cff30547102a3ec7e16df3d8fff17b7a2e7"
review_round: 1
reviewer: "independent_primary_x3_u01_02_r1"
review_role: "primary"
reviewed_at: "2026-08-08T22:10:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "2e321ed7808a35d7411fffe8518c7f3008edaa7c3e6cf1f9808ac0ecb79778b9"
validator_run_id: "VAL-20260808-211535+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "106204f5553675f2b90fc7fec0d63026ce5431a33032330fe47271ac41962dba"
validator_result: "passed"
decision: "rework"
---

# CARD-X3-U01-02 v0.2.0 独立主审 R1

## 1. 输入锁定与独立性

本轮只依据当前 `CARD-X3-U01-02`、冻结的 `2.0-textbook` knowledge_card rubric/taxonomy、Source/Artifact 注册表、canonical 学生教材、U01 单元任务和现行课标重新复核；不读取或复用旧版评审结论，不修改卡片、账本、validator 或状态。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-02.md`；v0.2.0；SHA `e445ecd610fbd7165d4cf192a4006cff30547102a3ec7e16df3d8fff17b7a2e7`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-002-PDF`；SHA `89a807fd0f166c4999331ca024f83d72f567aebce533b1eb23f34fa03faa32d5`；7页；物理页12—18、切分页1—7；路径 `Data/textbook_extract/选择性必修下册/02_U1_课2_孔雀东南飞并序.pdf` |
| 单元任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；2页；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；66页 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `2e321ed7808a35d7411fffe8518c7f3008edaa7c3e6cf1f9808ac0ecb79778b9`；CARD-X3-U01-02 为 v0.2.0 / `linted` |
| validator | `VAL-20260808-211535+0800`；`passed`；0 errors；`hash_verification=true`；报告 SHA `106204f5553675f2b90fc7fec0d63026ce5431a33032330fe47271ac41962dba` |

## 2. 覆盖、页码与内容复核

### 2.1 已通过部分

- 卡片登记 1/1 正文子文本 `《孔雀东南飞并序》`，并将序文、正文、注释、学习提示分层；正文覆盖 canonical 物理页12—18/切分页1—7，学习提示在物理页18/切分页7。
- 16/16 KP 均有知识陈述、类型、四层主归属、判定理由、证据ID和置信状态；10/10 EV 均登记 Source、Artifact、locator、短引文、支撑关系和 `verified`。
- EV-001—008 的序文、遣归对话、临别动作、磐石蒲苇誓言、逼婚/重逢、双死合葬、学习提示和偏义复词引文均可在对应 canonical 页回查。`“感于哀乐，缘事而发”`、`“运用对话推动情节发展、塑造人物形象”`和偏义复词定义/例词与物理页18一致。
- EV-009 的 U01 任务二至任务四定位到任务包物理页25—26/切分页1—2，所引比较、800字鉴赏文章和《古典诗词鉴赏集》要求可回查；高考栏保持 M0，纵向关系给出有理由的 N/A，教师用书边界声明 `edition_match=unknown`。

### 2.2 必须返工的问题

#### A. KP-014 主维度非法（P1）

`KP-CARD-X3-U01-02-014` 的主维度仍填为“思维”。冻结 `taxonomy.yaml` 的 `knowledge_dimensions` 只有 `人文`、`语言`；“思维”可以作为策略动作或核心素养说明，但不能作为知识卡主维度枚举。应改为与卡片语言/阅读方法双线一致的合法值（建议 `语言`），并复核理由与下游检索。

#### B. EV-010 混合 Claim 类型、来源职责和页位（P1）

EV-010 的类型写为 `M/D`，但冻结证据契约要求每条 EV 使用单一 `claim_type`（Q/F/I/M/R/E/D）。该行同时承载：

1. 课标任务群5与学业质量定位（M，课标物理页25—27、44）；
2. “未登记同版教师用书”缺源声明（D/项目边界，来自来源注册表）；
3. “本卡不判定完整水平”项目边界。

当前 Source/Artifact 指向 `SRC-CURR-2020` / `ART-CURR-2020-PDF`，不能同时证明教师用书缺源声明；locator 也把物理页25—27、44和来源注册表混为一条，无法形成单一可回查证据。应将 M 课标证据和 D 教师用书缺源/项目边界拆为独立 EV（各自单值类型、Source/Artifact、locator 和验证状态），或收窄 EV-010 只承担一种证明责任，并更新所有 KP/教学提示引用。

#### C. 若干复合 KP 的短引 span 仍应收窄（P2）

KP-003 的 `“十七为君妇，心中常苦悲”`、KP-007 的拒绝媒妁/“处分适兄意”、KP-008 的 `“愁思出门啼”`、KP-009 的 `“贺卿得高迁”`未在各自登记的 EV-002/005 短引中逐字出现；当前 locator 能定位到相应页，但 Claim—短引并非完全闭合。建议补齐代表性连续短引或将复合陈述拆成更小 KP，以维持正式 Claim 的可回查性。该项在上述两项 P1 修复后仍需随同回归核验。

## 3. R01—R10 与 P0/P1/P2

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、序文、人物、事件链、正文诗句和学习提示与 canonical 教材一致，未见关键事实张冠李戴。 |
| R02 | **是** | EV-010 的 M/D 混合行无法以一个 Source/Artifact/locator 支撑课标与教师用书缺源两类主张；KP-003/007/008/009还存在部分 Claim—短引 span 未闭合。 |
| R03 | 否 | 序文、正文、学习提示、任务、课标、纵向、高考和三类教学提示模块齐全；非特殊内容包模板漏项。 |
| R04 | **是** | EV-010 把来源注册表的教师用书缺源声明与课标 PDF 绑定在同一证据行，混淆规范课标定位和项目边界的证明责任。 |
| R05 | **是** | KP-014 使用不在冻结 taxonomy 的“思维”主维度；EV-010 作为单值证据无效，影响课标/教师用书相关字段的有效证据。 |
| R06 | 否 | 高考关系严格保持 M0，没有未登记真题、答案或评分资料。 |
| R07 | 否 | 正式内容只消费已登记并核验的教材、任务包和现行课标；问题是证据职责混合而非上游未验收。 |
| R08 | 否 | 卡片版本、ID、数量、路径和 ledger SHA 绑定一致；当前缺陷是字段/证据语义断裂，不是版本或文件链接断链。 |
| R09 | 否 | 使用现行课标任务群名称与三类语文活动，没有把任务群改写为固定课型。 |
| R10 | 否 | 未机械铺满四项核心素养，也未将学业质量水平当作单卡难度标签。 |

`P0/P1/P2 = 0/2/1`。P1分别为非法主维度和 EV-010 混合证据职责；P2为复合 KP 的短引 span收窄项。

## 4. knowledge_card 量表诊断分

因 R02/R04/R05 硬门尚未通过，以下分数用于定位返工成本，不能替代合格性判断。

| 维度 | 权重 | 门槛 | 诊断得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 18.0 | 9/10 EV可独立回查；EV-010把M/D两类责任混合，且若干复合KP的短引未覆盖全部子主张。 |
| 事实与术语准确性 | 20 | 18 | 16.5 | 正文与学习提示事实准确，但“思维”非法维度和EV-010的类型/来源职责错误降低术语与规范性。 |
| 字段完整与知识粒度 | 15 | 12 | 13.0 | 1/1子文本、16/16 KP、10/10 EV和模块齐全；KP-014主维度及EV-010字段需返工，复合KP需收窄。 |
| 双维度与母题质量 | 15 | 12 | 13.0 | 人文/语言母题、人物处境、对话、偏义复词和比较任务覆盖较好；非法维度使双线结构不能正式锁定。 |
| 四层与高考映射 | 10 | 8 | 9.0 | KP层级理由和M0边界大体清楚；EV-010的课标映射不能与教师用书D声明共用一条证据。 |
| 纵向贯通 | 8 | 6 | 8.0 | 相邻卡尚未完成同版本双审，N/A理由充分。 |
| 教学可用性与表达 | 7 | 5 | 5.5 | 对话/动作和偏义复词教学动作可操作；混合EV会误导课标/教师用书检索，复合KP需补span。 |
| **合计** | **100** | **85** | **83.0** | 诊断分低于门槛，且硬门未通过。 |

## 5. 返工与决定

1. 将 KP-014 主维度改为 `人文`或`语言`中的合法值（建议 `语言`），更新判定理由/下游引用。
2. 拆分或重写 EV-010：M 类课标任务群/学业质量证据与 D 类教师用书缺源/项目边界必须分别登记单值 Claim 类型、对应 Source/Artifact/locator；更新 §4、§8.2 和所有 KP 引用。
3. 补齐 KP-003/007/008/009 的关键短引 span，或收窄相应复合 Claim；重新计算卡片 SHA、更新 ledger transition、重跑 validator，再进行同新 SHA 的独立主审和第二复审。

**主审决定：`rework`。** 当前 v0.2.0/SHA 不得进入 `accepted` 或被单元图谱正式消费；完成上述返工并重新锁定全量绑定后才可复审。

## 6. 可复现绑定

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-02.md`；v0.2.0；SHA `e445ecd610fbd7165d4cf192a4006cff30547102a3ec7e16df3d8fff17b7a2e7`。
- 学生教材 canonical：`ART-PKG-X3-002-PDF` SHA `89a807fd0f166c4999331ca024f83d72f567aebce533b1eb23f34fa03faa32d5`；单元任务 canonical：`ART-PKG-X3-005-PDF` SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；课标 canonical：`ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- ledger：`work/knowledge/_meta/deliverables.jsonl` SHA `2e321ed7808a35d7411fffe8518c7f3008edaa7c3e6cf1f9808ac0ecb79778b9`。
- validator：`VAL-20260808-211535+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `106204f5553675f2b90fc7fec0d63026ce5431a33032330fe47271ac41962dba`；结果 `passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
