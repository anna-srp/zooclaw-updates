---
title: "桌面客户端去除多出来的「幽灵」程序坞图标"
type: "Bug Fix"
priority: "中"
date: "2026-06-18"
status: "待审核"
channels: "Discord+changelog"
---
# 桌面客户端去除多出来的「幽灵」程序坞图标
## 核心宣传点
修复 macOS 桌面客户端在程序坞/Cmd-Tab 里多出一个无窗口重复图标的问题，现在桌面端只显示一个图标，更干净。
## 原始内容
fix(desktop): run Next server via LSUIElement Helper to drop the ghost Dock icon (#2520)

## Problem
The packaged macOS app shows a **second, windowless `PandaClaw` icon**
in the Dock / Cmd-Tab.

## Cause
The standalone Next server is spawned by re-executing the app's MAIN
binary (`process.execPath`) with `ELECTRON_RUN_AS_NODE`. macOS
LaunchServices registers that re-exec as a second **Foreground** app
instance of the bundle (confirmed via `lsappinfo`: a
`com.pandaclaw.desktop` entry with `!cgsConnection` = no window).

## Fix
Spawn the server via the bundled `"<App> Helper.app"` binary, which is
marked **`LSUIElement`** (no Dock presence) — verified in the helper's
Info.plist. Guarded to macOS with a fallback to `process.execPath`;
Windows/Linux are unaffected.

One file, desktop-only. Purely cosmetic — no functional/runtime change.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>

## PR Description
## Problem
The packaged macOS app shows a **second, windowless `PandaClaw` icon** in the Dock / Cmd-Tab.

## Cause
The standalone Next server is spawned by re-executing the app's MAIN binary (`process.execPath`) with `ELECTRON_RUN_AS_NODE`. macOS LaunchServices registers that re-exec as a second **Foreground** app instance of the bundle (confirmed via `lsappinfo`: a `com.pandaclaw.desktop` entry with `!cgsConnection` = no window).

## Fix
Spawn the server via the bundled `"<App> Helper.app"` binary, which is marked **`LSUIElement`** (no Dock presence) — verified in the helper's Info.plist. Guarded to macOS with a fallback to `process.execPath`; Windows/Linux are unaffected.

One file, desktop-only. Purely cosmetic — no functional/runtime change.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
