#!/usr/bin/env node
"use strict";
const crypto = require("crypto"),
  fs = require("fs"),
  path = require("path");
function req(n) {
  try {
    return require(n);
  } catch (_) {
    return require(
      path.join(
        process.env.NODE_GLOBAL_ROOT ||
          "/usr/local/node-v22.22.2-linux-x64/lib/node_modules",
        n,
      ),
    );
  }
}
const pptxgen = req("pptxgenjs"),
  root =
    process.env.NODE_GLOBAL_ROOT ||
    "/usr/local/node-v22.22.2-linux-x64/lib/node_modules",
  JSZip = require(path.join(root, "pptxgenjs", "node_modules", "jszip")),
  source = require("./meng_v62/content/chapter_6"),
  { validate } = require("./verify_meng_v62_chapter6"),
  { PROJECT_ROOT, stageDir, assertV62OutputPath } = require("./meng_v62/paths");
const SNAP = path.join(
    stageDir(),
    "chapter_6",
    "package",
    "06_氓_V63第六章课程数据快照.json",
  ),
  OUT = assertV62OutputPath(path.join(stageDir(), "chapter_6", "pptx")),
  PPTX = assertV62OutputPath(path.join(OUT, "04_氓_V63第六章课堂课件.pptx")),
  MAN = assertV62OutputPath(path.join(OUT, "chapter6_pptx_manifest.json")),
  W = 13.333,
  H = 7.5,
  FH = "Noto Serif CJK SC",
  FB = "Noto Sans CJK SC",
  C = {
    ink: "29241F",
    ink2: "51483F",
    paper: "F6F0E5",
    paper2: "FFFCF7",
    warm: "E5DAC9",
    red: "9C4538",
    redSoft: "F0DDD5",
    river: "456F7C",
    riverSoft: "DDE9E9",
    leaf: "647752",
    leafSoft: "E1E7D9",
    gold: "AC8550",
    goldSoft: "EFE4D2",
    plum: "75515E",
    plumSoft: "EADDE1",
    muted: "766D63",
    night: "28241F",
    night2: "38312A",
  };
