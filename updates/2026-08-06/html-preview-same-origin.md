---
title: "修复交互式 HTML 预览白屏/半屏问题"
type: "Bug Fix"
priority: "高"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

生成的网页类作品（如小游戏）如果用到浏览器本地存储，之前预览会报错渲染不全；现已恢复正常，预览效果与直接打开网页一致。

## 原始内容

**fix(web): restore same-origin HTML previews (#3262)**

- sha: `0cd643f14d74c417edb13ded0a6d360d895a2ff9`
- PR: #3262

```
fix(web): restore same-origin HTML previews (#3262)

## What changed

- restore `allow-same-origin` on the HTML artifact preview iframe;
- update the renderer contract test to require the restored sandbox
capability.

## Why

HTML artifacts that use browser storage can fail during initialization
inside the current sandbox. For example, a generated 2048 game reads
`localStorage` for its high score before building the board; without
`allow-same-origin`, the browser throws a `SecurityError` and leaves the
preview partially rendered.

## Impact

Interactive HTML artifacts can access browser storage again and render
consistently with opening the HTML directly.

## Security tradeoff

This intentionally restores same-origin capability to script-enabled
artifact HTML. In particular, private workspace files rendered through
blob URLs need a follow-up design that moves HTML execution to an
isolated, cookie-less preview origin before the sandbox can be tightened
again safely.

## Validation

- `pnpm exec tsc --noEmit`
- `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/components/artifacts/renderers/HtmlRenderer.unit.spec.tsx` (4
tests passed)
- targeted ESLint
- pre-push changed-surface verification
```

**PR Body:**

## What changed

- restore `allow-same-origin` on the HTML artifact preview iframe;
- update the renderer contract test to require the restored sandbox capability.

## Why

HTML artifacts that use browser storage can fail during initialization inside the current sandbox. For example, a generated 2048 game reads `localStorage` for its high score before building the board; without `allow-same-origin`, the browser throws a `SecurityError` and leaves the preview partially rendered.

## Impact

Interactive HTML artifacts can access browser storage again and render consistently with opening the HTML directly.

## Security tradeoff

This intentionally restores same-origin capability to script-enabled artifact HTML. In particular, private workspace files rendered through blob URLs need a follow-up design that moves HTML execution to an isolated, cookie-less preview origin before the sandbox can be tightened again safely.

## Validation

- `pnpm exec tsc --noEmit`
- `pnpm exec vitest run --config ./vitest.config.mts tests/unit/components/artifacts/renderers/HtmlRenderer.unit.spec.tsx` (4 tests passed)
- targeted ESLint
- pre-push changed-surface verification

