# 全局自检报告 2026-08-15

标准版本：STANDARD-1.0

## 桌面账（设计条件）

### ✅ 原则注册库自检

    112 原则 / 20 节点 / 0 错误

### ✅ 课程数据底线检查（meng_v66）

    [PASS] frontstage_banned
    [PASS] timebox_conservation
    [PASS] three_questions_present（3）
    [PASS] total_minutes
    [FINDINGS] boilerplate_trace（188）
    报告已写入 /home/ubuntu/homes/LuoChongjing/Methods/yuwen/work/evaluation/reports/principle_checks_meng_v66.json
    课堂账：空——未真实试教（两本账纪律，P-12）

### ✅ 全量测试（pytest）

    ........................................................ [ 90%]
    .........................................                      [100%]
    453 passed, 30 subtests passed in 71.82s (0:01:11)

### ✅ 机制节点覆盖

    - 知识学习: 原则映射 8，机器 4，追溯 3，审查 3
    - 能够学懂: 原则映射 100，机器 38，追溯 38，审查 53
    - 享受学习: 原则映射 47，机器 15，追溯 15，审查 35
    - 仅追溯强制缺口：无（active 原则均有 machine/review 强制或为 meta）

## 课堂账（效果证据）

- 状态：**空——未真实试教**（两本账纪律，P-12）。全部桌面通过仅证明设计条件具备。
- 待采集信号见 `scripts/checks/run_principle_checks.py` 报告的 classroom_account。
