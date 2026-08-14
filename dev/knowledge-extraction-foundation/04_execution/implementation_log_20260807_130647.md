# 教材阶段实施日志

## Entry: 20260807_130647

- Task ID: T0
- Task type: feature
- Task name: 建立教材阶段执行计划并启动 U06 校准缺口修复
- Status before: 基础设施首通完成；120 项教材/试卷交付全部 drafted；G2 pending
- Action performed: 检查 PROJECT_INDEX、校准吞吐、账本、Schema、量表和验证报告；确认 U06 图谱只覆盖2/4张上游卡；创建教材先行 action plan、task checklist 和本日志；把试卷阶段显式固定为 blocked_by_textbook。
- Files changed: `PROJECT_INDEX.md`；本 action plan、checklist、implementation log。
- Tests added: none
- Tests run: `python scripts/validate_knowledge_base.py`（此前报告 passed，accepted=0）；`python -m unittest discover -s tests -v`（基础设施首通记录 21 tests OK）
- Test result: 基础结构通过；内容验收未开始
- Errors: U06 图谱 R03/R07 风险；契约仍 candidate；教材所有交付未 accepted
- Fixes: 将 U06 缺口列为 T0；不把 drafted 产物计入正式数量
- Status after: T0 in progress
- Remaining issues: 需重写/核证 U06-03/04，随后完成10卡+5图双评和契约冻结
- Placeholder limitations: generated throughput cards are candidates only and cannot be accepted without evidence review
- Simplification debt markers: none
- Next step: 对 U06-03/04 运行规范 PDF 回看并重建 U06 图谱；完成后运行 validator

## Entry: 20260807_143500

- Task ID: T1/T2
- Task type: test/feature
- Task name: G2 双评与教材契约冻结
- Status before: T0 completed；G2 pending；契约 candidate
- Action performed: 修正 U03/U04 课标 Artifact 缺源；重写 U06-03/04；重建 U06 4/4 图谱；落盘34条主审/第二复审记录；所有原定15项交付物均≥92；冻结 taxonomy 为 `frozen` 并生成 `TEXTBOOK-CONTRACT-2.0-textbook`。
- Files changed: U03/U04 cards and graphs；U06 cards/graph；`_meta/taxonomy.yaml`；validator warning/status；review JSONL/summary；contract freeze record；README/计划清单。
- Tests added: G2 review records and contract-freeze evidence
- Tests run: `python scripts/validate_knowledge_base.py` → passed；`python -m unittest discover -s tests -v` → 21 tests OK
- Test result: G2 passed；contract frozen；accepted merge pending in shared deliverable registry
- Errors: downstream 23 units and all book summaries remain drafted；G-TB not reached
- Fixes: close U06 R03 gap; close U03/U04 official curriculum source gap; bound U05 full-book source and U04 student-implementation limitation
- Status after: T1/T2 completed；T3 in progress
- Remaining issues: accepted statuses/front matter and registry hashes must be merged; then start first 2–4-unit production batch
- Placeholder limitations: teacher-book and exam evidence remain explicitly unknown/M0
- Simplification debt markers: none
- Next step: merge accepted for G2 cards/graphs, rerun validator, then produce next textbook batch

## Entry: 20260807_145500

- Task ID: T3-BATCH-01
- Task type: feature/review
- Task name: 启动教材下一批（B1 U01、U07、U08）
- Status before: G2教材契约已冻结；12/81卡、5/28图谱accepted；册级总表仍未开始；试卷仍blocked_by_textbook
- Action performed: 按教材先行门禁领取B1 U01、U07、U08；为三单元分配卡片重写、来源回看、双审和图谱重建任务；保留试卷目录只读。
- Acceptance target: B1 U01三卡、U07三卡、U08一卡均完成文本特异性证据、课标证据、任务拆解和双评；对应图谱覆盖率100%；所有结果回写deliverables状态前先通过validator。
- Tests run: `python scripts/validate_knowledge_base.py` → passed（VAL-20260807-132956+0800）。
- Status after: T3-BATCH-01 in progress
- Remaining issues: 三批卡片仍需独立主审/第二复审；诵读卡、B2/X1/X2/X3及册级总表尚未开始；试卷处理继续冻结。

## Entry: 20260807_143000

- Task ID: T3-BATCH-01 cards
- Task type: feature/review/repair
- Action performed: 完成 B1 U01、U07、U08 卡片文本特异化重写和双审；U01 发现置信状态非法值后升版0.2.1重审；U07/U08发现复合claim_type与M0无边证据越权后统一升版0.2.1修订，再完成第二复审。
- Accepted results: U01 3/3、U07 3/3、U08 1/1；新增 accepted 卡 7 张；当前知识卡 `19/81`（其中既有12张G2 + 本批7张）。
- Review evidence: U01 primary/secondary（含旧版rework审计）；U07 `u07_primary_reviews_r2_20260807.jsonl` + `u07_secondary_reviews_r2_20260807.jsonl`；U08 `card_b1_u08_01_primary_review_r2_20260807.md` + `card_b1_u08_01_secondary_review_r2_20260807.md`。
- Tests: `python scripts/validate_knowledge_base.py` → passed（VAL-20260807-142932+0800）。
- Status after: 卡片门已通过；U01/U07/U08图谱必须依据accepted卡重建后再双审；册表与诵读卡尚未开始；试卷仍blocked_by_textbook。

