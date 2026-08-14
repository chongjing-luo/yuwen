---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X3-U01-R2-PRIMARY-INDEPENDENT"
deliverable_id: "UNIT-X3-U01"
artifact_version: "0.2.2"
artifact_sha256: "34e6f0fed8a102843c81524f55add86917be584b2ad647a47358d16602ae86ab"
review_round: 2
reviewer: "independent_primary_unit_x3_u01_r2"
review_role: "primary"
reviewed_at: "2026-08-09T02:24:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "551802207634ae5eaaaf5de058362bd973b321d08be4168bcc008c6229433957"
validator_run_id: "VAL-20260809-022241+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u01_unit_final_pre_review_v022_20260809.json"
validator_report_sha256: "cd5998129e0da0b1ef85c4368fbed0e71b946d5217696e4c540da7cbaae9bdae"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "428c5d1e30baa97ac5ab5a3ad1fd6d613d448734c2a2faf79e6adf56e2e4bcbd"
---

# UNIT-X3-U01 v0.2.2 独立主审 R2

## 1. 锁定对象与上游门禁

本轮从当前快照重新独立复核 U01 单元图谱，不复用 v0.2.1 结论，不修改图谱、四张上游卡、ledger、validator 或状态迁移。采用冻结的 `2.0-textbook` 单元图谱量表：总分门槛 88，七维最低分 `22/16/12/12/8/8/4`。

