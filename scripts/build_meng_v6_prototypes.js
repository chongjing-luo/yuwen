#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");

function requireGlobal(name) {
  try { return require(name); }
  catch (_) {
    const root = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
    return require(path.join(root, name));
  }
}

const pptxgen = requireGlobal("pptxgenjs");
const npmRoot = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
const JSZip = require(path.join(npmRoot, "pptxgenjs", "node_modules", "jszip"));

const ROOT = path.resolve(__dirname, "..");
const STAGE = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage");
const SNAPSHOT = path.join(STAGE, "opening", "package", "06_氓_V6导入切片课程数据快照.json");
const OUT = path.join(STAGE, "prototypes");
const PPTX = path.join(OUT, "04P_氓_V6三类页面视觉原型.pptx");
const MANIFEST = path.join(OUT, "prototype_manifest.json");

const W = 13.333;
const H = 7.5;
const FONT_HEAD = "Noto Serif CJK SC";
const FONT_BODY = "Noto Sans CJK SC";
const FONT_TEXT = "Noto Serif CJK SC";
const C = {
  ink: "27231F", ink2: "4B443D", paper: "F6F0E5", paper2: "FFFCF6",
  warm: "E7DCCB", cinnabar: "A84A3A", cinnabarSoft: "F1DCD5",
  river: "4E7480", riverSoft: "DCE9EA", leaf: "647752", leafSoft: "E1E7D9",
  gold: "B18B52", white: "FFFFFF", muted: "766E65",
};

function sha256(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function presentation() {
  const pres = new pptxgen();
  pres.defineLayout({ name: "MENG_WIDE", width: W, height: H });
  pres.layout = "MENG_WIDE";
  pres.author = "语文备课系统";
  pres.company = "语文备课系统";
  pres.subject = "《氓》V6三类页面视觉原型";
  pres.title = "《氓》V6三类页面视觉原型";
  pres.lang = "zh-CN";
  pres.theme = { headFontFace: FONT_HEAD, bodyFontFace: FONT_BODY, lang: "zh-CN" };
  return pres;
}

function addText(slide, text, options = {}) {
  slide.addText(text, {
    x: 0.72, y: 0.55, w: 11.9, h: 0.5, margin: 0,
    fontFace: FONT_BODY, fontSize: 28, color: C.ink,
    breakLine: false, valign: "mid", ...options,
  });
}

function rect(slide, pres, x, y, w, h, fill, line = fill, radius = false) {
  slide.addShape(radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: fill }, line: { color: line, width: 1 },
    ...(radius ? { rectRadius: 0.06 } : {}),
  });
}

function line(slide, pres, x, y, w, color, width = 1) {
  slide.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width } });
}

function title(slide, text, accent = C.cinnabar) {
  addText(slide, text, {
    x: 0.72, y: 0.42, w: 11.9, h: 0.58,
    fontFace: FONT_HEAD, fontSize: 34, bold: true,
  });
}

function notesFor(page) {
  const script = page.script;
  const timeboxes = script.timeboxes.map((item) => `${item.label}：${item.seconds}秒`).join("；");
  const branches = script.branches.map((item) => `${item.kind}：${item.response}`).join("\n");
  return [
    `【V6页ID】${page.page_id}｜${page.title}｜${page.minutes}分钟`,
    "【教师逐字稿】", script.teacher_spoken,
    "【场面与走位】", script.scene, ...script.stage_directions.map((item) => `（${item}）`),
    "【时间盒】", timeboxes,
    "【现场分支】", branches,
    "【听者同步任务】", script.listener_task,
    "【证据位置】", script.evidence_location,
    "【自然切页句】", script.cut_line,
    "【声明边界】桌面排演稿；不声称真实学生已经理解、参与或学会。",
  ].join("\n");
}

function base(slide, pres) {
  slide.background = { color: C.paper };
  rect(slide, pres, 0, 0, W, 0.13, C.ink, C.ink);
}

