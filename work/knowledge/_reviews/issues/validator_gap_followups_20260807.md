# 验证器与评审门禁待补项（不改变冻结教材契约）

来源：B2 U01 三卡主审/复审过程（2026-08-07）。当前 `TEXTBOOK-CONTRACT-2.0-textbook` 保持冻结；下列事项作为后续工具增强与V3候选，不追溯改写已通过产物。

## 已确认盲区

- Markdown 证据表列数/`claim_type` 缺失时，基础 validator 仍可通过。
- Artifact 为切分 PDF 时，locator 的物理页超出该 artifact 页数，基础 validator 不拦截。
- `Q` 类短引文逐字一致性需要规范 PDF 视觉复核，不能只靠结构校验。
- 评审记录的目标 hash、量表 hash、checkpoint/batch 元数据尚未被机器强制绑定。

## V3 候选回归用例

`reject_evidence_table_column_mismatch`；`reject_artifact_page_out_of_range`；`reject_missing_or_composite_claim_type`；`reject_unregistered_qd_ref`；`require_review_target_hash_and_rubric_hash`；`recompute_checkpoint_scores`；`require_batch_id_before_sampling`；`invalidate_reviews_on_content_hash_change`。

这些用例仅作为后续门禁增强清单。当前批次仍以冻结2.0量表、人工证据复核和双审 hash 锁定为准。
