# SerendipityOneInc/ecap-workspace — commits 2026-08-10

## fix(billing): handle Creem trial paid events (#3325)

- **SHA**: `65f33fe3f400bfb6aae9e7ca5567676efff777de`
- **作者**: tim-srp
- **日期**: 2026-08-10T13:58:28Z
- **PR**: #3325

### Commit Message

```
fix(billing): handle Creem trial paid events (#3325)
```

### PR Body

## Summary
- Route Creem `subscription.paid` events whose subscription is still `trialing` through the existing fail-closed trial projection.
- Preserve the strict transaction and amount validation for normal `active` first payments.
- Cover both Creem event shapes accepted by the trial projection.

## Root cause
Creem starts a provider-managed free trial by sending `subscription.paid` with subscription status `trialing`. It does not send the expected `subscription.trialing` event in this checkout flow. The dispatcher therefore sent the event to normal first-payment settlement, which correctly rejected the zero-paid trial invoice and left the local order pending without Starter credits.

## Test plan
- [x] RED: new dispatcher regression test failed against the old routing.
- [x] `python -m pytest tests/unit/test_creem_first_payment.py tests/unit/test_creem_trial_lifecycle.py -q` (44 passed)
- [x] `python -m pytest tests/unit/test_creem*.py -q` (542 passed)
- [x] Ruff check and format for changed files
- [x] Pyright for changed files with the active Python interpreter (0 errors)
- [x] Pre-commit backend hooks, including repository Pyright and import contracts

## Staging evidence
- Creem subscription was created as `trialing` with a seven-day period and a zero-paid trial invoice.
- The signed `subscription.paid` webhook was recorded as failed with `billing.creem.first_payment_conflict`.
- Checkout binding completed, but the payment order remained pending and no Starter entitlement was granted.

## Recovery
After deployment, Creem webhook retry or the existing bound-trial reconciliation job can project affected pending trial orders idempotently.


---

## fix(agent-builder): guard v2 initialization and test models (#3320)

- **SHA**: `a7d7cc5ca1876aa22d0ac188fb8530e7a5cfb9e7`
- **作者**: kaka-srp
- **日期**: 2026-08-10T12:47:37Z
- **PR**: #3320

### Commit Message

```
fix(agent-builder): guard v2 initialization and test models (#3320)

## Summary

- serialize all Agent Builder v2 workspace mutations with one
server-authoritative, fenced lease per shared Builder runtime
- require a confirmed activation before turns, keep uncertain mutations
fail-closed, and reconcile only ambiguous turn posts from Mattermost's
authoritative thread state
- make turn stop/finish/recovery transitions atomic, including
cross-project page acquisition and concurrent stop dispatch
- keep the turn POST path bounded and let the client reconcile a
timed-out response by `pending_post_id`
- add Engine v2 Test Agent model selection with project/test-run-scoped
authorization
- keep the legacy v1 route, Model API, and backend runtime unchanged

## Root cause

The previous v2 lock mixed page ownership and background mutations
without a single fenced operation state. That allowed
initialization/renewal races, synchronous activation in the turn
request, and ambiguous Mattermost POST failures that could either
release too early or leave the shared workspace permanently locked. Test
Agent model selection also lacked an API scoped to the hidden Pack Test
workspace.

## Recovery policy

- explicit validation/rejection: release the operation
- uncertain activate/package/runtime mutation: retain
`recovery_required`
- uncertain turn POST: persist `pending_post_id`, read the authoritative
Mattermost thread, and use an exact operation/fence CAS
  - terminal matching post: release
- active matching post: bind its real post id and retain recovery
ownership
- no matching post: release only after the post timeout plus a
conservative 60-second grace
- unreadable/malformed thread or concurrent stop dispatch: make no
change

## Validation

- Agent Builder backend unit suite: 386 passed
- Mattermost client unit suite: 41 passed
- focused frontend unit suite: 131 passed across 7 files
- Ruff formatting/lint, Pyright, targeted ESLint/TypeScript, import
lint, and complexity gate
- `git diff --check`

## Size override justification

This is one cohesive concurrency correction across the lease schema,
Mongo CAS transitions, route/service handoff, client reconciliation, and
behavioral race tests. Splitting it would leave intermediate PRs with
incompatible state transitions or unprotected callers. The
implementation itself remains scoped to Agent Builder v2; the extra
lines are primarily explicit race coverage, and v1 is unchanged.
```

### PR Body

## Summary

- serialize all Agent Builder v2 workspace mutations with one server-authoritative, fenced lease per shared Builder runtime
- require a confirmed activation before turns, keep uncertain mutations fail-closed, and reconcile only ambiguous turn posts from Mattermost's authoritative thread state
- make turn stop/finish/recovery transitions atomic, including cross-project page acquisition and concurrent stop dispatch
- keep the turn POST path bounded and let the client reconcile a timed-out response by `pending_post_id`
- add Engine v2 Test Agent model selection with project/test-run-scoped authorization
- keep the legacy v1 route, Model API, and backend runtime unchanged

## Root cause

The previous v2 lock mixed page ownership and background mutations without a single fenced operation state. That allowed initialization/renewal races, synchronous activation in the turn request, and ambiguous Mattermost POST failures that could either release too early or leave the shared workspace permanently locked. Test Agent model selection also lacked an API scoped to the hidden Pack Test workspace.

## Recovery policy

- explicit validation/rejection: release the operation
- uncertain activate/package/runtime mutation: retain `recovery_required`
- uncertain turn POST: persist `pending_post_id`, read the authoritative Mattermost thread, and use an exact operation/fence CAS
  - terminal matching post: release
  - active matching post: bind its real post id and retain recovery ownership
  - no matching post: release only after the post timeout plus a conservative 60-second grace
  - unreadable/malformed thread or concurrent stop dispatch: make no change

## Validation

- Agent Builder backend unit suite: 386 passed
- Mattermost client unit suite: 41 passed
- focused frontend unit suite: 131 passed across 7 files
- Ruff formatting/lint, Pyright, targeted ESLint/TypeScript, import lint, and complexity gate
- `git diff --check`

## Size override justification

This is one cohesive concurrency correction across the lease schema, Mongo CAS transitions, route/service handoff, client reconciliation, and behavioral race tests. Splitting it would leave intermediate PRs with incompatible state transitions or unprotected callers. The implementation itself remains scoped to Agent Builder v2; the extra lines are primarily explicit race coverage, and v1 is unchanged.


---

## feat(org): support personal users joining enterprise (#3323)

- **SHA**: `f4b9c441be948559611455390ab4a4cf33d845ea`
- **作者**: kaka-srp
- **日期**: 2026-08-10T11:31:27Z
- **PR**: #3323

### Commit Message

```
feat(org): support personal users joining enterprise (#3323)

## Linear

N/A — no Linear issue was supplied.

## Summary

- allow an existing personal account to redeem an enterprise invite and
become a normal active enterprise member without a feature flag or
organization allowlist
- stop personal subscription renewal, then strictly stop personal v2
Computers and Engine Agents and disable user schedules and channel
bindings before switching billing ownership
- rebind the canonical user key to the enterprise Billing Team, verify
its non-secret billing readback, and atomically swap membership with
retry and compensation paths
- reuse the strict v2 cleanup abstraction for subscription-expiry
resource reclamation and add reconciliation, diagnostics, and a
pre-deploy invariant audit
- update enterprise-admin invite UX with explicit shutdown disclosure,
actionable provider/runtime/billing errors, retry support, and
enterprise redirect; iOS remains unchanged and no new collection/table
is introduced

## Cross-repo dependency

- Billing Gateway must be deployed first:
https://github.com/SerendipityOneInc/billing-gateway/pull/66

## Rollout

1. Merge and deploy the Billing Gateway dependency.
2. Run `python -m scripts.audit_existing_personal_enterprise_join_v2`
from `services/claw-interface` and repair any reported invariant
violations.
3. Deploy claw-interface, then enterprise-admin.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `pytest -q tests/unit/test_membership_service.py
tests/unit/test_routes_org_users.py
tests/unit/test_personal_enterprise_join.py` — 74 passed
- [x] broader task-related claw-interface regression — 463 passed
- [x] `pnpm lint` in `web/enterprise-admin`
- [x] `pnpm test` in `web/enterprise-admin` — 362 passed after merging
current `main`
- [x] `git diff --check`
```

