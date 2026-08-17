#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { contract: frozenContract } = require("./text");

const PROJECT_ROOT = path.resolve(__dirname, "../..");
const EXPECTED_SOURCE = {
  textbook_path: "Data/textbook_extract/选择性必修下册/mineru_result/01_U1_导语_课1_氓_离骚/full.md",
  textbook_sha256: "384266a83e13663cdf758c6202e2d5f95737ee5f25408bc3e229e295667a9cfd",
  evidence_dossier_path: "work/teaching/选择性必修下册/氓/01_文本研究与证据档案.md",
  evidence_dossier_sha256: "c0942e52d8655d40723f140b478cc1212292a733a342f796744fd1f51547ca10",
};
const SEMANTIC_HASHES = {
  chapters: "d01f80dfa26832620e2643966a9c97ebc5f4f4ebf6bfdb1f9f5ae9cbba5d543f",
  meaning_units: "15b198aa430b0b57ec361708c695cb072f6bcaa4e1b31381a220f6067d8146d5",
  interpretive_boundaries: "8c6b09c02efd87632a4ccb1ef60727887a92c4336e4dd8c313d0a1a80371edae",
};

const REQUIRED_BOUNDARIES = new Set([
  "CHI_CHI_IMPRESSION", "TRADE_VS_PROPOSAL", "NO_ANGER_AMBIGUITY", "SANG_LEAF_OPENNESS",
  "VIOLENCE_SCOPE", "FAMILY_SUPPORT_BOUNDARY", "QI_BANK_MULTIPLE_READINGS",
  "STOP_JUDGMENT_BOUNDARY", "RESPONSIBILITY_CAUSE_SPLIT",
]);

function parseArgs(argv) {
  const options = { input: null, dumpJson: false };
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--input") options.input = path.resolve(argv[++index]);
    else if (argv[index] === "--dump-json") options.dumpJson = true;
    else if (argv[index] === "--help" || argv[index] === "-h") options.help = true;
    else throw new Error(`unknown argument: ${argv[index]}`);
  }
  return options;
}

