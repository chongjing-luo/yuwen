---
review_id: book_b2_secondary_review_r1_20260807
review_type: secondary_book_summary_review
scope: BOOK-B2
reviewer: unit_u08_secondary
review_mode: independent_blind_review
review_date: 2026-08-08
validator_run_id: VAL-20260807-234530+0800
validator_result: passed
validator_errors: 0
---

# BOOK-B2 册级总表独立二审（r1）

## 结论

覆盖、前言、双线课程定位、M0 治理和教师用书边界均通过；但第 5 节六条跨单元递进关系只写单元名及“对应 KP/EV”，没有具体源/目标 KP-ID 和双方 EV-ID，无法按册级关系证据 checkpoint 复算。因此本轮暂不通过，结论为 `conditional`，需补齐关系证据后复审。

暂评分 93.0/100（覆盖25、递进14、分类14、双线15、高考10、一致性10、检索5）；数值分不替代 P1 硬门。

## 覆盖与边界核验

- ledger 核验：8 个 `UNIT-B2-U01`–`UNIT-B2-U08`、19 张 B2 知识卡（含 `CARD-B2-REC-01`）均为 `accepted`；覆盖计数与正文 8/8、19/19 一致。
- 前言证据明确回链 `SRC-PKG-B2-000` / `ART-PKG-B2-000-PDF` 与物理页/切分页定位；目录篇名未被直接冒充 KP。
- 人文主线、语言主线、任务群和 REC 文体差异分层清楚；高考五板块均保持 M0/N/A，未消费未登记真题。
- 教师用书 `edition_match=unknown`，来源可得率与引用率为 0，不以其他册或网络材料替代。
- 总表 front matter/ledger 均 `drafted`，版本 `0.2.0`；当前 SHA `64ebcbf44746a1b31d63c8fb2d2b7a07e9b7947e5164fd8f0fd10ce2cdbac3b3`。

## P/R 结果

- R01–R10：未触发。
- P0：0；P1：1；P2：0。
- P1-BOOK-B2-REL-001：§5 六条关系的源、目标和证据仅写 `UNIT-B2-Uxx对应KP/EV`，未列具体 `KP-CARD-B2-...` 和 `EV-CARD-B2-...`。这使“双方 accepted KP、关系类型、双方 EV 和版本哈希”这一生效条件无法复核，也无法确定关系是否真正落在所述卡片上。

## Validator

独立 validator `VAL-20260807-234530+0800`：`passed`，errors=`0`。三个 warning 为项目级外部来源/后续 G-TB 校准提示，不改变上述正文证据缺口。

## 修复要求

将六条关系改为明确的源 KP → 目标 KP（可列多个）并逐条列出双方 EV-ID；修订后递增版本、重算 SHA、复跑 validator，再进行 r2 复审。未补齐前不应进入 BOOK-B2 的 G4 `accepted` 写回。
