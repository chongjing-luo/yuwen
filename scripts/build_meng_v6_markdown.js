#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const opening = require("./meng_v6/content/opening.js");
const notes = require("./meng_v6/notes.js");

const root = path.resolve(__dirname, "..");
const defaultOut = path.join(root, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "opening", "package");
const auditPath = path.join(root, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "opening", "opening_audit.json");

function parseArgs(argv) {
  const result = { through: null, out: defaultOut };
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--through") result.through = argv[++index];
    else if (argv[index] === "--out") result.out = path.resolve(root, argv[++index]);
    else throw new Error(`unknown argument: ${argv[index]}`);
  }
  if (result.through !== "opening") throw new Error("only --through opening is implemented in this slice");
  return result;
}

function sha256(value) {
  return crypto.createHash("sha256").update(value).digest("hex");
}

function fileSha256(filePath) {
  return sha256(fs.readFileSync(filePath));
}

function pageMarker(pageId) {
  return `<!-- V6_PAGE:${pageId} -->`;
}

function enrichPages(audit) {
  const audited = new Map(audit.current_release_audit.pages.map((page) => [page.page_id, page]));
  return opening.pages.filter((page) => page.page_id !== "N006").map((source) => {
    const page = audited.get(source.page_id);
    if (!page) throw new Error(`opening audit is missing ${source.page_id}`);
    const note = notes[source.page_id];
    if (!note) throw new Error(`opening notes are missing ${source.page_id}`);
    const teacherSpoken = source.teacher_script;
    if (!teacherSpoken || teacherSpoken.length < 45) throw new Error(`${source.page_id} has no complete teacher script`);
    const timeboxes = note.timeboxes.map(([label, seconds]) => ({ label, seconds }));
    const branches = note.branches.map(([kind, response]) => ({ kind, response }));
    const compiled = {
      page_id: source.page_id,
      event_id: source.event_id,
      title: source.title,
      minutes: source.minutes,
      student_visible_text: source.visible,
      artifact_location: source.location,
      unique_function: source.function,
      observable_change: page.observable_change,
      channel_split: { ...page.channel_split, teacher: teacherSpoken },
      script: {
        scene: note.scene,
        teacher_spoken: teacherSpoken,
        stage_directions: note.directions,
        timeboxes,
        branches,
        listener_task: note.listener,
        evidence_location: source.location,
        cut_line: note.cut,
      },
    };
    const sum = timeboxes.reduce((total, item) => total + item.seconds, 0);
    if (sum !== source.minutes * 60) throw new Error(`${source.page_id} timeboxes=${sum} expected=${source.minutes * 60}`);
    return compiled;
  });
}

function renderLesson(pages, auditSha) {
  const lines = [
    "---", "document_type: teaching_master", "lesson: \"《氓》\"", "version: \"6.0-opening-slice\"",
    "claim_boundary: \"desktop_design_scaffold_only\"", `audit_sha256: \"${auditSha}\"`, "---", "",
    "# 《氓》V6导入切片教学母版", "",
    "> 本稿只覆盖导入、第一次完整听读与最小支架。它记录桌面设计条件，不声称真实学生已经参与、理解或学会。", "",
    "## 导入切片的课堂走向", "",
    "先让每个人从自己的语文记忆里找故事，再让四个人的记忆相遇，接着把八张真实贡献卡留在教室里。教师只沿现场材料整理，不预制婚姻答案；随后以三个朴素问题进入《氓》，完整听完六章，保存个人停顿，最后补足继续逐句阅读所需的最小《诗经》身份与四言节奏。", "",
    `- 页面：${pages.length}页`, `- 自然时长：${pages.reduce((sum, page) => sum + page.minutes, 0)}分钟`,
    "- 本切片无人物插图；题名、活动界面、真实卡墙、完整原诗和原文批注分别承担主视觉。", "",
  ];
  for (const page of pages) {
    lines.push(pageMarker(page.page_id), `## ${page.page_id}｜${page.title}`, "", `- 预计时间：${page.minutes}分钟`, `- 所属事件：${page.event_id}`, `- 学生作品位置：${page.artifact_location}`, "", "### 学生此刻看见", "", "```text", page.student_visible_text, "```", "", "### 课堂实施", "", page.script.teacher_spoken, "", `学生动作和时间以逐页剧本为准；听者同步任务：${page.script.listener_task}`, "", `本页留下：${page.observable_change.after}。判据：${page.observable_change.criterion}。`, "");
  }
  return `${lines.join("\n").trim()}\n`;
}

