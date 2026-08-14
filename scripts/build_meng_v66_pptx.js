#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

function requireGlobal(name) {
  try { return require(name); } catch (_) {
    return require(path.join(process.env.NODE_GLOBAL_ROOT || "/usr/local/node-v22.22.2-linux-x64/lib/node_modules", name));
  }
}

const pptxgen = requireGlobal("pptxgenjs");
const globalRoot = process.env.NODE_GLOBAL_ROOT || "/usr/local/node-v22.22.2-linux-x64/lib/node_modules";
const JSZip = require(path.join(globalRoot, "pptxgenjs", "node_modules", "jszip"));
const lesson = require("./meng_v66/lesson");

const ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v62_stage", "v66", "pptx");
const outputPath = path.join(OUT_DIR, `04_氓_V66逐页功能重构_${lesson.target_pages}状态无插图逐字稿_V5.pptx`);
const manifestPath = path.join(OUT_DIR, "v66_no_image_manifest.json");
const W = 13.333;
const H = 7.5;
const SERIF = "Noto Serif CJK SC";
const SANS = "Noto Sans CJK SC";
const ART_RANDOM_FONT_SIZE = 26;

const C = {
  ink: "29241F", ink2: "51483F", muted: "7B7167", paper: "F5EFE4", paper2: "FFFCF7",
  warm: "DED0BC", warm2: "C5B39B", gold: "A67F4A", gold2: "EFE3CF", river: "446E78",
  river2: "DCE9E8", leaf: "657653", leaf2: "E1E7D9", plum: "725260", plum2: "E9DDE2",
  red: "94473B", red2: "EFDDD5", night: "28231F", night2: "383129", white: "FFFDFC",
  yellow: "B58B3E", yellow2: "F0E4C8",
};

const MODULE = {
  opening: ["初见", C.gold], chapter_1: ["第一章", C.gold], chapter_2: ["第二章", C.river],
  chapter_3: ["第三章", C.leaf], chapter_4: ["第四章", C.yellow], chapter_5: ["第五章", C.plum],
  chapter_6: ["第六章", C.red], synthesis: ["全文", C.ink2],
};

function sha256(filePath) { return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex"); }

function presentation() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: "MENG_V66_WIDE", width: W, height: H });
  pptx.layout = "MENG_V66_WIDE";
  pptx.author = "语文备课系统";
  pptx.subject = `《诗经·卫风·氓》逐页功能重构；${lesson.target_pages}个可审查物理状态；无插图候选`;
  pptx.title = "《氓》V6.6逐页功能重构课堂课件";
  pptx.company = "语文备课系统";
  pptx.lang = "zh-CN";
  pptx.theme = { headFontFace: SERIF, bodyFontFace: SANS, lang: "zh-CN" };
  return pptx;
}

function addText(slide, value, options = {}) {
  slide.addText(value, { x: 0.8, y: 0.5, w: 11.8, h: 0.5, margin: 0, fontFace: SANS, fontSize: 27, color: C.ink, valign: "mid", ...options });
}

function rect(slide, pptx, x, y, w, h, fill, line = fill, rounded = false, width = 1) {
  slide.addShape(rounded ? pptx.shapes.ROUNDED_RECTANGLE : pptx.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: fill }, line: { color: line, width }, ...(rounded ? { rectRadius: 0.04 } : {}),
  });
}

function line(slide, pptx, x, y, w, color, width = 1, dashType = "solid") {
  slide.addShape(pptx.shapes.LINE, { x, y, w, h: 0, line: { color, width, dashType } });
}

function base(slide, pptx, page, state, physicalIndex, options = {}) {
  const [label, accent] = MODULE[page.module] || ["全文", C.ink2];
  const dark = Boolean(options.dark);
  slide.background = { color: dark ? C.night : C.paper };
  rect(slide, pptx, 0, 0, 0.15, H, accent);
  addText(slide, label, { x: 0.47, y: 0.32, w: 1.25, h: 0.28, fontSize: 15.5, bold: true, color: dark ? C.warm : accent });
  addText(slide, String(physicalIndex).padStart(2, "0"), { x: 11.95, y: 0.32, w: 0.7, h: 0.28, fontSize: 14.5, bold: true, color: dark ? C.warm2 : C.muted, align: "right" });
}

function title(slide, value, dark = false, size = 36, align = "left") {
  addText(slide, value, { x: 0.82, y: 0.72, w: 11.7, h: 0.68, fontFace: SERIF, fontSize: size, bold: true, color: dark ? C.white : C.ink, align });
}

