# 全局自检报告 2026-08-20

标准版本：STANDARD-1.1-candidate

## 桌面账（设计条件）

### ✅ 原则注册库自检

    116 原则 / 20 节点 / 0 错误

### ✅ 存放契约与重要路径

    storage layout: PASSED (K1/J7)

### ✅ 原则体系映射

    原则体系映射校验通过：主归属 46/46；六域机制节点完整；注册库一致

### ✅ 操作治理引用图

    操作治理校验通过：89条MM / 16个阶段skill / 唯一规程active

### ✅ 课程血缘（必修上册/沁园春长沙）

    G0通过；G1待所有者审核；下游为空（诚实停止）

### ✅ 课程血缘（选择性必修下册/氓）

    发现S2人读教案草案但G0未建立；不得进入G1及下游（无下游，诚实停止）

### ✅ 课程数据底线检查（跳过）

    未发现现行lesson.json；教案候选不得用历史数据替代

### ✅ 全量测试（pytest）

    ................................................................................................................................ [ 90%]
    ..........................................                     [100%]
    446 passed, 12 skipped, 26 subtests passed in 78.58s (0:01:18)

### ✅ node 测试

    [PASS] test_lib_theme_sync.js: LIB_THEME_SINGLE_SOURCE_OK colors=22 module=8

### ✅ 知识账本校验

    {"result": "passed", "run_id": "VAL-20260820-225821+0800", "errors": 0, "report": "/home/ubuntu/homes/LuoChongjing/Methods/yuwen/work/knowledge/_meta/validation_reports/latest.json"}

### ✅ 机制节点覆盖

    - 知识学习: 原则映射 10，机器 5，追溯 3，审查 5
    - 能够学懂: 原则映射 101，机器 39，追溯 38，审查 54
    - 享受学习: 原则映射 49，机器 16，追溯 15，审查 37
    - 仅追溯强制缺口：无（active 原则均有 machine/review 强制或为 meta）

## 课堂账（效果证据）

- 状态：**空——当前L4无记录**（两本账纪律，P-12）。全部桌面通过仅证明设计条件具备。
- 待采集信号见 `scripts/checks/run_principle_checks.py` 报告的 classroom_account。
