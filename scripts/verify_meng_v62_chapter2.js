#!/usr/bin/env node
"use strict";

const payload = require("./meng_v62/content/chapter_2");
const { contract: textContract } = require("./meng_v6/text");
const { validate: validateTextContract } = require("./meng_v6/verify_text");

const EXPECTED_IDS = ["C201", "C202", "C204", "C206"];
const EXPECTED_LINES = ["L006", "L007", "L008", "L009", "L010"];
const VISIBLE_BANNED = [
  /学生画像/u, /教学目标/u, /设计意图/u, /理解链/u, /学习任务群/u,
  /签认/u, /查重/u, /回执编号/u, /卡号/u, /组号/u, /标准答案/u,
  /背叛/u, /粗暴/u, /压榨/u, /三年劳作/u, /兄弟/u, /离开/u,
  /一定幸福/u, /保证以后/u, /证明婚姻/u,
];
const RETIRED_PROCEDURE = [/七词复位/u, /乱序：迁/u, /△待调整/u, /原提议者号/u, /贡献卡/u];
const ANSWER_LEAKS = [
  /女子登上残破的墙/u, /看不见复关，她哭/u, /已经看见复关/u,
  /显示的兆象没有不祥/u, /你驾车来接我/u, /我带着嫁妆/u,
];

function compact(text) { return String(text).replace(/[，。！？；：、\s｜《》“”‘’—]/gu, ""); }