function prompt(slide, value, options = {}) {
  addText(slide, value, { x: options.x ?? 1.0, y: options.y ?? 5.92, w: options.w ?? 11.33, h: options.h ?? 0.72, fontFace: SERIF, fontSize: options.fontSize || 28, bold: options.bold ?? true, color: options.color || C.plum, align: options.align || "center", valign: "mid" });
}

function poem(slide, pptx, lines, options = {}) {
  const dark = Boolean(options.dark);
  const x = options.x ?? 0.9, y = options.y ?? 1.5, w = options.w ?? 11.55, h = options.h ?? 4.4;
  rect(slide, pptx, x, y, w, h, dark ? C.night2 : C.paper2, options.border || C.warm2, true, 1.1);
  const count = lines.length || 1;
  const fontSize = options.fontSize || (count <= 2 ? 39 : count <= 4 ? 32 : 27);
  const step = Math.min(0.72, (h - 0.45) / count);
  const startY = y + (h - step * count) / 2;
  lines.forEach((value, index) => addText(slide, value, { x: x + 0.25, y: startY + index * step, w: w - 0.5, h: step * 0.82, fontFace: SERIF, fontSize, color: dark ? C.white : C.ink, align: "center" }));
}

function fullTextFor(page) {
  const map = {
    O05: ["氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。", "送子涉淇，至于顿丘。匪我愆期，子无良媒。", "将子无怒，秋以为期。", "乘彼垝垣，以望复关。不见复关，泣涕涟涟。", "既见复关，载笑载言。尔卜尔筮，体无咎言。", "以尔车来，以我贿迁。", "桑之未落，其叶沃若。于嗟鸠兮，无食桑葚！", "于嗟女兮，无与士耽！士之耽兮，犹可说也。", "女之耽兮，不可说也！"],
    O06: ["桑之落矣，其黄而陨。自我徂尔，三岁食贫。", "淇水汤汤，渐车帷裳。女也不爽，士贰其行。", "士也罔极，二三其德。", "三岁为妇，靡室劳矣。夙兴夜寐，靡有朝矣。", "言既遂矣，至于暴矣。兄弟不知，咥其笑矣。", "静言思之，躬自悼矣。", "及尔偕老，老使我怨。淇则有岸，隰则有泮。", "总角之宴，言笑晏晏。信誓旦旦，不思其反。", "反是不思，亦已焉哉！"],
  };
  return map[page.page_id] || String(page.original_text || "").split(/(?<=[。！？])/u).map((value) => value.trim()).filter(Boolean);
}

function logicalNotes(page) {
  return [
    `【V6.6逻辑页】${page.page_id}｜逻辑页${page.page_number}｜${page.minutes}分钟`,
    "【前页输入】", page.prior_input, "【唯一困难】", page.unique_difficulty, "【唯一功能】", page.unique_function,
    "【文学对象】", page.literary_object, "【信息状态】", page.info_state, "【学生主动作】", page.student_action.join("；"),
    "【参与路径】", page.participation_path, "【可见产物】", page.artifact, "【教师作用】", page.teacher_role,
    "【真实等待】", page.wait_contract, "【反馈与本人修订】", page.feedback_revision, "【首次后用】", page.next_use,
    "【正常反例】", page.normal_counterexample, "【主视觉职责】", page.visual_duty, "【插图资格】", page.illustration_eligibility,
    "【第一人称接收】", page.first_person_reception, "【故事回接】", page.story_return, "【删除损失】", page.deletion_loss,
    "【相邻反证】", page.adjacent_counterproof, "【失败信号】", page.failure_signals.join("；"),
  ].join("\n");
}

function addNotes(slide, page, state) {
  const s = state.script;
  slide.addNotes([
    `【V6.6物理画面】${page.page_id}-${state.state_id}｜${state.seconds}秒`,
    "【本画面为何存在】", state.state_function,
    "【学生此刻看见】", state.frontstage.join("｜"),
    "【教师逐字稿】", s.teacher_spoken,
    "【舞台动作】", ...s.stage_directions.map((item) => `（${item}）`),
    "【本画面时间盒】", s.timeboxes.map((item) => `${item.label}：${item.seconds}秒`).join("；"),
    "【现场分支】", s.branches.map((item) => `${item.kind}：${item.response}`).join("\n"),
    "【听者任务】", s.listener_task,
    "【证据位置】", s.evidence_location,
    "【切页触发】", s.cut_line,
    logicalNotes(page),
    "【声明边界】V5无插图桌面候选；不声称真实课堂或学生掌握已经通过。",
  ].join("\n"));
}

