# 共享参考：库路径索引（所有 yuwen skill 通用）

## 使命与北极星

- 三目标机制（20 节点 K/U/J 定义）：`work/evaluation/三目标实现机制.md`
- 全流程九环节地图：`docs/workflow/教学全流程地图.md`
- 项目宪法与验证命令：`AGENTS.md`

## 理念与原则

- 原则注册库（机器源，112 条）：`work/principles/registry.yaml`
- 强制配置（禁词表等）：`work/principles/enforcement_config.json`
- 人读权威文本：`work/备课基本原则.md`（43 条）、`work/备课/逐页功能审计与放行协议.md`、`work/备课/语文课堂教学手法库.md`、`work/备课/视觉与插图功能规范.md`

## 知识库

- 知识点卡/单元图谱/册表：`work/knowledge/<册>/cards|units/`（账本：`work/knowledge/_meta/deliverables.jsonl`）
- 教材解析源包：`Data/textbook_extract/<册>/mineru_result/<课>/full.md`
- 课标：`Data/reference/curriculum/`（PDF 为规范源）
- 高考语料与候选批次：`Data/2008-2024·（四川）语文高考真题/exam_extract/`、`work/knowledge/高考分析/kp_batches/`
- 命题题库与蓝图：`work/knowledge/assessment/`

## 方法论（人读，四层八份 + 原则）

见 `work/README.md` 导航：课程理论/备课方法论/教学环节技术/PPT 设计（各含通用版+语文版）。

## 机制节点速查

| 目标 | 节点 |
|---|---|
| 知识学习 | K1 教什么界定 · K2 文本位置生长 · K3 检索间隔 · K4 网络化 · K5 负荷预算 |
| 能够学懂 | U1 生成先于告知 · U2 证据锚定 · U3 校准后修订 · U4 困难→手法 · U5 负荷管理 · U6 解释分层 · U7 反例路径 · U8 理解闭环 |
| 享受学习 | J1 自主感 · J2 胜任感 · J3 关联感 · J4 文学愉悦 · J5 节奏多样 · J6 心理安全 · J7 流畅错觉防线 |

## 验证命令速查

```bash
python3 scripts/checks/validate_principle_registry.py            # 注册库自检
python3 scripts/checks/run_principle_checks.py --lesson-js <lesson.js> --name <id>
python3 scripts/checks/check_trace_evidence.py --lesson-js <lesson.js>
python3 scripts/validate_homework_package.py <homework_package.json>
python3 scripts/validate_assessment_package.py <blueprint.json>
python3 -m pytest tests/ -q                                       # 全量回归
```

## 硬性纪律（每个 skill 都适用）

1. 两本账：桌面验证 ≠ 课堂效果；未试教不得声称学生已理解/享受/掌握（P-12）。
2. 准入规则：产出物字段必须能引用机制节点，否则不加。
3. 反样板：字段不得用模板默认串充数（check_trace_evidence.py 会检出）。
4. 不追溯否决：候选按冻结标准版本评审（收敛规则）。
