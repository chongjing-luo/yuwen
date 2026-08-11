#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const {
  THREE_QUESTIONS,
  modules,
  chapters,
  meaningUnits,
  lineGroups,
  slides,
  totalMinutes,
  causalLines,
  snapshot,
} = require("./meng_v5_lesson");

const ROOT = path.resolve(__dirname, "..");
const OUT = path.join(ROOT, "work", "备课", "选择性必修下册", "氓");
const FILES = {
  lesson: path.join(OUT, "02_氓_V5全文逐句教学母版.md"),
  worksheet: path.join(OUT, "03_氓_V5学生学习单.md"),
  script: path.join(OUT, "04A_氓_V5逐页无生试讲稿.md"),
  snapshot: path.join(OUT, "06_氓_V5课程数据快照.json"),
  mapping: path.join(OUT, "07_氓_V5母版与模块页码映射.md"),
  audit: path.join(OUT, "08_氓_V5学生接收桌面审计.md"),
};

function write(file, content) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, `${content.trimEnd()}\n`, "utf8");
}

function cell(value) {
  return String(value ?? "").replace(/\|/g, "／").replace(/\n/g, "<br>");
}

function modulePages(moduleId) {
  return slides.map((slide, index) => ({ slide, page: index + 1 })).filter((item) => item.slide.module === moduleId);
}

function chapterPages(chapterId) {
  return slides.map((slide, index) => ({ slide, page: index + 1 })).filter((item) => item.slide.chapter?.id === chapterId);
}

