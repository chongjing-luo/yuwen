"use strict";

/**
 * 导出 canonical lesson.json（设计方案 §10 路线①：lesson.json canonical 化）。
 *
 * 从 meng_v66/lesson.js（含 v65→v62 派生链）一次性烘焙为独立 JSON：
 * - 解开三层 require 链（数据内联，旧模块不再被依赖）；
 * - 补齐 lesson_schema v1.0 顶层字段（text_contract / knowledge_refs / kp_scope /
 *   relations / claim_boundary），text_contract 直接取 meng_v6/text.js 冻结契约
 *   （同一 SHA，不二次转录）。
 *
 * 同源纪律（P-11）：导出后 lesson.json 为唯一数据源；scripts/meng_v66/lesson.js
 * 变为读 JSON 的加载器。本脚本仅在重建 JSON 骨架时使用（重建会丢弃对 JSON 的
 * 人工改写——样板清零等编辑直接改 lesson.json，不要重跑本脚本覆盖）。
 */
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const ROOT = path.resolve(__dirname, "../..");
// 一次性骨架工具：元数据冻结自 V5 候选（lesson.js 已改为 JSON 加载器，不再可require原模块）
const lesson = { pages: JSON.parse(require("fs").readSync(require("path").join(__dirname, "..", "..", "work", "teaching", "选择性必修下册", "氓", "lesson.json"))).pages,
  three_questions: JSON.parse(require("fs").readSync(require("path").join(__dirname, "..", "..", "work", "teaching", "选择性必修下册", "氓", "lesson.json"))).three_questions,
  version: "6.6-v5-p2-closure-candidate", status: "pre_review_candidate",
  target_pages: 81, target_logical_pages: 46, target_natural_minutes: 280 };
const textContract = require("../meng_v6/text").contract;

const OUT = path.join(ROOT, "work/teaching/选择性必修下册/氓/lesson.json");

const canonicalLines = (textContract.lines || []).map((line) =>
  typeof line === "string" ? line : line.text || line.line || String(line)
);

const enriched = {
  schema_version: "1.0",
  lesson_id: "LES-X3-MENG-01",
  lesson_title: "《氓》",
  book_unit: { card_refs: ["CARD-X3-U01-01"], unit_ref: "UNIT-X3-U01" },
  text_contract: {
    source_path: textContract.source.textbook_path,
    source_sha256: textContract.source.textbook_sha256,
    canonical_lines: canonicalLines,
    interpretation_boundaries: textContract.interpretive_boundaries || [],
    evidence_dossier: textContract.source.evidence_dossier_path,
  },
  three_questions: lesson.three_questions,
  kp_scope: {
    kp_ids: [
      "KP-CARD-X3-U01-01-003",
      "KP-CARD-X3-U01-01-004",
      "KP-CARD-X3-U01-01-005",
      "KP-CARD-X3-U01-01-006",
    ],
    deferred: [
      { kp_id: "KP-CARD-X3-U01-01-001", reason: "证据边界为研究元规则，不作课堂 KP 考查" },
      { kp_id: "KP-CARD-X3-U01-01-002", reason: "导语源流定位在《离骚》连排后的单元收束课回收" },
      { kp_id: "KP-CARD-X3-U01-01-007", reason: "《离骚》身世链属同卡下一课" },
      { kp_id: "KP-CARD-X3-U01-01-008", reason: "香草意象属《离骚》课" },
      { kp_id: "KP-CARD-X3-U01-01-009", reason: "哀民生句属《离骚》课" },
      { kp_id: "KP-CARD-X3-U01-01-010", reason: "遭谗与不改其志属《离骚》课" },
      { kp_id: "KP-CARD-X3-U01-01-011", reason: "退守与修德属《离骚》课" },
    ],
  },
  relations: [
    { card_id: "CARD-B1-REC-01", relation: "同出《诗经》：静女（邶风）之爱情开端与氓（卫风）之婚姻回望对照" },
  ],
  pages: lesson.pages,
  version: lesson.version,
  status: lesson.status,
  target_pages: lesson.target_pages,
  target_logical_pages: lesson.target_logical_pages,
  target_natural_minutes: lesson.target_natural_minutes,
  illustration_policy: lesson.illustration_policy,
  legacy_meta: {
    derived_from: "scripts/meng_v66/lesson.js（V5 候选，含 v65/v62 派生链，已内联）",
    exported_at: new Date().toISOString(),
  },
  claim_boundary: "桌面设计；课堂效果待真实试教（P-12，两本账纪律）",
};

fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(enriched, null, 2), "utf-8");
const sha = crypto.createHash("sha256").update(fs.readFileSync(OUT)).digest("hex");
console.log(`lesson.json → ${OUT}`);
console.log(`pages=${enriched.pages.length} states=${enriched.pages.reduce((n, p) => n + (p.states ? p.states.length : 0), 0)} minutes=${enriched.pages.reduce((n, p) => n + p.minutes, 0)} sha256=${sha.slice(0, 16)}…`);
