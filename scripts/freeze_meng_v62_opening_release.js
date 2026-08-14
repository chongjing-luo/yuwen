#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");
const source = require("./meng_v62/content/opening");
const { validate } = require("./verify_meng_v62_opening");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const ROOT = path.join(stageDir(), "opening");
const REVIEW_INPUT = path.join(ROOT, "reviews", "review_input_v4.json");
const VISUAL_REVIEW = path.join(PROJECT_ROOT, "scripts", "meng_v62", "reviews", "opening_visual_v4.json");
const STUDENT_REVIEW = path.join(PROJECT_ROOT, "scripts", "meng_v62", "reviews", "opening_student_v4.json");
const RECEIPT = assertV62OutputPath(path.join(ROOT, "opening_freeze_receipt.json"));
const MANIFEST_SHA = "29a5b1ce3a6f7d06f64db035531ac5e62e0e65932796d629f1063aad580dcde5";

function sha256(filePath) { return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex"); }
function rel(filePath) { return path.relative(PROJECT_ROOT, filePath).split(path.sep).join("/"); }

function priorityCounts(report) {
  return report.priority_counts || report.severity_counts || report.counts || {};
}

function assertPass(report, label) {
  const counts = priorityCounts(report);
  for (const key of ["P0", "P1", "P2"]) {
    if (Number(counts[key] || 0) !== 0) throw new Error(`${label} has unresolved ${key}`);
  }
  const verdict = String(report.verdict || report.total_verdict || report.status || "").toUpperCase();
  if (!verdict.includes("PASS")) throw new Error(`${label} verdict is not PASS: ${verdict}`);
}

function main() {
  const verification = validate(source);
  if (!verification.ok) throw new Error(`source contract failed: ${JSON.stringify(verification.errors)}`);
  if (sha256(REVIEW_INPUT) !== MANIFEST_SHA) throw new Error("review input manifest hash mismatch");
  const manifest = JSON.parse(fs.readFileSync(REVIEW_INPUT, "utf8"));
  for (const item of manifest.files) {
    const filePath = path.join(PROJECT_ROOT, item.path);
    if (!fs.existsSync(filePath) || sha256(filePath) !== item.sha256 || fs.statSync(filePath).size !== item.bytes) {
      throw new Error(`reviewed input changed: ${item.path}`);
    }
  }
  const visual = JSON.parse(fs.readFileSync(VISUAL_REVIEW, "utf8"));
  const student = JSON.parse(fs.readFileSync(STUDENT_REVIEW, "utf8"));
  assertPass(visual, "visual review");
  assertPass(student, "student review");
  const receipt = {
    schema_version: "1.0",
    receipt_id: "MENG_V62_OPENING_FREEZE_V4",
    module_id: source.module_id,
    status: "frozen",
    frozen_at: new Date().toISOString(),
    page_ids: source.pages.map((page) => page.page_id),
    logical_pages: source.pages.length,
    total_minutes: source.total_minutes,
    reviewed_input: { path: rel(REVIEW_INPUT), sha256: MANIFEST_SHA, files: manifest.files.length },
    independent_reviews: [
      { kind: "visual", path: rel(VISUAL_REVIEW), sha256: sha256(VISUAL_REVIEW), counts: priorityCounts(visual), verdict: visual.verdict || visual.total_verdict || visual.status },
      { kind: "student_reception", path: rel(STUDENT_REVIEW), sha256: sha256(STUDENT_REVIEW), counts: priorityCounts(student), verdict: student.verdict || student.total_verdict || student.status },
    ],
    release_gate: { P0: 0, P1: 0, P2: 0, passed: true },
    distribution_order: manifest.distribution_order,
    illustration_policy: "no_character_illustration_until_all_lesson_functions_are_frozen",
    claim_boundary: "desktop_design_frozen_not_classroom_observed",
    p3_policy: "P3 items remain pilot observations and do not justify claims of student learning.",
  };
  fs.writeFileSync(RECEIPT, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
  process.stdout.write(`V62_OPENING_FROZEN receipt=${RECEIPT} sha256=${sha256(RECEIPT)}\n`);
}

main();
