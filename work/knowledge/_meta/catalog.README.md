# catalog.jsonl —— 实体总目录（设计方案 §3.8 目录层）

**唯一真相源**：资料轴每个实体一行。人读视图（INDEX.md、按考点/任务群索引）由脚本从本文件**生成**，永不手工编辑。

## 行 schema

```json
{"id":"CARD-X3-U01-01","type":"knowledge_card","title":"氓/离骚","path":"work/knowledge/选择性必修下册/cards/CARD-X3-U01-01_氓.md","status":"accepted","authority":"S1-derived","tags":["选必下","U01","诗经","叙事诗"],"updated":"2026-08-14","summary":"氓与离骚的知识卡：叙事链、比兴、香草美人","last_consumed":"2026-08-14"}
```

字段：id / type / title / path（按《ID 解析表》规则可解析）/ status（draft 条目不得被正式产物引用，门禁查）/ authority / tags（索引维度：册、单元、文体、任务群、题型、主题）/ updated / summary（一句话：这是什么、给谁什么情境用）/ last_consumed（防腐：零消费触发处置）。

## 状态

**占位**（2026-08-15）：本文件为空，待 catalog 最小版实装（设计方案 §10 路线⑥）时由脚本从 `_meta/deliverables.jsonl`、`assessment/item_bank.jsonl`、`materials/`、`work/teaching/` 等源生成首批行。消费登记粒度：**条目级**（§12 裁决 5）。
