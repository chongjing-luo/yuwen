# 高考真题材料入口

计划登记2023、2024全国甲卷及2025、2026新课标II卷的原卷、答案和评分资料。当前交付清单只建立稳定的整卷ID，不预设题数或小问数。

每年材料必须分别登记：

- `document_role=paper`：正式试卷；
- `document_role=answer`：答案；
- `document_role=scoring`：评分资料。

三类文档各自拥有Source、canonical Artifact和权威等级，再用`answer_for`、`scoring_for`关系连接。非官方答案不得继承试卷的S1等级。
