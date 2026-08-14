---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U02-03-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U02-03"
artifact_version: "0.2.0"
artifact_sha256: "cc77e289d5667e1b91e07b0658f02e9c0d4b50f2eb39bb5ab5c0e40b43692a6b"
review_round: 1
reviewer: "independent_primary_x3_u02_03_r1"
review_role: "primary"
reviewed_at: "2026-08-08T23:15:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "c36568758b999271f0c95ff5e6b6a48b08f4fd895bd0f33ca193623790aa52b5"
validator_run_id: "VAL-20260808-230336+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-230336+0800.json"
validator_report_sha256: "1828d16c3aba55e032f17762225bc3970c23cddbe0aebf3c1f7d6173b4f2ce3d"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "1d678fbf8644e39ebf155e3082e9b909944e84ee04100de7d0d49095ba1b4095"
---

# CARD-X3-U02-03 v0.2.0 独立主审 R1

## 1. 输入锁定与状态一致性

本轮从当前 v0.2.0 快照开始独立主审，仅依据卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 课7教材、U02单元研习任务、现行课标、共享账本和指定 validator 归档报告复核；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U02-03.md`；v0.2.0；SHA `cc77e289d5667e1b91e07b0658f02e9c0d4b50f2eb39bb5ab5c0e40b43692a6b`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `c36568758b999271f0c95ff5e6b6a48b08f4fd895bd0f33ca193623790aa52b5`；CARD-X3-U02-03 为 v0.2.0/`linted`，REBUILD transition 一致 |
| 课7 canonical | `ART-PKG-X3-008-PDF`；SHA `b0767d09d076ec0284dd9aae73d346e18039671bc6dd0cb80df6c18e64da7af5`；《一个消逝了的山村》物理页52—54、《秦腔》物理页55—59、学习提示物理页59 |
| U02任务 canonical | `ART-PKG-X3-010-PDF`；SHA `ad805e6349d35afe4845ecb463a4cc062d6add372daffe5f655fc464d40b0a7c`；物理页72—73 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群10物理页31—33、学业质量4-3物理页46 |
| validator | `VAL-20260808-230336+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `1828d16c3aba55e032f17762225bc3970c23cddbe0aebf3c1f7d6173b4f2ce3d` |

卡片 front matter 的 `status: linted`、`reviewers: []` 与正文“尚未完成独立主审和独立第二复审；当前仅进入 linted”一致；ledger 同步为 v0.2.0/`linted`。状态元数据不触发 R08。

## 2. 覆盖、证据与边界复核

- 卡片覆盖 2 个正文子文本：《一个消逝了的山村》物理页52—54/切页1—3，《秦腔》物理页55—59/切页4—8；学习提示位于物理页59/切页8；U02任务物理页72—73；课标任务群10在物理页31—33，学业质量4-3在物理页46。
- `19/19` KP 均有唯一 ID、合法主维度（仅“人文/语言”）、冻结知识类型（事实/概念/程序/策略/解释/价值辨析）、四层主归属、判定理由、证据 ID 和置信状态；`19/19` EV 均为单值 `Q/F/M/D`（Q=14、F=1、M=2、D=2）。
- EV-001—012 覆盖两篇正文和山村遗迹、自然联想、秦腔地域/声音/场面/人民生活；EV-013—014 只承担学习提示；EV-015—016 只承担 U02任务；EV-017—018 只承担课标任务群10与学业质量4-3；EV-019 单独承担教师用书/外部解释边界。来源职责未混写。
- 课文物理页、切分页、印刷页和 MinerU 辅助路径可回查；正式证据回到 canonical PDF。学习提示的景物哲思、秦腔与人民的血肉联系、任务二作家风格研讨和任务三语言鉴赏札记均有对应证据。
- 高考栏严格保持 `N/A / M0 / N/A`，不消费未登记真题、答案或评分资料；纵向关系合法保持 N/A；教师用书 `edition_match=unknown`。

## 3. Claim—Evidence 复核与剩余风险

《一个消逝了的山村》的旧路、山村遗迹、泉水共同生活、鼠麹草/彩菌/加利树联想和生命关联结尾由 EV-003—007 支撑；《秦腔》的地域声韵、劳作苦乐、演出场面、声音细节、礼俗和文化意蕴由 EV-008—012 支撑；学习提示 EV-013—014、任务 EV-015—016 与课标 EV-017—018 的职责已分离。

