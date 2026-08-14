# V2.4 执行与评估控制稿（候选）

> 用途：供协调者合入 `work/语文备课系统_知识点提取研究计划.md`。
>
> 状态：candidate；用户/协调者批准前不替代 V2.3，不直接改变任何交付账本状态。
>
> 不变项：`2.0-textbook` 的教材字段含义、受控词表、R01–R10、六类量表权重、单项门槛、总分门槛和状态枚举。

## 1. 本次改版要解决的问题

V2.4 不继续增加原则性描述，只解决五个执行歧义：

1. 静态方案与实时进度混写，导致同一文件出现多组过期计数；
2. 单件门禁与项目阶段门共用 G1/G2/G3 名称；
3. 卡片抽样二审与实际、通用写回门要求的全量双审冲突；
4. 分数可以给到 0.5，但当前粗检查点不能唯一复算；
5. 17 年真题目标仍混有“四卷”旧分母，且不应在 G-TB 前冻结。

## 2. 固定基线与动态快照分离

主计划只保存固定目标：

```text
教材锁定分母 = 81 张知识卡 + 28 份单元图谱 + 5 份册级总表 = 114 项
真题正式分母 = G-TB 后由 exam-contract 和 17 年 manifest 冻结
```

实时进度只认：

```text
work/knowledge/_meta/deliverables.jsonl
+ 最新 validator run_id
+ 本批 batch manifest 的 SHA-256
```

主计划不再硬编码“当前 accepted 数”和“下一单元”。每个批次开始生成一次快照，至少包含：

```yaml
batch_id: B2-U06-20260807
snapshot_at: ISO-8601
ledger_sha256: ...
validator_run_id: ...
contract_version: 2.0-textbook
rubric_sha256: ...
targets: [...]
upstream_versions_and_hashes: [...]
producer: ...
primary_reviewer: ...
secondary_reviewer: ...
coordinator: ...
```

`blocked` 只作为 batch/gate disposition，不写入当前 deliverable 状态枚举；受阻产物保持 `drafted` 或 `review_required` 并附 blocker。

## 3. 两套门禁采用不同命名空间

### 3.1 单件生命周期门（DG）

| 门 | 进入条件 | 必须产出 | 失败处理 |
|---|---|---|---|
| `DG0 SNAPSHOT` | 准备领取单件 | batch manifest、账本/契约/量表/上游 hash、角色分离 | 停止领取，先处理漂移 |
| `DG1 STRUCTURE` | 初稿完成 | Schema、必填字段、ID、路径、表格结构、枚举和 M0/N/A 结构通过；状态 `linted` | `rework`，不得评分 |
| `DG2 EVIDENCE` | DG1 通过 | 需证主张 100% 有适配证据；Q 类逐字目视核对 canonical PDF；I 类至少两处独立文本证据 | `rework` 或 batch blocker |
| `DG3 REVIEW` | DG2 通过 | 主审与第二复审针对同版本同 SHA；双方总分、单项、R01–R10、缺陷和分差门均通过 | `rework` 或 `adjudication` |
| `DG4 MERGE` | DG3 通过 | 协调者写回 ledger/transition，登记 review/hash，复跑 validator；账本显示 `accepted` | 不计进度，下游冻结 |

任一内容修改都会改变 SHA，并使旧 DG2/DG3 结论失效；修改后从 DG1 重走。评审 `pass` 只闭合 DG3，不自动闭合 DG4。

### 3.2 项目阶段门（SG）

| 门 | 目的 | 退出条件 |
|---|---|---|
| `SG-CAL` | 教材契约校准 | 已完成；`TEXTBOOK-CONTRACT-2.0-textbook` 有效 |
| `SG-UNIT` | 单元闭环 | 本单元全部卡 DG4 accepted；图谱再完成 DG0–DG4 |
| `SG-REC` | 诵读卡闭环 | 本册全部篇目/子文本覆盖，诵读卡 DG4 accepted |
| `SG-BOOK` | 册级闭环 | 全册图谱、诵读卡、前言上游锁定；册表 DG4 accepted |
| `SG-TB` | 教材锁定 | 81/81、28/28、5/5 accepted；教材来源链与变更记录齐全；生成 TEXTBOOK-LOCK |
| `SG-EXAM` | 真题契约与全量解构 | G-TB 后冻结 17 年 manifest/schema/rubric；17 年产物全部 accepted |
| `SG-MAP` | 真题—KP 映射 | 每小问有 M1/M2/M3 边或 M0；81 卡反查完成；映射表 accepted |
| `SG-REL` | 全局发布 | 全局地图 accepted；发布审计和一致性审计无阻断项 |

不得再单独写“通过 G2/G3”；必须写完整门名，如 `DG2 EVIDENCE` 或 `SG-CAL`。

## 4. 唯一允许的依赖顺序

