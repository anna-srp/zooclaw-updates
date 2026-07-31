# SerendipityOneInc/ecap-workspace commits — 2026-07-30


## c1d4619d — feat(council): refresh runs from thread activity (#3160)

- **SHA**: c1d4619dc01643d2cb3739368cd7187e7ebc1740
- **作者**: bill-srp
- **日期**: 2026-07-30T17:22:48Z
- **PR**: #3160

### 完整 Commit Message

```
feat(council): refresh runs from thread activity (#3160)

## Summary

- subscribe to Mattermost activity for the persisted Council run thread
- coalesce websocket activity into the existing status refresh path with
a shared three-second throttle
- keep bounded backoff polling as the safety net, with a higher ceiling
while the socket is connected

## Stack

- Depends on #3158
- Review after #3157 and #3158
- This slice intentionally excludes thread-history synthesis rendering

## Verification

- `bash scripts/verify-web.sh web/app/src/hooks/council
web/app/src/hooks/queries/council web/app/src/hooks/useMattermost.ts
web/app/src/lib/council web/app/src/lib/mattermost/post-status.ts
web/app/tests/unit/hooks/council
web/app/tests/unit/hooks/queries/council web/app/tests/unit/lib/council`
- TypeScript passed
- 270 selected tests passed
- ESLint passed
```

### PR Body

## Summary

- subscribe to Mattermost activity for the persisted Council run thread
- coalesce websocket activity into the existing status refresh path with a shared three-second throttle
- keep bounded backoff polling as the safety net, with a higher ceiling while the socket is connected

## Stack

- Depends on #3158
- Review after #3157 and #3158
- This slice intentionally excludes thread-history synthesis rendering

## Verification

- `bash scripts/verify-web.sh web/app/src/hooks/council web/app/src/hooks/queries/council web/app/src/hooks/useMattermost.ts web/app/src/lib/council web/app/src/lib/mattermost/post-status.ts web/app/tests/unit/hooks/council web/app/tests/unit/hooks/queries/council web/app/tests/unit/lib/council`
- TypeScript passed
- 270 selected tests passed
- ESLint passed



## 374e610a — fix(council): preserve dedicated run thread identity (#3158)

- **SHA**: 374e610a48f3c9ed3b6a1517fc28aff804e15a5f
- **作者**: bill-srp
- **日期**: 2026-07-30T14:54:25Z
- **PR**: #3158

### 完整 Commit Message

```
fix(council): preserve dedicated run thread identity (#3158)

## Summary

Second slice of #3139, stacked on #3157.

- Create an untracked Mattermost thread for each Council run without
adding it to normal Chat conversations.
- Resolve the exact owner-scoped main workspace, including migrated
Engine mains.
- Persist immutable workspace, channel, root-post, and bot-user thread
identity on the run.
- Use the persisted channel for later approval/cancel replies, with a
root-only fallback for pre-existing runs.
- Preserve stable Council-domain error codes from the backend.
- Keep independent web/backend rollout compatibility: only a generic
route-missing 404 may use the legacy conversation bootstrap.

The event-driven refresh and synthesis summary remain in later slices.

## Stack

1. #3157 — approval, depth, and tier intent
2. This PR — dedicated run thread identity
3. #3160 — event-driven status refresh
4. #3161 — terminal thread synthesis

Review and merge in that order.

## Test plan

- [x] 112 targeted backend tests
- [x] 69 selected frontend Council tests
- [x] `bash scripts/verify-web.sh ...` for the changed Council hooks,
models, services, and tests
- [x] Ruff check and format
- [x] Pyright: 0 errors, 0 warnings (explicit existing venv interpreter
for the new worktree)
- [x] Import-linter: 8 contracts kept
```

### PR Body

## Summary

Second slice of #3139, stacked on #3157.

- Create an untracked Mattermost thread for each Council run without adding it to normal Chat conversations.
- Resolve the exact owner-scoped main workspace, including migrated Engine mains.
- Persist immutable workspace, channel, root-post, and bot-user thread identity on the run.
- Use the persisted channel for later approval/cancel replies, with a root-only fallback for pre-existing runs.
- Preserve stable Council-domain error codes from the backend.
- Keep independent web/backend rollout compatibility: only a generic route-missing 404 may use the legacy conversation bootstrap.

The event-driven refresh and synthesis summary remain in later slices.

## Stack

1. #3157 — approval, depth, and tier intent
2. This PR — dedicated run thread identity
3. #3160 — event-driven status refresh
4. #3161 — terminal thread synthesis

Review and merge in that order.

## Test plan

- [x] 112 targeted backend tests
- [x] 69 selected frontend Council tests
- [x] `bash scripts/verify-web.sh ...` for the changed Council hooks, models, services, and tests
- [x] Ruff check and format
- [x] Pyright: 0 errors, 0 warnings (explicit existing venv interpreter for the new worktree)
- [x] Import-linter: 8 contracts kept



## 61cc126c — feat(council): automate approval with depth and tier intent (#3157)

- **SHA**: 61cc126c479afc1f2b067e3a9d6c8daa2f0c1cbf
- **作者**: bill-srp
- **日期**: 2026-07-30T14:12:28Z
- **PR**: #3157

### 完整 Commit Message

```
feat(council): automate approval with depth and tier intent (#3157)

## Linear

https://linear.app/srpone/issue/ECA-1211/council-多模型调研功能上线-beta-版

## Summary

First slice of #3139.

- Add Auto / Quick / Standard / Deep depth selection without consuming
the topic's 2,000-character budget.
- Add Economy / Standard / Premium tier intent.
- Automatically post `go` only for the exact run dispatched in the
current browser session.
- Wait for requested depth and tier to be observed before automatic
approval.
- Fall back to an explicit approval control after reload, dispatch
failure, tier timeout, or an observed depth mismatch.
- Replace the mutable confirmation gate with read-only run details and
explicit retry controls.

The Mattermost event refresh, dedicated hidden Council thread, and
synthesis summary are intentionally excluded and land in the follow-up
slices below.

## Stack

1. This PR — approval, depth, and tier intent
2. #3158 — dedicated run thread identity
3. #3160 — event-driven status refresh
4. #3161 — terminal thread synthesis

Review and merge in that order.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/src/components/council
web/app/src/hooks/council web/app/tests/unit/app/council
web/app/tests/unit/hooks/council`
- [x] 64 selected Council tests
- [x] TypeScript and ESLint checks
```

### PR Body

## Linear

https://linear.app/srpone/issue/ECA-1211/council-多模型调研功能上线-beta-版

## Summary

First slice of #3139.

- Add Auto / Quick / Standard / Deep depth selection without consuming the topic's 2,000-character budget.
- Add Economy / Standard / Premium tier intent.
- Automatically post `go` only for the exact run dispatched in the current browser session.
- Wait for requested depth and tier to be observed before automatic approval.
- Fall back to an explicit approval control after reload, dispatch failure, tier timeout, or an observed depth mismatch.
- Replace the mutable confirmation gate with read-only run details and explicit retry controls.

The Mattermost event refresh, dedicated hidden Council thread, and synthesis summary are intentionally excluded and land in the follow-up slices below.

## Stack

1. This PR — approval, depth, and tier intent
2. #3158 — dedicated run thread identity
3. #3160 — event-driven status refresh
4. #3161 — terminal thread synthesis

Review and merge in that order.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/src/components/council web/app/src/hooks/council web/app/tests/unit/app/council web/app/tests/unit/hooks/council`
- [x] 64 selected Council tests
- [x] TypeScript and ESLint checks



## 19083484 — docs: add schedule v2 engine design spec and implementation plans (#3151)

- **SHA**: 1908348421bd7593d1d495356bfc639262700a22
- **作者**: bill-srp
- **日期**: 2026-07-30T13:49:55Z
- **PR**: #3151

### 完整 Commit Message

```
docs: add schedule v2 engine design spec and implementation plans (#3151)

## Summary
- Design spec for adding v2 engine-agent schedules to the `/schedule`
page alongside the untouched v1 bot cron:
`docs/superpowers/specs/2026-07-30-schedule-v2-engine-design.md`
- Two self-contained implementation plans, one per PR:
- `docs/superpowers/plans/2026-07-30-schedule-v2-backend.md` — PR 1:
runtime-agnostic `/agents/{workspace_id}/schedules` claw-interface
routes (engine branch via a new engine-client schedules mixin; computer
branch delegates reads to FastClaw cron), `AGENTS_V2_ENABLED`-gated,
engine 501 masked to `schedules_unavailable`, best-effort schedule
cleanup on engine-agent uninstall
- `docs/superpowers/plans/2026-07-30-schedule-v2-frontend.md` — PR 2
(after PR 1 deploys to staging): merged schedule list with agent badges,
form agent selector, per-runtime row actions; v1 WS write path untouched

Key decisions locked in session with Bill: merged list + agent badge UI;
unified runtime-agnostic API with v1 untouched; `AGENTS_V2_ENABLED`
gating (no new flag); v1-parity form with engine defaults
(`sessionTarget=isolated`, `delivery=none`, slugged `schedule_id`).

Upstream contract verified against the zooclaw-engine checkout (controld
peripheral routes/service/temporal adapter), including: engine list
entries carry no payload message (hence the detail route), runs endpoint
is limit-only (no offset), schedules are not auto-deleted with the
agent.

## Test plan
- [ ] Docs-only change — no code paths affected
- [ ] Spec/plan reviewed for consistency with the runtime-agnostic agent
API rule and GET/POST-only convention
```

