---
schema_version: "2.0-textbook"
review_id: "REV-UNIT-B2-U08-R1-SECONDARY-INDEPENDENT"
deliverable_id: "UNIT-B2-U08"
artifact_version: "0.2.2"
review_round: 1
reviewer: "independent_secondary_u08"
review_role: "secondary"
reviewed_at: "2026-08-07T23:00:00+08:00"
artifact_sha256: "3fae795540ab39facf686836bd5fbad3d4edea5c58157e9cf01a5893cc32f6e5"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260807-224741+0800"
batch_id: "B2-U08-20260807"
decision: "conditional"
---

# 图谱独立第二复审记录（R1）：UNIT-B2-U08

> 本轮为盲审，只读取当前图谱、两张已验收上游卡、账本及契约；未读取任何既有 U08 图谱评审报告，也未修改图谱。评审锁定当前文件 v0.2.2 / SHA `3fae7955…32f6e`。

## 1. 输入锁定与验证

- 图谱文件：`work/knowledge/必修下册/units/UNIT-B2-U08.md`，文件实算 SHA `3fae795540ab39facf686836bd5fbad3d4edea5c58157e9cf01a5893cc32f6e5`；front matter 与版本记录均为 v0.2.2、`linted`。
- 上游卡：`CARD-B2-U08-01` accepted / v0.2.2 / SHA `21fa02bebca5705137692db156cf508602a4eed40ae0eb1babd9383d0952dcf0`；`CARD-B2-U08-02` accepted / v0.2.2 / SHA `3406790c7c97c449e054f9f2fd88d7c3e4da54ae5416c81e39e44ea426acd5c8`。文件实算与任务给定 SHA 一致。
- 独立 validator：`VAL-20260807-224741+0800`，`passed`、0 errors；报告写入 `/tmp/val_unit_b2_u08_secondary_after_ledger_20260807.json`。
- 可复算计数：2/2 accepted 卡、4/4 唯一子文本 ID、24/24 唯一 KP ID、4/4 任务 ID、3 人文节点、3 语言节点、3 交叉边、4 关系 ID；图谱引用的 EV ID 均可回到两张卡。
- 账本已同步为 `UNIT-B2-U08` drafted/v0.2.2、owner `evidence_design`、upstream IDs 与图谱一致；`drafted` 是双审/G4 前的预期状态，不构成缺陷。

## 2. 合同专项核查

| 检查项 | R1 结果 |
|---|---|
| 2 卡、版本、SHA、accepted 门禁 | 通过；两卡状态和 SHA 均与图谱覆盖表一致。 |
| 4 子文本完整稳定 ID | 通过；四个 ID 分别映射《谏太宗十思疏》《答司马谏议书》《阿房宫赋》《六国论》，导语、任务和“如何论证”明确为栏目级材料。 |
| 24 KP 回链 | 通过；24 个 KP 均可解析且无重复，文本 KP 与任务 KP 分开索引。 |
| 4 任务与成果回链 | 通过；四任务均有完整 ID、成果、KP/EV 回链；最新版本已将任务一的 `...01-010`、任务二的 `...01-011/012` 与 `...02-011` 等修正到相应任务。 |
| 人文/语言双维度与交叉 | 通过；3+3 节点、3 条交叉边均有 KP/EV 回链，政治语境、文体和论证差异保留。 |
| 关系 | 4 条关系可形成前提/深化/比较/迁移链，均有稳定 REL ID、受控关系词和 EV；无无效自环。 |
| M0/N/A 与 edition 边界 | 通过；高考为结构化 M0/N/A，前后序为 N/A，TB2 `edition_match=unknown` 明示且未消费。 |

## 3. R01–R10 / P 等级

