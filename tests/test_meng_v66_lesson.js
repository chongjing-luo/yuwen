"use strict";

const assert = require("assert");
const lesson = require("../scripts/meng_v66/lesson");

assert.strictEqual(lesson.version, "6.6-v5-p2-closure-candidate");
assert.strictEqual(lesson.target_pages, 81);
assert.ok(lesson.target_logical_pages >= 46);
assert.ok(lesson.target_pages > lesson.target_logical_pages);
assert.strictEqual(lesson.target_natural_minutes, 280);
assert.strictEqual(lesson.pages.reduce((sum, p) => sum + p.minutes, 0), lesson.target_natural_minutes);
assert.deepStrictEqual(lesson.pages.map((p) => p.page_number), Array.from({ length: lesson.pages.length }, (_, i) => i + 1));
assert.strictEqual(new Set(lesson.pages.map((p) => p.page_id)).size, lesson.pages.length);

const fields = ["prior_input", "unique_difficulty", "unique_function", "literary_object", "info_state", "student_action", "participation_path", "artifact", "teacher_role", "wait_contract", "feedback_revision", "next_use", "normal_counterexample", "visual_duty", "illustration_eligibility", "first_person_reception", "story_return", "deletion_loss", "adjacent_counterproof", "failure_signals", "states", "script"];
for (const p of lesson.pages) {
  for (const f of fields) assert.ok(p[f] !== undefined && p[f] !== null && p[f] !== "", `${p.page_id} missing ${f}`);
  assert.strictEqual(p.states.reduce((sum, s) => sum + s.seconds, 0), p.minutes * 60, `${p.page_id} state time mismatch`);
  assert.strictEqual(p.script.timeboxes.reduce((sum, s) => sum + s.seconds, 0), p.minutes * 60, `${p.page_id} script time mismatch`);
  assert.ok(p.script.teacher_spoken.length >= Math.min(160, p.minutes * 80), `${p.page_id} script skeletal`);
  assert.ok(Array.isArray(p.failure_signals) && p.failure_signals.length >= 1, `${p.page_id} missing failures`);
  for (const s of p.states) {
    assert.ok(s.state_id && s.state_function && s.render_mode && Array.isArray(s.frontstage), `${p.page_id} invalid state`);
    assert.ok(s.script && s.script.teacher_spoken && s.script.cut_line, `${p.page_id}-${s.state_id} missing physical script`);
    assert.strictEqual(s.script.timeboxes.reduce((sum, item) => sum + item.seconds, 0), s.seconds, `${p.page_id}-${s.state_id} physical script time mismatch`);
  }
  if (p.states.length > 1) assert.strictEqual(new Set(p.states.map((s) => s.script.teacher_spoken)).size, p.states.length, `${p.page_id} repeats physical scripts`);
}

for (const id of ["O01", "O02", "O03", "O04"]) {
  const state = lesson.pages.find((p) => p.page_id === id).states[0];
  assert.doesNotMatch(state.script.branches.map((b) => `${b.kind}${b.response}`).join("\n"), /原词|原诗/, `${id} opening branches use poem template before poem analysis`);
}

assert.ok(!lesson.pages.some((p) => p.page_id === "O03_OLD"));
assert.ok(lesson.pages.some((p) => p.page_id === "O04" && /第一部诗歌总集/.test(p.frontstage.join(""))));
assert.ok(lesson.pages.some((p) => p.page_id === "C303A"));
assert.ok(lesson.pages.some((p) => p.page_id === "C303B"));
assert.match(lesson.pages.find((p) => p.page_id === "C303A").unique_function, /有意删去|删句/);
assert.doesNotMatch(lesson.pages.find((p) => p.page_id === "C303A").unique_function, /没有桑叶和斑鸠时的真实听读首答/);
assert.ok(lesson.pages.some((p) => p.page_id === "C306" && /每人/.test(p.student_action.join(""))));
assert.match(lesson.pages.find((p) => p.page_id === "C406").artifact, /个人第四章/);
assert.match(lesson.pages.find((p) => p.page_id === "C606_S01").student_action.join(""), /每人先独立.*六章/);
assert.ok(lesson.pages.find((p) => p.page_id === "C606_S01").states.some((s) => s.state_id === "B3" && s.render_mode === "blank_recall"));
assert.match(lesson.pages.find((p) => p.page_id === "S05B").unique_function, /六章各一项全员最低门槛/);
assert.ok(lesson.pages.find((p) => p.page_id === "S06").states.some((s) => s.state_id === "B0" && !/叙事推进|比兴与前后对照|复现、回环|四言节奏/.test(s.frontstage.join(""))));
assert.strictEqual(lesson.pages.find((p) => p.page_id === "C604").states.length, 2);
assert.ok(!/她记得的旧日|后来显出的事实|旧日欢乐与后来失信/.test(lesson.pages.find((p) => p.page_id === "C604").states[0].frontstage.join("")));
assert.ok(lesson.pages.find((p) => p.page_id === "C102").states.some((s) => s.state_id === "B3" && /蚩蚩.*一说嬉笑/.test(s.frontstage.join(""))), "C102 missing first-line lexical calibration");
assert.ok(lesson.pages.find((p) => p.page_id === "S02").states.some((s) => s.state_id === "B3" && /第二问/.test(s.state_function)));
assert.match(lesson.pages.find((p) => p.page_id === "S02").states.find((s) => s.state_id === "B3").frontstage.join(""), /四个方面都写到/);
assert.ok(lesson.pages.find((p) => p.page_id === "S03").states.some((s) => s.state_id === "B3" && /完整末答/.test(s.state_function)));
for (const token of ["割舍更难", "不能证明什么", "亦已焉哉"]) assert.match(lesson.pages.find((p) => p.page_id === "S03").states.find((s) => s.state_id === "B3").frontstage.join(""), new RegExp(token));
assert.ok(lesson.pages.find((p) => p.page_id === "S04").states.some((s) => s.state_id === "B4" && /文学长卷/.test(s.state_function)));
assert.strictEqual(lesson.pages.find((p) => p.page_id === "S05A").states.length, 3);
assert.ok(lesson.pages.find((p) => p.page_id === "S06").states.some((s) => s.state_id === "B3" && /四类最低识别/.test(s.state_function)));

