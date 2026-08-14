---
schema_version: "exam-reference-answer-candidate-comparison-0.1"
status: "candidate_only_cross_source_comparison"
authority_status: "both_sources_unverified"
coverage: "GK-NCA-2023 Q1-Q22; external Q1-Q3,Q6-Q10"
scoring_status: "not_available_as_official"
mapping_status: "M0 | kp_id=N/A"
---

# 2023 全国甲卷答案候选交叉比对

> 本报告比较本地解析共享答案块切分层与中国教育在线第三方答案快照。外部来源只覆盖 Q1—Q3、Q6—Q10；其余题号不使用搜索摘要或解析推断补齐。文本一致不等于官方核验。

- 本地切分候选：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/local_analysis_group_candidates.jsonl`，Q1—Q22。
- 外部候选：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/reference_answer_candidates.jsonl`，Q1—Q3、Q6—Q10。
- 比对 JSONL：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2023/answers/reference_answer_candidate_comparison.jsonl`；共 22 条。
- 判定计数：`textually_consistent_unverified`=7, `external_source_missing_local_candidate_only`=9, `local_mixed_analysis_no_explicit_answer`=1, `external_missing_local_mixed_analysis`=4, `writing_artifact_no_external`=1。

## 逐题比对

| 题号 | 本地候选 | 外部候选 | 证据 | 判定 |
|---:|---|---|---|---|
| 1 | C | C | `exact` | `textually_consistent_unverified` |
| 2 | C | C | `exact` | `textually_consistent_unverified` |
| 3 | B | B | `exact` | `textually_consistent_unverified` |
| 4 | B | — | `—` | `external_source_missing_local_candidate_only` |
| 5 | C | — | `—` | `external_source_missing_local_candidate_only` |
| 6 | ①在育种繁殖的过程中应采取措施恢复人工栽培植物在地面或地下的沟通能力，从而提高抵抗病虫害的能力，减少农药的使用量。 ②育种专家可借鉴自然野生植物的野性基因，如把利用气味传递信息等属性加入人工栽培植物的属性中去。 | ①在育种繁殖的过程中应采取措施恢复人工栽培植物在地面或地下的沟通能力，从而提高抵抗病虫害的能力，减少农药的使用量。 ②育种专家可借鉴自然野生植物的野性基因，如把利用气味传递信息等属性加入人工栽培植物的属性中去。 | `compact` | `textually_consistent_unverified` |
| 7 | C | C | `exact` | `textually_consistent_unverified` |
| 8 | （1）工人是机械的操控者、管理者、指挥者，是机器背后的灵魂。（2）机器的创造，本质上还是人的创造，在人的控制下，机械的力量才是完美的。（3）对机械力量的赞美，实则是对人能力的肯定。 | （1) 工人是机械的操控者、管理者、指挥者，是机器背后的灵魂。(2) 机器的创造，本质上还是人的创造，在人的控制下，机械的力量才是完美的。(3)对机械力量的赞美，实则是对人能力的肯定。 | `compact` | `textually_consistent_unverified` |
| 9 | （1）这是联想，由轮船上的机器联想到上海的建筑所用的机器，二者都体现机器的力量，具有相似性。 （2）拓展文章的广度，丰富其内容。（3）由“我”一个人的喜悦，拓展到“许多人”的喜悦，表明对机器力量的欣赏是普遍存在的，深化了文章的主题。 | （1）这是联想，由轮船上的机器联想到上海的建筑所用的机器，二者都体现机器的力量，具有相似性。 (2)拓展文章的广度，丰富其内容。(3)由“我”一个人的喜悦，拓展到“许多人”的喜悦，表明对机器力量的欣赏是普遍存在的，深化了文章的主题。 | `compact` | `textually_consistent_unverified` |
| 10 | — | BDG | `—` | `local_mixed_analysis_no_explicit_answer` |
| 11 | — | — | `—` | `external_missing_local_mixed_analysis` |
| 12 | — | — | `—` | `external_missing_local_mixed_analysis` |
| 13 | — | — | `—` | `external_missing_local_mixed_analysis` |
| 14 | A | — | `—` | `external_source_missing_local_candidate_only` |
| 15 | ①用动词“垂”“谢”赋予“柳”“梅”动态的美感，运用虚写的手法，想象在春季邀约友人同去东溪岸边，去观赏秀丽的春景。 ②此句以春光美景收束全词，通过想象未来再聚之景，表达了对即将再会的期盼，安慰即将远离的友人，更表达出对友人离别的不舍之情和乐 | — | `—` | `external_source_missing_local_candidate_only` |
| 16 | — | — | `—` | `external_missing_local_mixed_analysis` |
| 17 | C | — | `—` | `external_source_missing_local_candidate_only` |
| 18 | 语句：④；修改为：古人不能跟我们相提并论。 | — | `—` | `external_source_missing_local_candidate_only` |
| 19 | 示例一：柳宗元《江雪》里有“孤舟寰笠翁”的句子 示例二：寓言里有“刻舟求剑”的故事 示例三：“刻舟求剑”的成语 | — | `—` | `external_source_missing_local_candidate_only` |
| 20 | 第一位教师：①讲清道理，鼓舞学生前进；②但未解释字词。第二位教师：①讲清词义和变化，增长知识；②但未讲整体含义及使用。第三位教师：①知识、道理结合较好，②解说全面，简明扼要。 | — | `—` | `external_source_missing_local_candidate_only` |
| 21 | 答案示例“卧薪尝胆”：①越王立志报仇，夜里睡柴草，饭前尝苦胆，敦促自己不忘报仇雪耻，②后来用以表示刻苦自勉，奋发图强。 “庖丁解牛”：①庖丁为文惠君分割牛，运刀准确自如。②后来用以表示技艺高超，运用得心应手。 “一鼓作气”：①古代击鼓进军， | — | `—` | `external_source_missing_local_candidate_only` |
| 22 | 例文： | — | `—` | `writing_artifact_no_external` |

## 使用边界

1. Q1—Q3、Q4—Q6、Q7—Q9、Q14—Q15、Q17—Q21 的本地共享答案块仅按显式题号切分，源块题号归属和边界哈希均保留。
2. Q10—Q13、Q16 的本地字段无可安全分离答案，未从解析文字反推；Q22 的‘例文’不是评分标准。
3. 外部快照缺失题号保持缺失；所有记录保持 `not_available_as_official`、`M0 / kp_id=N/A`。