### PR Body

## Summary
- Design spec for adding v2 engine-agent schedules to the `/schedule` page alongside the untouched v1 bot cron: `docs/superpowers/specs/2026-07-30-schedule-v2-engine-design.md`
- Two self-contained implementation plans, one per PR:
  - `docs/superpowers/plans/2026-07-30-schedule-v2-backend.md` — PR 1: runtime-agnostic `/agents/{workspace_id}/schedules` claw-interface routes (engine branch via a new engine-client schedules mixin; computer branch delegates reads to FastClaw cron), `AGENTS_V2_ENABLED`-gated, engine 501 masked to `schedules_unavailable`, best-effort schedule cleanup on engine-agent uninstall
  - `docs/superpowers/plans/2026-07-30-schedule-v2-frontend.md` — PR 2 (after PR 1 deploys to staging): merged schedule list with agent badges, form agent selector, per-runtime row actions; v1 WS write path untouched

Key decisions locked in session with Bill: merged list + agent badge UI; unified runtime-agnostic API with v1 untouched; `AGENTS_V2_ENABLED` gating (no new flag); v1-parity form with engine defaults (`sessionTarget=isolated`, `delivery=none`, slugged `schedule_id`).

Upstream contract verified against the zooclaw-engine checkout (controld peripheral routes/service/temporal adapter), including: engine list entries carry no payload message (hence the detail route), runs endpoint is limit-only (no offset), schedules are not auto-deleted with the agent.

## Test plan
- [ ] Docs-only change — no code paths affected
- [ ] Spec/plan reviewed for consistency with the runtime-agnostic agent API rule and GET/POST-only convention



## 5a844d9c — fix(chat): skip restart prompt for v2 model changes (#3144)

- **SHA**: 5a844d9c615023265b46a9818807740bbb40a9a1
- **作者**: bill-srp
- **日期**: 2026-07-30T13:32:35Z
- **PR**: #3144

### 完整 Commit Message

```
fix(chat): skip restart prompt for v2 model changes (#3144)

## Summary

- pass the selected agent workspace runtime through every chat composer
surface
- apply ZooClaw Engine model changes without showing the OpenClaw
restart prompt
- preserve the existing restart flow for computer-backed agents
- add regression coverage for runtime propagation and the engine
no-restart behavior

## Root cause

The shared composer treated every successful model update as an OpenClaw
configuration change. ZooClaw Engine applies v2 model updates
immediately, so engine-backed agents were incorrectly asked to restart
after a successful update.

## Test plan

- [x] Web governance guards
- [x] Targeted Vitest run: 12 files, 315 tests passed
- [x] ESLint for all changed files
- [x] Full web ESLint through `scripts/verify-changed.sh`

## Known unrelated check failure

The project-wide TypeScript check currently fails at
`src/app/[locale]/(app)/plugins/PluginsClient.tsx:31` because
`searchParams` may be null. This file is unchanged by this PR.
```

### PR Body

## Summary

- pass the selected agent workspace runtime through every chat composer surface
- apply ZooClaw Engine model changes without showing the OpenClaw restart prompt
- preserve the existing restart flow for computer-backed agents
- add regression coverage for runtime propagation and the engine no-restart behavior

## Root cause

The shared composer treated every successful model update as an OpenClaw configuration change. ZooClaw Engine applies v2 model updates immediately, so engine-backed agents were incorrectly asked to restart after a successful update.

## Test plan

- [x] Web governance guards
- [x] Targeted Vitest run: 12 files, 315 tests passed
- [x] ESLint for all changed files
- [x] Full web ESLint through `scripts/verify-changed.sh`

## Known unrelated check failure

The project-wide TypeScript check currently fails at `src/app/[locale]/(app)/plugins/PluginsClient.tsx:31` because `searchParams` may be null. This file is unchanged by this PR.



## b794e0e2 — docs(council): address codex review on deep research docs (#3159)

- **SHA**: b794e0e20039ff67ff17ccfc6de501eb549ddd17
- **作者**: bill-srp
- **日期**: 2026-07-30T13:32:11Z
- **PR**: #3159

### 完整 Commit Message

```
docs(council): address codex review on deep research docs (#3159)

## Summary
- Follow-up to #3156, applying the three P2 accuracy notes from its
Codex review (the branch was already merge-queued when the fixes were
ready, so they could not ride along):
- Spec: `workspaceId` for the post-dispatch navigation comes from the
caller's `mainAgentWorkspaceId`, not the create-conversation response
(`OpenClawConversation` carries no workspace id).
- Spec: the future dossier-viewing note no longer overstates `pod_files`
reuse — the folder needs zero *discovery* logic, but `pod_files` still
roots reads under `council-runs/` and will need a mode-aware root to
serve `research/` paths.
- Plan: replaced the machine-specific venv interpreter path in test
steps with portable claw-interface venv guidance (devcontainer path /
`uv pip install` host setup).

## Test plan
- [x] Docs only; re-checked each corrected statement against
`web/app/src/models/agent-conversation.ts` and
`services/claw-interface/app/services/council/pod_files.py`.
```

### PR Body

## Summary
- Follow-up to #3156, applying the three P2 accuracy notes from its Codex review (the branch was already merge-queued when the fixes were ready, so they could not ride along):
  - Spec: `workspaceId` for the post-dispatch navigation comes from the caller's `mainAgentWorkspaceId`, not the create-conversation response (`OpenClawConversation` carries no workspace id).
  - Spec: the future dossier-viewing note no longer overstates `pod_files` reuse — the folder needs zero *discovery* logic, but `pod_files` still roots reads under `council-runs/` and will need a mode-aware root to serve `research/` paths.
  - Plan: replaced the machine-specific venv interpreter path in test steps with portable claw-interface venv guidance (devcontainer path / `uv pip install` host setup).

## Test plan
- [x] Docs only; re-checked each corrected statement against `web/app/src/models/agent-conversation.ts` and `services/claw-interface/app/services/council/pod_files.py`.



## 0d9cae6e — docs(council): add deep research mode spec and plan (#3156)

- **SHA**: 0d9cae6e29460f55e05d161f50915c5cf9176dbb
- **作者**: bill-srp
- **日期**: 2026-07-30T13:21:35Z
- **PR**: #3156

### 完整 Commit Message

```
docs(council): add deep research mode spec and plan (#3156)

## Summary
- Design spec + implementation plan for **Deep Research mode** on the
`/council` page, agreed in brainstorming with Bill. Docs only — no code
changes; implementation follows in two separate PRs.
- **What the feature is**: a tab selector at the top of the council
input card (`Council | Deep Research`). Deep Research lets the user pick
a depth (`quick` / `standard` / `deep`), records a **minimal, inert
run** (born terminal `done`, never polled — the unmodified skill writes
no `status.json`, so there is nothing to refresh), posts `/deep-research
<depth>: <topic>` plus a folder-pin line to the main agent's thread, and
navigates the user to the chat session where the research actually runs.
- **Key decisions captured in the spec**:
- **No skill changes** (neither `council` nor `deep-research` in
ecap-skills) — depth and the dossier-folder pin travel as plain
dispatch-message instructions.
- Reuse `pod_status_run_id` (assigned at creation as
`deep-research-<run_id>`, no discovery/pinning) to persist the run ⇄
folder link; the response exposes a server-built `pod_folder` so a
future PR can render dossiers with zero discovery logic.
- `refresh`/`cancel` reject deep-research runs
(`council.mode_unsupported`); admission (one-active-run) applies only to
council mode.
- History rail lists both modes; deep-research entries link to the chat
thread (session derived from `dispatch_root_post_id` via the
conversation list — nothing new persisted).
- **Delivery plan**: PR 1 = backend (`mode`/`depth` on the create
contract, inert create path, lifecycle guards), PR 2 = frontend
(composer tabs, depth selector, dispatch flow, history rail). PR 1 must
merge and deploy before PR 2 (the current backend's `extra="forbid"`
422s the new `mode` key).

Files:
- `docs/superpowers/specs/2026-07-30-deep-research-mode-design.md`
- `docs/superpowers/plans/2026-07-30-deep-research-mode.md`

## Test plan
- [x] Docs only — no code paths to test. Verified the plan against the
spec (coverage, placeholder scan, type/signature consistency across
tasks) and against current `schema/council.py` / `run_service.py` /
council frontend sources.
```

