#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const source = require("./meng_v62/content/synthesis");
const { validate } = require("./verify_meng_v62_synthesis");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const OUT = assertV62OutputPath(path.join(stageDir(), "synthesis", "package"));
const SRC = path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "synthesis.js");

function fileSha(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}
function marker(id) { return `<!-- V64_PAGE:${id} -->`; }

function master(data, sourceSha) {
  const lines = [
    "---", "document_type: synthesis_teaching_master", "lesson: \"《氓》全文三问、婚姻讨论与知识收束\"",
    `version: "${data.version}"`, `source_sha256: "${sourceSha}"`, "claim_boundary: \"desktop_design_scaffold_only\"", "---", "",
    "# 《氓》V6.4全文综合教学母版", "",
    `- 逻辑页：${data.pages.length}页`, `- 自然时长：${data.total_minutes}分钟`,
    "- 活动主链：个人生成 → 真实核查 → 本人按需修订。", "- 正常反例：不强制问号、修改、争议、分歧或未解问题。", "",
  ];
  for (const page of data.pages) {
    lines.push(
      marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "",
      `- 文学对象：${page.literary_object}`, `- 当前困难：${page.current_difficulty}`, `- 唯一功能：${page.unique_function}`,
      `- 学生动作：${page.student_action.join("；")}`, `- 作品：${page.artifact}`, `- 正常路径：${page.normal_path}`,
      `- 有界反馈：${page.bounded_feedback}`, `- 修订：${page.revision}`, `- 教师后置：${page.teacher_synthesis}`,
      `- 回到故事：${page.story_return}`, `- 后用：${page.next_use}`, `- 删除损失：${page.deletion_loss}`,
      `- 合并反证：${page.merge_test}`, `- 视觉职责：${page.visual_duty}`, `- 第一人称：${page.first_person_reception}`, "",
      "```text", page.visible, "```", "",
    );
  }
  return `${lines.join("\n").trim()}\n`;
}

function worksheet(data) {
  return `---
document_type: synthesis_student_materials
lesson: "《氓》全文综合"
version: "${data.version}"
distribution: "S01 after all six chapters; reveal one section just in time"
---

# 《氓》全文综合学习包

## S01｜她经历了什么？

请把第一至第六章六张章末卡按序放在桌面，再写六句人生：

一：________________________________________________________________

二：________________________________________________________________

三：________________________________________________________________

四：________________________________________________________________

五：________________________________________________________________

六：________________________________________________________________

同桌听见的真实断点：________________________________________________

若没有断点，最清楚的一处因果：________________________________________

我的处理：□按断点补说　□连贯，保留

第一问的一段答案：____________________________________________________

## S02｜把一处原句写成日常片刻

我选择的原句：________________________________________________________

第三人称日常片刻（20—35字）：________________________________________

同伴从文字中找回的原句：________________________________________________

同伴判断：□能配回　□配不回　□有诗中未写内容

我的处理：□删去虚构　□降低强度　□可配回，无需改

第二问的一段答案：____________________________________________________

## S03｜为什么走到这一步？

婚前值得警惕：________________________　原句：________________________

直接伤害责任：________________________　原句：________________________

使停止更困难：________________________　原句：________________________

诗中不能断言：________________________　边界：________________________

同桌只核：□责任与阻力分清　□事实与猜测分清

我的处理：□改弱／移层　□两项均通过，保留

第三问的一段答案：____________________________________________________

## S04｜重看开课时的爱情与婚姻主题

我选取的开课主题原话：________________________________________________

《氓》让我：□补充　□修正　□保留

我现在会这样说：______________________________________________________

托住它的原句：________________________________________________________

放进共同生活，我会观察这种行为：______________________________________

四人互证后：□修订　□有据，保留

## S05｜字词检索

《诗经》三项路标：____________________________________________________

从“愆、将、筮、说、徂、汤汤、渐、咥、隰、泮”中任选六个注音或释义：

______________________________________________________________________

我的真实错空项修复：__________________________________________________

进入S07的一项：_______________________________________________________

若全部准确，写一个最易混但已能解释的词：______________________________

## S06｜这些诗句，为什么非得这样写？

我选择：□桑叶荣枯　□两声于嗟　□信誓／反／不思

相照的原词：__________________________________________________________

声音或时间怎样改变：__________________________________________________

人物处境怎样显出：____________________________________________________

同桌用另一组原句检验：________________________________________________

我的处理：□按需修订　□迁移成立，保留

## S07｜我的语文知识书页

一个我已读准、说清的字词：____________　所在原句：____________________

一处我能讲明的写法：__________________________________________________

原词关系 → 声音／时间变化 → 人物处境：________________________________

诗写了：______________________________________________________________

诗没有写：____________________________________________________________

同桌定位：□三项可定位，保留　□返诗补准

## S08｜把理解与问题一起带走

她从____________________________走到____________________________。

她婚后的日子，让我看见______________________________________________。

这场婚姻走到这一步：__________________________________________________

我从《氓》带走的一条共同生活提醒：____________________________________

托住它的诗句：________________________________________________________

我仍愿继续追问：____________________________________________（可留白）

同桌只核一个事实边界：□边界准确，无需改　□作者已亲自修订
`;
}

