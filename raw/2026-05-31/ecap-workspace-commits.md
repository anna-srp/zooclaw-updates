# ecap-workspace - 2026-05-31

共 5 条 commits

---

## SHA: a27fffc82d241b8468d5302d3112fd314914e052

**作者**: kaka-srp

**日期**: 2026-05-31T10:58:01Z

**完整 Commit Message**:

```
refactor(billing): finish v2 backfill cutover (#2136)

## Linear

https://linear.app/srpone/issue/ECA-842/billing-v2-backfill-cutover

## Summary

- Add one-time Billing v2 backfill tooling with dry-run/write modes,
blockers, audit output, and the manual index/cutover runbook.
- Harden provider agreement handling for unknown-environment backfilled
rows, terminal webhook cleanup, legacy account projection sync from
current v2 entitlements, and canceling-state projection preservation.
- Preserve subscription credits on v2 payment orders and harden web
checkout-return confirmation with in-flight dedupe and scoped transient
retry.
- Document the v2 cutover checklist and post-stability legacy cleanup
path.

## Review Fixes

- Dry-run now also projects order-backed entitlements, so `--dry-run
--fail-on-blockers` can surface entitlement-level blockers before write
mode.
- Legacy account projection now restores `cancel_at_period_end=true`
after `transition_to_active()` when the current v2 agreement is already
canceling.
- Web payment confirmation only retries retryable API failures (`5xx`,
`408`, `429`, or transport failures); permanent `4xx` failures fail fast
with a single failure event.
- Stripe replacement cleanup only cancels a previous current
subscription when it is in the same environment or the old backfilled
agreement has `environment=unknown`.

## Validation

- `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check
scripts/backfill_billing_v2.py scripts/billing_v2_backfill.py
scripts/billing_v2_backfill_core.py
scripts/billing_v2_backfill_legacy.py
scripts/billing_v2_backfill_orders.py
scripts/billing_v2_backfill_subscriptions.py
app/services/billing_v2/subscription_agreements.py
app/services/billing_v2/fulfillment.py app/services/antom/billing_v2.py
app/services/antom/billing_v2_records.py
app/services/stripe/billing_v2.py
app/services/stripe/billing_v2_records.py
app/services/stripe/billing_v2_replacements.py
tests/unit/test_billing_v2_backfill.py
tests/unit/test_billing_v2_subscription_agreements.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_antom_billing_v2.py
tests/unit/test_stripe_billing_v2.py`
- `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_v2_backfill.py
tests/unit/test_billing_v2_subscription_agreements.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_antom_billing_v2.py
tests/unit/test_antom_billing_v2_adapter.py
tests/unit/test_stripe_billing_v2.py
tests/unit/test_stripe_billing_v2_adapter.py
tests/unit/test_billing_v2_subscription_current.py
tests/unit/test_billing_v2_expiry.py tests/unit/test_apple_billing_v2.py
tests/unit/test_orders_endpoints.py -q`
- `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright
scripts/backfill_billing_v2.py scripts/billing_v2_backfill.py
scripts/billing_v2_backfill_core.py
scripts/billing_v2_backfill_legacy.py
scripts/billing_v2_backfill_orders.py
scripts/billing_v2_backfill_subscriptions.py
app/services/billing_v2/subscription_agreements.py
app/services/billing_v2/fulfillment.py app/services/antom/billing_v2.py
app/services/antom/billing_v2_records.py
app/services/stripe/billing_v2.py
app/services/stripe/billing_v2_records.py
app/services/stripe/billing_v2_replacements.py
tests/unit/test_billing_v2_backfill.py
tests/unit/test_billing_v2_subscription_agreements.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_antom_billing_v2.py
tests/unit/test_stripe_billing_v2.py`
- `pnpm --dir web/app exec eslint
src/lib/payment/handle-payment-success.ts
tests/unit/lib/payment/handle-payment-success.unit.spec.ts --quiet`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/lib/payment/handle-payment-success.unit.spec.ts`
- `git diff --check`
- After review fix: `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_v2_backfill.py
tests/unit/test_billing_v2_fulfillment.py -q`
- After review fix: `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_v2_backfill.py
tests/unit/test_billing_v2_subscription_agreements.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_antom_billing_v2.py
tests/unit/test_antom_billing_v2_adapter.py
tests/unit/test_stripe_billing_v2.py
tests/unit/test_stripe_billing_v2_adapter.py
tests/unit/test_billing_v2_subscription_current.py
tests/unit/test_billing_v2_expiry.py tests/unit/test_apple_billing_v2.py
tests/unit/test_orders_endpoints.py -q`
- After review fix: `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff format --check .`
- After review fix: `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check
scripts/billing_v2_backfill_orders.py
tests/unit/test_billing_v2_backfill.py
app/services/billing_v2/fulfillment.py
tests/unit/test_billing_v2_fulfillment.py
app/services/stripe/billing_v2_replacements.py
tests/unit/test_stripe_billing_v2.py`
- After review fix: `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright
scripts/billing_v2_backfill_orders.py
tests/unit/test_billing_v2_backfill.py
app/services/billing_v2/fulfillment.py
tests/unit/test_billing_v2_fulfillment.py
app/services/stripe/billing_v2_replacements.py
tests/unit/test_stripe_billing_v2.py`
- After review fix: `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_stripe_billing_v2.py -q`
- After review fix: `pnpm --dir web/app exec eslint
src/lib/api/backend.ts src/lib/payment/handle-payment-success.ts
tests/unit/lib/payment/handle-payment-success.unit.spec.ts --quiet`
- After review fix: `pnpm --dir web/app exec vitest run --config
./vitest.config.mts
tests/unit/lib/payment/handle-payment-success.unit.spec.ts`
- After review fix: `pnpm --dir web/app exec tsc --noEmit`

