---
schema_version: "2.0-candidate"
review_id: "REV-BOOK-X1-R1-SECONDARY-INDEPENDENT"
deliverable_id: "BOOK-X1"
artifact_version: "0.2.0"
artifact_sha256: "82c60292b2c459668da944739b80ba50af4e8a63059dd31f70598091d0627747"
review_round: 1
reviewer: "independent_secondary_book_x1_r1"
review_role: "secondary"
reviewed_at: "2026-08-08T17:20:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-171132+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-171132+0800.json"
validator_report_sha256: "c93df8c294be11c7dc2e10d5482e67daca87e7d74bf8b611d3b1d179776b155f"
validator_result: "passed"
decision: "pass"
---

# BOOK-X1 v0.2.0 独立第二复审 R1

## 1. 独立锁定与复核范围

本轮独立读取当前册级总表、五个 accepted 上游交付物、13 张 accepted 卡、前言/主教材与课标 Artifact、冻结 rubric/taxonomy 和指定 validator 归档；不以其他评审结论替代当前证据，不修改 BOOK-X1、账本或状态迁移。

- 册表：`work/knowledge/册级汇总/BOOK-X1.md`，v0.2.0，SHA `82c60292b2c459668da944739b80ba50af4e8a63059dd31f70598091d0627747`。
- 上游图谱/卡片已按表中版本与 SHA 逐一复算：`UNIT-X1-U01` 0.2.0/`72e11879…`，`UNIT-X1-U02` 0.2.1/`56a06f60…`，`UNIT-X1-U03` 0.2.2/`d3eb0f7a…`，`UNIT-X1-U04` 0.2.1/`00e0eea0…`，`CARD-X1-REC-01` 0.2.1/`fca312dba…`。
- validator：`VAL-20260808-171132+0800`，archive 报告 SHA `c93df8c294be11c7dc2e10d5482e67daca87e7d74bf8b611d3b1d179776b155f`，passed，0 errors，hash verification=true。

## 2. 覆盖、版本和 ID 独立复算

- 单元图谱 4/4 accepted、诵读卡 1/1 accepted、底层卡 13/13 accepted；21/21 正文子文本和 160/160 KP 的计数由四图谱/诵读卡覆盖数（48+37+50+13+12）复算一致。
- 前言/主教材 `ART-MASTER-X1-PDF` SHA `59f554868f974b0c31686a2978c785f5de6dab40dfb1d7a5496775cb6fdbd456`、前言包 `ART-PKG-X1-000-PDF` SHA `aaa80a3f811e2571278c4f30a4f2b2e8d14a3d973189da4f60a4493e36b44ef0` 与课标 `ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` 均为 canonical/verified 注册 Artifact。
- 册表中的 CAND/REL/TASK/KP/EV 引用做了只读解析：未发现悬空 ID；人文节点 24 项、语言节点 29 项、单元内部关系 33 条的上游入口可回链，册级 6 条关系端点和证据也可定位。

## 3. 课程、人文/语言主线和边界核验

- U01 的革命传统与民族复兴主线同时保留人民主体、责任、生命、人道、科学和反思；U02 区分儒/道/墨的概念路径；U03 区分成长、罪责、失败、现代化与不同小说语境；U04 将逻辑判断与公共表达责任连接；REC 保留四篇诗词的共同赴战、月下相思、失意狂放和悼亡差异。综合陈述均标为册级解释，不冒充教材唯一答案。
- 语言主线“定位材料—识别形式/结构—复原解释链—表达与修订”能回到各图谱的任务和节点：U01新闻/通讯材料治理，U02经典说理/虚词，U03叙事细节/环境，U04论证/谬误，REC诵读/意象与时空。
- 前言、目录、后记仅承担册级范围；课标只作定位；教师用书 `edition_match=unknown` 且引用率0/0；高考不消费试卷，统一结构化 M0。边界分层没有把项目建议或网络资料升级为教材事实。

## 4. 跨单元关系与缺口

`REL-BOOK-X1-001—006` 的端点均回链 accepted 上游节点或 KP，并使用 taxonomy 受控的 `迁移`、`深化`、`比较`：材料核验→经典写作、先秦说理→逻辑论证、历史材料链→小说细节链、小说细节→诗词形式、逻辑质疑→革命传统研讨、成长尊严→革命人物品质。每条关系均写出语境差异，未把主题相似性变成高考映射。

