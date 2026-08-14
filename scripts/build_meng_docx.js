#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

function requireGlobal(name) {
  try {
    return require(name);
  } catch (_) {
    const root = execFileSync("npm", ["root", "-g"], { encoding: "utf8" }).trim();
    return require(path.join(root, name));
  }
}

const {
  AlignmentType,
  BorderStyle,
  Document,
  Footer,
  Header,
  HeadingLevel,
  LevelFormat,
  PageBreak,
  PageNumber,
  PageOrientation,
  Packer,
  Paragraph,
  ShadingType,
  Table,
  TableCell,
  TableRow,
  TextRun,
  VerticalAlign,
  WidthType,
} = requireGlobal("docx");

const ROOT = path.resolve(__dirname, "..");
const LESSON_DIR = path.join(ROOT, "work", "备课", "选择性必修下册", "氓");
const { slides, totalMinutes } = require("./meng_v5_lesson");

const COLORS = {
  ink: "2B2118",
  paper: "F4EBDD",
  paper2: "FBF7EF",
  leaf: "6C7B51",
  cinnabar: "A23A2E",
  gold: "B89A61",
  gray: "6B6259",
  border: "CFC2AF",
  white: "FFFFFF",
};

const FONT_SERIF = "Noto Serif CJK SC";
const FONT_SANS = "Noto Sans CJK SC";

function stripFrontMatter(markdown) {
  const lines = markdown.replace(/\r\n/g, "\n").split("\n");
  if (lines[0] !== "---") return lines;
  const end = lines.indexOf("---", 1);
  return end >= 0 ? lines.slice(end + 1) : lines;
}

function plainText(text) {
  return text
    .replace(/<br\s*\/?>/gi, "　")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1")
    .trim();
}

function inlineRuns(text, opts = {}) {
  const normalized = text
    .replace(/<br\s*\/?>/gi, "　")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1");
  const pattern = /(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)/g;
  const parts = normalized.split(pattern).filter(Boolean);
  return parts.map((part) => {
    if (part.startsWith("**") && part.endsWith("**")) {
      return new TextRun({ text: part.slice(2, -2), bold: true, ...opts });
    }
    if (part.startsWith("`") && part.endsWith("`")) {
      return new TextRun({ text: part.slice(1, -1), font: "Noto Sans Mono CJK SC", color: COLORS.cinnabar, ...opts });
    }
    if (part.startsWith("*") && part.endsWith("*")) {
      return new TextRun({ text: part.slice(1, -1), italics: true, ...opts });
    }
    return new TextRun({ text: part, ...opts });
  });
}

function isTableLine(line) {
  return /^\s*\|.*\|\s*$/.test(line);
}

function isTableDivider(line) {
  return /^\s*\|(?:\s*:?-{3,}:?\s*\|)+\s*$/.test(line);
}

function splitTableLine(line) {
  return line.trim().slice(1, -1).split("|").map((cell) => cell.trim());
}

function columnWidths(rows, totalWidth) {
  const columns = Math.max(...rows.map((row) => row.length));
  const weights = Array(columns).fill(1);
  for (let c = 0; c < columns; c += 1) {
    const maxLength = Math.max(...rows.map((row) => plainText(row[c] || "").length), 4);
    weights[c] = Math.max(2.2, Math.min(8.5, Math.sqrt(maxLength) * 1.5));
  }
  const sum = weights.reduce((a, b) => a + b, 0);
  const widths = weights.map((weight) => Math.floor((weight / sum) * totalWidth));
  widths[widths.length - 1] += totalWidth - widths.reduce((a, b) => a + b, 0);
  return widths;
}

function makeTable(rows, totalWidth, compact = false) {
  const widths = columnWidths(rows, totalWidth);
  const columns = widths.length;
  const fontSize = compact || columns >= 7 ? 15 : columns >= 5 ? 16 : 18;
  const border = { style: BorderStyle.SINGLE, size: 3, color: COLORS.border };
  const borders = { top: border, bottom: border, left: border, right: border, insideHorizontal: border, insideVertical: border };
  const tableRows = rows.map((row, rowIndex) => new TableRow({
    tableHeader: rowIndex === 0,
    cantSplit: true,
    children: widths.map((width, columnIndex) => new TableCell({
      width: { size: width, type: WidthType.DXA },
      borders,
      verticalAlign: VerticalAlign.CENTER,
      shading: {
        fill: rowIndex === 0 ? COLORS.ink : rowIndex % 2 === 0 ? COLORS.paper2 : COLORS.white,
        type: ShadingType.CLEAR,
      },
      margins: { top: 75, bottom: 75, left: 95, right: 95 },
      children: [new Paragraph({
        alignment: rowIndex === 0 ? AlignmentType.CENTER : AlignmentType.LEFT,
        spacing: { after: 0, line: 260 },
        children: inlineRuns(row[columnIndex] || "", {
          font: FONT_SANS,
          size: fontSize,
          color: rowIndex === 0 ? COLORS.white : COLORS.ink,
          bold: rowIndex === 0,
        }),
      })],
    })),
  }));
  return new Table({
    width: { size: totalWidth, type: WidthType.DXA },
    columnWidths: widths,
    rows: tableRows,
  });
}

