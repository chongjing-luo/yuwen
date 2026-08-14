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
const source = require("./meng_v62/content/opening");
const { validate } = require("./verify_meng_v62_opening");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const SNAPSHOT = path.join(stageDir(), "opening", "package", "06_氓_V62导入课程数据快照.json");
const OUT = assertV62OutputPath(path.join(stageDir(), "opening", "pptx"));
const PPTX = assertV62OutputPath(path.join(OUT, "04_氓_V62导入课堂课件.pptx"));
const MANIFEST = assertV62OutputPath(path.join(OUT, "opening_pptx_manifest.json"));

const W = 13.333;
const H = 7.5;
const FONT_HEAD = "Noto Serif CJK SC";
const FONT_BODY = "Noto Sans CJK SC";
const FONT_TEXT = "Noto Serif CJK SC";
const C = {
  ink: "29241F", ink2: "51483F", paper: "F6F0E5", paper2: "FFFCF7",
  warm: "E5DAC9", warm2: "D2C1AA", cinnabar: "9C4538", cinnabarSoft: "F0DDD5",
  river: "456F7C", riverSoft: "DDE9E9", leaf: "647752", leafSoft: "E1E7D9",
  gold: "AC8550", white: "FFFFFF", muted: "766D63", night: "28241F", night2: "38312A",
};

function sha256(filePath) { return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex"); }

function presentation() {
  const pres = new pptxgen();
  pres.defineLayout({ name: "MENG_WIDE", width: W, height: H });
  pres.layout = "MENG_WIDE";
  pres.author = "语文备课系统";
  pres.company = "语文备课系统";
  pres.subject = "《氓》V6.2导入课堂课件";
  pres.title = "《氓》V6.2导入课堂课件";
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
    x, y, w, h,
    fill: { color: fill, transparency },
    line: { color: lineColor, width },
    ...(radius ? { rectRadius: 0.05 } : {}),
  });
}

function line(slide, pres, x, y, w, color, width = 1, transparency = 0) {
  slide.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width, transparency } });
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
    x: 0.76, y: 0.42, w: 11.82, h: 0.62,
    fontFace: FONT_HEAD, fontSize: 33, bold: true, ...options,
  });
}

function notesFor(page) {
  const s = page.script;
  const timeboxes = s.timeboxes.map((item) => `${item.label}：${item.seconds}秒`).join("；");
  const branches = s.branches.map((item) => `${item.kind}：${item.response}`).join("\n");
  return [
    `【V6.3页ID】${page.page_id}｜${page.title}｜${page.minutes}分钟`,
    "【本页不可替代的意义】", page.unique_function,
    "【删除本页会失去什么】", page.deletion_loss,
    "【教师逐字稿】", s.teacher_spoken,
    "【场面与走位】", s.scene, ...s.stage_directions.map((item) => `（${item}）`),
    "【时间盒】", timeboxes,
    "【现场分支】", branches,
    "【听者同步任务】", s.listener_task,
    "【证据位置】", s.evidence_location,
    "【回到人物和故事】", page.story_return,
    "【后续真实调用】", page.next_use,
    "【自然切页句】", s.cut_line,
    "【声明边界】桌面排演稿；不声称真实学生已经理解、参与或学会。",
  ].join("\n");
}

function addNotes(slide, page) { slide.addNotes(notesFor(page)); }

function renderO01(slide, pres, page) {
  base(slide, pres);
  title(slide, "我们还记得哪些爱情与婚姻故事？");
  addText(slide, "篇名", { x: 0.95, y: 1.4, w: 1.75, h: 0.4, fontFace: FONT_HEAD, fontSize: 22, bold: true, color: C.cinnabar });
  addText(slide, "一句话唤回故事", { x: 3.02, y: 1.4, w: 3.3, h: 0.4, fontFace: FONT_HEAD, fontSize: 22, bold: true, color: C.river });
  addText(slide, "它让我想到什么", { x: 8.0, y: 1.4, w: 3.4, h: 0.4, fontFace: FONT_HEAD, fontSize: 22, bold: true, color: C.leaf });
  for (let index = 0; index < 4; index += 1) {
    const y = 2.05 + index * 1.02;
    dot(slide, pres, 1.03, y + 0.07, 0.19, index === 0 ? C.cinnabar : C.gold);
    line(slide, pres, 1.43, y + 0.57, 1.15, C.warm2, 1);
    line(slide, pres, 3.02, y + 0.57, 4.28, C.warm2, 1);
    line(slide, pres, 8.0, y + 0.57, 3.78, C.warm2, 1);
  }
  addText(slide, "先写一篇；还能想起，继续往下写。", {
    x: 2.05, y: 6.48, w: 9.2, h: 0.34, fontFace: FONT_HEAD, fontSize: 21,
    color: C.muted, align: "center",
  });
  addNotes(slide, page);
}

