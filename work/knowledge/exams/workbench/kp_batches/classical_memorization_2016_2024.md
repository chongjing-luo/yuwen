---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "CLASSICAL-MEMORIZATION-2016-2024"
status: "candidate_only"
mapping_status: "M0_only"
---

# 名篇名句默写小问级知识点候选批次（2016—2024）

> 本批次覆盖 2016—2024 名篇名句默写节点。2016、2024 的稳定分支保留为独立节点，其余年度按题目级节点登记；不把解析中的填空答案自动确认为官方答案，所有记录保持 `M0 / kp_id=N/A`。

| 年份 | 节点 | 分值 | 解析状态 | 源中有答案标记 | 审核门 |
|---:|---|---:|---|---|---|
| 2016 | `GK-NC3-2016-Q004-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q004.md|题干]] | 2 | `fill_in_candidate_source` | `false` | `fill_in_answer_and_scoring_review_required` |
| 2016 | `GK-NC3-2016-Q004-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q004.md|题干]] | 2 | `fill_in_candidate_source` | `false` | `fill_in_answer_and_scoring_review_required` |
| 2016 | `GK-NC3-2016-Q004-3` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q004.md|题干]] | 2 | `fill_in_candidate_source` | `false` | `fill_in_answer_and_scoring_review_required` |
| 2017 | `GK-NC3-2017-Q006-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2017/segments/question/Q006.md|题干]] | 5 | `fill_in_candidate_source` | `false` | `fill_in_answer_and_scoring_review_required` |
| 2018 | `GK-NC3-2018-Q006-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/Q006.md|题干]] | 6 | `fill_in_candidate_source` | `true` | `fill_in_answer_and_scoring_review_required` |
| 2019 | `GK-NC3-2019-Q006-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/segments/question/Q006.md|题干]] | 6 | `fill_in_candidate_source` | `true` | `fill_in_answer_and_scoring_review_required` |
| 2020 | `GK-NC3-2020-Q006-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/segments/question/Q006.md|题干]] | 6 | `fill_in_candidate_source` | `true` | `fill_in_answer_and_scoring_review_required` |
| 2021 | `GK-NCA-2021-Q016-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2021/segments/question/Q016.md|题干]] | 6 | `fill_in_candidate_source` | `true` | `fill_in_answer_and_scoring_review_required` |
| 2022 | `GK-NCA-2022-Q016-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2022/segments/question/Q016.md|题干]] | 6 | `fill_in_candidate_source` | `true` | `fill_in_answer_and_scoring_review_required` |
| 2023 | `GK-NCA-2023-Q016-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/segments/question/Q016.md|题干]] | 6 | `fill_in_candidate_source` | `true` | `fill_in_answer_and_scoring_review_required` |
| 2024 | `GK-NCA-2024-Q016-1` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q016.md|题干]] | 2 | `fill_in_candidate_source` | `true` | `fill_in_answer_and_scoring_review_required` |
| 2024 | `GK-NCA-2024-Q016-2` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q016.md|题干]] | 2 | `fill_in_candidate_source` | `true` | `fill_in_answer_and_scoring_review_required` |
| 2024 | `GK-NCA-2024-Q016-3` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q016.md|题干]] | 2 | `fill_in_candidate_source` | `true` | `fill_in_answer_and_scoring_review_required` |

## 统计

- 总节点：13；默写解析源：13；缺少解析源：0。
- `analysis_contains_answer_marker` 只表示源文本出现“答案”字样，不表示答案已核验；`answer_candidate` 全部保持空值。

## 复核规则

1. 逐页核对题干、篇目、上下句边界、限选数量、分值和 OCR/水印疑点。
2. 独立登记规范答案、易错字、通假字和评分规则；不得把解析示例直接当官方答案。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/exams/workbench/kp_batches/classical_memorization_2016_2024.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/classical_memorization_2016_2024.md` |
| 生成脚本 | `scripts/extract_classical_memorization_2016_2024_kp_batch.py` |
