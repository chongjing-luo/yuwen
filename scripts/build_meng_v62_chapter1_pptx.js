#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

function requireGlobal(name) {
  try { return require(name); }
  catch (_) {
    const root = process.env.NODE_GLOBAL_ROOT || "/usr/local/node-v22.22.2-linux-x64/lib/node_modules";
    return require(path.join(root, name));
  }
}

const pptxgen = requireGlobal("pptxgenjs");
const npmRoot = process.env.NODE_GLOBAL_ROOT || "/usr/local/node-v22.22.2-linux-x64/lib/node_modules";
const JSZip = require(path.join(npmRoot, "pptxgenjs", "node_modules", "jszip"));
const source = require("./meng_v62/content/chapter_1");
const { validate } = require("./verify_meng_v62_chapter1");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const SNAPSHOT = path.join(stageDir(), "chapter_1", "package", "06_氓_V62第一章课程数据快照.json");
const OUT = assertV62OutputPath(path.join(stageDir(), "chapter_1", "pptx"));
const PPTX = assertV62OutputPath(path.join(OUT, "04_氓_V62第一章课堂课件.pptx"));
const MANIFEST = assertV62OutputPath(path.join(OUT, "chapter1_pptx_manifest.json"));

const W = 13.333;
const H = 7.5;
const FONT_HEAD = "Noto Serif CJK SC";
const FONT_BODY = "Noto Sans CJK SC";
const FONT_TEXT = "Noto Serif CJK SC";
const C = {
  ink: "29241F", ink2: "51483F", paper: "F6F0E5", paper2: "FFFCF7",
  warm: "E5DAC9", warm2: "D2C1AA", cinnabar: "9C4538", cinnabarSoft: "F0DDD5",
  river: "456F7C", riverSoft: "DDE9E9", leaf: "647752", leafSoft: "E1E7D9",
  gold: "AC8550", goldSoft: "EFE4D2", white: "FFFFFF", muted: "766D63",
  night: "28241F", night2: "38312A",
};

function sha256(filePath) { return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex"); }

function presentation() {
  const pres = new pptxgen();
  pres.defineLayout({ name: "MENG_WIDE", width: W, height: H });
  pres.layout = "MENG_WIDE";
  pres.author = "语文备课系统";
  pres.company = "语文备课系统";
  pres.subject = "《氓》V6.2第一章逐句讲读";
  pres.title = "《氓》V6.2第一章课堂课件";
  pres.lang = "zh-CN";
  pres.theme = { headFontFace: FONT_HEAD, bodyFontFace: FONT_BODY, lang: "zh-CN" };
  return pres;
}

function addText(slide, text, options = {}) {
  slide.addText(text, {
    x: 0.72, y: 0.52, w: 11.9, h: 0.5, margin: 0,
    fontFace: FONT_BODY, fontSize: 28, color: C.ink,
    valign: "mid", breakLine: false, ...options,
  });
}

function rect(slide, pres, x, y, w, h, fill, lineColor = fill, radius = false, transparency = 0, width = 1) {
  slide.addShape(radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: fill, transparency }, line: { color: lineColor, width },
    ...(radius ? { rectRadius: 0.05 } : {}),
  });
}

function line(slide, pres, x, y, w, color, width = 1, transparency = 0, dash = "solid") {
  slide.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width, transparency, dashType: dash } });
}

function dot(slide, pres, x, y, d, color, transparency = 0) {
  slide.addShape(pres.shapes.OVAL, { x, y, w: d, h: d, fill: { color, transparency }, line: { color, transparency } });
}

function base(slide, pres, dark = false) {
  slide.background = { color: dark ? C.night : C.paper };
  rect(slide, pres, 0, 0, W, 0.12, dark ? C.gold : C.ink, dark ? C.gold : C.ink);
}

function title(slide, text, options = {}) {
  addText(slide, text, {
    x: 0.76, y: 0.38, w: 10.35, h: 0.62,
    fontFace: FONT_HEAD, fontSize: 33, bold: true, ...options,
  });
  addText(slide, "第一章　1 / 6", {
    x: 10.78, y: 0.5, w: 1.82, h: 0.3, fontSize: 17.5,
    bold: true, color: options.color || C.cinnabar, align: "right",
  });
}

