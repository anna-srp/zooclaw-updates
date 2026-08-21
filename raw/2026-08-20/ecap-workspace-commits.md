# SerendipityOneInc/ecap-workspace — commits 2026-08-20

## fix(billing): replace stale Airwallex checkout (#3471)

- **SHA**: `059948fcd842a91c9c65069cfd1802eb929e4115`
- **作者**: tim-srp
- **日期**: 2026-08-20T14:23:50Z
- **PR**: #3471

### Commit Message

```
fix(billing): replace stale Airwallex checkout (#3471)
```

### PR Body

## Summary

- replace a stale pending Airwallex checkout when a user changes subscription selection after an unsuccessful payment
- retain failed/ambiguous checkout outcomes for manual review and prevent duplicate provider mutations
- keep completed subscriptions outside this flow; plan changes continue through upgrade/downgrade handling

## Validation

- 193 focused backend tests passed
- ruff, formatting, import-linter, and project-venv Pyright pre-commit checks passed


---

## refactor(billing): remove Creem enterprise lifecycle (#3467)

- **SHA**: `f982b324a0cee839bd4a76a0936cecdb9e94f474`
- **作者**: tim-srp
- **日期**: 2026-08-20T09:57:11Z
- **PR**: #3467

### Commit Message

```
refactor(billing): remove Creem enterprise lifecycle (#3467)

## Summary

- remove the complete Creem enterprise-package payment lifecycle
- remove enterprise payment, renewal, active, refund/dispute,
reconciliation, and recovery services
- remove the Creem-only financial-loss repository and enterprise tests
- remove the unused Creem catalog preflight and historical runnable
command

## Impact boundary

This relies on the confirmed absence of real Creem users and Creem
enterprise orders. Standard Creem subscription webhook/reconciliation
and Airwallex enterprise checkout/settlement remain intact. Shared
Billing v2 and card replacement infrastructure remain intact.

Creem refund/dispute events are no longer projected as enterprise
financial loss. They fall through the existing known-but-unsupported
webhook behavior; no current business data can reach that path.

## Validation

- `bash scripts/verify-py.sh`
- all full static/architecture/dead-code/duplication gates from
`verify-py.sh --full` passed
- focused current-business regression suite: 346 passed
- focused Creem catalog/config/client suite: 145 passed
- full local pytest attempted twice but the macOS Python process
segfaulted during unrelated test collection; CI remains authoritative
for the full suite
- production/test reference scan confirms no imports of the removed
enterprise modules, repository, or vertical-pack Creem product setting

## Context

This follows #3460, #3462, and #3465 in the Creem cleanup sequence.
```

### PR Body

## Summary

- remove the complete Creem enterprise-package payment lifecycle
- remove enterprise payment, renewal, active, refund/dispute, reconciliation, and recovery services
- remove the Creem-only financial-loss repository and enterprise tests
- remove the unused Creem catalog preflight and historical runnable command

## Impact boundary

This relies on the confirmed absence of real Creem users and Creem enterprise orders. Standard Creem subscription webhook/reconciliation and Airwallex enterprise checkout/settlement remain intact. Shared Billing v2 and card replacement infrastructure remain intact.

Creem refund/dispute events are no longer projected as enterprise financial loss. They fall through the existing known-but-unsupported webhook behavior; no current business data can reach that path.

## Validation

- `bash scripts/verify-py.sh`
- all full static/architecture/dead-code/duplication gates from `verify-py.sh --full` passed
- focused current-business regression suite: 346 passed
- focused Creem catalog/config/client suite: 145 passed
- full local pytest attempted twice but the macOS Python process segfaulted during unrelated test collection; CI remains authoritative for the full suite
- production/test reference scan confirms no imports of the removed enterprise modules, repository, or vertical-pack Creem product setting

## Context

This follows #3460, #3462, and #3465 in the Creem cleanup sequence.


---

## feat(agent-packs): enable production engine rollout (#3468)

- **SHA**: `83fa9bc42caad59b2ab8b7fd363c21b877cca276`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-20T09:43:09Z
- **PR**: #3468

### Commit Message

```
feat(agent-packs): enable production engine rollout (#3468)

## Linear

N/A

## Summary

- enable Engine Pack runtime projection in production with the nine
production-local Pack IDs audited by the `v2.2.34-release` catalog
bootstrap
- expand the staging allowlist from five to all nine active Engine Packs
- lock both environment-specific allowlists in the deployment contract
test so the distinct Oura Ring WhatsApp IDs cannot be mixed

## Test plan

- [x] `pytest
services/claw-interface/tests/unit/test_pack_runtime_asset_deployment_wiring.py
-q`
- [x] render both overlays with `kubectl kustomize` and verify
`ENGINE_PACK_RUNTIME_ASSETS_ENABLED=true`, nine unique IDs, and the
environment-local Oura ID
- [x] `bash scripts/verify-changed.sh`

## Rollout

After merge, wait for the normal staging service deployment and replay
`v2.2.34-release` against staging so the four newly allowed Packs are
projected. Then publish a new Claw Interface service release tag, wait
for the production rollout to finish, and immediately replay
`v2.2.34-release` through the production Engine asset reconciliation
workflow. The replay schedules projections for the already registered
assets; this PR does not mutate shared environment data directly.
```

### PR Body

## Linear

N/A

## Summary

- enable Engine Pack runtime projection in production with the nine production-local Pack IDs audited by the `v2.2.34-release` catalog bootstrap
- expand the staging allowlist from five to all nine active Engine Packs
- lock both environment-specific allowlists in the deployment contract test so the distinct Oura Ring WhatsApp IDs cannot be mixed

## Test plan

- [x] `pytest services/claw-interface/tests/unit/test_pack_runtime_asset_deployment_wiring.py -q`
- [x] render both overlays with `kubectl kustomize` and verify `ENGINE_PACK_RUNTIME_ASSETS_ENABLED=true`, nine unique IDs, and the environment-local Oura ID
- [x] `bash scripts/verify-changed.sh`

## Rollout

After merge, wait for the normal staging service deployment and replay `v2.2.34-release` against staging so the four newly allowed Packs are projected. Then publish a new Claw Interface service release tag, wait for the production rollout to finish, and immediately replay `v2.2.34-release` through the production Engine asset reconciliation workflow. The replay schedules projections for the already registered assets; this PR does not mutate shared environment data directly.


---

## fix(agent-packs): bound catalog bootstrap uploads (#3466)

- **SHA**: `eb833ba03b81d1db02ececad338c52d749a676db`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-20T09:30:37Z
- **PR**: #3466

### Commit Message

```
fix(agent-packs): bound catalog bootstrap uploads (#3466)

## Summary
- Bound the official catalog bootstrap multipart read to the existing
100 MiB Pack archive limit.
- Reject declared oversized uploads before reading and probe at most one
byte beyond the limit when the multipart size is unknown.
- Return the existing Pack catalog size error as HTTP 413 and cover both
fast-path and streamed overflow cases.

Follow-up to the final Codex review on #3463.

## Root cause
The route called `await archive.read()` before the service-level archive
validation ran, so a valid bootstrap request could buffer an arbitrarily
large multipart file in worker memory before the 100 MiB check.

## Test plan
- [x] `pytest -q
services/claw-interface/tests/unit/test_agent_pack_catalog_bootstrap_route.py`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

## Summary
- Bound the official catalog bootstrap multipart read to the existing 100 MiB Pack archive limit.
- Reject declared oversized uploads before reading and probe at most one byte beyond the limit when the multipart size is unknown.
- Return the existing Pack catalog size error as HTTP 413 and cover both fast-path and streamed overflow cases.

Follow-up to the final Codex review on #3463.

## Root cause
The route called `await archive.read()` before the service-level archive validation ran, so a valid bootstrap request could buffer an arbitrarily large multipart file in worker memory before the 100 MiB check.

## Test plan
- [x] `pytest -q services/claw-interface/tests/unit/test_agent_pack_catalog_bootstrap_route.py`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`


