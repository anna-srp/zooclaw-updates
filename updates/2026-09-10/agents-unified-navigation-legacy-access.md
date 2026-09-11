---
title: "Agents 导航大统一：一个 Agent 名下直接挂任务、Build、产物、定时任务和渠道，旧版 project 也能继续用"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-10"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog+社媒素材"
---

# Agents 导航大统一：一个 Agent 名下直接挂任务、Build、产物、定时任务和渠道，旧版 project 也能继续用

## 核心宣传点

昨天上线的「自进化 Agent」把 Agent 变成了导航的一级对象，今天把这套导航正式铺满：**全局 Agents 导航与 V2 工作区合并成一套**，不再有两个平行的入口。

具体你会看到：

- **导航结构收敛**。五个分页的 Agent 快捷入口 + 固定的 Main 入口，外加 Connector / MCP / Skills / Knowledge Base 的直达链接。Main 仍然保持不可构建（不进 buildable 列表），已有的运行时 ID、任务、渠道和定时任务全部原样保留。
- **旧版 Agent 不用先迁移也能继续干活**。没有可编辑基线（baseline）的遗留 Agent，照样能正常用任务、历史、产物、定时任务和渠道；只有 Build、Agent Settings、Share、Rename 这四件事需要基线。Delete 沿用原有的确认与生命周期，Main 依旧受保护。
- **基线是从「你实际装的那份源」原地准备的**，persona 文件、私有/全局 skill 的归属、运行时配置和 environment pin 都保留，不会在转换过程里被抹平。这一版没有 Engine/ACS 改动，也没有数据库迁移。
- **全局 New Task 可以直接挑 Agent**了：自建的、别人分享的、遗留的都能选，走的是现有会话/对话通道。底部那个「Hire more Agents」页脚移除。

这次合并同样带了独立复审：三路复审分别覆盖前端、business API、基线/运行时源行为，提交前修掉的问题包括——补回丢失的固定 Main 入口（但不让 Main 变成可编辑）、模型选择器改用 Revision 提交而不是那个会拒绝定义编辑的遗留接口。

## 原始内容

### feat(agents): unify agent navigation and legacy workspace access (#3693)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `edfde328`
- PR: #3693
- 作者: kaka-srp
- 日期: 2026-09-10T11:36:18Z

### Summary（PR 原文要点）

- Unify the global Agents navigation with the existing V2 workspaces: five paginated shortcuts, fixed Main access, and direct Connector/MCP/Skills/Knowledge Base links. Keep Main out of the buildable list and preserve existing runtime IDs, tasks, channels and schedules.
- Prepare editable baselines in place from exact installed sources, preserving persona files, private/global skill ownership, runtime configuration and environment pins. No Engine/ACS changes or database migration in this PR.
- Keep ordinary task/history/artifact/schedule/channel use available for legacy Agents without a baseline. Build, Agent Settings, Share and Rename require a baseline; Delete retains the existing confirmation/lifecycle and Main protection.
- Global New Task can select available created/shared/legacy Agents and send through the existing session/conversation transport. Remove the Hire more Agents footer.

### 复审修正（PR 原文）

Independent reviewers covered frontend, business APIs, and baseline/runtime-source behavior. Verified issues fixed before submission: restore the missing fixed Main destination without making Main editable; use Revision commits for the selected definition's model picker instead of the legacy endpoint that rejects definition edits.

## 备注

发布状态：已合并待发版（尚未包含在最新的 `ecap-v0.19.3-release` 中）。

对外发布注意：这条与 2026-09-09 的「自进化 Agent」是同一条产品线的延续，对外可以合并成一个叙事讲，但要写清「旧版 project 不会丢、没有基线也能照常用任务」，避免用户担心迁移成本。
