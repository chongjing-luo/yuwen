---
document_type: lesson_schema_contract
scope: "S3课程数据契约；S4/S5的唯一现行输入形态"
status: "active"
version: "2.6"
date: "2026-08-25"
enforced_by: scripts/validate_lesson_schema.py --strict
mechanism_nodes: "K1知识范围 · K2文本锚定 · K4知识关系 · U1-U8页面合同 · J1-J7参与、体验、节奏与诚实边界"
---

# 通用课程数据契约 lesson schema v2.6

v2.6是新课文进入G2的现行契约。v1、v2.0和v2.1只允许非strict读取；存量v2.2—v2.5按冻结标准仍可strict验证，但新候选不得静默沿用。v2.6继承v2.5的课堂事件、学生经历、语义场景、元素级信息状态、视觉来源和逐物理画面蓝图，并新增页面呈现角色与支撑页触发—返回合同。G2必须足以让S4直接复原页面在整课中的职责、准确上屏内容、构图关系、配图资格和剧本对应；S4只负责精确实现。G2数据不携带课堂效果或宿主放行状态。

## 上游绑定与范围冻结

新候选的`schema_version`精确使用`"2.6"`。顶层采用闭合字段集：

- `lesson_id`；
- `lesson_plan_binding: {path, sha256}`，指向当前G1锁；
- `lesson_plan_scope`，含`objective_ids/knowledge_ids/deferred_ids/question_ids/stage_ids/contract_sha256/total_minutes/closing_mode`；
- `book_unit`、`text_contract`、`objectives`、`three_questions`、`kp_scope`、`relations`、`visual_source_profile`、`pages`、`claim_boundary`及可选`target_natural_minutes`。

strict会递归重跑G1。目标ID与陈述、KID及defer、贯穿问题、阶段顺序、总时长、收束方式和合同哈希不得漂移。`three_questions`只是兼容字段名，数量不固定且可以为空。

`text_contract`以`source_path/source_sha256/canonical_lines`绑定UTF-8原文，逐条原文必须实际存在。`kp_scope.kp_ids`与G1的`KID→KP`投影精确一致；目标`kp_refs`只能消费其G1 `kid_refs`获批的KP。

## 全课视觉来源档案

`visual_source_profile`字段闭合为：

- `strategy`：`textbook_first/text_type_only/hybrid`；教材有本课或本单元相关视觉时优先`textbook_first`，不能因方便跳过核验；
- `source_artifacts[]`：`asset_id/path/sha256/role/usage_boundary`。路径必须为项目根相对路径且资产真实存在、哈希一致；`textbook_first/hybrid`至少一项；
- `palette[]`：`role/hex/source_basis`，登记色彩角色、6位十六进制值及其教材或文本类型依据；
- `image_style/shape_language/typography_tone`：分别冻结图片风格、图形语言与字形气质；
- `consistency_rules[]`：本课人物、图形、色彩和图像派生的稳定规则；
- `fact_boundary`：教材图片能证明什么，不能由视觉补写什么。

教材视觉档案是设计来源，不是要求每页配图。水印、页码、印刷噪声、下一课插图和无关装饰不得作为本课资产。教材视觉不足时允许按文章类型补充，但须写明来源依据；历史人物教材肖像只能直接使用或作为身份核验锚，不能以生成的相似脸替代史实照片。

## 页面基本合同

每页含`page_id/stage_id/objective_ids/lesson_kids/title/minutes/literary_object`。页面按G1阶段顺序推进；PG04—PG09的目标与KID必须属于该阶段，PG01—PG03保持两个空列表。全部获批目标与`must_teach/retrieve_prior` KID至少有一个非定位结构页落实。`literary_object`锚定`canonical_lines`，或使用受控非行对象类别。

每页先由`activity_contract.event_type`确定主导课堂事件。以下十三项为全部事件的共同合同：

1. `previous_page_input`；2. `unique_difficulty`；3. `unique_function`；4. `first_view_contract`；5. `information_state`；6. `student_action[]`；7. `next_use`；8. `visual_role`；9. `first_person_reception`；10. `deletion_loss`；11. `continuous_increment`；12. `attention_budget`；13. `story_return`。

