# ecap-workspace - 2026-06-01

共 7 条 commits

---

## [8d5d921] fix(claw-interface): avoid channel probes during agent hire readiness (#2146)

- **SHA**: 8d5d9218c4bfee43a0cc4b7f85b67f962c19b054
- **作者**: sam-srp
- **日期**: 2026-06-01T12:58:37Z
- **PR**: #2146

### 完整 Commit Message

```
fix(claw-interface): avoid channel probes during agent hire readiness (#2146)

## Summary

- Stop using active Mattermost channel probes while waiting for a newly
hired agent to become ready.
- Use the OpenClaw runtime channel status snapshot instead, still
requiring the target account to be running, connected, and error-free
before sending the activation message.
- Update the unit expectation for the install activation path.

## Root cause

The hire flow wrote the new OpenClaw config and immediately called
`channels.status` with `probe=true`. That active probe could run before
hot reload completed, become an active gateway RPC, and delay reload
deferral. In production this showed up as a long `channels.status` call
blocking Mattermost channel reload.

## Validation

- `conda run -n base pytest
tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_install_runs_shared_deploy_pipeline_for_custom_agent
tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_waits_for_specific_mattermost_account
tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_skips_post_when_specific_mattermost_account_times_out
-q`

Note: running the full `test_openclaw_agents.py` file hit unrelated
existing tests that reached real OpenClaw/Mattermost endpoints and
produced socket warnings; the targeted activation tests pass.
```

### PR Body

## Summary

- Stop using active Mattermost channel probes while waiting for a newly hired agent to become ready.
- Use the OpenClaw runtime channel status snapshot instead, still requiring the target account to be running, connected, and error-free before sending the activation message.
- Update the unit expectation for the install activation path.

## Root cause

The hire flow wrote the new OpenClaw config and immediately called `channels.status` with `probe=true`. That active probe could run before hot reload completed, become an active gateway RPC, and delay reload deferral. In production this showed up as a long `channels.status` call blocking Mattermost channel reload.

## Validation

- `conda run -n base pytest tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_install_runs_shared_deploy_pipeline_for_custom_agent tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_waits_for_specific_mattermost_account tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_skips_post_when_specific_mattermost_account_times_out -q`

Note: running the full `test_openclaw_agents.py` file hit unrelated existing tests that reached real OpenClaw/Mattermost endpoints and produced socket warnings; the targeted activation tests pass.


---

## [8376b38] fix(billing): resolve apple product ids by environment (#2143)

- **SHA**: 8376b3871c69d3620e54eec5cb39e59c3cbbd54a
- **作者**: kaka-srp
- **日期**: 2026-06-01T08:24:02Z
- **PR**: #2143

### 完整 Commit Message

```
fix(billing): resolve apple product ids by environment (#2143)

## Summary
- Centralize Apple subscription product ID parsing in a shared backend
helper.
- Use production product IDs for production Apple transactions and
`com.zooclaw.staging.sub.*` for sandbox/non-production Apple
transactions.
- Apply the same product catalog to legacy Apple subscription handling
and Billing v2 transaction claims, including yearly Pro/Ultra coverage.

## Root cause
Apple product IDs were hard-coded in multiple backend paths and always
used production IDs, while staging/sandbox needs a separate product
namespace. The legacy Apple manager also had an incomplete product map.

## Review follow-up
- Fixed the Codex review blocker: product resolution now uses the
verified Apple transaction environment when available, so production
backend TestFlight/Sandbox fallback still accepts staging product IDs.
- Production Apple transactions still reject staging product IDs, and
sandbox Apple transactions reject production product IDs.

## Linear

https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-payment-refactor

## Test plan
- [x] `cd services/claw-interface && ruff format --check
app/services/apple/products.py
app/services/apple/billing_v2_transactions.py
app/services/apple_subscription_manager.py
tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py
tests/bdd/step_defs/test_apple_subscription.py
tests/unit/test_subscription_cron.py`
- [x] `cd services/claw-interface && ruff check
app/services/apple/products.py
app/services/apple/billing_v2_transactions.py
app/services/apple_subscription_manager.py
tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py
tests/bdd/step_defs/test_apple_subscription.py
tests/unit/test_subscription_cron.py`
- [x] `cd services/claw-interface && pyright
app/services/apple/products.py
app/services/apple/billing_v2_transactions.py
app/services/apple_subscription_manager.py
tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py
tests/bdd/step_defs/test_apple_subscription.py
tests/unit/test_subscription_cron.py`
- [x] `cd services/claw-interface && pytest -q
tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py
tests/unit/test_subscription_cron.py -q` # 86 passed
```

### PR Body

## Summary
- Centralize Apple subscription product ID parsing in a shared backend helper.
- Use production product IDs for production Apple transactions and `com.zooclaw.staging.sub.*` for sandbox/non-production Apple transactions.
- Apply the same product catalog to legacy Apple subscription handling and Billing v2 transaction claims, including yearly Pro/Ultra coverage.

## Root cause
Apple product IDs were hard-coded in multiple backend paths and always used production IDs, while staging/sandbox needs a separate product namespace. The legacy Apple manager also had an incomplete product map.

## Review follow-up
- Fixed the Codex review blocker: product resolution now uses the verified Apple transaction environment when available, so production backend TestFlight/Sandbox fallback still accepts staging product IDs.
- Production Apple transactions still reject staging product IDs, and sandbox Apple transactions reject production product IDs.

## Linear
https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-payment-refactor

## Test plan
- [x] `cd services/claw-interface && ruff format --check app/services/apple/products.py app/services/apple/billing_v2_transactions.py app/services/apple_subscription_manager.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py tests/bdd/step_defs/test_apple_subscription.py tests/unit/test_subscription_cron.py`
- [x] `cd services/claw-interface && ruff check app/services/apple/products.py app/services/apple/billing_v2_transactions.py app/services/apple_subscription_manager.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py tests/bdd/step_defs/test_apple_subscription.py tests/unit/test_subscription_cron.py`
- [x] `cd services/claw-interface && pyright app/services/apple/products.py app/services/apple/billing_v2_transactions.py app/services/apple_subscription_manager.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py tests/bdd/step_defs/test_apple_subscription.py tests/unit/test_subscription_cron.py`
- [x] `cd services/claw-interface && pytest -q tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py tests/unit/test_subscription_cron.py -q`  # 86 passed


---

## [7fe2da1] fix(login): add phone consent copy (#2142)

- **SHA**: 7fe2da1a525b6800a84caedf3d1eee81cd006c73
- **作者**: sam-srp
- **日期**: 2026-06-01T07:35:27Z
- **PR**: #2142

### 完整 Commit Message

```
fix(login): add phone consent copy (#2142)

## Summary
- Add the required SMS consent/update copy to the phone login form
before the Continue button.
- Style the copy as muted, compact helper text with each compliance line
on its own row.
- Cover the phone-login copy in the existing LoginForm unit spec.

## Validation
- `git diff --check -- web/app/src/components/LoginForm.tsx
web/app/src/components/login.css
web/app/tests/unit/components/LoginForm.unit.spec.tsx` passed.
- Rendered `http://localhost:3000` locally and verified the phone login
modal shows all three consent lines before Continue.
- Attempted unit validation locally, but this checkout is running Node
`v25.6.1` while `@zooclaw/web-app` requires `>=24 <25`; Vitest/jsdom
fails before tests with `window.localStorage.* is not a function` /
`--localstorage-file` warnings. No test failures specific to this change
were observed.
```

### PR Body

## Summary
- Add the required SMS consent/update copy to the phone login form before the Continue button.
- Style the copy as muted, compact helper text with each compliance line on its own row.
- Cover the phone-login copy in the existing LoginForm unit spec.

## Validation
- `git diff --check -- web/app/src/components/LoginForm.tsx web/app/src/components/login.css web/app/tests/unit/components/LoginForm.unit.spec.tsx` passed.
- Rendered `http://localhost:3000` locally and verified the phone login modal shows all three consent lines before Continue.
- Attempted unit validation locally, but this checkout is running Node `v25.6.1` while `@zooclaw/web-app` requires `>=24 <25`; Vitest/jsdom fails before tests with `window.localStorage.* is not a function` / `--localstorage-file` warnings. No test failures specific to this change were observed.


---

## [e78744f] refactor(billing): route v2 init through profiles (#2138)

- **SHA**: e78744fbe21e060ba1f0d88aaf41654a1c740bf8
- **作者**: kaka-srp
- **日期**: 2026-06-01T06:16:59Z
- **PR**: #2138

### 完整 Commit Message

