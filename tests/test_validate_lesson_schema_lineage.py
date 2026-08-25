from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from test_validate_lesson_plan import _lock as build_g1_lock  # noqa: E402
from validate_lesson_plan import canonical_json_sha256  # noqa: E402
from validate_lesson_schema import validate  # noqa: E402


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _lesson(tmp_path: Path) -> dict:
    g1_lock = build_g1_lock(tmp_path)
    g1_path = tmp_path / "work/teaching/lesson/_meta/lesson_plan_lock.json"
    g1_path.write_text(json.dumps(g1_lock, ensure_ascii=False, indent=2), encoding="utf-8")

    source = tmp_path / "Data/full.md"
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text("氓之蚩蚩，抱布贸丝", encoding="utf-8")
    card = tmp_path / "work/knowledge/测试册/cards/CARD-TEST-01.md"
    card.parent.mkdir(parents=True, exist_ok=True)
    card.write_text("KP-CARD-TEST-01-001", encoding="utf-8")
    category_source = (
        Path(__file__).resolve().parents[1]
        / "work/methodology/lesson-preparation/教学设计类别注册表.json"
    )
    category_target = (
        tmp_path / "work/methodology/lesson-preparation/教学设计类别注册表.json"
    )
    category_target.parent.mkdir(parents=True, exist_ok=True)
    category_target.write_bytes(category_source.read_bytes())
    objective = g1_lock["contract"]["objectives"][0]
    question = g1_lock["contract"]["questions"][0]
    return {
        "schema_version": "2.2",
        "lesson_id": "LES-TEST-01",
        "lesson_plan_binding": {
            "path": str(g1_path.relative_to(tmp_path)),
            "sha256": _sha(g1_path),
        },
        "lesson_plan_scope": {
            "objective_ids": ["O1"],
            "knowledge_ids": ["K01"],
            "deferred_ids": ["K02"],
            "question_ids": ["Q1"],
            "stage_ids": ["P0"],
            "contract_sha256": canonical_json_sha256(g1_lock["contract"]),
            "total_minutes": 5,
            "closing_mode": g1_lock["contract"]["closing_mode"],
        },
        "book_unit": {"card_refs": ["CARD-TEST-01"]},
        "text_contract": {
            "source_path": str(source.relative_to(tmp_path)),
            "source_sha256": _sha(source),
            "canonical_lines": ["氓之蚩蚩，抱布贸丝"],
        },
        "three_questions": [question["text"]],
        "objectives": [
            {
                "id": "O1",
                "dimension": "语言建构与运用",
                "statement": objective["statement"],
                "kp_refs": ["KP-CARD-TEST-01-001"],
                "nodes": ["K1", "U8"],
                "evidence_pages": ["T01"],
            }
        ],
        "kp_scope": {"kp_ids": ["KP-CARD-TEST-01-001"], "deferred": []},
        "pages": [
            {
                "page_id": "T01",
                "stage_id": "P0",
                "objective_ids": ["O1"],
                "lesson_kids": ["K01"],
                "title": "沿着原文看变化",
                "minutes": 5,
                "literary_object": "氓之蚩蚩，抱布贸丝",
                "previous_page_input": "学生刚听到开篇两句，尚未解释动作之间的关系。",
                "unique_difficulty": "学生容易只概括标签，忽略动作怎样推动人物关系。",
                "unique_function": "让学生从动作顺序中发现人物关系的第一处变化。",
                "first_view_contract": "B0只呈现‘氓之蚩蚩，抱布贸丝’和任务‘按顺序圈出动作’，不出现校准语。",
                "information_state": (
                    "B0（page_enter）可见：氓之蚩蚩，抱布贸丝｜按顺序圈出动作；"
                    "B1（after_primary_artifact_committed）新增可见：动作先后必须回到原词。"
                ),
                "student_action": ["按动作顺序复述并圈出依据"],
                "artifact": "一条带原词的复述",
                "real_wait": "教师静默巡视60秒，学生先独立圈画，不在首答前讲解。",
                "bounded_feedback": "只追问动作依据与先后，不公布人物品质结论。",
                "visible_revision": "学生用另一颜色补入遗漏动作并修订自己的复述。",
                "next_use": "课末收束取回复述并比较修订前后的证据变化。",
                "next_use_ref": {
                    "kind": "closure",
                    "target_id": "lesson_closure",
                    "use": "课末收束取回个人复述并完成证据修订。",
                },
                "normal_counterexample": "暂时看不懂的学生圈出最难解释的动作，不编造。",
                "visual_role": "放大原句并保存学生圈出的动作顺序。",
                "first_person_reception": "我用原词说明了这一处关系变化，并保留待修订处。",
                "deletion_loss": "后续比较失去个人首答。",
                "continuous_increment": "我比进页前多看见动作次序怎样改变两人的关系，并把疑问带到下一句。",
                "attention_budget": "一个主动作、一次依据追问、一次修订；记录位置固定在原句旁。",
                "story_return": "回到两人相遇的第一个动作。",
                "knowledge_payload": [
                    {
                        "kid": "K01",
                        "scope": "借开篇两个动作辨清人物关系第一次变化",
                        "page_role": "construct",
                    }
                ],
                "activity_contract": {
                    "primary_type": "AC05",
                    "secondary_types": [],
                    "teacher_move_types": ["TM03", "TM04"],
                    "learner_action_types": ["LA06", "LA09"],
                    "participation_type": "PS01",
                    "artifact_type": "EP06",
                    "sensory_channel_types": ["SC01", "SC04"],
                    "feedback_types": ["FB02", "FB04"],
                    "selection_reason": "动作关系必须由学生先圈出原词并自行解释，才能暴露真实断点。",
                    "knowledge_fit": "证据推理直接服务开篇动作关系，而不是用人物标签替代原句。",
                    "experience_fit": "学生先保留自己的猜测，再在追问中感到原词能够支持或限制解释。",
                },
                "student_experience": {
                    "perceives": "先只看见开篇原句和留出的圈画位置，没有现成关系结论。",
                    "thinks": "两个动作谁先谁后，人物为什么这样行动，原词能证明到哪一步。",
                    "possible_feeling": "可能先觉得句子直白，随后因动作目的并不明说而产生一点疑问。",
                    "does": "独立圈出动作，写一句复述，再依据追问补入遗漏的原词。",
                    "understands": "人物关系的解释必须从动作次序生长，不能只贴预设标签。",
                },
                "slide_design": {
                    "layout_type": "LT02",
                    "frontstage_elements": [
                        {"id": "E01", "text": "氓之蚩蚩，抱布贸丝", "role": "content"},
                        {"id": "E02", "text": "按顺序圈出动作", "role": "prompt"},
                        {"id": "E03", "text": "动作先后必须回到原词", "role": "calibration"},
                    ],
                    "information_states": [
                        {
                            "id": "B0",
                            "visible_element_ids": ["E01", "E02"],
                            "enter_trigger": "page_enter",
                        },
                        {
                            "id": "B1",
                            "visible_element_ids": ["E01", "E02", "E03"],
                            "enter_trigger": "after_primary_artifact_committed",
                        },
                    ],
                    "spatial_plan": "原句占左侧三分之二，右侧只留学生圈画与一句复述的位置。",
                    "information_hierarchy": "原句第一层，学生操作第二层，教师校准在首答后才出现。",
                    "reveal_sequence": "先出原句，静默圈画后再出现追问，学生修订后才揭示校准语。",
                    "layout_rationale": "让原词始终处于视觉主位，并用右侧空白保存学生首答与修订痕迹。",
                },
                "script": {
                    "transition_spoken": "我们已经听见开篇，现在先不急着评价人物，只看他们做了什么。",
                    "teacher_spoken": "请先沿动作顺序说清眼前发生了什么。动作先后必须回到原词，不以人物标签代替现场证据。",
                    "student_process": "学生静默圈出动词，独立写一句复述，再与原句逐字核对。",
                    "expected_responses": [
                        "先抱着布来换丝。",
                        "动作是抱布和贸丝，但来意可能还没有明说。",
                    ],
                    "timeboxes": [
                        {"label": "承接原句", "seconds": 20, "segment_ids": ["S01"]},
                        {"label": "发布圈画任务", "seconds": 25, "segment_ids": ["S02"]},
                        {"label": "独立圈画并留下首答", "seconds": 150, "segment_ids": ["S03"]},
                        {"label": "后置校准证据边界", "seconds": 40, "segment_ids": ["S04"]},
                        {"label": "依据反馈修订", "seconds": 45, "segment_ids": ["S05"]},
                        {"label": "切向下一动作", "seconds": 20, "segment_ids": ["S06"]},
                    ],
                    "branches": [
                        {"kind": "沉默", "response": "请先圈出原句动作"},
                        {"kind": "越界", "response": "请先回到原词依据"},
                    ],
                    "feedback_spoken": "先保留你的判断；请在旁边补上支持它的那个动词。",
                    "observable_evidence": "每名学生留下两个动作标记和一条能够回指原词的复述。",
                    "cut_spoken": "动作已经看清，下一步再问这些动作把人物关系带向哪里。",
                    "script_segments": [
                        {
                            "id": "S01",
                            "state_id": "B0",
                            "kind": "transition",
                            "enter_trigger": "page_enter",
                            "text": "我们已经听见开篇，现在先不急着评价人物，只看他们做了什么。",
                        },
                        {
                            "id": "S02",
                            "state_id": "B0",
                            "kind": "task",
                            "enter_trigger": "after_instruction",
                            "text": "请先沿动作顺序说清眼前发生了什么。",
                        },
                        {
                            "id": "S03",
                            "state_id": "B0",
                            "kind": "wait",
                            "enter_trigger": "after_instruction",
                            "text": "教师停止说话，等待学生独立圈画并留下首答。",
                        },
                        {
                            "id": "S04",
                            "state_id": "B1",
                            "kind": "calibration",
                            "enter_trigger": "after_primary_artifact_committed",
                            "text": "动作先后必须回到原词，不以人物标签代替现场证据。",
                        },
                        {
                            "id": "S05",
                            "state_id": "B1",
                            "kind": "feedback",
                            "enter_trigger": "after_primary_artifact_committed",
                            "text": "先保留你的判断；请在旁边补上支持它的那个动词。",
                        },
                        {
                            "id": "S06",
                            "state_id": "B1",
                            "kind": "cut",
                            "enter_trigger": "after_calibration",
                            "text": "动作已经看清，下一步再问这些动作把人物关系带向哪里。",
                        },
                    ],
                },
            }
        ],
        "claim_boundary": "课堂证据状态：未采集；学生掌握、理解与享受均待真实试教验证。",
    }


