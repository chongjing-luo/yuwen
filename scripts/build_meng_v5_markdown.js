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
    "version: \"5.3-literary-participation\"",
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
    `本母版以六章原文为唯一课堂主线，完整覆盖30组诗句，按12个意义句群组织，天然时长${totalMinutes}分钟。它不是固定两课时教案，而是可在章末和综合活动结束处安全拆分的完整教学内容。`,
    "",
    "学生先完整听读全文，再逐章完成“章读—逐句释义—叙事推进—关键语言—短活动—完整重读—连续章意”；全文读懂后才集中回答三问。活动服务诗句，不另起平行主题。",
    "",
    "未真实试教前，本文件只证明设计覆盖和桌面可实施条件，不声称学生已经理解、喜欢、享受或完成迁移。",
    "",
    "## 二、三个待解问题",
    "",
    ...THREE_QUESTIONS.map((question, index) => `${index + 1}. ${question}`),
    "",
    "三问依次面对故事、生活和判断：第一问由学生讲出人物经历，第二问让诗句重新长成生活镜头，第三问分开‘谁造成伤害’与‘她说出停止判断后会面对哪些阻力’。教师后台仍守住事实、合理推断和不能证明的边界，但不把研究术语投到学生面前。",
    "",
    "## 三、学习结果与可观察证据",
    "",
    "| 学习结果 | 可观察证据 |",
    "|---|---|",
    "| 准确理解全文 | 30组诗句逐句口译、每章连续章意、三次完整听读/朗读 |",
    "| 从语言形式解释人物处境 | 约10处“原词—形式—处境”短答或朗读方案 |",
    "| 梳理叙事与人物认识 | 六组接力讲述、每人一条转折判断、初读—再读修订 |",
    "| 让古诗进入现实生活 | 一段生活镜头、听众的原诗追问、每人一条‘不只是……更是……’总结 |",
    "| 辨明责任与停止后的现实阻力 | 每人一条责任判断、一次组际质询、四组人物处境解释 |",
    "| 形成自己的婚姻认识 | 每人一句有原诗依据的提醒、一次同伴反馈和班级共同收束 |",
    "| 收纳可迁移的语文知识 | 故事人物、字词诗经、意象写法、三问方法四组检索 |",
    "",
    "## 四、学生接收硬门",
    "",
    "每个课堂节点必须检查：学生接收到了什么信息、参加了什么活动、可能怎样思考、形成了什么收获。教师讲过或屏幕出现过，不自动等于学生已经理解；学生完成空格也不自动等于真正参与。",
    "",
    "每章固定完成“整章在场 → 逐句释义与行动 → 关键语言 → 学生产出 → 完整重读与连续章意”；全文后的三项活动固定完成“个人生成 → 小组共作 → 公开表达 → 听众追问 → 原诗核验 → 可见修订”。学生前台文字贴近人物、生活、声音和诗句，学生角色与研发语言只进入后台审计。",
    "",
    "## 五、教材与解释边界",
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
    "## 六、五个内容模块与安全停点",
    "",
    "| 模块 | 内容 | 时长 | 母版页码 | 安全停点 |",
    "|---|---|---:|---|---|",
  ];
  modules.forEach((module) => {
    const pages = modulePages(module.id);
    lines.push(`| 模块${module.number}·${module.title} | ${module.id === "M1" ? "导入、三问、首读、支架、第一章" : module.id === "M2" ? "第二、三章" : module.id === "M3" ? "第四、五章" : module.id === "M4" ? "第六章、全文重读、接力讲述与生活镜头" : "责任质询、停止后的现实阻力、婚姻圆桌、知识收纳与退出"} | ${module.minutes}分钟 | P${pages[0].page}—P${pages.at(-1).page} | ${module.safeStop} |`);
  });
  lines.push("");
  lines.push("## 七、12个意义句群");
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
  lines.push("## 八、30组诗句逐句覆盖表");
  lines.push("");
  lines.push("| 章 | 原句 | 基本释义 | 关键字词 | 行动与声音 | 语言形式 | 三问证据 |", "|---|---|---|---|---|---|---|");
  lineGroups.forEach((line) => {
    lines.push(`| ${line.chapterNumber} | ${cell(line.original)} | ${cell(line.translation)} | ${cell(line.keywords)} | ${cell(`${line.action} ${line.voice}`)} | ${cell(line.form)} | ${cell(line.q)} |`);
  });
  lines.push("");
  lines.push("## 九、逐章教学总谱");
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
  lines.push("## 十、第一章双重观看");
  lines.push("");
  lines.push("第一次阅读只问“这些行动给你什么印象”，允许憨厚、主动、热烈、执着等初始理解；不显示警告信号、伪装、恋爱脑或信息遮蔽。全文读完后才回看：");
  lines.push("");
  lines.push("| 层次 | 内容 |", "|---|---|");
  lines.push("| 文本事实 | 表面来意为贸丝，真实来意为谋婚；“蚩蚩”是忠厚的外在印象；女子说“将子无怒” |");
  lines.push("| 合理推断 | 可能存在初期印象管理；婚前印象与婚后行为形成反差 | ");
  lines.push("| 文本不能证明 | 有计划地伪装完整人格；女子长期不知真实意图；“无怒”已达到婚前暴力 | ");
  lines.push("| 现代工具 | 确认偏向、浪漫化解释；不是心理诊断、不是女性专属，也不是粗暴原因 | ");
  lines.push("");
  lines.push("## 十一、全文后的三项综合活动");
  lines.push("");
  lines.push("### 活动一　把她的一生讲出来");
  lines.push("");
  lines.push("全班组成六个任务组，每组认领一章。每名学生先独立写一句本章经历，组内再合成不超过三十秒的三句讲述：她经历了什么、她的心境或认识怎样变化、哪一句诗托住这段话。六组依次接力，听众记录一处最清楚的转折和一处尚未说清的空缺；每两章允许一次追问。");
  lines.push("");
  lines.push("接力以后，每名学生独立判断哪一步让她的生活明显转向，并用“转折—诗句—影响”说清理由。课堂可以保留不同转折判断，但个人最终叙述必须从“送子涉淇”走到“亦已焉哉”。");
  lines.push("");
  lines.push("### 活动二　让诗句重新长成日子");
  lines.push("");
  lines.push("各组选择一个生活时刻：天还没亮、终于停下劳作、丈夫态度已经改变、兄弟的讥笑响起或她独自静下来。学生不用诗中的话，采用旁白、定格或双人讲述还原四十秒以内的生活镜头；呈现后，听众必须指出哪句诗托住这一幕、哪一处只是合理想象。最后每名学生完成“她的不幸，不只是……更是……”。");
  lines.push("");
  lines.push("### 活动三　把谁造成伤害和她还会遇到什么分开说清");
  lines.push("");
  lines.push(`学生先从“${causalLines.responsibility.join("、")}”中选择最有力的一处，完成“我认为他应为……负责，诗中的依据是……”。另一组只追问：你说的是诗中明写的行为，还是补写的动机？`);
  lines.push("");
  lines.push("随后四组分别回答：最初有哪些事情还看不清；她已经交付了什么；受伤时谁真正接住她；在那个时代女子离开容易吗。每组先找诗，再用自己的话解释；听众负责补诗、质疑说得太满之处或连接不同回答。");
  lines.push("");
  lines.push("> 她的迁嫁、劳作、孤立与时代处境，可以说明她说出“亦已焉哉”以后可能面对的阻力；却不能制造、减轻或合理化他的失信与粗暴。 ");
  lines.push("");
  lines.push("## 十二、婚姻圆桌：把一句提醒留给后来人");
  lines.push("");
  lines.push("讨论题：如果把《氓》说给后来人听，一段值得珍惜的婚姻，最不能缺少什么？只讨论作品或第三人称案例，不要求学生公开私人经历。每名学生先发言一次，再写一句有原诗依据的提醒；同桌指出其中最有力量的词和仍可更具体之处，修改后向全班分享。 ");
  lines.push("");
  lines.push("教师最后才显示一段可以现场增删的收束文字。它必须保留学生原话和有证据的分歧，不能作为活动前的标准答案，也不要求学生逐字抄写。 ");
  lines.push("");
  lines.push("## 十三、最终知识收纳");
  lines.push("");
  lines.push("1. 故事与人物：六章叙事、关系过程、认识变化和责任判断。 ");
  lines.push("2. 字词与《诗经》：风雅颂、四言、赋比兴及本课重点古义和读音。 ");
  lines.push("3. 意象与写法：桑叶、淇水、赋比兴、对照、反复、叠词、呼告、时间压缩、时间回环、第一人称回望。 ");
  lines.push("4. 三问与方法：讲出她怎样走到结尾；让诗句长成具体生活；分开谁造成伤害与她说出停止后会面对什么；准确释义—追踪行动—听见声音—观察写法—用证据判断—联系真实生活。 ");
  lines.push("");
  lines.push("## 十四、形成性评价与课堂安全");
  lines.push("");
  lines.push("- 事实错误、字音和关键古义直接纠正；情绪不同不纠正，只追问诗句来源。 ");
  lines.push("- 开放回答按“有原句—推理连续—边界克制”评价。 ");
  lines.push("- 第五章及婚姻圆桌默认允许匿名书写、不公开分享和第三人称回应。 ");
  lines.push("- 三问活动按“个人生成、小组共作、公开表达、听众任务、同伴追问、原诗核验、可见修订”评价；只完成空格不视为充分参与。 ");
  lines.push("- 学生前台文字执行课堂朗读测试，不以项目式术语和重复核对模板代替语文表达。 ");
  lines.push("- 每个模块结束记录学生实际作品、负担和意外回应；未实施前不填“学生已经学会”。 ");
  lines.push("");
  lines.push("## 十五、PPT与逐字稿索引");
  lines.push("");
  lines.push(`完整母版共${slides.length}页；每页讲者备注均含承接、教师原话、学生动作与等待、必要回应分支、可观察证据和明确切页句。详见《04A_氓_V5逐页无生试讲稿.md》和《07_氓_V5母版与模块页码映射.md》。`);
  return lines.join("\n");
}

