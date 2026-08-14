---
schema_version: "exam-vertical-review-0.1"
exam_id: "GK-NCA-2021"
status: "structural_pass"
acceptance: "conditional_review"
mapping_status: "M0_only"
---

# GK-NCA-2021 垂直切片复核

- 作答节点：22；顶层题：22；分值复算：150/150。
- 题干来自空白卷；解析卷仅作为候选来源，未宣称官方答案或评分标准。
- 原始 PDF、MinerU full.md 未改写；清洗段与原卷保持双链。

## 节点概览

| 节点 | 分值 | 题型 | 答案源 | 状态 |
|---|---:|---|---|---|
| GK-NCA-2021-Q001-TOP | 3 | modern_reading_informational | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q002-TOP | 3 | modern_reading_informational | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q003-TOP | 3 | modern_reading_informational | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q004-TOP | 3 | practical_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q005-TOP | 4 | practical_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q006-TOP | 5 | practical_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q007-TOP | 3 | literary_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q008-TOP | 6 | literary_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q009-TOP | 6 | literary_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q010-TOP | 3 | ancient_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q011-TOP | 3 | ancient_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q012-TOP | 3 | ancient_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q013-TOP | 10 | classical_translation | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q014-TOP | 3 | poetry_appreciation | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q015-TOP | 6 | poetry_appreciation | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q016-TOP | 6 | classical_memorization | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q017-TOP | 9 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q018-TOP | 0 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q019-TOP | 0 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q020-TOP | 11 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q021-TOP | 0 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2021-Q022-TOP | 60 | topic_writing | candidate_unverified | response_nodes_derived |

## 视觉核对

- 2021 全国甲卷空白卷共11页；已逐页核对考试正文，PDF第10页为作文正文，第11页为广告页，不纳入题文。
- 卷面分区总分稳定为现代文36、古代诗文34、语言文字运用20、作文60，共150分。
- 实用类阅读Q4—Q6题组总分12，文学类阅读Q7—Q9题组总分15；采用3/4/5与3/6/6作为结构候选并显式标记，不宣称题面独立印刷分值。
- 语言文字运用分为Q17—Q19（9分）与Q20—Q21（11分）；仅保留组总分，Q18/Q19/Q21节点记0分占位，禁止把0解释为正式小题分值。
- 原始卷面可见水印；清洗稿仅去除下一节标题污染，原始PDF、MinerU full.md保持只读。

## 分值登记边界

- 本切片区分卷面组总分、候选分配和组首/占位登记；`score=0` 仅表示未分配占位，不表示该小题正式得0分。

| 分组 | 题号 | 卷面总分 | 登记方式 |
|---|---|---:|---|
| GK-NCA-2021-Q004-Q006 | Q4,Q5,Q6 | 12 | candidate_3_4_5 |
| GK-NCA-2021-Q007-Q009 | Q7,Q8,Q9 | 15 | candidate_3_6_6 |
| GK-NCA-2021-Q017-Q019 | Q17,Q18,Q19 | 9 | aggregate_only |
| GK-NCA-2021-Q020-Q021 | Q20,Q21 | 11 | aggregate_only |
