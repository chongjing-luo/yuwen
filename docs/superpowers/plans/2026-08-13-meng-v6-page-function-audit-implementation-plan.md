# 《氓》V6逐页功能审计重构实施计划

规格依据：`docs/superpowers/specs/2026-08-13-meng-page-function-audit-redesign.md`
实施标识：`6.5-44-page-continuous-understanding-rebuild`
基线：`5.3-literary-participation`，127页、274分钟，仅作只读参照
状态：用户已确认V6.5整体重构路线；旧48页候选的历史放行结论失效，当前按44页权威总账重建无插图完整候选

## 0. V6.5执行改线（2026-08-14）

本节优先于下文仍用于保存历史审计谱系的127页/V6早期任务。V6.5不再沿旧48页逐模块小修，也不以旧候选的P0/P1/P2归零作为新候选证据。

权威输入为：

- `docs/superpowers/specs/2026-08-14-meng-v65-page-function-global-rhythm-redesign.md`；
- `work/备课/选择性必修下册/氓/_v62_stage/15_氓_V65_44页逐页重构总账.md`；
- 两份绑定旧48页固定哈希的独立重新审计，仅作为缺陷来源，不作为新候选放行结论。

V6.5按以下顺序执行：

1. 机械核验44页、225分钟、旧页去向、首次后用、删除损失与全课节奏矩阵；
2. 建立独立的`scripts/meng_v65/`单一数据源，不覆盖V6.4源码、PPTX和审查证据；
3. 同源生成无插图44页PPTX、每页备注真实剧本、逐页剧本Markdown、教学母版和学习材料；
4. 自动检查页码—ID—分钟映射、每页功能字段、前台/后台分离、标题泄答、产物后用和底层协议重复；
5. 完成Office验证、Markitdown、PDF、44张PNG和联系表，并至少执行一轮发现—修复—复验；
6. 由两名未参与本轮内容写作的独立审查者分别做视觉/页面功能审查与学生接收复演；任一P0/P1/P2都使候选回到重构，不取平均；
7. 只有无插图候选双审P0/P1/P2均为0，才逐页决定是否需要插图；每张图继续执行人物圣经、原句绑定、无图/有图A-B和事实边界审查。

44页不作为质量目标，只是当前结构结果。若物理候选证明相邻页面仍可无损合并、教师讲解不足、连续理解中断或收束再次表单化，允许继续合并、移动、重写或删除。

## 1. 实施目标

在不覆盖V5.3基线的前提下，对旧S001—S127逐页完成“保留、合并、移动、重写、删除”判定；依据判定重建V6课程数据，再同源生成教案、学习单、逐页无生试讲稿、PPTX和DOCX。页面结构冻结以后，才建立统一人物设定和必要插图。最终必须经过学生接收、视觉两名独立审查者复验，P0/P1/P2清零后方可放行。

V6不继承127页和274分钟作为目标。新版页数、模块数和自然时长只能由通过审计的学习事件反推。

## 2. 架构决策

### 2.1 基线、暂存与正式输出分离

- V5.3现有文件和脚本不作为V6的直接写入目标；
- V6中间产物写入`work/备课/选择性必修下册/氓/_v6_stage/`；
- V6源码写入`scripts/meng_v6/`及独立的V6构建、验证脚本；
- 全量放行后，V6正式交付物才写入《氓》目录根部；
- 旧V5.3只按经过核对的精确清单移入系统回收站，不使用通配符，不永久删除；
- 其他代理的高考试卷、知识库和无关脚本不在本计划修改范围内。

### 2.2 三层审计与权威现行清单

- `legacy_initial_audit`按旧ID保存V5原页的不可改写初始诊断，恰好覆盖S001—S127；
- `legacy_disposition_closure`保存每个旧ID的决定、决定专属证据、带类型目标引用、旧失败关闭情况和独立复核；
- `current_release_audit`分别审计现行`learning_page/event_carrier`页面和`learning_event`事件；页面除G1—G6外必须通过G7物理真相、G8反例生存和G9理解闭环，事件独立通过G4/G5/G7/G8/G9；
- Checkpoint 4冻结不含物理输出的`structure_manifest`并与独立`structure_assembly_snapshot`核对；Task 27从最终PPTX实测生成`slide_occurrence_inventory`，从DOCX实测生成独立`document_page_inventory`和`physical_assembly_snapshot`，并与`other_channel_inventory/release_artifact_manifest`派生最终`current_manifest`；结构清单还须与源码声明、课程数据可达图分别相等，最终清单再与PPTX slide、DOCX页、隐藏标志和备注事件清点相等；`student_visible`由实际PPTX投影状态推导，不允许手填绕审；
- 现行`learning_page`在页面级通过九道硬门；现行`event_carrier`通过G1/G2/G3/G6/G7/G8/G9，并与同层清单中直接所属的`learning_event`双向互指，只允许G4/G5借用事件独立证据且无循环；
- 旧页初审与关闭源按旧ID分块保存，构建器合并为覆盖127页的JSON与Markdown总表；现行内容另由清单和现行审计承载；
- 单个内容任务只生成旧页初审草案；每个相应检查点（连续内容批次通常成对）由两名未参与写作的独立审查者逐旧ID复核后，才生成逐文件`initial_audit_seal`；任何初审或封存链变化使后续关闭和放行失效；
- 事实性纠错只能追加带链式哈希、双独立复核和`effective_view_hash`的`seal_amendment`，相关处置必须基于新有效哈希重验；
- 旧页六门失败与初审中全部P0—P2缺陷均须集合级逐项关闭；非删除目标须以目标字段双向承接旧功能，学生可见/视觉缺陷不得仅关闭到事件；删除须全局扫描换页重现；
- `stage`模式允许尚未审到的旧页初审与关闭记录为`pending`，也允许现行G5合法`deferred`；已经审计的记录不允许缺字段；
- `release`模式要求旧S001—S127初始诊断完整且未改写、处置全部关闭，并拒绝现行`pending/deferred/provisional`、`na`误用、未关闭缺陷、清单遗漏或现行失败门；
- 所有G5后用边必须严格指向执行顺序更晚的事件并通过全局DAG检查；结构冻结另执行相邻页/同事件载体的无损合并反事实和删除内容全局负向扫描，不以逐页自述代替。
- 每个内容批次、页面、事件、学习单区域、构建器、Office输出和插图资产都进入`authorship_registry`；独立审查者必须与目标及全部上游作者并集机械判异，不能靠改名或遗漏作者制造独立性；
- Checkpoint 4的结构审计保持不可变，G7先为`pending_physical_build`。物理候选生成后只追加`physical_release_gate_overlay`，再机械派生`effective_release_audit`；overlay不得反写G1—G6/G8/G9。

### 2.3 内容与生成器解耦

```text
教材/原诗/证据档案
        ↓
scripts/meng_v6/text.js                 30组诗句、12个意义句群、解释边界
        ↓
scripts/meng_v6/audit/*.json            旧S001—S127初始诊断与处置关闭证据
scripts/meng_v6/content/*.js            新学习事件、学生前台、真实剧本和学习证据
        ↓
scripts/meng_v6/assemble.js              结构冻结后分配V6页码
        ├──→ 权威现行清单、现行审计、旧页关闭总表与旧新映射
        ├──→ 教案、学习单、逐页无生试讲稿
        ├──→ 完整母版与模块PPTX
        ├──→ Markdown与DOCX
        └──→ 课程数据快照
        ↓
机器合同 → Office验证 → 全量渲染 → 学生接收/视觉双审 → 回归 → 放行
```

内容按`opening`、`chapter_1`至`chapter_6`、`question_1`至`question_3`、`marriage_roundtable`、`knowledge_and_final`拆分。这样每批都能完成“审计—课程数据—课堂材料—渲染—复验”的纵向闭环，避免再出现一个近千行文件承担全部职责。

### 2.4 视觉先原型、后批量、再生图

- 先制作短句群、最长句群、含比较/活动句群三张真实PPT原型；
- 原型通过学生接收和视觉审查后，才扩展六章；
- 每页只有一个`primary_visual_duty`；
- 页面结构冻结后才制作W01/M01多视角角色设定；
- 只有已批准插图任务卡可以调用生图；
- 正式生图前冻结`scene_registry`、`prop_registry`、角色阶段、服装、发式、镜头尺度、视线轴、光源和相邻场景连续性；
- 每张候选图均用同文字同版式的无图A版/有图B版接受至少四名盲化观察者三秒测试；图片只因“好看”不得入页；
- V13、V17、V18按规格默认使用原文批注、文本关系和留白，不强行生成人物图。

## 3. 依赖顺序与覆盖范围

| 批次 | 旧ID范围 | 内容 |
|---|---|---|
| A | S001—S016 | 隐藏导航、封面、导入、三问、首次听读、最小支架 |
| B1 | S017—S027 | 第一章及章内活动 |
| B2 | S028—S039 | 模块承接、第二章及章内活动 |
| B3 | S040—S050 | 第三章及章内活动 |
| B4 | S051—S062 | 模块承接、第四章及章内活动 |
| B5 | S063—S073 | 第五章及章内活动 |
| B6 | S074—S085 | 模块承接、第六章及章内活动 |
| C1 | S086—S095 | 全文回读、初读修订、问题一 |
| C2 | S096—S101 | 问题二 |
| C3 | S102—S112 | 问题三、责任/阻力、第一章回看 |
| C4 | S113—S116 | 婚姻圆桌 |
| D | S117—S127 | 知识检索、收纳、终读、退出条 |

这些范围合计覆盖旧版全部127页且互不重叠。所有批次完成后才分配新ID，页数不会在审计过程中被旧页码绑架。

## 4. 任务清单

### Phase 0：基线保护与审计合同

## Task 1：建立V5只读基线与V6暂存边界

**描述：** 精确登记V5.3正式交付物和当前课程快照的文件名、大小与SHA-256；建立V6暂存路径常量和基线检查命令。任何V6构建命令若试图写入V5文件名，应立即失败。

**验收标准：**

- [ ] 基线清单只包含《氓》V5.3范围内的明确文件，不包含整个工作区；
- [ ] V6所有中间输出只能落到`_v6_stage`；
- [ ] 修改任一基线样本后，检查器返回非零状态并指出具体文件；
- [ ] 不改动现有V5.3文件内容和时间戳。

**验证：**

- [ ] `node scripts/meng_v6/check_baseline.js --write-manifest`
- [ ] `node scripts/meng_v6/check_baseline.js --verify`
- [ ] `git diff --name-only -- work/备课/选择性必修下册/氓 | rg 'V5'`只显示进入本任务前已有的共享工作树变化，不出现本任务新增写入。

**依赖：** 无
**预计涉及文件：** `scripts/meng_v6/paths.js`、`scripts/meng_v6/check_baseline.js`、`work/备课/选择性必修下册/氓/_v6_stage/baseline_manifest.json`
**规模：** M

## Task 2：实现逐页审计数据合同与失败码

**描述：** 把规格中的三层证据、封存/修订链、决定专属闭合、权威现行清单及外部清点、`learning_page/event_carrier/learning_event`规则、九门状态、跨批次`deferred`、G5有向无环图、物理overlay、作者登记、证据引用格式、失败码和`stage/freeze/release`差异实现为可测试合同。

**验收标准：**

