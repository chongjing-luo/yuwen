# ChatGPT Luna 执行交接包：教材优先，试卷后置

## 任务目标

完成语文备课系统的教材知识点提取、单元图谱和册级总表；教材锁定后，再按冻结的高考契约处理四川省 2008—2024 真题。任何试卷清洗、切分、题型归并、知识点提取和教材映射，均须等待 `TEXTBOOK-LOCK` 记录。

## 当前状态（2026-08-07）

- 契约：`2.0-textbook`；评估量表：`2.0-candidate`。
- 进度唯一来源：`work/knowledge/_meta/deliverables.jsonl`。
- 教材计数（2026-08-07 账本快照）：知识卡 `34/81 accepted`；单元图谱 `13/28 accepted`；册级总表 `0/5 accepted`。执行前仍须以 `work/knowledge/_meta/deliverables.jsonl` 和最新 validator 重新核对。
- 当前工作批次：必修下册 U04。卡片已修订为 v0.2.1，SHA-256：
  `dc1de7ad2d5051eeca3039863ae1e94b3c3cef949472680ebebc69ed2d07f573`；validator `VAL-20260807-181953+0800` 已通过。
- U04 卡正在进行同一 SHA 的主审与第二复审，尚未写回 `accepted`。
- 试卷阶段状态：`blocked_by_textbook`。

## 严格执行顺序

### A. 教材阶段

1. 按 `deliverables.jsonl` 的 drafted 项逐卡重写；先卡后图，先图后册级总表。
2. 每张卡必须绑定规范学生教材 PDF 与 `SRC-CURR-2020`；MinerU 只用于定位，直接引文必须回看规范 PDF。
3. 教师用书 `edition_match=unknown` 时不得消费其内容；只能在边界栏登记不确定性。
4. 活动单元、合编课和诵读包必须枚举所有子任务/子文本并建立可回链 ID。
5. 没有逐小问双向证据时，高考衔接严格使用 M0：`KP-ID/真题小问/能力动作/真题证据/教材证据` 全部为 `N/A`。
6. 运行 `python scripts/validate_knowledge_base.py`；每一批次执行 G0→G1→G2→G3→G4：快照、结构、证据、双审、账本写回后再次验证。
7. 只有主审和独立第二复审对同一版本、同一 SHA 均 `pass`，且 R01–R10/P0/P1/P2 全部清零，才允许把卡/图/表写为 `accepted`。
8. 教材锁定条件：81 张卡、28 张图、5 册级总表全部为 `accepted`。生成并写入 `TEXTBOOK-LOCK-<version>` 记录，记录上游哈希、validator run_id 和锁定时间。

### B. 试卷阶段（仅在教材锁定后）

1. 读取 `/home/ubuntu/homes/LuoChongjing/Methods/yuwen/Data/2008-2024·（四川）语文高考真题`，先建立原始卷、答案/评分资料和哈希清单。
2. 对原始 Markdown 做可逆清洗：去水印、修复页眉页脚和断行，但保留原始文件；整理文件必须用双链回指原始卷。
3. 依据冻结真题 Schema 按题目类型和小问切分；同题型归并前先保留卷别、年份、题号、分值和原卷定位。
4. 对每个小问提取四层、四翼、情境、能力动作、答案和不确定性；严禁用题型相似替代教材双向证据。
5. 通过试卷阶段独立的 G1 结构校准、G2 证据校准、G3 双审后，才建立 M1/M2/M3 映射；无证据项保持 M0。

## 允许修改的核心文件

- `work/knowledge/**` 对应当前领取的卡、图或册级表。
- `work/knowledge/_reviews/**` 评审记录和状态迁移记录。
- `work/knowledge/_meta/deliverables.jsonl` 仅由协调者在双审通过后写回。
- 计划与交接记录；不得擅自修改冻结契约、模板、量表或他人未领取文件。

## 每个交付的回报格式

回报 deliverable ID、版本、SHA-256、validator run_id、主审/第二复审文件路径、分数、未决问题和下一步；不得只报告“已完成”。

## 禁止事项

- 在 `TEXTBOOK-LOCK` 前处理任何四川高考试卷内容。
- 使用未确认同版教师用书、网络解析、OCR 结果作为正式教材证据。
- 把 `pass` 直接当作 `accepted`；必须完成账本状态迁移并再次 validator。
- 使用 `git reset --hard`、`git checkout` 或破坏性清理。