### PR Body

## Summary
- Design spec + implementation plan for **Deep Research mode** on the `/council` page, agreed in brainstorming with Bill. Docs only — no code changes; implementation follows in two separate PRs.
- **What the feature is**: a tab selector at the top of the council input card (`Council | Deep Research`). Deep Research lets the user pick a depth (`quick` / `standard` / `deep`), records a **minimal, inert run** (born terminal `done`, never polled — the unmodified skill writes no `status.json`, so there is nothing to refresh), posts `/deep-research <depth>: <topic>` plus a folder-pin line to the main agent's thread, and navigates the user to the chat session where the research actually runs.
- **Key decisions captured in the spec**:
  - **No skill changes** (neither `council` nor `deep-research` in ecap-skills) — depth and the dossier-folder pin travel as plain dispatch-message instructions.
  - Reuse `pod_status_run_id` (assigned at creation as `deep-research-<run_id>`, no discovery/pinning) to persist the run ⇄ folder link; the response exposes a server-built `pod_folder` so a future PR can render dossiers with zero discovery logic.
  - `refresh`/`cancel` reject deep-research runs (`council.mode_unsupported`); admission (one-active-run) applies only to council mode.
  - History rail lists both modes; deep-research entries link to the chat thread (session derived from `dispatch_root_post_id` via the conversation list — nothing new persisted).
