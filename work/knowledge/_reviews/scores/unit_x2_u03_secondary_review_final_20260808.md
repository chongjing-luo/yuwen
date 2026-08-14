---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X2-U03-SECONDARY-FINAL"
deliverable_id: "UNIT-X2-U03"
artifact_version: "0.2.0"
artifact_sha256: "ef198aa567ab0dd31596aee371c763ca4d17e2c6a3bb7f649e277b3d59b1d2dc"
review_round: 1
reviewer: "independent_secondary_unit_x2_u03_final"
review_role: "secondary"
reviewed_at: "2026-08-08T19:50:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-190644+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "090a949289c3b185b08bbcfb0c3252b19a6dcdd05a0a305fcbc18dbf2cfd76db"
validator_archive_sha256: "29e0c6bd8e3bc1379bf4277761f0cb83d164c80ff8d01efbc4eca7b5aeb839b0"
ledger_sha256: "46ccc5a8a4213e5a1a1c26fd04d709a7bbf40675daf907b996f705ec39ea7a21"
validator_result: "passed"
decision: "pass"
---

# UNIT-X2-U03 v0.2.0 独立第二复审

## 1. 输入锁定与独立性

本轮只依据当前单元图谱、三张当前 `accepted` 上游卡、来源/Artifact 注册表、U03 任务包、现行课标、冻结 rubric/taxonomy 和 validator 机械报告独立判断；未读取主审报告、主审分数或主审缺陷结论，也未修改图谱、ledger 或状态迁移。当前节点采用稳定的 `CAND-H-*`/`CAND-L-*` 前缀，任务采用 `TASK-*` 前缀。

| 对象 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修中册/units/UNIT-X2-U03.md`；v0.2.0；SHA `ef198aa567ab0dd31596aee371c763ca4d17e2c6a3bb7f649e277b3d59b1d2dc`；状态 `linted` |
| `CARD-X2-U03-01` | accepted / v0.2.3 / SHA `0d6a0e46d3a2ec0521eff31d363a63de3b3914336d4a47921756114b05bb5ce4` |
| `CARD-X2-U03-02` | accepted / v0.2.4 / SHA `74459ad46c63cdd78b74c6d4d5434ba8cb157e228f29a38e3435b9498a2f49f6` |
| `CARD-X2-U03-03` | accepted / v0.2.4 / SHA `6ee9e835dded3cb1a47aae0481735d94eb2d9cac63e379ed445ec99d1902b035` |
| validator | `VAL-20260808-190644+0800`；passed；0 errors；`hash_verification=true` |

canonical Artifact 均与注册表和图谱 §1 一致：`ART-PKG-X2-011-PDF` `a32687c5561efa28c5d1924a75f6762dae2dc605e9921915b6095141220182d4`、`ART-PKG-X2-012-PDF` `97121b4473d6515eaacdf1e7576b02ed21b7482cc1c0977e3763bae30a3f6885`、`ART-PKG-X2-013-PDF` `0e9fc707b2e53ca026c559717c60ec88f3a5f8344f2b2d930ba8632ef992c3a4`、任务包 `ART-PKG-X2-014-PDF` `0479f6c8ba0eec387251220f76e97014c14d27787e992e557eef30eadffb82cb`、课标 `ART-CURR-2020-PDF` `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。

## 2. 覆盖、回链与结构复核

- 上游覆盖闭合：3/3 accepted 卡、4/4 正文子文本、47/47 KP 均有稳定入口；独立脚本复算 KP 集合为 47/47，图谱引用的 37 个 EV-ID 均存在于对应当前卡。
- 节点/任务结构闭合：4 个 `CAND-H` 人文节点、2 个 `CAND-L` 语言节点、5 项任务、5 条跨课/迁移关系、1 行结构化 M0 和 2 行有理由的纵向 N/A 均有稳定 ID。任务一至五均有任务包物理页/切分页、原文短引、能力动作、学习成果和评价证据。
- 人文综合覆盖屈原、苏武、两篇史论及证据边界；语言综合覆盖史传/史论文体比较、叙议与剪裁、文言句式、名词作状语和背诵迁移。共性、差异、迁移关系均标为单元综合，不冒充教材原文。
- 上游 SHA 逐一复算与图谱 §1 的 post-merge SHA 相同；当前卡 ledger 状态均为 `accepted`，图谱自身仍为 `linted`，不存在消费未验收上游的问题。
- 高考栏保持 `N/A | M0 | N/A | N/A`，明确无已登记真题/答案/评分双向证据；前后单元无双方 accepted 且逐边可核验目标时保持合法 N/A；教师用书 `edition_match=unknown`，未用于补正文解释。