function renderSimpleList(slide, pptx, page, state, physicalIndex) {
  const darkModes = new Set(["single_dark_verse", "sound_space", "ending_boundary", "final_reading", "cause_b0", "cause_b1", "cause_b2"]);
  const dark = darkModes.has(state.render_mode);
  base(slide, pptx, page, state, physicalIndex, { dark });
  const items = state.frontstage.filter(Boolean);
  const head = items[0] || page.title;
  title(slide, head, dark, head.length > 20 ? 31 : 37, page.render_mode === "title" ? "center" : "left");
  const body = items.slice(1);
  if (!body.length) return addNotes(slide, page, state);
  const y0 = 1.7;
  const max = Math.max(1, body.length);
  const step = Math.min(0.92, 4.65 / max);
  body.forEach((value, index) => {
    const isLast = index === body.length - 1;
    addText(slide, value, { x: 1.05, y: y0 + index * step, w: 11.15, h: Math.max(0.48, step * 0.78), fontFace: SERIF, fontSize: body.length > 6 ? 24 : isLast ? 28 : 30, bold: isLast || body.length <= 3, color: dark ? (isLast ? C.gold2 : C.white) : (isLast ? C.plum : C.ink), align: "center", fit: "shrink" });
  });
  addNotes(slide, page, state);
}

function renderMemory(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, state.frontstage[0], false, 38);
  prompt(slide, state.frontstage[1], { y: 1.55, color: C.gold, fontSize: 24 });
  state.frontstage.slice(2, 5).forEach((label, index) => { const y = 2.35 + index * 1.13; addText(slide, label, { x: 1.05, y, w: 3.4, h: 0.45, fontFace: SERIF, fontSize: 24, bold: true, color: index === 2 ? C.plum : C.ink2 }); line(slide, pptx, 4.35, y + 0.4, 7.55, index === 2 ? C.plum2 : C.warm, 1.4); });
  prompt(slide, state.frontstage[5], { y: 6.25, color: C.ink, fontSize: 24 }); addNotes(slide, page, state);
}

function renderSpeak(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex, { dark: true }); title(slide, state.frontstage[0], true, 38);
  addText(slide, state.frontstage[1], { x: 1.0, y: 2.15, w: 11.3, h: 0.85, fontFace: SERIF, fontSize: 34, bold: true, color: C.gold2, align: "center" });
  line(slide, pptx, 1.2, 3.45, 10.9, C.warm2, 1.1); prompt(slide, state.frontstage[2], { y: 4.45, color: C.river2, fontSize: 28 }); addNotes(slide, page, state);
}

function renderTitlePage(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex, { dark: true });
  addText(slide, "氓", { x: 1.5, y: 1.9, w: 10.33, h: 1.5, fontFace: SERIF, fontSize: 80, bold: true, color: C.white, align: "center" });
  addText(slide, "méng", { x: 4.5, y: 3.55, w: 4.33, h: 0.45, fontSize: 22, color: C.gold2, align: "center", charSpacing: 3 });
  addText(slide, "《诗经·卫风》", { x: 3.2, y: 4.6, w: 6.93, h: 0.55, fontFace: SERIF, fontSize: 28, color: C.warm, align: "center" }); addNotes(slide, page, state);
}

function renderCulture(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, state.frontstage[0], false, 34);
  const facts = state.frontstage.slice(1, 5); facts.forEach((value, index) => { const x = 0.82 + index * 3.1; rect(slide, pptx, x, 1.75, 2.72, 1.35, [C.gold2, C.river2, C.leaf2, C.plum2][index], [C.gold, C.river, C.leaf, C.plum][index], true, 1.05); addText(slide, value, { x: x + 0.16, y: 2.11, w: 2.4, h: 0.64, fontFace: SERIF, fontSize: 24, bold: true, color: C.ink, align: "center", fit: "shrink" }); });
  addText(slide, state.frontstage[5], { x: 1.1, y: 3.85, w: 11.1, h: 0.65, fontFace: SERIF, fontSize: 32, bold: true, color: C.plum, align: "center" }); prompt(slide, state.frontstage[6], { y: 5.2, color: C.ink2, fontSize: 25 }); addNotes(slide, page, state);
}

function renderListening(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex, { dark: true }); title(slide, state.frontstage[0] || page.title, true, 31);
  const lines = state.frontstage.length > 1 ? state.frontstage.slice(1) : fullTextFor(page);
  poem(slide, pptx, lines, { dark: true, y: 1.55, h: 4.95, fontSize: lines.length <= 3 ? 31 : 29, border: page.page_id === "O05" ? C.gold : C.plum }); addNotes(slide, page, state);
}

