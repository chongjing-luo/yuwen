const { execFileSync } = require("child_process");
const fs = require("fs");
const path = require("path");

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
const ASSET_DIR = path.join(
  ROOT,
  "work",
  "备课",
  "选择性必修下册",
  "氓",
  "assets",
  "illustrations_v2_vignettes",
);
const OUTPUT = path.join(ASSET_DIR, "00_插图入页效果样张.pptx");

const C = {
  ink: "28211B",
  paper: "F5EBDD",
  paper2: "FCF8F0",
  warm: "EBDCC7",
  river: "4D7481",
  cinnabar: "A44132",
  gold: "B68B4C",
  gray: "6E655C",
};

const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "OpenAI";
pptx.subject = "《氓》装饰性插图入页样张";
pptx.title = "《氓》插图入页效果样张";
pptx.company = "语文备课系统";
pptx.lang = "zh-CN";
pptx.theme = {
  headFontFace: "Noto Serif CJK SC",
  bodyFontFace: "Noto Sans CJK SC",
  lang: "zh-CN",
};

function addCommon(slide, chapter, page) {
  slide.background = { color: C.paper };
  slide.addText(chapter, {
    x: 0.75,
    y: 0.35,
    w: 2.4,
    h: 0.3,
    fontFace: "Noto Sans CJK SC",
    fontSize: 10.5,
    color: C.gold,
    bold: true,
    margin: 0,
    charSpacing: 0.5,
  });
  slide.addText(page, {
    x: 12.25,
    y: 7.05,
    w: 0.35,
    h: 0.18,
    fontFace: "Noto Sans CJK SC",
    fontSize: 7.5,
    color: C.gray,
    align: "right",
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.arc, {
    x: 12.36,
    y: 0.24,
    w: 0.38,
    h: 0.23,
    adjustPoint: 0.2,
    rotate: 18,
    fill: { color: C.gold, transparency: 8 },
    line: { color: C.gold, transparency: 100 },
  });
}

{
  const slide = pptx.addSlide();
  addCommon(slide, "第一章 · 初见与来意", "样张 01");
  slide.addText("氓之蚩蚩，抱布贸丝", {
    x: 0.85,
    y: 1.22,
    w: 7.5,
    h: 0.78,
    fontFace: "Noto Serif CJK SC",
    fontSize: 29,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  slide.addText("匪来贸丝，来即我谋", {
    x: 0.85,
    y: 2.15,
    w: 7.5,
    h: 0.72,
    fontFace: "Noto Serif CJK SC",
    fontSize: 27,
    color: C.ink,
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.85,
    y: 3.24,
    w: 7.35,
    h: 1.08,
    rectRadius: 0.05,
    fill: { color: C.paper2, transparency: 2 },
    line: { color: C.warm, width: 1 },
  });
  slide.addText("他抱来的，是布；真正要说的，却是婚事。", {
    x: 1.15,
    y: 3.55,
    w: 6.8,
    h: 0.38,
    fontFace: "Noto Sans CJK SC",
    fontSize: 17,
    color: C.cinnabar,
    margin: 0,
  });
  slide.addImage({
    path: path.join(ASSET_DIR, "01_动作小景_抱布来谋_透明_裁边.png"),
    x: 9.05,
    y: 1.14,
    w: 3.25,
    h: 3.25,
    altText: "男子抱布来到女子面前，两人相望",
  });
  slide.addNotes("样张一：检验动作小景缩小后能否帮助学生看见抱布、相望与来谋，而不遮挡诗句。");
}

{
  const slide = pptx.addSlide();
  addCommon(slide, "第六章 · 誓言与停止", "样张 02");
  slide.addText("信誓旦旦，不思其反", {
    x: 0.85,
    y: 1.26,
    w: 7.3,
    h: 0.7,
    fontFace: "Noto Serif CJK SC",
    fontSize: 27,
    color: C.ink,
    margin: 0,
  });
  slide.addText("反是不思，亦已焉哉", {
    x: 0.85,
    y: 2.2,
    w: 7.3,
    h: 0.76,
    fontFace: "Noto Serif CJK SC",
    fontSize: 30,
    bold: true,
    color: C.ink,
    margin: 0,
  });
  slide.addShape(pptx.ShapeType.roundRect, {
    x: 0.85,
    y: 3.34,
    w: 7.2,
    h: 1.08,
    rectRadius: 0.05,
    fill: { color: "D8E7EA", transparency: 20 },
    line: { color: "B9D0D5", width: 1 },
  });
  slide.addText("不是忘记伤痛，而是不再把余生交给反复的誓言。", {
    x: 1.15,
    y: 3.66,
    w: 6.6,
    h: 0.38,
    fontFace: "Noto Sans CJK SC",
    fontSize: 16.5,
    color: C.river,
    margin: 0,
  });
  slide.addImage({
    path: path.join(ASSET_DIR, "02_意象小景_亦已焉哉_透明_v2_裁边.png"),
    x: 9.42,
    y: 0.93,
    w: 2.48,
    h: 3.32,
    altText: "女子松开布带，身后只有一笔淇水",
  });
  slide.addNotes("样张二：检验意象小景能否以女子、松手与淇水一笔提示停止判断，而不把结论画满。");
}

async function repairPackage(fileName) {
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
  await pptx.writeFile({ fileName: OUTPUT, compression: true });
  await repairPackage(OUTPUT);
}

main().catch((error) => {
  console.error(error.stack || error);
  process.exit(1);
});
