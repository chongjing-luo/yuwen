"use strict";

const fs = require("fs");
const path = require("path");

const PROJECT_ROOT = path.resolve(__dirname, "..");
const OUTPUT = path.join(
  PROJECT_ROOT,
  "work",
  "备课",
  "选择性必修下册",
  "氓",
  "_v62_stage",
  "14_氓_V64_48页逐页放行总账.md",
);

const MODULES = [
  ["opening", "导入"],
  ["chapter_1", "第一章"],
  ["chapter_2", "第二章"],
  ["chapter_3", "第三章"],
  ["chapter_4", "第四章"],
  ["chapter_5", "第五章"],
  ["chapter_6", "第六章"],
  ["synthesis", "全文综合"],
];

const METHOD_LABELS = {
  O01: "静默检索＋目录恢复",
  O02: "同桌互说＋四人轮说＋公共增量",
  O03: "教师引用现场原话后置归纳",
  O04: "揭题停顿＋正音定位",
  O05: "连续听读（前三章）",
  O06: "连续听读（后三章）＋末句静默",
  O07: "停顿句保存＋同桌差异补记",
  O08: "真实初听引用＋三问书签",
  O09: "最小文化路标＋关系复述",
  C101: "整章朗读＋行动主体追踪",
  C102: "自然口译＋转折字比较",
  C103: "路线描画＋空间叙述",
  C104: "完整对话口译＋语气听辨",
  C105: "撤答旁白＋故事轨道",
  C201: "整章朗读＋视线定位",
  C202: "正面对照＋闭眼听辨＋按需改读",
  C204: "最小文化支架＋对称拆句",
  C206: "熄屏旁白＋故事轨道",
  C301: "整章朗读＋换声察觉",
  C302: "感官观察＋双假设",
  C303: "同节拍对读＋蒙句反事实听辨",
  C305: "同词异境比较＋边界判断",
  C306: "撤答旁白＋故事轨道",
  C401: "整章朗读＋开放定位",
  C402: "前后物象对照＋旧假设真修订",
  C403: "时间声场＋双镜头旁白",
  C404: "原词证据席＋责任句修订",
  C405: "替换实验＋声音损失比较",
  C406: "撤答旁白＋故事轨道",
  C501: "整章朗读＋生活声场定位",
  C502: "早晚走位＋反复听辨",
  C503: "跨章回看＋证据强度分级",
  C504: "外声—停顿—独白声场",
  C505: "撤答生活旁白＋故事轨道",
  C601: "整章朗读＋开放回望定位",
  C602: "同词铰链接读＋单点改读",
  C603: "双解释竞争＋证据席",
  C604: "旧日相册＋今日核验",
  C605: "回环词检索＋双声盲听",
  C606: "撤答旁白＋六章母轨道",
  S01: "个人六章人生＋真实断点核查",
  S02: "日常片刻＋同伴反向配诗",
  S03: "四层原因句＋双边界核查",
  S04: "真实主题谱回看＋共同生活互证",
  S05: "合书检索＋原句修复",
  S06: "三组原句任选＋迁移检验",
  S07: "个人语文知识书页＋定位核查",
  S08: "三问退出＋可选问题＋完整朗读",
};

const CLOSED_ISSUES = {
  C105: "删除无人读取的全文回看标记，只保留故事轨道第一格；固定三处婚前细节改由C503真实回看。",
  C303: "吸收旧C304蒙句听辨，旧页删除；反事实体验只在本页服务‘呼告怎样由物抵达人’。",
  C504: "学习单删除‘三秒沉默里’舞台指令，改为‘外面的笑声停下以后’；停顿只在真实剧本发生。",
  C601: "五句恢复等量同色，收束句由学生定位，不再以红色泄答。",
  C602: "删除卡片边界上的悬空‘老’字，铰链只由接读和原词位置形成。",
  C603: "首屏改为开放双解释，不预写‘反衬的没有边’。",
  C606: "恢复六张真实章末卡，写明跨课时材料袋保存、返还与缺卡便笺替代。",
  S01: "取消强制断点；没有断点者写一处清楚因果。",
  S02: "取消强制改写；可配回者明确写‘无需改’。",
  S03: "区分婚前警惕、直接责任、停止困难与不能断言，不把退出阻力平均分责。",
  S04: "真实回投O03主题谱，取消强制分歧和鱼缸程序。",
  S05: "撤去首屏文化常识答案，恢复先合书检索、后核对的真实时序。",
  S06: "前台明确三组原句任选一组，任务范围与学习包一致。",
  S07: "新增个人知识书页，真实消费S05错空项与S06修订短卡。",
  S08: "新增独立退出页，收束三问、关系提醒、可选问题和完整朗读。",
};

function compact(value) {
  return String(value || "")
    .replace(/\|/g, "／")
    .replace(/\s+/g, " ")
    .trim();
}

function firstUse(value) {
  const text = compact(value);
  const match = text.match(/^(.*?)(?:；|。)/u);
  return match ? match[1] : text;
}

function inputFromPrevious(previous) {
  return previous ? `${previous.page_id}留下：${compact(previous.artifact)}` : "学生既有的小学至高中爱情、婚姻文学经验";
}

