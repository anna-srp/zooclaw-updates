---
title: "修复：子任务失败重试成功后，活动摘要还一直挂着「Delegated work · needs attention」"
type: "Bug Fix"
priority: "中"
date: "2026-09-10"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：子任务失败重试成功后，活动摘要还一直挂着「Delegated work · needs attention」

## 核心宣传点

9 月 3 日上线的「聊天里能看到 Agent 派给子任务的活干到哪了」有个让人误判的显示问题：**子任务第一次创建失败、后来重试成功了，活动摘要却还停在 `Delegated work · needs attention`**，看上去像是活没干成。

现在这块的逻辑改了：终态的尝试回归普通的活动摘要规则，失败的那次尝试**仍然保留在可展开的明细行里**（不丢历史，只是不再绑架整组状态）。另外，**正在运行或等待授权的子任务被拆到独立的 delegated-work 分组**，带自己的状态和已耗时，不会再反过来覆盖普通的活动摘要。

根因：delegated-work 摘要此前只要存在任何 `sessions_spawn` 步骤，就绕过普通活动规则。于是历史上的 spawn 报错会把整组一直钉在失败并展开状态；反过来，一个已完成的子任务也可能把仍在运行的普通工具遮住。把「活跃子任务」和「历史步骤」分开之后，终态尝试就能正常走既有的活动摘要规则。

改动范围仅限共享的 `ToolGroup` 组件及其渲染测试。

## 原始内容

### fix(chat): isolate active subagents from activity summaries (#3689)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `b0739251`
- PR: #3689
- 作者: kaka-srp
- 日期: 2026-09-10T08:02:39Z

When subagent creation fails and later retries succeed, the activity summary now returns to the normal completed state instead of remaining at `Delegated work · needs attention`. Failed attempts stay available in the expandable detail rows. Active or approval-waiting subagents appear in a separate delegated-work group, with their own status and elapsed time, so they cannot override the ordinary activity summary.

验证：ToolGroup 与 AssistantMessage 渲染套件 82 passed，覆盖被拒调用与重试成功、恢复时序、独立的运行/授权状态、子任务完成/失败进入历史；`pnpm tsc`、`pnpm lint`（web/packages/chat-ui）、`git diff --check` 通过。

## 备注

发布状态：已上线（已包含在 `ecap-v0.19.3-release` 正式发布中）。
