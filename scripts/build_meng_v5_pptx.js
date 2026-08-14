#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");
const { modules, chapters, slides, totalMinutes } = require("./meng_v5_lesson");

function requireGlobal(name) {
  try {
    return require(name);
  } catch (_) {
    const root = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
    return require(path.join(root, name));
  }
}

const pptxgen = requireGlobal("pptxgenjs");
const npmRoot = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
const JSZip = require(path.join(npmRoot, "pptxgenjs", "node_modules", "jszip"));

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "work", "备课", "选择性必修下册", "氓");
const MASTER = path.join(OUT, "04_氓_V5全文逐句课堂课件_完整母版.pptx");
const MODULE_FILES = {
  M1: path.join(OUT, "04B1_氓_V5模块一_从旧故事走进初见.pptx"),
  M2: path.join(OUT, "04B2_氓_V5模块二_等待与回望中的劝诫.pptx"),
  M3: path.join(OUT, "04B3_氓_V5模块三_婚后事实与长期处境.pptx"),
  M4: path.join(OUT, "04B4_氓_V5模块四_回望六章把她的日子讲出来.pptx"),
  M5: path.join(OUT, "04B5_氓_V5模块五_辨明伤害把提醒留给后来人.pptx"),
};

const W = 13.333;
const H = 7.5;
const FONT_HEAD = "Noto Serif CJK SC";
const FONT_BODY = "Noto Sans CJK SC";
const C = {
  ink: "28211B",
  paper: "F5EBDD",
  paper2: "FCF8F0",
  warm: "EBDCC7",
  leaf: "63744A",
  leafSoft: "DEE5D1",
  river: "4D7481",
  riverSoft: "D8E7EA",
  cinnabar: "A44132",
  cinnabarSoft: "EED8D1",
  gold: "B68B4C",
  goldSoft: "EFE1C5",
  gray: "6E655C",
  pale: "EDE3D5",
  white: "FFFFFF",
  black: "17130F",
};
const MODULE_COLOR = { MASTER: C.ink, M1: C.gold, M2: C.river, M3: C.leaf, M4: C.cinnabar, M5: C.ink };
const MODULE_SOFT = { MASTER: C.pale, M1: C.goldSoft, M2: C.riverSoft, M3: C.leafSoft, M4: C.cinnabarSoft, M5: C.pale };

function presentation() {
  const pres = new pptxgen();
  pres.defineLayout({ name: "CUSTOM_WIDE", width: W, height: H });
  pres.layout = "CUSTOM_WIDE";
  pres.author = "语文备课系统";
  pres.company = "语文备课系统";
  pres.lang = "zh-CN";
  pres.theme = { headFontFace: FONT_HEAD, bodyFontFace: FONT_BODY, lang: "zh-CN" };
  return pres;
}

function addText(slide, text, options = {}) {
  slide.addText(String(text ?? ""), {
    x: 0.7, y: 0.7, w: 11.93, h: 0.5,
    fontFace: FONT_BODY,
    fontSize: 28,
    color: C.ink,
    margin: 0,
    breakLine: false,
    ...options,
  });
}

function shape(slide, SH, type, x, y, w, h, fill, line = null, extra = {}) {
  slide.addShape(type, {
    x, y, w, h,
    fill: { color: fill },
    line: line || { color: fill, transparency: 100 },
    ...extra,
  });
}

function moduleMeta(moduleId) {
  if (moduleId === "MASTER") return { number: "索引", title: "完整母版教师导航", color: C.ink, soft: C.pale };
  const module = modules.find((item) => item.id === moduleId);
  return { ...module, color: MODULE_COLOR[moduleId], soft: MODULE_SOFT[moduleId] };
}

function base(slide, pres, data, localPage, globalPage, dark = false) {
  const SH = pres.shapes;
  const meta = moduleMeta(data.module);
  slide.background = { color: dark ? C.ink : C.paper };
  if (!dark) {
    shape(slide, SH, SH.RECTANGLE, 0, 0, W, 0.13, meta.color);
    shape(slide, SH, SH.OVAL, 11.72, 0.35, 0.88, 0.34, meta.soft, null, { rotate: -18 });
    shape(slide, SH, SH.OVAL, 12.12, 0.54, 0.62, 0.25, meta.color, null, { rotate: 18 });
  } else {
    shape(slide, SH, SH.OVAL, 10.6, 0.35, 2.1, 0.85, C.leaf, null, { rotate: -12, transparency: 15 });
    shape(slide, SH, SH.OVAL, 11.45, 1.02, 1.35, 0.52, C.gold, null, { rotate: 18, transparency: 10 });
  }
  addText(slide, String(localPage).padStart(2, "0"), {
    x: 11.78, y: 7.02, w: 0.82, h: 0.2, fontSize: 17, align: "right",
    color: dark ? C.goldSoft : C.gray,
  });
}

function title(slide, text, options = {}) {
  addText(slide, text, {
    x: 0.7, y: 0.72, w: 11.55, h: 0.68,
    fontFace: FONT_HEAD, fontSize: 38, bold: true,
    color: C.ink, valign: "mid",
    ...options,
  });
}

