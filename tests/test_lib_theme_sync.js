"use strict";

/**
 * theme.js ↔ build_meng_v66_pptx.js 同步防护：
 * 从构建器源码正则提取 C / SERIF / SANS / MODULE / 字号常量，与 lib/theme.js 比对。
 * 构建器改参数而不改 theme（或反之）→ 本测试失败，逼同步。
 */
const assert = require("assert");
const fs = require("fs");
const path = require("path");
const theme = require("../scripts/lib/theme");

const BUILDER = path.join(__dirname, "..", "scripts", "build_meng_v66_pptx.js");
const src = fs.readFileSync(BUILDER, "utf-8");

function extractObject(varName) {
  const re = new RegExp(`const ${varName} = \\{([\\s\\S]*?)\\};`);
  const m = src.match(re);
  assert.ok(m, `构建器中未找到 const ${varName}`);
  const out = {};
  for (const [, key, value] of m[1].matchAll(/([A-Za-z_][\w]*)\s*:\s*"([^"]+)"/g)) {
    out[key] = value;
  }
  return out;
}

assert.strictEqual(theme.SERIF, "Noto Serif CJK SC");
assert.strictEqual(theme.SANS, "Noto Sans CJK SC");
assert.ok(src.includes(`"${theme.SERIF}"`), "构建器应使用同一 SERIF");
assert.ok(src.includes(`"${theme.SANS}"`), "构建器应使用同一 SANS");

const builderC = extractObject("C");
assert.strictEqual(Object.keys(builderC).length, 22, "构建器 C 应为 22 色");
for (const [key, value] of Object.entries(builderC)) {
  assert.strictEqual(theme.C[key], value, `色板漂移: C.${key}`);
}
for (const key of Object.keys(theme.C)) {
  assert.ok(key in builderC, `theme.C 多出构建器没有的键: ${key}`);
}

// 构建器 MODULE 值为数组 [中文名, C.xxx]——按 C 引用名提取
const moduleBlock = src.match(/const MODULE = \{([\s\S]*?)\};/);
assert.ok(moduleBlock, "未找到 MODULE");
const builderModule = {};
for (const [, key, colorKey] of moduleBlock[1].matchAll(/([A-Za-z_][\w]*)\s*:\s*\[[^\]]*,\s*C\.([A-Za-z_][\w]*)\s*\]/g)) {
  builderModule[key] = colorKey;
}
assert.ok(Object.keys(builderModule).length >= 8, "MODULE 提取不应为空");
for (const [key, colorKey] of Object.entries(builderModule)) {
  assert.strictEqual(theme.MODULE[key], colorKey, `章节色漂移: MODULE.${key} 应为 ${colorKey}`);
}

// 字号下限（构建器的 ART_RANDOM_FONT_SIZE 应等于短语卡下限）
const m = src.match(/ART_RANDOM_FONT_SIZE = (\d+)/);
assert.ok(m, "未找到 ART_RANDOM_FONT_SIZE");
assert.strictEqual(Number(m[1]), theme.FONT_FLOORS.phrase_card, "短语卡字号下限漂移");
assert.strictEqual(theme.FONT_FLOORS.original_verse, 28);
assert.strictEqual(theme.FONT_FLOORS.artifact_slot, 22);

console.log(`LIB_THEME_SYNC_OK colors=${Object.keys(builderC).length} module=${Object.keys(builderModule).length}`);
