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
const lesson = require("./meng_v65/lesson");

const PROJECT_ROOT = path.resolve(__dirname, "..");
const OUT_DIR = path.join(PROJECT_ROOT, "work", "备课", "选择性必修下册", "氓", "_v62_stage", "v65", "pptx");
const outputPath = path.join(OUT_DIR, "04_氓_V65完整课堂课件_45页无插图逐字稿_V4.pptx");
const manifestPath = path.join(OUT_DIR, "v65_no_image_manifest.json");
const W = 13.333;
const H = 7.5;

const FONT_SERIF = "Noto Serif CJK SC";
const FONT_SANS = "Noto Sans CJK SC";
const C = {
  ink: "29241F", ink2: "51483F", muted: "7B7167",
  paper: "F5EFE4", paper2: "FFFCF7", warm: "DED0BC", warm2: "C5B39B",
  red: "94473B", redSoft: "EFDDD5", plum: "725260", plumSoft: "E9DDE2",
  river: "446E78", riverSoft: "DCE9E8", leaf: "657653", leafSoft: "E1E7D9",
  gold: "A67F4A", goldSoft: "EFE3CF", night: "28231F", night2: "383129",
  white: "FFFDFC", yellow: "B58B3E", yellowSoft: "F0E4C8",
};

const moduleMeta = {
  opening: ["初见", C.gold],
  chapter_1: ["第一章", C.gold],
  chapter_2: ["第二章", C.river],
  chapter_3: ["第三章", C.leaf],
  chapter_4: ["第四章", C.yellow],
  chapter_5: ["第五章", C.plum],
  chapter_6: ["第六章", C.red],
  synthesis: ["全文", C.ink2],
};

function sha256(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function presentation() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: "MENG_V65_WIDE", width: W, height: H });
  pptx.layout = "MENG_V65_WIDE";
  pptx.author = "语文备课系统";
  pptx.subject = "《诗经·卫风·氓》完整课堂课件；无插图功能审查候选";
  pptx.title = "《氓》V6.5完整课堂课件";
  pptx.company = "语文备课系统";
  pptx.lang = "zh-CN";
  pptx.theme = { headFontFace: FONT_SERIF, bodyFontFace: FONT_SANS, lang: "zh-CN" };
  return pptx;
}

function addText(slide, value, options = {}) {
  slide.addText(value, {
    x: 0.8, y: 0.5, w: 11.8, h: 0.5, margin: 0,
    fontFace: FONT_SANS, fontSize: 27, color: C.ink, valign: "mid",
    breakLine: false, ...options,
  });
}

function rect(slide, pptx, x, y, w, h, fill, line = fill, rounded = false, width = 1) {
  slide.addShape(rounded ? pptx.shapes.ROUNDED_RECTANGLE : pptx.shapes.RECTANGLE, {
    x, y, w, h,
    fill: { color: fill }, line: { color: line, width },
    ...(rounded ? { rectRadius: 0.05 } : {}),
  });
}

function line(slide, pptx, x, y, w, color, width = 1, dashType = "solid") {
  slide.addShape(pptx.shapes.LINE, { x, y, w, h: 0, line: { color, width, dashType } });
}

function base(slide, pptx, page, options = {}) {
  const [moduleLabel, accent] = moduleMeta[page.module];
  const dark = Boolean(options.dark);
  slide.background = { color: dark ? C.night : C.paper };
  rect(slide, pptx, 0, 0, 0.15, H, accent);
  addText(slide, moduleLabel, {
    x: 0.48, y: 0.34, w: 1.05, h: 0.28,
    fontSize: 15.5, bold: true, color: dark ? C.warm : accent,
  });
  addText(slide, String(page.page_number).padStart(2, "0"), {
    x: 11.95, y: 0.34, w: 0.72, h: 0.28,
    fontSize: 14.5, bold: true, color: dark ? C.warm2 : C.muted, align: "right",
  });
}

function title(slide, page, options = {}) {
  addText(slide, page.title, {
    x: 0.82, y: 0.72, w: 11.7, h: 0.64,
    fontFace: FONT_SERIF, fontSize: options.size || 34, bold: true,
    color: options.dark ? C.white : C.ink, align: options.align || "left",
  });
}

function splitPoem(text) {
  if (!text) return [];
  return text.match(/[^。！？]+[。！？]?/gu)?.map((item) => item.trim()).filter(Boolean) || [text];
}

function poemBlock(slide, pptx, page, lines, options = {}) {
  const dark = Boolean(options.dark);
  const fill = options.fill || (dark ? C.night2 : C.paper2);
  const border = options.border || moduleMeta[page.module][1];
  const x = options.x ?? 0.85;
  const y = options.y ?? 1.48;
  const w = options.w ?? 11.65;
  const h = options.h ?? 3.9;
  rect(slide, pptx, x, y, w, h, fill, border, true, 1.15);
  const count = lines.length;
  const fontSize = options.fontSize || (count <= 2 ? 38 : count <= 4 ? 31 : 27);
  const lineHeight = Math.min(0.72, (h - 0.48) / Math.max(count, 1));
  const totalHeight = lineHeight * count;
  const startY = y + (h - totalHeight) / 2;
  lines.forEach((value, index) => {
    addText(slide, value, {
      x: x + 0.28, y: startY + index * lineHeight, w: w - 0.56, h: lineHeight * 0.82,
      fontFace: FONT_SERIF, fontSize, bold: options.bold ?? false,
      color: dark ? C.white : C.ink, align: "center",
    });
  });
}

function prompt(slide, value, options = {}) {
  addText(slide, value, {
    x: options.x ?? 1.0, y: options.y ?? 6.05, w: options.w ?? 11.33, h: options.h ?? 0.64,
    fontFace: FONT_SERIF, fontSize: options.fontSize || 27, bold: options.bold ?? true,
    color: options.color || C.plum, align: options.align || "center",
  });
}

