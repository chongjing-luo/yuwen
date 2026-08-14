---
name: yuwen-design-homework
description: 高中语文作业设计（S7a 环节）。当需要为一篇课文设计课后作业包（分层、闭卷检索、迁移变式、跨课文延伸）时使用。
---

# 作业设计（S7a）

服务机制节点：**K1（四站之一）、K3（闭卷检索）、U3（反馈触发修订）、U8（迁移变式）、J1（延伸选题自主）、J2（分层）、K4（跨课文比较）**。

## 输入

- 课程数据（lesson.js / schema JSON：KP 落点、课堂产物）
- 知识卡（KP 清单）
- 范式：`work/teaching/选择性必修下册/氓/homework/homework_package.json`

## 步骤

1. 从课程数据提取本课 KP 落点与课堂产物（作业必须回链课堂，page_refs + artifact_ref）。
2. 设计三层题目：
   - **巩固**（闭卷检索）：当日核心 KP 的提取式激活——先写后核对、亲手订正、订正痕迹计入证据（K3/U3）；
   - **迁移**（必做任选一）：变式情境中运用 KP（U8），作答区分"诗写/我推断"（U6）；
   - **延伸**（选做）：跨课文比较（引用真实 CARD-ID，K4），保留选题自主权（J1）。
3. 每题必填六件套：kp_ids / page_refs / prompt / expected_evidence / feedback_trigger / normal_path（U7 反例路径同样适用于作业）。
4. 时间预算：必做（巩固+迁移其一）≤ 45 分钟上限（K5/U5）。
5. 构建：`node scripts/build_homework_package.js <package.json>` → 学生作业单 + 教师批改要点。
6. 校验：`python3 scripts/validate_homework_package.py <package.json>` 必须通过。

## 放行条件

- 校验器通过（闭卷必含、迁移必含、KP 全解析、页引用真实、时长达标、无后台词）；
- 学生作业单通读一遍：语言是学生语言，无设计术语（P-13）；
- claim_boundary 声明待课堂验证。

## 常见错误

- 全是开卷抄写型题目（丢 K3）；考未教且无支架的 KP（违反对齐）；反馈只给对错不触发修订（丢 U3）。
