#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const chapter = require("./meng_v6/content/chapter_2.js");
const notes = require("./meng_v6/chapter2_notes.js");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "chapter_2", "package");

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
    "---", "document_type: teaching_master", "lesson: \"《氓》第二章\"", "version: \"6.9-chapter2-voice-contrast\"",
    "claim_boundary: \"desktop_design_scaffold_only\"", `source_sha256: "${sourceSha}"`, "---", "",
    "# 《氓》V6第二章教学母版", "",
    "> 本切片承接第一章旁白，以动作脉冲、视线、两句对照、双速度朗读、卜筮边界和对称行动推进；不复制第一章连续五页的校译节奏。", "",
    `- 页面：${pages.length}页`, `- 自然时长：${pages.reduce((sum, page) => sum + page.minutes, 0)}分钟`,
    "- 当前不放人物插图；页面功能双审冻结后，再判断视线空间或卜筮物件是否真的需要视觉资产。", "",
  ];
  for (const page of pages) {
    lines.push(marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "", "### 本页意义", "", page.unique_function, "", "### 学生此刻看见", "", "```text", page.visible, "```", "");
    if (page.line_glosses) {
      lines.push("### 教师定点释义", "");
      for (const [lineId, glosses] of Object.entries(page.line_glosses)) {
        lines.push(`#### ${lineId}`, "");
        for (const [term, gloss] of Object.entries(glosses)) lines.push(`- ${term}：${gloss}`);
        lines.push("", `校准后的自然话：${page.natural_paraphrases[lineId]}`, "");
      }
    }
    lines.push(
      "### 课堂实施", "", page.teacher_script, "",
      `- 学生活动：${page.student_action}`,
      `- 听者任务：${page.listener_task}`,
      `- 反馈与修订：${page.feedback_revision}`,
      `- 作品位置：${page.artifact_location}`,
      `- 可见变化：${page.observable_change}`,
      `- 主视觉职责：${page.primary_visual_duty}`,
      `- 后页接续：${page.next_event_id}`, "",
    );
  }
  return `${lines.join("\n").trim()}\n`;
}

function renderWorksheet() {
  return `---
document_type: student_worksheet
lesson: "《氓》第二章"
version: "6.9-chapter2-voice-contrast"
---

# 《氓》第二章学习单｜让等待在声音里起伏

## 一、完整读第二章

乘彼垝垣，以望复关。不见复关，泣涕涟涟。既见复关，载笑载言。尔卜尔筮，体无咎言。以尔车来，以我贿迁。

读到人物动作，轻点一下。带着感受的动作也可以写。读完写下三个最确定的动作：

________ → ________ → ________　换笔调序：____________________________

## 二、视线线条

乘彼垝垣，以望复关

女子所在处 ________　垝垣 ________　目光指向 ________

我画的是 □视线　□行走路线（核对后换笔修订）：________________________

## 三、两句对照

| 对照角度 | 上句原词 | 下句原词 |
|---|---|---|
| 视线条件 |  |  |
| 人物动作 |  |  |
| 语势原词 |  |  |

上句我先说成的自然话：____________________________________________

下句我先说成的自然话：____________________________________________

我用原词说转折：______________________________________________________

## 四、我的朗读谱

不见复关，泣涕涟涟。　既见复关，载笑载言。

慢下来的一处：________________　快起来的一处：________________

重音／停顿：__________________　原词理由：____________________________

## 五、听者回执

我在“____________”附近听见声音开始变化。

第一遍没有听清：________________　读者只改一处：____________________

第二遍：□更清楚　□仍需调整　若仍需调整，标“△待调整”，章末再试。

交换角色后我的修订：_________________________________________________

## 六、卜筮小注

卜：________________　筮：________________　体：________________

此次占问告诉他们：____________________________________________________

它不能替后来________________________________________________作保证。

## 七、以尔／以我

| 句式 | 主体 | 物件 | 动作 |
|---|---|---|---|
| 以尔车来 |  |  |  |
| 以我贿迁 |  |  |  |

## 八、从章首三步补出七个关键节点

写回第一部分的三个动作：________ → ________ → ________

下面七词中找得到的圈出；没有出现的动作照样保留，只要来自原诗。

乱序：迁　笑言　望　卜筮　泣　既见　不见

编号：_______________________________________________________________

排序完成后，在你自己的七词序列中圈出声音突然转向的一处，写下它位于第____与第____个节点之间，并用一道线连住前后两个节点。

同桌指出的断点：________________　翻诗后换笔修订：____________________

## 九、让第二章成为一段话

30秒旁白：她怎样等｜声音怎样转｜婚事怎样推进

听者提醒我补回：_____________________________________________________

第二章一句章意：_____________________________________________________
`;
}

function renderScript(pages, sourceSha) {
  const lines = [
    "---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》第二章\"", "version: \"6.9-chapter2-voice-contrast\"",
    "claim_boundary: \"scripted_not_observed\"", `source_sha256: "${sourceSha}"`, "---", "",
    "# 《氓》V6第二章逐页无生试讲稿", "",
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
  const snapshot = {
    schema_version: "1.0", lesson_version: "6.9-chapter2-voice-contrast", source_sha256: sourceSha,
    page_ids: pages.map((page) => page.page_id),
    total_minutes: pages.reduce((sum, page) => sum + page.minutes, 0), pages,
  };
  const outputs = [
    ["02_氓_V6第二章教学母版.md", renderLesson(pages, sourceSha)],
    ["03_氓_V6第二章学习单.md", renderWorksheet()],
    ["04A_氓_V6第二章逐页无生试讲稿.md", renderScript(pages, sourceSha)],
    ["06_氓_V6第二章课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(OUT, name), content, "utf8");
  const manifest = { schema_version: "1.0", source_sha256: sourceSha, files: outputs.map(([name]) => ({ name, sha256: fileSha(path.join(OUT, name)) })) };
  fs.writeFileSync(path.join(OUT, "chapter2_package_manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`CHAPTER2_MARKDOWN_OK pages=${pages.length} minutes=${snapshot.total_minutes}\n`);
}

if (require.main === module) main();

module.exports = { compilePages, renderLesson, renderWorksheet, renderScript };