function notesFor(page) {
  const script = page.script;
  return [
    `【V6.5页ID】${page.page_id}｜物理页${page.page_number}｜${page.minutes}分钟`,
    "【页面功能】", page.unique_function,
    "【学生主动作】", page.student_action.join("；"),
    "【可见产物】", page.artifact,
    "【首次后用】", page.next_use,
    "【删除损失】", page.deletion_loss,
    "【主视觉职责】", page.visual_duty,
    "【插图资格】", page.illustration_eligibility,
    "【教师逐字稿】", script.teacher_spoken,
    "【真实场景】", script.scene,
    ...script.stage_directions.map((item) => `（${item}）`),
    "【时间盒】", script.timeboxes.map((item) => `${item.label}：${item.seconds}秒`).join("；"),
    "【现场分支】", script.branches.map((item) => `${item.kind}：${item.response}`).join("\n"),
    "【听者任务】", script.listener_task,
    "【证据位置】", script.evidence_location,
    "【自然切页句】", script.cut_line,
    "【声明边界】无插图桌面排演候选；不声称真实课堂或学习效果已通过。",
  ].join("\n");
}

function addNotes(slide, page) {
  slide.addNotes(notesFor(page));
}

function renderO01(slide, pptx, page) {
  base(slide, pptx, page);
  title(slide, page, { size: 38 });
  prompt(slide, "从小学想到高中：课文、小说、整本书……", { y: 1.62, color: C.gold, fontSize: 26 });
  const rows = ["篇名", "一句话唤回故事", "它谈到怎样的相遇或共同生活？"];
  rows.forEach((label, index) => {
    const y = 2.45 + index * 1.15;
    addText(slide, label, { x: 1.12, y, w: 3.2, h: 0.45, fontFace: FONT_SERIF, fontSize: 24, bold: true, color: index === 2 ? C.plum : C.ink2 });
    line(slide, pptx, 4.2, y + 0.38, 7.8, index === 2 ? C.plumSoft : C.warm, 1.5);
  });
  prompt(slide, "先写一篇；还能想起，就继续往下写。", { y: 6.25, color: C.ink, fontSize: 25 });
  addNotes(slide, page);
}

function renderO02(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true, size: 38 });
  addText(slide, "《　　　　　　》让我想到爱情或婚姻中的　　　　　　　　　。", {
    x: 1.1, y: 1.75, w: 11.05, h: 0.72, fontFace: FONT_SERIF, fontSize: 31, bold: true, color: C.goldSoft, align: "center",
  });
  line(slide, pptx, 1.05, 3.4, 11.1, C.warm2, 1.2);
  const nodes = ["身边说", "合并不同", "带来一条新篇目或新说法"];
  nodes.forEach((label, index) => {
    const x = 1.1 + index * 4.02;
    slide.addShape(pptx.shapes.OVAL, { x, y: 4.05, w: 2.7, h: 1.2, fill: { color: index === 2 ? C.plum : C.night2 }, line: { color: index === 0 ? C.gold : index === 1 ? C.river : C.plumSoft, width: 1.6 } });
    addText(slide, label, { x: x + 0.18, y: 4.38, w: 2.34, h: 0.52, fontFace: FONT_SERIF, fontSize: 21, bold: true, color: C.white, align: "center" });
    if (index < 2) line(slide, pptx, x + 2.7, 4.65, 1.32, C.warm2, 1.4);
  });
  prompt(slide, "让教室里的文学版图，从你们的话里长出来。", { y: 6.15, color: C.warm, fontSize: 27 });
  addNotes(slide, page);
}

function renderO03(slide, pptx, page) {
  base(slide, pptx, page);
  title(slide, page, { align: "center", size: 42 });
  rect(slide, pptx, 1.0, 1.85, 11.33, 3.75, C.paper2, C.gold, true, 1.2);
  addText(slide, "爱情走进共同生活，", { x: 1.5, y: 2.55, w: 10.33, h: 0.72, fontFace: FONT_SERIF, fontSize: 38, bold: true, color: C.ink, align: "center" });
  addText(slide, "日子会怎样改变两个人？", { x: 1.5, y: 3.65, w: 10.33, h: 0.8, fontFace: FONT_SERIF, fontSize: 44, bold: true, color: C.plum, align: "center" });
  prompt(slide, "先让旧故事留在黑板上。新的故事，由一位女子自己说。", { y: 6.12, color: C.muted, fontSize: 23 });
  addNotes(slide, page);
}

function renderO04(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  addText(slide, "氓", { x: 1.5, y: 2.0, w: 10.33, h: 1.5, fontFace: FONT_SERIF, fontSize: 78, bold: true, color: C.white, align: "center" });
  addText(slide, "méng", { x: 4.5, y: 3.55, w: 4.33, h: 0.45, fontSize: 22, color: C.goldSoft, align: "center", charSpacing: 3 });
  addText(slide, "《诗经·卫风》", { x: 3.2, y: 4.6, w: 6.93, h: 0.55, fontFace: FONT_SERIF, fontSize: 28, color: C.warm, align: "center" });
  addNotes(slide, page);
}

function renderListening(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true, size: 31 });
  poemBlock(slide, pptx, page, splitPoem(page.literary_object.includes("第一至第三") ? [
    "氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。", "送子涉淇，至于顿丘。匪我愆期，子无良媒。", "将子无怒，秋以为期。", "乘彼垝垣，以望复关。不见复关，泣涕涟涟。", "既见复关，载笑载言。尔卜尔筮，体无咎言。", "以尔车来，以我贿迁。", "桑之未落，其叶沃若。于嗟鸠兮，无食桑葚！", "于嗟女兮，无与士耽！士之耽兮，犹可说也。", "女之耽兮，不可说也！",
  ].join("") : [
    "桑之落矣，其黄而陨。自我徂尔，三岁食贫。", "淇水汤汤，渐车帷裳。女也不爽，士贰其行。", "士也罔极，二三其德。", "三岁为妇，靡室劳矣。夙兴夜寐，靡有朝矣。", "言既遂矣，至于暴矣。兄弟不知，咥其笑矣。", "静言思之，躬自悼矣。", "及尔偕老，老使我怨。淇则有岸，隰则有泮。", "总角之宴，言笑晏晏。信誓旦旦，不思其反。", "反是不思，亦已焉哉！",
  ].join("")), { dark: true, y: 1.35, h: 5.25, fontSize: 23, border: page.page_id === "O05" ? C.gold : C.plum });
  addNotes(slide, page);
}

