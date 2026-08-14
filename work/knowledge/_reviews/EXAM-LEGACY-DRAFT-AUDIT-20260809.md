# 旧 `drafted` 交付条目审计

- 审计日期：2026-08-09
- 审计范围：`work/knowledge/_meta/deliverables.jsonl` 中状态为 `drafted` 的 6 条记录
- 审计目的：确认这些记录是否属于当前 2008—2024 四川高考阶段，避免误删或误消费旧批次
- 结论：6 条均为历史候选吞吐遗留项；不升格为正式交付，不删除，不并入当前 `SG-EXAM-CAL-2008-2024` 结构冻结。

## 逐条核查

| deliverable_id | 文件存在 | 当前来源/依赖 | 当前 manifest 关系 | 处置 |
|---|---:|---|---|---|
| `EXAM-2023-NCA` | 是 | `source_ids=[]`；文件自述为 S3 转载候选，缺少可核验题卷正文锚点 | 2023 全国甲卷在 2008—2024 语料中存在题卷/解析 PDF，但尚未形成正式 exam contract、官方答案/评分闭环 | 保留 `drafted`，标为 legacy candidate，禁止评审、映射和下游消费 |
| `EXAM-2024-NCA` | 是 | `source_ids=[]`；文件自述为 S3 转载候选，缺少可核验题卷正文锚点 | 2024 全国甲卷在语料中存在题卷/解析 PDF，但尚未完成正式来源核验和评分闭环 | 保留 `drafted`，标为 legacy candidate，禁止评审、映射和下游消费 |
| `EXAM-2025-NC2` | 是 | `source_ids=[]`；来自旧的 2025 入口 | 不在当前 2008—2024 正式语料 manifest；不得进入本批分母 | 保留 `drafted`，冻结在旧批次边界外 |
| `EXAM-2026-NC2` | 是 | `source_ids=[]`；`source_status=missing` | 不在当前 2008—2024 正式语料 manifest，且当前日期下无已登记可核验材料 | 保留 `drafted`，标记为缺失来源占位 |
| `MAP-EXAM-KP` | 是 | 依赖上述 4 个旧 exam 条目及教材卡；自身 `source_ids=[]` | 当前正式映射仍为 `M0 / kp_id=N/A`，且 `SG-EXAM` 尚未放行 | 保留 `drafted`，禁止生成 M1/M2/M3 或频次结论 |
| `GLOBAL-YUWEN` | 是 | 依赖 `MAP-EXAM-KP` 与 5 册教材交付 | 教材锁定已完成，但全局图谱依赖的真题映射尚未闭合 | 保留 `drafted`，不得宣称全局 accepted |

## 证据与边界

1. 当前正式试卷语料以 `Data/2008-2024·（四川）语文高考真题/manifest.json` 为准，覆盖 2008—2024 共 34 条题卷/解析记录。
2. `Data/reference/gaokao/manifest.json` 是来源恢复入口，包含部分转载或网页渲染材料；`source_level=S3`、`authenticity_status=unverified` 的记录不能单独闭合官方答案或评分权威性。
3. 2025 在来源恢复入口中存在，但不属于当前四川 2008—2024 语料分母；2026 没有登记记录。
4. 在 `SG-EXAM-CAL`、`SG-EXAM` 和教材—真题双向证据闭合前，任何高考交付继续保持 provisional；教材卡中已有 `M0 / kp_id=N/A` 不因这些旧条目改变。

## 后续动作

- 不修改这 6 条 ledger 状态，避免把历史批次静默改写为当前状态。
- 若未来扩大年份范围，先新建独立 exam contract、manifest、rubric 和 cutover batch，再重新领取对应条目。
- 若协调者批准清理旧遗留项，采用显式 `superseded` 状态迁移（含原因、操作者和日期），不直接删除文件或 ledger 行。

