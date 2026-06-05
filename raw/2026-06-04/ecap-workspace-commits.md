# SerendipityOneInc/ecap-workspace - Commits on 2026-06-04

## 1. feat(vertical-pack-plans): add internal CRUD API (#2219)

- **SHA**: `9440881e41c0864539169f69c446d6cc2dd30861`
- **Author**: bill-srp
- **Date**: 2026-06-04T16:45:13Z
- **Files Changed**: 13
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9440881e41c0864539169f69c446d6cc2dd30861
- **PR**: #2219

### Full Commit Message

```
feat(vertical-pack-plans): add internal CRUD API (#2219)

## Linear

https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary
- Add `VerticalPackPlan` schemas for plan/add-on pricing, billing
cycles, publish state, and soft deletion.
- Add a Mongo-backed vertical pack plan repository with indexes,
Decimal-safe persistence, update guards, and soft-delete filtering.
- Expose SRP-gated internal CRUD routes under
`/internal/vertical-pack-plans`.
- Document the implementation plan and design notes for the vertical
pack plans backend slice.

## Test plan
- [x] `ruff check .`
- [x] `pyright app tests`
- [x] Focused vertical-pack-plan unit tests
- [ ] Full backend coverage gate attempted locally; the devcontainer run
completed with existing unrelated failures in `test_ci_lint_deptry`,
`test_pagerduty_client`, and OpenClaw resource-warning setup paths, plus
local total coverage `88.42%` below the `90%` gate. The
vertical-pack-plan tests passed within that run.

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-886/agent-pack-admin-dashboard-webdashboard

## Summary
- Add `VerticalPackPlan` schemas for plan/add-on pricing, billing cycles, publish state, and soft deletion.
- Add a Mongo-backed vertical pack plan repository with indexes, Decimal-safe persistence, update guards, and soft-delete filtering.
- Expose SRP-gated internal CRUD routes under `/internal/vertical-pack-plans`.
- Document the implementation plan and design notes for the vertical pack plans backend slice.

## Test plan
- [x] `ruff check .`
- [x] `pyright app tests`
- [x] Focused vertical-pack-plan unit tests
- [ ] Full backend coverage gate attempted locally; the devcontainer run completed with existing unrelated failures in `test_ci_lint_deptry`, `test_pagerduty_client`, and OpenClaw resource-warning setup paths, plus local total coverage `88.42%` below the `90%` gate. The vertical-pack-plan tests passed within that run.


---

## 2. feat(claw-interface): make OpenClaw sessions Mattermost threads in a per-agent channel (#2218)

- **SHA**: `7d2aee6b7464abe17a1be641a01e0de0e18da1ca`
- **Author**: bill-srp
- **Date**: 2026-06-04T13:38:58Z
- **Files Changed**: 15
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7d2aee6b7464abe17a1be641a01e0de0e18da1ca
- **PR**: #2218

### Full Commit Message

```
feat(claw-interface): make OpenClaw sessions Mattermost threads in a per-agent channel (#2218)

## Linear

https://linear.app/srpone/issue/ECA-896/openclaw-session-threads-per-agent-channel-root-post-id

## Summary
Migrate OpenClaw chat sessions from "one private Mattermost channel per
session" to **one reusable per-agent channel with a thread (root post)
per session**. Backend-only (`services/claw-interface`); ships
independently of `web/`.

- `root_post_id` added to `OpenClawSessionChannelRecord` /
`OpenClawSessionChannelResponse`.
- `session_channel_id` added to `AgentMattermostRuntime` — the dedicated
per-agent channel, created lazily on first session and persisted back
via `agent_workspace_repo.update_fields`.
- `Account.resolve_mattermost_user_token()` (schema-level, so the
service can author the seed post as the user).
- Mattermost client: `get_channel_by_name` (create-race adoption) +
`delete_post` (orphan-post cleanup).
- Repo index migration: drop unique `mm_channel_id` → **sparse-unique**
`root_post_id`; `ensure_indexes` drop is idempotent.
- `create_session_channel` now resolves/creates the per-agent channel
(`_ensure_agent_channel`, deterministic `zc-a-{sha1}` name, race-safe),
posts a **user→bot→admin**-authored seed root post, and stores
`{mm_channel_id=channel, root_post_id}`. On DB-insert failure it deletes
the orphan **post** (never the shared channel) and re-raises.

The first commit is a precursor typed-repo refactor (extract the
session-channel schema into its own module; repo accepts/returns
`OpenClawSessionChannelRecord` instead of `dict`).

**Backward compatible:** legacy per-session-channel records read
unchanged (`root_post_id=None`); the index drop is guarded for
fresh/already-migrated DBs.

**Out of scope (follow-up):** the frontend/agent reply path must post
conversation messages with `root_id = root_post_id` so they land in the
thread (lives in `web/` + the bot runtime).

**Deploy note:** `ensure_indexes` drops `unique_mm_channel_id` at
startup on first deploy — safe (legacy rows have distinct channels; the
sparse index excludes rows without `root_post_id`), but it is the one
change that touches an existing prod index.

## Split note
This PR is the **backend half** of the original combined branch. The
frontend sidebar restructure + "New Chat" entry was split into **#2216**
(`feat/openclaw-session-threads`), now frontend-only. The two ship
independently; this backend PR carries no `web/` changes.

## Test plan
- [ ] CI `python-code-quality / build-and-test` green (ruff + pyright +
pytest)
- [ ] Local verified: 98 unit tests across the touched files pass;
pyright 0 errors; ruff clean; import-linter 8/8 contracts kept
- [ ] New session creates-or-reuses the per-agent channel and persists
`session_channel_id` on the workspace (no extra MM call on reuse)
- [ ] Session record carries `(mm_channel_id, root_post_id)`; the seed
root post appears in the channel
- [ ] Legacy per-session-channel records still list/read without error

---------

Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-896/openclaw-session-threads-per-agent-channel-root-post-id

## Summary
Migrate OpenClaw chat sessions from "one private Mattermost channel per session" to **one reusable per-agent channel with a thread (root post) per session**. Backend-only (`services/claw-interface`); ships independently of `web/`.

- `root_post_id` added to `OpenClawSessionChannelRecord` / `OpenClawSessionChannelResponse`.
- `session_channel_id` added to `AgentMattermostRuntime` — the dedicated per-agent channel, created lazily on first session and persisted back via `agent_workspace_repo.update_fields`.
- `Account.resolve_mattermost_user_token()` (schema-level, so the service can author the seed post as the user).
- Mattermost client: `get_channel_by_name` (create-race adoption) + `delete_post` (orphan-post cleanup).
- Repo index migration: drop unique `mm_channel_id` → **sparse-unique** `root_post_id`; `ensure_indexes` drop is idempotent.
- `create_session_channel` now resolves/creates the per-agent channel (`_ensure_agent_channel`, deterministic `zc-a-{sha1}` name, race-safe), posts a **user→bot→admin**-authored seed root post, and stores `{mm_channel_id=channel, root_post_id}`. On DB-insert failure it deletes the orphan **post** (never the shared channel) and re-raises.

The first commit is a precursor typed-repo refactor (extract the session-channel schema into its own module; repo accepts/returns `OpenClawSessionChannelRecord` instead of `dict`).

**Backward compatible:** legacy per-session-channel records read unchanged (`root_post_id=None`); the index drop is guarded for fresh/already-migrated DBs.

**Out of scope (follow-up):** the frontend/agent reply path must post conversation messages with `root_id = root_post_id` so they land in the thread (lives in `web/` + the bot runtime).

**Deploy note:** `ensure_indexes` drops `unique_mm_channel_id` at startup on first deploy — safe (legacy rows have distinct channels; the sparse index excludes rows without `root_post_id`), but it is the one change that touches an existing prod index.

## Split note
This PR is the **backend half** of the original combined branch. The frontend sidebar restructure + "New Chat" entry was split into **#2216** (`feat/openclaw-session-threads`), now frontend-only. The two ship independently; this backend PR carries no `web/` changes.

## Test plan
- [ ] CI `python-code-quality / build-and-test` green (ruff + pyright + pytest)
- [ ] Local verified: 98 unit tests across the touched files pass; pyright 0 errors; ruff clean; import-linter 8/8 contracts kept
- [ ] New session creates-or-reuses the per-agent channel and persists `session_channel_id` on the workspace (no extra MM call on reuse)
- [ ] Session record carries `(mm_channel_id, root_post_id)`; the seed root post appears in the channel
- [ ] Legacy per-session-channel records still list/read without error


---

## 3. feat(dashboard-console): real R2 upload for avatars and pack archives (#2217)

- **SHA**: `cbd3fbb9fdab69ba5dcce340df898ef53870e87f`
- **Author**: bill-srp
- **Date**: 2026-06-04T13:38:17Z
- **Files Changed**: 12
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/cbd3fbb9fdab69ba5dcce340df898ef53870e87f
- **PR**: #2217

### Full Commit Message

```
feat(dashboard-console): real R2 upload for avatars and pack archives (#2217)

## Linear
https://linear.app/srpone/issue/ECA-886

## Summary

Replace the mock avatar/pack-archive uploader with a real R2 upload path
(ECA-886 infrastructure). Mirrors enterprise-admin's `/api/r2/upload`,
adapted for React Router + the dashboard-console worker's network
constraints.

**Worker / R2 (`wrangler.jsonc`)**
- Bind `R2_PUBLIC_BUCKET`→`gem-image` (avatars) and
`R2_AGENT_PACKS_BUCKET`→`zooclaw-agent-packs` (pack archives) +
`R2_PUBLIC_DOMAIN`, in both the top-level (prod) and `env.staging`
blocks. Verified the bindings land in the build-generated
`build/server/wrangler.json`.

**Upload lib (`app/lib/r2/`)**
- Ported `key` (purpose→key) + `index` (`uploadToR2`, purpose→bucket
routing), refactored to take the Worker `env` as a parameter instead of
opennext's `getCloudflareContext()`.

**Resource route (`app/routes/api/r2-upload.ts`, registered in
`routes.ts`)**
- Headless POST `/api/r2/upload`, outside the auth-gate shell. Validates
the bearer token against the **public account service** (this worker
can't reach the internal claw-interface — that's why agent-packs are
fetched browser-side) and gates to `@srp.one`, then enforces the same
size/type/metadata rules as enterprise-admin (logo ≤2 MB
png/jpg/webp/svg; archive ≤100 MB `.zip` + `org_id`/`pack_id`).

**Client + wiring**
- `uploadFileToR2` now POSTs to the route (drops the mock);
`getAccountUser(token)` added for server-side token→account resolution.
- `use-view-model`: **live** writes do the real upload (archives now
send `org_id`/`pack_id` metadata); **seed/demo** stays offline (local
`objectURL` / synthetic key) so the no-backend demo still works.

`LIVE_WRITES_ENABLED` stays **off** — this lands the infrastructure
dormant; flipping it is the separate go-live switch.

## Test plan
- [x] Unit (+21 tests, 91 total): `lib/r2/key`, `lib/r2/index` (bucket
routing + public_url), the resource route
(401/403/size/type/metadata/happy paths), and the client (`POST` shape +
error propagation)
- [x] `pnpm run lint` + `pnpm run typecheck` clean
- [x] `react-router build` succeeds; generated
`build/server/wrangler.json` carries the R2 bindings +
`R2_PUBLIC_DOMAIN`
- [ ] Live upload exercised end-to-end once `LIVE_WRITES_ENABLED` flips
and the buckets are confirmed in the deploy account

## Notes
- The deploy worker needs the `gem-image` / `zooclaw-agent-packs`
buckets in the Cloudflare account — enterprise-admin already binds the
same names.
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-886

## Summary

Replace the mock avatar/pack-archive uploader with a real R2 upload path (ECA-886 infrastructure). Mirrors enterprise-admin's `/api/r2/upload`, adapted for React Router + the dashboard-console worker's network constraints.

**Worker / R2 (`wrangler.jsonc`)**
- Bind `R2_PUBLIC_BUCKET`→`gem-image` (avatars) and `R2_AGENT_PACKS_BUCKET`→`zooclaw-agent-packs` (pack archives) + `R2_PUBLIC_DOMAIN`, in both the top-level (prod) and `env.staging` blocks. Verified the bindings land in the build-generated `build/server/wrangler.json`.

**Upload lib (`app/lib/r2/`)**
- Ported `key` (purpose→key) + `index` (`uploadToR2`, purpose→bucket routing), refactored to take the Worker `env` as a parameter instead of opennext's `getCloudflareContext()`.

**Resource route (`app/routes/api/r2-upload.ts`, registered in `routes.ts`)**
- Headless POST `/api/r2/upload`, outside the auth-gate shell. Validates the bearer token against the **public account service** (this worker can't reach the internal claw-interface — that's why agent-packs are fetched browser-side) and gates to `@srp.one`, then enforces the same size/type/metadata rules as enterprise-admin (logo ≤2 MB png/jpg/webp/svg; archive ≤100 MB `.zip` + `org_id`/`pack_id`).

**Client + wiring**
- `uploadFileToR2` now POSTs to the route (drops the mock); `getAccountUser(token)` added for server-side token→account resolution.
- `use-view-model`: **live** writes do the real upload (archives now send `org_id`/`pack_id` metadata); **seed/demo** stays offline (local `objectURL` / synthetic key) so the no-backend demo still works.

`LIVE_WRITES_ENABLED` stays **off** — this lands the infrastructure dormant; flipping it is the separate go-live switch.

## Test plan
- [x] Unit (+21 tests, 91 total): `lib/r2/key`, `lib/r2/index` (bucket routing + public_url), the resource route (401/403/size/type/metadata/happy paths), and the client (`POST` shape + error propagation)
- [x] `pnpm run lint` + `pnpm run typecheck` clean
- [x] `react-router build` succeeds; generated `build/server/wrangler.json` carries the R2 bindings + `R2_PUBLIC_DOMAIN`
- [ ] Live upload exercised end-to-end once `LIVE_WRITES_ENABLED` flips and the buckets are confirmed in the deploy account

## Notes
- The deploy worker needs the `gem-image` / `zooclaw-agent-packs` buckets in the Cloudflare account — enterprise-admin already binds the same names.


---

## 4. ci(dashboard-console): add deploy workflow and eslint code-quality gate (#2215)

- **SHA**: `004fb739edcc4c39b19ac65b5f0bd5b8572e2a5e`
- **Author**: bill-srp
- **Date**: 2026-06-04T12:35:11Z
- **Files Changed**: 6
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/004fb739edcc4c39b19ac65b5f0bd5b8572e2a5e
- **PR**: #2215

### Full Commit Message

```
ci(dashboard-console): add deploy workflow and eslint code-quality gate (#2215)

## Summary

Bring dashboard-console's CI/infra to parity with the other web apps —
two `ci` commits:

**1. Cloudflare Workers deploy workflow**
(`deploy-dashboard-console.yml` + `wrangler.jsonc`)
- Modeled on `deploy-enterprise-admin.yml`: merge to `main` → staging;
tag `dashboard-console-v*-release` → production (`-beta` → staging);
manual `workflow_dispatch`.
- React Router 7 + `@cloudflare/vite-plugin` specifics:
**per-environment build** (Vite inlines `VITE_*` at build time,
`CLOUDFLARE_ENV` selects the wrangler env), then deploy the
plugin-generated `build/server/wrangler.json` (the source
`wrangler.jsonc` `main` is a Vite-only virtual module wrangler can't
bundle).
- Workers: `zooclaw-dashboard-console` /
`zooclaw-dashboard-console-staging`; `workers.dev` routing for now
(custom-domain TODO marked in `wrangler.jsonc`).
- **Reuses existing repo GitHub vars** mapped to `VITE_*` — no new vars:
`NEXT_PUBLIC_ACCOUNT_URL`, `NEXT_PUBLIC_FIREBASE_*` (×7),
`CLAW_INTERFACE_URL`. Only the existing `CLOUDFLARE_ACCOUNT_ID` /
`CLOUDFLARE_WORKER_DEPLOY_TOKEN` secrets are required. A validate step
fails fast if any are missing.

**2. ESLint + lint gate** (`eslint.config.mjs` + `package.json` +
`code-quality.yml`)
- dashboard-console had no eslint config, so its `dashboard-quality`
gate covered only typecheck + tests (the Next apps lint via
`eslint-config-next`, which is Next-specific and doesn't fit React
Router).
- Adds a focused Vite/React/TS flat config (`typescript-eslint` +
`react-hooks`), `lint`/`lint:fix` scripts + devdeps, and a **Lint** step
to the `dashboard-quality` CI job (a required merge gate).

Net: dashboard-console now has lint + typecheck + tests as CI gates +
the dual-AI review — substantive parity with web-app / enterprise-admin
/ enterprise-app.

## Test plan
- [x] `eslint .` — clean (58 files, 0 problems)
- [x] `pnpm run typecheck` (cf-typegen + react-router typegen + tsc -b)
— clean
- [x] `pnpm run test` — 70 passed
- [x] `react-router build` + `wrangler deploy --dry-run -c
build/server/wrangler.json` — generated worker name resolves per env
(`zooclaw-dashboard-console` / `-staging`)
- [x] Both workflow YAMLs validate
- [ ] First real deploy (staging on merge to main) once the GitHub
Environments are confirmed wired

## Notes
- The deploy workflow does **not** run on this PR (it triggers on
push-to-main / tags / dispatch). The `dashboard-quality` gate (now incl.
lint) and the dual-AI review do.
- Leftover scaffold var `VALUE_FROM_CLOUDFLARE` in `wrangler.jsonc` left
as-is.
```

### PR Description

## Summary

Bring dashboard-console's CI/infra to parity with the other web apps — two `ci` commits:

**1. Cloudflare Workers deploy workflow** (`deploy-dashboard-console.yml` + `wrangler.jsonc`)
- Modeled on `deploy-enterprise-admin.yml`: merge to `main` → staging; tag `dashboard-console-v*-release` → production (`-beta` → staging); manual `workflow_dispatch`.
- React Router 7 + `@cloudflare/vite-plugin` specifics: **per-environment build** (Vite inlines `VITE_*` at build time, `CLOUDFLARE_ENV` selects the wrangler env), then deploy the plugin-generated `build/server/wrangler.json` (the source `wrangler.jsonc` `main` is a Vite-only virtual module wrangler can't bundle).
- Workers: `zooclaw-dashboard-console` / `zooclaw-dashboard-console-staging`; `workers.dev` routing for now (custom-domain TODO marked in `wrangler.jsonc`).
- **Reuses existing repo GitHub vars** mapped to `VITE_*` — no new vars: `NEXT_PUBLIC_ACCOUNT_URL`, `NEXT_PUBLIC_FIREBASE_*` (×7), `CLAW_INTERFACE_URL`. Only the existing `CLOUDFLARE_ACCOUNT_ID` / `CLOUDFLARE_WORKER_DEPLOY_TOKEN` secrets are required. A validate step fails fast if any are missing.

**2. ESLint + lint gate** (`eslint.config.mjs` + `package.json` + `code-quality.yml`)
- dashboard-console had no eslint config, so its `dashboard-quality` gate covered only typecheck + tests (the Next apps lint via `eslint-config-next`, which is Next-specific and doesn't fit React Router).
- Adds a focused Vite/React/TS flat config (`typescript-eslint` + `react-hooks`), `lint`/`lint:fix` scripts + devdeps, and a **Lint** step to the `dashboard-quality` CI job (a required merge gate).

Net: dashboard-console now has lint + typecheck + tests as CI gates + the dual-AI review — substantive parity with web-app / enterprise-admin / enterprise-app.

## Test plan
- [x] `eslint .` — clean (58 files, 0 problems)
- [x] `pnpm run typecheck` (cf-typegen + react-router typegen + tsc -b) — clean
- [x] `pnpm run test` — 70 passed
- [x] `react-router build` + `wrangler deploy --dry-run -c build/server/wrangler.json` — generated worker name resolves per env (`zooclaw-dashboard-console` / `-staging`)
- [x] Both workflow YAMLs validate
- [ ] First real deploy (staging on merge to main) once the GitHub Environments are confirmed wired

## Notes
- The deploy workflow does **not** run on this PR (it triggers on push-to-main / tags / dispatch). The `dashboard-quality` gate (now incl. lint) and the dual-AI review do.
- Leftover scaffold var `VALUE_FROM_CLOUDFLARE` in `wrangler.jsonc` left as-is.


---

## 5. fix(billing): show trial subscription orders distinctly (#2214)

- **SHA**: `296a9a4b556175d377a3fc6db780e30868728cfd`
- **Author**: kaka-srp
- **Date**: 2026-06-04T09:36:45Z
- **Files Changed**: 17
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/296a9a4b556175d377a3fc6db780e30868728cfd
- **PR**: #2214

### Full Commit Message

```
fix(billing): show trial subscription orders distinctly (#2214)

## Summary
- Return Billing v2 zero-amount trial subscription orders as
`status=trial` instead of `paid` in order responses.
- Keep trial orders successful in checkout polling/history UI without
treating them as paid invoices.
- Add a paid-entitlement guard so Stripe/Antom payment entitlements
require positive payment amounts.
- One-off cleanup scripts are intentionally not included in this PR.

## Root cause
Stripe/Antom trial flows can create zero-amount subscription
orders/invoices. Billing v2 already records trial entitlements
separately, but order responses mapped all `succeeded` payment orders to
`paid`, and the paid entitlement validator allowed zero-amount provider
orders. That blurred trial display semantics with paid fulfillment
semantics.

## Test plan
- [x] `source /home/node/.venvs/claw-interface/bin/activate && pytest
services/claw-interface/tests/unit/test_billing_v2_order_requests.py
services/claw-interface/tests/unit/test_billing_v2_payment_orders.py`
- [x] `source /home/node/.venvs/claw-interface/bin/activate && ruff
check services/claw-interface/app/schema/order.py
services/claw-interface/app/services/billing_v2/order_requests.py
services/claw-interface/app/services/billing_v2/payment_orders.py
services/claw-interface/tests/unit/test_billing_v2_order_requests.py
services/claw-interface/tests/unit/test_billing_v2_payment_orders.py`
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/components/billing/InvoiceHistory.unit.spec.tsx
tests/unit/lib/payment/handle-payment-success.unit.spec.ts
tests/unit/app/subscription/SuccessClient.unit.spec.tsx`
- [x] `pnpm --dir web/app exec eslint
src/components/billing/InvoiceHistory.tsx
src/app/[locale]/admin/components/OrderHistoryModal.tsx
src/app/[locale]/subscription/success/SuccessClient.tsx
src/lib/api/user.ts src/lib/payment/handle-payment-success.ts
tests/unit/components/billing/InvoiceHistory.unit.spec.tsx
tests/unit/lib/payment/handle-payment-success.unit.spec.ts
tests/unit/app/subscription/SuccessClient.unit.spec.tsx` (warnings only
in pre-existing `user.ts` `any` types)
- [ ] `pnpm --dir web/app exec tsc --noEmit --pretty false` currently
fails on pre-existing `motion/react` module resolution and unrelated
implicit-any errors outside this PR scope.
```

### PR Description

## Summary
- Return Billing v2 zero-amount trial subscription orders as `status=trial` instead of `paid` in order responses.
- Keep trial orders successful in checkout polling/history UI without treating them as paid invoices.
- Add a paid-entitlement guard so Stripe/Antom payment entitlements require positive payment amounts.
- One-off cleanup scripts are intentionally not included in this PR.

## Root cause
Stripe/Antom trial flows can create zero-amount subscription orders/invoices. Billing v2 already records trial entitlements separately, but order responses mapped all `succeeded` payment orders to `paid`, and the paid entitlement validator allowed zero-amount provider orders. That blurred trial display semantics with paid fulfillment semantics.

## Test plan
- [x] `source /home/node/.venvs/claw-interface/bin/activate && pytest services/claw-interface/tests/unit/test_billing_v2_order_requests.py services/claw-interface/tests/unit/test_billing_v2_payment_orders.py`
- [x] `source /home/node/.venvs/claw-interface/bin/activate && ruff check services/claw-interface/app/schema/order.py services/claw-interface/app/services/billing_v2/order_requests.py services/claw-interface/app/services/billing_v2/payment_orders.py services/claw-interface/tests/unit/test_billing_v2_order_requests.py services/claw-interface/tests/unit/test_billing_v2_payment_orders.py`
- [x] `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/components/billing/InvoiceHistory.unit.spec.tsx tests/unit/lib/payment/handle-payment-success.unit.spec.ts tests/unit/app/subscription/SuccessClient.unit.spec.tsx`
- [x] `pnpm --dir web/app exec eslint src/components/billing/InvoiceHistory.tsx src/app/[locale]/admin/components/OrderHistoryModal.tsx src/app/[locale]/subscription/success/SuccessClient.tsx src/lib/api/user.ts src/lib/payment/handle-payment-success.ts tests/unit/components/billing/InvoiceHistory.unit.spec.tsx tests/unit/lib/payment/handle-payment-success.unit.spec.ts tests/unit/app/subscription/SuccessClient.unit.spec.tsx` (warnings only in pre-existing `user.ts` `any` types)
- [ ] `pnpm --dir web/app exec tsc --noEmit --pretty false` currently fails on pre-existing `motion/react` module resolution and unrelated implicit-any errors outside this PR scope.

---

## 6. fix(claw-interface): reconcile /agents with agent workspaces and drop legacy mattermost fallback (#2210)

- **SHA**: `4ac823306b65da2194831de69c04c2c0509ada1e`
- **Author**: bill-srp
- **Date**: 2026-06-04T08:10:43Z
- **Files Changed**: 18
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4ac823306b65da2194831de69c04c2c0509ada1e
- **PR**: #2210

### Full Commit Message

```
fix(claw-interface): reconcile /agents with agent workspaces and drop legacy mattermost fallback (#2210)

## Summary
- **Drop the legacy Mattermost user fallback.** The human Mattermost
identity now resolves from account-root `mattermost_user` only —
removing the `openclaw_bots[0].mattermost_user` fallback from
`resolve_mattermost_user_dict()`, the openclaw-agents route token helper
(and the now-dead `_get_user_openclaw_bot_root`), and user enrichment.
(drop-`openclaw_bots` migration, Task 1)
- **`GET /agents` now reads `ecap-agent-workspaces`.** The endpoint
reconciles `selected_agent_ids` against the primary computer's workspace
rows and drops any selected agent that has no workspace (`main` always
kept). An empty workspace set disables filtering, so an incomplete V2
backfill never hides every agent.

## Root cause
- **Mattermost identity:** post account-root canonicalization,
`mattermost_user` moved to the account root, but the resolver / route
helper / `extract_mattermost_info()` still fell back to the nested
`openclaw_bots[0].mattermost_user`, keeping the legacy embedded array
load-bearing.
- **Ghost agents:** `GET /agents` built its list purely from
`account.selected_agent_ids` + live FastClaw config and never read the
V2 workspace store. A selected agent whose `ecap-agent-workspaces` row
was missing (incomplete backfill, failed/rolled-back install, or a
soft-deleted workspace) was still returned — with a `null` workspace.

## Test plan
- [x] Affected unit files green in the devcontainer:
`test_account_mattermost_user_typed`, `test_user_enrichment_service`,
`test_user_routes_coverage`, `test_openclaw_agents`,
`test_agent_response`, `test_runtime_state` (222 passed)
- [x] Full unit suite: **1347 passed** (the only failure,
`test_ci_lint_deptry::test_clean_tree_passes`, is environmental — the
worktree git-pointer is unresolvable inside the devcontainer)
- [x] `ruff format --check` + `ruff check` clean; `pyright` 0 errors on
changed files
- [x] New regression tests: ghost agent filtered from `GET /agents`;
empty workspace store keeps all selected agents (no mass-hide during
backfill); MM token / resolver resolve root-only and ignore legacy
nested data

Split into two reviewable commits (fallback removal; `/agents`
reconciliation).
```

### PR Description

## Summary
- **Drop the legacy Mattermost user fallback.** The human Mattermost identity now resolves from account-root `mattermost_user` only — removing the `openclaw_bots[0].mattermost_user` fallback from `resolve_mattermost_user_dict()`, the openclaw-agents route token helper (and the now-dead `_get_user_openclaw_bot_root`), and user enrichment. (drop-`openclaw_bots` migration, Task 1)
- **`GET /agents` now reads `ecap-agent-workspaces`.** The endpoint reconciles `selected_agent_ids` against the primary computer's workspace rows and drops any selected agent that has no workspace (`main` always kept). An empty workspace set disables filtering, so an incomplete V2 backfill never hides every agent.

## Root cause
- **Mattermost identity:** post account-root canonicalization, `mattermost_user` moved to the account root, but the resolver / route helper / `extract_mattermost_info()` still fell back to the nested `openclaw_bots[0].mattermost_user`, keeping the legacy embedded array load-bearing.
- **Ghost agents:** `GET /agents` built its list purely from `account.selected_agent_ids` + live FastClaw config and never read the V2 workspace store. A selected agent whose `ecap-agent-workspaces` row was missing (incomplete backfill, failed/rolled-back install, or a soft-deleted workspace) was still returned — with a `null` workspace.

## Test plan
- [x] Affected unit files green in the devcontainer: `test_account_mattermost_user_typed`, `test_user_enrichment_service`, `test_user_routes_coverage`, `test_openclaw_agents`, `test_agent_response`, `test_runtime_state` (222 passed)
- [x] Full unit suite: **1347 passed** (the only failure, `test_ci_lint_deptry::test_clean_tree_passes`, is environmental — the worktree git-pointer is unresolvable inside the devcontainer)
- [x] `ruff format --check` + `ruff check` clean; `pyright` 0 errors on changed files
- [x] New regression tests: ghost agent filtered from `GET /agents`; empty workspace store keeps all selected agents (no mass-hide during backfill); MM token / resolver resolve root-only and ignore legacy nested data

Split into two reviewable commits (fallback removal; `/agents` reconciliation).

---

## 7. fix(billing): add provider fulfillment idempotency (#2209)

- **SHA**: `cb53981eea6d81d1da7003f7288c750207dba184`
- **Author**: kaka-srp
- **Date**: 2026-06-04T08:10:42Z
- **Files Changed**: 19
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/cb53981eea6d81d1da7003f7288c750207dba184
- **PR**: #2209

### Full Commit Message

```
fix(billing): add provider fulfillment idempotency (#2209)

## Summary
- Add `provider_fulfillment_key` as the non-identity idempotency alias
for provider subscription periods.
- Write the alias on Stripe, Antom, and Apple subscription
payment/entitlement facts, and add Stripe/Antom reconcile guards before
recovery grants.
- Add a dry-run/write backfill script plus spec for the historical data
cleanup.

Linear:
https://linear.app/srpone/issue/ECA-892/fix-billing-v2-reconcile-idempotency

## Root cause
Historical Billing v2 backfill rows used
`backfill:{provider}:payment:{payment_order_id}:subscription`
entitlement operation keys, while provider reconcile checks canonical
subscription-period keys. Stripe also had historical
`environment=unknown` orders, so reconcile could miss both the
historical entitlement and payment order, create a new production order,
and grant BG credits again.

## Production data migration
- Dry-run: `entitlements_scanned=120`,
`entitlement_key_would_update=120`, `payment_order_key_would_update=94`,
`payment_order_missing=26`, no derivation failures or conflicts.
- Write: `entitlement_key_updated=120`, `payment_order_key_updated=92`,
`payment_order_key_already_set=2`, `payment_order_missing=26`.
- Post-write verification: `entitlement_key_ok=120`,
`payment_order_key_ok=94`, `payment_order_missing=26`, no mismatches.
- The 26 missing payment orders are deliberate repaired duplicate-order
tombstones whose user-visible payment orders were deleted.

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check app tests
scripts/billing_v2_backfill_provider_fulfillment_keys.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff format --check app
tests scripts/billing_v2_backfill_provider_fulfillment_keys.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_v2*.py tests/unit/test_stripe_billing_v2.py
tests/unit/test_stripe_billing_v2_reconcile.py
tests/unit/test_antom_billing_v2.py
tests/unit/test_antom_billing_v2_reconcile.py
tests/unit/test_apple_billing_v2.py
tests/unit/test_apple_billing_v2_reconcile.py -q`
```

### PR Description

## Summary
- Add `provider_fulfillment_key` as the non-identity idempotency alias for provider subscription periods.
- Write the alias on Stripe, Antom, and Apple subscription payment/entitlement facts, and add Stripe/Antom reconcile guards before recovery grants.
- Add a dry-run/write backfill script plus spec for the historical data cleanup.

Linear: https://linear.app/srpone/issue/ECA-892/fix-billing-v2-reconcile-idempotency

## Root cause
Historical Billing v2 backfill rows used `backfill:{provider}:payment:{payment_order_id}:subscription` entitlement operation keys, while provider reconcile checks canonical subscription-period keys. Stripe also had historical `environment=unknown` orders, so reconcile could miss both the historical entitlement and payment order, create a new production order, and grant BG credits again.

## Production data migration
- Dry-run: `entitlements_scanned=120`, `entitlement_key_would_update=120`, `payment_order_key_would_update=94`, `payment_order_missing=26`, no derivation failures or conflicts.
- Write: `entitlement_key_updated=120`, `payment_order_key_updated=92`, `payment_order_key_already_set=2`, `payment_order_missing=26`.
- Post-write verification: `entitlement_key_ok=120`, `payment_order_key_ok=94`, `payment_order_missing=26`, no mismatches.
- The 26 missing payment orders are deliberate repaired duplicate-order tombstones whose user-visible payment orders were deleted.

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check app tests scripts/billing_v2_backfill_provider_fulfillment_keys.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff format --check app tests scripts/billing_v2_backfill_provider_fulfillment_keys.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/pyright app tests`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_v2*.py tests/unit/test_stripe_billing_v2.py tests/unit/test_stripe_billing_v2_reconcile.py tests/unit/test_antom_billing_v2.py tests/unit/test_antom_billing_v2_reconcile.py tests/unit/test_apple_billing_v2.py tests/unit/test_apple_billing_v2_reconcile.py -q`


---

## 8. feat(dashboard-console): restrict console and internal API to @srp.one accounts (#2211)

- **SHA**: `577e08e741de55b02fa304805807dade5f5e7b57`
- **Author**: bill-srp
- **Date**: 2026-06-04T07:25:12Z
- **Files Changed**: 12
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/577e08e741de55b02fa304805807dade5f5e7b57
- **PR**: #2211

### Full Commit Message

```
feat(dashboard-console): restrict console and internal API to @srp.one accounts (#2211)

## Linear
https://linear.app/srpone/issue/ECA-886

## Summary

Restrict the dashboard-console admin surface to SRP staff (`@srp.one`),
end-to-end, plus two smaller items bundled on the branch (one PR per
request).

**Backend (`claw-interface`)**
- Add `require_srp_account` FastAPI dependency: authorizes only when the
**token** email ends with `@srp.one`. Uses the token identity's email
(not `Account.email`, which is nullable/often blank); returns the
`Account`. Depends on both `get_token_identity` and
`get_current_account`, and `verify_user_token`'s TTL cache keeps it to a
single account-service call.
- Gate **every** `/internal` route at the router level
(`dependencies=[Depends(require_srp_account)]`), replacing the
per-endpoint `require_admin_user` on the agent-packs routes. Pinned by
`test_all_internal_routes_require_srp_account`.

**Frontend (`dashboard-console`)**
- `isSrpEmail()` mirrors the backend domain check (leading `@` anchor
rejects look-alike domains).
- `AuthGate` renders an "Access restricted" panel (with Sign out) for an
authenticated non-`@srp.one` user, instead of dropping them into a
console whose API calls would all 403.

**Also bundled**
- `fix(dashboard-console)`: the avatar uploader was gated to create
mode, so the Update-pack form had no avatar control. Render the
`FileField` in edit mode too (the view-model already wired the
edit-upload path, seeding from the pack's current `avatar_url`).
- `chore(dashboard-console)`: devcontainer publishes dev-server ports
(`127.0.0.1:5173` Vite, `127.0.0.1:8002→8000` backend) so the host
reaches them without a manual socat sidecar; host `8002` is offset from
`8000` to avoid colliding with the claw-interface worktree container
(inline comment flags the shared-file collision risk if it reaches
main).

## Test plan
- [x] Backend unit (49 passed): `require_srp_account` (srp / non-srp /
blank-email / case-insensitive / look-alike /
token-authoritative-over-account) +
`test_all_internal_routes_require_srp_account` + admin-route wiring +
CORS middleware
- [x] Frontend unit (70 passed) + `tsc -b` clean: `isSrpEmail`,
`AuthGate` restricted branch, `PackDialogBody` avatar field in edit &
create
- [ ] Manual: sign in as `@srp.one` → console loads; non-`@srp.one` →
restricted panel + Sign out; Update pack → Avatar upload field present
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-886

## Summary

Restrict the dashboard-console admin surface to SRP staff (`@srp.one`), end-to-end, plus two smaller items bundled on the branch (one PR per request).

**Backend (`claw-interface`)**
- Add `require_srp_account` FastAPI dependency: authorizes only when the **token** email ends with `@srp.one`. Uses the token identity's email (not `Account.email`, which is nullable/often blank); returns the `Account`. Depends on both `get_token_identity` and `get_current_account`, and `verify_user_token`'s TTL cache keeps it to a single account-service call.
- Gate **every** `/internal` route at the router level (`dependencies=[Depends(require_srp_account)]`), replacing the per-endpoint `require_admin_user` on the agent-packs routes. Pinned by `test_all_internal_routes_require_srp_account`.

**Frontend (`dashboard-console`)**
- `isSrpEmail()` mirrors the backend domain check (leading `@` anchor rejects look-alike domains).
- `AuthGate` renders an "Access restricted" panel (with Sign out) for an authenticated non-`@srp.one` user, instead of dropping them into a console whose API calls would all 403.

**Also bundled**
- `fix(dashboard-console)`: the avatar uploader was gated to create mode, so the Update-pack form had no avatar control. Render the `FileField` in edit mode too (the view-model already wired the edit-upload path, seeding from the pack's current `avatar_url`).
- `chore(dashboard-console)`: devcontainer publishes dev-server ports (`127.0.0.1:5173` Vite, `127.0.0.1:8002→8000` backend) so the host reaches them without a manual socat sidecar; host `8002` is offset from `8000` to avoid colliding with the claw-interface worktree container (inline comment flags the shared-file collision risk if it reaches main).

## Test plan
- [x] Backend unit (49 passed): `require_srp_account` (srp / non-srp / blank-email / case-insensitive / look-alike / token-authoritative-over-account) + `test_all_internal_routes_require_srp_account` + admin-route wiring + CORS middleware
- [x] Frontend unit (70 passed) + `tsc -b` clean: `isSrpEmail`, `AuthGate` restricted branch, `PackDialogBody` avatar field in edit & create
- [ ] Manual: sign in as `@srp.one` → console loads; non-`@srp.one` → restricted panel + Sign out; Update pack → Avatar upload field present


---

## 9. chore(claw-interface): add admin email→uid→bot_id lookup endpoint (#2204)

- **SHA**: `c58602dc3856472c978447e74a03375f0af23020`
- **Author**: Chris@ZooClaw
- **Date**: 2026-06-04T05:09:59Z
- **Files Changed**: 2
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c58602dc3856472c978447e74a03375f0af23020
- **PR**: #2204

### Full Commit Message

```
chore(claw-interface): add admin email→uid→bot_id lookup endpoint (#2204)

## Summary

Adds `POST /openclaw/admin/users/lookup` to `claw-interface`, resolving
a user's **email → uid(s) → bot_id(s)** in a single admin call.
Previously this required two manual hops across services (email→uid in
`user-interface`, then uid→bots here); there was no targeted endpoint.

### Design decisions
- **email→uid uses the authoritative store.** Reuses the existing
`profile_repo.find_uids_by_filter({"email": ...})`, which queries the
`gem_account` profile collection (the gem-sensitive/CSFLE store that
`user-interface` itself uses for ECAP) — **not** the `ecap-account`
mirror. No HTTP hop to `user-interface` and no change to that repo.
- **Multiple matches are surfaced, not hidden.** An email *should* map
to one uid; if more than one matches, we `logger.error(...)` the
collision but still return them all, so the caller sees it rather than
getting an arbitrary pick.
- **bot_ids prefer the Mongo cache, fall back to live FastClaw.** Each
uid's `bot_id`s come from the cached `ecap-account.openclaw_bots` array;
when that's empty we fall back to a live FastClaw `list_bots` call. A
failed fallback degrades to an empty list (`bot_source: "none"`) so one
user can't sink a multi-uid result. `bot_source` (`cache` / `fastclaw` /
`none`) is returned per user for transparency.
- **uid type bridging.** `gem_account.uid` is `Int64`;
`ecap-account.uid` is a string — converted explicitly before the second
hop.

Auth follows the existing admin pattern: guarded by `_require_admin`
(authn here, authz at the BFF layer); app tokens are always looked up
server-side, never accepted from the client.

### Response shape
```json
{
  "email": "user@example.com",
  "matched_uids": 1,
  "users": [
    { "uid": "12345", "bot_ids": ["b1", "b2"], "bot_source": "cache" }
  ]
}
```

## Review-driven fixes
- **FastClaw field-name asymmetry (Codex review).** The live
`client.list_bots()` API keys bot records as `id` (see
`routes/openclaw.py:366`), whereas the Mongo `openclaw_bots` cache keys
them as `bot_id`. The fallback now reads `bot.get("id")` (with a
defensive `or bot.get("bot_id")`) and the test mocks the real `{"id":
...}` shape, so empty-cache users no longer come back falsely as
`bot_source: "none"`.
- **Conflict with `main` resolved.** Merged the `runtime_state` /
`merge_runtime_bots_for_legacy_write` import refactor; the legacy
`openclaw_bots` cache + `bot_state_service.bot_ids_of` still exist
there, so the cache-first path is unchanged.

## Test plan
-
`tests/unit/test_openclaw_admin_routes.py::TestLookupUsersByEmailEndpoint`
— 5 cases:
  - single uid resolved from cache (asserts FastClaw is **not** called)
  - no match → 404
  - multiple uids → error logged + all returned
- cache empty → FastClaw fallback used, mocking the real `{"id": ...}`
shape (`bot_source: "fastclaw"`)
  - FastClaw fallback failure → degrades to empty (`bot_source: "none"`)
- `claw-interface` unit suite: **47 passed**. `ruff check` + `ruff
format` clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Adds `POST /openclaw/admin/users/lookup` to `claw-interface`, resolving a user's **email → uid(s) → bot_id(s)** in a single admin call. Previously this required two manual hops across services (email→uid in `user-interface`, then uid→bots here); there was no targeted endpoint.

### Design decisions
- **email→uid uses the authoritative store.** Reuses the existing `profile_repo.find_uids_by_filter({"email": ...})`, which queries the `gem_account` profile collection (the gem-sensitive/CSFLE store that `user-interface` itself uses for ECAP) — **not** the `ecap-account` mirror. No HTTP hop to `user-interface` and no change to that repo.
- **Multiple matches are surfaced, not hidden.** An email *should* map to one uid; if more than one matches, we `logger.error(...)` the collision but still return them all, so the caller sees it rather than getting an arbitrary pick.
- **bot_ids prefer the Mongo cache, fall back to live FastClaw.** Each uid's `bot_id`s come from the cached `ecap-account.openclaw_bots` array; when that's empty we fall back to a live FastClaw `list_bots` call. A failed fallback degrades to an empty list (`bot_source: "none"`) so one user can't sink a multi-uid result. `bot_source` (`cache` / `fastclaw` / `none`) is returned per user for transparency.
- **uid type bridging.** `gem_account.uid` is `Int64`; `ecap-account.uid` is a string — converted explicitly before the second hop.

Auth follows the existing admin pattern: guarded by `_require_admin` (authn here, authz at the BFF layer); app tokens are always looked up server-side, never accepted from the client.

### Response shape
```json
{
  "email": "user@example.com",
  "matched_uids": 1,
  "users": [
    { "uid": "12345", "bot_ids": ["b1", "b2"], "bot_source": "cache" }
  ]
}
```

## Review-driven fixes
- **FastClaw field-name asymmetry (Codex review).** The live `client.list_bots()` API keys bot records as `id` (see `routes/openclaw.py:366`), whereas the Mongo `openclaw_bots` cache keys them as `bot_id`. The fallback now reads `bot.get("id")` (with a defensive `or bot.get("bot_id")`) and the test mocks the real `{"id": ...}` shape, so empty-cache users no longer come back falsely as `bot_source: "none"`.
- **Conflict with `main` resolved.** Merged the `runtime_state` / `merge_runtime_bots_for_legacy_write` import refactor; the legacy `openclaw_bots` cache + `bot_state_service.bot_ids_of` still exist there, so the cache-first path is unchanged.

## Test plan
- `tests/unit/test_openclaw_admin_routes.py::TestLookupUsersByEmailEndpoint` — 5 cases:
  - single uid resolved from cache (asserts FastClaw is **not** called)
  - no match → 404
  - multiple uids → error logged + all returned
  - cache empty → FastClaw fallback used, mocking the real `{"id": ...}` shape (`bot_source: "fastclaw"`)
  - FastClaw fallback failure → degrades to empty (`bot_source: "none"`)
- `claw-interface` unit suite: **47 passed**. `ruff check` + `ruff format` clean.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 10. fix(web): preserve signup attribution context (#2200)

- **SHA**: `bc9c9acd91111c6912137d261c12874de622f122`
- **Author**: Mori-srp
- **Date**: 2026-06-04T03:58:21Z
- **Files Changed**: 6
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/bc9c9acd91111c6912137d261c12874de622f122
- **PR**: #2200

### Full Commit Message

```
fix(web): preserve signup attribution context (#2200)

## Summary
- capture a first-session attribution snapshot for landing URLs, UTM
params, and Google Ads auto-tagging click IDs
- attach attribution diagnostics to sign_up GA4 and Google Ads
conversion events
- track page views when query params change so UTM-only route changes
are observable
- sanitize referrer URLs before sending diagnostics

## Safety
- does not change login, OTP, user creation, routing, backend API,
payment, or onboarding logic
- storage and URL parsing failures are swallowed so attribution
diagnostics cannot block registration
- no email, phone, user ID, token, or arbitrary query params are sent

## Tests
- pnpm exec vitest run --config ./vitest.config.mts
tests/unit/lib/attribution-snapshot.unit.spec.ts
tests/unit/lib/tracking.unit.spec.ts
- pnpm run test:unit
- pnpm run lint
```

### PR Description

## Summary
- capture a first-session attribution snapshot for landing URLs, UTM params, and Google Ads auto-tagging click IDs
- attach attribution diagnostics to sign_up GA4 and Google Ads conversion events
- track page views when query params change so UTM-only route changes are observable
- sanitize referrer URLs before sending diagnostics

## Safety
- does not change login, OTP, user creation, routing, backend API, payment, or onboarding logic
- storage and URL parsing failures are swallowed so attribution diagnostics cannot block registration
- no email, phone, user ID, token, or arbitrary query params are sent

## Tests
- pnpm exec vitest run --config ./vitest.config.mts tests/unit/lib/attribution-snapshot.unit.spec.ts tests/unit/lib/tracking.unit.spec.ts
- pnpm run test:unit
- pnpm run lint

---

## 11. fix(web): unify artifact preview cache buster (#2207)

- **SHA**: `b19bc44b47fbfff3c468a27c6737cadabad281ca`
- **Author**: sam-srp
- **Date**: 2026-06-04T02:46:28Z
- **Files Changed**: 4
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/b19bc44b47fbfff3c468a27c6737cadabad281ca
- **PR**: #2207

### Full Commit Message

```
fix(web): unify artifact preview cache buster (#2207)

## Summary
- Reintroduce a unified `_t=<timestamp>` cache-buster for artifact proxy
preview URLs.
- Move cache-busting from `HtmlRenderer` into `ArtifactPreview` so all
artifact preview renderers share the same behavior.
- Remove the HTML-only `_cb` parameter and keep non-artifact/presigned
URLs unchanged.

## Root cause
Artifact previews can serve stale content when the browser caches the
same artifact proxy URL after a regenerated file keeps the same path.
HTML previously had a renderer-local `_cb` workaround, but other preview
types still used unchanged artifact proxy URLs. A prior global `_t`
implementation was removed because it also modified
presigned/non-artifact URLs, which can break S3/R2 signature validation.
This change applies `_t` only to known artifact proxy hosts.

## Test plan
- [x] `git diff --check`
- [ ] Not run: app instructions say not to run tests/lint/build unless
explicitly requested.
```

### PR Description

## Summary
- Reintroduce a unified `_t=<timestamp>` cache-buster for artifact proxy preview URLs.
- Move cache-busting from `HtmlRenderer` into `ArtifactPreview` so all artifact preview renderers share the same behavior.
- Remove the HTML-only `_cb` parameter and keep non-artifact/presigned URLs unchanged.

## Root cause
Artifact previews can serve stale content when the browser caches the same artifact proxy URL after a regenerated file keeps the same path. HTML previously had a renderer-local `_cb` workaround, but other preview types still used unchanged artifact proxy URLs. A prior global `_t` implementation was removed because it also modified presigned/non-artifact URLs, which can break S3/R2 signature validation. This change applies `_t` only to known artifact proxy hosts.

## Test plan
- [x] `git diff --check`
- [ ] Not run: app instructions say not to run tests/lint/build unless explicitly requested.


---

## 12. docs(claw-interface): note multi-computer scoping risk on drop-bots plan (#2191)

- **SHA**: `4a1b12fe27b41585c01fb8f412d9b62c6bb8e244`
- **Author**: bill-srp
- **Date**: 2026-06-04T01:08:00Z
- **Files Changed**: 1
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4a1b12fe27b41585c01fb8f412d9b62c6bb8e244
- **PR**: #2191

### Full Commit Message

```
docs(claw-interface): note multi-computer scoping risk on drop-bots plan (#2191)

## Summary

Records two transitional **open design risks** on the OpenClaw
legacy-removal plan, surfaced by review of the v2 read-flip (#2176).
Docs only — no code.

- **Multi-computer scoping:** the v2 read path resolves "the bot" as the
*oldest* computer, while the dual-write scopes to
`openclaw_bots[0].bot_id`. These diverge on multi-computer accounts (now
reachable via `POST /computer`). The legacy-removal redesign must
replace "primary computer = the bot" with explicit per-bot/per-computer
scope.
- **Phantom legacy bot:** V2-only `provision_agent_mm` still writes
`openclaw_bots.0` unconditionally; the legacy-write destination needs a
guard once legacy bots aren't guaranteed.

These are accepted transitional limitations for the read-flip; this note
ensures the redesign addresses them.

## Test plan
- [x] Docs only — no code/CI test impact
```

### PR Description

## Summary

Records two transitional **open design risks** on the OpenClaw legacy-removal plan, surfaced by review of the v2 read-flip (#2176). Docs only — no code.

- **Multi-computer scoping:** the v2 read path resolves "the bot" as the *oldest* computer, while the dual-write scopes to `openclaw_bots[0].bot_id`. These diverge on multi-computer accounts (now reachable via `POST /computer`). The legacy-removal redesign must replace "primary computer = the bot" with explicit per-bot/per-computer scope.
- **Phantom legacy bot:** V2-only `provision_agent_mm` still writes `openclaw_bots.0` unconditionally; the legacy-write destination needs a guard once legacy bots aren't guaranteed.

These are accepted transitional limitations for the read-flip; this note ensures the redesign addresses them.

## Test plan
- [x] Docs only — no code/CI test impact

---

## 13. refactor(claw-interface): flip openclaw route/service reads to v2 computer store (#2177)

- **SHA**: `83d9702a43d845a421d52440f03f301407296aa8`
- **Author**: bill-srp
- **Date**: 2026-06-04T01:01:47Z
- **Files Changed**: 46
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/83d9702a43d845a421d52440f03f301407296aa8
- **PR**: #2177

### Full Commit Message

```
refactor(claw-interface): flip openclaw route/service reads to v2 computer store (#2177)

## Summary

Stack 3/3 of the #2157 split — flips the remaining OpenClaw runtime-read
consumers onto the v2 helpers landed in #2176 (merged). Read-source
migration only; legacy writes unchanged → **no user-facing behavior
change**.

- openclaw routes (init/status/restart/redeploy), agents, settings
- `bot_init`/`bot_lifecycle`/`bot_stop`/`bot_token`, `bot_resources`,
`runtime_legacy` shim
- warm-pool, enrichment, chat-replay, clawhub, twilio, connectors
- reintroduces the v2 `test_agent_mm_wiring`;
`test_openclaw_settings_routes` 3-way-merged with #2164 (desktop connect
code copy)

Rebuilt onto `main` after #2176 merged (consumer-only diff, 0 docs/core
leakage).

## PR size (size-override)

Labeled `size-override`: 46 files / +2450 −439, but only **~490 lines
are business code** — the other **~2399 are co-located tests** that must
ship with their code (the claw-interface coverage gate is whole-`app/`
90%, so production code can't outrun its tests). Cohesive
read-flip-consumers slice; the core already landed separately in #2176.

## Test plan

- [x] Rebuilt onto main via 3-way merge — consumer-only diff, no
docs/core leakage
- [ ] CI `claw-interface-quality` (unit + BDD + 90% coverage) green
- [ ] Dual AI review (Claude + Codex) pass
```

### PR Description

## Summary

Stack 3/3 of the #2157 split — flips the remaining OpenClaw runtime-read consumers onto the v2 helpers landed in #2176 (merged). Read-source migration only; legacy writes unchanged → **no user-facing behavior change**.

- openclaw routes (init/status/restart/redeploy), agents, settings
- `bot_init`/`bot_lifecycle`/`bot_stop`/`bot_token`, `bot_resources`, `runtime_legacy` shim
- warm-pool, enrichment, chat-replay, clawhub, twilio, connectors
- reintroduces the v2 `test_agent_mm_wiring`; `test_openclaw_settings_routes` 3-way-merged with #2164 (desktop connect code copy)

Rebuilt onto `main` after #2176 merged (consumer-only diff, 0 docs/core leakage).

## PR size (size-override)

Labeled `size-override`: 46 files / +2450 −439, but only **~490 lines are business code** — the other **~2399 are co-located tests** that must ship with their code (the claw-interface coverage gate is whole-`app/` 90%, so production code can't outrun its tests). Cohesive read-flip-consumers slice; the core already landed separately in #2176.

## Test plan

- [x] Rebuilt onto main via 3-way merge — consumer-only diff, no docs/core leakage
- [ ] CI `claw-interface-quality` (unit + BDD + 90% coverage) green
- [ ] Dual AI review (Claude + Codex) pass

---

