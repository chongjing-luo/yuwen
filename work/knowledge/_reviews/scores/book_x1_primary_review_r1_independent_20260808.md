---
schema_version: "2.0-textbook"
review_id: "REV-BOOK-X1-R1-PRIMARY-INDEPENDENT"
deliverable_id: "BOOK-X1"
artifact_version: "0.2.0"
artifact_sha256: "82c60292b2c459668da944739b80ba50af4e8a63059dd31f70598091d0627747"
review_round: 1
reviewer: "independent_primary_r1"
review_role: "primary"
reviewed_at: "2026-08-08T17:18:29+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
validator_run_id: "VAL-20260808-171132+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-171132+0800.json"
validator_report_sha256: "c93df8c294be11c7dc2e10d5482e67daca87e7d74bf8b611d3b1d179776b155f"
validator_result: "passed"
decision: "pass"
---

# BOOK-X1 v0.2.0 独立主审 R1

## 1. 锁定对象与审查范围

- 本轮只审查 `BOOK-X1` v0.2.0，正文为 `work/knowledge/册级汇总/BOOK-X1.md`，当前 SHA-256 为 `82c60292b2c459668da944739b80ba50af4e8a63059dd31f70598091d0627747`。
- 复核对象包括正文、四个 accepted 单元图谱、accepted 诵读卡、主教材/切分包注册信息、现行课标注册信息和绑定的 validator 归档报告。
- 本轮不修改 BOOK-X1 正文、`work/knowledge/_meta/deliverables.jsonl` 或共享 validator 报告；不把历史报告或旧 SHA 当作本轮证据。

## 2. 上游验收与覆盖审计

| 上游ID | 状态/版本 | 当前 SHA-256 | 正文子文本 | KP | 复核结论 |
|---|---|---|---:|---:|---|
| `UNIT-X1-U01` | accepted / 0.2.0 | `72e11879deb905a2acae150239798318265764ad3f0b211fb577abe0dd0689df` | 6 | 48 | 与 BOOK §1 一致 |
| `UNIT-X1-U02` | accepted / 0.2.1 | `56a06f600a6b4a0e0802d397b34df4568b043276844dde84bfae8d979e300b` | 6 | 37 | 与 BOOK §1 一致 |
| `UNIT-X1-U03` | accepted / 0.2.2 | `d3eb0f7a75ad4e899276337f5349d733dd65a07b7166c1ae02b5978fc0f05481` | 4 | 50 | 与 BOOK §1 一致 |
| `UNIT-X1-U04` | accepted / 0.2.1 | `00e0eea0eef95963b578c6926ca25ecb1db6fa3b1038f3a1c5c731e6d6a01aba` | 1 | 13 | 与 BOOK §1 一致 |
| `CARD-X1-REC-01` | accepted / 0.2.1 | `fca312dba38367a8a2df116178476096f66a28a665e3ecb0239dcc132a249d96` | 4 | 12 | 与 BOOK §1 一致 |

人工复算结果：4/4 单元图谱、1/1 诵读卡、13/13 accepted 卡、21/21 正文子文本和 160/160 KP 闭合；单元内部关系为 U01 8、U02 9、U03 10、U04 6，合计 33 条。BOOK §10 的人文 24、语言 29、关系 33 可由上游图谱和诵读卡复算。

前言、目录、后记只用于册级范围和栏目边界；目录篇名未被直接升格为 KP。现行课标只用于课程定位和任务群边界，未在册级重新制造课标等级判断。

## 3. 来源注册与链接审计

- BOOK front matter 的 20 个 `SRC-*`（主教材、X1-000—017 切分包和 `SRC-CURR-2020`）在 `sources.jsonl` 中全部注册；相关来源等级均为 S1。
- 正文直接列出的 5 个 canonical `ART-*` 均在 `artifacts.jsonl` 中注册且为 canonical/verified；主教材 SHA、前言包 SHA 与正文声明一致。
- BOOK 引用的 Card/KP/EV/TASK/CAND ID，除六个在 BOOK 自身定义的 `REL-BOOK-X1-001`—`006` 外，均能在声明的 accepted 上游或注册表中解析。六个册级关系是本表新增稳定 ID，不要求在上游文件重复定义。
- 绑定 validator `VAL-20260808-171132+0800` 为 `passed`，六类检查均 0 errors，`hash_verification=true`；本报告使用其归档 SHA `c93df8...b155f`，不以运行后产生的其他临时报告替代绑定报告。

## 4. 六条册级关系的 Claim—Evidence 复核