function firstPerson(page) {
  if (page.first_person_reception) return compact(page.first_person_reception);
  return `我面对“${compact(page.literary_object)}”，实际完成“${compact(page.student_action.join("；"))}”，留下“${compact(page.artifact)}”。`;
}

function normalPath(page) {
  return compact(page.normal_path || page.normal_counterexample || "答案已准确、暂时空白、没有分歧或不愿公开时均可如实保留，不制造错误或争议。");
}

function mergeCounterevidence(page) {
  return compact(page.merge_test || `本页独立改变“${page.current_difficulty}”；相邻页不能同时生成并真实消费本页作品。`);
}

function currentDecision(page) {
  const fix = CLOSED_ISSUES[page.page_id];
  return fix
    ? `候选保留，历史问题已局部关闭：${fix} 仍须在同一V6.4完整母版上通过两路独立审查。`
    : "候选保留；存在意义与产物后用已写明，但未获完整母版两路独立放行前，不得标记PASS。";
}

const loaded = MODULES.map(([file, label]) => {
  const data = require(path.join(PROJECT_ROOT, "scripts", "meng_v62", "content", file));
  return { file, label, data };
});
const allPages = loaded.flatMap(({ data }) => data.pages);
const ids = allPages.map((page) => page.page_id);

if (allPages.length !== 48) throw new Error(`Expected 48 pages, got ${allPages.length}`);
if (new Set(ids).size !== 48) throw new Error("Page IDs must be unique");
if (ids.includes("C304")) throw new Error("C304 must be merged into C303 in V6.4");
if (!ids.includes("S08")) throw new Error("S08 must exist in V6.4");

const lines = [
  "---",
  "document_type: meng_page_function_release_ledger",
  "lesson: \"《氓》\"",
  "version: \"6.4-full-48-page-local-release\"",
  "status: \"candidate-not-released\"",
  "date: \"2026-08-14\"",
  "---",
  "",
  "# 《氓》V6.4四十八页逐页放行总账",
  "",
  "## 放行规则",
  "",
  "本账对每页分别证明存在意义。局部失败不能被全课优点抵消；若某页不能同时说明前页输入、当前困难、唯一功能、学生动作、可见产物、第一次后用、正常反例、删除损失、主视觉职责、第一人称接收与相邻不可合并性，该页必须重写、合并、移动或删除。自动测试通过只证明文件合同成立，不等于教学放行。完整PPT、备注、学习材料和本账须锁定同一哈希，原视觉审查者和原学生接收审查者均判P0=P1=P2=0后，才可冻结。",
  "",
  "## 全课理解脊柱",
  "",
  "广泛唤回小学至高中爱情与婚姻文学 → 教师据现场原话后置归纳 → 完整听见《氓》 → 沿六章原文细读与章末重建 → 回答经历、生活表现、婚姻原因 → 回看开课主题并形成共同生活理解 → 检索字词与写法 → 带着理解、问题和完整朗读离开。",
  "",
];

let absoluteIndex = 0;
for (const { label, data } of loaded) {
  lines.push(`## ${label}`, "");
  for (const page of data.pages) {
    const previous = allPages[absoluteIndex - 1];
    const next = allPages[absoluteIndex + 1];
    absoluteIndex += 1;
    lines.push(
      `### ${String(absoluteIndex).padStart(2, "0")}｜${page.page_id}｜${compact(page.title)}`,
      "",
      `- 前页输入：${inputFromPrevious(previous)}`,
      `- 当前困难：${compact(page.current_difficulty)}`,
      `- 唯一功能：${compact(page.unique_function)}`,
      `- 学生主动作：${compact(page.student_action.join("；"))}`,
      `- 可见产物：${compact(page.artifact)}`,
      `- 第一次真实后用：${firstUse(page.next_use)}`,
      `- 正常反例：${normalPath(page)}`,
      `- 删除损失：${compact(page.deletion_loss)}`,
      `- 主视觉职责：${compact(page.visual_duty)}`,
      `- 教学手法：${METHOD_LABELS[page.page_id] || compact(page.interaction_signature?.cognitive_action)}`,
      `- 第一人称接收：${firstPerson(page)}`,
      `- 相邻不可合并：${mergeCounterevidence(page)}`,
      `- 相邻因果：${previous ? previous.page_id : "课程起点"} → ${page.page_id} → ${next ? next.page_id : "课程收束"}`,
      `- 当前裁决：${currentDecision(page)}`,
      "",
    );
  }
}

lines.push(
  "## 尚未放行的门",
  "",
  "1. 当前页级裁决全部只是候选保留，不等于PASS。",
  "2. 必须生成V6.4四十八页完整母版，完成Office结构、Markitdown、PDF、PNG、联系表、前台禁用语和哈希冻结。",
  "3. 必须由原视觉审查者与原学生接收审查者复验修改页、相邻页及所有后用页；任一P0、P1或P2存在即继续返工。",
  "4. 页面双审清零后才进入统一人物圣经与插图阶段；插图加入后重新执行同样的否决审查。",
  "",
);

fs.mkdirSync(path.dirname(OUTPUT), { recursive: true });
fs.writeFileSync(OUTPUT, `${lines.join("\n")}\n`, "utf8");
process.stdout.write(`${OUTPUT}\n`);
