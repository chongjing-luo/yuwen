#!/usr/bin/env node
"use strict";

const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const { PROJECT_ROOT, assertV6OutputPath, lessonDir, pathIsInside, stageDir } = require("./paths");

const DEFAULT_SOURCE_MANIFEST = "11_氓_V5交付清单_SHA256.txt";
const DEFAULT_BASELINE_MANIFEST = "baseline_manifest.json";

function parseArguments(argv) {
  const options = {
    projectRoot: PROJECT_ROOT,
    mode: null,
    sourceManifest: null,
    manifest: null,
  };
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (argument === "--write-manifest" || argument === "--verify") {
      if (options.mode) throw new Error("Choose exactly one of --write-manifest or --verify");
      options.mode = argument.slice(2);
    } else if (argument === "--project-root") {
      options.projectRoot = path.resolve(argv[++index]);
    } else if (argument === "--source-manifest") {
      options.sourceManifest = path.resolve(argv[++index]);
    } else if (argument === "--manifest") {
      options.manifest = path.resolve(argv[++index]);
    } else if (argument === "--help" || argument === "-h") {
      options.help = true;
    } else {
      throw new Error(`Unknown argument: ${argument}`);
    }
  }
  return options;
}

function usage() {
  return [
    "Usage:",
    "  node scripts/meng_v6/check_baseline.js --write-manifest [options]",
    "  node scripts/meng_v6/check_baseline.js --verify [options]",
    "",
    "Options:",
    "  --project-root PATH      Project root (defaults to this repository)",
    "  --source-manifest PATH   Explicit V5 delivery manifest used when writing",
    "  --manifest PATH          V6 baseline manifest path",
  ].join("\n");
}

function sha256(filePath) {
  return crypto.createHash("sha256").update(fs.readFileSync(filePath)).digest("hex");
}

function projectRelative(filePath, projectRoot) {
  const resolved = path.resolve(filePath);
  if (resolved !== projectRoot && !pathIsInside(resolved, projectRoot)) {
    throw new Error(`Baseline path is outside the project root: ${resolved}`);
  }
  return path.relative(projectRoot, resolved).split(path.sep).join("/");
}

function readExplicitPaths(sourceManifest, projectRoot) {
  const paths = new Set([projectRelative(sourceManifest, projectRoot)]);
  const lines = fs.readFileSync(sourceManifest, "utf8").split(/\r?\n/);
  for (const line of lines) {
    if (!line.trim()) continue;
    const match = line.match(/^[0-9a-fA-F]{64}\s{2}(.+)$/);
    if (!match) throw new Error(`Invalid V5 delivery manifest line: ${line}`);
    const filePath = path.resolve(projectRoot, match[1]);
    paths.add(projectRelative(filePath, projectRoot));
  }
  return [...paths].sort();
}

function fileRecord(relativePath, projectRoot) {
  const filePath = path.resolve(projectRoot, relativePath);
  if (!fs.existsSync(filePath)) throw new Error(`BASELINE_FILE_MISSING: ${relativePath}`);
  const stat = fs.statSync(filePath, { bigint: true });
  if (!stat.isFile()) throw new Error(`BASELINE_NOT_FILE: ${relativePath}`);
  return {
    path: relativePath,
    size: Number(stat.size),
    mtime_ns: stat.mtimeNs.toString(),
    sha256: sha256(filePath),
  };
}

function writeManifest({ projectRoot, sourceManifest, manifest }) {
  assertV6OutputPath(manifest, projectRoot);
  const files = readExplicitPaths(sourceManifest, projectRoot).map((relativePath) =>
    fileRecord(relativePath, projectRoot),
  );
  fs.mkdirSync(path.dirname(manifest), { recursive: true });
  const data = {
    schema_version: "1.0",
    baseline_version: "5.3-literary-participation",
    scope: "explicit-v5.3-delivery-manifest-plus-source-manifest",
    generated_at: new Date().toISOString(),
    source_manifest: projectRelative(sourceManifest, projectRoot),
    file_count: files.length,
    files,
  };
  fs.writeFileSync(manifest, `${JSON.stringify(data, null, 2)}\n`, "utf8");
  process.stdout.write(`BASELINE_MANIFEST_WRITTEN files=${files.length} path=${manifest}\n`);
}

function verifyManifest({ projectRoot, manifest }) {
  const data = JSON.parse(fs.readFileSync(manifest, "utf8"));
  const errors = [];
  if (!Array.isArray(data.files) || data.file_count !== data.files.length) {
    errors.push("BASELINE_MANIFEST_INVALID: file_count does not match files");
  }
  const seen = new Set();
  for (const expected of data.files || []) {
    if (seen.has(expected.path)) {
      errors.push(`BASELINE_DUPLICATE_PATH: ${expected.path}`);
      continue;
    }
    seen.add(expected.path);
    let actual;
    try {
      actual = fileRecord(expected.path, projectRoot);
    } catch (error) {
      errors.push(String(error.message || error));
      continue;
    }
    if (actual.size !== expected.size) {
      errors.push(`BASELINE_SIZE_MISMATCH: ${expected.path}`);
    }
    if (actual.sha256 !== expected.sha256) {
      errors.push(`BASELINE_SHA256_MISMATCH: ${expected.path}`);
    }
    if (actual.mtime_ns !== expected.mtime_ns) {
      errors.push(`BASELINE_MTIME_MISMATCH: ${expected.path}`);
    }
  }
  if (errors.length) {
    for (const error of errors) process.stderr.write(`${error}\n`);
    process.exitCode = 1;
    return;
  }
  process.stdout.write(`BASELINE_OK files=${data.files.length} manifest=${manifest}\n`);
}

function main() {
  let options;
  try {
    options = parseArguments(process.argv.slice(2));
    if (options.help) {
      process.stdout.write(`${usage()}\n`);
      return;
    }
    if (!options.mode) throw new Error("Choose --write-manifest or --verify");
    const lesson = lessonDir(options.projectRoot);
    options.sourceManifest ||= path.join(lesson, DEFAULT_SOURCE_MANIFEST);
    options.manifest ||= path.join(stageDir(options.projectRoot), DEFAULT_BASELINE_MANIFEST);
    if (options.mode === "write-manifest") writeManifest(options);
    else verifyManifest(options);
  } catch (error) {
    process.stderr.write(`${error.code ? `${error.code}: ` : ""}${error.message || error}\n`);
    process.exitCode = 2;
  }
}

if (require.main === module) main();

module.exports = { fileRecord, parseArguments, readExplicitPaths, verifyManifest, writeManifest };
