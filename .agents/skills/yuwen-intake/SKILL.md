---
name: yuwen-intake
description: 高中语文资料采集入册（资料轴）。当外部资料（教材/试卷/教辅/课标/新闻/文献/书刊/他人PPT）需要进入系统、或需要裁决保留原始与否时使用。
---

# 采集入册（资料轴 · S0）

执行资料轴的来源、去留、存根和入册契约。规则：本手册 S0 册 MM-S0-01..04（P0）。入册资料可为后续备课目标服务，但不以绑定 K/U/J 节点作为资料合法性前提。

## 输入

- 外部资料文件（任意格式）+ 来源描述（网址/书名页/赠送人）

## 步骤（每步引用手册条目，不重述规则）

1. 落件：原样存入 `Tmp/inbox/`，并在 `Tmp/inbox/LEDGER.jsonl` 追加一行台账【MM-S0-01】。
2. 裁决四问：权威等级？可再生？转换含判断？版权敏感？→ 得出 keep_raw / process_only / discard，回写台账 verdict【MM-S0-02】。
3. 分流：keep_raw → 按 MM-S0-09 命名入 L0（`Data/` 对应区）+ 登记；process_only → 交 `yuwen-organize`，**留来源存根**【MM-S0-03】；discard → 台账记因后删除。
4. 登记：任何入库实体在 catalog 增行（或重跑 `scripts/build_catalog.py`）【MM-S0-04】。

## 门禁（放行条件）

- 台账无 pending 超过 3 日的件（驻留时限，Tmp/README）；
- 每个入库件能从台账行追到其 L0 路径或来源存根；
- 无存根的 process_only 产物被 MM-S0-03 判不合格。

## 产出

- 台账行（verdict 已决）+ L0 新原件（可选）+ catalog 增量