function worksheetMarkdown() {
  const lines = [
    "---",
    "document_type: student_worksheet",
    "lesson: \"《氓》\"",
    "version: \"5.3-literary-participation\"",
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
    "她经历了什么　她的日子苦在哪里　这场婚姻为什么走到这一步",
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
    "> 记录原则：每组诗句都要能口译，但不要求每格都写满。关键句、个人停顿句和活动证据必须落笔；其余诗句可只在教材旁标注关键词，避免把课堂变成连续填表。",
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
    lines.push("把这一章暂时放回三个问题（没有证据的地方可以留空）：");
    lines.push("");
    lines.push("| 她走到了哪一步 | 这一章让你看见怎样的日子 | 谁做了什么／她还要面对什么 |", "|---|---|---|", "|  |  |  |");
    lines.push("");
  });
  lines.push("## 五、回到最初的停顿点");
  lines.push("");
  lines.push("我的初读判断：________________　现在：□保留　□修正　□推翻");
  lines.push("");
  lines.push("新增的跨章证据：_______________________________________________");
  lines.push("");
  lines.push("## 六、把她的一生讲出来");
  lines.push("");
  lines.push("我所在的小组认领第____章。每个人先写一句，再合成三句讲述：");
  lines.push("");
  lines.push("她经历了什么：________________________________________________");
  lines.push("");
  lines.push("她的心境或认识怎样变化：______________________________________");
  lines.push("");
  lines.push("最能托住这段讲述的原诗：______________________________________");
  lines.push("");
  lines.push("我是故事守门人：最清楚的转折是______________________________");
  lines.push("");
  lines.push("还没有说清的空缺是____________________________________________");
  lines.push("");
  lines.push("我认为最重要的转折是________，因为诗中写道________；从这里以后________________________________________________________。");
  lines.push("");
  lines.push("## 七、让诗句重新长成日子");
  lines.push("");
  lines.push("我选择的生活时刻：____________________________________________");
  lines.push("");
  lines.push("这一幕里，她正在做什么：______________________________________");
  lines.push("");
  lines.push("我们准备用：□第三人称旁白　□定格　□双人讲述　□其他________（可以不表演）");
  lines.push("");
  lines.push("托住这一幕的原诗：____________________________________________");
  lines.push("");
  lines.push("呈现以后，听众指出：");
  lines.push("");
  lines.push("哪一句诗使它站得住：__________________________________________");
  lines.push("");
  lines.push("哪一处只是合理想象，不能当成诗中明写：______________________");
  lines.push("");
  lines.push("她的不幸，不只是________________，更是________________________。");
  lines.push("");
  lines.push("## 八、先把责任说清，再看她要面对哪些阻力");
  lines.push("");
  lines.push("我认为他应为____________________________负责。");
  lines.push("");
  lines.push("诗中的依据是__________________________________________________");
  lines.push("");
  lines.push("另一组的追问：你说的是诗中明写的行为，还是补写的动机？");
  lines.push("");
  lines.push("我的回答或修改：________________________________________________");
  lines.push("");
  lines.push("四个问题中，我们小组负责第____问；找到的原诗是______________");
  lines.push("");
  lines.push("我们的解释：____________________________________________________");
  lines.push("");
  lines.push("> 她的迁嫁、劳作、孤立与时代处境，可以说明她说出“亦已焉哉”以后可能面对的阻力；却不能制造、减轻或合理化他的失信与粗暴。 ");
  lines.push("");
  lines.push("## 九、回到最初的热烈");
  lines.push("");
  lines.push("| 细节 | 第一次看见什么 | 读到结局以后怎样重看 | 这句话能不能说满 |", "|---|---|---|---|", "| 蚩蚩 |  |  |  |", "| 贸丝／谋 |  |  |  |", "| 匪我愆期 |  |  |  |", "| 将子无怒 |  |  |  |");
  lines.push("");
  lines.push("如果使用“恋爱脑、初期伪装”等词，请把它换成更准确、能由诗句托住的表达：");
  lines.push("");
  lines.push("________________________________________________________________");
  lines.push("");
  lines.push("## 十、如果把《氓》说给后来人听");
  lines.push("");
  lines.push("一段值得珍惜的婚姻，最不能缺少什么？诗中哪一处使你这样想？");
  lines.push("");
  lines.push("________________________________________________________________");
  lines.push("");
  lines.push("### 把一句提醒留给后来人");
  lines.push("");
  lines.push("我留给后来人的一句提醒：");
  lines.push("");
  lines.push("________________________________________________________________");
  lines.push("");
  lines.push("同桌认为最有力量的词：________　还可以更具体之处：__________");
  lines.push("");
  lines.push("我的最终修改：________________________________________________");
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
    "version: \"5.3-literary-participation\"",
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

