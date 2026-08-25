---
schema_version: "exam-local-analysis-candidate-0.1"
status: "candidate_only"
answer_source_status: "missing_separate_answer_bundle"
scoring_status: "not_available_as_official"
mapping_status: "M0 | kp_id=N/A"
---

# GK-NCA-2023 本地解析候选层

> 该层从解析卷题目段提取可定位候选片段。解析卷不是独立答案/评分材料；本层不改变原答案索引，不提供官方性结论，也不升级教材映射。

- 题目段：22；明确答案片段：6；混合题干/解析候选：16；空缺：0。
- 派生 JSONL：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/local_analysis_candidates.jsonl`。
- 所有记录保留解析段路径、PDF/MinerU/清洗稿链路、源段哈希和候选文本哈希。

## 使用边界

1. `candidate_unverified` 只表示解析段存在显式答案片段，不等于官方答案。
2. `candidate_mixed_analysis` 可能混入题干、解析或学科网考点定位，必须人工分离。
3. 独立答案/评分源缺失时，原 `answer_source_status` 继续为 `missing`；评分状态固定 `not_available_as_official`。
4. 题文—答案/评分—教材 KP 三方证据闭合前，所有映射保持 `M0 / kp_id=N/A`。
