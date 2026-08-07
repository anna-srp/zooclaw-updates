---
title: "修复模型显示为「不可用」及 Agent 列表超出屏幕"
type: "Bug Fix"
priority: "中"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

当前工作区模型读取失败时不再把整个模型列表显示成不可用，而是回退显示默认模型；Agent 数量多时下拉框也不会再超出屏幕，可独立滚动。

## 原始内容

**fix(chat): 恢复模型默认回退并限制 Agent 下拉框高度 (#3281)**

- sha: `eb60a91b299ab45e164e1dc52265a3f213652b43`
- PR: #3281

```
fix(chat): 恢复模型默认回退并限制 Agent 下拉框高度 (#3281)

## 摘要
- 当前工作区模型读取失败时，回退显示模型目录中的默认模型，同时保留“无法切换模型”的只读原因。
- 分离模型目录错误与当前模型控制器错误，确保 New Task 和现有聊天会话仍可浏览模型列表。
- 限制 Agent 选择器的高度不超过可用视口，并为较长的 Agent 列表启用独立滚动。

## 根因
统一输入框此前会把“当前模型读取失败”传递成模型选择器的“模型目录错误”。即使模型目录已经成功加载，默认模型也会被 `Models
unavailable` 替代。与此同时，Agent 选择器使用了 `overflow-hidden`，却没有设置最大高度，导致 Agent
较多时下拉框会延伸到浏览器视口之外。

## 测试计划
- [x] `bash scripts/verify-web.sh
web/app/src/components/chat/unified-chat-composer/UnifiedChatComposer.tsx
web/app/tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx`
- [x] `pnpm --filter @zooclaw/chat-ui exec tsc --noEmit`
- [x] `pnpm --filter @zooclaw/chat-ui exec vitest run
src/__tests__/agent-picker.test.tsx`
- [x] `pnpm --filter @zooclaw/chat-ui exec eslint
src/composer/AgentPicker.tsx src/__tests__/agent-picker.test.tsx
--max-warnings=0`
- [x] `bash scripts/verify-changed.sh`
- [x] 本地可视化验证 New Task、聊天会话模型菜单，以及长 Agent 列表的滚动效果。
```

**PR Body:**

## 摘要
- 当前工作区模型读取失败时，回退显示模型目录中的默认模型，同时保留“无法切换模型”的只读原因。
- 分离模型目录错误与当前模型控制器错误，确保 New Task 和现有聊天会话仍可浏览模型列表。
- 限制 Agent 选择器的高度不超过可用视口，并为较长的 Agent 列表启用独立滚动。

## 根因
统一输入框此前会把“当前模型读取失败”传递成模型选择器的“模型目录错误”。即使模型目录已经成功加载，默认模型也会被 `Models unavailable` 替代。与此同时，Agent 选择器使用了 `overflow-hidden`，却没有设置最大高度，导致 Agent 较多时下拉框会延伸到浏览器视口之外。

## 测试计划
- [x] `bash scripts/verify-web.sh web/app/src/components/chat/unified-chat-composer/UnifiedChatComposer.tsx web/app/tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx`
- [x] `pnpm --filter @zooclaw/chat-ui exec tsc --noEmit`
- [x] `pnpm --filter @zooclaw/chat-ui exec vitest run src/__tests__/agent-picker.test.tsx`
- [x] `pnpm --filter @zooclaw/chat-ui exec eslint src/composer/AgentPicker.tsx src/__tests__/agent-picker.test.tsx --max-warnings=0`
- [x] `bash scripts/verify-changed.sh`
- [x] 本地可视化验证 New Task、聊天会话模型菜单，以及长 Agent 列表的滚动效果。

