# CARD-X1-U03-02 v0.2.2 独立第二复审

## 1. 结论

- `review_role`: `secondary`
- `reviewer`: `rubric_design/u03_02_secondary`
- `review_round`: 2
- `deliverable_id`: `CARD-X1-U03-02`
- `artifact_version`: `0.2.2`
- 唯一绑定内容 SHA：`edc8cd8663301d9ff9c5395e7e7e33c1f2520148a18cf8561304bb11eff22cee`
- 对象首 SHA：`edc8cd8663301d9ff9c5395e7e7e33c1f2520148a18cf8561304bb11eff22cee`
- 对象末 SHA：`edc8cd8663301d9ff9c5395e7e7e33c1f2520148a18cf8561304bb11eff22cee`
- `R01—R10`: 全否
- `P0/P1/P2`: `0/0/0`
- 七维总分：`100.0/100`
- `decision`: `pass`
- 边界：本结论只闭合当前 SHA 的 DG3 第二复审，不写回 card、ledger、transition，不等同于 `accepted` 或 DG4 receipt。

本复审从零建立分母；封存前未搜索、打开或读取本卡任何旧/新 primary 或 secondary 报告，也未复用既有分数、R/P 或结论。唯一读取的 `_reviews` 文件是任务明确指定的冻结执行矩阵。

## 2. 冻结绑定

| 对象 | 绑定值 |
|---|---|
| card | `work/knowledge/选择性必修上册/cards/CARD-X1-U03-02.md`; v0.2.2; SHA `edc8cd8663301d9ff9c5395e7e7e33c1f2520148a18cf8561304bb11eff22cee` |
| ledger | `work/knowledge/_meta/deliverables.jsonl`; SHA `de3a4b1c213749af3d420e8c4129b7951a93b773dc28348b8b8392354997baa9` |
| transition contract | `taxonomy.yaml.status_transitions`; 同 taxonomy SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b` |
| rubric | `work/knowledge/_meta/rubrics.json`; SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43` |
| taxonomy | `work/knowledge/_meta/taxonomy.yaml`; SHA `13e5e23c45c05359a5c91e360ce8bd71dbf2a841c2c6a72f1adca52bef7cbd4b` |
| 冻结执行矩阵 | `work/knowledge/_reviews/issues/u03_u04_new_sha_primary_review_matrix_book_x2_audit_20260808.md`; SHA `b654c008caa2f16a212a10fa9cc766ba23aa1593f38c9a4ff16880a98b516adc` |
| Source registry | `sources.jsonl`; SHA `fb9e5944c668558a25f047c071ea1f54131620f16eb06f277ebd2e98450fc0d4` |
| Artifact registry | `artifacts.jsonl`; SHA `36a6d972a0de9e1b8c7cac7c04b173cfcbe1c6411d8dcccf02d02ecc2e42c431` |
| Source relations | `source_relations.jsonl`; SHA `7a763d9450a60297beefd1138e8850ac690dc1cf46403f113f9a9e542d13c781` |
| split manifest | `split_manifest.jsonl`; SHA `ebb5757a568e2ae46b3fe6140d80ae9a43e2219a13a72c1b18da4ee1348804ba` |

Ledger 与 front matter 六项逐项一致：ID、路径、version、status=`linted`、owner=`root`、三个 `source_ids` 均一致。Source→canonical Artifact 三链均唯一、可解析，且 canonical、authenticity 与实际文件 SHA 一致。

## 3. Validator 绑定

- run ID：`VAL-20260808-124451+0800`
- run time：`2026-08-08T12:44:51.150010+08:00`
- command：`scripts/validate_knowledge_base.py --project-root . --report work/knowledge/_meta/validation_reports/latest.json`
- result：`passed`
- report：`work/knowledge/_meta/validation_reports/latest.json`
- report SHA：`458ce88e3c2524256b3adf1f4e14e7c5b96e733193e80a25830f4a055d013528`
- 六组机械检查错误数均为 0；本报告未将 validator passed 代替语义审查。

## 4. Canonical Artifact 与逐页目视

