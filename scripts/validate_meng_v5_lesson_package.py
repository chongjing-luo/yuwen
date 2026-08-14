#!/usr/bin/env python3
"""Deterministic contracts for the 《氓》 V5 text-spine lesson package."""

from __future__ import annotations

import argparse
import json
import re
import zipfile
from pathlib import Path
from typing import Iterable


EXPECTED_LINES = (
    "氓之蚩蚩，抱布贸丝",
    "匪来贸丝，来即我谋",
    "送子涉淇，至于顿丘",
    "匪我愆期，子无良媒",
    "将子无怒，秋以为期",
    "乘彼垝垣，以望复关",
    "不见复关，泣涕涟涟",
    "既见复关，载笑载言",
    "尔卜尔筮，体无咎言",
    "以尔车来，以我贿迁",
    "桑之未落，其叶沃若",
    "于嗟鸠兮，无食桑葚",
    "于嗟女兮，无与士耽",
    "士之耽兮，犹可说也",
    "女之耽兮，不可说也",
    "桑之落矣，其黄而陨",
    "自我徂尔，三岁食贫",
    "淇水汤汤，渐车帷裳",
    "女也不爽，士贰其行",
    "士也罔极，二三其德",
    "三岁为妇，靡室劳矣",
    "夙兴夜寐，靡有朝矣",
    "言既遂矣，至于暴矣",
    "兄弟不知，咥其笑矣",
    "静言思之，躬自悼矣",
    "及尔偕老，老使我怨",
    "淇则有岸，隰则有泮",
    "总角之宴，言笑晏晏",
    "信誓旦旦，不思其反",
    "反是不思，亦已焉哉",
)

THREE_QUESTIONS = (
    "她怎样从“送子涉淇”一步步走到“亦已焉哉”？",
    "她婚后的日子，究竟苦在哪里？",
    "这场婚姻为什么会走到这一步？谁应为伤害负责？当她说出“亦已焉哉”，还要面对哪些阻力？",
)

FIRST_VIEW_BANNED = ("警告信号", "伪装", "恋爱脑", "信息遮蔽")
FRONTSTAGE_BANNED = (
    "学生角色",
    "林晓",
    "三轨接收",
    "本页意图",
    "评估标准",
    "不填表",
    "不概括",
    "建立理解链",
    "责任线",
    "困境线",
    "关系结构",
    "观察维度",
    "现代生活转述",
    "解释边界",
    "共同回收",
    "建线",
    "关系过程｜现实处境",
    "这场伤害首先不是因为她",
    "迟迟难以抽身",
    "真正改变她命运",
    "真正的转折",
    "两类判断",
    "热烈可能遮住一部分不安",
)
NOTE_BANNED = (
    "为什么没有更早走开",
    "她为什么迟迟难以抽身",
    "热烈可能让人把不安解释成深情",
)
NOTE_MARKERS = (
    "【承接上一页】",
    "【教师原话】",
    "【学生动作与等待】",
    "【可观察证据】",
    "【明确切页句】",
)
PROMPT_NOTE_MARKERS = {
    "initial_compare": "初读记录",
    "q1_activity": "独立排序",
    "mapping_prompt": "现代生活转述",
    "responsibility_build": "责任",
    "difficulty_build": "四格",
    "retrospective": "事实、合理推断",
    "relation": "长期观察",
}
PARTICIPATION_NOTE_MARKERS = {
    "story_prepare": ("独立", "小组"),
    "story_relay": ("接力", "听众"),
    "story_turning": ("每名学生", "全班"),
    "story_revise": ("个人", "修订"),
    "scene_choose": ("每名学生", "小组"),
    "scene_build": ("小组", "生活镜头"),
    "scene_present": ("听众", "诗句"),
    "scene_reflect": ("独立", "同桌"),
    "scene_revise": ("个人", "修改"),
    "responsibility_choose": ("每名学生", "小组"),
    "responsibility_challenge": ("另一组", "原句"),
    "difficulty_discuss": ("小组", "诗句"),
    "difficulty_present": ("听众", "修改"),
    "marriage_write": ("每名学生", "原诗"),
    "marriage_share": ("同桌", "全班"),
    "marriage_after": ("学生原话", "修订"),
}
REQUIRED_PARTICIPATION_KINDS = tuple(PARTICIPATION_NOTE_MARKERS)
AI_CHECKING_TEMPLATE = "保留一处，修正一处，并为修改补回原句"


