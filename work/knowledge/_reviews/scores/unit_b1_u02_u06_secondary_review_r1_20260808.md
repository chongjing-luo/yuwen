---
schema_version: "2.0-textbook"
review_id: "REV-UNIT-B1-U02-U06-R1-SECONDARY-INDEPENDENT"
deliverable_id: "UNIT-B1-U02..U06"
artifact_version: "multi: U02=0.1.1; U03=0.2.1; U04=0.2.1; U05=0.1.1; U06=0.2.1"
review_round: 1
reviewer: "independent_secondary_b1_u02_u06"
review_role: "secondary"
reviewed_at: "2026-08-08T00:55:00+08:00"
rubric_version: "2.0-textbook"
rubric_sha256: "ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43"
validation_run_id: "VAL-20260807-232649+0800"
batch_id: "B1-U02-U06-20260807"
decision: "conditional"
---

# B1 U02–U06 单元图谱独立复审记录（R1）

> 本报告合并记录五份新版本的独立复核；各单元分别锁定 SHA、覆盖、R/P 和七维分数。未修改正文或账本，也未读取既有该五单元评审报告。

## 1. 共同验证与版本锁定

独立 validator：`VAL-20260807-232649+0800`，`passed`、0 errors；报告 `/tmp/val_b1_u02_u06_secondary_20260808.json`。

| 单元 | 文件版本/status | 文件 SHA | ledger 状态/version/owner | accepted 卡覆盖 |
|---|---|---|---|---|
| UNIT-B1-U02 | v0.1.1 / `accepted` | `51d092eda73c63201023d8549fff9956b6cfeb47e4d7769717b6f48656126b16` | `review_required` / v0.1.1 / execution_design | 3/3 |
| UNIT-B1-U03 | v0.2.1 / `accepted` | `f8c74177b81bb5830b6cb5985d0dbfc6ffc7047fe0acb1fc8bc9eb6a05bcf605` | `review_required` / v0.2.1 / evidence_design | 3/3 |
| UNIT-B1-U04 | v0.2.1 / `accepted` | `a70d055eddca58825019b08b426094c99475151d3f838cd046d9a4bed8080511` | `review_required` / v0.2.1 / evidence_design | 1/1 |
| UNIT-B1-U05 | v0.1.1 / `accepted` | `67d9f2e7eb4ab96dd380bb40db1e9cd95eddab97d0f4e71d419304387953b701` | `review_required` / v0.1.1 / rubric_design | 1/1 |
| UNIT-B1-U06 | v0.2.1 / `accepted` | `baede5b9adaed2dd257109c1e0191d665546d034a9cb363aeeecf65451515d3d` | `review_required` / v0.2.1 / coordinator | 4/4 |

## 2. 共通 R01–R10/P 核查

| 代码 | 五单元共同结论 |
|---|---|
| R01 | 否；各图篇目、册次、任务和教材边界未见新严重事实错误。 |
| R02 | 否；节点、任务和关系均有 Card/KP/EV 或任务 Artifact 回链。 |
| R03 | 否；各自合编/特殊内容覆盖与模板无新增缺口。 |
| R04 | 否；教材义务、项目解释、教师用书 unknown 与 M0 边界分离。 |
| R05 | 否；正式综合节点和关系均保留来源 KP/EV，不新增无证原子 KP。 |
| R06 | 否；均保持 M0/N/A，不伪造真题直接衔接。 |
| R07 | 否（但各单元均有 P1 状态声明漂移）；卡片本身均为 accepted，图谱正文 front matter 仍为 accepted，而 ledger 已改为 review_required。 |
| R08 | 否（P1）；文件内 ID、数量和上游 links 可解析，但正文 status 与 ledger review_required 不一致。 |
| R09 | 否；任务群沿用现行课标受控名称。 |
| R10 | 否；双维度和核心素养定位均有文本/任务语言实践依据。 |

各单元共同 P：`P0=0`；`P1=1`（front matter `accepted` 与 ledger `review_required` 状态漂移）；`P2=1` 仅在仍残留旧候选说明的单元计入（U02/U03/U04/U05）。

## 3. 分单元复核记录与评分

### UNIT-B1-U02（v0.1.1）

- **覆盖/结构**：3/3 accepted 卡、任务 5 子任务节点、4H+6L、3/3 卡内跨课关系、M0 和前后 N/A 均可回链；任务页码/Artifact 定位齐全。
- **已关闭项**：顶部“3/3 accepted”及 `CAND-` 稳定命名边界已说明；ledger 已改 `review_required`，故尚不得称最终 accepted 图谱。
- **未关闭项**：第3节仍保留“下表为待上游卡验收的候选视图，不构成正式汇总”，与本版三卡已 accepted 的事实相冲突；需改为“综合节点保留 CAND 命名，不表示上游门禁阻断”。front matter `accepted` 也应与 ledger `review_required` 对齐。
- **评分**：覆盖 23.0/25；综合 18.0/20；双维度 14.0/15；任务 14.5/15；高考 9.0/10；递进 8.0/10；可读性 4.0/5；**合计 90.5/100**。P0/P1/P2=`0/1/1`；决定 `conditional`。

### UNIT-B1-U03（v0.2.1）

