---
schema_version: "exam-reference-answer-candidate-comparison-0.1"
status: "candidate_only_cross_source_comparison"
authority_status: "both_sources_unverified"
coverage: "GK-SC-2013 Q1-Q21; external Q1-Q20; local Q1-Q21"
scoring_status: "not_available_as_official"
mapping_status: "M0 | kp_id=N/A"
---

# 2013 四川卷答案候选交叉比对

> 本报告只比较两个未核验候选层：带水印的新浪图像转录与本地解析卷候选。文本一致不等于官方核验；本层不修改主 `answer_index.jsonl`，不生成评分标准，也不升级教材知识点映射。

- 本地候选：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/local_analysis_candidates.jsonl`，Q1—Q21；新浪候选：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/reference_answer_candidates.jsonl`，Q1—Q20。
- 主答案索引 SHA-256：`489ba22579be29b0426db2ece4732bc83bc850a903ca8d513c192a510a74289a`（固定门禁，21 条仍为 missing）。
- 比对 JSONL：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-SC-2013/answers/reference_answer_candidate_comparison.jsonl`；共 21 条。
- 判定计数：`textually_consistent_unverified`=7, `format_equivalent_unverified`=4, `local_mixed_analysis_no_explicit_answer`=4, `ocr_or_format_difference_requires_review`=1, `text_difference_requires_review`=2, `format_or_label_difference_requires_review`=1, `coverage_difference_requires_review`=1, `both_sources_missing`=1。

## 逐题比对

| 题号 | 本地候选 | 新浪候选 | 比对证据 | 判定 |
|---:|---|---|---|---|
| 1 | B | B | `exact` | `textually_consistent_unverified` |
| 2 | A. | A | `compact` | `format_equivalent_unverified` |
| 3 | — | B | `—` | `local_mixed_analysis_no_explicit_answer` |
| 4 | c | C | `option` | `format_equivalent_unverified` |
| 5 | B | B | `exact` | `textually_consistent_unverified` |
| 6 | C | C | `exact` | `textually_consistent_unverified` |
| 7 | D | D | `exact` | `textually_consistent_unverified` |
| 8 | D | D | `exact` | `textually_consistent_unverified` |
| 9 | C. | C | `compact` | `format_equivalent_unverified` |
| 10 | — | （1）平时单独居处，整天严肃庄重；至于和人交往，则热情洋溢、和乐喜悦。（2）凡是引用的书籍，总是加上注解，用来裁断订正它们的意义，也有许多先儒没有阐发的内容。 | `—` | `local_mixed_analysis_no_explicit_answer` |
| 11 | — | 敏而好学，诲人不倦；严谨治学，敢于创新；忧国而献良策；助人而不居功；立志为本，知行合一。 | `—` | `local_mixed_analysis_no_explicit_answer` |
| 12 | 因民之所利而利之/斯不亦惠而不费乎/择可劳而劳之/又谁怨/欲仁而得仁/又焉贪/君子无众寡/无小大/无敢慢/斯不亦泰而不骄乎 | 因民之所利而利之/斯不亦惠而不费乎/择可劳而劳之/又谁怨/欲仁而得仁/又焉贪/君子无众寡/无小大/无敢慢/斯不亦泰而不骄乎 | `exact` | `textually_consistent_unverified` |
| 13 | — | （1）主要表达作者壮志未酬的忧愁和苦闷。华发、愁、寒无睡等写年岁已逝和愁苦；“壮心偶傍醉中来”写壮心未泯而又不得施展。（2）“佳节”与“愁”对比，“久”与“偶”对比，“愁”与“壮心”对比，三层对比强化了忧愁之深和潜藏于胸的壮心未绝。 | `—` | `local_mixed_analysis_no_explicit_answer` |
| 14 | (1)载笑载言(2)百步九折萦岩峦(3)浑欲不胜簪(4)轻拢慢捻抹复挑 (5)能谤讥于市朝 (6)疲敝之 卒(7)皆若空游无所依(8)浩浩乎如凭虚御风 | （1）载笑载言（2）百步九折萦岩峦（3）浑欲不胜簪（4）轻拢慢捻抹复挑（5）能谤讥于市朝（6）疲敝之卒（7）皆若空游无所依（8）浩浩乎如凭虚御风 | `compact` | `format_equivalent_unverified` |
| 15 | C、E | C、E | `exact` | `textually_consistent_unverified` |
| 16 | ①生动地刻画出胡杨林坚韧顽强的形象，增强文章的感染力；②深化主题，以胡杨树的生死暗示河流的变化，表现生命离开河流后的困顿；③由，河到树，由树到人，承上启下，结构更加严密。 | ①生动地刻画出胡杨林坚韧顽强的形象，增强文章的感染力；②深化主题，以胡杨树的生死暗示河流的变化，表现生命离开河流后的困顿；③由河到树，由树到人，承上启下，结构更加严密。 | `compact` | `ocr_or_format_difference_requires_review` |
| 17 | ①塔里木河身处沙漠，不得不与沙漠进行长期的坚韧的较量；②塔里木河给沙漠带来生命与文明，却不得不亲历文明的衰落；③塔里木河的奔腾与消失承载着人们的热爱、慌恐等复杂情感，引发了沉重的思考。 | ①塔里木河身处沙漠，不得不与沙漠进行长期的坚韧较量；②塔里木河给沙漠带来生命与文明，却不得不亲历文明的衰落；③塔里木河的奔腾和消失承载着人们的热爱、惶恐等复杂情感，引发沉重思考。 | `—` | `text_difference_requires_review` |
| 18 | 示例一 河流是人类文化的源头。塔里木河曾赋予罗布泊人浪漫的生活气息，长江、黄河乃至家乡的每一条河，都滋养了中华民族源远流长的文化。如今地球上的很多河流正像塔里木河一样在萎缩，人类社会的发展不应以破坏自然为代价，否则将会给人类及其文化带来不可 | 示例一：河流是人类文化的源头。塔里木河曾赋予罗布泊人浪漫的生活气息，长江、黄河乃至家乡的每一条河都滋养了中华民族源远流长的文化。如今许多河流正在萎缩，人类社会的发展不应以破坏自然为代价。 示例二：河流具有超越自然生命的文化魅力。塔里木河的率 | `—` | `text_difference_requires_review` |
| 19 | 示例 ①在和陌生人的交往中您印象最深的事是什么 ②从这些事例中您总结出了哪些与陌生人交往的技巧 ③为帮助我们更好地与陌生人交往，您还有哪些建议 | ①在和陌生人的交往中，您印象最深的事是什么？②从这些事例中，您总结出了哪些与陌生人交往的技巧？③为帮助我们更好地与陌生人交往，您还有哪些建议？ | `—` | `format_or_label_difference_requires_review` |
| 20 | 示例一 曹雪芹家道巨变，却磨砺出傲岸的风骨；备受冷遇，却迸发出创作的激情；绳床瓦灶，却熔铸成生命的华章。“十年辛苦不寻常”终换成彪炳千秋的文学巨著，这难道不是苦难带给他的人生意义吗？ 示例二 贝多芬童年不幸，却不曾破灭人生的梦想：恋人远离， | 示例一：曹雪芹家道巨变，却磨砺出傲岸的风骨；备受冷遇，却迸发出创作的激情；绳床瓦灶，却熔铸成生命的华章。“十年辛苦不寻常”终换成彪炳千秋的文学巨著，这难道不是苦难带给他的人生意义吗？ 示例二：贝多芬童年不幸，却不曾破灭人生的梦想；恋人远离， | `—` | `coverage_difference_requires_review` |
| 21 | — | — | `—` | `both_sources_missing` |

## 使用边界

1. Q3、Q10、Q11、Q13 的本地字段是混合解析文本，未从解析内容反推答案。
2. Q16—Q20 的差异保留为待复核事项；OCR、示例标签、答案长度差异均未静默修复。
3. Q21 两层均没有独立答案；作文示例或写作指导不得替代评分标准。
4. 所有记录保持 `scoring_status=not_available_as_official`、`mapping_level=M0`、`kp_id=N/A`。
