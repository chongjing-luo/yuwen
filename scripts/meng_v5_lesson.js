"use strict";

const THREE_QUESTIONS = [
  "女主人公经历了怎样的关系与婚姻过程？",
  "她的不幸婚姻，在现实生活中表现为哪些现象？",
  "诗把失信、粗暴和关系失衡的直接责任指向哪里？哪些信息、投入、支持和时代条件使这段关系更难及时停止？",
];

const modules = [
  { id: "M1", number: "一", title: "从旧故事走进初见", minutes: 47, safeStop: "首次听读后／第一章章结后" },
  { id: "M2", number: "二", title: "等待与回望中的劝诫", minutes: 49, safeStop: "第二章章结后／第三章章结后" },
  { id: "M3", number: "三", title: "婚后事实与长期处境", minutes: 52, safeStop: "第四章章结后／第五章章结后" },
  { id: "M4", number: "四", title: "核验誓言，回收前两问", minutes: 45, safeStop: "第六章章结后／第一问回收后" },
  { id: "M5", number: "五", title: "责任、困境与最终收纳", minutes: 37, safeStop: "责任线与困境线后／知识收纳后" },
];

const chapters = [
  {
    id: "C1", number: 1, label: "第一章", module: "M1", title: "相识、求婚与婚期",
    text: "氓之蚩蚩，抱布贸丝。匪来贸丝，来即我谋。\n送子涉淇，至于顿丘。匪我愆期，子无良媒。\n将子无怒，秋以为期。",
    actionChain: "接近 → 求婚 → 远送 → 说明条件 → 约定婚期",
    summary: "男子以贸丝为表面来意接近并求婚；女子远送、说明媒妁条件，又在安抚中约定秋期。",
    keyLines: [2, 5],
    lines: [
      { original: "氓之蚩蚩，抱布贸丝", translation: "那个人看起来忠厚，抱着布来换丝。", keywords: "氓 méng：这里指男子；蚩蚩：忠厚的样子；贸：交换。", action: "男子以贸丝的姿态出现并接近。", voice: "出场朴实、近乎无害。", form: "赋；用人物神态与动作开场。", q: "Q1 相识；Q3 初期外在印象。" },
      { original: "匪来贸丝，来即我谋", translation: "并非真来换丝，而是来找我商量婚事。", keywords: "匪：同“非”；即：走近、到；谋：商量，这里指商量婚事。", action: "叙述揭开贸丝背后的求婚来意。", voice: "主动、急切；表面来意与真实来意出现差别。", form: "“匪……来……”否定转折，使真实目的突然显出。", q: "Q2 表面来意与真实来意有别；Q3 初期信息有限。", key: "第一次读可以感到主动热烈；全文后再问：间接接近是否也需要更审慎地观察？文本能证明来意有别，不能证明完整人格是有计划伪装。" },
      { original: "送子涉淇，至于顿丘", translation: "我送你渡过淇水，一直送到顿丘。", keywords: "涉：渡过；至于：到达。", action: "女子把男子送过淇水，送到顿丘。", voice: "亲近、投入、不舍；行动比抽象形容更直接。", form: "空间逐步拉长，写出关系升温。", q: "Q1 关系升温；Q3 情感投入开始。" },
      { original: "匪我愆期，子无良媒", translation: "不是我故意拖延，是你没有合适的媒人。", keywords: "愆 qiān：拖延；良媒：合适的媒人。", action: "女子解释未能立即成婚的原因。", voice: "既亲近，又努力保留婚姻程序和条件。", form: "再次用“匪”解释；“我/子”形成直接对话。", q: "Q1 议婚；Q3 女子原本并非没有审慎边界。" },
      { original: "将子无怒，秋以为期", translation: "请你不要生气，就把秋天定作婚期。", keywords: "将 qiāng：愿、请；以……为：把……定作。", action: "女子安抚对方，同时给出明确婚期。", voice: "安抚、让步和条件同时存在。", form: "祈请语气与承诺并置，使关系张力进入声音。", q: "Q2 她需要安抚对方情绪；Q3 全文后重评“无怒”。", key: "“无怒”提示男子的愤怒已经进入现场或女子预期，但程度未写明。它是全文后需要重评的模糊细节，不足以反推女子当时已经掌握全部风险。" },
    ],
    activity: {
      title: "第一次看：这些行动给你什么印象？",
      prompt: "从“蚩蚩、贸丝、谋、无怒”中任选两处：只看第一章，你怎样理解男子的接近方式？",
      workspace: "原词：__________　我此刻的理解：________________\n原词：__________　我仍想追问：________________",
      returnTitle: "先保存第一印象，不急着定性",
      returnItems: ["憨厚、主动、热烈、执着，都可能是第一次阅读的真实印象。", "“贸丝/谋”“无怒”留下了尚未解释完的细节。", "等读完婚后经历，再回来判断这些细节的意义。"],
    },
  },
  {
    id: "C2", number: 2, label: "第二章", module: "M2", title: "等待、占卜与迁嫁",
    text: "乘彼垝垣，以望复关。不见复关，泣涕涟涟。\n既见复关，载笑载言。尔卜尔筮，体无咎言。\n以尔车来，以我贿迁。",
    actionChain: "登墙望 → 不见而泣 → 既见而笑 → 卜筮 → 迁嫁",
    summary: "女子的视线和情绪围绕复关迅速变化；卜筮无不吉后，她带着财物乘车迁嫁。",
    keyLines: [2, 3],
    lines: [
      { original: "乘彼垝垣，以望复关", translation: "登上那堵残破的墙，来眺望复关。", keywords: "乘：登上；垝垣 guǐ yuán：残破的墙；以：来。", action: "女子登高远望。", voice: "期待中带着焦灼。", form: "动作和视线共同拉开等待的空间。", q: "Q1 等待成婚。" },
      { original: "不见复关，泣涕涟涟", translation: "看不见复关，就泪流不断。", keywords: "泣涕：流泪；涟涟：泪流不断的样子。", action: "未见来人，女子哭泣。", voice: "失落、无助，时间被拉慢。", form: "“不见”触发“泣”；叠词“涟涟”延长情绪。", q: "Q2 情绪高度受关系进展牵动。", key: "不要只说“痴情”。先读出“不见”这一条件，再听“涟涟”怎样把等待拉长。" },
      { original: "既见复关，载笑载言", translation: "已经看见复关，便又笑又说。", keywords: "既：已经；载……载……：又……又……。", action: "见到来人后，女子转哭为笑。", voice: "情绪突然释放，声音变快变亮。", form: "“不见/既见”“泣/笑”正面对照；反复“载”加强动作。", q: "Q1 等待出现转折；Q3 情感投入很深。", key: "把前后两句连读：同一个“见”字改变情绪速度。诗没有解释全部心理，却用动作让依赖感可听见。" },
      { original: "尔卜尔筮，体无咎言", translation: "你用龟甲、蓍草占卜，卦象没有不吉利的话。", keywords: "卜：用火灼龟甲看裂纹；筮 shì：用蓍草占卜；体：卦象；咎：灾祸。", action: "男子以当时婚俗方式确认吉凶。", voice: "双方期待获得确定性。", form: "“尔”反复，叙事转入婚俗程序。", q: "Q1 婚前准备；现代延伸只比较仪式确定与长期行动。" },
      { original: "以尔车来，以我贿迁", translation: "你用车来接我，我带着财物嫁过去。", keywords: "贿：财物，这里指嫁妆；迁：迁往男子家。", action: "男子来迎，女子携财物迁嫁。", voice: "信任、期待与人生转折同时发生。", form: "“以尔/以我”对称，写出双方行动。", q: "Q1 成婚迁嫁；Q3 情感与生活资源投入。" },
    ],
    activity: {
      title: "让等待拥有两种速度",
      prompt: "排列“望—不见—泣—见—笑—迁”，为前半和后半各设计一种速度、停顿与重音。",
      workspace: "慢下来的一处：__________　因为：________________\n加快的一处：__________　因为：________________",
      returnTitle: "动作顺序就是情绪过程",
      returnItems: ["望—不见—泣：视线受阻，时间和声音都被拉长。", "见—笑—言：信息突然改变，情绪快速释放。", "迁嫁不是孤立事件，而是等待获得确定后的行动结果。"],
    },
  },
  {
    id: "C3", number: 3, label: "第三章", module: "M2", title: "桑叶、斑鸠与回望中的劝诫",
    text: "桑之未落，其叶沃若。于嗟鸠兮，无食桑葚！\n于嗟女兮，无与士耽！士之耽兮，犹可说也。\n女之耽兮，不可说也！",
    actionChain: "桑叶丰润 → 劝鸠勿食 → 劝女勿耽 → 比较男女处境",
    summary: "叙事暂时停下，回望中的女子由桑叶和斑鸠起兴，转向对情感沉溺及其不平等后果的劝诫。",
    keyLines: [1, 3],
    lines: [
      { original: "桑之未落，其叶沃若", translation: "桑叶还没有落下时，叶子润泽鲜嫩。", keywords: "沃若：润泽鲜嫩的样子。", action: "叙事暂停，镜头转向丰润桑叶。", voice: "明亮、丰盈，又因回望而隐含不安。", form: "兴，也可引发比的联想；意义须由上下文筛选。", q: "Q1 婚前或青春阶段的可能联想。", key: "先感受色泽和质地，再命名“比兴”。桑叶可以联想到青春、感情或关系状态，但没有固定的一对一密码。" },
      { original: "于嗟鸠兮，无食桑葚", translation: "唉，斑鸠啊，不要贪吃桑葚。", keywords: "于嗟 xū jiē：感叹词；鸠：斑鸠；桑葚：桑树果实。", action: "诗中声音转为对斑鸠的呼告。", voice: "叹息、警醒。", form: "由物起兴；呼告让劝诫突然进入。", q: "为下一句由物及人作准备。" },
      { original: "于嗟女兮，无与士耽", translation: "唉，女子啊，不要同男子沉溺情爱。", keywords: "耽：沉溺。", action: "劝诫对象由斑鸠转为女子。", voice: "后见之明、自警和痛惜并存。", form: "“于嗟”反复；由物到人的类比推进。", q: "Q2 情感沉溺后的处境；Q3 投入使停止更难。", key: "“耽”不是嘲笑爱得深，而是回望者对失去判断空间的警惕。现代所说的确认偏向只能到全文后再使用，不能把她的投入变成男子粗暴的原因。" },
      { original: "士之耽兮，犹可说也", translation: "男子沉溺情爱，尚且可以脱身。", keywords: "说 tuō：同“脱”，摆脱。", action: "叙述者开始比较男女沉溺后的处境。", voice: "不平与清醒。", form: "与下一句构成性别处境对照。", q: "Q2 脱身代价并不相等；Q3 权力和时代条件。" },
      { original: "女之耽兮，不可说也", translation: "女子沉溺情爱，往往难以脱身。", keywords: "说 tuō：同“脱”；不可：难以。", action: "劝诫最终落回女子自身处境。", voice: "沉痛、警醒，感叹语气收束。", form: "“士/女”“可/不可”正面对照。", q: "Q2 情感与结构性困境；Q3 时代不平等。" },
    ],
    activity: {
      title: "桑叶首先让你看见什么？",
      prompt: "先写“沃若”的颜色、质地和生命状态，再提出两种可能联想；暂不选择唯一答案。",
      workspace: "感官词：__________ / __________\n可能联想A：____________　依据：____________\n可能联想B：____________　依据：____________",
      returnTitle: "把解释保存成假设",
      returnItems: ["桑叶先是可感的颜色、质地和生命状态。", "青春、情感、关系都可以成为联想方向。", "第四章“黄而陨”出现后，再用位置、对照和叙事筛选。"],
    },
  },
  {
    id: "C4", number: 4, label: "第四章", module: "M3", title: "桑叶转黄与责任判断",
    text: "桑之落矣，其黄而陨。自我徂尔，三岁食贫。\n淇水汤汤，渐车帷裳。女也不爽，士贰其行。\n士也罔极，二三其德。",
    actionChain: "桑叶坠落 → 多年食贫 → 渡淇回忆 → 辨明责任 → 指出反复",
    summary: "桑叶由丰润转为枯黄，婚后贫困和渡淇场景进入回忆；叙述者明确指出自己无过而男子反复失信。",
    keyLines: [1, 4],
    lines: [
      { original: "桑之落矣，其黄而陨", translation: "桑叶落下，已经枯黄坠落。", keywords: "陨：坠落。", action: "桑叶状态由丰润转为枯黄坠落。", voice: "画面骤冷，叙事进入婚后回顾。", form: "与“其叶沃若”形成色彩、状态和位置对照。", q: "Q1 婚后转折；意象解释须保持开放。", key: "把第三章的“沃若”和此处“黄而陨”并置：青春、感情、关系状态都获得更多语境支持，但仍不能把桑叶压成一个固定答案。" },
      { original: "自我徂尔，三岁食贫", translation: "自从我嫁到你家，多年来生活贫苦。", keywords: "徂 cú：往；尔：你家；三岁：多年；食贫：过贫苦生活。", action: "女子回顾迁嫁后的长期贫困。", voice: "克制叙述中积累着艰辛。", form: "“三岁”压缩多年时间。", q: "Q1 迁嫁食贫；Q2 长期生活压力。" },
      { original: "淇水汤汤，渐车帷裳", translation: "淇水浩荡，浸湿了车上的帷幔。", keywords: "汤汤 shāng shāng：水势浩大；渐 jiān：浸湿；帷裳：车旁帷幔。", action: "回忆中的车经过淇水，帷幔被浸湿。", voice: "水势、湿冷和艰难进入画面。", form: "叠词和空间意象组织回忆。", q: "方向和归途并未写明，保持开放。" },
      { original: "女也不爽，士贰其行", translation: "女子没有差错，男子的行为却前后不一。", keywords: "爽：差错；贰：不专一、前后不一。", action: "叙述者从经历陈述转为明确责任判断。", voice: "控诉、辨明，不再只自悼。", form: "“女/士”“不爽/贰”并置，责任由语言直接显出。", q: "Q2 婚前婚后不一；Q3 男子失信责任。", key: "这不是旁观者替她判定，而是第一人称回望中的自我辨明。先区分“食贫、渡水”等经历事实，再看“不爽/贰”怎样作出责任判断。" },
      { original: "士也罔极，二三其德", translation: "男子的行为没有准则，品德反复无常。", keywords: "罔极：没有准则；二三：反复无常，这里是数词活用。", action: "女子进一步概括男子反复的行为。", voice: "失望、指责。", form: "与上句连续判断；“二三”把反复凝成一个动作感。", q: "Q2 行为反复；Q3 失信责任。" },
    ],
    activity: {
      title: "哪些是事实，哪些是责任判断？",
      prompt: "把本章诗句放入“经历事实”和“责任判断”两栏，并说明判断由哪组对照形成。",
      workspace: "经历事实：____________________________\n责任判断：____________________________\n语言依据：____________________________",
      returnTitle: "事实与判断并不混在一起",
      returnItems: ["食贫、淇水、车帷被浸，是叙述中的经历。", "“女也不爽，士贰其行”直接辨明双方责任。", "现代评价可以继续讨论，但必须先站稳诗中的事实和判断。"],
    },
  },
  {
    id: "C5", number: 5, label: "第五章", module: "M3", title: "长期劳动、粗暴与孤立",
    text: "三岁为妇，靡室劳矣。夙兴夜寐，靡有朝矣。\n言既遂矣，至于暴矣。兄弟不知，咥其笑矣。\n静言思之，躬自悼矣。",
    actionChain: "多年为妇 → 早起晚睡 → 遭遇粗暴 → 家人讥笑 → 独自悲悼",
    summary: "多年劳动被压进日复一日的早起晚睡；男子愿望满足后转为粗暴，家人不理解，女子只能独自反思悲悼。",
    keyLines: [2, 3],
    lines: [
      { original: "三岁为妇，靡室劳矣", translation: "多年来做妻子，家里的劳苦没有不做的。", keywords: "靡：没有；室劳：家务劳动。", action: "女子长期承担家庭劳动。", voice: "疲惫而克制。", form: "“三岁”继续压缩时间；“靡”写尽范围。", q: "Q2 家务负担集中；Q3 权责失衡。" },
      { original: "夙兴夜寐，靡有朝矣", translation: "早起晚睡，没有一天不是这样。", keywords: "夙：早；兴：起身；夜寐：晚睡；朝：一日。", action: "一天的早晚被重复为多年的生活。", voice: "漫长、无休止。", form: "早/夜对举；“靡”反复；以一日写多年。", q: "Q2 持续劳动；Q3 长期生活投入。", key: "把这句还原成二十四小时：不是偶尔辛苦，而是“没有一天不是这样”。时间结构让单边负担比抽象的“勤劳”更可感。" },
      { original: "言既遂矣，至于暴矣", translation: "你的愿望满足以后，竟然变得粗暴。", keywords: "言：助词；遂：如愿、满足；暴：粗暴。", action: "男子在婚后愿望满足后态度恶化。", voice: "震惊、控诉。", form: "“既……至于……”把前后反差压在一句中。", q: "Q2 婚前婚后反差与粗暴伤害；Q3 男子直接责任。", key: "“暴”首先按教材语境理解为粗暴，不擅自补写具体身体伤害；但任何粗暴和人格伤害都不能由她的信任、投入或未及时停止来解释。" },
      { original: "兄弟不知，咥其笑矣", translation: "家人不了解我的处境，反而讥笑我。", keywords: "咥 xì：笑的样子。", action: "家人进入叙事，却没有提供理解。", voice: "孤立、屈辱。", form: "外部人物突然出现，使私人困境显出社会空间。", q: "Q2 家人不理解；Q3 支持缺失。是否求助，诗中未写。" },
      { original: "静言思之，躬自悼矣", translation: "静下来想这些事，只能独自悲伤。", keywords: "言：助词；躬：自身；悼：悲伤。", action: "女子从外部劳作和冲突转入独自反思。", voice: "悲伤、孤独，也开始审视经历。", form: "由外部叙事转入内心回望。", q: "Q1 自悼反思；Q3 孤立使停止更困难。" },
    ],
    activity: {
      title: "把“多年”还原成一天",
      prompt: "用“原句证据｜现代生活转述｜诗中未写明”三栏，还原她的一天和她周围的支持网络。",
      workspace: "清晨：________　白日：________　夜晚：________\n能否得到理解：________\n诗中没有写明：________________________",
      returnTitle: "时间表让失衡变得可见",
      returnItems: ["长期家务与早起晚睡，使一方持续承担生活成本。", "粗暴与家人不解叠加，关系外的支持并未出现。", "诗没有写她是否求助，也没有写具体退出条件；这些空白不能被想当然填满。"],
    },
  },
  {
    id: "C6", number: 6, label: "第六章", module: "M4", title: "回望盟誓与作出停止判断",
    text: "及尔偕老，老使我怨。淇则有岸，隰则有泮。\n总角之宴，言笑晏晏。信誓旦旦，不思其反。\n反是不思，亦已焉哉！",
    actionChain: "偕老愿望破裂 → 自然边界反衬 → 回忆少年 → 核验违誓 → 作出停止判断",
    summary: "女子将偕老愿望、少年欢笑与当下违誓并置，核验男子“不思其反”，最终说出“亦已焉哉”。",
    keyLines: [4, 5],
    lines: [
      { original: "及尔偕老，老使我怨", translation: "原想同你白头到老，如今想到老去却使我怨恨。", keywords: "及：同、跟；偕老：共同到老；怨：怨恨。", action: "旧日偕老愿望与现实正面碰撞。", voice: "幻灭、怨。", form: "同一个“老”字在愿望和现实中回环。", q: "Q1 偕老誓愿破裂。" },
      { original: "淇则有岸，隰则有泮", translation: "淇水尚且有岸，低湿地尚且有边。", keywords: "隰 xí：低湿的地方；泮 pàn：同“畔”，边、岸。", action: "由自然边界转入关系或怨苦的反衬。", voice: "悲凉、清醒。", form: "比兴或反衬；教材保留两种解释。", q: "可反衬男子心意无常，也可反衬女子怨苦无边，不定唯一答案。" },
      { original: "总角之宴，言笑晏晏", translation: "回想少年时代一起欢乐，言谈笑语和悦。", keywords: "总角：少年时代；宴：欢乐；晏晏：和悦的样子。", action: "叙述跳回少年共同记忆。", voice: "温暖记忆进入当下痛苦。", form: "叠词；时间回环。", q: "Q1 回望最初；Q3 共同记忆增加停止难度。" },
      { original: "信誓旦旦，不思其反", translation: "当初誓言诚恳，没想到你竟会违背。", keywords: "旦旦：诚恳的样子；反：违背。", action: "女子核验当初誓言与后来行为。", voice: "失望、确认，不再替违誓寻找理由。", form: "誓言/违誓对照；“不思”进入结尾回环。", q: "Q2 承诺与行动断裂；Q3 失信责任。", key: "结尾不是突然“觉醒”。她先调回总角、言笑和誓言，再用后来行为逐项核验；判断由长期经历形成。" },
      { original: "反是不思，亦已焉哉", translation: "你违背誓言而不念旧情，那就到此为止吧。", keywords: "是：这，指誓言；已：止、了结；焉、哉：语气词连用。", action: "女子形成停止这段关系的判断。", voice: "痛、倦、清醒和决绝可以并存。", form: "“反/不思”回环；语气词强化收束。", q: "Q1 核验违誓后作出停止判断；实际离开与退出条件未写。", key: "“亦已”可以有疲惫克制和清醒决绝两种声音。诗写出了判断，没有继续叙述现实行动；朗读可以多解，事实边界必须一致。" },
    ],
    activity: {
      title: "把“亦已”读出两种声音",
      prompt: "设计A“疲惫克制”和B“清醒决绝”两版：标出停顿、重音、速度，并为每版写一条经历依据。",
      workspace: "A版：停顿____ 重音____ 速度____ 依据____\nB版：停顿____ 重音____ 速度____ 依据____",
      returnTitle: "声音可以不同，证据必须完整",
      returnItems: ["疲惫克制：多年投入、劳作、孤立使“已”带着耗尽。", "清醒决绝：核验反复与违誓后，“已”成为明确判断。", "诗写出停止判断，是否实际离开及其现实条件仍保持开放。"],
    },
  },
];

