#!/usr/bin/env node
"use strict";

const payload = require("./meng_v62/content/chapter_1");
const { contract: textContract } = require("./meng_v6/text");
const { validate: validateTextContract } = require("./meng_v6/verify_text");

const EXPECTED_IDS = ["C101", "C102", "C103", "C104", "C105"];
const EXPECTED_LINES = ["L001", "L002", "L003", "L004", "L005"];
const VISIBLE_BANNED = [
  /学生画像/u, /教学目标/u, /设计意图/u, /理解链/u, /学习任务群/u,
  /签认/u, /查重/u, /回执/u, /卡号/u, /组号/u, /标准答案/u,
  /恋爱脑/u, /沉没成本/u, /背叛/u, /压榨/u, /家人不理解/u,
  /婚后粗暴/u, /三年劳作/u, /兄弟咥笑/u, /反是不思/u,
];
const RETIRED_PROCEDURE = [/原提议者号/u, /签认/u, /查重/u, /回执/u, /卡墙/u, /贡献卡/u];
const ANSWER_LEAKS = [
  /男子看起来忠厚，抱着布来换丝/u,
  /女子送男子渡过淇水，一直送到顿丘/u,
  /不是我有意拖延婚期/u,
  /请你不要生气，就把秋天定作婚期/u,
  /装老实欺骗/u,
];

function compact(text) {
  return String(text).replace(/[，。！？；：、\s｜《》“”‘’—]/gu, "");
}

