"use strict";

const fs = require("fs");
const path = require("path");

const PROJECT_ROOT = path.resolve(__dirname, "../..");
const LESSON_RELATIVE = path.join("work", "备课", "选择性必修下册", "氓");

function lessonDir(projectRoot = PROJECT_ROOT) {
  return path.resolve(projectRoot, LESSON_RELATIVE);
}

function stageDir(projectRoot = PROJECT_ROOT) {
  return path.join(lessonDir(projectRoot), "_v62_stage");
}

function pathIsInside(candidate, parent) {
  const relative = path.relative(parent, candidate);
  return relative !== "" && relative !== ".." && !relative.startsWith(`..${path.sep}`) && !path.isAbsolute(relative);
}

function nearestExistingParent(candidate) {
  let current = candidate;
  while (!fs.existsSync(current)) {
    const parent = path.dirname(current);
    if (parent === current) return current;
    current = parent;
  }
  return current;
}

function assertV62OutputPath(candidate, projectRoot = PROJECT_ROOT) {
  const resolved = path.resolve(candidate);
  const stage = stageDir(projectRoot);
  if (!pathIsInside(resolved, stage)) {
    const error = new Error(`V6.2 output must be inside ${stage}: ${resolved}`);
    error.code = "V62_OUTPUT_OUTSIDE_STAGE";
    throw error;
  }
  if (fs.existsSync(stage)) {
    const realStage = fs.realpathSync(stage);
    const existingParent = nearestExistingParent(path.dirname(resolved));
    const realParent = fs.realpathSync(existingParent);
    if (realParent !== realStage && !pathIsInside(realParent, realStage)) {
      const error = new Error(`V6.2 output resolves outside stage: ${resolved}`);
      error.code = "V62_OUTPUT_SYMLINK_ESCAPE";
      throw error;
    }
  }
  return resolved;
}

module.exports = { PROJECT_ROOT, LESSON_RELATIVE, lessonDir, stageDir, assertV62OutputPath };