### PR Body

## Linear

N/A — no Linear issue was supplied.

## Summary

- allow an existing personal account to redeem an enterprise invite and become a normal active enterprise member without a feature flag or organization allowlist
- stop personal subscription renewal, then strictly stop personal v2 Computers and Engine Agents and disable user schedules and channel bindings before switching billing ownership
- rebind the canonical user key to the enterprise Billing Team, verify its non-secret billing readback, and atomically swap membership with retry and compensation paths
- reuse the strict v2 cleanup abstraction for subscription-expiry resource reclamation and add reconciliation, diagnostics, and a pre-deploy invariant audit
- update enterprise-admin invite UX with explicit shutdown disclosure, actionable provider/runtime/billing errors, retry support, and enterprise redirect; iOS remains unchanged and no new collection/table is introduced

## Cross-repo dependency

- Billing Gateway must be deployed first: https://github.com/SerendipityOneInc/billing-gateway/pull/66

## Rollout

1. Merge and deploy the Billing Gateway dependency.
2. Run `python -m scripts.audit_existing_personal_enterprise_join_v2` from `services/claw-interface` and repair any reported invariant violations.
3. Deploy claw-interface, then enterprise-admin.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] `pytest -q tests/unit/test_membership_service.py tests/unit/test_routes_org_users.py tests/unit/test_personal_enterprise_join.py` — 74 passed
- [x] broader task-related claw-interface regression — 463 passed
- [x] `pnpm lint` in `web/enterprise-admin`
- [x] `pnpm test` in `web/enterprise-admin` — 362 passed after merging current `main`
- [x] `git diff --check`


---

## feat(billing): move Card free trials to Creem (#3318)

- **SHA**: `13a0e7d93123b6f338fa76af2390b0ca29829d55`
- **作者**: tim-srp
- **日期**: 2026-08-10T10:36:27Z
- **PR**: #3318

### Commit Message

```
feat(billing): move Card free trials to Creem (#3318)

## Linear

N/A

## Summary

- Route eligible Starter Card free trials through Creem Test Mode hosted
checkout with provider-managed 7-day trials and no $1 authorization.
- Keep the existing Alipay free-trial flow unchanged and hard-disable
the removed Stripe trial-authorization path.
- Project authenticated Creem trialing webhooks into Billing v2, support
cancellation, and reconcile Creem subscription state through the
existing hourly maintenance job.
- Add Test Mode trial product configuration, server-side eligibility and
product selection, typed webhook schemas, frontend trial
capability/copy, and comprehensive regression tests.

## Test plan

- [x] Backend targeted suite: 576 passed.
- [x] Creem lifecycle/checkout suite: 84 passed.
- [x] Frontend verification: TypeScript, governance checks, ESLint, and
359 unit tests passed (1 skipped).
- [x] Post-merge changed-surface gate: frontend checks, Ruff, Ruff
format, and import-linter passed.
- [ ] CI Pyright (local host selected Miniconda Pyright without project
dependencies, producing missing-import errors; commit checks and
targeted behavior tests passed).
- [x] Confirmed both Creem Test Mode Trial Product IDs are synchronized
from Vault into the staging Kubernetes Secret.

## Operational notes

- Trial products were created only in Creem Test Mode.
- Staging Vault contains `CREEM_PRODUCT_ID_STARTER_MONTHLY_TRIAL` and
`CREEM_PRODUCT_ID_STARTER_YEARLY_TRIAL`.
- Production configuration was not modified.
```

### PR Body

## Linear

N/A

## Summary

- Route eligible Starter Card free trials through Creem Test Mode hosted checkout with provider-managed 7-day trials and no $1 authorization.
- Keep the existing Alipay free-trial flow unchanged and hard-disable the removed Stripe trial-authorization path.
- Project authenticated Creem trialing webhooks into Billing v2, support cancellation, and reconcile Creem subscription state through the existing hourly maintenance job.
- Add Test Mode trial product configuration, server-side eligibility and product selection, typed webhook schemas, frontend trial capability/copy, and comprehensive regression tests.

## Test plan

- [x] Backend targeted suite: 576 passed.
- [x] Creem lifecycle/checkout suite: 84 passed.
- [x] Frontend verification: TypeScript, governance checks, ESLint, and 359 unit tests passed (1 skipped).
- [x] Post-merge changed-surface gate: frontend checks, Ruff, Ruff format, and import-linter passed.
- [ ] CI Pyright (local host selected Miniconda Pyright without project dependencies, producing missing-import errors; commit checks and targeted behavior tests passed).
- [x] Confirmed both Creem Test Mode Trial Product IDs are synchronized from Vault into the staging Kubernetes Secret.

## Operational notes

- Trial products were created only in Creem Test Mode.
- Staging Vault contains `CREEM_PRODUCT_ID_STARTER_MONTHLY_TRIAL` and `CREEM_PRODUCT_ID_STARTER_YEARLY_TRIAL`.
- Production configuration was not modified.


---

## feat(service-api): enable GET /service/v1/agents list with forced ownership anchors (#3321)

- **SHA**: `80fc522416933d604ba88a39272567c3fc44db2f`
- **作者**: bill-srp
- **日期**: 2026-08-10T09:16:49Z
- **PR**: #3321

### Commit Message

```
feat(service-api): enable GET /service/v1/agents list with forced ownership anchors (#3321)

# Summary

Enables `GET /service/v1/agents` (list) in the service-token API. It
previously returned a fail-closed, tenant-hiding 404 — a v1 placeholder
from the org-service-tokens design spec, pending verification that
controld's list endpoint enforces an ownership filter.

That verification is now done (against `zooclaw-engine`
`services/controld/src/http/routes-agents.ts`): controld's `GET
/v1/agents` **requires** both `owner_uid` and `org_id` query params (400
otherwise) and enforces them server-side in the SQL `WHERE` clause, so a
scoped list cannot leak cross-tenant agents.

## Changes

- `_agents.handle` gains a `GET` branch on the bare `agents` path,
mirroring the existing skills-family list pattern exactly: strip
caller-supplied `owner_uid`/`org_id`, force `owner_uid=token.bound_uid`
and `org_id=token.org_id`, forward to engine `/v1/agents`. Other query
params (`page`, label filters) pass through unchanged. Engine 5xx is
masked via the existing `gateway_error` path.
- Per-agent fetch-and-check tenancy, the credentials block, and POST
create are untouched.
- Spec `2026-08-05-org-service-tokens-design.md`: tenancy-table list
rule updated from "404 in v1" to the forced-anchor forwarding rule; the
plan-phase verification item is marked resolved with the evidence.

Note the resulting scope: the list is user+org scoped (agents created by
this token's `bound_uid` in its org), matching what the create path
stamps as ownership — controld requires both selectors, so an org-wide
cross-owner list is not expressible today.

## Test plan

- [x] TDD: 5 new unit tests in `test_service_proxy_agents.py` (written
first, confirmed failing 404 before implementation):
- forwards to engine with forced anchors and relays the 200 body
verbatim
- caller-supplied `owner_uid`/`org_id` are stripped and overridden
without duplicate params
  - other query params pass through alongside the forced anchors
  - non-GET/POST on the bare path still 404s (`service_api.not_found`)
  - engine 5xx masked as 502 `service.unavailable` with no upstream leak
- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright,
import-linter all green
- [x] All 49 service-proxy unit tests pass
(`test_service_proxy_{agents,core,skills,environments}.py`)
- [ ] Staging smoke with a real service token after backend release

Full pytest+coverage suite left to CI (unit scope of this change is
fully covered by the targeted files above).
```

### PR Body

# Summary

Enables `GET /service/v1/agents` (list) in the service-token API. It previously returned a fail-closed, tenant-hiding 404 — a v1 placeholder from the org-service-tokens design spec, pending verification that controld's list endpoint enforces an ownership filter.

