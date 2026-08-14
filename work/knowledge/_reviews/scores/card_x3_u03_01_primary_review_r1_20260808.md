---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U03-01-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U03-01"
artifact_version: "0.2.0"
artifact_sha256: "7a5df02059327d0cdc7d35ddbbb2f789c00c38df7025ef97fc168caaba0050f6"
review_round: 1
reviewer: "independent_primary_x3_u03_01_r1"
review_role: "primary"
reviewed_at: "2026-08-08T23:50:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "3d04600b7d09112135b8bd9e0a9ca3638875e33c6342ef506b33a6767e07219c"
validator_run_id: "VAL-20260808-233432+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-233432+0800.json"
validator_report_sha256: "89bbb8c8794320a471d53708c622045495e8209bea9206a4afaa6cbd60521ec2"
validator_result: "passed"
decision: "rework"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "2f539ed8c5d3db71542a9b270843562222bd9b24bda84a665b457b337f24bfb8"
---

# CARD-X3-U03-01 v0.2.0 独立主审 R1

## 1. 输入锁定与状态一致性

本轮从 v0.2.0 快照重新进行独立主审，仅依据当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、课9《陈情表》《项脊轩志》及导语/学习提示、U03单元研习任务、现行课标、共享账本和指定 validator 归档报告复核；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U03-01.md`；v0.2.0；SHA `7a5df02059327d0cdc7d35ddbbb2f789c00c38df7025ef97fc168caaba0050f6`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `3d04600b7d09112135b8bd9e0a9ca3638875e33c6342ef506b33a6767e07219c`；CARD-X3-U03-01 为 v0.2.0/`linted`，含 `REBUILD drafted→linted` 记录 |
| 课9 canonical | `ART-PKG-X3-011-PDF`；SHA `c39d21aa9ebabe1870de3d2f4b5d07676217214ec24d846d7cdf5eec9b3c8b8e`；导语物理页74、两文正文物理页75—78、学习提示物理页79 |
| U03任务 canonical | `ART-PKG-X3-015-PDF`；SHA `e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；物理页90—91 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群8物理页29—30、学业质量4-3物理页46 |
| validator | `VAL-20260808-233432+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `89bbb8c8794320a471d53708c622045495e8209bea9206a4afaa6cbd60521ec2` |

卡片 front matter 的 `status: linted`、`reviewers: []`、正文“尚未完成独立主审和独立第二复审”与 ledger 状态一致；状态元数据不触发 R08。

## 2. 覆盖、证据与事实复核

- 卡片覆盖 U03 导语、课9两篇正文和学习提示：导语物理页74/切页1，《陈情表》物理页75—77/切页2—4，《项脊轩志》物理页77—78/切页4—5，学习提示物理页79/切页6；U03任务物理页90—91。
- `20/20` KP 均有唯一 ID、合法主维度（仅“人文/语言”）、冻结知识类型（事实/概念/程序/策略/解释/价值辨析）、四层主归属、判定理由、证据 ID 和置信状态；`20/20` EV 均为单值 `Q/F/M/D`（Q=16、F=1、M=2、D=1）。
- 导语关于魏晋至明代六篇经典散文、反复诵读/涵泳/梳理/评点，课文关于李密的祖孙处境、征召两难、表文得体，《项脊轩志》的空间、家变、亲情细节、后记和枇杷树，及任务一至四、任务群8和4-3定位，均可回到绑定的 canonical PDF。
- 高考栏严格保持 `N/A / M0 / N/A`，纵向关系合法保持 N/A；教师用书 `edition_match=unknown`，未消费未登记教师用书、网络解析、外部训诂或未经逐小问核验的真题。

## 3. 阻断性发现与返工项

### P1-A：KP-011 人物动作张冠李戴（R01）

KP-CARD-X3-U03-01-011 写为“老妪转述母亲问寒问饥、**祖母叩门赠象笏**等细节”。canonical 正文物理页78/切页5明确区分：母亲“以指叩门扉”询问“儿寒乎？欲食乎？”，祖母则“过余”、关门后“持一象笏至”，并未叩门或“赠”象笏。该句把两位亲人的动作和对象合并，属于教材关键人物动作的张冠李戴，不能由 EV-009/011 的正确页位抵消。应改为“母亲叩门问寒问饥、祖母持象笏勉励”（或等价的逐字可回查表述），并同步补足/收窄 EV-009 的短引，重新核验 KP-011 及 §2/§8.1 回链。

### P1-B：§8.1 教材学习提示与项目化观察未分层（R04）

§8.1 标题为“教材学习提示”，但第二条“重点语言观察：表文敬辞/自谦语、骈散句和请求语气；志文中的空间词、日常对话、动作细节和物象线索”是将任务二、正文细读和项目分析整理成观察清单；canonical 学习提示直接要求的是表文语言得体/谦敬词语、两文情感结构和细节体会，并未以该清单形式规定这些观察项。应将该条移至 §8.3 并明确为“本项目教学建议”，或改写为只保留 EV-007、011、013 可逐字支持的教材提示。当前分层不清，将研究性操作冒充教材提示，触发 R04。

其余正文、导语、任务、课标、M0、教师用书边界和数量/版本链未发现新的阻断问题。KP-004 中“写给晋武帝”可由物理页75题下注回查；少数复合 Claim 可进一步补连续短引，但不替代上述两项返工。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | **是** | KP-011 将母亲叩门与祖母持象笏误合为“祖母叩门赠象笏”，属于关键人物动作张冠李戴。 |
| R02 | 否 | `20/20` EV 均绑定已登记 Source、canonical Artifact、可解析 locator、短引和 `verified` 状态；除 KP-011 的错误陈述外，未发现直接引文错页或需证主张完全无适配来源。KP-011 的主要问题按 R01 处理，修复时须同步收窄/补强其 exact span。 |
| R03 | 否 | 导语、两篇正文、学习提示、U03任务、课标、20个KP、教学模块、M0和纵向N/A均存在，无合编文本漏项。 |
| R04 | **是** | §8.1 将项目化“重点语言观察”清单置于教材学习提示栏，未明确标为项目建议，造成规范教材提示与研究/教学解释边界混写。 |
| R05 | 否 | 20/20 KP 均具备合法维度、受控知识类型、四层归属、判定理由、有效证据和置信状态。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，未引用未登记真题、答案或评分资料，也未声称 M1—M3 直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并核验的课9教材包、U03任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、20 KP、20 EV、版本、路径和 SHA 一致；validator 哈希校验通过。 |
| R09 | 否 | 使用现行课标任务群8“中华传统文化经典研习”和物理页29—30，未改写任务群名称或把任务群当固定课型/教法。 |
| R10 | 否 | 人文/语言双线按古代散文、文体语言、文化观念和表达活动展开，未机械铺满四项核心素养，也未把学业质量4-3当作单课等级或题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 2 | `P1-KP011-ATTRIBUTION`：将母亲叩门和祖母持象笏张冠为“祖母叩门赠象笏”；`P1-SEC81-MIX`：§8.1 将项目化语言观察清单写入教材学习提示。 |
| P2 | 0 | 本轮未另发现独立的非阻断性缺陷；上述两项已按 P1 计入，不能以 P2 计数重复。 |

## 6. 2.0-textbook 诊断评分

因 R01/R04 与两项 P1 硬门触发，正式验收分记为 `N/A`；以下仅为返工定位诊断分，不能替代放行结论。

| 维度 | 权重 | 门槛 | 诊断得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 23.0 | 20/20 EV 的 Source、canonical Artifact、物理/切页、短引和状态基本闭合；KP-011 错误动作需收窄/补强 exact span，扣2.0。 |
| 事实与术语准确性 | 20 | 18 | 18.0 | 两篇正文、古代散文术语、任务群8和4-3定位总体准确；KP-011 的亲属动作张冠李戴扣2.0。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 导语/两文/提示、20/20 KP、20/20 EV、任务/课标/M0模块齐全。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文与语言双线覆盖伦理处境、亲情记忆、文体得体、空间叙事、骈散/章法/评点和真实表达；两文比较路径较完整。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、任务群8、学业质量4-3定位和 M0 边界均合规。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无双方 accepted 目标时合法使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 5.0 | 任务拆解和评点/书信路径可操作；§8.1来源分层问题扣2.0。 |
| **合计** | **100** | **85** | **93.5** | **诊断分达到数值门槛，但硬门与 P1 缺陷使正式决定为返工。** |

## 7. 返工与主审决定

1. 修正 KP-011 的动作主体和对象：母亲“以指叩门扉”问寒问饥，祖母“持一象笏至”勉励；同步复核 EV-009 短引、KP-011 理由及 §2/§8.1 回链。
2. 将 §8.1 第二条移至 §8.3 并标为本项目教学建议，或收窄为学习提示可直接支持的表文得体、谦敬词语、两文“喜/悲”和平淡语言/细节提示。
3. 内容修改后升版并重算卡片 SHA，更新 ledger transition，重跑 validator；主审与独立第二复审必须绑定同一新版本/SHA，从头复核。旧版分数和本报告不得与新版本拼接放行。

**主审决定：`rework`。** 当前 `CARD-X3-U03-01` v0.2.0/SHA `7a5df02059327d0cdc7d35ddbbb2f789c00c38df7025ef97fc168caaba0050f6` 未通过独立主审，不得转为 `accepted` 或供单元图谱正式消费。本报告不执行任何状态迁移。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U03-01.md`；v0.2.0；SHA `7a5df02059327d0cdc7d35ddbbb2f789c00c38df7025ef97fc168caaba0050f6`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `3d04600b7d09112135b8bd9e0a9ca3638875e33c6342ef506b33a6767e07219c`；CARD-X3-U03-01 为 `linted`/`REBUILD`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-233432+0800.json`；SHA `89bbb8c8794320a471d53708c622045495e8209bea9206a4afaa6cbd60521ec2`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-011-PDF`=`c39d21aa9ebabe1870de3d2f4b5d07676217214ec24d846d7cdf5eec9b3c8b8e`；`ART-PKG-X3-015-PDF`=`e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段值置空后，对 canonical 报告字节求 SHA-256，再回填该值。