function renderO07(slide, pptx, page) {
  base(slide, pptx, page);
  title(slide, page, { size: 36 });
  rect(slide, pptx, 1.05, 1.72, 11.2, 2.1, C.paper2, C.warm2, true, 1.1);
  addText(slide, "“　　　　　　　　　　　　　　　　　　　　　　　　”", { x: 1.45, y: 2.35, w: 10.4, h: 0.65, fontFace: FONT_SERIF, fontSize: 34, color: C.ink, align: "center" });
  const labels = [["我看见", C.gold], ["我听见", C.river], ["我想问", C.plum]];
  labels.forEach(([label, color], index) => {
    const x = 1.15 + index * 4.0;
    addText(slide, label, { x, y: 4.65, w: 2.1, h: 0.5, fontFace: FONT_SERIF, fontSize: 25, bold: true, color, align: "center" });
    line(slide, pptx, x + 0.05, 5.5, 2.0, color, 1.3);
  });
  prompt(slide, "只留下一处真正让你停住的声音。", { y: 6.2, color: C.ink, fontSize: 25 });
  addNotes(slide, page);
}

function renderO08(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true, size: 37 });
  const qs = ["她经历了什么？", "她婚后的不幸，在生活中是什么样子？", "这场婚姻为什么走到这一步？"];
  qs.forEach((value, index) => {
    const y = 1.72 + index * 1.55;
    addText(slide, String(index + 1), { x: 1.25, y: y + 0.05, w: 0.55, h: 0.55, fontFace: FONT_SERIF, fontSize: 26, bold: true, color: [C.goldSoft, C.riverSoft, C.plumSoft][index], align: "center" });
    line(slide, pptx, 2.05, y + 0.34, 0.75, [C.gold, C.river, C.plum][index], 2.4);
    addText(slide, value, { x: 3.05, y, w: 8.65, h: 0.72, fontFace: FONT_SERIF, fontSize: 34, bold: true, color: C.white });
  });
  prompt(slide, "先跟着事情走，再看日子，最后追问原因。", { y: 6.32, color: C.warm, fontSize: 24 });
  addNotes(slide, page);
}

const prompts = {
  C101: "圈一圈他做的事｜划一划她做的事",
  C102: "诗先写什么？女子随后说明什么？哪个字让话转了弯？",
  C103: "送　　涉　　至｜让三个动作连续发生。",
  C104: "说明条件｜安抚对方｜另约婚期｜把四句读成一轮话。",
  C105: "合书讲清：他怎样来，她怎样送，两个人怎样约。",
  C201: "乘—望—不见｜她站在哪里，目光投向哪里？",
  C202: "不见 → 泣涕｜既见 → 笑言｜让转折先从原词里响起来。",
  C204: "卜筮无咎 → 车来 → 贿迁｜谁的动作？怎样相接？",
  C206: "第一章：来—送—约｜第二章：等—见—迁",
  C301: "故事刚走到迁嫁，为什么先让一树桑叶进入眼前？",
  C302: "色泽｜质地｜生命感｜先留下感受，再留下可能。",
  C303: "桑 → 鸠 → 女｜两声‘于嗟’，怎样由物及人？",
  C305: "相同的词是什么？真正改变脱身处境的词是什么？",
  C306: "迁嫁以后——桑叶、斑鸠、女子的劝告｜这是谁的回望？",
  C401: "圈桑叶的新状态｜画生活事实｜框第一处责任判断",
  C402: "翻回原来的想法：保留、改写，还是撤回？",
  C403: "一句压着多年｜一句展开渡水的一刻",
  C404_405: "不爽 → 贰行 → 罔极 → 二三其德｜这些词怎样一步步加重？",
  C406: "物象变化｜婚后生活｜责任判断｜把三层连成一段。",
  C501: "谁在忙？谁在笑？谁在独自思量？",
  C502: "把一天的首尾，叠进许多重复的日子。",
  C503: "现在能说明什么？仍不能断言什么？",
  C504: "外声　—　三秒沉默　—　内声",
  C505: "请写40—60字：一间屋子里的许多年。",
  C601: "她把哪些旧愿、旧事和誓言重新放回眼前？",
  C602: "第一个‘老’落在旧愿里；第二个‘老’落在怎样的现实里？",
  C603: "先看清有岸、有泮的地貌，再用前后文托住解释。",
  C604: "旧日确有欢乐誓言｜后来行为仍要接受核验",
  C605: "诗写到什么？没有写到什么？让末句停在证据边界上。",
  C606_S01: "每组为一章留下人物、动作和转折；长卷完成后再画因果箭头。",
};

const fullChapterIds = new Set(["C101", "C201", "C301", "C401", "C501", "C601"]);

function renderChapterPage(slide, pptx, page) {
  const isSummary = ["C105", "C206", "C306", "C406", "C505", "C606_S01"].includes(page.page_id);
  const dark = isSummary || page.page_id === "C504";
  base(slide, pptx, page, { dark });
  title(slide, page, { dark, size: page.title.length > 18 ? 29 : 34 });
  let poem = splitPoem(page.original_text || "");
  if (page.page_id === "C606_S01") poem = [];
  if (poem.length) {
    poemBlock(slide, pptx, page, poem, {
      dark, y: 1.43, h: fullChapterIds.has(page.page_id) ? 4.65 : 3.45,
      fontSize: fullChapterIds.has(page.page_id) ? 28 : poem.length <= 2 ? 39 : 31,
    });
  } else {
    const stages = ["第一章", "第二章", "第三章", "第四章", "第五章", "第六章"];
    line(slide, pptx, 1.15, 3.75, 11.0, C.warm2, 1.4);
    stages.forEach((label, index) => {
      const x = 0.72 + index * 2.08;
      slide.addShape(pptx.shapes.OVAL, { x, y: 3.2, w: 1.42, h: 1.05, fill: { color: index === 5 ? C.plum : C.night2 }, line: { color: [C.gold, C.river, C.leaf, C.yellow, C.plum, C.red][index], width: 1.6 } });
      addText(slide, label, { x: x + 0.08, y: 3.48, w: 1.26, h: 0.46, fontFace: FONT_SERIF, fontSize: 16.5, bold: true, color: C.white, align: "center" });
    });
  }
  prompt(slide, prompts[page.page_id], {
    y: fullChapterIds.has(page.page_id) ? 6.28 : 5.55,
    h: fullChapterIds.has(page.page_id) ? 0.55 : 0.82,
    color: dark ? C.goldSoft : moduleMeta[page.module][1],
    fontSize: page.page_id === "C606_S01" ? 24 : 26,
  });
  addNotes(slide, page);
}

