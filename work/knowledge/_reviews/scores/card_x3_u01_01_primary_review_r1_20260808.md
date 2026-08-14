---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-01-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-01"
artifact_version: "0.2.0"
artifact_sha256: "acca68281bb932deab7b06db04ae7ab41d50bde04a6a19343d3d8b6a1a18306c"
review_round: 1
reviewer: "independent_primary_x3_u01_01_r1"
review_role: "primary"
reviewed_at: "2026-08-08T21:20:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "01cb8097b62863811410df023eda38137f19ceb8dcaa5bd0c424207a59b54189"
validator_run_id: "VAL-20260808-205806+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "b014b2146714512c6877922c36fcd493ca34055c8f70458c8b487b28571fcb5b"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-205806+0800.json"
validator_archive_report_sha256: "b014b2146714512c6877922c36fcd493ca34055c8f70458c8b487b28571fcb5b"
validator_result: "passed"
decision: "rework"
---

# CARD-X3-U01-01 v0.2.0 独立主审 R1

## 1. 锁定对象、独立性与量表

本轮只审当前 `CARD-X3-U01-01`，不修改卡片正文、账本、validator 或状态，不复用旧版本结论。采用冻结 `2.0-textbook` knowledge_card 量表：总分门槛 85，七维门槛为 `21/18/12/12/8/6/5`。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md`；v0.2.0；SHA `acca68281bb932deab7b06db04ae7ab41d50bde04a6a19343d3d8b6a1a18306c`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-001-PDF`；SHA `419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；6页；物理页6—11，切分页1—6；路径 `Data/textbook_extract/选择性必修下册/01_U1_导语_课1_氓_离骚.pdf` |
| 单元任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；2页；物理页25—26，切分页1—2；路径 `Data/textbook_extract/选择性必修下册/05_U1_单元研习任务.pdf` |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；66页；路径 `Data/reference/curriculum/普通高中语文课程标准（2017年版2020年修订）_教育部官方版.pdf` |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `01cb8097b62863811410df023eda38137f19ceb8dcaa5bd0c424207a59b54189`；CARD-X3-U01-01 为 v0.2.0 / `linted` |
| validator | `VAL-20260808-205806+0800`；latest/archive 均 `passed`、0 errors、`hash_verification=true`；报告 SHA `b014b2146714512c6877922c36fcd493ca34055c8f70458c8b487b28571fcb5b` |

正式判断回看 canonical PDF；MinerU 产物只作导航，不能替代以下引文复核。

## 2. 正文边界、页码与覆盖复核

### 2.1 正文与栏目边界

卡片登记 2 个正文子文本：`《氓》`、`《离骚》（节选）`，两者均来自教材包物理页7—10（切分页2—5）。单元导语位于物理页6/切分页1，学习提示位于物理页11/切分页6；U01 单元研习任务来自独立任务包物理页25—26/切分页1—2；课标定位来自现行 2020 修订课标。卡片明确不把网络赏析、其他版教师用书或外部真题写成教材事实，边界完整。

### 2.2 Canonical 页码与短引

- EV-001—008 的物理页、切分页和栏目均与教材包的实际顺序一致：导语6；《氓》标题/正文7—8；《离骚》标题/正文8—10；学习提示11。正文诗句、注释和提示中的题名、作者、情节、比兴、香草意象、节奏和抒情判断均可在 canonical 页回查。
- EV-009—012 的物理页25—26/切分页1—2与任务包一致。任务一“今天，我们为什么读古诗词”、任务二《氓》与《孔雀东飞》比较、任务三虚实/意象探究、任务四不少于800字鉴赏文章和鉴赏集均能定位。
- EV-013 的任务群5页码25—27/印刷页17—19与课标正文相符，直接引文“在感受形象、品味语言、体验情感的过程中提升文学欣赏能力，并尝试文学写作，撰写文学评论”可在 canonical PDF 定位。
- EV-014 的物理页44是正确的课标学业质量页，但其短引“能结合具体文本内容概括、阐释并用证据表达判断”不是 canonical PDF 的逐字连续引文。物理页44可定位的规范表述包括水平2-3“能对作品的内容和形式作出自己的评价”，以及水平4-3“能结合作品的具体内容，阐释作品的情感、形象、主题和思想内涵，能对作品的表现手法作出自己的评论”。当前引文把多个质量描述压缩重写，却保留了引号并标为 verified，不能作为正式直接引文。
- EV-003/004 的 locator 正确，但 KP-005 中引用的“士也罔极，二三其德”、KP-006 中引用的“信誓旦旦，不思其反”“反是不思，亦已焉哉”没有完整出现在对应 EV 的短引中：EV-004 只列到“女也不爽，士贰其行”，EV-003 只列“反是不思，亦已焉哉”而未给前置盟誓句。页位能定位正文，但 Claim—短引闭合仍需补精确 span 或收窄 KP 陈述。

## 3. KP、证据类型与结构检查

- 16/16 KP 均有知识陈述、类型、四层归属、映射理由、EV-ID 和置信状态；2 个正文子文本、15 个 EV、纵向 N/A、高考 M0 和教师用书 unknown 模块齐全。
- EV 类型均为单值 Q/F/M/D（Q=11、F=1、M=2、D=1），没有 `Q/M` 等混合枚举；但 EV-014 的 M 短引须改为 canonical 逐字引文。EV-015 的 D 缺源声明与 `edition_match=unknown` 一致，不消费教师用书意见。
- **受控维度违规：** `KP-CARD-X3-U01-01-014` 的主维度填为“思维”。冻结 `taxonomy.yaml` 的 `knowledge_dimensions` 仅允许 `人文`、`语言`；同卡其余 KP 均使用这两个合法值。“思维”可作为项目能力说明或改归语言维度，但不能作为知识卡主维度枚举。机械 validator 未捕获这一表格语义错误，不能据此视为已通过。
- KP-002—013 的事实/解释大体与正文或学习提示适配；KP-014 的程序链有任务/提示依据，但其主维度违规。KP-005/006 的解释/事实主张在 canonical 正文中存在，但证据表需补出与 Claim 对齐的短引 span。
- 课标仅用于任务群5和学业质量能力边界定位，未给单卡判定完整水平；高考栏严格保持 `N/A | M0 | N/A | N/A`；纵向关系保持有理由 N/A，未强造递进。

## 4. R01—R10 与 P0/P1/P2

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 《氓》《离骚》题名、作者、诗句、教材提示、任务页码与 canonical PDF 一致；未发现作者或关键文本事实张冠李戴。 |
| R02 | **是** | EV-014 的引号短引不能在 canonical 课标逐字定位；EV-003/004 对 KP-005/006 的 Claim—短引 span 也未完全闭合，需补引文或收窄主张。 |
| R03 | 否 | 两个正文子文本、导语、学习提示、任务、课标、M0/N/A、教师用书和证据表模块齐全。 |
| R04 | **是** | EV-014 将课标多个质量描述压缩为非原文短句，却以引号和 `verified` 呈现，实质上把研究性综合表述成规范直接引文。 |
| R05 | **是** | KP-014 的主维度“思维”不在冻结 taxonomy 的 `knowledge_dimensions=[人文, 语言]` 中，属于原子 KP 受控字段违规；同时其证据 span 尚未完全闭合。 |
| R06 | 否 | 高考仅保留结构化 M0，未引用未登记真题、答案或评分 Artifact。 |
| R07 | 否 | 当前卡只消费已登记教材包、任务包和现行课标，不依赖未验收下游产物。 |
| R08 | 否 | 卡片、Source、Artifact、版本、ID、16 KP/15 EV数量和 ledger 绑定一致；当前问题是证据语义/枚举而非版本断链。 |
| R09 | 否 | 使用现行 2020 修订课标的“文学阅读与写作”和语言积累关联，不改写任务群名称或把任务群当固定教法。 |
| R10 | 否 | 未机械铺满四项核心素养，也未把学业质量水平当作单课难度标签；EV-014 的问题是引文真实性，不是等级越级。 |

`P0/P1/P2 = 0/2/0`。两项 P1 均可局部修复，但在修复并重新计算 SHA、重跑结构检查前，不得进入独立第二复审或被单元图谱消费。

## 5. 知识卡量表评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **18.5** | 15/15 EV 均有 Source/Artifact/页码；但 EV-014 非逐字 canonical 引文，且 EV-003/004 对 KP-005/006 的相关短引 span 不完整。 |
| 事实与术语准确性 | 20 | 18 | **16.5** | 两篇诗正文、教材提示和任务事实准确；课标短引被重写，且“思维”不是冻结维度枚举。 |
| 字段完整与知识粒度 | 15 | 12 | **12.5** | 2/2 子文本、16/16 KP、15/15 EV和模块齐全；一项主维度非法、两项 Claim—EV 需补 span，保守扣2.5。 |
| 双维度与母题质量 | 15 | 12 | **13.0** | 人文/语言母题覆盖古典源流、婚姻处境、人格理想、比兴/象征/节奏与跨文本比较；KP-014 的“思维”维度需改回受控双线。 |
| 四层与高考映射 | 10 | 8 | **9.0** | 16 个 KP 均有四层理由，M0和不确定性边界清楚；受控维度问题不影响 M0，但降低可消费性。 |
| 纵向贯通 | 8 | 6 | **8.0** | 无双方均完成同版本复核的目标时保持理由充分的 N/A。 |
| 教学可用性与表达 | 7 | 5 | **6.0** | 学习提示、任务成果、项目建议和教师用书缺源分离，流程可操作；非规范课标短引和维度枚举会误导下游检索。 |
| **合计** | **100** | **85** | **83.5** | 总分低于校准要求，证据链/准确性两个维度未达最低门槛；不通过。 |

## 6. 返工建议与决定

### 必须修复（P1）

1. 将 `KP-CARD-X3-U01-01-014` 的主维度从“思维”改为 taxonomy 允许的“语言”（或依据卡片双线重写为“人文”，但不得新增“思维”枚举），并保持判定理由与教学动作一致。
2. 将 EV-014 改成 canonical 课标逐字短引，建议采用物理页44/印刷页36的水平2-3或4-3原文，例如：“能结合作品的具体内容，阐释作品的情感、形象、主题和思想内涵，能对作品的表现手法作出自己的评论。”同时保留“本卡不据此判定完整水平”的边界说明；不得用综合改写句加引号替代。
3. 补齐 EV-004 的 `“士也罔极，二三其德”` 与 `“信誓旦旦，不思其反”` 等对应 span，或将 KP-005/006 的陈述收窄到当前短引实际覆盖的诗句；重做 Claim—EV 逐条闭合。

### 修复后门禁

修复后必须重新计算卡片 SHA，更新 ledger 的审查绑定（不得覆盖本报告绑定的旧 SHA），重新运行 validator，并以新 SHA 重新进行 primary/secondary 双审。本报告的 `rework` 决定不等同于状态写回。

**主审决定：`rework`。** 当前卡片不得进入 accepted 或单元图谱消费；完成上述三项局部修复并通过新一轮独立复核后，才可重开审查。

## 7. 可复现绑定

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-01.md`；v0.2.0；SHA `acca68281bb932deab7b06db04ae7ab41d50bde04a6a19343d3d8b6a1a18306c`。
- Canonical 教材：`ART-PKG-X3-001-PDF` SHA `419c519e66287a19a9ea277b39ba8d17c1d991ab8f7d0051861daa8777cb6ba0`；任务：`ART-PKG-X3-005-PDF` SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；课标：`ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- ledger：`work/knowledge/_meta/deliverables.jsonl` SHA `01cb8097b62863811410df023eda38137f19ceb8dcaa5bd0c424207a59b54189`。
- validator：`VAL-20260808-205806+0800`；latest/archive SHA `b014b2146714512c6877922c36fcd493ca34055c8f70458c8b487b28571fcb5b`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