- [ ] 旧页初始诊断、旧页处置关闭、权威现行清单、现行页面审计和`learning_event`事件审计的必填字段、枚举值及引用规则逐项可验证；
- [ ] 现行page具有`execution_order/release_status/next_use_refs`，`event_carrier.owner_event_id`必填且`learning_page`为空；页面pass G5边也进入严格后继DAG与事件反向输入核对；
- [ ] 旧`event_carrier`只允许借同一封存层`legacy_event_evidence`的独立G4/G5证据，旧事件与旧载体双向互指；引用V6事件或缺旧事件证据失败；
- [ ] S001—S127初始门状态、失败和带严重度/证据的`defect_registry`一经审定不可被现行结果覆盖；P0—P2缺陷由登记表机械导出，`closed_failure_codes/closed_defect_ids`分别与初始集合严格相等且逐项有目标字段证据和原审查者复验；
- [ ] `initial_audit_seal`逐文件绑定精确旧ID范围、SHA-256、两个不同的独立审查者、逐旧ID证据和时间；单任务不能提前封存；
- [ ] 每个`initial_audit_seal`还绑定该内容批次/源文件从`authorship_registry`机械导出的`reviewed_author_ids`和`authorship_registry_effective_sha256`；两名reviewer彼此不同且均不在作者并集中；批次作者遗漏、登记或源谱系漂移使seal及全部下游证据失效；
- [ ] 追加式`seal_amendment`必填`author_id`，并验证前驱/后继哈希、唯一链、两名独立`reviewer_ids`、机械导出的`reviewed_author_ids`、作者登记有效哈希和有效视图；`author_id`与两名reviewer不得重合，两名reviewer也不得属于目标及全部上游作者并集；断链、分叉、自审、未复核、作者登记漂移或初审/封存篡改均使相关下游关闭失效；
- [ ] 保留/合并/移动/重写/删除分别执行目标数量/类型、旧门前提、逐内容元素覆盖、双向谱系、缺陷闭合和目标现行通过规则；只有删除允许零目标；
- [ ] 学生可见旧页或前台/视觉/接收缺陷采用合并/重写时至少有一个页面目标；后台`event-only`须有隐藏状态与理由；
- [ ] text/asset/layout/event删除签名按各自规范化器和检测器扫描全部课程源；最终含图Office文件生成后再扫正文、notes/XML、资产引用、模块切片、DOCX和渲染，换资产ID重现也失败；
- [ ] `structure_manifest`与现行审计页面/事件集合完全相等，并分别等于源码声明节点、课程数据可达图和独立`structure_assembly_snapshot`；源声明不可达孤儿失败；最终`current_manifest`另与`physical_assembly_snapshot`及物理输出核对；
- [ ] 最终完整/模块PPTX中每个物理slide恰有一个合法且文件内唯一的page_id，物理页数、映射数、artifact声明页数相等，并按顺序一一双射；无ID页、重复ID、重页和错序均失败；
- [ ] 清单逐页记录每个正式artifact occurrence；官方学生放映入口由release artifact manifest冻结，`student_visible`等于所有官方输出中projected occurrence的OR；母版隐藏但模块可见仍须接收审查；
- [ ] 现行page必填反向谱系，旧初诊不得被要求填写现行`legacy_source_refs/inherited_functions`；候选输出完成后由审计+该候选artifact manifest生成bundle，重建候选须换哈希并使旧审查失效；
- [ ] 非删除缺陷关闭绑定目标字段、元素映射和现行审计节点的规范化SHA-256；任一目标/映射/审计变化使关闭及原审查者复验回到`pending`，Checkpoint 4和release均重验；
- [ ] 现行`event_carrier`只有第4、5门可用`na`，与直接所属`learning_event`双向互指，且只引用事件独立G4/G5证据；
- [ ] 现行G7在结构阶段只能是`pending_physical_build`，G1—G6/G8/G9全部通过后方可构建候选；候选阶段以`physical_release_gate_overlay`记录G7及结构门是否被物理事实失效，并机械派生`effective_release_audit`；
- [ ] G8最少反例集完整包含想不起、暂无新增、尚未找到、走神、误读、沉默、不同意、回答重复、发言超时、少数人包办和依赖动画但对象不存在；每个页面和每个`learning_event`都逐项记录`applicable/not_applicable`，`not_applicable`必须给出针对其功能、载体切换和物理渠道的具体理由，禁止整页、整事件或全课统一填`na`；每项适用反例都要保存`counterexample_run_refs`、真实出口、作品和回到主线的记录，事件还须验证跨载体和其他渠道切换后仍能完成；只有理想回应路径时返回`G8_IDEAL_PATH_ONLY`；
- [ ] G9必须同时定位原文输入、学生加工控件、反馈、可见修订和后页读取；教师答案直达结论或作品从未修订/调用分别返回`G9_TEXT_PROCESSING_SKIP/G9_FEEDBACK_REVISION_MISSING`；
- [ ] 每一道`pass`必须引用至少两种真正异源的证据；每个证据保存`evidence_id/source_object_id/source_type/source_origin_id/content_sha256/pointer`，同一构建器、同一课程字段的格式派生物或互相抄录的PPT/notes/Markdown只算一个来源；字段齐全、作者布尔值、时间求和、哈希一致和自审结论均不能单独或彼此冒充异源证据；
- [ ] `authorship_registry`覆盖内容批次、页面、事件、学习单区域、构建器、Office输出和插图资产；每项登记`object_ref/author_ids/authored_at/source_state_sha256/lineage_refs`，审查者与目标及全部上游作者并集有交集时失败，删改作者记录使seal、amendment和全部下游审查失效；
- [ ] `deferred`只允许现行阶段审计的第五门，必须绑定目标事件、目标批次和预期用途，且节点只能是`provisional`；
- [ ] 目标事件实现后，验证器检查来源—目标双向引用、目标实际读取字段和严格后继顺序，只把G5转为`pass`或`fail/G5_OUTPUT_ORPHAN`；结构阶段节点仍为`provisional`，不得提前写成`final`；
- [ ] 节点`execution_order`唯一且严格递增；全部G5边组成有向无环图；self、A↔B、任意环、同序和倒序调用均失败；
- [ ] 恰有一个现行事件`terminal_sink=true`且位于最大顺序，其他事件显式为false；终端`terminal_use`六个子字段、实际交付/保存证据齐全，零/多终端、非最大、缺证或封面/中途节点冒充均失败；
- [ ] canonical证据链固定schema版本：结构bundle五组件为`structure_manifest/current_release_audit/legacy_effective_view/legacy_disposition_closure/authorship_registry_effective_view`；final bundle九组件为`structure_audit_bundle/release_artifact_manifest/slide_occurrence_inventory/document_page_inventory/other_channel_inventory/physical_release_gate_overlay/effective_release_audit/current_manifest/authorship_registry_effective_view`；release attestation五组件为`release_audit_bundle/release_review_ledger/effective_release_review_view/final_defect_closure_summary/final_scorecard`；同时固定组件哈希、UTF-8/LF/NFC、相对POSIX路径、对象键排序、语义有序数组/集合数组规则和明确排除字段，生产器与验证器独立重算；
- [ ] 每一失败码至少有一个失败测试；
- [ ] 两个审查者结果不一致时，记录状态自动为`blocked_for_adjudication`而非通过；双方先只围绕证据引用各复核一次并保存`evidence_only_reconsideration_refs`，不得通过讨论统一口径；仍不一致才进入通用裁决合同；
- [ ] 通用`adjudication_record`适用于硬门、G7、学生接收、视觉、缺陷关闭和评分分歧，必填`target_object_ref/target_gate_or_review_type/original_review_ids/original_conclusions/evidence_only_reconsideration_refs/adjudicator_id/reviewed_author_ids/blindness_and_role_provenance/decision/reason/evidence_refs/adjudicated_at`；裁决者必须未参加写作、与目标全部上游作者及两名原审查者均不同，并在未看双方结论的盲态下独立查看原始证据；只有有效裁决才可解除`blocked_for_adjudication`；
- [ ] 结构冻结拒绝旧页未关闭/漏缺陷状态、G1—G6/G8/G9的`pending/deferred/fail`、清单或结构集合不等、谱系无关、删除重现和全局无损可合并状态；此时G7必须为`pending_physical_build`且节点必须为`provisional`。只有正式`release`才拒绝任何`provisional`并要求九门全部有效通过。

**验证：**

- [ ] `python -m unittest tests/test_validate_meng_v6_page_audit.py`
- [ ] `python scripts/validate_meng_v6_page_audit.py --help`
- [ ] 反例至少覆盖：精确旧ID S001—S127；缺字段/误用`na`；旧载体缺旧事件证据/借V6事件；旧初诊非法`deferred`；合法现行G5 `deferred`；page pass边漏目标；目标无真实调用；任一道门仅一项证据、两项同类型证据、PPT与同源notes/Markdown假装异源；G5 self/A↔B/同序/倒序；终端零/多/非最大/缺交付/中途冒充；重复旧ID；删除带目标、文本换页重现、删除视觉换资产ID/后期生图重现；合并无目标/只承接一半；移动掩盖G2/G3/G4/G6；无关但通过的目标；关闭后目标字段修改/删除或映射/现行审计改变；现行page漏反向谱系；学生可见视觉缺陷event-only；G7物理不一致/关键指令只在后台；G8只有理想学生路径，以及想不起、暂无新增、尚未找到、走神、误读、沉默、不同意、回答重复、发言超时、少数人包办、依赖动画但对象不存在中的任一适用反例无出口；统一填`na`、`not_applicable`无逐页理由；G9跳过原文加工/无反馈修订/无后页读取；结构阶段错误预填G7 pass或节点final；overlay改写结构门、缺节点、候选或作者哈希失配；作者登记漏作者或审查者属于上游作者；源声明孤儿；清单漏物理页/备注事件；完整母版重复ID、无ID额外页；DOCX强制Nxxx污染结构清单；母版隐藏但模块可见；模块可见却伪称非官方；可见标志造假；缺事件审计；owner/carrier单向或循环；其他渠道不存在/owner或顺序错误/内容变更/未说备注冒充听见；脚本台词误标prepared、实物卡墙误标scripted、prepared无材料/保存证据；真实试教前伪标observed；旧P0—P2缺陷漏关；删除缺陷合法`deletion_absence`与非法target；seal篡改及amendment断链/分叉/未复核；ledger重复当前状态/断链/旧open未闭合；release缺陷漏关/伪open=0/重复或无源关闭/删除旧发现/修复后源变更；最终review ID非法回写structure audit造成hash循环；bundle键序变化哈希稳定、非排除字段变化必变、组件漏项/替换失败；release现行fail/pending/deferred/provisional，均得到对应失败码。
- [ ] 裁决负向fixtures至少覆盖：作者裁决、裁决者与任一原审查者同人、先看双方结论、没有先行证据复核、缺目标/原结论/理由/证据/时间/作者集合、设计者直接取较宽结论和无有效裁决却解除`blocked_for_adjudication`；
- [ ] seal/amendment作者负向fixtures至少覆盖：内容批次作者充当seal reviewer、amendment作者充当reviewer、作者登记漏掉一名批次作者、registry或source lineage漂移后仍沿用旧seal/amendment；

**依赖：** Task 1
**预计涉及文件：** `scripts/validate_meng_v6_page_audit.py`、`tests/test_validate_meng_v6_page_audit.py`、`tests/fixtures/meng_v6_audit/`
**规模：** M

## Task 3：生成覆盖127页的旧版审计台账骨架

**描述：** 从V5课程快照导入S001—S127的稳定ID、模块、阶段、页型、标题、可见文字、旧时长和页序；为十二个批次分别建立不可改写的初始诊断源和处置关闭源。未审批次只允许在`stage`模式标为`pending`，不能预填“保留”或关闭结论。

**验收标准：**

- [ ] 旧ID集合恰为S001—S127，无缺失、重复、越界；
- [ ] 每个旧页都绑定一个批次、一个初始诊断源文件和一个处置关闭源文件；
- [ ] 总表能生成JSON与便于人工复核的Markdown；
- [ ] 骨架不把旧`experience/thought/learning`模板误当成V6审计证据。

**验证：**

- [ ] `python scripts/build_meng_v6_audit.py --mode stage`
- [ ] `python scripts/validate_meng_v6_page_audit.py --mode stage --input work/备课/选择性必修下册/氓/_v6_stage/05_氓_V6逐页功能审计.json`
- [ ] `jq '.pages|length' .../05_氓_V6逐页功能审计.json`输出`127`。

**依赖：** Task 2
**预计涉及文件：** `scripts/build_meng_v6_audit.py`、`scripts/meng_v6/audit/index.json`、`scripts/meng_v6/audit/*.json`、`work/备课/选择性必修下册/氓/_v6_stage/05_氓_V6逐页功能审计.md`
**规模：** M

### Checkpoint 0：审计基础

- [ ] V5基线验证通过；
- [ ] 审计合同全部测试通过；
- [ ] 127页台账覆盖完整；
- [ ] V6尚未写入正式交付目录。

### Phase 1：原诗合同与导入纵向切片

## Task 4：冻结原诗、意义句群、认识边界与教学手法合同

**描述：** 从当前教材证据档案迁移30组原诗、教材释义、关键字词、12个意义句群、六章行动与高风险解释边界；同时建立教学手法注册表。数据只迁移可核对内容，不复制V5的页面结构。手法不按“热闹程度”收录，而按它解决的真实阅读困难和形成的学生作品收录。

**验收标准：**

- [ ] 30组诗句顺序、字形、标点与教材证据一致；
- [ ] 12个意义句群各自引用连续原诗范围；
- [ ] “贸丝/谋”“无怒”“淇则有岸”“亦已焉哉”等边界进入机器合同；
- [ ] 责任与关系延续/停止阻力不相互致因。
- [ ] 每项手法完整声明“原诗输入→阅读困难→学生加工→每人入口→交换/公开→听众任务→反馈修订→保存位置→后页读取”；缺一环不得进入正式课件；
- [ ] 每个意义单元最多一个主活动；仅换座位、颜色卡、抢答、计时器或角色称谓而不改变认知动作和作品形态时，机器合同判为无效花样；
- [ ] 手法库至少覆盖朗读比较、动作排序、证据分类、解释竞争、生活镜头、人生接力、证据听证、圆桌修订和遮答检索，但每项只在匹配真实阅读困难时调用，不以数量为目标。

**验证：**

- [ ] `node scripts/meng_v6/verify_text.js`
- [ ] `python -m unittest tests/test_validate_meng_v6_text_contract.py`
- [ ] 与`01_文本研究与证据档案.md`及教材原文进行逐项差异核对，差异为0或有书面解释。

**依赖：** Task 1
**预计涉及文件：** `scripts/meng_v6/text.js`、`scripts/meng_v6/methods.js`、`scripts/meng_v6/verify_text.js`、`tests/test_validate_meng_v6_text_contract.py`
**规模：** M

## Task 5：完成S001—S016逐页审计与新导入事件设计

**描述：** 逐页判断旧隐藏导航、封面、限定三篇导入、预制主题谱、四张三问页、完整听读、初读停顿和背景支架。建立“个人尽量多检索→四人轮说→每组两张贡献卡→全班扩展→全体先连接命名→至少三名学生公开举证并由全班修订→揭示《氓》→三问→完整听读”的导入顺序，明确记忆恢复路径、贴卡/换组余量和总公开时间上限；不为一句教师转场保留独立页面。

**验收标准：**

- [ ] S001—S016旧页初始六门、证据引用和处置方向草案齐全，初始失败不改写；本任务不得提前封存；对应V6现行主题谱等跨批次后用标为`deferred/provisional`，不提前伪造通过；
- [ ] 旧S003—S005不以原结构进入V6；
- [ ] 题名页不再是物理第一页，只能在本班主题谱形成后出现；删除“先宣布课题、再补做回忆”的旧顺序；
- [ ] 揭题前的回忆单、提示条、目录索引、教师台词和屏幕均不出现《氓》题名、版本号、人物或结局暗示；不是只移动PPT页；
- [ ] 每名学生有独立检索和小组发言入口，想不起作品者有隐藏提示条、翻目录或先听后补路径；
- [ ] 初始静态N002不声称不存在的淡入动画；60秒后的恢复路径由真实教师台词和学习单控件承担；不把三篇当上限，至少一篇以后允许继续扩充；
- [ ] N003每组形成两张不同贡献卡；N004按两卡/组和真实换组重新计时，班级卡墙约十六张，不因管理方便压回八张；
- [ ] N005全体先写卡号与临时名字，至少三名不同学生公开移动、命名并引用卡片文字，全班执行保留/改名/移回，原提议者留下修订；
- [ ] 主题谱只使用现场出现的学生材料，并保留作品出处、卡号和学生作者；教师固定类别在PPT、notes、逐字稿、学习单、板书模板、实物与插图中均为零；
- [ ] 全班贡献页同时提供“有新增”和“暂无新增但核对重复卡”的同层级听者路径，不强迫人人伪造新观点；
- [ ] 开头三问不要求学生写高阶归因猜想；
- [ ] 首次听读跨页只作为同一事件的`event_carrier`。
- [ ] N005课前冻结“跨课时保留实物卡墙”或“当场拍照、下节课使用归档照片”的真实备份路径；
- [ ] N010把“抄一句”和“尚未找到”作为同层级诚实出口；N011明确三项路标由教师提供，再撤去完整句让学生遮屏检索复述，不伪装成自主发现；
- [ ] N012把“需要调整”和“原本读顺”设为同层级路径；前者标重新停连处，后者圈连续动作，两者均在无斜线教材原句中重读；
- [ ] N008/N009实际7米可读性在物理候选阶段保留为待测P3，未取得渲染和教室证据前不宣称通过。

