---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "CLASSICAL-TRANSLATION-2009-2015"
status: "candidate_only"
mapping_status: "M0_only"
---

# 文言文翻译小问级知识点候选批次（2009—2015）

> 翻译属于自由作答题。本批次只登记题干、解析源和候选考点，不从混合解析文本自动生成翻译答案；答案与评分点须人工回看 PDF/独立评分材料。所有记录保持 `M0 / kp_id=N/A`。

| 年份 | 节点 | 解析状态 | 能力层级候选 | 候选考点 | 审核门 |
|---:|---|---|---|---|---|
| 2009 | `GK-SC-2009-Q011-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/segments/question/Q011.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2009 | `GK-SC-2009-Q011-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/segments/question/Q011.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2010 | `GK-SC-2010-Q011-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/segments/question/Q011.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2010 | `GK-SC-2010-Q011-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/segments/question/Q011.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2011 | `GK-SC-2011-Q011-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2011/segments/question/Q011.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2011 | `GK-SC-2011-Q011-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2011/segments/question/Q011.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2012 | `GK-SC-2012-Q011-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q011.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2012 | `GK-SC-2012-Q011-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q011.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2012 | `GK-SC-2012-Q011-3` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q011.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2013 | `GK-SC-2013-Q010-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q010.md|题干]] | `candidate_source_without_answer_text_authority_missing` | `N/A` | 文言文句子翻译 | `source_authority_missing` |
| 2013 | `GK-SC-2013-Q010-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q010.md|题干]] | `candidate_source_without_answer_text_authority_missing` | `N/A` | 文言文句子翻译 | `source_authority_missing` |
| 2014 | `GK-SC-2014-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/segments/question/Q010.md|题干]] | `free_response_candidate_source` | `理解B` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2015 | `GK-SC-2015-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/segments/question/Q010.md|题干]] | `free_response_candidate_source` | `N/A` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |

## 统计

- 总节点：13；自由作答解析源：11；2013 年权威缺失：2。
- 本批次没有自动生成 `answer_candidate`；即使解析段出现答案/译文，也只作为待人工核验的源文本。

## 复核规则

1. 逐页核对横线句、题号、分值和 OCR/水印疑点。
2. 独立登记译文候选、关键词采分点、句式处理和评分标准；不得把解析示例直接当官方评分。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/exams/workbench/kp_batches/classical_translation_2009_2015.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/classical_translation_2009_2015.md` |
| 生成脚本 | `scripts/extract_classical_translation_kp_batch.py` |
