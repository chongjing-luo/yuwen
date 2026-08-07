# 四川适用高考语文真题清洗、题组切分、题型汇编与知识点研究设计

> 版本：1.0.0-design  
> 日期：2026-08-07  
> 状态：经三路独立审查后冻结，等待用户审阅  
> 适用语料：2008—2024 年四川考生实际使用的语文高考试卷

## 一、最终决策

采用“不可变证据层—结构化事实层—Markdown 视图层—研究解释层”四层架构：

```text
原始 PDF + MinerU 快照（不可变证据）
                  ↓
页块 IR + accepted 结构化记录（唯一机器真源）
                  ↓
清洗整卷 MD ↔ 题组 MD ↔ 题型汇编 MD（确定性生成、双向链接）
                  ↓
题型综合研究 + AnswerUnit + EKP-occurrence + EKP-family
                  ↓
教材 KP 映射（后续独立阶段）
```

关键决定如下：

1. 一个完整材料题组对应一个物理 Markdown 文件；小题和子问在题组内拥有独立稳定 ID。
2. MinerU `full.md`、JSON、图片和原始 PDF 永不原位修改。
3. 不能只清洗 `full.md`；页块 IR 必须同时读取 MinerU 正常块、`layout.json` 中的 discarded blocks 和 PDF 页面。2012 年四川卷诗题“子规【注】”已被 MinerU 误标为页码并从 `full.md` 丢失，证明 discarded 不等于可删除。
4. accepted 结构化记录是唯一机器真源；清洗整卷、题组和题型汇编 Markdown 都是可审阅、可双链、可确定性重建的视图。
5. 空白卷承担题文主链；解析卷只建立独立的答案/解释链。解析卷不得覆盖题干，也不得被称为官方答案、标准答案或评分标准。
6. 每个题组设一个主类型；每个小题允许材料类型、任务动作、考查对象和作答形态等多标签。
7. 同题型汇编包含完整材料、相关小题、答案和解析，但全部自动生成，禁止手工修改。
8. 真题知识点不直接复用教材 `KP`。先建立 AnswerUnit、真题考点实例 `EKP-occurrence` 和跨年考点族 `EKP-family`，再在后续阶段建立 M0—M3 关系。
9. 四年校准不足。结构校准使用 2008、2011、2013、2016、2018、2024 六年；2021 作为冻结后的独立留出测试；2012、2017 另提供清洗安全金标页。
10. 当前不得立即全量执行。必须先关闭旧语料消费者、MinerU 断点续跑和来源登记三个前置 P0。

## 二、当前基线与事实边界

### 2.1 已确认输入

| 项目 | 当前数量或状态 |
|---|---:|
| 原始 PDF | 36 份 |
| 主批次 PDF | 34 份：17 空白卷 + 17 解析卷 |
| 备用或重复 PDF | 2 份：2017 空白卷替代版、2018 空白卷重复件 |
| MinerU 主批次 | 34/34 完成 |
| `full.md` | 34 份 |
| 带 `page_idx` 的 content list | 34/34 |
| 推广污染 | 34/34 |
| 图片资产 | 225 个；223 处引用；2 个未引用；当前引用 0 断链 |
| 来源真实性 | 主批次 34 条全部为 `unverified` |
| 正式知识库中的考试 Source/Artifact/Relation | 0 |
| 真题专用 Question/AU/EKP/Calculation Schema | 0 |

正式语料目录为：

```text
Data/2008-2024·（四川）语文高考真题/
```

旧目录 `Data/reference/gaokao/` 仅为历史候选，不得再被正式生成器或校验器消费。

### 2.2 当前不能声称的事实

- 17 对（34 份）主材料已经与官方原卷逐页一致；
- 解析卷答案、解析或评分思路具有官方权威性；
- 2017 无后缀版一定优于备用版；
- 去水印可以全自动、无损完成；
- 空白卷和解析卷可以仅按页码、位置或题号自动可靠对齐；
- MinerU `done` 表示题文完整准确；
- 当前的四份真题草稿、M0 映射骨架或知识库“0 errors”报告已经达到正式验收条件。

### 2.3 前置阻断问题

以下问题关闭前禁止批量重跑或正式发布：

