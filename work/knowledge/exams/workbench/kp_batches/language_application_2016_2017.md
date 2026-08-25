---
schema_version: "exam-kp-candidate-batch-0.1"
batch_id: "LANGUAGE-APPLICATION-2016-2017"
status: "candidate_only"
mapping_status: "M0_only"
---

# 语言文字运用稳定小问候选批次（2016—2017）

> 本批次覆盖两套新课标Ⅲ卷中独立稳定的 Q7—Q11，共 10 条节点。选择题答案、补写和开放表达均不自动转录；2017 Q9/Q11 的 OCR 疑点随源记录保留。

| 年份 | 节点 | 子类型 | 分值 | 作答形式 | 候选动作 | 审核门 |
|---:|---|---|---:|---|---|---|
| 2016 | `GK-NC3-2016-Q007-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q007.md|题干]] | `idiom_usage` | 3 | `selected_response` | 结合语境辨析成语意义、感情色彩和使用对象 | `language_application_answer_and_scoring_review_required` |
| 2016 | `GK-NC3-2016-Q008-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q008.md|题干]] | `sentence_error` | 3 | `selected_response` | 识别句子成分、搭配和逻辑关系并判断病句 | `language_application_answer_and_scoring_review_required` |
| 2016 | `GK-NC3-2016-Q009-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q009.md|题干]] | `discourse_connective_selection` | 3 | `selected_response` | 依据语意衔接和逻辑关系选择恰当词语 | `language_application_answer_and_scoring_review_required` |
| 2016 | `GK-NC3-2016-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q010.md|题干]] | `completion` | 5 | `language_expression_free_response` | 依据语段结构、语意和逻辑补写连贯语句 | `language_application_answer_and_scoring_review_required` |
| 2016 | `GK-NC3-2016-Q011-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/segments/question/Q011.md|题干]] | `constructed_language_response` | 6 | `language_expression_free_response` | 把图示/推断要求转化为准确、简明、连贯的表达 | `language_application_answer_and_scoring_review_required` |
| 2017 | `GK-NC3-2017-Q007-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2017/segments/question/Q007.md|题干]] | `idiom_usage` | 3 | `selected_response` | 结合语境辨析成语意义、感情色彩和使用对象 | `language_application_answer_and_scoring_review_required` |
| 2017 | `GK-NC3-2017-Q008-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2017/segments/question/Q008.md|题干]] | `sentence_error` | 3 | `selected_response` | 识别句子成分、搭配和逻辑关系并判断病句 | `language_application_answer_and_scoring_review_required` |
| 2017 | `GK-NC3-2017-Q009-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2017/segments/question/Q009.md|题干]] | `discourse_connective_selection` | 3 | `selected_response` | 依据语意衔接和逻辑关系选择恰当词语 | `language_application_answer_and_scoring_review_required` |
| 2017 | `GK-NC3-2017-Q010-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2017/segments/question/Q010.md|题干]] | `completion` | 6 | `language_expression_free_response` | 依据语段结构、语意和逻辑补写连贯语句 | `language_application_answer_and_scoring_review_required` |
| 2017 | `GK-NC3-2017-Q011-TOP` [[Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2017/segments/question/Q011.md|题干]] | `constructed_language_response` | 5 | `language_expression_free_response` | 把图示/推断要求转化为准确、简明、连贯的表达 | `language_application_answer_and_scoring_review_required` |

## 统计

- 总节点：10；子类型分布：completion=2、constructed_language_response=2、discourse_connective_selection=2、idiom_usage=2、sentence_error=2。
- `answer_candidate` 全部为空；解析中出现“答案”仅表示本地解析候选存在，不表示官方答案或评分标准已核验。

## 复核规则

1. 选择题须回看空白卷选项、独立答案来源和评分口径；自由作答须另行登记答案示例与评分点。
2. 2017 Q9/Q11 的 OCR/水印疑点不能静默修订，需先完成 PDF 视觉复核。
3. 只有题文—答案/评分—教材 KP 三方证据闭合后，才允许升级映射等级。

| 产物 | 路径 |
|---|---|
| JSONL | `work/knowledge/exams/workbench/kp_batches/language_application_2016_2017.jsonl` |
| 本报告 | `work/knowledge/exams/workbench/kp_batches/language_application_2016_2017.md` |
| 生成脚本 | `scripts/extract_language_application_2016_2017_kp_batch.py` |
