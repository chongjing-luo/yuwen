---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-U04-01-FINAL-R2-PRIMARY"
deliverable_id: "CARD-X2-U04-01"
artifact_version: "0.2.0"
artifact_sha256: "b0cc8339f1489ef177f623cd41e46992121023bd44b85ee5fe576e594053c6e2"
review_round: 2
reviewer: "independent_primary_x2_u04_01_final_r2"
review_role: "primary"
reviewed_at: "2026-08-08T19:30:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "0b6c8bfb31838978a54278ffae6fae4602e598f166c5ee5f76e42dfae53ca0ff"
validator_run_id: "VAL-20260808-192215+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "bade9ffe1b8608b78c94ce77749258efe340d549e0311db356f1e04ef6fc7b3c"
validator_archive: "work/knowledge/_meta/validation_reports/archive/x2_u04_cards_validation_20260808_r2.json"
validator_archive_sha256: "9ced37e955103b263e68cede11fcd823fbfdae1cbcc7a5e6d67b10a0b0bb06df"
validator_result: "passed"
decision: "pass"
---

# CARD-X2-U04-01 v0.2.0 最终 R2 独立主审

## 1. 绑定与范围

本轮独立复核当前 `CARD-X2-U04-01`，不修改卡片正文、账本、验证报告或状态。卡片包含 1 个正文子文本、15 个 KP、19 个 EV。冻结量表为 `2.0-textbook`（总分门槛 85；七维门槛 `21/18/12/12/8/6/5`）。

| 来源 | Artifact / SHA | 覆盖 |
|---|---|---|
| 教材包 | `ART-PKG-X2-015-PDF` / `388cd404624d7ee079316dc15273e383409eb738aee523e8bee70adc681cd0bd` | U04导语、 《玩偶之家》（节选）第三幕，物理页106—121；切分页1—16 |
| U04任务 | `ART-PKG-X2-017-PDF` / `b3a30d48ce56c2de0f52cfcfc3eb55c938afc080148cc3329302154457735c48` | 单元研习任务，物理页129—130 |
| 现行课标 | `ART-CURR-2020-PDF` / `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` | 任务群11定位及核心素养边界 |

## 2. 结构与证据复核

最新 validator `VAL-20260808-192215+0800` 通过，0 errors，`hash_verification=true`；归档报告同样通过。逐条复核确认 15/15 KP、19/19 EV 的 ID、类型、页位、短引和核验状态一致。正文的信件危机、海尔茂态度突转、娜拉主体确认、舞台物件与关门声均有可回查证据；单元任务、课标任务群11、教师用书 `edition_match=unknown`、高考 M0、纵向 N/A 均保持边界。

KP-004 的陈述包含借款、伪造签名和借据，而 EV-004 短引本身较压缩；其 locator 覆盖物理页111—114，正文及导语背景可回查伪造签名事实。因此仅作证据表达的轻微扣分，不构成 R02 或返工缺陷。

## 3. Claim—Evidence 闭包

- 戏剧类型、第三幕的高潮/结局功能、戏剧性事件和突转：EV-003、EV-014。
- 信件/借据引发危机、海尔茂的名誉自保与借据归还后的“饶恕”突转：EV-004—006。
- 娜拉由惊慌转冷静、婚姻中的玩偶角色、对自己的责任与“首先我是一个人”：EV-007—010。
- 对话语气、停顿、舞台动作及信箱、钥匙、披肩、门等物件的舞台功能：EV-011—012。
- “奇迹中的奇迹”、关门声与开放结尾：EV-013—014。
- 单元矛盾冲突、出走原因、社会意义、结局设想和对读任务：EV-015—016。
- 课标任务群11与能力边界、教师用书缺源声明：EV-017—019。

上述主张均由当前卡片的适配 EV 支撑；没有以外部评论、未登记教师用书或真题替代教材证据。

## 4. R01—R10 与缺陷计数

R01—R10 全部未触发；`P0/P1/P2 = 0/0/0`。未发现事实错误、材料越界、Claim—Evidence 断裂、版本/ID断链、非法高考或纵向升级、课标误引或教师用书冒充教材结论。

## 5. 七维评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | 19/19 EV 均有 canonical locator 和核验状态；KP-004 短引对复合主张压缩，扣 1.0。 |
| 事实与术语准确性 | 20 | 18 | 20.0 | 剧情、人物关系、舞台术语、任务群11及课标版本准确。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 15/15 KP 字段、类型、四层归属、理由与证据完整。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 婚姻权力、主体确认、社会问题与戏剧语言/舞台行动均有文本依据。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由充分；高考关系严格保持结构化 M0。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前无双方已验收目标，合法保持 N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 冲突链、人物言行表、短评和开放结局任务可直接执行，边界清楚。 |
| **合计** | **100** | **85** | **98.5** | **总分及七维均达标。** |

## 6. 主审结论

主审决定：`pass`；总分 `98.5/100`；R01—R10 全否；`P0/P1/P2=0/0/0`。本结论只绑定卡片 v0.2.0/SHA `b0cc8339f1489ef177f623cd41e46992121023bd44b85ee5fe576e594053c6e2`、validator `VAL-20260808-192215+0800`、最新报告与归档 SHA。须由第二复审以同一版本和 SHA 重新核验后再推进状态；本报告不写回 `accepted`。

## 7. 复现绑定

卡片 SHA `b0cc8339f1489ef177f623cd41e46992121023bd44b85ee5fe576e594053c6e2`；ledger SHA `0b6c8bfb31838978a54278ffae6fae4602e598f166c5ee5f76e42dfae53ca0ff`；validator report SHA `bade9ffe1b8608b78c94ce77749258efe340d549e0311db356f1e04ef6fc7b3c`；validator archive SHA `9ced37e955103b263e68cede11fcd823fbfdae1cbcc7a5e6d67b10a0b0bb06df`；rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
