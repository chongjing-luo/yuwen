#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const source = require("./meng_v62/content/chapter_1");
const { validate } = require("./verify_meng_v62_chapter1");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const OUT = assertV62OutputPath(path.join(stageDir(), "chapter_1", "package"));
const SOURCE_FILE = path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "chapter_1.js");

function sha256(value) { return crypto.createHash("sha256").update(value).digest("hex"); }
function fileSha(filePath) { return sha256(fs.readFileSync(filePath)); }
function marker(pageId) { return `<!-- V62_PAGE:${pageId} -->`; }

function renderLesson(data, sourceSha) {
  const lines = [
    "---", "document_type: teaching_master", "lesson: \"《氓》第一章\"",
    "version: \"6.2-chapter1-five-event\"", "claim_boundary: \"desktop_design_scaffold_only\"",
    `source_sha256: \"${sourceSha}\"`, "---", "", "# 《氓》V6.2第一章教学母版", "",
    "> 第一章先完整进入，再沿三个意义句群细读，最后撤去局部支架重建故事。每页只解决一个不可替代的文学困难；本稿是可排演方案，不声称未经试教的学习效果。", "",
    `- 逻辑页：${data.pages.length}页`, `- 自然时长：${data.total_minutes}分钟`,
    "- 学生材料：C101才发CH1-A；完成整章初读后，C102才发CH1-B。",
    "- 插图政策：全课功能冻结前不加入人物插图；本章用原诗、声音、空间和故事轨道构成视觉。", "",
  ];
  for (const page of data.pages) {
    lines.push(marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "",
      "### 为什么必须有这一页", "", `- 文学对象：${page.literary_object}`, `- 当前困难：${page.current_difficulty}`,
      `- 唯一功能：${page.unique_function}`, `- 删除损失：${page.deletion_loss}`, `- 相邻合并测试：${page.merge_test}`, "",
      "### 学生此刻看见", "", "```text", page.visible, "```", "", `第一眼：${page.first_glance}`, "",
      "### 信息边界", "", `- 已知：${page.information_state.known}`, `- 本页揭示：${page.information_state.reveal_now}`,
      `- 继续后置：${page.information_state.defer}`, "", "### 学生怎样生成", "");
    for (const action of page.student_action) lines.push(`- ${action}`);
    lines.push("", `- 留下的作品：${page.artifact}`, `- 正常路径：${page.normal_path}`, `- 有界反馈：${page.bounded_feedback}`,
      `- 修订：${page.revision}`, "", "### 教师怎样后置校准", "", page.teacher_synthesis, "",
      `- 回到人物和故事：${page.story_return}`, `- 后续真实调用：${page.next_use}`, `- 视觉职责：${page.visual_duty}`,
      `- 学生第一人称接收：${page.first_person_reception}`, "");
  }
  return `${lines.join("\n").trim()}\n`;
}

function renderInitialCard(data) {
  const poem = data.chapter_text.map((line) => `${line}。`).join("\n");
  return `---
document_type: chapter_initial_read_card
lesson: "《氓》第一章"
version: "6.2-chapter1-initial-read"
distribution: "C101 only"
information_boundary: "no gloss, paraphrase, chapter meaning, character judgment, or later fact"
---

# 第一章｜两个人怎样走近婚事

${poem}

## 先把整章读完

- 圈一圈男子做的事。
- 划一划女子做的事。
- 暂时不懂的词，留下“？”；先别让一个词拦住整章。

同桌只核对：“这一处是谁做的？”

我回到原诗补画或改画的一处：________________________________________
`;
}

