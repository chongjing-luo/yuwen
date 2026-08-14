#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const source = require("./meng_v62/content/chapter_1");
const { validate } = require("./verify_meng_v62_chapter1");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const ROOT = path.join(stageDir(), "chapter_1");
const REVIEW_DIR = assertV62OutputPath(path.join(ROOT, "reviews"));
const OUTPUT = assertV62OutputPath(path.join(REVIEW_DIR, "review_input_v5.json"));

function sha256(filePath) { return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex"); }
function rel(filePath) { return path.relative(PROJECT_ROOT, filePath).split(path.sep).join("/"); }
function item(filePath, role) {
  if (!fs.existsSync(filePath)) throw new Error(`missing review input: ${filePath}`);
  return { role, path: rel(filePath), sha256: sha256(filePath), bytes: fs.statSync(filePath).size };
}

function main() {
  const verification = validate(source);
  if (!verification.ok) throw new Error(`chapter1 contract failed: ${JSON.stringify(verification.errors)}`);
  const packageDir = path.join(ROOT, "package");
  const pptxDir = path.join(ROOT, "pptx");
  const renderDir = path.join(pptxDir, "rendered_v5");
  const files = [
    item(path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "chapter_1.js"), "single_source"),
    item(path.join(packageDir, "02_氓_V62第一章教学母版.md"), "teaching_master"),
    item(path.join(packageDir, "03A_氓_V62第一章初读卡_C101发.md"), "initial_read_card_C101"),
    item(path.join(packageDir, "03B_氓_V62第一章细读与故事轨道_C102发.md"), "close_reading_card_C102"),
    item(path.join(packageDir, "04A_氓_V62第一章逐页无生试讲稿.md"), "rehearsal_script"),
    item(path.join(packageDir, "06_氓_V62第一章课程数据快照.json"), "data_snapshot"),
    item(path.join(pptxDir, "04_氓_V62第一章课堂课件.pptx"), "pptx"),
    item(path.join(pptxDir, "markitdown_v5.txt"), "pptx_text_and_notes"),
    item(path.join(renderDir, "04_氓_V62第一章课堂课件.pdf"), "rendered_pdf"),
    item(path.join(renderDir, "contact.jpg"), "visual_contact_sheet"),
    ...Array.from({ length: 5 }, (_, index) => item(path.join(renderDir, `slide-${index + 1}.png`), `rendered_slide_${index + 1}`)),
    item(path.join(REVIEW_DIR, "internal_visual_qa_v1.md"), "internal_first_fix_and_verify_record"),
    item(path.join(REVIEW_DIR, "v2_independent_review_disposition.md"), "v2_rejection_and_disposition"),
    item(path.join(PROJECT_ROOT, "scripts", "meng_v62", "reviews", "chapter1_visual_v2.json"), "v2_independent_visual_fail"),
    item(path.join(PROJECT_ROOT, "scripts", "meng_v62", "reviews", "chapter1_student_v2.json"), "v2_independent_student_fail"),
    item(path.join(REVIEW_DIR, "internal_visual_qa_v3.md"), "v3_internal_fix_and_verify_record"),
    item(path.join(REVIEW_DIR, "v3_review_abort_integrity.md"), "v3_review_abort_integrity_record"),
    item(path.join(REVIEW_DIR, "v4_independent_review_disposition.md"), "v4_rejection_and_disposition"),
    item(path.join(PROJECT_ROOT, "scripts", "meng_v62", "reviews", "chapter1_visual_v4.json"), "v4_independent_visual_fail"),
  ];
  const manifest = {
    schema_version: "1.0", review_input_id: "MENG_V62_CHAPTER1_REVIEW_V5",
    created_at: new Date().toISOString(), status: "immutable_review_candidate",
    module_id: source.module_id, page_ids: source.pages.map((page) => page.page_id), total_minutes: source.total_minutes,
    distribution_order: ["03A at C101; poem, action marks, question marks only", "03B at C102 after C101; open prompts and blank story rail only"],
    required_review_axes: [
      "per-page unique literary function and deletion loss", "adjacent merge and global story-chain necessity",
      "student generation before teacher calibration", "no completed answer or later fact on frontstage",
      "rehearsable script, listener task, evidence, revision, story return and next use",
      "interaction variety without procedure overload", "visual readability, hierarchy, alignment and functional restraint",
      "C105 projector blackout makes closed-book retrieval genuine",
      "C104 does not pre-name explanation, appeasement or appointment before student generation",
      "C105 explicitly removes textbook, CH1-A/03A and CH1-B/03B before projector blackout",
      "C103 cut line does not orally pre-name C104's student-generated speech-act categories",
    ],
    release_gate: "P0=0 and P1=0 and P2=0 in both independent reviews",
    illustration_policy: "no_character_illustration_until_all_lesson_functions_are_frozen",
    files,
  };
  fs.mkdirSync(REVIEW_DIR, { recursive: true });
  fs.writeFileSync(OUTPUT, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`V62_CHAPTER1_REVIEW_INPUT_OK files=${files.length} manifest=${OUTPUT} sha256=${sha256(OUTPUT)}\n`);
}

main();
