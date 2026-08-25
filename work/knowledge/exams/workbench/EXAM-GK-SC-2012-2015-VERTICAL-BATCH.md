---
schema_version: "exam-vertical-batch-0.1"
batch_id: "SG-EXAM-CAL-SC-2012-2015"
status: "structural_pass_manual_review_pending"
exam_ids: ["GK-SC-2012", "GK-SC-2013", "GK-SC-2014", "GK-SC-2015"]
node_count: 92
adjusted_score_total_by_exam: {"GK-SC-2012": 150, "GK-SC-2013": 150, "GK-SC-2014": 150, "GK-SC-2015": 150}
mapping_status: "M0_only"
source_status: "unverified_local_provided"
textbook_lock_id: "TEXTBOOK-LOCK-2.0-textbook"
---

# 2012—2015 四川卷垂直切片批次

本批次把 2012、2013、2014、2015 四个年度纳入候选作答节点拆解。它只生成可追溯的结构候选，不宣称官方答案、评分标准或教材映射。

| 年份 | 顶层题 | 作答节点 | 原始节点分值 | 任选折算 | 调整后 | 文件 |
|---|---:|---:|---:|---:|---:|---|
| 2012 | 21 | 25 | 155 | Q13 两分支取一支 | 150 | [节点](GK-SC-2012-response_nodes_vertical_slice.jsonl) · [回执](../_reviews/receipts/exam_vertical_GK-SC-2012_20260809.json) |
| 2013 | 21 | 23 | 150 | Q14 八选六，卷面已按 6 分记录 | 150 | [节点](GK-SC-2013-response_nodes_vertical_slice.jsonl) · [回执](../_reviews/receipts/exam_vertical_GK-SC-2013_20260809.json) |
| 2014 | 21 | 22 | 150 | 无 | 150 | [节点](GK-SC-2014-response_nodes_vertical_slice.jsonl) · [回执](../_reviews/receipts/exam_vertical_GK-SC-2014_20260809.json) |
| 2015 | 21 | 22 | 150 | 无 | 150 | [节点](GK-SC-2015-response_nodes_vertical_slice.jsonl) · [回执](../_reviews/receipts/exam_vertical_GK-SC-2015_20260809.json) |

## 处理规则

- 2012 Q13 保留两个候选分支，记录原始分值与折算后分值；总分按卷面选择一支复算为 150。
- 2013 Q14 的“八选六”作为单一 6 分作答节点记录，避免把内部选项误计为 8 个独立计分节点；题段中的孤立 `Y` 显式登记为 OCR/水印疑点。
- 原始 PDF、MinerU `full.md`、清洗稿和题段均只读；每个节点保留清洗题段、原始 MinerU 与 PDF 的双链及页级定位。
- OCR/版面疑点显式写入节点警告，未静默修订；当前 `mapping_level=M0`、`KP_ID=N/A`。答案状态按年度单独登记：2013 已建立 `answer_bundle.md` 与 `answer_index.jsonl`，21/21 行明确为 `missing`；2012、2014、2015 尚未建立答案工件，仍属未核验候选，不得据此生成答案结论。

## 未闭合门

1. 四年题级 PDF 视觉复核与独立第二复审尚未完成；当前回执仅证明结构门禁通过。
2. 解析卷发布主体、官方答案和评分资料仍未核验；不据解析卷生成确定答案。
3. 完成上述复核前，不把本批次升级为正式 `SG-EXAM`，不生成 M1/M2/M3。