def _v23_direct_instruction_lesson(tmp_path: Path) -> dict:
    """A teacher-led event with no fabricated student task or instant artifact."""
    lesson = _lesson(tmp_path)
    lesson["schema_version"] = "2.3"
    page = lesson["pages"][0]
    page["first_view_contract"] = "B0只呈现‘氓之蚩蚩，抱布贸丝’，教师沿原词讲清‘蚩蚩’的语境义与人物初始形象。"
    page["student_action"] = ["学生对照原句倾听解释，并在心中修正对‘蚩蚩’的日常语感。"]
    page["next_use"] = "下一次释义检索要求学生脱离教师讲述解释‘蚩蚩’在句中的意思。"
    page["next_use_ref"]["use"] = "课末合书检索‘蚩蚩’的语境义，检查本次准确讲授是否进入理解。"
    for field in (
        "artifact",
        "real_wait",
        "bounded_feedback",
        "visible_revision",
        "normal_counterexample",
    ):
        page.pop(field)

    activity = page["activity_contract"]
    activity["event_type"] = "EV01"
    activity.pop("primary_type")
    activity["secondary_types"] = []
    activity["teacher_move_types"] = ["TM01"]
    activity["learner_action_types"] = ["LA03"]
    activity["participation_type"] = "PS08"
    activity.pop("artifact_type")
    activity["sensory_channel_types"] = ["SC01", "SC02"]
    activity["feedback_types"] = []
    activity["selection_reason"] = "这一语境义属于需要准确提供的规范知识，学生不能只凭现代口语稳定推出。"
    activity["knowledge_fit"] = "教师把词义限制在开篇原句与人物初始形象中，并把掌握检验留到后续合书检索。"
    activity["experience_fit"] = "学生不被迫制造一个首答，而是先听见准确解释，再在全文人物变化中检验这一初始印象。"

    page["student_experience"] = {
        "perceives": "学生眼前始终保留开篇原句，耳中听到词义如何从语境而不是字典标签中成立。",
        "thinks": "‘蚩蚩’在这里究竟写出了怎样的外在样子，它与后文人物变化有什么距离。",
        "possible_feeling": "原先熟悉却含混的词忽然有了具体语境，可能产生一种重新看见开篇的清晰感。",
        "does": "学生沿教师指向回看原词，把准确释义暂时放回人物初次出现的画面中。",
        "understands": "‘蚩蚩’不能只按现代口语猜测，它在本句中参与塑造人物最初呈现的样子。",
    }
    page["slide_design"] = {
        "layout_type": "LT02",
        "frontstage_elements": [
            {"id": "E01", "text": "氓之蚩蚩，抱布贸丝", "role": "content"},
        ],
        "information_states": [
            {
                "id": "B0",
                "visible_element_ids": ["E01"],
                "enter_trigger": "page_enter",
            }
        ],
        "spatial_plan": "开篇原句居中放大，教师讲述始终指回‘蚩蚩’，不另设任务区和答案卡。",
        "information_hierarchy": "原句是唯一视觉主位，准确释义由教师口头完成，屏幕不堆叠后台说明。",
        "reveal_sequence": "页面进入即见完整原句，教师沿词语和语境连续讲清，不制造虚假点击悬念。",
        "layout_rationale": "让学生在倾听准确讲授时始终能回看原词，使词义、人物形象与句中语境保持相连。",
    }
    page["information_state"] = (
        "B0（page_enter）可见：氓之蚩蚩，抱布贸丝。"
    )
    page["script"] = {
        "teacher_spoken": (
            "这里的‘蚩蚩’不是我们今天口语里的简单评价。请把眼睛留在开篇："
            "它先写一个看上去敦厚老实的人，抱着布来换丝。这个初次印象，后文会重新照亮。"
        ),
        "student_process": "学生对照开篇原句倾听，跟随教师的指向辨清词义和人物初次呈现。",
        "cut_spoken": "先把这个初次印象留住，继续看他为何抱布而来。",
        "timeboxes": [
            {"label": "沿原词准确讲授", "seconds": 260, "segment_ids": ["S01"]},
            {"label": "回到人物行动", "seconds": 40, "segment_ids": ["S02"]},
        ],
        "script_segments": [
            {
                "id": "S01",
                "state_id": "B0",
                "kind": "instruction",
                "enter_trigger": "page_enter",
                "text": (
                    "这里的‘蚩蚩’不是我们今天口语里的简单评价。请把眼睛留在开篇："
                    "它先写一个看上去敦厚老实的人，抱着布来换丝。这个初次印象，后文会重新照亮。"
                ),
            },
            {
                "id": "S02",
                "state_id": "B0",
                "kind": "cut",
                "enter_trigger": "page_enter",
                "text": "先把这个初次印象留住，继续看他为何抱布而来。",
            },
        ],
    }
    return lesson


