"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");
const builder = require("../scripts/build_meng_v66_pptx");

const globalRoot = process.env.NODE_GLOBAL_ROOT || "/usr/local/node-v22.22.2-linux-x64/lib/node_modules";
const JSZip = require(path.join(globalRoot, "pptxgenjs", "node_modules", "jszip"));

function decodeXml(value) {
  return value
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, "&");
}

async function main() {
  const archive = await JSZip.loadAsync(fs.readFileSync(builder.outputPath));
  const noteEntries = Object.keys(archive.files)
    .filter((name) => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(name));
  assert.strictEqual(noteEntries.length, builder.physicalPlan.length, "speaker-note XML count mismatch");

  for (const item of builder.physicalPlan) {
    const number = item.physical_number;
    const entry = archive.file(`ppt/notesSlides/notesSlide${number}.xml`);
    assert.ok(entry, `slide ${number} missing speaker-note XML`);
    const xml = await entry.async("string");
    const noteText = [...xml.matchAll(/<a:t>([\s\S]*?)<\/a:t>/g)]
      .map((match) => decodeXml(match[1]))
      .join("\n");
    assert.strictEqual((noteText.match(/【教师逐字稿】/g) || []).length, 1, `slide ${number} teacher-script marker count`);
    assert.strictEqual((noteText.match(/【本画面为何存在】/g) || []).length, 1, `slide ${number} function marker count`);
    assert.ok(noteText.includes(item.state.script.teacher_spoken), `slide ${number} teacher script differs from source`);
    assert.ok(noteText.includes(item.state.state_function), `slide ${number} function differs from source`);
  }

  process.stdout.write(`MENG_V66_PPTX_NOTES_OK physical=${builder.physicalPlan.length}\n`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
