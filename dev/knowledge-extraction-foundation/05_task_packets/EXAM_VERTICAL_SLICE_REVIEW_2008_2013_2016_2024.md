# 真题垂直切片复核任务包

## 目标

在 `SG-EXAM-CAL-2008-2024` 的结构候选基础上，复核四个代表卷，完成真实小问/作答节点、分值、答案来源和能力动作编码。任务只允许生成 review receipt 和派生节点文件，不改原始 PDF、MinerU `full.md`、清洗稿或共享主账本。

## 切片

| exam_id | 卷式 | 重点 |
|---|---|---|
| `GK-SC-2008` | 四川旧卷 | 已有 24 个作答节点；复核分值、Q13 任选组和答案分离 |
| `GK-SC-2013` | 四川新旧卷过渡 | Q8—14 文言/翻译/概括/断句/诗歌/默写组合，解析卷答案交错 |
| `GK-NC3-2016` | 新课标Ⅲ | 12 个顶层题，复核复合阅读题的子问拆解和实用类文本 |
| `GK-NCA-2024` | 全国甲卷 | 22 个顶层题，复核现代文/文言/语言运用/作文和解析卷缺失 Q21/Q22 |

## 输入

- [校准 manifest](../../work/knowledge/_meta/exam_calibration_manifest.json)
- [候选 Schema](../../work/knowledge/_meta/exam_schema_0.1.json)
- [候选量表](../../work/knowledge/_meta/exam_rubric_0.1.json)
- [顶层节点 JSONL](../../work/knowledge/高考分析/exam_response_nodes_top_level.jsonl)
- [2008 作答节点](../../work/knowledge/高考分析/EXAM-2008-SC-response_nodes.jsonl)

各年度的原始 PDF、MinerU `full.md`、清洗稿和 `segments/` 位于 `Data/2008-2024·（四川）语文高考真题/`，均只读。

## 每个作答节点必须填写

`response_node_id`、题号/小问、分值、题文规范页码、题干动作、四层、四翼、情境、原子考点、答案来源状态、证据 ID、`decomposition_status`。

## 硬门

1. 题文必须回到 PDF 视觉核对；MinerU 只作定位辅助。
2. 分值合计必须与原卷总分一致；任选组按“分支数”和“计分支数”分开。
3. 解析卷答案/解析与题干分开；本地解析不能标为官方答案或评分标准。
4. OCR 疑点、原卷疑点、缺失题号分别登记，不能静默改写。
5. 没有教材双向证据的关系统一为 `M0`，`KP_ID=N/A`，并填写 `na_reason`。

## 交付

- `work/knowledge/_reviews/receipts/exam_vertical_<exam_id>_<date>.json`
- 派生节点 JSONL（不得覆盖既有 TOP 节点）
- 问题清单：题文、分值、答案来源、定位和映射证据的缺口
- 复跑：

```bash
python scripts/validate_exam_calibration_manifest.py
python scripts/validate_exam_kp_extraction_drafts.py
python scripts/validate_knowledge_base.py
```

在四个切片均通过独立复核前，`SG-EXAM-CAL` 保持 `candidate_structural_freeze`，不得升级正式 `SG-EXAM` 或生成 M1/M2。
