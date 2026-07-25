---
title: "优化：阿拉伯语页面正确从右到左显示"
type: "Bug Fix"
priority: "中"
date: "2026-07-24"
status: "待审核"
channels: ""
---

## 核心宣传点

为阿拉伯语用户修复了页面方向问题：阿拉伯语首页及各路由现已正确采用从右到左（RTL）的文档方向，并修正了移动端菜单被裁切的显示问题，阿语用户体验更自然。

## 原始内容

**Commit**: `70ede4125c` — Mori-srp — 2026-07-24T09:58:10Z

### Commit Message

```
fix(web): add Arabic RTL document direction (#3060)

## What changed

- Add one locale-direction source of truth: Arabic uses `rtl`; the other
9 supported locales use `ltr`.
- Output the matching `dir` attribute from the shared `[locale]` layout,
so Arabic homepage and locale routes receive document-level RTL
semantics in server HTML.
- Change the homepage specialist menu anchor from physical `left-0` to
logical `start-0`. This preserves LTR placement and keeps the menu
inside the viewport in RTL.
- Add helper, layout-wiring, 10-locale direction, and English/Arabic
mobile menu geometry regression coverage.

## Why

Production `/ar` already had Arabic content, an independent URL,
canonical, hreflang, and localized metadata, but the document did not
declare RTL and the browser computed the page direction as LTR. During
local mobile Smoke, enabling document RTL exposed a real specialist-menu
regression: the 280px menu ended at `x=463.39` in a 390px viewport and
was clipped.

After the logical-inset fix, the Arabic mobile menu is fully visible at
`left=45 / right=325 / width=280` with no horizontal page overflow.

## Scope

This PR is intentionally limited to 6 production/test files and 147
changed lines. It does not change Arabic copy, metadata, canonical,
hreflang, sitemap, robots, crawler policy, authentication, or backend
behavior.

## Validation

- `web` `pnpm run lint:ci`: passed, 0 errors (309 existing W5 dependency
warnings remain informational).
- Relevant Vitest: 3 files, 57/57 passed after the latest `origin/main`
merge.
- Target ESLint and E2E spec ESLint: passed.
- Clean-source `verify-web --tsc-only`: passed.
- Next.js 15.5.19 production build: passed, 304/304 static pages
generated.
- Raw HTML: `/ar` and `/ar/features` output `lang="ar" dir="rtl"`; the
other 9 homepage locales output their language plus `dir="ltr"`.
- Arabic homepage raw HTML retains 1 H1, 1 main, 1 canonical, 11
alternate links, and 1 visible JSON-LD script.
- Desktop browser Smoke: HTML/body compute RTL; H1, input,
header/footer, language switch, model menu, specialist menu, and mixed
Arabic/English input were checked; no horizontal overflow or broken
images.
- Language switch Smoke: `ar → zh → ar` updated URL, `lang`, `dir`, and
H1 correctly.
- 390×844 browser Smoke: no page overflow; the specialist menu fits
completely after the fix.
- PR size gate: 147/3000 lines.
- Final read-only review: no P0/P1/P2 findings.

## Known validation boundary

A normal local push runs TypeScript against build-generated
`.next/types` and is blocked by the existing
`web/app/src/app/api/download/route.ts` illegal Route Handler helper
export (`isAllowedUrl`). This branch has no diff in that file.
Clean-source TypeScript and the production build both pass, so the
branch was pushed with `SKIP_VERIFY=1`; the PR size gate still ran and
passed. GitHub CI remains the required gate.

The new Playwright geometry spec is committed but could not launch
locally because this machine lacks Playwright 1.59.1's Chromium
headless-shell. The equivalent Arabic geometry was verified in the Codex
in-app browser; PR CI should be treated as the first automated execution
of that spec.

No GSC writes, real login, or real task submission were performed.
```

### PR Body

## What changed

- Add one locale-direction source of truth: Arabic uses `rtl`; the other 9 supported locales use `ltr`.
- Output the matching `dir` attribute from the shared `[locale]` layout, so Arabic homepage and locale routes receive document-level RTL semantics in server HTML.
- Change the homepage specialist menu anchor from physical `left-0` to logical `start-0`. This preserves LTR placement and keeps the menu inside the viewport in RTL.
- Add helper, layout-wiring, 10-locale direction, and English/Arabic mobile menu geometry regression coverage.

## Why

Production `/ar` already had Arabic content, an independent URL, canonical, hreflang, and localized metadata, but the document did not declare RTL and the browser computed the page direction as LTR. During local mobile Smoke, enabling document RTL exposed a real specialist-menu regression: the 280px menu ended at `x=463.39` in a 390px viewport and was clipped.

After the logical-inset fix, the Arabic mobile menu is fully visible at `left=45 / right=325 / width=280` with no horizontal page overflow.

## Scope

This PR is intentionally limited to 6 production/test files and 147 changed lines. It does not change Arabic copy, metadata, canonical, hreflang, sitemap, robots, crawler policy, authentication, or backend behavior.

## Validation

- `web` `pnpm run lint:ci`: passed, 0 errors (309 existing W5 dependency warnings remain informational).
- Relevant Vitest: 3 files, 57/57 passed after the latest `origin/main` merge.
- Target ESLint and E2E spec ESLint: passed.
- Clean-source `verify-web --tsc-only`: passed.
- Next.js 15.5.19 production build: passed, 304/304 static pages generated.
- Raw HTML: `/ar` and `/ar/features` output `lang="ar" dir="rtl"`; the other 9 homepage locales output their language plus `dir="ltr"`.
- Arabic homepage raw HTML retains 1 H1, 1 main, 1 canonical, 11 alternate links, and 1 visible JSON-LD script.
- Desktop browser Smoke: HTML/body compute RTL; H1, input, header/footer, language switch, model menu, specialist menu, and mixed Arabic/English input were checked; no horizontal overflow or broken images.
- Language switch Smoke: `ar → zh → ar` updated URL, `lang`, `dir`, and H1 correctly.
- 390×844 browser Smoke: no page overflow; the specialist menu fits completely after the fix.
- PR size gate: 147/3000 lines.
- Final read-only review: no P0/P1/P2 findings.

## Known validation boundary

A normal local push runs TypeScript against build-generated `.next/types` and is blocked by the existing `web/app/src/app/api/download/route.ts` illegal Route Handler helper export (`isAllowedUrl`). This branch has no diff in that file. Clean-source TypeScript and the production build both pass, so the branch was pushed with `SKIP_VERIFY=1`; the PR size gate still ran and passed. GitHub CI remains the required gate.

The new Playwright geometry spec is committed but could not launch locally because this machine lacks Playwright 1.59.1's Chromium headless-shell. The equivalent Arabic geometry was verified in the Codex in-app browser; PR CI should be treated as the first automated execution of that spec.

No GSC writes, real login, or real task submission were performed.