function notesFor(page) {
  const s = page.script;
  return [
    `【V6.2页ID】${page.page_id}｜${page.title}｜${page.minutes}分钟`,
    "【本页不可替代的意义】", page.unique_function,
    "【删除本页会失去什么】", page.deletion_loss,
    "【相邻合并测试】", page.merge_test,
    "【教师逐字稿】", s.teacher_spoken,
    "【场面与走位】", s.scene, ...s.stage_directions.map((item) => `（${item}）`),
    "【时间盒】", s.timeboxes.map((item) => `${item.label}：${item.seconds}秒`).join("；"),
    "【现场分支】", s.branches.map((item) => `${item.kind}：${item.response}`).join("\n"),
    "【听者同步任务】", s.listener_task,
    "【证据位置】", s.evidence_location,
    "【回到人物和故事】", page.story_return,
    "【后续真实调用】", page.next_use,
    "【自然切页句】", s.cut_line,
    "【声明边界】桌面排演稿；不声称真实学生已经理解、参与或学会。",
  ].join("\n");
}

function addNotes(slide, page) { slide.addNotes(notesFor(page)); }

function addPoemCard(slide, pres, lines, options = {}) {
  const x = options.x ?? 0.88;
  const y = options.y ?? 1.24;
  const w = options.w ?? 11.58;
  const h = options.h ?? 4.45;
  rect(slide, pres, x, y, w, h, options.fill || C.paper2, options.line || C.warm, true, 0, 1.05);
  const startY = y + (options.topInset ?? 0.38);
  const step = options.step ?? 0.66;
  lines.forEach((text, index) => addText(slide, text, {
    x: x + 0.38, y: startY + index * step, w: w - 0.76, h: options.lineH ?? 0.46,
    fontFace: FONT_TEXT, fontSize: options.fontSize ?? 31, color: C.ink,
    align: options.align || "center", bold: false,
  }));
}