function renderCloseReadingCard(data) {
  const p = Object.fromEntries(data.pages.map((item) => [item.page_id, item]));
  return `---
document_type: chapter_close_reading_and_story_rail
lesson: "《氓》第一章"
version: "6.2-chapter1-close-reading"
distribution: "C102 only; distribute after C101 complete initial reading"
information_boundary: "no prefilled gloss, paraphrase, chapter meaning, character label, or later fact"
---

# 第一章｜细读与故事轨道

## 一、抱布而来，是为了什么？

${p.C102.original_text}

诗先让我们看见：____________________________________________________

女子随后告诉我们：__________________________________________________

哪个字，让话转了弯？____________

把两句说成一句自然话：________________________________________________

教师校准后，我 □保留原话　□改准这一处：______________________________

## 二、她把他送了多远？

${p.C103.original_text}

送　　　　　　　　　涉　　　　　　　　　至

先用手指走一遍，再亲手留下送行线；只保存诗里真正写出的次序。

把三个动作说成一句自然话：____________________________________________

## 三、她怎样把婚事继续说下去？

${p.C104.original_text}

这四小句，各在做什么？先用自己的词写，不等教师分层：

1. ______________________________　2. ______________________________

3. ______________________________　4. ______________________________

我把第____、____小句合在一起，因为：____________________________________

我的停顿或重音：______________________________________________________

听者实际没听清的一处：________________　我改读的一处：________________

“无怒”将在第五章C503随婚后事实重新打开；此处不另设个人回看栏。

## 四、再读第一章，把故事讲完整

教材合上；03A、03B都翻到背面；屏幕熄暗以后，再讲30秒。

口头支架：他怎样来｜她怎样送｜婚事怎样暂缓又约定

听者只补一个真正遗漏：________________________________________________

我回到的原句：________________________　补说：________________________

### 六章故事轨道

| 第一章 | 第二章 | 第三章 | 第四章 | 第五章 | 第六章 |
|---|---|---|---|---|---|
|  |  |  |  |  |  |

第一章一句自然章意：____________________________________________________

`;
}

function renderScript(data, sourceSha) {
  const lines = [
    "---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》第一章\"",
    "version: \"6.2-chapter1-five-event\"", "claim_boundary: \"scripted_not_observed\"",
    `source_sha256: \"${sourceSha}\"`, "---", "", "# 《氓》V6.2第一章逐页无生试讲稿", "",
    "> 每页都是可直接排演的真实课堂场景。括号内动作用于教师排演，不显示在PPT前台。", "",
  ];
  for (const page of data.pages) {
    const s = page.script;
    lines.push(marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "",
      "【本页不可替代的意义】", "", page.unique_function, "", "【删除本页会失去什么】", "", page.deletion_loss, "",
      "【场面】", "", s.scene, "", "【教师实际说】", "", `“${s.teacher_spoken}”`, "",
      "【动作、等待与走位】", "");
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
  const verification = validate(source);
  if (!verification.ok) throw new Error(`chapter1 contract failed: ${JSON.stringify(verification.errors)}`);
  const sourceSha = fileSha(SOURCE_FILE);
  fs.mkdirSync(OUT, { recursive: true });
  const snapshot = { ...source, source_sha256: sourceSha, claim_boundary: "desktop_design_scaffold_only" };
  const outputs = [
    ["02_氓_V62第一章教学母版.md", renderLesson(source, sourceSha)],
    ["03A_氓_V62第一章初读卡_C101发.md", renderInitialCard(source)],
    ["03B_氓_V62第一章细读与故事轨道_C102发.md", renderCloseReadingCard(source)],
    ["04A_氓_V62第一章逐页无生试讲稿.md", renderScript(source, sourceSha)],
    ["06_氓_V62第一章课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(OUT, name), content, "utf8");
  const manifest = {
    schema_version: "1.0", module_id: source.module_id, version: source.version, source_sha256: sourceSha,
    distribution_order: ["03A at C101; complete poem and action marking only", "03B at C102 after C101; open prompts and blank story rail only"],
    files: outputs.map(([name]) => ({ name, sha256: fileSha(path.join(OUT, name)) })),
  };
  fs.writeFileSync(path.join(OUT, "chapter1_package_manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`V62_CHAPTER1_MARKDOWN_OK pages=${source.pages.length} minutes=${source.total_minutes} out=${OUT}\n`);
}

if (require.main === module) main();
module.exports = { renderLesson, renderInitialCard, renderCloseReadingCard, renderScript };