function renderN003(slide, pres, page) {
  base(slide, pres);
  title(slide, "把四个人的故事放在一起", C.gold);
  addText(slide, "自定1号｜按号轮说", { x: 0.82, y: 1.34, w: 3.25, h: 0.42, fontSize: 22, bold: true, color: C.cinnabar });
  ["1", "2", "3", "4"].forEach((label, index) => {
    const x = 4.05 + index * 1.72;
    slide.addShape(pres.shapes.OVAL, { x, y: 1.24, w: 0.72, h: 0.72, fill: { color: C.paper2 }, line: { color: C.cinnabar, width: 1.6 } });
    addText(slide, label, { x, y: 1.43, w: 0.72, h: 0.27, fontSize: 21, bold: true, color: C.cinnabar, align: "center" });
    if (index < 3) addText(slide, "→", { x: x + 0.82, y: 1.4, w: 0.72, h: 0.28, fontSize: 22, color: C.gold, align: "center" });
  });
  line(slide, pres, 0.82, 2.18, 11.68, C.warm, 1.2);
  rect(slide, pres, 0.82, 2.52, 5.58, 2.3, C.cinnabarSoft, C.cinnabar, true);
  addText(slide, "轮到我", { x: 1.2, y: 2.88, w: 4.82, h: 0.42, fontSize: 25, bold: true, color: C.cinnabar, align: "center" });
  addText(slide, "15—20秒", { x: 1.2, y: 3.52, w: 4.82, h: 0.42, fontSize: 29, bold: true, align: "center" });
  addText(slide, "篇名＋它写了什么", { x: 1.2, y: 4.16, w: 4.82, h: 0.35, fontFace: FONT_HEAD, fontSize: 24, bold: true, align: "center" });
  rect(slide, pres, 6.9, 2.52, 5.6, 2.3, C.leafSoft, C.leaf, true);
  addText(slide, "听别人", { x: 7.28, y: 2.88, w: 4.84, h: 0.42, fontSize: 25, bold: true, color: C.leaf, align: "center" });
  addText(slide, "听见新内容就勾", { x: 7.28, y: 3.42, w: 4.84, h: 0.42, fontSize: 27, bold: true, align: "center" });
  addText(slide, "有勾项，圈一项", { x: 7.28, y: 4.0, w: 4.84, h: 0.32, fontFace: FONT_HEAD, fontSize: 22.5, bold: true, align: "center" });
  addText(slide, "暂无新增，从作品谱圈一项", { x: 7.28, y: 4.38, w: 4.84, h: 0.28, fontSize: 18.5, color: C.muted, align: "center" });
  rect(slide, pres, 1.12, 5.22, 11.08, 0.7, C.riverSoft, C.river, true);
  addText(slide, "执笔人记全组作品谱；轮到自己时，下一位代记", { x: 1.48, y: 5.41, w: 10.36, h: 0.3, fontSize: 22, bold: true, color: C.river, align: "center" });
  addText(slide, "作品重复？可以补一个不同主题。", { x: 2.35, y: 6.37, w: 8.63, h: 0.3, fontSize: 22, color: C.muted, align: "center" });
  slide.addNotes(notesFor(page));
}

function renderN008(slide, pres, page) {
  base(slide, pres);
  addText(slide, "第一次完整听读｜第一至第三章", { x: 0.72, y: 0.32, w: 5.2, h: 0.4, fontFace: FONT_HEAD, fontSize: 25, bold: true, color: C.cinnabar });
  addText(slide, "眼随声走｜不齐读｜用笔在教材原句旁留一点", { x: 6.65, y: 0.39, w: 5.97, h: 0.28, fontSize: 17.5, bold: true, color: C.ink2, align: "right" });
  line(slide, pres, 0.72, 0.82, 11.9, C.warm, 1.1);
  const stanzas = [
    [
      "氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。",
      "送子涉淇，至于顿丘。匪我愆期，子无良媒。",
      "将子无怒，秋以为期。",
    ],
    [
      "乘彼垝垣，以望复关。不见复关，泣涕涟涟。",
      "既见复关，载笑载言。尔卜尔筮，体无咎言。",
      "以尔车来，以我贿迁。",
    ],
    [
      "桑之未落，其叶沃若。于嗟鸠兮，无食桑葚！",
      "于嗟女兮，无与士耽！士之耽兮，犹可说也。",
      "女之耽兮，不可说也！",
    ],
  ];
  const accents = [C.gold, C.river, C.leaf];
  stanzas.forEach((rows, index) => {
    const y = 0.98 + index * 2.07;
    rect(slide, pres, 0.72, y, 11.9, 1.85, index % 2 ? C.paper2 : "F9F4EA", index % 2 ? C.paper2 : "F9F4EA", true);
    rect(slide, pres, 0.72, y + 0.17, 0.08, 1.5, accents[index], accents[index]);
    addText(slide, `${["一", "二", "三"][index]}章`, { x: 0.89, y: y + 0.15, w: 0.55, h: 0.29, fontSize: 17.5, bold: true, color: accents[index], align: "center" });
    addText(slide, rows.map((text, row) => ({ text, options: { breakLine: row < rows.length - 1 } })), {
      x: 1.5, y: y + 0.16, w: 10.73, h: 1.49,
      fontFace: FONT_TEXT, fontSize: 29.5, color: C.ink, breakLine: true,
      breakLineOnTextOverflow: false, lineSpacingMultiple: 1.0,
    });
  });
  slide.addNotes(notesFor(page));
}

