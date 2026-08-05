#!/usr/bin/env python3
"""Split PDFs into per-lesson PDFs with manually verified boundaries.

Book2 (课本): 14 lessons + 古诗词诵读 + 后记
  - Lesson 1 = 氓 + 离骚 (one lesson, NOT two)
  - Lesson 5 = 阿Q正传 + 边城
  - etc.

Book1 (教师教学用书): 16 lessons (课文解说) + unit-level sections
  - Lesson 1 = 子路曾皙 + 齐桓晋文之事
  - Units 4 & 7 have no numbered lessons
"""
import os, re
import fitz


def sanitize(title):
    t = title.replace('\n', ' ').strip()
    t = re.sub(r'[\\/:*?"<>|（）()·\s]+', '_', t)
    return t[:40]


def split_book(orig_pdf, sections, out_dir):
    """sections: list of (seq, label, start_page_1based, end_page_1based)"""
    doc = fitz.open(orig_pdf)
    total = doc.page_count
    os.makedirs(out_dir, exist_ok=True)
    # Clean old files
    import glob
    for f in glob.glob(out_dir + '/*.pdf'):
        os.remove(f)

    print(f"\n===== {os.path.basename(out_dir)} ({total} pages) -> {len(sections)} files =====")
    for seq, label, start, end in sections:
        # Validate
        assert 1 <= start <= total, f"start {start} out of range for {label}"
        assert start <= end <= total, f"end {end} out of range for {label}"
        name = f"{seq:02d}_{sanitize(label)}.pdf"
        d = fitz.open()
        d.insert_pdf(doc, from_page=start - 1, to_page=end - 1)
        d.save(os.path.join(out_dir, name))
        d.close()
        print(f"  {name}  (p{start}-{end}, {end-start+1} pages)")
    doc.close()


# ============================================================
# Book2: 高中语文选择性必修下册 (123 pages)
# Lesson structure from TOC:
#   1 氓/离骚 | 2 孔雀东南飞 | 3 蜀道难/蜀相 | 4 望海潮/扬州慢
#   5 阿Q正传/边城 | 6 大堰河/再别康桥 | 7 一个消逝了的山村/秦腔 | 8 茶馆
#   9 陈情表/项脊轩志 | 10 兰亭集序/归去来兮辞 | 11 种树郭橐驼传 | 12 石钟山记
#   13 自然选择的证明/宇宙的边疆 | 14 天文学上的旷世之争
# ============================================================
BOOK2_SECTIONS = [
    (0,  '前言',              1,   5),
    # Unit 1
    (1,  'L01_氓_离骚',       6,  11),   # includes U1 intro p6
    (2,  'L02_孔雀东南飞并序', 12, 18),
    (3,  'L03_蜀道难_蜀相',   19, 21),
    (4,  'L04_望海潮_扬州慢', 22, 24),
    (5,  'U1_单元研习任务',   25, 25),
    # Unit 2
    (6,  'L05_阿Q正传_边城',  26, 45),   # includes U2 intro p26
    (7,  'L06_大堰河_再别康桥', 46, 51),
    (8,  'L07_一个消逝了的山村_秦腔', 52, 59),
    (9,  'L08_茶馆',          60, 71),
    (10, 'U2_单元研习任务_语言的锤炼', 72, 73),
    # Unit 3
    (11, 'L09_陈情表_项脊轩志', 74, 79),  # includes U3 intro p74
    (12, 'L10_兰亭集序_归去来兮辞', 80, 85),
    (13, 'L11_种树郭橐驼传',   86, 87),
    (14, 'L12_石钟山记',       88, 89),
    (15, 'U3_单元研习任务_说真话抒真情', 90, 91),
    # Unit 4
    (16, 'L13_自然选择的证明_宇宙的边疆', 92, 105),  # includes U4 intro p92
    (17, 'L14_天文学上的旷世之争', 106, 113),
    (18, 'U4_单元研习任务_文章修改', 114, 115),
    # Extras
    (19, '古诗词诵读',         116, 119),
    (20, '后记',              120, 123),
]

# ============================================================
# Book1: 教师教学用书 (347 pages)
# 16 numbered lessons in 课文解说 sections.
# Units 4 & 7 have no numbered lessons.
# Unit-level content (目标/意图/指导 + 学习任务/教学设计/资料)
# split into separate files.
# ============================================================
BOOK1_SECTIONS = [
    (0,  '前言',                    1,  18),
    # Unit 1 (p19-65)
    (1,  'U1_导引_目标_意图_指导',  19, 23),
    (2,  'L01_子路曾皙_齐桓晋文之事', 24, 26),
    (3,  'L02_烛之武退秦师',        27, 28),
    (4,  'L03_鸿门宴',             29, 29),
    (5,  'U1_学习任务_教学设计',    30, 65),
    # Unit 2 (p66-116)
    (6,  'U2_导引_目标_意图_指导',  66, 68),
    (7,  'L04_窦娥冤',             69, 71),
    (8,  'L05_雷雨',               72, 73),
    (9,  'L06_哈姆莱特',            74, 76),
    (10, 'U2_学习任务_教学设计_资料', 77, 116),
    # Unit 3 (p117-160)
    (11, 'U3_导引_目标_意图_指导',  117, 119),
    (12, 'L07_青蒿素_一名物理学家',  120, 122),
    (13, 'L08_中国建筑的特征',      123, 124),
    (14, 'L09_说木叶',             125, 125),
    (15, 'U3_学习任务_教学设计_资料', 126, 160),
    # Unit 4 (p161-177) - no lessons
    (16, 'U4_信息时代的语文生活',   161, 177),
    # Unit 5 (p178-217)
    (17, 'U5_导引_目标_意图_指导',  178, 181),
    (18, 'L10_在人民报演说_在马克思墓前', 182, 186),
    (19, 'L11_谏逐客书_与妻书',     187, 191),
    (20, 'U5_学习任务_教学设计_资料', 192, 217),
    # Unit 6 (p218-267)
    (21, 'U6_导引_目标_意图_指导',  218, 220),
    (22, 'L12_祝福',               221, 221),
    (23, 'L13_林教头风雪山神庙_装在套子里的人', 222, 226),
    (24, 'L14_促织_变形记',         227, 230),
    (25, 'U6_学习任务_教学设计_资料', 231, 267),
    # Unit 7 (p268-298) - no lessons
    (26, 'U7_整本书阅读',           268, 298),
    # Unit 8 (p299-347)
    (27, 'U8_导引_目标_意图_指导',  299, 303),
    (28, 'L15_谏太宗十思疏_答司马谏议书', 304, 307),
    (29, 'L16_阿房宫赋_六国论',     308, 309),
    (30, 'U8_学习任务_教学设计_资料', 310, 347),
]


if __name__ == '__main__':
    base = '/Users/luochongjing/Documents/Projects/Yuwen'
    out_base = f'{base}/textbook_extract'

    # Book1
    split_book(
        f'{base}/Data/textbook/统编本高中语文必修下册 教师教学用书.pdf',
        BOOK1_SECTIONS,
        f'{out_base}/book1_教师用书/split_pdf'
    )

    # Book2
    split_book(
        f'{base}/Data/textbook/高中语文选择性必修下册(OCR).pdf',
        BOOK2_SECTIONS,
        f'{out_base}/book2_课本/split_pdf'
    )

    print("\nDone!")
