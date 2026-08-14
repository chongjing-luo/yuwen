#!/usr/bin/env node
"use strict";
const crypto=require("crypto"),fs=require("fs"),path=require("path");
const source=require("./meng_v62/content/chapter_5");const {validate}=require("./verify_meng_v62_chapter5");const {PROJECT_ROOT,stageDir,assertV62OutputPath}=require("./meng_v62/paths");
const OUT=assertV62OutputPath(path.join(stageDir(),"chapter_5","package"));const SOURCE_FILE=path.join(PROJECT_ROOT,"scripts","meng_v62","content","chapter_5.js");
function sha(v){return crypto.createHash("sha256").update(v).digest("hex");}function fileSha(f){return sha(fs.readFileSync(f));}function marker(id){return`<!-- V63_PAGE:${id} -->`;}
function lesson(data,sourceSha){const lines=["---","document_type: teaching_master","lesson: \"《氓》第五章\"",`version: "${data.version}"`,`source_sha256: "${sourceSha}"`,"claim_boundary: \"desktop_design_scaffold_only\"","---","","# 《氓》V6.3第五章教学母版","","> 第五章以完整章声、一天折进多年、后文回看婚前细节、外声与内声、撤答生活旁白五个事件推进。","",`- 逻辑页：${data.pages.length}页`,`- 自然时长：${data.total_minutes}分钟`,""];for(const p of data.pages){lines.push(marker(p.page_id),`## ${p.page_id}｜${p.title}｜${p.minutes}分钟`,"","### 页面功能","",`- 文学对象：${p.literary_object}`,`- 当前困难：${p.current_difficulty}`,`- 唯一功能：${p.unique_function}`,`- 删除损失：${p.deletion_loss}`,`- 相邻合并：${p.merge_test}`,"","### 学生看见","","```text",p.visible,"```","",`第一眼：${p.first_glance}`,"","### 学生生成","");for(const a of p.student_action)lines.push(`- ${a}`);lines.push("",`- 作品：${p.artifact}`,`- 正常路径：${p.normal_path}`,`- 反馈：${p.bounded_feedback}`,`- 修订：${p.revision}`,"",`- 教师后置归纳：${p.teacher_synthesis}`,`- 回到故事：${p.story_return}`,`- 后续调用：${p.next_use}`,`- 视觉职责：${p.visual_duty}`,`- 第一人称接收：${p.first_person_reception}`,"");}return`${lines.join("\n").trim()}\n`;}
function worksheet(data){const p=Object.fromEntries(data.pages.map(x=>[x.page_id,x]));return`---
document_type: chapter5_progressive_worksheet
lesson: "《氓》第五章"
version: "${data.version}"
distribution: "C501 after complete reading; reveal one section at a time"
---

# 第五章｜一间屋子里的许多年

## C501｜完整读完以后

反复的生活动作：________________

声音转向内心的原句：____________________________________________

-------------------- 请先折到这里 --------------------

## C502｜一天折进多年

${p.C502.original_text}

一天从________________开始，到________________结束。

让它不只发生一天的字：________________

生活旁白：________________________________________________________

我的用词修订：____________________________________________________

## C503｜后文照亮开头

${p.C503.original_text}

既遂以后：________________________________________________________

婚前细节｜现在值得警惕什么｜仍不足以证明什么

蚩蚩｜________________｜________________

贸丝／来即我谋｜________________｜________________

将子无怒｜________________｜________________

## C504｜外声停下以后

${p.C504.original_text}

外面的笑声停下以后，我听见／看见：____________________________________

第三人称处境句：她身边缺少________________________________________

事实边界修订：____________________________________________________

## C505｜第五章旁白与故事轨道

合书讲40秒：她怎样过日子｜男子怎样变化｜外面的声音散去，谁留下

听者只报一个断点：________________________________________________

故事轨道第五格：__________________________________________________
`;}
function script(data,sourceSha){const lines=["---","document_type: page_by_page_rehearsal_script","lesson: \"《氓》第五章\"",`version: "${data.version}"`,`source_sha256: "${sourceSha}"`,`claim_boundary: "scripted_not_observed"`,"---","","# 《氓》V6.3第五章逐页无生试讲稿",""];for(const p of data.pages){const s=p.script;lines.push(marker(p.page_id),`## ${p.page_id}｜${p.title}｜${p.minutes}分钟`,"","【本页不可替代的意义】","",p.unique_function,"","【删除本页会失去什么】","",p.deletion_loss,"","【场面】","",s.scene,"","【教师实际说】","",`“${s.teacher_spoken}”`,"","【动作、等待与走位】","");for(const x of s.timeboxes)lines.push(`- ${x.label}：${x.seconds}秒`);for(const x of s.stage_directions)lines.push(`- （${x}）`);lines.push("","【现场分支】","");for(const x of s.branches)lines.push(`- ${x.kind}：${x.response}`);lines.push("","【听者同时做什么】","",s.listener_task,"","【证据留在哪里】","",s.evidence_location,"","【回到人物和故事】","",p.story_return,"","【后续怎样真实调用】","",p.next_use,"","【怎样自然切页】","",`“${s.cut_line}”`,"");}return`${lines.join("\n").trim()}\n`;}
function main(){const report=validate(source);if(!report.ok)throw new Error(JSON.stringify(report.errors));const sourceSha=fileSha(SOURCE_FILE);fs.mkdirSync(OUT,{recursive:true});const snapshot={...source,source_sha256:sourceSha,claim_boundary:"desktop_design_scaffold_only"};const outputs=[["02_氓_V63第五章教学母版.md",lesson(source,sourceSha)],["05E_氓_V63第五章渐进学习单_C501读后发.md",worksheet(source)],["04A_氓_V63第五章逐页无生试讲稿.md",script(source,sourceSha)],["06_氓_V63第五章课程数据快照.json",`${JSON.stringify(snapshot,null,2)}\n`]];for(const [n,c] of outputs)fs.writeFileSync(path.join(OUT,n),c,"utf8");fs.writeFileSync(path.join(OUT,"chapter5_package_manifest.json"),`${JSON.stringify({schema_version:"1.1",module_id:source.module_id,version:source.version,source_sha256:sourceSha,files:outputs.map(([name])=>({name,sha256:fileSha(path.join(OUT,name))}))},null,2)}\n`);process.stdout.write(`V63_CHAPTER5_MARKDOWN_OK pages=${source.pages.length} minutes=${source.total_minutes} out=${OUT}\n`);}
if(require.main===module)main();module.exports={lesson,worksheet,script};
