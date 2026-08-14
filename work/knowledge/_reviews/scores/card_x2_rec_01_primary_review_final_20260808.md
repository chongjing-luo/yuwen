---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X2-REC-01-FINAL-PRIMARY"
deliverable_id: "CARD-X2-REC-01"
artifact_version: "0.2.0"
artifact_sha256: "dc1577a29150ca5cf09511068586a4a02c5881725897897fa38e7aec28c92ef0"
review_round: 1
reviewer: "independent_primary_x2_rec_01_final"
review_role: "primary"
reviewed_at: "2026-08-08T20:30:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "f87e72cdd14a5059ed1854a77a3eacb68374207eca7918de06fedc0932e21f6f"
validator_run_id: "VAL-20260808-201123+0800"
validator_report: "work/knowledge/_meta/validation_reports/latest.json"
validator_report_sha256: "9cb58bfb9a3b9c39fa7ddc17f6851b5c6dd38eb61f7fcc2c7627b23530a4f441"
validator_archive_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-201123+0800.json"
validator_archive_report_sha256: "9cb58bfb9a3b9c39fa7ddc17f6851b5c6dd38eb61f7fcc2c7627b23530a4f441"
validator_result: "passed"
decision: "pass"
---

# CARD-X2-REC-01 v0.2.0 独立主审

## 1. 输入锁定、独立性与量表

本轮只审当前 `CARD-X2-REC-01` 知识卡，不修改卡片正文、账本、validator 报告或状态，不复用旧版本的 SHA、分数和结论。采用冻结 `2.0-textbook` 知识卡量表：总分门槛 85，七维门槛为 `21/18/12/12/8/6/5`。