---

## refactor(billing): neutralize shared card replacement infrastructure (#3465)

- **SHA**: `ed4be356a07bce7797474308d56e20e7a808fa07`
- **作者**: tim-srp
- **日期**: 2026-08-20T09:21:44Z
- **PR**: #3465

### Commit Message

```
refactor(billing): neutralize shared card replacement infrastructure (#3465)

## Summary

- rename shared Creem replacement modules and schemas to
provider-neutral card replacement names
- require every shared card repository caller to pass its billing
provider explicitly
- keep the legacy Mongo index name unchanged to avoid coupling this
refactor to an index migration

## Behavior

No checkout, settlement, renewal, reconciliation, or replacement
admission rules change. Existing Creem callers now pass
`provider="creem"`; Airwallex callers continue to pass
`provider="airwallex"`.

## Validation

- `bash scripts/verify-py.sh`
- 481 focused billing replacement/reconciliation/repository tests
passed, 1 skipped
- pre-commit and pre-push changed-surface gates passed

## Context

PR 2 of the Creem cleanup sequence. Follows #3462.
```

### PR Body

## Summary

- rename shared Creem replacement modules and schemas to provider-neutral card replacement names
- require every shared card repository caller to pass its billing provider explicitly
- keep the legacy Mongo index name unchanged to avoid coupling this refactor to an index migration

## Behavior

No checkout, settlement, renewal, reconciliation, or replacement admission rules change. Existing Creem callers now pass `provider="creem"`; Airwallex callers continue to pass `provider="airwallex"`.

## Validation

- `bash scripts/verify-py.sh`
- 481 focused billing replacement/reconciliation/repository tests passed, 1 skipped
- pre-commit and pre-push changed-surface gates passed

## Context

PR 2 of the Creem cleanup sequence. Follows #3462.


---

## fix(web): preserve main avatar for migrated agents (#3464)

- **SHA**: `015a6adda26719cc8576b54820ed8686a2c628e3`
- **作者**: kaka-srp
- **日期**: 2026-08-20T09:01:31Z
- **PR**: #3464

### Commit Message

```
fix(web): preserve main avatar for migrated agents (#3464)

## Summary
- Preserve canonical main-agent identity when migrated agents use a
public `agt_*` ID in both live chat and historical sessions.
- Use the branded Assistant avatar as the main-agent fallback in
transcript messages and the unified composer.
- Add regression coverage for migrated main agents and the empty
agent-picker fallback.

## Root cause
The session transcript inferred main-agent identity from the legacy
`main` ID, while migrated main agents expose a public `agt_*` ID. The
unified composer also used a hard-coded robot emoji when no explicit
avatar was present. Both paths therefore bypassed the branded main-agent
fallback even though the workspace correctly reported `is_main: true`.

## Test plan
- [x] `bash scripts/verify-web.sh <changed frontend paths>`
- [x] TypeScript compilation passed.
- [x] 158 targeted unit tests passed across the original changed chat
surfaces.
- [x] 56 targeted unit tests passed for the live-chat follow-up.
- [x] ESLint passed for the changed files and the repository commit
hook.
```

### PR Body

## Summary
- Preserve canonical main-agent identity when migrated agents use a public `agt_*` ID in both live chat and historical sessions.
- Use the branded Assistant avatar as the main-agent fallback in transcript messages and the unified composer.
- Add regression coverage for migrated main agents and the empty agent-picker fallback.

## Root cause
The session transcript inferred main-agent identity from the legacy `main` ID, while migrated main agents expose a public `agt_*` ID. The unified composer also used a hard-coded robot emoji when no explicit avatar was present. Both paths therefore bypassed the branded main-agent fallback even though the workspace correctly reported `is_main: true`.

## Test plan
- [x] `bash scripts/verify-web.sh <changed frontend paths>`
- [x] TypeScript compilation passed.
- [x] 158 targeted unit tests passed across the original changed chat surfaces.
- [x] 56 targeted unit tests passed for the live-chat follow-up.
- [x] ESLint passed for the changed files and the repository commit hook.


---

## feat(agent-packs): bootstrap official catalog (#3463)

- **SHA**: `b088f07b9495db3d19ac44fed7c00e830a7bb554`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-20T08:53:45Z
- **PR**: #3463

### Commit Message

```
feat(agent-packs): bootstrap official catalog (#3463)

## Linear

No linked issue.

## Summary

- add a dedicated-token `POST /agent-packs/bootstrap/catalog` lane for
environment-local official Pack creation
- return existing active Packs unchanged; create only missing hidden
Packs, and resume only bootstrap-authored partial state
- auto-approve the pinned initial OpenClaw submission and verify its
initial Environment binding even while production V2 routes remain dark
- validate bounded, single-root release ZIPs and preserve compatibility
with the legacy `multilingual` manifest marker
- wire the new optional Vault secret key into staging and production
deployments and document the ordered rollout

This PR does not enable the production Engine Pack gate or mutate
production data. It must deploy before the companion `ecap-agent-pack`
workflow PR is run.

## Rollout

1. Merge and deploy this PR.
2. Set a distinct `AGENT_PACK_CATALOG_BOOTSTRAP_TOKEN` in each
environment's Vault-backed Claw Interface secret and matching protected
`ecap-agent-pack` GitHub Environment.
3. Merge the companion Agent Pack PR and run pinned reconciliation.
4. Use the production-local Pack IDs from the Actions summary in a
separately reviewed production gate change.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] targeted catalog bootstrap, auth, and Kustomize wiring tests: 12
passed
- [x] rendered both staging and production Kustomize overlays
- [x] packaged and parsed the real OpenClaw archives for all 9 active
Engine Packs
```

### PR Body

## Linear

No linked issue.

## Summary

- add a dedicated-token `POST /agent-packs/bootstrap/catalog` lane for environment-local official Pack creation
- return existing active Packs unchanged; create only missing hidden Packs, and resume only bootstrap-authored partial state
- auto-approve the pinned initial OpenClaw submission and verify its initial Environment binding even while production V2 routes remain dark
- validate bounded, single-root release ZIPs and preserve compatibility with the legacy `multilingual` manifest marker
- wire the new optional Vault secret key into staging and production deployments and document the ordered rollout

This PR does not enable the production Engine Pack gate or mutate production data. It must deploy before the companion `ecap-agent-pack` workflow PR is run.

## Rollout

1. Merge and deploy this PR.
2. Set a distinct `AGENT_PACK_CATALOG_BOOTSTRAP_TOKEN` in each environment's Vault-backed Claw Interface secret and matching protected `ecap-agent-pack` GitHub Environment.
3. Merge the companion Agent Pack PR and run pinned reconciliation.
4. Use the production-local Pack IDs from the Actions summary in a separately reviewed production gate change.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] targeted catalog bootstrap, auth, and Kustomize wiring tests: 12 passed
- [x] rendered both staging and production Kustomize overlays
- [x] packaged and parsed the real OpenClaw archives for all 9 active Engine Packs


