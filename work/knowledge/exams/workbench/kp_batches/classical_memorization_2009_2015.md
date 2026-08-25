---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "CLASSICAL-MEMORIZATION-2009-2015"
status: "candidate_only"
mapping_status: "M0_only"
---

# 名篇名句默写小问级知识点候选批次（2009—2015）

> 本批次只登记默写任务、来源和候选考点，不把解析中的填空答案自动确认为官方答案；所有记录保持 `M0 / kp_id=N/A`。

| 年份 | 节点 | 解析状态 | 源中有答案标记 | 能力层级候选 | 审核门 |
|---:|---|---|---|---|---|
| 2009 | `GK-SC-2009-Q013-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/segments/question/Q013.md|题干]] | `fill_in_candidate_source` | `false` | `N/A` | `fill_in_answer_and_scoring_review_required` |
| 2009 | `GK-SC-2009-Q013-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/segments/question/Q013.md|题干]] | `fill_in_candidate_source` | `false` | `N/A` | `fill_in_answer_and_scoring_review_required` |
| 2010 | `GK-SC-2010-Q013-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/segments/question/Q013.md|题干]] | `fill_in_candidate_source` | `false` | `N/A` | `fill_in_answer_and_scoring_review_required` |
| 2010 | `GK-SC-2010-Q013-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/segments/question/Q013.md|题干]] | `fill_in_candidate_source` | `false` | `N/A` | `fill_in_answer_and_scoring_review_required` |
| 2011 | `GK-SC-2011-Q013-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2011/segments/question/Q013.md|题干]] | `fill_in_candidate_source` | `false` | `N/A` | `fill_in_answer_and_scoring_review_required` |
| 2011 | `GK-SC-2011-Q013-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2011/segments/question/Q013.md|题干]] | `fill_in_candidate_source` | `false` | `N/A` | `fill_in_answer_and_scoring_review_required` |
| 2012 | `GK-SC-2012-Q013-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q013.md|题干]] | `fill_in_candidate_source` | `false` | `N/A` | `fill_in_answer_and_scoring_review_required` |
| 2012 | `GK-SC-2012-Q013-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q013.md|题干]] | `fill_in_candidate_source` | `false` | `N/A` | `fill_in_answer_and_scoring_review_required` |
| 2013 | `GK-SC-2013-Q014-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q014.md|题干]] | `candidate_source_without_answer_text_authority_missing` | `true` | `N/A` | `source_authority_missing` |
| 2014 | `GK-SC-2014-Q014-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/segments/question/Q014.md|题干]] | `fill_in_candidate_source` | `true` | `识记A` | `fill_in_answer_and_scoring_review_required` |
| 2015 | `GK-SC-2015-Q014-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/segments/question/Q014.md|题干]] | `fill_in_candidate_source` | `true` | `识记A` | `fill_in_answer_and_scoring_review_required` |

## 统计

- 总节点：11；默写解析源：10；2013 年权威缺失：1。
- `analysis_contains_answer_marker` 只表示源文本出现“答案”字样，不表示答案已核验；`answer_candidate` 全部保持空值。

## 复核规则

1. 逐页核对题干、篇目、上下句边界、限选数量、分值和 OCR/水印疑点。
2. 独立登记规范答案、易错字、通假字和评分规则；不得把解析示例直接当官方答案。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/exams/workbench/kp_batches/classical_memorization_2009_2015.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/classical_memorization_2009_2015.md` |
| 生成脚本 | `scripts/extract_classical_memorization_kp_batch.py` |