1. `scripts/generate_summary_exam_drafts.py` 和 `scripts/validate_gaokao_corpus.py` 仍消费旧高考目录，存在双真源风险。
2. `scripts/process_sichuan_gaokao_mineru.py` 重跑时会先把已有记录重建为 `pending`，随后因 `full.md` 已存在而跳过，可能把已完成批次降级为 `partial_failed`；脚本还缺少并发锁和原子 manifest 提交。
3. 36 份原始 PDF 尚未全部进入统一登记；两个备用/重复文件只写在说明中，没有显式 Artifact 和关系记录。
4. 当前清单没有 `exam_id`、`pair_id`、稳定题组/小题 ID、答案关系和页段 locator。
5. 当前知识库没有 Question、AnswerUnit、EKP、EKP-family、Calculation 和题型研究 Schema。

## 三、目标、研究问题与范围

### 3.1 总目标

建立一套可核验、可复算、不过度推断、可由教师和 Agent 直接使用的 2008—2024 四川适用高考语文题库，使任一正式题文、答案说明、题型结论和知识点判断都能回到原始 PDF 的准确页段。

### 3.2 分目标

| 目标 | 可验收结果 |
|---|---|
| T1 输入可信 | 36/36 PDF 登记，角色、哈希、页数、版本关系和权威边界明确 |
| T2 清洗可逆 | 34 份主文档完成页块级清洗；任何删除、校订和图像处理都有 ledger |
| T3 题组完整 | 每个印刷小题恰好属于一个题组；材料、选项、注释、图表和分值完整 |
| T4 答案可追溯 | 解析内容以 AnswerUnit 对齐题组/小题；不确定项不强配 |
| T5 分类稳定 | 题组主类型、小题多标签和历史栏目别名有版本化代码本 |
| T6 汇编可重建 | 相同题型完整汇编可从 accepted 记录确定性生成，且双链 100% 有效 |
| T7 综合可复算 | 跨年统计有分子、分母、去重键、标签权重、输入 ID 和输出哈希 |
| T8 考点可核验 | EKP 原子化、证据充分、边界一致，未把第三方解析冒充官方评分 |
| T9 后续可映射 | EKP 与教材 KP 分离；双方 accepted 后才建立 M0—M3 关系 |

### 3.3 研究问题

1. 2008—2024 四川卷、全国Ⅲ卷、全国甲卷的题组结构如何变化？
2. 相同材料/文体下，任务动作、作答形态和答案证据要求如何变化？
3. 哪些 EKP-family 跨命题制度持续出现，哪些只在特定时期出现？
4. 多标签题型在不重复计数的前提下，其出现率、构成比和分值构成如何？
5. 哪些真题考点可以与教材 KP 建立 M1/M2/M3，哪些必须保持 M0？

### 3.4 本阶段纳入范围

- 36 份原始 PDF 的清点、身份和版本关系登记；
- 34 份主版本 MinerU 产物的不可变快照与页块 IR；
- 空白卷、解析卷的角色分离清洗；
- 题组、小题、答案单元、资产、类型和双链；
- 两级题型汇编、题型综合研究和 EKP；
- 为后续教材 KP 映射建立接口和门禁。

### 3.5 不纳入或延后

- 不对扫描 PDF 原位去水印、重编码或覆盖；
- 不使用生成式补图或猜测式修复还原题图；
- 不把第三方解析提升为官方评分标准；
- 不在 Question/AU/EKP 未 accepted 时建立正式 KP 映射；
- 不以四卷、六卷或单一命题制度结果代表 17 年整体；
- 不从描述性变化推出命题因果结论。

## 四、目录、产物和唯一真源

### 4.1 数据衍生产物

```text
Data/2008-2024·（四川）语文高考真题/
├── *.pdf                              # 原始输入，不修改
├── manifest.json                      # 现有摄取清单，后续迁移
├── mineru_result/                     # MinerU 不可变快照
└── exam_extract/
    ├── _meta/
    │   ├── schemas/
    │   ├── registry/
    │   │   ├── sources.jsonl
    │   │   ├── artifacts.jsonl
    │   │   └── source_relations.jsonl
    │   ├── accepted/
    │   │   ├── documents.jsonl
    │   │   ├── blocks.jsonl
    │   │   ├── question_groups.jsonl
    │   │   ├── questions.jsonl
    │   │   ├── answer_units.jsonl
    │   │   ├── classifications.jsonl
    │   │   ├── assets.jsonl
    │   │   ├── links.jsonl
    │   │   └── calculations.jsonl
    │   ├── id_ledger.jsonl
    │   ├── cleaning_ledger.jsonl
    │   ├── issues.jsonl
    │   ├── exam_taxonomy.yaml
    │   └── runs/<run_id>/<doc_id>/
    ├── cleaned/<exam_id>/
    │   ├── <exam_id>-paper.cleaned.md
    │   └── <exam_id>-analysis.cleaned.md
    ├── question_groups/<exam_id>/<group_id>.md
    ├── type_collections/
    │   ├── by_group_type/<type_id>.md
    │   └── by_question_type/<type_id>.md
    └── assets/<exam_id>/
```