function lessonMarkdown() {
  const lines = [
    "---",
    "document_type: lesson_plan",
    "lesson: \"《氓》\"",
    "version: \"5.0-text-spine\"",
    "status: \"desktop_design_ready_for_generation\"",
    "date: \"2026-08-11\"",
    `natural_minutes: ${totalMinutes}`,
    `slides: ${slides.length}`,
    "---",
    "",
    "# 《氓》V5全文逐句教学母版",
    "",
    "## 一、课型与设计边界",
    "",
    "本母版以六章原文为唯一课堂主线，完整覆盖30组诗句，按12个意义句群组织，天然时长230分钟。它不是固定两课时教案，而是可在章末安全停点拆分的完整教学内容。",
    "",
    "学生先完整听读全文，再逐章完成“章读—逐句释义—叙事推进—关键语言—短活动—完整重读—连续章意”；全文读懂后才集中回答三问。活动服务诗句，不另起平行主题。",
    "",
    "未真实试教前，本文件只证明设计覆盖和桌面可实施条件，不声称学生已经理解、喜欢、享受或完成迁移。",
    "",
    "## 二、三个待解问题",
    "",
    ...THREE_QUESTIONS.map((question, index) => `${index + 1}. ${question}`),
    "",
    "三问边界固定：Q1只收人物行动、关系阶段和认识变化；Q2只收诗中明确呈现的不幸处境及有边界的现代转述；Q3分为责任线与困境线，二者不画相互致因箭头。",
    "",
    "## 三、学习结果与可观察证据",
    "",
    "| 学习结果 | 可观察证据 |",
    "|---|---|",
    "| 准确理解全文 | 30组诗句逐句口译、每章连续章意、三次完整听读/朗读 |",
    "| 从语言形式解释人物处境 | 约10处“原词—形式—处境”短答或朗读方案 |",
    "| 梳理叙事与人物认识 | 八步关系过程、六章回链、初读—再读修订 |",
    "| 把古诗转成现实语言 | “原句证据—现代生活转述—解释边界”三栏 |",
    "| 区分责任与困境 | 责任线、困境线及独立责任边界页 |",
    "| 收纳可迁移的语文知识 | 故事人物、字词诗经、意象写法、三问方法四组检索 |",
    "",
    "## 四、教材与解释边界",
    "",
    "- 教材依据：`Data/textbook_extract/选择性必修下册/01_U1_导语_课1_氓_离骚.pdf`。",
    "- 课标依据：`Data/reference/curriculum/普通高中语文课程标准（2017年版2020年修订）_教育部官方版.pdf`。",
    "- “蚩蚩”先按教材注释理解为忠厚的样子，不直接等同“装老实”。",
    "- “贸丝/谋”能证明表面来意与真实来意有别，不能证明男子有计划地伪装完整人格。",
    "- “将子无怒”能提示女子在安抚男子情绪，不能据此补写婚前暴力程度。",
    "- “至于暴矣”先理解为粗暴，不擅自补写具体伤害方式。",
    "- “亦已焉哉”写出停止判断，是否实际离开及现实退出条件未继续叙述。",
    "- “恋爱脑”不作为人物标签。若学生提出，教师转换为“情感投入下的浪漫化解释/确认偏向”，并说明它不是粗暴原因。",
    "",
    "## 五、五个内容模块与安全停点",
    "",
    "| 模块 | 内容 | 时长 | 母版页码 | 安全停点 |",
    "|---|---|---:|---|---|",
  ];
  modules.forEach((module) => {
    const pages = modulePages(module.id);
    lines.push(`| 模块${module.number}·${module.title} | ${module.id === "M1" ? "导入、三问、首读、支架、第一章" : module.id === "M2" ? "第二、三章" : module.id === "M3" ? "第四、五章" : module.id === "M4" ? "第六章、全文重读、Q1/Q2" : "Q3、关系结构、知识收纳、退出"} | ${module.minutes}分钟 | P${pages[0].page}—P${pages.at(-1).page} | ${module.safeStop} |`);
  });
  lines.push("");
  lines.push("## 六、12个意义句群");
  lines.push("");
  lines.push("30组诗句是后台覆盖清单，课堂不逐格执行七维分析。每章前2组构成句群A，后3组构成句群B；全部句先解决释义和行动，关键句才增加形式、责任或现实讨论。");
  lines.push("");
  lines.push("| 句群 | 章节 | 覆盖 | 功能 |", "|---|---|---|---|");
  meaningUnits.forEach((unit) => {
    const chapter = chapters.find((item) => item.id === unit.chapter);
    const range = unit.lineIds.join("、");
    lines.push(`| ${unit.id} | ${chapter.label} | 第${range}组 | ${unit.lineIds.length === 2 ? "建立本章起点或转折" : "推进结果并形成章意"} |`);
  });
  lines.push("");
  lines.push("## 七、30组诗句逐句覆盖表");
  lines.push("");
  lines.push("| 章 | 原句 | 基本释义 | 关键字词 | 行动与声音 | 语言形式 | 三问证据 |", "|---|---|---|---|---|---|---|");
  lineGroups.forEach((line) => {
    lines.push(`| ${line.chapterNumber} | ${cell(line.original)} | ${cell(line.translation)} | ${cell(line.keywords)} | ${cell(`${line.action} ${line.voice}`)} | ${cell(line.form)} | ${cell(line.q)} |`);
  });
  lines.push("");
  lines.push("## 八、逐章教学总谱");
  lines.push("");
  chapters.forEach((chapter) => {
    const pages = chapterPages(chapter.id);
    lines.push(`### ${chapter.label}　${chapter.title}（P${pages[0].page}—P${pages.at(-1).page}）`);
    lines.push("");
    lines.push(`> ${chapter.text.replace(/\n/g, "<br>")}`);
    lines.push("");
    lines.push(`- 行动链：${chapter.actionChain}`);
    lines.push(`- 连续章意：${chapter.summary}`);
    lines.push(`- 关键句：第${chapter.keyLines.join("、")}组；其余诗句保证释义和行动，不强行增加手法任务。`);
    lines.push(`- 短活动：${chapter.activity.title}`);
    lines.push(`- 活动问题：${chapter.activity.prompt}`);
    lines.push(`- 产出：${chapter.activity.workspace.replace(/\n/g, "；")}`);
    lines.push(`- 讨论后回收：${chapter.activity.returnItems.join("；")}`);
    lines.push("- 章末证据：完整重读本章；不用列表，一口气口述本章行动怎样连接。 ");
    lines.push("");
  });
  lines.push("## 九、第一章双重观看");
  lines.push("");
  lines.push("第一次阅读只问“这些行动给你什么印象”，允许憨厚、主动、热烈、执着等初始理解；不显示警告信号、伪装、恋爱脑或信息遮蔽。全文读完后才回看：");
  lines.push("");
  lines.push("| 层次 | 内容 |", "|---|---|");
  lines.push("| 文本事实 | 表面来意为贸丝，真实来意为谋婚；“蚩蚩”是忠厚的外在印象；女子说“将子无怒” |");
  lines.push("| 合理推断 | 可能存在初期印象管理；婚前印象与婚后行为形成反差 | ");
  lines.push("| 文本不能证明 | 有计划地伪装完整人格；女子长期不知真实意图；“无怒”已达到婚前暴力 | ");
  lines.push("| 现代工具 | 确认偏向、浪漫化解释；不是心理诊断、不是女性专属，也不是粗暴原因 | ");
  lines.push("");
  lines.push("## 十、全文后的三项综合活动");
  lines.push("");
  lines.push("### 活动一　关系与婚姻过程");
  lines.push("");
  lines.push("> 相识议婚 → 等待成婚 → 迁嫁食贫 → 长期劳作 → 失信粗暴 → 家人不解 → 回望核验 → 作出停止判断");
  lines.push("");
  lines.push("每一步必须回链至少一章；第三章劝诫不误写为新的故事事件。 ");
  lines.push("");
  lines.push("### 活动二　原句—现实转述—解释边界");
  lines.push("");
  lines.push("按“表里差异、劳动与伤害、支持与停止”三组完成。现实语言不能直接抄诗句，也不能把“初期伪装、未及时识别”写成无争议事实或受伤者责任。 ");
  lines.push("");
  lines.push("### 活动三　责任线与困境线");
  lines.push("");
  lines.push(`> **责任线**：${causalLines.responsibility.join(" → ")}<br>诗把失信、反复、粗暴和违誓的责任指向男子，但没有解释他为何选择这样做。`);
  lines.push("");
  lines.push(`> **困境线**：${causalLines.difficulty.join(" → ")}<br>这条线只解释停止为何困难，不解释男子为何失信和粗暴。`);
  lines.push("");
  lines.push("> 她为何难以及时停止，与他为何失信、粗暴，是两个不同问题；困境线不能分担责任线中的责任。 ");
  lines.push("");
  lines.push("## 十一、从《氓》反推关系结构");
  lines.push("");
  lines.push("讨论题：一段关系要避免走向失衡，需要哪些可以长期观察和验证的条件？只讨论作品或第三人称案例，不要求学生公开私人经历。 ");
  lines.push("");
  lines.push("课堂共同形成的观察维度：审慎了解、言行一致、权责平衡、相互尊重、可靠支持、清晰安全边界，以及可获得的求助渠道和退出保障。它们是由作品提出、仍需在现实中检验的维度，不是简单处方。 ");
  lines.push("");
  lines.push("## 十二、最终知识收纳");
  lines.push("");
  lines.push("1. 故事与人物：六章叙事、关系过程、认识变化和责任判断。 ");
  lines.push("2. 字词与《诗经》：风雅颂、四言、赋比兴及本课重点古义和读音。 ");
  lines.push("3. 意象与写法：桑叶、淇水、赋比兴、对照、反复、叠词、呼告、时间压缩、时间回环、第一人称回望。 ");
  lines.push("4. 三问与方法：关系过程、现实处境、责任/困境；准确释义—行动叙事—声音情感—形式观察—证据判断—现实转换。 ");
  lines.push("");
  lines.push("## 十三、形成性评价与课堂安全");
  lines.push("");
  lines.push("- 事实错误、字音和关键古义直接纠正；情绪不同不纠正，只追问诗句来源。 ");
  lines.push("- 开放回答按“有原句—推理连续—边界克制”评价。 ");
  lines.push("- 第五章及关系讨论默认允许匿名书写、不公开分享和第三人称回应。 ");
  lines.push("- 每个模块结束记录学生实际作品、负担和意外回应；未实施前不填“学生已经学会”。 ");
  lines.push("");
  lines.push("## 十四、PPT与逐字稿索引");
  lines.push("");
  lines.push(`完整母版共${slides.length}页；每页讲者备注均含承接、教师原话、学生动作与等待、必要回应分支、可观察证据和明确切页句。详见《04A_氓_V5逐页无生试讲稿.md》和《07_氓_V5母版与模块页码映射.md》。`);
  return lines.join("\n");
}