function makeParagraph(text, options = {}) {
  return new Paragraph({
    spacing: { before: 0, after: 100, line: 330 },
    ...options,
    children: inlineRuns(text, { font: FONT_SANS, size: 19, color: COLORS.ink }),
  });
}

function makeQuote(text) {
  return new Paragraph({
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: COLORS.cinnabar, space: 8 } },
    shading: { fill: COLORS.paper2, type: ShadingType.CLEAR },
    indent: { left: 300, right: 180 },
    spacing: { before: 80, after: 130, line: 340 },
    children: inlineRuns(text.replace(/^>\s?/, ""), { font: FONT_SERIF, size: 21, color: COLORS.ink, italics: true }),
  });
}

function makeCode(lines) {
  return lines.map((line, index) => new Paragraph({
    shading: { fill: "F0ECE4", type: ShadingType.CLEAR },
    border: index === 0 ? { top: { style: BorderStyle.SINGLE, size: 3, color: COLORS.border } } : undefined,
    indent: { left: 240, right: 240 },
    spacing: { before: 0, after: index === lines.length - 1 ? 120 : 0, line: 270 },
    children: [new TextRun({ text: line || " ", font: "Noto Sans Mono CJK SC", size: 16, color: COLORS.ink })],
  }));
}

function markdownToDocxChildren(markdown, options) {
  const lines = stripFrontMatter(markdown);
  const children = [];
  let index = 0;
  let skippedFirstH1 = false;
  let orderedListCounter = 0;
  let orderedListReference = null;

  while (index < lines.length) {
    const line = lines[index];
    const trimmed = line.trim();
    if (!trimmed) {
      index += 1;
      continue;
    }
    if (/^(CORE_SESSION_|STUDENT_LANGUAGE_)/.test(trimmed)) {
      index += 1;
      continue;
    }
    if (trimmed === "---") {
      children.push(new Paragraph({ children: [new PageBreak()] }));
      index += 1;
      continue;
    }
    if (trimmed.startsWith("```")) {
      const code = [];
      index += 1;
      while (index < lines.length && !lines[index].trim().startsWith("```")) {
        code.push(lines[index]);
        index += 1;
      }
      index += 1;
      children.push(...makeCode(code));
      continue;
    }
    if (isTableLine(line) && index + 1 < lines.length && isTableDivider(lines[index + 1])) {
      const rows = [splitTableLine(line)];
      index += 2;
      while (index < lines.length && isTableLine(lines[index])) {
        rows.push(splitTableLine(lines[index]));
        index += 1;
      }
      children.push(makeTable(rows, options.contentWidth, options.compactTables));
      children.push(new Paragraph({ spacing: { after: 80 } }));
      continue;
    }
    const heading = trimmed.match(/^(#{1,4})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const text = plainText(heading[2]);
      if (level === 1 && options.skipFirstH1 && !skippedFirstH1) {
        skippedFirstH1 = true;
        index += 1;
        continue;
      }
      const headingLevel = level === 1 ? HeadingLevel.HEADING_1 : level === 2 ? HeadingLevel.HEADING_2 : HeadingLevel.HEADING_3;
      children.push(new Paragraph({
        heading: headingLevel,
        pageBreakBefore: options.headingOnePageBreak && level === 1,
        children: [new TextRun({ text, font: FONT_SERIF, color: level <= 2 ? COLORS.ink : COLORS.cinnabar, bold: true })],
      }));
      index += 1;
      continue;
    }
    if (trimmed.startsWith(">")) {
      const quoteLines = [];
      while (index < lines.length && lines[index].trim().startsWith(">")) {
        const content = lines[index].trim().replace(/^>\s?/, "");
        if (content) quoteLines.push(content);
        index += 1;
      }
      children.push(makeQuote(quoteLines.join(" ")));
      continue;
    }
    const unordered = trimmed.match(/^[-*]\s+(.+)$/);
    if (unordered) {
      children.push(new Paragraph({
        numbering: { reference: "bullets", level: 0 },
        spacing: { after: 60, line: 310 },
        children: inlineRuns(unordered[1], { font: FONT_SANS, size: 19, color: COLORS.ink }),
      }));
      index += 1;
      continue;
    }
    const ordered = trimmed.match(/^(\d+)\.\s+(.+)$/);
    if (ordered) {
      if (ordered[1] === "1" || orderedListReference === null) {
        orderedListCounter += 1;
        orderedListReference = `${options.numberingPrefix}-${orderedListCounter}`;
      }
      children.push(new Paragraph({
        numbering: { reference: orderedListReference, level: 0 },
        spacing: { after: 60, line: 310 },
        children: inlineRuns(ordered[2], { font: FONT_SANS, size: 19, color: COLORS.ink }),
      }));
      index += 1;
      continue;
    }
    if (/^_+$/.test(trimmed)) {
      children.push(new Paragraph({
        border: { bottom: { style: BorderStyle.SINGLE, size: 3, color: "8E877D", space: 1 } },
        spacing: { before: 60, after: 160 },
        children: [new TextRun({ text: " ", size: 19 })],
      }));
      index += 1;
      continue;
    }

    const paragraphLines = [trimmed];
    index += 1;
    while (index < lines.length) {
      const next = lines[index].trim();
      if (!next || next === "---" || next.startsWith("#") || next.startsWith(">") || next.startsWith("```") || /^[-*]\s+/.test(next) || /^\d+\.\s+/.test(next) || isTableLine(lines[index]) || /^_+$/.test(next)) break;
      paragraphLines.push(next);
      index += 1;
    }
    children.push(makeParagraph(paragraphLines.join(" ")));
  }
  return children;
}

function coverPage({ descriptor, focus, version }) {
  return [
    new Paragraph({ spacing: { before: 780, after: 140 }, alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "氓", font: FONT_SERIF, size: 72, bold: true, color: COLORS.ink }),
    ] }),
    new Paragraph({ spacing: { after: 260 }, alignment: AlignmentType.CENTER, children: [
      new TextRun({ text: "《诗经·卫风》", font: FONT_SERIF, size: 28, color: COLORS.cinnabar }),
    ] }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      border: { bottom: { style: BorderStyle.SINGLE, size: 14, color: COLORS.gold, space: 12 } },
      spacing: { after: 260 },
      children: [new TextRun({ text: descriptor, font: FONT_SANS, size: 24, bold: true, color: COLORS.leaf })],
    }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 180 }, children: [
      new TextRun({ text: focus, font: FONT_SERIF, size: 30, bold: true, color: COLORS.ink }),
    ] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 260, after: 80 }, children: [
      new TextRun({ text: "选择性必修下册 · 第一单元 · 文学阅读与写作", font: FONT_SANS, size: 20, color: COLORS.gray }),
    ] }),
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 60 }, children: [
      new TextRun({ text: version, font: FONT_SANS, size: 18, color: COLORS.gray }),
    ] }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

