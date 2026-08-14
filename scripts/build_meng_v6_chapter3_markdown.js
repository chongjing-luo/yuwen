#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const chapter = require("./meng_v6/content/chapter_3.js");
const notes = require("./meng_v6/chapter3_notes.js");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "chapter_3", "package");

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
    "---", "document_type: teaching_master", "lesson: \"《氓》第三章\"", `version: \"${chapter.version}\"`,
    "claim_boundary: \"desktop_design_scaffold_only\"", `source_sha256: \"${sourceSha}\"`, "---", "",
    "# 《氓》V6第三章教学母版", "",
    "> 本章沿‘故事轨道—完整听读—逐句生成—删句体验—撤答复位—整章旁白—知识收纳’推进。比兴后置命名；桑叶解释保持开放；处境不等不偷换为女子责任。", "",
    `- 页面：${pages.length}页`, `- 自然时长：${pages.reduce((sum, page) => sum + page.minutes, 0)}分钟`,
    "- 当前不放人物或物象插图；页面功能冻结后，再判断桑叶物象是否需要统一视觉资产。", "",
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
      `- 删除损失：${page.deletion_loss}`,
      `- 后页接续：${page.next_event_id}`, "",
    );
  }
  return `${lines.join("\n").trim()}\n`;
}

function renderWorksheet() {
  return `---
document_type: student_worksheet
lesson: "《氓》第三章"
version: "${chapter.version}"
---

# 《氓》第三章学习单｜让五句诗连成一段话

> 开始时请沿折线把后文折到背面，只露出第一栏；听到“展开一栏”再打开下一部分，不提前翻看。

## 一、故事走到这里

初见议婚：__________________________________________________________

等待迁嫁：__________________________________________________________

第三章先留空：______________________________________________________

完整读第三章；感觉说话方式有变化时，自己轻停。读后只写三处落点：

最先看见 __________________　先劝 __________________　后来劝 __________________

-------------------- 请先折到这里 --------------------

## 二、桑叶假设卡

桑之未落，其叶沃若。

自然话：____________________________________________________________

“沃若”让我看见的颜色、质地、生命状态：________________／________________

可能联想A：________________________　感官依据：________________________

可能联想B：________________________　感官依据：________________________

暂不裁决；第四章“黄而陨”出现后再筛选。

## 三、两声“于嗟”

于嗟鸠兮，无食桑葚！　于嗟女兮，无与士耽！

第一句自然话：______________________________________________________

第二句自然话：______________________________________________________

反复的声音：________________

改变的对象：________________ → ________________

改变的劝告：________________ → ________________

两声劝告怎样接过去：________________________________________________

## 四、同是“耽”，为何一边可说，一边不可说

士之耽兮，犹可说也。　女之耽兮，不可说也！

两句完全相同的词：__________________________________________________

真正改变判断的词：__________________________________________________

诗中明写的处境差异：________________________________________________

原因：□本章已写　□后文待证

同桌圈出的越界词：________________　我的换笔修订：____________________

## 五、删句听读

两种写法在画面、声音或情感铺垫上有什么不同？

□画面　□声音　□情感铺垫　□删改句更直接

我的具体解释：______________________________________________________

原词依据：__________________________________________________________

体验后再命名：______________________________________________________

## 六、把章首三处落点接成四级声音阶梯

写回章首三处落点：________________ → ________________ → ________________

乱序短签：劝女子勿耽　桑叶沃若　比较脱身处境　劝斑鸠勿食

我的编号与原词：____________________________________________________

同桌指出的断层：________________　翻诗后换笔修订：____________________

合上书，替这一章补一句故事旁白：

____________________________________________________________________

## 七、第三章三十秒旁白与故事轨道

迁嫁之后，眼前先出现什么？__________________________________________

两声劝告先后落在谁身上？____________________________________________

最后两句写出谁更难脱身？____________________________________________

听者提醒我补回：____________________________________________________

故事轨道第三格：初见议婚 → 等待迁嫁 → ______________________________

## 八、知识收纳星标

只给仍不稳的一项加★，不整页抄写。

□字词读音与意思　□两声劝告怎样相接　□这种写法的名称与作用　□两句脱身处境

我的★：________________　回到原句补证：______________________________
`;
}

function renderScript(pages, sourceSha) {
  const lines = [
    "---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》第三章\"", `version: \"${chapter.version}\"`,
    "claim_boundary: \"scripted_not_observed\"", `source_sha256: \"${sourceSha}\"`, "---", "",
    "# 《氓》V6第三章逐页无生试讲稿", "",
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
    schema_version: "1.0", lesson_version: chapter.version, source_sha256: sourceSha,
    page_ids: pages.map((page) => page.page_id),
    total_minutes: pages.reduce((sum, page) => sum + page.minutes, 0), pages,
  };
  const outputs = [
    ["02_氓_V6第三章教学母版.md", renderLesson(pages, sourceSha)],
    ["03_氓_V6第三章学习单.md", renderWorksheet()],
    ["04A_氓_V6第三章逐页无生试讲稿.md", renderScript(pages, sourceSha)],
    ["06_氓_V6第三章课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(OUT, name), content, "utf8");
  const manifest = { schema_version: "1.0", source_sha256: sourceSha, files: outputs.map(([name]) => ({ name, sha256: fileSha(path.join(OUT, name)) })) };
  fs.writeFileSync(path.join(OUT, "chapter3_package_manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`CHAPTER3_MARKDOWN_OK pages=${pages.length} minutes=${snapshot.total_minutes}\n`);
}

if (require.main === module) main();

module.exports = { compilePages, renderLesson, renderWorksheet, renderScript };
