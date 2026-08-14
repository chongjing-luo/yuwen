"use strict";

const assert = require("assert");

const lesson = require("../scripts/meng_v65/lesson");

const EXPECTED_IDS = [
  "O01", "O02", "O03", "O04", "O05", "O06", "O07", "O08",
  "C101", "C102", "C103", "C104", "C105",
  "C201", "C202", "C204", "C206",
  "C301", "C302", "C303", "C305", "C306",
  "C401", "C402", "C403", "C404_405", "C406",
  "C501", "C502", "C503", "C504", "C505",
  "C601", "C602", "C603", "C604", "C605", "C606_S01",
  "S02", "S03", "S04", "S05A", "S05B", "S06", "S08",
];

assert.strictEqual(lesson.version, "6.5-v4-45-page-continuous-understanding");
assert.strictEqual(lesson.pages.length, 45);
assert.deepStrictEqual(lesson.pages.map((page) => page.page_id), EXPECTED_IDS);
assert.deepStrictEqual(lesson.pages.map((page) => page.page_number), Array.from({ length: 45 }, (_, index) => index + 1));
assert.strictEqual(lesson.pages.reduce((sum, page) => sum + page.minutes, 0), 230);

const requiredPageFields = [
  "page_number", "page_id", "legacy_refs", "module", "title", "minutes",
  "literary_object", "unique_function", "student_action", "artifact", "next_use",
  "deletion_loss", "visual_duty", "illustration_eligibility", "protocol_signature",
  "frontstage", "script",
];
const requiredScriptFields = [
  "teacher_spoken", "scene", "stage_directions", "timeboxes", "branches",
  "listener_task", "evidence_location", "cut_line",
];

for (const page of lesson.pages) {
  for (const field of requiredPageFields) {
    assert.ok(page[field] !== undefined && page[field] !== null && page[field] !== "", `${page.page_id} missing ${field}`);
  }
  for (const field of requiredScriptFields) {
    assert.ok(page.script[field] !== undefined && page.script[field] !== null && page.script[field] !== "", `${page.page_id} script missing ${field}`);
  }
  assert.ok(Array.isArray(page.student_action) && page.student_action.length >= 1, `${page.page_id} missing student action`);
  assert.ok(Array.isArray(page.script.timeboxes) && page.script.timeboxes.length >= 1, `${page.page_id} missing timeboxes`);
  assert.strictEqual(
    page.script.timeboxes.reduce((sum, item) => sum + item.seconds, 0),
    page.minutes * 60,
    `${page.page_id} timebox mismatch`,
  );
  assert.ok(page.script.teacher_spoken.length >= Math.min(180, page.minutes * 110), `${page.page_id} teacher script is too skeletal`);
  assert.ok(!/学生角色|设计目标|今天不收集知识碎片|不填表|P[0-3]|后台|测试/.test(page.frontstage.join("\n")), `${page.page_id} leaks design language`);
}

const allLegacyPages = new Set(lesson.pages.flatMap((page) => page.legacy_refs));
for (let index = 1; index <= 48; index += 1) {
  assert.ok(allLegacyPages.has(index), `legacy page ${index} has no disposition`);
}

assert.strictEqual(lesson.pages[0].page_id, "O01");
assert.match(lesson.pages[0].unique_function, /小学至高中|广泛/);
assert.match(lesson.pages[1].unique_function, /每人|全班|文学/);
assert.match(lesson.pages[2].script.teacher_spoken, /你们|黑板|相遇以后|共同生活/);
assert.ok(!/幸福.*关于什么|幸福.*本质/.test(lesson.pages.slice(0, 4).map((page) => page.frontstage.join("\n")).join("\n")));

assert.ok(!lesson.pages.some((page) => page.page_id === "O09"));
assert.ok(!lesson.pages.some((page) => page.page_id === "C405"));
assert.ok(!lesson.pages.some((page) => page.page_id === "S01"));
assert.ok(!lesson.pages.some((page) => page.page_id === "S07"));

const responsibilityPage = lesson.pages.find((page) => page.page_id === "C404_405");
assert.match(responsibilityPage.original_text, /女也不爽，士贰其行/);
assert.match(responsibilityPage.original_text, /士也罔极，二三其德/);

