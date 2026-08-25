---
name: yuwen-audit-lesson
description: 高中语文课独立终审与宿主放行准备（G4/S5）。当G3物料完成后，需要冻结标准、复核哈希链、逐页功能审计、独立双审并形成待宿主放行候选时使用；审查者不直接代修教学内容，项目文件不得自称已放行。
---

# 独立终审与宿主放行准备（S5）

服务机制节点：K5/U1/U2/U3/U5/U6/U7/U8/J3/J4/J5/J6/J7 的 machine_check 与 review_gate 集中地。执行依据：`work/methodology/manuals/S5-审计手册.md`的`MM-S5-01`—`MM-S5-11`；逐页判据见`work/methodology/lesson-preparation/逐页功能审计与放行协议.md`。本skill只编排审查、记录缺陷与复验，不写或修教学内容。

创建G4冻结锁或排查血缘异常时读取 `../_shared/lesson-lineage-contracts.md` 的G4节，不由终审者补写上游锁。

## 输入

- S4 物料包（含 manifest）
- 有效 `materials_lock.json` 及完整G0—G3锁链
- 审查开始时**冻结的标准版本**（收敛规则：`work/evaluation/convergence.md`）

## 步骤

1. **确认独立性**：终审者不得是本轮教学内容作者；作者可以解释证据，不能自行放行。
2. **冻结标准**：把本次审查所用的完整原则注册库和实际执行的`enforcement_config`复制到同课reviews目录，分别记录路径、SHA-256、STANDARD-X.Y和带时区冻结时间；冻结注册库必须通过完整注册库校验，不能缩成空节点或伪原则。本轮递归校验与原则检查只读冻结配置，审查期间live注册库变更不影响本轮（不追溯否决）。
3. **先验血缘**：运行 `validate_lesson_lineage.py materials <materials_lock.json>` 并经 `yuwen-flow` 回归G0—G3；任一上游失效即停止审美审查。
4. 跑机器检查全链：
   ```bash
   python3 scripts/checks/run_principle_checks.py --lesson-json <lesson.json> --name <id> --strict
   python3 scripts/checks/check_trace_evidence.py --lesson-json <lesson.json> --strict
   ```
   《氓》历史重型链只在审查其兼容候选时附加运行，不是新课文G4通用入口。
5. 继续执行删除审判、六门、23项反退化测试、视觉功能审查、学生接收审查和五维节奏审计。
6. 输出缺陷与责任阶段；审查skill本身不改教案、设计或PPT。作者修复后，原审查者只复验受影响模块及其上游回归。
7. 按收敛规则裁决返工/重建/提交宿主；同一冻结候选连续两个不同`round_id`的复审仅剩P3，方可生成同课`_meta/reviews/`双审回执、审计报告和`_meta/audit_lock.json`。锁内`status`固定为`awaiting_host_release`。报告与回执精确绑定当前materials lock、冻结物料、注册库和执行配置哈希，且使用闭合字段集。宿主另提供项目目录外的`external-review-registry.v1`，其标准快照和每个审查事件也必须绑定这四类当前哈希；运行`python3 scripts/validate_lesson_audit.py <audit_lock.json> --external-event-registry <宿主只读路径>`。命令通过只证明本地候选与宿主所给审查记录一致，随后提交宿主作项目外放行裁决。

## 提交宿主的条件

- 机器检查全过 + 双审严重度仅使用精确`P0/P1/P2/P3`枚举，P0/P1/P2清零（或按收敛规则放行）；
- G4 audit lock递归验证G0—G3，冻结凭证（对象哈希、非空且绑定版本的标准快照、审查回执）写入同课`_meta/reviews/`；
- 两名审查者各自绑定结构化、可追溯且不同的外部review event/source，并通过宿主目录外事件注册表核验；同时人工复核G1外部所有者事件引用，本地JSON门不被表述成人类身份认证；
- `audit_report.p3_risks`结构化覆盖Office真实渲染、课堂节奏与学习效果三类等待实证风险，各有验证计划；
- 报告明确"真实课堂仍待试教"（P-12）。
- 审查者与作者身份分离；审查记录不得混入制作修改。
- `audit_lock.status`为`awaiting_host_release`；本地机器不得写`released`，不得把命令通过表述为宿主已放行。真正放行属于项目外宿主/对话层事件，宿主确认后方可进入S6。

## 常见错误

- 用更严的新标准追溯否决旧候选（违反收敛规则，历史教训：V6.5 双审清零旋即被推翻）；
- 一轮检查"零发现"就宣布完美——先怀疑检查力度（P-29）；
- 平均分妥协（P-21）。
