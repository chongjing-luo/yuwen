---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "ANCIENT-CONTENT-2009-2015"
status: "candidate_only"
mapping_status: "M0_only"
---

# 文言文内容概括/信息筛选小问级知识点候选批次（2009—2015）

> 本批次只登记题型、题干任务与解析候选中的能力/考点线索。解析候选不等同官方答案或评分标准，所有记录保持 `M0 / kp_id=N/A`。

| 年份 | 节点 | 候选答案 | 状态 | 候选考点 | 能力层级 | 审核门 |
|---:|---|---|---|---|---|---|
| 2009 | `GK-SC-2009-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/segments/question/Q010.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 文言文信息筛选、归纳内容要点与概括 | `N/A` | `answer_source_extraction_required` |
| 2010 | `GK-SC-2010-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/segments/question/Q010.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 文言文信息筛选、归纳内容要点与概括 | `N/A` | `answer_source_extraction_required` |
| 2011 | `GK-SC-2011-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2011/segments/question/Q010.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 文言文信息筛选、归纳内容要点与概括 | `N/A` | `answer_source_extraction_required` |
| 2012 | `GK-SC-2012-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q010.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 文言文信息筛选、归纳内容要点与概括 | `N/A` | `answer_source_extraction_required` |
| 2013 | `GK-SC-2013-Q011-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q011.md|题干]] | `N/A` | `candidate_source_without_answer_text_authority_missing` | 文言文信息筛选、归纳内容要点与概括 | `N/A` | `source_authority_missing` |
| 2014 | `GK-SC-2014-Q011-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/segments/question/Q011.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 文言文信息筛选、归纳内容要点与概括 | `C` | `answer_source_extraction_required` |
| 2015 | `GK-SC-2015-Q011-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/segments/question/Q011.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 文言文信息筛选、归纳内容要点与概括 | `C` | `answer_source_extraction_required` |

## 统计

- 总节点：7；解析源存在但无显式答案标记：6；2013 年权威缺失门禁：1。
- 2013 年题型已由选择题转为主观概括题；本批次不把解析中的概括示例自动登记为评分答案。

## 复核规则

1. 逐页核对文言原文、设问边界、分值和 OCR/水印疑点。
2. 将答案示例、评分点与能力描述分栏登记；没有独立评分材料时保持未核验。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/高考分析/kp_batches/ancient_content_2009_2015.jsonl` |
| 本报告 | `work/knowledge/高考分析/kp_batches/ancient_content_2009_2015.md` |
| 生成脚本 | `scripts/extract_ancient_content_kp_batch.py` |
