# ecap-workspace Commits — 2026-05-09

Total: 9 commits

---

## 8e1889b0 — fix(openclaw): upgrade bot image before redeploy so Refresh Now works (#1586)

- **Author**: tim-srp
- **Date**: 2026-05-09T16:28:22Z
- **SHA**: 8e1889b0ecc7d999fc867c3e820b38c420949b96
- **PR**: #1586

### Commit Message

```
fix(openclaw): upgrade bot image before redeploy so Refresh Now works (#1586)

## Summary

- The "Refresh Now" button triggered a redeploy (stop+start) without
updating the bot's `deployment.image`, so bots with an explicit image
pinned at an old version would restart on that same old version — the
upgrade banner persisted
- Root cause: once a bot has `config.deployment.image` explicitly set
(e.g. from batch upgrade scripts or the @srp.one image-version
selector), FastClaw uses that stored value on start instead of
`defaultDeployment.image`
- Fix: call the existing `upgrade_bot_image_if_needed()` helper before
`redeploy_bot()` to update the image to the latest published release
- Also aligns the image read path with current FastClaw API structure
(`bot.image` top-level field, with fallback to `deployment.image`)

## Test plan

- [x] `pyright` clean
- [x] All pre-commit hooks pass
- [x] Existing `test_bot_upgrade.py` tests still pass (9/9)
- [ ] Manual verification: after deploy, publish a new release → banner
appears → click "Refresh Now" → bot restarts on new version → banner
disappears

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

- The "Refresh Now" button triggered a redeploy (stop+start) without updating the bot's `deployment.image`, so bots with an explicit image pinned at an old version would restart on that same old version — the upgrade banner persisted
- Root cause: once a bot has `config.deployment.image` explicitly set (e.g. from batch upgrade scripts or the @srp.one image-version selector), FastClaw uses that stored value on start instead of `defaultDeployment.image`
- Fix: call the existing `upgrade_bot_image_if_needed()` helper before `redeploy_bot()` to update the image to the latest published release
- Also aligns the image read path with current FastClaw API structure (`bot.image` top-level field, with fallback to `deployment.image`)

## Test plan

- [x] `pyright` clean
- [x] All pre-commit hooks pass
- [x] Existing `test_bot_upgrade.py` tests still pass (9/9)
- [ ] Manual verification: after deploy, publish a new release → banner appears → click "Refresh Now" → bot restarts on new version → banner disappears

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 17cd6725 — feat(cron): trial BG terminate fix + BG/Lago↔Mongo reconciler (ECA-647 follow-ups) (#1583)

- **Author**: kaka-srp
- **Date**: 2026-05-09T09:43:28Z
- **SHA**: 17cd67255bfe5d51e562ceb5087fef6d84aec952
- **PR**: #1583

### Commit Message

```
feat(cron): trial BG terminate fix + BG/Lago↔Mongo reconciler (ECA-647 follow-ups) (#1583)

## Summary

Two ECA-647 follow-ups bundled, both stemming from the same
Apple-webhook RCA sweep:

### Fix #1: trial BG terminate gated on `billing_initialized`, not
external sub id

ECA-543's `has_external_sub` guard (skip BG terminate when no
Stripe/Apple sub id) silently skipped trial users redeemed via
invite-code — they have no Stripe/Apple ID but **do** have a
`free_month` BG sub from `ensure_billing_initialized`. Their trial cron
expiry flipped mongo to `expired` while leaving Lago holding the sub
alive, blocking their next subscribe attempt with the same 400 fixed in
#1582.

7 prod users affected (already wash-cleaned). Switch the predicate from
`has_external_sub` → `billing_initialized`. Preserves ECA-543's
noise-suppression intent while correctly covering invite-code trials.

### Fix #2: BG/Lago ↔ Mongo subscription drift reconciler

Companion to `stripe_reconcile.py` — together they cover both sides of
the three-way contract Mongo/Stripe/Lago that this codebase has
accumulated drift between.

Detects accounts whose mongo `subscription_status` is terminal
(`expired` / `free` / `canceled`) but whose Lago team still holds an
`active` subscription — the precondition behind every variant of the
ECA-647 \`start_date is only supported when creating a new
subscription\` 400.

- New cron: `app/cron/bg_reconcile.py` (`check_bg_mongo_reconcile`)
- New endpoint: `POST
/admin/cron/check-bg-mongo-reconcile?batch_limit=500&write_mode=false`
- Read-only by default; `write_mode=true` calls `terminate_subscription`
per orphan using Lago's actual `external_id` (not the customer_id
default that 404s on historic data)
- Per-team BG lookup is async with `asyncio.Semaphore(50)` — 50/sec is
well within BG tolerance based on the 2298-account manual sweep that
backfilled this work
- Greppable log markers: `[DRIFT]` / `[APPLIED]` / `[SUMMARY]`
- `docs/cron-triggers.md` updated

## Test plan

- [x] `tests/unit/test_subscription_cron.py` — 2 new tests on the trial
guard fix (invite-code trial → terminate IS called; uninitialized →
skipped). 22/22 file-level pass after merging main (codex correctly
flagged the missing `_accs(user)` wrap on the second new test — branch
was 3 commits behind main where the `Account.model_validate` switch
landed in #1581)
- [x] `tests/unit/test_bg_reconcile.py` — 8 new tests: empty result,
aligned-no-drift, drift-read-only, drift-write-mode,
terminate-failure-soft-retry, lookup-failure-counted,
no-billing-url-skip, missing-external-id fallback
- [x] 101 tests pass across `test_subscription_cron + test_bg_reconcile
+ test_apple_routes + test_stripe_billing_gateway +
test_stripe_reconcile`

Linear-issue: Refs ECA-647
```

### PR Body

## Summary

Two ECA-647 follow-ups bundled, both stemming from the same Apple-webhook RCA sweep:

### Fix #1: trial BG terminate gated on `billing_initialized`, not external sub id

ECA-543's `has_external_sub` guard (skip BG terminate when no Stripe/Apple sub id) silently skipped trial users redeemed via invite-code — they have no Stripe/Apple ID but **do** have a `free_month` BG sub from `ensure_billing_initialized`. Their trial cron expiry flipped mongo to `expired` while leaving Lago holding the sub alive, blocking their next subscribe attempt with the same 400 fixed in #1582.

7 prod users affected (already wash-cleaned). Switch the predicate from `has_external_sub` → `billing_initialized`. Preserves ECA-543's noise-suppression intent while correctly covering invite-code trials.

### Fix #2: BG/Lago ↔ Mongo subscription drift reconciler

Companion to `stripe_reconcile.py` — together they cover both sides of the three-way contract Mongo/Stripe/Lago that this codebase has accumulated drift between.

