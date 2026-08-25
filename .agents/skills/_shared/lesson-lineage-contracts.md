---
document_type: lesson_lineage_contract_reference
version: "1.5"
date: "2026-08-24"
mechanism_nodes: [K1, K2, U8, J7]
---

# 单篇备课G0—G4血缘契约

仅在创建或排查备课锁文件时读取。教学内容与阶段方法以 `work/methodology/lesson-preparation/语文备课操作规程.md` 为准；本文只规定机器字段。

## 通用规则

- 路径必须相对项目根且不得以`..`越界，G1起的正式课程对象必须位于`work/teaching/`课程树，SHA-256为当前文件完整字节哈希；
- 同一课的元数据放 `work/teaching/<册>/<课>/_meta/`；
- 正式课`lesson_id`使用`LES-{册代码}-{课文代码}-{两位序号}`；测试夹具仅允许`LES-TEST-{两位序号}`。它在全部对象中相同，一个ID只解析到一个课程目录，同一目录也只能登记一个ID；
- 上游对象或锁改变后，下游不得只换哈希，须回到责任阶段重新审核/生成；
- 正式锁只表示真实门禁结果，不创建“假批准”样例；新链各级`claim_boundary`统一使用受控值`课堂证据状态：未采集；学生掌握、理解与享受均待真实试教验证。`。这是治理枚举，不是可自由续写的设计文本；改写或追加相反结论均失败（U6/J7）。

## G0 `evidence_manifest.json`

| 字段 | 要求 |
|---|---|
| `schema_version` | 固定 `lesson-evidence.v1` |
| `lesson_id` | 正式课使用注册格式的LES稳定ID；G0即检查格式、manifest所在课程目录及跨目录唯一性，不把坏号拖到G1 |
| `mechanism_nodes` | 至少一个合法K/U/J节点 |
| `normative_sources[]` | `source_id/role/authority/path/sha256`；必须含S1 `textbook` PDF与S1 `curriculum_standard` PDF |
| `derived_sources[]` | `source_id/role/path/sha256/derived_from_source_id/derived_from_sha256`全部必填；派生父项须是已登记规范源 |
| `knowledge_sources[]` | `source_id/path/sha256`；为空时必须有 `knowledge_gap_reason` |
| `evidence_dossier` | `path/sha256` |
| `claim_boundary` | 使用通用规则中的受控课堂证据声明；规范源与解释分层另写证据档案，不混入此字段 |

G0对象必须位于`work/teaching/<册>/<课>/_meta/evidence_manifest.json`。同时设最低实体门：教材/课标PDF必须可解析且至少一页；至少有一个可检索派生源；知识源为空时须给出缺口理由；证据档案须为可读Markdown并达到最低篇幅、标题与非低熵结构。清单顶层字段闭合。该门只排除假文件和重复字符占位，不替代回页核验。

验证：`python3 scripts/validate_lesson_evidence.py <path>`。

## G1候选 `lesson_plan_candidate.json`

所有者审核前必须先生成可验证、但不含任何批准声明的候选对象：

| 字段 | 要求 |
|---|---|
| `schema_version` | 固定 `lesson-plan-candidate.v1` |
| `lesson_id` / `author_id` | 与人读教案和G0一致，作者为非空字符串 |
| `lesson_plan` | 当前人读`教案.md`的`path/sha256` |
| `evidence_manifest` | 当前G0清单的`path/sha256` |
| `contract` | 与正式G1锁相同的机器投影字段；须先完整通过内容、联合覆盖与血缘预检 |
| `status` | 固定 `candidate_owner_review`；不得写`approved`或`released` |

候选不含`owner_approval`。运行`python3 scripts/validate_lesson_plan.py --candidate <path>`；通过只证明当前教案—合同—证据组合具备送审条件，不构成所有者批准。送审时同时提供人读教案SHA-256、候选文件SHA-256、`contract`的canonical JSON SHA-256和G0清单SHA-256。任何一项改变都须重建候选并重新审核。

## G1所有者回执

`G1_owner_approval.json`只在所有者明确审核当前教案后创建：

