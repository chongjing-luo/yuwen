---
schema_version: "exam-answer-scoring-audit-0.1"
status: "passed_with_gaps"
audit_id: "EXAM-ANSWER-SCORING-2008-2024-20260809"
scoring_status: "not_available_as_official"
---

# 2008—2024 高考语文答案/评分来源审计

> 本清单只审计派生答案索引，不修改原始 PDF、MinerU `full.md` 或清洗源。`candidate` 只表示本地解析文本可被检索，不表示官方答案；当前没有任何题目可以宣布具备官方评分标准。

## 总结

- 覆盖 17 年、310 个顶层题目。
- bundle/index 层：有 bundle/index 的年份 8，已索引题目 118；其中候选答案文本 74。
- 垂直切片层：359 个作答节点中 336 个有本地解析候选，23 个显式缺失。两层口径不同，不能互相替代。
- bundle/index 层缺失或空答案：236；官方核验：0。
- 独立第三方候选登记：9 个 Source；不计入 bundle/index 答案覆盖，也不改变官方核验/评分计数。
- 所有题目的 `scoring_status` 固定为 `not_available_as_official`，直到独立评分材料和复核回执闭合。

## 年度清单

| 年份/试卷 | 顶层题数 | bundle/index | bundle候选 | bundle缺失 | 垂直候选 | 垂直缺失 | 评分状态 |
|---|---:|---|---:|---:|---:|---:|---|
| GK-SC-2008 | 21 | 有 | 21 | 0 | 24 | 0 | `not_available_as_official` |
| GK-SC-2009 | 21 | 缺失 | 0 | 21 | 24 | 0 | `not_available_as_official` |
| GK-SC-2010 | 21 | 缺失 | 0 | 21 | 24 | 0 | `not_available_as_official` |
| GK-SC-2011 | 21 | 缺失 | 0 | 21 | 24 | 0 | `not_available_as_official` |
| GK-SC-2012 | 21 | 缺失 | 0 | 21 | 25 | 0 | `not_available_as_official` |
| GK-SC-2013 | 21 | 有 | 0 | 21 | 0 | 23 | `not_available_as_official` |
| GK-SC-2014 | 21 | 缺失 | 0 | 21 | 22 | 0 | `not_available_as_official` |
| GK-SC-2015 | 21 | 缺失 | 0 | 21 | 22 | 0 | `not_available_as_official` |
| GK-NC3-2016 | 12 | 有 | 11 | 1 | 27 | 0 | `not_available_as_official` |
| GK-NC3-2017 | 12 | 有 | 12 | 0 | 23 | 0 | `not_available_as_official` |
| GK-NC3-2018 | 10 | 有 | 10 | 0 | 10 | 0 | `not_available_as_official` |
| GK-NC3-2019 | 10 | 有 | 10 | 0 | 10 | 0 | `not_available_as_official` |
| GK-NC3-2020 | 10 | 有 | 10 | 0 | 10 | 0 | `not_available_as_official` |
| GK-NCA-2021 | 22 | 缺失 | 0 | 22 | 22 | 0 | `not_available_as_official` |
| GK-NCA-2022 | 22 | 缺失 | 0 | 22 | 22 | 0 | `not_available_as_official` |
| GK-NCA-2023 | 22 | 缺失 | 0 | 22 | 22 | 0 | `not_available_as_official` |
| GK-NCA-2024 | 22 | 有 | 0 | 22 | 25 | 0 | `not_available_as_official` |

## 状态解释

- `candidate_answer_only_or_short`：索引中有非空答案片段，但来源仍是 `unverified_local_provided`。
- `candidate_mixed_analysis`：答案字段混入题干、分析、解析或例文，不能直接当作干净答案/评分点。
- `missing_source`：没有答案索引，或索引明确缺失/答案为空。
- `conflict`：字段声称官方但没有独立权威来源回执；当前应退回人工核验。

## 放行门槛

