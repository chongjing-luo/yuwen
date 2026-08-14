#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const chapter = require("./meng_v6/content/chapter_1.js");
const notes = require("./meng_v6/chapter1_notes.js");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "chapter_1", "package");

function sha256(value) { return crypto.createHash("sha256").update(value).digest("hex"); }
function fileSha(filePath) { return sha256(fs.readFileSync(filePath)); }
function marker(pageId) { return `<!-- V6_PAGE:${pageId} -->`; }

function compilePages() {
  return chapter.pages.map((source) => {
    const note = notes[source.page_id];
    if (!note) throw new Error(`missing notes ${source.page_id}`);
    const timeboxes = note.timeboxes.map(([label, seconds]) => ({ label, seconds }));
    if (timeboxes.reduce((sum, item) => sum + item.seconds, 0) !== source.minutes * 60) {
      throw new Error(`${source.page_id} timeboxes do not equal minutes`);
    }
    return {
      ...source,
      script: {
        scene: note.scene,
        teacher_spoken: source.teacher_script,
        stage_directions: note.directions,
        timeboxes,
        branches: note.branches.map(([kind, response]) => ({ kind, response })),
        listener_task: source.listener_task,
        evidence_location: source.artifact_location,
        cut_line: note.cut,
      },
    };
  });
}

function renderLesson(pages, sourceSha) {
  const lines = [
    "---", "document_type: teaching_master", "lesson: \"《氓》第一章\"", "version: \"6.8-chapter1-source-grown\"",
    "claim_boundary: \"desktop_design_scaffold_only\"", `source_sha256: \"${sourceSha}\"`, "---", "",
    "# 《氓》V6第一章教学母版", "",
    "> 本切片承接已经通过双审的导入，从第一章完整声音进入逐句释义、行动重建、初见档案和整章回读；不声称未经试教的学生效果。", "",
    `- 页面：${pages.length}页`, `- 自然时长：${pages.reduce((sum, page) => sum + page.minutes, 0)}分钟`,
    "- 当前不放人物插图；待页面功能冻结后，才对确有动作/空间理解收益的页面做A/B入页测试。", "",
  ];
  for (const page of pages) {
    lines.push(marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "", "### 本页意义", "", page.unique_function, "", "### 学生此刻看见", "", "```text", page.visible, "```", "");
    if (page.glosses) {
      lines.push("### 教师定点释义", "");
      for (const [term, gloss] of Object.entries(page.glosses)) lines.push(`- ${term}：${gloss}`);
      lines.push("", `校准后的自然话：${page.natural_paraphrase}`, "");
    }
    lines.push("### 课堂实施", "", page.teacher_script, "", `- 学生活动：${page.student_action}`, `- 听者任务：${page.listener_task}`, `- 反馈与修订：${page.feedback_revision}`, `- 作品位置：${page.artifact_location}`, `- 后页接续：${page.next_event_id}`, "");
  }
  return `${lines.join("\n").trim()}\n`;
}

