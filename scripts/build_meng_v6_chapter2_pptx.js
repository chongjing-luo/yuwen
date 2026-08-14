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
const PACKAGE = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "chapter_2", "package");
const SNAPSHOT = path.join(PACKAGE, "06_氓_V6第二章课程数据快照.json");
const OUT = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "chapter_2", "pptx");
const PPTX = path.join(OUT, "04_氓_V6第二章课堂课件.pptx");
const MANIFEST = path.join(OUT, "chapter2_pptx_manifest.json");
const W = 13.333, H = 7.5;
const FONT_HEAD = "Noto Serif CJK SC", FONT_BODY = "Noto Sans CJK SC", FONT_TEXT = "Noto Serif CJK SC";
const C = {
  ink: "27231F", ink2: "4B443D", paper: "F6F0E5", paper2: "FFFCF6", warm: "E7DCCB",
  red: "A84A3A", redSoft: "F1DCD5", river: "4E7480", riverSoft: "DCE9EA",
  leaf: "647752", leafSoft: "E1E7D9", gold: "B18B52", goldSoft: "F1E5CE",
  night: "282522", white: "FFFFFF", muted: "766E65", mist: "E9E4DB",
};
const LINES = [
  "乘彼垝垣，以望复关", "不见复关，泣涕涟涟", "既见复关，载笑载言", "尔卜尔筮，体无咎言", "以尔车来，以我贿迁",
];

function sha256(filePath) { return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex"); }
function addText(slide, text, options = {}) { slide.addText(text, { x: 0.72, y: 0.5, w: 11.9, h: 0.5, margin: 0, fontFace: FONT_BODY, fontSize: 28, color: C.ink, valign: "mid", ...options }); }
function rect(slide, pres, x, y, w, h, fill, lineColor = fill, radius = false) { slide.addShape(radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: lineColor, width: 1 }, ...(radius ? { rectRadius: 0.06 } : {}) }); }
function line(slide, pres, x, y, w, h, color, width = 1, dash = "solid") { slide.addShape(pres.shapes.LINE, { x, y, w, h, line: { color, width, dashType: dash, beginArrowType: "none", endArrowType: "none" } }); }
function base(slide, pres, dark = false) { slide.background = { color: dark ? C.night : C.paper }; rect(slide, pres, 0, 0, W, 0.13, dark ? C.gold : C.ink); }
function title(slide, text, options = {}) { addText(slide, text, { x: 0.72, y: 0.38, w: 10.3, h: 0.56, fontFace: FONT_HEAD, fontSize: 32, bold: true, ...options }); addText(slide, "第二章　2 / 6", { x: 10.85, y: 0.48, w: 1.75, h: 0.3, fontSize: 18, bold: true, color: C.red, align: "right" }); }

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