## Staging Verification

Current local `.env` points to staging. Staging dry-run passed with
`--fail-on-blockers` and conflicts `{}`:

- Sources: accounts 220, legacy orders 518, subscription-code
activations 7.
- Targets: billing profiles 35, subscription agreements 21, payment
orders 133, entitlements 146.
- Skips include covered cron renewals 16, terminal users without
unresolved state 185, terminal-user legacy orders 182, order-backed
entries without granted entitlement 3, expired subscription-code
activations 2.
- Manual migrated-flow validation completed for Stripe and Antom:
subscription, upgrade, downgrade, cancel, renew, canceling top-up,
active top-up, and billing order display.
- Apple still needs iOS sandbox beta validation before production
cutover; provider notification/claim paths are covered by code/unit
tests in this PR stack.

## Cutover Notes

- This PR does not automatically run backfill or create indexes at
service startup.
- Before production cutover, rerun the same read-only distribution check
and dry-run against production config, then create indexes manually and
only run write mode after blockers are zero.
- Enable v2 read/write flags together after backfill, monitor, and clean
legacy paths only after a stable-run window.
```

**PR #2136 Body**:

```
## Linear

https://linear.app/srpone/issue/ECA-842/billing-v2-backfill-cutover

## Summary

- Add one-time Billing v2 backfill tooling with dry-run/write modes, blockers, audit output, and the manual index/cutover runbook.
- Harden provider agreement handling for unknown-environment backfilled rows, terminal webhook cleanup, legacy account projection sync from current v2 entitlements, and canceling-state projection preservation.
- Preserve subscription credits on v2 payment orders and harden web checkout-return confirmation with in-flight dedupe and scoped transient retry.
- Document the v2 cutover checklist and post-stability legacy cleanup path.

## Review Fixes

- Dry-run now also projects order-backed entitlements, so `--dry-run --fail-on-blockers` can surface entitlement-level blockers before write mode.
- Legacy account projection now restores `cancel_at_period_end=true` after `transition_to_active()` when the current v2 agreement is already canceling.
- Web payment confirmation only retries retryable API failures (`5xx`, `408`, `429`, or transport failures); permanent `4xx` failures fail fast with a single failure event.
- Stripe replacement cleanup only cancels a previous current subscription when it is in the same environment or the old backfilled agreement has `environment=unknown`.

## Validation

