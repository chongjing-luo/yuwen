---
schema_version: "2.0-textbook"
review_id: "REV-UNIT-B1-U02-U06-R2-SECONDARY-INDEPENDENT"
deliverable_id: "UNIT-B1-U02..U06"
artifact_version: "multi: U02=0.1.2; U03=0.2.2; U04=0.2.2; U05=0.1.2; U06=0.2.2"
review_round: 2
reviewer: "independent_secondary_b1_u02_u06"
review_role: "secondary"
reviewed_at: "2026-08-08T01:20:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260807-233133+0800"
batch_id: "B1-U02-U06-20260807"
decision: "conditional"
---

# B1 U02–U06 单元图谱独立复审记录（R2）

> 本报告逐份锁定五个新 SHA，复核 front matter/ledger 状态、accepted 卡覆盖、旧候选措辞、R/P 与图谱量表；不修改正文或账本，也不读取既有该五单元评审报告。

## 1. 输入与验证

独立 validator：`VAL-20260807-233133+0800`，`passed`、0 errors；报告 `/tmp/val_b1_u02_u06_secondary_r2_20260808.json`。

| 单元 | 版本 | SHA | 正文 status | ledger status/version/owner | accepted 卡 |
|---|---|---|---|---|---:|
| UNIT-B1-U02 | 0.1.2 | `a7fe6b61b0f28c93d0c7e38c078e4df7955cf325f9c54485d8d89fb235d1df1c` | review_required | review_required/0.1.2/execution_design | 3/3 |
| UNIT-B1-U03 | 0.2.2 | `e26d31ae5a174b47cc36a99663789983b44d52a4480d700cad872f34a1c2a4b1` | review_required | review_required/0.2.2/evidence_design | 3/3 |
| UNIT-B1-U04 | 0.2.2 | `becd6d06e546cf0a8b7a164b238cdbcc874a4bb7fbf549ca6357719b94bad74b` | review_required | review_required/0.2.2/evidence_design | 1/1 |
| UNIT-B1-U05 | 0.1.2 | `34a82d2345a90e5d06586275627a4dcf200311c7eeaf9558827bc566edbe2716` | review_required | review_required/0.1.2/rubric_design | 1/1 |
| UNIT-B1-U06 | 0.2.2 | `c122f0838821652a4472e9b0a887ac044feac63a39b6fa1ea64c9c46d087bcd8` | review_required | review_required/0.2.2/coordinator | 4/4 |

账本与 front matter 的 status/version/owner 已一致；上游卡均为 accepted。旧“待上游/正式覆盖率暂不计算/阻断”段落已清除。剩余问题是五份正文导语仍写“账本状态为 accepted/上游均已 accepted”，与当前图谱本身 `review_required` 状态不一致；U05 另有“覆盖完整须以上游卡转为 accepted”旧条件句。

## 2. R01–R10/P 共通核查

| 代码 | 结论 |
|---|---|
| R01 | 否；教材事实、任务和边界无新严重错误。 |
| R02 | 否；节点、任务、关系均有 Card/KP/EV 或 Artifact 回链。 |
| R03 | 否；各单元合编/特殊内容覆盖完整。 |
| R04 | 否；教材义务、项目解释、TB unknown、M0 边界分离。 |
| R05 | 否；未新增无证 KP，综合节点保留来源链。 |
| R06 | 否；高考均保持 M0/N/A。 |
| R07 | 否；accepted 卡覆盖与 upstream IDs 一致。 |
| R08 | 否（P1）；文件 ID/数量/版本链可解析，状态导语与 review_required 状态的语义不一致。 |
| R09 | 否；任务群为现行课标受控名称。 |
| R10 | 否；双维度均有语言实践依据。 |

每份共同 P1=1（导语误称账本 accepted）；U05 另 P2=1（覆盖条件旧句）。P0=0。

## 3. 逐份复核与七维评分

### UNIT-B1-U02（0.1.2）

3/3 卡、5 子任务、4H+6L、3 关系、M0/N/A 和任务 Artifact 定位均闭合；`CAND-` 已清楚限定为综合节点稳定命名，旧“待上游候选视图”已删除。唯一缺陷是导语仍写账本 accepted。

七维得分：覆盖 24.0、综合 18.0、双维度 14.0、任务 14.5、高考 9.0、递进 8.0、可读性 4.5；**92.0/100**。R01–R10=0，P0/P1/P2=`0/1/0`，`conditional`。

### UNIT-B1-U03（0.2.2）

3/3 卡、3 子任务、4H/4L、4 关系、M0/N/A 和源定位闭合；覆盖结论已改为 3/3 accepted，CAND 仅为节点命名。导语仍把“账本状态”写成 accepted，而当前图谱和 ledger 为 review_required。

七维得分：覆盖 24.0、综合 18.5、双维度 14.0、任务 14.5、高考 9.0、递进 8.0、可读性 4.5；**92.5/100**。R01–R10=0，P0/P1/P2=`0/1/0`，`conditional`。

### UNIT-B1-U04（0.2.2）

1/1 卡、3 活动阶段、4H/5L、5 关系、M0/N/A 和三项任务 Artifact 定位闭合；旧正式覆盖率措辞已清除，CAND 命名边界清楚。导语仍误称账本 accepted。

七维得分：覆盖 24.0、综合 18.0、双维度 14.0、任务 14.5、高考 9.0、递进 8.0、可读性 4.5；**92.0/100**。R01–R10=0，P0/P1/P2=`0/1/0`，`conditional`。

### UNIT-B1-U05（0.1.2）

1/1 卡、4 个整本书任务、4H/6L、4 关系、M0 和缺源治理闭合；历史 drafted Issue 已 resolved，旧候选门禁主体已关闭。第1节仍写“覆盖完整须以上游卡转为 accepted”，与当前 review_required 图谱阶段不一致；导语也误称账本 accepted。

七维得分：覆盖 23.5、综合 18.5、双维度 14.5、任务 15.0、高考 9.0、递进 8.0、可读性 4.5；**93.0/100**。R01–R10=0，P0/P1/P2=`0/1/1`，`conditional`。

### UNIT-B1-U06（0.2.2）

4/4 卡、9 个任务、4H/5L、7 关系、M0 和教师用书 unknown 边界闭合；历史 drafted Issue 已 resolved，前后候选关系明确“不计正式边”。导语仍误称账本 accepted，需改为 review_required/待图谱双审。

七维得分：覆盖 24.0、综合 19.0、双维度 14.5、任务 15.0、高考 9.0、递进 8.0、可读性 4.5；**94.0/100**。R01–R10=0，P0/P1/P2=`0/1/0`，`conditional`。

## 4. 必须处理与总体结论

- **P1-STATUS（五单元）**：将导语中的“本图谱账本状态为 `accepted`”改为与当前 front matter/ledger 一致的 `review_required`，或写明“上游卡 accepted、图谱待双审”；不得把图谱状态写成 accepted。
- **P2-U05**：删改“覆盖完整须以上游卡转为 accepted”旧条件句，改为当前上游已 accepted、图谱本身待双审/G4 的准确表述。
- 五份图谱的内容、任务、双维度、关系和 M0 结构均达到图谱量表分数线；但 P1/P2 清零前不得转 accepted 或被册表正式消费。
- 总体决定：五份均 **`conditional`**；修订后需逐份新 SHA、validator 和状态一致性复核。

## 5. 可复现信息

- Validator：`VAL-20260807-233133+0800`，passed/errors=0；临时报告 `/tmp/val_b1_u02_u06_secondary_r2_20260808.json`
- Rubric：`2.0-textbook` / SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`
