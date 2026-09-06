# SerendipityOneInc/ecap-workspace — commits 2026-09-05

## fix(billing): centre subscription panel title and stop clipping price digits (#3637)

- **SHA**: `833c51a125b954354827acf76ce789d7f6710e09`
- **作者**: Nemo Feng
- **日期**: 2026-09-05T01:04:16Z
- **PR**: #3637

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


---

## fix(landing): show redirect progress for returning users (#3643)

- **SHA**: `ec0781d6bf9a21e2d5c7636e2048fe501e25967e`
- **作者**: Nemo Feng
- **日期**: 2026-09-05T01:03:54Z
- **PR**: #3643

### Commit Message

```
fix(landing): show redirect progress for returning users (#3643)

## Summary

- expose the landing auth redirect's real pending state and share it
with the marketing header
- replace the header and first hero Get Started labels with localized
Redirecting feedback and staggered, reduced-motion-safe dots
- disable both affected CTAs during the handoff while leaving lower-page
CTAs unchanged

## Root cause

The landing redirect waited for account-session validation before
navigating, but its state was discarded by the page orchestrator. The
header and hero therefore kept rendering interactive Get Started buttons
throughout that wait with no indication that navigation was already in
progress.

## Test plan

- [x] `TZ=UTC bash scripts/verify-web.sh` — 689 files, 9,456 tests
passed; TypeScript, ESLint, and governance guards passed
- [x] `TZ=UTC bash scripts/verify-changed.sh`
- [x] focused redirect-hook, landing-client, header, marketing-chrome,
and homepage component tests — 93 passed
- [ ] browser auth-flow smoke test — local checkout does not have the
full auth runtime environment; pending and completed handoffs are
covered by hook and component tests
```

### PR Body

## Summary

- expose the landing auth redirect's real pending state and share it with the marketing header
- replace the header and first hero Get Started labels with localized Redirecting feedback and staggered, reduced-motion-safe dots
- disable both affected CTAs during the handoff while leaving lower-page CTAs unchanged

## Root cause

The landing redirect waited for account-session validation before navigating, but its state was discarded by the page orchestrator. The header and hero therefore kept rendering interactive Get Started buttons throughout that wait with no indication that navigation was already in progress.

## Test plan

- [x] `TZ=UTC bash scripts/verify-web.sh` — 689 files, 9,456 tests passed; TypeScript, ESLint, and governance guards passed
- [x] `TZ=UTC bash scripts/verify-changed.sh`
- [x] focused redirect-hook, landing-client, header, marketing-chrome, and homepage component tests — 93 passed
- [ ] browser auth-flow smoke test — local checkout does not have the full auth runtime environment; pending and completed handoffs are covered by hook and component tests


---

## fix(web): delegate vertical pack runtime selection (#3658)

- **SHA**: `36f3f818b53bc33aa9f8573848deb7ac0c6f3fa8`
- **作者**: bill-srp
- **日期**: 2026-09-05T00:55:18Z
- **PR**: #3658

### Commit Message

```
fix(web): delegate vertical pack runtime selection (#3658)

## Summary
- Remove frontend OpenClaw init, onboarding status, and computer
readiness gates from vertical pack installation.
- Retain the frontend `pack_id` preflight dedupe across the unified
Agent list, without filtering by computer or runtime.
- Delegate runtime selection and final idempotency enforcement to the
existing backend install endpoint.
- Refresh the unified Agent list after the backend accepts the package
install.

## Root cause
The frontend inferred v1/v2 mode from onboarding state and required a
ready v1 computer before it would call the vertical pack install
endpoint. Migrated users can retain a stopped v1 computer record,
causing the frontend to suppress the install request even though the
backend considers the account eligible for Engine.

## Test plan
- [x] Run targeted web verification (governance guards, TypeScript,
Vitest, ESLint).
- [x] Verify 8 related test files and 114 tests pass.
- [x] Verify the changed-surface pre-push gate passes.
```

### PR Body

## Summary
- Remove frontend OpenClaw init, onboarding status, and computer readiness gates from vertical pack installation.
- Retain the frontend `pack_id` preflight dedupe across the unified Agent list, without filtering by computer or runtime.
- Delegate runtime selection and final idempotency enforcement to the existing backend install endpoint.
- Refresh the unified Agent list after the backend accepts the package install.

## Root cause
The frontend inferred v1/v2 mode from onboarding state and required a ready v1 computer before it would call the vertical pack install endpoint. Migrated users can retain a stopped v1 computer record, causing the frontend to suppress the install request even though the backend considers the account eligible for Engine.

## Test plan
- [x] Run targeted web verification (governance guards, TypeScript, Vitest, ESLint).
- [x] Verify 8 related test files and 114 tests pass.
- [x] Verify the changed-surface pre-push gate passes.


---