---

## refactor(billing): remove Creem checkout creation primitives (#3462)

- **SHA**: `1955ac8ba1b05b88c5d7a214ab698af1d24764cb`
- **作者**: tim-srp
- **日期**: 2026-08-20T08:38:58Z
- **PR**: #3462

### Commit Message

```
refactor(billing): remove Creem checkout creation primitives (#3462)

## Summary

- remove the unused Creem hosted-checkout mutation and response
ownership validation
- remove create-checkout-only request/response schemas
- remove the unused Restaurant product preflight that only served Creem
checkout creation

## Scope

This is the second low-risk Creem cleanup batch after #3460. It
preserves Creem webhook/retrieval and subscription-management models,
the read API client, and `is_official_creem_checkout_url`, which remains
shared by Airwallex replacement handling.

## Verification

- focused Creem client/catalog and Airwallex replacement suite: 170
passed
- `bash scripts/verify-py.sh`
- pre-push `bash scripts/verify-changed.sh`
- repository scan confirms no remaining references to the removed
checkout creation symbols
```

### PR Body

## Summary

- remove the unused Creem hosted-checkout mutation and response ownership validation
- remove create-checkout-only request/response schemas
- remove the unused Restaurant product preflight that only served Creem checkout creation

## Scope

This is the second low-risk Creem cleanup batch after #3460. It preserves Creem webhook/retrieval and subscription-management models, the read API client, and `is_official_creem_checkout_url`, which remains shared by Airwallex replacement handling.

## Verification

- focused Creem client/catalog and Airwallex replacement suite: 170 passed
- `bash scripts/verify-py.sh`
- pre-push `bash scripts/verify-changed.sh`
- repository scan confirms no remaining references to the removed checkout creation symbols


---

## refactor(billing): remove Creem vertical pack checkout (#3460)

- **SHA**: `2b18e9fd2883f2f21ea028daa7e00981a17537f6`
- **作者**: tim-srp
- **日期**: 2026-08-20T08:14:29Z
- **PR**: #3460

### Commit Message

```
refactor(billing): remove Creem vertical pack checkout (#3460)

## Summary

- remove the unreachable Creem checkout implementation for Restaurant
vertical packs
- restrict vertical-pack card capability and API contracts to Stripe or
Airwallex
- keep the active Airwallex orchestration coverage in a
provider-specific test module

## Scope

This is the first low-risk Creem cleanup batch. It does not remove Creem
webhook, reconciliation, refund/dispute, historical provider values, or
shared card-checkout infrastructure.

## Verification

- `pytest` focused billing suite: 146 passed
- enterprise-admin Vitest: 58 files / 416 tests passed
- enterprise-admin `tsc --noEmit`
- enterprise-admin ESLint
- `bash scripts/verify-py.sh`
- pre-push `bash scripts/verify-changed.sh`
```

### PR Body

## Summary

- remove the unreachable Creem checkout implementation for Restaurant vertical packs
- restrict vertical-pack card capability and API contracts to Stripe or Airwallex
- keep the active Airwallex orchestration coverage in a provider-specific test module

## Scope

This is the first low-risk Creem cleanup batch. It does not remove Creem webhook, reconciliation, refund/dispute, historical provider values, or shared card-checkout infrastructure.

## Verification

- `pytest` focused billing suite: 146 passed
- enterprise-admin Vitest: 58 files / 416 tests passed
- enterprise-admin `tsc --noEmit`
- enterprise-admin ESLint
- `bash scripts/verify-py.sh`
- pre-push `bash scripts/verify-changed.sh`


---

## fix(pack): separate runtime gates by environment (#3461)

- **SHA**: `4bbfc830d3a920a664c2d33c0e9268c62674aeda`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-20T08:09:22Z
- **PR**: #3461

### Commit Message

```
fix(pack): separate runtime gates by environment (#3461)

## Summary

- keep immutable `pack_id` as the Engine runtime-asset rollout identity
- document that Pack IDs are generated independently per Workspace
database and must never be copied between environments
- retain the five verified staging Pack IDs while disabling production
with an empty allowlist until its local catalog IDs are audited
- strengthen deployment wiring coverage so staging and production cannot
silently share the same rollout configuration again

## Why

The production overlay copied staging UUIDs. Those values cannot
identify the intended production rows. Replacing them with bare
`display_id` values would also be unsafe because uniqueness is scoped to
`(org_id, display_id)` and catalog metadata can change.

Runtime authorization therefore remains tied to the immutable local
`pack_id`. Reconciliation may use catalog metadata to locate a row, but
each environment must explicitly configure the resolved local IDs.

## Production follow-up

Production intentionally remains fail-closed in this PR. After its
catalog is complete, including `oura_ring_whatsapp`, audit the five
production Pack IDs, update only the production overlay, deploy, and
rerun Agent Pack reconciliation.

## Validation

- `bash scripts/verify-py.sh`
- `pytest tests/unit/test_pack_runtime_asset_deployment_wiring.py
tests/unit/test_pack_runtime_asset.py -q`
- `kubectl kustomize` for staging and production overlays
- repository pre-commit hooks
```

### PR Body

## Summary

- keep immutable `pack_id` as the Engine runtime-asset rollout identity
- document that Pack IDs are generated independently per Workspace database and must never be copied between environments
- retain the five verified staging Pack IDs while disabling production with an empty allowlist until its local catalog IDs are audited
- strengthen deployment wiring coverage so staging and production cannot silently share the same rollout configuration again

## Why

The production overlay copied staging UUIDs. Those values cannot identify the intended production rows. Replacing them with bare `display_id` values would also be unsafe because uniqueness is scoped to `(org_id, display_id)` and catalog metadata can change.

Runtime authorization therefore remains tied to the immutable local `pack_id`. Reconciliation may use catalog metadata to locate a row, but each environment must explicitly configure the resolved local IDs.

## Production follow-up

Production intentionally remains fail-closed in this PR. After its catalog is complete, including `oura_ring_whatsapp`, audit the five production Pack IDs, update only the production overlay, deploy, and rerun Agent Pack reconciliation.

## Validation

- `bash scripts/verify-py.sh`
- `pytest tests/unit/test_pack_runtime_asset_deployment_wiring.py tests/unit/test_pack_runtime_asset.py -q`
- `kubectl kustomize` for staging and production overlays
- repository pre-commit hooks


---

## fix(billing): correct Airwallex subscription cancellation (#3459)

- **SHA**: `68e0059dbedbab6c80a4dc4c3e864e755b23f4e9`
- **作者**: tim-srp
- **日期**: 2026-08-20T08:00:34Z
- **PR**: #3459

### Commit Message

```
fix(billing): correct Airwallex subscription cancellation (#3459)

## Summary

- 修复 Airwallex 订阅取消误走立即取消接口的问题，改为周期末取消。
- 兼容官方 subscription retrieve 与 webhook payload 字段。
- 保留 webhook Event ID 的幂等语义。

## Root cause

订阅 schema 未建模官方 `starts_at` / `ends_at`
字段，导致变更已提交后本地响应校验仍误判周期不一致。取消操作使用了立即取消 endpoint，且 webhook 仅支持
`data.object` 嵌套结构。

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 运行 108 个 Airwallex 相关单元测试

Closes #3456
```