- `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check scripts/backfill_billing_v2.py scripts/billing_v2_backfill.py scripts/billing_v2_backfill_core.py scripts/billing_v2_backfill_legacy.py scripts/billing_v2_backfill_orders.py scripts/billing_v2_backfill_subscriptions.py app/services/billing_v2/subscription_agreements.py app/services/billing_v2/fulfillment.py app/services/antom/billing_v2.py app/services/antom/billing_v2_records.py app/services/stripe/billing_v2.py app/services/stripe/billing_v2_records.py app/services/stripe/billing_v2_replacements.py tests/unit/test_billing_v2_backfill.py tests/unit/test_billing_v2_subscription_agreements.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_antom_billing_v2.py tests/unit/test_stripe_billing_v2.py`
- `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_v2_backfill.py tests/unit/test_billing_v2_subscription_agreements.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_antom_billing_v2.py tests/unit/test_antom_billing_v2_adapter.py tests/unit/test_stripe_billing_v2.py tests/unit/test_stripe_billing_v2_adapter.py tests/unit/test_billing_v2_subscription_current.py tests/unit/test_billing_v2_expiry.py tests/unit/test_apple_billing_v2.py tests/unit/test_orders_endpoints.py -q`
- `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright scripts/backfill_billing_v2.py scripts/billing_v2_backfill.py scripts/billing_v2_backfill_core.py scripts/billing_v2_backfill_legacy.py scripts/billing_v2_backfill_orders.py scripts/billing_v2_backfill_subscriptions.py app/services/billing_v2/subscription_agreements.py app/services/billing_v2/fulfillment.py app/services/antom/billing_v2.py app/services/antom/billing_v2_records.py app/services/stripe/billing_v2.py app/services/stripe/billing_v2_records.py app/services/stripe/billing_v2_replacements.py tests/unit/test_billing_v2_backfill.py tests/unit/test_billing_v2_subscription_agreements.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_antom_billing_v2.py tests/unit/test_stripe_billing_v2.py`
- `pnpm --dir web/app exec eslint src/lib/payment/handle-payment-success.ts tests/unit/lib/payment/handle-payment-success.unit.spec.ts --quiet`
- `pnpm --dir web/app exec tsc --noEmit`
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/lib/payment/handle-payment-success.unit.spec.ts`
- `git diff --check`
- After review fix: `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_v2_backfill.py tests/unit/test_billing_v2_fulfillment.py -q`
- After review fix: `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_v2_backfill.py tests/unit/test_billing_v2_subscription_agreements.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_antom_billing_v2.py tests/unit/test_antom_billing_v2_adapter.py tests/unit/test_stripe_billing_v2.py tests/unit/test_stripe_billing_v2_adapter.py tests/unit/test_billing_v2_subscription_current.py tests/unit/test_billing_v2_expiry.py tests/unit/test_apple_billing_v2.py tests/unit/test_orders_endpoints.py -q`
- After review fix: `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff format --check .`
- After review fix: `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check scripts/billing_v2_backfill_orders.py tests/unit/test_billing_v2_backfill.py app/services/billing_v2/fulfillment.py tests/unit/test_billing_v2_fulfillment.py app/services/stripe/billing_v2_replacements.py tests/unit/test_stripe_billing_v2.py`
- After review fix: `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright scripts/billing_v2_backfill_orders.py tests/unit/test_billing_v2_backfill.py app/services/billing_v2/fulfillment.py tests/unit/test_billing_v2_fulfillment.py app/services/stripe/billing_v2_replacements.py tests/unit/test_stripe_billing_v2.py`
- After review fix: `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_stripe_billing_v2.py -q`
- After review fix: `pnpm --dir web/app exec eslint src/lib/api/backend.ts src/lib/payment/handle-payment-success.ts tests/unit/lib/payment/handle-payment-success.unit.spec.ts --quiet`
- After review fix: `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/lib/payment/handle-payment-success.unit.spec.ts`
- After review fix: `pnpm --dir web/app exec tsc --noEmit`

## Staging Verification

Current local `.env` points to staging. Staging dry-run passed with `--fail-on-blockers` and conflicts `{}`:

- Sources: accounts 220, legacy orders 518, subscription-code activations 7.
- Targets: billing profiles 35, subscription agreements 21, payment orders 133, entitlements 146.
- Skips include covered cron renewals 16, terminal users without unresolved state 185, terminal-user legacy orders 182, order-backed entries without granted entitlement 3, expired subscription-code activations 2.
- Manual migrated-flow validation completed for Stripe and Antom: subscription, upgrade, downgrade, cancel, renew, canceling top-up, active top-up, and billing order display.
- Apple still needs iOS sandbox beta validation before production cutover; provider notification/claim paths are covered by code/unit tests in this PR stack.

## Cutover Notes

- This PR does not automatically run backfill or create indexes at service startup.
- Before production cutover, rerun the same read-only distribution check and dry-run against production config, then create indexes manually and only run write mode after blockers are zero.
- Enable v2 read/write flags together after backfill, monitor, and clean legacy paths only after a stable-run window.

```

---

## SHA: de4a63f48edf8ad563e658a0b4c9870620cf6d5b

**作者**: bill-srp

**日期**: 2026-05-31T08:43:16Z

**完整 Commit Message**:

```
chore(web): bump Sentry tracesSampleRate to 0.5 (#2137)

## Summary
- Bump browser Sentry `tracesSampleRate` from `0.2` → `0.5` in
`web/app/sentry.client.config.ts` for higher-fidelity production
performance traces.
- Edge-function middleware (`web/app/functions/_middleware.ts`)
intentionally left at `1.0` — low volume, full coverage is cheap there.
- Resolves
[ECA-792](https://linear.app/srpone/issue/ECA-792/sentry-采样率从-01-提升到-05).
Ticket title says `0.1 → 0.5`; actual file was already at `0.2`, so this
completes the bump.

## Test plan
- [ ] CI green (lint + tsc + unit)
- [ ] After merge, verify in Sentry that browser trace volume roughly
doubles (was ~20%, now ~50%)
- [ ] Watch Sentry billing for the first week to confirm the higher
sample rate is within budget
```

