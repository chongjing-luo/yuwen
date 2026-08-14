---
schema_version: "exam-calibration-status-0.1"
status: "candidate_structural_freeze"
calibration_id: "SG-EXAM-CAL-2008-2024"
textbook_lock_id: "TEXTBOOK-LOCK-2.0-textbook"
mapping_status: "N/A | M0 | N/A"
updated_at: "2026-08-10T14:13:32+08:00"
---

# 试卷校准阶段当前状态（2026-08-09）

本文件是 `SG-EXAM-CAL-RECEIPT.md` 的当前状态补充，历史回执不改写。它供 Luna 接手时作为动态状态入口；数量以机器验证报告和派生 JSONL 为准。

## 已锁定前置

- 教材锁定：`TEXTBOOK-LOCK-2.0-textbook`，81 张知识卡、28 份单元图谱、5 份册级总表，`114/114 accepted`。
- 锁定验证：`work/knowledge/_meta/validation_reports/x3_book_g4_final_validation_20260809.json`，结果 `passed`。
- 教材—真题映射仍不得越过 `M0 / kp_id=N/A`。

## 当前计数

| 层级 | 当前值 | 证据 |
|---|---:|---|
| 年度 | 17（2008—2024） | `exam_calibration_manifest.json` |
| PDF 配对 | 34（题卷/解析卷） | `exam_source_audit_20260809.json` |
| 顶层题目节点 | 310 | `exam_response_nodes_top_level.jsonl` |
| 垂直作答节点 | 359 | `exam_vertical_slices_validation.json` |
| 题型队列 | 30 类 | `exam_type_review_queue_validation_20260809.json` |
| 题型页面来源双链 | 359/359 节点的题段、清洗稿、原始 MinerU 与原始 PDF | `exam_type_review_queue_validation_20260809.json` |
| 本地解析候选 | 336 | `exam_answer_scoring_audit_20260809.json` |
| 明确缺失答案源 | 23 | `exam_answer_scoring_audit_20260809.json` |
| 2013 本地解析候选派生层 | 21（16 个显式候选、5 个混合候选；5 个混合段已按显式标记分离题干/解析） | `answers/local_analysis_candidates.jsonl` |
| 统一答案/解析候选清洗层 | 118 条索引记录；47 条显式分析+答案、5 条显式分析无答案，其余未界定/缺失 | `EXAM-ANSWER-CLEAN-CANDIDATES-20260809.md` |
| 显式缺失答案源复核队列 | 23 个垂直作答节点（2013 四川卷；Q10/Q13 含分支） | `EXAM-MISSING-SOURCE-REVIEW-QUEUE-20260809.md` |
| 官方核验题目 | 0 | 同上 |
| 官方评分材料 | 0 | 同上 |

## 已登记的边界修复