const discussionPage = lesson.pages.find((page) => page.page_id === "S04");
assert.ok(!/个人写三行|开课时的一句|现在的一句/.test(discussionPage.script.teacher_spoken), "S04 repeats a heavy three-line writing protocol");
assert.match(discussionPage.script.teacher_spoken, /每个人|依次|开口/);
assert.match(discussionPage.script.teacher_spoken, /每组只留一张/);

const retrievalPage = lesson.pages.find((page) => page.page_id === "S05A");
const retrievalFrontstage = retrievalPage.frontstage.join("\n");
assert.ok(!/最早诗歌总集|305篇|风、雅、颂|出自《卫风》/.test(retrievalFrontstage), "S05 frontstage reveals retrieval answers");

const wordRetrievalPage = lesson.pages.find((page) => page.page_id === "S05B");
assert.match(wordRetrievalPage.unique_function, /字词/);
assert.match(wordRetrievalPage.script.teacher_spoken, /任选两个/);
assert.ok(!/《诗经》是什么|有多少篇|分哪三类/.test(wordRetrievalPage.frontstage.join("\n")), "S05B must not repeat the cultural retrieval task");

const causePage = lesson.pages.find((page) => page.page_id === "S03");
assert.ok(!/失衡|缺少托举|警讯|沉没成本|责任边界/.test(causePage.frontstage.join("\n")), "S03 reveals the cause framework before first generation");

const knowledgeMapPage = lesson.pages.find((page) => page.page_id === "S06");
assert.ok(!/沃若|黄而陨|老｜|信誓|不思|涟涟|汤汤|晏晏|旦旦/.test(knowledgeMapPage.frontstage.join("\n")), "S06 reveals examples before students supply them");

const firstAnswerContracts = {
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
for (const [pageId, forbidden] of Object.entries(firstAnswerContracts)) {
  const page = lesson.pages.find((item) => item.page_id === pageId);
  assert.ok(!forbidden.test(page.frontstage.join("\n")), `${pageId} frontstage reveals a first-answer product`);
}

const objectToPersonPage = lesson.pages.find((page) => page.page_id === "C303");
assert.ok(
  !/桑之未落，其叶沃若。|于嗟鸠兮，无食桑葚！/.test(objectToPersonPage.frontstage.join("\n")),
  "C303 frontstage must not display the lines removed by its遮句 experiment",
);

const finalReadingPage = lesson.pages.find((page) => page.page_id === "S08");
assert.match(finalReadingPage.frontstage.join("\n"), /氓之蚩蚩.*亦已焉哉/);

const cultureRetrievalScript = retrievalPage.script.teacher_spoken;
const cultureWaitIndex = cultureRetrievalScript.indexOf("（等待作答。）");
assert.ok(cultureWaitIndex > 0, "S05 script must mark a real wait before cultural answers");
assert.ok(!/最早的诗歌总集|三百零五篇|风、雅、颂|出自《卫风》/.test(cultureRetrievalScript.slice(0, cultureWaitIndex)), "S05 teacher leaks cultural answers before retrieval");

const wordRetrievalScript = wordRetrievalPage.script.teacher_spoken;
const wordWaitIndex = wordRetrievalScript.indexOf("（等待首答。）");
assert.ok(wordWaitIndex > 0, "S05B must wait before word correction");
assert.ok(!/愆.*拖延|将.*请|说.*脱|爽.*差错/.test(wordRetrievalScript.slice(0, wordWaitIndex)), "S05B leaks word meanings before retrieval");

const knowledgeScript = knowledgeMapPage.script.teacher_spoken;
const knowledgeWaitIndex = knowledgeScript.indexOf("（等待补例。）");
assert.ok(knowledgeWaitIndex > 0, "S06 script must mark a real wait before representative examples");
assert.ok(!/沃若|黄而陨|于嗟|信誓|不思|涟涟|汤汤|晏晏|旦旦/.test(knowledgeScript.slice(0, knowledgeWaitIndex)), "S06 teacher leaks representative examples before students supply them");

for (let index = 0; index <= lesson.pages.length - 3; index += 1) {
  const fingerprints = lesson.pages.slice(index, index + 3).map((page) => JSON.stringify(page.protocol_signature));
  assert.ok(new Set(fingerprints).size > 1, `three identical protocol fingerprints at pages ${index + 1}-${index + 3}`);
}

console.log("MENG_V65_LESSON_CONTRACT_OK pages=45 minutes=230");
