# ecap-workspace commits — 2026-06-18

共 10 个 commit

---

## `10d51d62f0`

- **作者**: bill-srp
- **日期**: 2026-06-18T13:21:19Z
- **PR**: #2517
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/10d51d62f0ede64d0b25467abac67bf1a739ed97

### 完整 commit message

```
feat(web): extend agent pack API contract (#2517)

## Summary
- extend agent pack/org pack payload types with quick commands and
backend metadata fields
- allow the org packs hook to fetch all org pack statuses instead of
only active packs
- update the org packs hook unit coverage for the new request shape

## Test plan
- `pnpm --dir web/app exec vitest run
tests/unit/hooks/useOrgAgentPacks.unit.spec.ts
tests/unit/services/agent-packs.unit.spec.ts
tests/unit/services/org-agent-packs.unit.spec.ts`
- `bash scripts/verify-web.sh --no-test`
- `git diff --check`
```

### PR Description

## Summary
- extend agent pack/org pack payload types with quick commands and backend metadata fields
- allow the org packs hook to fetch all org pack statuses instead of only active packs
- update the org packs hook unit coverage for the new request shape

## Test plan
- `pnpm --dir web/app exec vitest run tests/unit/hooks/useOrgAgentPacks.unit.spec.ts tests/unit/services/agent-packs.unit.spec.ts tests/unit/services/org-agent-packs.unit.spec.ts`
- `bash scripts/verify-web.sh --no-test`
- `git diff --check`


---

## `7486cb2c28`

- **作者**: bill-srp
- **日期**: 2026-06-18T12:59:47Z
- **PR**: #2524
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/7486cb2c284fe31080d8c5b9c56688e772e15b81

### 完整 commit message

```
feat(account): expose account me session contract (#2524)

## Summary

- Extend `/account/me` with web session fields needed by the app:
permissions, preferences, Mattermost user credentials, and
subscription/account metadata.
- Add the web `getAccountMe` service and shared React Query key/hook.
- Keep the legacy `userBusinessDataKeys` in place for follow-up PRs in
the stack.

## Stack

1. This PR: account/me contract + client service.
2. `codex/web-account-session-gate`: web app session gate on account/me.
3. `codex/web-remove-users-get`: remove web users/get dependency.

## Verification

- `bash scripts/verify-web.sh web/app/src/services/account.ts
web/app/src/hooks/queries/useAccountMeQuery.ts
web/app/src/lib/query/keys.ts
web/app/tests/unit/services/account.unit.spec.ts`
-
`PATH=/Users/bill/Github/StarQuestAI/ecap-workspace-user/services/claw-interface/.venv/bin:$PATH
bash scripts/verify-py.sh`
```

### PR Description

## Summary

- Extend `/account/me` with web session fields needed by the app: permissions, preferences, Mattermost user credentials, and subscription/account metadata.
- Add the web `getAccountMe` service and shared React Query key/hook.
- Keep the legacy `userBusinessDataKeys` in place for follow-up PRs in the stack.

## Stack

1. This PR: account/me contract + client service.
2. `codex/web-account-session-gate`: web app session gate on account/me.
3. `codex/web-remove-users-get`: remove web users/get dependency.

## Verification

- `bash scripts/verify-web.sh web/app/src/services/account.ts web/app/src/hooks/queries/useAccountMeQuery.ts web/app/src/lib/query/keys.ts web/app/tests/unit/services/account.unit.spec.ts`
- `PATH=/Users/bill/Github/StarQuestAI/ecap-workspace-user/services/claw-interface/.venv/bin:$PATH bash scripts/verify-py.sh`


---

## `1af6387a5f`

- **作者**: bill-srp
- **日期**: 2026-06-18T12:44:43Z
- **PR**: #2521
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/1af6387a5fb6b8fb1ad12e64b133d2ac3f5afe67

### 完整 commit message

