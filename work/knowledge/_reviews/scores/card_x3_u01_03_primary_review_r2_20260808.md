---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U01-03-R2-PRIMARY-INDEPENDENT"
deliverable_id: "CARD-X3-U01-03"
artifact_version: "0.2.2"
artifact_sha256: "23b15296d70abd7b8ddb0c7b17f5cc98b32baa6de05431ea3e914a95c5f99469"
review_round: 2
reviewer: "independent_primary_x3_u01_03_r2"
review_role: "primary"
reviewed_at: "2026-08-08T21:45:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "fea2e39b3722566a732903779186df186ea6cadb05ca8f255383adf10c9fa7e5"
validator_run_id: "VAL-20260808-214232+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-214232+0800.json"
validator_report_sha256: "d2775657eccadc182d34439da0dc90a0ee55e4c05912a1e6cc14c037f302d853"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: ""
---

# CARD-X3-U01-03 v0.2.2 独立主审 R2

## 1. 输入锁定与独立性

本轮针对返工后的 v0.2.2 快照重新主审。仅使用当前卡片、冻结的 `2.0-textbook` rubric/taxonomy、Source/Artifact 注册表、canonical 学生教材、U01 单元任务、现行课标、共享账本和指定 validator 报告；不修改卡片、账本、validator 或状态迁移。

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U01-03.md`；v0.2.2；SHA `23b15296d70abd7b8ddb0c7b17f5cc98b32baa6de05431ea3e914a95c5f99469`；状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-003-PDF`；SHA `4d9e3d30605095b1a9131876a2e9fc2ebb6046ae9c48dfcedc0844f2e32a73ea`；物理页19—21、切分页1—3 |
| U01任务 canonical | `ART-PKG-X3-005-PDF`；SHA `f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；物理页25—26、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `fea2e39b3722566a732903779186df186ea6cadb05ca8f255383adf10c9fa7e5`；CARD-X3-U01-03 为 v0.2.2/`linted` |
| validator | `VAL-20260808-214232+0800`；归档报告 `passed`、0 errors、`hash_verification=true`；报告 SHA `d2775657eccadc182d34439da0dc90a0ee55e4c05912a1e6cc14c037f302d853` |

## 2. 覆盖与返工回归

- 当前卡片包含 2 个正文子文本、16 个原子 KP 和 15 个 EV；EV 类型为 Q=11、F=1、M=2、D=1，均为单值受控类型。所有 KP 均具备主维度、知识类型、四层归属、判定理由、证据 ID 和置信状态。
- canonical 三页课文完整覆盖《蜀道难》（物理页19—20、切页1—2）、《蜀相》和学习提示（物理页21、切页3）；U01 任务证据定位于任务包物理页25、切页1；课标学业质量 4-3 定位于规范物理页46。
- 上轮的 EV-001 混源已修正：当前 Claim 收窄为课文正文子文本与标题范围，Artifact/locator 只指向课文包，不再声称覆盖单元任务。任务边界由 EV-009—012 独立支持。
- §8.1 当前只保留教材学习提示关于诵读、古体/七律体式、风格和情志的内容；证据表、比较步骤和修订留痕已移入 §8.3，并明确为本项目教学建议。
- EV-003—005 已改为连续完整的《蜀道难》正文 span；KP-015 已收窄为任务一明示的主题研讨、观点提炼和代表发言，过程留痕不再冒充教材要求。M0、高考字段、纵向 N/A 和教师用书 `edition_match=unknown` 均保持规范。

## 3. Claim—Evidence 闭合复核

- 《蜀道难》开篇的神话/历史层、高险空间与身体动作链，第二段的鸟声、子规、绝壁和雷声，第三段的剑阁、守关风险和“早还家”，分别由 EV-003、EV-004、EV-005 的连续原文支持；三次“蜀道之难”的回环位置可逐段回查。
- 《蜀相》的祠堂空间、春草黄鹂、“自/空”、三顾两朝和尾联未捷之叹由 EV-007 支持；学习提示关于杂言古体诗、七律、李白/杜甫风格和感时忧国的说明由 EV-006、EV-008 支持。
- U01 研讨、比较阅读、虚实/意象探究、800 字鉴赏文章及《古典诗词鉴赏集》由 EV-009—012 支持；课标任务群5与学业质量4-3由 EV-013—014 支持；教师用书缺源仅由 EV-015 作 D 类边界声明。
- 人文维度覆盖山川行旅、历史人物、未竟功业和忧国情志；语言维度覆盖古体/七律、空间与声音意象、复沓、炼字、章法、虚实和比较策略。研究性概括均注明不是教材唯一答案。

仍有两项轻微表达加固建议，但不构成证据断链：

1. EV-001 类型仍为 Q，短引中“本canonical课文包”属于项目元数据措辞；标题与页位本身可回查。后续可将短引改成仅含教材标题，或将边界表述单独改作 D。
2. EV-006 Claim 同时覆盖体式、风格和诵读，短引主要列体式句，locator 已覆盖完整学习提示页。后续可扩展连续短引，或收窄 Claim 到当前短引明确承担的体式/形式差异。

## 4. R01—R10 判定

| 代码 | 触发？ | 本轮结论 |
|---|---|---|
| R01 | 否 | 两诗题名、作者、诗句、体式、人物事实、页码和课标术语均与 canonical 载体一致。 |
| R02 | 否 | 15/15 EV 均有可解析的 Source/Artifact/locator/短引；EV-001 已收窄，EV-006 虽可加固但可由完整页位回查，未形成需证主张缺适配来源。 |
| R03 | 否 | 正文子文本、学习提示、单元任务、课标、原子 KP、教学模块、M0 和纵向 N/A 均齐全。 |
| R04 | 否 | 教材提示、研究性概括、项目建议和教师用书缺源声明已分层；没有把项目操作写成教材要求。 |
| R05 | 否 | 16/16 KP 均有合法主维度、知识类型、四层归属、判定理由和有效证据。 |
| R06 | 否 | 高考表保持结构化 `M0/N/A`，没有未登记真题、答案或评分资料，也没有虚构 M1—M3 直连。 |
| R07 | 否 | 正式内容只消费已登记并核验的学生教材、任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、账本、Source/Artifact、KP/EV 数量、版本和当前 SHA 一致；validator 已验证哈希。 |
| R09 | 否 | 使用现行课标任务群“文学阅读与写作”“语言积累、梳理与探究”，没有改写任务群名称或把学业质量当课型。 |
| R10 | 否 | 未机械铺满四项核心素养，学业质量 4-3 仅作定位，不作为单课等级或题目难度标签。 |

## 5. P0/P1/P2

| 等级 | 数量 | 缺陷/说明 |
|---|---:|---|
| P0 | 0 | 未发现来源伪造、大面积事实错误或不可恢复损坏。 |
| P1 | 0 | 上轮 EV-001 边界和 §8.1 栏目混写已完成返工并通过回归。 |
| P2 | 2 | `P2-EV001-METADATA`：EV-001 Q 短引含项目元数据措辞，建议改为纯教材标题或 D；`P2-EV006-SPAN`：EV-006 Claim 比短引更宽，建议扩展连续 span 或收窄 Claim。两项均不阻断当前定位与验收。 |

## 6. 2.0-textbook 诊断评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 23.5 | 15/15 EV 均有 canonical 页位、来源和核验状态；EV-001 元数据措辞、EV-006 短引压缩各扣少量。 |
| 事实与术语准确性 | 20 | 18 | 20.0 | 两诗事实、体式、课标术语、页码和解释边界准确，未发现事实错配。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | 2 个子文本、16 KP、15 EV、任务/课标/教学/M0 模块完整，KP 已具文本特异性。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文与语言两线均有正文和学习提示依据，险阻/行旅、历史追慕、体式、意象、声音和炼字相互支撑。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 四层主归属理由清楚，课标 4-3 定位合规，高考严格保持 M0。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前没有双方已验收的相邻目标时，使用有理由的 N/A，不虚构递进边。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 三类教学提示已分离，课标边界、证据链操作和项目建议可直接使用；残余问题仅为 EV 短引加固。 |
| **合计** | **100** | **85** | **98.0** | **总分及七维单项均达标；无硬拒绝规则触发。** |

## 7. 主审决定

**决定：`pass`；总分 `98.0/100`；R01—R10 全部未触发；`P0/P1/P2=0/0/2`。**

当前 `CARD-X3-U01-03` v0.2.2/SHA `23b15296d70abd7b8ddb0c7b17f5cc98b32baa6de05431ea3e914a95c5f99469` 通过本轮独立主审。该结论只绑定本报告 front matter 所列卡片、账本、validator、rubric、taxonomy 和 canonical Artifact 快照；本报告不写回 `accepted`，也不执行 ledger 状态迁移。后续第二复审仍须以同一 SHA 复核，任一上游或卡片变更即使 validator 通过，也须重新绑定并复审。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U01-03.md`；SHA `23b15296d70abd7b8ddb0c7b17f5cc98b32baa6de05431ea3e914a95c5f99469`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `fea2e39b3722566a732903779186df186ea6cadb05ca8f255383adf10c9fa7e5`；当前状态 `linted`、版本 `0.2.2`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-214232+0800.json`；SHA `d2775657eccadc182d34439da0dc90a0ee55e4c05912a1e6cc14c037f302d853`；`passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-003-PDF`=`4d9e3d30605095b1a9131876a2e9fc2ebb6046ae9c48dfcedc0844f2e32a73ea`；`ART-PKG-X3-005-PDF`=`f3fb0f5c960db2f0abcd09ec84760c6332cdc461175e312a461b56372d2bfeb3`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- `report_sha256` 按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 值置空后，对 canonical 报告字节求 SHA-256，再回填本字段。