| Artifact | 实际 SHA | 声明/目视范围 | 结果 |
|---|---|---|---|
| `ART-PKG-X1-011-PDF` | `7c56934d7c63c2a87397289204e61f1f0471edcb96e2d4b9e81492e1f796d162` | 原物理页72—77；切分页1—6；6/6 页以 180 dpi 原图逐页目视 | pass |
| `ART-PKG-X1-014-PDF` | `6413d049be17349c7fb00c61d7ed4da85105d2f5de1a0a9cf6c7fc8d0f0858a6` | 原物理页96—97；切分页1—2；2/2 页以 180 dpi 原图逐页目视 | pass |
| `ART-CURR-2020-PDF` | `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977` | 声明物理页12—13、32—33（印刷页4—5、24—25）；4/4 页以 180 dpi 原图逐页目视 | pass |

OCR/文本抽取只用于导航；引文、版面、页脚、栏目与跨页边界均以 canonical PDF 渲染页判定。

## 5. 10 EV / 74 exact quote spans 全量核验

| EV | span 分母 | 实际页分布与 locator 复核 | 判定 |
|---|---:|---|---|
| EV-001 | 7 | 物理72/切1共6段；“选择性必修上册”位于物理73/切2页脚1段。“第三单元”位于物理72/切1页脚。卡载72—73/切1—2完整覆盖，未以宽范围掩盖越界。 | 7/7 pass |
| EV-002 | 11 | 物理72/切1共6段；物理73/切2共5段；铁栅栏对话至长凳转换顺序成立。 | 11/11 pass |
| EV-003 | 17 | 物理74/切3共3段；物理75/切4共7段；物理76/切5共7段；往事、钞票、内心动摇、改称与结束链完整。 | 17/17 pass |
| EV-004 | 8 | 物理77/切6“学习提示”第二段。 | 8/8 pass |
| EV-005 | 8 | 物理74/切3共5段，1段跨物理74—75/切3—4，物理75/切4共2段；跨页 locator 正确。 | 8/8 pass |
| EV-006 | 2 | 物理77/切6“学习提示”末段。 | 2/2 pass |
| EV-007 | 7 | 课标物理12共4段、物理13共1段、物理32共2段；另目视物理33确认任务群11连续上下文。印刷页4—5、24—25对应正确。 | 7/7 pass |
| EV-008 | 6 | 物理96/切1，任务一第1、2项及任务二第1、2项。 | 6/6 pass |
| EV-009 | 1 | 物理96/切1，任务二第1项。 | 1/1 pass |
| EV-010 | 7 | 物理96/切1共2段；物理97/切2共5段；任务三与“学写小小说”边界正确。 | 7/7 pass |

汇总：exact quote span 逐字/逐标点一致率 `74/74=100%`；span locator 有效率 `74/74=100%`；EV target 可解析率 `10/10=100%`；EV Source/Artifact 适配率 `10/10=100%`；EV 元数据完整率 `10/10=100%`；verification status 合法且为 verified `10/10=100%`。

## 6. Claim→EV 闭包与 semantic lint

复审先按 field path 建立 52 个审计单元，再把复合单元拆为 213 个最小命题：§1=28、§2=26、§3=33、§4=29、§5=70、§6=2、§7=2、§8=13、§9目标字段=10。自检、问题清单和版本记录未进分母。

| 指标 | 结果 |
|---|---:|
| 正式最小命题覆盖率 | `213/213=100%` |
| Claim→EV 目标绑定率 | `213/213=100%` |
| Claim→适配 Source→canonical Artifact 闭合率 | `213/213=100%` |
| exact span 与 locator 完整率 | `213/213=100%` |
| 合法 N/A 治理 | `4/4=100%`：教师用书、QD、纵向关系、M0 均有原因和边界 |
| 稳定 ID/路径解析率 | `34/34=100%` |
| 12 KP 完整命题有效证据率 | `12/12=100%` |