**PR #2137 Body**:

```
## Summary
- Bump browser Sentry `tracesSampleRate` from `0.2` → `0.5` in `web/app/sentry.client.config.ts` for higher-fidelity production performance traces.
- Edge-function middleware (`web/app/functions/_middleware.ts`) intentionally left at `1.0` — low volume, full coverage is cheap there.
- Resolves [ECA-792](https://linear.app/srpone/issue/ECA-792/sentry-采样率从-01-提升到-05). Ticket title says `0.1 → 0.5`; actual file was already at `0.2`, so this completes the bump.

## Test plan
- [ ] CI green (lint + tsc + unit)
- [ ] After merge, verify in Sentry that browser trace volume roughly doubles (was ~20%, now ~50%)
- [ ] Watch Sentry billing for the first week to confirm the higher sample rate is within budget
```

---

## SHA: 72fa3a4ab0baef78011a56c1358cae1281a1b551

**作者**: bill-srp

**日期**: 2026-05-31T04:53:00Z

**完整 Commit Message**:

```
feat(agent-mm): dual-write per-agent Mattermost runtime to AgentWorkspace (#2087)

## Linear

https://linear.app/srpone/issue/ECA-863/fixbot-state-scope-legacy-mirror-cleanup-for-service-agents-branch

## Summary
Iteration 2 of the V2 agent backend (the `mattermost_bots[]` slice).
Every legacy `Account.openclaw_bots[0].mattermost_bots[]` mutation now
also mirrors per-agent Mattermost runtime into the normalized
`ecap-agent-workspaces` store as `AgentWorkspace.mattermost` + `status`,
with **create-on-provision** so V2 agents appear/disappear live. Follows
Iteration 1 (`bot_state_service`, PR #2079) conventions:
legacy-canonical, swallow-and-log mirror, current-org resolution,
`computer_id = openclaw_bots[0].bot_id`.

- **New `app/services/computer/agent_mm_state_service.py`** (sibling to
`bot_state_service`) — persistence only, 5 ops:
- `provision_agent_mm` — route-through: owns the legacy seed/append
**and** the V2 create-on-provision upsert.
- `mirror_provisioned` / `mirror_mm_enabled` / `mirror_mm_field` /
`mirror_mm_removed` — post-write V2-only mirrors keyed by `agent_id`.
- Mattermost/FastClaw orchestration stays in
`mattermost_provisioner.py`; route-facing reads (`agent_service.py`)
untouched.
- **Projectors** (`_projectors.py`, pure) — `project_mm_runtime` +
`project_mm_to_workspace`. `enabled` → `status` (`False` → `disabled`,
`True`/absent → `active`); `channel_injected` dropped, `mattermost_user`
deferred; `created_at` falls back to mirror time.
- **Repo extension** — `agent_workspace_repo.upsert_mm_on_provision`:
`$setOnInsert` identity/creation (`workspace_id`, `created_at`,
`source`, scope keys) + `$set` runtime/`status`/`updated_at`, so a
re-provision never clobbers `workspace_id`/`created_at`.
- **Call-site wiring** — `mattermost_provisioner` (provision agent +
main bot), `agent_deploy_phases` (soft-disable / remove fired agent),
`openclaw_settings/helpers` (display-name sync), `bot_init` (initial-CAS
main bot), warm-pool materialization.
- **Legacy stays canonical** — legacy write first; V2 mirror failures
logged (`[AGENT_MM_DUAL_WRITE]`, `uid[:8]`) but never propagate. A
standalone backfill (out of scope) repairs the existing population.
- `workspace_id` is now a bare `uuid4().hex` (dropped the `aw_` prefix)
for consistency across the V2 store.

Design + plan:
`docs/superpowers/specs/2026-05-29-agent-mattermost-dual-write-design.md`,
`docs/superpowers/plans/2026-05-29-agent-mattermost-dual-write.md`.

## Test plan
- [x] Unit + BDD tests **included** (see diff):
`test_agent_mm_projectors.py`, `test_agent_mm_state_service.py`,
`test_agent_mm_wiring.py`, `test_agent_workspace_repo.py`
(`upsert_mm_on_provision`), and `agent_mm_dual_write.feature` (provision
/ soft-disable / remove / no-org) against real Mongo.
- [x] Existing tests updated for the new wiring:
`test_mattermost_provisioner.py`, `test_openclaw_settings_routes.py`,
`test_agent_service.py`.
- [ ] Local `pytest --cov=app --cov-fail-under=90` in devcontainer —
**not run this session**; relying on CI `build-and-test`.
- [ ] CI `build-and-test` + `auto-review` green.

## Known follow-ups (from self code-review — not blocking, tracked here)
- **H1 (test gap, HIGH):**
`test_warm_pool_materialization_mirrors_each_mm_bot` only exercises the
early-return (no-mirror) path; its name claims the opposite. The new
warm-pool mirror loop (`warm_pool.py:215-218`) has **zero executed
coverage** — it would pass `build-and-test` while testing nothing.
Rename + add a real materialization test
(`assets_materialized_at=None`).
- **M1 (data consistency, MEDIUM):** re-provisioning a
previously-tombstoned workspace flips `status` back to `active` but
never clears `deleted_at` (not in `upsert_mm_on_provision`'s `$set`, nor
in `mirror_mm_enabled(enabled=True)`). Add `deleted_at: None` to the
revive path + a provision→remove→re-provision regression test.
- **M2 (test gap, MEDIUM):** the `bot_init` `mirror_provisioned` loop
(`bot_init.py:359-360`) has no test coverage.
```