def _v24_semantic_page_lesson(tmp_path: Path) -> dict:
    """A v2.4 page whose geometry is derived from semantic relations."""
    lesson = _v23_direct_instruction_lesson(tmp_path)
    lesson["schema_version"] = "2.4"
    page = lesson["pages"][0]
    page["slide_design"] = {
        "semantic_unit": "开篇完整句及‘蚩蚩’在人物初次呈现中的语境义",
        "organizing_intention": "让完整原句与当前聚焦词保持同屏，学生听讲时始终能把释义放回人物初次出场的语境。",
        "content_object_types": ["CO01", "CO03"],
        "semantic_relations": [
            {
                "type": "SR01",
                "element_ids": ["E01", "E02"],
                "rationale": "E02是对E01中‘蚩蚩’的局部解释，必须依附完整原句而不是脱离语境独立出现。",
            }
        ],
        "display_constraints": ["DC01", "DC03", "DC05"],
        "layout_operations": ["LO01", "LO02", "LO07"],
        "co_view_groups": [
            {
                "id": "G01",
                "element_ids": ["E01", "E02"],
                "rationale": "原句和语境义需要同时可见，学生才能在倾听时反复核对词义落点。",
            }
        ],
        "must_stage": [],
        "priority_layers": [
            {
                "level": "L1",
                "element_ids": ["E01"],
                "rationale": "完整原句是共同阅读的基底，始终处于首要层。",
            },
            {
                "level": "L2",
                "element_ids": ["E02"],
                "rationale": "局部释义依附原句，只在教师指向时成为当前焦点。",
            },
        ],
        "continuity_anchor": ["E01"],
        "density_judgment": {
            "semantic_completeness": "保留整句而非只截‘蚩蚩’，词义、动作和人物初次形象的上下文没有断裂。",
            "readability_focus": "画面只有完整原句与一条局部释义，主焦点明确，学生可以在正常字号下共同阅读。",
            "decision": "retain_as_page",
        },
        "boundary_rationale": "本页只建立开篇词义与初始形象；来意和人物后续变化需要新的阅读动作，留到下一事件展开。",
        "frontstage_elements": [
            {"id": "E01", "text": "氓之蚩蚩，抱布贸丝", "role": "content"},
            {"id": "E02", "text": "蚩蚩：忠厚老实的样子", "role": "content"},
        ],
        "information_states": [
            {
                "id": "B0",
                "visible_element_ids": ["E01", "E02"],
                "enter_trigger": "page_enter",
            }
        ],
        "information_hierarchy": "完整原句构成稳定基底，‘蚩蚩’的语境义作为依附注释，教师讲述只在两者之间移动注意。",
        "reveal_sequence": "页面进入即呈现完整语义单位；本页是准确讲授事件，不为制造悬念把规范释义拆成多次点击。",
        "layout_rationale": "学生需要共视完整原句和局部释义，才能把词义、人物形象与句中动作保持在同一理解场中。",
    }
    page["first_view_contract"] = (
        "B0同时呈现‘氓之蚩蚩，抱布贸丝’和‘蚩蚩：忠厚老实的样子’，教师沿完整原句讲清语境义。"
    )
    page["information_state"] = (
        "B0（page_enter）可见：氓之蚩蚩，抱布贸丝｜蚩蚩：忠厚老实的样子。"
    )
    return lesson


def _v25_visual_blueprint_lesson(tmp_path: Path) -> dict:
    """A v2.5 page whose physical screen and visual source are fully frozen in S3."""
    lesson = _v24_semantic_page_lesson(tmp_path)
    lesson["schema_version"] = "2.5"
    asset_path = tmp_path / "work/assets/textbook-portrait.jpg"
    asset_path.parent.mkdir(parents=True, exist_ok=True)
    asset_path.write_bytes(b"\xff\xd8\xff\xdbtextbook-portrait\xff\xd9")
    lesson["visual_source_profile"] = {
        "strategy": "textbook_first",
        "source_artifacts": [
            {
                "asset_id": "TB01",
                "path": "work/assets/textbook-portrait.jpg",
                "sha256": _sha(asset_path),
                "role": "教材中的人物身份肖像",
                "usage_boundary": "只作人物身份锚，不据此推断未被教材和原文证明的经历。",
            }
        ],
        "palette": [
            {"role": "paper", "hex": "F5EFE8", "source_basis": "教材暖白纸色"},
            {"role": "accent", "hex": "A64A3F", "source_basis": "教材篇名的低饱和赭红"},
        ],
        "image_style": "优先使用教材灰黑肖像；新增图形只提取椭圆裁框和低饱和纸本质感。",
        "shape_language": "细边框、椭圆人物锚和大片留白，不复制教材页码、水印或无关装饰。",
        "typography_tone": "篇名与原文使用端正宋体，任务文字使用清楚黑体，保持教材阅读气质。",
        "consistency_rules": [
            "人物身份只使用TB01或由TB01核验的一致资产。",
            "教材色调只作起点，投影对比度和原文可读性优先。",
        ],
        "fact_boundary": "教材图片证明人物身份和视觉语境，不证明正文没有写出的动作、表情或因果。",
    }
    page = lesson["pages"][0]
    page["slide_design"]["physical_screens"] = [
        {
            "screen_id": f"{page['page_id']}-B0",
            "state_id": "B0",
            "visible_element_ids": ["E01", "E02"],
            "screen_function": "让完整原句与局部释义在同一视野中接受准确讲授。",
            "composition_blueprint": "原句占左侧约七成并保持完整行宽，释义贴近关键词置于右侧窄栏。",
            "reading_path": "先读完整原句，再沿教师指向移到右侧释义，最后回到原句复读。",
            "spatial_proportions": "原文区70%，就近释义区22%，四周和两栏间留白8%。",
            "image_plan": {
                "decision": "forbidden",
                "function": "本屏以完整原句为主视觉，人物肖像会分散词义讲授的注意。",
                "derivation_mode": "none",
                "asset_refs": [],
                "content_brief": "不放置图片或装饰性图标。",
                "style_brief": "沿用教材暖白底、赭红小面积强调和灰黑正文。",
                "placement": "不设图片区域，留白服务原句停留。",
                "visual_weight": "完整原文保持唯一且最重的视觉权重。",
                "appearance_timing": "B0进入时即保持无图。",
                "fact_boundary": "不以插图替代原文或增添人物判断。",
            },
            "script_segment_refs": ["S01", "S02"],
        }
    ]
    return lesson