function renderWordTurn(slide, pptx, page) {
  base(slide, pptx, page);
  title(slide, page);
  addText(slide, "抱布贸丝", { x: 1.05, y: 2.0, w: 3.35, h: 0.72, fontFace: FONT_SERIF, fontSize: 42, bold: true, color: C.gold, align: "center" });
  addText(slide, "匪", { x: 5.32, y: 1.92, w: 1.3, h: 0.9, fontFace: FONT_SERIF, fontSize: 52, bold: true, color: C.red, align: "center" });
  addText(slide, "来即我谋", { x: 7.05, y: 2.0, w: 4.35, h: 0.72, fontFace: FONT_SERIF, fontSize: 42, bold: true, color: C.plum, align: "center" });
  line(slide, pptx, 1.5, 3.25, 9.95, C.warm2, 1.4);
  addText(slide, "诗先让我们看见的动作", { x: 1.25, y: 3.65, w: 3.7, h: 0.5, fontFace: FONT_SERIF, fontSize: 23, color: C.ink2, align: "center" });
  addText(slide, "话在这里转弯", { x: 4.95, y: 3.65, w: 2.0, h: 0.5, fontFace: FONT_SERIF, fontSize: 23, bold: true, color: C.red, align: "center" });
  addText(slide, "女子随后说明的来意", { x: 7.15, y: 3.65, w: 4.0, h: 0.5, fontFace: FONT_SERIF, fontSize: 23, color: C.ink2, align: "center" });
  prompt(slide, "先说成自己的自然话：此刻能看见什么，还不能断言什么？", { y: 5.5, color: C.ink, fontSize: 28 });
  addNotes(slide, page);
}

function renderActionRoad(slide, pptx, page) {
  base(slide, pptx, page);
  title(slide, page);
  const words = [["送", C.gold], ["涉", C.river], ["至", C.plum]];
  line(slide, pptx, 1.65, 3.52, 10.0, C.warm2, 2.2);
  words.forEach(([word, color], index) => {
    const x = 1.35 + index * 4.65;
    slide.addShape(pptx.shapes.OVAL, { x, y: 2.62, w: 1.75, h: 1.75, fill: { color: C.paper2 }, line: { color, width: 2.5 } });
    addText(slide, word, { x, y: 3.04, w: 1.75, h: 0.65, fontFace: FONT_SERIF, fontSize: 42, bold: true, color, align: "center" });
  });
  addText(slide, "淇水", { x: 5.55, y: 4.4, w: 2.2, h: 0.45, fontFace: FONT_SERIF, fontSize: 22, color: C.river, align: "center" });
  addText(slide, "顿丘", { x: 10.0, y: 4.4, w: 2.2, h: 0.45, fontFace: FONT_SERIF, fontSize: 22, color: C.plum, align: "center" });
  prompt(slide, "不用‘她很投入’替代这段路。让三个动词自己走起来。", { y: 5.75, color: C.ink, fontSize: 27 });
  addNotes(slide, page);
}

function renderSpeechSequence(slide, pptx, page) {
  base(slide, pptx, page);
  title(slide, page);
  const blocks = [
    ["匪我愆期，子无良媒。", C.goldSoft, C.gold],
    ["将子无怒，", C.riverSoft, C.river],
    ["秋以为期。", C.plumSoft, C.plum],
  ];
  blocks.forEach(([verse, fill, color], index) => {
    const x = 0.85 + index * 4.15;
    rect(slide, pptx, x, 1.85, 3.65, 2.55, fill, color, true, 1.2);
    addText(slide, verse, { x: x + 0.25, y: 2.25, w: 3.15, h: 0.8, fontFace: FONT_SERIF, fontSize: 28, bold: true, color: C.ink, align: "center" });
    line(slide, pptx, x + 0.55, 3.7, 2.55, color, 1.25, "dash");
  });
  prompt(slide, "先说成自己的话，再试着分一分：她怎样把婚事继续说下去？", { y: 5.45, color: C.ink, fontSize: 27 });
  addNotes(slide, page);
}

function renderContrast(slide, pptx, page, left, right, footer) {
  base(slide, pptx, page);
  title(slide, page);
  const sides = [[left, C.riverSoft, C.river], [right, C.plumSoft, C.plum]];
  sides.forEach(([data, fill, color], index) => {
    const x = 0.85 + index * 6.1;
    rect(slide, pptx, x, 1.62, 5.55, 3.75, fill, color, true, 1.2);
    addText(slide, data.head, { x: x + 0.3, y: 2.0, w: 4.95, h: 0.62, fontFace: FONT_SERIF, fontSize: 31, bold: true, color, align: "center" });
    addText(slide, data.body, { x: x + 0.35, y: 3.05, w: 4.85, h: 1.15, fontFace: FONT_SERIF, fontSize: 27, color: C.ink, align: "center", valign: "mid" });
  });
  prompt(slide, footer, { y: 5.86, color: C.ink, fontSize: 26 });
  addNotes(slide, page);
}

function renderFlow(slide, pptx, page, nodes, footer) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true });
  line(slide, pptx, 1.25, 3.65, 10.8, C.warm2, 1.6);
  nodes.forEach(([head, sub, color], index) => {
    const x = 1.1 + index * (9.4 / (nodes.length - 1 || 1));
    slide.addShape(pptx.shapes.OVAL, { x, y: 3.07, w: 1.15, h: 1.15, fill: { color }, line: { color } });
    addText(slide, head, { x: x - 0.4, y: 2.25, w: 1.95, h: 0.45, fontFace: FONT_SERIF, fontSize: 24, bold: true, color: C.white, align: "center" });
    if (sub) addText(slide, sub, { x: x - 0.5, y: 4.45, w: 2.15, h: 0.7, fontSize: 18, color: C.warm, align: "center" });
  });
  prompt(slide, footer, { y: 5.9, color: C.goldSoft, fontSize: 27 });
  addNotes(slide, page);
}

function renderSingleVerse(slide, pptx, page, verse, question, color) {
  base(slide, pptx, page);
  title(slide, page);
  addText(slide, verse, { x: 1.0, y: 2.1, w: 11.33, h: 1.05, fontFace: FONT_SERIF, fontSize: 52, bold: true, color, align: "center" });
  line(slide, pptx, 2.6, 3.65, 8.13, C.warm, 1.2);
  prompt(slide, question, { y: 4.65, color: C.ink, fontSize: 29 });
  addNotes(slide, page);
}

