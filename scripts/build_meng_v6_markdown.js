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
    if (Array.isArray(note.physical_occurrences)) {
      compiled.physical_occurrences = note.physical_occurrences.map((occurrence) => ({
        occurrence_id: occurrence.occurrence_id,
        state: occurrence.state,
        seconds: occurrence.seconds,
        student_visible_prompt: occurrence.student_visible_prompt,
        scene: occurrence.scene,
        teacher_spoken: occurrence.teacher_spoken,
        stage_directions: occurrence.directions,
        timeboxes: occurrence.timeboxes.map(([label, seconds]) => ({ label, seconds })),
        branches: occurrence.branches.map(([kind, response]) => ({ kind, response })),
        listener_task: occurrence.listener,
        evidence_location: occurrence.evidence_location,
        cut_line: occurrence.cut,
      }));
      const physicalSeconds = compiled.physical_occurrences.reduce((total, occurrence) => total + occurrence.seconds, 0);
      if (physicalSeconds !== source.minutes * 60) throw new Error(`${source.page_id} physical occurrence seconds=${physicalSeconds}`);
    }
    const sum = timeboxes.reduce((total, item) => total + item.seconds, 0);
    if (sum !== source.minutes * 60) throw new Error(`${source.page_id} timeboxes=${sum} expected=${source.minutes * 60}`);
    return compiled;
  });
}

