# ecap-workspace commits — 2026-07-25

## fix(org): skip wallet provisioning during org upgrade (#3070)

- **SHA**: `9050e66efd1756ed9fcf45ed2523cb6c00ff9003`
- **Author**: bill-srp
- **Date**: 2026-07-25T03:54:29Z
- **PR**: #3070

### Commit Message
```
fix(org): skip wallet provisioning during org upgrade (#3070)

## Summary
- stop looking up or creating wallets when upgrading a personal org to a
team org
- leave existing `wallet_subscription_id` and `wallet_topup_id` values
untouched by removing them from the upgrade CAS contract
- keep the existing billing-mode conversion, Mattermost repair, tests,
and design documents aligned with the new behavior

## Root cause
The upgrade flow reused wallet provisioning behavior from fresh team-org
creation. Upgrading an existing org should only convert its existing
billing team to business mode; wallet setup belongs to the later
plan-purchase flow.

## Test plan
- [x] `pytest tests/unit/test_org_service.py tests/unit/test_org_repo.py
tests/unit/test_routes_internal_orgs.py
tests/unit/test_internal_users_orgs.py -q` — 64 passed
- [x] `bash scripts/verify-changed.sh` — ruff, format, pyright, and
import-linter passed
- [x] pre-commit and pre-push hooks passed
- [ ] Local BDD execution was unavailable because MongoDB was not
running; CI remains authoritative for the BDD scenario
```

### PR Body
```
## Summary
- stop looking up or creating wallets when upgrading a personal org to a team org
- leave existing `wallet_subscription_id` and `wallet_topup_id` values untouched by removing them from the upgrade CAS contract
- keep the existing billing-mode conversion, Mattermost repair, tests, and design documents aligned with the new behavior

## Root cause
The upgrade flow reused wallet provisioning behavior from fresh team-org creation. Upgrading an existing org should only convert its existing billing team to business mode; wallet setup belongs to the later plan-purchase flow.

## Test plan
- [x] `pytest tests/unit/test_org_service.py tests/unit/test_org_repo.py tests/unit/test_routes_internal_orgs.py tests/unit/test_internal_users_orgs.py -q` — 64 passed
- [x] `bash scripts/verify-changed.sh` — ruff, format, pyright, and import-linter passed
- [x] pre-commit and pre-push hooks passed
- [ ] Local BDD execution was unavailable because MongoDB was not running; CI remains authoritative for the BDD scenario

```

## feat(enterprise-admin): restore parsed pack archive uploads (#3067)

- **SHA**: `463ae7cc3224c0bcec949114331976da183965a7`
- **Author**: bill-srp
- **Date**: 2026-07-25T02:39:20Z
- **PR**: #3067

### Commit Message
```
feat(enterprise-admin): restore parsed pack archive uploads (#3067)

## Linear

N/A

## Summary

- restore the Enterprise Admin “Add pack” and “Submit new version” entry
points for organization admins
- share Dashboard Console’s Agent Pack archive parser through a
workspace package, support ZIP/TAR.GZ, and autofill archive metadata in
both Enterprise forms
- upload archives and optional avatars through the Worker R2 bindings,
including expanded metadata fields and parsed quick commands
- add an explicit admin-only direct-upload API contract while preserving
the Pack Test gate for non-admin submissions
- positively verify the target org admin and Pack before R2 writes;
clean up uploads after explicit rejection while preserving them when a
committed submission is possible
- redirect partial create failures to the persisted draft instead of
reusing stale form state against a cached Pack ID
- require claw-interface to HEAD the submitted private R2 key and verify
its stored org/Pack metadata before any direct upload can be
auto-approved

## Test plan

- [x] Enterprise Admin: 47 test files / 306 tests, TypeScript, ESLint,
and production build
- [x] Dashboard Console: 68 test files / 567 tests, TypeScript, ESLint,
and production build
- [x] Shared archive package: TypeScript and ESLint
- [x] claw-interface: targeted Pack Store/schema/service tests (78
passed), Ruff check, and Ruff format
- [x] Post-rebase focused checks: Enterprise 30 tests, Dashboard parser
19 tests, backend route 21 tests
- [x] Review fixes: R2 authorization/cleanup route tests plus
create/version compensation regressions
- [x] Provenance fix: 56 backend route, R2 storage, and direct-upload
validation tests plus Ruff check/format
- [x] Cleanup race fix: preserve assets after ambiguous transport/5xx
results; delete them after pre-submit failures or explicit 4xx rejection
- [ ] `scripts/verify-changed.sh` backend static tier was skipped
locally because `pyright` and `lint-imports` are not installed; CI
remains authoritative

## Size override

The size check counts 1,058 changed lines for moving the existing
526-line Dashboard archive parser into the shared workspace package (526
additions plus 532 deletions/re-export lines). The remaining overage is
the post-review org-admin authorization, R2 compensation path, and their
regression coverage. These changes form one cross-surface contract and
are kept together so neither app nor backend lands with a partial upload
flow.
```

### PR Body
```
## Linear

N/A

## Summary

- restore the Enterprise Admin “Add pack” and “Submit new version” entry points for organization admins
- share Dashboard Console’s Agent Pack archive parser through a workspace package, support ZIP/TAR.GZ, and autofill archive metadata in both Enterprise forms
- upload archives and optional avatars through the Worker R2 bindings, including expanded metadata fields and parsed quick commands
- add an explicit admin-only direct-upload API contract while preserving the Pack Test gate for non-admin submissions
- positively verify the target org admin and Pack before R2 writes; clean up uploads after explicit rejection while preserving them when a committed submission is possible
- redirect partial create failures to the persisted draft instead of reusing stale form state against a cached Pack ID
- require claw-interface to HEAD the submitted private R2 key and verify its stored org/Pack metadata before any direct upload can be auto-approved

## Test plan

- [x] Enterprise Admin: 47 test files / 306 tests, TypeScript, ESLint, and production build
- [x] Dashboard Console: 68 test files / 567 tests, TypeScript, ESLint, and production build
- [x] Shared archive package: TypeScript and ESLint
- [x] claw-interface: targeted Pack Store/schema/service tests (78 passed), Ruff check, and Ruff format
- [x] Post-rebase focused checks: Enterprise 30 tests, Dashboard parser 19 tests, backend route 21 tests
- [x] Review fixes: R2 authorization/cleanup route tests plus create/version compensation regressions
- [x] Provenance fix: 56 backend route, R2 storage, and direct-upload validation tests plus Ruff check/format
- [x] Cleanup race fix: preserve assets after ambiguous transport/5xx results; delete them after pre-submit failures or explicit 4xx rejection
- [ ] `scripts/verify-changed.sh` backend static tier was skipped locally because `pyright` and `lint-imports` are not installed; CI remains authoritative

## Size override

The size check counts 1,058 changed lines for moving the existing 526-line Dashboard archive parser into the shared workspace package (526 additions plus 532 deletions/re-export lines). The remaining overage is the post-review org-admin authorization, R2 compensation path, and their regression coverage. These changes form one cross-surface contract and are kept together so neither app nor backend lands with a partial upload flow.

```
