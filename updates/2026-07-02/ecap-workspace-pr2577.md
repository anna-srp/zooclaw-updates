---
title: "官网首页焕新：浅色主题 + 全新首屏设计"
type: "体验优化"
priority: "中"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# 官网首页焕新：浅色主题 + 全新首屏设计
## 核心宣传点
官网落地页整体改版为清爽的浅色主题，首屏与导航栏重新设计，页面加载更轻快、观感更现代。
## 原始内容
### [ecap-workspace PR #2577]

style(landing): aquavoice-style light theme + hero/header refresh (#2577)

## What

Landing-page visual refresh toward an Aqua-style (aquavoice.com) **light
theme**, plus several hero/header polish items requested along the way.

### Hero (first screen — kept dark on purpose)
- Replaced the background **video** with a background **image**
(`object-fit: cover` + `object-position: center 65%` so the round-table
subject survives cropping on any width).
- Removed the embedded demo video.
- Moved the copy/buttons into the upper area so they never overlap the
people in the lower part of the image.

### Header / nav
- Full-bleed, fixed liquid-glass nav (5% white glass + blur + saturate +
top highlight), no drop shadow.
- In compact/scrolled state it switches to a **solid dark bar** so the
white logo + white nav text stay readable over the now-light page body.
- New logo asset.

### Light theme (the rest of the page)
- Flipped the `--landing-*` token palette in `landing.css` from the old
dark scheme to an Aqua-style light scheme (near-white bg, dark-charcoal
text, white cards with thin borders, soft blue accent on the comparison
table).
- **Hero** and the bottom **CTA** re-declare the dark token values in
their own scope, so they stay dark as intentional contrast sections
(matching aquavoice's dark interludes).
- Fixed hardcoded-white surfaces that would otherwise vanish on a light
background: integration chips, comparison-table highlight column +
dividers, security-card icon backgrounds; mobile sticky CTA keeps its
dark scope.

## Scope
Only the public marketing landing surface (`landing/` + shared
`PublicHeader`). Token changes to `--marketing-header-*` are shared by
the other marketing pages (pricing / userguide) by design — header stays
visually in sync.

## Testing
- Verified locally across widths (1000 / 1440 / 1512 / 2200 / 2560 /
3000 and mobile 390) — full-width with no letterboxing, hero locked
dark, all sections legible in light mode, compact header dark bar
readable over light content.
- `tsc` + `eslint` pass via the pre-push changed-surface gate.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: shana-srp <undefined@users.noreply.github.com>
Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>

---

## PR Description

## What

Landing-page visual refresh toward an Aqua-style (aquavoice.com) **light theme**, plus several hero/header polish items requested along the way.

### Hero (first screen — kept dark on purpose)
- Replaced the background **video** with a background **image** (`object-fit: cover` + `object-position: center 65%` so the round-table subject survives cropping on any width).
- Removed the embedded demo video.
- Moved the copy/buttons into the upper area so they never overlap the people in the lower part of the image.

### Header / nav
- Full-bleed, fixed liquid-glass nav (5% white glass + blur + saturate + top highlight), no drop shadow.
- In compact/scrolled state it switches to a **solid dark bar** so the white logo + white nav text stay readable over the now-light page body.
- New logo asset.

### Light theme (the rest of the page)
- Flipped the `--landing-*` token palette in `landing.css` from the old dark scheme to an Aqua-style light scheme (near-white bg, dark-charcoal text, white cards with thin borders, soft blue accent on the comparison table).
- **Hero** and the bottom **CTA** re-declare the dark token values in their own scope, so they stay dark as intentional contrast sections (matching aquavoice's dark interludes).
- Fixed hardcoded-white surfaces that would otherwise vanish on a light background: integration chips, comparison-table highlight column + dividers, security-card icon backgrounds; mobile sticky CTA keeps its dark scope.

## Scope
Only the public marketing landing surface (`landing/` + shared `PublicHeader`). Token changes to `--marketing-header-*` are shared by the other marketing pages (pricing / userguide) by design — header stays visually in sync.

## Testing
- Verified locally across widths (1000 / 1440 / 1512 / 2200 / 2560 / 3000 and mobile 390) — full-width with no letterboxing, hero locked dark, all sections legible in light mode, compact header dark bar readable over light content.
- `tsc` + `eslint` pass via the pre-push changed-surface gate.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

