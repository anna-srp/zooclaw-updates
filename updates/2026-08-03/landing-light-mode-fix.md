---
title: "官网营销页统一浅色模式"
type: "体验优化"
priority: "低"
date: "2026-08-03"
status: "待审核"
channels: ""
---

## 核心宣传点

官网营销页面（首页、功能、定价等）统一浅色主题显示，视觉更一致；登录后的应用仍保留你的深色偏好。

## 原始内容

**Commit**: `b12770f0a67d31c6ebc5f6939e5bfa6465d1004b` — lynn Zhuang — 2026-08-03T08:19:46Z

### Commit Message

```
fix(landing): force light mode across marketing UI (#3200)

## Summary
- Force the complete public marketing route group (landing, features,
pricing, about/legal, and shared packs) to use light mode at both
pre-hydration bootstrap and React runtime.
- Preserve the user's saved theme preference so authenticated app routes
continue to honor dark mode.
- Add route-matrix unit coverage plus Playwright coverage for the
category-button hover state and the portaled template dialog.

## Root cause
The shared marketing wrapper pinned branded light tokens, but the
document could still retain the global `dark` class. The design-system
outline button's later `dark:hover` rule therefore overrode the landing
hover color, while Radix portal content rendered outside the
token-scoped wrapper. Enforcing the theme at the root provider across
every route rendered by `(marketing)` resolves both cases.

## Test plan
- [x] `bash scripts/verify-web.sh` on all changed frontend files (123
related unit tests, TypeScript, ESLint, and governance guards)
- [x] `bash scripts/verify-changed.sh`
- [x] Local Playwright landing theme scenario with a saved dark
preference, including category hover and template dialog assertions
```

### PR Body

```
## Summary
- Force the complete public marketing route group (landing, features, pricing, about/legal, and shared packs) to use light mode at both pre-hydration bootstrap and React runtime.
- Preserve the user's saved theme preference so authenticated app routes continue to honor dark mode.
- Add route-matrix unit coverage plus Playwright coverage for the category-button hover state and the portaled template dialog.

## Root cause
The shared marketing wrapper pinned branded light tokens, but the document could still retain the global `dark` class. The design-system outline button's later `dark:hover` rule therefore overrode the landing hover color, while Radix portal content rendered outside the token-scoped wrapper. Enforcing the theme at the root provider across every route rendered by `(marketing)` resolves both cases.

## Test plan
- [x] `bash scripts/verify-web.sh` on all changed frontend files (123 related unit tests, TypeScript, ESLint, and governance guards)
- [x] `bash scripts/verify-changed.sh`
- [x] Local Playwright landing theme scenario with a saved dark preference, including category hover and template dialog assertions

```
