# 高考语文真题材料（2011—2025四川覆盖批次）

本目录保存一批用于知识点迁移研究的高考语文材料。主批次按完整考试年度 2011—2025 建立；四川卷/四川适用卷映射如下：2011—2015 为四川省自主命题，2016—2020 为全国卷Ⅲ，2021—2024 为全国甲卷，2025 为全国二卷。2026 不混入主批次。

来源策略：当前可取得材料来自中国教育在线历史页面及其图片载体，登记为 `S3` 第三方转载，不冒充教育部、教育考试院或命题机构原卷。页面正文与答案分开登记；非官方答案不能继承试卷的 `S1` 等级。

## 目录

```text
html/{year}/                 原始 HTML 快照（question / answer）
pdf/{year}/                  由文章正文/试卷图片渲染的 PDF
mineru_result/{year_code_role}/ MinerU v4 解析包（full.md + JSON）
registry/                    本批次独立 Source/Artifact/Relation 登记
external/{scope}/            独立第三方候选快照及注册项（不提升权威等级）
manifest.json                每个文档的 URL、哈希、页数、校验与处理状态
```

`manifest.json` 是本批次的机器可读清单，含 HTML 快照和 PDF 的大小、SHA-256、来源 URL、四川适用关系及 MinerU 状态。`pdf` 记录通过 PDF 魔数、`pdfinfo` 页数和 `pdftotext` 检查；图片型卷的文本层可能只包含 OCR 结果，终审核对仍须回看规范 PDF 页面。

当前批次结果：14 个年度（2012—2025）取得 14 份试卷，另取得 6 份可用答案材料；共 20 个 PDF 均已进入 MinerU，20/20 结果为 `done`。2011 年原页面的题图已退化为 20×20 占位图，答案旧链接也失效，已登记为 `blocked`，待补充可核验来源。2012—2014 的答案旧链接同样失效，不以其他网站答案替代。

## 可复用命令

```bash
python scripts/download_gaokao_references.py
python scripts/process_gaokao_mineru.py
python scripts/process_gaokao_mineru.py --sync-only
```

下载脚本使用 HTTPS 优先、原子写入、内容类型检查、PDF 魔数和哈希记录；MinerU 脚本不写入教材 144 源包注册表，只维护本目录独立血缘。

每年材料必须分别登记：

- `document_role=paper`：正式试卷；
- `document_role=answer`：答案；
- `document_role=scoring`：评分资料。

三类文档各自拥有Source、canonical Artifact和权威等级，再用`answer_for`、`scoring_for`关系连接。非官方答案不得继承试卷的S1等级。

当前新增的独立候选层包括：2009 四川卷 Q1—Q6 的明确答案键（省级网站转载/菁优网解析 PDF）、2010 四川卷 Q1、Q2、Q4、Q8、Q9 的明确答案标记、2012 四川卷附件（核验为无答案内容）、2014 四川卷 Q1—Q9 水印图、2015 四川卷 Q1—Q20 答案/解析候选、2016 全国卷Ⅲ Q006（一苇轩）与 2024 全国甲卷 Q1—Q22（美篇）。它们分别保留来源快照、SHA-256、JSONL 候选（若存在）和回执，并已追加到 `registry/` 的 Source/Artifact/Relation 登记；统一标记为第三方未核验候选或显式阻断，不写回主 `answer_index.jsonl`，不提供官方评分标准。