function header(text) {
  return new Header({ children: [new Paragraph({
    border: { bottom: { style: BorderStyle.SINGLE, size: 5, color: COLORS.gold, space: 5 } },
    children: [new TextRun({ text, font: FONT_SANS, size: 15, color: COLORS.gray })],
  })] });
}

function footer(text) {
  return new Footer({ children: [new Paragraph({
    alignment: AlignmentType.RIGHT,
    children: [
      new TextRun({ text: `${text}　`, font: FONT_SANS, size: 14, color: COLORS.gray }),
      new TextRun({ text: "第 ", font: FONT_SANS, size: 14, color: COLORS.gray }),
      new TextRun({ children: [PageNumber.CURRENT], font: FONT_SANS, size: 14, color: COLORS.gray }),
      new TextRun({ text: " 页", font: FONT_SANS, size: 14, color: COLORS.gray }),
    ],
  })] });
}

function documentStyles() {
  return {
    default: { document: { run: { font: FONT_SANS, size: 19, color: COLORS.ink }, paragraph: { spacing: { line: 330 } } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: FONT_SERIF, color: COLORS.ink },
        paragraph: { spacing: { before: 260, after: 160 }, outlineLevel: 0, keepNext: true } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 27, bold: true, font: FONT_SERIF, color: COLORS.ink },
        paragraph: { spacing: { before: 220, after: 120 }, outlineLevel: 1, keepNext: true } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, font: FONT_SANS, color: COLORS.cinnabar },
        paragraph: { spacing: { before: 180, after: 90 }, outlineLevel: 2, keepNext: true } },
    ],
  };
}

function numberingConfig() {
  const numberReferences = ["lesson-numbers", "worksheet-numbers", "script-numbers"].flatMap((prefix) =>
    Array.from({ length: 32 }, (_, index) => ({
      reference: `${prefix}-${index + 1}`,
      levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 520, hanging: 260 } } } }],
    })),
  );
  return {
    config: [
      { reference: "bullets", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
        style: { paragraph: { indent: { left: 480, hanging: 240 } } } }] },
      ...numberReferences,
    ],
  };
}

