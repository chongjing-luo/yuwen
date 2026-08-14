---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U02-01-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U02-01"
artifact_version: "0.2.0"
artifact_sha256: "2b4fbe156972ff8848ae6ee1ea51767e3b467f7f6e7f1e960458a506f812e572"
review_round: 1
reviewer: "independent_primary_x3_u02_01_r1"
review_role: "primary"
reviewed_at: "2026-08-08T22:50:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "97a4396223bd660d44ba6942ca76e441a6305984280f19b0d069a6af6ed540ad"
validator_run_id: "VAL-20260808-224552+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-224552+0800.json"
validator_report_sha256: "0f6f86c25ecfb8e2cd20f90084d3114a344d8ebe21b28c55449fdc2b7e3fedb2"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "f38d7c75b11c00a84c4fe12c3ad0550c9e7f9ad930fffc61791274ef42085c12"
---

# CARD-X3-U02-01 v0.2.0 独立主审 R1

## 1. 输入锁定与状态一致性

本轮从当前 v0.2.0 快照开始独立主审，仅依据卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 课文包、U02单元研习任务、现行课标、共享账本和指定 validator 归档报告复核；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U02-01.md`；v0.2.0；SHA `2b4fbe156972ff8848ae6ee1ea51767e3b467f7f6e7f1e960458a506f812e572`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `97a4396223bd660d44ba6942ca76e441a6305984280f19b0d069a6af6ed540ad`；CARD-X3-U02-01 为 v0.2.0/`linted`，REBUILD transition 一致 |
| 课文 canonical | `ART-PKG-X3-006-PDF`；SHA `901a5c9228fc7a8d65ba0ef195da556adaf7bb0aefdc159345288f19eedbf73b`；《阿Q正传》物理页27—33、《边城》物理页34—44、学习提示物理页45 |
| U02任务 canonical | `ART-PKG-X3-010-PDF`；SHA `ad805e6349d35afe4845ecb463a4cc062d6add372daffe5f655fc464d40b0a7c`；物理页72—73 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群10物理页31—33、学业质量4-3物理页46 |
| validator | `VAL-20260808-224552+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `0f6f86c25ecfb8e2cd20f90084d3114a344d8ebe21b28c55449fdc2b7e3fedb2` |

卡片 front matter 的 `status: linted`、`reviewers: []` 与正文“尚未完成独立主审和独立第二复审；当前仅进入 linted”一致；ledger 同步为 v0.2.0/`linted`。状态元数据不触发 R08。

## 2. 覆盖、证据与边界复核

- 卡片覆盖 2 个正文子文本：《阿Q正传》（节选）物理页27—33/切页1—7，《边城》（节选）物理页34—44/切页8—18；学习提示位于物理页45/切页19；U02任务物理页72—73；课标任务群10在物理页31—33，学业质量4-3在物理页46。
- `19/19` KP 均有唯一 ID、合法主维度（仅“人文/语言”）、冻结知识类型（事实/概念/程序/策略/解释/价值辨析）、四层主归属、判定理由、证据 ID 和置信状态；`17/17` EV 均为单值 `Q/F/M/D`（Q=11、F=2、M=2、D=2）。
- EV-001—010 覆盖两篇正文和关键人物/语言/风俗事实；EV-011—012 只承担教材学习提示；EV-013—014 只承担 U02任务；EV-015—016 只承担课标任务群10与学业质量4-3；EV-017 单独承担教师用书/外部解释边界。来源职责未混写。
- 课文物理页、切分页、印刷页和 MinerU 辅助路径可回查；正式证据回到 canonical PDF，不把 MinerU 提取文本当作规范来源。学习提示中的历史背景、人物与艺术手法，任务中的“说不尽的阿Q”“《边城》中的‘矛盾’”、研讨会和语言鉴赏札记均有对应证据。
- 高考栏严格保持 `N/A / M0 / N/A`，不消费未登记真题、答案或评分资料；纵向关系合法保持 N/A；教师用书 `edition_match=unknown`。

## 3. Claim—Evidence 复核与剩余风险