| 字段 | 要求 |
|---|---|
| `schema_version` | 固定 `g1-owner-approval.v1` |
| `lesson_id` | 与教案一致 |
| `reviewer_id` / `author_id` | 非空、无首尾空白且规范化后仍不同；不得用空格绕过作者不得自审 |
| `decision` | 固定 `approved`；未批准不创建正式回执 |
| `reviewed_at` | 带时区的ISO 8601时间 |
| `approval_event_id` / `approval_source` | 可追溯到真实所有者批准事件，均非空 |
| `verification_mode` | 固定`external_review_gate` |
| `authentication_boundary` | 明说本地验证器只验证结构与血缘，不认证人类身份；真实所有者身份须由宿主对话/签名记录人工核验 |
| `approval_statement` | 真实批准原意的记录，必须包含当前教案SHA-256 |
| `lesson_plan_path` / `lesson_plan_sha256` | 审核时的人读教案 |
| `lesson_plan_contract_sha256` | G1机器合同按UTF-8、键排序、紧凑JSON序列化后的SHA-256 |
| `evidence_manifest_sha256` | 审核时G0清单哈希 |
| `standard_version` | 本轮审核采用的规程/标准版本 |
| `resolved_issues` | 已裁决问题数组，可为空；字段类型必须是真实数组，不能用字符串占位 |

**能力边界**：普通工作区JSON无法独立证明是谁写入。G1机器验证器只拒绝缺字段、错哈希、错时间和错上游；所有者真实性属于外部人工review gate，S5双审必须复核其事件引用。不得把`validate_lesson_plan.py`通过表述成“机器认证了所有者”。

## G1 `lesson_plan_lock.json`

正式锁必须写在同课`_meta/lesson_plan_lock.json`，并保留同目录`lesson_plan_candidate.json`。验证器会重新预检候选，并要求候选中的`lesson_id/author_id/lesson_plan/evidence_manifest/contract`与正式锁完全相同；缺候选、候选漂移或仅在课程目录外放置一份锁文件均不构成G1。

顶层字段：

| 字段 | 要求 |
|---|---|
| `schema_version` | 固定 `lesson-plan-lock.v1` |
| `lesson_id` / `author_id` | 与回执一致 |
| `lesson_plan` | `path/sha256` |
| `evidence_manifest` | `path/sha256` |
| `owner_approval` | `path/sha256` |
| `status` | 固定 `approved` |
| `contract` | 下表的教案机器投影 |

`contract`字段：

| 字段 | 要求 |
|---|---|
| `mechanism_nodes[]` | 教案整体服务节点 |
| `total_minutes` | 完整母版总分钟数，正数；下游只能阶段内细化，不得漂移 |
| `closing_mode` | 宏观收束方式；下游不得擅改 |
| `objective_framework` | 六键闭合集：`language_use/thinking/aesthetic/culture/moral_education/reality_transfer`；每键为`status/reason/objective_refs`，`status`为`included/not_primary`。六向均须裁决；`language_use/moral_education/reality_transfer`固定为`included`且有目标引用，其他三向可经说明后`not_primary` |
| `objectives[]` | `id/kind/dimensions/statement/kid_refs/mechanism_nodes/minimum_evidence/high_quality_evidence/failure_signal/recurrence`；`kind`为`literacy`或`reality_transfer`；`dimensions`使用上述六键且与`objective_framework`双向一致 |
| `knowledge_items[]` | `kid/statement/status/source_ref/stage_refs/mastery_evidence/mechanism_nodes`；`must_teach/retrieve_prior`另须有非空`kp_ids[]`，逐项解析到G0登记知识源，`source_ref`也须指向该知识源；`status`为`must_teach/retrieve_prior/teacher_reserve/defer`，defer另有`defer_reason`；`stage_refs`必须与`stages[].kid_refs`的反向投影完全一致；`teacher_reserve/defer`的`stage_refs`必须为空，且不得进入课堂阶段 |
| `knowledge_clusters[]` | 自适应知识簇；每项含`id/name/organizing_basis/rationale/kid_refs`。簇名、数量和组织方式由本篇课文决定，不采用固定类别枚举；全部`knowledge_items`（含教师储备/defer）必须且只能归入一个主簇 |
| `work_interpretation` | 固定三键`central_meaning/expressive_intent/emotional_organization`，分别裁决作品主旨/核心观点、表达意图/作品表达指向、情感变化/态度语调组织。每键只含`status/kid_refs/evidence_boundary/not_applicable_reason`；准确结论只在所引KID定义，避免第二事实源。`included`须有证据边界和至少一个`must_teach/retrieve_prior` KID，`not_applicable`须有具体文体理由且不得引用KID |
| `questions[]` | 可为空；有贯穿问题时，每项含`id/text/rationale/objective_refs/kid_refs/stage_refs/recovery_stage_refs/mechanism_nodes`，`id`非空且唯一，说明统摄理由、牵引的目标与知识、途中阶段和最终回收阶段；局部问题不进入本字段 |
| `overall_teaching_logic` | `text/stage_refs/mechanism_nodes/components`；节点至少含K1/K2/U8/J4 |
| `stages[]` | `id/name/entry_reason/text_scope/objective_refs/kid_refs/initial_method/student_change/student_experience/teacher_role/evidence/transition_reason`；逐阶段落实进入因果、原文范围、目标与知识、初步教法、学生变化与体验、达标证据和转段理由 |
| `claim_boundary` | 使用通用规则中的受控课堂证据声明 |

