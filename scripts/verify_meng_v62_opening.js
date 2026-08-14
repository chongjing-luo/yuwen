#!/usr/bin/env node
"use strict";

const payload = require("./meng_v62/content/opening");
const { contract: textContract } = require("./meng_v6/text");
const { validate: validateTextContract } = require("./meng_v6/verify_text");

const EXPECTED_IDS = ["O01", "O02", "O03", "O04", "O05", "O06", "O07", "O08", "O09"];
const EXPECTED_QUESTIONS = [
  "她经历了什么？",
  "她婚后的不幸，在生活中是什么样子？",
  "这场婚姻为什么走到这一步？",
];
const VISIBLE_BANNED = [
  /学生画像/u, /教学目标/u, /设计意图/u, /理解链/u, /学习任务群/u,
  /不填表/u, /不概括/u, /不齐读/u, /不回答/u, /原提议者/u,
  /签认/u, /查重/u, /回执/u, /星标/u, /卡号/u, /组号/u,
];
const GLOBAL_RETIRED_PROCEDURE = [/原提议者号/u, /签认/u, /查重/u, /回执/u, /卡墙/u, /贡献卡/u];
const PREMATURE_REVEALS = [/背叛/u, /失信/u, /粗暴/u, /压榨/u, /恋爱脑/u, /沉没成本/u, /离开/u];

function compactPoem(text) {
  return String(text).replace(/[，。！？；：、\s｜《》“”‘’]/gu, "");
}

