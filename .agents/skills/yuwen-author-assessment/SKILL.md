---
name: yuwen-author-assessment
description: 高中语文命题组卷（S8a 环节）。当需要设计命题蓝图、从题库组卷、生成评分量规时使用。
---

# 命题组卷（S8a）

服务机制节点：**K1（四站第三站）、K3（测评回收）、K4（跨课回投）、U6（解释分层给分）**。目录：`work/knowledge/assessment/`（schema 见其 README）。

## 输入

- 单元图谱（KP 权重依据）、课程数据与作业包（四站闭环引用）
- 题库 `item_bank.jsonl`（IB-AU 原创可入卷；IB-SC 真题参照只进教师卷）
- 17 年真题语料（题型分布依据：`work/knowledge/高考分析/kp_batches/`）

## 步骤

1. **先写蓝图再写题**（P-37）：kp_weights 每条给 basis（图谱定位或语料统计）；type_distribution 依据真题频次；总分/时长定死。
2. 原创题按题库 schema 完整填写：stem / kp_ids（必须解析到知识卡）/ expected_evidence / scoring_points（合计==题分）/ normal_path。
3. 题干设计继承课堂理念：主观题要求"区分诗写/推断"（U6）；立场不评分、论证质量评分（scoring_principles 写明）。
4. 真题参照条目（candidate_only_M0）不进学生卷，只作变式参照附教师卷，保留 prompt_source 与 sha 溯源。
5. 构建：`python3 scripts/build_assessment_paper.py <blueprint.json>` → 学生卷 + 教师卷与评分量规。
6. 校验：`python3 scripts/validate_assessment_package.py <blueprint.json>` 必须通过。

## 放行条件

- 校验器通过（守恒/覆盖/溯源/闭环引用/无后台词）；
- 每题 expected_evidence 先于评分点存在（P-37）；
- claim_boundary 声明信度效度待真实施测。

## 常见错误

- 权重"拍脑袋"无 basis（K1 违例）；蓝图不引用作业（四站断链，K3）；
- 把 M0 真题整题搬进学生卷（无官方答案核验，违反候选纪律）。
