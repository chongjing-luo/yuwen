---
schema_version: "2.0-textbook"
review_id: "REV-X1-U01-CARDS-R3-SECONDARY-STATUS-SYNC"
deliverable_id: "CARD-X1-U01-01,CARD-X1-U01-02,CARD-X1-U01-03,CARD-X1-U01-04"
artifact_version: "0.2.2/0.2.1/0.2.1/0.2.2"
review_round: 3
reviewer: "independent_status_sync_audit"
review_role: "secondary"
reviewed_at: "2026-08-08T00:41:30+08:00"
contract_version: "2.0-textbook"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260808-004122+0800"
decision: "rework"
---

# 选择性必修上册 U01 四卡最终 SHA 状态同步独立复审

本轮只复核最终卡片 SHA、状态同步元数据、既有内容门结论和 G4 审计链；不修改卡片、`deliverables.jsonl` 或 transition。结论是：四卡正文内容门继续成立，但当前 accepted 状态的控制面尚未闭合，因此本轮不能判为 batch green。

## 1. 最终输入锁定

| 卡片 | 当前版本/状态 | 最终 SHA-256 | 子文本/KP/EV | 与状态同步主审 SHA |
|---|---|---|---:|---|
| CARD-X1-U01-01 | v0.2.2 / accepted | `f9914f386e610ab513fb711222dc07ad2b902a7f7b11dd4525bdeea8fdea2531` | 1 / 12 / 9 | 一致 |
| CARD-X1-U01-02 | v0.2.1 / accepted | `4e0ec11b828790a62f45105bf997ad7dc62581d4243bd4b9404a2d2e9027cb48` | 2 / 12 / 11 | 一致 |
| CARD-X1-U01-03 | v0.2.1 / accepted | `9aa3983cc09606dc35e66ecdf956a984ad6ffdad1771a1b4be875807e9bf65ca` | 2 / 12 / 18 | 一致 |
| CARD-X1-U01-04 | v0.2.2 / accepted | `5940b8f03d12773b6a287a28b512fc53dc222d0d67da68ba3f1c3967bb91511c` | 1 / 12 / 14 | 一致 |

四卡的 front matter 与 ledger 在 `status`、`version`、`source_ids` 和稳定 ID 上一致；KP/EV 数量、单值 `Q`/`M` 类型、M0/N/A、任务群9及文本边界未见新的内容退化。四份状态同步主审均锁定上述最终 SHA。全库 validator `VAL-20260808-004122+0800` 为 `passed`、errors=0，但该 validator 不解析 Markdown front matter、版本记录表、评审者一致性或 transition 完整性，不能替代下列人工 G4 检查。

## 2. 内容门复核

| 检查项 | 结果 |
|---|---|
| 子文本与文本特异 KP | 通过；四卡保持 1/2/2/1 个正文子文本，每卡 12 个唯一 KP，无 generic 占位语句。 |
| EV 与 ID 解析 | 通过；四卡分别 9/11/18/14 条唯一 EV，仅使用单值 Q/M，卡内未发现未定义 EV 引用。 |
| 课标与边界 | 通过；主任务群均为“中国革命传统作品研习”，纵向无边和高考 M0 使用 N/A，未消费教师用书或真题。 |
| 既有七维内容评分 | 保持原独立二审的 97.5/97.0/97.5/97.5；各维度仍高于门槛，R01–R10 内容项未发现新增触发。 |

## 3. 阻断 accepted/G4 的控制问题

### P2-CTRL-01：评审者元数据未同步

四张卡 front matter 仍为 `reviewers: []`，而 ledger 已写为 `["evidence_design", "unit_u08_secondary"]`。当前文件的最终 SHA 是状态同步后新 SHA，旧二审报告锁定的是旧 SHA；因此卡内、账本和最终 SHA 评审记录并未形成同一条可复核链。

### P2-CTRL-02：当前版本未进入版本记录表

四卡 front matter/ledger 已分别升至 v0.2.2、v0.2.1、v0.2.1、v0.2.2，但各卡版本记录表的末行仍分别停在 v0.2.1、v0.2.0、v0.2.0、v0.2.1。状态、自检与版本号已改变，却没有对应的状态同步版本行。

### P2-CTRL-03：两卡标题元数据存在字面漂移

`CARD-X1-U01-02` 与 `CARD-X1-U01-03` 的 front matter 标题和 ledger 标题在冒号、书名号/标点及规范化形式上不完全一致。稳定 ID 未断，但 G4 要求账本与文件元数据一致，需明确采用同一规范串或登记允许的显示标题差异。

### G4-BLOCKER-01：缺少状态迁移记录

`work/knowledge/_reviews/scores/state_transitions_20260807.jsonl` 当前没有四张 X1 U01 卡的接受迁移。主计划要求 accepted 写回同时保存 pre/post SHA、changed_fields、review_refs 和原因；ledger 先行显示 accepted 不能替代 transition 审计记录。

## 4. R/P 与结论

- 内容 R01–R10：全否。
- 内容 P0/P1：0/0。
- 控制面开放 P2：3 个批次级问题；另有 1 个 G4 blocker。
- 决定：`rework`（准确说是“内容通过，状态写回未闭合”），不得把本批标为 green，也不得仅凭 validator passed 宣称 G4 完成。

## 5. 关闭条件

1. 四卡、ledger 与最终评审记录使用一致的 reviewer 身份；若修改卡片会产生新 SHA，须重新锁定并进行状态同步复审。
2. 四卡版本记录表补记当前状态同步版本，或将 front matter/ledger 回退为版本表已登记版本；两种方式均须保持单一口径。
3. 统一 U01-02/U01-03 的标题规范串，或在契约中明确 display title 与 ledger title 可不同。
4. 由协调者追加四条 transition，记录旧/新状态、pre/post SHA、版本、changed_fields 和最终主审/二审引用。
5. 复跑 validator，并对修订后的四个最终 SHA 做一次只针对元数据与 G4 的独立复核；P2 和 blocker 清零后方可判 pass。

## 6. 可复现信息

- ledger SHA-256：`25656b68e4462b3f5ad4d1f79a55665517453ac06c9700a41314214dfb38105c`
- transition 文件 SHA-256：`f24ceb7ce2eef21c1810df156fea22ad26751f81119d72e6ea21360655469775`
- validator 报告：`/tmp/x1_u01_status_sync_secondary_20260808.json`
- validator 局限：当前脚本只检查注册表、固定计数、来源/Artifact/hash、Schema/模板存在性和输出路径，不解析卡片 Markdown 内容或 G4 transition。