function renderObjectToPerson(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true, size: 32 });
  addText(slide, "于嗟女兮，无与士耽！", { x: 1.0, y: 1.85, w: 11.33, h: 0.9, fontFace: FONT_SERIF, fontSize: 45, bold: true, color: C.plumSoft, align: "center" });
  rect(slide, pptx, 1.15, 3.25, 4.95, 1.25, C.night2, C.plum, true, 1.2);
  rect(slide, pptx, 7.2, 3.25, 4.95, 1.25, C.night2, C.gold, true, 1.2);
  addText(slide, "只读这一句", { x: 1.45, y: 3.48, w: 4.35, h: 0.38, fontFace: FONT_SERIF, fontSize: 24, bold: true, color: C.white, align: "center" });
  addText(slide, "声音怎样落下？", { x: 1.45, y: 3.91, w: 4.35, h: 0.36, fontFace: FONT_SERIF, fontSize: 21, color: C.plumSoft, align: "center" });
  addText(slide, "再恢复前两句", { x: 7.5, y: 3.48, w: 4.35, h: 0.38, fontFace: FONT_SERIF, fontSize: 24, bold: true, color: C.white, align: "center" });
  addText(slide, "你又多听见了什么？", { x: 7.5, y: 3.91, w: 4.35, h: 0.36, fontFace: FONT_SERIF, fontSize: 21, color: C.goldSoft, align: "center" });
  prompt(slide, "先遮住，再恢复；请让原词替你回答。", { y: 5.55, color: C.goldSoft, fontSize: 28 });
  addNotes(slide, page);
}

function renderResponsibility(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true, size: 31 });
  const words = [["不爽", C.gold], ["二三其德", C.plum], ["贰行", C.river], ["罔极", C.red]];
  words.forEach(([head, color], index) => {
    const x = 1.0 + (index % 2) * 6.1;
    const y = 1.8 + Math.floor(index / 2) * 1.65;
    rect(slide, pptx, x, y, 5.2, 1.15, C.night2, color, true, 1.25);
    addText(slide, head, { x: x + 0.3, y: y + 0.26, w: 2.05, h: 0.58, fontFace: FONT_SERIF, fontSize: 32, bold: true, color: index === 0 ? C.goldSoft : C.white, align: "center" });
    line(slide, pptx, x + 2.65, y + 0.67, 2.0, color, 1.25, "dash");
  });
  prompt(slide, "先说准每个词，再用原句画出：语意怎样一步步加重？", { y: 5.65, color: C.goldSoft, fontSize: 28 });
  addNotes(slide, page);
}

function renderThreeLayers(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true });
  const layers = [["物象变化", C.leaf], ["婚后生活", C.river], ["责任判断", C.plum]];
  layers.forEach(([head, color], index) => {
    const x = 0.9 + index * 4.15;
    rect(slide, pptx, x, 1.85, 3.6, 2.65, C.night2, color, true, 1.2);
    addText(slide, head, { x: x + 0.25, y: 2.28, w: 3.1, h: 0.55, fontFace: FONT_SERIF, fontSize: 27, bold: true, color: C.white, align: "center" });
    line(slide, pptx, x + 0.55, 3.55, 2.5, color, 1.2, "dash");
  });
  prompt(slide, "合书四十五秒，把三层讲成一段。", { y: 5.65, color: C.goldSoft, fontSize: 30 });
  addNotes(slide, page);
}

function renderNestedTime(slide, pptx, page) {
  base(slide, pptx, page);
  title(slide, page);
  rect(slide, pptx, 1.1, 2.0, 11.0, 2.9, C.goldSoft, C.gold, true, 1.1);
  rect(slide, pptx, 2.2, 2.7, 8.8, 1.5, C.paper2, C.river, true, 1.1);
  addText(slide, "三岁为妇｜靡有朝矣", { x: 1.45, y: 2.2, w: 10.3, h: 0.45, fontFace: FONT_SERIF, fontSize: 25, bold: true, color: C.gold, align: "center" });
  addText(slide, "夙兴　　　　　　　　　　　　　　夜寐", { x: 2.65, y: 3.15, w: 7.9, h: 0.52, fontFace: FONT_SERIF, fontSize: 29, bold: true, color: C.river, align: "center" });
  prompt(slide, "把一天的首尾，叠进一日又一日。", { y: 5.65, color: C.ink, fontSize: 29 });
  addNotes(slide, page);
}

function renderBoundary(slide, pptx, page) {
  renderContrast(slide, pptx, page,
    { head: "现在能说明什么？", body: "________________\n________________" },
    { head: "仍不能断言什么？", body: "________________\n________________" },
    "只选一处早期细节，让后来的事实改变目光，也让原词守住边界。",
  );
}

function renderSoundField(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true });
  addText(slide, "兄弟不知，咥其笑矣。", { x: 1.0, y: 2.0, w: 4.45, h: 0.75, fontFace: FONT_SERIF, fontSize: 33, bold: true, color: C.plumSoft, align: "center" });
  addText(slide, "三秒沉默", { x: 5.62, y: 2.08, w: 2.1, h: 0.55, fontFace: FONT_SERIF, fontSize: 23, color: C.warm2, align: "center" });
  addText(slide, "静言思之，躬自悼矣。", { x: 7.9, y: 2.0, w: 4.45, h: 0.75, fontFace: FONT_SERIF, fontSize: 33, bold: true, color: C.riverSoft, align: "center" });
  line(slide, pptx, 1.2, 3.4, 10.9, C.warm2, 1.1);
  prompt(slide, "外面的声音退去以后，空间里只剩下谁？", { y: 4.65, color: C.white, fontSize: 34 });
  addNotes(slide, page);
}