function renderWhole(slide, pres, page) {
  base(slide, pres);
  title(slide, "第二章｜先听见等待怎样起伏");
  rect(slide, pres, 0.78, 1.25, 11.78, 3.48, C.paper2, C.warm, true);
  LINES.forEach((text, index) => addText(slide, `${text}。`, { x: 1.2, y: 1.54 + index * 0.56, w: 10.95, h: 0.36, fontFace: FONT_TEXT, fontSize: 29, bold: index === 0, color: index % 2 ? C.ink2 : C.ink, align: "center" }));
  rect(slide, pres, 0.92, 5.1, 3.52, 1.28, C.riverSoft, C.river, true);
  addText(slide, "读到动作", { x: 1.2, y: 5.31, w: 2.96, h: 0.34, fontSize: 24, bold: true, color: C.river, align: "center" });
  addText(slide, "指尖轻点一下", { x: 1.2, y: 5.79, w: 2.96, h: 0.3, fontSize: 22, color: C.ink2, align: "center" });
  addText(slide, "→", { x: 4.56, y: 5.48, w: 0.48, h: 0.38, fontSize: 27, color: C.gold, align: "center" });
  rect(slide, pres, 5.18, 5.1, 7.18, 1.28, C.goldSoft, C.gold, true);
  addText(slide, "读完，留下三个最确定的动作", { x: 5.48, y: 5.27, w: 6.58, h: 0.32, fontSize: 23, bold: true, color: C.gold, align: "center" });
  [5.55, 7.72, 9.89].forEach((x, index) => {
    rect(slide, pres, x, 5.78, 1.8, 0.4, C.paper2, C.gold, true);
    addText(slide, `${index + 1}　____`, { x: x + 0.12, y: 5.81, w: 1.56, h: 0.3, fontSize: 22, bold: true, color: C.ink2, align: "center" });
  });
  addText(slide, "带着感受的动作也可以写", { x: 4.48, y: 6.62, w: 4.37, h: 0.28, fontSize: 18.5, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderSightline(slide, pres, page) {
  base(slide, pres);
  title(slide, page.title);
  rect(slide, pres, 0.78, 1.2, 11.78, 1.2, C.paper2, C.red, true);
  addText(slide, "乘彼垝垣，以望复关。", { x: 1.1, y: 1.52, w: 11.1, h: 0.5, fontFace: FONT_TEXT, fontSize: 42, bold: true, align: "center" });
  addText(slide, "她站在哪里？目光从哪里出发？望向谁所在的地方？", { x: 1.0, y: 2.76, w: 11.3, h: 0.45, fontFace: FONT_HEAD, fontSize: 28, bold: true, align: "center" });
  rect(slide, pres, 1.06, 3.5, 11.2, 2.45, C.riverSoft, C.river, true);
  const prompts = [
    ["人物站位", "________", C.red, C.redSoft],
    ["视线方向", "____  →  ____", C.river, C.paper2],
    ["这是", "", C.gold, C.goldSoft],
  ];
  prompts.forEach(([head, body, color, fill], index) => {
    const x = 1.38 + index * 3.62;
    rect(slide, pres, x, 4.0, 3.15, 1.28, fill, color, true);
    addText(slide, head, { x: x + 0.2, y: 4.2, w: 2.75, h: 0.3, fontSize: 20, bold: true, color, align: "center" });
    addText(slide, body, { x: x + 0.2, y: 4.66, w: 2.75, h: 0.34, fontSize: 21, bold: true, color: C.ink2, align: "center" });
  });
  addText(slide, "□ 目光", { x: 9.16, y: 4.55, w: 1.28, h: 0.3, fontSize: 20, bold: true, color: C.ink2, align: "center" });
  addText(slide, "□ 行走路线", { x: 10.42, y: 4.55, w: 1.65, h: 0.3, fontSize: 20, bold: true, color: C.ink2, align: "center" });
  addText(slide, "先在纸上画　→　同桌只核对‘乘’和‘望’　→　换笔改图", { x: 2.05, y: 6.18, w: 9.23, h: 0.42, fontSize: 23, bold: true, color: C.river, align: "center" });
  addNotes(slide, page);
}

function renderContrast(slide, pres, page) {
  base(slide, pres);
  title(slide, "不见与既见，两句怎样突然转身");
  const rows = [
    { y: 1.35, fill: C.riverSoft, line: C.river, text: "不见复关，泣涕涟涟。", color: C.river },
    { y: 3.04, fill: C.goldSoft, line: C.gold, text: "既见复关，载笑载言。", color: C.gold },
  ];
  rows.forEach((row) => {
    rect(slide, pres, 0.88, row.y, 11.58, 1.3, row.fill, row.line, true);
    addText(slide, row.text, { x: 1.28, y: row.y + 0.34, w: 10.78, h: 0.55, fontFace: FONT_TEXT, fontSize: 40, bold: true, color: row.color, align: "center" });
  });
  const pairs = ["视线条件", "人物动作", "语势原词"];
  pairs.forEach((label, index) => {
    const x = 1.22 + index * 4.03;
    rect(slide, pres, x, 5.05, 3.45, 1.15, index === 1 ? C.redSoft : C.paper2, index === 1 ? C.red : C.warm, true);
    addText(slide, label, { x: x + 0.22, y: 5.18, w: 3.01, h: 0.28, fontSize: 19, bold: true, color: index === 1 ? C.red : C.ink2, align: "center" });
    addText(slide, "____  ↕  ____", { x: x + 0.22, y: 5.58, w: 3.01, h: 0.34, fontSize: 22, bold: true, color: index === 1 ? C.red : C.ink2, align: "center", altText: "学生填写" });
  });
  addText(slide, "独立填三组　→　同桌只找无原词依据的一格　→　换笔修订", { x: 2.15, y: 6.56, w: 9.03, h: 0.34, fontSize: 21, bold: true, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderScore(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "先把转折写进声音", { color: C.paper });
  addText(slide, "先写朗读谱，再开口", { x: 1.0, y: 1.18, w: 11.3, h: 0.5, fontFace: FONT_HEAD, fontSize: 31, bold: true, color: C.warm, align: "center" });
  rect(slide, pres, 0.92, 1.96, 11.5, 2.08, "35312D", C.gold, true);
  addText(slide, "不见复关，泣涕涟涟。", { x: 1.34, y: 2.28, w: 10.66, h: 0.5, fontFace: FONT_TEXT, fontSize: 36, bold: true, color: C.riverSoft, align: "center" });
  addText(slide, "既见复关，载笑载言。", { x: 1.34, y: 3.17, w: 10.66, h: 0.5, fontFace: FONT_TEXT, fontSize: 36, bold: true, color: C.goldSoft, align: "center" });
  const cards = [
    ["慢下来的一处", C.river, C.riverSoft], ["快起来的一处", C.gold, C.goldSoft], ["重音或停顿", C.red, C.redSoft],
  ];
  cards.forEach(([head, color, fill], index) => {
    const x = 0.92 + index * 4.03;
    rect(slide, pres, x, 4.52, 3.62, 1.4, fill, color, true);
    addText(slide, head, { x: x + 0.2, y: 4.78, w: 3.22, h: 0.34, fontSize: 22, bold: true, color, align: "center" });
    line(slide, pres, x + 0.55, 5.47, 2.52, 0, color, 1.2);
  });
  addText(slide, "为其中一处写下原词理由", { x: 3.5, y: 6.4, w: 6.33, h: 0.4, fontSize: 24, bold: true, color: C.warm, align: "center" });
  addNotes(slide, page);
}

function renderListening(slide, pres, page) {
  base(slide, pres);
  title(slide, "让听者闭眼，只凭声音找转轴");
  addText(slide, "不见复关，泣涕涟涟。　既见复关，载笑载言。", { x: 1.0, y: 1.2, w: 11.3, h: 0.56, fontFace: FONT_TEXT, fontSize: 30, bold: true, color: C.ink, align: "center" });
  const steps = [
    ["1", "读者", "按自己的朗读谱读两句", C.river, C.riverSoft],
    ["2", "听者闭眼", "在哪个原词附近，声音开始变化？", C.gold, C.goldSoft],
    ["3", "读者改一处", "速度｜停顿｜重音，只选一项", C.red, C.redSoft],
    ["4", "第二遍", "更清楚｜仍需调整；待调整者章末再试", C.leaf, C.leafSoft],
  ];
  steps.forEach(([num, head, body, color, fill], index) => {
    const y = 2.04 + index * 1.14;
    rect(slide, pres, 1.14, y, 11.05, 0.86, fill, color, true);
    rect(slide, pres, 1.4, y + 0.16, 0.56, 0.54, color, color, true);
    addText(slide, num, { x: 1.52, y: y + 0.27, w: 0.32, h: 0.28, fontSize: 19, bold: true, color: C.white, align: "center" });
    addText(slide, head, { x: 2.24, y: y + 0.22, w: 2.15, h: 0.38, fontSize: 24, bold: true, color });
    addText(slide, body, { x: 4.42, y: y + 0.22, w: 7.35, h: 0.38, fontSize: 22, color: C.ink2 });
  });
  addText(slide, "再交换角色", { x: 5.02, y: 6.76, w: 3.3, h: 0.3, fontSize: 20, bold: true, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderCulture(slide, pres, page) {
  base(slide, pres);
  title(slide, page.title);
  rect(slide, pres, 0.78, 1.18, 11.78, 1.16, C.paper2, C.red, true);
  addText(slide, "尔卜尔筮，体无咎言。", { x: 1.08, y: 1.48, w: 11.18, h: 0.52, fontFace: FONT_TEXT, fontSize: 42, bold: true, align: "center" });
  const terms = [["卜", "龟板"], ["筮", "蓍草"], ["体", "兆象"], ["无咎言", "没有不祥之语"]];
  terms.forEach(([term, gloss], index) => {
    const x = 0.87 + index * 3.09;
    rect(slide, pres, x, 2.75, 2.75, 1.18, index % 2 ? C.goldSoft : C.riverSoft, index % 2 ? C.gold : C.river, true);
    addText(slide, term, { x: x + 0.2, y: 2.89, w: 2.35, h: 0.39, fontFace: FONT_TEXT, fontSize: term.length > 1 ? 25 : 29, bold: true, color: index % 2 ? C.gold : C.river, align: "center" });
    addText(slide, gloss, { x: x + 0.12, y: 3.39, w: 2.51, h: 0.34, fontSize: gloss.length > 4 ? 22 : 23, bold: true, color: C.ink2, align: "center" });
  });
  rect(slide, pres, 1.18, 4.5, 5.2, 1.38, C.leafSoft, C.leaf, true);
  rect(slide, pres, 6.94, 4.5, 5.2, 1.38, C.redSoft, C.red, true);
  addText(slide, "此次占问告诉他们什么？", { x: 1.54, y: 4.75, w: 4.48, h: 0.4, fontSize: 24, bold: true, color: C.leaf, align: "center" });
  addText(slide, "它不能替后来什么作保证？", { x: 7.3, y: 4.75, w: 4.48, h: 0.4, fontSize: 24, bold: true, color: C.red, align: "center" });
  line(slide, pres, 2.05, 5.48, 3.48, 0, C.leaf, 1.2);
  line(slide, pres, 7.81, 5.48, 3.48, 0, C.red, 1.2);
  addText(slide, "先口译，再把两件事分开", { x: 4.15, y: 6.38, w: 5.03, h: 0.38, fontSize: 22, bold: true, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderParallel(slide, pres, page) {
  base(slide, pres);
  title(slide, page.title);
  rect(slide, pres, 0.78, 1.18, 11.78, 1.16, C.paper2, C.red, true);
  addText(slide, "以尔车来，以我贿迁。", { x: 1.08, y: 1.48, w: 11.18, h: 0.52, fontFace: FONT_TEXT, fontSize: 42, bold: true, align: "center" });
  const cols = [
    { x: 0.95, head: "以尔车来", fill: C.riverSoft, color: C.river, body: "谁来？　带来什么？" },
    { x: 6.89, head: "以我贿迁", fill: C.goldSoft, color: C.gold, body: "谁迁？　带着什么？" },
  ];
  cols.forEach((col) => {
    rect(slide, pres, col.x, 2.78, 5.48, 2.7, col.fill, col.color, true);
    addText(slide, col.head, { x: col.x + 0.35, y: 3.15, w: 4.78, h: 0.55, fontFace: FONT_TEXT, fontSize: 34, bold: true, color: col.color, align: "center" });
    addText(slide, col.body, { x: col.x + 0.35, y: 4.15, w: 4.78, h: 0.4, fontSize: 25, bold: true, color: C.ink2, align: "center" });
    line(slide, pres, col.x + 1.05, 4.87, 3.38, 0, col.color, 1.3);
  });
  addText(slide, "先拆成两人的动作　→　两人对读　→　再合回一句诗", { x: 2.46, y: 6.1, w: 8.41, h: 0.48, fontSize: 25, bold: true, color: C.leaf, align: "center" });
  addNotes(slide, page);
}

function renderRetrieval(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "从章首三步补出七个关键节点", { color: C.paper });
  addText(slide, "写回章首三步｜能对应的圈出｜没有出现的照样保留", { x: 1.0, y: 1.18, w: 11.3, h: 0.46, fontFace: FONT_HEAD, fontSize: 25.5, bold: true, color: C.warm, align: "center" });
  const scrambled = ["迁", "笑言", "望", "卜筮", "泣", "既见", "不见"];
  scrambled.forEach((word, index) => {
    const x = 0.55 + index * 1.78;
    rect(slide, pres, x, 2.02, 1.5, 1.18, index % 2 ? "323C3F" : "3B3530", index % 2 ? C.river : C.gold, true);
    addText(slide, word, { x: x + 0.12, y: 2.25, w: 1.26, h: 0.36, fontFace: FONT_TEXT, fontSize: 24, bold: true, color: index % 2 ? C.riverSoft : C.goldSoft, align: "center" });
    addText(slide, "序号 __", { x: x + 0.27, y: 2.76, w: 0.96, h: 0.24, fontSize: 17.5, color: C.warm, align: "center" });
  });
  rect(slide, pres, 1.28, 3.76, 10.78, 1.38, "343C3E", C.river, true);
  addText(slide, "排序完成后，再找声音转折", { x: 1.65, y: 3.94, w: 4.15, h: 0.38, fontSize: 23, bold: true, color: C.riverSoft, align: "center" });
  addText(slide, "落在第 ____ 与第 ____ 个节点之间", { x: 5.98, y: 3.94, w: 5.05, h: 0.42, fontSize: 23, bold: true, color: C.warm, align: "center" });
  addText(slide, "在自己的七词序列中，圈出这一处；用一道线连住前后两个节点", { x: 2.15, y: 4.55, w: 9.03, h: 0.34, fontSize: 20.5, color: C.riverSoft, align: "center" });
  addText(slide, "同桌只找顺序断点　→　翻诗定位，换笔修订　→　合书连说", { x: 1.75, y: 5.76, w: 9.83, h: 0.48, fontSize: 24, bold: true, color: C.warm, align: "center" });
  addText(slide, "章首三步，现在怎样和七个关键节点接起来？", { x: 2.85, y: 6.42, w: 7.63, h: 0.36, fontSize: 21, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderClose(slide, pres, page) {
  base(slide, pres);
  title(slide, "让第二章从等待走到迁嫁");
  addText(slide, "第二章全文", { x: 0.82, y: 1.08, w: 1.7, h: 0.32, fontSize: 20, bold: true, color: C.red });
  rect(slide, pres, 0.78, 1.48, 11.78, 3.06, C.paper2, C.warm, true);
  LINES.forEach((text, index) => addText(slide, `${text}。`, { x: 1.15, y: 1.78 + index * 0.48, w: 11.0, h: 0.34, fontFace: FONT_TEXT, fontSize: 27, color: C.ink, align: "center" }));
  addText(slide, "重读全章 → 合书讲30秒", { x: 0.96, y: 4.94, w: 3.72, h: 0.44, fontSize: 24, bold: true, color: C.river, align: "center" });
  addText(slide, "她怎样等", { x: 4.85, y: 4.94, w: 2.04, h: 0.42, fontSize: 23, bold: true, color: C.gold, align: "center" });
  addText(slide, "声音怎样转", { x: 7.1, y: 4.94, w: 2.1, h: 0.42, fontSize: 23, bold: true, color: C.leaf, align: "center" });
  addText(slide, "婚事怎样推进", { x: 9.38, y: 4.94, w: 2.46, h: 0.42, fontSize: 23, bold: true, color: C.red, align: "center" });
  rect(slide, pres, 2.18, 5.9, 8.98, 0.68, C.riverSoft, C.river, true);
  addText(slide, "听者找遗漏｜讲述者回诗补说｜写一句章意", { x: 2.52, y: 6.08, w: 8.3, h: 0.31, fontSize: 22, bold: true, color: C.river, align: "center" });
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
  pres.author = "语文备课系统"; pres.title = "《氓》V6第二章课堂课件"; pres.subject = "第二章逐句讲读与双速度朗读"; pres.lang = "zh-CN";
  pres.theme = { headFontFace: FONT_HEAD, bodyFontFace: FONT_BODY, lang: "zh-CN" };
  const renderers = [renderWhole, renderSightline, renderContrast, renderScore, renderListening, renderCulture, renderParallel, renderRetrieval, renderClose];
  snapshot.pages.forEach((page, index) => renderers[index](pres.addSlide(), pres, page));
  validate(pres);
  fs.mkdirSync(OUT, { recursive: true });
  await pres.writeFile({ fileName: PPTX, compression: true });
  await repairNotesMaster(PPTX);
  const manifest = {
    schema_version: "1.0",
    artifact: path.relative(ROOT, PPTX).split(path.sep).join("/"),
    sha256: sha256(PPTX), source_snapshot_sha256: sha256(SNAPSHOT),
    physical_slides: snapshot.pages.map((page, index) => ({ physical_index: index + 1, page_id: page.page_id, primary_visual_duty: page.primary_visual_duty, unique_function: page.unique_function })),
    illustration_policy: "no_character_illustration_before_page_function_freeze",
    claim_boundary: "chapter2_candidate_not_classroom_observed",
  };
  fs.writeFileSync(MANIFEST, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`CHAPTER2_PPTX_OK slides=9 pptx=${PPTX}\n`);
}

main().catch((error) => { console.error(error.stack || error); process.exit(1); });