function script(data, sourceSha) {
  const lines = [
    "---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》全文综合\"",
    `version: "${data.version}"`, `source_sha256: "${sourceSha}"`, "claim_boundary: \"scripted_not_observed\"", "---", "",
    "# 《氓》V6.4全文综合逐页无生试讲稿", "",
    "> 每页均为可真实演出的课堂剧本；舞台控制和设计理由只在本稿，不显示在学生前台。", "",
  ];
  for (const page of data.pages) {
    const s = page.script;
    lines.push(marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "",
      "【本页不可替代的意义】", "", page.unique_function, "", "【删除本页会失去什么】", "", page.deletion_loss, "",
      "【场面】", "", s.scene, "", "【教师实际说】", "", `“${s.teacher_spoken}”`, "", "【动作、等待与走位】", "");
    for (const item of s.timeboxes) lines.push(`- ${item.label}：${item.seconds}秒`);
    for (const item of s.stage_directions) lines.push(`- （${item}）`);
    lines.push("", "【现场分支】", "");
    for (const branch of s.branches) lines.push(`- ${branch.kind}：${branch.response}`);
    lines.push("", "【听者同时做什么】", "", s.listener_task, "", "【证据留在哪里】", "", s.evidence_location,
      "", "【回到人物和故事】", "", page.story_return, "", "【后续怎样真实调用】", "", page.next_use,
      "", "【怎样自然切页】", "", `“${s.cut_line}”`, "");
  }
  return `${lines.join("\n").trim()}\n`;
}

function main() {
  const report = validate(source);
  if (!report.ok) throw new Error(JSON.stringify(report.errors));
  const sourceSha = fileSha(SRC);
  fs.mkdirSync(OUT, { recursive: true });
  const snapshot = { ...source, source_sha256: sourceSha, claim_boundary: "desktop_design_scaffold_only" };
  const outputs = [
    ["02_氓_V64全文综合教学母版.md", master(source, sourceSha)],
    ["07G_氓_V64全文综合学习包.md", worksheet(source)],
    ["04A_氓_V64全文综合逐页无生试讲稿.md", script(source, sourceSha)],
    ["06_氓_V64全文综合课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(OUT, name), content, "utf8");
  fs.writeFileSync(path.join(OUT, "synthesis_v64_package_manifest.json"), `${JSON.stringify({
    schema_version: "1.2", module_id: source.module_id, version: source.version, source_sha256: sourceSha,
    files: outputs.map(([name]) => ({ name, sha256: fileSha(path.join(OUT, name)) })),
  }, null, 2)}\n`);
  process.stdout.write(`V64_SYNTHESIS_MARKDOWN_OK pages=${source.pages.length} minutes=${source.total_minutes} out=${OUT}\n`);
}

if (require.main === module) main();
module.exports = { master, worksheet, script };