def _contains_all(text: str, markers: Iterable[str]) -> bool:
    return all(marker in text for marker in markers)


def validate_data_contract(data: dict) -> list[str]:
    errors: list[str] = []
    if data.get("version") != "5.3-literary-participation":
        errors.append("version must be 5.3-literary-participation")

    lines = [item.get("original") for item in data.get("lines", [])]
    if len(lines) != 30:
        errors.append(f"30组诗句 required, found {len(lines)}")
    for position, expected in enumerate(EXPECTED_LINES, 1):
        if position > len(lines) or lines[position - 1] != expected:
            errors.append(f"L{position:02d} missing or out of order: {expected}")

    units = data.get("meaning_units", [])
    if len(units) != 12:
        errors.append(f"12个意义句群 required, found {len(units)}")

    modules = data.get("modules", [])
    module_minutes = sum(int(item.get("minutes", 0)) for item in modules)
    if len(modules) != 5:
        errors.append(f"five modules required, found {len(modules)}")
    if data.get("total_minutes") != 274 or module_minutes != 274:
        errors.append(
            f"natural time must be 274 minutes; total={data.get('total_minutes')} modules={module_minutes}"
        )

    if tuple(data.get("three_questions", [])) != THREE_QUESTIONS:
        errors.append("three_questions must use the approved V5 wording")

    causal = data.get("causal_lines", {})
    responsibility = set(causal.get("responsibility", []))
    difficulty = set(causal.get("difficulty", []))
    if not any("时代" in item for item in difficulty):
        errors.append("现实阻力讨论必须明确回答Q3中的时代条件")
    for source, target in causal.get("links", []):
        if source in difficulty and target in responsibility:
            errors.append(f"责任线与困境线不得相互致因: {source} -> {target}")

    slides = data.get("slides", [])
    kinds = {slide.get("kind") for slide in slides}
    for required_kind in REQUIRED_PARTICIPATION_KINDS:
        if required_kind not in kinds:
            errors.append(f"真实参与 activity stage missing: {required_kind}")
    has_first_read = "first_full_read" in kinds or any(
        slide.get("kind") == "full_read" and slide.get("phase") == "opening" for slide in slides
    )
    has_final_read = "final_full_read" in kinds or any(
        slide.get("kind") == "full_read" and slide.get("phase") == "final" for slide in slides
    )
    if not has_first_read:
        errors.append("first uninterrupted full reading is required")
    if not has_final_read:
        errors.append("final full rereading is required")

    expected_process = (
        "相识议婚", "等待成婚", "迁嫁食贫", "长期劳作",
        "失信粗暴", "家人不解", "核验誓言", "停止判断",
    )
    q1_prompts = [slide for slide in slides if slide.get("kind") == "q1_activity"]
    if q1_prompts and tuple(q1_prompts[0].get("items", [])) == expected_process:
        errors.append("Q1排序问题页不得按正确顺序提前泄漏答案")

    for prompt_kind, return_kind, label in (
        ("responsibility_build", "responsibility_line", "责任线"),
        ("difficulty_build", "difficulty_line", "困境线"),
    ):
        prompts = [index for index, slide in enumerate(slides) if slide.get("kind") == prompt_kind]
        returns = [index for index, slide in enumerate(slides) if slide.get("kind") == return_kind]
        if returns and (not prompts or prompts[0] >= returns[0]):
            errors.append(f"{label}必须先有独立问题态，再出现回收态")

    for index, question in enumerate(THREE_QUESTIONS, 1):
        question_label = ("一", "二", "三")[index - 1]
        opening = [
            slide for slide in slides
            if slide.get("kind") == "question"
            and slide.get("phase") == "opening"
            and slide.get("question_index") == index
        ]
        returned = [
            slide for slide in slides
            if slide.get("kind") == "question"
            and slide.get("phase") == "return"
            and slide.get("question_index") == index
        ]
        if len(opening) != 1 or opening[0].get("visible") != question:
            errors.append(f"第{question_label}问 opening page missing or wording differs")
        if len(returned) != 1 or returned[0].get("visible") != question:
            errors.append(f"第{question_label}问 return page must use 同措辞")

    for page, slide in enumerate(slides, 1):
        slide_id = slide.get("id", f"P{page}")
        visible = str(slide.get("visible", ""))
        for phrase in FRONTSTAGE_BANNED:
            if phrase in visible:
                errors.append(f"{slide_id} frontstage contains banned phrase: {phrase}")
        if slide.get("phase") == "opening" or slide.get("kind") == "first_full_read":
            for phrase in FIRST_VIEW_BANNED:
                if phrase in visible:
                    errors.append(f"{slide_id} 首次阅读提前出现 {phrase}")

        notes = str(slide.get("notes", ""))
        for phrase in NOTE_BANNED:
            if phrase in notes:
                errors.append(f"{slide_id} 逐字稿 contains banned victim-delay framing: {phrase}")
        if len(notes) < 180 or not _contains_all(notes, NOTE_MARKERS):
            errors.append(f"{slide_id} 逐字稿 too short or missing performable markers")
        if AI_CHECKING_TEMPLATE in notes:
            errors.append(f"{slide_id} 仍含重复AI式核对模板")
        participation_markers = PARTICIPATION_NOTE_MARKERS.get(slide.get("kind"))
        if participation_markers and not _contains_all(notes, participation_markers):
            errors.append(
                f"{slide_id} 真实参与脚本缺少 {'/'.join(participation_markers)}"
            )
        is_timed_prompt = slide.get("phase") == "question" or slide.get("kind") == "initial_compare"
        if is_timed_prompt and slide.get("kind") in PROMPT_NOTE_MARKERS:
            minutes = int(slide.get("minutes", 0))
            expected_time = f"总用时{minutes}分钟"
            if minutes <= 0 or expected_time not in notes:
                errors.append(f"{slide_id} 综合活动动作总时长必须与标称{minutes}分钟一致")
            marker = PROMPT_NOTE_MARKERS[slide.get("kind")]
            if marker not in notes:
                errors.append(f"{slide_id} 综合活动必须使用与任务匹配的专用脚本: {marker}")
        if slide.get("kind") == "chapter_text":
            if slide.get("phase") == "chapter" and "学生闭书" in notes:
                errors.append(f"{slide_id} 章首页不得在逐句教学前要求闭书概括")
            if slide.get("phase") == "end" and "学生闭书" not in notes:
                errors.append(f"{slide_id} 章末页必须回收闭书连续章意")
        if slide.get("kind") == "question" and slide.get("phase") == "return" and "六章之后" in notes:
            errors.append(f"{slide_id} 全文后回收页不得仍使用开场转场")
        if slide.get("kind") in {"responsibility_line", "difficulty_line"} and "核对" not in notes:
            errors.append(f"{slide_id} 答案回收页备注必须先核对学生已有产出")
        if slide.get("kind") == "module_reconnect" and slide.get("module") == "M5" and "下一章" in notes:
            errors.append(f"{slide_id} 模块五重连后应转入Q3，不得转入下一章")
        if slide.get("kind") == "full_read" and slide.get("phase") == "final" and not slide.get("continues") and "进入第一章" in notes:
            errors.append(f"{slide_id} 最终朗读后不得错误返回第一章")
        if slide.get("kind") in {"background", "mark", "checkpoint"} and "现在只处理这一页" in notes:
            errors.append(f"{slide_id} 支架页仍为无内容的通用逐字稿")

    return errors


