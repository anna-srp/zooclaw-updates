# SerendipityOneInc/ecap-workspace commits — 2026-07-23

共 18 个 commit


## `bdf14ed1ee` (PR #3052)

- **作者**: bill-srp
- **日期**: 2026-07-23T16:03:44Z
- **SHA**: bdf14ed1ee0d9db814920e309f91ea7463003cae

### Commit message

```
feat(claw-interface): bake pack archive into engine environment and pin on install (#3052)

## Summary

**PR B of pack-environment-binding** (backend-only, claw-interface),
stacked on the now-merged PR A (#3039).

This PR ships the environment pipeline without a separate runtime
feature flag. For each current approved submission, the existing
background post-approval task repacks the archive into a normalized
`pack.zip` (workspace-root persona markdown stripped, unix modes
preserved), creates or versions a zooclaw-engine **Environment**, and
binds `environment_id` onto the Pack. Engine-agent install then pins
that environment on agent creation.

### What's in this PR

- **Task 2** — `Pack.environment_id`; `pack_repo.set_environment_id`
(first-write-wins CAS).
- **Task 3** — engine env schemas (`EngineResolvedEnvironment`,
`EngineEnvironmentCreated`, `EngineEnvironmentUploadLine`),
`EngineAgentCreated.resolved_environment`, `AgentWorkspace.environment`.
- **Task 4** — `EnvironmentsMixin` on the engine client: create /
create-version / declare-uploads / presigned PUT (no auth header) /
finalize, with the org-service vs admin-global path split.
- **Task 5** — `repack_workspace_zip` + `_open_indexed_archive` (context
manager) in `engine_pack_translation`.
- **Task 6** — persona upsert → refetch current Pack and reject
missing/superseded submissions → repack → **50 MiB size guard**
(over-cap publishes without an env, logged) → **scope split**
(first-party official `org_id==zooclaw && origin_pack_id is None` →
admin/global; everything else → org-scoped) → inline (≤1 MiB) vs
declare/PUT/finalize upload → create-vs-version → **CAS-lose
reconciliation** onto the winning env. All inside the existing
swallow-and-log guard.
- **Task 8** — `create_agent(environment_id=...)` at the top level of
`resource`; parses `resolved_environment`; maps `409
environment_not_ready` → typed `DependencyNotReadyError`.
- **Task 9** — install pins `pack.environment_id` on **create only**
(engine locks the pin after first sandbox).

### Contract verification

The create / create-version / declare-uploads request envelopes were
verified against the engine source
(`services/controld/src/http/routes-environments.ts`): bodies are
`{resource:{…}, ownership:{owner_uid, org_id}}`, `config` nested under
`resource` for versions, and the engine's `ownership` validator requires
`owner_uid` always (+ `org_id` for org scope). `owner_uid =
submission.author_uid` — the exact owner semantics still want a staging
confirmation once the Environments API goes Available.

## Test plan

- [x] RED: removing test-side flag injection made all three
environment-scope cases skip engine creation and made install omit
`environment_id`.
- [x] GREEN: the same four focused cases pass after removing the
production gate.
- [x] 54 affected unit tests pass across the post-approval pipeline,
install service, and Pack environment repo.
- [x] `ruff check .` and `ruff format --check .`.
- [x] Full `pyright app/ tests/` with the current worktree venv: 0
errors, 0 warnings.
- [x] All 8 import-linter contracts kept.
- [ ] CI runs the Mongo-backed whole-app 90% coverage gate.

Mongo, R2, HTTP, and the engine client are stubbed in the unit tests.

## Rollout

No new environment setting or deployment variable is required.
Deployment of `claw-interface` is the rollout boundary; after
deployment, new approvals immediately snapshot persona and
create/version environments.

Before deployment, confirm the Environments API is Available in staging
and smoke one first-party official + one org pack end-to-end (approve →
build ready → install → sandbox contains extracted pack files).
Cross-org store installs of env-bound org packs still fail closed until
engine env sharing exists.

## Related

Spec/plan (merged in #3035, hardened in #3039, updated here for ungated
rollout):

- `docs/superpowers/specs/2026-07-23-pack-environment-binding-design.md`
- `docs/superpowers/plans/2026-07-23-pack-environment-binding.md`
```

### PR body

## Summary