function renderO02(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "一间教室，许多故事", { color: C.paper });
  rect(slide, pres, 0.95, 1.45, 11.43, 4.2, C.night2, C.gold, true, 0, 1.2);
  addText(slide, "《", {
    x: 1.58, y: 2.25, w: 0.42, h: 0.58, fontFace: FONT_HEAD, fontSize: 39,
    color: C.warm, align: "center",
  });
  line(slide, pres, 2.05, 2.79, 3.15, C.warm2, 1.2);
  addText(slide, "》", {
    x: 5.2, y: 2.25, w: 0.42, h: 0.58, fontFace: FONT_HEAD, fontSize: 39,
    color: C.warm, align: "center",
  });
  addText(slide, "让我想到爱情或婚姻中的", {
    x: 5.62, y: 2.22, w: 4.22, h: 0.58, fontFace: FONT_HEAD, fontSize: 22,
    color: C.gold, align: "center", bold: true,
  });
  line(slide, pres, 9.96, 2.79, 1.22, C.warm2, 1.2);
  addText(slide, "先把一篇作品，完整地说给身边的人听。", {
    x: 1.55, y: 4.26, w: 10.23, h: 0.52, fontFace: FONT_HEAD, fontSize: 27,
    color: C.paper, align: "center",
  });
  addNotes(slide, page);
}

function renderO03(slide, pres, page) {
  base(slide, pres, true);
  for (let index = 0; index < 9; index += 1) {
    const x = 0.7 + index * 1.5;
    dot(slide, pres, x, 1.2 + (index % 3) * 0.12, 0.11, index < 5 ? C.gold : C.river, 20);
  }
  slide.addShape(pres.shapes.ARC, {
    x: 1.04, y: 1.17, w: 11.25, h: 4.95,
    adjustPoint: 0.3, rotate: 0,
    fill: { color: C.night, transparency: 100 },
    line: { color: C.river, width: 2.2, transparency: 12 },
  });
  addText(slide, "相遇以后", {
    x: 1.05, y: 1.88, w: 11.23, h: 0.72, fontFace: FONT_HEAD, fontSize: 43,
    bold: true, color: C.paper, align: "center",
  });
  addText(slide, "爱情走进共同生活，\n日子会怎样改变两个人？", {
    x: 1.05, y: 3.12, w: 11.23, h: 1.35, fontFace: FONT_HEAD, fontSize: 39,
    bold: true, color: C.warm, align: "center",
  });
  addNotes(slide, page);
}

function renderO04(slide, pres, page) {
  base(slide, pres, true);
  dot(slide, pres, 6.31, 1.18, 0.7, C.cinnabar, 10);
  addText(slide, "氓", {
    x: 0.9, y: 1.5, w: 11.53, h: 2.4, fontFace: FONT_HEAD, fontSize: 110,
    bold: true, color: C.paper, align: "center",
  });
  addText(slide, "méng", {
    x: 4.85, y: 4.15, w: 3.63, h: 0.48, fontSize: 25, color: C.gold,
    charSpacing: 3.5, align: "center",
  });
  addText(slide, "《诗经·卫风》", {
    x: 3.6, y: 5.15, w: 6.13, h: 0.55, fontFace: FONT_HEAD, fontSize: 28,
    color: C.warm, align: "center",
  });
  addNotes(slide, page);
}

