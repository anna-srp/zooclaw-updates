---
title: "桌面客户端窗口现在可以拖动了"
type: "体验优化"
priority: "低"
date: "2026-06-16"
status: "待审核"
channels: ""
---
# 桌面客户端窗口现在可以拖动了
## 核心宣传点
桌面客户端（Electron）窗口现在可以正常拖动移动位置，使用体验更顺手。
## 原始内容
fix(web): make the desktop app window draggable (#2477)

## Problem

The desktop (Electron) window can't be dragged to move it. The shell
creates its `BrowserWindow` with `titleBarStyle: 'hiddenInset'`
(`desktop/main/index.ts`), which hides the native title bar — so macOS
provides no draggable region. The renderer (this web app) declared no
`-webkit-app-region: drag` area anywhere, so there was nothing to grab.

## Fix

Add a thin draggable strip across the top of the content area in
`AppLayout`, rendered **only under Electron**:

- **`useIsElectron` hook** (new) — detects the desktop shell via the
preload's `window.electronAPI`; SSR-safe (false → flips after mount,
like `useIsDesktop`). In a plain browser it's always `false`, so the
strip is never rendered there → the web build is unaffected.
- **Scoped to the content area** (not full width) so it doesn't cover
the sidebar's top-left link; verified the top 32px of the content area
has no interactive elements.
- **Inline `-webkit-app-region`** — Lightning CSS strips this
non-standard property out of compiled stylesheet rules (a class-based
version had no effect at runtime), so it's set via inline style.
`AppLayout.tsx` is already in the `react/forbid-dom-props` allowlist.

## Test

Verified in the running desktop app: the strip computes
`-webkit-app-region: drag` over the content-area top (`left:260, w:585,
h:32`), and the window drags from that band while the sidebar link stays
clickable. Browser build renders no strip.

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>

---

## PR Description

## Problem

The desktop (Electron) window can't be dragged to move it. The shell creates its `BrowserWindow` with `titleBarStyle: 'hiddenInset'` (`desktop/main/index.ts`), which hides the native title bar — so macOS provides no draggable region. The renderer (this web app) declared no `-webkit-app-region: drag` area anywhere, so there was nothing to grab.

## Fix

Add a thin draggable strip across the top of the content area in `AppLayout`, rendered **only under Electron**:

- **`useIsElectron` hook** (new) — detects the desktop shell via the preload's `window.electronAPI`; SSR-safe (false → flips after mount, like `useIsDesktop`). In a plain browser it's always `false`, so the strip is never rendered there → the web build is unaffected.
- **Scoped to the content area** (not full width) so it doesn't cover the sidebar's top-left link; verified the top 32px of the content area has no interactive elements.
- **Inline `-webkit-app-region`** — Lightning CSS strips this non-standard property out of compiled stylesheet rules (a class-based version had no effect at runtime), so it's set via inline style. `AppLayout.tsx` is already in the `react/forbid-dom-props` allowlist.

## Test

Verified in the running desktop app: the strip computes `-webkit-app-region: drag` over the content-area top (`left:260, w:585, h:32`), and the window drags from that band while the sidebar link stays clickable. Browser build renders no strip.
