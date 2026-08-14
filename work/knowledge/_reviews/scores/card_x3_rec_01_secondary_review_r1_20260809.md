---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-REC-01-SECONDARY-R1"
deliverable_id: "CARD-X3-REC-01"
artifact_version: "0.2.1"
artifact_sha256: "f86202970a981614fdf7e1d50f7d7e6062c5d9c890e268fac2481d0946ac0d41"
review_round: 1
reviewer: "independent_secondary_card_x3_rec_01_r1"
review_role: "secondary"
reviewed_at: "2026-08-09T02:45:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "234e9cfa97635ed49556fdd1796b7ac43d7695eb8d8cccef6d4670171f147760"
validator_run_id: "VAL-20260809-023805+0800"
validator_report: "work/knowledge/_meta/validation_reports/x3_rec_01_final_pre_review_v021_20260809.json"
validator_report_sha256: "2b04e39e134d7862a4bbb902732dd5eb613477b3d2d71cbbd1a53b27ffc29b9b"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "e5095b9199228dae199caf97b188602f1928cf31cc51e6fe5680a8197e642ca3"
---

# CARD-X3-REC-01 v0.2.1 独立第二复审 R1

## 1. 输入锁定与独立性

本轮从 v0.2.1 修订快照重新独立复核，不复用 v0.2.0 的分数、R/P 判定或结论。依据为当前卡片、已登记 canonical Artifact、现行课标、冻结 `2.0-textbook` rubric/taxonomy、共享 ledger 和指定 validator 机械报告；不修改卡片、ledger、validator 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-REC-01.md`；v0.2.1；SHA `f86202970a981614fdf7e1d50f7d7e6062c5d9c890e268fac2481d0946ac0d41`；状态 `linted` |
| 学生教材 | `SRC-PKG-X3-019` / `ART-PKG-X3-019-PDF`；4页；SHA `159ca50e62542f7d73a77e4de4f9c4551a92ca55ce546f66a7f2f8da07eebd44`；母本物理页116—119，切分页1—4 |
| 现行课标 | `SRC-CURR-2020` / `ART-CURR-2020-PDF`；66页；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `234e9cfa97635ed49556fdd1796b7ac43d7695eb8d8cccef6d4670171f147760`；卡片 v0.2.1/`linted` |
| validator | `VAL-20260809-023805+0800`；报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `2b04e39e134d7862a4bbb902732dd5eb613477b3d2d71cbbd1a53b27ffc29b9b` |

独立计数为 4/4 正文子文本、16/16 KP、15/15 EV；EV 类型为 Q=9、M=2、D=4。高考保持结构化 `M0`，纵向关系保持有理由的 `N/A`，教师用书 `edition_match=unknown`。

## 2. 四篇正文与材料边界复核

- `SUBTEXT-CARD-X3-REC-01-01`《拟行路难（其四）》：母本物理页116、切分页1（印刷页111）；正文、注释和页后教材提示均在范围内。
- `SUBTEXT-CARD-X3-REC-01-02`《客至》：母本物理页117、切分页2（印刷页112）；正文、待客细节和页后教材提示均可定位。
- `SUBTEXT-CARD-X3-REC-01-03`《登快阁》：母本物理页118、切分页3（印刷页113）；正文、典故注释和页后教材提示均可定位。
- `SUBTEXT-CARD-X3-REC-01-04`《临安春雨初霁》：母本物理页119、切分页4（印刷页114）；正文、背景/注释和页后教材提示均可定位。
- 《古诗词诵读》是选择性必修下册第四单元之后的独立栏目，卡片 v0.2.1 已将旧的 `U03` 归属表述修正为“选择性必修下册独立的《古诗词诵读》栏目”；与 `unit=REC`、包序列19及 canonical PDF 一致。

正式范围只消费上述四篇正文、正文注释及各篇正文后教材提示；后记、空白页、网络赏析、未登记教师用书和外部拓展不进入正式证据。MinerU `full.md` 只作定位辅助，正式引文回到 canonical PDF。

## 3. 证据链、课标和知识点核查

- 15/15 EV 均有受控单值类型、Source/Artifact、canonical 物理页与切分页 locator、短引、`supports` 关系和 `verified` 元数据。Q 证据逐篇覆盖正文/注释/教材提示；M 证据分别回链任务群8物理页29—30与学业质量4-3物理页46；D 证据用于范围、未登记任务包、教师用书和 MinerU/回链治理边界。
- 四篇文本特异知识均有对应正文和教材提示：泻水起兴与门第压抑、客至的生活细节和结构照应、登快阁的自嘲/知音/归隐与律诗格律、临安春雨的闲适表层和等待落寞/首尾照应。跨篇比较明确为项目综合解释，不写成作品唯一答案。
- 16/16 KP 均有唯一 ID、主维度（人文/语言）、受控知识类型、四层主归属、判定理由、证据回链和置信状态。文本解释型 KP 的证据至少由正文与提示两条 Q 证据互证；程序/边界 KP 明确标为项目程序或来源治理约束。
- 课标任务群8引文覆盖“选择不同时期、不同类型代表性作品精读”“重视诵读”“撰写评论”等原文；4-3仅作为“结合作品具体内容阐释并比较文学作品”的能力定位，卡片没有据此宣称达到完整学业质量水平。

## 4. 教学、纵向和高考边界

- 教材实际提示、教师用书缺源和本项目教学建议分层记录；未登记同版教师用书，`edition_match=unknown`，没有把项目建议冒充教材硬性任务。
- 纵向表使用带理由的 `N/A`：当前没有双方 accepted 且逐边证据闭合的跨课/跨册 KP 关系，不以一般意象、诵读或写景相似性强造递进边。
- 高考表使用 `N/A | M0 | N/A`，并说明尚未登记真题题文—答案/评分—教材 KP 的逐小问双向闭合证据；不把诗歌意象、典故、情感或结构题型相似性升级为 M1—M3。

## 5. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 四篇题名、作者、正文、注释、教材提示、独立 REC 栏目归属和页位均与 canonical 载体一致；v0.2.1 已修正旧 U03 归属误标。 |
| R02 | 否 | 15/15 EV 均有适配 Source/Artifact、可解析 locator、短引和 verified 元数据；解释型主张由对应正文/提示 Q 证据支撑。 |
| R03 | 否 | 四篇子文本、基本信息、双维度、课标、KP、纵向、高考、教学提示、证据表和自检/版本记录齐全。 |
| R04 | 否 | 正文事实、教材提示、课标 M、项目解释、D 边界和教师用书缺源严格分层；MinerU 不作为规范引文。 |
| R05 | 否 | 16/16 KP 均具主维度、受控类型、四层归属、判定理由、有效 EV 与置信状态。 |
| R06 | 否 | 高考严格保持结构化 M0；没有未登记真题、答案/评分资料或越级映射。 |
| R07 | 否 | 仅消费已登记且哈希匹配的学生教材和现行课标；MinerU 只作辅助。 |
| R08 | 否 | 卡片、ledger、validator 的 v0.2.1/SHA 绑定一致，ID/数量/版本/链接闭合。 |
| R09 | 否 | 使用现行课标“中华传统文化经典研习”等规范名称，未把任务群改写为固定课型/教法。 |
| R10 | 否 | 人文/语言双线按四篇文本和诵读任务需要展开；学业质量4-3只作能力定位，不作为单卡难度或达成标签。 |

## 6. 缺陷分级

| 等级 | 数量 | 独立结论 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | v0.2.1 已关闭独立 REC 栏目误标；无关键证据、版本、范围或状态阻断问题。 |
| P2 | 0 | 当前未发现新的非阻断事实、定位、粒度或边界缺陷。 |

## 7. `2.0-textbook` knowledge_card 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **24.5** | 15/15 EV 的类型、来源、Artifact、canonical 页位/切分页、短引和 verified 元数据闭合；D 边界证据与 MinerU 辅助链保留审慎扣分。 |
| 事实与术语准确性 | 20 | 18 | **20.0** | 四篇题名、作者、文体、正文意象、教材提示、REC 独立栏目归属、课标术语和 QD 边界均准确。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 4 子文本、16 个文本特异/程序 KP、15 EV、课标/M0/N/A/教师用书边界、版本记录和自检模块完整。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线保留门第压抑、贫家真率、官事自嘲/归隐和京华落寞；语言线覆盖起兴、章法、典故、格律、照应和诵读程序。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 16/16 KP 层级、理由和置信状态完整；高考严格 M0，课标质量描述不越级。 |
| 纵向贯通 | 8 | 6 | **8.0** | 缺少双方 accepted 且逐边核验的目标时保持有理由 N/A，不强造递进。 |
| 教学可用性与表达 | 7 | 5 | **6.5** | 四篇的准确诵读—注释核对—意象/结构标注—原句解释—跨篇比较流程可执行；教材提示、项目建议、教师用书缺源和独立 REC 边界清楚。 |
| **合计** | **100** | **85** | **98.5** | **总分及七维单项均达到冻结门槛；R01—R10 全部未触发。** |

## 8. 独立第二复审决定

**决定：`pass`；总分 `98.5/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

