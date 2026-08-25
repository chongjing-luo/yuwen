# 全局自检报告 2026-08-24

标准版本：STANDARD-1.3-candidate

## 桌面账（设计条件）

### ✅ 原则注册库自检

    117 原则 / 20 节点 / 0 错误

### ✅ 存放契约与重要路径

    storage layout: PASSED (storage contract)

### ✅ 原则体系映射

    原则体系映射校验通过：主归属 47/47；六域机制节点完整；注册库一致

### ✅ 操作治理引用图

    操作治理校验通过：94条MM / 16个阶段skill / 1个支持skill / 唯一规程active

### ✅ 课程血缘（必修上册/沁园春长沙）

    G0/G1通过；G2候选schema通过，尚待独立审查与design lock（诚实停止）

### ✅ 课程血缘（选择性必修下册/氓）

    发现S2人读教案草案但G0未建立；不得进入G1及下游（无下游，诚实停止）

### ✅ 课程血缘（选择性必修中册/记念刘和珍君）

    G0/G1通过；G2候选schema通过，尚待独立审查与design lock（诚实停止）

### ✅ 课程数据底线检查（必修上册-沁园春长沙）

    [PASS] frontstage_banned
    [PASS] timebox_conservation
    [PASS] guiding_questions_well_formed
    [PASS] total_minutes
    [PASS] boilerplate_trace
    报告已写入 /home/ubuntu/homes/LuoChongjing/Methods/yuwen/work/evaluation/reports/principle_checks_必修上册-沁园春长沙.json
    课堂账：空——未真实试教（两本账纪律，P-12）

### ✅ 课程数据底线检查（选择性必修中册-记念刘和珍君）

    [PASS] frontstage_banned
    [PASS] timebox_conservation
    [PASS] guiding_questions_well_formed（1）
    [PASS] total_minutes
    [PASS] boilerplate_trace
    报告已写入 /home/ubuntu/homes/LuoChongjing/Methods/yuwen/work/evaluation/reports/principle_checks_选择性必修中册-记念刘和珍君.json
    课堂账：空——未真实试教（两本账纪律，P-12）

### ✅ 全量测试（pytest）

    ........................................................ [ 90%]
    ....................................................           [100%]
    528 passed, 12 skipped, 26 subtests passed in 108.99s (0:01:48)

### ✅ node 测试

    [PASS] test_lib_theme_sync.js: LIB_THEME_SINGLE_SOURCE_OK colors=22 module=8

### ✅ 知识账本校验

    {"result": "passed", "run_id": "VAL-20260824-232311+0800", "errors": 0, "report": "/home/ubuntu/homes/LuoChongjing/Methods/yuwen/work/knowledge/_meta/validation_reports/latest.json"}

### ✅ 备课方法节点覆盖（candidate框架）

    - 知识学习: 原则映射 15，机器 9，追溯 4，审查 10
    - 能够学懂: 原则映射 107，机器 44，追溯 39，审查 60
    - 享受学习: 原则映射 52，机器 19，追溯 15，审查 41
    - 仅追溯强制缺口：无（active 原则均有 machine/review 强制或为 meta）

## 课堂账（效果证据）

- 状态：**空——当前L4无记录**（两本账纪律，P-12）。全部桌面通过仅证明设计条件具备。
- 待采集信号见 `scripts/checks/run_principle_checks.py` 报告的 classroom_account。