六向审计、14类覆盖框架、文化五类和作品整体解释三项只证明查漏结构，不能直接充当成品知识目录，也不能证明文学判断正确。所有者仍须审查知识簇是否由本篇原文推进、意义结构、叙事/论证关系或学习依赖自然形成，是否存在近义重复KID；作品主旨、表达意图和情感组织是否有全文证据，表达意图是否把合理推断冒充作者心理事实，立德树人与现实迁移是否从本篇原文、教材和必教知识生长，是否有伦理边界与反口号失败信号。每个目标的`kid_refs`至少含一个`must_teach`或`retrieve_prior` KID，不得把`teacher_reserve`或`defer`伪装成目标内容；对每一条`目标—KID`关系，必须有一个真实阶段同时承担该目标和KID，并能在该阶段回查原文范围、初步教法、学生变化和达标证据。分别覆盖目标与KID、但把二者交叉错配，不算落实。覆盖审计由这些阶段责任生成，不再维护一份重复的`implementation_map`。

`overall_teaching_logic.components`必须逐项裁决：`entry/context/text_development/knowledge_formation/student_experience/discussion/synthesis_retrieval/assessment_evidence/transfer/exam_link/contemporary_link`。每项含 `status/reason/stage_refs`；`status`为`included/not_applicable/deferred`，纳入者有阶段，未纳入者有理由。

人读`教案.md`须为可读Markdown，并达到至少300个非空白字符与4个标题的最低实体门；单字或空壳教案不得取得G1。篇幅门只排占位，逻辑完整性仍由所有者审查。

验证：`python3 scripts/validate_lesson_plan.py <path>`。

## G2 `lesson.json`与`design_lock.json`

新课程数据使用精确的`schema_version: "2.6"`。`2.0/2.1`仅供非strict读取；存量`2.2—2.5`按其冻结标准仍可strict验证，但新候选不得静默沿用或改写。除通用lesson字段外必须含：

- `lesson_plan_binding: {path, sha256}`，指向当前G1锁；
- `lesson_plan_scope`含五个ID数组`objective_ids/knowledge_ids/deferred_ids/question_ids/stage_ids`，以及`contract_sha256/total_minutes/closing_mode`；`stage_ids`须保留G1批准顺序；
- `page_id`全课唯一；每页含`stage_id/objective_ids/lesson_kids`；阶段不得倒灌，PG01—PG03的后两项为空列表，全部获批目标与必教/检索旧知KID必须至少被一个PG04—PG09页面落实；
- v2.6每页先在`activity_contract.event_type`登记受控课堂事件类型，并在`slide_design.presentation_role`登记标题/导航/章节（子标题）/主干/支撑/活动/作品反馈/总结/作业中的唯一主要职责。角色由学生第一注意对象、当页主动作和删除损失共同裁决；PG01—PG03只登记CO09，`objective_ids/lesson_kids/knowledge_payload`必须为空列表，不伪造知识负载。PG05另以`support_link`绑定此前触发来源、后续返回页和返回用途；页面角色不是固定版式。全部事件填写前页输入、困难、唯一功能、信息状态、学生接收/动作、后用、视觉职责、第一人称接收、删除损失、连续增量、注意力预算和故事回接；只有事件注册项`requires`声明时才强制`artifact/real_wait/bounded_feedback/visible_revision/normal_counterexample`。非空不等于有效，单字、重复字符或短垃圾串失败；
- `text_contract.canonical_lines`逐条存在于绑定的UTF-8文本源；G1的KID→KP映射与G2 `kp_scope/objectives.kp_refs`必须完全一致；
- 每页另有结构化`next_use_ref`，只能指向后续真实页面、最后一页的`lesson_closure`或明确测评对象；纯文本写“后面再用”不构成U8前向消费；
- 顶层另有`visual_source_profile`，登记教材优先的视觉资产路径/哈希/用途边界、色板、图像与图形语言、字体气质和一致性规则；每页四组闭合S3对象中的`slide_design`除页面角色、支撑页闭环、语义关系与逐态元素外，还须用`physical_screens[]`为每个信息状态冻结准确可见内容、构图关系、阅读路径、空间比例、配图资格/来源/功能/时机/事实边界和剧本片段。其余三组仍为`knowledge_payload[]/activity_contract/student_experience`；全部类别ID解析到`教学设计类别注册表.json`；
- `frontstage_elements[]`冻结`id/text/role`，`information_states[]`冻结每个B0/B1/B2的完整可见元素集合和进入触发；答案性元素不得在B0或首份产物提交前出现；
- `script`用`transition/instruction/narration/reading/task/wait/calibration/feedback/summary/cut`真实片段绑定信息状态与触发时点；讲授、叙述、朗读和总结可无任务，发生任务则必须紧接真实`wait`，只有事件合同要求时才强制可能回应、分支、反馈和证据字段；时间盒按顺序覆盖全部片段，可直接无声试讲；S4只同态投影；
- v2.6顶层及嵌套对象采用闭合字段集，不能另加`classroom_account`等字段绕过受控两本账声明；目标ID与陈述、贯穿问题文本和上述范围必须与G1一致。