### PR Body

## Summary

- 修复 Airwallex 订阅取消误走立即取消接口的问题，改为周期末取消。
- 兼容官方 subscription retrieve 与 webhook payload 字段。
- 保留 webhook Event ID 的幂等语义。

## Root cause

订阅 schema 未建模官方 `starts_at` / `ends_at` 字段，导致变更已提交后本地响应校验仍误判周期不一致。取消操作使用了立即取消 endpoint，且 webhook 仅支持 `data.object` 嵌套结构。

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 运行 108 个 Airwallex 相关单元测试

Closes #3456


---

## fix(billing): normalize airwallex invoice amounts (#3457)

- **SHA**: `2803c48cdedddc17f724b9d39ff77faa9640130d`
- **作者**: tim-srp
- **日期**: 2026-08-20T07:41:15Z
- **PR**: #3457

### Commit Message

```
fix(billing): normalize airwallex invoice amounts (#3457)

## Summary

- Normalize Airwallex Billing invoice amounts from major currency units
to exact USD cents before payment projection.
- Reject invoice amounts that cannot be represented exactly in cents
instead of silently skipping validation.
- Use the official Airwallex subscription collection endpoint for
reconciliation.

## Validation

- `pytest
services/claw-interface/tests/unit/test_airwallex_event_facts.py
services/claw-interface/tests/unit/test_airwallex_client.py
services/claw-interface/tests/unit/test_airwallex_first_payment.py
services/claw-interface/tests/unit/test_airwallex_renewal.py
services/claw-interface/tests/unit/test_airwallex_enterprise_subscription.py
-q` (93 passed)
- `bash scripts/verify-py.sh`

## Risk

This changes only the provider-to-domain money boundary. Existing
downstream billing logic continues to receive integer cents; malformed
sub-cent provider amounts now enter the existing webhook failure/retry
path rather than granting entitlements with an unverified amount.
```

### PR Body

## Summary

- Normalize Airwallex Billing invoice amounts from major currency units to exact USD cents before payment projection.
- Reject invoice amounts that cannot be represented exactly in cents instead of silently skipping validation.
- Use the official Airwallex subscription collection endpoint for reconciliation.

## Validation

- `pytest services/claw-interface/tests/unit/test_airwallex_event_facts.py services/claw-interface/tests/unit/test_airwallex_client.py services/claw-interface/tests/unit/test_airwallex_first_payment.py services/claw-interface/tests/unit/test_airwallex_renewal.py services/claw-interface/tests/unit/test_airwallex_enterprise_subscription.py -q` (93 passed)
- `bash scripts/verify-py.sh`

## Risk

This changes only the provider-to-domain money boundary. Existing downstream billing logic continues to receive integer cents; malformed sub-cent provider amounts now enter the existing webhook failure/retry path rather than granting entitlements with an unverified amount.


---

## refactor(billing): generalize vertical pack plan configuration (#3458)

- **SHA**: `5390319a7379a3986c88d6661b5c2aa746e1deb5`
- **作者**: tim-srp
- **日期**: 2026-08-20T07:30:50Z
- **PR**: #3458

### Commit Message

```
refactor(billing): generalize vertical pack plan configuration (#3458)

## Summary
- replace the Creem-prefixed Restaurant vertical-pack plan setting with
`VERTICAL_PACK_PLAN_ID_RESTAURANT_AI_TEAM_MONTHLY`
- update Airwallex, legacy Creem catalog, routing, capability, fixtures,
and the root environment example
- intentionally provide no fallback to the old environment variable

## Rollout
- the requester confirmed
`VERTICAL_PACK_PLAN_ID_RESTAURANT_AI_TEAM_MONTHLY` is already populated
with the same value as the old setting before rollout
- restart or redeploy `claw-interface` so Pods load the new environment
variable

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] 242 targeted Airwallex, Creem enterprise, and vertical-pack unit
tests
- [x] pre-push changed-surface verification
- [x] CI: 39/39 checks passed
```

### PR Body

## Summary
- replace the Creem-prefixed Restaurant vertical-pack plan setting with `VERTICAL_PACK_PLAN_ID_RESTAURANT_AI_TEAM_MONTHLY`
- update Airwallex, legacy Creem catalog, routing, capability, fixtures, and the root environment example
- intentionally provide no fallback to the old environment variable

## Rollout
- the requester confirmed `VERTICAL_PACK_PLAN_ID_RESTAURANT_AI_TEAM_MONTHLY` is already populated with the same value as the old setting before rollout
- restart or redeploy `claw-interface` so Pods load the new environment variable

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] 242 targeted Airwallex, Creem enterprise, and vertical-pack unit tests
- [x] pre-push changed-surface verification
- [x] CI: 39/39 checks passed


---

## fix(agent-packs): repair environment projection rollout (#3455)

- **SHA**: `3c595fa3a14b76174c2f6f973baa24b10f3a51bc`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-20T07:21:59Z
- **PR**: #3455

### Commit Message

```
fix(agent-packs): repair environment projection rollout (#3455)

## Summary

- enable the reviewed Engine Pack runtime-asset lane in staging and
production for the same five catalog Pack IDs
- wire the Workspace receiver token and Engine admin token from
Vault-backed Kubernetes secrets
- accept Engine `partial_ready` responses and distinguish in-flight
partial builds from resource-class failures
- advance the V2 idempotency generation when a persisted Environment pin
is already confirmed dead, avoiding stale upload-ID conflicts during
rebuild
- add unit and deployment-contract coverage for the recovery path and
both overlays

## Live audit that motivated this change

- staging has all 9 active Engine Packs in the Workspace catalog, but
four of the five selected Packs retain failed Engine pins
- replaying those projections exposed two compatibility failures: stale
idempotency keys returned `409 idempotency_conflict`, and Engine
`partial_ready` responses were rejected by the Workspace schema
- production has 8 of 9 catalog records, no Pack Environment projections
in Engine, and the runtime-asset receiver is currently
disabled/unconfigured
- the latest production Agent Pack release packaged all 9 Engine Packs,
but every registration failed because the production Workspace receiver
token was absent

## Rollout prerequisites and order

1. Before deploying the production overlay, add
`AGENT_PACK_RUNTIME_ASSET_TOKEN` to `vault-claw-interface-env-secret`
and make it match the protected `ecap-agent-pack` production Environment
secret. The Deployment intentionally fails closed if the key is absent.
2. Create the missing Oura Ring WhatsApp production catalog record
through the formal Pack admin API; do not repair shared data directly in
the database.
3. Deploy this change to staging, run the companion Agent Pack
reconciliation workflow, and verify all five recorded pins are `ready`.
4. Only then deploy production and run production reconciliation.

Companion workflow: SerendipityOneInc/ecap-agent-pack#247.

## Validation

- `bash scripts/verify-py.sh`
- targeted Pack Environment, Pack Test Environment, and
deployment-wiring tests
- pre-commit hook suite
- `kubectl kustomize` for staging and production overlays
```

### PR Body

## Summary

- enable the reviewed Engine Pack runtime-asset lane in staging and production for the same five catalog Pack IDs
- wire the Workspace receiver token and Engine admin token from Vault-backed Kubernetes secrets
- accept Engine `partial_ready` responses and distinguish in-flight partial builds from resource-class failures
- advance the V2 idempotency generation when a persisted Environment pin is already confirmed dead, avoiding stale upload-ID conflicts during rebuild
- add unit and deployment-contract coverage for the recovery path and both overlays

