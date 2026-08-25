# SerendipityOneInc/ecap-workspace — commits 2026-08-24

## feat(agents): add fast pack skill editor (#3499)

- **SHA**: `15967d27f1872c3f5feb4b0d607cd99a62caf79c`
- **作者**: kaka-srp
- **日期**: 2026-08-24T12:18:44Z
- **PR**: #3499

### Commit Message

```
feat(agents): add fast pack skill editor (#3499)

## Linear

N/A — this work was explicitly requested without a Linear issue.

## Summary

- add an archive-native v2 Pack Skills editor under Agents Manager,
without opening Agent Builder or starting a preview/test Agent
- publish immutable Skill-only Pack versions while preserving persona
files, non-text Skill assets, runtime variants, and Environment content
pins
- automatically submit origin-linked Marketplace listing updates for
normal review, with a separate pending pointer and an idempotent handoff
retry path
- offer a default-off “Update all installed Agents” option that updates
active v2 installs without copying or refreshing each owner's
credentials
- show the same lightweight update action in Agents Manager and the main
sidebar, querying availability once on page entry/refresh without focus
refetch or polling
- keep the new route on the repository's MVVM boundary and avoid
changing reconnect behavior for unrelated Pack query consumers

## Test plan

- [x] backend feature/regression suite: 188 tests passed
- [x] frontend feature/regression suite: 112 tests passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test`
- [x] post-rebase conflict checks: Agent workspace indexes and SideNav
actions

## Review notes

- The PR is 4,917 lines after repository exclusions, primarily complete
backend services, the editor UI, and regression tests. It intentionally
uses the repository's `size-override` path so the
source/Marketplace/update flow can be reviewed as one end-to-end change.
- No new collection/table is introduced. Marketplace review state uses
the existing Pack row plus `pending_submission_id`; immutable Pack
assets and submissions remain the source of truth.
```

### PR Body

## Linear

N/A — this work was explicitly requested without a Linear issue.

## Summary

- add an archive-native v2 Pack Skills editor under Agents Manager, without opening Agent Builder or starting a preview/test Agent
- publish immutable Skill-only Pack versions while preserving persona files, non-text Skill assets, runtime variants, and Environment content pins
- automatically submit origin-linked Marketplace listing updates for normal review, with a separate pending pointer and an idempotent handoff retry path
- offer a default-off “Update all installed Agents” option that updates active v2 installs without copying or refreshing each owner's credentials
- show the same lightweight update action in Agents Manager and the main sidebar, querying availability once on page entry/refresh without focus refetch or polling
- keep the new route on the repository's MVVM boundary and avoid changing reconnect behavior for unrelated Pack query consumers

## Test plan

- [x] backend feature/regression suite: 188 tests passed
- [x] frontend feature/regression suite: 112 tests passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --no-test`
- [x] post-rebase conflict checks: Agent workspace indexes and SideNav actions

## Review notes

- The PR is 4,917 lines after repository exclusions, primarily complete backend services, the editor UI, and regression tests. It intentionally uses the repository's `size-override` path so the source/Marketplace/update flow can be reviewed as one end-to-end change.
- No new collection/table is introduced. Marketplace review state uses the existing Pack row plus `pending_submission_id`; immutable Pack assets and submissions remain the source of truth.


---

## fix(deps): resolve all 85 dependabot alerts in web workspace (#3497)

- **SHA**: `6a672465c2f7b4c3d813a8cfc5491256209f7ce8`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-24T10:51:56Z
- **PR**: #3497

### Commit Message

```
fix(deps): resolve all 85 dependabot alerts in web workspace (#3497)

## 内容

清零 `web/` pnpm workspace 的全部 85 条 open Dependabot 告警（codex-coder
实现、Claude review）：

**直接依赖（package.json）**
- `next` 15.5.19 → 15.5.21（web-app）、16.2.6 →
16.2.11（enterprise-admin），同步 `eslint-config-next`
- `react-router` / `@react-router/dev` 7.16.0 →
7.18.2（dashboard-console）
- `mermaid` → 11.16.1、`dompurify` → 3.4.13、`postcss` → 8.5.23、`vite` →
8.0.16

**传递依赖（web/package.json pnpm.overrides，全部按 vulnerable range 限定）**
- 新增 12 条 range-scoped
overrides：`@babel/core`、`@opentelemetry/core`、`body-parser`、`form-data`、`js-yaml`、`nanoid`（3.x/5.x
双线）、`postcss`、`sharp`、`valibot`、`websocket-driver`、`ws`
- 其余（`brace-expansion`、`fast-uri`、`undici`、`protobufjs` 等）由 lockfile
刷新解决

无跳过项。

## 验证

- `pnpm install --frozen-lockfile` 通过（模拟 CI）
- `bash scripts/verify-web.sh` 全绿（guards / tsc / vitest 9037 passed /
eslint）
- enterprise-admin `tsc --noEmit`、dashboard-console `typecheck` 通过
- `pnpm audit --audit-level low`：0 vulnerabilities

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv
```

### PR Body

## 内容

清零 `web/` pnpm workspace 的全部 85 条 open Dependabot 告警（codex-coder 实现、Claude review）：

**直接依赖（package.json）**
- `next` 15.5.19 → 15.5.21（web-app）、16.2.6 → 16.2.11（enterprise-admin），同步 `eslint-config-next`
- `react-router` / `@react-router/dev` 7.16.0 → 7.18.2（dashboard-console）
- `mermaid` → 11.16.1、`dompurify` → 3.4.13、`postcss` → 8.5.23、`vite` → 8.0.16

**传递依赖（web/package.json pnpm.overrides，全部按 vulnerable range 限定）**
- 新增 12 条 range-scoped overrides：`@babel/core`、`@opentelemetry/core`、`body-parser`、`form-data`、`js-yaml`、`nanoid`（3.x/5.x 双线）、`postcss`、`sharp`、`valibot`、`websocket-driver`、`ws`
- 其余（`brace-expansion`、`fast-uri`、`undici`、`protobufjs` 等）由 lockfile 刷新解决

无跳过项。

## 验证

- `pnpm install --frozen-lockfile` 通过（模拟 CI）
- `bash scripts/verify-web.sh` 全绿（guards / tsc / vitest 9037 passed / eslint）
- enterprise-admin `tsc --noEmit`、dashboard-console `typecheck` 通过
- `pnpm audit --audit-level low`：0 vulnerabilities

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv


---

## fix(security): resolve web codeql alerts (insecure randomness, cleartext storage, dom xss) (#3496)

- **SHA**: `e18115a1ce4088e7e7fdbe8c1425135b005c345f`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-24T10:50:34Z
- **PR**: #3496

### Commit Message

```
fix(security): resolve web codeql alerts (insecure randomness, cleartext storage, dom xss) (#3496)

## 内容

修复 web/app 的 8 条 CodeQL code scanning 告警（由 codex-coder 实现、Claude
review）：

**insecure-randomness（#653 / #643 / #630 / #629）**
- 共享 helper `src/lib/uuid.ts` 删除 `Math.random()` 兜底，仅保留
`crypto.randomUUID()` / `crypto.getRandomValues()`，Web Crypto 不可用时 fail
closed。购买 nonce、landing session ID、R2 文件路径 UUID、device ID 全部走安全随机。

**clear-text-storage-of-sensitive-data（#635 / #619）**
- Firebase 手机验证的 verification ID 不再写 localStorage，改为内存
handoff（`src/lib/auth/phone-verification-handoff.ts`）。同 tab SPA
跳转不受影响；刷新页面则握手失效，走既有 sessionExpired 兜底。登出时随 `clearUserStorage` 一并清理。
- #632（mock-billing-data）为 false positive：仅写入开发/测试用展示数据，无凭据，另行 dismiss。

**xss-through-dom（#616 / #615）**
- `src/lib/upload.ts` 中 `setAttribute('src', url)` 改为直接属性赋值 `element.src
= url`。

## 测试

- 新增 `tests/unit/lib/uuid.unit.spec.ts`（3 cases），更新受影响的 auth/upload 单测。
- `bash scripts/verify-web.sh` 全绿（tsc / vitest 9040 passed / eslint /
guards）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv
```

### PR Body

## 内容

修复 web/app 的 8 条 CodeQL code scanning 告警（由 codex-coder 实现、Claude review）：

**insecure-randomness（#653 / #643 / #630 / #629）**
- 共享 helper `src/lib/uuid.ts` 删除 `Math.random()` 兜底，仅保留 `crypto.randomUUID()` / `crypto.getRandomValues()`，Web Crypto 不可用时 fail closed。购买 nonce、landing session ID、R2 文件路径 UUID、device ID 全部走安全随机。

**clear-text-storage-of-sensitive-data（#635 / #619）**
- Firebase 手机验证的 verification ID 不再写 localStorage，改为内存 handoff（`src/lib/auth/phone-verification-handoff.ts`）。同 tab SPA 跳转不受影响；刷新页面则握手失效，走既有 sessionExpired 兜底。登出时随 `clearUserStorage` 一并清理。
- #632（mock-billing-data）为 false positive：仅写入开发/测试用展示数据，无凭据，另行 dismiss。

**xss-through-dom（#616 / #615）**
- `src/lib/upload.ts` 中 `setAttribute('src', url)` 改为直接属性赋值 `element.src = url`。

## 测试

- 新增 `tests/unit/lib/uuid.unit.spec.ts`（3 cases），更新受影响的 auth/upload 单测。
- `bash scripts/verify-web.sh` 全绿（tsc / vitest 9040 passed / eslint / guards）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv


---