function studentAction(slide) {
  if (slide.kind === "teacher_index") return "本页隐藏，学生不接收";
  if (slide.kind === "line") return "朗读原句，借注释口译，指出人物动作，并把它接入本章行动链";
  if (slide.kind === "key") return "重读关键句，圈出形成对照、反复、语气或意象的原词，写一条‘形式—处境’解释";
  if (slide.kind === "activity") return slide.phase === "return" ? "先核对自己的产出，再用另一颜色修改一处" : "独立产出，和同伴交换证据，再保存自己的版本";
  if (slide.kind === "full_read") return "不中断跟读或朗读，轻点使自己停住的诗句，暂不急于解释";
  if (slide.kind === "chapter_text") return slide.phase === "end" ? "完整重读本章，闭书口述本章行动怎样连接" : "先整章朗读，标记动作与声音变化";
  if (slide.kind === "question" || slide.kind === "question_overview") return slide.phase === "return" ? "翻回初始猜想，补证、修改或保留" : "只写短猜想，允许证据暂时空白";
  if (["story_prepare", "story_script", "story_relay", "story_turning", "story_revise"].includes(slide.kind)) return "先个人写，再共同讲；听众记录转折与空缺、提出追问，最后修改自己的完整讲述";
  if (["scene_choose", "scene_build", "scene_present", "scene_reflect", "scene_revise"].includes(slide.kind)) return "选择生活时刻，小组完成生活镜头；听众指出原诗与合理想象，个人再写处境总结";
  if (["responsibility_choose", "responsibility_challenge", "responsibility_after"].includes(slide.kind)) return "每人先作责任判断，小组公开表达，另一组追问事实与动机并推动修改";
  if (["difficulty_discuss", "difficulty_present", "difficulty_after", "responsibility_boundary"].includes(slide.kind)) return "四组分别解释她说出停止判断后会面对哪些现实阻力，听众补诗、质疑或连接，个人留下不归责受伤者的解释";
  if (["first_heat", "first_heat_after"].includes(slide.kind)) return "把第一章初见与全文后重看并置，讨论哪些可以想到、哪些不能说满";
  if (["marriage_discussion", "marriage_write", "marriage_share", "marriage_after"].includes(slide.kind)) return "圆桌发言、独立写一句提醒、同桌反馈、全班分享，并用学生原话修订班级收束";
  if (slide.family === "knowledge") return slide.phase === "return" ? "对照回收页，为遗漏项补原句" : "先遮住答案独立检索，再与同桌互补";
  if (slide.kind === "exit") return "完成退出条：最终理解词＋跨章依据＋保留问题";
  if (slide.family === "synthesis") return "先找诗句，再完成排序、转述、边界判断或责任区分";
  return "按当前原文、问题或材料形成一个可留下的回应";
}

