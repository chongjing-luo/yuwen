---
schema_version: "2.0-candidate"
review_id: "REV-BOOK-X3-SECONDARY-R1"
deliverable_id: "BOOK-X3"
artifact_version: "0.2.1"
artifact_sha256: "d5e724f15f5e2bea5968337be52d8ebb01c6b9df02dea0ef9758cc4d5383bc6d"
review_round: 1
reviewer: "independent_secondary_book_x3_r1"
review_role: "secondary"
reviewed_at: "2026-08-09T02:55:00+08:00"
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
report_sha256: "dbaf08cc587547392db7bcf9dcc1632292b5525f5d3c6d53ce8e4d8f6bb67743"
---

# BOOK-X3 v0.2.1 独立第二复审 R1

## 1. 输入锁定与独立性

本轮只依据当前 BOOK-X3 v0.2.1、其 19 个直接上游交付物、Source/Artifact 注册表、冻结 `2.0-textbook` rubric/taxonomy、共享 ledger 和指定 validator 机械报告独立复核；不复用 v0.2.0 旧绑定、旧分数或旧结论，不修改册表、上游、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 册级总表 | `work/knowledge/册级汇总/BOOK-X3.md`；v0.2.1；SHA `d5e724f15f5e2bea5968337be52d8ebb01c6b9df02dea0ef9758cc4d5383bc6d`；状态 `linted` |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `15c7fd318be972203beb258166492be6e19971b8fe71a940a449981e3563cf7a`；BOOK-X3 v0.2.1/`linted`，19 个直接上游均为 `accepted` |
| validator | `VAL-20260809-024951+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `2c7fbf03d09cece3b648ebea61cd236afb9e8e4d8d454666749b5463db788e30` |
| 冻结量规 | `2.0-textbook`；rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b` |

册表 §1.1/§1.2 中 4 个单元图谱和 15 张知识卡的版本、状态、路径及 SHA 均与 ledger 和当前文件逐项复算一致。册级总量采用图谱去重口径：U01—U04 图谱 `65+74+78+54=271` 个 KP，REC 独立卡 `16` 个 KP，故全册唯一 KP 为 `287`；不能将图谱索引与其所属底层卡再次相加。

## 2. 上游覆盖、哈希与去重口径

### 2.1 单元图谱

| 上游 | 版本 | 当前 SHA | KP | 状态 |
|---|---:|---|---:|---|
| `UNIT-X3-U01` | 0.2.2 | `ed8970bf151ccfea52676e0e25092484ce4a9c6bbc712757fd9de07398bf82b1` | 65 | accepted |
| `UNIT-X3-U02` | 0.2.2 | `262bc994b796d113be275d60386779ab74f588a5c7a77cc74ae7be26da9b38fb` | 74 | accepted |
| `UNIT-X3-U03` | 0.2.0 | `2b2394ca482abedb9a8d5139f2eed28aa4075d629deaaa95dd0655999d14b687` | 78 | accepted |
| `UNIT-X3-U04` | 0.2.7 | `0b9dd1e7040cac06b1d698f2613c1d0cee116803695c06d02d4a3f4d9676d903` | 54 | accepted |
| **合计** | — | — | **271** | **4/4** |

### 2.2 底层卡与 REC

BOOK 表列出 U01 4 张、U02 4 张、U03 4 张、U04 2 张和 REC 1 张，共 `15/15` accepted 卡。卡片 KP 数独立相加为 `65+74+78+54+16=287`，与“图谱 271 + REC 16”相同；14 张单元卡在所属图谱内，仅作上游覆盖和反向检索，不重复计入册级唯一总量。REC 的 16 个 KP 单独计入。