function worksheetMarkdown() {
  const lines = [
    "---",
    "document_type: student_worksheet",
    "lesson: \"《氓》\"",
    "version: \"5.0-text-spine\"",
    "date: \"2026-08-11\"",
    "---",
    "",
    "# 《氓》V5学生学习单",
    "",
    "> 只讨论作品或第三人称案例，不必分享私人经历。你可以匿名书写，也可以保留不公开的问题。",
    "",
    "## 一、从已学作品出发",
    "",
    "我选择：《静女》 / 《小二黑结婚》 / 《玩偶之家（节选）》 / 其他已学作品__________",
    "",
    "这段关系的幸福或困境，取决于什么？请写一处人物行动或原句。",
    "",
    "________________________________________________________________",
    "",
    "## 二、三个问题：初始猜想",
    "",
    "关系过程｜现实处境｜责任与困境",
    "",
    ...THREE_QUESTIONS.flatMap((question, index) => [
      `${index + 1}. ${question}`,
      "",
      "初始猜想：____________________________________________________",
      "",
      "证据暂存：____________________________________________________",
      "",
    ]),
    "## 三、第一次完整听读",
    "",
    "哪一句把你留了下来？",
    "",
    "“____________________________________________________________”",
    "",
    "□我听见　□我看见　□我想问：________________________________",
    "",
    "## 四、六章逐句学习",
    "",
  ];
  chapters.forEach((chapter) => {
    lines.push(`### ${chapter.label}　${chapter.title}`);
    lines.push("");
    lines.push(`> ${chapter.text.replace(/\n/g, "<br>")}`);
    lines.push("");
    lines.push("| 原句证据 | 我的口译/关键词 | 人物行动与声音 |", "|---|---|---|");
    chapter.lines.forEach((line) => lines.push(`| ${cell(line.original)} |  |  |`));
    lines.push("");
    lines.push(`**本章活动：${chapter.activity.title}**`);
    lines.push("");
    lines.push(chapter.activity.prompt);
    lines.push("");
    chapter.activity.workspace.split("\n").forEach((item) => lines.push(`${item}  `));
    lines.push("");
    lines.push("完整重读后，用一口气讲清本章：");
    lines.push("");
    lines.push("________________________________________________________________");
    lines.push("");
    lines.push("三问证据暂存（本章没有证据的栏可留空）：");
    lines.push("");
    lines.push("| Q1 关系过程 | Q2 现实处境 | Q3 责任/困境 |", "|---|---|---|", "|  |  |  |");
    lines.push("");
  });
  lines.push("## 五、回到最初的停顿点");
  lines.push("");
  lines.push("我的初读判断：________________　现在：□保留　□修正　□推翻");
  lines.push("");
  lines.push("新增的跨章证据：_______________________________________________");
  lines.push("");
  lines.push("## 六、活动一：关系与婚姻过程");
  lines.push("");
  lines.push("请排序并为每一步写章次或原句：");
  lines.push("");
  lines.push("____ → ____ → ____ → ____ → ____ → ____ → ____ → ____");
  lines.push("");
  lines.push("## 七、活动二：把不幸翻译成现实生活语言");
  lines.push("");
  lines.push("| 原句证据 | 现代生活转述 | 解释边界：诗中未写明/不可直接等同 |", "|---|---|---|", "|  |  |  |", "|  |  |  |", "|  |  |  |", "|  |  |  |");
  lines.push("");
  lines.push("## 八、活动三：责任线与困境线");
  lines.push("");
  lines.push("### 责任线：诗把什么责任指向男子？");
  lines.push("");
  lines.push("__________ → __________ → __________ → __________");
  lines.push("");
  lines.push("### 困境线：什么使这段关系更难及时停止？");
  lines.push("");
  lines.push("__________ → __________ → __________ → __________");
  lines.push("");
  lines.push("> 责任边界：她为何难以及时停止，与他为何失信、粗暴，是两个不同问题；困境线不能分担责任线中的责任。 ");
  lines.push("");
  lines.push("## 九、回头看第一章");
  lines.push("");
  lines.push("| 细节 | 第一次看 | 全文后重新判断 | 事实/推断/不能证明 |", "|---|---|---|---|", "| 蚩蚩 |  |  |  |", "| 贸丝/谋 |  |  |  |", "| 将子无怒 |  |  |  |");
  lines.push("");
  lines.push("如果使用“恋爱脑、初期伪装”等词，请先把它换成可由诗句证明的表达：");
  lines.push("");
  lines.push("________________________________________________________________");
  lines.push("");
  lines.push("## 十、从《氓》反推关系结构");
  lines.push("");
  lines.push("一段关系要避免走向失衡，需要哪些可以长期观察和验证的条件？");
  lines.push("");
  lines.push("________________________________________________________________");
  lines.push("");
  lines.push("## 十一、四组知识检索");
  lines.push("");
  lines.push("| 故事与人物 | 字词与《诗经》 | 意象与写法 | 三问与阅读方法 |", "|---|---|---|---|", "|  |  |  |  |", "|  |  |  |  |");
  lines.push("");
  lines.push("## 十二、退出条");
  lines.push("");
  lines.push("我现在最愿意用________理解她，因为____________________________。 ");
  lines.push("");
  lines.push("我仍愿意保留的问题是__________________________________________。 ");
  return lines.join("\n");
}

