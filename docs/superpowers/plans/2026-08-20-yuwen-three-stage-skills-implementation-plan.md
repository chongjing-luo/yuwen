---
document_type: implementation_plan
status: "in-progress-independent-remediation"
completion_boundary: "原定G0—G3重构已完成；最终独立审查追加的G4、十八字段、OOXML关系树、全课程selfcheck与认证边界修复正在回归；未取得任何课例G1批准，课堂账为空"
date: "2026-08-20"
design: "docs/superpowers/specs/2026-08-20-yuwen-three-stage-skills-design.md"
mechanism_nodes: [K1, K2, K4, K5, U1, U4, U6, U8, J4, J5, J7]
---

# 语文备课三阶段 skill 架构实施计划

## 总体决策

以 S2 教案（内含 G0 证据研究）、S3 教学设计、S4 PPT与物料为三个正式阶段。G4终审和全局治理保持独立，但不算内容制作阶段；`yuwen-flow`只执行门禁，`yuwen-audit-lesson`只作放行判断，`yuwen-selfcheck`只审系统健康。

## Task 1：建立 G0/G1 可执行契约

**目标**：新增证据与教案验证器，使“有证据、有完整教案、有哈希绑定回执”成为可机器拒绝的条件。

**验收标准**：

- 先写失败测试，覆盖有效样本、规范原件缺失、哈希漂移、目标/KID孤项、defer无理由、审核回执错绑；
- `validate_lesson_evidence.py`与`validate_lesson_plan.py`使测试转绿；
- 机器只审结构、血缘和覆盖，不用标题词匹配冒充语义质量。

**验证**：`python3 -m pytest tests/test_validate_lesson_evidence.py tests/test_validate_lesson_plan.py -q`。

## Task 2：接通 G1→G2→G3 失效链

**目标**：课程数据绑定已批准教案，物料契约绑定教学设计；上游修改能自动使下游失效。

**验收标准**：

- 先扩展测试，证明缺 G1 锁、教案哈希变化、锁定目标/KID/三问/阶段漂移均被拒绝；
- `validate_lesson_schema.py`兼容 legacy，但新候选 strict 模式强制有效上游绑定；
- materials lock 的通用验证不依赖某一篇课文的专用构建器。

**验证**：相关定向测试＋`tests/test_validate_lesson_schema.py`全绿。

## Task 3：重构三个主 skill 与支持/门禁 skill

**目标**：使新 agent 只从教案主 skill 进入正式备课，文本研究只提供候选，后两阶段不能越权。

**验收标准**：

- 新建`yuwen-author-lesson-plan`；
- 更新`yuwen-research-text`、`yuwen-design-lesson`、`yuwen-build-materials`、`yuwen-flow`、`yuwen-audit-lesson`、`yuwen-selfcheck`；
- 每个skill写清输入、产物、禁止越界、失败回流和机制节点；
- 全部通过skill quick validation。

**验证**：逐skill `quick_validate.py`＋关键措辞交叉检查。

## Task 4：同步手册与项目入口

**目标**：消除S2/S3旧职责残留，保证操作规程、手册、AGENTS和流程地图只有一套主链。

**验收标准**：

- S2手册覆盖教案与内部证据研究，S3手册只负责教学设计；
- 更新`.agents/skills/README.md`、`AGENTS.md`、全流程地图和项目设计方案；
- “整体教学逻辑”明确覆盖导入、背景、文本、知识形成、讨论、总结、迁移及按需高考/时代材料；
- 不再出现“文本研究可直接进入lesson.json”或“S3第一步写教案”的有效入口。

**验证**：`rg`一致性审计＋手册校验测试。

## Task 5：迁移试跑与独立前向审查

**目标**：用《沁园春·长沙》当前候选证明链条诚实工作，再让新鲜上下文审查者尝试绕过教案。

**验收标准**：

- 不伪造所有者回执；当前教案应准确停在G1候选；
- 独立审查确认无法从文本研究直接跳到教学设计/PPT；
- 审查发现的真实缺陷完成修复与复验。

**验证**：试跑记录＋独立审查报告。

## Task 6：全局回归与收口

**目标**：确认新架构没有破坏原则、知识库和既有测试，并更新开发方向。

**验收标准**：

- 原则注册库校验、原则检查、Python全量测试和在役Node测试通过；
- 自检报告分开桌面账与课堂账；
- DEVLOG按归档规则更新；宿主确认前G4最多为“本地终审候选结构已验·待宿主放行”，宿主项目外确认后、未试教时才为“桌面已验·待试教”。

**验证**：`scripts/run_selfcheck.py`及显式全量命令退出码均为0。

## Task 7：独立终审追加整改

**目标**：修复最终独立审查发现的“文字上有G4但无通用锁”、v2合同少验字段、伪OOXML包、selfcheck固定抽样及本地身份认证过度声称。

**验收标准**：

- strict v2强制A-01十六项合同＋两个跨页预算和显式timeboxes；
- PPTX通过OPC核心成员、ContentType、根关系、presentation—slide关系及XML命名空间解析，Office渲染仍另作QA；
- 新建通用`audit_lock.v1`与验证器，递归G0—G3并绑定标准快照、冻结物料、视觉/学生接收双审；
- 原则检查支持lesson.json，selfcheck遍历全部课程链，不再默认历史《氓》对象；
- 所有路径项目根相对、同课元数据共置；G1/G4明确本地机器不认证真实人类身份，外部review gate不可被自报字段冒充。

**验证**：新增失败测试转绿、全量Python/Node/知识库/原则/skill校验通过，并再次由独立agent前向审查。
