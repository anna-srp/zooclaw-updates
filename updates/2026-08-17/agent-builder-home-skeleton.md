---
title: "Agent Builder 首页加载动画更顺眼"
type: 体验优化
priority: 低
date: 2026-08-17
status: "待审核"
channels: ""
---

## 核心宣传点

Agent Builder 首页在加载 Agent 列表时，不再显示一块生硬的灰色方块，而是按真实列表布局呈现三行占位骨架，带有柔和的流光动效，看起来更接近内容真正加载出来的样子；开启系统「减少动态效果」时会自动关闭动画。

## 原始内容

**Commit**: `719cdd79` — fix(agent-builder): add animated home loading skeleton (#3396)
**作者**: lynn Zhuang ｜ **日期**: 2026-08-17T07:18:25Z

```
fix(agent-builder): add animated home loading skeleton (#3396)

## Summary
- Replace the bordered pulse wireframe on the Agent Builder home page with a responsive three-row skeleton aligned to the agent list.
- Remove loading-only table headers and divider lines, and add staggered 1.4-second shimmer motion with a reduced-motion fallback.
- Fix the shared shimmer utility so its animated background position is no longer pinned by an important background shorthand.

## Root cause
The loading state used a generic bordered pulse block instead of mirroring the eventual list layout. The initial shimmer implementation also used an important `background` shorthand, which implicitly fixed `background-position` and prevented the running keyframes from producing visible motion.

## Test plan
- [x] `bash scripts/verify-local.sh --web-static 'src/app/globals.css' 'src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderHome.tsx' 'tests/unit/app/agent-builder-production-home.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] Local `ready-user` mock with the projects request delayed: confirmed three skeleton rows, no loading table/header chrome, and changing shimmer background positions.
- [x] Verified `prefers-reduced-motion` still disables the skeleton animation.
```
