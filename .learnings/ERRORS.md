# Errors

Command failures and integration errors.

---

## [ERR-20260814-001] update_plan_result_display

**Logged**: 2026-08-14T18:48:41+08:00
**Priority**: low
**Status**: resolved
**Area**: docs

### Summary
`update_plan` 调用后的展示代码假定返回值含 `plan` 属性，导致包装脚本报错。

### Error
```text
TypeError: Cannot read properties of undefined (reading 'forEach')
```

### Context
- 计划内容已提交给工具；仅是之后读取 `p.plan.forEach(...)` 时失败。
- 审查输入和源文件未受影响。

### Suggested Fix
调用 `update_plan` 时不对不透明返回值做结构化展示，直接用 `text(result)` 或忽略返回体。

### Metadata
- Reproducible: yes
- Related Files: none

### Resolution
- **Resolved**: 2026-08-14T18:48:41+08:00
- **Notes**: 后续改为不解构 `update_plan` 返回值。

---

## [ERR-20260813-001] build_tests_overwrote_review_candidate

**Logged**: 2026-08-13T17:45:00+08:00
**Priority**: high
**Status**: resolved
**Area**: tests

### Summary
回归测试在双独立审查期间覆盖第一章正式PPTX，导致两个审查者读取不同SHA-256对象。

### Error
```text
视觉审查输入PPTX：9e6b0b57…
学生接收审查时当前PPTX：24c07964…
```

### Context
- 运行第一、二章54项unittest时，构建测试写回正式`_v6_stage/chapter_1/pptx`目录。
- 新manifest与当前PPTX均登记`24c07964…`；当前MarkItDown与既有v8抽取完全相同。

### Suggested Fix
以当前`24c07964…`重新双审；今后发审前完成写入型测试或重定向到临时目录。

### Metadata
- Reproducible: yes
- Related Files: tests/test_build_meng_v6_chapter1_pptx.py, scripts/build_meng_v6_chapter1_pptx.js

### Resolution
- **Resolved**: 2026-08-13T17:46:00+08:00
- **Notes**: 已要求两名独立审查者统一复验当前24c候选，并把防覆盖规则写入冻结协议。

---
