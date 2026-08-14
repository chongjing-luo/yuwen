---
schema_version: "2.0-textbook"
review_id: "REV-CARD-B1-REC-01-R3-SECONDARY-INDEPENDENT"
deliverable_id: "CARD-B1-REC-01"
artifact_version: "0.2.0"
review_round: 3
reviewer: "independent_secondary_b1_rec"
review_role: "secondary"
reviewed_at: "2026-08-07T23:55:00+08:00"
artifact_sha256: "ab88df48e5a68089821939a6c70cb196708103e8bf6e067625eb6212f1b7f72b"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260807-231358+0800"
batch_id: "B1-REC-20260807"
decision: "pass"
---

# 知识点卡独立第二复审记录（R3）：CARD-B1-REC-01

> 本轮是同一正文 SHA 的门禁复核：r2 已指出的四层字段缺失已修订，本轮只确认正文未漂移、账本同步和 P1 清零；不修改正文或账本。

## 1. 输入与账本一致性

- 正文：`work/knowledge/必修上册/cards/CARD-B1-REC-01.md`，v0.2.0、`linted`，SHA `ab88df48e5a68089821939a6c70cb196708103e8bf6e067625eb6212f1b7f72b`。
- 账本 `deliverables.jsonl`：同一 `output_path`、version `0.2.0`、title“古诗词诵读：四篇诗词”、owner `evidence_design`、reviewers `[evidence_design, unit_u08_secondary]`、status `review_required`、source IDs `SRC-PKG-B1-025`/`SRC-CURR-2020`；与正文和当前复审阶段一致。
- 独立 validator：`VAL-20260807-231358+0800`，`passed`、0 errors；报告 `/tmp/val_card_b1_rec_01_secondary_r3_20260807.json`。
- 现场复算：4/4 子文本、12/12 KP、6/6 EV；12 个 KP 行均为 8 列，四层主归属均有值。正文 SHA 与 r2 相同，未发生内容漂移。

## 2. R01–R10 / P 等级

| 代码 | 触发？ | r3 复核依据 |
|---|---|---|
| R01 | 否 | 四篇题名、作者、文体和教材定位保持准确。 |
| R02 | 否 | 6 条教材/课标 EV 与四篇解释链保持有效。 |
| R03 | 否 | 四篇子文本和复合诵读卡范围完整。 |
| R04 | 否 | 教材提示、项目解释、课标和外部来源边界保持分离。 |
| R05 | 否 | 12/12 KP 均有主维度、类型、四层主归属、判定理由和 EV。 |
| R06 | 否 | 高考仍为 M0/N/A，无伪造真题映射。 |
| R07 | 否 | 来源范围仍仅为学生教材包和现行课标。 |
| R08 | 否 | 正文与账本的 ID、version、owner、reviewers、status、title、source/upstream 链一致。 |
| R09 | 否 | 任务群“文学阅读与写作”和课程类型为受控值。 |
| R10 | 否 | 素养/QD 定位仍有诵读、意象细读、比较与表达依据。 |

P0/P1/P2：`0 / 0 / 0`。

## 3. 七维评分（同一正文终版）

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.5 | 6/6 EV 定位、短引文、canonical Artifact 和元数据齐全。 |
| 事实与术语准确性 | 20 | 18 | 19.0 | 四篇事实、教材提示、任务群、M0 和边界准确。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 4 子文本、12 KP、8 列字段和四层归属完整。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文/语言维度保留四篇差异和可执行鉴赏动作。 |
| 四层与高考映射 | 10 | 8 | 9.0 | 12/12 KP 主层级及理由完整；M0/N/A 合规。 |
| 纵向贯通 | 8 | 6 | 6.0 | 双端证据不足时结构化 N/A，未伪造递进边。 |
| 教学可用性与表达 | 7 | 5 | 6.0 | 诵读—意象—情感—比较—修订链可执行。 |
| **合计** | **100** |  | **94.0** | 七项均达门槛。 |

## 4. 结论

- **94.0/100**；七项单项门槛全部达到。
- R01–R10 均未触发；P0/P1/P2=`0/0/0`。r2 发现的账本版本漂移已关闭。
- 决定：**`pass`**。当前卡片可进入协调者 G4；完成双审一致性及状态迁移记录后，方可将 `review_required` 改为 `accepted`。

## 5. 可复现信息

- 卡片：`work/knowledge/必修上册/cards/CARD-B1-REC-01.md`
- SHA：`ab88df48e5a68089821939a6c70cb196708103e8bf6e067625eb6212f1b7f72b`
- Validator：`VAL-20260807-231358+0800`，passed/errors=0；临时报告 `/tmp/val_card_b1_rec_01_secondary_r3_20260807.json`
- Rubric：`2.0-textbook` / SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`
