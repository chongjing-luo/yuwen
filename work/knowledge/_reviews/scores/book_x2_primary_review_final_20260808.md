---
schema_version: "2.0-textbook"
review_id: "REV-BOOK-X2-FINAL-PRIMARY"
deliverable_id: "BOOK-X2"
artifact_version: "0.2.0"
artifact_sha256: "7f80ad15071213da908856e5ea7b38eaa6bff4bdb219d8040e03b93b92212600"
review_round: 1
reviewer: "independent_primary_book_x2_final"
review_role: "primary"
reviewed_at: "2026-08-08T20:45:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "b4f55d67a932224810b6722280ca7cee4b38e828049e515d14c9b53364d83f2e"
validator_run_id: "VAL-20260808-203544+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "bfff60376e4a2f1451a7e9fc16692c6eb98224d9a1738c617664d3bd23c13add"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-203544+0800.json"
validator_archive_report_sha256: "bfff60376e4a2f1451a7e9fc16692c6eb98224d9a1738c617664d3bd23c13add"
validator_result: "passed"
decision: "pass"
---

# BOOK-X2 v0.2.0 独立主审

## 1. 锁定对象、独立性与量表

本轮只审当前册级总表 `BOOK-X2`，不修改总表正文、账本、上游交付物或 validator 报告，不复用旧版本 SHA、分数或结论。采用冻结 `2.0-textbook` 册级量表：总分门槛 90，七维门槛为 `23/17/13/13/8/9/4`。

