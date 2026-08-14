#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const source = require("./meng_v62/content/chapter_2");
const { validate } = require("./verify_meng_v62_chapter2");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const OUT = assertV62OutputPath(path.join(stageDir(), "chapter_2", "package"));
const SOURCE_FILE = path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "chapter_2.js");
function sha256(value) { return crypto.createHash("sha256").update(value).digest("hex"); }
function fileSha(filePath) { return sha256(fs.readFileSync(filePath)); }
function marker(pageId) { return `<!-- V62_PAGE:${pageId} -->`; }

function renderLesson(data, sourceSha) {
  const lines = [
    "---", "document_type: teaching_master", "lesson: \"《氓》第二章\"", "version: \"6.3-chapter2-four-event\"",
    "claim_boundary: \"desktop_design_scaffold_only\"", `source_sha256: \"${sourceSha}\"`, "---", "",
    "# 《氓》V6.2第二章教学母版", "",
    "> 第二章以视线、原词与声音合一、占问与迁移合一推进，最后撤答重建故事。四页保留全部核心体验，删除独立程序页；本稿不声称未经试教的学习效果。", "",
    `- 逻辑页：${data.pages.length}页`, `- 自然时长：${data.total_minutes}分钟`,
    "- 学生材料：完整章读和动作初稿完成后，C201中段才发CH2-A；C202才发CH2-B。",
    "- 插图政策：全课功能冻结前不加入人物插图；本章用原诗、视线、声音、文化名物和故事轨道形成视觉。", "",
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
document_type: chapter_initial_read_and_sightline_card
lesson: "《氓》第二章"
version: "6.3-chapter2-initial-read-sightline"
distribution: "C201 after the complete chapter reading; the three-action draft is written here, not in the textbook"
information_boundary: "no gloss, contrast answer, divination boundary, migration paraphrase, chapter meaning, or later fact"
---

# 第二章｜初读与视线

${poem}

## 一、完整读章以后，先保留自己的动作初稿

我最确定的三个动作：____________ → ____________ → ____________

听同桌后，我只调整了一处先后：________________________________________

## 二、等待从哪里望向哪里？

乘彼垝垣，以望复关。

我的自然话：__________________________________________________________

女子所在：____________________　目光指向：____________________

只画一道目光，不画行走地图：

________________________________________________________________________

我回到“乘／望”修订的一处：____________________________________________
`;
}

function renderCloseReadingCard(data) {
  const p = Object.fromEntries(data.pages.map((item) => [item.page_id, item]));
  return `---
document_type: chapter_close_reading_and_story_rail
lesson: "《氓》第二章"
version: "6.3-chapter2-close-reading"
distribution: "C202 only; distribute after C201 complete reading and sightline"
information_boundary: "no prefilled translation, contrast answer, reading speed, divination boundary, parallel-action answer, chapter meaning, or later fact"
---

# 第二章｜细读与故事轨道

## 一、“不见”与“既见”：先看原词，再让耳朵检验

${p.C202.original_text}

上句自然话：__________________________________________________________

下句自然话：__________________________________________________________

我圈出的原词彼此怎样照应：____________________________________________

听同桌以后，我补回的一组原词：________________________________________

我只标一处声音变化；它依据的原词是：__________________________________

听者在“____________”附近 □听见变化　□没有听出

我只改这一处：________________________　第二遍：________________________

## 二、卜筮、来、迁：两句怎样接在一起？

${p.C204.original_text}

卜｜龟甲　　筮｜蓍草　　体｜兆象　　咎言｜不祥之语

我的自然话：__________________________________________________________

这次占问得到的结果：__________________________________________________

教师校准后，我 □保留　□删去越界词：____________　□补“这次”

| 句式 | 主体 | 物件 | 动作 |
|---|---|---|---|
| 以尔车来 |  |  |  |
| 以我贿迁 |  |  |  |

两项动作合回一句自然话：________________________________________________

两句怎样接起来：________________________________________________________

## 三、让第二章从等待走到迁移

教材合上；03A、03B都翻到背面；屏幕熄暗以后，再讲30秒。

口头支架：她怎样等｜见与不见怎样改变她｜婚事怎样走到迁移

听者只补一个真正遗漏：________________________________________________

我只打开教材定位的原句：________________　合书补说：__________________

### 六章故事轨道

| 第一章 | 第二章 | 第三章 | 第四章 | 第五章 | 第六章 |
|---|---|---|---|---|---|
| 已完成 |  |  |  |  |  |

第二章一句自然章意：____________________________________________________

后文再回看的原词：____________________________________________________
`;
}

function renderScript(data, sourceSha) {
  const lines = ["---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》第二章\"",
    "version: \"6.3-chapter2-four-event\"", "claim_boundary: \"scripted_not_observed\"", `source_sha256: \"${sourceSha}\"`,
    "---", "", "# 《氓》V6.2第二章逐页无生试讲稿", "",
    "> 每页都是可直接排演的真实课堂场景。括号内动作用于教师排演，不显示在PPT前台。", ""];
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
  const verification = validate(source);
  if (!verification.ok) throw new Error(`chapter2 contract failed: ${JSON.stringify(verification.errors)}`);
  const sourceSha = fileSha(SOURCE_FILE); fs.mkdirSync(OUT, { recursive: true });
  const snapshot = { ...source, source_sha256: sourceSha, claim_boundary: "desktop_design_scaffold_only" };
  const outputs = [
    ["02_氓_V62第二章教学母版.md", renderLesson(source, sourceSha)],
    ["03A_氓_V62第二章初读与视线卡_C201读后发.md", renderInitialCard(source)],
    ["03B_氓_V62第二章细读与故事轨道_C202发.md", renderCloseReadingCard(source)],
    ["04A_氓_V62第二章逐页无生试讲稿.md", renderScript(source, sourceSha)],
    ["06_氓_V62第二章课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(OUT, name), content, "utf8");
  const manifest = { schema_version: "1.0", module_id: source.module_id, version: source.version, source_sha256: sourceSha,
    distribution_order: ["03A during C201 only after complete chapter reading and action draft", "03B at C202 after C201 sightline; open prompts and blank story rail only"],
    files: outputs.map(([name]) => ({ name, sha256: fileSha(path.join(OUT, name)) })) };
  fs.writeFileSync(path.join(OUT, "chapter2_package_manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`V62_CHAPTER2_MARKDOWN_OK pages=${source.pages.length} minutes=${source.total_minutes} out=${OUT}\n`);
}
if (require.main === module) main();
module.exports = { renderLesson, renderInitialCard, renderCloseReadingCard, renderScript };
