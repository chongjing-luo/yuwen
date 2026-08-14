---
name: yuwen-selfcheck
description: 语文项目全局自检与迭代循环。当完成任何阶段工作后、或需要评估项目健康度（理念覆盖、机制落地、测试、两本账）时使用。
---

# 全局自检与迭代（yuwen-selfcheck）

服务全部机制节点的治理面。产出可度量的一致性结论——"理念贯彻"从主观感受变成检查单。

## 步骤

1. **注册库自检**（理念层完整性）：
   ```bash
   python3 scripts/checks/validate_principle_registry.py --report work/evaluation/reports/principle_coverage.md
   ```
   关注：节点覆盖缺口（planned 警告）、"仅追溯强制"清单（active 但无 machine/review 强制的原则）。
2. **课程数据底线检查**（若有在制课程）：
   ```bash
   python3 scripts/checks/run_principle_checks.py --lesson-js <lesson.js> --name <id>
   python3 scripts/checks/check_trace_evidence.py --lesson-js <lesson.js>
   ```
3. **环节产物校验**（若有）：homework / assessment 校验器。
4. **全量测试**：`python3 -m pytest tests/ -q`（418+ 全绿为基线）。
5. **写报告**到 `work/evaluation/reports/selfcheck_<日期>.md`，按三目标分账：
   - 桌面已验：通过的检查清单（列标准版本）；
   - 已知缺口：样板发现数、planned 节点、未覆盖原则；
   - 待课堂验证：全部课堂度量（未试教前为空）。
6. **迭代决定**：按缺口严重度排下一步——样板 > 0 → 下一个候选必须清零；节点无强制 → 补检查器或审查门；测试红 → 先修再继续。

## 评估标准（自迭代纪律）

任何新内容入库前自问五件套：机制节点归属 / 环节落点 / 强制点 / 度量 / 诚实边界——缺一不收。
任何一轮修改后：测试绿 + 注册库校验过 + 覆盖报告更新，三件事缺一不可。

## 常见错误

- 自检报告只写"通过"不写缺口（应两本账如实）；
- 用新增检查追溯否决在审候选（收敛规则禁止）；
- 报告后不行动——缺口必须转化为下一步决定。
