---
schema_version: "2.0-candidate"
review_id: "REV-BOOK-X2-SECONDARY-FINAL"
deliverable_id: "BOOK-X2"
artifact_version: "0.2.0"
artifact_sha256: "7f80ad15071213da908856e5ea7b38eaa6bff4bdb219d8040e03b93b92212600"
review_round: 1
reviewer: "independent_secondary_book_x2_final"
review_role: "secondary"
reviewed_at: "2026-08-08T20:50:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-203544+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "bfff60376e4a2f1451a7e9fc16692c6eb98224d9a1738c617664d3bd23c13add"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-203544+0800.json"
validator_archive_report_sha256: "bfff60376e4a2f1451a7e9fc16692c6eb98224d9a1738c617664d3bd23c13add"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "b4f55d67a932224810b6722280ca7cee4b38e828049e515d14c9b53364d83f2e"
validator_result: "passed"
decision: "pass"
---

# BOOK-X2 v0.2.0 独立第二复审

## 1. 输入锁定与独立性

本轮只依据最终快照中的当前册级汇总、账本、四张 `accepted` 单元图谱、一张 `accepted` 古诗词诵读卡、各上游当前文件、冻结 `2.0-textbook` rubric/taxonomy 和 validator 机械报告独立判断；未读取或复用其他评审报告、分数或缺陷结论，不修改 BOOK、上游交付物、ledger 或状态迁移。

| 对象 | 当前绑定 |
|---|---|
| 册级汇总 | `work/knowledge/册级汇总/BOOK-X2.md`；v0.2.0；SHA `7f80ad15071213da908856e5ea7b38eaa6bff4bdb219d8040e03b93b92212600`；状态 `linted` |
| 单元图谱 | `UNIT-X2-U01` v0.2.0 SHA `6a9e4c92e8f442df18b8e698261e814b5010932c08ebb997a606615336a3dc68`；`UNIT-X2-U02` v0.2.2 SHA `99239de9a8a599ed7bd57f366caa6d2068541dcbaafda04090a652ba24bc8d49`；`UNIT-X2-U03` v0.2.0 SHA `da4924dc06fdd3b5c62490f7ac3583c941d22254baed26ad20ac94af04373ca9`；`UNIT-X2-U04` v0.2.0 SHA `d5ebda1d5d874bfc71da3e97987f61fb4a06f30ab4958758c243b59627c39a22` |
| 诵读卡 | `CARD-X2-REC-01` v0.2.0 SHA `7b6aaf24bd5b5ea660c2e467b9963f58f205fa1677d734fff5270688ed500a48` |
| ledger | `work/knowledge/_meta/deliverables.jsonl` SHA `b4f55d67a932224810b6722280ca7cee4b38e828049e515d14c9b53364d83f2e`；五个上游条目均为 `accepted` |
| validator | `VAL-20260808-203544+0800`；`passed`；0 errors；`hash_verification=true` |

## 2. 册级覆盖统计独立复算

| 覆盖口径 | 独立复算 | 结论 |
|---|---:|---|
| accepted 单元图谱 | 4/4 | U01—U04 ledger 状态均为 `accepted`，版本与 BOOK §1.1 SHA 一致。 |
| accepted 诵读卡 | 1/1 | REC 卡状态为 `accepted`，post-G4 SHA 与 BOOK §1.1 一致。 |
| 单元底层卡 | 13 | U01 5、U02 3、U03 3、U04 2；均来自 accepted 图谱。 |
| 诵读卡 | 1 | `CARD-X2-REC-01` 独立计入，不重复进入四个单元图谱。 |
| accepted 卡合计 | 14 | 13 张单元底层卡 + 1 张 REC 卡。 |
| 单元正文子文本 | 22 | U01 7、U02 6、U03 4、U04 5；不含 REC。 |
| 诵读子文本 | 4 | REC 四篇单独统计。 |
| 文本入口合计 | 26 | 22 单元正文 + 4 诵读，口径透明且不重复。 |
| 单元图谱 KP | 183 | 59 + 46 + 47 + 31；图谱 KP 与底层卡是同一批，不二次相加。 |
| REC KP | 17 | 独立栏目知识点。 |
| 全册去重 KP | 200 | 183 + 17；BOOK 未将图谱 KP 与底层卡 KP 再相加为 383。 |

各上游当前文件哈希与 BOOK §1.1/§1.2 逐项一致；14 张卡的题名、版本、KP 数和 post-merge SHA 均可回查，未见漏卡、重卡或旧 SHA 残留。

## 3. 上游状态、来源边界与课程主线

