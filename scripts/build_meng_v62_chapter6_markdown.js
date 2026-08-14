#!/usr/bin/env node
"use strict";
const crypto=require("crypto"),fs=require("fs"),path=require("path"),source=require("./meng_v62/content/chapter_6"),{validate}=require("./verify_meng_v62_chapter6"),{PROJECT_ROOT,stageDir,assertV62OutputPath}=require("./meng_v62/paths");const OUT=assertV62OutputPath(path.join(stageDir(),"chapter_6","package")),SOURCE=path.join(PROJECT_ROOT,"scripts","meng_v62","content","chapter_6.js");function hash(v){return crypto.createHash("sha256").update(v).digest("hex")}function fh(f){return hash(fs.readFileSync(f))}function mark(id){return`<!-- V63_PAGE:${id} -->`;}
function lesson(data,h){const a=["---","document_type: teaching_master","lesson: \"《氓》第六章\"",`version: "${data.version}"`,`source_sha256: "${h}"`,`claim_boundary: "desktop_design_scaffold_only"`,"---","","# 《氓》V6.3第六章教学母版","","> 第六章以完整时间回环、老字铰链、多义边界、旧日/今日双真相、末句双声、撤答全诗接续推进。",""];for(const p of data.pages){a.push(mark(p.page_id),`## ${p.page_id}｜${p.title}｜${p.minutes}分钟`,"",`- 当前困难：${p.current_difficulty}`,`- 唯一功能：${p.unique_function}`,`- 删除损失：${p.deletion_loss}`,`- 合并反证：${p.merge_test}`,"","```text",p.visible,"```","");for(const x of p.student_action)a.push(`- 学生动作：${x}`);a.push(`- 作品：${p.artifact}`,`- 反馈：${p.bounded_feedback}`,`- 修订：${p.revision}`,`- 教师后置：${p.teacher_synthesis}`,`- 回到故事：${p.story_return}`,`- 后用：${p.next_use}`,`- 视觉：${p.visual_duty}`,`- 第一人称：${p.first_person_reception}`,"")}return`${a.join("\n").trim()}\n`}
function worksheet(d){const p=Object.fromEntries(d.pages.map(x=>[x.page_id,x]));return`---
document_type: chapter6_progressive_worksheet
lesson: "《氓》第六章"
version: "${d.version}"
distribution: "C601 after complete reading; reveal one section at a time"
---

# 第六章｜最后一次回望

## C601｜完整读完以后

回到过去的原句：__________________________________________________

收束全诗的原句：__________________________________________________

初始声音词或问号：________________

-------------------- 请先折到这里 --------------------

## C602｜两个“老”

${p.C602.original_text}

第一个“老”落在________________；第二个“老”落在________________。

听者反馈与我的改读：________________________________________________

## C603｜有岸、有泮

${p.C603.original_text}

解释A：________________　接回原句：________________

解释B：________________　接回原句：________________

我现在更接受：□A　□B　□并列　理由：____________________________

## C604｜旧日与今日

她记住的旧日：____________________________________________________

今天核验出的事实：________________________________________________

能同时容纳两件真的一句话：________________________________________

## C605｜亦已焉哉

回来的词：________________／________________

停止判断怎样形成：________________________________________________

声线A听感：________________　声线B听感：________________

诗写了：________________　诗没有继续写：__________________________

## C606｜第六章旁白与六章轨道

合书讲40秒：旧愿怎样反折｜她重新看见什么｜最后作出怎样的判断

故事轨道第六格：__________________________________________________

取出第一至第六章六张章末卡，按章序排成一列。跨课时由小组材料袋收存并在下一课课前原组返还；缺卡者借同桌核对，在临时便笺补一个替代格。

一 → 二 → 三 → 四 → 五 → 六

六章连讲中的真实断点：____________________________________________

若没有断点，写最清楚的一处因果：____________________________________
`}
function script(d,h){const a=["---","document_type: page_by_page_rehearsal_script","lesson: \"《氓》第六章\"",`version: "${d.version}"`,`source_sha256: "${h}"`,`claim_boundary: "scripted_not_observed"`,"---","","# 《氓》V6.3第六章逐页无生试讲稿",""];for(const p of d.pages){const s=p.script;a.push(mark(p.page_id),`## ${p.page_id}｜${p.title}｜${p.minutes}分钟`,"","【本页不可替代的意义】","",p.unique_function,"","【删除本页会失去什么】","",p.deletion_loss,"","【场面】","",s.scene,"","【教师实际说】","",`“${s.teacher_spoken}”`,"","【动作、等待与走位】","");for(const x of s.timeboxes)a.push(`- ${x.label}：${x.seconds}秒`);for(const x of s.stage_directions)a.push(`- （${x}）`);a.push("","【现场分支】","");for(const x of s.branches)a.push(`- ${x.kind}：${x.response}`);a.push("","【听者同时做什么】","",s.listener_task,"","【证据留在哪里】","",s.evidence_location,"","【回到人物和故事】","",p.story_return,"","【后续怎样真实调用】","",p.next_use,"","【怎样自然切页】","",`“${s.cut_line}”`,"")}return`${a.join("\n").trim()}\n`}
function main(){const r=validate(source);if(!r.ok)throw new Error(JSON.stringify(r.errors));const h=fh(SOURCE);fs.mkdirSync(OUT,{recursive:true});const snap={...source,source_sha256:h,claim_boundary:"desktop_design_scaffold_only"},outs=[["02_氓_V63第六章教学母版.md",lesson(source,h)],["06F_氓_V63第六章渐进学习单_C601读后发.md",worksheet(source)],["04A_氓_V63第六章逐页无生试讲稿.md",script(source,h)],["06_氓_V63第六章课程数据快照.json",`${JSON.stringify(snap,null,2)}\n`]];for(const[n,c]of outs)fs.writeFileSync(path.join(OUT,n),c);fs.writeFileSync(path.join(OUT,"chapter6_package_manifest.json"),`${JSON.stringify({schema_version:"1.1",module_id:source.module_id,version:source.version,source_sha256:h,files:outs.map(([name])=>({name,sha256:fh(path.join(OUT,name))}))},null,2)}\n`);process.stdout.write(`V63_CHAPTER6_MARKDOWN_OK pages=${source.pages.length} minutes=${source.total_minutes} out=${OUT}\n`)}if(require.main===module)main();module.exports={lesson,worksheet,script};
