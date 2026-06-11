# SerendipityOneInc/ecap-workspace commits — 2026-06-10

共 31 个 commits

---

## chore(logging): claw-interface adopts favie-common v0.3.65 + removes double-logging root handler (#2355)

- **SHA**: `1b80d8808b93901da135f08d5cca80822c4eac0c`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T15:56:54Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/1b80d8808b93901da135f08d5cca80822c4eac0c
- **PR**: #2355

### 完整 Commit Message

```
chore(logging): claw-interface adopts favie-common v0.3.65 + removes double-logging root handler (#2355)

## Summary

Phase 2 of [ECA-954](https://linear.app/srpone/issue/ECA-954) for
**claw-interface**: eliminate residual unstructured GCP `textPayload`
logs by adopting the shared `favie-common` v0.3.65 logging toolkit,
mirroring the already-merged billing-gateway PR #52.

- **favie-helper adoption** (`app/app_logging.py`): replace the local
`_suppress_noisy_loggers()` / `_NOISY_LOGGERS` with the shared helpers.
`configure_logging()` now runs `configure_structured_logging()` →
`route_uvicorn_to_structured_root()` →
`quiet_noisy_loggers(extra=<LiteLLM/openai>)` →
`install_sensitive_data_filter()`, keeping the one-shot idempotency
guard.
- **httpx kept structured**: httpx is intentionally NOT included in
`extra=` and NOT quieted — at INFO it propagates to the structured root
as the request-correlated record of outbound LLM/tool calls, which is
valuable.
- **Removes the double-logging root handler**: `logging.yaml` carried an
**active** `root: handlers: [console]` block that double-logged every
app record (once structured via the favie root handler, once plain via
the console handler) — confirmed in production. `logging.yaml` is
deleted, and the `COPY ./logging.yaml` line + `--log-config
logging.yaml` are removed from the Dockerfile `ENTRYPOINT`.
- **ECA-516 canary preserved**: `_route_resource_warnings_to_logger()`
(the aiohttp "Unclosed client session" leak canary with tracemalloc
allocation traceback) is unchanged and still called in
`configure_logging()` — it is a separate diagnostic, not part of this
cleanup.
- **Re-pin** `favie-common` → `@v0.3.65` in `requirements.txt`.
- **Tests**: `tests/unit/test_app_logging.py` updated to assert the
favie helpers + canary are wired (with idempotency guard) and that httpx
is not quieted; all existing resource-warnings tests preserved.

## Test plan
- [x] venv install of claw-interface requirements +
favie-common@v0.3.65; new favie symbols import OK (`favie-common`
reports `0.3.65`)
- [x] `pytest tests/unit/test_app_logging.py` → 12 passed
- [x] `ruff check` + `ruff format --check` on changed files → clean
- [x] `py_compile` changed modules → OK
- [x] `grep -rn` confirms no remaining `logging.yaml` / `--log-config`
references

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Phase 2 of [ECA-954](https://linear.app/srpone/issue/ECA-954) for **claw-interface**: eliminate residual unstructured GCP `textPayload` logs by adopting the shared `favie-common` v0.3.65 logging toolkit, mirroring the already-merged billing-gateway PR #52.

- **favie-helper adoption** (`app/app_logging.py`): replace the local `_suppress_noisy_loggers()` / `_NOISY_LOGGERS` with the shared helpers. `configure_logging()` now runs `configure_structured_logging()` → `route_uvicorn_to_structured_root()` → `quiet_noisy_loggers(extra=<LiteLLM/openai>)` → `install_sensitive_data_filter()`, keeping the one-shot idempotency guard.
- **httpx kept structured**: httpx is intentionally NOT included in `extra=` and NOT quieted — at INFO it propagates to the structured root as the request-correlated record of outbound LLM/tool calls, which is valuable.
- **Removes the double-logging root handler**: `logging.yaml` carried an **active** `root: handlers: [console]` block that double-logged every app record (once structured via the favie root handler, once plain via the console handler) — confirmed in production. `logging.yaml` is deleted, and the `COPY ./logging.yaml` line + `--log-config logging.yaml` are removed from the Dockerfile `ENTRYPOINT`.
- **ECA-516 canary preserved**: `_route_resource_warnings_to_logger()` (the aiohttp "Unclosed client session" leak canary with tracemalloc allocation traceback) is unchanged and still called in `configure_logging()` — it is a separate diagnostic, not part of this cleanup.
- **Re-pin** `favie-common` → `@v0.3.65` in `requirements.txt`.
- **Tests**: `tests/unit/test_app_logging.py` updated to assert the favie helpers + canary are wired (with idempotency guard) and that httpx is not quieted; all existing resource-warnings tests preserved.

## Test plan
- [x] venv install of claw-interface requirements + favie-common@v0.3.65; new favie symbols import OK (`favie-common` reports `0.3.65`)
- [x] `pytest tests/unit/test_app_logging.py` → 12 passed
- [x] `ruff check` + `ruff format --check` on changed files → clean
- [x] `py_compile` changed modules → OK
- [x] `grep -rn` confirms no remaining `logging.yaml` / `--log-config` references

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(auth): verify tokens against ecap business (#2358)

- **SHA**: `c5137ddfa6585ea75a6d79c60c68fc6ccaa9c053`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T15:27:47Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c5137ddfa6585ea75a6d79c60c68fc6ccaa9c053
- **PR**: #2358

### 完整 Commit Message

```
fix(auth): verify tokens against ecap business (#2358)

## Summary

- Send `business=ecap` when `claw-interface` verifies user tokens
through `user-interface`.
- Add a unit test that locks the verifier request to
`/auth/verify?business=ecap`.

## Tests

- `services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_auth.py -q`
- `services/claw-interface/.venv/bin/python -m ruff check
services/claw-interface/app/auth/token_verifier.py
services/claw-interface/tests/unit/test_auth.py`
- `services/claw-interface/.venv/bin/python -m ruff format --check
services/claw-interface/app/auth/token_verifier.py
services/claw-interface/tests/unit/test_auth.py`
```

### PR Body

## Summary

- Send `business=ecap` when `claw-interface` verifies user tokens through `user-interface`.
- Add a unit test that locks the verifier request to `/auth/verify?business=ecap`.

## Tests

- `services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_auth.py -q`
- `services/claw-interface/.venv/bin/python -m ruff check services/claw-interface/app/auth/token_verifier.py services/claw-interface/tests/unit/test_auth.py`
- `services/claw-interface/.venv/bin/python -m ruff format --check services/claw-interface/app/auth/token_verifier.py services/claw-interface/tests/unit/test_auth.py`


---

## fix(web): fetch replay shares from backend (#2356)

- **SHA**: `3e369e603bffdce841acef098126cb0abca71695`
- **作者**: kaka-srp
- **日期**: 2026-06-10T14:47:47Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3e369e603bffdce841acef098126cb0abca71695
- **PR**: #2356

### 完整 Commit Message

```
fix(web): fetch replay shares from backend (#2356)

## Summary
- Route public replay share SSR through claw-interface directly instead
of self-fetching the public `/api` route.
- Preserve unavailable UI only for backend 404/revoked shares; surface
other upstream or routing failures through the error boundary.
- Add unit coverage for backend URL encoding, CF Access headers, 404
handling, non-JSON HTML fallback, and abort signals.

## Root cause
Staging Worker SSR fetches to its own custom domain
`/api/chat-replays/:id` could resolve through Cloudflare zone routing
and return the app HTML fallback. The share page caught that as a
generic fetch failure and rendered “This replay is no longer available,”
even though the backend replay record existed.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/lib/api/chat-replay-server.unit.spec.ts
tests/unit/lib/api/chat-replay-api.unit.spec.ts`
- [x] `pnpm exec eslint 'src/app/share/[shareId]/page.tsx'
src/lib/api/chat-replay-server.ts
tests/unit/lib/api/chat-replay-server.unit.spec.ts --quiet`\n- [x] `pnpm
exec tsc --noEmit`\n- [x] commit hook frontend lint\n
```

### PR Body

## Summary
- Route public replay share SSR through claw-interface directly instead of self-fetching the public `/api` route.
- Preserve unavailable UI only for backend 404/revoked shares; surface other upstream or routing failures through the error boundary.
- Add unit coverage for backend URL encoding, CF Access headers, 404 handling, non-JSON HTML fallback, and abort signals.

## Root cause
Staging Worker SSR fetches to its own custom domain `/api/chat-replays/:id` could resolve through Cloudflare zone routing and return the app HTML fallback. The share page caught that as a generic fetch failure and rendered “This replay is no longer available,” even though the backend replay record existed.

## Test plan
- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/lib/api/chat-replay-server.unit.spec.ts tests/unit/lib/api/chat-replay-api.unit.spec.ts`
- [x] `pnpm exec eslint 'src/app/share/[shareId]/page.tsx' src/lib/api/chat-replay-server.ts tests/unit/lib/api/chat-replay-server.unit.spec.ts --quiet`\n- [x] `pnpm exec tsc --noEmit`\n- [x] commit hook frontend lint\n

---

## fix(auth): add Turnstile to ECAP phone login (#2352)

- **SHA**: `3d9b8341a42098fc7c788cbb8164661441b46817`
- **作者**: tim-srp
- **日期**: 2026-06-10T13:32:32Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3d9b8341a42098fc7c788cbb8164661441b46817
- **PR**: #2352

### 完整 Commit Message

```
fix(auth): add Turnstile to ECAP phone login (#2352)

## Summary
- Extends Cloudflare Turnstile (added to Google login in #2339) to
phone-number login. Same env flag
`NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED` gates both — email OTP
is intentionally excluded.
- Gate is at `handlePhoneSubmit` (before SMS send), not after OTP verify
— adds a user-visible captcha layer on top of Firebase's invisible
reCAPTCHA so SMS bombing through our UI requires solving Turnstile per
attempt. Solved token is stashed in
`sessionStorage['ecap:phone-login:captcha-token']` and forwarded to
`loginUser → /auth/exchange` on the verify page, mirroring the mobile
Google-redirect pattern.
- Backend support already in user-interface `v0.6.5-release` (PR
`SerendipityOneInc/user-interface#124`, deployed to production today).

## Root cause
The phone-login surface previously had **no user-visible captcha** —
only Firebase's invisible reCAPTCHA on `sendSMSVerification`, which
protects Firebase but not our `/auth/exchange` backend, and not against
SMS bombing where attackers iterate phone numbers through our login
page. PR #2339 closed this gap for Google login; this PR closes it for
phone.

Also fixes a #983-style half-login bug on `/user/verify` (phone branch):
`saveLoginInfo` ran **before** `loginUser`, so a thrown exchange would
leave a Firebase profile in `localStorage` with no backend session.
Adding captcha makes `loginUser` more likely to fail in production
(expired single-use Turnstile token, etc.), so this reorder ships
together. The same bug pattern on the email-magic-link path is left for
a separate PR — out of scope here.

## Test plan
- [x] `pnpm tsc --noEmit` — only stale `.next/types/validator.ts` cache
errors, none from touched source.
- [x] `pnpm eslint <touched files>` — clean.
- [x] `pnpm vitest run tests/unit/components/LoginForm.unit.spec.tsx` —
48/48 pass (44 existing + 4 new phone-captcha cases: flag-off baseline,
unsolved token blocks SMS, solved token persisted, Firebase error wipes
token + resets widget).
- [ ] Local manual smoke with mock backend + Cloudflare test sitekey
(`1x00000000000000000000AA`): walk phone login end-to-end on desktop +
mobile UA, confirm captcha required → SMS sent → exchange carries
`captcha_token`.
- [ ] Staging: backend flag off, frontend flag on — phone login should
succeed with `captcha_token` visible in `/auth/exchange` payload and
backend should ignore it (gradual rollout step 2 of the spec).
- [ ] After staging green: turn on backend
`ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED=true` per spec step 3 (covers both
Google + phone).

## Spec
docs/superpowers/specs/2026-06-10-ecap-phone-login-turnstile.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- Extends Cloudflare Turnstile (added to Google login in #2339) to phone-number login. Same env flag `NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED` gates both — email OTP is intentionally excluded.
- Gate is at `handlePhoneSubmit` (before SMS send), not after OTP verify — adds a user-visible captcha layer on top of Firebase's invisible reCAPTCHA so SMS bombing through our UI requires solving Turnstile per attempt. Solved token is stashed in `sessionStorage['ecap:phone-login:captcha-token']` and forwarded to `loginUser → /auth/exchange` on the verify page, mirroring the mobile Google-redirect pattern.
- Backend support already in user-interface `v0.6.5-release` (PR `SerendipityOneInc/user-interface#124`, deployed to production today).

## Root cause
The phone-login surface previously had **no user-visible captcha** — only Firebase's invisible reCAPTCHA on `sendSMSVerification`, which protects Firebase but not our `/auth/exchange` backend, and not against SMS bombing where attackers iterate phone numbers through our login page. PR #2339 closed this gap for Google login; this PR closes it for phone.

Also fixes a #983-style half-login bug on `/user/verify` (phone branch): `saveLoginInfo` ran **before** `loginUser`, so a thrown exchange would leave a Firebase profile in `localStorage` with no backend session. Adding captcha makes `loginUser` more likely to fail in production (expired single-use Turnstile token, etc.), so this reorder ships together. The same bug pattern on the email-magic-link path is left for a separate PR — out of scope here.

## Test plan
- [x] `pnpm tsc --noEmit` — only stale `.next/types/validator.ts` cache errors, none from touched source.
- [x] `pnpm eslint <touched files>` — clean.
- [x] `pnpm vitest run tests/unit/components/LoginForm.unit.spec.tsx` — 48/48 pass (44 existing + 4 new phone-captcha cases: flag-off baseline, unsolved token blocks SMS, solved token persisted, Firebase error wipes token + resets widget).
- [ ] Local manual smoke with mock backend + Cloudflare test sitekey (`1x00000000000000000000AA`): walk phone login end-to-end on desktop + mobile UA, confirm captcha required → SMS sent → exchange carries `captcha_token`.
- [ ] Staging: backend flag off, frontend flag on — phone login should succeed with `captcha_token` visible in `/auth/exchange` payload and backend should ignore it (gradual rollout step 2 of the spec).
- [ ] After staging green: turn on backend `ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED=true` per spec step 3 (covers both Google + phone).

## Spec
docs/superpowers/specs/2026-06-10-ecap-phone-login-turnstile.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## ci: update wrangler action to Node 24 (#2350)

- **SHA**: `9f8e1754a8df3e7f1e2139bc384578af14dce36e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T13:02:08Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9f8e1754a8df3e7f1e2139bc384578af14dce36e
- **PR**: #2350

### 完整 Commit Message

```
ci: update wrangler action to Node 24 (#2350)

## Summary
- Update Cloudflare deploy steps from `cloudflare/wrangler-action@v3` to
`@v4` so GitHub Actions runs the action on Node.js 24 instead of
deprecated Node.js 20.
- Cover the ECAP, dashboard console, R2 access worker, and enterprise
admin deploy workflows.

## Test plan
- [x] `rg -n "cloudflare/wrangler-action@v3" .github/workflows` returns
no active workflow matches.
- [x] `rg -n "cloudflare/wrangler-action@v4" .github/workflows` shows
the 4 deploy workflow uses.
- [x] `git diff --check`
- [x] `actionlint .github/workflows/deploy.yml
.github/workflows/deploy-dashboard-console.yml
.github/workflows/deploy-r2-access-worker.yml
.github/workflows/deploy-enterprise-admin.yml` attempted; it is blocked
by existing repository warnings for Blacksmith runner labels and
existing shellcheck findings, not by this tag-only change.
```

### PR Body

## Summary
- Update Cloudflare deploy steps from `cloudflare/wrangler-action@v3` to `@v4` so GitHub Actions runs the action on Node.js 24 instead of deprecated Node.js 20.
- Cover the ECAP, dashboard console, R2 access worker, and enterprise admin deploy workflows.

## Test plan
- [x] `rg -n "cloudflare/wrangler-action@v3" .github/workflows` returns no active workflow matches.
- [x] `rg -n "cloudflare/wrangler-action@v4" .github/workflows` shows the 4 deploy workflow uses.
- [x] `git diff --check`
- [x] `actionlint .github/workflows/deploy.yml .github/workflows/deploy-dashboard-console.yml .github/workflows/deploy-r2-access-worker.yml .github/workflows/deploy-enterprise-admin.yml` attempted; it is blocked by existing repository warnings for Blacksmith runner labels and existing shellcheck findings, not by this tag-only change.

---

## fix(claw-interface): sync plan disk limits to bots (#2338)

- **SHA**: `05f46229708a837756797f71ecbb037d98f64772`
- **作者**: tim-srp
- **日期**: 2026-06-10T12:43:55Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/05f46229708a837756797f71ecbb037d98f64772
- **PR**: #2338

### 完整 Commit Message

```
fix(claw-interface): sync plan disk limits to bots (#2338)

## Summary
- Include plan disk limits in bot resource deployment sync payloads.
- Add regression coverage for Starter/Free, Pro, and Ultra disk limits.
- Add coverage that /resources overrides Ultra disk display to the plan
limit.

## Root cause
`sync_bot_resources()` reused `PLAN_RESOURCES` but only copied CPU and
memory into `deployment.resources.limits`, so plan upgrades could leave
the running bot disk limit behind even though creation and /resources
display knew about `disk_limit`.

Linear:
https://linear.app/srpone/issue/ECA-953/ultra-%E7%94%A8%E6%88%B7%E7%A3%81%E7%9B%98%E5%AE%B9%E9%87%8F%E6%98%BE%E7%A4%BA%E4%B8%BA-40gb%E9%9C%80%E4%B8%8E%E8%AE%A2%E9%98%85%E9%9D%A2%E6%9D%BF%E5%B1%95%E7%A4%BA%E4%BF%9D%E6%8C%81%E4%B8%80%E8%87%B4

## Test plan
- [x] `pytest -W ignore::PendingDeprecationWarning
services/claw-interface/tests/unit/test_bot_resources.py
services/claw-interface/tests/unit/test_openclaw_settings_routes.py -q
-k "bot_resources or GetBotResources"`
- [x] `ruff check app/services/bot_resources.py
tests/unit/test_bot_resources.py
tests/unit/test_openclaw_settings_routes.py`
- [x] `pyright -p pyproject.toml app/services/bot_resources.py`
- [x] `ruff check .`

## Notes
- Full `pyright -p pyproject.toml app tests` is blocked in this local
environment by unresolved third-party imports such as `fastapi`,
`pytest`, and `favie_common`; scoped pyright for the changed app module
passes.
- Full `pytest --cov=app --cov-report=term-missing --cov-fail-under=90
-q` was stopped after unrelated existing failures appeared
(`test_unauthenticated_websocket_rejected_e2e`, CORS preflight tests)
and it continued running beyond 35%.
```

### PR Body

## Summary
- Include plan disk limits in bot resource deployment sync payloads.
- Add regression coverage for Starter/Free, Pro, and Ultra disk limits.
- Add coverage that /resources overrides Ultra disk display to the plan limit.

## Root cause
`sync_bot_resources()` reused `PLAN_RESOURCES` but only copied CPU and memory into `deployment.resources.limits`, so plan upgrades could leave the running bot disk limit behind even though creation and /resources display knew about `disk_limit`.

Linear: https://linear.app/srpone/issue/ECA-953/ultra-%E7%94%A8%E6%88%B7%E7%A3%81%E7%9B%98%E5%AE%B9%E9%87%8F%E6%98%BE%E7%A4%BA%E4%B8%BA-40gb%E9%9C%80%E4%B8%8E%E8%AE%A2%E9%98%85%E9%9D%A2%E6%9D%BF%E5%B1%95%E7%A4%BA%E4%BF%9D%E6%8C%81%E4%B8%80%E8%87%B4

## Test plan
- [x] `pytest -W ignore::PendingDeprecationWarning services/claw-interface/tests/unit/test_bot_resources.py services/claw-interface/tests/unit/test_openclaw_settings_routes.py -q -k "bot_resources or GetBotResources"`
- [x] `ruff check app/services/bot_resources.py tests/unit/test_bot_resources.py tests/unit/test_openclaw_settings_routes.py`
- [x] `pyright -p pyproject.toml app/services/bot_resources.py`
- [x] `ruff check .`

## Notes
- Full `pyright -p pyproject.toml app tests` is blocked in this local environment by unresolved third-party imports such as `fastapi`, `pytest`, and `favie_common`; scoped pyright for the changed app module passes.
- Full `pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` was stopped after unrelated existing failures appeared (`test_unauthenticated_websocket_rejected_e2e`, CORS preflight tests) and it continued running beyond 35%.

---

## fix(web): render openclaw reaction emoji (#2351)

- **SHA**: `d75798e249e7dfa2e8b1ac5d2ae114f9f5c3dbfb`
- **作者**: sam-srp
- **日期**: 2026-06-10T12:15:55Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d75798e249e7dfa2e8b1ac5d2ae114f9f5c3dbfb
- **PR**: #2351

### 完整 Commit Message

```
fix(web): render openclaw reaction emoji (#2351)

## Summary
- add frontend mappings for OpenClaw status reaction emoji names
- cover the newer Mattermost reaction names with a unit test

## Root Cause
Mattermost reactions arrive as emoji names such as `white_check_mark`.
The chat UI only mapped a subset of older names, so unknown names
rendered as fallback text like `:white_check_mark:`.

## Validation
- `pnpm exec vitest run
tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx`
```

### PR Body

## Summary
- add frontend mappings for OpenClaw status reaction emoji names
- cover the newer Mattermost reaction names with a unit test

## Root Cause
Mattermost reactions arrive as emoji names such as `white_check_mark`. The chat UI only mapped a subset of older names, so unknown names rendered as fallback text like `:white_check_mark:`.

## Validation
- `pnpm exec vitest run tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx`

---

## chore(claw-interface): expose vertical pack plan details (#2348)

- **SHA**: `3025e945c12ea3a319c5570959edbae49b62ab69`
- **作者**: bill-srp
- **日期**: 2026-06-10T12:15:02Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3025e945c12ea3a319c5570959edbae49b62ab69
- **PR**: #2348

### 完整 Commit Message

```
chore(claw-interface): expose vertical pack plan details (#2348)

## Summary
- add public GET /vertical-pack-plans/{plan_id} route without auth
- return vertical pack plan details with referenced active zooclaw agent
packs resolved
- add batch pack lookup via pack_id $in query

## Tests
- cd services/claw-interface &&
/Users/bill/.venvs/claw-interface/bin/ruff format --check .
- cd services/claw-interface &&
/Users/bill/.venvs/claw-interface/bin/ruff check .
- cd services/claw-interface &&
/Users/bill/.venvs/claw-interface/bin/pyright --pythonpath
/Users/bill/.venvs/claw-interface/bin/python app tests
- cd services/claw-interface &&
/Users/bill/.venvs/claw-interface/bin/pytest
tests/unit/test_internal_vertical_pack_plans_routes.py
tests/unit/test_vertical_pack_plans_routes.py
tests/unit/test_pack_repo.py -q
```

### PR Body

## Summary
- add public GET /vertical-pack-plans/{plan_id} route without auth
- return vertical pack plan details with referenced active zooclaw agent packs resolved
- add batch pack lookup via pack_id $in query

## Tests
- cd services/claw-interface && /Users/bill/.venvs/claw-interface/bin/ruff format --check .
- cd services/claw-interface && /Users/bill/.venvs/claw-interface/bin/ruff check .
- cd services/claw-interface && /Users/bill/.venvs/claw-interface/bin/pyright --pythonpath /Users/bill/.venvs/claw-interface/bin/python app tests
- cd services/claw-interface && /Users/bill/.venvs/claw-interface/bin/pytest tests/unit/test_internal_vertical_pack_plans_routes.py tests/unit/test_vertical_pack_plans_routes.py tests/unit/test_pack_repo.py -q

---

## ci(release): limit frontend notify filter to web app (#2349)

- **SHA**: `71a0b82e9054f4689c73d817dd295dde14059c76`
- **作者**: bill-srp
- **日期**: 2026-06-10T11:57:21Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/71a0b82e9054f4689c73d817dd295dde14059c76
- **PR**: #2349

### 完整 Commit Message

```
ci(release): limit frontend notify filter to web app (#2349)

## Summary
- Limit the frontend release-notify Lark path filter from `web/` to
`web/app/` so only web app code changes are included in frontend release
notifications.

## Test plan
- [x] `ruby -e 'require "yaml";
YAML.load_file(".github/workflows/release-notify-lark.yml"); puts "ok"'`
- [x] Confirmed `actionlint` is not installed locally
```

### PR Body

## Summary
- Limit the frontend release-notify Lark path filter from `web/` to `web/app/` so only web app code changes are included in frontend release notifications.

## Test plan
- [x] `ruby -e 'require "yaml"; YAML.load_file(".github/workflows/release-notify-lark.yml"); puts "ok"'`
- [x] Confirmed `actionlint` is not installed locally

---

## fix(web): replace nested markdown hydration roots with segment rendering (ECA-765) (#2337)

- **SHA**: `abc14b6baf7d6c184f035dceda1f520870998567`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T11:43:29Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/abc14b6baf7d6c184f035dceda1f520870998567
- **PR**: #2337

### 完整 Commit Message

```
fix(web): replace nested markdown hydration roots with segment rendering (ECA-765) (#2337)

## Summary
- 根治 Sentry ECA-765(\`removeChild\` / \`insertBefore\` NotFoundError):消灭
\`MarkdownContent\` 的"\`dangerouslySetInnerHTML\` + 嵌套 \`createRoot\`"双
React root 反模式
- 新增 token 级分段渲染:\`parse-markdown-segments\` 在顶层 code fence 处切分文档,ERMP /
specialist 卡片成为主树的**真 React 子组件**(\`ERMPCardSegment\` /
\`SpecialistCardSlot\`,\`next/dynamic\` 懒加载保持 code-split),其余 token 段沿用现有
marked renderer 输出 per-segment sanitized HTML
- 取代并关闭止血 PR #2327;设计 spec 见
\`docs/superpowers/specs/2026-06-10-markdown-segment-rendering.md\`

## Root cause
外层 React tree 通过 \`dangerouslySetInnerHTML\` 拥有整段消息 HTML,hydration
effect 又用 \`createRoot()\` 往这段 HTML 内部的占位 div 挂嵌套 root——同一块 DOM 被两个 root
管理。流式输出时 content 每 token 一变:外层 root 在 **mutation 阶段**重写 innerHTML 铲掉嵌套
root 的 host 节点,嵌套 root 的 \`unmount()\` 在更晚的 **passive
阶段**才执行,此时其子节点已不在树上 → NotFoundError。

实现中还发现一个放大因素:**React 19 对 \`dangerouslySetInnerHTML\` 按对象身份 diff**(不比较
\`__html\` 字符串),内联 \`{{__html}}\` 字面量导致任何父级 re-render 都无条件重写
innerHTML——旧代码的触发面远不止 content 变化。新实现用 \`React.memo\` 的 \`HtmlSegment\`
让相同 html 字符串直接 bail out(load-bearing,非优化),流式时未变段 DOM 零重写。

行为变化台账(详见 spec):
1. \`suppressSpecialistCards\` 从 \`display:none\` 占位 div 变为不渲染(等价,数据在
React state 不需 DOM 占位存活)
2. 嵌套(blockquote/list 内)卡片 fence 从不可见空 div 退化为**可见** code
block(契约:卡片只在顶层 fence)
3. raw-HTML 注入的占位 div 不再是 hydration 向量;\`data-ermp-*\` / \`data-zc-*\`
移出 DOMPurify allowlist(src 内零 producer)
4. 卡片 payload 不再 encodeURIComponent 往返 DOM 属性

## Test plan
- [x] characterization 锁(重构前提交,跨重构原封不动通过):ERMP
happy/invalid、unknown-kind / 空 agent-id 降级、混合消息、**ERMP 流式挂载(ECA-765
触发场景)**、跨 fence reference 链接
- [x] 分段器单测含等价性属性测试:无卡片输入的分段输出与 \`renderMarkdownToHtml\` 字节级相同
- [x] ECA-765 专属回归:流式追加时前段 DOM **节点引用恒等**;卡片挂载中整体替换 content 正常卸载不抛错
- [x] 全量 unit suite 7023 passed / \`tsc --noEmit\` / \`pnpm lint\` /
\`pnpm dup\` 全过(\`react-hooks-config\` lint-contract 测试在本机全量并行下偶发 10s
超时,隔离运行通过,与本 diff 无交集)
- [ ] 手测:\`/chat\` 流式含 \`\`\`ecap-card 消息无控制台错误、卡片可交互;\`/new-chat\` →
session thread;hire/fire consent i18n 消息组装;图片 blur / file card / 视频缩略图 /
shiki / 分享回放
- [ ] 合并上线后观察 Sentry ECA-765:新增 NotFoundError 应归零(残留即浏览器扩展噪声,可借此区分归因)

后续 follow-up(不进本 PR):删 \`translate\` prop、Slot 直接
\`useTranslation()\`、\`humanizeAgentId\` 移 util 文件。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- 根治 Sentry ECA-765(\`removeChild\` / \`insertBefore\` NotFoundError):消灭 \`MarkdownContent\` 的"\`dangerouslySetInnerHTML\` + 嵌套 \`createRoot\`"双 React root 反模式
- 新增 token 级分段渲染:\`parse-markdown-segments\` 在顶层 code fence 处切分文档,ERMP / specialist 卡片成为主树的**真 React 子组件**(\`ERMPCardSegment\` / \`SpecialistCardSlot\`,\`next/dynamic\` 懒加载保持 code-split),其余 token 段沿用现有 marked renderer 输出 per-segment sanitized HTML
- 取代并关闭止血 PR #2327;设计 spec 见 \`docs/superpowers/specs/2026-06-10-markdown-segment-rendering.md\`

## Root cause
外层 React tree 通过 \`dangerouslySetInnerHTML\` 拥有整段消息 HTML,hydration effect 又用 \`createRoot()\` 往这段 HTML 内部的占位 div 挂嵌套 root——同一块 DOM 被两个 root 管理。流式输出时 content 每 token 一变:外层 root 在 **mutation 阶段**重写 innerHTML 铲掉嵌套 root 的 host 节点,嵌套 root 的 \`unmount()\` 在更晚的 **passive 阶段**才执行,此时其子节点已不在树上 → NotFoundError。

实现中还发现一个放大因素:**React 19 对 \`dangerouslySetInnerHTML\` 按对象身份 diff**(不比较 \`__html\` 字符串),内联 \`{{__html}}\` 字面量导致任何父级 re-render 都无条件重写 innerHTML——旧代码的触发面远不止 content 变化。新实现用 \`React.memo\` 的 \`HtmlSegment\` 让相同 html 字符串直接 bail out(load-bearing,非优化),流式时未变段 DOM 零重写。

行为变化台账(详见 spec):
1. \`suppressSpecialistCards\` 从 \`display:none\` 占位 div 变为不渲染(等价,数据在 React state 不需 DOM 占位存活)
2. 嵌套(blockquote/list 内)卡片 fence 从不可见空 div 退化为**可见** code block(契约:卡片只在顶层 fence)
3. raw-HTML 注入的占位 div 不再是 hydration 向量;\`data-ermp-*\` / \`data-zc-*\` 移出 DOMPurify allowlist(src 内零 producer)
4. 卡片 payload 不再 encodeURIComponent 往返 DOM 属性

## Test plan
- [x] characterization 锁(重构前提交,跨重构原封不动通过):ERMP happy/invalid、unknown-kind / 空 agent-id 降级、混合消息、**ERMP 流式挂载(ECA-765 触发场景)**、跨 fence reference 链接
- [x] 分段器单测含等价性属性测试:无卡片输入的分段输出与 \`renderMarkdownToHtml\` 字节级相同
- [x] ECA-765 专属回归:流式追加时前段 DOM **节点引用恒等**;卡片挂载中整体替换 content 正常卸载不抛错
- [x] 全量 unit suite 7023 passed / \`tsc --noEmit\` / \`pnpm lint\` / \`pnpm dup\` 全过(\`react-hooks-config\` lint-contract 测试在本机全量并行下偶发 10s 超时,隔离运行通过,与本 diff 无交集)
- [ ] 手测:\`/chat\` 流式含 \`\`\`ecap-card 消息无控制台错误、卡片可交互;\`/new-chat\` → session thread;hire/fire consent i18n 消息组装;图片 blur / file card / 视频缩略图 / shiki / 分享回放
- [ ] 合并上线后观察 Sentry ECA-765:新增 NotFoundError 应归零(残留即浏览器扩展噪声,可借此区分归因)

后续 follow-up(不进本 PR):删 \`translate\` prop、Slot 直接 \`useTranslation()\`、\`humanizeAgentId\` 移 util 文件。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(agent-packs): hide market packs from catalog (#2346)

- **SHA**: `b7ecc96d29a9b4424acbccff6acdfc8bbc1dee9c`
- **作者**: bill-srp
- **日期**: 2026-06-10T11:15:27Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/b7ecc96d29a9b4424acbccff6acdfc8bbc1dee9c
- **PR**: #2346

### 完整 Commit Message

```
fix(agent-packs): hide market packs from catalog (#2346)

## Summary
- Add hide_market to agent-pack schemas, create/update payloads, and
dashboard-console form state.
- Add a dashboard-console Hide market toggle and Hidden market badge for
agent packs.
- Filter public /agent-packs market results at the pack list query layer
with hide_market=false, while leaving internal/admin lists unfiltered.

## Local checks
- pnpm --dir web/dashboard-console test -- app/lib/claw-api.test.ts
tests/packs.test.ts app/routes/agent-packs/route.test.tsx
tests/agent-packs-data.test.ts
- pnpm --dir web/dashboard-console run typecheck
- services/claw-interface/.venv/bin/pytest
tests/unit/test_internal_agent_packs_routes.py
tests/unit/test_public_agent_packs_routes.py
tests/unit/test_pack_services.py tests/unit/test_pack_repo.py
tests/unit/test_routes_pack_store.py tests/unit/test_schema_pack.py
- services/claw-interface/.venv/bin/ruff format --check targeted backend
files
- services/claw-interface/.venv/bin/ruff check targeted backend files
- git diff --check

## Notes
- Local pyright is not available in services/claw-interface/.venv (also
unavailable via python -m pyright).
- wrangler prints a sandbox EPERM warning while trying to write its log
file under ~/Library/Preferences, but dashboard-console typecheck exits
0.
```

### PR Body

## Summary
- Add hide_market to agent-pack schemas, create/update payloads, and dashboard-console form state.
- Add a dashboard-console Hide market toggle and Hidden market badge for agent packs.
- Filter public /agent-packs market results at the pack list query layer with hide_market=false, while leaving internal/admin lists unfiltered.

## Local checks
- pnpm --dir web/dashboard-console test -- app/lib/claw-api.test.ts tests/packs.test.ts app/routes/agent-packs/route.test.tsx tests/agent-packs-data.test.ts
- pnpm --dir web/dashboard-console run typecheck
- services/claw-interface/.venv/bin/pytest tests/unit/test_internal_agent_packs_routes.py tests/unit/test_public_agent_packs_routes.py tests/unit/test_pack_services.py tests/unit/test_pack_repo.py tests/unit/test_routes_pack_store.py tests/unit/test_schema_pack.py
- services/claw-interface/.venv/bin/ruff format --check targeted backend files
- services/claw-interface/.venv/bin/ruff check targeted backend files
- git diff --check

## Notes
- Local pyright is not available in services/claw-interface/.venv (also unavailable via python -m pyright).
- wrangler prints a sandbox EPERM warning while trying to write its log file under ~/Library/Preferences, but dashboard-console typecheck exits 0.


---

## feat(web): auto-send landing initial query (#2345)

- **SHA**: `bd7db93b54d190e90d73f515b8407ec2d3da71e1`
- **作者**: bill-srp
- **日期**: 2026-06-10T11:14:14Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/bd7db93b54d190e90d73f515b8407ec2d3da71e1
- **PR**: #2345

### 完整 Commit Message

```
feat(web): auto-send landing initial query (#2345)

## Linear

https://linear.app/srpone/issue/ECA-927/web-specialist-%E8%90%BD%E5%9C%B0%E9%A1%B5%E5%88%9D%E5%A7%8B-query-%E8%87%AA%E5%8A%A8%E5%8F%91%E9%80%81%E5%85%8D%E5%8E%BB%E7%94%A8%E6%88%B7%E6%89%8B%E5%8A%A8%E7%82%B9%E5%87%BB-send%E7%BC%A9%E7%9F%AD%E9%A6%96%E6%AC%A1%E4%BA%92%E5%8A%A8%E6%BC%8F%E6%96%97

## Summary
- Auto-send non-empty landing-context initial queries after the chat
switches to the target Specialist and the Mattermost channel is ready.
- Keep the existing composer prefill path as the retry fallback when
direct auto-send fails.
- Return send success/failure from the shared chat send path and cover
the landing/send behavior with unit tests.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app test:unit
tests/unit/hooks/useLandingContextFlow.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts
- [x] pnpm --dir web run test:unit --
tests/unit/hooks/useLandingContextFlow.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts

Note: pnpm --dir web run tsc currently fails locally before TypeScript
runs because the root script invokes pnpm exec with an unsupported
--if-present flag under pnpm 10.30.1; the touched app typecheck above
passes.
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-927/web-specialist-%E8%90%BD%E5%9C%B0%E9%A1%B5%E5%88%9D%E5%A7%8B-query-%E8%87%AA%E5%8A%A8%E5%8F%91%E9%80%81%E5%85%8D%E5%8E%BB%E7%94%A8%E6%88%B7%E6%89%8B%E5%8A%A8%E7%82%B9%E5%87%BB-send%E7%BC%A9%E7%9F%AD%E9%A6%96%E6%AC%A1%E4%BA%92%E5%8A%A8%E6%BC%8F%E6%96%97

## Summary
- Auto-send non-empty landing-context initial queries after the chat switches to the target Specialist and the Mattermost channel is ready.
- Keep the existing composer prefill path as the retry fallback when direct auto-send fails.
- Return send success/failure from the shared chat send path and cover the landing/send behavior with unit tests.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app test:unit tests/unit/hooks/useLandingContextFlow.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts
- [x] pnpm --dir web run test:unit -- tests/unit/hooks/useLandingContextFlow.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts

Note: pnpm --dir web run tsc currently fails locally before TypeScript runs because the root script invokes pnpm exec with an unsupported --if-present flag under pnpm 10.30.1; the touched app typecheck above passes.

---

## refactor(claw-interface): add official agent uninstall lifecycle (#2334)

- **SHA**: `fbcf2eb1da045b4b58f5670a2c7d56a4f9603ba2`
- **作者**: bill-srp
- **日期**: 2026-06-10T10:47:45Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/fbcf2eb1da045b4b58f5670a2c7d56a4f9603ba2
- **PR**: #2334

### 完整 Commit Message

```
refactor(claw-interface): add official agent uninstall lifecycle (#2334)

## Summary
- Adds /computers/{computer_id}/agents/{agent_id}/uninstall.
- Adds official-agent uninstall lifecycle cleanup and workspace status
transitions.
- Adds stale operation reaper scheduling for stuck install/uninstall
states.

## Stack
- Base: #2333 update route PR.
- Frontend PR should stack above this backend layer.

## Test plan
- services/claw-interface/.venv/bin/python -m ruff check
services/claw-interface/app/database/agent_workspace_repo.py
services/claw-interface/app/routes/computer/agents.py
services/claw-interface/app/scheduler.py
services/claw-interface/app/services/computer/agent_uninstall_service.py
services/claw-interface/app/services/computer/agent_operation_reaper.py
services/claw-interface/tests/unit/test_agent_routes.py
services/claw-interface/tests/unit/test_agent_uninstall_service.py
services/claw-interface/tests/unit/test_agent_workspace_repo.py
services/claw-interface/tests/unit/test_scheduler.py
services/claw-interface/tests/unit/test_agent_operation_reaper.py
- services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_agent_routes.py
services/claw-interface/tests/unit/test_agent_uninstall_service.py
services/claw-interface/tests/unit/test_agent_workspace_repo.py
services/claw-interface/tests/unit/test_agent_operation_reaper.py
services/claw-interface/tests/unit/test_scheduler.py -q
```

### PR Body

## Summary
- Adds /computers/{computer_id}/agents/{agent_id}/uninstall.
- Adds official-agent uninstall lifecycle cleanup and workspace status transitions.
- Adds stale operation reaper scheduling for stuck install/uninstall states.

## Stack
- Base: #2333 update route PR.
- Frontend PR should stack above this backend layer.

## Test plan
- services/claw-interface/.venv/bin/python -m ruff check services/claw-interface/app/database/agent_workspace_repo.py services/claw-interface/app/routes/computer/agents.py services/claw-interface/app/scheduler.py services/claw-interface/app/services/computer/agent_uninstall_service.py services/claw-interface/app/services/computer/agent_operation_reaper.py services/claw-interface/tests/unit/test_agent_routes.py services/claw-interface/tests/unit/test_agent_uninstall_service.py services/claw-interface/tests/unit/test_agent_workspace_repo.py services/claw-interface/tests/unit/test_scheduler.py services/claw-interface/tests/unit/test_agent_operation_reaper.py
- services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_agent_routes.py services/claw-interface/tests/unit/test_agent_uninstall_service.py services/claw-interface/tests/unit/test_agent_workspace_repo.py services/claw-interface/tests/unit/test_agent_operation_reaper.py services/claw-interface/tests/unit/test_scheduler.py -q

---

## ci: pass Turnstile env vars to frontend deploy (#2344)

- **SHA**: `1d22ed1f468968c2a04b47377f257961522ffa47`
- **作者**: tim-srp
- **日期**: 2026-06-10T10:19:44Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/1d22ed1f468968c2a04b47377f257961522ffa47
- **PR**: #2344

### 完整 Commit Message

```
ci: pass Turnstile env vars to frontend deploy (#2344)

## Summary
- Pass `NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED` and
`NEXT_PUBLIC_TURNSTILE_SITE_KEY` from GitHub Actions variables into the
frontend deploy environment.
- Write the same variables into `.env.staging` / `.env.production`
before the OpenNext build.
- Fail deploy early when captcha is enabled but the Turnstile site key
is missing.

## Test Plan
- `python - <<'PY' ... yaml.safe_load(...) ... PY`
- `rg -n
"NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED|NEXT_PUBLIC_TURNSTILE_SITE_KEY"
.github/workflows/deploy.yml web/app/src/lib/auth/captcha.ts`
- `git diff --check -- .github/workflows/deploy.yml`

Note: `actionlint` is not installed locally.
```

### PR Body

## Summary
- Pass `NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED` and `NEXT_PUBLIC_TURNSTILE_SITE_KEY` from GitHub Actions variables into the frontend deploy environment.
- Write the same variables into `.env.staging` / `.env.production` before the OpenNext build.
- Fail deploy early when captcha is enabled but the Turnstile site key is missing.

## Test Plan
- `python - <<'PY' ... yaml.safe_load(...) ... PY`
- `rg -n "NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED|NEXT_PUBLIC_TURNSTILE_SITE_KEY" .github/workflows/deploy.yml web/app/src/lib/auth/captcha.ts`
- `git diff --check -- .github/workflows/deploy.yml`

Note: `actionlint` is not installed locally.


---

## fix(auth): add Turnstile to ECAP Google login (#2339)

- **SHA**: `44d4351d94ded140f22f004de0876bdc00e401fd`
- **作者**: tim-srp
- **日期**: 2026-06-10T10:01:54Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/44d4351d94ded140f22f004de0876bdc00e401fd
- **PR**: #2339

### 完整 Commit Message

```
fix(auth): add Turnstile to ECAP Google login (#2339)

## Summary
- add a Cloudflare Turnstile widget to the ECAP Google login entry point
- pass optional Turnstile captcha data through loginUser and
/auth/exchange
- keep email/phone login behavior unchanged; Turnstile is enabled only
by NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED and
NEXT_PUBLIC_TURNSTILE_SITE_KEY

## Root cause
Google login did not send a human-verification signal to
account-service, so the backend Turnstile + new-user rate-limit
protection could not be enforced from the ECAP frontend.

## Test plan
- [x] pnpm vitest run tests/unit/lib/auth/api.unit.spec.ts
tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/components/LoginForm.unit.spec.tsx
- [x] pnpm exec tsc --noEmit
- [x] pnpm exec eslint src/lib/auth/captcha.ts
src/components/TurnstileWidget.tsx src/lib/auth/api.ts
src/lib/auth/manager.ts src/components/LoginForm.tsx
tests/unit/lib/auth/api.unit.spec.ts
tests/unit/lib/auth/manager.unit.spec.ts
tests/unit/components/LoginForm.unit.spec.tsx --quiet --cache
--cache-location .eslintcache --cache-strategy content
- [x] pnpm lint
```

### PR Body

## Summary
- add a Cloudflare Turnstile widget to the ECAP Google login entry point
- pass optional Turnstile captcha data through loginUser and /auth/exchange
- keep email/phone login behavior unchanged; Turnstile is enabled only by NEXT_PUBLIC_ECAP_GOOGLE_LOGIN_CAPTCHA_REQUIRED and NEXT_PUBLIC_TURNSTILE_SITE_KEY

## Root cause
Google login did not send a human-verification signal to account-service, so the backend Turnstile + new-user rate-limit protection could not be enforced from the ECAP frontend.

## Test plan
- [x] pnpm vitest run tests/unit/lib/auth/api.unit.spec.ts tests/unit/lib/auth/manager.unit.spec.ts tests/unit/components/LoginForm.unit.spec.tsx
- [x] pnpm exec tsc --noEmit
- [x] pnpm exec eslint src/lib/auth/captcha.ts src/components/TurnstileWidget.tsx src/lib/auth/api.ts src/lib/auth/manager.ts src/components/LoginForm.tsx tests/unit/lib/auth/api.unit.spec.ts tests/unit/lib/auth/manager.unit.spec.ts tests/unit/components/LoginForm.unit.spec.tsx --quiet --cache --cache-location .eslintcache --cache-strategy content
- [x] pnpm lint

---

## feat(billing): block invalid Stripe trial payment methods (#2343)

- **SHA**: `346064d4e455d2d919d941daf8e7bf40d041d723`
- **作者**: kaka-srp
- **日期**: 2026-06-10T09:56:23Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/346064d4e455d2d919d941daf8e7bf40d041d723
- **PR**: #2343

### 完整 Commit Message

```
feat(billing): block invalid Stripe trial payment methods (#2343)

## Linear

https://linear.app/srpone/issue/ECA-952/block-invalid-stripe-trial-payment-methods

## Summary
- Add a Stripe Billing v2 trial payment-method guard before subscription
entitlement fulfillment.
- Block deterministic invalid trial cards, cancel the Stripe trial
subscription, and record the local payment order as failed instead of
granting credits.
- Persist Stripe payment method fingerprints for Billing v2 orders and
enforce the 5-other-account fingerprint threshold.
- Keep reconcile from treating blocked trial processing as recovered
entitlement fulfillment.

## Test plan
- [x] cd services/claw-interface && ruff format --check .
- [x] cd services/claw-interface && ruff check .
- [x] cd services/claw-interface && pyright app tests
- [x] cd services/claw-interface && pytest
tests/unit/test_stripe_billing_v2.py
tests/unit/test_stripe_billing_v2_reconcile.py
tests/unit/test_stripe_client.py -q
- [x] cd services/claw-interface && pytest
tests/unit/test_billing_v2_repos.py tests/unit/test_billing_v2_schema.py
-q
- [x] cd services/claw-interface && pytest
tests/unit/test_billing_v2_payment_orders.py -q
- [x] cd services/claw-interface && bash
scripts/ci-lint/01-file-length.sh
- [x] cd services/claw-interface && bash
scripts/ci-lint/03-complexity.sh

## Rollout note
- Billing v2 indexes are manually managed before rollout; this PR adds
the payment-order fingerprint lookup index to the existing manual index
spec/tests.
```

### PR Body

## Linear
https://linear.app/srpone/issue/ECA-952/block-invalid-stripe-trial-payment-methods

## Summary
- Add a Stripe Billing v2 trial payment-method guard before subscription entitlement fulfillment.
- Block deterministic invalid trial cards, cancel the Stripe trial subscription, and record the local payment order as failed instead of granting credits.
- Persist Stripe payment method fingerprints for Billing v2 orders and enforce the 5-other-account fingerprint threshold.
- Keep reconcile from treating blocked trial processing as recovered entitlement fulfillment.

## Test plan
- [x] cd services/claw-interface && ruff format --check .
- [x] cd services/claw-interface && ruff check .
- [x] cd services/claw-interface && pyright app tests
- [x] cd services/claw-interface && pytest tests/unit/test_stripe_billing_v2.py tests/unit/test_stripe_billing_v2_reconcile.py tests/unit/test_stripe_client.py -q
- [x] cd services/claw-interface && pytest tests/unit/test_billing_v2_repos.py tests/unit/test_billing_v2_schema.py -q
- [x] cd services/claw-interface && pytest tests/unit/test_billing_v2_payment_orders.py -q
- [x] cd services/claw-interface && bash scripts/ci-lint/01-file-length.sh
- [x] cd services/claw-interface && bash scripts/ci-lint/03-complexity.sh

## Rollout note
- Billing v2 indexes are manually managed before rollout; this PR adds the payment-order fingerprint lookup index to the existing manual index spec/tests.

---

## refactor(vertical-pack-plans): align package billing metadata (#2342)

- **SHA**: `73fb525a8c3909cbe60ff776c570a5f81c35f906`
- **作者**: bill-srp
- **日期**: 2026-06-10T09:24:34Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/73fb525a8c3909cbe60ff776c570a5f81c35f906
- **PR**: #2342

### 完整 Commit Message

```
refactor(vertical-pack-plans): align package billing metadata (#2342)

## Summary
- Add backend billing metadata fields for vertical pack plans and
packages, including Stripe price IDs.
- Add the VerticalPackPackage snapshot model/repository backed by
ecap-vertical-pack-packages with package_id as the primary key.
- Keep Stripe fields backend-managed by removing them from the
dashboard-console vertical pack form/table payload.

## Local checks
- services/claw-interface/.venv/bin/ruff format --check targeted backend
files
- services/claw-interface/.venv/bin/ruff check targeted backend files
- services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_vertical_pack_package_repo.py
services/claw-interface/tests/unit/test_schema_vertical_pack_package.py
-q
- services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_schema_vertical_pack_plan.py
services/claw-interface/tests/unit/test_schema_vertical_pack_package.py
services/claw-interface/tests/unit/test_vertical_pack_plan_repo.py
services/claw-interface/tests/unit/test_vertical_pack_package_repo.py
services/claw-interface/tests/unit/test_internal_vertical_pack_plans_routes.py
- pnpm --dir web/dashboard-console test -- vertical-pack-plans.test.ts
vertical-pack-plans-data.test.ts vertical-pack-plans-agents.test.ts
addon-agents-field.test.tsx route.test.tsx

## Notes
- Local pyright was not available in services/claw-interface/.venv (also
unavailable via python -m pyright).
```

### PR Body

## Summary
- Add backend billing metadata fields for vertical pack plans and packages, including Stripe price IDs.
- Add the VerticalPackPackage snapshot model/repository backed by ecap-vertical-pack-packages with package_id as the primary key.
- Keep Stripe fields backend-managed by removing them from the dashboard-console vertical pack form/table payload.

## Local checks
- services/claw-interface/.venv/bin/ruff format --check targeted backend files
- services/claw-interface/.venv/bin/ruff check targeted backend files
- services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_vertical_pack_package_repo.py services/claw-interface/tests/unit/test_schema_vertical_pack_package.py -q
- services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_schema_vertical_pack_plan.py services/claw-interface/tests/unit/test_schema_vertical_pack_package.py services/claw-interface/tests/unit/test_vertical_pack_plan_repo.py services/claw-interface/tests/unit/test_vertical_pack_package_repo.py services/claw-interface/tests/unit/test_internal_vertical_pack_plans_routes.py
- pnpm --dir web/dashboard-console test -- vertical-pack-plans.test.ts vertical-pack-plans-data.test.ts vertical-pack-plans-agents.test.ts addon-agents-field.test.tsx route.test.tsx

## Notes
- Local pyright was not available in services/claw-interface/.venv (also unavailable via python -m pyright).


---

## refactor(claw-interface): add official agent update route (#2333)

- **SHA**: `32d87763a2af7c4a0ba243eaac43b031a861446f`
- **作者**: bill-srp
- **日期**: 2026-06-10T09:18:50Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/32d87763a2af7c4a0ba243eaac43b031a861446f
- **PR**: #2333

### 完整 Commit Message

```
refactor(claw-interface): add official agent update route (#2333)

## Summary
- Adds /computers/{computer_id}/agents/{agent_id}/update.
- Adds update lifecycle validation that claims an existing official
workspace with latest pack metadata.
- Reuses the install background worker for the actual runtime update
after the workspace is marked installing.

## Stack
- Base: #2332 install lifecycle PR.
- Follow-up: uninstall/reaper will be a separate stacked backend PR.

## Test plan
- services/claw-interface/.venv/bin/python -m ruff check
services/claw-interface/app/routes/computer/agents.py
services/claw-interface/app/services/computer/agent_update_service.py
services/claw-interface/tests/unit/test_agent_routes.py
services/claw-interface/tests/unit/test_agent_update_service.py
- services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_agent_routes.py
services/claw-interface/tests/unit/test_agent_update_service.py -q
```

### PR Body

## Summary
- Adds /computers/{computer_id}/agents/{agent_id}/update.
- Adds update lifecycle validation that claims an existing official workspace with latest pack metadata.
- Reuses the install background worker for the actual runtime update after the workspace is marked installing.

## Stack
- Base: #2332 install lifecycle PR.
- Follow-up: uninstall/reaper will be a separate stacked backend PR.

## Test plan
- services/claw-interface/.venv/bin/python -m ruff check services/claw-interface/app/routes/computer/agents.py services/claw-interface/app/services/computer/agent_update_service.py services/claw-interface/tests/unit/test_agent_routes.py services/claw-interface/tests/unit/test_agent_update_service.py
- services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_agent_routes.py services/claw-interface/tests/unit/test_agent_update_service.py -q

---

## fix(r2-access-worker): support authenticated archive uploads (#2341)

- **SHA**: `6e9d47e5c81b39e36d9652a436464ebe2513c4ae`
- **作者**: bill-srp
- **日期**: 2026-06-10T09:12:55Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6e9d47e5c81b39e36d9652a436464ebe2513c4ae
- **PR**: #2341

### 完整 Commit Message

```
fix(r2-access-worker): support authenticated archive uploads (#2341)

## Summary
- Add POST /upload to the R2 access worker using bearer auth and
/account/me-derived org_id
- Store archives under <org_id>/<pack_id>/<uuid> with no timestamp
segment
- Restrict uploads to .zip and .tar.gz archives and document the
contract

## Test Plan
- pnpm --dir services/r2-access-worker test
- pnpm --dir services/r2-access-worker exec tsc --noEmit
```

### PR Body

## Summary
- Add POST /upload to the R2 access worker using bearer auth and /account/me-derived org_id
- Store archives under <org_id>/<pack_id>/<uuid> with no timestamp segment
- Restrict uploads to .zip and .tar.gz archives and document the contract

## Test Plan
- pnpm --dir services/r2-access-worker test
- pnpm --dir services/r2-access-worker exec tsc --noEmit

---

## refactor(claw-interface): add official agent install lifecycle (#2332)

- **SHA**: `cbc25f6676d2cbcd9a205a5fc65a5610e0cc62ae`
- **作者**: bill-srp
- **日期**: 2026-06-10T09:06:11Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/cbc25f6676d2cbcd9a205a5fc65a5610e0cc62ae
- **PR**: #2332

### 完整 Commit Message

```
refactor(claw-interface): add official agent install lifecycle (#2332)

## Summary
- Adds the user-facing official-agent install route under
/computers/{computer_id}/agents/{agent_id}/install.
- Adds the install lifecycle service for claiming/installing/activating
official agent workspaces.
- Extracts shared Mattermost activation handling used by the legacy
install path and the new V2 install path.

## Stack
- Base: #2270 foundation PR.
- Follow-ups: update route/service and uninstall/reaper will be separate
stacked backend PRs.

## Test plan
- services/claw-interface/.venv/bin/python -m ruff check
services/claw-interface/app/database/agent_workspace_repo.py
services/claw-interface/app/routes/computer/agents.py
services/claw-interface/app/routes/openclaw_agents/core.py
services/claw-interface/app/routes/openclaw_agents/deploy.py
services/claw-interface/app/routes/openclaw_agents/install.py
services/claw-interface/app/routes/openclaw_agents/shared.py
services/claw-interface/app/services/computer/agent_install_service.py
services/claw-interface/app/services/computer/official_agent_pack_deploy_script.py
services/claw-interface/app/services/openclaw/agent_runtime.py
services/claw-interface/app/services/openclaw/agent_mattermost_activation.py
services/claw-interface/tests/bdd/step_defs/test_openclaw_custom_agents.py
services/claw-interface/tests/unit/test_agent_install_service.py
services/claw-interface/tests/unit/test_agent_routes.py
services/claw-interface/tests/unit/test_openclaw_agents.py
- services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_agent_routes.py
services/claw-interface/tests/unit/test_agent_install_service.py
services/claw-interface/tests/unit/test_agent_workspace_repo.py -q
- services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_openclaw_agents.py -q

## Local note
- BDD step-def pytest collection is blocked locally by sandboxed MongoDB
SRV DNS resolution.
```

### PR Body

## Summary
- Adds the user-facing official-agent install route under /computers/{computer_id}/agents/{agent_id}/install.
- Adds the install lifecycle service for claiming/installing/activating official agent workspaces.
- Extracts shared Mattermost activation handling used by the legacy install path and the new V2 install path.

## Stack
- Base: #2270 foundation PR.
- Follow-ups: update route/service and uninstall/reaper will be separate stacked backend PRs.

## Test plan
- services/claw-interface/.venv/bin/python -m ruff check services/claw-interface/app/database/agent_workspace_repo.py services/claw-interface/app/routes/computer/agents.py services/claw-interface/app/routes/openclaw_agents/core.py services/claw-interface/app/routes/openclaw_agents/deploy.py services/claw-interface/app/routes/openclaw_agents/install.py services/claw-interface/app/routes/openclaw_agents/shared.py services/claw-interface/app/services/computer/agent_install_service.py services/claw-interface/app/services/computer/official_agent_pack_deploy_script.py services/claw-interface/app/services/openclaw/agent_runtime.py services/claw-interface/app/services/openclaw/agent_mattermost_activation.py services/claw-interface/tests/bdd/step_defs/test_openclaw_custom_agents.py services/claw-interface/tests/unit/test_agent_install_service.py services/claw-interface/tests/unit/test_agent_routes.py services/claw-interface/tests/unit/test_openclaw_agents.py
- services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_agent_routes.py services/claw-interface/tests/unit/test_agent_install_service.py services/claw-interface/tests/unit/test_agent_workspace_repo.py -q
- services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_openclaw_agents.py -q

## Local note
- BDD step-def pytest collection is blocked locally by sandboxed MongoDB SRV DNS resolution.

---

## chore(dev): production CDP validation launcher preset + report (#2340)

- **SHA**: `ebd3958198f9af800a5363fca0a1b65d30b6aabd`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T08:56:06Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/ebd3958198f9af800a5363fca0a1b65d30b6aabd
- **PR**: #2340

### 完整 Commit Message

```
chore(dev): production CDP validation launcher preset + report (#2340)

## What

Adds production (`zooclaw.ai`) support to the local Chrome-CDP
validation flow that already existed for staging, plus the post-refactor
production validation report it produced.

### 1. `--env production` preset for the CDP launcher
(`scripts/open-chrome-debug-profile.sh`)
- New `--env staging|production` preset (also via `CHROME_DEBUG_ENV`):
- `staging` (default, **unchanged**): `ecap.gensmo.nosay.live` ·
`~/.cache/ecap-chrome-cdp` · `:9222`
- `production`: `zooclaw.ai` · `~/.cache/ecap-chrome-cdp-prod` · `:9223`
+ a live-data safety reminder
- Distinct profile dir + port let staging and prod signed-in sessions
run side by side without colliding.
- Precedence preserved: explicit `--flag` > `CHROME_DEBUG_*` env >
`--env` preset. Bare invocation is byte-for-byte the old staging
behavior. `scripts/README.md` updated.

### 2. Production validation report
(`docs/production-validation/2026-06-10-...md`)
Validation of the frontend-refactor PRs released to production over the
last ~20h (prod web HEAD `914b25c64`), mirroring the
`docs/staging-validation/*` format.

## Validation result — 6/6 Pass

| # | Surface | PR |
|---|---------|----|
| 1 | Chat connection status | #2316 |
| 2 | Agent direct-message sidebar link | #2326 |
| 3 | Schedule surface + computer-status gating | #2336 / #2317 |
| 4 | Branded-CSS scoping (no global `:root` bleed) | #2322 / #2328 |
| 5 | Email-login gating behind `?email_login=1` (logged-out profile
`:9224`) | #2308 |
| 6 | Billing pre-open tab (user-authorized, observe-only, no payment) |
#2320 / #2321 |

Remaining follow-up: onboarding interactive flow (needs a fresh
non-onboarded account).

## Notes
- Screenshot evidence stays in the gitignored `.screenshots/` scratch
dir (not committed), consistent with the staging-report convention.
- The billing check touched **live Stripe** and was run only after
explicit authorization: it observed the pre-opened tab lands on a Stripe
URL (`about:blank` → `billing.stripe.com` in 117 ms) and closed the tab
immediately — no card entry, no payment.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

Adds production (`zooclaw.ai`) support to the local Chrome-CDP validation flow that already existed for staging, plus the post-refactor production validation report it produced.

### 1. `--env production` preset for the CDP launcher (`scripts/open-chrome-debug-profile.sh`)
- New `--env staging|production` preset (also via `CHROME_DEBUG_ENV`):
  - `staging` (default, **unchanged**): `ecap.gensmo.nosay.live` · `~/.cache/ecap-chrome-cdp` · `:9222`
  - `production`: `zooclaw.ai` · `~/.cache/ecap-chrome-cdp-prod` · `:9223` + a live-data safety reminder
- Distinct profile dir + port let staging and prod signed-in sessions run side by side without colliding.
- Precedence preserved: explicit `--flag` > `CHROME_DEBUG_*` env > `--env` preset. Bare invocation is byte-for-byte the old staging behavior. `scripts/README.md` updated.

### 2. Production validation report (`docs/production-validation/2026-06-10-...md`)
Validation of the frontend-refactor PRs released to production over the last ~20h (prod web HEAD `914b25c64`), mirroring the `docs/staging-validation/*` format.

## Validation result — 6/6 Pass

| # | Surface | PR |
|---|---------|----|
| 1 | Chat connection status | #2316 |
| 2 | Agent direct-message sidebar link | #2326 |
| 3 | Schedule surface + computer-status gating | #2336 / #2317 |
| 4 | Branded-CSS scoping (no global `:root` bleed) | #2322 / #2328 |
| 5 | Email-login gating behind `?email_login=1` (logged-out profile `:9224`) | #2308 |
| 6 | Billing pre-open tab (user-authorized, observe-only, no payment) | #2320 / #2321 |

Remaining follow-up: onboarding interactive flow (needs a fresh non-onboarded account).

## Notes
- Screenshot evidence stays in the gitignored `.screenshots/` scratch dir (not committed), consistent with the staging-report convention.
- The billing check touched **live Stripe** and was run only after explicit authorization: it observed the pre-opened tab lands on a Stripe URL (`about:blank` → `billing.stripe.com` in 117 ms) and closed the tab immediately — no card entry, no payment.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## refactor(claw-interface): expose agent workspace foundation (#2270)

- **SHA**: `129ff7b6755319cb22eb284c2d71285be8614fb4`
- **作者**: bill-srp
- **日期**: 2026-06-10T08:04:15Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/129ff7b6755319cb22eb284c2d71285be8614fb4
- **PR**: #2270

### 完整 Commit Message

```
refactor(claw-interface): expose agent workspace foundation (#2270)

## Summary
- Adds the authenticated public Zooclaw agent-pack catalog route.
- Extends AgentPublic with pack/submission metadata for installed
workspaces.
- Keeps legacy /openclaw/agents and session-channel reads aligned with
normalized workspace state.

## Split
- Foundation PR for backend agent workspace/catalog read surfaces.
- Install/update and uninstall execution routes are split into stacked
follow-up backend PRs.
- Frontend PR will be stacked on top of the backend lifecycle PRs.

## Test plan
- [x] `services/claw-interface/.venv/bin/python -m ruff format ...`
- [x] `services/claw-interface/.venv/bin/python -m ruff check ...`
- [ ] `services/claw-interface/.venv/bin/python -m pytest
tests/unit/test_agent_response.py
tests/unit/test_agent_workspace_repo.py
tests/unit/test_openclaw_session_channel_service.py
tests/unit/test_public_agent_packs_routes.py -q` — 74 passed, 1 local
env failure because this host venv is missing
`favie_common.middleware.request_context` while importing
`app.create_app`; CI/devcontainer remains the source of truth.
```

### PR Body

## Summary
- Adds the authenticated public Zooclaw agent-pack catalog route.
- Extends AgentPublic with pack/submission metadata for installed workspaces.
- Keeps legacy /openclaw/agents and session-channel reads aligned with normalized workspace state.

## Split
- Foundation PR for backend agent workspace/catalog read surfaces.
- Install/update and uninstall execution routes are split into stacked follow-up backend PRs.
- Frontend PR will be stacked on top of the backend lifecycle PRs.

## Test plan
- [x] `services/claw-interface/.venv/bin/python -m ruff format ...`
- [x] `services/claw-interface/.venv/bin/python -m ruff check ...`
- [ ] `services/claw-interface/.venv/bin/python -m pytest tests/unit/test_agent_response.py tests/unit/test_agent_workspace_repo.py tests/unit/test_openclaw_session_channel_service.py tests/unit/test_public_agent_packs_routes.py -q` — 74 passed, 1 local env failure because this host venv is missing `favie_common.middleware.request_context` while importing `app.create_app`; CI/devcontainer remains the source of truth.

---

## fix(web): gate schedule by computer status (#2336)

- **SHA**: `914b25c645fe568ab4e871716be30e9aa1a6809c`
- **作者**: bill-srp
- **日期**: 2026-06-10T07:50:10Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/914b25c645fe568ab4e871716be30e9aa1a6809c
- **PR**: #2336

### 完整 Commit Message

```
fix(web): gate schedule by computer status (#2336)

## Summary
- gate the schedule page jobs query on FastClaw computer status instead
of OpenClaw WebSocket status
- resolve the schedule page computer id from the hydrated bot, falling
back to the computers list
- keep WebSocket cron fallback/write paths intact while allowing REST
reads when the computer is ready

## Tests
- pnpm --dir web --filter @zooclaw/web-app exec vitest run --config
./vitest.config.mts tests/unit/app/schedule/cron-client.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app exec eslint
'src/app/[locale]/(app)/(chat)/schedule/CronClient.tsx'
tests/unit/app/schedule/cron-client.unit.spec.tsx --quiet

Note: initial dependency install with lifecycle scripts failed on sharp
source build; reran pnpm install --frozen-lockfile --ignore-scripts to
link workspace test binaries without modifying tracked files.
```

### PR Body

## Summary
- gate the schedule page jobs query on FastClaw computer status instead of OpenClaw WebSocket status
- resolve the schedule page computer id from the hydrated bot, falling back to the computers list
- keep WebSocket cron fallback/write paths intact while allowing REST reads when the computer is ready

## Tests
- pnpm --dir web --filter @zooclaw/web-app exec vitest run --config ./vitest.config.mts tests/unit/app/schedule/cron-client.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit
- pnpm --dir web/app exec eslint 'src/app/[locale]/(app)/(chat)/schedule/CronClient.tsx' tests/unit/app/schedule/cron-client.unit.spec.tsx --quiet

Note: initial dependency install with lifecycle scripts failed on sharp source build; reran pnpm install --frozen-lockfile --ignore-scripts to link workspace test binaries without modifying tracked files.

---

## fix(desktop): account-keyed reconnect, node-only bootstrap, dev process cleanup (#2335)

- **SHA**: `c4b37d17608a61c674679dec8309251799f23a2d`
- **作者**: zayne-srp
- **日期**: 2026-06-10T07:39:39Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c4b37d17608a61c674679dec8309251799f23a2d
- **PR**: #2335

### 完整 Commit Message

```
fix(desktop): account-keyed reconnect, node-only bootstrap, dev process cleanup (#2335)

## Summary
Three desktop fixes found during PandaClaw acceptance testing:

- **Account-keyed reconnect** — the desktop reconnect fast-path reused
the persisted gateway target/token without checking it belonged to the
currently logged-in account. After switching accounts the node kept
reconnecting to the *previous* account's bot, so the current account's
dashboard never showed a paired device. The cached `remote-target` is
now tagged with the `uid` that created it; the fast-path only fires when
it matches the current uid, otherwise it falls through to a fresh
pairing. Pre-existing caches (no uid) are treated as stale and re-pair.
- **Node-only bootstrap (least privilege)** — the desktop client
connects as a `node` with no scopes, but the bootstrap token profile
over-granted `roles: [node, operator]` + `operator.*` scopes. The
gateway auto-approves the node role but holds the operator-scope grant
for explicit approval, leaving a "role upgrade requires approval"
pending on every (re)connect. The bootstrap now requests the `node` role
only, so pairing is fully automatic.
- **Dev process-group cleanup** — `pnpm dev` spawned web (next) +
electron via `shell: true` and only killed the `sh` wrapper, so closing
the app window orphaned the real `next dev` server. It kept holding port
3000, shifting later launches to 3001/3002/3003 and breaking the
desktop→BFF connection. Each child is now spawned `detached` and the
whole process group is killed on every exit path
(SIGINT/SIGTERM/SIGHUP/exit/uncaughtException/window-close); added a
`pnpm dev:kill` manual nuke for stuck orphans.

## Linear
https://linear.app/srpone/issue/ECA-879

## Test plan
- [x] Switch accounts in PandaClaw → desktop node re-pairs against the
new account's bot instead of silently reconnecting to the old one.
- [x] Fresh pairing no longer leaves an operator-scope "role upgrade
requires approval" pending; node pairs + serves commands automatically.
- [x] Close the app window → no orphaned `next dev` / port left
occupied; next launch binds 3000 cleanly.
- [x] `tsc --noEmit` clean (desktop).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### PR Body

## Summary
Three desktop fixes found during PandaClaw acceptance testing:

- **Account-keyed reconnect** — the desktop reconnect fast-path reused the persisted gateway target/token without checking it belonged to the currently logged-in account. After switching accounts the node kept reconnecting to the *previous* account's bot, so the current account's dashboard never showed a paired device. The cached `remote-target` is now tagged with the `uid` that created it; the fast-path only fires when it matches the current uid, otherwise it falls through to a fresh pairing. Pre-existing caches (no uid) are treated as stale and re-pair.
- **Node-only bootstrap (least privilege)** — the desktop client connects as a `node` with no scopes, but the bootstrap token profile over-granted `roles: [node, operator]` + `operator.*` scopes. The gateway auto-approves the node role but holds the operator-scope grant for explicit approval, leaving a "role upgrade requires approval" pending on every (re)connect. The bootstrap now requests the `node` role only, so pairing is fully automatic.
- **Dev process-group cleanup** — `pnpm dev` spawned web (next) + electron via `shell: true` and only killed the `sh` wrapper, so closing the app window orphaned the real `next dev` server. It kept holding port 3000, shifting later launches to 3001/3002/3003 and breaking the desktop→BFF connection. Each child is now spawned `detached` and the whole process group is killed on every exit path (SIGINT/SIGTERM/SIGHUP/exit/uncaughtException/window-close); added a `pnpm dev:kill` manual nuke for stuck orphans.

## Linear
https://linear.app/srpone/issue/ECA-879

## Test plan
- [x] Switch accounts in PandaClaw → desktop node re-pairs against the new account's bot instead of silently reconnecting to the old one.
- [x] Fresh pairing no longer leaves an operator-scope "role upgrade requires approval" pending; node pairs + serves commands automatically.
- [x] Close the app window → no orphaned `next dev` / port left occupied; next launch binds 3000 cleanly.
- [x] `tsc --noEmit` clean (desktop).

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## chore: add gitignored .screenshots scratch dir for local UI captures (#2329)

- **SHA**: `124b0b0fb82f98efb6f0cf2152056ae9d52699ca`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T05:40:17Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/124b0b0fb82f98efb6f0cf2152056ae9d52699ca
- **PR**: #2329

### 完整 Commit Message

```
chore: add gitignored .screenshots scratch dir for local UI captures (#2329)

## What

Adds a dedicated, gitignored `.screenshots/` directory as the standard
home for local UI captures (Playwright `browser_take_screenshot`, manual
grabs, CDP-debug captures).

- `.screenshots/README.md` documents the convention (the only tracked
file in the dir).
- `.gitignore`: `.screenshots/*` + `!.screenshots/README.md` — images
stay local, never committed; the directory and its docs persist in the
repo.
- `AGENTS.md` (= `CLAUDE.md` symlink): new `## Screenshots` section so
agents write captures here instead of polluting the repo root.

## Why

Validation screenshots were landing at the repo root (e.g. stray
`billing-popup-*.png`). This gives them a clear, ignored scratch
location that both humans and agents know to use. If a capture is worth
keeping, it should be moved into the relevant `docs/` location and
referenced there.

## Notes

Config/docs only — no app or test code touched.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Body

## What

Adds a dedicated, gitignored `.screenshots/` directory as the standard home for local UI captures (Playwright `browser_take_screenshot`, manual grabs, CDP-debug captures).

- `.screenshots/README.md` documents the convention (the only tracked file in the dir).
- `.gitignore`: `.screenshots/*` + `!.screenshots/README.md` — images stay local, never committed; the directory and its docs persist in the repo.
- `AGENTS.md` (= `CLAUDE.md` symlink): new `## Screenshots` section so agents write captures here instead of polluting the repo root.

## Why

Validation screenshots were landing at the repo root (e.g. stray `billing-popup-*.png`). This gives them a clear, ignored scratch location that both humans and agents know to use. If a capture is worth keeping, it should be moved into the relevant `docs/` location and referenced there.

## Notes

Config/docs only — no app or test code touched.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## fix(billing): pre-open checkout tabs across async flows (#2320)

- **SHA**: `659e31499e35aa9421ed8374a2051553f3ebb33c`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T05:20:15Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/659e31499e35aa9421ed8374a2051553f3ebb33c
- **PR**: #2320

### 完整 Commit Message

```
fix(billing): pre-open checkout tabs across async flows (#2320)

## Summary

- Replaces old PR #1961 on latest `main`.
- Adds a fail-closed `openCheckoutPopup()` helper that pre-opens
checkout tabs synchronously, clears `opener`, verifies it stayed
cleared, and refuses to navigate unsafe popups.
- Preserves the old `noreferrer` privacy contract by navigating checkout
popups through a no-referrer redirect document instead of assigning the
external URL directly.
- Uses the helper in paywall checkout and billing subscription/top-up
checkout flows so async order creation does not lose browser user
activation.
- Adds production acceptance notes in
`docs/staging-validation/2026-06-10-billing-popup-checkout-validation.md`.

## Out of scope

- Customer portal and invoice download popup handling remain follow-up
work for the old #1965 scope.

## Validation

- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/lib/window-open.unit.spec.ts
tests/unit/components/PaywallContent.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx`
passed: 4 files, 91 tests.
- `pnpm --dir web run lint` passed with existing enterprise-app warnings
only.
- `pnpm --dir web/app exec tsc --noEmit` passed.
- `pnpm --dir web run tsc` did not reach TypeScript locally because
local pnpm 10.26.2 rejects the workspace script option `--if-present`.
- `pnpm --dir web/app run dev:staging` browser validation covered
`/new-chat`, `/chat`, desktop/mobile billing layouts, and popup-blocked
behavior through a temporary local-only billing harness that was not
committed.
```

### PR Body

## Summary

- Replaces old PR #1961 on latest `main`.
- Adds a fail-closed `openCheckoutPopup()` helper that pre-opens checkout tabs synchronously, clears `opener`, verifies it stayed cleared, and refuses to navigate unsafe popups.
- Preserves the old `noreferrer` privacy contract by navigating checkout popups through a no-referrer redirect document instead of assigning the external URL directly.
- Uses the helper in paywall checkout and billing subscription/top-up checkout flows so async order creation does not lose browser user activation.
- Adds production acceptance notes in `docs/staging-validation/2026-06-10-billing-popup-checkout-validation.md`.

## Out of scope

- Customer portal and invoice download popup handling remain follow-up work for the old #1965 scope.

## Validation

- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/lib/window-open.unit.spec.ts tests/unit/components/PaywallContent.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx` passed: 4 files, 91 tests.
- `pnpm --dir web run lint` passed with existing enterprise-app warnings only.
- `pnpm --dir web/app exec tsc --noEmit` passed.
- `pnpm --dir web run tsc` did not reach TypeScript locally because local pnpm 10.26.2 rejects the workspace script option `--if-present`.
- `pnpm --dir web/app run dev:staging` browser validation covered `/new-chat`, `/chat`, desktop/mobile billing layouts, and popup-blocked behavior through a temporary local-only billing harness that was not committed.


---

## refactor(web): finish branded module CSS cleanup for userguide/pricing (#796) (#2328)

- **SHA**: `c41b2f214746a2c1fe822a32b6cd40ced431d98e`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T04:57:03Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c41b2f214746a2c1fe822a32b6cd40ced431d98e
- **PR**: #796

### 完整 Commit Message

```
refactor(web): finish branded module CSS cleanup for userguide/pricing (#796) (#2328)

## What

Closes out the last two residuals of #796 (branded-module CSS
extraction). Both `userguide` and `pricing` already had scoped CSS
modules + `.{domain}-root`; only the **root element's** brand
background/colors were still applied via a JSX inline `style={{}}` (with
the very `eslint-disable` directives #796 set out to eliminate).

After this change, a repo-wide grep for the targeted anti-pattern
(`eslint-disable no-restricted-syntax -- …branded color palette via
inline styles`) returns **0** — all 6 domains (login / paywall /
onboarding / public / pricing / userguide) are now clean, and the
anti-regression guardrails (CI SHRINK-ONLY, `web/app/CLAUDE.md`
convention, `landing.css` reference) were already in place.

## Changes

- **userguide** (`UserGuideClient.tsx` + `userguide.css`): drop the
file-level `eslint-disable no-restricted-syntax` and the root
`style={{}}`; move `background` / `color` / font overrides into
`.userguide-root`. The CSS rule's old `font-family: Manrope` was
**dead** — the inline `Noto Sans SC` always won on the root element, so
descendants already inherited `Noto Sans SC`. The CSS now reflects what
actually rendered → behavior-preserving.
- **pricing** (`PublicPricingClient.tsx` + `pricing.css`): drop the
inline `forbid-dom-props` disable + root `style={{}}`; add the two
static brand hex (`#0a0a0f` / `#f5f4ef`) to the existing `.pricing-root`
block, beside the font overrides it already carried.

## Verification

- `pnpm lint` + `tsc --noEmit` — clean (removing the disables exposed no
hidden violations)
- `web/scripts/check-ignores-shrink-only.sh` — `react/forbid-dom-props`
ignores 26 → 26 (untouched)
- Objective completion test: repo-wide `eslint-disable
no-restricted-syntax` branded directives now **0** (was 1)
- Behavior preserved: dark background, white/off-white text, Noto Sans
SC font on both standalone marketing pages — no visual change intended.
Suggest a quick staging visual check of `/pricing` and `/userguide`
before merge.

Refs #796

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## fix(web): add agent direct message sidebar link (#2326)

- **SHA**: `25fb24c578687d68d3bd61c242b984a82f6f3e43`
- **作者**: bill-srp
- **日期**: 2026-06-10T03:57:43Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/25fb24c578687d68d3bd61c242b984a82f6f3e43
- **PR**: #2326

### 完整 Commit Message

```
fix(web): add agent direct message sidebar link (#2326)

## Summary
- Add a Direct Message entry at the top of each expanded agent session
list
- Route Direct Message to /chat with the current agent_id query
parameter
- Cover ordering and navigation with SideNavAgentSessions unit test

## Local checks
- pnpm --dir web run lint (passes with existing enterprise-app warnings)
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit

## Notes
- pnpm --dir web run tsc currently fails in the workspace script before
typechecking with: Unknown option: if-present
```

### PR Body

## Summary
- Add a Direct Message entry at the top of each expanded agent session list
- Route Direct Message to /chat with the current agent_id query parameter
- Cover ordering and navigation with SideNavAgentSessions unit test

## Local checks
- pnpm --dir web run lint (passes with existing enterprise-app warnings)
- pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx
- pnpm --dir web/app exec tsc --noEmit

## Notes
- pnpm --dir web run tsc currently fails in the workspace script before typechecking with: Unknown option: if-present

---

## docs: add post-merge staging validation report (#2319)

- **SHA**: `a306c873605f3870dc259f0d4c8e5c46e277ca9d`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T03:26:31Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/a306c873605f3870dc259f0d4c8e5c46e277ca9d
- **PR**: #2319

### 完整 Commit Message

```
docs: add post-merge staging validation report (#2319)

## Summary
- Add the final post-merge staging release validation report for the
latest main deployment.
- Record the /chat and /new-chat release-gate result plus
schedule/assets/claw-settings smoke evidence.
- Include the Chinese release conclusion requested for the test report.

## Test plan
- [x] git diff --cached --check
- [x] Manual review of the staged docs-only diff
- [x] No code tests run; this PR only adds a Markdown validation report
```

### PR Body

## Summary
- Add the final post-merge staging release validation report for the latest main deployment.
- Record the /chat and /new-chat release-gate result plus schedule/assets/claw-settings smoke evidence.
- Include the Chinese release conclusion requested for the test report.

## Test plan
- [x] git diff --cached --check
- [x] Manual review of the staged docs-only diff
- [x] No code tests run; this PR only adds a Markdown validation report

---

## fix(billing): pre-open portal and invoice tabs (#2321)

- **SHA**: `de3842d7b98904377d2e0e29ed47aac17d87d26a`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T03:23:59Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/de3842d7b98904377d2e0e29ed47aac17d87d26a
- **PR**: #2321

### 完整 Commit Message

```
fix(billing): pre-open portal and invoice tabs (#2321)

## Summary

- Replaces old PR #1965 on top of the latest `main`.
- Adds a fail-closed `openCheckoutPopup` path for hosted billing
redirects: the tab is opened synchronously, `window.opener` is cleared
before navigation, and redirects use a `no-referrer` document.
- Migrates `InvoiceHistory` customer portal, `InvoiceHistory` invoice
download, and `SubscriptionPanel` customer portal to the pre-opened
popup flow.
- Adds regression coverage for popup-blocked, opener-clearing failure,
redirect document failure, and successful no-referrer navigation.
- Adds an acceptance guide:
`docs/staging-validation/2026-06-10-billing-portal-popup-validation.md`.

## Out of scope

- Checkout/top-up flows from old PR #1961 are handled separately by PR
#2320.
- Non-Stripe billing channels keep their existing informational behavior
and do not pre-open a popup.

## Validation

- `pnpm --dir web install --config.minimumReleaseAge=0`
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts
tests/unit/lib/window-open.unit.spec.ts
tests/unit/components/billing/InvoiceHistory.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx`
  - Passed: 3 files, 86 tests.
- `pnpm --dir web run lint`
  - Passed with existing enterprise app warnings only.
- `pnpm --dir web/app exec tsc --noEmit`
  - Passed.
- `pnpm --dir web run tsc`
- Not completed locally: the local pnpm script failed before TypeScript
with `Unknown option: 'if-present'`. CI remains the source of truth for
the workspace script.
- Local `dev:staging` browser validation through Chrome CDP:
- Desktop and mobile billing popup harness rendered without positive
horizontal overflow.
- `InvoiceHistory` payment-method portal, invoice download, and
`SubscriptionPanel` portal all showed the blocked-popup toast
immediately when popups were blocked.
  - Buttons returned to enabled state after blocked-popup handling.
  - Both `/new-chat` and `/chat` loaded in the same local run.
```

### PR Body

## Summary

- Replaces old PR #1965 on top of the latest `main`.
- Adds a fail-closed `openCheckoutPopup` path for hosted billing redirects: the tab is opened synchronously, `window.opener` is cleared before navigation, and redirects use a `no-referrer` document.
- Migrates `InvoiceHistory` customer portal, `InvoiceHistory` invoice download, and `SubscriptionPanel` customer portal to the pre-opened popup flow.
- Adds regression coverage for popup-blocked, opener-clearing failure, redirect document failure, and successful no-referrer navigation.
- Adds an acceptance guide: `docs/staging-validation/2026-06-10-billing-portal-popup-validation.md`.

## Out of scope

- Checkout/top-up flows from old PR #1961 are handled separately by PR #2320.
- Non-Stripe billing channels keep their existing informational behavior and do not pre-open a popup.

## Validation

- `pnpm --dir web install --config.minimumReleaseAge=0`
- `pnpm --dir web/app exec vitest run --config ./vitest.config.mts tests/unit/lib/window-open.unit.spec.ts tests/unit/components/billing/InvoiceHistory.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx`
  - Passed: 3 files, 86 tests.
- `pnpm --dir web run lint`
  - Passed with existing enterprise app warnings only.
- `pnpm --dir web/app exec tsc --noEmit`
  - Passed.
- `pnpm --dir web run tsc`
  - Not completed locally: the local pnpm script failed before TypeScript with `Unknown option: 'if-present'`. CI remains the source of truth for the workspace script.
- Local `dev:staging` browser validation through Chrome CDP:
  - Desktop and mobile billing popup harness rendered without positive horizontal overflow.
  - `InvoiceHistory` payment-method portal, invoice download, and `SubscriptionPanel` portal all showed the blocked-popup toast immediately when popups were blocked.
  - Buttons returned to enabled state after blocked-popup handling.
  - Both `/new-chat` and `/chat` loaded in the same local run.


---

## refactor(web): scope onboarding styles (#2322)

- **SHA**: `dbfbacce67755d1ac98b59dbaa6dd3c295876f28`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-10T03:23:19Z
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/dbfbacce67755d1ac98b59dbaa6dd3c295876f28
- **PR**: #2322

### 完整 Commit Message

```
refactor(web): scope onboarding styles (#2322)

## Summary
- Supersedes old PR #828 and follows issue #754 by moving current
onboarding static inline styles into scoped `.ob-*` CSS classes.
- Removes 8 onboarding files from the `react/forbid-dom-props`
shrink-only grandfather list while keeping only prop/data-driven dynamic
styles as line-level disables with reasons.
- Adds
`docs/staging-validation/2026-06-10-onboarding-scoped-css-validation.md`
with staging acceptance steps for both `/chat` and `/new-chat`.

Refs #754.

## Test plan
- [x] `pnpm --dir web install --config.minimumReleaseAge=0`
- [x] `PATH=/opt/homebrew/bin:$PATH bash
web/scripts/check-ignores-shrink-only.sh`
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x]
`NODE_OPTIONS=--localstorage-file=/private/tmp/ecap-pr828-vitest-localstorage-seq
pnpm --dir web/app exec vitest run --config ./vitest.config.mts
--fileParallelism=false
tests/unit/components/onboarding/OnboardingLayout.unit.spec.tsx
tests/unit/components/onboarding/OnboardingModal.unit.spec.tsx
tests/unit/components/onboarding/WelcomeRewardToast.unit.spec.tsx
tests/unit/components/onboarding/CompanionSelectStep.unit.spec.tsx
tests/unit/components/onboarding/LandingScreen.unit.spec.tsx
tests/unit/components/onboarding/onboarding-progress.unit.spec.ts`
- [x] `pnpm --dir web/app run dev:staging` + Playwright CDP browser
validation:
- `/chat?onboarding=preview` desktop full flow: invite, name, companion,
loading.
  - `/chat?onboarding=preview` mobile invite at `390x844`.
  - `/new-chat?onboarding=preview` desktop invite.
- `https://ecap.gensmo.nosay.live/chat?onboarding=preview` desktop
visual comparison.
- [x] `git diff --check`

Note: `pnpm --dir web run tsc` still hits the known local script issue
`Unknown option: 'if-present'`; app-level `tsc --noEmit` passed and CI
remains the workspace typecheck gate.
```

### PR Body

## Summary
- Supersedes old PR #828 and follows issue #754 by moving current onboarding static inline styles into scoped `.ob-*` CSS classes.
- Removes 8 onboarding files from the `react/forbid-dom-props` shrink-only grandfather list while keeping only prop/data-driven dynamic styles as line-level disables with reasons.
- Adds `docs/staging-validation/2026-06-10-onboarding-scoped-css-validation.md` with staging acceptance steps for both `/chat` and `/new-chat`.

Refs #754.

## Test plan
- [x] `pnpm --dir web install --config.minimumReleaseAge=0`
- [x] `PATH=/opt/homebrew/bin:$PATH bash web/scripts/check-ignores-shrink-only.sh`
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `NODE_OPTIONS=--localstorage-file=/private/tmp/ecap-pr828-vitest-localstorage-seq pnpm --dir web/app exec vitest run --config ./vitest.config.mts --fileParallelism=false tests/unit/components/onboarding/OnboardingLayout.unit.spec.tsx tests/unit/components/onboarding/OnboardingModal.unit.spec.tsx tests/unit/components/onboarding/WelcomeRewardToast.unit.spec.tsx tests/unit/components/onboarding/CompanionSelectStep.unit.spec.tsx tests/unit/components/onboarding/LandingScreen.unit.spec.tsx tests/unit/components/onboarding/onboarding-progress.unit.spec.ts`
- [x] `pnpm --dir web/app run dev:staging` + Playwright CDP browser validation:
  - `/chat?onboarding=preview` desktop full flow: invite, name, companion, loading.
  - `/chat?onboarding=preview` mobile invite at `390x844`.
  - `/new-chat?onboarding=preview` desktop invite.
  - `https://ecap.gensmo.nosay.live/chat?onboarding=preview` desktop visual comparison.
- [x] `git diff --check`

Note: `pnpm --dir web run tsc` still hits the known local script issue `Unknown option: 'if-present'`; app-level `tsc --noEmit` passed and CI remains the workspace typecheck gate.

