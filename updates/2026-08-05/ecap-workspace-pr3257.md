---
title: "修复弹窗遮罩只盖住半个页面"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 修复弹窗遮罩只盖住半个页面

## 核心宣传点

聊天、发布、设置、账单等弹窗现在都能正确铺满整个屏幕，礼物兑换动画也不再出现空白图标。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`447c285de36416c8153a4fe95d41eeea12739d2b`
- 作者：lynn Zhuang
- 日期：2026-08-05T10:20:53Z
- PR：#3257

### Commit Message

```
fix(web): render modal overlays at viewport root (#3257)

## Summary
- add a hydration-safe `ViewportPortal` that renders full-screen
overlays under `document.body`
- migrate chat, publish, settings, preview, billing, and drag-capture
overlays to the shared viewport-root boundary
- keep the redeem gift artwork visible from the first animation frame
while preserving the drop, lid, and confetti motion
- add portal-boundary and gift-animation regression coverage

## Root cause
Several overlays were rendered inside application panel subtrees.
Ancestors that establish a containing block can constrain `position:
fixed`, so the backdrop covered only the right panel instead of the
viewport. Rendering these layers through a shared body portal restores
viewport-relative geometry consistently.

The redeem gift SVG also started its drop animation with `opacity: 0`,
which left an empty icon slot when the modal was opened or captured on
the first frame.

## Test plan
- [x] `bash scripts/verify-web.sh` — TypeScript, 599 test files / 8171
passing tests, and ESLint
- [x] `bash scripts/verify-changed.sh`
- [x] focused UserMenu, MobileAppModal, and AnimatedGiftDropIcon unit
tests
- [x] local Playwright validation at 1600x900: overlay parent is `BODY`,
overlay bounds match the viewport, and the gift artwork is visible at
animation frame zero
```

### PR Body

## Summary
- add a hydration-safe `ViewportPortal` that renders full-screen overlays under `document.body`
- migrate chat, publish, settings, preview, billing, and drag-capture overlays to the shared viewport-root boundary
- keep the redeem gift artwork visible from the first animation frame while preserving the drop, lid, and confetti motion
- add portal-boundary and gift-animation regression coverage

## Root cause
Several overlays were rendered inside application panel subtrees. Ancestors that establish a containing block can constrain `position: fixed`, so the backdrop covered only the right panel instead of the viewport. Rendering these layers through a shared body portal restores viewport-relative geometry consistently.

The redeem gift SVG also started its drop animation with `opacity: 0`, which left an empty icon slot when the modal was opened or captured on the first frame.

## Test plan
- [x] `bash scripts/verify-web.sh` — TypeScript, 599 test files / 8171 passing tests, and ESLint
- [x] `bash scripts/verify-changed.sh`
- [x] focused UserMenu, MobileAppModal, and AnimatedGiftDropIcon unit tests
- [x] local Playwright validation at 1600x900: overlay parent is `BODY`, overlay bounds match the viewport, and the gift artwork is visible at animation frame zero

