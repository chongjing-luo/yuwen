---
document_type: development_log
phase: 开发阶段
version: 1
date: 2026-08-15
rule: "更新本文件时：旧版本整体移入 docs/devlog/archive/DEVLOG_<日期>_v<序号>.md（并在其头部标注各条目完成情况），本文件只保留最新内容；条目保持简要：方向 + 验收标准各一行"
---

# 开发日志（当前优化方向）

> 开发阶段的每轮工作从本文件开始。完成的方向在下次更新时移入归档并标注结果，此处只留最新清单。历史见 `docs/devlog/archive/`。

## 当前方向（按优先级）

1. **《氓》V6.6 样板清零** — 462 处追溯字段逐页改写为具体陈述；验收：`check_trace_evidence.py --strict` 0 发现。
2. **V6.6 迁移 lesson_schema v1.0** — 补 knowledge_refs / kp_scope / text_contract 源哈希；验收：`validate_lesson_schema.py` 通过。
3. **第二课文切片《沁园春·长沙》** — 走通 S2→S5 全链验证通用契约；验收：脱离《氓》构建器产出并通过审计，顺带抽取 theme.json 主题库。
4. **真实试教** — 课堂账唯一来源；验收：S6 观察表 + mastery ledger 出现首批真实数据。
5. **题-KP 映射 M0→M1/M2** — 从古诗鉴赏与默写批次起步；验收：首批小问级双向闭合并登记权威状态。
6. **教师手工改页轻量规范** — 补 PPT 手册登记待办；验收：一页级改动的保底操作卡（不破坏同源性）。
