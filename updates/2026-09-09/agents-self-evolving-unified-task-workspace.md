---
title: "自进化 Agent 上线：在同一个任务工作区里边聊边改，Agent 自己升级自己"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-09"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog+社媒素材+push"
---

# 自进化 Agent 上线：在同一个任务工作区里边聊边改，Agent 自己升级自己

## 核心宣传点

这是 Agent Builder 的一次范式换血：**你创建的不再是一份「待构建的配置」，而是一个当场就能跑的真 Agent**；之后想改它，就在 Build 里跟它对话，它通过源码 Revision 升级**自己**——没有 Pack 打包流水线，没有 archive 构建，也没有另外那个「负责帮你造 Agent 的 Agent」。

具体变化：

- **Build 用的就是正常聊天界面**。消息、历史、附件走的都是现有 ACS/Engine 通道，Build 有自己独立的会话；普通任务线程会在你下一次开口时自动用上最新配置。
- **改动自动提交并生效**。Preview / Activate / My Team 发布这一整套流程从这个功能里移除了——不用再手动点「预览」再点「激活」。
- **Agent 变成导航的一级对象**。每个 Agent 名下直接挂着：任务、Build、产物（Artifacts）、定时任务、已连接渠道。
- **能改的东西挺全**：源文件、技能、头像都能在里面写；分享链接装进来的是一份**独立可编辑的副本**（不是只读引用）；另外做了 14 天活跃度与会话量的批量快查。
- **老入口退场**：全局 marketplace 与旧版 Builder 导航、旧的 project 创建流程一并下线；已有的旧 project 仍可从 Agents → Legacy agent projects 继续编辑，不会丢。

工程上这次是「合并 + 全量复审 + 修复」一起落的：三个独立 Agent 分别复审了 Web、business/backend、Engine/ACS 三条线，结论逐条对着当前源码和已确认的产品决策裁决后才修。几个值得一提的收口：授权对话会绑定到**当次精确的运行配置**（含最新渠道/MCP 凭据），重试与已提交的工具回执保留原快照；共享安装锁下加了持久化配额预留、同键单次执行、失败运行时清理；创建、分享安装、源码提交都强制走正常套餐的模型权限；依赖重建冲突会**显式告诉你「已保存但未应用」**，不会偷偷打断正在跑的任务。

同日还跟了三条修复（都在下面的原始内容里）：Artifacts 页对自进化 Agent 报「Agent runtime state could not be verified」已修；创建时填的意图现在会**自动作为 Build 的第一句话发出去**，不用再手打一遍；分享安装预览一度报 `Internal Server Error`（加密客户端不支持跨集合 `$lookup`）也已修。

## 原始内容

### feat(agents): build self-evolving agents in a unified task workspace (#3673)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `7c424992`
- PR: #3673
- 作者: kaka-srp
- 日期: 2026-09-09T06:56:52Z
- 配套 PR: zooclaw-engine#1297、agent-channel-service#117

### Summary

- Create a real runnable Agent; Build upgrades that same Agent through source Revisions. No Pack/archive build pipeline or separate builder Agent.
- Reuse the full normal chat UI and ACS/Engine message, history and attachment transport. Build has a dedicated session; normal task threads use the latest settings on their next user turn.
- Commit/apply source changes automatically. Remove Preview/Activate/My Team publication from this feature. Agent-scoped navigation includes tasks, Build, artifacts, schedules and connected channels.
- Support source-file and skill editing, avatar authoring, share-link installation into an independent editable copy, and fast bulk 14-day activity/conversation statistics.
- Retire global marketplace/legacy Builder navigation and legacy project creation; retain existing project editing through Agents → Legacy agent projects.

### 同日配套修复

**fix(agents): use runtime identity for self-evolving artifacts (#3677)** — SHA `83c21054`，2026-09-09T08:13:22Z，kaka-srp

新 Agent 在 Engine 里存的是不透明的运行时归属锚点，而 Artifact 适配器仍在传调用方的 business UID/org。staging 上同一个 Agent 的 artifact-list 请求：用 business actor 返回 `404 agent_not_found`，用定义里的 runtime actor 返回 `200`，ECAP 把前者映射成「Agent runtime state could not be verified」。现改为用既有 `runtime_actor` helper 解析已授权工作区的运行时归属，应用到 Artifact Library 分页、单 Agent 产物的 list/get/download/delete 以及工作区文件 list/content。普通 Engine 与旧运行时行为、business 归属校验、V2 资格校验均未改动。

**fix(agents): fix initial Build, shared installs and launch notices (#3678)** — SHA `6d1d49a2`，2026-09-09T12:00:36Z，kaka-srp

根因：创建 Agent 时只持久化了初始配置，没有把首条用户消息投进 Build 会话，导致用户跳转后得把意图**重打一遍**。现在创建意图会先经现有 Mattermost 会话通道发出首轮 Build 对话再跳转；手输意图与示例提示走同一条路径，空白创建仍保持空白。另外：失败时保留创建幂等键、重发前先对齐线程历史（含丢失的 POST 响应）；开通前先校验共享 Mattermost 的消息长度上限（4,000 字符通过，4,001/8,000 在开通前即拒绝），避免创建出一个首条消息永远发不出去的 Agent。同 PR 还把 ECAP 前后端的 Launch 发布说明生成切到 Azure Responses + GPT-5.6 Terra（此前 Claude 返回 `is_error: true` 导致 `ecap-v0.19.0-release` 与 `service-v0.18.0-release` 的通知失败，生产部署本身是成功的），并修正手动补发时把 annotated tag 解析成 tag-object SHA、可能把当前部署当成自己的基线误报为回滚的问题（未发出错误公告）。

**fix(agents): use CSFLE-compatible shared install lookup (#3681)** — SHA `48930586`，2026-09-09T12:47:22Z，kaka-srp

#3678 之后，共享 Agent 的安装预览与安装报 `Internal Server Error`。根因是部署环境的 CSFLE 加密客户端在 MongoDB 执行之前就拒绝了跨集合 `$lookup` 聚合——普通 MongoDB CI 测试却是通过的。修复只替换 source-install 这一处 lookup：改成按 owner/org 限定范围的有界单集合读取 + 批量关联，跨链接重建仍保留 source 身份、优先取最新保留副本、保留最近一条已删除记录以便重装，且按批持续推进（不再只静默检查前 N 条），也没有逐记录 N+1 查询。同时补了分页/归属回归覆盖，加了一个针对已知不支持的跨集合 stage 与直接指定聚合管道更新的语法守卫（明确声明**不能**替代真实的 CSFLE 验证），并把这条「加密客户端兼容性」教训写进根目录与后端的 `AGENTS.md`：不绕过加密，新查询形式必须用真实加密客户端验证，不能只靠 plain-Mongo CI。

## 备注

发布状态：主功能 `7c424992` 及 `83c21054`、`6d1d49a2` 均已包含在最新 `ecap-*-release` 正式发布中（已上线）；最后一条修复 `48930586` 已合并待发版。

对外发布注意：PR 自述「协同的 feature/staging 验收与必需的人工审批尚未完成，本轮复审未执行线上放量」。对外传播前建议确认放量状态与 `48930586` 的发版情况。另注意本次下线了全局 marketplace 与旧版 Builder 导航，属于**入口变更**，对外文案需要同时给出旧 project 的新位置（Agents → Legacy agent projects）。