逐项核对结果：BOOK 的 19 个上游 ID 均可在 ledger 找到，状态均为 `accepted`；其表中 SHA 与文件实际 SHA 全部相等，未发现旧 SHA、漏卡、重卡或版本漂移。`ART-MASTER-X3-PDF`（SHA `16a6d823c56a4842a53cb69839d216971a210892d47b3d16877349174d0abc67`）和 `ART-CURR-2020-PDF`（SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`）均为注册的 verified canonical Artifact；册级表不以未登记前言卡、教师用书或外部解析新增 KP。

## 3. 册级结构、人文/语言双线与任务覆盖

- 前言只承担选择性必修下册范围、四单元和独立 REC 栏目定位；不把目录篇名直接升格为册级原子知识点。
- 人文主题 4 条覆盖古典传统主体处境、现代社会普通人/乡土共同体、自然/历史/公共知识和证据化阅读责任；每条均回到 accepted 图谱节点或 REC 完整稳定 KP-ID，并保留文体、历史和学科语境差异。
- 语言主题 5 条覆盖古典诗歌体式/意象/典故/诵读、现代文学多文体、文言散文、科学论著/科学史和共同证据化表达程序；REC 的 KP 引用已在 v0.2.1 统一为完整 `KP-CARD-X3-REC-01-*`，不再使用裸缩写。
- 稳定任务 ID 为 `TASK-BOOK-X3-01`—`04`，分别索引 U01—U04 单元任务；REC 没有独立任务包，表中仅把诵读、比较和短评作为项目补充程序，并明确不能把 U01 任务移写为 REC 专属教材要求。
- 课标定位覆盖任务群5、8、10、12；学业质量4-3只作能力定位，不宣称学生或册表达到完整水平。教师用书均保持 `edition_match=unknown`，未消费未登记意见。

## 4. 跨单元递进、高考 M0 与边界

册级 `REL-BOOK-X3-001`—`005` 均明确登记为 `N/A`，并写出 `na_reason`：当前没有册级源单元 KP—目标单元 KP 的双方 accepted 逐边证据，因此不把单元顺序、任务群相似性或“证据链/比较/修订”工作流冒充确定递进。REC 与 U01 也仅保留并列索引，未臆造先后或前提关系。该保守处理与全库 N/A 治理一致。

高考表对 U01—U04 与 REC 统一采用 `N/A | M0 | N/A`，明确尚未登记真题题文—答案/评分—教材 KP 的逐小问双向闭合证据；不把诗歌、人物/环境、文言、科学说明或比较题型相似性升级为 M1—M3。高考与跨单元关系均保留可复核解锁条件。

问题清单中的 18 张卡旧说法、未登记前言知识卡、教师用书 unknown、高考双向证据缺口和跨单元证据缺口均显式标为 open/治理边界；它们没有被写成当前正式结论，也不构成当前上游状态或哈希断链。

## 5. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 册名、四单元、REC、15卡、任务群和主题入口均可回到当前 accepted 上游或已验证 canonical Artifact；未见关键事实错误。 |
| R02 | 否 | 册级主张、覆盖恒等式、主题/语言入口、任务和 N/A/M0 边界均有适配上游节点、KP、EV 或任务入口；REC 稳定 KP-ID 已修复。 |
| R03 | 否 | 4图谱、15卡、前言/范围、双线、4任务、5册级 REL、M0/N/A、教师用书和 Issue 模块齐全。 |
| R04 | 否 | 上游教材事实、课标定位、册级综合、项目程序、缺源声明和外部材料边界分层；没有把项目工作流冒充教材新增事实。 |
| R05 | 否 | 册表不新增原子 KP；287 个唯一 KP 通过 accepted 图谱/卡索引，主层级和 EV 由上游交付物承担。 |
| R06 | 否 | 高考严格保持结构化 M0，不引用未登记真题、答案或评分材料。 |
| R07 | 否 | 19 个直接上游均为 ledger `accepted`，版本、路径和实际文件 SHA 与 BOOK 表一致。 |
| R08 | 否 | BOOK front/ledger 均 v0.2.1/`linted`；19 个上游 ID、SHA、状态、287 去重口径和稳定主题/任务/REL ID 闭合。 |
| R09 | 否 | 使用现行课标任务群规范名称，未改写任务群或把册级主题当固定课型。 |
| R10 | 否 | 人文/语言双线按单元文本和任务展开，未机械铺满核心素养，4-3未被当作册级难度或达成标签。 |

## 6. 缺陷分级

| 等级 | 数量 | 独立结论 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 当前无上游未验收、版本/SHA 漂移、重复计数、非法关系或 M0 越级。 |
| P2 | 0 | v0.2.1 已关闭 REC 裸 KP 可检索性问题；当前未发现新的非阻断缺陷。 |

## 7. `2.0-textbook` book_summary 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25 | 23 | **25.0** | 4/4 accepted 图谱、15/15 accepted 卡、REC、前言范围和仅消费 accepted 上游规则均闭合。 |
| 跨单元递进 | 20 | 17 | **18.0** | 五条册级 REL 均带 `N/A` 和具体 `na_reason`，不强造无证递进；保守治理达到门槛但无正向跨单元边。 |
| 分类、去重与稳定 ID | 15 | 13 | **15.0** | 19 项上游、287 唯一 KP、4 任务、5 REL、4 主题/5语言主题均有稳定 ID；图谱 KP 与底层卡明确不重复相加。 |
| 双线、任务群与课程定位 | 15 | 13 | **14.5** | 人文4条、语言5条、任务群5/8/10/12和4-3边界均有 accepted 入口；册级概括保留语境差异，留0.5审慎余量。 |
| 高考板块映射 | 10 | 8 | **10.0** | 全册统一 M0/N/A，双向证据缺口、解锁条件和禁止越级规则清楚。 |
| 上下游一致性 | 10 | 9 | **10.0** | BOOK v0.2.1 front/ledger 一致，19 个上游状态、版本、路径、SHA、计数和来源链逐项闭合。 |
| 检索性 | 5 | 4 | **4.5** | 上游清单、主题/语言/任务/REL、M0、Issue 和版本记录齐全；REC ID 修订后可直接检索，保留0.5余量。 |
| **合计** | **100** | **90** | **97.0** | **总分及七维单项均达到冻结门槛；R01—R10 全部未触发。** |

## 8. 独立第二复审决定

**决定：`pass`；总分 `97.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