下列字段按类别注册表中该事件的`requires`条件启用，不适用时省略，不写“无产物”“无需反馈”等占位话术：

- `artifact`对应`artifact`；
- `real_wait`对应`wait`；
- `bounded_feedback`对应`feedback`；
- `visible_revision`对应`revision`；
- `normal_counterexample`对应`normal_counterexample`。

准确讲授、情境叙述、朗读停留和过渡沉静可以没有即时持久产物，但仍须通过`next_use/next_use_ref`安排后续检索、解释、应用或整体理解检验。学生生成、讨论、操练等事件按注册合同完整保留任务、等待、产物、反馈与必要修订。

另有`next_use_ref: {kind,target_id,use}`。`kind=page`只指向后续真实页面；末页可用`closure/lesson_closure`；未注册真实消费者前不得用`assessment`冒充后用。

## S3四组责任对象

### 1. `knowledge_payload[]`

每项字段闭合为：

```json
{"kid": "K01", "scope": "本页具体知识切片", "page_role": "construct"}
```

`kid`集合与该页`lesson_kids`一致；`scope`必须具体；`page_role`只允许`encounter/construct/practice/calibrate/retrieve/transfer`。一个KID可以在不同页经历不同生命周期，不能只挂编号而不说明本页形成了什么。

### 2. `activity_contract`

字段闭合为：

```json
{
  "event_type": "EV05",
  "primary_type": "AC05",
  "secondary_types": [],
  "teacher_move_types": ["TM03"],
  "learner_action_types": ["LA09"],
  "participation_type": "PS01",
  "artifact_type": "EP06",
  "sensory_channel_types": ["SC01", "SC04"],
  "feedback_types": ["FB02"],
  "selection_reason": "为什么选择这一学习机制",
  "knowledge_fit": "它怎样适配当前知识与目标深度",
  "experience_fit": "它怎样适配学生此刻的体验与困难"
}
```

所有ID解析到`work/methodology/lesson-preparation/教学设计类别注册表.json`。`event_type`先说明课堂实际发生什么，并通过注册项`requires`决定条件合同。只有学生主要通过自主加工获得增量时才填写`primary_type`；准确讲授、情境叙述和过渡沉静允许省略主活动，朗读停留通常使用`AC01`。`artifact_type`与`feedback_types`也只在事件合同或真实课堂需要时填写；非反馈事件使用空列表，不制造虚假反馈。

主活动只描述学生获得增量的主学习机制；讲授、提问、示范归教师动作，讨论、分组、展示归学生动作、参与结构或产物。用户举例与既往课例只是候选材料，不是固定菜单或配额；先形成待验证的目标、困难、期望变化和约束，再按本篇原文、获批目标/KID、学情、体验与证据需求校验、补正，最后裁决照用、修改、拆并、替换或舍弃。逐页依据进入`selection_reason/knowledge_fit/experience_fit`，不得以统一生成模板冒充真实取舍。

### 3. `student_experience`

闭合字段为`perceives/thinks/possible_feeling/does/understands`，分别写学生看见或听见什么、思考什么、可能而非被迫产生怎样的情绪、实际做什么、离页时理解增加了什么。不得把教师目标、学生画像或“学生很开心”当体验链。

### 4. `slide_design`

页面单位是一个连贯语义场景或一个组织意图，不是一个KID。一个完整段落、诗歌若干相邻句或同一人物证据链可承载多组知识；同页须证明它们属于同一意义单位、具有可见关系、主要加工动作一致并且需要共视。分页同时守住两条边界：语义完整与上下文连续构成下限，共同可读、焦点清楚和加工负荷可承受构成上限；固定条数、字数或“一页一个知识点”只可预警，不作硬门。

闭合字段为：