function renderWorksheet() {
  return `---
document_type: student_worksheet
lesson: "《氓》第一章"
version: "6.8-chapter1-source-grown"
---

# 《氓》第一章学习单｜让五句诗重新成为一段话

## 一、完整读第一章

氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。送子涉淇，至于顿丘。匪我愆期，子无良媒。将子无怒，秋以为期。

圈出男子的动作，划出女子的动作。有疑问先留“？”，不要停在一个词上。

## 二、逐句先说，再校准

### 1. 氓之蚩蚩，抱布贸丝

谁：____________　怎样：____________　拿什么：____________　做什么：____________

我先说成的自然话：____________________________________________________

同桌核对：□人物　□样子　□布　□交换动作

换笔修订：____________________________________________________________

### 2. 匪来贸丝，来即我谋

诗句先写的动作：__________________________________________________

女子随后说明的来意：____________________________________________

让意思转过来的字：________　换笔修订：_______________________________

### 3. 送子涉淇，至于顿丘

送行路线：________ → ________ → ________　行动主体：________

我先说成的自然话：____________________________________________________

换笔修订：____________________________________________________________

### 4. 匪我愆期，子无良媒

我先圈：□她在拒绝这门婚事　□她在说明此刻不能成婚的条件

托住判断的原词：________________　教师校准后，我 □保留　□换笔修改

我先说成的自然话：____________________________________________________

换笔修订：____________________________________________________________

### 5. 将子无怒，秋以为期

她先在劝什么：________________________　她又把什么定下来：________________

我的重音与停顿：______________________________________________________

同桌实际听见了：______________________　换笔修订：____________________

## 三、合上书，重建五步行动链

独立写五步，只写人物和动作；同桌只找断点，不报答案。

1. ____________________　2. ____________________　3. ____________________

4. ____________________　5. ____________________

翻书定位后换笔修订：__________________________________________________

## 四、第一章初见札记

| 诗里写着 | 初读时我觉得 | 现在还说不准 |
|---|---|---|
|  |  |  |
| 原词： | 原词： |  |

同桌质询后，我 □保留　□把话说轻一点　□移动了第____栏的一条判断。

## 五、让第一章成为一段话

30秒旁白：男子怎样来｜女子怎样回应｜婚期怎样定

听者提醒我补回：______________________________________________________

第一章一句章意：______________________________________________________
`;
}

function renderScript(pages, sourceSha) {
  const lines = [
    "---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》第一章\"", "version: \"6.8-chapter1-source-grown\"",
    "claim_boundary: \"scripted_not_observed\"", `source_sha256: \"${sourceSha}\"`, "---", "",
    "# 《氓》V6第一章逐页无生试讲稿", "",
    "> 每页均为可直接排演的真实场景。括号内动作不念给学生。", "",
  ];
  for (const page of pages) {
    lines.push(marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "", "【承接与场面】", page.script.scene, "", "【教师实际说】", `“${page.script.teacher_spoken}”`, "", "【动作、等待与走位】");
    for (const item of page.script.timeboxes) lines.push(`- ${item.label}：${item.seconds}秒`);
    for (const item of page.script.stage_directions) lines.push(`- （${item}）`);
    lines.push("", "【现场分支】");
    for (const branch of page.script.branches) lines.push(`- ${branch.kind}：${branch.response}`);
    lines.push("", "【听者同时做什么】", page.script.listener_task, "", "【留下什么】", `${page.script.evidence_location}。`, "", "【怎样接下去】", `“${page.script.cut_line}”`, "");
  }
  return `${lines.join("\n").trim()}\n`;
}

function main() {
  const pages = compilePages();
  const sourceSha = sha256(Buffer.from(JSON.stringify({ chapter, notes })));
  fs.mkdirSync(OUT, { recursive: true });
  const snapshot = { schema_version: "1.0", lesson_version: "6.8-chapter1-source-grown", source_sha256: sourceSha, page_ids: pages.map((page) => page.page_id), total_minutes: pages.reduce((sum, page) => sum + page.minutes, 0), pages };
  const outputs = [
    ["02_氓_V6第一章教学母版.md", renderLesson(pages, sourceSha)],
    ["03_氓_V6第一章学习单.md", renderWorksheet()],
    ["04A_氓_V6第一章逐页无生试讲稿.md", renderScript(pages, sourceSha)],
    ["06_氓_V6第一章课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(OUT, name), content, "utf8");
  const manifest = { schema_version: "1.0", source_sha256: sourceSha, files: outputs.map(([name]) => ({ name, sha256: fileSha(path.join(OUT, name)) })) };
  fs.writeFileSync(path.join(OUT, "chapter1_package_manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`CHAPTER1_MARKDOWN_OK pages=${pages.length} minutes=${snapshot.total_minutes}\n`);
}

if (require.main === module) main();

module.exports = { compilePages, renderLesson, renderWorksheet, renderScript };
