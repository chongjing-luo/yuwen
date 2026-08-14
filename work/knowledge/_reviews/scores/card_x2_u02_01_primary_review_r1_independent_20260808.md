---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-U02-01-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X2-U02-01"
artifact_version: "0.2.0"
artifact_sha256: "2e9f93933f093806fc562c3e0dec12710030809f1f2a3cc5bff28440b06d16cf"
review_round: 1
reviewer: "independent_primary_x2_u02_01_r1"
review_role: "primary"
reviewed_at: "2026-08-08T17:42:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-173748+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/x2_u02_cards_validation_20260808_rework3.json"
validator_report_sha256: "c17a24952c5166d88d93a0488e4061e6ce6116236d68a99c467c6b1309a967fe"
validator_result: "passed"
decision: "pass"
---

# CARD-X2-U02-01 v0.2.0 独立主审 R1

## 1. 锁定对象与独立性

- 本轮只审查当前 `work/knowledge/选择性必修中册/cards/CARD-X2-U02-01.md` v0.2.0，当前 SHA-256 为 `2e9f93933f093806fc562c3e0dec12710030809f1f2a3cc5bff28440b06d16cf`；不复用旧版本的正文判断、分数或结论。
- 采用冻结 `2.0-textbook` 知识卡量表：总分门槛 85，七维门槛依次为 21/18/12/12/8/6/5。Rubric、taxonomy、validator 绑定在页眉。
- `VAL-20260808-173748+0800` 为 `passed`，六类检查均 0 errors，hash verification=true；当前 ledger 条目为 `linted / v0.2.0 / root`。本报告不修改正文、`deliverables.jsonl` 或验证归档。

## 2. 来源、Artifact 与材料边界

| 项目 | 本轮核验结果 |
|---|---|
| canonical 教材包 | `ART-PKG-X2-007-PDF`，SHA `88f8f162f5cf46e9c5d4474d208fafe6de16c0d290624623a3063ba4cf637616`；规范物理页 42—56，切分页 1—15。 |
| 共用单元任务 | `ART-PKG-X2-010-PDF`，SHA `3d90ed6a9b2af696231f54c44a6ba991a42cccc02125bd6c3fdbd425830fe1ab`；物理页 85，切分页 1。 |
| 现行课标 | `ART-CURR-2020-PDF`，SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群10物理页 31—32/印刷页 23—24，核心素养物理页 12—13/印刷页 4—5。 |
| 覆盖范围 | 单元导语、鲁迅两篇规范正文、学习提示、U02 单元研习任务和课标；两个正文子文本分别登记，栏目边界未混入正文。 |

## 3. 结构、证据与 Claim—Evidence 复核

- 当前卡覆盖 2 个正文子文本、16 个 KP 和 19 个 EV（17 条 Q、2 条 M）。每个 KP 均有主维度、冻结知识类型、四层主归属、判定理由、EV-ID 与置信状态。
- 19/19 EV 均绑定已登记 Source、canonical Artifact、规范物理页/切分页、短引文及 `verified` 核验元数据；教材正文、学习提示、单元任务和课标来源分层。
- U02 革命文化语境、两文的纪念性散文体裁、人物事实、写作动机、语言反讽/对比、情感推进、人物比较和阅读迁移均能回链到相应 EV。复合 KP 的部分短引为压缩式摘引，但 locator 覆盖相邻正文范围，未见无证扩展。
- 学习提示与任务产出（批注本、札记、人物分析、红色作品集）被明确写成学习/项目层，不冒充教材正文；课标只用于任务定位，不据此判定完整学业质量水平。
- 高考栏严格为结构化 `M0`，纵向栏为有理由的 `N/A`；教师用书 `edition_match=unknown` 是已声明的来源边界。

## 4. R01—R10 硬性检查

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、鲁迅作者、两文体裁、人物/事件、革命文化语境和语言判断均可回到规范页 42—56。 |
| R02 | 否 | 19 条 EV 均有适配 Source、canonical Artifact、物理/切页和可解析短引；复合解释未出现完全无证主张。 |
| R03 | 否 | 导语、2 个正文子文本、学习提示、任务、课标、纵向、高考和三类教学提示模块齐全。 |
| R04 | 否 | 正文、学习提示、课标、任务和项目建议分层；未将网络解析、OCR 派生物或缺源教参冒充规范结论。 |
| R05 | 否 | 16/16 KP 均有主层级、映射理由、有效 EV 和置信状态，粒度可教且保持文本特异性。 |
| R06 | 否 | 未登记真题；高考关系仅为 M0，未将题型相似性称为直接衔接。 |
| R07 | 否 | 仅消费已核验教材包、任务包和现行课标，没有未验收上游依赖。 |
| R08 | 否 | 卡内 subtext/KP/EV ID、数量、版本、来源路径和当前 SHA 一致；ledger 也为当前 linted 版本。 |
| R09 | 否 | 使用现行任务群“中国现当代作家作品研习”等受控术语，未把任务群改写成固定课型。 |
| R10 | 否 | 核心素养只作相关表现定位，学业质量保持 N/A，未机械铺满四项或贴水平标签。 |

结论：`R01—R10 全部为否`。

## 5. 知识卡量表评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.5 | 19/19 EV 的来源、页码、切页、短引和状态闭合；少数复合主张采用跨段 locator，短引未逐字展开全部要件，保守扣 0.5。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 题名、作者、纪念性散文、革命文化和任务群术语准确；“对偶/反复”等语言判断有正文句群支撑，保守留 0.5 的术语解释余量。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2 个正文子文本、16 KP、19 EV、任务、课标、M0/N/A 与三类教学边界齐全，KP 可检索、可教学。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文维度覆盖纪念、正义、记忆、压迫与人物责任；语言维度覆盖叙事、抒情、反讽、比较和三类读写活动，综合母题仍以文本内证据为主，保守扣 0.5。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 每个 KP 有主层级和理由，课标 M 证据可定位，高考 M0 及其解锁条件透明。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前尚无双方 accepted 的跨卡证据，保持结构化 N/A，未强造递进关系。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 教材学习提示、教师用书缺源和项目建议分离；证据表、比较维度及作品产出可直接用于备课。 |
| **合计** | **100** | **85** | **98.5** | 总分及七维最低分均达标。 |

## 6. P0/P1/P2 与决定

| 等级 | 数量 | 说明 |
|---|---:|---|
| P0 | 0 | 无来源造假、关键事实错误、错页或不可恢复证据断裂。 |
| P1 | 0 | 16/16 KP、19/19 EV、双维、任务、M0 与 N/A 均闭合。 |
| P2 | 0 | 仅有少量复合引文的可读性优化空间，不影响当前验收。 |

**主审决定：`pass`。** 当前 v0.2.0/SHA 可进入独立第二复审；后续正文、证据或上游 Artifact 变更时须以新 SHA 重审。

## 7. 可复现信息

- 卡片：`work/knowledge/选择性必修中册/cards/CARD-X2-U02-01.md`，v0.2.0，SHA `2e9f93933f093806fc562c3e0dec12710030809f1f2a3cc5bff28440b06d16cf`。
- Validator：`VAL-20260808-173748+0800`，`passed`，0 errors；报告 `work/knowledge/_meta/validation_reports/archive/x2_u02_cards_validation_20260808_rework3.json`，SHA `c17a24952c5166d88d93a0488e4061e6ce6116236d68a99c467c6b1309a967fe`。
- Rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 分母：2 个正文子文本、16 KP、19 EV（17 Q/2 M）；高考 1 行 M0；纵向 1 行有理由 N/A。