function card(slide, pres, x, y, w, h, fill = C.paper2, border = C.warm) {
  shape(slide, pres.shapes, pres.shapes.ROUNDED_RECTANGLE, x, y, w, h, fill, { color: border, width: 1.2 }, { rectRadius: 0.06 });
}

function addItems(slide, pres, items, options = {}) {
  const x = options.x ?? 1.0;
  const y = options.y ?? 1.75;
  const w = options.w ?? 11.2;
  const h = options.h ?? 4.75;
  const fontSize = options.fontSize ?? 28;
  const meta = moduleMeta(options.module || "M1");
  const gap = options.gap ?? 0.18;
  const rowH = (h - gap * (items.length - 1)) / items.length;
  items.forEach((item, index) => {
    const rowY = y + index * (rowH + gap);
    card(slide, pres, x, rowY, w, rowH, index % 2 ? C.paper2 : meta.soft, index % 2 ? C.warm : meta.soft);
    shape(slide, pres.shapes, pres.shapes.OVAL, x + 0.22, rowY + Math.max(0.16, (rowH - 0.36) / 2), 0.36, 0.36, meta.color);
    addText(slide, String(index + 1), { x: x + 0.22, y: rowY + Math.max(0.19, (rowH - 0.24) / 2), w: 0.36, h: 0.22, fontSize: 16, bold: true, color: C.white, align: "center" });
    addText(slide, item, { x: x + 0.75, y: rowY + 0.13, w: w - 1.0, h: rowH - 0.26, fontSize, valign: "mid", bold: options.bold ?? false });
  });
}

function actionChain(slide, pres, data) {
  if (!data.chapter || !data.chapter.actionChain) return;
  const actions = data.chapter.actionChain.split(" → ");
  const active = Number(data.lineIndex || 0);
  const x = 0.85;
  const y = 6.25;
  const totalW = 11.65;
  const nodeW = totalW / actions.length;
  actions.forEach((action, index) => {
    const isActive = active === index + 1;
    shape(slide, pres.shapes, pres.shapes.ROUNDED_RECTANGLE, x + index * nodeW + 0.04, y, nodeW - 0.08, 0.52, isActive ? MODULE_COLOR[data.module] : C.pale, { color: isActive ? MODULE_COLOR[data.module] : C.warm, width: 1 }, { rectRadius: 0.04 });
    addText(slide, action, { x: x + index * nodeW + 0.12, y: y + 0.15, w: nodeW - 0.24, h: 0.2, fontSize: 17, bold: isActive, color: isActive ? C.white : C.gray, align: "center" });
  });
}

function renderTeacherIndex(slide, pres, data, moduleStarts) {
  base(slide, pres, data, 1, 1, true);
  addText(slide, "《氓》V5完整母版", { x: 0.85, y: 0.82, w: 7.7, h: 0.72, fontFace: FONT_HEAD, fontSize: 42, bold: true, color: C.white });
  addText(slide, "教师导航 · 本页隐藏，不进入学生正常放映", { x: 0.88, y: 1.62, w: 8.2, h: 0.34, fontSize: 23, color: C.goldSoft });
  modules.forEach((module, index) => {
    const y = 2.28 + index * 0.85;
    const color = MODULE_COLOR[module.id];
    shape(slide, pres.shapes, pres.shapes.ROUNDED_RECTANGLE, 1.0, y, 11.2, 0.66, index % 2 ? "3A322B" : "332B25", { color, width: 1.2 }, { rectRadius: 0.05 });
    addText(slide, `模块${module.number}`, { x: 1.25, y: y + 0.17, w: 1.1, h: 0.23, fontSize: 20, bold: true, color });
    addText(slide, module.title, { x: 2.45, y: y + 0.14, w: 5.1, h: 0.3, fontSize: 25, bold: true, color: C.white });
    addText(slide, `${module.minutes}分钟 · 母版P${moduleStarts[module.id]}`, { x: 8.6, y: y + 0.18, w: 2.9, h: 0.23, fontSize: 18, color: C.goldSoft, align: "right", hyperlink: { slide: moduleStarts[module.id] } });
  });
}

function renderCover(slide, pres, data, localPage, globalPage) {
  base(slide, pres, data, localPage, globalPage, true);
  addText(slide, data.title, { x: 0.9, y: 0.95, w: 3.0, h: 1.3, fontFace: FONT_HEAD, fontSize: 86, bold: true, color: C.white });
  addText(slide, data.subtitle, { x: 3.95, y: 1.2, w: 7.9, h: 0.75, fontFace: FONT_HEAD, fontSize: 43, bold: true, color: C.paper });
  card(slide, pres, 1.05, 3.55, 11.15, 1.45, C.paper2, C.gold);
  addText(slide, data.body, { x: 1.45, y: 3.93, w: 10.35, h: 0.63, fontFace: FONT_HEAD, fontSize: 39, bold: true, color: C.cinnabar, align: "center" });
  addText(slide, "《诗经·卫风》", { x: 1.05, y: 5.72, w: 4.0, h: 0.32, fontSize: 22, color: C.goldSoft });
}