| 对象 | 当前绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修中册/cards/CARD-X2-REC-01.md`；v0.2.0；SHA `dc1577a29150ca5cf09511068586a4a02c5881725897897fa38e7aec28c92ef0`；状态 `linted` |
| 教材 canonical artifact | `ART-PKG-X2-018-PDF`；7页；SHA `79e9299665b821edb9bf3494c0756d1318ff1af1c1cd3299fbc74a12e1df057c`；`Data/textbook_extract/选择性必修中册/18_古诗词诵读.pdf`；物理页131—137，切分页1—7 |
| 课标 canonical artifact | `ART-CURR-2020-PDF`；66页；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；`Data/reference/curriculum/普通高中语文课程标准（2017年版2020年修订）_教育部官方版.pdf` |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；当前 SHA `f87e72cdd14a5059ed1854a77a3eacb68374207eca7918de06fedc0932e21f6f`；条目为 `CARD-X2-REC-01` / v0.2.0 / `linted` |
| validator | `VAL-20260808-201123+0800`；latest 与 archive 均 `passed`，0 errors，`hash_verification=true` |

MinerU 的 `full.md` 和 JSON 仅作为导航辅助；正式引文与事实判定均回看上述 canonical PDF。现行课标引用物理页23—29、44—45（印刷页15—21、36—37），与卡片 EV 定位相符。

## 2. 来源、正文边界与逐条证据复核

### 2.1 覆盖与边界

卡片完整登记 4 个正文子文本、17 个 KP 和 16 个 EV。物理页131—135（切分页1—5）逐页覆盖《燕歌行并序》《李凭箜篌引》《锦瑟》《书愤》的题名、作者、正文、注释及各篇正文后的教材提示；物理页136 的《普通高中教科书 语文》后记和物理页137 空白页由 EV-011 明确排除，不建正文子文本。未登记网络赏析、外部诗词、未经双向核验的真题或未匹配教师用书。

### 2.2 Canonical PDF 引文复核

- EV-001 的栏目名、四篇题名和作者在物理页131—135逐页命中；“古诗词诵读”“燕歌行并序/高适”“李凭箜篌引/李贺”“锦瑟/李商隐”“书愤/陆游”与卡片范围一致。
- EV-002—004 的《燕歌行并序》正文及提示分别命中物理页131—132：出师、失利、被围、死斗；“战士军前半死生，美人帐下犹歌舞”；“至今犹忆李将军”；以及“气势雄浑悲壮”“格调雄健激越，慷慨悲壮，节奏起伏跌宕，张弛有度”等提示原文均可复核。
- EV-005—006 的《李凭箜篌引》正文/提示命中物理页133： “昆山玉碎凤凰叫，芙蓉泣露香兰笑”“石破天惊逗秋雨”“老鱼跳波瘦蛟舞”，以及“惊人的想象贯串神仙世界和人间世界”“视觉、听觉、触觉等多种感官体验熔铸于一炉”“摹写声音至文”。
- EV-007—008 的《锦瑟》正文/提示命中物理页134：教材明确说“一篇《锦瑟》解人难”“历来有多样的解释”“可以这样解读”，并以华年、梦蝶、杜鹃、珠泪、玉烟和“往事如烟”的感受给出示例边界；卡片未将示例写成唯一答案。
- EV-009—010 的《书愤》正文、注释和提示命中物理页135： “楼船夜雪瓜洲渡，铁马秋风大散关”“塞上长城空自许”“出师一表真名世”，以及宿志、失地、沉郁浑厚、颔联雄放和结合诗人经历诵读等提示原文均可定位。
- EV-011 的后记和空白页物理边界可在物理页136—137复核；EV-012—015 的任务群4、5、8和学业质量文字在课标 canonical PDF 物理页23—29、44—45逐字可定位；EV-016 是教师用书/外部材料缺源声明，没有被伪装成教材正文事实。

## 3. Claim—Evidence、KP 与结构复核

- 17/17 KP 均有受控主维度、人文/语言双线、知识类型、四层主归属、判定理由、有效 EV 和置信状态；没有孤立 KP。
- 四篇作品的正文事实、注释信息、教材提示和课标定位均分层。解释型 KP-002、005、009、011、014 由相应正文与提示的相邻证据共同支撑；策略/程序型 KP-004、007、010、015—017 明确是基于教材/课标证据形成的可执行项目表达，不冒充教材原句。
- 人文维度覆盖边塞现实批判、声音神话化、多解追忆、报国书愤；语言维度覆盖叙事阶段、意象联觉、典故与节奏、证据驱动的诵读比较。跨篇比较明确标注为项目综合，并保留四篇语境差异。
- 课标对接仅使用现行任务群4“语言积累、梳理与探究”、任务群5“文学阅读与写作”、任务群8“中华传统文化经典研习”；学业质量仅作可观察表现边界，不给单卡贴完整水平标签。
- 高考区保持结构化 `N/A | M0 | N/A | N/A`：当前未登记可双向核验的真题小问、答案和评分 Artifact，不把题型相似性升级为 M1—M3。纵向栏为有理由的 N/A，教师用书 `edition_match=unknown` 且未消费教辅意见。

## 4. R01—R10 与 P0/P1/P2

| 代码 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 四篇题名、作者、诗句、注释、教材提示和课标术语与 canonical PDF 一致；未发现关键事实错误或张冠李戴。 |
| R02 | 否 | 16/16 EV 均有适配 Source、canonical Artifact、物理/切分页 locator、短引和 verified 元数据；需证解释均有相邻正文/提示的适配证据。 |
| R03 | 否 | 四个正文子文本、注释/提示边界、课标、纵向、高考、三类教学提示和证据表齐全；后记/空白页排除明确。 |
| R04 | 否 | canonical 正文、教材提示、课标、项目建议、MinerU 导航和教师用书缺源分层清楚；没有把 OCR 或研究性解释冒充规范结论。 |
| R05 | 否 | 17/17 KP 均具主层级、受控类型、映射理由和有效证据。 |
| R06 | 否 | 仅保留合法结构化 M0，未引用未登记真题或声称高考直接衔接。 |
| R07 | 否 | 只消费已验证学生教材和现行课标；教师用书未知不被下游消费。 |
| R08 | 否 | 卡片、四个 SUBTEXT、17 KP、16 EV、Source/Artifact、版本与当前 SHA/ledger/validator 绑定一致。 |
| R09 | 否 | 使用现行 2020 修订课标任务群名称，未把任务群改写为固定课型或教法。 |
| R10 | 否 | 核心素养只作有证据的定位，未机械铺满；学业质量没有被当作单课难度标签。 |

`P0/P1/P2 = 0/0/0`。本轮未发现阻断接受或需返工的开放缺陷。

## 5. 知识卡量表评分

| 维度 | 权重 | 门槛 | 得分 | 依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | **24.5** | 16/16 EV 均有 canonical locator、Source/Artifact、短引和 verified 元数据；四诗、课标与边界证据闭合，保守扣0.5。 |
| 事实与术语准确性 | 20 | 18 | **20.0** | 题名、作者、诗句、注释、教材提示、任务群4/5/8及学业质量页位准确，事实与项目解释边界清楚。 |
| 字段完整与知识粒度 | 15 | 12 | **15.0** | 4/4子文本、17/17 KP、16/16 EV、纵向、高考和三类教学提示均完整；KP 保持文本特异且可检索。 |
| 双维度与母题质量 | 15 | 12 | **14.5** | 边塞现实批判、声音神话化、多解追忆、报国书愤与叙事/意象/联觉/典故/节奏双线并置；跨篇综合仍需依赖原句，保守扣0.5。 |
| 四层与高考映射 | 10 | 8 | **10.0** | 17个KP均有四层主归属和理由；课标定位与 M0/N/A 边界严格，无越级映射。 |
| 纵向贯通 | 8 | 6 | **8.0** | 无双方均 accepted 且证据对齐的目标 KP 时保留有理由 N/A，不以一般意象分析强造递进。 |
| 教学可用性与表达 | 7 | 5 | **6.5** | 教材提示、项目建议、教师用书缺源、课标成果边界分离；诵读—标注—原句解释—比较流程可执行，多文本汇总略复杂，扣0.5。 |
| **合计** | **100** | **85** | **98.5** | **总分及七维最低分均达标。** |

## 6. 主审决定

**决定：`pass`。** 当前 `CARD-X2-REC-01` v0.2.0/SHA `dc1577a29150ca5cf09511068586a4a02c5881725897897fa38e7aec28c92ef0` 可进入独立第二复审。本报告仅为独立 primary 记录，不写回 `accepted` 或修改任何上游/账本状态；若卡片、canonical Artifact、ledger 或 validator 绑定发生变化，本报告失效并须按新 SHA 重审。

## 7. 可复现绑定

- 卡片：`work/knowledge/选择性必修中册/cards/CARD-X2-REC-01.md`；v0.2.0；SHA `dc1577a29150ca5cf09511068586a4a02c5881725897897fa38e7aec28c92ef0`。
- 教材：`ART-PKG-X2-018-PDF` SHA `79e9299665b821edb9bf3494c0756d1318ff1af1c1cd3299fbc74a12e1df057c`；课标：`ART-CURR-2020-PDF` SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- ledger：`f87e72cdd14a5059ed1854a77a3eacb68374207eca7918de06fedc0932e21f6f`；latest/archive validator：`VAL-20260808-201123+0800`，两者 SHA 均 `9cb58bfb9a3b9c39fa7ddc17f6851b5c6dd38eb61f7fcc2c7627b23530a4f441`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
