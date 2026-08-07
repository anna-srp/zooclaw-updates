# SerendipityOneInc/ecap-workspace commits 2026-08-06

## fix(web): auto-preview session thread attachments (#3289)

- sha: `eb7f3626065a741b4f66110dcdd6745a05dceb73`
- 作者: sam-srp
- 日期: 2026-08-06T12:22:53Z
- PR: #3289

### Commit Message

```
fix(web): auto-preview session thread attachments (#3289)

## What changed

- reuse the existing artifacts sidebar state in Session Thread
- pass only the current thread's normalized messages into attachment
detection
- automatically open previewable native attachments such as generated
Excel files
- preserve manual preview controls and session-scoped reset behavior
- add a Session Thread regression test for an `.xlsx` attachment

## Root cause

The Session Thread page used a local preview state that only supported
manual file opening. Unlike the main chat page, it was not connected to
the existing attachment auto-preview hook.

## Impact

Generated previewable attachments now open automatically in Session
Thread without scanning unrelated channel messages.

## Validation

- `SessionThreadClient.unit.spec.tsx`: 42 tests passed
- `useArtifactsSidebar.unit.spec.ts`: 20 tests passed
- TypeScript `tsc --noEmit`
- targeted ESLint
- Prettier check
- `git diff --check`
```

### PR Body

## What changed

- reuse the existing artifacts sidebar state in Session Thread
- pass only the current thread's normalized messages into attachment detection
- automatically open previewable native attachments such as generated Excel files
- preserve manual preview controls and session-scoped reset behavior
- add a Session Thread regression test for an `.xlsx` attachment

## Root cause

The Session Thread page used a local preview state that only supported manual file opening. Unlike the main chat page, it was not connected to the existing attachment auto-preview hook.

## Impact

Generated previewable attachments now open automatically in Session Thread without scanning unrelated channel messages.

## Validation

- `SessionThreadClient.unit.spec.tsx`: 42 tests passed
- `useArtifactsSidebar.unit.spec.ts`: 20 tests passed
- TypeScript `tsc --noEmit`
- targeted ESLint
- Prettier check
- `git diff --check`


### Files

- web/app/src/app/[locale]/(app)/(chat)/chat/[workspaceId]/sessions/[sessionId]/SessionThreadClient.tsx
- web/app/src/hooks/chat/useSessionThreadDisplayMessages.ts
- web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx

---

## fix(schedules): complete v2 one-shot workflow (#3285)

- sha: `f857f5a4796012242bccc6e8a6e4a7383c796df6`
- 作者: kaka-srp
- 日期: 2026-08-06T11:29:46Z
- PR: #3285

### Commit Message

```
fix(schedules): complete v2 one-shot workflow (#3285)

## Summary

- interpret the Schedule page's `datetime-local` input in browser local
time and send the corresponding UTC instant, with explicit UI guidance
- make product-created Engine one-shots request `deleteAfterRun`, keep
completed runs visible as read-only history, and map Temporal month
names back to ISO instants
- expose schedule-scoped isolated-session results through claw-interface
and a dedicated read-only Web result page
- keep Engine delivery fixed to `none`; this PR does not add
owner-default onboarding or an outbound destination selector

Engine dependency:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/624

## Root cause

The V2 product flow crossed several incomplete contracts: the Engine
emitted Temporal calendar month names that claw-interface did not map
back, product `at` requests did not opt into one-shot cleanup, run
projections did not expose their isolated result session, and the UI did
not explain that `datetime-local` is browser-local before conversion to
UTC. As a result, users could not reliably create, retain, or inspect
one-shot jobs even after the Engine-side create bug was fixed.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Web schedule tests: 8 files, 233 tests passed (1 todo)
- [x] claw-interface schedule tests: 92 passed
- [x] Web governance guards, TypeScript, and ESLint passed
- [x] Python ruff, format, pyright, and import-linter passed
- [ ] After Engine PR deployment, create a future `at` job in staging
and verify it fires once at the matching UTC instant
- [ ] Verify the completed job remains in history and its result link
renders only assistant-visible text
```

### PR Body

## Summary

- interpret the Schedule page's `datetime-local` input in browser local time and send the corresponding UTC instant, with explicit UI guidance
- make product-created Engine one-shots request `deleteAfterRun`, keep completed runs visible as read-only history, and map Temporal month names back to ISO instants
- expose schedule-scoped isolated-session results through claw-interface and a dedicated read-only Web result page
- keep Engine delivery fixed to `none`; this PR does not add owner-default onboarding or an outbound destination selector

Engine dependency: https://github.com/SerendipityOneInc/zooclaw-engine/pull/624

## Root cause

The V2 product flow crossed several incomplete contracts: the Engine emitted Temporal calendar month names that claw-interface did not map back, product `at` requests did not opt into one-shot cleanup, run projections did not expose their isolated result session, and the UI did not explain that `datetime-local` is browser-local before conversion to UTC. As a result, users could not reliably create, retain, or inspect one-shot jobs even after the Engine-side create bug was fixed.

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Web schedule tests: 8 files, 233 tests passed (1 todo)
- [x] claw-interface schedule tests: 92 passed
- [x] Web governance guards, TypeScript, and ESLint passed
- [x] Python ruff, format, pyright, and import-linter passed
- [ ] After Engine PR deployment, create a future `at` job in staging and verify it fires once at the matching UTC instant
- [ ] Verify the completed job remains in history and its result link renders only assistant-visible text


### Files

- docs/superpowers/specs/2026-08-06-v2-schedule-reliability-delivery.md
- services/claw-interface/app/routes/agents/schedules.py
- services/claw-interface/app/schema/agent_schedules.py
- services/claw-interface/app/services/agents/agent_schedule_mapping.py
- services/claw-interface/app/services/agents/agent_schedule_result_service.py
- services/claw-interface/app/services/agents/agent_schedule_service.py
- services/claw-interface/app/services/engine_client/_schedules.py
- services/claw-interface/tests/unit/test_agent_schedule_mapping.py
- services/claw-interface/tests/unit/test_agent_schedule_service.py
- services/claw-interface/tests/unit/test_agents_v2_schedules_routes.py
- services/claw-interface/tests/unit/test_engine_client_schedules.py
- web/app/scripts/mock-backend.mjs
- web/app/scripts/mock-backend/schedules.mjs
- web/app/src/app/[locale]/(app)/schedule/AllJobsSection.tsx
- web/app/src/app/[locale]/(app)/schedule/CronClient.tsx
- web/app/src/app/[locale]/(app)/schedule/CronJobForm.tsx
- web/app/src/app/[locale]/(app)/schedule/cron-types.ts
- web/app/src/app/[locale]/(app)/schedule/engine-rows.ts
- web/app/src/app/[locale]/(app)/schedule/results/[workspaceId]/[scheduleId]/[sessionId]/ScheduleResultClient.tsx
- web/app/src/app/[locale]/(app)/schedule/results/[workspaceId]/[scheduleId]/[sessionId]/page.tsx
- web/app/src/app/[locale]/(app)/schedule/results/[workspaceId]/[scheduleId]/[sessionId]/useViewModel.ts
- web/app/src/hooks/queries/agent-schedules/keys.ts
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts
- web/app/src/models/agent-schedule.ts
- web/app/src/services/agent-schedules.ts
- web/app/tests/unit/app/schedule/cron-client.unit.spec.tsx
- web/app/tests/unit/hooks/useEngineSchedules.unit.spec.tsx
- web/app/tests/unit/schedule/cron-form-target.unit.spec.tsx
- web/app/tests/unit/schedule/cron-row-actions.unit.spec.tsx
- web/app/tests/unit/schedule/engine-rows.unit.spec.ts
- web/app/tests/unit/schedule/schedule-result.unit.spec.tsx
- web/app/tests/unit/scripts/mock-backend-agent-schedules.unit.spec.ts
- web/app/tests/unit/services/agent-schedules.unit.spec.ts

---

## feat(claw): encrypt service-token user JWT under token-derived key (#3284)

- sha: `b80cc48fb73f1afc3cd54a61efdd5f073177f44d`
- 作者: bill-srp
- 日期: 2026-08-06T11:24:36Z
- PR: #3284

### Commit Message

```
feat(claw): encrypt service-token user JWT under token-derived key (#3284)

## Summary

**Follow-up to the org service-token proxy (#3276, merged): the bound
user's JWT is stored encrypted under a key derived from the service
token itself — no mint, no cross-repo dependency, no server-side key,
zero new configuration.**

The proxy needs a bound-user JWT to seed each new agent's
`USER_INTERNAL_TOKEN`. The original design minted one per install via a
cross-repo admin-secret endpoint in `user-interface`. This PR replaces
that entirely:

```
sha256(zct_token) ──lookup──▶ { metadata,
                                user_jwt_ciphertext:
                                  Fernet(KDF(zct_token)).encrypt(admin_jwt) }
```

- The `zct_` token keeps its **original 47-char random format** (nothing
embedded).
- At create, the management API captures the calling admin's verified
JWT (`get_bearer_token`) and stores it encrypted under a key derived
from the token plaintext — the only moment the server holds that
plaintext.
- **Domain separation (load-bearing)**: lookup hash =
`sha256(plaintext)`; encryption key = `sha256("zct-jwt-enc:" +
plaintext)` → Fernet key. The stored hash cannot derive the key, so the
row does not contain its own decryption material.
- At auth, the proxy decrypts the row's ciphertext with a key derived
from the **presented** token; the JWT lives on the principal in-memory
only (never returned, never logged). Missing ciphertext or decrypt
failure → 401 `service_token.invalid`.
- **Threat model**: a Mongo dump yields a one-way hash and a ciphertext
whose key is the token the DB doesn't have — nothing, **even combined
with a full server-environment compromise** (there is no server-side
key). Extracting a JWT requires the customer-held token, which already
grants full proxy access.

### API semantics (caller-only binding)

- **Create** — body `{name}`; binds to the caller; returns the one-time
plaintext.
- **Rebind = rotate** — no body; the server can't re-encrypt without the
customer's plaintext, so rebind mints a new plaintext (same
`token_id`/name/audit; new hash, prefix, ciphertext; bound to the
rebinding admin; CAS on active) and returns it once — the old plaintext
stops working immediately. This is the refresh/recovery path.
- **Revoke** — status flip + ciphertext scrubbed.

### Removed

- `token_mint_service` + its tests, the `SERVICE_TOKEN_MINT_ADMIN_TOKEN`
setting, and the whole `user-interface` mint endpoint from the rollout.
New dependency: `cryptography` (Fernet).

Spec synced in the same branch
(`docs/superpowers/specs/2026-08-05-org-service-tokens-design.md` —
token-derived encryption section, decision table, rollout).
Implementation by Codex (gpt-5.6-luna, xhigh) through three design
iterations (Mongo-plaintext snapshot → embed-in-token → token-derived
key, per product-owner direction); main merged in (post-#3276).

## Test plan

- [x] Unit: crypto round-trip, wrong-token decrypt fails,
**stored-hash-derived key cannot decrypt** (domain-separation
regression), create shape (47-char token + ciphertext), rotate (new
plaintext, old hash/ciphertext replaced, revoked-rotate →
`service_token.revoked`), revoke scrubs ciphertext, middleware decrypt
paths (valid / missing ciphertext / tampered → 401), seeding from
`principal.user_jwt` — 90 feature unit tests green.
- [x] `bash scripts/verify-py.sh` — ruff / pyright / import-linter
green.
- [x] BDD against local Mongo — lifecycle + rotate scenarios (old
plaintext 401s after rotation).
- [ ] CI `claw-interface-quality` (authoritative coverage gate).
```

### PR Body

## Summary

