#!/usr/bin/env python3
"""Create a reversible 2013 Sichuan answer-image candidate layer.

The Sina gallery is a third-party reproduction and the page images carry a
watermark.  This script records a conservative visual transcription only; it
does not modify the main 2013 answer index, invent a scoring standard, or
promote the source to official status.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "Data/reference/gaokao/external/2013_sina_images"
OUT = ROOT / "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/reference_answer_candidates.jsonl"
REPORT = ROOT / "work/knowledge/exams/workbench/EXAM-REFERENCE-ANSWER-CANDIDATES-2013.md"
RECEIPT = ROOT / "work/knowledge/_reviews/receipts/exam_reference_answer_candidates_2013_20260809.json"


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_text(value: str) -> str:
    return sha_bytes(value.encode("utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


ANSWERS: dict[int, str] = {
    1: "B",
    2: "A",
    3: "B",
    4: "C",
    5: "B",
    6: "C",
    7: "D",
    8: "D",
    9: "C",
    10: "（1）平时单独居处，整天严肃庄重；至于和人交往，则热情洋溢、和乐喜悦。（2）凡是引用的书籍，总是加上注解，用来裁断订正它们的意义，也有许多先儒没有阐发的内容。",
    11: "敏而好学，诲人不倦；严谨治学，敢于创新；忧国而献良策；助人而不居功；立志为本，知行合一。",
    12: "因民之所利而利之/斯不亦惠而不费乎/择可劳而劳之/又谁怨/欲仁而得仁/又焉贪/君子无众寡/无小大/无敢慢/斯不亦泰而不骄乎",
    13: "（1）主要表达作者壮志未酬的忧愁和苦闷。华发、愁、寒无睡等写年岁已逝和愁苦；“壮心偶傍醉中来”写壮心未泯而又不得施展。（2）“佳节”与“愁”对比，“久”与“偶”对比，“愁”与“壮心”对比，三层对比强化了忧愁之深和潜藏于胸的壮心未绝。",
    14: "（1）载笑载言（2）百步九折萦岩峦（3）浑欲不胜簪（4）轻拢慢捻抹复挑（5）能谤讥于市朝（6）疲敝之卒（7）皆若空游无所依（8）浩浩乎如凭虚御风",
    15: "C、E",
    16: "①生动地刻画出胡杨林坚韧顽强的形象，增强文章的感染力；②深化主题，以胡杨树的生死暗示河流的变化，表现生命离开河流后的困顿；③由河到树，由树到人，承上启下，结构更加严密。",
    17: "①塔里木河身处沙漠，不得不与沙漠进行长期的坚韧较量；②塔里木河给沙漠带来生命与文明，却不得不亲历文明的衰落；③塔里木河的奔腾和消失承载着人们的热爱、惶恐等复杂情感，引发沉重思考。",
    18: "示例一：河流是人类文化的源头。塔里木河曾赋予罗布泊人浪漫的生活气息，长江、黄河乃至家乡的每一条河都滋养了中华民族源远流长的文化。如今许多河流正在萎缩，人类社会的发展不应以破坏自然为代价。\n\n示例二：河流具有超越自然生命的文化魅力。塔里木河的率直坦荡既是自然属性的体现，也是文化人格的写照；即使自然河流萎缩或消失，仍可从现存文化中感知其形态、历史和文化意义。",
    19: "①在和陌生人的交往中，您印象最深的事是什么？②从这些事例中，您总结出了哪些与陌生人交往的技巧？③为帮助我们更好地与陌生人交往，您还有哪些建议？",
    20: "示例一：曹雪芹家道巨变，却磨砺出傲岸的风骨；备受冷遇，却迸发出创作的激情；绳床瓦灶，却熔铸成生命的华章。“十年辛苦不寻常”终换成彪炳千秋的文学巨著，这难道不是苦难带给他的人生意义吗？\n\n示例二：贝多芬童年不幸，却不曾破灭人生的梦想；恋人远离，却不曾消逝心中的激情；耳疾侵扰，却不曾消泯对音乐的执着。即使在最恶劣的境遇中，他也把痛苦转换为精神的欢乐。这不就是苦难带给他的人生意义吗？\n\n示例三：大卫·科波菲尔受尽继父的毒打与折磨，饱尝童工的劳苦与屈辱，经历世俗的狡诈与险恶，但这些不都没有改变他“永不卑贱、永不虚伪、永不残忍”的人生信念吗？",
}


def main() -> int:
    image_a = SOURCE_DIR / "43271_112214_466277.jpg"
    image_b = SOURCE_DIR / "43271_112216_217968.jpg"
    gallery = SOURCE_DIR / "index.html"
    for path in (image_a, image_b, gallery):
        if not path.exists():
            raise SystemExit(f"missing source artifact: {path}")
    image_a_sha = sha_bytes(image_a.read_bytes())
    image_b_sha = sha_bytes(image_b.read_bytes())
    gallery_sha = sha_bytes(gallery.read_bytes())
    rows = []
    for qid in range(1, 21):
        text = ANSWERS[qid]
        source_image = image_a if qid <= 13 else image_b
        rows.append({
            "schema_version": "exam-reference-answer-candidate-0.1",
            "candidate_id": f"GK-SC-2013-Q{qid:03d}-SINA-IMAGE-ANSWER",
            "exam_id": "GK-SC-2013",
            "question_id": qid,
            "source_role": "answer_scoring_candidate",
            "candidate_status": "candidate_unverified",
            "candidate_scope": "third_party_sina_image_transcription_q1_q20",
            "source_authority_status": "unverified_third_party_reprint",
            "source_registry_id": "SRC-GK-2013-SC-SINA-IMAGE-ANSWER",
            "source_status": "unverified_third_party_reprint",
            "answer_source_status": "external_image_candidate",
            "scoring_status": "not_available_as_official",
            "mapping_level": "M0",
            "kp_id": "N/A",
            "answer_candidate_text": text,
            "answer_candidate_sha256": sha_text(text),
            "transcription_status": "manual_visual_transcription_candidate",
            "source_image": rel(source_image),
            "source_image_sha256": sha_bytes(source_image.read_bytes()),
            "source_gallery_html": rel(gallery),
            "source_gallery_html_sha256": gallery_sha,
            "source_gallery_url": "http://slide.edu.sina.com.cn/slide_11_43271_17944.html",
            "source_article_url": "http://edu.sina.com.cn/gaokao/2013-06-09/1337383931.shtml",
            "source_answer_index": "Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/answer_index.jsonl",
            "review_status": "needs_independent_review",
            "notes": [
                "新浪教育/新浪高清图集第三方转载；图像带水印，不是官方原始扫描件。",
                "Q1-Q20 为图像中的参考答案/评分示例转录；Q21 作文未见独立答案。",
                "本候选层不写回主 answer_index，不标记 official_verified，也不生成官方评分标准。",
            ],
        })
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        "---\n"
        'schema_version: "exam-reference-answer-candidate-0.1"\n'
        'status: "candidate_only_partial"\n'
        'authority_status: "unverified_third_party_reprint"\n'
        'coverage: "GK-SC-2013 Q1-Q20 image transcription; Q21 missing"\n'
        'scoring_status: "not_available_as_official"\n'
        'mapping_status: "M0 | kp_id=N/A"\n'
        "---\n\n"
        "# 2013 四川卷参考答案候选（独立图像来源）\n\n"
        "> 来源是新浪教育/新浪高清图集的第三方转载图像，带水印。Q1—Q20 已建立人工视觉转录候选；Q21 作文无独立答案。该层不改变主答案索引的 21 条 `missing`，不提供官方评分标准。\n\n"
        f"- 图集 HTML：`{rel(gallery)}`，SHA-256 `{gallery_sha}`。\n"
        f"- Q1—Q13 图像：`{rel(image_a)}`，SHA-256 `{image_a_sha}`。\n"
        f"- Q14—Q20 图像：`{rel(image_b)}`，SHA-256 `{image_b_sha}`。\n"
        f"- 派生 JSONL：`{rel(OUT)}`；记录数 20；Q21：仍缺失。\n",
        encoding="utf-8",
    )
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps({
        "schema_version": "exam-reference-answer-candidate-receipt-0.1",
        "receipt_id": "EXAM-REFERENCE-ANSWER-GK-SC-2013-20260809",
        "exam_id": "GK-SC-2013",
        "source_registry_id": "SRC-GK-2013-SC-SINA-IMAGE-ANSWER",
        "source_authority_status": "unverified_third_party_reprint",
        "coverage": {"candidate_questions": list(range(1, 21)), "missing_questions": [21]},
        "source_gallery_html": rel(gallery),
        "source_gallery_html_sha256": gallery_sha,
        "source_images": {"q1_q13": {"path": rel(image_a), "sha256": image_a_sha}, "q14_q20": {"path": rel(image_b), "sha256": image_b_sha}},
        "output": rel(OUT),
        "output_sha256": sha_bytes(OUT.read_bytes()),
        "report": rel(REPORT),
        "raw_source_mutation": False,
        "answer_index_mutation": False,
        "scoring_status": "not_available_as_official",
        "mapping_status": "M0 | kp_id=N/A",
        "policy": "图像转录仅作独立候选，须与题卷、其他来源和评分材料交叉复核后方可用于知识点映射。",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "missing": [21], "output": rel(OUT), "report": rel(REPORT), "receipt": rel(RECEIPT)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
