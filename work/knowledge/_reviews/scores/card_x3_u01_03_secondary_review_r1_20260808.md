---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-03-SECONDARY-R1"
deliverable_id: "CARD-X3-U01-03"
artifact_version: "0.2.0"
artifact_sha256: "c6388cbb05439e6ab3105e34df649c42371fb47d9c5d5104be4268217d1cb096"
review_round: 1
reviewer: "independent_secondary_x3_u01_03_r1"
review_role: "secondary"
reviewed_at: "2026-08-08T21:38:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "9bfee136f8917ef3c8e74d67f233580fbb20ca79cd500c23328721c8a0207a77"
validator_run_id: "VAL-20260808-213631+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-213631+0800.json"
validator_report_sha256: "aa66d88197a11d1219e7779d90c8f2885fff7524a47442dd383a19a7b916b9ed"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "7f033964d037759c55b4474a7b0de6ad26b6f3eaf99a6a2a73d8db09141b566c"
---

# CARD-X3-U01-03 v0.2.0 独立第二复审 R1

## 1. 输入锁定与独立性

本轮只依据指定的 v0.2.0 快照、冻结 `2.0-textbook` knowledge_card rubric/taxonomy、Source/Artifact 注册表、canonical 学生教材、U01 单元任务和现行课标重新核验；不修改卡片、账本、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-03.md`；v0.2.0；SHA `c6388cbb05439e6ab3105e34df649c42371fb47d9c5d5104be4268217d1cb096`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-003-PDF`；SHA `4d9e3d30605095b1a9131876a2e9fc2ebb6046ae9c48dfcedc0844f2e32a73ea`；物理页19—21、切分页1—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `9bfee136f8917ef3c8e74d67f233580fbb20ca79cd500c23328721c8a0207a77`；CARD-X3-U01-03 为 v0.2.0/`linted` |
| validator | `VAL-20260808-213631+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `aa66d88197a11d1219e7779d90c8f2885fff7524a47442dd383a19a7b916b9ed` |

卡片、账本、validator、rubric 和 taxonomy 的当前哈希与任务绑定一致。

## 2. canonical 页码、文本事实与证据复核

- 学生教材 canonical 物理页19—20/切分页1—2为《蜀道难》，物理页21/切分页3为《蜀相》及学习提示；任务二至任务四在任务包物理页25/切分页1。课标任务群5定位在规范物理页25—26，学业质量4-3定位在物理页46。
- 《蜀道难》EV-003—005的开篇神话/秦蜀阻隔、太白鸟道与六龙回日、黄鹤猿猱、悲鸟子规、飞湍雷声、剑阁守关风险和“早还家”均可在物理页19—20逐字回查；三次“蜀道之难”分别落在 EV-003、004、005 的页位。
- 《蜀相》EV-007的题名、作者、祠堂、柏森森、“自/空”、三顾两朝、出师未捷和泪满襟均在物理页21可见；EV-008逐字支持学习提示对古体/七律、李杜风格、诸葛亮评价及感时忧国的说明。
- EV-009—012的任务一、任务二、任务三虚实/意象探究和任务四800字鉴赏集要求均在任务包物理页25可回查；EV-013的任务群5定位、EV-014的课标学业质量4-3与规范课标物理页46均可回查。
- 结构计数为 `2/2` 正文子文本、`16/16` KP、`15/15` EV。KP主维度均为冻结枚举“人文/语言”，知识类型均为“事实/概念/程序/策略/解释/价值辨析”；EV类型为单值 F/Q/M/D，未见复合类型。
- M0表仅写 `N/A`，没有挂教材证据或真题ID；纵向关系为有理由的 `N/A`。教师用书为 `edition_match=unknown`，EV-015仅作缺源/边界声明，未把学习提示冒充教师用书意见。

两类非阻断性表达项需保留在问题单：部分复合 KP 的短引只列代表性片段而依赖同页上下文（如 KP-004/005/006/011），以及 KP-015 将“发言应保留诗句、观点形成过程和修订痕迹”写入任务程序，教材原文只明示研讨、提炼观点和代表发言；后者应在后续版本明确为本项目建议或收窄为教材直接成果。

## 3. R01—R10 判定

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 两首诗题名、作者、诗句、体式、人物/历史事实、任务与课标引文均与 canonical PDF 一致。 |
| R02 | 否 | 15/15 EV均有可解析 Source/Artifact/locator/短引；复合 KP 的局部短引仍可在锁定物理页回查，未形成关键事实不可定位。 |
| R03 | 否 | 两个正文子文本、学习提示、任务、课标、M0/N/A和三类教学提示模块齐全。 |
| R04 | 否 | 人文/语言研究性概括有正文与学习提示依据并明确边界；教师用书缺源和项目建议分栏，未互相冒充。 |
| R05 | 否 | 16/16 KP均有合法维度、知识类型、四层主归属、判定理由、证据ID和置信状态。 |
| R06 | 否 | 高考栏严格为M0/N/A，没有未登记真题、答案或评分资料。 |
| R07 | 否 | 仅消费已登记并核验的学生教材、任务包和现行课标canonical Artifact。 |
| R08 | 否 | 卡片当前SHA、版本、ledger transition、Source/Artifact ID及KP/EV数量一致。 |
| R09 | 否 | 使用现行课标任务群“文学阅读与写作”和“语言积累、梳理与探究”，没有改写为固定课型。 |
| R10 | 否 | 核心素养只作相关表现定位，未机械铺满四项，也未把学业质量4-3当作单课难度标签。 |

## 4. P0/P1/P2

`P0/P1/P2 = 0/0/2`。

- **P2-01（证据粒度）**：KP-004、KP-005、KP-006、KP-011等复合陈述的登记短引未逐项展开全部子短语，虽有合法宽页 locator 且可回查，建议下一版补连续最小 span。
- **P2-02（任务/项目建议边界）**：KP-015及§3“诵读与表达迁移”把“保留诗句、观点形成过程、反馈和修订”写成任务成果语气；教材任务直接要求的是研讨、提炼观点、代表发言、比较/探究和鉴赏集。建议显式标为“本项目建议”或收窄 Claim。

上述两项不影响当前事实、页码、受控枚举、M0/N/A和来源硬门，属于非阻断性可维护项。

## 5. 2.0-textbook 量规评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | 15/15 EV具备规范 Artifact、页位、短引和核验状态；复合 KP 的代表性短引与 D 边界声明保守扣1.0。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 两诗事实、体式、课标术语和页码准确；任务成果语气的边界歧义扣0.5。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2个正文子文本、16 KP、15 EV、任务/课标/教学/M0模块完整。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文线覆盖山川行旅、历史人物、忧国情志；语言线覆盖古体/七律、空间声音、炼字、虚实与比较；保留文本差异。 |
| 四层与高考映射 | 10 | 8 | 10.0 | KP四层理由、课标4-3边界和M0不确定性均清楚。 |
| 纵向贯通 | 8 | 6 | 8.0 | 没有双方 accepted 证据时保持合法N/A，不虚构递进边。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | 三类教学提示分栏且可操作；任务成果的项目化留痕语气需再标注，扣0.5。 |
| **合计** | **100** | **85** | **98.0** | 总分及七维单项均达到门槛；P2均为非阻断性建议。 |

## 6. 独立第二复审决定

**决定：`pass`。** 当前 `CARD-X3-U01-03` v0.2.0/SHA `c6388cbb05439e6ab3105e34df649c42371fb47d9c5d5104be4268217d1cb096` 通过独立第二复审，可与同一最终 SHA 的主审结果配对进入后续流程。当前 ledger 状态仍为 `linted`，本报告不执行状态迁移。卡片、canonical Artifact、validator、账本或版本绑定发生任何变化，均使本报告失效并须按新 SHA 重新复审。

## 7. 可复现绑定与报告校验

- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-213631+0800.json`；SHA `aa66d88197a11d1219e7779d90c8f2885fff7524a47442dd383a19a7b916b9ed`；`passed`、0 errors、`hash_verification=true`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `9bfee136f8917ef3c8e74d67f233580fbb20ca79cd500c23328721c8a0207a77`。
- canonical Artifact：`ART-PKG-X3-003-PDF`=`4d9e3d30605095b1a9131876a2e9fc2ebb6046ae9c48dfcedc0844f2e32a73ea`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 报告 SHA-256 按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 值置空后对 canonical 报告字节求 SHA，并回填于 front matter。

