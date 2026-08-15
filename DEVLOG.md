---
document_type: development_log
phase: 开发阶段
version: 2
date: "2026-08-15"
rule: "更新本文件时：旧版本整体移入 docs/devlog/archive/DEVLOG_<日期>_v<序号>.md（并在其头部标注各条目完成情况），本文件只保留最新内容；条目保持简要：方向 + 验收标准各一行"
---

# 开发日志（当前优化方向）

> 开发阶段的每轮工作从本文件开始。完成的方向在下次更新时移入归档并标注结果，此处只留最新清单。历史见 `docs/devlog/archive/`。路线总纲：`docs/architecture/项目设计方案.md` §10。

## 当前方向（按优先级）

1. **设计方案定稿** — Q7 有效期默认方案获确认后升 v1.0；验收：§12 七问全部闭环。
2. **V6.6 样板清零（进行中：462→403，O 模块已清）** — 逐页改写为具体陈述；验收：`check_trace_evidence --strict` 0 发现。
   2b. **lesson.json 迁移（已完成）** — canonical 数据源已迁至 work/teaching/…/lesson.json，lesson.js 变加载器，v65/v62 require 链解除。
   2c. **K2 锚定缺口（新登记）** — 21 处综合页 literary_object 为散文复合描述，需改为原句数组（schema 允许 string|array）；验收：validate_lesson_schema 0 错误。
3. **手册编译** — S3/S4/S5 三册从旧文档迁移成六字段格式，S1/S2/S6-S9 骨架充实；验收：条目带优先级/出处/预期信号。
4. **catalog 最小版实装** — 生成脚本 + INDEX/交叉视图 + 消费登记；验收：视图与账本一致、零消费体检可跑。
5. **证据轴落地** — OBS/GRD/MR/REF schema + 三条回流边工程化；验收：synthetic 数据走通 S6→S9→提案全链（明确标注测试数据）。
6. **随路线推进** — 第二课文切片、真实试教、题-KP M0→M1、新源类型预处理接入、L0 统一治理专项（见设计方案 §10）。
