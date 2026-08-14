---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-03-R1-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-03"
artifact_version: "0.2.0"
artifact_sha256: "c6388cbb05439e6ab3105e34df649c42371fb47d9c5d5104be4268217d1cb096"
review_round: 1
reviewer: "independent_primary_x3_u01_03_r1"
review_role: "primary"
reviewed_at: "2026-08-08T21:39:27+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "9bfee136f8917ef3c8e74d67f233580fbb20ca79cd500c23328721c8a0207a77"
validator_run_id: "VAL-20260808-213631+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-213631+0800.json"
validator_report_sha256: "aa66d88197a11d1219e7779d90c8f2885fff7524a47442dd383a19a7b916b9ed"
validator_result: "passed"
decision: "rework"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "a790e8fff46946c29a40b7ba04667c3dda522c21ed3b661e5d9844ee78bff12b"
---

# CARD-X3-U01-03 v0.2.0 独立主审 R1

## 1. 输入锁定与独立性

本轮从指定的 v0.2.0 快照重新开始，仅使用当前卡片、冻结 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 教材、U01 单元任务、现行课标、共享账本和指定 validator 归档报告；不修改卡片、账本、validator 或状态迁移，不用其他评审结论代替当前核验。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-03.md`；v0.2.0；SHA `c6388cbb05439e6ab3105e34df649c42371fb47d9c5d5104be4268217d1cb096`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-003-PDF`；SHA `4d9e3d30605095b1a9131876a2e9fc2ebb6046ae9c48dfcedc0844f2e32a73ea`；物理页19—21、切分页1—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；66页 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `9bfee136f8917ef3c8e74d67f233580fbb20ca79cd500c23328721c8a0207a77`；CARD-X3-U01-03 为 v0.2.0/`linted` |
| validator | `VAL-20260808-213631+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `aa66d88197a11d1219e7779d90c8f2885fff7524a47442dd383a19a7b916b9ed` |

## 2. 覆盖、页码与语义复核

- canonical 课3三页完整覆盖《蜀道难》（物理页19—20/切页1—2）、《蜀相》和学习提示（物理页21/切页3）；U01任务二至四可在任务包物理页25/切页1回查；课标任务群5位于物理页25—27，学业质量4-3位于物理页46。
- 16/16 KP 均有唯一 ID、合法主维度“人文/语言”、冻结知识类型、四层主归属、判定理由、证据 ID 和置信状态；15/15 EV 的 ID 连续，类型字段表面上为单值 Q/F/M/D（Q=11、F=1、M=2、D=1），来源与 locator 均登记。
- 《蜀道难》的开篇、神话/道路、高险意象、听觉与剑阁段，以及《蜀相》的七律结构、“自/空”、三顾两朝和尾联，均能在 canonical PDF 的所列页段找到；EV-002—008 的诗题、诗句和学习提示短引可回查。EV-009—012 的任务、EV-013 的任务群5和 EV-014 的 4-3 课标定位页码正确。
- **P1：EV-001 证据职责与短引不闭合。** 该行 Claim 写为“课3正文、学习提示和任务的来源边界”，但 Source/Artifact 仅为 `SRC-PKG-X3-003`/`ART-PKG-X3-003-PDF`，locator 仅物理页19—21，没有 `ART-PKG-X3-005-PDF` 的任务证据；短引“‘蜀道难’‘蜀相’及其正文、学习提示均位于本canonical课文包；正式引文回到PDF”是项目边界说明，不是教材正文/栏目原文，却将类型填为 Q。按证据表图例，边界声明应为 D，或将 Claim 收窄至课文包并把任务边界另由 EV-009 支撑。当前该行不能独立闭合其正式 Claim，且 KP-001 仍引用该行。
- **P1：§8.1 来源栏目混入项目操作。** “教材学习提示”栏写入“制作‘句式/意象/空间/声音/历史人物/情绪’证据表”和“比较《蜀道难》的虚实交织与《蜀相》的写景—咏史—抒情结构”。教材提示确实要求诵读、体式/风格和情志，任务三以《蜀道难》虚实交织为迁移示例，但并未要求制作该证据表，也未在该栏目直接规定这组具体比较。它们应放入 §8.3 本项目教学建议，或逐项明确标为项目层；否则教材提示与项目建议边界混写。
- 另有非阻断的证据精度项：KP-003—005 的复合 Claim 含道路形成、六龙/扪参/屏息等具体子短语，而 EV-003 的短引只列代表性片段；KP-006、KP-009—012也有少量以宽页 locator 承载的压缩 span。KP-015 的“保留诗句、观点形成过程和修订痕迹”也超出任务一明示的“提炼观点、代表发言”。这些可通过扩展 exact span、拆分 KP 或收窄 Claim 加固，但不改变上述两项 P1 判断。
- M0 行的 KP、真题小问、真题证据和教材证据均为 `N/A`，并给出未建立双向证据的理由；纵向为有理由的 `N/A`；教师用书 `edition_match=unknown`，未消费缺源意见。事实、页码、课标版本和外部真题边界本身无关键错误。

## 3. R01—R10 判定

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、作者、诗句、体式、人物事实、正文页位和课标引用均与 canonical 载体一致，未见关键事实张冠李戴。 |
| R02 | **是** | EV-001 的 Claim 同时要求课文包和任务边界，但其 Source/Artifact/locator 不含任务，且 Q 短引不是 canonical 教材原文；该正式 Claim—EV—来源链未闭合。复合 KP 的局部压缩 span另列为非阻断加固项。 |
| R03 | 否 | 两个正文子文本、学习提示、单元任务、课标、原子 KP、M0、纵向和三类教学提示模块均存在。 |
| R04 | **是** | EV-001 将项目来源边界说明写成 Q（教材正文/栏目原文）；§8.1 又把项目证据表和具体比较操作放进教材学习提示栏，造成规范教材提示与项目建议边界混淆。 |
| R05 | 否 | 16/16 KP 形式字段齐全且均有受控维度、类型、主层级、理由和证据；EV-001虽职责错误，KP-001仍有其他边界/正文/任务证据，未形成全卡原子 KP 无有效证据。 |
| R06 | 否 | 高考保持结构化 M0/N/A，未引用未登记真题、答案或评分资料，也未声称 M1—M3 直连。 |
| R07 | 否 | 正式内容只消费已登记并核验的教材、任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、账本、Source/Artifact、KP/EV 数量和指定版本 SHA 一致；问题是 Claim/栏目语义，不是文件或 ID 断链。 |
| R09 | 否 | 使用现行课标“文学阅读与写作”“语言积累、梳理与探究”和物理页46的 4-3，未改写任务群名称或把质量水平当课型。 |
| R10 | 否 | 未机械铺满四项核心素养，也未把学业质量 4-3 当作单课完整等级或题目难度标签。 |

## 4. P0/P1/P2

| 等级 | 数量 | 缺陷 |
|---|---:|---|
| P0 | 0 | 无来源伪造、大面积事实错误或不可恢复损坏。 |
| P1 | 2 | `P1-EV001-BOUNDARY`：EV-001 的 Q 类型、课文包 Artifact 与“任务边界”Claim不匹配；`P1-SEC81-MIX`：§8.1 将项目操作写成教材学习提示。 |
| P2 | 1 | `P2-SPAN-KP`：多个复合 KP 的代表性短引未逐项展开全部子短语，KP-015还加入任务一未明示的过程留痕要求；可选加固但应随 P1 返工回归检查。 |

## 5. 2.0-textbook 诊断评分

因 R02/R04 与两项 P1 硬门未通过，正式验收分记为 `N/A`；以下为返工定位用诊断分，不替代合格性判断。

| 维度 | 权重 | 门槛 | 诊断得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 18.5 | 14/15 EV 的 canonical 页位与短引基本可回查；EV-001 的 Claim/Artifact/类型职责不闭合，复合 KP 的 span 仍偏压缩。 |
| 事实与术语准确性 | 20 | 18 | 18.5 | 两诗事实、体式、人物和课标术语准确；EV-001 把项目边界写成 Q，且 §8.1 规范来源标签不严，保守扣分。 |
| 字段完整与知识粒度 | 15 | 12 | 14.5 | 双正文、16 KP、15 EV、任务/课标/M0模块齐全；复合 KP 与过程要求尚需收窄。 |
| 双维度与母题质量 | 15 | 12 | 14.0 | 人文/语言覆盖险阻、行旅、祠堂、历史追慕、体式、意象、声音和炼字；个别解释依赖宽 locator，扣分。 |
| 四层与高考映射 | 10 | 8 | 9.5 | 四层理由、4-3定位和 M0 边界合规；当前无真题双向证据。 |
| 纵向贯通 | 8 | 6 | 8.0 | 无可靠相邻 accepted 目标时使用有理由的 N/A。 |
| 教学可用性与表达 | 7 | 5 | 5.0 | 证据链教学动作可用，但 §8.1 将项目操作混入教材提示，来源分层未过。 |
| **诊断合计** | **100** | **85** | **88.0** | 仅用于返工优先级；R02/R04 硬门触发，不能作为放行分数。 |

## 6. 返工与决定

1. 修正 EV-001：将其改为单值 D 边界证据并回链来源注册表，或收窄 Claim 至课3教材包；若保留“任务”范围，必须同时绑定 `SRC-PKG-X3-005`/`ART-PKG-X3-005-PDF` 与任务 locator。更新 KP-001 和所有相关边界引用。
2. 严格拆分 §8.1 与 §8.3：§8.1 只保留 canonical 学习提示可直接支持的体式、风格、诵读和情志；“制作证据表”“具体比较结构”等项目操作移至 §8.3 并明确项目层。
3. 回归补齐 KP-003—005、KP-006、KP-009—012 的关键 exact spans，或删去短引未承载的子短语；核对 KP-015 的过程留痕是否应降为项目建议而非教材任务要求。
4. 升版并重算卡片 SHA、更新 ledger transition、重跑 validator，再以新 SHA 进行独立主审和第二复审；本 SHA 不得进入 `accepted` 或被单元图谱正式消费。

**主审决定：`rework`。** 当前 `CARD-X3-U01-03` v0.2.0/SHA `c6388cbb05439e6ab3105e34df649c42371fb47d9c5d5104be4268217d1cb096` 未通过独立主审。报告不执行任何状态迁移。

## 7. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-03.md`；v0.2.0；SHA `c6388cbb05439e6ab3105e34df649c42371fb47d9c5d5104be4268217d1cb096`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `9bfee136f8917ef3c8e74d67f233580fbb20ca79cd500c23328721c8a0207a77`；CARD-X3-U01-03 为 v0.2.0/`linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-213631+0800.json`；SHA `aa66d88197a11d1219e7779d90c8f2885fff7524a47442dd383a19a7b916b9ed`；结果 `passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-003-PDF`=`4d9e3d30605095b1a9131876a2e9fc2ebb6046ae9c48dfcedc0844f2e32a73ea`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 值置空后，对 canonical 报告字节求 SHA，并回填于 front matter。