**Follow-up to the org service-token proxy (#3276, merged): the bound user's JWT is stored encrypted under a key derived from the service token itself — no mint, no cross-repo dependency, no server-side key, zero new configuration.**

The proxy needs a bound-user JWT to seed each new agent's `USER_INTERNAL_TOKEN`. The original design minted one per install via a cross-repo admin-secret endpoint in `user-interface`. This PR replaces that entirely:

```
sha256(zct_token) ──lookup──▶ { metadata,
                                user_jwt_ciphertext:
                                  Fernet(KDF(zct_token)).encrypt(admin_jwt) }
```

- The `zct_` token keeps its **original 47-char random format** (nothing embedded).
- At create, the management API captures the calling admin's verified JWT (`get_bearer_token`) and stores it encrypted under a key derived from the token plaintext — the only moment the server holds that plaintext.
- **Domain separation (load-bearing)**: lookup hash = `sha256(plaintext)`; encryption key = `sha256("zct-jwt-enc:" + plaintext)` → Fernet key. The stored hash cannot derive the key, so the row does not contain its own decryption material.
- At auth, the proxy decrypts the row's ciphertext with a key derived from the **presented** token; the JWT lives on the principal in-memory only (never returned, never logged). Missing ciphertext or decrypt failure → 401 `service_token.invalid`.
- **Threat model**: a Mongo dump yields a one-way hash and a ciphertext whose key is the token the DB doesn't have — nothing, **even combined with a full server-environment compromise** (there is no server-side key). Extracting a JWT requires the customer-held token, which already grants full proxy access.

### API semantics (caller-only binding)

- **Create** — body `{name}`; binds to the caller; returns the one-time plaintext.
- **Rebind = rotate** — no body; the server can't re-encrypt without the customer's plaintext, so rebind mints a new plaintext (same `token_id`/name/audit; new hash, prefix, ciphertext; bound to the rebinding admin; CAS on active) and returns it once — the old plaintext stops working immediately. This is the refresh/recovery path.
- **Revoke** — status flip + ciphertext scrubbed.

### Removed

- `token_mint_service` + its tests, the `SERVICE_TOKEN_MINT_ADMIN_TOKEN` setting, and the whole `user-interface` mint endpoint from the rollout. New dependency: `cryptography` (Fernet).

Spec synced in the same branch (`docs/superpowers/specs/2026-08-05-org-service-tokens-design.md` — token-derived encryption section, decision table, rollout). Implementation by Codex (gpt-5.6-luna, xhigh) through three design iterations (Mongo-plaintext snapshot → embed-in-token → token-derived key, per product-owner direction); main merged in (post-#3276).

## Test plan

- [x] Unit: crypto round-trip, wrong-token decrypt fails, **stored-hash-derived key cannot decrypt** (domain-separation regression), create shape (47-char token + ciphertext), rotate (new plaintext, old hash/ciphertext replaced, revoked-rotate → `service_token.revoked`), revoke scrubs ciphertext, middleware decrypt paths (valid / missing ciphertext / tampered → 401), seeding from `principal.user_jwt` — 90 feature unit tests green.
- [x] `bash scripts/verify-py.sh` — ruff / pyright / import-linter green.
- [x] BDD against local Mongo — lifecycle + rotate scenarios (old plaintext 401s after rotation).
- [ ] CI `claw-interface-quality` (authoritative coverage gate).


### Files

- docs/superpowers/specs/2026-08-05-org-service-tokens-design.md
- services/claw-interface/app/database/service_token_repo.py
- services/claw-interface/app/middleware/service_token.py
- services/claw-interface/app/routes/enterprise/service_tokens.py
- services/claw-interface/app/routes/service_api/_agents.py
- services/claw-interface/app/schema/service_token.py
- services/claw-interface/app/services/org/service_token_service.py
- services/claw-interface/tests/bdd/features/service_tokens.feature
- services/claw-interface/tests/bdd/step_defs/test_service_tokens.py
- services/claw-interface/tests/unit/_service_token_builders.py
- services/claw-interface/tests/unit/test_middleware_service_token.py
- services/claw-interface/tests/unit/test_routes_service_tokens.py
- services/claw-interface/tests/unit/test_service_proxy_agents.py
- services/claw-interface/tests/unit/test_service_token_repo.py
- services/claw-interface/tests/unit/test_service_token_service.py

---

## feat(claw): /service/v1 controld proxy with gateway tenancy (#3276)

- sha: `96a911886987a40d9d85fcd62f72a8d956a206a7`
- 作者: bill-srp
- 日期: 2026-08-06T10:43:39Z
- PR: #3276

### Commit Message

```
feat(claw): /service/v1 controld proxy with gateway tenancy (#3276)

## Summary

**Org service tokens — the `/service/v1` controld proxy.** Stacked on
#3274 (token storage + management API); base branch is
`feat/org-service-tokens-backend`. Together they complete the backend
plan (`docs/superpowers/plans/2026-08-06-org-service-tokens-backend.md`,
Tasks 2, 6–14) for the merged spec.

- **Engine tenancy mappings** — `ecap-service-engine-agents`,
`ecap-service-engine-environments`, `ecap-service-engine-uploads`
collections + repos (rows kept after engine-side deletion so
tenant-hiding 404s flow through and DELETE stays idempotent).
- **`require_service_token`** — `zct_` bearer auth for the proxy
surface: stable 401 codes
(`service_token.required/invalid/revoked/bound_user_not_member`), fails
closed when the bound user leaves the org, throttled fire-and-forget
`last_used_at` (strong task refs).
- **Bound-user mint client** — `SERVICE_TOKEN_MINT_ADMIN_TOKEN` + `POST
/user/mint-access-token` contract against the account service; fails
closed until the user-interface endpoint + secret exist (cross-repo
dependency, ships separately).
- **Engine proxy transport** — `ProxyMixin`: streamed pass-through
(`send(stream=True)`) and multipart rebuild with Idempotency-Key
forwarding; never interprets engine responses.
- **Catch-all `/service/v1/{path}`** with per-family tenancy:
- **agents** — ownership rewritten from the token on create
(caller-supplied ownership ignored), mapping recorded on 2xx with
compensating engine DELETE + retryable 502 if the mapping write fails,
credential auto-seeding (LiteLLM billing key + minted bound-user token;
failure → 502 with `agent_id`, mapping kept), id-scoped paths
mapping-gated, `credentials/*` blocked, list 404 in v1.
- **skills** — create anchors forced by scope (multipart rebuilt), list
params forced, id paths pre-fetch-and-check ownership, engine 5xx
masked.
- **environments/uploads** — mapping-gated id paths, unconditional
ownership injection on create-shaped bodies, `:archive` compensation,
declare records `upload_id → org`, finalize mapping-gated, list 404;
forced `org_id` selector kept as defense-in-depth.
- Unknown families → 404. Engine 2xx–4xx relay verbatim (controld
envelope is the public contract); 5xx/transport → masked gateway
envelope. GET/POST/PUT/DELETE forwarding is the documented exception
mirroring the upstream REST contract.
- **BDD** — token lifecycle end-to-end through the proxy (ownership
injection, mapping, foreign-agent 404, revoke → 401, rebind restores
access after the bound member leaves).

Implementation by Codex (gpt-5.6-luna, xhigh) from the plan; deviations
were adaptations to real repo signatures (`mongo.upsert_document` shape,
`EngineSkillRequestError` naming, `route.path_format` wiring assertions,
seeding routed through `_forward.get_engine_client()` for the patch
seam, proxy catch-all excluded from OpenAPI to avoid duplicate operation
ids).

## Test plan

- [x] Unit: mapping repos, `require_service_token` (all auth paths +
throttle), mint client (mint/fails-closed/bodyless errors), proxy
transport (verbatim forwarding, auth replacement, multipart,
transport-error mapping), and all four proxy families (ownership
rewrite, mapping gates with no-engine-call 404 assertions, compensation
branches, 5xx masking, seeding) — green locally.
- [x] `bash scripts/verify-py.sh` — ruff / pyright / import-linter green
on the stacked tree.
- [x] BDD suite runs against local Mongo (`verify-py.sh --full`).
- [ ] CI `claw-interface-quality` (authoritative coverage gate).
- [ ] Staging smoke after backend release + user-interface mint
endpoint: create token → proxied agent create → get/start/stop via
`zct_` → foreign-agent 404 → environment create/get → revoke → 401.
```

### PR Body

## Summary

**Org service tokens — the `/service/v1` controld proxy.** Stacked on #3274 (token storage + management API); base branch is `feat/org-service-tokens-backend`. Together they complete the backend plan (`docs/superpowers/plans/2026-08-06-org-service-tokens-backend.md`, Tasks 2, 6–14) for the merged spec.

- **Engine tenancy mappings** — `ecap-service-engine-agents`, `ecap-service-engine-environments`, `ecap-service-engine-uploads` collections + repos (rows kept after engine-side deletion so tenant-hiding 404s flow through and DELETE stays idempotent).
- **`require_service_token`** — `zct_` bearer auth for the proxy surface: stable 401 codes (`service_token.required/invalid/revoked/bound_user_not_member`), fails closed when the bound user leaves the org, throttled fire-and-forget `last_used_at` (strong task refs).
- **Bound-user mint client** — `SERVICE_TOKEN_MINT_ADMIN_TOKEN` + `POST /user/mint-access-token` contract against the account service; fails closed until the user-interface endpoint + secret exist (cross-repo dependency, ships separately).
- **Engine proxy transport** — `ProxyMixin`: streamed pass-through (`send(stream=True)`) and multipart rebuild with Idempotency-Key forwarding; never interprets engine responses.
- **Catch-all `/service/v1/{path}`** with per-family tenancy:
  - **agents** — ownership rewritten from the token on create (caller-supplied ownership ignored), mapping recorded on 2xx with compensating engine DELETE + retryable 502 if the mapping write fails, credential auto-seeding (LiteLLM billing key + minted bound-user token; failure → 502 with `agent_id`, mapping kept), id-scoped paths mapping-gated, `credentials/*` blocked, list 404 in v1.
  - **skills** — create anchors forced by scope (multipart rebuilt), list params forced, id paths pre-fetch-and-check ownership, engine 5xx masked.
  - **environments/uploads** — mapping-gated id paths, unconditional ownership injection on create-shaped bodies, `:archive` compensation, declare records `upload_id → org`, finalize mapping-gated, list 404; forced `org_id` selector kept as defense-in-depth.
  - Unknown families → 404. Engine 2xx–4xx relay verbatim (controld envelope is the public contract); 5xx/transport → masked gateway envelope. GET/POST/PUT/DELETE forwarding is the documented exception mirroring the upstream REST contract.
- **BDD** — token lifecycle end-to-end through the proxy (ownership injection, mapping, foreign-agent 404, revoke → 401, rebind restores access after the bound member leaves).

Implementation by Codex (gpt-5.6-luna, xhigh) from the plan; deviations were adaptations to real repo signatures (`mongo.upsert_document` shape, `EngineSkillRequestError` naming, `route.path_format` wiring assertions, seeding routed through `_forward.get_engine_client()` for the patch seam, proxy catch-all excluded from OpenAPI to avoid duplicate operation ids).

## Test plan

- [x] Unit: mapping repos, `require_service_token` (all auth paths + throttle), mint client (mint/fails-closed/bodyless errors), proxy transport (verbatim forwarding, auth replacement, multipart, transport-error mapping), and all four proxy families (ownership rewrite, mapping gates with no-engine-call 404 assertions, compensation branches, 5xx masking, seeding) — green locally.
- [x] `bash scripts/verify-py.sh` — ruff / pyright / import-linter green on the stacked tree.
- [x] BDD suite runs against local Mongo (`verify-py.sh --full`).
- [ ] CI `claw-interface-quality` (authoritative coverage gate).
- [ ] Staging smoke after backend release + user-interface mint endpoint: create token → proxied agent create → get/start/stop via `zct_` → foreign-agent 404 → environment create/get → revoke → 401.


### Files

- docs/superpowers/specs/2026-08-05-org-service-tokens-design.md
- services/claw-interface/app/create_app.py
- services/claw-interface/app/middleware/service_token.py
- services/claw-interface/app/routes/service_api/__init__.py
- services/claw-interface/app/routes/service_api/_agents.py
- services/claw-interface/app/routes/service_api/_environments.py
- services/claw-interface/app/routes/service_api/_forward.py
- services/claw-interface/app/routes/service_api/_skills.py
- services/claw-interface/app/routes/service_api/router.py
- services/claw-interface/app/services/engine_client/__init__.py
- services/claw-interface/app/services/engine_client/_proxy.py
- services/claw-interface/app/services/user/token_mint_service.py
- services/claw-interface/app/settings.py
- services/claw-interface/tests/bdd/features/service_tokens.feature
- services/claw-interface/tests/bdd/step_defs/test_service_tokens.py
- services/claw-interface/tests/unit/_service_token_builders.py
- services/claw-interface/tests/unit/test_engine_client_proxy.py
- services/claw-interface/tests/unit/test_middleware_service_token.py
- services/claw-interface/tests/unit/test_service_proxy_agents.py
- services/claw-interface/tests/unit/test_service_proxy_core.py
- services/claw-interface/tests/unit/test_service_proxy_environments.py
- services/claw-interface/tests/unit/test_service_proxy_skills.py
- services/claw-interface/tests/unit/test_token_mint_service.py

---

## fix(claw-interface): map weixin to ACS wechat platform at channel boundary (#3283)

- sha: `cebe769db5702a9365da4bb0ae5835703d6a9851`
- 作者: bill-srp
- 日期: 2026-08-06T10:41:32Z
- PR: #3283

### Commit Message

```
fix(claw-interface): map weixin to ACS wechat platform at channel boundary (#3283)

## Summary
- Translate the product platform name `weixin` to the ACS platform name
`wechat` at every agent-channel-service boundary in
`engine_agent_channels_service.py`, in both directions:
- outbound: `_create_channel_acs`, `update_channel`, `remove_channel`
send/address `wechat`
- inbound: `list_channels`, `update_channel`, `_create_channel_acs` map
returned `wechat` rows back to `weixin` via immutable `model_copy`
before they reach routes/frontend
- `add_channel` now rejects both spellings (`weixin` and `wechat`) with
`channel.weixin_setup_required`, so the direct-add path cannot bypass
the QR setup flow by using the ACS spelling.
- `engine_weixin_channel_service.py` (QR flow) is unchanged — its
`weixin` constant is the product name; existing-channel detection and
create/update go through the mapped service functions.

## Root cause
The engine-agent WeChat QR bind has failed 100% since #2973: after the
user scans and confirms the QR, claw-interface calls ACS
`create_channel` with `platform: "weixin"`, but ACS
`ManagedChannelPlatformSchema` only accepts `["feishu", "mattermost",
"slack", "wechat", "wecom"]` — the request dies with 400 `request failed
validation` (surfaced as `channel.invalid_request`). The ACS channel-API
design doc maps the product WeChat platform to ACS `wechat`;
claw-interface never implemented that translation, while sibling flows
(`wecom`, `feishu`) happen to use enum-valid names. Diagnosed in staging
for uid `7268822997437874176` / workspace
`49593ba04519473d805a98745ae56a0b` (3 bind attempts 2026-08-06
08:19–08:25 UTC, each `confirmed` then ACS 400).

The frontend contract stays `weixin` throughout (`isWeixinPlatform()`
accepts `weixin`/`openclaw-weixin`, not `wechat`), so responses are
mapped back symmetrically. The v1 computer-runtime flow
(`openclaw-weixin`) never touches ACS and is unaffected.

## Test plan
- [x] TDD: new unit tests written first (red), then implementation
(green)
- create for weixin sends `platform="wechat"` to the ACS client
(idempotency key keeps the product name)
  - update/remove with `weixin` address the ACS channel as `wechat`
- `list_channels` maps a `wechat` row back to `weixin` (immutable copy,
original row untouched), passes `feishu`/`wecom`/`slack` through, still
filters `mattermost`
- `update_channel`/create return product-named rows (route
`AgentChannelPublic` never sees `wechat`)
- `add_channel` rejects both `weixin` and `wechat` with
`channel.weixin_setup_required`
- end-to-end QR poll test: existing-channel detection matches when ACS
returns a `wechat` row, `update_channel` called with `wechat`, no
duplicate create
- [x] `bash scripts/verify-py.sh` green (ruff, ruff-format, pyright,
import-linter 8/8 contracts)
- [x] 128 unit tests pass across
`test_engine_agent_channels_service.py`,
`test_engine_weixin_channel_service.py`,
`test_agents_v2_channels_routes.py`
- [ ] Post-deploy: staging QR bind smoke (scan → confirmed → channel row
created in ACS, listed as `weixin` in UI) — cross-service enum drift is
invisible to static checks, needs one real end-to-end pass
```

### PR Body

## Summary
- Translate the product platform name `weixin` to the ACS platform name `wechat` at every agent-channel-service boundary in `engine_agent_channels_service.py`, in both directions:
  - outbound: `_create_channel_acs`, `update_channel`, `remove_channel` send/address `wechat`
  - inbound: `list_channels`, `update_channel`, `_create_channel_acs` map returned `wechat` rows back to `weixin` via immutable `model_copy` before they reach routes/frontend
- `add_channel` now rejects both spellings (`weixin` and `wechat`) with `channel.weixin_setup_required`, so the direct-add path cannot bypass the QR setup flow by using the ACS spelling.
- `engine_weixin_channel_service.py` (QR flow) is unchanged — its `weixin` constant is the product name; existing-channel detection and create/update go through the mapped service functions.

## Root cause
The engine-agent WeChat QR bind has failed 100% since #2973: after the user scans and confirms the QR, claw-interface calls ACS `create_channel` with `platform: "weixin"`, but ACS `ManagedChannelPlatformSchema` only accepts `["feishu", "mattermost", "slack", "wechat", "wecom"]` — the request dies with 400 `request failed validation` (surfaced as `channel.invalid_request`). The ACS channel-API design doc maps the product WeChat platform to ACS `wechat`; claw-interface never implemented that translation, while sibling flows (`wecom`, `feishu`) happen to use enum-valid names. Diagnosed in staging for uid `7268822997437874176` / workspace `49593ba04519473d805a98745ae56a0b` (3 bind attempts 2026-08-06 08:19–08:25 UTC, each `confirmed` then ACS 400).

The frontend contract stays `weixin` throughout (`isWeixinPlatform()` accepts `weixin`/`openclaw-weixin`, not `wechat`), so responses are mapped back symmetrically. The v1 computer-runtime flow (`openclaw-weixin`) never touches ACS and is unaffected.

## Test plan
- [x] TDD: new unit tests written first (red), then implementation (green)
  - create for weixin sends `platform="wechat"` to the ACS client (idempotency key keeps the product name)
  - update/remove with `weixin` address the ACS channel as `wechat`
  - `list_channels` maps a `wechat` row back to `weixin` (immutable copy, original row untouched), passes `feishu`/`wecom`/`slack` through, still filters `mattermost`
  - `update_channel`/create return product-named rows (route `AgentChannelPublic` never sees `wechat`)
  - `add_channel` rejects both `weixin` and `wechat` with `channel.weixin_setup_required`
  - end-to-end QR poll test: existing-channel detection matches when ACS returns a `wechat` row, `update_channel` called with `wechat`, no duplicate create
- [x] `bash scripts/verify-py.sh` green (ruff, ruff-format, pyright, import-linter 8/8 contracts)
- [x] 128 unit tests pass across `test_engine_agent_channels_service.py`, `test_engine_weixin_channel_service.py`, `test_agents_v2_channels_routes.py`
- [ ] Post-deploy: staging QR bind smoke (scan → confirmed → channel row created in ACS, listed as `weixin` in UI) — cross-service enum drift is invisible to static checks, needs one real end-to-end pass


### Files

- services/claw-interface/app/services/agents/engine_agent_channels_service.py
- services/claw-interface/tests/unit/test_engine_agent_channels_service.py
- services/claw-interface/tests/unit/test_engine_weixin_channel_service.py

---

## fix(chat): 恢复模型默认回退并限制 Agent 下拉框高度 (#3281)

- sha: `eb60a91b299ab45e164e1dc52265a3f213652b43`
- 作者: lynn Zhuang
- 日期: 2026-08-06T09:30:21Z
- PR: #3281

### Commit Message

```
fix(chat): 恢复模型默认回退并限制 Agent 下拉框高度 (#3281)

## 摘要
- 当前工作区模型读取失败时，回退显示模型目录中的默认模型，同时保留“无法切换模型”的只读原因。
- 分离模型目录错误与当前模型控制器错误，确保 New Task 和现有聊天会话仍可浏览模型列表。
- 限制 Agent 选择器的高度不超过可用视口，并为较长的 Agent 列表启用独立滚动。

## 根因
统一输入框此前会把“当前模型读取失败”传递成模型选择器的“模型目录错误”。即使模型目录已经成功加载，默认模型也会被 `Models
unavailable` 替代。与此同时，Agent 选择器使用了 `overflow-hidden`，却没有设置最大高度，导致 Agent
较多时下拉框会延伸到浏览器视口之外。

## 测试计划
- [x] `bash scripts/verify-web.sh
web/app/src/components/chat/unified-chat-composer/UnifiedChatComposer.tsx
web/app/tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx`
- [x] `pnpm --filter @zooclaw/chat-ui exec tsc --noEmit`
- [x] `pnpm --filter @zooclaw/chat-ui exec vitest run
src/__tests__/agent-picker.test.tsx`
- [x] `pnpm --filter @zooclaw/chat-ui exec eslint
src/composer/AgentPicker.tsx src/__tests__/agent-picker.test.tsx
--max-warnings=0`
- [x] `bash scripts/verify-changed.sh`
- [x] 本地可视化验证 New Task、聊天会话模型菜单，以及长 Agent 列表的滚动效果。
```

### PR Body

## 摘要
- 当前工作区模型读取失败时，回退显示模型目录中的默认模型，同时保留“无法切换模型”的只读原因。
- 分离模型目录错误与当前模型控制器错误，确保 New Task 和现有聊天会话仍可浏览模型列表。
- 限制 Agent 选择器的高度不超过可用视口，并为较长的 Agent 列表启用独立滚动。

## 根因
统一输入框此前会把“当前模型读取失败”传递成模型选择器的“模型目录错误”。即使模型目录已经成功加载，默认模型也会被 `Models unavailable` 替代。与此同时，Agent 选择器使用了 `overflow-hidden`，却没有设置最大高度，导致 Agent 较多时下拉框会延伸到浏览器视口之外。

## 测试计划
- [x] `bash scripts/verify-web.sh web/app/src/components/chat/unified-chat-composer/UnifiedChatComposer.tsx web/app/tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx`
- [x] `pnpm --filter @zooclaw/chat-ui exec tsc --noEmit`
- [x] `pnpm --filter @zooclaw/chat-ui exec vitest run src/__tests__/agent-picker.test.tsx`
- [x] `pnpm --filter @zooclaw/chat-ui exec eslint src/composer/AgentPicker.tsx src/__tests__/agent-picker.test.tsx --max-warnings=0`
- [x] `bash scripts/verify-changed.sh`
- [x] 本地可视化验证 New Task、聊天会话模型菜单，以及长 Agent 列表的滚动效果。


### Files

- web/app/src/components/chat/unified-chat-composer/UnifiedChatComposer.tsx
- web/app/tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx
- web/packages/chat-ui/src/__tests__/agent-picker.test.tsx
- web/packages/chat-ui/src/composer/AgentPicker.tsx

---

## feat(web): add and update legal policy pages (#3282)

- sha: `13b2fbe4cdfccea4f6bd4be8ae61786dfb6db22a`
- 作者: ericma-srp
- 日期: 2026-08-06T09:21:10Z
- PR: #3282

### Commit Message

```
feat(web): add and update legal policy pages (#3282)

## Linear

N/A

## Summary

- add standalone Refund and DMCA policy pages using the existing Terms
page visual treatment
- update Terms eligibility and acceptable-use language, and disclose
Privacy Policy subprocessors
- keep the new legal routes locale-free without adding Landing, Header,
Footer, or settings entry points

## Risk and follow-up

- Product-owner decision: the `NEED_HUMAN_REVIEW` finding about the
Airwallex disclosure is accepted as controlled risk for this PR.
- This release ships the approved legal terms only. It does not change
payment, billing, subscription, cancellation, or refund execution logic.
- Payment-provider and business-logic alignment will be handled as a
separate follow-up after the legal terms are published and does not
block this legal-page rollout.

## Test plan

- [x] `bash scripts/verify-web.sh --test-only
tests/unit/app/legal-policy-pages.unit.spec.tsx
tests/unit/middleware/middleware.unit.spec.ts`
- [x] `bash scripts/verify-web.sh --no-test <changed paths>`
- [x] `bash scripts/verify-changed.sh`
- [x] locally rendered Refund, DMCA, Terms, and Privacy routes returned
HTTP 200 and were approved in preview

Co-authored-by: eric <eric.ma@creatibi.com>
```

### PR Body

## Linear

N/A

## Summary

- add standalone Refund and DMCA policy pages using the existing Terms page visual treatment
- update Terms eligibility and acceptable-use language, and disclose Privacy Policy subprocessors
- keep the new legal routes locale-free without adding Landing, Header, Footer, or settings entry points

## Risk and follow-up

- Product-owner decision: the `NEED_HUMAN_REVIEW` finding about the Airwallex disclosure is accepted as controlled risk for this PR.
- This release ships the approved legal terms only. It does not change payment, billing, subscription, cancellation, or refund execution logic.
- Payment-provider and business-logic alignment will be handled as a separate follow-up after the legal terms are published and does not block this legal-page rollout.

## Test plan

- [x] `bash scripts/verify-web.sh --test-only tests/unit/app/legal-policy-pages.unit.spec.tsx tests/unit/middleware/middleware.unit.spec.ts`
- [x] `bash scripts/verify-web.sh --no-test <changed paths>`
- [x] `bash scripts/verify-changed.sh`
- [x] locally rendered Refund, DMCA, Terms, and Privacy routes returned HTTP 200 and were approved in preview


### Files

- web/app/src/app/_seo.ts
- web/app/src/app/about/dmca/page.tsx
- web/app/src/app/about/privacy/page.tsx
- web/app/src/app/about/refund/page.tsx
- web/app/src/app/about/terms/page.tsx
- web/app/src/middleware.ts
- web/app/tests/unit/app/legal-policy-pages.unit.spec.tsx
- web/app/tests/unit/middleware/middleware.unit.spec.ts

---

## fix(council): send dispatch hints on one line (#3280)

- sha: `1e895a1b52cd2b56389a6cab2e73eb7454c28e09`
- 作者: bill-srp
- 日期: 2026-08-06T08:12:41Z
- PR: #3280

### Commit Message

```
fix(council): send dispatch hints on one line (#3280)

## Summary

- send Council `tier:` and optional `depth:` hints on the same line as
the `/council` command
- keep quoted setting values while avoiding OpenClaw's structural-prefix
stripping of newline-prefixed `tier:` and `depth:` fields
- update the Council skill contract and message assertions for the
single-line format

## Root cause

OpenClaw's inbound preprocessing treats a new line beginning with
`name:` as a structural sender prefix. A dispatch such as `/council
topic\ntier: "standard"` therefore reached the Council skill as
`/council topic standard`. Keeping the hints on the command line
preserves their labels without changing the OpenClaw runtime.

## Testing

- `bash scripts/verify-web.sh
web/app/src/hooks/council/useCouncilActions.ts
web/app/tests/unit/hooks/council/useCouncilActions.unit.spec.tsx
web/app/tests/unit/app/council/CouncilClient.unit.spec.tsx
web/app/tests/unit/lib/council/thread-messages.unit.spec.ts`
- `bash scripts/verify-changed.sh`
- 118 targeted Council tests passed
```

### PR Body

## Summary

- send Council `tier:` and optional `depth:` hints on the same line as the `/council` command
- keep quoted setting values while avoiding OpenClaw's structural-prefix stripping of newline-prefixed `tier:` and `depth:` fields
- update the Council skill contract and message assertions for the single-line format

## Root cause

OpenClaw's inbound preprocessing treats a new line beginning with `name:` as a structural sender prefix. A dispatch such as `/council topic\ntier: "standard"` therefore reached the Council skill as `/council topic standard`. Keeping the hints on the command line preserves their labels without changing the OpenClaw runtime.

## Testing

- `bash scripts/verify-web.sh web/app/src/hooks/council/useCouncilActions.ts web/app/tests/unit/hooks/council/useCouncilActions.unit.spec.tsx web/app/tests/unit/app/council/CouncilClient.unit.spec.tsx web/app/tests/unit/lib/council/thread-messages.unit.spec.ts`
- `bash scripts/verify-changed.sh`
- 118 targeted Council tests passed


### Files

- docs/council-skill-contract.md
- web/app/src/hooks/council/useCouncilActions.ts
- web/app/tests/unit/app/council/CouncilClient.unit.spec.tsx
- web/app/tests/unit/hooks/council/useCouncilActions.unit.spec.tsx
- web/app/tests/unit/lib/council/thread-messages.unit.spec.ts

---

## fix(pricing): correct starter annual price display (#3279)

- sha: `6c1ac8ed84baba80a8f6b579d0da290194e84c46`
- 作者: shana-srp
- 日期: 2026-08-06T08:11:53Z
- PR: #3279

### Commit Message

```
fix(pricing): correct starter annual price display (#3279)

## Summary

- update the Starter annual billing display from `$20/month` to
`$17/month`
- clarify that the post-trial annual charge is `$200/year`
- leave the monthly price and Stripe billing configuration unchanged

## Testing

- `bash scripts/verify-web.sh
'src/app/[locale]/(marketing)/pricing/PublicPricingClient.tsx'
src/locales/en.ts`
- `bash scripts/verify-changed.sh`
- local `/en/pricing` preview verified successfully

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary

- update the Starter annual billing display from `$20/month` to `$17/month`
- clarify that the post-trial annual charge is `$200/year`
- leave the monthly price and Stripe billing configuration unchanged

## Testing

- `bash scripts/verify-web.sh 'src/app/[locale]/(marketing)/pricing/PublicPricingClient.tsx' src/locales/en.ts`
- `bash scripts/verify-changed.sh`
- local `/en/pricing` preview verified successfully


### Files

- web/app/src/app/[locale]/(marketing)/pricing/PublicPricingClient.tsx
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts

---

## fix(billing): enable card subscription downgrades (#3278)

- sha: `3448bd5362eb1dab919a2ef346b631be2287d745`
- 作者: tim-srp
- 日期: 2026-08-06T07:49:05Z
- PR: #3278

### Commit Message

```
fix(billing): enable card subscription downgrades (#3278)

## Summary

- remove the temporary frontend block for active Card subscription
downgrades
- route Card downgrades through the existing provider-neutral
confirmation and scheduling flow
- preserve the existing Stripe, Antom, and Apple behavior

## Why

The Creem backend already supports same-cycle downgrade scheduling
through the existing subscription downgrade endpoint. The frontend still
returned an informational toast before opening the confirmation modal,
so the backend was never called.

## Validation

- TDD regression: confirmed the Card confirmation-flow test failed
before the source change
- `pnpm exec vitest run
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` — 73
passed
- billing unit suite — 205 passed
- `bash scripts/verify-web.sh
web/app/src/components/billing/hooks/useCheckoutFlow.ts
web/app/tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` —
passed
- pre-push changed-surface gate — passed

## Staging follow-up

After deploy, resume the currently canceling Test Mode subscription,
then schedule Ultra to Pro or Starter downgrade and verify the effective
period-end state.
```

### PR Body

## Summary

- remove the temporary frontend block for active Card subscription downgrades
- route Card downgrades through the existing provider-neutral confirmation and scheduling flow
- preserve the existing Stripe, Antom, and Apple behavior

## Why

The Creem backend already supports same-cycle downgrade scheduling through the existing subscription downgrade endpoint. The frontend still returned an informational toast before opening the confirmation modal, so the backend was never called.

## Validation

- TDD regression: confirmed the Card confirmation-flow test failed before the source change
- `pnpm exec vitest run tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` — 73 passed
- billing unit suite — 205 passed
- `bash scripts/verify-web.sh web/app/src/components/billing/hooks/useCheckoutFlow.ts web/app/tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx` — passed
- pre-push changed-surface gate — passed

## Staging follow-up

After deploy, resume the currently canceling Test Mode subscription, then schedule Ultra to Pro or Starter downgrade and verify the effective period-end state.


### Files

- web/app/src/components/billing/hooks/useCheckoutFlow.ts
- web/app/tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx

---

## feat(dashboard-console): create and render org topup offline orders (#3277)

- sha: `5e320574b68703272c3fdb7083402741e602affc`
- 作者: bill-srp
- 日期: 2026-08-06T07:12:38Z
- PR: #3277

### Commit Message

```
feat(dashboard-console): create and render org topup offline orders (#3277)

## Summary
Console UI for org topup offline orders, per the spec/plan in this
branch's docs commits (backend flow merged in #3271):

- **Create dialog**: segmented order-type toggle — "Package / Plan"
(unchanged) vs "Org topup". Topup mode: UID → Load orgs (user's team
orgs only) → org select + admin-entered credits + amount; no duration.
Client-side validation mirrors backend rules; mode switches clear
mode-specific state
- **View-model**: `loadOrgs` with the same stale-lookup sequence guard
as `loadPackages`; topup payload flows through the existing
`createOfflineOrder` call (backend dispatches on `topup_credits`)
- **List**: Type badge column (Topup / Package) via
`isTopupOrder(product_type)`
- **Detail**: topup orders show Organization + credits and hide
agreement/duration/period rows; confirm/cancel dialogs and
reconciliation banner unchanged (shared endpoints)
- **Lib**: `CreateOfflineOrderInput` three-variant union (duration moves
into package/plan variants), `billing_v2.offline_topup.*` friendly error
messages, `parsePositiveInt`
- **Backend (additive)**: `_order_summary` now exposes `product_type` +
`org_id` so the console detects topup orders without inferring from
nulls; console tolerates missing `product_type` (pre-release responses
render as before)

Spec: `docs/superpowers/specs/2026-08-06-org-topup-console-design.md` ·
Plan: `docs/superpowers/plans/2026-08-06-org-topup-console.md`

## Test plan
- [x] TDD per plan task — new vitest coverage: lib helpers/error codes,
view-model `loadOrgs` (success/failure/stale) + topup submit, dialog
mode toggle/validation/payload shape, list badge, topup detail rendering
- [x] Console gate: `pnpm run typecheck` + `pnpm run test` (628 passed /
71 files) + `pnpm run lint` clean from `web/dashboard-console`
- [x] Backend: offline/billing unit set 183 passed; ruff + import-linter
clean

## Rollout
Backend field (`product_type`/`org_id` in summaries) rides the pending
claw-interface release (with #3271 and its index migration). Console
deploy is independent — it renders pre-field responses unchanged.
```

### PR Body

## Summary
Console UI for org topup offline orders, per the spec/plan in this branch's docs commits (backend flow merged in #3271):

- **Create dialog**: segmented order-type toggle — "Package / Plan" (unchanged) vs "Org topup". Topup mode: UID → Load orgs (user's team orgs only) → org select + admin-entered credits + amount; no duration. Client-side validation mirrors backend rules; mode switches clear mode-specific state
- **View-model**: `loadOrgs` with the same stale-lookup sequence guard as `loadPackages`; topup payload flows through the existing `createOfflineOrder` call (backend dispatches on `topup_credits`)
- **List**: Type badge column (Topup / Package) via `isTopupOrder(product_type)`
- **Detail**: topup orders show Organization + credits and hide agreement/duration/period rows; confirm/cancel dialogs and reconciliation banner unchanged (shared endpoints)
- **Lib**: `CreateOfflineOrderInput` three-variant union (duration moves into package/plan variants), `billing_v2.offline_topup.*` friendly error messages, `parsePositiveInt`
- **Backend (additive)**: `_order_summary` now exposes `product_type` + `org_id` so the console detects topup orders without inferring from nulls; console tolerates missing `product_type` (pre-release responses render as before)

Spec: `docs/superpowers/specs/2026-08-06-org-topup-console-design.md` · Plan: `docs/superpowers/plans/2026-08-06-org-topup-console.md`

## Test plan
- [x] TDD per plan task — new vitest coverage: lib helpers/error codes, view-model `loadOrgs` (success/failure/stale) + topup submit, dialog mode toggle/validation/payload shape, list badge, topup detail rendering
- [x] Console gate: `pnpm run typecheck` + `pnpm run test` (628 passed / 71 files) + `pnpm run lint` clean from `web/dashboard-console`
- [x] Backend: offline/billing unit set 183 passed; ruff + import-linter clean

## Rollout
Backend field (`product_type`/`org_id` in summaries) rides the pending claw-interface release (with #3271 and its index migration). Console deploy is independent — it renders pre-field responses unchanged.


### Files

- docs/superpowers/plans/2026-08-06-org-topup-console.md
- docs/superpowers/specs/2026-08-06-org-topup-console-design.md
- services/claw-interface/app/services/billing_v2/offline_order_views.py
- services/claw-interface/tests/unit/test_offline_topup_orders.py
- web/dashboard-console/app/lib/offline-orders.test.ts
- web/dashboard-console/app/lib/offline-orders.ts
- web/dashboard-console/app/routes/offline-orders/create-order-dialog.test.tsx
- web/dashboard-console/app/routes/offline-orders/create-order-dialog.tsx
- web/dashboard-console/app/routes/offline-orders/detail/route.test.tsx
- web/dashboard-console/app/routes/offline-orders/detail/route.tsx
- web/dashboard-console/app/routes/offline-orders/route.test.tsx
- web/dashboard-console/app/routes/offline-orders/route.tsx
- web/dashboard-console/app/routes/offline-orders/use-view-model.test.tsx
- web/dashboard-console/app/routes/offline-orders/use-view-model.ts

---

## feat(claw): org service tokens storage and management API (#3274)

- sha: `6cc313afd74e80731f5b9059216a642a531ed528`
- 作者: bill-srp
- 日期: 2026-08-06T07:06:00Z
- PR: #3274

### Commit Message

```
feat(claw): org service tokens storage and management API (#3274)

## Summary

**Org service tokens — token storage + management API only.** (The
`/service/v1` controld proxy that consumes these tokens is split into
the follow-up stacked PR, per review scoping.)

Implements the token half of the merged spec
(`docs/superpowers/specs/2026-08-05-org-service-tokens-design.md`) and
plan (`docs/superpowers/plans/2026-08-06-org-service-tokens-backend.md`,
Tasks 1, 3–5):

- **Storage** — `ServiceToken` schema + `ecap-service-tokens` repo
(unique `token_hash`/`token_id` indexes, org-scoped reads, CAS
revoke/rebind), lifetime registration, import-linter entries.
- **Secrets** — `zct_` + `token_urlsafe(32)` (256-bit) generation with
unique-hash retry; SHA-256 at rest (deliberate — random machine secret,
not a password; expect CodeQL `py/weak-sensitive-data-hashing` and
dismiss with the entropy rationale). Plaintext returned exactly once on
create, never stored or logged.
- **Management API** — `/orgs/{org_id}/service-tokens`: `POST` create
(bound user defaults to caller; must be an active org member), `GET`
list (metadata + prefix only), `POST {id}/revoke` (idempotent), `POST
{id}/rebind` (active tokens only; CAS-checked so a concurrent revoke
surfaces `service_token.revoked` instead of a misleading 200). GET/POST
only.
- **Authorization** — new `require_org_token_admin`: team orgs require
an active admin; personal orgs accept the active member (the owner)
since `require_org_admin` 400s personal orgs and tokens are available to
all account types. Service tokens can't manage tokens by construction
(`zct_` bearers fail JWT verification).

Implementation by Codex (gpt-5.6-luna, xhigh) from the plan.

**Follow-up PR (stacked):** engine tenancy mappings,
`require_service_token`, bound-user mint client, engine proxy transport,
the `/service/v1/{path}` catch-all with per-family tenancy + credential
seeding, and the end-to-end BDD suite.

## Test plan

- [x] Unit: repo (hash/org scoping, CAS revoke-rebind, index shapes),
service (create/revoke/rebind rules, collision retry, bound-member
validation, revoke-race conflict), routes (one-time plaintext,
delegation, GET/POST-only + gating assertions),
`require_org_token_admin` (team/personal/suspended/non-member),
enterprise wiring — 73 tests green locally.
- [x] `bash scripts/verify-py.sh` — ruff / pyright / import-linter
green.
- [ ] CI `claw-interface-quality` (authoritative coverage gate).
```

### PR Body

## Summary

**Org service tokens — token storage + management API only.** (The `/service/v1` controld proxy that consumes these tokens is split into the follow-up stacked PR, per review scoping.)

Implements the token half of the merged spec (`docs/superpowers/specs/2026-08-05-org-service-tokens-design.md`) and plan (`docs/superpowers/plans/2026-08-06-org-service-tokens-backend.md`, Tasks 1, 3–5):

- **Storage** — `ServiceToken` schema + `ecap-service-tokens` repo (unique `token_hash`/`token_id` indexes, org-scoped reads, CAS revoke/rebind), lifetime registration, import-linter entries.
- **Secrets** — `zct_` + `token_urlsafe(32)` (256-bit) generation with unique-hash retry; SHA-256 at rest (deliberate — random machine secret, not a password; expect CodeQL `py/weak-sensitive-data-hashing` and dismiss with the entropy rationale). Plaintext returned exactly once on create, never stored or logged.
- **Management API** — `/orgs/{org_id}/service-tokens`: `POST` create (bound user defaults to caller; must be an active org member), `GET` list (metadata + prefix only), `POST {id}/revoke` (idempotent), `POST {id}/rebind` (active tokens only; CAS-checked so a concurrent revoke surfaces `service_token.revoked` instead of a misleading 200). GET/POST only.
- **Authorization** — new `require_org_token_admin`: team orgs require an active admin; personal orgs accept the active member (the owner) since `require_org_admin` 400s personal orgs and tokens are available to all account types. Service tokens can't manage tokens by construction (`zct_` bearers fail JWT verification).

Implementation by Codex (gpt-5.6-luna, xhigh) from the plan.

**Follow-up PR (stacked):** engine tenancy mappings, `require_service_token`, bound-user mint client, engine proxy transport, the `/service/v1/{path}` catch-all with per-family tenancy + credential seeding, and the end-to-end BDD suite.

## Test plan

- [x] Unit: repo (hash/org scoping, CAS revoke-rebind, index shapes), service (create/revoke/rebind rules, collision retry, bound-member validation, revoke-race conflict), routes (one-time plaintext, delegation, GET/POST-only + gating assertions), `require_org_token_admin` (team/personal/suspended/non-member), enterprise wiring — 73 tests green locally.
- [x] `bash scripts/verify-py.sh` — ruff / pyright / import-linter green.
- [ ] CI `claw-interface-quality` (authoritative coverage gate).


### Files

- services/claw-interface/app/database/collections.py
- services/claw-interface/app/database/service_token_repo.py
- services/claw-interface/app/lifetime.py
- services/claw-interface/app/middleware/org.py
- services/claw-interface/app/routes/enterprise/router.py
- services/claw-interface/app/routes/enterprise/service_tokens.py
- services/claw-interface/app/schema/service_token.py
- services/claw-interface/app/services/org/service_token_service.py
- services/claw-interface/pyproject.toml
- services/claw-interface/tests/unit/_service_token_builders.py
- services/claw-interface/tests/unit/test_enterprise_wiring.py
- services/claw-interface/tests/unit/test_middleware_auth_and_org.py
- services/claw-interface/tests/unit/test_routes_service_tokens.py
- services/claw-interface/tests/unit/test_service_token_repo.py
- services/claw-interface/tests/unit/test_service_token_service.py

---

## feat(web): bot-level Auto model control + hide Auto from agent-scoped pickers (#3258)

- sha: `c772f87ae87df61a86579181dc36f431207222d7`
- 作者: siqiao-srp
- 日期: 2026-08-06T06:59:36Z
- PR: #3258

### Commit Message

```
feat(web): bot-level Auto model control + hide Auto from agent-scoped pickers (#3258)

## What

Hide the **"Auto"** router option from the agent-scoped unified chat
composer on **every** runtime.

Addresses the P1a review finding on the Auto model-router work (backend
counterpart in #3191): *"Auto is still selectable from the
computer-agent composer, but its save path is now intentionally a
no-op."*

## Why

"Auto" is a **bot-wide routing toggle** owned by the global model
setting, not an agent-scoped choice:

- On the **engine** runtime, the per-agent model save path rejects
`auto` (`agent.model_unavailable`).
- On the **computer** runtime, a per-agent `auto` write is intentionally
a **no-op** (turning Auto on is a global-settings action only).

So selecting "Auto" in the composer never does what the user expects.
Previously the composer only dropped the sentinel on the **engine**
runtime, so it was still offered — and silently a no-op — on computer
workspaces.

## Change

- Replace `filterModelsForRuntime(models, runtime)` with
`filterComposerModels(models)`, which drops the `openai/auto` sentinel
from the composer picker on **every** runtime (both the bare and
provider-qualified forms).
- The **global settings** model picker is a separate surface and still
offers "Auto" — `buildModelPickerOptions` is unchanged.

## Tests

- `composer-model-presentations.unit.spec.ts`: `filterComposerModels`
drops `auto` (bare + `openai/auto`) and leaves a plain catalog
untouched.
- `UnifiedChatComposer.unit.spec.tsx`: composer hides `auto` on **both**
computer and engine workspaces.
- Local: `tsc --noEmit` clean, `eslint` clean, composer vitest suite 112
passed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

Hide the **"Auto"** router option from the agent-scoped unified chat composer on **every** runtime.

Addresses the P1a review finding on the Auto model-router work (backend counterpart in #3191): *"Auto is still selectable from the computer-agent composer, but its save path is now intentionally a no-op."*

## Why

"Auto" is a **bot-wide routing toggle** owned by the global model setting, not an agent-scoped choice:

- On the **engine** runtime, the per-agent model save path rejects `auto` (`agent.model_unavailable`).
- On the **computer** runtime, a per-agent `auto` write is intentionally a **no-op** (turning Auto on is a global-settings action only).

So selecting "Auto" in the composer never does what the user expects. Previously the composer only dropped the sentinel on the **engine** runtime, so it was still offered — and silently a no-op — on computer workspaces.

## Change

- Replace `filterModelsForRuntime(models, runtime)` with `filterComposerModels(models)`, which drops the `openai/auto` sentinel from the composer picker on **every** runtime (both the bare and provider-qualified forms).
- The **global settings** model picker is a separate surface and still offers "Auto" — `buildModelPickerOptions` is unchanged.

## Tests

- `composer-model-presentations.unit.spec.ts`: `filterComposerModels` drops `auto` (bare + `openai/auto`) and leaves a plain catalog untouched.
- `UnifiedChatComposer.unit.spec.tsx`: composer hides `auto` on **both** computer and engine workspaces.
- Local: `tsc --noEmit` clean, `eslint` clean, composer vitest suite 112 passed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


### Files

- web/app/src/app/[locale]/(app)/claw-settings/ClawSettingsClient.tsx
- web/app/src/app/[locale]/(app)/claw-settings/components/BotModelSection.tsx
- web/app/src/components/chat/unified-chat-composer/composer-model-presentations.ts
- web/app/src/components/chat/unified-chat-composer/useComposerModelState.ts
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts
- web/app/tests/unit/app/claw-settings/BotModelSection.unit.spec.tsx
- web/app/tests/unit/components/chat/unified-chat-composer/UnifiedChatComposer.unit.spec.tsx
- web/app/tests/unit/components/chat/unified-chat-composer/composer-model-presentations.unit.spec.ts

---

## fix(model-router): drive Auto via routingMode (not model.primary=auto) (#3191)

- sha: `ddd03d2b2243a339333058e6122ff39698932b3e`
- 作者: siqiao-srp
- 日期: 2026-08-06T06:56:52Z
- PR: #3191

### Commit Message

```
fix(model-router): drive Auto via routingMode (not model.primary=auto) (#3191)

## What

Adds an **"Auto"** chat-model option that engages the
`@zooclaw/model-router` (per-run routing) instead of pinning a fixed
model. This is the **claw-interface** half of the feature; it pairs with
the model-router plugin change in **zooclaw-extras PR #210**.

### Reversed verdict: "Auto" is a routing *flag*, not a model id

The original design stored `model.primary = "auto"` as a sentinel and
expected the router to treat that as standing routing consent. **A live
staging test proved this does NOTHING**: OpenClaw core resolves `"auto"`
to a real fallback model *before* the model-router hook ever sees the
run, so the hook never observes an `"auto"` model.

The plugin (zooclaw-extras #210) now routes on the **bot-wide**
`plugins.entries.model-router.config.routingMode == "auto"` flag
instead. So this PR reworks the backend to drive that flag:

- **Picking "Auto"** sets
`plugins.entries.model-router.config.routingMode = "auto"` (via a
section-level `update_bot_config` merge) and **leaves the configured
model as a real model** — the base/fallback used when routing is off. It
does **not** write `"auto"` into `agents.defaults.model.primary`.
- **Picking a real model** writes it via the existing defaults path
**and** sets `routingMode = "default"`, so switching away from Auto
turns routing off.
- **Reading settings**: when `routingMode == "auto"`, the reported
current/primary model is surfaced as `"auto"` so the picker still shows
"Auto"; otherwise the real model is reported. `"auto"` stays in
`available_models` and keeps its plan-403 bypass.

The model-router is a single **bot-level** plugin, so `routingMode` is
bot-wide (v1: the per-agent path flips the same bot-wide flag — noted
below).

## Backend (`services/claw-interface`)

- **`services/openclaw/bot_config_payload.py`** — new read helpers
`extract_model_router_routing_mode` / `is_routing_mode_auto` and write
helper `build_routing_mode_patch`. These centralize the config-shape
knowledge (`config.plugins.entries.model-router.config.routingMode`,
handling nested-vs-flat payloads and non-string values). Also gains
`resolve_agent_ids` (moved here — see note).
- **`services/openclaw/model_routing.py`** (new) — owns the write
translation so route/service bodies stay thin:
- `apply_primary_model_selection` — the `PUT /model` write: `"auto"` →
`routingMode="auto"` only (model.primary untouched); a real model →
defaults write + `routingMode="default"`.
- `resolve_agent_model_write` / `write_agent_routing_mode` — the
agent-settings equivalents.
- **`routes/openclaw_settings/core.py`** — `update_model` delegates to
`apply_primary_model_selection` (keeps the plan-403 bypass for
`"auto"`); `get_settings` overrides the reported `primary_model` to
`"auto"` when `routingMode` is auto.
- **`services/openclaw/agent_settings_service.py`** —
`update_agent_settings` translates a `model == "auto"` patch into the
bot-wide `routingMode="auto"` flip **without pinning `"auto"` as the
agent model** (the configured model stays as the fallback); a real model
sets the model **and** `routingMode="default"`. Read paths report
`"auto"` for every agent when `routingMode` is auto.
- **`services/agents/agent_model_service.py` /
`services/model_catalog.py`** — behavior unchanged: the engine runtime
still rejects `"auto"` with an accurate `agent.model_unavailable` domain
error (no per-run routing hook there); the `/models` catalog keeps its
`"Auto"` entry.

> **File-length note:** the routingMode threading pushed `core.py` and
`agent_settings_service.py` over the 500-line CI guard, so two pure
helpers were moved to their natural homes — `resolve_agent_ids` →
`bot_config_payload.py`, `get_agent_available_channels` →
`agent_settings_channels.py`. No behavior change.

## Frontend (`web/app`)

**No frontend change needed.** The API wire contract is unchanged from
the frontend's perspective: it still sends `openai/auto` and still
receives `"auto"` / `"openai/auto"` back, both of which normalize to
"Auto". Verified end-to-end — `AgentModelSection` canonicalizes the
picker value and dirty-check, `backend-model-label` maps both forms to
"Auto", and the composer's `normalizeAgentModelId` round-trips `auto ↔
openai/auto`. The backend just does something different internally
(routingMode flag instead of a stored model id).

## Tests

Backend (all pass):
- `update_model` with `"auto"` / `"openai/auto"` writes
`routingMode="auto"` and does **not** call `update_bot_config_defaults`
(model.primary is NOT set to "auto"); a real model writes the model
**and** `routingMode="default"`.
- `get_settings` reports `primary_model == "auto"` when `routingMode` is
auto, and the real model otherwise.
- per-agent `update_agent_settings` flips the bot-wide `routingMode` and
leaves the agent model unpinned for `"auto"`; reports `"auto"` for the
agent; real models clear routing to `"default"`.
- new focused unit tests for the read/write payload helpers
(`test_bot_config_payload_routing_mode.py`).
- `agent_model_service` / `model_catalog` tests updated only for the
routingMode translation contract.

## Verification

- `bash scripts/verify-py.sh` — ruff + ruff-format + import-linter
clean; all changed source files are **pyright-clean** (0 errors). The
residual pyright failures are pre-existing local-env `favie_common` /
`pytest_bdd` / stripe-SDK / FastAPI-stub import-resolution errors in
files this PR does not touch; CI has the correct env.
- `bash scripts/verify-web.sh` — tsc + eslint clean. The 2 vitest
failures (`AssetLibraryContent`, `LegacyWorkspaceBrowser`) are
pre-existing main-line issues unrelated to this PR (backend-only
change).
- CI file-length guard passes (touched files back under 500 lines).

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

Adds an **"Auto"** chat-model option that engages the `@zooclaw/model-router` (per-run routing) instead of pinning a fixed model. This is the **claw-interface** half of the feature; it pairs with the model-router plugin change in **zooclaw-extras PR #210**.

### Reversed verdict: "Auto" is a routing *flag*, not a model id

The original design stored `model.primary = "auto"` as a sentinel and expected the router to treat that as standing routing consent. **A live staging test proved this does NOTHING**: OpenClaw core resolves `"auto"` to a real fallback model *before* the model-router hook ever sees the run, so the hook never observes an `"auto"` model.

The plugin (zooclaw-extras #210) now routes on the **bot-wide** `plugins.entries.model-router.config.routingMode == "auto"` flag instead. So this PR reworks the backend to drive that flag:

- **Picking "Auto"** sets `plugins.entries.model-router.config.routingMode = "auto"` (via a section-level `update_bot_config` merge) and **leaves the configured model as a real model** — the base/fallback used when routing is off. It does **not** write `"auto"` into `agents.defaults.model.primary`.
- **Picking a real model** writes it via the existing defaults path **and** sets `routingMode = "default"`, so switching away from Auto turns routing off.
- **Reading settings**: when `routingMode == "auto"`, the reported current/primary model is surfaced as `"auto"` so the picker still shows "Auto"; otherwise the real model is reported. `"auto"` stays in `available_models` and keeps its plan-403 bypass.

The model-router is a single **bot-level** plugin, so `routingMode` is bot-wide (v1: the per-agent path flips the same bot-wide flag — noted below).

## Backend (`services/claw-interface`)

- **`services/openclaw/bot_config_payload.py`** — new read helpers `extract_model_router_routing_mode` / `is_routing_mode_auto` and write helper `build_routing_mode_patch`. These centralize the config-shape knowledge (`config.plugins.entries.model-router.config.routingMode`, handling nested-vs-flat payloads and non-string values). Also gains `resolve_agent_ids` (moved here — see note).
- **`services/openclaw/model_routing.py`** (new) — owns the write translation so route/service bodies stay thin:
  - `apply_primary_model_selection` — the `PUT /model` write: `"auto"` → `routingMode="auto"` only (model.primary untouched); a real model → defaults write + `routingMode="default"`.
  - `resolve_agent_model_write` / `write_agent_routing_mode` — the agent-settings equivalents.
- **`routes/openclaw_settings/core.py`** — `update_model` delegates to `apply_primary_model_selection` (keeps the plan-403 bypass for `"auto"`); `get_settings` overrides the reported `primary_model` to `"auto"` when `routingMode` is auto.
- **`services/openclaw/agent_settings_service.py`** — `update_agent_settings` translates a `model == "auto"` patch into the bot-wide `routingMode="auto"` flip **without pinning `"auto"` as the agent model** (the configured model stays as the fallback); a real model sets the model **and** `routingMode="default"`. Read paths report `"auto"` for every agent when `routingMode` is auto.
- **`services/agents/agent_model_service.py` / `services/model_catalog.py`** — behavior unchanged: the engine runtime still rejects `"auto"` with an accurate `agent.model_unavailable` domain error (no per-run routing hook there); the `/models` catalog keeps its `"Auto"` entry.

> **File-length note:** the routingMode threading pushed `core.py` and `agent_settings_service.py` over the 500-line CI guard, so two pure helpers were moved to their natural homes — `resolve_agent_ids` → `bot_config_payload.py`, `get_agent_available_channels` → `agent_settings_channels.py`. No behavior change.

## Frontend (`web/app`)

**No frontend change needed.** The API wire contract is unchanged from the frontend's perspective: it still sends `openai/auto` and still receives `"auto"` / `"openai/auto"` back, both of which normalize to "Auto". Verified end-to-end — `AgentModelSection` canonicalizes the picker value and dirty-check, `backend-model-label` maps both forms to "Auto", and the composer's `normalizeAgentModelId` round-trips `auto ↔ openai/auto`. The backend just does something different internally (routingMode flag instead of a stored model id).

## Tests

Backend (all pass):
- `update_model` with `"auto"` / `"openai/auto"` writes `routingMode="auto"` and does **not** call `update_bot_config_defaults` (model.primary is NOT set to "auto"); a real model writes the model **and** `routingMode="default"`.
- `get_settings` reports `primary_model == "auto"` when `routingMode` is auto, and the real model otherwise.
- per-agent `update_agent_settings` flips the bot-wide `routingMode` and leaves the agent model unpinned for `"auto"`; reports `"auto"` for the agent; real models clear routing to `"default"`.
- new focused unit tests for the read/write payload helpers (`test_bot_config_payload_routing_mode.py`).
- `agent_model_service` / `model_catalog` tests updated only for the routingMode translation contract.

## Verification

- `bash scripts/verify-py.sh` — ruff + ruff-format + import-linter clean; all changed source files are **pyright-clean** (0 errors). The residual pyright failures are pre-existing local-env `favie_common` / `pytest_bdd` / stripe-SDK / FastAPI-stub import-resolution errors in files this PR does not touch; CI has the correct env.
- `bash scripts/verify-web.sh` — tsc + eslint clean. The 2 vitest failures (`AssetLibraryContent`, `LegacyWorkspaceBrowser`) are pre-existing main-line issues unrelated to this PR (backend-only change).
- CI file-length guard passes (touched files back under 500 lines).


### Files

- services/claw-interface/app/routes/openclaw_settings/core.py
- services/claw-interface/app/services/agents/agent_model_service.py
- services/claw-interface/app/services/model_catalog.py
- services/claw-interface/app/services/openclaw/agent_settings_channels.py
- services/claw-interface/app/services/openclaw/agent_settings_service.py
- services/claw-interface/app/services/openclaw/bot_config_payload.py
- services/claw-interface/app/services/openclaw/model_routing.py
- services/claw-interface/app/services/plan_models.py
- services/claw-interface/app/settings.py
- services/claw-interface/tests/unit/test_agent_model_service.py
- services/claw-interface/tests/unit/test_agent_settings_effective_model.py
- services/claw-interface/tests/unit/test_bot_config_payload_routing_mode.py
- services/claw-interface/tests/unit/test_model_catalog.py
- services/claw-interface/tests/unit/test_openclaw_settings_routes.py

---

## ci: switch release-notify Claude generation to Microsoft Foundry (#3275)

- sha: `892b65aff11c220f12b57b1e0511bdbc7a5154a9`
- 作者: bill-srp
- 日期: 2026-08-06T06:44:37Z
- PR: #3275

### Commit Message

```
ci: switch release-notify Claude generation to Microsoft Foundry (#3275)

## Summary

Follow-up to #3269: move the release-notify Claude generation step off
AWS Bedrock and onto Microsoft Foundry (Azure), by opting the caller
into the `provider: foundry` path that the shared `srp-actions`
`release-notify-lark.yml` reusable already supports (same
provider-validation script as `claude-review.yaml`, byte-identical by
test).

- Add `provider: foundry` to the `notify` job's `with:` block — the only
functional change.
- `secrets: inherit` already forwards `AZURE_OPENAI_API_KEY` (the same
repo secret used by the `codex-review` and, since #3269, `claude-review`
jobs), and the reusable's default `foundry_base_url` points at the
shared `srp-openai-cicd-resource` Anthropic endpoint, so no new secrets
or vars are needed.
- `bedrock_model` stays empty → provider-aware default resolves to the
`claude-sonnet-4-6` Foundry deployment, the same model tier the workflow
used on Bedrock (`us.anthropic.claude-sonnet-4-6`).
- Update the permissions comment: `id-token: write` is unused on the
Foundry path but the reusable still declares it, and a caller may not
grant fewer permissions than the reusable declares (same treatment as
#3269 / zooclaw-engine#619).

## Test plan

- [x] YAML parse check on the edited workflow
- [x] Verified against the reusable's contract (fetched from
`srp-actions@main`): `provider: foundry` + inherited
`AZURE_OPENAI_API_KEY` + default `foundry_base_url` satisfy the
"Validate Claude provider configuration" step with no Bedrock fallback
warning
- [ ] Live verification happens on the next release: `workflow_dispatch`
with `dry_run: true` on any existing `*-release` tag can exercise the
Foundry generation path without sending a Lark message

## Notes

- If the Foundry path misbehaves, reverting this one input restores the
historical Bedrock behavior; the reusable also auto-falls-back to
Bedrock (with a warning) if the Azure key were ever removed while
`AWS_ROLE_TO_ASSUME` still exists.
```

### PR Body

## Summary

Follow-up to #3269: move the release-notify Claude generation step off AWS Bedrock and onto Microsoft Foundry (Azure), by opting the caller into the `provider: foundry` path that the shared `srp-actions` `release-notify-lark.yml` reusable already supports (same provider-validation script as `claude-review.yaml`, byte-identical by test).

- Add `provider: foundry` to the `notify` job's `with:` block — the only functional change.
- `secrets: inherit` already forwards `AZURE_OPENAI_API_KEY` (the same repo secret used by the `codex-review` and, since #3269, `claude-review` jobs), and the reusable's default `foundry_base_url` points at the shared `srp-openai-cicd-resource` Anthropic endpoint, so no new secrets or vars are needed.
- `bedrock_model` stays empty → provider-aware default resolves to the `claude-sonnet-4-6` Foundry deployment, the same model tier the workflow used on Bedrock (`us.anthropic.claude-sonnet-4-6`).
- Update the permissions comment: `id-token: write` is unused on the Foundry path but the reusable still declares it, and a caller may not grant fewer permissions than the reusable declares (same treatment as #3269 / zooclaw-engine#619).

## Test plan

- [x] YAML parse check on the edited workflow
- [x] Verified against the reusable's contract (fetched from `srp-actions@main`): `provider: foundry` + inherited `AZURE_OPENAI_API_KEY` + default `foundry_base_url` satisfy the "Validate Claude provider configuration" step with no Bedrock fallback warning
- [ ] Live verification happens on the next release: `workflow_dispatch` with `dry_run: true` on any existing `*-release` tag can exercise the Foundry generation path without sending a Lark message

## Notes

- If the Foundry path misbehaves, reverting this one input restores the historical Bedrock behavior; the reusable also auto-falls-back to Bedrock (with a warning) if the Azure key were ever removed while `AWS_ROLE_TO_ASSUME` still exists.


### Files

- .github/workflows/release-notify-lark.yml

---

## fix(web): hide all legacy Claw UI after V2 migration (#3273)

- sha: `0e2b9ca8f56a1784d5d2d984f8b3c50270d92879`
- 作者: kaka-srp
- 日期: 2026-08-06T06:27:50Z
- PR: #3273

### Commit Message

```
fix(web): hide all legacy Claw UI after V2 migration (#3273)

## Summary

- hide the shared legacy Claw connection status on every authenticated
page once canonical Main uses the Engine runtime
- resolve runtime ownership once in the persistent app layout so
page-header remounts do not refetch `/agents` or flicker for legacy
users
- keep failed ownership lookups in an explicit unknown state instead of
falling back to legacy UI
- show only Engine-configurable Channel platforms after migration while
preserving every legacy platform before migration

## Root cause

The first V2 migration cleanup only hid Claw status and operational
pages in Channel and Settings. Other pages still rendered the shared
`ClawPageHeader`, whose legacy connection control had no migration-aware
ownership gate.

A first follow-up placed ownership resolution inside each page header.
Because the unified agents query deliberately revalidates on mount, that
approach added a request on route changes and temporarily hid then
restored the status for unmigrated users. It also treated a terminal
agents-query error as confirmed legacy ownership.

This change moves the ownership observer to the persistent authenticated
app layout and exposes a narrow context to all headers. Ownership is now
`unknown`, `legacy`, or `engine`; legacy controls render only after
legacy ownership is positively confirmed.

## Performance

- native V2 users still short-circuit from the Engine onboarding
snapshot without an agents request
- existing accounts use one app-layout ownership observer rather than
one observer per page header
- page navigation no longer causes header-owned `/agents` revalidation
or connection-status flicker
- Channel retains its feature-specific agents observer because it needs
the actual Engine workspace list; concurrent initial observers share the
same React Query request

## Test plan

- [x] `bash scripts/verify-web.sh <19 changed frontend paths>` after
merging current `origin/main`
- [x] 19 targeted test files: 237 passed, 66 existing skips
- [x] `bash scripts/verify-changed.sh`
- [x] TypeScript, ESLint, import-boundary, dead-code, and diff checks
- [x] full Vitest run: 8298 passed; two unrelated concurrent
timeout/hydration failures passed when rerun independently (48/48 and
8/8)
```

### PR Body

## Summary

- hide the shared legacy Claw connection status on every authenticated page once canonical Main uses the Engine runtime
- resolve runtime ownership once in the persistent app layout so page-header remounts do not refetch `/agents` or flicker for legacy users
- keep failed ownership lookups in an explicit unknown state instead of falling back to legacy UI
- show only Engine-configurable Channel platforms after migration while preserving every legacy platform before migration

## Root cause

The first V2 migration cleanup only hid Claw status and operational pages in Channel and Settings. Other pages still rendered the shared `ClawPageHeader`, whose legacy connection control had no migration-aware ownership gate.

A first follow-up placed ownership resolution inside each page header. Because the unified agents query deliberately revalidates on mount, that approach added a request on route changes and temporarily hid then restored the status for unmigrated users. It also treated a terminal agents-query error as confirmed legacy ownership.

This change moves the ownership observer to the persistent authenticated app layout and exposes a narrow context to all headers. Ownership is now `unknown`, `legacy`, or `engine`; legacy controls render only after legacy ownership is positively confirmed.

## Performance

- native V2 users still short-circuit from the Engine onboarding snapshot without an agents request
- existing accounts use one app-layout ownership observer rather than one observer per page header
- page navigation no longer causes header-owned `/agents` revalidation or connection-status flicker
- Channel retains its feature-specific agents observer because it needs the actual Engine workspace list; concurrent initial observers share the same React Query request

## Test plan

- [x] `bash scripts/verify-web.sh <19 changed frontend paths>` after merging current `origin/main`
- [x] 19 targeted test files: 237 passed, 66 existing skips
- [x] `bash scripts/verify-changed.sh`
- [x] TypeScript, ESLint, import-boundary, dead-code, and diff checks
- [x] full Vitest run: 8298 passed; two unrelated concurrent timeout/hydration failures passed when rerun independently (48/48 and 8/8)


### Files

- web/app/src/app/[locale]/(app)/channels/ChannelsPageClient.tsx
- web/app/src/app/[locale]/(app)/channels/components/ChannelsSection.tsx
- web/app/src/app/[locale]/(app)/channels/components/channels/PlatformCards.tsx
- web/app/src/app/[locale]/(app)/claw-settings/ClawSettingsClient.tsx
- web/app/src/app/[locale]/(app)/layout.tsx
- web/app/src/components/ClawPageHeader.tsx
- web/app/src/components/providers/ClawRuntimeOwnershipProvider.tsx
- web/app/src/contexts/ClawRuntimeOwnershipContext.tsx
- web/app/src/hooks/useClawRuntimeOwnership.ts
- web/app/tests/unit/app/app-group-layout.unit.spec.tsx
- web/app/tests/unit/app/channels/ChannelsPageClient.unit.spec.tsx
- web/app/tests/unit/app/claw-settings/ChannelsSection-engine.unit.spec.tsx
- web/app/tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx
- web/app/tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx
- web/app/tests/unit/app/plugins/PluginsClient.unit.spec.tsx
- web/app/tests/unit/components/ClawPageHeader-extras.unit.spec.tsx
- web/app/tests/unit/components/ClawPageHeader.unit.spec.ts
- web/app/tests/unit/components/providers/ClawRuntimeOwnershipProvider.unit.spec.tsx
- web/app/tests/unit/hooks/useClawRuntimeOwnership.unit.spec.ts

---

## feat(claw-interface): grant org topup credits to the team topup wallet via offline orders (#3271)

- sha: `f0275124639456f470697c749a48133c22095867`
- 作者: bill-srp
- 日期: 2026-08-06T06:12:12Z
- PR: #3271

### Commit Message

```
feat(claw-interface): grant org topup credits to the team topup wallet via offline orders (#3271)

## Summary
Implements org topup offline orders per the merged spec/plan (#3270):
admins can sell an org one-time credits through `POST
/internal/offline-order/create` + `/confirm`, granting into the org's
team **topup** wallet on Billing Gateway (`customer_id =
Org.billing_team_id`).

- New `app/services/billing_v2/offline_topup_orders.py` lifecycle
(create/confirm) reusing the shared payment-order primitives (confirm
lease, bank-reference claim, audit, entitlement ledger); the
subscription confirm path is untouched — routes dispatch by
`product_type`
- Create preconditions: team org with `billing_team_id`, active
membership for `uid`, **effective** enterprise agreement
(`get_effective_enterprise_for_team(team_id, now_ts=...)` — status +
unexpired period, re-checked at confirm)
- Confirm state machine: GRANTING entitlement → BG grant (deduped via
`bg_grant_transaction_id`) → CAS order `succeeded` → flip entitlement
ACTIVE → audit; every crash state repairs by re-running confirm, no
compensation path needed
- Fulfillment: new team-topup branch (`access_kind=topup_credits` +
`team_id`) requires exactly one live team subscription, resolves/creates
the active `topup` wallet on BG (source of truth; `Org.wallet_topup_id`
refreshed as cache), grants credits — no model-tier changes
- `record_payment_entitlement` gains `org_id`; new partial unique index
`unique_pending_offline_topup_order_per_org` closes the
concurrent-create race; cancel guard and console detail view are
topup-aware
- v1 scope per spec: no revoke of succeeded topups, no expiry
(`effective_end=None`), backend only

Spec: `docs/superpowers/specs/2026-08-06-org-topup-design.md` · Plan:
`docs/superpowers/plans/2026-08-06-org-topup.md` (intentional deviations
documented in the plan)

## Test plan
- [x] TDD per plan task — 45 new unit tests across
`test_offline_topup_orders.py` (create preconditions, confirm
idempotency states, dispatch, cancel guard),
`test_billing_v2_fulfillment.py` (wallet resolve/create,
live-subscription requirement), `test_billing_v2_entitlements.py`
(`org_id`), `test_offline_orders_routes.py` (request-shape validation)
- [x] Full offline/billing unit set: 181 passed
- [x] `bash scripts/verify-py.sh` clean (ruff + ruff-format + pyright +
import-linter)


## Rollout (required)

This PR adds the Mongo partial unique index
`unique_pending_offline_topup_order_per_org` on `ecap-payment-orders`.
Billing v2 indexes are **not** created at app startup — before exposing
the org-topup flow, run in each target environment (staging, then
production):

```
python -m scripts.ensure_billing_v2_indexes
```

Until the index exists, the one-pending-topup-per-org guard relies only
on the read-then-create check, which has a concurrency window under
simultaneous admin creates. (Flagged by Codex review; the script already
covers the new index via `payment_order_repo.ensure_indexes()`.)
```

### PR Body

## Summary
Implements org topup offline orders per the merged spec/plan (#3270): admins can sell an org one-time credits through `POST /internal/offline-order/create` + `/confirm`, granting into the org's team **topup** wallet on Billing Gateway (`customer_id = Org.billing_team_id`).

- New `app/services/billing_v2/offline_topup_orders.py` lifecycle (create/confirm) reusing the shared payment-order primitives (confirm lease, bank-reference claim, audit, entitlement ledger); the subscription confirm path is untouched — routes dispatch by `product_type`
- Create preconditions: team org with `billing_team_id`, active membership for `uid`, **effective** enterprise agreement (`get_effective_enterprise_for_team(team_id, now_ts=...)` — status + unexpired period, re-checked at confirm)
- Confirm state machine: GRANTING entitlement → BG grant (deduped via `bg_grant_transaction_id`) → CAS order `succeeded` → flip entitlement ACTIVE → audit; every crash state repairs by re-running confirm, no compensation path needed
- Fulfillment: new team-topup branch (`access_kind=topup_credits` + `team_id`) requires exactly one live team subscription, resolves/creates the active `topup` wallet on BG (source of truth; `Org.wallet_topup_id` refreshed as cache), grants credits — no model-tier changes
- `record_payment_entitlement` gains `org_id`; new partial unique index `unique_pending_offline_topup_order_per_org` closes the concurrent-create race; cancel guard and console detail view are topup-aware
- v1 scope per spec: no revoke of succeeded topups, no expiry (`effective_end=None`), backend only

Spec: `docs/superpowers/specs/2026-08-06-org-topup-design.md` · Plan: `docs/superpowers/plans/2026-08-06-org-topup.md` (intentional deviations documented in the plan)

## Test plan
- [x] TDD per plan task — 45 new unit tests across `test_offline_topup_orders.py` (create preconditions, confirm idempotency states, dispatch, cancel guard), `test_billing_v2_fulfillment.py` (wallet resolve/create, live-subscription requirement), `test_billing_v2_entitlements.py` (`org_id`), `test_offline_orders_routes.py` (request-shape validation)
- [x] Full offline/billing unit set: 181 passed
- [x] `bash scripts/verify-py.sh` clean (ruff + ruff-format + pyright + import-linter)


## Rollout (required)

This PR adds the Mongo partial unique index `unique_pending_offline_topup_order_per_org` on `ecap-payment-orders`. Billing v2 indexes are **not** created at app startup — before exposing the org-topup flow, run in each target environment (staging, then production):

```
python -m scripts.ensure_billing_v2_indexes
```

Until the index exists, the one-pending-topup-per-org guard relies only on the read-then-create check, which has a concurrency window under simultaneous admin creates. (Flagged by Codex review; the script already covers the new index via `payment_order_repo.ensure_indexes()`.)


### Files

- services/claw-interface/app/database/billing_index_utils.py
- services/claw-interface/app/database/entitlement_ledger_repo.py
- services/claw-interface/app/database/payment_order_lifecycle_repo.py
- services/claw-interface/app/database/payment_order_repo.py
- services/claw-interface/app/routes/internal/offline_order.py
- services/claw-interface/app/services/billing_v2/entitlements.py
- services/claw-interface/app/services/billing_v2/fulfillment.py
- services/claw-interface/app/services/billing_v2/offline_order_cancellations.py
- services/claw-interface/app/services/billing_v2/offline_order_views.py
- services/claw-interface/app/services/billing_v2/offline_orders.py
- services/claw-interface/app/services/billing_v2/offline_topup_orders.py
- services/claw-interface/app/services/billing_v2/team_wallets.py
- services/claw-interface/tests/unit/test_billing_v2_entitlements.py
- services/claw-interface/tests/unit/test_billing_v2_fulfillment.py
- services/claw-interface/tests/unit/test_billing_v2_repos.py
- services/claw-interface/tests/unit/test_offline_orders_routes.py
- services/claw-interface/tests/unit/test_offline_topup_orders.py

---

## fix(plugins): polish connector catalog cards (#3266)

- sha: `82fbe074f03866fcb7f8abc56953ce9d9a32b3b2`
- 作者: shana-srp
- 日期: 2026-08-06T05:42:05Z
- PR: #3266

### Commit Message

```
fix(plugins): polish connector catalog cards (#3266)

## Summary
- Remove the connector loading/empty status box from the plugins page.
- Add consistent 36px provider logos with frontend-owned local assets
and fallbacks for the first coming-soon providers.
- Replace raw provider notes with concise localized descriptions for
common providers.
- Polish provider cards and switch the top-level plugin tabs to a
segmented control.

## Root cause
Unknown providers fell back to inconsistent initials, loading and empty
provider states rendered as an unnecessary bordered box, and the
tab/card treatments were visually inconsistent.

Provider logos are intentionally frontend-owned. This PR does not add or
depend on a backend `logo_url` field.

## Test plan
- [x] TypeScript `tsc --noEmit`
- [x] 53 targeted Vitest tests for PluginsClient, ProviderLogo, and
ComposioConnectorsClient
- [x] ESLint and frontend pre-push verification
- [x] Python ruff, ruff-format, and pyright pre-commit hooks
- [ ] Full CI checks after the latest push

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
- Remove the connector loading/empty status box from the plugins page.
- Add consistent 36px provider logos with frontend-owned local assets and fallbacks for the first coming-soon providers.
- Replace raw provider notes with concise localized descriptions for common providers.
- Polish provider cards and switch the top-level plugin tabs to a segmented control.

## Root cause
Unknown providers fell back to inconsistent initials, loading and empty provider states rendered as an unnecessary bordered box, and the tab/card treatments were visually inconsistent.

Provider logos are intentionally frontend-owned. This PR does not add or depend on a backend `logo_url` field.

## Test plan
- [x] TypeScript `tsc --noEmit`
- [x] 53 targeted Vitest tests for PluginsClient, ProviderLogo, and ComposioConnectorsClient
- [x] ESLint and frontend pre-push verification
- [x] Python ruff, ruff-format, and pyright pre-commit hooks
- [ ] Full CI checks after the latest push


### Files

- web/app/public/images/provider-logos/1password.svg
- web/app/public/images/provider-logos/21risk.svg
- web/app/public/images/provider-logos/2chat.svg
- web/app/public/images/provider-logos/ably.svg
- web/app/public/images/provider-logos/abstract.svg
- web/app/public/images/provider-logos/abuseipdb.svg
- web/app/public/images/provider-logos/abyssale.svg
- web/app/public/images/provider-logos/accredible.svg
- web/app/public/images/provider-logos/acculynx.svg
- web/app/public/images/provider-logos/activecampaign.svg
- web/app/public/images/provider-logos/activetrail.svg
- web/app/public/images/provider-logos/addressfinder.svg
- web/app/scripts/mock-backend/scenarios.mjs
- web/app/src/app/[locale]/(app)/plugins/PluginsClient.tsx
- web/app/src/components/ProviderLogo.tsx
- web/app/src/components/composio-connectors/ComposioConnectorsClient.tsx
- web/app/src/components/composio-connectors/components/ProviderCard.tsx
- web/app/src/locales/en.ts
- web/app/src/locales/zh.ts
- web/app/tests/unit/components/ProviderLogo.unit.spec.tsx
- web/app/tests/unit/components/composio-connectors/ComposioConnectorsClient.unit.spec.tsx

---

## docs: add org service tokens design spec and implementation plans (#3272)

- sha: `e919314863760b3eee0665e73af8d406199e50ba`
- 作者: bill-srp
- 日期: 2026-08-06T05:40:02Z
- PR: #3272

### Commit Message

```
docs: add org service tokens design spec and implementation plans (#3272)

## Summary

Docs-only PR: the approved design spec plus the two implementation plans
for **org service tokens** — long-lived `zct_` API credentials that let
org customers manage ZooClaw engine agents programmatically through an
authenticated controld proxy.

### Spec (v3, revised 2026-08-06)

`docs/superpowers/specs/2026-08-05-org-service-tokens-design.md`

- Service API = **auth + controld proxy only**: `/service/v1/{path}` →
engine `/v1/{path}`, all `/v1/*` pass-through, no ECAP-side re-modeling
(supersedes the earlier persona+skills lifecycle API).
- Gateway-enforced tenancy per resource family (ownership rewrite on
create, `agent_id → org` mapping, forced skills/environments anchors,
tenant-hiding 404s, unknown families 404).
- Engine-only agents (no `AgentWorkspace` docs, no ECAP UI visibility);
credential auto-seeding (LiteLLM billing key + minted bound-user token)
as the one non-proxy seam.
- Token model: `zct_` + 256-bit secret, SHA-256 at rest, no
scopes/expiry — revocation is the v1 kill switch; bound-user identity
with admin rebind.

### Plans

`docs/superpowers/plans/2026-08-06-org-service-tokens-backend.md` — 14
TDD tasks for `services/claw-interface`: schema/repos
(+import-linter/lifetime wiring), token service,
`require_org_token_admin` (personal-org owner variant), management
routes under `/orgs/{org_id}/service-tokens`, `require_service_token`
with throttled `last_used_at`, mint client (fails closed until the
user-interface endpoint + secret exist), engine-client `ProxyMixin`, the
`/service/v1` router with per-family tenancy modules, credential
auto-seeding, BDD + full gate.


`docs/superpowers/plans/2026-08-06-org-service-tokens-enterprise-admin.md`
— 4 tasks for `web/enterprise-admin`: types/hooks/view-model, admin-only
nav + `/tokens` route guard, token components (table, create dialog with
bound-member picker, one-time secret reveal with copy), page assembly +
vitest coverage.

Plan-phase verification items from the spec were resolved during
planning research: controld list-agents has no in-repo evidence (stays
404 in v1), per-id environment selector filtering moves to staging
smoke, agent-GET ownership stays on the mapping collection, and
multipart/stream forwarding mechanics are pinned to the existing engine
transport primitives.

## Test plan

- [ ] Docs-only — no code changes; CI is path-filtered so only
lightweight checks run.
- [ ] Implementation follows in separate PRs per the plans (backend
first, then enterprise-admin; user-interface mint endpoint is
cross-repo).
```

### PR Body

## Summary

Docs-only PR: the approved design spec plus the two implementation plans for **org service tokens** — long-lived `zct_` API credentials that let org customers manage ZooClaw engine agents programmatically through an authenticated controld proxy.

### Spec (v3, revised 2026-08-06)

`docs/superpowers/specs/2026-08-05-org-service-tokens-design.md`

- Service API = **auth + controld proxy only**: `/service/v1/{path}` → engine `/v1/{path}`, all `/v1/*` pass-through, no ECAP-side re-modeling (supersedes the earlier persona+skills lifecycle API).
- Gateway-enforced tenancy per resource family (ownership rewrite on create, `agent_id → org` mapping, forced skills/environments anchors, tenant-hiding 404s, unknown families 404).
- Engine-only agents (no `AgentWorkspace` docs, no ECAP UI visibility); credential auto-seeding (LiteLLM billing key + minted bound-user token) as the one non-proxy seam.
- Token model: `zct_` + 256-bit secret, SHA-256 at rest, no scopes/expiry — revocation is the v1 kill switch; bound-user identity with admin rebind.

### Plans

`docs/superpowers/plans/2026-08-06-org-service-tokens-backend.md` — 14 TDD tasks for `services/claw-interface`: schema/repos (+import-linter/lifetime wiring), token service, `require_org_token_admin` (personal-org owner variant), management routes under `/orgs/{org_id}/service-tokens`, `require_service_token` with throttled `last_used_at`, mint client (fails closed until the user-interface endpoint + secret exist), engine-client `ProxyMixin`, the `/service/v1` router with per-family tenancy modules, credential auto-seeding, BDD + full gate.

`docs/superpowers/plans/2026-08-06-org-service-tokens-enterprise-admin.md` — 4 tasks for `web/enterprise-admin`: types/hooks/view-model, admin-only nav + `/tokens` route guard, token components (table, create dialog with bound-member picker, one-time secret reveal with copy), page assembly + vitest coverage.

Plan-phase verification items from the spec were resolved during planning research: controld list-agents has no in-repo evidence (stays 404 in v1), per-id environment selector filtering moves to staging smoke, agent-GET ownership stays on the mapping collection, and multipart/stream forwarding mechanics are pinned to the existing engine transport primitives.

## Test plan

- [ ] Docs-only — no code changes; CI is path-filtered so only lightweight checks run.
- [ ] Implementation follows in separate PRs per the plans (backend first, then enterprise-admin; user-interface mint endpoint is cross-repo).


### Files

- docs/superpowers/plans/2026-08-06-org-service-tokens-backend.md
- docs/superpowers/plans/2026-08-06-org-service-tokens-enterprise-admin.md
- docs/superpowers/specs/2026-08-05-org-service-tokens-design.md

---

## docs: add org topup design spec and implementation plan (#3270)

- sha: `822740ac813283d1fe3b8e5942538bed879bc223`
- 作者: bill-srp
- 日期: 2026-08-06T03:40:09Z
- PR: #3270

### Commit Message

```
docs: add org topup design spec and implementation plan (#3270)

## Summary
- Add the approved design spec for org topup: offline orders that grant
one-time credits into the org's team **topup** wallet on Billing Gateway
(`docs/superpowers/specs/2026-08-06-org-topup-design.md`)
- Add the task-by-task implementation plan
(`docs/superpowers/plans/2026-08-06-org-topup.md`)

Key decisions captured in the spec:
- Trigger is the internal offline-order flow (create/confirm), not
self-serve Stripe/Antom
- Credit amount is admin-entered (`topup_credits` + `amount_cents`), no
coupling to `TOPUP_PACKS`
- Org must have an active enterprise agreement (topup credits are
otherwise unusable)
- No revoke of succeeded topups in v1; no expiry; backend only

The plan implements this as a dedicated `offline_topup_orders.py`
lifecycle module reusing the existing payment-order primitives (confirm
lease, bank-reference claim, audit, entitlement ledger) plus a
team-topup grant branch in `billing_v2/fulfillment.py`. Three
intentional deviations from the spec are documented at the end of the
plan (discovery-first wallet resolution, pending-topup-per-org unique
index, ACTIVE-flip-after-CAS ordering).

## Test plan
- [x] Docs only — no code changes; implementation PRs will follow the
plan with TDD
```

### PR Body

## Summary
- Add the approved design spec for org topup: offline orders that grant one-time credits into the org's team **topup** wallet on Billing Gateway (`docs/superpowers/specs/2026-08-06-org-topup-design.md`)
- Add the task-by-task implementation plan (`docs/superpowers/plans/2026-08-06-org-topup.md`)

Key decisions captured in the spec:
- Trigger is the internal offline-order flow (create/confirm), not self-serve Stripe/Antom
- Credit amount is admin-entered (`topup_credits` + `amount_cents`), no coupling to `TOPUP_PACKS`
- Org must have an active enterprise agreement (topup credits are otherwise unusable)
- No revoke of succeeded topups in v1; no expiry; backend only

The plan implements this as a dedicated `offline_topup_orders.py` lifecycle module reusing the existing payment-order primitives (confirm lease, bank-reference claim, audit, entitlement ledger) plus a team-topup grant branch in `billing_v2/fulfillment.py`. Three intentional deviations from the spec are documented at the end of the plan (discovery-first wallet resolution, pending-topup-per-org unique index, ACTIVE-flip-after-CAS ordering).

## Test plan
- [x] Docs only — no code changes; implementation PRs will follow the plan with TDD


### Files

- docs/superpowers/plans/2026-08-06-org-topup.md
- docs/superpowers/specs/2026-08-06-org-topup-design.md

---

## fix(web): hide legacy Claw surfaces for V2 users (#3268)

- sha: `89350c6f4f689e0a980cec2c34446d593f02089e`
- 作者: kaka-srp
- 日期: 2026-08-06T03:28:18Z
- PR: #3268

### Commit Message

```
fix(web): hide legacy Claw surfaces for V2 users (#3268)

## Summary
- detect Claw-independent accounts from the uid-scoped Engine onboarding
state or a freshly revalidated canonical Main Engine agent
- hide the legacy Claw connection control on Channel and Settings, and
remove Status, Sessions, and Statistics Dashboard for V2 users
- keep Engine channel management available without synthetic Claw
targets, start warnings, restart prompts, or legacy settings/runtime
requests
- preserve Usage plan allocation while disabling and masking legacy Claw
resource data, including cached values

## Root cause
Channel and Settings mounted legacy Claw state and operational pages
unconditionally. The UI did not distinguish native or migrated Engine
accounts from accounts whose canonical Main agent still uses the
computer runtime, so V2 users saw disconnected Claw controls and could
trigger legacy runtime/settings requests.

## Performance
- native Engine Settings short-circuits without an ownership agent
request
- Channel reuses one unified agent query instead of mounting a second
agent-list observer
- no polling was added; legacy settings, computer, init, and resource
queries remain disabled for Claw-independent accounts

## Test plan
- [x] `bash scripts/verify-web.sh <16 changed frontend paths>`
- [x] TypeScript and ESLint
- [x] 16 targeted test files: 308 passed, 66 existing skips
- [x] `bash scripts/verify-changed.sh` after merging current
`origin/main`
- [x] local code review, including a regression test for non-empty
cached Claw resources in Engine mode
```

### PR Body

## Summary
- detect Claw-independent accounts from the uid-scoped Engine onboarding state or a freshly revalidated canonical Main Engine agent
- hide the legacy Claw connection control on Channel and Settings, and remove Status, Sessions, and Statistics Dashboard for V2 users
- keep Engine channel management available without synthetic Claw targets, start warnings, restart prompts, or legacy settings/runtime requests
- preserve Usage plan allocation while disabling and masking legacy Claw resource data, including cached values

## Root cause
Channel and Settings mounted legacy Claw state and operational pages unconditionally. The UI did not distinguish native or migrated Engine accounts from accounts whose canonical Main agent still uses the computer runtime, so V2 users saw disconnected Claw controls and could trigger legacy runtime/settings requests.

## Performance
- native Engine Settings short-circuits without an ownership agent request
- Channel reuses one unified agent query instead of mounting a second agent-list observer
- no polling was added; legacy settings, computer, init, and resource queries remain disabled for Claw-independent accounts

## Test plan
- [x] `bash scripts/verify-web.sh <16 changed frontend paths>`
- [x] TypeScript and ESLint
- [x] 16 targeted test files: 308 passed, 66 existing skips
- [x] `bash scripts/verify-changed.sh` after merging current `origin/main`
- [x] local code review, including a regression test for non-empty cached Claw resources in Engine mode


### Files

- web/app/src/app/[locale]/(app)/channels/ChannelsPageClient.tsx
- web/app/src/app/[locale]/(app)/channels/components/ChannelsSection.tsx
- web/app/src/app/[locale]/(app)/channels/components/channels/helpers.ts
- web/app/src/app/[locale]/(app)/claw-settings/ClawSettingsClient.tsx
- web/app/src/app/[locale]/(app)/claw-settings/components/UsageTab.tsx
- web/app/src/contexts/OpenClawContext.tsx
- web/app/src/hooks/queries/agents/useAgents.ts
- web/app/src/hooks/useClawRuntimeOwnership.ts
- web/app/tests/unit/app/channels/ChannelsPageClient.unit.spec.tsx
- web/app/tests/unit/app/claw-settings/ChannelsSection.unit.spec.tsx
- web/app/tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx
- web/app/tests/unit/app/claw-settings/helpers.unit.spec.ts
- web/app/tests/unit/components/claw-settings/UsageTab.unit.spec.tsx
- web/app/tests/unit/contexts/OpenClawContext.unit.spec.tsx
- web/app/tests/unit/hooks/queries/agents/useAgentsOnCurrentComputer.unit.spec.tsx
- web/app/tests/unit/hooks/useClawRuntimeOwnership.unit.spec.ts

---

## ci: switch claude-review to Microsoft Foundry (#3269)

- sha: `a1e44816fdd28ed87507b02c41077745c1e3f777`
- 作者: bill-srp
- 日期: 2026-08-06T03:14:50Z
- PR: #3269

### Commit Message

```
ci: switch claude-review to Microsoft Foundry (#3269)

## Summary

Mirrors SerendipityOneInc/zooclaw-engine#619 in this repo: move the
`claude-review` job in `.github/workflows/auto-review.yaml` off the
temporary Bedrock fallback and onto Microsoft Foundry, the default
provider of the shared `srp-actions` `claude-review.yaml` reusable since
srp-actions#125.

- `model: us.anthropic.claude-sonnet-5` → `claude-sonnet-5` (Foundry
deployment name; this repo keeps its sonnet-5 + `effort: medium` choice
rather than zooclaw-engine's opus-4-8)
- secrets: `AWS_ROLE_TO_ASSUME` → `AZURE_OPENAI_API_KEY` (same secret
the sibling `codex-review` job already uses, so it is known to exist in
this repo)

Previously the reusable saw only `AWS_ROLE_TO_ASSUME` and fell back to
Bedrock with a per-run migration warning; after this change it runs
Claude review against the shared `srp-openai-cicd-resource` Foundry
endpoint.

## Test plan

- [x] YAML parse check on the edited workflow
- [x] Verified against the reusable's contract: `provider` defaults to
`foundry`, `AZURE_OPENAI_API_KEY` + default `foundry_base_url` satisfy
the provider validation step, and the model string is passed through as
the Foundry deployment name
- [ ] This PR's own `auto-review / claude-review` run is the live
verification that the `claude-sonnet-5` Foundry deployment works
(workflow config is taken from the PR branch)

## Notes / follow-ups

- `claude-arch-review.yaml`, `docs-maintenance.yml`,
`claude-develop.yaml`, and `claude-assistant.yaml` still use Bedrock
(`us.anthropic.*` + `AWS_ROLE_TO_ASSUME`); they are direct
`claude-code-action` users, not callers of the migrated reusable, and
are left for a separate migration if desired.
- The `id-token: write` permission on `claude-review` is now unused on
the Foundry path but harmless (zooclaw-engine#619 also kept it).
```

### PR Body

## Summary

Mirrors SerendipityOneInc/zooclaw-engine#619 in this repo: move the `claude-review` job in `.github/workflows/auto-review.yaml` off the temporary Bedrock fallback and onto Microsoft Foundry, the default provider of the shared `srp-actions` `claude-review.yaml` reusable since srp-actions#125.

- `model: us.anthropic.claude-sonnet-5` → `claude-sonnet-5` (Foundry deployment name; this repo keeps its sonnet-5 + `effort: medium` choice rather than zooclaw-engine's opus-4-8)
- secrets: `AWS_ROLE_TO_ASSUME` → `AZURE_OPENAI_API_KEY` (same secret the sibling `codex-review` job already uses, so it is known to exist in this repo)

Previously the reusable saw only `AWS_ROLE_TO_ASSUME` and fell back to Bedrock with a per-run migration warning; after this change it runs Claude review against the shared `srp-openai-cicd-resource` Foundry endpoint.

## Test plan

- [x] YAML parse check on the edited workflow
- [x] Verified against the reusable's contract: `provider` defaults to `foundry`, `AZURE_OPENAI_API_KEY` + default `foundry_base_url` satisfy the provider validation step, and the model string is passed through as the Foundry deployment name
- [ ] This PR's own `auto-review / claude-review` run is the live verification that the `claude-sonnet-5` Foundry deployment works (workflow config is taken from the PR branch)

## Notes / follow-ups

- `claude-arch-review.yaml`, `docs-maintenance.yml`, `claude-develop.yaml`, and `claude-assistant.yaml` still use Bedrock (`us.anthropic.*` + `AWS_ROLE_TO_ASSUME`); they are direct `claude-code-action` users, not callers of the migrated reusable, and are left for a separate migration if desired.
- The `id-token: write` permission on `claude-review` is now unused on the Foundry path but harmless (zooclaw-engine#619 also kept it).


### Files

- .github/workflows/auto-review.yaml

---

## fix(web): restore same-origin HTML previews (#3262)

- sha: `0cd643f14d74c417edb13ded0a6d360d895a2ff9`
- 作者: sam-srp
- 日期: 2026-08-06T02:44:22Z
- PR: #3262

### Commit Message

```
fix(web): restore same-origin HTML previews (#3262)

## What changed

- restore `allow-same-origin` on the HTML artifact preview iframe;
- update the renderer contract test to require the restored sandbox
capability.

## Why

HTML artifacts that use browser storage can fail during initialization
inside the current sandbox. For example, a generated 2048 game reads
`localStorage` for its high score before building the board; without
`allow-same-origin`, the browser throws a `SecurityError` and leaves the
preview partially rendered.

## Impact

Interactive HTML artifacts can access browser storage again and render
consistently with opening the HTML directly.

## Security tradeoff

This intentionally restores same-origin capability to script-enabled
artifact HTML. In particular, private workspace files rendered through
blob URLs need a follow-up design that moves HTML execution to an
isolated, cookie-less preview origin before the sandbox can be tightened
again safely.

## Validation

- `pnpm exec tsc --noEmit`
- `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/components/artifacts/renderers/HtmlRenderer.unit.spec.tsx` (4
tests passed)
- targeted ESLint
- pre-push changed-surface verification
```

### PR Body

## What changed

- restore `allow-same-origin` on the HTML artifact preview iframe;
- update the renderer contract test to require the restored sandbox capability.

## Why

HTML artifacts that use browser storage can fail during initialization inside the current sandbox. For example, a generated 2048 game reads `localStorage` for its high score before building the board; without `allow-same-origin`, the browser throws a `SecurityError` and leaves the preview partially rendered.

## Impact

Interactive HTML artifacts can access browser storage again and render consistently with opening the HTML directly.

## Security tradeoff

This intentionally restores same-origin capability to script-enabled artifact HTML. In particular, private workspace files rendered through blob URLs need a follow-up design that moves HTML execution to an isolated, cookie-less preview origin before the sandbox can be tightened again safely.

## Validation

- `pnpm exec tsc --noEmit`
- `pnpm exec vitest run --config ./vitest.config.mts tests/unit/components/artifacts/renderers/HtmlRenderer.unit.spec.tsx` (4 tests passed)
- targeted ESLint
- pre-push changed-surface verification


### Files

- web/app/src/components/artifacts/renderers/HtmlRenderer.tsx
- web/app/tests/unit/components/artifacts/renderers/HtmlRenderer.unit.spec.tsx

---

## fix(billing): recover Creem upgrade handoff (#3267)

- sha: `2b6d0aea2108c03a4ebcbc611b8c54bf99a7d0db`
- 作者: tim-srp
- 日期: 2026-08-06T02:26:49Z
- PR: #3267

### Commit Message

```
fix(billing): recover Creem upgrade handoff (#3267)
```

### PR Body

## Summary

- recover Creem same-cycle upgrade handoff when the existing Billing v2 Agreement omits the default `cancel_at_period_end` field
- default an active Card subscription to its asynchronously loaded current billing cycle until the user explicitly selects another cycle
- preserve the existing yearly default for new subscriptions, Stripe, and Antom, and preserve cross-cycle fail-closed behavior
- record the real staging Test Mode upgrade result and the exact post-deploy replay check

## Root cause

The real staging Test Mode payment succeeded and created the Ultra order, 40,000-credit entitlement, and new Agreement. The atomic replacement handoff then failed with `billing.creem.replacement_current_changed`.

The existing Pro Agreement is a valid sparse Billing v2 document without a stored `cancel_at_period_end` field. Upgrade admission already treats missing/null/false as not canceled, but the handoff CAS converted a missing field to literal `false` and required that literal field in Mongo. The query therefore matched no document.

The first UI correction also exposed a separate loading edge: `useBillingCredits` starts empty and resolves asynchronously. A one-time state initializer still left a monthly Card subscriber on the yearly default. The final implementation derives the Card cycle from loaded subscription state until the user makes an explicit selection.

## Scope

- Creem replacement handoff only on the backend
- Card subscription cycle selection only on the frontend
- no Stripe, Antom, product catalog, API contract, schema, or database migration changes

## Test plan

- [x] TDD: backend regression failed on literal `false`, then passed with the non-true CAS condition
- [x] TDD: frontend regression failed across empty-to-loaded billing context, then passed with derived Card cycle state
- [x] replacement-focused backend unit tests: 55 passed
- [x] all Creem/Card backend unit tests: 555 passed
- [x] SubscriptionPanel tests: 73 passed
- [x] frontend selected verification: TypeScript, Vitest, ESLint passed
- [x] backend verification: Ruff check/format, Pyright, import-linter passed
- [x] changed-surface pre-push gate passed
- [x] independent code review found no remaining blocker or non-blocking issue

## Staging evidence and follow-up

On staging revision `461ab48d5`, Creem Test Mode accepted the Pro Monthly to Ultra Monthly payment. The local order reached `succeeded`, the deterministic Ultra entitlement reached `active`, and 40,000 credits were granted once. The new Agreement remained `current=false` while the old Pro Agreement remained current because the handoff CAS failed.

After this fix is deployed to staging, replay the original signed `subscription.paid` event through Creem automatic retry or dashboard resend. Verify that the new Ultra Agreement becomes current, the old Pro subscription is scheduled for cancellation, the order projection is attached, and no duplicate credit grant occurs. Do not create another checkout for the partially settled payment.


### Files

- docs/staging-validation/2026-08-05-creem-card-rollout.md
- services/claw-interface/app/services/creem/checkout_replacement.py
- services/claw-interface/tests/unit/test_creem_checkout_replacement.py
- web/app/src/components/billing/SubscriptionPanel.tsx
- web/app/tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx

---

