# Luna 交接补充：教材锁定后试卷校准当前状态

本补充文件更新 `LUNA_HANDOFF_TEXTBOOK_THEN_EXAM_20260807.md` 中的动态计数；原交接包保留为历史计划，不再作为当前计数来源。

## 当前门禁

- 教材阶段已完成：`TEXTBOOK-LOCK-2.0-textbook`，`81/81` 卡、`28/28` 图、`5/5` 册表，合计 `114/114 accepted`。
- 试卷阶段已解锁 `SG-EXAM-CAL-2008-2024`，但仍是 `candidate_structural_freeze`，不是正式答案或映射放行。
- 当前所有教材—真题关系固定为 `M0 / kp_id=N/A`。

## SG-METHOD 新来源审计（2026-08-09 追加）

- 隔离审计目录：`work/knowledge/_staging/sg-method-source-audit-20260809/`。
- 审计记录：`source_audit.json`；人工报告：`source_audit.md`。
- 0784（选择性必修上册）和 0786（选择性必修中册）与现有版本分别达到 0.978924/0.987228 的 8-gram Jaccard，判定为同版新载体，不能作为前瞻留出集。
- 0785（选择性必修下册）为 126 页新版本候选，目录包含《风景谈》，与现有 2020 版 122 页且含《一个消逝了的山村》的版本有实质差异；已完成 MinerU 隔离解析，批次 `a8705340-2ebc-4303-8410-75282d0961aa`。
- 0785 的下载 PDF 仍是 `keben.app` 第三方 S3 载体；人民教育出版社官方目录记录 `1411001126201` 仅核对了书名/册次，尚未核验官方 PDF、ISBN 或版次页。因此只能做探索性稳健性 pilot，不能解除 `SG-METHOD = blocked (pending_new_source)`，不能写入 `sources.jsonl`、教材锁定或 Gold。
- 官方阅读器核验补充：已保存官方 `book.swf`、封面/缩略图快照及 SHA；对 `files/mobile/{page}.jpg` 的直接访问返回 `302 /404.html` 后 `403`（`x-tengine-error: denied by Referer ACL`），没有绕过 ACL/WAF，也没有把少量官方资源当作完整 PDF。
- Luna 后续可在隔离区切分 0785 候选，但必须先维持候选状态；若要正式评估，先补官方/授权来源证据，再按协议封存 `12 张卡 + 4 份单元图 + 1 份册表`，然后进行 Gold 双标、查询冻结和观察执行。
- 已准备探索性 pilot 入口：`work/knowledge/_staging/sg-method-source-audit-20260809/keben-app/pilot/x3_exploratory_pilot_manifest.json`，只定义 12 个卡槽、4 个单元图槽和 1 个册级摘要槽，`selection_status=not_sealed`；不得视为 Gold 或正式留出集。
- 已完成该 pilot 的隔离草稿：`x3_exploratory_knowledge_points.jsonl`（12 卡槽/36 KP/38 条证据）、`x3_exploratory_unit_graphs.jsonl`（4 图）和 `x3_exploratory_book_summary.json`（1 册表）；它们均为 `exploratory_only`，不得迁入 canonical、`sources.jsonl`、教材锁定或 Gold。

## 当前产物