function renderChapterPoem(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, state.frontstage[0] || page.title, false, (state.frontstage[0] || "").length > 19 ? 30 : 34);
  const all = state.frontstage.slice(1);
  const promptIndex = all.findIndex((value) => /^(完整读完|把第)/.test(value));
  const lines = promptIndex >= 0 ? all.slice(0, promptIndex) : (all.length ? all : fullTextFor(page));
  const prompts = promptIndex >= 0 ? all.slice(promptIndex) : [];
  poem(slide, pptx, lines, { y: 1.45, h: prompts.length ? 4.35 : 4.95, fontSize: lines.length > 5 ? 27 : 31, border: MODULE[page.module]?.[1] || C.warm2 });
  if (prompts.length) {
    addText(slide, prompts.join("　"), { x: 1.0, y: 6.05, w: 11.3, h: 0.75, fontFace: SERIF, fontSize: prompts.length > 2 ? 20 : 24, bold: true, color: C.plum, align: "center", fit: "shrink" });
  }
  addNotes(slide, page, state);
}

function renderTwoColumns(slide, pptx, page, state, physicalIndex, dark = false) {
  base(slide, pptx, page, state, physicalIndex, { dark }); const items = state.frontstage; title(slide, items[0], dark, items[0].length > 20 ? 31 : 36);
  const rest = items.slice(1);
  if (rest.length <= 3) {
    const count = Math.max(1, rest.length); const gap = 0.28; const cardW = (11.65 - gap * (count - 1)) / count;
    rest.forEach((value, index) => {
      const x = 0.84 + index * (cardW + gap);
      rect(slide, pptx, x, 1.72, cardW, 4.22, dark ? C.night2 : C.paper2, [C.river, C.plum, C.gold][index], true, 1.1);
      const localSize = count === 3 ? (value.length > 14 ? 22 : value.length > 9 ? 24 : 27) : 30;
      addText(slide, value, { x: x + 0.3, y: 2.22, w: cardW - 0.6, h: 3.1, fontFace: SERIF, fontSize: localSize, bold: true, color: dark ? C.white : C.ink, align: "center", valign: "mid", fit: "shrink" });
    });
  } else {
    const mid = Math.ceil(rest.length / 2); [rest.slice(0, mid), rest.slice(mid)].forEach((col, index) => {
      const x = 0.85 + index * 6.12; rect(slide, pptx, x, 1.55, 5.55, 4.6, dark ? C.night2 : C.paper2, index ? C.plum : C.river, true, 1.1);
      col.forEach((value, j) => addText(slide, value, { x: x + 0.3, y: 1.95 + j * Math.min(1.0, 3.6 / Math.max(col.length, 1)), w: 4.95, h: 0.72, fontFace: SERIF, fontSize: col.length > 4 ? 24 : 28, bold: j === col.length - 1, color: dark ? C.white : C.ink, align: "center", fit: "shrink" }));
    });
  }
  addNotes(slide, page, state);
}

function renderTimeline(slide, pptx, page, state, physicalIndex, completed = false) {
  const dark = completed; base(slide, pptx, page, state, physicalIndex, { dark }); title(slide, state.frontstage[0], dark, 35);
  const labels = completed ? ["相识议婚", "等待迁嫁", "桑叶劝告", "婚后失衡", "劳作孤立", "回望止息"] : ["第一章", "第二章", "第三章", "第四章", "第五章", "第六章"];
  line(slide, pptx, 1.0, 3.55, 11.15, dark ? C.warm2 : C.warm, 1.8);
  labels.forEach((label, index) => { const x = 0.65 + index * 2.1; slide.addShape(pptx.shapes.OVAL, { x, y: 3.05, w: 1.45, h: 1.02, fill: { color: dark ? C.night2 : C.paper2 }, line: { color: [C.gold, C.river, C.leaf, C.yellow, C.plum, C.red][index], width: 1.8 } }); addText(slide, label, { x: x + 0.08, y: 3.35, w: 1.29, h: 0.38, fontFace: SERIF, fontSize: label.length > 3 ? 16 : 18, bold: true, color: dark ? C.white : C.ink, align: "center", fit: "shrink" }); });
  if (state.frontstage[2]) prompt(slide, state.frontstage.slice(2).join("　"), { y: 5.05, color: dark ? C.gold2 : C.plum, fontSize: 24 }); addNotes(slide, page, state);
}