function renderPrior(slide, pres, data, localPage, globalPage) {
  base(slide, pres, data, localPage, globalPage);
  title(slide, data.title);
  if (data.items?.length) {
    const n = data.items.length;
    const gap = 0.28;
    const w = (11.5 - gap * (n - 1)) / n;
    data.items.forEach((item, index) => {
      const x = 0.9 + index * (w + gap);
      card(slide, pres, x, 1.75, w, 3.95, index === 0 ? C.goldSoft : index === 1 ? C.riverSoft : C.cinnabarSoft, C.warm);
      shape(slide, pres.shapes, pres.shapes.OVAL, x + 0.38, 2.12, 0.7, 0.7, [C.gold, C.river, C.cinnabar][index % 3]);
      addText(slide, item, { x: x + 0.4, y: 3.05, w: w - 0.8, h: 1.5, fontSize: 29, bold: true, valign: "mid" });
    });
    if (data.prompt) addText(slide, data.prompt, { x: 1.0, y: 6.05, w: 11.2, h: 0.32, fontSize: 25, bold: true, color: C.cinnabar, align: "center" });
  } else {
    card(slide, pres, 1.0, 1.75, 11.15, 1.35, C.paper2, C.gold);
    addText(slide, data.prompt, { x: 1.45, y: 2.05, w: 10.25, h: 0.72, fontSize: 34, bold: true, align: "center" });
    card(slide, pres, 1.0, 3.5, 11.15, 2.1, C.paper2, C.warm);
    addText(slide, data.body, { x: 1.5, y: 4.0, w: 10.15, h: 1.12, fontSize: 30, color: C.gray, breakLine: true });
  }
}

function renderQuestion(slide, pres, data, localPage, globalPage) {
  const dark = data.phase === "return";
  base(slide, pres, data, localPage, globalPage, dark);
  const color = dark ? C.white : C.ink;
  if (data.kind === "question_overview") {
    addText(slide, data.title, { x: 0.8, y: 0.92, w: 11.7, h: 0.6, fontFace: FONT_HEAD, fontSize: 40, bold: true, color });
    const colors = [C.gold, C.river, C.cinnabar];
    data.items.forEach((item, index) => {
      const x = 1.0 + index * 4.05;
      shape(slide, pres.shapes, pres.shapes.OVAL, x + 0.97, 2.0, 1.35, 1.35, colors[index]);
      addText(slide, String(index + 1), { x: x + 0.97, y: 2.28, w: 1.35, h: 0.52, fontSize: 34, bold: true, color: C.white, align: "center" });
      addText(slide, item, { x, y: 3.48, w: 3.3, h: 1.05, fontSize: 28, bold: true, color, align: "center", valign: "mid", breakLine: true });
    });
    addText(slide, dark ? "带着六章诗句，重新回答" : "先保存问题，六章之后再回答", { x: 1.5, y: 5.25, w: 10.3, h: 0.36, fontSize: 27, color: dark ? C.goldSoft : C.gray, align: "center" });
    return;
  }
  addText(slide, data.title, { x: 0.85, y: 1.05, w: 2.0, h: 0.4, fontSize: 23, bold: true, color: dark ? C.goldSoft : MODULE_COLOR[data.module] });
  if (data.question_index === 3) {
    const questions = [
      ["谁伤害了她？", "诗把哪些行为清楚地写在男子身上？"],
      ["停止以后呢？", "她说出“亦已焉哉”，还会面对哪些现实阻力？"],
    ];
    questions.forEach(([label, question], index) => {
      const y = 1.65 + index * 2.22;
      card(slide, pres, 0.95, y, 11.45, 1.82, dark ? (index ? "3A322B" : "332B25") : (index ? C.cinnabarSoft : C.paper2), dark ? C.gold : C.warm);
      addText(slide, label, { x: 1.35, y: y + 0.2, w: 2.05, h: 0.3, fontSize: 23, bold: true, color: dark ? C.goldSoft : C.cinnabar });
      addText(slide, question, { x: 3.65, y: y + 0.16, w: 8.1, h: 0.72, fontFace: FONT_HEAD, fontSize: 29, bold: true, color, valign: "mid" });
      addText(slide, dark ? "读一读最初那句话，再用六章诗句回答" : "写下此刻最朴素的猜想，也可以留下问号", { x: 3.65, y: y + 1.15, w: 8.0, h: 0.28, fontSize: 21, color: dark ? C.goldSoft : C.gray });
    });
    return;
  }
  card(slide, pres, 0.95, 1.75, 11.45, 3.55, dark ? "332B25" : C.paper2, dark ? C.gold : C.warm);
  addText(slide, data.body, { x: 1.5, y: 2.35, w: 10.35, h: 2.2, fontFace: FONT_HEAD, fontSize: data.question_index === 3 ? 37 : 43, bold: true, color, align: "center", valign: "mid" });
  addText(slide, data.phase === "return" ? "回看最初的猜想：保留 / 修正 / 推翻" : "先写一个不超过15字的猜想；证据可以空着", { x: 1.2, y: 5.72, w: 10.9, h: 0.34, fontSize: 24, color: dark ? C.goldSoft : C.gray, align: "center" });
}

