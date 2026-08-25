---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "LANGUAGE-GROUP-SUBQUESTION-2018-2020"
status: "candidate_only"
mapping_status: "M0_only"
---

# 2018—2020 语言文字运用组题小问候选批次

> 本批次把 2018—2020 Q7 组题拆成 9 个可逆小问文件。父题组总分保留，但小问分值不臆分；每条记录链接父题段、派生题干、派生解析、MinerU 和 PDF，答案全部不自动抽取。

| 年份 | 节点 | 子类型 | 父题总分 | 小问分值 | 题干源 | 审核门 |
|---:|---|---|---:|---|---|---|
| 2018 | `GK-NC3-2018-Q007-1` | `idiom_usage` | 20 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/subquestions/Q007-1.md|派生题干]] | `group_subquestion_answer_and_scoring_review_required` |
| 2018 | `GK-NC3-2018-Q007-2` | `sentence_error` | 20 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/subquestions/Q007-2.md|派生题干]] | `group_subquestion_answer_and_scoring_review_required` |
| 2018 | `GK-NC3-2018-Q007-3` | `completion` | 20 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/segments/question/subquestions/Q007-3.md|派生题干]] | `group_subquestion_answer_and_scoring_review_required` |
| 2019 | `GK-NC3-2019-Q007-1` | `lexical_usage` | 9 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/segments/question/subquestions/Q007-1.md|派生题干]] | `group_subquestion_answer_and_scoring_review_required` |
| 2019 | `GK-NC3-2019-Q007-2` | `sequence_selection` | 9 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/segments/question/subquestions/Q007-2.md|派生题干]] | `group_subquestion_answer_and_scoring_review_required` |
| 2019 | `GK-NC3-2019-Q007-3` | `sentence_error` | 9 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/segments/question/subquestions/Q007-3.md|派生题干]] | `group_subquestion_answer_and_scoring_review_required` |
| 2020 | `GK-NC3-2020-Q007-1` | `sequence_selection` | 9 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/segments/question/subquestions/Q007-1.md|派生题干]] | `group_subquestion_answer_and_scoring_review_required` |
| 2020 | `GK-NC3-2020-Q007-2` | `lexical_usage` | 9 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/segments/question/subquestions/Q007-2.md|派生题干]] | `group_subquestion_answer_and_scoring_review_required` |
| 2020 | `GK-NC3-2020-Q007-3` | `sentence_error` | 9 | `N/A` | [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/segments/question/subquestions/Q007-3.md|派生题干]] | `group_subquestion_answer_and_scoring_review_required` |

## 统计

- 总节点：9；年份分布：2018=3、2019=3、2020=3。
- 小问分值全部保持 `N/A`；父题组总分分别为 2018=20、2019=9、2020=9，仅作为上游总分提示。

## 复核规则

1. 先逐页核对父题组边界和小问编号，再独立登记小问分值；不能用父题总分平均分配。
2. 派生 Markdown 只用于定位和人工复核，不替代父题原始清洗源，也不承担独立官方页级定位。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| 小问切分清单 | `work/knowledge/exams/workbench/kp_batches/language_group_subquestion_split_2018_2020.json` |
| JSONL | `work/knowledge/exams/workbench/kp_batches/language_group_subquestion_2018_2020.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/language_group_subquestion_2018_2020.md` |
| 切分脚本 | `scripts/split_language_group_subquestions_2018_2020.py` |
| 生成脚本 | `scripts/extract_language_group_subquestion_2018_2020_kp_batch.py` |
