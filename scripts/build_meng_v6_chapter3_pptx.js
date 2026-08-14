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
const PACKAGE = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "chapter_3", "package");
const SNAPSHOT = path.join(PACKAGE, "06_氓_V6第三章课程数据快照.json");
const OUT = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage", "chapter_3", "pptx");
const PPTX = path.join(OUT, "04_氓_V6第三章课堂课件.pptx");
const MANIFEST = path.join(OUT, "chapter3_pptx_manifest.json");
const W = 13.333, H = 7.5;
const FONT_HEAD = "Noto Serif CJK SC", FONT_BODY = "Noto Sans CJK SC", FONT_TEXT = "Noto Serif CJK SC";
const C = {
  ink: "27231F", ink2: "4B443D", paper: "F6F0E5", paper2: "FFFCF6", warm: "E7DCCB",
  red: "A84A3A", redSoft: "F1DCD5", river: "4E7480", riverSoft: "DCE9EA",
  leaf: "647752", leaf2: "7B925E", leafSoft: "E1E7D9", gold: "B18B52", goldSoft: "F1E5CE",
  night: "282522", white: "FFFFFF", muted: "766E65", mist: "E9E4DB", plum: "75515E", plumSoft: "EADDE1",
};
const LINES = [
  "桑之未落，其叶沃若。",
  "于嗟鸠兮，无食桑葚！",
  "于嗟女兮，无与士耽！",
  "士之耽兮，犹可说也。",
  "女之耽兮，不可说也！",
];