function renderFullRead(slide, pres, data, localPage, globalPage) {
  base(slide, pres, data, localPage, globalPage, true);
  addText(slide, data.title, { x: 0.75, y: 0.78, w: 11.75, h: 0.55, fontFace: FONT_HEAD, fontSize: 36, bold: true, color: C.white });
  const pieces = data.body.split("\n\n");
  const gap = 0.28;
  const colW = (11.7 - gap * (pieces.length - 1)) / pieces.length;
  pieces.forEach((piece, index) => {
    const x = 0.82 + index * (colW + gap);
    card(slide, pres, x, 1.55, colW, 4.95, index % 2 ? "382F28" : "322A24", C.gold);
    addText(slide, piece, { x: x + 0.28, y: 1.92, w: colW - 0.56, h: 4.2, fontFace: FONT_HEAD, fontSize: 28, color: C.paper, breakLine: true, valign: "mid", align: "left", paraSpaceAfterPt: 9, lineSpacingMultiple: 1.1 });
  });
}

function renderBackground(slide, pres, data, localPage, globalPage) {
  base(slide, pres, data, localPage, globalPage);
  title(slide, data.title);
  if (data.items && !data.body) addItems(slide, pres, data.items, { x: 1.0, y: 1.75, w: 11.2, h: 4.75, fontSize: 28, module: data.module });
  if (data.body) {
    card(slide, pres, 1.0, 1.75, 11.2, 2.0, C.paper2, C.warm);
    addText(slide, data.body, { x: 1.45, y: 2.25, w: 10.3, h: 1.0, fontFace: FONT_HEAD, fontSize: 37, bold: true, align: "center", breakLine: true });
    if (data.items) addItems(slide, pres, data.items, { x: 1.25, y: 4.25, w: 10.7, h: 1.65, fontSize: 28, module: data.module });
  }
}

function renderMark(slide, pres, data, localPage, globalPage) {
  base(slide, pres, data, localPage, globalPage);
  title(slide, data.title);
  card(slide, pres, 1.0, 1.8, 11.2, 3.9, C.paper2, C.gold);
  addText(slide, data.prompt, { x: 1.5, y: 2.3, w: 10.2, h: 0.75, fontSize: 33, bold: true, align: "center" });
  addText(slide, data.body, { x: 1.8, y: 3.55, w: 9.65, h: 1.35, fontSize: 31, color: C.gray, breakLine: true, align: "center" });
}

function renderChapterText(slide, pres, data, localPage, globalPage) {
  const end = data.phase === "end";
  base(slide, pres, data, localPage, globalPage, end);
  addText(slide, data.title, { x: 0.75, y: 0.77, w: 11.75, h: 0.58, fontFace: FONT_HEAD, fontSize: 37, bold: true, color: end ? C.white : C.ink });
  card(slide, pres, 0.95, 1.55, 11.45, 3.95, end ? "332B25" : C.paper2, end ? MODULE_COLOR[data.module] : C.warm);
  addText(slide, data.body, { x: 1.45, y: 2.03, w: 10.45, h: 2.95, fontFace: FONT_HEAD, fontSize: 35, color: end ? C.paper : C.ink, align: "center", valign: "mid", breakLine: true, paraSpaceAfterPt: 12 });
  addText(slide, end ? data.chapter.actionChain : "先完整朗读，再逐句照亮", { x: 1.1, y: 5.85, w: 11.1, h: 0.42, fontSize: 24, bold: true, color: end ? C.goldSoft : MODULE_COLOR[data.module], align: "center" });
}

function renderLine(slide, pres, data, localPage, globalPage) {
  base(slide, pres, data, localPage, globalPage);
  title(slide, data.title, { fontSize: 31, color: MODULE_COLOR[data.module] });
  card(slide, pres, 0.95, 1.55, 11.45, data.translation ? 2.0 : 3.45, C.paper2, MODULE_COLOR[data.module]);
  addText(slide, data.original, { x: 1.4, y: 2.02, w: 10.55, h: 0.8, fontFace: FONT_HEAD, fontSize: 53, bold: true, align: "center" });
  if (data.translation) {
    addText(slide, data.translation, { x: 1.4, y: 3.02, w: 10.55, h: 0.55, fontSize: 31, color: C.cinnabar, align: "center" });
    card(slide, pres, 1.2, 4.0, 10.95, 1.55, MODULE_SOFT[data.module], C.warm);
    addText(slide, data.line.keywords, { x: 1.6, y: 4.42, w: 10.15, h: 0.72, fontSize: 24, color: C.gray, align: "center", valign: "mid" });
  } else {
    addText(slide, "借注释口译：谁在做什么？", { x: 1.5, y: 3.42, w: 10.35, h: 0.42, fontSize: 29, color: C.cinnabar, align: "center" });
  }
  actionChain(slide, pres, data);
}

