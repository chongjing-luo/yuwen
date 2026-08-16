#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const lesson = require("./meng_v66/lesson");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v62_stage", "v66", "package");
const MASTER = path.join(OUT, "02_氓_V66教学母版_V5.md");
const SCRIPT = path.join(OUT, "04A_氓_V66逐页真实剧本_V5.md");
const LEDGER = path.join(OUT, "05_氓_V66逐页功能总账_V5.md");

function scriptMarkdown() {
  const lines = ["---", "document_type: physical_slide_by_physical_slide_real_classroom_script", `version: ${lesson.version}`, "status: no_image_implementation_candidate", `physical_slides: ${lesson.target_pages}`, "claim_boundary: 桌面真实剧本；不声称真实课堂已经发生或学生已经学会", "---", "", `# 《氓》V6.6 V5｜${lesson.target_pages}张物理画面真实课堂剧本`, "", "每张物理画面只写该画面出现期间真正会说、会等、会看、会修的内容。多状态逻辑节点不得在每张备注中重复整段流程。", ""];
  let physical = 0;
  for (const page of lesson.pages) {
    for (const state of page.states) {
      physical += 1;
      const s = state.script;
      lines.push(`## ${String(physical).padStart(2, "0")}｜${page.page_id}-${state.state_id}｜${page.title}（${state.seconds}秒）`, "", `**这张画面的唯一意义：** ${state.state_function}`, "", `**所属逻辑节点：** ${String(page.page_number).padStart(2, "0")}｜${page.unique_function}`, "", `**学生此刻看见：** ${state.frontstage.join("｜")}`, "", `**学生实际动作与证据：** ${page.student_action.join("；")}；${s.evidence_location}`, "", `**场景：** ${s.scene}`, "", "**教师可直接演出的逐字稿：**", "", s.teacher_spoken, "", "**舞台动作：**", "");
      for (const item of s.stage_directions) lines.push(`- ${item}`, "");
      lines.push(`**本画面时间盒：** ${s.timeboxes.map((item) => `${item.label}${item.seconds}秒`).join("；")}`, "", "**现场分支：**", "");
      for (const branch of s.branches) lines.push(`- ${branch.kind}：${branch.response}`, "");
      lines.push(`**听者任务：** ${s.listener_task}`, "", `**切页触发：** ${s.cut_line}`, "", `**删除损失与相邻反证：** ${page.deletion_loss}；${page.adjacent_counterproof}`, "");
    }
  }
  return `${lines.join("\n").trimEnd()}\n`;
}

function masterMarkdown() {
  const lines = ["---", "document_type: teaching_master", `version: ${lesson.version}`, "status: no_image_implementation_candidate", `logical_pages: ${lesson.target_logical_pages}`, `physical_states: ${lesson.target_pages}`, `natural_minutes: ${lesson.target_natural_minutes}`, "---", "", "# 《氓》V6.6 V5教学母版", "", "## 教学目标（全课指导）", ""];
  for (const obj of lesson.objectives) {
    const kp = obj.kp_refs.length ? obj.kp_refs.map((k) => k.replace("KP-CARD-X3-U01-01-", "KP-")).join("、") : "无KP绑定（体验/迁移目标）";
    lines.push(`${obj.id}（${obj.dimension}）：${obj.statement}`, "", `　　归因：${obj.nodes.join("／")}；绑定：${kp}；证据页：${obj.evidence_pages.join("、")}`, "");
  }
  lines.push(`过程品质（享受·不单列目标）：${lesson.process_quality.statement}`, "", `　　归因：${lesson.process_quality.nodes.join("／")}`, "");
  lines.push("## 课程脊柱", "", "广泛回忆爱情与婚姻文学—教师引用现场作品后揭题—建立《诗经》最低文化坐标—完整听诗—沿六章逐句读懂并逐章形成个人章意—个人六章长卷—把不幸还原为生活并完成个人末答—质询婚姻悲剧的原因并完成个人末答—从原诗提出良好共同生活的支点—文化、字词、诗法检索修复—完整终读。", "", "## 三个全文问题", "", ...lesson.three_questions.map((value, index) => `${index + 1}. ${value}`), "", "## 逐页结构", "", "| 逻辑页 | ID | 分钟 | 物理状态 | 唯一意义 | 学生动作 | 产物 | 首次后用 |", "|---:|---|---:|---:|---|---|---|---|");
  for (const page of lesson.pages) lines.push(`| ${String(page.page_number).padStart(2, "0")} | ${page.page_id} | ${page.minutes} | ${page.states.length} | ${page.unique_function} | ${page.student_action.join("；")} | ${page.artifact} | ${page.next_use} |`);
  lines.push("", "## 结构说明", "", `本母版有${lesson.target_logical_pages}个教学节点、${lesson.target_pages}个可审查物理画面状态、${lesson.target_natural_minutes}分钟自然课堂内容。物理状态用于把首答、学生作品生成和教师校准分开审查，不等于增加同等数量的教学环节。页数服从理解，不作为质量目标。`, "", "## 知识收纳", "", "- 《诗经》：我国第一部诗歌总集，现存305篇，作品大致产生于西周初年至春秋中叶；风、雅、颂；《氓》出自《卫风》。", "- 六章最低字词门槛：愆、筮、说、爽、咥、泮；其他字词沿原句讲解并以两词加深。", "- 写法：以赋的铺陈直叙沿六章推进女子一生；桑叶的比兴与前后对照；词句复现、回环与反折；四言节奏、叠词与声音。", "- 伦理边界：不把女子投入、等待、劳作或旧日欢乐写成男子失信粗暴的原因；不把婚前警讯倒推为已证预谋；不把末句续写成诗中已经发生的出走。", "- 婚姻理解由学生返诗讨论后形成：审慎了解，承诺由长期行动核验，言行一致，尊重边界，劳动和决定不长期失衡，有理解支持和求助通道，发现持续伤害时能够止损。", "");
  return `${lines.join("\n").trimEnd()}\n`;
}