def _v26_page_role_lesson(tmp_path: Path) -> dict:
    """A v2.6 page whose presentation role is explicit but not a layout template."""
    lesson = _v25_visual_blueprint_lesson(tmp_path)
    lesson["schema_version"] = "2.6"
    page = lesson["pages"][0]
    page["slide_design"].update(
        {
            "presentation_role": "PG04",
            "role_rationale": "本页以完整原句和局部释义推进正文理解，属于沿原文展开的主干文本页。",
        }
    )
    return lesson


def test_v2_lesson_with_valid_g1_binding_passes(tmp_path: Path):
    errors, _, _ = validate(_lesson(tmp_path), strict=True, root=tmp_path)
    assert errors == []


def test_v23_direct_instruction_does_not_require_fake_task_or_artifact(tmp_path: Path):
    lesson = _v23_direct_instruction_lesson(tmp_path)
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert errors == []


def test_v24_semantic_page_contract_passes_without_fixed_layout_family(tmp_path: Path):
    lesson = _v24_semantic_page_lesson(tmp_path)
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert errors == []


def test_v25_requires_visual_source_profile_and_physical_screen_blueprint(tmp_path: Path):
    lesson = _v25_visual_blueprint_lesson(tmp_path)
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert errors == []


def test_v26_requires_registered_presentation_role_without_fixed_layout(tmp_path: Path):
    lesson = _v26_page_role_lesson(tmp_path)
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert errors == []


def test_v26_rejects_missing_or_unknown_presentation_role(tmp_path: Path):
    lesson = _v26_page_role_lesson(tmp_path)
    lesson["pages"][0]["slide_design"].pop("presentation_role")
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("presentation_role" in error for error in errors)

    lesson = _v26_page_role_lesson(tmp_path)
    lesson["pages"][0]["slide_design"]["presentation_role"] = "PG99"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("presentation_role未注册" in error for error in errors)


def test_v26_support_page_requires_trigger_and_return_contract(tmp_path: Path):
    lesson = _v26_page_role_lesson(tmp_path)
    design = lesson["pages"][0]["slide_design"]
    design["presentation_role"] = "PG05"
    design["role_rationale"] = "本页暂离原文补足理解所需的典故知识，学完后必须回到触发它的原句。"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("支撑页缺support_link" in error for error in errors)


def test_v26_structural_page_does_not_fake_objective_or_knowledge_payload(tmp_path: Path):
    lesson = _v26_page_role_lesson(tmp_path)
    page = lesson["pages"][0]
    page["objective_ids"] = []
    page["lesson_kids"] = []
    page["knowledge_payload"] = []
    page["literary_object"] = {"kind": "lesson_orientation"}
    page["slide_design"]["presentation_role"] = "PG01"
    page["slide_design"]["role_rationale"] = (
        "本页只确认课题与作者并完成课堂入场，不承担知识讲解或目标达成证据。"
    )
    page["slide_design"]["content_object_types"] = ["CO09"]

    errors, _, _ = validate(lesson, strict=True, root=tmp_path)

    assert not any("objective_ids必须为非空" in error for error in errors)
    assert not any("lesson_kids必须为非空" in error for error in errors)
    assert not any("knowledge_payload必须为非空" in error for error in errors)
    assert not any("PG01缺少匹配内容对象" in error for error in errors)


def test_v26_structural_page_rejects_fake_kid_binding(tmp_path: Path):
    lesson = _v26_page_role_lesson(tmp_path)
    page = lesson["pages"][0]
    page["slide_design"]["presentation_role"] = "PG03"
    page["slide_design"]["role_rationale"] = (
        "本页只标示新的文本范围与课堂阶段，知识形成将在后续主干页真实发生。"
    )
    page["slide_design"]["content_object_types"] = ["CO09"]

    errors, _, _ = validate(lesson, strict=True, root=tmp_path)

    assert any("定位结构页不得伪挂objective_ids" in error for error in errors)
    assert any("定位结构页不得伪挂lesson_kids" in error for error in errors)
    assert any("定位结构页不得伪造knowledge_payload" in error for error in errors)


def test_v26_structural_page_rejects_non_orientation_content_object(tmp_path: Path):
    lesson = _v26_page_role_lesson(tmp_path)
    page = lesson["pages"][0]
    page["objective_ids"] = []
    page["lesson_kids"] = []
    page["knowledge_payload"] = []
    page["slide_design"]["presentation_role"] = "PG02"
    page["slide_design"]["role_rationale"] = (
        "本页只显示课程路径与当前位置，不在此页讲解文本知识。"
    )
    page["slide_design"]["content_object_types"] = ["CO09", "CO03"]

    errors, _, _ = validate(lesson, strict=True, root=tmp_path)

    assert any("定位结构页只能登记CO09" in error for error in errors)


def test_v25_rejects_missing_visual_source_profile(tmp_path: Path):
    lesson = _v25_visual_blueprint_lesson(tmp_path)
    lesson.pop("visual_source_profile")
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("visual_source_profile" in error for error in errors)


def test_v25_physical_screens_must_exactly_project_states_and_scripts(tmp_path: Path):
    lesson = _v25_visual_blueprint_lesson(tmp_path)
    screen = lesson["pages"][0]["slide_design"]["physical_screens"][0]
    screen["visible_element_ids"] = ["E02"]
    screen["script_segment_refs"] = ["S99"]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("visible_element_ids必须与对应信息状态完全一致" in error for error in errors)
    assert any("script_segment_refs" in error for error in errors)


def test_v25_forbidden_image_screen_cannot_reference_asset(tmp_path: Path):
    lesson = _v25_visual_blueprint_lesson(tmp_path)
    image_plan = lesson["pages"][0]["slide_design"]["physical_screens"][0]["image_plan"]
    image_plan["asset_refs"] = ["TB01"]
    image_plan["derivation_mode"] = "direct_textbook_asset"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("forbidden画面不得引用图片资产" in error for error in errors)


def test_v25_visual_assets_must_exist_and_match_hash(tmp_path: Path):
    lesson = _v25_visual_blueprint_lesson(tmp_path)
    lesson["visual_source_profile"]["source_artifacts"][0]["sha256"] = "0" * 64
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("视觉来源资产sha256" in error for error in errors)


def test_v24_rejects_deprecated_fixed_layout_type(tmp_path: Path):
    lesson = _v24_semantic_page_lesson(tmp_path)
    lesson["pages"][0]["slide_design"]["layout_type"] = "LT02"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("slide_design含未知字段" in error for error in errors)