1. 题干、答案、评分标准分离登记，分别有稳定定位。
2. 来源发布主体/原始 URL 或考试机构文件可核验，并保留 SHA-256。
3. 至少一次独立 PDF/页面复核；OCR 异文写入问题回执，不覆盖原文。
4. 在上述三项及教材 KP 双向证据完成前，知识点节点保持 `M0 / kp_id=N/A`。

## 下一批执行顺序

0. GK-SC-2013 已完成新浪图像候选与本地解析候选逐题交叉比对；Q3/Q10/Q11/Q13 保持混合解析边界，Q16—Q20 保持差异复核，Q21 仍缺失。
0.5. GK-NCA-2023 已登记中国教育在线 Q1—Q3、Q6—Q10 部分外部候选，并完成本地共享答案块切分与逐题比对；Q4/Q5/Q11—Q22 的外部缺失保持显式。
0.75. GK-SC-2015 已登记高考网转载/新东方教研组 DOC 的 Q1—Q20 答案或作答指导候选；Q21 仅作文审题指导，所有记录仍是第三方候选。
0.8. GK-SC-2014 已登记高考网/中学学科网带水印图 Q1—Q9 候选；Q10—Q18 的分页图失链，继续保持显式缺失。
0.85. GK-SC-2012 高考网 RAR/DOC 已核验为题卷文本而非答案材料，登记为 blocked_no_answer_content，不生成候选层。
0.9. GK-SC-2010 高考网 RAR/DOC 已登记 Q1、Q2、Q4、Q8、Q9 的明确答案标记候选；其余题号保持缺失，不由混合文本推断。
1. 对 2009—2012、2014—2015、2021—2023 其余已有垂直解析候选的节点，补建独立候选索引；找不到评分源时保留显式缺失，不用搜索摘要替代。
2. 对 2008、2016—2020 的候选文本做题号级清洗，保留原解析文本双链，并单独抽取 `answer_candidate`；不写入 `official_verified`。
3. 2024 解析卷本地候选层已建立；Q8/Q9 圈码 OCR、Q12 选项冲突、Q16 重复答案串与 OCR 残片继续留在独立复核队列，不提升为官方答案。
4. 只有答案/评分来源审计通过后，才进入教材 KP 三方证据闭合和 M1 以上映射。

| 产物 | 路径 |
|---|---|
| 机器审计 | `work/knowledge/_meta/exam_answer_scoring_audit_20260809.json` |
| 本报告 | `work/knowledge/高考分析/EXAM-ANSWER-SCORING-AUDIT-20260809.md` |
| 候选答案层 | `work/knowledge/高考分析/EXAM-ANSWER-CANDIDATE-EXTRACTION-20260809.md` |
| 题型清洗队列 | `work/knowledge/高考分析/EXAM-TYPE-KP-REVIEW-QUEUE-20260809.md` |
| 执行脚本 | `scripts/audit_exam_answer_scoring_sources.py` |
| 2013 候选交叉比对 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/reference_answer_candidate_comparison.jsonl` |
| 2013 比对报告 | `work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATE-COMPARISON-2013.md` |
| 2013 比对验证 | `scripts/validate_2013_candidate_comparison.py` |
| 2023 外部部分候选 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/reference_answer_candidates.jsonl` |
| 2023 本地共享答案切分 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/local_analysis_group_candidates.jsonl` |
| 2023 候选比对 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/reference_answer_candidate_comparison.jsonl` |
| 2023 候选验证 | `scripts/validate_2023_candidate_comparison.py` |
| 2015 外部候选 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2015/answers/reference_answer_candidates.jsonl` |
| 2015 候选验证 | `scripts/validate_2015_reference_answer_candidates.py` |
| 2014 外部部分候选 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2014/answers/reference_answer_candidates.jsonl` |
| 2014 候选验证 | `scripts/validate_2014_reference_answer_candidates.py` |
| 2010 外部部分候选 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2010/answers/reference_answer_candidates.jsonl` |
| 2010 候选验证 | `scripts/validate_2010_reference_answer_candidates.py` |