**PR B of pack-environment-binding** (backend-only, claw-interface), stacked on the now-merged PR A (#3039).

This PR ships the environment pipeline without a separate runtime feature flag. For each current approved submission, the existing background post-approval task repacks the archive into a normalized `pack.zip` (workspace-root persona markdown stripped, unix modes preserved), creates or versions a zooclaw-engine **Environment**, and binds `environment_id` onto the Pack. Engine-agent install then pins that environment on agent creation.

### What's in this PR

- **Task 2** — `Pack.environment_id`; `pack_repo.set_environment_id` (first-write-wins CAS).
- **Task 3** — engine env schemas (`EngineResolvedEnvironment`, `EngineEnvironmentCreated`, `EngineEnvironmentUploadLine`), `EngineAgentCreated.resolved_environment`, `AgentWorkspace.environment`.
- **Task 4** — `EnvironmentsMixin` on the engine client: create / create-version / declare-uploads / presigned PUT (no auth header) / finalize, with the org-service vs admin-global path split.
- **Task 5** — `repack_workspace_zip` + `_open_indexed_archive` (context manager) in `engine_pack_translation`.
- **Task 6** — persona upsert → refetch current Pack and reject missing/superseded submissions → repack → **50 MiB size guard** (over-cap publishes without an env, logged) → **scope split** (first-party official `org_id==zooclaw && origin_pack_id is None` → admin/global; everything else → org-scoped) → inline (≤1 MiB) vs declare/PUT/finalize upload → create-vs-version → **CAS-lose reconciliation** onto the winning env. All inside the existing swallow-and-log guard.
- **Task 8** — `create_agent(environment_id=...)` at the top level of `resource`; parses `resolved_environment`; maps `409 environment_not_ready` → typed `DependencyNotReadyError`.
- **Task 9** — install pins `pack.environment_id` on **create only** (engine locks the pin after first sandbox).

### Contract verification

The create / create-version / declare-uploads request envelopes were verified against the engine source (`services/controld/src/http/routes-environments.ts`): bodies are `{resource:{…}, ownership:{owner_uid, org_id}}`, `config` nested under `resource` for versions, and the engine's `ownership` validator requires `owner_uid` always (+ `org_id` for org scope). `owner_uid = submission.author_uid` — the exact owner semantics still want a staging confirmation once the Environments API goes Available.

## Test plan

- [x] RED: removing test-side flag injection made all three environment-scope cases skip engine creation and made install omit `environment_id`.
- [x] GREEN: the same four focused cases pass after removing the production gate.
- [x] 54 affected unit tests pass across the post-approval pipeline, install service, and Pack environment repo.
- [x] `ruff check .` and `ruff format --check .`.
- [x] Full `pyright app/ tests/` with the current worktree venv: 0 errors, 0 warnings.
- [x] All 8 import-linter contracts kept.
- [ ] CI runs the Mongo-backed whole-app 90% coverage gate.

Mongo, R2, HTTP, and the engine client are stubbed in the unit tests.

## Rollout

No new environment setting or deployment variable is required. Deployment of `claw-interface` is the rollout boundary; after deployment, new approvals immediately snapshot persona and create/version environments.

Before deployment, confirm the Environments API is Available in staging and smoke one first-party official + one org pack end-to-end (approve → build ready → install → sandbox contains extracted pack files). Cross-org store installs of env-bound org packs still fail closed until engine env sharing exists.

## Related

Spec/plan (merged in #3035, hardened in #3039, updated here for ungated rollout):

- `docs/superpowers/specs/2026-07-23-pack-environment-binding-design.md`
- `docs/superpowers/plans/2026-07-23-pack-environment-binding.md`



## `9551b82f53` (PR #3056)

- **作者**: bill-srp
- **日期**: 2026-07-23T14:35:39Z
- **SHA**: 9551b82f53a788680023fab4c9f416fa9d303c6d

### Commit message

```
refactor(chat): migrate thread clients to the shared post store, retire useLiveThread (#3056)

## Summary

**PR 3 of 3 — the final slice** of the unified post container refactor
(Plan A from ECA-1304; spec + plan in #3041, PRs #3050 and #3053
merged). Unlike PRs 1–2 this one is **not dark** — it changes how the
thread surfaces render: session-thread and agent-builder chat now read
from the shared Mattermost `PostStore` via `useThreadPosts`, and the
parallel `useLiveThread` container is deleted. Message-list features
(reactions, pagination, edit/delete parity in threads) now have one home
instead of two.

Implements Tasks 6–8 of the plan:

- **Clients migrated.** `SessionThreadClient` and `AgentBuilderClient`
call `useThreadPosts(conversation, initialPosts, snapshotRevision)`.
`snapshotRevision` is React Query's `dataUpdatedAt` (advances on every
successful fetch, even under structural sharing), which drives the
hook's reseed/snap-to-truth logic; `useConversationThread` now exposes
it. Sends go through `thread.sync` / `thread.remove` (store-backed
optimistic insert + rollback).
- **Cross-thread guard retired.** The old `activeRootPostIdRef` guard is
gone — in store mode a post is written into its own channel bucket and
thread views select by `root_id`, so a late send can't land in the wrong
thread.
- **`useLiveThread` deleted**, along with `reconcilePendingPosts` and
the `onPostDeleted` fanout (`deleteListenersRef` + the
`UseMattermostReturn`/provider member). The `post_deleted → removePost`
store write now serves thread views, so deleted preview posts still
disappear.
- **Tests.** `useLiveThread.unit.spec.ts` →
`thread-post-utils.unit.spec.ts` (keeps the pure-helper describes);
client specs drive WS echoes through a store-backed mock instead of the
removed fanout; a deletion-parity test is ported to `useThreadPosts`.
Net −212 lines.

## Test plan

- [x] Full local gate green: `tsc --noEmit`, `lint:ci`
(dependency-cruiser + knip — no orphaned exports after the deletion),
eslint (all changed files incl. the renamed test), `dup:src`
- [x] **Full unit suite with coverage: 534 files / 7282 tests pass,
thresholds hold** after removing `useLiveThread.ts` (88.6% stmts / 81.9%
branches / 87.4% funcs / 90.9% lines)
- [x] Client specs retain the #3024 optimistic-render assertions
unweakened (bubble appears before REST resolves, retracts on failure, no
double-render on WS echo — now driven through the store)
- [ ] CI
- [ ] **Staging latency probe (post-merge):** as with #3015/#3024,
inject delay into `POST /api/v4/posts` and confirm in a session thread +
agent-builder that the bubble appears instantly and doesn't
duplicate/vanish, and that an offline send retracts + restores the
draft. The unit suite covers these paths, but the real-Mattermost
`pending_post_id` echo is only exercisable on staging.

## Known follow-up (not in this PR)

The pre-seed render path in `useThreadPosts` (`:175-182`) can briefly
show a stale server-deleted row for one frame when reopening a
previously-visited thread whose store still holds a row whose
`post_deleted` was missed (WS gap), until the seed effect prunes it.
Flagged by Codex on #3053 and consciously deferred there. Low blast
radius (self-heals next tick) but becomes user-visible with this PR;
worth a small follow-up to filter the pre-seed selection to the fresh
snapshot's keep-set.

## Related

- Spec/Plan:
`docs/superpowers/{specs,plans}/2026-07-23-unified-post-container-*.md`
(Tasks 6–8)
- Predecessors: #3050, #3053 (merged) · Docs: #3041 · Origin issue:
https://linear.app/srpone/issue/ECA-1304
```

### PR body

## Summary

**PR 3 of 3 — the final slice** of the unified post container refactor (Plan A from ECA-1304; spec + plan in #3041, PRs #3050 and #3053 merged). Unlike PRs 1–2 this one is **not dark** — it changes how the thread surfaces render: session-thread and agent-builder chat now read from the shared Mattermost `PostStore` via `useThreadPosts`, and the parallel `useLiveThread` container is deleted. Message-list features (reactions, pagination, edit/delete parity in threads) now have one home instead of two.

Implements Tasks 6–8 of the plan:

- **Clients migrated.** `SessionThreadClient` and `AgentBuilderClient` call `useThreadPosts(conversation, initialPosts, snapshotRevision)`. `snapshotRevision` is React Query's `dataUpdatedAt` (advances on every successful fetch, even under structural sharing), which drives the hook's reseed/snap-to-truth logic; `useConversationThread` now exposes it. Sends go through `thread.sync` / `thread.remove` (store-backed optimistic insert + rollback).
- **Cross-thread guard retired.** The old `activeRootPostIdRef` guard is gone — in store mode a post is written into its own channel bucket and thread views select by `root_id`, so a late send can't land in the wrong thread.
- **`useLiveThread` deleted**, along with `reconcilePendingPosts` and the `onPostDeleted` fanout (`deleteListenersRef` + the `UseMattermostReturn`/provider member). The `post_deleted → removePost` store write now serves thread views, so deleted preview posts still disappear.
- **Tests.** `useLiveThread.unit.spec.ts` → `thread-post-utils.unit.spec.ts` (keeps the pure-helper describes); client specs drive WS echoes through a store-backed mock instead of the removed fanout; a deletion-parity test is ported to `useThreadPosts`. Net −212 lines.

## Test plan

- [x] Full local gate green: `tsc --noEmit`, `lint:ci` (dependency-cruiser + knip — no orphaned exports after the deletion), eslint (all changed files incl. the renamed test), `dup:src`
- [x] **Full unit suite with coverage: 534 files / 7282 tests pass, thresholds hold** after removing `useLiveThread.ts` (88.6% stmts / 81.9% branches / 87.4% funcs / 90.9% lines)
- [x] Client specs retain the #3024 optimistic-render assertions unweakened (bubble appears before REST resolves, retracts on failure, no double-render on WS echo — now driven through the store)
- [ ] CI
- [ ] **Staging latency probe (post-merge):** as with #3015/#3024, inject delay into `POST /api/v4/posts` and confirm in a session thread + agent-builder that the bubble appears instantly and doesn't duplicate/vanish, and that an offline send retracts + restores the draft. The unit suite covers these paths, but the real-Mattermost `pending_post_id` echo is only exercisable on staging.

## Known follow-up (not in this PR)

The pre-seed render path in `useThreadPosts` (`:175-182`) can briefly show a stale server-deleted row for one frame when reopening a previously-visited thread whose store still holds a row whose `post_deleted` was missed (WS gap), until the seed effect prunes it. Flagged by Codex on #3053 and consciously deferred there. Low blast radius (self-heals next tick) but becomes user-visible with this PR; worth a small follow-up to filter the pre-seed selection to the fresh snapshot's keep-set.

## Related

- Spec/Plan: `docs/superpowers/{specs,plans}/2026-07-23-unified-post-container-*.md` (Tasks 6–8)
- Predecessors: #3050, #3053 (merged) · Docs: #3041 · Origin issue: https://linear.app/srpone/issue/ECA-1304



## `514e08ddbc` (PR #3048)

- **作者**: bill-srp
- **日期**: 2026-07-23T14:25:44Z
- **SHA**: 514e08ddbca19cb2182ac65f91f282f7abdeac78

### Commit message

```
feat(claw-interface): add engine-backed skills registry API (#3048)

## Summary

- add gated personal and team-org skill registry routes backed
exclusively by zooclaw-engine
- enforce visible-union reads and resource-anchor checks before
mutations
- bound uploaded archives at 50 MiB and translate safe engine validation
errors
- fail startup early when the enabled feature lacks engine configuration
- use team-only org dependencies and reject suspended memberships
consistently, including personal skill creation

This is the registry API split from #2875. It is stacked on #3047; merge
#3047 first, then retarget this PR to `main`.

Agent skill pinning is intentionally excluded and remains deferred until
ECAP has an authoritative engine-agent ownership mapping.

## Diff composition

- business code: +573 / -4
- tests: +1186 / -3
- docs: +5

## Test plan

- `pytest tests/unit/test_org_skills_routes.py
tests/unit/test_skills_manager_routes.py
tests/unit/test_skill_service.py
tests/unit/test_skill_version_service.py tests/unit/test_lifetime.py
tests/unit/test_middleware_auth_and_org.py -q` — 87 passed
- `ruff check .` — passed
- `ruff format --check .` — 1049 files already formatted
- `pyright --pythonpath <claw-interface-venv>/bin/python` on the changed
Python surface — 0 errors
- `lint-imports` — 8 contracts kept
```

### PR body

## Summary

- add gated personal and team-org skill registry routes backed exclusively by zooclaw-engine
- enforce visible-union reads and resource-anchor checks before mutations
- bound uploaded archives at 50 MiB and translate safe engine validation errors
- fail startup early when the enabled feature lacks engine configuration
- use team-only org dependencies and reject suspended memberships consistently, including personal skill creation

This is the registry API split from #2875. It is stacked on #3047; merge #3047 first, then retarget this PR to `main`.

Agent skill pinning is intentionally excluded and remains deferred until ECAP has an authoritative engine-agent ownership mapping.

## Diff composition

- business code: +573 / -4
- tests: +1186 / -3
- docs: +5

## Test plan

- `pytest tests/unit/test_org_skills_routes.py tests/unit/test_skills_manager_routes.py tests/unit/test_skill_service.py tests/unit/test_skill_version_service.py tests/unit/test_lifetime.py tests/unit/test_middleware_auth_and_org.py -q` — 87 passed
- `ruff check .` — passed
- `ruff format --check .` — 1049 files already formatted
- `pyright --pythonpath <claw-interface-venv>/bin/python` on the changed Python surface — 0 errors
- `lint-imports` — 8 contracts kept



## `142521209d` (PR #3053)

- **作者**: bill-srp
- **日期**: 2026-07-23T13:49:13Z
- **SHA**: 142521209dfc2eede97ee628f712c66ab61a5166

### Commit message

```
feat(chat): add useThreadPosts store-backed thread view (#3053)

## Summary

PR 2 of 3 for the **unified post container** refactor (Plan A from
ECA-1304; spec + plan in #3041). Follows **#3050 (PR 1, merged)** — this
branch has main merged in, so the diff is PR 2's changes only. This
slice is **dark**: the new `useThreadPosts` hook has no production
consumer yet (PR 3 wires the two thread clients onto it); existing
thread and main-chat behavior is unchanged.

Implements Tasks 3–5 of the plan:

- **`selectThreadPosts(store, channelId, rootId)`** (`post-store.ts`) —
thread view (root post + its replies) over the normalized `PostStore`.
- **Expose the store on the Mattermost context** — `UseMattermostReturn`
(and the provider `value`) gain `postStore` / `syncPosts` /
`removePost`; `PostStore` moves to `types.ts` (leaf, no import cycle).
The context previously exposed only the derived `messages` and the WS
fanouts.
- **`useThreadPosts` hook** (`session-thread/useThreadPosts.ts`) —
store-backed thread posts. It seeds the one-shot `fetchThread` snapshot
via a `thread-seed` sync (which never advances the reconnect-backfill
watermark), **gated by `sameThreadPosts`** so equivalent
window-focus/reconnect refetches don't re-seed; **snaps to server truth
on seed** (evicts selected rows absent from the fresh snapshot — e.g. a
`post_deleted` missed during a WS outage — while keeping optimistic
pendings and rows newer than the snapshot); and falls back to a
**root-scoped local overlay** when no Mattermost provider is present
(session threads can share one channel, so channel scoping alone would
leak a late send across threads). The seed effect reads the store
through a ref so it never depends on `postStore` (which would re-seed on
every WS post and resurrect deletions).
- **Extract `upsertThreadPost` / `removeThreadPost` /
`sameThreadPosts`** into `thread-post-utils.ts`; `useLiveThread` and the
two thread clients import the two helpers from there.
`reconcilePendingPosts` / `useLiveThread` stay in place until PR 3
deletes them.

Also extracted `useDisconnectOnUnmount` in `MattermostProvider`
(behavior-preserving move of the existing ref + unmount-cleanup effects)
to stay under the 300-line function limit after adding the 3 context
fields.

## Test plan

- [x] `tsc --noEmit`, `lint:ci` (dependency-cruiser + knip), eslint, and
vitest all green locally
- [x] New unit tests: `selectThreadPosts` (3), `useThreadPosts` (12 —
store mode: seed source, WS-first/REST-first ordering, failed-send
remove, equivalent-refetch no-op, stale-row eviction, pending/newer-row
survival; no-provider: REST echo, off-screen-channel drop, thread-change
clear, late-write-from-previous-thread drop)
- [x] Existing suites green — `useMattermost`, `useLiveThread`,
`SessionThreadClient`, `agent-builder-client` (174 tests total across
the affected suites)
- [ ] CI

## Related

- Stacked on: #3050 (PR 1)
- Spec/Plan:
`docs/superpowers/{specs,plans}/2026-07-23-unified-post-container-*.md`
(Tasks 3–5)
- Docs PR: #3041 (merged) · Origin issue:
https://linear.app/srpone/issue/ECA-1304
```

### PR body

## Summary

PR 2 of 3 for the **unified post container** refactor (Plan A from ECA-1304; spec + plan in #3041). Follows **#3050 (PR 1, merged)** — this branch has main merged in, so the diff is PR 2's changes only. This slice is **dark**: the new `useThreadPosts` hook has no production consumer yet (PR 3 wires the two thread clients onto it); existing thread and main-chat behavior is unchanged.

Implements Tasks 3–5 of the plan:

- **`selectThreadPosts(store, channelId, rootId)`** (`post-store.ts`) — thread view (root post + its replies) over the normalized `PostStore`.
- **Expose the store on the Mattermost context** — `UseMattermostReturn` (and the provider `value`) gain `postStore` / `syncPosts` / `removePost`; `PostStore` moves to `types.ts` (leaf, no import cycle). The context previously exposed only the derived `messages` and the WS fanouts.
- **`useThreadPosts` hook** (`session-thread/useThreadPosts.ts`) — store-backed thread posts. It seeds the one-shot `fetchThread` snapshot via a `thread-seed` sync (which never advances the reconnect-backfill watermark), **gated by `sameThreadPosts`** so equivalent window-focus/reconnect refetches don't re-seed; **snaps to server truth on seed** (evicts selected rows absent from the fresh snapshot — e.g. a `post_deleted` missed during a WS outage — while keeping optimistic pendings and rows newer than the snapshot); and falls back to a **root-scoped local overlay** when no Mattermost provider is present (session threads can share one channel, so channel scoping alone would leak a late send across threads). The seed effect reads the store through a ref so it never depends on `postStore` (which would re-seed on every WS post and resurrect deletions).
- **Extract `upsertThreadPost` / `removeThreadPost` / `sameThreadPosts`** into `thread-post-utils.ts`; `useLiveThread` and the two thread clients import the two helpers from there. `reconcilePendingPosts` / `useLiveThread` stay in place until PR 3 deletes them.

Also extracted `useDisconnectOnUnmount` in `MattermostProvider` (behavior-preserving move of the existing ref + unmount-cleanup effects) to stay under the 300-line function limit after adding the 3 context fields.

## Test plan

- [x] `tsc --noEmit`, `lint:ci` (dependency-cruiser + knip), eslint, and vitest all green locally
- [x] New unit tests: `selectThreadPosts` (3), `useThreadPosts` (12 — store mode: seed source, WS-first/REST-first ordering, failed-send remove, equivalent-refetch no-op, stale-row eviction, pending/newer-row survival; no-provider: REST echo, off-screen-channel drop, thread-change clear, late-write-from-previous-thread drop)
- [x] Existing suites green — `useMattermost`, `useLiveThread`, `SessionThreadClient`, `agent-builder-client` (174 tests total across the affected suites)
- [ ] CI

## Related

- Stacked on: #3050 (PR 1)
- Spec/Plan: `docs/superpowers/{specs,plans}/2026-07-23-unified-post-container-*.md` (Tasks 3–5)
- Docs PR: #3041 (merged) · Origin issue: https://linear.app/srpone/issue/ECA-1304



## `a717624855` (PR #3051)

- **作者**: bill-srp
- **日期**: 2026-07-23T12:13:25Z
- **SHA**: a717624855cd9f1b13d5ca8342dbf5c53d38fb87

### Commit message

```
feat(console): show organization type in users list (#3051)

## Summary

- add the current organization type to each admin user list response
using bounded batch reads
- show `Personal` or `Team` in the dashboard console Users table
- keep users without an active organization visible with a neutral
fallback

## Why

Staff currently need to open the upgrade dialog to determine whether a
user belongs to a personal or team organization. The list should expose
that state directly without issuing one request per row.

## Testing

- `pnpm --dir web/dashboard-console test` (567 tests)
- `pnpm --dir web/dashboard-console lint`
- `pnpm --dir web/dashboard-console typecheck`
- `.venv/bin/python -m pytest tests/unit/test_account_org_repo.py
tests/unit/test_org_repo.py tests/unit/test_internal_users_routes.py -q`
(49 tests)
- Ruff, Ruff format, Pyright, and import-linter
```

### PR body

## Summary

- add the current organization type to each admin user list response using bounded batch reads
- show `Personal` or `Team` in the dashboard console Users table
- keep users without an active organization visible with a neutral fallback

## Why

Staff currently need to open the upgrade dialog to determine whether a user belongs to a personal or team organization. The list should expose that state directly without issuing one request per row.

## Testing

- `pnpm --dir web/dashboard-console test` (567 tests)
- `pnpm --dir web/dashboard-console lint`
- `pnpm --dir web/dashboard-console typecheck`
- `.venv/bin/python -m pytest tests/unit/test_account_org_repo.py tests/unit/test_org_repo.py tests/unit/test_internal_users_routes.py -q` (49 tests)
- Ruff, Ruff format, Pyright, and import-linter



## `52398c845c` (PR #3047)

- **作者**: bill-srp
- **日期**: 2026-07-23T12:06:30Z
- **SHA**: 52398c845c9634881d382ac4e45b6bccf8bae7b8

### Commit message

```
feat(claw-interface): add engine skills client contracts (#3047)

## Summary

- add typed zooclaw-engine skill registry contracts
- extend the shared engine transport for multipart, raw zip, query, and
content-type requests
- add the skills client mixin for create, list, get, version
upload/read, and delete
- document zooclaw-engine as the sole skill source of truth
- explicitly defer agent skill pinning until ECAP has an authoritative
engine-agent ownership mapping

This is the engine-client foundation split from #2875. It does not mount
API routes or enable the feature.

## Test plan

- `pytest tests/unit/test_engine_client.py
tests/unit/test_engine_client_skills.py tests/unit/test_skill_schema.py
-q` — 43 passed
- `ruff check` and `ruff format --check` on the changed Python surface
- `pyright --pythonpath <claw-interface-venv>/bin/python` on the changed
Python surface — 0 errors
- `lint-imports` — 8 contracts kept
```

### PR body

## Summary

- add typed zooclaw-engine skill registry contracts
- extend the shared engine transport for multipart, raw zip, query, and content-type requests
- add the skills client mixin for create, list, get, version upload/read, and delete
- document zooclaw-engine as the sole skill source of truth
- explicitly defer agent skill pinning until ECAP has an authoritative engine-agent ownership mapping

This is the engine-client foundation split from #2875. It does not mount API routes or enable the feature.

## Test plan

- `pytest tests/unit/test_engine_client.py tests/unit/test_engine_client_skills.py tests/unit/test_skill_schema.py -q` — 43 passed
- `ruff check` and `ruff format --check` on the changed Python surface
- `pyright --pythonpath <claw-interface-venv>/bin/python` on the changed Python surface — 0 errors
- `lint-imports` — 8 contracts kept



## `f445888283` (PR #3050)

- **作者**: bill-srp
- **日期**: 2026-07-23T11:39:22Z
- **SHA**: f4458882837334446a2d73a37951b7f3e6992530

### Commit message

```
refactor(chat): extract pure post-store transitions + thread-seed sync source (#3050)

## Summary

PR 1 of 3 for the **unified post container** refactor (Plan A from
ECA-1304; spec + plan merged in #3041). This slice is **dark** — pure
extraction + an unused new option; no consumer behavior changes, main
chat still calls `syncPosts` without opts.

Implements Tasks 1–2 of
`docs/superpowers/plans/2026-07-23-unified-post-container-plan.md`:

- **Extract pure store transitions.** `applySyncPosts` /
`applyRemovePost` in `post-store.ts` are the current
`useMattermostPosts` `setState` updater bodies, moved verbatim so
they're unit-testable directly and so thread views (PR 2) can reconcile
over the same logic. `useMattermostPosts` now delegates to them.
- **`thread-seed` sync source.** New `SyncPostsOptions` (`types.ts`). A
`thread-seed` sync (a) never advances the reconnect-backfill watermark
`lastCreateAtByChannelRef` — a one-shot thread fetch can hold posts
newer than the channel's last channel-scoped sync, and advancing the
cursor from them would make reconnect backfill skip intervening channel
posts; and (b) never downgrades a row whose `update_at` is newer than
the snapshot's copy — a thread refetch racing a streaming `post_edited`
must not roll streamed content back.
- **Root-aware `matchesPendingPost`.** The content fallback now requires
equal `root_id`, so an echo lacking `pending_post_id` can't evict a
pending row from another thread in the same channel. This also closes
the latent reverse case that exists today, where a same-text thread
reply arriving over WS could content-evict a channel-level pending.

Why this direction (store as source of truth, threads become selectors)
is documented in the spec — it inverts ECA-1304's sketch because
pagination / reconnect backfill / reactions / `resetStore` live only on
the store side.

## Test plan

- [x] `bash scripts/verify-web.sh <changed files>` — 7 CI guards + `tsc
--noEmit` + vitest (105 tests / 5 files) + eslint, all green locally
- [x] New unit tests: `applySyncPosts`/`applyRemovePost` transitions
(idempotency, exact + content-fallback pending eviction, cross-thread
non-eviction, thread-seed no-downgrade, channel isolation) and the two
watermark-guard tests
- [x] Existing `useMattermost.unit.spec.tsx` (39 tests) still green —
main-chat behavior unchanged
- [ ] CI

## Related

- Spec:
`docs/superpowers/specs/2026-07-23-unified-post-container-design.md`
- Plan:
`docs/superpowers/plans/2026-07-23-unified-post-container-plan.md`
(Tasks 1–2)
- Docs PR: #3041 (merged)
- Origin issue: https://linear.app/srpone/issue/ECA-1304
```

### PR body

## Summary

PR 1 of 3 for the **unified post container** refactor (Plan A from ECA-1304; spec + plan merged in #3041). This slice is **dark** — pure extraction + an unused new option; no consumer behavior changes, main chat still calls `syncPosts` without opts.

Implements Tasks 1–2 of `docs/superpowers/plans/2026-07-23-unified-post-container-plan.md`:

- **Extract pure store transitions.** `applySyncPosts` / `applyRemovePost` in `post-store.ts` are the current `useMattermostPosts` `setState` updater bodies, moved verbatim so they're unit-testable directly and so thread views (PR 2) can reconcile over the same logic. `useMattermostPosts` now delegates to them.
- **`thread-seed` sync source.** New `SyncPostsOptions` (`types.ts`). A `thread-seed` sync (a) never advances the reconnect-backfill watermark `lastCreateAtByChannelRef` — a one-shot thread fetch can hold posts newer than the channel's last channel-scoped sync, and advancing the cursor from them would make reconnect backfill skip intervening channel posts; and (b) never downgrades a row whose `update_at` is newer than the snapshot's copy — a thread refetch racing a streaming `post_edited` must not roll streamed content back.
- **Root-aware `matchesPendingPost`.** The content fallback now requires equal `root_id`, so an echo lacking `pending_post_id` can't evict a pending row from another thread in the same channel. This also closes the latent reverse case that exists today, where a same-text thread reply arriving over WS could content-evict a channel-level pending.

Why this direction (store as source of truth, threads become selectors) is documented in the spec — it inverts ECA-1304's sketch because pagination / reconnect backfill / reactions / `resetStore` live only on the store side.

## Test plan

- [x] `bash scripts/verify-web.sh <changed files>` — 7 CI guards + `tsc --noEmit` + vitest (105 tests / 5 files) + eslint, all green locally
- [x] New unit tests: `applySyncPosts`/`applyRemovePost` transitions (idempotency, exact + content-fallback pending eviction, cross-thread non-eviction, thread-seed no-downgrade, channel isolation) and the two watermark-guard tests
- [x] Existing `useMattermost.unit.spec.tsx` (39 tests) still green — main-chat behavior unchanged
- [ ] CI

## Related

- Spec: `docs/superpowers/specs/2026-07-23-unified-post-container-design.md`
- Plan: `docs/superpowers/plans/2026-07-23-unified-post-container-plan.md` (Tasks 1–2)
- Docs PR: #3041 (merged)
- Origin issue: https://linear.app/srpone/issue/ECA-1304



## `5d900d598d` (PR #3044)

- **作者**: bill-srp
- **日期**: 2026-07-23T11:37:03Z
- **SHA**: 5d900d598d797a5ef4a48b8d4156fad2442c5c9a

### Commit message

```
feat(org): add admin API to upgrade a personal org to a team org (#3044)

## Linear
<!-- No Linear issue for this slice; tracked by the design spec + plan
under docs/superpowers. -->

## Summary
Backend for the staff-console "upgrade a personal org to a team org"
admin API (PR 1 of 2 — the dashboard-console UI follows). Implements
Tasks 1–6 of the merged plan
`docs/superpowers/plans/2026-07-23-org-upgrade-to-team.md` (design spec:
`docs/superpowers/specs/2026-07-23-org-upgrade-to-team-design.md`).

**New endpoint** — `POST /internal/orgs/{org_id}/upgrade-to-team` →
`OrgResponse`
- Under the `/internal` aggregator, so it inherits the
`require_srp_account` (@srp.one staff) gate; the mutation additionally
depends on `require_admin_user` (env allowlist), matching the
offline-order console's tiered model.
- Body `OrgUpgradeToTeamRequest { name }` (1–128 chars, stripped,
non-blank; `extra="forbid"`) — replaces the hard-coded "Personal" org
name at upgrade time.

**Upgrade semantics** (`org_service.upgrade_org_to_team`, keyed off the
org owner `created_by`, not the admin caller):
- Rejects non-personal orgs with `org.not_personal_org`.
- Preserves an existing non-blank `mattermost_team_id`. For a legacy org
where it is missing, provisions or reuses the deterministic Mattermost
team and ensures the creator's membership before billing. Concurrent
duplicate-name 400/409 responses re-read and adopt the winning team; if
no winner is visible, the original error is re-raised.
- Converts the org's existing billing team to business mode **in place**
(`add_user_to_personal_team(created_by, team_id=billing_team_id,
billing_mode="business")`) and ensures subscription/topup wallets —
**no** plan subscription (team plan purchase happens later via the
normal flows).
- Commits `org_type`, `name`, `mattermost_team_id`, and wallet IDs via a
CAS write filtered on `org_type == "personal"`
(`org_repo.upgrade_personal_to_team`), so validation is folded into the
atomic write and a concurrent upgrade loses loudly (re-read →
`org.not_found` / `org.not_personal_org`). External steps are
idempotent, so a retry after partial failure completes the upgrade.
- `billing_team_id`, the creator membership row, quotas, and
`registration_completed` are otherwise untouched.

**Supporting change (no compat window):** `GET
/internal/users/{uid}/orgs` gains `org_type` on each `UserOrgOption` and
an **opt-in** `include_personal` query param (default `false`). The
default response stays team-only, so the already-deployed offline-orders
picker is unaffected in every deploy window; only the upcoming
org-upgrade dialog (PR 2) passes `include_personal=true`.

**Implementation note:** the org-list handler uses a plain
`include_personal: bool = False` (still a query param at runtime) rather
than `Query(default=False)`, so direct-call unit tests receive a real
`False` instead of a truthy `FieldInfo` sentinel — no `is True`
workaround needed.

## Test plan
- [x] `bash scripts/verify-py.sh` — ruff + ruff-format + pyright +
import-linter clean (8/8 contracts kept)
- [x] Unit: `pytest tests/unit/test_org_repo.py test_schema_org.py
test_org_service.py test_routes_internal_orgs.py
test_internal_users_orgs.py` — 106 passed, including legacy Mattermost
backfill/CAS persistence and concurrent create-conflict
adoption/re-raise coverage
- [x] BDD against real Mongo:
`tests/bdd/step_defs/test_org_lifecycle.py` — 4 passed (incl.
upgrade-personal-org and upgrade-team-org-rejected)
- [x] jscpd duplication guard passed
- [ ] Whole-app `--cov-fail-under=90` — CI's `python-code-quality` is
the authoritative gate

## Rollout
- Backend deploys first; dashboard-console UI (Tasks 8–10) is a
follow-up PR. No data migration, no feature flag (route is staff-gated).
```

### PR body

## Linear
<!-- No Linear issue for this slice; tracked by the design spec + plan under docs/superpowers. -->

## Summary
Backend for the staff-console "upgrade a personal org to a team org" admin API (PR 1 of 2 — the dashboard-console UI follows). Implements Tasks 1–6 of the merged plan `docs/superpowers/plans/2026-07-23-org-upgrade-to-team.md` (design spec: `docs/superpowers/specs/2026-07-23-org-upgrade-to-team-design.md`).

**New endpoint** — `POST /internal/orgs/{org_id}/upgrade-to-team` → `OrgResponse`
- Under the `/internal` aggregator, so it inherits the `require_srp_account` (@srp.one staff) gate; the mutation additionally depends on `require_admin_user` (env allowlist), matching the offline-order console's tiered model.
- Body `OrgUpgradeToTeamRequest { name }` (1–128 chars, stripped, non-blank; `extra="forbid"`) — replaces the hard-coded "Personal" org name at upgrade time.

**Upgrade semantics** (`org_service.upgrade_org_to_team`, keyed off the org owner `created_by`, not the admin caller):
- Rejects non-personal orgs with `org.not_personal_org`.
- Preserves an existing non-blank `mattermost_team_id`. For a legacy org where it is missing, provisions or reuses the deterministic Mattermost team and ensures the creator's membership before billing. Concurrent duplicate-name 400/409 responses re-read and adopt the winning team; if no winner is visible, the original error is re-raised.
- Converts the org's existing billing team to business mode **in place** (`add_user_to_personal_team(created_by, team_id=billing_team_id, billing_mode="business")`) and ensures subscription/topup wallets — **no** plan subscription (team plan purchase happens later via the normal flows).
- Commits `org_type`, `name`, `mattermost_team_id`, and wallet IDs via a CAS write filtered on `org_type == "personal"` (`org_repo.upgrade_personal_to_team`), so validation is folded into the atomic write and a concurrent upgrade loses loudly (re-read → `org.not_found` / `org.not_personal_org`). External steps are idempotent, so a retry after partial failure completes the upgrade.
- `billing_team_id`, the creator membership row, quotas, and `registration_completed` are otherwise untouched.

**Supporting change (no compat window):** `GET /internal/users/{uid}/orgs` gains `org_type` on each `UserOrgOption` and an **opt-in** `include_personal` query param (default `false`). The default response stays team-only, so the already-deployed offline-orders picker is unaffected in every deploy window; only the upcoming org-upgrade dialog (PR 2) passes `include_personal=true`.

**Implementation note:** the org-list handler uses a plain `include_personal: bool = False` (still a query param at runtime) rather than `Query(default=False)`, so direct-call unit tests receive a real `False` instead of a truthy `FieldInfo` sentinel — no `is True` workaround needed.

## Test plan
- [x] `bash scripts/verify-py.sh` — ruff + ruff-format + pyright + import-linter clean (8/8 contracts kept)
- [x] Unit: `pytest tests/unit/test_org_repo.py test_schema_org.py test_org_service.py test_routes_internal_orgs.py test_internal_users_orgs.py` — 106 passed, including legacy Mattermost backfill/CAS persistence and concurrent create-conflict adoption/re-raise coverage
- [x] BDD against real Mongo: `tests/bdd/step_defs/test_org_lifecycle.py` — 4 passed (incl. upgrade-personal-org and upgrade-team-org-rejected)
- [x] jscpd duplication guard passed
- [ ] Whole-app `--cov-fail-under=90` — CI's `python-code-quality` is the authoritative gate

## Rollout
- Backend deploys first; dashboard-console UI (Tasks 8–10) is a follow-up PR. No data migration, no feature flag (route is staff-gated).



## `256022ad8c` (PR #2997)

- **作者**: rayrain-srp
- **日期**: 2026-07-23T11:36:47Z
- **SHA**: 256022ad8c6e4bcc4cc2ef7d2911b819fdd9120d

### Commit message

```
feat(agent-builder): add live model selector (#2997)

## Linear

https://linear.app/srpone/issue/ECA-1281

## Summary

- add a Builder-only chat model resolver that preserves the existing
main-chat filtering while exposing entitled ordinary and
`agent-studio-*` discounted models
- add shared Builder-computer GET/PUT model state APIs backed by the
atomic FastClaw agent-model patch, exact runtime capability marker,
bounded active-convergence polling, and a default-on kill switch
- add the Agent Builder header selector with explicit Apply,
active/pending/error states, shared-runtime cache scope, localized
discount labels, and no restart flow
- seed the official Agent Studio model only on first install when its
explicit primary is missing; project open/update never reconciles over a
user's selection
- harden independent rollout and transport edges: old-backend 404 hides
the selector, FastClaw envelope conflicts stay non-retryable, and only
the idempotent agent-model PATCH opts into one zero-byte disconnect
replay
- preserve existing runtime-status soft-error envelopes while the new
capability gate still fails closed, and classify transient runtime
errors separately from old-image marker gaps; a valid first-install seed
write must succeed before the workspace becomes active, and model state
is visible in the header during canary testing
- make the old-image state actionable and fully visible: the disabled
control now says `Upgrade Claw to select` / `升级 Claw 后可选模型` in a
compact, non-truncating caution style
- discard any unsubmitted model draft when navigating between projects,
while keeping the confirmed model cache scoped to their shared Builder
computer
- keep the pre-write capability gate fail-closed, but after active
convergence report the fresh capability state without mislabeling an
already-applied model change as failed

Dependencies and rollout gates:

- depends on merged `zooclaw-extras#190` and `fastclaw#161`; their
staging release and functional verification are complete
- merged the current `origin/main` and resolved its Agent Builder
import-relocation conflict; this branch temporarily carries the same
one-line E2E page-reference fix as #3031 so the repository TypeScript
gate stays green until that PR lands
- `AGENT_BUILDER_MODEL_SELECTOR_ENABLED` defaults to `true`; operators
can still set it to `false` as an emergency kill switch
- after this PR is deployed to staging, complete the Task 9 real-turn
E2E before any production enablement
- this supersedes the continuous-reconcile direction in draft #2892;
leave #2892 untouched until reviewers agree on the replacement

## Test plan

- [x] `pytest -q tests/unit/test_plan_models.py
tests/unit/test_agent_builder_model_service.py
tests/unit/test_agent_builder_routes.py
tests/unit/test_openclaw_client.py` — 255 passed
- [x] focused generic managed-agent isolation tests — 2 passed
- [x] focused Agent Builder frontend service/control/client tests — 51
passed
- [x] related Builder and Agent Settings frontend regression set — 105
passed
- [x] review-fix backend client/service regressions — 179 passed
- [x] review-fix frontend compatibility/status regressions — 109 passed
- [x] post-main-merge backend regression set — 417 passed
- [x] post-main-merge Agent Builder client/control regression set — 58
passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --tsc-only` and targeted Agent Builder
ESLint
- [x] pre-push PR-size and changed-surface gate: web
guards/TypeScript/ESLint plus Ruff/Pyright/import contracts
- [ ] pre-review local `bash scripts/verify-py.sh --full` — all pytest
cases completed without test failures, but the repository-wide coverage
gate reported 89.36% against 90%
- [ ] `bash scripts/verify-web.sh` — 7160 passed and 6 unrelated
timeout/cleanup failures; each affected file passed when rerun in
isolation (160 tests total)
- [ ] deploy backend and web to staging, then execute Task 9 across
ordinary -> discounted 4.6 -> discounted 5 -> ordinary while proving
persisted, active, turn-level model, and unchanged pod/account lifecycle
```

### PR body

## Linear

https://linear.app/srpone/issue/ECA-1281

## Summary

- add a Builder-only chat model resolver that preserves the existing main-chat filtering while exposing entitled ordinary and `agent-studio-*` discounted models
- add shared Builder-computer GET/PUT model state APIs backed by the atomic FastClaw agent-model patch, exact runtime capability marker, bounded active-convergence polling, and a default-on kill switch
- add the Agent Builder header selector with explicit Apply, active/pending/error states, shared-runtime cache scope, localized discount labels, and no restart flow
- seed the official Agent Studio model only on first install when its explicit primary is missing; project open/update never reconciles over a user's selection
- harden independent rollout and transport edges: old-backend 404 hides the selector, FastClaw envelope conflicts stay non-retryable, and only the idempotent agent-model PATCH opts into one zero-byte disconnect replay
- preserve existing runtime-status soft-error envelopes while the new capability gate still fails closed, and classify transient runtime errors separately from old-image marker gaps; a valid first-install seed write must succeed before the workspace becomes active, and model state is visible in the header during canary testing
- make the old-image state actionable and fully visible: the disabled control now says `Upgrade Claw to select` / `升级 Claw 后可选模型` in a compact, non-truncating caution style
- discard any unsubmitted model draft when navigating between projects, while keeping the confirmed model cache scoped to their shared Builder computer
- keep the pre-write capability gate fail-closed, but after active convergence report the fresh capability state without mislabeling an already-applied model change as failed

Dependencies and rollout gates:

- depends on merged `zooclaw-extras#190` and `fastclaw#161`; their staging release and functional verification are complete
- merged the current `origin/main` and resolved its Agent Builder import-relocation conflict; this branch temporarily carries the same one-line E2E page-reference fix as #3031 so the repository TypeScript gate stays green until that PR lands
- `AGENT_BUILDER_MODEL_SELECTOR_ENABLED` defaults to `true`; operators can still set it to `false` as an emergency kill switch
- after this PR is deployed to staging, complete the Task 9 real-turn E2E before any production enablement
- this supersedes the continuous-reconcile direction in draft #2892; leave #2892 untouched until reviewers agree on the replacement

## Test plan

- [x] `pytest -q tests/unit/test_plan_models.py tests/unit/test_agent_builder_model_service.py tests/unit/test_agent_builder_routes.py tests/unit/test_openclaw_client.py` — 255 passed
- [x] focused generic managed-agent isolation tests — 2 passed
- [x] focused Agent Builder frontend service/control/client tests — 51 passed
- [x] related Builder and Agent Settings frontend regression set — 105 passed
- [x] review-fix backend client/service regressions — 179 passed
- [x] review-fix frontend compatibility/status regressions — 109 passed
- [x] post-main-merge backend regression set — 417 passed
- [x] post-main-merge Agent Builder client/control regression set — 58 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-web.sh --tsc-only` and targeted Agent Builder ESLint
- [x] pre-push PR-size and changed-surface gate: web guards/TypeScript/ESLint plus Ruff/Pyright/import contracts
- [ ] pre-review local `bash scripts/verify-py.sh --full` — all pytest cases completed without test failures, but the repository-wide coverage gate reported 89.36% against 90%
- [ ] `bash scripts/verify-web.sh` — 7160 passed and 6 unrelated timeout/cleanup failures; each affected file passed when rerun in isolation (160 tests total)
- [ ] deploy backend and web to staging, then execute Task 9 across ordinary -> discounted 4.6 -> discounted 5 -> ordinary while proving persisted, active, turn-level model, and unchanged pod/account lifecycle



## `acb53ee81d` (PR #3040)

- **作者**: Mori-srp
- **日期**: 2026-07-23T11:29:19Z
- **SHA**: acb53ee81d3d6466b334fce854e1ef71e49071e6

### Commit message

```
feat(web): localize homepage meta descriptions (#3040)

## What changed

- add ZooClaw homepage Meta Description copy for all 10 supported
locales (`en`, `zh`, `ja`, `ko`, `fr`, `de`, `it`, `es`, `ar`, `pt`)
- select the localized value inside `createHomepageMetadata(locale)`
- reuse the same locale-specific description for standard metadata, Open
Graph, and Twitter
- preserve the existing English description as a fallback
- add exact-value, route-level, and cross-brand regression coverage

## Why

The localized homepage URLs already have self-canonical and reciprocal
hreflang signals, but all 10 pages currently share the same English Meta
Description. This PR gives each localized homepage a matching
search/social description without changing the URL or international SEO
architecture.

The nine non-English V0 strings have stage approval to ship now.
Native/professional language review remains a follow-up content
iteration and is not represented as completed here.

## Scope and impact

This PR is intentionally limited to homepage description metadata:

- no title changes
- no canonical or hreflang changes
- no sitemap, robots, schema, routing, or OG image changes
- no visible homepage copy changes
- no `src/locales/*` changes
- no changes to default/ocean (Gensmo) metadata
- does not reintroduce the removed `landingV2.heroDescription`

Users should not see a visual UI change. Search crawlers and social
previews can receive a locale-matched description in the initial HTML.
Google may still rewrite snippets based on the query and page content.

## Validation

- targeted unit tests: 4 files / 55 tests passed
- `web/scripts/verify-web.sh`: TypeScript, 5 files / 69 tests, ESLint,
and governance guards passed
- production build: 304 / 304 static pages generated
- generated raw HTML checked for `/`, `/zh`, `/ja`, `/ko`, `/fr`, `/de`,
`/it`, `/es`, `/ar`, `/pt`
  - all 10 descriptions are distinct
  - Meta = Open Graph = Twitter on every locale
  - self-canonical is correct on every locale
  - each page has 10 locale hreflang entries plus `x-default`
- independent diff review found no blocking or P0-P2 issues
- PR size guard passed: 112 changed lines across 6 files

## Known inherited local check issue

After the production build regenerated `.next/types`, the pre-push
TypeScript check surfaced the existing
`web/app/src/app/api/download/route.ts` named export `isAllowedUrl`.
This file is unchanged by this PR (its latest history is from PR #1713).
The branch was pushed with `SKIP_VERIFY=1` only after the scoped tests,
full selected verify, ESLint, production build, raw-HTML checks, and PR
size guard had passed.
```

### PR body

## What changed

- add ZooClaw homepage Meta Description copy for all 10 supported locales (`en`, `zh`, `ja`, `ko`, `fr`, `de`, `it`, `es`, `ar`, `pt`)
- select the localized value inside `createHomepageMetadata(locale)`
- reuse the same locale-specific description for standard metadata, Open Graph, and Twitter
- preserve the existing English description as a fallback
- add exact-value, route-level, and cross-brand regression coverage

## Why

The localized homepage URLs already have self-canonical and reciprocal hreflang signals, but all 10 pages currently share the same English Meta Description. This PR gives each localized homepage a matching search/social description without changing the URL or international SEO architecture.

The nine non-English V0 strings have stage approval to ship now. Native/professional language review remains a follow-up content iteration and is not represented as completed here.

## Scope and impact

This PR is intentionally limited to homepage description metadata:

- no title changes
- no canonical or hreflang changes
- no sitemap, robots, schema, routing, or OG image changes
- no visible homepage copy changes
- no `src/locales/*` changes
- no changes to default/ocean (Gensmo) metadata
- does not reintroduce the removed `landingV2.heroDescription`

Users should not see a visual UI change. Search crawlers and social previews can receive a locale-matched description in the initial HTML. Google may still rewrite snippets based on the query and page content.

## Validation

- targeted unit tests: 4 files / 55 tests passed
- `web/scripts/verify-web.sh`: TypeScript, 5 files / 69 tests, ESLint, and governance guards passed
- production build: 304 / 304 static pages generated
- generated raw HTML checked for `/`, `/zh`, `/ja`, `/ko`, `/fr`, `/de`, `/it`, `/es`, `/ar`, `/pt`
  - all 10 descriptions are distinct
  - Meta = Open Graph = Twitter on every locale
  - self-canonical is correct on every locale
  - each page has 10 locale hreflang entries plus `x-default`
- independent diff review found no blocking or P0-P2 issues
- PR size guard passed: 112 changed lines across 6 files

## Known inherited local check issue

After the production build regenerated `.next/types`, the pre-push TypeScript check surfaced the existing `web/app/src/app/api/download/route.ts` named export `isAllowedUrl`. This file is unchanged by this PR (its latest history is from PR #1713). The branch was pushed with `SKIP_VERIFY=1` only after the scoped tests, full selected verify, ESLint, production build, raw-HTML checks, and PR size guard had passed.



## `7010b0a7c0` (PR #3039)

- **作者**: bill-srp
- **日期**: 2026-07-23T11:21:43Z
- **SHA**: 7010b0a7c0f6a0160338b29a69d5195f5ea91327

### Commit message

```
feat(claw-interface): snapshot pack persona at approval, read DB-first on engine install (#3039)

## Summary

**PR A of pack-environment-binding** (backend-only, claw-interface).
Ships the ungated persona-snapshot half of the design; the environment
pipeline lands separately in PR B behind a flag.

When a pack submission is **approved**, a best-effort post-approval
pipeline extracts the workspace-root persona markdown from the approved
archive and snapshots it into the new `ecap-pack-persona-docs`
collection. Engine-agent **install** then reads persona from that
collection (keyed by `pack_id` + `latest_submission_id`) instead of
fetching + parsing the archive on every install, falling back to the
live archive fetch for packs approved before this shipped.

### What's in this PR
- `app/schema/pack_persona.py` — `PackPersonaDoc` / `PackPersonaDocs`
typed models (engine `persona.docs` shape).
- `app/database/pack_persona_docs_repo.py` +
`PACK_PERSONA_DOCS_COLLECTION` — typed repo (`upsert` keyed on
`(pack_id, submission_id)`, `get_by_submission`). Registered in the
three import-linter repo lists.
- `app/services/pack_store/pack_environment_service.py` —
`run_post_approval(pack, submission)`: fetch archive by
**`submission.asset_id`** (not the refetched Pack row — avoids the
multi-approval wrong-archive race), translate persona, upsert. Whole
body is a swallow-and-log guard so it can never break approval.
- `review_service.approve` — hooks the pipeline after the final pack
refetch (covers the auto-approve path too, which routes through
`approve`).
- `engine_agent_install_service.install_engine_agent` — persona DB-first
with archive fallback; both the create and update engine branches
repointed.

### Deliberately NOT in this PR (→ PR B, gated by
`ZOOCLAW_ENGINE_ENVIRONMENTS_ENABLED`)
Environment creation/versioning, the archive repack
(`repack_workspace_zip`), the size guard, CAS-lose reconciliation,
engine env client, and the install-time environment pin. Persona
snapshotting is independently useful and safe to ship now.

## Test plan
- [x] `verify-py.sh` fast tier: ruff, ruff-format, pyright, all 8
import-linter contracts KEPT
- [x] 100 unit tests pass across new + related suites (persona
repo/service/hook, install service, pack services, default-model,
routes-pack-store) — no regressions
- [x] pre-commit hooks green (incl. vulture dead-code, repo-list sync,
repo return-contract)
- [ ] CI runs the mongo-backed whole-app 90% coverage gate (no local
Mongo)

Mongo, R2, and HTTP boundaries are stubbed in the new unit tests.

## Related
Design spec + plan (merged in #3035):
- `docs/superpowers/specs/2026-07-23-pack-environment-binding-design.md`
- `docs/superpowers/plans/2026-07-23-pack-environment-binding.md`
```

### PR body

## Summary

**PR A of pack-environment-binding** (backend-only, claw-interface). Ships the ungated persona-snapshot half of the design; the environment pipeline lands separately in PR B behind a flag.

When a pack submission is **approved**, a best-effort post-approval pipeline extracts the workspace-root persona markdown from the approved archive and snapshots it into the new `ecap-pack-persona-docs` collection. Engine-agent **install** then reads persona from that collection (keyed by `pack_id` + `latest_submission_id`) instead of fetching + parsing the archive on every install, falling back to the live archive fetch for packs approved before this shipped.

### What's in this PR
- `app/schema/pack_persona.py` — `PackPersonaDoc` / `PackPersonaDocs` typed models (engine `persona.docs` shape).
- `app/database/pack_persona_docs_repo.py` + `PACK_PERSONA_DOCS_COLLECTION` — typed repo (`upsert` keyed on `(pack_id, submission_id)`, `get_by_submission`). Registered in the three import-linter repo lists.
- `app/services/pack_store/pack_environment_service.py` — `run_post_approval(pack, submission)`: fetch archive by **`submission.asset_id`** (not the refetched Pack row — avoids the multi-approval wrong-archive race), translate persona, upsert. Whole body is a swallow-and-log guard so it can never break approval.
- `review_service.approve` — hooks the pipeline after the final pack refetch (covers the auto-approve path too, which routes through `approve`).
- `engine_agent_install_service.install_engine_agent` — persona DB-first with archive fallback; both the create and update engine branches repointed.

### Deliberately NOT in this PR (→ PR B, gated by `ZOOCLAW_ENGINE_ENVIRONMENTS_ENABLED`)
Environment creation/versioning, the archive repack (`repack_workspace_zip`), the size guard, CAS-lose reconciliation, engine env client, and the install-time environment pin. Persona snapshotting is independently useful and safe to ship now.

## Test plan
- [x] `verify-py.sh` fast tier: ruff, ruff-format, pyright, all 8 import-linter contracts KEPT
- [x] 100 unit tests pass across new + related suites (persona repo/service/hook, install service, pack services, default-model, routes-pack-store) — no regressions
- [x] pre-commit hooks green (incl. vulture dead-code, repo-list sync, repo return-contract)
- [ ] CI runs the mongo-backed whole-app 90% coverage gate (no local Mongo)

Mongo, R2, and HTTP boundaries are stubbed in the new unit tests.

## Related
Design spec + plan (merged in #3035):
- `docs/superpowers/specs/2026-07-23-pack-environment-binding-design.md`
- `docs/superpowers/plans/2026-07-23-pack-environment-binding.md`



## `6a351b6d70` (PR #3045)

- **作者**: bill-srp
- **日期**: 2026-07-23T11:04:18Z
- **SHA**: 6a351b6d70a2cf7aaa897fbae72b6a6c942e2629

### Commit message

```
feat(console): upgrade a personal org to team from the users screen (#3045)

## Linear
<!-- No Linear issue for this slice; tracked by the design spec + plan
under docs/superpowers. -->

## Summary
Dashboard-console UI for the "upgrade a personal org to a team org"
admin feature (PR 2 of 2 — the claw-interface backend is #3044).
Implements Tasks 8–10 of the merged plan
`docs/superpowers/plans/2026-07-23-org-upgrade-to-team.md`.

**API layer** (`app/lib/`)
- `orgUpgradeToTeamUrl` + `upgradeOrgToTeam(orgId, { name })` → `POST
/internal/orgs/{org_id}/upgrade-to-team` with bearer auth + JSON body.
- `listUserOrgs(uid, { includePersonal })` threads an opt-in flag
through `userOrgsUrl` that appends `?include_personal=true` only when
set; `UserOrgOption` gains `org_type`.
- **Offline-orders picker untouched:** the no-opts `listUserOrgs()`
builds the identical URL and same team-only response as before (the
backend default stays team-only), so the existing flow is unaffected.

**Upgrade dialog** (`app/routes/users/`)
- New per-user RowMenu action "Upgrade org to team" opening a dialog
that follows the existing grant-credits/boost pattern (controller hook +
presentational dialog): loads the user's orgs with
`include_personal=true`, shows the personal org + a required team-name
input with a note that billing switches to business mode and **no plan
is auto-subscribed**, then calls `upgradeOrgToTeam`; success invalidates
the users + org-lookup queries and surfaces the screen's success notice.
- **Robustness (from the docs-PR review):** a failed org lookup renders
a retryable error state and **never** the "No active organization" empty
state — a 500 must not read as "user has no org". The org-lookup
`useQuery` key encodes `{ includePersonal: true }` so a flagless caller
can never be served the personal-inclusive cached response. An
`org.not_personal_org` API error (already-upgraded race) shows a clear
message and keeps the dialog open.

## Test plan
- [x] `pnpm run typecheck` — clean (exit 0, wrangler + react-router
typegen + `tsc -b`)
- [x] `pnpm vitest run app/lib/claw-api.test.ts app/routes/users` — 17
files / 186 tests pass (API client URL+auth+body, includePersonal
on/off, dialog personal/team/empty/**error** states, controller
happy/blank/not-personal/**lookup-failure no-op**, view-model open/close
wiring)
- [x] `pnpm lint` — eslint clean

## Rollout
- Backend (#3044) deploys first; this consumes `POST
/internal/orgs/{org_id}/upgrade-to-team` and `?include_personal=true`.
No data migration, no feature flag (route is staff-gated).
```

### PR body

## Linear
<!-- No Linear issue for this slice; tracked by the design spec + plan under docs/superpowers. -->

## Summary
Dashboard-console UI for the "upgrade a personal org to a team org" admin feature (PR 2 of 2 — the claw-interface backend is #3044). Implements Tasks 8–10 of the merged plan `docs/superpowers/plans/2026-07-23-org-upgrade-to-team.md`.

**API layer** (`app/lib/`)
- `orgUpgradeToTeamUrl` + `upgradeOrgToTeam(orgId, { name })` → `POST /internal/orgs/{org_id}/upgrade-to-team` with bearer auth + JSON body.
- `listUserOrgs(uid, { includePersonal })` threads an opt-in flag through `userOrgsUrl` that appends `?include_personal=true` only when set; `UserOrgOption` gains `org_type`.
- **Offline-orders picker untouched:** the no-opts `listUserOrgs()` builds the identical URL and same team-only response as before (the backend default stays team-only), so the existing flow is unaffected.

**Upgrade dialog** (`app/routes/users/`)
- New per-user RowMenu action "Upgrade org to team" opening a dialog that follows the existing grant-credits/boost pattern (controller hook + presentational dialog): loads the user's orgs with `include_personal=true`, shows the personal org + a required team-name input with a note that billing switches to business mode and **no plan is auto-subscribed**, then calls `upgradeOrgToTeam`; success invalidates the users + org-lookup queries and surfaces the screen's success notice.
- **Robustness (from the docs-PR review):** a failed org lookup renders a retryable error state and **never** the "No active organization" empty state — a 500 must not read as "user has no org". The org-lookup `useQuery` key encodes `{ includePersonal: true }` so a flagless caller can never be served the personal-inclusive cached response. An `org.not_personal_org` API error (already-upgraded race) shows a clear message and keeps the dialog open.

## Test plan
- [x] `pnpm run typecheck` — clean (exit 0, wrangler + react-router typegen + `tsc -b`)
- [x] `pnpm vitest run app/lib/claw-api.test.ts app/routes/users` — 17 files / 186 tests pass (API client URL+auth+body, includePersonal on/off, dialog personal/team/empty/**error** states, controller happy/blank/not-personal/**lookup-failure no-op**, view-model open/close wiring)
- [x] `pnpm lint` — eslint clean

## Rollout
- Backend (#3044) deploys first; this consumes `POST /internal/orgs/{org_id}/upgrade-to-team` and `?include_personal=true`. No data migration, no feature flag (route is staff-gated).



## `350bb326f2` (PR #3041)

- **作者**: bill-srp
- **日期**: 2026-07-23T11:00:38Z
- **SHA**: 350bb326f2e3b68bef9eeaf10277dd95b68a10fe

### Commit message

```
docs: add unified post container design spec and implementation plan (#3041)

## Summary

Design spec + implementation plan for "Plan A" deferred from ECA-1304:
retire the parallel `useLiveThread` thread-post container by making
session-thread and agent-builder views selectors over the normalized
`PostStore`, so message-list features (optimistic rendering was
implemented twice — #3015 then #3024) are built once.

**Direction decision**
(`docs/superpowers/specs/2026-07-23-unified-post-container-design.md`):
the store stays the single source of truth and thread views become a
`selectThreadPosts` filter over it — inverting ECA-1304's sketched
migration direction, for the reason its own capability table gives:
pagination, reconnect backfill, reactions, file-info backfill, and
`resetStore` exist only store-side, so this direction rebuilds nothing.
The store's pending-post matcher also runs per *arriving* post (not over
thread history), so the "identical message twice in 30s" hazard that
made the thread side reject content fallback disappears rather than
getting imported.

Key invariants the spec pins down:

- **Backfill watermark guard**: `fetchThread` seeds sync with `source:
'thread-seed'` and never advance `lastCreateAtByChannelRef` — otherwise
reconnect backfill silently skips intervening channel posts.
- **No-provider fallback keeps the REST echo**: today `locallySentPosts`
echoes confirmed sends even without the Mattermost provider; the
replacement hook preserves that with a local overlay, not a static
render.
- **Zero main-chat behavior change** in the first two slices; the
junction-box dispatcher ordering in `useMattermost` is untouched.

**Implementation plan**
(`docs/superpowers/plans/2026-07-23-unified-post-container-plan.md`): 9
TDD tasks across three independently landable PRs —

1. **PR 1**: extract `syncPosts`/`removePost` `setState` updaters into
pure `applySyncPosts`/`applyRemovePost` (bodies moved verbatim, direct
unit tests) + the `thread-seed` watermark option.
2. **PR 2**: `selectThreadPosts` selector; expose
`postStore`/`syncPosts`/`removePost` on `UseMattermostReturn` →
provider; `useThreadPosts` hook (seed + select + fallback), dark until
PR 3.
3. **PR 3**: migrate `SessionThreadClient` + `AgentBuilderClient`,
delete `useLiveThread`/`reconcilePendingPosts` and the `onPostDeleted`
fanout (the `post_deleted → removePost` store path stays and now serves
thread views), port the #3024 regression tests, manual mock-backend
probe incl. a reconnect-watermark check.

Docs only — no code changes in this PR.

## Test plan

- [ ] Docs-only change; no CI-affecting code
- [ ] Spec/plan cross-checked against origin/main code
(`useLiveThread.ts`, `useMattermostPosts.ts`, `useMattermost.ts`,
`MattermostProvider.tsx`, both thread clients, existing unit specs)

## Related

- Origin issue (Plan A section):
https://linear.app/srpone/issue/ECA-1304/thread-型界面session-thread-agent-builder-对话缺少用户消息乐观渲染
- Prior art: #3015 (main-chat optimistic rendering), #3024 (thread-side
optimistic rendering, the second implementation this refactor removes)
```

### PR body

## Summary

Design spec + implementation plan for "Plan A" deferred from ECA-1304: retire the parallel `useLiveThread` thread-post container by making session-thread and agent-builder views selectors over the normalized `PostStore`, so message-list features (optimistic rendering was implemented twice — #3015 then #3024) are built once.

**Direction decision** (`docs/superpowers/specs/2026-07-23-unified-post-container-design.md`): the store stays the single source of truth and thread views become a `selectThreadPosts` filter over it — inverting ECA-1304's sketched migration direction, for the reason its own capability table gives: pagination, reconnect backfill, reactions, file-info backfill, and `resetStore` exist only store-side, so this direction rebuilds nothing. The store's pending-post matcher also runs per *arriving* post (not over thread history), so the "identical message twice in 30s" hazard that made the thread side reject content fallback disappears rather than getting imported.

Key invariants the spec pins down:

- **Backfill watermark guard**: `fetchThread` seeds sync with `source: 'thread-seed'` and never advance `lastCreateAtByChannelRef` — otherwise reconnect backfill silently skips intervening channel posts.
- **No-provider fallback keeps the REST echo**: today `locallySentPosts` echoes confirmed sends even without the Mattermost provider; the replacement hook preserves that with a local overlay, not a static render.
- **Zero main-chat behavior change** in the first two slices; the junction-box dispatcher ordering in `useMattermost` is untouched.

**Implementation plan** (`docs/superpowers/plans/2026-07-23-unified-post-container-plan.md`): 9 TDD tasks across three independently landable PRs —

1. **PR 1**: extract `syncPosts`/`removePost` `setState` updaters into pure `applySyncPosts`/`applyRemovePost` (bodies moved verbatim, direct unit tests) + the `thread-seed` watermark option.
2. **PR 2**: `selectThreadPosts` selector; expose `postStore`/`syncPosts`/`removePost` on `UseMattermostReturn` → provider; `useThreadPosts` hook (seed + select + fallback), dark until PR 3.
3. **PR 3**: migrate `SessionThreadClient` + `AgentBuilderClient`, delete `useLiveThread`/`reconcilePendingPosts` and the `onPostDeleted` fanout (the `post_deleted → removePost` store path stays and now serves thread views), port the #3024 regression tests, manual mock-backend probe incl. a reconnect-watermark check.

Docs only — no code changes in this PR.

## Test plan

- [ ] Docs-only change; no CI-affecting code
- [ ] Spec/plan cross-checked against origin/main code (`useLiveThread.ts`, `useMattermostPosts.ts`, `useMattermost.ts`, `MattermostProvider.tsx`, both thread clients, existing unit specs)

## Related

- Origin issue (Plan A section): https://linear.app/srpone/issue/ECA-1304/thread-型界面session-thread-agent-builder-对话缺少用户消息乐观渲染
- Prior art: #3015 (main-chat optimistic rendering), #3024 (thread-side optimistic rendering, the second implementation this refactor removes)



## `8dd1b8eca0` (PR #3042)

- **作者**: shana-srp
- **日期**: 2026-07-23T09:51:38Z
- **SHA**: 8dd1b8eca0218ee3019d71de2aeaa56142607eed

### Commit message

```
fix(landing): refine hero composer behavior (#3042)

## Summary
- keep the selected landing-page prompt while allowing visitors to
switch specialists
- recommend PPT Master when a slide template is selected
- set Claude Sonnet 5 as the default model and align model multipliers
with the published values
- translate the Build Agents category in Chinese

## Root cause
The prompt recommendation always took precedence over a visitor's
explicit specialist choice, while template-only selection had no
displayed specialist fallback. The landing model metadata and Chinese
category copy were also stale.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/landing-content.unit.spec.ts
tests/unit/app/landing-hero-prompt-editing.unit.spec.tsx`
- [x] 18 related tests passed

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR body

## Summary
- keep the selected landing-page prompt while allowing visitors to switch specialists
- recommend PPT Master when a slide template is selected
- set Claude Sonnet 5 as the default model and align model multipliers with the published values
- translate the Build Agents category in Chinese

## Root cause
The prompt recommendation always took precedence over a visitor's explicit specialist choice, while template-only selection had no displayed specialist fallback. The landing model metadata and Chinese category copy were also stale.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/landing-content.unit.spec.ts tests/unit/app/landing-hero-prompt-editing.unit.spec.tsx`
- [x] 18 related tests passed



## `35502ec2e5` (PR #3037)

- **作者**: bill-srp
- **日期**: 2026-07-23T09:06:19Z
- **SHA**: 35502ec2e55db54562b98b31331c27624a172dce

### Commit message

```
docs: add org upgrade-to-team spec and implementation plan (#3037)

## Summary
- Design spec for a staff-console admin API that upgrades a personal org
to a team org in place:
`docs/superpowers/specs/2026-07-23-org-upgrade-to-team-design.md`
- Implementation plan (2 PR series: claw-interface backend first,
dashboard-console UI second):
`docs/superpowers/plans/2026-07-23-org-upgrade-to-team.md`

Key decisions locked in the spec (with Bill):
- New route `POST /internal/orgs/{org_id}/upgrade-to-team`, double-gated
by `require_srp_account` + `require_admin_user` (offline-order console
pattern), body `{ name }` replacing the hard-coded "Personal" org name.
- **Billing team converts in place**: the org keeps its
`billing_team_id`; that team's billing mode flips `personal → business`
via the same `add_user_to_personal_team(..., billing_mode="business")`
call org creation uses; subscription/topup wallets are ensured and their
ids stored.
- **No auto plan subscribe**: unlike fresh team-org creation, the
upgrade does not subscribe `BG_PLAN_STARTER_20_MONTH`; team plan
purchase happens later through normal flows.
- Final commit is an atomic CAS write filtered on `org_type ==
"personal"`, so validation is folded into the write and a concurrent
upgrade fails loudly; billing steps are idempotent, making the endpoint
retryable after partial failure.
- Supporting contract change: `GET /internal/users/{uid}/orgs` gains
`org_type` and includes personal orgs (offline-orders console filters to
team client-side).
- Console scope: upgrade dialog + controller hook on the
dashboard-console users screen, mirroring the grant-credits/boost action
pattern.

Docs only — no code changes in this PR.

## Test plan
- [x] Spec self-review (no placeholders, decisions consistent, error
codes/route shapes named)
- [x] Plan self-review (spec coverage, no placeholder steps,
type/signature consistency across tasks)
- [ ] Implementation PRs follow per the plan (backend first, console
second)
```

### PR body

## Summary
- Design spec for a staff-console admin API that upgrades a personal org to a team org in place: `docs/superpowers/specs/2026-07-23-org-upgrade-to-team-design.md`
- Implementation plan (2 PR series: claw-interface backend first, dashboard-console UI second): `docs/superpowers/plans/2026-07-23-org-upgrade-to-team.md`

Key decisions locked in the spec (with Bill):
- New route `POST /internal/orgs/{org_id}/upgrade-to-team`, double-gated by `require_srp_account` + `require_admin_user` (offline-order console pattern), body `{ name }` replacing the hard-coded "Personal" org name.
- **Billing team converts in place**: the org keeps its `billing_team_id`; that team's billing mode flips `personal → business` via the same `add_user_to_personal_team(..., billing_mode="business")` call org creation uses; subscription/topup wallets are ensured and their ids stored.
- **No auto plan subscribe**: unlike fresh team-org creation, the upgrade does not subscribe `BG_PLAN_STARTER_20_MONTH`; team plan purchase happens later through normal flows.
- Final commit is an atomic CAS write filtered on `org_type == "personal"`, so validation is folded into the write and a concurrent upgrade fails loudly; billing steps are idempotent, making the endpoint retryable after partial failure.
- Supporting contract change: `GET /internal/users/{uid}/orgs` gains `org_type` and includes personal orgs (offline-orders console filters to team client-side).
- Console scope: upgrade dialog + controller hook on the dashboard-console users screen, mirroring the grant-credits/boost action pattern.

Docs only — no code changes in this PR.

## Test plan
- [x] Spec self-review (no placeholders, decisions consistent, error codes/route shapes named)
- [x] Plan self-review (spec coverage, no placeholder steps, type/signature consistency across tasks)
- [ ] Implementation PRs follow per the plan (backend first, console second)



## `2eab857f0b` (PR #3038)

- **作者**: bill-srp
- **日期**: 2026-07-23T08:37:04Z
- **SHA**: 2eab857f0bc71500433ee6d0daba596e6f26aa33

### Commit message

```
fix(enterprise-admin): accept offline payment accounts (#3038)

## Summary
- Accept the backend `offline` payment channel in the Enterprise Admin
`/account/me` contract.
- Add regression coverage for OTP login by an existing offline-paid
enterprise account.

## Root cause
The backend added `payment_channel: "offline"` for offline enterprise
packages, but the Enterprise Admin Zod schema still accepted only
`stripe`, `antom`, and `apple`. After OTP verification, parsing
`/account/me` raised a Zod error and left the user on the verification
screen.

## Test plan
- [x] `pnpm --dir web/enterprise-admin exec vitest run --config
./vitest.config.mts lib/__tests__/auth.test.ts`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/enterprise-admin run lint`
```

### PR body

## Summary
- Accept the backend `offline` payment channel in the Enterprise Admin `/account/me` contract.
- Add regression coverage for OTP login by an existing offline-paid enterprise account.

## Root cause
The backend added `payment_channel: "offline"` for offline enterprise packages, but the Enterprise Admin Zod schema still accepted only `stripe`, `antom`, and `apple`. After OTP verification, parsing `/account/me` raised a Zod error and left the user on the verification screen.

## Test plan
- [x] `pnpm --dir web/enterprise-admin exec vitest run --config ./vitest.config.mts lib/__tests__/auth.test.ts`
- [x] `pnpm --dir web/enterprise-admin exec tsc --noEmit`
- [x] `pnpm --dir web/enterprise-admin run lint`



## `b8282cef6c` (PR #3035)

- **作者**: bill-srp
- **日期**: 2026-07-23T08:25:47Z
- **SHA**: b8282cef6c2fcdeb9336dfc734042be62e675bdd

### Commit message

```
docs: add pack environment binding spec and implementation plan (#3035)

## Summary

Design spec + implementation plan for **pack environment binding**:
wiring the zooclaw-engine Environments API (Developer Preview) into the
pack approval and engine-agent install flows.

- `docs/superpowers/specs/2026-07-23-pack-environment-binding-design.md`
— the agreed design:
- At **submission approval**, claw-interface downloads the approved
archive, extracts workspace-root persona markdown into a new
`pack_persona_docs` collection (ungated), and creates/versions an engine
Environment from the archive (gated by new
`ZOOCLAW_ENGINE_ENVIRONMENTS_ENABLED`, default off — upstream API is
Integration-pending).
- Pack stores `environment_id` only; agent create resolves + pins the
latest ready version. First-party official packs (`org_id == zooclaw`
AND `origin_pack_id is None`) build **global** envs via the admin API;
everything else — org packs and marketplace listing copies — builds
org-scoped envs (cross-org store installs fail closed).
- The approval pipeline is keyed off the **approved submission**
(`submission.asset_id`/`submission_id`), never the refetched Pack row,
to avoid a wrong-archive race on multi-approval paths.
- Engine agent install reads persona from the DB (archive fallback for
legacy packs) and pins `pack.environment_id`; `resolved_environment` is
persisted on the workspace row. Env is create-only (engine locks the pin
after the first sandbox).
- Size guard: archives whose normalized env zip exceeds the engine's 50
MB cap publish without an environment (the single deliberate fail-open,
logged at approval).
- `docs/superpowers/plans/2026-07-23-pack-environment-binding.md` —
10-task TDD plan (backend-only, claw-interface), sliced as two PRs: PR A
= ungated persona snapshot + DB-first install; PR B = environment
pipeline dark behind the flag.

No code changes in this PR.

## Review round 1 (addressed in 64b5337ac)

- Codex P1 — "official" now means `org_id == zooclaw` AND
`origin_pack_id is None`; marketplace listing copies take the org-scoped
service-API path.
- Codex P1 — pipeline source of truth switched to
`submission.asset_id`/`submission_id`; Pack row used only for binding
state. New test case added.
- Claude review — spec's build-script wording updated to match the
repack design; `_open_indexed_archive` pinned as a context manager;
flag-enablement prerequisite checklist added to rollout; service-token
admin-access verification called out; `seed_policy` default documented;
PR-A repack placement note added.

## Review / Merge checklist

- [x] Spec decisions confirmed with Bill in brainstorming (env source,
pin policy, attach point, org scope, approval-time pipeline, fail-closed
installs)
- [x] Codex + Claude review round 1 addressed
- [ ] Spec/plan review by Bill
```

### PR body

## Summary

Design spec + implementation plan for **pack environment binding**: wiring the zooclaw-engine Environments API (Developer Preview) into the pack approval and engine-agent install flows.

- `docs/superpowers/specs/2026-07-23-pack-environment-binding-design.md` — the agreed design:
  - At **submission approval**, claw-interface downloads the approved archive, extracts workspace-root persona markdown into a new `pack_persona_docs` collection (ungated), and creates/versions an engine Environment from the archive (gated by new `ZOOCLAW_ENGINE_ENVIRONMENTS_ENABLED`, default off — upstream API is Integration-pending).
  - Pack stores `environment_id` only; agent create resolves + pins the latest ready version. First-party official packs (`org_id == zooclaw` AND `origin_pack_id is None`) build **global** envs via the admin API; everything else — org packs and marketplace listing copies — builds org-scoped envs (cross-org store installs fail closed).
  - The approval pipeline is keyed off the **approved submission** (`submission.asset_id`/`submission_id`), never the refetched Pack row, to avoid a wrong-archive race on multi-approval paths.
  - Engine agent install reads persona from the DB (archive fallback for legacy packs) and pins `pack.environment_id`; `resolved_environment` is persisted on the workspace row. Env is create-only (engine locks the pin after the first sandbox).
  - Size guard: archives whose normalized env zip exceeds the engine's 50 MB cap publish without an environment (the single deliberate fail-open, logged at approval).
- `docs/superpowers/plans/2026-07-23-pack-environment-binding.md` — 10-task TDD plan (backend-only, claw-interface), sliced as two PRs: PR A = ungated persona snapshot + DB-first install; PR B = environment pipeline dark behind the flag.

No code changes in this PR.

## Review round 1 (addressed in 64b5337ac)

- Codex P1 — "official" now means `org_id == zooclaw` AND `origin_pack_id is None`; marketplace listing copies take the org-scoped service-API path.
- Codex P1 — pipeline source of truth switched to `submission.asset_id`/`submission_id`; Pack row used only for binding state. New test case added.
- Claude review — spec's build-script wording updated to match the repack design; `_open_indexed_archive` pinned as a context manager; flag-enablement prerequisite checklist added to rollout; service-token admin-access verification called out; `seed_policy` default documented; PR-A repack placement note added.

## Review / Merge checklist

- [x] Spec decisions confirmed with Bill in brainstorming (env source, pin policy, attach point, org scope, approval-time pipeline, fail-closed installs)
- [x] Codex + Claude review round 1 addressed
- [ ] Spec/plan review by Bill



## `131a4cd8ac` (PR #3034)

- **作者**: Mori-srp
- **日期**: 2026-07-23T07:14:38Z
- **SHA**: 131a4cd8acd40bdaae9c04416b54c18ef20aee1a

### Commit message

```
fix(web): remove homepage hero description (#3034)

## Summary

- Remove the visible homepage paragraph below the H1 after product
feedback confirmed it is not needed.
- Remove the now-unused `landingV2.heroDescription` copy from all 10
locale dictionaries.
- Update the landing hero unit test to preserve the single `main` /
single H1 contract and assert that the removed description is not
rendered.

## Why

The paragraph was introduced in #2962 as proposed, SEO-readable
supporting copy rather than approved product messaging. The latest
product review asked to remove it from the homepage.

The homepage Meta Description remains unchanged and continues to
describe the product for search results. This PR does not localize that
Meta Description; localized search snippets remain a separate follow-up
task requiring approved copy and language review.

## Scope and impact

This is a five-file change with no modifications to:

- homepage title or Meta Description
- SSR structure beyond removing the paragraph
- canonical or hreflang generation
- sitemap or robots
- Open Graph, Twitter metadata, or JSON-LD
- tracking, routing, authentication, or homepage interactions

## Validation

- Targeted Vitest: 5 test files, 78 tests passed.
- Targeted ESLint: passed.
- Commit hook selected web verification: passed.
- `git diff --check`: passed.
- Raw HTML smoke for `/zh`, `/ja`, and `/ar`: one `main`, one H1, no
hero description paragraph; Meta Description, self-canonical, and 11
hreflang entries preserved.
- Chrome desktop and mobile smoke: H1, task input, quick actions, and
footer layout remained intact without horizontal overflow.
- PR size guard: passed, 8 / 3000 counted lines after exclusions.

## Existing main baseline issue

The repository-wide TypeScript check is currently blocked by
`tests/e2e/specs/model-switching.spec.ts(21,25): Cannot find name
'sharedPage'`. The same stale reference exists on `origin/main`, and
this PR does not modify that file.

The normal push was attempted first. `SKIP_VERIFY=1` was then used only
to bypass that known pre-push verification false positive. No rebase,
force-push, or `--no-verify` was used.
```

### PR body

## Summary

- Remove the visible homepage paragraph below the H1 after product feedback confirmed it is not needed.
- Remove the now-unused `landingV2.heroDescription` copy from all 10 locale dictionaries.
- Update the landing hero unit test to preserve the single `main` / single H1 contract and assert that the removed description is not rendered.

## Why

The paragraph was introduced in #2962 as proposed, SEO-readable supporting copy rather than approved product messaging. The latest product review asked to remove it from the homepage.

The homepage Meta Description remains unchanged and continues to describe the product for search results. This PR does not localize that Meta Description; localized search snippets remain a separate follow-up task requiring approved copy and language review.

## Scope and impact

This is a five-file change with no modifications to:

- homepage title or Meta Description
- SSR structure beyond removing the paragraph
- canonical or hreflang generation
- sitemap or robots
- Open Graph, Twitter metadata, or JSON-LD
- tracking, routing, authentication, or homepage interactions

## Validation

- Targeted Vitest: 5 test files, 78 tests passed.
- Targeted ESLint: passed.
- Commit hook selected web verification: passed.
- `git diff --check`: passed.
- Raw HTML smoke for `/zh`, `/ja`, and `/ar`: one `main`, one H1, no hero description paragraph; Meta Description, self-canonical, and 11 hreflang entries preserved.
- Chrome desktop and mobile smoke: H1, task input, quick actions, and footer layout remained intact without horizontal overflow.
- PR size guard: passed, 8 / 3000 counted lines after exclusions.

## Existing main baseline issue

The repository-wide TypeScript check is currently blocked by `tests/e2e/specs/model-switching.spec.ts(21,25): Cannot find name 'sharedPage'`. The same stale reference exists on `origin/main`, and this PR does not modify that file.

The normal push was attempted first. `SKIP_VERIFY=1` was then used only to bypass that known pre-push verification false positive. No rebase, force-push, or `--no-verify` was used.