```
refactor(billing): route v2 init through profiles (#2138)

## Summary
- Route Billing v2 ensure/init through Billing Profile storage instead
of persisting legacy billing fields on ecap-account.
- Materialize warm-pool billing assets into Billing Profiles under the
v2 cutover flags while keeping ecap-account clean.
- Keep warm-pool pre-initialization user-only: it bootstraps billing
key/wallets but does not create a personal team until real personal-org
creation.
- Add trial/topup fulfillment, account creation, docs, and tests for the
v2 init cutover path.

## Linear

https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-payment-refactor

## Review follow-up
- Fixed fulfillment so reads/writes-disabled paths do not backfill or
initialize Billing Profiles.
- Fixed /account register response overlay so Billing v2 profile facts
are request-scope only and ecap-account remains clean.
- Fixed bootstrap team selection so personal-team responses are
authoritative for normal registration, while warm-pool preinit
explicitly skips personal team creation.
- Fixed trial entitlement fulfillment so open-registration trial credits
top up the subscription wallet without subscribing the user to the paid
starter BG plan.
- Made legacy billing initialization unit tests independent of
CI/staging v2 flag values.

## Verification
- cd services/claw-interface && ruff format --check
app/services/billing_key_bootstrap.py app/services/warm_pool_billing.py
app/services/user/warm_pool.py app/services/billing_v2/fulfillment.py
app/services/user/account_service.py
tests/unit/test_billing_key_bootstrap.py
tests/unit/test_billing_warm_pool.py
tests/unit/test_warm_pool_materialization.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_account_service.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_user_billing.py
- cd services/claw-interface && ruff check
app/services/billing_key_bootstrap.py app/services/warm_pool_billing.py
app/services/user/warm_pool.py app/services/billing_v2/fulfillment.py
app/services/user/account_service.py
tests/unit/test_billing_key_bootstrap.py
tests/unit/test_billing_warm_pool.py
tests/unit/test_warm_pool_materialization.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_account_service.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_user_billing.py
- cd services/claw-interface && pyright
app/services/billing_key_bootstrap.py app/services/warm_pool_billing.py
app/services/user/warm_pool.py app/services/billing_v2/fulfillment.py
app/services/user/account_service.py
tests/unit/test_billing_key_bootstrap.py
tests/unit/test_billing_warm_pool.py
tests/unit/test_warm_pool_materialization.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_account_service.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_user_billing.py
- cd services/claw-interface && pytest
tests/unit/test_account_builder.py tests/unit/test_account_service.py
tests/unit/test_billing_profiles_v2.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_billing_key_bootstrap.py
tests/unit/test_billing_warm_pool.py tests/unit/test_user_billing.py
tests/unit/test_warm_pool_materialization.py
tests/unit/test_user_trial_credits_service.py
tests/unit/test_billing_v2_fulfillment.py -q # 125 passed
- cd services/claw-interface && pytest
tests/unit/test_user_billing.py::TestEnsureBillingInitialized
tests/unit/test_billing_v2_fulfillment.py::test_trial_entitlement_updates_legacy_projection_as_trial
tests/unit/test_user_trial_credits_service.py::TestGrantTrialCreditsIfEligible::test_v2_new_user_records_entitlement_without_account_billing_update
-q # 21 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
&& bash scripts/ci-lint/03-complexity.sh
- Direct API smoke against local FastAPI with staging Mongo/Billing
Gateway: normal /users/create -> /users/credits/check -> /users/get,
verified ecap-account has no legacy billing fields and Billing Profile
is ready.
- Direct API smoke for POST /account, verified billing_initialized=true
in response, ecap-account has no legacy billing fields, Billing Profile
is ready with billing_key/team_id/wallets.
- Direct API smoke for warm-pool /users/create, verified warm-pool
billing fields land in Billing Profile, ecap-account stays clean, assets
are claimed, then cleaned test Mongo docs.

## Latest follow-up
- Fixed reads-only rollout semantics: when
`BILLING_V2_READS_ENABLED=true` and `BILLING_V2_WRITES_ENABLED=false`,
registration, `/users/create`, `/users/get`, and credits endpoints still
run legacy `ensure_billing_initialized`; v2 profile reads stay dry-run.
- Confirmed warm-pool pre-initialization remains user-only and
explicitly skips personal team creation.
- Fixed full-v2 invite trial grant: if the account row is clean and
lacks legacy billing fields, trial grant overlays Billing Profile
readiness through `ensure_billing_initialized` before recording/granting
the entitlement.
- Fixed OpenClaw init robustness: if billing initialization is not ready
during no-bot startup, the API returns `waiting` instead of surfacing a
500.

## Latest verification
- cd services/claw-interface && ruff format --check
app/services/user/account_service.py app/routes/user.py
app/routes/credits.py tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_user_credits.py
- cd services/claw-interface && ruff check
app/services/user/account_service.py app/routes/user.py
app/routes/credits.py tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_user_credits.py
- cd services/claw-interface && pyright
app/services/user/account_service.py app/routes/user.py
app/routes/credits.py tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_user_credits.py
- cd services/claw-interface && pytest
tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_user_credits.py tests/unit/test_account_service.py
tests/unit/test_user_routes_coverage.py -q # 33 passed
- cd services/claw-interface && pytest
tests/unit/test_account_builder.py tests/unit/test_account_service.py
tests/unit/test_billing_profiles_v2.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_billing_key_bootstrap.py
tests/unit/test_billing_warm_pool.py tests/unit/test_user_billing.py
tests/unit/test_warm_pool_materialization.py
tests/unit/test_user_trial_credits_service.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_user_credits.py tests/unit/test_user_routes_coverage.py
-q # 150 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
&& bash scripts/ci-lint/03-complexity.sh
- cd services/claw-interface && ruff check
app/services/user/trial_credits.py app/routes/openclaw.py
tests/unit/test_user_trial_credits_service.py
- cd services/claw-interface && pyright
app/services/user/trial_credits.py app/routes/openclaw.py
tests/unit/test_user_trial_credits_service.py
- cd services/claw-interface && pytest
tests/unit/test_user_trial_credits_service.py
tests/bdd/step_defs/test_openclaw_lifecycle.py::test_redeploy_no_bot_delegates
-q # 7 passed, 1 skipped locally
- cd services/claw-interface && pytest
tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_user_credits.py tests/unit/test_account_service.py
tests/unit/test_user_routes_coverage.py
tests/unit/test_user_trial_credits_service.py
tests/bdd/step_defs/test_openclaw_lifecycle.py::test_redeploy_no_bot_delegates
-q # 40 passed, 1 skipped locally
## Latest follow-up 2
- Classified the latest CI review findings: `/users/get` legacy expiry
downgrade and `user_type` stripping were real full-v2 issues; warm-pool
profile without personal team is intentional user-only preinit behavior.
- Fixed full-v2 `/account/me` to overlay Billing Summary before building
the flat account response.
- Fixed existing-user `/account` registration to seed billing
initialization from the persisted account row instead of a newly
constructed empty account.
- Kept `user_type` on new v2 account rows so legacy public response
validation remains stable while Billing Summary remains the subscription
source of truth.
- Skipped legacy expiry downgrade on `/users/get` when both Billing v2
reads and writes are enabled.

## Latest verification 2
- cd services/claw-interface && ruff format --check
app/services/user/account_service.py app/routes/account.py
app/routes/user.py app/services/user/account_builder.py
app/schema/account_api.py tests/unit/test_account_service.py
tests/unit/test_routes_account.py
tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_account_builder.py
- cd services/claw-interface && ruff check
app/services/user/account_service.py app/routes/account.py
app/routes/user.py app/services/user/account_builder.py
app/schema/account_api.py tests/unit/test_account_service.py
tests/unit/test_routes_account.py
tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_account_builder.py
- cd services/claw-interface && pyright
app/services/user/account_service.py app/routes/account.py
app/routes/user.py app/services/user/account_builder.py
app/schema/account_api.py tests/unit/test_account_service.py
tests/unit/test_routes_account.py
tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_account_builder.py
- cd services/claw-interface && pytest
tests/unit/test_account_builder.py tests/unit/test_account_service.py
tests/unit/test_routes_account.py
tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_user_credits.py tests/unit/test_user_routes_coverage.py
-q # 69 passed
- cd services/claw-interface && pytest
tests/unit/test_account_builder.py tests/unit/test_account_service.py
tests/unit/test_billing_profiles_v2.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_billing_key_bootstrap.py
tests/unit/test_billing_warm_pool.py tests/unit/test_user_billing.py
tests/unit/test_warm_pool_materialization.py
tests/unit/test_user_trial_credits_service.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_billing_v2_user_public_response.py
tests/unit/test_user_credits.py tests/unit/test_user_routes_coverage.py
tests/unit/test_routes_account.py -q # 185 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
&& bash scripts/ci-lint/03-complexity.sh
## Latest follow-up 3
- Latest CI review was NEED_HUMAN_REVIEW only. No new production logic
bug was confirmed.
- Added regression coverage for the reviewed boundaries: profile
bootstrap free-plan seeding, first paid subscription entitlement after
unready profile initialization, and OpenClaw billing-init-not-ready
returning `waiting` without creating a bot.

## Latest verification 3
- cd services/claw-interface && ruff format --check
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && ruff check
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pyright
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pytest
tests/unit/test_billing_profiles_initialization.py::test_new_user_bootstraps_wallets_marks_ready_and_audits
tests/unit/test_billing_v2_fulfillment.py::test_unready_profile_first_paid_subscription_initializes_then_subscribes_and_topups
tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_failure_returns_waiting_without_creating_bot
-q # 3 passed
- cd services/claw-interface && pytest
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_openclaw_endpoints_extra.py -q # 51 passed

## Latest follow-up 4
- Latest CI review found one real credits boundary: full-v2
`/users/credits`, `/users/credits/check`, and `/users/credits/usage`
could return 500 during retryable Billing Profile init lease contention.
Fixed these to return the existing `billing_not_ready` 503 response.
- Refined OpenClaw init so only retryable billing-init lease contention
returns `waiting`; hard billing failures now surface as 500 and do not
create a bot.

## Latest verification 4
- cd services/claw-interface && ruff format --check
app/services/billing.py app/routes/credits.py app/routes/openclaw.py
tests/unit/test_user_credits.py
tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && ruff check app/services/billing.py
app/routes/credits.py app/routes/openclaw.py
tests/unit/test_user_credits.py
tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pyright app/services/billing.py
app/routes/credits.py app/routes/openclaw.py
tests/unit/test_user_credits.py
tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pytest
tests/unit/test_user_credits.py::TestBillingV2InitializationContention
tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_failure_returns_waiting_without_creating_bot
tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_hard_failure_raises_without_creating_bot
-q # 5 passed
- cd services/claw-interface && pytest tests/unit/test_user_credits.py
tests/unit/test_openclaw_endpoints_extra.py -q # 46 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
&& bash scripts/ci-lint/03-complexity.sh


## Latest follow-up 5
- Fixed the CI-only BDD failure in `test_redeploy_no_bot_delegates`:
that scenario is about no-bot redeploy delegating to init and waiting
when the user has no usable billing/LiteLLM key, not about real Billing
Gateway initialization. The test now explicitly isolates billing init
for that scenario.

## Latest verification 5
- cd services/claw-interface && ruff format --check
tests/bdd/step_defs/test_openclaw_lifecycle.py app/services/billing.py
app/routes/credits.py app/routes/openclaw.py
tests/unit/test_user_credits.py
tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && ruff check
tests/bdd/step_defs/test_openclaw_lifecycle.py app/services/billing.py
app/routes/credits.py app/routes/openclaw.py
tests/unit/test_user_credits.py
tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pyright
tests/bdd/step_defs/test_openclaw_lifecycle.py app/services/billing.py
app/routes/credits.py app/routes/openclaw.py
tests/unit/test_user_credits.py
tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pytest
tests/unit/test_user_credits.py::TestBillingV2InitializationContention
tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_failure_returns_waiting_without_creating_bot
tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_hard_failure_raises_without_creating_bot
tests/bdd/step_defs/test_openclaw_lifecycle.py::test_redeploy_no_bot_delegates
-q # 5 passed, 1 skipped locally because MongoDB BDD fixture is
unavailable
- cd services/claw-interface && pytest tests/unit/test_user_credits.py
tests/unit/test_openclaw_endpoints_extra.py -q # 46 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
&& bash scripts/ci-lint/03-complexity.sh


## Latest follow-up 6
- Latest Codex review identified a real remaining lease-contention
boundary in `/users/create` and `/users/get` under full Billing v2.
Fixed these routes to translate retryable Billing Profile init
contention into 503 `billing_not_ready` instead of a generic 500.
- Added regression coverage for new-user create, existing-user create,
and get-user contention paths.

## Latest verification 6
- cd services/claw-interface && ruff format --check app/routes/user.py
tests/unit/test_user_routes_coverage.py
- cd services/claw-interface && ruff check app/routes/user.py
tests/unit/test_user_routes_coverage.py
- cd services/claw-interface && pyright app/routes/user.py
tests/unit/test_user_routes_coverage.py
- cd services/claw-interface && pytest
tests/unit/test_user_routes_coverage.py::TestCreateUserCoverage::test_new_user_billing_init_contention_returns_billing_not_ready
tests/unit/test_user_routes_coverage.py::TestCreateUserCoverage::test_existing_user_billing_init_contention_returns_billing_not_ready
tests/unit/test_user_routes_coverage.py::TestGetUserCoverage::test_get_user_billing_init_contention_returns_billing_not_ready
-q # 3 passed
- cd services/claw-interface && pytest
tests/unit/test_user_routes_coverage.py
tests/unit/test_billing_v2_user_public_response.py -q # 19 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
&& bash scripts/ci-lint/03-complexity.sh
## Latest follow-up 7
- Latest Codex review found two real full-v2 cleanup risks:
`/users/credits` could keep returning stale legacy subscription fields
from `ecap-account`, and warm-pool legacy placeholder finalization could
leave stale billing fields on `ecap-account`.
- Fixed `/users/credits` so full-v2 derives `subscription_code` /
`subscription_end_time` from Billing Summary instead of the account row.
Reads-only rollout keeps legacy fields unchanged.
- Fixed warm-pool materialization/finalization so full-v2 atomically
`$set`s materialized assets and `$unset`s the legacy billing account
fields, and strips those fields from the in-memory user before follow-up
work.

## Latest verification 7
- cd services/claw-interface && ruff format app/routes/credits.py
app/services/user/account_builder.py app/services/user/warm_pool.py
tests/unit/test_user_credits.py tests/unit/test_warm_pool.py
- cd services/claw-interface && ruff check app/routes/credits.py
app/services/user/account_builder.py app/services/user/warm_pool.py
tests/unit/test_user_credits.py tests/unit/test_warm_pool.py
- cd services/claw-interface && pyright app/routes/credits.py
app/services/user/account_builder.py app/services/user/warm_pool.py
tests/unit/test_user_credits.py tests/unit/test_warm_pool.py
- cd services/claw-interface && pytest tests/unit/test_user_credits.py
tests/unit/test_warm_pool.py -q # 28 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
&& bash scripts/ci-lint/03-complexity.sh

## Latest follow-up 8
- Latest Codex review was a real full-v2 reader/projection issue:
subscription fulfillment stopped legacy account projection while
OpenClaw and subscription-management routes could still read stale
account subscription fields.
- Fixed OpenClaw expired gating to derive full-v2 state from Billing
Summary across init/status/restart/redeploy/recreate, while legacy and
reads-only rollout keep the account-field behavior.
- Fixed subscription management so full-v2
downgrade/cancel-downgrade/renew/cancel do not fall back to stale
account fields when no v2 provider agreement exists; cancel now
dispatches through the v2 Stripe/Antom provider handlers.
- Kept compatibility account projection enabled for reads-only rollout
(`reads=true`, `writes=false`) and disabled only after full v2 cutover.
- Fixed the CI warm-pool materialization test to mock/assert the new
atomic `$set` + `$unset` account update path.
- Added `size-override`: the PR is 2041 lines after required review
fixes, 41 lines over the 2000-line guard; splitting this follow-up would
leave the current PR with a known unsafe full-v2 reader gap.

## Latest verification 8
- cd services/claw-interface && ruff check app/routes/openclaw.py
app/routes/subscription.py app/services/billing_v2/fulfillment.py
tests/unit/test_warm_pool_materialization.py
- cd services/claw-interface && pyright app/routes/openclaw.py
app/routes/subscription.py app/services/billing_v2/fulfillment.py
tests/unit/test_warm_pool_materialization.py
- cd services/claw-interface && pytest
tests/unit/test_warm_pool_materialization.py::test_materialize_warm_pool_assets_v2_syncs_profile_and_skips_account_billing_fields
tests/unit/test_openclaw_endpoints_extra.py
tests/unit/test_subscription_routes.py
tests/unit/test_billing_v2_fulfillment.py -q # 74 passed
- cd services/claw-interface && pytest tests/unit/test_warm_pool.py
tests/unit/test_warm_pool_materialization.py -q # 32 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
&& bash scripts/ci-lint/03-complexity.sh
- ./scripts/check-pr-size.sh --base origin/main --head HEAD --threshold
2000 # 2041 lines; size-override applied

## Latest follow-up 9
- Latest CI review raised two NEED_HUMAN_REVIEW items. Both were valid
enough to fix before merge.
- Existing open-registration retry path now reruns the idempotent trial
grant after billing init succeeds, so first-request init contention
cannot strand an exempt user without trial credits.
- Subscription management v2 mutation paths now require full Billing v2
(`reads && writes`); writes-only mode keeps legacy mutations and
projections consistent.
- Added route-level regression coverage for existing-user retry trial
grant, writes-only downgrade legacy behavior, and full-v2 cancel
provider dispatch.
- `size-override` remains intentional: the PR is now 2160 lines after
required review fixes, and splitting this final hardening would leave
the current rollout path with known mixed-flag/retry gaps.

## Latest verification 9
- cd services/claw-interface && ruff check app/routes/user.py
app/routes/subscription.py tests/unit/test_user_routes_coverage.py
tests/unit/test_subscription_routes.py
- cd services/claw-interface && pyright app/routes/user.py
app/routes/subscription.py tests/unit/test_user_routes_coverage.py
tests/unit/test_subscription_routes.py
- cd services/claw-interface && pytest
tests/unit/test_user_routes_coverage.py
tests/unit/test_subscription_routes.py -q # 40 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
- cd services/claw-interface && bash scripts/ci-lint/03-complexity.sh
- ./scripts/check-pr-size.sh --base origin/main --head HEAD --threshold
2000 # 2160 lines; size-override applied

## Latest follow-up 10
- Fixed the skipped-migration terminal-user edge case: OpenClaw now
keeps legacy `expired` / `canceled` / `stopped` / `revoked` accounts
blocked when Billing v2 has no current access facts, so old expired
users are guided back to subscription instead of silently reinitializing
resources.
- Preserved the intended v2 override: if a user has a real
active/trial/canceling Billing v2 access record, that v2 state wins even
if `ecap-account.subscription_status` is stale.
- Moved the gate into `app.services.openclaw.subscription_gate` to keep
`routes/openclaw.py` under the 500-line guard.
- `size-override` remains intentional: the PR is now 2259 lines after
required rollout-edge hardening.

## Latest verification 10
- cd services/claw-interface && ruff format --check
app/routes/openclaw.py app/services/openclaw/subscription_gate.py
tests/unit/test_openclaw_subscription_gate.py
- cd services/claw-interface && ruff check app/routes/openclaw.py
app/services/openclaw/subscription_gate.py
tests/unit/test_openclaw_subscription_gate.py
- cd services/claw-interface && pyright app/routes/openclaw.py
app/services/openclaw/subscription_gate.py
tests/unit/test_openclaw_subscription_gate.py
- cd services/claw-interface && pytest
tests/unit/test_openclaw_subscription_gate.py -q # 3 passed
- cd services/claw-interface && pytest
tests/unit/test_openclaw_endpoints_extra.py
tests/unit/test_openclaw_subscription_gate.py -q # 36 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
- cd services/claw-interface && bash scripts/ci-lint/03-complexity.sh
- ./scripts/check-pr-size.sh --base origin/main --head HEAD --threshold
2000 # 2259 lines; size-override applied
### Latest follow-up 11
- Addressed the warm-pool Billing v2 review by keeping
`BillingProfile.status=ready` focused on billing infrastructure
(`billing_key` + standard wallets), while ensuring real-user
initialization does not return a profile missing personal `team_id`.
- Warm-pool pre-provisioning still skips personal-team creation.
`team_key` is not required for personal users and remains allowed to be
null; only `team_id` is materialized later for personal org reuse /
compatibility.
- Added regression coverage for a warm-pool-style ready profile that has
wallets but no team metadata: the initializer claims the lease, reuses
existing wallets, does not resubscribe or recreate wallets, and syncs
`team_id` while leaving `team_key=None`.

### Latest verification 11
- `ruff format --check app/services/billing_profiles/initialization.py
tests/unit/test_billing_profiles_initialization.py`
- `ruff check app/services/billing_profiles/initialization.py
tests/unit/test_billing_profiles_initialization.py`
- `pyright app/services/billing_profiles/initialization.py
tests/unit/test_billing_profiles_initialization.py`
- `pytest tests/unit/test_billing_profiles_initialization.py -q`
- `pytest tests/unit/test_warm_pool_materialization.py -q`
- `pytest tests/unit/test_billing_warm_pool.py
tests/unit/test_account_service.py -q`

### Latest follow-up 12
- Corrected the warm-pool/team boundary: Billing Profile `ready` remains
billing-infrastructure readiness only (`billing_key` +
subscription/topup wallets). It does not require `team_id` or
`team_key`.
- Warm-pool pre-provisioning and claim/finalize do not create a personal
team just to make Billing Profile ready.
- Personal-org creation is now the team boundary in full-v2 mode: it
reads an existing personal `team_id` from Billing Profile when
`ecap-account` is clean, and writes the created/reused `team_id` back to
Billing Profile. `team_key` stays optional/null for personal users.

### Latest verification 12
- `ruff format --check app/services/billing_profiles/initialization.py
app/services/billing_profiles/service.py
app/services/billing_profiles/__init__.py
app/services/org/org_service.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_org_service.py`
- `ruff check app/services/billing_profiles/initialization.py
app/services/billing_profiles/service.py
app/services/billing_profiles/__init__.py
app/services/org/org_service.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_org_service.py`
- `pyright app/services/billing_profiles/initialization.py
app/services/billing_profiles/service.py
app/services/billing_profiles/__init__.py
app/services/org/org_service.py
tests/unit/test_billing_profiles_initialization.py
tests/unit/test_org_service.py`
- `pytest tests/unit/test_billing_profiles_initialization.py
tests/unit/test_warm_pool_materialization.py
tests/unit/test_billing_warm_pool.py tests/unit/test_org_service.py -q`

### Latest follow-up 13
- Tightened the org-team boundary: full-v2 team org creation never
reads/reuses the personal `team_id` from Billing Profile. Only
personal-org creation uses personal profile team metadata.

### Latest verification 13
- `ruff format app/services/org/org_service.py
tests/unit/test_org_service.py`
- `ruff check app/services/org/org_service.py
tests/unit/test_org_service.py`
- `pyright app/services/org/org_service.py
tests/unit/test_org_service.py`
- `pytest tests/unit/test_org_service.py -q`

### Latest follow-up 14
- Fixed open-registration trial idempotency: users with
`has_used_trial`, `trial_end_time`, or `subscription_status=trial` now
skip trial grant before wallet lookup; successful legacy and full-v2
grants persist `has_used_trial=true`.
- Fixed full-v2 downgrade/cancel-downgrade provider dispatch so Apple or
future providers return unsupported instead of falling through to
Stripe-specific handlers.

### Latest verification 14
- `ruff check app/services/user/trial_credits.py
app/routes/subscription.py tests/unit/test_user_trial_credits_service.py
tests/unit/test_subscription_routes.py`
- `pyright app/services/user/trial_credits.py app/routes/subscription.py
tests/unit/test_user_trial_credits_service.py
tests/unit/test_subscription_routes.py`
- `pytest tests/unit/test_user_trial_credits_service.py
tests/unit/test_subscription_routes.py -q`
- `bash scripts/ci-lint/01-file-length.sh`

### Latest follow-up 15
- Latest Codex review item about subscription mutation routes is the
intended cutover invariant: once both Billing v2 flags are enabled,
active provider users must have backfilled `subscription_agreement`
facts. The production checklist already blocks flag enablement until
final backfill has no unresolved blockers; falling back to legacy fields
in full-v2 mode would reintroduce split-brain mutations.
- Hardened the personal-org/profile edge raised by Codex: if team
metadata is synced before a Billing Profile exists,
`sync_profile_team_metadata()` now creates a minimal `uninitialized`
profile carrying the team id, so later billing initialization can fill
billing key and wallets without losing the org-created team.

### Latest verification 15
- `ruff check app/services/billing_profiles/service.py
tests/unit/test_billing_profiles_v2.py`
- `pyright app/services/billing_profiles/service.py
tests/unit/test_billing_profiles_v2.py tests/unit/test_org_service.py`
- `pytest tests/unit/test_billing_profiles_v2.py
tests/unit/test_org_service.py -q`
- `bash scripts/ci-lint/01-file-length.sh`

### Latest follow-up 16
- Fixed the Apple Billing v2 review blocker:
`activate_apple_subscription()` now delegates to Apple Billing v2 claim
when v2 writes are enabled, so it does not use legacy account billing
fields or legacy credit refresh in v2 mode.
- Fixed Apple v2 expiry cleanup to initialize/overlay Billing Profile
facts before running subscription expiry side effects, so BG
termination, wallet clear, and LiteLLM downgrade do not depend on
billing fields persisted on `ecap-account`.
- Left the legacy Apple notification cleanup branch behind
`BILLING_V2_WRITES_ENABLED=false`; full-v2 notifications return through
the Billing v2 handler and profile-backed cleanup path.

### Latest verification 16
- `ruff check app/services/apple_subscription_manager.py
app/routes/apple.py tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_routes.py`
- `pyright app/services/apple_subscription_manager.py
app/routes/apple.py tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_routes.py`
- `pytest tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_routes.py -q`
- `bash scripts/ci-lint/01-file-length.sh`

### Latest follow-up 17
- Latest Codex review found a real Apple Billing v2 cross-provider
exclusivity gap: the v2 Apple claim path could skip the legacy guard and
allow a user with an active Stripe/Antom subscription to claim Apple.
- Added a shared Apple provider exclusivity guard that checks both
current Billing v2 agreement facts and legacy account provider state
during cutover.
- Applied the guard to manual Apple transaction claims and activate
server notifications before any payment order, subscription agreement,
or entitlement grant is recorded.

### Latest verification 17
- `ruff check app/services/apple/billing_v2.py
app/services/apple/non_apple_subscription_guard.py
tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py`
- `pyright app/services/apple/billing_v2.py
app/services/apple/non_apple_subscription_guard.py
app/services/apple_subscription_manager.py app/routes/apple.py
tests/unit/test_apple_billing_v2.py
tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_routes.py`
- `pytest tests/unit/test_apple_billing_v2.py
tests/unit/test_apple_subscription_manager.py
tests/unit/test_apple_routes.py -q` # 52 passed
- `bash scripts/ci-lint/01-file-length.sh`
```

