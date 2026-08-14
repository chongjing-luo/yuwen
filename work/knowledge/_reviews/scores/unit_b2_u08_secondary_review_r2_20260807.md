---
schema_version: "2.0-textbook"
review_id: "REV-UNIT-B2-U08-R2-SECONDARY-INDEPENDENT"
deliverable_id: "UNIT-B2-U08"
artifact_version: "0.2.7"
review_round: 2
reviewer: "independent_secondary_u08"
review_role: "secondary"
reviewed_at: "2026-08-08T00:05:00+08:00"
artifact_sha256: "4c6b6cfc057ed1306e0eb285d0b3c51ef76afdea2e1278608cc1ebadd17dc012"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260807-231720+0800"
batch_id: "B2-U08-20260807"
decision: "pass"
---

# 图谱独立第二复审记录（R2）：UNIT-B2-U08

> 本轮只评 v0.2.7 / SHA `4c6b6cfc…dc012`，独立复算此前主审定向修订；不读取既有 U08 图谱评审报告，不修改图谱或账本。

## 1. 输入锁定与验证

- 图谱：`work/knowledge/必修下册/units/UNIT-B2-U08.md`，front matter v0.2.7、`linted`，SHA `4c6b6cfc057ed1306e0eb285d0b3c51ef76afdea2e1278608cc1ebadd17dc012`。
- 上游：`CARD-B2-U08-01` accepted/v0.2.2/SHA `21fa02bebca5705137692db156cf508602a4eed40ae0eb1babd9383d0952dcf0`；`CARD-B2-U08-02` accepted/v0.2.2/SHA `3406790c7c97c449e054f9f2fd88d7c3e4da54ae5416c81e39e44ea426acd5c8`。图谱覆盖表、ledger 与卡片 SHA 一致。
- ledger：`UNIT-B2-U08` drafted/v0.2.7、owner `evidence_design`、source/upstream IDs 与图谱一致；`drafted` 是 G4 前预期状态。
- 独立 validator：`VAL-20260807-231720+0800`，`passed`、0 errors；报告 `/tmp/val_unit_b2_u08_secondary_r2_20260807.json`。
- 结构复算：2/2 accepted 卡、4/4 子文本、24/24 唯一 KP、6/6 可观察任务成果节点（任务一、任务二三项、任务三、任务四）、3H、3L、3 交叉边、2 卡内关系+1 跨卡关系。

## 2. 合同专项核查

| 检查项 | R2 结果 |
|---|---|
| 上游卡门禁 | 通过；2/2 卡 accepted，版本与完整 SHA 锁定。 |
| 子文本与 KP | 通过；四篇正文分别映射四个稳定子文本；文本 KP、跨文本/单元级 KP、任务 KP 在卡片级索引中分层，不误归入正文子文本。24/24 KP 可回链。 |
| 任务覆盖 | 通过；任务一、任务二第1/2/3项、任务三、任务四六个可观察节点均保留教材义务与项目档案边界；任务二不再误写为单一未拆任务。 |
| 双维度 | 通过；3H+3L、3 条交叉边覆盖公共责任、历史鉴戒、文体/论证、断句翻译和写作迁移。 |
| 关系 | 通过；REL-01/02 为卡内前提/深化，REL-03 为唯一跨卡比较，关系类型、双端 KP 和 EV 均稳定可解析。 |
| M0/N/A 与 edition | 通过；M0 四字段均为结构化 N/A；前后序 N/A 有理由；TB2 `edition_match=unknown` 明示且未消费。 |

## 3. R01–R10 / P 等级

| 代码 | 触发？ | 依据 |
|---|---|---|
| R01 | 否 | 四篇课文、作者、文体、任务边界和上游事实未见严重错误。 |
| R02 | 否 | 节点、任务、关系和成果均有 Card/KP/EV 回链；没有无证新增正式 KP。 |
| R03 | 否 | 2 卡、4 子文本、24 KP 和六个任务成果节点覆盖完整；任务二拆分不构成漏项或模板误用。 |
| R04 | 否 | 教材义务、项目过程档案、卡片解释、TB2 unknown 与 M0 边界分离。 |
| R05 | 否 | 所有正式综合结论均有来源 KP、EV 或任务证据；关系说明不超出上游。 |
| R06 | 否 | 高考严格 M0/N/A，无伪造真题小问或直接衔接。 |
| R07 | 否 | 仅消费两张 accepted 卡；版本、SHA、owner、ledger 和 upstream IDs 一致。 |
| R08 | 否 | 数量、稳定 ID、版本和跨文件链接闭合；4 子文本、24 KP、6 任务节点与关系索引可解析。 |
| R09 | 否 | “思辨性阅读与表达”（学习任务群6）为现行课标受控值，未改写成固定教法。 |
| R10 | 否 | 人文/语言节点均以文本、句式、论证和可观察成果为依据，未机械铺满素养。 |

P0/P1/P2：`0 / 0 / 0`。

## 4. 七维评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | 25.0 | 2/2 卡、4/4 子文本、24/24 KP、6/6 任务成果节点和完整关系索引均闭合；任务二三项分拆、文本/任务 KP 边界清晰。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | 19.0 | REL-01/02/03 分别表达卡内前提、深化和跨卡比较；奏疏/书信与赋/史论差异、历史针对性均保留，扣 1.0 用于图谱仍限于 U08 内部。 |
| 人文/语言双维度结构 | 15 | 12 | 14.5 | 3H+3L+3 交叉边覆盖主题、文体、论证、古汉语和表达迁移；高层本体归并留待册级，扣 0.5。 |
| 单元任务拆解 | 15 | 12 | 15.0 | 任务一、任务二三项、任务三、任务四的教材义务、成果、证据和项目档案边界准确。 |
| 高考衔接及证据 | 10 | 8 | 9.0 | M0 四字段 N/A 且边界清楚；G-TB 前无真题双向 Artifact，扣 1.0。 |
| 前后递进 | 10 | 8 | 8.0 | 前序/后续均结构化 N/A，理由与关闭条件明确。 |
| 可读性与检索性 | 5 | 4 | 5.0 | 覆盖、子文本索引、任务、双维度、交叉、关系、M0、Issue、版本和 ledger 均可检索。 |
| **合计** | **100** |  | **95.5** | 25.0 + 19.0 + 14.5 + 15.0 + 9.0 + 8.0 + 5.0 = **95.5**。 |

## 5. 结论

- **总分 95.5/100**；七项单项门槛全部达到。
- R01–R10 均未触发；P0/P1/P2=`0/0/0`。
- 决定：**`pass`**。同一 v0.2.7/SHA 已通过独立第二复审和 validator；协调者完成 G4 双审一致性、reviewers/transition 写回后，方可将图谱状态从 `drafted` 改为 `accepted`。

## 6. 可复现信息

- 图谱：`work/knowledge/必修下册/units/UNIT-B2-U08.md`
- v0.2.7 SHA：`4c6b6cfc057ed1306e0eb285d0b3c51ef76afdea2e1278608cc1ebadd17dc012`
- Validator：`VAL-20260807-231720+0800`，passed/errors=0；临时报告 `/tmp/val_unit_b2_u08_secondary_r2_20260807.json`
- Rubric：`2.0-textbook` / SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`