**PR #2087 Body**:

```
## Linear
https://linear.app/srpone/issue/ECA-863/fixbot-state-scope-legacy-mirror-cleanup-for-service-agents-branch

## Summary
Iteration 2 of the V2 agent backend (the `mattermost_bots[]` slice). Every legacy `Account.openclaw_bots[0].mattermost_bots[]` mutation now also mirrors per-agent Mattermost runtime into the normalized `ecap-agent-workspaces` store as `AgentWorkspace.mattermost` + `status`, with **create-on-provision** so V2 agents appear/disappear live. Follows Iteration 1 (`bot_state_service`, PR #2079) conventions: legacy-canonical, swallow-and-log mirror, current-org resolution, `computer_id = openclaw_bots[0].bot_id`.

- **New `app/services/computer/agent_mm_state_service.py`** (sibling to `bot_state_service`) — persistence only, 5 ops:
  - `provision_agent_mm` — route-through: owns the legacy seed/append **and** the V2 create-on-provision upsert.
  - `mirror_provisioned` / `mirror_mm_enabled` / `mirror_mm_field` / `mirror_mm_removed` — post-write V2-only mirrors keyed by `agent_id`.
  - Mattermost/FastClaw orchestration stays in `mattermost_provisioner.py`; route-facing reads (`agent_service.py`) untouched.
- **Projectors** (`_projectors.py`, pure) — `project_mm_runtime` + `project_mm_to_workspace`. `enabled` → `status` (`False` → `disabled`, `True`/absent → `active`); `channel_injected` dropped, `mattermost_user` deferred; `created_at` falls back to mirror time.
- **Repo extension** — `agent_workspace_repo.upsert_mm_on_provision`: `$setOnInsert` identity/creation (`workspace_id`, `created_at`, `source`, scope keys) + `$set` runtime/`status`/`updated_at`, so a re-provision never clobbers `workspace_id`/`created_at`.
- **Call-site wiring** — `mattermost_provisioner` (provision agent + main bot), `agent_deploy_phases` (soft-disable / remove fired agent), `openclaw_settings/helpers` (display-name sync), `bot_init` (initial-CAS main bot), warm-pool materialization.
- **Legacy stays canonical** — legacy write first; V2 mirror failures logged (`[AGENT_MM_DUAL_WRITE]`, `uid[:8]`) but never propagate. A standalone backfill (out of scope) repairs the existing population.
- `workspace_id` is now a bare `uuid4().hex` (dropped the `aw_` prefix) for consistency across the V2 store.

Design + plan: `docs/superpowers/specs/2026-05-29-agent-mattermost-dual-write-design.md`, `docs/superpowers/plans/2026-05-29-agent-mattermost-dual-write.md`.

## Test plan
- [x] Unit + BDD tests **included** (see diff): `test_agent_mm_projectors.py`, `test_agent_mm_state_service.py`, `test_agent_mm_wiring.py`, `test_agent_workspace_repo.py` (`upsert_mm_on_provision`), and `agent_mm_dual_write.feature` (provision / soft-disable / remove / no-org) against real Mongo.
- [x] Existing tests updated for the new wiring: `test_mattermost_provisioner.py`, `test_openclaw_settings_routes.py`, `test_agent_service.py`.
- [ ] Local `pytest --cov=app --cov-fail-under=90` in devcontainer — **not run this session**; relying on CI `build-and-test`.
- [ ] CI `build-and-test` + `auto-review` green.

## Known follow-ups (from self code-review — not blocking, tracked here)
- **H1 (test gap, HIGH):** `test_warm_pool_materialization_mirrors_each_mm_bot` only exercises the early-return (no-mirror) path; its name claims the opposite. The new warm-pool mirror loop (`warm_pool.py:215-218`) has **zero executed coverage** — it would pass `build-and-test` while testing nothing. Rename + add a real materialization test (`assets_materialized_at=None`).
- **M1 (data consistency, MEDIUM):** re-provisioning a previously-tombstoned workspace flips `status` back to `active` but never clears `deleted_at` (not in `upsert_mm_on_provision`'s `$set`, nor in `mirror_mm_enabled(enabled=True)`). Add `deleted_at: None` to the revive path + a provision→remove→re-provision regression test.
- **M2 (test gap, MEDIUM):** the `bot_init` `mirror_provisioned` loop (`bot_init.py:359-360`) has no test coverage.

```

