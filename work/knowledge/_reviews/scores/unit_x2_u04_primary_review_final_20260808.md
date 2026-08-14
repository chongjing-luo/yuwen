---
schema_version: "2.0-candidate"
review_id: "REV-UNIT-X2-U04-FINAL-PRIMARY"
deliverable_id: "UNIT-X2-U04"
artifact_version: "0.2.0"
artifact_sha256: "10a30fbbf5af169e1651ff89ec0d9e49879cbe3a854c6058ceb4cf42d53f7d6f"
review_round: 1
reviewer: "independent_primary_unit_x2_u04_final"
review_role: "primary"
reviewed_at: "2026-08-08T19:58:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "53e8a978d4412977fc836f412cdf5599752d07a2d1b26d710e843455e40d94ba"
validator_run_id: "VAL-20260808-195345+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "e7347b4892e03ff0db18e044e4cad9479403f07e24c71d4bd873ddadc763eeca"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-195345+0800.json"
validator_archive_report_sha256: "e7347b4892e03ff0db18e044e4cad9479403f07e24c71d4bd873ddadc763eeca"
validator_result: "passed"
decision: "pass"
---

# UNIT-X2-U04 v0.2.0 独立主审

## 1. 锁定对象、量表与上游门禁

本轮只审当前 `UNIT-X2-U04` 图谱，不复用旧图谱结论，不修改图谱、上游卡、账本、验证归档或下游图谱。冻结量表为 `2.0-textbook` 单元图谱量表：总分门槛 88，七维门槛 `22/16/12/12/8/8/4`。

| 项目 | 当前绑定 |
|---|---|
| 图谱 | `work/knowledge/选择性必修中册/units/UNIT-X2-U04.md`；v0.2.0；SHA `10a30fbbf5af169e1651ff89ec0d9e49879cbe3a854c6058ceb4cf42d53f7d6f` |
| 上游卡01 | `CARD-X2-U04-01` v0.3.0，`accepted`，post-merge SHA `63683985b71331d6dc3b31fefc7bd0680a19a9a32c9ca7a0193b6dd303b1421c` |
| 上游卡02 | `CARD-X2-U04-02` v0.3.0，`accepted`，post-merge SHA `734847eaa30b6ddf3c8dff8540a1850ea98308692b1bb46a5020fbdc5ae80560` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；当前 SHA `53e8a978d4412977fc836f412cdf5599752d07a2d1b26d710e843455e40d94ba`；图谱条目为 `linted / v0.2.0`，路径、source_ids、upstream_card_ids 与 front matter 一致 |
| validator | `VAL-20260808-195345+0800`；latest 与 archive 均 `passed`、0 errors、`hash_verification=true` |

