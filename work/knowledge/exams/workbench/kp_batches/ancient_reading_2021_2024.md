---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "ANCIENT-READING-2021-2024"
status: "candidate_only"
mapping_status: "M0_only"
---

# 文言文基础阅读小问级知识点候选批次（2021—2024）

> 本批次覆盖断句、文言词语/文化常识和内容理解；文言翻译另列批次。答案不自动抽取，所有记录保持 `M0 / kp_id=N/A`。

| 年份 | 节点 | 分值 | 解析状态 | 候选作答动作 | 审核门 |
|---:|---|---:|---|---|---|
| 2021 | `GK-NCA-2021-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2021/segments/question/Q010.md|题干]] | 3 | `objective_candidate_source` | 依据语法结构、语意和虚词判断文言断句 | `objective_answer_and_evidence_review_required` |
| 2021 | `GK-NCA-2021-Q011-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2021/segments/question/Q011.md|题干]] | 3 | `objective_candidate_source` | 结合语境辨析文言词义与古代文化常识 | `objective_answer_and_evidence_review_required` |
| 2021 | `GK-NCA-2021-Q012-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2021/segments/question/Q012.md|题干]] | 3 | `objective_candidate_source` | 筛选原文信息并概括、判断内容理解 | `objective_answer_and_evidence_review_required` |
| 2022 | `GK-NCA-2022-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2022/segments/question/Q010.md|题干]] | 3 | `objective_candidate_source` | 依据语法结构、语意和虚词判断文言断句 | `objective_answer_and_evidence_review_required` |
| 2022 | `GK-NCA-2022-Q011-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2022/segments/question/Q011.md|题干]] | 3 | `objective_candidate_source` | 结合语境辨析文言词义与古代文化常识 | `objective_answer_and_evidence_review_required` |
| 2022 | `GK-NCA-2022-Q012-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2022/segments/question/Q012.md|题干]] | 3 | `objective_candidate_source` | 筛选原文信息并概括、判断内容理解 | `objective_answer_and_evidence_review_required` |
| 2023 | `GK-NCA-2023-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/segments/question/Q010.md|题干]] | 3 | `objective_candidate_source` | 依据语法结构、语意和虚词判断文言断句 | `objective_answer_and_evidence_review_required` |
| 2023 | `GK-NCA-2023-Q011-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/segments/question/Q011.md|题干]] | 3 | `objective_candidate_source` | 结合语境辨析文言词义与古代文化常识 | `objective_answer_and_evidence_review_required` |
| 2023 | `GK-NCA-2023-Q012-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/segments/question/Q012.md|题干]] | 4 | `objective_candidate_source` | 筛选原文信息并概括、判断内容理解 | `objective_answer_and_evidence_review_required` |
| 2024 | `GK-NCA-2024-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q010.md|题干]] | 3 | `objective_candidate_source` | 依据语法结构、语意和虚词判断文言断句 | `objective_answer_and_evidence_review_required` |
| 2024 | `GK-NCA-2024-Q011-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q011.md|题干]] | 3 | `objective_candidate_source` | 结合语境辨析文言词义与古代文化常识 | `objective_answer_and_evidence_review_required` |
| 2024 | `GK-NCA-2024-Q012-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/segments/question/Q012.md|题干]] | 3 | `objective_candidate_source` | 筛选原文信息并概括、判断内容理解 | `objective_answer_and_evidence_review_required` |

## 复核规则

1. 逐页核对断句标号、词语/文化常识选项、内容选项、分值和 OCR/水印疑点。
2. 将原文证据、正确选项和错因分栏登记；不能把解析结论直接当官方答案。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/exams/workbench/kp_batches/ancient_reading_2021_2024.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/ancient_reading_2021_2024.md` |
| 生成脚本 | `scripts/extract_ancient_reading_2021_2024_kp_batch.py` |
