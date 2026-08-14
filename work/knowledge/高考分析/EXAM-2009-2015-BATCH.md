---
schema_version: "exam-analysis-0.2-batch"
deliverable_id: "EXAM-2009-2015-SC-BATCH"
status: "pilot_segmented_structural_validation_passed"
years: [2009, 2010, 2011, 2012, 2013, 2014, 2015]
exam_count: 7
paper_count: 14
top_level_question_count_per_exam: 21
mapping_status: "M0"
source_status: "unverified_local_provided"
textbook_lock_id: "TEXTBOOK-LOCK-2.0-textbook"
textbook_deliverables_sha256: "63a2974acd668e6b9a4b55f4c0a12b4adc42fb9e4df806e0a0a2d336fb723baa"
---

# 2009—2015 四川适用高考语文批次处理回执

本批次沿用 2008 校准的清洗、双链和页级回溯约束，但按年份切换题型与章节配置：

- 2009—2012：Q1—Q21，第一卷 Q1—Q10；
- 2013—2015：Q1—Q21，第一卷 Q1—Q9，Q10—Q14 为非选择题文言/断句/诗歌/默写组合；
- 2011 空白卷 Q4 缺失题号、2012 Q6 OCR 为 `0.`、多年份 Q6/Q7 或 Q3/Q4 同行，均采用顺序校准并保留原始字样；
- 解析卷按题号挂接，不把交错答案/解析升级为题干事实源；未核验答案不称官方答案。

## 已生成

每个 `GK-SC-YYYY/` 包含：

- `clean_md/question.md` 与 `clean_md/analysis.md`：清洗副本，原始 MinerU/PDF 只读；
- `segments/question/Q001.md`—`Q021.md` 与 `segments/analysis/Q001.md`—`Q021.md`；
- `materials/MAT-YYYY-SC-01.md`—`04.md`；
- `by_type/` 双链索引、`ledger/questions*.jsonl`、`review/exceptions*.jsonl`；
- `review/validation-YYYY.json`：结构验证报告。

## 验收结果

2009—2015 七个年度均通过 `validate_sichuan_gaokao_batch.py`：题号集合恰为 1—21、空白/解析各 21 段、清洗副本含原始哈希、段落哈希与 PDF/MinerU/清洗稿双链、材料链接目标存在、推广广告不进入清洗正文。

这只是结构化批处理门禁，不等于人工 PDF 仲裁、来源权威核验或教材知识点映射。完成 `SG-EXAM-CAL` 双人复核前，教材—真题关系继续保持 `N/A | M0 | N/A`。

2009—2015 已另行完成候选作答节点的结构拆解：2009/2010/2011 各 24 个、2012 为 25 个、2013 为 23 个、2014/2015 各 22 个，共 164 个；见 [2009—2011 批次](EXAM-GK-SC-2009-2011-VERTICAL-BATCH.md) 与 [2012—2015 批次](EXAM-GK-SC-2012-2015-VERTICAL-BATCH.md)。各批次仍需题级 PDF 视觉复核、独立第二复审和答案/评分来源核验。

## 入口

- [输出 README](../../../Data/2008-2024·（四川）语文高考真题/exam_extract/README.md)
- [处理脚本](../../../scripts/split_sichuan_gaokao.py)
- [批次验证脚本](../../../scripts/validate_sichuan_gaokao_batch.py)
- [2008 校准回执](EXAM-2008-SC-PILOT.md)