`CARD-X3-REC-01` v0.2.1/SHA `f86202970a981614fdf7e1d50f7d7e6062c5d9c890e268fac2481d0946ac0d41` 通过本轮独立第二复审，可与同一 v0.2.1/SHA 的独立主审配对进入后续 G4。当前卡片仍为 `linted`，本报告不执行 `accepted` 状态迁移；卡片、canonical Artifact、课标、validator、rubric/taxonomy 或 ledger 绑定变化均使本报告失效并须按新快照复审。

## 9. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-REC-01.md`；v0.2.1；SHA `f86202970a981614fdf7e1d50f7d7e6062c5d9c890e268fac2481d0946ac0d41`。
- 学生教材 Artifact：`ART-PKG-X3-019-PDF` SHA `159ca50e62542f7d73a77e4de4f9c4551a92ca55ce546f66a7f2f8da07eebd44`；课标 Artifact：`ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- ledger：`work/knowledge/_meta/deliverables.jsonl` SHA `234e9cfa97635ed49556fdd1796b7ac43d7695eb8d8cccef6d4670171f147760`；当前卡片状态仍为 `linted`。
- validator：`work/knowledge/_meta/validation_reports/x3_rec_01_final_pre_review_v021_20260809.json`；run `VAL-20260809-023805+0800`；SHA `2b04e39e134d7862a4bbb902732dd5eb613477b3d2d71cbbd1a53b27ffc29b9b`；`passed`、0 errors、`hash_verification=true`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。

复算分母：4 个正文子文本、16 KP、15 EV（Q=9、M=2、D=4）、高考 1 行结构化 M0、纵向 1 行 N/A。
