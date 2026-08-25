---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "TOPIC-WRITING-2009-2015"
status: "candidate_only"
mapping_status: "M0_only"
---

# 材料/命题作文小问级知识点候选批次（2009—2015）

> 作文属于长篇自由作答。本批次只登记题干任务、来源和候选写作动作，不生成范文、立意答案或评分结论；所有记录保持 `M0 / kp_id=N/A`。

| 年份 | 节点 | 分值 | 解析状态 | 候选作答动作 | 审核门 |
|---:|---|---:|---|---|---|
| 2009 | `GK-SC-2009-Q021-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/segments/question/Q021.md|题干]] | 60 | `writing_candidate_source` | 围绕题目审题立意、构思并完成规范写作 | `writing_answer_and_scoring_review_required` |
| 2010 | `GK-SC-2010-Q021-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/segments/question/Q021.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2011 | `GK-SC-2011-Q021-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2011/segments/question/Q021.md|题干]] | 60 | `writing_candidate_source` | 围绕题目审题立意、构思并完成规范写作 | `writing_answer_and_scoring_review_required` |
| 2012 | `GK-SC-2012-Q021-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q021.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2013 | `GK-SC-2013-Q021-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q021.md|题干]] | 60 | `candidate_source_without_answer_text_authority_missing` | 理解材料寓意，选择角度立意并组织文章 | `source_authority_missing` |
| 2014 | `GK-SC-2014-Q021-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/segments/question/Q021.md|题干]] | 60 | `writing_candidate_source` | 审题立意、组织结构并完成书面表达 | `writing_answer_and_scoring_review_required` |
| 2015 | `GK-SC-2015-Q021-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/segments/question/Q021.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |

## 统计

- 总节点：7；作文解析候选源：6；2013 年权威缺失：1。
- `analysis_scope=top_level_exam_segment_with_possible_unrelated_context` 表示作文解析段可能混入同卷其他解析；不将其内容直接归为作文评分。
- `answer_candidate` 全部保持空值，解析中出现“答案”字样不表示答案已核验。

## 复核规则

1. 逐页核对材料、题目、写作要求、字数、文体和分值。
2. 独立登记材料寓意、可接受立意范围、评分等级和样文来源；不得把网络解析意见当官方评分。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/exams/workbench/kp_batches/topic_writing_2009_2015.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/topic_writing_2009_2015.md` |
| 生成脚本 | `scripts/extract_topic_writing_kp_batch.py` |
