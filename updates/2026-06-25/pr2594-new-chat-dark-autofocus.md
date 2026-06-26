---
title: "新任务页暗色模式适配 + 输入框自动聚焦"
type: "体验优化"
priority: "低"
date: "2026-06-25"
status: "待审核"
channels: ""
---

# 新任务页暗色模式适配 + 输入框自动聚焦

## 核心宣传点

新任务页在暗色模式下的 Agent 选中态更协调，进入页面后输入框自动聚焦，打开即可直接开始输入。

## 原始内容

### Commit Message

```
fix(new-chat): 暗色 agent 选中态适配与新任务输入框自动聚焦 (#2594)

## 背景 / 问题

新任务页（`/new-chat`）有两处体验问题：

1. **暗色模式下「选择 agent」选中态没适配**：暗色玻璃主题下，选中的 agent chip 仍是浅色白底 +
暗红字，和暗色界面格格不入。
2. **进入新任务后输入框未自动聚焦**：点击侧边栏「New Task」进入新任务页后，需要再次点击输入框才能开始输入。

## 改动

### 1. 暗色 agent 选中态适配（`AgentSelector.tsx`）
为选中 chip 的 active 分支补齐 `glass-dark:` 覆盖：`bg-red-500/15`（暗红底）+
`text-red-400`（亮红字）+ `border-red-500/70`（红描边）。

> 根因：active 分支此前只有 `glass:`（浅色玻璃）样式，而 `glass:` 选择器（`.liquid-glass-root
&`）在暗色玻璃（`.dark .liquid-glass-root`）下同样命中，导致白底泄漏到暗色模式。inactive 分支早已有
`glass-dark:` 覆盖，这次只是让 active 走同一套机制对齐。

### 2. 新任务输入框自动聚焦（`NewChatClient.tsx`）
用 `ref` + `useEffect`（以 URL 的 `agent_id` 为依赖）替代仅在挂载时生效的
`autoFocus`，覆盖全部进入路径：

- 顶部「New Task」从任意页进入 → 挂载即聚焦；
- 侧边栏按 agent 的「新任务」深链到 `/new-chat?agent_id=X`：当已处于 `/new-chat`
时属于**同路由切换**、组件不重新挂载，旧的 `autoFocus` 不会再次触发；以 `agent_id` 为 key
后，每次切换都会重新聚焦输入框。

### 3. 单元测试（`NewChatClient.unit.spec.tsx`）
新增两条用例：挂载即聚焦、按 agent 切换深链时重新聚焦。

## 验证

- 本地 `bash scripts/verify-web.sh`：`tsc` + `eslint` + 单元测试全绿（32 项）。
- 本地 mock 栈实测：暗色模式选中 chip 为暗红底（非白底）；侧边栏 agent「新任务」切换后，输入框自动聚焦、可直接输入。

## 影响范围

- 仅前端 `web/app` 新任务页（`/new-chat`），纯 UI/交互改动，无接口变更。
- 「选择 agent」模块在 agent 数 ≤ 1 时本就隐藏（既有逻辑，未改动）。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Description

## 背景 / 问题

新任务页（`/new-chat`）有两处体验问题：

1. **暗色模式下「选择 agent」选中态没适配**：暗色玻璃主题下，选中的 agent chip 仍是浅色白底 + 暗红字，和暗色界面格格不入。
2. **进入新任务后输入框未自动聚焦**：点击侧边栏「New Task」进入新任务页后，需要再次点击输入框才能开始输入。

## 改动

### 1. 暗色 agent 选中态适配（`AgentSelector.tsx`）
为选中 chip 的 active 分支补齐 `glass-dark:` 覆盖：`bg-red-500/15`（暗红底）+ `text-red-400`（亮红字）+ `border-red-500/70`（红描边）。

> 根因：active 分支此前只有 `glass:`（浅色玻璃）样式，而 `glass:` 选择器（`.liquid-glass-root &`）在暗色玻璃（`.dark .liquid-glass-root`）下同样命中，导致白底泄漏到暗色模式。inactive 分支早已有 `glass-dark:` 覆盖，这次只是让 active 走同一套机制对齐。

### 2. 新任务输入框自动聚焦（`NewChatClient.tsx`）
用 `ref` + `useEffect`（以 URL 的 `agent_id` 为依赖）替代仅在挂载时生效的 `autoFocus`，覆盖全部进入路径：

- 顶部「New Task」从任意页进入 → 挂载即聚焦；
- 侧边栏按 agent 的「新任务」深链到 `/new-chat?agent_id=X`：当已处于 `/new-chat` 时属于**同路由切换**、组件不重新挂载，旧的 `autoFocus` 不会再次触发；以 `agent_id` 为 key 后，每次切换都会重新聚焦输入框。

### 3. 单元测试（`NewChatClient.unit.spec.tsx`）
新增两条用例：挂载即聚焦、按 agent 切换深链时重新聚焦。

## 验证

- 本地 `bash scripts/verify-web.sh`：`tsc` + `eslint` + 单元测试全绿（32 项）。
- 本地 mock 栈实测：暗色模式选中 chip 为暗红底（非白底）；侧边栏 agent「新任务」切换后，输入框自动聚焦、可直接输入。

## 影响范围

- 仅前端 `web/app` 新任务页（`/new-chat`），纯 UI/交互改动，无接口变更。
- 「选择 agent」模块在 agent 数 ≤ 1 时本就隐藏（既有逻辑，未改动）。

