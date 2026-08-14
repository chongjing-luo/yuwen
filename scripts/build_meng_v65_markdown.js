#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const lesson = require("./meng_v65/lesson");

const PROJECT_ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.join(PROJECT_ROOT, "work", "备课", "选择性必修下册", "氓", "_v62_stage", "v65", "package");
const SCRIPT_OUT = path.join(OUT_DIR, "04A_氓_V65_45页逐页真实剧本_V4.md");
const MASTER_OUT = path.join(OUT_DIR, "02_氓_V65_45页教学母版_V4.md");

function scriptMarkdown() {
  const lines = [
    "---", "document_type: page_by_page_real_rehearsal_script", `version: ${lesson.version}`,
    "status: no_image_implementation_candidate", "claim_boundary: 桌面排演稿，不声称真实课堂已经发生或学生已经学会", "---", "",
    `# 《氓》V6.5：${lesson.target_pages}页逐页真实剧本`, "",
  ];
  for (const page of lesson.pages) {
    lines.push(`## ${String(page.page_number).padStart(2, "0")}｜${page.page_id}｜${page.title}（${page.minutes}分钟）`, "");
    lines.push(`**本页意义：** ${page.unique_function}`, "");
    lines.push(`**学生实际动作：** ${page.student_action.join("；")}`, "");
    lines.push(`**场景：** ${page.script.scene}`, "");
    lines.push("**教师台词：**", "", page.script.teacher_spoken, "");
    lines.push("**舞台动作：**", "");
    for (const item of page.script.stage_directions) lines.push(`- ${item}`, "");
    lines.push(`**时间盒：** ${page.script.timeboxes.map((item) => `${item.label}${item.seconds}秒`).join("；")}`, "");
    lines.push("**现场分支：**", "");
    for (const branch of page.script.branches) lines.push(`- ${branch.kind}：${branch.response}`, "");
    lines.push(`**听者任务：** ${page.script.listener_task}`, "");
    lines.push(`**证据位置：** ${page.script.evidence_location}`, "");
    lines.push(`**首次后用：** ${page.next_use}`, "");
    lines.push(`**切页句：** ${page.script.cut_line}`, "");
  }
  return `${lines.join("\n").trimEnd()}\n`;
}

function masterMarkdown() {
  const lines = [
    "---", "document_type: teaching_master", `version: ${lesson.version}`,
    "status: no_image_implementation_candidate", `target_pages: ${lesson.target_pages}`, `target_natural_minutes: ${lesson.target_natural_minutes}`, "---", "",
    "# 《氓》V6.5教学母版", "",
    "## 课程脊柱", "",
    "广泛回忆爱情与婚姻文学—完整听诗—沿六章逐句读懂—统整女子经历—把不幸还原为生活—沿时间分析原因—讨论良好共同生活的支点—收纳《诗经》、字词与语言艺术—完整终读。", "",
    "## 三个全文问题", "",
    ...lesson.three_questions.map((question, index) => `${index + 1}. ${question}`), "",
    "## 逐页结构", "",
    "| 页 | ID | 分钟 | 页面意义 | 学生动作 | 产物 | 首次后用 |", "|---:|---|---:|---|---|---|---|",
  ];
  for (const page of lesson.pages) {
    lines.push(`| ${String(page.page_number).padStart(2, "0")} | ${page.page_id} | ${page.minutes} | ${page.unique_function} | ${page.student_action.join("；")} | ${page.artifact} | ${page.next_use} |`);
  }
  lines.push("", "## 知识总结", "", "- 《诗经》：我国最早的诗歌总集，305篇；风、雅、颂；《氓》出自《卫风》。", "- 核心字词在原句中读准、释准，并保留完整逐句批注。", "- 第一人称六章叙事；桑叶比兴与前后对照；由物及人的起兴与呼告；复现、回环、同词反折。", "- 四言节奏、叠词、正面对照和叙事抒情交融。", "- 人物责任与解释边界：不把女子投入写成男子伤害的原因，不把婚前警讯说成已证预谋，不把末句说成已经实际出走。", "- 现实理解由学生讨论生成：审慎了解，承诺和行动一致，劳动与决定不长期失衡，伤害责任不转嫁，困难时有理解托举，旧日美好不能为后来伤害免责。", "");
  return `${lines.join("\n").trimEnd()}\n`;
}

function build() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.writeFileSync(SCRIPT_OUT, scriptMarkdown(), "utf8");
  fs.writeFileSync(MASTER_OUT, masterMarkdown(), "utf8");
  process.stdout.write(`MENG_V65_MARKDOWN_OK pages=${lesson.pages.length} outputs=2\n`);
}

if (require.main === module) build();
module.exports = { build, SCRIPT_OUT, MASTER_OUT, scriptMarkdown, masterMarkdown };
