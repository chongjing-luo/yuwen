---
schema_version: "2.0-textbook"
review_id: "REV-BOOK-B1-R1-SECONDARY-INDEPENDENT"
deliverable_id: "BOOK-B1"
artifact_version: "0.2.0"
review_round: 1
reviewer: "independent_secondary_book_b1"
review_role: "secondary"
reviewed_at: "2026-08-08T00:25:00+08:00"
artifact_sha256: "d539a42af99897e1fe75c1f1ef15cf82c06567b1f556c1a583ecba5ad67ad759"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260807-232043+0800"
batch_id: "B1-BOOK-20260807"
decision: "conditional"
---

# 册级总表独立第二复审记录（R1）：BOOK-B1

> 本轮为独立盲审，只读取当前册表、B1 账本和上游正文的可复算状态；不读取既有 BOOK-B1 评审报告，不修改正文或账本。

## 1. 输入锁定与全量覆盖

- 册表：`work/knowledge/册级汇总/BOOK-B1.md`，v0.2.0、`drafted`，SHA `d539a42af99897e1fe75c1f1ef15cf82c06567b1f556c1a583ecba5ad67ad759`。
- 独立 validator：`VAL-20260807-232043+0800`，`passed`、0 errors；报告 `/tmp/val_book_b1_secondary_r1_20260807.json`。
- ledger 计数：20/20 B1 知识卡、8/8 B1 单元图谱、1/1 B1 REC 卡均列为 `accepted`；BOOK-B1 ledger 为 drafted/v0.2.0、owner `evidence_design`，与册表 front matter 一致。
- 覆盖结构：U01(3)+U02(3)+U03(3)+U04(1)+U05(1)+U06(4)+U07(3)+U08(1)+REC(1)=20 卡；8 图与 1 REC 均列入 upstream。课程前言 `SRC-PKG-B1-000`、课标 `SRC-CURR-2020` 已登记。

## 2. 关键问题与契约核查

| 检查项 | R1 结果 |
|---|---|
| 20 卡/8 图/REC 全量覆盖 | ledger 分子分母通过；但册表第1节仍写 REC“当前待同SHA双审/G4”，与 ledger 已 accepted 矛盾，需清理措辞。 |
| 前言与课标证据 | `EV-BOOK-B1-001—003` 对前言目录、覆盖治理和课标定位有规范 Artifact/页码；通过。 |
| 人文/语言双线 | 8 单元+REC均有主题、文体、任务群和读写迁移行；但关键 KP/EV 仅写“UNIT及其上游KP/EV”，未给可检索的具体稳定 KP/EV 集合，扣分。 |
| 跨单元递进 | 五条关系保留方向、类型、差异和生效条件；“双方证据”均为 `UNIT-...对应KP/EV` 泛指，未列源/目标 KP-ID 与双方 EV-ID，不能直接复算关系。 |
| M0 与空白 | 五板块均保持 M0；N/A 说明“不消费试卷”，无 M1/M2/M3 越界。 |
| 教师用书 | 0/8、实际引用0/0、`edition_match=unknown` 明确；通过。 |
| 上游正文/账本一致性 | 发现开放问题：U01/U07正文保留 CAND 候选措辞；U02—U06正文仍写上游 drafted/候选；U08正文 `linted`，而 ledger 为 accepted；REC 卡正文自检仍写尚未 G4，而 ledger 已 accepted。册表已将该风险列 Issue-002，但未关闭。 |

## 3. R01–R10 / P 等级

| 代码 | 触发？ | 依据 |
|---|---|---|
| R01 | 否 | 册次、8 单元、REC 篇目和前言事实未见严重事实错误。 |
| R02 | 否（P1） | 册级主题与递进主张有单元级来源，但五条正式递进只给泛指 KP/EV，证据链不可逐边复算，列定向返修。 |
| R03 | 否 | 20 卡、8 图、REC 和前言模块均有覆盖入口；无整个必填模块缺失。 |
| R04 | 否 | 册级解释声明不替代单篇唯一主题；教师用书与学生教材边界分离。 |
| R05 | 否 | 本册不新增原子 KP；索引回指单元/卡片，问题是可检索性和关系粒度。 |
| R06 | 否 | 全册高考保持 M0/N/A，未伪造真题直接衔接。 |
| R07 | 否（P1） | ledger 上游均 accepted；但多个上游正文仍保留历史 drafted/CAND 状态措辞，需逐图确认并关闭。 |
| R08 | 否（P1） | 数量和 ledger 链闭合，但上游正文状态/候选措辞与 ledger accepted、REC正文自检与 ledger accepted 不一致。 |
| R09 | 否 | 单元任务群沿用各图谱现行课标受控名称。 |
| R10 | 否 | 人文/语言分布有文本、任务和语言实践依据，未机械铺满素养。 |

