---
schema_version: "2.0-candidate"
deliverable_id: "EXAM-2023-NCA"
status: "drafted"
title: "2023年全国甲卷"
source_status: "acquired_unofficial"
source_ids: []
producer: "throughput_generator"
reviewers: []
version: "0.1.0"
---

# 高考语文试卷解构：2023年全国甲卷

> 本文件是候选解构稿。高考试卷材料来自 `Data/reference/gaokao/manifest.json` 登记的转载源（S3），不是官方原卷；未取得答案或官方评分资料的小问不得建立确定性考点映射。

## 1. 来源与完整性

- 题卷状态：`acquired`；来源等级：`S3`。
- 题卷源ID：SRC-GK-2023-NCA-QUESTION；答案源ID：SRC-GK-2023-NCA-ANSWER
- 题卷文件：`Data/reference/gaokao/pdf/2023/2023_NCA_question.pdf`
- MinerU结果：`Data/reference/gaokao/mineru_result/2023_NCA_question`
- 题卷首段锚点：缺少可核验题卷正文。

## 2. 结构索引（候选）

| 序号 | 题卷标题/章节 | 稳定小问ID | 处理状态 |
|---:|---|---|---|
| — | 无可核验章节 | N/A | blocked；等待题卷补齐 |

## 3. 能力动作候选

| 候选动作 | 证据边界 | M等级 |
|---|---|---|
| 提取、概括、分析、比较、鉴赏、表达和迁移 | 仅根据题卷章节和小问逐题建立；本稿不把章节名称等同于题目要求。 | M0 |

## 4. 教材KP映射

| KP | 小问ID | 等级 | 双向证据 | 说明 |
|---|---|---|---|---|
| — | — | M0 | 未登记逐小问与教材KP的双向证据。 | 暂不建立直接衔接。 |

## 5. 缺口与下一步

- 需要逐小问题干、选项、答案和评分标准，建立稳定小问ID。
- 需要核验转载源与官方/省级考试机构版本的一致性。
- 只有完成双向证据核验后，才允许在 `MAP-EXAM-KP.md` 建立M1及以上关系。

## 6. 自检与版本

- [x] 已登记题卷来源状态和可信度边界。
- [x] 缺失材料未被冒充为完整。
- [ ] 小问级解析和教材映射待补。

| 版本 | 日期 | 修改者 | 变更 |
|---|---|---|---|
| 0.1.0 | 2026-08-06 | throughput_generator | 生成候选结构索引和M0治理稿 |
