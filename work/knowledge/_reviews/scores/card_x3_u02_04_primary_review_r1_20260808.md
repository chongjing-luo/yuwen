---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U02-04-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U02-04"
artifact_version: "0.2.0"
artifact_sha256: "5343c43ccdcf6da0be298417e7e7eeb0823f0aa390cb415964834480d8a9fae9"
review_round: 1
reviewer: "independent_primary_x3_u02_04_r1"
review_role: "primary"
reviewed_at: "2026-08-08T23:35:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "04c90608fd5da71596f648c8698f8269aa9ee7de79241caf1aec6d79a6c6a93f"
validator_run_id: "VAL-20260808-231938+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-231938+0800.json"
validator_report_sha256: "575148558b2ad11b30b94b66bcf91603f33dd5f775cbe9c38423f29f8ed960d6"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "063bc60f2c0bb595b73130b3e9769ec080003a6d70e08562eeaebe0a14ba6640"
---

# CARD-X3-U02-04 v0.2.0 独立主审 R1

## 1. 输入锁定与状态一致性

本轮从当前 v0.2.0 快照开始独立主审，仅依据卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 课8教材、U02单元研习任务、现行课标、共享账本和指定 validator 归档报告复核；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U02-04.md`；v0.2.0；SHA `5343c43ccdcf6da0be298417e7e7eeb0823f0aa390cb415964834480d8a9fae9`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `04c90608fd5da71596f648c8698f8269aa9ee7de79241caf1aec6d79a6c6a93f`；CARD-X3-U02-04 为 v0.2.0/`linted`，REBUILD transition 一致 |
| 课8 canonical | `ART-PKG-X3-009-PDF`；SHA `fa25db433fdda0a9468321de7cada4e84b590f3436125db92f683830957f5bc2`；《茶馆》第一幕物理页60—67、学习提示物理页67 |
| U02任务 canonical | `ART-PKG-X3-010-PDF`；SHA `ad805e6349d35afe4845ecb463a4cc062d6add372daffe5f655fc464d40b0a7c`；物理页72—73 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群10物理页31—33、学业质量4-3物理页46 |
| validator | `VAL-20260808-231938+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `575148558b2ad11b30b94b66bcf91603f33dd5f775cbe9c38423f29f8ed960d6` |

卡片 front matter 的 `status: linted`、`reviewers: []` 与正文“尚未完成独立主审和独立第二复审；当前仅进入 linted”一致；ledger 同步为 v0.2.0/`linted`。状态元数据不触发 R08。

## 2. 覆盖、证据与边界复核

- 卡片覆盖《茶馆》第一幕的 2 个正文片段：物理页60—64/切页1—5与物理页65—67/切页6—8；学习提示位于物理页67/切页8；U02任务物理页72—73；课标任务群10在物理页31—33，学业质量4-3在物理页46。
- `18/18` KP 均有唯一 ID、合法主维度（仅“人文/语言”）、冻结知识类型（事实/概念/程序/策略/解释/价值辨析）、四层主归属、判定理由、证据 ID 和置信状态；`18/18` EV 均为单值 `Q/F/M/D`（Q=13、F=1、M=2、D=2）。
- EV-001—011 覆盖第一幕舞台说明、茶馆空间、人物关系、交易、政治冲突、京味语言和动作；EV-012—013 只承担教材学习提示；EV-014—015 只承担 U02任务；EV-016—017 只承担课标任务群10与学业质量4-3；EV-018 单独承担教师用书/外部解释边界。来源职责未混写。
- 课文物理页、切分页、印刷页和 MinerU 辅助路径可回查；正式证据回到 canonical PDF。学习提示的时代横断面、京味语言、人物语言、结构与表现手法，任务二的作家风格研讨和任务三的语言鉴赏札记均有对应证据。
- 高考栏严格保持 `N/A / M0 / N/A`，不消费未登记真题、答案或评分资料；纵向关系合法保持 N/A；教师用书 `edition_match=unknown`。

## 3. Claim—Evidence 复核与剩余风险

