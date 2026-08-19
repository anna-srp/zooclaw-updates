# SerendipityOneInc/ecap-workspace — commits 2026-08-18

## fix(billing): scope Card checkout provider CAS to the active provider (#3420)

- **SHA**: `4371cce5ce365b3887c0589fb942a19b14e5f026`
- **作者**: tim-srp
- **日期**: 2026-08-18T17:40:34Z
- **PR**: #3420

### Commit Message

```
fix(billing): scope Card checkout provider CAS to the active provider (#3420)

## Summary

Fixes a staging bug where a brand-new user clicking "Try Starter for
free" was rejected with `billing.card_checkout.outcome_unresolved` ("A
previous Card checkout is still being reviewed") on their **first**
attempt.

The Airwallex switch (#3419) updated the checkout orchestration to
create orders with `provider=airwallex`, but the persistence layer still
hard-coded `provider=creem` in the provider-create CAS, checkout
attachment, and manual-review/fail markers. A new user's first trial
checkout therefore failed its provider claim against its own Airwallex
order, returned unresolved, and every retry hit the same unresolved
checkout.

## Root cause

- `claim_provider_request` (provider Create CAS) filtered on
`provider=creem`, so an Airwallex order never matched → claim returned
`False` → `_unresolved_error()` raised. First attempt fails immediately.
- `attach_checkout` / `mark_manual_review` / `mark_failed` had the same
`provider=creem` filter, so a successful Create could not attach, and
failures could not be marked correctly.
- Because the failed order stayed `pending` with
`provider_checkout_requested_at` set, every retry hit
`find_unresolved_subscription` (which correctly passes
`provider=airwallex`) and was permanently stuck.

## Change

- **repo layer** (`card_checkout_order_repo.py`): thread `provider`
(default `"creem"`) through `claim_provider_request`, `attach_checkout`,
`mark_manual_review`, `mark_failed`. Legacy Creem paths keep their exact
previous behavior.
- **wrapper layer** (`card_checkout_orders.py`):
`claim_card_checkout_request` accepts a `provider`;
`attach_card_checkout` and the status marker helper read the provider
from the persisted order.
- **callers**: Airwallex checkout flows (`card_checkout.py`,
`airwallex_upgrade_checkout.py`) pass `BillingProvider.AIRWALLEX`; the
Creem enterprise path keeps the default.

## Tests

- 625 card/airwallex/creem-related unit tests pass, including new repo
regression tests asserting the provider-scoped CAS filters.
- ruff + pyright clean.

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary

Fixes a staging bug where a brand-new user clicking "Try Starter for free" was rejected with `billing.card_checkout.outcome_unresolved` ("A previous Card checkout is still being reviewed") on their **first** attempt.

The Airwallex switch (#3419) updated the checkout orchestration to create orders with `provider=airwallex`, but the persistence layer still hard-coded `provider=creem` in the provider-create CAS, checkout attachment, and manual-review/fail markers. A new user's first trial checkout therefore failed its provider claim against its own Airwallex order, returned unresolved, and every retry hit the same unresolved checkout.

## Root cause

- `claim_provider_request` (provider Create CAS) filtered on `provider=creem`, so an Airwallex order never matched → claim returned `False` → `_unresolved_error()` raised. First attempt fails immediately.
- `attach_checkout` / `mark_manual_review` / `mark_failed` had the same `provider=creem` filter, so a successful Create could not attach, and failures could not be marked correctly.
- Because the failed order stayed `pending` with `provider_checkout_requested_at` set, every retry hit `find_unresolved_subscription` (which correctly passes `provider=airwallex`) and was permanently stuck.

## Change

- **repo layer** (`card_checkout_order_repo.py`): thread `provider` (default `"creem"`) through `claim_provider_request`, `attach_checkout`, `mark_manual_review`, `mark_failed`. Legacy Creem paths keep their exact previous behavior.
- **wrapper layer** (`card_checkout_orders.py`): `claim_card_checkout_request` accepts a `provider`; `attach_card_checkout` and the status marker helper read the provider from the persisted order.
- **callers**: Airwallex checkout flows (`card_checkout.py`, `airwallex_upgrade_checkout.py`) pass `BillingProvider.AIRWALLEX`; the Creem enterprise path keeps the default.

## Tests

- 625 card/airwallex/creem-related unit tests pass, including new repo regression tests asserting the provider-scoped CAS filters.
- ruff + pyright clean.


---

## feat(billing): unconditionally switch card subscription channel to Airwallex (#3419)

- **SHA**: `7724ba1a45a60fa52787523410ca984026fabe57`
- **作者**: tim-srp
- **日期**: 2026-08-18T17:01:26Z
- **PR**: #3419

### Commit Message

```
feat(billing): unconditionally switch card subscription channel to Airwallex (#3419)

## Summary

Unconditionally switch the card subscription payment channel from Creem
to Airwallex (both new sign-ups and upgrades), per the design spec
`docs/superpowers/specs/2026-08-18-airwallex-subscription-unconditional-switch.md`.

### What changed

**1. Checkout — unconditional Airwallex**
- Removed the `AIRWALLEX_CHECKOUT_ENABLED` feature switch; new card
subscriptions always create an Airwallex checkout.
- Upgrades also go through Airwallex (`airwallex_upgrade_checkout.py`)
using the "new subscription replaces the superseded one" shape — no
refund, remaining credits carry over into the new subscription.
- Provider-parameterized replacement admission so the same admission
logic serves both Creem (legacy) and Airwallex.

**2. Paid replacement settlement**
(`app/services/airwallex/replacement.py`)
- `prepare_paid_checkout_replacement` — admit a paid checkout as a
replacement of a superseded subscription.
- `record_paid_checkout_agreement` / `commit_paid_checkout_replacement`
— atomic handoff: old agreement demoted (`current: False`,
`superseded_at`, `replacement_cleanup_required: True`), new agreement
promoted (`current: True`, `replaced_subscription_agreement_id`), plus
audit records.
- `cancel_replaced_subscription` — cancel the superseded subscription at
period end (Airwallex `proration_behavior=NONE`, scheduled cancel), with
read-back on failure.
- `retry_cleanup` — bounded retry used by the reconciliation sweep.

**3. First-payment settlement wiring** (`first_payment.py`)
- Detects replacement orders, settles the new agreement as non-current,
records the paid agreement, releases the checkout lease, then cancels
the superseded subscription.

**4. Renewal guard** (`renewal.py`)
- A superseded agreement (`current is not True` or
`replacement_cleanup_required is True`) never renews — prevents
duplicate credit grants.

**5. Reconciliation cleanup sweep** (`reconciliation.py`)
- `reconcile_current_airwallex_subscriptions` also lists superseded
Airwallex agreements needing cleanup and retries their cancellation.

**6. Repo compatibility** (`creem_replacement_cleanup_repo.py`,
`subscription_agreement_repo.py`)
- `commit_paid_replacement_handoff` and `list_candidates` are
provider-parameterized, defaulting to `creem` — the Creem path is
unchanged.

### Tests

- 134 unit tests pass across the affected suites:
`test_airwallex_first_payment`, `test_airwallex_reconciliation`,
`test_airwallex_renewal`,
`test_subscription_agreement_replacement_repo`, `test_billing_v2_repos`.
- New tests cover: upgrade settlement + superseded cancel,
reconciliation cleanup sweep, superseded renewal guard,
provider-parameterized replacement handoff,
`list_candidates(provider="airwallex")`.
- `ruff`, `ruff-format`, import-linter pass. Remaining pyright errors
are pre-existing boto3 stub noise in `r2_storage.py` (untouched by this
branch).

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary

Unconditionally switch the card subscription payment channel from Creem to Airwallex (both new sign-ups and upgrades), per the design spec `docs/superpowers/specs/2026-08-18-airwallex-subscription-unconditional-switch.md`.

### What changed

**1. Checkout — unconditional Airwallex**
- Removed the `AIRWALLEX_CHECKOUT_ENABLED` feature switch; new card subscriptions always create an Airwallex checkout.
- Upgrades also go through Airwallex (`airwallex_upgrade_checkout.py`) using the "new subscription replaces the superseded one" shape — no refund, remaining credits carry over into the new subscription.
- Provider-parameterized replacement admission so the same admission logic serves both Creem (legacy) and Airwallex.

**2. Paid replacement settlement** (`app/services/airwallex/replacement.py`)
- `prepare_paid_checkout_replacement` — admit a paid checkout as a replacement of a superseded subscription.
- `record_paid_checkout_agreement` / `commit_paid_checkout_replacement` — atomic handoff: old agreement demoted (`current: False`, `superseded_at`, `replacement_cleanup_required: True`), new agreement promoted (`current: True`, `replaced_subscription_agreement_id`), plus audit records.
- `cancel_replaced_subscription` — cancel the superseded subscription at period end (Airwallex `proration_behavior=NONE`, scheduled cancel), with read-back on failure.
- `retry_cleanup` — bounded retry used by the reconciliation sweep.

**3. First-payment settlement wiring** (`first_payment.py`)
- Detects replacement orders, settles the new agreement as non-current, records the paid agreement, releases the checkout lease, then cancels the superseded subscription.

**4. Renewal guard** (`renewal.py`)
- A superseded agreement (`current is not True` or `replacement_cleanup_required is True`) never renews — prevents duplicate credit grants.

**5. Reconciliation cleanup sweep** (`reconciliation.py`)
- `reconcile_current_airwallex_subscriptions` also lists superseded Airwallex agreements needing cleanup and retries their cancellation.

**6. Repo compatibility** (`creem_replacement_cleanup_repo.py`, `subscription_agreement_repo.py`)
- `commit_paid_replacement_handoff` and `list_candidates` are provider-parameterized, defaulting to `creem` — the Creem path is unchanged.

### Tests

- 134 unit tests pass across the affected suites: `test_airwallex_first_payment`, `test_airwallex_reconciliation`, `test_airwallex_renewal`, `test_subscription_agreement_replacement_repo`, `test_billing_v2_repos`.
- New tests cover: upgrade settlement + superseded cancel, reconciliation cleanup sweep, superseded renewal guard, provider-parameterized replacement handoff, `list_candidates(provider="airwallex")`.
- `ruff`, `ruff-format`, import-linter pass. Remaining pyright errors are pre-existing boto3 stub noise in `r2_storage.py` (untouched by this branch).


---

## feat(web): refresh channel action and global loading (#3369)

- **SHA**: `71195904121902ee07a6c641fc8ae1c8874dec54`
- **作者**: shana-srp
- **日期**: 2026-08-18T09:14:40Z
- **PR**: #3369

### Commit Message

```
feat(web): refresh channel action and global loading (#3369)

## Linear

N/A — no Linear issue was provided for this UI polish request.

## Summary

- align the Channel “Add Channel” action with the Agent Builder button
shape and remove its glass-like shadow
- center Channel loading states within the right-side content panel
- replace the shared global loader with the new ZooClaw animation at
90×90 and 50% opacity
- preserve page-specific loading messages while preventing duplicate
generic labels

## Test plan

- [x] `bash scripts/verify-web.sh` for all changed frontend files
- [x] TypeScript and ESLint checks
- [x] 86 related Vitest tests
- [x] pre-push changed-surface verification

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Linear

N/A — no Linear issue was provided for this UI polish request.

## Summary

- align the Channel “Add Channel” action with the Agent Builder button shape and remove its glass-like shadow
- center Channel loading states within the right-side content panel
- replace the shared global loader with the new ZooClaw animation at 90×90 and 50% opacity
- preserve page-specific loading messages while preventing duplicate generic labels

## Test plan

- [x] `bash scripts/verify-web.sh` for all changed frontend files
- [x] TypeScript and ESLint checks
- [x] 86 related Vitest tests
- [x] pre-push changed-surface verification


---

## fix(chat): improve user message emphasis (#3366)

- **SHA**: `bd2d807414ed4cb8923f7e0f228f5a8944194d68`
- **作者**: shana-srp
- **日期**: 2026-08-18T09:14:23Z
- **PR**: #3366

### Commit Message

```
fix(chat): improve user message emphasis (#3366)

## Summary

- set user-authored chat message text to a consistent 500 font weight
across main, compact, shared-thread, deep-research, card-action, and
feedback chat surfaces
- keep assistant response body text at its existing default weight
- replace the Chinese degradation copy with “AI 能力受限 · 理解力 {score}/100”
and rename the action to “提升能力”
- add regression coverage for user-versus-assistant message emphasis

## Testing

- `pnpm --dir web/packages/chat-ui test` — 354 tests passed
- `pnpm --dir web/packages/chat-ui tsc`
- `pnpm --dir web/packages/chat-ui lint`
- targeted web app tests — 51 tests passed
- targeted ESLint for changed app files

## Notes

- Tailwind `font-medium` is used because it maps to font weight 500;
`font-semibold` maps to 600.

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary

- set user-authored chat message text to a consistent 500 font weight across main, compact, shared-thread, deep-research, card-action, and feedback chat surfaces
- keep assistant response body text at its existing default weight
- replace the Chinese degradation copy with “AI 能力受限 · 理解力 {score}/100” and rename the action to “提升能力”
- add regression coverage for user-versus-assistant message emphasis

## Testing

- `pnpm --dir web/packages/chat-ui test` — 354 tests passed
- `pnpm --dir web/packages/chat-ui tsc`
- `pnpm --dir web/packages/chat-ui lint`
- targeted web app tests — 51 tests passed
- targeted ESLint for changed app files

## Notes

- Tailwind `font-medium` is used because it maps to font weight 500; `font-semibold` maps to 600.


---

## feat(analytics): persist GA registration identifiers (#3415)

- **SHA**: `4aabde53410c0cabd0571ec7506acb618531aafb`
- **作者**: winston-srp
- **日期**: 2026-08-18T09:03:41Z
- **PR**: #3415

### Commit Message

```
feat(analytics): persist GA registration identifiers (#3415)

## Linear


https://linear.app/srpone/issue/ECA-1383/persist-ga4-registration-identifiers

## Summary

- collect GA4 measurement, client, and session identifiers during
first-time web registration with bounded, fail-soft `gtag` reads
- persist the identifiers as private Account metadata for normal and
warm-pool registration paths while preserving the existing
empty-metadata condition
- strip the private identifiers from public account responses and cover
validation, cancellation, propagation, and response privacy with
frontend, unit, and BDD tests

## Test plan

- [x] `bash scripts/verify-web.sh ...` — TypeScript, 31 test files / 450
tests, and ESLint passed
- [x] `bash scripts/verify-py.sh` — Ruff, format, Pyright, and import
contracts passed
- [x] targeted backend unit tests — 116 passed
- [x] registration BDD scenarios — 8 passed
- [x] end-to-end local web → local claw-interface → staging dependencies
via Telepresence — registration returned 201 and all three GA
identifiers were confirmed persisted in staging MongoDB

---------

Co-authored-by: Developer <dev@srp.one>
```

### PR Body

## Linear

https://linear.app/srpone/issue/ECA-1383/persist-ga4-registration-identifiers

## Summary

- collect GA4 measurement, client, and session identifiers during first-time web registration with bounded, fail-soft `gtag` reads
- persist the identifiers as private Account metadata for normal and warm-pool registration paths while preserving the existing empty-metadata condition
- strip the private identifiers from public account responses and cover validation, cancellation, propagation, and response privacy with frontend, unit, and BDD tests

## Test plan

- [x] `bash scripts/verify-web.sh ...` — TypeScript, 31 test files / 450 tests, and ESLint passed
- [x] `bash scripts/verify-py.sh` — Ruff, format, Pyright, and import contracts passed
- [x] targeted backend unit tests — 116 passed
- [x] registration BDD scenarios — 8 passed
- [x] end-to-end local web → local claw-interface → staging dependencies via Telepresence — registration returned 201 and all three GA identifiers were confirmed persisted in staging MongoDB


---

## feat(agents): map sandbox class from entitlement (#3408)

- **SHA**: `b1128787547b7355da32956c5e0af049b1c231d8`
- **作者**: kaka-srp
- **日期**: 2026-08-18T04:06:43Z
- **PR**: #3408

### Commit Message

```
feat(agents): map sandbox class from entitlement (#3408)

## Summary

- map personal current access to starter/pro/ultra and all Team
organizations to ultra
- inject the server-authoritative Sandbox class on every managed Agent
create/update/start/prepare path
- seed the pinned LiteLLM credential before any warm Sandbox is created
- propagate entitlement changes best-effort and add a protected
reconciliation cron for drift repair
- preserve free/no-subscription access behavior; allowed users receive
starter without an extra Sandbox gate

Supports
[zooclaw-engine#749](https://github.com/SerendipityOneInc/zooclaw-engine/issues/749).

Related implementation:
[zooclaw-engine#792](https://github.com/SerendipityOneInc/zooclaw-engine/pull/792),
[infra#19](https://github.com/SerendipityOneInc/infra/pull/19),
[billing-gateway#67](https://github.com/SerendipityOneInc/billing-gateway/pull/67).

## Verification

- `ruff check app tests`
- `ruff format --check app tests`
- `pyright app tests`
- Python file-length governance check
- affected Agent/resource tests: 277 passed

## Dependency

Deploy after the Engine Agent API accepts `sandbox_resource_class`.
Existing Agents can then be converged with the protected
`engine-sandbox-resource-class-reconcile` cron.
```

### PR Body

## Summary

- map personal current access to starter/pro/ultra and all Team organizations to ultra
- inject the server-authoritative Sandbox class on every managed Agent create/update/start/prepare path
- seed the pinned LiteLLM credential before any warm Sandbox is created
- propagate entitlement changes best-effort and add a protected reconciliation cron for drift repair
- preserve free/no-subscription access behavior; allowed users receive starter without an extra Sandbox gate

Supports [zooclaw-engine#749](https://github.com/SerendipityOneInc/zooclaw-engine/issues/749).

Related implementation: [zooclaw-engine#792](https://github.com/SerendipityOneInc/zooclaw-engine/pull/792), [infra#19](https://github.com/SerendipityOneInc/infra/pull/19), [billing-gateway#67](https://github.com/SerendipityOneInc/billing-gateway/pull/67).

## Verification

- `ruff check app tests`
- `ruff format --check app tests`
- `pyright app tests`
- Python file-length governance check
- affected Agent/resource tests: 277 passed

## Dependency

Deploy after the Engine Agent API accepts `sandbox_resource_class`. Existing Agents can then be converged with the protected `engine-sandbox-resource-class-reconcile` cron.


---

## feat(enterprise-admin): org usage dashboard with trend analytics, calendar range picker, and bulk quota management (#3397)

- **SHA**: `6682311863ebc73a3a815f959f077cd61c082652`
- **作者**: david-srp
- **日期**: 2026-08-18T02:28:30Z
- **PR**: #3397

### Commit Message

```
feat(enterprise-admin): org usage dashboard with trend analytics, calendar range picker, and bulk quota management (#3397)

## Linear
<!-- 无关联 issue -->

## Summary

Rebuild the enterprise-admin `/usage` page into a full org usage
dashboard + member usage management surface. **Frontend-only** — zero
`services/claw-interface` changes; every panel runs on existing
endpoints (design spec:
`docs/superpowers/specs/2026-08-14-enterprise-admin-usage-dashboard.md`).

**Org usage analytics (new)**
- Usage trend card: recharts daily/10-minute bar chart with 24h / 7d /
30d presets **plus a calendar date-range picker** (react-day-picker +
Radix Popover, zc theming) — custom ranges are client-side slices of the
30d daily dataset, bounded to the last 30 days; Credits / Requests /
Peak-window KPIs recompute per selection; truncation (`meta.truncated`)
surfaces as a banner; range switches dim stale data (keepPreviousData)
- Usage-by-model card: top-5 split with share bars, credits, requests
- Data source: the existing self-scoped `GET
/users/credits/usage/records` — team-first billing resolution means an
org admin's own call already returns org-wide aggregates
- Each section labels its time scope (trend = selected range, models =
fetched window, member table = current credit period) since the date
filter can only govern the trend card

**Member usage management (new)**
- Search (name/email/uid), filters (over quota / near quota ≥80% /
unlimited / no usage), column sorting, share-of-spend column,
near/over-quota badges, client-side pagination
- CSV export of the filtered view (RFC 4180 quoting + formula-injection
guard + UTF-8 BOM)
- **Bulk AI-quota apply**: multi-select rows → one dialog applies the
same limit sequentially via the existing single-member endpoint, with
progress and failed-row retry
- LLM-only scope footnote (member usage excludes search/video drawn from
the org wallet)

**Structure**: strict MVVM (`useUsageViewModel` owns all
state/derivation); new reusable primitives `Popover`, `DateRangePicker`;
new hooks `useUsageRecords`, `useBulkQuota`; `lib/csv`,
`lib/local-date`; chart tokens `--color-chart-1..5` aligned with
dashboard-console; full zh catalog coverage; `/usage` TopBar title fix.
New deps: `recharts@3.9.2` (exact pin matching web/app),
`react-day-picker@^9.14.0`.

**Known limits (by existing API contract, documented in the spec)**: no
token totals, no billing-period range, no period-over-period deltas,
model split capped at top-5 and not sliceable by custom dates, member
usage is a current-period scalar (no history — upstream ECA-1352).

## Test plan
- [x] `pnpm exec tsc --noEmit`, `pnpm run lint`, `pnpm test` in
`web/enterprise-admin` — 58 files / 416 tests green (new coverage: view
model slicing/filters/selection/deltas suppression, bulk quota state
machine incl. retry, CSV quoting + injection, date-range picker wiring,
trend/model cards, page wiring)
- [x] Browser validation against a local mock backend (real dev server +
real auth flow): KPI cards, trend chart + tooltip, preset & calendar
range selection/apply/clear with client-side re-aggregation, model card
window note, member search/filter/sort, bulk quota apply end-to-end with
live row updates, over/near-quota badges, reset-pending retry
- [x] 16-agent adversarial review pass; all 12 confirmed findings fixed
(select-all scoping, pagination clamping, bulk retry denominators, CSV
injection, stale-data dimming, MVVM cleanup, dead-code removal)
- [x] `git diff origin/main -- services/` is empty — backend untouched
- [ ] CI (`enterprise-admin-quality`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Linear
<!-- 无关联 issue -->

## Summary

Rebuild the enterprise-admin `/usage` page into a full org usage dashboard + member usage management surface. **Frontend-only** — zero `services/claw-interface` changes; every panel runs on existing endpoints (design spec: `docs/superpowers/specs/2026-08-14-enterprise-admin-usage-dashboard.md`).

**Org usage analytics (new)**
- Usage trend card: recharts daily/10-minute bar chart with 24h / 7d / 30d presets **plus a calendar date-range picker** (react-day-picker + Radix Popover, zc theming) — custom ranges are client-side slices of the 30d daily dataset, bounded to the last 30 days; Credits / Requests / Peak-window KPIs recompute per selection; truncation (`meta.truncated`) surfaces as a banner; range switches dim stale data (keepPreviousData)
- Usage-by-model card: top-5 split with share bars, credits, requests
- Data source: the existing self-scoped `GET /users/credits/usage/records` — team-first billing resolution means an org admin's own call already returns org-wide aggregates
- Each section labels its time scope (trend = selected range, models = fetched window, member table = current credit period) since the date filter can only govern the trend card

**Member usage management (new)**
- Search (name/email/uid), filters (over quota / near quota ≥80% / unlimited / no usage), column sorting, share-of-spend column, near/over-quota badges, client-side pagination
- CSV export of the filtered view (RFC 4180 quoting + formula-injection guard + UTF-8 BOM)
- **Bulk AI-quota apply**: multi-select rows → one dialog applies the same limit sequentially via the existing single-member endpoint, with progress and failed-row retry
- LLM-only scope footnote (member usage excludes search/video drawn from the org wallet)

**Structure**: strict MVVM (`useUsageViewModel` owns all state/derivation); new reusable primitives `Popover`, `DateRangePicker`; new hooks `useUsageRecords`, `useBulkQuota`; `lib/csv`, `lib/local-date`; chart tokens `--color-chart-1..5` aligned with dashboard-console; full zh catalog coverage; `/usage` TopBar title fix. New deps: `recharts@3.9.2` (exact pin matching web/app), `react-day-picker@^9.14.0`.

**Known limits (by existing API contract, documented in the spec)**: no token totals, no billing-period range, no period-over-period deltas, model split capped at top-5 and not sliceable by custom dates, member usage is a current-period scalar (no history — upstream ECA-1352).

## Test plan
- [x] `pnpm exec tsc --noEmit`, `pnpm run lint`, `pnpm test` in `web/enterprise-admin` — 58 files / 416 tests green (new coverage: view model slicing/filters/selection/deltas suppression, bulk quota state machine incl. retry, CSV quoting + injection, date-range picker wiring, trend/model cards, page wiring)
- [x] Browser validation against a local mock backend (real dev server + real auth flow): KPI cards, trend chart + tooltip, preset & calendar range selection/apply/clear with client-side re-aggregation, model card window note, member search/filter/sort, bulk quota apply end-to-end with live row updates, over/near-quota badges, reset-pending retry
- [x] 16-agent adversarial review pass; all 12 confirmed findings fixed (select-all scoping, pagination clamping, bulk retry denominators, CSV injection, stale-data dimming, MVVM cleanup, dead-code removal)
- [x] `git diff origin/main -- services/` is empty — backend untouched
- [ ] CI (`enterprise-admin-quality`)

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---