### 4.2 研究解释产物

```text
work/knowledge/高考分析/
├── 整卷研究/<exam_id>.md
├── 题型研究/<type_id>.md
├── 真题考点/<exam_id>/<group_id>.md
└── MAP-EXAM-KP.md                    # 后续阶段
```

`Data` 保存来源事实和确定性衍生视图；`work` 保存研究解释、教学含义和知识映射。研究解释不得反向覆盖题文事实。

### 4.3 权威边界

| 层 | 是否可手工修改 | 权威责任 |
|---|---|---|
| 原始 PDF | 否 | 最终视觉核对入口；当前真实性仍需核验 |
| MinerU 快照 | 否 | OCR 候选和页块定位，不是终审题文 |
| run 分片 | 仅当前任务写 | 候选结构、清洗建议和异常 |
| accepted JSONL | 只能经审核提交 | 唯一机器真源 |
| cleaned/group/collection MD | 否，重新生成 | 人工审阅和双链视图 |
| `work` 研究稿 | 可以，但须引证 accepted ID | 研究解释和教学使用 |

对 Markdown 发现的题文错误必须形成 correction proposal，经 PDF 核对后写入 accepted 记录，再重新生成视图；不得直接修改生成文件。

## 五、来源、Artifact 与精确定位

### 5.1 36 份原件全部登记

所有 PDF 均建立 Artifact，包括主版本、2017 备用版和 2018 重复件。关系至少增加：

- `answer_for`：解析/答案材料对应题卷；
- `analysis_for`：第三方讲解对应题卷；
- `duplicate_of`：字节或内容重复；
- `alternate_variant`：相同卷别的替代版；
- `derived_from`：OCR、清洗、题组和汇编派生；
- `aligned_span_of`：解析页段与题卷题目页段的对齐。

未核验 Artifact 不得成为 canonical。Source Schema 必须允许 `canonical_artifact_id: null`，并强制：

```text
is_canonical = true ⇒ authenticity_status = verified
```

### 5.2 角色与主张矩阵

| 字段或主张 | 首选来源 | 允许的回退 | 禁止事项 |
|---|---|---|---|
| 题文、选项、题号、分值 | 空白卷 PDF | 解析卷补缺，标 `source_fallback` | 解析卷静默覆盖题文 |
| 答案 | 已核验答案来源 | 当前解析卷，明确第三方/未核验 | 称官方答案或标准答案 |
| 解析 | 解析卷 | 无 | 称官方评分说明 |
| 官方评分点 | 官方 scoring Artifact | 无则为空 | 从解析文字反推为官方评分点 |
| 题型与 EKP | 项目研究解释 | 题文和答案证据 | 冒充试卷明示分类 |

### 5.3 Locator 最小字段

每个 accepted 题文、答案单元和证据至少保存：

```yaml
pdf_artifact_id: ART-...
pdf_page_1based: 3
ocr_artifact_id: ART-...
page_idx_0based: 2
block_id: ...
bbox: [x0, y0, x1, y1]
page_size: [width, height]
coordinate_origin: top_left
coordinate_unit: pixel
extractor: MinerU
extractor_version: ...
input_sha256: ...
```

`full.md` 行号和文本片段只作为辅助定位，不得是唯一 locator。

### 5.4 多父血缘

Artifact 的 `derived_from` 不再使用单个自由字符串，改为：

```yaml
input_artifact_ids: []
transform_activity_id: ACT-...
```

TransformActivity 记录工具、版本、参数、清洗规则版本、删除 mask、输入哈希、输出哈希、执行者和时间。

## 六、稳定 ID 与状态

### 6.1 ID 体系

```text
整卷：      EXAM-2008-SC
文档：      DOC-2008-SC-PAPER / DOC-2008-SC-ANALYSIS
题组：      QG-2008-SC-001
小题：      EXAM-2008-SC-Q001
子问：      EXAM-2008-SC-Q011-A
答案单元：  AU-2008-SC-Q011-A-01
考点实例：  EKP-O-2008-SC-Q011-A-01
考点族：    EKP-F-CLAS-TRANS-001
计算：      CALC-<type_id>-<version>-001
```

