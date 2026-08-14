---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "TOPIC-WRITING-2016-2024"
status: "candidate_only"
mapping_status: "M0_only"
---

# 材料/命题作文小问级知识点候选批次（2016—2024）

> 作文属于长篇自由作答。本批次只登记题干任务、来源和候选写作动作，不生成范文、立意答案或评分结论；所有记录保持 `M0 / kp_id=N/A`。

| 年份 | 节点 | 分值 | 解析状态 | 候选作答动作 | 审核门 |
|---:|---|---:|---|---|---|
| 2016 | `GK-NC3-2016-Q012-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q012.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2017 | `GK-NC3-2017-Q012-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2017/segments/question/Q012.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2018 | `GK-NC3-2018-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/Q010.md|题干]] | 50 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2019 | `GK-NC3-2019-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/segments/question/Q010.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2020 | `GK-NC3-2020-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/segments/question/Q010.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2021 | `GK-NCA-2021-Q022-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2021/segments/question/Q022.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2022 | `GK-NCA-2022-Q022-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2022/segments/question/Q022.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2023 | `GK-NCA-2023-Q022-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/segments/question/Q022.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |
| 2024 | `GK-NCA-2024-Q022-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q022.md|题干]] | 60 | `writing_candidate_source` | 理解材料寓意，选择角度立意并组织文章 | `writing_answer_and_scoring_review_required` |

## 复核规则

1. 逐页核对材料、题目、写作要求、字数、文体和分值。
2. 独立登记材料寓意、可接受立意范围、评分等级和样文来源；不得把网络解析意见当官方评分。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/高考分析/kp_batches/topic_writing_2016_2024.jsonl` |
| 本报告 | `work/knowledge/高考分析/kp_batches/topic_writing_2016_2024.md` |
| 生成脚本 | `scripts/extract_topic_writing_2016_2024_kp_batch.py` |