const meaningUnits = chapters.flatMap((chapter) => [
  { id: `${chapter.id}A`, chapter: chapter.id, lineIds: [1, 2], title: `${chapter.label}句群A` },
  { id: `${chapter.id}B`, chapter: chapter.id, lineIds: [3, 4, 5], title: `${chapter.label}句群B` },
]);

function allVisibleText(slide) {
  return [slide.title, slide.subtitle, slide.prompt, slide.original, slide.translation, slide.body]
    .concat(slide.items || [])
    .filter(Boolean)
    .join("\n");
}

function noteText({ page, module, bridge, speech, action, responses, evidence, transition }) {
  return [
    `【页码与模块】P${page}｜${module}`,
    "【连续课堂剧本】",
    `【承接上一页】${bridge}`,
    `【教师原话】${speech}`,
    `【学生动作与等待】${action}`,
    `【可能回应与接话】${responses}`,
    `【可观察证据】${evidence}`,
    `【明确切页句】${transition}`,
  ].join("\n");
}

function reception(slide) {
  const byKind = {
    cover: ["好奇或暂时无判断", "意识到结尾需要完整经历支撑", "保留一个阅读入口"],
    prior: ["熟悉感与检索兴趣", "从旧作品比较关系条件", "激活已学经验"],
    question: ["问题感或距离感", "知道全文要解决什么", "保存初始猜想"],
    full_read: ["陌生、压抑、疑惑或无明显感受", "先接收整体声音再拆解", "形成一处停顿或问号"],
    background: ["获得进入文本的把握", "区分最小背景与后续发现", "掌握必要《诗经》支架"],
    chapter_text: ["进入一段完整叙事", "预判本章动作与声音", "保持章的整体轮廓"],
    line: ["字词障碍降低", "从原句到行动和意思", "准确理解一组诗句"],
    key: ["产生比较、惊讶或重新判断", "用形式解释处境", "形成有边界的关键解释"],
    activity: ["参与、犹豫或发现不同读法", "把个人判断放回诗句", "形成可检查的课堂产出"],
    chapter_end: ["获得阶段完成感", "把分句重新连成过程", "口述连续章意并保存证据"],
    synthesis: ["复杂、愤怒、同情或审慎", "从故事进入现实转述与责任判断", "回答三问并区分责任和困境"],
    knowledge: ["回顾与掌握感", "主动检索而非再听一遍", "收纳语言、结构和方法"],
    exit: ["回味、清醒或保留问题", "比较初读与再读", "留下最终解释和未决问题"],
  };
  const [experience, thought, learning] = byKind[slide.family || slide.kind] || byKind.synthesis;
  return { experience, thought, learning };
}

