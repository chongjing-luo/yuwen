---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-02-SECONDARY-R1"
deliverable_id: "CARD-X3-U01-02"
artifact_version: "0.2.0"
artifact_sha256: "e445ecd610fbd7165d4cf192a4006cff30547102a3ec7e16df3d8fff17b7a2e7"
review_round: 1
reviewer: "independent_secondary_x3_u01_02_r1"
review_role: "secondary"
reviewed_at: "2026-08-08T21:23:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-211535+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "106204f5553675f2b90fc7fec0d63026ce5431a33032330fe47271ac41962dba"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-211535+0800.json"
validator_archive_report_sha256: "106204f5553675f2b90fc7fec0d63026ce5431a33032330fe47271ac41962dba"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "2e321ed7808a35d7411fffe8518c7f3008edaa7c3e6cf1f9808ac0ecb79778b9"
validator_result: "passed"
decision: "rework"
---

# CARD-X3-U01-02 v0.2.0 独立第二复审 R1

## 1. 输入锁定与独立性

本轮只依据当前 v0.2.0 卡片、冻结的 `2.0-textbook` rubric/taxonomy、来源与 Artifact 注册表、canonical 学生教材/单元任务/现行课标载体、共享账本和 validator 机械报告独立复核；不读取或复用旧报告、旧 SHA、旧分数或旧 R/P 结论。本轮不修改卡片、账本、validator 或状态迁移。

