---
name: yuwen-flow
description: 语文项目按环节跑门禁链（工程轴）。当需要只验证某一教学环节（S2-S9）的数据流门禁、或环节产物变更后做定向回归时使用。
---

# 环节门禁链（工程轴）

服务机制节点：全部节点的**门禁面**（设计方案 §6 九跳）。

## 输入

- 环节代号（S0-S9）+ 该环节涉及的实体路径

## 门禁链（按环节）

| 环节 | 跑什么 |
|---|---|
| S0 资料 | `build_catalog.py --check` + `validate_knowledge_base.py` |
| S2/S3 设计 | `validate_lesson_schema.py --lesson-json <lesson.json>`（--strict 为新候选要求） |
| S4 物料 | 构建器测试 + `checks/run_principle_checks.py --lesson-js …` |
| S5 审计 | `checks/check_trace_evidence.py` + 审查协议（人工双审） |
| S7 作业 | `validate_homework_package.py <package.json>` |
| S8 命题/诊断 | `validate_assessment_package.py <blueprint>` / `analyze_mastery.py --check`（如有台账） |
| 全局 | `scripts/run_selfcheck.py`（注册库+底线+全量测试+覆盖） |

## 步骤

1. 按表取该环节命令，逐条执行，收集退出码。
2. 失败项按失败归因表定位：操作漏引用（改 skill）/ 规则缺口（补手册，走中环）/ 工程问题（改工程轴）。
3. 通过后按 MM-S0-08 登记 consumed（更新 last_consumed）。

## 放行条件

- 该环节全部命令退出码 0；
- 涉及在审候选的，按收敛规则记录所用的 STANDARD 版本。

## 产出

- 门禁执行记录（退出码清单）+ catalog 消费增量