function notesForSlide(slide, page) {
  const module = modules.find((item) => item.id === slide.module);
  const moduleName = `模块${module.number}·${module.title}`;
  const common = {
    page, module: moduleName,
    bridge: "教师让上一页最后一句停稳，再把学生的视线带到本页唯一的新内容。",
    speech: `“现在只处理这一页。${slide.prompt || slide.title || slide.original || "请跟住眼前的文字"}”教师不预告下一页结论，先让原文或问题完整在场。`,
    action: "学生安静阅读二十秒；需要书写时独立落笔六十秒，需要交流时同桌交换九十秒。教师巡视时只看是否回到诗句，不读取私人经历。",
    responses: "如果回答只有‘痴情、负心、觉醒’等标签，教师追问所依据的原词和叙事位置；如果现场沉默，教师提供动作或字词入口，不提供完整答案。",
    evidence: slide.evidence || "一处原词标记、一句可复述的理解或一个诚实保留的问题。",
    transition: "教师用一句话保存本页证据：“先把这个发现放回故事里。”随后明确指向下一页再切屏。",
  };

  if (slide.kind === "cover") {
    return noteText({ ...common,
      bridge: "教师站在屏幕侧面，让标题和末句静置八秒，不用开场说明淹没诗句。",
      speech: "“先轻声读‘反是不思，亦已焉哉’。你听见的是疲惫、愤怒、清醒，还是暂时说不清？不用证明，只在纸角留下一个词或问号。”",
      action: "学生静默十秒后落笔；教师不点名检查情绪，只确认每个人拥有进入作品的方式。",
      responses: "如果有人立即说‘觉醒’或‘渣男’，教师回应：“把它保存成猜想；我们要看六章能不能给这个词足够重量。”如果无人落笔，允许写问号。",
      evidence: "一个初始声音词或问号。",
      transition: "“在走进这个更早的故事前，先从我们已经认识的关系故事出发。”",
    });
  }
  if (slide.kind === "prior") {
    return noteText({ ...common,
      bridge: "教师把学生从结尾的陌生声音带回熟悉作品，只使用班级确已学过的材料。",
      speech: `“三部作品不需要全部回答。选你最熟悉的一部：${slide.prompt || "这段关系的幸福或困境，取决于什么？"} 请先在记忆里找到一个人物行动或一句原文。”`,
      action: "个人检索三十秒，同桌各用四十秒说一部作品；听者只追问“依据是什么”。",
      responses: "可能出现‘真诚、选择权、尊重、经济和权力、外部支持’等回答。教师不排成标准答案，只把能由作品支撑的词写在板书边缘。",
      evidence: "一部已学作品、一处记忆锚点和一个关系条件。",
      transition: "“这些故事把问题带到了关系内部。现在去听《氓》中的当事人怎样讲自己的多年经历。”",
    });
  }
  if (slide.kind === "question" || slide.kind === "question_overview") {
    return noteText({ ...common,
      bridge: slide.phase === "return" ? "教师指向开课时保留的三问颜色和编号，提醒学生问题没有被换掉。" : "教师收起旧作品的答案，只留下三条等待全文检验的阅读线索。",
      speech: slide.kind === "question_overview" ? "“今天只跟住三个短锚点：关系过程、现实处境、责任与困境。它们现在不是答案目录。”" : `“请把这道问题原样读一遍：${slide.visible} 先写一个不超过十五字的猜想；证据可以暂时空着。”`,
      action: slide.phase === "return" ? "学生翻回初始猜想，静默四十秒，用不同颜色补写证据或划去旧判断。" : "学生静默二十秒读题；逐问页各停留二十秒，只写关键词，不展开讨论。",
      responses: "如果学生试图立即给出完整主题，教师说：“先保存；六章之后我们再看它是否需要修改。”若觉得问题太长，教师只重读本页加重词。",
      evidence: slide.phase === "return" ? "同一问题上的一处保留、修正或补证。" : "三道问题各一个初始猜想或空白。",
      transition: slide.phase === "return" ? "“问题不变，答案开始拥有诗句。接下来完成这一问的共同整理。”" : "“问题已经在场，现在第一次完整听她说，不在中途拦住她。”",
    });
  }
  if (slide.kind === "full_read") {
    return noteText({ ...common,
      bridge: slide.phase === "opening" ? "教师请学生把笔先放平，只留下耳朵和眼睛。" : "教师确认六章已经逐句走完，现在把所有分析暂时放下。",
      speech: slide.phase === "opening" ? "“这一遍不翻译、不回答三问。只让眼睛跟着诗句走，哪一句真正拉住你，再轻点一下。”" : "“从第一章一直读到第六章，中间不提问。读到初读停顿点时轻按纸面，等最后一句结束再回看。”",
      action: "教师或全班连续朗读本页内容；本页结束只无声切到下一半，不作口头插入。全部读完后静默十五秒。",
      responses: "出现漏读时教师只用手势从自然句首带回；有人急着解释时，教师以手势示意保存。没有停顿点也可写“尚未找到”。",
      evidence: slide.phase === "opening" ? "一次不中断整体接收和一处初读停顿/问号。" : "一次不中断全文重读以及初读点的保留或变化。",
      transition: slide.continues ? "教师不说话，直接无声切到下半首。" : "“完整声音先保留下来。现在从必要的出处和节奏支架开始，再进入第一章。”",
    });
  }
  if (slide.kind === "chapter_text") {
    return noteText({ ...common,
      bridge: slide.phase === "end" ? `教师把${slide.chapter.label}五组诗句重新放回同一页。` : `教师在进入${slide.chapter.label}逐句解释前，先让一章完整出现。`,
      speech: slide.phase === "end" ? `“现在完整重读${slide.chapter.label}。读完不用列点，请用一口气讲清：${slide.chapter.actionChain}之间怎样连接？”` : `“先完整读${slide.chapter.label}，遇到人物动作就轻点桌面，遇到声音变化就停半拍。暂时不翻译。”`,
      action: "全班按四言节奏朗读；章末学生闭书二十秒，向同桌连续口述章意，听者只补遗漏的行动。",
      responses: `如果口述变成主题标签，教师指向行动链；如果顺序混乱，让学生回到本页逐句寻找。可接受多种情绪，但事件顺序必须准确。`,
      evidence: `一次完整章读和一句连续章意：“${slide.chapter.summary}”`,
      transition: slide.phase === "end" ? "“这一章的证据先保存，故事继续向下一章走。”" : "“整章声音已经在场，接下来逐句把行动和意思照亮。”",
    });
  }
  if (slide.kind === "line") {
    const line = slide.line;
    const hasTranslation = Boolean(slide.translation);
    return noteText({ ...common,
      bridge: `教师指向${slide.chapter.label} ${slide.lineIndex}/5和累计行动链，不让这句脱离整章。`,
      speech: `“先读：‘${line.original}’。谁在做什么？”【等回答后】“${hasTranslation ? `用现代汉语说就是：${line.translation}` : "译意先不出现；请借关键词把它说完整。"} 关键词只处理${line.keywords}”教师随后补充：“${line.action}”`,
      action: "学生先独立借注释口译二十秒，再与同桌互查主语、动作和结果；教师只纠正事实、字音和关键古义。",
      responses: `如果误译，教师把句子拆成“谁—做什么—结果”；如果只读译文，要求重新读原句。情绪解释必须晚于基本意思。`,
      evidence: `准确口译“${line.original}”并指出：${line.action}`,
      transition: slide.isKey ? "“基本意思已经站稳。下一页不重复翻译，只看这句为何写得如此有力量。”" : "“这一步已经接回行动链，继续读下一句。”",
    });
  }
  if (slide.kind === "key") {
    const line = slide.line;
    return noteText({ ...common,
      bridge: `上一页已确认“${line.original}”的基本意思，本页只增加一个关键观察。`,
      speech: `“请把译意先放下，再读原句。你看见的形式是：${line.form} 它怎样改变我们对处境的理解？”教师在学生回应后用边界语收束：“${line.key}”`,
      action: "学生圈出形成对照、反复、语气或意象的原词，独立写一句“形式使我看见……”，再与同桌交换。",
      responses: "如果只报手法名，追问“哪两个词、使哪个人物时刻更可见”；如果推断过强，教师区分文本事实、合理推断和文本不能证明。",
      evidence: `一条“原词—形式—处境”解释，且不越过边界：${line.q}`,
      transition: "“手法不是另一套知识，它已经把人物行动照得更清楚。回到本章继续走。”",
    });
  }
  if (slide.kind === "activity") {
    const activity = slide.chapter ? slide.chapter.activity : null;
    const isReturn = slide.phase === "return";
    return noteText({ ...common,
      bridge: isReturn ? "教师确认学生已经形成个人或小组产出，才切到回收页。" : "教师把本章讲解暂时停住，只保留活动所需原句和空白。",
      speech: isReturn ? `“先别抄屏幕。请用你自己的产出核对：${(activity?.returnItems || slide.items || []).join("；")} 哪一点需要修改？”` : `“${slide.prompt} 产出只要一张图、一组朗读标记或一句判断，不需要长篇发言。”`,
      action: isReturn ? "学生用另一颜色修改一处，二十秒后自愿读出“我保留/修正了……因为……”。" : `学生独立准备六十秒，再同桌或四人组交流两分钟；记录者只写原句依据和一句产出。`,
      responses: "若讨论离开原文，教师只问“这来自哪句”；若出现不同答案，先检查证据和推理强度，不强求统一；若涉及私人经历，提醒只谈作品或第三人称案例。",
      evidence: isReturn ? "一处可见修订和一条有原句依据的阶段结论。" : "一份未被预制答案覆盖的学生产出。",
      transition: isReturn ? "“活动留下的不是热闹，而是一条可以放回整章的证据。现在完整重读本章。”" : "“请先保留你们的版本，下一页才出现共同核对。”",
    });
  }
  if (slide.kind === "module_reconnect") {
    return noteText({ ...common,
      bridge: "教师在新的内容模块开始时，不用复习题轰炸学生，只恢复故事位置。",
      speech: `“上次故事走到：${slide.body}。请用十五秒找到最后读懂的一句，再看今天要继续进入哪里。”`,
      action: "学生翻到对应诗句，先自己复述，再由一名学生用不超过三十秒连接前后。",
      responses: "若遗忘，教师给行动链首尾词；若复述过长，只保留人物行动和未回答的问题。",
      evidence: "能够说清上次停点、本次起点和仍在等待的三问。",
      transition: "“位置恢复了，让下一章完整出现。”",
    });
  }
  if (slide.family === "synthesis") {
    return noteText({ ...common,
      bridge: "教师确认六章已经完整讲解，才把问题和现代语言带回屏幕。",
      speech: `“${slide.prompt || slide.title} 先用诗句完成，再转换成现实语言；如果本页是共同回收，请先核对自己的版本，不直接抄结论。”`,
      action: "学生独立检索六十秒，小组按“原句—转述—边界”交流两分钟；涉及关系伤害时可匿名书写、不公开分享。",
      responses: "如果把女主人公投入连到男子粗暴，教师立即拆开责任线与困境线；如果说“恋爱脑”，转换为“情感投入下的浪漫化解释”，并声明它不是责任原因。",
      evidence: slide.evidence || "一条准确诗句、一条现代转述和一个解释边界。",
      transition: "“这一步完成以后，再进入下一层；两条线不混写，问题也不换词。”",
    });
  }
  if (slide.family === "knowledge") {
    return noteText({ ...common,
      bridge: "教师不再重讲全文，把主动权交给学生检索。",
      speech: `“${slide.prompt || slide.title} 请先遮住回收区，从今天真正读过的诗句中找答案。”`,
      action: slide.phase === "return" ? "学生对照回收页，勾出已找到项，给遗漏项补一处原句；用时六十秒。" : "学生个人检索四十秒，同桌互补四十秒；只写关键词和原句。",
      responses: "如果只背术语，追问术语解释了哪句；如果知识过多，优先保留能回到全文结构和阅读方法的内容。",
      evidence: "一组由学生先检索、再核对的知识收纳。",
      transition: "“知识已经归位，但诗还要以完整声音结束。”",
    });
  }
  if (slide.kind === "exit") {
    return noteText({ ...common,
      bridge: "全文最后一次朗读结束，教师让屏幕只留下结尾和两个空格。",
      speech: "“请完成两句：我现在最愿意用______理解她；我仍愿意保留的问题是______。不要求同一种声音，也不要求公开分享。”",
      action: "学生静默一分钟完成退出条；愿意者读出问题。教师收取或拍照保存，不现场给所有问题盖章。",
      responses: "若无人分享，教师允许问题随学生离开；若答案仍是单一标签，只追问一处跨章证据。",
      evidence: "一个最终理解词、一处跨章依据和一个保留问题。",
      transition: "“我们没有把她的多年经历缩成口号。请带着你能证明的理解和仍愿意追问的地方离开。”",
    });
  }
  return noteText(common);
}

