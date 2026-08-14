---
schema_version: "2.0-candidate"
review_id: "REV-CARD-X3-U02-04-SECONDARY-R2"
deliverable_id: "CARD-X3-U02-04"
artifact_version: "0.2.1"
review_round: 2
reviewer: "independent_secondary_x3_u02_04_r2"
review_role: "secondary"
reviewed_at: "2026-08-08T23:34:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
taxonomy_sha256: "13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b"
ledger_path: "work/knowledge/_meta/deliverables.jsonl"
ledger_sha256: "6529cd7994e76a7773c6c2c8d1fc424b345416d1cd021582b15101230933fc02"
validator_run_id: "VAL-20260808-232804+0800"
validator_report: "work/knowledge/_meta/validation_reports/archive/VAL-20260808-232804+0800.json"
validator_report_sha256: "d3b4e22e2bc3c90205573449a43d308189c917c747f7c781a5a2f22192046968"
validator_result: "passed"
decision: "pass"
report_sha256_scope: "canonical report bytes with report_sha256 value blank"
report_sha256: "49c3fd5744096eac5027cd041e0c31be9ac2ddc8c4df9294d173ce3fbe7bbaa2"
---

# CARD-X3-U02-04 v0.2.1 返工后的独立第二复审 R2

本轮为独立回归复审，只读取返工后的当前卡片、冻结 `2.0-textbook` rubric/taxonomy、来源与 Artifact 注册表、课8 canonical PDF、U02任务 canonical PDF、现行课标、共享账本和指定 validator 归档报告；不读取或复用上一轮评审结论作为证据，不修改卡片、ledger、validator 或状态迁移。

## 1. 输入锁定与结构复算

