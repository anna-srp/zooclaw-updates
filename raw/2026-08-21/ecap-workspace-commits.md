# SerendipityOneInc/ecap-workspace — commits 2026-08-21

## fix(chat): localize composer add menu (#3473)

- **SHA**: `2a2a970a96a89c639ee2dbe4415a0938f33b0d30`
- **作者**: rayrain-srp
- **日期**: 2026-08-21T12:29:06Z
- **PR**: #3473

### Commit Message

```
fix(chat): localize composer add menu (#3473)

## Summary

- Localize the Composer Add trigger and its Recent, Skills, Skill Store,
and Asset Library flows in English and Simplified Chinese.
- Keep shared `@zooclaw/chat-ui` components presentational by passing
localized labels from the app.
- Preserve English fallback for every other locale through the existing
deep-merge dictionary behavior; no other locale files are changed.
- Linear:
https://linear.app/srpone/issue/ECA-1389/chat-i18n-localize-add-menu-tooltip-and-attachment-menu-copy

## Root cause

The unified Composer Add menu and its nested attachment surfaces
contained hard-coded English strings, including the trigger tooltip/ARIA
label and loading, error, empty, and action copy. Shared chat UI
components also owned user-facing defaults, so the app locale could not
translate those states consistently in either v1 or v2.

## Test plan

- [x] App unit tests: 11 files / 94 tests covering English, Chinese,
menu states, localized prompt insertion, and non-English fallback.
- [x] Agent Builder integration regressions: 2 files / 73 tests covering
Composer usage from the creation flow.
- [x] Shared chat-ui unit tests: 2 files / 20 tests covering the
localized label contracts and loading/error/empty states.
- [x] `pnpm tsc` and targeted ESLint for `@zooclaw/chat-ui`.
- [x] `bash scripts/verify-web.sh --no-test` for the changed app surface
(governance guards, full app TypeScript, ESLint).
- [x] Pre-push changed-surface verification.
```

### PR Body

## Summary

- Localize the Composer Add trigger and its Recent, Skills, Skill Store, and Asset Library flows in English and Simplified Chinese.
- Keep shared `@zooclaw/chat-ui` components presentational by passing localized labels from the app.
- Preserve English fallback for every other locale through the existing deep-merge dictionary behavior; no other locale files are changed.
- Linear: https://linear.app/srpone/issue/ECA-1389/chat-i18n-localize-add-menu-tooltip-and-attachment-menu-copy

## Root cause

The unified Composer Add menu and its nested attachment surfaces contained hard-coded English strings, including the trigger tooltip/ARIA label and loading, error, empty, and action copy. Shared chat UI components also owned user-facing defaults, so the app locale could not translate those states consistently in either v1 or v2.

## Test plan

- [x] App unit tests: 11 files / 94 tests covering English, Chinese, menu states, localized prompt insertion, and non-English fallback.
- [x] Agent Builder integration regressions: 2 files / 73 tests covering Composer usage from the creation flow.
- [x] Shared chat-ui unit tests: 2 files / 20 tests covering the localized label contracts and loading/error/empty states.
- [x] `pnpm tsc` and targeted ESLint for `@zooclaw/chat-ui`.
- [x] `bash scripts/verify-web.sh --no-test` for the changed app surface (governance guards, full app TypeScript, ESLint).
- [x] Pre-push changed-surface verification.


---

## fix(chat): replace stale disconnected composer copy (#3472)

- **SHA**: `8de1900f5ae29c20160f5d43fcccb9ef8ee833a9`
- **作者**: rayrain-srp
- **日期**: 2026-08-21T12:07:11Z
- **PR**: #3472

### Commit Message