### PR Body

## Summary
- Route Billing v2 ensure/init through Billing Profile storage instead of persisting legacy billing fields on ecap-account.
- Materialize warm-pool billing assets into Billing Profiles under the v2 cutover flags while keeping ecap-account clean.
- Keep warm-pool pre-initialization user-only: it bootstraps billing key/wallets but does not create a personal team until real personal-org creation.
- Add trial/topup fulfillment, account creation, docs, and tests for the v2 init cutover path.

## Linear
https://linear.app/srpone/issue/ECA-842/billing-v2-subscription-payment-refactor

## Review follow-up
- Fixed fulfillment so reads/writes-disabled paths do not backfill or initialize Billing Profiles.
- Fixed /account register response overlay so Billing v2 profile facts are request-scope only and ecap-account remains clean.
- Fixed bootstrap team selection so personal-team responses are authoritative for normal registration, while warm-pool preinit explicitly skips personal team creation.
- Fixed trial entitlement fulfillment so open-registration trial credits top up the subscription wallet without subscribing the user to the paid starter BG plan.
- Made legacy billing initialization unit tests independent of CI/staging v2 flag values.

## Verification
- cd services/claw-interface && ruff format --check app/services/billing_key_bootstrap.py app/services/warm_pool_billing.py app/services/user/warm_pool.py app/services/billing_v2/fulfillment.py app/services/user/account_service.py tests/unit/test_billing_key_bootstrap.py tests/unit/test_billing_warm_pool.py tests/unit/test_warm_pool_materialization.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_account_service.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_user_billing.py
- cd services/claw-interface && ruff check app/services/billing_key_bootstrap.py app/services/warm_pool_billing.py app/services/user/warm_pool.py app/services/billing_v2/fulfillment.py app/services/user/account_service.py tests/unit/test_billing_key_bootstrap.py tests/unit/test_billing_warm_pool.py tests/unit/test_warm_pool_materialization.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_account_service.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_user_billing.py
- cd services/claw-interface && pyright app/services/billing_key_bootstrap.py app/services/warm_pool_billing.py app/services/user/warm_pool.py app/services/billing_v2/fulfillment.py app/services/user/account_service.py tests/unit/test_billing_key_bootstrap.py tests/unit/test_billing_warm_pool.py tests/unit/test_warm_pool_materialization.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_account_service.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_user_billing.py
- cd services/claw-interface && pytest tests/unit/test_account_builder.py tests/unit/test_account_service.py tests/unit/test_billing_profiles_v2.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_billing_key_bootstrap.py tests/unit/test_billing_warm_pool.py tests/unit/test_user_billing.py tests/unit/test_warm_pool_materialization.py tests/unit/test_user_trial_credits_service.py tests/unit/test_billing_v2_fulfillment.py -q  # 125 passed
- cd services/claw-interface && pytest tests/unit/test_user_billing.py::TestEnsureBillingInitialized tests/unit/test_billing_v2_fulfillment.py::test_trial_entitlement_updates_legacy_projection_as_trial tests/unit/test_user_trial_credits_service.py::TestGrantTrialCreditsIfEligible::test_v2_new_user_records_entitlement_without_account_billing_update -q  # 21 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh && bash scripts/ci-lint/03-complexity.sh
- Direct API smoke against local FastAPI with staging Mongo/Billing Gateway: normal /users/create -> /users/credits/check -> /users/get, verified ecap-account has no legacy billing fields and Billing Profile is ready.
- Direct API smoke for POST /account, verified billing_initialized=true in response, ecap-account has no legacy billing fields, Billing Profile is ready with billing_key/team_id/wallets.
- Direct API smoke for warm-pool /users/create, verified warm-pool billing fields land in Billing Profile, ecap-account stays clean, assets are claimed, then cleaned test Mongo docs.

