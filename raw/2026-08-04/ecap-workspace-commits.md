# SerendipityOneInc/ecap-workspace commits — 2026-08-04

## dc0ff8a7 — feat(billing): settle first Creem card payment (#3237)

- sha: dc0ff8a727b8c0b602ab397fa2a51d190fba76e3
- 作者: tim-srp
- 日期: 2026-08-04T16:13:40Z
- PR: #3237

### Commit message

```
feat(billing): settle first Creem card payment (#3237)
```

### PR body

## Linear

No Linear issue was created for this stacked delivery slice.

## Summary

- bind signed `checkout.completed` identities to the exact pending local Card order without granting access
- verify the first `subscription.paid` transaction against the local order, Creem catalog, customer, subscription, amount, currency, and billing period before recording Billing v2 state
- grant subscription credits through the existing Billing Gateway idempotency key; publish the active agreement only after the entitlement is active, then attach the durable projection and release the checkout lease
- treat `subscription.active` as a non-authorizing projection and make paid-before-checkout delivery safely retryable
- prevent concurrent replay from moving an active entitlement back to granting; the default Stripe and Antom entitlement write path remains unchanged
- keep a paid-but-unsettled Creem order sticky so an expired one-hour checkout lease cannot expose a second checkout
- keep later same-order payment events retryable until the separate renewal phase is implemented

#3234 is merged. This branch is synchronized with the resulting `main` commit, and the PR diff remains 2,385 additions / 20 deletions across 17 files.

Explicitly out of scope: renewals, refunds, disputes, cancellation, upgrade/downgrade, UI changes, and Creem moderation.

## Test plan

- [x] a102 exact Git snapshot: Creem/Card/Billing v2 related regression — 311 passed
- [x] a102 exact Git snapshot: Stripe/Antom legacy regression — 432 passed
- [x] `ruff check`, `ruff format --check`, pyright, and 8 import contracts
- [x] latest `main` merge audit: stable PR4 patch-id, no frontend/Stripe/Antom diff, no unresolved conflicts
- [x] all custom Python CI guards: file length, complexity, dependency consistency, collection rules, repo sync, dead-code, and database return contracts
- [x] local pre-commit hooks, including Python static checks and file-size/complexity guards
- [x] concurrency RED→GREEN: active entitlement can no longer be downgraded to granting
- [x] webhook-order RED→GREEN: paid-before-checkout returns retryable 503 with no authorization, then succeeds after binding
- [x] partial-binding RED→GREEN: missing or non-completed provider status returns 409 with no side effects
- [x] fulfillment-order RED→GREEN: Billing Gateway failure cannot publish an active agreement
- [x] duplicate-checkout RED→GREEN: paid-but-unsettled orders remain unresolved after the lease expires
- [x] GitHub CI on the latest `main` merge ref — 35/35 checks settled with no failures



---

## d3c9deb7 — feat(billing): receive signed Creem webhooks (#3234)

- sha: d3c9deb7f677f6b5aa0c44360c8314a313b42826
- 作者: tim-srp
- 日期: 2026-08-04T15:45:42Z
- PR: #3234

### Commit message

```
feat(billing): receive signed Creem webhooks (#3234)
```

### PR body

## Linear

No separate Linear issue; this is the third small, stacked delivery unit for the Creem Card test-mode rollout.

## Summary

- add an exact raw-body Next.js BFF for the public Creem webhook path
- verify Creem HMAC signatures before parsing and enforce a bounded request body
- parse security-relevant known events into strict typed schemas
- publish a self-contained OpenAPI request schema without dangling document-root references
- claim provider events with fenced CAS semantics so duplicates, retries, stale workers, and digest collisions are handled deterministically
- return retryable errors for known lifecycle events, including `subscription.trialing` and `subscription.update`, that are intentionally not implemented in this receiver-only PR

This PR builds on the merged #3231 checkout layer. It intentionally does not bind checkouts, settle payments, grant credits, mutate subscriptions, recover historical refunds, or expose UI.

## Test plan

- [x] a102 exact-commit frontend static gate: TypeScript and targeted ESLint passed
- [x] a102 exact-commit frontend tests: 89 passed
- [x] a102 final-merge-tree backend tests: 179 passed
- [x] a102 exact-commit backend static gate: Ruff, format, Pyright (0 errors), and 8 import contracts passed
- [x] checkout response compatibility regression included in the backend suite
- [x] independent scope and security reviews completed before push



---

## 5d2054a1 — refactor(web): flatten (workspace) route group into (app) (#3236)

- sha: 5d2054a1fd6e90a4887b259b743683fb2e970e6e
- 作者: bill-srp
- 日期: 2026-08-04T12:26:18Z
- PR: #3236

### Commit message

```
refactor(web): flatten (workspace) route group into (app) (#3236)

## Summary
- Remove the `(app)/(workspace)` route group introduced in #3228 and
move its 5 route clusters (`schedule`, `mini-chat`, `agents-manager`,
`claw-settings`, `channels`) directly under `(app)`, alongside the other
non-Mattermost routes (`integrations`, `profile`, `skills`, …).
- The group carried no `layout.tsx` / template / boundary, so it had
zero runtime effect — URLs and the provider stack are unchanged. The
behavioral split (Mattermost provider scoped to chat routes) lives
entirely in `(app)/(chat)/layout.tsx`, which keeps working as before;
its doc comment is updated to describe the flattened siblings.
- Mechanical fallout: rewrote 14 regex-escaped `\(workspace\)` paths in
`eslint.config.mjs` shrink-only exemption lists (renames only — list
counts unchanged, guards stay green), updated
`@/app/[locale]/(app)/(workspace)/…` import specifiers in unit tests and
one hook comment, and shortened two relative imports in moved files
(`PublishAgentsClient.tsx`, `MiniChatClient.tsx`) that previously
climbed out of the group.
- Net diff: 127 files, +138/−150 lines; 120 of them are pure `git mv`
renames.

## Test plan
- [x] `bash scripts/verify-web.sh` — shrink-only guards, `tsc`, vitest
(593 files / 8084 tests), eslint all green
- [x] Repo-wide sweep confirms no literal `(workspace)` route-path
references remain (src, tests, configs, docs, scripts)
- [x] Vitest coverage excludes contain no `(workspace)` paths
(glob-based; moved files stay excluded)
```

### PR body

## Summary
- Remove the `(app)/(workspace)` route group introduced in #3228 and move its 5 route clusters (`schedule`, `mini-chat`, `agents-manager`, `claw-settings`, `channels`) directly under `(app)`, alongside the other non-Mattermost routes (`integrations`, `profile`, `skills`, …).
- The group carried no `layout.tsx` / template / boundary, so it had zero runtime effect — URLs and the provider stack are unchanged. The behavioral split (Mattermost provider scoped to chat routes) lives entirely in `(app)/(chat)/layout.tsx`, which keeps working as before; its doc comment is updated to describe the flattened siblings.
- Mechanical fallout: rewrote 14 regex-escaped `\(workspace\)` paths in `eslint.config.mjs` shrink-only exemption lists (renames only — list counts unchanged, guards stay green), updated `@/app/[locale]/(app)/(workspace)/…` import specifiers in unit tests and one hook comment, and shortened two relative imports in moved files (`PublishAgentsClient.tsx`, `MiniChatClient.tsx`) that previously climbed out of the group.
- Net diff: 127 files, +138/−150 lines; 120 of them are pure `git mv` renames.

## Test plan
- [x] `bash scripts/verify-web.sh` — shrink-only guards, `tsc`, vitest (593 files / 8084 tests), eslint all green
- [x] Repo-wide sweep confirms no literal `(workspace)` route-path references remain (src, tests, configs, docs, scripts)
- [x] Vitest coverage excludes contain no `(workspace)` paths (glob-based; moved files stay excluded)



---

## 6f18d4fd — fix(agents): resolve install computer in BFF instead of per-click bot probe (#3233)

- sha: 6f18d4fd45f449c65ab229544065a00016654bf7
- 作者: bill-srp
- 日期: 2026-08-04T11:55:45Z
- PR: #3233

### Commit message

