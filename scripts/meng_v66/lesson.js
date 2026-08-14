"use strict";

const v65 = require("../meng_v65/lesson");
const stateScripts = require("./state_scripts_v3");

const old = new Map(v65.pages.map((page) => [page.page_id, page]));

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function scaledBoxes(boxes, seconds) {
  const source = boxes?.length ? boxes : [{ label: "完整课堂过程", seconds }];
  const total = source.reduce((sum, item) => sum + item.seconds, 0) || 1;
  const raw = source.map((item) => item.seconds * seconds / total);
  const values = raw.map(Math.floor);
  let rest = seconds - values.reduce((sum, value) => sum + value, 0);
  const order = raw.map((value, index) => [index, value - values[index]]).sort((a, b) => b[1] - a[1]);
  for (let index = 0; index < rest; index += 1) values[order[index % order.length][0]] += 1;
  return source.map((item, index) => ({ label: item.label, seconds: values[index] }));
}

function script(spoken, minutes, options = {}) {
  return {
    teacher_spoken: spoken,
    scene: options.scene || "屏幕只留下此刻要面对的原诗、问题或学生真实作品；教师说完邀请后退开，让阅读、表达和等待真实发生。",
    stage_directions: options.stage_directions || ["教师承接前页", "学生先独立形成", "同伴限定倾听", "教师据真实材料校准", "学生亲自修订", "自然切页"],
    timeboxes: scaledBoxes(options.timeboxes || [
      { label: "承接与说明", seconds: 45 },
      { label: "学生首答", seconds: 90 },
      { label: "交流与校准", seconds: 105 },
      { label: "修订与转场", seconds: 60 },
    ], minutes * 60),
    branches: options.branches || [
      { kind: "暂时没有答案", response: "允许先圈出最确定的一处原词，用不完整但真实的话开口；没有新增也可如实保留。" },
      { kind: "判断越过原诗", response: "请指出依据；找不到相应原词时，把断言降低为问题、可能或文本未写。" },
    ],
    listener_task: options.listener_task || "听清发言依据的是哪一句诗、给人物故事增加了什么；只补遗漏或提出一处证据追问。",
    evidence_location: options.evidence_location || "教材旁批、个人纸条、学习卡或现场板书",
    cut_line: options.cut_line || "把刚才得到的这一点带回下一句诗，我们继续听她讲。",
  };
}

function contract(base, patch) {
  const page = { ...clone(base || {}), ...patch };
  page.literary_object = patch.literary_object || page.original_text || page.literary_object || page.title;
  page.unique_difficulty = patch.unique_difficulty || `学生容易看见“${page.literary_object}”，却不能把它准确接回人物和前后故事。`;
  page.prior_input = patch.prior_input || `学生已经完成前页任务，手中保留与“${page.literary_object}”有关的原词或初稿。`;
  page.info_state = patch.info_state || "首答前只给原诗、必要字面和一个自然问题；解释、分类、关系与代表答案在学生首稿后出现。";
  page.participation_path = patch.participation_path || "个人先形成；需要交流时并行同桌或四人轮说；全班只公开少量有差异材料。";
  page.teacher_role = patch.teacher_role || "准确释词、引用真实回答、追问原词、后置归纳并守住解释边界。";
  page.wait_contract = patch.wait_contract || "逐字稿内有首答等待、限定反馈和本人修订的明确时间。";
  page.feedback_revision = patch.feedback_revision || "学生依据原词、同伴追问或教师校准，亲自保留、补充、改写或撤回初稿。";
  page.normal_counterexample = patch.normal_counterexample || "想不起、无新增、已经准确、不同意或暂时沉默均有诚实完成路径，不要求伪造改变。";
  page.first_person_reception = patch.first_person_reception || `我刚才面对“${page.literary_object}”，留下了${page.artifact}；我能用原词说清自己新增或修正的理解。`;
  page.story_return = patch.story_return || "页面结束前由一句自然复述回到谁做了什么、人物处境怎样变化以及故事推进到哪里。";
  page.adjacent_counterproof = patch.adjacent_counterproof || `相邻页不同时处理“${page.unique_difficulty}”；合并会挤掉必要首答、校准或故事回接。`;
  page.failure_signals = patch.failure_signals || ["学生只能复述活动手续，不能复述诗意", "首答前已经看见完成关系或答案", "产物在后页没有真实消费者"];
  page.render_mode = patch.render_mode || "poem";
  page.illustration_eligibility = patch.illustration_eligibility || page.illustration_eligibility || "禁止";
  if (page.script?.timeboxes) page.script.timeboxes = scaledBoxes(page.script.timeboxes, page.minutes * 60);
  return page;
}

function from(id, patch) {
  const base = old.get(id);
  if (!base) throw new Error(`missing v65 page ${id}`);
  return contract(base, { ...patch, legacy_refs: patch.legacy_refs || base.legacy_refs });
}