**验证：**

- [ ] `python scripts/validate_meng_v6_page_audit.py --mode stage --batch opening ...`
- [ ] `node scripts/meng_v6/assemble.js --through opening --dump-events`
- [ ] 人工核对审计总表中S001—S016无`pending`，S017—S127仍保持`pending`。

**依赖：** Tasks 3、4
**预计涉及文件：** `scripts/meng_v6/audit/opening.json`、`scripts/meng_v6/content/opening.js`、`scripts/meng_v6/assemble.js`
**规模：** M

## Task 6：生成导入切片的教案、学习单和真实剧本

**描述：** 从同一事件数据生成导入切片的教学母版、学习单和逐页无生试讲稿。逐字稿必须包含教师自然台词、等待、分支、听众任务、证据位置和转场。

**验收标准：**

- [ ] 三种Markdown的任务措辞、时长、产出位置一致；
- [ ] 学生前台不含角色、设计目标、方法论、评估语言和预制答案；
- [ ] 学生前台用自然、具体、可朗读的现代汉语与原诗语言组织，不出现“赋能、抓手、闭环、链路、颗粒度、价值引领”等项目化套话，不以整齐三段式代替真实语意；
- [ ] 每页前台由语文语言审读单独回答“学生第一眼读到什么、是否像课堂中的人话、是否保留诗意而不装腔”；任何一句需要教师二次翻译才可执行即返工；
- [ ] 每一实际屏幕状态均有可演剧本；
- [ ] 每页剧本是完整可排演场景，不是若干提示条：包含教师连续台词、停顿、走位、学生可见动作、听众同步任务、边界分支、收束与自然切页句；
- [ ] 页面合同中的关键指令在屏幕、学习单或明确会说出的台词中真实出现，后台设计字段不能冒充学生已接收；
- [ ] 导入学习单能保存个人作品、同伴补充和一项未想到的作品/主题；
- [ ] 导入学习单另保存N005个人连接的两张卡号、临时命名、公开核对后的保留/改名/移回及卡片文字依据；
- [ ] 学习材料拆成揭题前无课名的“爱情与婚姻文学回忆单”和揭题后才发放/翻开的《氓》阅读卡；任何页眉、页脚、文件打印标识和教师分发台词均不提前泄题；
- [ ] 物理材料包包含本班已学篇目目录索引、只写篇名的提示条、空白磁贴贡献卡、磁贴/胶贴、书写工具、空板位置和卡墙保存/摄影备份说明；材料清单没有用“课堂上会有”代替课前`prepared`证据；
- [ ] N003重新按教师完整口令、四人讲述、听记、每人圈两项、代记、两张贡献卡书写和换手计算真实时间；N004按十六张卡的贴卡、说明与换组计算；N005按全体个人生成、三人公开举证、全班反馈、原作者修订和教师现场复述计算；任一动作被压缩到不可执行时增加时长，不用秒数相加冒充课堂时间；
- [ ] 沉默、记忆空白、影视作品混入等分支有自然处理。

**验证：**

- [ ] `node scripts/build_meng_v6_markdown.js --through opening --out .../_v6_stage`
- [ ] `python scripts/validate_meng_v6_lesson_package.py --mode stage --through opening ...`
- [ ] `rg -n '林晓|硬门|接收审计|理解链|知识碎片|不填表|不概括' .../_v6_stage/*.md`无学生前台命中。
- [ ] 前台语言禁词扫描通过后，再由独立学生接收审查者逐页朗读任务；静态扫描不能代替语言审读。

**依赖：** Task 5
**预计涉及文件：** `scripts/build_meng_v6_markdown.js`、`scripts/meng_v6/notes.js`、`scripts/validate_meng_v6_lesson_package.py`、`tests/test_validate_meng_v6_lesson_package.py`
**规模：** M

## Task 7：建立三种句群真实版式原型

**描述：** 使用真实原诗制作短句群、最长句群、含比较/活动句群三张16:9原型；不是做最终整课，而是先验证当前原句、章内轨道、六章位置码和关系/活动区能否共存。

**验收标准：**

- [ ] 当前原句≥38pt，最长句群确需换行时≥34pt；
- [ ] 章内完整轨道≥22pt，六章位置码≥18pt；
- [ ] 每页最多四个主要信息块且只有一个`primary_visual_duty`；
- [ ] 使用`warnIfSlideHasOverlaps`和`warnIfSlideElementsOutOfBounds`，意外警告为0；
- [ ] 实际PPTX可打开、转PDF，并生成三张300 dpi单页审查图；
- [ ] 学生接收和视觉两名独立审查者均明确通过后才冻结。

**验证：**

- [ ] `node scripts/build_meng_v6_pptx_prototypes.js`
- [ ] `python /home/ubuntu/.agents/skills/pptx/scripts/office/validate.py .../_v6_stage/prototypes/00_句群版式原型.pptx`
- [ ] `python /home/ubuntu/.agents/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf .../00_句群版式原型.pptx`
- [ ] `pdftoppm -png -r 300 .../00_句群版式原型.pdf .../prototype`
- [ ] 修复至少一轮审查发现的问题后重新渲染并复验。

**依赖：** Tasks 4、6
**预计涉及文件：** `scripts/build_meng_v6_pptx_prototypes.js`、`scripts/meng_v6/visual_system.js`、`work/备课/选择性必修下册/氓/_v6_stage/prototypes/`
**规模：** M

## Task 8：走通导入切片PPTX与DOCX端到端

**描述：** 将导入事件、真实剧本和学习单生成PPTX/DOCX，证明单源数据能完整穿过构建、Office验证、文本提取和视觉审查。

**验收标准：**

- [ ] PPTX备注与逐页试讲稿逐页一致；
- [ ] DOCX显式使用A4尺寸、固定页边距、DXA表格宽度和正确列表；
- [ ] PPTX/DOCX均可转PDF，无损坏、裁切、溢出和占位符；
- [ ] 导入切片学生接收审查与视觉审查P0/P1/P2清零；
- [ ] 每张物理页逐项记录“唯一功能—共同动作—可见产物—视觉第一层—次级分支—后页调用”，PPT视觉第一层必须与唯一功能一致；
- [ ] 活动页不得让反例分支与共同动作争夺第一视觉；N003“两张贡献卡”、N004“贴两卡—说一处—听众留痕”、N005“原提议者根据全班反馈亲手修订”在教室投影中一眼可见；
- [ ] 完成至少一轮原尺寸渲染后“发现视觉问题—修改课程源与PPT—重新构建—重新渲染—复验”的闭环，并保存前后候选哈希；
- [ ] 实际物理顺序为个人检索、四人轮说、全班贡献、现场主题谱、题名揭示、三问、N008/N009一次完整听读、初读保存、最小《诗经》支架和四言节奏；物理页、notes和学习单顺序一致；
- [ ] 自动扫描所有学生暴露渠道，证明《氓》题名在N001揭题事件之前零出现；N001之后教材翻页、三问和阅读卡才合法出现课名；
- [ ] N003时间通过带完整口令、等待、换手和异常缓冲的剧本演算；N004“有新增/暂无新增”、N010“抄一句/尚未找到”、N012“需要调整/原本读顺”均在PPT和学习单上第一眼平权；
- [ ] 跨PPT、speaker notes、逐字稿、学习单、板书/物料和插图执行答案状态扫描；N005不存在固定“相遇、等待、错过、阻隔、相守、破裂”等口头预制类别；
- [ ] N011采用真实的两状态或遮答流程：教师提供必要输入时答案可见，检索复述时完整句不可见；仅在notes中声明“撤去”不算实现；
- [ ] 逐页保存G7物理清点、G8适用反例执行和G9理解闭环证据；未通过不得沿用此前只验证旧合同的绿色测试结果；
- [ ] 发现问题—修复—复验至少完成一轮。

**验证：**

- [ ] `node scripts/build_meng_v6_pptx.js --through opening --out .../_v6_stage`
- [ ] `node scripts/build_meng_v6_docx.js --through opening --out .../_v6_stage`
- [ ] `python -m markitdown .../_v6_stage/04_氓_V6导入切片.pptx`
- [ ] `pandoc .../_v6_stage/02_氓_V6导入切片教学母版.docx -t plain`
- [ ] PPTX和DOCX分别执行Office结构验证、PDF转换和联系表检查。

**依赖：** Tasks 6、7
**预计涉及文件：** `scripts/build_meng_v6_pptx.js`、`scripts/build_meng_v6_docx.js`、`work/备课/选择性必修下册/氓/_v6_stage/opening/`
**规模：** M

**2026-08-13二次独立审查与返工记录：** 用户要求导入扩大爱情/婚姻文学回顾范围并强化学生声音后，学生接收审查发现N005的P2：页面和规范声称主题谱只从现场卡片生长，但逐字稿固定说“相遇的欢喜、等待、错过、阻隔、相守与破裂”，且仅一名学生移动一张卡，教师串联时间反而更长。视觉审查确认N002—N005均不需要人物/叙事插图，真实卡墙是N004/N005主视觉；用合成图替代现场材料会构成P1。旧导入PASS凭证随源状态变化自动失效。返工将N002改为至少一篇、尽量多写；N003改为每人圈两项并形成两张贡献卡；N004扩展为约十六张卡；N005改为全体先连接临时命名、至少三人公开举证、全班保留/改名/移回、原提议者修订，教师只复述现场真实出现线索。新增逐页价值链、参与分母、作品作者、反馈上限、延后消费者状态与跨渠道答案扫描合同。新候选仍需原两名独立审查者按新哈希复验；未经复验不得恢复PASS。

### Checkpoint 1：首条纵向链

- [ ] 两名独立审查者逐旧ID复核S001—S016初诊草案；旧页被诊断出的P0/P1/P2全部编号写入`defect_registry`并原样封存，只要求审计记录自身无缺证、漏项或未裁决分歧；随后生成双审`initial_audit_seal`并验证范围、身份与哈希；
- [ ] S001—S016旧页初审无`pending`且已封存，处置记录无未解释状态；导入现行节点只允许第五门出现符合合同且目标已登记的`deferred`，相应`release_status`必须为`provisional`；
- [ ] 导入事件不预制婚姻处方；
- [ ] 揭题前所有物理渠道均未泄露《氓》，N005之后才发生唯一揭题事件；
- [ ] 全员发言、听众任务和记忆恢复可执行；
- [ ] 三张版式原型双审通过；
- [ ] 导入Markdown、PPTX、DOCX和备注同源且可渲染；
- [ ] V5基线哈希仍一致。

### Phase 2：六章逐句与句群讲读

以下六个任务均执行同一闭环：旧页审计 → 新意义句群 → 基本释义与行动 → 本章异质活动 → 整章回读与连续章意 → 局部材料生成 → 自动验证 → 学生接收结构化自检 → 视觉结构化自检。每批自检必须逐页记录前置、全员入口、听众任务、作品保存、第五门状态、后用目标、当前原句字号、章内轨道字号、六章位置码、信息块数和唯一主视觉。每一章不得复制上一章的模板化`experience/thought/learning`或通用讲稿。

早期V6现行节点的产出若只能在任何尚未实施的后续批次中核验（包括Task 12、Q1—Q3、全文回看或Task 19知识收纳），现行阶段审计将第五门记为`deferred`，同时登记目标事件；不得提前伪造`pass`。目标任务完成后必须把G5转为`pass`，节点仍为`provisional`或暴露为失败。旧页初始诊断不用`deferred`且不得随现行结果改写。每完成两个连续内容批次进行一次学生接收、视觉双独立审查和模块回归，未通过不得进入下一批。

## Task 9：重构第一章S017—S027

**描述：** 以“外在印象与真实来意”“远送、媒妁条件、安抚与婚期”两个句群重构第一章，保留第一次观看，全文后再进行后见重读。

**验收标准：**

- [ ] 旧11页初始诊断与处置方向草案齐全，本任务不提前封存；V6现行跨批次后用未实现者明确标`provisional/deferred`；
- [ ] “蚩蚩”“贸丝/谋”“无怒”不越过事实边界；
- [ ] 学生先形成自己的初见印象，教师不提前宣布“伪装”或“恋爱脑”；
- [ ] 章末能用自然话连续讲清相识、求婚和婚期条件；
- [ ] 本章产出登记Task 17第一章回看的目标事件和预期用途；Task 17完成前不得把第五门标为通过。

**验证：**

- [ ] `node scripts/meng_v6/assemble.js --through chapter_1`
- [ ] `python scripts/validate_meng_v6_page_audit.py --mode stage --batch chapter_1 ...`
- [ ] 生成并渲染第一章PPT、逐字稿和学习单局部，独立视觉复核版式原型没有在真实内容中失效。

**依赖：** Checkpoint 1
**预计涉及文件：** `scripts/meng_v6/audit/chapter_1.json`、`scripts/meng_v6/content/chapter_1.js`、相关测试快照
**规模：** M

**2026-08-13执行记录：** 已形成N013—N021九页、38分钟的第一章候选，完成课程源、学习单、逐页真实剧本、PPTX和课程快照的同源构建。第一轮视觉审查以N018孤字P2否决；修复后主审又以主视觉职责登记失真P2否决。与导入、第二章联合播放时，N015的“表面上/实际上”又因在已知失败婚姻语境中预置伪装/欺骗框架被判P2；随后按文本次序改为“诗句先写的动作/女子随后说明的来意”，保留“匪”的否定转折并明确单凭本句不能断言欺骗。三项均先增加失败测试，再重建、重渲染并由原独立审查者回归。最终候选教学功能9/9 PASS、视觉9/9 PASS，P0/P1/P2为0；第一、二章联合51项自动测试与Office结构验证通过。仍保留两项P3：N014—N018真实课堂节奏疲劳待试教，N020初见档案待Task 17物理回收。证据见`scripts/meng_v6/reviews/chapter1_package.json`。本记录只证明桌面设计存在可执行学习通道，不替代Checkpoint 2A的旧页封存或真实课堂验证。

## Task 10：重构第二章S028—S039

**描述：** 以等待动作和卜筮迁嫁为两个句群，使用“望—不见—泣—见—笑—迁”的动作与双速度朗读，让声音变化服务叙事。

**验收标准：**

