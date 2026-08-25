# AGENTS.md — 语文全流程教学辅助系统

本项目为高中语文教师提供覆盖教学全流程的辅助，包括知识与资料库、教学方法论、课程设计、课堂物料、评价反馈及各环节自动化机制。项目级要求是：资料可信、流程可执行、产物可追溯，课堂效果不被桌面推演冒充。

## 稳定入口与适用边界

- 当前备课方法采用“学到有价值的知识、真正学懂、享受学习”三目标工作框架及K/U/J机制节点：`work/methodology/lesson-preparation/备课三目标与实现机制.md`。它是可修订的备课方法组件，不是项目宪法或所有工程工作的普遍准入条件。
- 教学全流程地图：`docs/workflow/教学全流程地图.md`。
- 备课原则、教学活动、课堂观察和教学效果解释可以引用K/U/J节点；资料入库、目录、脚本、schema和工程治理按各自数据契约与验收标准执行。
- 当前开发方向、课程候选状态和阻断项只写入根目录`DEVLOG.md`，不在本文件维护动态任务进度。

## 范围控制与净结果交付

### 1. 区分工作过程与最终交付物

- **工作过程**：为形成结果而产生的检索记录、候选方案、初稿、首轮渲染、调试信息、比较材料和临时验证输出。
- **最终交付物**：用户或下游协作者实际使用的当前文件、界面、课程物料、代码、配置、报告、数据及最终回复。
- 工作过程放在`Tmp/`、指定workbench或正式审计位置；最终交付目录只保留当前可直接使用的成果及其成立所必需的文件。
- 不把工作记录、首轮版本、废弃候选或调试输出混入最终交付目录。

### 2. 只完成确认范围

只完成用户明确要求的内容，以及让这些内容正常成立所必需的配套工作。

以下属于必要配套工作，无需另行请示，但不得改变已确认的用户可见结果：

- 只读检索、来源核对、格式整理和兼容处理；
- 项目既有流程要求的测试、校验、哈希、门禁、账本和目录登记；
- 已确认合同内的排版适配、错误修复和可用性检查；
- 为生成指定文件必须使用的现有依赖和既有构建链。

以下行为会扩大范围，必须先在聊天中提出并取得确认：

- 新增页面、功能、活动、知识内容、视觉元素、组件或数据字段；
- 改变教学逻辑、信息结构、产品规则、正式目录或交付角色；
- 引入新的依赖、外部服务、费用、安全风险或显著维护成本；
- 把“优化”“做得更好”扩展成另一项独立任务。

不会实质改变结果的小问题采用最简单、最符合现有内容的方案，不建立额外机制。

### 3. 以最新确认状态为准

- 用户最新一次明确确认决定当前候选和最终交付状态，覆盖此前尚未定稿的讨论及代理自行提出的内容。
- 用户否定、撤回或要求删除的代理候选，不进入当前正式产物，也不以“已删除”“未采用”等说明继续留在交付物中。
- 修改后按最终要求重新审视整体结果，不在旧方案上持续叠加补丁、辩解和过程说明。
- 文件名、页面标题和组件名使用自然的正式名称；除非移除本身是必须传达的信息，不使用“无XX版”“已去除XX”“修订后版本”等带修改痕迹的命名。

最新确认不覆盖必须保存的事实与治理记录：

- L4课堂证据、原始资料、来源记录和其他只追加数据；
- Git历史、ADR、审查回执、哈希锁、manifest和正式审计记录；
- 已按冻结标准进入审查的候选及`work/evaluation/convergence.md`规定的不追溯否决规则。

新决定需要改变上述对象时，按其版本、迁移或追加契约形成新的当前状态，不改写历史事实。

### 4. 按产物角色保持纯净

| 产物角色 | 应包含 | 不应包含 |
|---|---|---|
| 学生PPT、学习单和课堂前台 | 学生此刻需要面对的原文、任务、资源、作品和反馈 | 教学目标、学生画像、设计理由、时间盒、代理思路和审计状态 |
| 教案、教学设计和教师剧本 | 当前目标、知识、教学逻辑、活动、逐字稿及必要的设计理由 | 调试过程、废弃方案、代理自我解释和与教学无关的元文案 |
| 方法论、原则和操作规程 | 当前有效的概念、规则、适用条件、执行步骤和验收标准 | 本轮讨论流水、撤回内容和为证明遵令而写的解释 |
| 正式代码、配置和测试 | 当前功能、接口、约束及验证当前合同所需的内容 | 错误尝试、废弃实现和修改过程辩解 |
| 审计、ADR、DEVLOG、QA和证据账 | 与其职责相符的问题、证据、决策、状态和追溯信息 | 与审计、决策或维护无关的制作过程 |
| 最终目录与最终回复 | 当前成果、必要入口、真实状态边界和关键验证结论 | 旧版本、调试文件、长篇修改流水和无关的下一步建议 |