| 对象 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修下册/units/UNIT-X3-U01.md`；v0.2.2；SHA `34e6f0fed8a102843c81524f55add86917be584b2ad647a47358d16602ae86ab`；状态 `linted` |
| 上游卡01 | `CARD-X3-U01-01` v0.2.1，ledger `accepted`，post SHA `48b418867024c97179db6f13a1e120938197d97bfe0db9467db24d531f5df9d6` |
| 上游卡02 | `CARD-X3-U01-02` v0.2.2，ledger `accepted`，post SHA `6b133b93f37ddbd22dc5e21eed7bdb9eb7c0bc6d923e24b7c8e3ae74fb4da0a9` |
| 上游卡03 | `CARD-X3-U01-03` v0.2.5，ledger `accepted`，post SHA `50e07df1126e83534832b704e270baa0e2ff9ae679cfab54d7022dd4e53c0873` |
| 上游卡04 | `CARD-X3-U01-04` v0.2.5，ledger `accepted`，post SHA `b274580dde4e276d2b4fcce3ec003761451b8cc853af7e212dcb3506e54dd49c` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `551802207634ae5eaaaf5de058362bd973b321d08be4168bcc008c6229433957`；U01 条目为 v0.2.2/`linted`，路径、source_ids、upstream_card_ids 与图谱一致 |
| validator | `VAL-20260809-022241+0800`；`work/knowledge/_meta/validation_reports/x3_u01_unit_final_pre_review_v022_20260809.json`；SHA `cd5998129e0da0b1ef85c4368fbed0e71b946d5217696e4c540da7cbaae9bdae`；`passed`、0 errors、`hash_verification=true` |

四张上游卡均为当前 ledger 的 `accepted` 版本，图谱 §1 中的四个 post SHA 与 ledger、实际卡文件 SHA 逐一一致。图谱只消费已登记的 U01 任务包、卡片证据和现行 2020 修订课标；未消费教师用书、未登记真题或外部解析。

## 2. 结构、覆盖与双维度复核

- 四卡 KP 数量为 `16+16+16+17=65`；§1.1 逐一列出全部稳定 `KP-CARD-X3-U01-*`，独立展开为 `65/65`，无漏项、重复或跨卡混淆。四卡综合入口和任务二评价证据均使用完整 Card/KP-ID；此前裸 KP 缩写已闭合。
- 6 个人文节点和 6 个语言节点均有稳定 ID、来源 Card/KP 与 EV 回链。人文线覆盖诗歌源流、婚恋与主体处境、人格操守/忧患、山河城市空间、盛衰对照和当代审美责任；语言线覆盖体式、比兴意象、叙事对话、复沓典故声音、鉴赏表达程序和文言/诗歌语言梳理。
- 4 个单元任务均有 `SRC-PKG-X3-005`、`ART-PKG-X3-005-PDF` 及物理页 25—26 定位，列出能力动作、学习成果、评价证据和对应 KP/EV。任务二现在明确使用 `KP-CARD-X3-U01-01-016`、`KP-CARD-X3-U01-02-016`；≥800 字鉴赏文章、研讨、比较表和合作编集均标为任务成果，不冒充教材正文结论。
- 11 条 `REL-UNIT-X3-U01-*` 均有稳定 REL-ID、受控 taxonomy 类型、双方 KP 与 EV 回链；关系类型计数为比较 6、迁移 3、组成 1、例证 1。关系分别覆盖婚恋叙事、主体价值、山河/城市空间、盛衰记忆、意象例证和鉴赏方法迁移，且明确不抹平文本语境差异。
- v0.2.2 将 `KP-CARD-X3-U01-02-001` 的正式证据边界纳入 `L-U01-06`，该语言节点现在同时区分正文、学习提示、任务和课标证据，不把现代直译或项目化要求当作教材明示。

## 3. 综合关系、M0 与边界复核

关系表的共性、差异和理由均来自四张 accepted 卡。REL-01 保留《氓》第一人称回顾/决绝与《孔雀东南飞》多轮对话、家族逼迫的差异；REL-03 区分《离骚》的修德忧患与《蜀相》的功业追慕；REL-04—06 区分蜀道险阻、承平城市和劫后空城的时间/空间语境；REL-07 的比兴例证不把桑叶与鸟道等同；REL-08—10 是可回链的鉴赏程序、语言辨析和声音/节奏迁移或比较；REL-11 只表示任务成果链的组成。未将单元顺序、主题相似性或泛化价值判断替代证据。

高考栏保持结构化 `N/A | M0 | N/A`，明确尚未登记“真题题文—答案/评分—教材 KP”逐小问闭合证据；不把古诗词情感、意象、典故、比较或鉴赏的一般题型相似性升级为 M1—M3。前序/后续递进均保留带 `na_reason` 的 N/A；教师用书维持 `edition_match=unknown`，不消费缺失版本意见。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 四张 accepted 卡覆盖导语及七篇诗词文本、U01 任务和课标边界；关系中的叙事、空间、盛衰与语言判断可回到 canonical 证据。 |
| R02 | 否 | 65/65 KP、6 H、6 L、4 TASK、11 REL 均有适配 Card/KP/EV 或任务来源；人文解释和关系陈述保留文本证据及差异，L-U01-06 的正式证据范围也已补齐。 |
| R03 | 否 | 上游清单、逐项 KP 索引、任务拆解、双维度节点、11 条关系、M0、纵向 N/A、Issue 和自检模块齐全。 |
| R04 | 否 | 教材正文/学习提示、卡片解释、任务原文、课标定位、项目评价和单元综合分层清楚；未将研究解释或项目要求冒充教材明示。 |
| R05 | 否 | 四卡全部 65 个 KP 均被索引并进入人文/语言节点、任务或关系入口；任务二两个评价 KP 和新增 U01-02-001 语言边界均可解析，无孤立 KP。 |
| R06 | 否 | 高考仅保留合法结构化 M0，未引用未登记真题、答案或评分资料，也未建立越级 M1—M3 边。 |
| R07 | 否 | 四张上游卡均为 `accepted`，图谱 §1 post SHA 与当前卡文件、ledger 一致；任务包和课标 artifact 已登记。 |
| R08 | 否 | 图谱版本、路径、卡/KP/EV/TASK/REL ID、数量、SHA、ledger 条目和 validator 绑定一致；任务二裸 KP 已补为完整 Card/KP-ID，L-U01-06 新入口同步。 |
| R09 | 否 | 使用现行 2020 修订课标的“文学阅读与写作”等任务群定位及学业质量 4-3 边界，未改写任务群名称或把课标描述当固定教法/达成水平。 |
| R10 | 否 | 人文/语言双维度依七篇诗词和四项任务实际展开，未机械铺满四项核心素养，也未把学业质量水平当题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键覆盖缺失、非法关系类型、未验收上游、M0 越级、教师用书混入、版本漂移或上游 SHA 断链。 |
| P2 | 0 | 未发现影响检索和复核的非阻断缺陷；任务二 Card/KP-ID、语言边界、关系计数和证据边界均已闭合。 |

## 6. 单元图谱诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 4/4 accepted 卡、65/65 KP、4/4 任务、6 H/6 L 和 11/11 REL 均有稳定入口；§1.1 索引、任务二 KP 和新增语言边界一致。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **19.0** | 11 条关系均有受控类型、共性/差异或迁移理由及双方证据；对婚恋、空间、盛衰与鉴赏方法的语境限制清楚，宽范围证据引用保守扣 1 分。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | 6 个 H 与 6 个 L 节点覆盖七篇诗词、任务群活动、体式/意象/叙事/声音和鉴赏表达程序，L-U01-06 的正式来源边界已闭合。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 4 项任务均有物理页 25—26、能力动作、成果、评价证据和上游 KP/EV 入口；任务二两个 KP 已为稳定完整 ID。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | `N/A | M0 | N/A`、双向证据缺口和禁止越级条件明确；未以题型相似性制造映射。 |
| 前后递进 | 10 | 8 | **10.0** | 前/后单元缺少双方 accepted 逐边证据时使用有理由的 N/A，未强造册级递进。 |
| 可读性与检索性 | 5 | 4 | **5.0** | §1.1 完整索引、任务/双维度/关系表、M0、Issue 和版本自检齐全；完整 ID、数量和修订边界可直接复核。 |
| **合计** | **100** | **88** | **99.0** | **总分及七维单项均达标；R01—R10 全部未触发。** |

## 7. 独立主审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `UNIT-X3-U01` v0.2.2/SHA `34e6f0fed8a102843c81524f55add86917be584b2ad647a47358d16602ae86ab` 通过独立主审，可进入同一 SHA 的独立第二复审。本报告只闭合主审，不写回 ledger 或执行 `accepted` 状态迁移；图谱、任一上游卡、canonical artifact、validator、rubric/taxonomy 或版本绑定变化时，本报告失效并须按新 SHA 全量复审。

## 8. 可复现绑定与报告校验

- 图谱：`work/knowledge/选择性必修下册/units/UNIT-X3-U01.md`；v0.2.2；SHA `34e6f0fed8a102843c81524f55add86917be584b2ad647a47358d16602ae86ab`。
- accepted 上游 post SHA：`CARD-X3-U01-01=48b418867024c97179db6f13a1e120938197d97bfe0db9467db24d531f5df9d6`；`CARD-X3-U01-02=6b133b93f37ddbd22dc5e21eed7bdb9eb7c0bc6d923e24b7c8e3ae74fb4da0a9`；`CARD-X3-U01-03=50e07df1126e83534832b704e270baa0e2ff9ae679cfab54d7022dd4e53c0873`；`CARD-X3-U01-04=b274580dde4e276d2b4fcce3ec003761451b8cc853af7e212dcb3506e54dd49c`。
- canonical 课标 artifact：`ART-CURR-2020-PDF`，SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；U01 任务 artifact `ART-PKG-X3-005-PDF` 已登记并验证。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `551802207634ae5eaaaf5de058362bd973b321d08be4168bcc008c6229433957`。
- validator：`work/knowledge/_meta/validation_reports/x3_u01_unit_final_pre_review_v022_20260809.json`；run `VAL-20260809-022241+0800`；SHA `cd5998129e0da0b1ef85c4368fbed0e71b946d5217696e4c540da7cbaae9bdae`；`passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。