function validate(data = payload) {
  const errors = [];
  const warn = [];
  const fail = (code, pageId = "MODULE", detail = "") => errors.push({ code, page_id: pageId, detail });

  if (data.module_id !== "MENG_V62_OPENING" || data.module !== "opening") fail("IDENTITY_MISMATCH");
  if (data.status !== "implementation_candidate") fail("STATUS_NOT_CANDIDATE");
  if (JSON.stringify(data.three_questions) !== JSON.stringify(EXPECTED_QUESTIONS)) fail("THREE_QUESTIONS_DRIFT");
  const pages = Array.isArray(data.pages) ? data.pages : [];
  if (JSON.stringify(pages.map((item) => item.page_id)) !== JSON.stringify(EXPECTED_IDS)) fail("PAGE_SEQUENCE_MISMATCH");
  if (data.total_minutes !== 31 || pages.reduce((sum, item) => sum + item.minutes, 0) !== 31) fail("TOTAL_TIME_MISMATCH");

  const textErrors = validateTextContract(textContract);
  if (textErrors.length) fail("FROZEN_TEXT_CONTRACT_INVALID", "MODULE", textErrors.join(","));
  const expectedPoem = compactPoem(textContract.lines.map((item) => item.text).join(""));
  const actualPoem = compactPoem((data.chapters || []).flatMap((item) => item.lines || []).join(""));
  if (actualPoem !== expectedPoem) fail("POEM_TEXT_MISMATCH");

  for (const page of pages) {
    const id = page.page_id || "UNKNOWN";
    const required = [
      "title", "literary_object", "current_difficulty", "unique_function", "visible", "first_glance",
      "student_action", "artifact", "normal_path", "bounded_feedback", "revision", "teacher_synthesis",
      "story_return", "next_use", "deletion_loss", "visual_duty", "script",
    ];
    for (const key of required) {
      const value = page[key];
      if (value === undefined || value === null || (typeof value === "string" && !value.length) || (Array.isArray(value) && !value.length)) {
        fail("REQUIRED_FIELD_EMPTY", id, key);
      }
    }
    if (!Number.isFinite(page.minutes) || page.minutes <= 0) fail("INVALID_MINUTES", id);
    if (!Array.isArray(page.student_action) || page.student_action.length < 1 || page.student_action.length > 3) fail("ACTION_BUDGET_EXCEEDED", id);
    const timeboxes = page.script?.timeboxes || [];
    const seconds = timeboxes.reduce((sum, item) => sum + Number(item.seconds || 0), 0);
    if (seconds !== page.minutes * 60) fail("TIMEBOX_MISMATCH", id, `${seconds}/${page.minutes * 60}`);
    if (!Array.isArray(page.script?.branches) || page.script.branches.length < 1) fail("NO_REAL_CLASSROOM_BRANCH", id);
    for (const pattern of VISIBLE_BANNED) if (pattern.test(page.visible)) fail("STUDENT_VISIBLE_META_OR_CONTROL", id, String(pattern));
    const serialized = JSON.stringify(page);
    for (const pattern of GLOBAL_RETIRED_PROCEDURE) if (pattern.test(serialized)) fail("RETIRED_PROCEDURE_REAPPEARS", id, String(pattern));
    if (["O01", "O02", "O03", "O04", "O05", "O06", "O07"].includes(id)) {
      for (const pattern of PREMATURE_REVEALS) if (pattern.test(page.visible)) fail("PREMATURE_STORY_REVEAL", id, String(pattern));
    }
    if (page.story_return.length < 18) fail("STORY_RETURN_TOO_THIN", id);
    if (page.deletion_loss.length < 18) fail("DELETION_LOSS_UNPROVEN", id);
    if (!page.script?.teacher_spoken || page.script.teacher_spoken.length < 80) fail("SCRIPT_NOT_REHEARSABLE", id);
    if (!page.script?.scene || !Array.isArray(page.script?.stage_directions) || page.script.stage_directions.length < 2) fail("STAGING_TOO_THIN", id);
  }

  const byId = Object.fromEntries(pages.map((item) => [item.page_id, item]));
  if (!byId.O02?.unique_function.includes("每个人先在并行") || !byId.O02?.student_action.join("").includes("每人讲一篇")) fail("BREADTH_NOT_WHOLE_CLASS", "O02");
  const o02Execution = `${byId.O02?.visible || ""}\n${byId.O02?.student_action?.join("\n") || ""}\n${byId.O02?.script?.teacher_spoken || ""}\n${byId.O02?.script?.stage_directions?.join("\n") || ""}`;
  if (/沿座位|逐人面向全班|每个人公开/u.test(o02Execution)) fail("SERIAL_WHOLE_CLASS_QUEUE_REAPPEARS", "O02");
  if (!/让我想到什么|朴素主题/u.test(`${byId.O01?.visible || ""}${byId.O01?.unique_function || ""}`)) fail("O01_THEME_ARTIFACT_MISSING", "O01");
  if (!/让我想到爱情或婚姻/u.test(byId.O02?.visible || "")) fail("O02_THEME_SPEECH_FRAME_MISSING", "O02");
  if (!byId.O03?.teacher_synthesis.includes("引用本班篇名与原话")) fail("SYNTHESIS_NOT_GROUNDED_IN_LIVE_SPEECH", "O03");
  if (!byId.O03?.script?.teacher_spoken.includes("记错、漏掉") || !byId.O03?.script?.teacher_spoken.includes("黑板还没有替我们回答的问题")) fail("O03_FACT_CHECK_OR_NEW_DIRECTION_MISSING", "O03");
  if (/说窄|哪一项归纳/u.test(JSON.stringify(byId.O03 || {}))) fail("O03_DEEP_META_ANALYSIS_REAPPEARS", "O03");
  if (!EXPECTED_QUESTIONS.every((question) => byId.O08?.visible.includes(question))) fail("THREE_QUESTIONS_NOT_POST_LISTENING", "O08");
  if (/婚后的不幸|为什么走到/u.test(pages.slice(0, 7).map((item) => item.visible).join("\n"))) fail("THREE_QUESTIONS_LEAK_BEFORE_INITIAL_RESPONSE", "O01-O07");
  if (/不齐读|不回答|不要/u.test(byId.O05?.visible || "") || /不齐读|不回答|不要/u.test(byId.O06?.visible || "")) {
    fail("LISTENING_SLIDE_NEGATIVE_CONTROL", "O05/O06");
  }
  if (byId.O09?.visible.match(/305/g)?.length !== 1) fail("POETRY_IDENTITY_HIERARCHY_INVALID", "O09");
  if (!byId.O07?.next_use.includes("O08开头立即引用")) fail("INITIAL_RESPONSE_NOT_IMMEDIATELY_REUSED", "O07");

  return { ok: errors.length === 0, module_id: data.module_id, pages: pages.length, total_minutes: data.total_minutes, errors, warnings: warn };
}

function main() {
  const report = validate(payload);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  if (!report.ok) process.exitCode = 1;
}

if (require.main === module) main();
module.exports = { validate };