卷别码固定：

- `SC`：2008—2015 四川自主命题；
- `NC3`：2016—2020 全国Ⅲ卷；
- `NCA`：2021—2024 全国甲卷。

### 6.2 印刷题号不等于身份

2016—2020 的转载版可能把官方 1—3 题重排成“题组 1 + 子题（1）—（3）”。因此同时保存：

- `printed_label`：页面可见题号；
- `source_local_label`：当前载体局部编号；
- `normalized_question_number`：核对后的逻辑题号；
- `display_order`：卷内展示顺序。

稳定 ID 只能在人工核对题号、分值和材料边界后由单一 ID ledger 签发。文本哈希用于漂移检测，不充当 ID。

### 6.3 状态分层

MinerU `done` 只表示 `ocr_generated`。文档状态至少区分：

```text
ingest_complete
→ lineage_verified
→ authority_verified 或 authority_unverified
→ ocr_generated
→ content_reviewed
→ split_reviewed
→ classified_reviewed
→ accepted
```

来源未核验时可以完成内部清洗和结构研究，但不得以正式官方证据发布。

## 七、页块 IR 与可逆清洗

### 7.1 页块 IR

页块 IR 由原 PDF、content list、layout/model JSON 和 `full.md` 联合构建。每个 PDF 页面上的块必须且只能被解释为以下之一：

```text
document_header / section_header / passage / note / figure / table /
question / option / answer / explanation / page_furniture /
promotion / uncertain
```

`discarded_blocks` 必须进入候选 IR，不能因 MinerU 标签而自动丢弃。

### 7.2 允许自动执行的清洗

- Unicode NFC、换行和空白规范化；
- 明确的 Markdown 标题层级修复；
- 已核验固定推广块和推广图片的排除；
- 已核验页眉、页脚和孤立页码的排除；
- 图片相对路径重写和资产命名空间化；
- 不改变文字内容的选项、表格和段落重排。

### 7.3 必须人工核对的修改

- 古文、诗词、专名、数字、分值、答案和作文材料；
- 题干、选项或段落的文字增删；
- discarded block 恢复；
- 跨页材料合并；
- 图表文字或注释恢复；
- 空白卷与解析卷冲突裁决。

### 7.4 禁止的自动删除依据

不得仅依据以下任一条件删除内容：

- `header/footer/page_number/aside_text` 标签；
- 页面边缘位置；
- 跨文档重复频率；
- 图片哈希重复；
- OCR 置信度低；
- 出现在作文之后。

这些条件只能产生 `promotion_candidate` 或 `page_furniture_candidate`，最终删除需要规则组合、金标验证或人工确认。

### 7.5 水印和图像

文本层水印片段可在清洗视图中排除；扫描图像中与正文处于同一像素层的斜向水印不得自动 inpaint。必要题图允许无损复制或经审核裁边；任何像素变换均登记 mask、工具、参数和输出哈希。

### 7.6 清洗 ledger

每个清洗动作记录：

```text
action_id、doc_id、输入 block/span、操作类型、原始文本或资产哈希、
候选输出、规则版本、自动/人工、执行者、审核者、状态、时间
```

状态为 `auto_cleaned / needs_review / verified / conflict / rejected`。

## 八、题组切分与答案对齐

### 8.1 题组定义

题组是共享同一材料或同一连续作答情境的一组小题：

- 共享现代文材料的若干小题为一个题组；
- 文言文材料、相关小题和翻译子问为一个题组；
- 一首诗词及其小题为一个题组；
- 同一语言材料下的多个语言运用题为一个题组；
- 独立语言基础题、默写题或作文各自形成题组。

题组文件包含完整材料一次，不为每个小题复制材料。

### 8.2 结构字段

每个题组至少包含：

```text
group_id、exam_id、section_path、historical_section_label、paper_spans[]、
analysis_spans[]、material_blocks[]、question_ids[]、asset_ids[]、
score_total、primary_group_type、secondary_tags[]、status、version、content_hash
```

每个小题分别记录题干、选项、分值、作答形态、任务动作、题文 locator 和复核状态。

### 8.3 答案对齐

答案对齐不得使用单一近邻规则。匹配证据包括：

- 题号或题号范围；
- 材料标题或文本指纹；
- 选项答案模式；
- 页码与顺序；
- 分值；
- `【n题详解】`、附录答案或题组答案结构。