def test_v24_requires_real_co_view_and_continuity_constraints(tmp_path: Path):
    lesson = _v24_semantic_page_lesson(tmp_path)
    design = lesson["pages"][0]["slide_design"]
    design["co_view_groups"][0]["element_ids"] = ["E01", "E99"]
    design["continuity_anchor"] = ["E02"]
    design["information_states"].append(
        {"id": "B1", "visible_element_ids": ["E01"], "enter_trigger": "after_instruction"}
    )
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("co_view_groups" in error and "未知元素" in error for error in errors)
    assert any("continuity_anchor" in error and "每个信息状态" in error for error in errors)


def test_v24_density_is_semantic_and_readability_judgment_not_item_count(tmp_path: Path):
    lesson = _v24_semantic_page_lesson(tmp_path)
    lesson["pages"][0]["slide_design"]["density_judgment"]["readability_focus"] = "七条以内"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("density_judgment.readability_focus" in error for error in errors)


def test_v23_reading_experience_can_use_ep13_without_instant_revision(tmp_path: Path):
    lesson = _v23_direct_instruction_lesson(tmp_path)
    page = lesson["pages"][0]
    page["activity_contract"]["event_type"] = "EV03"
    page["activity_contract"]["primary_type"] = "AC01"
    page["activity_contract"]["teacher_move_types"] = ["TM05"]
    page["activity_contract"]["artifact_type"] = "EP13"
    page["activity_contract"]["selection_reason"] = "这一处先需要完整听见声音和节奏，立即改写或答题会切断文学感受。"
    page["activity_contract"]["knowledge_fit"] = "示范朗读把‘蚩蚩’与抱布而来的动作放进同一声音过程，服务开篇整体感知。"
    page["activity_contract"]["experience_fit"] = "学生先完整倾听并停留片刻，随后在下一事件中用原词说出自己真正听见的变化。"
    page["script"]["teacher_spoken"] = "请先不写答案，只听这一句怎样把人物送到我们面前：氓之蚩蚩，抱布贸丝。"
    page["script"]["script_segments"][0]["kind"] = "reading"
    page["script"]["script_segments"][0]["text"] = page["script"]["teacher_spoken"]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert errors == []


