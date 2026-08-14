#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const source = require("./meng_v62/content/opening");
const { validate } = require("./verify_meng_v62_opening");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const OUT = assertV62OutputPath(path.join(stageDir(), "opening", "package"));
const SOURCE_FILE = path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "opening.js");

function sha256(value) { return crypto.createHash("sha256").update(value).digest("hex"); }
function fileSha(filePath) { return sha256(fs.readFileSync(filePath)); }
function marker(pageId) { return `<!-- V62_PAGE:${pageId} -->`; }

function renderLesson(data, sourceSha) {
  const lines = [
    "---",
    "document_type: teaching_master",
    "lesson: \"《氓》导入\"",
    "version: \"6.3-opening-parallel-literary-recall\"",
    "claim_boundary: \"desktop_design_scaffold_only\"",
    `source_sha256: \"${sourceSha}\"`,
    "---",
    "",
    "# 《氓》V6.3导入教学母版",
    "",
    "> 本导入先让全班广泛唤醒爱情、婚姻文学记忆，由教师依据现场发言后置归纳，再揭题、完整听读并保存个人初听。这里记录的是可排演方案，不声称未经试教的学生效果。",
    "",
    `- 逻辑页：${data.pages.length}页`,
    `- 自然时长：${data.total_minutes}分钟；全员发言主要在同桌与四人组并行发生，公共阶段只保存能扩展班级文学版图的材料`,
    "- 插图政策：导入功能冻结前不加入人物插图；页面视觉只承担书写、聚拢、原诗可读和关系定位。",
    "- 放行条件：每页必须能说明当前困难、唯一功能、学生动作、作品位置、故事回接、后续调用和删除损失。",
    "",
  ];
  for (const page of data.pages) {
    lines.push(
      marker(page.page_id),
      `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`,
      "",
      "### 这页为什么存在",
      "",
      `- 文学对象：${page.literary_object}`,
      `- 当前困难：${page.current_difficulty}`,
      `- 唯一功能：${page.unique_function}`,
      `- 删除损失：${page.deletion_loss}`,
      "",
      "### 学生此刻看见",
      "",
      "```text",
      page.visible,
      "```",
      "",
      `第一眼：${page.first_glance}`,
      "",
      "### 学生怎样参与",
      "",
    );
    for (const action of page.student_action) lines.push(`- ${action}`);
    lines.push(
      "",
      `- 留下的作品：${page.artifact}`,
      `- 正常反例：${page.normal_path}`,
      `- 有界反馈：${page.bounded_feedback}`,
      `- 修订机会：${page.revision}`,
      "",
      "### 教师怎样收束",
      "",
      page.teacher_synthesis,
      "",
      `- 回到人物和故事：${page.story_return}`,
      `- 后续真实调用：${page.next_use}`,
      `- 视觉职责：${page.visual_duty}`,
      "",
    );
  }
  return `${lines.join("\n").trim()}\n`;
}

function renderRecallSheet() {
  return `---
document_type: literature_recall_sheet
version: "6.3-love-and-marriage-literature-recall"
distribution: "O01 only"
---

# 爱情与婚姻文学回忆单

## 一、我们还记得哪些爱情与婚姻故事？

从小学一直想到高中，在读过的语文课文、小说或整本书中回想。先用一句平常话把故事唤回来，再写它让你想到爱情或婚姻中的什么。

| 篇名 | 一句话唤回故事 | 它让我想到什么 |
|---|---|---|
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |
|  |  |  |

只记得情节，也可以先留下情节；听同伴以后再补最后一栏。

听见自己没有想到的作品或同一篇作品的另一层意思，再补一项：

________________________________________________________________________

`;
}

function renderInitialResponseCard() {
  return `---
document_type: initial_response_card
lesson: "《氓》"
version: "6.2-opening-initial-response"
distribution: "O07 only; distribute after the first complete listening"
---

# 把第一次听见的《氓》留在纸上

“____________________________________________________________________”

我看见／我听见／我想问：

________________________________________________________________________

同桌的话让我多注意到：

________________________________________________________________________
`;
}

