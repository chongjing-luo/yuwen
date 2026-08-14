---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-REC-01-R2-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-REC-01"
artifact_version: "0.2.1"
artifact_sha256: "f86202970a981614fdf7e1d50f7d7e6062c5d9c890e268fac2481d0946ac0d41"
review_round: 2
reviewer: "independent_primary_card_x3_rec_01_r2"
review_role: "primary"
reviewed_at: "2026-08-09T02:42:00+08:00"
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
report_sha256: "6f8eec02fa069d1c403f56a074553f654097240e46e712f637f271b193d23e28"
---

# CARD-X3-REC-01 v0.2.1 独立主审 R2

## 1. 输入锁定与状态一致性

本轮从当前快照重新独立复核《古诗词诵读》卡片，不复用 v0.2.0 结论，不修改卡片、ledger、validator 或状态迁移。采用冻结的 `2.0-textbook` 知识卡量表：总分门槛 85，七维最低分 `21/18/12/12/8/6/5`。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-REC-01.md`；v0.2.1；SHA `f86202970a981614fdf7e1d50f7d7e6062c5d9c890e268fac2481d0946ac0d41`；状态 `linted` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`；SHA `234e9cfa97635ed49556fdd1796b7ac43d7695eb8d8cccef6d4670171f147760`；CARD-X3-REC-01 为 v0.2.1/`linted`、`REWORK`，无上游卡依赖 |
| canonical 教材包 | `ART-PKG-X3-019-PDF`；SHA `159ca50e62542f7d73a77e4de4f9c4551a92ca55ce546f66a7f2f8da07eebd44`；母本物理页116—119、切分页1—4 |
| MinerU 辅助产物 | `ART-PKG-X3-019-MINERU-FULLMD`；SHA `48aad24f8a2168c24348ea69a385d5dc555216c6b1f367b3cf0b2b654bca26f2`；仅作提取/定位辅助，不替代 canonical PDF |
| 现行课标 | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群8物理页29—30、学业质量4-3物理页46 |
| validator | `VAL-20260809-023805+0800`；`work/knowledge/_meta/validation_reports/x3_rec_01_final_pre_review_v021_20260809.json`；SHA `2b04e39e134d7862a4bbb902732dd5eb613477b3d2d71cbbd1a53b27ffc29b9b`；`passed`、0 errors、`hash_verification=true` |

卡片当前明确属于选择性必修下册的独立“古诗词诵读”栏目，不再误标为 U03 正文单元；front matter、ledger 的 `unit: REC` 和状态记录一致。正式来源仅为 `SRC-PKG-X3-019` 与 `SRC-CURR-2020`；未登记教师用书、外部赏析、真题或其他版本材料不进入正式证据。

## 2. 覆盖、证据与边界复核

- 卡片覆盖四个教材子文本：鲍照《拟行路难（其四）》、杜甫《客至》、黄庭坚《登快阁》和陆游《临安春雨初霁》，分别定位到 canonical 物理页116—119/切分页1—4；作者、文体和作品范围均有来源登记与正文/题注证据。
- `16/16` KP 均有稳定 ID、合法主维度（仅“人文/语言”）、冻结知识类型、四层主归属、判定理由、证据 ID 和置信状态；`15/15` EV 均为单值 `Q/F/M/D`，且 Source、Artifact、locator、短引和 `verified` 元数据闭合。
- 四篇正文、正文注释和各篇正文后的教材实际提示属于正式范围；后记、空白页、网络赏析和未登记教师用书被明确排除。MinerU `full.md` 仅作提取辅助，正式引文回到 canonical PDF。
- 卡片没有独立 REC 任务包；诵读、跨篇比较、朗诵或短评修订在 §8.3 明确标为项目建议，不冒充教材硬性任务。课标任务群8和学业质量4-3只作课程/能力定位，不判定学生已达成水平。

## 3. Claim—Evidence 与双维度复核

四篇作品分别闭合独立文本证据：`EV-002—004`支持《拟行路难（其四）》的泻水起兴、门第命运和举酒/吞声心态；`EV-005—006`支持《客至》的待客细节、铺垫照应与生活情趣；`EV-007—008`支持《登快阁》的公事自嘲、典故、格律与白鸥归隐志；`EV-009—010`支持《临安春雨初霁》的京华等待、闲适细节、郁闷暗线和首尾照应。跨篇 KP-012/013 明确把比较和诵读程序限制为“形式—情感—判断”证据链，不提供唯一鉴赏答案。

人文维度覆盖门第压抑、贫家待客、官事自嘲/归隐和京华闲居落寞；语言维度覆盖托物寓意、章法照应、律诗格律/典故、细节含蓄和诵读梳理程序。课标 EV-012/013 与边界 EV-011/014/015 分层清楚，教师用书保持 `edition_match=unknown`。