```
fix(chat): replace stale disconnected composer copy (#3472)

## Summary
- Replace `genClaw.inputDisabled` in all 10 supported locales with
connection-neutral copy that does not mention the stale Claw runtime
term or imply a manual connection step.
- Add regression coverage for both connecting/disconnected composer
states and for the exact copy in every supported locale.
- Linear:
https://linear.app/srpone/issue/ECA-1390/chat-copy-replace-stale-claw-wording-in-disconnected-composer

## Root cause
The shared v1/v2 `GenClawInput` composer still used legacy locale
strings that told users to connect to “Claw.” During automatic startup
or reconnect, that wording was both inconsistent with the current Agent
terminology and incorrectly suggested that users needed to take action.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/app/chat/GenClawInput.unit.spec.tsx
tests/unit/locales/index.unit.spec.ts` (118 tests)
- [x] `bash scripts/verify-web.sh --no-test <changed files>` (governance
guards, TypeScript, ESLint)
- [x] Pre-commit frontend lint
- [x] Pre-push PR size and changed-surface verification
```

### PR Body

## Summary
- Replace `genClaw.inputDisabled` in all 10 supported locales with connection-neutral copy that does not mention the stale Claw runtime term or imply a manual connection step.
- Add regression coverage for both connecting/disconnected composer states and for the exact copy in every supported locale.
- Linear: https://linear.app/srpone/issue/ECA-1390/chat-copy-replace-stale-claw-wording-in-disconnected-composer

## Root cause
The shared v1/v2 `GenClawInput` composer still used legacy locale strings that told users to connect to “Claw.” During automatic startup or reconnect, that wording was both inconsistent with the current Agent terminology and incorrectly suggested that users needed to take action.

## Test plan
- [x] `pnpm exec vitest run tests/unit/app/chat/GenClawInput.unit.spec.tsx tests/unit/locales/index.unit.spec.ts` (118 tests)
- [x] `bash scripts/verify-web.sh --no-test <changed files>` (governance guards, TypeScript, ESLint)
- [x] Pre-commit frontend lint
- [x] Pre-push PR size and changed-surface verification


---

## refactor(billing): migrate card cleanup index name (#3487)

- **SHA**: `554d10fc4b96a83197425fc13b1c496f64fe2284`
- **作者**: tim-srp
- **日期**: 2026-08-21T11:44:10Z
- **PR**: #3487

### Commit Message

```
refactor(billing): migrate card cleanup index name (#3487)

## Summary
- rename the subscription-agreement cleanup index from
`subscription_creem_replacement_cleanup` to
`subscription_card_replacement_cleanup`
- add a guarded migration helper that validates the legacy index
specification before replacing it
- update index validation and rollout documentation for the
provider-neutral name
- leave the subscription-agreement collection name and all index
keys/options unchanged

## Deployment
- Before deploying the application, run `python -m
scripts.ensure_billing_v2_indexes` during a controlled billing-write
window.
- MongoDB cannot rename an index or keep identical key specifications
under two names, so the command validates and drops the legacy index
before immediately recreating it under the new name.
- The migration is retryable if index creation is interrupted.

## Test plan
- [x] Billing v2 repository suite: 86 passed
- [x] `bash scripts/verify-py.sh`
- [x] pre-commit and pre-push changed-surface gates
- [x] `git diff --check`

## Risk
- No collection rename, document migration, query change, or application
API behavior change.
- The controlled migration has a short interval without this non-unique
lookup index; billing writes should be controlled as documented.
```

### PR Body

## Summary
- rename the subscription-agreement cleanup index from `subscription_creem_replacement_cleanup` to `subscription_card_replacement_cleanup`
- add a guarded migration helper that validates the legacy index specification before replacing it
- update index validation and rollout documentation for the provider-neutral name
- leave the subscription-agreement collection name and all index keys/options unchanged

## Deployment
- Before deploying the application, run `python -m scripts.ensure_billing_v2_indexes` during a controlled billing-write window.
- MongoDB cannot rename an index or keep identical key specifications under two names, so the command validates and drops the legacy index before immediately recreating it under the new name.
- The migration is retryable if index creation is interrupted.

## Test plan
- [x] Billing v2 repository suite: 86 passed
- [x] `bash scripts/verify-py.sh`
- [x] pre-commit and pre-push changed-surface gates
- [x] `git diff --check`

## Risk
- No collection rename, document migration, query change, or application API behavior change.
- The controlled migration has a short interval without this non-unique lookup index; billing writes should be controlled as documented.


---

## chore(billing): clean retired Creem references (#3486)

- **SHA**: `bbe06633d85b0b7c1699de55284d31f7ba1c5fe1`
- **作者**: tim-srp
- **日期**: 2026-08-21T11:23:43Z
- **PR**: #3486

### Commit Message

```
chore(billing): clean retired Creem references (#3486)

## Summary
- replace retired Creem-specific wording and URLs in active Card
checkout tests with provider-neutral fixtures
- update enterprise-admin auth test descriptions to match the public
Card contract
- remove the deleted Creem index validation command and stale Creem
manual-review cron documentation
- retain the explicit retired webhook 404 tests

## Test plan
- [x] `bash scripts/verify-web.sh
tests/unit/components/PaywallContent.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
tests/unit/app/subscription/SuccessClient.unit.spec.tsx`
- [x] enterprise-admin focused Vitest: 28 passed
- [x] enterprise-admin focused ESLint
- [x] pre-commit and pre-push changed-surface gates
- [x] `git diff --check`

## Risk
- Tests and documentation only; no production runtime behavior changes.
```

### PR Body

## Summary
- replace retired Creem-specific wording and URLs in active Card checkout tests with provider-neutral fixtures
- update enterprise-admin auth test descriptions to match the public Card contract
- remove the deleted Creem index validation command and stale Creem manual-review cron documentation
- retain the explicit retired webhook 404 tests

## Test plan
- [x] `bash scripts/verify-web.sh tests/unit/components/PaywallContent.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx tests/unit/app/subscription/SuccessClient.unit.spec.tsx`
- [x] enterprise-admin focused Vitest: 28 passed
- [x] enterprise-admin focused ESLint
- [x] pre-commit and pre-push changed-surface gates
- [x] `git diff --check`

## Risk
- Tests and documentation only; no production runtime behavior changes.


---

## refactor(billing): remove Creem provider compatibility (#3485)

- **SHA**: `965d484b6f87da3d5e91f4479d9659fea0e7d326`
- **作者**: tim-srp
- **日期**: 2026-08-21T11:12:49Z
- **PR**: #3485

### Commit Message

```
refactor(billing): remove Creem provider compatibility (#3485)

## Summary
- remove Creem from the persisted billing provider enum and active
card-provider sets
- delete Creem-only reconciliation queries, leases, projections, and
compatibility tests
- rename the remaining shared checkout lookup to a provider-neutral name
while preserving Airwallex behavior
- retain the existing Mongo physical index name until a dedicated index
migration

## Test plan
- [x] focused Billing v2 and Airwallex regression suite: 509 passed
- [x] `bash scripts/verify-py.sh`
- [x] pre-commit and pre-push quality gates
- [x] `git diff --check`

## Risk
- Backend-only cleanup. Current Stripe, Antom, Apple, offline, and
Airwallex provider paths remain supported.
- The retired web webhook path is unchanged and continues to reach
Next.js 404 handling.
```

### PR Body

## Summary
- remove Creem from the persisted billing provider enum and active card-provider sets
- delete Creem-only reconciliation queries, leases, projections, and compatibility tests
- rename the remaining shared checkout lookup to a provider-neutral name while preserving Airwallex behavior
- retain the existing Mongo physical index name until a dedicated index migration

## Test plan
- [x] focused Billing v2 and Airwallex regression suite: 509 passed
- [x] `bash scripts/verify-py.sh`
- [x] pre-commit and pre-push quality gates
- [x] `git diff --check`

## Risk
- Backend-only cleanup. Current Stripe, Antom, Apple, offline, and Airwallex provider paths remain supported.
- The retired web webhook path is unchanged and continues to reach Next.js 404 handling.


---

## refactor(billing): remove Creem-only persistence (#3481)

- **SHA**: `255244caca782924c55e52ddf245284deede9c6b`
- **作者**: tim-srp
- **日期**: 2026-08-21T10:43:31Z
- **PR**: #3481

### Commit Message

```
refactor(billing): remove Creem-only persistence (#3481)

## Summary

- remove Creem-only first-payment and manual-review persistence helpers
- remove the retired Creem card index validation script
- migrate still-relevant renewal, settlement, trial projection, and
Airwallex binding tests to provider-neutral files
- keep Airwallex repositories, shared indexes, and historical provider
compatibility unchanged

## Verification

- `197 passed` across Airwallex first-payment, reconciliation, trial,
enterprise subscription, shared repo, and card checkout tests
- `13 passed` for migrated provider-neutral persistence and retirement
contracts
- `bash scripts/verify-py.sh`
- `bash scripts/verify-py.sh --full`: all static, architecture, and
duplication checks passed; local pytest later hit a native
PyMongo/Miniconda segmentation fault at 3%, so GitHub Actions remains
the authoritative full-suite run

## Risk

Low. Removed functions and modules had no production callers.
Airwallex-active provider-neutral persistence paths and indexes are
retained.
```

### PR Body

## Summary

- remove Creem-only first-payment and manual-review persistence helpers
- remove the retired Creem card index validation script
- migrate still-relevant renewal, settlement, trial projection, and Airwallex binding tests to provider-neutral files
- keep Airwallex repositories, shared indexes, and historical provider compatibility unchanged

## Verification

- `197 passed` across Airwallex first-payment, reconciliation, trial, enterprise subscription, shared repo, and card checkout tests
- `13 passed` for migrated provider-neutral persistence and retirement contracts
- `bash scripts/verify-py.sh`
- `bash scripts/verify-py.sh --full`: all static, architecture, and duplication checks passed; local pytest later hit a native PyMongo/Miniconda segmentation fault at 3%, so GitHub Actions remains the authoritative full-suite run

## Risk

Low. Removed functions and modules had no production callers. Airwallex-active provider-neutral persistence paths and indexes are retained.


---

## fix(org): harden personal org upgrade-to-team preconditions (#3410)

- **SHA**: `c1f3eae3302a460b5e24cc9546b6c5e714c47945`
- **作者**: bill-srp
- **日期**: 2026-08-21T10:21:40Z
- **PR**: #3410

### Commit Message

```
fix(org): harden personal org upgrade-to-team preconditions (#3410)

# What

Backend-only hardening for `POST
/internal/orgs/{org_id}/upgrade-to-team`, closing four gaps a logic
review found by comparing the upgrade against the enterprise invite
handoff (which already solves each of them). Spec:
`docs/superpowers/specs/2026-07-23-org-upgrade-to-team-design.md`,
section "Hardening follow-up (2026-08-14, Bill: backend-only,
hard-block)".

`upgrade_org_to_team` now runs, in order:

1. **Owner-membership guard** — the org owner (`created_by`) must hold
an *active* membership in the org, else 409
`org.upgrade.owner_not_active_member`. Without this, upgrading an
orphaned personal org (owner already handed off to an enterprise) would
rebind the owner's live billing key back to the old personal team.
2. **Personal-subscription hard-block** — new read-only helper
`list_blocking_personal_agreement_providers` (shares the handoff's
`_is_canceling` predicate); any renewable personal agreement → 409
`org.upgrade.personal_subscription_active` with providers in context.
Business mode bills usage to the team customer while personal
fulfillment credits the uid customer, so upgrading with a renewing
personal subscription strands paid credits. Already-canceling agreements
do not block (handoff semantics).
3. **Transition lease** — claims the same `billing_transition` lease the
handoff uses (`org_upgrade:{uuid}`, 300s; 409
`org.join.transition_in_progress` when held; released in `finally`),
making upgrade and an in-flight enterprise handoff mutually exclusive on
the owner's membership row. Owner membership is re-checked under the
lease.
4. **Verified key bind** — the bare `add_user_to_personal_team` call is
replaced with the handoff's `bind_and_verify_key` (bind + canonical
readback assertion), so a partial business-mode flip aborts before the
CAS commit instead of going undetected.

No console changes (Bill's call): the dashboard-console dialog already
renders 409 details generically. The operational sequence is: cancel
owner's personal subscription → upgrade → purchase enterprise plan →
invite members.

# Why

The invite handoff cancels personal subscriptions, leases the
transition, and verifies key readback precisely because flipping billing
to business mode is destructive when interleaved or half-applied. The
upgrade flips the same switch and had none of those guards.

# Test plan

- [x] Unit (`test_org_service.py`, 9 new): inactive/missing owner
membership → 409 before billing; active personal subscription → 409 with
provider context before billing; already-canceling agreement does not
block; lease held → 409; lease released on success and on billing
failure; owner membership re-checked after claim; readback mismatch
aborts before CAS; retry after partial bind failure completes
- [x] Unit (`test_personal_subscription_stop.py`): new helper shares the
handoff canceling predicate
- [x] BDD (`org_lifecycle.feature`, real mongo): upgrade blocked while
the owner has an active personal subscription; existing upgrade
scenarios unchanged
- [x] `bash scripts/verify-py.sh` green (ruff, ruff-format, pyright,
import-linter)
- [x] 170 unit tests across all org/handoff-adjacent suites + 5 BDD
scenarios pass locally after rebasing onto #3407 (which reworked
`personal_subscription_stop.py`; merge verified semantically clean —
`_is_canceling` unchanged)
- Full whole-app coverage gate left to CI (`claw-interface-quality`)
```

### PR Body

# What

Backend-only hardening for `POST /internal/orgs/{org_id}/upgrade-to-team`, closing four gaps a logic review found by comparing the upgrade against the enterprise invite handoff (which already solves each of them). Spec: `docs/superpowers/specs/2026-07-23-org-upgrade-to-team-design.md`, section "Hardening follow-up (2026-08-14, Bill: backend-only, hard-block)".

`upgrade_org_to_team` now runs, in order:

1. **Owner-membership guard** — the org owner (`created_by`) must hold an *active* membership in the org, else 409 `org.upgrade.owner_not_active_member`. Without this, upgrading an orphaned personal org (owner already handed off to an enterprise) would rebind the owner's live billing key back to the old personal team.
2. **Personal-subscription hard-block** — new read-only helper `list_blocking_personal_agreement_providers` (shares the handoff's `_is_canceling` predicate); any renewable personal agreement → 409 `org.upgrade.personal_subscription_active` with providers in context. Business mode bills usage to the team customer while personal fulfillment credits the uid customer, so upgrading with a renewing personal subscription strands paid credits. Already-canceling agreements do not block (handoff semantics).
3. **Transition lease** — claims the same `billing_transition` lease the handoff uses (`org_upgrade:{uuid}`, 300s; 409 `org.join.transition_in_progress` when held; released in `finally`), making upgrade and an in-flight enterprise handoff mutually exclusive on the owner's membership row. Owner membership is re-checked under the lease.
4. **Verified key bind** — the bare `add_user_to_personal_team` call is replaced with the handoff's `bind_and_verify_key` (bind + canonical readback assertion), so a partial business-mode flip aborts before the CAS commit instead of going undetected.

No console changes (Bill's call): the dashboard-console dialog already renders 409 details generically. The operational sequence is: cancel owner's personal subscription → upgrade → purchase enterprise plan → invite members.

# Why

The invite handoff cancels personal subscriptions, leases the transition, and verifies key readback precisely because flipping billing to business mode is destructive when interleaved or half-applied. The upgrade flips the same switch and had none of those guards.

# Test plan

- [x] Unit (`test_org_service.py`, 9 new): inactive/missing owner membership → 409 before billing; active personal subscription → 409 with provider context before billing; already-canceling agreement does not block; lease held → 409; lease released on success and on billing failure; owner membership re-checked after claim; readback mismatch aborts before CAS; retry after partial bind failure completes
- [x] Unit (`test_personal_subscription_stop.py`): new helper shares the handoff canceling predicate
- [x] BDD (`org_lifecycle.feature`, real mongo): upgrade blocked while the owner has an active personal subscription; existing upgrade scenarios unchanged
- [x] `bash scripts/verify-py.sh` green (ruff, ruff-format, pyright, import-linter)
- [x] 170 unit tests across all org/handoff-adjacent suites + 5 BDD scenarios pass locally after rebasing onto #3407 (which reworked `personal_subscription_stop.py`; merge verified semantically clean — `_is_canceling` unchanged)
- Full whole-app coverage gate left to CI (`claw-interface-quality`)


---

## refactor(billing): remove Creem API configuration (#3478)

- **SHA**: `2e7cc313bc9ce9e260b96779d5d995bc94e41537`
- **作者**: tim-srp
- **日期**: 2026-08-21T09:58:52Z
- **PR**: #3478

### Commit Message

```
refactor(billing): remove Creem API configuration (#3478)

## Summary

- delete the retired Creem API client, catalog, config, and provider
schemas
- remove all `CREEM_*` fields/constants from `AppSettings` and
`.env.example`
- replace obsolete Creem fixtures in active Card tests with Airwallex
equivalents
- archive the old staging rollout instructions and document safe Vault
cleanup sequencing
- preserve Creem database literals, queries, indexes, and historical
projections for the next PR

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 182 focused Settings, Card checkout, and Airwallex
config/client/catalog tests
- [x] TDD RED confirmed the provider modules remained importable,
Settings still declared Creem fields, and `.env.example` still
advertised them
- [x] retirement contract validates real environment-variable loading
and confirms stale Vault values are ignored

## Deployment

- Deploy code before removing Vault values. Existing `CREEM_*` values
are unknown environment inputs and are ignored by the new `AppSettings`
model.
- Remove the retired Vault values and roll the deployment only after the
new revision is stable.
```

### PR Body

## Summary

- delete the retired Creem API client, catalog, config, and provider schemas
- remove all `CREEM_*` fields/constants from `AppSettings` and `.env.example`
- replace obsolete Creem fixtures in active Card tests with Airwallex equivalents
- archive the old staging rollout instructions and document safe Vault cleanup sequencing
- preserve Creem database literals, queries, indexes, and historical projections for the next PR

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 182 focused Settings, Card checkout, and Airwallex config/client/catalog tests
- [x] TDD RED confirmed the provider modules remained importable, Settings still declared Creem fields, and `.env.example` still advertised them
- [x] retirement contract validates real environment-variable loading and confirms stale Vault values are ignored

## Deployment

- Deploy code before removing Vault values. Existing `CREEM_*` values are unknown environment inputs and are ignored by the new `AppSettings` model.
- Remove the retired Vault values and roll the deployment only after the new revision is stable.


---

## refactor(billing): neutralize card replacement helpers (#3477)

- **SHA**: `2c83789c0bcdfbc45509f17bbb361a25b8ff5dfa`
- **作者**: tim-srp
- **日期**: 2026-08-21T09:33:29Z
- **PR**: #3477

### Commit Message

```
refactor(billing): neutralize card replacement helpers (#3477)

## Summary

- move Card replacement admission and cleanup helpers out of
`app.services.creem`
- restrict replacement catalog, identity, URL replay, and intent
creation to Airwallex
- rename shared errors from `billing.creem.replacement_*` to
`billing.card.replacement_*`
- add a naming/import contract that prevents active Card modules from
depending on Creem services

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 168 focused Airwallex/Card checkout tests
- [x] dead-function detection via `scripts/ci-lint/07-dead-code.sh`
- [x] TDD RED confirmed missing neutral modules, Creem imports, and old
error codes before implementation

## Risk

- Airwallex replacement behavior remains unchanged and is covered
through checkout creation, replay, first payment, paid handoff,
cancellation, and cleanup.
- Legacy Creem agreements continue to fail closed before Airwallex
provider I/O.
```

### PR Body

## Summary

- move Card replacement admission and cleanup helpers out of `app.services.creem`
- restrict replacement catalog, identity, URL replay, and intent creation to Airwallex
- rename shared errors from `billing.creem.replacement_*` to `billing.card.replacement_*`
- add a naming/import contract that prevents active Card modules from depending on Creem services

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 168 focused Airwallex/Card checkout tests
- [x] dead-function detection via `scripts/ci-lint/07-dead-code.sh`
- [x] TDD RED confirmed missing neutral modules, Creem imports, and old error codes before implementation

## Risk

- Airwallex replacement behavior remains unchanged and is covered through checkout creation, replay, first payment, paid handoff, cancellation, and cleanup.
- Legacy Creem agreements continue to fail closed before Airwallex provider I/O.


---

## refactor(billing): remove Creem subscription runtime (#3475)

- **SHA**: `1956caaee647fcdcdc1ca9dbb968ac81acd7e425`
- **作者**: tim-srp
- **日期**: 2026-08-21T09:10:50Z
- **PR**: #3475

### Commit Message

```
refactor(billing): remove Creem subscription runtime (#3475)

## Summary

- remove the remaining Creem standard-subscription runtime:
reconciliation, first payment, renewal, trials, subscription changes,
and replacement settlement
- remove Creem dispatches from subscription routes, enterprise-join
cancellation, hourly maintenance, billing summaries, and manual-review
monitoring
- delete the corresponding Creem-only tests while retaining Airwallex
and provider-neutral billing coverage
- document that standard Card lifecycle validation now runs through
Airwallex

## Impact

- Current Card checkout, first payment, renewal, reconciliation, cancel,
renew, and downgrade behavior remains owned by Airwallex.
- Stripe, Antom, Apple, and enterprise subscription paths remain
unchanged.
- Historical `provider=creem` literals and read adapters remain for
archival compatibility.
- Six Creem-named helpers are intentionally retained because
Airwallex/shared checkout still imports them; neutralizing those
dependencies is the next cleanup PR.
- There are no real Creem users or pending Creem lifecycle state to
preserve.

## Validation

- `bash scripts/verify-py.sh`
- focused backend regression: 200 passed
- pre-commit and pre-push changed-surface checks passed

## Size override

This PR is deletion-heavy: 15,330 removed lines and 21 added lines. The
added lines are documentation and a negative contract test confirming
Creem is no longer a supported subscription-management provider.
```

### PR Body

## Summary

- remove the remaining Creem standard-subscription runtime: reconciliation, first payment, renewal, trials, subscription changes, and replacement settlement
- remove Creem dispatches from subscription routes, enterprise-join cancellation, hourly maintenance, billing summaries, and manual-review monitoring
- delete the corresponding Creem-only tests while retaining Airwallex and provider-neutral billing coverage
- document that standard Card lifecycle validation now runs through Airwallex

## Impact

- Current Card checkout, first payment, renewal, reconciliation, cancel, renew, and downgrade behavior remains owned by Airwallex.
- Stripe, Antom, Apple, and enterprise subscription paths remain unchanged.
- Historical `provider=creem` literals and read adapters remain for archival compatibility.
- Six Creem-named helpers are intentionally retained because Airwallex/shared checkout still imports them; neutralizing those dependencies is the next cleanup PR.
- There are no real Creem users or pending Creem lifecycle state to preserve.

## Validation

- `bash scripts/verify-py.sh`
- focused backend regression: 200 passed
- pre-commit and pre-push changed-surface checks passed

## Size override

This PR is deletion-heavy: 15,330 removed lines and 21 added lines. The added lines are documentation and a negative contract test confirming Creem is no longer a supported subscription-management provider.


---

## refactor(billing): remove Creem webhook ingress (#3469)

- **SHA**: `b93942e453d02810dfeecd5248ce0b2be16e4a3e`
- **作者**: tim-srp
- **日期**: 2026-08-21T04:09:08Z
- **PR**: #3469

### Commit Message

```
refactor(billing): remove Creem webhook ingress (#3469)
```

### PR Body

## Summary

- remove the backend `POST /billing/webhooks/creem` ingress and its signature/claim/dispatcher implementation
- remove the frontend `/api/creem/webhook` proxy and middleware public-route exemption
- delete dedicated webhook tests and retain negative contracts proving the retired paths are unavailable
- update the historical staging validation guide to use Airwallex and expect Creem webhook routes to return 404

## Impact

- New and current Card payment flows remain on Airwallex.
- Stripe, Antom, and Airwallex webhook routes are unchanged.
- Creem reconciliation and historical `provider=creem` schema compatibility remain for a later cleanup PR.
- No active Creem users exist, so removing the external ingress does not drop a supported production flow.

## Validation

- `bash scripts/verify-changed.sh`
- backend focused suite: 183 passed
- frontend focused suite: 200 passed
- pre-commit and pre-push quality gates passed


---

## fix(chat): preserve terminal tool status (#3470)

- **SHA**: `aec8ed32c56daeba1f50e268302638b7f95ee4be`
- **作者**: rayrain-srp
- **日期**: 2026-08-21T03:50:59Z
- **PR**: #3470

### Commit Message

```
fix(chat): preserve terminal tool status (#3470)

## Summary
- keep legacy Mattermost tool states terminal once they reach `done`,
`error`, or `cancelled`
- still merge late descriptive metadata without letting a delayed
`running` event restart the timer
- add regression coverage for out-of-order terminal/start/running posts
and replayed running events

## Root cause
OpenClaw emits tool callbacks best-effort, and the Mattermost plugin
publishes lifecycle posts independently. For fast tool failures, the
terminal post can reach Mattermost before the start/running posts. The
ECAP parser merged by Mattermost arrival order and allowed the later
`running` status to overwrite an already-terminal step, so the UI
resumed an elapsed timer for a tool that had already failed.

This PR adds the agreed ECAP consumer-side protection only. It does not
change Mattermost/OpenClaw publishing or project/workspace association
behavior.

Linear:
https://linear.app/srpone/issue/ECA-1388/agent-builder-%E5%B7%A5%E5%85%B7%E7%BB%88%E6%80%81%E8%A2%AB%E8%BF%9F%E5%88%B0%E7%9A%84-running-%E8%A6%86%E7%9B%96%E5%AF%BC%E8%87%B4%E6%8C%81%E7%BB%AD%E8%AE%A1%E6%97%B6

## Test plan
- [x] `git diff --check`
- [x] Prettier check for both changed files
- [x] web governance guards
- [ ] targeted Vitest, TypeScript, and ESLint locally: attempted, but
Node workers repeatedly blocked in kernel `wait_on_page_bit_common`
before producing test/type/lint results; GitHub CI is the authoritative
clean-runner validation
- [x] GitHub CI: 38/38 checks passed, including web tests,
lint/typecheck, build, and CodeQL
```

### PR Body

## Summary
- keep legacy Mattermost tool states terminal once they reach `done`, `error`, or `cancelled`
- still merge late descriptive metadata without letting a delayed `running` event restart the timer
- add regression coverage for out-of-order terminal/start/running posts and replayed running events

## Root cause
OpenClaw emits tool callbacks best-effort, and the Mattermost plugin publishes lifecycle posts independently. For fast tool failures, the terminal post can reach Mattermost before the start/running posts. The ECAP parser merged by Mattermost arrival order and allowed the later `running` status to overwrite an already-terminal step, so the UI resumed an elapsed timer for a tool that had already failed.

This PR adds the agreed ECAP consumer-side protection only. It does not change Mattermost/OpenClaw publishing or project/workspace association behavior.

Linear: https://linear.app/srpone/issue/ECA-1388/agent-builder-%E5%B7%A5%E5%85%B7%E7%BB%88%E6%80%81%E8%A2%AB%E8%BF%9F%E5%88%B0%E7%9A%84-running-%E8%A6%86%E7%9B%96%E5%AF%BC%E8%87%B4%E6%8C%81%E7%BB%AD%E8%AE%A1%E6%97%B6

## Test plan
- [x] `git diff --check`
- [x] Prettier check for both changed files
- [x] web governance guards
- [ ] targeted Vitest, TypeScript, and ESLint locally: attempted, but Node workers repeatedly blocked in kernel `wait_on_page_bit_common` before producing test/type/lint results; GitHub CI is the authoritative clean-runner validation
- [x] GitHub CI: 38/38 checks passed, including web tests, lint/typecheck, build, and CodeQL


---

## fix(agent-builder): normalize preview environment timestamps (#3474)

- **SHA**: `6dfdac721dad39465a6b517fbe3a0a9a84973ed0`
- **作者**: kaka-srp
- **日期**: 2026-08-21T03:30:35Z
- **PR**: #3474

### Commit Message

```
fix(agent-builder): normalize preview environment timestamps (#3474)

## Summary

- Normalize persisted Pack Test Environment timestamps before Preview
deadline comparisons.
- Cover MongoDB-decoded naïve timestamps while an Environment is
building and when it times out.

## Root cause

MongoDB decodes persisted datetimes without timezone information, while
the Preview runtime compares them with `datetime.now(UTC)`. When a new
Pack Test Environment was still building, that mixed naïve and aware
values and raised `TypeError: can't compare offset-naive and
offset-aware datetimes` instead of returning the build status.

## Test plan

- [x] `pytest -q tests/unit/test_pack_test_engine_runtime_service.py` (9
passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

## Summary

- Normalize persisted Pack Test Environment timestamps before Preview deadline comparisons.
- Cover MongoDB-decoded naïve timestamps while an Environment is building and when it times out.

## Root cause

MongoDB decodes persisted datetimes without timezone information, while the Preview runtime compares them with `datetime.now(UTC)`. When a new Pack Test Environment was still building, that mixed naïve and aware values and raised `TypeError: can't compare offset-naive and offset-aware datetimes` instead of returning the build status.

## Test plan

- [x] `pytest -q tests/unit/test_pack_test_engine_runtime_service.py` (9 passed)
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`


---
