---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X3-U03-R1-PRIMARY-INDEPENDENT"
deliverable_id: "UNIT-X3-U03"
artifact_version: "0.2.0"
artifact_sha256: "c35abc0f7948228d85ef713db950f1573712d2e6207fc21cf1490cbe6aca7fa8"
review_round: 1
reviewer: "independent_primary_unit_x3_u03_r1"
review_role: "primary"
reviewed_at: "2026-08-09T01:12:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "576559a66d61bcd5690eddfa8262ab6ca865694df0d5a402b33820d37e488468"
validator_run_id: "VAL-20260809-010448+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_u03_unit_rebuild_validation_20260809.json"
validator_report_sha256: "fecc270afc6d0d56e08dce237732edbd1c0ea0cddecc0f9262fe01ef7b9cde45"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "e527713050780312dae65bc6ddcb7dcbba58a59a992690a5a0f4c2e2e7058722"
---

# UNIT-X3-U03 v0.2.0 独立主审 R1

## 1. 锁定对象与上游门禁

本轮仅审当前 U03 单元图谱，不复用旧图谱结论，不修改图谱、上游卡、ledger、validator 或状态迁移。冻结量表为 `2.0-textbook` 单元图谱 rubric：总分门槛 88，七维门槛 `22/16/12/12/8/8/4`。

