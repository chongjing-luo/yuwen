#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const source = require("./meng_v62/content/chapter_4");
const { validate } = require("./verify_meng_v62_chapter4");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const OUT = assertV62OutputPath(path.join(stageDir(), "chapter_4", "package"));
const SOURCE_FILE = path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "chapter_4.js");
function sha256(value) { return crypto.createHash("sha256").update(value).digest("hex"); }
function fileSha(filePath) { return sha256(fs.readFileSync(filePath)); }
function marker(pageId) { return `<!-- V63_PAGE:${pageId} -->`; }

function renderLesson(data, sourceSha) {
  const lines = [
    "---", "document_type: teaching_master", "lesson: \"《氓》第四章\"", `version: "${data.version}"`,
    "claim_boundary: \"desktop_design_scaffold_only\"", `source_sha256: "${sourceSha}"`, "---", "",
    "# 《氓》V6.3第四章教学母版", "",
    "> 第四章以完整换声、桑叶旧解修订、多年与一刻、责任证据席、二三替换听辨、撤答回望六个事件推进。经历事实与行为责任严格分开。", "",
    `- 逻辑页：${data.pages.length}页`, `- 自然时长：${data.total_minutes}分钟`,
    "- 学生材料：C401完整读后才发04D；C402同时取回第三章旧桑叶卡；其余逐栏展开。", "",
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
document_type: chapter4_progressive_worksheet
lesson: "《氓》第四章"
version: "${data.version}"
distribution: "C401 after complete reading; reveal one section at a time"
---

# 第四章｜从桑叶落下，到责任被说清

> 开始时只露第一栏；C402须同时翻回第三章旧桑叶卡。

## C401｜完整读完以后

桑叶的新状态（原词）：________________

第一处像在作判断的原句：________________________________________

暂时没听出，可以留问号：________________

-------------------- 请先折到这里 --------------------

## C402｜让后文修改旧解释

${p.C402.original_text}

旧假设A：□保留　□改写　□撤回　新依据：________________________

旧假设B：□保留　□改写　□撤回　新依据：________________________

我现在的解释（保留可能语气）：____________________________________

## C403｜多年与一刻

${p.C403.original_text}

“三岁”让我听见：________________________________________________

“汤汤”让我看见：________________________________________________

双镜头旁白：____________________________________________________

同桌圈出的越界词：________________　我的修订：____________________

## C404｜责任证据席

${p.C404.original_text}

我的责任判断（12—20字）：________________________________________

原词证据：________________／________________

质询后我的修订：________________________________________________

## C405｜“二三”的语言力度

${p.C405.original_text}

原句比“他的行为多次改变”多出的感觉：____________________________

“二三”的现代短语：________________　我的改读：____________________

## C406｜第四章旁白与故事轨道

合书讲40秒：桑叶怎样变｜哪些是经历｜她怎样辨明责任

听者只报一个真正断点：__________________________________________

第四章一句自然话：________________________________________________

故事轨道第四格：__________________________________________________
`;
}

function renderScript(data, sourceSha) {
  const lines = ["---", "document_type: page_by_page_rehearsal_script", "lesson: \"《氓》第四章\"", `version: "${data.version}"`, "claim_boundary: \"scripted_not_observed\"", `source_sha256: "${sourceSha}"`, "---", "", "# 《氓》V6.3第四章逐页无生试讲稿", ""];
  for (const page of data.pages) {
    const script = page.script;
    lines.push(marker(page.page_id), `## ${page.page_id}｜${page.title}｜${page.minutes}分钟`, "", "【本页不可替代的意义】", "", page.unique_function, "", "【删除本页会失去什么】", "", page.deletion_loss, "", "【场面】", "", script.scene, "", "【教师实际说】", "", `“${script.teacher_spoken}”`, "", "【动作、等待与走位】", "");
    for (const item of script.timeboxes) lines.push(`- ${item.label}：${item.seconds}秒`);
    for (const item of script.stage_directions) lines.push(`- （${item}）`);
    lines.push("", "【现场分支】", "");
    for (const branch of script.branches) lines.push(`- ${branch.kind}：${branch.response}`);
    lines.push("", "【听者同时做什么】", "", script.listener_task, "", "【证据留在哪里】", "", script.evidence_location, "", "【回到人物和故事】", "", page.story_return, "", "【后续怎样真实调用】", "", page.next_use, "", "【怎样自然切页】", "", `“${script.cut_line}”`, "");
  }
  return `${lines.join("\n").trim()}\n`;
}

function main() {
  const verification = validate(source);
  if (!verification.ok) throw new Error(`chapter4 contract failed: ${JSON.stringify(verification.errors)}`);
  const sourceSha = fileSha(SOURCE_FILE);
  fs.mkdirSync(OUT, { recursive: true });
  const snapshot = { ...source, source_sha256: sourceSha, claim_boundary: "desktop_design_scaffold_only" };
  const outputs = [
    ["02_氓_V63第四章教学母版.md", renderLesson(source, sourceSha)],
    ["04D_氓_V63第四章渐进学习单_C401读后发.md", renderWorksheet(source)],
    ["04A_氓_V63第四章逐页无生试讲稿.md", renderScript(source, sourceSha)],
    ["06_氓_V63第四章课程数据快照.json", `${JSON.stringify(snapshot, null, 2)}\n`],
  ];
  for (const [name, content] of outputs) fs.writeFileSync(path.join(OUT, name), content, "utf8");
  const manifest = { schema_version: "1.1", module_id: source.module_id, version: source.version, source_sha256: sourceSha, files: outputs.map(([name]) => ({ name, sha256: fileSha(path.join(OUT, name)) })) };
  fs.writeFileSync(path.join(OUT, "chapter4_package_manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`V63_CHAPTER4_MARKDOWN_OK pages=${source.pages.length} minutes=${source.total_minutes} out=${OUT}\n`);
}

if (require.main === module) main();
module.exports = { renderLesson, renderWorksheet, renderScript };