function renderKey(slide, pres, data, localPage, globalPage) {
  base(slide, pres, data, localPage, globalPage);
  title(slide, data.title, { fontSize: 31, color: MODULE_COLOR[data.module] });
  card(slide, pres, 0.9, 1.5, 5.65, 3.95, C.paper2, MODULE_COLOR[data.module]);
  const balancedOriginal = data.original.includes("，") ? data.original.replace("，", "，\n") : data.original;
  addText(slide, balancedOriginal, { x: 1.25, y: 1.82, w: 4.95, h: 1.18, fontFace: FONT_HEAD, fontSize: 40, bold: true, align: "center", valign: "mid", breakLine: true });
  addText(slide, data.translation, { x: 1.3, y: 3.05, w: 4.85, h: 0.72, fontSize: 29, color: C.cinnabar, align: "center", valign: "mid" });
  addText(slide, data.line.form, { x: 1.35, y: 4.05, w: 4.75, h: 0.85, fontSize: 25, color: C.gray, align: "center", valign: "mid" });
  card(slide, pres, 6.85, 1.5, 5.55, 3.95, MODULE_SOFT[data.module], C.warm);
  addText(slide, "这句使我们看见……", { x: 7.25, y: 1.95, w: 4.75, h: 0.38, fontSize: 26, bold: true, color: MODULE_COLOR[data.module] });
  addText(slide, data.items[0], { x: 7.25, y: 2.62, w: 4.75, h: 2.15, fontSize: 27, color: C.ink, valign: "mid" });
  actionChain(slide, pres, data);
}

function renderActivity(slide, pres, data, localPage, globalPage) {
  const isReturn = data.phase === "return";
  base(slide, pres, data, localPage, globalPage, isReturn);
  addText(slide, data.title, { x: 0.75, y: 0.78, w: 11.75, h: 0.6, fontFace: FONT_HEAD, fontSize: 37, bold: true, color: isReturn ? C.white : C.ink });
  if (isReturn) {
    addItems(slide, pres, data.items, { x: 0.95, y: 1.65, w: 11.45, h: 4.75, fontSize: 27, module: data.module });
    addText(slide, "先核对自己的产出，再修改一处", { x: 1.1, y: 6.58, w: 11.05, h: 0.28, fontSize: 22, color: C.goldSoft, align: "center" });
  } else {
    card(slide, pres, 0.95, 1.65, 11.45, 1.65, C.paper2, MODULE_COLOR[data.module]);
    addText(slide, data.prompt, { x: 1.45, y: 2.05, w: 10.45, h: 0.85, fontSize: 32, bold: true, align: "center", valign: "mid" });
    card(slide, pres, 1.15, 3.72, 11.05, 2.15, MODULE_SOFT[data.module], C.warm);
    addText(slide, data.body, { x: 1.65, y: 4.22, w: 10.05, h: 1.12, fontSize: 29, color: C.gray, breakLine: true, align: "center" });
  }
}

function renderReconnect(slide, pres, data, localPage, globalPage) {
  base(slide, pres, data, localPage, globalPage, true);
  addText(slide, data.title, { x: 0.8, y: 0.9, w: 11.7, h: 0.65, fontFace: FONT_HEAD, fontSize: 42, bold: true, color: C.white });
  card(slide, pres, 1.0, 2.0, 11.2, 2.4, "332B25", MODULE_COLOR[data.module]);
  addText(slide, data.body, { x: 1.35, y: 2.58, w: 10.5, h: 0.96, fontSize: 32, bold: true, color: C.paper, align: "center", valign: "mid" });
  addText(slide, data.prompt, { x: 1.05, y: 5.05, w: 11.2, h: 0.45, fontSize: 25, color: C.goldSoft, align: "center" });
}

