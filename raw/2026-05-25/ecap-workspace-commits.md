# SerendipityOneInc/ecap-workspace - 2026-05-25

共 27 条 commits

## 80031811 - feat(billing): support Antom subscription trials (#1932)

**作者**: kaka-srp  
**日期**: 2026-05-25T14:50:50Z  
**SHA**: 80031811dfa6eff2023079ba3db136600766e8fc

**完整 Commit Message**:

```
feat(billing): support Antom subscription trials (#1932)

## Linear

https://linear.app/srpone/issue/ECA-817/support-antom-subscription-trials

## Summary
- Add Antom Subscription Payment trial support aligned with Stripe:
Starter-only, 7 days, 1000 trial credits, monthly/yearly support, and no
local grace after trial expiry.
- Harden Antom subscription owner handling for cancel/renew, stale
webhook idempotency, create-subscription failure cleanup, and
providerless pending order visibility.
- Improve billing invoice activity labels for deferred entitlement and
trial subscription rows.

## Test plan
- [x] cd services/claw-interface && ruff check .
- [x] cd services/claw-interface && pnpm dlx pyright app tests
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_orders_trial_logic.py tests/unit/test_antom_routes.py
tests/unit/test_antom_client.py tests/unit/test_antom_handlers.py
tests/unit/test_subscription_cron.py tests/unit/test_orders_repo.py -q
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] cd web && pnpm --filter @zooclaw/web-app exec tsc --noEmit
- [ ] pnpm --dir web run tsc (workspace script fails before TypeScript
with pnpm Unknown option: --if-present; package tsc above passes)
- [ ] full backend pytest coverage run was interrupted per request after
reaching 100%; before interruption it had already surfaced unrelated
failures outside billing/opened PR scope

## Size override
- Required because this PR couples Antom trial support with billing
state-machine fixes, production data repair notes, and focused
regression tests for Stripe/Antom parity. Splitting would leave the
trial behavior and cancel/renew correctness partially validated across
PRs.
```

**PR Description**:

## Linear
https://linear.app/srpone/issue/ECA-817/support-antom-subscription-trials

## Summary
- Add Antom Subscription Payment trial support aligned with Stripe: Starter-only, 7 days, 1000 trial credits, monthly/yearly support, and no local grace after trial expiry.
- Harden Antom subscription owner handling for cancel/renew, stale webhook idempotency, create-subscription failure cleanup, and providerless pending order visibility.
- Improve billing invoice activity labels for deferred entitlement and trial subscription rows.

## Test plan
- [x] cd services/claw-interface && ruff check .
- [x] cd services/claw-interface && pnpm dlx pyright app tests
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_orders_trial_logic.py tests/unit/test_antom_routes.py tests/unit/test_antom_client.py tests/unit/test_antom_handlers.py tests/unit/test_subscription_cron.py tests/unit/test_orders_repo.py -q
- [x] pnpm --dir web run lint
- [x] pnpm --dir web run test:unit
- [x] cd web && pnpm --filter @zooclaw/web-app exec tsc --noEmit
- [ ] pnpm --dir web run tsc (workspace script fails before TypeScript with pnpm Unknown option: --if-present; package tsc above passes)
- [ ] full backend pytest coverage run was interrupted per request after reaching 100%; before interruption it had already surfaced unrelated failures outside billing/opened PR scope

## Size override
- Required because this PR couples Antom trial support with billing state-machine fixes, production data repair notes, and focused regression tests for Stripe/Antom parity. Splitting would leave the trial behavior and cancel/renew correctness partially validated across PRs.

---

## 6d48f649 - fix(web): wrap marketing-root reset in @layer base so Tailwind utilities win (#1931)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T13:39:05Z  
**SHA**: 6d48f6492fcdda3b1baf014a3d9de6a86de65663

**完整 Commit Message**:

