"use strict";

const assert = require("assert");
const fs = require("fs");
const path = require("path");

const builder = require("../scripts/build_meng_v65_pptx");

assert.strictEqual(builder.plan.length, 45);
assert.deepStrictEqual(builder.plan.map((item) => item.page_number), Array.from({ length: 45 }, (_, index) => index + 1));
assert.strictEqual(new Set(builder.plan.map((item) => item.page_id)).size, 45);
for (const item of builder.plan) {
  assert.ok(typeof item.render === "function", `${item.page_id} missing renderer`);
  const notes = builder.notesFor(item);
  assert.match(notes, new RegExp(`【V6.5页ID】${item.page_id.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}`));
  assert.match(notes, /【教师逐字稿】/);
  assert.match(notes, /【页面功能】/);
  assert.ok(notes.length > 300, `${item.page_id} notes are skeletal`);
}

const visibleText = (pageId) => builder.visibleTextFor(builder.plan.find((item) => item.page_id === pageId));
const forbiddenPhysicalFirstAnswers = {
  C104: /说明条件|安抚对方|另约婚期/,
  C303: /桑\s*[→—-]\s*鸠|鸠\s*[→—-]\s*女/,
  C404_405: /不爽\s*[→—-]\s*贰行|没有差错|前后不一|没有准则|反复无常/,
  C406: /沃若\s*[→—-]\s*黄而陨|食贫[｜|].*渐帷|不爽[｜|].*二三/,
  C503: /值得观察的早期细节|承诺需要长期行动核验|婚前已经证实预谋|女子应为后来伤害负责/,
  C602: /第一个.*落在旧愿|第二个.*落在现实/,
  C604: /旧日确有|后来也确有/,
  C605: /诗写到：|诗没有写到：|后来实际去了哪里/,
  C606_S01: /相识议婚\s*[→—-]|等待迁嫁|婚后失衡|劳作孤立|停止判断/,
};
for (const [pageId, forbidden] of Object.entries(forbiddenPhysicalFirstAnswers)) {
  assert.ok(!forbidden.test(visibleText(pageId)), `${pageId} physical slide reveals a first-answer product`);
}

// C303's遮句 experiment is invalid if the projection keeps either of the
// sentences that the student is being asked to remove from view.
assert.ok(
  !/桑之未落，其叶沃若。|于嗟鸠兮，无食桑葚！/.test(visibleText("C303")),
  "C303 projection contaminates the遮句 comparison",
);

// Keep the two endpoints in one uninterrupted string.  Full-width spacing
// previously made the rendered final phrase appear as “焉哉—亦已”.
assert.ok(
  visibleText("S08").includes("从“氓之蚩蚩”读到“亦已焉哉”"),
  "S08 must render the opening and ending in their correct reading order",
);

assert.ok(builder.outputPath.endsWith("04_氓_V65完整课堂课件_45页无插图逐字稿_V4.pptx"));
assert.ok(builder.outputPath.includes(`${path.sep}v65${path.sep}`));
if (fs.existsSync(builder.outputPath)) {
  assert.ok(fs.statSync(builder.outputPath).size > 10000, "existing physical build is unexpectedly small");
}

console.log("MENG_V65_PPTX_BUILD_CONTRACT_OK slides=45");
