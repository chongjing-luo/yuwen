# V2.4 教材执行与评估解释冻结候选

- 候选版本：`2.0-textbook-eval-1`
- 生成时间：2026-08-08 01:43 +08:00
- 最近修订：2026-08-08 13:18 +08:00（冻结 C 层 Gold一致性、KP匹配、聚类 bootstrap 与查询计时口径）
- 状态：`candidate / not-active`
- 适用范围：教材侧 81 张知识卡、28 份单元图谱、5 份册级总表
- 不适用范围：试卷解构、真题—KP 映射和全局地图；这些量表在 `SG-EXAM-CAL` 前保持 `provisional`
- 当前执行规则：本候选完成切换清单前，继续使用已冻结的 `2.0-textbook`，不得把本文件局部规则混入在制件

本候选合并三份 V2.4 草稿并闭合四个阻断：合法 N/A 的可比较计分、DG3/DG4 的 SHA 生命周期、评审绑定 Schema、validator 的语义能力边界。它不改变教材 Schema、受控词表、R01—R10、三类教材量表权重、正式总分门槛或单项门槛。

## 1. 权威层级与动态状态

批准后的权威顺序固定为：

1. `work/语文备课系统_知识点提取研究计划.md` V2.4：唯一人读规范；
2. `TEXTBOOK-CONTRACT-2.0-textbook`：教材字段、词表、状态机和基础量表的历史冻结；
3. `2.0-textbook-eval-1`：本文件定义的评价解释层及其机器文件 SHA；
4. `deliverables.jsonl + 最新 validator run_id + batch manifest SHA`：唯一实时状态；
5. review package 与 DG4 receipt：单件判定证据。

固定教材分母只有：

```text
81 张知识卡 + 28 份单元图谱 + 5 份册级总表 = 114 项
```

主计划不得保存当前 accepted 数、下一单元、owner 或短期波次。实时数量、目标和角色只写入带时间戳的 batch manifest 与实施日志。

## 2. 唯一依赖路径

```text
SG-CAL（教材基础契约，历史已完成）
  ↓
SG-EVAL（评价解释层与控制包切换）
  ↓
知识卡 DG0→DG4
  ↓
SG-UNIT：本单元全部卡 accepted
  ↓
单元图谱 DG0→DG4
  ↓
SG-REC：本册诵读卡 accepted
  ↓
SG-BOOK：册级总表 DG0→DG4
  ↓
SG-METHOD：方法有效性与教学查询验证
  ↓
SG-TB / TEXTBOOK-LOCK
  ↓
SG-EXAM-CAL：17 年 manifest/schema/rubric 校准与冻结
  ↓
SG-EXAM → SG-MAP → SG-REL
```

`SG-EXAM-CAL` 与 `SG-EXAM` 必须分开：前者冻结试卷来源、17 年分母和评价契约，后者才执行全量解构。`SG-TB` 前不存在正式试卷处理旁路。

## 3. 单件 DG0—DG4

| 门 | 输入 | 通过证据 | 失败处理 |
|---|---|---|---|
| `DG0 SNAPSHOT` | 待领取目标 | batch manifest 锁定 ledger、契约、量表、目标、上游、角色和 SHA；三角色分离 | 停止领取，先处理漂移 |
| `DG1 STRUCTURE` | 初稿或返修稿 | 基础 validator 已实现检查通过；人工 semantic lint 对 Markdown 表、枚举、ID、M0/N/A、版本和占位符全检；状态为 `linted` | `rework`，不得评分 |
| `DG2 EVIDENCE` | DG1 通过版本 | Claim 分母冻结；适用证据指标 100%；Q quote span 逐字目视核对；I Claim 至少两个独立文本依据；合法 N/A/constraint 完整 | `rework` 或 batch blocker |
| `DG3 REVIEW` | DG2 通过版本 | 主审与二审独立封存并绑定同一 content/claim/rubric/observation/upstream SHA；双方分别过门；分差合规 | `rework` 或 `adjudication` |
| `DG4 MERGE` | DG3 通过 | 协调者独占写回；保存 pre/post file SHA、稳定 content SHA、白名单差异、ledger/transition、review refs、validator 和影响清单 | 不计进度，下游冻结 |