- [ ] 旧12页初始诊断与处置方向草案齐全，本任务不提前封存；V6现行进入Q1的章意后用标`provisional/deferred`；
- [ ] 模块承接页若不能证明独立损失则合并，不保留纯口号；
- [ ] 学生能用动作顺序解释朗读速度，而非只接受情绪标签；
- [ ] 卜筮只按当时婚俗与人物寻求确定来解释，不写成长期关系保证；
- [ ] 章末产出登记Q1人生接力目标事件；Task 15完成后才核验并把G5转为`pass`，节点仍为`provisional`。

**验证：**

- [ ] `node scripts/meng_v6/assemble.js --through chapter_2`
- [ ] 运行批次审计、课程合同、PPTX/DOCX局部渲染；
- [ ] 检查与第一章连续页面没有无功能重复的布局或课堂动作。

**依赖：** Task 9
**预计涉及文件：** `scripts/meng_v6/audit/chapter_2.json`、`scripts/meng_v6/content/chapter_2.js`、相关测试快照
**规模：** M

**2026-08-13执行记录：** 已形成N022—N030九页、39分钟的第二章候选，完成课程源、教学母版、学习单、逐页真实剧本、PPTX和课程快照的同源构建。视觉首审以N023人物站位与‘乘彼垝垣’正面矛盾判P1并否决整章：原图把女子放在墙下、让视线穿墙。改为正确站位示意并通过局部复验后，三模块联合学生盲走又发现更深的答案时序问题：N023在学生画图前已经显示完整站位和视线，N024在学生配对前已经显示三组答案，两页均判P1。随后先增加课程、学习单、PPT三类失败测试；N023改为人物站位、视线方向、目光/路线三个生成空框，N024改为两句原诗加三组对照空槽，教师只在个人尝试后提供必要词义，同伴只指出断点、不代答。最终候选由原两名审查者复验通过，N022—N030教学功能9/9 PASS、视觉9/9 PASS，P0/P1/P2为0；三模块联合51项自动测试与Office结构验证通过。保留P3：真实分课、活动疲劳、材料管理和N026班级噪声下盲听稳定性待试教；N030章意待Task 15的`E_Q1_LIFE_RELAY`物理回收。证据见`scripts/meng_v6/reviews/chapter2_package.json`。本记录只证明第二章桌面设计存在可执行学习通道；整篇当前仍只精读2/6章，不构成全课通过。

### Checkpoint 2A：第一、二章双审回归

- [ ] 两名独立审查者逐旧ID复核S017—S039初诊草案；旧页P0/P1/P2全部编号封存，只清除审计记录自身的漏项、缺证与未裁决分歧；随后生成覆盖完整、身份合规的双审封存；
- [ ] 两章每页学生接收与视觉结构化自检完成；
- [ ] 学生接收审查者检查前置、全员入口、听众任务、保存和后用登记；
- [ ] 视觉审查者检查全部两章页面的实际渲染，不只看原型；
- [ ] P0/P1/P2清零；
- [ ] 第一、二章连续讲述和模块首尾回归通过。

## Task 11：重构第三章S040—S050

**描述：** 先让学生看见“沃若”的色彩、质地和生命状态，再从斑鸠过渡到女子劝诫；多解释先保存，到第四章“黄而陨”再修订。

**验收标准：**

- [ ] 旧11页初始诊断与处置方向草案齐全，本任务不提前封存；V6现行桑叶假设到Task 12、章意到Task 15的后用分别登记`deferred/provisional`；
- [ ] 赋比兴在学生先观察语言现象后才命名；
- [ ] “耽/说”进入男女后果差异，但不把女子投入写成对方伤害原因；
- [ ] 至少两种桑叶解释均记录证据和限度；
- [ ] 解释假设登记Task 12的目标事件和预期修订方式，不在Task 12实现前标`pass`。

**验证：**

- [ ] 运行`--through chapter_3`全链验证；
- [ ] 搜索课堂前台，不出现预制“青春—色衰—被弃”的唯一图解；
- [ ] 第三章先完成学生接收结构化自检；待第四章完成后，再按第三章＋第四章配对执行模块联系表双独立审查。

**依赖：** Checkpoint 2A
**预计涉及文件：** `scripts/meng_v6/audit/chapter_3.json`、`scripts/meng_v6/content/chapter_3.js`、相关测试快照
**规模：** M

## Task 12：重构第四章S051—S062

**描述：** 调用第三章桑叶假设，比较“沃若—黄而陨”，再区分食贫、淇水等经历事实与“不爽/贰其行/二三其德”的责任判断。

**验收标准：**

- [ ] 旧12页初始诊断与处置方向草案齐全，本任务不提前封存；V6现行第三章解释后用的双向引用在本任务把G5转为`pass`，节点仍为`provisional`，本章章意到Task 15的后用仍按合同登记；
- [ ] 第三章解释假设发生可见修订；
- [ ] “淇水汤汤”不固定为第三次明确渡水；
- [ ] 事实和责任判断由学生分类并返回原词；
- [ ] 男子责任不被贫困、女子投入或时代处境稀释。

**验证：**

- [ ] 运行`--through chapter_4`全链验证；
- [ ] 单独检查桑叶比较页与事实/判断页的`primary_visual_duty`唯一；
- [ ] 学习单保存解释修改前后和事实/判断分类证据。

**依赖：** Task 11
**预计涉及文件：** `scripts/meng_v6/audit/chapter_4.json`、`scripts/meng_v6/content/chapter_4.js`、相关测试快照
**规模：** M

### Checkpoint 2：第三、四章双审回归

- [ ] 两名独立审查者逐旧ID复核S040—S062初诊草案；旧页P0/P1/P2全部编号封存，只清除审计记录自身的漏项、缺证与未裁决分歧；随后生成覆盖完整、身份合规的双审封存；
- [ ] 第三、四章每页结构化自检完整；
- [ ] 第三章桑叶假设到第四章修订的双向调用已把G5转为`pass`且节点仍为`provisional`；
- [ ] 两名独立审查者覆盖第三、四章全部实际生成页面；
- [ ] P0/P1/P2清零；
- [ ] S017—S062旧页初诊均已双审封存，处置状态可追踪；对应现行节点审计完成，前三章到婚变责任的叙事、意象和语言连续回归通过。

## Task 13：重构第五章S063—S073

**描述：** 把“多年”还原为一天，通过个人动作、组内合成、生活镜头与原诗边界，使劳作、粗暴、家人不解和独自反思成为可感的日常。

**验收标准：**

- [ ] 旧11页初始诊断与处置方向草案齐全，本任务不提前封存；V6现行进入Q1/Q2的章意和生活处境产出按合同登记`deferred/provisional`；
- [ ] 每人先写生活动作和原诗依据，不能由一名表演者包办；
- [ ] 生活镜头标明诗中事实和合理想象，不虚构施暴方式；
- [ ] “兄弟不知”不推断女子必然曾求助，也不脸谱化全部家人；
- [ ] 时间压缩被学生还原并重新接回原诗。

**验证：**

- [ ] 运行`--through chapter_5`全链验证；
- [ ] 对最长句群原型在第五章真实页面上执行300 dpi单页视觉复验；
- [ ] 学生接收审查检查个人准备、听众任务和合理想象边界。

**依赖：** Checkpoint 2
**预计涉及文件：** `scripts/meng_v6/audit/chapter_5.json`、`scripts/meng_v6/content/chapter_5.js`、相关测试快照
**规模：** M

## Task 14：重构第六章S074—S085

**描述：** 处理偕老愿望、边界语言、总角记忆、违誓核验和停止判断；用两种朗读方案保留“亦已焉哉”的复杂声音。

**验收标准：**

- [ ] 旧12页初始诊断与处置方向草案齐全，本任务不提前封存；V6现行章意与朗读证据进入Task 15/19的后用按合同登记`deferred/provisional`；
- [ ] “有岸/有泮”保留教材允许的解释竞争；
- [ ] 总角是童年回忆，不以青年人物替代；
- [ ] “亦已焉哉”只证明停止判断，不证明已经离家或后来生活；
- [ ] 两种朗读方案都以长期经历和原词为依据，不规定唯一情绪。

**验证：**

- [ ] 运行`--through chapter_6`全链验证；
- [ ] V18页面保持原诗、朗读标记和留白，不调用人物结论图；
- [ ] 第五章＋第六章完成模块联系表双独立审查和一轮修复回归；六章连续讲读另做全程接收与视觉回归。

**依赖：** Task 13
**预计涉及文件：** `scripts/meng_v6/audit/chapter_6.json`、`scripts/meng_v6/content/chapter_6.js`、相关测试快照
**规模：** M

### Checkpoint 3：第五、六章双审与六章全文回归

- [ ] 两名独立审查者逐旧ID复核S063—S085初诊草案；旧页P0/P1/P2全部编号封存，只清除审计记录自身的漏项、缺证与未裁决分歧；随后生成覆盖完整、身份合规的双审封存；
- [ ] S017—S085旧页初诊均已双审封存、处置状态可追踪，对应现行页面/事件均已按当前阶段审计；
- [ ] 第五、六章每页结构化自检完整，两名独立审查者覆盖全部实际生成页面；
- [ ] 30组诗句、12个意义句群和六章顺序100%覆盖；
- [ ] 六章均完成整章读—句群讲读—章内活动—完整回读—连续章意；
- [ ] 原文不是孤句与术语碎片，而是持续叙事主线；
- [ ] 前态/当前变化/后向不超负荷，实际渲染无缩字；
- [ ] 六章学生接收与视觉审查P0/P1/P2清零。

### Phase 3：全文回连、三问、圆桌与收纳

## Task 15：重构全文回读与问题一S086—S095

**描述：** 把六章章意、初读停顿点和人生接力连接起来；六组每人先贡献一条章内变化，再合成接力叙述，听众找转折和断裂并促成修改。

**验收标准：**

- [ ] 旧10页初始诊断与处置方向草案齐全，本任务不提前封存；本任务关闭V6六章指向Q1的后用，自身转折修订进入Task 19收纳时登记`deferred/provisional`；
- [ ] 两张全文原文页只作为一个回读事件的载体；
- [ ] 组内材料覆盖全员，公开代表不能替代组员生成；
- [ ] 听众记录一处转折与一处空缺，每两章至少发生一次追问；
- [ ] 每人保存并修订“最重要转折＋原诗证据＋后续变化”。
- [ ] 第一至第六章所有指向Q1的`deferred`第五门逐项核验真实调用，把G5转为`pass`，节点仍为`provisional`；未被调用者标记失败并返工。

**验证：**

- [ ] 运行`--through question_1`全链验证；
- [ ] 检查六章接力是否能按原诗顺序讲出完整人生而不把第三章劝诫误当新事件；
- [ ] 听众记录和个人修订进入学习单并在教师收束中被调用。

**依赖：** Checkpoint 3
**预计涉及文件：** `scripts/meng_v6/audit/question_1.json`、`scripts/meng_v6/content/question_1.js`、相关测试快照
**规模：** M

## Task 16：重构问题二S096—S101

**描述：** 让诗句重新长成日子：个人选景与原诗准备、组内合成生活镜头、公开呈现、听众证据质疑、呈现组现场改写、个人总结句修订。

**验收标准：**

- [ ] 旧6页初始诊断与处置方向草案齐全，本任务不提前封存；本任务关闭V6前文章内指向Q2的后用，自身处境句进入Task 19时登记`deferred/provisional`；
- [ ] 每人有个人选景和原诗依据；
- [ ] 每个公开镜头后都发生一次证据质疑和现场修改；
- [ ] 听众能区分诗中依据与合理想象；
- [ ] 每人保存“她的不幸，不只是……更是……”修改前后。
- [ ] 前文章内生活处境产出凡登记Q2后用者，全部核验双向引用并把G5转为`pass`，节点仍为`provisional`。

**验证：**

- [ ] 运行`--through question_2`全链验证；
- [ ] 检查课堂前台没有预先列出教师分类答案；
- [ ] 学生接收独立审查确认不存在一人包办和听众闲置。

**依赖：** Task 15
**预计涉及文件：** `scripts/meng_v6/audit/question_2.json`、`scripts/meng_v6/content/question_2.js`、相关测试快照
**规模：** M

### Checkpoint 4A：Q1、Q2双审回归

- [ ] 两名独立审查者逐旧ID复核S086—S101初诊草案；旧页P0/P1/P2全部编号封存，只清除审计记录自身的漏项、缺证与未裁决分歧；随后生成覆盖完整、身份合规的双审封存；
- [ ] Q1、Q2每页学生接收与视觉结构化自检完整；
- [ ] 章意接力和生活镜头的前向`deferred`均按真实调用关闭；
- [ ] Q1/Q2新生成且指向Task 19收纳的`deferred`均有合法目标，不被误算为通过；
- [ ] 两名独立审查者覆盖S086—S101实际生成材料；
- [ ] P0/P1/P2清零；
- [ ] 全文回读—人生接力—生活处境的跨模块路径回归通过。

## Task 17：重构问题三与第一章回看S102—S112

**描述：** 在个人准备前显示“直接伤害、关系延续与失衡、停止后的现实阻力”三种不同问题；通过全班证据听证和全员卡片修订，区分责任、解释和边界，再回看第一章。

**验收标准：**

- [ ] 旧11页初始诊断与处置方向草案齐全，本任务不提前封存；本任务关闭V6第一章/Q3前向后用，自身原因修订进入Task 19时登记`deferred/provisional`；
- [ ] 每名学生明确选择一类问题，不写含混“主要原因”；
- [ ] 指定质询组和其余听众均有同步分类、证据或疑问任务；
- [ ] 每轮抽取一项非指定组补充；
- [ ] 每名学生执行“保留/移动/改写/撤回”并保存前后；
- [ ] 第一章回看区分文本明写、合理推断、不能证明和现代延伸；
- [ ] 女子投入与支持缺失不承担男子失信和粗暴责任。
- [ ] 第一章初见产出与其他登记到Q3/回看的后用逐项核验，关闭相应`deferred`。

**验证：**

- [ ] 运行`--through question_3`全链验证；
- [ ] 因果图机器测试拒绝“女子投入→男子粗暴”等错误连线；
- [ ] 学生接收审查逐项核验非发言者任务和全员修订；
- [ ] 视觉审查确认V13/V17使用原文或关系图而非补写情节。

**依赖：** Checkpoint 4A
**预计涉及文件：** `scripts/meng_v6/audit/question_3.json`、`scripts/meng_v6/content/question_3.js`、相关测试快照
**规模：** M

## Task 18：重构婚姻圆桌S113—S116

**描述：** 将五个生活问题作为候选而非全班必答清单；每人择一准备，小组轮流表达并保留真实分歧，公开阶段接受原诗、归责和限度追问，再形成个人婚姻提醒。

