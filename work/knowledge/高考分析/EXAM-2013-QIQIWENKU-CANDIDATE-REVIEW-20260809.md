---
schema_version: "exam-reference-answer-source-review-0.1"
status: "blocked_contaminated"
reviewed_at: "2026-08-09T15:02:15+08:00"
---

# 2013 四川卷齐齐文库候选来源复核

- 快照：`Data/reference/gaokao/external/2013_qiqiwenku_answer/full_preview.pdf`（29 页，SHA-256 `dbeebaaf73c027ee8431217e6f992175c82153d2dfea449de7bc5f6353e07d9c`）。
- 来源：360 文库转链 `https://wenku.so.com/d/c3cbdc68ef52be938ea746f39e9a3f84`；合作页 `https://www.qiqiwenku.com/docx/64926719.html`。
- 结论：阻断，不建立题目级答案候选，不修改主 `answer_index.jsonl`。

## 阻断证据

1. 答案段标题明确写作“语文（江苏卷）参考答案”。
2. 文档继续出现“语文Ⅱ（附加题）参考答案”及 Q22—Q29；2013 四川卷本题范围到 Q21。
3. 可见客观键与既有四川第三方候选发生冲突，不能把版面中的键归因于四川卷。

## 门禁

- `official_verified=0`；`scoring_status=not_available_as_official`。
- 保留 PDF、文本、HTML、分块哈希和复核 JSONL，仅用于后续人工追溯。
- 不从该材料提取知识点、不生成评分标准、不升级教材映射；继续保持 `M0 / kp_id=N/A`。
