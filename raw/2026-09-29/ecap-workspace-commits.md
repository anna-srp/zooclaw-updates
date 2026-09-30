# SerendipityOneInc/ecap-workspace — commits 2026-09-29

## feat(platform): migrate login to ZooWork account (#3937)

- **SHA**: `30366148b1950766181418125e30f03ef5fef01f`
- **作者**: finn-srp
- **日期**: 2026-09-29T16:13:06Z
- **PR**: #3937

### Commit Message

```
feat(platform): migrate login to ZooWork account (#3937)

## Summary

- Replace Platform Clerk login with user-interface email OTP and Google
login using `business=ecap-platform`. Interface verifies the account JWT
and uses the verified UID.
- Give each UID one personal Platform Organization for Project and API
key isolation. Reuse the existing `platform_users` and
`platform_organizations` collection names. The disposable Clerk-era
staging records and unique indexes must be cleaned before rollout.
- Keep the previous Organization-wallet billing routes disabled and show
a pending Billing page. UID billing, top-ups, metering and API key
runtime access remain follow-up work.
- Update the Platform deployment workflow to use the account, Interface
and Firebase browser configuration.
- Remove the old `/auth/callback` route. Platform was only released to
staging, so the login cutover does not preserve compatibility for cached
Clerk clients; a stale staging tab can reload the new entry page.

## Validation

- Dev login was tested by the requester. A local `/bootstrap` 500 seen
during testing came from a temporary test adapter missing `read`; it was
unrelated to legacy Project ownership.
- Platform on Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (19
passed), `pnpm build` all passed.
- Interface: `ecap-verify-py-ci` passed with 13,041 tests passed, 5
skipped and 89.83% coverage; dependency, lint and duplication checks
passed.

## Rollout

- Deploy backend and frontend together after staging cleanup of the old
Platform Clerk data and unique indexes. This PR does not run that
cleanup or deploy either service.
- Keep `PLATFORM_UID_BILLING_ENABLED=false`; this PR does not enable
Platform API keys for runtime requests.

## Review note

The PR changes 3,940 lines under the repository size rule, including
3,160 deleted lines from the old Clerk UI and tests. `size-override` is
requested for this single login migration.
```

### PR Body

## Summary

- Replace Platform Clerk login with user-interface email OTP and Google login using `business=ecap-platform`. Interface verifies the account JWT and uses the verified UID.
- Give each UID one personal Platform Organization for Project and API key isolation. Reuse the existing `platform_users` and `platform_organizations` collection names. The disposable Clerk-era staging records and unique indexes must be cleaned before rollout.
- Keep the previous Organization-wallet billing routes disabled and show a pending Billing page. UID billing, top-ups, metering and API key runtime access remain follow-up work.
- Update the Platform deployment workflow to use the account, Interface and Firebase browser configuration.
- Remove the old `/auth/callback` route. Platform was only released to staging, so the login cutover does not preserve compatibility for cached Clerk clients; a stale staging tab can reload the new entry page.

## Validation

- Dev login was tested by the requester. A local `/bootstrap` 500 seen during testing came from a temporary test adapter missing `read`; it was unrelated to legacy Project ownership.
- Platform on Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (19 passed), `pnpm build` all passed.
- Interface: `ecap-verify-py-ci` passed with 13,041 tests passed, 5 skipped and 89.83% coverage; dependency, lint and duplication checks passed.

## Rollout

- Deploy backend and frontend together after staging cleanup of the old Platform Clerk data and unique indexes. This PR does not run that cleanup or deploy either service.
- Keep `PLATFORM_UID_BILLING_ENABLED=false`; this PR does not enable Platform API keys for runtime requests.

## Review note

The PR changes 3,940 lines under the repository size rule, including 3,160 deleted lines from the old Clerk UI and tests. `size-override` is requested for this single login migration.

---

## feat(web): update English TDK for homepage, /solutions and /about (#3932)

- **SHA**: `15a8f3488511af85766d59e0999ff1a32b8d8e98`
- **作者**: Mori-srp
- **日期**: 2026-09-29T15:08:21Z
- **PR**: #3932

### Commit Message

```
feat(web): update English TDK for homepage, /solutions and /about (#3932)

English-only TDK update for the marketing site, based on the SEO
vendor's keyword recommendations (approved by 徐老师).

- `/`: title `AI Agent Platform to Build, Deploy & Run AI Agents |
ZooWork`, new description
- `/solutions`: title `AI Agents for Business | ZooWork Solutions`, new
description (new `solutions-seo.ts`)
- `/about`: title `About Serendipity One, the Company Behind ZooWork |
ZooWork` (absolute title, so HTML/OG/Twitter titles match with no
doubled suffix)
- `_seo.ts`: new optional `absoluteTitle`

zh/ja and all other locales unchanged. Tests: unit (app / lib/seo /
theme) pass, lint, tsc, knip pass. New test covers the /about metadata
titles.

Needs a human review before merge.
```

### PR Body

English-only TDK update for the marketing site, based on the SEO vendor's keyword recommendations (approved by 徐老师).

- `/`: title `AI Agent Platform to Build, Deploy & Run AI Agents | ZooWork`, new description
- `/solutions`: title `AI Agents for Business | ZooWork Solutions`, new description (new `solutions-seo.ts`)
- `/about`: title `About Serendipity One, the Company Behind ZooWork | ZooWork` (absolute title, so HTML/OG/Twitter titles match with no doubled suffix)
- `_seo.ts`: new optional `absoluteTitle`

zh/ja and all other locales unchanged. Tests: unit (app / lib/seo / theme) pass, lint, tsc, knip pass. New test covers the /about metadata titles.

Needs a human review before merge.

---

## fix(onboarding): preserve checkout during verification failures (#3936)

- **SHA**: `cd905d00775939b723098c5d29e61d14f6eee017`
- **作者**: ericma-srp
- **日期**: 2026-09-29T14:54:32Z
- **PR**: #3936

### Commit Message

```
fix(onboarding): preserve checkout during verification failures (#3936)

## Problem and behavior

After a new user opens Stripe and returns to ZooWork, a failed
background admission request currently unmounts onboarding and replaces
the checkout screen with a full-page error. Keep the known-unpaid user's
plan and Continue checkout action mounted, show verification retry in
the plan, and leave protected workspace content blocked until fresh
server evidence permits admission.

The provider and workspace gate now share the same error-display
decision. Cached, UID-matched account identity may preserve checkout
presentation, but cannot grant workspace access or skip the existing
completion-time verification. Initial unresolved verification and
explicit rejection of previously admitted users retain blocking
recovery. Polling frequency, payment evidence and backend behavior are
unchanged.

## Validation

- Four regression cases fail against the previous implementation; 361
relevant unit/integration tests pass after the fix.
- TypeScript, changed-file ESLint, frontend governance guards and full
pre-commit ESLint pass.
- Two local Chromium checkout cases pass with actual
Provider/Modal/query logic and mocked HTTP: open HTTPS checkout popup,
return after account or order 503s, keep checkout usable, retry without
extra orders or premature completion, then admit after confirmed order
evidence. Screenshots inspected.
- All 13 existing admission/loading browser cases also pass, including
desktop/mobile entry, initial errors/recovery, anonymous/unpaid
protection and paid users.
- Real Stripe payment and the original production request failure were
not reproduced.

## #3901 polling audit

Only one 3-second loop was introduced, owned by OnboardingProvider via
useOnboardingAdmission. Other consumers share its UID-scoped query
without enabling their own interval. It reads account/me, then personal
orders when needed; active team admins can additionally read team orders
and enterprise credits evidence. It begins whenever a protected-page
user resolves unpaid, even before Stripe is opened. Focus/mount,
checkout-open and completion checks are event-triggered; the 15-second
transient-error recovery was added later by #3916. These reads do not
create orders or confirm Stripe sessions.

## Review follow-up

Codex and Claude both approve. Claude's non-blocking account-error
observation does not introduce a new checkout-skip restriction:
previously account.isError forced audience=null, which already prevented
skipping checkout. The new explicit !account.isError preserves that
condition while cached identity now allows known-unpaid checkout to
remain usable. Both account observers use accountSessionKeys.me(uid),
rather than independent account caches. No expansion to paid-user error
policy is needed for this fix.
```

