---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X2-U04-SECONDARY-FINAL"
deliverable_id: "UNIT-X2-U04"
artifact_version: "0.2.0"
artifact_sha256: "10a30fbbf5af169e1651ff89ec0d9e49879cbe3a854c6058ceb4cf42d53f7d6f"
review_round: 1
reviewer: "independent_secondary_unit_x2_u04_final"
review_role: "secondary"
reviewed_at: "2026-08-08T20:20:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-195345+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "e7347b4892e03ff0db18e044e4cad9479403f07e24c71d4bd873ddadc763eeca"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-195345+0800.json"
validator_archive_report_sha256: "e7347b4892e03ff0db18e044e4cad9479403f07e24c71d4bd873ddadc763eeca"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "53e8a978d4412977fc836f412cdf5599752d07a2d1b26d710e843455e40d94ba"
validator_result: "passed"
decision: "pass"
---

# UNIT-X2-U04 v0.2.0 独立第二复审

## 1. 输入锁定与独立性

本轮只依据最终快照中的当前单元图谱、两张 `accepted` 上游知识卡、来源/Artifact 注册表、U04 单元研习任务包、现行课标、冻结 rubric/taxonomy、共享 ledger 和 validator 机械报告独立判断；未读取或复用主审报告、主审分数或主审缺陷结论，不修改图谱、上游卡、ledger、deliverable 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修中册/units/UNIT-X2-U04.md`；v0.2.0；SHA `10a30fbbf5af169e1651ff89ec0d9e49879cbe3a854c6058ceb4cf42d53f7d6f`；状态 `linted` |
| `CARD-X2-U04-01` | `accepted` / v0.3.0 / post-merge SHA `63683985b71331d6dc3b31fefc7bd0680a19a9a32c9ca7a0193b6dd303b1421c` |
| `CARD-X2-U04-02` | `accepted` / v0.3.0 / post-merge SHA `734847eaa30b6ddf3c8dff8540a1850ea98308692b1bb46a5020fbdc5ae80560` |
| 任务包 | `ART-PKG-X2-017-PDF`；SHA `b3a30d48ce56c2de0f52cfcfc3eb55c938afc080148cc3329302154457735c48`；canonical 物理页129—130、切分页1—2 |
| 课标 | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| validator | `VAL-20260808-195345+0800`；`passed`；0 errors；`hash_verification=true` |

图谱覆盖声明独立复算为 2/2 accepted 上游卡、5/5 正文子文本、31/31 KP、5/5 单元任务、4 个人文节点、4 个语言节点、8/8 单元关系、1 行结构化 M0 和 2 行纵向 N/A。图谱中的 `CAND-*`/`REL-*` 是基于上游证据的单元级综合，不冒充教材原文。

## 2. 覆盖、上游状态与回链复核

- 两张上游卡的 ledger 状态均为 `accepted`，版本均为 v0.3.0；图谱 §1 记录的 post-merge SHA 与当前卡文件逐一复算一致。未发现消费旧 SHA、`drafted` 卡或未验收上游的路径。
- 31/31 KP 在 §1.1 有唯一入口：卡01 15 个 KP、卡02 16 个 KP 均进入至少一个人文/语言节点或任务入口，并带有直接 EV 回链。表中 `001/002` 等斜线只是同一前缀下的紧凑 ID 写法，按图谱说明展开后均能在 accepted 卡证据表中找到。
- 4 个人文节点、4 个语言节点和 8 条 `REL-UNIT-X2-U04-*` 关系均有稳定 ID、源/目标、受控关系类型、共性/差异或迁移理由；关系证据同时覆盖源侧卡/KP/EV与目标侧节点/任务页。综合命题均标为 `CAND`，未新增无来源教材事实。
- `CARD-X2-U04-01` 的戏剧冲突/主体选择和 `CARD-X2-U04-02` 的诗歌意象/形式/文化表达保持正文、学习提示、任务和学生产出边界；未把鲁迅《娜拉走后怎样》或申论学生判断冒充教材正文。

## 3. 单元任务与双向证据复核

| 任务 | 独立复核结论 |
|---|---|
| `TASK-X2-U04-01` | 物理页129/切分页1，任务一第1项；原文要求梳理冲突、解释娜拉出走及社会意义；能力动作、成果和评价均回链卡01 KP-003—014 与正文/舞台动作 EV。 |
| `TASK-X2-U04-02` | 物理页129/切分页1，任务一第2项；原文要求按人物性格逻辑和社会环境设想结局并阅读鲁迅文章；外部文章单独标注，回链卡01 KP-005—010、013—015。 |
| `TASK-X2-U04-03` | 物理页129/切分页1，任务二第1项；《迷娘》（之一）和《树和天空》意象—情绪—节奏探究，回链卡02 KP-001—004、012—015；开放意境未压成唯一主题。 |
| `TASK-X2-U04-04` | 物理页129/切分页1，任务二第2项；《致大海》与《自己之歌》体式、节奏比较及形式改写，回链卡02 KP-005—011、014—015；保留原诗主题/意象的约束明确。 |
| `TASK-X2-U04-05` | 物理页129—130/切分页1—2，任务三；围绕“文化走出去”提炼观点、联系社会生活并完成不少于1000字申论，回链卡02 KP-001、016 和 EV-016/017；评价包含问题—对策—论证链。 |

五项任务均同时具备 canonical 原文短引、物理页/切分页、能力动作、学习成果和评价证据。关系表中的 `双向证据与状态` 字段虽采用卡片 EV 与任务页的压缩表示，但源/目标两端可由对应 ID、EV 和定位回查；未见单向无证迁移。

## 4. M0、纵向关系与边界治理

- 高考栏为结构化 `N/A | M0 | N/A`：当前未登记可逐小问核验的真题、答案和评分 Artifact，因此不把人物形象、戏剧冲突、意象作用、诗体节奏或申论的一般题型相似性升级为 M1/M2/M3；待 G-TB 后按小问—答案/评分—KP/EV 双向核验重开。
- 前序、后续均为有理由的 `N/A`：目前没有与 U04 同层级且双方 accepted、可逐边核验的目标图谱；不以“文学阅读”或单元排列顺序强造递进。
- 课标、教师用书和外部材料边界透明；上游卡教师用书 `edition_match=unknown`，图谱不消费缺源意见补正文解释。项目建议、学生改写、结局设想和申论成果均与教材事实分层。

## 5. R01—R10 与 P0/P1/P2

| 代码 | 触发 | 独立结论 |
|---|---|---|
| R01 | 否 | 5 个正文子文本、任务短引、作者/作品及单元综合均可回到 accepted 卡和 canonical 任务包。 |
| R02 | 否 | 31/31 KP、4 H、4 L、5 TASK、8 REL 均有 Card/KP/EV 或任务来源回链；无需证的综合主张无适配来源。 |
| R03 | 否 | 两卡、5 子文本、31 KP、5 TASK、H/L 节点、REL、M0、纵向和 Issue 模块齐全。 |
| R04 | 否 | 教材事实、学习提示、上游解释、课标、项目评价、教师用书缺源、外部材料和学生产出分层清楚。 |
| R05 | 否 | 31/31 KP 均保留上游主维度/类型/层级和 EV，并进入至少一个节点或任务。 |
| R06 | 否 | 未登记真题不作为实证，高考严格保持结构化 M0。 |
| R07 | 否 | 2/2 上游卡均为 `accepted`，post-merge SHA 与当前文件和图谱 §1 一致。 |
| R08 | 否 | 图谱版本、卡/KP/EV/TASK/CAND/REL ID、数量、路径和 SHA 链闭合。 |
| R09 | 否 | 使用现行 2020 修订课标及受控任务群名称，未制造固定课型或教法。 |
| R10 | 否 | 未机械铺满核心素养，也未把学业质量水平当作单元难度标签。 |

P0/P1/P2：`0/0/0`。

## 6. 2.0-textbook unit_graph 量规评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | **25.0** | 2/2 accepted 卡、5/5 子文本、31/31 KP、5/5 任务、4 H、4 L、8 REL 均有稳定入口和回链；上游 post SHA 逐一复算。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | **19.0** | 戏剧社会问题与诗歌自我/自然、形式/节奏差异均被保留；关系证据采用压缩 EV 范围，需回看上游卡定位，保守扣 1 分。 |
| 人文与语言双维度结构 | 15 | 12 | **15.0** | 4 个人文节点、4 个语言节点和交叉关系覆盖文化多样性、主体/自然、戏剧冲突、意象、诗体及申论表达。 |
| 单元任务拆解 | 15 | 12 | **15.0** | 5 项任务均有 canonical 原文、页码、能力动作、成果和评价底线；任务与 KP/EV 双向回链清楚。 |
| 高考衔接及证据 | 10 | 8 | **10.0** | M0、N/A、无真题边界和 G-TB 后重开条件明确，无越级映射。 |
| 前后递进 | 10 | 8 | **10.0** | 前后目标在无双方 accepted 且逐边证据时均给出理由充分的 N/A，未以单元排列强造递进。 |
| 可读性与检索性 | 5 | 4 | **4.5** | §1.1 全量 KP 索引、任务/节点/关系表和 Issue 清单齐全；斜线压缩 EV 和关系 CAND 状态要求回看上游卡，保守扣 0.5 分。 |
| **合计** | **100** | **88** | **98.5** | 总分及各维度均达到冻结门槛。 |

## 7. 独立第二复审决定

**决定：`pass`。** 当前 `UNIT-X2-U04` v0.2.0/SHA `10a30fbbf5af169e1651ff89ec0d9e49879cbe3a854c6058ceb4cf42d53f7d6f` 可与同一最终 SHA 的独立主审配对进入 G4。图谱在 G4 写回前仍不得标记为 `accepted`，也不得供 `BOOK-X2` 消费；图谱、任一上游卡、canonical Artifact、validator 或 ledger 绑定发生变化均使本报告失效并需重审。

## 8. 可复现绑定

- 图谱：`work/knowledge/选择性必修中册/units/UNIT-X2-U04.md`；v0.2.0；SHA `10a30fbbf5af169e1651ff89ec0d9e49879cbe3a854c6058ceb4cf42d53f7d6f`。
- 上游 accepted post SHA：`CARD-X2-U04-01`=`63683985b71331d6dc3b31fefc7bd0680a19a9a32c9ca7a0193b6dd303b1421c`；`CARD-X2-U04-02`=`734847eaa30b6ddf3c8dff8540a1850ea98308692b1bb46a5020fbdc5ae80560`。
- latest validator：`VAL-20260808-195345+0800`；`work/knowledge/_meta/validation_reports/latest.json` SHA `e7347b4892e03ff0db18e044e4cad9479403f07e24c71d4bd873ddadc763eeca`；归档运行报告 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-195345+0800.json` SHA 同为 `e7347b4892e03ff0db18e044e4cad9479403f07e24c71d4bd873ddadc763eeca`；passed，0 errors，`hash_verification=true`。
- ledger/deliverables binding：`work/knowledge/_meta/deliverables.jsonl` SHA `53e8a978d4412977fc836f412cdf5599752d07a2d1b26d710e843455e40d94ba`；图谱当前状态仍为 `linted`，本报告不执行状态迁移。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。

复算分母：2 张 accepted 卡、5 个正文子文本、31 KP、5 TASK、4 H、4 L、8 REL、1 行结构化 M0、2 行纵向 N/A。