## 4. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 四篇题名、作者、正文事实、注释、教材提示、独立诵读栏目归属和课标术语均可回到 canonical 载体；未发现关键事实错误或张冠李戴。 |
| R02 | 否 | `16/16` KP 的 Claim 均有适配 EV；`15/15` EV 均有 canonical Artifact、可解析 locator、短引和 `verified` 状态，跨篇解释有多篇证据。 |
| R03 | 否 | 四个子文本、注释/提示、16 KP、15 EV、双维度、教学模块、M0、纵向 N/A 和边界声明齐全。 |
| R04 | 否 | 正文、教材实际提示、课标定位、来源缺失声明和项目建议严格分层；未把 MinerU、网络赏析或教师用书意见冒充规范结论。 |
| R05 | 否 | 16/16 KP 均具备合法主维度、受控类型、四层归属、判定理由、有效证据和置信状态。 |
| R06 | 否 | 高考保持结构化 `M0/N/A`，未引用未登记真题、答案或评分资料，也未声称 M1—M3 直接衔接。 |
| R07 | 否 | 正式内容只消费已登记并验证的教材 canonical PDF、现行课标和边界声明；MinerU 明确为辅助产物。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、16 KP、15 EV、4 subtext、版本、路径和 SHA 一致；归属修正已在当前图谱与 ledger/validator 绑定中同步，哈希校验通过。 |
| R09 | 否 | 使用现行课标任务群8“中华传统文化经典研习”和物理页29—30，未改写任务群名称或把任务群当固定课型/教法。 |
| R10 | 否 | 人文/语言双线按四篇诵读文本和实际鉴赏程序展开，未机械铺满四项核心素养，也未把学业质量4-3当作题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误、状态破坏或不可恢复损坏。 |
| P1 | 0 | 独立栏目归属误标已修复；当前无关键证据缺失、非法维度/类型、未登记来源、教师用书混入、M0越级或版本漂移。 |
| P2 | 0 | 未发现影响检索和复核的非阻断缺陷；MinerU 辅助边界、独立任务包缺失和跨篇解释范围均已明确。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **24.5** | 15/15 EV 的来源、canonical Artifact、物理/切页、短引和验证状态闭合；MinerU 与正式证据职责分离，宽范围跨篇证据保守扣0.5。 |
| 事实与术语准确性 | 20 | 18 | **20.0** | 四篇题名、作者、正文事实、诗体/格律、独立诵读栏目归属、教材提示和任务群8术语准确，v0.2.0 归属问题已关闭。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 4 subtext、16/16 KP、15/15 EV、教学/课标/M0/纵向/边界模块齐全，KP粒度适合诵读卡。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 人文线和语言线均有四篇独立证据并有跨篇差异；跨篇综合保持开放解释边界，扣0.5。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 每个 KP 有四层主归属和理由；课标定位、M0 和不确定性边界完整。 |
| 纵向贯通 | 8 | 6 | **8.0** | 未具备双方 accepted 逐边证据时合法保持 N/A。 |
| 教学可用性与表达 | 7 | 5 | **7.0** | 教材提示、项目建议、教师用书缺失、MinerU 辅助和可执行诵读—比较程序分层清晰。 |
| **合计** | **100** | **85** | **99.0** | **总分及七维单项均达标；R01—R10 全部未触发。** |

## 7. 独立主审决定

**决定：`pass`；总分 `99.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/0`。**

当前 `CARD-X3-REC-01` v0.2.1/SHA `f86202970a981614fdf7e1d50f7d7e6062c5d9c890e268fac2481d0946ac0d41` 通过独立主审，可与同一 SHA 的独立第二复审配对进入后续流程。当前状态仍为 `linted`，本报告不执行状态迁移；卡片、ledger、validator、canonical Artifact、rubric/taxonomy 或版本绑定变化时，本报告失效并须按新 SHA 复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-REC-01.md`；v0.2.1；SHA `f86202970a981614fdf7e1d50f7d7e6062c5d9c890e268fac2481d0946ac0d41`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `234e9cfa97635ed49556fdd1796b7ac43d7695eb8d8cccef6d4670171f147760`；CARD-X3-REC-01 为 `linted`/`REWORK`。
- validator：`work/knowledge/_meta/validation_reports/x3_rec_01_final_pre_review_v021_20260809.json`；运行 ID `VAL-20260809-023805+0800`；SHA `2b04e39e134d7862a4bbb902732dd5eb613477b3d2d71cbbd1a53b27ffc29b9b`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-019-PDF`=`159ca50e62542f7d73a77e4de4f9c4551a92ca55ce546f66a7f2f8da07eebd44`；`ART-PKG-X3-019-MINERU-FULLMD`=`48aad24f8a2168c24348ea69a385d5dc555216c6b1f367b3cf0b2b654bca26f2`（辅助）；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将该字段置空后，对 canonical 报告字节求 SHA-256，再回填所得值。
