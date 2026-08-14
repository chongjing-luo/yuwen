---
schema_version: "2.0-textbook"
review_id: "REV-BOOK-B2-R1-PRIMARY-EVIDENCE-DESIGN"
deliverable_id: "BOOK-B2"
artifact_version: "0.2.0"
review_round: 1
reviewer: "evidence_design"
review_role: "primary"
reviewed_at: "2026-08-07T23:27:00+08:00"
artifact_sha256: "64ebcbf44746a1b31d63c8fb2d2b7a07e9b7947e5164fd8f0fd10ce2cdbac3b3"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260807-232242+0800"
batch_id: "B2-BOOK-20260807"
---

# 册级总表主审记录：BOOK-B2

## 1. 输入锁定

- 被评总表 v0.2.0，SHA `64ebcbf44746a1b31d63c8fb2d2b7a07e9b7947e5164fd8f0fd10ce2cdbac3b3`；前言 `ART-PKG-B2-000-PDF` SHA `26c898f79b301d629b44381d3d17bb5ae9d39def6f221c0bcd61e487092d65c9`；课标 SHA `7a187079f1fffe8ae834fdeff25bac9dd0e7de6b979db40fd875786dc0365977`。
- 账本显示 8 个单元图谱、19 张知识卡（含REC）均为 accepted；BOOK-B2仍drafted，故本报告不执行G4。
- Validator `VAL-20260807-232242+0800`：errors=0；上游ID、来源链、M0和结构字段可解析。

## 2. 覆盖与边界复核

- 目录覆盖8单元、19卡和4篇诵读子文本；卡数按 U01(3)+U02(3)+U03(3)+U04(1)+U05(2)+U06(3)+U07(1)+U08(2)+REC(1)=19 复算。
- 人文主线、语言主线、任务群、册内递进、高考板块和教师用书unknown分离；册表不新增未回链KP，不消费试卷或网络解析。
- 递进关系标出双方accepted KP/EV前置条件；所有高考关系保持M0。

## 3. 硬性规则

R01—R10均未触发；来源、版本、教材事实、课标术语、教师用书unknown、M0/N/A和上游accepted边界均合规。最终 `P0/P1/P2=0/0/0`。

## 4. 维度评分

| 维度 | 权重 | 最低 | 得分 | 依据与扣分 |
|---|---:|---:|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25 | 23 | 24.5 | 8图、19卡、前言和REC均覆盖，特殊单元边界清楚；回链索引仍需下游机器化增强扣0.5。 |
| 跨单元递进 | 20 | 17 | 18.0 | 6条有方向的候选递进，均声明双方KP/EV条件；未建立跨册边扣2。 |
| 分类、去重与稳定ID | 15 | 13 | 14.5 | 单元/卡/REC分母可复算，分类稳定；整本书与多文本关系仍需逐KP审计扣0.5。 |
| 双线、任务群与课程定位 | 15 | 13 | 14.5 | 八单元文体、任务群和文化议题双线清晰；跨单元总括保守扣0.5。 |
| 高考板块映射 | 10 | 8 | 9.0 | 五板块覆盖且全为M0；G-TB前无小问证据扣1。 |
| 上下游一致性 | 10 | 9 | 9.5 | source_ids、upstream IDs、版本和教材前言SHA完整。 |
| 检索性 | 5 | 4 | 4.5 | 索引词和问题清单可检索；尚无机器化KP反查扣0.5。 |
| **合计** | **100** | **90** | **94.5** | 全部单项门槛达到。 |

## 5. 主审结论

- 总分 **94.5/100**，全部单项门槛达到；R01—R10=0，P0/P1/P2=0/0/0。
- 决定：**`pass`**，可进入独立第二复审。册表仍不得在二审/G4前转accepted；上游或正文变化将使本报告按SHA失效。