Detects accounts whose mongo `subscription_status` is terminal (`expired` / `free` / `canceled`) but whose Lago team still holds an `active` subscription — the precondition behind every variant of the ECA-647 \`start_date is only supported when creating a new subscription\` 400.

- New cron: `app/cron/bg_reconcile.py` (`check_bg_mongo_reconcile`)
- New endpoint: `POST /admin/cron/check-bg-mongo-reconcile?batch_limit=500&write_mode=false`
- Read-only by default; `write_mode=true` calls `terminate_subscription` per orphan using Lago's actual `external_id` (not the customer_id default that 404s on historic data)
- Per-team BG lookup is async with `asyncio.Semaphore(50)` — 50/sec is well within BG tolerance based on the 2298-account manual sweep that backfilled this work
- Greppable log markers: `[DRIFT]` / `[APPLIED]` / `[SUMMARY]`
- `docs/cron-triggers.md` updated

## Test plan

- [x] `tests/unit/test_subscription_cron.py` — 2 new tests on the trial guard fix (invite-code trial → terminate IS called; uninitialized → skipped). 22/22 file-level pass after merging main (codex correctly flagged the missing `_accs(user)` wrap on the second new test — branch was 3 commits behind main where the `Account.model_validate` switch landed in #1581)
- [x] `tests/unit/test_bg_reconcile.py` — 8 new tests: empty result, aligned-no-drift, drift-read-only, drift-write-mode, terminate-failure-soft-retry, lookup-failure-counted, no-billing-url-skip, missing-external-id fallback
- [x] 101 tests pass across `test_subscription_cron + test_bg_reconcile + test_apple_routes + test_stripe_billing_gateway + test_stripe_reconcile`

Linear-issue: Refs ECA-647

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 87752450 — fix(claw-interface): Apple webhook BG terminate + Stripe drift recovery (ECA-647) (#1582)

- **Author**: kaka-srp
- **Date**: 2026-05-09T08:25:22Z
- **SHA**: 87752450941366c3259bb8ac31e78fe05111b6ee
- **PR**: #1582

### Commit Message

```
fix(claw-interface): Apple webhook BG terminate + Stripe drift recovery (ECA-647) (#1582)

## Summary

- **A.** `app/routes/apple.py` — Apple S2S webhook DEACTIVATE (`EXPIRED`
/ `DID_FAIL_TO_RENEW` / `REVOKE`) now calls
`billing.terminate_subscription(team_id)` before `clear_wallet`,
mirroring `subscription_cron.py:_handle_expired_subscription`. Closes
the asymmetry that left BG/Lago with active subs after Apple expiry.
- **B.** `app/services/stripe/billing_gateway.py` —
`grant_subscription_via_billing_gateway` catches the BG 400 `start_date
is only supported when creating a new subscription` and retries without
`start_date`. Mirrors the existing pattern in
`subscription_manager.py:178-195`. Belt-and-braces for any future drift
from sources other than the Apple webhook.

## Production incident

`uid=7274359038282399744` on 2026-05-09 05:57–05:58 UTC paid $20 via
Stripe → BG subscribe rejected with the 400 above (Apple sub from
2026-04-03 still alive in Lago) → saga refunded
`re_3TV3thA5By9khMVb0kyXmroP` → user got money back but no entitlement.
Sweep across all 2298 expired accounts found 11 affected users; data
wash already applied (BG terminate + mongo cleanup of stale Stripe IDs).

## Out of scope (separate issues)

- `free_month` trial auto-terminate gap (7/10 of the residual users
found in sweep)
- ECA-643 reconciler extension to detect Apple/trial drift (currently
only Stripe ↔ Mongo)

## Test plan

- [x] `tests/unit/test_apple_routes.py` — 4 updated tests assert
`terminate_subscription` is called (or skipped when no `team_id`); 1 new
test covers terminate failure not breaking the cleanup chain
- [x] `tests/unit/test_stripe_billing_gateway.py` — 3 new tests:
drift-400 retries without `start_date` (same `transaction_id` for BG
idempotency), other-400 propagates, no-`start_date`-400 propagates (no
infinite retry)
- [x] `_stripe_helpers.make_http_status_error` extended with optional
`body` arg

Linear-issue: Fixes ECA-647
```

### PR Body

## Summary

- **A.** `app/routes/apple.py` — Apple S2S webhook DEACTIVATE (`EXPIRED` / `DID_FAIL_TO_RENEW` / `REVOKE`) now calls `billing.terminate_subscription(team_id)` before `clear_wallet`, mirroring `subscription_cron.py:_handle_expired_subscription`. Closes the asymmetry that left BG/Lago with active subs after Apple expiry.
- **B.** `app/services/stripe/billing_gateway.py` — `grant_subscription_via_billing_gateway` catches the BG 400 `start_date is only supported when creating a new subscription` and retries without `start_date`. Mirrors the existing pattern in `subscription_manager.py:178-195`. Belt-and-braces for any future drift from sources other than the Apple webhook.

## Production incident

`uid=7274359038282399744` on 2026-05-09 05:57–05:58 UTC paid $20 via Stripe → BG subscribe rejected with the 400 above (Apple sub from 2026-04-03 still alive in Lago) → saga refunded `re_3TV3thA5By9khMVb0kyXmroP` → user got money back but no entitlement. Sweep across all 2298 expired accounts found 11 affected users; data wash already applied (BG terminate + mongo cleanup of stale Stripe IDs).

## Out of scope (separate issues)

- `free_month` trial auto-terminate gap (7/10 of the residual users found in sweep)
- ECA-643 reconciler extension to detect Apple/trial drift (currently only Stripe ↔ Mongo)

## Test plan

- [x] `tests/unit/test_apple_routes.py` — 4 updated tests assert `terminate_subscription` is called (or skipped when no `team_id`); 1 new test covers terminate failure not breaking the cleanup chain
- [x] `tests/unit/test_stripe_billing_gateway.py` — 3 new tests: drift-400 retries without `start_date` (same `transaction_id` for BG idempotency), other-400 propagates, no-`start_date`-400 propagates (no infinite retry)
- [x] `_stripe_helpers.make_http_status_error` extended with optional `body` arg

Linear-issue: Fixes ECA-647

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## 3f9a027f — fix(claw-interface): preserve cron plan/billing_cycle defaults after Account.model_dump() (#1581)

- **Author**: bill-srp
- **Date**: 2026-05-09T08:15:10Z
- **SHA**: 3f9a027f9a963be5bc0bc346d9f7d292c550c624
- **PR**: #1581

### Commit Message

```
fix(claw-interface): preserve cron plan/billing_cycle defaults after Account.model_dump() (#1581)

## Summary

Fixes a subtle bug introduced by PR #1580's typed-Account migration.
After `[a.model_dump() for a in accounts]`, the `plan` and
`billing_cycle` fields are materialized as **present-but-`None`** keys
(both are `str | None = None` on `Account`), defeating downstream
`.get(key, default)` fallbacks — a present-but-None key returns `None`,
not the default.

For a legacy `ecap-account` doc that lacks these fields, this caused:
- `credits_for_plan(None)` → `PLAN_CREDITS.get(None, 0)` returns **0
credits silently**
- `transition_to_active(plan=None, billing_cycle=None, …)` → persists
`plan=None` to Mongo
- `process_cron_renewal(plan=None, billing_cycle=None, …)` → same

## What changed

Switched `user.get(key, default)` → `user.get(key) or default` at every
affected site so missing-key and key-present-as-None are handled
uniformly:

| File | Lines | Fix |
|---|---|---|
| `app/cron/subscription_cron.py` | 200-201, 266, 384 | `plan` (3 sites)
+ `billing_cycle` (1 site) |
| `app/cron/_apple_expiry.py` | 43-44 | `plan` + `billing_cycle` (Apple
verification path) |

`_apple_expiry.py` had the identical bug pattern — it receives the same
`model_dump()`-derived dict from `check_yearly_credits_reset` line 271
and passes the values straight into `process_cron_renewal(plan: str,
billing_cycle: str)`. Originally surfaced by reuse-review of the
narrower fix.

## Why `… or default` and not `model_dump(exclude_none=True)`

The boundary fix (`exclude_none=True` at the three `model_dump()` call
sites) would also drop *every* defaulted-`None` field from the dict —
`subscription_status=None`, `email=None`, etc. — which would surprise
any consumer that uses `if "key" in user:` semantics. The `or` form is
narrower: it only matters at the four sites where a meaningful
non-`None` default exists.

## Why not migrate to `PlanTier.STARTER` / `BillingCycle.MONTHLY` enums

These enums exist in `app/schema/subscription.py:18-30`, but the cron
file uses bare strings throughout (lines 205, 292, 353, 391 — outside
this PR). Migrating only the new occurrences would create inconsistency
with adjacent existing code; doing it holistically would also require
changing `plan_from_stripe_product_id`'s return type and
`transition_to_active`'s signature, which is a separate refactor better
done as one cohesive PR.

## Test plan

- [x] 4 new regression tests in `tests/unit/test_subscription_cron.py`,
one per affected entry point:
- `test_trial_expiry_legacy_account_falls_back_to_starter_monthly` —
covers both `plan` and `billing_cycle` defaults flowing into
`credits_for_plan` and `transition_to_active`
- `test_yearly_reset_legacy_account_falls_back_to_starter` — covers
Stripe yearly path → `process_cron_renewal`
- `test_yearly_ios_legacy_account_falls_back_to_starter` — covers Apple
yearly path through `_check_apple_subscription` → `process_cron_renewal`
- `test_sync_legacy_account_falls_back_to_starter` — covers monthly
Stripe path → `process_cron_renewal`
- [x] Each test deletes `plan` (and where applicable `billing_cycle`)
from the input dict to mimic a legacy production record that predates
these fields.
- [x] All 21 tests in `test_subscription_cron.py` pass; broader 423-test
cron/subscription/stripe filter passes.
- [x] `ruff` + `pyright` clean on all 3 changed files.

## Notes for reviewers

- This addresses post-merge code-review feedback on PR #1580 referencing
`subscription_cron.py:176, 254, 357`.
- The MEMORY note "~56 downstream `.model_dump()` shims remain as
next-phase TODO" tracks the broader pattern. This PR fixes only the two
cron files where missing-key → wrong-default has a concrete, observable
consequence (silent 0-credit grants, wrong Mongo persistence). Other
shim sites should be audited as part of the typed-Account follow-up
migration.
```

### PR Body

## Summary

Fixes a subtle bug introduced by PR #1580's typed-Account migration. After `[a.model_dump() for a in accounts]`, the `plan` and `billing_cycle` fields are materialized as **present-but-`None`** keys (both are `str | None = None` on `Account`), defeating downstream `.get(key, default)` fallbacks — a present-but-None key returns `None`, not the default.

For a legacy `ecap-account` doc that lacks these fields, this caused:
- `credits_for_plan(None)` → `PLAN_CREDITS.get(None, 0)` returns **0 credits silently**
- `transition_to_active(plan=None, billing_cycle=None, …)` → persists `plan=None` to Mongo
- `process_cron_renewal(plan=None, billing_cycle=None, …)` → same

## What changed

Switched `user.get(key, default)` → `user.get(key) or default` at every affected site so missing-key and key-present-as-None are handled uniformly:

| File | Lines | Fix |
|---|---|---|
| `app/cron/subscription_cron.py` | 200-201, 266, 384 | `plan` (3 sites) + `billing_cycle` (1 site) |
| `app/cron/_apple_expiry.py` | 43-44 | `plan` + `billing_cycle` (Apple verification path) |

`_apple_expiry.py` had the identical bug pattern — it receives the same `model_dump()`-derived dict from `check_yearly_credits_reset` line 271 and passes the values straight into `process_cron_renewal(plan: str, billing_cycle: str)`. Originally surfaced by reuse-review of the narrower fix.

## Why `… or default` and not `model_dump(exclude_none=True)`

The boundary fix (`exclude_none=True` at the three `model_dump()` call sites) would also drop *every* defaulted-`None` field from the dict — `subscription_status=None`, `email=None`, etc. — which would surprise any consumer that uses `if "key" in user:` semantics. The `or` form is narrower: it only matters at the four sites where a meaningful non-`None` default exists.

## Why not migrate to `PlanTier.STARTER` / `BillingCycle.MONTHLY` enums

These enums exist in `app/schema/subscription.py:18-30`, but the cron file uses bare strings throughout (lines 205, 292, 353, 391 — outside this PR). Migrating only the new occurrences would create inconsistency with adjacent existing code; doing it holistically would also require changing `plan_from_stripe_product_id`'s return type and `transition_to_active`'s signature, which is a separate refactor better done as one cohesive PR.

## Test plan

- [x] 4 new regression tests in `tests/unit/test_subscription_cron.py`, one per affected entry point:
  - `test_trial_expiry_legacy_account_falls_back_to_starter_monthly` — covers both `plan` and `billing_cycle` defaults flowing into `credits_for_plan` and `transition_to_active`
  - `test_yearly_reset_legacy_account_falls_back_to_starter` — covers Stripe yearly path → `process_cron_renewal`
  - `test_yearly_ios_legacy_account_falls_back_to_starter` — covers Apple yearly path through `_check_apple_subscription` → `process_cron_renewal`
  - `test_sync_legacy_account_falls_back_to_starter` — covers monthly Stripe path → `process_cron_renewal`
- [x] Each test deletes `plan` (and where applicable `billing_cycle`) from the input dict to mimic a legacy production record that predates these fields.
- [x] All 21 tests in `test_subscription_cron.py` pass; broader 423-test cron/subscription/stripe filter passes.
- [x] `ruff` + `pyright` clean on all 3 changed files.

## Notes for reviewers

- This addresses post-merge code-review feedback on PR #1580 referencing `subscription_cron.py:176, 254, 357`.
- The MEMORY note "~56 downstream `.model_dump()` shims remain as next-phase TODO" tracks the broader pattern. This PR fixes only the two cron files where missing-key → wrong-default has a concrete, observable consequence (silent 0-credit grants, wrong Mongo persistence). Other shim sites should be audited as part of the typed-Account follow-up migration.

---

## 2b6e957a — refactor(claw-interface): dedup openclaw_repo.get_user onto user_repo (#1580)

- **Author**: bill-srp
- **Date**: 2026-05-09T07:10:49Z
- **SHA**: 2b6e957a3e9a886460ce57446b14c3ef1a3f7e04
- **PR**: #1580

### Commit Message

```
refactor(claw-interface): dedup openclaw_repo.get_user onto user_repo (#1580)

## Summary

Realizes the named follow-up from #1574 — _"`openclaw_repo.get_user`
dedup … verbatim duplicate of `user_repo.get_user`"_ — by migrating
every production caller off `openclaw_repo.get_user` and then deleting
the duplicate symbol. 7 atomic phase commits (`release_admin` →
`chat_replay` → `openclaw_integrations` → `mattermost_provisioner` →
`routes/openclaw` → `routes/openclaw_agents` → `services/openclaw`), one
file group per commit so each is reviewable in isolation.

## What's in the PR

### Migration pattern

Two flavors depending on the caller's downstream shape:

**Pattern A — typed-then-dump (mechanical caller):**
```python
account = await user_repo.get_user(uid)
user = account.model_dump() if account else None
```
Used where the caller passes `user` into a phase-6 helper that's still
`dict`-typed (`get_first_bot`, `get_app_token`,
`_is_subscription_expired`, `ensure_billing_initialized`, etc.). The
`model_dump()` boundary preserves all downstream dict-keyed code
untouched.

**Pattern B — typed attribute access (small caller):**
```python
account = await user_repo.get_user(uid)  # used as Account
```
Used in `release_admin._require_admin` (truthy check),
`chat_replay/create.py` (`_collect_user_bots(account.openclaw_bots)`),
`openclaw_integrations/_get_bot_user` (return value retyped), and the
`mattermost_provisioner` provision_* functions (`account.openclaw_bots`
direct access).

### Per-phase scope

| Phase | Commit | Files | Sites |
|---|---|---|---|
| 1 | `0e27a30db` | `routes/release_admin.py` | 1 |
| 2 | `65d50a4f7` | `services/chat_replay/create.py` | 1 |
| 3 | `dd368422c` | `routes/openclaw_integrations/{core,executor}.py` |
3 |
| 4 | `45cde3242` | `services/mattermost_provisioner.py` | 4 |
| 5a | `1bf893883` | `routes/openclaw.py` | 7 |
| 5b | `f6621ef2f` | `routes/openclaw_agents/*` (4 files) | 10 |
| 6 | `594a15910` | `services/openclaw/*` (5 files) + delete
`openclaw_repo.get_user` | 8 + symbol delete |

### Why phase 6 doesn't migrate the helper signatures

`bot_lifecycle.py`'s `get_first_bot(user: dict)`, `get_app(user: dict)`,
`get_app_token(user: dict)` stay `dict`-typed. Migrating those to
`Account` would cascade into rewriting every `model_dump()` shim and is
a larger refactor with broader blast radius — properly its own PR. The
shims are the marker for that follow-up: ~25 `model_dump()` lines
disappear when those signatures change.

### Test mock migration patterns

Three mock-source patterns surfaced:

1. **Mock `user_repo` directly** (e.g. `test_release_admin_routes.py`):
`@patch("...user_repo")` + `Account.model_validate({...})` returns.
Cleanest, ~5 sites.
2. **Mock at the `mongo` layer** (e.g. `test_openclaw_routes.py`,
`test_openclaw_endpoints_extra.py`, 7 fixtures in
`test_openclaw_agents.py`): added `patch("app.database.user_repo.mongo",
m)` to the existing `openclaw_repo.mongo` ExitStack so both repo paths
share the same MagicMock. Lowest-churn.
3. **Mock `openclaw_repo.get_user` becomes stale** (e.g. legacy
`executor.openclaw_repo.get_user` patches in
`test_integration_routes.py`): kept in place where the same patch also
mocks unrelated writes (`dec_credits`); the `get_user` attribute on the
mock is now dead. Flagged as cleanup debt; harmless.

`test_stop_user_bots.py` and `test_start_user_bots.py` got a top-level
`_as_account()` helper to wrap dict fixtures, plus
`@patch("...user_repo")` added to each test's `with` block.

### BDD test impact

- `tests/bdd/features/openclaw_repo.feature`: dropped two scenarios
(`Get user by uid`, `Get user returns None when not found`) that
explicitly tested `openclaw_repo.get_user`. Equivalent coverage exists
in `tests/unit/test_user_repo.py` for `user_repo.get_user`.
- `test_openclaw_repo.py`, `test_openclaw_lifecycle.py`,
`test_openclaw_custom_agents.py`: BDD step defs now read via
`user_repo.get_user(uid).model_dump()` (helpers `_read_user` /
`_read_user_doc`).

### Two file imports dropped entirely

`routes/openclaw_agents/core.py`, `routes/openclaw_agents/deploy.py`,
and `services/openclaw/agent_deploy.py` had `from app.database import
openclaw_repo as repo` purely for `get_user`. Once that single use
migrated, ruff's F401 caught the now-unused import — dropped cleanly.
Files that retained `openclaw_repo` (e.g. `bot_stop.py`,
`mattermost_provisioner.py`) genuinely still own writes
(`set_bot_status`, `update_*_fields`, `set_bot_field`, `push_to_array`).

## Test plan

```bash
# Run inside devcontainer
cd services/claw-interface
/home/node/.venvs/claw-interface/bin/pytest tests/unit/ -q --ignore=tests/unit/test_ci_lint_deptry.py
```

- [x] **2932 unit tests pass**, 366 skipped (BDD requires
`TEST_MONGODB_HOST=127.0.0.1` + a running mongod sidecar; this
devcontainer doesn't have one)
- [x] `pyright app/ tests/unit/` — 0 errors
- [x] `ruff check app/ tests/` — clean
- [x] `lint-imports` — all 8 architecture contracts kept (no C1
violations introduced or fixed by this PR; the `openclaw_repo as repo`
aliases that survive are sanctioned consumers)
- [x] Coverage: 87% (pre-existing baseline; not enforced by
`--cov-fail-under` anywhere in `pyproject.toml` / CI)
- [x] `grep -rn 'openclaw_repo.get_user\|repo.get_user'
services/claw-interface/app/` — zero production callers remain
- [x] `services/claw-interface/app/database/openclaw_repo.py` no longer
defines `get_user`

Pre-existing infra failures unchanged: `test_ci_lint_deptry::*`
(devcontainer can't resolve the host-absolute path in
`.git/worktrees/service-pydantic/gitdir`).

## Follow-ups

- **Migrate `bot_lifecycle.py` helpers to `Account`-typed signatures** —
would remove ~25 `model_dump()` shim lines added by this PR. Reviewable
as a single follow-up because the callers are already concentrated.
- **Cleanup stale `mock_oc_repo.get_user` lines** in
`test_integration_routes.py` — the legacy `executor.openclaw_repo`
patches still set a `.get_user` attribute that nothing reads. Pure
dead-code removal.
- **`chat.py` / `canvas.py` direct `mongo.read_one`** — still listed as
a follow-up in #1574; not addressed here.
```

### PR Body

## Summary

Realizes the named follow-up from #1574 — _"`openclaw_repo.get_user` dedup … verbatim duplicate of `user_repo.get_user`"_ — by migrating every production caller off `openclaw_repo.get_user` and then deleting the duplicate symbol. 7 atomic phase commits (`release_admin` → `chat_replay` → `openclaw_integrations` → `mattermost_provisioner` → `routes/openclaw` → `routes/openclaw_agents` → `services/openclaw`), one file group per commit so each is reviewable in isolation.

## What's in the PR

### Migration pattern

Two flavors depending on the caller's downstream shape:

**Pattern A — typed-then-dump (mechanical caller):**
```python
account = await user_repo.get_user(uid)
user = account.model_dump() if account else None
```
Used where the caller passes `user` into a phase-6 helper that's still `dict`-typed (`get_first_bot`, `get_app_token`, `_is_subscription_expired`, `ensure_billing_initialized`, etc.). The `model_dump()` boundary preserves all downstream dict-keyed code untouched.

**Pattern B — typed attribute access (small caller):**
```python
account = await user_repo.get_user(uid)  # used as Account
```
Used in `release_admin._require_admin` (truthy check), `chat_replay/create.py` (`_collect_user_bots(account.openclaw_bots)`), `openclaw_integrations/_get_bot_user` (return value retyped), and the `mattermost_provisioner` provision_* functions (`account.openclaw_bots` direct access).

### Per-phase scope

| Phase | Commit | Files | Sites |
|---|---|---|---|
| 1 | `0e27a30db` | `routes/release_admin.py` | 1 |
| 2 | `65d50a4f7` | `services/chat_replay/create.py` | 1 |
| 3 | `dd368422c` | `routes/openclaw_integrations/{core,executor}.py` | 3 |
| 4 | `45cde3242` | `services/mattermost_provisioner.py` | 4 |
| 5a | `1bf893883` | `routes/openclaw.py` | 7 |
| 5b | `f6621ef2f` | `routes/openclaw_agents/*` (4 files) | 10 |
| 6 | `594a15910` | `services/openclaw/*` (5 files) + delete `openclaw_repo.get_user` | 8 + symbol delete |

### Why phase 6 doesn't migrate the helper signatures

`bot_lifecycle.py`'s `get_first_bot(user: dict)`, `get_app(user: dict)`, `get_app_token(user: dict)` stay `dict`-typed. Migrating those to `Account` would cascade into rewriting every `model_dump()` shim and is a larger refactor with broader blast radius — properly its own PR. The shims are the marker for that follow-up: ~25 `model_dump()` lines disappear when those signatures change.

### Test mock migration patterns

Three mock-source patterns surfaced:

1. **Mock `user_repo` directly** (e.g. `test_release_admin_routes.py`): `@patch("...user_repo")` + `Account.model_validate({...})` returns. Cleanest, ~5 sites.
2. **Mock at the `mongo` layer** (e.g. `test_openclaw_routes.py`, `test_openclaw_endpoints_extra.py`, 7 fixtures in `test_openclaw_agents.py`): added `patch("app.database.user_repo.mongo", m)` to the existing `openclaw_repo.mongo` ExitStack so both repo paths share the same MagicMock. Lowest-churn.
3. **Mock `openclaw_repo.get_user` becomes stale** (e.g. legacy `executor.openclaw_repo.get_user` patches in `test_integration_routes.py`): kept in place where the same patch also mocks unrelated writes (`dec_credits`); the `get_user` attribute on the mock is now dead. Flagged as cleanup debt; harmless.

`test_stop_user_bots.py` and `test_start_user_bots.py` got a top-level `_as_account()` helper to wrap dict fixtures, plus `@patch("...user_repo")` added to each test's `with` block.

### BDD test impact

- `tests/bdd/features/openclaw_repo.feature`: dropped two scenarios (`Get user by uid`, `Get user returns None when not found`) that explicitly tested `openclaw_repo.get_user`. Equivalent coverage exists in `tests/unit/test_user_repo.py` for `user_repo.get_user`.
- `test_openclaw_repo.py`, `test_openclaw_lifecycle.py`, `test_openclaw_custom_agents.py`: BDD step defs now read via `user_repo.get_user(uid).model_dump()` (helpers `_read_user` / `_read_user_doc`).

### Two file imports dropped entirely

`routes/openclaw_agents/core.py`, `routes/openclaw_agents/deploy.py`, and `services/openclaw/agent_deploy.py` had `from app.database import openclaw_repo as repo` purely for `get_user`. Once that single use migrated, ruff's F401 caught the now-unused import — dropped cleanly. Files that retained `openclaw_repo` (e.g. `bot_stop.py`, `mattermost_provisioner.py`) genuinely still own writes (`set_bot_status`, `update_*_fields`, `set_bot_field`, `push_to_array`).

## Test plan

```bash
# Run inside devcontainer
cd services/claw-interface
/home/node/.venvs/claw-interface/bin/pytest tests/unit/ -q --ignore=tests/unit/test_ci_lint_deptry.py
```

- [x] **2932 unit tests pass**, 366 skipped (BDD requires `TEST_MONGODB_HOST=127.0.0.1` + a running mongod sidecar; this devcontainer doesn't have one)
- [x] `pyright app/ tests/unit/` — 0 errors
- [x] `ruff check app/ tests/` — clean
- [x] `lint-imports` — all 8 architecture contracts kept (no C1 violations introduced or fixed by this PR; the `openclaw_repo as repo` aliases that survive are sanctioned consumers)
- [x] Coverage: 87% (pre-existing baseline; not enforced by `--cov-fail-under` anywhere in `pyproject.toml` / CI)
- [x] `grep -rn 'openclaw_repo.get_user\|repo.get_user' services/claw-interface/app/` — zero production callers remain
- [x] `services/claw-interface/app/database/openclaw_repo.py` no longer defines `get_user`

Pre-existing infra failures unchanged: `test_ci_lint_deptry::*` (devcontainer can't resolve the host-absolute path in `.git/worktrees/service-pydantic/gitdir`).

## Follow-ups

- **Migrate `bot_lifecycle.py` helpers to `Account`-typed signatures** — would remove ~25 `model_dump()` shim lines added by this PR. Reviewable as a single follow-up because the callers are already concentrated.
- **Cleanup stale `mock_oc_repo.get_user` lines** in `test_integration_routes.py` — the legacy `executor.openclaw_repo` patches still set a `.get_user` attribute that nothing reads. Pure dead-code removal.
- **`chat.py` / `canvas.py` direct `mongo.read_one`** — still listed as a follow-up in #1574; not addressed here.

---

## 55601761 — fix(stripe): ECA-643 — Stripe ↔ Mongo subscription drift hotfix bundle (#1-#5 + 5 review rounds) (#1579)

- **Author**: kaka-srp
- **Date**: 2026-05-09T03:42:44Z
- **SHA**: 55601761243a60d6ce4fda9faab99118abd83287
- **PR**: #1579

### Commit Message

```
fix(stripe): ECA-643 — Stripe ↔ Mongo subscription drift hotfix bundle (#1-#5 + 5 review rounds) (#1579)

## Summary

修复 ECA-643 报障 "Failed to cancel subscription. Please try again":挖出 2
个独立代码缺陷 + 1 次 webhook 域名 outage(已恢复)联合造成的 Stripe ↔ Mongo 状态漂移。完整 RCA +
修复方案见
[`docs/superpowers/specs/2026-05-08-stripe-mongo-drift-rca.md`](docs/superpowers/specs/2026-05-08-stripe-mongo-drift-rca.md)。

生产实测影响范围:53 个有 stripe_subscription_id 的用户中,**25 个有漂移(47%)**,其中 5 例 P1 +
已 wash 完成,代码层修复 + 长期对账机制随本 PR ship。

## Hotfix Bundle(按 commit 顺序)

| # | Commit | 修复内容 |
|---|---|---|
| #1 | `99b387aa5` | saga refund 现在会取消底层 Stripe
subscription(防止退款后订阅继续自动扣款) |
| #2 | `4bc281dcc` | `handle_invoice_paid` 拒绝已 canceled/expired/unpaid 的
sub(防止 webhook outage 期间堆积的事件 flush 后误授 entitlement) |
| #3 | `f86b87f8c` | `cancel-subscription` 端点对已死 sub 不再 500,转而同步 mongo
后返回 success(原报障的直接 fix) |
| #4 | `aae457800` | 新增 `charge.refunded` webhook handler,Dashboard
退款后兜底取消孤儿 sub |
| #5 | `1b38cfce2` | 周期性 reconciler cron(read-only 默认),pass-1 用户扫 +
pass-2 saga-orphan 订单扫 |

## Review 迭代(4 轮)

逐轮根据 review 反馈修补:

- `16f009443` — round 1(6 条):reconciler orphan_sub_drift
kind、partial-refund 检查、trial cron handover、cancel 端点 cron
handover、refund handler 标本地 order、webhook 配置 doc 同步
- `fe3c2aed5` — round 2(3 条):terminal status += {free, canceled}、refund
加 sub_id fallback、partial-refund doc reconcile
- `10055ef21` — round 3(3 条):past_due 走 status_drift + flip-to-active
handoff、initial-order helper 排除 RENEWAL、partial-refund doc 与代码对齐
- `653e78f70` — round 4(3 条 + simplify):incomplete_expired 进 cron
terminal、reconciler pass-2 over saga-refunded orders、refund invoice 异常不
fallback;refactor: tuple→dataclass、projection、删 inline review-round 注释
- `4fcaa3eae` — round 5(1 条):pass-2 query 排除
is_upgrade=True(防止误杀升级用户的当前订阅)

## 数据洗(已在调查会话内完成)

| Wash | 类别 | 数量 | 状态 |
|---|---|---|---|
| Wash 0 | D2 saga 孤儿 sub(uid=7453,deadline 5/13)| 3 | ✅ |
| Wash 1 | D1 白嫖用户完整 expire(uid=7420 / uid=7445)| 2 | ✅ |
| Wash 2 | D3 cap drift mongo 同步 | 4 | ✅ |
| Wash 3 | D4/D5 小漂移 | 2 | ✅ |
| Wash 5 | D7 内部账号清理 | 1 | ✅ |
| Wash 4 | D6 残留 sub_id | 15 | ⏳ reconciler 上线写模式后自动处理 |

## Test plan

- [x] 142 hotfix unit tests 全过(120 stripe + 22 subscription_cron)
- [x] ruff + pyright + import-linter + 项目所有 pre-commit checks 全过
- [x] 端到端验证:Wash 0/1/2/3/5 在 prod mongo 已实操执行,生产用户漂移已修
- [ ] CI `auto-review` + `build-and-test` 通过
- [ ] reconciler 部署后跑一周 read-only 模式,review GCP Logs `[DRIFT]` 标记后切到
write_mode

## 部署顺序(deadline 5/12 之前先 ship #1+#2)

按 RCA 文档时间线:
1. **5/12 EOD 之前**:Hotfix #1 + #2 deploy(避免 5/13 触发新一轮误授 + 防止 webhook
outage 类似事件再发)
2. 5/13-5/16:Hotfix #3 deploy
3. 5/17-5/23:Hotfix #4 deploy
4. 5/24-5/30:Hotfix #5 reconciler read-only 部署 + 触发首次扫描观察
5. 6 月初:reconciler 切 write_mode + 自动处理 D6 残留

## 关于 PR 体量

12 commits / ~3000+ 行净增 → 触发 husky pre-push 的 size 检查。本地用
`SKIP_PR_SIZE_CHECK=1` 跳过推上来,需要 reviewer 在这个 PR 上加 `size-override` label
让 CI 通过。

不拆 PR 的理由:4 轮 review 是按 file/line 精确反向修补的,拆开后 reviewer 无法看到完整的 review
迭代链(file-level diff 会把 round 1 vs round 4 混在一起)。Bundle 单一 PR 保留这条审计
trail。

## Linear


[ECA-643](https://linear.app/srpone/issue/ECA-643/stripe-mongo-订阅状态漂移-rca-修复)
```

### PR Body

## Summary

修复 ECA-643 报障 "Failed to cancel subscription. Please try again":挖出 2 个独立代码缺陷 + 1 次 webhook 域名 outage(已恢复)联合造成的 Stripe ↔ Mongo 状态漂移。完整 RCA + 修复方案见 [`docs/superpowers/specs/2026-05-08-stripe-mongo-drift-rca.md`](docs/superpowers/specs/2026-05-08-stripe-mongo-drift-rca.md)。

生产实测影响范围:53 个有 stripe_subscription_id 的用户中,**25 个有漂移(47%)**,其中 5 例 P1 + 已 wash 完成,代码层修复 + 长期对账机制随本 PR ship。

## Hotfix Bundle(按 commit 顺序)

| # | Commit | 修复内容 |
|---|---|---|
| #1 | `99b387aa5` | saga refund 现在会取消底层 Stripe subscription(防止退款后订阅继续自动扣款) |
| #2 | `4bc281dcc` | `handle_invoice_paid` 拒绝已 canceled/expired/unpaid 的 sub(防止 webhook outage 期间堆积的事件 flush 后误授 entitlement) |
| #3 | `f86b87f8c` | `cancel-subscription` 端点对已死 sub 不再 500,转而同步 mongo 后返回 success(原报障的直接 fix) |
| #4 | `aae457800` | 新增 `charge.refunded` webhook handler,Dashboard 退款后兜底取消孤儿 sub |
| #5 | `1b38cfce2` | 周期性 reconciler cron(read-only 默认),pass-1 用户扫 + pass-2 saga-orphan 订单扫 |

## Review 迭代(4 轮)

逐轮根据 review 反馈修补:

- `16f009443` — round 1(6 条):reconciler orphan_sub_drift kind、partial-refund 检查、trial cron handover、cancel 端点 cron handover、refund handler 标本地 order、webhook 配置 doc 同步
- `fe3c2aed5` — round 2(3 条):terminal status += {free, canceled}、refund 加 sub_id fallback、partial-refund doc reconcile
- `10055ef21` — round 3(3 条):past_due 走 status_drift + flip-to-active handoff、initial-order helper 排除 RENEWAL、partial-refund doc 与代码对齐
- `653e78f70` — round 4(3 条 + simplify):incomplete_expired 进 cron terminal、reconciler pass-2 over saga-refunded orders、refund invoice 异常不 fallback;refactor: tuple→dataclass、projection、删 inline review-round 注释
- `4fcaa3eae` — round 5(1 条):pass-2 query 排除 is_upgrade=True(防止误杀升级用户的当前订阅)

## 数据洗(已在调查会话内完成)

| Wash | 类别 | 数量 | 状态 |
|---|---|---|---|
| Wash 0 | D2 saga 孤儿 sub(uid=7453,deadline 5/13)| 3 | ✅ |
| Wash 1 | D1 白嫖用户完整 expire(uid=7420 / uid=7445)| 2 | ✅ |
| Wash 2 | D3 cap drift mongo 同步 | 4 | ✅ |
| Wash 3 | D4/D5 小漂移 | 2 | ✅ |
| Wash 5 | D7 内部账号清理 | 1 | ✅ |
| Wash 4 | D6 残留 sub_id | 15 | ⏳ reconciler 上线写模式后自动处理 |

## Test plan

- [x] 142 hotfix unit tests 全过(120 stripe + 22 subscription_cron)
- [x] ruff + pyright + import-linter + 项目所有 pre-commit checks 全过
- [x] 端到端验证:Wash 0/1/2/3/5 在 prod mongo 已实操执行,生产用户漂移已修
- [ ] CI `auto-review` + `build-and-test` 通过
- [ ] reconciler 部署后跑一周 read-only 模式,review GCP Logs `[DRIFT]` 标记后切到 write_mode

## 部署顺序(deadline 5/12 之前先 ship #1+#2)

按 RCA 文档时间线:
1. **5/12 EOD 之前**:Hotfix #1 + #2 deploy(避免 5/13 触发新一轮误授 + 防止 webhook outage 类似事件再发)
2. 5/13-5/16:Hotfix #3 deploy
3. 5/17-5/23:Hotfix #4 deploy
4. 5/24-5/30:Hotfix #5 reconciler read-only 部署 + 触发首次扫描观察
5. 6 月初:reconciler 切 write_mode + 自动处理 D6 残留

## 关于 PR 体量

12 commits / ~3000+ 行净增 → 触发 husky pre-push 的 size 检查。本地用 `SKIP_PR_SIZE_CHECK=1` 跳过推上来,需要 reviewer 在这个 PR 上加 `size-override` label 让 CI 通过。

不拆 PR 的理由:4 轮 review 是按 file/line 精确反向修补的,拆开后 reviewer 无法看到完整的 review 迭代链(file-level diff 会把 round 1 vs round 4 混在一起)。Bundle 单一 PR 保留这条审计 trail。

## Linear

[ECA-643](https://linear.app/srpone/issue/ECA-643/stripe-mongo-订阅状态漂移-rca-修复)


---

## 67716450 — refactor(claw-interface): introduce Account pydantic and retype user_repo reads (#1574)

- **Author**: bill-srp
- **Date**: 2026-05-09T02:53:52Z
- **SHA**: 677164506cc47fe1e5953e96381cd72eecf0ce1e
- **PR**: #1574

### Commit Message

```
refactor(claw-interface): introduce Account pydantic and retype user_repo reads (#1574)

## Summary

Introduces an `Account` Pydantic model for the `ecap-account` collection
and wires it through `user_repo`'s read API, replacing the previously
dict-typed reads. 13 atomic commits covering schema introduction,
write-side defaults that survive real Mongo data, production caller
migration, and test mock migration.

## What's in the PR

### 1. Schema (`app/schema/account.py`)

- Full Pydantic document model composed from per-domain sub-models
(identity, billing, OpenClaw, locale, connectors, referral). Reuses
`OpenClawAppRecord` / `OpenClawBotRecord` / `CustomAgentMeta` from
`app/schema/openclaw.py`. Mongo `_id` intentionally omitted; callers
identify via `uid`.
- **Defensive defaults** for fields that real production data treats as
optional, even when the JSON-schema sample marked them required:
- `user_type: str = "0"` — observed missing in legacy docs and BDD
fixtures.
- `AccountLocale.timezone` defaulted to `None` — the locale write path
(`routes/openclaw_settings/locale.py`) does conditional `$set`s, so a
country-only update produces a doc with `locale.country` but no
`locale.timezone`, and the same handler immediately re-reads the user.
- `AccountMetadata.{created_from, platform}` and
`GoogleConnectorExtra.scopes` similarly defaulted because their writers
can produce partial sub-docs.
- **`BeforeValidator(None → typed-default)`** on every
container/numeric/bool field (`permissions`, `preferences`,
`openclaw_bots`, `total_credits`, `billing_initialized`, etc.).
`default_factory=list` only fires for *absent* keys; a
present-but-`null` value would still ValidationError. Production data is
empirically clean (`countDocuments({field: null}) == 0` for
permissions/preferences/user_type — verified before merging) but this is
defense-in-depth against future regressions.

### 2. `user_repo` typed read API

- `user_repo.get_user(uid)` → `Account | None`
- `user_repo.get_by_stripe_customer_id(customer_id)` → `Account | None`
- `user_repo.get_by_phone_number(phone_number)` → `Account | None`
- `user_repo.get_by_apple_original_transaction_id(txn_id)` → `Account |
None` (moved here from `apple_notification_repo`; renamed for the
`get_by_*` consistency).

Internal validation: `Account.model_validate(doc) if doc else None`.

### 3. Production migration — 49 call sites across 24 files

**Pattern A (heavy dict mutation downstream — kept
`account.model_dump(exclude_unset=True)`):** auth/dependencies,
routes/user, routes/credits, services/billing, services/gift_code,
services/subscription_code, services/apple_subscription_manager,
services/subscription_manager, services/stripe/{entitlement,
billing_gateway, handlers/checkout}, services/openclaw/bot_token,
routes/{admin_boost, openclaw_admin, connectors, clawhub, orders,
openclaw_settings/{core, locale}}.

**Pattern B (simple-read attribute access — dropped `model_dump`):**
routes/admin_events, routes/orders (admin grant), routes/subscription,
routes/twilio, routes/openclaw_conversation,
routes/openclaw_settings/{locale, helpers}, services/connector_store,
services/bot_resources, services/openclaw/bot_token,
services/mattermost_reconcile, services/stripe/portal,
services/stripe/handlers/{trial, invoice, subscription}.

`exclude_unset=True` keeps the round-tripped dict shape close to the
source Mongo doc — avoids default-value pollution that would fool
field-presence checks like `backfill_timestamps`.

### 4. Test mock migration — ~80 setups across 27 unit test files + 1
BDD step file

- `_stripe_helpers.make_entitlement_user` / `make_portal_user` and
`_builders.make_account_user` updated to return `Account` (or include
`user_type="0"`).
- Inline `AsyncMock(return_value={...})` sites wrapped with
`Account.model_validate(...)`.
- BDD `then_user_has_field` step now coerces `bool → "true"/"false"`
before string comparison (Pydantic typed-coerces `"true"` → `True` on
read).

### 5. Apple webhook user lookup

`get_user_by_original_transaction_id` moved from
`apple_notification_repo` to `user_repo` as
`get_by_apple_original_transaction_id`. The function reads
`ecap-account` (an account lookup) and belongs in `user_repo`.
`apple_notification_repo` now owns only the `ecap-apple-notifications`
writes.

### 6. Devcontainer ergonomics (chore)

`SKIP_FRONTEND_DEPS` / `SKIP_PLAYWRIGHT` env passthroughs so
backend-only worktrees can skip `pnpm install` + Playwright browser
download. Documentation comment corrected to reflect that values flow
via `${localEnv:...}` from the host shell, not from
`.devcontainer/.env`.

## Why typed-at-the-boundary, not full attribute access everywhere

Downstream dict-mutation helpers (`strip_mongo_id`,
`backfill_timestamps`, `ensure_billing_initialized`,
`enrich_user_response`, `public_user_response`,
`extract_safe_user_fields`) are still dict-typed. Converting all of them
would cascade into a much larger refactor with broad blast radius.
Stopping at `account.model_dump(exclude_unset=True)` at each call site
captures the type check at the API surface where it matters (the repo
signature) and leaves room for incremental tightening per-helper later.
Pattern B sites that just read 1-3 attributes were converted to
attribute access for real type safety; Pattern A sites still go through
model_dump.

## Test plan

```bash
cd services/claw-interface
TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER= MONGODB_PASSWORD= pytest tests/unit/
```

- [x] All migration-related unit tests pass (**2918 / 2920** — 2
pre-existing failures only)
- [x] `ruff format --check . && ruff check .` clean
- [x] `pyright app/` clean — 0 errors
- [x] `lint-imports` — all 8 architecture contracts kept
- [x] BDD `test_stripe_webhook_dispatch` exercised through the typed
reads
- [x] Production data null-check for at-risk fields:
`db['ecap-account'].countDocuments({permissions|preferences|user_type:
null}) == 0`

Pre-existing infra failures (unrelated to this PR, verified via `git
stash` on a clean tree): `test_ci_lint_deptry::test_clean_tree_passes`
and `::test_violation_fails_the_build` — both fail with `fatal: not a
git repository: ...worktrees/service-pydantic` (host-absolute path in
`.git/worktrees/<n>/gitdir` doesn't resolve inside the devcontainer).

## Follow-ups (not in this PR)

- **`openclaw_repo.get_user` dedup** — verbatim duplicate of
`user_repo.get_user`. ~32 callers across openclaw routes/services would
need to switch import + handle the typed return. Attempted in-PR,
reverted because it pushed the diff past the reviewable threshold;
deserves its own focused PR.
- **`chat.py` / `canvas.py` direct `mongo.read_one`** — 4 sites in
`routes/session/{chat, canvas}.py` still bypass `user_repo` and read the
collection directly. Layering violations (`import-linter` C1 contract is
meant to catch these). Easy to migrate per-site once the openclaw work
merges.
- **`ensure_billing_initialized` retype** — gates ~10 of the remaining
`model_dump` calls. The largest single Pattern A → typed conversion
left.
- **Move misplaced setters**: `openclaw_repo.dec_credits` (credits
concern) and `openclaw_repo.set_locale_timezone` (locale concern) belong
in `user_repo` / a credits repo.
- **Tighten nested typing** (`Account.openclaw_app: dict` → typed
sub-record) once downstream helpers migrate to consume them.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body

## Summary

Introduces an `Account` Pydantic model for the `ecap-account` collection and wires it through `user_repo`'s read API, replacing the previously dict-typed reads. 13 atomic commits covering schema introduction, write-side defaults that survive real Mongo data, production caller migration, and test mock migration.

## What's in the PR

### 1. Schema (`app/schema/account.py`)

- Full Pydantic document model composed from per-domain sub-models (identity, billing, OpenClaw, locale, connectors, referral). Reuses `OpenClawAppRecord` / `OpenClawBotRecord` / `CustomAgentMeta` from `app/schema/openclaw.py`. Mongo `_id` intentionally omitted; callers identify via `uid`.
- **Defensive defaults** for fields that real production data treats as optional, even when the JSON-schema sample marked them required:
  - `user_type: str = "0"` — observed missing in legacy docs and BDD fixtures.
  - `AccountLocale.timezone` defaulted to `None` — the locale write path (`routes/openclaw_settings/locale.py`) does conditional `$set`s, so a country-only update produces a doc with `locale.country` but no `locale.timezone`, and the same handler immediately re-reads the user.
  - `AccountMetadata.{created_from, platform}` and `GoogleConnectorExtra.scopes` similarly defaulted because their writers can produce partial sub-docs.
- **`BeforeValidator(None → typed-default)`** on every container/numeric/bool field (`permissions`, `preferences`, `openclaw_bots`, `total_credits`, `billing_initialized`, etc.). `default_factory=list` only fires for *absent* keys; a present-but-`null` value would still ValidationError. Production data is empirically clean (`countDocuments({field: null}) == 0` for permissions/preferences/user_type — verified before merging) but this is defense-in-depth against future regressions.

### 2. `user_repo` typed read API

- `user_repo.get_user(uid)` → `Account | None`
- `user_repo.get_by_stripe_customer_id(customer_id)` → `Account | None`
- `user_repo.get_by_phone_number(phone_number)` → `Account | None`
- `user_repo.get_by_apple_original_transaction_id(txn_id)` → `Account | None` (moved here from `apple_notification_repo`; renamed for the `get_by_*` consistency).

Internal validation: `Account.model_validate(doc) if doc else None`.

### 3. Production migration — 49 call sites across 24 files

**Pattern A (heavy dict mutation downstream — kept `account.model_dump(exclude_unset=True)`):** auth/dependencies, routes/user, routes/credits, services/billing, services/gift_code, services/subscription_code, services/apple_subscription_manager, services/subscription_manager, services/stripe/{entitlement, billing_gateway, handlers/checkout}, services/openclaw/bot_token, routes/{admin_boost, openclaw_admin, connectors, clawhub, orders, openclaw_settings/{core, locale}}.

**Pattern B (simple-read attribute access — dropped `model_dump`):** routes/admin_events, routes/orders (admin grant), routes/subscription, routes/twilio, routes/openclaw_conversation, routes/openclaw_settings/{locale, helpers}, services/connector_store, services/bot_resources, services/openclaw/bot_token, services/mattermost_reconcile, services/stripe/portal, services/stripe/handlers/{trial, invoice, subscription}.

`exclude_unset=True` keeps the round-tripped dict shape close to the source Mongo doc — avoids default-value pollution that would fool field-presence checks like `backfill_timestamps`.

### 4. Test mock migration — ~80 setups across 27 unit test files + 1 BDD step file

- `_stripe_helpers.make_entitlement_user` / `make_portal_user` and `_builders.make_account_user` updated to return `Account` (or include `user_type="0"`).
- Inline `AsyncMock(return_value={...})` sites wrapped with `Account.model_validate(...)`.
- BDD `then_user_has_field` step now coerces `bool → "true"/"false"` before string comparison (Pydantic typed-coerces `"true"` → `True` on read).

### 5. Apple webhook user lookup

`get_user_by_original_transaction_id` moved from `apple_notification_repo` to `user_repo` as `get_by_apple_original_transaction_id`. The function reads `ecap-account` (an account lookup) and belongs in `user_repo`. `apple_notification_repo` now owns only the `ecap-apple-notifications` writes.

### 6. Devcontainer ergonomics (chore)

`SKIP_FRONTEND_DEPS` / `SKIP_PLAYWRIGHT` env passthroughs so backend-only worktrees can skip `pnpm install` + Playwright browser download. Documentation comment corrected to reflect that values flow via `${localEnv:...}` from the host shell, not from `.devcontainer/.env`.

## Why typed-at-the-boundary, not full attribute access everywhere

Downstream dict-mutation helpers (`strip_mongo_id`, `backfill_timestamps`, `ensure_billing_initialized`, `enrich_user_response`, `public_user_response`, `extract_safe_user_fields`) are still dict-typed. Converting all of them would cascade into a much larger refactor with broad blast radius. Stopping at `account.model_dump(exclude_unset=True)` at each call site captures the type check at the API surface where it matters (the repo signature) and leaves room for incremental tightening per-helper later. Pattern B sites that just read 1-3 attributes were converted to attribute access for real type safety; Pattern A sites still go through model_dump.

## Test plan

```bash
cd services/claw-interface
TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER= MONGODB_PASSWORD= pytest tests/unit/
```

- [x] All migration-related unit tests pass (**2918 / 2920** — 2 pre-existing failures only)
- [x] `ruff format --check . && ruff check .` clean
- [x] `pyright app/` clean — 0 errors
- [x] `lint-imports` — all 8 architecture contracts kept
- [x] BDD `test_stripe_webhook_dispatch` exercised through the typed reads
- [x] Production data null-check for at-risk fields: `db['ecap-account'].countDocuments({permissions|preferences|user_type: null}) == 0`

Pre-existing infra failures (unrelated to this PR, verified via `git stash` on a clean tree): `test_ci_lint_deptry::test_clean_tree_passes` and `::test_violation_fails_the_build` — both fail with `fatal: not a git repository: ...worktrees/service-pydantic` (host-absolute path in `.git/worktrees/<n>/gitdir` doesn't resolve inside the devcontainer).

## Follow-ups (not in this PR)

- **`openclaw_repo.get_user` dedup** — verbatim duplicate of `user_repo.get_user`. ~32 callers across openclaw routes/services would need to switch import + handle the typed return. Attempted in-PR, reverted because it pushed the diff past the reviewable threshold; deserves its own focused PR.
- **`chat.py` / `canvas.py` direct `mongo.read_one`** — 4 sites in `routes/session/{chat, canvas}.py` still bypass `user_repo` and read the collection directly. Layering violations (`import-linter` C1 contract is meant to catch these). Easy to migrate per-site once the openclaw work merges.
- **`ensure_billing_initialized` retype** — gates ~10 of the remaining `model_dump` calls. The largest single Pattern A → typed conversion left.
- **Move misplaced setters**: `openclaw_repo.dec_credits` (credits concern) and `openclaw_repo.set_locale_timezone` (locale concern) belong in `user_repo` / a credits repo.
- **Tighten nested typing** (`Account.openclaw_app: dict` → typed sub-record) once downstream helpers migrate to consume them.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## c221176c — chore(deps): update openai requirement from <2.34.0,>=2.32.0 to >=2.33.0,<2.34.0 in /services/claw-interface (#1578)

- **Author**: dependabot[bot]
- **Date**: 2026-05-09T02:41:21Z
- **SHA**: c221176c0cdecfabf2050e3618f55e4b4fabd5e8
- **PR**: #1578

### Commit Message

```
chore(deps): update openai requirement from <2.34.0,>=2.32.0 to >=2.33.0,<2.34.0 in /services/claw-interface (#1578)

Updates the requirements on
[openai](https://github.com/openai/openai-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/releases">openai's
releases</a>.</em></p>
<blockquote>
<h2>v2.33.0</h2>
<h2>2.33.0 (2026-04-28)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.32.0...v2.33.0">v2.32.0...v2.33.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> api update (<a
href="https://github.com/openai/openai-python/commit/18f834a54f92ea827452471a46a4f442f251e2c8">18f834a</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> correct prompt_cache_retention enum value from
in-memory to in_memory (<a
href="https://redirect.github.com/openai/openai-python/issues/1822">#1822</a>)
(<a
href="https://github.com/openai/openai-python/commit/f9d2d1359688a6247ecba858fc687173c480c9c8">f9d2d13</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>ci:</strong> remove release-doctor workflow (<a
href="https://github.com/openai/openai-python/commit/00b20910e3539842f21d86ab5928fb5216d3a765">00b2091</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's
changelog</a>.</em></p>
<blockquote>
<h2>2.33.0 (2026-04-28)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.32.0...v2.33.0">v2.32.0...v2.33.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> api update (<a
href="https://github.com/openai/openai-python/commit/18f834a54f92ea827452471a46a4f442f251e2c8">18f834a</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> correct prompt_cache_retention enum value from
in-memory to in_memory (<a
href="https://redirect.github.com/openai/openai-python/issues/1822">#1822</a>)
(<a
href="https://github.com/openai/openai-python/commit/f9d2d1359688a6247ecba858fc687173c480c9c8">f9d2d13</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>ci:</strong> remove release-doctor workflow (<a
href="https://github.com/openai/openai-python/commit/00b20910e3539842f21d86ab5928fb5216d3a765">00b2091</a>)</li>
</ul>
<h2>2.32.0 (2026-04-15)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.31.0...v2.32.0">v2.31.0...v2.32.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add detail to InputFileContent (<a
href="https://github.com/openai/openai-python/commit/60de21d1fcfbcadea0d9b8d884c73c9dc49d14ff">60de21d</a>)</li>
<li><strong>api:</strong> add OAuthErrorCode type (<a
href="https://github.com/openai/openai-python/commit/0c8d2c3b44242c9139dc554896ea489b56e236b8">0c8d2c3</a>)</li>
<li><strong>client:</strong> add event handler implementation for
websockets (<a
href="https://github.com/openai/openai-python/commit/0280d0568f706684ecbf0aabf3575cdcb7fd22d5">0280d05</a>)</li>
<li><strong>client:</strong> allow enqueuing to websockets even when not
connected (<a
href="https://github.com/openai/openai-python/commit/67aa20e69bc0e4a3b7694327c808606bfa24a966">67aa20e</a>)</li>
<li><strong>client:</strong> support reconnection in websockets (<a
href="https://github.com/openai/openai-python/commit/eb72a953ea9dc5beec3eef537be6eb32292c3f65">eb72a95</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>ensure file data are only sent as 1 parameter (<a
href="https://github.com/openai/openai-python/commit/c0c2ecd0f6b64fa5fafda6134bb06995b143a2cf">c0c2ecd</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>improve examples (<a
href="https://github.com/openai/openai-python/commit/84712fa0f094b53151a0fe6ac85aa98018b2a7e2">84712fa</a>)</li>
</ul>
<h2>2.31.0 (2026-04-08)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.30.0...v2.31.0">v2.30.0...v2.31.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add phase field to conversations message (<a
href="https://github.com/openai/openai-python/commit/3e5834efb39b24e019a29dc54d890c67d18cbb54">3e5834e</a>)</li>
<li><strong>api:</strong> add web_search_call.results to
ResponseIncludable type (<a
href="https://github.com/openai/openai-python/commit/ffd8741dd38609a5af0159ceb800d8ddba7925f8">ffd8741</a>)</li>
<li><strong>client:</strong> add support for short-lived tokens (<a
href="https://redirect.github.com/openai/openai-python/issues/1608">#1608</a>)
(<a
href="https://github.com/openai/openai-python/commit/22fe7228d4990c197cd721b3ad7931ad05cca5dd">22fe722</a>)</li>
<li><strong>client:</strong> support sending raw data over websockets
(<a
href="https://github.com/openai/openai-python/commit/f1bc52ef641dfca6fdf2a5b00ce3b09bff2552f5">f1bc52e</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/openai/openai-python/commit/94c88b80b9811f23c4494c414758358243d7e2e6"><code>94c88b8</code></a>
release: 2.33.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3119">#3119</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/c5b099cf9f08e2b0cda02a68f8cbfadbc35da4de"><code>c5b099c</code></a>
release: 2.33.0</li>
<li><a
href="https://github.com/openai/openai-python/commit/cb63de72923d89de4ba870e329038f99e10eb9dd"><code>cb63de7</code></a>
codegen metadata</li>
<li><a
href="https://github.com/openai/openai-python/commit/18f834a54f92ea827452471a46a4f442f251e2c8"><code>18f834a</code></a>
feat(api): api update</li>
<li><a
href="https://github.com/openai/openai-python/commit/00b20910e3539842f21d86ab5928fb5216d3a765"><code>00b2091</code></a>
chore(ci): remove release-doctor workflow</li>
<li><a
href="https://github.com/openai/openai-python/commit/f9d2d1359688a6247ecba858fc687173c480c9c8"><code>f9d2d13</code></a>
fix(api): correct prompt_cache_retention enum value from in-memory to
in_memo...</li>
<li>See full diff in <a
href="https://github.com/openai/openai-python/compare/v2.32.0...v2.33.0">compare
view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Body

Updates the requirements on [openai](https://github.com/openai/openai-python) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/releases">openai's releases</a>.</em></p>
<blockquote>
<h2>v2.33.0</h2>
<h2>2.33.0 (2026-04-28)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.32.0...v2.33.0">v2.32.0...v2.33.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> api update (<a href="https://github.com/openai/openai-python/commit/18f834a54f92ea827452471a46a4f442f251e2c8">18f834a</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> correct prompt_cache_retention enum value from in-memory to in_memory (<a href="https://redirect.github.com/openai/openai-python/issues/1822">#1822</a>) (<a href="https://github.com/openai/openai-python/commit/f9d2d1359688a6247ecba858fc687173c480c9c8">f9d2d13</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>ci:</strong> remove release-doctor workflow (<a href="https://github.com/openai/openai-python/commit/00b20910e3539842f21d86ab5928fb5216d3a765">00b2091</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's changelog</a>.</em></p>
<blockquote>
<h2>2.33.0 (2026-04-28)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.32.0...v2.33.0">v2.32.0...v2.33.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> api update (<a href="https://github.com/openai/openai-python/commit/18f834a54f92ea827452471a46a4f442f251e2c8">18f834a</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> correct prompt_cache_retention enum value from in-memory to in_memory (<a href="https://redirect.github.com/openai/openai-python/issues/1822">#1822</a>) (<a href="https://github.com/openai/openai-python/commit/f9d2d1359688a6247ecba858fc687173c480c9c8">f9d2d13</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>ci:</strong> remove release-doctor workflow (<a href="https://github.com/openai/openai-python/commit/00b20910e3539842f21d86ab5928fb5216d3a765">00b2091</a>)</li>
</ul>
<h2>2.32.0 (2026-04-15)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.31.0...v2.32.0">v2.31.0...v2.32.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add detail to InputFileContent (<a href="https://github.com/openai/openai-python/commit/60de21d1fcfbcadea0d9b8d884c73c9dc49d14ff">60de21d</a>)</li>
<li><strong>api:</strong> add OAuthErrorCode type (<a href="https://github.com/openai/openai-python/commit/0c8d2c3b44242c9139dc554896ea489b56e236b8">0c8d2c3</a>)</li>
<li><strong>client:</strong> add event handler implementation for websockets (<a href="https://github.com/openai/openai-python/commit/0280d0568f706684ecbf0aabf3575cdcb7fd22d5">0280d05</a>)</li>
<li><strong>client:</strong> allow enqueuing to websockets even when not connected (<a href="https://github.com/openai/openai-python/commit/67aa20e69bc0e4a3b7694327c808606bfa24a966">67aa20e</a>)</li>
<li><strong>client:</strong> support reconnection in websockets (<a href="https://github.com/openai/openai-python/commit/eb72a953ea9dc5beec3eef537be6eb32292c3f65">eb72a95</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li>ensure file data are only sent as 1 parameter (<a href="https://github.com/openai/openai-python/commit/c0c2ecd0f6b64fa5fafda6134bb06995b143a2cf">c0c2ecd</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>improve examples (<a href="https://github.com/openai/openai-python/commit/84712fa0f094b53151a0fe6ac85aa98018b2a7e2">84712fa</a>)</li>
</ul>
<h2>2.31.0 (2026-04-08)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.30.0...v2.31.0">v2.30.0...v2.31.0</a></p>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> add phase field to conversations message (<a href="https://github.com/openai/openai-python/commit/3e5834efb39b24e019a29dc54d890c67d18cbb54">3e5834e</a>)</li>
<li><strong>api:</strong> add web_search_call.results to ResponseIncludable type (<a href="https://github.com/openai/openai-python/commit/ffd8741dd38609a5af0159ceb800d8ddba7925f8">ffd8741</a>)</li>
<li><strong>client:</strong> add support for short-lived tokens (<a href="https://redirect.github.com/openai/openai-python/issues/1608">#1608</a>) (<a href="https://github.com/openai/openai-python/commit/22fe7228d4990c197cd721b3ad7931ad05cca5dd">22fe722</a>)</li>
<li><strong>client:</strong> support sending raw data over websockets (<a href="https://github.com/openai/openai-python/commit/f1bc52ef641dfca6fdf2a5b00ce3b09bff2552f5">f1bc52e</a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/openai/openai-python/commit/94c88b80b9811f23c4494c414758358243d7e2e6"><code>94c88b8</code></a> release: 2.33.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3119">#3119</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/c5b099cf9f08e2b0cda02a68f8cbfadbc35da4de"><code>c5b099c</code></a> release: 2.33.0</li>
<li><a href="https://github.com/openai/openai-python/commit/cb63de72923d89de4ba870e329038f99e10eb9dd"><code>cb63de7</code></a> codegen metadata</li>
<li><a href="https://github.com/openai/openai-python/commit/18f834a54f92ea827452471a46a4f442f251e2c8"><code>18f834a</code></a> feat(api): api update</li>
<li><a href="https://github.com/openai/openai-python/commit/00b20910e3539842f21d86ab5928fb5216d3a765"><code>00b2091</code></a> chore(ci): remove release-doctor workflow</li>
<li><a href="https://github.com/openai/openai-python/commit/f9d2d1359688a6247ecba858fc687173c480c9c8"><code>f9d2d13</code></a> fix(api): correct prompt_cache_retention enum value from in-memory to in_memo...</li>
<li>See full diff in <a href="https://github.com/openai/openai-python/compare/v2.32.0...v2.33.0">compare view</a></li>
</ul>
</details>
<br />


Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

---

## 2b2e3685 — chore(deps-dev): bump wrangler from 3.114.17 to 4.85.0 in /web (#1577)

- **Author**: dependabot[bot]
- **Date**: 2026-05-09T02:40:39Z
- **SHA**: 2b2e36856deaaf8fe358ddcea180f2a91cced4d4
- **PR**: #1577

### Commit Message

```
chore(deps-dev): bump wrangler from 3.114.17 to 4.85.0 in /web (#1577)

Bumps
[wrangler](https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler)
from 3.114.17 to 4.85.0.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/cloudflare/workers-sdk/releases">wrangler's
releases</a>.</em></p>
<blockquote>
<h2>wrangler@4.85.0</h2>
<h3>Minor Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13222">#13222</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/56802879641c123ee11160d77ecaf104915cd826"><code>5680287</code></a>
Thanks <a
href="https://github.com/maxwellpeterson"><code>@​maxwellpeterson</code></a>!
- Add enabled and previews_enabled support for custom domain routes</p>
<p>Custom domain routes can now include optional <code>enabled</code>
and <code>previews_enabled</code> boolean fields to control whether a
custom domain serves production and/or preview traffic. When omitted,
the API defaults apply (production enabled, previews disabled).</p>
</li>
</ul>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13622">#13622</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/5a2968ab69dd3d42ddf532fc547236a2f034874d"><code>5a2968a</code></a>
Thanks <a
href="https://github.com/petebacondarwin"><code>@​petebacondarwin</code></a>!
- Fix inherited <code>ai_search_namespaces</code> binding display in
<code>wrangler deploy</code></p>
<p>When an <code>ai_search_namespaces</code> binding inherits from the
existing deployment, the bindings table now correctly shows
<code>(inherited)</code> instead of a raw
<code>Symbol(inherit_binding)</code> string.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13633">#13633</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/34948423c4d873a3b493091b2a39ae9ed389bb67"><code>3494842</code></a>
Thanks <a
href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>!
- Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260421.1</td>
<td>1.20260422.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13645">#13645</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/7d728fbca56a58b621767c83f734c1daf3e11c41"><code>7d728fb</code></a>
Thanks <a
href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>!
- Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260422.1</td>
<td>1.20260423.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13657">#13657</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/df9319d3c302866db7972ec5636a80d041e80900"><code>df9319d</code></a>
Thanks <a
href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>!
- Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260423.1</td>
<td>1.20260424.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13574">#13574</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/d5e3c57207f2c76defee1878c3cfaa8ca41dbcc7"><code>d5e3c57</code></a>
Thanks <a
href="https://github.com/dario-piotrowicz"><code>@​dario-piotrowicz</code></a>!
- Detect Cloudflare WAF block pages and include Ray ID in API error
messages</p>
<p>When the Cloudflare WAF blocks an API request, the response is an
HTML page rather than JSON. Previously, this caused a confusing
&quot;Received a malformed response from the API&quot; error with a
truncated HTML snippet. Wrangler now detects WAF block pages and
displays a clear error message explaining that the request was blocked
by the firewall, along with the Cloudflare Ray ID (when available) for
use in support tickets.</p>
<p>For other non-JSON responses that aren't WAF blocks, the
&quot;malformed response&quot; error also now includes the Ray ID to
help reference failing requests in support tickets.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13560">#13560</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/7567ef703f1bf157ef29e6d19dd0dd9f1ff8771f"><code>7567ef7</code></a>
Thanks <a
href="https://github.com/vaishnav-mk"><code>@​vaishnav-mk</code></a>! -
Preserve NonRetryableError message and name when the
<code>workflows_preserve_non_retryable_error_message</code>
compatibility flag is enabled, instead of replacing it with a generic
error message.</p>
</li>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/11784">#11784</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/2831b545efe86c71fe1930909ca9e891c27a0722"><code>2831b54</code></a>
Thanks <a
href="https://github.com/JPeer264"><code>@​JPeer264</code></a>! -
fix(wrangler): Bind the console methods directly instead of using a
global proxy</p>
</li>
<li>
<p><a
href="https://redirect.github.com/cloudflare/workers-sdk/pull/13644">#13644</a>
<a
href="https://github.com/cloudflare/workers-sdk/commit/377715d9f6ec7f3428e12a6ce56b367984fb0673"><code>377715d</code></a>
Thanks <a
href="https://github.com/MattieTK"><code>@​MattieTK</code></a>! - Update
<code>@clack/core</code> and <code>@clack/prompts</code> to v1.2.0</p>
<p>Bumps the bundled <code>@clack/core</code> dependency used internally
by <code>@cloudflare/cli</code> from <code>0.3.x</code> to
<code>1.2.0</code>, and the <code>@clack/prompts</code> dependency in
<code>create-cloudflare</code> from <code>0.6.x</code> to
<code>1.2.0</code>. Clack v1 includes a number of API changes, but no
user-facing prompt behaviour changes are expected.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/a3f648171ff9d0325848355dfd654c7ac9a9be61"><code>a3f6481</code></a>
Version Packages (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13625">#13625</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/47ac63f05ca86d781110490ff21ff88f2828fbbf"><code>47ac63f</code></a>
Publish <code>@cloudflare/cli-shared-helpers</code> and
<code>@cloudflare/workers-utils</code> to n...</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/df9319d3c302866db7972ec5636a80d041e80900"><code>df9319d</code></a>
chore(deps): bump the workerd-and-workers-types group with 2 updates (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13657">#13657</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/2831b545efe86c71fe1930909ca9e891c27a0722"><code>2831b54</code></a>
fix(wrangler): Bind the console methods directly instead of using a
global pr...</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/56802879641c123ee11160d77ecaf104915cd826"><code>5680287</code></a>
[wrangler] Add enabled and previews_enabled options for custom domains
(<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13222">#13222</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/7d728fbca56a58b621767c83f734c1daf3e11c41"><code>7d728fb</code></a>
chore(deps): bump the workerd-and-workers-types group with 2 updates (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13645">#13645</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/6e99feb9c8a883cc41caa6fadca8a283fc302d97"><code>6e99feb</code></a>
[vite-plugin-cloudflare] Support Cloudflare registry images in Vite dev
(<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13611">#13611</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/7567ef703f1bf157ef29e6d19dd0dd9f1ff8771f"><code>7567ef7</code></a>
fix: preserve NonRetryableError message when compat flag is enabled (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13560">#13560</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/5a2968ab69dd3d42ddf532fc547236a2f034874d"><code>5a2968a</code></a>
[wrangler] Fix inherited ai_search_namespaces binding display (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13622">#13622</a>)</li>
<li><a
href="https://github.com/cloudflare/workers-sdk/commit/34948423c4d873a3b493091b2a39ae9ed389bb67"><code>3494842</code></a>
chore(deps): bump the workerd-and-workers-types group with 2 updates (<a
href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13633">#13633</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/cloudflare/workers-sdk/commits/wrangler@4.85.0/packages/wrangler">compare
view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility
score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=wrangler&package-manager=npm_and_yarn&previous-version=3.114.17&new-version=4.85.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop
Dependabot creating any more for this major version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop
Dependabot creating any more for this minor version (unless you reopen
the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop
Dependabot creating any more for this dependency (unless you reopen the
PR or upgrade to it yourself)


</details>

---------

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
Co-authored-by: github-actions[bot] <41898282+github-actions[bot]@users.noreply.github.com>
```

### PR Body

Bumps [wrangler](https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler) from 3.114.17 to 4.85.0.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/cloudflare/workers-sdk/releases">wrangler's releases</a>.</em></p>
<blockquote>
<h2>wrangler@4.85.0</h2>
<h3>Minor Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13222">#13222</a> <a href="https://github.com/cloudflare/workers-sdk/commit/56802879641c123ee11160d77ecaf104915cd826"><code>5680287</code></a> Thanks <a href="https://github.com/maxwellpeterson"><code>@​maxwellpeterson</code></a>! - Add enabled and previews_enabled support for custom domain routes</p>
<p>Custom domain routes can now include optional <code>enabled</code> and <code>previews_enabled</code> boolean fields to control whether a custom domain serves production and/or preview traffic. When omitted, the API defaults apply (production enabled, previews disabled).</p>
</li>
</ul>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13622">#13622</a> <a href="https://github.com/cloudflare/workers-sdk/commit/5a2968ab69dd3d42ddf532fc547236a2f034874d"><code>5a2968a</code></a> Thanks <a href="https://github.com/petebacondarwin"><code>@​petebacondarwin</code></a>! - Fix inherited <code>ai_search_namespaces</code> binding display in <code>wrangler deploy</code></p>
<p>When an <code>ai_search_namespaces</code> binding inherits from the existing deployment, the bindings table now correctly shows <code>(inherited)</code> instead of a raw <code>Symbol(inherit_binding)</code> string.</p>
</li>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13633">#13633</a> <a href="https://github.com/cloudflare/workers-sdk/commit/34948423c4d873a3b493091b2a39ae9ed389bb67"><code>3494842</code></a> Thanks <a href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>! - Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260421.1</td>
<td>1.20260422.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13645">#13645</a> <a href="https://github.com/cloudflare/workers-sdk/commit/7d728fbca56a58b621767c83f734c1daf3e11c41"><code>7d728fb</code></a> Thanks <a href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>! - Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260422.1</td>
<td>1.20260423.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13657">#13657</a> <a href="https://github.com/cloudflare/workers-sdk/commit/df9319d3c302866db7972ec5636a80d041e80900"><code>df9319d</code></a> Thanks <a href="https://github.com/apps/dependabot"><code>@​dependabot</code></a>! - Update dependencies of &quot;miniflare&quot;, &quot;wrangler&quot;</p>
<p>The following dependency versions have been updated:</p>
<table>
<thead>
<tr>
<th>Dependency</th>
<th>From</th>
<th>To</th>
</tr>
</thead>
<tbody>
<tr>
<td>workerd</td>
<td>1.20260423.1</td>
<td>1.20260424.1</td>
</tr>
</tbody>
</table>
</li>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13574">#13574</a> <a href="https://github.com/cloudflare/workers-sdk/commit/d5e3c57207f2c76defee1878c3cfaa8ca41dbcc7"><code>d5e3c57</code></a> Thanks <a href="https://github.com/dario-piotrowicz"><code>@​dario-piotrowicz</code></a>! - Detect Cloudflare WAF block pages and include Ray ID in API error messages</p>
<p>When the Cloudflare WAF blocks an API request, the response is an HTML page rather than JSON. Previously, this caused a confusing &quot;Received a malformed response from the API&quot; error with a truncated HTML snippet. Wrangler now detects WAF block pages and displays a clear error message explaining that the request was blocked by the firewall, along with the Cloudflare Ray ID (when available) for use in support tickets.</p>
<p>For other non-JSON responses that aren't WAF blocks, the &quot;malformed response&quot; error also now includes the Ray ID to help reference failing requests in support tickets.</p>
</li>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13560">#13560</a> <a href="https://github.com/cloudflare/workers-sdk/commit/7567ef703f1bf157ef29e6d19dd0dd9f1ff8771f"><code>7567ef7</code></a> Thanks <a href="https://github.com/vaishnav-mk"><code>@​vaishnav-mk</code></a>! - Preserve NonRetryableError message and name when the <code>workflows_preserve_non_retryable_error_message</code> compatibility flag is enabled, instead of replacing it with a generic error message.</p>
</li>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/11784">#11784</a> <a href="https://github.com/cloudflare/workers-sdk/commit/2831b545efe86c71fe1930909ca9e891c27a0722"><code>2831b54</code></a> Thanks <a href="https://github.com/JPeer264"><code>@​JPeer264</code></a>! - fix(wrangler): Bind the console methods directly instead of using a global proxy</p>
</li>
<li>
<p><a href="https://redirect.github.com/cloudflare/workers-sdk/pull/13644">#13644</a> <a href="https://github.com/cloudflare/workers-sdk/commit/377715d9f6ec7f3428e12a6ce56b367984fb0673"><code>377715d</code></a> Thanks <a href="https://github.com/MattieTK"><code>@​MattieTK</code></a>! - Update <code>@clack/core</code> and <code>@clack/prompts</code> to v1.2.0</p>
<p>Bumps the bundled <code>@clack/core</code> dependency used internally by <code>@cloudflare/cli</code> from <code>0.3.x</code> to <code>1.2.0</code>, and the <code>@clack/prompts</code> dependency in <code>create-cloudflare</code> from <code>0.6.x</code> to <code>1.2.0</code>. Clack v1 includes a number of API changes, but no user-facing prompt behaviour changes are expected.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/a3f648171ff9d0325848355dfd654c7ac9a9be61"><code>a3f6481</code></a> Version Packages (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13625">#13625</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/47ac63f05ca86d781110490ff21ff88f2828fbbf"><code>47ac63f</code></a> Publish <code>@cloudflare/cli-shared-helpers</code> and <code>@cloudflare/workers-utils</code> to n...</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/df9319d3c302866db7972ec5636a80d041e80900"><code>df9319d</code></a> chore(deps): bump the workerd-and-workers-types group with 2 updates (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13657">#13657</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/2831b545efe86c71fe1930909ca9e891c27a0722"><code>2831b54</code></a> fix(wrangler): Bind the console methods directly instead of using a global pr...</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/56802879641c123ee11160d77ecaf104915cd826"><code>5680287</code></a> [wrangler] Add enabled and previews_enabled options for custom domains (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13222">#13222</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/7d728fbca56a58b621767c83f734c1daf3e11c41"><code>7d728fb</code></a> chore(deps): bump the workerd-and-workers-types group with 2 updates (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13645">#13645</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/6e99feb9c8a883cc41caa6fadca8a283fc302d97"><code>6e99feb</code></a> [vite-plugin-cloudflare] Support Cloudflare registry images in Vite dev (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13611">#13611</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/7567ef703f1bf157ef29e6d19dd0dd9f1ff8771f"><code>7567ef7</code></a> fix: preserve NonRetryableError message when compat flag is enabled (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13560">#13560</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/5a2968ab69dd3d42ddf532fc547236a2f034874d"><code>5a2968a</code></a> [wrangler] Fix inherited ai_search_namespaces binding display (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13622">#13622</a>)</li>
<li><a href="https://github.com/cloudflare/workers-sdk/commit/34948423c4d873a3b493091b2a39ae9ed389bb67"><code>3494842</code></a> chore(deps): bump the workerd-and-workers-types group with 2 updates (<a href="https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler/issues/13633">#13633</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/cloudflare/workers-sdk/commits/wrangler@4.85.0/packages/wrangler">compare view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=wrangler&package-manager=npm_and_yarn&previous-version=3.114.17&new-version=4.85.0)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore this major version` will close this PR and stop Dependabot creating any more for this major version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this minor version` will close this PR and stop Dependabot creating any more for this minor version (unless you reopen the PR or upgrade to it yourself)
- `@dependabot ignore this dependency` will close this PR and stop Dependabot creating any more for this dependency (unless you reopen the PR or upgrade to it yourself)


</details>

