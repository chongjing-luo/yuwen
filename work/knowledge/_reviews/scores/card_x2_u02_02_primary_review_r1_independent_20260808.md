---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-U02-02-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X2-U02-02"
artifact_version: "0.2.0"
artifact_sha256: "9771a916f3a4eb625b889c22ad2dbd97a6afc59fdc580740504380b4f71d7185"
review_round: 1
reviewer: "independent_primary_x2_u02_02_r1"
review_role: "primary"
reviewed_at: "2026-08-08T17:43:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-173748+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/x2_u02_cards_validation_20260808_rework3.json"
validator_report_sha256: "c17a24952c5166d88d93a0488e4061e6ce6116236d68a99c467c6b1309a967fe"
validator_result: "passed"
decision: "pass"
---

# CARD-X2-U02-02 v0.2.0 独立主审 R1

## 1. 锁定对象与独立性

- 本轮只审查当前 `work/knowledge/选择性必修中册/cards/CARD-X2-U02-02.md` v0.2.0，当前 SHA-256 为 `9771a916f3a4eb625b889c22ad2dbd97a6afc59fdc580740504380b4f71d7185`；不复用旧版本判断或分数。
- 采用冻结 `2.0-textbook` 知识卡量表：总分门槛 85，七维门槛为 21/18/12/12/8/6/5。Rubric、taxonomy、validator 绑定在页眉。
- `VAL-20260808-173748+0800` 为 `passed`，六类检查均 0 errors，hash verification=true；ledger 条目为 `linted / v0.2.0 / root`。本报告不修改卡片、账本或验证归档。

## 2. 来源、Artifact 与材料边界

| 项目 | 本轮核验结果 |
|---|---|
| canonical 教材包 | `ART-PKG-X2-008-PDF`，SHA `24081913e2ee0fa8e2d1b899b0a9476bcbfc9afa708088293893c413ac6cb316`；规范物理页 57—65，切分页 1—9。 |
| 共用单元任务 | `ART-PKG-X2-010-PDF`，SHA `3d90ed6a9b2af696231f54c44a6ba991a42cccc02125bd6c3fdbd425830fe1ab`；物理页 85，切分页 1。 |
| 现行课标 | `ART-CURR-2020-PDF`，SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群10物理页 31—32/印刷页 23—24。 |
| 覆盖范围 | 夏衍《包身工》一篇规范正文、学习提示、U02 单元任务及课标；未虚构额外正文子文本，也未把外部史料或教师用书当作教材证据。 |

## 3. 结构、证据与 Claim—Evidence 复核

- 当前卡覆盖 1 个正文子文本、14 个 KP 和 16 个 EV。EV 由教材事实/解释、学习提示、任务和课标证据组成，均登记 Source、Artifact、locator、短引和核验元数据。
- 课文的报告文学文体、凌晨现场、包身契与带工老板、机器反讽、暴力和封闭管理、工资/工时机制、墨鸭类比及结尾“黑暗—黎明”链条均有正文定位。解释型 KP 没有把外部社会史结论写成课文事实。
- “新闻性与文学性”既通过全文结构证据，又由学习提示和单元札记任务分层支撑；EV-010 使用全篇结构范围，定位可解析但不是最小页范围，作为可读性扣分点。
- 高考栏为结构化 `M0`，纵向栏为有理由的 `N/A`；教师用书 `edition_match=unknown` 明确保留缺源边界，项目札记步骤没有冒充教材要求。

## 4. R01—R10 硬性检查

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、夏衍作者、报告文学定位、包身工制度事实和结尾判断与规范页 57—65 一致。 |
| R02 | 否 | 16 条 EV 均有适配来源、canonical Artifact、物理/切页和可解析引文；制度链和文学性解释均有正文或学习提示证据。 |
| R03 | 否 | 1 个正文子文本、学习提示、单元任务、课标、纵向、高考和三类教学提示模块完整。 |
| R04 | 否 | 正文、学习提示、课标、任务及项目建议边界清楚；未以 OCR、网络解析、外部史料或缺源教参替代规范来源。 |
| R05 | 否 | 14/14 KP 均具主层级、映射理由、有效证据和置信状态，且保留报告文学的文本特异性。 |
| R06 | 否 | 未登记真题；高考部分严格为 M0，未把一般题型相似性升级为 M1。 |
| R07 | 否 | 仅消费已核验教材包、任务包和现行课标。 |
| R08 | 否 | 卡内 KP/EV ID、数量、版本、来源链接和当前 SHA 一致；ledger 为同版本 linted。 |
| R09 | 否 | 使用现行任务群“中国现当代作家作品研习”，未改写任务群名称或当作固定教法。 |
| R10 | 否 | 核心素养仅作相关表现定位，学业质量保持 N/A，未机械铺满四项。 |

结论：`R01—R10 全部为否`。

## 5. 知识卡量表评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | 16/16 EV 的来源、Artifact、页码、短引和状态完整；EV-010 以全篇结构范围支撑新闻性/文学性，非最小定位，扣 1.0。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 报告文学、制度事实、人物案例、经济机制和课标术语准确；少量复合制度判断仍需依 locator 阅读完整段落，保守扣 0.5。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 10 个模块、1 个正文子文本、14 KP、16 EV、任务、课标、M0/N/A 与教学边界齐全。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文线闭合“制度控制—非人化—人道/历史希望”，语言线覆盖现场、细节、类比、新闻性/文学性和读写活动；综合判断均留在文本证据内。 |
| 四层与高考映射 | 10 | 8 | 10.0 | KP 的层级、理由和课标 M 证据完整；高考 M0 及其解锁条件清楚。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前无双方 accepted 目标证据，合法保持 N/A，未凭主题词强造递进。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | 教材提示、教师用书缺源和项目札记建议三层分离；任务动作可执行，但 EV-010 全篇 locator 使检索略宽。 |
| **合计** | **100** | **85** | **97.5** | 总分及七维最低分均达标。 |

## 6. P0/P1/P2 与决定

| 等级 | 数量 | 说明 |
|---|---:|---|
| P0 | 0 | 无关键事实错误、伪造来源、错页或不可恢复断链。 |
| P1 | 0 | 14/14 KP、16/16 EV、双维、任务和 M0/N/A 均闭合。 |
| P2 | 0 | EV-010 可选优化为更窄的学习提示页定位，但不影响当前验收。 |

**主审决定：`pass`。** 当前 v0.2.0/SHA 可进入独立第二复审；正文、证据或上游 Artifact 发生变更时须重新计算 SHA 并重审。

## 7. 可复现信息

- 卡片：`work/knowledge/选择性必修中册/cards/CARD-X2-U02-02.md`，v0.2.0，SHA `9771a916f3a4eb625b889c22ad2dbd97a6afc59fdc580740504380b4f71d7185`。
- Validator：`VAL-20260808-173748+0800`，`passed`，0 errors；报告 `work/knowledge/_meta/validation_reports/archive/x2_u02_cards_validation_20260808_rework3.json`，SHA `c17a24952c5166d88d93a0488e4061e6ce6116236d68a99c467c6b1309a967fe`。
- Rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 分母：1 个正文子文本、14 KP、16 EV（14 Q/1 R/1 M）；高考 1 行 M0；纵向 1 行有理由 N/A。
