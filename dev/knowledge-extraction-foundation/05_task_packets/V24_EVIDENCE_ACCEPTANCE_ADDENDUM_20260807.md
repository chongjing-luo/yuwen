# V2.4 证据验收协议（候选附录）

> 用途：供协调者合入 V2.4 执行与评估方案；在批准前不改变 `2.0-textbook` 契约、账本状态或既有 `accepted` 成果。
>
> 目标：让“证据覆盖率 100%”具有冻结分母、可复算日志和明确失败条件，避免只按 EV 数量或评审印象判定。

本协议批准后前向适用于新领取或进入 `review_required` 的成果，不静默重写既有 `accepted` 分数。为使 SG-TB 的全项目证据指标仍可复算，既有 `accepted` 成果须在教材锁定前完成一次只读证据包回填审计：通过则附加 Claim/证据清单而不改正文和历史评分；发现硬门失败则由协调者转入 `review_required`，按新协议重走 DG1—DG4。

## 1. 核心判定

1. 不存在“未列主张清单的 100% 覆盖率”。生产者必须先冻结正式主张分母，再进入证据核验。
2. 证据覆盖按 `Claim` 计，不按 EV 数量、正文段数或文件大小计；一条 EV 可以支撑多个目标，但必须逐目标记录绑定关系。
3. Q 类准确率按“引文片段”计，不按证据行计。一行包含三段直接引文时，分母为三，不是一。
4. I 类“双证据”要求两个独立文本依据，不等于两个 EV 编号；把同一段落机械拆成两条 EV 不构成独立证据。
5. `N/A` 只能表达允许的不适用或外部边界，不能代替缺失的必需证据。
6. 分数只在证据硬门通过后计算；任何证据硬门失败均不得用其它维度高分抵消。

Claim 以“可独立判断真伪或成立与否的最小命题”为单位。一个单元格同时写作者、体裁、节选范围和翻译信息时，至少拆成四条 Claim；不能用其中一项有证据把整个复合单元格记为已覆盖。

## 2. 正式主张清单与冻结分母

每个交付物在 DG2 前生成一份 `claim_register`。当前冻结 Schema 不增字段时，可作为批次证据包中的伴随清单保存；每条至少包含：

```yaml
claim_id: CLM-<deliverable>-NNN
target_id: <CARD/KP/TASK/REL/NODE 等稳定 ID>
field_path: <模板语义路径，不使用 Markdown 行号>
claim_type: Q|F|I|M|R|E|D
claim_text: <被验收的完整主张>
formal: true
required_evidence_rule: <规则代码>
evidence_ids: []
disposition: asserted|N/A
na_kind: null
na_reason: null
```

`field_path` 使用模板语义路径，例如 `human_dimension.motif`、`knowledge_points[KP-...].statement`、`curriculum.primary_task_group`；不得使用会随排版变化的行号。

正式分母至少覆盖：

- 需证的 front matter 字段，包括题名/作者边界、主任务群、QD、Source；
- 人文维度、语言维度和课标对接中的正式结论；
- 每个 KP 陈述、四层归属及映射理由；
- 每个 TASK、图谱节点、关系边、纵向关系和高考关系；
- 教材学习提示、教师用书意见及所有被写成事实或权威意见的教学主张；
- 册表、真题和映射中的统计或派生结论。

问题清单中的未核实线索、模板说明、自检文字和版本记录不进入正式主张分母。边界声明进入 `constraint_register`，不与 Q/F/I/M/R/E/D 主张混算。

生产者冻结 `claim_register_sha256` 后，评审者才开始核验。评审中如发现漏列主张，必须扩充分母并重新计算；不得通过删除 Claim 缩小分母。任何正文内容修改都会改变交付物 SHA，并使旧 Claim 清单和旧 DG2/DG3 结论失效。

## 3. 合格证据链

一条 Claim 只有同时满足以下条件才算“已覆盖”：

1. `target_id + field_path` 能解析到当前交付物中的唯一目标；
2. EV、Source、Artifact 均已登记且 ID 可解析；
3. Artifact 的真实性状态、canonical 状态和 SHA 与 batch snapshot 一致；
4. Locator 类型与载体匹配，页码在 Artifact 范围内，切分页与原 PDF 页可按 manifest 复算；
5. `support_relation=supports`，证据内容确实支持完整 Claim，而非只与主题相关；
6. Claim 类型与来源适配；
7. 核验状态、核验人和日期齐全；
8. 当前 Claim 要求的专门规则全部满足。

专门规则：

| Claim 类型 | 合格条件 |
|---|---|
| Q | 每个引文片段均逐字回看 canonical PDF；省略、跨页和多片段分别记录范围，解释性转述不冒充 exact quote |
| F | S1 为优先；教材未载的作者、年代、术语等事实补 S2；来源只与主题相关不算支持 |
| I | 至少两个独立文本依据并写出推理桥；外部评论不能替代文本依据 |
| M | 同时具有官方框架定义和本课/本任务证据；纵向关系另须两端均 `accepted` 且有递进理由 |
| R | 教师用书意见须有已确认配套关系；本项目建议须显式标注，并回链到已验收 KP/任务，不冒充教材意见 |
| E | SG-TB 前只允许结构化 M0；解锁后 M1/M2 必须回链真题小问与教材 KP 双方证据 |
| D | 输入 ID、口径、公式/算法、工具版本和结果均可复算 |