---

## SHA: 73b79f1cc119020b53ea302b98e7fbc91ff7d3d4

**作者**: kaka-srp

**日期**: 2026-05-31T04:54:48Z

**完整 Commit Message**:

```
refactor(billing): complete provider v2 subscription flows (#2133)

## Summary
- Refactor Billing v2 provider flows for Stripe, Antom, and Apple into
separated payment-order, subscription-agreement, entitlement-ledger,
provider-event, and audit records.
- Add provider-specific v2 handlers for subscription checkout,
renew/cancel/downgrade, topup fulfillment, refund/compensation, Apple
transaction claim, and server notifications.
- Keep Billing v2 index management out of service startup; indexes are
created manually with `python -m scripts.ensure_billing_v2_indexes`
before rollout.
- Update billing UI/API adapters for cancel downgrade, renew, v2 order
reads, and provider-compatible manage-plan behavior.

## Rollout / verification notes
- Staging beta deployed successfully with `service-v0.7.2-beta.1` from
commit `e27f4d94`; after merging latest main and review fix, this PR
branch is now at `7dd24def`.
- Staging env has `BILLING_V2_WRITES_ENABLED=true`,
`BILLING_V2_READS_ENABLED=true`, and Apple sandbox config loaded.
- Staging Mongo Billing v2 indexes were verified present.
- Stripe and Antom provider flows were exercised locally against staging
dependencies through real checkout/webhook-style paths during
implementation.
- iOS Apple sandbox end-to-end is not completed yet because the iOS side
cannot currently run the full sandbox path; backend Apple v2 route/unit
coverage is included and staging is configured for sandbox.
- Apple v2 notifications record provider facts first;
terminal-notification legacy account/resource cleanup is best-effort and
the hourly subscription sync is the compensating path for stale Apple
account transitions.

## PR size
- `size-override` is intentional for this PR. We previously agreed not
to split the provider-flow refactor into many PRs; this change is large
because it wires the shared v2 storage model through Stripe, Antom,
Apple, API adapters, UI states, and provider-specific regression tests
together.

## Test plan
- [x] `cd services/claw-interface && ruff check app/routes/antom.py
app/routes/apple.py app/routes/orders.py app/routes/stripe.py
app/routes/subscription.py app/services/antom app/services/apple
app/services/stripe app/services/billing_v2
app/services/billing_summary/current_access.py app/lifetime.py
scripts/ensure_billing_v2_indexes.py tests/unit/test_antom_billing_v2.py
tests/unit/test_apple_billing_v2.py tests/unit/test_stripe_billing_v2.py
tests/unit/test_subscription_routes.py
tests/unit/test_orders_endpoints.py tests/unit/test_lifetime.py
tests/unit/test_billing_v2_repos.py`
- [x] `cd services/claw-interface && pyright app/routes/antom.py
app/routes/apple.py app/routes/orders.py app/routes/stripe.py
app/routes/subscription.py app/services/antom app/services/apple
app/services/stripe app/services/billing_v2
app/services/billing_summary/current_access.py app/lifetime.py
scripts/ensure_billing_v2_indexes.py tests/unit/test_antom_billing_v2.py
tests/unit/test_apple_billing_v2.py tests/unit/test_stripe_billing_v2.py
tests/unit/test_subscription_routes.py
tests/unit/test_orders_endpoints.py tests/unit/test_lifetime.py
tests/unit/test_billing_v2_repos.py`
- [x] `cd services/claw-interface && pytest
tests/unit/test_antom_billing_v2.py tests/unit/test_apple_*.py
tests/unit/test_stripe_billing_v2.py
tests/unit/test_subscription_routes.py
tests/unit/test_orders_endpoints.py tests/unit/test_lifetime.py
tests/unit/test_billing_v2_repos.py -q` (224 passed)
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/components/billing/SharedPlanCard.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx`
(75 passed)
- [x] `cd services/claw-interface && pytest
tests/unit/test_orders_endpoints.py::TestGetOrder::test_v2_get_order_reads_payment_order_by_local_order_id
tests/unit/test_orders_endpoints.py::TestGetOrder::test_v2_get_order_uses_read_flag_without_write_flag
tests/unit/test_apple_routes.py::TestAppleNotification::test_v2_expired_notification_runs_expiry_cleanup
-q` (3 passed)
- [x] `cd services/claw-interface && ruff check app/routes/orders.py
app/routes/apple.py tests/unit/test_orders_endpoints.py`
- [x] `cd /workspaces/ecap-workspace && pyright
services/claw-interface/app/routes/orders.py
services/claw-interface/app/routes/apple.py
services/claw-interface/tests/unit/test_orders_endpoints.py`
- [x] `gh run watch 26582682753 --exit-status` for beta deploy
(`service-v0.7.2-beta.1`) succeeded
- [ ] iOS Apple sandbox end-to-end test pending