function renderWordGrid(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, state.frontstage[0], false, 34);
  if (state.render_mode === "word_gate_b2") {
    const entries = state.frontstage.slice(1, 7);
    entries.forEach((value, index) => {
      const col = index % 3, row = Math.floor(index / 3);
      const x = 0.86 + col * 4.14, y = 1.72 + row * 1.92;
      rect(slide, pptx, x, y, 3.72, 1.5, C.paper2, [C.gold, C.river, C.leaf, C.yellow, C.plum, C.red][index], true, 1.1);
      addText(slide, value, { x: x + 0.22, y: y + 0.22, w: 3.28, h: 1.05, fontFace: SERIF, fontSize: 20, bold: true, color: C.ink, align: "center", valign: "mid", fit: "shrink" });
    });
    prompt(slide, state.frontstage[7], { y: 5.83, color: C.plum, fontSize: 23 });
    return addNotes(slide, page, state);
  }
  const glyphs = ["愆", "筮", "说", "爽", "咥", "泮"]; glyphs.forEach((g, index) => { const x = 0.8 + index * 2.08; rect(slide, pptx, x, 2.0, 1.72, 1.5, C.paper2, [C.gold, C.river, C.leaf, C.yellow, C.plum, C.red][index], true, 1.1); addText(slide, g, { x, y: 2.35, w: 1.72, h: 0.72, fontFace: SERIF, fontSize: 40, bold: true, color: C.ink, align: "center" }); });
  state.frontstage.slice(2).forEach((value, index) => prompt(slide, value, { y: 4.25 + index * 0.75, color: index ? C.ink2 : C.plum, fontSize: 25 })); addNotes(slide, page, state);
}

function renderRandomCards(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, state.frontstage[0], false, 34);
  const cards = state.frontstage.slice(1, -1);
  const promptText = state.frontstage[state.frontstage.length - 1];
  const cols = cards.length > 6 ? 4 : 3;
  const rows = Math.ceil(cards.length / cols);
  const dense = cards.length > 12;
  const cardW = cards.length > 6 ? 2.72 : 3.55;
  const cardH = dense ? 0.76 : cards.length > 6 ? 0.92 : 1.15;
  const colGap = cards.length > 6 ? 0.25 : 0.58;
  const rowGap = dense ? 0.18 : cards.length > 6 ? 0.32 : 0.42;
  const fullRowW = cols * cardW + (cols - 1) * colGap;
  const positions = [];
  for (let row = 0; row < rows; row += 1) {
    const count = Math.min(cols, cards.length - row * cols);
    const rowW = count * cardW + (count - 1) * colGap;
    const rowX = 0.82 + (fullRowW - rowW) / 2;
    for (let col = 0; col < count; col += 1) {
      positions.push({ x: rowX + col * (cardW + colGap), y: (dense ? 1.62 : 1.68) + row * (cardH + rowGap) });
    }
  }
  cards.forEach((value, index) => {
    // The source order deliberately alternates likely semantic families. Keeping
    // that order on an equal card tray prevents either row or color from
    // becoming a hidden answer key.
    const pos = positions[index];
    rect(slide, pptx, pos.x, pos.y, cardW, cardH, C.paper2, C.warm2, true, 1.05);
    addText(slide, value, { x: pos.x + 0.14, y: pos.y + 0.10, w: cardW - 0.28, h: cardH - 0.20, fontFace: SERIF, fontSize: dense ? ART_RANDOM_FONT_SIZE : cards.length > 6 ? 22 : 24, bold: true, color: C.ink, align: "center", valign: "mid", fit: "shrink" });
  });
  prompt(slide, promptText, { y: dense ? 5.72 : 6.15, fontSize: 23, color: C.plum }); addNotes(slide, page, state);
}

function renderFutureCardOnly(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex);
  title(slide, state.frontstage[0], false, 36);
  rect(slide, pptx, 1.1, 1.62, 11.1, 3.85, C.paper2, C.river, true, 1.2);
  addText(slide, state.frontstage[1], { x: 1.55, y: 2.2, w: 10.2, h: 1.2, fontFace: SERIF, fontSize: 44, color: C.warm2, align: "center" });
  addText(slide, state.frontstage[2], { x: 1.55, y: 4.2, w: 10.2, h: 0.72, fontFace: SERIF, fontSize: 24, color: C.ink2, align: "center", fit: "shrink" });
  prompt(slide, "先让真实的话被听见。", { y: 5.95, fontSize: 26, color: C.plum });
  addNotes(slide, page, state);
}

