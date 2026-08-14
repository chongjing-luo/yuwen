# `2.0-textbook-eval-1` 切换执行清单

- 对应候选：`evaluation_freeze_candidate_20260808_014300.md`
- 状态：`pending`
- 原则：控制面完整切换；不得把候选规则局部套入当前在制件

## A. 规范与审批

- [x] 单一候选文件已统一 DG/SG、A/B/C 三层评价、教材正式门槛和全量双审。
- [x] 已移除候选中的动态 accepted 数、当前 owner、旧队列和 U06 过渡例外。
- [x] 已把试卷契约冻结与全量解构拆为 `SG-EXAM-CAL / SG-EXAM`。
- [ ] 协调者批准候选内容与前向生效边界。
- [x] 主计划升级为 V2.4，并删除旧 G 名称、25% 卡片二审、静态进度和试卷前置旁路。
- [x] `PROJECT_INDEX.md` 已登记 `04-evaluation-freeze / 04-evaluation-cutover`，重置 V2.4 批准状态，并将旧行动计划/清单标为 pre-cutover legacy。
- [ ] 批准后在 `PROJECT_INDEX.md` 记录全部机器文件 SHA 和 cutover batch，并将三份 V2.4 任务包草稿标为 superseded/source draft。

## B. SHA 生命周期

- [x] 候选已定义 `content_sha256 / pre_merge_file_sha256 / post_merge_file_sha256`。
- [x] 候选已定义 DG4 白名单和 content SHA 不变规则。
- [x] 新模板加入且只加入一个 `lifecycle-metadata` 标记区。
- [x] 实现确定性 content SHA 计算器，并提供 LF/CRLF、YAML 键序、状态/评审者变化、正文变化的回归夹具。
- [x] 负例证明正文、KP、EV、引文、version 或版本史改变会使 content SHA 改变并拒绝 DG4。
- [x] DG4 receipt Schema/模板可记录 pre/post/content SHA、白名单 diff、review SHA、transition 和 validator。

## C. Review binding

- [x] 已新增候选伴随 Schema：`review_binding_manifest_schema_candidate_20260808_014300.json`。
- [x] 使用 JSON Schema validator 验证正例和缺字段/错 SHA/角色重合/决定冲突负例。
- [x] 更新 review 模板，正文评分与 binding manifest 分离；不向现有 `review.schema.json` 静默加字段。
- [ ] 主审、二审在互不可见条件下分别封存，binding 能证明同 content/claim/rubric/observation/upstream SHA。
- [x] 仲裁模板明确只在两份原始评审封存后启用。

## D. Claim、N/A 与观察项

- [x] 候选已冻结允许的四类 N/A、`missing_required` 失败规则和 0/0 报告方式。
- [x] 知识点卡纵向 8 分、图谱前序/后续及 G-TB 前 M0 已定义替代观察项。
- [x] 创建 `claim_register.schema.json`、`constraint_register.schema.json` 和正反例。
- [x] 创建 `rubric_observations_2.0-textbook-eval-1.json`，覆盖卡/图/册表全部检查点及替代观察项。
- [x] 实现十进制定点、`ROUND_HALF_UP` 到 0.5 的复算器；两位评审能由同一观察输入复算相同分数。
- [ ] 负例覆盖非法 N/A、整维剔除、M0 携带 KP/小问/动作/证据、删 Claim 缩分母。

## E. Validator 能力与 semantic lint

- [x] 候选明确基础 validator 的自动覆盖和语义盲区。
- [x] 创建版本化 validator capability matrix，逐项标明自动/人工必检/待自动化。
- [x] 创建 semantic lint Schema/模板，至少覆盖 Markdown 表列、front matter/ledger 一致、Claim/KP/EV、Q/I、locator 范围、M0/N/A 和三类教学提示。
- [x] batch 报告分别列自动检查与人工检查，禁止把人工项写成 validator 已通过。
- [x] warning register 具有 owner、影响、动作和关闭条件。

## F. 试运行与 cutover

- [ ] 用一张双文本卡、一张特殊内容卡和一份单元图做完整 DG0—DG4 试运行。
- [ ] 第三人仅凭 review package 能复算 Claim 分母、七维分数、双审结论和 DG4 白名单。
- [ ] 连续两个试运行 batch 为 green；P0 逃逸=0，P1≤10%，观察项一致率≥90%。
- [ ] 协调者记录唯一 `cutover_batch_id`、旧/新规则边界和在制件处置；cutover 前领取件继续旧规则，cutover 后领取件完整使用新规则。
- [ ] `SG-EVAL` 记录含候选文件、所有机器文件和回归报告 SHA；随后才标记 `frozen/active`。
- [ ] 高考相关任务继续 `blocked_by_textbook`；试卷、映射和全局量表继续 provisional。

## G. 当前判定

当前为 `not ready to cut over`。这不阻断已领取教材卡按 `2.0-textbook` 继续人工双审，但阻断：宣布 V2.4 已冻结、扩大 WIP、使用新 N/A 计分、采用新 content SHA 写回或启动任何试卷任务。