| 对象 | 本轮绑定 |
|---|---|
| 卡片 | `work/knowledge/选择性必修下册/cards/CARD-X3-U02-04.md`；v0.2.1；SHA `c2f58ee65c5d8161e9751eac65b884675da0ef575766a5d6d718ad626547e8b6`；front matter 状态 `linted` |
| 学生教材 canonical | `ART-PKG-X3-009-PDF`；SHA `fa25db433fdda0a9468321de7cada4e84b590f3436125db92f683830957f5bc2`；母本物理页60—71、切分页1—12 |
| U02任务 canonical | `ART-PKG-X3-010-PDF`；SHA `ad805e6349d35afe4845ecb463a4cc062d6add372daffe5f655fc464d40b0a7c`；母本物理页72—73、切分页1—2 |
| 现行课标 canonical | `ART-CURR-2020-PDF`；SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`；任务群10物理页31—33、学业质量4-3物理页46 |
| 账本 | `work/knowledge/_meta/deliverables.jsonl`；SHA `6529cd7994e76a7773c6c2c8d1fc424b345416d1cd021582b15101230933fc02`；CARD-X3-U02-04 v0.2.1 / `linted`，含 `REWORK` 迁移 |
| validator | `VAL-20260808-232804+0800`；归档报告 SHA `d3b4e22e2bc3c90205573449a43d308189c917c747f7c781a5a2f22192046968`；结果 `passed`、0 errors、`hash_verification=true` |

独立复算为 `2/2` 登记子文本、`18/18` KP、`18/18` EV；EV 类型为单值 `Q=13`、`F=1`、`M=2`、`D=2`。卡片、账本和 validator 的 v0.2.1/hash 绑定一致。

## 2. 正文与学习提示覆盖回归

### 2.1 canonical 页位

`ART-PKG-X3-009-PDF` 的 split manifest 确认母本物理页60—71对应切分页1—12。逐页核对 canonical PDF：第一幕正文从切页1延续至切页11（物理页60—70、印刷页55—65），“——幕落”在切页11；学习提示完整位于切页12（物理页71、印刷页66）。返工后的卡片已登记：

| 内容 | 卡片当前登记 | canonical 回归结果 |
|---|---|---|
| 第一幕前半 `SUBTEXT-CARD-X3-U02-04-01` | 物理页60—64、切页1—5、印刷页55—59 | 通过；正文连续覆盖 |
| 第一幕后半 `SUBTEXT-CARD-X3-U02-04-02` | 物理页65—70、切页6—11、印刷页60—65 | 通过；含庞太监、茶客议论、常四爷被捕、康顺子昏倒和幕落 |
| 学习提示 | 物理页71、切页12、印刷页66 | 通过；学习提示全文和栏目边界一致 |

### 2.2 EV-010—013 回归

- `EV-CARD-X3-U02-04-010` 当前 locator 为物理页66—70/切页7—11/印刷页61—65；“天下太平了：圣旨下来，谭嗣同问斩”命中切页8，“莫谈国事吧”命中切页9，“你还想拒捕吗”命中切页10，均落在登记范围内。
- `EV-CARD-X3-U02-04-011` 当前 locator 为物理页68—70/切页9—11/印刷页63—65；“又饿又气，昏过去了”“我要活的，可不要死的”“——幕落”均命中切页11。
- `EV-CARD-X3-U02-04-012` 与 `EV-CARD-X3-U02-04-013` 当前均定位物理页71/切页12/印刷页66；教材对全剧时代横断面、第一幕结构、京味语言、人物语言和表现手法的两组短引逐字命中学习提示。
- 第1节、§2—§3、第8节、自检和版本记录均已同步正文物理页60—70/学习提示物理页71；不再存在上一版本的漏页或前移页位。

## 3. KP-015 与其余边界回归

- `KP-CARD-X3-U02-04-015` 已改为“从写作理念、艺术特色或语言风格任选一项，结合茶馆正文提出有证据的观点并交流”；判定理由明确角色/场景数量由项目建议另行约定，不写成教材明示要求。canonical 任务二只要求拓展阅读、选择角度、深入思考和全班研讨，当前不再伪造“至少两个”数量下限。
- `KP-016` 的“不少于800字”由任务三 canonical 明确支持；“原句—语言/戏剧形式—人物或时代功能—判断”作为可执行札记程序，未冒充教材硬性栏目标注。
- 正文事实、学习提示、任务、课标和教师用书 unknown 边界分栏保持；课标任务群10及学业质量4-3使用现行受控名称，仅作定位，不判定本卡完整水平。
- 高考关系保持结构化 `N/A / M0 / N/A`，未挂教材EV或未登记真题；纵向关系为有理由的 `N/A`。

## 4. R01—R10 判定

| 规则 | 触发？ | 独立结论 |
|---|---|---|
| R01 | 否 | 题名、老舍作者、第一幕时间地点、人物与事件、后段正文和课标术语均与 canonical 载体一致；返工未引入事实错误。 |
| R02 | 否 | `18/18` EV均有适配 Source/Artifact、可回查 locator 和短引；EV-010—013晚页链已闭合，学习提示和正文引用均可定位。 |
| R03 | 否 | 两个正文子文本完整覆盖第一幕正文物理页60—70，学习提示、U02任务、课标、M0、纵向和教师用书边界模块齐全。 |
| R04 | 否 | 正文、学习提示、任务、课标、教师用书缺源和项目建议已分层；KP-015数量约束已明确降为项目建议属性。 |
| R05 | 否 | `18/18` KP均具备合法主维度、受控知识类型、四层主归属、判定理由、证据ID和置信状态。 |
| R06 | 否 | 高考栏保持 `M0`，无未登记真题、答案/评分资料或M1—M3直接衔接断言。 |
| R07 | 否 | 正式证据仅消费已登记且 hash 匹配的课8教材、U02任务包和现行课标 canonical Artifact。 |
| R08 | 否 | 卡片、ledger、Source/Artifact、版本、2子文本、18 KP、18 EV及 validator SHA 一致；REWORK 后新版本绑定闭合。 |
| R09 | 否 | 使用现行课标“ 中国现当代作家作品研习”等受控任务群名称，没有改写成固定课型或教法。 |
| R10 | 否 | 人文/语言双维度均有文本实践依据；学业质量4-3仅作能力定位，未机械铺满核心素养或标注单课完整水平。 |

## 5. P0/P1/P2

`P0/P1/P2 = 0/0/0`。

上一版本的正文漏页、学习提示错页、EV-010—013 locator 断链和 KP-015 数量边界均已在 v0.2.1 明确修复并回归通过。本轮未发现新的事实、证据、枚举、字段、版本、来源或教学边界缺陷。

## 6. 2.0-textbook 量规评分

| 维度 | 权重 | 单项门槛 | 得分 | 复核依据 |
|---|---:|---:|---:|---|
| 证据链与可追溯性 | 25 | 21 | 24.5 | `18/18` EV均有 canonical Artifact、物理/切页、短引和核验元数据；所有晚页 EV 已闭合，复合短引的宽页范围可回查，保守扣0.5。 |
| 事实与术语准确性 | 20 | 18 | 19.5 | 题名/作者、茶馆人物与冲突、任务群10、4-3边界均准确；返工未引入事实漂移，扣0.5用于部分研究性解释的保守表达。 |
| 字段完整与知识粒度 | 15 | 12 | 15.0 | `2/2`正文子文本、`18/18` KP、`18/18` EV、任务/课标/教学/M0/N/A/教师用书模块和版本记录完整。 |
| 双维度与母题质量 | 15 | 12 | 14.5 | 人文线覆盖茶馆公共空间、贫困、权力与时代；语言线覆盖京味、台词、动作、静默和横断面结构，保留戏剧文本特异性，扣0.5用于综合概括的谨慎度。 |
| 四层与高考映射 | 10 | 8 | 10.0 | 每个KP有受控四层主归属及理由；课标定义可回查；高考严格M0。 |
| 纵向贯通 | 8 | 6 | 8.0 | 当前无双方 accepted 的跨课/跨册逐边证据时，合法保持有理由的N/A。 |
| 教学可用性与表达 | 7 | 5 | 7.0 | 时间—空间—人物—冲突表、台词—动作配对和语言札记路径可直接用于备课；教材/项目/教师用书边界清楚。 |
| **合计** | **100** | **85** | **98.5** | 所有单项和总分门槛达到；R01—R10及P0/P1/P2均通过。 |

## 7. 独立第二复审决定

**决定：`pass`。** `CARD-X3-U02-04` v0.2.1 / SHA `c2f58ee65c5d8161e9751eac65b884675da0ef575766a5d6d718ad626547e8b6` 通过返工后的独立第二复审；R01—R10 全部未触发，`P0/P1/P2=0/0/0`。当前 ledger 状态仍为 `linted`，本报告不执行 G4/状态迁移；只有同一最终 SHA 的主审与第二复审配对并由协调者写回 transition 后，才可转为 `accepted`。

## 8. 可复现绑定与报告校验

- 卡片：`work/knowledge/选择性必修下册/cards/CARD-X3-U02-04.md`；v0.2.1；SHA `c2f58ee65c5d8161e9751eac65b884675da0ef575766a5d6d718ad626547e8b6`。
- ledger：`work/knowledge/_meta/deliverables.jsonl`；SHA `6529cd7994e76a7773c6c2c8d1fc424b345416d1cd021582b15101230933fc02`；CARD-X3-U02-04 为 v0.2.1/`linted`。
- validator：`work/knowledge/_meta/validation_reports/archive/VAL-20260808-232804+0800.json`；SHA `d3b4e22e2bc3c90205573449a43d308189c917c747f7c781a5a2f22192046968`；结果 `passed`、0 errors、`hash_verification=true`。
- canonical Artifact：`ART-PKG-X3-009-PDF`=`fa25db433fdda0a9468321de7cada4e84b590f3436125db92f683830957f5bc2`；`ART-PKG-X3-010-PDF`=`ad805e6349d35afe4845ecb463a4cc062d6add372daffe5f655fc464d40b0a7c`；`ART-CURR-2020-PDF`=`7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- rubric SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`；taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b`。
- 报告 SHA-256按 front matter 的 `report_sha256_scope` 计算：将 `report_sha256` 置空后对 canonical 报告字节求 SHA，再回填该值；另行记录实际文件 SHA。