```
feat(ios): migrate agents to computer APIs (#2521)

## Summary

- Migrate iOS official agent install/update/uninstall and agent list
refresh to the computer-scoped agents API.
- Replace iOS `users/get` refresh with `account/me`, including nested
`mattermost_user`, and derive Mattermost bot channels from computer
agents.
- Expose `mattermost_user` from backend `GET /account/me`.
- Remove iOS dependency on legacy async agent install operations.

## Local checks

- `swiftlint lint --config ios/ZooClaw/.swiftlint.yml ...` for changed
iOS files
- `services/claw-interface/.venv/bin/python -m ruff check
services/claw-interface/app/schema/account_api.py
services/claw-interface/tests/unit/test_routes_account.py`
- `services/claw-interface/.venv/bin/python -m ruff format --check
services/claw-interface/app/schema/account_api.py
services/claw-interface/tests/unit/test_routes_account.py`
- `PATH=".../services/claw-interface/.venv/bin:$PATH" bash
scripts/verify-py.sh`
- `services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_routes_account.py -q`

## Notes

- `bash scripts/verify-changed.sh` reported py tooling missing on the
default PATH, so backend verification was rerun with the claw-interface
venv on PATH.
- Local `xcodebuild` was not run; prior attempts in this worktree hung
without output, so this PR relies on SwiftLint locally and CI for Xcode
build/test coverage.
```

### PR Description

## Summary

- Migrate iOS official agent install/update/uninstall and agent list refresh to the computer-scoped agents API.
- Replace iOS `users/get` refresh with `account/me`, including nested `mattermost_user`, and derive Mattermost bot channels from computer agents.
- Expose `mattermost_user` from backend `GET /account/me`.
- Remove iOS dependency on legacy async agent install operations.

## Local checks

- `swiftlint lint --config ios/ZooClaw/.swiftlint.yml ...` for changed iOS files
- `services/claw-interface/.venv/bin/python -m ruff check services/claw-interface/app/schema/account_api.py services/claw-interface/tests/unit/test_routes_account.py`
- `services/claw-interface/.venv/bin/python -m ruff format --check services/claw-interface/app/schema/account_api.py services/claw-interface/tests/unit/test_routes_account.py`
- `PATH=".../services/claw-interface/.venv/bin:$PATH" bash scripts/verify-py.sh`
- `services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_routes_account.py -q`

## Notes

- `bash scripts/verify-changed.sh` reported py tooling missing on the default PATH, so backend verification was rerun with the claw-interface venv on PATH.
- Local `xcodebuild` was not run; prior attempts in this worktree hung without output, so this PR relies on SwiftLint locally and CI for Xcode build/test coverage.


---

## `81464d4e18`

- **作者**: zayne-srp
- **日期**: 2026-06-18T08:11:20Z
- **PR**: #2520
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/81464d4e1827fe97cd6562c0682f26f23240cdf9

### 完整 commit message