允许一题多 AnswerUnit、多版本答案、答案缺失和 `review_required`。自动匹配只能生成候选；accepted 对齐必须人工复核。

### 8.4 AnswerUnit

AnswerUnit 是最小独立计分或独立评价要求：

- 客观题通常一个小题对应一个 AU；
- 主观题若有可分别计分的两个要求，拆成两个 AU；
- 没有官方评分资料时，解析卷中的答案要点只能称“解析给出的答案单元”，不能称官方评分点。

## 九、题型本体与自动汇编

### 9.1 四轴分类

```text
内容领域 → 材料/文体 → 任务动作 → 作答形态
```

内容领域：

- `LANG`：语言文字积累与运用；
- `MODR`：现代文阅读；
- `CLAS`：古代诗文阅读；
- `MEM`：名篇名句默写；
- `WRIT`：写作。

材料/文体包括但不限于：信息类、论述类、实用类、小说、散文、多材料比较、文言文、诗、词、曲、材料作文等。

任务动作受控为：

```text
识记、辨析、理解、提取、筛选、概括、推断、分析、鉴赏、
比较、评价、探究、翻译、断句、补写、改写、表达、写作
```

作答形态受控为：

```text
单项选择、多项选择、填空、简答、翻译、开放探究、整篇写作
```

### 9.2 主标签与多标签

- 每个题组恰有一个主材料类型；
- 每个小题恰有一个主任务类型；
- 可以增加辅助动作、考查对象、情境和知识标签；
- 历史栏目名原样保存，并通过 alias 映射到统一类型；
- 分类理由必须引用题干动作和材料特征。

### 9.3 两级汇编

1. `by_group_type`：按论述类、文学类、文言文、古诗词、语言材料、作文等完整题组汇编。
2. `by_question_type`：按人物形象、论证分析、炼字、翻译、语病、补写等小题类型汇编。

小题汇编仍呈现完整共享材料和整组上下文，但醒目标出本汇编关注的小题。

汇编仅保存 accepted ID、版本和哈希引用；Markdown 正文由 assembler 展开生成，不形成第二事实源。

## 十、Markdown 双链

### 10.1 链接方向

```text
cleaned.md 的题组锚点 ↔ question_group.md
question_group.md ↔ 它所属的所有 type_collection.md
question_group.md ↔ work 中的题型研究/EKP研究稿
```

原始 `full.md` 不修改；其反向派生关系保存在 `links.jsonl`。`cleaned.md` 提供到原始 PDF、OCR 文件和对应页码的正向链接。

### 10.2 生成区

自动区使用边界标记：

```markdown
<!-- AUTO:SOURCE START content_hash=... -->
...
<!-- AUTO:SOURCE END -->

<!-- AUTO:BACKLINKS START -->
...
<!-- AUTO:BACKLINKS END -->
```

所有生成 Markdown 均禁止手工改动；校验器通过哈希检测漂移。

### 10.3 链接验收

文件、相对路径、锚点、ID、版本和内容哈希必须 100% 有效。任何断链冻结题型汇编和下游研究稿。

## 十一、题型综合研究与真题知识点

### 11.1 每类题型研究稿

每个至少含一个 accepted 实例的主类型都生成研究稿，包含：

1. 类型定义、纳入和排除标准；
2. 适用年份、命题制度、题组数、小题数、AU 数和分值；
3. 四川卷、全国Ⅲ卷、全国甲卷的结构变化；
4. 材料和文本特征；
5. 设问表达及其历史变体；
6. 任务动作组合；
7. 答案证据类型和组织方式；
8. 干扰项机制或主观题常见失误；
9. 难点来源；
10. EKP-family 及实例；
11. 教学使用建议和教材映射候选；
12. 来源局限、OCR 冲突和未决问题；
13. 可复算统计和 CALC-ID。

样本少于 3 个 AU 的类型标记 `evidence_sparse`，可以描述实例，不得声称趋势或高频。

### 11.2 EKP 两级结构

`EKP-occurrence` 表示一个 AU 中的：

```text
能力动作 × 考查对象 × 条件或评价标准
```

它至少记录：一句话原子考点、主动作、对象、条件、题干证据、答案证据、判定理由、来源等级和置信状态。

`EKP-family` 是跨题归并的规范考点族，必须给出定义、纳入/排除规则、正例、反例、版本和审核记录。不能仅凭措辞相近自动合并。

### 11.3 三种频次口径

三种指标不得混用：