P0/P1/P2：`0 / 2 / 1`。

## 4. 册级七维评分

| 维度 | 权重 | 门槛 | 得分 | 依据与扣分 |
|---|---:|---:|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25 | 23 | 22.5 | ledger 20/20 卡、8/8 图、REC及前言均纳入；REC“待双审/G4”旧措辞、U08正文 status 与 ledger 不一致扣 2.5，低于门槛。 |
| 跨单元递进 | 20 | 17 | 13.0 | 五条关系方向与差异合理，但无具体源/目标 KP-ID、双方 EV-ID、受控 REL-ID，不能复算关系边，扣 7.0。 |
| 分类、去重与稳定 ID | 15 | 13 | 11.0 | 单元/卡片层级 ID 和目录分组清楚；册级人文/语言行仅泛指“上游KP/EV”，缺可检索 KP 索引和关系 ID，扣 4.0。 |
| 双线、任务群与课程定位 | 15 | 13 | 13.0 | 人文8单元+REC和语言任务群分布完整，前言/课标定位清楚；具体 KP 证据未展开扣 2.0。 |
| 高考板块映射 | 10 | 8 | 9.0 | 五板块均有 M0、N/A 和 G-TB 阶段边界；无真题双向 Artifact 扣 1.0。 |
| 上下游一致性 | 10 | 9 | 5.0 | ledger 计数和 source IDs通过，但 U02—U08/REC 正文历史 drafted/CAND/未G4措辞与 ledger accepted 不一致，且未提供逐图 hash 核对表，扣 5.0。 |
| 检索性 | 5 | 4 | 3.0 | 目录、主题词、Issue 和单元 ID 可检索；缺 KP/EV 具体索引和逐边关系 ID，扣 2.0。 |
| **诊断合计** | **100** |  | **76.5** | 多项低于册表门槛；P1 未清前不具 accepted 验收效力。 |

## 5. 必须返修项与结论

- **P1-BOOK-01：递进关系证据粒度不足。** 将五条跨单元关系改为稳定关系 ID，并逐条列出源/目标单元、源/目标 KP-ID、关系类型、双方 EV-ID 和生效状态；不得用“对应KP/EV”泛指替代。
- **P1-BOOK-02：上游正文与 ledger 状态漂移。** 逐图核对 U01—U08 和 REC 的当前 SHA/version/status；清理 U02—U06 的 drafted/候选旧声明、U01/U07 的 CAND 说明、U08 `linted` 与 ledger accepted 的冲突；同步 REC 卡正文“尚未 G4”自检措辞。不得静默改写，应保留版本记录和核验表。
- **P2-BOOK-01：册表覆盖说明旧措辞。** 第1节将 REC“当前待同SHA双审/G4”更新为与当前 ledger/评审状态一致的表述；Issue-002 关闭条件需写成可复核状态。
- 决定：**`conditional`**（册表覆盖框架和 M0/教师用书治理合格，但递进证据、上游状态一致性和旧候选措辞未清；修订后须以新 SHA 复跑 validator 并重做册级二审）。

## 6. 可复现信息

- 册表：`work/knowledge/册级汇总/BOOK-B1.md`
- SHA：`d539a42af99897e1fe75c1f1ef15cf82c06567b1f556c1a583ecba5ad67ad759`
- Validator：`VAL-20260807-232043+0800`，passed/errors=0；临时报告 `/tmp/val_book_b1_secondary_r1_20260807.json`
- Rubric：`2.0-textbook` / SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`
