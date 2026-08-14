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
const root = process.env.NODE_GLOBAL_ROOT || "/usr/local/node-v22.22.2-linux-x64/lib/node_modules";
const JSZip = require(path.join(root, "pptxgenjs", "node_modules", "jszip"));
const source = require("./meng_v62/content/synthesis");
const { validate } = require("./verify_meng_v62_synthesis");
const { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");

const SNAP = path.join(stageDir(), "synthesis", "package", "06_氓_V64全文综合课程数据快照.json");
const OUT = assertV62OutputPath(path.join(stageDir(), "synthesis", "pptx"));
const PPTX = assertV62OutputPath(path.join(OUT, "04_氓_V64全文综合课堂课件.pptx"));
const MANIFEST = assertV62OutputPath(path.join(OUT, "synthesis_v64_pptx_manifest.json"));
const W = 13.333;
const H = 7.5;
const FONT_H = "Noto Serif CJK SC";
const FONT_B = "Noto Sans CJK SC";
const COLORS = {
  ink: "29241F", ink2: "51483F", paper: "F6F0E5", paper2: "FFFCF7",
  warm: "E5DAC9", red: "9C4538", redSoft: "F0DDD5", river: "456F7C",
  riverSoft: "DDE9E9", leaf: "647752", leafSoft: "E1E7D9", gold: "AC8550",
  goldSoft: "EFE4D2", plum: "75515E", plumSoft: "EADDE1", night: "28241F",
  night2: "38312A", creamText: "F8F1E7",
};

function sha(filePath) { return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex"); }
function presentation() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: "MENG_WIDE", width: W, height: H });
  pptx.layout = "MENG_WIDE";
  pptx.author = "语文备课系统";
  pptx.title = "《氓》V6.4全文综合课堂课件";
  pptx.lang = "zh-CN";
  pptx.theme = { headFontFace: FONT_H, bodyFontFace: FONT_B, lang: "zh-CN" };
  return pptx;
}
function text(slide, value, options = {}) {
  slide.addText(value, {
    x: 0.72, y: 0.52, w: 11.9, h: 0.5, margin: 0,
    fontFace: FONT_B, fontSize: 28, color: COLORS.ink, valign: "mid", ...options,
  });
}
function rect(slide, pptx, x, y, w, h, fill, line = fill, radius = false, width = 1) {
  slide.addShape(radius ? pptx.shapes.ROUNDED_RECTANGLE : pptx.shapes.RECTANGLE, {
    x, y, w, h, fill: { color: fill }, line: { color: line, width }, ...(radius ? { rectRadius: 0.05 } : {}),
  });
}
function line(slide, pptx, x, y, w, color, width = 1, dashType = "solid") {
  slide.addShape(pptx.shapes.LINE, { x, y, w, h: 0, line: { color, width, dashType } });
}
function base(slide, pptx, dark = false, accent = COLORS.ink) {
  slide.background = { color: dark ? COLORS.night : COLORS.paper };
  rect(slide, pptx, 0, 0, W, 0.12, accent);
}
function title(slide, value, dark = false) {
  text(slide, value, { x: 0.76, y: 0.36, w: 10.8, h: 0.64, fontFace: FONT_H, fontSize: 34, bold: true, color: dark ? COLORS.creamText : COLORS.ink });
  text(slide, "全文综合", { x: 11.1, y: 0.5, w: 1.5, h: 0.3, fontSize: 16.5, bold: true, color: dark ? COLORS.goldSoft : COLORS.red, align: "right" });
}
function notesFor(page) {
  const s = page.script;
  return [
    `【V6.4页ID】${page.page_id}｜${page.title}｜${page.minutes}分钟`,
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

function renderS01(slide, pptx, page) {
  base(slide, pptx, false, COLORS.ink);
  title(slide, "一｜她经历了什么？");
  text(slide, "沿着桌上的六张章末卡，用六句话，把她的一生讲清。", { x: 1.15, y: 1.28, w: 11.03, h: 0.5, fontFace: FONT_H, fontSize: 28, bold: true, align: "center" });
  line(slide, pptx, 1.15, 3.25, 11.0, COLORS.warm, 2);
  const labels = ["一", "二", "三", "四", "五", "六"];
  const colors = [COLORS.gold, COLORS.river, COLORS.leaf, COLORS.red, COLORS.plum, COLORS.ink2];
  labels.forEach((label, index) => {
    const x = 1.05 + index * 2.02;
    slide.addShape(pptx.shapes.OVAL, { x, y: 2.75, w: 0.95, h: 0.95, fill: { color: COLORS.paper2 }, line: { color: colors[index], width: 2.2 } });
    text(slide, label, { x, y: 2.99, w: 0.95, h: 0.38, fontFace: FONT_H, fontSize: 24, bold: true, color: colors[index], align: "center" });
    if (index < 5) line(slide, pptx, x + 0.95, 3.23, 1.07, colors[index], 1.6);
  });
  text(slide, "哪一步，改变了下一步？", { x: 2.1, y: 4.48, w: 9.13, h: 0.62, fontFace: FONT_H, fontSize: 36, bold: true, color: COLORS.plum, align: "center" });
  text(slide, "有断点，回诗补回；没有断点，说出最清楚的一处因果。", { x: 1.65, y: 5.62, w: 10.03, h: 0.46, fontSize: 22, bold: true, color: COLORS.ink2, align: "center" });
  addNotes(slide, page);
}

function renderS02(slide, pptx, page) {
  base(slide, pptx, false, COLORS.river);
  title(slide, "二｜她婚后的不幸，在生活中是什么样子？");
  rect(slide, pptx, 0.9, 1.25, 7.7, 4.9, COLORS.paper2, COLORS.warm, true, 1.1);
  text(slide, "从第四、第五章选一句，写成一个能被看见的日常片刻。", { x: 1.25, y: 1.7, w: 7.0, h: 0.66, fontFace: FONT_H, fontSize: 29, bold: true, color: COLORS.ink, align: "center" });
  line(slide, pptx, 1.45, 3.0, 6.6, COLORS.river, 1.3, "dash");
  text(slide, "谁在做什么？", { x: 1.35, y: 3.45, w: 3.0, h: 0.5, fontFace: FONT_H, fontSize: 30, bold: true, color: COLORS.river, align: "center" });
  text(slide, "日子怎样一天天过去？", { x: 4.15, y: 3.45, w: 4.0, h: 0.5, fontFace: FONT_H, fontSize: 30, bold: true, color: COLORS.plum, align: "center" });
  text(slide, "________________________________________", { x: 1.42, y: 4.55, w: 6.65, h: 0.4, fontSize: 23, color: COLORS.warm, align: "center" });
  text(slide, "________________________________________", { x: 1.42, y: 5.15, w: 6.65, h: 0.4, fontSize: 23, color: COLORS.warm, align: "center" });
  rect(slide, pptx, 9.02, 1.65, 3.4, 3.95, COLORS.riverSoft, COLORS.river, true, 1.15);
  text(slide, "让同伴从你的文字里，找回原诗。", { x: 9.38, y: 2.25, w: 2.68, h: 1.15, fontFace: FONT_H, fontSize: 27, bold: true, color: COLORS.river, align: "center", valign: "mid" });
  text(slide, "能配回：保留\n配不回：返诗", { x: 9.42, y: 4.15, w: 2.6, h: 0.8, fontSize: 21, bold: true, color: COLORS.ink2, align: "center", breakLine: false });
  addNotes(slide, page);
}

function renderS03(slide, pptx, page) {
  base(slide, pptx, true, COLORS.red);
  title(slide, "三｜这场婚姻为什么走到这一步？", true);
  const questions = [
    ["婚前", "有哪些细节值得警惕？", COLORS.goldSoft],
    ["婚后", "谁直接造成了伤害？", COLORS.redSoft],
    ["处境", "为什么那么难停下来？", COLORS.riverSoft],
    ["边界", "诗里还有什么不能武断？", COLORS.plumSoft],
  ];
  questions.forEach(([tag, question, color], index) => {
    const y = 1.35 + index * 1.2;
    text(slide, tag, { x: 1.02, y: y + 0.13, w: 1.25, h: 0.4, fontSize: 19, bold: true, color, align: "center" });
    line(slide, pptx, 2.35, y + 0.34, 0.6, color, 2.5);
    text(slide, question, { x: 3.2, y, w: 8.6, h: 0.66, fontFace: FONT_H, fontSize: 31, bold: true, color: COLORS.creamText });
  });
  text(slide, "让每一层，都有原句可回。", { x: 2.0, y: 6.35, w: 9.33, h: 0.42, fontFace: FONT_H, fontSize: 27, bold: true, color: COLORS.goldSoft, align: "center" });
  addNotes(slide, page);
}

function renderS04(slide, pptx, page) {
  base(slide, pptx, false, COLORS.gold);
  title(slide, "读完《氓》，再看开课时的爱情与婚姻主题");
  rect(slide, pptx, 0.85, 1.28, 3.65, 5.15, COLORS.goldSoft, COLORS.gold, true, 1.1);
  text(slide, "开课时，\n我们曾这样谈\n爱情与婚姻……", { x: 1.22, y: 1.82, w: 2.9, h: 1.45, fontFace: FONT_H, fontSize: 27, bold: true, color: COLORS.ink, align: "center" });
  text(slide, "班级主题谱", { x: 1.55, y: 4.35, w: 2.2, h: 0.42, fontSize: 21, bold: true, color: COLORS.gold, align: "center" });
  text(slide, "从那面黑板上，\n选一句真正说过的话。", { x: 1.3, y: 4.95, w: 2.7, h: 0.72, fontFace: FONT_H, fontSize: 20, color: COLORS.ink2, align: "center" });
  text(slide, "读完《氓》，你愿意替当时的自己补上哪一句？", { x: 4.95, y: 1.45, w: 7.55, h: 0.76, fontFace: FONT_H, fontSize: 32, bold: true, color: COLORS.plum, align: "center" });
  const rows = [
    ["我原来想到", "____________________________", COLORS.gold],
    ["《氓》让我", "补充／修正／保留：____________", COLORS.red],
    ["放进共同生活", "我会观察：____________________", COLORS.river],
  ];
  rows.forEach(([label, blank, color], index) => {
    const y = 2.75 + index * 1.05;
    text(slide, label, { x: 5.1, y, w: 1.85, h: 0.4, fontSize: 19, bold: true, color });
    text(slide, blank, { x: 7.0, y: y - 0.04, w: 5.1, h: 0.46, fontFace: FONT_H, fontSize: 23, color: COLORS.ink });
    line(slide, pptx, 7.0, y + 0.5, 5.0, COLORS.warm, 1.1);
  });
  text(slide, "让一处诗句，托住你的新理解。", { x: 5.25, y: 6.1, w: 6.95, h: 0.5, fontFace: FONT_H, fontSize: 29, bold: true, color: COLORS.ink, align: "center" });
  addNotes(slide, page);
}

function renderS05(slide, pptx, page) {
  base(slide, pptx, false, COLORS.ink);
  title(slide, "这些字，离开注释还认得吗？");
  text(slide, "《诗经》是什么？　｜　分哪三类？　｜　《氓》收在哪里？", { x: 1.05, y: 1.28, w: 11.23, h: 0.55, fontFace: FONT_H, fontSize: 28, bold: true, color: COLORS.plum, align: "center" });
  const glyphs = ["愆", "将", "筮", "说", "徂", "汤汤", "渐", "咥", "隰", "泮"];
  glyphs.forEach((glyph, index) => {
    const x = 1.0 + (index % 5) * 2.4;
    const y = 2.25 + Math.floor(index / 5) * 1.4;
    rect(slide, pptx, x, y, 1.95, 0.98, index < 5 ? COLORS.paper2 : COLORS.riverSoft, index < 5 ? COLORS.gold : COLORS.river, true, 1.0);
    text(slide, glyph, { x: x + 0.12, y: y + 0.23, w: 1.71, h: 0.48, fontFace: FONT_H, fontSize: glyph.length > 1 ? 28 : 34, bold: true, color: index < 5 ? COLORS.ink : COLORS.river, align: "center" });
  });
  text(slide, "先凭记忆读、写、解释；再回到原句相认。", { x: 1.4, y: 5.43, w: 10.53, h: 0.54, fontFace: FONT_H, fontSize: 30, bold: true, color: COLORS.ink, align: "center" });
  text(slide, "只修复自己的错项与空项。", { x: 3.1, y: 6.25, w: 7.13, h: 0.38, fontSize: 21, bold: true, color: COLORS.red, align: "center" });
  addNotes(slide, page);
}

function renderS06(slide, pptx, page) {
  base(slide, pptx, false, COLORS.leaf);
  title(slide, "这些诗句，为什么非得这样写？");
  text(slide, "任选一组", { x: 5.55, y: 1.05, w: 2.23, h: 0.34, fontFace: FONT_H, fontSize: 19, bold: true, color: COLORS.red, align: "center" });
  const blocks = [
    { text: "桑之未落，其叶沃若。\n桑之落矣，其黄而陨。", color: COLORS.leaf, fill: COLORS.leafSoft },
    { text: "于嗟鸠兮……\n于嗟女兮……", color: COLORS.gold, fill: COLORS.goldSoft },
    { text: "信誓旦旦，不思其反。\n反是不思，亦已焉哉！", color: COLORS.plum, fill: COLORS.plumSoft },
  ];
  blocks.forEach((block, index) => {
    const x = 0.8 + index * 4.18;
    rect(slide, pptx, x, 1.35, 3.82, 2.25, block.fill, block.color, true, 1.1);
    text(slide, block.text, { x: x + 0.23, y: 1.88, w: 3.36, h: 1.12, fontFace: FONT_H, fontSize: index === 1 ? 27 : 24, bold: true, color: block.color, align: "center", valign: "mid" });
  });
  text(slide, "原词怎样相照？", { x: 1.2, y: 4.25, w: 4.7, h: 0.52, fontFace: FONT_H, fontSize: 31, bold: true, color: COLORS.ink, align: "center" });
  text(slide, "声音、时间与人的处境，怎样改变？", { x: 5.6, y: 4.25, w: 6.5, h: 0.52, fontFace: FONT_H, fontSize: 31, bold: true, color: COLORS.plum, align: "center" });
  line(slide, pptx, 2.1, 5.25, 9.1, COLORS.warm, 1.2);
  text(slide, "原词关系　→　声音／时间变化　→　人物处境", { x: 2.0, y: 5.75, w: 9.33, h: 0.52, fontFace: FONT_H, fontSize: 29, bold: true, color: COLORS.river, align: "center" });
  addNotes(slide, page);
}

function renderS07(slide, pptx, page) {
  base(slide, pptx, false, COLORS.plum);
  title(slide, "把字词和写法，收回手中");
  rect(slide, pptx, 1.0, 1.25, 11.33, 5.4, COLORS.paper2, COLORS.warm, true, 1.1);
  text(slide, "我的语文知识书页", { x: 4.2, y: 1.62, w: 4.93, h: 0.55, fontFace: FONT_H, fontSize: 32, bold: true, color: COLORS.plum, align: "center" });
  const rows = [
    ["一个我已读准、说清的字词", "____________________________"],
    ["一处我能讲明的写法", "____________________________"],
    ["它怎样改变声音、时间或人物处境", "____________________________"],
  ];
  rows.forEach(([label, blank], index) => {
    const y = 2.55 + index * 0.9;
    text(slide, label, { x: 1.55, y, w: 4.15, h: 0.44, fontSize: index === 2 ? 18 : 20, bold: true, color: index === 0 ? COLORS.river : COLORS.ink2 });
    text(slide, blank, { x: 5.65, y: y - 0.04, w: 5.9, h: 0.44, fontFace: FONT_H, fontSize: 24, color: COLORS.ink });
  });
  line(slide, pptx, 1.55, 5.42, 10.2, COLORS.warm, 1.2);
  text(slide, "诗写了：______________________", { x: 1.65, y: 5.72, w: 4.8, h: 0.46, fontFace: FONT_H, fontSize: 25, bold: true, color: COLORS.leaf });
  text(slide, "诗没有写：__________________", { x: 6.7, y: 5.72, w: 4.8, h: 0.46, fontFace: FONT_H, fontSize: 25, bold: true, color: COLORS.red });
  addNotes(slide, page);
}

function renderS08(slide, pptx, page) {
  base(slide, pptx, true, COLORS.gold);
  title(slide, "把理解与问题一起带走", true);
  const lines = [
    "她从________走到________。",
    "她婚后的日子，让我看见________。",
    "这场婚姻走到这一步：________。",
  ];
  lines.forEach((value, index) => text(slide, value, { x: 1.15, y: 1.35 + index * 0.82, w: 11.03, h: 0.48, fontFace: FONT_H, fontSize: 28, color: COLORS.creamText }));
  line(slide, pptx, 1.15, 4.0, 11.0, COLORS.gold, 1.2);
  text(slide, "我从《氓》带走的一条共同生活提醒：________", { x: 1.15, y: 4.4, w: 11.03, h: 0.5, fontFace: FONT_H, fontSize: 27, bold: true, color: COLORS.goldSoft });
  text(slide, "托住它的诗句：____________________________", { x: 1.15, y: 5.14, w: 11.03, h: 0.46, fontFace: FONT_H, fontSize: 25, color: COLORS.creamText });
  text(slide, "我仍愿继续追问：________________（可留白）", { x: 1.15, y: 5.88, w: 11.03, h: 0.46, fontFace: FONT_H, fontSize: 25, color: COLORS.plumSoft });
  text(slide, "最后，从“氓之蚩蚩”完整读到“亦已焉哉”。", { x: 2.1, y: 6.65, w: 9.13, h: 0.34, fontSize: 20, bold: true, color: COLORS.creamText, align: "center" });
  addNotes(slide, page);
}

function check(pptx, expected) {
  const errors = [];
  if (pptx._slides.length !== expected) errors.push("slide_count");
  pptx._slides.forEach((slide, index) => {
    if (!slide._slideObjects.some((object) => object._type === "notes")) errors.push(`notes_${index + 1}`);
    for (const object of slide._slideObjects) {
      const o = object.options || {};
      if ([o.x, o.y, o.w, o.h].every((value) => typeof value === "number") && (o.x < -0.01 || o.y < -0.01 || o.x + o.w > W + 0.01 || o.y + o.h > H + 0.01)) errors.push(`bounds_${index + 1}`);
    }
  });
  if (errors.length) throw new Error(errors.join(","));
}

async function repairNotesMaster(filePath) {
  const zip = await JSZip.loadAsync(fs.readFileSync(filePath));
  const entry = zip.file("ppt/presentation.xml");
  let xml = await entry.async("string");
  const match = xml.match(/<p:notesMasterIdLst>[\s\S]*?<\/p:notesMasterIdLst>/);
  if (match) {
    xml = xml.replace(match[0], "");
    xml = xml.replace(/(<p:sldMasterIdLst>[\s\S]*?<\/p:sldMasterIdLst>)/, `$1${match[0]}`);
  }
  zip.file("ppt/presentation.xml", xml);
  fs.writeFileSync(filePath, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

async function main() {
  const report = validate(source);
  if (!report.ok) throw new Error(JSON.stringify(report.errors));
  const snapshot = JSON.parse(fs.readFileSync(SNAP, "utf8"));
  const sourceSha = sha(path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "synthesis.js"));
  if (snapshot.source_sha256 !== sourceSha) throw new Error("stale snapshot");

  const map = new Map(snapshot.pages.map((page) => [page.page_id, page]));
  const plan = [
    ["S01", renderS01, "真实六章母轨道"], ["S02", renderS02, "日常片刻与原句回配"],
    ["S03", renderS03, "四层原因追问"], ["S04", renderS04, "开课主题谱回看"],
    ["S05", renderS05, "字词合书检索"], ["S06", renderS06, "三组原句形式比较"],
    ["S07", renderS07, "个人语文知识书页"], ["S08", renderS08, "三问关系提醒与完整朗读"],
  ];
  const pptx = presentation();
  const physical = [];
  plan.forEach(([id, renderer, duty], index) => {
    const page = map.get(id);
    const slide = pptx.addSlide();
    renderer(slide, pptx, page);
    physical.push({ physical_index: index + 1, page_id: id, primary_visual_duty: duty, unique_function: page.unique_function });
  });
  check(pptx, plan.length);
  fs.mkdirSync(OUT, { recursive: true });
  await pptx.writeFile({ fileName: PPTX, compression: true });
  await repairNotesMaster(PPTX);
  fs.writeFileSync(MANIFEST, `${JSON.stringify({
    schema_version: "1.2", module_id: source.module_id, version: source.version,
    artifact: path.relative(PROJECT_ROOT, PPTX).split(path.sep).join("/"), sha256: sha(PPTX),
    source_snapshot_sha256: sha(SNAP), physical_slides: physical,
    illustration_policy: "no_character_illustration_until_page_function_double_review_passes",
    claim_boundary: "synthesis_candidate_not_classroom_observed",
  }, null, 2)}\n`);
  process.stdout.write(`V64_SYNTHESIS_PPTX_OK slides=${plan.length} pptx=${PPTX}\n`);
}

main().catch((error) => { process.stderr.write(`${error.stack || error}\n`); process.exit(1); });
