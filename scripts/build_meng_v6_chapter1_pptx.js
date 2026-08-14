#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

function requireGlobal(name) {
  try { return require(name); }
  catch (_) { return require(path.join("/usr/local/node-v22.22.2-linux-x64/lib/node_modules", name)); }
}

const pptxgen = requireGlobal("pptxgenjs");
const JSZip = require(path.join("/usr/local/node-v22.22.2-linux-x64/lib/node_modules", "pptxgenjs", "node_modules", "jszip"));
const ROOT = path.resolve(__dirname, "..");
const PACKAGE = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "chapter_1", "package");
const SNAPSHOT = path.join(PACKAGE, "06_氓_V6第一章课程数据快照.json");
const OUT = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "chapter_1", "pptx");
const PPTX = path.join(OUT, "04_氓_V6第一章课堂课件.pptx");
const MANIFEST = path.join(OUT, "chapter1_pptx_manifest.json");
const W = 13.333, H = 7.5;
const FONT_HEAD = "Noto Serif CJK SC", FONT_BODY = "Noto Sans CJK SC", FONT_TEXT = "Noto Serif CJK SC";
const C = { ink: "27231F", ink2: "4B443D", paper: "F6F0E5", paper2: "FFFCF6", warm: "E7DCCB", red: "A84A3A", redSoft: "F1DCD5", river: "4E7480", riverSoft: "DCE9EA", leaf: "647752", leafSoft: "E1E7D9", gold: "B18B52", night: "282522", white: "FFFFFF", muted: "766E65" };
const LINES = [
  "氓之蚩蚩，抱布贸丝", "匪来贸丝，来即我谋", "送子涉淇，至于顿丘", "匪我愆期，子无良媒", "将子无怒，秋以为期",
];

function sha256(filePath) { return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex"); }
function addText(slide, text, options = {}) { slide.addText(text, { x: 0.72, y: 0.5, w: 11.9, h: 0.5, margin: 0, fontFace: FONT_BODY, fontSize: 28, color: C.ink, valign: "mid", ...options }); }
function rect(slide, pres, x, y, w, h, fill, lineColor = fill, radius = false) { slide.addShape(radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: lineColor, width: 1 }, ...(radius ? { rectRadius: 0.06 } : {}) }); }
function line(slide, pres, x, y, w, color, width = 1) { slide.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width } }); }
function base(slide, pres, dark = false) { slide.background = { color: dark ? C.night : C.paper }; rect(slide, pres, 0, 0, W, 0.13, dark ? C.gold : C.ink); }
function title(slide, text, options = {}) { addText(slide, text, { x: 0.72, y: 0.38, w: 10.3, h: 0.56, fontFace: FONT_HEAD, fontSize: 32, bold: true, ...options }); addText(slide, "第一章　1 / 6", { x: 10.85, y: 0.48, w: 1.75, h: 0.3, fontSize: 18, bold: true, color: C.red, align: "right" }); }

function notesFor(page) {
  const script = page.script;
  return [
    `【V6页ID】${page.page_id}｜${page.title}｜${page.minutes}分钟`,
    "【教师逐字稿】", script.teacher_spoken,
    "【场面与走位】", script.scene, ...script.stage_directions.map((item) => `（${item}）`),
    "【时间盒】", script.timeboxes.map((item) => `${item.label}：${item.seconds}秒`).join("；"),
    "【现场分支】", script.branches.map((item) => `${item.kind}：${item.response}`).join("\n"),
    "【听者同步任务】", script.listener_task,
    "【证据位置】", script.evidence_location,
    "【自然切页句】", script.cut_line,
    "【声明边界】桌面排演稿；不声称真实学生已经理解、参与或学会。",
  ].join("\n");
}

function addNotes(slide, page) { slide.addNotes(notesFor(page)); }

function chapterTrack(slide, pres, currentIndex) {
  const y = 5.38;
  addText(slide, "第一章原文轨道", { x: 0.78, y: y - 0.38, w: 2.1, h: 0.28, fontSize: 17.5, bold: true, color: C.muted });
  LINES.forEach((text, index) => {
    const itemY = y + index * 0.37;
    if (index === currentIndex) rect(slide, pres, 0.74, itemY - 0.03, 11.86, 0.34, C.redSoft, C.red, true);
    addText(slide, text, { x: 1.02, y: itemY, w: 11.15, h: 0.25, fontFace: FONT_TEXT, fontSize: 22, bold: index === currentIndex, color: index === currentIndex ? C.red : C.ink2 });
  });
}