### PR Body

## Problem and behavior

After a new user opens Stripe and returns to ZooWork, a failed background admission request currently unmounts onboarding and replaces the checkout screen with a full-page error. Keep the known-unpaid user's plan and Continue checkout action mounted, show verification retry in the plan, and leave protected workspace content blocked until fresh server evidence permits admission.

The provider and workspace gate now share the same error-display decision. Cached, UID-matched account identity may preserve checkout presentation, but cannot grant workspace access or skip the existing completion-time verification. Initial unresolved verification and explicit rejection of previously admitted users retain blocking recovery. Polling frequency, payment evidence and backend behavior are unchanged.

## Validation

- Four regression cases fail against the previous implementation; 361 relevant unit/integration tests pass after the fix.
- TypeScript, changed-file ESLint, frontend governance guards and full pre-commit ESLint pass.
- Two local Chromium checkout cases pass with actual Provider/Modal/query logic and mocked HTTP: open HTTPS checkout popup, return after account or order 503s, keep checkout usable, retry without extra orders or premature completion, then admit after confirmed order evidence. Screenshots inspected.
- All 13 existing admission/loading browser cases also pass, including desktop/mobile entry, initial errors/recovery, anonymous/unpaid protection and paid users.
- Real Stripe payment and the original production request failure were not reproduced.

## #3901 polling audit

Only one 3-second loop was introduced, owned by OnboardingProvider via useOnboardingAdmission. Other consumers share its UID-scoped query without enabling their own interval. It reads account/me, then personal orders when needed; active team admins can additionally read team orders and enterprise credits evidence. It begins whenever a protected-page user resolves unpaid, even before Stripe is opened. Focus/mount, checkout-open and completion checks are event-triggered; the 15-second transient-error recovery was added later by #3916. These reads do not create orders or confirm Stripe sessions.

## Review follow-up

Codex and Claude both approve. Claude's non-blocking account-error observation does not introduce a new checkout-skip restriction: previously account.isError forced audience=null, which already prevented skipping checkout. The new explicit !account.isError preserves that condition while cached identity now allows known-unpaid checkout to remain usable. Both account observers use accountSessionKeys.me(uid), rather than independent account caches. No expansion to paid-user error policy is needed for this fix.

---

## feat(pricing): refresh plan comparison and limited offer messaging (#3934)

- **SHA**: `d01352eb67f819067c7ffcc8c9b4287a254dafbf`
- **作者**: ericma-srp
- **日期**: 2026-09-29T14:19:17Z
- **PR**: #3934

### Commit Message

```
feat(pricing): refresh plan comparison and limited offer messaging (#3934)

## Summary
- Refresh the pricing comparison with continuous Pro and Enterprise
columns, clearer feature groups, larger CTAs, and English-only serif
taglines. Update copy across all 10 locales.
- Highlight the limited offer and 70% savings in red. Show 6,000 credits
plus 14,000 bonus credits with a limited-time footnote, and add a shared
additional-credits row.
- Align the Manage plan dialog with the pricing page: display `6k + 14k
bonus credits/mo*` and a 14k limited-time monthly bonus footnote.
- Remove the unavailable-offer notice and route both Contact Sales
buttons to https://zoowork.ai/enterprise.
- Frontend only: no backend, API, database, billing, catalog, or
credit-issuance changes. The existing Pro sign-up handoff remains
unchanged; this does not enable promotional checkout.
- Localize the Chinese monthly-credit and limited-time bonus copy,
retaining `credits` as a product term: `6000 credits + 赠送 14000
credits*` and `*每月额外赠送 14000 credits，限时有效。`.
- Preserve accessible associations between each benefit cell, its
feature name, and its applicable plan header(s), including the shared
additional-credits row.

## Test plan
- [x] Frontend governance guards, TypeScript, and ESLint passed after
syncing the latest main.
- [x] 55 initial targeted tests passed across pricing comparison,
pricing typography, marketing chrome, and locale completeness; the
pricing suite was rerun with a new regression test for table header
associations.
- [x] Browser checks passed for all 10 locales at 1440, 1024, 390, and
320 px, with no overflow or page errors.
- [x] Verified both Contact Sales buttons navigate to the Enterprise
page.
- [x] Reviewed English and Chinese desktop/mobile previews.
- [x] Credit-split follow-up: all 61 tests passed across pricing
rendering, locale completeness, Manage plan dialog, and Pro plan
actions. Verified old 8k/12k offer copy is absent from both frontend
surfaces.
- [x] GitHub Actions on `3cb79a589`: frontend build, lint/typecheck,
full tests, and CodeQL passed; both automated reviewers reported no new
issues.

## Review follow-up
- Fixed the screen-reader row-header association regression and added
coverage.
- Localized the Chinese bonus message and footnote while preserving
`credits`; updated the rendering and accessible-description assertions
for each language. Unused `scrollHint` translation keys remain as a
harmless cleanup item with no runtime effect. Manage plan keeps its
existing English presentation; broader dialog localization is a
pre-existing follow-up, outside this display-number correction.
```

### PR Body

## Summary
- Refresh the pricing comparison with continuous Pro and Enterprise columns, clearer feature groups, larger CTAs, and English-only serif taglines. Update copy across all 10 locales.
- Highlight the limited offer and 70% savings in red. Show 6,000 credits plus 14,000 bonus credits with a limited-time footnote, and add a shared additional-credits row.
- Align the Manage plan dialog with the pricing page: display `6k + 14k bonus credits/mo*` and a 14k limited-time monthly bonus footnote.
- Remove the unavailable-offer notice and route both Contact Sales buttons to https://zoowork.ai/enterprise.
- Frontend only: no backend, API, database, billing, catalog, or credit-issuance changes. The existing Pro sign-up handoff remains unchanged; this does not enable promotional checkout.
- Localize the Chinese monthly-credit and limited-time bonus copy, retaining `credits` as a product term: `6000 credits + 赠送 14000 credits*` and `*每月额外赠送 14000 credits，限时有效。`.
- Preserve accessible associations between each benefit cell, its feature name, and its applicable plan header(s), including the shared additional-credits row.

## Test plan
- [x] Frontend governance guards, TypeScript, and ESLint passed after syncing the latest main.
- [x] 55 initial targeted tests passed across pricing comparison, pricing typography, marketing chrome, and locale completeness; the pricing suite was rerun with a new regression test for table header associations.
- [x] Browser checks passed for all 10 locales at 1440, 1024, 390, and 320 px, with no overflow or page errors.
- [x] Verified both Contact Sales buttons navigate to the Enterprise page.
- [x] Reviewed English and Chinese desktop/mobile previews.
- [x] Credit-split follow-up: all 61 tests passed across pricing rendering, locale completeness, Manage plan dialog, and Pro plan actions. Verified old 8k/12k offer copy is absent from both frontend surfaces.
- [x] GitHub Actions on `3cb79a589`: frontend build, lint/typecheck, full tests, and CodeQL passed; both automated reviewers reported no new issues.

## Review follow-up
- Fixed the screen-reader row-header association regression and added coverage.
- Localized the Chinese bonus message and footnote while preserving `credits`; updated the rendering and accessible-description assertions for each language. Unused `scrollHint` translation keys remain as a harmless cleanup item with no runtime effect. Manage plan keeps its existing English presentation; broader dialog localization is a pre-existing follow-up, outside this display-number correction.

---

## feat(billing): support Stripe promotion codes for credits topups (#3931)

- **SHA**: `dbf7ef485ee9e350558df676fa7202076bc3e7c6`
- **作者**: tim-srp
- **日期**: 2026-09-29T12:00:32Z
- **PR**: #3931

### Commit Message

