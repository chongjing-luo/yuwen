"use strict";

/**
 * 作业包构建器（S7 环节）：从 homework_package.json 同源生成
 * - 学生作业单（分层、闭卷说明、无答案、有反例路径）
 * - 教师批改要点（预期证据、反馈触发、KP 绑定、两本账边界）
 * 同源纪律（P-11）：两份产物均由同一 JSON 生成，不手工分叉。
 */
const fs = require("fs");
const path = require("path");

function readPackage(packagePath) {
  const raw = fs.readFileSync(packagePath, "utf-8");
  return JSON.parse(raw);
}

function tierBadge(tier, tiers) {
  const rule = (tiers && tiers[tier]) || "";
  return `- **${tier}**${rule ? `（${rule}）` : ""}`;
}

function buildStudentSheet(pkg) {
  const lines = [];
  lines.push(`# 作业单：${pkg.lesson_ref.lesson_title}`);
  lines.push("");
  lines.push(`> ${pkg.retrieval_note || ""}`);
  lines.push("");
  Object.entries(pkg.tiers || {}).forEach(([tier, rule]) => lines.push(`- **${tier}**：${rule}`));
  lines.push("");
  (pkg.items || []).forEach((item) => {
    lines.push(`## 第${item.item_id.replace("HW-", "")}题（${item.tier} · 约 ${item.time_budget_minutes} 分钟）`);
    lines.push("");
    lines.push(item.prompt);
    lines.push("");
    lines.push(`*如果遇到困难：${item.normal_path}*`);
    lines.push("");
  });
  lines.push("---");
  lines.push("");
  lines.push(`写不完时优先保证闭卷部分真实完成；订正痕迹和“我原来以为”的记录都是作业的一部分。`);
  lines.push("");
  return lines.join("\n");
}

function buildTeacherKey(pkg) {
  const lines = [];
  lines.push(`# 教师批改要点：${pkg.homework_id}`);
  lines.push("");
  lines.push(`- 课程数据：\`${pkg.lesson_ref.lesson_js}\`（${pkg.lesson_ref.lesson_pages} 页）`);
  lines.push(`- 知识卡：${(pkg.lesson_ref.card_refs || []).join("、")}`);
  lines.push(
    `- KP 范围：${(pkg.kp_scope.kp_ids || []).join("、")}${(pkg.kp_scope.deferred || []).length ? `；defer：${pkg.kp_scope.deferred.map((d) => `${d.kp_id}（${d.reason}）`).join("；")}` : ""}`
  );
  lines.push(`- 必做时长：见 validate_homework_package.py 输出；上限 ${pkg.max_total_time_minutes} 分钟`);
  lines.push("");
  (pkg.items || []).forEach((item) => {
    lines.push(`## 第${item.item_id.replace("HW-", "")}题（${item.tier} · ${item.retrieval_mode}）`);
    lines.push("");
    lines.push(`- **知识点**：${(item.kp_ids || []).join("、")}`);
    lines.push(`- **课堂回链**：${(item.page_refs || []).join("、")}；依赖产物：${item.artifact_ref || "—"}`);
    lines.push(`- **预期证据**：${item.expected_evidence}`);
    lines.push(`- **反馈触发（批改后学生的修订动作）**：${item.feedback_trigger}`);
    lines.push(`- **反例路径**：${item.normal_path}`);
    lines.push("");
  });
  lines.push("## 边界声明");
  lines.push("");
  lines.push(pkg.claim_boundary || "");
  lines.push("");
  lines.push("批改产出：错因类型标注 → 输入 mastery ledger（scripts/analyze_mastery.py）；优秀迁移作品登记为下节课公共材料并真实取回。");
  lines.push("");
  return lines.join("\n");
}

function main() {
  const packagePath = process.argv[2];
  if (!packagePath) {
    console.error("用法: node scripts/build_homework_package.js <homework_package.json>");
    process.exit(1);
  }
  const pkg = readPackage(packagePath);
  if (!pkg.items || !pkg.items.length) {
    throw new Error("items 为空");
  }
  if (!pkg.claim_boundary || !pkg.claim_boundary.includes("课堂")) {
    throw new Error("claim_boundary 缺失或未声明课堂边界（P-12）");
  }
  const outDir = path.dirname(path.resolve(packagePath));
  const studentPath = path.join(outDir, `学生作业单_${pkg.homework_id}.md`);
  const teacherPath = path.join(outDir, `教师批改要点_${pkg.homework_id}.md`);
  fs.writeFileSync(studentPath, buildStudentSheet(pkg), "utf-8");
  fs.writeFileSync(teacherPath, buildTeacherKey(pkg), "utf-8");
  console.log(`学生作业单 → ${studentPath}`);
  console.log(`教师批改要点 → ${teacherPath}`);
}

if (require.main === module) {
  main();
}

module.exports = { readPackage, buildStudentSheet, buildTeacherKey };
