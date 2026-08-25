---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "WORD-PRONUNCIATION-2008-2015"
status: "candidate_only"
mapping_status: "M0_only"
---

# 字音辨析小问级知识点候选批次（2008—2015）

> 本批次只把题型和解析中的考点描述整理成候选字段。`candidate_answer_present` 仍是本地解析候选，不是官方答案；没有显式答案标记的解析段不被补写。

| 年份 | 节点 | 候选答案 | 答案状态 | 候选考点 | 能力层级 | 审核门 |
|---:|---|---|---|---|---|---|
| 2008 | `GK-SC-2008-Q001-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/segments/question/Q001.md|题干]] | `N/A` | `missing_analysis_source` | 现代汉语普通话常用字字音识记与辨析 | `N/A` | `answer_source_missing` |
| 2009 | `GK-SC-2009-Q001-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2009/segments/question/Q001.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 现代汉语普通话常用字字音识记与辨析 | `N/A` | `answer_source_extraction_required` |
| 2010 | `GK-SC-2010-Q001-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/segments/question/Q001.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 现代汉语普通话常用字字音识记与辨析 | `N/A` | `answer_source_extraction_required` |
| 2011 | `GK-SC-2011-Q001-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2011/segments/question/Q001.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 现代汉语普通话常用字字音识记与辨析 | `N/A` | `answer_source_extraction_required` |
| 2012 | `GK-SC-2012-Q001-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2012/segments/question/Q001.md|题干]] | `N/A` | `candidate_source_without_answer_text` | 现代汉语普通话常用字字音识记与辨析 | `N/A` | `answer_source_extraction_required` |
| 2013 | `GK-SC-2013-Q001-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q001.md|题干]] | `B` | `candidate_text_present_authority_missing` | 现代汉语普通话常用字字音识记与辨析 | `N/A` | `source_authority_missing` |
| 2014 | `GK-SC-2014-Q001-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/segments/question/Q001.md|题干]] | `A` | `candidate_answer_present` | 现代汉语普通话常用字字音识记与辨析 | `识记` | `manual_answer_and_pdf_review` |
| 2015 | `GK-SC-2015-Q001-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/segments/question/Q001.md|题干]] | `D` | `candidate_answer_present` | 现代汉语普通话常用字字音识记与辨析 | `识记A` | `manual_answer_and_pdf_review` |

## 批次统计

- 总节点：8。
- 显式候选答案（未核验来源）：2；权限缺失但文本有答案：1；解析源存在但无答案标记：4；分析源缺失：1。
- 所有记录保持 `M0 / kp_id=N/A`；`knowledge_evidence_excerpt` 仅为候选证据摘录。

## 复核顺序

1. 先逐页回看题干 PDF，确认加点字、音标和 OCR 异文。
2. 再核对解析候选的答案字母与题干选项；没有独立来源时标为 `candidate_unverified`。
3. 将“多音字、形声字、习惯性误读”等子技能作为候选标签，不直接等同教材 KP。
4. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/exams/workbench/kp_batches/word_pronunciation_2008_2015.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/word_pronunciation_2008_2015.md` |
| 生成脚本 | `scripts/extract_word_pronunciation_kp_batch.py` |
