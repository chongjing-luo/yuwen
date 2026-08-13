"use strict";

const SOURCE = "TEXTBOOK#氓正文";

const chapterData = [
  {
    chapter_id: "C1",
    title: "相识、议婚与婚期",
    action_chain: ["以贸丝姿态接近", "说明求婚来意", "女子远送", "说明媒妁条件", "安抚并约定婚期"],
    lines: [
      "氓之蚩蚩，抱布贸丝", "匪来贸丝，来即我谋", "送子涉淇，至于顿丘",
      "匪我愆期，子无良媒", "将子无怒，秋以为期",
    ],
  },
  {
    chapter_id: "C2",
    title: "等待、卜筮与迁嫁",
    action_chain: ["登垣远望", "不见而泣", "既见而笑", "卜筮无咎", "乘车迁嫁"],
    lines: [
      "乘彼垝垣，以望复关", "不见复关，泣涕涟涟", "既见复关，载笑载言",
      "尔卜尔筮，体无咎言", "以尔车来，以我贿迁",
    ],
  },
  {
    chapter_id: "C3",
    title: "桑叶、斑鸠与回望中的劝诫",
    action_chain: ["桑叶丰润", "劝鸠勿食", "劝女勿耽", "指出男子尚可脱身", "指出女子难以脱身"],
    lines: [
      "桑之未落，其叶沃若", "于嗟鸠兮，无食桑葚", "于嗟女兮，无与士耽",
      "士之耽兮，犹可说也", "女之耽兮，不可说也",
    ],
  },
  {
    chapter_id: "C4",
    title: "桑叶转黄、食贫与责任判断",
    action_chain: ["桑叶枯黄坠落", "回顾多年食贫", "淇水浸湿车帷", "辨明双方责任", "指出男子反复"],
    lines: [
      "桑之落矣，其黄而陨", "自我徂尔，三岁食贫", "淇水汤汤，渐车帷裳",
      "女也不爽，士贰其行", "士也罔极，二三其德",
    ],
  },
  {
    chapter_id: "C5",
    title: "长期劳动、粗暴与孤立",
    action_chain: ["多年承担室劳", "早起晚睡", "男子转为粗暴", "兄弟不理解而讥笑", "独自反思悲悼"],
    lines: [
      "三岁为妇，靡室劳矣", "夙兴夜寐，靡有朝矣", "言既遂矣，至于暴矣",
      "兄弟不知，咥其笑矣", "静言思之，躬自悼矣",
    ],
  },
  {
    chapter_id: "C6",
    title: "回望盟誓与作出停止判断",
    action_chain: ["偕老愿望破裂", "以自然边界反衬", "回忆少年言笑", "核验违誓", "作出停止判断"],
    lines: [
      "及尔偕老，老使我怨", "淇则有岸，隰则有泮", "总角之宴，言笑晏晏",
      "信誓旦旦，不思其反", "反是不思，亦已焉哉",
    ],
  },
];

const lines = [];
chapterData.forEach((chapter, chapterIndex) => {
  chapter.lines.forEach((text, lineIndex) => {
    lines.push({
      line_id: `L${String(lines.length + 1).padStart(3, "0")}`,
      chapter_id: chapter.chapter_id,
      chapter_order: chapterIndex + 1,
      chapter_line_order: lineIndex + 1,
      text,
      source_ref: SOURCE,
    });
  });
});

const chapters = chapterData.map((chapter, chapterIndex) => ({
  chapter_id: chapter.chapter_id,
  chapter_order: chapterIndex + 1,
  title: chapter.title,
  action_chain: chapter.action_chain,
  line_ids: lines.filter((line) => line.chapter_id === chapter.chapter_id).map((line) => line.line_id),
}));

const meaningUnits = [
  ["U01", "C1", "外在印象与真实来意", 1, 2],
  ["U02", "C1", "远送、媒妁条件、安抚与婚期", 3, 5],
  ["U03", "C2", "登垣、未见、哭泣、见到后的骤变", 6, 8],
  ["U04", "C2", "卜筮、车来与迁嫁", 9, 10],
  ["U05", "C3", "桑叶、斑鸠与劝诫的起点", 11, 12],
  ["U06", "C3", "从物到人、从自身到性别处境", 13, 15],
  ["U07", "C4", "桑叶变化与多年食贫", 16, 17],
  ["U08", "C4", "淇水场景与明确责任判断", 18, 20],
  ["U09", "C5", "多年劳动如何重复成生活", 21, 22],
  ["U10", "C5", "粗暴、家人不解与独自反思", 23, 25],
  ["U11", "C6", "偕老愿望与“有岸/有泮”", 26, 27],
  ["U12", "C6", "少年记忆、违誓核验与停止判断", 28, 30],
].map(([unit_id, chapter_id, title, start, end]) => ({
  unit_id, chapter_id, title,
  line_ids: Array.from({ length: end - start + 1 }, (_, index) => `L${String(start + index).padStart(3, "0")}`),
}));

