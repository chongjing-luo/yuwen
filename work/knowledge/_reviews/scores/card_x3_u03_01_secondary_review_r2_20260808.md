---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U03-01-SECONDARY-R2"
deliverable_id: "CARD-X3-U03-01"
artifact_version: "0.2.1"
artifact_sha256: "e17a5c2a81610374797f720064ffa35560fd417e5b845e6a400c9d78c70f6f5a"
review_round: 2
reviewer: "independent_secondary_x3_u03_01_r2"
review_role: "secondary"
reviewed_at: "2026-08-08T23:55:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "56595583ff9ffc507f3d11e0cf747b2a01515d481a11e0cfcd0e95e219811109"
validator_run_id: "VAL-20260808-235756+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u03_01_rework_post_u03_04_validation_20260808.json"
validator_report_sha256: "f8e0bf42fd81f2bc381dd2f6a7f29b564b2ede1cc5d95a6162989cde9e8c2c35"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "9528a9c47c4227252d35f29c14ff25bfedb1de572fbd2212c9cc587bdbe0eca7"
---

# CARD-X3-U03-01 v0.2.1 独立第二复审 R2

## 1. 输入锁定与独立性

本轮基于 v0.2.1 重工快照重新独立复审，重点回归上一轮主审指出的两项 P1：人物动作归属和教材学习提示/项目建议分层；同时核对剩余 P2 的边界。仅消费当前卡片、登记的 canonical Artifact、U03 单元研习任务、现行课标、冻结 `2.0-textbook` rubric/taxonomy、共享 ledger 和指定 validator 报告；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U03-01.md`；v0.2.1；SHA `e17a5c2a81610374797f720064ffa35560fd417e5b845e6a400c9d78c70f6f5a`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `56595583ff9ffc507f3d11e0cf747b2a01515d481a11e0cfcd0e95e219811109`；CARD-X3-U03-01 为 v0.2.1/`linted`，含 `REWORK linted→linted` 记录 |
| 课文 canonical | `ART-PKG-X3-011-PDF`；SHA `c39d21aa9ebabe1870de3d2f4b5d07676217214ec24d846d7cdf5eec9b3c8b8e`；导语物理页74、两篇正文物理页75—78、学习提示物理页79（切分页1—6） |
| U03任务 canonical | `ART-PKG-X3-015-PDF`；SHA `e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；物理页90—91（切分页1—2） |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群8物理页29—30、学业质量4-3物理页46 |
| validator | `VAL-20260808-235756+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `f8e0bf42fd81f2bc381dd2f6a7f29b564b2ede1cc5d95a6162989cde9e8c2c35` |

卡片 front matter 的 `status: linted`、`reviewers: []`、正文评审勾选状态与 ledger 一致。本报告只记录复审，不执行状态迁移。

## 2. 两项 P1 修复回归

### 2.1 KP-011 人物动作归属：已关闭

v0.2.1 将 KP-011 改为“母亲以指叩门问寒问饥，以及祖母持象笏至等细节”，不再把两位亲人的动作合并为“祖母叩门赠象笏”。该表述与课文物理页78/切页5的原文顺序一致：母亲“以指叩门扉”并问“儿寒乎？欲食乎？”，祖母“持一象笏至”。R01/P1-KP011-ATTRIBUTION 已关闭。

但证据表 EV-009 的短引仍只列“儿寒乎？欲食乎？”和“瞻顾遗迹，如在昨日”，没有把“以指叩门扉”“持一象笏至”两个动作逐字写入短引；locator 正确、原文可回查，因此将其作为证据粒度 P2（`P2-EV009-SPAN`），不升级为 R02/P1。

### 2.2 §8.1 教材学习提示/项目建议分层：已关闭

v0.2.1 已将“重点语言观察”清单移入 §8.3“本项目教学建议”，并明确“以上各项为项目建议，不冒充教材要求或教师用书意见”；§8.1只保留可由学习提示逐项支持的两文情感、细节和表达说明。R04/P1-SEC81-MIX 已关闭。

## 3. 覆盖、来源和回链复核

- `2/2` 子文本、`20/20` KP、`20/20` EV 均有稳定 ID、主维度、受控知识类型、四层主归属、判定理由和证据回链；EV 类型均为单值 `Q/F/M/D`。
- canonical 页位保持正确：导语物理页74；《陈情表》75—77；《项脊轩志》77—78；学习提示79；任务90—91；课标任务群8物理页29—30、学业质量4-3物理页46。
- 任务、课标和教材边界分层；教师用书未登记，`edition_match=unknown`；MinerU 只作辅助定位，正式证据回到 canonical PDF。
- 高考栏为 `N/A / M0 / N/A`，纵向关系为有理由的 `N/A`，没有未核验真题、答案/评分资料或跨课映射。

## 4. 剩余 P2 边界

1. `P2-EV009-SPAN`：KP-011已改正事实，但 EV-009 短引没有覆盖其两个动作子主张；补齐 exact span 可提高可追溯性。
2. `P2-EV019-SPAN`：KP-019写出课标任务群8的“内容提要、阅读感受和作品评论”，EV-019短引只列“精读”“梳理文言项目”和“撰写评论”；locator正确、canonical物理页29—30含完整原文，属短引粒度不足。
3. `P2-KP015/017-BOUNDARY`：KP-015的“交流修订”比任务二明示的“评点并与同学交流”多一步修订；KP-017的“回应可能的差异或限制”是合理项目化展开，而任务一直接要求的是讨论传统文化观念的当代价值。两者不构成教材事实错误，但后续可分别收窄为“交流”和“讨论当代价值”，或明确标为项目建议。合并计一项 P2。

## 5. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | v0.2.1已纠正KP-011的母亲/祖母动作归属；其余题名、作者、正文事实和课标术语均可回到canonical来源。 |
| R02 | 否 | 20/20 EV均有Source、Artifact、locator、短引和验证状态；EV-009/019为正确locator下的短引粒度P2，不是无适配来源或不可定位引文。 |
| R03 | 否 | 2个子文本、导语/学习提示、任务、课标、20 KP、20 EV、教学提示、M0和纵向N/A模块齐全。 |
| R04 | 否 | v0.2.1已把项目化语言观察移出§8.1，正文、学习提示、任务、课标、教师用书缺源和项目建议边界清楚。 |
| R05 | 否 | 20/20 KP均具备合法主维度、受控知识类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，未引用未登记真题、答案或评分资料，也未声称M1—M3直接衔接。 |
| R07 | 否 | 正式内容仅消费已登记并核验的课文包、U03任务包和现行课标Artifact；教师用书缺失已透明声明。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、20 KP、20 EV、版本、路径和SHA绑定一致；v0.2.1/REWORK记录与当前文件一致。 |
| R09 | 否 | 使用现行课标任务群8及学业质量4-3定位，未改写任务群名称或把质量描述当课型/难度标签。 |
| R10 | 否 | 人文/语言双线按文本需要展开，未机械铺满核心素养，也未把学业质量4-3判为单课完整等级。 |

## 6. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 上一轮人物动作张冠李戴和教材提示/项目建议混写均已修复；当前无关键事实、证据断链、版本漂移或边界硬错。 |
| P2 | 3 | `P2-EV009-SPAN`、`P2-EV019-SPAN` 及合并计数的 `P2-KP015/017-BOUNDARY`。均不阻断放行。 |

## 7. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **23.5** | 20/20 EV的来源、Artifact、物理/切页、短引和状态闭合；EV-009、EV-019短引粒度各扣0.75。 |
| 事实与术语准确性 | 20 | 18 | **20.0** | v0.2.1已关闭KP-011关键动作错误；两篇课文、任务群8和4-3术语及页位准确。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 2/2子文本、20/20 KP、20/20 EV及任务/课标/M0/纵向模块齐全。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线覆盖孝道、亲情、记忆和传统观念；语言线覆盖表文得体、情理结构、空间叙事、骈散/章法/评点。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 四层主归属、理由、现行课标对接及M0/N/A边界完整。 |
| 纵向贯通 | 8 | 6 | **8.0** | 当前无双方可核验的纵向KP关系，合法使用有理由的N/A。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 三类提示已分离，结构线、评点、文化讨论和书信任务可直接用于备课。 |
| **合计** | **100** | **85** | **98.0** | **总分及单项达到冻结门槛；R01—R10全部未触发。** |

## 8. 独立第二复审决定

**决定：`pass`；总分 `98.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/3`。**

当前 `CARD-X3-U03-01` v0.2.1/SHA `e17a5c2a81610374797f720064ffa35560fd417e5b845e6a400c9d78c70f6f5a` 通过本轮独立第二复审，可与同一 SHA 的独立主审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、canonical Artifact、validator、ledger 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 9. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U03-01.md`；v0.2.1；SHA `e17a5c2a81610374797f720064ffa35560fd417e5b845e6a400c9d78c70f6f5a`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `56595583ff9ffc507f3d11e0cf747b2a01515d481a11e0cfcd0e95e219811109`。
- validator：`work/knowledge/_meta/validation_reports/x3_u03_01_rework_post_u03_04_validation_20260808.json`；run `VAL-20260808-235756+0800`；SHA `f8e0bf42fd81f2bc381dd2f6a7f29b564b2ede1cc5d95a6162989cde9e8c2c35`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：课文包 `ART-PKG-X3-011-PDF`=`c39d21aa9ebabe1870de3d2f4b5d07676217214ec24d846d7cdf5eec9b3c8b8e`；U03任务 `ART-PKG-X3-015-PDF`=`e7f405d2972c3134bc6f8f81bd1dfcb512947ec60efac14150e0e7f7da605001`；现行课标 `ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填该值。