const slides = [];

function addSlide(slide) {
  slides.push({ weight: 1, family: "synthesis", ...slide });
}

addSlide({ module: "M1", phase: "opening", kind: "cover", family: "cover", weight: 1, title: "氓", subtitle: "她怎样走到“亦已焉哉”？", body: "反是不思，亦已焉哉！", evidence: "一个初始声音词或问号。" });
addSlide({ module: "M1", phase: "opening", kind: "prior", family: "prior", weight: 2, title: "你记得哪一种关系？", items: ["《静女》｜相遇与等待", "《小二黑结婚》｜选择与阻力", "《玩偶之家（节选）》｜婚内结构与离开"], prompt: "选择最熟悉的一篇。" });
addSlide({ module: "M1", phase: "opening", kind: "prior", family: "prior", weight: 3, title: "从一部作品开始回忆", prompt: "这段关系的幸福或困境，取决于什么？", body: "人物行动/原句：________________\n我的判断：______________________" });
addSlide({ module: "M1", phase: "opening", kind: "prior", family: "prior", weight: 2, title: "三种故事，一道尚未结束的问题", items: ["相遇的欣悦，需要真实了解", "婚姻的选择，需要尊重与行动", "共同生活，需要平衡、支持与边界"], prompt: "这些是回忆入口，不是《氓》的预制答案。" });
addSlide({ module: "M1", phase: "opening", kind: "question_overview", family: "question", weight: 1, title: "带着三个问题走完六章", visible: "关系过程｜现实处境｜责任与困境", items: ["关系过程", "现实处境", "责任与困境"] });
THREE_QUESTIONS.forEach((question, index) => addSlide({ module: "M1", phase: "opening", kind: "question", family: "question", weight: 1, title: `问题${["一", "二", "三"][index]}`, visible: question, question_index: index + 1, body: question }));
addSlide({ module: "M1", phase: "opening", kind: "full_read", family: "full_read", weight: 3, title: "第一次完整听读｜第一至第三章", body: chapters.slice(0, 3).map((chapter) => chapter.text).join("\n\n"), continues: true });
addSlide({ module: "M1", phase: "opening", kind: "full_read", family: "full_read", weight: 3, title: "第一次完整听读｜第四至第六章", body: chapters.slice(3).map((chapter) => chapter.text).join("\n\n"), continues: false });
addSlide({ module: "M1", phase: "opening", kind: "mark", family: "full_read", weight: 2, title: "哪一句把你留了下来？", prompt: "抄下一句；写“我听见/我看见/我想问……”", body: "“____________________________”\n我______________________________" });
addSlide({ module: "M1", phase: "opening", kind: "background", family: "background", weight: 2, title: "《诗经》与《卫风》", items: ["我国最早的诗歌总集｜305篇", "风、雅、颂｜《氓》属于《卫风》", "女子第一人称回望婚姻经历"] });
addSlide({ module: "M1", phase: "opening", kind: "background", family: "background", weight: 2, title: "先借四言节奏走进声音", body: "氓之/蚩蚩，抱布/贸丝。\n匪来/贸丝，来即/我谋。", items: ["赋、比、兴到相应诗句再命名", "反复、叠词先在朗读中听见"] });
addSlide({ module: "M1", phase: "opening", kind: "background", family: "background", weight: 2, title: "让字音先通行", items: ["愆 qiān｜将 qiāng｜垝垣 guǐ yuán", "筮 shì｜说 tuō｜徂 cú", "汤汤 shāng shāng｜渐 jiān｜咥 xì", "隰 xí｜泮 pàn"] });
addSlide({ module: "M1", phase: "opening", kind: "checkpoint", family: "background", weight: 1, title: "故事从一次接近开始", body: "第一章｜相识、求婚与婚期", prompt: "先看见行动，再判断关系。" });