**验收标准：**

- [ ] 旧4页初始诊断与处置方向草案齐全，本任务不提前封存；本任务关闭V6 Task 5主题谱后用，自身婚姻提醒进入Task 19时登记`deferred/provisional`；
- [ ] 五问不预制成必须全部出现的教师框架；
- [ ] 四人轮流发言，听者分别承担找依据、查归责、问限度；
- [ ] 每组保留一项分歧，公开后发生可见修订；
- [ ] 个人提醒与开头旧故事主题谱建立一处联系；
- [ ] Task 5中指向圆桌的主题谱`deferred`逐项核验真实调用并把G5转为`pass`，节点仍为`provisional`；
- [ ] 不要求学生披露私人关系或家庭经历。

**验证：**

- [ ] 运行`--through marriage_roundtable`全链验证；
- [ ] 检查教师总结只收束现场真实出现的材料，补充意见明确标为教师补充；
- [ ] 学生接收审查确认“圆桌”具有完整参与链。

**依赖：** Task 17
**预计涉及文件：** `scripts/meng_v6/audit/marriage_roundtable.json`、`scripts/meng_v6/content/marriage_roundtable.js`、相关测试快照
**规模：** M

### Checkpoint 4B：Q3、圆桌双审回归

- [ ] 两名独立审查者逐旧ID复核S102—S116初诊草案；旧页P0/P1/P2全部编号封存，只清除审计记录自身的漏项、缺证与未裁决分歧；随后生成覆盖完整、身份合规的双审封存；
- [ ] Q3和圆桌每页结构化自检完整；
- [ ] 第一章回看、责任/阻力听证和圆桌之间的输入、产出、听众任务、修订与后用闭合；
- [ ] Q3/圆桌新生成且指向Task 19收纳的`deferred`目标合法，不被误算为通过；
- [ ] 两名独立审查者覆盖S102—S116实际生成材料；
- [ ] P0/P1/P2清零；
- [ ] 现代延伸没有覆盖原诗，私人议题安全边界可执行。

## Task 19：重构知识收纳、终读和退出条S117—S127

**描述：** 先遮答检索，再核对故事、字词、语言形式、意象、人物关系与阅读方法；最后完整朗读，保存个人理解变化和仍保留的问题。

**验收标准：**

- [ ] 旧11页初始诊断与处置方向草案齐全，本任务不提前封存；
- [ ] 知识页不是看答案式重讲，检索和答案状态严格分开；
- [ ] 收纳覆盖故事结构、字词、四言、叠词/反复/对照/时间压缩、赋比兴、意象多解、人物与阅读方法；
- [ ] 个人初读停顿、转折句、生活处境句、原因判断和婚姻提醒均可回看；
- [ ] Task 15—18指向知识收纳的全部`deferred`逐项核验真实调用并把G5转为`pass`，节点仍为`provisional`；
- [ ] 终读用于把知识放回完整声音，退出条允许保留问题。
- [ ] 生成全课唯一`terminal_sink`事件：学生将退出条交至明确收集位置或保存在规定载体，教师课后据此诊断尚未解决的问题；`terminal_use`六字段及交付证据齐全，其余事件均`terminal_sink=false`。

**验证：**

- [ ] 运行`--through final`全链验证；
- [ ] 审计总表S001—S127全部无`pending`；
- [ ] S117—S127在本任务仍为待检查点双审的初诊草案；相应处置不得在有效封存哈希产生前伪标`closed`；
- [ ] S001—S116已封存旧页的处置关闭表无无法解释的状态，旧页初始失败仍原样保留；
- [ ] `structure_manifest`与现行审计、源码声明、课程数据可达图、独立`structure_assembly_snapshot`集合分别相等；G1—G6/G8/G9无`pending/deferred/fail`，G7恰为`pending_physical_build`，节点恰为`provisional`；
- [ ] `python scripts/validate_meng_v6_page_audit.py --mode freeze-candidate ...`通过；正式`release`验证只在Checkpoint 4完成末批封存和全量处置重验后运行；
- [ ] 旧ID覆盖集合、处理决定计数和删除/合并映射可复算。

**依赖：** Checkpoint 4B
**预计涉及文件：** `scripts/meng_v6/audit/knowledge_and_final.json`、`scripts/meng_v6/content/knowledge_and_final.js`、相关测试快照
**规模：** M

### Checkpoint 4：结构冻结

- [ ] 两名独立审查者逐旧ID复核S117—S127初诊草案；旧页P0/P1/P2全部编号封存，只清除审计记录自身的漏项、缺证与未裁决分歧；随后生成覆盖完整、身份合规的双审封存；至此所有旧ID均且只被一个有效封存覆盖；
- [ ] 旧S001—S127不可改写初始诊断、明确决定、决定专属证据和关闭记录齐全；
- [ ] 全部处置记录引用当前`effective_view_hash`重验；旧六门失败码与P0—P2缺陷集合逐项关闭；非删除关闭的目标字段/映射/现行审计节点哈希复算一致且原审查者复验仍有效，删除签名全局无重现；
- [ ] 所有现行阶段性`deferred`均依真实调用把G5转为`pass`，节点仍为`provisional`或经返工关闭；
- [ ] 所有学习事件输入、产出、保存和后用闭合；
- [ ] 除唯一、位于最大顺序且具真实交付/保存用途的退出条终端事件外，所有G5边严格后继且全局无环；终端事件缺交付证据时不得通过；
- [ ] `structure_manifest`与现行审计、源码声明节点、课程数据可达图、独立`structure_assembly_snapshot`的页面/事件集合分别完全相等，无源声明孤儿；该快照只含结构节点/计划归属/安全停点，此时不预测物理页、occurrence或student_visible；
- [ ] 全局反事实检查证明没有可以无损合并的现行页面/载体；
- [ ] 冻结V6事件顺序、模块安全停点、自然时长和新页码；
- [ ] 生成旧ID—决定—新ID完整映射；
- [ ] 双独立审查同意结构冻结后，才进入正式全量生成与生图。
- [ ] `python scripts/validate_meng_v6_page_audit.py --mode freeze ...`通过；最终物理PPTX清点留待Task 21/26/27和正式`release`模式。
- [ ] 生成`structure_audit_bundle.json`及其SHA-256；它只封存结构审计五组件（含作者登记有效视图），不预测物理occurrence或最终artifact清单。

### Phase 4：全量无图材料与跨文件回归

## Task 20：生成全量Markdown、审计、映射和课程快照

**描述：** 依据冻结数据生成设计标准、教学母版、学习单、逐页剧本、审计总表、旧新页码映射和课程快照。此任务只验证文本与数据链，不同时承担Office文件故障。

**验收标准：**

- [ ] S001—S127旧ID映射完整，所有V6现行ID完整、唯一且与冻结的`structure_manifest`集合相等；
- [ ] `structure_manifest`中的全部页面以及最终全部实际slide occurrence（含隐藏管理页）均有与其功能匹配的连续剧本或明确管理台词，并与PPTX notes逐出现双射；
- [ ] 教案、学习单、逐页剧本、审计表和课程快照的任务、时长、产出位置一致；
- [ ] 旧页处置无未关闭状态；结构阶段G1—G6/G8/G9无`pending`、`deferred`、`fail`或未裁决审查分歧，G7保持`pending_physical_build`且节点保持`provisional`；旧页初始失败证据完整保留；
- [ ] 学生前台禁词、预制答案和假共创命中为0；
- [ ] 所有文件仍位于`_v6_stage`。

**验证：**

- [ ] `node scripts/build_meng_v6_markdown.js --mode freeze --out .../_v6_stage`
- [ ] `python scripts/validate_meng_v6_page_audit.py --mode freeze ...`
- [ ] `python scripts/validate_meng_v6_lesson_package.py --mode freeze --formats data,markdown ...`
- [ ] 文本、页码、事件与产出引用的全量一致性测试通过。

**依赖：** Checkpoint 4
**预计涉及文件：** V6 Markdown构建器与`_v6_stage`中的Markdown、JSON、映射
**规模：** M

## Task 21：生成全量无图PPTX并逐页验证视觉合同

**描述：** 生成完整母版和所有模块PPTX的无正式插图候选；三张原型只作为布局起点，本任务对每一张实际句群页重新验证字号、坐标、信息块和主视觉。

**验收标准：**

- [ ] 完整母版与模块课件的可见文字、备注、任务、新页码一致；
- [ ] 全量视觉合同逐页输出`slide_id/current_text_pt/chapter_track_pt/chapter_code_pt/block_count/primary_visual_duty`；
- [ ] 每张句群页当前原句≥38pt或有记录的长句例外≥34pt，章内轨道≥22pt，六章位置码≥18pt且始终存在；
- [ ] 每页主要信息块≤4，`primary_visual_duty`唯一，没有用缩字容纳真实内容；
- [ ] 验证器同时核对实际PPTX XML和生成时布局清单；任何例外都有页ID、原因和300 dpi人工复验；
- [ ] `warnIfSlideHasOverlaps`与`warnIfSlideElementsOutOfBounds`意外警告为0；
- [ ] 每个PPTX通过Office结构验证、文本/备注提取和PDF转换。
- [ ] 为完整母版和每个模块生成候选`render_manifest`：`structure_audit_bundle_sha256`、源路径/SHA-256、页数、页ID—物理页码有序双射及哈希、实测逐artifact occurrence/候选入口、资产清单哈希、PDF路径/哈希、渲染器版本和参数、联系表/单页图路径及哈希齐全；物理页、映射和声明页数相等。最终`release_audit_bundle_sha256`在Task 27冻结实际artifact清单后回填并重验，不得预测。

**验证：**

- [ ] 无图构建命令：`node scripts/build_meng_v6_pptx.js --mode release --assets none --out .../_v6_stage/no_assets`
- [ ] `python -m unittest tests/test_validate_meng_v6_pptx_visual_contract.py`
- [ ] 通用验证命令：`python scripts/validate_meng_v6_pptx_visual_contract.py --pptx-dir <target_dir> --layout-manifest <target_layout_manifest> --assets-manifest <none_or_approved_manifest>`；验证器不得重建PPTX；
- [ ] 完整母版和每个模块均生成逐页合同结果，失败数为0；
- [ ] 150 dpi只能生成节奏概览；全量页面按每批8—12页制作可读联系表，每张子图不小于1600×900像素，并逐页登记审查状态；
- [ ] 最长文字、文本比较、活动、跨页整读、模块首尾全部另输出300 dpi单页图。
- [ ] 修改任一源PPTX、页码映射、资产清单或渲染参数的测试样本后，相关逐页视觉状态自动失效为`pending`，不能继续通过验证。

**依赖：** Task 20
**预计涉及文件：** V6 PPTX构建器、视觉合同验证器与测试、无图PPTX、布局清单、逐页视觉状态表
**规模：** M

## Task 22：生成三份DOCX并完成XML与逐页打印审查

**描述：** 生成教学母版、学习单和逐页无生试讲稿DOCX；用XML合同验证结构，用全量PDF页面审查分页、表格和打印可用性。

**验收标准：**

- [ ] 三份DOCX与对应Markdown正文一致；
- [ ] 每个section的A4尺寸、页边距、页眉页脚和分页设置一致；
- [ ] 表格使用DXA宽度，表总宽等于各列宽之和，每个单元格宽度匹配对应列，百分比表宽为0；
- [ ] 列表使用真实编号定义，不使用Unicode项目符号模拟；
- [ ] 每份DOCX通过Office结构验证和PDF转换；
- [ ] 三份DOCX每一页进入可读分批联系表并有逐页状态；
- [ ] 表格密集页、分页交界、页眉页脚、学习单书写区另输出300 dpi单页图；
- [ ] 无孤立标题、跨页表头丢失、内容裁切、书写区不足或打印越界。
- [ ] 每份DOCX的候选`render_manifest`绑定`structure_audit_bundle_sha256`、源路径/SHA-256、页数、`artifact_id—doc_page_index`有序清点及哈希、可选内容引用、PDF路径/哈希、渲染器版本和参数、全部联系表/单页图路径与SHA-256；不分配Nxxx。Task 27冻结`document_page_inventory`后绑定final bundle并重验；任一bundle、源文件或证据变化使相关状态失效。

**验证：**

- [ ] `node scripts/build_meng_v6_docx.js --mode release --out .../_v6_stage`
- [ ] `python -m unittest tests/test_validate_meng_v6_docx_contract.py`
- [ ] `python scripts/validate_meng_v6_docx_contract.py .../_v6_stage/*.docx`
- [ ] 对三份DOCX逐一运行Office验证、PDF转换、分批联系表与300 dpi关键单页审查。
- [ ] 用修改源DOCX、页码映射和渲染参数的反例验证旧逐页状态不能复用。

**依赖：** Task 20
**预计涉及文件：** V6 DOCX构建器、XML合同验证器与测试、三份DOCX及逐页视觉状态表
**规模：** M

## Task 23：执行无图版本跨文件一致性回归

**描述：** 把Task 20—22的候选合并验证，避免各格式单独通过却在页码、任务、时间、备注或学习证据上分叉。

**验收标准：**

- [ ] Markdown、PPTX、DOCX、课程快照和页码映射的页面/事件集合一致；
- [ ] PPTX备注与独立逐页剧本逐页一致；
- [ ] 学习单的所有必写位置均有课堂生成和后用；
- [ ] 完整母版与模块PPTX无缺页、重页、错序或备注差异；
- [ ] 修复任一格式后重新运行相关格式和跨文件回归。

**验证：**

- [ ] `python scripts/validate_meng_v6_lesson_package.py --mode freeze --formats all --assets none ...`
- [ ] `python -m unittest tests/test_validate_meng_v6_lesson_package.py`
- [ ] V5基线清单再次验证一致。

**依赖：** Tasks 21、22
**预计涉及文件：** 跨文件验证器、测试和无图版本回归报告
**规模：** S

### Phase 5：统一角色、分批插图与含图版重建

## Task 24：冻结W01/M01角色设定与插图任务卡

**描述：** 按规格制作W01-T/A/B/C、M01-T/A/B/C多视角设定卡、同框比例、固定色值、服装/发式/道具编号和V01—V18调用矩阵，并建立受审批与哈希保护的`scene_registry/prop_registry`。先审人物、场景和道具设定，不直接生成场景。

**验收标准：**