| 对象 | 最终快照绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-02.md`；v0.2.0；SHA `e445ecd610fbd7165d4cf192a4006cff30547102a3ec7e16df3d8fff17b7a2e7`；状态 `linted` |
| 正文/学习提示 Artifact | `ART-PKG-X3-002-PDF`；SHA `89a807fd0f166c4999331ca024f83d72f567aebce533b1eb23f34fa03faa32d5`；canonical 物理页12—18、切分页1—7 |
| U01任务 Artifact | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；canonical 物理页25—26、切分页1—2 |
| 现行课标 Artifact | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| validator | `VAL-20260808-211535+0800`；`passed`；0 errors；`hash_verification=true` |

当前正文结构为 1 个正文子文本、16/16 KP、10/10 EV；实际 EV 类型为 Q=9、M/D=1。card front matter 与 ledger 均为 v0.2.0、状态 `linted`，ID、路径和 Source 列表一致。

## 2. 内容、页码与证据复核

- 《孔雀东南飞并序》序文和正文覆盖物理页12—18/切页1—7；EV-001—006 的正文短引、EV-007—008 的学习提示短引均能在所声明范围回查。U01 任务 EV-009 的物理页25—26/切页1—2范围包含任务二至四原文；课标任务群5原文可在物理页25—27、学业质量4-3可在物理页46回查。
- 16/16 KP 均登记主维度、受控知识类型、四层主归属、判定理由、证据ID和置信状态；解释/比较类 KP 有正文、学习提示或任务证据。但 KP-008 的陈述把后续迎亲排场称为“县令迎亲”：正文先写“县令遣媒来”议第三郎，车马、钱帛、从人四五百等排场随后由“太守家/府君”安排（物理页15—16，切页4—5）。这是关键主体的张冠李戴。
- EV-010 同时写作 `M/D`，Claim 为“课标任务群5与学业质量边界、教师用书边界”，Source/Artifact 却只登记 `SRC-CURR-2020`/`ART-CURR-2020-PDF`；课标 PDF 可以支持任务群和学业质量 M 部分，但不能支持“未登记同版教师用书”D 部分。该行违反证据表明示的“类型只使用单值 Q/F/M/D”规则，也使该 Claim 的 Source—Artifact—quote 闭合不完整。
- 版本历史行称“12条单值Q/F/M/D证据”，而当前证据表只有 EV-001—010 共10行且含 `M/D`；自检勾选“每条EV的类型为单值”。这是数量与枚举声明的版本/结构漂移，触发 R08。M0 行还在“教材证据”栏挂载 EV-002、EV-007；冻结 M0 结构要求关系字段（含教材证据）为 `N/A`，候选能力和教材证据只能放入边界说明。
- 教师用书仅应作为 D 型缺源声明，`edition_match=unknown`；纵向保持有理由的 `N/A`，高考保持结构化 `M0`，当前未伪造 M1—M3 真题关系。

## 3. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | **是** | KP-008 将太守/府君的迎亲排场错写为县令迎亲；canonical 正文明确区分“县令遣媒”与“太守家/府君”迎亲。 |
| R02 | **是** | EV-010 将 M 与 D 两类主张混在一条证据中，且课标 Artifact 不承载教师用书缺源声明；正式 Claim—EV—Source/Artifact 闭合失败。 |
| R03 | 否 | 一个正文子文本、序文/正文/学习提示边界、U01任务、课标、教师用书边界、M0和纵向 N/A 模块均存在。 |
| R04 | 否 | 正文、学习提示、任务、课标和项目建议分层；KP-008的问题是事实主体错误，不是把网络解析冒充教材结论。 |
| R05 | 否 | 16/16 KP 都有主层级、知识类型、理由和证据ID；KP-008的事实错误和 EV-010 的证据问题不等同于字段缺失。 |
| R06 | 否 | 高考栏保持 `M0`，没有引用未登记真题或宣称直接衔接；M0字段规范错误另列 P2。 |
| R07 | 否 | 仅使用已验收教材包、任务包、现行课标和注册表，无未验收下游成果依赖。 |
| R08 | **是** | 当前表实际10 EV且含复合 `M/D`，版本历史却称12条单值证据；数量与受控枚举声明不一致。 |
| R09 | 否 | 使用现行课标版本及“文学阅读与写作”“语言积累、梳理与探究”规范名称，未把任务群改写为固定课型。 |
| R10 | 否 | 人文/语言双维度服务于叙事、对话和语言积累，未机械铺满核心素养，也未将学业质量当单课难度标签。 |

## 4. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、不可恢复损坏或大面积证据崩溃。 |
| P1 | **3** | `P1-KP008-FACT`：县令/太守迎亲主体张冠李戴；`P1-EV010-TYPE-SOURCE`：EV-010 使用非法复合类型且以课标 Artifact 承载教师用书 D 声明；`P1-VERSION-COUNT`：版本历史12条与当前10条EV及单值自检不一致。 |
| P2 | **1** | `P2-M0-EXTRA-EVIDENCE`：M0“教材证据”栏仍挂 EV-002、EV-007，应全部改为 `N/A`并把理由移至边界说明。 |

## 5. 2.0-textbook 诊断性评分

R01/R02/R08 为硬性否决；正式验收分数记为 `N/A`。以下仅为返工优先级的诊断值，不能抵消硬门或 P 项。

| 维度 | 权重 | 门槛 | 诊断得分 |
|---|---:|---:|---:|
| 证据链与可追溯性 | 25 | 21 | 19.0 |
| 事实与术语准确性 | 20 | 18 | 17.0 |
| 字段完整与知识粒度 | 15 | 12 | 14.0 |
| 双维度与母题质量 | 15 | 12 | 14.0 |
| 四层与高考映射 | 10 | 8 | 8.0 |
| 纵向贯通 | 8 | 6 | 8.0 |
| 教学可用性与表达 | 7 | 5 | 6.0 |
| **诊断合计** | **100** | **85** | **86.0** |

## 6. 独立第二复审 R1 决定

**正式决定：`rework`。** 当前 v0.2.0/SHA `e445ecd610fbd7165d4cf192a4006cff30547102a3ec7e16df3d8fff17b7a2e7` 不得进入 `accepted`、G4 或被 U01 单元图谱正式消费。最小返工要求：

1. 将 KP-008 的“县令迎亲”改为“太守/府君迎亲排场”，或收窄为“县令遣媒、太守府君迎亲”的准确事件链。
2. 将 EV-010 拆成单值 M 与 D 两条证据（D 应回链来源注册表/匹配教师用书缺源记录），分别更新 Claim、Artifact、locator、证据数量和 KP 引用。
3. 将 M0 的“教材证据”改为 `N/A`，修正版本历史中的12条/单值声明，升版、重算 SHA、复跑 validator，并由主审和独立第二复审对新 SHA 从零复核。

## 7. 可复现绑定

- latest validator：`VAL-20260808-211535+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `106204f5553675f2b90fc7fec0d63026ce5431a33032330fe47271ac41962dba`；归档报告 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-211535+0800.json` SHA 同为 `106204f5553675f2b90fc7fec0d63026ce5431a33032330fe47271ac41962dba`。
- ledger binding：`work/knowledge/_meta/deliverables.jsonl` SHA `2e321ed7808a35d7411fffe8518c7f3008edaa7c3e6cf1f9808ac0ecb79778b9`；当前状态仍为 `linted`，本报告不执行状态迁移。
- canonical Artifact SHA：`ART-PKG-X3-002-PDF`=`89a807fd0f166c4999331ca024f83d72f567aebce533b1eb23f34fa03faa32d5`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
