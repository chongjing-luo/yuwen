---
document_type: review_abort_record
module_id: MENG_V62_CHAPTER_1
candidate: review_input_v3.json
status: aborted_before_review
---

# 第一章V3送审中止记录

V3清单生成后，测试套件的初始化逻辑再次调用PPTX构建器。PPTX内部包时间戳导致二进制SHA-256变化，清单复核检测到PPTX漂移，尽管页面内容没有观察到改变。

处置：立即中止两路V3复审，不接受任何基于漂移清单的结论。测试套件已改为只读验证，构建、渲染、测试全部完成后才生成V4不可变清单。V4必须连续两次验证全部文件hash和bytes零漂移后方可送审。