function ledgerMarkdown() {
  const lines = ["---", "document_type: page_function_release_ledger", `version: ${lesson.version}`, "status: pre_review_candidate", "claim_boundary: 设计与构建候选；独立双审前不放行", "---", "", "# 《氓》V6.6 V5逐页功能总账", "", `## 一、${lesson.target_logical_pages}个逻辑教学节点合同`, "", "| 页/ID | 前页输入 | 唯一困难与功能 | 信息状态 | 参与与产物 | 后用 | 主视觉/插图 | 接收、删并反证与失败信号 |", "|---|---|---|---|---|---|---|---|"];
  for (const p of lesson.pages) lines.push(`| ${String(p.page_number).padStart(2, "0")}/${p.page_id} | ${p.prior_input} | ${p.unique_difficulty}；${p.unique_function} | ${p.info_state} | ${p.participation_path}；${p.artifact} | ${p.next_use} | ${p.visual_duty}；${p.illustration_eligibility} | ${p.first_person_reception}；删除：${p.deletion_loss}；相邻：${p.adjacent_counterproof}；失败：${p.failure_signals.join("、")} |`);
  lines.push("", `## 二、${lesson.target_pages}张物理页面逐张验收账`, "", "物理页不是逻辑节点的重复编号。每个状态必须说明此刻为何单独出现；首答、现场学生作品、教师校准、撤答复述和本人末答必须能分别渲染与审查。", "", "| 物理页 | 逻辑ID-状态 | 秒 | 此刻唯一意义 | 学生此刻看见什么 | 学生实际动作与可见产物 | 信息边界 | 后用与删除损失 | 主视觉与插图资格 | 失败即返工 |", "|---:|---|---:|---|---|---|---|---|---|---|");
  let physical = 0;
  for (const p of lesson.pages) {
    for (const state of p.states) {
      physical += 1;
      lines.push(`| ${physical} | ${p.page_id}-${state.state_id} | ${state.seconds} | ${state.state_function} | ${state.frontstage.join("；")} | ${p.student_action.join("；")}；${p.artifact} | ${p.info_state} | ${p.next_use}；删除：${p.deletion_loss} | ${p.visual_duty}；${p.illustration_eligibility} | ${p.failure_signals.join("、")} |`);
    }
  }
  lines.push("", "## 三、放行状态", "", "当前为无插图构建候选。必须完成全量渲染、至少一次修复—复验，并由独立视觉与学生接收审查在同一组SHA上清零P0/P1/P2，才可进入受控试教；插图A/B必须在其后重新预注册。", "");
  return `${lines.join("\n").trimEnd()}\n`;
}

function build() {
  fs.mkdirSync(OUT, { recursive: true }); fs.writeFileSync(MASTER, masterMarkdown(), "utf8"); fs.writeFileSync(SCRIPT, scriptMarkdown(), "utf8"); fs.writeFileSync(LEDGER, ledgerMarkdown(), "utf8");
  process.stdout.write(`MENG_V66_MARKDOWN_OK logical=${lesson.target_logical_pages} physical=${lesson.target_pages} outputs=3\n`);
}

if (require.main === module) build();
module.exports = { build, MASTER, SCRIPT, LEDGER, masterMarkdown, scriptMarkdown, ledgerMarkdown };