async function buildLessonDocx() {
  const input = path.join(LESSON_DIR, "02_氓_V5全文逐句教学母版.md");
  const output = path.join(LESSON_DIR, "02_氓_V5全文逐句教学母版.docx");
  const markdown = fs.readFileSync(input, "utf8");
  const pageWidth = 16838;
  const marginLeft = 780;
  const marginRight = 780;
  const contentWidth = pageWidth - marginLeft - marginRight;
  const children = [
    ...coverPage({
      descriptor: `六章逐句教学 · 五个同源模块 · 自然时长${totalMinutes}分钟`,
      focus: "沿原文走完整个故事，让学生讲述、还原生活并形成判断",
      version: "全文逐句教学母版 V5.3 · 2026年8月11日",
    }),
    ...markdownToDocxChildren(markdown, {
      contentWidth,
      compactTables: true,
      skipFirstH1: true,
      headingOnePageBreak: false,
      numberingPrefix: "lesson-numbers",
    }),
  ];
  const doc = new Document({
    creator: "语文备课系统",
    title: "《氓》V5全文逐句教学母版",
    description: "选择性必修下册第一单元；六章逐句讲授、体验活动与三问综合",
    styles: documentStyles(),
    numbering: numberingConfig(),
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838, orientation: PageOrientation.LANDSCAPE },
          margin: { top: 760, right: marginRight, bottom: 760, left: marginLeft, header: 360, footer: 360 },
        },
      },
      headers: { default: header(`《氓》V5全文逐句教学母版｜五模块·${totalMinutes}分钟`) },
      footers: { default: footer("原文主线·真实参与·语文表达") },
      children,
    }],
  });
  fs.writeFileSync(output, await Packer.toBuffer(doc));
  return output;
}

async function buildWorksheetDocx() {
  const input = path.join(LESSON_DIR, "03_氓_V5学生学习单.md");
  const output = path.join(LESSON_DIR, "03_氓_V5学生学习单.docx");
  const markdown = fs.readFileSync(input, "utf8");
  const pageWidth = 11906;
  const marginLeft = 850;
  const marginRight = 850;
  const contentWidth = pageWidth - marginLeft - marginRight;
  const children = markdownToDocxChildren(markdown, {
    contentWidth,
    compactTables: false,
    skipFirstH1: false,
    headingOnePageBreak: false,
    numberingPrefix: "worksheet-numbers",
  });
  const doc = new Document({
    creator: "语文备课系统",
    title: "《氓》V5学生学习单",
    description: "保存逐句口译、六章行动、接力讲述、生活镜头、婚姻讨论与理解修订",
    styles: documentStyles(),
    numbering: numberingConfig(),
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 760, right: marginRight, bottom: 760, left: marginLeft, header: 340, footer: 340 },
        },
      },
      headers: { default: header("《氓》V5学生学习单｜原句·口译·行动·证据·修订") },
      footers: { default: footer("选择性必修下册·第一单元") },
      children,
    }],
  });
  fs.writeFileSync(output, await Packer.toBuffer(doc));
  return output;
}

async function buildScriptDocx() {
  const input = path.join(LESSON_DIR, "04A_氓_V5逐页无生试讲稿.md");
  const output = path.join(LESSON_DIR, "04A_氓_V5逐页无生试讲稿.docx");
  const markdown = fs.readFileSync(input, "utf8");
  const pageWidth = 11906;
  const marginLeft = 850;
  const marginRight = 850;
  const contentWidth = pageWidth - marginLeft - marginRight;
  const children = [
    ...coverPage({
      descriptor: `${slides.length}页母版连续课堂剧本 · 与五个模块备注同源`,
      focus: "逐页可直接演出的教师原话、等待、回应与切页",
      version: "全文逐句教学母版 V5.3 · 2026年8月11日",
    }),
    ...markdownToDocxChildren(markdown, {
      contentWidth,
      compactTables: false,
      skipFirstH1: true,
      headingOnePageBreak: false,
      numberingPrefix: "script-numbers",
    }),
  ];
  const doc = new Document({
    creator: "语文备课系统",
    title: "《氓》V5逐页无生试讲稿",
    description: "与V5完整母版及五模块PPT讲者备注同源的逐页连续课堂剧本",
    styles: documentStyles(),
    numbering: numberingConfig(),
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 760, right: marginRight, bottom: 760, left: marginLeft, header: 340, footer: 340 },
        },
      },
      headers: { default: header(`《氓》V5逐页无生试讲稿｜${slides.length}页母版连续课堂剧本`) },
      footers: { default: footer("与PPT讲者备注同源") },
      children,
    }],
  });
  fs.writeFileSync(output, await Packer.toBuffer(doc));
  return output;
}

async function main() {
  const lesson = await buildLessonDocx();
  const worksheet = await buildWorksheetDocx();
  const script = await buildScriptDocx();
  for (const output of [lesson, worksheet, script]) {
    console.log(`${path.relative(ROOT, output)}\t${fs.statSync(output).size} bytes`);
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
