---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-02-R3-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-02"
artifact_version: "0.2.2"
artifact_sha256: "facbb46c6756ba8ed08fa1de91f57bfb858ff72a5ae35460e3d3ece7d068d47d"
review_round: 3
reviewer: "independent_primary_x3_u01_02_r3"
review_role: "primary"
reviewed_at: "2026-08-08T21:29:39+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "11e715dcab5e0a7928852ed991b415555454138d81e8b8367651c830dc8cfd63"
validator_run_id: "VAL-20260808-212605+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-212605+0800.json"
validator_report_sha256: "fbc249e8f68fbb2da54a842c05a320a9a6ed6ae7b4248b946736fdce4245e800"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "25008a7f7f3742f0f58f6d1ebad9e91e3b116a2fd8ba4380d4211b2bc80a3ed8"
---

# CARD-X3-U01-02 v0.2.2 独立主审 R3

## 1. 输入锁定与独立性

本轮从当前 v0.2.2 快照重新开始，仅依据卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 学生教材、U01 单元任务、现行课标、共享账本和指定 validator 归档报告复核；不修改卡片、账本、validator 或状态迁移，也不以旧版报告结论代替当前核验。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-02.md`；v0.2.2；SHA `facbb46c6756ba8ed08fa1de91f57bfb858ff72a5ae35460e3d3ece7d068d47d`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-002-PDF`；SHA `89a807fd0f166c4999331ca024f83d72f567aebce533b1eb23f34fa03faa32d5`；物理页12—18、切分页1—7 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；66页 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `11e715dcab5e0a7928852ed991b415555454138d81e8b8367651c830dc8cfd63`；CARD-X3-U01-02 为 v0.2.2/`linted` |
| validator | `VAL-20260808-212605+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `fbc249e8f68fbb2da54a842c05a320a9a6ed6ae7b4248b946736fdce4245e800` |

## 2. 全量内容、证据与边界复核

- 学生教材 canonical 页12—18完整覆盖序文、正文、注释和学习提示；学习提示在物理页18/切分页7。任务二至任务四在 `ART-PKG-X3-005-PDF` 物理页25/切分页1；课标任务群5在物理页25—27，学业质量4-3在物理页46。
- 16/16 KP 均具有唯一 ID、合法主维度（仅“人文/语言”）、冻结知识类型（事实/概念/程序/策略/解释/价值辨析）、四层主归属、判定理由、证据 ID 和置信状态。KP-013 当前为合法的“解释”，没有把“比较”误作知识类型。
- 12/12 EV 均为单值类型（Q=9、M=2、D=1），均登记适配 Source、canonical Artifact、locator、短引、`supports` 关系及 `verified` 元数据。EV-010（任务群5）和 EV-011（学业质量）各自承担 M；EV-012 单独承担教师用书缺源 D，`edition_match=unknown`，来源职责没有混写。
- EV-001—006 的序文、遣归、告别、逼婚、重逢、双死和合葬引文可在学生教材物理页12—18回查；EV-008 的偏义复词例词和定义可在物理页18回查；EV-009 的比较、鉴赏文章和鉴赏集任务可在任务包物理页25回查。
- 本轮重点核对的 EV-007 已登记连续原文：`“但造成悲剧的原因并非男主人公的始乱终弃，而是封建礼教的残酷无情”`，与 canonical 学习提示物理页18逐字一致；KP-013 的 Claim—EV 关键限定已经闭合。
- KP-008 现写为“太守府君迎亲”。正文先由县令遣媒议亲，随后太守府君安排车马、钱帛和从人排场；卡片没有再将县令写成迎亲主体。KP-003、KP-007、KP-008、KP-009 的代表性短引虽采用省略/压缩并配合宽页 locator，但目标页包含全部相关原文，能够回查，不构成硬门断链。
- 高考栏严格保持结构化 `M0`：真题小问、真题证据和教材证据均为 `N/A`，并说明尚未建立逐小问双向证据；纵向栏以有理由的 `N/A` 表示尚未完成同版本相邻卡双审。三类教学提示分栏，项目建议没有冒充教材或教师用书意见。

## 3. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、人物、序文事件链、正文事实、太守府君迎亲主体和学习提示均与 canonical 载体一致。 |
| R02 | 否 | 12/12 EV 的 Source/Artifact/locator/短引/状态可复核；EV-007 已补齐 KP-013 的完整限定。复合 KP 的压缩短引均有目标页可回查，未出现无适配来源或不可定位直接引文。 |
| R03 | 否 | 正文子文本、序文/正文/学习提示、U01任务、课标、纵向、高考和三类教学提示模块齐全。 |
| R04 | 否 | 教材正文、学习提示、任务、课标 M、教师用书 D 和项目建议分层，未将开放解释或缺源声明冒充规范来源结论。 |
| R05 | 否 | 16/16 KP 均具备合法主维度、受控知识类型、四层归属、判定理由和有效证据；KP-013 枚举问题已关闭。 |
| R06 | 否 | 高考关系保持 M0/N/A，没有未登记真题、答案或评分资料，也未声称 M1—M3 直接衔接。 |
| R07 | 否 | 仅消费已登记并核验的教材、任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片 v0.2.2、账本 transition、Source/Artifact ID、16 KP、12 EV、路径和指定 SHA 一致。 |
| R09 | 否 | 使用现行课标版本、规范任务群名称和三类语文活动，未把任务群改写为固定课型或教法。 |
| R10 | 否 | 人文/语言双线按文本需要展开，未机械铺满四项核心素养，也未把学业质量描述当作单课完整等级或题目难度标签。 |

## 4. P0/P1/P2

`P0/P1/P2 = 0/0/0`。本轮未发现关键事实错误、引文不可定位、非法枚举、版本漂移、M0越权、字段缺失或跨文件断链。复合短引的可选扩充属于表达优化，不影响当前验收。

## 5. 2.0-textbook 量规评分

| 维度 | 权重 | 门槛 | 得分 | 复核依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.0 | 12/12 EV 的来源、canonical Artifact、物理/切页、短引和状态闭合；对少数压缩短引保守扣分。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 正文事实、太守府君/县令角色区分、现行课标术语和来源边界均准确。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 1/1正文子文本、16/16 KP、12/12 EV、任务/课标/教师用书/M0模块齐全。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文与语言双线覆盖悲剧结构、人物处境、对话、偏义复词和《氓》比较，语境差异得到保留。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 各 KP 四层理由清楚，课标能力定位合规，高考 M0 和不确定性边界明确。 |
| 纵向贯通 | 8 | 6 | 8.0 | 未强行建立未完成双审的相邻卡递进关系，N/A 理由充分。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 教材提示、教师用书边界和项目建议分离；情节表、对话证据表和任务成果可直接用于备课。 |
| **合计** | **100** | **85** | **98.0** | 所有单项达到冻结量规门槛，且 R01—R10/P0/P1/P2 均通过。 |

## 6. 主审决定

**决定：`pass`。** 当前 `CARD-X3-U01-02` v0.2.2/SHA `facbb46c6756ba8ed08fa1de91f57bfb858ff72a5ae35460e3d3ece7d068d47d` 通过独立主审，可与同一最终 SHA 的独立第二复审配对进入后续流程。当前账本状态仍为 `linted`；本报告不执行状态迁移。卡片、canonical Artifact、validator、账本或版本绑定发生任何变化，本报告即失效并须以新 SHA 重新复审。

## 7. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-02.md`；v0.2.2；SHA `facbb46c6756ba8ed08fa1de91f57bfb858ff72a5ae35460e3d3ece7d068d47d`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `11e715dcab5e0a7928852ed991b415555454138d81e8b8367651c830dc8cfd63`；CARD-X3-U01-02 为 v0.2.2/`linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-212605+0800.json`；SHA `fbc249e8f68fbb2da54a842c05a320a9a6ed6ae7b4248b946736fdce4245e800`；结果 `passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-002-PDF`=`89a807fd0f166c4999331ca024f83d72f567aebce533b1eb23f34fa03faa32d5`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 值置空后，对 canonical 报告字节求 SHA，并回填于 front matter。
