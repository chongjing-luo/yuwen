"use strict";

/**
 * 主题参数表（theme.json 的种子，设计方案 §8/E3）。
 * 与 scripts/build_meng_v66_pptx.js 的 C / SERIF / SANS / MODULE 同源；
 * 同步由 tests/test_lib_theme_sync.js 保护（从构建器源码提取比对，防两处漂移）。
 * 新课文从这里取参数，不复制进构建器（PPT 手册 §九 跨课文复用）。
 */
const SERIF = "Noto Serif CJK SC";
const SANS = "Noto Sans CJK SC";

const C = {
  ink: "29241F", ink2: "51483F", muted: "7B7167", paper: "F5EFE4", paper2: "FFFCF7", white: "FFFDFC",
  warm: "DED0BC", warm2: "C5B39B", gold: "A67F4A", gold2: "EFE3CF", yellow: "B58B3E", yellow2: "F0E4C8",
  river: "446E78", river2: "DCE9E8", leaf: "657653", leaf2: "E1E7D9", plum: "725260", plum2: "E9DDE2",
  red: "94473B", red2: "EFDDD5", night: "28231F", night2: "383129",
};

// 章节色映射（《氓》课文级派生；新课文按气质重映射，结构照抄——PPT 手册 §三）
const MODULE = {
  opening: "gold", chapter_1: "gold", chapter_2: "river", chapter_3: "leaf",
  chapter_4: "yellow", chapter_5: "plum", chapter_6: "red", synthesis: "ink2",
};

// 字号下限表（PPT 手册 §二 裁决线）
const FONT_FLOORS = {
  original_verse: 28,   // 原文诗句（≤2 行 39 / ≤4 行 32 / 更多 27 自适应）
  phrase_card: 26,      // 短语卡/随机散卡
  artifact_slot: 22,    // 产物槽标题/文化释义
  title: 36,            // 页标题（>20 字降 31）
  label: 15,            // 标签/页码/模块名（非内容性）
};

module.exports = { SERIF, SANS, C, MODULE, FONT_FLOORS, ART_RANDOM_FONT_SIZE: FONT_FLOORS.phrase_card };
