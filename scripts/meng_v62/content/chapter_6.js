"use strict";
const { contract: textContract } = require("../../meng_v6/text");
const chapter = textContract.chapters.find((x) => x.chapter_id === "C6"),
  lineMap = Object.fromEntries(
    textContract.lines.map((x) => [x.line_id, x.text]),
  ),
  CHAPTER_TEXT = chapter.line_ids.map((id) => lineMap[id]);
function page(v) {
  const req = [
    "page_id",
    "title",
    "minutes",
    "source_line_refs",
    "original_text",
    "literary_object",
    "current_difficulty",
    "unique_function",
    "visible",
    "first_glance",
    "information_state",
    "student_action",
    "artifact",
    "normal_path",
    "bounded_feedback",
    "revision",
    "teacher_synthesis",
    "story_return",
    "next_use",
    "deletion_loss",
    "merge_test",
    "visual_duty",
    "interaction_signature",
    "first_person_reception",
    "screen",
    "script",
  ];
  for (const k of req)
    if (v[k] === undefined || v[k] === null || v[k] === "")
      throw new Error(`${v.page_id || "unknown"} missing ${k}`);
  for (const k of [
    "teacher_spoken",
    "scene",
    "stage_directions",
    "timeboxes",
    "branches",
    "listener_task",
    "evidence_location",
    "cut_line",
  ])
    if (!v.script[k] || !v.script[k].length)
      throw new Error(`${v.page_id} script missing ${k}`);
  return v;
}
const pages = [
  page({
    page_id: "C601",
    title: "第六章｜她把哪些旧事重新放回眼前？",
    minutes: 4,
    source_line_refs: chapter.line_ids,
    original_text: CHAPTER_TEXT.join("。") + "。",
    literary_object:
      "第六章完整声音及偕老愿望、自然边界、少年言笑、信誓与停止判断的时间回环",
    current_difficulty:
      "学生带着第五章孤立处境进入，容易只抓住末句决绝，忽略女子在停止之前重新核验了愿望、共同记忆和誓言",
    unique_function:
      "让第六章完整响起，由学生先标一处回到过去的原句和一处真正收束全诗的原句，建立回望—核验—停止的初稿",
    visible: `第六章｜她把哪些旧事重新放回眼前？\n\n${CHAPTER_TEXT.map((x) => `${x}。`).join("\n")}\n\n完整读完，再留下：\n一处回到过去的原句｜一处真正收束全诗的原句`,
    first_glance:
      "整章原诗主位，不在标题或提示中预告违誓、觉醒、离开和决绝等完成结论",
    information_state: {
      known: "故事已到多年劳作、男子粗暴、兄弟讥笑和女子独自思量",
      reveal_now: "第六章的完整时间跨度、回到过去和结尾收束的初步位置",
      defer: "老字回环、有岸/有泮多解、少年记忆与誓言核验、停止判断边界",
    },
    student_action: [
      "完整朗读第六章，读完才抄一处回到过去的原句",
      "再抄一处真正收束全诗的原句；暂时只留下声音词或问号",
    ],
    artifact: "06F C601区的过去句、收束句与一个初始声音词",
    normal_path:
      "把第一句视为过去也可暂存；声音词写不出可留问号；同桌后仍分歧不由教师立即裁决",
    bounded_feedback:
      "同桌只核对原句来源和时间感，不报结尾标准情绪，不替同伴解释",
    revision: "学生移动一次时间标记，或将抽象结论改回完整原句，并保留声音问号",
    teacher_synthesis:
      "只确认本章把当下怨意、自然边界、少年言笑和信誓放在同一回望中，最后以亦已焉哉收束；意义逐句生成",
    story_return:
      "独自思量以后，女子重新看向偕老愿望、少年欢笑与当初誓言，核验它们如何走到今天",
    next_use:
      "C602读取偕老句，C603读取边界句，C604读取旧事，C605读取结尾声音，C606整章重建",
    deletion_loss:
      "若没有完整章读，末句会被抽成励志口号，学生看不见停止判断是在回望和核验旧事之后形成",
    merge_test:
      "不能并入C602：整章未知声音必须先于老字解释发生，C602才聚焦一个词的前后回环",
    visual_duty: "让第六章全文成为唯一主视觉，并保存过去与收束的两个开放定位",
    interaction_signature: {
      cognitive_action: "整体接收与时间回环察觉",
      sensory_channel: "完整朗读、原句摘录",
      social_structure: "个人初读—同桌来源核对",
      artifact_form: "过去与收束初稿",
      emotional_rhythm: "旧事回涌、声音等待收束",
    },
    first_person_reception:
      "我先完整读完，没有直接跳到结尾；我找到她重新看见的旧事，也留下了末句最初的声音。",
    screen: {
      kind: "full",
      prompt: "一处回到过去的原句｜一处真正收束全诗的原句",
    },
    script: {
      teacher_spoken:
        "第五章最后，她静下来，只能独自思量。第六章会不会立刻斩断过去？请先不要只等最后一句，让五句完整地走一次。读时听一听：她把哪些旧事重新放回眼前，哪一句才真正把全诗收住。（教师完整范读，学生再低声完整读。）现在才落笔：抄一处回到过去的原句，再抄一处真正收束全诗的原句；在末句旁只留一个你最初听见的声音词，听不准就留问号。同桌只核对是不是原句、时间是否真的回到过去，不替对方命名情绪。（等待。）我们先不把末句叫成觉醒或离开。女子要先重新经过偕老、边界、少年言笑和誓言，结尾才会到来。",
      scene:
        "屏幕只呈现第六章全文和两个读后入口；教师不突出末句，学生落笔前不染色时间层。",
      stage_directions: [
        "读取第五格",
        "教师完整范读",
        "学生完整低声读",
        "读后才摘过去句和收束句",
        "同桌只核对来源与时间",
        "学生亲自修订",
      ],
      timeboxes: [
        { label: "承接第五格", seconds: 25 },
        { label: "教师和学生完整读章", seconds: 90 },
        { label: "个人两项初稿", seconds: 60 },
        { label: "同桌来源核对和修订", seconds: 40 },
        { label: "引用原句与转场", seconds: 25 },
      ],
      branches: [
        {
          kind: "只等亦已焉哉",
          response: "先抄一处更早的旧事句，让停止之前的核验过程保留下来。",
        },
        {
          kind: "直接写已经离开",
          response: "退回原句，只写收束声音；是否实际离开待C605区分。",
        },
        {
          kind: "情绪词互相不同",
          response: "保留疲惫、怨、清醒等不同初听，不以投票选唯一。",
        },
      ],
      listener_task: "只核对原句和时间位置，不替同伴给末句定性。",
      evidence_location: "06F C601区",
      cut_line: "先看第一个回环：同一个‘老’字，一边是愿望，一边为什么成了怨？",
    },
  }),
  page({
    page_id: "C602",
    title: "及尔偕老｜老使我怨",
    minutes: 5,
    source_line_refs: ["L026"],
    original_text: `${lineMap.L026}。`,
    literary_object:
      "同一个老字在共同愿望与现实怨苦中的回环，以及一句之内过去期待与当下判断的正面冲撞",
    current_difficulty:
      "学生会把句子平直翻译为不能白头，却听不见同一字如何把曾经愿望反折成当下怨意",
    unique_function:
      "借两人接读同一个老字，让学生用停顿和重音亲耳发现同词在两个时间层中意义翻转",
    visible: `${lineMap.L026}。\n\n及：同、跟　偕老：共同到老\n\n同一个“老”，\n前后两次落在怎样不同的生活里？`,
    first_glance:
      "原句与最低词义占中心，不显示愿望破裂、幻灭等教师答案；两个老由学生在声音中区分",
    information_state: {
      known: "C601已发现本章重新回望旧事",
      reveal_now: "及、偕老、怨的自然义及两个老连接的过去愿望与当下怨意",
      defer: "自然边界如何反衬、少年和誓言如何进一步核验",
    },
    student_action: [
      "两人分别读及尔偕老与老使我怨，在同一老字处交接；交换角色",
      "听者写两次老分别落在怎样的生活里，读者据反馈只改一次停顿或重音",
    ],
    artifact: "06F C602区的两层老、一次声音反馈与改读痕迹",
    normal_path:
      "认为两处都指年老者可先保留字面，再补愿望/现实语境差异；不愿对读者可作听者",
    bounded_feedback:
      "听者只报告是否听出愿望与怨的转折，不评价感情饱满；教师后置解释回环",
    revision: "学生补写两个时间层或只改一处交接停顿，使同词翻转可被听见",
    teacher_synthesis:
      "前一个老属于共同到老的愿望，后一个老落在现实设想中的怨苦；同词回环让愿望与现实在一句中相撞",
    story_return: "她曾想与他共同到老，如今想到这样的未来，首先升起的却是怨",
    next_use: "C603比较有岸/有泮反衬的是心意无常还是怨苦无边；C606重建章意",
    deletion_loss:
      "删除会让首句只剩译文，学生无法从同词回环体验愿望如何在现实中反折，也削弱下一句无边之感",
    merge_test:
      "不能并入C603：本页核心是同词声音翻转，下一页核心是两种解释比较；需要不同证据状态",
    visual_duty:
      "将一句分成两个以老字相接的时间面，让学生的对读成为视觉和听觉焦点",
    interaction_signature: {
      cognitive_action: "同词回环与声音翻转",
      sensory_channel: "双人接读、闭眼听、单点改读",
      social_structure: "角色对读—听者定位反馈",
      artifact_form: "两层老与改读",
      emotional_rhythm: "旧愿从一个字折回现实",
    },
    first_person_reception:
      "我通过同一个老字的两次落点，听见共同到老的愿望怎样反成今天的怨，也改了一处读法。",
    screen: {
      kind: "hinge",
      left: "及尔偕老",
      hinge: "老",
      right: "使我怨",
      gloss: "及：同、跟｜偕老：共同到老",
      prompt: "同一个‘老’，前后两次落在怎样不同的生活里？",
    },
    script: {
      teacher_spoken:
        "先把句子说成自然话。及是同、跟；偕老是共同到老。现在两人一组，一人读‘及尔偕老’，另一人紧接‘老使我怨’。两人的声音必须在同一个‘老’字上交接，交换再来一次。听的人闭眼，只写：第一个老落在怎样的生活愿望里，第二个老落在怎样的现实感受里。（等待对读。）读者只根据反馈改一次停顿或重音，不需要哭腔。我们听一组第二遍。同一个字没有变，时间和生活却变了：曾经盼共同到老，如今想到这样的未来，老去只会使她怨。诗不是另起一句说失望，而让旧愿从同一个字里折回来。",
      scene:
        "屏幕把原句在老字处形成铰链；两名学生以同一个字交接，听者闭眼定位愿望与现实。",
      stage_directions: [
        "个人自然口译",
        "教师校准及与偕老",
        "双人以老字接读",
        "交换角色再读",
        "听者写两层生活",
        "读者只改一次",
        "呈现一组第二遍",
      ],
      timeboxes: [
        { label: "口译与词义", seconds: 60 },
        { label: "两轮接读", seconds: 70 },
        { label: "听者写两层生活", seconds: 55 },
        { label: "单点改读和抽样", seconds: 65 },
        { label: "后置归纳与转场", seconds: 50 },
      ],
      branches: [
        {
          kind: "只说都是年老",
          response: "保留字面，再补前半的愿望语气和后半的怨意语境。",
        },
        {
          kind: "表演过度",
          response: "收回哭腔，只改老字前后的一处停顿或重音。",
        },
        {
          kind: "没有听出翻转",
          response: "分别把偕老和怨按住再读，听者只定位两个词的方向。",
        },
      ],
      listener_task: "只听同一老字前后的愿望与现实是否转折，不示范标准读法。",
      evidence_location: "06F C602区",
      cut_line:
        "愿望与怨已经撞在一起。下一句忽然说淇水有岸、低湿地有边——究竟在反衬什么没有边？",
    },
  }),
  page({
    page_id: "C603",
    title: "淇则有岸，隰则有泮",
    minutes: 6,
    source_line_refs: ["L027"],
    original_text: `${lineMap.L027}。`,
    literary_object:
      "淇水与低湿地的自然边界，以及它可反衬男子心意无常或女子偕老怨苦无边的两种有据解释",
    current_difficulty:
      "学生容易把岸、泮机械译成做人要有边界，或只接受一个象征密码，忽略教材保留的多义衔接",
    unique_function:
      "用两条竞争解释在全班证据席中比较它们各自怎样接前后文，允许学生排序而不封唯一答案",
    visible: `${lineMap.L027}。\n\n隰（xí）：低湿的地方\n泮（pàn）：同“畔”，边、岸\n\n为什么在“偕老／怨”之后，\n忽然写淇与隰的岸和泮？\n它怎样接前句，也怎样照见后文？`,
    first_glance:
      "原句与最低词义在先，只提出开放问题；不提前展示两种教材解释标签",
    information_state: {
      known: "首句将偕老愿望折为怨",
      reveal_now: "隰、泮词义，自然有界与人事无边的反衬，两种可竞争解释",
      defer: "不将边界现代口号硬套入原句；具体选择允许保留到全文理解",
    },
    student_action: [
      "个人先写一种可能及前后文依据；听到同伴另一种解释后，再写第二种",
      "四人组把两种解释分别接回首句或后文，个人最终标更能说服自己的一个并写保留理由",
    ],
    artifact: "06F C603区的双解释、前后文证据、个人排序和保留分歧",
    normal_path:
      "只想到一种者先保留，听同伴后补第二种；认为两种都可者标并列但须说明各自衔接；不站队也可",
    bounded_feedback:
      "同伴只问这解释接哪句、靠哪个词，不以人数裁决；教师后置说明教材多解",
    revision:
      "学生补第二种解释、调整排序或把现代婚姻边界口号改回男子无常/女子怨苦的语境",
    teacher_synthesis:
      "自然都有边，一说反衬男子心意无常、没有限制，一说反衬女子若偕老将怨苦无边；两种都须由全章衔接证明",
    story_return:
      "女子看见自然万物都有边界，却感到人的反复或自己的怨苦仿佛没有边",
    next_use:
      "C606允许旁白保留所选解释；全文知识收纳将本句作为多义比兴/反衬示例",
    deletion_loss:
      "删除会把有岸有泮变成孤立译文或现代口号，学生既不知道两种教材解释，也不能学习如何比较多义诗句",
    merge_test:
      "不能并入C602：本页需要个人双解释和小组证据比较，时间与社会结构均不同于同词对读",
    visual_duty:
      "以自然边界的对称词居中，留出两个未命名解释方向供学生生成和比较",
    interaction_signature: {
      cognitive_action: "竞争解释与前后文比较",
      sensory_channel: "默读、双解书写、证据连线",
      social_structure: "个人首解—四人证据席—个人排序",
      artifact_form: "双解释与保留分歧",
      emotional_rhythm: "自然有界，人事意义悬而未决",
    },
    first_person_reception:
      "我能提出并比较两种解释，知道诗句不是一对一密码；我可以选择更有说服力的一种，也能说明另一种为何成立。",
    screen: {
      kind: "open",
      focus: "淇则有岸，隰则有泮。",
      gloss: "隰 xí：低湿的地方｜泮 pàn：同‘畔’，边、岸",
      prompt: "为什么在‘偕老／怨’之后，忽然写淇与隰的岸和泮？它怎样接前句，也怎样照见后文？",
    },
    script: {
      teacher_spoken:
        "先把字面说准：隰读xí，是低湿的地方；泮读pàn，同畔，是边、岸。淇水有岸，低湿地有边。请先独立写一种可能：诗为什么在偕老与怨之后忽然说自然有界？你的解释要接回前一句或后面的回忆。（等待首解。）四人组轮流只读自己的解释和所接原句；听到不同想法，再补第二种。组内不要投票，把两种解释分别问清：它靠哪个词，怎样接前后文？最后每个人给更能说服自己的一个轻轻加圈，也可以并列，但要写保留理由。（等待。）教材允许两种理解：可反衬男子心意无常、没有限制；也可反衬女子若偕老将产生无边怨苦。它们不是随意猜测，都要经过全章语境。这里不要直接改写成现代口号‘做人要有边界’；先让诗自己的怨、反与信誓说话。",
      scene:
        "屏幕只显示原句、词义和开放问题；学生先个人写，四人组交流时屏幕不出现两种成品解释，教师最后才归纳。",
      stage_directions: [
        "个人字面口译",
        "教师校音释义",
        "个人写第一种解释",
        "四人轮读证据",
        "每人补第二种解释",
        "个人排序或并列",
        "教师后置多解",
      ],
      timeboxes: [
        { label: "口译与词义", seconds: 55 },
        { label: "个人第一种解释", seconds: 75 },
        { label: "四人证据轮读", seconds: 85 },
        { label: "个人补解和排序", seconds: 70 },
        { label: "公开两种衔接", seconds: 35 },
        { label: "教师后置归纳", seconds: 40 },
      ],
      branches: [
        {
          kind: "直接写现代边界",
          response:
            "追问原句在偕老、怨和后文誓言之间怎样衔接，先恢复诗内意义。",
        },
        {
          kind: "只有一种解释",
          response: "先保留，听见同伴或教师后再补第二种，不要求假装认同。",
        },
        {
          kind: "用人数判对错",
          response: "取消表决，只比较各自接哪一句、靠哪个词。",
        },
      ],
      listener_task: "只追问解释的前后文落点和原词，不替全班选唯一答案。",
      evidence_location: "06F C603区",
      cut_line:
        "自然边界之后，时间突然退回少年。她为什么在最痛的时候，还把当初的言笑和信誓完整地记起？",
    },
  }),
  page({
    page_id: "C604",
    title: "总角之宴｜信誓旦旦",
    minutes: 6,
    source_line_refs: ["L028", "L029"],
    original_text: `${lineMap.L028}。${lineMap.L029}。`,
    literary_object:
      "少年和悦记忆与诚恳誓言被当下违誓重新核验的时间回环，以及共同记忆既真实又不能抵消后来的行为",
    current_difficulty:
      "学生可能把美好回忆当成关系本来很好，或反过来把它全部判成伪装；都没有区分当时真实经验与后来违誓责任",
    unique_function:
      "借‘旧日相册—今日核验’双栏，让学生保存一份真实美好，同时用后文事实说明它不能替后来的行为免责",
    visible: `${lineMap.L028}。\n${lineMap.L029}。\n\n总角：少年时代　宴：欢乐\n晏晏：和悦的样子　旦旦：诚恳的样子\n反：违背\n\n她记住了什么？\n如今再看，这些旧事让她明白什么？`,
    first_glance:
      "两句与词义在先，问题分开记忆和核验；不显示全是伪装或美好能抵消伤害的结论",
    information_state: {
      known: "当下已有长期劳作、粗暴、反复和孤立事实",
      reveal_now:
        "总角、宴、晏晏、旦旦、反的意义；旧日言笑/信誓与今日违誓的时间对照",
      defer:
        "停止判断由C605在核验后生成；共同记忆如何增加退出难度在全文三问综合",
    },
    student_action: [
      "个人把两句分写为她确实记住的旧日经验与今天核验出的行为事实",
      "同桌各挑一句越界说法‘全是假的/曾经美好所以应继续’，作者用原词改成同时容纳真实记忆和违誓责任的句子",
    ],
    artifact: "06F C604区的旧日相册、今日核验和一条双真相修订句",
    normal_path:
      "认为旧日也可能有表象者可以保留可能，但不能抹去叙述者记得的言笑晏晏；不愿判断动机只写经验与行为即可",
    bounded_feedback:
      "同桌只圈抹除旧日经验或用旧日替后来免责的词；教师不推断当初誓言主观真伪",
    revision:
      "学生把全是假象或既有美好就应坚持改为曾有和悦经验/誓言诚恳呈现，但后来行为违背",
    teacher_synthesis:
      "诗保存少年言笑与信誓的真实记忆，同时用不思其反核验后来违背；记忆可解释为何难舍，却不能抵消失信责任",
    story_return:
      "她没有删除曾经的欢乐和誓言，正因为记得清楚，后来违背才被看得更清楚",
    next_use:
      "C605以信誓/反/不思回环形成停止判断；全文第三问区分沉没投入与造成伤害",
    deletion_loss:
      "删除会使结尾变成忘掉过去才能停止，或把美好回忆变成继续承受的理由，失去全诗复杂真实",
    merge_test:
      "不能并入C605：本页必须先保存旧日经验并完成行为核验，下一页才有资格读停止判断及其声音",
    visual_duty:
      "用旧日相册与今日核验两栏承载时间对照，使记忆与责任同时可见而不相互抵消",
    interaction_signature: {
      cognitive_action: "双真相保存与行为核验",
      sensory_channel: "双栏书写、原词修订",
      social_structure: "个人双栏—同桌越界词核查",
      artifact_form: "旧日/今日双真相句",
      emotional_rhythm: "温暖记忆越清楚，违背越清楚",
    },
    first_person_reception:
      "我没有把过去全判成假，也没有用过去的美好替后来免责；我能同时保存记忆和违誓事实。",
    screen: {
      kind: "split",
      left_label: "她记住的旧日",
      left_lines: ["总角之宴，言笑晏晏。"],
      right_label: "如今再看",
      right_lines: ["信誓旦旦，不思其反。"],
      gloss: "总角：少年时代｜宴：欢乐｜晏晏：和悦｜旦旦：诚恳｜反：违背",
      prompt: "记忆是真的；后来什么也是真的？",
    },
    script: {
      teacher_spoken:
        "先把词说准：总角是少年时代；宴是欢乐；晏晏是和悦的样子；旦旦是诚恳的样子；反是违背。现在把纸分成两栏：左边只写她确实记住了什么，右边只写今天核验出了什么行为事实。不要先判断当初内心是真是假。（等待。）同桌交换，各找一种越界：如果写‘过去全是假的’，问言笑晏晏在叙述者记忆里是否真实；如果写‘曾经美好，所以还应该坚持’，问不思其反能否被过去抵消。作者自己改成一句能同时容纳两件真的话。（等待。）我们听两句。她保存少年欢乐和当初信誓，也确认后来行为违背。共同记忆可以解释为什么难以割舍，却不能替失信免责。正因为她记得信誓旦旦，‘反’才如此清楚。",
      scene:
        "屏幕左右为旧日相册和今日核验；学生个人先写，教师不讨论男子当初主观真伪，只守经验与行为事实。",
      stage_directions: [
        "个人口译两句",
        "教师校词",
        "个人完成旧日/今日双栏",
        "同桌圈两类越界词",
        "作者写双真相句",
        "公开听两句",
        "教师后置责任边界",
      ],
      timeboxes: [
        { label: "口译与词义", seconds: 70 },
        { label: "个人双栏", seconds: 85 },
        { label: "同桌越界核查", seconds: 55 },
        { label: "作者修订", seconds: 55 },
        { label: "公开抽样与归纳", seconds: 65 },
        { label: "转场", seconds: 30 },
      ],
      branches: [
        {
          kind: "断言过去全假",
          response: "把主观动机改为叙述者确实保存的言笑晏晏与信誓旦旦。",
        },
        {
          kind: "美好成为继续理由",
          response: "补回不思其反，区分为何难舍与后来行为责任。",
        },
        {
          kind: "追问当初誓言真假",
          response:
            "允许保留问题，诗只提供誓言呈现与后来违背，不直接证明当初心理。",
        },
      ],
      listener_task:
        "只核查是否抹除真实记忆或用记忆替后来免责，不判断当初动机。",
      evidence_location: "06F C604区",
      cut_line:
        "旧日没有被删掉，违誓也没有被稀释。最后一句便不再是突然的口号：她把‘反’和‘不思’再说一次，然后说‘亦已焉哉’。",
    },
  }),
  page({
    page_id: "C605",
    title: "反是不思，亦已焉哉",
    minutes: 7,
    source_line_refs: ["L029", "L030"],
    original_text: `${lineMap.L029}。${lineMap.L030}。`,
    literary_object:
      "信誓/反/不思的回环核验，亦已焉哉的停止意义、语气多层和实际行动边界",
    current_difficulty:
      "学生容易把末句只读成爽快决绝，或直接叙述女子已离家成功；也可能只读成无力悲伤，忽略判断已经形成",
    unique_function:
      "先从两句重复词读出核验链，再让两种声线完成公开盲听与个人二次选择，最终准确写出停止判断而非补造行动",
    visible: `${lineMap.L029}。\n${lineMap.L030}！\n\n是：这，指誓言　已：止、了结\n焉、哉：语气词，连用加强收束\n\n哪些词一再回来？\n再把末句读成两种声音：你分别听见什么？`,
    first_glance:
      "两句完整并列与最低词义主位，不在标题中宣布觉醒、离开或胜利；允许疲惫克制与清醒决绝并存",
    information_state: {
      known: "旧日言笑与信誓已被保存，后来违誓已核验",
      reveal_now:
        "反、不思的回环，已、焉、哉的意义，停止判断的形成与两种朗读可能",
      defer: "诗没有写实际离家、离开方式和后来生活；全文三问再讨论现实阻力",
    },
    student_action: [
      "圈出信誓/反/不思的前后照应，用自然话写停止判断如何形成",
      "同一句分别读成疲惫克制和清醒决绝，听者只报实际听见；个人选择或融合后改读并写事实边界",
    ],
    artifact:
      "06F C605区的回环词、停止判断句、双声听感、个人改读和‘诗写/未写’边界",
    normal_path:
      "两种都听不出者可先准确平读；认为两种兼有者写先后层次；不要求每人公开朗读",
    bounded_feedback:
      "听者只写实际听见的声音和原词位置，不评最佳；教师明确停止判断/实际离开边界",
    revision:
      "学生依据听感改一处停顿重音，将她已成功离开改为她形成到此为止的判断，后续行动未写",
    teacher_synthesis:
      "反与不思回环核验违誓，亦已焉哉形成停止判断；语气可含疲惫、痛、清醒、决绝，但实际离开及后来生活不在诗中",
    story_return: "回看欢乐与誓言、确认违背之后，她终于说：这段关系到此为止",
    next_use:
      "C606撤答重建第六章与故事轨道终格；全文第一问写到停止判断，第三问讨论停止后可能面对的结构阻力",
    deletion_loss:
      "删除会让结尾事实、声音和伦理边界混为一谈：或只剩励志决绝，或把停止判断误写成已完成离开",
    merge_test:
      "不能并入C604：旧日记忆和违誓核验必须先完成，末句才可进行双声体验与事实边界判断",
    visual_duty:
      "将两句回环置于同一视野，并给双声朗读留白；最终把‘诗写/未写’边界落在学习单而非屏幕答案",
    interaction_signature: {
      cognitive_action: "回环核验、双声实验与事实边界",
      sensory_channel: "圈词、双声朗读、闭眼听、改读",
      social_structure: "个人生成—双人盲听—个人定稿",
      artifact_form: "停止判断与双声修订",
      emotional_rhythm: "痛与倦沉到底，判断在收束中站起",
    },
    first_person_reception:
      "我从重复词读出她不是突然喊口号；我试过两种声音，并能准确说诗写了停止判断，却没有写完她怎样离开。",
    screen: {
      kind: "compare",
      left_label: "信誓",
      left_lines: ["信誓旦旦，不思其反。"],
      right_label: "收束",
      right_lines: ["反是不思，亦已焉哉！"],
      gloss: "是：这，指誓言｜已：止、了结｜焉、哉：连用加强收束",
      prompt: "哪些词一再回来？再把末句读成两种声音。",
    },
    script: {
      teacher_spoken:
        "把两句并在一起读。圈出回来一次又一次的词：信誓、反、不思。‘是’指这，指誓言；‘已’是止、了结；焉、哉两个语气词连用，加强收束。请先用自然话写清：她经过什么核验，才说到此为止？（等待。）现在做两种声音实验。同一句‘反是不思，亦已焉哉’，第一遍读得疲惫、克制，像把许多话沉下去；第二遍读得清醒、决绝，像判断终于站稳。两人轮换，听者闭眼，只报实际听见什么，以及在已、焉、哉哪处听见；不要评谁最好。（等待双声与改读。）每个人最后可以选择一种，也可以写两种声音先后交叠，再只改一处。最后写边界：诗写出了什么，没有继续写什么。请把‘她已经离家并开始新生活’改回文本：她形成停止这段关系的判断；怎样实际离开、后来怎样生活，诗没有叙述。她的清醒不因现实行动未写而减少，阅读的诚实也不能因我们希望她离开就补写结局。",
      scene:
        "屏幕两句并列；学生先圈回环词和写判断链，双人完成两种声音的盲听，边界写在学习单，不上屏预给。",
      stage_directions: [
        "并读两句并圈回环词",
        "个人写判断形成链",
        "双人第一种声线",
        "交换第二种声线",
        "听者只报听感位置",
        "个人选择或融合并改读",
        "写诗写/未写边界",
      ],
      timeboxes: [
        { label: "词义与回环定位", seconds: 70 },
        { label: "个人判断链", seconds: 70 },
        { label: "双声盲听", seconds: 100 },
        { label: "个人改读", seconds: 55 },
        { label: "事实边界写作", seconds: 65 },
        { label: "分享归纳与转场", seconds: 60 },
      ],
      branches: [
        {
          kind: "只读爽快决绝",
          response:
            "保留，再试一次疲惫克制，比较已、焉、哉的收束是否多出层次。",
        },
        {
          kind: "只读无力悲伤",
          response: "保留痛与倦，再回到已的停止义，看判断是否已经形成。",
        },
        {
          kind: "补写实际离开",
          response: "将事实降回形成停止判断；行动方式和后来生活标为诗未写。",
        },
      ],
      listener_task:
        "只报实际听见的声音及原词位置，不选择最佳演法；核查停止判断与实际行动是否混淆。",
      evidence_location: "06F C605区",
      cut_line:
        "结尾已经逐字走到。现在收起所有局部解释，看看能否从偕老愿望一路讲到亦已焉哉，并把六章故事真正合拢。",
    },
  }),
  page({
    page_id: "C606",
    title: "把第六章讲成她最后一次回望",
    minutes: 7,
    source_line_refs: chapter.line_ids,
    original_text: CHAPTER_TEXT.join("。") + "。",
    literary_object:
      "第六章完整原诗及偕老反折、自然边界多解、少年记忆、违誓核验和停止判断的连续形成",
    current_difficulty:
      "学生可能分别记住多义、双声和边界，却不能离开支架说明她为何要回到旧事、停止判断如何形成",
    unique_function:
      "完整重读后撤去全部支架，用四十秒旁白讲清旧愿—旧事—核验—停止，再恢复六张章末卡排成一条母轨道并连说六章",
    visible: `把第六章讲成她最后一次回望\n\n${CHAPTER_TEXT.map((x) => `${x}。`).join("\n")}\n\n旧愿怎样反折？\n她重新看见什么？\n最后作出怎样的判断？`,
    first_glance:
      "整章原诗重新主位，三个自然问题限定旁白；随后合书、翻背材料、熄屏检索",
    information_state: {
      known: "五句字词、声音、多解和事实边界已生成",
      reveal_now: "撤答后能否将停止形成过程讲完整并与前五章接通",
      defer: "全文三问、婚姻结构讨论和知识收纳在后续模块完成",
    },
    student_action: [
      "完整重读后合书、翻背全部材料、熄屏，用四十秒讲旧愿—旧事—核验—停止",
      "听者只报一个断点，讲述者返诗补说并写第六格",
      "按一至六章恢复六张章末卡排成母轨道，每人沿轨道连续讲述",
    ],
    artifact: "第六章旁白、一次查漏补说、第六格、按序排好的六章母轨道和一段六章连续人生",
    normal_path:
      "讲不全者从亦已焉哉往前找理由；听者没有遗漏如实确认；缺一张章末卡者借同桌核对后在临时便笺补一格，不假装材料齐全",
    bounded_feedback:
      "听者只核对三层和停止边界，不代讲；教师只修事实、顺序和多解边界",
    revision:
      "讲述者定位断点后合书补说，用自然话写第六格；恢复六张卡后本人按真实断点补说，准确者可不改；把实际离开改回停止判断",
    teacher_synthesis:
      "引用两条章意，收束为旧愿反折、自然反衬、少年和誓言回看、违誓核验、停止判断；不替学生统一末句声线",
    story_return:
      "她把曾经的偕老、言笑和信誓一一看清，在违誓事实前作出到此为止的判断",
    next_use:
      "全文S01直接读取桌面六章母轨道回答经历；S02/S03读取生活与责任证据；末句边界贯穿现实讨论",
    deletion_loss:
      "没有撤答重建，第六章仍会散成多义句与朗读活动，全诗也不能从相识迁嫁连续走到停止判断",
    merge_test:
      "不能并入C605：C605在两句支架下完成声音和边界，本页切换为全支架撤除、全章与全诗重建",
    visual_duty: "先让整章和三层旁白范围收束，再以一条连续章序提示学生恢复真实六张材料，不用六个空框假装作品",
    interaction_signature: {
      cognitive_action: "撤答重建与全诗接续",
      sensory_channel: "完整重读、熄屏旁白、六格连讲",
      social_structure: "个人旁白—同桌查漏—全班抽样",
      artifact_form: "第六格与六章人生旁白",
      emotional_rhythm: "旧事完成核验，全诗安静合拢",
    },
    first_person_reception:
      "我撤去提示后仍能讲清她为什么回望旧事、怎样核验违誓、最后作出什么判断；我又亲手把六张章末卡排成一条母轨道，沿真实材料连讲六章。",
    screen: {
      kind: "rebuild",
      prompts: ["旧愿怎样反折？", "她重新看见什么？", "最后作出怎样的判断？"],
      rail: "故事轨道｜第六格",
    },
    script: {
      teacher_spoken:
        "第六章已经逐句走过。请完整重读一遍，让老字的反折、自然边界、少年言笑、信誓与末句依次回来。（读完。）现在合上教材，翻背全部学习卡，同桌互看桌面没有原诗，我按B键熄暗屏幕。用四十秒讲三层：旧愿怎样反折；她重新看见什么；最后作出怎样的判断。听者只报一个断点，没有就说完整。交换。（等待。）讲述者只开教材找遗漏句，合书补说。现在翻回06F写第六格。（等待。）接下来恢复真实材料：从个人故事夹中取出第一至第六章六张章末卡，按章序在桌面排成一列。跨课时由每组材料袋收存，下一课课前原组返还；此刻若缺一张，不凭记忆假装齐全，向同桌借读对应章意，在临时便笺补一个替代格。请先自己沿六格低声连说六十秒，再讲给同桌听；听者只指出一个真正断点，没有断点就说出最清楚的一处因果，不制造错误。作者只在有断点时返诗补说。（等待。）谁愿意让全班听一段六章人生？（引用，修事实边界。）她不是忘掉过去才停止，而是把过去与今天一一核验以后，说出亦已焉哉。诗写停止判断，没有写完现实行动。六张卡保持原序，下一页第一问会直接读取这条母轨道。",
      scene:
        "屏幕先供完整重读；第六章检索时撤去教材、全部卡片和投影。完成第六格后，学生从个人故事夹恢复六张章末卡，按一至六章横向排成真实母轨道；屏幕只显示章序，不显示六个假作品框。",
      stage_directions: [
        "完整重读第六章",
        "合书翻背全部材料",
        "按B键熄屏",
        "双方各讲四十秒",
        "返诗定位后合书补说",
        "写第六格",
        "从故事夹恢复六张章末卡并按序排开",
        "个人先沿六格低声连说",
        "同桌沿母轨道互讲并按真实断点反馈",
        "全班听一段完整作品",
      ],
      timeboxes: [
        { label: "完整重读", seconds: 45 },
        { label: "撤去支架", seconds: 30 },
        { label: "双方旁白", seconds: 90 },
        { label: "返诗补说", seconds: 35 },
        { label: "写第六格", seconds: 35 },
        { label: "恢复六张卡并排成母轨道", seconds: 30 },
        { label: "个人低声连说与同桌互讲", seconds: 115 },
        { label: "真实断点反馈、全班作品与转场", seconds: 40 },
      ],
      branches: [
        {
          kind: "只讲末句",
          response: "从末句往前找它依赖的旧愿、旧事和违誓核验。",
        },
        {
          kind: "把过去全抹掉",
          response: "补回总角言笑和信誓，它们真实存在但不替后来免责。",
        },
        { kind: "写成实际离开", response: "改回形成停止判断；现实行动未写。" },
        { kind: "章末卡缺失", response: "借同桌核对对应章意，在临时便笺补一个替代格；课后再补齐个人故事夹。" },
      ],
      listener_task:
        "先核对旧愿、旧事、核验、停止是否连成过程；六章互讲时只报一个真实断点或最清楚的因果，并检查是否越过实际行动边界。",
      evidence_location: "06F C606区、按序排开的六张章末卡、临时缺卡便笺和六章连讲",
      cut_line:
        "六张卡保持原序。下一页先沿这条人生轨道回答：她经历了什么？",
    },
  }),
];
const materials = [
  {
    material_id: "CH6-F",
    file_role: "chapter6_progressive_close_reading_and_story_rail",
    first_distribution_event: "C601_AFTER_COMPLETE_READ",
    visible_when_distributed: "C601初稿区；其余逐栏展开",
    information_boundary:
      "首次不提前显示两种边界解释、旧事核验结论、停止判断或实际行动边界答案",
  },
];
const payload = {
  schema_version: "1.1",
  module_id: "MENG_V63_CHAPTER_6",
  version: "6.3-chapter6-six-event",
  status: "implementation_candidate",
  module: "chapter_6",
  prerequisite_module: "MENG_V63_CHAPTER_5",
  next_module: "MENG_V63_SYNTHESIS",
  total_minutes: pages.reduce((a, b) => a + b.minutes, 0),
  chapter_text: CHAPTER_TEXT,
  materials,
  pages,
};
if (require.main === module)
  process.stdout.write(`${JSON.stringify(payload)}\n`);
module.exports = payload;