function renderFutureSummaryOnly(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex);
  title(slide, state.frontstage[0], false, 36);
  const right = [
    { x: 0.9, line: C.gold, head: state.frontstage[1], body: state.frontstage[2] },
    { x: 6.82, line: C.plum, head: state.frontstage[3], body: `${state.frontstage[4]}\n${state.frontstage[5]}` },
  ];
  right.forEach((item) => {
    rect(slide, pptx, item.x, 1.72, 5.62, 4.55, C.paper2, item.line, true, 1.2);
    addText(slide, item.head, { x: item.x + 0.3, y: 2.05, w: 5.02, h: 0.5, fontFace: SERIF, fontSize: 25, bold: true, color: item.line, align: "center" });
    addText(slide, item.body, { x: item.x + 0.38, y: 2.82, w: 4.86, h: 2.75, fontFace: SERIF, fontSize: 24, bold: true, color: C.ink, align: "center", valign: "mid", breakLine: false, fit: "shrink" });
  });
  addNotes(slide, page, state);
}

function renderFirstLineWords(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, state.frontstage[0], false, 34);
  const entries = state.frontstage.slice(1, 7);
  entries.forEach((value, index) => {
    const col = index % 3, row = Math.floor(index / 3);
    const x = 0.86 + col * 4.14, y = 1.68 + row * 1.88;
    rect(slide, pptx, x, y, 3.72, 1.45, C.paper2, [C.gold, C.river, C.leaf, C.yellow, C.plum, C.red][index], true, 1.05);
    addText(slide, value, { x: x + 0.2, y: y + 0.2, w: 3.32, h: 1.03, fontFace: SERIF, fontSize: value.length > 17 ? 19 : 21, bold: true, color: C.ink, align: "center", valign: "mid", fit: "shrink" });
  });
  prompt(slide, state.frontstage[7], { y: 5.72, fontSize: 24, color: C.plum });
  addNotes(slide, page, state);
}

function renderDualTruth(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex);
  title(slide, "旧日与后来，两面都不能抹去", false, 34);
  const items = state.frontstage;
  [[0, 1, C.gold], [2, 3, C.plum]].forEach(([headIndex, textIndex, accent], index) => {
    const x = 0.86 + index * 6.15;
    rect(slide, pptx, x, 1.65, 5.48, 2.65, C.paper2, accent, true, 1.1);
    addText(slide, items[headIndex], { x: x + 0.25, y: 1.95, w: 4.98, h: 0.45, fontFace: SERIF, fontSize: 23, bold: true, color: accent, align: "center" });
    addText(slide, items[textIndex], { x: x + 0.35, y: 2.65, w: 4.78, h: 1.05, fontFace: SERIF, fontSize: 22, bold: true, color: C.ink, align: "center", valign: "mid", fit: "shrink" });
  });
  addText(slide, items[4], { x: 1.1, y: 4.72, w: 11.13, h: 0.58, fontFace: SERIF, fontSize: 29, bold: true, color: C.ink, align: "center" });
  prompt(slide, items[5], { y: 5.65, fontSize: 25, color: C.plum }); addNotes(slide, page, state);
}

function renderBlankRecall(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex, { dark: true });
  const items = state.frontstage;
  title(slide, items[0], true, 39, "center");
  items.slice(1).forEach((value, index) => addText(slide, value, { x: 1.3, y: 2.25 + index * 1.0, w: 10.73, h: 0.62, fontFace: SERIF, fontSize: index === 0 ? 29 : 25, bold: index === 0, color: index === items.length - 2 ? C.gold2 : C.white, align: "center", fit: "shrink" }));
  addNotes(slide, page, state);
}

function renderPersonalAnswer(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, state.frontstage[0], false, 35);
  const items = state.frontstage.slice(1);
  items.forEach((value, index) => {
    const y = 1.62 + index * Math.min(1.02, 4.75 / Math.max(items.length, 1));
    addText(slide, value, { x: 1.0, y, w: 11.25, h: 0.58, fontFace: SERIF, fontSize: items.length > 4 ? 23 : 27, bold: index === 0, color: index === 0 ? C.plum : C.ink, align: "left", fit: "shrink" });
    if (index < items.length - 1) line(slide, pptx, 1.0, y + 0.66, 11.15, C.warm, 0.8);
  });
  addNotes(slide, page, state);
}

function renderCultureAnswer(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, "《诗经》｜把五项事实校准", false, 34);
  state.frontstage.slice(0, 5).forEach((value, index) => {
    const col = index % 3, row = Math.floor(index / 3), x = 0.86 + col * 4.14, y = 1.72 + row * 1.75;
    rect(slide, pptx, x, y, 3.72, 1.35, C.paper2, [C.gold, C.river, C.leaf, C.plum, C.red][index], true, 1.05);
    addText(slide, value, { x: x + 0.2, y: y + 0.24, w: 3.32, h: 0.85, fontFace: SERIF, fontSize: 21, bold: true, color: C.ink, align: "center", valign: "mid", fit: "shrink" });
  });
  prompt(slide, state.frontstage[5], { y: 5.7, fontSize: 24, color: C.plum }); addNotes(slide, page, state);
}