产物脱离聊天记录后必须完整、自然、可理解、可直接使用。不得出现与当前角色无关的“我将”“我们可以”“本页面用于展示”“这里会”“实现了”等代理型或解释型元文案。

### 5. 过程信息只进入指定位置

过程、决策和证据信息只在下列情况保留：

1. 用户明确要求设计过程、方法论、工作日志或决策记录；
2. 文件本身承担过程或证据职责，例如`DEVLOG.md`、ADR、审查报告、QA、门禁锁、manifest、`.learnings/`和L4课堂证据；
3. 信息会实质影响兼容、迁移、安全、审计、回滚或后续维护；
4. 被移除内容原本属于用户提供的正式材料，且移除本身是当前任务的一部分。

代码注释只解释当前仍然有效且不易理解的约束。测试表达当前合同，不记录调试历史。除非用户或既有工作流要求，不为证明完成任务而额外创建说明、QA或变更日志。

### 6. 交付前静默检查

每次交付前自行检查并直接清理普通问题，不把检查过程写入交付物：

1. 是否增加了用户没有要求且并非结果成立所必需的内容；
2. 是否残留被否定的方案、名称、结构或解释；
3. 是否在描述修改过程，而不是呈现当前结果；
4. 产物是否符合自己的角色，脱离聊天后能否直接使用；
5. 是否存在无功能的页面、元素、注释、文件或说明；
6. 最终目录是否只包含当前交付所需文件；
7. 必须保留的来源、证据、审计和版本记录是否完整。

只有阻断、风险、正式门禁结论或用户明确要求的验证信息需要在最终回复中说明。

## 开发阶段与DEVLOG

当前处于开发阶段。`DEVLOG.md`是唯一的当前优化方向清单：

- 每轮工作从读取`DEVLOG.md`开始，按优先级选择与当前请求相符的方向；
- 新方向写明问题来源、作用范围和验收标准；教学方法规则另按收敛规则记录目标框架映射与触发事件；
- 更新时将旧版本整体移入`docs/devlog/archive/DEVLOG_<日期>_v<序号>.md`并标注各条完成情况；
- `DEVLOG.md`只保留最新内容，条目采用“方向＋验收标准”的简要格式。

## 目录导航

| 路径 | 内容 |
|---|---|
| `DEVLOG.md` | 当前优化方向清单；旧版归档于`docs/devlog/archive/` |
| `docs/architecture/项目设计方案.md` | 系统总体架构 |
| `docs/architecture/ID解析表.md` | 稳定ID到实体的机器寻址规则 |
| `docs/architecture/storage-layout.json` | 规范根、旧根禁用和重要路径契约 |
| `docs/decisions/ADR-001-统一方法论与高考资料存放.md` | 方法论与高考资料存放决策 |
| `docs/decisions/ADR-002-三目标降为备课方法工作框架.md` | 三目标适用层级决策 |
| `docs/workflow/教学全流程地图.md` | S0—S9教学全流程 |
| `Data/reference/` | 有来源记录、可核验的规范参考原件 |
| `Data/reference/curriculum/普通高中语文课程标准（2017年版2020年修订）_教育部官方版.pdf` | 现行高中语文课程标准规范原件 |
| `Data/textbook_extract` | 教材与教师用书MinerU解析源包 |
| `work/methodology/README.md` | 人读方法论唯一入口 |
| `work/methodology/lesson-preparation/备课基本原则.md` | 备课原则人读权威文本 |
| `work/methodology/lesson-preparation/语文备课操作规程.md` | 单篇备课唯一总流程 |
| `work/methodology/manuals/README.md` | S0—S9专项操作手册入口 |
| `work/principles/README.md` | 人读方法与机器原则的职责边界 |
| `work/principles/registry.yaml` | 机器原则注册真相源 |
| `work/evaluation/README.md` | 评估制度、标准收敛和检查报告入口 |
| `work/knowledge/README.md` | 机读知识库入口与领取协议 |
| `work/knowledge/_meta/catalog.jsonl` | 全库实体目录生成物，不手编 |
| `work/knowledge/exams/README.md` | 高考资料唯一入口与分层规则 |
| `work/knowledge/exams/papers` | 试卷、题目、答案候选及卷内账本的实体真相源 |
| `work/knowledge/exams/views/by_type` | 可重建的题型索引视图 |
| `work/knowledge/exams/research` | 带来源和状态边界的研究报告 |
| `work/knowledge/exams/workbench` | 切片、草稿、队列、候选和批处理过程件 |
| `work/teaching` | L2课程数据、作业包和L4课堂证据 |
| `Tmp/` | 外部资料入口及临时加工区；除README外不入Git |
| `scripts/` | 构建器、校验器、检查器和知识库脚本 |
| `scripts/checks/validate_storage_layout.py` | 存放契约与重要路径校验器 |
| `.agents/skills` | 教学全流程、资料轴及工程治理skill |
| `.learnings/` | 可晋升为原则的经验与错误记录 |

## 唯一存放规则