- BOOK 仅消费账本中当前 `accepted` 的四张单元图谱和一张 REC 卡；不存在消费 `linted`/`drafted` 上游的路径。BOOK 自身仍为 `linted`，不会因上游已接受而自动变为 `accepted`。
- 课程范围由 `ART-MASTER-X2-PDF`、前言/目录包和各 canonical 任务包锁定；学生教材、课标、任务成果、项目建议和外部资料分层记录，教师用书为 `edition_match=unknown` 且引用 0/0。
- 册级人文主线将 U01 思辨/实践/正义、U02 革命记忆、U03 历史现场、U04 主体/自由/文化多样性和 REC 战争/声音/惘然/报国串为检索线，同时明确不抹平文体与文化语境。
- 册级语言主线“材料定位—形式识别—证据化解释—受众表达—修订”可回链各图谱节点、任务和 KP；它是综合索引，不新增 KP 或教材原文。

## 4. 六条跨单元关系双端证据复核

| REL-ID | 独立核对结果 |
|---|---|
| `REL-BOOK-X2-001` | 源 `CAND-L-X2-U01-006` 与目标 `CAND-L-X2-U02-006` 均存在于 accepted 图谱；U01 EV-002—009/任务01-02/05 与 U02 三卡 EV/任务02—04可回查，支撑“理性表达→人物分析”的迁移，未混换文体语境。 |
| `REL-BOOK-X2-002` | 源 `CAND-H-X2-U02-005`、目标 `CAND-H-X2-U03-001` 均存在；U02 卡/任务证据与 U03 卡01/03 EV-001/002/013/012/016均可解析，支持“证据化记忆→历史现场”的深化，史实/作者判断/学生质疑边界明确。 |
| `REL-BOOK-X2-003` | 源 `CAND-L-X2-U03-001`、目标 `CAND-L-X2-U04-001` 均存在；U03 EV-013/014/012/013 与 U04 EV-004/006/011/012/014均存在，形式比较理由与戏剧/史传边界闭合。 |
| `REL-BOOK-X2-004` | 源 `CAND-H-X2-U04-003`、目标 REC 卡四篇意象入口均有稳定来源；U04 EV-002—015/020—023 与 REC EV-002—010均存在，明确共享“形式—情感”动作但不将跨文化诗歌同质化。 |
| `REL-BOOK-X2-005` | 源 `CAND-L-X2-U02-004`、目标 `CAND-L-X2-U04-004` 均存在；U04 EV-001/015、EV-014—018和任务05精确可回查。源侧采用“U02 三卡正文 EV”压缩写法，需回到 U02 节点表展开，但对应三卡均为 accepted，未形成断链；因此仅在可检索性/关系综合维度保守扣分。 |
| `REL-BOOK-X2-006` | 源 `CAND-H-X2-U01-003`、目标 REC《燕歌行并序》《书愤》入口均有稳定来源；U01 卡04/05 EV 与 REC EV-002—004/009—010均存在，比较的是语境化价值判断，不把哲学论证等同诗歌抒情。 |

六条关系的源/目标节点、受控关系类型和双端证据均可回查；其中 REL-BOOK-X2-005 的源证据是有意压缩而非缺失。未登记仅由单元排列产生的虚假线性递进，跨册前后关系按 `N/A (no_reliable_relation)` 处理。

## 5. 高考 M0、纵向 N/A 与外部边界

- 高考四板块（现代文/实用性阅读、古诗文阅读、语言文字运用、写作与表达）均保持 `M0`；没有消费 `Data/reference/gaokao`、四川真题或答案/评分资料，也没有将教材任务或题型相似性升格为 M1—M3。
- M0 的含义明确为“当前尚未完成题文—答案/评分—教材 KP/EV 双向映射”，不表示“不考”；待 `TEXTBOOK-LOCK`/G-TB 后按具体小问重新核验。
- 跨册前后递进没有双方 accepted 且逐边可核验的目标，统一为有理由的 `N/A`；六条册内关系不被误写成跨册能力等级。
- 未登记教师用书、网络解析、外部历史资料、学生改写/申论成果均不进入册级正式 KP/证据统计。

## 6. R01—R10 与 P0/P1/P2

| 代码 | 触发 | 独立结论 |
|---|---|---|
| R01 | 否 | 上游 14 张卡、4 图谱、REC 四篇和册级范围/题名/版本可回到当前文件与 canonical 注册。 |
| R02 | 否 | 200 个去重 KP、26 个文本入口、6 条 REL 的源/目标和双端证据均可回查；REL-005 的压缩证据可展开，无实质无证断言。 |
| R03 | 否 | 4 图谱、1 REC、14 卡、22+4 子文本、课程主线、任务、关系、M0/N/A、教师用书和 Issue 模块齐全。 |
| R04 | 否 | 册级综合、上游教材事实、课标、任务成果、项目建议、教师用书缺源和外部材料分层清楚。 |
| R05 | 否 | 册级人文/语言主线均以 accepted KP/EV/任务入口为索引，不新增未证 KP。 |
| R06 | 否 | 未登记真题不进入册级关系；四板块均为结构化 M0。 |
| R07 | 否 | 只消费 ledger 当前 `accepted` 上游，且 BOOK §1 的 14 卡/4 图谱/1 REC SHA 与工作区复算一致。 |
| R08 | 否 | BOOK、上游版本、路径、状态、来源和 SHA 链闭合；自身保持 linted，不提前写回 accepted。 |
| R09 | 否 | 课程定位、任务群和现行 2020 修订课标边界保持受控名称，未将册级主线当固定课型。 |
| R10 | 否 | 主线按各单元文本与任务需要展开，未机械铺满核心素养，也未把学业质量当册级等级。 |