《阿Q正传》的身份、社会关系、犯讳、受辱、精神胜利法和“得胜”叙述由 EV-003—005 支撑；《边城》的地方风俗、人物关系、翠翠等待/误会和唢呐句式由 EV-007—010 支撑；两篇学习提示的风格、人物、艺术手法、风俗景物和悲喜并置由 EV-011—012 支撑；任务 EV-013—014 与课标 EV-015—016 的职责已分离。

本轮未发现事实错误、来源错配或字段缺失。少数复合 Claim（如犯讳词语链、人物关系链和语言鉴赏例句）使用页级 locator 或压缩短引，但 locator 覆盖完整原文、证据 ID 适配且可回查；这属于可选的短引细化，不构成阻断性缺陷。KP-017 的“得胜/忽忽不乐”例句可在正文 EV-004/005 回查，任务证据 EV-014 负责鉴赏角度与篇幅要求。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | 题名、作者、两篇节选范围、人物事实、风俗、艺术手法和课标术语与 canonical 载体一致。 |
| R02 | 否 | 17/17 EV 均有适配 Source、Artifact、locator、短引和验证状态；复合 Claim 的压缩短引仍有目标页可回查，未出现无适配来源或不可定位直接引文。 |
| R03 | 否 | 2个正文子文本、学习提示、U02任务、课标、19个KP、教学模块、M0和纵向N/A齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标 M、教师用书 D 和项目建议分层；开放的“国民性/理想化现实/悲剧感”等均标为可讨论概括，不冒充唯一答案。 |
| R05 | 否 | 19/19 KP 均具备合法维度、受控知识类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，未引用未登记真题、答案或评分资料，也未声称 M1—M3 直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课文包、U02任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、19 KP、17 EV、版本、路径和 SHA 一致；`linted` 状态与 `reviewers: []` 一致。 |
| R09 | 否 | 使用现行课标任务群10“中国现当代作家作品研习”和物理页46的4-3定位，未改写任务群或把质量描述当作课型。 |
| R10 | 否 | 人文/语言双线按文本需要展开，未机械铺满四项核心素养，也未把学业质量4-3当作单课完整等级或题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键证据缺失、边界混写、非法枚举、版本漂移或高考越权。 |
| P2 | 0 | 未发现影响后续消费的非阻断性缺陷；宽 locator/压缩短引仅为可选表达优化。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | 17/17 EV 的来源、canonical Artifact、物理/切页、短引和状态闭合；对少数压缩短引保守扣分。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两篇小说事实、人物/风俗、任务群10和4-3术语准确；开放解释均保留边界。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2/2正文子文本、19/19 KP、17/17 EV、学习提示/任务/课标/M0模块齐全。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文与语言双线覆盖社会关系、人物、叙述语言、风俗景物、喜剧/悲剧和比较研习。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标任务群10、学业质量4-3和 M0 边界合规。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方 accepted 目标时合法使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 三类提示分离，人物/环境/语言证据表、比较研讨和800字札记路径可直接用于备课。 |
| **合计** | **100** | **85** | **98.0** | **总分及七维单项均达标，R01—R10 全部未触发。** |

## 7. 主审决定

**决定：`pass`；总分 `98.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-U02-01` v0.2.0/SHA `2b4fbe156972ff8848ae6ee1ea51767e3b467f7f6e7f1e960458a506f812e572` 通过本轮独立主审，可与同一 SHA 的独立第二复审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、validator 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U02-01.md`；v0.2.0；SHA `2b4fbe156972ff8848ae6ee1ea51767e3b467f7f6e7f1e960458a506f812e572`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `97a4396223bd660d44ba6942ca76e441a6305984280f19b0d069a6af6ed540ad`；版本 `0.2.0`、状态 `linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-224552+0800.json`；SHA `0f6f86c25ecfb8e2cd20f90084d3114a344d8ebe21b28c55449fdc2b7e3fedb2`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-006-PDF`=`901a5c9228fc7a8d65ba0ef195da556adaf7bb0aefdc159345288f19eedbf73b`；`ART-PKG-X3-010-PDF`=`ad805e6349d35afe4845ecb463a4cc062d6add372daffe5f655fc464d40b0a7c`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填该值。