| REL-ID | 关系适配复核 | 证据闭合结论 |
|---|---|---|
| `REL-BOOK-X1-001` | U01 `CAND-L-X1-U01-05` 的真实性、出处、材料—观点功能链迁移到 U02 `CAND-L-UNIT-X1-U02-007` 的原句理解、概念界定、立意与修订。两端动作相近但文体语境不同，正文明确写出差异。 | U01 `EV-CARD-X1-U01-01-007`、`EV-CARD-X1-U01-03-018` 与 U02 `EV-CARD-X1-U02-01-011`、`EV-CARD-X1-U02-02-013` 均可定位；任务源为 `ART-PKG-X1-005-PDF`/`ART-PKG-X1-009-PDF`。通过。 |
| `REL-BOOK-X1-002` | U02 `CAND-L-UNIT-X1-U02-002` 先复算“命题—证据—推理—结论”，U04 `CAND-L-UNIT-X1-U04-003` 再检查论据支持、隐含前提和反例；关系是证据化阅读到公共论证审查的深化，不把经典思想改写成形式逻辑定理。 | U02 `EV-CARD-X1-U02-01-004`、`EV-CARD-X1-U02-03-003` 与 U04 `EV-CARD-X1-U04-01-018`—`019`、`025`—`026` 对齐；均为 accepted 卡证据。通过。 |
| `REL-BOOK-X1-003` | U01 `CAND-L-X1-U01-05` 的“材料—形式—解释”链迁移为 U03 `CAND-L-UNIT-X1-U03-004` 的“细节—行动/心理—人物关系—主题功能”链；正文保留历史/新闻材料责任与小说叙事解释的差异。 | U01 `EV-CARD-X1-U01-03-011`—`016` 与 U03 `EV-CARD-X1-U03-01-008`、`EV-CARD-X1-U03-02-008`、`EV-CARD-X1-U03-04-014`—`015` 均可回查。通过。 |
| `REL-BOOK-X1-004` | U03 小说以叙事细节和环境制约组织人物关系，REC `KP-CARD-X1-REC-01-011` 以意象、复沓、时空、虚实和情绪转折复原诗词形式—情感关系；正文明确关系是比较，不把叙事技巧与诗词格律同质化。 | U03 `EV-CARD-X1-U03-02-001`—`003`、`EV-CARD-X1-U03-03-018`—`019` 与 REC `EV-CARD-X1-REC-01-002`—`005` 可定位；REC KP 为 accepted。通过。 |
| `REL-BOOK-X1-005` | U04 `CAND-H-UNIT-X1-U04-003` 的虚拟论敌、反例和前提质疑迁移到 U01 `TASK-X1-U01-03` 的情感—理性研讨；正文明确只能服务有证讨论，不能用逻辑术语替代作品语境。 | U04 `EV-CARD-X1-U04-01-024`—`030`、U01 任务源 `ART-PKG-X1-005-PDF` 物理页 46 及 `EV-CARD-X1-U01-01-006` 对齐。通过。 |
| `REL-BOOK-X1-006` | U03 `CAND-H-UNIT-X1-U03-001` 的成长、受辱与尊严与 U01 `CAND-H-X1-U01-04` 的人物品质均要求以事件、细节和选择证明判断；正文保留个体成长与革命/建设历史集体语境的边界，关系标为比较而非递进。 | U03 `EV-CARD-X1-U03-01-002`—`008` 与 U01 `EV-CARD-X1-U01-02-002`—`007`、`EV-CARD-X1-U01-04-002`—`008` 均能回查。通过。 |

六条关系均具备唯一 REL-ID、受控关系类型、两端节点/任务、共性—差异或迁移说明和双方证据；未发现把主题邻近偷换为确定性递进或只有单端证据的关系。

## 5. 硬性否决项

