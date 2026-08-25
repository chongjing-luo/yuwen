---
schema_version: "exam-vertical-review-0.1"
exam_id: "GK-NCA-2023"
status: "structural_pass"
acceptance: "conditional_review"
mapping_status: "M0_only"
---

# GK-NCA-2023 垂直切片复核

- 作答节点：22；顶层题：22；分值复算：150/150。
- 题干来自空白卷；解析卷仅作为候选来源，未宣称官方答案或评分标准。
- 原始 PDF、MinerU full.md 未改写；清洗段与原卷保持双链。

## 节点概览

| 节点 | 分值 | 题型 | 答案源 | 状态 |
|---|---:|---|---|---|
| GK-NCA-2023-Q001-TOP | 3 | modern_reading_informational | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q002-TOP | 3 | modern_reading_informational | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q003-TOP | 3 | modern_reading_informational | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q004-TOP | 3 | practical_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q005-TOP | 4 | practical_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q006-TOP | 5 | practical_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q007-TOP | 3 | literary_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q008-TOP | 6 | literary_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q009-TOP | 6 | literary_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q010-TOP | 3 | ancient_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q011-TOP | 3 | ancient_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q012-TOP | 4 | ancient_reading | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q013-TOP | 9 | classical_translation | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q014-TOP | 3 | poetry_appreciation | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q015-TOP | 6 | poetry_appreciation | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q016-TOP | 6 | classical_memorization | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q017-TOP | 20 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q018-TOP | 0 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q019-TOP | 0 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q020-TOP | 0 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q021-TOP | 0 | language_application | candidate_unverified | response_nodes_derived |
| GK-NCA-2023-Q022-TOP | 60 | topic_writing | candidate_unverified | response_nodes_derived |

## 视觉核对

- 2023 全国甲卷空白卷共11页；考试正文为第1—8页，第9—10页为空白水印页，第11页为广告页。
- 卷面分区总分按150分复核为现代文36、古代诗文34、语言文字运用20、作文60；但题面同时印有文言文20分与诗歌9分，产生1分算术冲突。为不静默修订，文言文小问暂登记3/3/4/9候选并保留冲突警告。
- 实用类阅读Q4—Q6题组总分12，文学类阅读Q7—Q9题组总分15；采用3/4/5与3/6/6作为结构候选并显式标记。
- 语言文字运用Q17—Q21统一为20分题组；仅保留组总分，Q18—Q21节点记0分占位，禁止把0解释为正式小题分值。
- 原始水印、空白页和广告页不进入题文清洗正文；原始PDF、MinerU full.md保持只读。

## 分值登记边界

- 本切片区分卷面组总分、候选分配和组首/占位登记；`score=0` 仅表示未分配占位，不表示该小题正式得0分。

| 分组 | 题号 | 卷面总分 | 登记方式 |
|---|---|---:|---|
| GK-NCA-2023-Q004-Q006 | Q4,Q5,Q6 | 12 | candidate_3_4_5 |
| GK-NCA-2023-Q007-Q009 | Q7,Q8,Q9 | 15 | candidate_3_6_6 |
| GK-NCA-2023-Q010-Q013 | Q10,Q11,Q12,Q13 | 19 | candidate_3_3_4_9 |
| GK-NCA-2023-Q017-Q021 | Q17,Q18,Q19,Q20,Q21 | 20 | aggregate_only |