- 34 份 PDF 配对，17 个年度；原始 PDF 与 MinerU `full.md` 只读。
- 310 个顶层题目节点、359 个垂直作答节点、30 类题型清洗队列；每个题型页面都显式保留题段、清洗稿、原始 MinerU、原始 PDF 及解析候选（如有）的双链，并由 `validate_exam_type_review_queue.py` 校验路径与页面覆盖。
- 336 个本地解析候选、23 个显式缺失答案源；官方答案核验 0、官方评分材料 0。
- 2013 另有 21 条本地解析候选派生记录（16 条显式答案片段、5 条题干/解析混合片段）；5 条混合段已按源段明确标记分离，见 `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/local_analysis_candidates.jsonl`；不改变 23 个独立答案源缺失状态。
- 新增统一答案/解析候选清洗层：`work/knowledge/高考分析/EXAM-ANSWER-CLEAN-CANDIDATES-20260809.md` 及各有 `answer_index.jsonl` 年份的 `answers/answer_clean_candidates.jsonl`。覆盖 118 条索引记录：47 条有显式分析与答案标记、5 条有分析但无答案标记，其余保持未界定或缺失；所有记录仍为本地候选、`not_available_as_official`、`M0 / kp_id=N/A`。
- 对应人工队列：`work/knowledge/高考分析/EXAM-ANSWER-CLEAN-REVIEW-QUEUE-20260809.md`，当前 45 条；显式“解答→答案”及 2008 年可识别的无标记答案字段已移出边界队列，2016 Q005 的跨题复合源段仍保留人工对齐任务。
- 清洗层回执：`work/knowledge/_reviews/receipts/exam_answer_clean_candidates_20260809.json`，记录 118 条索引覆盖、45 条人工队列、报告/队列 SHA-256 及 `raw_source_mutation=false`。
- 2024 部分参考答案候选：`work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2024.md`，中国教育在线第三方来源派生 Q1—Q9 9 条；校验：`work/knowledge/_meta/reference_answer_candidate_validation_2024_20260809.json`。
- 2024 独立完整第三方候选：`work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2024-MEIPIAN.md`，美篇快照覆盖 Q1—Q22 共 22 条；Q22 明确为作文写作指导候选，不是范文/评分标准。HTML SHA-256 与回执见 `work/knowledge/_reviews/receipts/exam_reference_answer_candidates_meipian_GK-NCA-2024_20260809.json`；校验：`work/knowledge/_meta/reference_answer_candidate_validation_2024_meipian_20260809.json`。主 `answer_index.jsonl` 仍保持 22 条 `missing`。
- 2016 Q006 独立单题候选：`work/knowledge/高考分析/EXAM-REFERENCE-ANSWER-CANDIDATES-2016-Q006.md`，来源为一苇轩第三方题库；候选 JSONL、HTML SHA-256 和回执见 `Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NC3-2016/answers/reference_answer_candidates_q006_gzywtk.jsonl` 与 `work/knowledge/_reviews/receipts/exam_reference_answer_candidate_GK-NC3-2016-Q006_20260809.json`。Q006 主答案索引仍为 `N/A`，未从 Q005 推断。
- 2009、2010、2012—2015 新增来源已正式接入 `Data/reference/gaokao/registry/`：2009 省级网站转载/菁优网解析 PDF 明确覆盖 Q1—Q6；2010 高考网 RAR/DOC 仅明确覆盖 Q1、Q2、Q4、Q8、Q9；2012 附件核验为“题卷文本、无答案内容”并保持阻断；2014 水印图仅覆盖 Q1—Q9；2015 第三方教研附件覆盖 Q1—Q20（Q21 仅作文指导）。这些来源均保留本地 `registry_entry.json`、来源快照/附件哈希与候选层，未写入主答案索引。
- 2024 美篇完整第三方候选与 2016 Q006 一苇轩候选也已追加全局 Source/Artifact/Relation；`sources.jsonl` 38 条、`artifacts.jsonl` 37 条、`source_relations.jsonl` 22 条均通过 JSONL 解析、缺键和重复 ID 检查。候选状态不等于官方核验，`official_verified_questions=0`、`scoring_official_questions=0` 不变。
- 当前状态入口：`work/knowledge/高考分析/SG-EXAM-CAL-STATUS-20260809.md`。

## 已完成的安全修复

2016 Q006、2024 Q006/Q009 和 2024 Q021/Q022 的派生边界已按独立复核修正；所有修改均写入派生 segment/ledger/node 层，原始 PDF、MinerU `full.md` 和 `prompt_text_raw` 保留。2024 Q021/Q022 的本地解析仍只作为候选，不得称官方答案或评分标准。

2013 答案文件是显式缺失占位；验证器已按“显式缺失可通过、但不提供答案”处理。该修复不改变 2013 的 `missing` 状态。

## 执行协议

1. 先做边界与来源审计，再做题型内候选答案清洗。
2. 找不到独立权威来源时登记 `missing`，不以本地解析、搜索摘要、范文或教师用书替代评分材料。
3. 2013 本地解析候选中的混合片段先人工分离；候选答案与分析分开保存，保留题卷、解析卷和派生段的双链及 SHA-256。
4. 统一清洗层中有嵌套标记、OCR 异文或无安全边界的行先进入人工队列；不得把 `answer_key_excerpt` 当作官方答案。
5. 只有题文、答案/评分和教材 KP 三方证据闭合，且完成独立复审，才允许从 `M0` 申请更高映射级别。
