---
title: "修复快速重复点击登录弹窗时的闪退问题"
type: "Bug Fix"
priority: "低"
date: "2026-05-13"
status: "待审核"
channels: "Discord + changelog"
---

# 修复快速重复点击登录弹窗时的闪退问题

## 核心宣传点

登录弹窗的小毛病修好了：快速关闭再打开时，弹窗不会在刚出现时就莫名消失了。

## 原始内容

**来源**: ecap-workspace PR #1601 | SHA: c39f59e5

**Commit Message**:
```
fix(web): prevent login modal reopen race (#1601)

Fixes a race where rapidly reopening the login modal (close → open within 300ms)
caused a stale exit timer to unmount the freshly-opened modal.

- Track the in-flight transition timer in a useRef so each isOpen flip cancels
  the prior handle before scheduling the next.
- Use a single setTimeout-based primitive for both the enter (0ms, kicks the CSS
  transition) and exit (300ms, gates shouldRender). requestAnimationFrame +
  setTimeout were initially used together, but their id-spaces aren't unified
  across all environments — cancelling an rAF id with cancelAnimationFrame can
  silently no-op while the callback still fires.
```

**PR #1601 Description**:
```
Summary: Fixes a race where rapidly reopening the login modal (close → open within 300ms)
caused a stale exit timer to unmount the freshly-opened modal.

Fix: Track the in-flight transition timer in a useRef so each isOpen flip cancels
the prior handle before scheduling the next.

Test plan:
- pnpm lint — passes
- npx tsc --noEmit — passes
- pnpm test:unit — 4522 passed, 1 todo. New regression test covers the race.
```
