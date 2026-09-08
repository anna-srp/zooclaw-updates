---
title: "修复：聊天记录里那条永远转圈的「routing decision」不见了"
type: "Bug Fix"
priority: "中"
date: "2026-09-07"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：聊天记录里那条永远转圈的「routing decision」不见了

## 核心宣传点

翻旧对话时，有些会话里会挂着一条永远在「进行中」的活动步骤——名字叫 `routing_decision`，转圈转到天荒地老，看上去像是有个任务卡死了没跑完。实际上什么都没卡住：那是引擎在决定「这条消息交给谁处理」时留下的一次性内部决策记录。

根因是这类决策被当成普通的工具进度事件发布出来，带着 `phase=update` 却永远不会有配套的「完成」事件。前端拿到这种通用进度结构，只能按「还在运行」渲染——它的判断没错，是这类事件根本不存在终态。

现在把这个内部事件名加进了前端已有的隐藏工具清单，历史记录加载和新收到的消息都会经过同一个解析器过滤掉，之前已经存进数据库的那些残留决策也不会再显示了。引擎的路由数据本身没有改动，正常的工具进度和助手回复照常可见。另有一处配套改动（在 agent-channel-service 侧）从源头上不再产生新的路由决策工具消息。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `2ba2c816`
- PR: #3661
- 日期: 2026-09-07

### Commit Message

```
fix(chat): hide historical routing decision progress (#3661)

## Summary
Hide `routing_decision` tool-status posts through the shared parser,
covering history loading and incoming messages. Previously saved routing
decisions no longer render as indefinitely running activity steps.
Ordinary tool progress and assistant replies remain visible.

## Root cause
The channel conversion published one-shot engine routing decisions with
`phase=update` and no terminal status. The frontend correctly
interpreted that generic progress shape as running, but no completion
event exists for these decisions. Add the internal event name to the
existing hidden-tool list; engine routing data is not changed.

The companion agent-channel-service fix prevents new routing-decision
tool posts.

## Test plan
- [x] Tool-status parser and chat activity suites: 88 tests passed.
- [x] Changed-file ESLint and git diff checks passed.
- Full web gate was not run; Git hooks skipped it because the worktree
has no workspace-root node_modules. Targeted checks above were run using
the existing app dependencies.
```

## 备注

发布状态：已上线（已包含在最新的 `ecap-*-release` 前端正式发布中）。