function personaThought(slide) {
  if (slide.kind === "teacher_index") return "无；本页不进入学生放映路径。";
  if (slide.kind === "cover") return "“‘亦已焉哉’像决绝，但她为什么到这一步，我现在并不知道。”";
  if (slide.kind === "prior") return "“熟悉作品里的尊重、行动和支持，也许能成为读《氓》的参照，但还不能替代原文。”";
  if (slide.kind === "question" || slide.kind === "question_overview") return slide.phase === "return" ? "“我原来的答案有哪些只是标签？现在能补哪句诗？”" : "“三个问题先记住；我现在只能猜，不能当作已经懂了。”";
  if (slide.kind === "full_read") return slide.phase === "opening" ? "“有些字还不懂，但我先听到故事从期待走向怨与停止。”" : "“逐句读过以后，同一句在全文中的位置和声音已经变了。”";
  if (slide.kind === "chapter_text") return `“这一章不是五条散句；我要跟住‘${slide.chapter?.actionChain || "动作变化"}’。”`;
  if (slide.kind === "line") return `“先把‘${slide.original}’译对，再确认${slide.line?.action || "它推进了什么"}。”`;
  if (slide.kind === "key") return `“不能只报手法名；${slide.line?.form || "语言形式"}究竟让我多看见了什么？”`;
  if (slide.kind === "activity") return slide.phase === "return" ? "“屏幕不是标准答案抄写区；我要比较自己的版本到底差在哪里。”" : `“我必须用原句完成‘${slide.title}’，而不是只说痴情、负心或觉醒。”`;
  if (slide.kind === "module_reconnect") return "“先恢复故事停在哪里，再继续；否则新模块会变成另一节无关的课。”";
  if (["story_prepare", "story_script", "story_relay", "story_turning", "story_revise"].includes(slide.kind)) return "“我不能只把八个标签排好；我要把她每一步怎样发生、怎样改变后来讲给别人听，也要回应别人发现的空缺。”";
  if (["scene_choose", "scene_build", "scene_present", "scene_reflect", "scene_revise"].includes(slide.kind)) return "“诗句要变成可以看见的一天，但我不能替诗编出伤害细节；听别人呈现时，我也要找诗和判断想象边界。”";
  if (["responsibility_choose", "responsibility_challenge", "responsibility_after", "difficulty_discuss", "difficulty_present", "difficulty_after", "responsibility_boundary"].includes(slide.kind)) return "“谁选择了失信和粗暴，与她说出停止后会面对什么是两回事；我既要说清责任，也要理解她真实受到的阻力。”";
  if (["first_heat", "first_heat_after"].includes(slide.kind)) return "“读到结局再回头，我会更警醒，但不能把后来知道的一切都说成她当初已经看见。”";
  if (["marriage_discussion", "marriage_write", "marriage_share", "marriage_after"].includes(slide.kind)) return "“我要先形成自己的婚姻观点，听过同伴以后再修改，而不是等屏幕给五条处方。”";
  if (slide.family === "knowledge") return slide.phase === "return" ? "“哪些是我真的从诗里检索出来的，哪些只是刚看到答案？”" : "“我能否不看答案，从原诗重建故事、字词、写法和方法？”";
  if (slide.kind === "exit") return "“我的结论可以不和别人一样，但必须有跨章证据；问题也可以保留。”";
  if (slide.family === "synthesis") return "“先把经历和诗句站稳，再谈现实；责任是谁与为什么难停止不能混成一件事。”";
  return "“这页和上一页是什么关系？我需要留下一条能回到原文的证据。”";
}