解释性命题另冻结为17组；17/17均有至少两处承担不同推理前提的独立正文/学习提示/任务证据，同段重复与 OCR/PDF 同内容未重复计数。重点包括“精神复活”的过程性判断、聂赫留朵夫自责与迟疑并存、玛丝洛娃的记忆—屈辱—求生防卫、称谓/语气与关系、双人物心理呈现、细节功能及 KP-003/004/006/007/010，均闭合到 EV-001—005、008 的不同文本前提。

结构与枚举复核：10个必填模块齐；1个正文子文本边界清楚；12个 KP ID 与10个 EV ID 唯一。KP 维度仅“人文/语言”；类型分布为事实1、概念2、程序2、策略3、解释2、价值辨析2；四层分布为必备知识3、关键能力4、学科素养3、核心价值2；置信状态为已核实8、有依据的解释4。EV 类型为Q×9、M×1，关系均 supports，状态均 verified，全部属于冻结枚举。

严格 M0：仅1条 M0 治理行；KP、真题小问与双向证据均为 N/A，不创建伪映射、不称“直接衔接”，并明确 SG-TB 前不处理真题及后续核验边界。§8.1 教材学习提示、§8.2 教师用书 N/A、§8.3 项目教学建议三层分离。核心素养同时具备 EV-007 官方定义/任务群依据和 EV-001—010 本课语言实践依据，只定位三项素养；QD 明确 N/A，未给单卡判完整水平。

## 7. R01—R10

| 代码 | 判定 | 依据摘要 |
|---|---|---|
| R01 | 否 | 作者、篇名、册次、课号、单元及页序与 canonical 一致。 |
| R02 | 否 | 74/74 quote spans、213/213最小命题及17/17解释组闭合。 |
| R03 | 否 | 模块、子文本、12 KP、10 EV与课程对接结构齐全。 |
| R04 | 否 | 正文、学习提示、单元任务、课标、教师用书 N/A 与项目建议分层清楚。 |
| R05 | 否 | 12/12 KP均有主层级、理由及支持完整命题的有效证据。 |
| R06 | 否 | 严格 M0；无真题、无非M1“直接衔接”。 |
| R07 | 否 | 本卡无上游 deliverable 消费；三条正式来源注册与 canonical hash 均闭合。 |
| R08 | 否 | 数量、ID、version、路径、ledger与Artifact链接一致，无断链。 |
| R09 | 否 | 使用现行课标及规范任务群11名称，未固定化为课型/教法。 |
| R10 | 否 | 三项素养有官方与本课双层依据；未机械铺满四项，未误判QD水平。 |

## 8. 七维评分

| 维度 | 得分/权重 | 门槛 | 检查点结果 |
|---|---:|---:|---|
| 证据链与可追溯性 | `25.0/25` | 21 | 正式主张覆盖、定位、canonical一致性、来源适配、元数据均通过。 |
| 事实与术语准确性 | `20.0/20` | 18 | 书目信息、课标术语、事实/解释边界、内外一致均通过。 |
| 字段完整与知识粒度 | `15.0/15` | 12 | 必填字段、子文本覆盖、原子化与文本特异性均通过。 |
| 双维度与母题质量 | `15.0/15` | 12 | 人文、语言及三类活动、母题双证据与学生关怀均通过。 |
| 四层与高考映射 | `10.0/10` | 8 | 主层级/理由、官方定义、严格M0、不确定性治理均通过。 |
| 纵向贯通 | `8.0/8` | 6 | 合法N/A切换为等值治理观察：不造目标、不造关系、不造递进、不造双方证据，原因与边界齐。 |
| 教学可用性与表达 | `7.0/7` | 5 | 三层提示、核心素养/QD依据、可操作性、边界/N/A均通过。 |
| **总分** | **`100.0/100`** | **85** | **七维全部过线。** |

## 9. 缺陷与决定

- `hard_rejections`: `[]`
- `P0`: 0
- `P1`: 0
- `P2`: 0
- `decision`: `pass`
- 本报告只绑定 SHA `edc8cd8663301d9ff9c5395e7e7e33c1f2520148a18cf8561304bb11eff22cee`；card 内容一旦变化，本报告立即失效并须从 Task 1 重审。
