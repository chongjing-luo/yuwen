"use strict";

/**
 * 主题参数装载器（真值：scripts/lib/theme.json，设计方案 §8/E3 正式化）。
 * 本文件是 JSON 的纯投影，不持有任何字面量；同步由 tests/test_lib_theme_sync.js 保护。
 * 新课文从这里取参数，不复制进构建器（PPT 手册 §九 跨课文复用）。
 *
 * 派生约定（ rulings 不进 JSON）：
 * - 章节色映射是《氓》课文级派生；新课文按气质重映射 module_colors，结构照抄（PPT 手册 §三）。
 * - 字号下限（PPT 手册 §二 裁决线）：original_verse 按行数自适应（≤2 行 39 / ≤4 行 32 /
 *   更多 27）；title >20 字降 31；label 为非内容性文字下限。
 */
const fs = require("fs");
const path = require("path");

const data = JSON.parse(fs.readFileSync(path.join(__dirname, "theme.json"), "utf-8"));

const SERIF = data.serif;
const SANS = data.sans;
const C = data.colors;
const MODULE = data.module_colors;
const MODULE_LABELS = data.module_labels;
const FONT_FLOORS = data.font_floors;

module.exports = { SERIF, SANS, C, MODULE, MODULE_LABELS, FONT_FLOORS, ART_RANDOM_FONT_SIZE: FONT_FLOORS.phrase_card };
