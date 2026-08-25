import json
import re
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "work/teaching/必修上册/沁园春长沙"
LESSON_PATH = COURSE / "lesson.json"
DESIGN_PATH = COURSE / "教学设计.md"
G1_LOCK_PATH = COURSE / "_meta/lesson_plan_lock.json"

pytestmark = pytest.mark.skipif(
    not (G1_LOCK_PATH.is_file() and LESSON_PATH.is_file() and DESIGN_PATH.is_file()),
    reason="《沁园春·长沙》当前没有完整S3审批候选",
)


@pytest.fixture(scope="module")
def lesson():
    return json.loads(LESSON_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def pages(lesson):
    return {page["page_id"]: page for page in lesson["pages"]}


@pytest.fixture(scope="module")
def g1():
    return json.loads(G1_LOCK_PATH.read_text(encoding="utf-8"))["contract"]


def frontstage(page):
    return {item["id"]: item for item in page["slide_design"]["frontstage_elements"]}


def visible_text(page, state_id="B0"):
    elements = frontstage(page)
    state = next(item for item in page["slide_design"]["information_states"] if item["id"] == state_id)
    return "｜".join(elements[element_id]["text"] for element_id in state["visible_element_ids"])


def literary_lines(page):
    value = page["literary_object"]
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return value
    return value.get("lines", []) if isinstance(value, dict) else []


def test_current_candidate_has_28_pages_and_g1_time_stage_contract(lesson, g1):
    assert lesson["schema_version"] == "2.2"
    assert [page["page_id"] for page in lesson["pages"]] == [
        f"QYC-S3-{index:03d}" for index in range(1, 29)
    ]
    assert sum(page["minutes"] for page in lesson["pages"]) == g1["total_minutes"] == 135
    assert lesson["target_natural_minutes"] == 135
    assert lesson["lesson_plan_scope"]["stage_ids"] == ["P0", "P1", "P2", "P3", "P4"]


def test_three_period_boundaries_are_real_page_boundaries(lesson):
    elapsed = 0
    boundaries = {}
    for page in lesson["pages"]:
        elapsed += page["minutes"]
        if elapsed in {45, 90, 135}:
            boundaries[elapsed] = page["page_id"]
    assert boundaries == {45: "QYC-S3-011", 90: "QYC-S3-020", 135: "QYC-S3-028"}

    design = DESIGN_PATH.read_text(encoding="utf-8")
    assert "第一课时" in design and "第二课时" in design and "第三课时" in design
    assert "QYC-S3-001—QYC-S3-011" in design
    assert "QYC-S3-012—QYC-S3-020" in design
    assert "QYC-S3-021—QYC-S3-028" in design


def test_g1_scope_is_preserved_including_k15_and_empty_questions(lesson, g1):
    expected_teachable = {
        item["kid"]
        for item in g1["knowledge_items"]
        if item["status"] in {"must_teach", "retrieve_prior"}
    }
    expected_deferred = {
        item["kid"] for item in g1["knowledge_items"] if item["status"] == "defer"
    }
    assert set(lesson["lesson_plan_scope"]["knowledge_ids"]) == expected_teachable
    assert set(lesson["lesson_plan_scope"]["deferred_ids"]) == expected_deferred == {"K09"}
    assert "K15" in lesson["lesson_plan_scope"]["knowledge_ids"]
    assert "KP-CARD-B1-U01-01-010" in lesson["kp_scope"]["kp_ids"]
    assert lesson["three_questions"] == []
    assert lesson["lesson_plan_scope"]["question_ids"] == []


def test_no_old_42_page_or_200_minute_contract_survives(lesson):
    raw = json.dumps(lesson, ensure_ascii=False)
    page_numbers = {int(number) for number in re.findall(r"QYC-S3-(\d{3})", raw)}
    assert page_numbers <= set(range(1, 29))
    for forbidden in ("80至150", "一周后", "延迟回取", "200分钟", "P5各句"):
        assert forbidden not in raw


def test_all_25_meaning_units_are_anchored_in_sequential_close_reading(lesson):
    canonical = lesson["text_contract"]["canonical_lines"]
    close_reading = lesson["pages"][3:20]
    anchored = "".join(line for page in close_reading for line in literary_lines(page))
    missing = [line for line in canonical if line not in anchored]
    assert missing == []
    assert close_reading[0]["page_id"] == "QYC-S3-004"
    assert close_reading[-1]["page_id"] == "QYC-S3-020"


def test_complete_poem_is_heard_before_background_or_analysis(lesson, pages):
    first = pages["QYC-S3-001"]
    spoken = first["script"]["teacher_spoken"]
    assert all(line in spoken for line in lesson["text_contract"]["canonical_lines"])
    assert first["activity_contract"]["primary_type"] == "AC01"
    assert not any(term in visible_text(first) for term in ("毛泽东", "1925", "豪迈", "主旨"))
    assert pages["QYC-S3-002"]["lesson_kids"] == ["K14", "K15"]


def test_title_genre_and_coordinates_are_retrieved_before_reveal(pages):
    page = pages["QYC-S3-002"]
    assert not any(
        term in visible_text(page)
        for term in ("沁园春：词牌", "长沙：题目", "毛泽东", "1925")
    )
    segments = page["script"]["script_segments"]
    wait_index = next(i for i, segment in enumerate(segments) if segment["kind"] == "wait")
    calibration_index = next(i for i, segment in enumerate(segments) if segment["kind"] == "calibration")
    assert wait_index < calibration_index
    assert all(term in page["script"]["teacher_spoken"] for term in ("词牌", "题目", "毛泽东", "1925"))


def test_initial_diagnosis_includes_real_pronunciation_and_reading_breaks(pages):
    page = pages["QYC-S3-003"]
    raw = json.dumps(page, ensure_ascii=False)
    assert all(item in raw for item in ("舸 gě", "怅 chàng", "遒 qiú", "遏 è"))
    assert "一处个人朗读断点" in page["artifact"]
    assert "舸 gě" not in visible_text(page, "B0")
    calibration = [segment for segment in page["script"]["script_segments"] if segment["kind"] == "calibration"]
    assert calibration and calibration[0]["enter_trigger"] == "after_secondary_artifact_committed"


def test_upper_stanza_preserves_scene_question_and_background_boundary(pages):
    assert pages["QYC-S3-004"]["title"] == "一人，一洲，一江"
    assert all(kid in pages["QYC-S3-007"]["lesson_kids"] for kid in ("K01", "K03", "K04", "K08"))
    q011 = pages["QYC-S3-011"]
    spoken = q011["script"]["teacher_spoken"]
    assert all(item in spoken for item in ("怅", "沉浮", "暂悬", "1925", "不能替"))
    assert "时代坐标" not in visible_text(q011, "B0")
    q012 = pages["QYC-S3-012"]
    combined = " ".join((q012["artifact"], q012["script"]["teacher_spoken"], q012["script"]["student_process"]))
    assert "上阕" in combined and "不看参考译文" in combined


def test_lower_stanza_reaches_collective_voice_and_literary_boundary(pages):
    titles = [pages[f"QYC-S3-{index:03d}"]["title"] for index in range(13, 21)]
    assert titles == [
        "从一个人走进共同旧游",
        "‘恰’从哪里领起",
        "‘书生意气，挥斥方遒’怎样理解",
        "‘指点、激扬’写的是哪些行动",
        "‘粪土当年万户侯’怎样译",
        "让一群少年从原词中站起来",
        "一声‘曾记否’，把人带到中流",
        "下阕：从共同回忆走向中流",
    ]
    q019 = json.dumps(pages["QYC-S3-019"], ensure_ascii=False)
    assert all(item in q019 for item in ("百侣", "我们", "击水指游泳", "夸张", "诗性回应", "具体史事"))
    q020 = " ".join(
        (
            pages["QYC-S3-020"]["artifact"],
            pages["QYC-S3-020"]["script"]["teacher_spoken"],
            pages["QYC-S3-020"]["script"]["student_process"],
        )
    )
    assert "下阕" in q020 and "不看参考译文" in q020


def test_full_translation_and_overall_interpretation_preserve_individual_evidence(pages):
    q021 = pages["QYC-S3-021"]
    script = q021["script"]["teacher_spoken"]
    assert "A只看原词完整译述全文" in script
    assert "B从头完整译述" in script
    assert "参考译文" not in visible_text(q021, "B0")

    q024 = pages["QYC-S3-024"]
    assert q024["minutes"] >= 9
    assert set(("K10", "K11", "K12", "K13", "K14", "K16", "K17")) <= set(q024["lesson_kids"])
    spoken = q024["script"]["teacher_spoken"]
    assert all(item in spoken for item in ("至少三处短引", "1925", "作品通过", "不补成具体史事"))
    assert q024["activity_contract"]["participation_type"] == "PS01"


def test_structure_sort_does_not_reveal_order_or_relation_in_first_state(pages):
    page = pages["QYC-S3-022"]
    first = visible_text(page, "B0")
    correct = ["万类霜天竞自由", "谁主沉浮", "忆往昔峥嵘岁月稠", "浪遏飞舟"]
    positions = [first.index(item) for item in correct]
    assert positions != sorted(positions)
    assert "看见盛景→发问→回忆群像→中流回应" not in first
    assert "____→____→____→____" in first


def test_keyword_evidence_meets_the_three_distinct_word_requirement(pages):
    page = pages["QYC-S3-025"]
    raw = " ".join((page["artifact"], page["script"]["teacher_spoken"], page["script"]["observable_evidence"]))
    assert "至少三处不同关键词" in raw
    assert all(item in raw for item in ("画面", "意境", "情绪", "全文位置"))
    assert page["minutes"] >= 7


def test_reality_response_is_40_to_80_words_and_keeps_dissent(pages):
    page = pages["QYC-S3-027"]
    raw = json.dumps(page, ensure_ascii=False)
    assert "40—80字" in raw
    assert "80至150" not in raw
    assert all(item in raw for item in ("准确引文", "具体理解", "今天的启发"))
    assert page["activity_contract"]["participation_type"] == "PS03"
    assert all(item in raw for item in ("可以选择跳过", "保留分歧", "不必为了不同而强改"))
    assert page["next_use_ref"]["target_id"] == "QYC-S3-028"
    assert page["minutes"] >= 7


def test_three_long_writes_have_real_wait_time(pages):
    def wait_after_task(page, task_fragment):
        segments = page["script"]["script_segments"]
        task_index = next(
            index
            for index, segment in enumerate(segments)
            if segment["kind"] == "task" and task_fragment in segment["text"]
        )
        wait_segment = segments[task_index + 1]
        assert wait_segment["kind"] == "wait"
        wait_id = wait_segment["id"]
        return next(
            box["seconds"]
            for box in page["script"]["timeboxes"]
            if wait_id in box["segment_ids"]
        )

    assert wait_after_task(pages["QYC-S3-024"], "独立写一段全文解释") >= 240
    assert wait_after_task(pages["QYC-S3-025"], "选一处写成一段鉴赏") >= 150
    assert wait_after_task(pages["QYC-S3-027"], "独立写40到80字") >= 180


def test_q016_q017_q021_execution_contracts_are_single_state(pages):
    q016 = json.dumps(pages["QYC-S3-016"], ensure_ascii=False)
    assert "Q024" not in q016
    assert all(item in q016 for item in ("‘恰’的开放线", "双行动卡", "下阕声音理由"))

    q017 = json.dumps(pages["QYC-S3-017"], ensure_ascii=False)
    assert all(item in q017 for item in ("课文明写", "教材注释", "课文未写", "三类"))
    assert "两栏判断" not in q017 and "两层" not in q017

    q021 = json.dumps(pages["QYC-S3-021"], ensure_ascii=False)
    assert "两分半" not in q021 and "一百五十秒" not in q021
    assert q021.count("一百二十秒") >= 2
    first_translation_wait = next(
        box["seconds"]
        for box in pages["QYC-S3-021"]["script"]["timeboxes"]
        if box["segment_ids"] == ["S05"]
    )
    assert first_translation_wait >= 130


def test_explicit_spoken_times_fit_their_timeboxes(pages):
    assert "二十秒后停笔" not in json.dumps(pages["QYC-S3-005"], ensure_ascii=False)


def test_q013_artifact_is_retrieved_under_the_same_name(pages):
    assert "人物与时间箭头" in pages["QYC-S3-013"]["artifact"]
    target_script = "".join(
        segment["text"] for segment in pages["QYC-S3-018"]["script"]["script_segments"]
    )
    assert "取回人物与时间箭头" in target_script
    assert "人物关系图" not in json.dumps(pages["QYC-S3-018"], ensure_ascii=False)


def test_final_page_returns_to_full_poem_and_closes_without_new_task(pages):
    page = pages["QYC-S3-028"]
    assert page["next_use_ref"] == {
        "kind": "closure",
        "target_id": "lesson_closure",
        "use": page["next_use"],
    }
    raw = json.dumps(page, ensure_ascii=False)
    assert all(item in raw for item in ("完整读一次", "全文终读", "静默"))
    assert set(("K02", "K12", "K13")) == set(page["lesson_kids"])
    script_text = "".join(segment["text"] for segment in page["script"]["script_segments"])
    assert not any(term in script_text for term in ("共同生活", "愿意做", "今天的启发"))
    assert page["script"]["script_segments"][-1]["kind"] == "cut"
    assert "本课到这里" in page["script"]["script_segments"][-1]["text"]
    assert all(item in raw for item in ("上阕声音标记", "下阕声音理由", "背诵断点", "一字鉴赏", "回应中选定的原词"))
    assert "五份旧痕迹" in raw
    assert "三份旧" not in raw and "两处声音处理" not in raw


def test_replacement_states_really_remove_prior_elements(pages):
    q021_states = {
        state["id"]: state["visible_element_ids"]
        for state in pages["QYC-S3-021"]["slide_design"]["information_states"]
    }
    assert q021_states["B4"] == ["E08", "E09"]

    q028_states = {
        state["id"]: state["visible_element_ids"]
        for state in pages["QYC-S3-028"]["slide_design"]["information_states"]
    }
    assert q028_states["B1"] == ["E03"]
    assert q028_states["B2"] == ["E03", "E04"]


def test_every_task_is_followed_by_wait_and_calibration_is_post_answer(lesson):
    for page in lesson["pages"]:
        segments = page["script"]["script_segments"]
        for index, segment in enumerate(segments):
            if segment["kind"] == "task":
                assert segments[index + 1]["kind"] == "wait", page["page_id"]
            if segment["kind"] == "calibration":
                assert index > next(i for i, item in enumerate(segments) if item["kind"] == "wait")
                assert segment["enter_trigger"] in {
                    "after_primary_artifact_committed",
                    "after_secondary_artifact_committed",
                    "after_peer_response",
                }


def test_first_answer_states_never_contain_calibration_or_feedback(lesson):
    for page in lesson["pages"]:
        elements = frontstage(page)
        b0 = page["slide_design"]["information_states"][0]
        roles = {elements[element_id]["role"] for element_id in b0["visible_element_ids"]}
        assert roles.isdisjoint({"calibration", "feedback"}), page["page_id"]


def test_next_use_chain_is_forward_and_last_page_is_only_closure(lesson):
    ids = [page["page_id"] for page in lesson["pages"]]
    positions = {page_id: index for index, page_id in enumerate(ids)}
    for index, page in enumerate(lesson["pages"]):
        ref = page["next_use_ref"]
        if index == len(lesson["pages"]) - 1:
            assert ref["kind"] == "closure"
            assert ref["target_id"] == "lesson_closure"
        else:
            assert ref["kind"] == "page"
            assert positions[ref["target_id"]] > index


def test_every_next_use_is_spoken_as_a_real_retrieval_in_target_page(lesson):
    anchors = {
        1: (3, "最初留下的原词"),
        2: (24, "作者、1925年和教材坐标"),
        3: (21, "初读时画星的断点"),
        4: (12, "开篇站位"),
        5: (6, "‘看’字领起的范围"),
        6: (8, "江面位置"),
        7: (8, "鹰鱼位置"),
        8: (10, "观看路径"),
        9: (10, "换字辩护"),
        10: (11, "明丽竞发的秋景"),
        11: (12, "怅—问"),
        12: (28, "上阕声音标记"),
        13: (18, "人物与时间箭头"),
        14: (16, "‘恰’的开放线"),
        15: (16, "声音首稿"),
        16: (17, "‘恰’的开放线"),
        17: (18, "意动译句"),
        18: (20, "群像证据"),
        19: (20, "问话对象"),
        20: (21, "下阕译述"),
        21: (22, "全文译述"),
        22: (23, "结构链"),
        23: (24, "情感线"),
        24: (27, "全文解释"),
        25: (28, "一字鉴赏"),
        26: (28, "背诵断点"),
        27: (28, "回应中选定的原词"),
    }
    pages = {int(page["page_id"].rsplit("-", 1)[1]): page for page in lesson["pages"]}
    for source_number, (target_number, anchor) in anchors.items():
        assert pages[source_number]["next_use_ref"]["target_id"] == f"QYC-S3-{target_number:03d}"
        target_script = "".join(
            segment["text"] for segment in pages[target_number]["script"]["script_segments"]
        )
        assert anchor in target_script, (source_number, target_number, anchor)


def test_no_phantom_question_stale_page_id_or_foreign_template_language(lesson):
    raw = json.dumps(lesson, ensure_ascii=False)
    for forbidden in (
        "开课问题",
        "开课时留下的问题",
        "取回Q024",
        "现代标层",
        "婚姻",
    ):
        assert forbidden not in raw
    for page in lesson["pages"]:
        assert not re.search(r"QYC-S3-\d{3}|Q\d{3}", page["script"]["student_process"])


def test_student_frontstage_has_no_governance_or_student_persona_language(lesson):
    banned = (
        "G1",
        "G2",
        "KID",
        "机制节点",
        "学生画像",
        "林晓",
        "设计理由",
        "本页面用于",
        "今天不收集知识碎片",
        "不填表",
        "不概括",
    )
    for page in lesson["pages"]:
        text = "｜".join(item["text"] for item in page["slide_design"]["frontstage_elements"])
        assert not any(term in text for term in banned), (page["page_id"], text)


def test_human_design_is_current_candidate_and_contains_every_page_id(lesson):
    design = DESIGN_PATH.read_text(encoding="utf-8")
    assert 'status: "S3教学设计审批候选·待用户审批"' in design
    assert "28页、135分钟" in design
    assert "42页" not in design and "200分钟" not in design
    for page in lesson["pages"]:
        assert f"### {page['page_id']}　{page['title']}" in design
        assert "**教师逐字稿**" in design[design.index(page["page_id"]):]
    for page in lesson["pages"]:
        assert design.count(f"### {page['page_id']}　{page['title']}") == 1