function validate(data = payload) {
  const errors = [];
  const warnings = [];
  const fail = (code, pageId = "MODULE", detail = "") => errors.push({ code, page_id: pageId, detail });

  if (data.module_id !== "MENG_V62_CHAPTER_1" || data.module !== "chapter_1") fail("IDENTITY_MISMATCH");
  if (data.status !== "implementation_candidate") fail("STATUS_NOT_CANDIDATE");
  if (data.prerequisite_module !== "MENG_V62_OPENING" || data.next_module !== "MENG_V62_CHAPTER_2") fail("MODULE_CHAIN_MISMATCH");

  const pages = Array.isArray(data.pages) ? data.pages : [];
  if (JSON.stringify(pages.map((item) => item.page_id)) !== JSON.stringify(EXPECTED_IDS)) fail("PAGE_SEQUENCE_MISMATCH");
  if (data.total_minutes !== 27 || pages.reduce((sum, item) => sum + Number(item.minutes || 0), 0) !== 27) fail("TOTAL_TIME_MISMATCH");

  const textErrors = validateTextContract(textContract);
  if (textErrors.length) fail("FROZEN_TEXT_CONTRACT_INVALID", "MODULE", textErrors.join(","));
  const chapter = textContract.chapters.find((item) => item.chapter_id === "C1");
  const lineMap = Object.fromEntries(textContract.lines.map((item) => [item.line_id, item.text]));
  const expectedText = compact(chapter.line_ids.map((id) => lineMap[id]).join(""));
  if (compact((data.chapter_text || []).join("")) !== expectedText) fail("CHAPTER_TEXT_MISMATCH");

  const materialIds = (data.materials || []).map((item) => item.material_id);
  if (JSON.stringify(materialIds) !== JSON.stringify(["CH1-A", "CH1-B"])) fail("MATERIAL_SEQUENCE_MISMATCH");
  const materials = Object.fromEntries((data.materials || []).map((item) => [item.material_id, item]));
  if (materials["CH1-A"]?.first_distribution_event !== "C101") fail("CH1_A_WRONG_DISTRIBUTION");
  if (materials["CH1-B"]?.first_distribution_event !== "C102") fail("CH1_B_WRONG_DISTRIBUTION");
  if (!/不出现词义/u.test(materials["CH1-A"]?.information_boundary || "")) fail("CH1_A_BOUNDARY_MISSING");
  if (!/不预填译文/u.test(materials["CH1-B"]?.information_boundary || "")) fail("CH1_B_BOUNDARY_MISSING");

  const seenRefs = new Set();
  const signatures = new Set();
  for (const page of pages) {
    const id = page.page_id || "UNKNOWN";
    const required = [
      "title", "source_line_refs", "original_text", "literary_object", "current_difficulty", "unique_function",
      "visible", "first_glance", "information_state", "student_action", "artifact", "normal_path",
      "bounded_feedback", "revision", "teacher_synthesis", "story_return", "next_use", "deletion_loss",
      "merge_test", "visual_duty", "interaction_signature", "first_person_reception", "script",
    ];
    for (const key of required) {
      const value = page[key];
      if (value === undefined || value === null || (typeof value === "string" && !value.length) || (Array.isArray(value) && !value.length)) {
        fail("REQUIRED_FIELD_EMPTY", id, key);
      }
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
    if (!Array.isArray(page.script?.branches) || page.script.branches.length < 2) fail("CLASSROOM_BRANCHES_TOO_THIN", id);
    if (!Array.isArray(page.script?.stage_directions) || page.script.stage_directions.length < 3) fail("STAGING_TOO_THIN", id);
    if (!page.script?.teacher_spoken || page.script.teacher_spoken.length < 180) fail("SCRIPT_NOT_REHEARSABLE", id);
    if (!page.script?.listener_task || !page.script?.evidence_location || !page.script?.cut_line) fail("SCRIPT_EVIDENCE_CHAIN_INCOMPLETE", id);
    if (page.story_return.length < 24) fail("STORY_RETURN_TOO_THIN", id);
    if (page.next_use.length < 20) fail("NEXT_USE_UNPROVEN", id);
    if (page.deletion_loss.length < 24) fail("DELETION_LOSS_UNPROVEN", id);
    if (page.merge_test.length < 30) fail("MERGE_TEST_UNPROVEN", id);
    if (!/故事|人物|婚事|男子|女子|相遇|等待/u.test(page.story_return)) fail("NO_RETURN_TO_STORY", id);
    for (const pattern of VISIBLE_BANNED) if (pattern.test(page.visible)) fail("STUDENT_VISIBLE_META_OR_PREMATURE_FACT", id, String(pattern));
    for (const pattern of ANSWER_LEAKS) if (pattern.test(page.visible)) fail("COMPLETED_ANSWER_VISIBLE", id, String(pattern));
    for (const pattern of RETIRED_PROCEDURE) if (pattern.test(JSON.stringify(page))) fail("RETIRED_PROCEDURE_REAPPEARS", id, String(pattern));
    const sig = page.interaction_signature || {};
    const signature = [sig.cognitive_action, sig.sensory_channel, sig.social_structure, sig.artifact_form].join("|");
    if (signatures.has(signature)) fail("INTERACTION_SIGNATURE_DUPLICATED", id, signature);
    signatures.add(signature);
  }
  if (JSON.stringify([...seenRefs].sort()) !== JSON.stringify(EXPECTED_LINES)) fail("FIRST_CHAPTER_COVERAGE_INCOMPLETE");

  const byId = Object.fromEntries(pages.map((item) => [item.page_id, item]));
  if (!byId.C101?.script?.scene.includes("03A") || /03B/u.test(byId.C101?.script?.scene || "")) fail("C101_MATERIAL_ORDER_BROKEN", "C101");
  if (!byId.C102?.script?.scene.includes("03B")) fail("C102_MATERIAL_ORDER_BROKEN", "C102");
  if (!/贸丝/u.test(byId.C102?.visible || "") || !/哪个字/u.test(byId.C102?.visible || "")) fail("C102_TURN_NOT_DISCOVERABLE", "C102");
  if (/→|渡过|一直送到/u.test(byId.C103?.visible || "")) fail("C103_ROUTE_PRECOMPLETED", "C103");
  if (/解释|安抚|约期/u.test(byId.C103?.script?.cut_line || "")) fail("C103_CUT_LINE_LEAKS_C104_SPEECH_ACTS", "C103");
  if (/拒婚|暴力|生气/u.test(byId.C104?.visible || "")) fail("C104_DIALOGUE_PREJUDGED", "C104");
  if (/解释什么|安抚什么|定了下来/u.test(byId.C104?.visible || "")) fail("C104_SPEECH_ACT_LABELS_PRECOMPLETED", "C104");
  if (!/四小句，各在做什么/u.test(byId.C104?.visible || "")) fail("C104_OPEN_GENERATION_MISSING", "C104");
  if (!/他怎样来｜她怎样送｜婚事怎样暂缓又约定/u.test(byId.C105?.visible || "")) fail("C105_STORY_REBUILD_MISSING", "C105");
  if (!byId.C105?.next_use.includes("C201开头直接打开")) fail("CHAPTER_RAIL_NOT_REUSED", "C105");
  if (!/03A初读卡和03B细读单一起翻到背面/u.test(byId.C105?.script?.teacher_spoken || "")) fail("C105_ALL_PAPER_SUPPORTS_NOT_REMOVED", "C105");
  if (!/同桌互相看一眼/u.test(byId.C105?.script?.teacher_spoken || "") || !/按B键熄暗屏幕/u.test(byId.C105?.script?.teacher_spoken || "")) fail("C105_RETRIEVAL_CONTROL_INCOMPLETE", "C105");
  if (pages.length !== 5) fail("OLD_NINE_PAGE_STRUCTURE_REAPPEARS");

  return { ok: errors.length === 0, module_id: data.module_id, pages: pages.length, total_minutes: data.total_minutes, errors, warnings };
}

function main() {
  const report = validate(payload);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  if (!report.ok) process.exitCode = 1;
}

if (require.main === module) main();
module.exports = { validate };