| 代码 | 触发？ | 依据 |
|---|---|---|
| R01 | 否 | 篇目、作者、册次和任务事实未见严重错误。 |
| R02 | 否 | 图谱节点、任务和关系均有 Card/KP/EV 证据，无无证新增主张。 |
| R03 | 否 | 合编的四篇正文均分别映射到四个子文本；任务材料未误造正文子文本。 |
| R04 | 否 | 教材任务、上游卡解释、项目成果、TB2 unknown 与 M0 边界有区分。 |
| R05 | 否 | 未新增脱离卡片证据的 KP；节点/关系均回链。 |
| R06 | 否 | 未把一般能力相似性升级为 M1/M2/M3，未引用未登记真题。 |
| R07 | 否 | 两个上游均为 accepted，版本和 SHA 锁定一致。 |
| R08 | 否 | 图谱文件与 ledger 的版本、owner、状态和上游 IDs 已同步；`drafted` 符合双审/G4 前状态。 |
| R09 | 否 | 使用现行课标规范任务群“思辨性阅读与表达”。 |
| R10 | 否 | 双维度均以语言实践、证据和任务成果为依据，未机械铺满素养或误用 QD。 |

P0/P1/P2：`0 / 0 / 0`。

## 4. 维度评分

| 维度 | 权重 | 单项门槛 | 得分 | 依据与扣分 |
|---|---:|---:|---:|---|
| 卡片、KP、单元任务覆盖及回链 | 25 | 22 | 25.0 | 2/2 卡、4/4 子文本、24/24 KP、4/4 TASK 全量闭合，版本/owner/upstream 链一致。 |
| 跨课综合、共性与差异提炼 | 20 | 16 | 18.5 | 4 条关系覆盖前提、深化、比较、迁移；赋/史论与奏疏/书信差异清楚；无真跨单元边界时保持候选性扣 1.5。 |
| 人文/语言双维度结构 | 15 | 12 | 14.5 | 3H+3L+3 交叉边覆盖两卡和四篇文本，均有回链；交叉索引未逐 KP 展开扣 0.5。 |
| 单元任务拆解 | 15 | 12 | 14.5 | 四任务描述、成果、任务边界与 KP/EV 回链均准确；缺独立规范 Artifact/page 定位列扣 0.5。 |
| 高考衔接及证据 | 10 | 8 | 9.0 | M0、真题 N/A 与不确定性边界合规；尚无 G-TB 真题双向证据扣 1.0。 |
| 前后递进 | 10 | 8 | 8.0 | 前序/后续均结构化 N/A，并写明双方 accepted 证据缺失及关闭条件。 |
| 可读性与检索性 | 5 | 4 | 5.0 | 章节、表格、稳定 ID、Issue、版本记录和 ledger 链齐全。 |
| **合计** | **100** |  | **95.0** | 25.0 + 18.5 + 14.5 + 14.5 + 9.0 + 8.0 + 5.0 = **95.0**。 |

## 5. 结论与门禁

- **总分 95.0/100**；七项单项门槛全部达到，R01–R10 均未触发，P0/P1/P2=`0/0/0`。
- 决定：**`pass`**；同一 v0.2.2/SHA 已通过独立二审和 validator。协调者完成 G4 双审一致性、reviewers/transition 写回后，方可将图谱状态迁移为 `accepted`。

## 6. 可复现信息

- 图谱：`work/knowledge/必修下册/units/UNIT-B2-U08.md`
- 图谱 v0.2.2 SHA：`3fae795540ab39facf686836bd5fbad3d4edea5c58157e9cf01a5893cc32f6e5`
- 上游：U08-01 v0.2.2 / `21fa02bebca5705137692db156cf508602a4eed40ae0eb1babd9383d0952dcf0`；U08-02 v0.2.2 / `3406790c7c97c449e054f9f2fd88d7c3e4da54ae5416c81e39e44ea426acd5c8`
- Validator：`VAL-20260807-224741+0800`，passed/errors=0；临时报告 `/tmp/val_unit_b2_u08_secondary_after_ledger_20260807.json`
- Rubric：`2.0-textbook` / SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`