## 3. R01—R10 与 P 级缺陷

| 代码 | 触发 | 独立结论 |
|---|---|---|
| R01 | 否 | 节点、任务、课文/作者和史实综合均可回到当前 accepted 卡及 canonical 任务包。 |
| R02 | 否 | 47/47 KP、节点、任务和关系均有 Card/KP/EV 或任务来源回链；任务原文定位可解析，未见需证的综合主张无适配来源。 |
| R03 | 否 | 3 卡、4 子文本、47 KP、4 H、2 L、5 TASK、关系、M0、纵向和 Issue 模块齐全。 |
| R04 | 否 | 教材正文、学习提示、上游研究解释、课标、项目评价、教师用书缺源和学生产出边界分层清楚。 |
| R05 | 否 | 47/47 KP 保留上游主维度/类型/层级和证据，并有节点或任务入口。 |
| R06 | 否 | 未登记真题不作为实证；高考仅保留结构化 M0。 |
| R07 | 否 | 3 个上游状态均为 `accepted`，且 post-merge SHA 与当前卡文件逐一匹配。 |
| R08 | 否 | 图谱版本、卡/KP/EV/TASK/节点/关系 ID、数量、路径和 SHA 链闭合。 |
| R09 | 否 | 使用现行 2020 修订课标及受控任务群名称，未把任务群改作固定课型/教法。 |
| R10 | 否 | 未机械铺满核心素养，也未把学业质量水平当作单元难度标签。 |

P0/P1/P2：`0/0/0`。

## 4. 2.0-textbook unit_graph 量规评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 3/3 accepted 卡、4/4 子文本、47/47 KP、5/5 任务和有效 Card/KP/EV 回链；上游 SHA 已逐一复算。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **19.0** | 4 H/2 L 节点与 5 条受控关系保留史传/史论共性和文体差异；综合命题有卡片证据和任务证据，关系压缩表示保留检索余量。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | 人文节点覆盖三课历史人物/兴亡议题，语言节点覆盖史传史论、文言积累和迁移任务，并有交叉关系。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 5 项任务均有 canonical 原文、物理页/切分页、能力动作、学习成果和评价底线。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | 结构化 M0、真题未登记边界和 G-TB 后重开条件明确，无越级映射。 |
| 前后递进 | 10 | 8 | **10.0** | 前后目标在无双方 accepted 且逐边证据时均给出理由充分的 N/A，未以单元排列强造递进。 |
| 可读性与检索性 | 5 | 4 | **4.5** | §1.1 覆盖索引、节点/任务/关系表和 Issue 清单齐全；少数关系以压缩 EV 范围表达，需回看上游卡定位。 |
| **合计** | **100** | **88** | **98.5** | 总分及各维度均达到冻结门槛。 |

## 5. 独立第二复审决定

**决定：`pass`。** 当前图谱 v0.2.0/SHA `ef198aa567ab0dd31596aee371c763ca4d17e2c6a3bb7f649e277b3d59b1d2dc` 可与同 SHA 主审报告配对进入 G4。图谱在 G4 写回前仍不得标记为 `accepted`；任一上游卡、canonical Artifact、图谱正文或 ledger 绑定变化都会使本报告失效并要求重审。

## 6. 可复现绑定

- latest validator：`VAL-20260808-190644+0800`，passed，0 errors，`hash_verification=true`；latest 报告 SHA `090a949289c3b185b08bbcfb0c3252b19a6dcdd05a0a305fcbc18dbf2cfd76db`；归档 g2 SHA `29e0c6bd8e3bc1379bf4277761f0cb83d164c80ff8d01efbc4eca7b5aeb839b0`。
- ledger SHA：`46ccc5a8a4213e5a1a1c26fd04d709a7bbf40675daf907b996f705ec39ea7a21`；rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 分母复算：3 张 accepted 卡、4 个正文子文本、47 KP、4 H、2 L、5 TASK、5 REL、1 行 M0、2 行纵向 N/A。
