#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");

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

const ROOT = path.resolve(__dirname, "..");
const STAGE = path.join(ROOT, "work", "备课", "选择性必修下册", "氓", "_v6_stage");
const SNAPSHOT = path.join(STAGE, "opening", "package", "06_氓_V6导入切片课程数据快照.json");
const OUT = path.join(STAGE, "opening", "pptx");
const PPTX = path.join(OUT, "04_氓_V6导入课堂课件.pptx");
const MANIFEST = path.join(OUT, "opening_pptx_manifest.json");

const W = 13.333;
const H = 7.5;
const FONT_HEAD = "Noto Serif CJK SC";
const FONT_BODY = "Noto Sans CJK SC";
const FONT_TEXT = "Noto Serif CJK SC";
const C = {
  ink: "27231F", ink2: "4B443D", paper: "F6F0E5", paper2: "FFFCF6",
  warm: "E7DCCB", cinnabar: "A84A3A", cinnabarSoft: "F1DCD5",
  river: "4E7480", riverSoft: "DCE9EA", leaf: "647752", leafSoft: "E1E7D9",
  gold: "B18B52", white: "FFFFFF", muted: "766E65", night: "282522",
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
  pres.subject = "《氓》V6导入课堂课件";
  pres.title = "《氓》V6导入课堂课件";
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

function rect(slide, pres, x, y, w, h, fill, lineColor = fill, radius = false, transparency = 0) {
  slide.addShape(radius ? pres.shapes.ROUNDED_RECTANGLE : pres.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: fill, transparency },
    line: { color: lineColor, width: 1 }, ...(radius ? { rectRadius: 0.06 } : {}),
  });
}

function line(slide, pres, x, y, w, color, width = 1) {
  slide.addShape(pres.shapes.LINE, { x, y, w, h: 0, line: { color, width } });
}

function base(slide, pres, dark = false) {
  slide.background = { color: dark ? C.night : C.paper };
  rect(slide, pres, 0, 0, W, 0.13, dark ? C.gold : C.ink, dark ? C.gold : C.ink);
}

function title(slide, text, options = {}) {
  addText(slide, text, {
    x: 0.72, y: 0.42, w: 11.9, h: 0.58,
    fontFace: FONT_HEAD, fontSize: 34, bold: true, ...options,
  });
}