```
fix(agents): resolve install computer in BFF instead of per-click bot probe (#3233)

# 🔧 Fix

## Summary

Installing an uploaded pack on **My Custom Specialists** demanded a
running bot even when the install would route to the engine runtime and
never touch the bot. The page's per-click gate (`useEnsureBotReady`) ran
a 3-request probe (`/computers`, `/computers/{id}`,
`/computers/{id}/status`) before every install/uninstall and threw "Bot
must be running before install or uninstall" unless the bot was fully
ready — a leftover from the pre-engine (v1 computer runtime) world.

This PR removes the client-side computer detection entirely and moves
computer resolution into the install BFF:

- **BFF** (`/api/agents/install`): when the request routes to the
computer runtime without a `computer_id`, the route now resolves the
user's computer server-side (one `GET /computers`, excluding
`pack_test`, requiring `status === 'ready'`). No ready computer → `409
agent.computer_not_ready` (fail-fast preserved). Engine-eligible
installs never touch the computer path at all. `agent_id` missing
remains a 400.
- **Frontend**: `useEnsureBotReady.ts` deleted. Install sends
`computerId: null` and lets the BFF decide; computer-runtime polling
uses the `computer_id` returned on the created workspace.
Computer-runtime uninstall/update take the `computer_id` already present
on the installed agent row (threaded through `PublishAgentCardItem` and
the toggle/update targets) with a missing-id guard.
- **UX**: the existing `botNotReady` toast is preserved by mapping the
BFF's `agent.computer_not_ready` ApiError code in `PublishAgentsClient`.

Net effect: engine-eligible users (and users with no bot) can install
custom specialists without a running bot; only genuine legacy
computer-runtime installs still require one, enforced server-side with a
single call. The marketplace hire flow (`useAgentActions`, untouched)
automatically gains the same server-side fallback when it has no cached
computer id.

## Root cause

`useAgentInstallToggle` called `ensureBotReady()` unconditionally before
`installAgentViaBff`, but the BFF's routing decision
(`install-decision.ts`) only needs a computer for the legacy
computer-runtime path — engine installs go to `POST /agents` with just
`pack_id`. The marketplace hire flow already treated the computer id as
optional for pack installs; the specialists page never got the same
update.

## Changes

- `web/app/src/app/api/agents/_lib/install-decision.ts` — new
`computer-resolve` route kind when `agent_id` is present but
`computer_id` is missing
- `web/app/src/app/api/agents/install/route.ts` — server-side
ready-computer resolution + `409 agent.computer_not_ready`
-
`web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useAgentInstallToggle.ts`
— bot probe removed; BFF-resolved install; uninstall uses target
`computerId`
-
`web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useAgentUpdateAction.ts`
— bot probe removed; update uses target `computerId`
-
`web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useEnsureBotReady.ts`
— deleted
-
`web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/PublishAgentsClient.tsx`
+ `components/types.ts` — thread `computerId` from installed rows; map
`agent.computer_not_ready` to the bot-not-ready toast
- Unit tests updated across the BFF decision/route and publish
hooks/page specs

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (593 files,
8073 passed) + eslint, all green
- [x] BFF specs: resolves `/computers` when `computer_id` omitted; `409
agent.computer_not_ready` when no ready computer; engine path unchanged
- [x] Hook specs: install without bot probe; computer-runtime
uninstall/update use row `computerId`; missing-id guards surface the
existing failure toasts
- [ ] Staging smoke after deploy: install an uploaded pack as an
engine-eligible user with no running bot
```

### PR body

# 🔧 Fix

## Summary

Installing an uploaded pack on **My Custom Specialists** demanded a running bot even when the install would route to the engine runtime and never touch the bot. The page's per-click gate (`useEnsureBotReady`) ran a 3-request probe (`/computers`, `/computers/{id}`, `/computers/{id}/status`) before every install/uninstall and threw "Bot must be running before install or uninstall" unless the bot was fully ready — a leftover from the pre-engine (v1 computer runtime) world.

This PR removes the client-side computer detection entirely and moves computer resolution into the install BFF:

- **BFF** (`/api/agents/install`): when the request routes to the computer runtime without a `computer_id`, the route now resolves the user's computer server-side (one `GET /computers`, excluding `pack_test`, requiring `status === 'ready'`). No ready computer → `409 agent.computer_not_ready` (fail-fast preserved). Engine-eligible installs never touch the computer path at all. `agent_id` missing remains a 400.
- **Frontend**: `useEnsureBotReady.ts` deleted. Install sends `computerId: null` and lets the BFF decide; computer-runtime polling uses the `computer_id` returned on the created workspace. Computer-runtime uninstall/update take the `computer_id` already present on the installed agent row (threaded through `PublishAgentCardItem` and the toggle/update targets) with a missing-id guard.
- **UX**: the existing `botNotReady` toast is preserved by mapping the BFF's `agent.computer_not_ready` ApiError code in `PublishAgentsClient`.

Net effect: engine-eligible users (and users with no bot) can install custom specialists without a running bot; only genuine legacy computer-runtime installs still require one, enforced server-side with a single call. The marketplace hire flow (`useAgentActions`, untouched) automatically gains the same server-side fallback when it has no cached computer id.

## Root cause

`useAgentInstallToggle` called `ensureBotReady()` unconditionally before `installAgentViaBff`, but the BFF's routing decision (`install-decision.ts`) only needs a computer for the legacy computer-runtime path — engine installs go to `POST /agents` with just `pack_id`. The marketplace hire flow already treated the computer id as optional for pack installs; the specialists page never got the same update.

## Changes

- `web/app/src/app/api/agents/_lib/install-decision.ts` — new `computer-resolve` route kind when `agent_id` is present but `computer_id` is missing
- `web/app/src/app/api/agents/install/route.ts` — server-side ready-computer resolution + `409 agent.computer_not_ready`
- `web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useAgentInstallToggle.ts` — bot probe removed; BFF-resolved install; uninstall uses target `computerId`
- `web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useAgentUpdateAction.ts` — bot probe removed; update uses target `computerId`
- `web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useEnsureBotReady.ts` — deleted
- `web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/PublishAgentsClient.tsx` + `components/types.ts` — thread `computerId` from installed rows; map `agent.computer_not_ready` to the bot-not-ready toast
- Unit tests updated across the BFF decision/route and publish hooks/page specs

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (593 files, 8073 passed) + eslint, all green
- [x] BFF specs: resolves `/computers` when `computer_id` omitted; `409 agent.computer_not_ready` when no ready computer; engine path unchanged
- [x] Hook specs: install without bot probe; computer-runtime uninstall/update use row `computerId`; missing-id guards surface the existing failure toasts
- [ ] Staging smoke after deploy: install an uploaded pack as an engine-eligible user with no running bot



---

## 6744e4cb — feat(billing): add idempotent Creem Card checkout (#3231)

- sha: 6744e4cb807e1271f1a3d5fcae78f4ebcbaecb91
- 作者: tim-srp
- 日期: 2026-08-04T11:28:56Z
- PR: #3231

### Commit message

```
feat(billing): add idempotent Creem Card checkout (#3231)
```

### PR body

## Parent PR

- #3229 — Creem Card foundation

## Summary

- Add one authenticated, provider-neutral `POST /billing/card-checkouts` endpoint for new Creem Test Mode subscriptions.
- Resolve plan, billing cycle, Product ID, amount, currency, customer identity, and success URL on the server.
- Persist deterministic insert-only Billing v2 orders with a UID checkout lease and a one-winner Provider Create CAS.
- Reuse an existing verified Checkout for the same intent; fail closed on changed intent, ambiguous Provider outcomes, and non-pending Create responses.

This stacked PR contains backend Checkout creation only. It does not add webhook processing, subscription activation, refunds, disputes, frontend entry, Trial, Top-up, plan changes, provider selection, fallback, or production enablement.

## Test plan

- [x] a102 devcontainer Checkout/Foundation targeted suite: 360 passed.
- [x] a102 devcontainer Stripe, Antom, and Apple regression suite: 86 passed.
- [x] Review-driven TDD: 3 non-pending Provider responses failed before the one-line status guard and passed afterward.
- [x] CAS loser, UID lease conflict/order, and attachment owner-fence regression tests passed.
- [x] Ruff check and Ruff format passed.
- [x] Pyright (0 errors) and import-linter (8/8 contracts) passed on the final candidate.
- [x] Real Creem Test Mode catalog contract: 6/6 products passed.
- [x] Staging Mongo Billing v2 index contract: passed (read-only).
- [x] Real Creem Test Mode Create Checkout on final SHA `a0cc93fa7`: one exact local order attached; same/new operation reuse made zero additional Provider calls; changed intent failed closed.
- [x] `git diff --check` passed.
- [x] Stacked PR net size: 1,633 changed lines, below the 3,000-line limit.
- [x] Independent scope and quality reviews passed.

## Rollout safety

- Production rejects the operation before database or Provider I/O, even if Creem settings are present.
- No frontend calls this endpoint until the later UI PR.
- Existing Stripe, Antom, and Apple code paths are unchanged and have dedicated regression coverage.
- Ambiguous network or Provider responses are never retried automatically.



---

## e91b6e1d — feat(web): route landing specialist auto-hire through the v2 install BFF (#3232)