def test_v23_guided_oral_response_can_reveal_feedback_after_student_response(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["schema_version"] = "2.3"
    page = lesson["pages"][0]
    page.pop("artifact")
    page.pop("visible_revision")
    page["activity_contract"]["event_type"] = "EV04"
    page["activity_contract"].pop("artifact_type")
    page["activity_contract"]["primary_type"] = "AC03"
    page["activity_contract"]["selection_reason"] = (
        "学生只需当场指出开篇动作并说清先后，短口答足以暴露这一处局部理解。"
    )
    page["activity_contract"]["knowledge_fit"] = (
        "教师依据口答追问原词，使动作顺序得到校准，不把局部回应扩成书面作品。"
    )
    page["activity_contract"]["experience_fit"] = (
        "学生先看原句、短暂思考并口头回应，随后立即听见针对现场回答的准确反馈。"
    )
    page["student_action"] = ["学生静默看原句后，用一句口答指出动作先后。"]
    page["first_view_contract"] = (
        "B0只呈现‘氓之蚩蚩，抱布贸丝’和‘按顺序说出人物动作’，不出现教师反馈语。"
    )
    page["information_state"] = (
        "B0（page_enter）可见：氓之蚩蚩，抱布贸丝｜按顺序说出人物动作；"
        "B1（after_student_response）新增可见：动作先后必须回到原词。"
    )
    page["slide_design"]["frontstage_elements"][1]["text"] = "按顺序说出人物动作"
    page["slide_design"]["frontstage_elements"][2]["role"] = "feedback"
    page["slide_design"]["information_states"][1]["enter_trigger"] = (
        "after_student_response"
    )
    page["script"].pop("observable_evidence", None)
    page["script"]["observable_evidence"] = (
        "能够听见学生用一句话指出抱布、贸丝的先后，并能回指相应原词。"
    )
    page["script"]["student_process"] = (
        "学生先静默看原句，再用一句口答指出动作先后；教师听取后作有界反馈。"
    )
    page["script"]["teacher_spoken"] = "请先沿动作顺序说清眼前发生了什么。"
    page["script"]["timeboxes"] = [
        {"label": "发布口答任务", "seconds": 30, "segment_ids": ["S01"]},
        {"label": "静默思考", "seconds": 90, "segment_ids": ["S02"]},
        {"label": "听取回应并反馈", "seconds": 150, "segment_ids": ["S03"]},
        {"label": "转入下一句", "seconds": 30, "segment_ids": ["S04"]},
    ]
    page["script"]["script_segments"] = [
        {
            "id": "S01",
            "state_id": "B0",
            "kind": "task",
            "enter_trigger": "after_instruction",
            "text": "请先沿动作顺序说清眼前发生了什么。",
        },
        {
            "id": "S02",
            "state_id": "B0",
            "kind": "wait",
            "enter_trigger": "after_instruction",
            "text": "教师停止说话，等待学生看原句并形成一句口答。",
        },
        {
            "id": "S03",
            "state_id": "B1",
            "kind": "feedback",
            "enter_trigger": "after_student_response",
            "text": "先把动作说全，再看你的顺序是否能逐字回到原句。",
        },
        {
            "id": "S04",
            "state_id": "B1",
            "kind": "cut",
            "enter_trigger": "after_student_response",
            "text": "动作已经说清，继续看这次相遇怎样向后推进。",
        },
    ]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert errors == []


def test_v23_generation_event_still_requires_task_followed_by_wait(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["schema_version"] = "2.3"
    page = lesson["pages"][0]
    page["activity_contract"]["event_type"] = "EV05"
    page["script"]["script_segments"] = [
        segment
        for segment in page["script"]["script_segments"]
        if segment["kind"] != "wait"
    ]
    for index, segment in enumerate(page["script"]["script_segments"], 1):
        segment["id"] = f"S{index:02d}"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("task片段后必须紧接真实wait" in error for error in errors)


def test_v23_rejects_unregistered_event_type(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["schema_version"] = "2.3"
    lesson["pages"][0]["activity_contract"]["event_type"] = "EV99"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("event_type未注册" in error for error in errors)


def test_v23_non_generation_timeboxes_still_cover_every_real_segment(tmp_path: Path):
    lesson = _v23_direct_instruction_lesson(tmp_path)
    lesson["pages"][0]["script"]["timeboxes"] = [
        {"label": "沿原词准确讲授", "seconds": 300, "segment_ids": ["S01"]}
    ]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("timeboxes必须按顺序完整分配script_segments" in error for error in errors)


def test_text_source_inline_mineru_sup_note_does_not_pollute_canonical_line(tmp_path: Path):
    lesson = _lesson(tmp_path)
    source = tmp_path / lesson["text_contract"]["source_path"]
    source.write_text("氓之蚩 <sup>a</sup> 蚩，抱布贸丝", encoding="utf-8")
    lesson["text_contract"]["source_sha256"] = _sha(source)
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert not any("canonical_lines未出现在绑定文本源" in error for error in errors)


def test_v21_strict_rejects_missing_g1_binding(tmp_path: Path):
    lesson = _lesson(tmp_path)
    del lesson["lesson_plan_binding"]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("lesson_plan_binding" in error for error in errors)


def test_plan_file_change_invalidates_lesson_design(tmp_path: Path):
    lesson = _lesson(tmp_path)
    plan_path = tmp_path / "work/teaching/lesson/教案.md"
    plan_path.write_text(plan_path.read_text(encoding="utf-8") + "上游已修改。", encoding="utf-8")
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("G1上游无效" in error or "教案哈希" in error for error in errors)


def test_objective_and_question_cannot_drift_from_g1(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["objectives"][0]["statement"] = "这是教学设计阶段偷偷改写后的目标，长度足够但不属于获批教案。"
    lesson["three_questions"] = ["教学设计另造的问题是什么？"]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("目标陈述漂移" in error for error in errors)
    assert any("贯穿问题漂移" in error for error in errors)


def test_page_stage_must_exist_in_approved_plan(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["stage_id"] = "P99"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("stage_id未获G1批准" in error for error in errors)


def test_total_minutes_and_closing_mode_cannot_drift(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["lesson_plan_scope"]["total_minutes"] = 45
    lesson["lesson_plan_scope"]["closing_mode"] = "改成教师直接总结。"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("total_minutes" in error for error in errors)
    assert any("closing_mode" in error for error in errors)


def test_page_must_bind_and_cover_approved_objectives_and_kids(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["objective_ids"] = []
    lesson["pages"][0]["lesson_kids"] = []
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("未被任何页面落实" in error and "O1" in error for error in errors)
    assert any("未被任何页面落实" in error and "K01" in error for error in errors)


def test_strict_v2_requires_all_eighteen_page_contract_fields(tmp_path: Path):
    lesson = _lesson(tmp_path)
    missing_fields = (
        "previous_page_input",
        "first_view_contract",
        "real_wait",
        "bounded_feedback",
        "visible_revision",
        "visual_role",
        "continuous_increment",
        "attention_budget",
    )
    for field in missing_fields:
        candidate = json.loads(json.dumps(lesson, ensure_ascii=False))
        del candidate["pages"][0][field]
        errors, _, _ = validate(candidate, strict=True, root=tmp_path)
        assert any(field in error for error in errors), (field, errors)


def test_strict_v2_requires_explicit_timeboxes(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["script"]["timeboxes"] = []
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("timeboxes为空" in error for error in errors)


def test_v2_g1_binding_must_be_project_relative(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["lesson_plan_binding"]["path"] = str(
        (tmp_path / lesson["lesson_plan_binding"]["path"]).resolve()
    )
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("lesson_plan_binding.path必须使用项目根相对路径" in error for error in errors)


def test_v2_contract_rejects_wrong_field_types(tmp_path: Path):
    lesson = _lesson(tmp_path)
    page = lesson["pages"][0]
    page["minutes"] = "5"
    page["student_action"] = "圈画"
    page["objective_ids"] = "O1"
    page["script"] = []
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("minutes必须为正数" in error for error in errors)
    assert any("student_action必须为非空字符串列表" in error for error in errors)
    assert any("objective_ids必须为非空字符串列表" in error for error in errors)
    assert any("script必须为对象" in error for error in errors)


def test_v2_script_branches_require_distinct_kind_and_nonempty_response(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["script"]["branches"] = [
        {"kind": "沉默", "response": ""},
        {"kind": "沉默", "response": "再等待"},
    ]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("branch[0].response为空" in error for error in errors)
    assert any("分支kind重复" in error for error in errors)


def test_v2_contract_rejects_placeholder_content(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["continuous_increment"] = "TODO"
    errors, _, stats = validate(lesson, strict=True, root=tmp_path)
    assert stats["boilerplate"] >= 1
    assert any("样板自证" in error for error in errors)


def test_v2_claim_boundary_cannot_assert_classroom_success(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["claim_boundary"] = "课堂效果仍待真实试教记录；但学生已经全部学懂并享受，试教已经完成。"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("待真实课堂/试教验证" in error for error in errors)


def test_strict_rejects_schema_older_than_v22(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["schema_version"] = "2.0"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("schema_version必须为2.2、2.3、2.4、2.5或2.6" in error for error in errors)


def test_v20_remains_readable_only_outside_strict(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["schema_version"] = "2.0"
    page = lesson["pages"][0]
    for field in ("knowledge_payload", "activity_contract", "student_experience", "slide_design"):
        page.pop(field)
    for field in (
        "transition_spoken", "student_process", "expected_responses",
        "feedback_spoken", "observable_evidence", "cut_spoken", "script_segments",
    ):
        page["script"].pop(field)
    for box in page["script"]["timeboxes"]:
        box.pop("segment_ids", None)
    errors, _, _ = validate(lesson, strict=False, root=tmp_path)
    assert errors == []


def test_v21_rejects_unregistered_category_ids(tmp_path: Path):
    lesson = _lesson(tmp_path)
    contract = lesson["pages"][0]["activity_contract"]
    contract["primary_type"] = "AC99"
    contract["teacher_move_types"] = ["TM99"]
    contract["learner_action_types"] = ["LA99"]
    contract["participation_type"] = "PS99"
    contract["artifact_type"] = "EP99"
    contract["sensory_channel_types"] = ["SC99"]
    contract["feedback_types"] = ["FB99"]
    lesson["pages"][0]["slide_design"]["layout_type"] = "LT99"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    for unknown in ("AC99", "TM99", "LA99", "PS99", "EP99", "SC99", "FB99", "LT99"):
        assert any(unknown in error for error in errors), (unknown, errors)


def test_v21_rejects_duplicate_primary_secondary_activity(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["activity_contract"]["secondary_types"] = ["AC05"]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("主辅活动类别重复" in error for error in errors)


def test_v21_knowledge_payload_must_exactly_cover_page_kids(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["knowledge_payload"][0]["kid"] = "K99"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("knowledge_payload与lesson_kids不一致" in error for error in errors)


def test_v21_rejects_unknown_page_role(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["knowledge_payload"][0]["page_role"] = "decorate"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("page_role未注册" in error for error in errors)


def test_v21_requires_complete_student_experience(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["student_experience"]["possible_feeling"] = "开心"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("student_experience.possible_feeling最低有效内容不足" in error for error in errors)


def test_v21_rejects_empty_aesthetic_layout_rationale(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["slide_design"]["layout_rationale"] = "为了美观、清晰、大气。"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("版式理由必须说明教学作用" in error for error in errors)


def test_v22_requires_element_level_information_states(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["slide_design"].pop("information_states")
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("information_states" in error for error in errors)


def test_v22_rejects_calibration_elements_visible_in_b0(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["slide_design"]["information_states"][0]["visible_element_ids"].append("E03")
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("calibration元素不得在B0可见" in error for error in errors)


def test_v22_rejects_answer_segments_before_artifact_commit(tmp_path: Path):
    lesson = _lesson(tmp_path)
    segment = lesson["pages"][0]["script"]["script_segments"][3]
    segment["kind"] = "calibration"
    segment["state_id"] = "B0"
    segment["enter_trigger"] = "after_instruction"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("calibration片段不得早于首份产物提交" in error for error in errors)


def test_v22_requires_calibration_segment_when_calibration_element_exists(tmp_path: Path):
    lesson = _lesson(tmp_path)
    segments = lesson["pages"][0]["script"]["script_segments"]
    lesson["pages"][0]["script"]["script_segments"] = [
        segment for segment in segments if segment["kind"] != "calibration"
    ]
    for index, segment in enumerate(lesson["pages"][0]["script"]["script_segments"], 1):
        segment["id"] = f"S{index:02d}"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("存在calibration元素但缺校准台词片段" in error for error in errors)


def test_v22_script_segments_must_preserve_spoken_order_and_content(tmp_path: Path):
    lesson = _lesson(tmp_path)
    segments = lesson["pages"][0]["script"]["script_segments"]
    segments[1]["text"] += segments[3]["text"]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("task/calibration片段未按原顺序完整投影teacher_spoken" in error for error in errors)


def test_v22_calibration_segment_must_follow_wait_segment(tmp_path: Path):
    lesson = _lesson(tmp_path)
    segments = lesson["pages"][0]["script"]["script_segments"]
    segments[2], segments[3] = segments[3], segments[2]
    for index, segment in enumerate(segments, 1):
        segment["id"] = f"S{index:02d}"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("calibration片段必须位于wait之后" in error for error in errors)


def test_v22_calibration_segment_must_enter_the_same_state_as_its_trigger(tmp_path: Path):
    lesson = _lesson(tmp_path)
    calibration = next(
        segment
        for segment in lesson["pages"][0]["script"]["script_segments"]
        if segment["kind"] == "calibration"
    )
    calibration["state_id"] = "B0"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("calibration片段与信息状态触发不一致" in error for error in errors)


def test_v22_segment_cannot_run_before_its_bound_state_exists(tmp_path: Path):
    lesson = _lesson(tmp_path)
    feedback = next(
        segment
        for segment in lesson["pages"][0]["script"]["script_segments"]
        if segment["kind"] == "feedback"
    )
    feedback["enter_trigger"] = "after_instruction"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("片段早于所绑定状态" in error for error in errors)


def test_v22_rejects_legacy_generated_activity_reason(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["activity_contract"]["selection_reason"] = (
        "本页真正的断点是学生没有圈出动作，所以以证据推理为主机制，并以证据链留下可观察结果。"
    )
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("selection_reason仍是统一生成模板" in error for error in errors)


def test_v22_rejects_generated_fit_rationales(tmp_path: Path):
    lesson = _lesson(tmp_path)
    contract = lesson["pages"][0]["activity_contract"]
    contract["knowledge_fit"] = "处理开篇动作关系；页面只通过‘圈出动词’处理这些内容。"
    contract["experience_fit"] = (
        "学生先感到‘有一点疑问’，再围绕‘动作有什么关系’完成‘圈出动词’；"
        "体验不靠统一表态制造。"
    )
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("knowledge_fit仍是统一生成模板" in error for error in errors)
    assert any("experience_fit仍是统一生成模板" in error for error in errors)


def test_v22_every_revealed_state_requires_a_matching_script_event(tmp_path: Path):
    lesson = _lesson(tmp_path)
    segments = lesson["pages"][0]["script"]["script_segments"]
    for segment in segments:
        if segment["state_id"] == "B1":
            segment["state_id"] = "B0"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("信息状态没有同触发剧本事件" in error for error in errors)


def test_v22_each_task_requires_its_own_following_wait(tmp_path: Path):
    lesson = _lesson(tmp_path)
    page = lesson["pages"][0]
    page["script"]["script_segments"].insert(
        3,
        {
            "id": "S04",
            "state_id": "B0",
            "kind": "task",
            "enter_trigger": "after_primary_artifact_committed",
            "text": "现在再比较两份首答并选择一处修订。",
        },
    )
    for index, segment in enumerate(page["script"]["script_segments"], 1):
        segment["id"] = f"S{index:02d}"
    page["script"]["teacher_spoken"] = (
        "请先沿动作顺序说清眼前发生了什么。"
        "现在再比较两份首答并选择一处修订。"
        "动作先后必须回到原词，不以人物标签代替现场证据。"
    )
    page["script"]["timeboxes"] = [
        {
            "label": f"事件{index}",
            "seconds": seconds,
            "segment_ids": [segment["id"]],
        }
        for index, (segment, seconds) in enumerate(
            zip(page["script"]["script_segments"], [20, 25, 120, 30, 35, 45, 25]),
            1,
        )
    ]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("task片段后必须紧接真实wait" in error for error in errors)


def test_v22_timeboxes_must_partition_script_segments_in_order(tmp_path: Path):
    lesson = _lesson(tmp_path)
    boxes = lesson["pages"][0]["script"]["timeboxes"]
    boxes[1]["segment_ids"] = ["S03"]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("timeboxes必须按顺序完整分配script_segments" in error for error in errors)


def test_v22_legacy_information_state_is_canonical_projection(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["information_state"] = "首屏已经出现教师校准答案。"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("information_state与结构化信息状态不一致" in error for error in errors)


def test_v21_requires_complete_real_script(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["script"].pop("cut_spoken")
    lesson["pages"][0]["script"]["expected_responses"] = []
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("script缺cut_spoken" in error for error in errors)
    assert any("expected_responses必须为非空字符串列表" in error for error in errors)


def test_v21_rejects_unknown_nested_design_fields(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["activity_contract"]["discussion_magic"] = True
    lesson["pages"][0]["slide_design"]["decorative_mood"] = "宏大"
    lesson["pages"][0]["script"]["secret_effect_claim"] = "学生已经学会"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("activity_contract含未知字段" in error for error in errors)
    assert any("slide_design含未知字段" in error for error in errors)
    assert any("script含未知字段" in error for error in errors)


def test_duplicate_page_ids_are_rejected(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"].append(json.loads(json.dumps(lesson["pages"][0], ensure_ascii=False)))
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("page_id重复" in error for error in errors)


def test_v2_previous_page_input_cannot_reuse_legacy_default_pattern(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["previous_page_input"] = "学生已经完成前页任务，手中保留与“氓之蚩蚩”有关的原词或初稿。"
    errors, _, stats = validate(lesson, strict=True, root=tmp_path)
    assert stats["boilerplate"] >= 1
    assert any("样板自证" in error for error in errors)


def test_v2_contract_rejects_single_character_fillers(tmp_path: Path):
    lesson = _lesson(tmp_path)
    page = lesson["pages"][0]
    for field in (
        "previous_page_input", "unique_difficulty", "unique_function",
        "first_view_contract", "information_state", "artifact", "real_wait",
        "bounded_feedback", "visible_revision", "next_use",
        "normal_counterexample", "visual_role", "first_person_reception",
        "deletion_loss", "continuous_increment", "attention_budget", "story_return",
    ):
        page[field] = "x"
    page["student_action"] = ["x"]
    page["script"]["teacher_spoken"] = "x"
    page["script"]["branches"] = [
        {"kind": "x", "response": "x"},
        {"kind": "y", "response": "y"},
    ]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("最低有效内容" in error for error in errors)


def test_v2_canonical_lines_must_exist_in_bound_source(tmp_path: Path):
    lesson = _lesson(tmp_path)
    source_path = tmp_path / lesson["text_contract"]["source_path"]
    source_path.write_text("此文件完全没有所声明的教材原文。", encoding="utf-8")
    lesson["text_contract"]["source_sha256"] = _sha(source_path)
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("canonical_lines未出现在绑定文本源" in error for error in errors)


def test_v2_kp_scope_and_objectives_cannot_change_g1_kid_mapping(tmp_path: Path):
    lesson = _lesson(tmp_path)
    card_path = tmp_path / "work/knowledge/测试册/cards/CARD-TEST-01.md"
    card_path.write_text("KP-CARD-TEST-01-001\nKP-CARD-TEST-01-002", encoding="utf-8")
    lesson["kp_scope"]["kp_ids"] = ["KP-CARD-TEST-01-002"]
    lesson["objectives"][0]["kp_refs"] = ["KP-CARD-TEST-01-002"]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("G1批准的KID→KP映射漂移" in error for error in errors)


def test_v2_requires_structured_forward_use(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0].pop("next_use_ref", None)
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("next_use_ref" in error for error in errors)


def test_v2_rejects_unknown_top_level_classroom_claim_field(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["classroom_account"] = {
        "status": "verified",
        "mastery": "学生已经全部掌握并享受课堂。",
    }
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("v2含未知顶层字段: classroom_account" in error for error in errors)


def test_v2_uses_supplied_root_for_enforcement_config(tmp_path: Path):
    lesson = _lesson(tmp_path)
    config_path = tmp_path / "work/principles/enforcement_config.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps({
        "frontstage_banned_v5": ["沿着原文"],
        "first_view_banned_v5": ["占位"],
        "note_banned_v5": ["占位"],
        "frontstage_banned_v6": ["占位"],
    }, ensure_ascii=False), encoding="utf-8")
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("前台含后台词「沿着原文」" in error for error in errors)


def test_v2_rejects_empty_canonical_line_even_for_non_poem_page(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["text_contract"]["canonical_lines"] = [""]
    lesson["pages"][0]["literary_object"] = {"kind": "student_products"}
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("canonical_lines必须" in error for error in errors)


def test_v2_assessment_forward_use_must_target_an_approved_objective(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["next_use_ref"] = {
        "kind": "assessment",
        "target_id": "DOES-NOT-EXIST",
        "use": "把本页产物交给后续测评继续检索使用。",
    }
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("assessment目标未获G1批准" in error for error in errors)


def test_v2_rejects_nested_classroom_account_and_unknown_page_fields(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["metadata"] = {"classroom_account": {"status": "全体学生已经掌握"}}
    lesson["pages"][0]["host_release_status"] = "released"
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("metadata" in error for error in errors)
    assert any("页面含未知字段: host_release_status" in error for error in errors)


def test_v2_rejects_six_character_contract_fillers(tmp_path: Path):
    lesson = _lesson(tmp_path)
    page = lesson["pages"][0]
    for field in (
        "previous_page_input", "unique_difficulty", "unique_function",
        "first_view_contract", "information_state", "artifact", "real_wait",
        "bounded_feedback", "visible_revision", "next_use",
        "normal_counterexample", "visual_role", "first_person_reception",
        "deletion_loss", "continuous_increment", "attention_budget", "story_return",
    ):
        page[field] = "甲乙丙丁戊己"
    page["student_action"] = ["甲乙丙丁戊己"]
    errors, _, _ = validate(lesson, strict=True, root=tmp_path)
    assert any("最低有效内容不足" in error for error in errors)


def test_v2_page_responsibilities_must_match_its_approved_stage(tmp_path: Path):
    lesson = _lesson(tmp_path)
    g1_path = tmp_path / lesson["lesson_plan_binding"]["path"]
    g1 = json.loads(g1_path.read_text(encoding="utf-8"))
    g1["contract"]["stages"].append({
        "id": "P1",
        "name": "教师储备背景",
        "objective_refs": ["O1"],
        "kid_refs": ["K02"],
        "student_change": "辨认哪些背景不进入本课主线。",
        "teacher_role": "控制背景负荷并说明延后理由。",
        "evidence": "学生仍能回到原文证据。",
        "transition_reason": "只有主线稳定后才讨论延后内容。",
    })
    receipt_path = tmp_path / g1["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["lesson_plan_contract_sha256"] = canonical_json_sha256(g1["contract"])
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    g1["owner_approval"]["sha256"] = _sha(receipt_path)
    g1_path.write_text(json.dumps(g1, ensure_ascii=False, indent=2), encoding="utf-8")
    lesson["lesson_plan_binding"]["sha256"] = _sha(g1_path)
    lesson["lesson_plan_scope"]["contract_sha256"] = canonical_json_sha256(g1["contract"])
    lesson["lesson_plan_scope"]["stage_ids"] = ["P0", "P1"]
    lesson["pages"][0]["stage_id"] = "P1"

    errors, _, _ = validate(lesson, strict=True, root=tmp_path)

    assert any("lesson_kid不属于获批阶段P1" in error for error in errors)


def test_v2_must_include_every_g1_approved_stage(tmp_path: Path):
    lesson = _lesson(tmp_path)
    g1_path = tmp_path / lesson["lesson_plan_binding"]["path"]
    g1 = json.loads(g1_path.read_text(encoding="utf-8"))
    g1["contract"]["stages"].append({
        "id": "P1",
        "name": "再次整体化",
        "objective_refs": ["O1"],
        "kid_refs": ["K01"],
        "student_change": "把局部证据重新组织为完整解释。",
        "teacher_role": "只校准证据边界并组织回取。",
        "evidence": "学生形成带原词的完整末答。",
        "transition_reason": "本阶段完成后才可进入收束。",
    })
    receipt_path = tmp_path / g1["owner_approval"]["path"]
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    receipt["lesson_plan_contract_sha256"] = canonical_json_sha256(g1["contract"])
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    g1["owner_approval"]["sha256"] = _sha(receipt_path)
    g1_path.write_text(json.dumps(g1, ensure_ascii=False, indent=2), encoding="utf-8")
    lesson["lesson_plan_binding"]["sha256"] = _sha(g1_path)
    lesson["lesson_plan_scope"]["contract_sha256"] = canonical_json_sha256(g1["contract"])
    lesson["lesson_plan_scope"]["stage_ids"] = ["P0", "P1"]

    errors, _, _ = validate(lesson, strict=True, root=tmp_path)

    assert any("G1阶段未被任何页面落实: P1" in error for error in errors)


def test_assessment_next_use_requires_a_registered_real_consumer(tmp_path: Path):
    lesson = _lesson(tmp_path)
    lesson["pages"][0]["next_use_ref"] = {
        "kind": "assessment",
        "target_id": "O1",
        "use": "后续测评将按同一目标读取这份学生复述。",
    }

    errors, _, _ = validate(lesson, strict=True, root=tmp_path)

    assert any("assessment消费者" in error for error in errors)