P0/P1/P2：`0/0/0`。

## 7. 2.0-textbook book_summary 量规评分

| 维度 | 权重 | 门槛 | 得分 | 独立依据 |
|---|---:|---:|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25 | 23 | **25.0** | 4/4 图谱、1/1 REC、14 张 accepted 卡、22+4 子文本、200 去重 KP 和前言/目录/后记边界均闭合。 |
| 跨单元递进 | 20 | 17 | **18.5** | 6 条册内关系均有源/目标和双端证据；REL-005 源证据采用可展开的三卡 EV 压缩写法，保守扣 1.5。 |
| 分类、去重与稳定 ID | 15 | 13 | **15.0** | 13 单元卡/1 REC 卡、22 正文+4 诵读子文本、200 KP 的口径和稳定 ID 清楚，未把图谱 KP 与底层卡重复相加。 |
| 双线、任务群与课程定位 | 15 | 13 | **15.0** | 五单元人文/语言主线、各自任务群和课标来源均有 accepted 上游入口，保留文体/文化差异。 |
| 高考板块映射 | 10 | 8 | **10.0** | 现代文、古诗文、语言运用、写作四板块均严格 M0，未消费未登记试卷或答案评分证据。 |
| 上下游一致性 | 10 | 9 | **9.5** | 14 张卡/4 图谱/1 REC 的状态、版本、当前 SHA、来源路径与 ledger 一致；BOOK 自身状态边界清楚，保守扣 0.5。 |
| 检索性 | 5 | 4 | **4.5** | 覆盖索引、主线、6 条 REL、M0、Issue 和问题清单齐全；REL-005 的压缩证据需要回看 U02 节点表，扣 0.5。 |
| **合计** | **100** | **90** | **97.5** | 总分及各维度均达到冻结门槛。 |

## 8. 独立第二复审决定

**决定：`pass`。** 当前 `BOOK-X2` v0.2.0/SHA `7f80ad15071213da908856e5ea7b38eaa6bff4bdb219d8040e03b93b92212600` 可与同一最终 SHA 的独立主审配对进入 G4。BOOK 在 G4 写回前仍不得标记为 `accepted` 或供更高层汇总消费；册级正文、任一上游交付物、validator 或 ledger 绑定变化均使本报告失效并需重新复审。

## 9. 可复现绑定

- BOOK：`work/knowledge/册级汇总/BOOK-X2.md`；v0.2.0；SHA `7f80ad15071213da908856e5ea7b38eaa6bff4bdb219d8040e03b93b92212600`。
- 上游：`UNIT-X2-U01` `6a9e4c92e8f442df18b8e698261e814b5010932c08ebb997a606615336a3dc68`；`UNIT-X2-U02` `99239de9a8a599ed7bd57f366caa6d2068541dcbaafda04090a652ba24bc8d49`；`UNIT-X2-U03` `da4924dc06fdd3b5c62490f7ac3583c941d22254baed26ad20ac94af04373ca9`；`UNIT-X2-U04` `d5ebda1d5d874bfc71da3e97987f61fb4a06f30ab4958758c243b59627c39a22`；`CARD-X2-REC-01` `7b6aaf24bd5b5ea660c2e467b9963f58f205fa1677d734fff5270688ed500a48`。
- validator：`VAL-20260808-203544+0800`；latest `work/knowledge/_meta/validation_reports/latest.json` SHA `bfff60376e4a2f1451a7e9fc16692c6eb98224d9a1738c617664d3bd23c13add`；归档运行报告 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-203544+0800.json` SHA 同为 `bfff60376e4a2f1451a7e9fc16692c6eb98224d9a1738c617664d3bd23c13add`；passed，0 errors，`hash_verification=true`。
- ledger：`work/knowledge/_meta/deliverables.jsonl` SHA `b4f55d67a932224810b6722280ca7cee4b38e828049e515d14c9b53364d83f2e`；BOOK 当前状态仍为 `linted`，本报告不执行状态迁移。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。

复算分母：4 个 accepted 单元图谱、1 张 accepted 诵读卡、14 张 accepted 卡、22 个单元正文子文本、4 个诵读子文本、200 个去重 KP、6 条册内 REL、4 行高考 M0、跨册关系 N/A。