function renderQuestionBookmark(slide, pres, page) {
  base(slide, pres);
  title(slide, "读懂六章，我们要回答什么？");
  const questions = [
    ["一", "她经历了什么？", C.gold, "EEE3D2"],
    ["二", "她婚后的不幸，\n在生活中是什么样子？", C.river, C.riverSoft],
    ["三", "这场婚姻为什么\n走到这一步？", C.cinnabar, C.cinnabarSoft],
  ];
  questions.forEach(([label, question, color, fill], index) => {
    const x = 0.82 + index * 4.18;
    rect(slide, pres, x, 1.55, 3.75, 4.62, fill, color, true, 0, 1.2);
    rect(slide, pres, x + 1.43, 1.55, 0.9, 0.7, color, color, false);
    slide.addShape(pres.shapes.CHEVRON, {
      x: x + 1.43, y: 2.02, w: 0.9, h: 0.68,
      fill: { color }, line: { color }, rotate: 90,
    });
    addText(slide, label, { x: x + 1.43, y: 1.72, w: 0.9, h: 0.3, fontSize: 21, bold: true, color: C.white, align: "center" });
    addText(slide, question, {
      x: x + 0.38, y: 3.05, w: 2.99, h: 1.55, fontFace: FONT_HEAD,
      fontSize: index === 0 ? 31 : 28, bold: true, color: C.ink,
      align: "center", valign: "mid", breakLine: true,
    });
  });
  addNotes(slide, page);
}

function addPoemSlide(slide, pres, page, startIndex) {
  base(slide, pres);
  addText(slide, page.title, {
    x: 0.74, y: 0.32, w: 6.7, h: 0.43, fontFace: FONT_HEAD,
    fontSize: 25, bold: true, color: C.cinnabar,
  });
  addText(slide, "眼随声走", {
    x: 9.8, y: 0.38, w: 2.8, h: 0.33, fontFace: FONT_HEAD,
    fontSize: 19, bold: true, color: C.river, align: "right",
  });
  line(slide, pres, 0.74, 0.84, 11.86, C.warm2, 1);
  const accents = startIndex === 0 ? [C.gold, C.river, C.leaf] : [C.leaf, C.cinnabar, C.river];
  source.chapters.slice(startIndex, startIndex + 3).forEach((chapter, index) => {
    const y = 1.02 + index * 2.05;
    rect(slide, pres, 0.74, y, 11.86, 1.8, index % 2 === 0 ? "FAF6EE" : C.paper2, index % 2 === 0 ? "FAF6EE" : C.paper2, true);
    rect(slide, pres, 0.74, y + 0.16, 0.08, 1.48, accents[index], accents[index]);
    addText(slide, chapter.chapter, {
      x: 0.92, y: y + 0.2, w: 0.82, h: 0.3, fontSize: 17.5,
      bold: true, color: accents[index], align: "center",
    });
    addText(slide, chapter.lines.map((text, row) => ({ text, options: { breakLine: row < 2 } })), {
      x: 1.83, y: y + 0.13, w: 10.25, h: 1.5, fontFace: FONT_TEXT,
      fontSize: 26.5, color: C.ink, breakLine: true, breakLineOnTextOverflow: false,
      lineSpacingMultiple: 0.92, valign: "mid",
    });
  });
  addNotes(slide, page);
}

function renderO05(slide, pres, page) { addPoemSlide(slide, pres, page, 0); }
function renderO06(slide, pres, page) { addPoemSlide(slide, pres, page, 3); }

function renderO07(slide, pres, page) {
  base(slide, pres);
  title(slide, "把第一次听见的《氓》留在纸上");
  addText(slide, "“", { x: 0.95, y: 1.48, w: 0.72, h: 0.85, fontFace: FONT_HEAD, fontSize: 72, color: C.cinnabar, align: "center" });
  addText(slide, "”", { x: 11.7, y: 2.35, w: 0.72, h: 0.85, fontFace: FONT_HEAD, fontSize: 72, color: C.cinnabar, align: "center" });
  line(slide, pres, 1.72, 2.55, 9.86, C.warm2, 1.4);
  line(slide, pres, 1.72, 3.26, 9.86, C.warm2, 1.4);
  addText(slide, "我看见／我听见／我想问", {
    x: 1.05, y: 4.2, w: 4.2, h: 0.48, fontFace: FONT_HEAD, fontSize: 27,
    bold: true, color: C.river,
  });
  line(slide, pres, 1.05, 5.13, 11.12, C.warm2, 1.2);
  line(slide, pres, 1.05, 6.0, 11.12, C.warm2, 1.2);
  addNotes(slide, page);
}

function renderO08(slide, pres, page) { renderQuestionBookmark(slide, pres, page); }