`教学设计.md`是G2唯一人读审批对象。严格校验通过后先提交当前Markdown、`lesson.json`和G1锁三项SHA-256，等待用户明确批准；JSON、聊天摘要、此前版本批准或“继续/执行”不能代替对当前组合的审批。未批准时不得创建design lock。

`G2_owner_approval.json`只在用户明确审批当前组合后创建，schema固定为`g2-owner-approval.v1`，字段闭合集为：`schema_version/lesson_id/reviewer_id/author_id/decision/reviewed_at/approval_event_id/approval_source/verification_mode/authentication_boundary/teaching_design_path/teaching_design_sha256/lesson_data_sha256/lesson_plan_lock_sha256/approval_statement/standard_version/resolved_issues`。`decision`固定为`approved`，审批者不得与S3设计作者相同，时间须带时区，`verification_mode`固定为`external_review_gate`，声明须包含当前教学设计哈希，三项哈希须精确绑定当前Markdown、课程数据和G1锁。本地验证器只验证结构与血缘，不认证人类身份。

`design_lock.json`字段：

| 字段 | 要求 |
|---|---|
| `schema_version` | 固定 `design-lock.v1` |
| `lesson_id` | 与G1/lesson一致 |
| `author_id` | S3教学设计作者，非空；进入G4内容作者全集 |
| `lesson_plan_lock` | `path/sha256` |
| `lesson_plan_sha256` | G1锁内当前人读教案哈希 |
| `teaching_design` / `lesson_data` | 各为`path/sha256`；人读教学设计至少120个非空白字符、3个Markdown标题、6行有效内容，并显式包含本课`lesson_id`及全部`page_id`，以证明和lesson.json同源；这只是占位防线，不替代语义审查 |
| `owner_approval` | `path/sha256`，指向同课`_meta/G2_owner_approval.json`；回执精确绑定当前教学设计、课程数据和G1锁 |
| `validation` | `validator: validate_lesson_schema.py`、`strict: true`、`passed: true` |
| `status` | 固定 `validated` |

验证顺序：先 `validate_lesson_schema.py --lesson-json <lesson.json> --strict`，提交人读审批稿并取得当前哈希回执，再运行 `validate_lesson_lineage.py design <design_lock.json>`。后者会重新执行真实strict schema校验并验证审批血缘，不信任`validation.passed: true`的自报结果。`教学设计.md`、`lesson.json`或G1锁任一改变，旧回执与design lock立即失效。

## G3 manifest与`materials_lock.json`

manifest使用`schema_version: lesson-materials-manifest.v1`，含`lesson_id/source_design_lock_sha256/artifacts[]`。manifest与所有artifact必须留在G2 design lock所属同一课的`materials/`目录，课目录根部不得遗留PPTX/DOCX，`materials/`中的实际文件除manifest自身外必须全部登记。每个artifact含`role/path/sha256`；必需角色为`pptx/screenplay/learning_sheet/board_plan`，四种角色各用独立路径且内容哈希不同的非空文件。三种文本物料须为可读UTF-8 Markdown并达到角色最低有效内容（剧本200、学习单100、板书80个非空白字符且有标题）；screenplay必须逐页同态投影S3剧本并出现全部`page_id`及教师/学生/等待/回应/切页要素，S4不得重写教学语言，只可补设备操作提示；学习单和板书至少锚定一处教材原文。该门只拦占位，不以字数冒充语义质量。

`pptx`必须通过OPC核心成员、XML命名空间、`.rels`默认ContentType、presentation及每个slide的ContentType、根officeDocument与 presentation—slide内部关系、所有slide部件自身关系（均不允许External TargetMode）和slide部件解析；整份课件至少有一个非空文本对象，或一个经`r:embed`、内部image关系、`ppt/media/`目标、image ContentType与真实图片签名完整绑定的图片。空`p:pic`、把XML冒充图片、空白结构包或仅放两个伪成员的ZIP均失败。该结构门不替代S4的Office打开/渲染QA。

