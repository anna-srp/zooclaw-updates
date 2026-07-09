---
title: "聊天连接状态下拉菜单更清晰易读"
type: "体验优化"
priority: "低"
date: "2026-07-08"
status: "待审核"
channels: ""
---

# 聊天连接状态下拉菜单更清晰易读

## 核心宣传点

聊天顶部的连接状态下拉菜单换上了更清晰的磨砂弹层，文字和背景对比更明显，一眼就能看清当前连接状态。

## 原始内容

```
fix(app): improve chat status dropdown readability (#2772)

## Summary
- Make the chat header connection dropdown use a readable frosted
popover surface.
- Add unit coverage that pins the dropdown background, blur, and
foreground color contract.

## Root cause
The connection dropdown used a plain opaque-token class without the
frosted surface treatment needed on liquid-glass chat pages. When the
panel overlapped chat content, background text could visually bleed
through and make dropdown text hard to read.

## Test plan
- [x] `bash scripts/verify-local.sh --web-static
web/app/src/components/ClawConnectionStatus.tsx
web/app/tests/unit/components/ClawPageHeader-extras.unit.spec.tsx`
- [x] Local mock preview at `http://localhost:3002/chat`; captured the
opened dropdown and confirmed `bg-popover/95` computes to 95% light
popover background with `blur(24px) saturate(1.5)`.

![Uploading screenshot-20260708-170224.png…]()

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>

---

**PR Description:**

## Summary
- Make the chat header connection dropdown use a readable frosted popover surface.
- Add unit coverage that pins the dropdown background, blur, and foreground color contract.

## Root cause
The connection dropdown used a plain opaque-token class without the frosted surface treatment needed on liquid-glass chat pages. When the panel overlapped chat content, background text could visually bleed through and make dropdown text hard to read.

## Test plan
- [x] `bash scripts/verify-local.sh --web-static web/app/src/components/ClawConnectionStatus.tsx web/app/tests/unit/components/ClawPageHeader-extras.unit.spec.tsx`
- [x] Local mock preview at `http://localhost:3002/chat`; captured the opened dropdown and confirmed `bg-popover/95` computes to 95% light popover background with `blur(24px) saturate(1.5)`.

![Uploading screenshot-20260708-170224.png…]()


```