## Latest follow-up
- Fixed reads-only rollout semantics: when `BILLING_V2_READS_ENABLED=true` and `BILLING_V2_WRITES_ENABLED=false`, registration, `/users/create`, `/users/get`, and credits endpoints still run legacy `ensure_billing_initialized`; v2 profile reads stay dry-run.
- Confirmed warm-pool pre-initialization remains user-only and explicitly skips personal team creation.
- Fixed full-v2 invite trial grant: if the account row is clean and lacks legacy billing fields, trial grant overlays Billing Profile readiness through `ensure_billing_initialized` before recording/granting the entitlement.
- Fixed OpenClaw init robustness: if billing initialization is not ready during no-bot startup, the API returns `waiting` instead of surfacing a 500.

## Latest verification
- cd services/claw-interface && ruff format --check app/services/user/account_service.py app/routes/user.py app/routes/credits.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_user_credits.py
- cd services/claw-interface && ruff check app/services/user/account_service.py app/routes/user.py app/routes/credits.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_user_credits.py
- cd services/claw-interface && pyright app/services/user/account_service.py app/routes/user.py app/routes/credits.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_user_credits.py
- cd services/claw-interface && pytest tests/unit/test_billing_v2_user_public_response.py tests/unit/test_user_credits.py tests/unit/test_account_service.py tests/unit/test_user_routes_coverage.py -q  # 33 passed
- cd services/claw-interface && pytest tests/unit/test_account_builder.py tests/unit/test_account_service.py tests/unit/test_billing_profiles_v2.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_billing_key_bootstrap.py tests/unit/test_billing_warm_pool.py tests/unit/test_user_billing.py tests/unit/test_warm_pool_materialization.py tests/unit/test_user_trial_credits_service.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_user_credits.py tests/unit/test_user_routes_coverage.py -q  # 150 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh && bash scripts/ci-lint/03-complexity.sh
- cd services/claw-interface && ruff check app/services/user/trial_credits.py app/routes/openclaw.py tests/unit/test_user_trial_credits_service.py
- cd services/claw-interface && pyright app/services/user/trial_credits.py app/routes/openclaw.py tests/unit/test_user_trial_credits_service.py
- cd services/claw-interface && pytest tests/unit/test_user_trial_credits_service.py tests/bdd/step_defs/test_openclaw_lifecycle.py::test_redeploy_no_bot_delegates -q  # 7 passed, 1 skipped locally
- cd services/claw-interface && pytest tests/unit/test_billing_v2_user_public_response.py tests/unit/test_user_credits.py tests/unit/test_account_service.py tests/unit/test_user_routes_coverage.py tests/unit/test_user_trial_credits_service.py tests/bdd/step_defs/test_openclaw_lifecycle.py::test_redeploy_no_bot_delegates -q  # 40 passed, 1 skipped locally
## Latest follow-up 2
- Classified the latest CI review findings: `/users/get` legacy expiry downgrade and `user_type` stripping were real full-v2 issues; warm-pool profile without personal team is intentional user-only preinit behavior.
- Fixed full-v2 `/account/me` to overlay Billing Summary before building the flat account response.
- Fixed existing-user `/account` registration to seed billing initialization from the persisted account row instead of a newly constructed empty account.
- Kept `user_type` on new v2 account rows so legacy public response validation remains stable while Billing Summary remains the subscription source of truth.
- Skipped legacy expiry downgrade on `/users/get` when both Billing v2 reads and writes are enabled.