内容改变后必须回到 DG1。评审 `pass` 只闭合 DG3；只有 ledger 为 `accepted` 且 DG4 receipt 完整，产物才可被下游消费。

## 4. 三层评价

| 层 | 判断对象 | 结论用途 |
|---|---|---|
| A. 合格性硬门 | Schema、来源、Claim—Evidence、Q 引文、I 双证、ID/链接、上游、R/P、SHA | 任一失败即不得产生正式分数或 pass |
| B. 产物质量分 | 已通过 A 层的当前版本 | 使用冻结权重、单项门槛与机器观察项复算 |
| C. 方法与过程有效性 | 批次和整个提取方法 | 双审一致性、缺陷逃逸、封存评估集、教学查询；失败会暂停扩批，不自动改写单件历史分 |

三层不得混算。A 层失败时可保留诊断性分数，但正式总分写 `N/A`。

## 5. 教材正式门槛

| 产物 | 正式总分 | 七维最低分 | 双审覆盖 |
|---|---:|---|---:|
| 知识点卡 | ≥85 | `21/18/12/12/8/6/5` | 81/81 |
| 单元图谱 | ≥88 | `22/16/12/12/8/8/4` | 28/28 |
| 册级总表 | ≥90 | `23/17/13/13/8/9/4` | 5/5 |

- 校准样板和明确标记的首件试运行：两审分别 ≥92。
- 交主审前可使用 ≥92 作为内部工作目标，但不得把它改写成正式验收门槛。
- R01—R10 必须全部为否；最终 P0/P1/P2 必须为 `0/0/0`。
- 两位评审各自达到总分和全部单项；总分差 ≤5，任一单维差 ≤2。
- 两审结论、R 判断、Claim 分母或 N/A 分母不一致时进入独立仲裁，不能取平均通过。
- 最终展示分可为两审算术平均值并保留 0.25；accepted 判定始终使用两审各自门槛，不使用平均分过门。

## 6. 可复算计分

```text
覆盖型检查点得分 = checkpoint_weight × pass_count / applicable_count
判断型检查点得分 = checkpoint_weight × 通过子项权重 / 适用子项权重
维度得分         = ROUND_HALF_UP(检查点得分之和, 0.5)
总分             = 七个维度得分之和，不二次取整
```

- 计分器使用十进制定点运算，不使用二进制浮点近似。
- 子观察项默认等权；非等权必须在评审前写入带 SHA 的 observation manifest。
- 每项保存 `scope_query / applicable_count / pass_count / failed_ids / evidence_refs / defect_ids`。
- 评审后不得删除 Claim、观察项或失败 ID 来缩小分母。

## 7. Claim、证据与 N/A

### 7.1 正式 Claim 分母

每个正式主张使用 `claim_id + target_id + field_path` 唯一标识。正文正式结果区所有非 N/A 的 Q/F/I/M/R/E/D 目标均进入分母；问题清单、模板说明、自检和版本记录不进入。Claim 注册表封存 SHA 后才进入 DG2。

适用指标均要求 100%：

```text
正式主张覆盖率
I 类独立双证率
Q quote span 准确率
Locator 有效率
目标绑定率
来源适配率
合法 N/A 率
```

`0/0` 只能报告 `N/A + reason`，不得报告 100%。`missing_required` 不是 N/A，直接判 DG2 失败。

### 7.2 允许的 N/A

只允许：`not_applicable / permitted_unavailable / future_locked / no_reliable_relation`。每项必须登记字段、核查范围、理由、依赖边界和两审一致判断。

### 7.3 无边治理替代观察项

合法无关系时只剔除“关系事实”分母，不剔除整个质量维度。对应权重切换到等值治理观察项，维度仍按 100 分制和原单项门槛比较。

知识点卡“纵向贯通”8 分在无边时使用：

| 替代观察项 | 分值 |
|---|---:|
| 已登记候选目标与核查范围 | 2 |
| 已说明不存在可靠关系的文本/状态理由 | 2 |
| 源 KP、关系、目标、双方证据均使用结构化 N/A | 2 |
| 未强造关系且依赖边界、重开条件明确 | 2 |