I 类证据的“独立”按文本依据判断：两个依据须对应不同事实节点、叙事环节、语言现象或子文本，并分别承担推理中的不同前提。同一语句的 OCR、PDF 和截图是同一依据；同一段落换两个 EV 编号仍只计一份。

Q 类“逐字一致”默认要求字形、用字和标点与规范页面一致；仅允许忽略由版面造成的换行与字间空白。任何异体字替换、标点改写、补字、删字或跨段拼接都必须显式分成 quote span 并标出省略，不能静默规范化。

## 4. N/A 与外部边界

允许的 `na_kind` 仅有：

- `not_applicable`：该字段对本材料真正不适用；
- `permitted_unavailable`：Schema 允许缺源，例如未取得同册教师用书；
- `future_locked`：依赖尚未解锁，例如 SG-TB 前的真题映射；
- `no_reliable_relation`：已核查但不存在可靠关系边，例如当前纵向关系或 M0。

`missing_required` 不是 N/A，必须判 DG2 失败。每个 N/A 都须记录字段、类型、理由、依赖/核查范围和两位评审的一致判断。合法 N/A 从对应证据分母剔除；`0/0` 报 `N/A + reason`，不得报 100%。

`edition_match=unknown` 是来源治理约束：不得消费 TB2 内容，也不得写成当前学生教材编者意图。M0 是“当前无可靠映射”的显式记录，不携带 KP 边，不表示“不考”。

## 5. 可复算证据指标

```text
正式主张覆盖率 = 具有完整合格证据链的 asserted Claim 数 / asserted Claim 总数
I 类独立双证率 = 具有至少两个独立文本依据的 I Claim 数 / I Claim 总数
Q 引文片段准确率 = canonical PDF 逐字匹配的 quote span 数 / quote span 总数
Locator 有效率 = 可在锁定 Artifact 上复核的 locator 数 / locator 总数
目标绑定率 = 可唯一解析 target_id + field_path 的证据绑定数 / 证据绑定总数
来源适配率 = 满足对应 Claim 类型来源规则的 Claim 数 / asserted Claim 总数
合法 N/A 率 = 通过允许类型与理由核查的 N/A 数 / N/A 总数
```

所有适用指标均须达到 100%。报告必须保存分子、分母、异常 ID 清单、计算时间、交付物 SHA、Claim 清单 SHA、Source/Artifact snapshot SHA 和 validator `run_id`。EV 数量、平均每 KP 的证据数和正文长度只作描述信息，不作为绩效指标，避免用堆证据替代证据适配。

## 6. 三角色核验

- 生产者：建立 Claim 清单、证据绑定和 100% 自检日志；不得担任两位内容评审。
- 主审：独立重算正式分母，逐条核验所有 Claim、Locator、Q quote span 和 I 双证据，并完成全量评分。
- 第二复审：针对同一版本、交付物 SHA、Claim 清单 SHA 和量表 SHA 再次完整核验；不得只复述主审结论。
- 协调者：只在双审同 SHA、证据指标 100%、R01–R10=0、P0/P1/P2=0 后执行 DG4 写回。

评审记录必须保存在交付物之外，避免把评审签名写回正文后改变被审 SHA。任何内容修订均回到 DG1；旧评审保留为审计记录，不能继续支撑新 SHA。

## 7. 失败、扩审与传播

以下任一项直接判 DG2 失败并触发相应 R 代码：错引/伪引、Locator 不可复核、正式 Claim 无适配证据、I 类不足两个独立文本依据、来源等级或教师用书边界冒充、未验收上游被消费。

- P0：冻结所有已消费该上游 SHA 的下游，生成影响清单；修复后完整重审。
- P1：本件返工；同批逃逸率超过阈值时暂停扩批并全批复核。
- P2：修正并复核；清零前不得 DG4。
- 主审和二审的证据分母、Q span 数或 I 独立性判断不一致：进入 adjudication，不得取平均。

## 8. DG4 最小证据包

每个按本协议新进入 `accepted` 的交付物必须能从同一目录或 manifest 找到：

1. batch snapshot；
2. 交付物版本与 SHA；
3. `claim_register` 及其 SHA；
4. Claim—EV—Source—Artifact 绑定清单；
5. Q quote span 目视核验日志和 I 类独立性核验表；
6. 两份独立评分/证据复核记录及量表 SHA；
7. 问题单、修改记录和缺陷关闭记录；
8. validator 报告；
9. ledger/transition 写回记录和下游影响清单。

缺少任一必需件时，评审 `pass` 最多闭合 DG3，不能进入 DG4。

既有 `accepted` 成果可保留原评审格式，但在 SG-TB 前必须具有等价的只读 Claim 分母、证据绑定、核验结果和哈希记录；“历史已通过”不能替代教材锁定时的全量证据可复算性。

## 9. 扩批前准备清单

- [ ] 冻结 `claim_register` 模板和字段语义；
- [ ] 冻结允许的 N/A 矩阵及 `na_kind`；
- [ ] 将 Q 类分母从“证据行”改为“quote span”；
- [ ] 为 I 类独立性给出正例、反例各至少两个；
- [ ] 评审模板增加 deliverable/Claim/rubric 三个 SHA；
- [ ] validator 能力表明确“自动检查、人工全检、V3 待补”三列；
- [ ] 以一张双文本卡和一张特殊内容卡做证据协议试运行；
- [ ] 两个试运行件均能由第三人仅凭证据包复算出相同分母和结论后，再扩大 WIP。
