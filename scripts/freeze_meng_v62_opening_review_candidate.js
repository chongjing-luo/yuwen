#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const source = require("./meng_v62/content/opening");
const { validate } = require("./verify_meng_v62_opening");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const ROOT = path.join(stageDir(), "opening");
const REVIEW_DIR = assertV62OutputPath(path.join(ROOT, "reviews"));
const OUTPUT = assertV62OutputPath(path.join(REVIEW_DIR, "review_input_v4.json"));

function sha256(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function rel(filePath) { return path.relative(PROJECT_ROOT, filePath).split(path.sep).join("/"); }

function item(filePath, role) {
  if (!fs.existsSync(filePath)) throw new Error(`missing review input: ${filePath}`);
  return { role, path: rel(filePath), sha256: sha256(filePath), bytes: fs.statSync(filePath).size };
}

function main() {
  const verification = validate(source);
  if (!verification.ok) throw new Error(`opening contract failed: ${JSON.stringify(verification.errors)}`);
  const packageDir = path.join(ROOT, "package");
  const pptxDir = path.join(ROOT, "pptx");
  const renderDir = path.join(pptxDir, "rendered_v4");
  const files = [
    item(path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "opening.js"), "single_source"),
    item(path.join(packageDir, "02_氓_V62导入教学母版.md"), "teaching_master"),
    item(path.join(packageDir, "03A_爱情与婚姻文学回忆单_O01发.md"), "literature_recall_sheet_O01"),
    item(path.join(packageDir, "03B_氓_V62初听卡_O07发.md"), "initial_response_card_O07"),
    item(path.join(packageDir, "03C_氓_V62三问阅读书签_O08发.md"), "question_bookmark_O08"),
    item(path.join(packageDir, "04A_氓_V62导入逐页无生试讲稿.md"), "rehearsal_script"),
    item(path.join(packageDir, "06_氓_V62导入课程数据快照.json"), "data_snapshot"),
    item(path.join(pptxDir, "04_氓_V62导入课堂课件.pptx"), "pptx"),
    item(path.join(pptxDir, "markitdown_v4.txt"), "pptx_text_and_notes"),
    item(path.join(renderDir, "04_氓_V62导入课堂课件.pdf"), "rendered_pdf"),
    item(path.join(renderDir, "contact.jpg"), "visual_contact_sheet"),
    ...Array.from({ length: 9 }, (_, index) => item(path.join(renderDir, `slide-${index + 1}.png`), `rendered_slide_${index + 1}`)),
  ];
  const manifest = {
    schema_version: "1.0",
    review_input_id: "MENG_V62_OPENING_REVIEW_V4",
    created_at: new Date().toISOString(),
    status: "immutable_review_candidate",
    module_id: source.module_id,
    page_ids: source.pages.map((page) => page.page_id),
    total_minutes: source.total_minutes,
    distribution_order: ["03A at O01; contains no Meng title or later scaffold", "03B at O07 after complete listening", "03C at O08 after O07 response", "O09 scaffold written into textbook; never preprinted"],
    release_gate: "P0=0 and P1=0 and P2=0 in both independent reviews",
    illustration_policy: "no_character_illustration_until_function_freeze",
    files,
  };
  fs.mkdirSync(REVIEW_DIR, { recursive: true });
  fs.writeFileSync(OUTPUT, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`V62_OPENING_REVIEW_INPUT_OK files=${files.length} manifest=${OUTPUT} sha256=${sha256(OUTPUT)}\n`);
}

main();
