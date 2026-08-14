#!/usr/bin/env node
"use strict";

const payload=require("./meng_v62/content/chapter_5");
const {contract:textContract}=require("./meng_v6/text");
const {validate:validateTextContract}=require("./meng_v6/verify_text");
const EXPECTED_IDS=["C501","C502","C503","C504","C505"];
const EXPECTED_LINES=["L021","L022","L023","L024","L025"];
const ALLOWED=["L001","L002","L005"];
const BANNED=[/学生画像/u,/教学目标/u,/设计意图/u,/理解链/u,/学习任务群/u,/标准答案/u,/恋爱脑/u,/身体暴力/u,/全家拒绝/u,/系统伪装/u];
function compact(text){return String(text).replace(/[，。！？；：、\s｜《》“”‘’—]/gu,"");}
function validate(data=payload){const errors=[],warnings=[];const fail=(code,page_id="MODULE",detail="")=>errors.push({code,page_id,detail});
 if(data.module_id!=="MENG_V63_CHAPTER_5"||data.module!=="chapter_5")fail("IDENTITY_MISMATCH");
 if(data.status!=="implementation_candidate")fail("STATUS_NOT_CANDIDATE");
 if(data.prerequisite_module!=="MENG_V63_CHAPTER_4"||data.next_module!=="MENG_V63_CHAPTER_6")fail("MODULE_CHAIN_MISMATCH");
 const pages=Array.isArray(data.pages)?data.pages:[];if(JSON.stringify(pages.map(x=>x.page_id))!==JSON.stringify(EXPECTED_IDS))fail("PAGE_SEQUENCE_MISMATCH");
 if(data.total_minutes!==31||pages.reduce((a,b)=>a+Number(b.minutes||0),0)!==31)fail("TOTAL_TIME_MISMATCH");
 const textErrors=validateTextContract(textContract);if(textErrors.length)fail("FROZEN_TEXT_CONTRACT_INVALID","MODULE",textErrors.join(","));
 const lineMap=Object.fromEntries(textContract.lines.map(x=>[x.line_id,x.text]));const chapter=textContract.chapters.find(x=>x.chapter_id==="C5");
 if(compact((data.chapter_text||[]).join(""))!==compact(chapter.line_ids.map(id=>lineMap[id]).join("")))fail("CHAPTER_TEXT_MISMATCH");
 if(data.materials?.[0]?.first_distribution_event!=="C501_AFTER_COMPLETE_READ")fail("MATERIAL_DISTRIBUTION_MISMATCH");
 const seen=new Set(),signatures=new Set();for(const page of pages){const id=page.page_id||"UNKNOWN";for(const key of ["title","source_line_refs","original_text","literary_object","current_difficulty","unique_function","visible","student_action","artifact","bounded_feedback","revision","story_return","next_use","deletion_loss","merge_test","visual_duty","interaction_signature","first_person_reception","screen","script"])if(page[key]===undefined||page[key]===null||page[key]==="")fail("REQUIRED_FIELD_EMPTY",id,key);
  for(const ref of page.source_line_refs||[]){if(![...EXPECTED_LINES,...ALLOWED].includes(ref))fail("OUT_OF_SCOPE_LINE_REF",id,ref);if(EXPECTED_LINES.includes(ref))seen.add(ref);if(!compact(page.original_text).includes(compact(lineMap[ref]||"")))fail("LINE_REF_TEXT_MISMATCH",id,ref);}
  const seconds=(page.script?.timeboxes||[]).reduce((a,b)=>a+Number(b.seconds||0),0);if(seconds!==page.minutes*60)fail("TIMEBOX_MISMATCH",id,`${seconds}/${page.minutes*60}`);if((page.script?.branches||[]).length<3)fail("BRANCHES_TOO_THIN",id);if((page.script?.stage_directions||[]).length<5)fail("STAGING_TOO_THIN",id);if((page.script?.teacher_spoken||"").length<220)fail("SCRIPT_NOT_REHEARSABLE",id);for(const pattern of BANNED)if(pattern.test(page.visible))fail("VISIBLE_META_OR_LEAK",id,String(pattern));const sig=Object.values(page.interaction_signature||{}).slice(0,4).join("|");if(signatures.has(sig))fail("INTERACTION_DUPLICATED",id);signatures.add(sig);
 }
 if(JSON.stringify([...seen].sort())!==JSON.stringify(EXPECTED_LINES))fail("CHAPTER_COVERAGE_INCOMPLETE");const by=Object.fromEntries(pages.map(x=>[x.page_id,x]));
 if(!/三人一组/u.test(by.C503?.script?.teacher_spoken||"")||!/不足以证明/u.test(by.C503?.visible||""))fail("C503_REVISIT_BOUNDARY_MISSING","C503");
 if(!/沉默三秒/u.test(by.C504?.script?.teacher_spoken||"")||!/第三人称/u.test(by.C504?.script?.teacher_spoken||""))fail("C504_SAFE_SOUNDFIELD_MISSING","C504");
 if(!/合上教材/u.test(by.C505?.script?.teacher_spoken||"")||!/按B键熄暗屏幕/u.test(by.C505?.script?.teacher_spoken||""))fail("C505_SUPPORT_REMOVAL_MISSING","C505");
 return{ok:errors.length===0,module_id:data.module_id,pages:pages.length,total_minutes:data.total_minutes,errors,warnings};}
function main(){const report=validate(payload);process.stdout.write(`${JSON.stringify(report,null,2)}\n`);if(!report.ok)process.exitCode=1;}
if(require.main===module)main();module.exports={validate};