function personaGain(slide) {
  if (slide.kind === "teacher_index") return "无；教师后台页。";
  if (slide.kind === "line") return `${slide.line?.translation || "待下一页完成关键句释义"}；并知道：${slide.line?.action || "该句推进叙事"}`;
  if (slide.kind === "key") return `能用原词解释：${slide.line?.form || "形式参与意义"}；判断边界保持为“${slide.line?.q || "不把推断当事实"}”。`;
  if (slide.kind === "chapter_text") return slide.phase === "end" ? `能够连续口述${slide.chapter?.label || "本章"}：${slide.chapter?.summary || "行动与结果相连"}` : `先获得${slide.chapter?.label || "本章"}的完整轮廓，不让逐句学习失去上下文。`;
  if (slide.kind === "activity") return slide.phase === "return" ? "形成一处有依据的修订，知道自己的答案如何变得更准确。" : "形成一份尚未被教师结论覆盖的个人或小组产出。";
  if (slide.kind === "full_read") return slide.phase === "opening" ? "拥有全诗的声音轮廓和个人停顿点；尚不要求准确解释。" : "把逐句解释重新收束为完整作品，并能比较初读与再读。";
  if (slide.kind === "question" || slide.kind === "question_overview") return slide.phase === "return" ? "把同一问题上的初始猜想变为有诗句支撑的回答。" : "获得贯穿六章的阅读方向，同时保留‘目前不知道’。";
  if (["story_prepare", "story_script", "story_relay", "story_turning", "story_revise"].includes(slide.kind)) return "形成一段能从‘送子涉淇’讲到‘亦已焉哉’的个人叙述、一条转折判断和一处由听众追问促成的修订。";
  if (["scene_choose", "scene_build", "scene_present", "scene_reflect", "scene_revise"].includes(slide.kind)) return "形成一段以原诗为根的生活镜头，能分清诗中明写与合理想象，并写出有层次的生活处境句。";
  if (["responsibility_choose", "responsibility_challenge", "responsibility_after", "difficulty_discuss", "difficulty_present", "difficulty_after", "responsibility_boundary"].includes(slide.kind)) return "能用原诗分别回答谁造成伤害、她作出停止判断后会面对哪些现实阻力，不把她的投入或孤立转写成男子伤害的原因。";
  if (["first_heat", "first_heat_after"].includes(slide.kind)) return "能在明写、可想和不能断言之间调整语气，形成有证据也有分寸的警醒。";
  if (["marriage_discussion", "marriage_write", "marriage_share", "marriage_after"].includes(slide.kind)) return "形成一句有原诗根基的婚姻提醒，接受同伴反馈，并参与班级共同收束。";
  if (slide.family === "knowledge") return "通过先检索后核对，把故事、字词、写法和阅读方法收纳为可再次调用的结构。";
  if (slide.kind === "exit") return "留下一个最终解释、至少一处跨章依据和一个仍未解决的问题。";
  if (slide.family === "synthesis") return slide.evidence || "形成一条由学生先生成、再经原诗和同伴追问变得更准确的回答。";
  return slide.learning || "获得一条可回到原文核验的新理解。";
}