const visibleAll = lesson.pages.flatMap((p) => p.states.map((s) => s.frontstage.join("\n"))).join("\n");
assert.ok(!/学生角色|设计目标|今天不收集知识碎片|P[0-3]|后台|机器校验/.test(visibleAll), "frontstage leaks backend language");
assert.ok(!/B[0-9]|O0[1-9]|C[0-9]{3}|S0[1-9]/.test(visibleAll), "frontstage leaks state/page ids");
assert.ok(!lesson.pages.find((p) => p.page_id === "C504").frontstage.join("\n").includes("三秒沉默"), "C504 leaks stage direction");
assert.ok(!/幸福.*本质/.test(lesson.pages.slice(0, 4).flatMap((p) => p.frontstage).join("\n")), "opening asks premature abstract question");
assert.strictEqual(lesson.pages.find((p) => p.page_id === "O05").states.length, 3, "O05 must keep three readable listening states");
assert.strictEqual(lesson.pages.find((p) => p.page_id === "O06").states.length, 3, "O06 must keep three readable listening states");

for (const id of ["C102", "C103", "C104", "C303B", "C404_405", "C606_S01", "S02", "S03", "S04", "S05B", "S06"]) assert.ok(lesson.pages.find((p) => p.page_id === id).states.length >= 2, `${id} missing physical state separation`);

assert.ok(!/长期行动核验|求助通道|不长期失衡/.test(lesson.pages.find((p) => p.page_id === "S04").states.flatMap((s) => s.frontstage).join("\n")), "S04 frontstage remains consultative/AI language");
const wordCalibration = lesson.pages.find((p) => p.page_id === "S05B").states.find((s) => s.state_id === "B2").frontstage.join("\n");
for (const token of ["愆（qiān）", "筮（shì）", "说（tuō）", "爽（shuǎng）", "咥（xì）", "泮（pàn）"]) assert.match(wordCalibration, new RegExp(token.replace(/[（）]/g, ".")), `word calibration missing ${token}`);
const artB0 = lesson.pages.find((p) => p.page_id === "S06").states.find((s) => s.state_id === "B0").frontstage.join("\n");
assert.doesNotMatch(artB0, /相识—迁嫁—婚后—止息|淇水再现|老｜老/);
const artCards = lesson.pages.find((p) => p.page_id === "S06").states.find((s) => s.state_id === "B0").frontstage.slice(1, -1);
assert.strictEqual(artCards.length, 16, "S06 B0 must expose sixteen atomic cards");
assert.strictEqual(new Set(artCards).size, artCards.length, "S06 B0 cards must be unique");
for (const card of artCards) {
  assert.doesNotMatch(card, /[／/→｜]/, `S06 B0 pre-pairs evidence inside card: ${card}`);
  assert.strictEqual(Array.from(card.replace(/[，。！？；：、“”‘’]/g, "")).length, 4, `S06 B0 card is not equal-grain: ${card}`);
}
assert.match(lesson.pages.find((p) => p.page_id === "S06").states.find((s) => s.state_id === "B2").frontstage.join("\n"), /赋：铺陈直叙/);