- `presentation_role`：解析到注册表PG01—PG09，表示标题、导航、章节（子标题）、主干文本、支撑、活动、作品与反馈、总结收纳或作业中的唯一主要职责；它不是固定版式，也不替代`knowledge_payload.page_role`的知识生命周期；
- `role_rationale`：说明为什么本页承担该角色，以及删除或改作另一角色会损失什么；
- `support_link`：只允许PG05使用，闭合为`trigger/source_ref/return_ref/return_use`。`source_ref`取此前页面ID或`lesson_entry`，`return_ref`必须指向后续真实页面；非支撑页不得填写；
- `semantic_unit`：本页保持完整的文本或意义单位；
- `organizing_intention`：这一页为什么把这些对象组织在一起；
- `content_object_types[]`：内容对象类别ID；
- `semantic_relations[]: {type,element_ids,rationale}`：对象之间需要被看见的关系；
- `display_constraints[]`：必须共视、必须分时、连续锚定、单一焦点、上下文完整、共同可读、现场留痕等约束ID；
- `layout_operations[]`：分组、分层、对齐、并置、连接、突出、就近注释、分时揭示、留白、全局回归等操作ID；
- `co_view_groups[]: {id,element_ids,rationale}`：必须在至少一个信息状态中同时可见的元素组；
- `must_stage[]: {element_ids,rationale}`：不得在B0出现、必须等待合法触发的元素组；无分时需要时使用空列表；
- `priority_layers[]: {level,element_ids,rationale}`：按`L1/L2...`连续编号并恰好覆盖全部前台元素；
- `continuity_anchor[]`：在全部信息状态中持续可见的元素ID；
- `density_judgment: {semantic_completeness,readability_focus,decision}`：分别说明为何没有过碎、为何没有过密；当前成页决定固定为`retain_as_page`；
- `boundary_rationale`：相对前后页为何在此划界；
- `frontstage_elements/information_states/information_hierarchy/reveal_sequence/layout_rationale`。

`presentation_role/content_object_types/semantic_relations/display_constraints/layout_operations`解析到类别注册表。页面角色只规定主要职责和视觉优先级，不提供模板坐标。S3冻结页面角色、语义分组、分页、共视/分时、主次层级、连续锚点与揭示时序，并为每个信息状态冻结一个物理画面蓝图；不冻结像素级字号、栏宽、边距或卡片坐标。S4根据真实内容长度落实精确几何、配色、字体、资产、音视频、动效和美学；若可读实现要求改变页面角色、支撑页返回目标、语义分组、分页、信息时序、可见内容或配图功能，退回S3。`layout_rationale`必须说明怎样帮助当前知识和学生动作，不能写“美观、清晰、大气”。

PG01—PG03属于定位结构页：`literary_object.kind`可用`lesson_orientation`，`content_object_types`必须包含CO09，`objective_ids/lesson_kids/knowledge_payload`必须为空列表。它们可以帮助入场、导向和注意力恢复，但不得为合同形式伪造目标达成或知识增量。PG04—PG09仍必须绑定获批目标、KID和知识生命周期。

标题必须先让学生识别页面对象或职责，再追求文学气息。作者、背景、体裁、用典、活动和作业等规范知识使用直接主标题；副标题、引文、节奏和画面可以增添艺术性。问句标题只用于本页真实探究，不得把规范知识包装成猜测，也不得提前给出学生本应形成的结论。

`frontstage_elements[]`逐项冻结`{id,text,role}`，`role`只允许`content/prompt/material/student_work/calibration/feedback`；ID按`E01`起连续编号。`information_states[]`按`B0/B1/B2...`连续编号，每态闭合为`{id,visible_element_ids,enter_trigger}`；B0固定由`page_enter`进入，后续触发可使用`after_instruction/after_prior_artifact_retrieved/after_student_response/after_primary_artifact_committed/after_secondary_artifact_committed/after_peer_response/after_calibration`。各状态登记该时刻完整可见元素集合，所有元素至少进入一态；`calibration/feedback`元素不得出现在B0，也不得早于其所回应的学生口答、作品提交或同伴回应。准确讲授若需首屏呈现规范知识，应把它登记为本页`content`而非伪装成首答后的`calibration`。题名、前台元素和逐态可见内容共同接受后台词与泄答审查。自由文本`reveal_sequence`只解释设计意图，不能替代元素级状态。

### `physical_screens[]`

每个`information_state`恰对应一个按相同顺序排列的物理画面，字段闭合为：