## fix(security): validate redirect hops in /api/download proxy (CodeQL #617) (#3495)

- **SHA**: `46e6a071637b8a06031350e2c08226ee3c28beee`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-24T10:50:19Z
- **PR**: #3495

### Commit Message

```
fix(security): validate redirect hops in /api/download proxy (CodeQL #617) (#3495)

## 问题

CodeQL alert #617（`js/request-forgery`，critical）：`/api/download` 代理虽然有
hostname 白名单，但 `fetch(url)` 默认自动跟随重定向。白名单里包含
`cloudfront.net`、`myshopify.com` 这类任何人都可托管内容的域——攻击者在自己的 CloudFront
发行版上返回 302 指向内网地址（如云 metadata endpoint），即可绕过白名单发起 SSRF。

## 修复

- `fetch` 改为 `redirect: 'manual'`，手动跟随重定向，每一跳的 `Location`（含相对路径解析）都重新过
`isAllowedUrl` 白名单校验。
- 命中不允许的重定向目标返回 403（不发起该请求）。
- 重定向上限 5 跳，超出返回 500。

## 测试

- 新增 4 个单测：允许域间重定向正常流式返回、重定向到内网地址被 403 拦截且不发请求、相对 Location
正确解析、重定向循环在上限处终止。
- `bash scripts/verify-web.sh` 全绿（tsc / vitest 9041 passed / eslint）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## 问题

CodeQL alert #617（`js/request-forgery`，critical）：`/api/download` 代理虽然有 hostname 白名单，但 `fetch(url)` 默认自动跟随重定向。白名单里包含 `cloudfront.net`、`myshopify.com` 这类任何人都可托管内容的域——攻击者在自己的 CloudFront 发行版上返回 302 指向内网地址（如云 metadata endpoint），即可绕过白名单发起 SSRF。

## 修复

- `fetch` 改为 `redirect: 'manual'`，手动跟随重定向，每一跳的 `Location`（含相对路径解析）都重新过 `isAllowedUrl` 白名单校验。
- 命中不允许的重定向目标返回 403（不发起该请求）。
- 重定向上限 5 跳，超出返回 500。

## 测试

- 新增 4 个单测：允许域间重定向正常流式返回、重定向到内网地址被 403 拦截且不发请求、相对 Location 正确解析、重定向循环在上限处终止。
- `bash scripts/verify-web.sh` 全绿（tsc / vitest 9041 passed / eslint）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01NWHV9vozVf6qN6zB5cUUdv


---

## feat(assets): show published artifacts for engine agents (#3380)

- **SHA**: `76377d0105dd77ef5ace895620315b6b615dffe1`
- **作者**: bill-srp
- **日期**: 2026-08-24T10:41:04Z
- **PR**: #3380

### Commit Message

```
feat(assets): show published artifacts for engine agents (#3380)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Assets library now surfaces v2 engine artifacts: when the selected
agent in the workspace browser is an **engine-runtime** agent, the panel
splits into a "Published Artifacts" section (from the v2 artifact
registry via the existing per-workspace `GET
/agents/{workspace_id}/artifacts` API) above the existing "Workspace
Files" browser. Computer (v1) agents are unchanged — they keep the plain
file browser.
- New `web/app/src/components/assets/PublishedArtifactsList.tsx`: pages
through `useAgentArtifacts` (limit 20) with a frozen `createdBefore`
snapshot cursor (same pattern as the chat Resources panel's
PublishedArtifactsTab) so pagination stays stable while new artifacts
land; snapshot + page reset on workspace switch and on error-retry.
- Ready artifacts with a stable `url` are clickable and open in the
existing preview pane as an attachable target (`messageUrl` = the
artifact's stable engine URL, image extensions previewed as images);
pending/failed/deleted artifacts render disabled with their status.
- `WorkspaceBrowser.tsx` keeps a single agent selector; the engine
branch wraps both sections in labeled `<section>`s with i18n headings
(`assets.publishedArtifacts` / `assets.workspaceFiles`, en + zh).
- Frontend half of the Artifact Library feature; backend cross-agent
library API is PR #3372.

## Test plan
- [x] 7 new unit tests for `PublishedArtifactsList` (attachable preview
target with stable URL, non-ready/URL-less not selectable, image
detection, shared loading/empty states, error retry re-snapshots, page
next/prev drives the query, workspace switch resets page + snapshot)
- [x] 1 new `WorkspaceBrowser` test: engine workspaces split into
Published Artifacts + Workspace Files sections (computer agents keep the
legacy browser — existing tests unchanged)
- [x] Full local gate green: `bash scripts/verify-web.sh` — CI guards,
tsc, eslint, and the full vitest suite (364 files / 5166 tests)
- [ ] `web-build-check` (`next build`) runs in CI

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Assets library now surfaces v2 engine artifacts: when the selected agent in the workspace browser is an **engine-runtime** agent, the panel splits into a "Published Artifacts" section (from the v2 artifact registry via the existing per-workspace `GET /agents/{workspace_id}/artifacts` API) above the existing "Workspace Files" browser. Computer (v1) agents are unchanged — they keep the plain file browser.
- New `web/app/src/components/assets/PublishedArtifactsList.tsx`: pages through `useAgentArtifacts` (limit 20) with a frozen `createdBefore` snapshot cursor (same pattern as the chat Resources panel's PublishedArtifactsTab) so pagination stays stable while new artifacts land; snapshot + page reset on workspace switch and on error-retry.
- Ready artifacts with a stable `url` are clickable and open in the existing preview pane as an attachable target (`messageUrl` = the artifact's stable engine URL, image extensions previewed as images); pending/failed/deleted artifacts render disabled with their status.
- `WorkspaceBrowser.tsx` keeps a single agent selector; the engine branch wraps both sections in labeled `<section>`s with i18n headings (`assets.publishedArtifacts` / `assets.workspaceFiles`, en + zh).
- Frontend half of the Artifact Library feature; backend cross-agent library API is PR #3372.

## Test plan
- [x] 7 new unit tests for `PublishedArtifactsList` (attachable preview target with stable URL, non-ready/URL-less not selectable, image detection, shared loading/empty states, error retry re-snapshots, page next/prev drives the query, workspace switch resets page + snapshot)
- [x] 1 new `WorkspaceBrowser` test: engine workspaces split into Published Artifacts + Workspace Files sections (computer agents keep the legacy browser — existing tests unchanged)
- [x] Full local gate green: `bash scripts/verify-web.sh` — CI guards, tsc, eslint, and the full vitest suite (364 files / 5166 tests)
- [ ] `web-build-check` (`next build`) runs in CI


---

## fix(billing): cover Billing v2 orders in orphan cron (#3494)

- **SHA**: `e776987854d4fad5fe7d0722c1456ff2df71e212`
- **作者**: tim-srp
- **日期**: 2026-08-24T09:49:49Z
- **PR**: #3494

### Commit Message

```
fix(billing): cover Billing v2 orders in orphan cron (#3494)

## Summary

- extend `check-orphaned-entitlements` to detect settled Billing v2
payment orders that never received an entitlement
- restore a provider-neutral alert for stale subscription checkouts in
`manual_review`
- aggregate legacy and Billing v2 orphan counts into one PagerDuty
incident while keeping manual-review alerts independent
- use provider-neutral PagerDuty naming; no Creem runtime code or
configuration is restored

## Context

Supersedes #3484. That PR was correct but conflicted with the subsequent
Creem retirement series. This branch was recreated from the latest
`main`, then the monitoring behavior was migrated and revalidated
against the current repository structure.

## Validation

- `bash scripts/verify-py.sh`
- `.venv/bin/python -m pytest -q
tests/unit/test_orphaned_entitlements_cron.py
tests/unit/test_billing_v2_repos.py` — 108 passed
- pre-push changed-surface verification — passed

## Risk

Detection-only. The cron reads existing order state and triggers or
resolves aggregate PagerDuty incidents; it does not mutate payment
orders or entitlements.
```

### PR Body

## Summary

- extend `check-orphaned-entitlements` to detect settled Billing v2 payment orders that never received an entitlement
- restore a provider-neutral alert for stale subscription checkouts in `manual_review`
- aggregate legacy and Billing v2 orphan counts into one PagerDuty incident while keeping manual-review alerts independent
- use provider-neutral PagerDuty naming; no Creem runtime code or configuration is restored

## Context

Supersedes #3484. That PR was correct but conflicted with the subsequent Creem retirement series. This branch was recreated from the latest `main`, then the monitoring behavior was migrated and revalidated against the current repository structure.

## Validation

- `bash scripts/verify-py.sh`
- `.venv/bin/python -m pytest -q tests/unit/test_orphaned_entitlements_cron.py tests/unit/test_billing_v2_repos.py` — 108 passed
- pre-push changed-surface verification — passed

## Risk

Detection-only. The cron reads existing order state and triggers or resolves aggregate PagerDuty incidents; it does not mutate payment orders or entitlements.


---

## fix(agents): make Sandbox readiness credential-aware (#3476)

- **SHA**: `2e80ab70817de813493375b1ced2852678cad35f`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-24T09:17:51Z
- **PR**: #3476

### Commit Message

```
fix(agents): make Sandbox readiness credential-aware (#3476)

## Summary

- initialize the Engine's LiteLLM and user-internal-token credentials
idempotently and keep the exact final `config_version` receipt
- make service-API `warm=true` synchronous: seed first, prepare that
exact version, then return the final version to the caller
- reject session-scoped `warm=true` before creating an Agent because
there is no session Sandbox to prepare yet
- require internal Agent installs to pass the same credential-readiness
barrier before activation and channel binding

## Dependency and rollout

- depends on
https://github.com/SerendipityOneInc/zooclaw-engine/pull/847
- merge/deploy the Engine change first; this PR is the consumer-side
switch to the new initialization and readiness contract

## Testing

- full Python pre-commit suite passed: Ruff, format, file length,
complexity, deptry, import-linter, repository contracts, vulture, and
staged Pyright
- related unit suite: 284 passed
- focused post-review suite: 127 passed
- service-token BDD module: 2 skipped locally without its Mongo/BDD
environment
```

### PR Body

## Summary

- initialize the Engine's LiteLLM and user-internal-token credentials idempotently and keep the exact final `config_version` receipt
- make service-API `warm=true` synchronous: seed first, prepare that exact version, then return the final version to the caller
- reject session-scoped `warm=true` before creating an Agent because there is no session Sandbox to prepare yet
- require internal Agent installs to pass the same credential-readiness barrier before activation and channel binding

## Dependency and rollout

- depends on https://github.com/SerendipityOneInc/zooclaw-engine/pull/847
- merge/deploy the Engine change first; this PR is the consumer-side switch to the new initialization and readiness contract

## Testing

- full Python pre-commit suite passed: Ruff, format, file length, complexity, deptry, import-linter, repository contracts, vulture, and staged Pyright
- related unit suite: 284 passed
- focused post-review suite: 127 passed
- service-token BDD module: 2 skipped locally without its Mongo/BDD environment


---

## feat(agent): add debug database viewer (#3492)

- **SHA**: `a872d21dd2238540b7f457b7973fa4c9e0ee826c`
- **作者**: Chris@ZooClaw
- **日期**: 2026-08-24T09:07:12Z
- **PR**: #3492

### Commit Message

```
feat(agent): add debug database viewer (#3492)

## What changed

Redo of #3165 on current `main` (ea8ea177e): the internal Agent Database
viewer, ported hunk-by-hunk with the auth/error-envelope conventions
that changed since July.

- Owner-authorized claw-interface proxy routes for the Engine Agent
database APIs: `GET /agents/{workspace_id}/database` and `GET
/agents/{workspace_id}/database/tables/{table_name}/rows` (new
`DatabaseMixin` in `engine_client`, Engine 404/5xx semantics preserved).
- Sidebar database entry shown only to internal debug users
(`canViewInternalOnlyFeatures`) and only after the Agent has a
provisioned database (catalog reports `ready`).
- Read-only database viewer page listing tables and rendering a selected
table as a paginated data grid.
- Spec kept as
`docs/superpowers/specs/2026-07-31-agent-database-viewer.md`.

Deviations from #3165 (main moved on):
- Auth dependency rewritten to the current `require_current_org` →
`CurrentOrgAccount` pattern (the old
`get_current_account`/`get_current_org` pair is gone from agents
routes).
- Non-engine workspace now raises the agents-package `NotFoundError`
envelope (`agent.not_found`) instead of a bare `HTTPException(404)`;
still a 404.
- Added route tests (7 cases: proxy pass-through, pagination
pass-through, `limit>100` → 422, non-engine workspace 404 without engine
call, agents_v2 gate ordering) — the original PR had none.

## Why

The internal Agent Database viewer needs to inspect an existing Agent
Turso database without provisioning one by opening the UI.

## Validation

- `verify-py.sh`: ruff, pyright (0 errors), import-linter 8 contracts
KEPT
- pytest `test_agent_database_routes.py` + `test_agents_v2_routes.py`:
26 passed
- `verify-web.sh`: tsc, eslint, vitest 9034 passed / 70 skipped
- `verify-local.sh` changed-surface gate: green

## Companion

Engine side: SerendipityOneInc/zooclaw-engine#864 (redo of
zooclaw-engine#556); response contract unchanged.

Supersedes #3165.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01KqDbsbSeKmV3Yw5uascyuC

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## What changed

Redo of #3165 on current `main` (ea8ea177e): the internal Agent Database viewer, ported hunk-by-hunk with the auth/error-envelope conventions that changed since July.

- Owner-authorized claw-interface proxy routes for the Engine Agent database APIs: `GET /agents/{workspace_id}/database` and `GET /agents/{workspace_id}/database/tables/{table_name}/rows` (new `DatabaseMixin` in `engine_client`, Engine 404/5xx semantics preserved).
- Sidebar database entry shown only to internal debug users (`canViewInternalOnlyFeatures`) and only after the Agent has a provisioned database (catalog reports `ready`).
- Read-only database viewer page listing tables and rendering a selected table as a paginated data grid.
- Spec kept as `docs/superpowers/specs/2026-07-31-agent-database-viewer.md`.

Deviations from #3165 (main moved on):
- Auth dependency rewritten to the current `require_current_org` → `CurrentOrgAccount` pattern (the old `get_current_account`/`get_current_org` pair is gone from agents routes).
- Non-engine workspace now raises the agents-package `NotFoundError` envelope (`agent.not_found`) instead of a bare `HTTPException(404)`; still a 404.
- Added route tests (7 cases: proxy pass-through, pagination pass-through, `limit>100` → 422, non-engine workspace 404 without engine call, agents_v2 gate ordering) — the original PR had none.

## Why

The internal Agent Database viewer needs to inspect an existing Agent Turso database without provisioning one by opening the UI.

## Validation

- `verify-py.sh`: ruff, pyright (0 errors), import-linter 8 contracts KEPT
- pytest `test_agent_database_routes.py` + `test_agents_v2_routes.py`: 26 passed
- `verify-web.sh`: tsc, eslint, vitest 9034 passed / 70 skipped
- `verify-local.sh` changed-surface gate: green

## Companion

Engine side: SerendipityOneInc/zooclaw-engine#864 (redo of zooclaw-engine#556); response contract unchanged.

Supersedes #3165.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01KqDbsbSeKmV3Yw5uascyuC


---

## build(deps): update cachetools requirement from >=7.1.6 to >=7.1.7 in /services/claw-interface (#3400)

- **SHA**: `7366edc27cbc3716c5dd71a1e530759b581da0cd`
- **作者**: dependabot[bot]
- **日期**: 2026-08-24T08:40:10Z
- **PR**: #3400

### Commit Message

```
build(deps): update cachetools requirement from >=7.1.6 to >=7.1.7 in /services/claw-interface (#3400)

Updates the requirements on
[cachetools](https://github.com/tkem/cachetools) to permit the latest
version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's
changelog</a>.</em></p>
<blockquote>
<h1>v7.1.7 (2026-08-01)</h1>
<ul>
<li>
<p>Improve <code>Cache.__setitem__</code> behavior when replacing an
existing
cache item with a larger value.</p>
</li>
<li>
<p>Update CI environment.</p>
</li>
</ul>
<h1>v7.1.6 (2026-07-24)</h1>
<ul>
<li>Minor style improvements to keep <code>ruff</code> happy.</li>
</ul>
<h1>v7.1.5 (2026-07-23)</h1>
<ul>
<li>
<p>Fix <code>TLRUCache</code> silently keeping stale values on expired
overwrites.</p>
</li>
<li>
<p>Reject negative cache item <code>getsizeof</code> values.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.4 (2026-05-22)</h1>
<ul>
<li>
<p>Minor unit test improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.3 (2026-05-18)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.2 (2026-05-16)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Minor documentation improvements.</p>
</li>
<li>
<p>Modernize build environment.</p>
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
href="https://github.com/tkem/cachetools/commit/01af8e5b7ce44432b357e26c7d67eb7fa055ae72"><code>01af8e5</code></a>
Release v7.1.7.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/ccaa8c8c882b7cb76904ea5ae21aae33cca0c2c1"><code>ccaa8c8</code></a>
Minor stylistic improvements.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/c65b625da6a0e73839100a0d5f5153b4245d1689"><code>c65b625</code></a>
Prepare v7.1.7.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/89a5928c2f8abee030c34e7964523872cb2a81ba"><code>89a5928</code></a>
Bump actions/setup-python from 6.3.0 to 7.0.0 (<a
href="https://redirect.github.com/tkem/cachetools/issues/411">#411</a>)</li>
<li><a
href="https://github.com/tkem/cachetools/commit/39b31bc9b63abe98497409945e9d382d8918c8fb"><code>39b31bc</code></a>
Fix <a
href="https://redirect.github.com/tkem/cachetools/issues/405">#405</a>:
Fix Cache.<strong>setitem</strong> over-evicting when growing an
existing key</li>
<li><a
href="https://github.com/tkem/cachetools/commit/16e88894ef7d79b25a68f5a3b5411ed881342725"><code>16e8889</code></a>
Bump actions/checkout from 7.0.0 to 7.0.1 (<a
href="https://redirect.github.com/tkem/cachetools/issues/410">#410</a>)</li>
<li>See full diff in <a
href="https://github.com/tkem/cachetools/compare/v7.1.6...v7.1.7">compare
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

Updates the requirements on [cachetools](https://github.com/tkem/cachetools) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's changelog</a>.</em></p>
<blockquote>
<h1>v7.1.7 (2026-08-01)</h1>
<ul>
<li>
<p>Improve <code>Cache.__setitem__</code> behavior when replacing an existing
cache item with a larger value.</p>
</li>
<li>
<p>Update CI environment.</p>
</li>
</ul>
<h1>v7.1.6 (2026-07-24)</h1>
<ul>
<li>Minor style improvements to keep <code>ruff</code> happy.</li>
</ul>
<h1>v7.1.5 (2026-07-23)</h1>
<ul>
<li>
<p>Fix <code>TLRUCache</code> silently keeping stale values on expired
overwrites.</p>
</li>
<li>
<p>Reject negative cache item <code>getsizeof</code> values.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.4 (2026-05-22)</h1>
<ul>
<li>
<p>Minor unit test improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.3 (2026-05-18)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.2 (2026-05-16)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Minor documentation improvements.</p>
</li>
<li>
<p>Modernize build environment.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/tkem/cachetools/commit/01af8e5b7ce44432b357e26c7d67eb7fa055ae72"><code>01af8e5</code></a> Release v7.1.7.</li>
<li><a href="https://github.com/tkem/cachetools/commit/ccaa8c8c882b7cb76904ea5ae21aae33cca0c2c1"><code>ccaa8c8</code></a> Minor stylistic improvements.</li>
<li><a href="https://github.com/tkem/cachetools/commit/c65b625da6a0e73839100a0d5f5153b4245d1689"><code>c65b625</code></a> Prepare v7.1.7.</li>
<li><a href="https://github.com/tkem/cachetools/commit/89a5928c2f8abee030c34e7964523872cb2a81ba"><code>89a5928</code></a> Bump actions/setup-python from 6.3.0 to 7.0.0 (<a href="https://redirect.github.com/tkem/cachetools/issues/411">#411</a>)</li>
<li><a href="https://github.com/tkem/cachetools/commit/39b31bc9b63abe98497409945e9d382d8918c8fb"><code>39b31bc</code></a> Fix <a href="https://redirect.github.com/tkem/cachetools/issues/405">#405</a>: Fix Cache.<strong>setitem</strong> over-evicting when growing an existing key</li>
<li><a href="https://github.com/tkem/cachetools/commit/16e88894ef7d79b25a68f5a3b5411ed881342725"><code>16e8889</code></a> Bump actions/checkout from 7.0.0 to 7.0.1 (<a href="https://redirect.github.com/tkem/cachetools/issues/410">#410</a>)</li>
<li>See full diff in <a href="https://github.com/tkem/cachetools/compare/v7.1.6...v7.1.7">compare view</a></li>
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

## chore(deps-dev): update ruff requirement from >=0.16.1 to >=0.16.3 in /services/claw-interface (#3488)

- **SHA**: `8265073e642d4d07c988bedc19a6129da503e357`
- **作者**: dependabot[bot]
- **日期**: 2026-08-24T08:39:56Z
- **PR**: #3488

### Commit Message

```
chore(deps-dev): update ruff requirement from >=0.16.1 to >=0.16.3 in /services/claw-interface (#3488)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.16.3</h2>
<h2>Release Notes</h2>
<p>Released on 2026-08-13.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>pylint</code>] Fix false negatives on negative numbers
(<code>PLR6104</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27251">#27251</a>)</li>
<li>[<code>pyupgrade</code>] Add rule to replace <code>while 1</code>
with <code>while True</code> (<code>UP048</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27190">#27190</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-bandit</code>] Also check keyword arguments
(<code>S602</code>, <code>S603</code>, <code>S607</code>,
<code>S609</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27687">#27687</a>)</li>
<li>[<code>pylint</code>] Allow <code>continue</code> in
<code>finally</code> on Python 3.8 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27626">#27626</a>)</li>
<li>[<code>pylint</code>] Fix <code>PLE1307</code> false positive with
bools (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27651">#27651</a>)</li>
<li>[<code>pylint</code>] Fix false positives and negatives with
<code>%b</code> format character (<code>PLE1300</code>,
<code>PLE1307</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27560">#27560</a>)</li>
<li>[<code>pylint</code>] Improve handling of concatenated strings
(<code>PLE1300</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27659">#27659</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>numpy</code>] Make <code>np.chararray</code> autofix
backwards-compatible (<code>NPY201</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27527">#27527</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Enable PGO for Linux x86-64 Ruff releases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27570">#27570</a>)</li>
<li>Enable PGO for Linux ARM64 Ruff releases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27574">#27574</a>)</li>
<li>Enable PGO for Windows x86-64 Ruff releases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27573">#27573</a>)</li>
<li>Enable PGO for macOS ARM64 Ruff releases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27572">#27572</a>)</li>
<li>Reduce <code>Expr</code> size to 64 bytes (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27591">#27591</a>)</li>
</ul>
<h3>CLI</h3>
<ul>
<li>Hyperlink rule codes in <code>ruff check --statistics</code> output
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/27646">#27646</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>ruff</code>] Also suggest <code>asyncio.TaskGroup</code>
(<code>RUF006</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27461">#27461</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Use mimalloc v3 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27586">#27586</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/Andrej730"><code>@​Andrej730</code></a></li>
<li><a
href="https://github.com/alonfaraj"><code>@​alonfaraj</code></a></li>
<li><a
href="https://github.com/romero-deshaw"><code>@​romero-deshaw</code></a></li>
<li><a href="https://github.com/Avasam"><code>@​Avasam</code></a></li>
<li><a href="https://github.com/tjkuson"><code>@​tjkuson</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.16.3</h2>
<p>Released on 2026-08-13.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>pylint</code>] Fix false negatives on negative numbers
(<code>PLR6104</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27251">#27251</a>)</li>
<li>[<code>pyupgrade</code>] Add rule to replace <code>while 1</code>
with <code>while True</code> (<code>UP048</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27190">#27190</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-bandit</code>] Also check keyword arguments
(<code>S602</code>, <code>S603</code>, <code>S607</code>,
<code>S609</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27687">#27687</a>)</li>
<li>[<code>pylint</code>] Allow <code>continue</code> in
<code>finally</code> on Python 3.8 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27626">#27626</a>)</li>
<li>[<code>pylint</code>] Fix <code>PLE1307</code> false positive with
bools (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27651">#27651</a>)</li>
<li>[<code>pylint</code>] Fix false positives and negatives with
<code>%b</code> format character (<code>PLE1300</code>,
<code>PLE1307</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27560">#27560</a>)</li>
<li>[<code>pylint</code>] Improve handling of concatenated strings
(<code>PLE1300</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27659">#27659</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>numpy</code>] Make <code>np.chararray</code> autofix
backwards-compatible (<code>NPY201</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27527">#27527</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Enable PGO for Linux x86-64 Ruff releases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27570">#27570</a>)</li>
<li>Enable PGO for Linux ARM64 Ruff releases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27574">#27574</a>)</li>
<li>Enable PGO for Windows x86-64 Ruff releases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27573">#27573</a>)</li>
<li>Enable PGO for macOS ARM64 Ruff releases (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27572">#27572</a>)</li>
<li>Reduce <code>Expr</code> size to 64 bytes (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27591">#27591</a>)</li>
</ul>
<h3>CLI</h3>
<ul>
<li>Hyperlink rule codes in <code>ruff check --statistics</code> output
(<a
href="https://redirect.github.com/astral-sh/ruff/pull/27646">#27646</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>ruff</code>] Also suggest <code>asyncio.TaskGroup</code>
(<code>RUF006</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27461">#27461</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Use mimalloc v3 (<a
href="https://redirect.github.com/astral-sh/ruff/pull/27586">#27586</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/Andrej730"><code>@​Andrej730</code></a></li>
<li><a
href="https://github.com/alonfaraj"><code>@​alonfaraj</code></a></li>
<li><a
href="https://github.com/romero-deshaw"><code>@​romero-deshaw</code></a></li>
<li><a href="https://github.com/Avasam"><code>@​Avasam</code></a></li>
<li><a href="https://github.com/tjkuson"><code>@​tjkuson</code></a></li>
<li><a
href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a
href="https://github.com/chirizxc"><code>@​chirizxc</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/b0e47022cfce4f3594aa26d15ea792681430b6f6"><code>b0e4702</code></a>
Bump 0.16.3 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27723">#27723</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/ecdd401fdbc5b0b22e18759c8bd25cda452e8b32"><code>ecdd401</code></a>
[ty] Separate script and uv modules from project metadata (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27720">#27720</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/126352467217bebfa4cb86fd3c4d20820322d9e3"><code>1263524</code></a>
[ty] Simplify display implementations with std::fmt::from_fn (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27718">#27718</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/59196baedf23c9876d1fcf1fa2ae78f80d306f94"><code>59196ba</code></a>
[ty] Unify polarity-aware relation construction (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27707">#27707</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/b8c5e73abe5b15a74fb066e474d30397d1421cfe"><code>b8c5e73</code></a>
[ty] Disable CodSpeed cycle estimation for instrumented benchmarks (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27706">#27706</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/2b0d21094e2a55491bff60c07fd6f8803876cae5"><code>2b0d210</code></a>
[ty] Centralize matched argument relations (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27705">#27705</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/a9130f3381fe137626d22288c0d45f996541ca7e"><code>a9130f3</code></a>
[<code>pyupgrade</code>] Add rule to replace <code>while 1</code> with
<code>while True</code> (<code>while-one</code>, `...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/c64c7d6dad1e0a4966ce578b2c03af1e8e7673e1"><code>c64c7d6</code></a>
[ty] Model try exception flow with operation checkpoints (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27471">#27471</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/9dea5ef180b3de748b5fe45787056716f235d11a"><code>9dea5ef</code></a>
[ty] Avoid deriving sequents for typevars with concrete bounds (<a
href="https://redirect.github.com/astral-sh/ruff/issues/27587">#27587</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/9798e88de673ec73051980ebd9aeb681161f3c27"><code>9798e88</code></a>
[ty] Preserve enum exhaustiveness with custom <em>missing</em> methods
(<a
href="https://redirect.github.com/astral-sh/ruff/issues/27700">#27700</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.16.1...0.16.3">compare
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

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.16.3</h2>
<h2>Release Notes</h2>
<p>Released on 2026-08-13.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>pylint</code>] Fix false negatives on negative numbers (<code>PLR6104</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27251">#27251</a>)</li>
<li>[<code>pyupgrade</code>] Add rule to replace <code>while 1</code> with <code>while True</code> (<code>UP048</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27190">#27190</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-bandit</code>] Also check keyword arguments (<code>S602</code>, <code>S603</code>, <code>S607</code>, <code>S609</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27687">#27687</a>)</li>
<li>[<code>pylint</code>] Allow <code>continue</code> in <code>finally</code> on Python 3.8 (<a href="https://redirect.github.com/astral-sh/ruff/pull/27626">#27626</a>)</li>
<li>[<code>pylint</code>] Fix <code>PLE1307</code> false positive with bools (<a href="https://redirect.github.com/astral-sh/ruff/pull/27651">#27651</a>)</li>
<li>[<code>pylint</code>] Fix false positives and negatives with <code>%b</code> format character (<code>PLE1300</code>, <code>PLE1307</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27560">#27560</a>)</li>
<li>[<code>pylint</code>] Improve handling of concatenated strings (<code>PLE1300</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27659">#27659</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>numpy</code>] Make <code>np.chararray</code> autofix backwards-compatible (<code>NPY201</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27527">#27527</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Enable PGO for Linux x86-64 Ruff releases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27570">#27570</a>)</li>
<li>Enable PGO for Linux ARM64 Ruff releases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27574">#27574</a>)</li>
<li>Enable PGO for Windows x86-64 Ruff releases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27573">#27573</a>)</li>
<li>Enable PGO for macOS ARM64 Ruff releases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27572">#27572</a>)</li>
<li>Reduce <code>Expr</code> size to 64 bytes (<a href="https://redirect.github.com/astral-sh/ruff/pull/27591">#27591</a>)</li>
</ul>
<h3>CLI</h3>
<ul>
<li>Hyperlink rule codes in <code>ruff check --statistics</code> output (<a href="https://redirect.github.com/astral-sh/ruff/pull/27646">#27646</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>ruff</code>] Also suggest <code>asyncio.TaskGroup</code> (<code>RUF006</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27461">#27461</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Use mimalloc v3 (<a href="https://redirect.github.com/astral-sh/ruff/pull/27586">#27586</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/Andrej730"><code>@​Andrej730</code></a></li>
<li><a href="https://github.com/alonfaraj"><code>@​alonfaraj</code></a></li>
<li><a href="https://github.com/romero-deshaw"><code>@​romero-deshaw</code></a></li>
<li><a href="https://github.com/Avasam"><code>@​Avasam</code></a></li>
<li><a href="https://github.com/tjkuson"><code>@​tjkuson</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.16.3</h2>
<p>Released on 2026-08-13.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>pylint</code>] Fix false negatives on negative numbers (<code>PLR6104</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27251">#27251</a>)</li>
<li>[<code>pyupgrade</code>] Add rule to replace <code>while 1</code> with <code>while True</code> (<code>UP048</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27190">#27190</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>[<code>flake8-bandit</code>] Also check keyword arguments (<code>S602</code>, <code>S603</code>, <code>S607</code>, <code>S609</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27687">#27687</a>)</li>
<li>[<code>pylint</code>] Allow <code>continue</code> in <code>finally</code> on Python 3.8 (<a href="https://redirect.github.com/astral-sh/ruff/pull/27626">#27626</a>)</li>
<li>[<code>pylint</code>] Fix <code>PLE1307</code> false positive with bools (<a href="https://redirect.github.com/astral-sh/ruff/pull/27651">#27651</a>)</li>
<li>[<code>pylint</code>] Fix false positives and negatives with <code>%b</code> format character (<code>PLE1300</code>, <code>PLE1307</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27560">#27560</a>)</li>
<li>[<code>pylint</code>] Improve handling of concatenated strings (<code>PLE1300</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27659">#27659</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>numpy</code>] Make <code>np.chararray</code> autofix backwards-compatible (<code>NPY201</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27527">#27527</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Enable PGO for Linux x86-64 Ruff releases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27570">#27570</a>)</li>
<li>Enable PGO for Linux ARM64 Ruff releases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27574">#27574</a>)</li>
<li>Enable PGO for Windows x86-64 Ruff releases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27573">#27573</a>)</li>
<li>Enable PGO for macOS ARM64 Ruff releases (<a href="https://redirect.github.com/astral-sh/ruff/pull/27572">#27572</a>)</li>
<li>Reduce <code>Expr</code> size to 64 bytes (<a href="https://redirect.github.com/astral-sh/ruff/pull/27591">#27591</a>)</li>
</ul>
<h3>CLI</h3>
<ul>
<li>Hyperlink rule codes in <code>ruff check --statistics</code> output (<a href="https://redirect.github.com/astral-sh/ruff/pull/27646">#27646</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>[<code>ruff</code>] Also suggest <code>asyncio.TaskGroup</code> (<code>RUF006</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/27461">#27461</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Use mimalloc v3 (<a href="https://redirect.github.com/astral-sh/ruff/pull/27586">#27586</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/Andrej730"><code>@​Andrej730</code></a></li>
<li><a href="https://github.com/alonfaraj"><code>@​alonfaraj</code></a></li>
<li><a href="https://github.com/romero-deshaw"><code>@​romero-deshaw</code></a></li>
<li><a href="https://github.com/Avasam"><code>@​Avasam</code></a></li>
<li><a href="https://github.com/tjkuson"><code>@​tjkuson</code></a></li>
<li><a href="https://github.com/charliermarsh"><code>@​charliermarsh</code></a></li>
<li><a href="https://github.com/chirizxc"><code>@​chirizxc</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/b0e47022cfce4f3594aa26d15ea792681430b6f6"><code>b0e4702</code></a> Bump 0.16.3 (<a href="https://redirect.github.com/astral-sh/ruff/issues/27723">#27723</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/ecdd401fdbc5b0b22e18759c8bd25cda452e8b32"><code>ecdd401</code></a> [ty] Separate script and uv modules from project metadata (<a href="https://redirect.github.com/astral-sh/ruff/issues/27720">#27720</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/126352467217bebfa4cb86fd3c4d20820322d9e3"><code>1263524</code></a> [ty] Simplify display implementations with std::fmt::from_fn (<a href="https://redirect.github.com/astral-sh/ruff/issues/27718">#27718</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/59196baedf23c9876d1fcf1fa2ae78f80d306f94"><code>59196ba</code></a> [ty] Unify polarity-aware relation construction (<a href="https://redirect.github.com/astral-sh/ruff/issues/27707">#27707</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/b8c5e73abe5b15a74fb066e474d30397d1421cfe"><code>b8c5e73</code></a> [ty] Disable CodSpeed cycle estimation for instrumented benchmarks (<a href="https://redirect.github.com/astral-sh/ruff/issues/27706">#27706</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/2b0d21094e2a55491bff60c07fd6f8803876cae5"><code>2b0d210</code></a> [ty] Centralize matched argument relations (<a href="https://redirect.github.com/astral-sh/ruff/issues/27705">#27705</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/a9130f3381fe137626d22288c0d45f996541ca7e"><code>a9130f3</code></a> [<code>pyupgrade</code>] Add rule to replace <code>while 1</code> with <code>while True</code> (<code>while-one</code>, `...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/c64c7d6dad1e0a4966ce578b2c03af1e8e7673e1"><code>c64c7d6</code></a> [ty] Model try exception flow with operation checkpoints (<a href="https://redirect.github.com/astral-sh/ruff/issues/27471">#27471</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/9dea5ef180b3de748b5fe45787056716f235d11a"><code>9dea5ef</code></a> [ty] Avoid deriving sequents for typevars with concrete bounds (<a href="https://redirect.github.com/astral-sh/ruff/issues/27587">#27587</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/9798e88de673ec73051980ebd9aeb681161f3c27"><code>9798e88</code></a> [ty] Preserve enum exhaustiveness with custom <em>missing</em> methods (<a href="https://redirect.github.com/astral-sh/ruff/issues/27700">#27700</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.16.1...0.16.3">compare view</a></li>
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

## chore(deps): update openai requirement from <2.53.0,>=2.52.0 to >=3.0.0,<3.1.0 in /services/claw-interface (#3489)

- **SHA**: `e34ebac6eb71159f870e09c33c13fdb92f3e0d16`
- **作者**: dependabot[bot]
- **日期**: 2026-08-24T08:39:45Z
- **PR**: #3489

### Commit Message

```
chore(deps): update openai requirement from <2.53.0,>=2.52.0 to >=3.0.0,<3.1.0 in /services/claw-interface (#3489)

Updates the requirements on
[openai](https://github.com/openai/openai-python) to permit the latest
version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/releases">openai's
releases</a>.</em></p>
<blockquote>
<h2>v3.0.0</h2>
<h2><a
href="https://github.com/openai/openai-python/compare/v2.54.0...v3.0.0">3.0.0</a>
(2026-08-12)</h2>
<h3>⚠ BREAKING CHANGES</h3>
<ul>
<li><strong>api:</strong> HTTPX2 is now the default HTTP client, and
<code>httpx</code> is no longer installed automatically. Applications
using custom HTTPX clients, transports, or configuration objects must
migrate to their HTTPX2 equivalents or use the temporary, runtime-only
legacy HTTPX escape hatch. See the <a
href="https://github.com/openai/openai-python/blob/main/httpx2.md">HTTPX2
migration guide</a>.</li>
</ul>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> migrate to HTTPX2 (<a
href="https://redirect.github.com/openai/openai-python/pull/3594">#3594</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's
changelog</a>.</em></p>
<blockquote>
<h2><a
href="https://github.com/openai/openai-python/compare/v2.54.0...v3.0.0">3.0.0</a>
(2026-08-12)</h2>
<h3>⚠ BREAKING CHANGES</h3>
<ul>
<li><strong>api:</strong> HTTPX2 is now the default HTTP client, and
<code>httpx</code> is no longer installed automatically. Applications
using custom HTTPX clients, transports, or configuration objects must
migrate to their HTTPX2 equivalents or use the temporary, runtime-only
legacy HTTPX escape hatch. See the <a
href="https://github.com/openai/openai-python/blob/main/httpx2.md">HTTPX2
migration guide</a>.</li>
</ul>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> migrate to HTTPX2 (<a
href="https://redirect.github.com/openai/openai-python/pull/3594">#3594</a>)</li>
</ul>
<h2><a
href="https://github.com/openai/openai-python/compare/v2.53.0...v2.54.0">2.54.0</a>
(2026-08-11)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add new Responses model identifiers (<a
href="https://redirect.github.com/openai/openai-python/issues/3595">#3595</a>)
(<a
href="https://github.com/openai/openai-python/commit/06527878b8759ba52f28ab53e4d95a33989700d0">0652787</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> clarify audio upload metadata requirements (<a
href="https://redirect.github.com/openai/openai-python/issues/3596">#3596</a>)
(<a
href="https://github.com/openai/openai-python/commit/28888f9cc1635dc1247c400a8054c836abc2c129">28888f9</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>api:</strong> Update generated-file header attribution to
Castiron (<a
href="https://redirect.github.com/openai/openai-python/issues/3583">#3583</a>)
(<a
href="https://github.com/openai/openai-python/commit/ea17fda01d7067a6d829effa437952a09f2bb3a3">ea17fda</a>)</li>
</ul>
<h2><a
href="https://github.com/openai/openai-python/compare/v2.52.1...v2.53.0">2.53.0</a>
(2026-08-03)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add gpt-5.5 and tool name/namespace to
Responses types (<a
href="https://redirect.github.com/openai/openai-python/issues/3569">#3569</a>)
(<a
href="https://github.com/openai/openai-python/commit/dd1202d5dacff985861289c1d9c46996ded2d2a5">dd1202d</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>ci:</strong> avoid NumPy source builds and duplicate HTTPX
coverage (<a
href="https://redirect.github.com/openai/openai-python/issues/3573">#3573</a>)
(<a
href="https://github.com/openai/openai-python/commit/b58332f8a0717f7b1effb1788a594011cee6e02f">b58332f</a>)</li>
</ul>
<h2>2.52.1 (2026-07-31)</h2>
<p>Full Changelog: <a
href="https://github.com/openai/openai-python/compare/v2.52.0...v2.52.1">v2.52.0...v2.52.1</a></p>
<h3>Chores</h3>
<ul>
<li><strong>ci:</strong> pin setup-uv v5 to its underlying commit (<a
href="https://redirect.github.com/openai/openai-python/issues/3560">#3560</a>)
(<a
href="https://github.com/openai/openai-python/commit/cbdc98b6c1e21df7ee43d13b5de7243c6ed1ee7f">cbdc98b</a>)</li>
</ul>
<h2>2.52.0 (2026-07-31)</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/openai/openai-python/commit/8bb0e14e58b537baa216fd483e2b950907063470"><code>8bb0e14</code></a>
release: 3.0.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3598">#3598</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/ae8c3d5d8be96c8253e5875e7c79b646a0c239d6"><code>ae8c3d5</code></a>
feat(api)!: migrate to HTTPX2 (<a
href="https://redirect.github.com/openai/openai-python/issues/3594">#3594</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/03b3ec474241fe3a73c4818dc6b886da28faaf91"><code>03b3ec4</code></a>
release: 2.54.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3592">#3592</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/28888f9cc1635dc1247c400a8054c836abc2c129"><code>28888f9</code></a>
fix(api): clarify audio upload metadata requirements (<a
href="https://redirect.github.com/openai/openai-python/issues/3596">#3596</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/06527878b8759ba52f28ab53e4d95a33989700d0"><code>0652787</code></a>
feat(api): Add new Responses model identifiers (<a
href="https://redirect.github.com/openai/openai-python/issues/3595">#3595</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/ea17fda01d7067a6d829effa437952a09f2bb3a3"><code>ea17fda</code></a>
chore(api): Update generated-file header attribution to Castiron (<a
href="https://redirect.github.com/openai/openai-python/issues/3583">#3583</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/0c09a3fe815184f0a46fbf18b1aba84a467c854e"><code>0c09a3f</code></a>
ci: use GitHub App for Release Please (<a
href="https://redirect.github.com/openai/openai-python/issues/3577">#3577</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/5e36cd326fa2ebe00260386e7a27fe1c8c02d4fd"><code>5e36cd3</code></a>
release: 2.53.0 (<a
href="https://redirect.github.com/openai/openai-python/issues/3575">#3575</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/875a5c21353f43e6a4c3810c1cbaf56980f27f7b"><code>875a5c2</code></a>
ci: prepare checks for merge queue (<a
href="https://redirect.github.com/openai/openai-python/issues/3574">#3574</a>)</li>
<li><a
href="https://github.com/openai/openai-python/commit/b58332f8a0717f7b1effb1788a594011cee6e02f"><code>b58332f</code></a>
fix(ci): avoid NumPy source builds and duplicate HTTPX coverage (<a
href="https://redirect.github.com/openai/openai-python/issues/3573">#3573</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/openai/openai-python/compare/v2.52.0...v3.0.0">compare
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
<h2>v3.0.0</h2>
<h2><a href="https://github.com/openai/openai-python/compare/v2.54.0...v3.0.0">3.0.0</a> (2026-08-12)</h2>
<h3>⚠ BREAKING CHANGES</h3>
<ul>
<li><strong>api:</strong> HTTPX2 is now the default HTTP client, and <code>httpx</code> is no longer installed automatically. Applications using custom HTTPX clients, transports, or configuration objects must migrate to their HTTPX2 equivalents or use the temporary, runtime-only legacy HTTPX escape hatch. See the <a href="https://github.com/openai/openai-python/blob/main/httpx2.md">HTTPX2 migration guide</a>.</li>
</ul>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> migrate to HTTPX2 (<a href="https://redirect.github.com/openai/openai-python/pull/3594">#3594</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/openai/openai-python/blob/main/CHANGELOG.md">openai's changelog</a>.</em></p>
<blockquote>
<h2><a href="https://github.com/openai/openai-python/compare/v2.54.0...v3.0.0">3.0.0</a> (2026-08-12)</h2>
<h3>⚠ BREAKING CHANGES</h3>
<ul>
<li><strong>api:</strong> HTTPX2 is now the default HTTP client, and <code>httpx</code> is no longer installed automatically. Applications using custom HTTPX clients, transports, or configuration objects must migrate to their HTTPX2 equivalents or use the temporary, runtime-only legacy HTTPX escape hatch. See the <a href="https://github.com/openai/openai-python/blob/main/httpx2.md">HTTPX2 migration guide</a>.</li>
</ul>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> migrate to HTTPX2 (<a href="https://redirect.github.com/openai/openai-python/pull/3594">#3594</a>)</li>
</ul>
<h2><a href="https://github.com/openai/openai-python/compare/v2.53.0...v2.54.0">2.54.0</a> (2026-08-11)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add new Responses model identifiers (<a href="https://redirect.github.com/openai/openai-python/issues/3595">#3595</a>) (<a href="https://github.com/openai/openai-python/commit/06527878b8759ba52f28ab53e4d95a33989700d0">0652787</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>api:</strong> clarify audio upload metadata requirements (<a href="https://redirect.github.com/openai/openai-python/issues/3596">#3596</a>) (<a href="https://github.com/openai/openai-python/commit/28888f9cc1635dc1247c400a8054c836abc2c129">28888f9</a>)</li>
</ul>
<h3>Chores</h3>
<ul>
<li><strong>api:</strong> Update generated-file header attribution to Castiron (<a href="https://redirect.github.com/openai/openai-python/issues/3583">#3583</a>) (<a href="https://github.com/openai/openai-python/commit/ea17fda01d7067a6d829effa437952a09f2bb3a3">ea17fda</a>)</li>
</ul>
<h2><a href="https://github.com/openai/openai-python/compare/v2.52.1...v2.53.0">2.53.0</a> (2026-08-03)</h2>
<h3>Features</h3>
<ul>
<li><strong>api:</strong> Add gpt-5.5 and tool name/namespace to Responses types (<a href="https://redirect.github.com/openai/openai-python/issues/3569">#3569</a>) (<a href="https://github.com/openai/openai-python/commit/dd1202d5dacff985861289c1d9c46996ded2d2a5">dd1202d</a>)</li>
</ul>
<h3>Bug Fixes</h3>
<ul>
<li><strong>ci:</strong> avoid NumPy source builds and duplicate HTTPX coverage (<a href="https://redirect.github.com/openai/openai-python/issues/3573">#3573</a>) (<a href="https://github.com/openai/openai-python/commit/b58332f8a0717f7b1effb1788a594011cee6e02f">b58332f</a>)</li>
</ul>
<h2>2.52.1 (2026-07-31)</h2>
<p>Full Changelog: <a href="https://github.com/openai/openai-python/compare/v2.52.0...v2.52.1">v2.52.0...v2.52.1</a></p>
<h3>Chores</h3>
<ul>
<li><strong>ci:</strong> pin setup-uv v5 to its underlying commit (<a href="https://redirect.github.com/openai/openai-python/issues/3560">#3560</a>) (<a href="https://github.com/openai/openai-python/commit/cbdc98b6c1e21df7ee43d13b5de7243c6ed1ee7f">cbdc98b</a>)</li>
</ul>
<h2>2.52.0 (2026-07-31)</h2>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/openai/openai-python/commit/8bb0e14e58b537baa216fd483e2b950907063470"><code>8bb0e14</code></a> release: 3.0.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3598">#3598</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/ae8c3d5d8be96c8253e5875e7c79b646a0c239d6"><code>ae8c3d5</code></a> feat(api)!: migrate to HTTPX2 (<a href="https://redirect.github.com/openai/openai-python/issues/3594">#3594</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/03b3ec474241fe3a73c4818dc6b886da28faaf91"><code>03b3ec4</code></a> release: 2.54.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3592">#3592</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/28888f9cc1635dc1247c400a8054c836abc2c129"><code>28888f9</code></a> fix(api): clarify audio upload metadata requirements (<a href="https://redirect.github.com/openai/openai-python/issues/3596">#3596</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/06527878b8759ba52f28ab53e4d95a33989700d0"><code>0652787</code></a> feat(api): Add new Responses model identifiers (<a href="https://redirect.github.com/openai/openai-python/issues/3595">#3595</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/ea17fda01d7067a6d829effa437952a09f2bb3a3"><code>ea17fda</code></a> chore(api): Update generated-file header attribution to Castiron (<a href="https://redirect.github.com/openai/openai-python/issues/3583">#3583</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/0c09a3fe815184f0a46fbf18b1aba84a467c854e"><code>0c09a3f</code></a> ci: use GitHub App for Release Please (<a href="https://redirect.github.com/openai/openai-python/issues/3577">#3577</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/5e36cd326fa2ebe00260386e7a27fe1c8c02d4fd"><code>5e36cd3</code></a> release: 2.53.0 (<a href="https://redirect.github.com/openai/openai-python/issues/3575">#3575</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/875a5c21353f43e6a4c3810c1cbaf56980f27f7b"><code>875a5c2</code></a> ci: prepare checks for merge queue (<a href="https://redirect.github.com/openai/openai-python/issues/3574">#3574</a>)</li>
<li><a href="https://github.com/openai/openai-python/commit/b58332f8a0717f7b1effb1788a594011cee6e02f"><code>b58332f</code></a> fix(ci): avoid NumPy source builds and duplicate HTTPX coverage (<a href="https://redirect.github.com/openai/openai-python/issues/3573">#3573</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/openai/openai-python/compare/v2.52.0...v3.0.0">compare view</a></li>
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

## fix(runtime): restore v2 agents after subscription renewal (#3491)

- **SHA**: `2ba43d8ce927824ec5b7a7ffbd0ea724a8c90a54`
- **作者**: kaka-srp
- **日期**: 2026-08-24T08:06:54Z
- **PR**: #3491

### Commit Message

```
fix(runtime): restore v2 agents after subscription renewal (#3491)

## Summary

- restore subscription-expired Engine v2 workspaces when effective
personal subscription access returns
- persist cleanup provenance for lifecycle state, enabled schedules, and
enabled channels so recovery restores only state disabled by expiry
- resume stale expiry cleanup while access remains absent, preventing
crashed cleanup attempts from leaving runtime triggers active
- scan non-restorable stale cleanup rows without allowing them into
inverse recovery
- fence and renew cleanup/recovery leases between bounded remote calls
- reconcile missed callbacks and crashed cleanup/recovery attempts with
bounded retry scheduling
- preserve Engine startup semantics where `desired_state=running`,
`render_ok=true`, and `actual_state=activating` is a successful accepted
start
- keep manual-review, team-org, enterprise handoff, and legacy FastClaw
resources outside destructive personal-expiry reconciliation

## Root cause

Subscription expiry correctly stopped Engine lifecycle execution,
disabled ACS channels and user schedules, and marked Engine workspaces
disabled. Billing v2 renewal fulfillment restored entitlement, credits,
model access, and resource class, but it had no inverse operation for
the v2 runtime cleanup. The account therefore became entitled while its
Engine workspace remained disabled.

The fix records a durable cleanup snapshot before remote mutation and
restores it after access returns. Cleanup and recovery use independent
renewable leases, handle stale or unleased `suspending` rows, capture
shared migrated Computer lifecycle intent before any stop, and defer
failed eligibility lookups so one owner cannot starve the bounded
reconciler page. If access is confirmed `EXPIRED` or `FREE/NONE` in the
same current personal org, reconciliation resumes strict expiry cleanup
before deferring completed recovery candidates. Ambiguous/manual-review
access and org mismatches never enter destructive cleanup.

The affected production user was restored manually before this code is
deployed.

## Test plan

- [x] 103 focused unit tests covering cleanup, recovery, billing
fulfillment, enterprise handoff, scheduler, repository fencing, indexes,
manual-review/team guards, non-restorable stale cleanup, and lost-lease
behavior
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] independent agent review after each correction: no remaining P0-P2
findings
```

### PR Body

## Summary

- restore subscription-expired Engine v2 workspaces when effective personal subscription access returns
- persist cleanup provenance for lifecycle state, enabled schedules, and enabled channels so recovery restores only state disabled by expiry
- resume stale expiry cleanup while access remains absent, preventing crashed cleanup attempts from leaving runtime triggers active
- scan non-restorable stale cleanup rows without allowing them into inverse recovery
- fence and renew cleanup/recovery leases between bounded remote calls
- reconcile missed callbacks and crashed cleanup/recovery attempts with bounded retry scheduling
- preserve Engine startup semantics where `desired_state=running`, `render_ok=true`, and `actual_state=activating` is a successful accepted start
- keep manual-review, team-org, enterprise handoff, and legacy FastClaw resources outside destructive personal-expiry reconciliation

## Root cause

Subscription expiry correctly stopped Engine lifecycle execution, disabled ACS channels and user schedules, and marked Engine workspaces disabled. Billing v2 renewal fulfillment restored entitlement, credits, model access, and resource class, but it had no inverse operation for the v2 runtime cleanup. The account therefore became entitled while its Engine workspace remained disabled.

The fix records a durable cleanup snapshot before remote mutation and restores it after access returns. Cleanup and recovery use independent renewable leases, handle stale or unleased `suspending` rows, capture shared migrated Computer lifecycle intent before any stop, and defer failed eligibility lookups so one owner cannot starve the bounded reconciler page. If access is confirmed `EXPIRED` or `FREE/NONE` in the same current personal org, reconciliation resumes strict expiry cleanup before deferring completed recovery candidates. Ambiguous/manual-review access and org mismatches never enter destructive cleanup.

The affected production user was restored manually before this code is deployed.

## Test plan

- [x] 103 focused unit tests covering cleanup, recovery, billing fulfillment, enterprise handoff, scheduler, repository fencing, indexes, manual-review/team guards, non-restorable stale cleanup, and lost-lease behavior
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] independent agent review after each correction: no remaining P0-P2 findings



---

## fix(web): preserve media download filenames (#3480)

- **SHA**: `ea8ea177ecb6bf1f2104afcaf01a996b236fc797`
- **作者**: rayrain-srp
- **日期**: 2026-08-24T07:23:54Z
- **PR**: #3480

### Commit Message

```
fix(web): preserve media download filenames (#3480)

## Summary

- Preserve original image and video filenames across Mattermost
attachments, replay, My Uploads, Markdown media, AssetsPanel, and
gallery navigation.
- Replace the legacy `gensmo-<timestamp>` fallback with
`zooclaw-<timestamp>` in both the browser download helper and download
proxy.
- Add regression coverage for filename propagation, raw HTML table-image
galleries, and the ZooClaw fallback.
- Linear:
[ECA-1392](https://linear.app/srpone/issue/ECA-1392/zoowork-%E4%B8%8B%E8%BD%BD%E5%9B%BE%E7%89%87%E6%97%B6%E6%96%87%E4%BB%B6%E5%90%8D%E4%BB%8D%E4%BD%BF%E7%94%A8-gensmo-timestamppng)

## Root cause

Mattermost attachment views already carried `file.name`, but the
image-preview open call forwarded only the resolved URL. The preview
context and gallery item contract also had no filename field, so the
download button received `undefined` and fell back to the old
Gensmo-branded name. Markdown and other shared download surfaces had the
same missing-name path.

## Test plan

- [x] `VITEST_MAX_WORKERS=1 bash scripts/verify-web.sh <changed web/app
paths>` (guards, full TypeScript, 351/351 related tests, ESLint)
- [x] Review follow-up scoped verification (126/126 tests, full
TypeScript, ESLint)
- [x] `bash scripts/verify-changed.sh`
- [x] Pre-commit and pre-push repository hooks
- [x] GitHub CI, including full `web-quality / test`, build, CodeQL, and
auto-review (41/41 settled without failures)

Note: the initial unscoped local Vitest run passed 9,016 tests and hit
two unrelated load-sensitive timeouts. Both affected files passed in
isolated single-worker reruns, and GitHub's full Web test suite is
green.
```

### PR Body

## Summary

- Preserve original image and video filenames across Mattermost attachments, replay, My Uploads, Markdown media, AssetsPanel, and gallery navigation.
- Replace the legacy `gensmo-<timestamp>` fallback with `zooclaw-<timestamp>` in both the browser download helper and download proxy.
- Add regression coverage for filename propagation, raw HTML table-image galleries, and the ZooClaw fallback.
- Linear: [ECA-1392](https://linear.app/srpone/issue/ECA-1392/zoowork-%E4%B8%8B%E8%BD%BD%E5%9B%BE%E7%89%87%E6%97%B6%E6%96%87%E4%BB%B6%E5%90%8D%E4%BB%8D%E4%BD%BF%E7%94%A8-gensmo-timestamppng)

## Root cause

Mattermost attachment views already carried `file.name`, but the image-preview open call forwarded only the resolved URL. The preview context and gallery item contract also had no filename field, so the download button received `undefined` and fell back to the old Gensmo-branded name. Markdown and other shared download surfaces had the same missing-name path.

## Test plan

- [x] `VITEST_MAX_WORKERS=1 bash scripts/verify-web.sh <changed web/app paths>` (guards, full TypeScript, 351/351 related tests, ESLint)
- [x] Review follow-up scoped verification (126/126 tests, full TypeScript, ESLint)
- [x] `bash scripts/verify-changed.sh`
- [x] Pre-commit and pre-push repository hooks
- [x] GitHub CI, including full `web-quality / test`, build, CodeQL, and auto-review (41/41 settled without failures)

Note: the initial unscoped local Vitest run passed 9,016 tests and hit two unrelated load-sensitive timeouts. Both affected files passed in isolated single-worker reruns, and GitHub's full Web test suite is green.


---

## fix(openclaw): allow ordinary Team Plan access (#3483)

- **SHA**: `ebd9b4f41cfc40e93915fe35c973c78d6620b0c3`
- **作者**: bill-srp
- **日期**: 2026-08-24T03:18:33Z
- **PR**: #3483

### Commit Message

```
fix(openclaw): allow ordinary Team Plan access (#3483)

## Summary
- allow ordinary Team Plan members to pass the OpenClaw access gate when
their personal Billing Summary is expired
- keep active Vertical packages allowed and expired Vertical-package
teams blocked
- share the ordinary Team Plan contract with effective model catalog
resolution

## Root cause
The OpenClaw gate checked a user's personal Billing Summary first and,
for an expired personal summary, only accepted `vertical_active` team
access. Ordinary Team Plan membership was therefore ignored even though
the team billing context reports it as active. The shared resolver now
distinguishes ordinary Team Plans from teams with a historical but
inactive Vertical agreement.

## Test plan
- [x] `pytest tests/unit/test_openclaw_subscription_gate.py
tests/unit/test_effective_model_access.py -q` — 18 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] `git diff --check`
```

### PR Body

## Summary
- allow ordinary Team Plan members to pass the OpenClaw access gate when their personal Billing Summary is expired
- keep active Vertical packages allowed and expired Vertical-package teams blocked
- share the ordinary Team Plan contract with effective model catalog resolution

## Root cause
The OpenClaw gate checked a user's personal Billing Summary first and, for an expired personal summary, only accepted `vertical_active` team access. Ordinary Team Plan membership was therefore ignored even though the team billing context reports it as active. The shared resolver now distinguishes ordinary Team Plans from teams with a historical but inactive Vertical agreement.

## Test plan
- [x] `pytest tests/unit/test_openclaw_subscription_gate.py tests/unit/test_effective_model_access.py -q` — 18 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] `git diff --check`


---

## feat(chat): render multiselect interactive cards in the webapp (#3482)

- **SHA**: `b810654f3e35ca691aaf4ec58f051b0ae78f1f1a`
- **作者**: bill-srp
- **日期**: 2026-08-24T02:57:02Z
- **PR**: #3482

### Commit Message

```
feat(chat): render multiselect interactive cards in the webapp (#3482)

## Linear
<!-- none -->

## Summary
Webapp support for the `multiselect` interactive card kind — companion
to [zooclaw-extras
#227](https://github.com/SerendipityOneInc/zooclaw-extras/pull/227),
which renders a multiselect card as N toggle buttons plus a Submit
button with selection state stored in the post itself. Design spec:
`docs/superpowers/specs/2026-08-21-chat-multiselect-cards-webapp.md`.

- **Schema** (`@zooclaw/chat-ui` `types.ts`): new `multiselect` member
of `InteractiveCardView` (`options` with server-authoritative `checked`,
`submitActionId`, `submitLabel`).
- **Parser** (`interactive-attachments.ts`): structural detection — ≥2
button actions, last id prefixed `cardmssubmit`, all preceding ids
prefixed `cardms` (Mattermost strips `integration.context` before posts
reach clients, so id shape + position is the only client-visible
signal). `checked` derives from the `✓ ` name prefix the plugin toggles
via post edits; label strips it. Non-matching shapes fall through to the
existing button-row path unchanged.
- **Renderer** (`InteractiveCards.tsx`): explicit `switch` on card kind
with a safe text-banner fallback for unknown kinds (previously a new
kind would fall into the select branch and crash). Multiselect renders
checkbox rows driven purely by props (no local selection model — state
lives in the post and updates via `post_edited`) plus a primary Submit
button disabled while nothing is checked (client-side guard for the
server's empty-submit ephemeral, which the webapp can't render).
- **Pending fix**: card `key` now includes a content signature, so the
authoritative post edit remounts the card and clears `pendingActionId`.
Previously pending never cleared on success — harmless when every click
ended the card, but it would have frozen a multiselect card after the
first toggle.
- **Float classification**: `multiselect` counts as pending, so it
floats above the composer and is suppressed inline exactly like
`buttons`/`select`.
- No transport changes: toggle and submit are plain post actions through
the existing `doPostAction`.

Out of scope (pre-existing, tracked separately): card-only posts dropped
by the replay snapshot pipeline.

## Test plan
- [x] Parser: multiselect detection with mixed checked state + `✓ `
stripping, minimum shape, plain button rows unaffected,
`cardms`-prefixed rows without a trailing submit stay a button row,
malformed shapes fall through (`interactive-attachments.unit.spec.ts`)
- [x] Renderer: checkbox/submit rendering from server state, toggle +
submit dispatch, submit disabled with zero checked, all controls
disabled while pending, pending clears on content remount, unknown-kind
fallback (`interactive-cards.test.tsx`)
- [x] Float: multiselect pending/inline/float behavior
(`interactive-card-float.unit.spec.ts`)
- [x] `bash scripts/verify-web.sh` full gate green (9,022 tests / 660
files, tsc, eslint, guards)
- [x] `@zooclaw/chat-ui` package suite 438/438 + tsc + eslint
- [ ] Live smoke against a Mattermost instance running the #227 plugin
build (blocked on #227 publish)
```

### PR Body

## Linear
<!-- none -->

## Summary
Webapp support for the `multiselect` interactive card kind — companion to [zooclaw-extras #227](https://github.com/SerendipityOneInc/zooclaw-extras/pull/227), which renders a multiselect card as N toggle buttons plus a Submit button with selection state stored in the post itself. Design spec: `docs/superpowers/specs/2026-08-21-chat-multiselect-cards-webapp.md`.

- **Schema** (`@zooclaw/chat-ui` `types.ts`): new `multiselect` member of `InteractiveCardView` (`options` with server-authoritative `checked`, `submitActionId`, `submitLabel`).
- **Parser** (`interactive-attachments.ts`): structural detection — ≥2 button actions, last id prefixed `cardmssubmit`, all preceding ids prefixed `cardms` (Mattermost strips `integration.context` before posts reach clients, so id shape + position is the only client-visible signal). `checked` derives from the `✓ ` name prefix the plugin toggles via post edits; label strips it. Non-matching shapes fall through to the existing button-row path unchanged.
- **Renderer** (`InteractiveCards.tsx`): explicit `switch` on card kind with a safe text-banner fallback for unknown kinds (previously a new kind would fall into the select branch and crash). Multiselect renders checkbox rows driven purely by props (no local selection model — state lives in the post and updates via `post_edited`) plus a primary Submit button disabled while nothing is checked (client-side guard for the server's empty-submit ephemeral, which the webapp can't render).
- **Pending fix**: card `key` now includes a content signature, so the authoritative post edit remounts the card and clears `pendingActionId`. Previously pending never cleared on success — harmless when every click ended the card, but it would have frozen a multiselect card after the first toggle.
- **Float classification**: `multiselect` counts as pending, so it floats above the composer and is suppressed inline exactly like `buttons`/`select`.
- No transport changes: toggle and submit are plain post actions through the existing `doPostAction`.

Out of scope (pre-existing, tracked separately): card-only posts dropped by the replay snapshot pipeline.

## Test plan
- [x] Parser: multiselect detection with mixed checked state + `✓ ` stripping, minimum shape, plain button rows unaffected, `cardms`-prefixed rows without a trailing submit stay a button row, malformed shapes fall through (`interactive-attachments.unit.spec.ts`)
- [x] Renderer: checkbox/submit rendering from server state, toggle + submit dispatch, submit disabled with zero checked, all controls disabled while pending, pending clears on content remount, unknown-kind fallback (`interactive-cards.test.tsx`)
- [x] Float: multiselect pending/inline/float behavior (`interactive-card-float.unit.spec.ts`)
- [x] `bash scripts/verify-web.sh` full gate green (9,022 tests / 660 files, tsc, eslint, guards)
- [x] `@zooclaw/chat-ui` package suite 438/438 + tsc + eslint
- [ ] Live smoke against a Mattermost instance running the #227 plugin build (blocked on #227 publish)


---
