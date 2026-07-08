---
title: "Agent Builder 测试模式布局优化"
type: "体验优化"
priority: "中"
date: "2026-07-07"
status: "待审核"
channels: ""
---

# Agent Builder 测试模式布局优化

## 核心宣传点

Agent Builder 测试面板独立展示、可随时关闭重开，打包测试后直接进入测试模式，构建 Agent 更顺手。

## 原始内容

```
style(agent-builder): 优化测试模式布局 (#2755)

## 变更内容

- 优化 Agent Builder 的 test mode 布局：右侧测试面板独立展示，标题与左侧 header 对齐，并支持关闭/重新打开。
- 点击 `Package & Test` 后立即进入 test mode 展示测试面板，同时保留失败回滚。
- 将顶部状态标签调整为更小的状态 tag 样式，避免看起来像按钮。
- 统一右上角图标 tooltip 样式，并补充 `Test panel` 文案。
- 完善本地 mock 预览数据，方便在本地直接查看 Agent Builder 测试模式页面。

## 验证

- `node --check web/app/scripts/mock-backend.mjs`
- `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/agent-builder-client.unit.spec.tsx`
- `bash scripts/verify-web.sh ...`
- push 前的 `verify-changed` 检查已通过

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>

---

## PR Description

## 变更内容

- 优化 Agent Builder 的 test mode 布局：右侧测试面板独立展示，标题与左侧 header 对齐，并支持关闭/重新打开。
- 点击 `Package & Test` 后立即进入 test mode 展示测试面板，同时保留失败回滚。
- 将顶部状态标签调整为更小的状态 tag 样式，避免看起来像按钮。
- 统一右上角图标 tooltip 样式，并补充 `Test panel` 文案。
- 完善本地 mock 预览数据，方便在本地直接查看 Agent Builder 测试模式页面。

## 验证

- `node --check web/app/scripts/mock-backend.mjs`
- `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/agent-builder-client.unit.spec.tsx`
- `bash scripts/verify-web.sh ...`
- push 前的 `verify-changed` 检查已通过

```
