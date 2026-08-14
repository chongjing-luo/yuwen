# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## [LRN-20260813-002] best_practice

**Logged**: 2026-08-13T17:45:00+08:00
**Priority**: high
**Status**: promoted
**Area**: tests

### Summary
独立审查运行期间不得让构建测试覆盖正式冻结候选。

### Details
第一章视觉审查正在读取SHA-256为`9e6b…`的PPTX时，主流程执行的回归测试机械重建了正式文件，使当前PPTX和manifest变成`24c079…`。抽取文字、备注和既有渲染未变，但两名审查者实际面对了不同字节对象，破坏了冻结凭证的一致性。

### Suggested Action
所有构建/回归测试必须在发审前完成，或将输出重定向到临时目录；审查开始后对正式候选设只读纪律，审查报告只接受同一组哈希。发生重建时，必须以当前文件重新完成双审，不能据“看起来等价”直接继承结论。

### Metadata
- Source: error
- Related Files: work/备课/逐页功能审计与放行协议.md, tests/test_build_meng_v6_chapter1_pptx.py
- Tags: pptx, hash, review, reproducibility
- Pattern-Key: lesson.freeze_candidate_during_independent_review
- Recurrence-Count: 1
- First-Seen: 2026-08-13
- Last-Seen: 2026-08-13
- Promoted: work/备课/逐页功能审计与放行协议.md

---

## [LRN-20260813-001] correction

**Logged**: 2026-08-13T12:00:00+08:00
**Priority**: critical
**Status**: promoted
**Area**: docs

### Summary
语文课堂PPT必须以逐页学生接收变化为最小责任单位，不能以内容覆盖或版式完整代替教学功能。

### Details
用户指出，导入页只列三篇作品并立即追问“爱情的幸福关于什么”，既缩窄文学回忆范围，又在学生缺乏分析框架时要求过深回答。此前方案还多次把教师目标、学生画像和设计口号放到学生前台，或给活动换名称却没有改变学生体验。根因是把“教师准备发送什么”误当成“学生怎样形成理解”。

### Suggested Action
所有页面执行功能合同、第一人称接收测试、多渠道泄答测试和P0—P2缺陷否决；教学手法按具体学习困难选择；插图先证明学习功能并冻结人物圣经。

### Metadata
- Source: user_feedback
- Related Files: work/备课基本原则.md, work/备课/逐页功能审计与放行协议.md, work/备课/语文课堂教学手法库.md, work/备课/视觉与插图功能规范.md
- Tags: chinese-teaching, slide-function, student-reception, activity-design, illustration
- Pattern-Key: lesson.slide_function_over_content_coverage
- Recurrence-Count: 4
- First-Seen: 2026-08-12
- Last-Seen: 2026-08-13
- Promoted: work/备课基本原则.md

---

## LRN-20260814-001 逐页合同字段被模板默认串填充等于未落实

- **Date**: 2026-08-14
- **Context**: 《氓》V6.6 课程数据 46 页中 45 页的教师角色、等待合同、故事回接等追溯字段仍是 `contract()` 的通用默认串（462 处，见 `work/evaluation/reports/principle_checks_meng_v66.json`）。
- **Learning**: 设计字段的存在不等于原则的落实；只要字段可以有默认值，默认值就会被批量留下并冒充证据。机器合同必须区分"非空"与"非模板"。
- **Action**: 反样板检查器 `scripts/checks/check_trace_evidence.py` 上线（P-17/P-19 的 enforcement），模式与 lesson.js 默认串同步由测试保护；新候选按 STANDARD-1.0 须样板清零。
- **Recurrence-Count**: 1
- **Status**: active
- **Promoted-Principle**: P-28 enforcement 扩充（机器层）