function validate(data = payload) {
  const errors = [];
  const warnings = [];
  const fail = (code, pageId = "MODULE", detail = "") => errors.push({ code, page_id: pageId, detail });
  if (data.module_id !== "MENG_V62_CHAPTER_2" || data.module !== "chapter_2") fail("IDENTITY_MISMATCH");
  if (data.status !== "implementation_candidate") fail("STATUS_NOT_CANDIDATE");
  if (data.prerequisite_module !== "MENG_V62_CHAPTER_1" || data.next_module !== "MENG_V62_CHAPTER_3") fail("MODULE_CHAIN_MISMATCH");
  const pages = Array.isArray(data.pages) ? data.pages : [];
  if (JSON.stringify(pages.map((item) => item.page_id)) !== JSON.stringify(EXPECTED_IDS)) fail("PAGE_SEQUENCE_MISMATCH");
  if (data.total_minutes !== 27 || pages.reduce((sum, item) => sum + Number(item.minutes || 0), 0) !== 27) fail("TOTAL_TIME_MISMATCH");
  const textErrors = validateTextContract(textContract);
  if (textErrors.length) fail("FROZEN_TEXT_CONTRACT_INVALID", "MODULE", textErrors.join(","));
  const chapter = textContract.chapters.find((item) => item.chapter_id === "C2");
  const lineMap = Object.fromEntries(textContract.lines.map((item) => [item.line_id, item.text]));
  if (compact((data.chapter_text || []).join("")) !== compact(chapter.line_ids.map((id) => lineMap[id]).join(""))) fail("CHAPTER_TEXT_MISMATCH");
  const materialIds = (data.materials || []).map((item) => item.material_id);
  if (JSON.stringify(materialIds) !== JSON.stringify(["CH2-A", "CH2-B"])) fail("MATERIAL_SEQUENCE_MISMATCH");
  const materials = Object.fromEntries((data.materials || []).map((item) => [item.material_id, item]));
  if (materials["CH2-A"]?.first_distribution_event !== "C201_AFTER_COMPLETE_READ") fail("CH2_A_WRONG_DISTRIBUTION");
  if (materials["CH2-B"]?.first_distribution_event !== "C202") fail("CH2_B_WRONG_DISTRIBUTION");

  const seenRefs = new Set();
  const signatures = new Set();
  for (const page of pages) {
    const id = page.page_id || "UNKNOWN";
    const required = ["title", "source_line_refs", "original_text", "literary_object", "current_difficulty", "unique_function", "visible", "first_glance", "information_state", "student_action", "artifact", "normal_path", "bounded_feedback", "revision", "teacher_synthesis", "story_return", "next_use", "deletion_loss", "merge_test", "visual_duty", "interaction_signature", "first_person_reception", "script"];
    for (const key of required) {
      const value = page[key];
      if (value === undefined || value === null || (typeof value === "string" && !value.length) || (Array.isArray(value) && !value.length)) fail("REQUIRED_FIELD_EMPTY", id, key);
    }
    if (!Number.isFinite(page.minutes) || page.minutes <= 0) fail("INVALID_MINUTES", id);
    if (!Array.isArray(page.student_action) || page.student_action.length < 1 || page.student_action.length > 3) fail("ACTION_BUDGET_EXCEEDED", id);
    for (const ref of page.source_line_refs || []) {
      if (!EXPECTED_LINES.includes(ref)) fail("OUT_OF_CHAPTER_LINE_REF", id, ref);
      seenRefs.add(ref);
      if (!compact(page.original_text).includes(compact(lineMap[ref] || ""))) fail("LINE_REF_TEXT_MISMATCH", id, ref);
    }
    const seconds = (page.script?.timeboxes || []).reduce((sum, item) => sum + Number(item.seconds || 0), 0);
    if (seconds !== page.minutes * 60) fail("TIMEBOX_MISMATCH", id, `${seconds}/${page.minutes * 60}`);
    if (!Array.isArray(page.script?.branches) || page.script.branches.length < 3) fail("CLASSROOM_BRANCHES_TOO_THIN", id);
    if (!Array.isArray(page.script?.stage_directions) || page.script.stage_directions.length < 4) fail("STAGING_TOO_THIN", id);
    if (!page.script?.teacher_spoken || page.script.teacher_spoken.length < 220) fail("SCRIPT_NOT_REHEARSABLE", id);
    if (page.story_return.length < 26) fail("STORY_RETURN_TOO_THIN", id);
    if (page.next_use.length < 25) fail("NEXT_USE_UNPROVEN", id);
    if (page.deletion_loss.length < 28) fail("DELETION_LOSS_UNPROVEN", id);
    if (page.merge_test.length < 35) fail("MERGE_TEST_UNPROVEN", id);
    for (const pattern of VISIBLE_BANNED) if (pattern.test(page.visible)) fail("STUDENT_VISIBLE_META_OR_PREMATURE_FACT", id, String(pattern));
    for (const pattern of ANSWER_LEAKS) if (pattern.test(page.visible)) fail("COMPLETED_ANSWER_VISIBLE", id, String(pattern));
    for (const pattern of RETIRED_PROCEDURE) if (pattern.test(JSON.stringify(page))) fail("RETIRED_PROCEDURE_REAPPEARS", id, String(pattern));
    const sig = page.interaction_signature || {};
    const signature = [sig.cognitive_action, sig.sensory_channel, sig.social_structure, sig.artifact_form].join("|");
    if (signatures.has(signature)) fail("INTERACTION_SIGNATURE_DUPLICATED", id, signature);
    signatures.add(signature);
  }
  if (JSON.stringify([...seenRefs].sort()) !== JSON.stringify(EXPECTED_LINES)) fail("SECOND_CHAPTER_COVERAGE_INCOMPLETE");
  const byId = Object.fromEntries(pages.map((item) => [item.page_id, item]));
  if (!byId.C201?.script?.teacher_spoken.includes("读完以后我才发03A") || !byId.C201.script.teacher_spoken.includes("完整读一遍")) fail("C201_MATERIAL_AFTER_READ_NOT_EXECUTABLE", "C201");
  if (/等待从登高远望开始|读后再发视线卡/u.test(`${byId.C201?.title || ""}${byId.C201?.visible || ""}`)) fail("C201_TITLE_OR_FRONTSTAGE_LEAK", "C201");
  if (!/动作、自然话和视线全部写在03A/u.test(byId.C201?.script?.scene || "")) fail("C201_ARTIFACT_LOCATION_AMBIGUOUS", "C201");
  if (!byId.C202?.script?.scene.includes("才发03B")) fail("C202_MATERIAL_ORDER_BROKEN", "C202");
  if (/失落|喜悦|伤心|高兴/u.test(byId.C202?.visible || "")) fail("C202_EMOTION_LABEL_PRECOMPLETED", "C202");
  if (!/只选一处/u.test(byId.C202?.visible || "") || !/闭着眼睛/u.test(byId.C202?.visible || "")) fail("C202_BLIND_LISTEN_CORE_MISSING", "C202");
  if (/保证|后来幸福|一定幸福/u.test(byId.C204?.visible || "")) fail("C204_FUTURE_BOUNDARY_PRECOMPLETED", "C204");
  if (/嫁妆|男子|女子|车来迎|迁嫁/u.test(byId.C204?.visible || "")) fail("C204_PARALLEL_ANSWER_VISIBLE", "C204");
  if (!/以尔.*以我/u.test(byId.C204?.visible || "") || !/各是谁、带着什么、做什么/u.test(byId.C204?.visible || "")) fail("C204_PARALLEL_OPEN_PROMPT_MISSING", "C204");
  if (/七词|排序|编号/u.test(byId.C206?.visible || "") || /七词|排序|编号/u.test(byId.C206?.script?.teacher_spoken || "")) fail("C206_SEVEN_WORD_SORT_REAPPEARS", "C206");
  if (!/03A和03B同时翻到背面/u.test(byId.C206?.script?.teacher_spoken || "")) fail("C206_ALL_PAPER_SUPPORTS_NOT_REMOVED", "C206");
  if (!/按B键熄暗屏幕/u.test(byId.C206?.script?.teacher_spoken || "")) fail("C206_PROJECTOR_SUPPORT_NOT_REMOVED", "C206");
  if (pages.some((item) => ["C203", "C205"].includes(item.page_id))) fail("RETIRED_STANDALONE_PROGRAM_PAGE_REAPPEARS");
  if (pages.length !== 4) fail("FOUR_EVENT_STRUCTURE_MISMATCH");
  return { ok: errors.length === 0, module_id: data.module_id, pages: pages.length, total_minutes: data.total_minutes, errors, warnings };
}

function main() { const report = validate(payload); process.stdout.write(`${JSON.stringify(report, null, 2)}\n`); if (!report.ok) process.exitCode = 1; }
if (require.main === module) main();
module.exports = { validate };