1. 出现率：`含标签的唯一 AU 数 ÷ 合格 AU 总数`。多标签之和可以超过 100%，必须称“出现率”。
2. 构成比：只统计主标签，合计必须为 100%。
3. 分值构成：每个 AU 的标签权重之和为 1，按 `AU 分值 × 标签权重` 汇总。

每个正式统计保存：

```text
CALC-ID、输入 ID 集合、命题制度范围、计数单位、分子、分母、
去重键、标签权重、公式或代码版本、输出和输出哈希
```

### 11.4 教材 KP 映射接口

Question/AU/EKP 和教材 KP 都 accepted 后，才建立独立 Mapping：

```text
Question/AU/EKP-ID、KP-ID、M0—M3、真题侧证据、教材侧证据、
映射理由、规则版本、审核状态
```

M1/M2/M3 必须有双向证据；M0 只表示当前无可靠关联，不携带 KP-ID。每个教材 KP 接受反向核对，但不强迫建立正向映射。

## 十二、执行模块与并发规则

### 12.1 模块边界

```text
registry/schema
→ block_ir
→ reversible_cleaner
→ question_segmenter
→ stable_id_issuer
→ answer_aligner
→ asset_registry
→ classifier
→ review_gate
→ accepted_store
→ deterministic_assembler
→ type_analyzer / ekp_extractor
→ validator/orchestrator
```

每个模块只读上游并写自己的 run 分片；accepted store 和共享 ledger 由单一协调者提交。

### 12.2 多 Agent 并发

- Agent 按 `run_id/doc_id` 或题组分片写入独立目录；
- 禁止并发修改共享 manifest、ID ledger、taxonomy 或 accepted JSONL；
- 稳定 ID 签发、Schema/词表变更和最终合并只有协调者执行；
- 合并使用输入哈希和预期上游版本进行 compare-and-swap；
- 失败分片可单独重跑，不能覆盖已 accepted 版本；
- 每个 Agent 的生产、主审和第二复审角色分离。

### 12.3 确定性与恢复

- 所有生成先写 run/staging，校验通过后原子发布；
- MinerU 重跑必须保持已完成状态，不得因跳过已有文件而状态回退；
- 并发使用锁、唯一 `.part` 和原子 manifest 替换；
- 同一输入、工具版本、规则版本和参数必须生成相同结构和内容哈希；
- 汇编只消费 accepted 结构化记录，不回读手工 Markdown。

## 十三、阶段计划

### G0：范围与阻断修复

1. 冻结 2008—2024、三种命题制度和 36 份文件清单。
2. 让所有正式消费者停止读取旧 `Data/reference/gaokao/`。
3. 修复 MinerU resume、状态回退、锁和原子 manifest 写入；当前 34 份结果不重跑。
4. 标记旧四份真题草稿和旧映射骨架为 legacy，不得进入新流水线。

### G1：来源与 Schema

1. 登记 36/36 PDF、34 套 MinerU 快照和版本关系。
2. 修订 Source/Artifact/Relation Schema，支持未核验无 canonical、多父血缘和结构化 transform。
3. 新增 Document、Block、QuestionGroup、Question、AnswerUnit、Classification、Asset、EKP、EKP-family、Calculation、Link、Review Schema。
4. 为 validator 添加正例和故意断链、错配、重复计数、未 accepted 依赖等负例。

### G2：端到端垂直切片

先用 2013、2016、2024 三年建立完整吞吐：

```text
PDF → IR → 清洗 → 题组 → 答案对齐 → 分类 → accepted → 双链汇编
```

垂直切片用于证明模块接口，而不是冻结全量规则。

### G3：结构校准与清洗安全金标

- 结构校准：2008、2011、2013、2016、2018、2024；
- 清洗安全页：加入 2012“子规【注】”、2017 备用版/页边内容、跨页材料、图表、注释、斜向水印和“绝密★启用前”；
- 两名独立评审者完成题组边界、题型和 EKP 校准；
- 达到门槛后冻结 Schema、清洗规则、ID 规则和 taxonomy 1.0。

### G4：独立留出测试

用未参与规则设计的 2021 年空白卷和解析卷端到端运行。留出失败必须回到 G3 修订并重新测试，不得只为 2021 增加一次性特例后直接放行。

### G5：17 年全量生产

1. 34 份主文档先全量 dry-run；
2. 逐卷处理异常队列和 PDF 目视核对；
3. 题号、题组、分值、答案关系和资产全部 accepted；
4. 生成 cleaned、question_groups 和双链；
5. 全量结构覆盖测试通过后生成题型汇编。

