---
schema_version: "exam-missing-answer-source-queue-0.1"
status: "open_missing_authoritative_source"
exam_id: "GK-SC-2013"
generated_at: "2026-08-09T15:02:15+08:00"
authority_gate: `official_verified=0`
scoring_gate: `not_available_as_official`
mapping_gate: `M0 | kp_id=N/A`
---

# 2013 四川卷显式缺失答案/评分来源复核队列

> 本队列只登记待检索节点，不补答案、不生成评分标准，不改变主答案索引。已有本地解析或第三方候选时，仍按 `candidate_only` 处理。

- 队列节点：`23` 个垂直作答节点。
- 题目级范围：Q1—Q21；Q10、Q13 各含两个作答节点。
- JSONL：`work/knowledge/高考分析/EXAM-MISSING-SOURCE-REVIEW-QUEUE-20260809.jsonl`。
- 主答案索引：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/answer_index.jsonl`，保持显式 `missing`，不得回写。
- 本轮外部候选复核：360 文库转链/齐齐文库 29 页预览已抓取，但答案区属于江苏卷并含 Q22—Q29 附加题，复核状态为 `blocked_contaminated`；不改变本队列的 `missing` 门禁。详见 `work/knowledge/高考分析/EXAM-2013-QIQIWENKU-CANDIDATE-REVIEW-20260809.md`。

## 节点清单

| 节点 | 题型 | 分值 | 本地候选 | 第三方候选 | 当前动作 |
|---|---|---:|---|---|---|
| `GK-SC-2013-Q001-TOP` | `word_pronunciation` | 3 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q002-TOP` | `orthography` | 3 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q003-TOP` | `word_usage` | 3 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q004-TOP` | `sentence_grammar` | 3 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q005-TOP` | `modern_reading_informational` | 3 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q006-TOP` | `modern_reading_informational` | 3 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q007-TOP` | `modern_reading_informational` | 3 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q008-TOP` | `ancient_vocab` | 3 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q009-TOP` | `ancient_function_words` | 3 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q010-1` | `classical_translation` | 4 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q010-2` | `classical_translation` | 4 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q011-TOP` | `ancient_text_content` | 5 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q012-TOP` | `sentence_segmentation` | 4 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q013-1` | `poetry_appreciation` | 4 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q013-2` | `poetry_appreciation` | 4 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q014-TOP` | `classical_memorization` | 6 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q015-TOP` | `literary_reading` | 4 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q016-TOP` | `literary_reading` | 6 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q017-TOP` | `literary_reading` | 6 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q018-TOP` | `literary_reading` | 6 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q019-TOP` | `summary_or_application` | 4 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q020-TOP` | `practical_or_expansion` | 6 | 有 | 有 | 检索独立答案/评分材料；无可靠来源则保留 missing |
| `GK-SC-2013-Q021-TOP` | `topic_writing` | 60 | 有 | 无 | 检索独立答案/评分材料；无可靠来源则保留 missing |

## 执行门禁

1. 先确认发布主体、原始 URL/文件和来源快照，再建立候选记录。
2. 客观题只可记录明确答案键；主观题必须区分示例答案、解析和评分点。
3. 每条来源保留 SHA-256、题号边界、题卷双链和复核人/时间。
4. 找不到权威答案或评分材料时，写明检索范围与缺失原因，继续保持 `missing`。
5. 未完成题文—答案/评分—教材 KP 三方证据闭合和独立二审前，禁止 M1+ 映射。

## 既有输入证据

- 垂直节点：`work/knowledge/高考分析/GK-SC-2013-response_nodes_vertical_slice.jsonl`（SHA-256 `1c3d988730a505b9df82654eeaee1151e2bde646286170a846bdbecebc73bc14`）。
- 主答案索引：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/answer_index.jsonl`（SHA-256 `489ba22579be29b0426db2ece4732bc83bc850a903ca8d513c192a510a74289a`）。
- 本地候选：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/local_analysis_candidates.jsonl`（SHA-256 `e1d9294a50e04937e97c456a4df9a8bd37430e794b7b14e4280c6df1a3f2b45c`）。
- 第三方候选：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/reference_answer_candidates.jsonl`（SHA-256 `2a656850f6e6c2b8d64495f684b2b9a8144c690cddd91a4329df9ff90d8bfd7f`）。
- 候选比对：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/reference_answer_candidate_comparison.jsonl`（SHA-256 `7c3268fcdb1f702c216aae2a8c526a77ce0da884f5a1cca9636215a009379b05`）。

## 与主索引的关系

本队列是下游检索任务，不是答案索引。任何新增来源必须先进入独立 registry 和候选 JSONL，经来源权威性审查后，才可讨论是否更新主索引；当前阶段不自动升级任何记录。
