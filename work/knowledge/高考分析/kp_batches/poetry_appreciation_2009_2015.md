---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "POETRY-APPRECIATION-2009-2015"
status: "candidate_only"
mapping_status: "M0_only"
---

# 古诗词鉴赏小问级知识点候选批次（2009—2015）

> 本批次覆盖炼字、形象、情感和表达技巧等自由作答小问。解析源常按顶层题目共享，因此仅登记题干任务和候选考点，不自动生成答案或评分点；所有记录保持 `M0 / kp_id=N/A`。

| 年份 | 节点 | 分值 | 解析状态 | 候选作答动作 | 审核门 |
|---:|---|---:|---|---|---|
| 2009 | `GK-SC-2009-Q012-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/segments/question/Q012.md|题干]] | 2 | `poetry_candidate_source` | 结合语境赏析炼字、句子或表达技巧 | `poetry_answer_and_scoring_review_required` |
| 2009 | `GK-SC-2009-Q012-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/segments/question/Q012.md|题干]] | 6 | `poetry_candidate_source` | 结合诗句概括诗歌形象特征 | `poetry_answer_and_scoring_review_required` |
| 2010 | `GK-SC-2010-Q012-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/segments/question/Q012.md|题干]] | 4 | `poetry_candidate_source` | 结合语境赏析炼字、句子或表达技巧 | `poetry_answer_and_scoring_review_required` |
| 2010 | `GK-SC-2010-Q012-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/segments/question/Q012.md|题干]] | 4 | `poetry_candidate_source` | 结合全诗分析形象、语言、技巧或情感 | `poetry_answer_and_scoring_review_required` |
| 2011 | `GK-SC-2011-Q012-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2011/segments/question/Q012.md|题干]] | 3 | `poetry_candidate_source` | 结合诗句概括诗歌形象特征 | `poetry_answer_and_scoring_review_required` |
| 2011 | `GK-SC-2011-Q012-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2011/segments/question/Q012.md|题干]] | 5 | `poetry_candidate_source` | 结合语境赏析炼字、句子或表达技巧 | `poetry_answer_and_scoring_review_required` |
| 2012 | `GK-SC-2012-Q012-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q012.md|题干]] | 3 | `poetry_candidate_source` | 结合语境赏析炼字、句子或表达技巧 | `poetry_answer_and_scoring_review_required` |
| 2012 | `GK-SC-2012-Q012-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q012.md|题干]] | 5 | `poetry_candidate_source` | 结合诗句/意象分析诗歌情感与作者态度 | `poetry_answer_and_scoring_review_required` |
| 2013 | `GK-SC-2013-Q013-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q013.md|题干]] | 4 | `candidate_source_without_answer_text_authority_missing` | 结合全诗分析形象、语言、技巧或情感 | `source_authority_missing` |
| 2013 | `GK-SC-2013-Q013-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q013.md|题干]] | 4 | `candidate_source_without_answer_text_authority_missing` | 结合语境赏析炼字、句子或表达技巧 | `source_authority_missing` |
| 2014 | `GK-SC-2014-Q013-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/segments/question/Q013.md|题干]] | 3 | `poetry_candidate_source` | 结合语境赏析炼字、句子或表达技巧 | `poetry_answer_and_scoring_review_required` |
| 2014 | `GK-SC-2014-Q013-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/segments/question/Q013.md|题干]] | 5 | `poetry_candidate_source` | 结合诗句/意象分析诗歌情感与作者态度 | `poetry_answer_and_scoring_review_required` |
| 2015 | `GK-SC-2015-Q013-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/segments/question/Q013.md|题干]] | 3 | `poetry_candidate_source` | 结合语境赏析炼字、句子或表达技巧 | `poetry_answer_and_scoring_review_required` |
| 2015 | `GK-SC-2015-Q013-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/segments/question/Q013.md|题干]] | 5 | `poetry_candidate_source` | 结合诗句/意象分析诗歌情感与作者态度 | `poetry_answer_and_scoring_review_required` |

## 统计

- 总节点：14；共享解析候选源：12；2013 年权威缺失：2。
- `analysis_scope=shared_top_level_analysis_segment` 表示同一解析段可能服务同题两小问；不能把段内任一结论直接归给单个小问。
- `answer_candidate` 全部保持空值；解析中出现“答案”字样也不表示答案已核验。

## 复核规则

1. 逐页核对诗文、设问、分值、材料边界和 OCR/水印疑点。
2. 按小问分别登记诗句证据、作答要点、评分点和解析来源；共享解析段不得跨小问复制结论。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/高考分析/kp_batches/poetry_appreciation_2009_2015.jsonl` |
| 本报告 | `work/knowledge/高考分析/kp_batches/poetry_appreciation_2009_2015.md` |
| 生成脚本 | `scripts/extract_poetry_appreciation_kp_batch.py` |
