---
title: "修复 ZooClaw 桌面版启动白屏问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-20"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了 ZooClaw 桌面客户端启动时出现白屏、无法进入的问题；同时桌面版现在会记住并可在新建对话时设置全局工作目录（CWD），使用更顺手。

### 原始内容

**Commit message:**

```
fix: stabilize ZooClaw desktop runtime and CWD UI (#2952)

## Summary
- flatten staged pnpm dependencies and assert critical Next.js runtime
modules resolve
- persist and migrate the desktop global CWD, and expose the localized
CWD control on new chat
- keep the latest main UI while applying desktop-only ZooClaw logo
assets

## Root cause fixed
The production DMG from zooclaw-desktop v0.1.2 started with a white
screen because the packaged Next.js server could not resolve
`styled-jsx/package.json`. The flattening fix makes that dependency
top-level and fails staging when required runtime packages are
unavailable.

## Verification
- production CI run:
https://github.com/SerendipityOneInc/zooclaw-desktop/actions/runs/29723308516
- macOS and Windows packaging passed
- packaged Next.js runtime smoke gate passed
- Apple Silicon DMG installed locally
- Electron CDP verified a non-empty rendered page (78 body children),
title `ZooClaw — Your Proactive Agent Team`, and no startup exception

Supersedes #2913, whose branch conflicts with current main and would
restore deleted web components.
```

**PR body:**

## Summary
- flatten staged pnpm dependencies and assert critical Next.js runtime modules resolve
- persist and migrate the desktop global CWD, and expose the localized CWD control on new chat
- keep the latest main UI while applying desktop-only ZooClaw logo assets

## Root cause fixed
The production DMG from zooclaw-desktop v0.1.2 started with a white screen because the packaged Next.js server could not resolve `styled-jsx/package.json`. The flattening fix makes that dependency top-level and fails staging when required runtime packages are unavailable.

## Verification
- production CI run: https://github.com/SerendipityOneInc/zooclaw-desktop/actions/runs/29723308516
- macOS and Windows packaging passed
- packaged Next.js runtime smoke gate passed
- Apple Silicon DMG installed locally
- Electron CDP verified a non-empty rendered page (78 body children), title `ZooClaw — Your Proactive Agent Team`, and no startup exception

Supersedes #2913, whose branch conflicts with current main and would restore deleted web components.
