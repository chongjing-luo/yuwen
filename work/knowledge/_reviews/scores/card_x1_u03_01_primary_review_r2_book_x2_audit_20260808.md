---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X1-U03-01-R2-PRIMARY-BOOK-X2-AUDIT"
deliverable_id: "CARD-X1-U03-01"
artifact_version: "0.2.1"
review_round: 2
reviewer: "book_x2_audit"
review_role: "primary"
reviewed_at: "2026-08-08T03:04:17+08:00"
---

# 独立完整主审 R2：CARD-X1-U03-01

## 1. 锁定对象与独立性

- 目标文件：`work/knowledge/选择性必修上册/cards/CARD-X1-U03-01.md`
- 被评版本：`0.2.1`
- artifact SHA-256：`70ce1c1a98e4e0962755bf7b586adbe2cd86ca823ff8b61eb0107d2a40a93fe5`
- rubric SHA-256：`ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`
- taxonomy SHA-256：`13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`
- 账本快照：`deliverables.jsonl` 为 `linted / 0.2.1`，路径、owner 与三项 Source 同卡片一致。
- 独立性：未读取本轮同版本另一审的正文、分数、R/P 或结论；旧版本评分不滚存。本评审者未修改卡片、账本或 transition。
- 判定顺序：冻结契约规定硬性否决先于计分；本轮触发 R02，故不以数值分数抵消，也不继续给出虚假的七维实得分。

## 2. canonical 来源核验

| Artifact | SHA-256 | 本轮目视范围 | 结果 |
|---|---|---|---|
| `ART-PKG-X1-010-PDF` | `d762a16af5519d8200e8e0816aa6f9a70c57daec7caedb4b913a3f65a22530ec` | 切分页1—12；规范 PDF 物理页60—71 | 单元导语、题名、正文、注释与学习提示全部重新渲染目视；发现 EV-003、EV-004 的 exact span 与所列页码不闭合 |
| `ART-PKG-X1-014-PDF` | `6413d049be17349c7fb00c61d7ed4da85105d2f5de1a0a9cf6c7fc8d0f0858a6` | 切分页1—2；规范 PDF 物理页96—97 | 三项单元任务及“学写小小说”重新渲染目视 |
| `ART-CURR-2020-PDF` | `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` | 规范 PDF 物理页32—33；印刷页24—25 | 学习任务群11名称、目标、内容与教学提示重新渲染目视；EV-009 引文一致 |

辅助 `full.md` 只用于导航，不作终审载体：课文提取 SHA `8f7007d424523c8ae75c500bfb8c02d1b30db86ececfe71e101e1701c461a0d4`，单元任务提取 SHA `40b590db25866c5e4075a86acdb61ddc0f9d0305152e219becd3600f6e868745`。

## 3. 硬门缺陷

### P0-01 / R02：EV-003、EV-004 的直接引文不在声明 locator 内

| EV | 卡片声明 locator | canonical PDF 实际位置 | 影响 |
|---|---|---|---|
| EV-CARD-X1-U03-01-003 | 规范物理页62—63；切分页3—4 | “房子真正是老鼠横行的地方”“地板和楼梯都已腐烂”均在规范物理页61、切分页2；只有“这全是我的活儿”在物理页62、切分页3 | 一条 Q 中 2/3 exact span 无法由所列 locator 定位；EV-003 及其消费 Claim/KP-008 的证据链不合格 |
| EV-CARD-X1-U03-01-004 | 规范物理页64—65；切分页5—6 | “脑袋又大又亮……”在规范物理页62、切分页3；“简而言之”首次支撑位置在物理页63、切分页4；“腰杆儿笔挺地走出来……”在物理页64、切分页5 | 一条 Q 中 2/3 exact span 无法由所列 locator 定位；EV-004 及其消费 Claim/KP-006、KP-007 的证据链不合格 |

这不是页码展示偏好：split manifest 的起页为规范物理页60，切分页2/3/4/5可分别复算为物理页61/62/63/64。冻结 R02 明定“直接引文不可定位”即硬性否决。

### P0-02 / R02：正式主张未闭合到所列 exact span

- §2“价值辨析边界”及 KP-009 明确断言“学习提示同时指出作品对善良、宽厚、仁爱的赞美”；该原文确在物理页71/切分页12，但所绑定 EV-007 的 Claim 目标和 exact span只摘“成长”线索、儿童眼光和社会批判，未摘“善良、宽厚、仁爱”句，因而正式 Claim 没有闭合到 exact span。
- KP-013 使用“语言简洁”“删繁去冗/避免空泛主题”等写作要求，所绑定 EV-012 的 exact span只含“明确立意”“巧于构思”“抓住传神之处重点刻画”；相关核心要件虽在同页正文中，却未进入该 Q 的 exact span。
- KP-012 把赏析对象展开为情节、人物、叙述视角、环境与语言风格，但唯一绑定 EV-012 的 exact span只写“选取感兴趣的某一要点”和字数，未收录这些分类；卡内其他 EV 也未回链到该 KP。

