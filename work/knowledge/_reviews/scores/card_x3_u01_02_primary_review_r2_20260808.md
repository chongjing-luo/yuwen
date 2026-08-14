---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-02-R2-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-02"
artifact_version: "0.2.1"
artifact_sha256: "0c27e18d705129f66300204a532108543eb08fee826bc00aa65b488594010e0c"
review_round: 2
reviewer: "independent_primary_x3_u01_02_r2"
review_role: "primary"
reviewed_at: "2026-08-08T22:30:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "15250d2e11689da159230b184b6458319be132d30f5833453c24d9a280c4ca83"
validator_run_id: "VAL-20260808-212325+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-212325+0800.json"
validator_report_sha256: "52a4c7989192b43adb00d08ae7dd233cd08417d9435938a7acca7b0be9fc63d9"
validator_result: "passed"
decision: "rework"
---

# CARD-X3-U01-02 v0.2.1 独立主审 R2

## 1. 输入锁定与独立性

本轮只依据指定的 `CARD-X3-U01-02 v0.2.1` 快照、冻结 `2.0-textbook` knowledge_card rubric/taxonomy、Source/Artifact 注册表、canonical 学生教材、U01 单元任务和现行课标重新复核；不读取或复用旧版评审分数/结论，不修改卡片、账本、validator 或状态。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-02.md`；v0.2.1；SHA `0c27e18d705129f66300204a532108543eb08fee826bc00aa65b488594010e0c`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-002-PDF`；SHA `89a807fd0f166c4999331ca024f83d72f567aebce533b1eb23f34fa03faa32d5`；7页；物理页12—18、切分页1—7 |
| 单元任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；2页；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；66页 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `15250d2e11689da159230b184b6458319be132d30f5833453c24d9a280c4ca83`；CARD-X3-U01-02 为 v0.2.1 / `linted` |
| validator | `VAL-20260808-212325+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `52a4c7989192b43adb00d08ae7dd233cd08417d9435938a7acca7b0be9fc63d9` |

## 2. 内容、页码与结构复核

### 2.1 已通过项

- 1/1 正文子文本《孔雀东南飞并序》完整覆盖序文、正文、注释和学习提示：教材 canonical 物理页12—18/切分页1—7，学习提示在物理页18/切分页7。
- 12/12 EV 均为单值 Q/F/M/D，均登记 Source、canonical Artifact、可回查 locator、短引、支撑关系和 `verified`；EV-010 课标任务群5、EV-011 学业质量4-3、EV-012 教师用书缺源已分拆，职责边界清楚。
- 16/16 KP 具备陈述、主维度、类型、四层主归属、判定理由、证据ID和置信状态；`KP-014` 已从“思维”改为 taxonomy 允许的 `语言`。
- EV-001—008 的序文、兰芝劳苦/遣归、对话、临别动作、磐石蒲苇、逼婚与重逢、双死合葬、乐府/对话/偏义复词学习提示均可在 canonical 页12—18回查；EV-009 任务比较与鉴赏成果定位物理页25/切分页1正确。
- M0 行已清除教材证据，所有真题小问、动作、真题证据和教材证据均为 `N/A`，并明确尚未建立逐小问双向证据；教师用书保持 `edition_match=unknown`。
- KP-008 的事实主体已校正为“太守府君迎亲”，与正文“府君得闻之……交语速装束”等段落一致。

### 2.2 仍需返工的硬门问题

#### A. KP-013 使用非法知识类型（P1）

`KP-CARD-X3-U01-02-013` 的“类型”填为 `比较`。冻结 taxonomy 的 `knowledge_types` 只有：`事实`、`概念`、`程序`、`策略`、`解释`、`价值辨析`；“比较”只在 `kp_relation_types` 中存在，不是知识类型枚举。该行应改为与主张性质相符的合法类型（建议 `解释`），并保留比较关系在陈述/判定理由中。

#### B. KP-013 Claim—Evidence span 仍不闭合（P1）

KP-013 声称作品悲剧成因“**而非男主人公始乱终弃**”。其唯一学习提示证据 `EV-CARD-X3-U01-02-007` 的短引为：`“造成悲剧的原因……是封建礼教的残酷无情”`，省略号没有包含 canonical 原文中的关键限定 `“并非男主人公的始乱终弃”`。物理页18虽能定位完整句，但当前正式短引不能闭合该对比性 Claim。应补齐连续短引，例如 `“造成悲剧的原因并非男主人公的始乱终弃，而是封建礼教的残酷无情”`，或收窄 KP-013 删除“而非……”子主张。

另外，KP-003、KP-007、KP-008、KP-009 的复合陈述仍以代表性短引配合宽页 locator，分别未在登记短引中逐字出现“十七为君妇，心中常苦悲”“处分适兄意”“愁思出门啼”“贺卿得高迁”。这些是可在同页回查的局部 span，建议一并补齐或拆分；至少 KP-013 的关键限定必须在下一版关闭。

## 3. R01—R10 与 P0/P1/P2

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 序文、人物、事件链、正文诗句、太守府君迎亲事实和学习提示均与 canonical 教材一致。 |
| R02 | **是** | KP-013 的正式比较性 Claim 缺少短引中的“并非男主人公的始乱终弃”关键 span；另有若干复合KP短引未完全覆盖全部子主张。 |
| R03 | 否 | 序文、正文、学习提示、任务、课标、纵向、高考和三类教学提示模块齐全。 |
| R04 | 否 | 当前课标 M、教师用书 D 和项目建议已分层，未把缺源声明冒充课标原文。 |
| R05 | **是** | KP-013 的知识类型“比较”不在冻结 `knowledge_types` 枚举中；同时其关键 Claim—EV span不完整。 |
| R06 | 否 | 高考严格保持 M0/N/A，未引用未登记真题、答案或评分资料。 |
| R07 | 否 | 仅消费已登记并核验的教材、任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 版本、卡片 SHA、ledger transition、Source/Artifact ID、KP/EV 数量和路径一致。 |
| R09 | 否 | 现行课标任务群名称和三类语文活动使用正确，未改写为固定课型。 |
| R10 | 否 | 未机械铺满四项核心素养，未把学业质量描述当作单课完整水平或难度标签。 |

`P0/P1/P2 = 0/2/1`。P1 为 KP-013 非法知识类型及其关键比较性证据 span 未闭合；P2 为其他复合 KP 的可选 span 加固项。

## 4. knowledge_card 量表诊断分

因 R02/R05 硬门尚未通过，以下为返工成本诊断分，不替代合格性判断。

| 维度 | 权重 | 门槛 | 诊断得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 20.0 | 12/12 EV 的 Source/Artifact/locator/类型均合规；KP-013关键短引未闭合，其他复合KP还有代表性短引缺口。 |
| 事实与术语准确性 | 20 | 18 | 17.5 | 正文事实主体、太守府君迎亲、任务、M0和课标术语准确；KP-013知识类型枚举错误，扣分。 |
| 字段完整与知识粒度 | 15 | 12 | 14.0 | 1/1子文本、16/16 KP、12/12 EV、任务/课标/教学模块完整；KP-013需改合法类型并收紧证据闭合。 |
| 双维度与母题质量 | 15 | 12 | 14.0 | 人文/语言双线覆盖悲剧结构、人物、对话、偏义复词和跨文本比较；局部比较证据缺span，保守扣分。 |
| 四层与高考映射 | 10 | 8 | 9.5 | KP层级理由完整，M0契约和不确定性边界清楚。 |
| 纵向贯通 | 8 | 6 | 8.0 | 相邻卡和前后册尚未完成同版本双审，N/A理由充分。 |
| 教学可用性与表达 | 7 | 5 | 6.5 | 对话/动作、偏义复词、情节表和任务成果均可操作；KP-013修复后检索更稳。 |
| **合计** | **100** | **85** | **89.5** | 诊断总分达到部分质量要求，但总分与证据/准确性单项均未过门槛，且 R02/R05 仍触发。 |

## 5. 返工与决定

1. 将 KP-013 类型从 `比较` 改为 taxonomy 允许的合法类型（建议 `解释`），保留“比较”作为关系/动作表述而非知识类型。
2. 补齐 EV-007 的完整原文 `“造成悲剧的原因并非男主人公的始乱终弃，而是封建礼教的残酷无情”`，或收窄 KP-013；同时回归检查 KP-003/007/008/009 的关键短引 span。
3. 重新计算卡片 SHA、更新 ledger transition、运行 validator，并以新 SHA 重新进行 primary/secondary 双审。

**主审决定：`rework`。** 当前 v0.2.1/SHA 不得进入 `accepted` 或被单元图谱正式消费；完成 KP-013 类型和证据 span 修复后再复审。

## 6. 可复现绑定

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-02.md`；v0.2.1；SHA `0c27e18d705129f66300204a532108543eb08fee826bc00aa65b488594010e0c`。
- 学生教材 canonical：`ART-PKG-X3-002-PDF` SHA `89a807fd0f166c4999331ca024f83d72f567aebce533b1eb23f34fa03faa32d5`；单元任务 canonical：`ART-PKG-X3-005-PDF` SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；课标 canonical：`ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- ledger：`work/knowledge/_meta/deliverables.jsonl` SHA `15250d2e11689da159230b184b6458319be132d30f5833453c24d9a280c4ca83`。
- validator：`VAL-20260808-212325+0800`；归档报告 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-212325+0800.json` SHA `52a4c7989192b43adb00d08ae7dd233cd08417d9435938a7acca7b0be9fc63d9`；结果 `passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
