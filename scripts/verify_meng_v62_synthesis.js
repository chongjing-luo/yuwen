#!/usr/bin/env node
"use strict";

const payload = require("./meng_v62/content/synthesis");

const IDS = ["S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08"];
const VISIBLE_BANNED = [
  /学生画像/u, /教学目标/u, /设计意图/u, /理解链/u, /标准答案/u,
  /恋爱脑/u, /沉没成本/u, /教师总结/u, /五项标准/u, /鱼缸/u,
  /结构梁/u, /真实分歧/u, /知识收纳/u, /生活分镜/u,
];
const FORCED_PROCEDURES = [
  /必须.{0,8}(?:问号|分歧|修改|移动)/u,
  /每组.{0,8}(?:问号|争议|分歧)/u,
  /固定.{0,8}(?:争议|卡)/u,
  /鱼缸/u,
  /五根纸梁|五梁/u,
  /六种笔迹/u,
];

function validate(data = payload) {
  const errors = [];
  const warnings = [];
  const fail = (code, page_id = "MODULE", detail = "") => errors.push({ code, page_id, detail });

  if (data.module_id !== "MENG_V63_SYNTHESIS" || data.module !== "synthesis") fail("IDENTITY");
  if (data.status !== "implementation_candidate" || data.prerequisite_module !== "MENG_V63_CHAPTER_6") fail("CHAIN");
  const pages = data.pages || [];
  if (JSON.stringify(pages.map((item) => item.page_id)) !== JSON.stringify(IDS)) fail("SEQUENCE");
  if (data.total_minutes !== 79) fail("TOTAL_TIME", "MODULE", String(data.total_minutes));

  const signatures = new Set();
  for (const page of pages) {
    for (const key of [
      "title", "literary_object", "current_difficulty", "unique_function", "visible",
      "student_action", "artifact", "normal_path", "bounded_feedback", "revision",
      "teacher_synthesis", "story_return", "next_use", "deletion_loss", "merge_test",
      "visual_duty", "first_person_reception", "script",
    ]) {
      if (page[key] === undefined || page[key] === null || page[key] === "") fail("REQUIRED", page.page_id, key);
    }
    if (!Array.isArray(page.student_action) || page.student_action.length < 1 || page.student_action.length > 3) fail("ACTION_COUNT", page.page_id);
    const seconds = (page.script?.timeboxes || []).reduce((sum, item) => sum + Number(item.seconds || 0), 0);
    if (seconds !== page.minutes * 60) fail("TIMEBOX", page.page_id, `${seconds}/${page.minutes * 60}`);
    if ((page.script?.teacher_spoken || "").length < 260) fail("SCRIPT_THIN", page.page_id);
    if ((page.script?.branches || []).length < 3) fail("BRANCHES", page.page_id);
    if ((page.script?.stage_directions || []).length < 5) fail("STAGING", page.page_id);
    for (const pattern of VISIBLE_BANNED) if (pattern.test(page.visible)) fail("VISIBLE_LEAK", page.page_id, String(pattern));
    for (const pattern of FORCED_PROCEDURES) {
      const frontAndScript = `${page.visible}\n${page.script?.teacher_spoken || ""}`;
      if (pattern.test(frontAndScript)) fail("FORCED_PROCEDURE", page.page_id, String(pattern));
    }
    if (!/(?:无需改|保留|不制造|可留白)/u.test(page.normal_path || "")) fail("HONEST_NORMAL_PATH", page.page_id);
    const signature = (page.student_action || []).join("|").slice(0, 150);
    if (signatures.has(signature)) fail("DUP_SIGNATURE", page.page_id);
    signatures.add(signature);
  }

  const by = Object.fromEntries(pages.map((page) => [page.page_id, page]));
  if (!/六张章末卡/u.test(by.S01?.literary_object || "") || !/没有断点/u.test(by.S01?.normal_path || "")) fail("MOTHER_RAIL_REUSE", "S01");
  if (!/可配回，无需改/u.test(by.S02?.normal_path || "") || !/找回原诗/u.test(by.S02?.visible || "")) fail("Q2_HONEST_REVERSE_EVIDENCE", "S02");
  if (!/直接伤害责任/u.test(by.S03?.unique_function || "") || !/不归责/u.test(by.S03?.unique_function || "")) fail("Q3_RESPONSIBILITY", "S03");
  if (!/O03/u.test(by.S04?.literary_object || "") || !/主题谱照片/u.test(by.S04?.script?.teacher_spoken || "") || !/补充、修正或保留/u.test(by.S04?.unique_function || "")) fail("OPENING_CLOSURE", "S04");
  if (!/S07/u.test(by.S05?.next_use || "") || !/S07/u.test(by.S06?.next_use || "")) fail("KNOWLEDGE_REUSE", "S05-S06");
  if (!/S05/u.test(by.S07?.student_action?.join("") || "") || !/S06/u.test(by.S07?.student_action?.join("") || "")) fail("KNOWLEDGE_CONSUMER", "S07");
  if (!/仍愿继续追问/u.test(by.S08?.visible || "") || !/可留白/u.test(by.S08?.visible || "") || !/完整读/u.test(by.S08?.script?.teacher_spoken || "")) fail("FINAL_EXIT", "S08");
  if (!/停顿/u.test(by.S08?.script?.cut_line || "")) fail("ENDING_NOT_QUIET", "S08");

  return { ok: errors.length === 0, module_id: data.module_id, pages: pages.length, total_minutes: data.total_minutes, errors, warnings };
}

function main() {
  const report = validate(payload);
  process.stdout.write(`${JSON.stringify(report, null, 2)}\n`);
  if (!report.ok) process.exitCode = 1;
}

if (require.main === module) main();
module.exports = { validate };
