---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "REMAINING-LANGUAGE-2009-2015"
status: "candidate_only"
mapping_status: "M0_only"
---

# 剩余语言表达与文言断句小问级知识点候选批次（2013—2015）

> 本批次补齐 2013—2015 的 3 个文言断句节点和 3 个信息概括/应用表达节点。解析中可能含示例答案，但不自动转录；所有记录保持 `M0 / kp_id=N/A`。

| 题型 | 年份 | 节点 | 分值 | 上游状态 | 候选作答动作 | 审核门 |
|---|---:|---|---:|---|---|---|
| `sentence_segmentation` | 2013 | `GK-SC-2013-Q012-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q012.md|题干]] | 4 | `candidate_source_without_answer_text_authority_missing` | 依据文言句意、虚词/句式和语气标志划分分句 | `source_authority_missing` |
| `sentence_segmentation` | 2014 | `GK-SC-2014-Q012-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/segments/question/Q012.md|题干]] | 4 | `remaining_language_candidate_source` | 依据文言句意、虚词/句式和语气标志划分分句 | `remaining_language_answer_and_scoring_review_required` |
| `sentence_segmentation` | 2015 | `GK-SC-2015-Q012-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/segments/question/Q012.md|题干]] | 4 | `remaining_language_candidate_source` | 依据文言句意、虚词/句式和语气标志划分分句 | `remaining_language_answer_and_scoring_review_required` |
| `summary_or_application` | 2013 | `GK-SC-2013-Q019-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/segments/question/Q019.md|题干]] | 4 | `candidate_source_without_answer_text_authority_missing` | 围绕交往目的设计递进、简明、得体的访谈问题 | `source_authority_missing` |
| `summary_or_application` | 2014 | `GK-SC-2014-Q019-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/segments/question/Q019.md|题干]] | 4 | `remaining_language_candidate_source` | 从图表筛选特征并写成准确、简明、连贯的说明 | `remaining_language_answer_and_scoring_review_required` |
| `summary_or_application` | 2015 | `GK-SC-2015-Q019-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/segments/question/Q019.md|题干]] | 4 | `remaining_language_candidate_source` | 紧扣宣传目的并运用比喻拟写简洁、有号召力的宣传语 | `remaining_language_answer_and_scoring_review_required` |

## 统计

- 总节点：6；2013 年权威缺失门禁：2；其余解析候选：4。
- `answer_candidate` 全部保持空值；`analysis_contains_answer_marker=true` 只表示解析中出现答案段，不表示答案已核验。

## 复核规则

1. 文言断句逐页核对原文、断线范围、断句数和句意；信息概括/应用题逐页核对材料、图表、字数、修辞和表达要求。
2. 将答案示例、解析思路与评分点分栏登记；没有独立官方答案/评分材料时保持未核验。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/高考分析/kp_batches/remaining_language_2009_2015.jsonl` |
| 本报告 | `work/knowledge/高考分析/kp_batches/remaining_language_2009_2015.md` |
| 生成脚本 | `scripts/extract_remaining_language_kp_batch.py` |