function addChapter(chapter) {
  addSlide({ module: chapter.module, phase: "chapter", kind: "chapter_text", family: "chapter_text", weight: 2, title: `${chapter.label}｜${chapter.title}`, body: chapter.text, chapter });
  chapter.lines.forEach((line, lineIndex) => {
    const index = lineIndex + 1;
    const isKey = chapter.keyLines.includes(index);
    addSlide({ module: chapter.module, phase: "chapter", kind: "line", family: "line", weight: 1.5, title: `${chapter.label} · ${index}/5`, original: line.original, translation: isKey ? "" : line.translation, body: isKey ? line.keywords : `${line.translation}\n${line.keywords}`, chapter, line, lineIndex: index, isKey, actionChain: chapter.actionChain });
    if (isKey) {
      addSlide({ module: chapter.module, phase: "chapter", kind: "key", family: "key", weight: 2, title: `${chapter.label} · ${index}/5｜读懂关键变化`, original: line.original, translation: line.translation, body: `${line.translation}\n${line.form}`, items: [line.key], chapter, line, lineIndex: index, actionChain: chapter.actionChain });
    }
  });
  addSlide({ module: chapter.module, phase: "question", kind: "activity", family: "activity", weight: 3, title: chapter.activity.title, prompt: chapter.activity.prompt, body: chapter.activity.workspace, chapter });
  addSlide({ module: chapter.module, phase: "return", kind: "activity", family: "activity", weight: 2, title: chapter.activity.returnTitle, items: chapter.activity.returnItems, chapter });
  addSlide({ module: chapter.module, phase: "end", kind: "chapter_text", family: "chapter_end", weight: 2, title: `${chapter.label}｜完整重读，连成一句`, body: chapter.text, subtitle: chapter.actionChain, chapter });
}

