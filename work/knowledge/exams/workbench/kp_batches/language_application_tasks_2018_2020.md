---
schema_version: "exam-kp-candidate-task-batch-0.1"
batch_id: "LANGUAGE-APPLICATION-TASKS-2018-2020"
status: "candidate_only"
mapping_status: "M0_only"
---

# 2018—2020 语言文字运用 Q8/Q9 任务候选批次

> 本批次将 2018—2020 Q8/Q9 按稳定任务边界派生为 14 个候选任务节点（每个题干/解析各有一个可逆文件）。父题原文不变；答案、评分和教材 KP 映射均不自动生成，全部保持 M0。

| 年份 | 节点 | 子类型 | 父题总分 | 任务分值 | 题干任务源 | 审核门 |
|---:|---|---|---:|---|---|---|
| 2018 | `GK-NC3-2018-Q008-1` | `pragmatic_register` | 4 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/subquestions/Q008-1.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2018 | `GK-NC3-2018-Q008-2` | `pragmatic_register` | 4 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/subquestions/Q008-2.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2018 | `GK-NC3-2018-Q008-3` | `pragmatic_register` | 4 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/subquestions/Q008-3.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2018 | `GK-NC3-2018-Q008-4` | `pragmatic_register` | 4 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/subquestions/Q008-4.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2018 | `GK-NC3-2018-Q008-5` | `pragmatic_register` | 4 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/subquestions/Q008-5.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2018 | `GK-NC3-2018-Q009-1` | `diagram_conversion` | 6 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/subquestions/Q009-1.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2019 | `GK-NC3-2019-Q008-1` | `completion` | 6 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/segments/question/subquestions/Q008-1.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2019 | `GK-NC3-2019-Q008-2` | `completion` | 6 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/segments/question/subquestions/Q008-2.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2019 | `GK-NC3-2019-Q008-3` | `completion` | 6 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/segments/question/subquestions/Q008-3.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2019 | `GK-NC3-2019-Q009-1` | `summary` | 5 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/segments/question/subquestions/Q009-1.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2020 | `GK-NC3-2020-Q008-1` | `completion` | 6 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/segments/question/subquestions/Q008-1.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2020 | `GK-NC3-2020-Q008-2` | `completion` | 6 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/segments/question/subquestions/Q008-2.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2020 | `GK-NC3-2020-Q008-3` | `completion` | 6 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/segments/question/subquestions/Q008-3.md|派生任务]] | `task_answer_and_scoring_review_required` |
| 2020 | `GK-NC3-2020-Q009-1` | `summary` | 5 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/segments/question/subquestions/Q009-1.md|派生任务]] | `task_answer_and_scoring_review_required` |

## 审核边界

1. 任务文件保留完整父题上下文，只增加边界声明；不能替代父题清洗源。
2. 2018 Q008 的五处修改、2019/2020 Q008 的三个空是候选任务单位，不把解析中的修订/补写文本写入答案字段。
3. Q009 是单一压缩或图文转换任务；图示、OCR 和水印疑点按源字段保留。
4. 只有题文—官方答案/评分—教材 KP 三方闭合后，才允许升级 M1 以上。

| 产物 | 路径 |
|---|---|
| 任务切分清单 | `work/knowledge/exams/workbench/kp_batches/language_application_tasks_split_2018_2020.json` |
| JSONL | `work/knowledge/exams/workbench/kp_batches/language_application_tasks_2018_2020.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/language_application_tasks_2018_2020.md` |
| 切分脚本 | `scripts/split_language_application_tasks_2018_2020.py` |
| 生成脚本 | `scripts/extract_language_application_tasks_2018_2020_kp_batch.py` |
| 验证报告 | `work/knowledge/_meta/language_application_tasks_2018_2020_kp_batch_validation_20260809.json` |