function renderLifeWriting(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true });
  rect(slide, pptx, 1.05, 1.55, 11.2, 3.95, C.night2, C.plum, true, 1.2);
  const anchors = ["夙兴夜寐", "既遂至暴", "兄弟不知", "躬自悼矣"];
  anchors.forEach((value, index) => addText(slide, value, { x: 1.35 + index * 2.72, y: 1.95, w: 2.25, h: 0.45, fontFace: FONT_SERIF, fontSize: 21, bold: true, color: [C.goldSoft, C.redSoft, C.plumSoft, C.riverSoft][index], align: "center" }));
  line(slide, pptx, 1.7, 3.15, 9.9, C.warm2, 1.1, "dash");
  line(slide, pptx, 1.7, 4.35, 9.9, C.warm2, 1.1, "dash");
  prompt(slide, "四十到六十字｜不添具体家务，不添诗外伤害。", { y: 5.95, color: C.goldSoft, fontSize: 26 });
  addNotes(slide, page);
}

function renderOldNew(slide, pptx, page) {
  base(slide, pptx, page);
  title(slide, page, { size: 32 });
  const words = [
    ["信誓旦旦", C.goldSoft, C.gold], ["二三其德", C.plumSoft, C.plum],
    ["言笑晏晏", C.riverSoft, C.river], ["至于暴矣", C.redSoft, C.red],
    ["总角之宴", C.leafSoft, C.leaf], ["不思其反", C.plumSoft, C.plum],
  ];
  words.forEach(([value, fill, color], index) => {
    const x = 0.75 + index * 2.08;
    rect(slide, pptx, x, 1.7, 1.75, 0.85, fill, color, true, 1.0);
    addText(slide, value, { x: x + 0.1, y: 1.95, w: 1.55, h: 0.38, fontFace: FONT_SERIF, fontSize: 19.5, bold: true, color, align: "center" });
  });
  rect(slide, pptx, 1.0, 3.2, 5.3, 1.65, C.paper2, C.river, true, 1.1);
  rect(slide, pptx, 7.0, 3.2, 5.3, 1.65, C.paper2, C.plum, true, 1.1);
  addText(slide, "她记得的旧日", { x: 1.3, y: 3.7, w: 4.7, h: 0.5, fontFace: FONT_SERIF, fontSize: 27, bold: true, color: C.river, align: "center" });
  addText(slide, "后来核验出的事实", { x: 7.3, y: 3.7, w: 4.7, h: 0.5, fontFace: FONT_SERIF, fontSize: 27, bold: true, color: C.plum, align: "center" });
  prompt(slide, "先独立放置；有犹豫，就让那张原词卡暂时停在中间。", { y: 5.75, color: C.ink, fontSize: 26 });
  addNotes(slide, page);
}

function renderEndBoundary(slide, pptx, page) {
  base(slide, pptx, page, { dark: true });
  title(slide, page, { dark: true });
  addText(slide, "信誓旦旦，不思其反。", { x: 1.0, y: 1.75, w: 11.33, h: 0.75, fontFace: FONT_SERIF, fontSize: 40, bold: true, color: C.goldSoft, align: "center" });
  addText(slide, "反是不思，亦已焉哉！", { x: 1.0, y: 2.75, w: 11.33, h: 0.75, fontFace: FONT_SERIF, fontSize: 43, bold: true, color: C.plumSoft, align: "center" });
  rect(slide, pptx, 1.05, 4.05, 5.25, 1.1, C.night2, C.gold, true, 1.1);
  rect(slide, pptx, 7.0, 4.05, 5.25, 1.1, C.night2, C.river, true, 1.1);
  addText(slide, "诗写到了什么？", { x: 1.35, y: 4.37, w: 4.65, h: 0.45, fontFace: FONT_SERIF, fontSize: 27, bold: true, color: C.white, align: "center" });
  addText(slide, "诗没有继续写什么？", { x: 7.3, y: 4.37, w: 4.65, h: 0.45, fontFace: FONT_SERIF, fontSize: 27, bold: true, color: C.white, align: "center" });
  prompt(slide, "先让自己的回答停在原词能够托住的地方。", { y: 5.75, color: C.goldSoft, fontSize: 30 });
  addNotes(slide, page);
}