| 对象 | 当前绑定 |
|---|---|
| 总表 | `work/knowledge/册级汇总/BOOK-X2.md`；v0.2.0；SHA `7f80ad15071213da908856e5ea7b38eaa6bff4bdb219d8040e03b93b92212600`；状态 `linted` |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `b4f55d67a932224810b6722280ca7cee4b38e828049e515d14c9b53364d83f2e`；BOOK-X2 条目为 v0.2.0 / `linted`，上游条目均为 `accepted` |
| validator | `VAL-20260808-203544+0800`；latest 与 archive 均 `passed`、0 errors、`hash_verification=true`；SHA `bfff60376e4a2f1451a7e9fc16692c6eb98224d9a1738c617664d3bd23c13add` |
| rubric/taxonomy | rubric `2.0-textbook` / SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b` |

## 2. 上游验收、哈希与覆盖审计

### 2.1 单元图谱和诵读卡

| 上游 | ledger 状态/版本 | BOOK 声明 SHA | 当前文件 SHA | 子文本 | KP | 复核 |
|---|---|---|---|---:|---:|---|
| `UNIT-X2-U01` | accepted / 0.2.0 | `6a9e4c92e8f442df18b8e698261e814b5010932c08ebb997a606615336a3dc68` | 同左 | 7 | 59 | 一致 |
| `UNIT-X2-U02` | accepted / 0.2.2 | `99239de9a8a599ed7bd57f366caa6d2068541dcbaafda04090a652ba24bc8d49` | 同左 | 6 | 46 | 一致 |
| `UNIT-X2-U03` | accepted / 0.2.0 | `da4924dc06fdd3b5c62490f7ac3583c941d22254baed26ad20ac94af04373ca9` | 同左 | 4 | 47 | 一致 |
| `UNIT-X2-U04` | accepted / 0.2.0 | `d5ebda1d5d874bfc71da3e97987f61fb4a06f30ab4958758c243b59627c39a22` | 同左 | 5 | 31 | 一致 |
| `CARD-X2-REC-01` | accepted / 0.2.0 | `7b6aaf24bd5b5ea660c2e467b9963f58f205fa1677d734fff5270688ed500a48` | 同左 | 4 | 17 | 一致 |

账本逐条核验确认 `4/4` 单元图谱与 `1/1` 诵读卡均为 `accepted`，版本、路径、上游 ID 和正文 SHA 与 BOOK §1.1 一致。四个图谱提供 `22` 个单元正文子文本和 `183` 个 KP；诵读卡提供 `4` 个诵读子文本和 `17` 个 KP。两种文本入口明确分栏，合并口径为 `26`，去重后的全册底层交付物为 `14` 张 accepted 卡、`200` 个 KP（183+17，不把图谱索引再相加）。

### 2.2 底层卡、来源与 canonical Artifact

BOOK 的底层卡表列出 U01 5 张、U02 3 张、U03 3 张、U04 2 张和 REC 1 张，共 `14/14`；逐卡检查 ledger 状态均为 `accepted`，版本和表内 SHA 均与当前卡片文件一致。KP 计数复算为：U01 `59`、U02 `46`、U03 `47`、U04 `31`、REC `17`，合计 `200`。

BOOK front matter 的 `SRC-MASTER-X2`、`SRC-PKG-X2-000`—`019` 和 `SRC-CURR-2020` 共 22 个 source ID 均在 `sources.jsonl` 注册；其 canonical Artifact 均在 `artifacts.jsonl` 登记为 `is_canonical=true`、`authenticity_status=verified`。主教材、前言、四个单元任务、诵读包和课标的 SHA 与 BOOK §1.3 完全一致。主教材 source 的 `metadata_status=pending_enrichment` 只影响书目元数据丰富度，不影响其已验证 canonical Artifact 身份；本总表未以缺失书目信息生成正文事实。

前言/目录/后记仅承担册级范围和栏目边界；四个单元任务包和诵读卡作为相应任务/特殊内容入口；MinerU 衍生文本、网络赏析、未注册教师用书和外部拓展材料均未被冒充为 canonical 证据。

## 3. 册级主线、任务群与入口覆盖

- 人文主线覆盖 U01 的理论—实践—真/善/正义、U02 的革命记忆与制度/人民、U03 的历史现场与国家兴亡、U04 的主体/自由/文化多样性及 REC 的战争/声音/惘然/报国；每一行都回链 accepted 图谱/卡片的节点、KP 和 EV，并明确是册级综合而非教材唯一答案。
- 语言主线覆盖理论论证、纪念散文/报告文学/小说、史传史论与文言、戏剧/诗体/申论、古诗诵读的“材料定位—形式识别—解释链—受众表达—反馈修订”动作。各单元任务、课标任务群和项目建议分层，没有把综合索引写成新 KP。
- 4 个单元任务包和 REC 诵读入口均保留；册级表不将目录篇名直接升格为知识点。教师用书 `edition_match=unknown`，可得率 `0/5`、引用率 `0/0`，与上游卡边界一致。

## 4. 六条册级关系的独立 Claim—Evidence 复核

| REL-ID | 关系核验 | 证据闭合结论 |
|---|---|---|
| `REL-BOOK-X2-001` | U01 理性表达成果链迁移到 U02 证据化人物分析；双方保留理论论证与革命文学人物语境差异。 | U01 的实践/论证 EV 与 TASK-X2-U01-02/05、U02 三卡人物/形式/时代 EV 及 TASK-X2-U02-02/04 可由 accepted 图谱和卡片逐边回查。通过。 |
| `REL-BOOK-X2-002` | U02 革命文化的证据化记忆深化为 U03 回到历史现场；关系强调材料边界治理，而非把革命记忆改写为史学定论。 | U02 纪念/制度/人民证据与任务、U03 导语/史传/史论边界和任务 EV 均列于对应节点；双方均为 accepted 上游。通过。 |
| `REL-BOOK-X2-003` | U03 史传/史论形式比较到 U04 戏剧冲突阅读链；史传的时序剪裁/叙议与戏剧的对白/物件/动作被明确区分。 | U03 `EV-CARD-X2-U03-01-013/014`、`EV-CARD-X2-U03-03-012/013` 与 U04 `EV-CARD-X2-U04-01-004/006/011/012/014` 均能在 accepted 上游定位。通过。 |
| `REL-BOOK-X2-004` | U04 自我、自然与自由与 REC 四诗的意象—情感入口作跨文化比较；明确只共享“形式—情感”动作，不同质化诗歌语境。 | U04 诗歌 EV `002—015、020—023` 与 REC `002—010` 可回到 accepted 卡片；REC 以整卡为目标入口但给出具体诗篇 EV 范围，边界充分。通过。 |
| `REL-BOOK-X2-005` | U02 语言形式承载价值判断迁移为 U04 证据驱动表达/申论；迁移的是材料边界和证据协议，不是主题结论。 | U02 `CAND-L-X2-U02-004` 的三卡正文证据可沿其节点回链；U04 卡01/02 EV、TASK-X2-U04-05 和申论任务定位齐全。关系可复核，但 BOOK 采用“U02 三卡正文 EV”的紧凑写法，直接检索性略低。通过。 |
| `REL-BOOK-X2-006` | U01 真—善—正义的条件化判断与 REC《燕歌行并序》《书愤》的价值/历史处境作比较；明确不把哲学论证等同诗歌抒情。 | U01 卡04/05 EV 与 REC `EV-CARD-X2-REC-01-002—004、009—010` 均能定位，双方证据与语境边界清楚。通过。 |

六条关系均有唯一 `REL-BOOK-X2-*` ID、taxonomy 受控关系类型、源/目标、共性—差异或迁移说明和双端证据。REL-BOOK-X2-004 的目标使用 accepted 诵读卡作为跨文本入口，REL-BOOK-X2-005 的 U02 EV 采用紧凑索引；两者均可沿 accepted 上游节点展开，属于检索增强项而非证据断裂。

## 5. 高考、纵向、教师用书与不确定性治理

- 现代文/实用性阅读、古诗文阅读、语言文字运用、写作与表达四个板块均保持 `M0`。每行明确没有题文—答案/评分—教材 KP/EV 的双向闭合证据，不消费 `Data/reference/gaokao` 或四川真题，也不把题型相似性升级为 M1—M3。M0 表示尚未映射，不表示不会考。
- 前后册关系统一保持有理由的 `N/A (no_reliable_relation)`；不以教材排列顺序或“先理论后文学”制造线性递进。册内六条关系则均有双方 accepted KP/EV 入口。
- 同版教师用书未登记，U01—U04 与 REC 均为 `edition_match=unknown`；教师用书 `0/5` 可得、`0/0` 引用。外部历史资料、学生结局设想/诗体改写和申论拓展只作为任务/产出边界，不计入教材正文或 KP 覆盖。

## 6. R01—R10 硬性检查与 P0/P1/P2

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 册次、单元/诵读范围、文本类型、课标任务群、来源和六条关系的语境说明可回到 accepted 上游或已验证 canonical Artifact。 |
| R02 | 否 | 关键册级主张、六条关系、M0/N/A 和覆盖结论都有适配上游节点/KP/EV/任务入口；紧凑 EV 写法可沿节点展开，未出现无来源关系。 |
| R03 | 否 | 4 单元、REC、前言/目录/后记、22+4 文本入口、200 KP、任务群、关系、M0/N/A、教师用书和 Issue 模块齐全。 |
| R04 | 否 | 教材事实、课标、上游研究解释、册级综合、项目建议、外部材料和缺源教师用书分层；未把目录或综合主线冒充正文 KP。 |
| R05 | 否 | BOOK 只索引 accepted 上游 KP；14 张卡的 KP 字段、主层级、理由和 EV 由上游验收提供，册级入口不产生孤立原子点。 |
| R06 | 否 | 四个考试板块均为合法 M0；未引用未登记真题、答案或评分 Artifact。 |
| R07 | 否 | 4/4 单元图谱、1/1 诵读卡及 14/14 底层卡均为 ledger `accepted`，版本和 SHA 与总表一致。 |
| R08 | 否 | BOOK、上游图谱/卡片、source/artifact、版本、200 KP、26 文本入口和六条关系 ID/链接均闭合；BOOK 自身仍为 linted 是正常待审状态。 |
| R09 | 否 | 只使用现行 2020 修订课标的任务群和课程定位，未改写任务群名称或把任务群当固定课型。 |
| R10 | 否 | 未机械铺满核心素养，未给册级综合贴完整学业质量等级标签；M0/N/A 边界明确。 |

`P0/P1/P2 = 0/0/0`。REL-BOOK-X2-005 的紧凑“U02 三卡正文 EV”以及 REL-BOOK-X2-004 的整卡入口仅造成检索性校准扣分，不构成当前版本的内容阻断或返工缺陷。

## 7. 册级量表评分

| 维度 | 权重 | 门槛 | 得分 | 复核依据 |
|---|---:|---:|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25 | 23 | **25.0** | 4/4 accepted 单元、1/1 accepted REC、14/14 底层卡、22+4 文本入口、200 KP、前言/目录/后记边界完整。 |
| 跨单元递进 | 20 | 17 | **18.5** | 六条受控关系覆盖迁移、深化、比较，并有两端 accepted 证据；两处紧凑 EV/整卡入口需要沿节点二跳，保守扣1.5。 |
| 分类、去重与稳定 ID | 15 | 13 | **14.5** | 关系类型受控、六个 REL-ID 唯一，图谱 KP 与底层卡明确去重；未另建独立去重清单，扣0.5。 |
| 双线、任务群与课程定位 | 15 | 13 | **14.5** | 人文/语言主线覆盖五类入口，四任务群/关联任务群和课标边界清楚；册级主线保持综合身份，扣0.5。 |
| 高考板块映射 | 10 | 8 | **9.0** | 四板块均有 M0 和解锁条件，未越级；尚无真题双向证据，保留治理余量。 |
| 上下游一致性 | 10 | 9 | **10.0** | 4/4 图谱、1/1 REC、14/14 卡的 ledger 状态、版本、当前 SHA、source/artifact 与计数完全闭合；BOOK 自身 linted 与待审阶段一致。 |
| 检索性 | 5 | 4 | **4.5** | 索引词、单元入口、问题清单、M0/教师用书边界齐全；紧凑关系证据需回到上游二跳，扣0.5。 |
| **合计** | **100** | **90** | **96.0** | **总分及七维最低分均达标。** |

## 8. 主审决定

**决定：`pass`。** 当前 `BOOK-X2` v0.2.0/SHA `7f80ad15071213da908856e5ea7b38eaa6bff4bdb219d8040e03b93b92212600` 可进入同一版本/SHA 的独立第二复审。本报告不执行 G4 或 `accepted` 状态写回；若总表、任一上游版本/SHA、账本或绑定 validator 改变，本报告失效并须重新复核。

## 9. 可复现绑定

- 总表：`work/knowledge/册级汇总/BOOK-X2.md`；v0.2.0；SHA `7f80ad15071213da908856e5ea7b38eaa6bff4bdb219d8040e03b93b92212600`。
- 上游图谱 SHA：U01 `6a9e4c92e8f442df18b8e698261e814b5010932c08ebb997a606615336a3dc68`；U02 `99239de9a8a599ed7bd57f366caa6d2068541dcbaafda04090a652ba24bc8d49`；U03 `da4924dc06fdd3b5c62490f7ac3583c941d22254baed26ad20ac94af04373ca9`；U04 `d5ebda1d5d874bfc71da3e97987f61fb4a06f30ab4958758c243b59627c39a22`；REC `7b6aaf24bd5b5ea660c2e467b9963f58f205fa1677d734fff5270688ed500a48`。
- ledger：`work/knowledge/_meta/deliverables.jsonl` SHA `b4f55d67a932224810b6722280ca7cee4b38e828049e515d14c9b53364d83f2e`。
- validator：`VAL-20260808-203544+0800`；latest/archive `work/knowledge/_meta/validation_reports/latest.json` 与 `work/knowledge/_meta/validation_reports/archive/VAL-20260808-203544+0800.json`；两者 SHA `bfff60376e4a2f1451a7e9fc16692c6eb98224d9a1738c617664d3bd23c13add`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