## Latest verification 2
- cd services/claw-interface && ruff format --check app/services/user/account_service.py app/routes/account.py app/routes/user.py app/services/user/account_builder.py app/schema/account_api.py tests/unit/test_account_service.py tests/unit/test_routes_account.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_account_builder.py
- cd services/claw-interface && ruff check app/services/user/account_service.py app/routes/account.py app/routes/user.py app/services/user/account_builder.py app/schema/account_api.py tests/unit/test_account_service.py tests/unit/test_routes_account.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_account_builder.py
- cd services/claw-interface && pyright app/services/user/account_service.py app/routes/account.py app/routes/user.py app/services/user/account_builder.py app/schema/account_api.py tests/unit/test_account_service.py tests/unit/test_routes_account.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_account_builder.py
- cd services/claw-interface && pytest tests/unit/test_account_builder.py tests/unit/test_account_service.py tests/unit/test_routes_account.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_user_credits.py tests/unit/test_user_routes_coverage.py -q  # 69 passed
- cd services/claw-interface && pytest tests/unit/test_account_builder.py tests/unit/test_account_service.py tests/unit/test_billing_profiles_v2.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_billing_key_bootstrap.py tests/unit/test_billing_warm_pool.py tests/unit/test_user_billing.py tests/unit/test_warm_pool_materialization.py tests/unit/test_user_trial_credits_service.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_billing_v2_user_public_response.py tests/unit/test_user_credits.py tests/unit/test_user_routes_coverage.py tests/unit/test_routes_account.py -q  # 185 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh && bash scripts/ci-lint/03-complexity.sh
## Latest follow-up 3
- Latest CI review was NEED_HUMAN_REVIEW only. No new production logic bug was confirmed.
- Added regression coverage for the reviewed boundaries: profile bootstrap free-plan seeding, first paid subscription entitlement after unready profile initialization, and OpenClaw billing-init-not-ready returning `waiting` without creating a bot.

