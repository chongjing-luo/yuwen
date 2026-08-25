---
name: yuwen-diagnose-learning
description: 高中语文学情诊断（S8b 环节）。当需要录入作业/测验掌握数据、生成 KP 掌握热图与回教建议时使用。
---

# 学情诊断（S8b）

服务机制节点：**K1（四站第四站闭环）、K3（掌握记录）、K4（班级知识地图）**。执行依据：`work/methodology/manuals/S8-命题诊断手册.md`的`MM-S8-05`与`MM-S8-06`。

## 输入

- mastery ledger：`work/teaching/_classes/<班级>/mastery_ledger.jsonl`（S8只追加MR；格式见 `scripts/analyze_mastery.py` docstring）
- 数据来源：批改记录（yuwen-grade-feedback 产出）、测验成绩、观察记录

## 步骤

1. 逐行追加**真实**观测到 ledger（诚实纪律：不生成推演数据）：`{date, class_id, student_id, source{type,ref}, kp_id, score, max_score, error_type?}`。
2. 错因类型必须可操作（如"现代义干扰""推断当诗写"），不写"粗心"。
3. 运行：`python3 scripts/analyze_mastery.py <ledger.jsonl> --out work/teaching/<班级>/diagnostics/掌握热图_<日期>.md`。
4. 读报告做决定：
   - 低于阈值的 KP → 回教方案：回到知识卡与课堂落点，重走"首答—校准—个人末答"循环，并排下次闭卷检索（K3）；
   - 高掌握 KP → 进入间隔回投清单（不重复教）；
   - 个别学生薄弱 → 分层作业指定题（联动 yuwen-design-homework）。
5. 回教建议同步给 S9 反思与 S1 下一轮规划。

## 放行条件

- ledger 条目 kp_id 全部解析到知识卡（脚本强校验）；
- 每条低掌握 KP 的回教方案绑回具体卡片与页面；
- 报告含"数据来源：真实作业/测验/观察记录"声明。

## 常见错误

- 用班级平均分掩盖两极（应看分布与个体）；
- 回教=再讲一遍（应为再检索+再修订）；
- 采集一次就停（K3 需要间隔多次观测才能谈"保持"）。
