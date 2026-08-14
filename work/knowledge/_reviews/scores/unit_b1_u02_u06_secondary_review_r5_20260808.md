---
review_id: unit_b1_u02_u06_secondary_review_r5_20260808
review_type: secondary_graph_review
scope: [UNIT-B1-U02, UNIT-B1-U03, UNIT-B1-U04, UNIT-B1-U05, UNIT-B1-U06]
reviewer: unit_u08_secondary
review_mode: independent_blind_re-review
review_date: 2026-08-08
validator_run_id: VAL-20260807-233607+0800
validator_result: passed
validator_errors: 0
---

# 必修上册 U02–U06 单元图谱独立二审（r5）

## 结论

五份图谱均达到 unit_graph 校准门槛（92 分），本轮结论均为 `pass`。本轮未修改正文、账本或共享 validator 报告；仅写入本评审报告。

| 图谱 | 内容评分 | P0/P1/P2 | 结论 | 本轮 SHA-256 |
|---|---:|---:|---|---|
| UNIT-B1-U02 | 92.0 | 0/0/0 | pass | `404a4a622feeb67235d16bc11d956c69732517225ff342c108fef46c1cf497b1` |
| UNIT-B1-U03 | 92.5 | 0/0/0 | pass | `53d2e2d0bc6d8e456aa294a75bfee9729c8baddd527b4a90959428c5181156eb` |
| UNIT-B1-U04 | 92.0 | 0/0/0 | pass | `f4252975274f40e28d253b3f4aac0ff1efaee09fc558a3bcc226e59436267672` |
| UNIT-B1-U05 | 93.0 | 0/0/0 | pass | `b26543ddab0104ea8e586010693cfd3f78c649121eb29c4e2a01c16f4734b5ac` |
| UNIT-B1-U06 | 94.0 | 0/0/0 | pass | `a57f9c992c7d531f1adc9e5b086925af9c440707a16c326fdbae90fdb8055861` |

## 独立核验记录

1. 五份正文 front matter 与 `work/knowledge/_meta/deliverables.jsonl` 的 `status`、版本、owner/producer 和 upstream 列表一致；图谱状态均为 `review_required`，上游卡均为 `accepted`。
2. 五份导语均如实说明本次正文修订后的 `review_required` 门禁，不再声称账本为 `accepted`；U05 覆盖结论、前后递进措辞已改为等待图谱复核/双方证据核对；U06 过时的“双方卡尚未验收”条目已关闭。
3. `CAND-`、候选边和“待图谱复核”均有明确限定，不把候选关系写成正式边；历史 `drafted` 仅出现在已标为 resolved 的版本记录中，不构成当前状态断言。
4. 各单元任务均具备规范来源、Artifact 和页码定位；人文/语言双维度、KP/EV 回链、前后递进边界以及 M0 高考治理均可复核。未登记真题不被表述为 M1–M3 直接衔接。
5. 独立 validator：`VAL-20260807-233607+0800`，`passed`，errors=`0`。三个 warning 均为项目级缺源/后续 G-TB 校准提示，不影响本轮教材图谱结构验收。

## P/R 结果

- R01–R10：均未触发。
- P0：0（无关键事实、来源、覆盖或上游门禁错误）。
- P1：0（未发现正文与 ledger 状态漂移、断链或未限定的正式关系）。
- P2：0（此前发现的 U02–U06 导语漂移、U05 旧覆盖条件句、U05 前后递进旧候选措辞和 U06 过时验收条目均已修复）。

## 后续建议

在完成本轮同 SHA 双审记录后，按项目门禁将五份图谱从 `review_required` 转为 `accepted`；教师用书 edition_match、正式真题小问及评分材料仍按各图谱的 open issue 继续补源，不应在当前版本提前建立高考直接衔接边。