function renderWhole(slide, pres, page) {
  base(slide, pres);
  title(slide, "第一章｜先看两个人怎样行动");
  rect(slide, pres, 0.78, 1.25, 11.78, 3.62, C.paper2, C.warm, true);
  LINES.forEach((text, index) => addText(slide, `${text}。`, { x: 1.2, y: 1.57 + index * 0.59, w: 10.95, h: 0.37, fontFace: FONT_TEXT, fontSize: 29, bold: index === 0, color: index % 2 ? C.ink2 : C.ink, align: "center" }));
  rect(slide, pres, 1.58, 5.38, 10.18, 0.82, C.riverSoft, C.river, true);
  addText(slide, "圈男子动作｜划女子动作｜同桌只问：这是谁做的？", { x: 1.98, y: 5.61, w: 9.38, h: 0.34, fontSize: 25, bold: true, color: C.river, align: "center" });
  addText(slide, "暂时只追踪“谁做了什么”", { x: 4.12, y: 6.55, w: 5.1, h: 0.28, fontSize: 19, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function linePrompt(page) {
  const lineId = page.source_line_refs[0];
  return {
    L001: ["谁，以怎样的样子，拿什么来做什么？", "先说自然话｜再借注释校准｜换笔改一处"],
    L002: ["先看诗句写什么，再圈出让意思转过来的字", "诗句先写的动作：________　｜　女子随后说明的来意：________"],
    L003: ["沿三个动作画一条送行路线", "送　→　涉　→　至　｜　是谁在送？送到哪里？"],
    L004: ["她在解释什么？", "婚期没有立刻定下，是因为________________"],
    L005: ["一句话里同时有哪两层话？", "第一层：________　｜　第二层：________　｜　再标重音和停顿"],
  }[lineId];
}

function renderLine(slide, pres, page, currentIndex) {
  base(slide, pres);
  title(slide, page.title);
  rect(slide, pres, 0.78, 1.18, 11.78, 1.25, C.paper2, C.red, true);
  addText(slide, `${page.original_text}。`, { x: 1.08, y: 1.5, w: 11.18, h: 0.58, fontFace: FONT_TEXT, fontSize: 42, bold: true, align: "center" });
  const lineId = page.source_line_refs[0];
  const [question, action] = linePrompt(page);
  if (lineId === "L001") {
    addText(slide, "先看眼前这个出场", { x: 1.0, y: 2.72, w: 11.3, h: 0.5, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: C.ink, align: "center" });
    const slots = [["谁", C.river, C.riverSoft], ["怎样", C.gold, C.warm], ["拿什么", C.leaf, C.leafSoft], ["做什么", C.red, C.redSoft]];
    slots.forEach(([label, color, fill], index) => {
      const x = 1.02 + index * 2.91;
      rect(slide, pres, x, 3.38, 2.55, 0.9, fill, color, true);
      addText(slide, label, { x: x + 0.2, y: 3.52, w: 2.15, h: 0.3, fontFace: FONT_HEAD, fontSize: 22, bold: true, color, align: "center" });
      line(slide, pres, x + 0.56, 4.02, 1.43, color, 1.1);
    });
    addText(slide, "把四格说成一句自然话｜只写眼前，不忙替后来下结论", { x: 1.42, y: 4.56, w: 10.5, h: 0.32, fontSize: 20.5, bold: true, color: C.ink2, align: "center" });
  } else if (lineId === "L004") {
    addText(slide, "两种读法，哪一种更贴近原句？", { x: 1.0, y: 2.68, w: 11.3, h: 0.5, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: C.ink, align: "center" });
    const readings = [["她在拒绝这门婚事？", C.red, C.redSoft], ["她在说明此刻不能成婚的条件？", C.leaf, C.leafSoft]];
    readings.forEach(([label, color, fill], index) => {
      const x = 1.0 + index * 5.82;
      rect(slide, pres, x, 3.36, 5.48, 0.92, fill, color, true);
      addText(slide, label, { x: x + 0.28, y: 3.61, w: 4.92, h: 0.34, fontFace: FONT_HEAD, fontSize: 22, bold: true, color, align: "center" });
    });
    addText(slide, "先圈一项，再抄下托住判断的原词：________________", { x: 1.36, y: 4.55, w: 10.62, h: 0.34, fontSize: 21, bold: true, color: C.river, align: "center" });
  } else {
    addText(slide, question, { x: 1.0, y: 2.82, w: 11.3, h: 0.58, fontFace: FONT_HEAD, fontSize: 29, bold: true, color: C.ink, align: "center" });
    rect(slide, pres, 1.32, 3.65, 10.7, 0.94, currentIndex % 2 ? C.leafSoft : C.riverSoft, currentIndex % 2 ? C.leaf : C.river, true);
  }
  if (lineId === "L005") {
    const color = currentIndex % 2 ? C.leaf : C.river;
    addText(slide, "她先在劝什么：________", { x: 1.62, y: 3.91, w: 3.2, h: 0.38, fontSize: 21, bold: true, color, align: "center" });
    addText(slide, "她又把什么定下来：________", { x: 4.95, y: 3.91, w: 3.55, h: 0.38, fontSize: 21, bold: true, color, align: "center" });
    addText(slide, "再标重音和停顿", { x: 8.37, y: 3.91, w: 2.72, h: 0.38, fontSize: 21.5, bold: true, color, align: "center" });
  } else if (!['L001', 'L004'].includes(lineId)) {
    addText(slide, action, { x: 1.72, y: 3.91, w: 9.9, h: 0.38, fontSize: 23, bold: true, color: currentIndex % 2 ? C.leaf : C.river, align: "center" });
  }
  chapterTrack(slide, pres, currentIndex);
  addNotes(slide, page);
}

function renderRetrieval(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "合上书，把这场相遇接起来", { color: C.paper });
  addText(slide, "独立写五步，只写人物和动作", { x: 1.1, y: 1.27, w: 11.1, h: 0.5, fontFace: FONT_HEAD, fontSize: 31, bold: true, color: C.warm, align: "center" });
  ["1", "2", "3", "4", "5"].forEach((label, index) => {
    const x = 0.86 + index * 2.48;
    rect(slide, pres, x, 2.28, 2.12, 2.05, index % 2 ? "323C3F" : "37322D", index % 2 ? C.river : C.gold, true);
    addText(slide, label, { x: x + 0.72, y: 2.65, w: 0.68, h: 0.45, fontSize: 27, bold: true, color: index % 2 ? C.riverSoft : C.warm, align: "center" });
    line(slide, pres, x + 0.42, 3.46, 1.28, index % 2 ? C.river : C.gold, 1.2);
  });
  addText(slide, "同桌只找断点，不报答案", { x: 1.1, y: 5.04, w: 5.2, h: 0.43, fontSize: 25, bold: true, color: C.warm, align: "center" });
  addText(slide, "→", { x: 6.27, y: 5.05, w: 0.72, h: 0.38, fontSize: 26, color: C.gold, align: "center" });
  addText(slide, "翻书定位，换笔修订，再合书连说", { x: 7.0, y: 5.04, w: 5.2, h: 0.43, fontSize: 24, bold: true, color: C.riverSoft, align: "center" });
  addNotes(slide, page);
}

function renderDossier(slide, pres, page) {
  base(slide, pres);
  title(slide, "只读第一章，你怎样看这次接近？");
  addText(slide, "每栏写一条；给前两栏各补一个第一章原词", { x: 1.1, y: 1.22, w: 11.1, h: 0.38, fontSize: 22, bold: true, color: C.red, align: "center" });
  const cols = [["诗里写着", C.river, C.riverSoft], ["初读时我觉得", "8A6A34", "F0E6D3"], ["现在还说不准", C.red, C.redSoft]];
  cols.forEach(([head, color, fill], index) => {
    const x = 0.78 + index * 4.17;
    rect(slide, pres, x, 1.86, 3.75, 3.4, fill, color, true);
    addText(slide, head, { x: x + 0.25, y: 2.24, w: 3.25, h: 0.5, fontFace: FONT_HEAD, fontSize: 28, bold: true, color, align: "center" });
    line(slide, pres, x + 0.58, 3.02, 2.59, color, 1.2);
    addText(slide, index < 2 ? "原词：____________" : "先留一句：________", { x: x + 0.48, y: 4.46, w: 2.79, h: 0.32, fontSize: 20, color: C.ink2, align: "center" });
  });
  addText(slide, "同桌问一句：这是诗里写着的，还是我此刻的感觉？", { x: 2.25, y: 5.65, w: 8.83, h: 0.44, fontSize: 24, bold: true, color: C.leaf, align: "center" });
  addText(slide, "我再决定：保留｜说轻一点｜移栏", { x: 3.42, y: 6.1, w: 6.5, h: 0.38, fontSize: 22, bold: true, color: C.ink2, align: "center" });
  addText(slide, "全文读完后，我们再回来", { x: 4.26, y: 6.62, w: 4.82, h: 0.3, fontSize: 19, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderClose(slide, pres, page) {
  base(slide, pres);
  title(slide, "让第一章重新成为一段话");
  addText(slide, "第一章全文", { x: 0.82, y: 1.12, w: 1.7, h: 0.32, fontSize: 20, bold: true, color: C.red });
  rect(slide, pres, 0.78, 1.48, 7.55, 4.7, C.paper2, C.warm, true);
  LINES.forEach((text, index) => addText(slide, `${text}。`, { x: 1.08, y: 1.88 + index * 0.73, w: 6.95, h: 0.42, fontFace: FONT_TEXT, fontSize: 31, color: C.ink, align: "center" }));
  addText(slide, "完整重读", { x: 8.82, y: 1.72, w: 3.75, h: 0.48, fontFace: FONT_HEAD, fontSize: 30, bold: true, color: C.river, align: "center" });
  addText(slide, "↓", { x: 10.25, y: 2.3, w: 0.9, h: 0.38, fontSize: 26, color: C.gold, align: "center" });
  addText(slide, "合书讲30秒", { x: 8.82, y: 2.75, w: 3.75, h: 0.48, fontFace: FONT_HEAD, fontSize: 29, bold: true, color: C.red, align: "center" });
  const retellItems = [["男子怎样来", C.gold], ["女子怎样回应", C.leaf], ["婚期怎样定", C.red]];
  retellItems.forEach(([text, color], index) => {
    addText(slide, `${index + 1}`, { x: 8.9, y: 3.67 + index * 0.64, w: 0.48, h: 0.3, fontSize: 20, bold: true, color, align: "center" });
    addText(slide, text, { x: 9.52, y: 3.6 + index * 0.64, w: 2.62, h: 0.38, fontSize: 23, bold: true, color: C.ink2 });
  });
  rect(slide, pres, 1.58, 6.48, 10.18, 0.6, C.riverSoft, C.river, true);
  addText(slide, "听者找遗漏｜回诗补说｜写一句章意", { x: 2.05, y: 6.63, w: 9.24, h: 0.3, fontSize: 22, bold: true, color: C.river, align: "center" });
  addNotes(slide, page);
}

function validate(pres) {
  const errors = [];
  if (pres._slides.length !== 9) errors.push(`slides=${pres._slides.length}`);
  pres._slides.forEach((slide, slideIndex) => {
    if (!slide._slideObjects.some((item) => item._type === "notes")) errors.push(`slide ${slideIndex + 1} missing notes`);
    slide._slideObjects.forEach((object, objectIndex) => {
      const o = object.options || {};
      if ([o.x, o.y, o.w, o.h].every((value) => typeof value === "number") && (o.x < 0 || o.y < 0 || o.x + o.w > W + 0.01 || o.y + o.h > H + 0.01)) errors.push(`slide ${slideIndex + 1} object ${objectIndex + 1} out of bounds`);
    });
  });
  if (errors.length) throw new Error(errors.join("\n"));
}

async function repairNotesMaster(fileName) {
  const zip = await JSZip.loadAsync(fs.readFileSync(fileName));
  const entry = zip.file("ppt/presentation.xml");
  if (!entry) throw new Error("missing ppt/presentation.xml");
  let xml = await entry.async("string");
  const notesMaster = xml.match(/<p:notesMasterIdLst>[\s\S]*?<\/p:notesMasterIdLst>/);
  if (notesMaster) {
    xml = xml.replace(notesMaster[0], "");
    xml = xml.replace(/(<p:sldMasterIdLst>[\s\S]*?<\/p:sldMasterIdLst>)/, `$1${notesMaster[0]}`);
  }
  zip.file("ppt/presentation.xml", xml);
  fs.writeFileSync(fileName, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

async function main() {
  const snapshot = JSON.parse(fs.readFileSync(SNAPSHOT, "utf8"));
  const pres = new pptxgen();
  pres.defineLayout({ name: "MENG_WIDE", width: W, height: H }); pres.layout = "MENG_WIDE";
  pres.author = "语文备课系统"; pres.title = "《氓》V6第一章课堂课件"; pres.subject = "第一章逐句讲读"; pres.lang = "zh-CN";
  pres.theme = { headFontFace: FONT_HEAD, bodyFontFace: FONT_BODY, lang: "zh-CN" };
  const renderers = [renderWhole, ...[0, 1, 2, 3, 4].map((index) => (slide, p, page) => renderLine(slide, p, page, index)), renderRetrieval, renderDossier, renderClose];
  snapshot.pages.forEach((page, index) => renderers[index](pres.addSlide(), pres, page));
  validate(pres);
  fs.mkdirSync(OUT, { recursive: true });
  await pres.writeFile({ fileName: PPTX, compression: true });
  await repairNotesMaster(PPTX);
  const manifest = { schema_version: "1.0", artifact: path.relative(ROOT, PPTX).split(path.sep).join("/"), sha256: sha256(PPTX), source_snapshot_sha256: sha256(SNAPSHOT), physical_slides: snapshot.pages.map((page, index) => ({ physical_index: index + 1, page_id: page.page_id, primary_visual_duty: page.primary_visual_duty, unique_function: page.unique_function })), illustration_policy: "no_character_illustration_before_page_function_freeze", claim_boundary: "chapter1_candidate_not_classroom_observed" };
  fs.writeFileSync(MANIFEST, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`CHAPTER1_PPTX_OK slides=9 pptx=${PPTX}\n`);
}

main().catch((error) => { console.error(error.stack || error); process.exit(1); });