function sha(f) {
  return crypto.createHash("sha256").update(fs.readFileSync(f)).digest("hex");
}
function pres() {
  const p = new pptxgen();
  p.defineLayout({ name: "MENG_WIDE", width: W, height: H });
  p.layout = "MENG_WIDE";
  p.author = "语文备课系统";
  p.title = "《氓》V6.3第六章课堂课件";
  p.lang = "zh-CN";
  p.theme = { headFontFace: FH, bodyFontFace: FB, lang: "zh-CN" };
  return p;
}
function tx(s, t, o = {}) {
  s.addText(t, {
    x: 0.72,
    y: 0.52,
    w: 11.9,
    h: 0.5,
    margin: 0,
    fontFace: FB,
    fontSize: 28,
    color: C.ink,
    valign: "mid",
    ...o,
  });
}
function rect(s, p, x, y, w, h, f, l = f, r = false, width = 1) {
  s.addShape(r ? p.shapes.ROUNDED_RECTANGLE : p.shapes.RECTANGLE, {
    x,
    y,
    w,
    h,
    fill: { color: f },
    line: { color: l, width },
    ...(r ? { rectRadius: 0.05 } : {}),
  });
}
function line(s, p, x, y, w, c, width = 1) {
  s.addShape(p.shapes.LINE, { x, y, w, h: 0, line: { color: c, width } });
}
function base(s, p, d = false) {
  s.background = { color: d ? C.night : C.paper };
  rect(s, p, 0, 0, W, 0.12, d ? C.river : C.ink);
}
function title(s, t, o = {}) {
  tx(s, t, {
    x: 0.76,
    y: 0.38,
    w: 10.35,
    h: 0.62,
    fontFace: FH,
    fontSize: 33,
    bold: true,
    ...o,
  });
  tx(s, "第六章　6 / 6", {
    x: 10.78,
    y: 0.5,
    w: 1.82,
    h: 0.3,
    fontSize: 17.5,
    bold: true,
    color: o.color || C.red,
    align: "right",
  });
}
function notes(p) {
  const s = p.script;
  return [
    `【V6.3页ID】${p.page_id}｜${p.title}｜${p.minutes}分钟`,
    `【本页不可替代的意义】`,
    p.unique_function,
    `【删除本页会失去什么】`,
    p.deletion_loss,
    `【相邻合并测试】`,
    p.merge_test,
    `【教师逐字稿】`,
    s.teacher_spoken,
    `【场面与走位】`,
    s.scene,
    ...s.stage_directions.map((x) => `（${x}）`),
    `【时间盒】`,
    s.timeboxes.map((x) => `${x.label}：${x.seconds}秒`).join("；"),
    `【现场分支】`,
    s.branches.map((x) => `${x.kind}：${x.response}`).join("\n"),
    `【听者同步任务】`,
    s.listener_task,
    `【证据位置】`,
    s.evidence_location,
    `【回到人物和故事】`,
    p.story_return,
    `【后续真实调用】`,
    p.next_use,
    `【自然切页句】`,
    s.cut_line,
    `【声明边界】桌面排演稿；不声称真实学生已经理解、参与或学会。`,
  ].join("\n");
}
function addN(s, p) {
  s.addNotes(notes(p));
}
function C601(s, p, page) {
  base(s, p);
  title(s, "第六章｜她把哪些旧事重新放回眼前？");
  const ls = page.original_text
    .split("。")
    .filter(Boolean)
    .map((x) => `${x}。`);
  rect(s, p, 0.88, 1.18, 11.57, 4.65, C.paper2, C.warm, true, 1.05);
  ls.forEach((x, i) =>
    tx(s, x, {
      x: 1.15,
      y: 1.5 + i * 0.72,
      w: 11.03,
      h: 0.49,
      fontFace: FH,
      fontSize: 31.5,
      align: "center",
      color: C.ink,
      bold: false,
    }),
  );
  tx(s, "读完以后，只留下两处原文", {
    x: 4.37,
    y: 6.08,
    w: 4.6,
    h: 0.34,
    fontFace: FH,
    fontSize: 18.5,
    bold: true,
    color: C.muted,
    align: "center",
  });
  tx(s, "一处回到过去　｜　一处真正收束全诗", {
    x: 1.5,
    y: 6.48,
    w: 10.33,
    h: 0.43,
    fontFace: FH,
    fontSize: 25,
    bold: true,
    color: C.plum,
    align: "center",
  });
  addN(s, page);
}
function C602(s, p, page) {
  base(s, p, true);
  title(s, "及尔偕老｜老使我怨", { color: C.paper });
  rect(s, p, 0.92, 1.42, 5.72, 2.16, "333A3D", C.river, true, 1.05);
  rect(s, p, 6.72, 1.42, 5.72, 2.16, "3D3134", C.plum, true, 1.05);
  tx(s, "及尔偕老", {
    x: 1.18,
    y: 2.07,
    w: 5.2,
    h: 0.56,
    fontFace: FH,
    fontSize: 40,
    bold: true,
    color: C.riverSoft,
    align: "center",
  });
  tx(s, "老使我怨", {
    x: 6.98,
    y: 2.07,
    w: 5.2,
    h: 0.56,
    fontFace: FH,
    fontSize: 40,
    bold: true,
    color: C.plumSoft,
    align: "center",
  });
  tx(s, "及：同、跟　｜　偕老：共同到老", {
    x: 3.0,
    y: 4.23,
    w: 7.33,
    h: 0.38,
    fontSize: 23,
    bold: true,
    color: C.warm,
    align: "center",
  });
  tx(s, "同一个‘老’，前后两次落在怎样不同的生活里？", {
    x: 1.25,
    y: 5.25,
    w: 10.83,
    h: 0.56,
    fontFace: FH,
    fontSize: 30,
    bold: true,
    color: C.paper,
    align: "center",
  });
  tx(s, "让两个声音在这个字上交接", {
    x: 3.43,
    y: 6.23,
    w: 6.47,
    h: 0.34,
    fontSize: 19.5,
    bold: true,
    color: C.warm,
    align: "center",
  });
  addN(s, page);
}
function C603(s, p, page) {
  base(s, p);
  title(s, "淇则有岸，隰则有泮");
  rect(s, p, 1.0, 1.35, 11.33, 1.4, C.riverSoft, C.river, true, 1.05);
  tx(s, "淇则有岸，隰则有泮。", {
    x: 1.28,
    y: 1.77,
    w: 10.77,
    h: 0.55,
    fontFace: FH,
    fontSize: 41,
    bold: true,
    color: C.river,
    align: "center",
  });
  tx(s, "隰 xí：低湿的地方　｜　泮 pàn：同‘畔’，边、岸", {
    x: 2.0,
    y: 3.18,
    w: 9.33,
    h: 0.42,
    fontSize: 23,
    bold: true,
    color: C.ink2,
    align: "center",
  });
  tx(s, "为什么在‘偕老／怨’之后，忽然写淇与隰的岸和泮？", {
    x: 1.25,
    y: 4.32,
    w: 10.83,
    h: 0.55,
    fontFace: FH,
    fontSize: 29,
    bold: true,
    color: C.plum,
    align: "center",
  });
  tx(s, "它怎样接前句，也怎样照见后文？", {
    x: 2.0,
    y: 5.34,
    w: 9.33,
    h: 0.52,
    fontFace: FH,
    fontSize: 28,
    bold: true,
    color: C.ink,
    align: "center",
  });
  addN(s, page);
}
function C604(s, p, page) {
  base(s, p, true);
  title(s, "总角之宴｜信誓旦旦", { color: C.paper });
  rect(s, p, 0.85, 1.35, 5.75, 3.65, "333A31", C.leaf, true, 1.05);
  rect(s, p, 6.73, 1.35, 5.75, 3.65, "3D3330", C.gold, true, 1.05);
  tx(s, "她记住的旧日", {
    x: 1.15,
    y: 1.7,
    w: 5.15,
    h: 0.34,
    fontSize: 22,
    bold: true,
    color: C.leafSoft,
    align: "center",
  });
  tx(s, "总角之宴，言笑晏晏。", {
    x: 1.02,
    y: 2.55,
    w: 5.41,
    h: 0.55,
    fontFace: FH,
    fontSize: 31,
    bold: true,
    color: C.paper,
    align: "center",
  });
  tx(s, "如今再看", {
    x: 7.03,
    y: 1.7,
    w: 5.15,
    h: 0.34,
    fontSize: 22,
    bold: true,
    color: C.goldSoft,
    align: "center",
  });
  tx(s, "信誓旦旦，不思其反。", {
    x: 6.9,
    y: 2.55,
    w: 5.41,
    h: 0.55,
    fontFace: FH,
    fontSize: 31,
    bold: true,
    color: C.paper,
    align: "center",
  });
  tx(s, "总角：少年　宴：欢乐　晏晏：和悦　｜　旦旦：诚恳　反：违背", {
    x: 1.1,
    y: 5.5,
    w: 11.13,
    h: 0.4,
    fontSize: 21.5,
    bold: true,
    color: C.warm,
    align: "center",
  });
  tx(s, "记忆是真的；后来什么也是真的？", {
    x: 2.1,
    y: 6.23,
    w: 9.13,
    h: 0.46,
    fontFace: FH,
    fontSize: 28,
    bold: true,
    color: C.plumSoft,
    align: "center",
  });
  addN(s, page);
}
function C605(s, p, page) {
  base(s, p, true);
  title(s, "反是不思，亦已焉哉", { color: C.paper });
  rect(s, p, 0.82, 1.38, 5.83, 2.35, "343A3C", C.river, true, 1.05);
  rect(s, p, 6.75, 1.38, 5.75, 2.35, "3D3134", C.plum, true, 1.05);
  tx(s, "信誓旦旦，不思其反。", {
    x: 1.02,
    y: 2.16,
    w: 5.43,
    h: 0.52,
    fontFace: FH,
    fontSize: 29,
    bold: true,
    color: C.riverSoft,
    align: "center",
  });
  tx(s, "反是不思，亦已焉哉！", {
    x: 6.95,
    y: 2.16,
    w: 5.35,
    h: 0.52,
    fontFace: FH,
    fontSize: 29,
    bold: true,
    color: C.plumSoft,
    align: "center",
  });
  tx(s, "是：这，指誓言　｜　已：止、了结　｜　焉、哉：连用加强收束", {
    x: 1.15,
    y: 4.27,
    w: 11.03,
    h: 0.4,
    fontSize: 22,
    bold: true,
    color: C.warm,
    align: "center",
  });
  tx(s, "哪些词一再回来？", {
    x: 1.15,
    y: 5.17,
    w: 5.18,
    h: 0.45,
    fontFace: FH,
    fontSize: 27,
    bold: true,
    color: C.riverSoft,
    align: "center",
  });
  tx(s, "再把末句读成两种声音", {
    x: 6.93,
    y: 5.17,
    w: 5.18,
    h: 0.45,
    fontFace: FH,
    fontSize: 27,
    bold: true,
    color: C.plumSoft,
    align: "center",
  });
  tx(s, "你分别听见什么？", {
    x: 3.4,
    y: 6.17,
    w: 6.53,
    h: 0.48,
    fontFace: FH,
    fontSize: 29,
    bold: true,
    color: C.paper,
    align: "center",
  });
  addN(s, page);
}
function C606(s, p, page) {
  base(s, p, true);
  title(s, "把第六章讲成她最后一次回望", { color: C.paper });
  const ls = page.original_text
    .split("。")
    .filter(Boolean)
    .map((x) => `${x}。`);
  rect(s, p, 0.78, 1.2, 7.72, 5.14, C.night2, C.river, true, 1.05);
  ls.forEach((x, i) =>
    tx(s, x, {
      x: 1.04,
      y: 1.61 + i * 0.82,
      w: 7.2,
      h: 0.46,
      fontFace: FH,
      fontSize: 29,
      color: C.paper,
      align: "center",
    }),
  );
  tx(s, "旧愿怎样反折？", {
    x: 8.82,
    y: 1.67,
    w: 3.78,
    h: 0.48,
    fontFace: FH,
    fontSize: 25,
    bold: true,
    color: C.riverSoft,
    align: "center",
  });
  tx(s, "她重新看见什么？", {
    x: 8.82,
    y: 2.95,
    w: 3.78,
    h: 0.48,
    fontFace: FH,
    fontSize: 25,
    bold: true,
    color: C.paper,
    align: "center",
  });
  tx(s, "最后作出\n怎样的判断？", {
    x: 8.82,
    y: 4.18,
    w: 3.78,
    h: 0.92,
    fontFace: FH,
    fontSize: 25,
    bold: true,
    color: C.plumSoft,
    align: "center",
  });
  tx(s, "合书以后，只讲这三层", {
    x: 8.82,
    y: 5.65,
    w: 3.78,
    h: 0.38,
    fontSize: 20,
    bold: true,
    color: C.warm,
    align: "center",
  });
  tx(s, "故事轨道｜第六格", {
    x: 0.82,
    y: 6.62,
    w: 2.12,
    h: 0.3,
    fontSize: 18,
    bold: true,
    color: C.riverSoft,
  });
  line(s, p, 3.2, 6.86, 8.73, C.river, 2);
  tx(s, "第一章　→　第二章　→　第三章　→　第四章　→　第五章　→　第六章", {
    x: 3.15,
    y: 6.55,
    w: 9.15,
    h: 0.32,
    fontSize: 17.5,
    bold: true,
    color: C.paper,
    align: "center",
  });
  addN(s, page);
}
function check(p, n) {
  const e = [];
  if (p._slides.length !== n) e.push("slides");
  p._slides.forEach((s, i) => {
    if (!s._slideObjects.some((x) => x._type === "notes")) e.push(`notes${i}`);
    s._slideObjects.forEach((x) => {
      const o = x.options || {};
      if (
        [o.x, o.y, o.w, o.h].every((v) => typeof v === "number") &&
        (o.x < -0.01 ||
          o.y < -0.01 ||
          o.x + o.w > W + 0.01 ||
          o.y + o.h > H + 0.01)
      )
        e.push(`bounds${i}`);
    });
  });
  if (e.length) throw new Error(e.join(","));
}
async function repair(f) {
  const z = await JSZip.loadAsync(fs.readFileSync(f)),
    e = z.file("ppt/presentation.xml");
  let x = await e.async("string"),
    m = x.match(/<p:notesMasterIdLst>[\s\S]*?<\/p:notesMasterIdLst>/);
  if (m) {
    x = x.replace(m[0], "");
    x = x.replace(
      /(<p:sldMasterIdLst>[\s\S]*?<\/p:sldMasterIdLst>)/,
      `$1${m[0]}`,
    );
  }
  z.file("ppt/presentation.xml", x);
  fs.writeFileSync(
    f,
    await z.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }),
  );
}
async function main() {
  const v = validate(source);
  if (!v.ok) throw new Error(JSON.stringify(v.errors));
  const snap = JSON.parse(fs.readFileSync(SNAP));
  if (
    snap.source_sha256 !==
    sha(
      path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", "chapter_6.js"),
    )
  )
    throw new Error("stale snapshot");
  const map = new Map(snap.pages.map((x) => [x.page_id, x])),
    plan = [
      ["C601", C601, "完整章声与时间回环"],
      ["C602", C602, "老字铰链"],
      ["C603", C603, "自然边界多解"],
      ["C604", C604, "旧日今日双真相"],
      ["C605", C605, "末句双声与边界"],
      ["C606", C606, "撤答全诗接续"],
    ],
    pages = plan.map(([id, r, d], i) => ({
      ...map.get(id),
      renderer: r,
      duty: d,
      physicalIndex: i + 1,
    })),
    p = pres();
  pages.forEach((x) => x.renderer(p.addSlide(), p, x));
  check(p, pages.length);
  fs.mkdirSync(OUT, { recursive: true });
  await p.writeFile({ fileName: PPTX, compression: true });
  await repair(PPTX);
  fs.writeFileSync(
    MAN,
    `${JSON.stringify({ schema_version: "1.1", module_id: source.module_id, version: source.version, artifact: path.relative(PROJECT_ROOT, PPTX).split(path.sep).join("/"), sha256: sha(PPTX), source_snapshot_sha256: sha(SNAP), physical_slides: pages.map((x) => ({ physical_index: x.physicalIndex, page_id: x.page_id, primary_visual_duty: x.duty, unique_function: x.unique_function })), illustration_policy: "no_character_illustration_until_all_lesson_functions_are_frozen", claim_boundary: "chapter6_candidate_not_classroom_observed" }, null, 2)}\n`,
  );
  process.stdout.write(
    `V63_CHAPTER6_PPTX_OK slides=${pages.length} pptx=${PPTX}\n`,
  );
}
main().catch((e) => {
  process.stderr.write(`${e.stack || e}\n`);
  process.exit(1);
});