- [ ] 每个角色阶段有正面、侧面、背面、三分之四视图和同框比例；
- [ ] 总角版本与青年版本严格区分；
- [ ] 每项候选资产绑定页面、角色版本、服装、发式、道具、时序、相邻场景和无图替代方案；
- [ ] 每项插图任务卡强制填写`source_line_refs/student_action/primary_visual_duty/unique_visual_function/deletion_loss/next_use_refs/no_image_alternative`；`next_use_refs`只能指向严格后继页面、事件或明确会说出的notes台词，并须在目标中找到对该资产或其可观察信息的反向引用；
- [ ] 相邻页复用同一资产时逐项写明绑定原诗或学生理解变化的新增功能；删除后无具体学习损失、无图版同样快且同样准确、后续从未观察/比较/指认/引用，或只能说“美观”的资产必须改为`no_image_required`或`rejected`；
- [ ] V13、V17、V18标为非人物图默认方案；
- [ ] V01—V18每项均为`approved_to_generate`、`no_image_required`或`rejected`；
- [ ] 每张图的`scene_id`必须外键指向已批准场景；`prop_ids`可为空，但必须说明`no_prop_reason`，不得伪造`PROP_NONE`；
- [ ] 场景冻结季节、时刻、天气、地平线、地貌、建筑、镜头尺度、视线轴和光源；相邻场景联系表自动输出脸型、发式、服装、人物比例、左右关系、视线轴、镜头尺度、光源、场景和道具的逐邻页差异，每项变化必须有绑定原诗或唯一页面功能的`allowed_difference_reason`，无理由变化即失败；
- [ ] 角色、场景、道具登记表均记录参考资产SHA-256、作者集合和至少两名独立批准者；两名批准者彼此不同，且均与候选资产、参考资产和全部上游登记表作者并集不相交；登记表、任务卡、参考资产、作者集合或相邻联系表任一变化均使批准失效，必须重新独立批准、跨页盲认和入页A/B测试；
- [ ] 学生接收与视觉审查者均通过角色设定和任务卡。

**验证：**

- [ ] `python -m unittest tests/test_validate_meng_v6_visual_assets.py`
- [ ] 每个连续性字段、V13/V17/V18限制、`no_image_required`误生成、角色版本冲突、相邻差异无`allowed_difference_reason`、登记表/任务卡/参考资产/作者集合/联系表漂移、一名批准者、自批、批准者属于参考资产作者、作者缺失和参考SHA漂移至少各有一个失败测试；
- [ ] 教学功能负向fixtures至少覆盖任务卡缺少`source_line_refs/student_action/primary_visual_duty/unique_visual_function/deletion_loss/next_use_refs/no_image_alternative`任一项、next-use不存在/不后继/目标无反向调用、删除后A版同效、相邻页重复无新增功能和只写“美观”；
- [ ] `python scripts/validate_meng_v6_visual_assets.py --mode cards .../_v6_stage/assets/manifest.json`
- [ ] 角色版本—服装—发式—场景矩阵无空引用和冲突。

**依赖：** Task 23
**预计涉及文件：** 视觉资产验证器与测试、`_v6_stage/assets/manifest.json`、角色设定卡
**规模：** M

## Task 25：按每批最多四项生成和验收被批准插图

**描述：** 将`approved_to_generate`资产按页面功能和叙事时序分批，每批最多四项。每批独立完成生成、无图/有图对照、实际入页渲染、至少四名盲化观察者三秒测试、修复和复验，再进入下一批。

**验收标准：**

- [ ] 不生成`no_image_required`和`rejected`场景；
- [ ] 每批不超过四项且有独立批次清单与关闭记录；
- [ ] 人物图严格调用设定图和所有连续性字段；
- [ ] 至少四名未看提示词的观察者完成同一三秒任务，分别记录原诗/任务识别、动作/空间/意象判断、置信度、完成时间和新增误读；
- [ ] 每个`observer_id`必须通过资格核验：不属于该候选图、提示词、任务卡、参考图和入页构建器的作者或生成参与者集合；记录`observer_eligibility/role_provenance/reviewed_author_ids`，生成者或提示词作者充当观察者时测试失败；
- [ ] 观察者用预先登记的随机种子和分层平衡规则分入A先/B先组；最小四人时固定2人A先、2人B先，人数更多时两臂各至少2人且人数差不超过1；每名观察者首次判断只看一个版本，记录`observer_id/group/first_version/order/assignment_seed/assignment_rule`，主比较使用未受另一版本记忆影响的首次结果；若再看另一版，只能作为次级配对证据并单独标记；缺臂、任一臂少于2人或失衡均失败；
- [ ] B版只有在原诗/任务识别率不低于A版、没有新增越界误读，且核心视觉准确率提高或中位完成时间缩短时才可通过；四名观察者均不得把插图当作标准答案；
- [ ] 每批及全部场景完成后生成按叙事顺序排列、隐藏场景ID和提示词的跨页联系表；独立观察者逐图判断人物身份、年龄阶段和诗中事实边界，任一人物/阶段误认或把推断当事实即整项退回，修复后重做完整跨页盲认；
- [ ] 任一推断被说成事实、人物漂移或图片抢夺原诗时立即否决；
- [ ] 每项通过资产具有同源无图/有图对照、实际入页尺寸、三秒记录和修复复验；
- [ ] 每项资产另由独立视觉审查者在实际入页渲染上逐项签署`style_coherence/composition_balance/color_harmony/drawing_finish/artifact_integrity`；五项须分别有证据且全部通过，覆盖冻结画风、构图与留白、固定色卡、造型完成度，以及手部/肢体/五官/边缘/透视/重复纹理/伪文字等生成瑕疵；教学收益与审美质量互不补偿；
- [ ] 每项批准资产生成不可拆的`asset_evidence_bundle_sha256`，固定绑定A/B整页渲染、课程数据SHA-256、生成器源码SHA-256/版本、布局manifest SHA-256、A/B非图片区结构指纹（除插图槽从空到有图这一项变量外，文字、字号、位置、色彩、背景、其他图形和版式必须相同）、原始观察记录、观察者资格谱系、分组/顺序与随机种子、评分派生结果、跨页联系表与盲认记录、双批准记录、资产文件路径/SHA-256和页面绑定；批准资产清单必须引用该证据包哈希；
- [ ] 证据包另冻结`tested_b_full_visual_state`，至少逐字段保存图片文件SHA-256、图片槽`x/y/w/h`、裁切四边、蒙版/裁切几何、透明度、旋转/翻转、描边、阴影/发光/重着色等效果、相对全部页面元素的`z-order`、非图片区结构指纹、渲染器/版本/参数，以及去元数据并规范到固定色彩空间和像素尺寸后的`normalized_full_page_render_sha256`；只保存原图SHA或只保存“有图”布尔值不得批准；
- [ ] 所有批次完成后，批准资产清单固定文件路径、SHA-256、页面绑定和`asset_evidence_bundle_sha256`；只改资格、分组、答案、时间、评分、联系表、盲认或批准记录中的任一字段，均使批准失效并阻断入页/发布，必须重测重审。

**验证：**

- [ ] 每批运行`python scripts/validate_meng_v6_visual_assets.py --mode batch --batch-id ...`；
- [ ] 每批由视觉审查者明确P0/P1/P2清零后才继续；观察者资格、随机/交叉顺序、单页A/B与跨页盲认记录缺一不可；
- [ ] 负向测试覆盖4:0、3:1、单样本臂、缺随机种子，以及只篡改观察资格/原始回答/完成时间/派生评分/跨页盲认/批准记录但资产图片不变的情况；
- [ ] 审美负向fixtures至少覆盖风格漂移、色彩失衡、构图拥挤或失衡、造型完成度不足、手部/边缘/透视/重复纹理/伪文字瑕疵，以及技术字段和三秒收益全部合格但任一审美项失败；
- [ ] 全部批次结束运行`--mode release`，批准清单与磁盘资产一一对应。

**依赖：** Task 24
**预计涉及文件：** `_v6_stage/assets/approved/`、批次任务卡、三秒测试与缺陷关闭记录
**规模：** M（每个实际批次为S）

## Task 26：由批准资产清单同源重建并全量复验最终PPTX

**描述：** 禁止手工粘贴图片。把批准资产清单写入共享课程数据，由同一生成器重新构建完整母版和全部模块PPTX，并对最终含图版重新执行所有结构、文本、备注、页码和视觉检查。

**验收标准：**

- [ ] 每张入页图片都来自批准资产清单，未批准资产引用为0；
- [ ] 构建器逐资产复算`asset_evidence_bundle_sha256`并把它纳入批准资产清单总哈希；任何证据包缺失或漂移都在生成PPTX前失败；
- [ ] Task 26从最终PPTX/XML和标准化整页渲染中为每个实际含图`occurrence`独立提取`final_full_visual_state`，与对应证据包的`tested_b_full_visual_state`逐字段比较；图片文件SHA-256、图片槽`x/y/w/h`、裁切、蒙版、透明度、旋转/翻转、描边、效果、`z-order`、非图片区结构指纹和`normalized_full_page_render_sha256`必须全部相等；
- [ ] 标题、任务、字号、位置、色彩、背景、其他图形、布局manifest、课程数据、生成器、图片裁切/尺寸/透明度/旋转/层级/效果任一变化，即使图片文件不变，也使该`occurrence`的A/B批准失效并要求按最终物理状态完成完整盲化A/B；
- [ ] 同一页面出现在完整母版和一个或多个模块PPTX时逐`occurrence`核验。只有完整视觉状态及标准化整页渲染完全一致的多个`occurrence`才可引用同一测试；任一字段或像素哈希不等价，必须为不等价`occurrence`重新测试，不得按页面ID或资产ID去重复用；
- [ ] 无图/有图对照由同一课程数据和生成器版本产生；
- [ ] 完整母版及所有模块PPTX重新通过Office结构、文本/备注、页码、重叠、越界和视觉合同；
- [ ] 所有最终学生可见页重新渲染，不沿用无图Task 21的视觉合格证；
- [ ] 全量页面按每批8—12页可读审查并逐页登记；所有含图页另有300 dpi单页审查；
- [ ] 含图版修复后重新构建完整母版和全部模块，不进行局部手工修改。
- [ ] 最终含图版生成新的`render_manifest`和逐页`review_evidence`；它们绑定最终源文件、批准资产清单总哈希、逐资产`asset_evidence_bundle_sha256`和最终渲染的SHA-256，不沿用Task 21无图版或Task 25候选图的视觉状态。
- [ ] 对最终含图PPTX正文/notes/XML/资产关系、全部模块切片、DOCX/学习单和渲染结果重跑text/asset/layout/event删除签名扫描；删除视觉换资产ID或后期插图重现为0。

**验证：**

- [ ] `node scripts/build_meng_v6_pptx.js --mode release --assets .../_v6_stage/assets/approved_manifest.json --out .../_v6_stage/final`
- [ ] 不运行Task 21的无图构建命令；只对`_v6_stage/final`复用Task 21的通用验证器、Office/文本/备注/页码检查和全量渲染步骤，并显式传入`approved_manifest.json`；
- [ ] `python scripts/validate_meng_v6_visual_assets.py --mode binding --pptx-dir .../_v6_stage/final ...`
- [ ] 最终完整母版和模块PPTX的图片引用集合与批准资产绑定集合完全相等；Task 26的命令记录中不得出现`--assets none`；
- [ ] 负向测试分别只修改最终含图页的标题、任务、字号、位置、色彩、背景、其他图形、布局manifest、生成器源码、图片裁切、图片槽尺寸/位置、透明度、旋转/翻转、`z-order`、描边或滤镜/效果而保持图片文件不变，`final_full_visual_state`或标准化整页渲染必须失配并阻断发布；
- [ ] 负向测试另覆盖完整母版与模块页共用同一页面ID和图片资产、但只在一个`occurrence`改变裁切/主题/字体替换的情况；验证器必须拒绝共享测试并要求该`occurrence`重测；
- [ ] 视觉审查者确认含图最终版P0/P1/P2为0。

**依赖：** Task 25
**预计涉及文件：** 共享课程数据中的资产绑定、最终含图PPTX、全量渲染与逐页状态表
**规模：** M

### Checkpoint 5：材料和视觉候选

- [ ] Markdown、审计、映射和课程快照通过；
- [ ] 三份DOCX结构、XML合同和逐页打印审查通过；
- [ ] 最终含图完整/模块PPTX全量重建和逐页复验通过；
- [ ] 角色设定无漂移，只有具有理解收益的图片进入课件；
- [ ] 全量备注、页码和课堂语言一致；
- [ ] V5基线仍未被覆盖。

### Phase 6：双审闭环、全量放行与旧版回收

## Task 27：完成学生接收和视觉双独立审查闭环

**描述：** 先从Task 26最终PPTX实测生成`slide_occurrence_inventory`，从Task 22最终DOCX实测生成`document_page_inventory`，再生成`release_artifact_manifest`、教师话语/学习单/板书/音频等`other_channel_inventory`和候选`physical_release_gate_overlay`。候选overlay必须先由至少两名未参与物理构建、且与目标和全部上游作者并集不相交的审查者逐节点审查G7；双审通过后才冻结overlay，机械派生`effective_release_audit/current_manifest`并生成“审查前”`release_audit_bundle_sha256`。随后再进行全量学生接收和视觉审查，结果只写入独立哈希链式`release_review_ledger`，不反写结构审计或overlay。学生接收审查既覆盖每个投影slide，也独立覆盖每个完整学习事件；视觉审查不得只依赖概览联系表，而要覆盖每一页的可读渲染。

**验收标准：**

