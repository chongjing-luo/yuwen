"use strict";

/**
 * 兼容加载器：canonical 数据源已迁移至
 * work/teaching/选择性必修下册/氓/lesson.json（schema v1.0）。
 * 本文件保留模块接口供既有构建器/测试 require；不再承载内容，
 * 也不再依赖 meng_v65 / meng_v62（派生内容已内联进 JSON）。
 * 编辑课程数据请直接改 lesson.json（P-11 单一数据源）。
 */
const fs = require("fs");
const path = require("path");

const LESSON_JSON = path.join(__dirname, "..", "..", "work", "teaching", "选择性必修下册", "氓", "lesson.json");

module.exports = JSON.parse(fs.readFileSync(LESSON_JSON, "utf-8"));