function renderArtMastery(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, state.frontstage[0], false, 34);
  const labels = state.frontstage[1].split("｜");
  labels.forEach((value, index) => {
    const x = 0.88 + index * 3.08;
    rect(slide, pptx, x, 1.85, 2.7, 1.55, C.paper2, [C.gold, C.leaf, C.river, C.plum][index], true, 1.05);
    addText(slide, value, { x: x + 0.2, y: 2.25, w: 2.3, h: 0.65, fontFace: SERIF, fontSize: 22, bold: true, color: C.ink, align: "center", fit: "shrink" });
  });
  addText(slide, state.frontstage[2], { x: 1.1, y: 4.35, w: 11.1, h: 0.5, fontFace: SERIF, fontSize: 27, bold: true, color: C.plum, align: "center" });
  prompt(slide, state.frontstage[3], { y: 5.15, fontSize: 24, color: C.ink }); addNotes(slide, page, state);
}

function renderArtCalibration(slide, pptx, page, state, physicalIndex) {
  base(slide, pptx, page, state, physicalIndex); title(slide, state.frontstage[0], false, 34);
  const entries = state.frontstage.slice(1, 5);
  entries.forEach((value, index) => {
    const col = index % 2, row = Math.floor(index / 2);
    const x = 0.88 + col * 6.1, y = 1.65 + row * 2.05;
    rect(slide, pptx, x, y, 5.48, 1.62, C.paper2, [C.gold, C.leaf, C.river, C.plum][index], true, 1.05);
    addText(slide, value, { x: x + 0.28, y: y + 0.3, w: 4.92, h: 1.02, fontFace: SERIF, fontSize: value.length > 17 ? 22 : 25, bold: true, color: C.ink, align: "center", valign: "mid", fit: "shrink" });
  });
  prompt(slide, state.frontstage[5], { y: 5.95, fontSize: 23, color: C.plum });
  addNotes(slide, page, state);
}

function renderState(slide, pptx, page, state, physicalIndex) {
  switch (state.render_mode) {
    case "memory_sheet": return renderMemory(slide, pptx, page, state, physicalIndex);
    case "speak_entry": return renderSpeak(slide, pptx, page, state, physicalIndex);
    case "title": return renderTitlePage(slide, pptx, page, state, physicalIndex);
    case "culture_map": return renderCulture(slide, pptx, page, state, physicalIndex);
    case "listening": return renderListening(slide, pptx, page, state, physicalIndex);
    case "chapter_poem": case "story_rebuild": case "chapter_three_close": return renderChapterPoem(slide, pptx, page, state, physicalIndex);
    case "see_contrast": case "couplet_contrast": case "leaf_revisit": case "time_compare": case "old_word": case "warning_boundary": case "neutral_cards": case "ending_boundary": case "speech_b0": case "speech_b1": case "speech_b2": case "responsibility_b0": case "responsibility_b1": case "responsibility_b2": case "object_to_person_b1": case "object_to_person_b2": case "life_fact_b0": case "life_fact_b1": case "life_fact_b2": case "cause_b0": case "cause_b1": case "cause_b2": case "future_b0": case "future_b1": case "art_b0": case "art_b1": return renderTwoColumns(slide, pptx, page, state, physicalIndex, state.render_mode.startsWith("cause_") || state.render_mode === "ending_boundary");
    case "future_card_only": return renderFutureCardOnly(slide, pptx, page, state, physicalIndex);
    case "future_summary_only": return renderFutureSummaryOnly(slide, pptx, page, state, physicalIndex);
    case "art_b2": return renderArtCalibration(slide, pptx, page, state, physicalIndex);
    case "life_line_b0": case "life_line_b1": return renderTimeline(slide, pptx, page, state, physicalIndex, false);
    case "life_line_b2": return renderTimeline(slide, pptx, page, state, physicalIndex, true);
    case "word_gate_b0": case "word_gate_b1": case "word_gate_b2": case "word_retrieval": return renderWordGrid(slide, pptx, page, state, physicalIndex);
    case "first_line_words": return renderFirstLineWords(slide, pptx, page, state, physicalIndex);
    case "random_cards": case "art_random": return renderRandomCards(slide, pptx, page, state, physicalIndex);
    case "dual_truth_calibration": return renderDualTruth(slide, pptx, page, state, physicalIndex);
    case "blank_recall": return renderBlankRecall(slide, pptx, page, state, physicalIndex);
    case "personal_answer": return renderPersonalAnswer(slide, pptx, page, state, physicalIndex);
    case "culture_answer": return renderCultureAnswer(slide, pptx, page, state, physicalIndex);
    case "art_mastery": return renderArtMastery(slide, pptx, page, state, physicalIndex);
    default: return renderSimpleList(slide, pptx, page, state, physicalIndex);
  }
}