def validate_markdown_contract(texts: dict[str, str]) -> list[str]:
    errors: list[str] = []
    required_files = ("lesson", "worksheet", "script", "audit")
    for label in required_files:
        if not texts.get(label):
            errors.append(f"{label} markdown missing")

    lesson = texts.get("lesson", "")
    for marker in ("5.3-literary-participation", "30组诗句", "12个意义句群", "274分钟", "接力讲述", "生活镜头", "婚姻圆桌"):
        if marker not in lesson:
            errors.append(f"lesson missing {marker}")
    for line in EXPECTED_LINES:
        if line not in lesson:
            errors.append(f"lesson missing original line: {line}")
    for question in THREE_QUESTIONS:
        if question not in lesson:
            errors.append(f"lesson missing question: {question}")

    worksheet = texts.get("worksheet", "")
    for marker in ("把她的一生讲出来", "让诗句重新长成日子", "先把责任说清", "把一句提醒留给后来人"):
        if marker not in worksheet:
            errors.append(f"worksheet missing {marker}")
    for question in THREE_QUESTIONS:
        if question not in worksheet:
            errors.append(f"worksheet missing question: {question}")
    for phrase in ("真正改变她命运", "她转身时面对的阻力"):
        if phrase in worksheet:
            errors.append(f"worksheet contains outdated framing: {phrase}")
    if "我认为最重要的转折是" not in worksheet:
        errors.append("worksheet missing non-deterministic turning-point prompt")

    script = texts.get("script", "")
    if not _contains_all(script, NOTE_MARKERS):
        errors.append("script missing performable note markers")
    if "三问重新回来了。下一页，先把第一问读完整" not in script:
        errors.append("script P89 must transition to question one before story relay")

    audit = texts.get("audit", "")
    for marker in (
        "桌面模拟",
        "不是真实课堂数据",
        "学生角色：林晓",
        "接收到了什么信息",
        "参加了什么活动",
        "可能怎样思考",
        "形成了什么收获",
        "可观察证据",
        "接力讲述",
        "生活镜头",
        "婚姻圆桌",
    ):
        if marker not in audit:
            errors.append(f"audit missing {marker}")
    return errors