## Latest verification 3
- cd services/claw-interface && ruff format --check tests/unit/test_billing_profiles_initialization.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && ruff check tests/unit/test_billing_profiles_initialization.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pyright tests/unit/test_billing_profiles_initialization.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pytest tests/unit/test_billing_profiles_initialization.py::test_new_user_bootstraps_wallets_marks_ready_and_audits tests/unit/test_billing_v2_fulfillment.py::test_unready_profile_first_paid_subscription_initializes_then_subscribes_and_topups tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_failure_returns_waiting_without_creating_bot -q  # 3 passed
- cd services/claw-interface && pytest tests/unit/test_billing_profiles_initialization.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_openclaw_endpoints_extra.py -q  # 51 passed

## Latest follow-up 4
- Latest CI review found one real credits boundary: full-v2 `/users/credits`, `/users/credits/check`, and `/users/credits/usage` could return 500 during retryable Billing Profile init lease contention. Fixed these to return the existing `billing_not_ready` 503 response.
- Refined OpenClaw init so only retryable billing-init lease contention returns `waiting`; hard billing failures now surface as 500 and do not create a bot.

## Latest verification 4
- cd services/claw-interface && ruff format --check app/services/billing.py app/routes/credits.py app/routes/openclaw.py tests/unit/test_user_credits.py tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && ruff check app/services/billing.py app/routes/credits.py app/routes/openclaw.py tests/unit/test_user_credits.py tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pyright app/services/billing.py app/routes/credits.py app/routes/openclaw.py tests/unit/test_user_credits.py tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pytest tests/unit/test_user_credits.py::TestBillingV2InitializationContention tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_failure_returns_waiting_without_creating_bot tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_hard_failure_raises_without_creating_bot -q  # 5 passed
- cd services/claw-interface && pytest tests/unit/test_user_credits.py tests/unit/test_openclaw_endpoints_extra.py -q  # 46 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh && bash scripts/ci-lint/03-complexity.sh


## Latest follow-up 5
- Fixed the CI-only BDD failure in `test_redeploy_no_bot_delegates`: that scenario is about no-bot redeploy delegating to init and waiting when the user has no usable billing/LiteLLM key, not about real Billing Gateway initialization. The test now explicitly isolates billing init for that scenario.

## Latest verification 5
- cd services/claw-interface && ruff format --check tests/bdd/step_defs/test_openclaw_lifecycle.py app/services/billing.py app/routes/credits.py app/routes/openclaw.py tests/unit/test_user_credits.py tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && ruff check tests/bdd/step_defs/test_openclaw_lifecycle.py app/services/billing.py app/routes/credits.py app/routes/openclaw.py tests/unit/test_user_credits.py tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pyright tests/bdd/step_defs/test_openclaw_lifecycle.py app/services/billing.py app/routes/credits.py app/routes/openclaw.py tests/unit/test_user_credits.py tests/unit/test_openclaw_endpoints_extra.py
- cd services/claw-interface && pytest tests/unit/test_user_credits.py::TestBillingV2InitializationContention tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_failure_returns_waiting_without_creating_bot tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_billing_init_hard_failure_raises_without_creating_bot tests/bdd/step_defs/test_openclaw_lifecycle.py::test_redeploy_no_bot_delegates -q  # 5 passed, 1 skipped locally because MongoDB BDD fixture is unavailable
- cd services/claw-interface && pytest tests/unit/test_user_credits.py tests/unit/test_openclaw_endpoints_extra.py -q  # 46 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh && bash scripts/ci-lint/03-complexity.sh


## Latest follow-up 6
- Latest Codex review identified a real remaining lease-contention boundary in `/users/create` and `/users/get` under full Billing v2. Fixed these routes to translate retryable Billing Profile init contention into 503 `billing_not_ready` instead of a generic 500.
- Added regression coverage for new-user create, existing-user create, and get-user contention paths.

## Latest verification 6
- cd services/claw-interface && ruff format --check app/routes/user.py tests/unit/test_user_routes_coverage.py
- cd services/claw-interface && ruff check app/routes/user.py tests/unit/test_user_routes_coverage.py
- cd services/claw-interface && pyright app/routes/user.py tests/unit/test_user_routes_coverage.py
- cd services/claw-interface && pytest tests/unit/test_user_routes_coverage.py::TestCreateUserCoverage::test_new_user_billing_init_contention_returns_billing_not_ready tests/unit/test_user_routes_coverage.py::TestCreateUserCoverage::test_existing_user_billing_init_contention_returns_billing_not_ready tests/unit/test_user_routes_coverage.py::TestGetUserCoverage::test_get_user_billing_init_contention_returns_billing_not_ready -q  # 3 passed
- cd services/claw-interface && pytest tests/unit/test_user_routes_coverage.py tests/unit/test_billing_v2_user_public_response.py -q  # 19 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh && bash scripts/ci-lint/03-complexity.sh
## Latest follow-up 7
- Latest Codex review found two real full-v2 cleanup risks: `/users/credits` could keep returning stale legacy subscription fields from `ecap-account`, and warm-pool legacy placeholder finalization could leave stale billing fields on `ecap-account`.
- Fixed `/users/credits` so full-v2 derives `subscription_code` / `subscription_end_time` from Billing Summary instead of the account row. Reads-only rollout keeps legacy fields unchanged.
- Fixed warm-pool materialization/finalization so full-v2 atomically `$set`s materialized assets and `$unset`s the legacy billing account fields, and strips those fields from the in-memory user before follow-up work.

## Latest verification 7
- cd services/claw-interface && ruff format app/routes/credits.py app/services/user/account_builder.py app/services/user/warm_pool.py tests/unit/test_user_credits.py tests/unit/test_warm_pool.py
- cd services/claw-interface && ruff check app/routes/credits.py app/services/user/account_builder.py app/services/user/warm_pool.py tests/unit/test_user_credits.py tests/unit/test_warm_pool.py
- cd services/claw-interface && pyright app/routes/credits.py app/services/user/account_builder.py app/services/user/warm_pool.py tests/unit/test_user_credits.py tests/unit/test_warm_pool.py
- cd services/claw-interface && pytest tests/unit/test_user_credits.py tests/unit/test_warm_pool.py -q  # 28 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh && bash scripts/ci-lint/03-complexity.sh

## Latest follow-up 8
- Latest Codex review was a real full-v2 reader/projection issue: subscription fulfillment stopped legacy account projection while OpenClaw and subscription-management routes could still read stale account subscription fields.
- Fixed OpenClaw expired gating to derive full-v2 state from Billing Summary across init/status/restart/redeploy/recreate, while legacy and reads-only rollout keep the account-field behavior.
- Fixed subscription management so full-v2 downgrade/cancel-downgrade/renew/cancel do not fall back to stale account fields when no v2 provider agreement exists; cancel now dispatches through the v2 Stripe/Antom provider handlers.
- Kept compatibility account projection enabled for reads-only rollout (`reads=true`, `writes=false`) and disabled only after full v2 cutover.
- Fixed the CI warm-pool materialization test to mock/assert the new atomic `$set` + `$unset` account update path.
- Added `size-override`: the PR is 2041 lines after required review fixes, 41 lines over the 2000-line guard; splitting this follow-up would leave the current PR with a known unsafe full-v2 reader gap.

