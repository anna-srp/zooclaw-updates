---
title: 模型选择器详情面板交互与样式优化
type: Bug Fix
priority: B
date: 2026-07-22
status: 已合并待发版
pr: 3012
author: lynn-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/3012
---

模型选择器详情面板交互与样式优化

## 概要
- 让模型选择器详情面板与输入框二级菜单使用一致的视觉语言
- 将带箭头的 Tooltip 替换为非交互式 HoverCard 侧边面板
- 保留模型选项原有的鼠标与键盘选择语义

## 改动范围
用户可见的改动仅涉及 `@zooclaw/chat-ui` 中的模型选择器。本 PR 没有修改 webapp 业务逻辑、聊天消息渲染，也没有修改向组件传递模型列表和选择回调的 composer adapter。

最终改动包含 6 个文件：
- `@zooclaw/chat-ui`：ModelPicker 实现及其回归测试
- `@zooclaw/design-system`：共享 HoverCard、DropdownMenu 基础组件及其测试

## 交互与行为
- 将模型详情面板固定在当前悬停或聚焦选项的右侧，并与选项顶部对齐
- 鼠标可以从模型选项移动到详情面板，不会导致面板立即关闭
- 模型选项继续使用标准 `menuitemradio` 和 Radix 原生 `onSelect` 选择路径
- 支持鼠标点击、Enter 和 Space 键选择模型
- 静态模型详情使用 `role="note"` 和 `aria-describedby`，不再包含 Tooltip 箭头或错误的 submenu 语义
- 根 dropdown 关闭时同步清理模型详情状态

## Des
