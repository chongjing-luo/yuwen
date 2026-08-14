"use strict";

const assert = require("assert");
const lesson = require("../scripts/meng_v66/lesson");
const builder = require("../scripts/build_meng_v66_pptx");

assert.strictEqual(builder.physicalPlan.length, lesson.target_pages);
assert.deepStrictEqual(builder.physicalPlan.map((p) => p.physical_number), Array.from({ length: lesson.target_pages }, (_, i) => i + 1));
for (const item of builder.physicalPlan) assert.ok(item.page && item.state && item.state.render_mode, "invalid physical item");

assert.ok(!/不是来换丝|转过话头/.test(builder.visibleTextFor("C102", "B0")), "C102 B0 leaks calibration");
assert.ok(/不是来换丝|转过话头/.test(builder.visibleTextFor("C102", "B2")), "C102 B2 missing calibration");
assert.ok(/蚩蚩.*一说嬉笑|布.*一说布币/.test(builder.visibleTextFor("C102", "B3")), "C102 B3 missing first-line lexical calibration");
assert.ok(!/解释、安抚、重新约定/.test(builder.visibleTextFor("C104", "B0")), "C104 B0 leaks categories");
assert.ok(/解释、安抚、重新约定/.test(builder.visibleTextFor("C104", "B2")), "C104 B2 missing categories");
assert.ok(!/桑叶在眼前|由眼前物象起声/.test(builder.visibleTextFor("C303B", "B1")), "C303B B1 leaks structure");
assert.ok(/由眼前物象起声/.test(builder.visibleTextFor("C303B", "B2")), "C303B B2 missing naming");
assert.ok(!/女子没有差错|反复无常/.test(builder.visibleTextFor("C404_405", "B0")), "responsibility B0 leaks meanings");
assert.ok(/婚姻的操持中.*并无差失|反复无常/.test(builder.visibleTextFor("C404_405", "B2")), "responsibility B2 missing bounded meanings");
assert.ok(/伤害不能归责于她/.test(builder.visibleTextFor("C404_405", "B2")), "responsibility B2 missing blame boundary");
assert.ok(!/伤害的责任在他|不能倒推/.test(builder.visibleTextFor("S03", "B0")), "cause B0 leaks framework");
assert.ok(/伤害的责任在他|不能倒推/.test(builder.visibleTextFor("S03", "B2")), "cause B2 missing framework");
assert.ok(!/审慎了解|言行一致/.test(builder.visibleTextFor("S04", "B0")), "future B0 leaks standard supports");
assert.ok(/先听你们写下的话|原作者读卡/.test(builder.visibleTextFor("S04", "B2")), "future B2 lacks real student-card stage");
assert.ok(!/诗中写到的|由诗想到今天|必要时离开/.test(builder.visibleTextFor("S04", "B2")), "future B2 leaks teacher summary");
assert.ok(/诗中写到的|由诗想到今天|现代建议不是诗中已经发生的结局/.test(builder.visibleTextFor("S04", "B3")), "future B3 fails to separate text from modern extension");
assert.ok(!/长期行动核验|求助通道|不长期失衡/.test(builder.visibleTextFor("S04", "B3")), "future B3 keeps consultative language");
assert.ok(!/愆：延误|咥（xì）/.test(builder.visibleTextFor("S05B", "B0")), "word B0 leaks answers");
assert.ok(/愆（qiān）|说（tuō）|爽（shuǎng）|咥（xì）|泮（pàn）/.test(builder.visibleTextFor("S05B", "B2")), "word B2 missing complete pronunciation correction");
assert.ok(!/六章叙事推进|桑叶比兴与前后对照/.test(builder.visibleTextFor("S06", "B0")), "art B0 leaks terminology");
assert.ok(/六章叙事推进|桑叶比兴与前后对照/.test(builder.visibleTextFor("S06", "B2")), "art B2 missing terminology");
assert.ok(/四类都先留下一个原诗例子/.test(builder.visibleTextFor("S06", "B3")), "art B3 missing four-class mastery gate");
assert.ok(!/[／/→｜]/.test(builder.visibleTextFor("S06", "B0")), "art B0 still pre-pairs atomic evidence");
assert.ok(builder.ART_RANDOM_FONT_SIZE >= 24, "art B0 card font remains below back-row threshold");

assert.ok(!/她记得的旧日|后来显出的事实|旧日欢乐与后来失信/.test(builder.visibleTextFor("C604", "B0")), "C604 B0 verbally pre-classifies cards");
assert.ok(/她记得的旧日|后来显出的事实/.test(builder.visibleTextFor("C604", "B1")), "C604 B1 missing post-calibration");
assert.ok(!/相识议婚|等待迁嫁|桑叶劝告/.test(builder.visibleTextFor("C606_S01", "B3")), "C606 B3 keeps answer scaffold during recall");
assert.ok(/答案已经撤下/.test(builder.visibleTextFor("C606_S01", "B3")), "C606 B3 missing explicit physical withdrawal");
assert.ok(/只写自己的答案|四个方面都写到/.test(builder.visibleTextFor("S02", "B3")), "S02 B3 missing complete individual final answer");
assert.ok(/不看归纳|谁应为伤害负责/.test(builder.visibleTextFor("S03", "B3")), "S03 B3 missing individual cause answer");
assert.ok(/《氓》为它新添了什么/.test(builder.visibleTextFor("S04", "B4")), "S04 B4 missing opening return");
assert.ok(!/第一部诗歌总集|305篇/.test(builder.visibleTextFor("S05A", "B0")), "S05A B0 leaks culture answers");
assert.ok(/第一部诗歌总集|305篇/.test(builder.visibleTextFor("S05A", "B1")), "S05A B1 missing culture answers");
assert.ok(!/第一部诗歌总集|305篇/.test(builder.visibleTextFor("S05A", "B2")), "S05A B2 fails to withdraw answers");

for (const stateId of ["B1", "B2", "B3"]) {
  const visible = builder.visibleTextFor("O05", stateId);
  assert.ok(/她自己说｜第[一二三]章/.test(visible), `O05 ${stateId} missing readable chapter heading`);
  assert.ok(!/第一至第三章/.test(visible), `O05 ${stateId} still compresses three chapters`);
}
for (const stateId of ["B4", "B5", "B6"]) {
  const visible = builder.visibleTextFor("O06", stateId);
  assert.ok(/她自己说｜第[四五六]章/.test(visible), `O06 ${stateId} missing readable chapter heading`);
  assert.ok(!/第四至第六章/.test(visible), `O06 ${stateId} still compresses three chapters`);
}

for (const item of builder.physicalPlan) {
  const visible = builder.visibleTextFor(item.page.page_id, item.state.state_id);
  assert.ok(!/\bB[0-9]\b|\bO0[1-9]\b|\bC[0-9]{3}\b|\bS0[1-9]\b/.test(visible), `${item.page.page_id}-${item.state.state_id} leaks backend id`);
}

console.log(`MENG_V66_PPTX_BUILD_CONTRACT_OK physical=${lesson.target_pages}`);
