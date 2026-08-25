---
name: yuwen-selfcheck
description: 语文项目全局治理与自检。当原则、skill、schema、校验器、流程架构或重要课例发生变化，需要检查系统级一致性、测试和两本账时使用；不替代单课G0-G4门禁，也不必每个备课动作都运行。
---

# 全局自检与迭代（yuwen-selfcheck）

本 skill 负责系统级健康检查，独立于“教案→教学设计→PPT与物料”内容主链。它按对象分别检查教学方法映射、资料治理契约和工程契约；不审某一页该怎样改，也不替代G4终审。

## 步骤

1. **注册库自检**（理念层完整性）：
   ```bash
   python3 scripts/checks/validate_principle_registry.py --report work/evaluation/reports/principle_coverage.md
   ```
   关注：节点覆盖缺口（planned 警告）、"仅追溯强制"清单（active 但无 machine/review 强制的原则）。
2. **存放契约与操作治理引用图**：先运行`python3 scripts/checks/validate_storage_layout.py`，确认规范根、AGENTS重要路径和旧根禁用均通过；再运行`python3 scripts/checks/validate_operational_governance.py`，核对唯一规程active、当前98条MM六字段、16个阶段skill到真实MM的引用、1个决策支持skill的结构化治理合同与explicit-only策略，以及候选STANDARD的诚实状态。S1—S9教学条目核对K/U/J或教学原则锚点；S0资料条目核对数据治理来源，不为形式合法性强绑节点。
3. **全课程血缘巡检**：遍历`work/teaching/**`中出现人读`教案.md`、G0—G4对象、任意`materials/`文件、课目录根部PPTX/DOCX、`lesson.json`或`_meta/host_release*.json`的全部课目录，依次验证evidence manifest、lesson plan lock、lesson.json/design lock、materials lock、audit lock；项目内宿主放行凭证直接失败。报告每课第一个失效点，不抽查固定课例、不自动修锁。只有人读草案而无下游时可作“未进入G0”的诚实停止，不算G0通过；存在G4时还须由环境变量`YUWEN_EXTERNAL_REVIEW_REGISTRY`指向项目目录外宿主注册表，否则失败关闭。G4验证成功只能报告“本地终审候选结构已验、待宿主放行”，不得报告“已放行”。
4. **课程数据底线检查**（若有在制课程）：
   ```bash
   python3 scripts/checks/run_principle_checks.py --lesson-json <lesson.json> --name <id>
   python3 scripts/checks/check_trace_evidence.py --lesson-js <lesson.js>
   ```
5. **环节产物校验**（若有）：homework / assessment 校验器。
6. **全量测试**：`python3 -m pytest tests/ -q`。使用`--skip-tests`的快速巡检必须显示为“未执行”，返回非零，不得标成或宣称全量通过。
7. **只读课堂账统计**：只读遍历`work/teaching/_classes/`。零条才写“课堂账为空”；已有记录则按OBS/GRD/MR/REF/PR报告数量与文件，不修改L4、不据数量宣称效果。
8. **写报告**到 `work/evaluation/reports/selfcheck_<日期>.md`，按系统对象与两本账分区：
   - 桌面已验：通过的检查清单（列标准版本）；
   - 已知缺口：样板发现数、planned 节点、未覆盖原则；
   - 待课堂验证：全部课堂度量（未试教前为空）。
9. **迭代决定**：按缺口严重度排下一步——样板 > 0 → 下一个候选必须清零；教学原则无强制 → 补设计追溯或审查门；数据/工程契约无校验 → 补契约测试；测试红 → 先修再继续。

## 评估标准（自迭代纪律）

新内容入库前先判断对象类型：教学方法对象检查目标框架作用/环节落点/强制点/度量/诚实边界；资料对象检查来源/权威/血缘/状态/可寻址；工程对象检查问题来源/输入输出契约/失败边界/测试/回归。不用K/U/J作为后两类对象的通行证。
任何一轮修改后：测试绿 + 注册库校验过 + 覆盖报告更新，三件事缺一不可。

## 常见错误

- 自检报告只写"通过"不写缺口（应两本账如实）；
- 用新增检查追溯否决在审候选（收敛规则禁止）；
- 报告后不行动——缺口必须转化为下一步决定。
