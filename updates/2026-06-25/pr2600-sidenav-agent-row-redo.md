---
title: "侧边栏 Agent 行交互重做：多开展开 + 一键新任务"
type: "体验优化"
priority: "中"
date: "2026-06-25"
status: "待审核"
channels: ""
---

# 侧边栏 Agent 行交互重做：多开展开 + 一键新任务

## 核心宣传点

侧边栏的 Agent 列表支持同时展开多个，每行常驻「＋」可直接对该 Agent 发起新任务，找会话、开任务都更顺手。

## 原始内容

### Commit Message

```
feat(sidenav): agent 行多开手风琴与新任务入口交互重做 (#2600)

## 背景

侧边栏 MY TEAM 的 agent 行交互重做，覆盖「折叠/展开」与「发起新任务」两块，参考设计稿对齐。

## 改动

### 1. 多开手风琴（`SideNav.tsx` + `expanded-agents.ts`）
展开态由单值 `expandedAgentId: string | null` 改为 `Set<string>`，可**同时展开多个
agent**。集合只在手动点击时增删、在导航进某 agent 时**叠加**（保留其他已展开），收起完全靠手动。抽出纯函数
`toggleExpandedAgent` / `withExpandedAgent` 并单测。

### 2. agent 行重做（`SideNavAgentRow.tsx`）
- **去掉 hover 背景块**；agent 名字只有两态：默认 `text-muted-foreground`、hover
`text-foreground`（无选中态）。
- **箭头移到名字正后面**，且**仅在 hover 名字时出现**（group 收窄到名字按钮，所以
hover「＋」不会再触发箭头）；默认朝下（`ChevronDownIcon`），展开时 `rotate-180` 朝上。
- 每行**右侧常驻「＋」新任务按钮**，深链 `/new-chat?agent_id=X`，hover 出现
tooltip（右对齐向左展开，避免被侧栏 `overflow` 裁断）。

### 3. 移除面板内「＋ New chat」（`SideNavAgentSessions.tsx`）
新任务入口已上移到行上的「＋」，展开面板只保留 Session History + 历史会话。

### 4. 适配（`SideNavAgentList.tsx` / `useAgentScrollOverlay.ts`）
列表 prop 改 `expandedAgentIds: Set`、`isExpanded` 用 `.has()`；滚动遮罩重测依赖从单个 id
改为集合派生 key。

## 验证

- `bash scripts/verify-web.sh`：`tsc` + `eslint` + 单元测试全绿。
- 全程 TDD：`expanded-agents` 多开 toggle/叠加、列表多开渲染、行上「＋」深链、面板移除 New chat
均有用例；hook 改名同步更新。
- 本地 mock 栈逐项实测（computed style）：箭头方向（收起 ↓ / 展开 ↑）、箭头与名字变黑仅 hover
名字时成立、hover「＋」只出 tooltip 不出箭头、tooltip 不再截断、多开可同时展开。

## 影响范围

- 仅前端 `web/app` 侧边栏 agent 行，纯 UI/交互改动，无接口变更。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Description

## 背景

侧边栏 MY TEAM 的 agent 行交互重做，覆盖「折叠/展开」与「发起新任务」两块，参考设计稿对齐。

## 改动

### 1. 多开手风琴（`SideNav.tsx` + `expanded-agents.ts`）
展开态由单值 `expandedAgentId: string | null` 改为 `Set<string>`，可**同时展开多个 agent**。集合只在手动点击时增删、在导航进某 agent 时**叠加**（保留其他已展开），收起完全靠手动。抽出纯函数 `toggleExpandedAgent` / `withExpandedAgent` 并单测。

### 2. agent 行重做（`SideNavAgentRow.tsx`）
- **去掉 hover 背景块**；agent 名字只有两态：默认 `text-muted-foreground`、hover `text-foreground`（无选中态）。
- **箭头移到名字正后面**，且**仅在 hover 名字时出现**（group 收窄到名字按钮，所以 hover「＋」不会再触发箭头）；默认朝下（`ChevronDownIcon`），展开时 `rotate-180` 朝上。
- 每行**右侧常驻「＋」新任务按钮**，深链 `/new-chat?agent_id=X`，hover 出现 tooltip（右对齐向左展开，避免被侧栏 `overflow` 裁断）。

### 3. 移除面板内「＋ New chat」（`SideNavAgentSessions.tsx`）
新任务入口已上移到行上的「＋」，展开面板只保留 Session History + 历史会话。

### 4. 适配（`SideNavAgentList.tsx` / `useAgentScrollOverlay.ts`）
列表 prop 改 `expandedAgentIds: Set`、`isExpanded` 用 `.has()`；滚动遮罩重测依赖从单个 id 改为集合派生 key。

## 验证

- `bash scripts/verify-web.sh`：`tsc` + `eslint` + 单元测试全绿。
- 全程 TDD：`expanded-agents` 多开 toggle/叠加、列表多开渲染、行上「＋」深链、面板移除 New chat 均有用例；hook 改名同步更新。
- 本地 mock 栈逐项实测（computed style）：箭头方向（收起 ↓ / 展开 ↑）、箭头与名字变黑仅 hover 名字时成立、hover「＋」只出 tooltip 不出箭头、tooltip 不再截断、多开可同时展开。

## 影响范围

- 仅前端 `web/app` 侧边栏 agent 行，纯 UI/交互改动，无接口变更。

