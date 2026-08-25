---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "CLASSICAL-TRANSLATION-2021-2024"
status: "candidate_only"
mapping_status: "M0_only"
---

# 文言文翻译小问级知识点候选批次（2021—2024）

> 本批次覆盖 2021—2024 全国甲卷 Q13。2021—2023 为题目级节点（每题含两句），2024 已有两个小问节点；共享解析段仅作为证据来源，不自动生成官方译文或评分点。所有记录保持 `M0 / kp_id=N/A`。

| 年份 | 节点 | 分值 | 解析状态 | 候选考点 | 审核门 |
|---:|---|---:|---|---|---|
| 2021 | `GK-NCA-2021-Q013-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2021/segments/question/Q013.md|题干]] | 10 | `free_response_candidate_source` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2022 | `GK-NCA-2022-Q013-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2022/segments/question/Q013.md|题干]] | 10 | `free_response_candidate_source` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2023 | `GK-NCA-2023-Q013-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/segments/question/Q013.md|题干]] | 9 | `free_response_candidate_source` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2024 | `GK-NCA-2024-Q013-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q013.md|题干]] | 5 | `free_response_candidate_source` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |
| 2024 | `GK-NCA-2024-Q013-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q013.md|题干]] | 5 | `free_response_candidate_source` | 文言文句子翻译 | `free_response_answer_and_scoring_review_required` |

## 统计

- 总节点：5；解析候选源：5；缺少解析源：0。
- `answer_candidate` 全部保持空值；解析中出现“答案”字样不表示答案或评分点已核验。

## 复核规则

1. 逐页核对题干、横线句、分值和 OCR/水印疑点；2021—2023 的两句不能臆拆分值。
2. 独立登记译文候选、关键词采分点、句式处理和评分标准；不得把解析示例直接当官方评分。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/exams/workbench/kp_batches/classical_translation_2021_2024.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/classical_translation_2021_2024.md` |
| 生成脚本 | `scripts/extract_classical_translation_2021_2024_kp_batch.py` |