单元图谱“前序/后续”各 5 分在对应方向无边时使用：候选范围 2、无边理由 1、结构化 N/A 1、不强造及重开条件 1。册级总表拥有多个已验收单元时，跨单元递进不是可整体 N/A 项。

`SG-TB` 前 M0 的冻结结构为：

```text
等级 = M0
边界说明 = 必填
KP-ID / 真题小问 / 能力动作 / 真题证据 / 教材证据 = N/A
```

其质量按“锁定状态正确、必填字段 N/A、边界理由清楚、未伪造实边”评分；不能因不存在真题实边把高考维度整体删除，也不能携带 KP 范围或潜在题型。

## 8. 独立双审与缺陷逃逸

1. 生产者、主审、二审三角色分离；两审在各自封存前不得读取对方原始记录。
2. 两审绑定同一 artifact version、`content_sha256`、Claim SHA、rubric SHA、observation SHA 和 upstream snapshot SHA。
3. 内容返修产生新 content SHA 后，两审完整重走；旧评审仅留作审计。
4. 批次观察项一致率目标 ≥90%。
5. P0 逃逸率必须为 0；任一 P0 立即冻结受影响下游并审计同源链。
6. P1 逃逸率 ≤10%；超过即暂停扩批并全批复核。
7. P2 逃逸率 ≤20%；超过则下一批前重校准边界与措辞样例。
8. 修订后的 `P0/P1/P2=0` 不得覆盖首次检出记录。

## 9. content SHA、pre/post SHA 与 DG4 白名单

### 9.1 三种哈希

- `pre_merge_file_sha256`：DG3 被评文件的完整字节 SHA；两审必须相同。
- `content_sha256`：排除生命周期元数据后的规范化语义内容 SHA；DG3 与 DG4 前后必须不变。
- `post_merge_file_sha256`：DG4 状态同步后的完整字节 SHA。

### 9.2 content SHA 规范化

新模板必须把生命周期正文放入唯一标记区：

```html
<!-- lifecycle-metadata:start -->
...仅含评审状态、自检状态同步和评审引用...
<!-- lifecycle-metadata:end -->
```

计算步骤冻结为：

1. UTF-8 解码，换行统一为 LF；
2. 解析 YAML front matter，移除且只移除 `status`、`reviewers`；`version`、来源、题名和其它字段保留；
3. 移除唯一 lifecycle-metadata 区块；不存在或出现多个区块即失败；
4. YAML 采用键名排序的 canonical JSON 表达；Markdown 正文不折叠空白、不改标点；
5. `SHA-256(canonical_front_matter + "\n---\n" + body_without_lifecycle_block)`。

### 9.3 DG4 允许差异

DG4 只允许：front matter 的 `status/reviewers`、标记区内的状态同步、外部 ledger/transition/review refs。不得修改正文正式主张、KP、EV、Source、Artifact、locator、引文、分数、version 或版本史。

DG4 receipt 必须保存 pre/post SHA、content SHA、白名单 diff、两份 review SHA、transition ID、validator run 和影响清单。content SHA 变化或出现非白名单 diff 时，DG4 失败并回到 DG1。

现有未使用 lifecycle 标记的在制件继续走 `2.0-textbook` 旧流程，不得局部套用本算法；本规则只从明确 cutover batch 前向生效。

## 10. Review binding companion

现有 `review.schema.json` 不含 artifact/rubric/claim/batch/upstream SHA 且 `additionalProperties=false`。本候选不静默修改它，而是新增伴随绑定清单：

`review_binding_manifest_schema_candidate_20260808_014300.json`

每个 DG3 包必须由该清单绑定：目标版本、content/pre-merge SHA、contract/rubric/observation/claim/upstream/batch SHA、validator run、两份 review 文件及其 SHA、两审分数/R/P/决定。DG4 后再补 post-merge SHA 与 receipt 路径。

若未来把这些字段并入 `review.schema.json`，必须升级到新 contract 版本并做 G2/SG-EVAL 影响评估。

## 11. Validator 能力边界