1. 同一语义类别只设一个规范根：人读方法论归`work/methodology/`，机器原则归`work/principles/`，评估治理归`work/evaluation/`，高考资料归`work/knowledge/exams/`。
2. 实体与视图严格分离：`papers`是真相源；`views`只能由脚本重建；`research`保存带状态边界的研究报告；`workbench`保存未定稿的过程件；`_meta`保存协议、映射和冻结记录。
3. 不建立同内容副本、兼容目录或旧路径软链接。跨目录只写链接；迁移同时修改脚本、账本、文档引用和ID解析规则。
4. 新增重要路径先更新`docs/architecture/storage-layout.json`；架构性变更另写ADR，再更新本表。运行`python3 scripts/checks/validate_storage_layout.py`通过后才可完成迁移。

## 工作流入口

单篇备课以三阶段为正式主链：

`yuwen-author-lesson-plan`（S2教案，内部可调用`yuwen-research-text`完成G0研究）→ `yuwen-design-lesson`（S3教学设计）→ `yuwen-build-materials`（S4 PPT与物料）

完成后由`yuwen-audit-lesson`独立执行G4终审。它不是第四个制作阶段；项目内最多生成`awaiting_host_release`候选，真正放行属于项目外宿主或对话层事件。

S3必须把完整设计投影为同课唯一人读`教学设计.md`供用户逐页审批。只有用户明确批准当前Markdown、`lesson.json`和G1锁三项哈希后，才可写`G2_owner_approval.json`与`design_lock.json`，不得以JSON、摘要或旧批准代替。具体课程的当前状态服从`DEVLOG.md`和该课锁文件。

课后流程：`yuwen-trial-observation` → `yuwen-design-homework` / `yuwen-grade-feedback` → `yuwen-author-assessment` / `yuwen-diagnose-learning` → `yuwen-reflect-lesson`。

外部资料流程：`yuwen-intake` → `yuwen-organize` → `yuwen-curate`（→ `yuwen-catalog`）。

`yuwen-flow`只执行所选环节门禁，不生成内容或放行决定；`yuwen-selfcheck`在内容主链之外执行全局治理。

## 环境安装

```bash
pip install -r requirements.txt
npm install
```

## 验证命令

```bash
# 知识库账本校验
python3 scripts/validate_knowledge_base.py
# 存放契约与重要路径校验
python3 scripts/checks/validate_storage_layout.py
# 原则注册库与操作治理校验
python3 scripts/checks/validate_principle_registry.py
python3 scripts/checks/validate_operational_governance.py
# 有在制课程数据时运行；PATH/ID替换为当前课程数据
python3 scripts/checks/run_principle_checks.py --lesson-json PATH --name ID
# 测试
python3 -m pytest tests/ -x -q
node tests/test_lib_theme_sync.js
# 全量自检
python3 scripts/run_selfcheck.py
```

## 硬性纪律

1. **两本账**：桌面验证只证明设计条件具备；学生理解、享受和掌握的断言必须来自真实课堂证据。宿主确认前，G4最多写“本地终审候选结构已验·待宿主放行”；宿主在项目外确认后、真实试教前，才可在宿主记录中写“桌面已验·待试教”。项目文件不得自造放行状态。
2. **原则即机器**：理念必须落到注册库的`enforcement`（`machine_check` / `design_trace` / `review_gate`）；人读文档更新时同步注册库锚点。
3. **反样板**：设计字段填入默认模板串视为未落实；使用`scripts/checks/check_trace_evidence.py`检查。
4. **不追溯否决**：候选按审查开始时冻结的标准版本评审；新原则进入下一版本，不用于推翻已进入流程的候选。具体规则见`work/evaluation/convergence.md`。
5. **版本管理**：正式目录只保留当前版本；旧版进入Git历史；不永久删除处理教学成果。
6. **测试先行**：修复bug先写失败测试；构建器改动必须执行`python3 -m pytest tests/ -q`和Node测试全量回归。
7. **资料三纪**：外部资料必须经过`Tmp/inbox`台账裁决；实体入册即登记catalog；L4证据只追加并绑定课程版本，其中用于解释教学效果的课堂记录再按当前备课目标框架标注机制节点。

## 数据治理

- `Data/reference/`只收有来源记录、可核验版本的规范材料；AI输出与第三方题库不作为规范Artifact。
- 教材、教师用书、试卷及第三方参考原件只在本机保留，不进入公开Git历史；整理后的Markdown、JSON、知识卡、题目切分、来源登记和MinerU结果公开。
- `work/knowledge/_meta/artifacts.jsonl` 以 `repository_visibility` 区分 `public` 与 `private_local`；后者可在公开工作树缺席，但本机存在时必须通过大小与SHA-256校验。
- 知识交付物使用`work/knowledge/_meta/deliverables.jsonl`状态机；领取任务前`python3 scripts/validate_knowledge_base.py`必须通过。
- 大体积原始暂存和批处理过程件不进入Git。