function renderWorksheetA() {
  return `---
document_type: student_worksheet
lesson: "《氓》"
version: "6.0-opening-slice-A"
---

# 《氓》V6导入学习单A｜旧故事与第一次听读

> 只谈作品或第三人称故事，不必公开私人经历。想不起、尚未找到或暂时不同意，都可以如实留下。

## 一、我读过的爱情或婚姻故事

每篇只写：篇名＋它写了什么。

1. 篇名：________________　它写了什么：________________________________

2. 篇名：________________　它写了什么：________________________________

3. 篇名：________________　它写了什么：________________________________

一时想不起：□翻教材目录　□领取一张只写篇名的提示条　□先听后补

## 二、四个人的小组作品谱

| 谁说的 | 篇名 | 它写了什么 |
|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |

听别人说时，我勾下的作品或主题：________________________________________

## 三、全班作品卡墙

我未想到的一项：________________________________________________________

看完八张卡，我发现的一处相近或不同：__________________________________

## 四、读完六章，再回答

一、她经历了什么？

二、她婚后的不幸，在生活中是什么样子？

三、这场婚姻为什么走到这一步？

我最想追踪的一问：□一　□二　□三

## 五、第一次完整听读

哪一句把你留了下来？

“______________________________________________________________________”

□我听见　□我看见　□我想问：________________________________________

如果暂时没有：□尚未找到；听同桌后，我 □补一句　□仍保留

同桌让我补记的一个不同之处：__________________________________________
`;
}

function renderWorksheetB() {
  return `---
document_type: student_worksheet_card
lesson: "《氓》"
version: "6.0-opening-slice-B"
distribution_timing: "after_first_listening_and_mark"
---

# 《氓》V6导入学习单B｜初听后的路标卡

> 教师在第一次完整听读和停顿交流完成后发下本卡。

## 一、三块最小路标

《诗经》篇数：305篇　｜　《氓》所属：《卫风》　｜　叙述者：女子第一人称

我用自己的话写下三块路标：____________________________________________

同桌各说一句：谁在回望什么？__________________________________________

## 二、先把前两句读顺

氓之／蚩蚩，抱布／贸丝。匪来／贸丝，来即／我谋。

先看斜线跟读，再看教材中没有斜线的原句互读。

同桌听见机械停顿时问“谁做什么”。我写下重读后改动的一处：____________
`;
}

function renderScript(pages, auditSha) {
  const lines = [
    "---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》\"", "version: \"6.0-opening-slice\"",
    "claim_boundary: \"scripted_not_observed\"", `audit_sha256: \"${auditSha}\"`, "---", "",
    "# 《氓》V6导入切片逐页无生试讲稿", "",
    "> 以下是可以直接排演的真实课堂剧本，不是提纲。括号内为动作，不念给学生；引号内或“教师实际说”段为将真实说出的台词。", "",
  ];
  for (const page of pages) {
    lines.push(pageMarker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "", "【承接与场面】", page.script.scene, "", "【教师实际说】", `“${page.script.teacher_spoken}”`, "", "【动作、等待与走位】");
    for (const item of page.script.timeboxes) lines.push(`- ${item.label}：${item.seconds}秒`);
    for (const item of page.script.stage_directions) lines.push(`- （${item}）`);
    lines.push("", "【现场分支】");
    for (const branch of page.script.branches) lines.push(`- ${branch.kind}：${branch.response}`);
    lines.push("", "【听者同时做什么】", page.script.listener_task, "", "【留下什么】", `${page.script.evidence_location}。`, "", "【怎样接下去】", `“${page.script.cut_line}”`, "");
  }
  return `${lines.join("\n").trim()}\n`;
}

function writePackage(outDir) {
  const auditRaw = fs.readFileSync(auditPath);
  const auditSha = sha256(auditRaw);
  const audit = JSON.parse(auditRaw.toString("utf8"));
  const pages = enrichPages(audit);
  const snapshot = {
    schema_version: "1.0",
    lesson_version: "6.0-opening-slice",
    claim_boundary: "desktop_design_scaffold_only",
    source_audit_path: path.relative(root, auditPath).split(path.sep).join("/"),
    source_audit_sha256: auditSha,
    page_ids: pages.map((page) => page.page_id),
    total_minutes: pages.reduce((sum, page) => sum + page.minutes, 0),
    pages,
  };
  fs.mkdirSync(outDir, { recursive: true });
  const outputs = [
    ["02_氓_V6导入切片教学母版.md", renderLesson(pages, auditSha)],
    ["03A_氓_V6导入学习单A_旧故事与初听.md", renderWorksheetA()],
    ["03B_氓_V6导入学习单B_初听后路标卡.md", renderWorksheetB()],
    ["04A_氓_V6导入切片逐页无生试讲稿.md", renderScript(pages, auditSha)],
    ["06_氓_V6导入切片课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(outDir, name), content, "utf8");
  const manifest = {
    schema_version: "1.0",
    package_version: "6.0-opening-slice",
    claim_boundary: "desktop_design_scaffold_only",
    source_audit_sha256: auditSha,
    files: outputs.map(([name]) => ({ name, sha256: fileSha256(path.join(outDir, name)) })),
  };
  fs.writeFileSync(path.join(outDir, "opening_package_manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  return { pages: pages.length, minutes: snapshot.total_minutes, outDir };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const result = writePackage(args.out);
  process.stdout.write(`MARKDOWN_OK pages=${result.pages} minutes=${result.minutes} out=${result.outDir}\n`);
}

if (require.main === module) main();

module.exports = { enrichPages, renderLesson, renderWorksheetA, renderWorksheetB, renderScript, writePackage };
