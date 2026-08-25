---
name: yuwen-build-materials
description: 高中语文PPT与教学物料制作（第三阶段/S4）。只在教学设计通过G2并有有效design lock时，忠实执行已冻结的知识分页、语义关系、显示约束、活动和逐页剧本，并完成具体几何、视觉、美学与多媒体构建；不重新设计讲授逻辑。
---

# PPT与教学物料制作（第三阶段 / S4）

服务机制节点：**K2（知识锚定）、U1（分发时点）、J3（学生作品）、J4（前台语言）**。三阶段唯一操作方法是`work/methodology/lesson-preparation/语文备课操作规程.md`；专项规则引用`work/methodology/manuals/S4-物料手册.md`的`MM-S4-01`—`MM-S4-14`，PPT技术参数再读`work/methodology/lesson-preparation/PPT制作操作手册.md`。本skill只编排构建与门禁，不另造物料制作方法。

创建manifest与物料锁时读取 `../_shared/lesson-lineage-contracts.md` 的G3节。

## 输入

- S3 `教学设计.md`、现行v2.6（或按冻结标准仍有效的v2.2—v2.5）`lesson.json`、`_meta/design_lock.json`

## 步骤

1. 先运行 `python3 scripts/validate_lesson_lineage.py design <design_lock.json>`；失败则退回S3，不得边制作边改设计。
2. 从课程数据同源生成全部物料，不手工分叉修改单一产物（P-11）。必须使用已经存在且通过测试的通用S4构建入口；若项目尚未提供该入口，本阶段如实阻断，不得把课文专项脚本或G3校验器冒充通用构建能力。
3. **忠实执行S3页面与视觉合同**：不得更换知识分页、`presentation_role`、支撑页触发—返回、`semantic_unit`、对象关系、共视/分时、主次层级、连续锚点、`frontstage_elements`、`information_states`、`physical_screens`、视觉来源、配图裁决、揭示顺序或页面状态；逐屏按`script_segment_refs`投影备注，不能让答案性元素或校准台词提前。S4依据真实文字长度把构图蓝图落实为精确坐标，按PG01—PG09实现各自视觉重点；标题、导航与章节（子标题）页保持定位职责，不在制作阶段增加虚构知识卡、目标标签或装饰框。支撑页可与主干页使用不同构图，但字体、课文色板、视觉母题和导航同源。标题先直接说明对象或职责，艺术意味只在不遮蔽意义的副标题、引文和画面中实现。若真实画布证明当前角色、语义分组、构图或配图功能不可读，退回S3重审，不在S4暗拆、暗并、换图或缩字。
4. 学习单按真实分发时点拆件；知识收纳区对应KP与原文锚点（U1/K2）。
5. 学生前台文字过课堂朗读测试。学生可见区不出现教学目标、学生画像、设计理由、失败信号、代理思路或机器语言（P-07/J4）。
6. 把S3已经冻结的**逐页真实剧本**同源投影为讲者备注和独立screenplay，不新增讲授结论、不改等待时序、不替换学生回应分支；只允许为放映操作补充不改变教学含义的设备提示。
7. 视觉和插图只服务页面唯一功能；无功能装饰默认删除。
8. 生成 `lesson-materials-manifest.v1`，至少登记pptx、screenplay、learning_sheet、board_plan及SHA-256；四种角色必须路径不同、内容哈希不同且各有最低有效内容，剧本逐页锚定page ID与真实课堂要素，学习单和板书回扣教材原文。manifest与全部物料只放同一课`materials/`目录，目录内不得有清单外文件，课目录根部不得留PPTX/DOCX；写含非空字符串S4内容作者`author_id`的 `_meta/materials_lock.json`。
9. 完成QA渲染“发现→修复→复验”闭环后，运行 `python3 scripts/validate_lesson_lineage.py materials <materials_lock.json>` 及构建/原则检查。

## 放行条件

- design lock有效；全部产物由同一数据源生成且哈希登记；
- PPTX不是空白结构包，slide级关系不依赖外部网络内容；图片只有在`r:embed`、内部image关系和非空media部件完整绑定时才算可见对象，空`p:pic`不算；三种文本物料通过角色内容与同源锚点底线；
- 前台禁词扫描 0 命中；
- 学习单分发时点表完成；
- 朗读测试逐页通过（人检，记录在案）；
- QA 渲染环完成至少一轮"发现→修复→复验"闭环。

## 常见错误

- PPT 与母版措辞分叉（违反 P-11）；
- 学习单装订成一册导致提前泄答（U1 断裂）；
- 备注写"此处沉默三秒"上屏（舞台指令属于后台，P-07）。
- 在制作阶段新增知识、改目标、换活动机制、改变语义分组或分页、重写逐字稿或调换信息顺序；需要改变时退回S3，必要时继续退回G1。
