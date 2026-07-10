# SerendipityOneInc/ecap-workspace commits — 2026-07-09

共 20 个 commit


## feat(dashboard-console): add subscription codes admin page (#2807)

- **SHA**: `6d7d2ffe420754ddf544ca4014628fad85f78346`
- **作者**: bill-srp
- **日期**: 2026-07-09T13:58:26Z
- **PR**: #2807

**完整 commit message:**

```
feat(dashboard-console): add subscription codes admin page (#2807)

# Purpose

Plan 4a of the staff-admin relocation ([design
spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)):
the first admin page in `web/dashboard-console` — **Subscription codes**
(`/subscription-codes`), replacing the web/app admin tab. Sits on the
`/internal/subscription-codes` endpoints (#2774) and the
`AdminOnly`/`useIsAdmin` infra (#2804). Establishes the page pattern the
Releases and Users pages (4b/4c) will copy.

# Approach

- **Page** (`routes/subscription-codes/`, agent-packs folder pattern):
`route.tsx` wrapped in `AdminOnly`, `use-subscription-codes-query.ts`
(react-query, 20/page), `use-view-model.ts` (search + create-form state,
direct api call + invalidate — no useMutation, matching console
convention).
- **Features (faithful port of the legacy `SubscriptionCodesTab`)**:
exact-code search / reset / refresh toolbar; inline create form
(optional code "leave blank to auto-generate", plan tier
starter/pro/ultra, duration days, note); 9-column table (code mono,
type, plan badge, days, max uses, used — red at limit, expires, created,
note); "N codes · page X of Y" pagination. The legacy tab had no row
actions/modals — none invented.
- **Deliberate deltas from legacy** (both documented in the plan):
English copy (console has no i18n; legacy tab was Chinese), and
**`max_activations` is never sent** — the new backend enforces
`Literal[1]` (single-use) and defaults it.
- **API**: `subscriptionCodesUrl` builder +
`listSubscriptionCodes`/`createSubscriptionCode` fetchers (Bearer via
`authHeaders`, `ApiError` surface; a claw-interface failure never signs
the user out).
- **Discoverability, admin-gated**: new "Administration" sidebar group +
`PAGE_TITLE` entry + home `EntryCard`, all rendered only when
`useIsAdmin()` — non-admins see no admin nav at all (and the backend
independently enforces `require_srp_account` + `require_admin_user`).

# Tests

- [x] 36 files / 276 tests green (6 new/extended test files): URL
builder; fetcher contract (query-string with/without code, Bearer
header, no `max_activations` in create body, `ApiError` on non-ok);
query hook; view-model (payload shape, duration parsing `"0"`→1 /
`""`→30, error keeps fields + surfaces message, search trim + offset
reset, prev-page clamp); route (rows from data, non-admin sees "Admin
access required", create submit, pagination bounds)
- [x] `pnpm lint`, `pnpm typecheck` (react-router typegen picks up the
new route), `pnpm test` — all green (exactly what `dashboard-quality`
runs)

# Notes

- Implementation plan:
`docs/superpowers/plans/2026-07-09-console-subscription-codes-page.md`
- `StatusBadge` has no plan-tier tones yet — starter/pro/ultra render
the neutral tone (kit extension left for a design pass).
- Next slices: 4b Releases page, 4c Users page (grant/boost modals with
stable idempotency keys per #2783/#2788), then Plan 5 web/app `/admin`
teardown.
```

**PR body:**

# Purpose