- **Delivery plan**: PR 1 = backend (`mode`/`depth` on the create contract, inert create path, lifecycle guards), PR 2 = frontend (composer tabs, depth selector, dispatch flow, history rail). PR 1 must merge and deploy before PR 2 (the current backend's `extra="forbid"` 422s the new `mode` key).

Files:
- `docs/superpowers/specs/2026-07-30-deep-research-mode-design.md`
- `docs/superpowers/plans/2026-07-30-deep-research-mode.md`

## Test plan
- [x] Docs only — no code paths to test. Verified the plan against the spec (coverage, placeholder scan, type/signature consistency across tasks) and against current `schema/council.py` / `run_service.py` / council frontend sources.



## 0036c9bf — fix(channels): resolve migrated ACS identity (#3155)

- **SHA**: 0036c9bf3b85fe7ecf52f2356c62845284338aa0
- **作者**: kaka-srp
- **日期**: 2026-07-30T13:07:13Z
- **PR**: #3155

### 完整 Commit Message

```
fix(channels): resolve migrated ACS identity (#3155)

## Summary
- resolve the canonical ACS agent identity from each workspace
- use migrated internal agent IDs for channel list, create, update,
remove, disable, and Mattermost binding
- preserve public Engine agent IDs for native V2 workspaces and
Mattermost account names

## Root cause
V1-to-V2 migration preserves the original internal agent ID, such as
`main`, for ACS bindings while exposing a new public Engine `agt_*` ID
through ecap. Channel listing and mutations used the public ID, so ACS
could not find migrated bindings even though uninstall cleanup already
used the internal ID.

## Test plan
- [x] targeted unit tests for workspace identity and every ACS channel
operation (125 passed)
- [x] ruff check and format
- [x] pyright
- [x] import-linter architecture contracts
- [x] pre-commit and pre-push changed-surface checks
```

### PR Body

## Summary
- resolve the canonical ACS agent identity from each workspace
- use migrated internal agent IDs for channel list, create, update, remove, disable, and Mattermost binding
- preserve public Engine agent IDs for native V2 workspaces and Mattermost account names

## Root cause
V1-to-V2 migration preserves the original internal agent ID, such as `main`, for ACS bindings while exposing a new public Engine `agt_*` ID through ecap. Channel listing and mutations used the public ID, so ACS could not find migrated bindings even though uninstall cleanup already used the internal ID.

## Test plan
- [x] targeted unit tests for workspace identity and every ACS channel operation (125 passed)
- [x] ruff check and format
- [x] pyright
- [x] import-linter architecture contracts
- [x] pre-commit and pre-push changed-surface checks



## 92bd8a93 — fix(openclaw): block migrated V1 runtime restarts (#3154)

- **SHA**: 92bd8a939a3ac0342eb09030e0785edce9beb3dd
- **作者**: kaka-srp
- **日期**: 2026-07-30T12:04:57Z
- **PR**: #3154

### 完整 Commit Message

```
fix(openclaw): block migrated V1 runtime restarts (#3154)

## Summary

- add a migration-owned fence to normalized V1 computer records
- reject start and restart at the final ecap-to-FastClaw client boundary
- preserve the fence across legacy-shaped computer upserts
- keep admin endpoints from converting the conflict response into HTTP
500

## Migration contract

The local migration kit sets `v1_start_blocked_by_migration_id` before
stopping
the V1 bot. Once set, all ecap start and restart paths fail before
FastClaw is
called. Redeploy remains covered because it stops and then uses the
guarded
start path.

Issue:
https://linear.app/srpone/issue/ECA-1341/block-v1-runtime-restarts-after-migration

## Validation

- Ruff check and format check
- Pyright: 0 errors
- Import-linter: all 8 contracts kept
- Focused unit tests: 179 passed
- Interrupted the full coverage suite at 550 passed / 260 skipped to
submit the requested PR immediately
```

### PR Body

## Summary

- add a migration-owned fence to normalized V1 computer records
- reject start and restart at the final ecap-to-FastClaw client boundary
- preserve the fence across legacy-shaped computer upserts
- keep admin endpoints from converting the conflict response into HTTP 500

## Migration contract

The local migration kit sets `v1_start_blocked_by_migration_id` before stopping
the V1 bot. Once set, all ecap start and restart paths fail before FastClaw is
called. Redeploy remains covered because it stops and then uses the guarded
start path.

Issue: https://linear.app/srpone/issue/ECA-1341/block-v1-runtime-restarts-after-migration

## Validation

- Ruff check and format check
- Pyright: 0 errors
- Import-linter: all 8 contracts kept
- Focused unit tests: 179 passed
- Interrupted the full coverage suite at 550 passed / 260 skipped to submit the requested PR immediately



## e2f73079 — fix(agents): source engine billing key from profile (#3150)

- **SHA**: e2f73079cc5bc9f965c78496437c1b73e400d73e
- **作者**: bill-srp
- **日期**: 2026-07-30T11:56:10Z
- **PR**: #3150

### 完整 Commit Message

```
fix(agents): source engine billing key from profile (#3150)

## Summary
- source engine-agent LiteLLM credentials exclusively from the
authoritative Billing Profile
- remove the deprecated `ecap-account.billing_key` bootstrap and
persistence path from engine credential seeding
- fail installation before activation only when the ready Billing
Profile does not contain a key
- pass any non-empty Billing Profile key to the engine unchanged,
without inferring validity from its prefix or format
- update unit and BDD boundaries to lock the Billing Profile-only
contract

Fixes #3148

## Root cause
Engine-agent installation bypassed Billing Profile and bootstrapped from
the deprecated account projection. The fallback path could obtain a
64-character alias/hash from LiteLLM key listing, persist it to the
account, and seed it into the agent as though it were the original key.

The engine path now removes that fallback entirely and reads only the
ready Billing Profile. Billing Profile is the authoritative owner of the
original key, so engine credential seeding checks only that the value
exists and does not impose an `sk-` prefix or other content-format
contract.

## Test plan
- [x] `pytest tests/unit/test_engine_agent_install_service.py
tests/unit/test_engine_agent_lifecycle_service.py
tests/unit/test_pack_test_engine_runtime_service.py -q` — 106 passed
- [x] `bash scripts/verify-py.sh` — ruff, format, pyright, and
import-linter passed
- [ ] Engine install BDD scenario — skipped locally because MongoDB was
not running on `127.0.0.1:27017`
```

### PR Body

## Summary
- source engine-agent LiteLLM credentials exclusively from the authoritative Billing Profile
- remove the deprecated `ecap-account.billing_key` bootstrap and persistence path from engine credential seeding
- fail installation before activation only when the ready Billing Profile does not contain a key
- pass any non-empty Billing Profile key to the engine unchanged, without inferring validity from its prefix or format
- update unit and BDD boundaries to lock the Billing Profile-only contract

Fixes #3148

## Root cause
Engine-agent installation bypassed Billing Profile and bootstrapped from the deprecated account projection. The fallback path could obtain a 64-character alias/hash from LiteLLM key listing, persist it to the account, and seed it into the agent as though it were the original key.

The engine path now removes that fallback entirely and reads only the ready Billing Profile. Billing Profile is the authoritative owner of the original key, so engine credential seeding checks only that the value exists and does not impose an `sk-` prefix or other content-format contract.

## Test plan
- [x] `pytest tests/unit/test_engine_agent_install_service.py tests/unit/test_engine_agent_lifecycle_service.py tests/unit/test_pack_test_engine_runtime_service.py -q` — 106 passed
- [x] `bash scripts/verify-py.sh` — ruff, format, pyright, and import-linter passed
- [ ] Engine install BDD scenario — skipped locally because MongoDB was not running on `127.0.0.1:27017`



## 83b53728 — feat(plugins): redesign connector cards (#3149)

- **SHA**: 83b537288c1393785c4048d7e83458a89e4c5240
- **作者**: shana-srp
- **日期**: 2026-07-30T11:29:26Z
- **PR**: #3149

### 完整 Commit Message

```
feat(plugins): redesign connector cards (#3149)

## Summary

- Redesign the Connector tab toolbar and provider cards for a clearer,
more compact layout.
- Add distinct connected, disabled, disconnected, and coming-soon visual
states without changing backend data contracts.
- Add an accessible disconnect confirmation dialog before revoking a
provider connection.
- Update Gmail and Google Calendar provider icons and responsive card
behavior.

## Testing

- `bash scripts/verify-web.sh ...`
  - TypeScript passed
  - ESLint passed
  - 305 test files passed
  - 4,432 tests passed, 1 existing todo
- Post-merge targeted validation:
  - `pnpm exec tsc --noEmit`
  - Connector unit suite: 21 tests passed
  - Targeted ESLint passed

## Scope

Frontend only. No backend API or connector data logic changes.

## Preview

`http://localhost:3005/plugins?tab=connector`

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Summary

- Redesign the Connector tab toolbar and provider cards for a clearer, more compact layout.
- Add distinct connected, disabled, disconnected, and coming-soon visual states without changing backend data contracts.
- Add an accessible disconnect confirmation dialog before revoking a provider connection.
- Update Gmail and Google Calendar provider icons and responsive card behavior.

## Testing

- `bash scripts/verify-web.sh ...`
  - TypeScript passed
  - ESLint passed
  - 305 test files passed
  - 4,432 tests passed, 1 existing todo
- Post-merge targeted validation:
  - `pnpm exec tsc --noEmit`
  - Connector unit suite: 21 tests passed
  - Targeted ESLint passed

## Scope

Frontend only. No backend API or connector data logic changes.

## Preview

`http://localhost:3005/plugins?tab=connector`



## 40325ec0 — fix(agents): recognize migrated main workspaces (#3146)

- **SHA**: 40325ec004cb1313058653b0a5afc3bb941e6475
- **作者**: kaka-srp
- **日期**: 2026-07-30T11:03:29Z
- **PR**: #3146

### 完整 Commit Message

```
fix(agents): recognize migrated main workspaces (#3146)

## Summary

- expose `AgentPublic.is_main` from the authoritative
`migration_v1_to_v2.internal_agent_id` while preserving literal-`main`
compatibility
- bind migrated Engine main workspaces to the fixed `Assistant` sidebar
row, exclude the duplicate agent row, and load conversations by the real
workspace ID
- normalize workspace-route accordion identity to `main`, update the
local mock contract, and add backend/frontend regression coverage

Linear:
https://linear.app/srpone/issue/ECA-1340/recognize-migrated-v2-main-agents-in-workspace-ui

## Root cause

Migrated V2 workspaces retain their canonical V1 identity under
`migration_v1_to_v2.internal_agent_id`, but `AgentWorkspace` ignored
that metadata. The unified Agent API therefore exposed only the
Engine-issued public `agt_*` ID, while the frontend classified main
agents with `agent.agent_id === "main"`. The migrated main workspace was
rendered as an extra agent, and the fixed `Assistant` row had no
workspace ID for conversation loading.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_agent_workspace_schema_v2.py
services/claw-interface/tests/unit/test_agents_v2_routes.py -q`
- [x] `bash scripts/verify-web.sh --tsc-only`
- [x] targeted frontend ESLint for changed web files
- [x] targeted Vitest: agent classification, sidebar workspace/session
binding, and mock Agent API contract (121 tests)
```

### PR Body

## Summary

- expose `AgentPublic.is_main` from the authoritative `migration_v1_to_v2.internal_agent_id` while preserving literal-`main` compatibility
- bind migrated Engine main workspaces to the fixed `Assistant` sidebar row, exclude the duplicate agent row, and load conversations by the real workspace ID
- normalize workspace-route accordion identity to `main`, update the local mock contract, and add backend/frontend regression coverage

Linear: https://linear.app/srpone/issue/ECA-1340/recognize-migrated-v2-main-agents-in-workspace-ui

## Root cause

Migrated V2 workspaces retain their canonical V1 identity under `migration_v1_to_v2.internal_agent_id`, but `AgentWorkspace` ignored that metadata. The unified Agent API therefore exposed only the Engine-issued public `agt_*` ID, while the frontend classified main agents with `agent.agent_id === "main"`. The migrated main workspace was rendered as an extra agent, and the fixed `Assistant` row had no workspace ID for conversation loading.

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_agent_workspace_schema_v2.py services/claw-interface/tests/unit/test_agents_v2_routes.py -q`
- [x] `bash scripts/verify-web.sh --tsc-only`
- [x] targeted frontend ESLint for changed web files
- [x] targeted Vitest: agent classification, sidebar workspace/session binding, and mock Agent API contract (121 tests)



## a3b7d1b4 — fix(council): persist member reports as members finish (#3145)

- **SHA**: a3b7d1b421b9fca5cd9d9b1e9e19901ce1b9c441
- **作者**: bill-srp
- **日期**: 2026-07-30T10:58:20Z
- **PR**: #3145

### 完整 Commit Message

```
fix(council): persist member reports as members finish (#3145)

## Summary
- Persist raw council member reports **as each member finishes**,
instead of only when the run reaches a terminal state, so completed
reports survive a mid-run pod loss.
- `member_reports.ingest_completed(files, run)`: best-effort ingest of
members with `state == "done"` and a `report` path. It lists stored
reports once per call and only reads/stores members not already in
Mongo, so the 3s status poll doesn't re-read up to 2 MB pod files per
member.
- `status_poll.refresh_from_pod` now calls `ingest_completed` after
every non-terminal reconcile (including unchanged snapshots, as a retry
safety net for a previously failed ingest), wrapped so a Mongo/pod blip
never fails the refresh. Terminal transitions keep the existing
`ingest_terminal` path and don't double-ingest.
- `ingest_terminal` shares the new dedup helper, so the terminal poll
skips reports already ingested mid-run.
- The read path (`list_reports`) is unchanged: mid-run drafts of
still-running members are served live from the pod and never persisted —
storage is a `$setOnInsert` upsert (first write wins), so only final
(member-done) content may ever be written.

## Root cause
`member_reports` gated all persistence on `run.state in TERMINAL_STATES`
(both the read-path fallback's `persist=` flag and the poller's
`_ingest_after_terminal`). A run whose pod died mid-flight never reached
a terminal transition through the poller, so completed members' raw
reports were permanently lost.

## Test plan
- [x] New unit tests (written first, watched fail): `ingest_completed`
persists only done+missing members; no-op without `pod_status_run_id`;
per-member read-failure isolation; terminal ingest skips already-stored
members; mid-run refresh calls `ingest_completed` (and not
`ingest_terminal`) with the updated run; terminal refresh calls only
`ingest_terminal`; a raising `ingest_completed` doesn't fail the
refresh; unchanged snapshots still trigger ingest.
- [x] All 6 council unit-test files green: 95 passed.
- [x] `bash scripts/verify-py.sh`: ruff check/format, pyright (0
errors), import-linter (8 contracts) all pass.
```

### PR Body

## Summary
- Persist raw council member reports **as each member finishes**, instead of only when the run reaches a terminal state, so completed reports survive a mid-run pod loss.
- `member_reports.ingest_completed(files, run)`: best-effort ingest of members with `state == "done"` and a `report` path. It lists stored reports once per call and only reads/stores members not already in Mongo, so the 3s status poll doesn't re-read up to 2 MB pod files per member.
- `status_poll.refresh_from_pod` now calls `ingest_completed` after every non-terminal reconcile (including unchanged snapshots, as a retry safety net for a previously failed ingest), wrapped so a Mongo/pod blip never fails the refresh. Terminal transitions keep the existing `ingest_terminal` path and don't double-ingest.
- `ingest_terminal` shares the new dedup helper, so the terminal poll skips reports already ingested mid-run.
- The read path (`list_reports`) is unchanged: mid-run drafts of still-running members are served live from the pod and never persisted — storage is a `$setOnInsert` upsert (first write wins), so only final (member-done) content may ever be written.

## Root cause
`member_reports` gated all persistence on `run.state in TERMINAL_STATES` (both the read-path fallback's `persist=` flag and the poller's `_ingest_after_terminal`). A run whose pod died mid-flight never reached a terminal transition through the poller, so completed members' raw reports were permanently lost.

## Test plan
- [x] New unit tests (written first, watched fail): `ingest_completed` persists only done+missing members; no-op without `pod_status_run_id`; per-member read-failure isolation; terminal ingest skips already-stored members; mid-run refresh calls `ingest_completed` (and not `ingest_terminal`) with the updated run; terminal refresh calls only `ingest_terminal`; a raising `ingest_completed` doesn't fail the refresh; unchanged snapshots still trigger ingest.
- [x] All 6 council unit-test files green: 95 passed.
- [x] `bash scripts/verify-py.sh`: ruff check/format, pyright (0 errors), import-linter (8 contracts) all pass.



## c868af2f — feat(channels): add engine Feishu/WeCom guided QR setup (#3137)

- **SHA**: c868af2ff63d4dd5536961b82ef315d641262970
- **作者**: bill-srp
- **日期**: 2026-07-30T09:08:22Z
- **PR**: #3137

### 完整 Commit Message

```
feat(channels): add engine Feishu/WeCom guided QR setup (#3137)

## Linear

No Linear issue — this is spec-driven work. Design of record:
[`docs/superpowers/specs/2026-07-29-engine-feishu-wecom-qr-setup.md`](../blob/codex/engine-feishu-wecom-qr/docs/superpowers/specs/2026-07-29-engine-feishu-wecom-qr-setup.md)
(slices EQ-0, EQ-1, EQ-2).

## Summary

Lifts the remaining half of the 2026-07-20 engine-channels non-goal —
*"No QR/guided auto-provision wizard for engine Slack/Feishu/WeCom in
v1"* — for **Feishu and WeCom**. Slack shipped separately in #3131.

Engine users could already connect both platforms by pasting console
credentials. This drives the same app-registration handshakes the bot
leg uses, so nobody has to open a developer console, create an app, and
copy two secrets by hand. **Manual entry stays** as the fallback — this
is purely additive.

### EQ-0 — generic engine setup-session store (`refactor` commit)

`engine_weixin_session.py` was never a fork of the v1 stores; it is a
claim/lease state machine that exists because the ACS terminal mutation
can span two consecutive 120s timeouts. Rather than grow two more
hand-forked copies of a ~300-line concurrency invariant, its
platform-independent half moves into a generic
`EngineSetupSessionStore[SessionT]`, parameterized by key prefix and
payload dataclass. **Weixin stays the only caller in that commit**, so
the migration is reviewable in isolation.

Behaviour is unchanged by construction: the five Lua scripts, the
`current:` claim key, the 300s lease and the Redis-absent fallback move
verbatim; Redis key prefixes, the logger name and the
`[ENGINE_WEIXIN_SETUP]` log prefix all come out identical, so sessions
in flight across the deploy keep working.

### EQ-1 / EQ-2 — Feishu and WeCom (`feat` commit)

Six routes under the `/agents` group, GET/POST only, gated by
`AGENTS_V2_ENABLED` and workspace-guarded. Setup is a credential
mutation so it requires an `active` workspace; poll and cancel follow
the Weixin precedent.

Both handshake helpers are extracted so the two runtimes share one
implementation — `_feishu_registration` into
`app/services/openclaw/feishu_registration.py`, and the WeCom QR pair
(previously inline in the v1 route) into `wecom_registration.py`. The v1
helpers remain as thin wrappers passing
`client_factory=httpx.AsyncClient`, preserving their existing HTTP patch
seam and the module constants the v1 route tests read.

Three things in the v1 terminal step do **not** carry over: the bot
lookup + `client.add_channel` becomes `_create_channel_acs`;
`enable_skills` drops (engine Weixin does not call it);
`_try_set_channel_bound_agent` drops because engine channels have no
`bound_agent_id`. The config written to ACS is exactly what the manual
engine path already sends today — `{appId, appSecret, domain}` and
`{botId, secret}` — which is the main reason this is low-risk.

Unlike Weixin, the account stays **user-chosen** rather than pinned to
`"default"`: Feishu/WeCom credentials are durable and a workspace may
legitimately hold several. Collisions are refused up front, and one
appearing between setup and the terminal write surfaces as
`channel.conflict` from ACS's 409 — never a silent credential overwrite.

Frontend: both modals take an optional `workspaceId` and branch
start/poll/cancel on it, exactly as `WeixinSetupModal` already does;
without it they keep calling the v1 bot-scoped endpoints. `feishu` and
`wecom` join `ENGINE_GUIDED_PLATFORMS`. The account field stays visible
and editable (Weixin hides it only because its backend pins the
account).

### Note on the merge commit

Main landed the Slack slice as a squash (#3131) while this branch
carried its own copy, so `origin/main` was merged in and six conflicts
resolved toward this branch — main's versions asserted the pre-change
behaviour (engine Feishu/WeCom on bare manual entry) that this PR
deliberately replaces. Both gates were re-run green on the merged tree.

## Test plan

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright (0
errors), import-linter (8/8 contracts)
- [x] `bash scripts/verify-web.sh` — 7 governance guards, tsc, **7453**
vitest tests, eslint
- [x] Full backend suite incl. BDD, CI-equivalent (`-n 4 --dist
loadfile`, Mongo on `127.0.0.1`) — **7347 passed**, coverage **89.61%**
- [x] jscpd duplication **2.64%** against the 3.0% gate; file-length and
complexity guards clean
- [ ] **Staging smoke (owed before release)** — one engine Feishu QR
provision with a message round-trip, one engine WeCom QR provision. This
also settles open question 1 in the spec: whether ACS accepts the Feishu
`domain` config key on the engine leg. The bot payload includes it, but
the engine manual form collects only `appId`/`appSecret`, so if ACS
rejects unknown keys the guided flow would fail where manual entry
succeeds.

## Review findings — fixed in `0b614239b`

Three P1s, raised independently by local review and the Codex gate, all
the same class: a recoverable condition escalated into a terminal wizard
failure.

1. **Feishu poll treated every exception as terminal.** One
`httpx.ReadTimeout` inside the 10-minute QR window ended the flow.
Timeouts and network errors now return `pending`; anything else stays
terminal.
2. **WeCom poll dropped v1's 429-as-transient handling.**
`wecom_query_result()` raises on any non-2xx, so a single upstream
rate-limit aborted the engine wizard where the bot leg keeps polling — a
regression against shipped behaviour. Mapping extracted to
`_poll_outcome_from_exception`, mirroring v1's helper, including its
rule about never logging the exception (httpx stringifies the URL, which
embeds the one-time `scode`).
3. **Feishu `slow_down` save was unguarded**, so a session-store blip
turned a non-terminal provider hint into a server error. Now
best-effort, consistent with the brand persist above it.

Five tests added, each watched failing first. Two pin the boundary
rather than the fix — an unexpected Feishu exception and a WeCom 500
must still be terminal — so the retry paths cannot quietly widen into
swallowing real errors.

## Known follow-ups

Still open, not fixed here:

1. **The EQ-0 concurrency test does not test concurrency.**
`asyncio.gather` over the Redis-absent path cannot interleave — there is
no `await` between the read and write — so `["binding", "claimed"]`
holds sequentially. The property the spec asked EQ-0 to prove is
currently unproven.
2. No mock-backend handlers for engine Feishu/WeCom, so the documented
`scripts/dev-mock.sh` workflow cannot drive either new flow.
3. `_claim_terminal_write` is duplicated verbatim between the two new
services; it belongs next to its siblings in
`engine_channel_setup_service`.

## Deploy

Backend first, then web.
```

### PR Body

## Linear

No Linear issue — this is spec-driven work. Design of record: [`docs/superpowers/specs/2026-07-29-engine-feishu-wecom-qr-setup.md`](../blob/codex/engine-feishu-wecom-qr/docs/superpowers/specs/2026-07-29-engine-feishu-wecom-qr-setup.md) (slices EQ-0, EQ-1, EQ-2).

## Summary

Lifts the remaining half of the 2026-07-20 engine-channels non-goal — *"No QR/guided auto-provision wizard for engine Slack/Feishu/WeCom in v1"* — for **Feishu and WeCom**. Slack shipped separately in #3131.

Engine users could already connect both platforms by pasting console credentials. This drives the same app-registration handshakes the bot leg uses, so nobody has to open a developer console, create an app, and copy two secrets by hand. **Manual entry stays** as the fallback — this is purely additive.

### EQ-0 — generic engine setup-session store (`refactor` commit)

`engine_weixin_session.py` was never a fork of the v1 stores; it is a claim/lease state machine that exists because the ACS terminal mutation can span two consecutive 120s timeouts. Rather than grow two more hand-forked copies of a ~300-line concurrency invariant, its platform-independent half moves into a generic `EngineSetupSessionStore[SessionT]`, parameterized by key prefix and payload dataclass. **Weixin stays the only caller in that commit**, so the migration is reviewable in isolation.

Behaviour is unchanged by construction: the five Lua scripts, the `current:` claim key, the 300s lease and the Redis-absent fallback move verbatim; Redis key prefixes, the logger name and the `[ENGINE_WEIXIN_SETUP]` log prefix all come out identical, so sessions in flight across the deploy keep working.

### EQ-1 / EQ-2 — Feishu and WeCom (`feat` commit)

Six routes under the `/agents` group, GET/POST only, gated by `AGENTS_V2_ENABLED` and workspace-guarded. Setup is a credential mutation so it requires an `active` workspace; poll and cancel follow the Weixin precedent.

Both handshake helpers are extracted so the two runtimes share one implementation — `_feishu_registration` into `app/services/openclaw/feishu_registration.py`, and the WeCom QR pair (previously inline in the v1 route) into `wecom_registration.py`. The v1 helpers remain as thin wrappers passing `client_factory=httpx.AsyncClient`, preserving their existing HTTP patch seam and the module constants the v1 route tests read.

Three things in the v1 terminal step do **not** carry over: the bot lookup + `client.add_channel` becomes `_create_channel_acs`; `enable_skills` drops (engine Weixin does not call it); `_try_set_channel_bound_agent` drops because engine channels have no `bound_agent_id`. The config written to ACS is exactly what the manual engine path already sends today — `{appId, appSecret, domain}` and `{botId, secret}` — which is the main reason this is low-risk.

Unlike Weixin, the account stays **user-chosen** rather than pinned to `"default"`: Feishu/WeCom credentials are durable and a workspace may legitimately hold several. Collisions are refused up front, and one appearing between setup and the terminal write surfaces as `channel.conflict` from ACS's 409 — never a silent credential overwrite.

Frontend: both modals take an optional `workspaceId` and branch start/poll/cancel on it, exactly as `WeixinSetupModal` already does; without it they keep calling the v1 bot-scoped endpoints. `feishu` and `wecom` join `ENGINE_GUIDED_PLATFORMS`. The account field stays visible and editable (Weixin hides it only because its backend pins the account).

### Note on the merge commit

Main landed the Slack slice as a squash (#3131) while this branch carried its own copy, so `origin/main` was merged in and six conflicts resolved toward this branch — main's versions asserted the pre-change behaviour (engine Feishu/WeCom on bare manual entry) that this PR deliberately replaces. Both gates were re-run green on the merged tree.

## Test plan

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright (0 errors), import-linter (8/8 contracts)
- [x] `bash scripts/verify-web.sh` — 7 governance guards, tsc, **7453** vitest tests, eslint
- [x] Full backend suite incl. BDD, CI-equivalent (`-n 4 --dist loadfile`, Mongo on `127.0.0.1`) — **7347 passed**, coverage **89.61%**
- [x] jscpd duplication **2.64%** against the 3.0% gate; file-length and complexity guards clean
- [ ] **Staging smoke (owed before release)** — one engine Feishu QR provision with a message round-trip, one engine WeCom QR provision. This also settles open question 1 in the spec: whether ACS accepts the Feishu `domain` config key on the engine leg. The bot payload includes it, but the engine manual form collects only `appId`/`appSecret`, so if ACS rejects unknown keys the guided flow would fail where manual entry succeeds.

## Review findings — fixed in `0b614239b`

Three P1s, raised independently by local review and the Codex gate, all the same class: a recoverable condition escalated into a terminal wizard failure.

1. **Feishu poll treated every exception as terminal.** One `httpx.ReadTimeout` inside the 10-minute QR window ended the flow. Timeouts and network errors now return `pending`; anything else stays terminal.
2. **WeCom poll dropped v1's 429-as-transient handling.** `wecom_query_result()` raises on any non-2xx, so a single upstream rate-limit aborted the engine wizard where the bot leg keeps polling — a regression against shipped behaviour. Mapping extracted to `_poll_outcome_from_exception`, mirroring v1's helper, including its rule about never logging the exception (httpx stringifies the URL, which embeds the one-time `scode`).
3. **Feishu `slow_down` save was unguarded**, so a session-store blip turned a non-terminal provider hint into a server error. Now best-effort, consistent with the brand persist above it.

Five tests added, each watched failing first. Two pin the boundary rather than the fix — an unexpected Feishu exception and a WeCom 500 must still be terminal — so the retry paths cannot quietly widen into swallowing real errors.

## Known follow-ups

Still open, not fixed here:

1. **The EQ-0 concurrency test does not test concurrency.** `asyncio.gather` over the Redis-absent path cannot interleave — there is no `await` between the read and write — so `["binding", "claimed"]` holds sequentially. The property the spec asked EQ-0 to prove is currently unproven.
2. No mock-backend handlers for engine Feishu/WeCom, so the documented `scripts/dev-mock.sh` workflow cannot drive either new flow.
3. `_claim_terminal_write` is duplicated verbatim between the two new services; it belongs next to its siblings in `engine_channel_setup_service`.

## Deploy

Backend first, then web.



## 1d58c556 — fix(agents): allow tar root directory entries (#3143)

- **SHA**: 1d58c556184306ee8c48b526bfda9fd90228bfa4
- **作者**: bill-srp
- **日期**: 2026-07-30T09:05:43Z
- **PR**: #3143

### 完整 Commit Message

```
fix(agents): allow tar root directory entries (#3143)

## Summary

- Ignore the explicit `.` root directory entry emitted by tar archives
during agent-pack indexing.
- Keep rejecting a file named `.`, traversal paths, absolute paths, and
links.
- Add regression coverage for the environment-repack path used by
staging rebuilds.

## Root cause

The staging Video Duplicate pack archive contains a harmless tar
directory member named `.`. The claw-interface archive index passed
every member through the non-empty path validator before filtering
directories, so the root placeholder normalized to an empty path and
failed with `Pack archive contains an unsafe member path` before
zooclaw-engine was called.

## Test plan

- [x] `pytest tests/unit/test_engine_pack_translation.py -q` — 57 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
```

### PR Body

## Summary

- Ignore the explicit `.` root directory entry emitted by tar archives during agent-pack indexing.
- Keep rejecting a file named `.`, traversal paths, absolute paths, and links.
- Add regression coverage for the environment-repack path used by staging rebuilds.

## Root cause

The staging Video Duplicate pack archive contains a harmless tar directory member named `.`. The claw-interface archive index passed every member through the non-empty path validator before filtering directories, so the root placeholder normalized to an empty path and failed with `Pack archive contains an unsafe member path` before zooclaw-engine was called.

## Test plan

- [x] `pytest tests/unit/test_engine_pack_translation.py -q` — 57 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`



## f6cc1c1d — fix(chat): 优化 New Task 类目与快捷卡片体验 (#3142)

- **SHA**: f6cc1c1d732420896d5e7fe2eaf09119f13d99de
- **作者**: lynn Zhuang
- **日期**: 2026-07-30T09:02:20Z
- **PR**: #3142

### 完整 Commit Message

```
fix(chat): 优化 New Task 类目与快捷卡片体验 (#3142)

## 变更概要

- 按照已确认的目录，同步 New Task 的一级类目、快捷卡片、Agent 分配，以及点击卡片后写入输入框的完整 Prompt。
- 复用官网 Landing 页的类目胶囊结构，同时让 Chat UI 版本适配亮色/暗色主题，包括右上角选中对勾、柔和描边、单色图标和通过
Portal 渲染的 More 下拉菜单。
- 选择 More 中的「Plan Marketing」后，一级入口会切换为当前类目，并正确展示选中态、对勾及对应卡片。
- 仅在用户从 Agent Picker 中显式选择 Agent 后，入口才由「Hire Agent」替换为具体 Agent；starter
自动匹配 Agent 时仍保留「Hire Agent」。
- 未完成新版卡片翻译的语言会显式回退到最新版英文目录，避免继续展示旧卡片和旧 Prompt。
- 将 starter 图标的组件样式从全局样式表迁移到 CSS Module，避免组件选择器污染其他页面。

## 根因

Landing 和应用内 New Task 长期使用了两套独立的内容及样式路径，导致类目、卡片和 Prompt 逐渐不一致。直接复用
Landing 的亮色 token 后，又造成暗色模式下描边、文字、图标和 Portal 菜单对比度异常。

另外，More 中的类目虽然能更新内容区域，但原入口没有同步展示当前选中类目；Agent 的发送目标状态也与“用户是否显式操作
Picker”共用了同一个判断，导致 starter 自动匹配 Agent 时错误替换「Hire Agent」文案。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui test` — 337 个测试通过
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] New Task / Landing 相关定向测试 — 105 个测试通过
- [x] Agent Picker 与 starter 交互相关测试 — 43 个测试通过
- [x] 本地实际页面验证：类目选中态、More 菜单及图标、Prompt 自动填充、亮色/暗色模式、Agent Picker 文案
- [x] GitHub CI — 41/41 通过
- [x] Codex Review — `APPROVE`，无新增问题
```

### PR Body

## 变更概要

- 按照已确认的目录，同步 New Task 的一级类目、快捷卡片、Agent 分配，以及点击卡片后写入输入框的完整 Prompt。
- 复用官网 Landing 页的类目胶囊结构，同时让 Chat UI 版本适配亮色/暗色主题，包括右上角选中对勾、柔和描边、单色图标和通过 Portal 渲染的 More 下拉菜单。
- 选择 More 中的「Plan Marketing」后，一级入口会切换为当前类目，并正确展示选中态、对勾及对应卡片。
- 仅在用户从 Agent Picker 中显式选择 Agent 后，入口才由「Hire Agent」替换为具体 Agent；starter 自动匹配 Agent 时仍保留「Hire Agent」。
- 未完成新版卡片翻译的语言会显式回退到最新版英文目录，避免继续展示旧卡片和旧 Prompt。
- 将 starter 图标的组件样式从全局样式表迁移到 CSS Module，避免组件选择器污染其他页面。

## 根因

Landing 和应用内 New Task 长期使用了两套独立的内容及样式路径，导致类目、卡片和 Prompt 逐渐不一致。直接复用 Landing 的亮色 token 后，又造成暗色模式下描边、文字、图标和 Portal 菜单对比度异常。

另外，More 中的类目虽然能更新内容区域，但原入口没有同步展示当前选中类目；Agent 的发送目标状态也与“用户是否显式操作 Picker”共用了同一个判断，导致 starter 自动匹配 Agent 时错误替换「Hire Agent」文案。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm --filter @zooclaw/chat-ui tsc`
- [x] `pnpm --filter @zooclaw/chat-ui test` — 337 个测试通过
- [x] `pnpm --filter @zooclaw/chat-ui lint`
- [x] New Task / Landing 相关定向测试 — 105 个测试通过
- [x] Agent Picker 与 starter 交互相关测试 — 43 个测试通过
- [x] 本地实际页面验证：类目选中态、More 菜单及图标、Prompt 自动填充、亮色/暗色模式、Agent Picker 文案
- [x] GitHub CI — 41/41 通过
- [x] Codex Review — `APPROVE`，无新增问题



## cdfe6d69 — fix(billing): show Stripe checkout in staging (#3141)

- **SHA**: cdfe6d69dc5f2a155496eb8fbbb3a03bb83dfcc6
- **作者**: tim-srp
- **日期**: 2026-07-30T08:06:58Z
- **PR**: #3141

### 完整 Commit Message

```
fix(billing): show Stripe checkout in staging (#3141)

## Summary
- Show the Stripe card payment entry in staging and local development.
- Keep the Stripe entry hidden in production and unknown environments.
- Reuse the existing `NEXT_PUBLIC_APP_ENV`; no deployment variables or
workflow changes are required.
- Keep all Stripe checkout, webhook, and subscription logic unchanged.

## Root cause
The previous production safety change removed the Stripe option
unconditionally, which also prevented staging from exercising the Stripe
sandbox flow.

## Test plan
- [x] `pnpm --dir web/app exec vitest run
tests/unit/lib/env.unit.spec.ts
tests/unit/components/billing/PaymentMethodModal.unit.spec.tsx
tests/unit/components/PaywallContent.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh web/app/src/lib/env.ts
web/app/src/components/billing/PaymentMethodModal.tsx
web/app/tests/unit/lib/env.unit.spec.ts
web/app/tests/unit/components/billing/PaymentMethodModal.unit.spec.tsx`
- [x] Pre-push changed-surface verification
```

### PR Body

## Summary
- Show the Stripe card payment entry in staging and local development.
- Keep the Stripe entry hidden in production and unknown environments.
- Reuse the existing `NEXT_PUBLIC_APP_ENV`; no deployment variables or workflow changes are required.
- Keep all Stripe checkout, webhook, and subscription logic unchanged.

## Root cause
The previous production safety change removed the Stripe option unconditionally, which also prevented staging from exercising the Stripe sandbox flow.

## Test plan
- [x] `pnpm --dir web/app exec vitest run tests/unit/lib/env.unit.spec.ts tests/unit/components/billing/PaymentMethodModal.unit.spec.tsx tests/unit/components/PaywallContent.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh web/app/src/lib/env.ts web/app/src/components/billing/PaymentMethodModal.tsx web/app/tests/unit/lib/env.unit.spec.ts web/app/tests/unit/components/billing/PaymentMethodModal.unit.spec.tsx`
- [x] Pre-push changed-surface verification



## 5629df53 — feat(ios): add session history navigation (#3140)

- **SHA**: 5629df532b4cb35c91b673517273f637fe1899ce
- **作者**: tim-srp
- **日期**: 2026-07-30T07:29:12Z
- **PR**: #3140

### 完整 Commit Message

```
feat(ios): add session history navigation (#3140)

## Linear

- N/A

## Summary

- Add a Session History row to each expanded agent in the iOS sidebar.
- Route Session History to the selected agent's DM/history channel
instead of opening the latest concrete session.
- Guard asynchronous history navigation from clearing a newer session
selection and add focused regression coverage.

## Test plan

- [x] Regression coverage for history-channel routing and stale
selection handling passed in #3130.
- [x] GitHub Actions `ios-quality` passed for the fix branch.
- [x] TestFlight upload for iOS 1.8.2 build 3 succeeded.
- Local tests were not rerun, per request.

---------

Co-authored-by: bill-srp <bill@srp.one>
```

### PR Body

## Linear

- N/A

## Summary

- Add a Session History row to each expanded agent in the iOS sidebar.
- Route Session History to the selected agent's DM/history channel instead of opening the latest concrete session.
- Guard asynchronous history navigation from clearing a newer session selection and add focused regression coverage.

## Test plan

- [x] Regression coverage for history-channel routing and stale selection handling passed in #3130.
- [x] GitHub Actions `ios-quality` passed for the fix branch.
- [x] TestFlight upload for iOS 1.8.2 build 3 succeeded.
- Local tests were not rerun, per request.



## 4135e11f — fix(agent-builder): allow stable v1 project migrations (#3138)

- **SHA**: 4135e11f2e9ad6fe2a346596ea32905dea0bb9ed
- **作者**: kaka-srp
- **日期**: 2026-07-30T07:03:22Z
- **PR**: #3138

### 完整 Commit Message

```
fix(agent-builder): allow stable v1 project migrations (#3138)

## Summary

- make the backend the authoritative Agent Builder v1-to-v2 migration
readiness gate
- allow stable Pack Test states such as preview, review, accepted,
failed, and cleaned
- block only active source import, packaging, Test runtime
provisioning/transfer, promotion, and archived projects
- remove the frontend's duplicate busy-status list so it cannot drift
from backend behavior
- document the readiness matrix and add regression coverage for every
Pack Test status

## Why

Legacy projects could become permanently un-migratable after a Pack Test
because the project-level status remained `testing` or `reviewing_test`,
even though the associated TestRun had already reached a stable state.
The staging project that exposed this was in `reviewing_test` with a
`previewing` TestRun.

The migration already preserves the current iteration and TestRun
identifiers and finishes with a compare-and-set. Stable review states
therefore do not need to block migration; only operations that are
actively producing side effects must wait.

## Validation

- `pytest -q tests/unit/test_agent_builder_migration_service.py` — 32
passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-web.sh
'src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderProjectActions.tsx'`
- pre-push changed-surface verification
```

### PR Body

## Summary

- make the backend the authoritative Agent Builder v1-to-v2 migration readiness gate
- allow stable Pack Test states such as preview, review, accepted, failed, and cleaned
- block only active source import, packaging, Test runtime provisioning/transfer, promotion, and archived projects
- remove the frontend's duplicate busy-status list so it cannot drift from backend behavior
- document the readiness matrix and add regression coverage for every Pack Test status

## Why

Legacy projects could become permanently un-migratable after a Pack Test because the project-level status remained `testing` or `reviewing_test`, even though the associated TestRun had already reached a stable state. The staging project that exposed this was in `reviewing_test` with a `previewing` TestRun.

The migration already preserves the current iteration and TestRun identifiers and finishes with a compare-and-set. Stable review states therefore do not need to block migration; only operations that are actively producing side effects must wait.

## Validation

- `pytest -q tests/unit/test_agent_builder_migration_service.py` — 32 passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-web.sh 'src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderProjectActions.tsx'`
- pre-push changed-surface verification



## b2f7b4a5 — fix(skills): update skill icon (#3092)

- **SHA**: b2f7b4a5d84586d5e2f329552af07ccb827e8d8c
- **作者**: shana-srp
- **日期**: 2026-07-30T06:57:38Z
- **PR**: #3092

### 完整 Commit Message

```
fix(skills): update skill icon (#3092)

## Summary

- replace the legacy wrench sprite used by Skill cards and menus
- add the provided Skill SVG as a dedicated static asset
- render Skill icons directly through `next/image` while preserving
existing sizes

## Validation

- `bash scripts/verify-changed.sh`
- local Skill page and SVG asset both return HTTP 200
- manual preview at `/skills/search`

## Screenshots

- Updated icon verified in the local Skill module preview.

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Body

## Summary

- replace the legacy wrench sprite used by Skill cards and menus
- add the provided Skill SVG as a dedicated static asset
- render Skill icons directly through `next/image` while preserving existing sizes

## Validation

- `bash scripts/verify-changed.sh`
- local Skill page and SVG asset both return HTTP 200
- manual preview at `/skills/search`

## Screenshots

- Updated icon verified in the local Skill module preview.



## fcb95918 — fix(billing): hide Stripe subscription entry (#3136)

- **SHA**: fcb95918126b45c9b3c34d9b6b6b8466b69f05cf
- **作者**: tim-srp
- **日期**: 2026-07-30T06:43:03Z
- **PR**: #3136

### 完整 Commit Message

```
fix(billing): hide Stripe subscription entry (#3136)

## Summary
- Hide the Stripe card option from the shared subscription
payment-method modal.
- Keep Alipay available and remove the card authorization notice from
the visible UI.
- Preserve the existing Stripe checkout, webhook, subscription
lifecycle, and billing-management logic.

## Root cause
The shared payment-method modal still rendered the Stripe card
subscription entry after the Stripe account became unavailable.

## Test plan
- [x] `pnpm --dir web/app exec vitest run
tests/unit/components/billing/PaymentMethodModal.unit.spec.tsx
tests/unit/components/PaywallContent.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx
tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh
web/app/src/components/billing/PaymentMethodModal.tsx
web/app/tests/unit/components/billing/PaymentMethodModal.unit.spec.tsx
web/app/tests/unit/components/PaywallContent.unit.spec.tsx`
- [x] Pre-push changed-surface verification
```

### PR Body

## Summary
- Hide the Stripe card option from the shared subscription payment-method modal.
- Keep Alipay available and remove the card authorization notice from the visible UI.
- Preserve the existing Stripe checkout, webhook, subscription lifecycle, and billing-management logic.

## Root cause
The shared payment-method modal still rendered the Stripe card subscription entry after the Stripe account became unavailable.

## Test plan
- [x] `pnpm --dir web/app exec vitest run tests/unit/components/billing/PaymentMethodModal.unit.spec.tsx tests/unit/components/PaywallContent.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel.unit.spec.tsx tests/unit/components/billing/SubscriptionPanel-extras.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh web/app/src/components/billing/PaymentMethodModal.tsx web/app/tests/unit/components/billing/PaymentMethodModal.unit.spec.tsx web/app/tests/unit/components/PaywallContent.unit.spec.tsx`
- [x] Pre-push changed-surface verification



## c21955b9 — refactor(chat): 抽离并复用 New Task 引导组件 (#3135)

- **SHA**: c21955b92df7a44a12108749ea369ca43bd04b75
- **作者**: lynn Zhuang
- **日期**: 2026-07-30T06:10:11Z
- **PR**: #3135

### 完整 Commit Message

```
refactor(chat): 抽离并复用 New Task 引导组件 (#3135)

## 变更说明

本 PR 主要是组件抽离与复用优化：将 landing 页面输入框下方已有的新任务引导能力整理为共享组件，并在登录后的 New Task
页面复用，减少两套实现之间的样式和交互漂移。

- 从 landing 页面抽离 `NewTaskStarter` 与 `NewTaskTemplateDialog` 到
`@zooclaw/chat-ui`，统一承载能力分类、示例 Prompt、Agent 标识、模板卡片与预览、选中状态、键盘操作及无障碍语义。
- landing 与登录后的 New Task 页面共用同一套 starter catalog 和组件；已有 Chat Session
仍保持输入框固定在页面底部，不改变会话内布局。
- 保持 landing 当前的使用方式：点击示例或模板后，将推荐 Agent 与 Prompt 填入输入框，用户可以修改后再发送；未安装的可用
Agent 在发送时自动 Hire。
- 对齐 ZooClaw 当前产品信息：New Task 中不展示 Agent Builder；Organize Work
提升为一级分类；Marketing 保留在 More 中；入口统一使用 Hire Agent，并复用线上图标。
- 补齐组件复用后的边界处理：内置 Assistant 正确映射到 Main Agent；连续切换模板不会嵌套旧 Prompt；选择
Prompt 或模板后焦点回到输入框末尾。
- 同步设计说明、实现计划与回归测试。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm run lint:ci`
- [x] `bash scripts/check-pr-size.sh` — 2886 / 3000 行
- [x] New Task、landing、Unified Composer 相关测试 — 94 tests
- [x] `@zooclaw/chat-ui` 全量测试 — 333 tests
- [x] `@zooclaw/chat-ui` TypeScript 与 ESLint
- [x] GitHub CI 与自动审查 — 41 / 41 passed
- [ ] 本地未运行完整 Playwright E2E；以部署环境 E2E 为准。

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR Body

## 变更说明

本 PR 主要是组件抽离与复用优化：将 landing 页面输入框下方已有的新任务引导能力整理为共享组件，并在登录后的 New Task 页面复用，减少两套实现之间的样式和交互漂移。

- 从 landing 页面抽离 `NewTaskStarter` 与 `NewTaskTemplateDialog` 到 `@zooclaw/chat-ui`，统一承载能力分类、示例 Prompt、Agent 标识、模板卡片与预览、选中状态、键盘操作及无障碍语义。
- landing 与登录后的 New Task 页面共用同一套 starter catalog 和组件；已有 Chat Session 仍保持输入框固定在页面底部，不改变会话内布局。
- 保持 landing 当前的使用方式：点击示例或模板后，将推荐 Agent 与 Prompt 填入输入框，用户可以修改后再发送；未安装的可用 Agent 在发送时自动 Hire。
- 对齐 ZooClaw 当前产品信息：New Task 中不展示 Agent Builder；Organize Work 提升为一级分类；Marketing 保留在 More 中；入口统一使用 Hire Agent，并复用线上图标。
- 补齐组件复用后的边界处理：内置 Assistant 正确映射到 Main Agent；连续切换模板不会嵌套旧 Prompt；选择 Prompt 或模板后焦点回到输入框末尾。
- 同步设计说明、实现计划与回归测试。

## 验证

- [x] `bash scripts/verify-changed.sh`
- [x] `pnpm run lint:ci`
- [x] `bash scripts/check-pr-size.sh` — 2886 / 3000 行
- [x] New Task、landing、Unified Composer 相关测试 — 94 tests
- [x] `@zooclaw/chat-ui` 全量测试 — 333 tests
- [x] `@zooclaw/chat-ui` TypeScript 与 ESLint
- [x] GitHub CI 与自动审查 — 41 / 41 passed
- [ ] 本地未运行完整 Playwright E2E；以部署环境 E2E 为准。



## db01d1c3 — feat(agents-manager): show agent avatars on publish page (#3109)

- **SHA**: db01d1c3111602b7ae29dfa1c1ae8b39fb7feea2
- **作者**: ericma-srp
- **日期**: 2026-07-30T05:54:12Z
- **PR**: #3109

### 完整 Commit Message

```
feat(agents-manager): show agent avatars on publish page (#3109)

## What changed

- preserve existing `avatar_url` values while building publish-page
agent records
- show each agent's real avatar on cards, details, confirmation dialogs,
and install/update result dialogs
- keep the existing emoji when the avatar URL is missing or blank
- prefer an installed workspace avatar over the matching organization
pack avatar

## Why

The publish page received avatar data from existing APIs but dropped it
while creating its local card view model, so every agent rendered the
same fixed emoji.

## Impact

Agents on `/agents-manager/publish` now keep a consistent identity
throughout the publish and lifecycle flows. No backend, API, database,
or additional network request changes are included.

## Validation

- `corepack pnpm exec vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx` - 64 passed
- publish page plus install/update hook coverage - 80 tests passed
- `bash scripts/verify-web.sh --no-test` - governance guards,
TypeScript, and ESLint passed
- pre-push changed-surface verification passed

---------

Co-authored-by: eric <eric.ma@creatibi.com>
```

### PR Body

## What changed

- preserve existing `avatar_url` values while building publish-page agent records
- show each agent's real avatar on cards, details, confirmation dialogs, and install/update result dialogs
- keep the existing emoji when the avatar URL is missing or blank
- prefer an installed workspace avatar over the matching organization pack avatar

## Why

The publish page received avatar data from existing APIs but dropped it while creating its local card view model, so every agent rendered the same fixed emoji.

## Impact

Agents on `/agents-manager/publish` now keep a consistent identity throughout the publish and lifecycle flows. No backend, API, database, or additional network request changes are included.

## Validation

- `corepack pnpm exec vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx` - 64 passed
- publish page plus install/update hook coverage - 80 tests passed
- `bash scripts/verify-web.sh --no-test` - governance guards, TypeScript, and ESLint passed
- pre-push changed-surface verification passed

