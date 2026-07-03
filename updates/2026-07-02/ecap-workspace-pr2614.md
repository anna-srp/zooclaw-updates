---
title: "企业版登录页焕新并更名为 ZooWork"
type: "体验优化"
priority: "中"
date: "2026-07-02"
status: "待审核"
channels: ""
---
# 企业版登录页焕新并更名为 ZooWork
## 核心宣传点
企业版（business.zooclaw.ai）登录与验证码页面全面视觉升级，品牌更名为 ZooWork | BUSINESS，界面更专业精致。
## 原始内容
### [ecap-workspace PR #2614]

feat(enterprise-admin): rebrand sign-in surfaces to ZooWork and polish UI (#2614)

## Summary

Polishes and rebrands the **enterprise-admin** business sign-in surfaces
(`/login` + `/verify`) at `business.zooclaw.ai`, and rebrands
user-facing copy from **ZooClaw → ZooWork**.

Both auth screens now render through a single shared `BRAND_AUTH_SHELL`
config so they stay visually identical from one source of truth. `/join`
and the onboarding forms (which also use `AuthShell` / `OtpGrid`) are
intentionally **unchanged** — every new shell behavior is opt-in and
defaults off.

## What changed

**Visual polish (login + verify)**
- Staggered entrance animation (reuses the previously-unused
`login-reveal` keyframes), brand-red → **gray-black** input focus ring,
equal-height (48px) centered black/white primary CTA.
- Left hero now uses an editorial bronze photo (`login-hero-bg.webp`,
53KB) with a left+bottom legibility scrim so white text stays readable
over the artwork.
- Dark `#272420` page backdrop; white hero shield icon (only when a hero
photo is set).
- Form panel restructured: dropped the eyebrow + divider, sentence-case
bold field labels, and a "Talk to our team" contact line.
- All type on these surfaces is **Roboto** (scoped via a `.login-roboto`
rule + `next/font`).
- OTP underline fill is now a prop (`fillClassName`); verify passes
gray-black, `/join` keeps the default red.

**Rebrand (ZooClaw → ZooWork)**
- New white "ZOOWORK | BUSINESS" hero lockup + new favicon
(`favicon.png`).
- Page title → "ZooWork Enterprise Admin".
- Hero eyebrow/title/subtitle + "New to … Business?" + onboarding © +
Chinese catalog (`i18n-zh.ts`) updated to ZooWork.
- Hero headline reworded to "Orchestrate your entire digital workforce."
and the subtitle to a plain-language security line.

## Testing

- `pnpm exec tsc --noEmit` — pass
- `pnpm exec eslint . --max-warnings=0` (full enterprise-admin) — pass
- Verified every change via rendered computed styles in a local dev
browser (`/login` and `/verify`, EN).
- **Unit tests (vitest) were not run locally**: the local Node is
20.11.1 and vitest 4 needs ≥20.12 (`node:util.styleText`). CI (Node 24+)
runs them. No existing test assertions depend on the changed
copy/structure (checked `AuthShell`, `Brand`, `verify` tests).

## Known follow-ups (not in this PR)

- "Talk to our team" link target is a placeholder
(`https://zooclaw.ai/contact`) pending the real sales/contact URL.
- The `ZooClawWordmark` SVG logo (mobile auth wordmark, sidebar,
onboarding header, checkout) still shows **ZooClaw** — its `alt` was
intentionally left as-is since the image is unchanged; replacing it
needs a ZooWork wordmark SVG (black + white).

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>

---

## PR Description

## Summary

Polishes and rebrands the **enterprise-admin** business sign-in surfaces (`/login` + `/verify`) at `business.zooclaw.ai`, and rebrands user-facing copy from **ZooClaw → ZooWork**.

Both auth screens now render through a single shared `BRAND_AUTH_SHELL` config so they stay visually identical from one source of truth. `/join` and the onboarding forms (which also use `AuthShell` / `OtpGrid`) are intentionally **unchanged** — every new shell behavior is opt-in and defaults off.

## What changed

**Visual polish (login + verify)**
- Staggered entrance animation (reuses the previously-unused `login-reveal` keyframes), brand-red → **gray-black** input focus ring, equal-height (48px) centered black/white primary CTA.
- Left hero now uses an editorial bronze photo (`login-hero-bg.webp`, 53KB) with a left+bottom legibility scrim so white text stays readable over the artwork.
- Dark `#272420` page backdrop; white hero shield icon (only when a hero photo is set).
- Form panel restructured: dropped the eyebrow + divider, sentence-case bold field labels, and a "Talk to our team" contact line.
- All type on these surfaces is **Roboto** (scoped via a `.login-roboto` rule + `next/font`).
- OTP underline fill is now a prop (`fillClassName`); verify passes gray-black, `/join` keeps the default red.

**Rebrand (ZooClaw → ZooWork)**
- New white "ZOOWORK | BUSINESS" hero lockup + new favicon (`favicon.png`).
- Page title → "ZooWork Enterprise Admin".
- Hero eyebrow/title/subtitle + "New to … Business?" + onboarding © + Chinese catalog (`i18n-zh.ts`) updated to ZooWork.
- Hero headline reworded to "Orchestrate your entire digital workforce." and the subtitle to a plain-language security line.

## Testing

- `pnpm exec tsc --noEmit` — pass
- `pnpm exec eslint . --max-warnings=0` (full enterprise-admin) — pass
- Verified every change via rendered computed styles in a local dev browser (`/login` and `/verify`, EN).
- **Unit tests (vitest) were not run locally**: the local Node is 20.11.1 and vitest 4 needs ≥20.12 (`node:util.styleText`). CI (Node 24+) runs them. No existing test assertions depend on the changed copy/structure (checked `AuthShell`, `Brand`, `verify` tests).

## Known follow-ups (not in this PR)

- "Talk to our team" link target is a placeholder (`https://zooclaw.ai/contact`) pending the real sales/contact URL.
- The `ZooClawWordmark` SVG logo (mobile auth wordmark, sidebar, onboarding header, checkout) still shows **ZooClaw** — its `alt` was intentionally left as-is since the image is unchanged; replacing it needs a ZooWork wordmark SVG (black + white).