Plan 4a of the staff-admin relocation ([design spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)): the first admin page in `web/dashboard-console` — **Subscription codes** (`/subscription-codes`), replacing the web/app admin tab. Sits on the `/internal/subscription-codes` endpoints (#2774) and the `AdminOnly`/`useIsAdmin` infra (#2804). Establishes the page pattern the Releases and Users pages (4b/4c) will copy.

# Approach

- **Page** (`routes/subscription-codes/`, agent-packs folder pattern): `route.tsx` wrapped in `AdminOnly`, `use-subscription-codes-query.ts` (react-query, 20/page), `use-view-model.ts` (search + create-form state, direct api call + invalidate — no useMutation, matching console convention).
- **Features (faithful port of the legacy `SubscriptionCodesTab`)**: exact-code search / reset / refresh toolbar; inline create form (optional code "leave blank to auto-generate", plan tier starter/pro/ultra, duration days, note); 9-column table (code mono, type, plan badge, days, max uses, used — red at limit, expires, created, note); "N codes · page X of Y" pagination. The legacy tab had no row actions/modals — none invented.
- **Deliberate deltas from legacy** (both documented in the plan): English copy (console has no i18n; legacy tab was Chinese), and **`max_activations` is never sent** — the new backend enforces `Literal[1]` (single-use) and defaults it.
- **API**: `subscriptionCodesUrl` builder + `listSubscriptionCodes`/`createSubscriptionCode` fetchers (Bearer via `authHeaders`, `ApiError` surface; a claw-interface failure never signs the user out).
- **Discoverability, admin-gated**: new "Administration" sidebar group + `PAGE_TITLE` entry + home `EntryCard`, all rendered only when `useIsAdmin()` — non-admins see no admin nav at all (and the backend independently enforces `require_srp_account` + `require_admin_user`).

# Tests

- [x] 36 files / 276 tests green (6 new/extended test files): URL builder; fetcher contract (query-string with/without code, Bearer header, no `max_activations` in create body, `ApiError` on non-ok); query hook; view-model (payload shape, duration parsing `"0"`→1 / `""`→30, error keeps fields + surfaces message, search trim + offset reset, prev-page clamp); route (rows from data, non-admin sees "Admin access required", create submit, pagination bounds)
- [x] `pnpm lint`, `pnpm typecheck` (react-router typegen picks up the new route), `pnpm test` — all green (exactly what `dashboard-quality` runs)

# Notes

- Implementation plan: `docs/superpowers/plans/2026-07-09-console-subscription-codes-page.md`
- `StatusBadge` has no plan-tier tones yet — starter/pro/ultra render the neutral tone (kit extension left for a design pass).
- Next slices: 4b Releases page, 4c Users page (grant/boost modals with stable idempotency keys per #2783/#2788), then Plan 5 web/app `/admin` teardown.



## fix(enterprise-admin): hide pack upload actions (#2808)

- **SHA**: `d5f1c367de72dac0df688cb46047ce3a77dc936a`
- **作者**: bill-srp
- **日期**: 2026-07-09T13:58:09Z
- **PR**: #2808

**完整 commit message:**

```
fix(enterprise-admin): hide pack upload actions (#2808)

## Summary
- derive the enterprise-admin auth cookie domain from the request host
instead of `AUTH_SESSION_COOKIE_DOMAIN`
- remove enterprise-admin pack upload entry points from the pack library
and pack detail screens

## Root cause
Enterprise Admin still exposed pack creation/version upload actions in
the pack store UI, and auth cookie sharing depended on a deploy-time
domain variable instead of the runtime host.

## Test plan
- [x] `./node_modules/.bin/vitest run --config ./vitest.config.mts
'app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx'
'app/(dashboard)/packs/__tests__/packs-page.test.tsx'
app/api/auth/__tests__/auth-routes.test.ts`
- [x] `./node_modules/.bin/tsc --noEmit`
- [x] `./node_modules/.bin/eslint 'app/(dashboard)/packs/page.tsx'
'app/(dashboard)/packs/__tests__/packs-page.test.tsx'
'app/(dashboard)/packs/[packId]/page.tsx'
'app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx'
lib/auth-session-cookie.ts app/api/auth/__tests__/auth-routes.test.ts
--max-warnings=0`
- [x] `./node_modules/.bin/vitest run --config ./vitest.config.mts`
```

**PR body:**

## Summary
- derive the enterprise-admin auth cookie domain from the request host instead of `AUTH_SESSION_COOKIE_DOMAIN`
- remove enterprise-admin pack upload entry points from the pack library and pack detail screens

## Root cause
Enterprise Admin still exposed pack creation/version upload actions in the pack store UI, and auth cookie sharing depended on a deploy-time domain variable instead of the runtime host.

## Test plan
- [x] `./node_modules/.bin/vitest run --config ./vitest.config.mts 'app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx' 'app/(dashboard)/packs/__tests__/packs-page.test.tsx' app/api/auth/__tests__/auth-routes.test.ts`
- [x] `./node_modules/.bin/tsc --noEmit`
- [x] `./node_modules/.bin/eslint 'app/(dashboard)/packs/page.tsx' 'app/(dashboard)/packs/__tests__/packs-page.test.tsx' 'app/(dashboard)/packs/[packId]/page.tsx' 'app/(dashboard)/packs/[packId]/__tests__/pack-detail-page.test.tsx' lib/auth-session-cookie.ts app/api/auth/__tests__/auth-routes.test.ts --max-warnings=0`
- [x] `./node_modules/.bin/vitest run --config ./vitest.config.mts`



## fix(billing): keep sends after low-credit prompt (#2806)

- **SHA**: `ac7076eacfc658849b652c8229296e4a75cf59ab`
- **作者**: tim-srp
- **日期**: 2026-07-09T12:28:51Z
- **PR**: #2806

**完整 commit message:**

```
fix(billing): keep sends after low-credit prompt (#2806)

## Summary
- Keep the current message/task send going after the low-credit billing
prompt is shown.
- Preserve the 30-minute prompt cooldown behavior: first send can open
the subscription panel, cooldown sends show a toast.
- Update the cooldown toast copy so it does not imply the message was
blocked.

## Product decision
This PR intentionally makes the frontend billing send gate advisory:
providerless low-credit and billing-not-ready users should still have
the current send proceed after seeing a subscription panel or cooldown
toast. The same advisory behavior applies to later sends during the
30-minute cooldown window; the goal is frequent subscription visibility
without dropping user messages.

## Root cause
The previous billing gate treated providerless low-credit and
billing-not-ready states as hard blockers by returning false after
showing the panel/toast. Chat and new-chat callers interpret false as
canceling the in-flight send.

## Test plan
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/hooks/useBillingSendGate.unit.spec.ts
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/hooks/useBillingSendGate.unit.spec.ts
tests/unit/components/GiftPaywallFab.unit.spec.tsx
tests/unit/lib/billing/card-bind-gate.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/new-chat/useViewModel.unit.spec.tsx
- [x] pnpm --dir web/app run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
- [x] pnpm --dir web/app run lint:ci
- [x] pnpm --dir web/app run test:unit
- [x] git diff --check

Note: pnpm --dir web run tsc currently fails before typechecking because
the aggregate script calls pnpm exec with unsupported --if-present under
pnpm 10; web/app tsc passed.
```

**PR body:**

## Summary
- Keep the current message/task send going after the low-credit billing prompt is shown.
- Preserve the 30-minute prompt cooldown behavior: first send can open the subscription panel, cooldown sends show a toast.
- Update the cooldown toast copy so it does not imply the message was blocked.

## Product decision
This PR intentionally makes the frontend billing send gate advisory: providerless low-credit and billing-not-ready users should still have the current send proceed after seeing a subscription panel or cooldown toast. The same advisory behavior applies to later sends during the 30-minute cooldown window; the goal is frequent subscription visibility without dropping user messages.

## Root cause
The previous billing gate treated providerless low-credit and billing-not-ready states as hard blockers by returning false after showing the panel/toast. Chat and new-chat callers interpret false as canceling the in-flight send.

## Test plan
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/hooks/useBillingSendGate.unit.spec.ts
- [x] pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/hooks/useBillingSendGate.unit.spec.ts tests/unit/components/GiftPaywallFab.unit.spec.tsx tests/unit/lib/billing/card-bind-gate.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/new-chat/useViewModel.unit.spec.tsx
- [x] pnpm --dir web/app run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
- [x] pnpm --dir web/app run lint:ci
- [x] pnpm --dir web/app run test:unit
- [x] git diff --check

Note: pnpm --dir web run tsc currently fails before typechecking because the aggregate script calls pnpm exec with unsupported --if-present under pnpm 10; web/app tsc passed.


## feat(dashboard-console): add offline order management pages (#2802)

- **SHA**: `daa80b2a477aef4da52fc55dfe96500750acfd05`
- **作者**: bill-srp
- **日期**: 2026-07-09T12:22:20Z
- **PR**: #2802

**完整 commit message:**

```
feat(dashboard-console): add offline order management pages (#2802)

## Linear
<!-- 无对应 Linear issue；如需要可补充 -->

## Summary

Frontend half of the offline-order admin console (split from #2798;
backend endpoints in #2801). Admin UI in `web/dashboard-console` for the
full offline enterprise-payment lifecycle.

- `/offline-orders` — filterable (uid / status / package id, persisted
in URL search params), paginated table with a create dialog (uid →
package lookup → duration/amount/currency), new "Billing" sidebar
section.
- `/offline-orders/:orderId` — order/agreement/entitlement status
badges, full field grid, audit timeline, confirm/cancel dialogs (confirm
requires bank reference and warns that credits are granted). A
reconciliation banner appears for compensation states (`revoking` /
`revoke_failed` / `compensation_pending`), where the backend blocks
further actions.
- Error handling: backend conflict `detail` strings surface verbatim in
dialogs; conflicts that mean "state moved on" trigger a refetch. No
optimistic updates.

**Deploy dependency:** the create-form package picker and the detail
audit timeline consume the endpoints added in #2801; deploy
`claw-interface` with that change before (or with) this console release.
Design spec lives in #2801
(`docs/superpowers/specs/2026-07-09-offline-order-dashboard-console-design.md`).

## Test plan
- [x] vitest 280/280, eslint, `tsc -b`, production build all clean
- [x] Content identical to #2798, where dashboard-quality CI and both AI
reviews passed
- [ ] Staging smoke: create → confirm walkthrough with an admin account
```

**PR body:**

## Linear
<!-- 无对应 Linear issue；如需要可补充 -->

## Summary

Frontend half of the offline-order admin console (split from #2798; backend endpoints in #2801). Admin UI in `web/dashboard-console` for the full offline enterprise-payment lifecycle.

- `/offline-orders` — filterable (uid / status / package id, persisted in URL search params), paginated table with a create dialog (uid → package lookup → duration/amount/currency), new "Billing" sidebar section.
- `/offline-orders/:orderId` — order/agreement/entitlement status badges, full field grid, audit timeline, confirm/cancel dialogs (confirm requires bank reference and warns that credits are granted). A reconciliation banner appears for compensation states (`revoking` / `revoke_failed` / `compensation_pending`), where the backend blocks further actions.
- Error handling: backend conflict `detail` strings surface verbatim in dialogs; conflicts that mean "state moved on" trigger a refetch. No optimistic updates.

**Deploy dependency:** the create-form package picker and the detail audit timeline consume the endpoints added in #2801; deploy `claw-interface` with that change before (or with) this console release. Design spec lives in #2801 (`docs/superpowers/specs/2026-07-09-offline-order-dashboard-console-design.md`).

## Test plan
- [x] vitest 280/280, eslint, `tsc -b`, production build all clean
- [x] Content identical to #2798, where dashboard-quality CI and both AI reviews passed
- [ ] Staging smoke: create → confirm walkthrough with an admin account



## feat(dashboard-console): add isAdmin signal and AdminOnly guard (#2804)

- **SHA**: `afd70af5bdcd42e6a3a7dad006abd8f6d72bc81f`
- **作者**: bill-srp
- **日期**: 2026-07-09T11:58:11Z
- **PR**: #2804

**完整 commit message:**

```
feat(dashboard-console): add isAdmin signal and AdminOnly guard (#2804)

# Purpose

Plan 3 of the staff-admin relocation ([design
spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)):
give `web/dashboard-console` the admin infrastructure the upcoming Users
/ Subscription Codes / Releases pages (Plan 4) will sit on — an
`isAdmin` signal and an `AdminOnly` route-content guard. Follows the
backend slices #2774 / #2781 / #2783 / #2788 / #2796, which completed
the `/internal/*` admin API surface.

# Approach

- **Admin signal source = claw-interface `GET /account/me`** — it
appends `"admin"` to `permissions` for emails in the same
`get_admin_emails()` allowlist that backs `require_admin_user` on every
`/internal/*` admin endpoint (and it's how web/app's middleware checks
admin today). The console already calls claw-interface directly from the
browser, so this adds `accountMeUrl` (in `lib/claw-url.ts`) +
`getAccountMe` (in `lib/claw-api.ts`) following the module idioms. **The
shared `@zooclaw/auth-client` package is deliberately untouched** —
account-service `/user/me` does not carry this permission.
- **`useIsAdmin()` hook** — TanStack query with a **uid-scoped key** (an
account switch never reuses a stale admin flag), 5-minute staleTime
(focus refetches pick up allowlist changes), disabled when signed out,
**fail-closed** (any fetch error reads as not-admin) and never signs the
user out (claw-interface authz ≠ account session); errors are surfaced
separately with a `refresh` affordance.
- **`AdminOnly` guard** — renders inside the dashboard shell: spinner
while resolving, quiet `EmptyState` "Admin access required" for
non-admins, a distinct "Couldn't verify admin access" + Retry state for
failed permission checks (post-review hardening), children for admins.
UX-only mirror of the backend gate, same stance as `AuthGate`'s
`isSrpEmail` check.
- **Infra only, by design**: no nav entries, no `routes.ts` changes, no
home cards — each lands with its Plan-4 page (a nav entry without its
page is a dead link).

# Tests

- [x] 4 new/extended test files: `claw-url` builder cases, `claw-api`
fetcher (Bearer header, URL, ApiError on non-ok), `useIsAdmin` (admin /
non-admin / absent permissions / fetch-error fail-closed / signed-out
disabled / uid-scoped refetch), `AdminOnly` (loading / restricted /
children)
- [x] Full suite: 33 files / 256 tests pass; `useIsAdmin.tsx` and
`AdminOnly.tsx` at 100% coverage
- [x] `pnpm lint`, `pnpm typecheck` (wrangler types + react-router
typegen + tsc -b), `pnpm test` — all green (exactly what
`dashboard-quality` runs)

# Notes

- Implementation plan:
`docs/superpowers/plans/2026-07-09-console-admin-infra.md`
- Next: Plan 4 console pages (subscription-codes → releases → users);
the grant/boost modals must generate stable `idempotency_key`s per the
#2783/#2788 contracts.
```

**PR body:**

# Purpose

Plan 3 of the staff-admin relocation ([design spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)): give `web/dashboard-console` the admin infrastructure the upcoming Users / Subscription Codes / Releases pages (Plan 4) will sit on — an `isAdmin` signal and an `AdminOnly` route-content guard. Follows the backend slices #2774 / #2781 / #2783 / #2788 / #2796, which completed the `/internal/*` admin API surface.

# Approach

- **Admin signal source = claw-interface `GET /account/me`** — it appends `"admin"` to `permissions` for emails in the same `get_admin_emails()` allowlist that backs `require_admin_user` on every `/internal/*` admin endpoint (and it's how web/app's middleware checks admin today). The console already calls claw-interface directly from the browser, so this adds `accountMeUrl` (in `lib/claw-url.ts`) + `getAccountMe` (in `lib/claw-api.ts`) following the module idioms. **The shared `@zooclaw/auth-client` package is deliberately untouched** — account-service `/user/me` does not carry this permission.
- **`useIsAdmin()` hook** — TanStack query with a **uid-scoped key** (an account switch never reuses a stale admin flag), 5-minute staleTime (focus refetches pick up allowlist changes), disabled when signed out, **fail-closed** (any fetch error reads as not-admin) and never signs the user out (claw-interface authz ≠ account session); errors are surfaced separately with a `refresh` affordance.
- **`AdminOnly` guard** — renders inside the dashboard shell: spinner while resolving, quiet `EmptyState` "Admin access required" for non-admins, a distinct "Couldn't verify admin access" + Retry state for failed permission checks (post-review hardening), children for admins. UX-only mirror of the backend gate, same stance as `AuthGate`'s `isSrpEmail` check.
- **Infra only, by design**: no nav entries, no `routes.ts` changes, no home cards — each lands with its Plan-4 page (a nav entry without its page is a dead link).

# Tests

- [x] 4 new/extended test files: `claw-url` builder cases, `claw-api` fetcher (Bearer header, URL, ApiError on non-ok), `useIsAdmin` (admin / non-admin / absent permissions / fetch-error fail-closed / signed-out disabled / uid-scoped refetch), `AdminOnly` (loading / restricted / children)
- [x] Full suite: 33 files / 256 tests pass; `useIsAdmin.tsx` and `AdminOnly.tsx` at 100% coverage
- [x] `pnpm lint`, `pnpm typecheck` (wrangler types + react-router typegen + tsc -b), `pnpm test` — all green (exactly what `dashboard-quality` runs)

# Notes

- Implementation plan: `docs/superpowers/plans/2026-07-09-console-admin-infra.md`
- Next: Plan 4 console pages (subscription-codes → releases → users); the grant/boost modals must generate stable `idempotency_key`s per the #2783/#2788 contracts.



## feat(billing): add enterprise-package lookup and audit trail for offline orders (#2801)

- **SHA**: `8e396994797d32823d24cd87cf262b9cc95a336d`
- **作者**: bill-srp
- **日期**: 2026-07-09T11:37:45Z
- **PR**: #2801

**完整 commit message:**

```
feat(billing): add enterprise-package lookup and audit trail for offline orders (#2801)

## Linear
<!-- 无对应 Linear issue；如需要可补充 -->

## Summary

Backend half of the offline-order admin console (split from #2798;
frontend follows in #2802). Two small admin-gated additions to the
offline enterprise-payment surface shipped in #2765–#2767, plus the
design spec and implementation plan docs.

- `GET /internal/users/{uid}/enterprise-packages` (admin-gated) —
package picker source for the console's create form; new typed repo
method `vertical_pack_package_repo.list_by_uid`. The offline-order
create flow's owned-package validation remains authoritative.
- `GET /internal/offline-order/{id}` now includes an `audit` array
(action, from/to status, actor, note, timestamp) sourced from the
existing billing-audit repo. The list endpoint is unchanged.

Design spec:
`docs/superpowers/specs/2026-07-09-offline-order-dashboard-console-design.md`.

## Test plan
- [x] New + existing offline-order/users unit suites pass
(devcontainer); ruff, ruff-format, pyright (0 errors), import-linter
(8/8 contracts) clean
- [x] Content identical to #2798, where the full CI matrix (including
claw-interface coverage gate) and both AI reviews passed
```

**PR body:**

## Linear
<!-- 无对应 Linear issue；如需要可补充 -->

## Summary

Backend half of the offline-order admin console (split from #2798; frontend follows in #2802). Two small admin-gated additions to the offline enterprise-payment surface shipped in #2765–#2767, plus the design spec and implementation plan docs.

- `GET /internal/users/{uid}/enterprise-packages` (admin-gated) — package picker source for the console's create form; new typed repo method `vertical_pack_package_repo.list_by_uid`. The offline-order create flow's owned-package validation remains authoritative.
- `GET /internal/offline-order/{id}` now includes an `audit` array (action, from/to status, actor, note, timestamp) sourced from the existing billing-audit repo. The list endpoint is unchanged.

Design spec: `docs/superpowers/specs/2026-07-09-offline-order-dashboard-console-design.md`.

## Test plan
- [x] New + existing offline-order/users unit suites pass (devcontainer); ruff, ruff-format, pyright (0 errors), import-linter (8/8 contracts) clean
- [x] Content identical to #2798, where the full CI matrix (including claw-interface coverage gate) and both AI reviews passed



## fix(billing): look up org wallets before creating (#2803)

- **SHA**: `1d42e56f8cceebd862828a18d7784b1b1d7ac572`
- **作者**: bill-srp
- **日期**: 2026-07-09T11:32:12Z
- **PR**: #2803

**完整 commit message:**

```
fix(billing): look up org wallets before creating (#2803)

## Summary

- add Billing Gateway client support for `GET
/billing/customers/{customer_id}/wallets`
- make team-org wallet provisioning always look up existing wallets
before creating missing ones
- remove the wallet-path dependency on Billing Gateway `team_created`
- treat a wallet lookup 404 as "no reusable wallets yet" so first-time
team org creation can still create wallets
- move the shared GET retry helper out of `billing_client.py` to keep
the file under CI's length limit

## Tests

- `/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_billing_client.py
services/claw-interface/tests/unit/test_org_service.py -q` (`116
passed`)
- `/Users/bill/.venvs/claw-interface/bin/ruff check
services/claw-interface/app/services/billing_client.py
services/claw-interface/app/services/billing_client_utils.py
services/claw-interface/app/services/org/org_service.py
services/claw-interface/tests/unit/test_billing_client.py
services/claw-interface/tests/unit/test_org_service.py`
- `/Users/bill/.venvs/claw-interface/bin/ruff format --check
services/claw-interface/app/services/billing_client.py
services/claw-interface/app/services/billing_client_utils.py
services/claw-interface/app/services/org/org_service.py
services/claw-interface/tests/unit/test_billing_client.py
services/claw-interface/tests/unit/test_org_service.py`
- `cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh`

## Notes

- `bash scripts/verify-py.sh` was also attempted. Its ruff and
import-linter stages passed, but local pyright failed because
`services/claw-interface/.venv` cannot resolve installed dependencies
such as `fastapi`, `httpx`, and `pytest` in this checkout.
```

**PR body:**

## Summary

- add Billing Gateway client support for `GET /billing/customers/{customer_id}/wallets`
- make team-org wallet provisioning always look up existing wallets before creating missing ones
- remove the wallet-path dependency on Billing Gateway `team_created`
- treat a wallet lookup 404 as "no reusable wallets yet" so first-time team org creation can still create wallets
- move the shared GET retry helper out of `billing_client.py` to keep the file under CI's length limit

## Tests

- `/Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_billing_client.py services/claw-interface/tests/unit/test_org_service.py -q` (`116 passed`)
- `/Users/bill/.venvs/claw-interface/bin/ruff check services/claw-interface/app/services/billing_client.py services/claw-interface/app/services/billing_client_utils.py services/claw-interface/app/services/org/org_service.py services/claw-interface/tests/unit/test_billing_client.py services/claw-interface/tests/unit/test_org_service.py`
- `/Users/bill/.venvs/claw-interface/bin/ruff format --check services/claw-interface/app/services/billing_client.py services/claw-interface/app/services/billing_client_utils.py services/claw-interface/app/services/org/org_service.py services/claw-interface/tests/unit/test_billing_client.py services/claw-interface/tests/unit/test_org_service.py`
- `cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh`

## Notes

- `bash scripts/verify-py.sh` was also attempted. Its ruff and import-linter stages passed, but local pyright failed because `services/claw-interface/.venv` cannot resolve installed dependencies such as `fastapi`, `httpx`, and `pytest` in this checkout.



## fix(billing): rate-limit low-credit paywall prompts (#2800)

- **SHA**: `d6ec8cfe24d6a2334eabdf600372b70363a2e1c3`
- **作者**: tim-srp
- **日期**: 2026-07-09T11:20:21Z
- **PR**: #2800

**完整 commit message:**

```
fix(billing): rate-limit low-credit paywall prompts (#2800)

## Summary
- Keep the existing billing send-gate result for low-credit/providerless
users: blocked paths still return false.
- Rate-limit the subscription panel prompt to once per uid per 30-minute
browser session window.
- Add unit coverage for blocked-result preservation, cooldown
boundaries, and cross-hook-instance cooldown.

## Verification
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/hooks/useBillingSendGate.unit.spec.ts
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/new-chat/useViewModel.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit --pretty false
- pnpm --dir web/app run lint
- git diff --check
```

**PR body:**

## Summary
- Keep the existing billing send-gate result for low-credit/providerless users: blocked paths still return false.
- Rate-limit the subscription panel prompt to once per uid per 30-minute browser session window.
- Add unit coverage for blocked-result preservation, cooldown boundaries, and cross-hook-instance cooldown.

## Verification
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/hooks/useBillingSendGate.unit.spec.ts tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/new-chat/useViewModel.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit --pretty false
- pnpm --dir web/app run lint
- git diff --check


## feat(claw-interface): add GET /internal/users/{uid}/credits admin credits check (#2796)

- **SHA**: `5d43112fa8d65e39d78a47e1a92e1478e4766124`
- **作者**: bill-srp
- **日期**: 2026-07-09T10:55:50Z
- **PR**: #2796

**完整 commit message:**

```
feat(claw-interface): add GET /internal/users/{uid}/credits admin credits check (#2796)

# Purpose

Plan 2b-credits-check of the staff-admin relocation ([design
spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)):
add the admin-only `GET
/internal/users/{uid}/credits?expected_credits=N` endpoint (balance +
subscription-context read, check-shaped) for the dashboard-console
grant/boost modals. Follow-up to #2774, #2781, #2783, #2788 — the last
backend slice of Plan 2.

# Approach

Unlike grant/boost (copy-then-delegate), this slice **moves live code**
— the shared helpers serve four live self-service endpoints, and
near-verbatim duplication is no longer possible (the jscpd `app/` gate
sits at 3.0%/3% since #2788):

- **`app/services/user/credits_context.py`** (new, FastAPI-free): the
~13 module-private helpers move out of `app/routes/credits.py` verbatim
under public names. One behavioral seam: `raise_billing_not_ready` now
raises the `DependencyNotReadyError` domain error instead of
`HTTPException(503)`.
- **`app/services/user/credits_read.py`** (new, FastAPI-free): the whole
`/users/credits/check` flow moves into `check_user_credits_flow(uid,
expected_credits)` — including the ECA-669 duplicate-wallet summing —
raising `NotFoundError` / letting `DependencyNotReadyError` bubble.
- **Live wire shapes are byte-identical**: the four live handlers
become/stay thin and each translates `DependencyNotReadyError` back to
the legacy `503 {"error": "billing_not_ready", ...}` (clause placed
before the generic `except Exception`, which would otherwise silently
turn live 503s into 500s); `NotFoundError` → legacy `404 "User not
found"`; generic errors keep their legacy 500 messages.
- **`GET /internal/users/{uid}/credits`**: thin handler on the
admin-gated `/internal/users` sub-router calling the same service;
domain errors are shaped by the global handlers (`{"code":
"user.not_found"}` 404, `{"code": "billing.not_ready"}` 503). Same
response shape the legacy admin grant modal already renders — drop-in
for Plan 4.

# Tests

- [x] `tests/unit/test_user_credits.py` (the 25-test live regression
net): **mechanical patch-target/rename updates only — zero assertion
changes**; all pass. Same for `test_billing_v2_user_public_response.py`
(imported the moved helpers).
- [x] 13 new tests (`test_internal_users_credits.py`): user-not-found;
personal happy path (terminated wallet excluded, duplicate subscription
wallets summed per ECA-669, string balances normalized); team-billing
path; no-subscription-without-ready-profile short-circuit; BG 400 →
no-subscription vs non-400 re-raise; `DependencyNotReadyError` bubbling;
`_id` stripping; internal route delegation; legacy-shape translation
proofs (503/404/500)
- [x] Coverage: `credits_context.py` **100%**, `credits_read.py`
**100%**; `routes/credits.py` 91.5% (residual misses are pre-existing
branches)
- [x] ruff + format, pyright 0 errors, import-linter 8 kept / 0 broken
(C3: new services FastAPI-free), broad `-k "credits or internal or boost
or grant"` sweep: 387 passed

# Notes

- Implementation plan:
`docs/superpowers/plans/2026-07-09-internal-users-credits-check.md`
- Local BDD billing regression not run (mongo down locally) — covered by
CI's `claw-interface-quality / test`.
- Legacy BFF `web/app/api/admin/users/credits/check` untouched — retired
at the Plan-5 teardown, which can now also drop the arbitrary-`uid`
query support from the self-service endpoints.
```

**PR body:**

# Purpose

Plan 2b-credits-check of the staff-admin relocation ([design spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)): add the admin-only `GET /internal/users/{uid}/credits?expected_credits=N` endpoint (balance + subscription-context read, check-shaped) for the dashboard-console grant/boost modals. Follow-up to #2774, #2781, #2783, #2788 — the last backend slice of Plan 2.

# Approach

Unlike grant/boost (copy-then-delegate), this slice **moves live code** — the shared helpers serve four live self-service endpoints, and near-verbatim duplication is no longer possible (the jscpd `app/` gate sits at 3.0%/3% since #2788):

- **`app/services/user/credits_context.py`** (new, FastAPI-free): the ~13 module-private helpers move out of `app/routes/credits.py` verbatim under public names. One behavioral seam: `raise_billing_not_ready` now raises the `DependencyNotReadyError` domain error instead of `HTTPException(503)`.
- **`app/services/user/credits_read.py`** (new, FastAPI-free): the whole `/users/credits/check` flow moves into `check_user_credits_flow(uid, expected_credits)` — including the ECA-669 duplicate-wallet summing — raising `NotFoundError` / letting `DependencyNotReadyError` bubble.
- **Live wire shapes are byte-identical**: the four live handlers become/stay thin and each translates `DependencyNotReadyError` back to the legacy `503 {"error": "billing_not_ready", ...}` (clause placed before the generic `except Exception`, which would otherwise silently turn live 503s into 500s); `NotFoundError` → legacy `404 "User not found"`; generic errors keep their legacy 500 messages.
- **`GET /internal/users/{uid}/credits`**: thin handler on the admin-gated `/internal/users` sub-router calling the same service; domain errors are shaped by the global handlers (`{"code": "user.not_found"}` 404, `{"code": "billing.not_ready"}` 503). Same response shape the legacy admin grant modal already renders — drop-in for Plan 4.

# Tests

- [x] `tests/unit/test_user_credits.py` (the 25-test live regression net): **mechanical patch-target/rename updates only — zero assertion changes**; all pass. Same for `test_billing_v2_user_public_response.py` (imported the moved helpers).
- [x] 13 new tests (`test_internal_users_credits.py`): user-not-found; personal happy path (terminated wallet excluded, duplicate subscription wallets summed per ECA-669, string balances normalized); team-billing path; no-subscription-without-ready-profile short-circuit; BG 400 → no-subscription vs non-400 re-raise; `DependencyNotReadyError` bubbling; `_id` stripping; internal route delegation; legacy-shape translation proofs (503/404/500)
- [x] Coverage: `credits_context.py` **100%**, `credits_read.py` **100%**; `routes/credits.py` 91.5% (residual misses are pre-existing branches)
- [x] ruff + format, pyright 0 errors, import-linter 8 kept / 0 broken (C3: new services FastAPI-free), broad `-k "credits or internal or boost or grant"` sweep: 387 passed

# Notes

- Implementation plan: `docs/superpowers/plans/2026-07-09-internal-users-credits-check.md`
- Local BDD billing regression not run (mongo down locally) — covered by CI's `claw-interface-quality / test`.
- Legacy BFF `web/app/api/admin/users/credits/check` untouched — retired at the Plan-5 teardown, which can now also drop the arbitrary-`uid` query support from the self-service endpoints.



## fix(billing): gate free-access users on card binding (#2786)

- **SHA**: `00aff2ab017266fdb38aa438454f4a03ebe41ae5`
- **作者**: tim-srp
- **日期**: 2026-07-09T08:39:27Z
- **PR**: #2786

**完整 commit message:**

```
fix(billing): gate free-access users on card binding (#2786)

## Summary
- Change invite binding from trial-credit grant to zero-credit seven-day
free access.
- Add a provider-backed subscription gate so real Stripe/Antom
subscribers keep the existing low-credit banner flow.
- Auto-open the existing card-binding paywall once per browser session
on `/chat` and `/new-chat` for providerless users.
- Block every chat/new-chat send attempt for providerless users when the
real-time credits check is insufficient.
- Add a conservative positive credits cache: 30-minute TTL, cache only
when `available_credits >= 50`, locally reserve expected credits, and
fail open after a 3-second credits-check timeout.

## Testing
- `NODE_OPTIONS=--no-deprecation ./node_modules/.bin/vitest run --config
./vitest.config.mts tests/unit/lib/billing/card-bind-gate.unit.spec.ts
tests/unit/hooks/useBillingSendGate.unit.spec.ts
tests/unit/components/GiftPaywallFab.unit.spec.tsx
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/new-chat/useViewModel.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx`
- `NODE_OPTIONS=--no-deprecation ./node_modules/.bin/tsc --noEmit
--pretty false`
- `pnpm lint:imports`
- `pnpm run lint` from `web` (0 errors; existing enterprise-app
warnings)
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit --pretty false`
- `pnpm --filter @zooclaw/web-app run test:unit`
- `pytest
services/claw-interface/tests/unit/test_user_bind_invite_trial.py
services/claw-interface/tests/unit/test_user_free_access_service.py -q`
- `ruff check .` from `services/claw-interface`
- `pyright --pythonpath "$(which python)"
tests/unit/test_user_bind_invite_trial.py` from
`services/claw-interface`

## Notes
- I also started the full backend coverage command locally, but stopped
it after several minutes because this local Python/protobuf warning
configuration was producing unrelated admin cron setup errors; the
affected backend tests above pass.
```

**PR body:**

## Summary
- Change invite binding from trial-credit grant to zero-credit seven-day free access.
- Add a provider-backed subscription gate so real Stripe/Antom subscribers keep the existing low-credit banner flow.
- Auto-open the existing card-binding paywall once per browser session on `/chat` and `/new-chat` for providerless users.
- Block every chat/new-chat send attempt for providerless users when the real-time credits check is insufficient.
- Add a conservative positive credits cache: 30-minute TTL, cache only when `available_credits >= 50`, locally reserve expected credits, and fail open after a 3-second credits-check timeout.

## Testing
- `NODE_OPTIONS=--no-deprecation ./node_modules/.bin/vitest run --config ./vitest.config.mts tests/unit/lib/billing/card-bind-gate.unit.spec.ts tests/unit/hooks/useBillingSendGate.unit.spec.ts tests/unit/components/GiftPaywallFab.unit.spec.tsx tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/new-chat/useViewModel.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx`
- `NODE_OPTIONS=--no-deprecation ./node_modules/.bin/tsc --noEmit --pretty false`
- `pnpm lint:imports`
- `pnpm run lint` from `web` (0 errors; existing enterprise-app warnings)
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit --pretty false`
- `pnpm --filter @zooclaw/web-app run test:unit`
- `pytest services/claw-interface/tests/unit/test_user_bind_invite_trial.py services/claw-interface/tests/unit/test_user_free_access_service.py -q`
- `ruff check .` from `services/claw-interface`
- `pyright --pythonpath "$(which python)" tests/unit/test_user_bind_invite_trial.py` from `services/claw-interface`

## Notes
- I also started the full backend coverage command locally, but stopped it after several minutes because this local Python/protobuf warning configuration was producing unrelated admin cron setup errors; the affected backend tests above pass.



## refactor(ios): resolve arch-review #2505 findings F5, F6 (#2797)

- **SHA**: `0c1e919f855c49285c165c60bf836261172e75d1`
- **作者**: bill-srp
- **日期**: 2026-07-09T08:00:13Z
- **PR**: #2797

**完整 commit message:**

```
refactor(ios): resolve arch-review #2505 findings F5, F6 (#2797)

## Summary

Resolves the two active findings in iOS arch-review cohort #2505 (module
`ios`). Both are behavior-preserving refactors; one commit per finding.

Closes the F5/F6 findings tracked in #2505.

## F6 — Duplication: image prefetch re-converts already-converted posts

`syncMessages(_:)` already calls `post.toChatMessage(...)` for every
displayable post while building the message array, then
`prefetchImages(for: posts)` re-ran `shouldDisplay` + `toChatMessage` on
the same posts purely to extract image URLs — double work and two call
sites of the conversion to keep in sync.

- `syncMessages` now collects the `ChatMessage`s it already builds into
a batch-local array and passes them to `prefetchImages(for messages:
[ChatMessage])`.
- **Batch-locality preserved.** The prefetch still operates on the
current sync *batch* (not the full message list), so `loadMoreHistory()`
— which syncs *older* posts — keeps prefetching the correct batch's
images rather than the newest.
- Documented edge: the `suffix(20)` window is now over displayable
converted messages rather than raw posts. These differ only when hidden
posts sit in the raw tail, in which case the new set is a harmless
superset (prefetch is best-effort cache-warming, capped at 20).

## F5 — Separation of Concerns: `ZooClawApp` mixed 4 concerns (468
lines)

Split SDK init and session-validation routing out of the `App` struct so
routing is unit-testable and the file is no longer a grab-bag.

- **`AppSetup.swift`** (new) — pure move of `setupSentry` /
`setupFirebase` / `setupAppsFlyer` + the Sentry DSN into an `enum
AppSetup` namespace. All `#if STAGING` / `#if !os(macOS)` guards
preserved.
- **`AppCoordinator.swift`** (new) — an `@Observable @MainActor` class
that owns `appRoute` and hosts `resolveUserAndStartScreen` /
`ejectToOnboarding` / `completeOnboarding` / `handleSignedOut`.
Collaborators are injected via a closure-based `Dependencies` struct, so
route decisions are testable without instantiating the full app.
- **`ZooClawApp.swift`** — 468 → 341 lines. Keeps scene-lifecycle
modifiers; all four `appRoute` touchpoints (body switch,
`preferredColorScheme`, push-notification guard, foreground-retry check)
now read through the coordinator.
- **`AppCoordinatorTests.swift`** (new) — Swift Testing coverage for
token-rejection → onboarding, network-error → stays on chat, missing-uid
→ onboarding.

Auth-critical semantics were verified line-by-line against the
originals: network-error-stays-on-`.chat`, token-reject / missing-uid
eject, the `async let` fan-out ordering, and the eject/sign-out teardown
order are unchanged. (The network-error test pins the exact branch that
regressed in the #365 F4 fix.)

## Test plan

Local (iOS has no compile CI — xcodebuild is the local gate):

- [x] `xcodebuild build-for-testing -destination 'platform=iOS
Simulator,name=iPhone 17 Pro,OS=26.5'` — **TEST BUILD SUCCEEDED** (app +
test target compiled)
- [x] `swiftlint --no-cache` — **0 violations / 275 files**
- [x] No new compiler warnings (the pre-existing warnings only shifted
line numbers)
- [ ] Full simulator test run (`xcodebuild test`) not executed locally —
relying on the compiled test target + CI `ios-quality`

Ref: #2505
```

**PR body:**

## Summary

Resolves the two active findings in iOS arch-review cohort #2505 (module `ios`). Both are behavior-preserving refactors; one commit per finding.

Closes the F5/F6 findings tracked in #2505.

## F6 — Duplication: image prefetch re-converts already-converted posts

`syncMessages(_:)` already calls `post.toChatMessage(...)` for every displayable post while building the message array, then `prefetchImages(for: posts)` re-ran `shouldDisplay` + `toChatMessage` on the same posts purely to extract image URLs — double work and two call sites of the conversion to keep in sync.

- `syncMessages` now collects the `ChatMessage`s it already builds into a batch-local array and passes them to `prefetchImages(for messages: [ChatMessage])`.
- **Batch-locality preserved.** The prefetch still operates on the current sync *batch* (not the full message list), so `loadMoreHistory()` — which syncs *older* posts — keeps prefetching the correct batch's images rather than the newest.
- Documented edge: the `suffix(20)` window is now over displayable converted messages rather than raw posts. These differ only when hidden posts sit in the raw tail, in which case the new set is a harmless superset (prefetch is best-effort cache-warming, capped at 20).

## F5 — Separation of Concerns: `ZooClawApp` mixed 4 concerns (468 lines)

Split SDK init and session-validation routing out of the `App` struct so routing is unit-testable and the file is no longer a grab-bag.

- **`AppSetup.swift`** (new) — pure move of `setupSentry` / `setupFirebase` / `setupAppsFlyer` + the Sentry DSN into an `enum AppSetup` namespace. All `#if STAGING` / `#if !os(macOS)` guards preserved.
- **`AppCoordinator.swift`** (new) — an `@Observable @MainActor` class that owns `appRoute` and hosts `resolveUserAndStartScreen` / `ejectToOnboarding` / `completeOnboarding` / `handleSignedOut`. Collaborators are injected via a closure-based `Dependencies` struct, so route decisions are testable without instantiating the full app.
- **`ZooClawApp.swift`** — 468 → 341 lines. Keeps scene-lifecycle modifiers; all four `appRoute` touchpoints (body switch, `preferredColorScheme`, push-notification guard, foreground-retry check) now read through the coordinator.
- **`AppCoordinatorTests.swift`** (new) — Swift Testing coverage for token-rejection → onboarding, network-error → stays on chat, missing-uid → onboarding.

Auth-critical semantics were verified line-by-line against the originals: network-error-stays-on-`.chat`, token-reject / missing-uid eject, the `async let` fan-out ordering, and the eject/sign-out teardown order are unchanged. (The network-error test pins the exact branch that regressed in the #365 F4 fix.)

## Test plan

Local (iOS has no compile CI — xcodebuild is the local gate):

- [x] `xcodebuild build-for-testing -destination 'platform=iOS Simulator,name=iPhone 17 Pro,OS=26.5'` — **TEST BUILD SUCCEEDED** (app + test target compiled)
- [x] `swiftlint --no-cache` — **0 violations / 275 files**
- [x] No new compiler warnings (the pre-existing warnings only shifted line numbers)
- [ ] Full simulator test run (`xcodebuild test`) not executed locally — relying on the compiled test target + CI `ios-quality`

Ref: #2505



## fix(web): avoid sending chat on IME commit enter (#2795)

- **SHA**: `2bd72630066dd617dee78220a02e713c7594452a`
- **作者**: bill-srp
- **日期**: 2026-07-09T07:27:08Z
- **PR**: #2795

**完整 commit message:**

```
fix(web): avoid sending chat on IME commit enter (#2795)

## Summary

- Treat IME Enter commit events with keyCode/which 229 as composition
events in RichTextInput.
- Keep normal Enter-to-send and Shift+Enter newline behavior unchanged.
- Add a regression test for IME Enter committing preedit text without
triggering submit.

## Tests

- `./node_modules/.bin/vitest run
tests/unit/components/RichTextInput.unit.spec.tsx`
- `./node_modules/.bin/tsc --noEmit --target ES2022 --module ESNext
--moduleResolution bundler --jsx react-jsx --types react
src/components/rich-text-input/hooks/useRichTextKeyboard.ts`
- `git diff --check --
web/app/src/components/rich-text-input/hooks/useRichTextKeyboard.ts
web/app/tests/unit/components/RichTextInput.unit.spec.tsx`

## Notes

- `bash scripts/verify-web.sh
web/app/src/components/rich-text-input/hooks/useRichTextKeyboard.ts
web/app/tests/unit/components/RichTextInput.unit.spec.tsx` could not
complete locally because its `pnpm exec` steps hit
`ERR_PNPM_MISSING_TARBALL_INTEGRITY` for
`xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`; the
verifier's governance guards passed before that dependency-resolution
failure.
```

**PR body:**

## Summary

- Treat IME Enter commit events with keyCode/which 229 as composition events in RichTextInput.
- Keep normal Enter-to-send and Shift+Enter newline behavior unchanged.
- Add a regression test for IME Enter committing preedit text without triggering submit.

## Tests

- `./node_modules/.bin/vitest run tests/unit/components/RichTextInput.unit.spec.tsx`
- `./node_modules/.bin/tsc --noEmit --target ES2022 --module ESNext --moduleResolution bundler --jsx react-jsx --types react src/components/rich-text-input/hooks/useRichTextKeyboard.ts`
- `git diff --check -- web/app/src/components/rich-text-input/hooks/useRichTextKeyboard.ts web/app/tests/unit/components/RichTextInput.unit.spec.tsx`

## Notes

- `bash scripts/verify-web.sh web/app/src/components/rich-text-input/hooks/useRichTextKeyboard.ts web/app/tests/unit/components/RichTextInput.unit.spec.tsx` could not complete locally because its `pnpm exec` steps hit `ERR_PNPM_MISSING_TARBALL_INTEGRITY` for `xlsx@https://cdn.sheetjs.com/xlsx-0.20.3/xlsx-0.20.3.tgz`; the verifier's governance guards passed before that dependency-resolution failure.



## fix(claw-interface): expose pack version asset id (#2794)

- **SHA**: `996216b36a9b6997012ce667c1bc3e94057c2827`
- **作者**: bill-srp
- **日期**: 2026-07-09T06:17:43Z
- **PR**: #2794

**完整 commit message:**

```
fix(claw-interface): expose pack version asset id (#2794)

## Summary
- Expose `asset_id` on public `/agent-packs/{pack_id}/versions` version
items.
- Update the public route contract test to require the approved
submission asset id while keeping internal review fields hidden.

## Root cause
The route already converts approved `PackSubmission` rows into
`PublicPackVersion`, but the public response model did not include
`asset_id`, so Pydantic dropped it during model validation.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_public_agent_packs_routes.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff check
services/claw-interface/app/schema/pack.py
services/claw-interface/tests/unit/test_public_agent_packs_routes.py`
- [x] `git diff --check`
- [ ] `bash scripts/verify-py.sh` blocked locally: ruff and
import-linter passed, but pyright resolved through the local
`services/claw-interface/.venv` toolchain and reported missing imports
for dependencies such as `fastapi`, `pytest`, and `favie_common`.
```

**PR body:**

## Summary
- Expose `asset_id` on public `/agent-packs/{pack_id}/versions` version items.
- Update the public route contract test to require the approved submission asset id while keeping internal review fields hidden.

## Root cause
The route already converts approved `PackSubmission` rows into `PublicPackVersion`, but the public response model did not include `asset_id`, so Pydantic dropped it during model validation.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_public_agent_packs_routes.py -q`
- [x] `/Users/bill/.venvs/claw-interface/bin/ruff check services/claw-interface/app/schema/pack.py services/claw-interface/tests/unit/test_public_agent_packs_routes.py`
- [x] `git diff --check`
- [ ] `bash scripts/verify-py.sh` blocked locally: ruff and import-linter passed, but pyright resolved through the local `services/claw-interface/.venv` toolchain and reported missing imports for dependencies such as `fastapi`, `pytest`, and `favie_common`.



## docs(web): add SMS compliance terms to legal pages (#2789)

- **SHA**: `ee8f9cde33e526262d0ee9279e88c2955bd50b3b`
- **作者**: sam-srp
- **日期**: 2026-07-09T06:04:05Z
- **PR**: #2789

**完整 commit message:**

```
docs(web): add SMS compliance terms to legal pages (#2789)

## Summary
- add SMS communication terms to the public Terms page, including
program name, message frequency, rates notice, STOP opt-out, HELP
support, and legal links
- add SMS/mobile data handling details to the public Privacy page
- keep localized legal routes aligned and normalize SMS support contact
email to support@zooclaw.ai

## Validation
- git diff --check
- CI=true npx -y pnpm@10.26.2 --filter @zooclaw/web-app lint

Note: lint emitted the existing local Node warning because this machine
is on Node v25.6.1 while the project expects >=24 <25; lint completed
successfully.
```

**PR body:**

## Summary
- add SMS communication terms to the public Terms page, including program name, message frequency, rates notice, STOP opt-out, HELP support, and legal links
- add SMS/mobile data handling details to the public Privacy page
- keep localized legal routes aligned and normalize SMS support contact email to support@zooclaw.ai

## Validation
- git diff --check
- CI=true npx -y pnpm@10.26.2 --filter @zooclaw/web-app lint

Note: lint emitted the existing local Node warning because this machine is on Node v25.6.1 while the project expects >=24 <25; lint completed successfully.


## feat(whatsapp): add webhook business logs (#2793)

- **SHA**: `466d981ba3ae58a94e60da63fd0b86c65e1fceab`
- **作者**: bill-srp
- **日期**: 2026-07-09T05:59:18Z
- **PR**: #2793

**完整 commit message:**

```
feat(whatsapp): add webhook business logs (#2793)

## Linear
N/A

## Summary
- Add structured WhatsApp webhook business logs for intake, per-message
routing state, claim state, completion, retries, and skipped messages.
- Mask WhatsApp sender identifiers and avoid logging message text,
WhatsApp access tokens, or Mattermost tokens.
- Cover the logging contract with a focused app-level test.

## Test plan
- [x] `bash scripts/verify-changed.sh` (no locally verifiable surfaces
changed vs origin/main)
- [x] `cd services/whatsapp-business-service &&
./node_modules/.bin/vitest run src/app.test.ts` (49 tests)
- [x] `cd services/whatsapp-business-service && ./node_modules/.bin/tsc
--noEmit`
- [x] `cd services/whatsapp-business-service && ./node_modules/.bin/tsc
-p tsconfig.build.json`
- [x] `git diff --check`
```

**PR body:**

## Linear
N/A

## Summary
- Add structured WhatsApp webhook business logs for intake, per-message routing state, claim state, completion, retries, and skipped messages.
- Mask WhatsApp sender identifiers and avoid logging message text, WhatsApp access tokens, or Mattermost tokens.
- Cover the logging contract with a focused app-level test.

## Test plan
- [x] `bash scripts/verify-changed.sh` (no locally verifiable surfaces changed vs origin/main)
- [x] `cd services/whatsapp-business-service && ./node_modules/.bin/vitest run src/app.test.ts` (49 tests)
- [x] `cd services/whatsapp-business-service && ./node_modules/.bin/tsc --noEmit`
- [x] `cd services/whatsapp-business-service && ./node_modules/.bin/tsc -p tsconfig.build.json`
- [x] `git diff --check`



## refactor(ios): resolve arch-review #365 findings F1-F4 (#2791)

- **SHA**: `84a683f6f48497207f82bd212f95b9c82f679208`
- **作者**: bill-srp
- **日期**: 2026-07-09T04:24:04Z
- **PR**: #2791

**完整 commit message:**

```
refactor(ios): resolve arch-review #365 findings F1-F4 (#2791)

## Summary

Resolves all four active findings from the rolling iOS arch-review issue
#365, one behavior-preserving commit per finding:

- **F2 — `ImageCacheService` defined inside a View file**: moved the
shared `actor ImageCacheService` out of
`Views/Chat/CachedAsyncImage.swift` into
`Services/ImageCacheService.swift`, restoring the Services → ViewModels
→ Views layering. Pure move; no `project.pbxproj` edit needed
(filesystem-synchronized groups).
- **F1 — `AccountService` duplicated HTTP boilerplate**: extracted one
private generic `request<T: Decodable>(endpoint:method:options:)` helper
plus a `RequestOptions` struct. All four public methods
(`exchangeToken`, `verifyUser`, `sendEmailOTP`, `verifyEmailOTP`) now
delegate to it. Preserved per-endpoint semantics: `fb-token` vs
`Authorization` headers, `business=ecap` query param, 10/5/10/10s
timeouts, Sentry tags, inactive-user check, and verify-OTP HTTP
error-body logging (via `httpErrorHandler`). 281 → 226 lines.
- **F4 — `stopRecording()` interleaved async branching**: extracted the
`.connecting` busy-wait into a named helper; `stopRecording()` is now a
flat fallback/realtime decision tree (see review follow-up below for the
final shape).
- **F3 — `AppTheme` adaptive colors forced `colorScheme` threading**:
replaced the six `adaptive*(colorScheme)` static funcs with static
`Color` properties backed by `UIColor` trait providers, migrated all 37
call sites across 10 view files, and removed now-unused
`@Environment(\.colorScheme)` declarations. Inlined light values
verified identical to the original token constants.

Implementation delegated to Codex; each seam diff was manually reviewed
before commit.

**Review follow-up (85544511d)**: Codex review flagged a P1 on the F4
slice — the `!ready → fallback` shape (taken verbatim from the issue's
recommendation) changed cancel/timeout semantics: a cancel during the
10s connect wait would have fallback-transcribed a recording whose file
`cancelRecording()` already deleted, and a wait timeout skipped the
realtime commit attempt. Fixed by restoring the original decision
structure (pre-wait fallback check → wait → post-wait fallback check →
state guard) with a pure `waitWhileConnecting(timeout:)` helper; the
file's diff vs `main` is now a pure extraction.

## Test plan
- [x] Scoped SwiftLint over all 15 touched Swift files: 0 violations
- [x] Grep verification: `ImageCacheService` only in `Services/`; single
request/decode path in `AccountService`; polling loop only in
`waitWhileConnecting`; zero remaining calls to the old
`adaptive*(colorScheme)` API
- [ ] **Xcode build + unit tests not run** (no Xcode toolchain in this
environment, and `ios/` has no CI coverage) — please build and
smoke-test locally before merge, especially light/dark rendering of the
10 migrated views

## Related

- Addresses findings F1–F4 of the rolling arch-review issue #365 (issue
is auto-maintained weekly; next scan should mark them resolved)
```

**PR body:**

## Summary

Resolves all four active findings from the rolling iOS arch-review issue #365, one behavior-preserving commit per finding:

- **F2 — `ImageCacheService` defined inside a View file**: moved the shared `actor ImageCacheService` out of `Views/Chat/CachedAsyncImage.swift` into `Services/ImageCacheService.swift`, restoring the Services → ViewModels → Views layering. Pure move; no `project.pbxproj` edit needed (filesystem-synchronized groups).
- **F1 — `AccountService` duplicated HTTP boilerplate**: extracted one private generic `request<T: Decodable>(endpoint:method:options:)` helper plus a `RequestOptions` struct. All four public methods (`exchangeToken`, `verifyUser`, `sendEmailOTP`, `verifyEmailOTP`) now delegate to it. Preserved per-endpoint semantics: `fb-token` vs `Authorization` headers, `business=ecap` query param, 10/5/10/10s timeouts, Sentry tags, inactive-user check, and verify-OTP HTTP error-body logging (via `httpErrorHandler`). 281 → 226 lines.
- **F4 — `stopRecording()` interleaved async branching**: extracted the `.connecting` busy-wait into a named helper; `stopRecording()` is now a flat fallback/realtime decision tree (see review follow-up below for the final shape).
- **F3 — `AppTheme` adaptive colors forced `colorScheme` threading**: replaced the six `adaptive*(colorScheme)` static funcs with static `Color` properties backed by `UIColor` trait providers, migrated all 37 call sites across 10 view files, and removed now-unused `@Environment(\.colorScheme)` declarations. Inlined light values verified identical to the original token constants.

Implementation delegated to Codex; each seam diff was manually reviewed before commit.

**Review follow-up (85544511d)**: Codex review flagged a P1 on the F4 slice — the `!ready → fallback` shape (taken verbatim from the issue's recommendation) changed cancel/timeout semantics: a cancel during the 10s connect wait would have fallback-transcribed a recording whose file `cancelRecording()` already deleted, and a wait timeout skipped the realtime commit attempt. Fixed by restoring the original decision structure (pre-wait fallback check → wait → post-wait fallback check → state guard) with a pure `waitWhileConnecting(timeout:)` helper; the file's diff vs `main` is now a pure extraction.

## Test plan
- [x] Scoped SwiftLint over all 15 touched Swift files: 0 violations
- [x] Grep verification: `ImageCacheService` only in `Services/`; single request/decode path in `AccountService`; polling loop only in `waitWhileConnecting`; zero remaining calls to the old `adaptive*(colorScheme)` API
- [ ] **Xcode build + unit tests not run** (no Xcode toolchain in this environment, and `ios/` has no CI coverage) — please build and smoke-test locally before merge, especially light/dark rendering of the 10 migrated views

## Related

- Addresses findings F1–F4 of the rolling arch-review issue #365 (issue is auto-maintained weekly; next scan should mark them resolved)



## feat(claw-interface): add POST /internal/users/boost admin subscription boost route (#2788)

- **SHA**: `b54e6f29b63bffa13236c8b36145a585fa304d54`
- **作者**: bill-srp
- **日期**: 2026-07-09T03:42:40Z
- **PR**: #2788

**完整 commit message:**

```
feat(claw-interface): add POST /internal/users/boost admin subscription boost route (#2788)

# Purpose

Plan 2b-boost of the staff-admin relocation ([design
spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)):
add the admin-only `POST /internal/users/boost` endpoint (grant
subscription credits + extend access window; single uid or batch ≤ 50)
for the upcoming dashboard-console Users page. Follow-up to #2774 (Plan
1), #2781 (Plan 2a), #2783 (Plan 2b-grant).

# Approach

- **`POST /internal/users/boost`** — action sub-path on the existing
`/internal/users` sub-router (GET/POST-only convention; batch-capable,
so not under `/{uid}`). Double-gated: parent `/internal` router
`require_srp_account` + sub-router `require_admin_user`; handler also
injects the JWT-verified admin uid for audit.
- **Full service layer**: thin route delegates to a new **FastAPI-free**
`app/services/orders/admin_boost.py` — the boost saga extracted from the
legacy `POST /admin/users/boost-subscription` handler. The **legacy
route now delegates to the same service** (thin wrapper generating a
per-call random key, preserving its no-replay semantics until teardown)
— no duplicated saga (jscpd 3% gate).
- **Schemas** in `app/schema/internal/users.py`: shared
`BoostRequestBase` (uid⊕uids, credits, days, batch-limit + duplicate-uid
rejection); internal `BoostRequest` adds a **required, trimmed
`idempotency_key`** — same contract as the grant endpoint (#2783);
legacy `BoostRequest` adds only the deprecated-ignored `admin_uid`
field.
- **Retry safety (post-review hardening)**: `boost_ref` = the caller's
idempotency key; replay (drift guard → idempotent hit) is checked
**before** current-access resolution, so an already-boosted key replays
cleanly regardless of later subscription-state changes; a reused key
with different credits/days degrades to a `failed` result item.
- **Semantics preserved**: boost **degrades per-uid** (a failed uid
yields a `failed` result item, never aborts the batch); provider-trial
boundary is never moved; GRANTING→ACTIVE / GRANT_FAILED entitlement
recording unchanged. Per-uid failure reasons are now stable public
strings — raw upstream exception text stays in server logs and
`GRANT_FAILED` audit records only.

# Tests

- [x] 31 boost tests (`test_internal_users_boost.py`): saga branches
(happy / not-found / idempotent-hit / replay-skips-access-resolution /
idempotency-drift / reuse-GRANTING /
gateway-failure-degrades-with-sanitized-reason / batch-mixed /
balance-warning), `_subscription_balance_warning` branches, parametrized
pure helpers, schema validation (required+trimmed key, duplicate uids),
route delegation
- [x] 9 legacy-route tests (`test_admin_boost.py`, rewritten): legacy
schema boundaries + delegation with generated `BOOST-` key + JWT admin
(not the spoofable body field)
- [x] `app/services/orders/admin_boost.py` **100%** and
`app/routes/admin_boost.py` **100%** line coverage
- [x] Regression: `test_internal_users_grant.py` passes; broad `-k
"boost or grant or internal"` sweep (279 tests) passes
- [x] ruff check + format, pyright (0 errors), import-linter (8 kept, 0
broken), local jscpd run with CI config exits 0

# Notes

- Implementation plan + post-review amendments:
`docs/superpowers/plans/2026-07-09-internal-users-boost.md`
- The Plan-4 console boost UI must generate + reuse a stable
`idempotency_key` per operator action (same follow-up as the grant
modal).
- Console UI wiring (Plans 3–5) is a later slice.
```

**PR body:**

# Purpose

Plan 2b-boost of the staff-admin relocation ([design spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)): add the admin-only `POST /internal/users/boost` endpoint (grant subscription credits + extend access window; single uid or batch ≤ 50) for the upcoming dashboard-console Users page. Follow-up to #2774 (Plan 1), #2781 (Plan 2a), #2783 (Plan 2b-grant).

# Approach

- **`POST /internal/users/boost`** — action sub-path on the existing `/internal/users` sub-router (GET/POST-only convention; batch-capable, so not under `/{uid}`). Double-gated: parent `/internal` router `require_srp_account` + sub-router `require_admin_user`; handler also injects the JWT-verified admin uid for audit.
- **Full service layer**: thin route delegates to a new **FastAPI-free** `app/services/orders/admin_boost.py` — the boost saga extracted from the legacy `POST /admin/users/boost-subscription` handler. The **legacy route now delegates to the same service** (thin wrapper generating a per-call random key, preserving its no-replay semantics until teardown) — no duplicated saga (jscpd 3% gate).
- **Schemas** in `app/schema/internal/users.py`: shared `BoostRequestBase` (uid⊕uids, credits, days, batch-limit + duplicate-uid rejection); internal `BoostRequest` adds a **required, trimmed `idempotency_key`** — same contract as the grant endpoint (#2783); legacy `BoostRequest` adds only the deprecated-ignored `admin_uid` field.
- **Retry safety (post-review hardening)**: `boost_ref` = the caller's idempotency key; replay (drift guard → idempotent hit) is checked **before** current-access resolution, so an already-boosted key replays cleanly regardless of later subscription-state changes; a reused key with different credits/days degrades to a `failed` result item.
- **Semantics preserved**: boost **degrades per-uid** (a failed uid yields a `failed` result item, never aborts the batch); provider-trial boundary is never moved; GRANTING→ACTIVE / GRANT_FAILED entitlement recording unchanged. Per-uid failure reasons are now stable public strings — raw upstream exception text stays in server logs and `GRANT_FAILED` audit records only.

# Tests

- [x] 31 boost tests (`test_internal_users_boost.py`): saga branches (happy / not-found / idempotent-hit / replay-skips-access-resolution / idempotency-drift / reuse-GRANTING / gateway-failure-degrades-with-sanitized-reason / batch-mixed / balance-warning), `_subscription_balance_warning` branches, parametrized pure helpers, schema validation (required+trimmed key, duplicate uids), route delegation
- [x] 9 legacy-route tests (`test_admin_boost.py`, rewritten): legacy schema boundaries + delegation with generated `BOOST-` key + JWT admin (not the spoofable body field)
- [x] `app/services/orders/admin_boost.py` **100%** and `app/routes/admin_boost.py` **100%** line coverage
- [x] Regression: `test_internal_users_grant.py` passes; broad `-k "boost or grant or internal"` sweep (279 tests) passes
- [x] ruff check + format, pyright (0 errors), import-linter (8 kept, 0 broken), local jscpd run with CI config exits 0

# Notes

- Implementation plan + post-review amendments: `docs/superpowers/plans/2026-07-09-internal-users-boost.md`
- The Plan-4 console boost UI must generate + reuse a stable `idempotency_key` per operator action (same follow-up as the grant modal).
- Console UI wiring (Plans 3–5) is a later slice.



## refactor(ios): extract ChatView overlays into builders and drop stale lint suppression (#2790)

- **SHA**: `48c75fd3dabfc657226b155b3d9c397dd1c1d44f`
- **作者**: bill-srp
- **日期**: 2026-07-09T03:05:41Z
- **PR**: #2790

**完整 commit message:**

```
refactor(ios): extract ChatView overlays into builders and drop stale lint suppression (#2790)

## Summary
- Addresses arch-review finding **F8** in #2646 (iOS cohort,
2026-06-29): `ChatView.body` mixed banner/overlay/sheet logic inline and
carried a `swiftlint:disable:next type_body_length` suppression with a
TODO to split it up.
- Extracts the remaining inline blocks from `ChatView.body` into a
private `ChatView` extension, in original order: `copyTooltipLayer`
(long-press copy tooltip incl. `GeometryReader` positioning),
`scrollToBottomButton`, `floatingHeaderOverlay`, `floatingInputOverlay`,
`degradationToastOverlay`, and `withAgentSettingsSheet(_:)` for the
`AgentSettingsSheet` modifier. `body` is now a structural skeleton; each
block can be previewed independently.
- Moves `TooltipMetrics` / `CopyTooltipState` (pure positioning types)
into a new `ChatView+CopyTooltipState.swift`, following the existing
`ChatView+Banners.swift` pattern.
- Removes the now-stale `swiftlint:disable:next type_body_length`
suppression and its TODO comment — the type body is under the 350-line
threshold after extraction.
- No behavior change, no external interface change. (Refs #2646 — not
auto-closing; the weekly arch-review scan marks F8 resolved and closes
the cohort issue itself.)

## Test plan
- [x] `swiftlint lint --strict` on `ChatView.swift` +
`ChatView+CopyTooltipState.swift` — 0 violations (suppression removal
verified)
- [x] `xcodebuild build -project ZooClaw.xcodeproj -scheme ZooClaw -sdk
iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO` — BUILD
SUCCEEDED
- [ ] CI checks green
```

**PR body:**

## Summary
- Addresses arch-review finding **F8** in #2646 (iOS cohort, 2026-06-29): `ChatView.body` mixed banner/overlay/sheet logic inline and carried a `swiftlint:disable:next type_body_length` suppression with a TODO to split it up.
- Extracts the remaining inline blocks from `ChatView.body` into a private `ChatView` extension, in original order: `copyTooltipLayer` (long-press copy tooltip incl. `GeometryReader` positioning), `scrollToBottomButton`, `floatingHeaderOverlay`, `floatingInputOverlay`, `degradationToastOverlay`, and `withAgentSettingsSheet(_:)` for the `AgentSettingsSheet` modifier. `body` is now a structural skeleton; each block can be previewed independently.
- Moves `TooltipMetrics` / `CopyTooltipState` (pure positioning types) into a new `ChatView+CopyTooltipState.swift`, following the existing `ChatView+Banners.swift` pattern.
- Removes the now-stale `swiftlint:disable:next type_body_length` suppression and its TODO comment — the type body is under the 350-line threshold after extraction.
- No behavior change, no external interface change. (Refs #2646 — not auto-closing; the weekly arch-review scan marks F8 resolved and closes the cohort issue itself.)

## Test plan
- [x] `swiftlint lint --strict` on `ChatView.swift` + `ChatView+CopyTooltipState.swift` — 0 violations (suppression removal verified)
- [x] `xcodebuild build -project ZooClaw.xcodeproj -scheme ZooClaw -sdk iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO` — BUILD SUCCEEDED
- [ ] CI checks green



## feat(claw-interface): add POST /internal/users/{uid}/credits admin grant route (#2783)

- **SHA**: `a5a23718aac5de475bf94853f4ce198e247b7540`
- **作者**: bill-srp
- **日期**: 2026-07-09T02:35:38Z
- **PR**: #2783

**完整 commit message:**

```
feat(claw-interface): add POST /internal/users/{uid}/credits admin grant route (#2783)

## Linear
<!-- Internal staff-admin relocation; no dedicated Linear issue. -->

## Summary

Staff-admin relocation, **Plan 2b (grant)** — the first Users mutation
for the `dashboard-console`. Follows Plan 1 (#2774) and Plan 2a reads
(#2781).

- **`POST /internal/users/{uid}/credits`** — grant topup credits to a
user (admin only). Body: `credits_amount`, `reason?`,
`idempotency_key?`, `skip_subscription_check?`; `uid` from path, admin
from auth.

Thin route on the `@srp.one`-gated `/internal/users` sub-router (adds
`require_admin_user`) over a **new FastAPI-free service**
`app/services/orders/admin_grant.py`, **extracted** from the legacy
`POST /orders/admin/grant` saga: entitlement **idempotency**
(idempotent-hit returns the existing grant), double-grant prevention,
and per-grant **`GRANT_FAILED`** recording on billing-gateway failure.
The service raises `app.errors` domain errors (`NotFoundError`→404,
`DomainValidationError`→400); billing `ServiceError`s propagate.
`import-linter` confirms **C2/C3**.

**Deliberately NOT modified:** the legacy `/orders/admin/grant` route
(`app/routes/orders.py`) is left untouched — retired at the web/app
teardown phase. This avoids touching live billing code; the transient
duplication is the same accepted pattern as Plans 1 & 2a.

**Scope:** grant only. The credits-**balance read** (`GET
/{uid}/credits`) and **boost subscription** are follow-on slices.

## Test plan

- [x] 9 unit tests (`tests/unit/test_internal_users_grant.py`) covering
**every saga branch**: happy path, idempotent-hit, user-404,
no-active-subscription, `skip_subscription_check` bypass,
billing-gateway `ServiceError` → records `GRANT_FAILED` + re-raises,
non-`ServiceError` → records + re-raises, `_record_grant_failed`
swallow, reuse-existing-non-active entitlement.
- [x] `app/services/orders/admin_grant.py` at **100% coverage** (locally
measured) — the whole-app 89.5% gate bit Plan 2a, so branch coverage was
verified up front here.
- [x] `ruff check` + `ruff format --check` clean; `pyright` 0 errors
(app **and** tests); `import-linter` 8/8 (C2 + C3).
- [ ] CI: whole-app `pytest` + 89.5% coverage gate, `web-build-check`,
CodeQL (run on PR).
```

**PR body:**

## Linear
<!-- Internal staff-admin relocation; no dedicated Linear issue. -->

## Summary

Staff-admin relocation, **Plan 2b (grant)** — the first Users mutation for the `dashboard-console`. Follows Plan 1 (#2774) and Plan 2a reads (#2781).

- **`POST /internal/users/{uid}/credits`** — grant topup credits to a user (admin only). Body: `credits_amount`, `reason?`, `idempotency_key?`, `skip_subscription_check?`; `uid` from path, admin from auth.

Thin route on the `@srp.one`-gated `/internal/users` sub-router (adds `require_admin_user`) over a **new FastAPI-free service** `app/services/orders/admin_grant.py`, **extracted** from the legacy `POST /orders/admin/grant` saga: entitlement **idempotency** (idempotent-hit returns the existing grant), double-grant prevention, and per-grant **`GRANT_FAILED`** recording on billing-gateway failure. The service raises `app.errors` domain errors (`NotFoundError`→404, `DomainValidationError`→400); billing `ServiceError`s propagate. `import-linter` confirms **C2/C3**.

**Deliberately NOT modified:** the legacy `/orders/admin/grant` route (`app/routes/orders.py`) is left untouched — retired at the web/app teardown phase. This avoids touching live billing code; the transient duplication is the same accepted pattern as Plans 1 & 2a.

**Scope:** grant only. The credits-**balance read** (`GET /{uid}/credits`) and **boost subscription** are follow-on slices.

## Test plan

- [x] 9 unit tests (`tests/unit/test_internal_users_grant.py`) covering **every saga branch**: happy path, idempotent-hit, user-404, no-active-subscription, `skip_subscription_check` bypass, billing-gateway `ServiceError` → records `GRANT_FAILED` + re-raises, non-`ServiceError` → records + re-raises, `_record_grant_failed` swallow, reuse-existing-non-active entitlement.
- [x] `app/services/orders/admin_grant.py` at **100% coverage** (locally measured) — the whole-app 89.5% gate bit Plan 2a, so branch coverage was verified up front here.
- [x] `ruff check` + `ruff format --check` clean; `pyright` 0 errors (app **and** tests); `import-linter` 8/8 (C2 + C3).
- [ ] CI: whole-app `pytest` + 89.5% coverage gate, `web-build-check`, CodeQL (run on PR).



## refactor(web): split useSession into history, initialization, and reconnect hooks (F1 final) (#2787)

- **SHA**: `97e49f969cccaa5018c74ca24b41cf94768f147f`
- **作者**: bill-srp
- **日期**: 2026-07-09T02:30:40Z
- **PR**: #2787

**完整 commit message:**

```
refactor(web): split useSession into history, initialization, and reconnect hooks (F1 final) (#2787)

## Summary

**Final slice of the F1 split** from arch-review issue #2553 (follows
#2784 `useMessageQueue` and #2785 `useChatSSE`). This slice splits
`useSession.ts` (633 → 184 lines) into three co-located sub-hooks:

- `useSessionHistory.ts` (273) — session history loading, backend
message parsing, playback hydration, read-only ownership metadata, task
title state, refresh handling
- `useSessionInitialization.ts` (272) — URL/query-driven init, session
creation, login retry/subscription hooks, new-task reset, lifecycle
cleanup
- `useSessionReconnect.ts` (107) — in-progress task SSE recovery handoff
+ fallback polling (composed inside `useSessionHistory`, mirroring the
original control flow where recovery fires during history load)

Three seams instead of the arch-review's suggested two
(`useSessionInit`/`useSessionReconnect`): history parsing/load/refresh
turned out to be a concern independent of URL/login initialization, so
it got its own hook rather than being lumped into init.

`useSession` is now a thin composer that owns the shared public state
(passed into sub-hooks via explicit setters — avoids a circular
dependency between initialization needing `loadExistingSession` and
history needing init-state setters) plus the title-edit handlers.

Behavior-preserving: public API/return shape of `useSession` unchanged
(verified against the `index.tsx` consumer — same fields, same types;
`handleRefreshSession` was already render-unstable before, so the new
wrapper is identity-equivalent for its `onEmptyStreamComplete`
consumer). `useSendMessage.ts`, `useChatSSE.ts`, `useMessageQueue.ts`
untouched.

With this, **F1 is fully addressed**: `useSendMessage` 699 → 200,
`useSession` 633 → 184, and every extracted state machine now has an
isolated unit spec.

## Test plan

- [x] New unit specs (written red-first): `useSessionHistory` /
`useSessionInitialization` / `useSessionReconnect`
- [x] All 17 spec files exercising `agent-chat-client` pass (167 tests),
including the pre-existing `useSession.unit.spec.ts`
- [x] `bash scripts/verify-web.sh` on touched paths — guards + `tsc` +
vitest + `eslint` pass
- [ ] CI `code-quality / lint-and-test`
```

**PR body:**

## Summary

**Final slice of the F1 split** from arch-review issue #2553 (follows #2784 `useMessageQueue` and #2785 `useChatSSE`). This slice splits `useSession.ts` (633 → 184 lines) into three co-located sub-hooks:

- `useSessionHistory.ts` (273) — session history loading, backend message parsing, playback hydration, read-only ownership metadata, task title state, refresh handling
- `useSessionInitialization.ts` (272) — URL/query-driven init, session creation, login retry/subscription hooks, new-task reset, lifecycle cleanup
- `useSessionReconnect.ts` (107) — in-progress task SSE recovery handoff + fallback polling (composed inside `useSessionHistory`, mirroring the original control flow where recovery fires during history load)

Three seams instead of the arch-review's suggested two (`useSessionInit`/`useSessionReconnect`): history parsing/load/refresh turned out to be a concern independent of URL/login initialization, so it got its own hook rather than being lumped into init.

`useSession` is now a thin composer that owns the shared public state (passed into sub-hooks via explicit setters — avoids a circular dependency between initialization needing `loadExistingSession` and history needing init-state setters) plus the title-edit handlers.

Behavior-preserving: public API/return shape of `useSession` unchanged (verified against the `index.tsx` consumer — same fields, same types; `handleRefreshSession` was already render-unstable before, so the new wrapper is identity-equivalent for its `onEmptyStreamComplete` consumer). `useSendMessage.ts`, `useChatSSE.ts`, `useMessageQueue.ts` untouched.

With this, **F1 is fully addressed**: `useSendMessage` 699 → 200, `useSession` 633 → 184, and every extracted state machine now has an isolated unit spec.

## Test plan

- [x] New unit specs (written red-first): `useSessionHistory` / `useSessionInitialization` / `useSessionReconnect`
- [x] All 17 spec files exercising `agent-chat-client` pass (167 tests), including the pre-existing `useSession.unit.spec.ts`
- [x] `bash scripts/verify-web.sh` on touched paths — guards + `tsc` + vitest + `eslint` pass
- [ ] CI `code-quality / lint-and-test`

