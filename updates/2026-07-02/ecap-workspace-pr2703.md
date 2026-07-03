---
title: "BossClaw 页面启用全新藏青金爪 App 图标"
type: "体验优化"
priority: "低"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# BossClaw 页面启用全新藏青金爪 App 图标
## 核心宣传点
BossClaw 活动页的应用图标和网页小图标统一换成全新的藏青底金色爪印品牌标识，视觉更统一醒目。
## 原始内容
### [ecap-workspace PR #2703]

feat(bossclaw): use the new navy ZooClaw app icon for tiles & favicon (#2703)

## What

Refresh the bossclaw campaign's **square app icon + favicon** to the new
**navy gold-claw ZooClaw mark**, replacing the old gold-chip +
white-claw composite and the gold app-icon favicon.

## Changes

- **New asset** `public/bossclaw/appicon.png` (192×192, ~12 KB,
pngquant-optimized) — one shared brand mark for every square-icon
surface.
- **On-page tiles** (Preloader loading mark, Done-card avatar, WeChat
QR-center badge) now point at `appicon.png` and render **full-bleed**
(`object-fit: cover` + `border-radius: inherit`); their chips drop the
now-covered gold gradient and the dead flex-centering.
- **Favicon + apple-touch icon** (`page.tsx` metadata) → `appicon.png`.
- **Removed** the two superseded assets (`claw-appicon-white.png`,
`favicon.png`); no references remain.

## Scope

Frontend-only, and **scoped strictly to the app icon / favicon** — no
greeting, flow, copy, or backend changes. (This is the standalone logo
half extracted from the earlier combined PR.)

## Testing

- `bash scripts/verify-web.sh 'web/app/src/app/[locale]/bossclaw'` —
guards + vitest + eslint green; the bossclaw sources are tsc-clean.
- Rendered at mobile size (previously verified): the navy tile shows
correctly in the preloader and done-card, gold claw legible against the
dark page.

> Note: a local `tsc` run flags a pre-existing, unrelated error in
`src/components/public/PublicHeader.tsx` (a node_modules resolution
quirk after a branch switch; `usePathname` is `string`). It does not
reproduce in CI — current main passes `web-quality / lint-and-typecheck`
— and this PR does not touch that file.

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>

---

## PR Description

## What

Refresh the bossclaw campaign's **square app icon + favicon** to the new **navy gold-claw ZooClaw mark**, replacing the old gold-chip + white-claw composite and the gold app-icon favicon.

## Changes

- **New asset** `public/bossclaw/appicon.png` (192×192, ~12 KB, pngquant-optimized) — one shared brand mark for every square-icon surface.
- **On-page tiles** (Preloader loading mark, Done-card avatar, WeChat QR-center badge) now point at `appicon.png` and render **full-bleed** (`object-fit: cover` + `border-radius: inherit`); their chips drop the now-covered gold gradient and the dead flex-centering.
- **Favicon + apple-touch icon** (`page.tsx` metadata) → `appicon.png`.
- **Removed** the two superseded assets (`claw-appicon-white.png`, `favicon.png`); no references remain.

## Scope

Frontend-only, and **scoped strictly to the app icon / favicon** — no greeting, flow, copy, or backend changes. (This is the standalone logo half extracted from the earlier combined PR.)

## Testing

- `bash scripts/verify-web.sh 'web/app/src/app/[locale]/bossclaw'` — guards + vitest + eslint green; the bossclaw sources are tsc-clean.
- Rendered at mobile size (previously verified): the navy tile shows correctly in the preloader and done-card, gold claw legible against the dark page.

> Note: a local `tsc` run flags a pre-existing, unrelated error in `src/components/public/PublicHeader.tsx` (a node_modules resolution quirk after a branch switch; `usePathname` is `string`). It does not reproduce in CI — current main passes `web-quality / lint-and-typecheck` — and this PR does not touch that file.