## Live audit that motivated this change

- staging has all 9 active Engine Packs in the Workspace catalog, but four of the five selected Packs retain failed Engine pins
- replaying those projections exposed two compatibility failures: stale idempotency keys returned `409 idempotency_conflict`, and Engine `partial_ready` responses were rejected by the Workspace schema
- production has 8 of 9 catalog records, no Pack Environment projections in Engine, and the runtime-asset receiver is currently disabled/unconfigured
- the latest production Agent Pack release packaged all 9 Engine Packs, but every registration failed because the production Workspace receiver token was absent

## Rollout prerequisites and order

1. Before deploying the production overlay, add `AGENT_PACK_RUNTIME_ASSET_TOKEN` to `vault-claw-interface-env-secret` and make it match the protected `ecap-agent-pack` production Environment secret. The Deployment intentionally fails closed if the key is absent.
2. Create the missing Oura Ring WhatsApp production catalog record through the formal Pack admin API; do not repair shared data directly in the database.
3. Deploy this change to staging, run the companion Agent Pack reconciliation workflow, and verify all five recorded pins are `ready`.
4. Only then deploy production and run production reconciliation.

Companion workflow: SerendipityOneInc/ecap-agent-pack#247.

## Validation

- `bash scripts/verify-py.sh`
- targeted Pack Environment, Pack Test Environment, and deployment-wiring tests
- pre-commit hook suite
- `kubectl kustomize` for staging and production overlays


---

## fix(auth): branch signup bootstrap on install-capability runtime (#3423)

- **SHA**: `044636aa369cc0d97b09198382e2df4266898b33`
- **作者**: bill-srp
- **日期**: 2026-08-20T06:48:18Z
- **PR**: #3423

### Commit Message

```
fix(auth): branch signup bootstrap on install-capability runtime (#3423)

## Summary
- Signup bootstrap now branches on `capability.runtime === 'engine'`
instead of `capability.reason !== 'agents_v2_disabled'` when deciding
whether to provision a v1 computer (`web/app/src/lib/auth/manager.ts`).
- Parametrizes the pinned unit test over all three computer-runtime
reasons (`agents_v2_disabled`, `email_missing`,
`email_not_allowlisted`), each asserting `createComputer` is called.

## Root cause
`GET /agents/install-capability` returns `runtime: "computer"` for every
ineligible user, but signup bootstrap only treated `reason ===
'agents_v2_disabled'` as the computer case. Users with `email_missing` /
`email_not_allowlisted` (production, `AGENTS_V2_ENABLED=true`, not
allowlisted) were treated as engine users at signup — no v1 computer
created — while every other consumer of the capability (BFF install
route, claw-settings tab, landing hire flow) branches on `runtime` and
later routes those same users to the v1 computer install path, which
then waits on a computer that never exists. Branching on `runtime` makes
signup provisioning agree with install-time routing.

## Test plan
- [x] `pnpm exec vitest run tests/unit/lib/auth/manager.unit.spec.ts` —
87/87 passed
- [x] `bash scripts/verify-web.sh --no-test` on the touched files —
guards + tsc + eslint clean
- [ ] CI (`web-quality` + `web-build-check`) green on the
merged-with-main combination
```

### PR Body

## Summary
- Signup bootstrap now branches on `capability.runtime === 'engine'` instead of `capability.reason !== 'agents_v2_disabled'` when deciding whether to provision a v1 computer (`web/app/src/lib/auth/manager.ts`).
- Parametrizes the pinned unit test over all three computer-runtime reasons (`agents_v2_disabled`, `email_missing`, `email_not_allowlisted`), each asserting `createComputer` is called.

## Root cause
`GET /agents/install-capability` returns `runtime: "computer"` for every ineligible user, but signup bootstrap only treated `reason === 'agents_v2_disabled'` as the computer case. Users with `email_missing` / `email_not_allowlisted` (production, `AGENTS_V2_ENABLED=true`, not allowlisted) were treated as engine users at signup — no v1 computer created — while every other consumer of the capability (BFF install route, claw-settings tab, landing hire flow) branches on `runtime` and later routes those same users to the v1 computer install path, which then waits on a computer that never exists. Branching on `runtime` makes signup provisioning agree with install-time routing.

## Test plan
- [x] `pnpm exec vitest run tests/unit/lib/auth/manager.unit.spec.ts` — 87/87 passed
- [x] `bash scripts/verify-web.sh --no-test` on the touched files — guards + tsc + eslint clean
- [ ] CI (`web-quality` + `web-build-check`) green on the merged-with-main combination


---

## fix(billing): tolerate missing request_id on retrieved Airwallex topup checkouts (#3453)

- **SHA**: `3b8e1eae308eec0e5a36192881100f1349f86e57`
- **作者**: tim-srp
- **日期**: 2026-08-20T04:23:08Z
- **PR**: #3453

### Commit Message

```
fix(billing): tolerate missing request_id on retrieved Airwallex topup checkouts (#3453)

## Summary

Staging end-to-end testing found completed top-up payments stuck in
`pending` with `billing.card_topup_checkout.order_conflict` on confirm.

**Root cause (sandbox-verified)**: Airwallex's checkout **retrieval**
endpoint omits `request_id` (creation responses carry it, retrievals
return `null`). Both `confirm_card_topup_order` and
`settle_airwallex_topup_checkout` required `checkout.request_id ==
local_order_id`, so every completed top-up was rejected with a conflict
— via the success-page confirm poll and via the webhook settlement path
alike.

## Changes

- Tolerate a missing `request_id` on retrieved checkouts in both
validation sites; only a present-but-mismatched value is rejected.
Ownership authority stays with the metadata `uid`/`local_order_id`
binding (still strictly validated).
- Tests: confirm settles when the retrieved checkout omits `request_id`;
settlement likewise accepts it; existing present-mismatch conflict cases
unchanged.

## Evidence

- Staging order `ORD-20260820-AE2C9987` (status `pending`) → retrieved
checkout: `request_id: null`, all other identity fields match → conflict
reproduced from logs.
- Local: 46 targeted tests pass; `verify-py` green.

## Note

A separate staging issue (all Airwallex webhook deliveries rejected with
`invalid_payload` — signature verifies, envelope parse fails) is under
investigation in parallel and is not fixed by this PR.
```

### PR Body

## Summary

Staging end-to-end testing found completed top-up payments stuck in `pending` with `billing.card_topup_checkout.order_conflict` on confirm.

**Root cause (sandbox-verified)**: Airwallex's checkout **retrieval** endpoint omits `request_id` (creation responses carry it, retrievals return `null`). Both `confirm_card_topup_order` and `settle_airwallex_topup_checkout` required `checkout.request_id == local_order_id`, so every completed top-up was rejected with a conflict — via the success-page confirm poll and via the webhook settlement path alike.

## Changes

- Tolerate a missing `request_id` on retrieved checkouts in both validation sites; only a present-but-mismatched value is rejected. Ownership authority stays with the metadata `uid`/`local_order_id` binding (still strictly validated).
- Tests: confirm settles when the retrieved checkout omits `request_id`; settlement likewise accepts it; existing present-mismatch conflict cases unchanged.