addChapter(chapters[0]);
addSlide({ module: "M2", phase: "reconnect", kind: "module_reconnect", family: "chapter_end", weight: 1, title: "故事走到这里", body: "相识议婚｜女子远送并约定秋期", prompt: "第二章将进入等待、卜筮与迁嫁。" });
addChapter(chapters[1]);
addChapter(chapters[2]);
addSlide({ module: "M3", phase: "reconnect", kind: "module_reconnect", family: "chapter_end", weight: 1, title: "故事走到这里", body: "相识议婚 → 等待迁嫁 → 回望中的劝诫", prompt: "第四、五章将进入婚后事实。" });
addChapter(chapters[3]);
addChapter(chapters[4]);
addSlide({ module: "M4", phase: "reconnect", kind: "module_reconnect", family: "chapter_end", weight: 1, title: "故事走到这里", body: "婚后食贫、长期劳动、粗暴与家人不解", prompt: "第六章回到旧日誓言。" });
addChapter(chapters[5]);

addSlide({ module: "M4", phase: "return", kind: "full_read", family: "full_read", weight: 3, title: "再次完整朗读｜第一至第三章", body: chapters.slice(0, 3).map((chapter) => chapter.text).join("\n\n"), continues: true });
addSlide({ module: "M4", phase: "return", kind: "full_read", family: "full_read", weight: 3, title: "再次完整朗读｜第四至第六章", body: chapters.slice(3).map((chapter) => chapter.text).join("\n\n"), continues: false });
addSlide({ module: "M4", phase: "return", kind: "initial_compare", family: "synthesis", weight: 2, title: "回到最初的停顿点", prompt: "我的初读判断：__________\n现在：□保留　□修正　□推翻\n因为新增证据：________________" });
addSlide({ module: "M4", phase: "return", kind: "question_overview", family: "question", weight: 1, title: "三个问题，开始回收", visible: "关系过程｜现实处境｜责任与困境", items: ["关系过程", "现实处境", "责任与困境"] });
THREE_QUESTIONS.slice(0, 2).forEach((question, index) => addSlide({ module: "M4", phase: "return", kind: "question", family: "question", weight: 1, title: `回到问题${["一", "二"][index]}`, visible: question, question_index: index + 1, body: question }));
addSlide({ module: "M4", phase: "question", kind: "q1_activity", family: "synthesis", weight: 3, title: "把她的经历连成一条路", prompt: "按六章排序，并为每一步标一处诗句。", items: ["相识议婚", "等待成婚", "迁嫁食贫", "长期劳作", "失信粗暴", "家人不解", "核验誓言", "停止判断"] });
addSlide({ module: "M4", phase: "return", kind: "q1_return", family: "synthesis", weight: 2, title: "关系与婚姻过程", body: "相识议婚 → 等待成婚 → 迁嫁食贫 → 长期劳作\n→ 失信粗暴 → 家人不解 → 回望核验 → 作出停止判断", evidence: "八步过程、六章回链和一处初始排序修订。" });
addSlide({ module: "M4", phase: "question", kind: "mapping_prompt", family: "synthesis", weight: 2, title: "把不幸翻译成现实生活语言", prompt: "每项都写：原句证据｜现代生活转述｜解释边界", body: "不直接抄诗句，也不把推断冒充事实。" });
addSlide({ module: "M4", phase: "return", kind: "mapping", family: "synthesis", weight: 2, title: "表里差异", items: ["“贸丝/谋”｜表面来意与真实来意有别｜不能证明完整人格有计划伪装", "“女也不爽，士贰其行”｜婚前婚后表现反差｜责任由诗句直接指向男子", "“信誓旦旦/不思其反”｜承诺没有转化为长期行动｜不补写男子心理动机"] });
addSlide({ module: "M4", phase: "return", kind: "mapping", family: "synthesis", weight: 2, title: "劳动与伤害", items: ["“夙兴夜寐”｜生活负担长期集中于一方｜不是偶发辛劳", "“至于暴矣”｜关系转为粗暴和伤害｜具体伤害方式未写明", "“二三其德”｜行为反复、不稳定｜不以投入为其原因"] });
addSlide({ module: "M4", phase: "return", kind: "mapping", family: "synthesis", weight: 2, title: "支持与停止", items: ["“兄弟不知”｜未获得家人理解｜是否求助未写", "“女之耽兮，不可说也”｜停止代价不平等｜须结合时代处境", "“亦已焉哉”｜形成停止判断｜是否实际离开及退出条件未写"] });
addSlide({ module: "M4", phase: "return", kind: "mapping_return", family: "synthesis", weight: 1, title: "第二问的回答边界", body: "现实语言让古诗进入今天；\n原句与“未写明”让今天的概念不覆盖古诗。", evidence: "至少三条“原句—转述—边界”映射。" });