本轮未发现事实错误、来源错配或字段缺失。发现一项非阻断性边界维护项：KP-016 将“回引两个以上正文细节”写成任务产出，但 EV-015/017 的教材任务与课标并未规定该数量；应删去数量或明确标为本项目建议。KP-017 的“含着笑”跨课示例也应继续保持项目建议属性，或改用本课“彩菌/秦腔”实例。两者不影响正文事实、正式证据链和当前通过，但进入 accepted 前建议收窄。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | 两篇散文题名、作者、山村遗迹、自然物、秦腔地域/人民生活、形式和课标术语与 canonical 载体一致。 |
| R02 | 否 | 19/19 EV 均有适配 Source、Artifact、locator、短引和验证状态；KP-016 的任务数量要求是局部维护项，核心主张仍有适配来源和可回查定位。 |
| R03 | 否 | 2个正文子文本、学习提示、U02任务、课标、19个KP、教学模块、M0和纵向N/A齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标 M、教师用书 D 和项目建议分层；“哲思之美”“血肉联系”“文化意蕴”等为有边界的学习方向，不冒充唯一阐释。 |
| R05 | 否 | 19/19 KP 均具备合法维度、受控知识类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，未引用未登记真题、答案或评分资料，也未声称 M1—M3 直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课7教材、U02任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、19 KP、19 EV、版本、路径和 SHA 一致；`linted` 状态与 `reviewers: []` 一致。 |
| R09 | 否 | 使用现行课标任务群10“中国现当代作家作品研习”和物理页46的4-3定位，未改写任务群或把质量描述当作课型。 |
| R10 | 否 | 人文/语言双线按文本需要展开，未机械铺满四项核心素养，也未把学业质量4-3当作单课完整等级或题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键事实错误、证据缺失、边界混写、非法枚举、版本漂移或高考越权。 |
| P2 | 1 | `P2-U02-03-TASK-SCOPE`：KP-016 的“两个以上正文细节”不是 EV-015/017 明示的任务数量，KP-017 的跨课“含着笑”实例应标为项目建议或改用本课实例。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | 19/19 EV 的来源、canonical Artifact、物理/切页、短引和状态闭合；对任务数量及跨课示例边界保守扣分。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两篇散文事实、秦腔地域/文化术语、任务群10和4-3术语准确；开放解释均保留边界。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2/2正文子文本、19/19 KP、19/19 EV、学习提示/任务/课标/M0模块齐全。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文与语言双线覆盖山村历史/自然联想、秦腔声音/场面/人民生活、地方文化与比较研习。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标任务群10、学业质量4-3和 M0 边界合规。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方 accepted 目标时合法使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 三类提示分离，景物—联想、场面—声音证据表和800字语言札记路径可直接用于备课。 |
| **合计** | **100** | **85** | **98.0** | **总分及七维单项均达标；P2为非阻断性的任务边界维护项。** |

## 7. 主审决定

**决定：`pass`；总分 `98.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/1`。**

当前 `CARD-X3-U02-03` v0.2.0/SHA `cc77e289d5667e1b91e07b0658f02e9c0d4b50f2eb39bb5ab5c0e40b43692a6b` 通过本轮独立主审，可与同一 SHA 的独立第二复审配对进入后续流程；建议配对前收窄 KP-016/KP-017 的项目建议边界。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、validator 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U02-03.md`；v0.2.0；SHA `cc77e289d5667e1b91e07b0658f02e9c0d4b50f2eb39bb5ab5c0e40b43692a6b`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `c36568758b999271f0c95ff5e6b6a48b08f4fd895bd0f33ca193623790aa52b5`；版本 `0.2.0`、状态 `linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-230336+0800.json`；SHA `1828d16c3aba55e032f17762225bc3970c23cddbe0aebf3c1f7d6173b4f2ce3d`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-008-PDF`=`b0767d09d076ec0284dd9aae73d346e18039671bc6dd0cb80df6c18e64da7af5`；`ART-PKG-X3-010-PDF`=`ad805e6349d35afe4845ecb463a4cc062d6add372daffe5f655fc464d40b0a7c`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填该值。
