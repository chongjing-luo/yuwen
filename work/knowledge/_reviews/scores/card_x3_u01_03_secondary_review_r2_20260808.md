---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-03-SECONDARY-R2"
deliverable_id: "CARD-X3-U01-03"
artifact_version: "0.2.2"
artifact_sha256: "23b15296d70abd7b8ddb0c7b17f5cc98b32baa6de05431ea3e914a95c5f99469"
review_round: 2
reviewer: "independent_secondary_x3_u01_03_r2"
review_role: "secondary"
reviewed_at: "2026-08-08T21:44:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "fea2e39b3722566a732903779186df186ea6cadb05ca8f255383adf10c9fa7e5"
validator_run_id: "VAL-20260808-214232+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-214232+0800.json"
validator_report_sha256: "d2775657eccadc182d34439da0dc90a0ee55e4c05912a1e6cc14c037f302d853"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "f6a8aedb7d51ff7e980d9369258c490bad1e328b9674a2cb0265cf9afb6387f6"
---

# CARD-X3-U01-03 v0.2.2 独立第二复审 R2

## 1. 输入锁定与独立性

本轮重新锁定 v0.2.2 快照，从 canonical PDF、任务包、课标和注册表独立核验正文事实、引文 span、枚举、M0/N/A及教师用书边界；不修改卡片、账本、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-03.md`；v0.2.2；SHA `23b15296d70abd7b8ddb0c7b17f5cc98b32baa6de05431ea3e914a95c5f99469`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-003-PDF`；SHA `4d9e3d30605095b1a9131876a2e9fc2ebb6046ae9c48dfcedc0844f2e32a73ea`；物理页19—21、切分页1—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；学业质量4-3物理页46 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `fea2e39b3722566a732903779186df186ea6cadb05ca8f255383adf10c9fa7e5`；CARD-X3-U01-03为v0.2.2/`linted` |
| validator | `VAL-20260808-214232+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `d2775657eccadc182d34439da0dc90a0ee55e4c05912a1e6cc14c037f302d853` |

任务给出的 card、ledger、validator、rubric 和 taxonomy SHA 均与当前文件实算一致。

## 2. canonical 页码、引文与修订项核验

- `2/2` 正文子文本覆盖完整：《蜀道难》位于学生教材物理页19—20/切分页1—2，《蜀相》及学习提示位于物理页21/切分页3；U01任务一至四位于任务包物理页25/切分页1；课标任务群5位于物理页25—26，学业质量4-3位于物理页46。
- EV-003已扩展为《蜀道难》第一段连续最小原文，包含“六龙回日”“扪参历井”等 KP-004/005 所需 span；EV-004为第二段连续原文，EV-005为第三段连续原文，KP-006/007/008的声音、剑阁和三次回环均可逐字回查。
- EV-001已收窄为课文包正文范围，不再把任务包/课标混入同一来源职责；§8.1只陈述教材学习提示原意，项目证据表和比较操作未冒充教材要求。
- 《蜀相》正文四联、题名作者和学习提示均与学生教材物理页21一致；课标 EV-014 的 `4-3` 引文与规范物理页46逐字一致。任务 EV-009—012 的研讨、比较、虚实/意象探究、800字鉴赏与鉴赏集要求均可在物理页25回查。
- `16/16` KP 的主维度、知识类型、四层、理由、证据和置信状态齐全且受控；`15/15` EV 的类型为单值 F/Q/M/D。M0所有真题/KP/教材证据字段均为 `N/A`；纵向关系为有理由的 `N/A`；教师用书 `edition_match=unknown` 且未被写成当前编者意见。

仍保留一项低风险证据粒度建议：KP-011把“才干、德行”与“三顾、两朝、开济”合并为一项，登记 EV-007 的诗句虽能回到正文，但学习提示中“才干、德行”的明确措辞在 EV-008；后续可补挂 EV-008 或拆分 Claim。该项不影响当前核心事实和页码验收。

## 3. R01—R10 判定

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两首诗题名、作者、正文事实、体式、诸葛亮/蜀道叙述及课标页46引文均与 canonical 载体一致。 |
| R02 | 否 | 15/15 EV均有可解析 Source/Artifact/locator/短引；三段《蜀道难》连续 span已补齐，KP-011的单项粒度建议不构成不可定位主张。 |
| R03 | 否 | 两个正文子文本、学习提示、U01任务、课标、三类教学提示、M0和纵向N/A模块齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标M、教师用书D和本项目建议分层；没有把OCR、网络解释或学生提示冒充教师用书意见。 |
| R05 | 否 | 16/16 KP均使用合法“人文/语言”主维度和冻结知识类型，并有四层、理由、证据及置信状态。 |
| R06 | 否 | 高考栏保持M0/N/A，没有未登记真题、答案或评分资料。 |
| R07 | 否 | 仅消费已登记并核验的学生教材、任务包和现行课标canonical Artifact。 |
| R08 | 否 | 当前card SHA、version、ledger transition、Source/Artifact ID、KP/EV数量及路径一致。 |
| R09 | 否 | 使用现行课标任务群名称，未把任务群写成固定课型或教法。 |
| R10 | 否 | 核心素养仅作相关表现定位，未机械铺满四项，也未把学业质量4-3当作单课难度标签。 |

## 4. P0/P1/P2

`P0/P1/P2 = 0/0/1`。

- **P2-01（可维护证据粒度）**：KP-011的“三顾/两朝/开济—才干/德行/功业”复合 Claim 可补挂 EV-008 或拆成最小命题。当前 EV-007 locator 与诗句事实有效，故不构成P1或R02。

无P0/P1；没有影响当前验收的事实错误、错页、非法枚举、M0越权、教师用书误引或版本断链。

## 5. 2.0-textbook 量规评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.5 | 15/15 EV的Source/Artifact/locator/短引可回查；KP-011复合Claim的学习提示措辞尚未逐项回链，扣0.5。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两诗文本事实、体式、人物和课标术语准确；KP-011粒度边界保守扣0.5。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2子文本、16 KP、15 EV、课标/任务/教学/M0/N/A模块完整。 |
| 双维度与母题质量 | 15 | 12 | 15.0 | 人文线覆盖险阻、历史记忆、未捷忧国；语言线覆盖古体/七律、空间/声音/炼字、虚实和比较；差异保留充分。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层理由、课标4-3边界和M0不确定性完整。 |
| 纵向贯通 | 8 | 6 | 8.0 | 没有双方accepted证据时合法保持N/A，不强造递进边。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 教材提示、教师用书边界和项目建议三栏分离；修订后的8.1可直接转成诵读、证据表和鉴赏任务。 |
| **合计** | **100** | **85** | **99.0** | 所有单项及校准门槛均达到；P2为非阻断性维护建议。 |

## 6. 独立第二复审决定

**决定：`pass`。** 当前 `CARD-X3-U01-03` v0.2.2/SHA `23b15296d70abd7b8ddb0c7b17f5cc98b32baa6de05431ea3e914a95c5f99469` 通过独立第二复审，可与同一最终 SHA 的主审结果配对进入后续流程。当前 ledger 状态仍为 `linted`；本报告不执行状态迁移。卡片、canonical Artifact、validator、账本或绑定任一变化均使本报告失效，须按新 SHA 重新复审。

## 7. 可复现绑定与报告校验

- validator归档报告：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-214232+0800.json`；SHA `d2775657eccadc182d34439da0dc90a0ee55e4c05912a1e6cc14c037f302d853`；`passed`、0 errors、`hash_verification=true`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `fea2e39b3722566a732903779186df186ea6cadb05ca8f255383adf10c9fa7e5`。
- canonical Artifact：`ART-PKG-X3-003-PDF`=`4d9e3d30605095b1a9131876a2e9fc2ebb6046ae9c48dfcedc0844f2e32a73ea`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 报告 SHA-256 按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 值置空后对 canonical 报告字节求 SHA，并回填于 front matter。