当前册级关系没有单独登记 `前提` 类型的确定性边，而是用迁移/深化说明能力链；在无跨册双方 accepted 目标时保持 `N/A (no_reliable_relation)`。这不是阻断缺陷，但在“前置”检查点保留审慎扣分。

## 5. R01—R10 与缺陷等级

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 五个内容入口、版本/SHA、前言边界和课标版本与 canonical/账本一致。 |
| R02 | 否 | 覆盖计数、上游哈希、CAND/REL/KP/EV/TASK 引用均可回链；未发现不可定位的正式主张。 |
| R03 | 否 | 四单元、REC、前言、双线、关系、M0、教师用书、索引和问题清单完整。 |
| R04 | 否 | 教材范围、课标定位、上游解释、项目建议、教师书缺源和真题未处理边界严格分层。 |
| R05 | 否 | 册表不新增卡外 KP；160/160 上游 KP 只通过 accepted 图谱/卡纳入。 |
| R06 | 否 | 高考板块全为合法 M0，不消费真题、不做题型相似越级。 |
| R07 | 否 | 五个上游交付物均 accepted，版本与当前文件 SHA 一致。 |
| R08 | 否 | 前言/Artifact/上游路径、CAND/REL/TASK/EV/KP 引用和覆盖分母闭合。 |
| R09 | 否 | 使用现行课标与各单元规范任务群，不把册级主题改成固定课型。 |
| R10 | 否 | 人文/语言综合均连到具体文本、形式和任务动作，未机械铺满素养或学业质量等级。 |

P0/P1/P2：**0/0/0**。开放项均是教师用书缺源、真题阶段门禁或册级自身待双审，已有显式处置，不构成当前内容缺陷。

## 6. 册级量表评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25 | 23 | **25.0** | 4/4图谱、1/1诵读、前言边界和仅 accepted 上游均闭合；13卡/21子文本/160 KP 计数可复算。 |
| 跨单元递进 | 20 | 17 | **18.5** | 6条迁移/深化/比较关系有端点和证据，N/A 边界合法；无单独 `前提` 边，保留1.5审慎余量。 |
| 分类、去重与稳定ID | 15 | 13 | **15.0** | 任务群与索引分层、无重漏、REL-ID/上游 ID 稳定且可解析。 |
| 双线、任务群与课程定位 | 15 | 13 | **15.0** | 五入口的人文和语言线均有 accepted 图谱/卡及任务支撑；课标定位不过度扩张。 |
| 高考板块映射 | 10 | 8 | **10.0** | 四板块均覆盖且明确 M0、N/A 和 G-TB 解锁条件。 |
| 上下游一致性 | 10 | 9 | **10.0** | 五个上游版本/SHA、源 Artifact、当前路径和账本状态一致。 |
| 检索性 | 5 | 4 | **4.5** | 索引词、问题清单、表格和版本记录齐全；跨单元关系证据密度高，保留0.5余量。 |
| **合计** | **100** | **90** | **98.0** | 七维均过门槛。 |

## 7. 独立第二复审决定

**决定：`pass`。** 当前 BOOK-X1 v0.2.0/SHA `82c60292b2c459668da944739b80ba50af4e8a63059dd31f70598091d0627747` 可进入同 SHA G4 配对；总分与任一主审分差须按 rubric 核对，正文或上游变化后本报告失效。当前不得仅凭本报告标记 `accepted`。

## 8. 可复现信息

- 册表：`work/knowledge/册级汇总/BOOK-X1.md`；v0.2.0；SHA `82c60292b2c459668da944739b80ba50af4e8a63059dd31f70598091d0627747`。
- validator：`VAL-20260808-171132+0800`；archive SHA `c93df8c294be11c7dc2e10d5482e67daca87e7d74bf8b611d3b1d179776b155f`；passed/0 errors。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 分母：4 图谱、1 诵读卡、13 底层卡、21 子文本、160 KP、24 人文项、29 语言项、33 单元关系、6 册级关系；高考 4 板块均为 M0。