```
fix(web): wrap marketing-root reset in @layer base so Tailwind utilities win (#1931)

## Why

Follow-up to #1928. After that PR deployed to staging, padding/margin
Tailwind utilities on `<PublicHeader>` / `<PublicFooter>` were **still**
being zeroed. Playwright probe of staging `/pricing`:

| element | className | expected | observed |
|---|---|---|---|
| dropdown trigger | `pb-5 -mb-5 group/dropdown ...` | `pb 20px / mb
-20px` | `pb 0 / mb 0` |
| footer | `pt-24 pb-12 px-20 ...` | `pt 96px / pb 48px / px 80px` | all
0 |
| footer col h5 | `mb-4 ...` | `mb 16px` | `mb 0` |

## Root cause

Tailwind v4 puts utility classes in `@layer utilities`. **Unlayered
styles always beat any @layered styles regardless of specificity.** The
`:where()` fix from #1928 dropped the reset to `(0,0,1)` but it was
still unlayered, so it still won the cascade against `@layer utilities {
.pb-5 { ... } }`.

## Fix

Wrap the reset in `@layer base { ... }`:

```diff
+@layer base {
   :where(.pricing-root) *,
   :where(.pricing-root) *::before,
   :where(.pricing-root) *::after { margin: 0; padding: 0; box-sizing: border-box; }
+}
```

Cascade order now resolves correctly:
1. `@layer base { :where(.pricing-root) * }` (lowest layer) — only wins
if nothing else applies
2. `@layer utilities { .pb-5 }` (later layer) — beats base
3. `.pricing-root .plan-card` (unlayered, page-body) — beats everything
in layers

Page-body styling is unchanged — they're already unlayered multi-class
selectors that beat both the reset and Tailwind utilities, just as
before. The `:where()` guard from #1928 stays in place as defense in
depth.

Also drops the redundant box-sizing-only reset on `userguide.css` line
19 — the layered reset already covers it.

## Test guard

Extends `tests/unit/css/marketing-root-reset.unit.spec.ts` to assert
BOTH invariants per file:

1. `:where()` wrap (specificity guard, from #1928)
2. `@layer ...` wrap (cascade-layer guard, this PR)

Verified by temporarily unwrapping `pricing.css`'s `@layer base` and
re-running — the new assertion fired with a clear message pointing at
the offending selector. Restored.

## Test plan

- [x] `pnpm tsc --noEmit`
- [x] `pnpm lint`
- [x] `pnpm test:unit` — 371 files / 5719 cases pass (3 new assertions
added across the 3 CSS files)
- [ ] After staging deploy: Playwright probe should report `triggerPb:
20px / triggerMb: -20px / footerPt: 96px / footerH5Mb: 16px` etc.,
matching what the Tailwind class strings ask for.
- [ ] Hover smoke on staging: dropdown menus stay open while mouse moves
through the bridge zone.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Why

Follow-up to #1928. After that PR deployed to staging, padding/margin Tailwind utilities on `<PublicHeader>` / `<PublicFooter>` were **still** being zeroed. Playwright probe of staging `/pricing`:

| element | className | expected | observed |
|---|---|---|---|
| dropdown trigger | `pb-5 -mb-5 group/dropdown ...` | `pb 20px / mb -20px` | `pb 0 / mb 0` |
| footer | `pt-24 pb-12 px-20 ...` | `pt 96px / pb 48px / px 80px` | all 0 |
| footer col h5 | `mb-4 ...` | `mb 16px` | `mb 0` |

## Root cause

Tailwind v4 puts utility classes in `@layer utilities`. **Unlayered styles always beat any @layered styles regardless of specificity.** The `:where()` fix from #1928 dropped the reset to `(0,0,1)` but it was still unlayered, so it still won the cascade against `@layer utilities { .pb-5 { ... } }`.

## Fix

Wrap the reset in `@layer base { ... }`:

```diff
+@layer base {
   :where(.pricing-root) *,
   :where(.pricing-root) *::before,
   :where(.pricing-root) *::after { margin: 0; padding: 0; box-sizing: border-box; }
+}
```

Cascade order now resolves correctly:
1. `@layer base { :where(.pricing-root) * }` (lowest layer) — only wins if nothing else applies
2. `@layer utilities { .pb-5 }` (later layer) — beats base
3. `.pricing-root .plan-card` (unlayered, page-body) — beats everything in layers

Page-body styling is unchanged — they're already unlayered multi-class selectors that beat both the reset and Tailwind utilities, just as before. The `:where()` guard from #1928 stays in place as defense in depth.

Also drops the redundant box-sizing-only reset on `userguide.css` line 19 — the layered reset already covers it.

## Test guard

Extends `tests/unit/css/marketing-root-reset.unit.spec.ts` to assert BOTH invariants per file:

1. `:where()` wrap (specificity guard, from #1928)
2. `@layer ...` wrap (cascade-layer guard, this PR)

Verified by temporarily unwrapping `pricing.css`'s `@layer base` and re-running — the new assertion fired with a clear message pointing at the offending selector. Restored.

## Test plan

- [x] `pnpm tsc --noEmit`
- [x] `pnpm lint`
- [x] `pnpm test:unit` — 371 files / 5719 cases pass (3 new assertions added across the 3 CSS files)
- [ ] After staging deploy: Playwright probe should report `triggerPb: 20px / triggerMb: -20px / footerPt: 96px / footerH5Mb: 16px` etc., matching what the Tailwind class strings ask for.
- [ ] Hover smoke on staging: dropdown menus stay open while mouse moves through the bridge zone.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 4fbcfa1c - fix(web): lower marketing-root reset specificity so Tailwind utilities win (#1928)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T13:13:51Z  
**SHA**: 4fbcfa1c7e47babac6f76966203646d187e1f2f6

**完整 Commit Message**:

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

---

## 2e5b6122 - style(enterprise-admin): polish onboarding flow (#1929)

**作者**: bill-srp  
**日期**: 2026-05-25T11:10:55Z  
**SHA**: 2e5b612264d1d6a922a151d7711e0ccaed3ec87a

**完整 Commit Message**:

```
style(enterprise-admin): polish onboarding flow (#1929)

## Summary
- Polish the Enterprise Admin onboarding flow UI across setup, invite,
warm pool, and progress components
- Add Enterprise Admin coverage badge support to code-quality CI
- Add Enterprise Admin coverage badges to the root and package READMEs

## Test plan
- [x] pnpm --dir web/enterprise-admin test --
app/onboarding/__tests__/onboarding-page.test.tsx
components/onboarding/__tests__/StepIndicator.test.tsx
components/onboarding/__tests__/OrgSetupForm.test.tsx
components/onboarding/__tests__/BulkInviteForm.test.tsx
components/onboarding/__tests__/WarmPoolForm.test.tsx
- [x] pnpm --dir web/enterprise-admin exec eslint
app/onboarding/page.tsx components/onboarding/StepIndicator.tsx
components/onboarding/OrgSetupForm.tsx
components/onboarding/BulkInviteForm.tsx
components/onboarding/WarmPoolForm.tsx --max-warnings=0
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin test:coverage
- [x] git diff --check
```

**PR Description**:

## Summary
- Polish the Enterprise Admin onboarding flow UI across setup, invite, warm pool, and progress components
- Add Enterprise Admin coverage badge support to code-quality CI
- Add Enterprise Admin coverage badges to the root and package READMEs

## Test plan
- [x] pnpm --dir web/enterprise-admin test -- app/onboarding/__tests__/onboarding-page.test.tsx components/onboarding/__tests__/StepIndicator.test.tsx components/onboarding/__tests__/OrgSetupForm.test.tsx components/onboarding/__tests__/BulkInviteForm.test.tsx components/onboarding/__tests__/WarmPoolForm.test.tsx
- [x] pnpm --dir web/enterprise-admin exec eslint app/onboarding/page.tsx components/onboarding/StepIndicator.tsx components/onboarding/OrgSetupForm.tsx components/onboarding/BulkInviteForm.tsx components/onboarding/WarmPoolForm.tsx --max-warnings=0
- [x] pnpm --dir web/enterprise-admin exec tsc --noEmit
- [x] pnpm --dir web/enterprise-admin test:coverage
- [x] git diff --check

---

## 2d4e73a5 - fix(billing): polish payment method selection modal (#1925)

**作者**: vincent-srp  
**日期**: 2026-05-25T10:28:52Z  
**SHA**: 2d4e73a52d4e2280395881396177da7c04dc878c

**完整 Commit Message**:

```
fix(billing): polish payment method selection modal (#1925)

## Summary
- Render `Select Payment Method` through a body portal and polish it
into a balanced wide dual-column modal with a Montserrat heading,
clearer vertical spacing, and stable provider marks.
- Keep trial promotion on the subscription plan card rather than
repeating the Card ribbon inside the payment-method chooser, and
localize chooser copy across the existing 10 locales.
- Offer the same Card/Alipay choice from the paywall and open
Antom/Alipay checkout in a new tab consistently for subscription,
top-up, and gift flows while removing duplicate loading feedback.
- Add regression coverage for modal mounting, localized/ribbon-free
rendering, paywall selection, and Antom new-tab flows.

## Root cause
The shared payment chooser rendered inside transformed
subscription/paywall modal ancestors, so its fixed overlay inherited the
parent sizing context and appeared distorted. Provider marks also relied
on auto intrinsic sizing, the chooser repeated promotional ribbon
content in a transactional step, and the Antom success paths still
replaced the current page instead of opening checkout separately.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit` (`370` files, `5710` tests passed,
`1` todo)
- [x] Playwright against existing `localhost:3000/zh/subscription` with
checkout APIs intercepted: verified localized heading (`选择支付方式`),
localized Card option (`银行卡`), no option ribbon, and Alipay opening a
popup while closing the chooser.
- [ ] `pnpm --dir web run tsc` is blocked before compilation by the
existing workspace script passing unsupported `--if-present` to `pnpm
exec` (`Unknown option: 'if-present'`); the affected app typecheck above
passes.

## Environment note
Local validation reports the existing engine warning because this
machine currently runs Node `v22.14.0` while the workspace declares Node
`>=24 <25`.
```

**PR Description**:

## Summary
- Render `Select Payment Method` through a body portal and polish it into a balanced wide dual-column modal with a Montserrat heading, clearer vertical spacing, and stable provider marks.
- Keep trial promotion on the subscription plan card rather than repeating the Card ribbon inside the payment-method chooser, and localize chooser copy across the existing 10 locales.
- Offer the same Card/Alipay choice from the paywall and open Antom/Alipay checkout in a new tab consistently for subscription, top-up, and gift flows while removing duplicate loading feedback.
- Add regression coverage for modal mounting, localized/ribbon-free rendering, paywall selection, and Antom new-tab flows.

## Root cause
The shared payment chooser rendered inside transformed subscription/paywall modal ancestors, so its fixed overlay inherited the parent sizing context and appeared distorted. Provider marks also relied on auto intrinsic sizing, the chooser repeated promotional ribbon content in a transactional step, and the Antom success paths still replaced the current page instead of opening checkout separately.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit` (`370` files, `5710` tests passed, `1` todo)
- [x] Playwright against existing `localhost:3000/zh/subscription` with checkout APIs intercepted: verified localized heading (`选择支付方式`), localized Card option (`银行卡`), no option ribbon, and Alipay opening a popup while closing the chooser.
- [ ] `pnpm --dir web run tsc` is blocked before compilation by the existing workspace script passing unsupported `--if-present` to `pnpm exec` (`Unknown option: 'if-present'`); the affected app typecheck above passes.

## Environment note
Local validation reports the existing engine warning because this machine currently runs Node `v22.14.0` while the workspace declares Node `>=24 <25`.


---

## f01e71b9 - docs(web): add SideNav refactor spec (issue #368 F11) (#1927)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T10:16:33Z  
**SHA**: f01e71b91262a7215fb0412d404a5499e0ddd21f

**完整 Commit Message**:

```
docs(web): add SideNav refactor spec (issue #368 F11) (#1927)

## Summary

加 design spec 记录 `web/app/src/components/SideNav.tsx` 拆分重构计划，对应 issue
[#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
F11 finding。

**This PR 只加文档，不动代码。** 3 个实现 PR 后续开。

- 主函数 506 → ≤150 行，子组件 + 子 hook 落到新建 `web/app/src/components/sidenav/`
- 3-PR 串行：PR 1（UI helpers + `useNavAuthState`）→ PR 2（logo + agent list +
scroll hooks）→ PR 3（bottom nav + user section + `git mv`）
- 同步消除 `UserInfoSection` 内与主组件重复的 auth event listener
- Reconcile issue body 与代码 drift（937 → 876 行，hook 路径，"locale switching"
不存在）

## Tracking

Closes: – (跟踪 issue
[#1926](https://github.com/SerendipityOneInc/ecap-workspace/issues/1926)，由后续
3 个 refactor PR 关闭)
Parent:
[#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
F11

## Test plan

- [ ] CI 全过（spec PR，无代码改动）
- [ ] Spec 内 8 条 staging 手测路径在每个 follow-up refactor PR 落地时执行

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

加 design spec 记录 `web/app/src/components/SideNav.tsx` 拆分重构计划，对应 issue [#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) F11 finding。

**This PR 只加文档，不动代码。** 3 个实现 PR 后续开。

- 主函数 506 → ≤150 行，子组件 + 子 hook 落到新建 `web/app/src/components/sidenav/`
- 3-PR 串行：PR 1（UI helpers + `useNavAuthState`）→ PR 2（logo + agent list + scroll hooks）→ PR 3（bottom nav + user section + `git mv`）
- 同步消除 `UserInfoSection` 内与主组件重复的 auth event listener
- Reconcile issue body 与代码 drift（937 → 876 行，hook 路径，"locale switching" 不存在）

## Tracking

Closes: – (跟踪 issue [#1926](https://github.com/SerendipityOneInc/ecap-workspace/issues/1926)，由后续 3 个 refactor PR 关闭)
Parent: [#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) F11

## Test plan

- [ ] CI 全过（spec PR，无代码改动）
- [ ] Spec 内 8 条 staging 手测路径在每个 follow-up refactor PR 落地时执行

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 14f1b973 - refactor(web): dedupe public chrome via Tailwind + --marketing-* tokens (#1915)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T09:23:20Z  
**SHA**: 14f1b973f008f3de4e6c5598f3fbba6038552887

**完整 Commit Message**:

```
refactor(web): dedupe public chrome via Tailwind + --marketing-* tokens (#1915)

## Summary
- Dedupe the public-marketing chrome (header / nav-dropdown / mobile-nav
/ btn-signin/up / footer / lang-dropdown) across `landing` / `pricing` /
`userguide` so #1896's hover-bridge fix is no longer at risk of
regressing on a single page (which is exactly what was observed after
landing on `/pricing`).
- Move chrome styling into Tailwind classes on `PublicHeader` /
`PublicFooter`, backed by `--marketing-*` tokens in `globals.css`. Each
page's local CSS file shrinks to page-body-only.
- No new wrapper component — `LandingClient` / `PublicPricingClient` /
`UserGuideClient` continue to import `<PublicHeader>` and
`<PublicFooter>` directly. An earlier draft introduced a
`<PublicChrome>` wrapper that only relayed prop bags; reviewer flagged
it as a non-abstraction and it's been dropped.

## What changed
- **Modified** `web/app/src/components/public/PublicHeader.tsx` /
`PublicFooter.tsx` — every className converted from CSS-class names to
Tailwind utilities (using `bg-marketing-*` / `text-marketing-*` /
`border-marketing-*` tokens for branded colors and `text-white/N` for
pure-white opacity tints). `PublicHeader` extracts `DesktopNav` +
`MobileMenu` subcomponents to stay under `max-lines-per-function`.
- **Modified** `web/app/src/app/globals.css` — adds a `--marketing-*`
token block under `:root` (17 tokens) and aliases them in `@theme
inline` so they're consumable as Tailwind utility classes.
- **Modified** `landing.css` / `pricing.css` / `userguide.css` — chrome
blocks deleted, page-body styles kept, breadcrumb comment left pointing
at `PublicHeader.tsx` / `PublicFooter.tsx` + `globals.css`.
- **Modified** `UserGuideClient.tsx` — sidebar visibility scroll handler
queries `[data-marketing-footer]` instead of the stripped `.footer`
class.

## Hover-bridge invariant
The "dropdown disappears when crossing the gap" bug class is prevented
in one place, with the constraint co-located in code:
- `PublicHeader.tsx` — `DESKTOP_DROPDOWN_TRIGGER = 'group/dropdown
relative -mb-5 pb-5'` (extends the trigger's hit area 20px down)
- `PublicHeader.tsx` — `DESKTOP_DROPDOWN_MENU` includes `mt-0` (no top
margin = continuous hover surface)
- Comment block above the trigger constant explains the invariant

## Known visual deltas (mobile only)
Landing was the richest variant and became the merged baseline. On
mobile, `pricing` and `userguide` pick up two minor changes:
- footer top padding: **60px → 48px**
- footer-inner gap: **48px → 32px** (landing-only override before)

Visually almost unnoticeable but worth eyeballing on the deployed env.

## Test plan
- [x] `pnpm tsc --noEmit`
- [x] `pnpm lint`
- [x] `pnpm test:unit` — 367 files / 5686 cases pass
- [ ] On deployed env, hover Learn + Resources dropdowns on landing /
pricing / userguide and confirm menus stay open while moving into them
- [ ] On deployed env, eyeball mobile footer on pricing / userguide for
the two deltas noted above

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary
- Dedupe the public-marketing chrome (header / nav-dropdown / mobile-nav / btn-signin/up / footer / lang-dropdown) across `landing` / `pricing` / `userguide` so #1896's hover-bridge fix is no longer at risk of regressing on a single page (which is exactly what was observed after landing on `/pricing`).
- Move chrome styling into Tailwind classes on `PublicHeader` / `PublicFooter`, backed by `--marketing-*` tokens in `globals.css`. Each page's local CSS file shrinks to page-body-only.
- No new wrapper component — `LandingClient` / `PublicPricingClient` / `UserGuideClient` continue to import `<PublicHeader>` and `<PublicFooter>` directly. An earlier draft introduced a `<PublicChrome>` wrapper that only relayed prop bags; reviewer flagged it as a non-abstraction and it's been dropped.

## What changed
- **Modified** `web/app/src/components/public/PublicHeader.tsx` / `PublicFooter.tsx` — every className converted from CSS-class names to Tailwind utilities (using `bg-marketing-*` / `text-marketing-*` / `border-marketing-*` tokens for branded colors and `text-white/N` for pure-white opacity tints). `PublicHeader` extracts `DesktopNav` + `MobileMenu` subcomponents to stay under `max-lines-per-function`.
- **Modified** `web/app/src/app/globals.css` — adds a `--marketing-*` token block under `:root` (17 tokens) and aliases them in `@theme inline` so they're consumable as Tailwind utility classes.
- **Modified** `landing.css` / `pricing.css` / `userguide.css` — chrome blocks deleted, page-body styles kept, breadcrumb comment left pointing at `PublicHeader.tsx` / `PublicFooter.tsx` + `globals.css`.
- **Modified** `UserGuideClient.tsx` — sidebar visibility scroll handler queries `[data-marketing-footer]` instead of the stripped `.footer` class.

## Hover-bridge invariant
The "dropdown disappears when crossing the gap" bug class is prevented in one place, with the constraint co-located in code:
- `PublicHeader.tsx` — `DESKTOP_DROPDOWN_TRIGGER = 'group/dropdown relative -mb-5 pb-5'` (extends the trigger's hit area 20px down)
- `PublicHeader.tsx` — `DESKTOP_DROPDOWN_MENU` includes `mt-0` (no top margin = continuous hover surface)
- Comment block above the trigger constant explains the invariant

## Known visual deltas (mobile only)
Landing was the richest variant and became the merged baseline. On mobile, `pricing` and `userguide` pick up two minor changes:
- footer top padding: **60px → 48px**
- footer-inner gap: **48px → 32px** (landing-only override before)

Visually almost unnoticeable but worth eyeballing on the deployed env.

## Test plan
- [x] `pnpm tsc --noEmit`
- [x] `pnpm lint`
- [x] `pnpm test:unit` — 367 files / 5686 cases pass
- [ ] On deployed env, hover Learn + Resources dropdowns on landing / pricing / userguide and confirm menus stay open while moving into them
- [ ] On deployed env, eyeball mobile footer on pricing / userguide for the two deltas noted above

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 69ce4fd5 - refactor(web): delete window.openXxxPreview shim + add ESLint guard (#368 F6+F10 PR 4) (#1918)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T09:15:24Z  
**SHA**: 69ce4fd5030c9010f6a140f80fd1d53d29640466

**完整 Commit Message**:

```
refactor(web): delete window.openXxxPreview shim + add ESLint guard (#368 F6+F10 PR 4) (#1918)

## Summary

**Final PR in the F6/F10 series.** After
[#1900](https://github.com/SerendipityOneInc/ecap-workspace/pull/1900) /
[#1914](https://github.com/SerendipityOneInc/ecap-workspace/pull/1914) /
[#1916](https://github.com/SerendipityOneInc/ecap-workspace/pull/1916)
migrated all consumers to `useImagePreview()` / `useFilePreview()`, the
`window.openImagePreview` / `window.openFilePreview` shims and their
module-level stack registry became dead code. This PR deletes them
entirely and adds a lint guard.

### Deletions

**`ImagePreviewProvider.tsx`** (–71 LoC):
- Module-level `shimHandlers` / `shimPrevious` / `shimInstalled` state
- `ensureShimInstalled` / `maybeTeardownShim` helpers
- `useEffect` that pushed handlers onto the stack
- `registerWindowShim` prop
- `declare global { interface Window { openImagePreview } }` block
- `useEffect` import (no longer used)

**`FilePreviewProvider.tsx`** — mirror cleanup (–70 LoC).

**Tests** (–~270 LoC across both specs):
- Removed entire `describe('window.openXxxPreview compat shim', ...)`
blocks — covered shim install/teardown, single-delegate routing,
top-of-stack delegation, LIFO / non-LIFO unmount semantics,
`registerWindowShim={false}` opt-out. All testing now-deleted
infrastructure.
- Added one new test per Provider: `useOptional*Preview()` returns
`null` outside the Provider (preserves the detached-`createRoot`
contract that's the only remaining differentiator between the strict and
optional hook variants).

### Additions

- **ESLint guard** (`eslint.config.mjs` Rule 8): selector
`MemberExpression[object.name="window"][property.name=/^open(Image|File)Preview$/]`
rejects future reintroduction of `window.openImagePreview` /
`window.openFilePreview` with a Chinese rationale pointing to the
Provider files.
- Minor doc refresh in `ReplayPlayer.tsx`: "install
window.openFilePreview" comment → "publish via useFilePreview()".

### Issue #368 status

F6 + F10 fully resolved. Next rolling `claude-arch-review.yaml` cycle
should auto-strike them through and move them to `<!--
ARCH_REVIEW:RESOLVED_BEGIN -->`.

### Net diff

**6 files, +42 / –449 lines** — pure subtraction.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean (includes the new Rule 8 self-applying to the
source tree)
- [x] `pnpm lint:ci` (knip + dep-cruiser) — passes
- [x] `pnpm test:unit` — 370 files / 5703 tests pass (–12 shim-specific
tests, +2 useOptional null-return tests)
- [x] Grep audit: zero `window.openImagePreview` /
`window.openFilePreview` / `Window['openXxxPreview']` references in
`src/` or `tests/` outside the ESLint rule string itself in
`eslint.config.mjs`
- [ ] Manual smoke after merge: try all 5 chat / canvas / replay preview
paths from PR 1-3 manuals; intentionally write
`window.openImagePreview(...)` in any consumer and confirm lint rejects
it

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

**Final PR in the F6/F10 series.** After [#1900](https://github.com/SerendipityOneInc/ecap-workspace/pull/1900) / [#1914](https://github.com/SerendipityOneInc/ecap-workspace/pull/1914) / [#1916](https://github.com/SerendipityOneInc/ecap-workspace/pull/1916) migrated all consumers to `useImagePreview()` / `useFilePreview()`, the `window.openImagePreview` / `window.openFilePreview` shims and their module-level stack registry became dead code. This PR deletes them entirely and adds a lint guard.

### Deletions

**`ImagePreviewProvider.tsx`** (–71 LoC):
- Module-level `shimHandlers` / `shimPrevious` / `shimInstalled` state
- `ensureShimInstalled` / `maybeTeardownShim` helpers
- `useEffect` that pushed handlers onto the stack
- `registerWindowShim` prop
- `declare global { interface Window { openImagePreview } }` block
- `useEffect` import (no longer used)

**`FilePreviewProvider.tsx`** — mirror cleanup (–70 LoC).

**Tests** (–~270 LoC across both specs):
- Removed entire `describe('window.openXxxPreview compat shim', ...)` blocks — covered shim install/teardown, single-delegate routing, top-of-stack delegation, LIFO / non-LIFO unmount semantics, `registerWindowShim={false}` opt-out. All testing now-deleted infrastructure.
- Added one new test per Provider: `useOptional*Preview()` returns `null` outside the Provider (preserves the detached-`createRoot` contract that's the only remaining differentiator between the strict and optional hook variants).

### Additions

- **ESLint guard** (`eslint.config.mjs` Rule 8): selector `MemberExpression[object.name="window"][property.name=/^open(Image|File)Preview$/]` rejects future reintroduction of `window.openImagePreview` / `window.openFilePreview` with a Chinese rationale pointing to the Provider files.
- Minor doc refresh in `ReplayPlayer.tsx`: "install window.openFilePreview" comment → "publish via useFilePreview()".

### Issue #368 status

F6 + F10 fully resolved. Next rolling `claude-arch-review.yaml` cycle should auto-strike them through and move them to `<!-- ARCH_REVIEW:RESOLVED_BEGIN -->`.

### Net diff

**6 files, +42 / –449 lines** — pure subtraction.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean (includes the new Rule 8 self-applying to the source tree)
- [x] `pnpm lint:ci` (knip + dep-cruiser) — passes
- [x] `pnpm test:unit` — 370 files / 5703 tests pass (–12 shim-specific tests, +2 useOptional null-return tests)
- [x] Grep audit: zero `window.openImagePreview` / `window.openFilePreview` / `Window['openXxxPreview']` references in `src/` or `tests/` outside the ESLint rule string itself in `eslint.config.mjs`
- [ ] Manual smoke after merge: try all 5 chat / canvas / replay preview paths from PR 1-3 manuals; intentionally write `window.openImagePreview(...)` in any consumer and confirm lint rejects it

---

## 1e712e28 - ci(services): deploy protected R2 access worker (#1917)

**作者**: bill-srp  
**日期**: 2026-05-25T09:12:11Z  
**SHA**: 1e712e282ad816ddd6e07d3c382034eb6b862db3

**完整 Commit Message**:

```
ci(services): deploy protected R2 access worker (#1917)

## Summary
- Add a standalone Cloudflare Worker for protected R2 object reads from
the agent packs bucket.
- Authorize reads by validating the caller against claw-interface
/account/me and matching the org_id from the R2 key path.
- Add a production-only GitHub Actions workflow to test, type-check, and
deploy the worker with Wrangler.

## Test plan
- [x] pnpm --dir services/r2-access-worker test
- [x] pnpm --dir services/r2-access-worker exec tsc --noEmit
```

**PR Description**:

## Summary
- Add a standalone Cloudflare Worker for protected R2 object reads from the agent packs bucket.
- Authorize reads by validating the caller against claw-interface /account/me and matching the org_id from the R2 key path.
- Add a production-only GitHub Actions workflow to test, type-check, and deploy the worker with Wrangler.

## Test plan
- [x] pnpm --dir services/r2-access-worker test
- [x] pnpm --dir services/r2-access-worker exec tsc --noEmit

---

## 97172437 - refactor(web): migrate file consumers to useFilePreview() (#368 F10 PR 3) (#1916)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T09:00:27Z  
**SHA**: 97172437e048447847f25a7196fa27df799b0374

**完整 Commit Message**:

```
refactor(web): migrate file consumers to useFilePreview() (#368 F10 PR 3) (#1916)

## Summary

Third PR in the F6/F10 series (after
[#1900](https://github.com/SerendipityOneInc/ecap-workspace/pull/1900) /
[#1914](https://github.com/SerendipityOneInc/ecap-workspace/pull/1914)).
Five consumer components now read the file-preview opener from React
Context (`useFilePreview()` / `useOptionalFilePreview()`) instead of
`window.openFilePreview`. **After this PR, zero consumer code reads
either `window.openImagePreview` or `window.openFilePreview`** — only
the Providers themselves do, as part of the transitional shim. PR 4 will
delete the shims entirely.

Migrated consumers:
- **`MarkdownContent.tsx`** (file card click via container delegation) —
uses `useOptionalFilePreview()` for the same detached `createRoot`
reason as the image-side. Copy Link / Download branches remain
Provider-independent (carrying the PR 2 round-1 Codex fix pattern
through to the file path).
- **`MyUploadsTab.tsx`** (file path of asset row click)
- **`WorkspaceFilesTab.tsx`**
- **`MmPendingAttachmentChip.tsx`**
- **`mattermost/MMAttachments.tsx`** (`FileAttachment` for live MM +
`ReplayAttachment` generic file path)

**API change**: positional `window.openFilePreview(url, name, ext,
source?)` → named-arg `open({ url, name, ext, source? })`.

**New helper export**: `useOptionalFilePreview()` in
`FilePreviewProvider.tsx` mirrors `useOptionalImagePreview()`. Required
for `MarkdownContent` because it renders into detached `createRoot`
sub-trees (nested SpecialistConsentCard) where Context doesn't
propagate.

**Type declaration relocated**: `Window['openFilePreview']` moves from
`MarkdownContent.tsx` (former consumer) to `FilePreviewProvider.tsx`
(the producer of the shim). The PR-1-relocated
`Window['openImagePreview']` already lives in ImagePreviewProvider.

**Behavior cleanup**: `ReplayAttachment.openInPanel` previously fell
back to `window.open(url, '_blank', 'noopener,noreferrer')` when no
handler was registered. The fallback is dead post F10 (ReplayPlayer
always wraps with FilePreviewProvider via PR 1 round-1) and is removed.
Corresponding fallback test dropped.

**Test plumbing**: `GenClawInput.unit.spec.tsx` transitively renders
`MmPendingAttachmentChip` (now Provider-dependent); added the
`FilePreviewProvider` mock there.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm lint:ci` (knip + dep-cruiser) — passes
- [x] `pnpm test:unit` — 370 files / 5715 tests pass
- [x] Grep audit: zero `window.openImagePreview` /
`window.openFilePreview` references in consumer code; only the Providers
reference these globals (to install/teardown shims)
- [ ] Manual smoke after merge: file card click in chat → artifacts
sidebar; click .docx / .pdf attachment in MM thread → sidebar; click
file row in MyUploads / WorkspaceFiles tab; paste a previewable file
into composer → MmPendingAttachmentChip click previews it; public replay
link → click MM file attachment → sidebar

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

Third PR in the F6/F10 series (after [#1900](https://github.com/SerendipityOneInc/ecap-workspace/pull/1900) / [#1914](https://github.com/SerendipityOneInc/ecap-workspace/pull/1914)). Five consumer components now read the file-preview opener from React Context (`useFilePreview()` / `useOptionalFilePreview()`) instead of `window.openFilePreview`. **After this PR, zero consumer code reads either `window.openImagePreview` or `window.openFilePreview`** — only the Providers themselves do, as part of the transitional shim. PR 4 will delete the shims entirely.

Migrated consumers:
- **`MarkdownContent.tsx`** (file card click via container delegation) — uses `useOptionalFilePreview()` for the same detached `createRoot` reason as the image-side. Copy Link / Download branches remain Provider-independent (carrying the PR 2 round-1 Codex fix pattern through to the file path).
- **`MyUploadsTab.tsx`** (file path of asset row click)
- **`WorkspaceFilesTab.tsx`**
- **`MmPendingAttachmentChip.tsx`**
- **`mattermost/MMAttachments.tsx`** (`FileAttachment` for live MM + `ReplayAttachment` generic file path)

**API change**: positional `window.openFilePreview(url, name, ext, source?)` → named-arg `open({ url, name, ext, source? })`.

**New helper export**: `useOptionalFilePreview()` in `FilePreviewProvider.tsx` mirrors `useOptionalImagePreview()`. Required for `MarkdownContent` because it renders into detached `createRoot` sub-trees (nested SpecialistConsentCard) where Context doesn't propagate.

**Type declaration relocated**: `Window['openFilePreview']` moves from `MarkdownContent.tsx` (former consumer) to `FilePreviewProvider.tsx` (the producer of the shim). The PR-1-relocated `Window['openImagePreview']` already lives in ImagePreviewProvider.

**Behavior cleanup**: `ReplayAttachment.openInPanel` previously fell back to `window.open(url, '_blank', 'noopener,noreferrer')` when no handler was registered. The fallback is dead post F10 (ReplayPlayer always wraps with FilePreviewProvider via PR 1 round-1) and is removed. Corresponding fallback test dropped.

**Test plumbing**: `GenClawInput.unit.spec.tsx` transitively renders `MmPendingAttachmentChip` (now Provider-dependent); added the `FilePreviewProvider` mock there.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm lint:ci` (knip + dep-cruiser) — passes
- [x] `pnpm test:unit` — 370 files / 5715 tests pass
- [x] Grep audit: zero `window.openImagePreview` / `window.openFilePreview` references in consumer code; only the Providers reference these globals (to install/teardown shims)
- [ ] Manual smoke after merge: file card click in chat → artifacts sidebar; click .docx / .pdf attachment in MM thread → sidebar; click file row in MyUploads / WorkspaceFiles tab; paste a previewable file into composer → MmPendingAttachmentChip click previews it; public replay link → click MM file attachment → sidebar

---

## 8b887b32 - refactor(web): migrate image consumers to useImagePreview() (#368 F6 PR 2) (#1914)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T08:36:20Z  
**SHA**: 8b887b321b6067e17879a91970baa91b986e9964

**完整 Commit Message**:

```
refactor(web): migrate image consumers to useImagePreview() (#368 F6 PR 2) (#1914)

## Summary

Second PR in the F6/F10 series (after
[#1900](https://github.com/SerendipityOneInc/ecap-workspace/pull/1900)).
Three consumer components now read the image-preview opener from React
Context (`useImagePreview()`) instead of `window.openImagePreview` —
that global shim now exists only for un-migrated file consumers (PR 3
will eliminate it).

- **`MarkdownContent.tsx`** — image + video thumbnail click via
`document` delegation. Uses the new `useOptionalImagePreview()` so
detached `createRoot` renderings (nested SpecialistConsentCard → compact
MarkdownContent) gracefully no-op rather than throw.
- **`MyUploadsTab.tsx`** — asset row click for image mime types.
- **`mattermost/MMAttachments.tsx`** — `ImageAttachment`,
`VideoAttachment`, and `ReplayAttachment` (image + video paths).

**API change**: positional `window.openImagePreview(url, gallery?)` →
named-arg `open({ url, gallery? })`.

**New helper export**: `useOptionalImagePreview()` in
`ImagePreviewProvider.tsx` returns the context value or `null` (vs.
strict `useImagePreview()` which throws when missing). Required for
`MarkdownContent` because it can be rendered into detached `createRoot`
sub-trees (Specialist cards) where Context doesn't cross the root
boundary. All other consumers use the strict variant.

**Type declaration relocated**: `Window['openImagePreview']` moves from
`MarkdownContent.tsx` (former consumer) to `ImagePreviewProvider.tsx`
(the producer of the shim). `Window['openFilePreview']` stays in
`MarkdownContent.tsx` until PR 3.

**Behavior cleanup**: `ImageAttachment` previously fell back to
`window.open(url, '_blank')` when no `window.openImagePreview` handler
was registered. The fallback is dead post F6 (the Provider is always in
scope for chat / replay trees) and is removed. Corresponding "falls back
to window.open" test dropped.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm lint:ci` (knip + dep-cruiser) — passes
- [x] `pnpm test:unit` — 370 files / 5715 tests pass (1 dropped:
window.open fallback no longer reachable)
- [x] Grep audit: zero `window.openImagePreview` references in consumer
code; only `ImagePreviewProvider.tsx` references the global to
install/teardown the shim
- [ ] Manual smoke after merge: click an image in main chat / Canvas /
public replay → lightbox; gallery navigation works;
SpecialistConsentCard renders without throwing

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

Second PR in the F6/F10 series (after [#1900](https://github.com/SerendipityOneInc/ecap-workspace/pull/1900)). Three consumer components now read the image-preview opener from React Context (`useImagePreview()`) instead of `window.openImagePreview` — that global shim now exists only for un-migrated file consumers (PR 3 will eliminate it).

- **`MarkdownContent.tsx`** — image + video thumbnail click via `document` delegation. Uses the new `useOptionalImagePreview()` so detached `createRoot` renderings (nested SpecialistConsentCard → compact MarkdownContent) gracefully no-op rather than throw.
- **`MyUploadsTab.tsx`** — asset row click for image mime types.
- **`mattermost/MMAttachments.tsx`** — `ImageAttachment`, `VideoAttachment`, and `ReplayAttachment` (image + video paths).

**API change**: positional `window.openImagePreview(url, gallery?)` → named-arg `open({ url, gallery? })`.

**New helper export**: `useOptionalImagePreview()` in `ImagePreviewProvider.tsx` returns the context value or `null` (vs. strict `useImagePreview()` which throws when missing). Required for `MarkdownContent` because it can be rendered into detached `createRoot` sub-trees (Specialist cards) where Context doesn't cross the root boundary. All other consumers use the strict variant.

**Type declaration relocated**: `Window['openImagePreview']` moves from `MarkdownContent.tsx` (former consumer) to `ImagePreviewProvider.tsx` (the producer of the shim). `Window['openFilePreview']` stays in `MarkdownContent.tsx` until PR 3.

**Behavior cleanup**: `ImageAttachment` previously fell back to `window.open(url, '_blank')` when no `window.openImagePreview` handler was registered. The fallback is dead post F6 (the Provider is always in scope for chat / replay trees) and is removed. Corresponding "falls back to window.open" test dropped.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm lint:ci` (knip + dep-cruiser) — passes
- [x] `pnpm test:unit` — 370 files / 5715 tests pass (1 dropped: window.open fallback no longer reachable)
- [x] Grep audit: zero `window.openImagePreview` references in consumer code; only `ImagePreviewProvider.tsx` references the global to install/teardown the shim
- [ ] Manual smoke after merge: click an image in main chat / Canvas / public replay → lightbox; gallery navigation works; SpecialistConsentCard renders without throwing

---

## f201230d - feat(account): enrich account and org users from profiles (#1906)

**作者**: bill-srp  
**日期**: 2026-05-25T08:02:58Z  
**SHA**: f201230d48adc04cbc4418ea0164c03f8dee328b

**完整 Commit Message**:

```
feat(account): enrich account and org users from profiles (#1906)

Linear:
https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Fill /account/me email and name from profile lookup when available
- Enrich org user list rows with profile email/name
- Tighten list-users response typing so internal billing fields cannot
leak

## Stack
Depends on #1905.

## Checks
- devcontainer: ruff check focused profile-enrichment files
- devcontainer: pyright focused profile-enrichment files
- devcontainer: pytest focused profile-enrichment unit suite (86 passed)
- size check: under budget
```

**PR Description**:

Linear: https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Fill /account/me email and name from profile lookup when available
- Enrich org user list rows with profile email/name
- Tighten list-users response typing so internal billing fields cannot leak

## Stack
Depends on #1905.

## Checks
- devcontainer: ruff check focused profile-enrichment files
- devcontainer: pyright focused profile-enrichment files
- devcontainer: pytest focused profile-enrichment unit suite (86 passed)
- size check: under budget

---

## 5d100ab8 - feat(org): add enterprise org billing and invite registration (#1905)

**作者**: bill-srp  
**日期**: 2026-05-25T07:44:59Z  
**SHA**: 5d100ab8ec7d84fc2b17023b567fc4b1673ccd9e

**完整 Commit Message**:

```
feat(org): add enterprise org billing and invite registration (#1905)

Linear:
https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Provision and store org billing team ids server-side
- Bind invited users to billing teams during join
- Support invite-code signup through /account
- Add member role update and restore admin gate on org creation

## Stack
Depends on #1904, which depends on #1903.

## Checks
- devcontainer: ruff check focused org/billing files
- devcontainer: pyright focused org/billing files
- devcontainer: pytest focused org/billing/account unit suite (257
passed)
- size check: under budget

---------

Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: bill-srp <undefined@users.noreply.github.com>
```

**PR Description**:

Linear: https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Provision and store org billing team ids server-side
- Bind invited users to billing teams during join
- Support invite-code signup through /account
- Add member role update and restore admin gate on org creation

## Stack
Depends on #1904, which depends on #1903.

## Checks
- devcontainer: ruff check focused org/billing files
- devcontainer: pyright focused org/billing files
- devcontainer: pytest focused org/billing/account unit suite (257 passed)
- size check: under budget

---

## 288abf48 - refactor(claw-interface): split pack creation from submissions (#1909)

**作者**: bill-srp  
**日期**: 2026-05-25T07:37:07Z  
**SHA**: 288abf4817b05ab6893141f88cae294c8b2c0167

**完整 Commit Message**:

```
refactor(claw-interface): split pack creation from submissions (#1909)

## Summary
- create packs as backend draft records without an initial submission
- submit pack versions separately; first submission only changes the
draft pack status to submitted while unapproved version metadata stays
on PackSubmission
- add the enterprise-admin pack flow: create pack details first, then
add a submission with uploaded ZIP
- add R2 agent-pack upload key support for
`{org_id}/{pack_id}/{uuid-without-dashes}.zip`

## Tests
- python3 -m py_compile app/database/pack_repo.py
app/routes/enterprise/pack_store.py app/schema/pack.py
app/services/pack_store/submission_service.py
tests/unit/test_pack_services.py tests/unit/test_pack_repo.py
tests/unit/test_routes_pack_store.py tests/unit/test_schema_pack.py
- pnpm --filter @zooclaw/enterprise-admin test --
"app/(dashboard)/packs/__tests__/packs-page.test.tsx"
"app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx"
"app/api/r2/upload/__tests__/route.test.ts"
"hooks/__tests__/usePacks.test.tsx" "lib/r2/__tests__/index.test.ts"
"lib/r2/__tests__/key.test.ts"
```

**PR Description**:

## Summary
- create packs as backend draft records without an initial submission
- submit pack versions separately; first submission only changes the draft pack status to submitted while unapproved version metadata stays on PackSubmission
- add the enterprise-admin pack flow: create pack details first, then add a submission with uploaded ZIP
- add R2 agent-pack upload key support for `{org_id}/{pack_id}/{uuid-without-dashes}.zip`

## Tests
- python3 -m py_compile app/database/pack_repo.py app/routes/enterprise/pack_store.py app/schema/pack.py app/services/pack_store/submission_service.py tests/unit/test_pack_services.py tests/unit/test_pack_repo.py tests/unit/test_routes_pack_store.py tests/unit/test_schema_pack.py
- pnpm --filter @zooclaw/enterprise-admin test -- "app/(dashboard)/packs/__tests__/packs-page.test.tsx" "app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx" "app/api/r2/upload/__tests__/route.test.ts" "hooks/__tests__/usePacks.test.tsx" "lib/r2/__tests__/index.test.ts" "lib/r2/__tests__/key.test.ts"

---

## 9d8b1a21 - refactor(web): introduce ImagePreview/FilePreview providers (#368 F6+F10 PR 1) (#1900)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T07:33:09Z  
**SHA**: 9d8b1a2192b998b0f05809930b369a7a04827734

**完整 Commit Message**:

```
refactor(web): introduce ImagePreview/FilePreview providers (#368 F6+F10 PR 1) (#1900)

## Summary

Land React Context infrastructure for the
[#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368)
F6 (`window.openImagePreview`) / F10 (`window.openFilePreview`)
window-bridge migration. **Pure addition + one dead-code cleanup**:
every existing consumer continues to work via the compat shim each
Provider installs. This is the first of a 4-PR series — PR 2/3 migrate
consumers off `(window as any)`, PR 4 removes the shims.

- **`ImagePreviewProvider`**
(`web/app/src/components/providers/ImagePreviewProvider.tsx`) owns
`previewImage` / `previewGallery` state, renders the `ImagePreview`
modal, exposes `useImagePreview()` returning `{ open, close, navigate
}`, and registers `window.openImagePreview` with a save/restore shim
(improves on the older `delete window.openImagePreview` in
`useImagePreviewBridge` / `agent-chat-client`).
- **`FilePreviewProvider`**
(`web/app/src/components/providers/FilePreviewProvider.tsx`) takes the
`useArtifactsSidebar` return as a `state` prop, exposes
`useFilePreview()` returning `{ open, close, activeFile, isOpen }`, and
registers `window.openFilePreview`. `useArtifactsSidebar` itself stops
touching the global and now returns an imperative `openFile(file)`; the
reducer / race-fix machinery (#1415, #1781) is **untouched**.
- **Caller wrap**: `GenClawClient`,
`components/agent-chat-client/index.tsx`, and
`app/share/[shareId]/ReplayPlayer.tsx` wrap their trees in the new
Provider(s). The public-replay `ReplayLightbox` component will be
deleted in PR 4 once its minimal JSX has fully migrated into
`ImagePreviewProvider`.
- **`useImagePreviewBridge.ts` deleted** — its responsibilities are
entirely internalized into `ImagePreviewProvider`. The hook's unit test
is replaced by `ImagePreviewProvider.unit.spec.tsx`.
`useArtifactsSidebar.unit.spec.ts` rewritten to drive
`result.current.openFile({...})` instead of
`window.openFilePreview(...)`.

**Zero consumer files modified.** `MarkdownContent`, `MMAttachments`,
`MyUploadsTab`, `WorkspaceFilesTab`, `MmPendingAttachmentChip` still
read `(window as any).openXxxPreview?.()` and continue to work through
the Provider-installed shim. Migration of those call sites to
`useImagePreview()` / `useFilePreview()` is PR 2 (image) + PR 3 (file).
PR 4 deletes the window shims after both migrations land.

Design rationale and full multi-PR plan: see
`/home/node/.claude/plans/issue-368-merry-ocean.md` (local) — the
unified approach matches the existing 4 Provider+imperative-hook
patterns in the codebase (`ToastProvider` / `FeedbackProvider` /
`SupportTicketProvider` / `SubscriptionPanelProvider`) instead of
introducing zustand/jotai.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit` — 367 files / 5685 tests pass (1 todo)
- [x] New unit tests cover: `useXxxPreview()` throws outside Provider;
modal/state lifecycle; window shim save/restore;
`registerWindowShim={false}` opt-out
- [x] Grep audit: consumer files (`MarkdownContent` / `MMAttachments` /
`MmPendingAttachmentChip` / etc.) still reference
`window.openXxxPreview`, unchanged; new Provider files own the
registration
- [ ] Manual smoke after merge: click an image in chat → lightbox; click
a file card → artifacts sidebar; open replay share link → lightbox still
works

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

Land React Context infrastructure for the [#368](https://github.com/SerendipityOneInc/ecap-workspace/issues/368) F6 (`window.openImagePreview`) / F10 (`window.openFilePreview`) window-bridge migration. **Pure addition + one dead-code cleanup**: every existing consumer continues to work via the compat shim each Provider installs. This is the first of a 4-PR series — PR 2/3 migrate consumers off `(window as any)`, PR 4 removes the shims.

- **`ImagePreviewProvider`** (`web/app/src/components/providers/ImagePreviewProvider.tsx`) owns `previewImage` / `previewGallery` state, renders the `ImagePreview` modal, exposes `useImagePreview()` returning `{ open, close, navigate }`, and registers `window.openImagePreview` with a save/restore shim (improves on the older `delete window.openImagePreview` in `useImagePreviewBridge` / `agent-chat-client`).
- **`FilePreviewProvider`** (`web/app/src/components/providers/FilePreviewProvider.tsx`) takes the `useArtifactsSidebar` return as a `state` prop, exposes `useFilePreview()` returning `{ open, close, activeFile, isOpen }`, and registers `window.openFilePreview`. `useArtifactsSidebar` itself stops touching the global and now returns an imperative `openFile(file)`; the reducer / race-fix machinery (#1415, #1781) is **untouched**.
- **Caller wrap**: `GenClawClient`, `components/agent-chat-client/index.tsx`, and `app/share/[shareId]/ReplayPlayer.tsx` wrap their trees in the new Provider(s). The public-replay `ReplayLightbox` component will be deleted in PR 4 once its minimal JSX has fully migrated into `ImagePreviewProvider`.
- **`useImagePreviewBridge.ts` deleted** — its responsibilities are entirely internalized into `ImagePreviewProvider`. The hook's unit test is replaced by `ImagePreviewProvider.unit.spec.tsx`. `useArtifactsSidebar.unit.spec.ts` rewritten to drive `result.current.openFile({...})` instead of `window.openFilePreview(...)`.

**Zero consumer files modified.** `MarkdownContent`, `MMAttachments`, `MyUploadsTab`, `WorkspaceFilesTab`, `MmPendingAttachmentChip` still read `(window as any).openXxxPreview?.()` and continue to work through the Provider-installed shim. Migration of those call sites to `useImagePreview()` / `useFilePreview()` is PR 2 (image) + PR 3 (file). PR 4 deletes the window shims after both migrations land.

Design rationale and full multi-PR plan: see `/home/node/.claude/plans/issue-368-merry-ocean.md` (local) — the unified approach matches the existing 4 Provider+imperative-hook patterns in the codebase (`ToastProvider` / `FeedbackProvider` / `SupportTicketProvider` / `SubscriptionPanelProvider`) instead of introducing zustand/jotai.

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit` — 367 files / 5685 tests pass (1 todo)
- [x] New unit tests cover: `useXxxPreview()` throws outside Provider; modal/state lifecycle; window shim save/restore; `registerWindowShim={false}` opt-out
- [x] Grep audit: consumer files (`MarkdownContent` / `MMAttachments` / `MmPendingAttachmentChip` / etc.) still reference `window.openXxxPreview`, unchanged; new Provider files own the registration
- [ ] Manual smoke after merge: click an image in chat → lightbox; click a file card → artifacts sidebar; open replay share link → lightbox still works

---

## 6f9357f3 - test(account): add registration BDD coverage (#1904)

**作者**: bill-srp  
**日期**: 2026-05-25T07:24:19Z  
**SHA**: 6f9357f35177320d0ba1217b191ec5ebe4d2fe96

**完整 Commit Message**:

```
test(account): add registration BDD coverage (#1904)

Linear:
https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Add registration BDD feature scenarios for /account
- Cover auto-org, idempotent register, metadata, /me, and warm-pool
asset test alignment

## Stack
Depends on #1903.

## Checks
- devcontainer: ruff check BDD/warm-pool tests
- devcontainer: pyright BDD/warm-pool tests
- devcontainer: pytest registration BDD + warm-pool unit tests (BDD
scenarios skipped locally because Mongo auth is unavailable; unit tests
passed)
- size check: under budget
```

**PR Description**:

Linear: https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Add registration BDD feature scenarios for /account
- Cover auto-org, idempotent register, metadata, /me, and warm-pool asset test alignment

## Stack
Depends on #1903.

## Checks
- devcontainer: ruff check BDD/warm-pool tests
- devcontainer: pyright BDD/warm-pool tests
- devcontainer: pytest registration BDD + warm-pool unit tests (BDD scenarios skipped locally because Mongo auth is unavailable; unit tests passed)
- size check: under budget

---

## b3dd3631 - refactor(web): extract escape handler + add hook unit specs (#368 F12 PR5) (#1912)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T07:21:36Z  
**SHA**: b3dd363125a3b05041e3c5837b72ee606fcb5095

**完整 Commit Message**:

```
refactor(web): extract escape handler + add hook unit specs (#368 F12 PR5) (#1912)

## Summary

**Fifth and final slice** of the [PublishAgentsClient
refactor](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-publish-agents-refactor.md).
Closes out issue #368 F12.

### Extraction

- New \`useModalStackEscape\` hook (35 lines) accepts a declarative
stack of \`{ open, close }\` entries and drives a document-level Escape
listener that closes the first open modal in array order. Internal ref
pattern attaches the listener exactly once and reads the latest stack on
each keypress — the naive \`[stack]\` deps would re-attach the listener
on every parent render.
- Orchestrator's 36-line \`useEffect\` block collapses to a 6-line call
that lists the priority chain (result modal → install confirm → delete
confirm → detail → create) declaratively.
- PublishAgentsClient drops from **451 → 422 lines** and is finally free
of \`useEffect\`.

### Test coverage

- \`useModalStackEscape.unit.spec.tsx\` (6 tests) — priority order,
skipping closed entries, Escape-only filter, latest-stack semantics
(regression for the ref pattern), unmount cleanup.
- \`useAgentInstallToggle.unit.spec.tsx\` (9 tests) — all 4
install/uninstall branches (custom × install/uninstall, import ×
install/uninstall), post-mutation refresh, bot-not-ready failure routing
to \`onError\` without firing any install API, install API failure
routing to \`onError\`, **refresh-failure swallow contract** (refresh
rejection must still route to \`onSuccess\` — preserves the legacy
\"best-effort cache flush\" semantics that two earlier PRs protected via
load-bearing comments), and \`togglingId\` / \`isToggling\` lifecycle
around a pending mutation.

Total publish-page tests now **39 green** (17 integration + 6
useZipPackages + 6 useModalStackEscape + 9 useAgentInstallToggle + 1
ad-hoc).

## Series totals

| | Before | After |
|---|---|---|
| Orchestrator size | 1159 lines | **422 lines** (-737, -64%) |
| \`useState\` count | 13 | **7** |
| Raw \`fetch\` callsites | 1 | **0** |
| Raw mutation \`useEffect\` | 1 | **0** |
| Inline modal JSX blocks | 5 | **0** (pure subcomponents) |
| Module-scoped hooks | 0 | **6** (useZipPackages / useEnsureBotReady /
useAgentInstallToggle / usePublishForm / usePublishDelete /
useModalStackEscape) |
| Dedicated hook unit specs | 0 | **3** (~22 cases) |

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| 0+1 | refactor/publish-zip-packages-query | merged #1898 |
| 2 | refactor/publish-install-mutation | merged #1901 |
| 3 | refactor/publish-form-and-delete | merged #1908 |
| 4 | refactor/publish-modal-subcomponents | merged #1911 |
| **5** | this PR (final) | here |

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green
- [x] \`pnpm vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx
tests/unit/app/agents-manager/publish/\` — all 39 tests pass
- [ ] CI \`code-quality / lint-and-test\` green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

**Fifth and final slice** of the [PublishAgentsClient refactor](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-publish-agents-refactor.md). Closes out issue #368 F12.

### Extraction

- New \`useModalStackEscape\` hook (35 lines) accepts a declarative stack of \`{ open, close }\` entries and drives a document-level Escape listener that closes the first open modal in array order. Internal ref pattern attaches the listener exactly once and reads the latest stack on each keypress — the naive \`[stack]\` deps would re-attach the listener on every parent render.
- Orchestrator's 36-line \`useEffect\` block collapses to a 6-line call that lists the priority chain (result modal → install confirm → delete confirm → detail → create) declaratively.
- PublishAgentsClient drops from **451 → 422 lines** and is finally free of \`useEffect\`.

### Test coverage

- \`useModalStackEscape.unit.spec.tsx\` (6 tests) — priority order, skipping closed entries, Escape-only filter, latest-stack semantics (regression for the ref pattern), unmount cleanup.
- \`useAgentInstallToggle.unit.spec.tsx\` (9 tests) — all 4 install/uninstall branches (custom × install/uninstall, import × install/uninstall), post-mutation refresh, bot-not-ready failure routing to \`onError\` without firing any install API, install API failure routing to \`onError\`, **refresh-failure swallow contract** (refresh rejection must still route to \`onSuccess\` — preserves the legacy \"best-effort cache flush\" semantics that two earlier PRs protected via load-bearing comments), and \`togglingId\` / \`isToggling\` lifecycle around a pending mutation.

Total publish-page tests now **39 green** (17 integration + 6 useZipPackages + 6 useModalStackEscape + 9 useAgentInstallToggle + 1 ad-hoc).

## Series totals

| | Before | After |
|---|---|---|
| Orchestrator size | 1159 lines | **422 lines** (-737, -64%) |
| \`useState\` count | 13 | **7** |
| Raw \`fetch\` callsites | 1 | **0** |
| Raw mutation \`useEffect\` | 1 | **0** |
| Inline modal JSX blocks | 5 | **0** (pure subcomponents) |
| Module-scoped hooks | 0 | **6** (useZipPackages / useEnsureBotReady / useAgentInstallToggle / usePublishForm / usePublishDelete / useModalStackEscape) |
| Dedicated hook unit specs | 0 | **3** (~22 cases) |

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| 0+1 | refactor/publish-zip-packages-query | merged #1898 |
| 2 | refactor/publish-install-mutation | merged #1901 |
| 3 | refactor/publish-form-and-delete | merged #1908 |
| 4 | refactor/publish-modal-subcomponents | merged #1911 |
| **5** | this PR (final) | here |

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green
- [x] \`pnpm vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx tests/unit/app/agents-manager/publish/\` — all 39 tests pass
- [ ] CI \`code-quality / lint-and-test\` green

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## cddf9b83 - fix(web): use canonical origin for Antom redirects (#1910)

**作者**: kaka-srp  
**日期**: 2026-05-25T07:15:31Z  
**SHA**: cddf9b83eb27d309e3e843b4a8d4714a692aa7a8

**完整 Commit Message**:

```
fix(web): use canonical origin for Antom redirects (#1910)

## Summary
- Use configured `NEXT_PUBLIC_SITE_URL` as the canonical Antom
success/cancel redirect origin.
- Keep request `Origin` as a local/dev fallback when no canonical site
URL is configured.
- Add unit coverage for `www.zooclaw.ai` requests producing `zooclaw.ai`
redirect URLs.

## Root cause
The Antom BFF built redirect URLs directly from the browser `Origin`
header. Requests from `https://www.zooclaw.ai` therefore sent
`www.zooclaw.ai` to claw-interface, whose redirect-host allowlist only
includes configured canonical frontend/backend hosts, so it rejected the
request before reaching Antom.

## Test plan
- [x] `git diff --check --
web/app/src/app/api/antom/create-payment/route.ts
web/app/tests/unit/app/api/antom-create-payment.unit.spec.ts`
- [ ] Not run: web unit tests require installing `web/node_modules`;
install was stopped per request because local dependency download was
too slow and space-heavy.
```

**PR Description**:

## Summary
- Use configured `NEXT_PUBLIC_SITE_URL` as the canonical Antom success/cancel redirect origin.
- Keep request `Origin` as a local/dev fallback when no canonical site URL is configured.
- Add unit coverage for `www.zooclaw.ai` requests producing `zooclaw.ai` redirect URLs.

## Root cause
The Antom BFF built redirect URLs directly from the browser `Origin` header. Requests from `https://www.zooclaw.ai` therefore sent `www.zooclaw.ai` to claw-interface, whose redirect-host allowlist only includes configured canonical frontend/backend hosts, so it rejected the request before reaching Antom.

## Test plan
- [x] `git diff --check -- web/app/src/app/api/antom/create-payment/route.ts web/app/tests/unit/app/api/antom-create-payment.unit.spec.ts`
- [ ] Not run: web unit tests require installing `web/node_modules`; install was stopped per request because local dependency download was too slow and space-heavy.

---

## 074b68d2 - fix(pack-store): use mongo-compatible sort arguments (#1907)

**作者**: bill-srp  
**日期**: 2026-05-25T07:11:25Z  
**SHA**: 074b68d2f70fd8fd418cadda6f9808fee3463060

**完整 Commit Message**:

```
fix(pack-store): use mongo-compatible sort arguments (#1907)

## Summary
- Use Mongo-compatible sort argument shapes in pack repositories
- Add unit coverage for pack and pack-submission sort behavior

## Split
Independent cleanup split out of the enterprise account PR because it is
unrelated to account/org registration.

## Checks
- devcontainer: ruff check pack repository files
- devcontainer: pyright pack repository files
- devcontainer: pytest tests/unit/test_pack_repo.py
tests/unit/test_pack_submission_repo.py (14 passed)
- size check: under budget
```

**PR Description**:

## Summary
- Use Mongo-compatible sort argument shapes in pack repositories
- Add unit coverage for pack and pack-submission sort behavior

## Split
Independent cleanup split out of the enterprise account PR because it is unrelated to account/org registration.

## Checks
- devcontainer: ruff check pack repository files
- devcontainer: pyright pack repository files
- devcontainer: pytest tests/unit/test_pack_repo.py tests/unit/test_pack_submission_repo.py (14 passed)
- size check: under budget

---

## e1849b94 - refactor(web): extract publish modal + card subcomponents (#368 F12 PR4) (#1911)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T07:10:47Z  
**SHA**: e1849b9451cc49664e61d6990030514002833f21

**完整 Commit Message**:

```
refactor(web): extract publish modal + card subcomponents (#368 F12 PR4) (#1911)

## Summary

Fourth slice of the [PublishAgentsClient
refactor](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-publish-agents-refactor.md).
Pulls 5 inline modals and the card grid item out of the orchestrator
into pure presentational components under \`publish/components/\`.

**New components**:
- \`PublishCard\` (+ inline \`PublishInstallButton\` /
\`PublishDeleteButton\` / \`DeleteHint\` re-exports used by the detail
modal)
- \`PublishCreateModal\` / \`PublishDetailModal\` /
\`PublishInstallConfirmModal\` / \`PublishDeleteConfirmModal\` /
\`PublishSyncingOverlay\` / \`PublishActionResultModal\`

**Shared pieces**:
- \`EmojiBadge\` (5 callsites) / \`formatDate\` (2 callsites)
- \`types.ts\` — \`PublishAgentCardItem\` + \`InstallButtonProps\` /
\`DeleteButtonProps\` / \`DeleteHintKey\` / \`ActionResultState\` /
\`PendingInstallAction\`

**Orchestrator drops**:
- 5 modal JSX blocks (~440 lines combined)
- 3 inline render helpers (\`renderInstallButton\` /
\`renderDeleteButton\` / \`renderDeleteHint\`) + \`installButtonLabel\`
- \`EmojiBadge\` + \`formatDate\` definitions (moved to shared files)
- 3 type aliases (moved to \`types.ts\`)

Replaced by \`buildInstallButtonProps\` / \`buildDeleteButtonProps\` /
\`getDeleteHintKey\` helpers built once per card and passed to both
\`PublishCard\` and \`PublishDetailModal\` so the buttons render
identically in both surfaces.

The orchestrator now owns: react-query hooks + useState + useEffect
(escape key) + handler glue + page chrome (header + cards grid + 5
conditional \`<Modal />\` tags).

**Component drops 957 → 451 lines (-506).**

## Behavior parity preserved

- All 9 \`data-testid\` attributes intact: \`publish-upload-card\` /
\`publish-name-input\` / \`publish-id-preview\` /
\`publish-zip-path-select\` / \`publish-link-input\` /
\`publish-submit-button\` / \`publish-install-confirm-button\` /
\`publish-delete-button-\${id}\` / \`publish-delete-confirm-button\`
- Z-index stacking unchanged: modal z-50 / install-confirm z-54 /
delete-confirm z-55 / syncing z-58 / action-result z-60
- \`onClick={(e) => e.stopPropagation()}\` on every modal inner div —
overlay-click-to-close still works
- \`autoFocus\` on create modal's name input preserved
- \`bg-[var(--ecap-overlay-heavy)]\` arbitrary value left intact (not in
scope to migrate to a semantic token)

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| 0+1 | refactor/publish-zip-packages-query | merged #1898 |
| 2 | refactor/publish-install-mutation | merged #1901 |
| 3 | refactor/publish-form-and-delete | merged #1908 |
| **4** | this PR | here |
| 5 | refactor/publish-escape-cleanup | after |

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green
- [x] \`pnpm vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx\` — all 17
integration tests pass (no test changes needed — testids + visible text
survived)
- [x] \`pnpm vitest run
tests/unit/app/agents-manager/publish/useZipPackages.unit.spec.tsx\` — 6
hook tests still green
- [ ] CI \`code-quality / lint-and-test\` green
- [ ] Visual smoke: modal layering / overlay-click / Escape priority —
TODO before approving

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

Fourth slice of the [PublishAgentsClient refactor](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-publish-agents-refactor.md). Pulls 5 inline modals and the card grid item out of the orchestrator into pure presentational components under \`publish/components/\`.

**New components**:
- \`PublishCard\` (+ inline \`PublishInstallButton\` / \`PublishDeleteButton\` / \`DeleteHint\` re-exports used by the detail modal)
- \`PublishCreateModal\` / \`PublishDetailModal\` / \`PublishInstallConfirmModal\` / \`PublishDeleteConfirmModal\` / \`PublishSyncingOverlay\` / \`PublishActionResultModal\`

**Shared pieces**:
- \`EmojiBadge\` (5 callsites) / \`formatDate\` (2 callsites)
- \`types.ts\` — \`PublishAgentCardItem\` + \`InstallButtonProps\` / \`DeleteButtonProps\` / \`DeleteHintKey\` / \`ActionResultState\` / \`PendingInstallAction\`

**Orchestrator drops**:
- 5 modal JSX blocks (~440 lines combined)
- 3 inline render helpers (\`renderInstallButton\` / \`renderDeleteButton\` / \`renderDeleteHint\`) + \`installButtonLabel\`
- \`EmojiBadge\` + \`formatDate\` definitions (moved to shared files)
- 3 type aliases (moved to \`types.ts\`)

Replaced by \`buildInstallButtonProps\` / \`buildDeleteButtonProps\` / \`getDeleteHintKey\` helpers built once per card and passed to both \`PublishCard\` and \`PublishDetailModal\` so the buttons render identically in both surfaces.

The orchestrator now owns: react-query hooks + useState + useEffect (escape key) + handler glue + page chrome (header + cards grid + 5 conditional \`<Modal />\` tags).

**Component drops 957 → 451 lines (-506).**

## Behavior parity preserved

- All 9 \`data-testid\` attributes intact: \`publish-upload-card\` / \`publish-name-input\` / \`publish-id-preview\` / \`publish-zip-path-select\` / \`publish-link-input\` / \`publish-submit-button\` / \`publish-install-confirm-button\` / \`publish-delete-button-\${id}\` / \`publish-delete-confirm-button\`
- Z-index stacking unchanged: modal z-50 / install-confirm z-54 / delete-confirm z-55 / syncing z-58 / action-result z-60
- \`onClick={(e) => e.stopPropagation()}\` on every modal inner div — overlay-click-to-close still works
- \`autoFocus\` on create modal's name input preserved
- \`bg-[var(--ecap-overlay-heavy)]\` arbitrary value left intact (not in scope to migrate to a semantic token)

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| 0+1 | refactor/publish-zip-packages-query | merged #1898 |
| 2 | refactor/publish-install-mutation | merged #1901 |
| 3 | refactor/publish-form-and-delete | merged #1908 |
| **4** | this PR | here |
| 5 | refactor/publish-escape-cleanup | after |

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green
- [x] \`pnpm vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx\` — all 17 integration tests pass (no test changes needed — testids + visible text survived)
- [x] \`pnpm vitest run tests/unit/app/agents-manager/publish/useZipPackages.unit.spec.tsx\` — 6 hook tests still green
- [ ] CI \`code-quality / lint-and-test\` green
- [ ] Visual smoke: modal layering / overlay-click / Escape priority — TODO before approving

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 2a969d3b - feat(account): add enterprise account API core (#1903)

**作者**: bill-srp  
**日期**: 2026-05-25T07:01:30Z  
**SHA**: 2a969d3b9cf6b2aed29b64607d2f3fdb6afd8112

**完整 Commit Message**:

```
feat(account): add enterprise account API core (#1903)

Linear:
https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Add /account registration and /account/me core response surface
- Add token-only registration auth dependency and account-backed auth
dependency
- Finalize warm-pool registration before falling back to normal account
upsert

## Split
This is PR 1 of the enterprise account stack. Follow-ups add BDD
coverage, org billing/invite behavior, and profile enrichment.

## Checks
- devcontainer: ruff check focused account files
- devcontainer: pyright focused account files
- devcontainer: pytest tests/unit/test_routes_account.py
- size check: under budget
```

**PR Description**:

Linear: https://linear.app/srpone/issue/ECA-764/phase-1-backend-changes-enterprise-data-model-warm-pool-cross-service

## Summary
- Add /account registration and /account/me core response surface
- Add token-only registration auth dependency and account-backed auth dependency
- Finalize warm-pool registration before falling back to normal account upsert

## Split
This is PR 1 of the enterprise account stack. Follow-ups add BDD coverage, org billing/invite behavior, and profile enrichment.

## Checks
- devcontainer: ruff check focused account files
- devcontainer: pyright focused account files
- devcontainer: pytest tests/unit/test_routes_account.py
- size check: under budget

---

## 96007ad0 - refactor(web): extract publish form + delete hooks (#368 F12 PR3) (#1908)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T06:52:01Z  
**SHA**: 96007ad0dd60779fe7045faa1b3d09f73594dcd6

**完整 Commit Message**:

```
refactor(web): extract publish form + delete hooks (#368 F12 PR3) (#1908)

## Summary

Third slice of the [PublishAgentsClient
refactor](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-publish-agents-refactor.md).
Pulls the create-form and delete-record flows out into two module-scoped
hooks:

- **\`usePublishForm\`** — owns the form useState, the derived
submission contract (\`canSubmit\` / \`normalizedId\` / \`idError\` /
\`duplicateId\`), \`validateForm\`, \`handleSubmit\`,
\`updatePathValue\`, and \`resetForm\`. Takes \`defaults\` / \`records\`
/ \`createPublishRecord\` as opts (not re-calling
\`useCustomAgentPublishes()\` to avoid registering a second \`storage\`
listener).
- **\`usePublishDelete\`** — \`useMutation\` wrapping
\`deletePublishRecord\`. Exposes \`deleteRecord\` / \`isDeleting\` /
\`deletingId\`.

**Orchestrator drops**:
- 3 useState (\`isSubmitting\`, \`deletingId\`, \`formState\`).
- 4 derivations + 4 handlers (\`resetForm\` / \`updatePathValue\` /
\`validateForm\` / \`canSubmit\` / \`handleSubmit\` etc.).
- Async branch of \`handleDeleteConfirm\`.
- \`FormErrors\` / \`PublishFormState\` type aliases +
\`createInitialFormState\` helper.

useState count: **11 → 8**. Component drops **96 lines (1054 → 958)**.

## Behavior parity preserved

- **Submit error branch**: only \`duplicate_id\` surfaces as the
form-field error; all other rejections silently keep the modal open
(legacy contract — left a code comment).
- **Delete success ordering**: success banner → close detail if matching
→ clear matching action result → close delete modal.
- **Form reset cycle**: \`closeCreateModal\` calls \`resetForm\`, and
\`openCreateModal\` also calls \`resetForm\` before opening — matches
legacy \"reset on both sides of the close-open cycle\".

## Stacking note

Branches off PR 2 (#1901, currently in merge queue) since main doesn't
have it yet. Once PR 2 lands, this branch's history will fold cleanly
during rebase (PR 2's commits are already in main and will drop as
duplicates).

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| 0+1 | refactor/publish-zip-packages-query | merged #1898 |
| 2 | refactor/publish-install-mutation | in merge queue (#1901) |
| **3** | this PR | here |
| 4 | refactor/publish-modal-subcomponents | after |
| 5 | refactor/publish-escape-cleanup | after |

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green
- [x] \`pnpm vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx\` — all 17
integration tests pass
- [x] \`pnpm vitest run
tests/unit/app/agents-manager/publish/useZipPackages.unit.spec.tsx\` — 6
hook tests still green
- [ ] CI \`code-quality / lint-and-test\` green
- [ ] Dedicated hook unit specs (\`usePublishForm\`,
\`usePublishDelete\`) — integration spec already exercises the full
surface; per the design spec, no separate hook spec is planned for these
two.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

Third slice of the [PublishAgentsClient refactor](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-publish-agents-refactor.md). Pulls the create-form and delete-record flows out into two module-scoped hooks:

- **\`usePublishForm\`** — owns the form useState, the derived submission contract (\`canSubmit\` / \`normalizedId\` / \`idError\` / \`duplicateId\`), \`validateForm\`, \`handleSubmit\`, \`updatePathValue\`, and \`resetForm\`. Takes \`defaults\` / \`records\` / \`createPublishRecord\` as opts (not re-calling \`useCustomAgentPublishes()\` to avoid registering a second \`storage\` listener).
- **\`usePublishDelete\`** — \`useMutation\` wrapping \`deletePublishRecord\`. Exposes \`deleteRecord\` / \`isDeleting\` / \`deletingId\`.

**Orchestrator drops**:
- 3 useState (\`isSubmitting\`, \`deletingId\`, \`formState\`).
- 4 derivations + 4 handlers (\`resetForm\` / \`updatePathValue\` / \`validateForm\` / \`canSubmit\` / \`handleSubmit\` etc.).
- Async branch of \`handleDeleteConfirm\`.
- \`FormErrors\` / \`PublishFormState\` type aliases + \`createInitialFormState\` helper.

useState count: **11 → 8**. Component drops **96 lines (1054 → 958)**.

## Behavior parity preserved

- **Submit error branch**: only \`duplicate_id\` surfaces as the form-field error; all other rejections silently keep the modal open (legacy contract — left a code comment).
- **Delete success ordering**: success banner → close detail if matching → clear matching action result → close delete modal.
- **Form reset cycle**: \`closeCreateModal\` calls \`resetForm\`, and \`openCreateModal\` also calls \`resetForm\` before opening — matches legacy \"reset on both sides of the close-open cycle\".

## Stacking note

Branches off PR 2 (#1901, currently in merge queue) since main doesn't have it yet. Once PR 2 lands, this branch's history will fold cleanly during rebase (PR 2's commits are already in main and will drop as duplicates).

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| 0+1 | refactor/publish-zip-packages-query | merged #1898 |
| 2 | refactor/publish-install-mutation | in merge queue (#1901) |
| **3** | this PR | here |
| 4 | refactor/publish-modal-subcomponents | after |
| 5 | refactor/publish-escape-cleanup | after |

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green
- [x] \`pnpm vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx\` — all 17 integration tests pass
- [x] \`pnpm vitest run tests/unit/app/agents-manager/publish/useZipPackages.unit.spec.tsx\` — 6 hook tests still green
- [ ] CI \`code-quality / lint-and-test\` green
- [ ] Dedicated hook unit specs (\`usePublishForm\`, \`usePublishDelete\`) — integration spec already exercises the full surface; per the design spec, no separate hook spec is planned for these two.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 4b363265 - fix(claw-interface): restore litellm install from PyPI (#1902)

**作者**: tim-srp  
**日期**: 2026-05-25T06:22:01Z  
**SHA**: 4b363265fcd1d7fbf5cf329b3ad932d145b7089a

**完整 Commit Message**:

```
fix(claw-interface): restore litellm install from PyPI (#1902)

## Summary
- Switch `services/claw-interface/requirements.txt` from
`git+https://github.com/BerriAI/litellm.git@v1.82.3` to
`litellm==1.82.3`.
- Same exact version (1.82.3), only the install source changes (git →
PyPI).
- Speeds up every fresh devcontainer / CI `uv pip install` by skipping
the git clone + setuptools wheel build of litellm (several minutes →
~15s for a cached PyPI wheel).

## Root cause
The original switch to git install — `91fb7a48` (2026-03-24, "fix:
install litellm from GitHub (PyPI quarantined)") — was a workaround for
PyPI quarantining all litellm versions. That quarantine has since been
lifted:

- `GET https://pypi.org/pypi/litellm/1.82.3/json` → `200`, both files
`yanked=False`
- `GET https://pypi.org/simple/litellm/` → `200`
- `pypi.org/pypi/litellm/json` lists 1.86.0 as latest stable (so the
project is actively publishing again)

`pyproject.toml`'s `[tool.deptry.package_module_name_map]` entry
`litellm = "litellm"` was already added as a defensive identity mapping
intended to survive a PyPI ↔ git source flip (per its own comment), so
no other config changes are needed.

## Test plan
- [x] Confirm PyPI hosts 1.82.3 unyanked: `curl
pypi.org/pypi/litellm/1.82.3/json | jq '.urls[].yanked'`
- [x] `uv pip install --reinstall-package litellm 'litellm==1.82.3'`
succeeds and replaces the git-installed copy
- [x] `importlib.metadata.version("litellm")` → `'1.82.3'`
- [x] `litellm.acompletion`, `litellm.exceptions.BadRequestError`,
`litellm.api_base`, `litellm.api_key` all available (these are the only
attrs used by `app/routes/litellm.py`)
- [x] `from app.routes import litellm` + `app.create_app.create_app()`
import cleanly (211 routes)
- [ ] CI `python-code-quality` (ruff + pyright + pytest + deptry +
import-linter) green
- [ ] `code-quality` (frontend lint+tsc+unit) — not relevant to this
change, expected unaffected

## Notes
- `app/routes/litellm.py` is documented as deprecated in
`services/claw-interface/CLAUDE.md` (legacy — serves only
`fullstack_assistant` and `canvas`; OpenClaw doesn't call it). The
conservative choice to stay at `1.82.3` rather than jump to latest
1.86.0 avoids spending regression effort on a module being phased out.
- `services/claw-interface/uv.lock` is an 8-line placeholder (only the
virtual `claw-interface` package), so no lockfile update is needed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 <noreply@anthropic.com>
```

**PR Description**:

## Summary
- Switch `services/claw-interface/requirements.txt` from `git+https://github.com/BerriAI/litellm.git@v1.82.3` to `litellm==1.82.3`.
- Same exact version (1.82.3), only the install source changes (git → PyPI).
- Speeds up every fresh devcontainer / CI `uv pip install` by skipping the git clone + setuptools wheel build of litellm (several minutes → ~15s for a cached PyPI wheel).

## Root cause
The original switch to git install — `91fb7a48` (2026-03-24, "fix: install litellm from GitHub (PyPI quarantined)") — was a workaround for PyPI quarantining all litellm versions. That quarantine has since been lifted:

- `GET https://pypi.org/pypi/litellm/1.82.3/json` → `200`, both files `yanked=False`
- `GET https://pypi.org/simple/litellm/` → `200`
- `pypi.org/pypi/litellm/json` lists 1.86.0 as latest stable (so the project is actively publishing again)

`pyproject.toml`'s `[tool.deptry.package_module_name_map]` entry `litellm = "litellm"` was already added as a defensive identity mapping intended to survive a PyPI ↔ git source flip (per its own comment), so no other config changes are needed.

## Test plan
- [x] Confirm PyPI hosts 1.82.3 unyanked: `curl pypi.org/pypi/litellm/1.82.3/json | jq '.urls[].yanked'`
- [x] `uv pip install --reinstall-package litellm 'litellm==1.82.3'` succeeds and replaces the git-installed copy
- [x] `importlib.metadata.version("litellm")` → `'1.82.3'`
- [x] `litellm.acompletion`, `litellm.exceptions.BadRequestError`, `litellm.api_base`, `litellm.api_key` all available (these are the only attrs used by `app/routes/litellm.py`)
- [x] `from app.routes import litellm` + `app.create_app.create_app()` import cleanly (211 routes)
- [ ] CI `python-code-quality` (ruff + pyright + pytest + deptry + import-linter) green
- [ ] `code-quality` (frontend lint+tsc+unit) — not relevant to this change, expected unaffected

## Notes
- `app/routes/litellm.py` is documented as deprecated in `services/claw-interface/CLAUDE.md` (legacy — serves only `fullstack_assistant` and `canvas`; OpenClaw doesn't call it). The conservative choice to stay at `1.82.3` rather than jump to latest 1.86.0 avoids spending regression effort on a module being phased out.
- `services/claw-interface/uv.lock` is an 8-line placeholder (only the virtual `claw-interface` package), so no lockfile update is needed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 9eae9eb8 - refactor(web): extract install/uninstall mutation hook (#368 F12 PR2) (#1901)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T05:59:18Z  
**SHA**: 9eae9eb8a5bf653b593550c37799f65f077bd4b8

**完整 Commit Message**:

```
refactor(web): extract install/uninstall mutation hook (#368 F12 PR2) (#1901)

## Summary

Second slice of the [PublishAgentsClient
refactor](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-publish-agents-refactor.md)
(issue #368 F12). Pulls the 4-branch install/uninstall flow out of
\`PublishAgentsClient\` into two module-scoped hooks:

- **\`useEnsureBotReady\`** — plain async fn wrapping the per-click
\`getOpenClawStatus\` + \`initOpenClaw\` gate.
- **\`useAgentInstallToggle\`** — \`useMutation\` wrapping the bot-ready
gate + 4-branch install/uninstall + post-mutation
\`refreshUserAgentsCache\` swallow. Exposes \`toggle\` / \`isToggling\`
/ \`togglingId\` so the orchestrator no longer needs a separate
\`installingId\` useState.

**Behavior parity preserved**:
- Refresh-failure swallow contract (legacy \`refreshInstalledState()\`
semantics) — kept the load-bearing comment verbatim.
- Action-result modal payload \`{ action, agentId, emoji, name }\`
unchanged.
- Bot-not-ready error still routes to the same \`actionFailed\` banner.

**Orchestrator drops**:
- \`installingId\` useState (now \`togglingId\` derived from
\`mutation.variables\`).
- \`ensureBotReady\` / \`performInstallToggle\` callbacks.
- 8 \`@/lib/api/openclaw\` imports + \`AGENT_OPERATION_TIMEOUT_MS\`
const.
- Unused \`userInfo\` destructuring from \`useAuth\`.

useState count: 12 → 11. The whole async-action concern leaves the file.

## Test infra change

Integration spec now wraps renders in \`createQueryWrapper\` so the real
\`useAgentInstallToggle\` executes its \`useMutation\` against the
existing API-level mocks (\`mockGetOpenClawStatus\` /
\`mockInstallCustomAgent\` / etc.). Other react-query hooks
(\`useUserAgents\` / \`useCustomAgentPublishes\` / \`useZipPackages\`)
remain module-mocked — they don't touch the provider so the wrapper is
inert for them.

This trades PR 1's "module-mock the hook" pattern for "wrap in provider
+ let real hook run against API mocks". The mock-the-hook approach would
have required duplicating ~50 lines of mutation logic in the test file;
the provider wrap is one helper.

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| 0+1 | refactor/publish-zip-packages-query | merged #1898 |
| **2** | this PR | here |
| 3 | refactor/publish-form-and-delete | after |
| 4 | refactor/publish-modal-subcomponents | after |
| 5 | refactor/publish-escape-cleanup | after |

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green (component + 2 new hooks + spec all clean)
- [x] \`pnpm vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx\` — all 17
integration tests pass
- [x] \`pnpm vitest run
tests/unit/app/agents-manager/publish/useZipPackages.unit.spec.tsx\` — 6
hook tests still green
- [x] \`web/scripts/check-no-raw-fetch-shrink-only.sh\` — guard passes
(0 → 0)
- [ ] CI \`code-quality / lint-and-test\` green
- [ ] Dedicated \`useAgentInstallToggle.unit.spec.tsx\` lands in PR 5
(per spec — exercises bot-ready failure routing, refresh-failure
swallow)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

Second slice of the [PublishAgentsClient refactor](https://github.com/SerendipityOneInc/ecap-workspace/blob/main/docs/superpowers/specs/2026-05-25-publish-agents-refactor.md) (issue #368 F12). Pulls the 4-branch install/uninstall flow out of \`PublishAgentsClient\` into two module-scoped hooks:

- **\`useEnsureBotReady\`** — plain async fn wrapping the per-click \`getOpenClawStatus\` + \`initOpenClaw\` gate.
- **\`useAgentInstallToggle\`** — \`useMutation\` wrapping the bot-ready gate + 4-branch install/uninstall + post-mutation \`refreshUserAgentsCache\` swallow. Exposes \`toggle\` / \`isToggling\` / \`togglingId\` so the orchestrator no longer needs a separate \`installingId\` useState.

**Behavior parity preserved**:
- Refresh-failure swallow contract (legacy \`refreshInstalledState()\` semantics) — kept the load-bearing comment verbatim.
- Action-result modal payload \`{ action, agentId, emoji, name }\` unchanged.
- Bot-not-ready error still routes to the same \`actionFailed\` banner.

**Orchestrator drops**:
- \`installingId\` useState (now \`togglingId\` derived from \`mutation.variables\`).
- \`ensureBotReady\` / \`performInstallToggle\` callbacks.
- 8 \`@/lib/api/openclaw\` imports + \`AGENT_OPERATION_TIMEOUT_MS\` const.
- Unused \`userInfo\` destructuring from \`useAuth\`.

useState count: 12 → 11. The whole async-action concern leaves the file.

## Test infra change

Integration spec now wraps renders in \`createQueryWrapper\` so the real \`useAgentInstallToggle\` executes its \`useMutation\` against the existing API-level mocks (\`mockGetOpenClawStatus\` / \`mockInstallCustomAgent\` / etc.). Other react-query hooks (\`useUserAgents\` / \`useCustomAgentPublishes\` / \`useZipPackages\`) remain module-mocked — they don't touch the provider so the wrapper is inert for them.

This trades PR 1's "module-mock the hook" pattern for "wrap in provider + let real hook run against API mocks". The mock-the-hook approach would have required duplicating ~50 lines of mutation logic in the test file; the provider wrap is one helper.

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| 0+1 | refactor/publish-zip-packages-query | merged #1898 |
| **2** | this PR | here |
| 3 | refactor/publish-form-and-delete | after |
| 4 | refactor/publish-modal-subcomponents | after |
| 5 | refactor/publish-escape-cleanup | after |

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green (component + 2 new hooks + spec all clean)
- [x] \`pnpm vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx\` — all 17 integration tests pass
- [x] \`pnpm vitest run tests/unit/app/agents-manager/publish/useZipPackages.unit.spec.tsx\` — 6 hook tests still green
- [x] \`web/scripts/check-no-raw-fetch-shrink-only.sh\` — guard passes (0 → 0)
- [ ] CI \`code-quality / lint-and-test\` green
- [ ] Dedicated \`useAgentInstallToggle.unit.spec.tsx\` lands in PR 5 (per spec — exercises bot-ready failure routing, refresh-failure swallow)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 1e9c63d4 - refactor(web): publish-agents spec + zip-packages react-query (#368 F12 PR1) (#1898)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T05:21:57Z  
**SHA**: 1e9c63d44464b66be345586ce9b3553024daea56

**完整 Commit Message**:

```
refactor(web): publish-agents spec + zip-packages react-query (#368 F12 PR1) (#1898)

## Summary

Lands the **PublishAgentsClient refactor spec** (PR 0 of the series)
plus the **first code slice** (PR 1) for issue #368 F12:

- New design spec at
`docs/superpowers/specs/2026-05-25-publish-agents-refactor.md` with the
full 5-PR plan, target architecture, sequence diagrams, and decision
log.
- Replaces the lone raw fetch in `PublishAgentsClient`
(`getCustomAgentZipPackages` driven by a `useEffect +
.then/.catch/.finally`) with a token-scoped `useQuery` wrapped in a new
module-scoped `useZipPackages` hook under `publish/hooks/`.
- Adds the `openclawKeys.customAgentZipPackages(authToken)` key
alongside the rest of the openclaw query-key factory.
- Drops `zipPackageOptions` / `zipPackageLoading` `useState` from the
component (13 → 12 useState; the larger reductions land in PR 2-3).

**Why this slice first**: it closes the file's only remaining
`no-raw-fetch` violation per the project's react-query mandate, with the
smallest surface area — zero behavior change.

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| **0+1** | this PR | here |
| 2 | refactor/publish-install-mutation | next |
| 3 | refactor/publish-form-and-delete | after PR 2 |
| 4 | refactor/publish-modal-subcomponents | after PR 3 |
| 5 | refactor/publish-escape-cleanup | after PR 4 |

PR 0 is bundled with PR 1 to save a CI cycle on a tiny code change (~100
LOC excluding spec).

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green (component + new hook + spec + key file all
clean)
- [x] \`pnpm vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx\` — all 17
integration tests pass
- [x] \`pnpm vitest run
tests/unit/hooks/useCustomAgentPublishes.unit.spec.ts\` — sibling spec
still green
- [x] \`web/scripts/check-no-raw-fetch-shrink-only.sh\` — shrink-only
guard passes (0 → 0)
- [ ] CI \`code-quality / lint-and-test\` green
- [ ] Dedicated \`useZipPackages.unit.spec.tsx\` lands in PR 5 (per spec
— uses real \`createQueryWrapper\`)

## Testing notes

The integration spec mock-replaces the new \`useZipPackages\` hook
(mirroring the existing \`useUserAgents\` / \`useCustomAgentPublishes\`
mock pattern) so it stays free of a \`QueryClientProvider\` wrapper
while existing \`mockGetCustomAgentZipPackages.mockResolvedValueOnce\` /
\`.mockRejectedValueOnce\` chains keep driving the fetch behavior. The
dedicated hook spec lands in PR 5 with the real react-query path.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**PR Description**:

## Summary

Lands the **PublishAgentsClient refactor spec** (PR 0 of the series) plus the **first code slice** (PR 1) for issue #368 F12:

- New design spec at `docs/superpowers/specs/2026-05-25-publish-agents-refactor.md` with the full 5-PR plan, target architecture, sequence diagrams, and decision log.
- Replaces the lone raw fetch in `PublishAgentsClient` (`getCustomAgentZipPackages` driven by a `useEffect + .then/.catch/.finally`) with a token-scoped `useQuery` wrapped in a new module-scoped `useZipPackages` hook under `publish/hooks/`.
- Adds the `openclawKeys.customAgentZipPackages(authToken)` key alongside the rest of the openclaw query-key factory.
- Drops `zipPackageOptions` / `zipPackageLoading` `useState` from the component (13 → 12 useState; the larger reductions land in PR 2-3).

**Why this slice first**: it closes the file's only remaining `no-raw-fetch` violation per the project's react-query mandate, with the smallest surface area — zero behavior change.

## Scope (this PR vs the rest)

| PR | Branch | Status |
|---|---|---|
| **0+1** | this PR | here |
| 2 | refactor/publish-install-mutation | next |
| 3 | refactor/publish-form-and-delete | after PR 2 |
| 4 | refactor/publish-modal-subcomponents | after PR 3 |
| 5 | refactor/publish-escape-cleanup | after PR 4 |

PR 0 is bundled with PR 1 to save a CI cycle on a tiny code change (~100 LOC excluding spec).

## Test plan

- [x] \`npx tsc --noEmit\` green (full workspace)
- [x] \`pnpm lint\` green (component + new hook + spec + key file all clean)
- [x] \`pnpm vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx\` — all 17 integration tests pass
- [x] \`pnpm vitest run tests/unit/hooks/useCustomAgentPublishes.unit.spec.ts\` — sibling spec still green
- [x] \`web/scripts/check-no-raw-fetch-shrink-only.sh\` — shrink-only guard passes (0 → 0)
- [ ] CI \`code-quality / lint-and-test\` green
- [ ] Dedicated \`useZipPackages.unit.spec.tsx\` lands in PR 5 (per spec — uses real \`createQueryWrapper\`)

## Testing notes

The integration spec mock-replaces the new \`useZipPackages\` hook (mirroring the existing \`useUserAgents\` / \`useCustomAgentPublishes\` mock pattern) so it stays free of a \`QueryClientProvider\` wrapper while existing \`mockGetCustomAgentZipPackages.mockResolvedValueOnce\` / \`.mockRejectedValueOnce\` chains keep driving the fetch behavior. The dedicated hook spec lands in PR 5 with the real react-query path.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## e11c5070 - fix(web): remove dead sidenav language panel (#1897)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T04:08:22Z  
**SHA**: e11c5070b487461707cc59ff638cb460efd337f8

**完整 Commit Message**:

```
fix(web): remove dead sidenav language panel (#1897)

## Summary
- remove the unreachable SideNav language/theme hover panel from the
collapsed-only user summary
- keep language switching owned by Settings > General

## Root cause
`SideNav` rendered `UserCard`/`UserMenu` in the expanded sidebar, while
the old language selector lived inside the collapsed-only
`UserInfoSection`. That selector also required `!isCollapsed`, making
the language panel unreachable and leaving stale locale/theme
responsibilities in `SideNav`.

## Test plan
- [x] `pnpm -C web/app exec eslint src/components/SideNav.tsx --quiet`
- [x] `pnpm -C web exec tsc --noEmit --project app/tsconfig.json`
- [x] `git diff --check`
```

**PR Description**:

## Summary
- remove the unreachable SideNav language/theme hover panel from the collapsed-only user summary
- keep language switching owned by Settings > General

## Root cause
`SideNav` rendered `UserCard`/`UserMenu` in the expanded sidebar, while the old language selector lived inside the collapsed-only `UserInfoSection`. That selector also required `!isCollapsed`, making the language panel unreachable and leaving stale locale/theme responsibilities in `SideNav`.

## Test plan
- [x] `pnpm -C web/app exec eslint src/components/SideNav.tsx --quiet`
- [x] `pnpm -C web exec tsc --noEmit --project app/tsconfig.json`
- [x] `git diff --check`


---

## 9ae045fd - fix(landing): keep public nav dropdown hoverable (#1896)

**作者**: Chris@ZooClaw  
**日期**: 2026-05-25T03:49:11Z  
**SHA**: 9ae045fd27c5a82b66909a7ee04b97a26999a573

**完整 Commit Message**:

```
fix(landing): keep public nav dropdown hoverable (#1896)

## Summary
- Keep public header dropdowns open while moving from the nav trigger
into menu content.
- Preserve the existing visual spacing by making the dropdown hit area
continuous.

## Root cause
The desktop public header uses CSS :hover to reveal dropdown menus. The
menu had margin-top: 4px below the hover container, leaving a small
non-hoverable gap between the trigger and the menu. Crossing that gap
dropped :hover and hid the menu.

## Test plan
- [x] `git diff --check`
- [x] `pnpm -C web/app run lint`
- [x] Local Playwright hover smoke test on `http://localhost:3002/`:
moving from `Learn` to `Getting Started` kept the menu visible.
- [x] Local Playwright hover smoke test on `http://localhost:3002/`:
moving from `Resources` to its first menu item kept the menu visible.
```

**PR Description**:

## Summary
- Keep public header dropdowns open while moving from the nav trigger into menu content.
- Preserve the existing visual spacing by making the dropdown hit area continuous.

## Root cause
The desktop public header uses CSS :hover to reveal dropdown menus. The menu had margin-top: 4px below the hover container, leaving a small non-hoverable gap between the trigger and the menu. Crossing that gap dropped :hover and hid the menu.

## Test plan
- [x] `git diff --check`
- [x] `pnpm -C web/app run lint`
- [x] Local Playwright hover smoke test on `http://localhost:3002/`: moving from `Learn` to `Getting Started` kept the menu visible.
- [x] Local Playwright hover smoke test on `http://localhost:3002/`: moving from `Resources` to its first menu item kept the menu visible.

---