function renderSynthesis(slide, pres, data, localPage, globalPage) {
  const darkKinds = new Set([
    "story_revise", "scene_revise", "responsibility_after", "responsibility_boundary",
    "first_heat_after", "marriage_after",
  ]);
  const dark = darkKinds.has(data.kind);
  base(slide, pres, data, localPage, globalPage, dark);
  addText(slide, data.title, { x: 0.75, y: 0.78, w: 11.75, h: 0.62, fontFace: FONT_HEAD, fontSize: 37, bold: true, color: dark ? C.white : C.ink });
  const color = dark ? C.paper : C.ink;
  if (data.kind === "story_prepare") {
    addText(slide, data.prompt, { x: 0.95, y: 1.48, w: 11.45, h: 0.55, fontSize: 25, bold: true, color: C.cinnabar, align: "center", valign: "mid" });
    data.items.forEach((item, index) => {
      const column = index % 2;
      const row = Math.floor(index / 2);
      const x = 0.95 + column * 5.82;
      const y = 2.25 + row * 1.25;
      card(slide, pres, x, y, 5.55, 0.92, index % 2 ? C.paper2 : C.cinnabarSoft, C.warm);
      shape(slide, pres.shapes, pres.shapes.OVAL, x + 0.28, y + 0.24, 0.44, 0.44, MODULE_COLOR[data.module]);
      addText(slide, String(index + 1), { x: x + 0.28, y: y + 0.32, w: 0.44, h: 0.2, fontSize: 16, bold: true, color: C.white, align: "center" });
      addText(slide, item, { x: x + 0.95, y: y + 0.2, w: 4.15, h: 0.48, fontSize: 25, bold: true, valign: "mid" });
    });
    addText(slide, "先让每个人写一句，再把几个人的句子合成一段。", { x: 1.2, y: 6.28, w: 10.9, h: 0.34, fontSize: 23, color: C.gray, align: "center" });
    return;
  }
  if (data.kind === "responsibility_choose") {
    addText(slide, data.prompt, { x: 0.95, y: 1.46, w: 11.45, h: 0.44, fontSize: 26, bold: true, color: C.cinnabar, align: "center" });
    data.items.forEach((item, index) => {
      const column = index % 2;
      const row = Math.floor(index / 2);
      const x = 0.95 + column * 5.82;
      const y = 2.02 + row * 1.12;
      card(slide, pres, x, y, 5.55, 0.82, index % 2 ? C.paper2 : C.cinnabarSoft, C.warm);
      addText(slide, item, { x: x + 0.3, y: y + 0.21, w: 4.95, h: 0.38, fontFace: FONT_HEAD, fontSize: 25, bold: true, align: "center", valign: "mid" });
    });
    card(slide, pres, 1.15, 4.58, 11.05, 1.55, C.paper2, C.cinnabar);
    addText(slide, data.body, { x: 1.65, y: 4.94, w: 10.05, h: 0.82, fontSize: 27, bold: true, color: C.ink, align: "center", valign: "mid", breakLine: true });
    return;
  }
  if (data.kind === "story_revise") {
    card(slide, pres, 0.95, 1.62, 11.45, 2.35, "332B25", C.gold);
    addText(slide, data.body, { x: 1.35, y: 2.05, w: 10.65, h: 1.45, fontFace: FONT_HEAD, fontSize: 29, bold: true, color: C.paper, align: "center", valign: "mid", breakLine: true });
    addItems(slide, pres, data.items, { x: 1.05, y: 4.42, w: 11.2, h: 1.58, fontSize: 24, module: data.module, gap: 0.18 });
    return;
  }
  if (data.kind === "marriage_after") {
    card(slide, pres, 0.95, 1.55, 11.45, 4.55, "332B25", C.gold);
    addText(slide, data.body, { x: 1.5, y: 2.05, w: 10.35, h: 3.15, fontFace: FONT_HEAD, fontSize: 27, bold: true, color: C.paper, align: "center", valign: "mid", breakLine: true, paraSpaceAfterPt: 11 });
    addText(slide, data.prompt, { x: 1.25, y: 6.35, w: 10.85, h: 0.35, fontSize: 22, color: C.goldSoft, align: "center" });
    return;
  }
  if (data.kind === "first_heat_after") {
    addItems(slide, pres, data.items, { x: 0.95, y: 1.62, w: 11.45, h: 4.8, fontSize: 25, module: data.module });
    return;
  }
  if (data.kind === "q1_activity") {
    addText(slide, data.prompt, { x: 1.0, y: 1.48, w: 11.3, h: 0.38, fontSize: 25, bold: true, color: C.cinnabar, align: "center" });
    data.items.forEach((item, index) => {
      const column = index % 2;
      const row = Math.floor(index / 2);
      const x = 1.0 + column * 5.78;
      const y = 2.05 + row * 1.04;
      card(slide, pres, x, y, 5.5, 0.78, index % 2 ? C.paper2 : MODULE_SOFT[data.module], C.warm);
      shape(slide, pres.shapes, pres.shapes.OVAL, x + 0.24, y + 0.19, 0.4, 0.4, MODULE_COLOR[data.module]);
      addText(slide, String.fromCharCode(65 + index), { x: x + 0.24, y: y + 0.27, w: 0.4, h: 0.18, fontSize: 16, bold: true, color: C.white, align: "center" });
      addText(slide, item, { x: x + 0.82, y: y + 0.18, w: 4.3, h: 0.4, fontSize: 28, bold: true, valign: "mid" });
    });
    return;
  }
  if (data.kind === "retrospective" && data.prompt && data.items?.length) {
    card(slide, pres, 0.95, 1.55, 11.45, 1.18, C.paper2, MODULE_COLOR[data.module]);
    addText(slide, data.prompt, { x: 1.35, y: 1.82, w: 10.65, h: 0.68, fontSize: 29, bold: true, align: "center", valign: "mid", breakLine: true });
    addItems(slide, pres, data.items, { x: 1.0, y: 3.05, w: 11.2, h: 3.15, fontSize: 28, module: data.module });
    return;
  }
  if (data.prompt && data.body) {
    card(slide, pres, 0.95, 1.6, 11.45, 1.6, dark ? "332B25" : C.paper2, dark ? C.gold : C.warm);
    addText(slide, data.prompt, { x: 1.35, y: 1.98, w: 10.65, h: 0.8, fontSize: data.kind === "first_heat" ? 29 : 31, bold: true, color, align: "center", valign: "mid" });
    card(slide, pres, 1.05, 3.58, 11.25, 2.2, dark ? "3A322B" : MODULE_SOFT[data.module], dark ? MODULE_COLOR[data.module] : C.warm);
    addText(slide, data.body, { x: 1.55, y: 4.03, w: 10.25, h: 1.25, fontSize: 30, color: dark ? C.goldSoft : C.gray, align: "center", valign: "mid", breakLine: true });
  } else if (data.body && !data.items?.length) {
    card(slide, pres, 0.95, 1.7, 11.45, 3.95, dark ? "332B25" : C.paper2, dark ? MODULE_COLOR[data.module] : C.warm);
    addText(slide, data.body, { x: 1.45, y: 2.35, w: 10.45, h: 2.6, fontSize: data.kind === "boundary" ? 34 : 32, bold: true, color, align: "center", valign: "mid", breakLine: true });
    if (data.prompt) addText(slide, data.prompt, { x: 1.2, y: 5.9, w: 10.9, h: 0.38, fontSize: 25, color: dark ? C.goldSoft : C.cinnabar, align: "center" });
  } else if (data.items?.length) {
    if (data.body) {
      addText(slide, data.body, { x: 1.0, y: 1.53, w: 11.3, h: 0.7, fontSize: 29, bold: true, color, align: "center", valign: "mid", breakLine: true });
      addItems(slide, pres, data.items, { x: 1.0, y: 2.52, w: 11.2, h: 3.8, fontSize: data.items.length >= 5 ? 22 : data.items.length === 4 ? 24 : 28, module: data.module });
    } else if (data.prompt) {
      addText(slide, data.prompt, { x: 0.95, y: 1.46, w: 11.45, h: 0.55, fontSize: 25, bold: true, color: dark ? C.goldSoft : C.cinnabar, align: "center", valign: "mid", breakLine: true });
      addItems(slide, pres, data.items, { x: 0.95, y: 2.25, w: 11.45, h: 4.05, fontSize: data.items.length >= 5 ? 22 : data.items.length === 4 ? 24 : 27, module: data.module });
    } else {
      addItems(slide, pres, data.items, { x: 0.95, y: 1.62, w: 11.45, h: 4.8, fontSize: data.items.length >= 5 ? 22 : data.items.length === 4 ? 24 : 28, module: data.module });
    }
  } else if (data.prompt) {
    card(slide, pres, 0.95, 1.65, 11.45, 4.2, C.paper2, MODULE_COLOR[data.module]);
    addText(slide, data.prompt, { x: 1.45, y: 2.55, w: 10.45, h: 2.25, fontSize: 34, bold: true, align: "center", valign: "mid", breakLine: true });
  }
}

