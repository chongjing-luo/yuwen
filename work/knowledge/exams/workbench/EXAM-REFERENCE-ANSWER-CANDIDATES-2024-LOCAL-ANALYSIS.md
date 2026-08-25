---
schema_version: "exam-reference-answer-candidate-0.3"
status: "candidate_only_local_analysis"
authority_status: "unverified_local_provided"
coverage: "GK-NCA-2024 Q1-Q22"
scoring_status: "not_available_as_official"
mapping_status: "M0 | kp_id=N/A"
---

# 2024 全国甲卷本地解析答案候选层

> 本层从解析卷 MinerU `full.md` 恢复答案区和解析区的可定位候选，仅供与美篇第三方候选做结构/文本比对。任何候选均未达到官方答案或评分标准门槛；主 `answer_index.jsonl` 仍保持 22 条 `N/A`。

- 本地候选：22 条（Q1—Q22）；与美篇文本一致（未核验）：17 条。
- 需重点复核：4 条（Q8/Q9 圈码 OCR、Q12 选项冲突、Q16 OCR/重复串）；Q22 为写作材料，不参与答案一致性判断。
- 源 MinerU：`Data/2008-2024·（四川）语文高考真题/mineru_result/2024年高考语文试卷（全国甲卷）（解析卷）/full.md`，SHA-256 `e48e7f510bba0a182b1c2de396cf0794396d817e3e066e6b4b779522e46794a8`。
- 源 PDF：`Data/2008-2024·（四川）语文高考真题/2024年高考语文试卷（全国甲卷）（解析卷）.pdf`，SHA-256 `1d253ae46e3b9cca979d5936ec638c6812edd1d2252be8d142914b4fc1f703bd`。
- 派生 JSONL：`Data/2008-2024·（四川）语文高考真题/exam_extract/GK-NCA-2024/answers/reference_answer_candidates_local_analysis.jsonl`。

## 逐题比对

