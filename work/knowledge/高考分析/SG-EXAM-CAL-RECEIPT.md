---
schema_version: "exam-calibration-receipt-0.1"
calibration_id: "SG-EXAM-CAL-2008-2024"
status: "candidate_structural_freeze"
manifest: "work/knowledge/_meta/exam_calibration_manifest.json"
schema: "work/knowledge/_meta/exam_schema_0.1.json"
rubric: "work/knowledge/_meta/exam_rubric_0.1.json"
validation: "work/knowledge/_meta/validation_reports/exam_calibration_validation.json"
textbook_lock_id: "TEXTBOOK-LOCK-2.0-textbook"
mapping_status: "N/A | M0 | N/A"
---

# SG-EXAM-CAL 校准回执

## 当前结论

17 个年度、34 个配对 PDF 已完成结构性冻结候选：题卷/解析卷角色、卷码、年度题数、题号分母、清洗稿、题目段落、材料对象和验证报告均已登记。校准验证报告为 `passed`，但阶段仍是 `candidate_structural_freeze`，尚不能写成正式 `SG-EXAM-CAL passed`。

原因是三项来源性门禁仍未闭合：

1. 本地 PDF 的发布主体和原始下载 URL 尚未逐卷核验；
2. 解析卷是 `unverified_local_provided` 候选，未取得可核验官方答案/评分资料；
3. 四个正式校准切片和六个补充结构切片的首轮 PDF 视觉核对/小问分值复算尚未全部闭合，独立第二复审仍未完成；2022 空白卷 Q6 已经完成 PDF 视觉恢复并登记手工定位，2024 解析卷 Q21/Q22 仍为缺失答案源。

## 冻结内容

| 项目 | 冻结结果 |
|---|---|
| 年度范围 | 2008—2024，共17年 |
| PDF 配对 | 每年 question + analysis，共34份 |
| 顶层题数 | 2008—2015：21；2016—2017：12；2018—2020：10；2021—2024：22 |
| 原始文件 | PDF 与 MinerU `full.md` 只读，SHA 已核验 |
| 定位 | `page_level_fallback`；不宣称题级 bbox |
| 答案边界 | 解析卷仅为候选；无官方评分资料时不生成确定答案结论 |
| 映射边界 | 默认 M0；M1/M2 需稳定小问与教材双向证据 |

2022 Q006 的例外恢复回执：[Q006 source recovery](../_reviews/receipts/exam_source_recovery_GK-NCA-2022-Q006_20260809.json)。该题使用 `P4-MANUAL-Q006` 合成定位标识，不能据此宣称 MinerU 已识别题文。

## 验证证据

- [全量语料回执](EXAM-2008-2024-CORPUS.md)
- [校准 manifest](../../work/knowledge/_meta/exam_calibration_manifest.json)
- [校准 Schema](../../work/knowledge/_meta/exam_schema_0.1.json)
- [候选量表](../../work/knowledge/_meta/exam_rubric_0.1.json)
- [校准验证](../../work/knowledge/_meta/validation_reports/exam_calibration_validation.json)
- [批次验证脚本](../../scripts/validate_sichuan_gaokao_batch.py)
- [2008 垂直切片节点](GK-SC-2008-response_nodes_vertical_slice.jsonl) · 由旧试点节点规范化生成，保留任选分支原始/折算分值 · [规范化回执](../_reviews/receipts/exam_2008_normalization_20260809.json)
- [2009—2011 补充垂直切片](EXAM-GK-SC-2009-2011-VERTICAL-BATCH.md) · 72 个节点，三年均保持 M0，题级视觉复核待完成
- [2012—2015 补充垂直切片](EXAM-GK-SC-2012-2015-VERTICAL-BATCH.md) · 92 个节点，四年均保持 M0，题级视觉复核待完成
- [2013 垂直切片节点](GK-SC-2013-response_nodes_vertical_slice.jsonl) · [复核回执](../_reviews/receipts/exam_vertical_GK-SC-2013_20260809.json)
- [2016 垂直切片节点](GK-NC3-2016-response_nodes_vertical_slice.jsonl) · [复核回执](../_reviews/receipts/exam_vertical_GK-NC3-2016_20260809.json)
- [2017 垂直切片节点](GK-NC3-2017-response_nodes_vertical_slice.jsonl) · [复核回执](../_reviews/receipts/exam_vertical_GK-NC3-2017_20260809.json)
- [2024 垂直切片节点](GK-NCA-2024-response_nodes_vertical_slice.jsonl) · [复核回执](../_reviews/receipts/exam_vertical_GK-NCA-2024_20260809.json)
- [2008 Q006 视觉复核回执](../_reviews/receipts/exam_visual_review_GK-SC-2008-Q006_20260809.json) · 卷面缺词保留，不补写“得到”
- [垂直切片验证](../_meta/validation_reports/exam_vertical_slices_validation.json)
- [2022 Q006 视觉恢复回执](../_reviews/receipts/exam_source_recovery_GK-NCA-2022-Q006_20260809.json)

## 放行条件

完成上述三类来源/人工复核后，协调者重新运行校准验证，并由独立复审者对 10 个垂直切片复核（2008、2013、2016、2024 为正式校准切片；2009—2012、2014—2015 为补充结构切片）：

- 小问/作答节点拆解和分值复算；
- 题干、材料、答案、解析和评分资料角色分离；
- 四层、四翼、情境、能力动作和原子考点编码；
- 负例（OCR 错字、缺题号、广告、非官方答案）不被静默吞并。

放行前只允许生产结构化草稿和 M0 记录，不允许建立 M1/M2/M3 或教材—真题确定性映射。