const interpretiveBoundaries = [
  {
    boundary_id: "CHI_CHI_IMPRESSION", evidence_line_ids: ["L001"],
    allowed_claims: ["“蚩蚩”先按教材理解为忠厚的样子，是男子的出场印象"],
    forbidden_claims: ["“蚩蚩”直接证明男子真实忠厚", "“蚩蚩”直接等于有计划地装老实"],
  },
  {
    boundary_id: "TRADE_VS_PROPOSAL", evidence_line_ids: ["L001", "L002"],
    allowed_claims: ["表面来意是贸丝，真实来意是议婚，两者有别"],
    forbidden_claims: ["来意有别足以证明男子系统伪装完整人格", "诗已写明男子有预谋欺骗"],
  },
  {
    boundary_id: "NO_ANGER_AMBIGUITY", evidence_line_ids: ["L004", "L005"],
    allowed_claims: ["女子需要安抚或预期男子愤怒，这一细节适合全文后重读"],
    forbidden_claims: ["“无怒”证明婚前已经发生暴力", "女子当时已经掌握全部风险却故意忽视"],
  },
  {
    boundary_id: "SANG_LEAF_OPENNESS", evidence_line_ids: ["L011", "L016"],
    allowed_claims: ["桑叶荣枯可引发青春、情感或关系状态等竞争解释"],
    forbidden_claims: ["桑叶只能等于女子容貌或青春", "意象有脱离语境的一对一密码"],
  },
  {
    boundary_id: "VIOLENCE_SCOPE", evidence_line_ids: ["L023"],
    allowed_claims: ["“暴”首先按教材语境理解为婚后粗暴和态度恶化"],
    forbidden_claims: ["诗已写明具体身体伤害方式", "用女子的信任、投入或劳作解释男子的粗暴责任"],
  },
  {
    boundary_id: "FAMILY_SUPPORT_BOUNDARY", evidence_line_ids: ["L024", "L025"],
    allowed_claims: ["兄弟不理解而讥笑，使女子处在缺乏理解和托举的位置", "兄弟是诗中明确写出的家人；更广义的支持缺失只能标为处境推断"],
    forbidden_claims: ["诗写明女子曾向家人求助", "诗写明所有家人都出于恶意拒绝支持"],
  },
  {
    boundary_id: "QI_BANK_MULTIPLE_READINGS", evidence_line_ids: ["L027"],
    allowed_claims: ["可反衬男子心意无常，也可反衬女子怨苦无边，需比较语境"],
    forbidden_claims: ["“淇则有岸”只有一个确定象征义", "该句证明一次方向明确的第三次渡水"],
  },
  {
    boundary_id: "STOP_JUDGMENT_BOUNDARY", evidence_line_ids: ["L029", "L030"],
    allowed_claims: ["女子在回看盟誓和违誓后形成停止这段关系的判断", "诗没有写明她已经实际离家、怎样离开或后来怎样生活"],
    forbidden_claims: ["诗已经写明她实际离家并获得新的生活", "结尾证明她已经释然并获得胜利"],
  },
  {
    boundary_id: "RESPONSIBILITY_CAUSE_SPLIT", evidence_line_ids: ["L013", "L014", "L015", "L019", "L020", "L021", "L022", "L023", "L024"],
    allowed_claims: ["女子的投入、长期劳作和支持缺失可以解释关系为何难以及时停止", "男子失信、反复和粗暴是诗中可直接定位的伤害责任"],
    forbidden_claims: ["女子的投入、长期劳作或未及时停止，解释或分担了男子失信、反复和粗暴的责任", "用“恋爱脑”标签替代对文本处境和结构的分析"],
  },
];

const contract = {
  schema_version: "1.0",
  contract_id: "MENG_V6_TEXT_1",
  source: {
    textbook_path: "Data/textbook_extract/选择性必修下册/mineru_result/01_U1_导语_课1_氓_离骚/full.md",
    textbook_sha256: "384266a83e13663cdf758c6202e2d5f95737ee5f25408bc3e229e295667a9cfd",
    evidence_dossier_path: "work/备课/选择性必修下册/氓/01_文本研究与证据档案.md",
    evidence_dossier_sha256: "c0942e52d8655d40723f140b478cc1212292a733a342f796744fd1f51547ca10",
  },
  chapters,
  lines,
  meaning_units: meaningUnits,
  interpretive_boundaries: interpretiveBoundaries,
};

module.exports = { contract };