- 2016 Q006：正文止于印刷第 11 页，下一节标题从提取 prompt 截断；原始题段和 PDF 未改写。
- 2024 Q006：正文止于印刷第 5 页首行；同步建立 `MAT-2024-SC-02-clean.md`。
- 2024 Q009：截断后续“古代诗文阅读”标题并同步题段、ledger、垂直节点和草稿。
- 2024 Q021/Q022：去除题干尾部下一节标题；解析候选定位到第 17—20 页，第 21 页广告页排除；仍为 `candidate_unverified_local_analysis_only`。
- 2013 答案占位：验证器现接受显式 `missing` 状态，但只把它记录为来源缺口，不把占位文件当答案。
- 2013 解析卷候选层：新增 `answers/local_analysis_candidates.jsonl`，保留 21 个解析段候选；5 个混合段（Q003/Q010/Q011/Q013/Q021）已按源段中明确可见的解析起点分离 `question_excerpt` 与 `analysis_excerpt`，并记录原混合片段哈希；该层不改变原答案索引的 `missing`，也不改变评分和 M0 门禁。
- 统一答案/解析候选清洗层：对现有 `answer_index.jsonl` 的 118 条记录建立 `answers/answer_clean_candidates.jsonl`；只按明确标记切分，保留 `solution_excerpt`、`answer_key_excerpt`、标记清单与原答案哈希。47 条有显式分析和答案标记，5 条有分析但无答案标记；嵌套标记与无边界记录继续进入人工队列，不改变任何权威性、评分或 M0 状态。
- 2008 年 21 条无 `分析/答案`标记的字段已仅按形式分类为短选项、答案评分摘录或评分占位，并保留被移除的题号/分值前缀哈希；这不是答案核验，也不改变其候选状态。
- 2024 参考库新增两层答案候选：已有中国教育在线 Q1—Q9 9 条；另有美篇独立第三方快照覆盖 Q1—Q22 共 22 条，Q22 为写作指导候选。两层均为 `unverified`，主 `answer_index.jsonl` 的 22 条缺失状态不变。
- 2016 Q006 新增一条一苇轩独立第三方候选；本地 Q005/Q006 复合源边界仍保持已对齐、Q006 主索引仍为 `N/A`，没有从 Q005 推断答案。
- 2012—2015 新增来源已接入全局 `Data/reference/gaokao/registry/`：2012 附件确认为“无答案内容”并阻断；2014 水印图只覆盖 Q1—Q9；2015 第三方教研附件覆盖 Q1—Q20（Q21 只有作文指导）。它们均保持候选/阻断状态，不写入主答案索引。
- 全局来源登记当前为 39 条 Source、38 条 Artifact、23 条 Relation；三份 JSONL 均通过解析、缺键与重复 ID 检查。2009 省级网站转载/菁优网解析候选、2010 高考网 RAR/DOC 候选、2013 齐齐文库阻断候选、2016 Q006 与 2024 美篇候选同步登记，官方核验与官方评分计数仍为 0。
- 2009 四川卷新增候选层仅覆盖 Q1—Q6 明确答案键；Q7—Q12 主观示例答案和 Q13 作文指导不进入答案键层。2010 四川卷新增高考网 RAR/DOC 候选层仅覆盖 Q1、Q2、Q4、Q8、Q9；其余题号保持显式缺失。两批候选 JSONL 与验证回执已生成，主答案索引仍未创建/修改。
- 2009 Q6 候选摘录已修复为“答案：”至“参考译文：”之间的显式边界，避免将整段参考译文吞入候选层；2009 候选验证通过（6 条，`main_index_present=false`）。
- 人工队列：`work/knowledge/高考分析/EXAM-ANSWER-CLEAN-REVIEW-QUEUE-20260809.md`，当前 45 条；已将显式“解答→答案”顺序和 2008 年无标记但可识别的短选项/评分字段移出边界队列，仍保留 2016 Q005 的跨题复合源段、无答案标记和缺失源记录。
- 显式缺失源队列：`work/knowledge/高考分析/EXAM-MISSING-SOURCE-REVIEW-QUEUE-20260809.md` 与同名 JSONL，登记 23 个 2013 垂直作答节点；队列验证通过，主 `answer_index.jsonl` 仍为显式 `missing`，不得回写。
- 来源检索回执：`work/knowledge/高考分析/EXAM-REFERENCE-SOURCE-SEARCH-LOG-20260809.md`，记录 2011—2015、2021—2022 的阻断/缺失结论及本轮新增候选，避免重复检索和权威性误判。
- 2013 齐齐文库第三方预览已完整抓取 29 页并登记为 `SRC-GK-2013-SC-QIQIWENKU-ANSWER`，但答案段明确属于江苏卷并含 Q22—Q29 附加题；复核记录 `work/knowledge/高考分析/EXAM-2013-QIQIWENKU-CANDIDATE-REVIEW-20260809.md`，状态 `blocked_contaminated`，不建立题目级候选，不改变主答案索引。
- 该来源完整性与门禁验证回执：`work/knowledge/_reviews/receipts/exam_qiqiwenku_candidate_review_20260809.json`，结果 `passed`；2013 主答案索引 SHA-256 仍为 `489ba22579be29b0426db2ece4732bc83bc850a903ca8d513c192a510a74289a`。

## 本轮验证

以下命令均已通过：

```text
python scripts/validate_sichuan_gaokao_extract.py --year 2008
python scripts/validate_sichuan_gaokao_extract.py --year 2013
python scripts/validate_exam_vertical_slices.py
python scripts/validate_local_analysis_candidates.py
python scripts/audit_exam_answer_scoring_sources.py
python scripts/validate_knowledge_base.py
```

垂直切片验证的分值复算为 17 年全部 `150/150`；`2013` 的答案/评分仍为显式缺失，不能升级为官方来源。

本次 2009 Q6 边界修复后的全量回归结果：答案/评分来源审计通过（官方核验 `0`、官方评分材料 `0`），垂直切片验证通过，知识库验证通过，`pytest` 为 `57 passed`。

本次新增缺失源队列验证：`python scripts/validate_missing_answer_source_queue.py` 通过（23/23，覆盖、唯一性、来源链、M0 与主索引缺失门禁均通过）；答案/解析清洗层重建与 `validate_answer_clean_candidates.py` 也通过。

本次题型归并展示层验证：`python scripts/build_exam_type_review_queue.py` 与 `python scripts/validate_exam_type_review_queue.py` 通过（359 条、30 类）；校验器要求每一条题型页面记录都能回溯到题段、清洗稿、原始 MinerU 和原始 PDF，解析候选仍只在存在时显示且保持未核验。

本轮齐齐文库候选复核：`python scripts/validate_2013_qiqiwenku_candidate_review.py` 通过（29/29 页、污染标记、registry 血缘和主索引 SHA-256 门禁均通过）；来源状态保持 `blocked_contaminated`。

## Luna 下一步放行顺序

1. 只读复核 2016/2024 边界修复及 2024 Q021/Q022 候选解析定位；若发现冲突，新增问题回执，不覆盖 raw/full.md。
2. 对 23 个明确缺失节点建立来源检索清单；可核验官方答案/评分材料缺失时保持 `missing`，不可用搜索摘要补齐。
3. 对 2013 本地解析候选逐题分离“答案候选”和“分析候选”，继续标记 `unverified_local_provided`；5 个混合候选已完成边界清洗，仍需人工复核分析内容。
4. 对 336 个其他本地解析候选逐题分离“答案候选”和“分析候选”，继续标记 `unverified_local_provided`。
5. 完成题文—答案/评分—教材 KP 三方证据闭合及独立二审前，所有节点继续保持 `M0 / kp_id=N/A`。
