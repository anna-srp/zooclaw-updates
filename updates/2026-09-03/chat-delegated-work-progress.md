---
title: "聊天里能看到「Agent 派给子任务的活干到哪了」"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-03"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# 聊天里能看到「Agent 派给子任务的活干到哪了」

## 核心宣传点

Agent 在处理复杂任务时会把工作拆出去交给子任务（delegated work）执行。以前这些子任务在对话里没有独立的呈现，你只能看到一段最终结果，中间到底派了几个活、哪个在跑、哪个卡住需要你介入，都看不出来。

现在对话里会把派发出去的子任务渲染成一个专门的进度组，每个子任务带四种状态：进行中（running）、需要关注（attention）、已完成（completed），并显示已耗时。长的子任务详情直接在对话流里就地展开阅读，不再塞进一个小小的嵌套滚动框里翻。顶部的状态摘要只统计当前展示的优先状态下的任务数，保证「摘要数字」和「下面列出来的任务」始终对得上，不会出现摘要说 3 个进行中、列表里只有 1 个的情况。

中英文文案都已就位。这条改动是三端协同的：Engine 侧负责产出进度事件、Agent Channel Service 负责按契约投递、Web 侧负责渲染，需要三方都部署到位后才完整生效。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `84e12b5872281dc4b72457262e7809edf23d3e56`
- PR: #3640
- 作者: kaka-srp
- 日期: 2026-09-03T13:41:54Z

### Commit Message

```
feat(chat): show delegated work progress (#3640)

## Linear

Not applicable — requested without a Linear issue.

## Summary

- document the complete v2 Engine → ACS channel delivery → Web rendering
design
- render delegated child work as a dedicated progress group with
running, attention, completed, and elapsed states
- expand long child-task details inline in the conversation instead of
inside a small nested scroll box
- keep status summaries internally consistent by counting only tasks in
the displayed priority state
- add English/Chinese copy and parser/rendering regression coverage

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Web parser and locale tests (59 tests)
- [x] `@zooclaw/chat-ui` tests (61 tests), typecheck, and lint
- [x] local Web + local ACS + local Engine end-to-end acceptance with a
staging account and live child Agent progress

## Companion changes

- Engine producer:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1146
- Agent Channel Service contract coverage:
https://github.com/SerendipityOneInc/agent-channel-service/pull/112
```

### PR Body

```
## Linear

Not applicable — requested without a Linear issue.

## Summary

- document the complete v2 Engine → ACS channel delivery → Web rendering design
- render delegated child work as a dedicated progress group with running, attention, completed, and elapsed states
- expand long child-task details inline in the conversation instead of inside a small nested scroll box
- keep status summaries internally consistent by counting only tasks in the displayed priority state
- add English/Chinese copy and parser/rendering regression coverage

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Web parser and locale tests (59 tests)
- [x] `@zooclaw/chat-ui` tests (61 tests), typecheck, and lint
- [x] local Web + local ACS + local Engine end-to-end acceptance with a staging account and live child Agent progress

## Companion changes

- Engine producer: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1146
- Agent Channel Service contract coverage: https://github.com/SerendipityOneInc/agent-channel-service/pull/112
```


## 备注

需要 Engine（zooclaw-engine#1146）与 Agent Channel Service（#112）配套发布后才完整生效；本仓库改动为 Web 渲染侧。
