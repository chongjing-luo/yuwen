---
name: yuwen-audit-lesson
description: 高中语文课质量审计与放行（S5 环节）。当需要对课件做逐页功能审计、六门检查、双审否决、节奏审计、冻结放行时使用。
---

# 质量审计与放行（S5）

服务机制节点：K5/U1/U2/U3/U5/U6/U7/U8/J3/J4/J5/J6/J7 的 machine_check 与 review_gate 集中地。协议：`work/备课/逐页功能审计与放行协议.md`。

## 输入

- S4 物料包（含 manifest）
- 审查开始时**冻结的标准版本**（收敛规则：`work/evaluation/convergence.md`）

## 步骤

1. **冻结标准**：记录本次审查所用的 STANDARD-X.Y 与注册库哈希；审查期间注册库变更不影响本轮（不追溯否决）。
2. 跑机器检查全链：
   ```bash
   python3 scripts/checks/run_principle_checks.py --lesson-js <lesson.js> --name <id>
   python3 scripts/checks/check_trace_evidence.py --lesson-js <lesson.js>   # 反样板
   python3 scripts/validate_meng_v6_page_audit.py --mode stage|freeze-candidate|freeze|release  # 《氓》链
   ```
3. **删除审判**（P-39）：逐页默认应删除，由设计举证保留资格。
4. 六门审计（A-05…A-10）：G1 前置缺失 / G2 功能重复 / G3 覆盖虚假 / G4 变化不可观察 / G5 产物孤儿 / G6 可无损合并。
5. 23 项反退化测试（A-T01…A-T23）逐页执行——重点：教师抢答（T01）、多渠道泄答（T04）、活动遮蔽故事（T06）、程序成本（T08）、协议指纹（T17）。
6. 独立双审：视觉功能审查 + 学生接收审查，审查者与本轮作者分离；意见须含页面、证据、严重度、可执行修复（P-21 缺陷否决制）。
7. 全课节奏五维矩阵审计（J5）；模块失败率 > 1/4 或同根因贯穿 3 页 → 触发整体重建（P-43）。
8. 修复 → 原审查者复验 → 回归所属模块。
9. 收敛判定：按 `work/evaluation/convergence.md` 决定放行/返工/重建——连续两轮仅 P3 可"桌面已验·待试教"放行。

## 放行条件

- 机器检查全过 + 双审 P0/P1/P2 清零（或按收敛规则放行）；
- 冻结凭证（对象哈希、标准版本、审查回执）写入 reviews；
- 报告明确"真实课堂仍待试教"（P-12）。

## 常见错误

- 用更严的新标准追溯否决旧候选（违反收敛规则，历史教训：V6.5 双审清零旋即被推翻）；
- 一轮检查"零发现"就宣布完美——先怀疑检查力度（P-29）；
- 平均分妥协（P-21）。