### G6：题型综合与 EKP

1. 生成全部主类型汇编；
2. 建立 AU、EKP-occurrence 和 EKP-family；
3. 执行多标签统计和 CALC 复算；
4. 完成每类题型研究稿；
5. 独立双审并清零缺陷。

### G7：教材映射（后续）

只消费 accepted Question/AU/EKP 和 accepted 教材 KP，建立 M0—M3 关系和反向核对表。

单工程师预估为 3—5 人周；多 Agent 可缩短处理时间，但 PDF 目视核对、答案对齐和独立评审不能线性并行压缩。

## 十四、硬性否决项

任一项触发即不评分并冻结受影响下游：

1. 原始 PDF、MinerU 快照被覆盖、重编码或无法重算原哈希；
2. 伪造 Source、Artifact、路径、ID、版本、页码或发布主体；
3. 未核验 Artifact 被标为 canonical；
4. 仅因版面标签、页边位置、重复频率或低置信度删除真实内容；
5. 漏题、重题、错序、材料边界错误、题号或分值错误；
6. 题文、选项、注释、图表或答案无法定位到原 PDF 页段；
7. 解析卷覆盖题文，或第三方解析被称为官方/标准答案/评分标准；
8. 自动答案对齐的不确定结果直接进入 accepted；
9. 题组、Question、AU、EKP 无稳定 ID，或可独立计分要求未拆成 AU；
10. 生成视图被手工修改，或汇编回读手工 MD 形成第二真源；
11. 多标签统计未声明计数单位、分母、去重键和权重；
12. 用局部年份声称 17 年趋势，混合命题制度不分层，或把描述性结果解释为因果；
13. 使用未 accepted 上游建立汇编、统计、EKP-family 或教材映射；
14. 文件、锚点、关系、版本或内容哈希断裂；
15. 无独立评审记录或开放 P0/P1/P2 未清零却进入 accepted/published。

## 十五、可量化验收门槛

### 15.1 二元阶段门

| 指标 | 门槛 |
|---|---:|
| PDF 库存登记 | 36/36 |
| 原 PDF 重算哈希一致率 | 100% |
| 未核验 Artifact 被设为 canonical | 0 |
| 派生 Artifact 输入、工具、参数、输出哈希完整率 | 100% |
| 金标真实内容与删除 mask 交集 | 0 |
| 金标内容保留率 | 100% |
| accepted 题文、选项、注释、图表、分值目视核对率 | 100% |
| locator 打开正确 PDF 页并命中区域 | 100% |
| 每个印刷小题恰属一个题组 | 100% |
| 无解释的未归属正文块或重叠正文块 | 0 |
| accepted 空白卷—解析卷配对准确率 | 100%；不确定项不强配 |
| 非官方材料误写为官方/标准答案/评分标准 | 0 |
| 资产引用与题型汇编链接有效率 | 100% |
| 汇编 ID、版本、内容哈希一致率 | 100% |
| 自动题组边界金标 F1 | ≥0.98 |
| EKP 边界金标 F1 | ≥0.90 |
| 题型双评 Cohen’s κ | ≥0.85 |
| EKP 标签双评 Cohen’s κ | ≥0.80 |
| 后续 M 等级双评 Cohen’s κ | ≥0.80 |
| 同输入重放结构和内容哈希一致率 | 100% |
| 自动统计 CALC 复算一致率 | 100% |
| 双链文件/锚点/ID 有效率 | 100% |
| 随机正式结论 2 分钟内回溯成功率 | ≥95% |

### 15.2 最终研究包评分（100 分）

二元阶段门全部通过后才评分。两名评审者必须对同一最终版本分别达到总分 92，且每个维度达最低分；平均分不能补救任一评审未通过。

| 维度 | 权重 | 最低分 | 必备证据 |
|---|---:|---:|---|
| 研究范围与主张边界 | 8 | 7 | 语料—问题—产物矩阵、纳入排除、制度分层 |
| 来源与语料完整性 | 12 | 11 | Source/Artifact/Relation、哈希、角色、权威状态 |
| 题文忠实度与题组覆盖 | 16 | 15 | Question 清单、PDF locator、题号/分值/材料审计 |
| 答案对齐与 AnswerUnit | 12 | 11 | answer_for、AU、缺失/冲突和人工复核记录 |
| 题型与 EKP 编码质量 | 16 | 14 | taxonomy、EKP 记录、F1/κ、冲突裁决 |
| 题型综合与频次研究 | 14 | 12 | CALC、分子分母、去重、权重、分层和敏感性复算 |
| 可复现性与治理 | 10 | 9 | Schema/规则版本、run、状态、评审、变更影响和哈希 |
| 双链、检索与回溯 | 6 | 6 | 链接审计、定时回溯测试、典型查询 |
| 教学可用性与边界 | 6 | 5 | 题型研究稿、教学使用案例、非官方来源声明 |
| **合计** | **100** | **90** | 最终总分仍须 ≥92 |

