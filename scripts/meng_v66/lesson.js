"use strict";

/**
 * 历史V6.6兼容加载器，仅在旧lesson.json存在时供旧构建器读取。
 * 它不是现行备课默认入口，也不得被当作v2 strict课程数据。
 * 《氓》现行候选须依次重走G0/G1/G2，在G1真实批准前不重建此JSON。
 */
const fs = require("fs");
const path = require("path");

const LESSON_JSON = path.join(__dirname, "..", "..", "work", "teaching", "选择性必修下册", "氓", "lesson.json");

module.exports = JSON.parse(fs.readFileSync(LESSON_JSON, "utf-8"));
