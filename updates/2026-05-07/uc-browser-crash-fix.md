---
title: "修复 UC 浏览器打开落地页崩溃问题"
type: "Bug Fix"
priority: "中"
date: "2026-05-07"
status: "待审核"
channels: ""
---
# 修复 UC 浏览器打开落地页崩溃问题

## 核心宣传点
使用 UC 浏览器访问 ZooClaw 落地页时不再崩溃白屏，所有主流手机浏览器均可正常访问。

## 原始内容

### Commit Message
```
fix(web): defensive matchMedia wrapper to prevent UC Browser crash (#1569)
```

### PR Description
## Summary
- UC Browser 17.x patches `window.matchMedia` with internal telemetry that calls `JSON.stringify` on objects containing DOM element references. On React-hydrated pages, this hits circular `__reactFiber` refs and throws `TypeError: Converting circular structure to JSON`, crashing the landing page via the route-error boundary.
- Adds an inline `<script>` in `<head>` that wraps `matchMedia` with try-catch, returning a spec-compliant `MediaQueryList` stub on failure (defaults to light mode — acceptable degradation)
- Filters `"circular structure" + "reactFiber"` errors in Sentry `beforeSend` as secondary noise reduction

**Sentry issue:** https://serendipity-one-inc.sentry.io/issues/7462625509/
