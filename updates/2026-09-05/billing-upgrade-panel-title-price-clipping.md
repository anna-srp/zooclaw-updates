---
title: "修复：升级套餐面板标题偏心、月付价格末尾的 0 被裁掉"
type: "Bug Fix"
priority: "低"
date: "2026-09-05"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：升级套餐面板标题偏心、月付价格末尾的 0 被裁掉

## 核心宣传点

「Upgrade your plan」升级面板上两处一眼可见的排版毛病修掉了。

一是标题没居中，偏了 26 像素，手机上更糟——标题会直接钻到右上角关闭按钮底下。根因是关闭按钮用了 `float-right`：浮动元素的外边距盒不允许与 flex 容器的边框盒重叠，浏览器于是把整个标题栏按浮动占位（36px 按钮 + 16px 边距）缩窄了一截，标题自然就居中在一个被削过的区域里。现在关闭按钮改成和其他弹窗一致的写法——一行零高度的 `sticky` 容器承载 `absolute top-4 right-4` 的按钮，同时在标题栏左右两侧各预留这颗按钮 52px 的位置（`px-14`），标题在任何视口宽度下都真正居中，也不会再和按钮打架。

二是月付价格滚动动画时，末尾那个 `0` 会被「/ month」后缀挤掉一半。之前每个滚动数字被固定分配 `w-[0.6em]` 的宽度槽，宽字形放不下就被裁。现在每个数字改成按自身字形自适应（`inline-flex … items-end`）；而保证数字滚动时不左右抖动的 `tabular-nums` 被移到真正依赖它的 `AnimatedPrice` 组件上。

## 原始内容

### fix(billing): centre subscription panel title and stop clipping price digits (#3637)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `833c51a125b954354827acf76ce789d7f6710e09`
- PR: #3637
- 作者: Nemo Feng
- 日期: 2026-09-05T01:04:16Z

### Commit Message

```
fix(billing): centre subscription panel title and stop clipping price digits (#3637)

## Summary
- Un-float the close button of the "Upgrade your plan" panel (a
zero-height `sticky` row holding an `absolute top-4 right-4` button,
matching the other modals) and reserve the button's 52px footprint on
both sides of the header (`px-14`), so the title is centred on every
viewport and never runs under the button on phones.
- Let each rolling price digit shrink-wrap its glyph (`inline-flex …
items-end`) instead of a fixed `w-[0.6em]` slot, so the trailing `0` of
monthly prices is no longer clipped against the `/ month` suffix.
`tabular-nums` moves onto `AnimatedPrice`, the component that relies on
it to keep digits from shifting while they roll.

## Root cause
- **Title 26px off-centre.** The close button was `float-right`. A flex
container's border box may not overlap a float's margin box, so the
browser narrowed the header by the float's footprint (36px button + 16px
margin = 52px) and centred the `h2` inside the narrowed box. Measured
against the production CSS bundle: header 1046px wide in a 1098px box,
title centre offset −26px. The float also acted as an accidental gutter,
which is why the header padding must grow when the float goes away: with
`px-6` the full-width title collides with the button on viewports up to
~412px.
- **Trailing digit clipped.** `RollingDigit` slots were `w-[0.6em]`
(19.19px at the 32px price size) with `overflow-hidden`, while the price
font (Inter 600, tabular figures) advances 20.53px per digit, so 1.34px
of every digit's right edge was cut off. Monthly prices ($20 / $100 /
$200) end in `0` right against the suffix, where the clip is visible;
yearly per-month prices ($17 / $84 / $167) hid it.

## Test plan
- [x] `TZ=UTC bash scripts/verify-web.sh
web/app/src/components/billing/SubscriptionPanel.tsx
web/app/src/components/billing/PlanCard.tsx` — governance guards, `tsc`,
vitest (4 billing suites, 142 tests), eslint all green. (`TZ=UTC` only
because the devcontainer runs in America/Los_Angeles, where three
pre-existing `switch-cycle` tests with a `Date.UTC(2026, 7, 15)` fixture
render "August 14"; CI runs in UTC and is green on main at the base
commit. Untouched here; follow-up: pin `TZ` in the vitest config.)
- [x] Playwright measurement of the exact committed markup against the
production CSS bundle and real fonts (Libre Baskerville title, Inter
price): title centre offset 0px (was −26px) at 1280 / 412 / 390 / 360 /
320px viewports, close button pinned 17px from the top-right corner
before and after scrolling, no title/button overlap for "Upgrade your
plan", "Manage your plan", "Subscription under review"; price digit clip
0px (was 1.34px), digit-to-suffix gap 4px, digit baseline and top
position unchanged
- [ ] Staging after deploy: open the panel, toggle Monthly / Yearly,
check the title and the `$20` / `$100` / `$200` digits on desktop and a
phone-width viewport

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01SyroT8ta8nvKdNvrhFQNir

---------

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
```

### PR Body

```
## Summary
- Un-float the close button of the "Upgrade your plan" panel (a zero-height `sticky` row holding an `absolute top-4 right-4` button, matching the other modals) and reserve the button's 52px footprint on both sides of the header (`px-14`), so the title is centred on every viewport and never runs under the button on phones.
- Let each rolling price digit shrink-wrap its glyph (`inline-flex … items-end`) instead of a fixed `w-[0.6em]` slot, so the trailing `0` of monthly prices is no longer clipped against the `/ month` suffix. `tabular-nums` moves onto `AnimatedPrice`, the component that relies on it to keep digits from shifting while they roll.

## Root cause
- **Title 26px off-centre.** The close button was `float-right`. A flex container's border box may not overlap a float's margin box, so the browser narrowed the header by the float's footprint (36px button + 16px margin = 52px) and centred the `h2` inside the narrowed box. Measured against the production CSS bundle: header 1046px wide in a 1098px box, title centre offset −26px. The float also acted as an accidental gutter, which is why the header padding must grow when the float goes away: with `px-6` the full-width title collides with the button on viewports up to ~412px.
- **Trailing digit clipped.** `RollingDigit` slots were `w-[0.6em]` (19.19px at the 32px price size) with `overflow-hidden`, while the price font (Inter 600, tabular figures) advances 20.53px per digit, so 1.34px of every digit's right edge was cut off. Monthly prices ($20 / $100 / $200) end in `0` right against the suffix, where the clip is visible; yearly per-month prices ($17 / $84 / $167) hid it.

## Test plan
- [x] `TZ=UTC bash scripts/verify-web.sh web/app/src/components/billing/SubscriptionPanel.tsx web/app/src/components/billing/PlanCard.tsx` — governance guards, `tsc`, vitest (4 billing suites, 142 tests), eslint all green. (`TZ=UTC` only because the devcontainer runs in America/Los_Angeles, where three pre-existing `switch-cycle` tests with a `Date.UTC(2026, 7, 15)` fixture render "August 14"; CI runs in UTC and is green on main at the base commit. Untouched here; follow-up: pin `TZ` in the vitest config.)
- [x] Playwright measurement of the exact committed markup against the production CSS bundle and real fonts (Libre Baskerville title, Inter price): title centre offset 0px (was −26px) at 1280 / 412 / 390 / 360 / 320px viewports, close button pinned 17px from the top-right corner before and after scrolling, no title/button overlap for "Upgrade your plan", "Manage your plan", "Subscription under review"; price digit clip 0px (was 1.34px), digit-to-suffix gap 4px, digit baseline and top position unchanged
- [ ] Staging after deploy: open the panel, toggle Monthly / Yearly, check the title and the `$20` / `$100` / `$200` digits on desktop and a phone-width viewport

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01SyroT8ta8nvKdNvrhFQNir

```
