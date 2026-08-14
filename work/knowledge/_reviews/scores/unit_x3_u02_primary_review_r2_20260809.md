---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X3-U02-R2-PRIMARY-INDEPENDENT"
deliverable_id: "UNIT-X3-U02"
artifact_version: "0.2.2"
artifact_sha256: "464bba3a461fdb07f0d4fbcc95157f27c3ebaa4afa59a505c6df29f45214e83f"
review_round: 2
reviewer: "independent_primary_unit_x3_u02_r2"
review_role: "primary"
reviewed_at: "2026-08-09T02:32:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "3d039ba22e89c780673ffe404114b945937939ac7b8321ebfb7b36f1271e93f4"
validator_run_id: "VAL-20260809-022936+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u02_unit_final_pre_review_v022_20260809.json"
validator_report_sha256: "0d31570ae63630cbedbdd0313c5b255e8c690a7318e8fb5339e06a8d4201c59e"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "99a6e18988e14d7ddb998e90596941aa6e64651fa9f4bdee04dc4bd5c9c8f3db"
---

# UNIT-X3-U02 v0.2.2 独立主审 R2

## 1. 锁定对象与上游门禁

本轮从当前快照重新独立复核 U02 单元图谱，不复用 v0.2.1 结论，不修改图谱、四张上游卡、ledger、validator 或状态迁移。采用冻结的 `2.0-textbook` 单元图谱量表：总分门槛 88，七维最低分 `22/16/12/12/8/8/4`。

