---
schema_version: "2.0-textbook"
review_id: "REV-CARD-B2-U01-01-R3-PRIMARY-EVIDENCE-DESIGN"
deliverable_id: "CARD-B2-U01-01"
artifact_version: "0.2.2"
review_round: 3
reviewer: "evidence_design"
review_role: "primary"
reviewed_at: "2026-08-07T15:42:30+08:00"
---

# 主审记录（R3）：CARD-B2-U01-01

- 锁定版本：v0.2.2 / `linted`
- SHA-256：`f4a31882bed4524fc28cd4f1cd39f5d76cbfde3510ac9089cc7106a280334281`
- 结构校验：`VAL-20260807-154213+0800`通过。
- R2中的母题、文化议题、语言现象、子文本出处及主要正文EV已明显改善。

## 未关闭问题

| 等级 | 定位 | 问题与返修要求 |
|---|---|---|
| P1 | KP-008、§4、EV-003 | KP及课标对接声称覆盖“议论文写作、实词卡片”，但EV-003只定位并引用任务一，EV-007是《齐桓晋文之事》正文，均不能证明任务三、四。补任务三、四逐字EV并重绑KP/§4；当前属于需证主张缺适配证据。 |
| P1 | front matter、§4、EV-005 | `quality_descriptor_refs`与§4仍为`QD-2-1/QD-2-2`，EV-005却引用水平4-2；且4-2实际在课标物理页46，不在所写43—44页。统一采用的表现描述、ID和正确locator，并保持“只定位表现、不判单卡水平”的边界。 |
| P2 | §10版本记录 | front matter已为0.2.2，但版本记录止于0.2.1；补本轮变更记录。 |

## 结论

- 决定：`rework`
- 开放缺陷：P1=2，P2=1。
- 官方总分：`N/A`（存在需证主张缺适配证据）。
- 当前不得进入第二复审；返修后升版、重新lint并提供新哈希，再做R4主审。
- 本记录未修改卡片正文或共享账本。