按照冻结 Claim→EV→exact span→locator 闭包要求，同页存在但未被所列 Q span 覆盖，不能视为已完成正式证据绑定。

## 4. 其他须修订项

### P2-01：核心素养字段未给出核心素养及语言实践依据

课标对接表的“主要核心素养表现及依据”单元只复述任务群11并说明不判完整学业质量水平，未选择任何受控核心素养，也未提供核心素养官方定义与本课可观察语言实践的双向依据。模块标题存在不能替代必填字段内容。

### P2-02：版本记录中的 canonical Artifact SHA 错一位

版本记录把 `ART-PKG-X1-010-PDF` 写为 `d762a16af5519d820e8e...`；注册表与实文件均为 `d762a16af5519d8200e8e...`。Artifact ID 和路径仍可借注册表追溯，故当前未升级为“导致断链”的 R08，但内外一致检查不通过。

## 5. 已通过范围

- front matter 与 ledger 的 card ID、版本、状态、路径及 Source 列表一致。
- 一个正文子文本的边界合理；导语、学习提示与单元任务未伪造成正文子文本。
- 13 个 KP 均有稳定 ID、受控主维度/知识类型/主层级、理由和证据引用；纵向 N/A 与高考 M0 结构合法。
- EV-001/002/005—012 的所列短引在对应 canonical PDF 中可复核；任务群11名称、课程类型及 QD N/A 边界正确。
- 教材学习提示、教师用书缺源与本项目建议三类边界分离。

上述通过项不能抵消 R02。

## 6. R01—R10

| 代码 | 触发？ | 证据/说明 |
|---|---|---|
| R01 | 否 | 未发现题名、作者、作品或课标关键事实张冠李戴。 |
| R02 | **是** | EV-003/004 的多个 Q span 不在所列 locator；另有三组正式 Claim 未闭合到所列 exact span。 |
| R03 | 否 | 一个正文子文本及十个模块均存在；核心素养字段内容不足记 P2，不按整个模块缺失处理。 |
| R04 | 否 | 学习提示、课标、教师用书缺源和项目建议边界清楚。 |
| R05 | 否 | 13 个 KP 均有主层级、理由和证据 ID；本轮问题是证据闭包质量。 |
| R06 | 否 | 高考保持结构化 M0，未引用未登记真题。 |
| R07 | 否 | 知识卡直接消费已登记 S1 教材与课标，不构成下游消费未验收知识成果。 |
| R08 | 否 | 当前 card/ledger 版本与 SHA 锁定一致；版本记录 Artifact SHA 错字尚未使注册表回溯断裂，记 P2。 |
| R09 | 否 | 使用现行课标，任务群11名称与课程类型准确。 |
| R10 | 否 | 未机械铺满四项核心素养，QD 保持 N/A。 |

## 7. 七维评分与 P0/P1/P2

| 项目 | 结果 |
|---|---|
| 七维实得分 | **N/A（R02 硬性否决，按 §6.1 不计分）** |
| 总分 | **N/A** |
| P0 | **2**：定位失配；正式 Claim—exact span 未闭合 |
| P1 | **0** |
| P2 | **2**：核心素养字段内容不足；版本记录 Artifact SHA 错字 |

## 8. validator、决定与状态边界

- validator：`python scripts/validate_knowledge_base.py --project-root . --report /tmp/card_x1_u03_01_v021_primary_book_x2_audit_20260808.json`
- run_id：`VAL-20260808-025822+0800`
- 结果：`passed`；errors `0`；warnings `3`。
- validator 报告 SHA-256：`3334f1bc06ec7782b23d7b52869291827f0c552a0ea6ab0754b2518e2e1607d2`
- 三项 warning 分别为外部评价/政策/真题待并入、TB2/B2 edition_match unknown、试卷契约待校准；均不解释或关闭上述卡内 R02。
- validator 不解析 Markdown 的 Claim/Q exact span 和 locator 语义，故结构通过不等于本轮内容门通过。
- 决定：**fail / rework**。
- 必须修改项：修正 EV-003/004 locator；补齐正式 Claim 所需 exact span/回链；补核心素养及实践依据；校正版本记录 Artifact SHA；随后升版、生成新 SHA 并从结构门开始完整双审。
- 本报告只绑定 v0.2.1/SHA `70ce1c1a...93fe5`；未修改卡片、ledger 或 transition。