| 规则 | 触发？ | 复核依据 |
|---|---|---|
| R01 关键事实错误、伪造或张冠李戴 | 否 | 单元、诵读篇目、任务群、作者/人物和关系主张均可回到 accepted 上游或 canonical 来源。 |
| R02 不可定位引文/来源不适配/I 类解释少于两处证据 | 否 | 正式关系均有适配 Card/KP/EV；六条册级关系均给出双方证据，未发现孤立引文。 |
| R03 合编文本漏项或必填模块缺失 | 否 | 4 单元、REC、前言/目录/后记边界、任务、M0、前后序、问题清单和自检模块齐全；21 子文本/160 KP 闭合。 |
| R04 把解释、提示或 OCR 冒充规范结论 | 否 | 教材事实、课标证据、上游研究解释、项目评价和教师用书缺源均分层呈现。 |
| R05 原子知识点缺主层级、映射理由或有效证据 | 否 | BOOK 只消费上游 KP，不重造原子 KP；上游 160/160 KP 已由 accepted 图谱/卡片验收。 |
| R06 越级高考衔接或引用未登记真题 | 否 | 四个高考板块全部保持结构化 M0/N/A，未消费试卷、答案或评分 Artifact。 |
| R07 使用未验收上游 | 否 | 五个上游均为 ledger `accepted`，版本和 SHA 与正文表格一致。 |
| R08 数量、ID、版本或链接不一致导致断链 | 否 | 正文声明的上游数量、SHA、Card/KP/EV/TASK/CAND ID 均可解析；册级 REL-ID 在本表内定义完整。账本旧版状态是待同步行政事项，未造成内容链接断裂。 |
| R09 使用非现行课标或改写任务群 | 否 | 仅使用 `SRC-CURR-2020`，任务群名称和三类语文学习活动均保留现行课标表述。 |
| R10 机械铺满核心素养或把学业质量当难度标签 | 否 | 未为单元/KP/关系贴学业质量等级，未机械补齐素养；M0/N/A 边界明确。 |

## 6. 册级量表评分

| 维度 | 权重 | 门槛 | 得分 | 复核依据 |
|---|---:|---:|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25 | 23 | **25.0** | 4/4 单元、U04 专题、REC 四篇、前言定位和仅 accepted 上游均覆盖。 |
| 跨单元递进 | 20 | 17 | **19.0** | 六条关系覆盖迁移、深化、比较并有双方证据；前后册无可靠双方证据处保持 N/A。 |
| 分类、去重与稳定 ID | 15 | 13 | **14.5** | 关系类型在受控词表内，六个 REL-ID 唯一，检索节点不重复；未另设独立去重清单，扣 0.5。 |
| 双线、任务群与课程定位 | 15 | 13 | **14.5** | 人文 24、语言 29、任务群/课标定位均可回到上游；综合语言主线明确区分教材事实与研究性索引。 |
| 高考板块映射 | 10 | 8 | **9.0** | 现代文、古诗文、语言文字运用、写作四板块均有 M0 入口和解锁条件；尚无真题双向证据，保留 1 分治理余量。 |
| 上下游一致性 | 10 | 9 | **9.0** | 上游版本/SHA、计数和链接闭合；`deliverables.jsonl` 仍记录 BOOK-X1 drafted/v0.1.0，待状态同步，故不计满分。 |
| 检索性 | 5 | 4 | **4.5** | §8 索引词、单元入口和 §9 Issue 清单齐全；部分综合主线仍需通过上游节点二跳，扣 0.5。 |
| **合计** | **100** | **90** | **95.5** | 达到总分和所有单项门槛。 |

## 7. P0/P1/P2 与决定

| 等级 | 数量 | 说明 |
|---|---:|---|
| P0 | 0 | 无来源造假、严重事实错误、硬依赖断裂或不可恢复错误。 |
| P1 | 0 | 覆盖、Claim—Evidence、六条 REL、M0 和 accepted 上游链均已闭合。 |
| P2 | 0 | 未发现影响本版内容验收的独立缺陷。账本的 drafted/v0.1.0 是已知状态同步事项，不改正文、不改变已锁定 SHA；G4 前需由授权流程同步，但不构成本轮内容 P2。 |

**主审决定：`pass`。** BOOK-X1 v0.2.0/SHA 可进入同 SHA 的独立二审；本报告不等同于 G4 或 `accepted` 状态写回。后续若正文、上游版本或绑定 validator 改变，必须重新计算 SHA 并使本报告失效。

## 8. 可复现信息

- 被评正文：`work/knowledge/册级汇总/BOOK-X1.md`；版本 `0.2.0`；SHA `82c60292b2c459668da944739b80ba50af4e8a63059dd31f70598091d0627747`。
- 上游锁定：`UNIT-X1-U01` `72e11879...0689df`；`UNIT-X1-U02` `56a06f60...e300b`；`UNIT-X1-U03` `d3eb0f7a...05481`；`UNIT-X1-U04` `00e0eea0...01aba`；`CARD-X1-REC-01` `fca312db...9d96`。
- validator：`VAL-20260808-171132+0800`；归档报告 [VAL-20260808-171132+0800.json](../../_meta/validation_reports/archive/VAL-20260808-171132+0800.json)；SHA `c93df8c294be11c7dc2e10d5482e67daca87e7d74bf8b611d3b1d179776b155f`；结果 `passed`。
- rubric：`2.0-textbook`；SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`。
- taxonomy SHA：`13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