That verification is now done (against `zooclaw-engine` `services/controld/src/http/routes-agents.ts`): controld's `GET /v1/agents` **requires** both `owner_uid` and `org_id` query params (400 otherwise) and enforces them server-side in the SQL `WHERE` clause, so a scoped list cannot leak cross-tenant agents.

## Changes

- `_agents.handle` gains a `GET` branch on the bare `agents` path, mirroring the existing skills-family list pattern exactly: strip caller-supplied `owner_uid`/`org_id`, force `owner_uid=token.bound_uid` and `org_id=token.org_id`, forward to engine `/v1/agents`. Other query params (`page`, label filters) pass through unchanged. Engine 5xx is masked via the existing `gateway_error` path.
- Per-agent fetch-and-check tenancy, the credentials block, and POST create are untouched.
- Spec `2026-08-05-org-service-tokens-design.md`: tenancy-table list rule updated from "404 in v1" to the forced-anchor forwarding rule; the plan-phase verification item is marked resolved with the evidence.

Note the resulting scope: the list is user+org scoped (agents created by this token's `bound_uid` in its org), matching what the create path stamps as ownership — controld requires both selectors, so an org-wide cross-owner list is not expressible today.

## Test plan

- [x] TDD: 5 new unit tests in `test_service_proxy_agents.py` (written first, confirmed failing 404 before implementation):
  - forwards to engine with forced anchors and relays the 200 body verbatim
  - caller-supplied `owner_uid`/`org_id` are stripped and overridden without duplicate params
  - other query params pass through alongside the forced anchors
  - non-GET/POST on the bare path still 404s (`service_api.not_found`)
  - engine 5xx masked as 502 `service.unavailable` with no upstream leak
- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright, import-linter all green
- [x] All 49 service-proxy unit tests pass (`test_service_proxy_{agents,core,skills,environments}.py`)
- [ ] Staging smoke with a real service token after backend release

Full pytest+coverage suite left to CI (unit scope of this change is fully covered by the targeted files above).


---

## feat(web): add Auth Action V2 lifecycle tracking (#3312)

- **SHA**: `72ea5c121ef4cf243d9aa417927951d386628aa8`
- **作者**: Mori-srp
- **日期**: 2026-08-10T09:08:30Z
- **PR**: #3312

### Commit Message

```
feat(web): add Auth Action V2 lifecycle tracking (#3312)

## What changed

- add the canonical `auth_started` event and a non-PII `auth_action_id`
for valid Email OTP, Phone, and Google authentication requests;
- retain the entry fact as `signup`, `login`, or `neutral_auth`, while
Account `created` / `existing` remains the terminal business truth;
- pass the immutable request-start action and safe attribution snapshot
to `account_created` or `login_succeeded`;
- keep the legacy `signup_started` contract only for explicit signup,
with `signup_action_id === auth_action_id`;
- carry typed auth context through the global modal and classify Tips,
ordinary Chat, Header Sign in, Get Started, and confirmed
expired-session gates honestly;
- keep analytics failures isolated from Account, cookies, registration,
login, and navigation.

## Why

The previous signup-only action ID could not connect valid `login ->
created` or neutral-gate registrations. Tips visitors could also be
classified as expired-session login before any confirmed identity
existed. This made the browser start event and Account-confirmed
terminal impossible to reconcile reliably.

This PR separates three facts:

1. the entry intent/surface/trigger;
2. the concrete authentication action;
3. the Account-confirmed `created` or `existing` result.

## Scope boundary

This is a front-end analytics contract change. It does **not** modify
Account backend creation semantics, databases, GTM, Page View
production, GA4 User-ID, Google Ads/Reddit conversion configuration,
Consent, or the known gtag bootstrap gap.

The current Draft covers the normal single-path Email OTP, Phone, Google
popup, and Google redirect flows. Low-frequency cross-generation races
(for example OTP A, then Google/OTP B, followed by a late A callback),
old-popup generation ownership, and fine-grained navigation/cross-tab
context reclamation are documented follow-ups and are not claimed as
solved here.

## Validation

- focused Auth Action regression: 12 files, 326/326 tests passed;
- TypeScript: `pnpm exec tsc --noEmit` passed;
- changed-file ESLint: 0 errors (74 pre-existing `no-explicit-any`
warnings in the large manager test file);
- `git diff --check` passed;
- earlier full unit run: 625/626 files passed in the sandbox; the only
`listen EPERM` file passed 32/32 when rerun in an environment allowed to
bind localhost.

## Remaining gates

- human review of the event contract and Account-truth boundary;
- deployed Staging Email OTP / Phone / Google acceptance;
- GA4 Network, DebugView, and BigQuery receipt after the independent
gtag bootstrap repair;
- no deployment or merge is requested by this Draft PR.
```

### PR Body

## What changed

- add the canonical `auth_started` event and a non-PII `auth_action_id` for valid Email OTP, Phone, and Google authentication requests;
- retain the entry fact as `signup`, `login`, or `neutral_auth`, while Account `created` / `existing` remains the terminal business truth;
- pass the immutable request-start action and safe attribution snapshot to `account_created` or `login_succeeded`;
- keep the legacy `signup_started` contract only for explicit signup, with `signup_action_id === auth_action_id`;
- carry typed auth context through the global modal and classify Tips, ordinary Chat, Header Sign in, Get Started, and confirmed expired-session gates honestly;
- keep analytics failures isolated from Account, cookies, registration, login, and navigation.

## Why

The previous signup-only action ID could not connect valid `login -> created` or neutral-gate registrations. Tips visitors could also be classified as expired-session login before any confirmed identity existed. This made the browser start event and Account-confirmed terminal impossible to reconcile reliably.

This PR separates three facts:

1. the entry intent/surface/trigger;
2. the concrete authentication action;
3. the Account-confirmed `created` or `existing` result.

## Scope boundary

This is a front-end analytics contract change. It does **not** modify Account backend creation semantics, databases, GTM, Page View production, GA4 User-ID, Google Ads/Reddit conversion configuration, Consent, or the known gtag bootstrap gap.

The current Draft covers the normal single-path Email OTP, Phone, Google popup, and Google redirect flows. Low-frequency cross-generation races (for example OTP A, then Google/OTP B, followed by a late A callback), old-popup generation ownership, and fine-grained navigation/cross-tab context reclamation are documented follow-ups and are not claimed as solved here.

## Validation

- focused Auth Action regression: 12 files, 326/326 tests passed;
- TypeScript: `pnpm exec tsc --noEmit` passed;
- changed-file ESLint: 0 errors (74 pre-existing `no-explicit-any` warnings in the large manager test file);
- `git diff --check` passed;
- earlier full unit run: 625/626 files passed in the sandbox; the only `listen EPERM` file passed 32/32 when rerun in an environment allowed to bind localhost.

## Remaining gates

- human review of the event contract and Account-truth boundary;
- deployed Staging Email OTP / Phone / Google acceptance;
- GA4 Network, DebugView, and BigQuery receipt after the independent gtag bootstrap repair;
- no deployment or merge is requested by this Draft PR.


---

## feat(pack): expose public shared pack metadata (#3319)

- **SHA**: `6b563417097c5459db314274c9733f35474968a5`
- **作者**: bill-srp
- **日期**: 2026-08-10T09:01:09Z
- **PR**: #3319

### Commit Message

```
feat(pack): expose public shared pack metadata (#3319)

## Linear

N/A

## Summary

- expose author name, current version, publication timestamp, and quick
commands from the anonymous shared-pack response
- keep the public payload allowlisted while preserving protected asset,
owner-id, organization, and billing fields
- preserve shared-pack version metadata and quick commands when mapping
the response into frontend agent detail state

## Test plan

- [x] `pytest -q tests/unit/test_shared_listing_service.py
tests/unit/test_public_agent_packs_routes.py
tests/unit/test_schema_pack.py
tests/unit/test_pack_schema_default_model.py` (69 passed)
- [x] backend Ruff check and format check
- [x] backend Pyright over `app/ tests/` (0 errors)
- [x] backend import-linter contracts
- [x] `bash scripts/verify-web.sh` for changed frontend files
(TypeScript, 38 related tests, ESLint)
```

### PR Body

## Linear

N/A

## Summary

- expose author name, current version, publication timestamp, and quick commands from the anonymous shared-pack response
- keep the public payload allowlisted while preserving protected asset, owner-id, organization, and billing fields
- preserve shared-pack version metadata and quick commands when mapping the response into frontend agent detail state

## Test plan

- [x] `pytest -q tests/unit/test_shared_listing_service.py tests/unit/test_public_agent_packs_routes.py tests/unit/test_schema_pack.py tests/unit/test_pack_schema_default_model.py` (69 passed)
- [x] backend Ruff check and format check
- [x] backend Pyright over `app/ tests/` (0 errors)
- [x] backend import-linter contracts
- [x] `bash scripts/verify-web.sh` for changed frontend files (TypeScript, 38 related tests, ESLint)


---

## fix(billing): allow free org credit topups (#3317)

- **SHA**: `275f746640619f3560738029e189ad5a5107c96c`
- **作者**: bill-srp
- **日期**: 2026-08-10T08:50:22Z
- **PR**: #3317

### Commit Message

```
fix(billing): allow free org credit topups (#3317)

## Summary
- allow team organizations without an Enterprise Package agreement to
create and confirm offline credit topups
- idempotently ensure the baseline Billing Gateway subscription before
granting team topup credits
- create and persist the team topup wallet when Billing Gateway has no
usable wallet, including a 404 credits response
- update the org-topup design contract and regression coverage

## Root cause

The org-topup lifecycle required an effective Enterprise Package
agreement at both order creation and confirmation. That policy blocked
free team organizations even though topup credits do not grant package
benefits or change model access. Personal-to-team upgrades could also
lack the Billing Gateway subscription and wallet required for
fulfillment.

## Test plan
- [x] `.venv/bin/pytest -q tests/unit/test_offline_topup_orders.py
tests/unit/test_billing_v2_fulfillment.py` — 37 passed
- [x] changed-file Pyright with the claw-interface venv — 0 errors
- [x] Ruff check and format — passed
- [x] import-linter — 8 contracts kept
- [x] dashboard-console Vitest — 71 files / 631 tests passed
- [x] dashboard-console ESLint and TypeScript build check — passed

The full local `verify-changed.sh` could not complete because the local
Pyright invocation did not resolve installed venv dependencies and
reported repository-wide missing imports. The same changed files pass
when Pyright is explicitly pointed at `.venv/bin/python`; CI remains
authoritative for the full backend gate.
```

### PR Body

## Summary
- allow team organizations without an Enterprise Package agreement to create and confirm offline credit topups
- idempotently ensure the baseline Billing Gateway subscription before granting team topup credits
- create and persist the team topup wallet when Billing Gateway has no usable wallet, including a 404 credits response
- update the org-topup design contract and regression coverage

## Root cause

The org-topup lifecycle required an effective Enterprise Package agreement at both order creation and confirmation. That policy blocked free team organizations even though topup credits do not grant package benefits or change model access. Personal-to-team upgrades could also lack the Billing Gateway subscription and wallet required for fulfillment.

## Test plan
- [x] `.venv/bin/pytest -q tests/unit/test_offline_topup_orders.py tests/unit/test_billing_v2_fulfillment.py` — 37 passed
- [x] changed-file Pyright with the claw-interface venv — 0 errors
- [x] Ruff check and format — passed
- [x] import-linter — 8 contracts kept
- [x] dashboard-console Vitest — 71 files / 631 tests passed
- [x] dashboard-console ESLint and TypeScript build check — passed

The full local `verify-changed.sh` could not complete because the local Pyright invocation did not resolve installed venv dependencies and reported repository-wide missing imports. The same changed files pass when Pyright is explicitly pointed at `.venv/bin/python`; CI remains authoritative for the full backend gate.


---

## feat(enterprise-admin): edit member AI quotas from the usage page (#3316)

- **SHA**: `03545f57cb2d9376f3ffadc9c877fce642aaf9e1`
- **作者**: bill-srp
- **日期**: 2026-08-10T08:22:38Z
- **PR**: #3316

### Commit Message

```
feat(enterprise-admin): edit member AI quotas from the usage page (#3316)

## Linear
<!-- no Linear issue for this feature -->

## Summary
- Let org admins edit a member's AI-credit quota directly from the
**Usage** page (follow-up to #3315), reusing the exact editing flow from
the Users page.
- Extracts the quota-dialog logic (state, validation, submit with toast,
per-row retryable issues, `reset_pending` retry) out of
`useUsersViewModel` into a shared `hooks/useQuotaEditor.ts`; the Users
view model now delegates to it with its **public contract unchanged** —
the Users page component and all its existing tests pass unmodified,
which is the regression proof for the extraction.
- `useUsageViewModel` composes the editor and exposes `openQuotaForRow`
(resolves the full org user for a row; rows without an active org user
are a no-op); `MemberUsageTable` gains a per-row pencil action plus a
Retry affordance on rows with a quota issue; the page renders the shared
`QuotaDialog`.
- The existing mutation's invalidation of `["member-llm-quotas", orgId]`
already refreshes both pages' tables — no new cache wiring. No backend
changes.

Design spec:
`docs/superpowers/specs/2026-08-10-usage-page-quota-edit-design.md`
(committed here with the implementation plan).

## Test plan
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm run lint` — clean (`--max-warnings=0`)
- [x] Full vitest suite — 352/352 pass (14 new: 9 `useQuotaEditor` hook
cases, 2 usage view-model cases, 3 usage page cases)
- [x] Changed-file allow-list verified: no Users page/component/test
files modified — only `useUsersViewModel.ts` internals
- [ ] Staging smoke after web release: as a team-org admin, edit a quota
from the Usage page, confirm the Users page quota dialog shows the same
value, and retry a `reset_pending` row
```

### PR Body

## Linear
<!-- no Linear issue for this feature -->

## Summary
- Let org admins edit a member's AI-credit quota directly from the **Usage** page (follow-up to #3315), reusing the exact editing flow from the Users page.
- Extracts the quota-dialog logic (state, validation, submit with toast, per-row retryable issues, `reset_pending` retry) out of `useUsersViewModel` into a shared `hooks/useQuotaEditor.ts`; the Users view model now delegates to it with its **public contract unchanged** — the Users page component and all its existing tests pass unmodified, which is the regression proof for the extraction.
- `useUsageViewModel` composes the editor and exposes `openQuotaForRow` (resolves the full org user for a row; rows without an active org user are a no-op); `MemberUsageTable` gains a per-row pencil action plus a Retry affordance on rows with a quota issue; the page renders the shared `QuotaDialog`.
- The existing mutation's invalidation of `["member-llm-quotas", orgId]` already refreshes both pages' tables — no new cache wiring. No backend changes.

Design spec: `docs/superpowers/specs/2026-08-10-usage-page-quota-edit-design.md` (committed here with the implementation plan).

## Test plan
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm run lint` — clean (`--max-warnings=0`)
- [x] Full vitest suite — 352/352 pass (14 new: 9 `useQuotaEditor` hook cases, 2 usage view-model cases, 3 usage page cases)
- [x] Changed-file allow-list verified: no Users page/component/test files modified — only `useUsersViewModel.ts` internals
- [ ] Staging smoke after web release: as a team-org admin, edit a quota from the Usage page, confirm the Users page quota dialog shows the same value, and retry a `reset_pending` row


---

## feat(enterprise-admin): add org usage page with per-member credits breakdown (#3315)

- **SHA**: `63bc8b983d9d0f520435517e2e0bad39d4351feb`
- **作者**: bill-srp
- **日期**: 2026-08-10T07:27:51Z
- **PR**: #3315

### Commit Message

```
feat(enterprise-admin): add org usage page with per-member credits breakdown (#3315)

## Linear
<!-- no Linear issue for this feature -->

## Summary
- Add an admin-only **Usage** page to the enterprise-admin console
showing the current org's credit usage: balance, used-this-period,
subscription/topup wallet split, credit period range, and a per-member
usage table (used vs quota, progress bar, unlimited state,
`reset_pending` badge).
- Frontend-only: composes three existing claw-interface endpoints
through the claw proxy — `GET /users/credits/check` (org pool via
team-first resolution), `GET /orgs/{org_id}/users/llm-quotas`
(per-member used/quota + period bounds), and the org users list for the
uid→name/email join. No backend changes.
- Follows the app's MVVM contract: `page.tsx` renders purely from a
co-located `useUsageViewModel`; new `useCreditsCheckQuery` hook +
`types/credits.ts`; `formatCredits` helper; zh catalog entries for all
new copy.
- Access control: nav entry is `adminOnly`, and `/usage` is added to
`ADMIN_ONLY_PREFIXES` so non-admin members are redirected to `/users`.
- States: per-section loading skeletons, independent stats/members error
alerts, and a billing-not-ready notice for orgs without an initialized
billing profile (`billing_initialized: false` or backend 503
`billing_not_ready`).

Design spec:
`docs/superpowers/specs/2026-08-10-enterprise-admin-org-usage-page-design.md`
(included in this PR along with the implementation plan).

## Test plan
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm run lint` — clean (`--max-warnings=0`)
- [x] `pnpm run test:coverage` — 51 suites, 337 tests pass; new
co-located specs cover the credits hook (fetch URL + disabled states),
view model (wallet filtering, uid join, sort, quota/unlimited/pct,
billing-not-ready, independent errors), page rendering (cards, table,
skeletons, notices, alerts), sidebar visibility, and the `/usage` guard
redirect
- [ ] Staging smoke after web release: log in as a team-org admin, open
**Usage**, verify balance/used figures match `/users/credits` data and
the member table matches the Users page quota dialog
```

### PR Body

## Linear
<!-- no Linear issue for this feature -->

## Summary
- Add an admin-only **Usage** page to the enterprise-admin console showing the current org's credit usage: balance, used-this-period, subscription/topup wallet split, credit period range, and a per-member usage table (used vs quota, progress bar, unlimited state, `reset_pending` badge).
- Frontend-only: composes three existing claw-interface endpoints through the claw proxy — `GET /users/credits/check` (org pool via team-first resolution), `GET /orgs/{org_id}/users/llm-quotas` (per-member used/quota + period bounds), and the org users list for the uid→name/email join. No backend changes.
- Follows the app's MVVM contract: `page.tsx` renders purely from a co-located `useUsageViewModel`; new `useCreditsCheckQuery` hook + `types/credits.ts`; `formatCredits` helper; zh catalog entries for all new copy.
- Access control: nav entry is `adminOnly`, and `/usage` is added to `ADMIN_ONLY_PREFIXES` so non-admin members are redirected to `/users`.
- States: per-section loading skeletons, independent stats/members error alerts, and a billing-not-ready notice for orgs without an initialized billing profile (`billing_initialized: false` or backend 503 `billing_not_ready`).

Design spec: `docs/superpowers/specs/2026-08-10-enterprise-admin-org-usage-page-design.md` (included in this PR along with the implementation plan).

## Test plan
- [x] `pnpm exec tsc --noEmit` — clean
- [x] `pnpm run lint` — clean (`--max-warnings=0`)
- [x] `pnpm run test:coverage` — 51 suites, 337 tests pass; new co-located specs cover the credits hook (fetch URL + disabled states), view model (wallet filtering, uid join, sort, quota/unlimited/pct, billing-not-ready, independent errors), page rendering (cards, table, skeletons, notices, alerts), sidebar visibility, and the `/usage` guard redirect
- [ ] Staging smoke after web release: log in as a team-org admin, open **Usage**, verify balance/used figures match `/users/credits` data and the member table matches the Users page quota dialog


---

## feat(settings): add API Keys tab for org service tokens (#3310)

- **SHA**: `7b71f4fcb647505f1ba9e66c46ee72b5d6d3df73`
- **作者**: bill-srp
- **日期**: 2026-08-10T06:06:08Z
- **PR**: #3310

### Commit Message

```
feat(settings): add API Keys tab for org service tokens (#3310)

## Linear
<!-- no Linear issue for this change -->

## Summary
- Add an **API Keys** tab to the webapp settings page (`claw-settings`)
that manages org service tokens through the already-merged
claw-interface management API (`/orgs/{org_id}/service-tokens` create /
list / revoke / rebind, PRs #3272/#3274/#3276/#3284).
- Tab visibility requires BOTH gates: (1) the backend
`require_org_token_admin` mirror — personal-org members (owner) or
team-org admins, from `GET /account/me` (`org.org_type` / `org.role`);
and (2) server-authoritative **agents-v2 eligibility** — `GET
/agents/install-capability` must return `runtime: "engine"` (i.e.
`AGENTS_V2_ENABLED` on AND staging open-rollout or
`AGENTS_V2_EMAIL_ALLOWLIST` match). Capability loading/error states fail
closed; the capability query fires only when the org gate already
passes. New `useAgentInstallCapabilityQuery` hook (5-min staleTime)
added to the `hooks/queries/agents/` factory.
- Flows: create dialog (name, 1–100 chars) → one-time secret reveal
dialog with copy-to-clipboard and a "shown only once" warning; rotate
(`/rebind`) with confirmation → new one-time secret; revoke with
confirmation; loading / error / empty states. Revoked rows expose no
actions.
- Layering follows the repo conventions: `src/models/service-token.ts` →
`src/services/service-tokens.ts` (via the generic `callClawInterfaceAPI`
catch-all — no new BFF route) → `src/hooks/queries/service-tokens/`
(QUERY_VERSION-prefixed, org-scoped keys) → `ApiKeysTab.tsx` +
`useApiKeysController.ts`.
- Security constraint carried over from the backend design review: the
plaintext `zct_` token never passes through `useMutation` / the React
Query cache — create and rotate are direct service calls with the secret
held only in controller-local state and cleared when the reveal dialog
closes. Only revoke (no secret in the response path it consumes) uses
`useMutation`.
- UI uses `@zooclaw/design-system` components (Dialog, AlertDialog,
Alert, Badge, Button, Input, Label) + heroicons; en + zh strings added
(other locales fall back to English).

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, tsc, vitest (8534 passed),
eslint all green
- [x] Unit specs added: service contract
(`service-tokens.unit.spec.ts`), query hook
(`useServiceTokensQuery.unit.spec.ts`), tab flows
(`ApiKeysTab.unit.spec.tsx`: metadata rendering, create validation,
one-time reveal + clear-on-close, copy, rotate confirm, revoke confirm +
list invalidation), and settings tab gating
(`ClawSettingsClient.unit.spec.tsx`)
- [ ] Staging smoke after backend release: create → call `/service/v1`
with the token → rotate (old plaintext 401s) → revoke
```

### PR Body

## Linear
<!-- no Linear issue for this change -->

## Summary
- Add an **API Keys** tab to the webapp settings page (`claw-settings`) that manages org service tokens through the already-merged claw-interface management API (`/orgs/{org_id}/service-tokens` create / list / revoke / rebind, PRs #3272/#3274/#3276/#3284).
- Tab visibility requires BOTH gates: (1) the backend `require_org_token_admin` mirror — personal-org members (owner) or team-org admins, from `GET /account/me` (`org.org_type` / `org.role`); and (2) server-authoritative **agents-v2 eligibility** — `GET /agents/install-capability` must return `runtime: "engine"` (i.e. `AGENTS_V2_ENABLED` on AND staging open-rollout or `AGENTS_V2_EMAIL_ALLOWLIST` match). Capability loading/error states fail closed; the capability query fires only when the org gate already passes. New `useAgentInstallCapabilityQuery` hook (5-min staleTime) added to the `hooks/queries/agents/` factory.
- Flows: create dialog (name, 1–100 chars) → one-time secret reveal dialog with copy-to-clipboard and a "shown only once" warning; rotate (`/rebind`) with confirmation → new one-time secret; revoke with confirmation; loading / error / empty states. Revoked rows expose no actions.
- Layering follows the repo conventions: `src/models/service-token.ts` → `src/services/service-tokens.ts` (via the generic `callClawInterfaceAPI` catch-all — no new BFF route) → `src/hooks/queries/service-tokens/` (QUERY_VERSION-prefixed, org-scoped keys) → `ApiKeysTab.tsx` + `useApiKeysController.ts`.
- Security constraint carried over from the backend design review: the plaintext `zct_` token never passes through `useMutation` / the React Query cache — create and rotate are direct service calls with the secret held only in controller-local state and cleared when the reveal dialog closes. Only revoke (no secret in the response path it consumes) uses `useMutation`.
- UI uses `@zooclaw/design-system` components (Dialog, AlertDialog, Alert, Badge, Button, Input, Label) + heroicons; en + zh strings added (other locales fall back to English).

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, tsc, vitest (8534 passed), eslint all green
- [x] Unit specs added: service contract (`service-tokens.unit.spec.ts`), query hook (`useServiceTokensQuery.unit.spec.ts`), tab flows (`ApiKeysTab.unit.spec.tsx`: metadata rendering, create validation, one-time reveal + clear-on-close, copy, rotate confirm, revoke confirm + list invalidation), and settings tab gating (`ClawSettingsClient.unit.spec.tsx`)
- [ ] Staging smoke after backend release: create → call `/service/v1` with the token → rotate (old plaintext 401s) → revoke


---

## refactor(web): codify page MVVM layer contract and migrate agents-manager family (#3313)

- **SHA**: `ee2d75d973de86ac3c37119ebe4c326e636fc8a1`
- **作者**: bill-srp
- **日期**: 2026-08-10T06:05:54Z
- **PR**: #3313

### Commit Message

```
refactor(web): codify page MVVM layer contract and migrate agents-manager family (#3313)

<!-- PR 标题：type(scope): description -->

## Summary
- **Codify the page MVVM layer contract in `web/app/AGENTS.md`**
(settled with Bill): render-only view with an
ephemeral-presentation-state exception; the view model as a coordinator
only (composes query + flow hooks, mediates in 1–2-line callbacks,
adapts to one grouped return object); one controller hook per user flow
under page `hooks/`, receiving capabilities as function-typed parameters
and never importing `src/services`, `src/hooks/queries`, or sibling flow
hooks; "state lives with its invariants" ownership rule; the open (view)
vs fenced (VM-and-below) review-surface split. Flow-hook extraction
becomes the default for business interaction, with the 600/300 line
gates demoted to backstop.
- **Migrate the whole `agents-manager` family as the exemplar**
(implementation by Codex, independently reviewed + verified):
- **Root page**: `useViewModel.ts` 510 → 232 lines. New `hooks/`
(`useAgentModals` ModalState machine, `useHireFlow`, `useFireFlow`,
`useUpdateFlow`, `usePackPurchase` moved in — its direct
`purchaseAgentPack` service import becomes a capability param) and
`lib/` (`pack-workspace`, `agent-eligibility`, `catalog-rows` pure
functions; `catalog-view` moved in). `AgentsManagerClient.tsx` changes
by exactly one type-import line.
- **`[id]` detail page**: `useViewModel.ts` 396 → 222 lines.
`lib/agent-detail-resolution.ts` (install state, eligibility,
shared/installed fallbacks, `selectInstalledRow`) + `hooks/`
(`useDetailModals`, `useDetailHireFlow`, `useDetailFireFlow`,
`useDetailUpdateFlow`). `AgentDetailClient.tsx` untouched.
- **`publish` page**: through-the-VM retrofit — `useAgentInstallToggle`
/ `useAgentUpdateAction` / `usePackListingActions` no longer import
`@/services/*` or `@/hooks/queries/*` values; each receives one
structured gateway parameter built by the VM (the `openclawKeys`
invalidation is an injected callback). Internal `useMutation` usage
stays; the fence is path-based.
- Behavior is unchanged by design: all three VM return contracts are
byte-identical, and the pre-existing behavioral specs (incl. the
1,499-line root `useViewModel` spec and both `AgentDetailClient` specs)
pass with at most import-path updates and mock-injection changes — no
assertion weakened.
- New focused specs: table-driven eligibility matrices and pure-function
specs for the `lib/` modules; renderHook specs for the modal machines
and every flow hook using plain `vi.fn()` capabilities (no query
wrapper, no service mocks — the testability payoff of the params rule).

**size-override justification**: docs + a 3-page structural refactor
land together so the codified contract and its reference implementation
stay in one reviewable unit; ~2/5 of the diff is new focused test files,
and the largest single source change is a file move
(`usePackPurchase.ts`, 98% similarity).

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, `tsc`, full vitest suite
(8,572 passed), eslint: green (run after each of the two migration
phases)
- [x] `pnpm test:unit:coverage` — ratcheted thresholds pass (statements
88.8 vs 83; agents-manager tree 94–98%)
- [x] grep gate: zero value imports from `@/services` or
`@/hooks/queries` under any `agents-manager/**/hooks/`
- [x] Pre-existing behavioral specs unchanged in substance: root VM spec
(1,499 lines) + `AgentDetailClient` specs pass against the refactored
VMs
- [ ] CI (`web-quality` + `web-build-check`) green
```

### PR Body

<!-- PR 标题：type(scope): description -->

## Summary
- **Codify the page MVVM layer contract in `web/app/AGENTS.md`** (settled with Bill): render-only view with an ephemeral-presentation-state exception; the view model as a coordinator only (composes query + flow hooks, mediates in 1–2-line callbacks, adapts to one grouped return object); one controller hook per user flow under page `hooks/`, receiving capabilities as function-typed parameters and never importing `src/services`, `src/hooks/queries`, or sibling flow hooks; "state lives with its invariants" ownership rule; the open (view) vs fenced (VM-and-below) review-surface split. Flow-hook extraction becomes the default for business interaction, with the 600/300 line gates demoted to backstop.
- **Migrate the whole `agents-manager` family as the exemplar** (implementation by Codex, independently reviewed + verified):
  - **Root page**: `useViewModel.ts` 510 → 232 lines. New `hooks/` (`useAgentModals` ModalState machine, `useHireFlow`, `useFireFlow`, `useUpdateFlow`, `usePackPurchase` moved in — its direct `purchaseAgentPack` service import becomes a capability param) and `lib/` (`pack-workspace`, `agent-eligibility`, `catalog-rows` pure functions; `catalog-view` moved in). `AgentsManagerClient.tsx` changes by exactly one type-import line.
  - **`[id]` detail page**: `useViewModel.ts` 396 → 222 lines. `lib/agent-detail-resolution.ts` (install state, eligibility, shared/installed fallbacks, `selectInstalledRow`) + `hooks/` (`useDetailModals`, `useDetailHireFlow`, `useDetailFireFlow`, `useDetailUpdateFlow`). `AgentDetailClient.tsx` untouched.
  - **`publish` page**: through-the-VM retrofit — `useAgentInstallToggle` / `useAgentUpdateAction` / `usePackListingActions` no longer import `@/services/*` or `@/hooks/queries/*` values; each receives one structured gateway parameter built by the VM (the `openclawKeys` invalidation is an injected callback). Internal `useMutation` usage stays; the fence is path-based.
- Behavior is unchanged by design: all three VM return contracts are byte-identical, and the pre-existing behavioral specs (incl. the 1,499-line root `useViewModel` spec and both `AgentDetailClient` specs) pass with at most import-path updates and mock-injection changes — no assertion weakened.
- New focused specs: table-driven eligibility matrices and pure-function specs for the `lib/` modules; renderHook specs for the modal machines and every flow hook using plain `vi.fn()` capabilities (no query wrapper, no service mocks — the testability payoff of the params rule).

**size-override justification**: docs + a 3-page structural refactor land together so the codified contract and its reference implementation stay in one reviewable unit; ~2/5 of the diff is new focused test files, and the largest single source change is a file move (`usePackPurchase.ts`, 98% similarity).

## Test plan
- [x] `bash scripts/verify-web.sh` — guards, `tsc`, full vitest suite (8,572 passed), eslint: green (run after each of the two migration phases)
- [x] `pnpm test:unit:coverage` — ratcheted thresholds pass (statements 88.8 vs 83; agents-manager tree 94–98%)
- [x] grep gate: zero value imports from `@/services` or `@/hooks/queries` under any `agents-manager/**/hooks/`
- [x] Pre-existing behavioral specs unchanged in substance: root VM spec (1,499 lines) + `AgentDetailClient` specs pass against the refactored VMs
- [ ] CI (`web-quality` + `web-build-check`) green


---

## fix(whatsapp): pin Oura Ring installs to DeepSeek (#3311)

- **SHA**: `ce7e61baf66465bd07e70b89b7f0185935ed0eda`
- **作者**: bill-srp
- **日期**: 2026-08-10T04:24:50Z
- **PR**: #3311

### Commit Message

```
fix(whatsapp): pin Oura Ring installs to DeepSeek (#3311)

## Summary

- pin WhatsApp-provisioned Oura Ring Agents to
`litellm/deepseek-v4-flash-0731`
- pass the channel-specific model through an explicit install context
without changing normal Pack, Main Agent, or Agent Builder installs
- fail closed when the configured override is absent from the Engine
model catalog

## Test plan

- [x] focused unit tests (`126 passed`)
- [x] Ruff check and format check
- [x] import-linter architecture contracts
- [x] targeted Pyright on all changed Python files (`0 errors`)
- [x] Python file-length guard

## Local environment note

The repository-wide Pyright command cannot resolve the local
virtualenv's installed dependencies in this checkout and reports
pre-existing missing-import errors. The targeted Pyright run using
`services/claw-interface/.venv/bin/python` passed for every changed
file; CI remains authoritative for the full check.
```

### PR Body

## Summary

- pin WhatsApp-provisioned Oura Ring Agents to `litellm/deepseek-v4-flash-0731`
- pass the channel-specific model through an explicit install context without changing normal Pack, Main Agent, or Agent Builder installs
- fail closed when the configured override is absent from the Engine model catalog

## Test plan

- [x] focused unit tests (`126 passed`)
- [x] Ruff check and format check
- [x] import-linter architecture contracts
- [x] targeted Pyright on all changed Python files (`0 errors`)
- [x] Python file-length guard

## Local environment note

The repository-wide Pyright command cannot resolve the local virtualenv's installed dependencies in this checkout and reports pre-existing missing-import errors. The targeted Pyright run using `services/claw-interface/.venv/bin/python` passed for every changed file; CI remains authoritative for the full check.


---

## fix(whatsapp): filter engine sentinel acks from WhatsApp outbound delivery (#3309)

- **SHA**: `9f5da286799faf35dba50e8481bf14a1c0bc56ba`
- **作者**: Nemo Feng
- **日期**: 2026-08-10T03:46:05Z
- **PR**: #3309

### Commit Message

```
fix(whatsapp): filter engine sentinel acks from WhatsApp outbound delivery (#3309)

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary
- Skip standalone `NO_REPLY` / `HEARTBEAT_OK` sentinel posts in
Mattermost→WhatsApp outbound delivery, reported as a new
`sentinel_message` result reason. The check runs before the Claw
Interface target resolve, so pure-sentinel posts make zero network
calls.
- Strip a glued trailing sentinel token (`"reply text\nNO_REPLY"`) from
otherwise-real replies before sending to WhatsApp, mirroring the web
client's `stripSentinelTokens`.

## Root cause
The engine's agent policy ends turns with a literal `NO_REPLY` post when
the real reply was already delivered via the message tool (and heartbeat
runs post `HEARTBEAT_OK`). Both existing user-facing surfaces filter
these sentinels — web chat (`web/app/src/lib/chat/message-filters.ts`)
and chat replay
(`services/claw-interface/app/services/chat_replay/visibility.py`) — but
the WhatsApp bridge forwarded every non-empty, non-preview bot post, so
WhatsApp users received a separate "NO_REPLY" message alongside every
agent reply.

Before #3308 the sentinel was buried in streaming-preview fragment
noise; with previews filtered it arrives whole on every turn, which is
the "extra NO_REPLY message" users now see.

The new `SENTINEL_SUFFIX_RE` in `mattermost-outbound.ts` is the same
expression the web client uses, so all three surfaces share one
filtering contract.

## Test plan
- [x] `pnpm typecheck` — clean
- [x] `pnpm test` — 92/92 passing; 5 new cases in
`mattermost-outbound.test.ts`: standalone `NO_REPLY`, whitespace-padded
`NO_REPLY \n`, and standalone `HEARTBEAT_OK` all return
`sentinel_message` with no fetch calls; a trailing glued token is
stripped from the delivered Graph API body; text where the token is not
a trailing suffix is delivered unchanged
- Live dev/staging validation intentionally not run — code-only
verification requested for this change

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary
- Skip standalone `NO_REPLY` / `HEARTBEAT_OK` sentinel posts in Mattermost→WhatsApp outbound delivery, reported as a new `sentinel_message` result reason. The check runs before the Claw Interface target resolve, so pure-sentinel posts make zero network calls.
- Strip a glued trailing sentinel token (`"reply text\nNO_REPLY"`) from otherwise-real replies before sending to WhatsApp, mirroring the web client's `stripSentinelTokens`.

## Root cause
The engine's agent policy ends turns with a literal `NO_REPLY` post when the real reply was already delivered via the message tool (and heartbeat runs post `HEARTBEAT_OK`). Both existing user-facing surfaces filter these sentinels — web chat (`web/app/src/lib/chat/message-filters.ts`) and chat replay (`services/claw-interface/app/services/chat_replay/visibility.py`) — but the WhatsApp bridge forwarded every non-empty, non-preview bot post, so WhatsApp users received a separate "NO_REPLY" message alongside every agent reply.

Before #3308 the sentinel was buried in streaming-preview fragment noise; with previews filtered it arrives whole on every turn, which is the "extra NO_REPLY message" users now see.

The new `SENTINEL_SUFFIX_RE` in `mattermost-outbound.ts` is the same expression the web client uses, so all three surfaces share one filtering contract.

## Test plan
- [x] `pnpm typecheck` — clean
- [x] `pnpm test` — 92/92 passing; 5 new cases in `mattermost-outbound.test.ts`: standalone `NO_REPLY`, whitespace-padded `NO_REPLY \n`, and standalone `HEARTBEAT_OK` all return `sentinel_message` with no fetch calls; a trailing glued token is stripped from the delivered Graph API body; text where the token is not a trailing suffix is delivered unchanged
- Live dev/staging validation intentionally not run — code-only verification requested for this change

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(whatsapp): deliver only final agent replies and show typing indicator (#3308)

- **SHA**: `0901f9eca0363da1e66e0672790a6066a41f868a`
- **作者**: Nemo Feng
- **日期**: 2026-08-10T02:47:09Z
- **PR**: #3308

### Commit Message

```
fix(whatsapp): deliver only final agent replies and show typing indicator (#3308)

## Summary
- Skip the engine's streaming **preview** posts in Mattermost→WhatsApp
outbound delivery, so WhatsApp users receive only final reply posts
instead of a truncated first fragment ("N", "Your", …).
- Send Meta's official [typing
indicator](https://developers.facebook.com/docs/whatsapp/cloud-api/typing-indicators/)
(which also marks the inbound message read) once an inbound message is
committed to Mattermost on the routable path, so the user sees "typing…"
while the agent generates instead of dead air.

## Root cause
The engine streams each reply into Mattermost via the Engine v2
preview-post protocol: a `posted` event creates a nearly-empty preview
post (measured first frame: 1 char; props `openclaw_streaming: "true"` /
`openclaw_stream_state: "preview"`), ~50 `post_edited` events grow it in
place (~74 chars / 1.24 s), then the final full message arrives as new
`posted` post(s) and the preview is deleted (protocol measured in
`docs/superpowers/specs/2026-07-21-chat-streaming-smoothness.md`).

The bridge (`src/mattermost-outbound.ts`) forwards every non-inbound
`posted` event and ignores `post_edited`/`post_deleted` — so WhatsApp
received the preview's first frame as a permanent message (WhatsApp
messages cannot be edited). When the user replied mid-stream the turn
aborted, the final post never arrived, and the fragment was all they
ever got.

The new filter mirrors the two existing consumers of the same contract:
claw-interface `_is_preview_post`
(`app/services/agent_builder_service.py:1628`) and the web client's
`isStreamingPreview` (`src/hooks/chat/useMmTypewriter.ts:91`). Comparing
**values** (not prop presence) is load-bearing: final posts carry the
same prop names with values `"false"` / `"final"` (v2 staging capture:
`docs/staging-validation/2026-07-31-v2-main-agent-model-and-stream-error-report.md`).

## Test plan
- [x] `pnpm typecheck` clean in `services/whatsapp-business-service`
- [x] `pnpm test` clean — 87/87 across 6 files (11 new tests)
- [x] `pnpm build` clean
- New unit coverage:
- preview post via `openclaw_streaming: "true"` → skipped (reason
`streaming_preview`), no resolve/send
  - preview post via `openclaw_stream_state: "preview"` → skipped
- regression guard: final post with `{openclaw_streaming: "false",
openclaw_stream_state: "final"}` → delivered
- typing indicator request shape (`status: "read"` + inbound
`message_id` + `typing_indicator: {type: "text"}`) on the routable path
- typing-indicator failure does not affect the webhook response; no
indicator on canned-reply paths
- Staging: send a WhatsApp message to the oura_ring number; verify the
reply arrives once, complete, with a typing indicator while generating.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Summary
- Skip the engine's streaming **preview** posts in Mattermost→WhatsApp outbound delivery, so WhatsApp users receive only final reply posts instead of a truncated first fragment ("N", "Your", …).
- Send Meta's official [typing indicator](https://developers.facebook.com/docs/whatsapp/cloud-api/typing-indicators/) (which also marks the inbound message read) once an inbound message is committed to Mattermost on the routable path, so the user sees "typing…" while the agent generates instead of dead air.

## Root cause
The engine streams each reply into Mattermost via the Engine v2 preview-post protocol: a `posted` event creates a nearly-empty preview post (measured first frame: 1 char; props `openclaw_streaming: "true"` / `openclaw_stream_state: "preview"`), ~50 `post_edited` events grow it in place (~74 chars / 1.24 s), then the final full message arrives as new `posted` post(s) and the preview is deleted (protocol measured in `docs/superpowers/specs/2026-07-21-chat-streaming-smoothness.md`).

The bridge (`src/mattermost-outbound.ts`) forwards every non-inbound `posted` event and ignores `post_edited`/`post_deleted` — so WhatsApp received the preview's first frame as a permanent message (WhatsApp messages cannot be edited). When the user replied mid-stream the turn aborted, the final post never arrived, and the fragment was all they ever got.

The new filter mirrors the two existing consumers of the same contract: claw-interface `_is_preview_post` (`app/services/agent_builder_service.py:1628`) and the web client's `isStreamingPreview` (`src/hooks/chat/useMmTypewriter.ts:91`). Comparing **values** (not prop presence) is load-bearing: final posts carry the same prop names with values `"false"` / `"final"` (v2 staging capture: `docs/staging-validation/2026-07-31-v2-main-agent-model-and-stream-error-report.md`).

## Test plan
- [x] `pnpm typecheck` clean in `services/whatsapp-business-service`
- [x] `pnpm test` clean — 87/87 across 6 files (11 new tests)
- [x] `pnpm build` clean
- New unit coverage:
  - preview post via `openclaw_streaming: "true"` → skipped (reason `streaming_preview`), no resolve/send
  - preview post via `openclaw_stream_state: "preview"` → skipped
  - regression guard: final post with `{openclaw_streaming: "false", openclaw_stream_state: "final"}` → delivered
  - typing indicator request shape (`status: "read"` + inbound `message_id` + `typing_indicator: {type: "text"}`) on the routable path
  - typing-indicator failure does not affect the webhook response; no indicator on canned-reply paths
- Staging: send a WhatsApp message to the oura_ring number; verify the reply arrives once, complete, with a typing indicator while generating.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(agent-builder): integrate home chat and publishing flows (#3299)

- **SHA**: `152529cb255da9522990eb484058e112bd86bae2`
- **作者**: lynn Zhuang
- **日期**: 2026-08-10T02:41:11Z
- **PR**: #3299

### Commit Message

```
feat(agent-builder): integrate home chat and publishing flows (#3299)

## Linear

N/A

## Summary

- Replace the legacy Agent Builder screens with the latest chat-first
home, creation, Builder, Preview, and Publish UI while keeping Agent
Builder V1 and V2 fully decoupled behind their own adapters.
- Complete the new Publish orchestration: Publish now covers the former
Accept Test and Submit workflow, updates an already installed V1 or V2
agent to the newly published version, and supports Only me, private
link, and Marketplace destinations.
- Restore generic chat composer Skill and Connector behavior instead of
introducing Agent Builder project-level bindings; keep Agent settings,
User feedback, and Analysis disabled until their new-UI workflows are
defined.
- Harden long-running Builder flows: retain publish selection during
polling, keep active V2 workspaces visible across lease renewal, release
acquired leases during cleanup, recover interrupted project
initialization without duplicate posts, and make Preview feedback retry
finite and recoverable.
- Align user-facing copy and actions with the new UI by removing
obsolete Accept Test, Cancel Test, Submit, and Review affordances while
preserving the backend Accept/Submit APIs used internally by Publish.

## Test plan

- [x] `bash scripts/verify-local.sh --changed` — frontend
TypeScript/ESLint and backend Ruff/Pyright/import-linter passed.
- [x] Agent Builder frontend unit suite — 33 files, 341 tests passed.
- [x] Web CI lint orchestrator (`pnpm run lint:ci`) passed, including
dependency boundaries and the Knip dead-code hard gate.
- [x] Agent Builder backend route/service unit suite — 203 tests passed
with V2 disabled for the V1 contract run.
- [x] `git diff --check` passed.
- [x] Local staging-backed smoke: Agent Builder route returned 200, V2
lease/activate calls returned 200, and the page rendered without console
errors.
- [x] GitHub CI validates the PR merge result against current `main` —
Code Quality, CodeQL, build, frontend/backend tests, and automated
review passed.

## Notes

- V1 and V2 remain separate runtime implementations. V1 is retained only
for the migration window and can be removed independently when it is
retired.
- `.external-worktrees/` is local-only and intentionally excluded from
the PR.

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
Co-authored-by: kaka-srp <kaka@srp.one>
```

### PR Body

## Linear

N/A

## Summary

- Replace the legacy Agent Builder screens with the latest chat-first home, creation, Builder, Preview, and Publish UI while keeping Agent Builder V1 and V2 fully decoupled behind their own adapters.
- Complete the new Publish orchestration: Publish now covers the former Accept Test and Submit workflow, updates an already installed V1 or V2 agent to the newly published version, and supports Only me, private link, and Marketplace destinations.
- Restore generic chat composer Skill and Connector behavior instead of introducing Agent Builder project-level bindings; keep Agent settings, User feedback, and Analysis disabled until their new-UI workflows are defined.
- Harden long-running Builder flows: retain publish selection during polling, keep active V2 workspaces visible across lease renewal, release acquired leases during cleanup, recover interrupted project initialization without duplicate posts, and make Preview feedback retry finite and recoverable.
- Align user-facing copy and actions with the new UI by removing obsolete Accept Test, Cancel Test, Submit, and Review affordances while preserving the backend Accept/Submit APIs used internally by Publish.

## Test plan

- [x] `bash scripts/verify-local.sh --changed` — frontend TypeScript/ESLint and backend Ruff/Pyright/import-linter passed.
- [x] Agent Builder frontend unit suite — 33 files, 341 tests passed.
- [x] Web CI lint orchestrator (`pnpm run lint:ci`) passed, including dependency boundaries and the Knip dead-code hard gate.
- [x] Agent Builder backend route/service unit suite — 203 tests passed with V2 disabled for the V1 contract run.
- [x] `git diff --check` passed.
- [x] Local staging-backed smoke: Agent Builder route returned 200, V2 lease/activate calls returned 200, and the page rendered without console errors.
- [x] GitHub CI validates the PR merge result against current `main` — Code Quality, CodeQL, build, frontend/backend tests, and automated review passed.

## Notes

- V1 and V2 remain separate runtime implementations. V1 is retained only for the migration window and can be removed independently when it is retired.
- `.external-worktrees/` is local-only and intentionally excluded from the PR.


---