```
fix(desktop): run Next server via LSUIElement Helper to drop the ghost Dock icon (#2520)

## Problem
The packaged macOS app shows a **second, windowless `PandaClaw` icon**
in the Dock / Cmd-Tab.

## Cause
The standalone Next server is spawned by re-executing the app's MAIN
binary (`process.execPath`) with `ELECTRON_RUN_AS_NODE`. macOS
LaunchServices registers that re-exec as a second **Foreground** app
instance of the bundle (confirmed via `lsappinfo`: a
`com.pandaclaw.desktop` entry with `!cgsConnection` = no window).

## Fix
Spawn the server via the bundled `"<App> Helper.app"` binary, which is
marked **`LSUIElement`** (no Dock presence) — verified in the helper's
Info.plist. Guarded to macOS with a fallback to `process.execPath`;
Windows/Linux are unaffected.

One file, desktop-only. Purely cosmetic — no functional/runtime change.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### PR Description

## Problem
The packaged macOS app shows a **second, windowless `PandaClaw` icon** in the Dock / Cmd-Tab.

## Cause
The standalone Next server is spawned by re-executing the app's MAIN binary (`process.execPath`) with `ELECTRON_RUN_AS_NODE`. macOS LaunchServices registers that re-exec as a second **Foreground** app instance of the bundle (confirmed via `lsappinfo`: a `com.pandaclaw.desktop` entry with `!cgsConnection` = no window).

## Fix
Spawn the server via the bundled `"<App> Helper.app"` binary, which is marked **`LSUIElement`** (no Dock presence) — verified in the helper's Info.plist. Guarded to macOS with a fallback to `process.execPath`; Windows/Linux are unaffected.

One file, desktop-only. Purely cosmetic — no functional/runtime change.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

---

## `66462b24b5`

- **作者**: zayne-srp
- **日期**: 2026-06-18T07:07:17Z
- **PR**: #2503
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/66462b24b539d187614d0e548f8594de757c73e0

### 完整 commit message

```
fix(desktop): pin packaged Next server to port 3000 so backends accept its origin (#2503)

## Problem
The packaged PandaClaw desktop app served its renderer from
`http://localhost:<random free port>`. The app's backends gate
cross-origin requests on an **Origin allow-list that only permits
`http://localhost:3000`** (the dev origin) — verified directly:
Mattermost returns no `Access-Control-Allow-Origin` for
`localhost:55477`/`:3001`/etc., only for `:3000`. So a packaged build
(random port) had its Mattermost WS/REST origin rejected → chat stuck on
"正在接通你的 Claw…", realtime never connects. (Dev worked because `next dev`
is always on `:3000`.)

## Fix
- **Pin the packaged Next server to port 3000** so the packaged origin
is identical to dev's, which the backends already allow. No CORS bridge
/ header rewriting needed. Falls back to a free port only if 3000 is
taken.
- **Inject `CLAW_INTERFACE_URL` into the spawned standalone server's
env** — the packaged standalone has no `.env`, so the BFF proxy would
fall back to `localhost:8000`. Selectable per build via the tsup-inlined
`DESKTOP_BACKEND_URL` (prod vs staging); defaults to staging.

## Verification
Built a local staging DMG: confirmed the packaged app listens on
`:3000`, login (Google) works, and Mattermost realtime connects (chat
"Claw 已连接"). Same behavior as `pnpm dev`.

## Scope
Two files, desktop-only (`desktop/main/next-server.ts`,
`desktop/tsup.config.ts`). No web/runtime behavior change.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

---------

Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### PR Description

## Problem
The packaged PandaClaw desktop app served its renderer from `http://localhost:<random free port>`. The app's backends gate cross-origin requests on an **Origin allow-list that only permits `http://localhost:3000`** (the dev origin) — verified directly: Mattermost returns no `Access-Control-Allow-Origin` for `localhost:55477`/`:3001`/etc., only for `:3000`. So a packaged build (random port) had its Mattermost WS/REST origin rejected → chat stuck on "正在接通你的 Claw…", realtime never connects. (Dev worked because `next dev` is always on `:3000`.)

## Fix
- **Pin the packaged Next server to port 3000** so the packaged origin is identical to dev's, which the backends already allow. No CORS bridge / header rewriting needed. Falls back to a free port only if 3000 is taken.
- **Inject `CLAW_INTERFACE_URL` into the spawned standalone server's env** — the packaged standalone has no `.env`, so the BFF proxy would fall back to `localhost:8000`. Selectable per build via the tsup-inlined `DESKTOP_BACKEND_URL` (prod vs staging); defaults to staging.

## Verification
Built a local staging DMG: confirmed the packaged app listens on `:3000`, login (Google) works, and Mattermost realtime connects (chat "Claw 已连接"). Same behavior as `pnpm dev`.

## Scope
Two files, desktop-only (`desktop/main/next-server.ts`, `desktop/tsup.config.ts`). No web/runtime behavior change.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>

---

## `eab8293fb8`

- **作者**: bill-srp
- **日期**: 2026-06-18T06:01:24Z
- **PR**: #2514
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/eab8293fb83b33bec398f7f26104204448a2a293

### 完整 commit message

```
chore(agents): link private packs to workspaces (#2514)

## Summary

- add a dry-run-first script to link existing custom/import agent
workspaces to matching private packs
- match by same-org pack display ID, with a fallback for versioned agent
IDs via approved submission avatar paths
- add unit coverage for private pack linking decisions and versioned
agent ID matching

## Files

-
`services/claw-interface/scripts/link_private_packs_to_agent_workspaces.py`
-
`services/claw-interface/tests/unit/test_link_private_packs_to_agent_workspaces.py`

## Local Checks

- `bash scripts/verify-py.sh --ruff-only` passed
- `bash scripts/verify-py.sh` blocked locally: `pyright` and
`lint-imports` are not installed in the backend venv
- targeted pytest blocked locally: backend venv has no `pytest`
```

### PR Description

## Summary

- add a dry-run-first script to link existing custom/import agent workspaces to matching private packs
- match by same-org pack display ID, with a fallback for versioned agent IDs via approved submission avatar paths
- add unit coverage for private pack linking decisions and versioned agent ID matching

## Files

- `services/claw-interface/scripts/link_private_packs_to_agent_workspaces.py`
- `services/claw-interface/tests/unit/test_link_private_packs_to_agent_workspaces.py`

## Local Checks

- `bash scripts/verify-py.sh --ruff-only` passed
- `bash scripts/verify-py.sh` blocked locally: `pyright` and `lint-imports` are not installed in the backend venv
- targeted pytest blocked locally: backend venv has no `pytest`


---

## `4af2d85ac6`

- **作者**: tim-srp
- **日期**: 2026-06-18T06:02:12Z
- **PR**: #2508
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4af2d85ac65878133ba08a791a9e9d3536879d71

### 完整 commit message

```
fix(warm-pool): adopt claimed bots before cold create (#2508)

## Summary
- Add an idempotent warm-pool runtime adoption service for
claimed/materialized bots.
- Run adoption after org membership exists and again before
/openclaw/init enters cold-create.
- Mirror Mattermost runtime with the adopted bot computer_id and avoid
overwriting existing runtime computers.

## Root cause
Warm-pool registration finalization can materialize bot assets before
the user has an active org membership. The existing V2 bot mirror write
skips when no org exists, leaving the claimed warm-pool FastClaw bot
outside ecap-zooclaw-computers. Later /openclaw/init sees no primary
runtime bot and creates a second bot.

## Test plan
- [x] pytest tests/unit/test_warm_pool_runtime_adoption.py
tests/unit/test_openclaw_endpoints_extra.py
tests/unit/test_account_team_org_route.py
tests/unit/test_account_service.py tests/unit/test_warm_pool.py
- [x] ruff check app/services/warm_pool_runtime_adoption.py
app/routes/openclaw.py app/routes/account.py
tests/unit/test_warm_pool_runtime_adoption.py
tests/unit/test_openclaw_endpoints_extra.py
tests/unit/test_account_team_org_route.py
- [x] python -m py_compile app/services/warm_pool_runtime_adoption.py
app/routes/openclaw.py app/routes/account.py
tests/unit/test_warm_pool_runtime_adoption.py
tests/unit/test_openclaw_endpoints_extra.py
tests/unit/test_account_team_org_route.py

Note: local pyright could not resolve fastapi with this shell
interpreter; the new service-specific type issue was fixed before final
checks.
```

### PR Description

## Summary
- Add an idempotent warm-pool runtime adoption service for claimed/materialized bots.
- Run adoption after org membership exists and again before /openclaw/init enters cold-create.
- Mirror Mattermost runtime with the adopted bot computer_id and avoid overwriting existing runtime computers.

## Root cause
Warm-pool registration finalization can materialize bot assets before the user has an active org membership. The existing V2 bot mirror write skips when no org exists, leaving the claimed warm-pool FastClaw bot outside ecap-zooclaw-computers. Later /openclaw/init sees no primary runtime bot and creates a second bot.

## Test plan
- [x] pytest tests/unit/test_warm_pool_runtime_adoption.py tests/unit/test_openclaw_endpoints_extra.py tests/unit/test_account_team_org_route.py tests/unit/test_account_service.py tests/unit/test_warm_pool.py
- [x] ruff check app/services/warm_pool_runtime_adoption.py app/routes/openclaw.py app/routes/account.py tests/unit/test_warm_pool_runtime_adoption.py tests/unit/test_openclaw_endpoints_extra.py tests/unit/test_account_team_org_route.py
- [x] python -m py_compile app/services/warm_pool_runtime_adoption.py app/routes/openclaw.py app/routes/account.py tests/unit/test_warm_pool_runtime_adoption.py tests/unit/test_openclaw_endpoints_extra.py tests/unit/test_account_team_org_route.py

Note: local pyright could not resolve fastapi with this shell interpreter; the new service-specific type issue was fixed before final checks.

---

## `99df290573`

- **作者**: bill-srp
- **日期**: 2026-06-18T03:38:14Z
- **PR**: #2513
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/99df2905734f96d8c90d0bb20be1e27d751dcf84

### 完整 commit message

```
feat(dashboard-console): edit pack quick commands (#2513)

## Linear

N/A

## Summary
- Add a quick commands editor to the dashboard-console update pack
modal.
- Preserve the existing pack form flow by writing edits back to
`form.quick_commands`.
- Disable saving when any quick command is missing `id`, `label`, or
`prompt`.

## Test plan
- [x] `pnpm --dir web/dashboard-console exec vitest run
app/routes/agent-packs/route.test.tsx`
- [x] `pnpm --dir web/dashboard-console exec eslint
app/routes/agent-packs/pack-dialog.tsx
app/routes/agent-packs/route.test.tsx`
- [x] `pnpm --dir web/dashboard-console exec tsc -b`
- [x] `bash scripts/verify-web.sh
web/dashboard-console/app/routes/agent-packs/pack-dialog.tsx
web/dashboard-console/app/routes/agent-packs/route.test.tsx` exits with
"No provided targets are under web/app"; dashboard-console was verified
with its owning package tooling above.
```

### PR Description

## Linear

N/A

## Summary
- Add a quick commands editor to the dashboard-console update pack modal.
- Preserve the existing pack form flow by writing edits back to `form.quick_commands`.
- Disable saving when any quick command is missing `id`, `label`, or `prompt`.

## Test plan
- [x] `pnpm --dir web/dashboard-console exec vitest run app/routes/agent-packs/route.test.tsx`
- [x] `pnpm --dir web/dashboard-console exec eslint app/routes/agent-packs/pack-dialog.tsx app/routes/agent-packs/route.test.tsx`
- [x] `pnpm --dir web/dashboard-console exec tsc -b`
- [x] `bash scripts/verify-web.sh web/dashboard-console/app/routes/agent-packs/pack-dialog.tsx web/dashboard-console/app/routes/agent-packs/route.test.tsx` exits with "No provided targets are under web/app"; dashboard-console was verified with its owning package tooling above.


---

## `0f6820874e`

- **作者**: bill-srp
- **日期**: 2026-06-18T03:09:49Z
- **PR**: #2506
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0f6820874ea725cbe9da617cd1e8ea0c155d8100

### 完整 commit message

```
feat(pack): sync quick commands and archive metadata (#2506)

## Summary

- Add `quick_commands` to backend pack and pack-submission schemas,
persistence, approval sync, install metadata, and internal/enterprise
routes.
- Add a dashboard-console row action to download the latest pack
archive, reparse `description.json` and `agent-pack.yaml`, preview
metadata changes, and confirm updating the pack record.
- Add private R2 archive download support for dashboard-console and
parse quick commands from pack archives.

## Tests

- `services/claw-interface/.venv/bin/pytest
services/claw-interface/tests/unit/test_schema_pack.py
services/claw-interface/tests/unit/test_pack_services.py
services/claw-interface/tests/unit/test_pack_repo.py
services/claw-interface/tests/unit/test_pack_store_txn_repo.py
services/claw-interface/tests/unit/test_routes_pack_store.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
services/claw-interface/tests/unit/test_agent_install_service.py
services/claw-interface/tests/unit/test_openclaw_agent_catalog_routes.py
-q`
- `NODE_OPTIONS=--max-old-space-size=8192 pnpm --dir
web/dashboard-console exec vitest run
app/routes/agent-packs/metadata-refresh.test.ts
app/lib/agent-pack-archive.test.ts app/routes/api/r2-download.test.ts
app/routes/agent-packs/route.test.tsx
app/routes/agent-packs/submissions/use-view-model.test.tsx`
- `pnpm --dir web/dashboard-console exec eslint
app/lib/agent-pack-archive.ts app/lib/packs.ts app/lib/claw-api.ts
app/lib/r2-download.ts app/routes/api/r2-download.ts
app/routes/api/r2-download.test.ts
app/routes/agent-packs/metadata-refresh.ts
app/routes/agent-packs/metadata-refresh.test.ts
app/routes/agent-packs/pack-table.tsx
app/routes/agent-packs/metadata-refresh-dialog.tsx
app/routes/agent-packs/route.tsx
app/routes/agent-packs/submission-form.ts
app/routes/agent-packs/use-view-model.ts
app/routes/agent-packs/route.test.tsx
app/routes/agent-packs/submissions/use-view-model.test.tsx`
- `NODE_OPTIONS=--max-old-space-size=8192 pnpm --dir
web/dashboard-console exec tsc -b`
- `git diff --check`

Note: `bash scripts/verify-changed.sh` degraded because
dashboard-console is outside `web/app` and the script did not detect the
claw-interface venv tooling; targeted checks above covered the changed
surfaces.
```

### PR Description

## Summary

- Add `quick_commands` to backend pack and pack-submission schemas, persistence, approval sync, install metadata, and internal/enterprise routes.
- Add a dashboard-console row action to download the latest pack archive, reparse `description.json` and `agent-pack.yaml`, preview metadata changes, and confirm updating the pack record.
- Add private R2 archive download support for dashboard-console and parse quick commands from pack archives.

## Tests

- `services/claw-interface/.venv/bin/pytest services/claw-interface/tests/unit/test_schema_pack.py services/claw-interface/tests/unit/test_pack_services.py services/claw-interface/tests/unit/test_pack_repo.py services/claw-interface/tests/unit/test_pack_store_txn_repo.py services/claw-interface/tests/unit/test_routes_pack_store.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py services/claw-interface/tests/unit/test_agent_install_service.py services/claw-interface/tests/unit/test_openclaw_agent_catalog_routes.py -q`
- `NODE_OPTIONS=--max-old-space-size=8192 pnpm --dir web/dashboard-console exec vitest run app/routes/agent-packs/metadata-refresh.test.ts app/lib/agent-pack-archive.test.ts app/routes/api/r2-download.test.ts app/routes/agent-packs/route.test.tsx app/routes/agent-packs/submissions/use-view-model.test.tsx`
- `pnpm --dir web/dashboard-console exec eslint app/lib/agent-pack-archive.ts app/lib/packs.ts app/lib/claw-api.ts app/lib/r2-download.ts app/routes/api/r2-download.ts app/routes/api/r2-download.test.ts app/routes/agent-packs/metadata-refresh.ts app/routes/agent-packs/metadata-refresh.test.ts app/routes/agent-packs/pack-table.tsx app/routes/agent-packs/metadata-refresh-dialog.tsx app/routes/agent-packs/route.tsx app/routes/agent-packs/submission-form.ts app/routes/agent-packs/use-view-model.ts app/routes/agent-packs/route.test.tsx app/routes/agent-packs/submissions/use-view-model.test.tsx`
- `NODE_OPTIONS=--max-old-space-size=8192 pnpm --dir web/dashboard-console exec tsc -b`
- `git diff --check`

Note: `bash scripts/verify-changed.sh` degraded because dashboard-console is outside `web/app` and the script did not detect the claw-interface venv tooling; targeted checks above covered the changed surfaces.


---

## `8d875d12f1`

- **作者**: kaka-srp
- **日期**: 2026-06-18T03:03:29Z
- **PR**: #2507
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8d875d12f1860b69a9912667ff9ccace418d40bc

### 完整 commit message

```
feat(chat): show turn status (#2507)

## Linear
https://linear.app/srpone/issue/ECA-1011

## Summary
- Add durable Mattermost turn_status parsing and rendering for
chat/user-message state.
- Use fresh turn status as the authoritative generating signal while
preserving old waiting heuristics when status is missing.
- Support main chat and session-thread views, including stale-heartbeat
unknown state and same-post status edit ordering.
- Emit a 2-minute `chat.message.slow_response` Sentry log with uid, bot
id, message id, elapsed time, and unresolved ack/reply state.
- Document the cross-repo producer/consumer contract for Mattermost turn
status.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/app/chat/turnStatusParser.unit.spec.ts
tests/unit/hooks/useMmTypewriter.unit.spec.ts
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx
tests/unit/app/chat-thread/useLiveThread.unit.spec.ts
tests/unit/hooks/mattermost/useMattermostPosts.unit.spec.ts
tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts`
- [x] `pnpm exec vitest run
tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh --no-test
web/app/src/lib/mattermost/post-store.ts
web/app/src/hooks/mattermost/useMattermostPosts.ts
web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/hooks/useLiveThread.ts
web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/hooks/useSessionThreadDisplayMessages.ts
web/app/src/app/[locale]/(app)/(chat)/chat/lib/turnStatusParser.ts
web/app/src/lib/sentry/message-latency-monitor.ts
web/app/src/app/[locale]/(app)/(chat)/chat/components/ChatBody.tsx
web/app/tests/unit/hooks/mattermost/useMattermostPosts.unit.spec.ts
web/app/tests/unit/app/chat-thread/useLiveThread.unit.spec.ts
web/app/tests/unit/app/chat/turnStatusParser.unit.spec.ts
web/app/tests/unit/hooks/useMmTypewriter.unit.spec.ts
web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx
web/app/tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts`
- [x] `bash scripts/verify-web.sh --no-test
web/app/src/lib/sentry/message-latency-monitor.ts
web/app/src/app/[locale]/(app)/(chat)/chat/hooks/useChatMessaging.ts
web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx
web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/SessionThreadClient.tsx
web/app/tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts
web/app/tests/unit/app/chat/useChatMessaging.unit.spec.ts
web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `git diff --check origin/main...HEAD`
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-1011

## Summary
- Add durable Mattermost turn_status parsing and rendering for chat/user-message state.
- Use fresh turn status as the authoritative generating signal while preserving old waiting heuristics when status is missing.
- Support main chat and session-thread views, including stale-heartbeat unknown state and same-post status edit ordering.
- Emit a 2-minute `chat.message.slow_response` Sentry log with uid, bot id, message id, elapsed time, and unresolved ack/reply state.
- Document the cross-repo producer/consumer contract for Mattermost turn status.

## Test plan
- [x] `pnpm exec vitest run tests/unit/app/chat/turnStatusParser.unit.spec.ts tests/unit/hooks/useMmTypewriter.unit.spec.ts tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx tests/unit/app/chat-thread/useLiveThread.unit.spec.ts tests/unit/hooks/mattermost/useMattermostPosts.unit.spec.ts tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts`
- [x] `pnpm exec vitest run tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh --no-test web/app/src/lib/mattermost/post-store.ts web/app/src/hooks/mattermost/useMattermostPosts.ts web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/hooks/useLiveThread.ts web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/hooks/useSessionThreadDisplayMessages.ts web/app/src/app/[locale]/(app)/(chat)/chat/lib/turnStatusParser.ts web/app/src/lib/sentry/message-latency-monitor.ts web/app/src/app/[locale]/(app)/(chat)/chat/components/ChatBody.tsx web/app/tests/unit/hooks/mattermost/useMattermostPosts.unit.spec.ts web/app/tests/unit/app/chat-thread/useLiveThread.unit.spec.ts web/app/tests/unit/app/chat/turnStatusParser.unit.spec.ts web/app/tests/unit/hooks/useMmTypewriter.unit.spec.ts web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx web/app/tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts`
- [x] `bash scripts/verify-web.sh --no-test web/app/src/lib/sentry/message-latency-monitor.ts web/app/src/app/[locale]/(app)/(chat)/chat/hooks/useChatMessaging.ts web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx web/app/src/app/[locale]/(app)/(chat)/chat/[computerId]/[agentId]/[sessionId]/SessionThreadClient.tsx web/app/tests/unit/lib/sentry/message-latency-monitor.unit.spec.ts web/app/tests/unit/app/chat/useChatMessaging.unit.spec.ts web/app/tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx`
- [x] `git diff --check origin/main...HEAD`