function scriptMarkdown() {
  const lines = [
    "---",
    "document_type: page_by_page_speaker_script",
    "lesson: \"《氓》\"",
    "version: \"5.0-text-spine\"",
    `slides: ${slides.length}`,
    `natural_minutes: ${totalMinutes}`,
    "date: \"2026-08-11\"",
    "---",
    "",
    "# 《氓》V5逐页无生试讲稿",
    "",
    "本稿与V5完整母版及五个模块课件同源。每页只对应一个学生可见状态；台词中的学生回应均以条件分支书写，不虚构真实课堂已经发生。",
    "",
  ];
  slides.forEach((slide, index) => {
    lines.push(`## P${index + 1}｜${slide.title || slide.original || slide.kind}`);
    lines.push("");
    lines.push(`- 模块：${slide.module}`);
    lines.push(`- 页型：${slide.kind} / ${slide.phase}`);
    lines.push(`- 预计时间：${slide.minutes}分钟`);
    lines.push(`- 学生可见：${cell(slide.visible)}`);
    lines.push("");
    lines.push(slide.notes);
    lines.push("");
  });
  return lines.join("\n");
}

function auditMarkdown() {
  const lines = [
    "---",
    "document_type: student_reception_desktop_simulation",
    "lesson: \"《氓》V5全文逐句教学母版\"",
    "version: \"5.0-text-spine\"",
    `slides: ${slides.length}`,
    "date: \"2026-08-11\"",
    "---",
    "",
    "# 《氓》V5学生接收桌面审计",
    "",
    "## 1. 审计边界",
    "",
    "本文件是桌面模拟，不是真实课堂数据。它只检查每页是否给学生提供看见原文、作出行动、形成思考和留下可观察证据的条件，不能证明学生已经产生预期情绪或学习效果。",
    "",
    "## 2. 逐页接收模拟",
    "",
    "| 页 | 模块 | 学生看见 | 课堂行动 | 可能体验 | 可能思考 | 可能理解/学到 | 可观察证据 |",
    "|---:|---|---|---|---|---|---|---|",
  ];
  slides.forEach((slide, index) => {
    const action = slide.kind === "line" ? "朗读、口译、确认人物行动" : slide.kind === "key" ? "圈原词、解释形式作用" : slide.kind === "activity" ? "独立产出、交流、修订" : slide.kind === "full_read" ? "不中断听读/朗读与个人标记" : slide.family === "knowledge" ? "先检索、后核对" : "按本页问题或材料形成回应";
    lines.push(`| ${index + 1} | ${slide.module} | ${cell(slide.visible)} | ${cell(action)} | ${cell(slide.experience)} | ${cell(slide.thought)} | ${cell(slide.learning)} | ${cell(slide.evidence || "原词、短答、图示、朗读标记或修订痕迹")} |`);
  });
  lines.push("");
  lines.push("## 3. 关键连续性压力测试");
  lines.push("");
  lines.push("| 风险 | 当前设计控制 |", "|---|---|");
  lines.push("| 逐句拆解重新碎片化 | 30组后台覆盖、12句群前台推进；章首章末完整读；章末连续口述 | ");
  lines.push("| 现代概念压住古诗 | 先释义和行动；现代概念集中到全文后；每项带解释边界 | ");
  lines.push("| 责任线与困境线混写 | 两张互不相连的图；禁止“投入→粗暴”箭头；独立责任边界页 | ");
  lines.push("| 第一章被后见答案污染 | 首次只问印象；全文后才做事实/推断/不能证明/现代工具四层回看 | ");
  lines.push("| 课堂情绪或私人经历被强迫 | 允许无明显感受、匿名书写、不公开分享、第三人称案例 | ");
  lines.push("");
  lines.push("## 4. 桌面结论");
  lines.push("");
  lines.push("- 责任线和困境线在数据、页面和逐字稿中分开。 ");
  lines.push("- 三问在开头和全文后使用相同措辞，学生可比较初始猜想与最终回答。 ");
  lines.push("- 117页均有连续课堂剧本和可观察证据字段。 ");
  lines.push("- 仍待真实课堂验证：230分钟自然节奏、学生对逐句页的疲劳度、第五章情绪负担、关系讨论的安全感和实际学习证据质量。 ");
  return lines.join("\n");
}