`materials_lock.json`含：

- `schema_version: materials-lock.v1`；
- `lesson_id`；
- `author_id`：S4物料制作者，非空；进入G4内容作者全集；
- `design_lock: {path, sha256}`；
- `manifest: {path, sha256}`；
- `status: built`。

验证：`python3 scripts/validate_lesson_lineage.py materials <materials_lock.json>`。

## G4 `audit_lock.json`

S5完成独立视觉审查与学生接收审查后创建：

| 字段 | 要求 |
|---|---|
| `schema_version` | 固定`audit-lock.v1` |
| `lesson_id` / `author_ids[]` | 精确覆盖S2教案作者、S3设计作者、S4物料作者；任何内容作者不得进入两名审查者 |
| `materials_lock` | 同课`_meta/materials_lock.json`的`path/sha256` |
| `standard_snapshot` | `version/path/sha256/registry_sha256/frozen_at/enforcement_config{path,sha256}`；注册库与实际执行配置均复制到同课`_meta/reviews/`，G4递归校验和原则检查只消费冻结配置，不读取live配置；快照必须通过完整原则注册库校验，不能只保留20个空节点和伪原则 |
| `audit_report` | `path/sha256`；报告内部精确绑定当前物料锁、冻结物料、注册库哈希、执行配置哈希、机器检查、缺陷与P3风险 |
| `reviews[]` | 角色恰含`visual`与`student_reception`，不同审查者，各自回执精确绑定同一物料锁、冻结物料、注册库与执行配置哈希 |
| `frozen_artifacts_sha256` | 对G3 manifest的`artifacts[]`作canonical JSON SHA-256 |
| `status` | 固定`awaiting_host_release`；项目内对象不得写`released` |
| `claim_boundary` | 使用通用规则中的受控课堂证据声明 |

两份`audit-review.v1`回执须含带时区时间、完整内容作者清单、`decision: pass`、空的未清`defect_ids`，各自使用不同且可追溯的`review_event_id`；`review_source`为`{locator,record_sha256}`结构，另含`verification_mode: external_review_gate`与认证边界。宿主外部注册表顶层也须登记同一冻结标准版本、注册库哈希与执行配置哈希；每个事件须逐项匹配角色、审查者、来源、决定、当前materials lock、冻结物料及两份标准哈希。报告、回执及其嵌套对象均采用闭合字段集，不能夹带本地放行或课堂效果声明。缺外部注册表时G4候选验证失败关闭；但项目外JSON仍不是密码学身份凭证，因此本地验证成功只表示“终审候选结构与宿主所给记录一致”，不能自行转成项目内放行状态。真正宿主放行是部署/对话层事件，不写回可由内容进程修改的项目文件。两份回执同时记录对G1同一所有者事件引用的人工复核。

`audit-report.v1`严重度只允许`P0/P1/P2/P3`精确枚举，不得有开放P0/P1/P2；`p3_risks[]`使用`category/statement/verification_plan`结构，恰好覆盖`office_rendering/classroom_pacing/learning_effect`三类残余风险。报告至少登记G0—G3、strict schema和原则检查结果，并保存最终同一冻结候选连续两轮、不同`round_id`、仅剩P3的复审记录。验证器会递归重跑G3及全部上游、重跑原则检查、重算冻结物料哈希，不信任单独写下的`exit_code: 0`。

验证：`python3 scripts/validate_lesson_audit.py <audit_lock.json> --external-event-registry /宿主只读挂载/external_review_registry.json`。命令通过只生成/验证`awaiting_host_release`候选；宿主另行确认后才可进入S6，项目内不得生成“已放行”凭证。

## S6 OBS宿主放行引用

S6每条`OBS-*`在课程版本与机制节点之外，必须带：

- `g4_audit_lock_sha256`：宿主所放行G4候选的完整SHA-256；
- `host_release_event_id`：项目外宿主事件ID；
- `host_release_source: {locator,record_sha256}`：可追溯宿主记录。

运行`python3 scripts/validate_evidence.py <obs.jsonl> --type obs --host-release-registry /宿主只读挂载/external_host_release_registry.json`。注册表必须位于项目目录外、schema为`external-host-release-registry.v1`；事件须由宿主核验且逐项匹配`lesson_id/g4_audit_lock_sha256/locator/record_sha256/decision`。缺失时S6默认失败关闭，项目内`_meta/host_release*.json`一律视为伪放行凭证。