for (const id of ["O05", "O06"]) for (const state of lesson.pages.find((p) => p.page_id === id).states) {
  const branches = state.script.branches.map((b) => `${b.kind}${b.response}`).join("\n");
  assert.doesNotMatch(branches, /暂时没有答案|判断越过原诗/, `${id}-${state.state_id} keeps answer template`);
  assert.match(branches, /跟丢|错行|卡住|卡顿|静默|提前/, `${id}-${state.state_id} lacks listening-specific branch`);
}
for (const state of lesson.pages.find((p) => p.page_id === "S05A").states) {
  const branches = state.script.branches.map((b) => `${b.kind}${b.response}`).join("\n");
  assert.doesNotMatch(branches, /判断越过原诗|原词支撑/, `S05A-${state.state_id} keeps poem-analysis branch`);
  assert.match(branches, /留空|混淆|遗漏|错空|核对/, `S05A-${state.state_id} lacks culture-retrieval branch`);
}
for (const state of lesson.pages.find((p) => p.page_id === "S05B").states) {
  const branches = state.script.branches.map((b) => `${b.kind}${b.response}`).join("\n");
  assert.doesNotMatch(branches, /判断越过原诗/, `S05B-${state.state_id} keeps generic judgment branch`);
  assert.match(branches, /读音|原句|通假|六项|句中义/, `S05B-${state.state_id} lacks word-retrieval branch`);
}
assert.match(lesson.pages.find((p) => p.page_id === "O08").states[0].script.cut_line, /三个问题先留在手边.*第一章.*他做了什么/);
assert.doesNotMatch(lesson.pages.find((p) => p.page_id === "C306").frontstage.join("\n"), /讲回她的一生/);
assert.match(lesson.pages.find((p) => p.page_id === "S02").states.find((s) => s.state_id === "B3").frontstage.join("\n"), /不被兄弟理解/);
assert.doesNotMatch(lesson.pages.find((p) => p.page_id === "S02").states.find((s) => s.state_id === "B3").frontstage.join("\n"), /不被家人理解/);
assert.doesNotMatch(lesson.pages.find((p) => p.page_id === "C404_405").states.find((s) => s.state_id === "B2").frontstage.join("\n"), /^女子没有差错/m);
assert.match(lesson.pages.find((p) => p.page_id === "C404_405").states.find((s) => s.state_id === "B2").frontstage.join("\n"), /婚姻的操持中.*并无差失|伤害不能归责于她/);
assert.match(lesson.pages.find((p) => p.page_id === "C606_S01").states.find((s) => s.state_id === "B3").script.stage_directions.join("\n"), /摘下|反扣|覆盖/);
assert.match(lesson.pages.find((p) => p.page_id === "S02").states.find((s) => s.state_id === "B3").frontstage.join("\n"), /原稿已齐全.*说得更具体/);
assert.doesNotMatch(lesson.pages.find((p) => p.page_id === "S02").states.find((s) => s.state_id === "B3").script.teacher_spoken, /必须是你最初旧稿没有|必须.*新增/);
assert.strictEqual(lesson.pages.find((p) => p.page_id === "S04").states.length, 5);
const futureB2 = lesson.pages.find((p) => p.page_id === "S04").states.find((s) => s.state_id === "B2").frontstage.join("\n");
const futureB3 = lesson.pages.find((p) => p.page_id === "S04").states.find((s) => s.state_id === "B3").frontstage.join("\n");
assert.doesNotMatch(futureB2, /诗中写到的|由诗想到今天|必要时离开/);
for (const token of ["诗中写到的", "由诗想到今天", "现代建议不是诗中已经发生的结局"]) assert.match(futureB3, new RegExp(token));

const artCats = new Map([
  ["抱布贸丝", "A"], ["送子涉淇", "A"], ["以我贿迁", "A"], ["夙兴夜寐", "A"],
  ["桑之未落", "B"], ["桑之落矣", "B"], ["于嗟鸠兮", "B"], ["于嗟女兮", "B"],
  ["不思其反", "C"], ["反是不思", "C"], ["不见复关", "C"], ["既见复关", "C"],
  ["泣涕涟涟", "D"], ["氓之蚩蚩", "D"], ["信誓旦旦", "D"], ["言笑晏晏", "D"],
]);
for (let col = 0; col < 4; col += 1) {
  const counts = {};
  for (let row = 0; row < 4; row += 1) counts[artCats.get(artCards[row * 4 + col])] = (counts[artCats.get(artCards[row * 4 + col])] || 0) + 1;
  assert.ok(Math.max(...Object.values(counts)) <= 1, `S06 B0 category clusters in column ${col + 1}`);
}
for (const [a, b] of [["桑之未落", "桑之落矣"], ["于嗟鸠兮", "于嗟女兮"], ["不思其反", "反是不思"], ["不见复关", "既见复关"]]) {
  const ia = artCards.indexOf(a), ib = artCards.indexOf(b);
  assert.notStrictEqual(Math.floor(ia / 4), Math.floor(ib / 4), `S06 B0 pair shares row: ${a}/${b}`);
  assert.notStrictEqual(ia % 4, ib % 4, `S06 B0 pair shares column: ${a}/${b}`);
  assert.ok(Math.max(Math.abs(Math.floor(ia / 4) - Math.floor(ib / 4)), Math.abs((ia % 4) - (ib % 4))) > 1, `S06 B0 pair is adjacent: ${a}/${b}`);
}

console.log(`MENG_V66_LESSON_CONTRACT_OK logical=${lesson.target_logical_pages} physical=${lesson.target_pages} minutes=${lesson.target_natural_minutes}`);
