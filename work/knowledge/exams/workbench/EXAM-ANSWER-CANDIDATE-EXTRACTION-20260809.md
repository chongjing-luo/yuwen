---
schema_version: "exam-answer-candidate-extraction-0.1"
status: "candidate_only"
scoring_status: "not_available_as_official"
---

# 高考答案候选层抽取回执（2008—2024）

> 本层是可逆派生物：从现有 `answer_index.jsonl` 的非空字段中截取原文，不修订原文、不补 OCR、不宣称官方答案，也不包含评分标准。

- 年度数：17；候选片段：74；缺失：44。
- 所有记录保留 `source_answer_index`、`source_answer_bundle`、原答案哈希和候选片段哈希；后续清洗必须在该层或其再派生层完成。

| 试卷 | 索引行数 | 候选片段 | 缺失 | 输出 |
|---|---:|---:|---:|---|
| GK-NC3-2016 | 12 | 11 | 1 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers/answer_candidates.jsonl` |
| GK-NC3-2017 | 12 | 12 | 0 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2017/answers/answer_candidates.jsonl` |
| GK-NC3-2018 | 10 | 10 | 0 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2018/answers/answer_candidates.jsonl` |
| GK-NC3-2019 | 10 | 10 | 0 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2019/answers/answer_candidates.jsonl` |
| GK-NC3-2020 | 10 | 10 | 0 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2020/answers/answer_candidates.jsonl` |
| GK-NCA-2021 | 0 | 0 | 0 | `N/A` |
| GK-NCA-2022 | 0 | 0 | 0 | `N/A` |
| GK-NCA-2023 | 0 | 0 | 0 | `N/A` |
| GK-NCA-2024 | 22 | 0 | 22 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/answer_candidates.jsonl` |
| GK-SC-2008 | 21 | 21 | 0 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/answers/answer_candidates.jsonl` |
| GK-SC-2009 | 0 | 0 | 0 | `N/A` |
| GK-SC-2010 | 0 | 0 | 0 | `N/A` |
| GK-SC-2011 | 0 | 0 | 0 | `N/A` |
| GK-SC-2012 | 0 | 0 | 0 | `N/A` |
| GK-SC-2013 | 21 | 0 | 21 | `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/answer_candidates.jsonl` |
| GK-SC-2014 | 0 | 0 | 0 | `N/A` |
| GK-SC-2015 | 0 | 0 | 0 | `N/A` |

## 使用限制

1. `candidate_unverified` 只用于检索和人工比对；不能写入 `official_verified`。
2. `scoring_status=not_available_as_official` 固定不变，直到独立评分标准、发布主体、定位和复核回执同时具备。
3. 长片段、题干与解析混入、OCR 异文和答案与评分点不分离的记录，必须先进入人工清洗队列。
4. 在题文—答案/评分—教材 KP 三方证据闭合前，映射继续保持 `M0 / kp_id=N/A`。

| 产物 | 路径 |
|---|---|
| 执行脚本 | `scripts/extract_exam_answer_candidates.py` |
| 候选层验证 | `scripts/validate_exam_answer_candidates.py`；结果 `work/knowledge/_meta/exam_answer_candidate_validation_20260809.json` |
| 审计总表 | `work/knowledge/_meta/exam_answer_scoring_audit_20260809.json` |