## Linear
https://linear.app/srpone/issue/ECA-842/provider-flow-refactor
```

**PR #2133 Body**:

```
## Summary
- Refactor Billing v2 provider flows for Stripe, Antom, and Apple into separated payment-order, subscription-agreement, entitlement-ledger, provider-event, and audit records.
- Add provider-specific v2 handlers for subscription checkout, renew/cancel/downgrade, topup fulfillment, refund/compensation, Apple transaction claim, and server notifications.
- Keep Billing v2 index management out of service startup; indexes are created manually with `python -m scripts.ensure_billing_v2_indexes` before rollout.
- Update billing UI/API adapters for cancel downgrade, renew, v2 order reads, and provider-compatible manage-plan behavior.

## Rollout / verification notes
- Staging beta deployed successfully with `service-v0.7.2-beta.1` from commit `e27f4d94`; after merging latest main and review fix, this PR branch is now at `7dd24def`.
- Staging env has `BILLING_V2_WRITES_ENABLED=true`, `BILLING_V2_READS_ENABLED=true`, and Apple sandbox config loaded.
- Staging Mongo Billing v2 indexes were verified present.
- Stripe and Antom provider flows were exercised locally against staging dependencies through real checkout/webhook-style paths during implementation.
- iOS Apple sandbox end-to-end is not completed yet because the iOS side cannot currently run the full sandbox path; backend Apple v2 route/unit coverage is included and staging is configured for sandbox.
- Apple v2 notifications record provider facts first; terminal-notification legacy account/resource cleanup is best-effort and the hourly subscription sync is the compensating path for stale Apple account transitions.

## PR size
- `size-override` is intentional for this PR. We previously agreed not to split the provider-flow refactor into many PRs; this change is large because it wires the shared v2 storage model through Stripe, Antom, Apple, API adapters, UI states, and provider-specific regression tests together.

## Test plan
- [x] `cd services/claw-interface && ruff check app/routes/antom.py app/routes/apple.py app/routes/orders.py app/routes/stripe.py app/routes/subscription.py app/services/antom app/services/apple app/services/stripe app/services/billing_v2 app/services/billing_summary/current_access.py app/lifetime.py scripts/ensure_billing_v2_indexes.py tests/unit/test_antom_billing_v2.py tests/unit/test_apple_billing_v2.py tests/unit/test_stripe_billing_v2.py tests/unit/test_subscription_routes.py tests/unit/test_orders_endpoints.py tests/unit/test_lifetime.py tests/unit/test_billing_v2_repos.py`
- [x] `cd services/claw-interface && pyright app/routes/antom.py app/routes/apple.py app/routes/orders.py app/routes/stripe.py app/routes/subscription.py app/services/antom app/services/apple app/services/stripe app/services/billing_v2 app/services/billing_summary/current_access.py app/lifetime.py scripts/ensure_billing_v2_indexes.py tests/unit/test_antom_billing_v2.py tests/unit/test_apple_billing_v2.py tests/unit/test_stripe_billing_v2.py tests/unit/test_subscription_routes.py tests/unit/test_orders_endpoints.py tests/unit/test_lifetime.py tests/unit/test_billing_v2_repos.py`
- [x] `cd services/claw-interface && pytest tests/unit/test_antom_billing_v2.py tests/unit/test_apple_*.py tests/unit/test_stripe_billing_v2.py tests/unit/test_subscription_routes.py tests/unit/test_orders_endpoints.py tests/unit/test_lifetime.py tests/unit/test_billing_v2_repos.py -q` (224 passed)
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/components/billing/SharedPlanCard.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx` (75 passed)
- [x] `cd services/claw-interface && pytest tests/unit/test_orders_endpoints.py::TestGetOrder::test_v2_get_order_reads_payment_order_by_local_order_id tests/unit/test_orders_endpoints.py::TestGetOrder::test_v2_get_order_uses_read_flag_without_write_flag tests/unit/test_apple_routes.py::TestAppleNotification::test_v2_expired_notification_runs_expiry_cleanup -q` (3 passed)
- [x] `cd services/claw-interface && ruff check app/routes/orders.py app/routes/apple.py tests/unit/test_orders_endpoints.py`
- [x] `cd /workspaces/ecap-workspace && pyright services/claw-interface/app/routes/orders.py services/claw-interface/app/routes/apple.py services/claw-interface/tests/unit/test_orders_endpoints.py`
- [x] `gh run watch 26582682753 --exit-status` for beta deploy (`service-v0.7.2-beta.1`) succeeded
- [ ] iOS Apple sandbox end-to-end test pending

## Linear
https://linear.app/srpone/issue/ECA-842/provider-flow-refactor

```

