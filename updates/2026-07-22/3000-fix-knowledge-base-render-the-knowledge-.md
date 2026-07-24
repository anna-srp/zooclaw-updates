---
title: 知识库改为设置内嵌页，切换不再整页刷新
type: Bug Fix
priority: B
date: 2026-07-22
status: 已合并待发版
pr: 3000
author: kevin-f-srp
url: https://github.com/SerendipityOneInc/ecap-workspace/pull/3000
---

知识库改为设置内嵌页，切换不再整页刷新

## 问题分类
- [x] 前端 (web/)
- [ ] 后端 (services/claw-interface/)
- [ ] 基础设施/CI
- [ ] 其他

## 问题描述

Closes #2987

知识库虽然出现在 settings 的 tab 列表里，但行为和其他 tab 完全不同：

1. 页面布局不一致
2. 点击其他 tab 不刷新页面，点知识库**整页重新加载**
3. URL pattern 不对（`/knowledge-base` vs `/claw-settings?tab=…`）

## 根因

三个现象是同一个原因。知识库的 tab 配置带了 `href`，而 `SettingsLayout` 对带 `href` 的 tab 渲染成**纯 `<a>` 而非 `next/link`**：

```ts
{ id: 'knowledge-base', …, href: '/knowledge-base' },
```

所以点击触发的是真实浏览器导航——整个 document 重载、provider 栈重新挂载、react-query 缓存重置、Mattermost socket 状态丢失。其余 tab 只改变 `?tab=` query，pathname 不变，App Router 视为 soft navigation，`ClawSettingsC