function renderKnowledge(slide, pres, data, localPage, globalPage) {
  const isReturn = data.phase === "return";
  base(slide, pres, data, localPage, globalPage, isReturn);
  addText(slide, data.title, { x: 0.75, y: 0.78, w: 11.75, h: 0.62, fontFace: FONT_HEAD, fontSize: 37, bold: true, color: isReturn ? C.white : C.ink });
  if (isReturn) {
    addItems(slide, pres, data.items, { x: 0.95, y: 1.65, w: 11.45, h: 4.85, fontSize: data.items.length === 2 ? 28 : 25, module: data.module });
  } else {
    card(slide, pres, 1.0, 1.85, 11.2, 3.7, C.paper2, MODULE_COLOR[data.module]);
    addText(slide, data.prompt, { x: 1.55, y: 2.75, w: 10.1, h: 1.8, fontSize: 34, bold: true, align: "center", valign: "mid" });
    addText(slide, "先检索，再翻页核对", { x: 1.2, y: 5.95, w: 10.9, h: 0.36, fontSize: 24, color: C.cinnabar, align: "center" });
  }
}

function renderExit(slide, pres, data, localPage, globalPage) {
  base(slide, pres, data, localPage, globalPage, true);
  addText(slide, data.title, { x: 0.8, y: 0.85, w: 11.7, h: 0.62, fontFace: FONT_HEAD, fontSize: 42, bold: true, color: C.white });
  card(slide, pres, 1.0, 1.8, 11.2, 3.7, "332B25", C.gold);
  addText(slide, data.body, { x: 1.55, y: 2.6, w: 10.1, h: 1.9, fontSize: 32, color: C.paper, align: "center", valign: "mid", breakLine: true });
  addText(slide, data.subtitle, { x: 1.2, y: 5.9, w: 10.9, h: 0.48, fontFace: FONT_HEAD, fontSize: 31, bold: true, color: C.goldSoft, align: "center" });
}