- **覆盖/结构**：3/3 卡、任务表、4H/4L、4 条关系、M0/N/A 均有 Card/KP/EV 或任务定位；跨卡关系有具体 KP/EV。
- **已关闭项**：顶部与节点说明已把 CAND 限定为综合节点稳定命名，不再称上游未验收。
- **未关闭项**：第1节仍写“覆盖结论：初稿；正式覆盖率暂不计算，待三卡全部 accepted 后锁定”，与三卡已 accepted 和 ledger review_required 双重不一致。需改为 review_required 的图谱评审门，不得保留 drafted 覆盖措辞；front matter 状态亦需同步。
- **评分**：覆盖 23.0/25；综合 18.5/20；双维度 14.0/15；任务 14.5/15；高考 9.0/10；递进 8.0/10；可读性 4.0/5；**合计 91.0/100**。P0/P1/P2=`0/1/1`；决定 `conditional`。

### UNIT-B1-U04（v0.2.1）

- **覆盖/结构**：1/1 卡、3 项活动/任务、4H/5L、5 条关系、M0/N/A 和 Artifact 页码定位均可解析。
- **已关闭项**：顶部已写唯一卡 accepted，CAND 限定为综合节点命名。
- **未关闭项**：第1节仍写“形成初稿，正式覆盖率待卡片 accepted 后锁定”，与卡 accepted 和 ledger review_required 矛盾；front matter 状态需同步。候选节点命名本身不构成问题。
- **评分**：覆盖 23.0/25；综合 18.0/20；双维度 14.0/15；任务 14.5/15；高考 9.0/10；递进 8.0/10；可读性 4.0/5；**合计 90.5/100**。P0/P1/P2=`0/1/1`；决定 `conditional`。

### UNIT-B1-U05（v0.1.1）

- **覆盖/结构**：1/1 accepted 卡、4 项整本书任务、4H/6L、4 条卡内关系、M0 和缺源治理均有 KP/EV/Artifact 定位。
- **已关闭项**：顶部和 Issue-001 已把历史 drafted 记录标为 resolved，综合节点不再以候选门禁阻断；正文来源链闭合。
- **未关闭项**：第1节仍说“覆盖完整须以上游卡转为 accepted 为前提”，但卡与 ledger 当前阶段已为 accepted/review_required；前后候选边待对端复核属合理 N/A，不是缺陷。front matter status 需与 ledger review_required 同步。
- **评分**：覆盖 24.0/25；综合 18.5/20；双维度 14.5/15；任务 15.0/15；高考 9.0/10；递进 8.0/10；可读性 4.0/5；**合计 93.0/100**。P0/P1/P2=`0/1/1`；决定 `conditional`。

### UNIT-B1-U06（v0.2.1）

- **覆盖/结构**：4/4 accepted 卡、9 项任务、4H/5L、7 条关系、M0 和教师用书 unknown 边界齐全；关系均有具体 KP/EV 或任务 EV。
- **已关闭项**：顶部明确四卡 accepted，历史 drafted 已在 Issue-001 标为 resolved；候选前后递进明确“不计正式边”，不误称确定性递进。
- **未关闭项**：front matter status 仍 `accepted`，ledger 已 `review_required`；需同步状态。U06 的候选前后关系和 CAND 综合命名有清楚“不计正式边”边界，不另列 P2。
- **评分**：覆盖 24.0/25；综合 19.0/20；双维度 14.5/15；任务 15.0/15；高考 9.0/10；递进 8.0/10；可读性 4.5/5；**合计 94.0/100**。P0/P1/P2=`0/1/0`；决定 `conditional`。

## 4. 必须处理与总体结论

- **P1-STATE（五单元）**：ledger 已按协调要求改为 `review_required`，但五个图谱 front matter 仍是 `status: accepted`；须统一为 review_required 或按正式状态机写明“图谱正文已通过上游门、待图谱双审”的受控状态，不能让跨文件状态冲突继续存在。
- **P1-TEXT（U02/U03/U04/U05）**：清理“待上游卡验收/正式覆盖率暂不计算/待卡片 accepted 后锁定”等旧候选门禁措辞；保留 CAND 仅作为综合节点稳定命名或明确“不计正式边”。
- **P2（U02/U03/U04/U05）**：修订后逐单元重跑 validator，并核对版本记录、ledger version、上游 accepted 卡 SHA 与图谱正文覆盖表。
- 总体结论：五份新图谱均为 **`conditional`**；内容结构基本达图谱量表门槛，但状态声明和旧候选措辞未清零，当前不得把任一份作为 `accepted` 图谱消费。

## 5. 可复现信息

| 单元 | SHA |
|---|---|
| UNIT-B1-U02 | `51d092eda73c63201023d8549fff9956b6cfeb47e4d7769717b6f48656126b16` |
| UNIT-B1-U03 | `f8c74177b81bb5830b6cb5985d0dbfc6ffc7047fe0acb1fc8bc9eb6a05bcf605` |
| UNIT-B1-U04 | `a70d055eddca58825019b08b426094c99475151d3f838cd046d9a4bed8080511` |
| UNIT-B1-U05 | `67d9f2e7eb4ab96dd380bb40db1e9cd95eddab97d0f4e71d419304387953b701` |
| UNIT-B1-U06 | `baede5b9adaed2dd257109c1e0191d665546d034a9cb363aeeecf65451515d3d` |

- Validator：`VAL-20260807-232649+0800`，passed/errors=0；临时报告 `/tmp/val_b1_u02_u06_secondary_20260808.json`
- Rubric：`2.0-textbook` / SHA `ab9cc53d57834642e66e568824d1c0c53e128953e15b20b4c7bd04aa30610d43`
