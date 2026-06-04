# ecap-workspace — 2026-06-03

共 40 条 commits

## [5a587e01] feat(enterprise-app): integrate claw-interface APIs for session and workspace data (#2206)

- **SHA**: `5a587e01dd8f7ad055d281fcb598c0d98be5ba1d`
- **作者**: bill-srp
- **日期**: 2026-06-03T17:04:38Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/5a587e01dd8f7ad055d281fcb598c0d98be5ba1d

### 完整 Commit Message

```
feat(enterprise-app): integrate claw-interface APIs for session and workspace data (#2206)

## Linear

https://linear.app/srpone/issue/ECA-890/integrate-claw-interface-apis-for-enterprise-app-session-and-workspace

## Summary
- Add typed claw-interface API client in `web/enterprise-app/lib/claw/`
(account/me, computers, get/list agents) — calls the gateway directly
with the stored account bearer token via a single `clawFetch` choke
point (+ `ClawApiError`).
- Add `WorkspaceProvider` (console-scoped): loads `account/me` (login
gate) → `computers` → the first computer's agents, shared across all
console pages via `useWorkspace()`.
- claw `/account/me` now drives the console login gate
(`useConsoleAuthGate`); account-service `/user/me` retained for
username/email.
- Add configurable CORS middleware to claw-interface
(`CORS_ALLOW_ORIGINS`, env-driven, default-deny) so the browser can call
the gateway cross-origin.

## Test plan
- [ ] web/enterprise-app: `pnpm test` — claw client + WorkspaceProvider
+ gate (lib/claw 100% coverage)
- [ ] services/claw-interface: `pytest
tests/unit/test_cors_middleware.py`
- [ ] Manual: log in → console loads account/me → computers → first
computer's agents; 401 → /login
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-890/integrate-claw-interface-apis-for-enterprise-app-session-and-workspace

## Summary
- Add typed claw-interface API client in `web/enterprise-app/lib/claw/` (account/me, computers, get/list agents) — calls the gateway directly with the stored account bearer token via a single `clawFetch` choke point (+ `ClawApiError`).
- Add `WorkspaceProvider` (console-scoped): loads `account/me` (login gate) → `computers` → the first computer's agents, shared across all console pages via `useWorkspace()`.
- claw `/account/me` now drives the console login gate (`useConsoleAuthGate`); account-service `/user/me` retained for username/email.
- Add configurable CORS middleware to claw-interface (`CORS_ALLOW_ORIGINS`, env-driven, default-deny) so the browser can call the gateway cross-origin.

## Test plan
- [ ] web/enterprise-app: `pnpm test` — claw client + WorkspaceProvider + gate (lib/claw 100% coverage)
- [ ] services/claw-interface: `pytest tests/unit/test_cors_middleware.py`
- [ ] Manual: log in → console loads account/me → computers → first computer's agents; 401 → /login


---

## [81b89f88] refactor(claw-interface): v2 dual-write/read core for openclaw runtime state (#2176)

- **SHA**: `81b89f8888e721d9cfad9078f9a8af4bff14039c`
- **作者**: bill-srp
- **日期**: 2026-06-03T16:18:42Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/81b89f8888e721d9cfad9078f9a8af4bff14039c

### 完整 Commit Message

```
refactor(claw-interface): v2 dual-write/read core for openclaw runtime state (#2176)

## Summary

Stack 2/3 of the #2157 split. The **dual-write/read core** of the
OpenClaw runtime read-flip, carried as one unit because its tests and
code are behavior-coupled (V2-computer resolution +
\`channel_injected\`), so they can't be cut apart without an
intermediate red.

- \`runtime_state\` — V2 runtime read helpers (org resolution,
primary-computer lookup, legacy-shape + Mattermost projections)
- \`agent_workspace_repo.list_active_by_computer\` +
\`AgentMattermostRuntime.channel_injected\` — consumed by
\`runtime_state\` / \`_projectors\`
- \`bot_state_service.set_bot_status_for_computer\` — explicit-computer
dual-write
- \`_projectors\` / \`agent_mm_state_service\` — V2 computer resolution
- \`mattermost_provisioner\` / \`mattermost_reconcile\` — read via
\`runtime_state\`

\`test_agent_mm_wiring\` is an end-to-end wiring test spanning the
not-yet-flipped route/deploy consumers; it is removed here and
**reintroduced in 3/3** where its dependencies are migrated. Core paths
stay covered by \`test_agent_mm_state_service\` /
\`test_agent_mm_projectors\` / \`test_runtime_state\`.

> **Stacked on #2175** (base = \`split/1-docs\`). Review/merge after
1/3.

## Test plan
- [x] Differential unit run (base vs this branch, mongo-stubbed): **0
regressions** — identical failure set to \`main\` (all pre-existing
env/flake)
- [x] Core unit tests (\`test_runtime_state\`,
\`test_bot_state_service\`, \`test_agent_mm_*\`, \`test_mattermost_*\`,
\`test_computer_service\`) ran & passed
- [ ] CI \`python-code-quality / build-and-test\` (full unit + BDD + 90%
coverage) green
```

### PR Body

## Summary

Stack 2/3 of the #2157 split. The **dual-write/read core** of the OpenClaw runtime read-flip, carried as one unit because its tests and code are behavior-coupled (V2-computer resolution + \`channel_injected\`), so they can't be cut apart without an intermediate red.

- \`runtime_state\` — V2 runtime read helpers (org resolution, primary-computer lookup, legacy-shape + Mattermost projections)
- \`agent_workspace_repo.list_active_by_computer\` + \`AgentMattermostRuntime.channel_injected\` — consumed by \`runtime_state\` / \`_projectors\`
- \`bot_state_service.set_bot_status_for_computer\` — explicit-computer dual-write
- \`_projectors\` / \`agent_mm_state_service\` — V2 computer resolution
- \`mattermost_provisioner\` / \`mattermost_reconcile\` — read via \`runtime_state\`

\`test_agent_mm_wiring\` is an end-to-end wiring test spanning the not-yet-flipped route/deploy consumers; it is removed here and **reintroduced in 3/3** where its dependencies are migrated. Core paths stay covered by \`test_agent_mm_state_service\` / \`test_agent_mm_projectors\` / \`test_runtime_state\`.

> **Stacked on #2175** (base = \`split/1-docs\`). Review/merge after 1/3.

## Test plan
- [x] Differential unit run (base vs this branch, mongo-stubbed): **0 regressions** — identical failure set to \`main\` (all pre-existing env/flake)
- [x] Core unit tests (\`test_runtime_state\`, \`test_bot_state_service\`, \`test_agent_mm_*\`, \`test_mattermost_*\`, \`test_computer_service\`) ran & passed
- [ ] CI \`python-code-quality / build-and-test\` (full unit + BDD + 90% coverage) green

---

## [920e5264] feat(dashboard-console): add login modal with email-OTP + Google auth gate (#2205)

- **SHA**: `920e52648de074dd6c021c3cb71cca84988bf63f`
- **作者**: bill-srp
- **日期**: 2026-06-03T16:17:26Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/920e52648de074dd6c021c3cb71cca84988bf63f

### 完整 Commit Message

```
feat(dashboard-console): add login modal with email-OTP + Google auth gate (#2205)

## Linear
https://linear.app/srpone/issue/ECA-886

## Summary
- Add a **required login gate** to `web/dashboard-console`:
unauthenticated users see a non-dismissable login modal; the console
chrome and agent-packs queries only mount once authenticated.
- Auth via the shared `@zooclaw/auth-client` (email OTP) plus **Google**
sign-in through Firebase, **dynamically imported** so it never executes
in the workerd SSR bundle and code-splits out of the initial client
bundle.
- `AuthProvider`/`useAuth` over react-query (`loadCurrentUser`); MVVM
login view model (the modal holds zero logic); `AuthGate` renders a
neutral loading state while the auth query settles to avoid an SSR
login→app flash.
- Attach `Authorization: Bearer <token>` to agent-packs requests
(progress toward ECA-886's admin-token need); a 401 signs the user out
back to the gate. The seed-data fallback is retained for non-401
failures until backend CORS/admin support lands.
- Tooling: adopt **Vitest + Testing Library + jsdom** (migrated the 3
existing `node:test` files); **62 tests**. Coverage on the auth surface:
`auth.ts` 97%, `useAuth` 94%, `AuthGate`/`UserMenu` 100%, `claw-api`
100%, `LoginModal` 89%.
- Also included on this branch: a devcontainer dev-server port-exposure
fix (Vite host binding gated on `DEVCONTAINER`), and the design spec +
implementation plan under `docs/superpowers/`.

**Deploy note:** requires `VITE_ACCOUNT_URL` + `VITE_FIREBASE_*` env
(see `web/dashboard-console/.env.example`). Live agent-packs calls may
still 401 until ECA-886's backend CORS/admin endpoint lands.

## Test plan
- [ ] CI `code-quality / dashboard-quality` (typecheck + Vitest) green
- [ ] Unauthenticated load shows the non-dismissable login modal (no
sidebar/console behind it)
- [ ] Email OTP: send code → verify → gate opens to the console
- [ ] Google: popup → token exchange → gate opens
- [ ] Sign out (sidebar footer) returns to the gate
- [ ] agent-packs requests carry the bearer token; a 401 signs the user
out
- [ ] Production build succeeds with Firebase in a separate lazy chunk

---------

Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-886

## Summary
- Add a **required login gate** to `web/dashboard-console`: unauthenticated users see a non-dismissable login modal; the console chrome and agent-packs queries only mount once authenticated.
- Auth via the shared `@zooclaw/auth-client` (email OTP) plus **Google** sign-in through Firebase, **dynamically imported** so it never executes in the workerd SSR bundle and code-splits out of the initial client bundle.
- `AuthProvider`/`useAuth` over react-query (`loadCurrentUser`); MVVM login view model (the modal holds zero logic); `AuthGate` renders a neutral loading state while the auth query settles to avoid an SSR login→app flash.
- Attach `Authorization: Bearer <token>` to agent-packs requests (progress toward ECA-886's admin-token need); a 401 signs the user out back to the gate. The seed-data fallback is retained for non-401 failures until backend CORS/admin support lands.
- Tooling: adopt **Vitest + Testing Library + jsdom** (migrated the 3 existing `node:test` files); **62 tests**. Coverage on the auth surface: `auth.ts` 97%, `useAuth` 94%, `AuthGate`/`UserMenu` 100%, `claw-api` 100%, `LoginModal` 89%.
- Also included on this branch: a devcontainer dev-server port-exposure fix (Vite host binding gated on `DEVCONTAINER`), and the design spec + implementation plan under `docs/superpowers/`.

**Deploy note:** requires `VITE_ACCOUNT_URL` + `VITE_FIREBASE_*` env (see `web/dashboard-console/.env.example`). Live agent-packs calls may still 401 until ECA-886's backend CORS/admin endpoint lands.

## Test plan
- [ ] CI `code-quality / dashboard-quality` (typecheck + Vitest) green
- [ ] Unauthenticated load shows the non-dismissable login modal (no sidebar/console behind it)
- [ ] Email OTP: send code → verify → gate opens to the console
- [ ] Google: popup → token exchange → gate opens
- [ ] Sign out (sidebar footer) returns to the gate
- [ ] agent-packs requests carry the bearer token; a 401 signs the user out
- [ ] Production build succeeds with Firebase in a separate lazy chunk

---

## [a977724a] chore(composio): surface provider discovery and demand tracking (#2165)

- **SHA**: `a977724a8ca770ef6a7446aba5892a51095fed3b`
- **作者**: tim-srp
- **日期**: 2026-06-03T15:01:58Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/a977724a8ca770ef6a7446aba5892a51095fed3b

### 完整 Commit Message

```
chore(composio): surface provider discovery and demand tracking (#2165)

## Summary
- list supported and coming-soon Composio providers through the
connector page
- keep supported providers sorted ahead of coming-soon providers under
search/category filters
- track Request access clicks in `ecap-composio-provider-interest`
without per-user de-dupe
- return and display aggregate request counts on coming-soon provider
cards
- make the Request access CTA visually prominent and keep long tool
lists collapsed by default

Depends on proxy-service PR:
https://github.com/SerendipityOneInc/ecap-proxy-service/pull/84

## Tests
- pytest services/claw-interface/tests/unit/test_composio_connectors.py
-q
- ruff check
services/claw-interface/app/database/composio_provider_interest_repo.py
services/claw-interface/app/routes/composio_connectors.py
services/claw-interface/app/schema/composio_connector.py
services/claw-interface/app/lifetime.py
services/claw-interface/tests/unit/test_composio_connectors.py
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/app/composio-connectors/ComposioConnectorsClient.unit.spec.tsx
```

### PR Body

## Summary
- list supported and coming-soon Composio providers through the connector page
- keep supported providers sorted ahead of coming-soon providers under search/category filters
- track Request access clicks in `ecap-composio-provider-interest` without per-user de-dupe
- return and display aggregate request counts on coming-soon provider cards
- make the Request access CTA visually prominent and keep long tool lists collapsed by default

Depends on proxy-service PR: https://github.com/SerendipityOneInc/ecap-proxy-service/pull/84

## Tests
- pytest services/claw-interface/tests/unit/test_composio_connectors.py -q
- ruff check services/claw-interface/app/database/composio_provider_interest_repo.py services/claw-interface/app/routes/composio_connectors.py services/claw-interface/app/schema/composio_connector.py services/claw-interface/app/lifetime.py services/claw-interface/tests/unit/test_composio_connectors.py
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/app/composio-connectors/ComposioConnectorsClient.unit.spec.tsx

---

## [96f639e4] fix(billing): subscribe trial fulfillment in billing gateway (#2203)

- **SHA**: `96f639e44a65ed01969ec026078424aa80424cfe`
- **作者**: kaka-srp
- **日期**: 2026-06-03T13:22:49Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/96f639e44a65ed01969ec026078424aa80424cfe

### 完整 Commit Message

```
fix(billing): subscribe trial fulfillment in billing gateway (#2203)

## Summary
- Ensure Billing v2 subscription-wallet fulfillment always
creates/updates the BG/Lago subscription relationship before topup,
including trial entitlements.
- Update the trial fulfillment unit test to assert BG subscribe is
called.
- Include the workspace `AGENTS.md` cluster/startup instruction update.

## Root cause
Trial entitlements used `source_type=trial`, and the shared fulfillment
path skipped `billing_client.subscribe()` for that source type. The
entitlement ledger and v2 current access became active/trialing, but BG
`/credits/check` still failed because Lago had no active subscription
for the customer.

## Production repair
- Repaired customer `7453048380181188608` by creating BG subscription
`starter_20_month` under customer id `7453048380181188608`.
- Verified `/credits/check` returns `enough=true` with
`available_credits=5040`.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/ruff check
app/services/billing_v2/fulfillment.py
tests/unit/test_billing_v2_fulfillment.py`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_antom_billing_v2.py tests/unit/test_stripe_billing_v2.py
-q`
```

### PR Body

## Summary
- Ensure Billing v2 subscription-wallet fulfillment always creates/updates the BG/Lago subscription relationship before topup, including trial entitlements.
- Update the trial fulfillment unit test to assert BG subscribe is called.
- Include the workspace `AGENTS.md` cluster/startup instruction update.

## Root cause
Trial entitlements used `source_type=trial`, and the shared fulfillment path skipped `billing_client.subscribe()` for that source type. The entitlement ledger and v2 current access became active/trialing, but BG `/credits/check` still failed because Lago had no active subscription for the customer.

## Production repair
- Repaired customer `7453048380181188608` by creating BG subscription `starter_20_month` under customer id `7453048380181188608`.
- Verified `/credits/check` returns `enough=true` with `available_credits=5040`.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/ruff check app/services/billing_v2/fulfillment.py tests/unit/test_billing_v2_fulfillment.py`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_v2_fulfillment.py tests/unit/test_antom_billing_v2.py tests/unit/test_stripe_billing_v2.py -q`

---

## [e4233473] feat(settings): add desktop connect code copy (#2164)

- **SHA**: `e4233473cfb0cccf07b4a56678a058688c8e63fb`
- **作者**: tim-srp
- **日期**: 2026-06-03T13:17:19Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e4233473cfb0cccf07b4a56678a058688c8e63fb

### 完整 Commit Message

```
feat(settings): add desktop connect code copy (#2164)

## Summary
- add backend desktop connect-code endpoint that patches OpenAI gateway
config, restarts the bot, and returns a base64 code
- add Next.js proxy/client API and General settings copy button
- keep gateway/bootstrap tokens out of the UI; only copy the base64 code
to clipboard

## Linear
-
https://linear.app/srpone/issue/ECA-879/zooclaw-web%E7%AB%AF%E7%94%A8%E6%88%B7setting%E9%A1%B5%E5%A2%9E%E5%8A%A0%E4%B8%80%E4%B8%AA%E6%8C%89%E9%92%AE%E7%94%A8%E6%9D%A5%E8%8E%B7%E5%8F%96pc%E7%89%88%E6%9C%ACzooclaw%E8%BF%9E%E6%8E%A5%E4%BA%91%E7%AB%AF%E7%9A%84%E9%93%BE%E6%8E%A5

## Tests
- `ruff check app/routes/openclaw_settings/desktop.py
app/routes/openclaw_settings/router.py app/schema/openclaw_settings.py
tests/unit/test_openclaw_settings_routes.py pyproject.toml`
- `ruff format --check app/routes/openclaw_settings/desktop.py
app/routes/openclaw_settings/router.py app/schema/openclaw_settings.py
tests/unit/test_openclaw_settings_routes.py`
- `pytest tests/unit/test_openclaw_settings_routes.py -k
DesktopConnectCode`
- `pnpm --filter @zooclaw/web-app exec eslint
web/app/src/app/api/openclaw/settings/desktop-connect-code/route.ts
web/app/src/components/settings/GeneralTab.tsx
web/app/src/lib/api/openclaw-settings.ts web/app/src/locales/en.ts
web/app/tests/unit/app/api/openclaw-status-settings.unit.spec.ts
web/app/tests/unit/components/settings/GeneralTab.unit.spec.tsx
web/app/tests/unit/lib/api/openclaw-settings.unit.spec.ts`
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit --pretty false`
- `pnpm --filter @zooclaw/web-app run test:unit --
tests/unit/lib/api/openclaw-settings.unit.spec.ts
tests/unit/components/settings/GeneralTab.unit.spec.tsx
tests/unit/app/api/openclaw-status-settings.unit.spec.ts`
```

### PR Body

## Summary
- add backend desktop connect-code endpoint that patches OpenAI gateway config, restarts the bot, and returns a base64 code
- add Next.js proxy/client API and General settings copy button
- keep gateway/bootstrap tokens out of the UI; only copy the base64 code to clipboard

## Linear
- https://linear.app/srpone/issue/ECA-879/zooclaw-web%E7%AB%AF%E7%94%A8%E6%88%B7setting%E9%A1%B5%E5%A2%9E%E5%8A%A0%E4%B8%80%E4%B8%AA%E6%8C%89%E9%92%AE%E7%94%A8%E6%9D%A5%E8%8E%B7%E5%8F%96pc%E7%89%88%E6%9C%ACzooclaw%E8%BF%9E%E6%8E%A5%E4%BA%91%E7%AB%AF%E7%9A%84%E9%93%BE%E6%8E%A5

## Tests
- `ruff check app/routes/openclaw_settings/desktop.py app/routes/openclaw_settings/router.py app/schema/openclaw_settings.py tests/unit/test_openclaw_settings_routes.py pyproject.toml`
- `ruff format --check app/routes/openclaw_settings/desktop.py app/routes/openclaw_settings/router.py app/schema/openclaw_settings.py tests/unit/test_openclaw_settings_routes.py`
- `pytest tests/unit/test_openclaw_settings_routes.py -k DesktopConnectCode`
- `pnpm --filter @zooclaw/web-app exec eslint web/app/src/app/api/openclaw/settings/desktop-connect-code/route.ts web/app/src/components/settings/GeneralTab.tsx web/app/src/lib/api/openclaw-settings.ts web/app/src/locales/en.ts web/app/tests/unit/app/api/openclaw-status-settings.unit.spec.ts web/app/tests/unit/components/settings/GeneralTab.unit.spec.tsx web/app/tests/unit/lib/api/openclaw-settings.unit.spec.ts`
- `pnpm --filter @zooclaw/web-app exec tsc --noEmit --pretty false`
- `pnpm --filter @zooclaw/web-app run test:unit -- tests/unit/lib/api/openclaw-settings.unit.spec.ts tests/unit/components/settings/GeneralTab.unit.spec.tsx tests/unit/app/api/openclaw-status-settings.unit.spec.ts`

---

## [ad08bebb] fix(billing): preserve local cancel on stale active updates (#2201)

- **SHA**: `ad08bebb4eb95c5eb1de29a8a556eacfe92bc95d`
- **作者**: kaka-srp
- **日期**: 2026-06-03T12:48:49Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/ad08bebb4eb95c5eb1de29a8a556eacfe92bc95d

### 完整 Commit Message

```
fix(billing): preserve local cancel on stale active updates (#2201)

## Summary
- Preserve local `canceling` / `cancel_at_period_end` when non-user
stale ACTIVE subscription facts retry against the latest agreement
state.
- Keep user-initiated renew / clear-cancel flows allowed.
- Add regression coverage for the CAS race window raised by CI review.

## Root cause
After #2199 allowed the legitimate `canceling -> active` state
transition, a stale provider ACTIVE update could load an `active`
snapshot, lose CAS to a concurrent local cancel, then retry against the
latest `canceling` agreement and clear `cancel_at_period_end` because
the service-layer stale-live guard only preserved `current` and
`current_period_end`.

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/ruff check
app/services/billing_v2/subscription_agreement_upsert.py
app/services/billing_v2/subscription_agreements.py
tests/unit/test_billing_v2_subscription_agreements.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_billing_v2_subscription_agreements.py -q`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_billing_v2_*.py tests/unit/test_antom_billing_v2.py -q`
- [x] `cd services/claw-interface && scripts/ci-lint/01-file-length.sh`
```

### PR Body

## Summary
- Preserve local `canceling` / `cancel_at_period_end` when non-user stale ACTIVE subscription facts retry against the latest agreement state.
- Keep user-initiated renew / clear-cancel flows allowed.
- Add regression coverage for the CAS race window raised by CI review.

## Root cause
After #2199 allowed the legitimate `canceling -> active` state transition, a stale provider ACTIVE update could load an `active` snapshot, lose CAS to a concurrent local cancel, then retry against the latest `canceling` agreement and clear `cancel_at_period_end` because the service-layer stale-live guard only preserved `current` and `current_period_end`.

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/ruff check app/services/billing_v2/subscription_agreement_upsert.py app/services/billing_v2/subscription_agreements.py tests/unit/test_billing_v2_subscription_agreements.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_billing_v2_subscription_agreements.py -q`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_billing_v2_*.py tests/unit/test_antom_billing_v2.py -q`
- [x] `cd services/claw-interface && scripts/ci-lint/01-file-length.sh`

---

## [85d1a3c1] chore(enterprise-app): add auth gate and login (#2170)

- **SHA**: `85d1a3c1694124e45de2f13112c90128d93cd325`
- **作者**: bill-srp
- **日期**: 2026-06-03T12:14:40Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/85d1a3c1694124e45de2f13112c90128d93cd325

### 完整 Commit Message

```
chore(enterprise-app): add auth gate and login (#2170)

## Linear
Not applicable: PR title is `chore`, not `feat`.

## Summary
- Add enterprise-app auth helpers around `@zooclaw/auth-client` and
Firebase.
- Add React Query auth provider, protected console gate, and logout
wiring.
- Add login UI and view model for Google, phone, and email-code sign-in.

## Test plan
- [x] `pnpm --filter @zooclaw/enterprise-app test`
- [x] `pnpm --filter @zooclaw/enterprise-app tsc`
- [x] `pnpm --filter @zooclaw/enterprise-app lint` exited 0 with known
warning-only output

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Linear
Not applicable: PR title is `chore`, not `feat`.

## Summary
- Add enterprise-app auth helpers around `@zooclaw/auth-client` and Firebase.
- Add React Query auth provider, protected console gate, and logout wiring.
- Add login UI and view model for Google, phone, and email-code sign-in.

## Test plan
- [x] `pnpm --filter @zooclaw/enterprise-app test`
- [x] `pnpm --filter @zooclaw/enterprise-app tsc`
- [x] `pnpm --filter @zooclaw/enterprise-app lint` exited 0 with known warning-only output


---

## [86e63450] fix(billing): guard subscription agreement state updates (#2199)

- **SHA**: `86e634509c606a766c250dad15ab8bcce9109922`
- **作者**: kaka-srp
- **日期**: 2026-06-03T12:18:10Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/86e634509c606a766c250dad15ab8bcce9109922

### 完整 Commit Message

```
fix(billing): guard subscription agreement state updates (#2199)

## Summary
- Complete subscription agreement transition coverage for Antom
lifecycle states while keeping active -> pending regression blocked.
- Add guarded/CAS agreement updates and duplicate-key retry revalidation
so raced webhook handlers cannot bypass the state machine.
- Treat late paid Antom CREATE + ACTIVE status webhooks as processed
no-ops once the agreement has already been settled by payment success.
- Keep stale Antom ACTIVE status webhooks from clearing local
canceling/cancel_at_period_end state.
- Split guarded upsert helpers into a dedicated module to keep the main
agreement service under CI file-length limits.

## Root cause
Antom subscription payment success can settle an agreement to
active/current before a delayed SUBSCRIPTION_STATUS CREATE + ACTIVE
webhook arrives. That late status maps to pending/current=false for paid
subscriptions, so the previous implementation could overwrite the active
agreement, clear current fields, and leave downstream bot startup seeing
the subscription as not current.

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/ruff format --check .`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/ruff check .`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `cd services/claw-interface && scripts/ci-lint/01-file-length.sh`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_antom_billing_v2.py
tests/unit/test_billing_v2_subscription_agreements.py -q` (47 passed)
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_billing_v2_*.py tests/unit/test_antom_billing_v2.py
tests/unit/test_antom_handlers.py tests/unit/test_apple_billing_v2*.py
tests/unit/test_stripe_billing_v2*.py -q` (318 passed)
- [ ] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pytest --cov=app
--cov-report=term-missing --cov-fail-under=90 -q` was started but not
completed; it was stopped before completion after one unrelated OpenClaw
agent test failure was observed.
```

### PR Body

## Summary
- Complete subscription agreement transition coverage for Antom lifecycle states while keeping active -> pending regression blocked.
- Add guarded/CAS agreement updates and duplicate-key retry revalidation so raced webhook handlers cannot bypass the state machine.
- Treat late paid Antom CREATE + ACTIVE status webhooks as processed no-ops once the agreement has already been settled by payment success.
- Keep stale Antom ACTIVE status webhooks from clearing local canceling/cancel_at_period_end state.
- Split guarded upsert helpers into a dedicated module to keep the main agreement service under CI file-length limits.

## Root cause
Antom subscription payment success can settle an agreement to active/current before a delayed SUBSCRIPTION_STATUS CREATE + ACTIVE webhook arrives. That late status maps to pending/current=false for paid subscriptions, so the previous implementation could overwrite the active agreement, clear current fields, and leave downstream bot startup seeing the subscription as not current.

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/ruff format --check .`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/ruff check .`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `cd services/claw-interface && scripts/ci-lint/01-file-length.sh`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_antom_billing_v2.py tests/unit/test_billing_v2_subscription_agreements.py -q` (47 passed)
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_billing_v2_*.py tests/unit/test_antom_billing_v2.py tests/unit/test_antom_handlers.py tests/unit/test_apple_billing_v2*.py tests/unit/test_stripe_billing_v2*.py -q` (318 passed)
- [ ] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` was started but not completed; it was stopped before completion after one unrelated OpenClaw agent test failure was observed.

---

## [6a18a6f0] refactor(web): model LoginCheckProvider modal as an event-driven reducer (#2196) (#2198)

- **SHA**: `6a18a6f00a0f4ed8145e3b05a3901e7256eda319`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T12:04:41Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6a18a6f00a0f4ed8145e3b05a3901e7256eda319

### 完整 Commit Message

```
refactor(web): model LoginCheckProvider modal as an event-driven reducer (#2196) (#2198)

## What & why

Fixes **part 1** of #2196 — model modal visibility as an event-driven
reducer instead of a bare `useState<boolean>` driven by scattered
transition effects.

`LoginCheckProvider`'s modal `open` state was a bare boolean written by
**three scattered transition effects** plus **two prev-value refs**
(`prevPathnameRef`, `lastSeenRequestRef`). This PR collapses all of that
into a single event-driven `useReducer`, mirroring the in-repo
`useArtifactsSidebar` pattern (the codebase's existing "good version" of
this shape).

Each signal becomes an **event**, and the open/close decision —
including the three pathname hydration/locale subtleties — now lives in
a **pure, directly unit-testable reducer**:

| Event | Replaces |
|---|---|
| `show-requested` | the `showRequest` effect + `lastSeenRequestRef`
dedupe |
| `auth-changed` | the `userInfoType === '1'` auto-close effect |
| `navigated` | the pathname-change effect + `prevPathnameRef` (3
subtleties moved into the reducer) |
| `open` / `close` | `checkLogin` / `showLoginModal` / `hideLoginModal`
setters |

The three effects shrink to one-line dispatchers; the two refs are gone
(their state lives in the reducer).

## Behavior-preserving

- `isModalOpen` is **fully internal** — verified that all 16
`useLoginCheck()` consumers call only the 4 public methods (`checkLogin`
/ `showLoginModal` / `hideLoginModal` / `onLoginSuccess`); none read
modal state. The public contract is unchanged.
- The 3 documented pathname invariants are preserved (now as reducer
logic): hydration `null` ignore, value-based comparison
(StrictMode-safe), and `removeLocaleFromPathname` normalization so
`/en/chat ↔ /chat` oscillation isn't treated as navigation.
- Effect definition order preserved so same-commit multi-dep changes
dispatch in the prior sequence.
- Only intentional drop: the dev-only `logger.log` on pathname-close
(kept the reducer pure; `logger.log` is stripped in prod and asserted by
no test).

> Note: this is **not** a render-time-derivation rewrite (that approach
previously broke 9 tests on this exact auto-close and was reverted). A
reducer keeps the effect-dispatch model, so transition semantics are
identical.

## Tests

- The **17 existing integration tests pass unchanged** (they are the
characterization baseline — all 7 events + the 3 subtleties + the "real
nav still closes" sanity case).
- Added **8 pure-reducer unit tests** (`describe('modalReducer')`)
asserting the subtleties directly without rendering — the testability
win of the refactor. **25/25 green.**
- `tsc --noEmit` and `eslint` clean on the changed files.

## Scope

`LoginCheckProvider` only. `OnboardingProvider` (the other provider
named in #2196) is **deferred** to a follow-up PR — its `isModalOpen` is
exposed in `OnboardingContext` and entangled with the
progress/`localProgress`/resolution triad, so it needs separate scoping.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

---

## [cfef79fe] feat(dashboard): agent packs admin — list, CRUD, submissions, claw API (#2189)

- **SHA**: `cfef79fea324aaf70d6d1ed0ebf2669bd6c7e3cd`
- **作者**: bill-srp
- **日期**: 2026-06-03T11:33:46Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/cfef79fea324aaf70d6d1ed0ebf2669bd6c7e3cd

### 完整 Commit Message

```
feat(dashboard): agent packs admin — list, CRUD, submissions, claw API (#2189)

## Linear

https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

**PR 2 of 2** — the agent-packs feature, layered on the dashboard shell
merged in #2174.

- `/agent-packs` catalogue: list with create / edit / submit-version
flows (scrollable dialog editor), plus avatar + pack-archive upload (R2)
- `/agent-packs/:packId/submissions` history with approve / reject
actions
- Client-side data layer: a React Query hook fetching the claw-interface
`/internal/agent-packs` API directly from the browser
(`VITE_CLAW_INTERFACE_URL`, since the Worker is network-restricted),
plus the packs domain model and route view-models
- Feature UI primitives (`badge`, `card`, `dialog`, `table`) and 16 unit
tests (`packs`, `claw-url`)

Wires `QueryClientProvider`, the agent-packs routes, the sidebar nav
entry, and the home CTA into the shell. Validated by the
`dashboard-quality` CI job added in #2174.

## Known follow-ups (from ECA-886 / #2158 reviews)
- Backend CORS + admin auth on `/internal/agent-packs` — the
browser-direct fetch is currently unauthenticated. `TODO(ECA-886)`
- Real R2 upload — `r2-upload.ts` is still a mock. `TODO(ECA-886)`

## PR size
`size-override` applied (~3.4k lines). The feature shares one data layer
(`packs.ts` alone is 576 lines) so it can't be split under the 2000-line
gate without fragmenting a cohesive feature; a large share is vendored
shadcn primitives + tests.

## Test plan
- [x] dashboard `typecheck` passes (cf-typegen + react-router typegen +
`tsc -b`)
- [x] dashboard `test` — 16/16 pass
- [x] `pnpm install --frozen-lockfile` consistent
- [ ] CI green (`dashboard-quality` + `size-override`)
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

**PR 2 of 2** — the agent-packs feature, layered on the dashboard shell merged in #2174.

- `/agent-packs` catalogue: list with create / edit / submit-version flows (scrollable dialog editor), plus avatar + pack-archive upload (R2)
- `/agent-packs/:packId/submissions` history with approve / reject actions
- Client-side data layer: a React Query hook fetching the claw-interface `/internal/agent-packs` API directly from the browser (`VITE_CLAW_INTERFACE_URL`, since the Worker is network-restricted), plus the packs domain model and route view-models
- Feature UI primitives (`badge`, `card`, `dialog`, `table`) and 16 unit tests (`packs`, `claw-url`)

Wires `QueryClientProvider`, the agent-packs routes, the sidebar nav entry, and the home CTA into the shell. Validated by the `dashboard-quality` CI job added in #2174.

## Known follow-ups (from ECA-886 / #2158 reviews)
- Backend CORS + admin auth on `/internal/agent-packs` — the browser-direct fetch is currently unauthenticated. `TODO(ECA-886)`
- Real R2 upload — `r2-upload.ts` is still a mock. `TODO(ECA-886)`

## PR size
`size-override` applied (~3.4k lines). The feature shares one data layer (`packs.ts` alone is 576 lines) so it can't be split under the 2000-line gate without fragmenting a cohesive feature; a large share is vendored shadcn primitives + tests.

## Test plan
- [x] dashboard `typecheck` passes (cf-typegen + react-router typegen + `tsc -b`)
- [x] dashboard `test` — 16/16 pass
- [x] `pnpm install --frozen-lockfile` consistent
- [ ] CI green (`dashboard-quality` + `size-override`)


---

## [7e7d9bf8] refactor(enterprise-app): add ci and view models (#2169)

- **SHA**: `7e7d9bf81bfa1faf0f64fccb9864fefa89f6c7a3`
- **作者**: bill-srp
- **日期**: 2026-06-03T11:30:59Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7e7d9bf81bfa1faf0f64fccb9864fefa89f6c7a3

### 完整 Commit Message

```
refactor(enterprise-app): add ci and view models (#2169)

## Linear
Not applicable: PR title is `refactor`, not `feat`.

## Summary
- Register `@zooclaw/enterprise-app` in workspace CI surfaces.
- Remove dead enterprise-app code surfaced by lint and usage scans.
- Extract market and workbench view models with focused tests.

## Test plan
- [x] `pnpm --filter @zooclaw/enterprise-app test`
- [x] `pnpm --filter @zooclaw/enterprise-app tsc`
- [x] `pnpm --filter @zooclaw/enterprise-app lint` exited 0 with known
warning-only output

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Linear
Not applicable: PR title is `refactor`, not `feat`.

## Summary
- Register `@zooclaw/enterprise-app` in workspace CI surfaces.
- Remove dead enterprise-app code surfaced by lint and usage scans.
- Extract market and workbench view models with focused tests.

## Test plan
- [x] `pnpm --filter @zooclaw/enterprise-app test`
- [x] `pnpm --filter @zooclaw/enterprise-app tsc`
- [x] `pnpm --filter @zooclaw/enterprise-app lint` exited 0 with known warning-only output


---

## [923d4115] chore(web): simplify window.open guard to must-be-zero (#2128) (#2193)

- **SHA**: `923d411508050c73e86dd1fe248281a0755e988e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T11:30:58Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/923d411508050c73e86dd1fe248281a0755e988e

### 完整 Commit Message

```
chore(web): simplify window.open guard to must-be-zero (#2128) (#2193)

Follows the completed #2128 migration (#2132 / #2184 / #2187 / #2190 /
#2192).

## What

Now that every raw `window.open` is funneled through
`src/lib/window-open.ts` and the disable count is **0**, replace the
shrink-only counter with a flat **must-be-zero** check.

- `check-window-open-disables-shrink-only.sh` (~97 lines: `git fetch
origin main` + `git archive` its `src/` tree + base-vs-head count +
bootstrap-skip detection) → **`check-no-window-open-disables.sh`** (~35
lines: grep the `window.open #2128` disable tag, fail if any exist).
- Updated `code-quality.yml` `pre_lint_scripts` entry + the ESLint Rule
13 comment.

## Why

The shrink-only machinery only mattered *while* sites were being
migrated (count had to monotonically decrease from 22). At 0,
enforcement is equivalent and simpler:
- a new raw `window.open(...)` trips **ESLint Rule 13** directly;
- a disable-comment bypass trips **this guard**.

No git / network / temp-dir machinery needed.

## Verification
- New guard passes on `main` (0 disables); manually verified it
**fails** when a `window.open #2128` disable comment is injected.
- No stale references to the old script name remain (`grep` across
`*.yml` / `*.mjs` / `*.sh`).
- `eslint` config still valid; `pnpm lint` clean.
- CI tooling change — no unit test (consistent with the sibling
shrink-only scripts).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [6d45a74b] refactor(web): migrate billing window.open sites to openExternal (#2128) (#2192)

- **SHA**: `6d45a74b910b54125d2d63e5a38bb2fbedf4cbde`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T11:16:06Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6d45a74b910b54125d2d63e5a38bb2fbedf4cbde

### 完整 Commit Message

```
refactor(web): migrate billing window.open sites to openExternal (#2128) (#2192)

Tracking: #2128 · **Final migration** · Follows #2132 / #2184 / #2187 /
#2190

## What (PR 4 — billing payment-path opens)

Migrate the last 8 raw `window.open` sites — all `window.open(url,
'_blank', 'noopener,noreferrer')` — to `openExternal(url)` (the helper's
secure default *is* `noopener,noreferrer`, so byte-identical):
- `SubscriptionPanel` — 5 (subscribe Stripe + Antom, topup Stripe +
Antom, customer portal)
- `PaywallContent` — 2 (Stripe + Antom checkout)
- `InvoiceHistory` — 1 (Stripe customer/billing portal)

## This completes #2128

`window.open` disable count **8 → 0**. Every raw `window.open` in `src/`
is now funneled through `src/lib/window-open.ts`; ESLint Rule 13 rejects
new raw calls and the shrink-only guard holds the count at 0.

## Behavior preserved

No functional change (payment path). Existing specs already assert the
3-arg `'_blank', 'noopener,noreferrer'` form and pass **unchanged**
(SubscriptionPanel happy-path + topup + portal, PaywallContent
Stripe/Antom, InvoiceHistory portal). No test edits.

## Verification
- Billing specs: 96 passed (SubscriptionPanel + extras + PaywallContent
+ InvoiceHistory), unchanged
- `pnpm lint` clean; full `tsc --noEmit` clean; window.open audit: 0;
disable count: 0
- shrink-only guard: 8 → 0 PASS
- Rebased onto latest `main` (picks up the enterprise-app console
migration #2168 merged mid-series)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [e64602aa] chore(enterprise-app): migrate console views (#2168)

- **SHA**: `e64602aaab6ecc572cc107910af36aa7371beeb2`
- **作者**: bill-srp
- **日期**: 2026-06-03T11:01:09Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e64602aaab6ecc572cc107910af36aa7371beeb2

### 完整 Commit Message

```
chore(enterprise-app): migrate console views (#2168)

## Linear
Not applicable: PR title is `chore`, not `feat`.

## Summary
- Move enterprise app router files out of `src`.
- Add the migrated ZooClaw OS console shell and 8 console pages.
- Add shared data, brand assets, UI primitives, overlays, and console
routing.

## Test plan
- [x] Verified as part of top stack checks on
`split/enterprise-app-auth`.
- [x] `pnpm --filter @zooclaw/enterprise-app test`
- [x] `pnpm --filter @zooclaw/enterprise-app tsc`
- [x] `pnpm --filter @zooclaw/enterprise-app lint` exited 0 with known
warning-only output

## Size override
`size-override` applied. This is a single cohesive migration of the
existing ZooClaw OS prototype console — 8 routed pages + the app shell +
shared overlays/UI primitives + mock data and binary brand assets. The
bulk is generated mock-data UI and image assets, not hand-written logic,
and it can't be split further without landing a half-wired console that
doesn't build. Splitting per-page would only add merge churn for no
review benefit.

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: bill-srp <undefined@users.noreply.github.com>
Co-authored-by: Copilot Autofix powered by AI <62310815+github-advanced-security[bot]@users.noreply.github.com>
```

### PR Body

## Linear
Not applicable: PR title is `chore`, not `feat`.

## Summary
- Move enterprise app router files out of `src`.
- Add the migrated ZooClaw OS console shell and 8 console pages.
- Add shared data, brand assets, UI primitives, overlays, and console routing.

## Test plan
- [x] Verified as part of top stack checks on `split/enterprise-app-auth`.
- [x] `pnpm --filter @zooclaw/enterprise-app test`
- [x] `pnpm --filter @zooclaw/enterprise-app tsc`
- [x] `pnpm --filter @zooclaw/enterprise-app lint` exited 0 with known warning-only output

## Size override
`size-override` applied. This is a single cohesive migration of the existing ZooClaw OS prototype console — 8 routed pages + the app shell + shared overlays/UI primitives + mock data and binary brand assets. The bulk is generated mock-data UI and image assets, not hand-written logic, and it can't be split further without landing a half-wired console that doesn't build. Splitting per-page would only add merge churn for no review benefit.


---

## [7be34f8a] refactor(web): migrate C-class OAuth popups to openBlankPopup (#2128) (#2190)

- **SHA**: `7be34f8adc21c4503cf64f839f359373fc40de75`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T11:01:50Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7be34f8adc21c4503cf64f839f359373fc40de75

### 完整 Commit Message

```
refactor(web): migrate C-class OAuth popups to openBlankPopup (#2128) (#2190)

Tracking: #2128 · Follows #2132 / #2184 / #2187

## What (PR 3 — C-class OAuth/invoice popups)

Migrate the two `about:blank`-presync popups to `openBlankPopup()`:
- `ComposioConnectorsClient` — connector OAuth connect
- `InvoiceHistory` — Stripe hosted-invoice download

`openBlankPopup()` encapsulates the shared, Safari-safe dance —
synchronous `window.open('about:blank', '_blank')` + defensive `opener =
null` (try/catch) — and exposes `navigate(url): boolean` / `close()`.
The **per-site fallback stays at the call site** because they differ:
- Composio: blocked popup → `window.location.assign(auth_url)` (full
redirect)
- InvoiceHistory: blocked popup / missing URL → `close()` + "not
available" toast

## Behavior preserved

No functional change. The existing specs already assert the exact
`openBlankPopup` contract and pass **unchanged**:
- Composio: `window.open('about:blank','_blank')`, `popup.opener ===
null`, `popup.location.href === auth_url`, `popup.close()` on
connect-link failure
- InvoiceHistory: same about:blank open + `opener === null` +
`location.href` navigation on success (`close()` NOT called), and
`close()` + "not available" toast on the missing-URL path

`window.open` disable count **10 → 8**. (InvoiceHistory's line-162
billing-portal `window.open(url, '_blank', 'noopener,noreferrer')` is
A-class/PR-4 scope and remains disabled; its test at L221 is untouched.)

## Verification
- Composio (17) + InvoiceHistory specs: 38 passed, unchanged
- `pnpm lint` clean; changed files tsc-clean (only pre-existing local
`motion` cascade, resolved in CI); window.open audit: 0

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [1d8bd88a] refactor(web): migrate B-class sized-popup window.open to openExternal (#2128) (#2187)

- **SHA**: `1d8bd88a328c707f3190b93072ec3c218a63e1d3`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T10:49:03Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/1d8bd88a328c707f3190b93072ec3c218a63e1d3

### 完整 Commit Message

```
refactor(web): migrate B-class sized-popup window.open to openExternal (#2128) (#2187)

Tracking: #2128 · Follows #2132 (PR 0) + #2184 (PR 1)

## What (PR 2 — B-class sized popups)

Migrate the 2 fixed-size OAuth connect popups to `openExternal`:
- `ConnectorsSection.tsx` — `openExternal(url, { features:
'width=600,height=700' })`
- `IntegrationsSection.tsx` — same

**Byte-identical behavior**: when `features` is provided, `openExternal`
passes it to `window.open` verbatim (no `noopener` added) — so the call
remains `window.open(url, '_blank', 'width=600,height=700')`. The
existing tests already assert this 3-arg form, so they pass unchanged
(no test edits).

`window.open` disable count **12 → 10** (shrink-only guard enforces the
decrease).

## Verification
- `ConnectorsSection` + `IntegrationsSection` specs: 51 passed
(unchanged)
- `pnpm lint` clean; changed files tsc-clean (only pre-existing local
`motion/react` cascade noise, resolved in CI per #2132/#2184);
window.open audit: 0

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [24303559] refactor(web): make useAuth the canonical auth hook; unify login predicate (#2172)

- **SHA**: `24303559b7fa11210a94bafcd8f31c83f59e46a2`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T10:43:50Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/24303559b7fa11210a94bafcd8f31c83f59e46a2

### 完整 Commit Message

```
refactor(web): make useAuth the canonical auth hook; unify login predicate (#2172)

## What & why

Review follow-up to #2131. That PR inlined the authoritative login
predicate (`type === '1' && !!access_token`) in `PublicPricingClient`.
Investigating revealed the real problem: auth state is read **four
different ways** across ~100 render-path sites — `useAuth()` (×32),
ad-hoc `useAuthSnapshot((s)=>…)` (×11), imperative `isLoggedIn()` (×31),
imperative `getPlanTier()`/`getUserInfo()` (×35) — and
`useAuth().isLoggedIn` had drifted to a token-less `type === '1'`.

The auth snapshot is tiny (`userInfo` + `subscriptionInfo`) and changes
only on **rare, discrete events** (login / logout / token refresh /
billing init) — so granular selector hooks have no perf payoff and only
fragment the API further. **Plan A: consolidate on `useAuth()` as the
single reactive auth source.**

## Changes (this PR = the foundation)
- **`isLoggedInUserInfo(userInfo)`** — new pure predicate in
`auth/storage.ts`; the single definition of "logged in". `isLoggedIn()`
delegates to it.
- **`useAuth()`** — `isLoggedIn` now uses the predicate (**token-check
fix**, see below) and the hook additionally exposes `subscriptionInfo`
(parallel to `userInfo`).
- **`PublicPricingClient`** — derives `isLoggedIn` + `currentPlan` from
`useAuth()` alone (was: inline predicate + ad-hoc `useAuthSnapshot`
selector).
- Regression tests for the predicate (`storage.unit.spec`) and
`useAuth()` tokenless case; test mock exposes `isLoggedInUserInfo`.

> An earlier revision of this PR added a `useIsLoggedIn()` selector
hook; that was the wrong call (extra layer, no perf benefit for
near-static auth state) and has been removed in favor of `useAuth()`.

## ⚠️ Behavior change — reviewer confirmation requested
`useAuth().isLoggedIn` now **requires an access_token** (was `type ===
'1'` alone). A tokenless type-1 record is now treated as NOT logged in,
matching `isLoggedIn()`. Blast radius ~10 consumers (chat,
OnboardingProvider, MattermostProvider, composio, claw-settings…). Full
suite (455 files / 6750 tests) passes unchanged; requiring a token is
the security-correct direction. Flagging for confirmation.

## Follow-up (not in this PR)
Migrate the remaining ad-hoc `useAuthSnapshot` selectors + in-render
imperative `isLoggedIn()`/`getPlanTier()`/`getUserInfo()` calls onto
`useAuth()`; reserve the imperative readers for non-React code
(`auth/manager.ts`, API interceptors). Tracked as an incremental epic.

## Verification
- `tsc --noEmit` clean; `eslint` clean (one pre-existing `any` warning
in mocks.ts, unrelated).
- Full unit suite: **455 files / 6750 tests pass**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What & why

Review follow-up to #2131. That PR inlined the authoritative login predicate (`type === '1' && !!access_token`) in `PublicPricingClient`. Investigating revealed the real problem: auth state is read **four different ways** across ~100 render-path sites — `useAuth()` (×32), ad-hoc `useAuthSnapshot((s)=>…)` (×11), imperative `isLoggedIn()` (×31), imperative `getPlanTier()`/`getUserInfo()` (×35) — and `useAuth().isLoggedIn` had drifted to a token-less `type === '1'`.

The auth snapshot is tiny (`userInfo` + `subscriptionInfo`) and changes only on **rare, discrete events** (login / logout / token refresh / billing init) — so granular selector hooks have no perf payoff and only fragment the API further. **Plan A: consolidate on `useAuth()` as the single reactive auth source.**

## Changes (this PR = the foundation)
- **`isLoggedInUserInfo(userInfo)`** — new pure predicate in `auth/storage.ts`; the single definition of "logged in". `isLoggedIn()` delegates to it.
- **`useAuth()`** — `isLoggedIn` now uses the predicate (**token-check fix**, see below) and the hook additionally exposes `subscriptionInfo` (parallel to `userInfo`).
- **`PublicPricingClient`** — derives `isLoggedIn` + `currentPlan` from `useAuth()` alone (was: inline predicate + ad-hoc `useAuthSnapshot` selector).
- Regression tests for the predicate (`storage.unit.spec`) and `useAuth()` tokenless case; test mock exposes `isLoggedInUserInfo`.

> An earlier revision of this PR added a `useIsLoggedIn()` selector hook; that was the wrong call (extra layer, no perf benefit for near-static auth state) and has been removed in favor of `useAuth()`.

## ⚠️ Behavior change — reviewer confirmation requested
`useAuth().isLoggedIn` now **requires an access_token** (was `type === '1'` alone). A tokenless type-1 record is now treated as NOT logged in, matching `isLoggedIn()`. Blast radius ~10 consumers (chat, OnboardingProvider, MattermostProvider, composio, claw-settings…). Full suite (455 files / 6750 tests) passes unchanged; requiring a token is the security-correct direction. Flagging for confirmation.

## Follow-up (not in this PR)
Migrate the remaining ad-hoc `useAuthSnapshot` selectors + in-render imperative `isLoggedIn()`/`getPlanTier()`/`getUserInfo()` calls onto `useAuth()`; reserve the imperative readers for non-React code (`auth/manager.ts`, API interceptors). Tracked as an incremental epic.

## Verification
- `tsc --noEmit` clean; `eslint` clean (one pre-existing `any` warning in mocks.ts, unrelated).
- Full unit suite: **455 files / 6750 tests pass**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## [9aebf1fe] feat(dashboard): scaffold React Router v7 admin dashboard shell on Workers (#2174)

- **SHA**: `9aebf1fe44163b6fda530c877c31bd61a7dfa5e7`
- **作者**: bill-srp
- **日期**: 2026-06-03T10:37:46Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9aebf1fe44163b6fda530c877c31bd61a7dfa5e7

### 完整 Commit Message

```
feat(dashboard): scaffold React Router v7 admin dashboard shell on Workers (#2174)

## Linear

https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

**PR 1 of 2** — splits the closed #2158 (agent-pack admin dashboard)
into two smaller, independently reviewable PRs. This one lands the
**dashboard shell only**, with no agent-packs feature logic.

- New `@zooclaw/dashboard-app`: a **React Router v7** app on Cloudflare
Workers (`web/dashboard`), distinct from the Next.js enterprise-admin
console
- shadcn/ui primitives scoped to what the shell actually consumes
(`button`, `input`, `separator`, `sheet`, `sidebar`, `skeleton`,
`tooltip`)
- Collapsible sidebar layout (`dashboard-shell`) with an Overview-only
nav and a blank masthead home page
- Registered as a pnpm workspace member and wired into the
`dependabot-lockfile-refresh` + `auto-review` workflows

The agent-packs catalogue (list/CRUD, submit-version flow, submissions
history, claw-interface API) lands in **PR 2** once this merges.

## Test plan
- [x] `pnpm typecheck` (cf-typegen + react-router typegen + `tsc -b`)
passes
- [x] `pnpm test` passes (0 tests — the suite ships with the feature in
PR 2)
- [x] `pnpm install --frozen-lockfile` is consistent (CI-equivalent)
- [ ] CI green on this PR
## PR size
`size-override` applied (~2045 lines, just over the 2000 gate). The bulk
is **generated/vendored**, not hand-written logic: the pnpm-lock delta
for a new workspace app plus shadcn/ui primitives copied verbatim from
the registry. Mirrors the original #2158, which also carried
`size-override`. Splitting the scaffold further would fragment a single
coherent app skeleton.
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary

**PR 1 of 2** — splits the closed #2158 (agent-pack admin dashboard) into two smaller, independently reviewable PRs. This one lands the **dashboard shell only**, with no agent-packs feature logic.

- New `@zooclaw/dashboard-app`: a **React Router v7** app on Cloudflare Workers (`web/dashboard`), distinct from the Next.js enterprise-admin console
- shadcn/ui primitives scoped to what the shell actually consumes (`button`, `input`, `separator`, `sheet`, `sidebar`, `skeleton`, `tooltip`)
- Collapsible sidebar layout (`dashboard-shell`) with an Overview-only nav and a blank masthead home page
- Registered as a pnpm workspace member and wired into the `dependabot-lockfile-refresh` + `auto-review` workflows

The agent-packs catalogue (list/CRUD, submit-version flow, submissions history, claw-interface API) lands in **PR 2** once this merges.

## Test plan
- [x] `pnpm typecheck` (cf-typegen + react-router typegen + `tsc -b`) passes
- [x] `pnpm test` passes (0 tests — the suite ships with the feature in PR 2)
- [x] `pnpm install --frozen-lockfile` is consistent (CI-equivalent)
- [ ] CI green on this PR
## PR size
`size-override` applied (~2045 lines, just over the 2000 gate). The bulk is **generated/vendored**, not hand-written logic: the pnpm-lock delta for a new workspace app plus shadcn/ui primitives copied verbatim from the registry. Mirrors the original #2158, which also carried `size-override`. Splitting the scaffold further would fragment a single coherent app skeleton.

---

## [059c00e1] refactor(web): migrate A-class window.open sites to openExternal (#2128) (#2184)

- **SHA**: `059c00e14a14058a5ee46d063fe4926002504b21`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T10:34:32Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/059c00e14a14058a5ee46d063fe4926002504b21

### 完整 Commit Message

```
refactor(web): migrate A-class window.open sites to openExternal (#2128) (#2184)

Tracking: #2128 · Spec:
`docs/superpowers/specs/2026-05-30-window-open-wrapper.md` · Follows
#2132 (PR 0)

## What (PR 1 — A-class non-sensitive migration)

Migrate the 10 non-sensitive external-link / new-tab `window.open` sites
to the `openExternal` helper introduced in #2132:

| File | sites |
|---|---|
| `GuideTourModal.tsx` | 4 (agents-manager / chat / schedule / chat?q=…)
|
| `ExamplePromptGrid.tsx` | 2 (playback links) |
| `UploadsFeed.tsx` | 1 (non-image blob open) |
| `InviteCodeStep.tsx` | 1 (waitlist) |
| `MarkdownContent.tsx` | 1 (download fetch fallback) |
| `ArtifactPreview.tsx` | 1 (non-MM file open) |

All were `window.open(url, '_blank')` (InviteCodeStep: `'_blank',
'noopener'`). `openExternal` applies the secure
**`noopener,noreferrer`** default — the standardization agreed for this
rollout (severs `window.opener`, suppresses referrer; safe/beneficial
for these external + internal-route opens).

## Guard

`window.open` disable count **22 → 12**; the shrink-only guard
(`check-window-open-disables-shrink-only.sh`) enforces the decrease
(verified locally: `22 → 12 ✅`). ESLint `window.open` audit: 0
un-disabled calls in `src/`.

## Behavior / tests

No UX change beyond the agreed `noopener,noreferrer` standardization.
Call-site tests asserting the `window.open` arg list updated to include
the third arg:
- `GuideTourModal` — 5 spy assertions
- `UploadsFeed` — 3 blob-URL assertions (revoke-timing behavior
unchanged; only the open wrapper changed)
- `MarkdownContent` — 1 download-fallback assertion

Remaining raw sites (12, still disabled) ship in later PRs per the spec:
B sized popups, C OAuth (Composio / InvoiceHistory), billing
(SubscriptionPanel / PaywallContent).

## Verification
- Affected specs pass: GuideTourModal (34), UploadsFeed,
MarkdownContent-extras, ArtifactPreview-extras, window-open helper (7)
- `pnpm lint` clean; changed files tsc-clean (only pre-existing local
`motion/react` resolution noise, which CI resolves — see #2132)
- shrink-only guard: 22 → 12 PASS

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [6b5622b9] refactor(web): drive SubscriptionPanel via AnimatePresence (adds exit animation) (#2180)

- **SHA**: `6b5622b9c1fae2f37b9aa3233f238340a87f8aee`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T10:33:36Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6b5622b9c1fae2f37b9aa3233f238340a87f8aee

### 完整 Commit Message

```
refactor(web): drive SubscriptionPanel via AnimatePresence (adds exit animation) (#2180)

## What

`SubscriptionPanel` used the double-RAF→`setVisible(true)` entrance
anti-pattern, and the provider mounted it via `{isOpen &&
<SubscriptionPanelInner/>}` with **no exit animation** — closing
unmounted it instantly.

This lifts `<AnimatePresence>` to `SubscriptionPanelProvider` and
converts the backdrop + card to `motion.div` with
`initial`/`animate`/`exit`. Deletes the `useEffect`, the double-RAF, and
the `visible` state — and **adds a proper exit animation** (fade +
scale-down) the panel previously lacked.

> Per the agreed decision, this PR intentionally **adds an exit
animation** (a small behavior change), rather than preserving
entrance-only.

## Animation fidelity

| Layer | motion props | mirrors former |
|---|---|---|
| backdrop | opacity 0↔1, 200ms | `transition-opacity duration-200` |
| card | opacity + scale 0.96↔1, 250ms easeOut | `duration-[250ms]
ease-out` + `scale-[0.96]` |

## Unchanged
- `useBodyLock()` and `useEscapeKey(...)` stay (the Escape enabled flag
still suppresses while a nested payment/cancel modal is open).
- Inline styles use CSS vars (`--ecap-overlay-backdrop` /
`--ecap-shadow-dialog`), not hardcoded colors — kept as style props.

## Tests

Adds a `motion/react` passthrough mock so the panel renders under jsdom.
No existing assertion depended on the `visible` classes, so all **47**
existing cases pass unchanged.

## Scope / risk

Mechanism swap + intentional exit-animation addition. Only needs
`motion/react` (on main via #2125) — independent of the other open
animation PRs, lands in parallel.

Part of the zero-`useEffect` animation series. Remaining:
`WelcomeRewardToast`, `VerifyPage`.

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — SubscriptionPanel 47 pass; full suite green (1
unrelated pre-existing flaky `react-hooks-config` timeout under worker
load — passes in isolation, untouched here)
- ⚠️ Exit animation is a behavior change — needs a staging visual-check
of panel **close** (the new fade+scale-out)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

`SubscriptionPanel` used the double-RAF→`setVisible(true)` entrance anti-pattern, and the provider mounted it via `{isOpen && <SubscriptionPanelInner/>}` with **no exit animation** — closing unmounted it instantly.

This lifts `<AnimatePresence>` to `SubscriptionPanelProvider` and converts the backdrop + card to `motion.div` with `initial`/`animate`/`exit`. Deletes the `useEffect`, the double-RAF, and the `visible` state — and **adds a proper exit animation** (fade + scale-down) the panel previously lacked.

> Per the agreed decision, this PR intentionally **adds an exit animation** (a small behavior change), rather than preserving entrance-only.

## Animation fidelity

| Layer | motion props | mirrors former |
|---|---|---|
| backdrop | opacity 0↔1, 200ms | `transition-opacity duration-200` |
| card | opacity + scale 0.96↔1, 250ms easeOut | `duration-[250ms] ease-out` + `scale-[0.96]` |

## Unchanged
- `useBodyLock()` and `useEscapeKey(...)` stay (the Escape enabled flag still suppresses while a nested payment/cancel modal is open).
- Inline styles use CSS vars (`--ecap-overlay-backdrop` / `--ecap-shadow-dialog`), not hardcoded colors — kept as style props.

## Tests

Adds a `motion/react` passthrough mock so the panel renders under jsdom. No existing assertion depended on the `visible` classes, so all **47** existing cases pass unchanged.

## Scope / risk

Mechanism swap + intentional exit-animation addition. Only needs `motion/react` (on main via #2125) — independent of the other open animation PRs, lands in parallel.

Part of the zero-`useEffect` animation series. Remaining: `WelcomeRewardToast`, `VerifyPage`.

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — SubscriptionPanel 47 pass; full suite green (1 unrelated pre-existing flaky `react-hooks-config` timeout under worker load — passes in isolation, untouched here)
- ⚠️ Exit animation is a behavior change — needs a staging visual-check of panel **close** (the new fade+scale-out)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [8e3f66a5] refactor(web): drive ExamplePreviewModal via AnimatePresence + useBodyLock/useEscapeKey (#2179)

- **SHA**: `8e3f66a5c80ae75db92d3bfdc19b373248db0670`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T10:33:05Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8e3f66a5c80ae75db92d3bfdc19b373248db0670

### 完整 Commit Message

```
refactor(web): drive ExamplePreviewModal via AnimatePresence + useBodyLock/useEscapeKey (#2179)

## What

`ExamplePreviewModal`'s mount effect did **four** things; only two were
the `mount→RAF→setState` animation anti-pattern:

| # | Old | New |
|---|---|---|
| 1 | double-RAF → `isVisible` entrance | `<AnimatePresence>` |
| 2 | `setTimeout(400)` delayed unmount | `<AnimatePresence>` |
| 3 | `document.body.style.overflow` lock | `useBodyLock(isOpen)` |
| 4 | `window` keydown Escape listener | `useEscapeKey(onClose, isOpen)`
|

Deletes `useEffect`, both `useState`s (`isVisible` / `shouldRender`),
the double-RAF, and the `setTimeout`. Enter/exit is now declarative:
- backdrop: opacity 0↔1, 400ms
- card: opacity + `y(16→0)` + `scale(0.95→1)`, 400ms easeOut

(mirrors the former `translate-y-4/scale-95/opacity-0 ↔
translate-y-0/scale-100/opacity-100` `transition-all duration-400
ease-out`.)

## Side benefit — fixes a latent scroll-lock bug

The old cleanup ran `document.body.style.overflow = 'unset'`
**unconditionally**, so closing this modal would unlock scrolling even
if another modal were still open. `useBodyLock` is ref-counted (shared
module counter) and only unlocks when the last consumer releases —
matching how `SubscriptionPanel` / `ImagePreview` already use it.

## Notes
- The inline `boxShadow` (formerly toggled on `isVisible`) becomes a
static Tailwind arbitrary-value class — the card only exists while open,
and moving it out of a `style` prop also keeps it clear of the
hardcoded-rgba lint rule.
- `useEscapeKey` matches the convergence already done in #2116.

## Tests

Adds `ExamplePreviewModal.unit.spec.tsx` (none existed): open/close
mount, `null` previewData guard, unmount on close, close button, Escape
(open vs closed), and recreate→`onRecreate(query)`+`onClose` wiring.
`motion/react` mocked as passthrough so `AnimatePresence` unmounts
synchronously in jsdom.

## Scope / risk

Behaviour-preserving mechanism swap (plus the scroll-lock fix). Only
needs `motion/react` (already on main via #2125) — **independent of
#2171/#2173** (different files, no shared CSS), so it can land in
parallel.

Part of the zero-`useEffect` animation series. Remaining:
`SubscriptionPanel`, `WelcomeRewardToast`, `VerifyPage`.

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — ExamplePreviewModal 8 pass; full suite green (1
unrelated pre-existing flaky `react-hooks-config` timeout under worker
load — passes in isolation, touches no code here)
- ⚠️ Visual regression (fade/slide/scale in a real browser) not run
locally — needs a staging check on open/close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

`ExamplePreviewModal`'s mount effect did **four** things; only two were the `mount→RAF→setState` animation anti-pattern:

| # | Old | New |
|---|---|---|
| 1 | double-RAF → `isVisible` entrance | `<AnimatePresence>` |
| 2 | `setTimeout(400)` delayed unmount | `<AnimatePresence>` |
| 3 | `document.body.style.overflow` lock | `useBodyLock(isOpen)` |
| 4 | `window` keydown Escape listener | `useEscapeKey(onClose, isOpen)` |

Deletes `useEffect`, both `useState`s (`isVisible` / `shouldRender`), the double-RAF, and the `setTimeout`. Enter/exit is now declarative:
- backdrop: opacity 0↔1, 400ms
- card: opacity + `y(16→0)` + `scale(0.95→1)`, 400ms easeOut

(mirrors the former `translate-y-4/scale-95/opacity-0 ↔ translate-y-0/scale-100/opacity-100` `transition-all duration-400 ease-out`.)

## Side benefit — fixes a latent scroll-lock bug

The old cleanup ran `document.body.style.overflow = 'unset'` **unconditionally**, so closing this modal would unlock scrolling even if another modal were still open. `useBodyLock` is ref-counted (shared module counter) and only unlocks when the last consumer releases — matching how `SubscriptionPanel` / `ImagePreview` already use it.

## Notes
- The inline `boxShadow` (formerly toggled on `isVisible`) becomes a static Tailwind arbitrary-value class — the card only exists while open, and moving it out of a `style` prop also keeps it clear of the hardcoded-rgba lint rule.
- `useEscapeKey` matches the convergence already done in #2116.

## Tests

Adds `ExamplePreviewModal.unit.spec.tsx` (none existed): open/close mount, `null` previewData guard, unmount on close, close button, Escape (open vs closed), and recreate→`onRecreate(query)`+`onClose` wiring. `motion/react` mocked as passthrough so `AnimatePresence` unmounts synchronously in jsdom.

## Scope / risk

Behaviour-preserving mechanism swap (plus the scroll-lock fix). Only needs `motion/react` (already on main via #2125) — **independent of #2171/#2173** (different files, no shared CSS), so it can land in parallel.

Part of the zero-`useEffect` animation series. Remaining: `SubscriptionPanel`, `WelcomeRewardToast`, `VerifyPage`.

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — ExamplePreviewModal 8 pass; full suite green (1 unrelated pre-existing flaky `react-hooks-config` timeout under worker load — passes in isolation, touches no code here)
- ⚠️ Visual regression (fade/slide/scale in a real browser) not run locally — needs a staging check on open/close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [981fd5d6] refactor(web): replace GiftPaywallFab mount-flag effect with CSS @keyframes (#2173)

- **SHA**: `981fd5d6b7b20787a5e099413ad52bdae85ca459`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T10:31:44Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/981fd5d6b7b20787a5e099413ad52bdae85ca459

### 完整 Commit Message

```
refactor(web): replace GiftPaywallFab mount-flag effect with CSS @keyframes (#2173)

## What

`GiftPaywallFab` used the **mount→setTimeout→setState** anti-pattern to
fire its entrance animation: a `useEffect` ran `setTimeout(100)` to flip
a `mounted` flag, toggling `.gift-paywall-fab--mounted` so the CSS
transition would play after mount.

This replaces it with a **play-once CSS `@keyframes` entrance**,
deleting the `useEffect`, `setTimeout`, and `mounted` state entirely.

### Why no AnimatePresence (unlike #2171)
The FAB has **no exit animation** — it unmounts directly via the
`dismissed` guard (`return null`). So there's no delayed-unmount to
coordinate; pure CSS `@keyframes` is sufficient and lighter than motion
here.

## Animation fidelity (exact)

| Aspect | Before (transition + JS flag) | After (@keyframes) |
|---|---|---|
| transform | `scale(0)→scale(1)`, 500ms overshoot cubic-bezier |
`gift-fab-pop` 500ms, same bezier |
| opacity | `0→1`, 300ms ease | `gift-fab-fade` 300ms ease |
| delay | `setTimeout(100)` | `animation-delay: 100ms` |
| start/end states | initial `scale(0)/opacity(0)` + `--mounted`
`scale(1)/opacity(1)` | `animation-fill-mode: both` |

Two separate keyframes preserve the original **split timing** (transform
500ms vs opacity 300ms) that a single animation couldn't reproduce.

## Tests

Updated the Fab spec: the obsolete `vi.useFakeTimers` → "`--mounted`
after 100ms" test becomes a no-timer assertion that the FAB renders with
its entrance class and the JS-driven `--mounted` modifier is gone. (13
tests pass.)

## Scope / risk

Behaviour-preserving entrance-animation mechanism swap. No exit/unmount
change.

This is **PR 3** of the zero-`useEffect` animation series (after #2125
motion rename, #2171 GiftPaywallModal). Remaining B-class:
`SubscriptionPanel`, `ExamplePreviewModal`, `WelcomeRewardToast`,
`VerifyPage`.

## Verification

- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — Fab spec 13 pass; full suite green (1 unrelated
pre-existing flaky `react-hooks-config` timeout under worker load —
passes in isolation, touches no code here)
- ⚠️ Visual regression (the spring "pop" in a real browser) not run
locally — needs a staging check on the 🎁 FAB appearing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

`GiftPaywallFab` used the **mount→setTimeout→setState** anti-pattern to fire its entrance animation: a `useEffect` ran `setTimeout(100)` to flip a `mounted` flag, toggling `.gift-paywall-fab--mounted` so the CSS transition would play after mount.

This replaces it with a **play-once CSS `@keyframes` entrance**, deleting the `useEffect`, `setTimeout`, and `mounted` state entirely.

### Why no AnimatePresence (unlike #2171)
The FAB has **no exit animation** — it unmounts directly via the `dismissed` guard (`return null`). So there's no delayed-unmount to coordinate; pure CSS `@keyframes` is sufficient and lighter than motion here.

## Animation fidelity (exact)

| Aspect | Before (transition + JS flag) | After (@keyframes) |
|---|---|---|
| transform | `scale(0)→scale(1)`, 500ms overshoot cubic-bezier | `gift-fab-pop` 500ms, same bezier |
| opacity | `0→1`, 300ms ease | `gift-fab-fade` 300ms ease |
| delay | `setTimeout(100)` | `animation-delay: 100ms` |
| start/end states | initial `scale(0)/opacity(0)` + `--mounted` `scale(1)/opacity(1)` | `animation-fill-mode: both` |

Two separate keyframes preserve the original **split timing** (transform 500ms vs opacity 300ms) that a single animation couldn't reproduce.

## Tests

Updated the Fab spec: the obsolete `vi.useFakeTimers` → "`--mounted` after 100ms" test becomes a no-timer assertion that the FAB renders with its entrance class and the JS-driven `--mounted` modifier is gone. (13 tests pass.)

## Scope / risk

Behaviour-preserving entrance-animation mechanism swap. No exit/unmount change.

This is **PR 3** of the zero-`useEffect` animation series (after #2125 motion rename, #2171 GiftPaywallModal). Remaining B-class: `SubscriptionPanel`, `ExamplePreviewModal`, `WelcomeRewardToast`, `VerifyPage`.

## Verification

- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — Fab spec 13 pass; full suite green (1 unrelated pre-existing flaky `react-hooks-config` timeout under worker load — passes in isolation, touches no code here)
- ⚠️ Visual regression (the spring "pop" in a real browser) not run locally — needs a staging check on the 🎁 FAB appearing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [4c2c4907] refactor(web): drive Toast enter/exit via AnimatePresence (#2185)

- **SHA**: `4c2c4907c1b18312c876c7ce50ab4dba439a83f9`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T10:31:15Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4c2c4907c1b18312c876c7ce50ab4dba439a83f9

### 完整 Commit Message

```
refactor(web): drive Toast enter/exit via AnimatePresence (#2185)

## What

The `Toast` provider tracked a per-toast `visible` boolean purely to
drive animation: `false`→`requestAnimationFrame`→`true` for entrance,
and `true`→`false`→`setTimeout(200)`→remove-from-array for exit. Replace
with `<AnimatePresence>`:

- toast shape drops `visible` (now just `{id, message, type}`)
- `removeToast` filters the toast out immediately; AnimatePresence plays
the exit before unmounting (deletes the 200ms delayed-removal timer)
- entrance is declarative `motion` `initial`/`animate` (deletes the
`requestAnimationFrame` flip + the two `setToasts(...map visible...)`
passes)
- added `layout` so surviving toasts slide up smoothly when one is
removed

## Unchanged business logic (NOT animation)

- the **3s auto-dismiss** `setTimeout` + its `timersRef` map + the
unmount cleanup effect are real timers and stay
- **MAX_VISIBLE eviction** is preserved — the array slice happens
**inside** the `setToasts` updater (pure), while the evicted toast's
timer cleanup runs **outside** it (side effects must not live in a state
updater — per the project's setState-purity rule)

## Tests

Adds a `Toast` unit spec (none existed): show, 3s auto-dismiss,
close-button dismiss, MAX_VISIBLE eviction of the oldest, and the
`useToast`-outside-provider guard. `motion/react` mocked as passthrough
so exit unmounts synchronously.

## Scope / risk

Behaviour-preserving mechanism swap. Only needs `motion/react` (on main
via #2125) — independent of the other open animation PRs, lands in
parallel.

This completes the zero-`useEffect` animation series — `Toast` was the
last/most-tangled B-class item (`GiftPaywallModal` #2171,
`GiftPaywallFab` #2173, `ExamplePreviewModal` #2179, `SubscriptionPanel`
#2180, `WelcomeRewardToast` #2182, `VerifyPage` #2183, and this).

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — Toast 5 pass; **full suite green (458 files / 6766
tests, 0 failures)**
- ⚠️ Visual regression (slide-down + fade, and the new layout slide-up
on dismiss) not run locally — needs a staging check (trigger a few
toasts, dismiss the middle one)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

The `Toast` provider tracked a per-toast `visible` boolean purely to drive animation: `false`→`requestAnimationFrame`→`true` for entrance, and `true`→`false`→`setTimeout(200)`→remove-from-array for exit. Replace with `<AnimatePresence>`:

- toast shape drops `visible` (now just `{id, message, type}`)
- `removeToast` filters the toast out immediately; AnimatePresence plays the exit before unmounting (deletes the 200ms delayed-removal timer)
- entrance is declarative `motion` `initial`/`animate` (deletes the `requestAnimationFrame` flip + the two `setToasts(...map visible...)` passes)
- added `layout` so surviving toasts slide up smoothly when one is removed

## Unchanged business logic (NOT animation)

- the **3s auto-dismiss** `setTimeout` + its `timersRef` map + the unmount cleanup effect are real timers and stay
- **MAX_VISIBLE eviction** is preserved — the array slice happens **inside** the `setToasts` updater (pure), while the evicted toast's timer cleanup runs **outside** it (side effects must not live in a state updater — per the project's setState-purity rule)

## Tests

Adds a `Toast` unit spec (none existed): show, 3s auto-dismiss, close-button dismiss, MAX_VISIBLE eviction of the oldest, and the `useToast`-outside-provider guard. `motion/react` mocked as passthrough so exit unmounts synchronously.

## Scope / risk

Behaviour-preserving mechanism swap. Only needs `motion/react` (on main via #2125) — independent of the other open animation PRs, lands in parallel.

This completes the zero-`useEffect` animation series — `Toast` was the last/most-tangled B-class item (`GiftPaywallModal` #2171, `GiftPaywallFab` #2173, `ExamplePreviewModal` #2179, `SubscriptionPanel` #2180, `WelcomeRewardToast` #2182, `VerifyPage` #2183, and this).

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — Toast 5 pass; **full suite green (458 files / 6766 tests, 0 failures)**
- ⚠️ Visual regression (slide-down + fade, and the new layout slide-up on dismiss) not run locally — needs a staging check (trigger a few toasts, dismiss the middle one)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [bfd2c2e5] refactor(web): replace VerifyPage entrance effect with CSS @keyframes (#2183)

- **SHA**: `bfd2c2e51579b248626de5dc6d333f8c4b9e948f`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T10:30:50Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/bfd2c2e51579b248626de5dc6d333f8c4b9e948f

### 完整 Commit Message

```
refactor(web): replace VerifyPage entrance effect with CSS @keyframes (#2183)

## What

`VerifyPage` used the `mount→requestAnimationFrame→setIsVisible(true)`
pattern: `isVisible` threaded from the page through `VerifyShell` to
toggle Tailwind opacity/scale/translate classes on the backdrop + card.

Replace with pure CSS `@keyframes` (`login-verify-backdrop-in` /
`-card-in` in `login.css`) that play once on mount. Deletes the
`isVisible` state, the `requestAnimationFrame`, and the `isVisible` prop
on `VerifyShell` (+ its 5 call sites).

### Why CSS, not AnimatePresence
`VerifyPage` is a full-page route with no exit/unmount animation — so
pure CSS is the right tool (same as the FAB in #2173), not
`<AnimatePresence>`.

## Scroll-lock kept as an effect
The effect toggles `overflow-hidden` on **`documentElement`**
(`<html>`), which `useBodyLock` doesn't target (it locks `<body>`). So
it stays a dedicated effect — a legitimate DOM side effect, not the
animation anti-pattern.

## SSR/hydration-safe
The keyframes' `from` is the hidden state, which is also the
server-rendered first paint — the client animates from the same state it
hydrates into, so no flash and no `:root.client-ready` gate needed.

## Animation fidelity
- backdrop: opacity 0→1, 300ms
- card: opacity + scale(0.95→1) + translateY(−45%→−50%), 300ms ease-out,
holding the −50% X centering throughout (the keyframe owns the full
transform, since an animated `transform` overrides Tailwind translate
utilities)

## Tests
All 3 verify suites (email-otp / magic-link / phone, **9** tests) pass
unchanged — none depended on the `isVisible`/RAF mechanism.

## Scope / risk
Entrance-animation mechanism swap; scroll-lock behavior unchanged. No
new dependency (pure CSS).

This is the **final B-class item** in the zero-`useEffect` animation
series (#2125 rename → #2171 modal → #2173 fab → #2179 preview → #2180
panel → #2182 toast → this).

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — verify suites 9 pass; full suite green (1 unrelated
pre-existing flaky `react-hooks-config` timeout under worker load —
passes in isolation, untouched here)
- ⚠️ Visual regression (the verify card fade+scale-in on page load) not
run locally — needs a staging check; SSR-flash specifically worth
eyeballing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

`VerifyPage` used the `mount→requestAnimationFrame→setIsVisible(true)` pattern: `isVisible` threaded from the page through `VerifyShell` to toggle Tailwind opacity/scale/translate classes on the backdrop + card.

Replace with pure CSS `@keyframes` (`login-verify-backdrop-in` / `-card-in` in `login.css`) that play once on mount. Deletes the `isVisible` state, the `requestAnimationFrame`, and the `isVisible` prop on `VerifyShell` (+ its 5 call sites).

### Why CSS, not AnimatePresence
`VerifyPage` is a full-page route with no exit/unmount animation — so pure CSS is the right tool (same as the FAB in #2173), not `<AnimatePresence>`.

## Scroll-lock kept as an effect
The effect toggles `overflow-hidden` on **`documentElement`** (`<html>`), which `useBodyLock` doesn't target (it locks `<body>`). So it stays a dedicated effect — a legitimate DOM side effect, not the animation anti-pattern.

## SSR/hydration-safe
The keyframes' `from` is the hidden state, which is also the server-rendered first paint — the client animates from the same state it hydrates into, so no flash and no `:root.client-ready` gate needed.

## Animation fidelity
- backdrop: opacity 0→1, 300ms
- card: opacity + scale(0.95→1) + translateY(−45%→−50%), 300ms ease-out, holding the −50% X centering throughout (the keyframe owns the full transform, since an animated `transform` overrides Tailwind translate utilities)

## Tests
All 3 verify suites (email-otp / magic-link / phone, **9** tests) pass unchanged — none depended on the `isVisible`/RAF mechanism.

## Scope / risk
Entrance-animation mechanism swap; scroll-lock behavior unchanged. No new dependency (pure CSS).

This is the **final B-class item** in the zero-`useEffect` animation series (#2125 rename → #2171 modal → #2173 fab → #2179 preview → #2180 panel → #2182 toast → this).

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — verify suites 9 pass; full suite green (1 unrelated pre-existing flaky `react-hooks-config` timeout under worker load — passes in isolation, untouched here)
- ⚠️ Visual regression (the verify card fade+scale-in on page load) not run locally — needs a staging check; SSR-flash specifically worth eyeballing

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [7fe1af76] refactor(web): drive WelcomeRewardToast enter/exit via AnimatePresence (#2182)

- **SHA**: `7fe1af76295ed5fb1be5fbfcf0ef9f61fbccaf30`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T10:29:59Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7fe1af76295ed5fb1be5fbfcf0ef9f61fbccaf30

### 完整 Commit Message

```
refactor(web): drive WelcomeRewardToast enter/exit via AnimatePresence (#2182)

## What

`WelcomeRewardToast` used the `mount→RAF→setVisible` entrance +
`setVisible(false)`+`setTimeout(400)` delayed-unmount pattern (a
`shouldRender`/`visible` state pair). Collapse to a single `shown` flag
driven by `<AnimatePresence>` — entrance and exit play declaratively,
deleting the RAF and the 400ms unmount timer.

## Unchanged business logic (NOT animation)

Two effects stay exactly as-is — they decide *whether/when* to show, not
how it animates:
- onboarding-completion detection: sessionStorage flag +
`ecap:onboarding:complete` window event
- credits gating: `setTimeout(show, 1200)` once credits settle above the
threshold

`show()` now just flips `shown` instead of toggling `shouldRender` +
RAF.

## Animation fidelity

Mirrors the former inline transition: opacity 0↔1 + translateY −20px↔0
over 500ms ease-out (x stays −50% for the center transform).
`initial`/`animate`/`exit` on the `motion.div`.

## Tests

Adds a `motion/react` passthrough mock. All **7** existing cases
(credits gating ≤50/0/>50, fetch-wait, billing error, event trigger,
dismiss) pass unchanged.

## Scope / risk

Behaviour-preserving mechanism swap. Only needs `motion/react` (on main
via #2125) — independent of the other open animation PRs, lands in
parallel.

Part of the zero-`useEffect` animation series. Remaining: `VerifyPage`
(entrance-only; body-lock stays an effect).

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean (`--quiet`; the `as any` in the motion mock
matches the existing PaywallContent spec convention)
- `pnpm test:unit` — WelcomeRewardToast 7 pass; full suite green (1
unrelated pre-existing flaky `react-hooks-config` timeout under worker
load — passes in isolation, untouched here)
- ⚠️ Visual regression (slide-down + fade in a real browser) not run
locally — needs a staging check on the post-onboarding reward toast

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

`WelcomeRewardToast` used the `mount→RAF→setVisible` entrance + `setVisible(false)`+`setTimeout(400)` delayed-unmount pattern (a `shouldRender`/`visible` state pair). Collapse to a single `shown` flag driven by `<AnimatePresence>` — entrance and exit play declaratively, deleting the RAF and the 400ms unmount timer.

## Unchanged business logic (NOT animation)

Two effects stay exactly as-is — they decide *whether/when* to show, not how it animates:
- onboarding-completion detection: sessionStorage flag + `ecap:onboarding:complete` window event
- credits gating: `setTimeout(show, 1200)` once credits settle above the threshold

`show()` now just flips `shown` instead of toggling `shouldRender` + RAF.

## Animation fidelity

Mirrors the former inline transition: opacity 0↔1 + translateY −20px↔0 over 500ms ease-out (x stays −50% for the center transform). `initial`/`animate`/`exit` on the `motion.div`.

## Tests

Adds a `motion/react` passthrough mock. All **7** existing cases (credits gating ≤50/0/>50, fetch-wait, billing error, event trigger, dismiss) pass unchanged.

## Scope / risk

Behaviour-preserving mechanism swap. Only needs `motion/react` (on main via #2125) — independent of the other open animation PRs, lands in parallel.

Part of the zero-`useEffect` animation series. Remaining: `VerifyPage` (entrance-only; body-lock stays an effect).

## Verification
- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean (`--quiet`; the `as any` in the motion mock matches the existing PaywallContent spec convention)
- `pnpm test:unit` — WelcomeRewardToast 7 pass; full suite green (1 unrelated pre-existing flaky `react-hooks-config` timeout under worker load — passes in isolation, untouched here)
- ⚠️ Visual regression (slide-down + fade in a real browser) not run locally — needs a staging check on the post-onboarding reward toast

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [8331fe50] chore(web): rename version upgrade CTA from "Refresh now" to "Relaunch" (#2178)

- **SHA**: `8331fe5007519cddc284e492c63733c0d3469ed9`
- **作者**: lynn Zhuang
- **日期**: 2026-06-03T10:06:39Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8331fe5007519cddc284e492c63733c0d3469ed9

### 完整 Commit Message

```
chore(web): rename version upgrade CTA from "Refresh now" to "Relaunch" (#2178)

The widget action calls window.location.reload(), so "Relaunch"
describes what happens more accurately than "Refresh now". Updates en +
zh locales and the component's English fallbacks; i18n keys (refreshNow
/ refreshing) unchanged to limit blast radius.

<img width="1736" height="460" alt="image"
src="https://github.com/user-attachments/assets/edf4d869-d882-4070-ac6f-28672aa0c22e"
/>

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

The widget action calls window.location.reload(), so "Relaunch" describes what happens more accurately than "Refresh now". Updates en + zh locales and the component's English fallbacks; i18n keys (refreshNow / refreshing) unchanged to limit blast radius.

<img width="1736" height="460" alt="image" src="https://github.com/user-attachments/assets/edf4d869-d882-4070-ac6f-28672aa0c22e" />


---

## [e7d7e0b9] refactor(web): add window.open wrappers + no-restricted-syntax guard (#2128) (#2132)

- **SHA**: `e7d7e0b97f2e33ac706e4322a24cbd9d63256fdc`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T09:58:56Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e7d7e0b97f2e33ac706e4322a24cbd9d63256fdc

### 完整 Commit Message

```
refactor(web): add window.open wrappers + no-restricted-syntax guard (#2128) (#2132)

Tracking issue: #2128 · Spec:
`docs/superpowers/specs/2026-05-30-window-open-wrapper.md`

## What (PR 0 — infrastructure, zero behavior change)

Establishes the helpers + lint guard to consolidate the 25 raw
`window.open` call sites, following the #2072 lineage (funnel
browser-global side-effects through a helper + a shrink-only
`no-restricted-syntax` guard — same shape as the
`createObjectURL`→`useObjectUrl` guard in #2095).

**Existing call sites keep calling `window.open`** behind tracked
disable comments — the actual migration to the helpers happens in
follow-up PRs. The only runtime change is one `mailto:` site (see
below).

### Added
- **`src/lib/window-open.ts`** + unit tests (7):
- `openExternal(url, opts?)` — new tab, secure `noopener,noreferrer`
default; pass `{ features }` for sized popups (the helper then uses the
caller's features verbatim).
- `openBlankPopup()` — the Safari-safe `about:blank` →
navigate-after-await dance OAuth / hosted-invoice flows need; defensive
`opener = null`; `navigate()` returns `false` when blocked so the caller
owns the fallback (full-redirect vs. toast — they differ).
- **ESLint Rule 13** (`eslint.config.mjs`): bans native
`window.open(...)`, points at the wrappers. The wrapper file
self-exempts; 24 pre-existing sites carry inline `//
eslint-disable-next-line no-restricted-syntax -- window.open #2128`.
- **`web/scripts/check-window-open-disables-shrink-only.sh`**:
shrink-only counter. Uses a distinct `-- window.open #2128` tag so it
never cross-counts the cache-governance `-- TODO(#` counter;
bootstrap-skips until Rule 13 is on `main`. Wired into
`code-quality.yml` `pre_lint_scripts`.
- **Spec** doc.

### Changed (runtime)
- `verify/page.tsx`: the "open email app" `mailto:` button →
`openExternal`. This was the lone site whose inline JSX-children
position can't take a `//` disable; `noopener,noreferrer` is
behavior-neutral for `mailto:`.

## Migration plan (follow-up PRs, per spec)
PR 1 = A-class non-sensitive sites (GuideTourModal / ExamplePromptGrid /
UploadsFeed / InviteCodeStep / MarkdownContent / ArtifactPreview /
VersionUpgradeWidget — `noopener` standardization lands here, with
call-site test updates) · PR 2 = B sized popups · PR 3 = C OAuth
(Composio / InvoiceHistory) · PR 4 = billing (SubscriptionPanel /
PaywallContent). Each migration removes sites from the disable list; the
shrink-only guard enforces the count only ever decreases.

## Verification
- `pnpm test:unit …/window-open.unit.spec.ts` → 7 passed; verify-page
specs → 9 passed
- `pnpm lint` (src + tests + scripts) clean; full-repo `tsc --noEmit`
clean; `pnpm dup:src` under threshold
- ESLint audit: 0 un-disabled `window.open` in src
- shrink-only script: bootstrap-skips on this PR (Rule 13 not on main
yet), then enforces 24-and-shrinking

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [ab278882] fix(billing): remove legacy subscription cron writes (#2161)

- **SHA**: `ab2788826a2d45f70450af56f1970f7d3af05803`
- **作者**: kaka-srp
- **日期**: 2026-06-03T09:47:12Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/ab2788826a2d45f70450af56f1970f7d3af05803

### 完整 Commit Message

```
fix(billing): remove legacy subscription cron writes (#2161)

## Summary
- Disable legacy trial-expiry cron writes and keep the endpoint as a
no-op for stale scheduler calls.
- Route subscription sync to Billing v2 maintenance only.
- Add Billing v2 yearly credit reset based on current provider-backed
agreements, with entitlement leases, retry deferral, and idempotent
wallet balance setting.
- Fix Stripe Billing v2 period extraction so active subscriptions do not
keep stale trial dates.

## Root cause
Legacy cron jobs were still scanning and mutating legacy account
subscription fields after the Billing v2 cutover. That allowed stale
Stripe subscription state to activate or mutate users outside the v2
agreement/order/entitlement model. Yearly credit reset also still
depended on legacy account cron fields instead of v2 provider-backed
agreement state.

## Size override rationale
This PR is over the 2000-line size gate because it removes the legacy
subscription cron branches and replaces the old broad cron test file
with narrow v2/no-op tests. Splitting the change would leave either
stale legacy cron writes enabled or the new v2 yearly reset path
unverified.

## Test plan
- [x] `ruff check .`
- [x] `pyright app tests`
- [x] Relevant backend unit tests: `146 passed`
- [x] Full `pytest --cov=app --cov-report=term-missing
--cov-fail-under=90 -q` started after rebasing; interrupted per request
before completion. It had one unrelated OpenClaw test failure/error
while running.

Linear: https://linear.app/srpone/issue/ECA-882/billing-v2-cron-cleanup
```

### PR Body

## Summary
- Disable legacy trial-expiry cron writes and keep the endpoint as a no-op for stale scheduler calls.
- Route subscription sync to Billing v2 maintenance only.
- Add Billing v2 yearly credit reset based on current provider-backed agreements, with entitlement leases, retry deferral, and idempotent wallet balance setting.
- Fix Stripe Billing v2 period extraction so active subscriptions do not keep stale trial dates.

## Root cause
Legacy cron jobs were still scanning and mutating legacy account subscription fields after the Billing v2 cutover. That allowed stale Stripe subscription state to activate or mutate users outside the v2 agreement/order/entitlement model. Yearly credit reset also still depended on legacy account cron fields instead of v2 provider-backed agreement state.

## Size override rationale
This PR is over the 2000-line size gate because it removes the legacy subscription cron branches and replaces the old broad cron test file with narrow v2/no-op tests. Splitting the change would leave either stale legacy cron writes enabled or the new v2 yearly reset path unverified.

## Test plan
- [x] `ruff check .`
- [x] `pyright app tests`
- [x] Relevant backend unit tests: `146 passed`
- [x] Full `pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` started after rebasing; interrupted per request before completion. It had one unrelated OpenClaw test failure/error while running.

Linear: https://linear.app/srpone/issue/ECA-882/billing-v2-cron-cleanup

---

## [70e8732d] docs(claw-interface): add v2 openclaw read-flip design, plan, and bots-removal plan (#2175)

- **SHA**: `70e8732d9c872e5c8fe1f4e17a7e7023181d0ce7`
- **作者**: bill-srp
- **日期**: 2026-06-03T09:36:26Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/70e8732d9c872e5c8fe1f4e17a7e7023181d0ce7

### 完整 Commit Message

```
docs(claw-interface): add v2 openclaw read-flip design, plan, and bots-removal plan (#2175)

## Summary

Stack 1/3 — splits the oversized **#2157** ("flip OpenClaw runtime reads
to V2 computer store") into three coupling-safe,
independently-reviewable PRs. This first PR carries **only
documentation** (no code), so it merges with zero risk.

- `2026-06-02-v2-openclaw-read-flip` {design, plan} — the read-source
migration
- `2026-06-03-drop-account-openclaw-bots` {design, plan} — the follow-up
legacy-bots removal

### Stack (merge in order)
1. **#2175 — docs (this PR)** → `main`
2. **#2176 — dual-write/read core** → `split/1-docs`
3. **#2177 — read-flip consumers** → `split/2-dualwrite-core`

The three branches reproduce #2157 exactly: `git diff
feat/computer-agent split/3-read-consumers` is empty (lossless split).

## Test plan
- [x] Docs only — no code, no CI test impact
- [ ] CI green (pr-title-check + python-code-quality no-op on docs-only)
```

### PR Body

## Summary

Stack 1/3 — splits the oversized **#2157** ("flip OpenClaw runtime reads to V2 computer store") into three coupling-safe, independently-reviewable PRs. This first PR carries **only documentation** (no code), so it merges with zero risk.

- `2026-06-02-v2-openclaw-read-flip` {design, plan} — the read-source migration
- `2026-06-03-drop-account-openclaw-bots` {design, plan} — the follow-up legacy-bots removal

### Stack (merge in order)
1. **#2175 — docs (this PR)** → `main`
2. **#2176 — dual-write/read core** → `split/1-docs`
3. **#2177 — read-flip consumers** → `split/2-dualwrite-core`

The three branches reproduce #2157 exactly: `git diff feat/computer-agent split/3-read-consumers` is empty (lossless split).

## Test plan
- [x] Docs only — no code, no CI test impact
- [ ] CI green (pr-title-check + python-code-quality no-op on docs-only)

---

## [98d7dc71] chore(chat-ui): add shared chat package (#2167)

- **SHA**: `98d7dc71b413acb56454017cbc3cf8924d0bfd26`
- **作者**: bill-srp
- **日期**: 2026-06-03T09:01:25Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/98d7dc71b413acb56454017cbc3cf8924d0bfd26

### 完整 Commit Message

```
chore(chat-ui): add shared chat package (#2167)

## Linear
Not applicable: PR title is `chore`, not `feat`.

## Summary
- Add `@zooclaw/chat-ui` shared presentational chat components, types,
tests, and docs.
- Wire the enterprise app demo to consume the shared chat UI package.
- Add Tailwind source coverage for shared chat UI classes.

## Test plan
- [x] `pnpm --filter @zooclaw/chat-ui test`
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] `pnpm --filter @zooclaw/chat-ui tsc`

---------

Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: bill-srp <undefined@users.noreply.github.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Linear
Not applicable: PR title is `chore`, not `feat`.

## Summary
- Add `@zooclaw/chat-ui` shared presentational chat components, types, tests, and docs.
- Wire the enterprise app demo to consume the shared chat UI package.
- Add Tailwind source coverage for shared chat UI classes.

## Test plan
- [x] `pnpm --filter @zooclaw/chat-ui test`
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] `pnpm --filter @zooclaw/chat-ui tsc`


---

## [77047240] chore(web): add enterprise app scaffold (#2166)

- **SHA**: `7704724008611c68ea966ff72e71c7d7b94e1f45`
- **作者**: bill-srp
- **日期**: 2026-06-03T08:41:21Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7704724008611c68ea966ff72e71c7d7b94e1f45

### 完整 Commit Message

```
chore(web): add enterprise app scaffold (#2166)

## Linear
Not applicable: PR title is `chore`, not `feat`.

## Summary
- Add the initial `web/enterprise-app` Next.js scaffold.
- Register the app in the web workspace lockfile/package metadata.
- Include baseline Cloudflare/OpenNext config and public assets.

## Test plan
- [x] Verified as part of top stack checks on
`split/enterprise-app-auth`.

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Linear
Not applicable: PR title is `chore`, not `feat`.

## Summary
- Add the initial `web/enterprise-app` Next.js scaffold.
- Register the app in the web workspace lockfile/package metadata.
- Include baseline Cloudflare/OpenNext config and public assets.

## Test plan
- [x] Verified as part of top stack checks on `split/enterprise-app-auth`.


---

## [ef1447c0] refactor(web): drive GiftPaywallModal enter/exit via AnimatePresence (no useEffect) (#2171)

- **SHA**: `ef1447c06c69e9044c6d9daaad164578bc5c7a3b`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T08:34:39Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/ef1447c06c69e9044c6d9daaad164578bc5c7a3b

### 完整 Commit Message

```
refactor(web): drive GiftPaywallModal enter/exit via AnimatePresence (no useEffect) (#2171)

## What

`GiftPaywallModal` used the classic
**mount→requestAnimationFrame→setState→CSS-transition** anti-pattern to
animate open/close. This PR replaces it with `motion/react`'s
`<AnimatePresence>`, removing the `useEffect` entirely.

### Before
```tsx
const [isVisible, setIsVisible] = useState(false)
const [shouldRender, setShouldRender] = useState(false)
useEffect(() => {
  if (isOpen) {
    setShouldRender(true)
    requestAnimationFrame(() => setIsVisible(true))   // flip flag next frame → CSS transition
  } else {
    setIsVisible(false)
    const timer = setTimeout(() => setShouldRender(false), 300)  // delay unmount for exit anim
    return () => clearTimeout(timer)
  }
}, [isOpen])
```

### After
`<AnimatePresence>` owns enter/exit; mount/unmount is driven directly by
`isOpen`. `useEffect` / `setTimeout` / `requestAnimationFrame` /
`isVisible` / `shouldRender` all deleted.

## Animation fidelity (sibling-layer, faithful to the old CSS)

Per the agreed approach, backdrop and card are **independent motion
layers** (no single-overlay parent-opacity stacking):

| Layer | motion props | mirrors old CSS |
|---|---|---|
| backdrop | `opacity 0↔1`, 300ms easeInOut | `.paywall-modal-backdrop`
/ `--hidden` background transition |
| card | `opacity+scale {0,0.95}↔{1,1}`, 300ms easeOut | `.paywall-card`
/ `--hidden` |

The `--hidden` class variants + JS-driven transitions are removed from
`paywall.css` (motion owns enter/exit now); the static scrim/blur/card
box styles stay.

## Tests

Adds `GiftPaywallModal.unit.spec.tsx` (none existed before) — open/close
mount, backdrop self-click close, card-child click does **not** close, X
button, Escape (open vs closed). `motion/react` is mocked as a
passthrough so `AnimatePresence` unmounts children synchronously in
jsdom.

Also adds `aria-label="Close"` to the previously-unlabeled X button.

## Scope / risk

Behaviour-preserving animation mechanism swap. Depends on `motion/react`
(landed via #2125).

This is **PR 2** of the zero-`useEffect` animation series (audit + plan
tracked separately). Follow-ups: `GiftPaywallFab` own mount-flag,
`SubscriptionPanel`, `ExamplePreviewModal`, `WelcomeRewardToast`,
`VerifyPage`.

## Verification

- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — GiftPaywallModal 9 + GiftPaywallFab 12 = 21 pass;
full suite green (1 unrelated pre-existing flaky `react-hooks-config`
timeout under worker load — passes in isolation, touches no code in this
PR)
- ⚠️ Visual regression (fade/scale in a real browser) not run locally —
needs a staging check on open/close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

`GiftPaywallModal` used the classic **mount→requestAnimationFrame→setState→CSS-transition** anti-pattern to animate open/close. This PR replaces it with `motion/react`'s `<AnimatePresence>`, removing the `useEffect` entirely.

### Before
```tsx
const [isVisible, setIsVisible] = useState(false)
const [shouldRender, setShouldRender] = useState(false)
useEffect(() => {
  if (isOpen) {
    setShouldRender(true)
    requestAnimationFrame(() => setIsVisible(true))   // flip flag next frame → CSS transition
  } else {
    setIsVisible(false)
    const timer = setTimeout(() => setShouldRender(false), 300)  // delay unmount for exit anim
    return () => clearTimeout(timer)
  }
}, [isOpen])
```

### After
`<AnimatePresence>` owns enter/exit; mount/unmount is driven directly by `isOpen`. `useEffect` / `setTimeout` / `requestAnimationFrame` / `isVisible` / `shouldRender` all deleted.

## Animation fidelity (sibling-layer, faithful to the old CSS)

Per the agreed approach, backdrop and card are **independent motion layers** (no single-overlay parent-opacity stacking):

| Layer | motion props | mirrors old CSS |
|---|---|---|
| backdrop | `opacity 0↔1`, 300ms easeInOut | `.paywall-modal-backdrop` / `--hidden` background transition |
| card | `opacity+scale {0,0.95}↔{1,1}`, 300ms easeOut | `.paywall-card` / `--hidden` |

The `--hidden` class variants + JS-driven transitions are removed from `paywall.css` (motion owns enter/exit now); the static scrim/blur/card box styles stay.

## Tests

Adds `GiftPaywallModal.unit.spec.tsx` (none existed before) — open/close mount, backdrop self-click close, card-child click does **not** close, X button, Escape (open vs closed). `motion/react` is mocked as a passthrough so `AnimatePresence` unmounts children synchronously in jsdom.

Also adds `aria-label="Close"` to the previously-unlabeled X button.

## Scope / risk

Behaviour-preserving animation mechanism swap. Depends on `motion/react` (landed via #2125).

This is **PR 2** of the zero-`useEffect` animation series (audit + plan tracked separately). Follow-ups: `GiftPaywallFab` own mount-flag, `SubscriptionPanel`, `ExamplePreviewModal`, `WelcomeRewardToast`, `VerifyPage`.

## Verification

- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — GiftPaywallModal 9 + GiftPaywallFab 12 = 21 pass; full suite green (1 unrelated pre-existing flaky `react-hooks-config` timeout under worker load — passes in isolation, touches no code in this PR)
- ⚠️ Visual regression (fade/scale in a real browser) not run locally — needs a staging check on open/close

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [5bb7331b] refactor(web): derive pricing auth state at render time instead of via effect (#2131)

- **SHA**: `5bb7331b7e70d3984540b71ffa3dc5c2fc36899a`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T08:25:05Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/5bb7331b7e70d3984540b71ffa3dc5c2fc36899a

### 完整 Commit Message

```
refactor(web): derive pricing auth state at render time instead of via effect (#2131)

## What & why

Continues the `useEffect` anti-pattern cleanup (audit follow-up to
#2129), targeting the **A3 state-sync** category — effects whose only
job is to mirror reactive values into local state.

### `PublicPricingClient` — convert (the real change)
The component mirrored `isLoggedIn()` / `getPlanTier()` into
`isUserLoggedIn` / `currentPlan` via an effect keyed on the auth
snapshot:

```ts
const userInfoType = useAuthSnapshot((s) => s.userInfo.type)
const subscriptionCode = useAuthSnapshot((s) => s.subscriptionInfo?.subscription_code ?? null)
useEffect(() => {
  if (!isMounted) return
  setIsUserLoggedIn(isLoggedIn())
  setCurrentPlan(isLoggedIn() ? (getPlanTier() as PlanTier | null) : null)
}, [isMounted, userInfoType, subscriptionCode])
```

The snapshot's `userInfo` / `subscriptionInfo` **are the same objects**
`isLoggedIn()` / `getPlanTier()` read from storage
(`auth-snapshot-store.ts` builds the snapshot from `getUserInfo()` /
`getSubscriptionInfo()`), so the values can be read straight from the
reactive store and derived at render time:

```ts
const userInfo = useAuthSnapshot((s) => s.userInfo)
const subscriptionPlan = useAuthSnapshot((s) => s.subscriptionInfo?.plan ?? null)
const isUserLoggedIn = isMounted && userInfo.type === '1' && !!userInfo.access_token
const currentPlan: PlanTier | null = isUserLoggedIn ? (subscriptionPlan as PlanTier | null) : null
```

Equivalent and reactive (recomputes on every `notifyAuthChange()`),
drops the effect + 2 `useState` + an extra render pass. The `isMounted`
gate is preserved so SSR / first client render stay logged-out (no
hydration mismatch).

### `LoginCheckProvider` — documented, **not** changed
The adjacent auto-close effect was also A3-flagged, but its dep array
encodes *transition* detection ("close the modal when `type` flips to
`'1'`"). A render-time guard (`type === '1' && isModalOpen`) is **not**
equivalent — it force-closes on every render, so it would prevent the
modal from ever opening for an already-logged-in user (a unit test
caught exactly this). The faithful replacement is a longer prev-value
dance that's less clear than the 3-line effect, so it stays an effect on
purpose — now with a comment so a future audit doesn't re-flag it.

## Verification
- `tsc --noEmit`: changed files clean.
- `eslint`: clean.
- `LoginCheckProvider` unit tests: **17 pass** (the suite that caught
the bad first attempt).
- `PublicPricingClient` has no unit harness (large page); the change is
a provably-equivalent derivation, also covered by
`tests/e2e/specs/subscription-pricing.spec.ts`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What & why

Continues the `useEffect` anti-pattern cleanup (audit follow-up to #2129), targeting the **A3 state-sync** category — effects whose only job is to mirror reactive values into local state.

### `PublicPricingClient` — convert (the real change)
The component mirrored `isLoggedIn()` / `getPlanTier()` into `isUserLoggedIn` / `currentPlan` via an effect keyed on the auth snapshot:

```ts
const userInfoType = useAuthSnapshot((s) => s.userInfo.type)
const subscriptionCode = useAuthSnapshot((s) => s.subscriptionInfo?.subscription_code ?? null)
useEffect(() => {
  if (!isMounted) return
  setIsUserLoggedIn(isLoggedIn())
  setCurrentPlan(isLoggedIn() ? (getPlanTier() as PlanTier | null) : null)
}, [isMounted, userInfoType, subscriptionCode])
```

The snapshot's `userInfo` / `subscriptionInfo` **are the same objects** `isLoggedIn()` / `getPlanTier()` read from storage (`auth-snapshot-store.ts` builds the snapshot from `getUserInfo()` / `getSubscriptionInfo()`), so the values can be read straight from the reactive store and derived at render time:

```ts
const userInfo = useAuthSnapshot((s) => s.userInfo)
const subscriptionPlan = useAuthSnapshot((s) => s.subscriptionInfo?.plan ?? null)
const isUserLoggedIn = isMounted && userInfo.type === '1' && !!userInfo.access_token
const currentPlan: PlanTier | null = isUserLoggedIn ? (subscriptionPlan as PlanTier | null) : null
```

Equivalent and reactive (recomputes on every `notifyAuthChange()`), drops the effect + 2 `useState` + an extra render pass. The `isMounted` gate is preserved so SSR / first client render stay logged-out (no hydration mismatch).

### `LoginCheckProvider` — documented, **not** changed
The adjacent auto-close effect was also A3-flagged, but its dep array encodes *transition* detection ("close the modal when `type` flips to `'1'`"). A render-time guard (`type === '1' && isModalOpen`) is **not** equivalent — it force-closes on every render, so it would prevent the modal from ever opening for an already-logged-in user (a unit test caught exactly this). The faithful replacement is a longer prev-value dance that's less clear than the 3-line effect, so it stays an effect on purpose — now with a comment so a future audit doesn't re-flag it.

## Verification
- `tsc --noEmit`: changed files clean.
- `eslint`: clean.
- `LoginCheckProvider` unit tests: **17 pass** (the suite that caught the bad first attempt).
- `PublicPricingClient` has no unit harness (large page); the change is a provably-equivalent derivation, also covered by `tests/e2e/specs/subscription-pricing.spec.ts`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [b195f994] chore(web): rename framer-motion to motion/react (#2125)

- **SHA**: `b195f994ed384363eabee26c5c7cdc9a55c9ddef`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-03T08:17:15Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/b195f994ed384363eabee26c5c7cdc9a55c9ddef

### 完整 Commit Message

```
chore(web): rename framer-motion to motion/react (#2125)

## What

`framer-motion` was renamed to the **`motion`** package; the React entry
point is now **`motion/react`**. This PR:

- Swaps the dependency: `framer-motion@^12.40.0` → `motion@^12.40.0`
(same v12 codebase, drop-in rename)
- Updates all **9 import sites** (`from 'framer-motion'` → `from
'motion/react'`) across onboarding + paywall components
- Removes a stray `.claude/ralph-loop.local.md` (a Claude Code local
loop-state artifact accidentally committed in the first push) and
gitignores it so it can't recur

## Scope / risk

Pure rename, **no behaviour change**. Same library version, same API
surface — `motion`, `AnimatePresence`, `LayoutGroup`, `PanInfo` are all
re-exported from `motion/react`.

No vitest config change is needed: `motion/react` ships **both** ESM and
CJS export conditions (`require → ./dist/cjs/react.js`), so vitest's
node resolver loads it without a `server.deps.inline` entry. (An earlier
draft of this description mentioned an inline-deps change — that turned
out unnecessary and is not in the diff.)

`pnpm-lock.yaml` keeps `framer-motion` as a **transitive** dep of
`motion` (motion is a thin re-export wrapper) — expected, and there are
zero direct `framer-motion` references left in any `package.json`.

This is **PR 1** of a series that migrates
`setTimeout`/`requestAnimationFrame`-driven mount-animation `useEffect`s
to `<AnimatePresence>` (zero-`useEffect`). It unblocks those follow-ups.

## Verification

- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — 446 files / 6682 tests pass (1 pre-existing skip, 1
todo)
- CI: all 20 checks pass; both AI reviewers APPROVE on the corrected
commit

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

`framer-motion` was renamed to the **`motion`** package; the React entry point is now **`motion/react`**. This PR:

- Swaps the dependency: `framer-motion@^12.40.0` → `motion@^12.40.0` (same v12 codebase, drop-in rename)
- Updates all **9 import sites** (`from 'framer-motion'` → `from 'motion/react'`) across onboarding + paywall components
- Removes a stray `.claude/ralph-loop.local.md` (a Claude Code local loop-state artifact accidentally committed in the first push) and gitignores it so it can't recur

## Scope / risk

Pure rename, **no behaviour change**. Same library version, same API surface — `motion`, `AnimatePresence`, `LayoutGroup`, `PanInfo` are all re-exported from `motion/react`.

No vitest config change is needed: `motion/react` ships **both** ESM and CJS export conditions (`require → ./dist/cjs/react.js`), so vitest's node resolver loads it without a `server.deps.inline` entry. (An earlier draft of this description mentioned an inline-deps change — that turned out unnecessary and is not in the diff.)

`pnpm-lock.yaml` keeps `framer-motion` as a **transitive** dep of `motion` (motion is a thin re-export wrapper) — expected, and there are zero direct `framer-motion` references left in any `package.json`.

This is **PR 1** of a series that migrates `setTimeout`/`requestAnimationFrame`-driven mount-animation `useEffect`s to `<AnimatePresence>` (zero-`useEffect`). It unblocks those follow-ups.

## Verification

- `npx tsc --noEmit` — 0 errors
- `pnpm lint` — clean
- `pnpm test:unit` — 446 files / 6682 tests pass (1 pre-existing skip, 1 todo)
- CI: all 20 checks pass; both AI reviewers APPROVE on the corrected commit

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [3d1923b4] fix(auth-client): support Firebase token exchange (#2163)

- **SHA**: `3d1923b47d180a24fcf18f5155163c9d222da6a6`
- **作者**: bill-srp
- **日期**: 2026-06-03T07:48:08Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3d1923b47d180a24fcf18f5155163c9d222da6a6

### 完整 Commit Message

```
fix(auth-client): support Firebase token exchange (#2163)

## Linear
Not applicable: PR title is `fix`, not `feat`.

## Summary
- Add `AccountClient.exchangeFirebaseToken()` for account-service
`/auth/exchange`.
- Send Firebase ID tokens through the expected `fb-token` bearer header.
- Cover successful exchange and non-2xx error behavior in auth-client
tests.

## Test plan
- [x] `pnpm --filter @zooclaw/auth-client test`
- [x] `pnpm --filter @zooclaw/auth-client lint`
```

### PR Body

## Linear
Not applicable: PR title is `fix`, not `feat`.

## Summary
- Add `AccountClient.exchangeFirebaseToken()` for account-service `/auth/exchange`.
- Send Firebase ID tokens through the expected `fb-token` bearer header.
- Cover successful exchange and non-2xx error behavior in auth-client tests.

## Test plan
- [x] `pnpm --filter @zooclaw/auth-client test`
- [x] `pnpm --filter @zooclaw/auth-client lint`


---

## [6c8cb40f] perf(openclaw): reduce session list file io (#2160)

- **SHA**: `6c8cb40f75bd671792256bbf0e5bc6636a746e7b`
- **作者**: kaka-srp
- **日期**: 2026-06-03T07:44:39Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6c8cb40f75bd671792256bbf0e5bc6636a746e7b

### 完整 Commit Message

```
perf(openclaw): reduce session list file io (#2160)

## Linear
https://linear.app/srpone/issue/ECA-884/reduce-session-list-file-io

## Summary
- Disable automatic runtime session listing from subagent session
hydration and subscribe fallback paths.
- Stop conversation tasks GET from syncing runtime sessions; it now
reads the persisted Mongo task index only.
- Keep the runtime sessions route as a disabled compatibility endpoint
and cache archived session list/history reads.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] ruff check .
- [x] pyright app tests
- [x] pytest tests/unit/test_openclaw_conversation.py
tests/unit/test_openclaw_runtime_routes.py -q
- [ ] pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q
(interrupted at user request after unrelated openclaw_agents failures)
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-884/reduce-session-list-file-io

## Summary
- Disable automatic runtime session listing from subagent session hydration and subscribe fallback paths.
- Stop conversation tasks GET from syncing runtime sessions; it now reads the persisted Mongo task index only.
- Keep the runtime sessions route as a disabled compatibility endpoint and cache archived session list/history reads.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web run test:unit
- [x] ruff check .
- [x] pyright app tests
- [x] pytest tests/unit/test_openclaw_conversation.py tests/unit/test_openclaw_runtime_routes.py -q
- [ ] pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q (interrupted at user request after unrelated openclaw_agents failures)

---

## [2bca6fb8] fix: reduce claw-interface probe restarts (#2159)

- **SHA**: `2bca6fb882e09e91c999e43dac71fdbd576e8038`
- **作者**: kaka-srp
- **日期**: 2026-06-03T07:28:42Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/2bca6fb882e09e91c999e43dac71fdbd576e8038

### 完整 Commit Message

```
fix: reduce claw-interface probe restarts (#2159)

## Summary
- remove uvicorn --reload from the claw-interface container entrypoint
- increase liveness/readiness probe timeout from 1s to 5s while keeping
the existing / probe path

## Tests
- .venv/bin/pytest tests/unit/test_status.py
- .venv/bin/python -m ruff check app/routes/status.py
tests/unit/test_status.py
- kubectl kustomize kustomize/overlays/production
- git diff --check -- services/claw-interface/Dockerfile
services/claw-interface/kustomize/base/deployment.yaml

Note: full .venv/bin/pytest --cov=app --cov-report=term-missing -q was
started and then stopped at user request.
```

### PR Body

## Summary
- remove uvicorn --reload from the claw-interface container entrypoint
- increase liveness/readiness probe timeout from 1s to 5s while keeping the existing / probe path

## Tests
- .venv/bin/pytest tests/unit/test_status.py
- .venv/bin/python -m ruff check app/routes/status.py tests/unit/test_status.py
- kubectl kustomize kustomize/overlays/production
- git diff --check -- services/claw-interface/Dockerfile services/claw-interface/kustomize/base/deployment.yaml

Note: full .venv/bin/pytest --cov=app --cov-report=term-missing -q was started and then stopped at user request.

---

## [f48984d4] feat(web): polish Slack channel setup — configurable manifest, connection-ID collision avoidance, Add-Channel modal redesign (#2156)

- **SHA**: `f48984d4e81e108b2d49f7562149bf92621e1214`
- **作者**: vincent-srp
- **日期**: 2026-06-03T07:17:33Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/f48984d4e81e108b2d49f7562149bf92621e1214

### 完整 Commit Message

```
feat(web): polish Slack channel setup — configurable manifest, connection-ID collision avoidance, Add-Channel modal redesign (#2156)

## Linear

https://linear.app/srpone/issue/ECA-885/im-channel-setup-polish-configurable-slack-manifest-connection-id

## Summary
Polish of the **Settings → IM Channels** Slack connection flow.

- **Configurable Slack manifest** — new pure builder
`web/app/src/lib/openclaw/slack-manifest.ts`. App name + short
description are user-editable in the wizard with a live, copyable
manifest preview. `display_information.name` and `bot_user.display_name`
both mirror the app-name input **verbatim** (truncated to Slack's
35-char limit — no slug transform). Manifest content follows OpenClaw
"Group A′" best practices (assistant `suggested_prompts`,
`emoji`/`groups`/`usergroups` read scopes, `assistant_thread_*` events;
no Home tab, no slash command).
- **Connection-ID (accountId) collision avoidance** —
`computeDefaultAccountId({ platform, channels })` proposes a
non-colliding, **platform-named** default (`slack`, `slack-2`, …) per
the `(channel, accountId)` unique key, scoped per platform.
`computeDefaultSlackAppName` likewise avoids collisions with existing
channels.
- **AddChannelModal UX redesign** — guided vs. manual setup as
**parallel accordion method cards** (manual is no longer a subordinate
link); top-right `×` close; shared fields (Platform, Connection ID with
a field-accurate hint, Agent, DM/Group policy each with a one-line
per-option meaning); meaningful, non-redundant icons; setup-duration
shown as a **stopwatch badge on the CTA**; CTA copy "按指引接通 / Connect
with guidance".
- **i18n** — ~13 `clawSettings.channels` keys added/updated across all
10 locales (en, zh, ja, ko, fr, de, it, es, pt, ar).
- **Docs** — design spec + implementation plan reconciled with
as-shipped state (spec §13 "As-shipped reconciliation").

## Test plan
- [x] `pnpm tsc` — clean
- [x] `pnpm test:unit` — 453 files / 6750 tests pass (incl. new
`slack-manifest` + `helpers` specs, updated `ChannelsSection` /
`SlackSetupWizard` / locale-parity specs)
- [x] `pnpm lint` — clean
- [x] `pnpm lint:imports` — clean (no `src/lib` → `src/app`)
- [ ] Manual: add a Slack channel via the redesigned modal — edit app
name/description, confirm live manifest preview + copy, confirm default
Connection ID skips existing collisions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-885/im-channel-setup-polish-configurable-slack-manifest-connection-id

## Summary
Polish of the **Settings → IM Channels** Slack connection flow.

- **Configurable Slack manifest** — new pure builder `web/app/src/lib/openclaw/slack-manifest.ts`. App name + short description are user-editable in the wizard with a live, copyable manifest preview. `display_information.name` and `bot_user.display_name` both mirror the app-name input **verbatim** (truncated to Slack's 35-char limit — no slug transform). Manifest content follows OpenClaw "Group A′" best practices (assistant `suggested_prompts`, `emoji`/`groups`/`usergroups` read scopes, `assistant_thread_*` events; no Home tab, no slash command).
- **Connection-ID (accountId) collision avoidance** — `computeDefaultAccountId({ platform, channels })` proposes a non-colliding, **platform-named** default (`slack`, `slack-2`, …) per the `(channel, accountId)` unique key, scoped per platform. `computeDefaultSlackAppName` likewise avoids collisions with existing channels.
- **AddChannelModal UX redesign** — guided vs. manual setup as **parallel accordion method cards** (manual is no longer a subordinate link); top-right `×` close; shared fields (Platform, Connection ID with a field-accurate hint, Agent, DM/Group policy each with a one-line per-option meaning); meaningful, non-redundant icons; setup-duration shown as a **stopwatch badge on the CTA**; CTA copy "按指引接通 / Connect with guidance".
- **i18n** — ~13 `clawSettings.channels` keys added/updated across all 10 locales (en, zh, ja, ko, fr, de, it, es, pt, ar).
- **Docs** — design spec + implementation plan reconciled with as-shipped state (spec §13 "As-shipped reconciliation").

## Test plan
- [x] `pnpm tsc` — clean
- [x] `pnpm test:unit` — 453 files / 6750 tests pass (incl. new `slack-manifest` + `helpers` specs, updated `ChannelsSection` / `SlackSetupWizard` / locale-parity specs)
- [x] `pnpm lint` — clean
- [x] `pnpm lint:imports` — clean (no `src/lib` → `src/app`)
- [ ] Manual: add a Slack channel via the redesigned modal — edit app name/description, confirm live manifest preview + copy, confirm default Connection ID skips existing collisions

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## [d4b5eefa] feat(openclaw): create Mattermost session channels (#2155)

- **SHA**: `d4b5eefaf8285248ac19db668bfc74ba02bb4dbb`
- **作者**: bill-srp
- **日期**: 2026-06-03T02:59:13Z
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d4b5eefaf8285248ac19db668bfc74ba02bb4dbb

### 完整 Commit Message

```
feat(openclaw): create Mattermost session channels (#2155)

## Linear

https://linear.app/srpone/issue/ECA-881/create-mattermost-channel-per-openclaw-chat-session

## Summary
- Add `ecap-openclaw-session-channels` Mongo mapping for OpenClaw
session id, uid, computer id, agent id, Mattermost channel id, title,
and status.
- Add backend service to create a fresh Mattermost private channel per
OpenClaw chat session, add the human Mattermost user and selected agent
bot, remove the service/admin creator member, and persist the mapping.
- Add best-effort cleanup for Mattermost channels created before
downstream membership/creator/DB persistence failures, preserving the
original error while logging cleanup failures.
- Add Mattermost client support for private channel creation,
current-user lookup, member removal, and channel deletion.
- Expose backend APIs: `POST /openclaw/conversation/sessions` and `GET
/openclaw/conversation/sessions`.
- Add `MATTERMOST_TEAM_ID` setting plus startup index creation for the
session-channel collection.

Scope explicitly excludes Next.js BFF and chat UI wiring.

## Test plan
- [x] `.venv/bin/ruff check .`
- [x] `.venv/bin/python -m pytest
tests/unit/test_openclaw_session_channel_repo.py
tests/unit/test_mattermost_client.py
tests/unit/test_openclaw_session_channel_service.py
tests/unit/test_openclaw_conversation.py tests/unit/test_lifetime.py -v`
— 79 passed
- [x] `.venv/bin/python -m pytest --cov=app --cov-report=term-missing
--cov-fail-under=90 -q` — 4456 passed, 377 skipped, but repo-wide
coverage gate failed at 88.53% vs 90%
- [ ] CI `python-code-quality / build-and-test` green
- [ ] Manual: `POST /openclaw/conversation/sessions` for a
provisioned-agent user creates a Mattermost private channel with human +
bot user only, no service/admin member
- [ ] Manual: `GET /openclaw/conversation/sessions?agent_id=main` lists
prior sessions in descending recency

---------

Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: bill-srp <undefined@users.noreply.github.com>
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-881/create-mattermost-channel-per-openclaw-chat-session

## Summary
- Add `ecap-openclaw-session-channels` Mongo mapping for OpenClaw session id, uid, computer id, agent id, Mattermost channel id, title, and status.
- Add backend service to create a fresh Mattermost private channel per OpenClaw chat session, add the human Mattermost user and selected agent bot, remove the service/admin creator member, and persist the mapping.
- Add best-effort cleanup for Mattermost channels created before downstream membership/creator/DB persistence failures, preserving the original error while logging cleanup failures.
- Add Mattermost client support for private channel creation, current-user lookup, member removal, and channel deletion.
- Expose backend APIs: `POST /openclaw/conversation/sessions` and `GET /openclaw/conversation/sessions`.
- Add `MATTERMOST_TEAM_ID` setting plus startup index creation for the session-channel collection.

Scope explicitly excludes Next.js BFF and chat UI wiring.

## Test plan
- [x] `.venv/bin/ruff check .`
- [x] `.venv/bin/python -m pytest tests/unit/test_openclaw_session_channel_repo.py tests/unit/test_mattermost_client.py tests/unit/test_openclaw_session_channel_service.py tests/unit/test_openclaw_conversation.py tests/unit/test_lifetime.py -v` — 79 passed
- [x] `.venv/bin/python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` — 4456 passed, 377 skipped, but repo-wide coverage gate failed at 88.53% vs 90%
- [ ] CI `python-code-quality / build-and-test` green
- [ ] Manual: `POST /openclaw/conversation/sessions` for a provisioned-agent user creates a Mattermost private channel with human + bot user only, no service/admin member
- [ ] Manual: `GET /openclaw/conversation/sessions?agent_id=main` lists prior sessions in descending recency

---

