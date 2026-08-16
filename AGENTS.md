# AGENTS.md — 语文全流程教学辅助系统

本项目为高中语文教师提供覆盖教学全流程的辅助：知识/资料库、方法论/理念库（通用教学 + 语文特异）、各环节自动化机制与 skill。一切工作服务于三个目标：**让学生学到更多有价值的知识、真正学懂、享受学习**。

## 使命与北极星（先读这个）

- 三目标的因果机制与 20 个机制节点（K1-K5 / U1-U8 / J1-J7）：`work/evaluation/三目标实现机制.md`
- 九环节全流程地图：`docs/workflow/教学全流程地图.md`
- **准入规则**：任何新内容（原则、skill 步骤、校验器、库条目、产物字段）必须引用至少一个机制节点，否则不收录。

## 开发阶段与开发日志

当前处于**开发阶段**。`DEVLOG.md`（根目录）是唯一的当前优化方向清单：

- 每轮工作从读它开始，按优先级取方向；新方向经收敛规则准入（北极星映射 + 触发事件）后写入；
- 更新时旧版本整体移入 `docs/devlog/archive/DEVLOG_<日期>_v<序号>.md` 并标注各条完成情况，`DEVLOG.md` 只保留最新内容；
- 条目保持简要：方向 + 验收标准各一行。

## 目录导航

| 路径 | 内容 |
|---|---|
| `DEVLOG.md` | 开发日志：当前优化方向清单（只留最新，旧版归档于 `docs/devlog/archive/`） |
| `docs/architecture/` | 项目设计方案（v0.9.x 待审计）+ ID 解析表（机器寻址规则） |
| `work/manuals/` | 手册之家：S0-S9 十册（可执行核心；条目六字段含 P0/P1/P2 优先级，不设数量上限） |
| `work/teaching/` | 设计层 L2（课程数据/作业包）与证据层 L4（`_classes/`：观察/批改/掌握/反思——学生数据如实入库不脱敏，只追加） |
| `Tmp/` | 外部资料唯一入口（inbox 台账 + work 加工区；永不入 git，README 除外） |
| `work/knowledge/` | 机读知识库：81 知识卡、28 单元图谱、5 册表（114/114 accepted）、高考分析、素材库 `materials/`；账本与契约在 `_meta/`（含 catalog） |
| `work/principles/` | 原则注册库（机器可读理念，每条绑定机制节点与强制方式） |
| `work/evaluation/` | 三目标机制、评估标准、收敛规则、自检报告 |
| `work/备课基本原则.md` | 44 条备课原则（人读权威文本，注册库的来源） |
| `work/备课/` | 审计协议、手法库、视觉规范、《氓》课例全部产物 |
| `work/`（根） | 四层八份方法论（课程理论/备课/课堂技术/PPT，各含通用版+语文版） |
| `docs/superpowers/` | 《氓》V4→V6.6 设计规格与实施计划（历史沿革） |
| `docs/workflow/` | 教学全流程地图 |
| `Data/reference/` | 规范参考原件（课标 PDF、17 年四川高考真题与登记账本） |
| `Data/textbook_extract/` | 144 个教材 MinerU 解析源包 |
| `scripts/` | 构建器（build_*）、校验器（validate_*）、检查器（checks/）、知识库抽取脚本 |
| `.agents/skills/` | 17 个 skill（12 环节 + 资料轴 4：intake/organize/curate/catalog + 工程轴 flow） |
| `.learnings/` | 经验与错误沉淀（可 promote 为原则） |

## 工作流入口（按环节）

备课从 S2 开始走：`.agents/skills/yuwen-research-text` → `yuwen-design-lesson` → `yuwen-build-materials` → `yuwen-audit-lesson`；课后走 `yuwen-trial-observation` → `yuwen-design-homework` / `yuwen-grade-feedback` → `yuwen-author-assessment` / `yuwen-diagnose-learning` → `yuwen-reflect-lesson`。外部资料入库走资料轴：`yuwen-intake` → `yuwen-organize` → `yuwen-curate`（→ `yuwen-catalog` 登记消费）。按环节跑门禁链：`yuwen-flow`；全局健康检查：`yuwen-selfcheck`。

## 环境安装（一次性）

```bash
pip install -r requirements.txt   # python 依赖
npm install                        # node 依赖（pptxgenjs/docx，本地 node_modules）
```

## 验证命令

```bash
# 知识库账本校验
python3 scripts/validate_knowledge_base.py
# 原则注册库自检 + 通用机制检查 + 覆盖报告
python3 scripts/checks/validate_principle_registry.py
python3 scripts/checks/run_principle_checks.py
# 测试
python3 -m pytest tests/ -x -q
node tests/test_meng_v66_lesson.js   # JS 测试逐个 node 运行
# 全量自检（注册库+检查+测试+报告）
python3 scripts/run_selfcheck.py
```

## 硬性纪律

1. **两本账**：桌面验证只证明"设计条件具备"；学生理解/享受/掌握的一切断言必须来自真实课堂证据（试教观察、学生作品、测评数据）。未试教前产物状态只能写"桌面已验·待试教"。
2. **原则即机器**：理念必须落到注册库的 enforcement（machine_check / design_trace / review_gate）；人读文档的更新要同步注册库锚点。
3. **反样板**：设计字段填了默认模板串 = 未落实。`scripts/checks/check_trace_evidence.py` 会检出。
4. **不追溯否决**：候选按审查开始时冻结的标准版本评审；新原则进下一版本，不用于推翻已进入流程的候选（收敛规则见 `work/evaluation/convergence.md`）。
5. **版本管理**：正式目录只保留当前版本；旧版进 git 历史；不用永久删除处理教学成果。
6. **测试先行**：修 bug 先写失败测试；构建器改动必须全量回归（`python3 -m pytest tests/ -q` + node 测试）。
7. **资料三纪**：外部资料必经 `Tmp/inbox` 台账（裁决四问后入库）；实体入册即登记 catalog（五件套）；L4 证据只追加、每条绑课程版本与机制节点。

## 数据治理

- `Data/reference/` 只收有来源记录、可核验版本的规范材料；AI 输出与第三方题库不作规范 Artifact。
- 知识交付物走 `work/knowledge/_meta/deliverables.jsonl` 状态机；领取任务前 `validate_knowledge_base.py` 必须 passed。
- 大体积原始暂存（如 `work/knowledge/_staging/`）不入 git。