function renderSlide(pres, data, localPage, globalPage, moduleStarts, notesText) {
  const slide = pres.addSlide();
  const renderers = {
    teacher_index: () => renderTeacherIndex(slide, pres, data, moduleStarts),
    cover: () => renderCover(slide, pres, data, localPage, globalPage),
    prior: () => renderPrior(slide, pres, data, localPage, globalPage),
    question_overview: () => renderQuestion(slide, pres, data, localPage, globalPage),
    question: () => renderQuestion(slide, pres, data, localPage, globalPage),
    full_read: () => renderFullRead(slide, pres, data, localPage, globalPage),
    mark: () => renderMark(slide, pres, data, localPage, globalPage),
    background: () => renderBackground(slide, pres, data, localPage, globalPage),
    checkpoint: () => renderReconnect(slide, pres, data, localPage, globalPage),
    chapter_text: () => renderChapterText(slide, pres, data, localPage, globalPage),
    line: () => renderLine(slide, pres, data, localPage, globalPage),
    key: () => renderKey(slide, pres, data, localPage, globalPage),
    activity: () => renderActivity(slide, pres, data, localPage, globalPage),
    module_reconnect: () => renderReconnect(slide, pres, data, localPage, globalPage),
    knowledge: () => renderKnowledge(slide, pres, data, localPage, globalPage),
    exit: () => renderExit(slide, pres, data, localPage, globalPage),
  };
  const renderer = renderers[data.kind] || (() => renderSynthesis(slide, pres, data, localPage, globalPage));
  renderer();
  slide.addNotes(notesText);
  return slide;
}

function validateObjects(pres, expected) {
  const errors = [];
  if (pres._slides.length !== expected) errors.push(`expected ${expected} slides, got ${pres._slides.length}`);
  pres._slides.forEach((slide, slideIndex) => {
    if (!slide._slideObjects.some((object) => object._type === "notes")) errors.push(`slide ${slideIndex + 1}: missing notes`);
    slide._slideObjects.forEach((object, objectIndex) => {
      const o = object.options || {};
      if ([o.x, o.y, o.w, o.h].every((value) => typeof value === "number")) {
        if (o.x < -0.01 || o.y < -0.01 || o.x + o.w > W + 0.01 || o.y + o.h > H + 0.01) {
          errors.push(`slide ${slideIndex + 1} object ${objectIndex + 1} out of bounds`);
        }
      }
    });
  });
  if (errors.length) throw new Error(errors.join("\n"));
}

async function repairPackage(fileName, hideFirst) {
  const zip = await JSZip.loadAsync(fs.readFileSync(fileName));
  const entry = zip.file("ppt/presentation.xml");
  if (!entry) throw new Error("missing ppt/presentation.xml");
  let xml = await entry.async("string");
  const notesMaster = xml.match(/<p:notesMasterIdLst>[\s\S]*?<\/p:notesMasterIdLst>/);
  if (notesMaster) {
    xml = xml.replace(notesMaster[0], "");
    xml = xml.replace(/(<p:sldMasterIdLst>[\s\S]*?<\/p:sldMasterIdLst>)/, `$1${notesMaster[0]}`);
  }
  if (hideFirst) {
    const firstSlide = zip.file("ppt/slides/slide1.xml");
    if (!firstSlide) throw new Error("missing ppt/slides/slide1.xml");
    let firstSlideXml = await firstSlide.async("string");
    firstSlideXml = firstSlideXml.replace(/(<p:sld\b[^>]*?)(>)/, (match, start, end) => start.includes("show=") ? match : `${start} show="0"${end}`);
    zip.file("ppt/slides/slide1.xml", firstSlideXml);
  }
  zip.file("ppt/presentation.xml", xml);
  fs.writeFileSync(fileName, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

async function buildFile(fileName, selected, options = {}) {
  const pres = presentation();
  pres.subject = "《氓》V5全文逐句教学母版";
  pres.title = options.title;
  const moduleStarts = {};
  slides.forEach((slide, index) => {
    if (slide.module !== "MASTER" && !(slide.module in moduleStarts)) moduleStarts[slide.module] = index + 1;
  });
  selected.forEach((data, localIndex) => {
    const globalIndex = slides.indexOf(data) + 1;
    const notesText = options.moduleId
      ? `【模块课件】${options.moduleId}-P${localIndex + 1}｜母版P${globalIndex}\n${data.notes}`
      : data.notes;
    renderSlide(pres, data, localIndex + 1, globalIndex, moduleStarts, notesText);
  });
  validateObjects(pres, selected.length);
  fs.mkdirSync(path.dirname(fileName), { recursive: true });
  await pres.writeFile({ fileName, compression: true });
  await repairPackage(fileName, Boolean(options.hideFirst));
  console.log(`${path.relative(ROOT, fileName)}\t${selected.length} slides\t${fs.statSync(fileName).size} bytes`);
}

async function main() {
  await buildFile(MASTER, slides, { title: "《氓》V5全文逐句课堂课件（完整母版）", hideFirst: true });
  for (const module of modules) {
    const selected = slides.filter((slide) => slide.module === module.id);
    await buildFile(MODULE_FILES[module.id], selected, { title: `《氓》V5模块${module.number}：${module.title}`, moduleId: module.id });
  }
  console.log(`master=${slides.length} slides\tmodules=${modules.length}\ttotal=${totalMinutes} minutes`);
}

main().catch((error) => {
  console.error(error.stack || error);
  process.exit(1);
});