function renderSynthesis(slide, pptx, page) {
  const dark = page.page_id === "S03" || page.page_id === "S08";
  base(slide, pptx, page, { dark });
  title(slide, page, { dark, size: page.page_id === "S03" ? 35 : 33 });
  const items = page.frontstage.slice(1);
  if (page.page_id === "S02") {
    rect(slide, pptx, 0.9, 1.45, 7.55, 4.85, C.paper2, C.river, true, 1.1);
    addText(slide, "一段匿名生活文字", { x: 1.3, y: 1.9, w: 6.75, h: 0.52, fontFace: FONT_SERIF, fontSize: 31, bold: true, color: C.river, align: "center" });
    line(slide, pptx, 1.45, 3.05, 6.45, C.warm, 1.2, "dash");
    line(slide, pptx, 1.45, 4.15, 6.45, C.warm, 1.2, "dash");
    line(slide, pptx, 1.45, 5.25, 6.45, C.warm, 1.2, "dash");
    rect(slide, pptx, 8.9, 1.8, 3.45, 3.95, C.riverSoft, C.river, true, 1.1);
    addText(slide, "猜回原诗", { x: 9.25, y: 2.35, w: 2.75, h: 0.62, fontFace: FONT_SERIF, fontSize: 33, bold: true, color: C.river, align: "center" });
    addText(slide, "哪一个生活细节\n把你带了回去？", { x: 9.3, y: 3.65, w: 2.65, h: 1.0, fontFace: FONT_SERIF, fontSize: 23, color: C.ink, align: "center" });
  } else if (page.page_id === "S03") {
    addText(slide, "先独立写下，你认为最重要的一两个原因。", { x: 1.25, y: 1.85, w: 10.83, h: 0.7, fontFace: FONT_SERIF, fontSize: 35, bold: true, color: C.goldSoft, align: "center" });
    line(slide, pptx, 2.15, 3.35, 9.03, C.warm2, 1.2, "dash");
    line(slide, pptx, 2.15, 4.55, 9.03, C.warm2, 1.2, "dash");
    prompt(slide, "先不看框架。写完以后，再把原句放回时间、质询因果。", { y: 5.85, color: C.white, fontSize: 27 });
  } else if (page.page_id === "S04") {
    addText(slide, "每个人都先开口", { x: 1.0, y: 1.55, w: 3.2, h: 0.62, fontFace: FONT_SERIF, fontSize: 29, bold: true, color: C.river, align: "center" });
    addText(slide, "一处原诗　＋　一个关系条件", { x: 4.05, y: 1.55, w: 5.25, h: 0.62, fontFace: FONT_SERIF, fontSize: 29, bold: true, color: C.plum, align: "center" });
    addText(slide, "一组只留一张卡", { x: 9.15, y: 1.55, w: 3.2, h: 0.62, fontFace: FONT_SERIF, fontSize: 29, bold: true, color: C.gold, align: "center" });
    [C.river, C.leaf, C.plum, C.gold].forEach((color, index) => {
      const x = 1.13 + index * 1.15;
      slide.addShape(pptx.shapes.OVAL, { x, y: 2.75, w: 0.82, h: 0.82, fill: { color }, line: { color } });
    });
    line(slide, pptx, 5.95, 3.16, 1.2, C.warm2, 2);
    slide.addShape(pptx.shapes.CHEVRON, { x: 7.0, y: 2.83, w: 0.7, h: 0.65, fill: { color: C.warm2 }, line: { color: C.warm2 } });
    rect(slide, pptx, 8.15, 2.55, 3.7, 1.25, C.goldSoft, C.gold, true, 1.2);
    addText(slide, "好的共同生活，需要______", { x: 8.4, y: 2.84, w: 3.2, h: 0.5, fontFace: FONT_SERIF, fontSize: 22, bold: true, color: C.ink, align: "center" });
    addText(slide, "一段良好的共同生活，需要哪些支点？", { x: 1.2, y: 4.45, w: 10.93, h: 0.72, fontFace: FONT_SERIF, fontSize: 38, bold: true, color: C.plum, align: "center" });
    prompt(slide, "四个人都说过以后，讨论才开始。", { y: 5.75, color: C.ink, fontSize: 27 });
  } else if (page.page_id === "S05A") {
    const facts = ["它是什么？", "有多少篇？", "分哪三类？", "《氓》收在哪里？"];
    facts.forEach((value, index) => {
      const x = 0.88 + index * 3.08;
      rect(slide, pptx, x, 1.72, 2.7, 1.05, C.paper2, [C.gold, C.river, C.leaf, C.plum][index], true, 1);
      addText(slide, value, { x: x + 0.14, y: 2.05, w: 2.42, h: 0.36, fontFace: FONT_SERIF, fontSize: 21, bold: true, align: "center" });
    });
    line(slide, pptx, 1.1, 3.75, 11.05, C.warm, 1.2, "dash");
    line(slide, pptx, 1.1, 4.75, 11.05, C.warm, 1.2, "dash");
    prompt(slide, "先合书独立写；不确定，可以留空。", { y: 5.75, color: C.red, fontSize: 28 });
  } else if (page.page_id === "S05B") {
    const glyphs = ["愆", "将", "筮", "说", "徂", "汤汤", "渐", "爽", "暴", "泮"];
    glyphs.forEach((value, index) => {
      const x = 1.0 + (index % 5) * 2.35;
      const y = 1.75 + Math.floor(index / 5) * 1.65;
      addText(slide, value, { x, y, w: 1.8, h: 0.62, fontFace: FONT_SERIF, fontSize: value.length > 1 ? 25 : 33, bold: true, color: index < 5 ? C.ink : C.river, align: "center" });
      line(slide, pptx, x + 0.25, y + 0.74, 1.3, C.warm, 1.1);
    });
    prompt(slide, "任选两个：读音｜句中义｜原句。先凭记忆，再用教材修复。", { y: 5.75, color: C.red, fontSize: 27 });
  } else if (page.page_id === "S06") {
    const zones = [
      ["六章第一人称叙事", "原诗：________________", C.goldSoft, C.gold],
      ["桑叶比兴与对照", "原诗：________________", C.leafSoft, C.leaf],
      ["复现、回环、反折", "原诗：________________", C.plumSoft, C.plum],
      ["四言与叠词", "原诗：________________", C.riverSoft, C.river],
    ];
    zones.forEach(([head, body, fill, color], index) => {
      const x = 0.85 + (index % 2) * 6.12;
      const y = 1.5 + Math.floor(index / 2) * 2.4;
      rect(slide, pptx, x, y, 5.58, 1.75, fill, color, true, 1.05);
      addText(slide, head, { x: x + 0.25, y: y + 0.28, w: 5.08, h: 0.44, fontFace: FONT_SERIF, fontSize: 24, bold: true, color, align: "center" });
      addText(slide, body, { x: x + 0.25, y: y + 0.98, w: 5.08, h: 0.38, fontSize: 19.5, color: C.ink2, align: "center" });
    });
    prompt(slide, "请为每一块，补回一处已经读过的原诗。", { y: 6.3, color: C.ink, fontSize: 25 });
  } else if (page.page_id === "S08") {
    addText(slide, "一处改变最大的理解", { x: 1.2, y: 1.95, w: 4.9, h: 0.72, fontFace: FONT_SERIF, fontSize: 33, bold: true, color: C.goldSoft, align: "center" });
    addText(slide, "或", { x: 6.25, y: 2.02, w: 0.8, h: 0.55, fontFace: FONT_SERIF, fontSize: 25, color: C.warm2, align: "center" });
    addText(slide, "一个仍愿追问的问题", { x: 7.25, y: 1.95, w: 4.9, h: 0.72, fontFace: FONT_SERIF, fontSize: 33, bold: true, color: C.riverSoft, align: "center" });
    line(slide, pptx, 1.65, 3.25, 9.95, C.warm2, 1.1);
    addText(slide, "从“氓之蚩蚩”读到“亦已焉哉”", { x: 1.1, y: 4.2, w: 11.13, h: 0.65, fontFace: FONT_SERIF, fontSize: 29, color: C.white, align: "center" });
    prompt(slide, "然后，让全诗完整响起。", { y: 5.75, color: C.plumSoft, fontSize: 37 });
  } else {
    items.forEach((value, index) => addText(slide, value, { x: 1.1, y: 1.6 + index * 1.0, w: 11.05, h: 0.65, fontFace: FONT_SERIF, fontSize: 28, bold: index === 0, align: "center" }));
  }
  addNotes(slide, page);
}