function renderO09(slide, pres, page) {
  base(slide, pres);
  title(slide, "这首诗，收在哪里？谁在说话？");
  addText(slide, "出处", {
    x: 0.82, y: 1.38, w: 1.15, h: 0.42, fontFace: FONT_HEAD, fontSize: 24,
    bold: true, color: C.gold, align: "center",
  });
  const sourceNodes = [
    ["《诗经》", 1.72, 2.35, C.gold, "EEE2D0", 1.85],
    ["风", 4.25, 2.34, C.leaf, C.leafSoft, 1.05],
    ["《卫风》", 6.0, 2.35, C.river, C.riverSoft, 1.85],
    ["《氓》", 8.55, 2.35, C.cinnabar, C.cinnabarSoft, 1.85],
  ];
  sourceNodes.forEach(([label, x, y, color, fill, w], index) => {
    rect(slide, pres, x, 1.95, w, 1.2, fill, color, true, 0, 1.2);
    addText(slide, label, {
      x, y, w, h: 0.42, fontFace: FONT_HEAD, fontSize: index === 1 ? 29 : 28,
      bold: true, color, align: "center",
    });
    if (index < sourceNodes.length - 1) {
      const nextX = sourceNodes[index + 1][1];
      addText(slide, "→", {
        x: x + w + 0.14, y: 2.34, w: nextX - x - w - 0.28, h: 0.38,
        fontSize: 26, color: C.muted, align: "center",
      });
    }
  });
  addText(slide, "我国最早的诗歌总集，共305篇｜分风、雅、颂", {
    x: 1.68, y: 3.42, w: 8.78, h: 0.38, fontFace: FONT_HEAD, fontSize: 20,
    color: C.muted, align: "center",
  });
  line(slide, pres, 0.9, 4.15, 11.55, C.warm2, 1);
  addText(slide, "诗中谁在说话？", {
    x: 0.95, y: 4.72, w: 2.65, h: 0.44, fontFace: FONT_HEAD, fontSize: 25,
    bold: true, color: C.cinnabar,
  });
  rect(slide, pres, 3.92, 4.46, 8.15, 1.42, C.cinnabarSoft, C.cinnabar, true, 0, 1.2);
  addText(slide, "一位女子，用第一人称回望自己的婚姻", {
    x: 4.25, y: 4.78, w: 7.49, h: 0.56, fontFace: FONT_HEAD, fontSize: 29,
    bold: true, color: C.cinnabar, align: "center",
  });
  addText(slide, "这是《氓》里的讲述声音", {
    x: 5.2, y: 5.4, w: 5.59, h: 0.3, fontSize: 18.5,
    color: C.ink2, align: "center",
  });
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
  if (!verification.ok) throw new Error(`opening contract failed: ${JSON.stringify(verification.errors)}`);
  if (!fs.existsSync(SNAPSHOT)) throw new Error(`missing snapshot: ${SNAPSHOT}`);
  const snapshot = JSON.parse(fs.readFileSync(SNAPSHOT, "utf8"));
  if (snapshot.source_sha256 !== sha256(path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "opening.js"))) {
    throw new Error("snapshot is stale; rebuild markdown package first");
  }
  const pageMap = new Map(snapshot.pages.map((page) => [page.page_id, page]));
  const screenPlan = [
    ["O01", renderO01, "开放书写"],
    ["O02", renderO02, "并行表达与公共文学长卷"],
    ["O03", renderO03, "据实归纳后的新问题"],
    ["O04", renderO04, "题名聚拢"],
    ["O05", renderO05, "原诗听读"],
    ["O06", renderO06, "原诗听读"],
    ["O07", renderO07, "初听留痕"],
    ["O08", renderO08, "读后三问"],
    ["O09", renderO09, "文本身份"],
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
    schema_version: "1.0",
    module_id: source.module_id,
    version: source.version,
    artifact: path.relative(PROJECT_ROOT, PPTX).split(path.sep).join("/"),
    sha256: sha256(PPTX),
    source_snapshot_sha256: sha256(SNAPSHOT),
    physical_slides: pages.map((page) => ({
      physical_index: page.physicalIndex,
      page_id: page.page_id,
      primary_visual_duty: page.duty,
      unique_function: page.unique_function,
    })),
    illustration_policy: "no_character_illustration_until_function_freeze",
    claim_boundary: "rendered_opening_not_classroom_observed",
  };
  fs.writeFileSync(MANIFEST, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`V62_OPENING_PPTX_OK slides=${pages.length} pptx=${PPTX}\n`);
}

main().catch((error) => { process.stderr.write(`${error.stack || error}\n`); process.exit(1); });
