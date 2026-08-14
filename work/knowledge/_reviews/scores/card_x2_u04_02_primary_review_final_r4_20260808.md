---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-U04-02-FINAL-R4-PRIMARY"
deliverable_id: "CARD-X2-U04-02"
artifact_version: "0.3.0"
artifact_sha256: "5680a0b3b9080be9d2ea0ac573ecb331d2ee7a05baf7f6f72a77a34fb4cf31b7"
review_round: 4
reviewer: "independent_primary_x2_u04_02_final_r4"
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

# CARD-X2-U04-02 v0.3.0 最终 R4 独立主审

## 1. 绑定与范围

本轮从当前快照重新独立复核 `CARD-X2-U04-02`，不复用旧版本 SHA、分数或结论；不修改卡片正文、账本、验证报告或状态。当前卡为 4 个正文子文本、16 个 KP、23 个 EV。冻结量表为 `2.0-textbook`（总分门槛 85；七维门槛 `21/18/12/12/8/6/5`）。

| 来源 | canonical Artifact / SHA | 覆盖 |
|---|---|---|
| U04 导语/教材包 | `ART-PKG-X2-015-PDF` / `388cd404624d7ee079316dc15273e383409eb738aee523e8bee70adc681cd0bd` | 单元导语文化多样性语境，物理页106、切分页1 |
| 课13教材包 | `ART-PKG-X2-016-PDF` / `3e000c3958b8ee35f567a05abe700d134bd64d53b1ab2224be6e7517ccc98d59` | 四首诗、学习提示，物理页122—128、切分页1—7 |
| U04 任务 | `ART-PKG-X2-017-PDF` / `b3a30d48ce56c2de0f52cfcfc3eb55c938afc080148cc3329302154457735c48` | 单元研习任务，物理页129—130、切分页1—2 |
| 现行课标 | `ART-CURR-2020-PDF` / `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` | 任务群11与学业质量定位 |

账本当前条目 `CARD-X2-U04-02` 的路径、ID、状态 `linted`、版本 `0.3.0` 与卡片 front matter 一致，source_ids 已包含 EV-003 所用的 `SRC-PKG-X2-015`，并与其余 X2-016/017、CURR-2020 来源一致；ledger SHA 为本报告页眉绑定值。

## 2. Validator、结构与来源分层

`VAL-20260808-194012+0800` 的最新报告与归档报告均为 `passed`，0 errors，`hash_verification=true`。人工复核确认 4 个正文子文本、16/16 KP、23/23 EV 的 ID 唯一且全部被引用，EV 表为 9 列，Q/F/M/D 类型均为单值，核验状态均为 `verified`。导语、四首诗正文、学习提示、单元任务、课标、教师用书缺源声明和项目建议分层清楚；没有把外部诗评、其他译本、OCR 或项目建议冒充教材事实。

课13正文物理页122—128（切分页1—7）覆盖《迷娘》（之一）、《致大海》、《自己之歌》（节选）和《树和天空》；U04 导语 EV-003 使用已登记的 X2-015 canonical Artifact，任务和课标分别由 X2-017 与 CURR-2020 承担。

## 3. R02/R04/R08 重点 Claim—Evidence 复核

- **R02：否。** 23/23 EV 均解析到已核验 canonical Artifact；诗歌正文、学习提示和任务证据的 locator 与短引可回查。KP-003 的《迷娘》反复呼告由正文 EV-020 与学习提示 EV-004 双证；KP-006/007/011 的自由象征、情绪链、宏大自我和自然万物铺陈分别由正文与学习提示/任务的独立节点支撑；开放解读 KP-013 明确保留“可能关联主题”边界。没有需证主张无适配来源或 I 类解释单证情形。
- **R04：否。** U04 导语、四诗正文、学习提示、任务、课标和项目建议各自分层；EV-003 的导语虽来自 X2-015，但已在卡片 source_ids 与账本登记，且是规范学生教材来源，不是外部解析或 OCR 冒充。
- **R08：否。** 卡片、账本、4 个 SUBTEXT、KP、EV、Source、Artifact 的 ID、路径、版本和数量一致；当前卡 SHA 与本报告绑定 SHA 一致，账本已同步为 v0.3.0，X2-015/016/017 与课标来源链完整。

其余硬门：R01（作者/作品事实）、R03（合编覆盖/模块）、R05（KP字段）、R06（M0）、R07（上游）、R09（课标）、R10（核心素养/学业质量）均未触发。高考栏维持结构化 M0，纵向关系保持有理由的 N/A。

## 4. P0/P1/P2 与决定

`P0/P1/P2 = 0/0/0`。本轮没有开放缺陷，不存在阻断接受或需返工的证据、事实、来源分层或版本问题。

## 5. 七维评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.5 | 23/23 EV 有 canonical locator、Source/Artifact 和 verified 元数据；四诗/导语/任务跨包边界清楚，保守扣 0.5。 |
| 事实与术语准确性 | 20 | 18 | 20.0 | 四首诗作者、作品事实、放逐背景、诗体术语、任务群11和课标页位准确。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 4 个正文子文本、16 个文本特异 KP、23 个 EV及任务/课标/边界模块完整。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 自由/主体、人与自然、文化多样性与意象/节奏/象征分析相互支撑。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 每个 KP 均有四层归属和理由；高考严格保持 M0。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前无双方已验收目标，合法保持 N/A，不强造关系。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | 意象—情绪图谱、朗读/比较、改写与申论评价链可操作；多诗材料整理复杂，保守扣 0.5。 |
| **合计** | **100** | **85** | **98.5** | **总分及七维均达标。** |

**主审决定：`pass`。** 当前 v0.3.0/SHA 可进入独立第二复审；本报告不写回 `accepted`。

## 6. 复现绑定

卡片 SHA `5680a0b3b9080be9d2ea0ac573ecb331d2ee7a05baf7f6f72a77a34fb4cf31b7`；ledger SHA `82778a8a230aa5e662c6c2bce6ab368448c14eb67c8ccfd6765f965587acb321`；latest validator SHA `07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6`；archive validator SHA `07ceb9afd7dc13e90367d6d6d9fb5c1cfedaab0877ffc0ced35d0e5874f88ba6`；rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
