---
schema_version: "2.0-textbook"
review_id: "REV-BOOK-X3-R1-PRIMARY-INDEPENDENT"
deliverable_id: "BOOK-X3"
artifact_version: "0.2.1"
artifact_sha256: "d5e724f15f5e2bea5968337be52d8ebb01c6b9df02dea0ef9758cc4d5383bc6d"
review_round: 1
reviewer: "independent_primary_book_x3_r1"
review_role: "primary"
reviewed_at: "2026-08-09T02:51:02+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "15c7fd318be972203beb258166492be6e19971b8fe71a940a449981e3563cf7a"
validator_run_id: "VAL-20260809-024951+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_book_final_pre_review_v021_current_20260809.json"
validator_report_sha256: "2c7fbf03d09cece3b648ebea61cd236afb9e8e4d8d454666749b5463db788e30"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "0a25402874c73b563eaa8b6feb931a2255acb32e4b03bcd81c3e5e399d3a0298"
---

# BOOK-X3 v0.2.1 独立主审 R1

## 1. 锁定对象、独立性与量表

本轮只审当前册级总表 `BOOK-X3` v0.2.1，不复用 v0.2.0 旧结论，不修改总表正文、上游交付物、ledger、validator 或状态迁移。采用冻结的 `2.0-textbook` 册级量表：总分门槛 90，七维最低分为 `23/17/13/13/8/9/4`。