## Latest verification 8
- cd services/claw-interface && ruff check app/routes/openclaw.py app/routes/subscription.py app/services/billing_v2/fulfillment.py tests/unit/test_warm_pool_materialization.py
- cd services/claw-interface && pyright app/routes/openclaw.py app/routes/subscription.py app/services/billing_v2/fulfillment.py tests/unit/test_warm_pool_materialization.py
- cd services/claw-interface && pytest tests/unit/test_warm_pool_materialization.py::test_materialize_warm_pool_assets_v2_syncs_profile_and_skips_account_billing_fields tests/unit/test_openclaw_endpoints_extra.py tests/unit/test_subscription_routes.py tests/unit/test_billing_v2_fulfillment.py -q  # 74 passed
- cd services/claw-interface && pytest tests/unit/test_warm_pool.py tests/unit/test_warm_pool_materialization.py -q  # 32 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh && bash scripts/ci-lint/03-complexity.sh
- ./scripts/check-pr-size.sh --base origin/main --head HEAD --threshold 2000  # 2041 lines; size-override applied

## Latest follow-up 9
- Latest CI review raised two NEED_HUMAN_REVIEW items. Both were valid enough to fix before merge.
- Existing open-registration retry path now reruns the idempotent trial grant after billing init succeeds, so first-request init contention cannot strand an exempt user without trial credits.
- Subscription management v2 mutation paths now require full Billing v2 (`reads && writes`); writes-only mode keeps legacy mutations and projections consistent.
- Added route-level regression coverage for existing-user retry trial grant, writes-only downgrade legacy behavior, and full-v2 cancel provider dispatch.
- `size-override` remains intentional: the PR is now 2160 lines after required review fixes, and splitting this final hardening would leave the current rollout path with known mixed-flag/retry gaps.

## Latest verification 9
- cd services/claw-interface && ruff check app/routes/user.py app/routes/subscription.py tests/unit/test_user_routes_coverage.py tests/unit/test_subscription_routes.py
- cd services/claw-interface && pyright app/routes/user.py app/routes/subscription.py tests/unit/test_user_routes_coverage.py tests/unit/test_subscription_routes.py
- cd services/claw-interface && pytest tests/unit/test_user_routes_coverage.py tests/unit/test_subscription_routes.py -q  # 40 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
- cd services/claw-interface && bash scripts/ci-lint/03-complexity.sh
- ./scripts/check-pr-size.sh --base origin/main --head HEAD --threshold 2000  # 2160 lines; size-override applied

## Latest follow-up 10
- Fixed the skipped-migration terminal-user edge case: OpenClaw now keeps legacy `expired` / `canceled` / `stopped` / `revoked` accounts blocked when Billing v2 has no current access facts, so old expired users are guided back to subscription instead of silently reinitializing resources.
- Preserved the intended v2 override: if a user has a real active/trial/canceling Billing v2 access record, that v2 state wins even if `ecap-account.subscription_status` is stale.
- Moved the gate into `app.services.openclaw.subscription_gate` to keep `routes/openclaw.py` under the 500-line guard.
- `size-override` remains intentional: the PR is now 2259 lines after required rollout-edge hardening.

## Latest verification 10
- cd services/claw-interface && ruff format --check app/routes/openclaw.py app/services/openclaw/subscription_gate.py tests/unit/test_openclaw_subscription_gate.py
- cd services/claw-interface && ruff check app/routes/openclaw.py app/services/openclaw/subscription_gate.py tests/unit/test_openclaw_subscription_gate.py
- cd services/claw-interface && pyright app/routes/openclaw.py app/services/openclaw/subscription_gate.py tests/unit/test_openclaw_subscription_gate.py
- cd services/claw-interface && pytest tests/unit/test_openclaw_subscription_gate.py -q  # 3 passed
- cd services/claw-interface && pytest tests/unit/test_openclaw_endpoints_extra.py tests/unit/test_openclaw_subscription_gate.py -q  # 36 passed
- cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
- cd services/claw-interface && bash scripts/ci-lint/03-complexity.sh
- ./scripts/check-pr-size.sh --base origin/main --head HEAD --threshold 2000  # 2259 lines; size-override applied
### Latest follow-up 11
- Addressed the warm-pool Billing v2 review by keeping `BillingProfile.status=ready` focused on billing infrastructure (`billing_key` + standard wallets), while ensuring real-user initialization does not return a profile missing personal `team_id`.
- Warm-pool pre-provisioning still skips personal-team creation. `team_key` is not required for personal users and remains allowed to be null; only `team_id` is materialized later for personal org reuse / compatibility.
- Added regression coverage for a warm-pool-style ready profile that has wallets but no team metadata: the initializer claims the lease, reuses existing wallets, does not resubscribe or recreate wallets, and syncs `team_id` while leaving `team_key=None`.

### Latest verification 11
- `ruff format --check app/services/billing_profiles/initialization.py tests/unit/test_billing_profiles_initialization.py`
- `ruff check app/services/billing_profiles/initialization.py tests/unit/test_billing_profiles_initialization.py`
- `pyright app/services/billing_profiles/initialization.py tests/unit/test_billing_profiles_initialization.py`
- `pytest tests/unit/test_billing_profiles_initialization.py -q`
- `pytest tests/unit/test_warm_pool_materialization.py -q`
- `pytest tests/unit/test_billing_warm_pool.py tests/unit/test_account_service.py -q`

### Latest follow-up 12
- Corrected the warm-pool/team boundary: Billing Profile `ready` remains billing-infrastructure readiness only (`billing_key` + subscription/topup wallets). It does not require `team_id` or `team_key`.
- Warm-pool pre-provisioning and claim/finalize do not create a personal team just to make Billing Profile ready.
- Personal-org creation is now the team boundary in full-v2 mode: it reads an existing personal `team_id` from Billing Profile when `ecap-account` is clean, and writes the created/reused `team_id` back to Billing Profile. `team_key` stays optional/null for personal users.

### Latest verification 12
- `ruff format --check app/services/billing_profiles/initialization.py app/services/billing_profiles/service.py app/services/billing_profiles/__init__.py app/services/org/org_service.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_org_service.py`
- `ruff check app/services/billing_profiles/initialization.py app/services/billing_profiles/service.py app/services/billing_profiles/__init__.py app/services/org/org_service.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_org_service.py`
- `pyright app/services/billing_profiles/initialization.py app/services/billing_profiles/service.py app/services/billing_profiles/__init__.py app/services/org/org_service.py tests/unit/test_billing_profiles_initialization.py tests/unit/test_org_service.py`
- `pytest tests/unit/test_billing_profiles_initialization.py tests/unit/test_warm_pool_materialization.py tests/unit/test_billing_warm_pool.py tests/unit/test_org_service.py -q`

### Latest follow-up 13
- Tightened the org-team boundary: full-v2 team org creation never reads/reuses the personal `team_id` from Billing Profile. Only personal-org creation uses personal profile team metadata.

### Latest verification 13
- `ruff format app/services/org/org_service.py tests/unit/test_org_service.py`
- `ruff check app/services/org/org_service.py tests/unit/test_org_service.py`
- `pyright app/services/org/org_service.py tests/unit/test_org_service.py`
- `pytest tests/unit/test_org_service.py -q`

### Latest follow-up 14
- Fixed open-registration trial idempotency: users with `has_used_trial`, `trial_end_time`, or `subscription_status=trial` now skip trial grant before wallet lookup; successful legacy and full-v2 grants persist `has_used_trial=true`.
- Fixed full-v2 downgrade/cancel-downgrade provider dispatch so Apple or future providers return unsupported instead of falling through to Stripe-specific handlers.

### Latest verification 14
- `ruff check app/services/user/trial_credits.py app/routes/subscription.py tests/unit/test_user_trial_credits_service.py tests/unit/test_subscription_routes.py`
- `pyright app/services/user/trial_credits.py app/routes/subscription.py tests/unit/test_user_trial_credits_service.py tests/unit/test_subscription_routes.py`
- `pytest tests/unit/test_user_trial_credits_service.py tests/unit/test_subscription_routes.py -q`
- `bash scripts/ci-lint/01-file-length.sh`

### Latest follow-up 15
- Latest Codex review item about subscription mutation routes is the intended cutover invariant: once both Billing v2 flags are enabled, active provider users must have backfilled `subscription_agreement` facts. The production checklist already blocks flag enablement until final backfill has no unresolved blockers; falling back to legacy fields in full-v2 mode would reintroduce split-brain mutations.
- Hardened the personal-org/profile edge raised by Codex: if team metadata is synced before a Billing Profile exists, `sync_profile_team_metadata()` now creates a minimal `uninitialized` profile carrying the team id, so later billing initialization can fill billing key and wallets without losing the org-created team.

