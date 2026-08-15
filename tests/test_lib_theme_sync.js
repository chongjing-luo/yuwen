"use strict";

/**
 * 主题单一来源防护（E3 后）：构建器必须消费 scripts/lib/theme，
 * 且不再持有色板/字号字面量（字面量回归 = 两处维护 = 漂移）。
 */
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const theme = require("../scripts/lib/theme");

const BUILDER = path.join(__dirname, "..", "scripts", "build_meng_v66_pptx.js");
const src = fs.readFileSync(BUILDER, "utf-8");

assert.ok(src.includes('require("./lib/theme")'), "构建器必须从 lib/theme 取参数");
assert.ok(!/const C = \{/.test(src), "构建器不得持有色板字面量（单一来源）");
assert.ok(!/ART_RANDOM_FONT_SIZE = \d/.test(src), "字号常量不得在构建器内定义");

// theme 自身不变量
assert.strictEqual(Object.keys(theme.C).length, 22);
assert.strictEqual(theme.SERIF, "Noto Serif CJK SC");
assert.strictEqual(theme.SANS, "Noto Sans CJK SC");
assert.deepStrictEqual(Object.keys(theme.MODULE).sort(), Object.keys(theme.MODULE_LABELS).sort());
assert.strictEqual(theme.ART_RANDOM_FONT_SIZE, 26);
assert.strictEqual(theme.FONT_FLOORS.original_verse, 28);
assert.strictEqual(theme.FONT_FLOORS.artifact_slot, 22);
for (const colorKey of Object.values(theme.MODULE)) {
  assert.ok(colorKey in theme.C, `MODULE 引用了不存在的色键: ${colorKey}`);
}

console.log(`LIB_THEME_SINGLE_SOURCE_OK colors=${Object.keys(theme.C).length} module=${Object.keys(theme.MODULE).length}`);
