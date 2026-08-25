---
name: yuwen-catalog
description: 高中语文资料目录维护（资料轴）。当需要重建实体总目录/索引视图、登记消费、跑零消费体检时使用。
---

# 目录维护（资料轴 · S0）

执行资料轴的可寻址、视图生成、消费登记与防腐契约。规则：MM-S0-07/08（P1）、MM-S0-04（P0）。目录可间接支持备课取材，但不属于备课目标节点本体。

## 输入

- 各真相源（账本/题库/teaching/manuals/materials 的增删改）

## 步骤

1. 重建：`python3 scripts/build_catalog.py` → catalog.jsonl + `work/knowledge/INDEX.md`【MM-S0-07：视图永不手工编辑】。
2. 校验：`python3 scripts/build_catalog.py --check` → 路径悬空=0；列出未消费清单。
3. 消费登记：任何操作读取实体为输入后，更新该行 last_consumed（条目级）【MM-S0-08】。
4. 处置：>90 天零消费实体 → 补消费方或降级归档，决定记录在案。

## 门禁（放行条件）

- --check 退出码 0（无悬空路径）；
- 视图重跑 diff 为空（除日期）；
- 新增实体已在 ID 解析表登记规则。

## 产出

- catalog.jsonl / INDEX.md（生成物）+ 体检报告行