function auditMarkdown() {
  const lines = [
    "---",
    "document_type: student_reception_desktop_simulation",
    "lesson: \"《氓》V5全文逐句教学母版\"",
    "version: \"5.3-literary-participation\"",
    `slides: ${slides.length}`,
    "date: \"2026-08-11\"",
    "---",
    "",
    "# 《氓》V5学生接收桌面审计",
    "",
    "## 1. 审计边界",
    "",
    "本文件是桌面模拟，不是真实课堂数据。它检查学生沿课堂时间实际接收到了什么信息、参加了什么活动、可能怎样思考、形成了什么收获，以及哪里仍可能发生认知断点；不能证明真实学生已经产生预期情绪或学习效果。",
    "",
    "## 2. 学生角色：林晓",
    "",
    "林晓是高二普通学习者：借助教材注释能读懂大意，但不熟悉《氓》；会说“比兴、对照、叠词”等术语，却容易先贴“痴情、负心、觉醒”标签再找证据；工作记忆一次大约能稳定保留三至五个新信息点；愿意与同桌交流，但不喜欢被要求公开私人经历。她不是班级平均值，也不是实际学生数据，而是用来压力测试信息连续性的一名具体角色。",
    "",
    "审计采用四个固定问题：**她接收到了什么信息？参加了什么活动？可能怎样思考？形成了什么收获？** 每一项都必须能在学生可见页、教师备注或学生产出中定位。",
    "",
    "## 3. 关键节点全程模拟",
    "",
    "| 页段 | 林晓接收到了什么信息 | 参加了什么活动 | 可能怎样思考 | 形成了什么收获 | 连续性判定 |",
    "|---|---|---|---|---|---|",
    "| P2—P5 进入作品 | 先听见结尾“亦已焉哉”，再从已学关系故事提取尊重、行动、支持等参照 | 留一个初始声音词；选择一篇熟悉作品，写行动或原句 | “她像是在结束关系，但为什么结束还不知道；旧作品只能给我问题，不能替我回答《氓》。” | 保存一个可回看的初始判断和一个旧经验锚点 | 闭合：有入口但没有提前公布主题 |",
    "| P6—P12 三问与首次听读 | 三个贯穿问题；全诗从相识、迁嫁到怨与停止的整体声音 | 写短猜想；不中断听读；抄下一句并写“听见/看见/想问” | “字词还不都懂，但我先感觉故事发生了明显转折；我停在‘女也不爽，士贰其行’。” | 获得全文轮廓、个人停顿点和待验证问题 | 闭合：不懂细节是预期状态，随后进入必要支架 |",
    "| P13—P16 阅读支架 | 《诗经·卫风》、四言节奏、关键字音；故事将从第一次接近开始 | 节奏试读、字音互查、定位第一章起点 | “背景只够我读进去；真正的意思还要在诗句里形成。” | 排除主要字音障碍，知道下一步沿第一章行动推进 | 闭合：支架短而直接服务原文 |",
    "| P17—P27 第一章 | 男子以贸丝接近求婚；女子远送、说明媒妁条件并约定秋期；“贸丝/谋”“无怒”留下模糊细节 | 整章读—逐句口译—关键句圈词—第一次印象活动—整章重读口述 | “他看起来主动热烈；但表面来意和真实来意不同，‘无怒’也值得保存，暂时不能直接判定伪装或暴力。” | 能连续讲清相识议婚过程，并保存而非封死第一印象 | 闭合：行动链把五句重新连回一章 |",
    "| P28—P39 第二章 | 等待由望、不见、泣、见、笑推进，最后进入卜筮和迁嫁 | 恢复上章停点；逐句口译；设计等待的两种速度；完整重读 | “不是抽象的‘痴情’，而是‘不见/既见’让情绪和节奏突然改变。” | 能用动作顺序、对照、叠词和朗读速度解释等待 | 闭合：活动直接回收本章动作链 |",
    "| P40—P50 第三章 | 桑叶丰润、斑鸠勿食、女子勿耽以及男女脱身处境不等 | 先感受“沃若”的色泽和质地；提出两种意象假设；暂不选唯一答案 | “桑叶不一定只等于青春；我要等‘黄而陨’出现后再用前后位置筛选。” | 理解比兴意义由感官、位置和语境共同形成 | 闭合：解释被保存为假设，不被术语替代 |",
    "| P51—P62 第四章 | 桑叶黄落、婚后食贫、淇水浸车帷；“女不爽/士贰行”把责任直接写出 | 恢复前三章；逐句口译；区分经历事实与责任判断；整章口述 | “食贫、渡水是经历；‘不爽/贰’才是叙述者明确辨责。桑叶两种状态现在可以比较了。” | 能区分事实和判断，并用对照解释责任指向 | 闭合：第三章假设在第四章获得筛选材料 |",
    "| P63—P73 第五章 | 多年家务、早起晚睡、男子粗暴、家人不解、女子自悼构成长时段处境 | 把“多年”还原成一天；完成原句—现实转述—未写明三栏；整章重读 | “这不是一天辛苦，而是没有一天不是这样；诗写了粗暴和孤立，却没写具体伤害方式或她是否求助。” | 能把时间压缩、伤害与支持缺失连成处境，同时守住文本空白 | 闭合但有情绪负担：允许匿名和不公开分享 |",
    "| P74—P85 第六章 | 偕老愿望破裂、自然边界、少年欢乐、誓言被违背，最后形成停止判断 | 比较“亦已”的疲惫克制与清醒决绝两种朗读；写经历依据；整章口述 | “结尾不是突然觉醒，而是她把旧誓言与后来行为逐项核验后的判断；诗没有继续写实际离开。” | 能以跨章经历支持两种朗读，并区分判断与后续行动 | 闭合：结尾获得前五章的因果重量 |",
    "| P86—P88 全文再读 | 六章重新以完整声音出现；初读停顿点与当前理解并置 | 不停顿重读；对初始判断作保留、修正或推翻 | “同一句现在不再是孤立情绪；我能说出它前面经历了什么。” | 显示理解变化，而不是只累计知识点 | 闭合：逐句分析重新回到作品整体 |",
    "| P89—P95 回答第一问 | 六章将由六个任务组重新讲成一个人的一生 | 个人先写、小组合成、六组接力；听众记录转折与空缺并追问；每人另写转折判断 | “我不是把八个标签排好，而是在听她怎样一步步走到结尾；同学发现了我漏掉的家人讥笑。” | 完整个人叙述、转折判断和一处同伴促成的修订 | 闭合：台上讲述与台下听众任务同时发生 |",
    "| P96—P101 回答第二问 | ‘夙兴夜寐、至于暴矣、兄弟不知’重新成为具体可见的生活 | 选择时刻，小组完成生活镜头；听众指出原诗和合理想象；个人写‘不只是……更是……’ | “我能看见她的一天，但不能替诗编出具体暴力；听别人讲时，我也要守住原文。” | 一段生活镜头、一项边界判断和一条有层次的处境句 | 闭合：现实理解由生活呈现和听众追问共同形成 |",
    "| P102—P110 回答第三问 | 男子的失信、反复、粗暴与违誓由诗直接指认；她说出停止以后仍会面对迁嫁、多年劳作、支持缺失与时代处境带来的现实阻力 | 每人先作责任判断，另一组质询事实/动机；四组分别解释现实阻力，听众补诗、质疑或连接 | “她还要面对什么，不能替代谁选择伤害；理解阻力不是重新归责。” | 经质询的责任句、现实阻力解释和不归责受伤者的边界 | 闭合：两个问题分开生成、表达和修订 |",
    "| P111—P112 回到最初的热烈 | ‘蚩蚩、贸丝/谋、无怒’可被重看，但后见警醒不能越过证据 | 比较初读与全文后判断；把自己的话放到‘明写/可想/不能说满’并修改语气 | “可以警惕初见形象和婚后行动的反差，但不能断言完整人格有计划伪装，也不能责怪她没有预知后来。” | 一处有证据又有分寸的判断强度修订 | 闭合：‘恋爱脑’若出现被转成理解工具而非归责标签 |",
    "| P113—P116 婚姻圆桌 | 学生要从作品形成自己的婚姻认识，而不是观看教师五条处方 | 个人发言、四人圆桌、独立写句、同桌反馈、全班分享；教师最后依据学生原话收束 | “我的句子会被别人真正听见，也可能因同桌一句反馈而改变。” | 每名学生一句有原诗依据的婚姻提醒和一处修改 | 闭合：教师结论晚于学生表达，且允许现场增删 |",
    "| P117—P124 知识收纳 | 故事人物、字词《诗经》、意象写法、三问方法四组知识 | 每组先遮答检索，再翻页补原句和遗漏项 | “我能否从刚读过的诗重建知识，而不是看到答案才觉得会？” | 把零散知识组织为可检索结构，并留下真正不会的项 | 闭合但有疲劳风险：连续四组检索可按课堂状态删减 |",
    "| P125—P127 最终朗读与退出 | 全诗第三次完整出现；结尾保留最终解释与未决问题 | 完整朗读；写最终理解词、跨章依据和保留问题 | “我的理解从‘觉醒’变成‘核验经历后作出停止判断’，但我仍想问她之后怎样生活。” | 同时带走有证据的解释和开放问题 | 闭合：以原文而不是知识清单结束 |",
    "",
    "## 4. 逐页接收账本",
    "",
    "| 页 | 学生接收到了什么信息 | 参加了什么活动 | 林晓可能怎样思考 | 本页形成的收获 | 可观察证据 |",
    "|---:|---|---|---|---|---|",
  ];
  slides.forEach((slide, index) => {
    lines.push(`| ${index + 1} | ${cell(slide.visible)} | ${cell(studentAction(slide))} | ${cell(personaThought(slide))} | ${cell(personaGain(slide))} | ${cell(slide.evidence || "原词、短答、图示、朗读标记或修订痕迹")} |`);
  });
  lines.push("");
  lines.push("## 5. 关键连续性压力测试");
  lines.push("");
  lines.push("| 风险 | 当前设计控制 |", "|---|---|");
  lines.push("| 逐句拆解重新碎片化 | 30组后台覆盖、12句群前台推进；章首章末完整读；章末连续口述 | ");
  lines.push("| 现代概念压住古诗 | 先释义和行动；全文后先讲述人物和生活，再由教师在后台辨清概念边界 | ");
  lines.push("| 学生活动仍是填框式配合 | 三问均要求个人生成、小组共作、公开表达、听众任务、同伴追问和可见修订 | ");
  lines.push("| 台上学生参与、台下学生等待 | 接力讲述记录转折与空缺；生活镜头判断原诗与合理想象；圆桌分享必须给同伴反馈 | ");
  lines.push("| 第一章被后见答案污染 | 首次只问印象；全文后才讨论哪些细节值得重看、哪些话不能说满 | ");
  lines.push("| 教师预先公布婚姻处方 | 学生先圆桌、独立写句、同桌反馈和全班分享；教师收束最后出现并允许现场改写 | ");
  lines.push("| 章首与章末任务错位 | 章首只整章朗读并标动作/声音，不闭书概括；章末才闭书连续口述章意 | ");
  lines.push("| 第三问遗漏时代条件 | 四组问题包含‘在她所处的时代，女子离开一段婚姻容易吗’，并回到‘士可说/女不可说’ | ");
  lines.push("| 前台语言像研究报告 | 禁止项目式术语；标题和提问通过课堂朗读测试，改用人物、场景、动作和声音 | ");
  lines.push("| 转场把学生带回错误阶段 | 首读、再读、终读使用不同切页句；第六章后转全文重读，模块五重连后转Q3 | ");
  lines.push("| 课堂情绪或私人经历被强迫 | 允许无明显感受、匿名书写、不公开分享、第三人称案例 | ");
  lines.push("");
  lines.push("## 6. 桌面结论");
  lines.push("");
  lines.push("- 谁造成伤害与她说出停止后会面对哪些现实阻力，在数据、页面和逐字稿中分开；后台逻辑清楚，前台不用研究术语。 ");
  lines.push("- 三问在开头和全文后使用相同措辞，学生可比较初始猜想与最终回答。 ");
  lines.push("- 林晓在每一章都先接收整章、再逐句释义、完成一次本章活动，最后重读并口述章意；六章之后才进入接力讲述、生活镜头、责任质询和婚姻圆桌。 ");
  lines.push(`- 当前主要剩余风险不是原文主线缺失，而是${totalMinutes}分钟母版较长、逐句页型重复和P117—P124连续检索可能造成疲劳；实际授课必须使用模块安全停点，并依据真实试教删减重复练习。 `);
  lines.push(`- ${slides.length}页均有连续课堂剧本和可观察证据字段；教师索引页在母版中隐藏，不进入学生正常放映路径。 `);
  lines.push(`- 仍待真实课堂验证：${totalMinutes}分钟自然节奏、学生对逐句页的疲劳度、第五章情绪负担、婚姻圆桌的安全感和实际学习证据质量。 `);
  return lines.join("\n");
}

function mappingMarkdown() {
  const localCounters = { MASTER: 0, ...Object.fromEntries(modules.map((module) => [module.id, 0])) };
  const lines = [
    "---",
    "document_type: master_module_page_mapping",
    "lesson: \"《氓》\"",
    "version: \"5.3-literary-participation\"",
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