```text
教材/课标来源治理
        ↓
教材契约 SG-CAL（已完成）
        ↓
卡 DG0→DG4 → 单元图 DG0→DG4
        ↓
本册诵读卡 SG-REC
        ↓
册级总表 SG-BOOK
        ↓
81卡 + 28图 + 5册表 → SG-TB / TEXTBOOK-LOCK
        ↓
真题来源治理 → 真题契约校准 → 17年全量解构 SG-EXAM
        ↓
真题—KP映射 SG-MAP
        ↓
全局知识地图与发布 SG-REL
```

教材卡、图谱或册表未全部锁定前，不存在通向正式真题处理的并行分支。

## 5. 评估标准

### 5.1 硬门优先

以下四层必须逐层通过，高分不能补偿前一层失败：

1. `R01–R10 = 0`；
2. 最终版本 `P0/P1/P2 = 0`；
3. 结构、证据、引用定位、ID/链接和上游合规硬指标通过；
4. 总分、单项和双审一致性通过。

外部依赖边界（例如 `edition_match=unknown`、G-TB 前无真题边）不是 P2。它必须作为 `constraint/dependency` 问题登记，并用允许的结构化 N/A 表达；不得与内容缺陷混记。

### 5.2 产物阈值（保持 2.0-textbook 不变）

| 产物 | 总分 | 单项最低分 | 二审覆盖 |
|---|---:|---|---:|
| 知识点卡 | ≥85；校准样板≥92 | 21/18/12/12/8/6/5 | 81/81 |
| 单元图谱 | ≥88；校准样板≥92 | 22/16/12/12/8/8/4 | 28/28 |
| 册级总表 | ≥90；首份 B1 册表试运行要求两审均≥92 | 23/17/13/13/8/9/4 | 5/5 |
| 真题解构 | provisional ≥90 | 18/23/20/12/9/4 | G-TB 后按 17 年 contract 全量 |
| 考点映射 | provisional ≥90 | 18/18/22/13/8/4/4 | 1/1 |
| 全局地图 | ≥92 | 23/18/13/13/9/8/4 | 1/1 |

教材 114 项全部采用最终版本全量主审和全量第二复审。V2.4 不再使用教材卡 25% 抽检规则；这样 DG3/DG4 对所有教材产物只有一条判定路径。

### 5.3 分数复算协议

冻结权重中的每个粗检查点必须展开为 `rubric_interpretation_version=2.0-textbook-observation-1` 的可观察子项：

```text
observation.result ∈ {pass, fail, N/A}
checkpoint_score = checkpoint_weight × passed_weight / applicable_weight
dimension_score = round_to_0.5(sum(checkpoint_score))
total_score = sum(dimension_score)
```

- 子项默认等权；如不等权，权重必须写入机器可读量表；
- `N/A` 只在 Schema 允许且理由、证据边界完整时剔除；
- 0/0 记为 `N/A`，不能伪记 100%；
- 评审者不得直接凭整体印象给 19.5、14.5 等结果；评分文件必须能从观察项重新计算；
- 已 accepted 的历史分数保留为历史审计记录，不静默重写；新协议生效后只对新版本/触发 `review_required` 的版本执行。

在观察项协议尚未冻结前，已领取的 U06-01 可以继续按现行完整量表人工双审；不得以这一个过渡例外扩展新批次。

### 5.4 指标分母

正式需证主张集合定义为正文正式结果区中所有非 N/A 的 `Q/F/I/M/R/E/D` 目标；唯一键为 `target_id + field_path`，KP、任务、图谱节点和关系使用其稳定 ID。仅在问题清单中的未核实线索不进入正式分母。

```text
需证主张覆盖率 = 有适配且 verified 证据的正式 Claim 数 / 正式 Claim 总数
I 类双证据率   = 至少有两处相互独立文本证据的 I Claim 数 / I Claim 总数
Q 引文准确率   = canonical PDF 逐字命中的 Q Evidence 数 / Q Evidence 总数
定位有效率     = 能在 canonical artifact 两分钟复核的 Evidence 数 / Evidence 总数
引用解析率     = 能解析到存在目标的 ID/路径数 / ID/路径引用总数
上游合规率     = 仅消费 accepted 且 hash 匹配上游的下游数 / 本批下游总数
```

前五项对适用分母要求 100%；无适用对象时写 `N/A + reason`，不得用 0/0=100%。

### 5.5 双审一致性

每份教材核心产物必须同时满足：

- 生产者、主审、第二复审三角色分离；
- 两审针对同一 version、artifact SHA 和 rubric SHA；
- 两位评审各自达到总分与全部单项门槛；
- 两审决定一致，R01–R10 判断一致；
- 总分差 ≤5，任一单维度差 ≤2；
- 超阈值或否决判断冲突进入独立仲裁，不能直接平均通过。

最终显示分数为两审算术平均值；是否 accepted 仍由硬门和 DG4 决定，不由平均分单独决定。

### 5.6 缺陷与扩审