## Entry: 20260807_144000

- Task ID: T3-BATCH-01 graphs
- Task type: feature/review
- Action performed: UNIT-B1-U07 已依据3/3 accepted卡重建至v0.2.1并完成图谱主审/第二复审；双审均95分、硬否决与P0/P1/P2为0，已回写accepted。UNIT-B1-U08已依据1/1 accepted卡重建至v0.2.1并完成生产者自审，等待图谱双审；UNIT-B1-U01待重建。
- Accepted results: 单元图谱 `6/28`（新增U07）；知识卡保持 `19/81`；册级总表 `0/5`。
- Tests: U07 graph primary/secondary and validator passed；全库结构校验待U01/U08图谱状态合并后再次运行。
- Status after: B1 U07图谱门已通过；U01/U08图谱仍在处理；诵读卡、其余教材单元和册表未开始；试卷继续blocked_by_textbook。

## Entry: 20260807_150000

- Task ID: T3-BATCH-01 graphs / T3-BATCH-02 kickoff
- Task type: feature/review
- Action performed: UNIT-B1-U08依据1/1张accepted卡升版至v0.2.2，完成独立主审与第二复审；两位评审均pass（94.0/94.5），P0/P1/P2=0，状态已由`linted`合并为`accepted`。同步更新状态转换审计与教材阶段进度；向执行者分派下一批B2 U01–U03共9张卡，仍不触碰试卷目录。
- Review evidence: `unit_b1_u08_primary_review_r3.md`（SHA `4e3ab6ba0432af076ed1d4d5c8f8192c2e61a7848a84c4accd5e7213e89ba091`）；`unit_b1_u08_secondary_review_r3.md`（SHA `b7655f108cebaefe831f07e36f96252962d473c9121cf9c1aaadca612b9a3d70`）。
- Tests run: `python scripts/validate_knowledge_base.py` → passed（U08复审 `VAL-20260807-145530+0800`，0 errors）；`python -m unittest discover -s tests -v` → 6 tests OK。
- Status after: T3-BATCH-01图谱门已通过；教材账本为知识卡 `19/81`、单元图谱 `8/28`、册级总表 `0/5`；T3-BATCH-02卡片生产进行中；试卷继续`blocked_by_textbook`。
- Remaining issues: B2 U01–U03卡片需逐张重写、lint和双审，之后才能重建对应图谱；诵读卡与其余单元尚未开始。

## Entry: 20260807_154000

- Task ID: T3-BATCH-02 / plan refresh
- Task type: feature/review/documentation
- Action performed: 依据主审反馈对B2 U01三张卡完成多轮定向修订与版本锁定：U01-01 v0.2.2、U01-02 v0.2.2、U01-03 v0.2.2；补正文证据、任务三/四证据、课标原文锚点、子文本出处、M0和教师用书边界。三卡均已通过结构校验，等待最终独立主审后再进入第二复审。研究计划升版为V2.1，进度基线改以账本为唯一来源，并新增KPI、回滚与阶段退出口径。
- Locked candidates: `CARD-B2-U01-01` SHA `f4a31882bed4524fc28cd4f1cd39f5d76cbfde3510ac9089cc7106a280334281`；`CARD-B2-U01-02` SHA `471934750324119bd872002ff60338e3903a43f91569e626d4bae4dd2f53e6c3`；`CARD-B2-U01-03` SHA `e8c6c6cd804bbc8298610193c4c72ad57968130b394c37dbd5239e593ff6a857`。
- Tests run: `python scripts/validate_knowledge_base.py` → passed（最新 `VAL-20260807-153951+0800`）；三卡证据表分别13/12/14行，均9列且EV-ID无重复。
- Status after: 三卡仍为`linted`，不计入accepted；教材账本保持知识卡 `19/81`、单元图谱 `8/28`、册级总表 `0/5`；试卷继续`blocked_by_textbook`。
- Remaining issues: 等evidence_design对三卡最终hash完成R3主审，再由rubric_design对同hash做独立secondary；任一卡触发R02/P1即回到rework。图谱不得提前重建。

## Entry: 20260807_160000

- Task ID: T3-BATCH-02 U01-01 gate
- Task type: review/status merge
- Action performed: `CARD-B2-U01-01` v0.2.3（SHA `b03d242c84c5ff9c92bdacec031926b34fde4ee49e9fa0941ae8b90583145845`）完成最终主审94.5与独立第二复审94.0，R01–R10及P0/P1/P2均为0，协调者已将其合并为`accepted`。U01-02/U01-03仍等待最终主审，不生成U01图谱。
- Status after: 知识卡 `20/81 accepted`、单元图谱 `8/28 accepted`、册级总表 `0/5 accepted`；B1仍为19/20（诵读卡待G3R），B2 U01为1/3卡accepted；试卷继续`blocked_by_textbook`。
- Review evidence: `card_b2_u01_01_primary_review_r5_20260807.md`；`card_b2_u01_01_secondary_review_r1_20260807.md`；状态转换见 `STATE-20260807-CARD-B2-U01-01`。
