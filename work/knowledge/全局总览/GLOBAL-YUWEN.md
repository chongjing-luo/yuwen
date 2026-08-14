---
schema_version: "2.0-candidate"
deliverable_id: "GLOBAL-YUWEN"
status: "drafted"
source_ids:
  - "SRC-CURR-2020"
producer: "throughput_generator"
reviewers: []
version: "0.2.0"
---

# 高中语文知识体系总览

> 本总览为 drafted 状态的结构性索引；各册卡、图谱与册表以
> `work/knowledge/_meta/deliverables.jsonl` 账本为权威状态源。

## 1. 五册覆盖

| 册次 | 册级总表 | 卡片 | 单元图谱 | 账本状态 |
|---|---|---:|---:|---|
| 必修上册 | BOOK-B1 | 20 | 8 | accepted |
| 必修下册 | BOOK-B2 | 19 | 8 | accepted |
| 选择性必修上册 | BOOK-X1 | 13 | 4 | accepted |
| 选择性必修中册 | BOOK-X2 | 14 | 4 | accepted |
| 选择性必修下册 | BOOK-X3 | 15 | 4 | accepted |

教材锁定 TEXTBOOK-LOCK-2.0-textbook：114/114（81 卡 + 28 图谱 + 5 册表）全部 accepted，经 G2 校准双审（15 件校准项均 ≥92 分、R01-R10 零触发，见 `work/knowledge/_reviews/scores/g2_review_summary_20260807.md`）。

## 2. 全局能力链

1. 从教材材料和课标语境提取事实、语言形式、人物/观点与文化问题。
2. 通过证据链完成概括、比较、鉴赏、论证、实践或文学创作。
3. 用过程成果、反馈和修订记录评价迁移。
4. 高考映射先以 M0 治理，待小问级双向证据后升级。

## 3. 质量门禁

- 教材卡与图谱已全部 accepted（双人评审 + G2 校准完成）。
- 教师用书仅在已取得同版材料时纳入；未取得版本不填补（现 4/5 册未取得）。
- 课程标准统一使用《普通高中语文课程标准（2017年版2020年修订）》。
- 全流程教学消费：见 `docs/workflow/教学全流程地图.md` 与 `work/evaluation/三目标实现机制.md`（知识库经 lesson_schema/homework/assessment 校验器接入备课管线）。

## 4. 关联交付

- 册级总表：BOOK-B1、BOOK-B2、BOOK-X1、BOOK-X2、BOOK-X3。
- 高考映射：MAP-EXAM-KP；当前全部 M0（题—KP 闭合为登记在案的后续工作）。
- 命题题库与蓝图：`work/knowledge/assessment/`（真题参照条目保持 candidate_only_M0）。
- 教学应用层：`work/teaching/`（作业包/批改量规/学情台账/反思模板）。

| 版本 | 日期 | 修改者 | 变更 |
|---|---|---|---|
| 0.2.0 | 2026-08-14 | yuwen-fullcycle-rebuild | 状态对齐账本（accepted）；补教学应用层入口 |
| 0.1.0 | 2026-08-06 | throughput_generator | 建立五册覆盖、能力链和质量门禁总览 |
