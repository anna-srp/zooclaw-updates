---
title: "修复暗色模式刷新时闪白问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# 修复暗色模式刷新时闪白问题

## 核心宣传点

开启暗色模式后刷新页面不再先闪一下白底再变暗，分享页和关于页也同步修复，夜间使用眼睛更舒服。

## 原始内容

[3f6d03ee] fix(theme): bootstrap dark mode before hydration (#2720)

## Summary
- Add a head bootstrap script that mirrors next-themes class mode before
hydration.
- Share the ecap-theme storage key between ThemeProvider and the
bootstrap script.
- Apply the same theme-mode bootstrap to standalone /share and /about
root layouts.
- Cover dark, light, system, missing storage, storage-error, and
matchMedia-error behavior in unit tests.

## Root cause
The app dark variant depends on html.dark, but the App Router locale
layout only bootstrapped the brand theme before hydration. next-themes
persisted ecap-theme correctly, but its client provider runs from the
body, so a refresh could paint before html.dark was applied. Standalone
root layouts also need the same pre-hydration class bootstrap because
they bypass the locale layout and ThemeProvider.

## Test plan
- [x] corepack pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/_brand-bootstrap.unit.spec.ts
- [x] corepack pnpm exec tsc --noEmit
- [x] corepack pnpm exec eslint src/app/_brand-bootstrap.ts
src/app/[locale]/layout.tsx src/app/share/layout.tsx
src/app/about/layout.tsx src/components/providers/ThemeProvider.tsx
src/theme/theme-mode.ts tests/unit/app/_brand-bootstrap.unit.spec.ts
- [x] git diff --check
- [x] web governance guard scripts

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>

--- PR #2720 body ---
## Summary
- Add a head bootstrap script that mirrors next-themes class mode before hydration.
- Share the ecap-theme storage key between ThemeProvider and the bootstrap script.
- Apply the same theme-mode bootstrap to standalone /share and /about root layouts.
- Cover dark, light, system, missing storage, storage-error, and matchMedia-error behavior in unit tests.

## Root cause
The app dark variant depends on html.dark, but the App Router locale layout only bootstrapped the brand theme before hydration. next-themes persisted ecap-theme correctly, but its client provider runs from the body, so a refresh could paint before html.dark was applied. Standalone root layouts also need the same pre-hydration class bootstrap because they bypass the locale layout and ThemeProvider.

## Test plan
- [x] corepack pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/_brand-bootstrap.unit.spec.ts
- [x] corepack pnpm exec tsc --noEmit
- [x] corepack pnpm exec eslint src/app/_brand-bootstrap.ts src/app/[locale]/layout.tsx src/app/share/layout.tsx src/app/about/layout.tsx src/components/providers/ThemeProvider.tsx src/theme/theme-mode.ts tests/unit/app/_brand-bootstrap.unit.spec.ts
- [x] git diff --check
- [x] web governance guard scripts