- `screen_id`：固定为`<page_id>-<state_id>`；
- `state_id/visible_element_ids`：与对应信息状态完全一致；
- `screen_function`：该物理画面的唯一课堂作用；
- `composition_blueprint/reading_path/spatial_proportions`：构图关系、学生视线顺序和大致空间比例；比例是可执行意图，不是精确坐标；
- `image_plan`：闭合为`decision/function/derivation_mode/asset_refs/content_brief/style_brief/placement/visual_weight/appearance_timing/fact_boundary`。`decision`取`required/optional/forbidden`；`derivation_mode`取`direct_textbook_asset/textbook_visual_derivation/text_type_fallback/none`。必需配图必须引用视觉来源；禁止配图不得引用资产且派生方式为`none`；
- `script_segment_refs`：按原顺序恰好覆盖该状态的全部剧本片段。

逐屏蓝图要让PPT制作者无需猜测：学生实际看见什么、先看哪里、图文各占多大关系、图片是否出现、从哪里来、承担什么、何时出现以及不能误画什么。精确坐标、字体微调、真实裁切和渲染修复仍属于S4。

## 完整逐页剧本

`script`字段按事件合同启用：

- `teacher_spoken`、`student_process`、`timeboxes[]`和`script_segments[]`为共同字段；教师语言必须是可直接说出的完整教学语言；
- `transition_spoken`与`cut_spoken`在真实存在承接或切页时填写；
- `expected_responses[]`只在事件`requires`含`expected_responses`时强制，须包含多种可能回应；
- `branches[]`只在`requires`含`branches`时强制至少两种不同`kind/response`；
- `feedback_spoken`只在`requires`含`feedback`时强制；
- `observable_evidence`在事件要求学生回应或产物时强制，说明当场能看见或听见什么；
- `timeboxes[]`：`label/seconds/segment_ids`，总秒数恰等于`minutes×60`；按剧本顺序完整且不重复地覆盖全部`script_segments`。时间盒数量由真实事件决定，不固定为五段或任何配额。
- `script_segments[]`：按`S01/S02...`连续编号，逐项闭合为`{id,state_id,kind,enter_trigger,text}`；`kind`允许`transition/instruction/narration/reading/task/wait/calibration/feedback/summary/cut`。讲授、叙述、朗读与总结片段连同任务/校准片段按原序投影`teacher_spoken`。每次真实`task`后必须紧接属于它的`wait`；多阶段任务重复`task→wait`。需要学生先答、先回应或先提交作品的事件，`calibration/feedback`不得早于相应的`after_student_response`、作品提交或同伴回应触发。任何片段不得早于所绑定状态；信息状态、台词触发与时间盒必须同态。

来源辨界或分类页的材料卡只写待判断陈述，不在卡面自报“教材注释／自然译句／作品作用／课文未写”等归属；类别名称统一放在任务区或学生提交后的校准态。G1批准的字数、独立性、闭卷条件、产物载体与后用规格在G2必须原样守恒，不能以更短、更公共或更弱的产物替代。

S3剧本必须可无声试讲，不得用“提问—讨论—总结”三项提纲代替。准确讲授、情境叙述、示范朗读可以构成连续完整片段；生成事件的答案性前台元素与校准台词必须在同一合法触发之后进入。S4可据`information_states + script_segments`唯一复原真实课堂，只同态投影为备注与独立screenplay，可以补设备操作提示，不得重写教学语言。

## 校验与下游

```bash
python3 scripts/validate_lesson_schema.py --lesson-json <lesson.json> --strict
python3 scripts/checks/check_trace_evidence.py --lesson-json <lesson.json> --strict
python3 scripts/validate_lesson_lineage.py design <design_lock.json>
```

三条命令通过后才能进入S4。人读`教学设计.md`显式包含lesson ID和全部page ID，与`lesson.json`同源。`claim_boundary`固定为`课堂证据状态：未采集；学生掌握、理解与享受均待真实试教验证。`，不得另造相反课堂账字段。G2锁及下游结构见`.agents/skills/_shared/lesson-lineage-contracts.md`。