def _numbered_members(archive: zipfile.ZipFile, pattern: re.Pattern[str]) -> list[tuple[int, str]]:
    members: list[tuple[int, str]] = []
    for name in archive.namelist():
        match = pattern.fullmatch(name)
        if match:
            members.append((int(match.group(1)), name))
    return sorted(members)


def validate_pptx_contract(
    path: Path,
    expected_slide_count: int | None = None,
    first_view_pages: set[int] | None = None,
) -> list[str]:
    errors: list[str] = []
    first_view_pages = first_view_pages or set()
    try:
        with zipfile.ZipFile(path) as archive:
            slides = _numbered_members(archive, re.compile(r"ppt/slides/slide(\d+)\.xml"))
            notes = _numbered_members(archive, re.compile(r"ppt/notesSlides/notesSlide(\d+)\.xml"))
            if expected_slide_count is not None and len(slides) != expected_slide_count:
                errors.append(f"slide count expected {expected_slide_count}, found {len(slides)}")
            if len(slides) != len(notes):
                errors.append(f"notes count mismatch: slides={len(slides)} notes={len(notes)}")

            note_map = {page: name for page, name in notes}
            for page, name in slides:
                text = archive.read(name).decode("utf-8", errors="ignore")
                for phrase in FRONTSTAGE_BANNED:
                    if phrase in text:
                        errors.append(f"P{page} frontstage contains banned phrase: {phrase}")
                if page in first_view_pages:
                    for phrase in FIRST_VIEW_BANNED:
                        if phrase in text:
                            errors.append(f"P{page} first view contains {phrase}")
                note_name = note_map.get(page)
                if note_name:
                    note_text = archive.read(note_name).decode("utf-8", errors="ignore")
                    if len(note_text) < 180 or not _contains_all(note_text, NOTE_MARKERS):
                        errors.append(f"P{page} notes are not a performable script")
    except (OSError, zipfile.BadZipFile) as exc:
        errors.append(f"cannot open pptx: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path)
    parser.add_argument("--lesson", type=Path)
    parser.add_argument("--worksheet", type=Path)
    parser.add_argument("--script", type=Path)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--pptx", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    data: dict | None = None
    if args.data:
        data = json.loads(args.data.read_text(encoding="utf-8"))
        errors.extend(validate_data_contract(data))
    if all((args.lesson, args.worksheet, args.script, args.audit)):
        texts = {
            "lesson": args.lesson.read_text(encoding="utf-8"),
            "worksheet": args.worksheet.read_text(encoding="utf-8"),
            "script": args.script.read_text(encoding="utf-8"),
            "audit": args.audit.read_text(encoding="utf-8"),
        }
        errors.extend(validate_markdown_contract(texts))
    if args.pptx:
        expected = len(data.get("slides", [])) if data else None
        first_pages = {
            index for index, slide in enumerate(data.get("slides", []), 1)
            if slide.get("phase") == "opening" or slide.get("kind") == "first_full_read"
        } if data else set()
        errors.extend(validate_pptx_contract(args.pptx, expected, first_pages))

    if errors:
        for error in errors:
            print(f"ERROR\t{error}")
        return 1
    print("OK\tMeng V5 contracts passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