- sha: e91b6e1d3c2cb52c30780e8a55df1f10c41e299c
- 作者: bill-srp
- 日期: 2026-08-04T11:22:27Z
- PR: #3232

### Commit message

```
feat(web): route landing specialist auto-hire through the v2 install BFF (#3232)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven:
docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md -->

## Summary
Phase 3 (final) of the v2 onboarding spec (Phase 1 = #3221, Phase 2 =
#3227): the landing `?sp=` specialist auto-hire goes through the
runtime-routing install BFF instead of force-installing v1.

- `useLandingContextFlow.hireSpecialist` → `installAgentViaBff`
(specialist ids are pack ids): engine result → `completeEngineInstall`;
computer result → existing `waitForAgentWorkspaceStatus` + cache
refresh, unchanged.
- The `!computerId` wait gate is now capability-aware
(`getAgentInstallCapability`, fetched once per flow and cached): engine
runtime → hire immediately with no computer (post-#3227 engine-mode
users never get one — the old wait would hang forever); computer runtime
or capability outage → today's wait/refresh behavior, fail-safe.
- BFF 409 `agent.already_installed` → hand off to the specialist as
already-hired instead of the Main-Agent fallback. All other install
failures keep the existing Sentry capture + Main-Agent fallback.
- `useAgentActions` needed no change — pack hires already pass a
nullable computer id through the BFF correctly.

**Scope decision (recorded in the spec): the BossClaw wizard stays v1,
untouched** — `bossclaw` is a v1 official agent id with no active pack
in the engine registry; its future cutover needs a published pack + the
per-workspace engine WeChat setup (already exists end-to-end).

## Test plan
- [x] TDD (RED confirmed first, 5 new cases): engine-capability hire
with no computer → BFF + `completeEngineInstall` + hand-off; computer
path unchanged; 409 → hand-off as hired; engine install failure →
Main-Agent fallback; capability fetch failure → waits for computer
(`useLandingContextFlow.unit.spec.ts`, 37/37)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc +
vitest + eslint — green
- [x] `pnpm lint:imports`: 0 errors
- [ ] CI (`web-quality` + `web-build-check`)
```

### PR body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven: docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md -->