const physicalPlan = [];
for (const page of lesson.pages) for (const state of page.states) physicalPlan.push({ page, state, physical_number: physicalPlan.length + 1 });

function textFromObject(object) {
  if (!object || object._type === "notes" || object.text === null || object.text === undefined) return "";
  if (typeof object.text === "string") return object.text;
  if (Array.isArray(object.text)) return object.text.map((run) => typeof run === "string" ? run : run?.text || "").join("");
  return "";
}

function visibleTextFor(pageId, stateId = "A") {
  const item = physicalPlan.find((entry) => entry.page.page_id === pageId && entry.state.state_id === stateId);
  if (!item) throw new Error(`missing physical state ${pageId}-${stateId}`);
  const pptx = presentation(); const slide = pptx.addSlide(); renderState(slide, pptx, item.page, item.state, item.physical_number);
  return slide._slideObjects.map(textFromObject).filter(Boolean).join("\n");
}

function validate(pptx) {
  const errors = [];
  if (pptx._slides.length !== lesson.target_pages) errors.push(`slides ${pptx._slides.length}/${lesson.target_pages}`);
  pptx._slides.forEach((slide, slideIndex) => {
    const notesCount = slide._slideObjects.filter((item) => item._type === "notes").length;
    if (notesCount !== 1) errors.push(`slide ${slideIndex + 1} notes ${notesCount}/1`);
    slide._slideObjects.forEach((item, objectIndex) => { const o = item.options || {}; if ([o.x, o.y, o.w, o.h].every((value) => typeof value === "number")) if (o.x < -0.01 || o.y < -0.01 || o.x + o.w > W + 0.01 || o.y + o.h > H + 0.01) errors.push(`slide ${slideIndex + 1} object ${objectIndex + 1} out of bounds`); });
  });
  if (errors.length) throw new Error(errors.join("\n"));
}

async function repairNotesMaster(filePath) {
  const archive = await JSZip.loadAsync(fs.readFileSync(filePath)); const entry = archive.file("ppt/presentation.xml"); let xml = await entry.async("string"); const match = xml.match(/<p:notesMasterIdLst>[\s\S]*?<\/p:notesMasterIdLst>/);
  if (match) { xml = xml.replace(match[0], ""); xml = xml.replace(/(<p:sldMasterIdLst>[\s\S]*?<\/p:sldMasterIdLst>)/, `$1${match[0]}`); }
  archive.file("ppt/presentation.xml", xml); fs.writeFileSync(filePath, await archive.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

async function build() {
  const pptx = presentation(); for (const item of physicalPlan) renderState(pptx.addSlide(), pptx, item.page, item.state, item.physical_number); validate(pptx);
  fs.mkdirSync(OUT_DIR, { recursive: true }); await pptx.writeFile({ fileName: outputPath, compression: true }); await repairNotesMaster(outputPath);
  const manifest = { schema_version: "2.0", version: lesson.version, artifact: path.relative(ROOT, outputPath).split(path.sep).join("/"), sha256: sha256(outputPath), logical_pages: lesson.target_logical_pages, physical_states: lesson.target_pages, total_minutes: lesson.target_natural_minutes, illustrations: 0, states: physicalPlan.map((item) => ({ physical_number: item.physical_number, logical_page: item.page.page_number, page_id: item.page.page_id, state_id: item.state.state_id, seconds: item.state.seconds, render_mode: item.state.render_mode })), claim_boundary: "no_image_physical_candidate_not_independently_released" };
  fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8"); process.stdout.write(`MENG_V66_PPTX_OK physical=${lesson.target_pages} logical=${lesson.target_logical_pages} minutes=${lesson.target_natural_minutes} sha256=${manifest.sha256} output=${outputPath}\n`); return manifest;
}

if (require.main === module) build().catch((error) => { console.error(error); process.exitCode = 1; });
module.exports = { build, physicalPlan, visibleTextFor, outputPath, manifestPath, logicalNotes, ART_RANDOM_FONT_SIZE };