### Latest verification 15
- `ruff check app/services/billing_profiles/service.py tests/unit/test_billing_profiles_v2.py`
- `pyright app/services/billing_profiles/service.py tests/unit/test_billing_profiles_v2.py tests/unit/test_org_service.py`
- `pytest tests/unit/test_billing_profiles_v2.py tests/unit/test_org_service.py -q`
- `bash scripts/ci-lint/01-file-length.sh`

### Latest follow-up 16
- Fixed the Apple Billing v2 review blocker: `activate_apple_subscription()` now delegates to Apple Billing v2 claim when v2 writes are enabled, so it does not use legacy account billing fields or legacy credit refresh in v2 mode.
- Fixed Apple v2 expiry cleanup to initialize/overlay Billing Profile facts before running subscription expiry side effects, so BG termination, wallet clear, and LiteLLM downgrade do not depend on billing fields persisted on `ecap-account`.
- Left the legacy Apple notification cleanup branch behind `BILLING_V2_WRITES_ENABLED=false`; full-v2 notifications return through the Billing v2 handler and profile-backed cleanup path.

### Latest verification 16
- `ruff check app/services/apple_subscription_manager.py app/routes/apple.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_routes.py`
- `pyright app/services/apple_subscription_manager.py app/routes/apple.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_routes.py`
- `pytest tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_routes.py -q`
- `bash scripts/ci-lint/01-file-length.sh`

### Latest follow-up 17
- Latest Codex review found a real Apple Billing v2 cross-provider exclusivity gap: the v2 Apple claim path could skip the legacy guard and allow a user with an active Stripe/Antom subscription to claim Apple.
- Added a shared Apple provider exclusivity guard that checks both current Billing v2 agreement facts and legacy account provider state during cutover.
- Applied the guard to manual Apple transaction claims and activate server notifications before any payment order, subscription agreement, or entitlement grant is recorded.

### Latest verification 17
- `ruff check app/services/apple/billing_v2.py app/services/apple/non_apple_subscription_guard.py tests/unit/test_apple_billing_v2.py tests/unit/test_apple_routes.py`
- `pyright app/services/apple/billing_v2.py app/services/apple/non_apple_subscription_guard.py app/services/apple_subscription_manager.py app/routes/apple.py tests/unit/test_apple_billing_v2.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_routes.py`
- `pytest tests/unit/test_apple_billing_v2.py tests/unit/test_apple_subscription_manager.py tests/unit/test_apple_routes.py -q`  # 52 passed
- `bash scripts/ci-lint/01-file-length.sh`


---

## [db4cc35] fix(web): activate OpenClaw on agent detail pages (#2140)

- **SHA**: db4cc351bd1cb40edfc01b68c3b9e865d6edd138
- **作者**: sam-srp
- **日期**: 2026-06-01T04:58:54Z
- **PR**: #2140

### 完整 Commit Message

```
fix(web): activate OpenClaw on agent detail pages (#2140)

## Summary
- Activate OpenClaw from the agent detail page instead of passively
reading connection state.
- Update the AgentDetailClient unit test mock to match the active hook.

## Root Cause
Direct visits to `/agents-manager/:id` used `useOpenClawPassive()`, so
the page could render the shared header and lock CTA actions against an
idle/disconnected frontend state without triggering init/connect. The
list page already used `useOpenClaw()`, which is why navigation paths
could show different connection states.

## Impact
Directly opening `/zh/agents-manager/agent_studio` now activates the
same OpenClaw connection flow as the agents list, while shared passive
surfaces like the header keep their existing behavior.

## Validation
- `pnpm test:unit
tests/unit/app/agents-manager/AgentDetailClient.unit.spec.tsx`
```

### PR Body

## Summary
- Activate OpenClaw from the agent detail page instead of passively reading connection state.
- Update the AgentDetailClient unit test mock to match the active hook.

## Root Cause
Direct visits to `/agents-manager/:id` used `useOpenClawPassive()`, so the page could render the shared header and lock CTA actions against an idle/disconnected frontend state without triggering init/connect. The list page already used `useOpenClaw()`, which is why navigation paths could show different connection states.

## Impact
Directly opening `/zh/agents-manager/agent_studio` now activates the same OpenClaw connection flow as the agents list, while shared passive surfaces like the header keep their existing behavior.

## Validation
- `pnpm test:unit tests/unit/app/agents-manager/AgentDetailClient.unit.spec.tsx`


---

## [a9a9ccc] fix(chat): clear typing on final Mattermost stream (#2139)

- **SHA**: a9a9ccca041a25544875599ba09e071696a621f3
- **作者**: sam-srp
- **日期**: 2026-06-01T03:24:09Z
- **PR**: #2139

### 完整 Commit Message

```
fix(chat): clear typing on final Mattermost stream (#2139)

## Summary
- clear the chat typing indicator when a Mattermost stream preview is
finalized in-place
- add unit coverage for final vs preview post_edited markers

## Root Cause
Mattermost finalizes some bot replies by editing the preview post with
props.openclaw_stream_state = final. The chat frontend only cleared
waiting on posted events, so Typing could linger after the visible
output finished.

## Validation
- pnpm test:unit tests/unit/hooks/useMattermost.unit.spec.ts
```

### PR Body

## Summary
- clear the chat typing indicator when a Mattermost stream preview is finalized in-place
- add unit coverage for final vs preview post_edited markers

## Root Cause
Mattermost finalizes some bot replies by editing the preview post with props.openclaw_stream_state = final. The chat frontend only cleared waiting on posted events, so Typing could linger after the visible output finished.

## Validation
- pnpm test:unit tests/unit/hooks/useMattermost.unit.spec.ts


---

## [ec65b32] chore(claw-interface): add account org v2 backfill (#2135)

- **SHA**: ec65b32b375667876fc93d0a98af106acd5148cf
- **作者**: bill-srp
- **日期**: 2026-06-01T03:02:11Z
- **PR**: #2135

### 完整 Commit Message

```
chore(claw-interface): add account org v2 backfill (#2135)

## Summary
- Add a dry-run-by-default account org v2 backfill script for personal
org creation and v2 mirror repair.
- Backfill ZooClaw computer mirrors and per-agent Mattermost workspaces
while skipping personal org creation when a current org already exists.
- Add workspace backfill upsert support plus unit coverage for dry-run,
write mode, source classification, batching, and CLI validation.

## Test plan
- [x] docker exec -w /workspaces/service-agents/services/claw-interface
service-agents-bill /home/node/.venvs/claw-interface/bin/python -m ruff
check .
- [x] docker exec -w /workspaces/service-agents/services/claw-interface
service-agents-bill /home/node/.venvs/claw-interface/bin/pyright app
tests
- [x] services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_backfill_account_org_v2_mirrors.py
services/claw-interface/tests/unit/test_agent_workspace_repo.py
- [x] services/claw-interface/.venv/bin/python -m ruff check
services/claw-interface/scripts/backfill_account_org_v2_mirrors.py
services/claw-interface/tests/unit/test_backfill_account_org_v2_mirrors.py
services/claw-interface/app/database/agent_workspace_repo.py
services/claw-interface/tests/unit/test_agent_workspace_repo.py
- [x] bash scripts/ci-lint/02-import-linter.sh
- [ ] docker exec -w /workspaces/service-agents/services/claw-interface
service-agents-bill /home/node/.venvs/claw-interface/bin/python -m
pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q (fails
in this host-created worktree devcontainer: git metadata unavailable for
deptry tests; unclosed socket warnings in unrelated OpenClaw tests;
total coverage reported 89%)
```

### PR Body

## Summary
- Add a dry-run-by-default account org v2 backfill script for personal org creation and v2 mirror repair.
- Backfill ZooClaw computer mirrors and per-agent Mattermost workspaces while skipping personal org creation when a current org already exists.
- Add workspace backfill upsert support plus unit coverage for dry-run, write mode, source classification, batching, and CLI validation.

## Test plan
- [x] docker exec -w /workspaces/service-agents/services/claw-interface service-agents-bill /home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] docker exec -w /workspaces/service-agents/services/claw-interface service-agents-bill /home/node/.venvs/claw-interface/bin/pyright app tests
- [x] services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_backfill_account_org_v2_mirrors.py services/claw-interface/tests/unit/test_agent_workspace_repo.py
- [x] services/claw-interface/.venv/bin/python -m ruff check services/claw-interface/scripts/backfill_account_org_v2_mirrors.py services/claw-interface/tests/unit/test_backfill_account_org_v2_mirrors.py services/claw-interface/app/database/agent_workspace_repo.py services/claw-interface/tests/unit/test_agent_workspace_repo.py
- [x] bash scripts/ci-lint/02-import-linter.sh
- [ ] docker exec -w /workspaces/service-agents/services/claw-interface service-agents-bill /home/node/.venvs/claw-interface/bin/python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q (fails in this host-created worktree devcontainer: git metadata unavailable for deptry tests; unclosed socket warnings in unrelated OpenClaw tests; total coverage reported 89%)

