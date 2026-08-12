"use strict";

const fs = require("fs");
const path = require("path");

const PROJECT_ROOT = path.resolve(__dirname, "../..");
const LESSON_RELATIVE = path.join("work", "备课", "选择性必修下册", "氓");

function lessonDir(projectRoot = PROJECT_ROOT) {
  return path.resolve(projectRoot, LESSON_RELATIVE);
}

function stageDir(projectRoot = PROJECT_ROOT) {
  return path.join(lessonDir(projectRoot), "_v6_stage");
}

function pathIsInside(candidate, parent) {
  const relative = path.relative(parent, candidate);
  return relative !== "" && !relative.startsWith(`..${path.sep}`) && relative !== ".." && !path.isAbsolute(relative);
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

function outputPathError(code, message) {
  const error = new Error(message);
  error.code = code;
  return error;
}

function assertV6OutputPath(candidate, projectRoot = PROJECT_ROOT) {
  const resolvedCandidate = path.resolve(candidate);
  const resolvedStage = stageDir(projectRoot);
  if (!pathIsInside(resolvedCandidate, resolvedStage)) {
    throw outputPathError(
      "V6_OUTPUT_OUTSIDE_STAGE",
      `V6 output must be inside ${resolvedStage}: ${resolvedCandidate}`,
    );
  }
  if (/v5/i.test(path.basename(resolvedCandidate))) {
    throw outputPathError(
      "V6_OUTPUT_V5_NAME",
      `V6 output must not use a V5 filename: ${resolvedCandidate}`,
    );
  }

  if (fs.existsSync(resolvedStage)) {
    const realStage = fs.realpathSync(resolvedStage);
    const resolvedLesson = lessonDir(projectRoot);
    const realLesson = fs.existsSync(resolvedLesson)
      ? fs.realpathSync(resolvedLesson)
      : resolvedLesson;
    if (!pathIsInside(realStage, realLesson)) {
      throw outputPathError(
        "V6_OUTPUT_SYMLINK_ESCAPE",
        `V6 stage directory resolves outside the lesson directory: ${resolvedStage}`,
      );
    }
    const existingParent = nearestExistingParent(path.dirname(resolvedCandidate));
    const realParent = fs.realpathSync(existingParent);
    if (realParent !== realStage && !pathIsInside(realParent, realStage)) {
      throw outputPathError(
        "V6_OUTPUT_SYMLINK_ESCAPE",
        `V6 output resolves outside the stage directory: ${resolvedCandidate}`,
      );
    }
    if (fs.existsSync(resolvedCandidate)) {
      const realCandidate = fs.realpathSync(resolvedCandidate);
      if (!pathIsInside(realCandidate, realStage)) {
        throw outputPathError(
          "V6_OUTPUT_SYMLINK_ESCAPE",
          `V6 destination resolves outside the stage directory: ${resolvedCandidate}`,
        );
      }
    }
  }
  return resolvedCandidate;
}

module.exports = {
  LESSON_RELATIVE,
  PROJECT_ROOT,
  assertV6OutputPath,
  lessonDir,
  pathIsInside,
  stageDir,
};
