#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const source = require("./meng_v62/content/chapter_3");
const { validate } = require("./verify_meng_v62_chapter3");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const OUT = assertV62OutputPath(path.join(stageDir(), "chapter_3", "package"));
const SOURCE_FILE = path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "chapter_3.js");
function sha256(value) { return crypto.createHash("sha256").update(value).digest("hex"); }
function fileSha(filePath) { return sha256(fs.readFileSync(filePath)); }
function marker(pageId) { return `<!-- V63_PAGE:${pageId} -->`; }

function renderLesson(data, sourceSha) {
  const lines = [
    "---", "document_type: teaching_master", "lesson: \"《氓》第三章\"", `version: \"${data.version}\"`,
    "claim_boundary: \"desktop_design_scaffold_only\"", `source_sha256: \"${sourceSha}\"`, "---", "",
    "# 《氓》V6.3第三章教学母版", "",
    "> 第三章以完整换声、桑叶假设、呼告与蒙句听辨、脱身处境和撤答回望五个事件推进。知识不在章末重复结账，而在全文末统一检索。", "",
    `- 逻辑页：${data.pages.length}页`, `- 自然时长：${data.total_minutes}分钟`,
    "- 学生材料：C301完整读后才发03C；首次只露C301，其余按栏展开。", "",
  ];
  for (const page of data.pages) {
    lines.push(marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "",
      "### 为什么必须有这一页", "", `- 文学对象：${page.literary_object}`, `- 当前困难：${page.current_difficulty}`,
      `- 唯一功能：${page.unique_function}`, `- 删除损失：${page.deletion_loss}`, `- 相邻合并测试：${page.merge_test}`, "",
      "### 学生此刻看见", "", "```text", page.visible, "```", "", `第一眼：${page.first_glance}`, "",
      "### 信息边界", "", `- 已知：${page.information_state.known}`, `- 本页揭示：${page.information_state.reveal_now}`, `- 继续后置：${page.information_state.defer}`, "",
      "### 学生怎样生成", "");
    for (const action of page.student_action) lines.push(`- ${action}`);
    lines.push("", `- 留下的作品：${page.artifact}`, `- 正常路径：${page.normal_path}`, `- 有界反馈：${page.bounded_feedback}`, `- 修订：${page.revision}`, "",
      "### 教师怎样后置校准", "", page.teacher_synthesis, "", `- 回到人物和故事：${page.story_return}`, `- 后续真实调用：${page.next_use}`,
      `- 视觉职责：${page.visual_duty}`, `- 学生第一人称接收：${page.first_person_reception}`, "");
  }
  return `${lines.join("\n").trim()}\n`;
}

function renderWorksheet(data) {
  const p = Object.fromEntries(data.pages.map((item) => [item.page_id, item]));
  return `---
document_type: chapter3_progressive_worksheet
lesson: "《氓》第三章"
version: "${data.version}"
distribution: "C301 after complete reading; reveal one section at a time"
---

# 第三章｜从桑叶到一声劝告

> 开始时只露第一栏；听到“展开一栏”再打开下一部分。

## C301｜完整读完以后

眼前先出现：________________　原词：________________

哪一句开始像在劝告：____________________________________________

暂时没听出，可以留问号：________________

-------------------- 请先折到这里 --------------------

## C302｜桑叶假设

${p.C302.original_text}

自然话：__________________________________________________________

色泽、质地、生命感：________________／________________

可能联想A：________________　依据：________________

可能联想B：________________　依据：________________

第四章再筛选：□保留　□改写　□撤回

## C303｜两声“于嗟”

${p.C303.original_text}

第一句自然话：____________________________________________________

第二句自然话：____________________________________________________

没有改变的声音：________________

改变的对象：________________ → ________________

改变的劝告：________________ → ________________

两声怎样接过去：__________________________________________________

用手蒙住桑叶、斑鸠两句，只听最后一句：

少了或增强了：________________　原词依据：________________________

同桌追问后：□能找到，无需改　□我改成：__________________________

体验以后才命名：__________________________________________________

## C305｜同是“耽”

${p.C305.original_text}

相同的词：________________　改变结果的词：________________

诗中明写的脱身差异：________________________________________________

原因：后文待证。　同桌圈出的越界词：________________

我的修订：________________________________________________________

## C306｜第三章旁白与故事轨道

合书讲30秒：眼前先出现什么｜劝告怎样从物到人｜最后看见怎样的脱身处境

听者只补一处真正遗漏：______________________________________________

第三章一句自然话：__________________________________________________

故事轨道第三格：____________________________________________________
`;
}

function renderScript(data, sourceSha) {
  const lines = ["---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》第三章\"", `version: \"${data.version}\"`, "claim_boundary: \"scripted_not_observed\"", `source_sha256: \"${sourceSha}\"`, "---", "", "# 《氓》V6.3第三章逐页无生试讲稿", ""];
  for (const page of data.pages) {
    const s = page.script;
    lines.push(marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "", "【本页不可替代的意义】", "", page.unique_function, "", "【删除本页会失去什么】", "", page.deletion_loss, "", "【场面】", "", s.scene, "", "【教师实际说】", "", `“${s.teacher_spoken}”`, "", "【动作、等待与走位】", "");
    for (const item of s.timeboxes) lines.push(`- ${item.label}：${item.seconds}秒`);
    for (const item of s.stage_directions) lines.push(`- （${item}）`);
    lines.push("", "【现场分支】", "");
    for (const branch of s.branches) lines.push(`- ${branch.kind}：${branch.response}`);
    lines.push("", "【听者同时做什么】", "", s.listener_task, "", "【证据留在哪里】", "", s.evidence_location, "", "【回到人物和故事】", "", page.story_return, "", "【后续怎样真实调用】", "", page.next_use, "", "【怎样自然切页】", "", `“${s.cut_line}”`, "");
  }
  return `${lines.join("\n").trim()}\n`;
}

function main() {
  const verification = validate(source);
  if (!verification.ok) throw new Error(`chapter3 contract failed: ${JSON.stringify(verification.errors)}`);
  const sourceSha = fileSha(SOURCE_FILE);
  fs.mkdirSync(OUT, { recursive: true });
  const snapshot = { ...source, source_sha256: sourceSha, claim_boundary: "desktop_design_scaffold_only" };
  const outputs = [
    ["02_氓_V63第三章教学母版.md", renderLesson(source, sourceSha)],
    ["03C_氓_V63第三章渐进学习单_C301读后发.md", renderWorksheet(source)],
    ["04A_氓_V63第三章逐页无生试讲稿.md", renderScript(source, sourceSha)],
    ["06_氓_V63第三章课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(OUT, name), content, "utf8");
  const manifest = { schema_version: "1.1", module_id: source.module_id, version: source.version, source_sha256: sourceSha, files: outputs.map(([name]) => ({ name, sha256: fileSha(path.join(OUT, name)) })) };
  fs.writeFileSync(path.join(OUT, "chapter3_package_manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`V63_CHAPTER3_MARKDOWN_OK pages=${source.pages.length} minutes=${source.total_minutes} out=${OUT}\n`);
}

if (require.main === module) main();
module.exports = { renderLesson, renderWorksheet, renderScript };