| 事件 | 动作 |
|---|---|
| 第二复审发现 P0 | 立即冻结本单元下游；审计同生产者在本 batch 的全部产物；修订后完整重审 |
| 第二复审发现 P1 | 本件返工；保留首次检出记录；本批 P1 逃逸率 >10% 时暂停扩批并做原因复盘 |
| 发现 P2 | 修订并复核；P2 清零前不得 DG4 |
| 同件第二次不通过 | 全件重做并复审相关上游链接 |
| 同件第三次不通过 | 更换生产者，回到相同 material_type 样板重新校准 |

`P0/P1 escape rate` 使用第二复审首次检出记录计算，不能被修订后的 0 覆盖。它是过程改进指标；最终版本仍必须 P0/P1/P2=0。

## 6. 批次绿灯

一批只有同时满足以下条件才是 `green`：

- batch manifest 完整，输入/上游/契约/量表 hash 可复核；
- 本批目标均完成 DG0–DG4，或在领取前已明确排除；
- validator errors=0；每条 warning 有 owner、影响、处置与关闭条件；
- 适用的结构、证据、引文、定位、ID/链接和上游合规率均为 100%；
- 两审同 SHA、分差合规，最终 P0/P1/P2=0；
- ledger 状态、文件 front matter、transition 记录和批次报告一致；
- 保存分子/分母、评分观察项、问题单、修改记录、SHA、validator run 和影响清单。

平均分高、完成文件多或 validator 单独通过均不能替代上述条件。

## 7. 角色与并行规则

采用 hybrid 模式：

- 同一文件、共享 registry、DG4 写回严格串行；
- 不同单元的证据整理可并行；
- 每个单元内严格“全部卡 accepted → 才写图谱”；
- 每位执行者同时只拥有一个生产文件；
- 主审/二审可流水并行，但不得在同一未锁 SHA 上评审；
- 协调者独占 `deliverables.jsonl`、transition、batch manifest 和最终 validator 复跑。

教材阶段 WIP 上限为 2 个单元；只有连续两批 green 且第二复审 P0=0、P1 escape rate≤10%，才允许临时提高到 3 个单元。

## 8. 后续执行波次

以下顺序以 2026-08-07 19:28 快照（31/81 卡、13/28 图、0/5 册表）为起点；真实领取仍以新 batch snapshot 为准。

### Wave 0：控制面准备

- 统一 DG/SG 名称；
- 生成 batch manifest 模板；
- 冻结评分观察项协议；
- 修正动态进度与旧队列；
- 将 validator 能力表拆为已自动化/人工必检/V3 待补。

### Wave 1：尽早验证册级汇总

- Lane A：`CARD-B1-REC-01` → DG4 → `BOOK-B1` 首份册表试运行；
- Lane B：B2 U06 三张卡 → DG4 → `UNIT-B2-U06`；
- `BOOK-B1` 两审均要求 ≥92，用于暴露册级去重、递进、前言和诵读汇总风险。

### Wave 2：闭合必修下册

- B2 U07 一张卡及图谱；
- B2 U08 两张卡及图谱；
- `CARD-B2-REC-01`；
- `BOOK-B2`。

### Wave 3：选择性必修上册

- 按 4 个单元逐单元垂直闭环；
- 诵读卡；
- `BOOK-X1`。

### Wave 4：选择性必修中、下册

- X2、X3 各一次只在制一个单元，可跨册形成 WIP=2；
- 每册完成 4 图 + 诵读卡后分别生成 `BOOK-X2/BOOK-X3`。

### Wave 5：教材总审计与锁定

- 81/81 卡、28/28 图、5/5 册表账本验收；
- 144 包来源链、课标版本、TB2 unknown 边界、hash、review、transition 全审计；
- 下游影响清单清零；
- 生成 `TEXTBOOK-LOCK-2.0-textbook`，通过 `SG-TB`。

### Wave 6：另建真题契约

G-TB 后才执行：

1. 17 年原卷/解析卷/答案与权威边界登记；
2. 冻结 17 年 deliverable manifest，废止“四卷”旧分母；
3. 2013/2016/2024 端到端校准；
4. 2008/2011/2018/2021 结构校准和留出测试；
5. 全量 17 年解构；
6. 真题—KP 映射、全局地图与发布审计。

## 9. 启动前最终检查

- [ ] 用户/协调者批准 V2.4 候选控制稿；
- [ ] 主计划不再保存会过期的实时 accepted 数；
- [ ] DG 与 SG 无重名；
- [ ] 依赖图包含 SG-TB 且无真题前置旁路；
- [ ] 教材卡二审覆盖明确为 81/81；
- [ ] 评分观察项可机器复算；
- [ ] batch manifest 能锁定目标/上游/量表/validator hash；
- [ ] 当前 warning 均有处置记录；
- [ ] `CARD-B1-REC-01` 与 B2 U06 有独立 owner，未发生同文件并写；
- [ ] 高考相关任务保持 `blocked_by_textbook`。

