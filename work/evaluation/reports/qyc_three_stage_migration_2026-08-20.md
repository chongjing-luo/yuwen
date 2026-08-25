---
document_type: lesson_workflow_migration_report
lesson_id: LES-B1-QYC-01
date: "2026-08-20"
status: "G0通过；G1待所有者审核；未试教"
mechanism_nodes: [K1, K2, K4, U4, U6, J4, J7]
standard: "语文备课操作规程 v0.3 candidate-g1-trial"
---

# 《沁园春·长沙》三阶段迁移试跑

## 结论

当前候选已完成新链G0结构与血缘验证，必须停在G1所有者审核前。没有创建 `G1_owner_approval.json` 或 `lesson_plan_lock.json`，因此不能进入教学设计、lesson.json或PPT制作。这是门禁正常工作，不是缺失步骤被忽略。

两轮独立前向审查后，门禁完成严格化：G1递归重跑G0并把所有者真实性明确留在外部人工review gate；G2 strict只接受v2，强制A-01十六项合同＋两个跨页预算、页面目标/KID、阶段顺序、完整母版总时长和收束方式；G3解析OPC核心成员、ContentType、根关系与presentation—slide树，同时保留Office打开/渲染QA；S5新增通用G4 audit lock，绑定标准快照、冻结物料与视觉/学生接收双审。selfcheck改为遍历全部课程链。这些改进没有改变本课的诚实停止点。

## G0证据门

- 证据清单：`work/teaching/必修上册/沁园春长沙/_meta/evidence_manifest.json`；
- 规范根：统编必修上册完整教材PDF、2017年版2020年修订课标PDF；
- 派生层：本课PDF切片、MinerU `full.md`，均绑定完整教材PDF登记哈希；
- 知识层：`CARD-B1-U01-01`与`UNIT-B1-U01`；
- 证据档案：`TR-B1-U01-01_文本研究.md`；
- 命令：`python3 scripts/validate_lesson_evidence.py <manifest>`；
- 结果：退出码0，规范源2、派生源2、知识源2。

机器通过只证明路径、SHA-256、规范原件优先和派生绑定等设计条件。教材切片与完整教材之间的语义切分正确性仍由既有教材管线与人工回页记录承担，不由哈希关系自动证明。

## G1诚实停止点

- 当前人读教案：`work/teaching/必修上册/沁园春长沙/教案.md`；
- 当前教案SHA-256：`566bc680dd9ec02b13f6e3bb34d469a5260f416313b0a06ff5f9a8f887d18d08`；
- 状态：`G1教案候选·待所有者审核`；
- 所有者回执：不存在；
- G1锁：不存在；
- 下游教学设计、lesson.json、design lock、PPT与物料：不得生成。

教案若在所有者审核前后发生任何字节变化，批准回执必须绑定变化后的新SHA-256；不得复用本报告记录的候选哈希。

## 课堂账

尚无真实试教、学生作品或测评数据。学生是否学到、学懂或享受均未验证。

## 系统回归

- 全部18个项目skill通过`skill-creator` quick validation；
- G0—G4、十八字段、OOXML、原则JSON入口和全课程selfcheck定向测试81项通过；
- `python3 -m pytest tests/ -q`退出码0；
- 在役Node测试、知识账本、116条原则/20节点注册库和原则体系映射均通过；
- `scripts/run_selfcheck.py`退出码0，发现并验证`必修上册/沁园春长沙`，报告“G0通过；G1待所有者审核；下游为空”；课堂账仍为空；
- 通用S4构建入口尚未完成，已进入`DEVLOG.md` v6，不以G3契约和校验器冒充构建能力。