function renderC101(slide, pres, page) {
  base(slide, pres);
  title(slide, "第一章｜两个人怎样走近婚事");
  const poemLines = page.original_text.split("。").filter(Boolean).map((text) => `${text}。`);
  addPoemCard(slide, pres, poemLines, { y: 1.18, h: 4.38, fontSize: 31, step: 0.69, topInset: 0.42 });
  dot(slide, pres, 1.0, 6.05, 0.18, C.cinnabar);
  addText(slide, "圈一圈他做的事", { x: 1.35, y: 5.94, w: 3.1, h: 0.4, fontFace: FONT_HEAD, fontSize: 23, bold: true, color: C.cinnabar });
  dot(slide, pres, 5.12, 6.05, 0.18, C.river);
  addText(slide, "划一划她做的事", { x: 5.47, y: 5.94, w: 3.1, h: 0.4, fontFace: FONT_HEAD, fontSize: 23, bold: true, color: C.river });
  addText(slide, "同桌只核对：这是谁做的？", { x: 8.65, y: 5.94, w: 3.75, h: 0.4, fontSize: 21.5, color: C.muted, align: "right" });
  addText(slide, "暂时不懂的词，先留一个问号。", { x: 3.8, y: 6.66, w: 5.72, h: 0.3, fontSize: 19.5, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderC102(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "抱布而来，是为了什么？", { color: C.paper });
  rect(slide, pres, 0.9, 1.28, 11.53, 2.3, C.night2, C.gold, true, 0, 1.1);
  const lines = page.original_text.split("。").filter(Boolean);
  addText(slide, `${lines[0]}。`, {
    x: 1.22, y: 1.67, w: 10.89, h: 0.62, fontFace: FONT_TEXT,
    fontSize: 39, color: C.paper, align: "center",
  });
  addText(slide, `${lines[1]}。`, {
    x: 1.22, y: 2.58, w: 10.89, h: 0.62, fontFace: FONT_TEXT,
    fontSize: 39, color: C.paper, align: "center",
  });
  const prompts = [
    ["诗先让我们看见什么？", C.gold, "3E372E"],
    ["女子随后告诉我们什么？", C.river, "303A3D"],
    ["哪个字，让话转了弯？", C.cinnabar, "40302D"],
  ];
  prompts.forEach(([textValue, color, fill], index) => {
    const x = 0.9 + index * 4.02;
    rect(slide, pres, x, 4.35, 3.52, 1.28, fill, color, true, 0, 1.1);
    addText(slide, textValue, {
      x: x + 0.1, y: 4.67, w: 3.32, h: 0.54, fontFace: FONT_HEAD,
      fontSize: 20.5, bold: true, color: index === 0 ? C.warm : index === 1 ? C.riverSoft : C.cinnabarSoft,
      align: "center", valign: "mid",
    });
  });
  addText(slide, "先说成自己的自然话，再回到原词。", {
    x: 3.3, y: 6.36, w: 6.73, h: 0.4, fontFace: FONT_HEAD,
    fontSize: 22, color: C.warm, align: "center",
  });
  addNotes(slide, page);
}

function renderC103(slide, pres, page) {
  base(slide, pres);
  title(slide, "她把他送了多远？");
  addText(slide, page.original_text, {
    x: 0.9, y: 1.32, w: 11.53, h: 0.76, fontFace: FONT_TEXT,
    fontSize: 44, bold: true, color: C.ink, align: "center",
  });
  line(slide, pres, 1.3, 2.38, 10.73, C.warm2, 1);
  const words = [
    ["送", 1.35, C.gold, C.goldSoft],
    ["涉", 5.19, C.river, C.riverSoft],
    ["至", 9.03, C.cinnabar, C.cinnabarSoft],
  ];
  words.forEach(([word, x, color, fill]) => {
    dot(slide, pres, x, 3.0, 2.95, fill);
    addText(slide, word, { x, y: 3.69, w: 2.95, h: 0.76, fontFace: FONT_TEXT, fontSize: 49, bold: true, color, align: "center" });
  });
  addText(slide, "用这三个字，把这段路说出来。", {
    x: 3.15, y: 6.25, w: 7.03, h: 0.48, fontFace: FONT_HEAD,
    fontSize: 27, bold: true, color: C.ink, align: "center",
  });
  addNotes(slide, page);
}

function renderC104(slide, pres, page) {
  base(slide, pres);
  title(slide, "她怎样把婚事继续说下去？");
  const lines = page.original_text.split("。").filter(Boolean);
  rect(slide, pres, 0.88, 1.25, 11.57, 2.2, C.paper2, C.warm2, true, 0, 1.05);
  addText(slide, `${lines[0]}。`, {
    x: 1.15, y: 1.65, w: 11.03, h: 0.6, fontFace: FONT_TEXT,
    fontSize: 38, color: C.ink, align: "center",
  });
  addText(slide, `${lines[1]}。`, {
    x: 1.15, y: 2.51, w: 11.03, h: 0.6, fontFace: FONT_TEXT,
    fontSize: 38, color: C.ink, align: "center",
  });
  addText(slide, "这四小句，各在做什么？", {
    x: 2.4, y: 3.88, w: 8.53, h: 0.48, fontFace: FONT_HEAD,
    fontSize: 28, bold: true, color: C.ink, align: "center",
  });
  const colors = [C.river, C.gold, C.leaf, C.cinnabar];
  const fills = [C.riverSoft, C.goldSoft, C.leafSoft, C.cinnabarSoft];
  for (let index = 0; index < 4; index += 1) {
    const x = 1.15 + index * 3.0;
    rect(slide, pres, x, 4.63, 2.56, 0.74, fills[index], colors[index], true, 0, 1.05);
    addText(slide, `${index + 1}`, { x: x + 0.15, y: 4.85, w: 0.35, h: 0.24, fontSize: 16, bold: true, color: colors[index], align: "center" });
    line(slide, pres, x + 0.67, 5.06, 1.48, colors[index], 1.1);
  }
  addText(slide, "自己先分，再把相连的意思合起来。", {
    x: 2.35, y: 5.67, w: 8.63, h: 0.36, fontSize: 21, color: C.muted, align: "center",
  });
  addText(slide, "一人读，一人听；交换，再读。", {
    x: 3.65, y: 6.34, w: 6.03, h: 0.38, fontSize: 21.5,
    color: C.muted, align: "center",
  });
  addNotes(slide, page);
}

function renderC105(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "再读第一章，把这场相遇讲完整", { color: C.paper });
  const poemLines = page.original_text.split("。").filter(Boolean).map((text) => `${text}。`);
  rect(slide, pres, 0.78, 1.2, 7.7, 4.85, C.night2, C.gold, true, 0, 1.05);
  poemLines.forEach((textValue, index) => addText(slide, textValue, {
    x: 1.03, y: 1.62 + index * 0.77, w: 7.2, h: 0.45,
    fontFace: FONT_TEXT, fontSize: 29, color: C.paper, align: "center",
  }));
  addText(slide, "合书讲30秒", {
    x: 8.88, y: 1.48, w: 3.82, h: 0.56, fontFace: FONT_HEAD,
    fontSize: 31, bold: true, color: C.gold, align: "center",
  });
  const prompts = ["他怎样来", "她怎样送", "婚事怎样暂缓又约定"];
  prompts.forEach((textValue, index) => {
    const y = 2.47 + index * 0.88;
    dot(slide, pres, 8.92, y + 0.08, 0.36, index === 0 ? C.gold : index === 1 ? C.river : C.cinnabar);
    addText(slide, `${index + 1}`, { x: 8.92, y: y + 0.12, w: 0.36, h: 0.2, fontSize: 13, bold: true, color: C.white, align: "center" });
    addText(slide, textValue, { x: 9.52, y, w: 3.0, h: 0.48, fontFace: FONT_HEAD, fontSize: index === 2 ? 21 : 24, bold: true, color: C.paper });
  });
  addText(slide, "听者只补一个真正遗漏", {
    x: 8.88, y: 5.4, w: 3.82, h: 0.38, fontSize: 20.5,
    color: C.riverSoft, align: "center",
  });
  addText(slide, "第一章", { x: 0.78, y: 6.45, w: 1.15, h: 0.3, fontSize: 17.5, bold: true, color: C.gold });
  for (let index = 0; index < 6; index += 1) {
    const x = 1.95 + index * 1.73;
    line(slide, pres, x, 6.74, 1.23, index === 0 ? C.gold : C.muted, index === 0 ? 2 : 1, index === 0 ? 0 : 35);
    addText(slide, `${index + 1}`, { x: x + 0.44, y: 6.36, w: 0.35, h: 0.24, fontSize: 14, color: index === 0 ? C.gold : C.muted, align: "center" });
  }
  addNotes(slide, page);
}

function validateObjects(pres, expectedSlides) {
  const errors = [];
  if (pres._slides.length !== expectedSlides) errors.push(`expected ${expectedSlides} slides, got ${pres._slides.length}`);
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
  const verification = validate(source);
  if (!verification.ok) throw new Error(`chapter1 contract failed: ${JSON.stringify(verification.errors)}`);
  if (!fs.existsSync(SNAPSHOT)) throw new Error(`missing snapshot: ${SNAPSHOT}`);
  const snapshot = JSON.parse(fs.readFileSync(SNAPSHOT, "utf8"));
  if (snapshot.source_sha256 !== sha256(path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "chapter_1.js"))) {
    throw new Error("snapshot is stale; rebuild markdown package first");
  }
  const pageMap = new Map(snapshot.pages.map((page) => [page.page_id, page]));
  const screenPlan = [
    ["C101", renderC101, "整章人物行动初读"],
    ["C102", renderC102, "贸丝到谋婚的叙事转折"],
    ["C103", renderC103, "送涉至的空间行迹"],
    ["C104", renderC104, "解释安抚约期的完整话轮"],
    ["C105", renderC105, "撤去局部支架后的故事重建"],
  ];
  const pages = screenPlan.map(([id, renderer, duty], index) => {
    const page = pageMap.get(id);
    if (!page) throw new Error(`snapshot missing ${id}`);
    return { ...page, renderer, duty, physicalIndex: index + 1 };
  });
  const pres = presentation();
  pages.forEach((page) => page.renderer(pres.addSlide(), pres, page));
  validateObjects(pres, pages.length);
  fs.mkdirSync(OUT, { recursive: true });
  await pres.writeFile({ fileName: PPTX, compression: true });
  await repairNotesMaster(PPTX);
  const manifest = {
    schema_version: "1.0", module_id: source.module_id, version: source.version,
    artifact: path.relative(PROJECT_ROOT, PPTX).split(path.sep).join("/"), sha256: sha256(PPTX),
    source_snapshot_sha256: sha256(SNAPSHOT),
    physical_slides: pages.map((page) => ({
      physical_index: page.physicalIndex, page_id: page.page_id,
      primary_visual_duty: page.duty, unique_function: page.unique_function,
    })),
    illustration_policy: "no_character_illustration_until_all_lesson_functions_are_frozen",
    claim_boundary: "chapter1_candidate_not_classroom_observed",
  };
  fs.writeFileSync(MANIFEST, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`V62_CHAPTER1_PPTX_OK slides=${pages.length} pptx=${PPTX}\n`);
}

main().catch((error) => { process.stderr.write(`${error.stack || error}\n`); process.exit(1); });