评分约束：

- 覆盖类按合格数/应检数比例计分，不使用无法达到最低分的粗粒度五分块；
- 一个缺陷只归一个主评分维度，避免重复扣分；
- 硬约束只作门禁，不能靠其他得分补偿；
- `N/A` 必须由 Schema 预先允许并给出理由；
- 所有开放 P0/P1/P2 在 accepted 前清零。

## 十六、自动检查、人工评审与缺陷扩批

### 16.1 100% 自动检查

- Schema、枚举、ID、路径、哈希、状态迁移和 accepted 依赖；
- 页块覆盖、题号/分值、Question→AU→EKP 覆盖；
- 主标签唯一、标签权重和为 1、去重键和 CALC 复算；
- 资产、双链、锚点、版本和内容哈希；
- 确定性重放、断点恢复和并发冲突测试。

### 16.2 100% 人工主审

- PDF 视觉核对和来源适配；
- 清洗删除、discarded block 恢复、跨页材料和题图；
- 题组边界、答案对齐、AU 原子性；
- 题型、EKP、跨年综合和教学结论。

### 16.3 100% 独立双审

- 所有校准和留出样本；
- 全部正式真题题组、AU 和 EKP；
- 全部题型研究和正式频次结论；
- 后续全部 M1/M2 映射。

真题数据不使用低比例抽检代替双审。任一 P0 立即扩至受影响全批；同类 P1 出现两次，扩该结构簇为 100% 复审；重大缺陷率达到 5% 时全批返工。评审同时报告一致率。

## 十七、审查迭代记录

本设计由三名独立审查者从不同角度只读审查后修订：

| 审查方向 | 主要否决意见 | 最终修订 |
|---|---|---|
| 证据与清洗 | 全部来源未核验；discarded block 有真实题文；`full.md` 不能作终审 | 加入 36 件原件登记、页块 IR、discarded 恢复、PDF 逐项核对和不可变证据门 |
| 执行架构 | 旧目录仍被消费；MinerU resume 会状态回退；双 MD 真源不可执行 | accepted 结构化记录改为唯一机器真源；先修旧消费者/resume；生成 MD 只作视图 |
| 目标与量表 | 原量表混合不同产物；没有 AU/EKP/Calculation；多标签会膨胀 | 分离二元数据门和最终评分；增加 AU、EKP 两级、CALC 和三种频次口径 |

其他关键迭代：

- 将四年校准扩为六年结构校准、两年安全金标补充和一年独立留出；
- 将“解析卷是答案与评分思路主输入”收紧为“未核验第三方答案/解释链”；
- 将“题组 MD 是规范题文源”改为“题组 MD 是 accepted 记录的确定性视图”；
- 将物理复制到题型目录改为 ID/版本/哈希引用后自动展开；
- 将一个笼统 92 分表改为不可补偿的阶段门加最终 100 分量表。

## 十八、完成定义

本项目这一阶段只有同时满足以下条件才算完成：

1. G0—G6 全部通过，G7 明确作为后续独立阶段；
2. 36/36 原件登记、34/34 主文档完成 accepted 清洗和切分；
3. 每个印刷小题、题组、答案单元、资产和类型均有稳定 ID 与 PDF locator；
4. cleaned、题组和两级题型汇编可以从 clean checkout 确定性重建；
5. 双链、资产、版本、哈希和 CALC 100% 通过自动审计；
6. 全部正式题型研究和 EKP 完成独立双审；
7. 两位评审分别达到最终评分 ≥92、各维度过线；
8. 硬否决为 0，P0/P1/P2 为 0；
9. 任何正式结论可回到 accepted ID，并可在两分钟内打开正确 PDF 页段；
10. 未核验来源继续保持明确边界，不因清洗和结构化而被提升为官方权威来源。

达到以上条件后，才能开始正式的“真题 EKP—教材 KP”映射与全局知识地图更新。
