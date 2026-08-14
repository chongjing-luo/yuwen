#!/usr/bin/env node
"use strict";

const payload = require("./meng_v62/content/chapter_3");
const { contract: textContract } = require("./meng_v6/text");
const { validate: validateTextContract } = require("./meng_v6/verify_text");

const EXPECTED_IDS = ["C301", "C302", "C303", "C305", "C306"];
const EXPECTED_LINES = ["L011", "L012", "L013", "L014", "L015"];
const VISIBLE_BANNED = [
  /学生画像/u, /教学目标/u, /设计意图/u, /理解链/u, /学习任务群/u,
  /签认/u, /查重/u, /回执/u, /卡号/u, /组号/u, /标准答案/u,
  /恋爱脑/u, /沉没成本/u, /婚后粗暴/u, /长期劳作/u, /兄弟不知/u,
  /女子的投入，不分担/u,
];
const PREMATURE_TERMS = [/由物起兴/u, /由物及人/u, /比兴/u];

function compact(text) { return String(text).replace(/[，。！？；：、\s｜《》“”‘’—]/gu, ""); }

function validate(data = payload) {
  const errors = [];
  const warnings = [];
  const fail = (code, pageId = "MODULE", detail = "") => errors.push({ code, page_id: pageId, detail });
  if (data.module_id !== "MENG_V63_CHAPTER_3" || data.module !== "chapter_3") fail("IDENTITY_MISMATCH");
  if (data.status !== "implementation_candidate") fail("STATUS_NOT_CANDIDATE");
  if (data.prerequisite_module !== "MENG_V62_CHAPTER_2" || data.next_module !== "MENG_V63_CHAPTER_4") fail("MODULE_CHAIN_MISMATCH");
  const pages = Array.isArray(data.pages) ? data.pages : [];
  if (JSON.stringify(pages.map((item) => item.page_id)) !== JSON.stringify(EXPECTED_IDS)) fail("PAGE_SEQUENCE_MISMATCH");
  if (data.total_minutes !== 30 || pages.reduce((sum, item) => sum + Number(item.minutes || 0), 0) !== 30) fail("TOTAL_TIME_MISMATCH");
  const textErrors = validateTextContract(textContract);
  if (textErrors.length) fail("FROZEN_TEXT_CONTRACT_INVALID", "MODULE", textErrors.join(","));
  const lineMap = Object.fromEntries(textContract.lines.map((item) => [item.line_id, item.text]));
  const chapter = textContract.chapters.find((item) => item.chapter_id === "C3");
  if (compact((data.chapter_text || []).join("")) !== compact(chapter.line_ids.map((id) => lineMap[id]).join(""))) fail("CHAPTER_TEXT_MISMATCH");
  if (JSON.stringify((data.materials || []).map((item) => item.material_id)) !== JSON.stringify(["CH3-C"])) fail("MATERIAL_SEQUENCE_MISMATCH");
  if (data.materials?.[0]?.first_distribution_event !== "C301_AFTER_COMPLETE_READ") fail("CH3_C_WRONG_DISTRIBUTION");

  const seenRefs = new Set();
  const signatures = new Set();
  for (const page of pages) {
    const id = page.page_id || "UNKNOWN";
    const required = ["title", "source_line_refs", "original_text", "literary_object", "current_difficulty", "unique_function", "visible", "first_glance", "information_state", "student_action", "artifact", "normal_path", "bounded_feedback", "revision", "teacher_synthesis", "story_return", "next_use", "deletion_loss", "merge_test", "visual_duty", "interaction_signature", "first_person_reception", "script"];
    for (const key of required) {
      const value = page[key];
      if (value === undefined || value === null || (typeof value === "string" && !value.length) || (Array.isArray(value) && !value.length)) fail("REQUIRED_FIELD_EMPTY", id, key);
    }
    if (!Array.isArray(page.student_action) || page.student_action.length < 1 || page.student_action.length > 3) fail("ACTION_BUDGET_EXCEEDED", id);
    for (const ref of page.source_line_refs || []) {
      if (!EXPECTED_LINES.includes(ref)) fail("OUT_OF_CHAPTER_LINE_REF", id, ref);
      seenRefs.add(ref);
      if (!compact(page.original_text).includes(compact(lineMap[ref] || ""))) fail("LINE_REF_TEXT_MISMATCH", id, ref);
    }
    const seconds = (page.script?.timeboxes || []).reduce((sum, item) => sum + Number(item.seconds || 0), 0);
    if (seconds !== page.minutes * 60) fail("TIMEBOX_MISMATCH", id, `${seconds}/${page.minutes * 60}`);
    if (!Array.isArray(page.script?.branches) || page.script.branches.length < 3) fail("CLASSROOM_BRANCHES_TOO_THIN", id);
    if (!Array.isArray(page.script?.stage_directions) || page.script.stage_directions.length < 5) fail("STAGING_TOO_THIN", id);
    if (!page.script?.teacher_spoken || page.script.teacher_spoken.length < 220) fail("SCRIPT_NOT_REHEARSABLE", id);
    if (page.story_return.length < 25) fail("STORY_RETURN_TOO_THIN", id);
    if (page.next_use.length < 25) fail("NEXT_USE_UNPROVEN", id);
    if (page.deletion_loss.length < 28) fail("DELETION_LOSS_UNPROVEN", id);
    if (page.merge_test.length < 35) fail("MERGE_TEST_UNPROVEN", id);
    for (const pattern of VISIBLE_BANNED) if (pattern.test(page.visible)) fail("STUDENT_VISIBLE_META_OR_PREMATURE_FACT", id, String(pattern));
    const signature = Object.values(page.interaction_signature || {}).slice(0, 4).join("|");
    if (signatures.has(signature)) fail("INTERACTION_SIGNATURE_DUPLICATED", id, signature);
    signatures.add(signature);
  }
  if (JSON.stringify([...seenRefs].sort()) !== JSON.stringify(EXPECTED_LINES)) fail("THIRD_CHAPTER_COVERAGE_INCOMPLETE");
  const byId = Object.fromEntries(pages.map((item) => [item.page_id, item]));
  for (const id of ["C301", "C302", "C303"]) for (const pattern of PREMATURE_TERMS) if (pattern.test(byId[id]?.visible || "")) fail("PREMATURE_BIXING_TERM_VISIBLE", id, String(pattern));
  if (!/蒙住前两句/u.test(byId.C303?.visible || "") || !/少了什么/u.test(byId.C303?.visible || "")) fail("C303_MERGED_COUNTERFACTUAL_MISSING", "C303");
  if (!/后文待证/u.test(byId.C305?.script?.teacher_spoken || "") || !/天生/u.test(byId.C305?.script?.teacher_spoken || "")) fail("C305_EVIDENCE_BOUNDARY_NOT_EXECUTABLE", "C305");
  if (!/合上教材/u.test(byId.C306?.script?.teacher_spoken || "") || !/按B键熄暗屏幕/u.test(byId.C306?.script?.teacher_spoken || "")) fail("C306_SUPPORT_REMOVAL_NOT_EXECUTABLE", "C306");
  if (pages.some((item) => /知识收纳/u.test(item.title))) fail("PER_CHAPTER_KNOWLEDGE_SHELF_REAPPEARS");
  return { ok: errors.length === 0, module_id: data.module_id, pages: pages.length, total_minutes: data.total_minutes, errors, warnings };
}

function main() {
  const report = validate(payload);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  if (!report.ok) process.exitCode = 1;
}

if (require.main === module) main();
module.exports = { validate };