function renderQuestionBookmark() {
  return `---
document_type: post_listening_reading_bookmark
lesson: "《氓》导入"
version: "6.2-opening-post-listening"
distribution: "O08 only; do not distribute before the first complete listening and O07 response"
---

# 《氓》三问阅读书签｜完整听读后再发

1. 她经历了什么？
2. 她婚后的不幸，在生活中是什么样子？
3. 这场婚姻为什么走到这一步？

第一问跟着事情走；第二问落到她具体过着的日子；第三问等事实一件件出现以后再判断。

我的初步判断只写在这里，读到新的原句以后可以补充、改写或撤回：

________________________________________________________________________
`;
}

function renderScript(data, sourceSha) {
  const lines = [
    "---",
    "document_type: page_by_page_rehearsal_script",
    "lesson: \"《氓》导入\"",
    "version: \"6.3-opening-parallel-literary-recall\"",
    "claim_boundary: \"scripted_not_observed\"",
    `source_sha256: \"${sourceSha}\"`,
    "---",
    "",
    "# 《氓》V6.3导入逐页无生试讲稿",
    "",
    "> 这是可直接排演的课堂剧本。括号内动作不念给学生；PPT页脚不显示方法论，完整台词只进入备注与本稿。",
    "",
  ];
  for (const page of data.pages) {
    const s = page.script;
    lines.push(
      marker(page.page_id),
      `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`,
      "",
      "【场面】",
      "",
      s.scene,
      "",
      "【教师实际说】",
      "",
      `“${s.teacher_spoken}”`,
      "",
      "【动作、等待与走位】",
      "",
    );
    for (const item of s.timeboxes) lines.push(`- ${item.label}：${item.seconds}秒`);
    for (const item of s.stage_directions) lines.push(`- （${item}）`);
    lines.push("", "【现场分支】", "");
    for (const branch of s.branches) lines.push(`- ${branch.kind}：${branch.response}`);
    lines.push(
      "",
      "【听者同时做什么】",
      "",
      s.listener_task,
      "",
      "【证据留在哪里】",
      "",
      s.evidence_location,
      "",
      "【怎样自然切页】",
      "",
      `“${s.cut_line}”`,
      "",
    );
  }
  return `${lines.join("\n").trim()}\n`;
}

function main() {
  const verification = validate(source);
  if (!verification.ok) throw new Error(`opening contract failed: ${JSON.stringify(verification.errors)}`);
  const sourceSha = fileSha(SOURCE_FILE);
  fs.mkdirSync(OUT, { recursive: true });
  const snapshot = {
    ...source,
    source_sha256: sourceSha,
    claim_boundary: "desktop_design_scaffold_only",
  };
  const outputs = [
    ["02_氓_V62导入教学母版.md", renderLesson(source, sourceSha)],
    ["03A_爱情与婚姻文学回忆单_O01发.md", renderRecallSheet()],
    ["03B_氓_V62初听卡_O07发.md", renderInitialResponseCard()],
    ["03C_氓_V62三问阅读书签_O08发.md", renderQuestionBookmark()],
    ["04A_氓_V62导入逐页无生试讲稿.md", renderScript(source, sourceSha)],
    ["06_氓_V62导入课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(OUT, name), content, "utf8");
  const manifest = {
    schema_version: "1.0",
    module_id: source.module_id,
    version: source.version,
    source_sha256: sourceSha,
    files: outputs.map(([name]) => ({ name, sha256: fileSha(path.join(OUT, name)) })),
  };
  fs.writeFileSync(path.join(OUT, "opening_package_manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`V62_OPENING_MARKDOWN_OK pages=${source.pages.length} minutes=${source.total_minutes} out=${OUT}\n`);
}

if (require.main === module) main();
module.exports = { renderLesson, renderRecallSheet, renderInitialResponseCard, renderQuestionBookmark, renderScript };
