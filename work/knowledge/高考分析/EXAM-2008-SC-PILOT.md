---
schema_version: "exam-analysis-0.1-pilot"
deliverable_id: "EXAM-2008-SC-PILOT"
status: "pilot_segmented"
exam_id: "GK-SC-2008"
source_status: "unverified_local_provided"
source_roles: ["question", "analysis", "answer_scoring_candidate", "advertisement"]
question_count: 21
response_unit_count: 24
choice_group_count: 1
mapping_status: "M0"
textbook_lock_id: "TEXTBOOK-LOCK-2.0-textbook"
textbook_deliverables_sha256: "63a2974acd668e6b9a4b55f4c0a12b4adc42fb9e4df806e0a0a2d336fb723baa"
textbook_validator_run_id: "VAL-20260809-025336+0800"
textbook_validator_sha256: "9ac9195f15aadddcaadb45f92fc31f93867e4daa22cb6c25568130a2dbb2ed58"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
---

# 2008 年四川卷试卷级校准切片

这是教材锁定后的第一份高考试卷处理试点。它验证清洗、材料分离、题目级分割、空白—解析配对和题型归并，不代表来源已被官方核验，也不建立教材 KP 的 M1/M2 关系。

## 处理结果

- 空白卷：21 个题目文件，5 个材料文件；
- 解析卷：21 个题文文件，独立答案/解析 bundle；
- 题型索引：`language_use`、`objective_choice`、`reading_subjective`、`memorization`、`writing`；
- 广告页已隔离；原始 `full.md` 和 PDF 未改写；
- 当前验证报告：[validation.json](../../../Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/review/validation.json)

## 双链入口

- [空白卷清洗稿](../../../Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/clean_md/question.md)
- [解析卷清洗稿](../../../Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/clean_md/analysis.md)
- [题目清单](../../../Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/ledger/questions.jsonl)
- [异常与 OCR 复核清单](../../../Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2008/review/exceptions.jsonl)
- [分割协议](试卷处理协议-v0.1.md)

## 当前边界与后续

1. 本页是 2008 历史试点回执；其旧版节点已规范化为 [统一垂直切片 JSONL](GK-SC-2008-response_nodes_vertical_slice.jsonl)，原始 24 个节点的 155 分包含任选组两个分支，折算后为 150 分。
2. PDF 为扫描型输入，题段仍使用页级回退定位；需要人工视觉复核时，必须单独登记页码与复核者，不把 MinerU 定位当作题级 bbox。
3. 解析卷发布主体、答案/评分权威等级仍未闭合；所有答案保持 `candidate_unverified`，教材关系保持 `M0`。
4. 2009—2024 已完成结构化批次和 M0 首轮；当前已有十一个垂直切片，下一阶段是这些切片（四个正式校准、七个补充结构）的独立第二复审与官方/可核验答案、评分材料核验，不能由本试点页直接宣布正式映射。
