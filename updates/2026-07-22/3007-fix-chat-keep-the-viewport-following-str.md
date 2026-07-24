---
title: 流式回复时视口自动跟随，长回答不再需手动滚动
type: Bug Fix
priority: B
date: 2026-07-22
status: 已合并待发版
pr: 3007
author: chris-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/3007
---

流式回复时视口自动跟随，长回答不再需手动滚动

## 问题

`/chat` 流式输出时对话窗口**从头到尾不自动下滚**，底部「↓」按钮也不出现。

## 先排除的两条

**不是布局问题。** viewport 就是唯一滚动容器，实测 `scrollHeight 87557 / clientHeight 444 / scrollTop 87113`（正好在底部），从它到 `<html>` 每一层祖先（含 `<main class="flex-1 overflow-y-auto">`）都不滚动。

**「↓ 按钮不出现」不构成证据。** 那个按钮只在 `handleScroll` 里重算显隐，而 `handleScroll` 只由 scroll 事件触发；内容在下方增长不产生 scroll 事件，所以它在流式期间**结构上就不可能出现**。这是一个独立 bug，不是主因的线索——我差点把它当决定性证据用。

## 根因：`isAtBottom` 被布局假象锁死

assistant-ui 的流式跟随只有一条路径，在 `useThreadViewportAutoScroll` 里：

```js
else if (autoScroll && store.isAtBottom) scrollToBottom("instant")
```

而 `isAtBottom` **只在 scroll 事件的 handler 里重算**，且