| 对象 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修下册/units/UNIT-X3-U02.md`；v0.2.2；SHA `464bba3a461fdb07f0d4fbcc95157f27c3ebaa4afa59a505c6df29f45214e83f`；状态 `linted` |
| 上游卡01 | `CARD-X3-U02-01` v0.2.0，ledger `accepted`，post SHA `f0814040c695ef9d65b7ddca2b5d8f837e044f85a597ae7a7bfd58da5b8a91b4` |
| 上游卡02 | `CARD-X3-U02-02` v0.2.0，ledger `accepted`，post SHA `1ad573c3d1cfb97876d604970e55129ca18e10e3147c08703bde6f43755c0715` |
| 上游卡03 | `CARD-X3-U02-03` v0.2.1，ledger `accepted`，post SHA `a86827411ce824d72546d98c0e2f9a72dad2e6480f6dca828d2159f71d7c9c78` |
| 上游卡04 | `CARD-X3-U02-04` v0.2.1，ledger `accepted`，post SHA `c56d5511b1a7cd58efc4ab4827b63bb979a6fac48c4b688f719630c3905c3fa7` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `3d039ba22e89c780673ffe404114b945937939ac7b8321ebfb7b36f1271e93f4`；U02 条目为 v0.2.2/`linted`，路径、source_ids、upstream_card_ids 与图谱一致 |
| validator | `VAL-20260809-022936+0800`；`work/knowledge/_meta/validation_reports/x3_u02_unit_final_pre_review_v022_20260809.json`；SHA `0d31570ae63630cbedbdd0313c5b255e8c690a7318e8fb5339e06a8d4201c59e`；`passed`、0 errors、`hash_verification=true` |

四张上游卡均为当前 ledger 的 `accepted` 版本，图谱 §1 中的四个 post SHA 与 ledger、实际卡文件 SHA 逐一一致。图谱只消费已登记的 U02 任务包、卡片证据和现行 2020 修订课标；未消费教师用书、未登记真题或外部解析。

## 2. 结构、覆盖与双维度复核

- 四卡 KP 数量为 `19+18+19+18=74`；§1.1 逐一列出全部稳定 `KP-CARD-X3-U02-*`，独立展开为 `74/74`，无漏项、重复或跨卡混淆。v0.2.2 将此前只出现在索引的 13 个 KP（01-001/002/008、02-001/002/014、03-001/002/004/005/007、04-001/002）分别挂接到 H/L 语义节点，综合入口和任务入口仍使用完整 Card/KP-ID。
- 5 个人文节点和 5 个语言节点均有稳定 ID、来源 Card/KP 与 EV 回链。新增入口补充了题名/作者与材料边界、阿Q艺术手法、诗歌结尾、山村记忆/自然联想和正式证据边界；人文线覆盖普通民众处境、乡土风俗/共同体、尊严伦理/命运、记忆与时代变化和现代文学审美，语言线覆盖小说、诗歌、散文、话剧及共同鉴赏证据链。
- 4 个单元任务均有 `SRC-PKG-X3-010`、`ART-PKG-X3-010-PDF`、母本物理页 72—73/切分页 1—2（印刷页 67—68）定位，写出比较、研讨、语言札记和成果交流的能力动作、学习成果、评价证据和上游 KP/EV 入口。
- 12 条 `REL-X3-U02-*` 均有稳定 REL-ID、受控 taxonomy 类型、双方 KP 与 EV 回链；关系类型计数为比较 8、迁移 2、组成 2。关系覆盖人物处境、共同体/场面、诗歌记忆、跨文体鉴赏程序和任务成果链，均明确共性、差异或迁移边界。

## 3. 综合关系、M0 与边界复核

关系表以四张 accepted 卡的 KP/EV 为边界。REL-001/005 分别比较阿Q、茶馆穷人、康六、大堰河等普通民众的生计、尊严与伦理压力，保留叙事策略差异；REL-003/004 区分边城端午、秦腔演出和茶馆戏剧场面的共同体结构与文体证据；REL-006/009 处理诗歌记忆、色彩节奏和散文场面声音的受限比较；REL-008/010 是可复用的引文—形式—判断鉴赏程序；REL-011/012 仅表示四卡共同构成研讨、评论和札记成果链。新增 13 个 KP 的入口是语义补全，不新增文学史事实，也没有以“现代文学”标签或文体相似性替代来源证据。

高考栏保持结构化 `N/A | M0 | N/A`，明确尚未登记“真题题文—答案/评分—教材 KP”逐小问闭合证据；不把人物、环境、叙述语言、意象、舞台动作或比较题型相似性升级为 M1—M3。前序/后续递进均保留带 `na_reason` 的 N/A；教师用书维持 `edition_match=unknown`，不消费缺失版本意见。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 四张 accepted 卡覆盖导语及七个正文/戏剧文本、U02 任务和课标边界；关系中的人物、共同体、记忆与形式判断可回到 canonical 证据。 |
| R02 | 否 | 74/74 KP、5 H、5 L、4 TASK、12 REL 均有适配 Card/KP/EV 或任务来源；新增 13 个 KP 的语义入口与正式证据边界均可回链。 |
| R03 | 否 | 上游清单、逐项 KP 索引、任务拆解、双维度节点、12 条关系、M0、纵向 N/A、Issue 和自检模块齐全。 |
| R04 | 否 | 教材正文/学习提示、卡片解释、任务原文、课标定位、项目评价和单元综合分层清楚；未将研究解释或项目要求冒充教材明示。 |
| R05 | 否 | 四卡全部 74 个 KP 均被索引并进入人文/语言节点、任务或关系入口；此前仅索引的 13 个 KP 已有 H/L 语义承载，无孤立缺口。 |
| R06 | 否 | 高考仅保留合法结构化 M0，未引用未登记真题、答案或评分资料，也未建立越级 M1—M3 边。 |
| R07 | 否 | 四张上游卡均为 `accepted`，图谱 §1 post SHA 与当前卡文件、ledger 一致；任务包和课标 artifact 已登记。 |
| R08 | 否 | 图谱版本、路径、卡/KP/EV/TASK/REL ID、数量、SHA、ledger 条目和 validator 绑定一致；13 个新增语义入口与 v0.2.2 ledger/validator 绑定一致。 |
| R09 | 否 | 使用现行 2020 修订课标任务群 10（物理页 31—33）及学业质量 4-3 边界，未改写任务群名称或把课标描述当固定教法/达成水平。 |
| R10 | 否 | 人文/语言双维度依七个文本、四种文体和四项任务实际展开，未机械铺满四项核心素养，也未把学业质量水平当题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键覆盖缺失、非法关系类型、未验收上游、M0 越级、教师用书混入、版本漂移或上游 SHA 断链。 |
| P2 | 0 | 未发现影响检索和复核的非阻断缺陷；13 个 KP 语义入口、关系计数和四类文体证据边界均已闭合。 |

## 6. 单元图谱诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 4/4 accepted 卡、74/74 KP、4/4 任务、5 H/5 L 和 12/12 REL 均有稳定入口；13 个新增 KP 已纳入 H/L 语义节点。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **19.0** | 12 条关系均有受控类型、共性/差异或迁移理由及双方证据；跨文体比较保留人物、场面、记忆和形式差异，宽范围证据引用保守扣 1 分。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | 5 个 H 与 5 个 L 节点覆盖七个文本、四种文体、共同体/时代经验和共同鉴赏程序；新增材料边界、艺术手法和记忆入口均可回链。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 4 项任务均有物理页 72—73、能力动作、成果、评价边界和上游 KP/EV 入口。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | `N/A | M0 | N/A`、双向证据缺口和禁止越级条件明确；未以题型相似性制造映射。 |
| 前后递进 | 10 | 8 | **10.0** | 前/后单元缺少双方 accepted 逐边证据时使用有理由的 N/A，未强造册级递进。 |
| 可读性与检索性 | 5 | 4 | **5.0** | §1.1 完整索引、任务/双维度/关系表、M0、Issue 和版本自检齐全；新增 KP、完整 ID、数量和文体边界可直接复核。 |
| **合计** | **100** | **88** | **99.0** | **总分及七维单项均达标；R01—R10 全部未触发。** |

## 7. 独立主审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `UNIT-X3-U02` v0.2.2/SHA `464bba3a461fdb07f0d4fbcc95157f27c3ebaa4afa59a505c6df29f45214e83f` 通过独立主审，可进入同一 SHA 的独立第二复审。本报告只闭合主审，不写回 ledger 或执行 `accepted` 状态迁移；图谱、任一上游卡、canonical artifact、validator、rubric/taxonomy 或版本绑定变化时，本报告失效并须按新 SHA 全量复审。

## 8. 可复现绑定与报告校验

- 图谱：`work/knowledge/选择性必修下册/units/UNIT-X3-U02.md`；v0.2.2；SHA `464bba3a461fdb07f0d4fbcc95157f27c3ebaa4afa59a505c6df29f45214e83f`。
- accepted 上游 post SHA：`CARD-X3-U02-01=f0814040c695ef9d65b7ddca2b5d8f837e044f85a597ae7a7bfd58da5b8a91b4`；`CARD-X3-U02-02=1ad573c3d1cfb97876d604970e55129ca18e10e3147c08703bde6f43755c0715`；`CARD-X3-U02-03=a86827411ce824d72546d98c0e2f9a72dad2e6480f6dca828d2159f71d7c9c78`；`CARD-X3-U02-04=c56d5511b1a7cd58efc4ab4827b63bb979a6fac48c4b688f719630c3905c3fa7`。
- canonical 课标 artifact：`ART-CURR-2020-PDF`，SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；U02 任务 artifact `ART-PKG-X3-010-PDF` 已登记并验证。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `3d039ba22e89c780673ffe404114b945937939ac7b8321ebfb7b36f1271e93f4`。
- validator：`work/knowledge/_meta/validation_reports/x3_u02_unit_final_pre_review_v022_20260809.json`；run `VAL-20260809-022936+0800`；SHA `0d31570ae63630cbedbdd0313c5b255e8c690a7318e8fb5339e06a8d4201c59e`；`passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。