- [ ] 冻结`final_review_assignment`：恰有一个`student_reception_reviewer_id`和一个`visual_execution_reviewer_id`，两者必须不同、角色不可互换，并分别与其审查对象及全部上游作者并集不相交；前者只能签署`student_occurrence/student_event`，后者只能签署`visual_slide/visual_document_page`；
- [ ] 学生接收桌面模拟覆盖由`slide_occurrence_inventory`和冻结官方放映入口推导出的所有`projected=true` slide及全部跨页事件；不得以母版隐藏或手填`student_visible=false`排除计划投影路径中的页面；字段使用`simulated_* / possible_*`，不声称学生已实际接收或理解；
- [ ] `student_event_review`的event_id集合严格等于全部现行`learning_event`集合；每条绑定最终bundle、按序载体occurrence/其他渠道，并复核学生看/听/做、事件`inputs/actions/artifacts/observable_change/next_uses/fallback_routes/gate_8`，逐项保存完整11类反例的适用性与理由、`counterexample_run_refs`、事件整体出口/作品/返回主线；载体页各自有出口不能替代跨载体/跨渠道事件反例；
- [ ] `other_channel_inventory`逐项记录渠道类型、源文件/字段/内容哈希、脚本暴露顺序、owner event、`exposure_status=scripted|prepared`及证据：教师台词、学习单字段和音频按`scripted`核验，卡片、磁贴、空板、场地、保存/拍照备份按`prepared`核验；event review引用须双向一致，教师未说出的备注不得充当模拟听见证据，未备妥实体不得冒充`prepared`；`observed`只允许真实试教后另行追加且不作为本轮硬门；
- [ ] `student_occurrence_review`按辨别字段合同记录occurrence/artifact/物理slide、模拟看见/听见/参加活动、可能理解/误解和可能收获；其有序键集合恰等于全部`projected=true` slide occurrences，隐藏非投影页不混入接收集合；
- [ ] 每个页面的独立审查记录必须逐项填写十项且不得合并省略：学生第一眼看见什么；教师在精确时点说了什么；不同角色分别做什么及何时结束；完整最少反例集逐项适用性、理由及适用反例出口；本页调用哪句原文或哪项前页作品；形成什么学生作品及保存在哪里；页前页后有什么可观察变化；谁按什么判据反馈、学生怎样可见修订；后续哪一页/事件实际读取；当前P0/P1/P2/P3、证据、最小修复与`Pass/Veto`；
- [ ] 完整母版和每个模块PPTX的每一页都有视觉审查状态；
- [ ] 每条`visual_slide`审查记录必填`occurrence_ref/render_ref/primary_visual_duty_observed/first_visual/text_readability/hierarchy/contrast/spacing/overlap/out_of_bounds/asset_text_boundary/character_scene_prop_continuity/cross_channel_physical_consistency/issue_refs/status/evidence_refs`；所有判断必须定位到当前渲染或物理渠道，不允许只写总体`pass`；
- [ ] 含图`visual_slide`另必填并复核`source_line_refs/student_action_observed/unique_visual_function/deletion_loss/next_use_refs/next_use_reverse_refs/no_image_alternative_result/style_coherence/composition_balance/color_harmony/drawing_finish/artifact_integrity`；后用不存在、不后继、目标未反向调用、无图同效、邻页重复无新增功能或任一审美项不通过均为`Veto`；
- [ ] 每条`visual_document_page`审查记录必填`artifact_id/doc_page_index/render_ref/crop/margin/header_footer/table_integrity/page_break/writing_space/printability/issue_refs/status/evidence_refs`；学习单须额外核对书写区域，讲稿须核对分页后连续可读；任一字段缺失、无渲染引用或只写总体`pass`即失败；
- [ ] 全量页面以每批8—12页、每张子图≥1600×900像素的可读联系表审查；
- [ ] 最长文字、比较、活动、跨页整读、模块首尾和所有含图页具有300 dpi单页审查；
- [ ] 三份DOCX的每一页均有视觉状态，表格密集、分页交界、页眉页脚和书写区有300 dpi单页审查；
- [ ] 审查证据采用按`review_type`区分的联合类型：`student_occurrence/visual_slide`绑定单一PPTX slide；`visual_document_page`绑定DOCX artifact+doc page index；`student_event`绑定event及多个按序occurrence/其他渠道，可含多个source/render refs，不强制伪造单一页码；每条都必须保存`release_audit_bundle_sha256`、`authorship_registry_effective_sha256`、机械导出的`reviewed_author_ids`、单一`reviewer_id`、时间、状态和缺陷，并验证审查者不在上游作者并集中；
- [ ] 每个缺陷定位到页ID/事件ID/资产ID并标P0—P3；
- [ ] P0/P1/P2全部关闭；
- [ ] Task 27最终缺陷与关闭只进入`release_review_ledger`，不得回写已在structure bundle中的`current_release_audit.review_status`；回写尝试自动失败，避免哈希循环和双状态源；
- [ ] `physical_release_gate_overlay`逐节点绑定冻结结构bundle、物理候选源和作者登记有效视图的SHA-256，并保存至少两名独立`reviewer_ids`、机械导出的`reviewed_author_ids`、逐审查者裁决、`reviewed_at`和证据；审查者彼此不同且均不在目标及全部上游作者并集中。只有双审通过且审查时间不晚于overlay冻结时间，G7才可转为`pass`；分歧按证据复核，仍不一致则第三方裁决；缺审查者、自批、作者谱系漂移或先冻结后审查均失败；
- [ ] G7物理事实若推翻其他结构门，只能在overlay标`invalidated`并阻断发布，不得覆盖结构记录；候选overlay未通过独立G7审查时不得生成final bundle或`effective_release_status=final`；
- [ ] `effective_release_audit`只能由结构审计与overlay机械派生；overlay缺节点、重复节点、哈希过期、作者登记变化或试图改写结构门时失败；
- [ ] 每次物理候选重建建立不可分叉的`release_iteration`链，记录`release_iteration_id/previous_release_bundle_sha256/current_candidate_sha256s/rebuild_reason`；重建后必须重新生成全部物理inventory、重新进行G7双审、冻结新overlay、生成新final bundle，并对全部受影响的occurrence/event/visual记录建立绑定新bundle的新审查，不得复用旧review或跨bundle supersede；
- [ ] canonical `release_iteration`链及其链头/链尾哈希作为`release_review_ledger.release_iteration_chain`固定字段进入既有ledger组件，不新增attestation顶层组件；按`release_iteration_id`和唯一前驱顺序哈希，删中间节点、改顺序或分叉均失败；
- [ ] ledger审查记录含review ID/revision/唯一前驱/supersedes、`authorship_registry_effective_sha256`、`source_state_sha256`、`reviewed_author_ids`和`reviewer_id`，按`bundle+review_type+object_key`机械生成唯一有效链尾；作者不相交验证失败、作者登记漂移、source state复算不等、断链、分叉、重复当前状态或跨bundle替代均失败；完整原账与有效视图均保留；
- [ ] 四类`source_state_sha256`按规格固定输入独立canonical派生：`student_occurrence`绑定occurrence、源PPTX/slide XML/notes/关系/媒体、render与实际暴露渠道；`student_event`绑定event固定字段、有序carrier原始源组件、有序渠道和scripted/prepared证据；`visual_slide`绑定occurrence、源PPTX/slide物理内容、render/layout及含图资产完整证据；`visual_document_page`绑定doc inventory、源DOCX、固定PDF单页/图像、render参数和content refs源区域；任何组件缺失或变化均改变哈希；
- [ ] `source_state_sha256`不包含review结论、缺陷、时间或自报哈希；对象键、语义有序数组、集合数组和路径遵守统一canonical规则。prior/carried的from/to source只能逐字复制已由验证器从原始对象复算通过的新旧review值，不能互相自证；
- [ ] `effective_release_review_view`从最终物理清单机械派生四类预期键集合：全部`projected=true`的`student_occurrence`、全部现行事件的`student_event`、全部PPTX物理页的`visual_slide`和全部DOCX物理页的`visual_document_page`；每个预期键在当前bundle内必须恰有一个有效链尾且`status=Pass`，任何`Veto/pending/blocked_for_adjudication`、缺项或多链尾均阻断总评与发布；
- [ ] 缺陷关闭不得自动翻转review状态；复审链的`revision/supersedes_review_id`严格限制在同一bundle内：只有final bundle受保护源状态完全未变时，原审查者才可追加同bundle新`Pass` revision并supersede旧`Veto`；
- [ ] 修复引起源、候选或受保护物理状态变化时必须生成新bundle；新bundle针对每个键从`revision=1, supersedes_review_id=null`开链，以不参与当前链尾选择的`prior_bundle_review_ref`指向旧bundle `Veto`，并绑定当前bundle/源、有效closure、原审查者身份核对、所属模块回归和整课回归证据；`release_iteration.carried_reviews`机械保存跨bundle历史，禁止跨bundle supersede；旧bundle的`Pass`不能替代当前bundle的`Veto`或待审状态；
- [ ] `prior_bundle_review_ref`固定为`release_audit_bundle_sha256/review_id/review_type/object_key/reviewer_id/status/source_state_sha256`且`status=Veto`；必须指向唯一iteration祖先链上同一`review_type+object_key+reviewer_id`最近的有效Veto链尾，当前新Pass reviewer必须相同；跳过更近同键Veto、非祖先/旁支、错键/错类型/错审查者或非Veto状态均失败；
- [ ] `release_iteration.carried_reviews[]`每行固定为`from_bundle_sha256/from_review_id/to_bundle_sha256/to_review_id/review_type/object_key/reviewer_id/from_source_state_sha256/to_source_state_sha256/closure_ids`；from逐字段匹配旧不可变账和prior ref，to逐字段匹配当前新Pass，closure_ids非空且均在当前源状态有效；
- [ ] `carried_reviews`按`from_bundle_sha256+from_review_id+to_bundle_sha256+to_review_id`稳定复合键canonical排序并纳入`release_iteration_chain`节点哈希；当前bundle全部带prior ref的新Pass集合与本iteration carried row的to集合双向严格相等，from/to各自唯一，禁止漏项、额外、重复、分叉或ref—row不对称；验证器从祖先ledger和当前ledger独立重算；
- [ ] 不可删除`release_defect_registry`与追加式关闭记录逐项关联；P0—P2发现集合必须等于恰有一条仍匹配当前源状态的有效关闭集合，漏关、伪`open=0`、重复/无源关闭、删除旧发现或修复后源变更均失败；P3进入试教观察项；
- [ ] 新`release_iteration`必须逐ID把全部历史bundle的缺陷登记迁入`carried_defects`，保留原`defect_id/severity/review_record_ref/claim/evidence/reviewer/source_state`且不可改名、删除或降级；关闭只能在新source state上追加，由原发现审查者复验。最终缺陷汇总覆盖整条iteration链的并集，并要求每个P0—P2恰有一条匹配最终source state的有效关闭；
- [ ] canonical跨迭代`carried_defects`有效视图及其哈希作为`final_defect_closure_summary.carried_defects_effective_view`固定字段进入既有缺陷汇总组件，不新增attestation顶层组件；ID集合稳定排序，链头/链尾必须与ledger中的iteration链相互校验；
- [ ] 完整不可变review记录中`defect_ids`并集严格等于registry ID集合，逐ID双向恰一关联且severity/object/evidence/reviewer一致；记录漏登记、孤儿registry、错误反指或同ID多registry均失败；
- [ ] 修复页由原审查者复验，所属模块和跨模块路径完成回归；
- [ ] 审查分歧全部调用Task 2通用`adjudication_record`：先保存双方各一次只围绕证据的复核；仍不一致时才由身份和盲态均合规的第三人裁决，裁决记录进入ledger并绑定final bundle；
- [ ] 两个固定角色的总`Pass`只能由各自权限范围内全部当前有效链尾均为`Pass`机械派生，不是独立可写字段；同一人兼任两类、角色串写、任一角色漏覆盖、任一局部链尾非`Pass`均阻断放行；第三方裁决者只裁决具体分歧，不取代两个主审角色的全量职责；
- [ ] 至少一轮完整“发现—修复—复验—模块回归—整课回归”有永久记录。

**验证：**

- [ ] PPTX slide状态有序多重集与实际slide一一双射，每张slide恰有一个合法、文件内唯一的Nxxx，页数/映射数/声明数相等；DOCX视觉状态另与`document_page_inventory`一一对应，只用artifact ID+doc page index，不要求Nxxx；
- [ ] 事件接收状态表与现行学习事件集合严格相等；缺事件记录、漏载体、载体乱序或用逐页记录冒充事件记录均失败；
- [ ] occurrence接收记录有序多重集严格等于官方`projected=true` slide出现；漏一项、额外隐藏项、跨artifact复用记录，或逐页十项记录中任一项缺失、合并为总体印象、无精确证据均失败；视觉记录分别覆盖全部PPTX slide与DOCX页面，不与接收集合混用；
- [ ] 逐页十项记录的负向fixtures至少覆盖：无精确听见时点、角色无结束条件、无边界出口、无原文/前页作品调用、作品无保存位置、无前后变化、无反馈判据、无可见修订、无后页读取、缺最小修复或只写总体`Pass`；
- [ ] 事件G8负向fixtures至少覆盖：事件只有理想路径、各载体页局部可完成但切换时断裂、`scripted/prepared`渠道缺失、事件统一填`na`或`not_applicable`无理由、无`counterexample_run_refs`或反例无法返回主线；
- [ ] G7 overlay负向fixtures至少覆盖：单一审查者、审查者与上游作者重合、`reviewed_author_ids`漏作者、作者登记漂移、审查时间晚于overlay冻结、双审分歧未经裁决和候选未审即派生final；
- [ ] 视觉记录负向fixtures至少覆盖：`visual_slide`缺第一视觉/远距可读/层级/对比/间距/重叠越界/图文边界/连续性/跨渠道一致性之一，`visual_document_page`缺裁切/边距/页眉页脚/表格/分页/书写区/打印性之一，以及两类记录无`render_ref`或只填总体`pass`；
- [ ] 含图视觉记录负向fixtures另覆盖缺少唯一教学功能/删除损失/后用及反向调用/无图替代结论/任一审美字段，或相邻重复图无新增功能；
- [ ] 局部状态负向fixtures至少覆盖：局部`Veto`但缺陷已关且角色总Pass、局部`pending`、局部`blocked_for_adjudication`、同bundle已关缺陷但无superseding Pass、旧bundle Pass代替当前Veto，以及角色总Pass被手填而非从全部局部Pass派生；
- [ ] 跨bundle复审正例覆盖“祖先链最近同键旧bundle Veto→修复重建→同一原审查者签新bundle revision=1 Pass＋固定prior ref＋双向等价carried row”；负例覆盖新bundle revision>1、新bundle supersedes旧bundle review、错object_key/type/reviewer/status/source、非祖先/旁支bundle、跳过更近Veto、缺/额外/重复/分叉carried row、ref—row不对称、历史引用参与当前链尾、closure_ids空/失效、缺当前bundle/source/模块或整课回归证据；
- [ ] source-state负向fixtures按四类分别覆盖review缺哈希、自报错哈希、只改任一构成组件仍沿用旧哈希、语义有序数组换序、集合数组仅书写顺序变化、prior/carried source与所指已验证review不等，以及用prior/carried相互引用冒充原始对象重算；
- [ ] release iteration负向fixtures至少覆盖：重建后复用旧review、跨bundle supersede、漏迁旧defect、改变旧ID/严重度、只重审修复页而不重建inventory/G7 overlay/final bundle，以及新registry手填`open=0`；
- [ ] 最终角色负向fixtures至少覆盖：同一审查者兼任学生接收与视觉、把`student_event`交视觉角色签署、把`visual_slide`交接收角色签署、某角色漏一项对象、任一角色未明确总`Pass`或角色作者谱系漂移；
- [ ] 从最终PPTX/DOCX/讲稿/学习单实测生成`physical_assembly_snapshot`，冻结`release_artifact_manifest`、`slide_occurrence_inventory`、`document_page_inventory`、`other_channel_inventory`、`physical_release_gate_overlay`和官方入口，机械派生`effective_release_audit/current_manifest`并生成审查前`release_audit_bundle_sha256`；`render_manifest`中的final bundle、源文件、批准资产清单、PDF、分批联系表、300 dpi单页图、页数和各自物理清点哈希全部存在且可复算；所有`review_evidence`引用的哈希与当前最终候选完全一致；
- [ ] final bundle中的批准资产清单间接但完整地绑定每项`asset_evidence_bundle_sha256`；验证器复算其A/B渲染、`tested_b_full_visual_state`、观察原始记录、资格、分组、评分、跨页盲认和批准记录，并逐实际含图`occurrence`复算`final_full_visual_state`及标准化整页渲染；任一改变、任一不等价或任一未重测`occurrence`即产生新final bundle并使旧审查全部失效；
- [ ] 验证器独立重算结构/最终bundle；键书写顺序变化不改变哈希，任一非排除字段或语义顺序变化改变哈希，组件缺失/替换失败；
- [ ] 负向篡改测试证明只改`current_manifest/current_release_audit`形成的新bundle、作者登记有效视图/上游作者集合、源文件、批准资产清单、页码映射、官方入口、渲染器版本/参数或任一被审图哈希时，相关状态立即失效为`pending`并阻断放行；
- [ ] 审查报告机器扫描确认`open_p0=open_p1=open_p2=0`；
- [ ] 所有修复提交均能由缺陷ID追溯；
- [ ] 修复后重新运行页面审计、课程合同、Office/XML合同、最终PPTX重建和全量渲染。

