---
schema_version: "exam-vertical-batch-0.1"
batch_id: "SG-EXAM-CAL-SC-2009-2011"
status: "structural_pass_manual_review_pending"
exam_ids: ["GK-SC-2009", "GK-SC-2010", "GK-SC-2011"]
node_count: 72
adjusted_score_total_by_exam: {"GK-SC-2009": 150, "GK-SC-2010": 150, "GK-SC-2011": 150}
mapping_status: "M0_only"
source_status: "unverified_local_provided"
textbook_lock_id: "TEXTBOOK-LOCK-2.0-textbook"
---

# 2009—2011 四川卷垂直切片批次

本批次在既有 2008、2013、2016、2024 校准结构上，新增 2009—2011 三年作答节点拆解。它只生成可追溯的候选结构，不宣称官方答案、评分标准或教材映射。

| 年份 | 顶层题 | 作答节点 | 原始节点分值 | 任选折算 | 调整后 | 文件 |
|---|---:|---:|---:|---:|---:|---|
| 2009 | 21 | 24 | 155 | Q13 两分支取一支 | 150 | [节点](GK-SC-2009-response_nodes_vertical_slice.jsonl) · [回执](../_reviews/receipts/exam_vertical_GK-SC-2009_20260809.json) |
| 2010 | 21 | 24 | 155 | Q13 两分支取一支 | 150 | [节点](GK-SC-2010-response_nodes_vertical_slice.jsonl) · [回执](../_reviews/receipts/exam_vertical_GK-SC-2010_20260809.json) |
| 2011 | 21 | 24 | 155 | Q13 两分支取一支 | 150 | [节点](GK-SC-2011-response_nodes_vertical_slice.jsonl) · [回执](../_reviews/receipts/exam_vertical_GK-SC-2011_20260809.json) |

## 处理规则

- 文言翻译、诗歌鉴赏、名句默写按卷面小问拆分；任选题保留两个分支，但总分只折算一支。
- 2009 Q14—Q17 的题干集中在 Q17 题段；节点同时登记 `canonical_question_segment` 和 `source_prompt_segment`，不把材料片段误当题干。
- 原始 PDF、MinerU `full.md`、清洗稿和题段均只读；派生节点保留页级定位与双链。
- OCR/版面疑点（2009 Q13、2010 Q14、2011 Q13）显式写入节点警告，未静默修订。
- 三年当前 `answer_source_status=candidate_unverified`，`mapping_level=M0`，`KP_ID=N/A`。

## 未闭合门

1. 三年题级 PDF 视觉复核与独立第二复审尚未完成；本批次回执的视觉状态为 `not_completed`。
2. 解析卷发布主体、官方答案和评分资料仍未核验；不据解析卷生成确定答案。
3. 完成上述复核前，不把本批次升级为正式 `SG-EXAM`，不生成 M1/M2/M3。
