# 教材契约冻结记录

## 冻结标识

- Freeze ID: `TEXTBOOK-CONTRACT-2.0-textbook`
- Gate: `G2`
- Frozen at: 2026-08-07 14:35 +0800
- Coordinator: `coordinator`
- Scope: 教材知识卡、单元图谱、册级总表及其来源/证据/评审状态；高考试卷 Schema 不在本冻结范围内。

## G2 证据

- 原定校准包：10 张卡、5 份图谱。
- 额外完整性预门禁：CARD-B1-U06-03、CARD-B1-U06-04，用于解除 U06 图谱的 R03 完整性阻断。
- 评分记录：`work/knowledge/_reviews/scores/g2_reviews_20260807.jsonl`（34 条主审/第二复审记录）。
- 评分汇总：`work/knowledge/_reviews/scores/g2_review_summary_20260807.md`。
- 结果：原定 15 项交付物两位评审均 ≥92；补齐卡两位评审均 93.5；R01–R10=0；阻断性 P0/P1/P2=0。

## 冻结内容

| 契约 | 冻结版本 | 证据 |
|---|---|---|
| 知识卡/图谱/册表 Schema | `2.0-textbook`（文件实例保留 `2.0-candidate` 兼容标记，版本通过本记录锁定） | `_meta/schemas/*.json`、校准实例和 validator 通过 |
| taxonomy/状态机/受控词表 | `taxonomy.yaml` `contract_status=frozen` | 18 个任务群、状态迁移和 M0–M3 枚举均未改写 |
| 评分量表 | `rubrics.json` `2.0-textbook` 语义冻结 | G2 记录逐维度分数及最低门槛 |
| 证据与定位规则 | 规范 PDF 为直接引文终证；MinerU 仅定位 | 10 卡+5 图证据表、U03/U04课标补证 |
| 上游门禁 | 图谱只允许消费本单元 `accepted` 卡；册表只允许消费 accepted 图/诵读卡/前言 | `PROJECT_INDEX`、执行计划、图谱覆盖表 |

## 冻结后变更规则

1. 不得直接修改冻结枚举、字段含义、评分权重或状态迁移；任何变更创建 `2.1` 变更记录并重新跑 G2 影响评估。
2. 内容事实修订必须递增交付物版本并将下游置为 `review_required`；不能覆盖原 accepted 文件而不留哈希。
3. 高考试卷仍保持 `blocked_by_textbook`，直到 `TEXTBOOK-LOCK-2.0-textbook` 生成。