function sha256(filePath) { return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex"); }
function addText(slide, text, options = {}) { slide.addText(text, { x: 0.72, y: 0.5, w: 11.9, h: 0.5, margin: 0, fontFace: FONT_BODY, fontSize: 28, color: C.ink, valign: "mid", ...options }); }
function rect(slide, pres, x, y, w, h, fill, lineColor = fill, radius = false) { slide.addShape(radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, { x, y, w, h, fill: { color: fill }, line: { color: lineColor, width: 1 }, ...(radius ? { rectRadius: 0.06 } : {}) }); }
function line(slide, pres, x, y, w, h, color, width = 1, dash = "solid") { slide.addShape(pres.shapes.LINE, { x, y, w, h, line: { color, width, dashType: dash, beginArrowType: "none", endArrowType: "none" } }); }
function base(slide, pres, dark = false) { slide.background = { color: dark ? C.night : C.paper }; rect(slide, pres, 0, 0, W, 0.13, dark ? C.leaf2 : C.ink); }
function title(slide, text, options = {}) { addText(slide, text, { x: 0.72, y: 0.38, w: 10.3, h: 0.56, fontFace: FONT_HEAD, fontSize: 32, bold: true, ...options }); addText(slide, "第三章　3 / 6", { x: 10.85, y: 0.48, w: 1.75, h: 0.3, fontSize: 18, bold: true, color: C.red, align: "right" }); }

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

function renderOpening(slide, pres, page) {
  base(slide, pres);
  title(slide, "第三章｜迁嫁之后，诗接着写了什么");
  addText(slide, "故事走到这里", { x: 0.9, y: 1.1, w: 2.2, h: 0.35, fontSize: 21, bold: true, color: C.red });
  const rail = [
    ["初见议婚", C.riverSoft, C.river], ["等待迁嫁", C.goldSoft, C.gold], ["________", C.leafSoft, C.leaf],
  ];
  rail.forEach(([label, fill, color], index) => {
    const x = 1.0 + index * 3.96;
    rect(slide, pres, x, 1.55, 3.15, 0.75, fill, color, true);
    addText(slide, label, { x: x + 0.2, y: 1.76, w: 2.75, h: 0.3, fontSize: 23, bold: true, color, align: "center" });
    if (index < 2) addText(slide, "→", { x: x + 3.28, y: 1.72, w: 0.45, h: 0.34, fontSize: 26, color: C.muted, align: "center" });
  });
  rect(slide, pres, 0.82, 2.7, 11.7, 2.92, C.paper2, C.warm, true);
  LINES.forEach((text, index) => addText(slide, text, { x: 1.15, y: 3.02 + index * 0.48, w: 11.0, h: 0.34, fontFace: FONT_TEXT, fontSize: 27.5, color: index < 1 ? C.leaf : C.ink, bold: index === 0, align: "center" }));
  addText(slide, "感觉说话方式有变化时，自己轻停", { x: 1.0, y: 5.92, w: 4.85, h: 0.36, fontSize: 22, bold: true, color: C.leaf, align: "center" });
  addText(slide, "最先看见 ____　先劝 ____　后来劝 ____", { x: 5.58, y: 5.92, w: 6.7, h: 0.36, fontSize: 22, bold: true, color: C.plum, align: "center" });
  addText(slide, "读完再落笔｜每一处回答都请抄回一个原词", { x: 3.4, y: 6.62, w: 6.55, h: 0.3, fontFace: FONT_HEAD, fontSize: 19.5, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderMulberry(slide, pres, page) {
  base(slide, pres);
  title(slide, "桑之未落，其叶沃若");
  rect(slide, pres, 0.82, 1.18, 11.7, 1.12, C.leafSoft, C.leaf, true);
  addText(slide, "桑之未落，其叶沃若。", { x: 1.1, y: 1.48, w: 11.14, h: 0.5, fontFace: FONT_TEXT, fontSize: 42, bold: true, color: C.leaf, align: "center" });
  addText(slide, "沃若：润泽的样子", { x: 4.4, y: 2.55, w: 4.55, h: 0.35, fontSize: 23, bold: true, color: C.ink2, align: "center" });
  addText(slide, "一片‘沃若’的桑叶，唤起了怎样的感觉？", { x: 3.15, y: 3.08, w: 7.05, h: 0.38, fontFace: FONT_HEAD, fontSize: 27, bold: true, color: C.red, align: "center" });
  rect(slide, pres, 0.95, 3.68, 3.25, 2.12, C.paper2, C.warm, true);
  addText(slide, "色泽・质地・生命感", { x: 1.18, y: 3.96, w: 2.79, h: 0.35, fontSize: 19.5, bold: true, color: C.ink2, align: "center" });
  addText(slide, "________", { x: 1.35, y: 4.63, w: 1.05, h: 0.3, fontSize: 22, color: C.leaf, align: "center" });
  addText(slide, "／", { x: 2.45, y: 4.63, w: 0.32, h: 0.3, fontSize: 22, color: C.muted, align: "center" });
  addText(slide, "________", { x: 2.82, y: 4.63, w: 1.05, h: 0.3, fontSize: 22, color: C.leaf, align: "center" });
  const hypotheses = [
    { x: 4.52, head: "假设 A", fill: C.goldSoft, color: C.gold },
    { x: 8.48, head: "假设 B", fill: C.riverSoft, color: C.river },
  ];
  hypotheses.forEach((item) => {
    rect(slide, pres, item.x, 3.68, 3.55, 2.12, item.fill, item.color, true);
    addText(slide, item.head, { x: item.x + 0.25, y: 3.94, w: 3.05, h: 0.34, fontSize: 23, bold: true, color: item.color, align: "center" });
    addText(slide, "可能让我想到", { x: item.x + 0.28, y: 4.45, w: 2.99, h: 0.3, fontSize: 19, color: C.ink2, align: "center" });
    line(slide, pres, item.x + 0.55, 5.02, 2.45, 0, item.color, 1.1);
    addText(slide, "感官依据 ______", { x: item.x + 0.45, y: 5.3, w: 2.65, h: 0.28, fontSize: 18, color: C.ink2, align: "center" });
  });
  addText(slide, "两种可能先都保留　→　第四章‘黄而陨’出现后再筛选", { x: 2.18, y: 6.25, w: 8.98, h: 0.42, fontSize: 23, bold: true, color: C.leaf, align: "center" });
  addNotes(slide, page);
}

function renderEcho(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "两声‘于嗟’，各自在劝谁", { color: C.paper });
  const rows = [
    { y: 1.28, text: "于嗟鸠兮，无食桑葚！", fill: "343C32", line: C.leaf2, color: C.leafSoft },
    { y: 2.58, text: "于嗟女兮，无与士耽！", fill: "3D3436", line: C.plum, color: C.plumSoft },
  ];
  rows.forEach((row) => {
    rect(slide, pres, 0.88, row.y, 11.58, 0.98, row.fill, row.line, true);
    addText(slide, row.text, { x: 1.2, y: row.y + 0.25, w: 10.94, h: 0.44, fontFace: FONT_TEXT, fontSize: 36, bold: true, color: row.color, align: "center" });
  });
  addText(slide, "于嗟 xū jiē｜无同‘毋’｜旧说斑鸠多食桑葚会昏醉｜耽：沉溺、沉醉", { x: 1.05, y: 3.82, w: 11.25, h: 0.34, fontSize: 20, color: C.warm, align: "center" });
  const cards = [
    ["反复的声音", "________", C.gold, "3B372F"],
    ["改变的对象", "____  →  ____", C.leaf2, "303933"],
    ["改变的劝告", "____  →  ____", C.plum, "3B3034"],
  ];
  cards.forEach(([head, body, color, fill], index) => {
    const x = 0.92 + index * 4.03;
    rect(slide, pres, x, 4.45, 3.62, 1.35, fill, color, true);
    addText(slide, head, { x: x + 0.2, y: 4.7, w: 3.22, h: 0.3, fontSize: 21, bold: true, color, align: "center" });
    addText(slide, body, { x: x + 0.2, y: 5.2, w: 3.22, h: 0.34, fontSize: 22, bold: true, color: C.paper, align: "center" });
  });
  addText(slide, "两人同节拍对读　→　交换角色　→　用一句自然话说两声劝告怎样接过去", { x: 1.45, y: 6.3, w: 10.43, h: 0.4, fontSize: 22, bold: true, color: C.warm, align: "center" });
  addNotes(slide, page);
}

function renderExitContrast(slide, pres, page) {
  base(slide, pres);
  title(slide, "同是‘耽’，为何一边可说，一边不可说");
  const cols = [
    { x: 0.9, text: "士之耽兮，犹可说也。", fill: C.riverSoft, color: C.river },
    { x: 6.83, text: "女之耽兮，不可说也！", fill: C.plumSoft, color: C.plum },
  ];
  cols.forEach((col) => {
    rect(slide, pres, col.x, 1.28, 5.58, 1.18, col.fill, col.color, true);
    addText(slide, col.text, { x: col.x + 0.25, y: 1.59, w: 5.08, h: 0.48, fontFace: FONT_TEXT, fontSize: 32, bold: true, color: col.color, align: "center" });
  });
  addText(slide, "说（tuō）：同‘脱’，摆脱、脱身", { x: 3.75, y: 2.72, w: 5.83, h: 0.36, fontSize: 23, bold: true, color: C.ink2, align: "center" });
  rect(slide, pres, 0.98, 3.34, 5.4, 1.18, C.paper2, C.warm, true);
  rect(slide, pres, 6.94, 3.34, 5.4, 1.18, C.paper2, C.warm, true);
  addText(slide, "两句完全相同的词", { x: 1.28, y: 3.58, w: 4.8, h: 0.32, fontSize: 21, bold: true, color: C.leaf, align: "center" });
  addText(slide, "真正改变判断的词", { x: 7.24, y: 3.58, w: 4.8, h: 0.32, fontSize: 21, bold: true, color: C.red, align: "center" });
  addText(slide, "________________", { x: 1.55, y: 4.05, w: 4.25, h: 0.28, fontSize: 21, color: C.ink2, align: "center" });
  addText(slide, "________________", { x: 7.51, y: 4.05, w: 4.25, h: 0.28, fontSize: 21, color: C.ink2, align: "center" });
  rect(slide, pres, 1.35, 4.95, 10.63, 1.24, C.goldSoft, C.gold, true);
  addText(slide, "两句写出了怎样不同的脱身处境？", { x: 1.7, y: 5.18, w: 9.93, h: 0.34, fontFace: FONT_HEAD, fontSize: 25, bold: true, color: C.gold, align: "center" });
  line(slide, pres, 2.45, 5.82, 8.43, 0, C.gold, 1.1);
  addText(slide, "此刻能确认的是 __________　仍待追问：为什么会有这种差别？", { x: 2.2, y: 6.46, w: 8.93, h: 0.32, fontSize: 20.5, color: C.red, align: "center" });
  addNotes(slide, page);
}

function renderDeletion(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "若诗直接从‘于嗟女兮’开始，会失去什么", { color: C.paper });
  addText(slide, "读两遍，听劝诫怎样来到耳边", { x: 3.28, y: 1.12, w: 6.8, h: 0.42, fontFace: FONT_HEAD, fontSize: 27, bold: true, color: C.warm, align: "center" });
  rect(slide, pres, 0.88, 1.8, 5.8, 3.25, "343A31", C.leaf2, true);
  rect(slide, pres, 6.92, 1.8, 5.55, 3.25, "3D3336", C.plum, true);
  addText(slide, "A｜原诗", { x: 1.2, y: 2.1, w: 5.16, h: 0.35, fontSize: 23, bold: true, color: C.leafSoft, align: "center" });
  ["桑之未落，其叶沃若。", "于嗟鸠兮，无食桑葚！", "于嗟女兮，无与士耽！"].forEach((text, index) => addText(slide, text, { x: 1.15, y: 2.72 + index * 0.64, w: 5.26, h: 0.42, fontFace: FONT_TEXT, fontSize: 27, bold: index === 2, color: index === 2 ? C.plumSoft : C.paper, align: "center" }));
  addText(slide, "B｜删去桑叶与斑鸠", { x: 7.25, y: 2.1, w: 4.9, h: 0.35, fontSize: 23, bold: true, color: C.plumSoft, align: "center" });
  addText(slide, "于嗟女兮，无与士耽！", { x: 7.25, y: 3.3, w: 4.9, h: 0.5, fontFace: FONT_TEXT, fontSize: 30, bold: true, color: C.paper, align: "center" });
  addText(slide, "两种写法，劝告怎样不同地来到耳边？", { x: 7.25, y: 4.08, w: 4.9, h: 0.38, fontSize: 20.5, color: C.warm, align: "center" });
  rect(slide, pres, 1.42, 5.47, 10.5, 0.95, "34312E", C.gold, true);
  addText(slide, "差异　□画面　□声音　□情感铺垫　□删改句更直接　原词依据 ______", { x: 1.72, y: 5.75, w: 9.9, h: 0.36, fontSize: 21.5, bold: true, color: C.goldSoft, align: "center" });
  addText(slide, "哪一种更打动你？请让原词替你说话", { x: 4.15, y: 6.67, w: 5.05, h: 0.28, fontFace: FONT_HEAD, fontSize: 19, color: C.warm, align: "center" });
  addNotes(slide, page);
}

function renderRetrieval(slide, pres, page) {
  base(slide, pres);
  title(slide, "把章首三处落点接成四级声音阶梯");
  addText(slide, "取回章首三处落点　→　合上书", { x: 3.4, y: 1.18, w: 6.53, h: 0.38, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: C.leaf, align: "center" });
  const cards = [
    ["劝女子勿耽", C.plumSoft, C.plum], ["桑叶沃若", C.leafSoft, C.leaf], ["比较脱身处境", C.goldSoft, C.gold], ["劝斑鸠勿食", C.riverSoft, C.river],
  ];
  cards.forEach(([word, fill, color], index) => {
    const x = 0.67 + index * 3.16;
    rect(slide, pres, x, 2.05, 2.85, 1.42, fill, color, true);
    addText(slide, word, { x: x + 0.2, y: 2.28, w: 2.45, h: 0.38, fontFace: FONT_TEXT, fontSize: 24, bold: true, color, align: "center" });
    addText(slide, "序号 __　原词 ______", { x: x + 0.18, y: 2.86, w: 2.49, h: 0.28, fontSize: 17.5, color: C.ink2, align: "center" });
  });
  rect(slide, pres, 1.1, 4.05, 11.13, 0.98, C.paper2, C.warm, true);
  addText(slide, "同桌只找声音断层　→　翻诗定位，换笔修订", { x: 1.45, y: 4.35, w: 10.43, h: 0.36, fontSize: 23, bold: true, color: C.ink2, align: "center" });
  rect(slide, pres, 1.1, 5.35, 11.13, 1.12, C.leafSoft, C.leaf, true);
  addText(slide, "合上书，替这一章补一句故事旁白：________________", { x: 1.45, y: 5.62, w: 10.43, h: 0.4, fontFace: FONT_HEAD, fontSize: 25, bold: true, color: C.leaf, align: "center" });
  line(slide, pres, 3.0, 6.2, 7.33, 0, C.leaf, 1.1);
  addNotes(slide, page);
}

function renderClose(slide, pres, page) {
  base(slide, pres);
  title(slide, "让第三章成为回望中的一段话");
  rect(slide, pres, 0.78, 1.15, 11.78, 2.78, C.paper2, C.warm, true);
  LINES.forEach((text, index) => addText(slide, text, { x: 1.15, y: 1.47 + index * 0.45, w: 11.0, h: 0.34, fontFace: FONT_TEXT, fontSize: 26.5, color: C.ink, align: "center" }));
  addText(slide, "完整重读　→　合书讲30秒", { x: 0.95, y: 4.32, w: 3.5, h: 0.42, fontSize: 23, bold: true, color: C.river, align: "center" });
  addText(slide, "眼前先出现什么", { x: 4.42, y: 4.32, w: 2.24, h: 0.42, fontSize: 20.5, bold: true, color: C.leaf, align: "center" });
  addText(slide, "两声劝告先后落在谁身上", { x: 6.62, y: 4.32, w: 3.36, h: 0.42, fontSize: 20.5, bold: true, color: C.plum, align: "center" });
  addText(slide, "最后谁更难脱身", { x: 9.94, y: 4.32, w: 2.2, h: 0.42, fontSize: 20.5, bold: true, color: C.gold, align: "center" });
  rect(slide, pres, 0.98, 5.1, 11.37, 1.02, C.riverSoft, C.river, true);
  addText(slide, "听见遗漏，只报一处｜讲述者回到诗中，把它补上", { x: 1.3, y: 5.41, w: 10.73, h: 0.36, fontSize: 23, bold: true, color: C.river, align: "center" });
  addText(slide, "初见议婚　→　等待迁嫁　→　____________________________", { x: 2.35, y: 6.45, w: 8.63, h: 0.4, fontFace: FONT_HEAD, fontSize: 23, bold: true, color: C.red, align: "center" });
  addNotes(slide, page);
}

function renderShelf(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "把第三章收进书页", { color: C.paper });
  const rows = [
    ["字词", "沃若：润泽｜于嗟 xū jiē｜无同‘毋’｜耽：沉溺｜说 tuō 同‘脱’", C.leaf2, "313A31"],
    ["声音", "桑叶入眼 → 劝鸠 → 劝女 → 士/女、可/不可正面对照", C.river, "303A3D"],
    ["手法", "由物起兴、由物及人的比兴｜‘于嗟’反复与呼告｜正面对照", C.gold, "3B372F"],
    ["待证", "桑叶待‘黄而陨’筛选｜男女处境为何不同，要看婚后事实", C.plum, "3C3236"],
    ["责任", "女子的投入，不分担男子失信或粗暴的责任", C.red, "3D302D"],
  ];
  rows.forEach(([head, body, color, fill], index) => {
    const y = 1.08 + index * 0.96;
    rect(slide, pres, 0.92, y, 11.5, 0.78, fill, color, true);
    rect(slide, pres, 1.15, y + 0.13, 1.0, 0.52, color, color, true);
    addText(slide, head, { x: 1.35, y: y + 0.24, w: 0.6, h: 0.26, fontSize: 19, bold: true, color: C.white, align: "center" });
    addText(slide, body, { x: 2.48, y: y + 0.18, w: 9.45, h: 0.42, fontSize: index >= 3 ? 19.5 : 21, bold: index >= 3, color: index === 3 ? C.plumSoft : index === 4 ? C.redSoft : C.paper, align: "left" });
  });
  rect(slide, pres, 1.38, 5.93, 10.58, 0.98, "35312E", C.warm, true);
  addText(slide, "翻回自己的学习单：桑叶假设｜两声记录｜脱身对照｜删句比较｜故事旁白\n给仍未站稳的一项加 ★；回到原句，让诗句把它托住", { x: 1.62, y: 6.08, w: 10.1, h: 0.62, fontFace: FONT_HEAD, fontSize: 18.2, bold: true, color: C.warm, align: "center", breakLine: false });
  addNotes(slide, page);
}

function validate(pres) {
  const errors = [];
  if (pres._slides.length !== 8) errors.push(`slides=${pres._slides.length}`);
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
  pres.author = "语文备课系统"; pres.title = "《氓》V6第三章课堂课件"; pres.subject = "第三章由桑叶物象进入劝诫与处境对照"; pres.lang = "zh-CN";
  pres.theme = { headFontFace: FONT_HEAD, bodyFontFace: FONT_BODY, lang: "zh-CN" };
  const renderers = [renderOpening, renderMulberry, renderEcho, renderExitContrast, renderDeletion, renderRetrieval, renderClose, renderShelf];
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
    illustration_policy: "no_illustration_before_page_function_freeze",
    claim_boundary: "chapter3_candidate_not_classroom_observed",
  };
  fs.writeFileSync(MANIFEST, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`CHAPTER3_PPTX_OK slides=8 pptx=${PPTX}\n`);
}

main().catch((error) => { console.error(error.stack || error); process.exit(1); });