**依赖：** Checkpoint 5
**预计涉及文件：** 全量接收/视觉审查、逐页状态表、缺陷关闭记录及修复源码
**规模：** M

## Task 28：执行最终验收、评分与可恢复发布

**描述：** 在所有硬门和缺陷清零后，完成95分/各维度90%评分证据、SHA-256、正式输出和V5可恢复回收。发布前再次解析精确目标，不使用广泛删除命令。

**验收标准：**

- [ ] 旧S001—S127初始诊断由有效双审封存/追加修订链全覆盖且原记录未改写，旧六门失败和P0—P2缺陷逐项关闭，处置全部基于当前有效哈希重验；
- [ ] V6现行页面/事件全部适用九门通过；G7来自有效物理overlay，G8有反例执行记录，G9有原文—加工—反馈—修订—后用证据；
- [ ] 每一道通过门均重新验证至少两种异源证据的`source_type/source_origin_id`；一项证据、两项同类型/同源派生证据或自审布尔值不得通过；
- [ ] 所有非删除关闭重新复算目标字段、映射和现行审计节点哈希；任一变化/删除均使旧关闭与原审查者结论失效，未完成重新复验不得发布；
- [ ] `structure_manifest`中的页面/事件全部适用硬门通过，且分别等于现行审计、源码声明、课程数据可达图和装配快照；派生最终`current_manifest`再与PPTX物理页/备注事件清点相等，可见性等于实际投影状态；
- [ ] P0/P1/P2为0；
- [ ] `effective_release_review_view`的四类预期键集合与最终物理清单完全相等，当前bundle内每个唯一有效链尾均为`Pass`；同bundle缺陷关闭而无superseding Pass、新bundle修复后无revision=1 Pass及有效跨bundle历史关联、任何局部`Veto/pending/blocked_for_adjudication`、旧bundle Pass复用或手填总体Pass均阻断评分与发布；
- [ ] `final_scorecard`固定六维及权重，不允许增删改名或改权重：文本、教材和认识边界20；学生接收连续性与问题时机20；页面必要性与因果闭合20；参与覆盖、倾听、追问和修订15；语文质地、体验和课堂剧本15；视觉、插图与跨文件实施质量10；
- [ ] 每维固定使用规格中的90/95/100三档锚点；两名固定主审分别保存`reviewer_id/anchor=90|95|100/satisfied_clauses/object_field_evidence_refs`，任何得分必须绑定页/事件/资产及确切证据字段；处于两档之间时只能取已经完整满足的较低锚点；
- [ ] 每维最终anchor机械取两位主审的较低档；若分歧导致不放行，第三名未参与写作、未看双方结论、且与作者并集及两位主审均不同的裁决者只围绕证据独立裁决。总分由六维最终anchor按固定权重机械计算，不接受手填；总分≥95且每维≥90方可通过；
- [ ] 生成`release_attestation_sha256`，固定绑定审查前final bundle、完整`release_review_ledger`、机械`effective_release_review_view`、最终缺陷关闭汇总和评分表；ledger记录只绑定前置bundle，不形成自引用；
- [ ] `release_attestation_sha256`仍严格只有固定五个顶层组件；它通过`release_review_ledger.release_iteration_chain`和`final_defect_closure_summary.carried_defects_effective_view`间接但完整地绑定迭代链与跨迭代缺陷，不得另加第六/第七组件；验证器证明从首个final bundle到最终bundle无分叉、无缺陷丢失、无旧review复用；
- [ ] 全部PPTX、DOCX、Markdown、JSON和图片通过最终合同；
- [ ] 质量报告明确“桌面设计已验证；真实课堂效果待试教”；
- [ ] V6正式交付清单与SHA-256只包含当前版本；
- [ ] 每个正式PPTX/DOCX的SHA-256等于Task 27最终已审候选的源文件SHA-256；候选路径—正式路径晋升记录逐文件一致，视觉证据未失效；
- [ ] V5精确清单移入系统回收站，可恢复，不永久删除；
- [ ] 移动后再次验证V6全部路径和哈希。

**验证：**

- [ ] `python scripts/validate_meng_v6_release.py --stage .../_v6_stage --baseline-manifest .../baseline_manifest.json`
- [ ] 对正式目录重新运行V6页面审计、课程合同、Office/XML合同、PDF页数、逐页状态集合和SHA-256核验；
- [ ] `validate_meng_v6_release.py`复算`structure_audit_bundle_sha256`、`release_audit_bundle_sha256`、`release_review_ledger`和`release_attestation_sha256`，并核验正式文件、最终候选、`render_manifest`及学生接收/视觉证据全部哈希；结构审计出现Task27 review ID、自引用、渠道内容变化、路径外内容或任一哈希/页码双射不一致时拒绝发布；
- [ ] 发布验证器从两位主审的锚点条款和对象字段证据重新计算六维较低档、固定权重总分和阈值；改权重、缺维度、锚点条款未满足、无对象字段证据、档间取高、两审分歧取高、裁决者身份不独立或手填总分与派生值不符均拒绝发布；
- [ ] scorecard负向fixtures至少覆盖：删改六维名称/权重、缺任一主审评分、无证据分、仅满足90却填95、档间任意94/97、两审90/100却取100、裁决者与作者/主审重合、手改总分但组件哈希自洽；
- [ ] attestation负向fixtures至少覆盖：删除中间iteration、漏迁一个carried defect、改变iteration顺序/前驱、只改迭代链或缺陷有效视图但attestation不变，以及擅自增加第六/第七顶层组件；发布验证器须从两个既有组件独立重算五组件证明哈希；
- [ ] 跨bundle review lineage篡改fixtures至少覆盖只改prior ref或carried row任一字段、排序、集合基数、祖先关系或双向对应但保持Office文件不变；`release_iteration_chain`、ledger组件和attestation复算必须变化并拒绝旧证明；
- [ ] 发布验证逐条复算`authorship_registry_effective_sha256`和`reviewed_author_ids`，证明每个`reviewer_id`与目标及全部上游作者并集不相交；作者谱系或登记哈希漂移即拒绝发布；
- [ ] 发布验证复算`final_review_assignment`，证明两名角色ID不同、类型签署权限未串写、各自覆盖集合完整且分别明确`Pass`；同一人包办两类审查即拒绝发布；
- [ ] 发布验证从四类预期键集合逐键复算当前bundle的唯一有效链尾及状态，证明两名角色总`Pass`由所属全部局部`Pass`机械派生；局部非Pass、closure代替Pass、旧bundle Pass复用、跨bundle supersede、非法revision/prior历史关系或可写总体Pass均拒绝发布；
- [ ] 发布验证复算全部`adjudication_record`的目标、先行证据复核、身份判异、盲态来源、理由、证据和时间；任何无效裁决、裁决者看过双方结论或未解除的`blocked_for_adjudication`均拒绝发布；
- [ ] 最终完整母版及模块PPTX逐物理页验证单一合法ID、文件内唯一性、有序双射和occurrence可见性；重复ID、无ID额外页、母版隐藏但模块可见漏审、伪造非官方入口均拒绝发布；
- [ ] 最终Office/XML/渲染重跑四类删除签名扫描，后期资产重现为0；
- [ ] 过期版本扫描只针对学生可见文本、文件标题和当前版本元数据；审计总表、旧新映射、基线说明和回收记录列入明确溯源白名单；
- [ ] 结构化校验确保所有正式内容的`current_version`为`6.7-canonical-review-source-state`，不要求删除合法V5历史引用；
- [ ] 系统回收站记录V5移动清单，未使用永久删除；
- [ ] 最终质量报告明确所有学生接收结论为桌面模拟，只验证按类型登记的`scripted/prepared`渠道与可执行性；`observed`留待真实试教台账，不虚构学生效果。

**依赖：** Task 27
**预计涉及文件：** 正式V6交付物、质量报告、机器验收报告、SHA-256清单、V5回收记录
**规模：** M

## 5. 全局验收矩阵

| 要求 | 权威证据 | 放行条件 |
|---|---|---|
| 每页存在意义 | 127页旧页初始诊断与处置关闭、权威现行清单、现行适用硬门、声明/可达图、装配/物理页清点、全局删除/合并反事实 | 旧失败原样保存且逐缺陷关闭；结构冻结时G1—G6/G8/G9通过、G7待物理构建且节点为`provisional`；正式放行时九门均通过且无`pending/deferred/provisional` |
| 原文连续讲读 | 30组诗句合同、12句群、六章页面与学生接收审查 | 全覆盖，能由学生作品重建故事 |
| 活动真实参与 | 学习单痕迹、逐字稿、接收审查 | 个人—小组—公开—听众—修订闭合 |
| 学生前台纯净 | PPTX文本提取、禁词与删除测试 | 研发语言、预制答案、假共创为0 |
| 真实逐字稿 | PPTX备注、独立讲稿、时间合同 | 每页可演，等待与分支完整 |
| 语文质地 | 前台文本、朗读/语言活动、P2关闭记录 | 无AI套话与项目式术语 |
| 插图有用且统一 | 角色设定、任务卡、三秒测试、含图对照 | 文本边界与一致性全通过 |
| 文件质量 | Office/XML验证、全量PDF逐页状态、300 dpi重点页、文本提取 | 无损坏、溢出、裁切、错页，PPTX/DOCX每页均有证据 |
| 跨文件一致 | 课程快照、页码映射、机器合同 | 教案/学习单/讲稿/PPT一致 |
| 独立审查 | 学生接收与视觉报告 | P0/P1/P2清零并明确通过 |
| 真实性 | 最终质量报告 | 只声明桌面设计验证 |

## 6. 风险与控制

| 风险 | 影响 | 控制 |
|---|---|---|
| 工作树有其他代理改动 | 误覆盖无关成果 | V6使用独立路径；每任务限制文件清单；提交只含本任务文件 |
| 审计字段变成形式填表 | 页面仍无必要性 | 九门结构化失败码；删除/合并反事实；G8反例执行；G9理解闭环；独立接收审查 |
| 分批重构破坏整课连续性 | 局部都好、整体断裂 | 每两批执行模块回归；结构冻结后整课回归 |
| 原文轨道挤压当前句 | 视觉主线失效 | 三张真实原型先行；字号与信息块硬限制；最长句复验 |
| 活动由少数学生包办 | 参与感虚假 | 全员先生成；公开代表只呈现共同作品；听众有同步产出 |
| 现代婚恋框架覆盖文本 | 语文课变处方课 | 事实/推断/延伸三分；圆桌置于全文后；回诗和限度追问 |
| 生图人物漂移或过度定性 | 误导原诗 | 结构冻结后生图；角色/场景/道具注册表；V13/V17/V18非人物默认；至少四人盲化A/B三秒测试 |
| 总分掩盖关键缺陷 | “基本可用”被放行 | 先硬门和P0—P2清零，再评分；分歧默认不放行 |
| 真实课堂时间未知 | 设计时长与课堂不符 | 记录自然时长和安全停点；不在桌面阶段硬压课时；真实试教后再压缩 |

## 7. 实施中的提交策略

- 每个Checkpoint最多形成一个只含V6范围文件的提交；
- 不把共享工作树中的无关修改带入提交；
- 生成物只有在Checkpoint验证通过后提交；
- 任何阶段都不使用`git reset --hard`、`git checkout --`或广泛清理命令；
- V5回收只发生在Task 28，并依据精确清单执行。

## 8. 计划完成判定

本计划的终点不是“完成一个新PPT”，而是以下事实同时成立：

1. 旧S001—S127逐页得到可核验决定；
2. V6所有页面/事件都通过适用九门，能证明其位置、学生动作、可见变化、后续用途、物理一致性、反例出口和理解闭环；
3. 六章原文、三问、圆桌、知识收纳和终读形成完整学习链；
4. 教案、学习单、逐页剧本、PPTX、DOCX和课程数据同源一致；
5. 视觉与插图服务页面意义，人物、场景和道具不漂移，文本不越界，所有入页图通过至少四人盲化A/B测试；
6. 两名独立审查者与全部上游作者集合机械判异后明确通过，P0/P1/P2为0；
7. 全量文件与渲染证据证明交付可用；
8. V5已按精确清单移入可恢复回收站，正式目录只指向V6；
9. 质量报告如实声明真实课堂效果仍待试教。

只有九项全部由当前文件、渲染、报告和审查证据证明，V6才算完成。
