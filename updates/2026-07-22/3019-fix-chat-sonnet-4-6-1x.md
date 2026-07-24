---
title: Sonnet 4.6 费用倍率修正为 1x，模型菜单支持滚动限高
type: Bug Fix
priority: B
date: 2026-07-22
status: 已合并待发版
pr: 3019
author: lynn-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/3019
---

Sonnet 4.6 费用倍率修正为 1x，模型菜单支持滚动限高

## 变更概述
- 保持 Sonnet 4.6 为输入框默认模型，并将其费用倍率从 `2.5x` 修正为 `1x`。
- 为共享组件 `@zooclaw/chat-ui` 的模型选择菜单增加自适应最大高度：空间充足时最多显示 10 行模型，空间不足时服从 Radix 提供的视口可用高度。
- 模型数量超过可见范围后，在菜单内部显示纵向滚动，并补充设计说明与实施计划。

## 问题原因
webapp 的模型展示元数据把默认模型 Sonnet 4.6 标记成了 `2.5x`。与此同时，共享模型选择器原先使用 `overflow-visible` 且没有最大高度限制，模型列表较长时会超出屏幕可用范围，无法在菜单内滚动查看更多模型。

## 实现说明
- 默认模型和倍率等业务展示数据继续由 webapp 适配层维护。
- dropdown 的高度、滚动和交互样式由 `@zooclaw/chat-ui` 统一维护。
- 菜单最大高度使用 `min(20.5rem, var(--radix-dropdown-menu-content-available-height))`，即“10 行模型加菜单内边距”和“当前视口可用高度”中的较小值。

## 测试计划
- [x] `bash scripts/verify-changed.sh`
- [x] 针对模型展示配置运行 `bash scripts/
