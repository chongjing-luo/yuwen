---
checklist_id: "G4-CHECK-X1-U03-U04-20260808"
scope: ["UNIT-X1-U03", "UNIT-X1-U04"]
status: "pending_reviews"
created_at: "2026-08-08T16:10:00+08:00"
author: "unit_x1_u03_graph"
---

# X1 U03/U04 图谱 G4 回写清单（不改正文）

本清单只记录协调者在同一版本、同一 SHA 的主审与独立二审完成后应执行的控制面核对；当前不修改图谱正文、知识点、证据、关系、引文或 locator，也不执行 G4。

## 当前冻结快照

| 交付物 | 文件版本/SHA | front/ledger 状态 | 当前评审证据 | 阻断 |
|---|---|---|---|---|
| UNIT-X1-U03 | v0.2.2 / `f4dcefa2dfef5d0fa1bed6c17506d98f4e099ae4889a27023993b87a900d74da` | `linted` / `linted` | primary R3 `pass` 100.0，`VAL-20260808-155542+0800`；待同 SHA secondary | 未形成 DG3 双审 |
| UNIT-X1-U04 | v0.2.0 / `c2a7ebf19d8681f612a78c146b914a66601a10bdc4abbf04cdef320615226de2` | `linted` / `linted` | 尚无图谱 primary/secondary；版本记录旧 validator `VAL-20260808-153415+0800` | 须从零双审并绑定新 validator |

上游快照：U03 的四张卡均 `accepted`（当前图谱 §1 已绑定其 SHA）；U04 的 `CARD-X1-U04-01` 已 `accepted` v0.3.0 / `0a500cb3543974c6ac3d7cde61e9af0d09f56115bcef510b913ff836d022aebc`。

## 双审完成后的 G4 门槛

- 主审和独立二审必须绑定同一 `artifact_version`、图谱文件 SHA、rubric/taxonomy SHA、upstream snapshot 和 validator run；旧版评审不得拼接。
- 两审均 `pass`；R01—R10 全否；P0/P1/P2=`0/0/0`；单元图谱总分≥88，七维最低分 `22/16/12/12/8/8/4`；总分差≤5、任一单维差≤2。
- Claim—Evidence、Q quote span、I 双证、Card/KP/TASK/CAND/REL 覆盖、M0/N/A、上游 SHA 和受控关系类型均为 100% 闭合。
- `pass` 只闭合 DG3；缺少 DG4 receipt、ledger/transition 写回或最终 validator 复跑不得标记 `accepted`。

## 控制面回写（仅协调者执行）

1. 在每件完成双审后归档带唯一 run_id 和 SHA 的 validator 报告副本；不要只保留会被后续运行覆盖的 `latest.json`。
2. 将图谱 front matter 的 `status` 从 `linted` 改为 `accepted`，`reviewers` 填入实际 primary/secondary reviewer；版本、source_ids、upstream_card_ids 不改。
3. 将 `deliverables.jsonl` 中对应条目同步为同一 `status/version/owner/reviewers/source_ids/upstream_deliverable_ids`，不提前刷新册级总表。
4. 各追加一条 `state_transitions_20260807.jsonl`：`linted→accepted`、reviewed version、pre-SHA、状态写回后的 post-SHA、changed_fields、两审 review_refs、validator/report SHA、原因和下游影响。
5. 保存 DG4 receipt：batch snapshot、版本与前后 SHA、claim/EV binding、Q/I 核验日志、两份评审及 SHA、问题/缺陷关闭表、validator、ledger/transition 和影响清单。
6. 回写后重跑 validator，并核对 front matter↔ledger↔transition↔receipt；只有该闭环完成，图谱才可被 `BOOK-X1` 消费。

## 正文保护与失效规则

- G4 不得改动正式 Claim、KP、EV、Source、Artifact、locator、引文、关系、任务、M0/N/A 或版本号；不在本清单执行 self-check/issues/version-history 的正文同步。
- 若协调者确需同步正文中的 self-check/issues/version-history，必须按旧 `2.0-textbook` 生命周期白名单记录允许差异、重算 post-SHA 并确认不改变语义 content；任何非白名单内容变化都使两审失效，必须升版并从 DG1 重走。
- U03 v0.2.0/v0.2.1 评审与 U04 generic 旧草稿均不得支撑本清单后的 G4；旧 transition 仅作审计历史，不覆盖新 transition。