| 对象 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修下册/units/UNIT-X3-U03.md`；v0.2.0；SHA `c35abc0f7948228d85ef713db950f1573712d2e6207fc21cf1490cbe6aca7fa8`；状态 `linted` |
| 上游卡01 | `CARD-X3-U03-01` v0.2.2，ledger `accepted`，post SHA `846119c5135c6c3786bd580f42b19e1a5678792ef88a833558758b889ff80797` |
| 上游卡02 | `CARD-X3-U03-02` v0.2.5，ledger `accepted`，post SHA `a76887a6e7382e45ffc12d5f6466d154b1adaf03b68306bc8a39f3c03f8d28ab` |
| 上游卡03 | `CARD-X3-U03-03` v0.2.1，ledger `accepted`，post SHA `566448adf8fc79cf96cf81d4637a441fe96db4e9d495d60e5eb12d97087cc456` |
| 上游卡04 | `CARD-X3-U03-04` v0.2.1，ledger `accepted`，post SHA `b06a7fc6ba021bd6d77c238a847ddda428c13bc009845b02bdd24bb2661300a5` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `576559a66d61bcd5690eddfa8262ab6ca865694df0d5a402b33820d37e488468`；图谱条目为 v0.2.0/`linted`，路径、source_ids、upstream_card_ids 一致 |
| validator | `VAL-20260809-010448+0800`；报告 `work/knowledge/_meta/validation_reports/x3_u03_unit_rebuild_validation_20260809.json`；SHA `fecc270afc6d0d56e08dce237732edbd1c0ea0cddecc0f9262fe01ef7b9cde45`；`passed`、0 errors、`hash_verification=true` |

四张上游卡均为当前 ledger 的 `accepted` 版本，且图谱 §1 声明的四个 post SHA 与 ledger、实际文件 SHA 完全一致。任务包和课标来源均为已登记、已核验的 canonical 来源；图谱不消费教师用书或未登记真题。

## 2. 结构、覆盖与双维度复核

- 四卡合计 `20+22+18+18=78/78` KP；§1.1 的连续编号索引可展开为每个完整 `KP-CARD-X3-U03-xx-nnn`，无漏项或重复项。六个正文子文本（《陈情表》《项脊轩志》《兰亭集序》《归去来兮辞》《种树郭橐驼传》《石钟山记》）均被覆盖，导语未被误计为正文。
- 人文节点 `4/4`、语言节点 `5/5`、单元任务 `4/4`、跨课/任务关系 `9/9`、Issue `3/3` 均有稳定 ID。每个节点和关系均给出完整 Card/KP-ID 或任务入口及 EV 回链；修订后的 EV/KP 前缀可直接解析。
- 人文线分别覆盖孝亲与亲情记忆、雅集/生命/归隐、顺应天性与治理反思、求真辨伪与实地观察；语言线覆盖身份化表达、空间/序辞/辞的结构、叙事说理与对举类比、游记绘声与评点，以及词类活用/章法/书信等三类语言活动。
- 任务一至四分别闭合文化观念讨论、骈散/章法/评点、词类活用和书信写作；项目评价证据明确标为操作化设计，不冒充教材原文或教师用书意见。

## 3. 综合关系、M0 与边界复核

9 条关系均使用 taxonomy 受控类型（比较、组成、迁移、前提），并写明共性、差异、目标节点和证据理由。`REL-003` 特别保留“顺木之天”与“目见耳闻”的差异，不把两文压成同一方法；`REL-008/009` 将形式分析、词语梳理迁移到书信任务，且说明迁移不改写正文。关系没有以单元顺序或主题相似性替代证据。

单元高考栏保持结构化 `N/A | M0 | N/A`：尚未登记逐小问真题—答案/评分—教材 KP 双向闭合证据，因此不建立 M1—M3 边。前序/后续递进均为有理由的 `N/A`，没有将“古代散文”标签或单元顺序伪装成双方证据。教师用书保持 `edition_match=unknown`，图谱不消费外部意见。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 四张 accepted 卡、六个正文子文本、U03任务和课标任务群定位均与当前 canonical/ledger 绑定一致。 |
| R02 | 否 | `78/78` KP、`4/4`任务、`4+5`双维度节点和 `9/9`关系均有适配的 Card/KP/EV 或任务来源与可回链定位；综合陈述保留边界。 |
| R03 | 否 | 上游清单、完整 KP 索引、任务拆解、双维度节点、关系、M0、前后 N/A、Issue 与自检模块齐全。 |
| R04 | 否 | 教材原文、卡片解释、单元综合、项目评价、教师用书缺失声明和外部真题边界分层清楚，未把综合结论冒充教材明示。 |
| R05 | 否 | `78/78` 上游 KP 均有索引并进入人文/语言节点或任务，关系和任务均有回链；没有孤立 KP。 |
| R06 | 否 | 仅保留合法结构化 M0；未登记真题、答案或评分资料未被消费，未把题型相似性升级为 M1—M3。 |
| R07 | 否 | 四张上游卡全部为 `accepted`，post SHA 与图谱绑定一致；任务包和课标为已核验 canonical 来源。 |
| R08 | 否 | 图谱、ledger、版本、路径、upstream_card_ids、四个 post SHA、78 KP、节点/任务/关系 ID 与数量一致；validator hash verification=true。 |
| R09 | 否 | 使用现行 2020 修订课标的任务群8边界，未改写任务群名称或将其固化为固定课型/教法。 |
| R10 | 否 | 人文/语言线按文本和任务实际展开，未机械铺满四项核心素养，也未给单元贴完整学业质量水平标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无上游伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 无关键覆盖缺失、非法关系类型、M0越级、教师用书混入、版本漂移或上游 SHA 断链。 |
| P2 | 0 | 修订后的 KP/EV 前缀均可直接解析；未发现影响检索和复核的非阻断缺陷。 |

## 6. 单元图谱诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 四张 accepted 卡、六个正文子文本、78/78 KP、4/4任务和节点/关系入口闭合；修订后的完整 KP/EV 前缀可直接解析。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **19.0** | 4个人文节点、5个语言节点和9条关系均给出共性、差异与迁移边界；少量综合语句依赖上游卡摘要，保守扣1.0。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | 双线覆盖六篇正文、U03任务和阅读/表达/梳理活动，节点与 EV 回链完整。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 4/4任务有 canonical 物理页、能力动作、学习成果、评价边界和上游 KP/EV入口。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | M0/N/A 的双向证据缺口与禁止越级边界清楚。 |
| 前后递进 | 10 | 8 | **10.0** | 无双方 accepted 目标时合法使用有理由的前序/后续 N/A，不强造递进。 |
| 可读性与检索性 | 5 | 4 | **5.0** | 上游清单、78项索引、双维度、任务、9条关系、M0、Issue和自检齐全。 |
| **合计** | **100** | **88** | **99.0** | **总分及各维度均达标；R01—R10 全未触发。** |

## 7. 独立主审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `UNIT-X3-U03` v0.2.0/SHA `c35abc0f7948228d85ef713db950f1573712d2e6207fc21cf1490cbe6aca7fa8` 通过独立主审，可进入独立第二复审。本报告只闭合主审，不写回 ledger 或执行 `accepted` 状态迁移；同一图谱、任一上游卡、ledger、validator、rubric/taxonomy 或版本绑定变化时，本报告失效并须按新 SHA 全量复审。

## 8. 可复现绑定与报告校验

- 图谱：`work/knowledge/选择性必修下册/units/UNIT-X3-U03.md`；v0.2.0；SHA `c35abc0f7948228d85ef713db950f1573712d2e6207fc21cf1490cbe6aca7fa8`。
- 上游 accepted 卡 post SHA：CARD-X3-U03-01=`846119c5135c6c3786bd580f42b19e1a5678792ef88a833558758b889ff80797`；CARD-X3-U03-02=`a76887a6e7382e45ffc12d5f6466d154b1adaf03b68306bc8a39f3c03f8d28ab`；CARD-X3-U03-03=`566448adf8fc79cf96cf81d4637a441fe96db4e9d495d60e5eb12d97087cc456`；CARD-X3-U03-04=`b06a7fc6ba021bd6d77c238a847ddda428c13bc009845b02bdd24bb2661300a5`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `576559a66d61bcd5690eddfa8262ab6ca865694df0d5a402b33820d37e488468`。
- validator：`work/knowledge/_meta/validation_reports/x3_u03_unit_rebuild_validation_20260809.json`；run `VAL-20260809-010448+0800`；SHA `fecc270afc6d0d56e08dce237732edbd1c0ea0cddecc0f9262fe01ef7b9cde45`；`passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。
