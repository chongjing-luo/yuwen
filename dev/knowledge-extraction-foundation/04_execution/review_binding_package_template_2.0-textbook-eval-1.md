# Review package template — `2.0-textbook-eval-1`

本模板将“正文评分记录”和“同 SHA 绑定清单”分开，避免向历史 `review.schema.json` 静默加字段。

## 文件布局

```text
review_package/
├── artifact.md                         # 被评版本；DG3 后不得由评审者改写
├── primary_review.json                 # review.schema.json；主审独立封存
├── secondary_review.json               # review.schema.json；二审独立封存
├── claim_register.json                 # DG2 封存 Claim 分母
├── constraint_register.json            # DG2 约束与 N/A 边界
├── observation_manifest.json            # 版本化观察输入
└── review_binding_manifest.json        # 本候选伴随 Schema
```

## 封存顺序

1. 生产者完成 DG2 后保存 artifact、Claim、Constraint、Observation 和 upstream snapshot 的 SHA。
2. 主审在看不到二审原始记录的条件下完成 `primary_review.json` 并封存 SHA。
3. 二审在看不到主审原始记录的条件下完成 `secondary_review.json` 并封存 SHA。
4. 协调者填写 `review_binding_manifest.json`，确认两审绑定同一 `content_sha256`、`claim_register_sha256`、`rubric_sha256`、`observation_manifest_sha256`、`upstream_snapshot_sha256` 与 `batch_manifest_sha256`。
5. 任一正文返修、Claim 删除、locator 改写或 version 改变都会产生新 content SHA；旧评审只留作审计，不得复用。

## DG3 结论规则

- `pass` 只允许在两份 review 均为 `decision=pass`、R01—R10 为空、P0/P1/P2 均为 0 且分差合规时出现。
- 角色重合、文件 SHA 相同、content/Claim/rubric/observation/upstream SHA 不一致时，绑定校验失败。
- `adjudication` 只有在两份原始评审均封存后才可启用；仲裁记录不能覆盖原始分数或缺陷。

