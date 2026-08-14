---
schema_version: "exam-type-review-queue-0.1"
type: "metaphor_series"
mapping_status: "M0_only"
---

# 题型清洗队列：metaphor_series

> 候选原子考点：修辞辨析与表达效果。此描述只由题型和题干推断，不能替代小问级答案/评分复核，也不构成教材映射。

| 节点 | 年份 | 题段 | 清洗稿 | 原始来源 | 解析源 | 分值 | 答案源 | 审核门 |
|---|---:|---|---|---|---|---:|---|---|
| `GK-SC-2008-Q020-TOP` | 2008 | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/segments/question/Q020.md|题干]] | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/clean_md/question.md|清洗稿]] | [[Data/2008-2024·（四川）语文高考真题/mineru_result/2008年高考语文试卷（四川）（空白卷）/full.md|原始 MinerU]]<br>[[Data/2008-2024·（四川）语文高考真题/2008年高考语文试卷（四川）（空白卷）.pdf|原始 PDF]] | N/A | 5 | `candidate_unverified` | `candidate_ready_for_manual_kp_review` |

## 人工核验字段

- 先回看题段、清洗稿、原始 MinerU 与原始 PDF，确认小问边界和 OCR/水印疑点。
- 再回看解析候选；答案与评分点分开记录，不能把解析段落整体作为答案。
- 最后再检查教材 KP 的双向证据；没有闭合证据时保持 `M0 / kp_id=N/A`。