function validate(contract) {
  const errors = [];
  if (contract.schema_version !== "1.0" || contract.contract_id !== "MENG_V6_TEXT_1") {
    errors.push("TEXT_CONTRACT_IDENTITY_MISMATCH");
  }
  const source = contract.source || {};
  if (Object.entries(EXPECTED_SOURCE).some(([field, expected]) => source[field] !== expected)) {
    errors.push("TEXT_SOURCE_IDENTITY_MISMATCH");
  }
  for (const [pathField, hashField] of [["textbook_path", "textbook_sha256"], ["evidence_dossier_path", "evidence_dossier_sha256"]]) {
    const sourcePath = path.resolve(PROJECT_ROOT, String(source[pathField] || ""));
    let actualHash = null;
    try { actualHash = crypto.createHash("sha256").update(fs.readFileSync(sourcePath)).digest("hex"); } catch (_) { /* handled below */ }
    if (!actualHash || source[hashField] !== actualHash) errors.push("TEXT_SOURCE_HASH_MISMATCH");
  }
  const expectedLines = frozenContract.lines;
  const lines = Array.isArray(contract.lines) ? contract.lines : [];
  let textbookPoemLines = [];
  try {
    const textbook = fs.readFileSync(path.resolve(PROJECT_ROOT, EXPECTED_SOURCE.textbook_path), "utf8");
    const poemSection = textbook.split("## 氓")[1]?.split("离骚")[0] || "";
    textbookPoemLines = poemSection
      .replace(/<sup>[\s\S]*?<\/sup>/g, "")
      .replace(/^\s*《诗经·卫风》\s*/u, "")
      .replace(/汤\s+汤/g, "汤汤")
      .replace(/二三\s+其德/g, "二三其德")
      .replace(/徂\s+尔/g, "徂尔")
      .replace(/渐\s+车/g, "渐车")
      .replace(/总角之宴[^\S\r\n]*，[^\S\r\n]*言笑/g, "总角之宴，言笑")
      .split(/[。！]/)
      .map((item) => item.trim().replace(/\s+/g, ""))
      .filter(Boolean);
  } catch (_) { /* source-hash diagnostic already emitted */ }
  if (JSON.stringify(textbookPoemLines) !== JSON.stringify(lines.map((line) => line.text))) {
    errors.push("TEXTBOOK_EXTRACTION_MISMATCH");
  }
  if (lines.length !== 30 || lines.some((line, index) =>
    !line || line.line_id !== expectedLines[index].line_id || line.chapter_id !== expectedLines[index].chapter_id
      || line.chapter_order !== expectedLines[index].chapter_order
      || line.chapter_line_order !== expectedLines[index].chapter_line_order
      || line.text !== expectedLines[index].text || line.source_ref !== expectedLines[index].source_ref
  )) errors.push("TEXT_LINE_MISMATCH");

  const chapters = Array.isArray(contract.chapters) ? contract.chapters : [];
  if (chapters.length !== 6 || chapters.some((chapter, index) =>
    !chapter || chapter.chapter_id !== `C${index + 1}` || chapter.chapter_order !== index + 1
      || !Array.isArray(chapter.action_chain) || chapter.action_chain.length !== 5
      || JSON.stringify(chapter.line_ids) !== JSON.stringify(expectedLines.slice(index * 5, index * 5 + 5).map((line) => line.line_id))
  )) errors.push("CHAPTER_CONTRACT_INVALID");
  const semanticHash = (value) => crypto.createHash("sha256").update(JSON.stringify(value)).digest("hex");
  if (semanticHash(chapters) !== SEMANTIC_HASHES.chapters) errors.push("CHAPTER_SEMANTICS_MISMATCH");

  const units = Array.isArray(contract.meaning_units) ? contract.meaning_units : [];
  const covered = units.flatMap((unit) => Array.isArray(unit?.line_ids) ? unit.line_ids : []);
  const expectedIds = expectedLines.map((line) => line.line_id);
  const contiguous = units.every((unit) => {
    const numbers = (unit.line_ids || []).map((lineId) => Number(String(lineId).slice(1)));
    return numbers.length > 0 && numbers.every((number, index) => number === numbers[0] + index);
  });
  if (units.length !== 12 || JSON.stringify(covered) !== JSON.stringify(expectedIds)
      || new Set(covered).size !== 30 || !contiguous) errors.push("MEANING_UNIT_COVERAGE_INVALID");
  if (semanticHash(units) !== SEMANTIC_HASHES.meaning_units) errors.push("MEANING_UNIT_SEMANTICS_MISMATCH");

  const boundaries = Array.isArray(contract.interpretive_boundaries) ? contract.interpretive_boundaries : [];
  const ids = boundaries.map((boundary) => boundary?.boundary_id);
  if (REQUIRED_BOUNDARIES.size !== ids.length || [...REQUIRED_BOUNDARIES].some((id) => !ids.includes(id))
      || boundaries.some((boundary) => !Array.isArray(boundary?.evidence_line_ids) || !boundary.evidence_line_ids.length
        || boundary.evidence_line_ids.some((lineId) => !expectedIds.includes(lineId))
        || !Array.isArray(boundary.allowed_claims) || !boundary.allowed_claims.length
        || !Array.isArray(boundary.forbidden_claims) || !boundary.forbidden_claims.length)) {
    errors.push("BOUNDARY_SET_INVALID");
  }
  if (semanticHash(boundaries) !== SEMANTIC_HASHES.interpretive_boundaries) errors.push("BOUNDARY_SEMANTICS_MISMATCH");
  return [...new Set(errors)];
}

function main() {
  const options = parseArgs(process.argv.slice(2));
  if (options.help) {
    process.stdout.write("Usage: node scripts/meng_v6/verify_text.js [--input contract.json] [--dump-json]\n");
    return;
  }
  const contract = options.input ? JSON.parse(fs.readFileSync(options.input, "utf8")) : frozenContract;
  const errors = validate(contract);
  if (errors.length) {
    errors.forEach((code) => process.stderr.write(`${code}\n`));
    process.exitCode = 1;
    return;
  }
  if (options.dumpJson) process.stdout.write(`${JSON.stringify(contract)}\n`);
  else process.stdout.write(`TEXT_CONTRACT_OK lines=${contract.lines.length} units=${contract.meaning_units.length} boundaries=${contract.interpretive_boundaries.length}\n`);
}

if (require.main === module) {
  try { main(); } catch (error) {
    process.stderr.write(`TEXT_CONTRACT_INPUT_ERROR\t${error.message || error}\n`);
    process.exitCode = 2;
  }
}

module.exports = { validate };