| 对象 | 当前绑定 |
|---|---|
| 册级总表 | `work/knowledge/册级汇总/BOOK-X3.md`；v0.2.1；SHA `d5e724f15f5e2bea5968337be52d8ebb01c6b9df02dea0ef9758cc4d5383bc6d`；front matter 状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `15c7fd318be972203beb258166492be6e19971b8fe71a940a449981e3563cf7a`；BOOK-X3 条目为 v0.2.1/`linted`，owner `book_x3_rebuild`，最新转换为 `REWORK` |
| validator | `VAL-20260809-024951+0800`；`work/knowledge/_meta/validation_reports/x3_book_final_pre_review_v021_current_20260809.json`；SHA `2c7fbf03d09cece3b648ebea61cd236afb9e8e4d8d454666749b5463db788e30`；`passed`、0 errors、`hash_verification=true` |
| rubric/taxonomy | rubric `2.0-textbook` / SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b` |

v0.2.1 只修复册表主题、任务表中 REC 的裸 `KP-xxx` 缩写，统一为 `KP-CARD-X3-REC-01-*` 稳定 ID；上游 accepted 文件未发生变化。因此本轮同时检查修订后的每个 REC 引用是否能回到当前 accepted 卡片。

## 2. 上游验收、哈希与覆盖审计

### 2.1 四个单元图谱

| 上游ID | ledger 状态/版本 | 当前文件 SHA-256 | KP | 下游知识卡 | 复核结论 |
|---|---|---|---:|---|---|
| `UNIT-X3-U01` | accepted / 0.2.2 | `ed8970bf151ccfea52676e0e25092484ce4a9c6bbc712757fd9de07398bf82b1` | 65 | 4 | 表内版本、SHA、路径与 ledger/实际文件一致 |
| `UNIT-X3-U02` | accepted / 0.2.2 | `262bc994b796d113be275d60386779ab74f588a5c7a77cc74ae7be26da9b38fb` | 74 | 4 | 一致 |
| `UNIT-X3-U03` | accepted / 0.2.0 | `2b2394ca482abedb9a8d5139f2eed28aa4075d629deaaa95dd0655999d14b687` | 78 | 4 | 一致 |
| `UNIT-X3-U04` | accepted / 0.2.7 | `0b9dd1e7040cac06b1d698f2613c1d0cee116803695c06d02d4a3f4d9676d903` | 54 | 2 | 一致 |

独立逐文件哈希核验为 `4/4` accepted 图谱通过；KP 复算为 `65+74+78+54=271`。四图的 reviewer/G4 状态均已写入 ledger，BOOK 未消费其历史 drafted/candidate 版本。

### 2.2 十五张知识卡（含 REC）

BOOK 表列出 U01 4 张、U02 4 张、U03 4 张、U04 2 张、REC 1 张，共 `15/15`。逐条读取 ledger、当前路径和实际文件，结果为 `15/15` accepted，版本及 post-G4/REWORK SHA 全部一致。卡片 KP 复算为：U01 `16+16+16+17=65`，U02 `19+18+19+18=74`，U03 `20+22+18+18=78`，U04 `24+30=54`，REC `16`。

覆盖恒等式成立：单元图谱合计 `271` 个 KP；独立 REC 卡 `16` 个 KP；底层 accepted 卡合计 `287` 个 KP。图谱是卡片的上层综合交付物，不将图谱和所属卡片重复相加。BOOK 的 19 个 direct upstream ID 均唯一、存在于 ledger，且全部为 `accepted`。

### 2.3 来源、前言与边界

- `SRC-MASTER-X3` 仅承担册级母本/范围定位；未登记的 `SRC-PKG-X3-000` 前言包被明确列为不产生正式册级 KP。
- `SRC-PKG-X3-001`—`019` 与 `SRC-CURR-2020` 通过已接受单元/卡片间接消费；课标只用于任务群和学业质量能力定位，不把 4-3 写成学生已达成水平。
- 教材事实、学习提示、项目化建议、外部解析、教师用书和高考资料均有边界声明；未登记的教师用书不被替代消费。

## 3. 册级人文/语言双线、任务与稳定 ID

- 人文主题 `THEME-BOOK-X3-H01`—`H04` 共 4 条，分别覆盖古典传统主体处境、现代社会普通人/乡土共同体、自然—历史—公共知识和证据化阅读责任；每条均回链已接受单元节点或 REC 完整稳定 KP。
- 语言主题 `THEME-BOOK-X3-L01`—`L05` 共 5 条，覆盖古典诗歌体式与鉴赏、现代文学多文体、文言散文方法、科学论著/科学史表达和共同证据化表达程序；均注明语境与迁移边界，不把册级索引新增为教材原子 KP。
- `TASK-BOOK-X3-01`—`04` 共 4 个稳定任务 ID，分别回链 U01—U04 的已接受单元任务；REC 只补充诵读/比较/短评程序，未被误写成具有独立任务包。
- v0.2.1 的 REC 引用已统一为完整形式，例如 `KP-CARD-X3-REC-01-002`、`KP-CARD-X3-REC-01-012`—`016`；不存在新的裸 `KP-xxx` 证据入口。

## 4. 跨单元关系、高考与教师用书治理

### 4.1 五条跨单元关系

`REL-BOOK-X3-001`—`005` 均具有唯一 ID、方向字段和显式 `N/A`，并写出 `na_reason`：前三条缺少册级双方 accepted KP/EV 逐边证据，第四条 REC 与 U01 缺少册内顺序/前提证据，第五条是项目综合工作流而非教材明示的统一递进等级。关系表没有把教材排列顺序、任务群相似性或主题邻近性升级为确定递进。

本轮判定五条 `N/A` 均为合法治理结果，而不是漏填；在缺少两端逐边证据时，保持 N/A 比强造“前置/深化/迁移”更符合冻结边界。由于当前版本没有可确认的正向册级关系，跨单元递进维度保留 0.5 分审慎余量。

### 4.2 高考映射

全册统一为结构化 `N/A | M0 | N/A`。当前没有真题题文—答案/评分—教材 KP/EV 的逐小问闭合证据；BOOK 不把古诗词、人物/环境、文言、科学说明或比较题型相似性升级为 M1—M3。M0 表示尚未完成映射，不表示不会考。高考板块在 G-TB 前暂无适用的双向证据，按项目冻结校准保留 1 分治理余量。

### 4.3 教师用书与开放问题

所有 U01—U04、REC 的教师用书均为 `edition_match=unknown`，可得率和引用率为 0；未用其他版本或网络解析填补。Issue-001 明确当前 ledger 是 15 张 accepted 卡（不是用户曾指称的 18 张），Issue-002—005 分别记录未登记前言卡、教师用书缺源、高考逐小问证据缺口和册级逐边递进缺口。这些均是透明的后续工作项，不被误写为当前事实或通过条件。

## 5. R01—R10 与 P0/P1/P2

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 册次、单元/REC 范围、文本类型、任务群和 REC 稳定引用均可回到 accepted 上游或已注册课标；未见关键事实错误。 |
| R02 | 否 | 19 个上游、287 个底层 KP、4 主题、5 语言主题、4 任务和 5 条关系均可定位；关系缺证处明确为合法 N/A。 |
| R03 | 否 | 4 个单元、REC、前言边界、主题/语言双线、任务、关系、高考 M0、教师用书和 Issue 模块齐全。 |
| R04 | 否 | 教材事实、课标定位、项目建议、外部材料与教师用书缺源分层清楚；未把 REC 缩写或项目解释冒充规范结论。 |
| R05 | 否 | BOOK 只索引 accepted 上游 KP，不新增孤立原子知识点；REC 引用已统一为完整稳定 ID。 |
| R06 | 否 | 高考仅保持合法 M0/N/A，未引用未登记真题、答案/评分或越级建立 M1—M3。 |
| R07 | 否 | 4/4 图谱、15/15 卡片均为 ledger `accepted`，版本、实际 SHA 与 BOOK 表一致。 |
| R08 | 否 | BOOK v0.2.1 与 ledger v0.2.1/`linted`、REWORK post SHA、19 upstream ID、计数和 validator 绑定闭合；REC 裸 KP 旧问题已在新版本关闭。 |
| R09 | 否 | 使用现行课标任务群 5、8、10、12 的受控名称和 2020 修订课标，未改写为固定课型或教学法。 |
| R10 | 否 | 人文/语言双线按具体单元内容建立，未机械铺满核心素养，也未将学业质量 4-3 当作学生达成或题目难度标签。 |

`P0/P1/P2 = 0/0/0`。未发现必须在本 SHA 上返工的阻断缺陷；Issue-001—005 是已显式记录的后续治理项，不改变本轮验收范围。

## 6. 册级量表评分

| 维度 | 权重 | 门槛 | 得分 | 复核依据与扣分 |
|---|---:|---:|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25 | 23 | **25.0** | 4/4 单元、15/15 accepted 卡、REC、前言边界、19 项 accepted upstream 全部覆盖；计数和去重恒等式可复算。 |
| 跨单元递进 | 20 | 17 | **19.5** | 5 条 REL 均有稳定 ID、方向和合法 `N/A/na_reason`，不强造递进；当前没有可确认的正向册级边，审慎扣 0.5。 |
| 分类、去重与稳定 ID | 15 | 13 | **15.0** | 4/5 主题、4 任务、5 REL、19 upstream ID 唯一；287 KP 的图谱/卡片去重口径和 REC 完整 ID 均闭合。 |
| 双线、任务群与课程定位 | 15 | 13 | **15.0** | 人文 4 条、语言 5 条，任务群 5/8/10/12 与 4-3 边界均有上游入口和明确迁移限制。 |
| 高考板块映射 | 10 | 8 | **9.0** | 全册 M0/N/A、不确定性和待解锁条件完整；G-TB 前没有真题逐小问双向证据，保留 1 分治理余量。 |
| 上下游一致性 | 10 | 9 | **10.0** | BOOK/front、ledger、19 个 upstream 状态/版本/实际 SHA、validator 和 REC v0.2.1 修订记录完全一致。 |
| 检索性 | 5 | 4 | **4.5** | 主题、任务、REL、Issue 和完整 REC KP-ID 可定位；部分单元主题仍需沿上游节点二跳复核，扣 0.5。 |
| **合计** | **100** | **90** | **98.0** | **总分与七维单项均达标；R01—R10 全部未触发。** |

## 7. 独立主审决定

**决定：`pass`；总分 `98.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `BOOK-X3` v0.2.1/SHA `d5e724f15f5e2bea5968337be52d8ebb01c6b9df02dea0ef9758cc4d5383bc6d` 通过独立主审，可进入同一版本与同一 SHA 的独立第二复审。本报告不执行 G4、不写回 `accepted`，也不修改 ledger。若册表、任一上游版本/SHA、ledger、rubric/taxonomy 或绑定 validator 改变，本报告立即失效，必须以新绑定从零复核。

## 8. 可复现绑定与报告校验

- 册级总表：`work/knowledge/册级汇总/BOOK-X3.md`；v0.2.1；SHA `d5e724f15f5e2bea5968337be52d8ebb01c6b9df02dea0ef9758cc4d5383bc6d`。
- 单元图谱 post SHA：U01 `ed8970bf151ccfea52676e0e25092484ce4a9c6bbc712757fd9de07398bf82b1`；U02 `262bc994b796d113be275d60386779ab74f588a5c7a77cc74ae7be26da9b38fb`；U03 `2b2394ca482abedb9a8d5139f2eed28aa4075d629deaaa95dd0655999d14b687`；U04 `0b9dd1e7040cac06b1d698f2613c1d0cee116803695c06d02d4a3f4d9676d903`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `15c7fd318be972203beb258166492be6e19971b8fe71a940a449981e3563cf7a`。
- validator：`work/knowledge/_meta/validation_reports/x3_book_final_pre_review_v021_current_20260809.json`；运行 `VAL-20260809-024951+0800`；SHA `2c7fbf03d09cece3b648ebea61cd236afb9e8e4d8d454666749b5463db788e30`；`passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：保持该字段为空，对 canonical 报告字节求 SHA-256，再回填所得值。