图谱登记的 canonical 包与任务/课标载体均为已验证 S1 来源：`ART-PKG-X2-015-PDF` / `388cd404624d7ee079316dc15273e383409eb738aee523e8bee70adc681cd0bd`，`ART-PKG-X2-016-PDF` / `3e000c3958b8ee35f567a05abe700d134bd64d53b1ab2224be6e7517ccc98d59`，`ART-PKG-X2-017-PDF` / `b3a30d48ce56c2de0f52cfcfc3eb55c938afc080148cc3329302154457735c48`，`ART-CURR-2020-PDF` / `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。

## 2. Validator 与结构复算

Validator 六项检查（contracts、deliverables、existing_outputs、registry_links、rubrics、taxonomy）均通过，`errors=[]`，`hash_verification=true`；归档报告与 latest SHA 相同。独立结构复算确认：

- `2/2` 上游卡均为 `accepted`，版本与图谱 §1 的 post-merge SHA 完全一致；
- `5/5` 正文子文本覆盖（《玩偶之家》及四首诗）；
- `31/31` KP 在 §1.1 逐项列出，至少进入一个 H/L 节点或任务，并带直接 EV 回链；没有孤立 KP；
- `4` 个人文节点、`4` 个语言节点、`5/5` 单元任务、`8/8` 单元内部关系均有稳定 ID；
- 高考栏为一行结构化 `N/A | M0 | N/A | N/A`；前序、后续各一行合法 N/A，并写明无双方 accepted 目标证据的原因。

图谱 §1.1 的斜线/短横线是明确声明的紧凑枚举写法；按其说明展开后，31 个 KP 与两张 accepted 卡的 KP/EV 可逐项解析。节点、关系和任务的综合陈述均使用 `CAND-`/`REL-`/`TASK-` 稳定 ID，且标明综合或项目评价身份，不冒充教材原文。

## 3. 节点、任务与关系独立核查

### 3.1 人文与语言节点

- `CAND-H-X2-U04-001` 以 U04 导语建立外国文学文化多样性语境，并明确不替代正文结论；其 EV 来自两张卡的导语/作品/课标证据。
- `CAND-H-X2-U04-002` 将《玩偶之家》的借款危机、海尔茂的名誉/占有逻辑、娜拉的主体确认和开放结尾串为社会问题剧议题，均回链卡01 EV-003—010、013、020—023。
- `CAND-H-X2-U04-003` 将四首诗的意象、自由/主体、自然与开放想象并置，回链卡02 KP-002—013 及正文/学习提示 EV；未压缩成唯一主题。
- `CAND-H-X2-U04-004` 明示“文化走出去”是任务与项目评价框架的综合，不是诗歌正文结论，回链任务、卡02 KP-001/016 和课标证据。
- `CAND-L-X2-U04-001—004` 分别覆盖戏剧事件—言行—舞台动作链、诗歌意象—情绪—节奏链、诗体比较/改写和证据驱动申论；每个节点均有 Card/KP/EV 或任务入口。

### 3.2 五项单元任务

五项任务均指向 `ART-PKG-X2-017-PDF` 物理页129—130（切分页1—2），并将原文任务、能力动作、学习成果和项目评价证据分层：

1. `TASK-X2-U04-01`：梳理矛盾冲突、解释娜拉出走和社会意义；
2. `TASK-X2-U04-02`：联系性格逻辑/社会环境设想结局，并对读《娜拉走后怎样》；
3. `TASK-X2-U04-03`：朗读《迷娘》（之一）和《树和天空》，梳理意象组合与情感流动；
4. `TASK-X2-U04-04`：比较《致大海》与《自己之歌》的诗体/节奏并完成边界清楚的改写；
5. `TASK-X2-U04-05`：完成“文化走出去”1000 字以上、90 分钟申论，经历观点归纳—问题分析—对策—论证。

每项任务均有对应的上游 KP 回链、物理页/切分页定位和可评价成果；外部文章、学生结局设想/改写和项目评价没有被写成教材正文事实。

### 3.3 八条关系

`REL-UNIT-X2-U04-001—008` 的类型均来自 taxonomy 受控集合（组成、冲突、迁移、深化、比较）。源/目标节点或 KP、迁移/差异说明和双向 Card/KP/EV 证据均齐全：导语到戏剧/诗歌具体化、戏剧冲突到任务迁移、意象到朗读任务、诗体比较到改写、外国文学证据链到申论、以及人文主题与语言形式的比较，均没有以单元顺序替代关系证据。

## 4. M0、N/A、教师用书与 R01—R10

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 上游卡、五个正文子文本、任务和课标事实均与已验收 canonical 来源一致。 |
| R02 | 否 | 31/31 KP、4H/4L 节点、5任务和8关系均有可定位 Card/KP/EV 或任务来源；综合解释有适配上游证据与边界声明。 |
| R03 | 否 | 上游清单、正文子文本、KP索引、任务、双维度节点、关系、M0、纵向和覆盖自检齐全。 |
| R04 | 否 | 教材原文、上游卡研究解释、单元综合、项目评价、外部材料和教师用书缺源分层清楚；未把 CAND 结论冒充教材明示。 |
| R05 | 否 | 31/31 KP 至少进入节点或任务，均有合法入口和直接 EV 回链；无孤立 KP。 |
| R06 | 否 | 仅保留合法结构化 M0；未登记真题、答案或评分 Artifact 未被消费，也未将题型相似性升级为 M1—M3。 |
| R07 | 否 | 2/2 上游均为 ledger `accepted` 且 post-merge SHA 与图谱一致；任务/课标为已验证 canonical 来源。 |
| R08 | 否 | 图谱版本、路径、upstream_card_ids、卡片 post SHA、31 KP、5任务、8关系及节点 ID/数量均一致；validator hash verification=true。 |
| R09 | 否 | 使用现行 2020 修订课标和受控任务群边界，未把任务群改写为固定课型/固定教法。 |
| R10 | 否 | 未机械铺满核心素养，也未给单元贴完整学业质量水平标签。 |

教师用书：两张上游卡均为 `edition_match=unknown`，图谱不消费教师用书意见；前序/后续无可靠双方证据时保持合法 N/A，不以宽泛“文学阅读”或单元顺序造递进。

## 5. P0/P1/P2 与决定

`P0/P1/P2 = 0/0/0`。本轮未发现需阻断接受的覆盖、证据、任务、关系、M0/N/A、来源分层或版本问题。

## 6. 单元图谱量表评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | 24.5 | 2/2 accepted 卡、5/5 子文本、31/31 KP、5/5任务和节点/任务 EV入口闭合；紧凑索引已声明展开规则，保守扣0.5。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | 19.0 | 4H+4L节点、8条关系包含共性、差异和迁移边界；单元级综合存在少量宽泛表达，保守扣1.0。 |
| 人文与语言双维度结构 | 15 | 12 | 15.0 | 4个人文节点、4个语言节点和交叉关系覆盖戏剧、诗歌、任务与读写活动。 |
| 单元任务拆解 | 15 | 12 | 15.0 | 5/5任务有原文定位、能力动作、KP回链、成果和评价证据。 |
| 高考衔接及证据 | 10 | 8 | 10.0 | M0 与未登记真题的不确定性边界明确，无越级映射。 |
| 前后递进 | 10 | 8 | 10.0 | 双方目标缺证时合法保持前序/后续 N/A，不强造递进。 |
| 可读性与检索性 | 5 | 4 | 5.0 | 上游清单、31项 KP 索引、任务/节点/关系表、M0、Issue 和覆盖复算齐全。 |
| **合计** | **100** | **88** | **98.5** | **总分及各维度均达标。** |

**主审决定：`pass`。** 当前 v0.2.0/SHA 可进入独立第二复审；本报告不写回 `accepted`，不得在二审前供 `BOOK-X2` 消费。

## 7. 可复现绑定

- 图谱 SHA：`10a30fbbf5af169e1651ff89ec0d9e49879cbe3a854c6058ceb4cf42d53f7d6f`。
- 上游 accepted 卡 post SHA：`63683985b71331d6dc3b31fefc7bd0680a19a9a32c9ca7a0193b6dd303b1421c`、`734847eaa30b6ddf3c8dff8540a1850ea98308692b1bb46a5020fbdc5ae80560`。
- ledger SHA：`53e8a978d4412977fc836f412cdf5599752d07a2d1b26d710e843455e40d94ba`。
- latest validator SHA：`e7347b4892e03ff0db18e044e4cad9479403f07e24c71d4bd873ddadc763eeca`；archive validator SHA：`e7347b4892e03ff0db18e044e4cad9479403f07e24c71d4bd873ddadc763eeca`。
- rubric SHA：`ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA：`13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