function renderLesson(pages, auditSha) {
  const lines = [
    "---", "document_type: teaching_master", "lesson: \"《氓》\"", "version: \"6.2-cross-channel-page-proof\"",
    "claim_boundary: \"desktop_design_scaffold_only\"", `audit_sha256: \"${auditSha}\"`, "---", "",
    "# 《氓》V6导入切片教学母版", "",
    "> 本稿只覆盖导入、第一次完整听读与最小支架。它记录桌面设计条件，不声称真实学生已经参与、理解或学会。", "",
    "## 导入切片的课堂走向", "",
    "先让每个人从自己的语文记忆里尽量多找故事，再让四个人的记忆相遇，接着每组贡献两张真实卡片。全体学生先连接、命名，至少三人公开举证并接受全班修订；教师只复述现场已经出现的线索，不预制婚姻答案。直到本班主题谱形成，才揭示《氓》。随后以三个朴素问题进入完整听读，保存个人停顿，最后补足继续逐句阅读所需的最小《诗经》身份与四言节奏。", "",
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
distribution_timing: "before_title_reveal"
---

# 爱情与婚姻文学回忆单

> 只谈作品或第三人称故事，不必公开私人经历。想不起、没有新增或暂时不同意，都可以如实留下。

## 一、我读过的爱情或婚姻故事

尽量多写，至少一篇。每篇只写：篇名＋它写了什么。

1. 篇名：________________　它写了什么：________________________________

2. 篇名：________________　它写了什么：________________________________

3. 篇名：________________　它写了什么：________________________________

4. 篇名：________________　它写了什么：________________________________

5. 篇名：________________　它写了什么：________________________________

更多：__________________________________________________________________

一时想不起：□翻教材目录　□领取一张只写篇名的提示条　□先听后补

## 二、四个人的小组作品谱

| 谁说的 | 篇名 | 它写了什么 |
|---|---|---|
| 1 |  |  |
| 2 |  |  |
| 3 |  |  |
| 4 |  |  |

听见同伴说到新内容就勾；四轮后，每人圈出最想带进全班的两项。

□作品／主题：__________________________________________________________

□暂无新增；我从上方小组作品谱圈出两项值得全班听见的。

□作品／主题：__________________________________________________________

□作品／主题：__________________________________________________________

□作品／主题：__________________________________________________________

两张贡献卡都要保留来源：

卡A｜组号______－卡号______－原提议者号______　□原提议者亲写　□原提议者签认

卡B｜组号______－卡号______－原提议者号______　□原提议者亲写　□原提议者签认

尽量由两位不同同学贡献；若确实同源，如实写同一个号码。

## 三、我们的作品卡墙

我未想到的一项：________________________________________________________

看完约十六张卡，我未想到的一项：________________________________________

我先连接：卡号______与卡号______；临时命名：____________________________

公开核对后，选择“保留／改名／移回”：□保留　□改名为________________　□移回

理由（引用卡片上的字）：________________________________________________

`;
}

function renderWorksheetB() {
  return `---
document_type: student_reading_card
lesson: "《氓》"
version: "6.2-opening-reading-card"
distribution_timing: "at_title_reveal"
---

# 《氓》阅读卡｜三问与第一次听读

> 先完整听她把六章说完。只谈诗句或第三人称故事，不必公开私人经历。

## 一、读完六章，再回答

一、她经历了什么？

二、她婚后的不幸，在生活中是什么样子？

三、这场婚姻为什么走到这一步？

我最想追踪的一问：□一　□二　□三

## 二、第一次完整听读

哪一句把你留了下来？

“______________________________________________________________________”

□我听见　□我看见　□我想问：________________________________________

如果暂时没有：□尚未找到；听同桌后，我 □补一句　□仍保留

同桌让我补记的一个不同之处：__________________________________________
`;
}

function renderWorksheetC() {
  return `---
document_type: student_worksheet_card
lesson: "《氓》"
version: "6.2-opening-context-card"
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

先看斜线跟读；听到教师说“看教材”，再转看教材第一章开头没有斜线的原句。

听者若听见机械停顿，就问“谁做什么”；读者带着完整动作再读。

□需要调整：我标出的停连处是____________________________________________

□原本读顺：我圈出的连续动作是__________________________________________
`;
}

function renderMaterials() {
  return `---
document_type: teacher_material_pack
lesson: "《氓》"
version: "6.2-opening-materials"
---

# 《氓》导入物料包｜课前逐项备齐

## 一、本班已学篇目目录索引

- 按本班真实教材与教学进度打印一页“本班已学篇目目录索引”；只列篇名，不写主题和答案。
- 初中、高中、整本书各留一栏；删去本班未学篇目，避免虚假回忆。

## 二、只写篇名的提示条

- 将索引中的篇名分别裁成窄条，正面只写篇名，背面保持空白。
- 课前扣放讲台；个人静想60秒后才按需领取，不在PPT上提前展示。

## 三、现场共创材料

- 每组两张空白贡献卡，大小须能让后排看清“篇名＋它写了什么”；卡面预留“组号－卡号－原提议者号－原提议者签认”。
- 原提议者亲手写卡或在卡上签认；优先保留两位不同提议者的内容，若两张确实同源则如实标同一号码。
- 备磁贴或可移胶、粗头笔、计时器与一块完全空白的卡墙区域。
- 课前不得预贴作品、主题词或分类框。

## 四、保存与跨课时调用

- 若教室允许保留：下课后原位保留卡墙，并标注班级与日期。
- 若不能保留：教师在N005末尾正面拍照备份，核对文字可辨；下节课将归档照片投影或打印，供三问回收与婚姻圆桌真实调用。
`;
}

function renderScript(pages, auditSha) {
  const lines = [
    "---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》\"", "version: \"6.2-cross-channel-page-proof\"",
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
    if (Array.isArray(page.physical_occurrences)) {
      lines.push("【本页的物理屏幕状态】", "");
      for (const occurrence of page.physical_occurrences) {
        lines.push(`### ${occurrence.occurrence_id}｜${occurrence.state}｜${occurrence.seconds}秒`, "", "【承接与场面】", occurrence.scene, "", "【教师实际说】", `“${occurrence.teacher_spoken}”`, "", "【动作、等待与走位】");
        for (const item of occurrence.timeboxes) lines.push(`- ${item.label}：${item.seconds}秒`);
        for (const item of occurrence.stage_directions) lines.push(`- （${item}）`);
        lines.push("", "【现场分支】");
        for (const branch of occurrence.branches) lines.push(`- ${branch.kind}：${branch.response}`);
        lines.push("", "【听者同时做什么】", occurrence.listener_task, "", "【留下什么】", `${occurrence.evidence_location}。`, "", "【怎样接下去】", `“${occurrence.cut_line}”`, "");
      }
    }
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
    lesson_version: "6.2-cross-channel-page-proof",
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
    ["03A_爱情与婚姻文学回忆单.md", renderWorksheetA()],
    ["03B_氓_V6导入阅读卡.md", renderWorksheetB()],
    ["03C_氓_V6初听后路标卡.md", renderWorksheetC()],
    ["03D_氓_V6导入物料包.md", renderMaterials()],
    ["04A_氓_V6导入切片逐页无生试讲稿.md", renderScript(pages, auditSha)],
    ["06_氓_V6导入切片课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  const legacyNames = [
    "03A_氓_V6导入学习单A_旧故事与初听.md",
    "03B_氓_V6导入学习单B_初听后路标卡.md",
  ];
  for (const name of legacyNames) {
    const target = path.join(outDir, name);
    if (fs.existsSync(target)) fs.rmSync(target);
  }
  for (const [name, content] of outputs) fs.writeFileSync(path.join(outDir, name), content, "utf8");
  const manifest = {
    schema_version: "1.0",
    package_version: "6.2-cross-channel-page-proof",
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

module.exports = { enrichPages, renderLesson, renderWorksheetA, renderWorksheetB, renderWorksheetC, renderMaterials, renderScript, writePackage };
