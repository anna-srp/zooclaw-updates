---
title: "侧边栏 My Team 入口精简、Hub 图标更直观"
type: "体验优化"
priority: "低"
date: "2026-06-25"
status: "待审核"
channels: ""
---

# 侧边栏 My Team 入口精简、Hub 图标更直观

## 核心宣传点

侧边栏去掉了重复的「添加专家」加号入口，并把 AI Specialists Hub 换成更贴切的人物组图标，导航更清爽好认。

## 原始内容

### Commit Message

```
feat(sidenav): 去掉 My Team 添加专家加号并更换 AI Specialists Hub 图标 (#2601)

## What & Why

侧边栏导航的两处微调，目标是去掉冗余的「添加专家」入口并让 Hub 图标语义更贴切：

1. **去掉 `My Team` 标题旁的「添加专家」加号按钮** —— 该 `+` 按钮指向 `/agents-manager`，与下方的
**AI Specialists Hub** 导航项完全重复（同一目标路由），属于冗余入口，移除后标题行更干净。
2. **更换 AI Specialists Hub 图标** —— 由原来的「加号圆圈」(`PlusCircleIcon`) 改为
**`UserGroupIcon`**（一组人物）。加号圆圈语义偏「新建/添加」，而 Hub
实为「浏览/雇佣专家」的目的地，人物组图标更契合，也与刚移除的 `+` 入口不再视觉撞车。

## Changes

- `web/app/src/components/sidenav/SideNavAgentList.tsx`
  - 删除 `My Team` 表头右侧的加号链接 + 其 hover tooltip
  - 顺带清理仅被该块使用的导入：`PlusCircleIcon`、`LocaleLink`、`TooltipArrowDownIcon`
  - 表头容器去掉已无意义的 `justify-between`（其唯一作用是把 `+` 推到右端）
- `web/app/src/components/sidenav/build-bottom-nav-items.ts`
  - `agents-manager` 项图标 `PlusCircleIcon`（outline 别名）→ `UserGroupIcon`
- `web/app/tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx`
- 更新两条断言：表头渲染时「不再」出现添加专家按钮；collapsed 模式下表头省略（锚点从已永久消失的按钮 label 改为 `My
Team` 标题）

> 注：`nav.addSpecialists` i18n key 现已无引用，但仍存在于 10 个 locale 文件中。本 PR
未删除它，以免把 diff 扩散到 10 个语言文件；如需清理可另起小 PR。

## Verification

- `bash scripts/verify-web.sh <changed paths>` —— 全绿：CI guards ✓ / `tsc
--noEmit` ✓ / vitest（36 passed）✓ / eslint ✓
- 本地 mock 栈（`scripts/dev-mock.sh`，`ready-user` 场景）人工核验：`My Team`
表头不再有加号；AI Specialists Hub 显示为人物组图标。每个 agent 行右侧的 `+` 是「New
Task」按钮（`SideNavAgentRow`），与本次改动无关、保持原样。

## Risk

低。仅 sidenav 渲染层改动，无数据/接口/路由变更；被移除的 `+` 入口功能由现存的 AI Specialists Hub
项完整覆盖。

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR Description

## What & Why

侧边栏导航的两处微调，目标是去掉冗余的「添加专家」入口并让 Hub 图标语义更贴切：

1. **去掉 `My Team` 标题旁的「添加专家」加号按钮** —— 该 `+` 按钮指向 `/agents-manager`，与下方的 **AI Specialists Hub** 导航项完全重复（同一目标路由），属于冗余入口，移除后标题行更干净。
2. **更换 AI Specialists Hub 图标** —— 由原来的「加号圆圈」(`PlusCircleIcon`) 改为 **`UserGroupIcon`**（一组人物）。加号圆圈语义偏「新建/添加」，而 Hub 实为「浏览/雇佣专家」的目的地，人物组图标更契合，也与刚移除的 `+` 入口不再视觉撞车。

## Changes

- `web/app/src/components/sidenav/SideNavAgentList.tsx`
  - 删除 `My Team` 表头右侧的加号链接 + 其 hover tooltip
  - 顺带清理仅被该块使用的导入：`PlusCircleIcon`、`LocaleLink`、`TooltipArrowDownIcon`
  - 表头容器去掉已无意义的 `justify-between`（其唯一作用是把 `+` 推到右端）
- `web/app/src/components/sidenav/build-bottom-nav-items.ts`
  - `agents-manager` 项图标 `PlusCircleIcon`（outline 别名）→ `UserGroupIcon`
- `web/app/tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx`
  - 更新两条断言：表头渲染时「不再」出现添加专家按钮；collapsed 模式下表头省略（锚点从已永久消失的按钮 label 改为 `My Team` 标题）

> 注：`nav.addSpecialists` i18n key 现已无引用，但仍存在于 10 个 locale 文件中。本 PR 未删除它，以免把 diff 扩散到 10 个语言文件；如需清理可另起小 PR。

## Verification

- `bash scripts/verify-web.sh <changed paths>` —— 全绿：CI guards ✓ / `tsc --noEmit` ✓ / vitest（36 passed）✓ / eslint ✓
- 本地 mock 栈（`scripts/dev-mock.sh`，`ready-user` 场景）人工核验：`My Team` 表头不再有加号；AI Specialists Hub 显示为人物组图标。每个 agent 行右侧的 `+` 是「New Task」按钮（`SideNavAgentRow`），与本次改动无关、保持原样。

## Risk

低。仅 sidenav 渲染层改动，无数据/接口/路由变更；被移除的 `+` 入口功能由现存的 AI Specialists Hub 项完整覆盖。