`BOOK-X3` v0.2.1/SHA `d5e724f15f5e2bea5968337be52d8ebb01c6b9df02dea0ef9758cc4d5383bc6d` 通过本轮独立第二复审，可与同一 v0.2.1/SHA 的独立主审配对进入后续 G4。BOOK 当前仍为 `linted`，本报告不执行 `accepted` 状态迁移；册表、任一上游交付物、canonical Artifact、validator、rubric/taxonomy 或 ledger 绑定变化均使本报告失效并须按新快照复审。

## 9. 可复现绑定与报告校验

- BOOK：`work/knowledge/册级汇总/BOOK-X3.md`；v0.2.1；SHA `d5e724f15f5e2bea5968337be52d8ebb01c6b9df02dea0ef9758cc4d5383bc6d`。
- 单元图谱 SHA：U01 `ed8970bf151ccfea52676e0e25092484ce4a9c6bbc712757fd9de07398bf82b1`；U02 `262bc994b796d113be275d60386779ab74f588a5c7a77cc74ae7be26da9b38fb`；U03 `2b2394ca482abedb9a8d5139f2eed28aa4075d629deaaa95dd0655999d14b687`；U04 `0b9dd1e7040cac06b1d698f2613c1d0cee116803695c06d02d4a3f4d9676d903`。
- 15 张知识卡：BOOK §1.2 的 ID/版本/KP 数/SHA 与 ledger 及实际文件逐项一致；其中 REC post-G4 SHA 为 `c5b8f314825d5643b6c7227c099ee88c8432b86e3ffdd9a8cde24cf876db6c0d`。
- ledger：`work/knowledge/_meta/deliverables.jsonl` SHA `15c7fd318be972203beb258166492be6e19971b8fe71a940a449981e3563cf7a`；BOOK 当前状态 `linted`，19 个直接上游均 `accepted`。
- validator：`work/knowledge/_meta/validation_reports/x3_book_final_pre_review_v021_current_20260809.json`；run `VAL-20260809-024951+0800`；SHA `2c7fbf03d09cece3b648ebea61cd236afb9e8e4d8d454666749b5463db788e30`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-MASTER-X3-PDF` SHA `16a6d823c56a4842a53cb69839d216971a210892d47b3d16877349174d0abc67`；`ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。

复算分母：4 个 accepted 单元图谱、15 张 accepted 知识卡（14 张正文卡+1 张 REC）、271 个图谱 KP、16 个 REC KP、287 个唯一 KP、4 条册级任务、5 条 N/A 递进 REL、全册 1 行 M0。
