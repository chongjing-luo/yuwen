---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-U04-01-FINAL-R4-PRIMARY"
deliverable_id: "CARD-X2-U04-01"
artifact_version: "0.3.0"
artifact_sha256: "f582983378a104cfda4eeecfb5ca4ebd0e59a33d28bfc32e3ecf4aed381d1281"
review_round: 4
reviewer: "independent_primary_x2_u04_01_final_r4"
review_role: "primary"
reviewed_at: "2026-08-08T19:45:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "82778a8a230aa5e662c6c2bce6ab368448c14eb67c8ccfd6765f965587acb321"
validator_run_id: "VAL-20260808-194012+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-194012+0800.json"
validator_archive_report_sha256: "07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6"
validator_result: "passed"
decision: "pass"
---

# CARD-X2-U04-01 v0.3.0 最终 R4 独立主审

## 1. 绑定与范围

本轮从当前快照重新独立复核 `CARD-X2-U04-01`，不复用旧版本 SHA、分数或结论；不修改卡片正文、账本、验证报告或状态。当前卡为 1 个正文子文本、15 个 KP、23 个 EV。冻结量表为 `2.0-textbook`（总分门槛 85；七维门槛 `21/18/12/12/8/6/5`）。

| 来源 | canonical Artifact / SHA | 覆盖 |
|---|---|---|
| 教材包 | `ART-PKG-X2-015-PDF` / `388cd404624d7ee079316dc15273e383409eb738aee523e8bee70adc681cd0bd` | U04 导语、《玩偶之家》（节选）第三幕，物理页106—121、切分页1—16 |
| U04 任务 | `ART-PKG-X2-017-PDF` / `b3a30d48ce56c2de0f52cfcfc3eb55c938afc080148cc3329302154457735c48` | 单元研习任务，物理页129—130、切分页1—2 |
| 现行课标 | `ART-CURR-2020-PDF` / `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` | 任务群11与学业质量定位 |

账本当前条目 `CARD-X2-U04-01` 的路径、ID、状态 `linted`、版本 `0.3.0` 与卡片 front matter 一致，source_ids 同为 `SRC-PKG-X2-015/017`、`SRC-CURR-2020`；ledger SHA 为本报告页眉绑定值。

## 2. Validator、结构与来源分层

`VAL-20260808-194012+0800` 的最新报告与归档报告均为 `passed`，0 errors，`hash_verification=true`。人工复核确认 15/15 KP、23/23 EV 的 ID 唯一且全部被引用，EV 表为 9 列，Q/F/M/D 类型均为单值，核验状态均为 `verified`。正文、导语、学习提示、单元任务、课标、教师用书缺源声明和项目建议分层清楚；未把外部史料、网络解析、OCR 或项目建议冒充教材事实。

正文物理页107—121（切分页2—16）覆盖第三幕；导语和脚注位于物理页106—107（切分页1—2）；任务与课标分别由已登记的 X2-017 与 CURR-2020 载体承担。新增脚注 EV-023、海尔茂后续反应 EV-020/021 和“奇迹”条件 EV-022 均落在声明页位，补强了复合主张的证据闭包。

## 3. R02/R04/R08 重点 Claim—Evidence 复核

- **R02：否。** 23/23 EV 均解析到已核验 canonical Artifact；关键 Q/F/M 证据的 locator 与短引可回查。KP-004 的借款/伪造签名/借据链由正文危机 EV-004 与脚注 EV-023 分担；KP-005、KP-006、KP-008、KP-013 等解释型主张均有至少两处相互独立的正文节点或正文加学习提示节点。不存在需证主张无适配来源或 I 类解释单证情形。
- **R04：否。** 导语和学习提示只承担教材栏目定位，课标证据只承担官方框架映射，教师用书明确 `edition_match=unknown`，项目建议显式标为本项目建议；没有来源层级冒充。
- **R08：否。** 卡片、账本、SUBTEXT、KP、EV、Source、Artifact 的 ID、路径、版本和数量一致；当前卡 SHA 与本报告绑定 SHA 一致，账本已同步为 v0.3.0，无跨文件断链。

其余硬门：R01（关键事实）、R03（覆盖/模块）、R05（KP字段）、R06（M0）、R07（上游）、R09（课标）、R10（核心素养/学业质量）均未触发。高考栏维持结构化 M0，纵向关系保持有理由的 N/A。

## 4. P0/P1/P2 与决定

`P0/P1/P2 = 0/0/0`。本轮没有开放缺陷，不存在阻断接受或需返工的证据、事实、来源分层或版本问题。

## 5. 七维评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.5 | 23/23 EV 有 canonical locator、Source/Artifact 和 verified 元数据；跨页/多片段证据均可回查，保守扣 0.5。 |
| 事实与术语准确性 | 20 | 18 | 20.0 | 作品、作者、幕次、人物行动、舞台术语、课标任务群11和页位准确。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 1 个正文子文本、15 个文本特异 KP、23 个 EV及任务/课标/边界模块完整。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 婚姻权力、主体确认、社会问题与对话/舞台行动形成双维证据链。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 每个 KP 均有四层归属和理由；高考严格保持 M0。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前无双方已验收目标，合法保持 N/A，不强造关系。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | 冲突链、人物言行表、短评和开放结局任务可执行；项目建议与规范意见分层，保守扣 0.5。 |
| **合计** | **100** | **85** | **98.5** | **总分及七维均达标。** |

**主审决定：`pass`。** 当前 v0.3.0/SHA 可进入独立第二复审；本报告不写回 `accepted`。

## 6. 复现绑定

卡片 SHA `f582983378a104cfda4eeecfb5ca4ebd0e59a33d28bfc32e3ecf4aed381d1281`；ledger SHA `82778a8a230aa5e662c6c2bce6ab368448c14eb67c8ccfd6765f965587acb321`；latest validator SHA `07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6`；archive validator SHA `07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6`；rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