《茶馆》第一幕的时间地点、茶馆公共功能、二德子/常四爷冲突、刘麻子卖女、王利发与秦仲义、乡妇饥饿、庞太监政治台词和幕落由 EV-003—011 支撑；学习提示 EV-012—013、任务 EV-014—015 与课标 EV-016—017 的职责已分离。

本轮未发现事实错误、来源错配或字段缺失。发现一项非阻断性边界维护项：KP-015 将“结合茶馆中的至少两个角色/场景”写成任务产出，但 EV-014 的教材任务只明示选定写作理念、艺术特色或语言风格角度并交流，并未规定该数量；应删去数量或明确标为本项目建议。其余正文、学习提示、M0和教师用书边界可回查。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | 《茶馆》题名、作者、第一幕时间地点、人物、交易/政治冲突、舞台动作和课标术语与 canonical 载体一致。 |
| R02 | 否 | 18/18 EV 均有适配 Source、Artifact、locator、短引和验证状态；KP-015 的任务数量要求是局部维护项，核心主张仍有适配来源和可回查定位。 |
| R03 | 否 | 2个正文片段、学习提示、U02任务、课标、18个KP、教学模块、M0和纵向N/A齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标 M、教师用书 D 和项目建议分层；“社会缩影”“时代沧桑”等概括以学习提示为边界，不冒充完整历史结论。 |
| R05 | 否 | 18/18 KP 均具备合法维度、受控知识类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，未引用未登记真题、答案或评分资料，也未声称 M1—M3 直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课8教材、U02任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、18 KP、18 EV、版本、路径和 SHA 一致；`linted` 状态与 `reviewers: []` 一致。 |
| R09 | 否 | 使用现行课标任务群10“中国现当代作家作品研习”和物理页46的4-3定位，未改写任务群或把质量描述当作课型。 |
| R10 | 否 | 人文/语言双线按戏剧文本需要展开，未机械铺满四项核心素养，也未把学业质量4-3当作单课完整等级或题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键事实错误、证据缺失、边界混写、非法枚举、版本漂移或高考越权。 |
| P2 | 1 | `P2-U02-04-TASK-SCOPE`：KP-015 的“至少两个角色/场景”不是 EV-014 明示的任务数量，应删去或标为本项目建议。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | 18/18 EV 的来源、canonical Artifact、物理/切页、短引和状态闭合；对任务数量边界保守扣分。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 第一幕事实、戏剧术语、任务群10和4-3术语准确；开放解释均保留边界。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2/2正文片段、18/18 KP、18/18 EV、学习提示/任务/课标/M0模块齐全。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文与语言双线覆盖茶馆空间、人物关系、贫困/政治冲突、京味语言、舞台动作和社会横断面。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标任务群10、学业质量4-3和 M0 边界合规。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方 accepted 目标时合法使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 三类提示分离，时间—空间—人物—冲突表和800字语言札记路径可直接用于备课。 |
| **合计** | **100** | **85** | **98.0** | **总分及七维单项均达标；P2为非阻断性的任务边界维护项。** |

## 7. 主审决定

**决定：`pass`；总分 `98.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/1`。**

当前 `CARD-X3-U02-04` v0.2.0/SHA `5343c43ccdcf6da0be298417e7e7eeb0823f0aa390cb415964834480d8a9fae9` 通过本轮独立主审，可与同一 SHA 的独立第二复审配对进入后续流程；建议配对前收窄 KP-015 的项目建议边界。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、validator 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U02-04.md`；v0.2.0；SHA `5343c43ccdcf6da0be298417e7e7eeb0823f0aa390cb415964834480d8a9fae9`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `04c90608fd5da71596f648c8698f8269aa9ee7de79241caf1aec6d79a6c6a93f`；版本 `0.2.0`、状态 `linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-231938+0800.json`；SHA `575148558b2ad11b30b94b66bcf91603f33dd5f775cbe9c38423f29f8ed960d6`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-009-PDF`=`fa25db433fdda0a9468321de7cada4e84b590f3436125db92f683830957f5bc2`；`ART-PKG-X3-010-PDF`=`ad805e6349d35afe4845ecb463a4cc062d6add372daffe5f655fc464d40b0a7c`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填该值。