function mappingMarkdown() {
  const localCounters = Object.fromEntries(modules.map((module) => [module.id, 0]));
  const lines = [
    "---",
    "document_type: master_module_page_mapping",
    "lesson: \"《氓》\"",
    "version: \"5.0-text-spine\"",
    `master_slides: ${slides.length}`,
    "date: \"2026-08-11\"",
    "---",
    "",
    "# 《氓》V5母版与模块页码映射",
    "",
    "五个模块课件从同一页面数组筛选生成，不单独改写。母版页码用于全局索引，模块页码用于实际课堂。",
    "",
    "| 母版页 | 模块 | 模块页 | 标题 | 页型 | 分钟 |",
    "|---:|---|---:|---|---|---:|",
  ];
  slides.forEach((slide, index) => {
    localCounters[slide.module] += 1;
    lines.push(`| ${index + 1} | ${slide.module} | ${localCounters[slide.module]} | ${cell(slide.title || slide.original)} | ${slide.kind} | ${slide.minutes} |`);
  });
  return lines.join("\n");
}

function main() {
  write(FILES.lesson, lessonMarkdown());
  write(FILES.worksheet, worksheetMarkdown());
  write(FILES.script, scriptMarkdown());
  write(FILES.audit, auditMarkdown());
  write(FILES.mapping, mappingMarkdown());
  write(FILES.snapshot, JSON.stringify(snapshot(), null, 2));
  Object.values(FILES).forEach((file) => console.log(`${path.relative(ROOT, file)}\t${fs.statSync(file).size} bytes`));
  console.log(`slides=${slides.length}\tminutes=${totalMinutes}\tlines=${lineGroups.length}\tmeaning_units=${meaningUnits.length}`);
}

main();