function chooseRenderer(page) {
  const openingRenderers = {
    O01: renderO01, O02: renderO02, O03: renderO03, O04: renderO04,
    O05: renderListening, O06: renderListening, O07: renderO07, O08: renderO08,
  };
  if (openingRenderers[page.page_id]) return openingRenderers[page.page_id];
  if (page.module === "synthesis") return renderSynthesis;
  const specialized = {
    C102: renderWordTurn,
    C103: renderActionRoad,
    C104: renderSpeechSequence,
    C202: (slide, pptx, p) => renderContrast(slide, pptx, p,
      { head: "不见复关", body: "泣涕涟涟" },
      { head: "既见复关", body: "载笑载言" },
      "哪些原词彼此照应？声音从哪里真正转过去？"),
    C204: (slide, pptx, p) => renderFlow(slide, pptx, p,
      [["卜筮", "尔卜尔筮", C.gold], ["无咎", "体无咎言", C.leaf], ["车来", "以尔车来", C.river], ["贿迁", "以我贿迁", C.plum]],
      "辨清双方主体，再把占问到迁嫁说成因序。"),
    C206: (slide, pptx, p) => renderContrast(slide, pptx, p,
      { head: "第一章", body: "来—送—约" },
      { head: "第二章", body: "等—见—迁" },
      "‘秋以为期’，怎样把两章接成一条因果？"),
    C302: (slide, pptx, p) => renderSingleVerse(slide, pptx, p, "桑之未落，其叶沃若。", "色泽、质地、生命感｜先留下感受，再留下可能。", C.leaf),
    C303: renderObjectToPerson,
    C305: (slide, pptx, p) => renderContrast(slide, pptx, p,
      { head: "士之耽兮", body: "犹可说也" },
      { head: "女之耽兮", body: "不可说也" },
      "同样的‘耽/说’，哪些词改变了两人的脱身处境？"),
    C402: (slide, pptx, p) => renderContrast(slide, pptx, p,
      { head: "桑之未落", body: "其叶沃若" },
      { head: "桑之落矣", body: "其黄而陨" },
      "翻回原来的想法：保留、改写，还是撤回？"),
    C403: (slide, pptx, p) => renderContrast(slide, pptx, p,
      { head: "三岁食贫", body: "一句压着许多年的生活" },
      { head: "淇水汤汤", body: "一句展开渡水的一刻" },
      "用一句自然话，让多年与当下同时存在。"),
    C404_405: renderResponsibility,
    C406: renderThreeLayers,
    C502: renderNestedTime,
    C503: renderBoundary,
    C504: renderSoundField,
    C505: renderLifeWriting,
    C602: (slide, pptx, p) => renderContrast(slide, pptx, p,
      { head: "及尔偕老", body: "第一个‘老’：________________" },
      { head: "老使我怨", body: "第二个‘老’：________________" },
      "同一个字，前后两次分别让你看见怎样的生活？"),
    C604: renderOldNew,
    C605: renderEndBoundary,
  };
  if (specialized[page.page_id]) return specialized[page.page_id];
  return renderChapterPage;
}

const plan = lesson.pages.map((page) => ({ ...page, render: chooseRenderer(page) }));

function textFromSlideObject(object) {
  if (!object || object._type === "notes" || object.text === null || object.text === undefined) return "";
  if (typeof object.text === "string") return object.text;
  if (Array.isArray(object.text)) return object.text.map((run) => typeof run === "string" ? run : run?.text || "").join("");
  return "";
}

function visibleTextFor(page) {
  const pptx = presentation();
  const slide = pptx.addSlide();
  page.render(slide, pptx, page);
  return slide._slideObjects.map(textFromSlideObject).filter(Boolean).join("\n");
}

function validatePresentation(pptx) {
  const errors = [];
  if (pptx._slides.length !== lesson.target_pages) errors.push(`slides ${pptx._slides.length}/${lesson.target_pages}`);
  pptx._slides.forEach((slide, slideIndex) => {
    if (!slide._slideObjects.some((item) => item._type === "notes")) errors.push(`slide ${slideIndex + 1} missing notes`);
    slide._slideObjects.forEach((item, objectIndex) => {
      const options = item.options || {};
      if ([options.x, options.y, options.w, options.h].every((value) => typeof value === "number")) {
        if (options.x < -0.01 || options.y < -0.01 || options.x + options.w > W + 0.01 || options.y + options.h > H + 0.01) {
          errors.push(`slide ${slideIndex + 1} object ${objectIndex + 1} out of bounds`);
        }
      }
    });
  });
  if (errors.length) throw new Error(errors.join("\n"));
}

async function repairNotesMaster(filePath) {
  const archive = await JSZip.loadAsync(fs.readFileSync(filePath));
  const entry = archive.file("ppt/presentation.xml");
  let xml = await entry.async("string");
  const match = xml.match(/<p:notesMasterIdLst>[\s\S]*?<\/p:notesMasterIdLst>/);
  if (match) {
    xml = xml.replace(match[0], "");
    xml = xml.replace(/(<p:sldMasterIdLst>[\s\S]*?<\/p:sldMasterIdLst>)/, `$1${match[0]}`);
  }
  archive.file("ppt/presentation.xml", xml);
  fs.writeFileSync(filePath, await archive.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

async function build() {
  const pptx = presentation();
  for (const page of plan) page.render(pptx.addSlide(), pptx, page);
  validatePresentation(pptx);
  fs.mkdirSync(OUT_DIR, { recursive: true });
  await pptx.writeFile({ fileName: outputPath, compression: true });
  await repairNotesMaster(outputPath);
  const manifest = {
    schema_version: "1.0",
    version: lesson.version,
    artifact: path.relative(PROJECT_ROOT, outputPath).split(path.sep).join("/"),
    sha256: sha256(outputPath),
    pages: plan.map((page) => ({ page_number: page.page_number, page_id: page.page_id, minutes: page.minutes, legacy_refs: page.legacy_refs })),
    total_pages: lesson.target_pages,
    total_minutes: lesson.target_natural_minutes,
    illustrations: 0,
    claim_boundary: "no_image_physical_candidate_not_independently_released",
  };
  fs.writeFileSync(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`MENG_V65_PPTX_OK slides=${lesson.target_pages} sha256=${manifest.sha256} output=${outputPath}\n`);
  return manifest;
}

if (require.main === module) build().catch((error) => { console.error(error); process.exitCode = 1; });

module.exports = { build, notesFor, visibleTextFor, outputPath, manifestPath, plan };