---

## SHA: 4d4a140cdd7b0ded1c4890cf67709133c4ca6a9f

**作者**: kaka-srp

**日期**: 2026-05-31T03:05:22Z

**完整 Commit Message**:

```
fix(claw-interface): guard legacy Apple ownership claims (#2134)

## Summary
- Block legacy Apple activation when the account already has an active
non-Apple provider subscription, before transaction ownership is claimed
or subscription credits are refreshed.
- Backfill amount and currency when linking Stripe invoice renewals to
existing CRON-RENEWAL orders so recharge history does not show $0.00.
- Note: existing production rows with zero amount still need a one-time
data repair; this fixes future linking.

## Root cause
The legacy Apple activation path trusted a manually submitted Apple
transaction before checking whether the account was already owned by
Stripe or Antom. A tokenless Apple claim could therefore overwrite the
active provider state and refresh the wallet to the Apple plan.
Separately, the legacy cron renewal order linker attached Stripe invoice
metadata but left the pre-created order amount at its default zero
value.

## Test plan
- [x] /home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_apple_subscription_manager.py -q
- [x] /home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_stripe_renewal_order.py
tests/unit/test_apple_subscription_manager.py -q
- [x] /home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_handle_invoice_paid.py
tests/unit/test_stripe_renewal_order.py -q
- [x] /home/node/.venvs/claw-interface/bin/python -m ruff check
app/services/stripe/renewal_order.py
app/services/apple_subscription_manager.py
tests/unit/test_stripe_renewal_order.py
tests/unit/test_apple_subscription_manager.py
- [x] /home/node/.venvs/claw-interface/bin/python -m ruff format --check
app/services/stripe/renewal_order.py
app/services/apple_subscription_manager.py
tests/unit/test_stripe_renewal_order.py
tests/unit/test_apple_subscription_manager.py
- [x] /home/node/.venvs/claw-interface/bin/pyright
app/services/stripe/renewal_order.py
app/services/apple_subscription_manager.py
tests/unit/test_stripe_renewal_order.py
tests/unit/test_apple_subscription_manager.py
- [x] /home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] /home/node/.venvs/claw-interface/bin/pyright app tests
- [ ] /home/node/.venvs/claw-interface/bin/python -m pytest --cov=app
--cov-report=term-missing --cov-fail-under=90 -q (interrupted after
unrelated local OpenClaw live-config failures)
```

**PR #2134 Body**:

```
## Summary
- Block legacy Apple activation when the account already has an active non-Apple provider subscription, before transaction ownership is claimed or subscription credits are refreshed.
- Backfill amount and currency when linking Stripe invoice renewals to existing CRON-RENEWAL orders so recharge history does not show $0.00.
- Note: existing production rows with zero amount still need a one-time data repair; this fixes future linking.

## Root cause
The legacy Apple activation path trusted a manually submitted Apple transaction before checking whether the account was already owned by Stripe or Antom. A tokenless Apple claim could therefore overwrite the active provider state and refresh the wallet to the Apple plan. Separately, the legacy cron renewal order linker attached Stripe invoice metadata but left the pre-created order amount at its default zero value.

## Test plan
- [x] /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_apple_subscription_manager.py -q
- [x] /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_stripe_renewal_order.py tests/unit/test_apple_subscription_manager.py -q
- [x] /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_handle_invoice_paid.py tests/unit/test_stripe_renewal_order.py -q
- [x] /home/node/.venvs/claw-interface/bin/python -m ruff check app/services/stripe/renewal_order.py app/services/apple_subscription_manager.py tests/unit/test_stripe_renewal_order.py tests/unit/test_apple_subscription_manager.py
- [x] /home/node/.venvs/claw-interface/bin/python -m ruff format --check app/services/stripe/renewal_order.py app/services/apple_subscription_manager.py tests/unit/test_stripe_renewal_order.py tests/unit/test_apple_subscription_manager.py
- [x] /home/node/.venvs/claw-interface/bin/pyright app/services/stripe/renewal_order.py app/services/apple_subscription_manager.py tests/unit/test_stripe_renewal_order.py tests/unit/test_apple_subscription_manager.py
- [x] /home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] /home/node/.venvs/claw-interface/bin/pyright app tests
- [ ] /home/node/.venvs/claw-interface/bin/python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q (interrupted after unrelated local OpenClaw live-config failures)

```