const pages = [
  from("O01", {
    page_id: "O01", title: "我们还记得哪些爱情与婚姻故事？", minutes: 5,
    unique_function: "让每个人从自己的阅读经历中先得到至少一条可说材料，并尽量扩大爱情与婚姻文学的篇目和主题范围。",
    unique_difficulty: "少数快想者容易垄断导入，抽象问题又会使多数学生尚未开口便退出。",
    student_action: ["检索篇名和一句故事", "写它谈到爱情或婚姻中的什么"],
    artifact: "时间封存的个人文学回忆单", next_use: "O02同桌轮说和公共增量", deletion_loss: "多数学生失去独立检索时间，公共发言被快想者占据。",
    visual_duty: "一张真正可以落笔的文学记忆纸", illustration_eligibility: "禁止：图像会预列作品或主题。", render_mode: "memory_sheet",
    frontstage: ["我们还记得哪些爱情与婚姻故事？", "从小学想到高中：课文、小说、整本书……", "篇名", "用一句话唤回故事", "它写到爱情或婚姻中的什么？", "先写你真正记得的一篇；想起新的，再添下去。"],
    script: script("今天先不急着翻到新课。请从小学一直想到高中：语文课文、小说、整本书里，哪些作品写过爱情，哪些写过婚姻？先写篇名，再用一句平常话把故事唤回来；最后写它谈到爱情或婚姻中的什么。这里不需要分析得很深，也没有三篇规定答案。真正记得什么，就先写什么。现在安静两分半。（教师不报篇名，退到后排巡视。）一时想不起，可以翻本班读过的篇目目录；只记得情节，也先留下情节。时间到，我会请大家把纸翻面一瞬，封住这一刻真正想起的内容，然后再与同学说。", 5, {
      timeboxes: [{ label: "说明三个落点", seconds: 45 }, { label: "个人静默检索", seconds: 165 }, { label: "补写和时间封存", seconds: 60 }, { label: "转场", seconds: 30 }],
      stage_directions: ["教师从零篇名开场", "学生独立检索并静写", "教师后排巡视而不报答案", "学生封存个人首答", "切到同伴互说"],
      branches: [
        { kind: "一时想不起作品", response: "允许翻看本班读过的篇目目录；只记得情节，也先留下真实情节。" },
        { kind: "只能想起篇名", response: "先写最确定的一点故事；主题可以暂写‘还说不准’，不借同伴答案补抄。" },
      ],
      evidence_location: "O01文学回忆单；公共作品出现前的时间封存照片或翻面状态",
      listener_task: "此页没有听者任务；每个人先保护自己的文学记忆。",
      cut_line: "每个人手里先有了一点自己的文学记忆。现在说给身边的人听，也听听自己没有想到的故事。",
    }),
    prior_input: "学生尚未看到教师或同伴提供的任何标准篇目。",
    info_state: "公共篇目和教师分类全部未知；首答态只显示三个自然落笔处。",
    participation_path: "全员个人静写；任何公共声音出现前封存个人首答。",
    first_person_reception: "我从自己的阅读经历中想起了作品、故事和一个朴素主题；这些不是老师替我列出的。",
    adjacent_counterproof: "O02负责表达和扩展，不能替代O01不受同伴影响的个人检索。",
    failure_signals: ["大量答案来自邻座刚说的篇名", "主题栏复制教师抽象词", "固定样本有效材料率低于90%"],
  }),
  from("O02", {
    page_id: "O02", title: "一间教室，能想起多少种爱情与婚姻？", minutes: 8,
    unique_function: "分别实现每个人低压开口和全班文学版图的广度，让作品与朴素主题从学生话语中相遇。",
    student_action: ["同桌和四人组内每人说一篇", "公共阶段只贡献一条增量并补记新作品"],
    artifact: "黑板文学长卷和个人新增栏", next_use: "O03教师引用并揭题；S04回投", deletion_loss: "失去全员声音或公共文学广度。",
    visual_duty: "一句自然表达入口；真正主视觉为现场黑板长卷", illustration_eligibility: "禁止：现场学生作品是主视觉。", render_mode: "speak_entry",
    frontstage: ["一间教室，能想起多少种爱情与婚姻？", "我想起《　　　　　》：它写了　　　　　　　　　", "听见一篇自己没有想到的，就把它添进自己的清单。"],
    script: script("先和同桌互相说：‘《什么》写的是怎样的爱情或婚姻故事。’说的人可以看自己的纸，听的人只在没听清时问一句；一分钟后交换。（等待。）现在前后四个人依次说一圈，每个人都说完以前不选代表、不替别人总结。四个人说完，只留下两三条彼此不同的作品或主题。接下来每组只向全班带来一条增量：黑板上没有的篇目，或者同一篇不同的朴素主题。请先说篇名，再说那句自然话。我只把你们真正说出的篇名和关键词写到黑板上，此刻不分类。听见自己没想到的，请添进个人清单。若本组没有新增，可以如实说‘我们先听记’，不制造差异。", 8, {
      timeboxes: [{ label: "同桌互说", seconds: 95 }, { label: "四人依次轮说", seconds: 150 }, { label: "公共增量和板书", seconds: 190 }, { label: "个人补记", seconds: 45 }],
      stage_directions: ["接回个人封存清单", "同桌依次说与听", "四人全员轮说并保留差异", "各组贡献一个公共增量", "个人补记后切页"],
      branches: [
        { kind: "本组没有新增", response: "如实说‘我们先听记’，把别组新篇目补进个人清单，不制造虚假差异。" },
        { kind: "主题说得过深或过空", response: "请先回到一句故事，再用‘它写到……’说一条朴素认识。" },
      ],
      listener_task: "听清篇名、那句故事和朴素主题；只补一篇自己没有想到的作品或一个真实不同的理解。",
      evidence_location: "O01新增栏；黑板篇名＋学生主题长卷",
      cut_line: "先别擦掉这面黑板。我们沿着大家真正说出的故事，去听一位更早的女子怎样讲自己的相识与后来。",
    }),
    prior_input: "每人已有一份公共声音出现前封存的文学回忆单。",
    info_state: "教师不预填篇目和分类；课堂只逐步暴露同伴真实作品。",
    participation_path: "个人材料→同桌并行→四人全员轮说→每组一个公共增量→教师后置记录。",
    first_person_reception: "我完整说过一篇，也从同学那里补到自己没有想到的作品或主题。",
    adjacent_counterproof: "O01只能证明个人检索，O03只负责教师归纳；本页不可由两者代替。",
    failure_signals: ["组长包办", "四人未轮说便形成公共答案", "公共材料少于8部作品或5个主题方向", "教师提前分类"],
  }),
  from("O04", {
    page_id: "O03", legacy_refs: [3, 4], title: "氓", minutes: 3,
    unique_function: "教师用现场文学长卷完成后置归纳，再从众多旧作聚焦到一位先秦女子的声音，完成题名、正音和出处。",
    student_action: ["核对教师是否准确引用本班材料", "读准méng并定位首句"], artifact: "主题谱照片和题名旁注音", next_use: "O04文化定位和O05起读", deletion_loss: "导入成为篇目堆积，揭题与现场发言断裂。",
    visual_duty: "先由黑板长卷主导，再切换为题名和留白", illustration_eligibility: "禁止：人物图会提前规定讲述者和悲剧主题。", render_mode: "title",
    frontstage: ["氓", "méng", "《诗经·卫风》"],
    script: script("请先把目光留在黑板上。（投影熄暗。）我从现场长卷里选三条彼此不同的材料来读：‘《____》写的是____’，‘《____》写的是____’，‘《____》还写到了____’。如果这些不是你们刚才的原话，请立刻纠正我。（停顿，按学生纠正改写。）我们今天想起的爱情与婚姻故事远不止一种，我不拿预先准备的词替它们分类；只把你们真正说出的几条线索圈出来。现在再听一个更早的故事：一位女子从相识讲到婚后的后来。（切题名页，停两秒。）题目只有一个字——氓。这个字在这里读méng，收在《诗经·卫风》里。请在题名旁写下读音，找到第一句‘氓之蚩蚩’。", 3, {
      timeboxes: [{ label: "黑板引用和纠错", seconds: 100 }, { label: "拍照、揭题与正音", seconds: 50 }, { label: "定位首句", seconds: 30 }],
      stage_directions: ["投影熄暗并回看现场长卷", "教师引用三条学生原话", "学生纠正教师事实误记", "切出题名并正音", "全员定位首句"],
      branches: [
        { kind: "教师误记篇名或主题", response: "立即请原发言者纠正，并当场改写黑板，不用教师概括覆盖学生原话。" },
        { kind: "学生把氓读成máng", response: "只校准本篇题名读méng，并请学生在题名旁补音后再定位首句。" },
      ],
      evidence_location: "黑板主题谱照片；教材题名旁注音",
      listener_task: "核对教师是否准确引用本班篇目和主题；随后读准题名并定位首句。",
      cut_line: "先给这首诗一个最小的来处，再让她不被打断地把六章说完。",
    }),
    info_state: "归纳时投影熄暗，不以预制PPT覆盖现场；揭题时只暴露题名、读音和出处。",
    feedback_revision: "学生只纠正教师对现场篇名和主题的事实误记；教师当场改写。",
    first_person_reception: "我看见本班文学回忆被准确保存，也知道新故事叫《氓》、读méng、出自《诗经·卫风》。",
    adjacent_counterproof: "只有本页把导入的真实公共作品接到新文本；独立抽象转场页已经删除。",
  }),
  contract({}, {
    page_id: "O04", legacy_refs: [45, 9], module: "opening", title: "《诗经》：三千年前的声音怎样来到今天", minutes: 3,
    literary_object: "《诗经》最低文化坐标及《氓》的归属", original_text: "",
    unique_function: "在不打断初听的前提下，给学生阅读《氓》所需的最低文化坐标，并只点名后文会亲自遇见的赋、比、兴。",
    unique_difficulty: "没有最低文化坐标，学生会把《氓》当作孤立古诗；背景过多又会压过讲述者的声音。",
    student_action: ["听取必要文化微讲", "在题下注记诗经—卫风—氓的归属"], artifact: "题名旁的归属批注", next_use: "C303B命名兴；S05A合书检索", deletion_loss: "初读失去作品身份，结尾检索变成第一次讲授。",
    visual_duty: "诗经—卫风—氓的简洁归属关系", illustration_eligibility: "禁止：古籍装饰不能增加当前理解。", render_mode: "culture_map",
    frontstage: ["《诗经》", "我国第一部诗歌总集｜305篇", "西周初年至春秋中叶", "风　雅　颂", "《氓》在《卫风》里", "赋、比、兴——先记住名字，后面会真正遇见。"],
    script: script("翻开课文前，只给《氓》一个最小的来处。《诗经》是我国第一部诗歌总集，现存三百零五篇，作品大致产生于西周初年至春秋中叶。传统上分为风、雅、颂；《氓》在十五国风的《卫风》中。古人还用赋、比、兴谈《诗经》的写法。今天此刻只记住这三个名字，不背定义；读到第三章时，我们会亲自听见‘兴’怎样发生。请在题名旁只留下‘诗经—卫风—氓’这条归属，不抄整页。", 3, {
      timeboxes: [{ label: "最低文化坐标微讲", seconds: 115 }, { label: "学生归属批注", seconds: 35 }, { label: "回到讲述者", seconds: 30 }],
      stage_directions: ["题名页后给最低文化坐标", "教师短讲而不展开百科", "学生只做归属批注", "教师巡视真实错项", "立即回到全文初读"],
      branches: [
        { kind: "学生追问为何又称诗三百", response: "说明‘诗三百’是概称，现存篇数按课堂口径记305篇；不在此页展开版本学。" },
        { kind: "已有知识与本页表述不同", response: "先核对教材和本课口径，只修归属事实；其余差异记录为课后追问。" },
      ],
      evidence_location: "教材题名旁的‘诗经—卫风—氓’归属批注",
      listener_task: "听清作品身份和归属；赋、比、兴只记名字，不提前抄定义。",
      cut_line: "来处已经清楚。现在不再介绍，让她从第一句讲到最后一句。",
    }),
    prior_input: "学生已经知道题名、读音和《诗经·卫风》出处，但没有系统文化坐标。",
    info_state: "只揭示最低事实和术语名称；比兴定义及本诗例子保持未知。",
    participation_path: "教师必要微讲；全员完成一个最低成本的归属批注。",
    teacher_role: "准确说明第一部诗歌总集、305篇、大致年代、风雅颂和篇目归属；不展开无关百科。",
    wait_contract: "微讲后留35秒完成批注并巡视真实错项。",
    feedback_revision: "学生只修正归属批注；更完整知识在S05A合书检索后修复。",
    normal_counterexample: "已有相关知识者不额外抄写；有不同教材表述时以本课教材和课程常用表述校准。",
    first_person_reception: "我知道《氓》在《诗经·卫风》中，也知道赋、比、兴要等到原诗里再理解。",
    story_return: "微讲立即结束，回到女子第一人称六章讲述。",
    adjacent_counterproof: "题名页无法同时承担文化坐标；结尾检索不能作为第一次讲授。",
    failure_signals: ["背景微讲超过三分钟", "学生抄百科表格", "提前讲完比兴答案"],
  }),
  from("O05", { page_id: "O05", title: "她自己说｜第一至第三章", minutes: 3, render_mode: "listening", frontstage: ["她自己说｜第一至第三章"],
    prior_input: "学生知道作品来处，但尚未收到人物主题和三问框架。", info_state: "只暴露原诗声音；主题、章意和知识解释保持未知。",
    states: [
      { state_id: "B1", seconds: 65, state_function: "让第一章以可供后排阅读的完整画面进入，朗读不被解释打断。", render_mode: "listening", frontstage: ["她自己说｜第一章", "氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。", "送子涉淇，至于顿丘。匪我愆期，子无良媒。", "将子无怒，秋以为期。"] },
      { state_id: "B2", seconds: 60, state_function: "让第二章以可供后排阅读的完整画面接续，保持女子讲述的声音。", render_mode: "listening", frontstage: ["她自己说｜第二章", "乘彼垝垣，以望复关。不见复关，泣涕涟涟。", "既见复关，载笑载言。尔卜尔筮，体无咎言。", "以尔车来，以我贿迁。"] },
      { state_id: "B3", seconds: 55, state_function: "让第三章的桑叶与劝告完整落下，并无声接入后半首。", render_mode: "listening", frontstage: ["她自己说｜第三章", "桑之未落，其叶沃若。于嗟鸠兮，无食桑葚！", "于嗟女兮，无与士耽！士之耽兮，犹可说也。", "女之耽兮，不可说也！"] },
    ],
  }),
  from("O06", { page_id: "O06", title: "她自己说｜第四至第六章", minutes: 3, render_mode: "listening", frontstage: ["她自己说｜第四至第六章"],
    prior_input: "前三章已经连续响过，朗读不因换页停止。", info_state: "只继续暴露原诗，末句后保持十五秒无解释静默。",
    states: [
      { state_id: "B4", seconds: 50, state_function: "让第四章的多年贫困、渡水与责任判断完整进入。", render_mode: "listening", frontstage: ["她自己说｜第四章", "桑之落矣，其黄而陨。自我徂尔，三岁食贫。", "淇水汤汤，渐车帷裳。女也不爽，士贰其行。", "士也罔极，二三其德。"] },
      { state_id: "B5", seconds: 50, state_function: "让第五章的日复一日、外部笑声与内心悲悼完整进入。", render_mode: "listening", frontstage: ["她自己说｜第五章", "三岁为妇，靡室劳矣。夙兴夜寐，靡有朝矣。", "言既遂矣，至于暴矣。兄弟不知，咥其笑矣。", "静言思之，躬自悼矣。"] },
      { state_id: "B6", seconds: 80, state_function: "让第六章回望旧愿并使末句真正落下，随后守住无解释静默。", render_mode: "listening", frontstage: ["她自己说｜第六章", "及尔偕老，老使我怨。淇则有岸，隰则有泮。", "总角之宴，言笑晏晏。信誓旦旦，不思其反。", "反是不思，亦已焉哉！"] },
    ],
  }),
  from("O07", { page_id: "O07", title: "把第一次听见的《氓》留在纸上", minutes: 4, render_mode: "first_impression",
    frontstage: ["把第一次听见的《氓》留在纸上", "“　　　　　　　　　　　　　　　　　　　　　　　”", "我看见……", "我听见……", "我想问……"],
    normal_counterexample: "暂时没有停点可以写‘尚未找到’，先听同桌后仍可保留，不复制他人句子。",
  }),
  from("O08", { page_id: "O08", title: "读懂六章，我们要回答什么？", minutes: 2, render_mode: "three_questions",
    frontstage: ["读懂六章，我们要回答什么？", "她经历了什么？", "她婚后的不幸，在生活中是什么样子？", "这场婚姻为什么走到这一步？"],
    prior_input: "全诗已经完整听过，个人初见也已保存。", info_state: "三问此刻首次出现；不显示标准答案和原因框架。",
  }),
  from("C101", { page_id: "C101", title: "第一章｜他做了什么？她又做了什么？", render_mode: "chapter_poem",
    frontstage: ["第一章｜他做了什么？她又做了什么？", "氓之蚩蚩，抱布贸丝。", "匪来贸丝，来即我谋。", "送子涉淇，至于顿丘。", "匪我愆期，子无良媒。", "将子无怒，秋以为期。"],
  }),
  from("C102", { page_id: "C102", title: "贸丝，还是来谋？", render_mode: "word_turn",
    unique_function: "从重复的‘贸丝’和‘匪—谋’读出叙事转弯，校准首句易误词，并守住初见证据边界。",
    student_action: ["自然口译并圈出转折字", "把氓、蚩蚩、布、贸、即、谋送回原句"],
    artifact: "叙事转弯句和首句词义旁批", next_use: "C105与C503", deletion_loss: "首句会被压成‘男子来求婚’的结论，叙事转弯、词义异说和证据边界同时丢失。",
    frontstage: ["贸丝，还是来谋？", "氓之蚩蚩，抱布贸丝。", "匪来贸丝，来即我谋。", "第一句让我们看见什么？", "第二句又告诉了我们什么？"],
    info_state: "首答只给两句和两个问题；叙事转弯、来意、人格和预谋判断都不预填。",
    failure_signals: ["屏幕标出‘表面动作／真实来意’答案", "学生看图猜人格", "教师在首答前解释匪—谋关系"],
    states: [
      { state_id: "B0", seconds: 110, state_function: "只面对两句原诗，形成第一句所见与第二句所知的个人首答。", render_mode: "word_turn_b0", frontstage: ["贸丝，还是来谋？", "氓之蚩蚩，抱布贸丝。", "匪来贸丝，来即我谋。", "第一句让我们看见什么？", "第二句又告诉了我们什么？"] },
      { state_id: "B1", seconds: 40, state_function: "观察学生真正圈出的转折处和不同口译。", render_mode: "word_turn_b1", frontstage: ["哪一个字，让话转了方向？", "氓之蚩蚩，抱布贸丝。", "匪来贸丝，来即我谋。", "看一眼黑板上大家圈出的地方。"] },
      { state_id: "B2", seconds: 60, state_function: "准确收束叙事转弯、自然口译和证据边界。", render_mode: "word_turn_b2", frontstage: ["先看见：抱布贸丝", "一个“匪”字，转过话头", "女子告诉我们：不是来换丝，是来谈婚事。", "至于他的为人和后来，此刻还不能断定。"] },
      { state_id: "B3", seconds: 90, state_function: "把首句六个易含混词校准回具体语境，不用一个标签替代整句。", render_mode: "first_line_words", frontstage: ["把第一句说准", "氓｜这里指诗中的男子", "蚩蚩｜忠厚的样子；一说嬉笑的样子", "布｜布匹；一说布币", "贸｜交易、交换", "即｜靠近、到这里来", "谋｜商量婚事", "把六个词送回原句，再完整说一遍。"] },
    ],
  }),
  from("C103", { page_id: "C103", title: "她把他送了多远？", render_mode: "action_path",
    frontstage: ["她把他送了多远？", "送", "涉", "至", "淇水", "顿丘", "沿着三个动词走一遍：她把他送到了哪里？"],
    states: [
      { state_id: "B0", seconds: 105, state_function: "保留完整原句和未经连线的动词，让学生自己生成路径。", render_mode: "action_path_b0", frontstage: ["她把他送了多远？", "送子涉淇，至于顿丘。", "送　　涉　　至", "沿着三个动词，自己画出这段路。"] },
      { state_id: "B1", seconds: 60, state_function: "同桌对照路径，听清动作主体和到达位置。", render_mode: "action_path_b1", frontstage: ["把你画的这段路，指给同桌看。", "送子涉淇，至于顿丘。", "谁在送？经过哪里？到达哪里？"] },
      { state_id: "B2", seconds: 75, state_function: "用原词准确收束女子远送的空间长度。", render_mode: "action_path_b2", frontstage: ["送　→　涉淇　→　至于顿丘", "她送他渡过淇水，一直送到顿丘。", "这份投入，先由三个动作说出来。"] },
    ],
  }),
  from("C104", { page_id: "C104", title: "把这几句当作她说的一番话", render_mode: "speech_poem",
    frontstage: ["把这几句当作她说的一番话", "匪我愆期，子无良媒。", "将子无怒，秋以为期。", "哪里解释，哪里安抚，哪里重新约定？"],
    info_state: "首答只给完整话语和自然问题；三类功能不做成三个已完成色块。",
    states: [
      { state_id: "B0", seconds: 135, state_function: "先把四小句口译成一番连续的话。", render_mode: "speech_b0", frontstage: ["把这几句当作她说的一番话", "匪我愆期，子无良媒。", "将子无怒，秋以为期。", "先把她的话完整说成今天的语言。"] },
      { state_id: "B1", seconds: 70, state_function: "同桌只听一处意思或语气是否清楚。", render_mode: "speech_b1", frontstage: ["再听一遍她的话", "哪里是在解释？", "哪里是在安抚？", "哪里是在重新约定？"] },
      { state_id: "B2", seconds: 95, state_function: "准确收束解释婚期、请其勿怒和另约秋期。", render_mode: "speech_b2", frontstage: ["不是我故意拖延婚期，是你没有请来合适的媒人。", "请你不要生气。", "就把婚期定在秋天吧。", "她没有把婚事推开，而是在解释、安抚、重新约定。"] },
    ],
  }),
  from("C105", { page_id: "C105", title: "他怎样来，她怎样送，两个人怎样约？", render_mode: "story_rebuild",
    frontstage: ["他怎样来，她怎样送，两个人怎样约？", "氓之蚩蚩，抱布贸丝。", "匪来贸丝，来即我谋。", "送子涉淇，至于顿丘。", "匪我愆期，子无良媒。", "将子无怒，秋以为期。"],
  }),
  from("C201", { page_id: "C201", title: "第二章｜她站到哪里？目光投向哪里？", render_mode: "chapter_poem",
    frontstage: ["第二章｜她站到哪里？目光投向哪里？", "乘彼垝垣，以望复关。", "不见复关，泣涕涟涟。", "既见复关，载笑载言。", "尔卜尔筮，体无咎言。", "以尔车来，以我贿迁。"],
  }),
  from("C202", { page_id: "C202", title: "两个“见”字，怎样牵动她的哭与笑？", render_mode: "see_contrast",
    frontstage: ["两个“见”字，怎样牵动她的哭与笑？", "不见复关，泣涕涟涟。", "既见复关，载笑载言。"],
  }),
  from("C204", { page_id: "C204", title: "卜筮以后，婚事怎样走到迁移？", render_mode: "subject_alignment",
    frontstage: ["卜筮以后，婚事怎样走到迁移？", "尔卜尔筮，体无咎言。", "以尔车来，以我贿迁。", "谁来？用什么来？谁迁？带着什么迁？"],
    info_state: "首答只对齐尔／我、车／贿、来／迁；完整因序由学生口译和现场板书后置形成。",
    failure_signals: ["默认画面出现卜筮→无咎→车来→贿迁完成流程", "文化微讲扩展成占卜史", "主体混淆未修订"],
  }),
  from("C206", { page_id: "C206", title: "从“秋以为期”到“以我贿迁”", minutes: 6, render_mode: "chapter_bridge",
    frontstage: ["从“秋以为期”到“以我贿迁”", "将子无怒，秋以为期。", "乘彼垝垣，以望复关。", "以尔车来，以我贿迁。", "前一章的哪件事，使后一章的等待成为必然？"],
    info_state: "不显示来—送—约／等—见—迁完成章意；学生接力后教师才板书。",
    student_action: ["每人先写两章各发生什么", "同桌接力后各自补出章间因果"], artifact: "个人两章自然概括和秋期因果句",
    script: script("先把教材摊开，目光从第一章末的‘秋以为期’移到第二章。每个人先写两小句：第一章发生了什么；第二章发生了什么。不要分工。（等待并巡视。）现在同桌接力，一人先讲第一章，另一人接第二章；交换角色，再讲一次。两个人都讲过两章以后，各自补一句：第一章的哪件事，使第二章的等待成为必然？请两组公开不同连接。教师最后沿原诗板书：他抱布来谋婚，她远送并约定秋期；约定使她登垣等待，由不见到既见，卜筮无咎后车来贿迁。请每个人把这条因果补进自己的两章概括，不抄同桌整句。", 6, {
      timeboxes: [{ label: "个人两章概括", seconds: 90 }, { label: "同桌交换角色接力", seconds: 120 }, { label: "个人章间因果", seconds: 55 }, { label: "公开两组和教师板书", seconds: 65 }, { label: "本人修订", seconds: 30 }],
      evidence_location: "每个人的第一、二章自然概括和秋期因果句",
      cut_line: "故事已经走到迁嫁。第三章却没有立刻写婚后的日子，眼前先出现了一树桑叶。",
    }),
  }),
  from("C301", { page_id: "C301", title: "第三章｜迁嫁以后，诗里忽然出现了什么？", render_mode: "chapter_poem",
    frontstage: ["第三章｜迁嫁以后，诗里忽然出现了什么？", "桑之未落，其叶沃若。", "于嗟鸠兮，无食桑葚！", "于嗟女兮，无与士耽！", "士之耽兮，犹可说也。", "女之耽兮，不可说也！"],
    info_state: "标题不先说故事停驻、比兴和回望；学生从整章发现物象与声音转向。",
  }),
  from("C302", { page_id: "C302", title: "桑之未落，其叶沃若", render_mode: "single_verse",
    frontstage: ["桑之未落，其叶沃若。", "这片桑叶，是什么颜色、光泽和状态？"],
    info_state: "首答无青桑图、无‘生命感’提示；学生从沃若形成感官词后才允许校准。",
  }),
  from("C303", { page_id: "C303A", legacy_refs: [21], title: "这一声劝告，怎样落下？", minutes: 3, render_mode: "single_dark_verse",
    unique_function: "在已经读过第三章以后，有意删去桑叶和斑鸠两句重新听劝女句，感受原诗句群被抽空后的声音损失。",
    student_action: ["有意删去前两句后再听劝女句", "写删句后的声音变化"], artifact: "删句再听记录", next_use: "C303B恢复句群后比较", deletion_loss: "无法把比兴从术语还原为句群有无造成的可感差异。",
    visual_duty: "唯一暴露的劝女原句和大面积暗色留白", frontstage: ["于嗟女兮，无与士耽！", "这一声劝告，怎样落下？"],
    info_state: "物理画面绝不显示桑叶、斑鸠、由物及人、比兴名称或比较答案。",
    script: script("我们刚才已经读过完整的第三章。现在做一次有意的删句再听，不假装自己忘记了前文。请用一张空白纸盖住桑叶和斑鸠两句，屏幕也只留下：‘于嗟女兮，无与士耽！’读一遍，写下：拿掉前两句以后，这声劝告变得怎样？你失去了什么，又多了什么？可以写急、重、近、直，也可以用自己的词，但要说清你听见的差异。（教师退开，等待。）请两位同学只读自己的句子，不判断谁更好。先把这次删句记录留住，下一页恢复原句群，再看声音如何改变。", 3, {
      timeboxes: [{ label: "说明删句实验边界", seconds: 35 }, { label: "删句再听与个人记录", seconds: 75 }, { label: "两份公开", seconds: 45 }, { label: "封存与转场", seconds: 25 }],
      evidence_location: "C303A删句再听记录",
      cut_line: "现在把纸移开，让桑叶和斑鸠重新回来。",
    }),
    first_person_reception: "我明知前文存在，却故意拿掉两句再听，感到了句群被删后的声音变化。",
    adjacent_counterproof: "C303B必须读取这份删句记录；合成一张静态页会污染比较。",
    failure_signals: ["把删句再听冒充未知前文的基线", "教师先说由物及人", "记录未封存便进入校准"],
  }),
  from("C303", { page_id: "C303B", legacy_refs: [21, 23], title: "桑叶、斑鸠和女子重新连起来以后", minutes: 5, render_mode: "object_to_person",
    unique_function: "恢复完整句群，让学生比较删句前后声音增加了什么，再后置命名由物起声、由物及人的兴与比。",
    student_action: ["恢复并连读三句", "比较删句记录并用原词修订"], artifact: "由物及人的比较修订句", next_use: "C305处境对照；S06艺术收纳", deletion_loss: "比兴仍是没有经历的术语。",
    visual_duty: "桑—鸠—女三句的连续声音，不预画完成箭头", frontstage: ["桑叶、斑鸠和女子重新连起来以后", "桑之未落，其叶沃若。", "于嗟鸠兮，无食桑葚！", "于嗟女兮，无与士耽！", "你又多听见了什么？"],
    info_state: "先恢复原句但不显示桑→鸠→女箭头和比兴定义；学生比较后教师命名。",
    script: script("现在移开纸，恢复前两句。请把‘桑之未落’‘于嗟鸠兮’‘于嗟女兮’连起来读。打开刚才的删句记录，在下面续一句：原句回来以后，我又听见了____，因为原诗中的____。（等待。）请两位同学读前后两句，听者只判断他有没有回到原词。现在校准三个字词：‘于嗟’读xū jiē，是感叹词；‘无’同‘毋’，是不要；‘耽’是沉溺。再看声音怎样走：眼前的桑叶引来斑鸠，劝斑鸠的话又把声音送到女子身边。由眼前物象起声、引出所咏，是‘兴’；物与人的处境互相映照，又含着‘比’。这不是一个伪装成首次接收的实验，而是删去与恢复原句以后可以听见的差异。最后再读三句。它也像经历以后的一次回望：婚事已经迁嫁，后来的声音却回来提醒自己和后来的人。", 5, {
      timeboxes: [{ label: "恢复句群和连读", seconds: 50 }, { label: "前后比较和个人修订", seconds: 85 }, { label: "公开两份与原词追问", seconds: 65 }, { label: "释词、命名比兴和重读", seconds: 100 }],
      evidence_location: "C303A首答下方的C303B有依据修订句",
      cut_line: "声音已经由物来到人。接下来，同一个‘耽’落在男女身上，脱身处境却并不相同。",
    }),
    first_person_reception: "我比较了有意删句与恢复原句时的声音差异，再理解比兴怎样从桑、鸠来到女子。",
    adjacent_counterproof: "C303A提供删句后的再听记录，C305讨论男女处境；本页独自承担恢复、比较和命名。",
    failure_signals: ["首屏画出完成箭头", "教师在比较前给比兴定义", "学生只抄术语未修订首答"],
    states: [
      { state_id: "B1", seconds: 185, state_function: "恢复三句但不命名结构，让学生形成有依据修订。", render_mode: "object_to_person_b1", frontstage: ["桑叶、斑鸠和女子重新连起来以后", "桑之未落，其叶沃若。", "于嗟鸠兮，无食桑葚！", "于嗟女兮，无与士耽！", "你又多听见了什么？"] },
      { state_id: "B2", seconds: 115, state_function: "准确命名桑—鸠—女的声音路径及比、兴。", render_mode: "object_to_person_b2", frontstage: ["桑叶在眼前", "劝告先落到斑鸠", "声音又来到女子身边", "由眼前物象起声、引出所咏，是“兴”；物与人的处境互相映照，又含着“比”。"] },
    ],
  }),
  from("C305", { page_id: "C305", title: "同一个“耽”，哪些词改变了脱身处境？", render_mode: "couplet_contrast",
    frontstage: ["同一个“耽”，哪些词改变了脱身处境？", "士之耽兮，犹可说也。", "女之耽兮，不可说也！"],
  }),
  from("C306", { page_id: "C306", legacy_refs: [23], title: "迁嫁以后，为什么先有这一树桑叶？", minutes: 4, render_mode: "chapter_three_close",
    unique_function: "让每个人把第三章的物象、由物及人的劝告、男女处境差异和经历后回望重新讲成一段。",
    student_action: ["每人写第三章自然章意", "合书口述后在断点返诗修订"], artifact: "个人第三章自然章意", next_use: "C401进入桑叶落下；C606六章检索", deletion_loss: "第三章仍是比兴术语和两句性别对照，不能接回故事。",
    visual_duty: "第三章完整原诗和一条开放叙事入口", frontstage: ["迁嫁以后，为什么先有这一树桑叶？", "桑之未落，其叶沃若。", "于嗟鸠兮，无食桑葚！", "于嗟女兮，无与士耽！", "士之耽兮，犹可说也。女之耽兮，不可说也！", "用三四句话，把桑叶、劝告和她的处境连起来。"],
    script: script("请把第三章完整读一遍。现在每个人用三四句自然话写清：迁嫁以后，诗为什么先让桑叶出现；劝告怎样从斑鸠来到女子；同一个‘耽’怎样写出不同的脱身处境；这更像当时旁边人的话，还是经历后的回望。（等待。）合上书，低声把这段讲给自己听。讲到真正断开的地方，立刻打开书找到那一句，再合书补完。请一位同学讲，其他人只指出他漏了哪一步；每个人最后都要在自己的文字上亲自补回。", 4, {
      timeboxes: [{ label: "完整重读", seconds: 35 }, { label: "个人自然章意", seconds: 95 }, { label: "合书低声口述和返诗", seconds: 55 }, { label: "公开一份和个人修订", seconds: 55 }],
      evidence_location: "每个人的第三章自然章意及返诗修订痕迹",
      cut_line: "这份回望还只是警告。第四章，桑叶真正落下，婚后的生活也随之出现。",
    }),
    prior_input: "学生已经体验由物及人的比兴，并读出处境不等。",
    info_state: "不预填完整章意；学生首答后教师只补真实断点。",
    participation_path: "全员个人写→全员低声自述→抽样一份→全员返诗修订。",
    first_person_reception: "我能把比兴和处境差异放回迁嫁后的回望，而不只记一个术语。",
    adjacent_counterproof: "C303B命名写法，C305辨处境；本页独自完成第三章个人重建。",
    failure_signals: ["只有公开一人形成章意", "学生只写‘用了比兴’", "无法从迁嫁接到第四章桑落"],
  }),
  from("C401", { page_id: "C401", title: "第四章｜桑叶落下以后", render_mode: "chapter_poem" }),
  from("C402", { page_id: "C402", title: "沃若｜黄而陨", render_mode: "leaf_revisit" }),
  from("C403", { page_id: "C403", title: "三岁食贫｜淇水汤汤", render_mode: "time_compare",
    frontstage: ["三岁食贫｜淇水汤汤", "自我徂尔，三岁食贫。", "淇水汤汤，渐车帷裳。", "这两句里的时间，一样长吗？"],
    info_state: "首答不显示‘多年／片刻’完成答案；教师在学生读写以后命名两种时间尺度。",
  }),
  from("C404_405", { page_id: "C404_405", title: "不爽｜贰行｜罔极｜二三其德", render_mode: "responsibility_words",
    states: [
      { state_id: "B0", seconds: 180, state_function: "在完整三句中先写四词短义并标清人物主体。", render_mode: "responsibility_b0", frontstage: ["女也不爽，士贰其行。", "士也罔极，二三其德。", "不爽　贰行　罔极　二三其德", "先写准每个词，再标出它在说谁。"] },
      { state_id: "B1", seconds: 105, state_function: "公开两份真实首答，用上下句比较词义和主体分歧。", render_mode: "responsibility_b1", frontstage: ["哪些词在说女子？哪些词在说男子？", "看看黑板上两份真实标法。", "只用上下句提出修正。"] },
      { state_id: "B2", seconds: 135, state_function: "校准四词，在句内范围说明双方行为与伤害责任，再由学生亲自画出语意的加重。", render_mode: "responsibility_b2", frontstage: ["“女也不爽”，说的是哪一层？", "在这段婚姻的操持中，她并无差失。", "男子却行为前后不一，后来反复无常。", "她过去的判断可以反思；男子的失信与伤害不能归责于她。"] },
    ],
  }),
  from("C406", { page_id: "C406", title: "桑叶落下以后，发生了什么？", minutes: 6, render_mode: "story_rebuild",
    frontstage: ["桑叶落下以后，发生了什么？", "桑之落矣，其黄而陨。", "自我徂尔，三岁食贫。", "淇水汤汤，渐车帷裳。", "女也不爽，士贰其行。", "士也罔极，二三其德。"],
    info_state: "首屏不预填物象／生活／责任三卡；三层由学生复述后的现场板书形成。",
    student_action: ["每人写第四章自然章意", "合书口述并在断点返诗修订"], artifact: "个人第四章自然章意",
    script: script("请把第四章再读一遍。每个人先用三四句自然话写清：桑叶发生了什么变化；她嫁过去以后经历了怎样的生活和渡水片刻；诗怎样分清两个人的行为与责任。（等待，不给三层标题。）现在合上书，低声讲给自己听四十五秒。真正断开的地方立刻返诗，找到原句以后合书补完。请一位同学讲，其他人只指出应该回到哪一句。教师根据真实材料在黑板后置写出三个短语：桑叶变化、婚后生活、责任判断。每个人再看自己的章意，补一处原词或改一处责任表述。", 6, {
      timeboxes: [{ label: "完整重读", seconds: 40 }, { label: "个人第四章自然章意", seconds: 125 }, { label: "合书低声口述和返诗", seconds: 65 }, { label: "公开一份和定位断点", seconds: 60 }, { label: "教师后置板书和本人修订", seconds: 70 }],
      evidence_location: "每个人的第四章自然章意、原词补证和责任修订",
      cut_line: "第四章已经把生活事实和责任说清。第五章会把三岁拆成每一天，又让屋外的笑声传进来。",
    }),
    failure_signals: ["只有随机一人形成章意", "学生只抄三层标题", "个人文字没有任何原词或责任边界"],
  }),
  from("C501", { page_id: "C501", title: "第五章｜谁在忙，谁在笑，谁在独自思量？", render_mode: "chapter_poem" }),
  from("C502", { page_id: "C502", title: "一天，叠成许多年", render_mode: "nested_time",
    frontstage: ["三岁为妇，靡室劳矣。", "夙兴夜寐，靡有朝矣。", "靡室劳矣：家里的劳苦活儿，没有一样不做。", "夙：早　兴：起身　夜寐：晚睡　朝：一日", "一天从哪里开始，到哪里结束？", "哪个字让它不只发生一天？"],
  }),
  from("C503", { page_id: "C503", title: "后来再看开头，哪些细节值得留意？", render_mode: "warning_boundary",
    frontstage: ["后来再看开头，哪些细节值得留意？", "抱布贸丝　来即我谋　将子无怒", "后来再看，值得留意", "只凭当时，不能断定"],
    script: script("先读‘言既遂矣，至于暴矣’。‘言’是助词，‘遂’是如愿，‘暴’是粗暴；这句明写婚事如愿以后，他的行为走到了粗暴。现在翻回第一章，从‘抱布贸丝、来即我谋、将子无怒’中选一处，在纸上写两行：后来再看，这处值得留意什么；只凭当时，又不能断定什么。（等待首答。）请三位同学各读一处，听众只追问判断由哪个原词和哪条后来事实托住。后来的‘贰其行、二三其德、至于暴矣’会使早期细节成为需要认真观察的信息，提醒承诺要由长期行动核验；但它们不能证明男子从一开始就有已证实的预谋，也不能要求女子为没有预知未来负责。恋爱中的强烈投入可能使人忽略不协调信息，这值得我们学会审慎；但‘恋爱脑’不能成为责怪受伤者的标签。请把自己的两行改得更准确。", 6, {
      timeboxes: [{ label: "本句释义和翻回开头", seconds: 65 }, { label: "个人双行首答", seconds: 105 }, { label: "三份公开和证据追问", seconds: 85 }, { label: "边界校准和本人修订", seconds: 105 }],
      evidence_location: "第一、五章之间的‘值得留意／不能断定’双行句",
      cut_line: "男子的变化已经写明。第五章还有另一重孤立：外面的笑声散去以后，她只能独自思量。",
    }),
  }),
  from("C504", { page_id: "C504", title: "笑声散去以后……", render_mode: "sound_space",
    frontstage: ["笑声散去以后……", "兄弟不知，咥其笑矣。", "静言思之，躬自悼矣。", "外面的声音退去以后，空间里只剩下谁？"],
    info_state: "屏幕中间只保留空白；三秒沉默、站位和声场程序全部进入备注，不写在前台。",
    failure_signals: ["画面写出‘三秒沉默’", "外声表演成夸张嘲笑", "要求学生披露家庭经历"],
  }),
  from("C505", { page_id: "C505", title: "一间屋子里的许多年", render_mode: "life_writing",
    frontstage: ["一间屋子里的许多年", "夙兴夜寐｜既遂至暴｜兄弟不知｜躬自悼矣", "只写诗里有的日子，不替她增添诗外的遭遇。"],
  }),
  from("C601", { page_id: "C601", title: "第六章｜哪些旧愿、旧事和誓言又回来了？", render_mode: "chapter_poem" }),
  from("C602", { page_id: "C602", title: "及尔偕老｜老使我怨", render_mode: "old_word" }),
  from("C603", { page_id: "C603", title: "淇则有岸，隰则有泮", render_mode: "boundary_land",
    frontstage: ["淇则有岸，隰则有泮。", "这两处地貌有什么共同点？", "放在前后句之间，它可能接住什么？"],
  }),
  from("C604", { page_id: "C604", title: "这六处原词，怎样彼此照见？", render_mode: "neutral_cards", minutes: 5,
    info_state: "六张原词卡为同一中性色、随机散放；学生首排以后才显示旧日与后来两组事实。",
    states: [
      { state_id: "B0", seconds: 180, state_function: "让学生在无颜色、无分栏暗示下自行发现六处原词之间的关系。", render_mode: "random_cards", frontstage: ["这六处原词，怎样彼此照见？", "信誓旦旦", "至于暴矣", "言笑晏晏", "二三其德", "总角之宴", "不思其反", "先自己摆一摆：哪些词可以放在一起？依据是什么？"] },
      { state_id: "B1", seconds: 120, state_function: "依据学生首排后置校准双真相，并让本人写出能同时容纳两组事实的一句。", render_mode: "dual_truth_calibration", frontstage: ["她记得的旧日", "总角之宴｜言笑晏晏｜信誓旦旦", "后来显出的事实", "不思其反｜二三其德｜至于暴矣", "过去的欢乐是真；后来的失信也是真。", "请把两面都写进同一句话。"] },
    ],
  }),
  from("C605", { page_id: "C605", title: "反是不思，亦已焉哉", render_mode: "ending_boundary",
    frontstage: ["反是不思，亦已焉哉", "信誓旦旦，不思其反。", "反是不思，亦已焉哉！", "诗写到了哪里？又停在了哪里？"],
  }),
  from("C606_S01", { page_id: "C606_S01", title: "她的一生，怎样走到“亦已焉哉”？", minutes: 17, render_mode: "empty_life_line",
    student_action: ["每人先独立完成六章小长卷", "分组互证后接成公共长卷，再闭卷复述"], artifact: "时间封存的个人六章长卷和公共人生长卷",
    frontstage: ["她的一生，怎样走到“亦已焉哉”？", "第一章　　第二章　　第三章　　第四章　　第五章　　第六章"],
    info_state: "首屏只显示未完成六章时间线；相识、迁嫁、失衡、孤立、止息等章意不预填。",
    participation_path: "个人六章长卷先封存→六组各互证一章→一组一章卡→全班接成长卷→每人闭卷复述并返诗修复。",
    failure_signals: ["个人纸带在公共答案后补抄", "小组代表代替组员形成章意", "长卷只有事件没有转折或因果"],
    script: script("现在回答第一个问题：她的一生怎样走到‘亦已焉哉’？每个人先独立完成一条六章小长卷。每章只写三样：发生的一件事；一处关键原句的自然意思；它和前一章相比发生了什么变化。不会的地方先留空，不看同伴。（四分钟后翻面封存并抽取固定分层样本。）现在六组各互证一章：每个人都先读自己这一章的三项，有分歧就返诗；全员说过后，合成一张公共章卡。六张章卡按次序贴成长卷，每组只用一句话接上前一章。听众打开自己的六章小长卷，边听边补一个转折，但不整段抄公共卡。长卷完成后，教师沿原诗作一次朴素串讲：相识议婚、等待迁嫁、桑叶劝告、婚后贫困与失信、日复一日和孤立、回看旧誓并作出止息判断。现在合书三十秒，低声从第一章讲到第六章；断点立刻返诗，只修自己的空项。", 15, {
      timeboxes: [{ label: "个人六章小长卷首答", seconds: 250 }, { label: "六组各互证一章", seconds: 190 }, { label: "公共章卡接成长卷", seconds: 160 }, { label: "教师朴素串讲", seconds: 95 }, { label: "个人闭卷复述和返诗修复", seconds: 145 }, { label: "收束", seconds: 60 }],
      evidence_location: "公共答案前封存的个人六章小长卷；公共章卡；个人闭卷返诗修复",
      cut_line: "她的一生已经连成一条路。现在把其中最难熬的日子换成今天的生活语言，回答第二个问题。",
    }),
    states: [
      { state_id: "B0", seconds: 440, state_function: "每个人在公共答案前独立写事件、关键句自然义和章间变化。", render_mode: "life_line_b0", frontstage: ["她的一生，怎样走到“亦已焉哉”？", "第一章　第二章　第三章　第四章　第五章　第六章", "每章留下：一件事｜一句诗的自然意思｜与前一章相比发生了什么变化"] },
      { state_id: "B1", seconds: 250, state_function: "以六张真实章卡形成公共长卷，让听众补转折。", render_mode: "life_line_b1", frontstage: ["六张章卡，接成她的一生", "看黑板上的真实长卷：每一章怎样接住前一章？", "只补自己原先缺少的一个转折。"] },
      { state_id: "B2", seconds: 190, state_function: "教师沿原诗校准六章人生长卷，不把校准画面冒充个人检索。", render_mode: "life_line_b2", frontstage: ["相识议婚　→　等待迁嫁　→　桑叶劝告", "婚后贫困与失信　→　日复一日与孤立　→　回望旧誓，止息关系", "先看清这条路；下一页撤去答案。"] },
      { state_id: "B3", seconds: 140, state_function: "同时撤去屏幕与黑板上的六章答案，让每个人真正离屏复述并只修自己的断点。", render_mode: "blank_recall", frontstage: ["答案已经撤下。", "合上书，从第一章讲到第六章。", "断在何处，就回哪一句；补好以后，再合书讲完。"] },
    ],
  }),
  from("S02", { page_id: "S02", title: "她婚后的不幸，在生活中是什么样子？", minutes: 14, render_mode: "life_fact_entry",
    unique_function: "用现实生活语言说清婚后不幸的具体表现，再通过交换、猜诗和撤回越界表述返回原诗。",
    student_action: ["取回C505生活片段并由本人抽取两句现实生活事实", "四人合成生活事实卡并与他组交换核验", "每人完成第二问末答"], artifact: "C505个人片段、正反面生活事实卡和个人第二问末答", next_use: "S03读取失衡事实", deletion_loss: "不幸仍停在辛苦、悲惨等标签，C505也会沦为孤立写作。",
    visual_duty: "自然书写入口和学生真实生活事实卡", render_mode: "life_fact_entry",
    frontstage: ["她婚后的不幸，在生活中是什么样子？", "她每天过着怎样的日子？", "她在伴侣和家人那里遭遇了什么？", "先用今天的生活语言说清楚，再回原诗核验。"],
    script: script("现在回答第二个问题。先找回你在第五章写的《一间屋子里的许多年》。不要重写一份新作，只从旧稿中划出两处：她每天过着怎样的日子；她在伴侣和兄弟那里遭遇了什么。若旧稿漏了第四章的贫困或男子失信，就在旁边补一句并写原诗。（等待个人取回。）四人依次读，每个人都说过后，把重复内容合并，形成三到五张互不重复的‘生活事实卡’。正面只写生活语言，背面写能够托住它的原诗。与邻组交换，只看正面猜诗，再翻面核验；若添加了诗中没有的具体家务、暴力方式或求助过程，就退回这张卡的作者改稳。教师沿真实卡片归纳后撤去答案，每个人完成第二问末答：贫困与劳作、失信与粗暴、兄弟不知而笑、独自悲伤四个方面都要写到，每一项都带一处原诗。原稿有漏项就补一项；原稿已经齐全，就选一项把古词改成具体生活事实，再用原诗托住，不制造虚假的‘新增’。", 14, {
      timeboxes: [{ label: "个人现实语言首答", seconds: 125 }, { label: "四人轮说和合成卡", seconds: 220 }, { label: "组间交换猜诗和退回", seconds: 190 }, { label: "公共分歧和教师归纳", seconds: 185 }],
      evidence_location: "C505生活片段的取回痕迹、S02生活事实卡正反面及个人第二问末答",
      cut_line: "这些日子已经说清。下一步不是再列一次悲惨，而要追问：它为什么会一步步持续到这里？",
    }),
    info_state: "首答不显示标准五类不幸；教师归纳只在学生卡组形成和核验以后出现。",
    participation_path: "全员取回C505旧稿并抽取→四人全员轮说→一组3—5卡→组间交换→全班少量分歧卡→全员个人末答。",
    first_person_reception: "我能不用古词说清她婚后过着怎样的日子，又能把每一项送回原诗。",
    adjacent_counterproof: "C505只产生一个第五章片段，S03讨论原因；本页独自完成全文第二问的生活化和原诗核验。",
    failure_signals: ["生活语言只是古词同义替换", "少数代表包办卡片", "出现诗外具体伤害", "正反面无法互相核验"],
    states: [
      { state_id: "B0", seconds: 250, state_function: "真实取回C505个人生活片段，从旧稿抽取并补足第二问事实。", render_mode: "life_fact_b0", frontstage: ["找回《一间屋子里的许多年》", "划出：她每天过着怎样的日子。", "划出：她在伴侣和兄弟那里遭遇了什么。", "旧稿若漏了一项，只在旁边补一句并写原诗。"] },
      { state_id: "B1", seconds: 300, state_function: "四人卡片与邻组交换，正面生活语言和背面原诗依据互相核验。", render_mode: "life_fact_b1", frontstage: ["只看卡片正面：你能猜回哪一句诗？", "翻到背面核验。", "若写出了诗中没有的遭遇，把它退回这张卡的作者修订。"] },
      { state_id: "B2", seconds: 170, state_function: "根据真实卡片后置归纳婚后不幸的生活表现。", render_mode: "life_fact_b2", frontstage: ["婚后的日子一直贫困，家里的劳苦没有停歇", "说过的话变了，行为反复，后来甚至粗暴", "兄弟不了解她，反而笑她", "笑声退去以后，她只能独自悲伤", "每一项，都要回到原诗。"] },
      { state_id: "B3", seconds: 120, state_function: "撤去公共答案，让每个人完成四个方面齐全且带原诗的第二问末答，并按原稿状态诚实补缺或深化。", render_mode: "personal_answer", frontstage: ["现在只写自己的答案", "她婚后的不幸，具体落在怎样的日子里？", "贫困与劳作｜失信与粗暴｜不被兄弟理解｜独自悲伤", "四个方面都写到；每一项都带回一处原诗。", "原稿有漏项，就补一项；原稿已齐全，就把一项说得更具体。"] },
    ],
  }),
  from("S03", { page_id: "S03", title: "这场婚姻为什么走到这一步？", minutes: 18, render_mode: "cause_evidence_entry",
    unique_function: "沿人生长卷区分直接责任、使失衡持续的条件、支持缺失、割舍困难、婚前警讯边界和女子回应，形成不归责受伤者的完整原因结构。",
    student_action: ["每人写事实说明与不能说明", "小组放置证据卡并接受他组原因类型质询", "撤答后每人完成完整原因末答"], artifact: "事实—作用—边界卡、经质询修订的原因长卷和个人原因末答", next_use: "S04由悲剧反推共同生活支点", deletion_loss: "三问第三问缺少整体、有界和不归责的个人解释。",
    visual_duty: "未完成的人生长卷与学生原因证据卡", frontstage: ["这场婚姻为什么走到这一步？", "这组事实说明了什么？", "它不能被说成什么？", "把证据放回她的一生，再判断它起了怎样的作用。"],
    script: script("现在回答第三个问题。五组各领取一组尚未分类的原句：开头的抱布、来谋与‘将子无怒’；婚后的‘贰其行、二三其德、至于暴矣’；长期劳作和食贫；兄弟笑与独自悲；第六章的旧誓、回望和‘亦已焉哉’。每个人先写两行：这组事实说明了什么；它又不能被说成什么。（等待并封存。）组内每人读完以后，形成一张‘事实—作用—边界’卡，沿刚才的人生长卷放置。现在每组移到右边一张卡，用不同颜色的小签判断：这是男子伤害的直接责任，是使失衡继续的条件，是支持缺失，还是女子对处境的回应？若你认为箭头过强，写‘依据不足’。原组回来，只能用原诗修订。最后教师沿真实卡片归纳：男子失信、反复和粗暴承担直接责任；劳动、权力和情感投入长期失衡，使关系继续恶化；过去欢乐和已有投入可以解释为何难以割舍，却不是伤害原因；亲人不知和嘲笑使她缺少理解和托举；末章写的是她彻底失望后作出止息判断，是回应，不是婚姻失败的原因。开头细节值得审慎观察，但不能倒推预谋，也不能责怪她没有预知未来。", 15, {
      timeboxes: [{ label: "个人事实—作用—边界首答", seconds: 170 }, { label: "组内轮说和制卡", seconds: 245 }, { label: "沿长卷放置", seconds: 120 }, { label: "轮换质询原因类型", seconds: 160 }, { label: "原组返诗修订", seconds: 95 }, { label: "教师后置归纳", seconds: 110 }],
      evidence_location: "公共人生长卷上的事实—作用—边界卡、异色质询签和原组修订",
      cut_line: "悲剧的结构已经看清。现在不再只谈她该避开什么，而要转向未来：一段好的共同生活，最不能缺少什么？",
    }),
    info_state: "首答不显示警讯、沉没成本、责任、托举等预制分类；类别名称在学生制卡后用于质询。",
    participation_path: "个人双行封存→五组全员轮说→一组一卡→轮换质询→原组修订→教师后置归纳。",
    first_person_reception: "我能独立说明责任、持续条件、支持缺失、为何难以割舍、婚前可观察而不可倒推的边界，以及她最后的回应。",
    adjacent_counterproof: "S02只说明生活表现，S04转向建设性讨论；本页独自承担原因结构和伦理边界。",
    failure_signals: ["把女子投入、等待或劳作写成男子伤害的原因", "把止息判断列为婚姻破裂原因", "公共结构由教师在首答前给出", "卡片在公共答案后补抄"],
    states: [
      { state_id: "B0", seconds: 300, state_function: "每个人在未经分类的原句事实前写说明与不能说明。", render_mode: "cause_b0", frontstage: ["这场婚姻为什么走到这一步？", "这组事实说明了什么？", "它不能被说成什么？", "先独立写下，再把证据放回她的一生。"] },
      { state_id: "B1", seconds: 380, state_function: "以现场事实—作用—边界卡和异色质询签形成原因长卷。", render_mode: "cause_b1", frontstage: ["沿着她的一生，看看这些事实起了怎样的作用。", "谁应为伤害负责？哪些日子让不幸继续？她身边少了谁的理解？", "若一句判断说得太满，请写：原诗还不能证明。"] },
      { state_id: "B2", seconds: 160, state_function: "后置形成不归责受伤者的原因结构和婚前审慎边界。", render_mode: "cause_b2", frontstage: ["男子失信、反复并走向粗暴，伤害的责任在他", "贫困与劳作日复一日，关系里的担子越来越偏向一人", "兄弟不知而笑，她在困境中没有得到理解", "旧日欢乐与已有投入会让割舍更难，却不是她受伤的原因", "开头的细节值得留意，却不能倒推一开始就有预谋", "“亦已焉哉”是她醒悟后的回应，不是悲剧的原因"] },
      { state_id: "B3", seconds: 240, state_function: "撤去公共结构，让每个人用原诗完成六层原因与边界完整末答。", render_mode: "personal_answer", frontstage: ["现在不看归纳，只写自己的答案", "谁应为伤害负责？", "哪些日子让不幸继续？她缺少谁的理解？", "什么让割舍更难，却不能成为责怪她的理由？", "开头哪些细节值得留意？又不能证明什么？", "“亦已焉哉”是什么回应？为什么不是悲剧原因？", "每一层都写一处原诗。"] },
    ],
  }),
  from("S04", { page_id: "S04", title: "一段好的共同生活，最不能缺少什么？", minutes: 15, render_mode: "future_card",
    unique_function: "让每个人以一处原诗形成婚姻观，再由全员轮说和冲突质询生成班级共同生活支点。",
    student_action: ["每人用一处原诗提出一个关系条件", "四人全说后只留一张给未来的卡"], artifact: "每组一张给未来的共同生活支点卡", next_use: "S08终课引用；真实试教评估", deletion_loss: "全文讨论停在悲剧诊断，导入主题谱成为孤儿。",
    visual_duty: "开放问题；随后由真实学生卡形成平衡木", frontstage: ["一段好的共同生活，最不能缺少什么？", "这处悲剧提醒我……", "因此，好的共同生活需要……", "只给未来的自己或朋友留一句话。"],
    script: script("现在把书翻在自己最想引用的一处。假如只给未来的自己或朋友留一句话：一段好的共同生活，最不能缺少什么？先用两句话准备：‘这处悲剧提醒我……因此，好的共同生活需要……’不谈自己的家庭，也不猜老师的标准词。（等待。）四个人按座位依次完整说；所有人说过以前不评价、不抢答。说完以后才追问原诗、合并相近或保留分歧。每组只留一张最想送给未来的卡，写原诗依据和一句关系条件。贴到黑板的平衡木周围。全班不逐张朗读，只看同义卡、冲突卡和明显缺项。教师只沿真实卡片归纳：可能有审慎了解、言行长期一致、边界与尊重、劳动和决定公平、共同承担、困难时的理解与支持网络、发现持续伤害后的求助和止损。若现场没有某项，教师明确说这是基于全文事实补充，不冒充学生原话。最后回投开头的爱情婚姻文学主题谱：《氓》为它新添了什么？只补一条新认识。", 13, {
      timeboxes: [{ label: "个人返诗准备", seconds: 100 }, { label: "四人全员轮说", seconds: 220 }, { label: "追问、合并和一组一卡", seconds: 150 }, { label: "贴卡和冲突质询", seconds: 140 }, { label: "教师后置归纳", seconds: 110 }, { label: "回投导入主题谱", seconds: 60 }],
      evidence_location: "个人原诗标记；每组唯一‘给未来的卡’；回投主题谱新增项",
      cut_line: "共同生活的支点已经从悲剧和你们的话里长出来。最后，我们把沿途读过的文化、字词和写法收好，再完整读一遍。",
    }),
    info_state: "首屏不预填好的婚姻结构；教师支点只在学生卡片形成后归纳。",
    participation_path: "个人返诗→四人全员轮说→全员后才讨论→每组一卡→全班只看同义、冲突和缺项。",
    first_person_reception: "我用一处原诗表达了自己的婚姻观，也听见并参与形成了一张给未来的共同生活条件卡。",
    adjacent_counterproof: "S03停在原因，S05转入知识；本页独自完成价值表达、建设性迁移和导入回扣。",
    failure_signals: ["组长代劳", "教师提前显示标准支点", "讨论评判同学家庭或受伤者", "多数学生只旁观公共卡"],
    states: [
      { state_id: "B0", seconds: 330, state_function: "每个人先用一处原诗形成自己的婚姻观。", render_mode: "future_b0", frontstage: ["一段好的共同生活，最不能缺少什么？", "这处悲剧提醒我……", "因此，好的共同生活需要……", "只给未来的自己或朋友留一句话。"] },
      { state_id: "B1", seconds: 280, state_function: "四人全员轮说后形成每组唯一的给未来的卡。", render_mode: "future_b1", frontstage: ["把每组最想送给未来的一句话贴上来。", "先看哪些彼此照应，再看哪些彼此冲突。", "每张卡都要带着一处《氓》的原诗。"] },
      { state_id: "B2", seconds: 100, state_function: "只呈现当堂真实学生卡，让原作者和同学先把学生话语与原诗照应说清。", render_mode: "future_card_only", frontstage: ["先听你们写下的话", "“　　　　　　　　　　　　　　　　”", "原作者读卡；同学只指出它照应的原诗，或仍保留的分歧。"] },
      { state_id: "B3", seconds: 70, state_function: "在学生卡已经被听见以后，分清诗中事实与由诗走向今天的建议。", render_mode: "future_summary_only", frontstage: ["听过你们的话，再分清两层", "诗中写到的", "承诺落空｜日子失衡｜兄弟不知而笑｜她作出止息判断", "由诗想到今天", "面对持续伤害，可以求助；必要时离开", "现代建议不是诗中已经发生的结局。"] },
      { state_id: "B4", seconds: 120, state_function: "每个人亲自把《氓》带回开头文学长卷，留下自己的新增认识。", render_mode: "personal_answer", frontstage: ["回到开头那幅爱情与婚姻文学长卷", "《氓》为它新添了什么？", "请用自己的话补上一句。", "可以不同意教师的归纳，但要带着一处原诗。"] },
    ],
  }),
  from("S05A", { page_id: "S05A", title: "《诗经》，我们真正记住了什么？", minutes: 6, render_mode: "culture_retrieval",
    frontstage: ["《诗经》，我们真正记住了什么？", "它是什么？", "有多少篇？", "作品大致来自怎样的年代？", "分哪三类？《氓》在哪里？", "先合书写；不确定，可以留空。"],
    unique_function: "检验开篇文化入口是否真正留下，并修复第一部诗歌总集、305篇、大致年代、风雅颂和篇目归属。",
    student_action: ["合书完成五项文化检索", "开书或看课堂批注核对，再合书串说"], artifact: "《诗经》五项文化修复稿", next_use: "S06艺术收纳和S08终读", deletion_loss: "开篇文化输入未经检索，学生可能把看过冒充记住。",
    script: script("请合上书和文化批注，独立写五项：第一，《诗经》在中国文学史上是什么；第二，现存多少篇；第三，作品大致来自怎样的年代；第四，传统上分哪三类；第五，《氓》收在哪里。不确定可以留空，不偷看同桌。（等待并封存。）现在打开开篇批注或教材核对：我国第一部诗歌总集，三百零五篇，作品大致产生于西周初年至春秋中叶，传统上分风、雅、颂，《氓》在《卫风》中。请本人只修错空项。最后重新合上书，用两句话说给同桌听：先说《诗经》的基本身份，再说《氓》在其中的位置。听者只指出一项事实是否遗漏，不替对方整句重写。", 6, {
      timeboxes: [{ label: "合书五项首答", seconds: 125 }, { label: "开书核对和本人修订", seconds: 115 }, { label: "教师准确收束真实错项", seconds: 55 }, { label: "再合书同桌串说", seconds: 65 }],
      evidence_location: "公共答案前封存的五项文化首答、本人修订和再合书串说",
      cut_line: "文化坐标已经重新取回。接下来检查六章的关键字词，哪里还会让我们在完整朗读中断下来。",
    }),
    info_state: "首答不显示第一部诗歌总集、305篇、年代、风雅颂和卫风答案；校准在等待以后。",
    states: [
      { state_id: "B0", seconds: 130, state_function: "合书完成五项无答案首答，允许真实留空。", render_mode: "culture_retrieval", frontstage: ["《诗经》，我们真正记住了什么？", "它是什么？", "有多少篇？", "作品大致来自怎样的年代？", "分哪三类？《氓》在哪里？", "先合书写；不确定，可以留空。"] },
      { state_id: "B1", seconds: 140, state_function: "打开开篇批注校准五项事实，只修本人错空。", render_mode: "culture_answer", frontstage: ["《诗经》｜我国第一部诗歌总集", "现存305篇", "作品大致产生于西周初年至春秋中叶", "风｜雅｜颂", "《氓》在《卫风》中", "只修自己错空的地方。"] },
      { state_id: "B2", seconds: 90, state_function: "再次撤去答案，让每个人用两句话说清《诗经》身份与《氓》位置。", render_mode: "blank_recall", frontstage: ["现在再合上书", "用两句话说给同桌听：", "《诗经》的基本身份是什么？", "《氓》在其中什么位置？"] },
    ],
  }),
  from("S05B", { page_id: "S05B", title: "六章关键字词，能不能回到原句？", minutes: 12, render_mode: "word_retrieval",
    unique_function: "用六章各一项全员最低门槛发现个人基础盲点，再以自选两词作加深，不让抽样词表冒充全诗读通。",
    student_action: ["独立完成六章六项音义原句", "持教材修复空项，再自选两词加深"], artifact: "六章字词通关卡和两词加深稿", next_use: "S08终读提醒", deletion_loss: "个人未选词盲点无法发现，逐句讲解没有基础语义兜底。",
    visual_duty: "六章关键原句与六个最低通关空位", frontstage: ["六章关键字词，能不能回到原句？", "第一章：愆", "第二章：筮", "第三章：说", "第四章：爽", "第五章：咥", "第六章：泮", "每项写：读音｜句中义｜原句。不会，可以留空。"],
    script: script("合上书，六章各有一个最低门槛词：第一章‘愆’，第二章‘筮’，第三章‘说’，第四章‘爽’，第五章‘咥’，第六章‘泮’。每项只写三样：读音、在本句中的意思、含有它的原句。不会可以留空，不能先挑会的做。（等待并封存。）现在打开教材逐项核对：愆是拖延、延误；筮是用蓍草占问；说同‘脱’，脱身；爽是差错；咥读xì，笑的样子；泮同‘畔’，边岸。请本人只修自己错空处，并在教材对应句旁圈一个终读提醒。六项修复后，再从全诗自选两个仍不稳的词，写音义原句作加深。教师只讲固定分层样本中的共性错项，不把十几个词再抄成大表。", 12, {
      timeboxes: [{ label: "合书六章六项首答", seconds: 210 }, { label: "开书逐项核对和本人修复", seconds: 245 }, { label: "固定样本共错微讲", seconds: 105 }, { label: "自选两词加深", seconds: 125 }, { label: "终读提醒", seconds: 35 }],
      evidence_location: "公共答案前封存的六章字词通关卡；本人修订；两词加深稿",
      cut_line: "字词已经回到六章原句。接下来不再列知识点，而要看这些句子怎样共同写成这首诗。",
    }),
    info_state: "首答只给六个目标词和原句任务，不给读音与义；校准后再显示答案。",
    participation_path: "全员六项首答→开书本人修复→教师只讲真实共错→个人两词加深。",
    first_person_reception: "我知道自己在哪一章的哪个词断过，也已经把读音和句中义修回原句。",
    adjacent_counterproof: "逐句细读分散发生，S08只终读；本页独自承担全诗基础语义的个人兜底。",
    failure_signals: ["仍只任选两词", "公共答案后补抄被计为首答", "词义不回原句", "六项没有固定样本审计"],
    states: [
      { state_id: "B0", seconds: 250, state_function: "六章六项无答案首答，发现每个人真实错空。", render_mode: "word_gate_b0", frontstage: ["六章关键字词，能不能回到原句？", "愆　筮　说　爽　咥　泮", "每项写：读音｜句中义｜原句。不会，可以留空。"] },
      { state_id: "B1", seconds: 275, state_function: "打开教材逐项核对并由本人修复。", render_mode: "word_gate_b1", frontstage: ["打开教材，只修自己错空的地方。", "每修一项，都把它送回所在原句。", "在对应句旁圈一个终读提醒。"] },
      { state_id: "B2", seconds: 195, state_function: "校准六项共性错处，再让学生自选两词加深。", render_mode: "word_gate_b2", frontstage: ["六章六词，逐项校准", "愆（qiān）｜延误｜匪我愆期", "筮（shì）｜用蓍草占问｜尔卜尔筮", "说（tuō）｜同“脱”，脱身｜犹可说也", "爽（shuǎng）｜差错｜女也不爽", "咥（xì）｜笑的样子｜咥其笑矣", "泮（pàn）｜同“畔”，边岸｜隰则有泮", "六项修好以后，再自选两个仍不稳的词。"] },
    ],
  }),
  from("S06", { page_id: "S06", title: "她的故事，怎样被写进六章诗里？", minutes: 15, render_mode: "art_map",
    unique_function: "把逐句体验收成叙事推进、桑叶比兴与对照、词句复现反折、四言叠词与声音四类知识，并说明写法怎样改变人物故事。",
    frontstage: ["她的故事，怎样被写进六章诗里？", "六章叙事怎样推进？", "桑叶怎样前后照应？", "哪些词句回来以后改变了声音？", "四言与叠词怎样让她说话？", "每一处都要带回原诗，也要说它改变了什么。"],
    info_state: "只给知识检索类别，不给代表原句和作用答案；教师术语提升在小组补例以后。",
    student_action: ["面对随机散卡自行分组", "比较黑板分法后由教师命名", "每人完成四类识别并自选两类深做"], artifact: "个人随机分组、教师后置知识图、四类最低识别和个人两类深做",
    script: script("先不看术语。屏幕上只有已经读过的材料：六章事件变化；‘桑之未落／桑之落矣’和鸠、女句；两个‘老’、两个‘反’及淇水复现；涟涟、汤汤、晏晏、旦旦。每个人先选两组你认为可以放在一起的材料，写共同点和它们怎样改变故事或声音。（等待。）四组各把一种分法写到黑板，不给标准名称。全班看黑板：哪些分法其实在看同一种写法，哪些仍混在一起？教师此时后置命名：六章叙事推进；桑叶比兴与前后对照；词句复现、回环和反折；四言节奏、叠词与声音。每一类都必须带一处原诗和作用。最后每个人任选两类，合书写‘原诗—写法—它怎样改变人物故事或声音’，开书返诗修正。", 12, {
      timeboxes: [{ label: "无术语例句观察和个人分组", seconds: 190 }, { label: "四组黑板分法", seconds: 150 }, { label: "全班比较学生分法", seconds: 100 }, { label: "教师后置命名和准确提升", seconds: 115 }, { label: "个人两类说明和返诗修订", seconds: 165 }],
      evidence_location: "个人无术语分组；黑板学生分法；个人两类‘原诗—写法—作用’修订",
      cut_line: "这些名字已经重新落回她的六章故事。最后不再做一张表，只留一句自己的话，再完整读一遍。",
    }),
    states: [
      { state_id: "B0", seconds: 250, state_function: "把十六张等颗粒原诗证据做成等大同色、经反聚簇校验的混排卡，让学生真正自拟分组。", render_mode: "art_random", frontstage: ["这些已经读过的句子，哪些可以放在一起？", "抱布贸丝", "桑之未落", "不思其反", "泣涕涟涟", "反是不思", "氓之蚩蚩", "送子涉淇", "桑之落矣", "信誓旦旦", "以我贿迁", "于嗟鸠兮", "不见复关", "于嗟女兮", "既见复关", "言笑晏晏", "夙兴夜寐", "先自己分；不要猜老师准备了几类。"] },
      { state_id: "B1", seconds: 250, state_function: "比较黑板上的学生分法、差异和混杂。", render_mode: "art_b1", frontstage: ["看看黑板上你们自己的分法", "哪些其实在看同一种写法？", "哪些材料还混在一起？", "只用原诗说明。"] },
      { state_id: "B2", seconds: 220, state_function: "后置命名四类写法，回收赋比兴，并为每类补一处原诗和具体作用。", render_mode: "art_b2", frontstage: ["四种写法，从原诗里生长出来", "赋：铺陈直叙，六章叙事推进", "比、兴：桑叶起兴与前后对照", "词句复现、回环与反折", "四言节奏、叠词与声音", "每一类都要带一处原诗，也要说它怎样改变故事或声音。"] },
      { state_id: "B3", seconds: 180, state_function: "撤去教师例子，完成四类最低识别，再自选两类深入说明。", render_mode: "art_mastery", frontstage: ["四类都先留下一个原诗例子", "赋与叙事｜比兴与对照｜复现与反折｜节奏与声音", "然后自选两类写深：", "原诗｜写法｜它怎样改变人物故事或声音"] },
    ],
  }),
  from("S08", { page_id: "S08", title: "读完《氓》", minutes: 7, render_mode: "final_reading",
    frontstage: ["读完《氓》", "一处改变最大的理解", "一处最想带走的语言发现", "一个仍愿意追问的问题", "从“氓之蚩蚩”读到“亦已焉哉”"],
    student_action: ["三选一留下真实终课句", "至少180秒完整朗读"], artifact: "个人终课句和完整终读",
    normal_counterexample: "没有发生明显改变者可选语言发现或真实问题，不伪造改变。",
    script: script("请先看自己一路留下的批注、长卷和最后的关系卡，只选一个出口：一处改变最大的理解；一处最想带走的语言发现；或者一个仍愿意追问的问题。三选一，写一句真实的话，不必把三项填满。（等待并收取少量自愿分享。）现在把屏幕降暗，翻回全文，也看一眼你在六个关键字词旁圈出的终读提醒。我们不再停下来分析，从‘氓之蚩蚩’完整读到‘亦已焉哉’。读到自己的提醒处，只把音义读稳；读到最想带走的一处，让声音自然慢一点。末句以后不加总结，安静停十五秒。", 7, {
      timeboxes: [{ label: "三选一个人终课句", seconds: 105 }, { label: "少量真实分享", seconds: 75 }, { label: "完整终读", seconds: 210 }, { label: "末句静默", seconds: 15 }, { label: "自然收束", seconds: 15 }],
      evidence_location: "个人三选一终课句；完整终读与末句静默计时",
      listener_task: "分享阶段只听取他人带走的原诗或问题；终读阶段共同维护节奏，不评价情绪是否相同。",
      cut_line: "（末句后保持安静，不再切入新的结论页。）",
    }),
  }),
];

