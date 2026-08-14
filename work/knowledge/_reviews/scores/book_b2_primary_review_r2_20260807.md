---
schema_version: "2.0-textbook"
review_id: "REV-BOOK-B2-R2-PRIMARY-EVIDENCE-DESIGN"
deliverable_id: "BOOK-B2"
artifact_version: "0.2.1"
review_round: 2
reviewer: "evidence_design"
review_role: "primary"
reviewed_at: "2026-08-08T00:00:00+08:00"
artifact_sha256: "b41b2eaa289cf24a1e907873ae7400dd5b0e40da419c89976d90d3ae472ea70c"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260807-235129+0800"
batch_id: "B2-BOOK-20260808"
---

# 册级总表主审记录：BOOK-B2（r2）

## 1. 输入锁定

- 被评总表 v0.2.1，SHA `b41b2eaa289cf24a1e907873ae7400dd5b0e40da419c89976d90d3ae472ea70c`；上游八个单元图谱、19张知识卡（含诵读卡）均为 accepted。
- 本版本仅补齐 §5 六条册内递进关系的稳定 REL-ID、具体源/目标 KP-ID 与双方 EV-ID，并同步 front matter 版本；上游正文未改。
- Validator `VAL-20260807-235129+0800`：errors=0。

## 2. 覆盖与边界复核

- 目录覆盖8单元、19卡和4篇诵读子文本；卡数按 U01(3)+U02(3)+U03(3)+U04(1)+U05(2)+U06(3)+U07(1)+U08(2)+REC(1)=19 复算。
- 人文主线、语言主线、任务群、册内递进、高考板块和教师用书unknown分离；册表不新增未回链KP，不消费试卷或网络解析。
- 五个高考板块仍为 M0/N/A，教材锁定前未建立任何真题映射。

## 3. 递进关系证据复核

逐条检查 `REL-B2-BOOK-01` 至 `REL-B2-BOOK-06`：每条均含具体源 KP、目标 KP、受控关系类型、递进说明、源 EV 和目标 EV；KP/EV 均可在对应 accepted 卡片中定位，关系方向和文体差异说明可复算。未发现孤立 EV、错卡引用、缺关系类型或仅凭主题相似升级正式边。

## 4. 硬性规则与评分

R01–R10 均未触发；`P0/P1/P2=0/0/0`。

| 维度 | 权重 | 得分 | 依据 |
|---|---:|---:|---|
| 全单元、特殊内容和诵读覆盖 | 25 | 25.0 | 8图、19卡、前言和REC覆盖可复算。 |
| 跨单元递进 | 20 | 19.0 | 6条关系具备稳定REL、KP双端和EV双端；跨册关系留待全局阶段。 |
| 分类、去重与稳定ID | 15 | 14.0 | 分母、卡片/图谱类型和REL-ID稳定。 |
| 双线、任务群与课程定位 | 15 | 14.0 | 人文/语言双线和任务边界清楚。 |
| 高考板块映射 | 10 | 9.0 | 五板块覆盖且严格M0/N/A。 |
| 上下游一致性 | 10 | 10.0 | 上游 accepted、来源链、版本和正文状态可核对。 |
| 检索性 | 5 | 4.5 | 索引词、问题清单及稳定ID可定位。 |
| **合计** | **100** | **95.5** | 全部单项门槛达到。 |

## 5. 主审结论

总分 **95.5/100**，`pass`；R01–R10=0，P0/P1/P2=0/0/0。可与独立二审在同一 SHA 上完成 G4；在状态同步前仍保持 `review_required`。
