---
name: yuwen-trial-observation
description: 高中语文课课堂实施与观察（S6 环节）。当需要准备试教/授课的观察表、采集三目标课堂证据时使用。
---

# 课堂实施与观察（S6）

服务机制节点：**课堂账的观察来源**——全部20节点的课堂度量可经此采集。这是桌面账与课堂账的分界（P-12）；执行依据为`work/methodology/manuals/S6-观察手册.md`的`MM-S6-00`—`MM-S6-05`。

## 输入

- 当前G4 `audit_lock.json`与S4物料包/逐屏真实剧本
- 项目外宿主提供的`external-host-release-registry.v1`；事件必须绑定本课、当前G4锁哈希与可追溯宿主记录
- 观察字段契约：`work/teaching/_shared/evidence_schemas.md`；观察表须由当前课程的G4锁与S6手册生成，不引用已退出正式树的旧课例模板

## 步骤

1. **S6准入**：不得信任项目内“已放行”JSON。核对宿主项目外事件与当前G4锁哈希，准备OBS时写入`g4_audit_lock_sha256/host_release_event_id/host_release_source`；运行：
   ```bash
   python3 scripts/validate_evidence.py <obs.jsonl> --type obs --host-release-registry <宿主只读路径> --audit-lock <当前课程/_meta/audit_lock.json>
   ```
   缺事件、错哈希或注册表位于项目目录内，停止试教准备（J7）。
2. 试教前冻结课程数据版本与标准版本（审查链延续）。
3. 按三目标配置观察信号（每信号对应节点）：
   - **学懂**：首答阶段非空白抽样率（U1）；个人末答抽样正确率（U3）；修订痕迹率（U8）；学生用原词自证比例（U2）
   - **知识**：章意/字词闭卷复述质量（K2/K3）
   - **享受**：主动开口率与自愿发言面（J1/J3）；自发回读与课后谈论（J4）；沉默学生的真实完成路径（U7/J6）
   - **负荷**：实际耗时 vs 时间盒偏差（U5）；累计疲劳信号
4. 观察纪律：记录事实不记录评价；"这节课很顺"不是证据（J7 流畅错觉）。
5. 采集学生作品样本（学习单、末答、作业）并保留原件照片/扫描。
6. 课后只追加S6责任产物：OBS写入`work/teaching/_classes/<班级>/observations.jsonl`，学生作品原件/照片按来源登记并供S7/S9引用；不修改既有L4行。
7. 不在S6写mastery ledger，也不修改`work/evaluation/reports/`充当课堂账。S7记录GRD，S8消费批改/测验证据形成MR；全局自检只读统计L4。

## 放行条件（观察有效性）

- 每个预设信号有真实记录或如实标"未采集到"；
- 每条OBS均通过项目外宿主放行事件与当前G4锁哈希核验；
- 学生作品样本可追溯到具体页/题；
- 无任何用桌面推演代替观察的条目。

## 常见错误

- 只记录"气氛好"；只采前排学生样本；把公开回答当个人掌握（P-41）；
- 在项目内创建`host_release.json`，或把G4候选校验通过误当宿主放行；
- 试教后不回流数据——课堂证据断链，三目标失去验证。
