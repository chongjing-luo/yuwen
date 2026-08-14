---
schema_version: "2.0-textbook"
review_id: "REV-BOOK-B2-R5-PRIMARY-EVIDENCE-DESIGN"
deliverable_id: "BOOK-B2"
artifact_version: "0.2.2"
review_round: 5
reviewer: "evidence_design"
review_role: "primary"
reviewed_at: "2026-08-08T00:25:00+08:00"
artifact_sha256: "7a18f340be194ca2bef08912d45e4765ce231a7785a2aa90e9c3a36bd6a0f4c2"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260807-235457+0800"
batch_id: "B2-BOOK-20260808"
---

# 册级总表主审记录：BOOK-B2（r5）

## 输入与变更范围

- 被评总表 v0.2.2，SHA `7a18f340be194ca2bef08912d45e4765ce231a7785a2aa90e9c3a36bd6a0f4c2`；8 个单元图谱、19 张知识卡（含 REC）均为 accepted。
- 本轮仅关闭 §8 的遗留 `ISSUE-BOOK-B2-001` 状态措辞并升版，明确双审/G4 已完成；六条 REL、来源链、M0 和教师用书边界不变。
- 正文与 ledger 均为 `review_required/version=0.2.2`，validator `VAL-20260807-235457+0800` errors=0。

## 复核结果

- 8/8 单元、19/19 卡和四篇诵读子文本覆盖可复算；人文/语言双线、任务群及 M0/N/A 边界无漂移。
- `REL-B2-BOOK-01`—`REL-B2-BOOK-06` 每条均含具体源/目标 KP-ID、受控关系类型、递进说明和双方 EV-ID，均可在相应 accepted 上游中定位。
- `ISSUE-BOOK-B2-001` 已明确标记为已关闭，不再与 `status` 或 G4 自检互相矛盾。

## 规则与评分

R01–R10=0；P0/P1/P2=0/0/0。

| 维度 | 得分 |
|---|---:|
| 全单元、特殊内容和诵读覆盖 | 25.0/25 |
| 跨单元递进 | 19.0/20 |
| 分类、去重与稳定ID | 14.0/15 |
| 双线、任务群与课程定位 | 14.0/15 |
| 高考板块映射 | 9.0/10 |
| 上下游一致性 | 10.0/10 |
| 检索性 | 4.5/5 |
| **合计** | **95.5/100** |

结论：`pass`。可与独立二审在同一 SHA 上执行最终 G4 状态同步。