addSlide({ module: "M5", phase: "reconnect", kind: "module_reconnect", family: "chapter_end", weight: 1, title: "故事与前两问已经站稳", body: "关系过程已排序｜现实处境已完成诗句—转述—边界", prompt: "现在只拆开责任线与困境线。" });
addSlide({ module: "M5", phase: "return", kind: "question", family: "question", weight: 2, title: "回到问题三", visible: THREE_QUESTIONS[2], question_index: 3, body: THREE_QUESTIONS[2] });
addSlide({ module: "M5", phase: "return", kind: "responsibility_line", family: "synthesis", weight: 3, title: "责任线｜诗把什么责任指向男子？", body: "士贰其行 → 二三其德 → 至于暴矣 → 不思其反", items: ["失信", "行为反复", "粗暴", "违誓"], evidence: "责任线四处直接诗句；不补写男子动机。" });
addSlide({ module: "M5", phase: "return", kind: "difficulty_line", family: "synthesis", weight: 3, title: "困境线｜什么使停止更加困难？", body: "初期信息有限与良好印象 → 情感和生活投入\n→ 单边劳动与权责失衡 → 家人不解与支持缺失", items: ["沉没成本、确认偏向、支持系统是现代分析工具", "这些概念只解释困境，不分担责任"] });
addSlide({ module: "M5", phase: "return", kind: "boundary", family: "synthesis", weight: 2, title: "两条线之间，不画这支箭", body: "她的信任、投入、未及时停止　✕→　他的失信与粗暴", prompt: "困境线不能分担责任线中的责任。", evidence: "能够分别回答“谁的责任”和“为何难以停止”。" });
addSlide({ module: "M5", phase: "question", kind: "retrospective", family: "synthesis", weight: 2, title: "回头看第一章", prompt: "第一次看，这些行动给你什么印象？\n读完全诗，哪些模糊细节需要重新评估？", items: ["蚩蚩", "贸丝/谋", "匪我愆期", "将子无怒"] });
addSlide({ module: "M5", phase: "return", kind: "retrospective", family: "synthesis", weight: 2, title: "事实、推断与不能证明", items: ["事实｜表面来意为贸丝，真实来意为谋婚；蚩蚩是外在印象", "推断｜可能存在初期印象管理；婚前印象与婚后行为反差", "不能证明｜有计划地伪装完整人格；女子长期不知；无怒已是婚前暴力", "现代工具｜确认偏向、浪漫化解释；不是心理诊断，也不是粗暴原因"] });
addSlide({ module: "M5", phase: "question", kind: "relation", family: "synthesis", weight: 3, title: "从《氓》反推关系结构", prompt: "一段关系要避免走向失衡，需要哪些可以长期观察和验证的条件？", body: "只讨论作品或第三人称案例，不必分享私人经历。" });
addSlide({ module: "M5", phase: "return", kind: "relation", family: "synthesis", weight: 2, title: "从作品提出的观察维度", items: ["审慎了解｜不以一时形象替代长期观察", "言行一致｜承诺由持续行动检验", "权责平衡｜劳动、资源与决定共同承担", "相互尊重｜边界不以愤怒和粗暴回应", "可靠支持｜有可获得的理解、求助渠道与退出保障"] });