## Evidence

- Staging order `ORD-20260820-AE2C9987` (status `pending`) → retrieved checkout: `request_id: null`, all other identity fields match → conflict reproduced from logs.
- Local: 46 targeted tests pass; `verify-py` green.

## Note

A separate staging issue (all Airwallex webhook deliveries rejected with `invalid_payload` — signature verifies, envelope parse fails) is under investigation in parallel and is not fixed by this PR.


---

## fix(billing): stamp bg_granted_at on settled Airwallex trial entitlements (#3451)

- **SHA**: `e09663116f672a5cd53c16512b6c91f82b1335ec`
- **作者**: tim-srp
- **日期**: 2026-08-20T04:09:31Z
- **PR**: #3451

### Commit Message

```
fix(billing): stamp bg_granted_at on settled Airwallex trial entitlements (#3451)

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary

Airwallex trial settlement records the entitlement as `ACTIVE` with the
trial credits, but never stamps `bg_granted_at` — the timestamp that
other grant flows (first payment, renewal, subscription code) write
**after** billing-gateway confirms the credits landed.

Missing stamp breaks two consumers:
- Order API `entitlement_granted` flag — `orders.py` treats
`bg_granted_at` as the proof the grant landed, so trial orders look
never-granted.
- Credit-reset scans (`credit_reset_repo.py`) that key off
`bg_granted_at` to know when trial credits started.

## Root cause

`record_trial_entitlement` had no `bg_granted_at` parameter and
`settle_airwallex_trial_subscription` wrote the entitlement only once,
before the billing-gateway grant — unlike the paid-card first payment
flow which writes `ACTIVE + bg_granted_at` after the grant succeeds.

## Change

- `record_trial_entitlement` gains an optional `bg_granted_at` parameter
(same pattern as `record_payment_entitlement` /
`record_subscription_code_entitlement`).
- `settle_airwallex_trial_subscription` re-records the entitlement with
`bg_granted_at=now` after the billing-gateway grant succeeds, and skips
the re-stamp when a replay already carries the timestamp (idempotent).

## Test plan

- [x] `test_settles_trial_when_all_facts_match` — asserts the second
`record_trial_entitlement` call carries `bg_granted_at`.
- [x] `test_replayed_trial_preserves_existing_credits` — asserts the
backfill keeps the reused credits (`777`) and adds the stamp.
- [x] New `test_replayed_trial_skips_grant_stamp_when_already_set` — a
replay that already has `bg_granted_at` is not re-stamped.
- [x] `verify-py` (ruff + pyright + import-linter) passes;
pre-commit/pre-push hooks pass.

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary

Airwallex trial settlement records the entitlement as `ACTIVE` with the trial credits, but never stamps `bg_granted_at` — the timestamp that other grant flows (first payment, renewal, subscription code) write **after** billing-gateway confirms the credits landed.

Missing stamp breaks two consumers:
- Order API `entitlement_granted` flag — `orders.py` treats `bg_granted_at` as the proof the grant landed, so trial orders look never-granted.
- Credit-reset scans (`credit_reset_repo.py`) that key off `bg_granted_at` to know when trial credits started.

## Root cause

`record_trial_entitlement` had no `bg_granted_at` parameter and `settle_airwallex_trial_subscription` wrote the entitlement only once, before the billing-gateway grant — unlike the paid-card first payment flow which writes `ACTIVE + bg_granted_at` after the grant succeeds.

## Change

- `record_trial_entitlement` gains an optional `bg_granted_at` parameter (same pattern as `record_payment_entitlement` / `record_subscription_code_entitlement`).
- `settle_airwallex_trial_subscription` re-records the entitlement with `bg_granted_at=now` after the billing-gateway grant succeeds, and skips the re-stamp when a replay already carries the timestamp (idempotent).

## Test plan

- [x] `test_settles_trial_when_all_facts_match` — asserts the second `record_trial_entitlement` call carries `bg_granted_at`.
- [x] `test_replayed_trial_preserves_existing_credits` — asserts the backfill keeps the reused credits (`777`) and adds the stamp.
- [x] New `test_replayed_trial_skips_grant_stamp_when_already_set` — a replay that already has `bg_granted_at` is not re-stamped.
- [x] `verify-py` (ruff + pyright + import-linter) passes; pre-commit/pre-push hooks pass.


---

## fix(billing): send invoice_data on Airwallex PAYMENT topup checkouts (#3452)

- **SHA**: `c276c08a17a115c34fef00039fbdb4565166bad8`
- **作者**: tim-srp
- **日期**: 2026-08-20T04:05:15Z
- **PR**: #3452

### Commit Message

```
fix(billing): send invoice_data on Airwallex PAYMENT topup checkouts (#3452)

## Summary

Staging verification of #3449 found that Airwallex rejects PAYMENT-mode
`billing_checkouts/create` without `invoice_data`:

```json
{"code":"validation_error","message":"invoice_data must be provided for PAYMENT mode in checkout.","source":"invoice_data"}
```

This closes the [VERIFY sandbox] request-shape open item in the design
spec.

## Changes

- `app/schema/airwallex.py` — add `AirwallexInvoiceData`
(`days_until_due` / `default_tax_percent` / `due_at` / `memo` /
`metadata`, all optional per the [Airwallex Billing Checkouts
API](https://www.airwallex.com/docs/api/billing/billing_checkouts/retrieve#2));
`AirwallexCreateCheckoutRequest` gains `invoice_data` and the mode
validator now **requires** it for PAYMENT mode (alongside the existing
no-`subscription_data` rule)
- `app/services/billing_v2/card_topup_checkout.py` — top-up checkout
creation sends `invoice_data=AirwallexInvoiceData(days_until_due=0)`
(invoice due immediately on completion)
- Spec + tests updated (schema PAYMENT-mode rules, checkout request
assertion)

## Verification

- Empirical sandbox repro inside the staging pod: without `invoice_data`
→ 400 `validation_error`; with `invoice_data={days_until_due: 0}` →
**201**, `bco_...` checkout with hosted URL on
`checkout.sandbox.airwallex.com` (already in the official-host
allowlist)
- `pytest -k "airwallex or topup or card"` → 688 passed; `bash
scripts/verify-py.sh` → all checks passed

## Remaining open item

`payment_intent.succeeded` event shape for PAYMENT-mode checkouts (the
completion-event side) — verifiable end-to-end once this fix is on
staging and a real top-up payment is completed with a sandbox test card.
```

### PR Body

## Summary

Staging verification of #3449 found that Airwallex rejects PAYMENT-mode `billing_checkouts/create` without `invoice_data`:

```json
{"code":"validation_error","message":"invoice_data must be provided for PAYMENT mode in checkout.","source":"invoice_data"}
```

This closes the [VERIFY sandbox] request-shape open item in the design spec.

## Changes

- `app/schema/airwallex.py` — add `AirwallexInvoiceData` (`days_until_due` / `default_tax_percent` / `due_at` / `memo` / `metadata`, all optional per the [Airwallex Billing Checkouts API](https://www.airwallex.com/docs/api/billing/billing_checkouts/retrieve#2)); `AirwallexCreateCheckoutRequest` gains `invoice_data` and the mode validator now **requires** it for PAYMENT mode (alongside the existing no-`subscription_data` rule)
- `app/services/billing_v2/card_topup_checkout.py` — top-up checkout creation sends `invoice_data=AirwallexInvoiceData(days_until_due=0)` (invoice due immediately on completion)
- Spec + tests updated (schema PAYMENT-mode rules, checkout request assertion)

## Verification

- Empirical sandbox repro inside the staging pod: without `invoice_data` → 400 `validation_error`; with `invoice_data={days_until_due: 0}` → **201**, `bco_...` checkout with hosted URL on `checkout.sandbox.airwallex.com` (already in the official-host allowlist)
- `pytest -k "airwallex or topup or card"` → 688 passed; `bash scripts/verify-py.sh` → all checks passed

## Remaining open item

`payment_intent.succeeded` event shape for PAYMENT-mode checkouts (the completion-event side) — verifiable end-to-end once this fix is on staging and a real top-up payment is completed with a sandbox test card.


---

## feat(marketing): add contact sales page (#3430)

- **SHA**: `4e493efabfa1306ae5977e30aebdd353fedd0ae1`
- **作者**: shana-srp
- **日期**: 2026-08-20T03:09:28Z
- **PR**: #3430

### Commit Message

```
feat(marketing): add contact sales page (#3430)

## Linear

No linked issue.

## Summary

- add the localized Contact Sales route and contact form client
- register `/contact` with public SEO and marketing-route locale
handling
- keep the route feature-gated until the Contact page is enabled

## Test plan

- [x] `bash scripts/verify-web.sh --no-test`
- [x] Contact unit tests: 2 files / 4 tests passed
- [x] TypeScript passed
- [x] ESLint passed

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Linear

No linked issue.

## Summary

- add the localized Contact Sales route and contact form client
- register `/contact` with public SEO and marketing-route locale handling
- keep the route feature-gated until the Contact page is enabled

## Test plan

- [x] `bash scripts/verify-web.sh --no-test`
- [x] Contact unit tests: 2 files / 4 tests passed
- [x] TypeScript passed
- [x] ESLint passed


---

## fix(billing): declare trial window on Airwallex trial checkout creation (#3450)

- **SHA**: `2489fd13c080f809d7b5c9dc66cc52e0c54ca75a`
- **作者**: tim-srp
- **日期**: 2026-08-20T02:35:46Z
- **PR**: #3450

### Commit Message

```
fix(billing): declare trial window on Airwallex trial checkout creation (#3450)

## Problem

生产环境通过 free trial 订阅年度 Starter，Airwallex 端**立即扣费 200 USD**（预期 trial
不应扣费）。Issue: #3448

## Root cause

`create_card_checkout` 创建 Airwallex Billing Checkout 时只传了 trial 价格
id（`pri_uspd5s6n8hlgn9vy366`），没有把 trial 窗口传给 provider：

```python
subscription_data=AirwallexSubscriptionData(duration=_subscription_duration(intent.billing_cycle))
```

Airwallex 的 trial 语义完全由 checkout
请求决定（`subscription_data.trial_ends_at`），trial 价格本身只是一个普通的 200
USD/年预付费价格。因此订阅创建后直接进入付费周期并扣费。

生产环境证据（uid 7495857210153504768）：
- checkout `bco_uspdfkhxhhlhq51leki`：`subscription_data` 无
`trial_ends_at`
- subscription `sub_uspd67vdnhlhq5qk662`：`duration: {period: 0,
period_unit: "DAY"}`
- invoice `inv_uspd67vdnhlhq5qkx6c`：`total_amount:
200.0`，`payment_status: PAID`

业务层随后凭本地 `order.is_trial` 把订阅投影为 trialing 并发放 1000 trial credits，造成「被扣费
+ 拿到 trial credits」的双重伤害。

Design spec `2026-08-18-airwallex-subscription-channel-design.md` 第 190
行明确要求创建请求带 `trial_ends_at`，这是实现遗漏。

## Fix

当 intent 是 Starter trial 时，在 checkout 创建请求中声明 provider-managed trial
窗口（`now + AIRWALLEX_TRIAL_DURATION_DAYS`，7 天，与 Stripe/Antom trial 时长一致）：

```python
subscription_data = AirwallexSubscriptionData(
    trial_ends_at=trial_ends_at,
    duration=_subscription_duration(intent.billing_cycle),
)
```

新增设置 `AIRWALLEX_TRIAL_DURATION_DAYS =
7`（`app/schema/airwallex_settings.py`）。

非 trial 路径不变（`trial_ends_at` 为 `None`）。升级路径不受影响（trial 资格校验强制
`new_subscription` intent）。

## Tests

- `test_trial_checkout_uses_server_selected_trial_product`：新增断言 trial
checkout 请求携带 `trial_ends_at == now + 7 days`（patch `time.time` 固定时间）
- 非 trial 主路径新增断言 `trial_ends_at is None`
- 全套 Airwallex + card checkout 测试 449 passed

## 后续（不在本 PR 范围）

- #3448 中已扣费的订单需要人工退款处理
- 上线后需在 staging/production 各验证一次 trial checkout 全流程（sandbox 优先）

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Problem

生产环境通过 free trial 订阅年度 Starter，Airwallex 端**立即扣费 200 USD**（预期 trial 不应扣费）。Issue: #3448

## Root cause

`create_card_checkout` 创建 Airwallex Billing Checkout 时只传了 trial 价格 id（`pri_uspd5s6n8hlgn9vy366`），没有把 trial 窗口传给 provider：

```python
subscription_data=AirwallexSubscriptionData(duration=_subscription_duration(intent.billing_cycle))
```

Airwallex 的 trial 语义完全由 checkout 请求决定（`subscription_data.trial_ends_at`），trial 价格本身只是一个普通的 200 USD/年预付费价格。因此订阅创建后直接进入付费周期并扣费。

生产环境证据（uid 7495857210153504768）：
- checkout `bco_uspdfkhxhhlhq51leki`：`subscription_data` 无 `trial_ends_at`
- subscription `sub_uspd67vdnhlhq5qk662`：`duration: {period: 0, period_unit: "DAY"}`
- invoice `inv_uspd67vdnhlhq5qkx6c`：`total_amount: 200.0`，`payment_status: PAID`

业务层随后凭本地 `order.is_trial` 把订阅投影为 trialing 并发放 1000 trial credits，造成「被扣费 + 拿到 trial credits」的双重伤害。

Design spec `2026-08-18-airwallex-subscription-channel-design.md` 第 190 行明确要求创建请求带 `trial_ends_at`，这是实现遗漏。

## Fix

当 intent 是 Starter trial 时，在 checkout 创建请求中声明 provider-managed trial 窗口（`now + AIRWALLEX_TRIAL_DURATION_DAYS`，7 天，与 Stripe/Antom trial 时长一致）：

```python
subscription_data = AirwallexSubscriptionData(
    trial_ends_at=trial_ends_at,
    duration=_subscription_duration(intent.billing_cycle),
)
```

新增设置 `AIRWALLEX_TRIAL_DURATION_DAYS = 7`（`app/schema/airwallex_settings.py`）。

非 trial 路径不变（`trial_ends_at` 为 `None`）。升级路径不受影响（trial 资格校验强制 `new_subscription` intent）。

## Tests

- `test_trial_checkout_uses_server_selected_trial_product`：新增断言 trial checkout 请求携带 `trial_ends_at == now + 7 days`（patch `time.time` 固定时间）
- 非 trial 主路径新增断言 `trial_ends_at is None`
- 全套 Airwallex + card checkout 测试 449 passed

## 后续（不在本 PR 范围）

- #3448 中已扣费的订单需要人工退款处理
- 上线后需在 staging/production 各验证一次 trial checkout 全流程（sandbox 优先）


---

## feat(billing): move card top-up checkout to Airwallex and remove Creem portal (#3449)

- **SHA**: `15ac660120fbbf26e53aa8c950638423b1d80a53`
- **作者**: tim-srp
- **日期**: 2026-08-20T02:34:12Z
- **PR**: #3449

### Commit Message

```
feat(billing): move card top-up checkout to Airwallex and remove Creem portal (#3449)

## Summary

Completes the card channel migration to Airwallex: one-time top-up
checkouts now run on Airwallex PAYMENT mode, and the Creem top-up stack
+ customer portal are removed (no Creem users exist).

Design spec:
`docs/superpowers/specs/2026-08-19-airwallex-topup-design.md`

## Changes

**Airwallex top-up stack (backend)**
- `AirwallexCreateCheckoutRequest.mode` widened to `SUBSCRIPTION |
PAYMENT`; PAYMENT rejects `subscription_data`
- `AirwallexCatalog.resolve_topup(credits)` + top-up config completeness
(`airwallex_topup_configuration_complete`) and availability gate
(`airwallex_topup_checkout_enabled`)
- New `airwallex/topup_payment.py`: settles a PAYMENT checkout against
its local order, grants TOPUP_CREDITS once via billing gateway
(idempotent entitlement replay), operation key
`airwallex:checkout:<id>:topup`
- `payment_events.py`: `payment_intent.succeeded` without a
`subscription_id` settles top-up orders instead of raising
`event_not_supported`
- `card_topup_checkout.py` rewritten as Airwallex-only (create PAYMENT
checkout, confirm via `get_billing_checkout` → settle; replay via
`is_official_airwallex_checkout_url`)
- `card_topup_checkout_repo.py` provider filters now `airwallex`;
capability `topup.card_available` driven by the Airwallex top-up gate

**Creem removal**
- Deleted `creem/topup_payment.py`, `creem/topup_loss.py`,
`creem/portal.py`; top-up branches in `creem/lifecycle.py`;
`resolve_topup`/top-up config in creem catalog/config;
`CREEM_PRODUCT_ID_TOPUP_*` settings; portal schemas and client surface
(`create_customer_billing_link` etc.)
- `POST /billing/creem-customer-portal` route removed; frontend
`createCreemCustomerPortal` + InvoiceHistory card-portal branch removed
(card users no longer see Edit billing / View billing — Airwallex has no
customer portal); mock-backend portal mock removed

**Frontend top-up flow unchanged** — contracts preserved: `{order_id,
checkout_url}` response, `?channel=card&local_order_id=...&type=topup`
success URL, confirm `status + entitlement_granted`, capability
`topup.card_available`.

## Not in this PR (follow-ups)

- **Refund/dispute revoke** (top-up loss) — deferred until the Airwallex
refund event shape is sandbox-verified
- **Sandbox verification of the PAYMENT-mode event shape** —
`payment_intent.succeeded` handling is reused from the subscription
channel; the top-up branch validates the retrieved checkout, so only
event-name/field extraction would change
- **Ops**: create the three one-time payment prices in the Airwallex
dashboard (sandbox + prod) and set
`AIRWALLEX_PRICE_ID_TOPUP_1000/5000/10000`
- Creem subscription/vertical-pack legacy teardown (separate work)

## Local checks

- `bash scripts/verify-py.sh` — passed (ruff, ruff-format, pyright,
import-linter)
- Backend targeted tests: billing/airwallex/creem/card/topup suites —
all passed
- Frontend: vitest 9009 passed, eslint passed, changed-file tsc clean
- Note: local full `tsc` and full pytest runs hit pre-existing
environment issues (stale `node_modules` codemirror resolution identical
to the main checkout; `test_stripe_billing_v2.py` segfaults at
collection in the main checkout too). CI's fresh install should be
clean.

---------

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Body

## Summary

Completes the card channel migration to Airwallex: one-time top-up checkouts now run on Airwallex PAYMENT mode, and the Creem top-up stack + customer portal are removed (no Creem users exist).

Design spec: `docs/superpowers/specs/2026-08-19-airwallex-topup-design.md`

## Changes

**Airwallex top-up stack (backend)**
- `AirwallexCreateCheckoutRequest.mode` widened to `SUBSCRIPTION | PAYMENT`; PAYMENT rejects `subscription_data`
- `AirwallexCatalog.resolve_topup(credits)` + top-up config completeness (`airwallex_topup_configuration_complete`) and availability gate (`airwallex_topup_checkout_enabled`)
- New `airwallex/topup_payment.py`: settles a PAYMENT checkout against its local order, grants TOPUP_CREDITS once via billing gateway (idempotent entitlement replay), operation key `airwallex:checkout:<id>:topup`
- `payment_events.py`: `payment_intent.succeeded` without a `subscription_id` settles top-up orders instead of raising `event_not_supported`
- `card_topup_checkout.py` rewritten as Airwallex-only (create PAYMENT checkout, confirm via `get_billing_checkout` → settle; replay via `is_official_airwallex_checkout_url`)
- `card_topup_checkout_repo.py` provider filters now `airwallex`; capability `topup.card_available` driven by the Airwallex top-up gate

**Creem removal**
- Deleted `creem/topup_payment.py`, `creem/topup_loss.py`, `creem/portal.py`; top-up branches in `creem/lifecycle.py`; `resolve_topup`/top-up config in creem catalog/config; `CREEM_PRODUCT_ID_TOPUP_*` settings; portal schemas and client surface (`create_customer_billing_link` etc.)
- `POST /billing/creem-customer-portal` route removed; frontend `createCreemCustomerPortal` + InvoiceHistory card-portal branch removed (card users no longer see Edit billing / View billing — Airwallex has no customer portal); mock-backend portal mock removed

**Frontend top-up flow unchanged** — contracts preserved: `{order_id, checkout_url}` response, `?channel=card&local_order_id=...&type=topup` success URL, confirm `status + entitlement_granted`, capability `topup.card_available`.

## Not in this PR (follow-ups)

- **Refund/dispute revoke** (top-up loss) — deferred until the Airwallex refund event shape is sandbox-verified
- **Sandbox verification of the PAYMENT-mode event shape** — `payment_intent.succeeded` handling is reused from the subscription channel; the top-up branch validates the retrieved checkout, so only event-name/field extraction would change
- **Ops**: create the three one-time payment prices in the Airwallex dashboard (sandbox + prod) and set `AIRWALLEX_PRICE_ID_TOPUP_1000/5000/10000`
- Creem subscription/vertical-pack legacy teardown (separate work)

## Local checks

- `bash scripts/verify-py.sh` — passed (ruff, ruff-format, pyright, import-linter)
- Backend targeted tests: billing/airwallex/creem/card/topup suites — all passed
- Frontend: vitest 9009 passed, eslint passed, changed-file tsc clean
- Note: local full `tsc` and full pytest runs hit pre-existing environment issues (stale `node_modules` codemirror resolution identical to the main checkout; `test_stripe_billing_v2.py` segfaults at collection in the main checkout too). CI's fresh install should be clean.


---
