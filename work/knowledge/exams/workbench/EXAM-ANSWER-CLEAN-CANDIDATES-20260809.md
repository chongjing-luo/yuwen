---
schema_version: "answer-clean-candidate-0.1"
status: "candidate_only"
scoring_status: "not_available_as_official"
mapping_status: "M0 | kp_id=N/A"
---

# 2008—2024 答案/解析候选清洗派生层

> 该层只按源字段中明确出现的分析/解析/解答/答案标记切分题干、分析与候选答案。不能安全切分的行保留为 unbounded；不修改原答案索引，不生成评分标准，不宣称官方性。

- 覆盖索引行：118；明确分析边界且有答案标记：52；明确分析边界但无答案标记：0；派生答案边界（无分析标记）：1；其余保留未界定：65。
- 检出明确跨题复合源段：1 条；已记录分段偏移、题号和 SHA-256，未将缺失答案补入索引。
- 已登记两类派生边界回执：2020 Q002 的嵌套答案标记边界，以及 2008 全卷答案字段范围；两者均不改变原始答案索引或答案权威性。
- 全部记录固定 `scoring_status=not_available_as_official`、`mapping_level=M0`、`kp_id=N/A`。
- 每条记录保留原答案字段 SHA-256、标记清单、派生字段哈希和 `source_answer_index` 双链。

| 试卷 | 索引行数 | 显式分析+答案 | 显式分析无答案 | 派生答案边界 | 未界定/缺失 | 输出 |
|---|---:|---:|---:|---:|---:|---|
| GK-NC3-2016 | 12 | 11 | 0 | 0 | 1 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers/answer_clean_candidates.jsonl` |
| GK-NC3-2017 | 12 | 12 | 0 | 0 | 0 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2017/answers/answer_clean_candidates.jsonl` |
| GK-NC3-2018 | 10 | 10 | 0 | 0 | 0 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/answers/answer_clean_candidates.jsonl` |
| GK-NC3-2019 | 10 | 10 | 0 | 0 | 0 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/answers/answer_clean_candidates.jsonl` |
| GK-NC3-2020 | 10 | 9 | 0 | 1 | 0 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/answers/answer_clean_candidates.jsonl` |
| GK-NCA-2021 | 0 | 0 | 0 | 0 | 0 | `N/A` |
| GK-NCA-2022 | 0 | 0 | 0 | 0 | 0 | `N/A` |
| GK-NCA-2023 | 0 | 0 | 0 | 0 | 0 | `N/A` |
| GK-NCA-2024 | 22 | 0 | 0 | 0 | 22 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/answer_clean_candidates.jsonl` |
| GK-SC-2008 | 21 | 0 | 0 | 0 | 21 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/answers/answer_clean_candidates.jsonl` |
| GK-SC-2009 | 0 | 0 | 0 | 0 | 0 | `N/A` |
| GK-SC-2010 | 0 | 0 | 0 | 0 | 0 | `N/A` |
| GK-SC-2011 | 0 | 0 | 0 | 0 | 0 | `N/A` |
| GK-SC-2012 | 0 | 0 | 0 | 0 | 0 | `N/A` |
| GK-SC-2013 | 21 | 0 | 0 | 0 | 21 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/answer_clean_candidates.jsonl` |
| GK-SC-2014 | 0 | 0 | 0 | 0 | 0 | `N/A` |
| GK-SC-2015 | 0 | 0 | 0 | 0 | 0 | `N/A` |

## 放行限制

1. `answer_candidate_text` 只是本地候选；`答案`/`解答`标签不是权威来源证明。
2. 嵌套标记、OCR 异文、题干与解析混入的行必须人工复核；不能把分析内容当评分点。
3. 独立答案与评分来源、题目定位、教材 KP 双向证据和独立复审均完成前，继续保持 M0。

| 产物 | 路径 |
|---|---|
| 执行脚本 | `scripts/build_answer_clean_candidates.py` |
| 校验脚本 | `scripts/validate_answer_clean_candidates.py` |