## Summary
Phase 3 (final) of the v2 onboarding spec (Phase 1 = #3221, Phase 2 = #3227): the landing `?sp=` specialist auto-hire goes through the runtime-routing install BFF instead of force-installing v1.

- `useLandingContextFlow.hireSpecialist` → `installAgentViaBff` (specialist ids are pack ids): engine result → `completeEngineInstall`; computer result → existing `waitForAgentWorkspaceStatus` + cache refresh, unchanged.
- The `!computerId` wait gate is now capability-aware (`getAgentInstallCapability`, fetched once per flow and cached): engine runtime → hire immediately with no computer (post-#3227 engine-mode users never get one — the old wait would hang forever); computer runtime or capability outage → today's wait/refresh behavior, fail-safe.
- BFF 409 `agent.already_installed` → hand off to the specialist as already-hired instead of the Main-Agent fallback. All other install failures keep the existing Sentry capture + Main-Agent fallback.
- `useAgentActions` needed no change — pack hires already pass a nullable computer id through the BFF correctly.

**Scope decision (recorded in the spec): the BossClaw wizard stays v1, untouched** — `bossclaw` is a v1 official agent id with no active pack in the engine registry; its future cutover needs a published pack + the per-workspace engine WeChat setup (already exists end-to-end).

## Test plan
- [x] TDD (RED confirmed first, 5 new cases): engine-capability hire with no computer → BFF + `completeEngineInstall` + hand-off; computer path unchanged; 409 → hand-off as hired; engine install failure → Main-Agent fallback; capability fetch failure → waits for computer (`useLandingContextFlow.unit.spec.ts`, 37/37)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc + vitest + eslint — green
- [x] `pnpm lint:imports`: 0 errors
- [ ] CI (`web-quality` + `web-build-check`)



---

## 140138d9 — feat(whatsapp): grant 500-credit starter trial to new WhatsApp-bound users (#3218)

- sha: 140138d97ef299cf6c0c175546e27d6dfa43b605
- 作者: bill-srp
- 日期: 2026-08-04T11:09:18Z
- PR: #3218

### Commit message

```
feat(whatsapp): grant 500-credit starter trial to new WhatsApp-bound users (#3218)

## Summary
- Users receive a **7-day starter trial with 500 credits** on their
**first genuine WhatsApp bind**. The grant fires in `POST
/whatsapp/users/bind` — a route authenticated with the connector service
token that only the WhatsApp bridge holds, and which the bridge only
calls while processing a real inbound WhatsApp message. Caller-supplied
registration metadata can no longer mint credits (addresses the review's
forgery finding).
- `whatsapp_repo.bind_user` now returns `(binding, freshly_bound)`: the
flag is true only for the atomic `pending_binding → bound` transition,
so Meta webhook replays and idempotent re-binds never re-evaluate the
grant. The entitlement operation key `trial:whatsapp_bind:{uid}` and the
deterministic billing-gateway transaction id remain the second lock.
- Eligibility (owner-confirmed, identical to the long-standing
invite-trial recipient set): no prior trial of any kind, current billing
status `free` or `expired`, zero subscription wallet balance. `expired`
deliberately includes lapsed ex-paying users — the grant doubles as a
win-back incentive. At most once per user for life (the unique bound-uid
index means a user can only ever complete one WhatsApp bind, and the
trial operation key is per-uid).
- Reuses the invite-trial machinery: `grant_trial_credits_if_eligible`
gained keyword-only `trial_key` / `credits` / `duration_days` /
`actor_id` (defaults preserve the legacy invite flow byte-for-byte). New
constants `WHATSAPP_BIND_TRIAL_CREDITS = 500`,
`WHATSAPP_BIND_TRIAL_DURATION_DAYS = 7` (either ≤ 0 disables).
- Grant is best-effort and fail-closed: a billing-gateway failure logs
with context, never fails the bind response (no Meta webhook retry
storms), and deliberately leaves the recorded trial row consuming the
one-trial slot — repair is the manual admin grant flow (comment at call
site + contract tests).

## Review history
- Cross-flow double-grant race with the invite trial: resolved by
product fact — the invite-bind route has no callers (dead surface);
whatsapp_bind is the sole live onboarding-trial writer. If invite
binding is ever revived, re-establish a uid-level unique invariant first
(reference implementation in 9b72b868f, deliberately reverted in
79fbc79fa).
- Forgeable registration metadata (grant under user bearer token): fixed
in c773ff7cb by moving the grant behind the bridge-authenticated bind
step as described above.

## Test plan
- [x] TDD: repo contract tests for `(binding, freshly_bound)` (fresh
transition / idempotent replay / failure); service tests: fresh bind
grants with exact whatsapp kwargs, idempotent re-bind never grants,
grant failure leaves the bind response unchanged; trial-service tests
for generalized params, invite defaults, disable switches, fail-closed
(no entitlement mutation on billing-gateway failure)
- [x] `pytest` on touched files — 139 passed
- [x] `bash scripts/verify-py.sh` — ruff, ruff format, pyright,
import-linter green
- [x] Pre-commit + pre-push hook gates passed

## Deployment
Backend-only (`services/claw-interface`); no bridge or web changes.
Requires Billing Gateway reachable (same dependency as the invite
trial).
```

### PR body

## Summary
- Users receive a **7-day starter trial with 500 credits** on their **first genuine WhatsApp bind**. The grant fires in `POST /whatsapp/users/bind` — a route authenticated with the connector service token that only the WhatsApp bridge holds, and which the bridge only calls while processing a real inbound WhatsApp message. Caller-supplied registration metadata can no longer mint credits (addresses the review's forgery finding).
- `whatsapp_repo.bind_user` now returns `(binding, freshly_bound)`: the flag is true only for the atomic `pending_binding → bound` transition, so Meta webhook replays and idempotent re-binds never re-evaluate the grant. The entitlement operation key `trial:whatsapp_bind:{uid}` and the deterministic billing-gateway transaction id remain the second lock.
- Eligibility (owner-confirmed, identical to the long-standing invite-trial recipient set): no prior trial of any kind, current billing status `free` or `expired`, zero subscription wallet balance. `expired` deliberately includes lapsed ex-paying users — the grant doubles as a win-back incentive. At most once per user for life (the unique bound-uid index means a user can only ever complete one WhatsApp bind, and the trial operation key is per-uid).
- Reuses the invite-trial machinery: `grant_trial_credits_if_eligible` gained keyword-only `trial_key` / `credits` / `duration_days` / `actor_id` (defaults preserve the legacy invite flow byte-for-byte). New constants `WHATSAPP_BIND_TRIAL_CREDITS = 500`, `WHATSAPP_BIND_TRIAL_DURATION_DAYS = 7` (either ≤ 0 disables).
- Grant is best-effort and fail-closed: a billing-gateway failure logs with context, never fails the bind response (no Meta webhook retry storms), and deliberately leaves the recorded trial row consuming the one-trial slot — repair is the manual admin grant flow (comment at call site + contract tests).

## Review history
- Cross-flow double-grant race with the invite trial: resolved by product fact — the invite-bind route has no callers (dead surface); whatsapp_bind is the sole live onboarding-trial writer. If invite binding is ever revived, re-establish a uid-level unique invariant first (reference implementation in 9b72b868f, deliberately reverted in 79fbc79fa).
- Forgeable registration metadata (grant under user bearer token): fixed in c773ff7cb by moving the grant behind the bridge-authenticated bind step as described above.

## Test plan
- [x] TDD: repo contract tests for `(binding, freshly_bound)` (fresh transition / idempotent replay / failure); service tests: fresh bind grants with exact whatsapp kwargs, idempotent re-bind never grants, grant failure leaves the bind response unchanged; trial-service tests for generalized params, invite defaults, disable switches, fail-closed (no entitlement mutation on billing-gateway failure)
- [x] `pytest` on touched files — 139 passed
- [x] `bash scripts/verify-py.sh` — ruff, ruff format, pyright, import-linter green
- [x] Pre-commit + pre-push hook gates passed

## Deployment
Backend-only (`services/claw-interface`); no bridge or web changes. Requires Billing Gateway reachable (same dependency as the invite trial).



---

## dfe95558 — refactor(web): split non-Mattermost routes into (workspace) group (#3228)

- sha: dfe95558668deffa8689f95c50ce484b4ec014de
- 作者: bill-srp
- 日期: 2026-08-04T10:58:06Z
- PR: #3228

### Commit message

```
refactor(web): split non-Mattermost routes into (workspace) group (#3228)

## Summary
- Move the five routes that never consume the Mattermost context out of
the `(chat)` route group into a new `(workspace)` group: `schedule`,
`claw-settings`, `channels`, `agents-manager`, `mini-chat`. URLs are
unchanged (route groups don't affect paths).
- The new `(workspace)/layout.tsx` keeps the
`VerticalPackPackageInstaller` side effect (identical behavior to
before) but does **not** mount the WebSocket-heavy `MattermostProvider`
— so visiting these pages no longer opens/holds a Mattermost WebSocket,
syncs channel history, or pulls the MM client into their render path.
- `(chat)` retains only the routes that actually consume Mattermost:
`chat`, `agent-builder`, `council` (via `useCouncilViewModel`), `assets`
(via `UploadsFeed`).
- Safety audit done before the move: none of the five routes reach
`MattermostContext` directly or transitively; shared components they
render (`ClawConnectionStatus`, `FeedbackDialog`) use the null-safe
`useMattermostOptional`; `mini-chat` talks over the OpenClaw websocket.
No remaining `(chat)` route imports from the moved five.
- Mechanical follow-through: two cross-group relative imports updated
(`MiniChatClient` → chat components, `PublishAgentsClient` →
agent-builder fork dialog), 46 test files' import paths, 14
regex-escaped shrink-only exemption paths in `eslint.config.mjs`, stale
path comments (`useCronJobs.ts`, `(chat)/layout.tsx` docstring).

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, `tsc --noEmit`, vitest (592
files / 8046 tests), eslint all green
- [x] Leftover sweep: zero references to the old
`(chat)/{schedule,claw-settings,channels,agents-manager,mini-chat}`
paths in `src/`, `tests/`, and config files (including the escaped-regex
forms in `eslint.config.mjs`)
- [x] Diff review: non-move changes are symmetric path rewrites (134
insertions / 134 deletions across 48 files); 79 files detected as pure
renames

## Follow-up: installer hoisted to `(app)` layout (deliberate behavior
change)
- Per Bill's request, `VerticalPackPackageInstaller` moved from the
group layouts to `(app)/layout.tsx`: vertical-pack package installs now
start from **any** authenticated app page once OpenClaw init is ready,
instead of waiting for a chat/workspace visit. This intentionally
supersedes the "identical installer behavior" note above.
- Safety: the hook stays gated on `initStatus === 'ready'` (inert on
pages that never activate OpenClaw), the install flow is idempotent
(fetches current package, installs only missing agents, module-global
`uid:computer:package` start guard), and `new-chat`'s data-consuming
hook call is double-mount safe for the same reason.
- `(chat)/layout.tsx` is now a pure `MattermostProvider` wrapper; the
installer-only `(workspace)/layout.tsx` was deleted (group is purely
organizational). `tests/unit/app/app-group-layout.unit.spec.tsx` pins
the app-wide installer mount.
```

### PR body

## Summary
- Move the five routes that never consume the Mattermost context out of the `(chat)` route group into a new `(workspace)` group: `schedule`, `claw-settings`, `channels`, `agents-manager`, `mini-chat`. URLs are unchanged (route groups don't affect paths).
- The new `(workspace)/layout.tsx` keeps the `VerticalPackPackageInstaller` side effect (identical behavior to before) but does **not** mount the WebSocket-heavy `MattermostProvider` — so visiting these pages no longer opens/holds a Mattermost WebSocket, syncs channel history, or pulls the MM client into their render path.
- `(chat)` retains only the routes that actually consume Mattermost: `chat`, `agent-builder`, `council` (via `useCouncilViewModel`), `assets` (via `UploadsFeed`).
- Safety audit done before the move: none of the five routes reach `MattermostContext` directly or transitively; shared components they render (`ClawConnectionStatus`, `FeedbackDialog`) use the null-safe `useMattermostOptional`; `mini-chat` talks over the OpenClaw websocket. No remaining `(chat)` route imports from the moved five.
- Mechanical follow-through: two cross-group relative imports updated (`MiniChatClient` → chat components, `PublishAgentsClient` → agent-builder fork dialog), 46 test files' import paths, 14 regex-escaped shrink-only exemption paths in `eslint.config.mjs`, stale path comments (`useCronJobs.ts`, `(chat)/layout.tsx` docstring).

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, `tsc --noEmit`, vitest (592 files / 8046 tests), eslint all green
- [x] Leftover sweep: zero references to the old `(chat)/{schedule,claw-settings,channels,agents-manager,mini-chat}` paths in `src/`, `tests/`, and config files (including the escaped-regex forms in `eslint.config.mjs`)
- [x] Diff review: non-move changes are symmetric path rewrites (134 insertions / 134 deletions across 48 files); 79 files detected as pure renames

## Follow-up: installer hoisted to `(app)` layout (deliberate behavior change)
- Per Bill's request, `VerticalPackPackageInstaller` moved from the group layouts to `(app)/layout.tsx`: vertical-pack package installs now start from **any** authenticated app page once OpenClaw init is ready, instead of waiting for a chat/workspace visit. This intentionally supersedes the "identical installer behavior" note above.
- Safety: the hook stays gated on `initStatus === 'ready'` (inert on pages that never activate OpenClaw), the install flow is idempotent (fetches current package, installs only missing agents, module-global `uid:computer:package` start guard), and `new-chat`'s data-consuming hook call is double-mount safe for the same reason.
- `(chat)/layout.tsx` is now a pure `MattermostProvider` wrapper; the installer-only `(workspace)/layout.tsx` was deleted (group is purely organizational). `tests/unit/app/app-group-layout.unit.spec.tsx` pins the app-wide installer mount.



---

## 96ba4a52 — feat(billing): add Creem Card foundation (#3229)

- sha: 96ba4a52e5658c53e1589453fbf45510f212e996
- 作者: tim-srp
- 日期: 2026-08-04T10:36:35Z
- PR: #3229

### Commit message

```
feat(billing): add Creem Card foundation (#3229)
```

### PR body

## Linear

No linked Linear issue.

## Summary

- Add a default-off Creem Test Mode configuration boundary and strict provider-neutral Card schemas.
- Add a fixed-host `aiohttp` Creem client, a six-product server-authoritative catalog, and a secret-free catalog preflight.
- Add an authenticated read-only Card capability and a read-only validator for the seven existing Billing v2 indexes.
- Project internal `creem` values to public `card` responses while leaving Stripe, Antom, and Apple values unchanged.

This is a dark foundation PR. It does not add a Card checkout POST route, webhook handling, subscription lifecycle, frontend entry, provider registry, fallback, Trial, Top-up, Portal, or plan-change behavior.

## Test plan

- [x] a102 devcontainer targeted Creem, public projection (including Team credits), Settings, Stripe, Antom, and Apple regression suite: 390 passed.
- [x] a102 devcontainer `scripts/verify-py.sh`: Ruff, format, Pyright, and import-linter passed.
- [x] Real Creem Test Mode catalog preflight: all six monthly/yearly products passed.
- [x] Product endpoint TDD: old path failed the contract test; official query-parameter contract passed after the minimal fix.
- [x] `git diff --check` passed.
- [x] PR size gate: 2,469 changed lines, below the 3,000-line limit.
- [x] Independent scope/spec review passed.

## Rollout safety

- Production capability remains false even if the feature flag is accidentally enabled.
- This PR contains no payment mutation endpoint and cannot create Creem orders or checkouts.
- Secrets are held as secret values and are excluded from API responses and diagnostic output.



---

## 1e59b570 — feat(web): stop creating computers for new users when AGENTS_V2 is enabled (#3227)

- sha: 1e59b570b385151dbd3576b4fcdc9a95d674480c
- 作者: bill-srp
- 日期: 2026-08-04T09:10:20Z
- PR: #3227

### Commit message

```
feat(web): stop creating computers for new users when AGENTS_V2 is enabled (#3227)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven:
docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md
(merged in #3221) -->

## Summary
Phase 2 of the v2 onboarding spec (Phase 1 = #3221): **new users stop
getting a v1 computer when AGENTS_V2 is enabled**. Decision recorded in
the spec: the gate is the env-level enable flag (derived from `GET
/agents/install-capability` — enabled iff `reason !==
'agents_v2_disabled'`), not per-user allowlist eligibility.

- `services/agent-install.ts`: `getAgentInstallCapability()` passthrough
via the claw catch-all (no new BFF route).
- `services/computers.ts`: `findUserComputer()` split out of
`ensureUserComputer()` so lookup and creation can be gated independently
(`ensureUserComputer` contract unchanged for its other callers).
- `lib/auth/manager.ts` (`_completeBusinessDataSync`, the single
creation site): existing computer → today's behavior byte-for-byte. No
computer → capability decides: AGENTS_V2 on → dispatch new `'engine'`
bootstrap status, **no `POST /computers`**; off → create as today.
Capability fetch failure → fail-safe to creating, so an outage never
strands a v1 signup.
- `lib/onboarding/resolve-status.ts`: `botStatus === 'engine'` resolves
as active-user (`not-required`), same as `'ready'`.
- `contexts/OpenClawContext.tsx`: `useOpenClaw()` skips v1 init
activation in engine mode (uid-matched onboarding store +
`getUserInfo()` — lib-only imports, W3-clean), so `/chat` never renders
the guaranteed `computer not ready` init error for computer-less users.

Existing users with computers are untouched in every path; nothing
deletes or stops a pod. Rollout precondition (documented in the spec):
flipping the env in an environment requires all new users there to be
engine-eligible, else they'd get neither a computer nor engine installs.

## Test plan
- [x] TDD (RED confirmed first): engine-mode new user → no `POST
/computers`, `'engine'` status dispatched, onboarding `not-required`, no
v1 init activation; v1 new user unchanged; capability outage → creates;
existing-computer user unchanged (`manager.unit.spec.ts` ~15 assertions
updated, new `computers.unit.spec.ts`, `resolveOnboardingStatus` /
`OpenClawContext` / `agent-install` specs)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc +
vitest + eslint — green
- [x] `pnpm lint:imports`: 0 errors (a W3 contexts→hooks violation was
caught locally and fixed to lib-only imports)
- [ ] CI (`web-quality` + `web-build-check`)
```

### PR body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven: docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md (merged in #3221) -->

## Summary
Phase 2 of the v2 onboarding spec (Phase 1 = #3221): **new users stop getting a v1 computer when AGENTS_V2 is enabled**. Decision recorded in the spec: the gate is the env-level enable flag (derived from `GET /agents/install-capability` — enabled iff `reason !== 'agents_v2_disabled'`), not per-user allowlist eligibility.

- `services/agent-install.ts`: `getAgentInstallCapability()` passthrough via the claw catch-all (no new BFF route).
- `services/computers.ts`: `findUserComputer()` split out of `ensureUserComputer()` so lookup and creation can be gated independently (`ensureUserComputer` contract unchanged for its other callers).
- `lib/auth/manager.ts` (`_completeBusinessDataSync`, the single creation site): existing computer → today's behavior byte-for-byte. No computer → capability decides: AGENTS_V2 on → dispatch new `'engine'` bootstrap status, **no `POST /computers`**; off → create as today. Capability fetch failure → fail-safe to creating, so an outage never strands a v1 signup.
- `lib/onboarding/resolve-status.ts`: `botStatus === 'engine'` resolves as active-user (`not-required`), same as `'ready'`.
- `contexts/OpenClawContext.tsx`: `useOpenClaw()` skips v1 init activation in engine mode (uid-matched onboarding store + `getUserInfo()` — lib-only imports, W3-clean), so `/chat` never renders the guaranteed `computer not ready` init error for computer-less users.

Existing users with computers are untouched in every path; nothing deletes or stops a pod. Rollout precondition (documented in the spec): flipping the env in an environment requires all new users there to be engine-eligible, else they'd get neither a computer nor engine installs.

## Test plan
- [x] TDD (RED confirmed first): engine-mode new user → no `POST /computers`, `'engine'` status dispatched, onboarding `not-required`, no v1 init activation; v1 new user unchanged; capability outage → creates; existing-computer user unchanged (`manager.unit.spec.ts` ~15 assertions updated, new `computers.unit.spec.ts`, `resolveOnboardingStatus` / `OpenClawContext` / `agent-install` specs)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc + vitest + eslint — green
- [x] `pnpm lint:imports`: 0 errors (a W3 contexts→hooks violation was caught locally and fixed to lib-only imports)
- [ ] CI (`web-quality` + `web-build-check`)



---

## e719380c — feat(web): enable engine agent chat without a v1 computer (#3221)

- sha: e719380c8aed0d31a426ed5d08b3b371ac3dd2f1
- 作者: bill-srp
- 日期: 2026-08-04T08:25:13Z
- PR: #3221

### Commit message

```
feat(web): enable engine agent chat without a v1 computer (#3221)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- none — spec-driven work, see design spec in this PR -->

## Summary
Phase 1 of
`docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md`
(included in this PR): make engine-agent chat work for a user with **no
v1 computer**. This was explicitly scoped out of the P2-6 engine-chat
plan ("dogfood users all have one") — this is the planned revisit,
prerequisite for new users skipping computer creation entirely (Phase
2).

Changes (all five sites from the spec):
- `MattermostProvider`: agents query enabled on `uid` alone (was gated
on the v1 computer id); auto-connect no longer requires `oc.initStatus
=== 'ready'`; bot selection still prefers the `computer` runtime bot but
falls back to any bot with a DM channel (engine);
`refreshMattermostBots` works without a computer id.
- `GenClawClient.useRouteAwareChatAgents`: drop the `!currentComputerId
→ []` short-circuit so active engine rows survive on the chat page (same
shape as `useChatEligibleAgents`).

v1 behavior is preserved: computer rows still can't match until the
computer id resolves, so v1 auto-connect effectively still waits for
init, and the computer bot keeps priority when both exist.

## Test plan
- [x] TDD: 4 new unit cases written first (RED confirmed), covering
engine-only registration + auto-connect fallback, computer-bot
preference, refresh without computer, and engine rows on the chat page
(`MattermostContext.unit.spec.tsx`,
`GenClawClient.internals.unit.spec.tsx`)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc +
vitest (8,046 passed) + eslint — all green
- [ ] CI (`web-quality` + `web-build-check`)
```

### PR body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- none — spec-driven work, see design spec in this PR -->

## Summary
Phase 1 of `docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md` (included in this PR): make engine-agent chat work for a user with **no v1 computer**. This was explicitly scoped out of the P2-6 engine-chat plan ("dogfood users all have one") — this is the planned revisit, prerequisite for new users skipping computer creation entirely (Phase 2).

Changes (all five sites from the spec):
- `MattermostProvider`: agents query enabled on `uid` alone (was gated on the v1 computer id); auto-connect no longer requires `oc.initStatus === 'ready'`; bot selection still prefers the `computer` runtime bot but falls back to any bot with a DM channel (engine); `refreshMattermostBots` works without a computer id.
- `GenClawClient.useRouteAwareChatAgents`: drop the `!currentComputerId → []` short-circuit so active engine rows survive on the chat page (same shape as `useChatEligibleAgents`).

v1 behavior is preserved: computer rows still can't match until the computer id resolves, so v1 auto-connect effectively still waits for init, and the computer bot keeps priority when both exist.

## Test plan
- [x] TDD: 4 new unit cases written first (RED confirmed), covering engine-only registration + auto-connect fallback, computer-bot preference, refresh without computer, and engine rows on the chat page (`MattermostContext.unit.spec.tsx`, `GenClawClient.internals.unit.spec.tsx`)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc + vitest (8,046 passed) + eslint — all green
- [ ] CI (`web-quality` + `web-build-check`)



---

## f0fe91a8 — feat(council): composer depth/tier tips and file attachments (#3222)

- sha: f0fe91a810c4aaf78c0c138a3bb2a717f6258a6a
- 作者: bill-srp
- 日期: 2026-08-04T08:25:07Z
- PR: #3222

### Commit message

```
feat(council): composer depth/tier tips and file attachments (#3222)

## Linear
<!-- no Linear issue for this change -->

## Summary
- Add explanatory tips under the Council composer's Depth and Tier rows.
Depth tips give the council size per depth (quick/standard/deep = 3/4/5
members, Auto = the skill classifies the topic); tier tips name each
tier's representative models with a "Latest" suffix to signal the skill
resolves each series to the newest version on the pod (e.g. "Mid-class
models · Claude Sonnet Latest, GPT Terra Latest, Gemini Flash Latest… ·
the balanced default."). Copy is grounded in `ecap-skills/council`
(`SKILL.md` + `roster.py` tier lineups / `SEATS_BY_DEPTH`).
- Add file attachments to the Council/Deep-Research composer: paperclip
button + pending-attachment chips (name · size · remove) with the
Mattermost per-post file cap enforced. On dispatch, files upload to the
run thread's channel via the existing `uploadMattermostAttachment`
helper (HEIC normalization + image-downscale retries), and the topic
post carries their `file_ids` — `postThreadReply` gains an optional
`fileIds` pass-through to `sendPost`. Protocol messages (`go` / `cancel`
/ tier tokens) never attach files. Upload failure aborts the dispatch
post and keeps the files for retry; success clears them.
- Map the `--chat-ui-*` CSS variables to app semantic tokens on the
chips container so `AttachmentChip` follows the app theme (its built-in
fallbacks are light-mode colors, which rendered unreadable chips in dark
mode).
- Design note: a per-model selection picker was explored and specced
during review but deliberately dropped in favor of the simpler tips
(`docs/superpowers/specs/2026-08-04-council-composer-attachments.md`
documents the attachment design; the picker never landed on this
branch).

## Test plan
- [x] Unit: tip rendering + selection swaps, attach button/chips
add-remove/cap, dispatch carries `file_ids` on council and deep-research
paths, upload-failure aborts the post, `postThreadReply` file-id
forwarding (council suite green)
- [x] `bash scripts/verify-web.sh` — guards, tsc, vitest (8050 tests),
eslint all green; coverage thresholds pass
- [x] Manual (mock stack + Chrome): tips swap across all depth/tier
pills; attach → chips render with correct dark-theme contrast → remove
works
- [ ] Staging (post-merge): dispatch a council run with attachments and
confirm the skill sees the files in the run thread (skill contract does
not formalize attachments yet — noted in the spec)
```

### PR body

## Linear
<!-- no Linear issue for this change -->

## Summary
- Add explanatory tips under the Council composer's Depth and Tier rows. Depth tips give the council size per depth (quick/standard/deep = 3/4/5 members, Auto = the skill classifies the topic); tier tips name each tier's representative models with a "Latest" suffix to signal the skill resolves each series to the newest version on the pod (e.g. "Mid-class models · Claude Sonnet Latest, GPT Terra Latest, Gemini Flash Latest… · the balanced default."). Copy is grounded in `ecap-skills/council` (`SKILL.md` + `roster.py` tier lineups / `SEATS_BY_DEPTH`).
- Add file attachments to the Council/Deep-Research composer: paperclip button + pending-attachment chips (name · size · remove) with the Mattermost per-post file cap enforced. On dispatch, files upload to the run thread's channel via the existing `uploadMattermostAttachment` helper (HEIC normalization + image-downscale retries), and the topic post carries their `file_ids` — `postThreadReply` gains an optional `fileIds` pass-through to `sendPost`. Protocol messages (`go` / `cancel` / tier tokens) never attach files. Upload failure aborts the dispatch post and keeps the files for retry; success clears them.
- Map the `--chat-ui-*` CSS variables to app semantic tokens on the chips container so `AttachmentChip` follows the app theme (its built-in fallbacks are light-mode colors, which rendered unreadable chips in dark mode).
- Design note: a per-model selection picker was explored and specced during review but deliberately dropped in favor of the simpler tips (`docs/superpowers/specs/2026-08-04-council-composer-attachments.md` documents the attachment design; the picker never landed on this branch).

## Test plan
- [x] Unit: tip rendering + selection swaps, attach button/chips add-remove/cap, dispatch carries `file_ids` on council and deep-research paths, upload-failure aborts the post, `postThreadReply` file-id forwarding (council suite green)
- [x] `bash scripts/verify-web.sh` — guards, tsc, vitest (8050 tests), eslint all green; coverage thresholds pass
- [x] Manual (mock stack + Chrome): tips swap across all depth/tier pills; attach → chips render with correct dark-theme contrast → remove works
- [ ] Staging (post-merge): dispatch a council run with attachments and confirm the skill sees the files in the run thread (skill contract does not formalize attachments yet — noted in the spec)



---

## 3b7fa205 — feat(agent-share): add frontend-only public share page (#3216)

- sha: 3b7fa205420052b5930a1c30463c650d19438aca
- 作者: ericma-srp
- 日期: 2026-08-04T07:49:49Z
- PR: #3216

### Commit message

```
feat(agent-share): add frontend-only public share page (#3216)

## Linear

N/A

## Summary

- Add a frontend-only Agent Store-style public pack page using the
anonymous fields already available on `main`.
- Preserve the dedicated share-page header, all-method login return
path, hire routing, paid-pack CTA behavior, avatar-derived hero,
conditional field rendering, and natural hero-tail sticky treatment.
- Keep the share page inside the common marketing chrome so it renders
the same `LandingFooter` and `getFooterColumns` source as the ZooClaw
homepage; homepage footer changes therefore flow through automatically.
- Add a local mock fixture for visual QA and regression tests for the
stable-field boundary, shared footer, header auth flow, and hire links.

## Scope

- Frontend only: all changed files are under `web/`.
- No `services/` code, database schema, backend response model, or
production API change.
- This is the fast-release frontend-only alternative to #3166; the
existing frontend + backend PR remains separate.

## Known limitations

- Trigger words, version, author, license, languages, archive size,
published time, and release notes are intentionally omitted because the
current anonymous response does not reliably expose them.
- Missing optional values are omitted instead of rendering empty
information rows.

## Test plan

- [x] Targeted share-page and authentication tests — 99 tests across 6
files passed, including `LoginForm`, email OTP verification, and phone
verification return paths.
- [x] `bash scripts/verify-web.sh --no-test` — governance guards,
TypeScript, and ESLint passed.
- [x] `bash scripts/verify-changed.sh` — all changed surfaces passed.
- [x] Browser QA at `/zh/packs/mock-agent-share-frontend-only`: hero,
sticky state, stable fields, CTA routing, and zero console errors.
- [x] Compared the local and production homepage footer: identical text
and all 26 links.

---------

Co-authored-by: eric <eric.ma@creatibi.com>
```

### PR body

## Linear

N/A

## Summary

- Add a frontend-only Agent Store-style public pack page using the anonymous fields already available on `main`.
- Preserve the dedicated share-page header, all-method login return path, hire routing, paid-pack CTA behavior, avatar-derived hero, conditional field rendering, and natural hero-tail sticky treatment.
- Keep the share page inside the common marketing chrome so it renders the same `LandingFooter` and `getFooterColumns` source as the ZooClaw homepage; homepage footer changes therefore flow through automatically.
- Add a local mock fixture for visual QA and regression tests for the stable-field boundary, shared footer, header auth flow, and hire links.

## Scope

- Frontend only: all changed files are under `web/`.
- No `services/` code, database schema, backend response model, or production API change.
- This is the fast-release frontend-only alternative to #3166; the existing frontend + backend PR remains separate.

## Known limitations

- Trigger words, version, author, license, languages, archive size, published time, and release notes are intentionally omitted because the current anonymous response does not reliably expose them.
- Missing optional values are omitted instead of rendering empty information rows.

## Test plan

- [x] Targeted share-page and authentication tests — 99 tests across 6 files passed, including `LoginForm`, email OTP verification, and phone verification return paths.
- [x] `bash scripts/verify-web.sh --no-test` — governance guards, TypeScript, and ESLint passed.
- [x] `bash scripts/verify-changed.sh` — all changed surfaces passed.
- [x] Browser QA at `/zh/packs/mock-agent-share-frontend-only`: hero, sticky state, stable fields, CTA routing, and zero console errors.
- [x] Compared the local and production homepage footer: identical text and all 26 links.



---

## 0df94387 — feat(agent-builder): complete v2 Agent Studio runtime projection (#3215)

- sha: 0df94387bc3087107e057623f2a45a274f2b19d1
- 作者: kaka-srp
- 日期: 2026-08-04T07:35:49Z
- PR: #3215

### Commit message

```
feat(agent-builder): complete v2 Agent Studio runtime projection (#3215)

## Summary

- project v2 Agent Pack `dependencies.python` and `dependencies.bins`
into Engine Environment packages and include them in Environment
identity;
- keep ordinary installed Agents and Pack Test on Engine's default
onboarding lifecycle, while creating only the shared hidden Agent
Builder with `onboarding:false`;
- apply candidate avatar metadata to the Pack Test workspace using the
same bounded archive validation used by Submit;
- preserve Pack Test's existing physical-Agent reuse policy: no
onboarding-specific replacement or update branch;
- share avatar parsing and split dependency/model/install policy into
focused modules so existing service files stay within repository size
limits.

Agent Studio source changes are reviewed separately in [ecap-agent-pack
PR #209](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/209).

## Design

The implementation follows [the checked-in
design](docs/superpowers/specs/2026-08-04-agent-studio-v2-runtime-completeness.md).

Important lifecycle behavior:

- each newly created installed Agent inherits Engine onboarding and
onboards once;
- Pack updates and new Sessions do not reset onboarding;
- uninstall/reinstall creates a new Agent and therefore onboards again;
- Agent Builder's hidden shared authoring Agent skips onboarding;
- Pack Test receives no onboarding special case.

## Compatibility

- normal install omits the `onboarding` field, preserving the existing
Engine default;
- legacy Pack translation remains permissive; strict dependency
validation is enabled only for v2 runtime assets and v2 Pack Test
candidates;
- empty dependency sets preserve the legacy Environment hash;
- no endpoint or Engine API shape is added beyond using Engine's
existing optional create-time `onboarding` field;
- v1 Builder behavior is unchanged; the only shared-file change moves
existing avatar validation into a common helper with its tests
preserved.

## Validation

- `bash scripts/verify-py.sh` — passed (ruff, formatting, pyright,
import contracts);
- focused Engine/Pack runtime tests — `279 passed`;
- additional model/lifecycle refactor coverage — `206 passed`;
- Pack Test runtime — `5 passed`;
- pre-commit and pre-push repository gates — passed.

## Staging acceptance

- create/open an Agent Builder v2 project;
- Package & Test a Pack with Python/binary dependencies and a relative
avatar;
- rerun Package & Test with persona-only changes and confirm Test Agent
reuse with a fresh Session;
- change Environment content/dependencies and confirm physical Agent
replacement;
- install a submitted Agent and confirm its own onboarding starts once.
```

### PR body

## Summary

- project v2 Agent Pack `dependencies.python` and `dependencies.bins` into Engine Environment packages and include them in Environment identity;
- keep ordinary installed Agents and Pack Test on Engine's default onboarding lifecycle, while creating only the shared hidden Agent Builder with `onboarding:false`;
- apply candidate avatar metadata to the Pack Test workspace using the same bounded archive validation used by Submit;
- preserve Pack Test's existing physical-Agent reuse policy: no onboarding-specific replacement or update branch;
- share avatar parsing and split dependency/model/install policy into focused modules so existing service files stay within repository size limits.

Agent Studio source changes are reviewed separately in [ecap-agent-pack PR #209](https://github.com/SerendipityOneInc/ecap-agent-pack/pull/209).

## Design

The implementation follows [the checked-in design](docs/superpowers/specs/2026-08-04-agent-studio-v2-runtime-completeness.md).

Important lifecycle behavior:

- each newly created installed Agent inherits Engine onboarding and onboards once;
- Pack updates and new Sessions do not reset onboarding;
- uninstall/reinstall creates a new Agent and therefore onboards again;
- Agent Builder's hidden shared authoring Agent skips onboarding;
- Pack Test receives no onboarding special case.

## Compatibility

- normal install omits the `onboarding` field, preserving the existing Engine default;
- legacy Pack translation remains permissive; strict dependency validation is enabled only for v2 runtime assets and v2 Pack Test candidates;
- empty dependency sets preserve the legacy Environment hash;
- no endpoint or Engine API shape is added beyond using Engine's existing optional create-time `onboarding` field;
- v1 Builder behavior is unchanged; the only shared-file change moves existing avatar validation into a common helper with its tests preserved.

## Validation

- `bash scripts/verify-py.sh` — passed (ruff, formatting, pyright, import contracts);
- focused Engine/Pack runtime tests — `279 passed`;
- additional model/lifecycle refactor coverage — `206 passed`;
- Pack Test runtime — `5 passed`;
- pre-commit and pre-push repository gates — passed.

## Staging acceptance

- create/open an Agent Builder v2 project;
- Package & Test a Pack with Python/binary dependencies and a relative avatar;
- rerun Package & Test with persona-only changes and confirm Test Agent reuse with a fresh Session;
- change Environment content/dependencies and confirm physical Agent replacement;
- install a submitted Agent and confirm its own onboarding starts once.



---

## 922928f1 — fix(web): restore custom specialists marketplace entry (#3219)

- sha: 922928f19ede5ab98131f6ce4178254c12aaa974
- 作者: lynn Zhuang
- 日期: 2026-08-04T07:06:29Z
- PR: #3219

### Commit message

```
fix(web): restore custom specialists marketplace entry (#3219)

## Linear

N/A — no Linear issue was provided.

## Summary

- restore the `My Custom Specialists` entry beside the Agent Marketplace
subtitle
- link the entry to `/agents-manager/publish` and hide it while
authentication is loading
- update unit coverage for the restored entry and loading state

## Test plan

- [x] `bash scripts/verify-web.sh
'src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx'
tests/unit/app/agents-manager-client.unit.spec.tsx
tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx`
- [x] verify the Marketplace in the local `ready-user` mock session and
confirm the entry appears once
```

### PR body

## Linear

N/A — no Linear issue was provided.

## Summary

- restore the `My Custom Specialists` entry beside the Agent Marketplace subtitle
- link the entry to `/agents-manager/publish` and hide it while authentication is loading
- update unit coverage for the restored entry and loading state

## Test plan

- [x] `bash scripts/verify-web.sh 'src/app/[locale]/(app)/(chat)/agents-manager/AgentsManagerClient.tsx' tests/unit/app/agents-manager-client.unit.spec.tsx tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx`
- [x] verify the Marketplace in the local `ready-user` mock session and confirm the entry appears once



---

## f3b1e947 — fix(whatsapp): surface real send failures in outbound delivery logs (#3217)

- sha: f3b1e947a3a4cd5080df087181b48f97bd540bab
- 作者: bill-srp
- 日期: 2026-08-04T06:55:56Z
- PR: #3217

### Commit message

```
fix(whatsapp): surface real send failures in outbound delivery logs (#3217)

## Summary
- Log outbound Mattermost→WhatsApp delivery failures under pino's `err`
key (previously logged under `error`, which pino does not serialize, so
every failure appeared as `"error": {}` with no detail) and attach
`mattermost_post_id` / `mattermost_channel_id` context.
- Include the (truncated, ≤500 chars) Meta Graph API error response body
in the `WhatsApp message send failed: <status>` error, so token expiry /
recipient-not-allowed reasons are visible instead of just the HTTP
status.
- Add outcome logging for the outbound path: info-level on successful
delivery (`mattermost_post_id` + `whatsapp_message_id`), debug-level for
not-delivered results (`ignored_event` / `invalid_post` /
`empty_message` / `unmapped_post`) to keep per-post noise out of info.
- Move the onEvent logging into a testable helper
(`handleMattermostWebSocketEventWithLogging` in
`mattermost-outbound.ts`) so `main.ts` stays a thin composition root.

## Root cause
Staging showed repeated `failed to deliver Mattermost post to WhatsApp`
entries with an empty `error: {}` payload. Two compounding issues:
`main.ts` passed the exception as `{ error }` (pino only serializes
`Error` instances under the `err` key), and `whatsapp-graph.ts` threw
only the HTTP status, discarding the Graph API response body that
carries Meta's actual error (in this incident: an expired staging
`WHATSAPP_ACCESS_TOKEN`, OAuth code 190 subcode 463 — rotated separately
via Vault; this PR fixes the observability that hid it).

## Test plan
- [x] TDD: new vitest coverage for delivered/not-delivered/error logging
(`mattermost-outbound.test.ts`) and enriched + truncated Graph error
bodies (`whatsapp-graph.test.ts`)
- [x] `pnpm test` in `services/whatsapp-business-service` — 6 files, 76
tests passed
- [x] `pnpm run typecheck` — clean
- [x] `pnpm run build` — clean
```

### PR body

## Summary
- Log outbound Mattermost→WhatsApp delivery failures under pino's `err` key (previously logged under `error`, which pino does not serialize, so every failure appeared as `"error": {}` with no detail) and attach `mattermost_post_id` / `mattermost_channel_id` context.
- Include the (truncated, ≤500 chars) Meta Graph API error response body in the `WhatsApp message send failed: <status>` error, so token expiry / recipient-not-allowed reasons are visible instead of just the HTTP status.
- Add outcome logging for the outbound path: info-level on successful delivery (`mattermost_post_id` + `whatsapp_message_id`), debug-level for not-delivered results (`ignored_event` / `invalid_post` / `empty_message` / `unmapped_post`) to keep per-post noise out of info.
- Move the onEvent logging into a testable helper (`handleMattermostWebSocketEventWithLogging` in `mattermost-outbound.ts`) so `main.ts` stays a thin composition root.

## Root cause
Staging showed repeated `failed to deliver Mattermost post to WhatsApp` entries with an empty `error: {}` payload. Two compounding issues: `main.ts` passed the exception as `{ error }` (pino only serializes `Error` instances under the `err` key), and `whatsapp-graph.ts` threw only the HTTP status, discarding the Graph API response body that carries Meta's actual error (in this incident: an expired staging `WHATSAPP_ACCESS_TOKEN`, OAuth code 190 subcode 463 — rotated separately via Vault; this PR fixes the observability that hid it).

## Test plan
- [x] TDD: new vitest coverage for delivered/not-delivered/error logging (`mattermost-outbound.test.ts`) and enriched + truncated Graph error bodies (`whatsapp-graph.test.ts`)
- [x] `pnpm test` in `services/whatsapp-business-service` — 6 files, 76 tests passed
- [x] `pnpm run typecheck` — clean
- [x] `pnpm run build` — clean



---

## 5f1ee0e1 — fix(agent-builder): correct v1 connection handling (#3213)

- sha: 5f1ee0e1c12afaa9147b0f04767eab33d799ff7d
- 作者: kaka-srp
- 日期: 2026-08-04T03:05:14Z
- PR: #3213

### Commit message

```
fix(agent-builder): correct v1 connection handling (#3213)

## Summary

- make the v1 Agent Builder header report the builder computer's
Mattermost transport instead of the unrelated global OpenClaw WebSocket
- let ready v1 Pack Test previews connect without waiting on stale
Mattermost bot presence
- preserve the existing Engine v2 presence gate and hidden Builder
connection status

## Root cause

The v1 Builder supplied no explicit connection source, so
`/agent-builder` fell back to the global OpenClaw WebSocket and computer
even though Builder messaging uses Mattermost. Separately, v1 Test
passed `botUserId` to the shared Mattermost `autoConnect`, which blocked
WebSocket setup while Mattermost presence remained `offline` even after
the preview bot had connected.

## Scope

- frontend only
- v1 Agent Builder project header and v1 Pack Test preview connection
only
- no backend or shared presence-polling behavior changes
- Engine v2 behavior remains unchanged

## Test plan

- [x] targeted Agent Builder and connection-status unit tests (82
passed)
- [x] `bash scripts/verify-local.sh --web-static ...`
- [x] TypeScript and ESLint
- [x] import-boundary and test-duplication checks
- [x] pre-push changed-surface verification
```

### PR body

## Summary

- make the v1 Agent Builder header report the builder computer's Mattermost transport instead of the unrelated global OpenClaw WebSocket
- let ready v1 Pack Test previews connect without waiting on stale Mattermost bot presence
- preserve the existing Engine v2 presence gate and hidden Builder connection status

## Root cause

The v1 Builder supplied no explicit connection source, so `/agent-builder` fell back to the global OpenClaw WebSocket and computer even though Builder messaging uses Mattermost. Separately, v1 Test passed `botUserId` to the shared Mattermost `autoConnect`, which blocked WebSocket setup while Mattermost presence remained `offline` even after the preview bot had connected.

## Scope

- frontend only
- v1 Agent Builder project header and v1 Pack Test preview connection only
- no backend or shared presence-polling behavior changes
- Engine v2 behavior remains unchanged

## Test plan

- [x] targeted Agent Builder and connection-status unit tests (82 passed)
- [x] `bash scripts/verify-local.sh --web-static ...`
- [x] TypeScript and ESLint
- [x] import-boundary and test-duplication checks
- [x] pre-push changed-surface verification



---

## 941ed9e5 — feat(agents): remove auto Hi greeting after agent install (#3214)

- sha: 941ed9e59a60aab8fa363685dca7f47863ffee09
- 作者: bill-srp
- 日期: 2026-08-04T02:51:34Z
- PR: #3214

### Commit message

```
feat(agents): remove auto Hi greeting after agent install (#3214)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Remove the automatic "Hi" activation message sent to an agent's
Mattermost DM channel after every install, across all three
computer-runtime install flows (the engine runtime never auto-messaged):
- V2 background install: `agent_install_service.install_agent` no longer
runs the post-commit activation stage; the now-unused
`skip_mattermost_activation` parameter is removed from `install_agent` /
`run_agent_install_background` and its `agent_builder.py` caller.
- Legacy install route (`routes/openclaw_agents/install.py`): activation
block and `activate_agent` stage marks removed.
- Hire flow (`lifecycle.py`): `_activate_hired_agents` removed from
`shared.py`.
- Delete the now-dead helpers
`ensure_agent_mattermost_ready_and_activate`,
`wait_for_agent_mattermost_ready`, and `_account_ready` (vulture
dead-code guard scans `app/`). `post_agent_mattermost_message` and
`get_agent_mattermost_bot_entry` are kept — still used by
`/agents/{agent_id}/reset-session`.
- Keep the `InstallAgentRequest.skip_mattermost_activation` API field:
it still gates deploy-time Mattermost readiness
(`require_mattermost_ready`); only its description changed.

Product note: the auto "Hi" previously triggered `BOOTSTRAP.md`
onboarding right after install/hire. With this change, an agent
bootstraps on the user's first real message instead.

## Test plan
- [x] Unit: 269 tests pass across `test_agent_install_service.py`,
`test_openclaw_agents.py`, `test_agent_builder_routes.py` (install/hire
paths assert no activation message is posted; tests for deleted helpers
removed)
- [x] BDD: 19 scenarios pass in
`tests/bdd/step_defs/test_openclaw_custom_agents.py` against local Mongo
- [x] `bash scripts/verify-py.sh`: ruff + ruff-format + pyright +
import-linter clean (8/8 contracts kept)
- [x] No residual references to removed symbols in `app/`, `tests/`, or
the vulture whitelist
```

### PR body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Remove the automatic "Hi" activation message sent to an agent's Mattermost DM channel after every install, across all three computer-runtime install flows (the engine runtime never auto-messaged):
  - V2 background install: `agent_install_service.install_agent` no longer runs the post-commit activation stage; the now-unused `skip_mattermost_activation` parameter is removed from `install_agent` / `run_agent_install_background` and its `agent_builder.py` caller.
  - Legacy install route (`routes/openclaw_agents/install.py`): activation block and `activate_agent` stage marks removed.
  - Hire flow (`lifecycle.py`): `_activate_hired_agents` removed from `shared.py`.
- Delete the now-dead helpers `ensure_agent_mattermost_ready_and_activate`, `wait_for_agent_mattermost_ready`, and `_account_ready` (vulture dead-code guard scans `app/`). `post_agent_mattermost_message` and `get_agent_mattermost_bot_entry` are kept — still used by `/agents/{agent_id}/reset-session`.
- Keep the `InstallAgentRequest.skip_mattermost_activation` API field: it still gates deploy-time Mattermost readiness (`require_mattermost_ready`); only its description changed.

Product note: the auto "Hi" previously triggered `BOOTSTRAP.md` onboarding right after install/hire. With this change, an agent bootstraps on the user's first real message instead.

## Test plan
- [x] Unit: 269 tests pass across `test_agent_install_service.py`, `test_openclaw_agents.py`, `test_agent_builder_routes.py` (install/hire paths assert no activation message is posted; tests for deleted helpers removed)
- [x] BDD: 19 scenarios pass in `tests/bdd/step_defs/test_openclaw_custom_agents.py` against local Mongo
- [x] `bash scripts/verify-py.sh`: ruff + ruff-format + pyright + import-linter clean (8/8 contracts kept)
- [x] No residual references to removed symbols in `app/`, `tests/`, or the vulture whitelist



---