```
feat(billing): support Stripe promotion codes for credits topups (#3931)

## Linear
<!-- none -->

## Summary
Credits topup Checkout now accepts Stripe promotion codes, following the
Pro promotion-code design (#3891). Stripe owns code eligibility,
discount, redemption limits and applicable products; there is no local
issuance.

- A discount lowers only the amount paid; every verified topup grants
the order's full `credits_amount`. The list price is derived from the
server-fixed credits (`credits / 2` cents), never from Stripe or the
(possibly already-settled) order amount.
- `checkout.session.completed`: verifies USD, `amount_subtotal == list`,
`total_details.amount_discount` in `[0, list]`, zero tax/shipping and
`amount_total == list - discount`. A positive total requires `paid` plus
a PaymentIntent; a zero total requires no PaymentIntent.
- `payment_intent.succeeded` arriving first with a lower amount re-reads
the order's Checkout Session and requires the same PaymentIntent and
verified amount. Undiscounted or already-settled PaymentIntents keep the
existing exact-amount check.
- `invoice.paid` attaches when `amount_paid + discounts == list`, with
no tax or credit notes. The order must still carry the list price before
settlement, or exactly the paid amount after.
- The payment order records the actual paid amount (including 0) and
`provider_discount_amount_cents`; existing `payment_order.recorded`
audit events carry before/after values of both.
- **100% codes are allowed.** The entitlement guard admits a zero amount
for a topup only when it is a current-policy Stripe USD topup,
Checkout-sourced, with a Session, no PaymentIntent and a discount equal
to the list price. A $0 topup has no charge, so Stripe refunds cannot
revoke its credits; reversal must use the audited manual compensation
flow. Coupon product and redemption limits in Stripe are the control.
- API Platform accounts share the same topup Checkout, so they also see
the promotion-code field.
- Legacy topups, subscriptions and billing-gateway are unchanged. No new
env vars, DB queries or jobs.
- Spec:
`docs/superpowers/specs/2026-09-29-stripe-topup-promotion-codes.md`; ops
notes in `services/claw-interface/docs/stripe-credits-v1.md` (充值优惠码).

## Test plan
- [x] New `tests/unit/test_stripe_topup_promotion_codes.py` (58 cases):
partial/full discount Sessions, malformed or mismatched Sessions,
PaymentIntent-first discounted delivery, invoice attachment before/after
settlement, zero-amount guard not relaxing other orders, full-credit
grant for $0 without a payment lookup.
- [x] Billing, Stripe, order, credit and Feishu unit suites locally
(3363 passed).
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, import-linter)
and ci-lint guards (file length, complexity, dead code).
- [ ] Stripe Sandbox acceptance: partial and 100% codes, real
Session/invoice shape for $0 payment mode, webhook ordering. Not covered
by unit tests.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body

## Linear
<!-- none -->

## Summary
Credits topup Checkout now accepts Stripe promotion codes, following the Pro promotion-code design (#3891). Stripe owns code eligibility, discount, redemption limits and applicable products; there is no local issuance.

- A discount lowers only the amount paid; every verified topup grants the order's full `credits_amount`. The list price is derived from the server-fixed credits (`credits / 2` cents), never from Stripe or the (possibly already-settled) order amount.
- `checkout.session.completed`: verifies USD, `amount_subtotal == list`, `total_details.amount_discount` in `[0, list]`, zero tax/shipping and `amount_total == list - discount`. A positive total requires `paid` plus a PaymentIntent; a zero total requires no PaymentIntent.
- `payment_intent.succeeded` arriving first with a lower amount re-reads the order's Checkout Session and requires the same PaymentIntent and verified amount. Undiscounted or already-settled PaymentIntents keep the existing exact-amount check.
- `invoice.paid` attaches when `amount_paid + discounts == list`, with no tax or credit notes. The order must still carry the list price before settlement, or exactly the paid amount after.
- The payment order records the actual paid amount (including 0) and `provider_discount_amount_cents`; existing `payment_order.recorded` audit events carry before/after values of both.
- **100% codes are allowed.** The entitlement guard admits a zero amount for a topup only when it is a current-policy Stripe USD topup, Checkout-sourced, with a Session, no PaymentIntent and a discount equal to the list price. A $0 topup has no charge, so Stripe refunds cannot revoke its credits; reversal must use the audited manual compensation flow. Coupon product and redemption limits in Stripe are the control.
- API Platform accounts share the same topup Checkout, so they also see the promotion-code field.
- Legacy topups, subscriptions and billing-gateway are unchanged. No new env vars, DB queries or jobs.
- Spec: `docs/superpowers/specs/2026-09-29-stripe-topup-promotion-codes.md`; ops notes in `services/claw-interface/docs/stripe-credits-v1.md` (充值优惠码).

## Test plan
- [x] New `tests/unit/test_stripe_topup_promotion_codes.py` (58 cases): partial/full discount Sessions, malformed or mismatched Sessions, PaymentIntent-first discounted delivery, invoice attachment before/after settlement, zero-amount guard not relaxing other orders, full-credit grant for $0 without a payment lookup.
- [x] Billing, Stripe, order, credit and Feishu unit suites locally (3363 passed).
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, import-linter) and ci-lint guards (file length, complexity, dead code).
- [ ] Stripe Sandbox acceptance: partial and 100% codes, real Session/invoice shape for $0 payment mode, webhook ordering. Not covered by unit tests.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(web): 修复官网 Resources 菜单交互并精简入口 (#3929)

- **SHA**: `faa0dfbd4b662210657878af7fac43afb42b10f0`
- **作者**: lynn Zhuang
- **日期**: 2026-09-29T09:56:22Z
- **PR**: #3929

### Commit Message

```
fix(web): 修复官网 Resources 菜单交互并精简入口 (#3929)

## 问题与修改

官网导航中的 Resources 虽然有下拉菜单，但标题仍是外链，点击后会直接打开
Tips。改为按钮，点击展开或收起菜单，并支持点击外部、失焦和 Escape 关闭。

移除 Resources 下拉菜单中的 Learn 和 What’s New，仅保留
Blog、Docs、ZooData，同时让菜单高度随内容收缩。首页、Pricing 等页面共用导航，统一生效。Solutions
的链接行为及页脚入口保持不变。

## 验证

- 14 个相关单元测试通过，覆盖点击切换、焦点顺序、Escape、外部点击及菜单内容。
- TypeScript、修改文件的 ESLint、仓库前端治理检查通过。
- `git diff --check` 通过。
- 本地首页返回 HTTP 200；浏览器交互验证因用户正在操作 Chrome 而中断，未完成实测。
```

### PR Body

## 问题与修改

官网导航中的 Resources 虽然有下拉菜单，但标题仍是外链，点击后会直接打开 Tips。改为按钮，点击展开或收起菜单，并支持点击外部、失焦和 Escape 关闭。

移除 Resources 下拉菜单中的 Learn 和 What’s New，仅保留 Blog、Docs、ZooData，同时让菜单高度随内容收缩。首页、Pricing 等页面共用导航，统一生效。Solutions 的链接行为及页脚入口保持不变。

## 验证

- 14 个相关单元测试通过，覆盖点击切换、焦点顺序、Escape、外部点击及菜单内容。
- TypeScript、修改文件的 ESLint、仓库前端治理检查通过。
- `git diff --check` 通过。
- 本地首页返回 HTTP 200；浏览器交互验证因用户正在操作 Chrome 而中断，未完成实测。

---

## fix(onboarding): admit all effective Pro entitlements (#3924)

- **SHA**: `9cbeac6b651a24d73e7be2558a53dccf0687019f`
- **作者**: ericma-srp
- **日期**: 2026-09-29T09:36:47Z
- **PR**: #3924

### Commit Message

```
fix(onboarding): admit all effective Pro entitlements (#3924)

## Problem and behavior
After #3901, effective Pro users granted access without a payment
provider could be forced into Stripe onboarding. Every effective,
unexpired Pro entitlement (server status `active` or `trial`) now skips
Stripe, regardless of its source: subscription code, manual adjustment,
server-confirmed trial or payment. The same shared rule preserves the
supported Starter/Ultra tiers.

A server-resolved Pro account with no card, code, paid cycles or orders
can finish onboarding, refresh and open protected workspace routes.
Access is fetched again before onboarding completion is saved. An
expired or incomplete grant is not accepted merely because its plan says
Pro.

## Implementation
- Share the active/trial status + supported plan + future finite expiry
predicate between onboarding admission and card-binding/send prompts. Do
not enumerate source types or require a code/source id.
- Reuse `/account/me`'s current-access projection for admission and
billing initialization; use `billing_summary.current_access` for credits
checks. Team/legacy credits responses without a summary use their
existing resolved status/plan/expiry fields. A present summary takes
precedence over flat fields.
- All admitted personal/team users skip the Stripe plan step, without
catalog, order or popup creation. Preserve the existing paid-history,
invited-member and legacy enterprise admission paths.
- Keep payment-provider identity unchanged; no personal entitlement is
injected into team billing responses.

## Validation
- Four admission/modal regression tests fail on the previous code for
valid Pro accounts without a subscription code or provider.
- 409 targeted unit/integration tests across 22 files passed, including
manual Pro, code/card parity, zero credits, billing initialization,
invalid status/expiry, summary precedence and expiry immediately before
completion.
- TypeScript, ESLint and frontend governance guards passed.
- Chromium: all 6 personal scenarios passed (code, card, manual grant,
valid Pro trial, expired code, expired trial). Verified completion
retry, refresh and direct `/home`, `/identity`, `/agents`; zero
catalog/order/popup for admitted users.
- Three additional trial admission/modal regressions failed before the
status update and pass afterward, including expiry during completion.
- CI settled on `4b4179155`: 23 checks passed, 16 skipped, no failures.
Full frontend tests, production build, lint/typecheck, CodeQL and review
gates passed.
- Claude and Codex re-reviews both APPROVE, with no new inline findings.
Claude explicitly confirms both Tim comments (providerless grants and
effective Pro trials) are addressed. Its optional suggestion to share
expiry logic with the legacy enterprise branch is left unchanged: this
is a pre-existing duplication, not a defect or necessary part of this
fix.
- Local API fixtures only: no live grant/redemption, production payment,
deployment or merge.

## Review resolution
Tim's P1 and subsequent P2 are addressed: valid Pro trials are
explicitly included under the user's all-effective-Pro rule. A trial
status alone, free plan, missing/invalid expiry or expired trial remains
insufficient. Completion re-verification covers a trial expiring
mid-flow. Access continues to be based on the effective server-resolved
entitlement.

Original P1: access is based on the effective server-resolved
entitlement, not its acquisition source. The personal skip-checkout
behavior is explicitly intended by the user. Earlier team-summary
feedback is handled using the team's own resolved fields when no summary
is returned, preserving the personal/team billing boundary.

Frontend only: no backend, BFF, dependencies or lockfile changes. Based
on main `5c3a5d973`, including #3916 (merge `2cdfd5ce9`); its shared
account query, retries and initial loading optimizations are preserved.
```

### PR Body

## Problem and behavior
After #3901, effective Pro users granted access without a payment provider could be forced into Stripe onboarding. Every effective, unexpired Pro entitlement (server status `active` or `trial`) now skips Stripe, regardless of its source: subscription code, manual adjustment, server-confirmed trial or payment. The same shared rule preserves the supported Starter/Ultra tiers.

A server-resolved Pro account with no card, code, paid cycles or orders can finish onboarding, refresh and open protected workspace routes. Access is fetched again before onboarding completion is saved. An expired or incomplete grant is not accepted merely because its plan says Pro.

## Implementation
- Share the active/trial status + supported plan + future finite expiry predicate between onboarding admission and card-binding/send prompts. Do not enumerate source types or require a code/source id.
- Reuse `/account/me`'s current-access projection for admission and billing initialization; use `billing_summary.current_access` for credits checks. Team/legacy credits responses without a summary use their existing resolved status/plan/expiry fields. A present summary takes precedence over flat fields.
- All admitted personal/team users skip the Stripe plan step, without catalog, order or popup creation. Preserve the existing paid-history, invited-member and legacy enterprise admission paths.
- Keep payment-provider identity unchanged; no personal entitlement is injected into team billing responses.

## Validation
- Four admission/modal regression tests fail on the previous code for valid Pro accounts without a subscription code or provider.
- 409 targeted unit/integration tests across 22 files passed, including manual Pro, code/card parity, zero credits, billing initialization, invalid status/expiry, summary precedence and expiry immediately before completion.
- TypeScript, ESLint and frontend governance guards passed.
- Chromium: all 6 personal scenarios passed (code, card, manual grant, valid Pro trial, expired code, expired trial). Verified completion retry, refresh and direct `/home`, `/identity`, `/agents`; zero catalog/order/popup for admitted users.
- Three additional trial admission/modal regressions failed before the status update and pass afterward, including expiry during completion.
- CI settled on `4b4179155`: 23 checks passed, 16 skipped, no failures. Full frontend tests, production build, lint/typecheck, CodeQL and review gates passed.
- Claude and Codex re-reviews both APPROVE, with no new inline findings. Claude explicitly confirms both Tim comments (providerless grants and effective Pro trials) are addressed. Its optional suggestion to share expiry logic with the legacy enterprise branch is left unchanged: this is a pre-existing duplication, not a defect or necessary part of this fix.
- Local API fixtures only: no live grant/redemption, production payment, deployment or merge.

## Review resolution
Tim's P1 and subsequent P2 are addressed: valid Pro trials are explicitly included under the user's all-effective-Pro rule. A trial status alone, free plan, missing/invalid expiry or expired trial remains insufficient. Completion re-verification covers a trial expiring mid-flow. Access continues to be based on the effective server-resolved entitlement.

Original P1: access is based on the effective server-resolved entitlement, not its acquisition source. The personal skip-checkout behavior is explicitly intended by the user. Earlier team-summary feedback is handled using the team's own resolved fields when no summary is returned, preserving the personal/team billing boundary.

Frontend only: no backend, BFF, dependencies or lockfile changes. Based on main `5c3a5d973`, including #3916 (merge `2cdfd5ce9`); its shared account query, retries and initial loading optimizations are preserved.

---

## fix(agents): authorize Codex subscriptions for Builder runtimes (#3927)

- **SHA**: `73c2dab16c15a4df4918647a223931dc9366096b`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-29T09:02:01Z
- **PR**: #3927

### Commit Message

```
fix(agents): authorize Codex subscriptions for Builder runtimes (#3927)

## Summary

Builder Agents can select a connected personal Codex model even when
their Engine runtime uses an opaque UID/org. After checking the
authenticated owner's connection and discovered model, authorize that
exact workspace runtime before saving the model. Apply the same
authorization to source creation, Revision commits and shared-source
updates. Ordinary and baseline-backed Agents retain the same-owner path.

Companion: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1761

## Root cause

ECAP validates the real subscription owner, but Builder creates Agents
under a workspace-derived runtime principal. Engine previously treated
that runtime principal as the subscription owner and returned `409
codex_reauth_required` despite a connected account. The companion adds
explicit connection/runtime authorization for rendering and inference;
this PR supplies only server-derived target identities after existing
access checks. Editable source and browser requests cannot select a
grant target.

## Test plan

- [x] Focused subscription/model/authoring regression selection: 103
passed.
- [x] Builder creation/shared-update/apply selection, including two new
source-creation tests: 71 passed. Selections overlap.
- [x] `bash scripts/verify-py.sh`: ruff, formatting, pyright, all eight
import contracts passed; commit hooks passed.
- [x] Real EngineClient HTTP serialization: real-owner lookup, opaque
runtime authorization before model save, unchanged ordinary/baseline
behavior, and refusal before saving on failed authorization.
- [ ] Full suite is delegated to CI. No live user Agent/connection was
mutated; live provider smoke is not claimed.

## Deployment

Deploy the companion Engine migrations, controld and workers before this
backend. Existing Builder Agents establish grants when their owners
retry model selection; no account reconnect, identity rewrite or
historical-data repair is needed. The separate API-model/sandbox-tier
issue is outside this PR.

The runtime identity concept entered main with ECAP #3673 on 2026-09-09
(development began 2026-09-04); these dates are not rollout timestamps.
```

### PR Body

## Summary

Builder Agents can select a connected personal Codex model even when their Engine runtime uses an opaque UID/org. After checking the authenticated owner's connection and discovered model, authorize that exact workspace runtime before saving the model. Apply the same authorization to source creation, Revision commits and shared-source updates. Ordinary and baseline-backed Agents retain the same-owner path.

Companion: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1761

## Root cause

ECAP validates the real subscription owner, but Builder creates Agents under a workspace-derived runtime principal. Engine previously treated that runtime principal as the subscription owner and returned `409 codex_reauth_required` despite a connected account. The companion adds explicit connection/runtime authorization for rendering and inference; this PR supplies only server-derived target identities after existing access checks. Editable source and browser requests cannot select a grant target.

## Test plan

- [x] Focused subscription/model/authoring regression selection: 103 passed.
- [x] Builder creation/shared-update/apply selection, including two new source-creation tests: 71 passed. Selections overlap.
- [x] `bash scripts/verify-py.sh`: ruff, formatting, pyright, all eight import contracts passed; commit hooks passed.
- [x] Real EngineClient HTTP serialization: real-owner lookup, opaque runtime authorization before model save, unchanged ordinary/baseline behavior, and refusal before saving on failed authorization.
- [ ] Full suite is delegated to CI. No live user Agent/connection was mutated; live provider smoke is not claimed.

## Deployment

Deploy the companion Engine migrations, controld and workers before this backend. Existing Builder Agents establish grants when their owners retry model selection; no account reconnect, identity rewrite or historical-data repair is needed. The separate API-model/sandbox-tier issue is outside this PR.

The runtime identity concept entered main with ECAP #3673 on 2026-09-09 (development began 2026-09-04); these dates are not rollout timestamps.

---

## feat(billing): 优化用量页面并完善订阅管理入口 (#3895)

- **SHA**: `a57dc72e6cc29522525e8584febf598ff53d5037`
- **作者**: shana-srp
- **日期**: 2026-09-29T08:24:09Z
- **PR**: #3895

### Commit Message

```
feat(billing): 优化用量页面并完善订阅管理入口 (#3895)

## 改动说明


优化设置中的用量页面：将剩余积分、充值积分和当前套餐整理为三列概览，统一时间范围控件、统计图表和明细表格，改善字体、对比度与深色模式。移除重复标题及计算资源摘要，保留原有积分计算、查询、筛选和分页能力。

统一订阅管理入口：仍有效的 Stripe 订阅通过客户门户管理和取消；已结束的 Stripe
订阅保留“激活”入口，进入现有套餐购买流程。符合条件的非 Stripe 订阅在 Usage 与 Billing
均保留“管理”和“取消”，取消仍通过既有确认流程。Billing 页面也复用这套操作，保留非 Stripe
套餐管理按钮，修复从套餐选择弹窗移除取消按钮后，Billing 页面没有取消入口的问题。Apple、旧版
Creem、团队及权限限制沿用现有规则。

调整套餐展示与选择弹窗：Pro 不再附加套餐后缀，已结束订阅显示 Free，并在有数据时展示结束日期；优化深色 Pro
卡片、购买按钮和间距，隐藏侧栏手机入口，移除托管运行时/API 权益文案。

## 本次修复

- 按 [Tim
的确认框评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5886168682)，将取消确认框改为设计系统独立
AlertDialog，提供标题/描述语义、自动聚焦、焦点约束与关闭后焦点恢复；取消成功导致原入口移除时，焦点回到可用的管理操作。
- 取消请求处理中保持确认框打开，禁用重复提交、关闭按钮及 Escape 关闭；默认聚焦“保留订阅”。新增键盘与可访问性测试，覆盖
Tab/Shift+Tab 循环、背景焦点隔离、退出与成功后的焦点恢复。

- 按 [Tim
第二轮评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5885536252)
修复“取消 → 续订 →
再次取消”的状态同步：服务端确认取消后清除本地临时标记，后续续订刷新重新恢复取消入口并移除旧提示；服务端确认前继续保留临时取消保护。
- 新增使用真实订阅 action/lifecycle hooks 的回归测试，覆盖 Usage/Billing
全程不卸载的连续操作，确认第二次取消实际调用接口，并覆盖服务端延迟确认。

- 按 [Tim
的评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5885192183)
恢复已结束 Stripe 订阅的重新购买入口，并在 Usage 页面保留非 Stripe 套餐管理按钮。
- 新增跨组件回归测试，从 Usage/Billing 的激活入口进入真实套餐弹窗，再点击
Resubscribe，确认触发订阅购买；管理与取消分别验证各自回调。

- 合入最新 main，解决用量明细组件冲突，保留游标分页、快照、归属筛选与服务端时间窗口，同时保留界面本地化。
- 补回 Billing 页面的取消确认入口；Stripe 管理及已预约取消后的管理统一进入客户门户。
- 新增默认账单卡片回归测试，覆盖 Card/Antom 的取消入口、保留套餐管理，以及 Stripe 的门户跳转。

## 验证

- 前端治理检查、TypeScript 类型检查及全部改动 TS/TSX 文件的 ESLint 检查通过。
- 7 个相关单元测试文件、87 条用例通过；按 Tim 反馈修复后，相关 59 条用例通过；第二轮状态同步修复后，3 个相关测试文件、62
条用例通过；本轮确认框改动后上述 62 条仍通过，并新增 4 条可访问性用例通过。
- 覆盖用量游标/快照分页、归属筛选、订阅操作、日期回退、套餐弹窗及设置页面回调。
- 未执行真实付款、取消订阅或权益变更；本轮未运行浏览器视觉验证。构建和完整测试由 CI 验证。

## 自动检查与评审说明

最新提交 `593a952f0` 已获得 [Codex
review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#pullrequestreview-5349630629)
和 [Claude
review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5886365152)，未发现问题。GitHub
CI 已全部通过（不适用检查正常跳过），包括完整前端测试与构建。

此前保留 Usage 非 Stripe 场景“仅取消”的处理已按 Tim 的反馈修正：两处页面均同时保留管理与取消入口。`Free`
继续按原设计文档作为套餐名称展示，结束日期等说明文案仍本地化。

## 范围

仅涉及前端，复用现有账单 API。Free 只是已结束订阅的展示标签，不新增免费权益。取消操作从套餐选择弹窗迁移到 Usage 和
Billing 页面。

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
Co-authored-by: lynn-srp <lynn@srp.one>
```

### PR Body

## 改动说明

优化设置中的用量页面：将剩余积分、充值积分和当前套餐整理为三列概览，统一时间范围控件、统计图表和明细表格，改善字体、对比度与深色模式。移除重复标题及计算资源摘要，保留原有积分计算、查询、筛选和分页能力。

统一订阅管理入口：仍有效的 Stripe 订阅通过客户门户管理和取消；已结束的 Stripe 订阅保留“激活”入口，进入现有套餐购买流程。符合条件的非 Stripe 订阅在 Usage 与 Billing 均保留“管理”和“取消”，取消仍通过既有确认流程。Billing 页面也复用这套操作，保留非 Stripe 套餐管理按钮，修复从套餐选择弹窗移除取消按钮后，Billing 页面没有取消入口的问题。Apple、旧版 Creem、团队及权限限制沿用现有规则。

调整套餐展示与选择弹窗：Pro 不再附加套餐后缀，已结束订阅显示 Free，并在有数据时展示结束日期；优化深色 Pro 卡片、购买按钮和间距，隐藏侧栏手机入口，移除托管运行时/API 权益文案。

## 本次修复

- 按 [Tim 的确认框评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5886168682)，将取消确认框改为设计系统独立 AlertDialog，提供标题/描述语义、自动聚焦、焦点约束与关闭后焦点恢复；取消成功导致原入口移除时，焦点回到可用的管理操作。
- 取消请求处理中保持确认框打开，禁用重复提交、关闭按钮及 Escape 关闭；默认聚焦“保留订阅”。新增键盘与可访问性测试，覆盖 Tab/Shift+Tab 循环、背景焦点隔离、退出与成功后的焦点恢复。

- 按 [Tim 第二轮评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5885536252) 修复“取消 → 续订 → 再次取消”的状态同步：服务端确认取消后清除本地临时标记，后续续订刷新重新恢复取消入口并移除旧提示；服务端确认前继续保留临时取消保护。
- 新增使用真实订阅 action/lifecycle hooks 的回归测试，覆盖 Usage/Billing 全程不卸载的连续操作，确认第二次取消实际调用接口，并覆盖服务端延迟确认。

- 按 [Tim 的评审](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5885192183) 恢复已结束 Stripe 订阅的重新购买入口，并在 Usage 页面保留非 Stripe 套餐管理按钮。
- 新增跨组件回归测试，从 Usage/Billing 的激活入口进入真实套餐弹窗，再点击 Resubscribe，确认触发订阅购买；管理与取消分别验证各自回调。

- 合入最新 main，解决用量明细组件冲突，保留游标分页、快照、归属筛选与服务端时间窗口，同时保留界面本地化。
- 补回 Billing 页面的取消确认入口；Stripe 管理及已预约取消后的管理统一进入客户门户。
- 新增默认账单卡片回归测试，覆盖 Card/Antom 的取消入口、保留套餐管理，以及 Stripe 的门户跳转。

## 验证

- 前端治理检查、TypeScript 类型检查及全部改动 TS/TSX 文件的 ESLint 检查通过。
- 7 个相关单元测试文件、87 条用例通过；按 Tim 反馈修复后，相关 59 条用例通过；第二轮状态同步修复后，3 个相关测试文件、62 条用例通过；本轮确认框改动后上述 62 条仍通过，并新增 4 条可访问性用例通过。
- 覆盖用量游标/快照分页、归属筛选、订阅操作、日期回退、套餐弹窗及设置页面回调。
- 未执行真实付款、取消订阅或权益变更；本轮未运行浏览器视觉验证。构建和完整测试由 CI 验证。

## 自动检查与评审说明

最新提交 `593a952f0` 已获得 [Codex review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#pullrequestreview-5349630629) 和 [Claude review：APPROVE](https://github.com/SerendipityOneInc/ecap-workspace/pull/3895#issuecomment-5886365152)，未发现问题。GitHub CI 已全部通过（不适用检查正常跳过），包括完整前端测试与构建。

此前保留 Usage 非 Stripe 场景“仅取消”的处理已按 Tim 的反馈修正：两处页面均同时保留管理与取消入口。`Free` 继续按原设计文档作为套餐名称展示，结束日期等说明文案仍本地化。

## 范围

仅涉及前端，复用现有账单 API。Free 只是已结束订阅的展示标签，不新增免费权益。取消操作从套餐选择弹窗迁移到 Usage 和 Billing 页面。

---

## fix(agents): prepare template runtime offline and speed up creation (#3925)

- **SHA**: `e223aebf96cae97bb2042d0cfa66dd076411e22a`
- **作者**: kaka-srp
- **日期**: 2026-09-29T08:22:18Z
- **PR**: #3925

### Commit Message

```
fix(agents): prepare template runtime offline and speed up creation (#3925)

## Summary

Fixes #3922. Creating an Agent from a prepared template now reuses
immutable shared Skill pins and a prebuilt Environment instead of
uploading Skills and initiating an Environment build in the request.
Local HTTP tests against real staging reduced Amazon Analyst creation
from about 25–29 seconds to 2.8–5.7 seconds (two samples, not a
production latency guarantee).

- Add offline prepare/verify/publish support with immutable runtime
bindings, registry readback and publication CAS. Runtime resource class
follows the account plan; staging Pro Environments were verified at 4
CPU / 4 GiB.
- Reuse offline source validation while retaining payload integrity,
binding/configuration checks, mutable-field validation and model access
checks. Ordinary creation, sharing and editing retain their existing
full validation.
- Preserve Engine's native `.agents/skills -> /skills` link in the
template workspace helper. The repair utility creates a new immutable
template and helper Skill version, preserving existing Agents and other
resource pins.

## Root cause

Template creation synchronously repeated source scans, uploaded each
template Skill and waited on Environment preparation. After moving
resource preparation offline, three full source scans still dominated
request time. The converted template helper also rejected the native
Skill link already created by Engine, preventing workspace
initialization.

## Test plan

- [x] 481 template / Agent development regressions passed during
implementation.
- [x] Independent branch code review: no actionable findings; 109
targeted tests passed.
- [x] Helper repair and template suites: 54 tests passed, including
native/legacy/absent aliases, repeated initialization and conflict
preservation.
- [x] Ruff, formatting, backend Pyright, import-linter and
offline-script Pyright passed; push gate runs changed-surface checks.
- [x] Real staging HTTP + ACP + Mattermost + ACS + Engine + E2B
validation using the authorized test account. Latest repaired-template
sample: create 5.815s, idempotent replay 0.250s; helper ran twice with
exit 0, preserved the native link and user profile, and the run
succeeded.
- [x] Prepared/published eight repaired staging templates; catalog
remains nine including unaffected Deco. Exact registry manifests and
unchanged old sources/bindings were independently read back.

## Rollout and validation limits

Backend-only change; no Engine change or frontend deployment required.
Prepare and verify production template runtime bindings and required
resource-class builds before enabling this backend path for the
production catalog. Templates without a valid prepared binding fail
closed. Production data and deployments have not been changed by this
work.

Existing Agents retain their previous pinned versions. Real
repaired-template business execution covered Amazon Analyst; the other
seven received source-layout checks plus offline registry verification.
Browser UI, cross-account sharing/editing and production preflight were
not rerun in this task.

Design and detailed receipts: [offline runtime
spec](docs/superpowers/specs/2026-09-29-template-offline-runtime.md).
```

### PR Body

## Summary

Fixes #3922. Creating an Agent from a prepared template now reuses immutable shared Skill pins and a prebuilt Environment instead of uploading Skills and initiating an Environment build in the request. Local HTTP tests against real staging reduced Amazon Analyst creation from about 25–29 seconds to 2.8–5.7 seconds (two samples, not a production latency guarantee).

- Add offline prepare/verify/publish support with immutable runtime bindings, registry readback and publication CAS. Runtime resource class follows the account plan; staging Pro Environments were verified at 4 CPU / 4 GiB.
- Reuse offline source validation while retaining payload integrity, binding/configuration checks, mutable-field validation and model access checks. Ordinary creation, sharing and editing retain their existing full validation.
- Preserve Engine's native `.agents/skills -> /skills` link in the template workspace helper. The repair utility creates a new immutable template and helper Skill version, preserving existing Agents and other resource pins.

## Root cause

Template creation synchronously repeated source scans, uploaded each template Skill and waited on Environment preparation. After moving resource preparation offline, three full source scans still dominated request time. The converted template helper also rejected the native Skill link already created by Engine, preventing workspace initialization.

## Test plan

- [x] 481 template / Agent development regressions passed during implementation.
- [x] Independent branch code review: no actionable findings; 109 targeted tests passed.
- [x] Helper repair and template suites: 54 tests passed, including native/legacy/absent aliases, repeated initialization and conflict preservation.
- [x] Ruff, formatting, backend Pyright, import-linter and offline-script Pyright passed; push gate runs changed-surface checks.
- [x] Real staging HTTP + ACP + Mattermost + ACS + Engine + E2B validation using the authorized test account. Latest repaired-template sample: create 5.815s, idempotent replay 0.250s; helper ran twice with exit 0, preserved the native link and user profile, and the run succeeded.
- [x] Prepared/published eight repaired staging templates; catalog remains nine including unaffected Deco. Exact registry manifests and unchanged old sources/bindings were independently read back.

## Rollout and validation limits

Backend-only change; no Engine change or frontend deployment required. Prepare and verify production template runtime bindings and required resource-class builds before enabling this backend path for the production catalog. Templates without a valid prepared binding fail closed. Production data and deployments have not been changed by this work.

Existing Agents retain their previous pinned versions. Real repaired-template business execution covered Amazon Analyst; the other seven received source-layout checks plus offline registry verification. Browser UI, cross-account sharing/editing and production preflight were not rerun in this task.

Design and detailed receipts: [offline runtime spec](docs/superpowers/specs/2026-09-29-template-offline-runtime.md).

---

## feat(agents): add gated Codex runtime subscription UI (#3917)

- **SHA**: `5c3a5d97320144bf05f5db737e0ffa16086f5216`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-29T07:24:39Z
- **PR**: #3917

### Commit Message

```
feat(agents): add gated Codex runtime subscription UI (#3917)

## Problem and behavior

Adds a server-gated runtime interface for personal Codex subscriptions.
The entry lives in the Agent workspace header rather than Agent
Settings, so a user can bind their own subscription to template, shared,
or legacy Agents without gaining definition-edit permissions.

The dialog supports device-code authorization, connection
status/reconnection, account-discovered model selection, refresh and
disconnect. Subscription models are shown separately from ZooWork API
models. Selecting a personal model updates the effective runtime only;
the Agent definition keeps its platform default. Choosing a platform
model in the message composer exits the personal subscription.

The entry consumes the backend capability and stays completely hidden
when discovery returns `enabled: false`, the API is absent/unavailable,
or the preview is disabled. Admission remains server-side using
`CODEX_SUBSCRIPTIONS_INTERNAL_ENABLED` plus verified `@srp.one` email or
`CODEX_SUBSCRIPTIONS_ALLOWED_EMAILS`; there is no browser allowlist or
environment bypass.

## Dependency and rollout

- Backend runtime separation: #3923
- Existing provider connection APIs: #3912
- Deploy #3923 before this frontend head.
- Keep the master switch off until a dedicated staging Agent smoke
passes.
- Tools and sandbox remain separately metered; no silent platform
fallback is introduced.

No deployment settings or live data are changed by this PR.

## Validation

- full frontend unit suite: 6,250 passed, 1 todo
- TypeScript, ESLint, and frontend governance guards passed
- focused tests cover server-authoritative hiding, runtime binding on
managed definitions, platform/subscription presentation, authorization
polling, and account switching
- dedicated local staging-backed manual verification remains to be done
before rollout
```

### PR Body

## Problem and behavior

Adds a server-gated runtime interface for personal Codex subscriptions. The entry lives in the Agent workspace header rather than Agent Settings, so a user can bind their own subscription to template, shared, or legacy Agents without gaining definition-edit permissions.

The dialog supports device-code authorization, connection status/reconnection, account-discovered model selection, refresh and disconnect. Subscription models are shown separately from ZooWork API models. Selecting a personal model updates the effective runtime only; the Agent definition keeps its platform default. Choosing a platform model in the message composer exits the personal subscription.

The entry consumes the backend capability and stays completely hidden when discovery returns `enabled: false`, the API is absent/unavailable, or the preview is disabled. Admission remains server-side using `CODEX_SUBSCRIPTIONS_INTERNAL_ENABLED` plus verified `@srp.one` email or `CODEX_SUBSCRIPTIONS_ALLOWED_EMAILS`; there is no browser allowlist or environment bypass.

## Dependency and rollout

- Backend runtime separation: #3923
- Existing provider connection APIs: #3912
- Deploy #3923 before this frontend head.
- Keep the master switch off until a dedicated staging Agent smoke passes.
- Tools and sandbox remain separately metered; no silent platform fallback is introduced.

No deployment settings or live data are changed by this PR.

## Validation

- full frontend unit suite: 6,250 passed, 1 todo
- TypeScript, ESLint, and frontend governance guards passed
- focused tests cover server-authoritative hiding, runtime binding on managed definitions, platform/subscription presentation, authorization polling, and account switching
- dedicated local staging-backed manual verification remains to be done before rollout

---

## feat(platform): manage projects through Engine (#3920)

- **SHA**: `5354ed9d6e2a1d9c411f239461db5ca8f9fce08a`
- **作者**: finn-srp
- **日期**: 2026-09-29T06:27:35Z
- **PR**: #3920

### Commit Message

```
feat(platform): manage projects through Engine (#3920)

## Summary

- Create named Platform Projects through Engine, persist Engine IDs, and
recover only matching Platform-owned Engine Projects after an
interrupted local save.
- Archive named Projects through Engine. The implicit Default Project
cannot be archived.
- Use Engine's implicit `project_id = null` Default for each
Organization. Platform exposes it as `"default"` in management routes;
Default API Keys are stored and queried by Organization with a null
Project ID.
- Keep legacy local Default rows out of Project lists and reject their
API Keys. This PR does not delete staging data.
- Update the Platform Project UI and its documented API contract.

## Test plan

- [x] Backend targeted unit tests: 93 passed.
- [x] Backend Mongo BDD tests: 7 passed.
- [x] Backend `bash scripts/verify-py.sh`: passed, including ruff,
pyright, and import contracts.
- [x] Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (71 passed),
and `pnpm build`: passed with Node 24.
- [x] Pre-commit and pre-push checks: passed. The outdated `check-user`
hook was skipped because the active Finn GitHub login is `finn930`;
commit author is `finn-srp <finn@srp.one>`.
- [ ] Backend `--full` was not run, per maintainer instruction.
- [x] Staging CSFLE: exact PR repository reads and index creation passed
through the deployed encrypted client. See
`docs/staging-validation/2026-09-29-platform-projects-csfle-and-cleanup.md`.

## Scope and rollout

The Platform machine-key authentication mode remains disabled for
SDK/runtime requests. In staging, 7 legacy `prj_` Projects and 2
already-revoked Keys were removed after a protected backup and reference
audit. Organization, Billing order, payment-event, and user records were
preserved. The cleanup and validation are recorded in
`docs/staging-validation/2026-09-29-platform-projects-csfle-and-cleanup.md`.

Related Engine issue:
https://github.com/SerendipityOneInc/zooclaw-engine/issues/1573
```

### PR Body

## Summary

- Create named Platform Projects through Engine, persist Engine IDs, and recover only matching Platform-owned Engine Projects after an interrupted local save.
- Archive named Projects through Engine. The implicit Default Project cannot be archived.
- Use Engine's implicit `project_id = null` Default for each Organization. Platform exposes it as `"default"` in management routes; Default API Keys are stored and queried by Organization with a null Project ID.
- Keep legacy local Default rows out of Project lists and reject their API Keys. This PR does not delete staging data.
- Update the Platform Project UI and its documented API contract.

## Test plan

- [x] Backend targeted unit tests: 93 passed.
- [x] Backend Mongo BDD tests: 7 passed.
- [x] Backend `bash scripts/verify-py.sh`: passed, including ruff, pyright, and import contracts.
- [x] Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (71 passed), and `pnpm build`: passed with Node 24.
- [x] Pre-commit and pre-push checks: passed. The outdated `check-user` hook was skipped because the active Finn GitHub login is `finn930`; commit author is `finn-srp <finn@srp.one>`.
- [ ] Backend `--full` was not run, per maintainer instruction.
- [x] Staging CSFLE: exact PR repository reads and index creation passed through the deployed encrypted client. See `docs/staging-validation/2026-09-29-platform-projects-csfle-and-cleanup.md`.

## Scope and rollout

The Platform machine-key authentication mode remains disabled for SDK/runtime requests. In staging, 7 legacy `prj_` Projects and 2 already-revoked Keys were removed after a protected backup and reference audit. Organization, Billing order, payment-event, and user records were preserved. The cleanup and validation are recorded in `docs/staging-validation/2026-09-29-platform-projects-csfle-and-cleanup.md`.

Related Engine issue: https://github.com/SerendipityOneInc/zooclaw-engine/issues/1573

---

## feat(agents): decouple Codex runtime subscriptions (#3923)

- **SHA**: `c5fa4ebe4df31c6f77b29e6f149e8a9415d8e7d5`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-29T06:09:33Z
- **PR**: #3923

### Commit Message

```
feat(agents): decouple Codex runtime subscriptions (#3923)

## Summary

- allow a personal Codex subscription to override an Engine Agent at
runtime without requiring an editable Agent Revision
- keep the Revision-owned platform default managed until a personal
subscription is active
- preserve an active personal subscription across unrelated Revision
renders, while allowing an explicit platform selection to exit it

## Frontend

- UI remains in #3917
- provider-connection discovery remains the server-authoritative
allowlist gate; non-allowlisted users receive `enabled: false` and see
no entry

## Verification

- `ruff check` and `ruff format --check`
- `pyright app/ tests/`
- import-linter contracts
- 21 focused model/runtime-binding tests
- 101 Agent Revision/apply/share-update regression tests
```

### PR Body

## Summary

- allow a personal Codex subscription to override an Engine Agent at runtime without requiring an editable Agent Revision
- keep the Revision-owned platform default managed until a personal subscription is active
- preserve an active personal subscription across unrelated Revision renders, while allowing an explicit platform selection to exit it

## Frontend

- UI remains in #3917
- provider-connection discovery remains the server-authoritative allowlist gate; non-allowlisted users receive `enabled: false` and see no entry

## Verification

- `ruff check` and `ruff format --check`
- `pyright app/ tests/`
- import-linter contracts
- 21 focused model/runtime-binding tests
- 101 Agent Revision/apply/share-update regression tests

---

## fix(billing): allow repurchase after terminal subscriptions (#3921)

- **SHA**: `21c1d37bb80239fe6042e19cebe8af12b48d1cf7`
- **作者**: sam-srp
- **日期**: 2026-09-29T04:42:47Z
- **PR**: #3921

### Commit Message

```
fix(billing): allow repurchase after terminal subscriptions (#3921)

## Summary
- Allow a new subscription after an agreement is canceled or expired
even if its historical billing cycle ends in the future. Keep
active/canceling agreements, unresolved payments, and legacy Stripe
`missing_in_stripe` recovery periods protected.
- Hide future historical end dates in the expired personal-access
summary; effective subscriptions retain their existing dates.

## Root cause
Purchase eligibility treated a terminal agreement's original
`current_period_end` as remaining access, while the access resolver
correctly returned expired. Immediate termination therefore left users
unable to buy a replacement plan. The expired summary also reused future
dates from stale agreements/payment entitlements.

## Test plan
- [x] 99 targeted unit tests: terminal states across providers,
active/canceling/manual-review protection, legacy cutover recovery
boundaries, unresolved checkout protection, and access-summary
contracts.
- [x] Full backend static checks: Ruff, formatting, Pyright and import
architecture contracts.
- No database migration or new environment variables. This PR does not
perform bulk account repairs.
```

### PR Body

## Summary
- Allow a new subscription after an agreement is canceled or expired even if its historical billing cycle ends in the future. Keep active/canceling agreements, unresolved payments, and legacy Stripe `missing_in_stripe` recovery periods protected.
- Hide future historical end dates in the expired personal-access summary; effective subscriptions retain their existing dates.

## Root cause
Purchase eligibility treated a terminal agreement's original `current_period_end` as remaining access, while the access resolver correctly returned expired. Immediate termination therefore left users unable to buy a replacement plan. The expired summary also reused future dates from stale agreements/payment entitlements.

## Test plan
- [x] 99 targeted unit tests: terminal states across providers, active/canceling/manual-review protection, legacy cutover recovery boundaries, unresolved checkout protection, and access-summary contracts.
- [x] Full backend static checks: Ruff, formatting, Pyright and import architecture contracts.
- No database migration or new environment variables. This PR does not perform bulk account repairs.

---

## feat(agents): support revision-checked Build source file edits (#3919)

- **SHA**: `ab84000b1e07a7e8650bdea01bc5a35efc1f0ee7`
- **作者**: kaka-srp
- **日期**: 2026-09-29T04:02:13Z
- **PR**: #3919

### Commit Message

```
feat(agents): support revision-checked Build source file edits (#3919)

## Summary

Build currently requires the model to resend whole source files for
small edits. Add bounded internal `files_read` / `files_apply`
operations so Engine can apply ordinary file-tool edits and persist
affected files through the existing ChangeSet.

- Bind reads and writes to the canonical Build session, computer and
existing edit permission. Require an opaque revision token and the
existing state/version CAS for mutation.
- Store net changes relative to the immutable base: repeated edits
consume one operation per changed path, and reverting removes the
operation. Preserve the 32-path / 4 MiB limits, avatar normalization,
derived assets, inherited references and Skill validation.
- Validate the complete candidate before avatar promotion; check the
normalized result again before CAS. Invalid new Skill names, oversize
and NUL inputs are rejected before artifact I/O.
- Keep legacy authoring tools compatible. No new tables, background
synchronization or automatic cross-turn draft continuation.

Related:
https://github.com/SerendipityOneInc/zooclaw-engine/issues/1693.
Companion Engine PR:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/1758. Deploy
this backend before Engine; roll Engine back first.

## Test plan

- Independent local review completed; 120 backend tests passed after
rebasing onto main and adding avatar pre-validation regressions (240
broader tests passed in the implementation validation).
- Backend static verification and commit hooks passed.
- Real existing zooclaw-dev lane with staging CSFLE Mongo, actual model
and staging E2B: ordinary edit/write/patch → validate → isolated
run_test → commit → a new active task executing the registered Skill.
Both evaluation and active execution returned `SOURCE_VERSION_2`.
- Readback confirmed only two expected files changed; untouched CRLF
script bytes remained identical. Exact 4 MiB snapshot, oversize
rejection, stale retry, concurrent 200/409 CAS, failed-batch atomicity
and session/computer authorization checked through HTTP.
- Disposable fixtures and sandboxes cleaned. No production or existing
user data changed.

The live evidence predates the final rebase onto main; focused
regression/static checks are repeated on the rebased branch. This does
not claim browser UI, deployed ingress, channel delivery or concurrent
peak-memory validation.

Atomicity covers ChangeSet content/version persistence. Avatar promotion
retains the existing shared content-addressed storage behavior: a
concurrent CAS loss can leave an unreferenced object, and this PR does
not add object deletion/GC that could remove another reference to the
same immutable bytes.
```

### PR Body

## Summary

Build currently requires the model to resend whole source files for small edits. Add bounded internal `files_read` / `files_apply` operations so Engine can apply ordinary file-tool edits and persist affected files through the existing ChangeSet.

- Bind reads and writes to the canonical Build session, computer and existing edit permission. Require an opaque revision token and the existing state/version CAS for mutation.
- Store net changes relative to the immutable base: repeated edits consume one operation per changed path, and reverting removes the operation. Preserve the 32-path / 4 MiB limits, avatar normalization, derived assets, inherited references and Skill validation.
- Validate the complete candidate before avatar promotion; check the normalized result again before CAS. Invalid new Skill names, oversize and NUL inputs are rejected before artifact I/O.
- Keep legacy authoring tools compatible. No new tables, background synchronization or automatic cross-turn draft continuation.

Related: https://github.com/SerendipityOneInc/zooclaw-engine/issues/1693. Companion Engine PR: https://github.com/SerendipityOneInc/zooclaw-engine/pull/1758. Deploy this backend before Engine; roll Engine back first.

## Test plan

- Independent local review completed; 120 backend tests passed after rebasing onto main and adding avatar pre-validation regressions (240 broader tests passed in the implementation validation).
- Backend static verification and commit hooks passed.
- Real existing zooclaw-dev lane with staging CSFLE Mongo, actual model and staging E2B: ordinary edit/write/patch → validate → isolated run_test → commit → a new active task executing the registered Skill. Both evaluation and active execution returned `SOURCE_VERSION_2`.
- Readback confirmed only two expected files changed; untouched CRLF script bytes remained identical. Exact 4 MiB snapshot, oversize rejection, stale retry, concurrent 200/409 CAS, failed-batch atomicity and session/computer authorization checked through HTTP.
- Disposable fixtures and sandboxes cleaned. No production or existing user data changed.

The live evidence predates the final rebase onto main; focused regression/static checks are repeated on the rebased branch. This does not claim browser UI, deployed ingress, channel delivery or concurrent peak-memory validation.

Atomicity covers ChangeSet content/version persistence. Avatar promotion retains the existing shared content-addressed storage behavior: a concurrent CAS loss can leave an unreferenced object, and this PR does not add object deletion/GC that could remove another reference to the same immutable bytes.

---