| 题号 | 本地候选摘要 | 美篇候选摘要 | 判定 |
|---:|---|---|---|
| 1 | C | C | `textually_consistent_unverified` |
| 2 | D | D | `textually_consistent_unverified` |
| 3 | B | B | `textually_consistent_unverified` |
| 4 | C | C | `textually_consistent_unverified` |
| 5 | ①. 原柱 ②. 新柱 ③. 假柱 | ①. 原柱 ②. 新柱 ③. 假柱 | `textually_consistent_unverified` |
| 6 | ①新柱如果没有原位替换原柱，可能会改变建筑原结构的受力和传力方式，影响整体的稳定性； ②太和殿是中国最大的木构大殿，建造之初工匠们应该经过了精心的测量，原位替换才是最佳的解决… | ①新柱如果没有原位替换原柱，可能会改变建筑原结构的受力和传力方式，影响整体的稳定性； ②太和殿是中国最大的木构大殿，建造之初工匠们应该经过了精心的测量，原位替换才是最佳的解决… | `textually_consistent_unverified` |
| 7 | D | D | `textually_consistent_unverified` |
| 8 | ①面对生活的困境，有人经不起打击而败退，有人则迎难而上，开始了新生；②虽然前行艰难，但也要凭借坚韧和勇气勇敢踏上征程，寻找属于自己的新生活；(3)此句表达了作者在乌乡霜降夜的… | ①面对生活的困境，有人经不起打击而败退，有人则迎难而上，开始了新生；②虽然前行艰难，但也要凭借坚韧和勇气勇敢踏上征程，寻找属于自己的新生活；③此句表达了作者在乌乡霜降夜的所见… | `ocr_or_format_difference_requires_review` |
| 9 | 1自然景象的描写中渗透着独特的生命感受：文章开头描写了乌乡清晨的霜景，草叶上的霜、萧条的桦树、寒星的隐逝、农家炊烟等细节，写出了霜降节气中自然的变化；通过写作者感受到风中对的… | ①自然景象的描写中渗透着独特的生命感受：文章开头描写了乌乡清晨的霜景，草叶上的霜、萧条的桦树、寒星的隐逝、农家炊烟等细节，写出了霜降节气中自然的变化；通过写作者感受到风中对的… | `ocr_or_format_difference_requires_review` |
| 10 | BDG | BDG | `textually_consistent_unverified` |
| 11 | A | A | `textually_consistent_unverified` |
| 12 | A | C | `conflict_requires_independent_verification` |
| 13 | （1）曹操让臧霸交出那两个人，臧霸说：“我之所以能够自立的原因，是因为不做这样的事情。” （2）我以前听信谗言，与令尊的关系不够深厚，因此辜负了你。 | （1）曹操让臧霸交出那两个人，臧霸说：“我之所以能够自立的原因，是因为不做这样的事情。” （2）我以前听信谗言，与令尊的关系不够深厚，因此辜负了你。 | `textually_consistent_unverified` |
| 14 | C | C | `textually_consistent_unverified` |
| 15 | “软”字形容斜风的温柔轻柔，营造出宁静和谐的氛围；“低”字描绘夕照的柔和低垂，增强了画面的层次感和诗意，使景象更生动。 | “软”字形容斜风的温柔轻柔，营造出宁静和谐的氛围；“低”字描绘夕照的柔和低垂，增强了画面的层次感和诗意，使景象更生动。 | `textually_consistent_unverified` |
| 16 | ①. 海日生残夜 ②. 江春入旧年 ③. 山重水复疑无路 ④. 柳暗花明又一村 ⑤. 飞流直下三千尺 ⑥.疑是银河落九天（飞湍瀑流争喧，o崖转石万壑雷） | ①. 海日生残夜 ②. 江春入旧年 ③. 山重水复疑无路 ④. 柳暗花明又一村 ⑤. 飞流直下三千尺 ⑥. 疑是银河落九天（飞湍瀑流争喧豗，砯崖转石万壑雷） | `ocr_or_format_difference_requires_review` |
| 17 | C | C | `textually_consistent_unverified` |
| 18 | 示例（1）：暖湿气流带着充沛的水汽在伊犁河谷一路长驱直入，它造就了一片片麦浪滚滚的田地，以及水草丰美的牧场。 示例（2)：带着充沛水汽的暖湿气流在伊犁河谷一路长驱直入，它造就… | 示例（1）：暖湿气流带着充沛的水汽在伊犁河谷一路长驱直入，它造就了一片片麦浪滚滚的田地，以及水草丰美的牧场。 示例（2）：带着充沛水汽的暖湿气流在伊犁河谷一路长驱直入，它造就… | `textually_consistent_unverified` |
| 19 | B | B | `textually_consistent_unverified` |
| 20 | 序号②修改为：能浮现出这样一幅包罗万象的全景图； 序号③修改为：图上呈现了天山的所有山脉、雪峰、盆地； 序号④修改为：还有河流、湖泊（还有河流和湖泊）。 | 序号②修改为：能浮现出这样一幅包罗万象的全景图； 序号③修改为：图上呈现了天山的所有山脉、雪峰、盆地； 序号④修改为： 还有河流、湖泊（还有河流和湖泊） 。 | `textually_consistent_unverified` |
| 21 | 大夫好！我是你们医院的老病号，一直在这儿看高血压和糖尿病。昨天晚上吃完饭后开始头疼，先是头顶一圈疼，后来整个头都疼。今天早上醒来仍然头疼，头一动就更疼，所以赶紧来医院了。 | 大夫好！我是你们医院的老病号，一直在这儿看高血压和糖尿病。昨天晚上吃完饭后开始头疼，先是头顶一圈疼，后来整个头都疼。今天早上醒来仍然头疼，头一动就更疼，所以赶紧来医院了。 | `textually_consistent_unverified` |
| 22 | 例文 ## 心迹不掩，英雄本色 现代社会，人际错综，在群体相处的复杂过程中，人们往往为了提高“隐蔽性”、增加安全感而掩藏心迹、力求“大同”，生怕被人看穿自己的“底牌”，拿住自… | 本题考查学生写作的能力。 审题： 这是一道引语式材料作文题。 材料意在引导青少年形成健康正向人际交往理念，关键句“坦诚交流才有可能遇到真正的相遇”直接指明中心论点和写作方向，… | `not_comparable_writing_artifact` |

## 边界和异常

- Q1/Q2：原始答案区只有 Q3 的 `3. B`；Q1=C、Q2=D 仅由对应解析末尾 `故选C/D` 派生，不能写回主答案索引。
- Q4—Q21：按显式 `【答案】`—`【解析】` 区间登记；答案文本与解析文本分开保存并保留源偏移/哈希。
- Q12：本地解析卷给出 A，美篇候选给出 C；这是实质选项冲突，必须独立核验，不能多数表决。
- Q16：有两个 `【答案】` 标记，①—⑥答案串均重复；候选去重保留首份，登记完整重复 payload 与疑似 `o崖` OCR 残片。
- Q22：本地答案区为例文，美篇对应区为作文审题/写作指导；两者均不构成评分标准。

## 使用限制

1. `candidate_unverified` 不等于官方答案；`scoring_status` 固定为 `not_available_as_official`。
2. 未取得独立命题机构/考试机构答案与评分材料前，不从文本一致性推导权威性。
3. 所有题目的教材映射继续保持 `M0 / kp_id=N/A`。
