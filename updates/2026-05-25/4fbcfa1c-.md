---
title: "修复网站公开页面样式覆盖问题"
type: "Bug Fix"
priority: "低"
date: "2026-05-25"
status: "待审核"
channels: ""
---

# 修复网站公开页面样式覆盖问题

## 核心宣传点

修复官网页面部分样式被错误覆盖的问题，导航栏和页脚显示恢复正常

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**Commit**: 4fbcfa1c7e47babac6f76966203646d187e1f2f6  
**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T13:13:51Z  

**Commit Message**:

```
fix(web): lower marketing-root reset specificity so Tailwind utilities win (#1928)

## Why

Follow-up to #1915. Verified on staging (`ecap.gensmo.nosay.live`):
every padding/margin Tailwind utility on chrome elements rendered by
`<PublicHeader>` / `<PublicFooter>` is being silently zeroed by the
per-page reset selector `.{name}-root *` (specificity `0,1,1`) which
beats single-class utilities like `.pb-5` (`0,1,0`).

The dropdown hover-bridge (the original bug this whole effort was about
— see #1896 and the pricing-page report) actually still didn't work
after #1915. Bridge appeared to "work" only because `pb=0` / menu `mt=0`
left no gap at all, which also collapsed the intended ~20px visual
spacing between trigger and menu.

## Observations on staging /pricing (pre-fix)

| Element | className | computed padding / margin |
|---|---|---|
| header inner | `px-[61px] max-md:px-5 px-6` | `padding 0 0 0 0` |
| hamburger btn | `p-1 ...` | `padding 0 0 0 0` |
| footer | `px-20 pt-24 pb-12` | `padding 0 0 0 0` |
| footer-inner | `mx-auto px-6` | `margin 0, padding 0` |
| footer h5 | `mb-4` | `margin 0 0 0 0` |
| dropdown trigger | `group/dropdown relative -mb-5 pb-5` |
`padding-bottom 0, margin-bottom 0` |

## Fix

Wrap the reset's `.{name}-root` in `:where()`:

```diff
-.pricing-root *, .pricing-root *::before, .pricing-root *::after {
+:where(.pricing-root) *,
+:where(.pricing-root) *::before,
+:where(.pricing-root) *::after {
   margin: 0; padding: 0; box-sizing: border-box;
 }
```

`:where()` contributes `0` to selector specificity. The reset still
applies to every descendant — just at `(0,0,1)` instead of `(0,1,1)`.
Tailwind utilities at `(0,1,0)` now win the cascade; multi-class
page-body rules like `.pricing-root .plan-card` (`0,2,1`) continue to
beat the reset, so no page-body styling changes.

Same change applied to `landing.css` / `pricing.css` / `userguide.css`.

## Risk

Low. The only behavior change is that single-class utilities (Tailwind
or otherwise) used anywhere inside marketing pages now actually take
effect against the reset. Page-body subcomponents that may have written
`pb-N` / `mb-N` expecting them to work will now have them work — likely
a positive correction rather than a regression.

## Test plan

- [x] `pnpm tsc --noEmit`
- [x] `pnpm lint`
- [x] `pnpm test:unit` — 370 files / 5703 cases pass
- [ ] After staging deploy: re-run the Playwright probe that exposed the
regression; expect `padding-bottom: 20px`, `margin-bottom: -20px` on the
dropdown trigger and proper paddings on header-inner / footer / etc.
- [ ] Hover smoke on staging: Learn / Resources dropdowns stay visible
while moving from trigger into menu (the original ECAP bug)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Why

Follow-up to #1915. Verified on staging (`ecap.gensmo.nosay.live`): every padding/margin Tailwind utility on chrome elements rendered by `<PublicHeader>` / `<PublicFooter>` is being silently zeroed by the per-page reset selector `.{name}-root *` (specificity `0,1,1`) which beats single-class utilities like `.pb-5` (`0,1,0`).

The dropdown hover-bridge (the original bug this whole effort was about — see #1896 and the pricing-page report) actually still didn't work after #1915. Bridge appeared to "work" only because `pb=0` / menu `mt=0` left no gap at all, which also collapsed the intended ~20px visual spacing between trigger and menu.

## Observations on staging /pricing (pre-fix)

| Element | className | computed padding / margin |
|---|---|---|
| header inner | `px-[61px] max-md:px-5 px-6` | `padding 0 0 0 0` |
| hamburger btn | `p-1 ...` | `padding 0 0 0 0` |
| footer | `px-20 pt-24 pb-12` | `padding 0 0 0 0` |
| footer-inner | `mx-auto px-6` | `margin 0, padding 0` |
| footer h5 | `mb-4` | `margin 0 0 0 0` |
| dropdown trigger | `group/dropdown relative -mb-5 pb-5` | `padding-bottom 0, margin-bottom 0` |

## Fix

Wrap the reset's `.{name}-root` in `:where()`:

```diff
-.pricing-root *, .pricing-root *::before, .pricing-root *::after {
+:where(.pricing-root) *,
+:where(.pricing-root) *::before,
+:where(.pricing-root) *::after {
   margin: 0; padding: 0; box-sizing: border-box;
 }
```

`:where()` contributes `0` to selector specificity. The reset still applies to every descendant — just at `(0,0,1)` instead of `(0,1,1)`. Tailwind utilities at `(0,1,0)` now win the cascade; multi-class page-body rules like `.pricing-root .plan-card` (`0,2,1`) continue to beat the reset, so no page-body styling changes.

Same change applied to `landing.css` / `pricing.css` / `userguide.css`.

## Risk

Low. The only behavior change is that single-class utilities (Tailwind or otherwise) used anywhere inside marketing pages now actually take effect against the reset. Page-body subcomponents that may have written `pb-N` / `mb-N` expecting them to work will now have them work — likely a positive correction rather than a regression.

## Test plan

- [x] `pnpm tsc --noEmit`
- [x] `pnpm lint`
- [x] `pnpm test:unit` — 370 files / 5703 cases pass
- [ ] After staging deploy: re-run the Playwright probe that exposed the regression; expect `padding-bottom: 20px`, `margin-bottom: -20px` on the dropdown trigger and proper paddings on header-inner / footer / etc.
- [ ] Hover smoke on staging: Learn / Resources dropdowns stay visible while moving from trigger into menu (the original ECAP bug)

🤖 Generated with [Claude Code](https://claude.com/claude-code)
