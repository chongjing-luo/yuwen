---
review_id: book_b1_secondary_review_r2_20260807
review_type: secondary_book_summary_review
scope: BOOK-B1
reviewer: unit_u08_secondary
review_mode: independent_blind_re-review
review_date: 2026-08-08
validator_run_id: VAL-20260807-234107+0800
validator_result: passed
validator_errors: 0
---

# BOOK-B1 册级总表独立二审（r2）

## 结论

BOOK-B1 当前内容评分 95.5，达到 book_summary 校准门槛，评审结论为 `pass`。总表自身仍按流程保持 `drafted`，不将“评审通过”误写为 G4 `accepted`。

| 维度 | 得分 | 复核要点 |
|---|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25/25 | 8 个单元、4 篇诵读诗词、前言定位和仅 accepted 上游门禁均明确。 |
| 跨单元递进 | 19/20 | 5 条册内关系覆盖深化、迁移、贯通和支撑，均有两端证据。 |
| 分类、去重与稳定 ID | 14/15 | 20 卡、8 图、REC 的受控索引和 REL-ID 稳定，无重复关系。 |
| 双线、任务群与课程定位 | 14/15 | 人文主线、语言主线、任务群和课程定位分层呈现。 |
| 高考板块映射 | 9/10 | 五板块均覆盖；G-TB 前严格维持 M0/N/A。 |
| 上下游一致性 | 10/10 | ledger 与正文状态/版本/上游链一致；KP/EV 可解析。 |
| 检索性 | 4.5/5 | 主题索引和问题清单完整，可定位到单元/KP。 |
| **总分** | **95.5/100** | **pass** |

## 覆盖与状态核验

- ledger 中 8 个 `UNIT-B1-U01`–`UNIT-B1-U08` 和 `CARD-B1-REC-01` 均为 `accepted`。
- B1 知识卡共 20 张，20/20 为 `accepted`；册表覆盖计数与卡清单一致。
- BOOK-B1 正文与 ledger 均为 `drafted`、版本 `0.2.0`、owner/producer 为 `evidence_design`；状态仍等待册表双审/G4，符合流程。
- 当前 SHA-256：`28e90a0b12776410a73d43dbce931edf4f664aade7dd450049b37561196a88a0`。

## REL-ID 与证据可复算性

逐条复核 `REL-BOOK-B1-001` 至 `REL-BOOK-B1-005`：

- 每条均有唯一 REL-ID、明确源/目标 KP 和关系类型；源/目标 KP 均存在于对应 accepted 卡。
- 每条均提供双方 EV；逐一回查后，所有 EV-ID 均存在于其声明的源卡/目标卡，未发现错卡、孤立或只单向给证据的关系。
- 关系说明区分深化、迁移、贯通、支撑，不把主题相似性直接升级为正式递进；候选/待核边界有总则约束。

## 边界与治理核验

- 高考五板块只记录 M0/N/A；未登记真题小问、答案或评分材料，不声称 M1–M3 直接衔接。
- 教师用书 `edition_match=unknown`，来源可得率和引用率均为 0，不消费其他册教师用书替代。
- 主题归纳明确不替代课文唯一主题；正式关系均回链 accepted KP/EV。
- 独立 validator `VAL-20260807-234107+0800`：`passed`，errors=`0`。3 条 warning 均为项目级外部来源/后续 G-TB 校准提示。

## R/P 结果

- R01–R10：均未触发。
- P0/P1/P2：`0/0/0`。
- 本轮未修改 BOOK-B1、ledger 或共享 validator 报告。