const knowledgeGroups = [
  { title: "故事与人物", prompt: "不看答案：用六个动作写出叙事结构，再写人物认识怎样变化。", items: ["相识议婚—等待迁嫁—婚后食贫—长期劳作—失信孤立—停止判断", "期待—投入—承受—自悼—核验违誓—形成停止判断"] },
  { title: "字词与《诗经》", prompt: "找出本课最容易误读、误解的八个字词，并说明《氓》属于哪一类诗。", items: ["《诗经》305篇；风、雅、颂；《氓》属于《卫风》；以四言为主", "愆 qiān｜将 qiāng｜筮 shì｜说 tuō｜徂 cú｜汤汤 shāng shāng｜渐 jiān｜咥 xì｜隰 xí｜泮 pàn"] },
  { title: "意象与写法", prompt: "各找一组原句说明：桑叶、淇水、对照、反复怎样参与理解。", items: ["桑叶｜沃若/黄而陨：比兴、状态对照，意义由语境筛选", "淇水｜三处语言连接空间与回望，方向不强行补写", "赋、比、兴｜对照、反复、叠词、呼告｜时间压缩、时间回环、第一人称回望"] },
  { title: "三问与阅读方法", prompt: "用一条证据回答每问，再写出可迁移到其他叙事诗的阅读顺序。", items: ["Q1 关系过程｜Q2 现实处境｜Q3 责任线/困境线", "准确释义 → 行动叙事 → 声音情感 → 形式观察 → 证据判断 → 现实转换"] },
];
knowledgeGroups.forEach((group) => {
  addSlide({ module: "M5", phase: "question", kind: "knowledge", family: "knowledge", weight: 2, title: `知识检索｜${group.title}`, prompt: group.prompt });
  addSlide({ module: "M5", phase: "return", kind: "knowledge", family: "knowledge", weight: 2, title: `知识收纳｜${group.title}`, items: group.items });
});
addSlide({ module: "M5", phase: "final", kind: "full_read", family: "full_read", weight: 3, title: "最后一次完整朗读｜第一至第三章", body: chapters.slice(0, 3).map((chapter) => chapter.text).join("\n\n"), continues: true });
addSlide({ module: "M5", phase: "final", kind: "full_read", family: "full_read", weight: 3, title: "最后一次完整朗读｜第四至第六章", body: chapters.slice(3).map((chapter) => chapter.text).join("\n\n"), continues: false });
addSlide({ module: "M5", phase: "final", kind: "exit", family: "exit", weight: 2, title: "把理解和问题一起带走", body: "我现在最愿意用________理解她，因为________。\n我仍愿意保留的问题是________________。", subtitle: "反是不思，亦已焉哉！" });

function allocateMinutes() {
  modules.forEach((module) => {
    const moduleSlides = slides.filter((slide) => slide.module === module.id);
    const totalWeight = moduleSlides.reduce((sum, slide) => sum + slide.weight, 0);
    moduleSlides.forEach((slide) => {
      slide._rawMinutes = (module.minutes * slide.weight) / totalWeight;
      slide.minutes = Math.max(1, Math.floor(slide._rawMinutes));
    });
    let assigned = moduleSlides.reduce((sum, slide) => sum + slide.minutes, 0);
    const byRemainder = [...moduleSlides].sort((a, b) => (b._rawMinutes - b.minutes) - (a._rawMinutes - a.minutes));
    let cursor = 0;
    while (assigned < module.minutes) {
      byRemainder[cursor % byRemainder.length].minutes += 1;
      assigned += 1;
      cursor += 1;
    }
    while (assigned > module.minutes) {
      const candidate = [...moduleSlides].sort((a, b) => b.minutes - a.minutes).find((slide) => slide.minutes > 1);
      if (!candidate) throw new Error(`Cannot allocate ${module.minutes} minutes for ${module.id}`);
      candidate.minutes -= 1;
      assigned -= 1;
    }
    moduleSlides.forEach((slide) => delete slide._rawMinutes);
  });
}

allocateMinutes();
slides.forEach((slide, index) => {
  slide.id = `S${String(index + 1).padStart(3, "0")}`;
  if (!slide.visible) slide.visible = allVisibleText(slide);
  slide.notes = notesForSlide(slide, index + 1);
  Object.assign(slide, reception(slide));
});

const lineGroups = chapters.flatMap((chapter) => chapter.lines.map((line, index) => ({
  id: `${chapter.id}L${index + 1}`,
  chapter: chapter.id,
  chapterNumber: chapter.number,
  lineNumber: index + 1,
  ...line,
})));

const totalMinutes = modules.reduce((sum, module) => sum + module.minutes, 0);

const causalLines = {
  responsibility: ["士贰其行", "二三其德", "至于暴矣", "不思其反"],
  difficulty: ["初期信息有限", "情感和生活投入", "单边劳动", "支持缺失", "停止更加困难"],
  links: [["士贰其行", "失信责任"], ["支持缺失", "停止更加困难"]],
};

function snapshot() {
  return {
    version: "5.0-text-spine",
    generated_at: "2026-08-11",
    total_minutes: totalMinutes,
    modules,
    lines: lineGroups,
    meaning_units: meaningUnits,
    three_questions: THREE_QUESTIONS,
    causal_lines: causalLines,
    slides: slides.map((slide) => {
      const copy = { ...slide };
      if (copy.chapter) copy.chapter = copy.chapter.id;
      if (copy.line) copy.line = copy.line.original;
      return copy;
    }),
  };
}

module.exports = {
  THREE_QUESTIONS,
  modules,
  chapters,
  meaningUnits,
  lineGroups,
  slides,
  totalMinutes,
  causalLines,
  snapshot,
};
