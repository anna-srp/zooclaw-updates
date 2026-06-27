---
title: "侧边栏「会话历史」入口移到 Agent 列表底部"
type: "体验优化"
priority: "低"
date: "2026-06-26"
status: "待审核"
channels: ""
---
# 侧边栏「会话历史」入口移到 Agent 列表底部

## 核心宣传点
展开某个 Agent 时，历史会话会先显示，「会话历史」入口移到了列表最底部，更符合「先看会话、再找入口」的习惯。

## 原始内容
```
feat(sidenav): 把 Session History 移到 agent 展开列表底部 (#2612)

## What & Why

调整侧边栏中 agent 展开后「Session History」入口的排序位置。

此前 agent 行展开时，**Session History** 入口渲染在会话列表的**最上方**，下方才是该 agent
的历史会话条目。本 PR 把 Session History 移到列表**最底部**（位于所有历史会话之下），符合「先看会话、再看入口」的预期。

## Changes

- `web/app/src/components/sidenav/SideNavAgentSessions.tsx`
  - 把 `Session History` 按钮从列表顶部移动到 `sessions.map(...)` 之后（列表底部）
- 纯 JSX 顺序调整，无逻辑/props/active-route 检测变更 —— `isSessionHistoryActive` /
`aria-current` 高亮逻辑基于路由而非 DOM 位置，迁移后在新位置仍正确高亮
-
`web/app/tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx`
- 新增排序守卫测试：断言 Session History 是展开面板内的**最后一个**条目（位于所有 session 行之后）。原有测试均为
order-agnostic（`getByTestId` / `getByText`），不会捕捉顺序回归，故补此用例锁定意图

## Verification

- `bash scripts/verify-web.sh
src/components/sidenav/SideNavAgentSessions.tsx` —— 全绿：CI guards ✓ /
`tsc --noEmit` ✓ / vitest（16 passed，含新增排序用例）✓ / eslint ✓
- 本地 mock 栈（`scripts/dev-mock.sh`，`ready-user` 场景）人工核验：展开 Assistant
后，Session History 显示在所有历史会话条目之下；无历史会话的 agent（如 Founder IP Studio）则
Session History 单独位于底部

## Risk

低。仅 sidenav 展开面板的渲染顺序调整，无数据/接口/路由/交互行为变更。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR description

## What & Why

调整侧边栏中 agent 展开后「Session History」入口的排序位置。

此前 agent 行展开时，**Session History** 入口渲染在会话列表的**最上方**，下方才是该 agent 的历史会话条目。本 PR 把 Session History 移到列表**最底部**（位于所有历史会话之下），符合「先看会话、再看入口」的预期。

## Changes

- `web/app/src/components/sidenav/SideNavAgentSessions.tsx`
  - 把 `Session History` 按钮从列表顶部移动到 `sessions.map(...)` 之后（列表底部）
  - 纯 JSX 顺序调整，无逻辑/props/active-route 检测变更 —— `isSessionHistoryActive` / `aria-current` 高亮逻辑基于路由而非 DOM 位置，迁移后在新位置仍正确高亮
- `web/app/tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx`
  - 新增排序守卫测试：断言 Session History 是展开面板内的**最后一个**条目（位于所有 session 行之后）。原有测试均为 order-agnostic（`getByTestId` / `getByText`），不会捕捉顺序回归，故补此用例锁定意图

## Verification

- `bash scripts/verify-web.sh src/components/sidenav/SideNavAgentSessions.tsx` —— 全绿：CI guards ✓ / `tsc --noEmit` ✓ / vitest（16 passed，含新增排序用例）✓ / eslint ✓
- 本地 mock 栈（`scripts/dev-mock.sh`，`ready-user` 场景）人工核验：展开 Assistant 后，Session History 显示在所有历史会话条目之下；无历史会话的 agent（如 Founder IP Studio）则 Session History 单独位于底部

## Risk

低。仅 sidenav 展开面板的渲染顺序调整，无数据/接口/路由/交互行为变更。