pages.forEach((page, index) => {
  page.page_number = index + 1;
  if (!page.states?.length) {
    page.states = [{ state_id: "A", seconds: page.minutes * 60, state_function: page.unique_function, render_mode: page.render_mode, frontstage: page.frontstage }];
  }
  for (const state of page.states) {
    const key = `${page.page_id}-${state.state_id}`;
    if (stateScripts[key]) state.script = clone(stateScripts[key]);
    else if (page.states.length === 1) state.script = clone(page.script);
    else throw new Error(`missing V5 physical-state script ${key}`);
  }
});

const lesson = {
  schema_version: "2.0",
  lesson: "《氓》",
  version: "6.6-v5-p2-closure-candidate",
  status: "no-image-implementation-candidate",
  target_pages: pages.reduce((sum, page) => sum + page.states.length, 0),
  target_logical_pages: pages.length,
  target_natural_minutes: pages.reduce((sum, page) => sum + page.minutes, 0),
  illustration_policy: "no_illustration_until_v66_no_image_dual_review",
  three_questions: ["她经历了什么？", "她婚后的不幸，在生活中是什么样子？", "这场婚姻为什么走到这一步？"],
  pages,
};

if (require.main === module) process.stdout.write(`${JSON.stringify(lesson, null, 2)}\n`);
module.exports = lesson;
