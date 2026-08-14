---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-U03-02-FINAL-PRIMARY"
deliverable_id: "CARD-X2-U03-02"
artifact_version: "0.2.1"
artifact_sha256: "a364ed80346f02bf76edf49afb8c9452eb6b0ff3b9805a6b789116c43bbb9fed"
review_round: 1
reviewer: "independent_primary_x2_u03_02_final"
review_role: "primary"
reviewed_at: "2026-08-08T18:44:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-183514+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "c797f9056d1a65cabc8bc6b268cb37546d724b820e768da4d52e7db871f6aee8"
validator_result: "passed"
decision: "rework"
---

# CARD-X2-U03-02 v0.2.1 最终独立主审

## 1. 审查范围与绑定

本轮只审当前 `work/knowledge/选择性必修中册/cards/CARD-X2-U03-02.md`，不修改正文、账本或 validator 归档。冻结量表为 `2.0-textbook`（总分门槛85；七维门槛21/18/12/12/8/6/5）。

| 来源 | canonical Artifact / SHA | 覆盖 |
|---|---|---|
| 教材包 | `ART-PKG-X2-012-PDF` / `97121b4473d6515eaacdf1e7576b02ed21b7482cc1c0977e3763bae30a3f6885` | 《苏武传》页92—96；学习提示页97 |
| U03任务 | `ART-PKG-X2-014-PDF` / `0479f6c8ba0eec387251220f76e97014c14d27787e992e557eef30eadffb82cb` | 页104—105 |
| 现行课标 | `ART-CURR-2020-PDF` / `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` | 任务群8与学业质量定位 |

## 2. 结构与 Claim—Evidence 复核

最新 validator `VAL-20260808-183514+0800` 为 passed，0 errors、hash verification=true。本卡为1个正文子文本、15 KP、18 EV；Q/F/M/D 为单值类型，并含课标、任务、教学提示、纵向 N/A、高考 M0 和教师用书 `unknown` 边界。

发现一处仍未闭合的硬性证据链：`KP-CARD-X2-U03-02-005` 声称“卫律以受辞、刑讯和降汉条件逼迫苏武；苏武以‘屈节辱命，虽生，何面目以归汉’拒绝”。当前证据列仅为 `EV-CARD-X2-U03-02-004`，其短引支撑受辞/刑讯场景中的自刺与拒绝降节，但没有支撑主张后半段的阶段性转折“律知武终不可胁，白单于。单于愈益欲降之”；该明确证据在 `EV-CARD-X2-U03-02-005`。应至少将 EV-005 补列至 KP-005，或拆为连续的两个原子 KP。

其余苏武出使、虞常谋反、北海生存、李陵劝降、史传叙事艺术、任务和课标定位均有 canonical locator，未发现来源伪造、正文越界或版本/数量断链。

## 3. R01—R10

| 代码 | 触发？ | 结论 |
|---|---|---|
| R01 | 否 | 题名、作者、苏武经历和史传艺术与页92—97一致。 |
| R02 | **是** | KP-005 的复合主张缺少 EV-005 的显式绑定。 |
| R03 | 否 | 正文、学习提示、任务、课标、纵向、高考和教学提示模块齐全。 |
| R04 | 否 | 学生正文、栏目、任务、课标和项目建议分层清楚。 |
| R05 | **是** | KP-005 后半段主张在当前证据列中没有直接有效证据 ID。 |
| R06 | 否 | 高考维持 M0，无未登记真题调用。 |
| R07 | 否 | 仅消费已登记教材、任务包和课标。 |
| R08 | 否 | ID、版本、数量和路径结构一致；问题是语义绑定缺口。 |
| R09 | 否 | 任务群名称与现行课标一致。 |
| R10 | 否 | 未机械铺满核心素养，学业质量仅作定位。 |

## 4. 评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 22.5 | 18/18 EV 有 locator，但 KP-005 复合主张缺 EV-005 显式绑定。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 苏武史实、文言语言、史传术语和课标定位准确，复合证据覆盖不足扣0.5。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 1正文子文本、15 KP、18 EV和任务/课标模块完整。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 使命、威逼利诱、行动细节、人物对照和寓评于叙完整。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由齐全，高考边界为 M0。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前无双方 accepted 目标，合法保持 N/A。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | 年表和“压力—回应—后果”证据表可操作，但 KP-005 修复前不宜正式定稿。 |
| **合计** | **100** | **85** | **96.0** | R02/R05 触发，当前不得按 pass 接受。 |

## 5. P0/P1/P2 与决定

| 等级 | 数量 | 说明 |
|---|---:|---|
| P0 | 0 | 无来源伪造、重大事实错误或不可恢复损坏。 |
| P1 | 1 | KP-005 至少补列 EV-005；如保留复合陈述，须同时保留 EV-004。 |
| P2 | 0 | 该缺口已达到 R02/R05，不降级为一般优化。 |

**主审决定：`rework`。** 请补齐 KP-005 的 EV-005 绑定或拆分主张，重算卡片 SHA 后再复审；当前 v0.2.1/SHA 不得转为 `accepted`。

## 6. 可复现信息

- 卡片：`work/knowledge/选择性必修中册/cards/CARD-X2-U03-02.md`；v0.2.1；SHA `a364ed80346f02bf76edf49afb8c9452eb6b0ff3b9805a6b789116c43bbb9fed`。
- Validator：`VAL-20260808-183514+0800`；报告 `work/knowledge/_meta/validation_reports/latest.json`；SHA `c797f9056d1a65cabc8bc6b268cb37546d724b820e768da4d52e7db871f6aee8`。
- Rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