function notesFor(page, physicalState = null) {
  if (page.page_id === "N011" && physicalState) {
    const occurrenceId = physicalState === "input" ? "N011_INPUT" : "N011_RECALL";
    const occurrence = (page.physical_occurrences || []).find((item) => item.occurrence_id === occurrenceId);
    if (!occurrence) throw new Error(`snapshot missing ${occurrenceId}`);
    const occurrenceTimeboxes = occurrence.timeboxes.map((item) => `${item.label}：${item.seconds}秒`).join("；");
    const occurrenceBranches = occurrence.branches.map((item) => `${item.kind}：${item.response}`).join("\n");
    return [
      `【V6页ID】${page.page_id}｜${page.title}｜2分钟`,
      `【物理状态】${occurrence.state}｜${occurrence.seconds}秒`,
      "【教师逐字稿】", occurrence.teacher_spoken,
      "【场面与走位】", occurrence.scene, ...occurrence.stage_directions.map((item) => `（${item}）`),
      "【时间盒】", occurrenceTimeboxes,
      "【现场分支】", occurrenceBranches,
      "【听者同步任务】", occurrence.listener_task,
      "【证据位置】", occurrence.evidence_location,
      "【自然切页句】", occurrence.cut_line,
      "【声明边界】桌面排演稿；不声称真实学生已经理解、参与或学会。",
    ].join("\n");
  }
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

function addNotes(slide, page, physicalState = null) {
  slide.addNotes(notesFor(page, physicalState));
}

function renderN001(slide, pres, page) {
  base(slide, pres, true);
  addText(slide, "氓", {
    x: 0.9, y: 1.34, w: 11.53, h: 2.2, fontFace: FONT_HEAD,
    fontSize: 104, bold: true, color: C.paper, align: "center",
  });
  addText(slide, "《诗经·卫风》", {
    x: 3.6, y: 4.36, w: 6.13, h: 0.62, fontFace: FONT_HEAD,
    fontSize: 30, color: C.warm, align: "center",
  });
  addText(slide, "翻到题名，找到第一句", {
    x: 4.45, y: 6.3, w: 4.43, h: 0.36, fontSize: 19,
    color: "C8BFB5", align: "center",
  });
  addNotes(slide, page);
}

function renderN002(slide, pres, page) {
  base(slide, pres);
  title(slide, "想起哪些爱情或婚姻故事？");
  addText(slide, "从初中到高中，尽量多写", {
    x: 0.82, y: 1.35, w: 7.5, h: 0.55, fontFace: FONT_HEAD,
    fontSize: 31, bold: true,
  });
  rect(slide, pres, 8.55, 1.18, 3.85, 0.94, C.cinnabarSoft, C.cinnabar, true);
  addText(slide, "至少一篇\n篇名＋它写了什么", {
    x: 8.82, y: 1.35, w: 3.31, h: 0.58, fontSize: 19.5,
    bold: true, color: C.cinnabar, align: "center", breakLine: true,
  });
  ["1", "2", "3", "4", "5"].forEach((label, index) => {
    const y = 2.18 + index * 0.78;
    addText(slide, label, { x: 1.0, y: y + 0.2, w: 0.45, h: 0.32, fontSize: 21, bold: true, color: C.gold, align: "center" });
    line(slide, pres, 1.62, y + 0.62, 10.12, index === 0 ? C.cinnabar : C.warm, 1.2);
    addText(slide, index === 0 ? "篇名　　　　　　　　　它写了什么" : "", {
      x: 1.72, y: y + 0.03, w: 9.82, h: 0.35, fontSize: 18.5,
      color: C.muted,
    });
  });
  addText(slide, "先独立回想｜还能想起，就继续往下添", {
    x: 2.02, y: 6.42, w: 9.3, h: 0.32, fontSize: 20,
    color: C.river, bold: true, align: "center",
  });
  addNotes(slide, page);
}

function renderN003(slide, pres, page) {
  base(slide, pres);
  title(slide, "四个人，把记得的故事说给彼此听");
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
  addText(slide, "每人圈两项", { x: 7.28, y: 3.94, w: 4.84, h: 0.34, fontFace: FONT_HEAD, fontSize: 22, bold: true, color: C.ink2, align: "center" });
  addText(slide, "暂无新增，也从作品谱选两项", { x: 7.28, y: 4.34, w: 4.84, h: 0.34, fontFace: FONT_HEAD, fontSize: 22, bold: true, color: C.ink2, align: "center" });
  rect(slide, pres, 1.12, 5.04, 11.08, 1.22, C.riverSoft, C.river, true);
  addText(slide, "四轮后｜每人圈两项  →  每组写两张贡献卡", { x: 1.42, y: 5.22, w: 10.48, h: 0.38, fontFace: FONT_HEAD, fontSize: 25, bold: true, color: C.river, align: "center" });
  addText(slide, "卡面写清：组号－卡号－原提议者号｜原提议者签认", { x: 1.72, y: 5.72, w: 9.88, h: 0.3, fontSize: 20.5, bold: true, color: C.ink2, align: "center" });
  addText(slide, "执笔人记全组作品谱；轮到自己时，下一位代记｜共 6 分钟", { x: 2.05, y: 6.43, w: 9.23, h: 0.3, fontSize: 19.5, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderN004(slide, pres, page) {
  base(slide, pres);
  title(slide, "让更多故事走到全班面前");
  const sharedSteps = [
    ["1", "每组贴两张卡", C.gold, C.warm],
    ["2", "20秒说一处", C.cinnabar, C.cinnabarSoft],
    ["3", "听众留一个结果", C.river, C.riverSoft],
  ];
  sharedSteps.forEach(([number, label, color, fill], index) => {
    const x = 0.92 + index * 4.05;
    rect(slide, pres, x, 1.28, 3.63, 0.82, fill, color, true);
    addText(slide, number, { x: x + 0.22, y: 1.52, w: 0.42, h: 0.28, fontSize: 20, bold: true, color, align: "center" });
    addText(slide, label, { x: x + 0.72, y: 1.48, w: 2.61, h: 0.34, fontFace: FONT_HEAD, fontSize: 23, bold: true, color: C.ink, align: "center" });
  });
  const paths = [
    ["卡墙还没有", "说清：篇名＋它写了什么", C.river, C.riverSoft],
    ["卡墙已有相同内容", "说清相同或不同\n完全重复：说“暂无新增”", C.leaf, C.leafSoft],
  ];
  paths.forEach(([head, body, color, fill], index) => {
    const x = 0.92 + index * 6.05;
    rect(slide, pres, x, 2.42, 5.45, 1.5, fill, color, true);
    addText(slide, head, { x: x + 0.32, y: 2.65, w: 4.81, h: 0.34, fontFace: FONT_HEAD, fontSize: 23, bold: true, color, align: "center" });
    line(slide, pres, x + 1.25, 3.1, 2.95, color, 1.1);
    addText(slide, body, { x: x + 0.42, y: 3.2, w: 4.61, h: 0.52, fontSize: index === 1 ? 19.5 : 21, bold: true, color: C.ink2, breakLine: true, align: "center", valign: "mid" });
  });
  addText(slide, "台下每个人｜留下一个听见的结果", { x: 0.95, y: 4.18, w: 4.75, h: 0.38, fontFace: FONT_HEAD, fontSize: 22, bold: true, color: C.gold, align: "left" });
  const listenerPaths = [
    ["有新增", "记下一项自己未想到的内容", C.river, C.riverSoft],
    ["暂无新增", "核对一张重复卡：它真的补了不同说法吗？", C.cinnabar, C.cinnabarSoft],
  ];
  listenerPaths.forEach(([head, body, color, fill], index) => {
    const x = 0.92 + index * 6.05;
    rect(slide, pres, x, 4.68, 5.45, 1.28, fill, color, true);
    addText(slide, head, { x: x + 0.3, y: 4.95, w: 1.36, h: 0.34, fontFace: FONT_HEAD, fontSize: 23, bold: true, color, align: "center" });
    addText(slide, body, { x: x + 1.7, y: 4.85, w: 3.35, h: 0.72, fontSize: 18.5, bold: true, color: C.ink2, breakLine: true, valign: "mid" });
  });
  addText(slide, "八组公开、贴卡、换组与补记｜共 6 分钟", { x: 3.02, y: 6.53, w: 7.3, h: 0.32, fontSize: 20, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function renderN005(slide, pres, page) {
  base(slide, pres, true);
  title(slide, "我们读过的爱情与婚姻故事", { color: C.paper });
  addText(slide, "请看教室里的作品卡墙", { x: 0.85, y: 1.25, w: 11.63, h: 0.5, fontSize: 22, color: C.warm, align: "center" });
  const moves = [
    ["每人先连一组", "写两张卡号\n给它临时命名", C.gold],
    ["三位同学上台", "移动卡片\n读出卡上依据", C.river],
    ["全班核对", "每人写理由\n提议者当场改定", C.leaf],
  ];
  moves.forEach(([verb, question, color], index) => {
    const x = 0.82 + index * 4.17;
    addText(slide, `${index + 1}`, { x, y: 2.18, w: 0.52, h: 0.38, fontSize: 20, bold: true, color, align: "center" });
    addText(slide, verb, { x: x + 0.68, y: 2.03, w: 2.9, h: 0.62, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: C.paper });
    line(slide, pres, x + 0.68, 2.88, 2.95, color, 2.2);
    addText(slide, question, { x: x + 0.68, y: 3.26, w: 3.05, h: 1.15, fontFace: FONT_HEAD, fontSize: 23, color: C.warm, breakLine: true, valign: "top" });
  });
  addText(slide, "保留／改名／移回｜只留下卡片原话能够托住的联系", { x: 1.72, y: 6.18, w: 9.9, h: 0.38, fontFace: FONT_HEAD, fontSize: 22, bold: true, color: C.warm, align: "center" });
  addNotes(slide, page);
}

function renderN007(slide, pres, page) {
  base(slide, pres);
  title(slide, "读完六章，再回答");
  const questions = [
    ["一", "她经历了什么？", C.gold],
    ["二", "她婚后的不幸，\n在生活中是什么样子？", C.river],
    ["三", "这场婚姻为什么\n走到这一步？", C.cinnabar],
  ];
  questions.forEach(([label, question, color], index) => {
    const y = 1.45 + index * 1.72;
    slide.addShape(pres.shapes.OVAL, { x: 1.0, y: y + 0.12, w: 0.78, h: 0.78, fill: { color }, line: { color } });
    addText(slide, label, { x: 1.0, y: y + 0.32, w: 0.78, h: 0.29, fontSize: 20, bold: true, color: C.white, align: "center" });
    addText(slide, question, { x: 2.18, y, w: 9.65, h: 1.18, fontFace: FONT_HEAD, fontSize: index === 0 ? 34 : 30, bold: true, breakLine: true, valign: "mid" });
    if (index < 2) line(slide, pres, 2.18, y + 1.38, 9.25, C.warm, 1);
  });
  addText(slide, "此刻只选一问做记号，不急着回答", { x: 3.55, y: 6.72, w: 6.23, h: 0.31, fontSize: 19, color: C.muted, align: "center" });
  addNotes(slide, page);
}

function addPoemListening(slide, pres, page, startChapter) {
  base(slide, pres);
  addText(slide, page.title, { x: 0.72, y: 0.32, w: 5.6, h: 0.4, fontFace: FONT_HEAD, fontSize: 25, bold: true, color: C.cinnabar });
  addText(slide, "眼随声走｜不齐读｜用笔在教材原句旁留一点", { x: 6.65, y: 0.39, w: 5.97, h: 0.28, fontSize: 17.5, bold: true, color: C.ink2, align: "right" });
  line(slide, pres, 0.72, 0.82, 11.9, C.warm, 1.1);
  const all = [
    ["氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。", "送子涉淇，至于顿丘。匪我愆期，子无良媒。", "将子无怒，秋以为期。"],
    ["乘彼垝垣，以望复关。不见复关，泣涕涟涟。", "既见复关，载笑载言。尔卜尔筮，体无咎言。", "以尔车来，以我贿迁。"],
    ["桑之未落，其叶沃若。于嗟鸠兮，无食桑葚！", "于嗟女兮，无与士耽！士之耽兮，犹可说也。", "女之耽兮，不可说也！"],
    ["桑之落矣，其黄而陨。自我徂尔，三岁食贫。", "淇水汤汤，渐车帷裳。女也不爽，士贰其行。", "士也罔极，二三其德。"],
    ["三岁为妇，靡室劳矣。夙兴夜寐，靡有朝矣。", "言既遂矣，至于暴矣。兄弟不知，咥其笑矣。", "静言思之，躬自悼矣。"],
    ["及尔偕老，老使我怨。淇则有岸，隰则有泮。", "总角之宴，言笑晏晏。信誓旦旦，不思其反。", "反是不思，亦已焉哉！"],
  ];
  const accents = [C.gold, C.river, C.leaf];
  all.slice(startChapter - 1, startChapter + 2).forEach((rows, index) => {
    const y = 0.98 + index * 2.07;
    rect(slide, pres, 0.72, y, 11.9, 1.85, index % 2 ? C.paper2 : "F9F4EA", index % 2 ? C.paper2 : "F9F4EA", true);
    rect(slide, pres, 0.72, y + 0.17, 0.08, 1.5, accents[index], accents[index]);
    addText(slide, `第${["一", "二", "三", "四", "五", "六"][startChapter + index - 1]}章`, { x: 0.84, y: y + 0.15, w: 0.67, h: 0.29, fontSize: 17.5, bold: true, color: accents[index], align: "center" });
    addText(slide, rows.map((text, row) => ({ text, options: { breakLine: row < rows.length - 1 } })), {
      x: 1.55, y: y + 0.16, w: 10.68, h: 1.49, fontFace: FONT_TEXT,
      fontSize: 29.5, color: C.ink, breakLine: true,
      breakLineOnTextOverflow: false, lineSpacingMultiple: 1.0,
    });
  });
  addNotes(slide, page);
}

function renderN008(slide, pres, page) { addPoemListening(slide, pres, page, 1); }
function renderN009(slide, pres, page) { addPoemListening(slide, pres, page, 4); }

function renderN010(slide, pres, page) {
  base(slide, pres);
  title(slide, "把第一次听见的《氓》留在纸上");
  const paths = [
    ["有一句把我留住", "抄下它，再接一句\n我听见／我看见／我想问……", C.river, C.riverSoft],
    ["尚未找到", "如实写下\n先听同桌，再决定补一句或保留", C.cinnabar, C.cinnabarSoft],
  ];
  paths.forEach(([head, body, color, fill], index) => {
    const x = 0.92 + index * 6.05;
    rect(slide, pres, x, 1.52, 5.45, 3.05, fill, color, true);
    addText(slide, head, { x: x + 0.35, y: 2.05, w: 4.75, h: 0.54, fontFace: FONT_HEAD, fontSize: 31, bold: true, color, align: "center" });
    line(slide, pres, x + 1.25, 2.91, 2.95, color, 1.3);
    addText(slide, body, { x: x + 0.48, y: 3.16, w: 4.49, h: 0.96, fontSize: 22.5, bold: true, breakLine: true, align: "center", valign: "mid" });
  });
  line(slide, pres, 0.95, 5.12, 11.42, C.warm, 1.1);
  addText(slide, "同桌各说一次", { x: 1.35, y: 5.56, w: 3.6, h: 0.44, fontSize: 26, bold: true, color: C.leaf, align: "center" });
  addText(slide, "→", { x: 5.22, y: 5.59, w: 0.72, h: 0.34, fontSize: 25, color: C.gold, align: "center" });
  addText(slide, "听的人补记一个不同之处", { x: 6.18, y: 5.56, w: 5.0, h: 0.44, fontSize: 25, bold: true, color: C.cinnabar, align: "center" });
  addNotes(slide, page);
}

function renderN011(slide, pres, page) {
  const occurrence = (page.physical_occurrences || []).find((item) => item.occurrence_id === "N011_INPUT");
  if (!occurrence) throw new Error("snapshot missing N011_INPUT");
  base(slide, pres);
  title(slide, "《诗经》与《卫风》");
  const items = [
    ["305篇", "我国最早的诗歌总集", C.gold, C.warm],
    ["《卫风》", "风、雅、颂｜《氓》属于《卫风》", C.river, C.riverSoft],
    ["女子第一人称", "她回望自己的\n婚姻经历", C.cinnabar, C.cinnabarSoft],
  ];
  items.forEach(([head, body, color, fill], index) => {
    const x = 0.8 + index * 4.18;
    rect(slide, pres, x, 1.52, 3.75, 3.24, fill, color, true);
    addText(slide, head, { x: x + 0.3, y: 2.06, w: 3.15, h: 0.68, fontFace: FONT_HEAD, fontSize: index === 2 ? 30 : 36, bold: true, color, align: "center" });
    line(slide, pres, x + 0.72, 3.02, 2.31, color, 1.2);
    addText(slide, body, { x: x + 0.42, y: 3.38, w: 2.91, h: 0.88, fontSize: 21, bold: true, color: C.ink2, align: "center", breakLine: true, valign: "mid" });
  });
  rect(slide, pres, 2.48, 5.58, 8.37, 0.8, C.leafSoft, C.leaf, true);
  addText(slide, occurrence.student_visible_prompt, { x: 2.83, y: 5.79, w: 7.67, h: 0.36, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: C.leaf, align: "center" });
  addNotes(slide, page, "input");
}

function renderN011Recall(slide, pres, page) {
  const occurrence = (page.physical_occurrences || []).find((item) => item.occurrence_id === "N011_RECALL");
  if (!occurrence) throw new Error("snapshot missing N011_RECALL");
  base(slide, pres, true);
  title(slide, "把答案收起来，说出三块路标", { color: C.paper });
  const prompts = ["这是怎样的一部\n诗歌总集？", "《氓》属于\n哪一部分？", "谁在回望\n什么？"];
  prompts.forEach((prompt, index) => {
    const x = 0.82 + index * 4.18;
    const border = [C.gold, C.river, C.cinnabar][index];
    const numberColor = [C.warm, C.riverSoft, C.cinnabarSoft][index];
    rect(slide, pres, x, 1.58, 3.75, 3.42, index === 1 ? "323C3F" : "37322D", border, true);
    addText(slide, `${index + 1}`, { x: x + 1.54, y: 1.98, w: 0.68, h: 0.42, fontSize: 22, bold: true, color: numberColor, align: "center" });
    addText(slide, prompt, { x: x + 0.42, y: 2.74, w: 2.91, h: 1.18, fontFace: FONT_HEAD, fontSize: 29, bold: true, color: C.paper, breakLine: true, align: "center", valign: "mid" });
  });
  addText(slide, occurrence.student_visible_prompt, { x: 2.02, y: 5.74, w: 9.3, h: 0.52, fontSize: 26, bold: true, color: C.warm, align: "center" });
  addNotes(slide, page, "recall");
}

function renderN012(slide, pres, page) {
  base(slide, pres);
  title(slide, "先借四言节奏走进声音");
  rect(slide, pres, 0.82, 1.34, 11.7, 3.2, C.paper2, C.river, true);
  addText(slide, "氓之／蚩蚩，抱布／贸丝。", { x: 1.25, y: 1.84, w: 10.84, h: 0.78, fontFace: FONT_TEXT, fontSize: 44, bold: true, align: "center" });
  addText(slide, "匪来／贸丝，来即／我谋。", { x: 1.25, y: 2.95, w: 10.84, h: 0.78, fontFace: FONT_TEXT, fontSize: 44, bold: true, align: "center" });
  addText(slide, "／只提示节奏，不切碎完整动作", { x: 3.45, y: 4.06, w: 6.43, h: 0.3, fontSize: 20.5, bold: true, color: C.river, align: "center" });
  addText(slide, "跟读一遍  →  听到“看教材”，转看第一章开头的无斜线原句", { x: 1.0, y: 4.79, w: 11.33, h: 0.4, fontFace: FONT_HEAD, fontSize: 23.5, bold: true, color: C.gold, align: "center" });
  const readingPaths = [
    ["停顿需要调整", "听者问“谁做什么？”\n读者带着完整动作再读", C.cinnabar, C.cinnabarSoft],
    ["原本读顺", "圈出连续动作\n再读给同桌听", C.leaf, C.leafSoft],
  ];
  readingPaths.forEach(([head, body, color, fill], index) => {
    const x = 0.95 + index * 6.02;
    rect(slide, pres, x, 5.43, 5.42, 1.24, fill, color, true);
    addText(slide, head, { x: x + 0.3, y: 5.59, w: 4.82, h: 0.32, fontFace: FONT_HEAD, fontSize: 21.5, bold: true, color, align: "center" });
    addText(slide, body, { x: x + 0.3, y: 6.02, w: 4.82, h: 0.48, fontSize: 19.5, bold: true, breakLine: true, align: "center", valign: "mid" });
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
  const snapshot = JSON.parse(fs.readFileSync(SNAPSHOT, "utf8"));
  const pageMap = new Map(snapshot.pages.map((page) => [page.page_id, page]));
  const screenPlan = [
    ["N002", renderN002, "活动界面"],
    ["N003", renderN003, "活动界面"],
    ["N004", renderN004, "活动界面"],
    ["N005", renderN005, "现场共创"],
    ["N001", renderN001, "题名"],
    ["N007", renderN007, "活动界面"],
    ["N008", renderN008, "全文/章内整读"],
    ["N009", renderN009, "全文/章内整读"],
    ["N010", renderN010, "活动界面"],
    ["N011", renderN011, "信息提供"],
    ["N011", renderN011Recall, "撤答检索"],
    ["N012", renderN012, "原文批注"],
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
    artifact: path.relative(ROOT, PPTX).split(path.sep).join("/"),
    sha256: sha256(PPTX),
    source_snapshot_sha256: sha256(SNAPSHOT),
    physical_slides: pages.map((page) => ({
      physical_index: page.physicalIndex,
      page_id: page.page_id,
      primary_visual_duty: page.duty,
      unique_function: page.unique_function,
      artifact_location: page.artifact_location,
    })),
    illustration_policy: "no_character_illustration",
    claim_boundary: "rendered_opening_not_classroom_observed",
  };
  fs.writeFileSync(MANIFEST, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
  process.stdout.write(`OPENING_PPTX_OK slides=${pages.length} pptx=${PPTX}\n`);
}

main().catch((error) => { console.error(error.stack || error); process.exit(1); });