当前基础 validator 自动检查：受控任务群与状态枚举、量表类型/权重/门槛、120 项账本恒等式、Source/Artifact/上游 ID 存在性、144 源包与 split manifest 恒等式、canonical Artifact/文件大小/SHA、Schema/模板存在性、非 planned 输出文件存在性。

当前基础 validator 不检查：

- 卡/图/册表 Markdown 是否符合实例 Schema；
- front matter 与 ledger 版本/状态是否一致；
- 证据表列数、Claim/KP/EV/任务、Q 引文逐字准确性、I 双证据；
- locator 是否落在切分 PDF 实际页范围；
- M0/N/A、教材提示/教师用书/项目建议的语义边界；
- review 同 SHA、角色独立、R/P、分数复算、DG4 白名单与状态迁移闭环。

因此 `validator passed` 只能闭合其已实现检查，不能单独闭合 DG1 或 DG2。未自动化项必须进入版本化 semantic lint；能力矩阵按“自动 / 人工必检 / 待自动化”三列维护。

## 12. 批次绿灯与 WIP

批次 `green` 必须同时满足：manifest 完整、目标全部 DG0—DG4、自动检查 errors=0、warning 有 owner/影响/处置/关闭条件、适用硬指标 100%、两审同绑定且分差合规、P0/P1/P2 清零、ledger/front matter/transition/DG4 receipt 一致。

教材默认 WIP=2 个单元；只有连续两批 green、P0 逃逸为 0、P1 逃逸率 ≤10%，才允许临时提高到 3。共享 registry、同一文件和 DG4 始终串行单写。

## 13. 方法有效性

C 层至少包括：

- 从尚未重建的 X2/X3 材料中，在生产任务发出前封存 12 张分层评估卡、4 个单元图和 1 份尚未生成的册表；记录既有 generic 草稿造成的污染风险，不把它宣称为完全盲测；
- 关键事实/强制任务召回率 100%，KP precision/recall/F1 均 ≥90%，标签 macro-F1 ≥85%，Claim—Evidence 与 Q/locator 准确率 100%，关系边精确率 ≥90%，未支持正式主张率 0%；
- Gold 必须由两名盲于生产输出的标注者独立生成并在封存后仲裁；仲裁前分类标签 `Krippendorff's alpha ≥0.80`、KP 集合配对 F1≥0.85，否则修订手册后重标。KP 在单卡内按核心命题、对象/动作、范围和证据边界做一对一最优匹配；重复输出计假阳性，过宽/过窄/无证扩展不计命中。
- 95% 区间按“册码 × material_type”分层，以交付物为聚类单位、使用预登记种子做 10,000 次 bootstrap；不把同卡 KP 视为独立样本。单份册表只做完整个案过门，不伪造置信区间。关系边召回率/F1 只做诊断，不以边数量驱动强造关系。
- 12 个固定教学查询，任务完成率 ≥90%，核心事实与证据准确率 100%。计时从独立评估者看到冻结查询开始，到打开 canonical Artifact 目标页并完成核对为止；至少11/12问在120秒内完成，并报告中位数/P90。最终门至少需要3名未参与生产/评审的语文教师或等价专家，可用性中位数 ≥4/5，且无教学事实严重错误意见；只有2人时仅能记 pilot。

当前 81 张卡文件已全部存在，不能把其中任意集合无条件称为“真正前瞻盲留出集”。真正盲测需等待未暴露的新来源或新契约；本阶段只称“封存评估集”，并公开污染边界。

## 14. 既有 accepted 产物

本候选批准后只前向适用于 cutover batch。既有 accepted 产物不重写历史分数；在 `SG-TB` 前做一次只读 Claim/证据回填审计。回填通过只附证据包；发现 A 层硬门失败时由协调者转为 `review_required` 并重走 DG1—DG4。

## 15. 冻结条件

只有 `evaluation_cutover_checklist_20260808_014300.md` 全部必需项通过并由协调者记录 cutover batch 后，本候选才从 `candidate` 变为 `frozen/active`。此前当前教材执行继续按现有 `2.0-textbook`，高考仍为 `blocked_by_textbook`。