function renderN012(slide, pres, page) {
  base(slide, pres);
  title(slide, "先借四言节奏走进声音", C.river);
  rect(slide, pres, 0.82, 1.34, 11.7, 3.2, C.paper2, C.river, true);
  addText(slide, "氓之／蚩蚩，抱布／贸丝。", {
    x: 1.25, y: 1.84, w: 10.84, h: 0.78, fontFace: FONT_TEXT,
    fontSize: 44, bold: true, align: "center", color: C.ink,
  });
  addText(slide, "匪来／贸丝，来即／我谋。", {
    x: 1.25, y: 2.95, w: 10.84, h: 0.78, fontFace: FONT_TEXT,
    fontSize: 44, bold: true, align: "center", color: C.ink,
  });
  addText(slide, "／只提示节奏，不切碎完整动作", { x: 3.45, y: 4.06, w: 6.43, h: 0.3, fontSize: 20.5, bold: true, color: C.river, align: "center" });
  addText(slide, "① 屏幕跟读", { x: 0.95, y: 4.92, w: 2.45, h: 0.34, fontSize: 23, bold: true, color: C.river, align: "center" });
  addText(slide, "听到“看教材”", { x: 4.2, y: 4.92, w: 2.7, h: 0.34, fontSize: 22, bold: true, color: C.gold, align: "center" });
  addText(slide, "② 教材第一章开头｜无斜线原句", { x: 7.38, y: 4.92, w: 4.95, h: 0.34, fontSize: 22, bold: true, color: C.leaf, align: "center" });
  addText(slide, "→", { x: 3.42, y: 4.9, w: 0.62, h: 0.35, fontSize: 25, bold: true, color: C.gold, align: "center" });
  addText(slide, "→", { x: 6.82, y: 4.9, w: 0.52, h: 0.35, fontSize: 25, bold: true, color: C.gold, align: "center" });
  line(slide, pres, 0.95, 5.56, 11.38, C.warm, 1.1);
  addText(slide, "听者问：谁做什么？", { x: 1.15, y: 5.9, w: 4.4, h: 0.42, fontSize: 24, bold: true, color: C.leaf, align: "center" });
  addText(slide, "→", { x: 5.78, y: 5.94, w: 0.8, h: 0.35, fontSize: 26, bold: true, color: C.gold, align: "center" });
  addText(slide, "读者带着完整动作再读", { x: 6.82, y: 5.9, w: 5.0, h: 0.42, fontSize: 24, bold: true, color: C.cinnabar, align: "center" });
  addText(slide, "在路标卡写下重读后改动的一处", { x: 3.36, y: 6.63, w: 6.62, h: 0.3, fontSize: 20.5, bold: true, color: C.ink2, align: "center" });
  slide.addNotes(notesFor(page));
}

function validateObjects(pres) {
  const errors = [];
  if (pres._slides.length !== 3) errors.push(`expected 3 slides, got ${pres._slides.length}`);
  pres._slides.forEach((slide, slideIndex) => {
    if (!slide._slideObjects.some((item) => item._type === "notes")) errors.push(`slide ${slideIndex + 1}: missing notes`);
    slide._slideObjects.forEach((object, objectIndex) => {
      const o = object.options || {};
      if ([o.x, o.y, o.w, o.h].every((value) => typeof value === "number")) {
        if (o.x < -0.01 || o.y < -0.01 || o.x + o.w > W + 0.01 || o.y + o.h > H + 0.01) {
          errors.push(`slide ${slideIndex + 1} object ${objectIndex + 1}: out of bounds`);
        }
      }
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
  const pageMap = new Map(snapshot.pages.map((page) => [page.page_id, page]));
  const selected = ["N003", "N008", "N012"].map((id) => {
    const page = pageMap.get(id);
    if (!page) throw new Error(`snapshot missing ${id}`);
    return page;
  });
  const pres = presentation();
  const renderers = [renderN003, renderN008, renderN012];
  selected.forEach((page, index) => renderers[index](pres.addSlide(), pres, page));
  validateObjects(pres);
  fs.mkdirSync(OUT, { recursive: true });
  await pres.writeFile({ fileName: PPTX, compression: true });
  await repairNotesMaster(PPTX);
  const manifest = {
    schema_version: "1.0",
    artifact: path.relative(ROOT, PPTX).split(path.sep).join("/"),
    sha256: sha256(PPTX),
    source_snapshot_sha256: sha256(SNAPSHOT),
    physical_slides: selected.map((page, index) => ({ physical_index: index + 1, page_id: page.page_id, primary_visual_duty: page.page_id === "N003" ? "活动界面" : page.page_id === "N008" ? "全文/章内整读" : "原文批注" })),
    illustration_policy: "no_character_illustration; page function is carried by role interface, complete poem, or removable rhythm scaffold",
    claim_boundary: "rendered_prototype_not_classroom_observed",
  };
  fs.writeFileSync(MANIFEST, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`PROTOTYPE_OK slides=3 pptx=${PPTX}\n`);
}

main().catch((error) => { console.error(error.stack || error); process.exit(1); });
