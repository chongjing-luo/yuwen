"use strict";

/**
 * 统一路径工具（E3：合并 meng_v6/meng_v62 各自的 paths 副本）。
 * 新代码一律从这里取；旧构建器内的副本随其归档退役。
 */
const path = require("path");

const PROJECT_ROOT = path.resolve(__dirname, "..", "..");

/** 断言 target 位于 root 内（防符号链接/写越界——沿用 meng_v6/paths 的边界保护语义） */
function assertInside(root, target) {
  const rel = path.relative(root, target);
  if (rel.startsWith("..") || path.isAbsolute(rel)) {
    throw new Error(`path escapes root: ${target} not inside ${root}`);
  }
  return target;
}

/** 项目内路径拼接（自动校验不越界） */
function inRoot(...segments) {
  return assertInside(PROJECT_ROOT, path.join(PROJECT_ROOT, ...segments));
}

module.exports = { PROJECT_ROOT, assertInside, inRoot };
