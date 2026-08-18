---
title: "Agent Builder 创建弹窗改用统一输入框，并可直接选模型"
type: 体验优化
priority: 中
date: 2026-08-17
status: "待审核"
channels: ""
---

## 核心宣传点

在 Agent Builder 里新建 Agent 的弹窗变得和正常聊天一样顺手：换成与聊天页一致的输入框，标题直接问「你想创建什么样的 Agent」，并提供 5 个专门为 Agent Builder 写的示例提示词，点标题就自动填入完整提示。模型选择也换成了标准的模型选择器（带正确的厂商图标和名称），创建前就能选好模型，即使不发消息只建空项目，选择的模型也会被保存。

## 原始内容

**Commit**: `21d032c5` — fix(agent-builder): refine create dialog composer (#3395)
**作者**: lynn Zhuang ｜ **日期**: 2026-08-17T11:58:59Z

```
fix(agent-builder): refine create dialog composer (#3395)

## Summary
- update the Agent Builder Create dialog heading to ask what kind of agent the user wants to create
- replace the shared Landing examples with five Agent Builder-specific sample prompts; clicking a short title inserts its full prompt
- reuse the shared `UnifiedChatComposer` used by chat sessions instead of maintaining a separate Create-dialog composer
- replace the clipped model avatar/readout with the shared model picker and preserve the catalog logo and display name for Builder model aliases
- limit the picker to Builder-authorized models when that list is available
- apply the selected model before the first Builder turn; blank creation saves the model without sending a message
- keep legacy pending-creation recovery records compatible

## Root cause
The Create dialog had its own partial composer implementation and rendered the model through a circular avatar, so its behavior and presentation had drifted from chat sessions. Builder model aliases also did not resolve to their matching catalog presentation metadata.

The Create dialog also reused Landing prompt keys, which prevented its examples from changing independently.

## Test plan
- [x] selected frontend verification: TypeScript, 9 test files / 180 tests, and ESLint passed
- [x] pre-push changed-surface verification passed
- [x] local mock preview verified the shared composer, intact provider logo, and working model dropdown
```
