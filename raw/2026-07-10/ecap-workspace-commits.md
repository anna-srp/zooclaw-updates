# SerendipityOneInc/ecap-workspace — commits 2026-07-10

共 16 个 commit


## feat(dashboard-console): add kit groundwork for admin pages redesign (#2827)

- **sha**: `004f48d6059bba51cf2af89e184c1d81bf18e222`
- **author**: bill-srp
- **date**: 2026-07-10T13:08:59Z

### Commit message

```
feat(dashboard-console): add kit groundwork for admin pages redesign (#2827)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- No Linear issue; design spec committed in this PR:
docs/superpowers/specs/2026-07-10-console-admin-pages-redesign-design.md
-->

## Summary
Slice 1 of 5 (kit groundwork) of the console Administration pages
redesign. Design spec included in this PR
(`docs/superpowers/specs/2026-07-10-console-admin-pages-redesign-design.md`);
no page recomposition here (that is slices 2-3).

- **R1 status semantics**: extend `DOMAIN_STATUS_TONE` in `ui-kit.tsx`
with the subscription vocabulary (`trial`/`past_due` amber,
`expired`/`canceled` red, `free` neutral) and add an optional `label`
prop to `StatusBadge`. Delete the private `subscriptionTone()` duplicate
in `boost-subscription-dialog.tsx` and use the kit; tones there are
unchanged.
- **R5 groundwork**: restyle the dead stock shadcn `ui/skeleton.tsx` to
ZooClaw tokens (`bg-zc-canvas-2`, ledger radius) and add `TableSkeleton`
(configurable rows/columns) to the kit for later slices. Not wired to
pages yet.
- **`RowMenu`**: new ledger-styled per-row overflow menu (radix
DropdownMenu, required accessible trigger label, icon items,
`danger`/`disabled` states). Not wired to pages yet; consumed by slices
2-3.
- **`ConsoleDialog` shell**: generalize `agent-packs/dialog-kit.tsx`'s
`DialogHead`/`DialogFoot` into a shared `app/components/dialog-kit.tsx`
(`ConsoleDialog`/`Header`/`Body`/`Footer`, preserving `showCloseButton`
gating, `max-h` override, responsive footer variant) and migrate the six
agent-packs dialog consumers pixel-for-pixel. The
users/subscription-codes/releases dialogs port in slices 2-3.

Implemented by Codex (rescue task) from the spec; reviewed, re-verified,
and committed by Claude.

## Test plan
- [x] New colocated Vitest tests: `StatusBadge` label/tone,
`TableSkeleton` shape + `role="status"`, `RowMenu`
accessibility/selection/disabled, `ConsoleDialog` shell + close gating,
`Skeleton` tokens
- [x] Full suite: `pnpm exec vitest run` — 63 files, 522 tests pass
(baseline was 60/509)
- [x] `pnpm run typecheck` — exit 0
- [x] `pnpm run lint` — exit 0
- [x] Agent-packs dialog tests pass unmodified (pixel-for-pixel
migration)
```

### PR body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- No Linear issue; design spec committed in this PR: docs/superpowers/specs/2026-07-10-console-admin-pages-redesign-design.md -->

## Summary
Slice 1 of 5 (kit groundwork) of the console Administration pages redesign. Design spec included in this PR (`docs/superpowers/specs/2026-07-10-console-admin-pages-redesign-design.md`); no page recomposition here (that is slices 2-3).

- **R1 status semantics**: extend `DOMAIN_STATUS_TONE` in `ui-kit.tsx` with the subscription vocabulary (`trial`/`past_due` amber, `expired`/`canceled` red, `free` neutral) and add an optional `label` prop to `StatusBadge`. Delete the private `subscriptionTone()` duplicate in `boost-subscription-dialog.tsx` and use the kit; tones there are unchanged.
- **R5 groundwork**: restyle the dead stock shadcn `ui/skeleton.tsx` to ZooClaw tokens (`bg-zc-canvas-2`, ledger radius) and add `TableSkeleton` (configurable rows/columns) to the kit for later slices. Not wired to pages yet.
- **`RowMenu`**: new ledger-styled per-row overflow menu (radix DropdownMenu, required accessible trigger label, icon items, `danger`/`disabled` states). Not wired to pages yet; consumed by slices 2-3.
- **`ConsoleDialog` shell**: generalize `agent-packs/dialog-kit.tsx`'s `DialogHead`/`DialogFoot` into a shared `app/components/dialog-kit.tsx` (`ConsoleDialog`/`Header`/`Body`/`Footer`, preserving `showCloseButton` gating, `max-h` override, responsive footer variant) and migrate the six agent-packs dialog consumers pixel-for-pixel. The users/subscription-codes/releases dialogs port in slices 2-3.

Implemented by Codex (rescue task) from the spec; reviewed, re-verified, and committed by Claude.

## Test plan
- [x] New colocated Vitest tests: `StatusBadge` label/tone, `TableSkeleton` shape + `role="status"`, `RowMenu` accessibility/selection/disabled, `ConsoleDialog` shell + close gating, `Skeleton` tokens
- [x] Full suite: `pnpm exec vitest run` — 63 files, 522 tests pass (baseline was 60/509)
- [x] `pnpm run typecheck` — exit 0
- [x] `pnpm run lint` — exit 0
- [x] Agent-packs dialog tests pass unmodified (pixel-for-pixel migration)



## feat(web): re-enable skills store for computer agents (#2824)

- **sha**: `07d251d466d6b637c770905fd043a778e46a9de7`
- **author**: bill-srp
- **date**: 2026-07-10T12:48:11Z

### Commit message

```
feat(web): re-enable skills store for computer agents (#2824)

# Summary

Frontend slice of the skill-store re-enable: migrates the Skills Store
pages to the V2 computer-agents model and restores the hidden UserMenu
entry. Companion to backend PR #2823 (merged), which added
`agent_id`-based workdir resolution to the clawhub endpoints.

Background: the Skills Store entry was removed from UserMenu in #2569
because the store's install flow was still keyed on the legacy
`useUserAgents` data while the rest of the app moved to V2 computer
agents.

- **BFF** (`api/openclaw/clawhub/[action]/route.ts`): forwards
`agent_id` (query param on list, body field on install/uninstall)
instead of `workdir`; computer resolution / readiness polling / credits
check unchanged.
- **API client** (`lib/api/skills-store.ts`): request types switch from
`workdir` to `agentId`, sent as `agent_id` on the wire.
- **Store pages** (`SkillsSearchClient`, `SkillDetailClient`): migrated
from `useUserAgents` to `useCurrentComputerAgents`, filtered to
runtime-visible agents — consistent with the rest of the app.
- **`lib/skills/agent-install-state.ts`**: workspace-path logic deleted
entirely (`getAgentWorkspace` / `hasAgentWorkspace` /
`DEFAULT_MAIN_AGENT_WORKSPACE`); install state keyed purely by
`agent_id`; `SkillStoreInstalledAgent` now carries `avatar_url` instead
of `emoji`/`workspace`.
- **`useAgentInstalledSkills`**: converted from a hand-rolled
`useEffect` fetcher to React Query, keyed by uid + computer_id + sorted
agent ids.
- **UserMenu**: Skills Store entry restored (navigates to
`/skills/search`), guard test flipped back to the navigation assertion.

# Test Plan

- [x] Updated/added unit specs: BFF route (`openclaw-clawhub`,
`clawhub-polling`), `skills-store` API client, `agent-install-state`,
`useAgentInstalledSkills` (new), `SkillAgentComponents` (new),
`SkillDetailClient`, `SkillsSearchClient`, install-toast integration,
`UserMenu`
- [x] Full `pnpm exec vitest run`: 567 files, 7,576 passed / 0 failed
- [x] `bash scripts/verify-web.sh`: guards + tsc + vitest + eslint all
passed
- [ ] Staging smoke after deploy: open Skills Store from UserMenu,
list/install/uninstall a community skill on main and a non-main agent

# Notes

- Deploy ordering: backend #2823 is already merged; this PR must not be
released to production before a `claw-interface` release containing
#2823 is live (the BFF now sends `agent_id`, which old backends ignore —
that would silently target the main workspace).
- The store previously relied on legacy `useUserAgents`; this PR removes
the store's last dependency on it.
```

### PR body

# Summary

Frontend slice of the skill-store re-enable: migrates the Skills Store pages to the V2 computer-agents model and restores the hidden UserMenu entry. Companion to backend PR #2823 (merged), which added `agent_id`-based workdir resolution to the clawhub endpoints.

Background: the Skills Store entry was removed from UserMenu in #2569 because the store's install flow was still keyed on the legacy `useUserAgents` data while the rest of the app moved to V2 computer agents.

- **BFF** (`api/openclaw/clawhub/[action]/route.ts`): forwards `agent_id` (query param on list, body field on install/uninstall) instead of `workdir`; computer resolution / readiness polling / credits check unchanged.
- **API client** (`lib/api/skills-store.ts`): request types switch from `workdir` to `agentId`, sent as `agent_id` on the wire.
- **Store pages** (`SkillsSearchClient`, `SkillDetailClient`): migrated from `useUserAgents` to `useCurrentComputerAgents`, filtered to runtime-visible agents — consistent with the rest of the app.
- **`lib/skills/agent-install-state.ts`**: workspace-path logic deleted entirely (`getAgentWorkspace` / `hasAgentWorkspace` / `DEFAULT_MAIN_AGENT_WORKSPACE`); install state keyed purely by `agent_id`; `SkillStoreInstalledAgent` now carries `avatar_url` instead of `emoji`/`workspace`.
- **`useAgentInstalledSkills`**: converted from a hand-rolled `useEffect` fetcher to React Query, keyed by uid + computer_id + sorted agent ids.
- **UserMenu**: Skills Store entry restored (navigates to `/skills/search`), guard test flipped back to the navigation assertion.

# Test Plan

- [x] Updated/added unit specs: BFF route (`openclaw-clawhub`, `clawhub-polling`), `skills-store` API client, `agent-install-state`, `useAgentInstalledSkills` (new), `SkillAgentComponents` (new), `SkillDetailClient`, `SkillsSearchClient`, install-toast integration, `UserMenu`
- [x] Full `pnpm exec vitest run`: 567 files, 7,576 passed / 0 failed
- [x] `bash scripts/verify-web.sh`: guards + tsc + vitest + eslint all passed
- [ ] Staging smoke after deploy: open Skills Store from UserMenu, list/install/uninstall a community skill on main and a non-main agent

# Notes

- Deploy ordering: backend #2823 is already merged; this PR must not be released to production before a `claw-interface` release containing #2823 is live (the BFF now sends `agent_id`, which old backends ignore — that would silently target the main workspace).
- The store previously relied on legacy `useUserAgents`; this PR removes the store's last dependency on it.



## feat(dashboard-console): add users mutation workflows (#2820)

- **sha**: `d80a9533bc7f814662601fbf0593f048e38ed8fc`
- **author**: bill-srp
- **date**: 2026-07-10T11:58:38Z

### Commit message

```
feat(dashboard-console): add users mutation workflows (#2820)

## Linear

N/A

## Summary

- add typed dashboard-console contracts for user credits context, credit
grants, and subscription boosts
- add single Grant, multi-user Boost, and resumable Batch Grant
workflows with explicit idempotency and retry behavior
- add current-page selection, bulk action controls, stale-page mutation
guards, operation notices, and structured backend error messages
- include the accepted design spec and implementation plan for the Users
mutation surface

## Test plan

- [x] `cd web/dashboard-console && pnpm lint`
- [x] `cd web/dashboard-console && pnpm typecheck` (exit 0; Wrangler
log-file EPERM is sandbox-only)
- [x] `cd web/dashboard-console && pnpm test` (59 files, 497 tests)
- [x] `cd web/dashboard-console && pnpm test:coverage` (59 files, 493
tests at time of run; suite is now 497)
- [x] `bash scripts/verify-changed.sh` (exit 0; dashboard-console is
outside the locally mapped `web/app` verifier and remains CI-covered)
- [x] `git diff --check origin/main...HEAD`

## Review notes

- batch grant freezes the normalized amount, reason, and campaign after
the first attempt so resume/retry cannot mix operation inputs
- navigation/unmount stops future batch targets; running dialogs ignore
Escape/outside dismissal and require explicit Stop
- stopped batches report succeeded/failed/not-attempted counts,
interrupt backoff within 200 ms, and expose Continue for mixed
failed/pending progress
- batch backoff runs only when another target remains; the Campaign hint
distinguishes a new logical batch from resume/retry
- `skip_subscription_check` is exposed as a visible, default-off
checkbox in the Grant dialog (responding to the 08:29Z Codex P1 dead-end
finding); when off, the field is omitted so the backend default
(`false`) applies; toggling it resets the idempotency key, and the
review step shows the override when enabled — capability parity with the
legacy `web/app` admin surface, which already forwards this flag
- the Batch Grant campaign default is day-scoped
`compensation_<YYYY_MM_DD>` (UTC), not month-scoped (responding to the
09:00Z Codex P1 collision finding); distinct runs on different days no
longer silently replay, and operators resume a prior batch by
re-entering its campaign key per the field hint — the design spec and
plan carry a dated revision note recording both amendments
- successful Boost responses with `results: []` retain the existing
accepted settled-response behavior
```

### PR body

## Linear

N/A

## Summary

- add typed dashboard-console contracts for user credits context, credit grants, and subscription boosts
- add single Grant, multi-user Boost, and resumable Batch Grant workflows with explicit idempotency and retry behavior
- add current-page selection, bulk action controls, stale-page mutation guards, operation notices, and structured backend error messages
- include the accepted design spec and implementation plan for the Users mutation surface

## Test plan

- [x] `cd web/dashboard-console && pnpm lint`
- [x] `cd web/dashboard-console && pnpm typecheck` (exit 0; Wrangler log-file EPERM is sandbox-only)
- [x] `cd web/dashboard-console && pnpm test` (59 files, 497 tests)
- [x] `cd web/dashboard-console && pnpm test:coverage` (59 files, 493 tests at time of run; suite is now 497)
- [x] `bash scripts/verify-changed.sh` (exit 0; dashboard-console is outside the locally mapped `web/app` verifier and remains CI-covered)
- [x] `git diff --check origin/main...HEAD`

## Review notes

- batch grant freezes the normalized amount, reason, and campaign after the first attempt so resume/retry cannot mix operation inputs
- navigation/unmount stops future batch targets; running dialogs ignore Escape/outside dismissal and require explicit Stop
- stopped batches report succeeded/failed/not-attempted counts, interrupt backoff within 200 ms, and expose Continue for mixed failed/pending progress
- batch backoff runs only when another target remains; the Campaign hint distinguishes a new logical batch from resume/retry
- `skip_subscription_check` is exposed as a visible, default-off checkbox in the Grant dialog (responding to the 08:29Z Codex P1 dead-end finding); when off, the field is omitted so the backend default (`false`) applies; toggling it resets the idempotency key, and the review step shows the override when enabled — capability parity with the legacy `web/app` admin surface, which already forwards this flag
- the Batch Grant campaign default is day-scoped `compensation_<YYYY_MM_DD>` (UTC), not month-scoped (responding to the 09:00Z Codex P1 collision finding); distinct runs on different days no longer silently replay, and operators resume a prior batch by re-entering its campaign key per the field hint — the design spec and plan carry a dated revision note recording both amendments
- successful Boost responses with `results: []` retain the existing accepted settled-response behavior




## feat(claw-interface): resolve clawhub workdirs by agent_id (#2823)

- **sha**: `98ca0c140c0494d246095975fdc9304cddbdddcb`
- **author**: bill-srp
- **date**: 2026-07-10T11:19:14Z

### Commit message

```
feat(claw-interface): resolve clawhub workdirs by agent_id (#2823)

# Summary

Backend slice of the skill-store re-enable plan: the ClawHub skill
endpoints now accept an `agent_id` and resolve the target workspace
directory (`workdir`) on demand from FastClaw live config, so the
frontend no longer needs to know workspace path conventions.

- `POST /bots/{bot_id}/clawhub/install`, `GET /bots/{bot_id}/clawhub`,
and `POST /bots/{bot_id}/clawhub/uninstall` accept an optional
`agent_id` (body field on mutations, query param on list).
- New service helper
`app/services/openclaw/clawhub.py::resolve_clawhub_workdir`: `agent_id`
absent → legacy `workdir` passthrough (backward compatible); `agent_id
== "main"` → no workdir (FastClaw defaults to the main workspace);
otherwise resolve via `get_bot` live config + the existing
`build_workspace_by_agent_id` helper.
- Unresolvable agent → stable product-domain 404
`clawhub.agent_workspace_not_found` (no upstream topology leaked).
- When both `agent_id` and `workdir` are provided, `agent_id` wins;
`agent_id`/`workdir` are stripped from the payload forwarded to FastClaw
and replaced with the resolved value.

Context: the Skills Store UI entry was hidden in #2569 because the
store's install flow was still keyed on legacy agent data. This PR lets
the upcoming frontend migration send `agent_id` from the V2
computer-agents model. Frontend slice follows in a separate PR.

# Test Plan

- [x] Unit tests (TDD, added in this PR):
- `tests/unit/test_clawhub_service.py` — main → no live-config fetch;
workdir-only legacy passthrough; non-main agent resolved from live
config; unresolved agent → 404 with stable code/detail
- `tests/unit/test_clawhub_routes.py` — list omits workdir for `main`;
install resolves agent workdir and forwards it; `agent_id` preferred
over `workdir`; unknown agent → product 404 on uninstall; pre-existing
route contract (ownership, running-bot, invalid bot id, upstream error
mapping) still covered
- [x] `ruff check` + `ruff format --check` (passed in the implementation
sandbox)
- [ ] `pytest` / `pyright` / `lint-imports` locally — **skipped: no
devcontainer available on this host**; relying on `python-code-quality /
build-and-test` CI as the authoritative gate
- [ ] Staging smoke after deploy: list/install/uninstall a skill against
a non-main agent via `agent_id`
```

### PR body

# Summary

Backend slice of the skill-store re-enable plan: the ClawHub skill endpoints now accept an `agent_id` and resolve the target workspace directory (`workdir`) on demand from FastClaw live config, so the frontend no longer needs to know workspace path conventions.

- `POST /bots/{bot_id}/clawhub/install`, `GET /bots/{bot_id}/clawhub`, and `POST /bots/{bot_id}/clawhub/uninstall` accept an optional `agent_id` (body field on mutations, query param on list).
- New service helper `app/services/openclaw/clawhub.py::resolve_clawhub_workdir`: `agent_id` absent → legacy `workdir` passthrough (backward compatible); `agent_id == "main"` → no workdir (FastClaw defaults to the main workspace); otherwise resolve via `get_bot` live config + the existing `build_workspace_by_agent_id` helper.
- Unresolvable agent → stable product-domain 404 `clawhub.agent_workspace_not_found` (no upstream topology leaked).
- When both `agent_id` and `workdir` are provided, `agent_id` wins; `agent_id`/`workdir` are stripped from the payload forwarded to FastClaw and replaced with the resolved value.

Context: the Skills Store UI entry was hidden in #2569 because the store's install flow was still keyed on legacy agent data. This PR lets the upcoming frontend migration send `agent_id` from the V2 computer-agents model. Frontend slice follows in a separate PR.

# Test Plan

- [x] Unit tests (TDD, added in this PR):
  - `tests/unit/test_clawhub_service.py` — main → no live-config fetch; workdir-only legacy passthrough; non-main agent resolved from live config; unresolved agent → 404 with stable code/detail
  - `tests/unit/test_clawhub_routes.py` — list omits workdir for `main`; install resolves agent workdir and forwards it; `agent_id` preferred over `workdir`; unknown agent → product 404 on uninstall; pre-existing route contract (ownership, running-bot, invalid bot id, upstream error mapping) still covered
- [x] `ruff check` + `ruff format --check` (passed in the implementation sandbox)
- [ ] `pytest` / `pyright` / `lint-imports` locally — **skipped: no devcontainer available on this host**; relying on `python-code-quality / build-and-test` CI as the authoritative gate
- [ ] Staging smoke after deploy: list/install/uninstall a skill against a non-main agent via `agent_id`



## fix(agent-builder): return version conflicts to builder (#2822)

- **sha**: `2294916920112f8909586839fe92d3b304a3746a`
- **author**: kaka-srp
- **date**: 2026-07-10T10:19:23Z

### Commit message

```
fix(agent-builder): return version conflicts to builder (#2822)

## Summary
- classify Agent Builder validation failures and duplicate Pack Test
versions as repairable preflight errors
- send repairable error summaries to the Builder thread, return the
project to `drafting`, and retain iteration diagnostics
- report repaired duplicate-version iterations as warnings in
operational diagnostics
- accept structured repairable error codes from `publish.py` when a
future Agent Studio release provides them

## Root cause
The Package & Test background handler only considered the exact code
`agent_builder.validation_failed` repairable. The duplicate-version
preflight introduced `agent_builder.pack_version_exists`, so its summary
was stored in the UI error fields without ever being posted to the Agent
Studio Builder thread. The project therefore remained `failed` even
though updating `agent/agent-pack.yaml` was a workspace-repairable
action.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pytest
services/claw-interface/tests/unit/test_agent_builder_service.py
services/claw-interface/tests/unit/test_agent_builder_diagnostics.py -q`
— 119 passed
- [x] pre-commit Python guards: ruff, format, pyright, complexity,
dependency consistency, import contracts, dead code

## Follow-up boundary
The reproduced issue is caught by claw-interface preflight and is fully
fixed here. A separate Agent Studio pack change would only be needed to
preserve the structured error code for the rare race where the version
becomes occupied after preflight but before the Pack Test create
request; that defensive follow-up is intentionally not required for this
PR.
```

### PR body

## Summary
- classify Agent Builder validation failures and duplicate Pack Test versions as repairable preflight errors
- send repairable error summaries to the Builder thread, return the project to `drafting`, and retain iteration diagnostics
- report repaired duplicate-version iterations as warnings in operational diagnostics
- accept structured repairable error codes from `publish.py` when a future Agent Studio release provides them

## Root cause
The Package & Test background handler only considered the exact code `agent_builder.validation_failed` repairable. The duplicate-version preflight introduced `agent_builder.pack_version_exists`, so its summary was stored in the UI error fields without ever being posted to the Agent Studio Builder thread. The project therefore remained `failed` even though updating `agent/agent-pack.yaml` was a workspace-repairable action.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pytest services/claw-interface/tests/unit/test_agent_builder_service.py services/claw-interface/tests/unit/test_agent_builder_diagnostics.py -q` — 119 passed
- [x] pre-commit Python guards: ruff, format, pyright, complexity, dependency consistency, import contracts, dead code

## Follow-up boundary
The reproduced issue is caught by claw-interface preflight and is fully fixed here. A separate Agent Studio pack change would only be needed to preserve the structured error code for the rare race where the version becomes occupied after preflight but before the Pack Test create request; that defensive follow-up is intentionally not required for this PR.



## fix(web): align chat status with usable transport (#2792)

- **sha**: `b6a98c196af22aa194e23a8f8ec963525e405c81`
- **author**: sharplee-srp
- **date**: 2026-07-10T09:43:47Z

### Commit message

```
fix(web): align chat status with usable transport (#2792)

## Summary
- Treat usable chat/MM transport as authoritative for the connection
pill so init phases do not override a working conversation.
- Use known computer IDs and FastClaw ready status to show
`Reconnecting...` instead of `Initializing...` while OpenClaw provider
hydration is still catching up.
- Keep shared chat gating semantics intact: composer-facing status still
treats init phases as non-connected, while only the pill display layer
suppresses misleading init text.
- Preserve explicit error/retry states when init fails or non-Mattermost
OpenClaw transport errors, even if FastClaw `/status` is still ready.
- Scope the “usable transport beats init lifecycle” override to
Mattermost chat routes; non-chat OpenClaw pages still show FastClaw
pending/restarting lifecycle states.
- Fix the missing initializing i18n key so raw `genClaw.*` keys do not
leak into the UI.

## Root cause
The pill mixed three different signals with the wrong priority: OpenClaw
init status, FastClaw platform readiness, and the interactive chat
transport. `oc.initStatus=loading/starting` could win even when the
backend computer was already ready or Mattermost chat was usable. The
header also did not pass the known current computer id into the pill, so
during page hydration the pill could not poll FastClaw status yet and
fell back to init loading. Separately, the label used
`genClaw.initializing`, but the locale key is
`genClaw.initializingClaw`.

Refs: https://linear.app/srpone/issue/ECA-1195

## Test plan
- [x] `pnpm exec vitest run
tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx
--config ./vitest.config.mts`
- [x] `pnpm exec vitest run
tests/unit/hooks/useStableConnectionStatus.unit.spec.ts --config
./vitest.config.mts`
- [x] `pnpm exec vitest run
tests/unit/components/ClawPageHeader.unit.spec.ts --config
./vitest.config.mts`
- [x] Added deterministic recorder regression coverage for
`oc.initStatus=loading` + OpenClaw WS disconnected +
Mattermost/interactive transport connected + FastClaw ready, asserting
the visible status stays `connected` and no degraded display episode
starts.
- [x] Added regressions for the review P1 cases: shared hook keeps init
phases gated, init errors keep the pill in `error` with retry, and
non-Mattermost OpenClaw WS errors are not masked by FastClaw ready.
- [x] Added regressions for non-Mattermost FastClaw pending/restarting
states and true cold-start `loading` with no computer id.
- [x] Added regression for preserved-bot init errors with FastClaw
`status=stopped`, keeping the pill in `error` with retry instead of
downgrading to plain disconnected.
- [x] Added regression for non-Mattermost pages with connected OpenClaw
transport while the first FastClaw `/status` poll is still pending,
preserving the old healthy first-poll behavior without hiding later
pending/restarting lifecycle states.
- [x] Added regression that shared composer status stays `connected` for
`initStatus=error` when WS/MM are still connected, while the pill
independently keeps showing `error`/retry from raw init state.
- [x] `bash scripts/verify-web.sh
web/app/src/components/ClawConnectionStatus.tsx
web/app/src/hooks/useOpenClawInit.ts
web/app/src/hooks/useStableConnectionStatus.ts
'web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx'
web/app/tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx
web/app/tests/unit/components/ClawPageHeader.unit.spec.ts
web/app/tests/unit/components/ClawPageHeader-extras.unit.spec.tsx
web/app/tests/unit/hooks/useStableConnectionStatus.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`
- [x] Devcontainer staging E2E against bot
`31b7ba01-5b22-4c7c-a3aa-45f0e4def472`: backend ready, agent `main` has
a Mattermost DM channel, page pill displayed `Reconnecting...` with no
raw `genClaw.*` and no initializing/starting/pending text. The run did
not observe a Mattermost websocket hello, so the real staging run
covered the backend-ready/chat-unavailable branch; connected transport
behavior is covered by deterministic unit tests.
```

### PR body

## Summary
- Treat usable chat/MM transport as authoritative for the connection pill so init phases do not override a working conversation.
- Use known computer IDs and FastClaw ready status to show `Reconnecting...` instead of `Initializing...` while OpenClaw provider hydration is still catching up.
- Keep shared chat gating semantics intact: composer-facing status still treats init phases as non-connected, while only the pill display layer suppresses misleading init text.
- Preserve explicit error/retry states when init fails or non-Mattermost OpenClaw transport errors, even if FastClaw `/status` is still ready.
- Scope the “usable transport beats init lifecycle” override to Mattermost chat routes; non-chat OpenClaw pages still show FastClaw pending/restarting lifecycle states.
- Fix the missing initializing i18n key so raw `genClaw.*` keys do not leak into the UI.

## Root cause
The pill mixed three different signals with the wrong priority: OpenClaw init status, FastClaw platform readiness, and the interactive chat transport. `oc.initStatus=loading/starting` could win even when the backend computer was already ready or Mattermost chat was usable. The header also did not pass the known current computer id into the pill, so during page hydration the pill could not poll FastClaw status yet and fell back to init loading. Separately, the label used `genClaw.initializing`, but the locale key is `genClaw.initializingClaw`.

Refs: https://linear.app/srpone/issue/ECA-1195

## Test plan
- [x] `pnpm exec vitest run tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx --config ./vitest.config.mts`
- [x] `pnpm exec vitest run tests/unit/hooks/useStableConnectionStatus.unit.spec.ts --config ./vitest.config.mts`
- [x] `pnpm exec vitest run tests/unit/components/ClawPageHeader.unit.spec.ts --config ./vitest.config.mts`
- [x] Added deterministic recorder regression coverage for `oc.initStatus=loading` + OpenClaw WS disconnected + Mattermost/interactive transport connected + FastClaw ready, asserting the visible status stays `connected` and no degraded display episode starts.
- [x] Added regressions for the review P1 cases: shared hook keeps init phases gated, init errors keep the pill in `error` with retry, and non-Mattermost OpenClaw WS errors are not masked by FastClaw ready.
- [x] Added regressions for non-Mattermost FastClaw pending/restarting states and true cold-start `loading` with no computer id.
- [x] Added regression for preserved-bot init errors with FastClaw `status=stopped`, keeping the pill in `error` with retry instead of downgrading to plain disconnected.
- [x] Added regression for non-Mattermost pages with connected OpenClaw transport while the first FastClaw `/status` poll is still pending, preserving the old healthy first-poll behavior without hiding later pending/restarting lifecycle states.
- [x] Added regression that shared composer status stays `connected` for `initStatus=error` when WS/MM are still connected, while the pill independently keeps showing `error`/retry from raw init state.
- [x] `bash scripts/verify-web.sh web/app/src/components/ClawConnectionStatus.tsx web/app/src/hooks/useOpenClawInit.ts web/app/src/hooks/useStableConnectionStatus.ts 'web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx' web/app/tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx web/app/tests/unit/components/ClawPageHeader.unit.spec.ts web/app/tests/unit/components/ClawPageHeader-extras.unit.spec.tsx web/app/tests/unit/hooks/useStableConnectionStatus.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`
- [x] Devcontainer staging E2E against bot `31b7ba01-5b22-4c7c-a3aa-45f0e4def472`: backend ready, agent `main` has a Mattermost DM channel, page pill displayed `Reconnecting...` with no raw `genClaw.*` and no initializing/starting/pending text. The run did not observe a Mattermost websocket hello, so the real staging run covered the backend-ready/chat-unavailable branch; connected transport behavior is covered by deterministic unit tests.



## fix(web): update IM channel quick start prompt (#2761)

- **sha**: `a7d26c12828e36f6858aa4b7ad042ef027494cee`
- **author**: rayrain-srp
- **date**: 2026-07-10T09:33:26Z

### Commit message

```
fix(web): update IM channel quick start prompt (#2761)

## Summary
- Update the built-in main-agent `connect-im` Quick Start prompt to send
users to ZooClaw `Settings > IM Channels` from the bottom-left avatar
menu.
- Keep the existing quick-command click behavior and localized label
behavior unchanged.
- Add regression coverage for the prompt contents and New Chat card
subtitle.

## Linear
- https://linear.app/srpone/issue/ECA-1179/

## Test Plan
- `bash -lc 'source ~/.nvm/nvm.sh && nvm use 24.16.0 >/dev/null && bash
scripts/verify-web.sh
web/app/src/app/'"'"'[locale]'"'"'/'"'"'(app)'"'"'/'"'"'(chat)'"'"'/chat/components/quick-commands.ts
web/app/tests/unit/app/chat/quick-commands.unit.spec.ts
web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx'`
- pre-push changed-surface gate: PR size budget, `verify-web.sh
--no-test` (`tsc`, full frontend lint, guards)

This is the ECA-1179 short-term prompt stopgap only. It does not add
quick-command navigation; a future fix can make this command open
`/claw-settings?tab=channels` directly.

---------

Co-authored-by: Developer <dev@srp.one>
```

### PR body

## Summary
- Update the built-in main-agent `connect-im` Quick Start prompt to send users to ZooClaw `Settings > IM Channels` from the bottom-left avatar menu.
- Keep the existing quick-command click behavior and localized label behavior unchanged.
- Add regression coverage for the prompt contents and New Chat card subtitle.

## Linear
- https://linear.app/srpone/issue/ECA-1179/

## Test Plan
- `bash -lc 'source ~/.nvm/nvm.sh && nvm use 24.16.0 >/dev/null && bash scripts/verify-web.sh web/app/src/app/'"'"'[locale]'"'"'/'"'"'(app)'"'"'/'"'"'(chat)'"'"'/chat/components/quick-commands.ts web/app/tests/unit/app/chat/quick-commands.unit.spec.ts web/app/tests/unit/app/new-chat/NewChatClient.unit.spec.tsx'`
- pre-push changed-surface gate: PR size budget, `verify-web.sh --no-test` (`tsc`, full frontend lint, guards)

This is the ECA-1179 short-term prompt stopgap only. It does not add quick-command navigation; a future fix can make this command open `/claw-settings?tab=channels` directly.



## fix(openclaw): align session reset settings with 6.11 (#2818)

- **sha**: `d6ba6fba31461e8d2de08daacfb803590f248378`
- **author**: tim-srp
- **date**: 2026-07-10T08:47:00Z

### Commit message

```
fix(openclaw): align session reset settings with 6.11 (#2818)

## Summary
- replace the legacy `off` contract with strict `disabled | daily |
idle` product modes mapped to valid OpenClaw 6.11 config
- replace the complete `session.reset` object while preserving unrelated
FastClaw config, with fail-closed reads and same-process per-bot
serialization
- convert daily reset hours between the user's configured IANA timezone
and UTC, and update the settings UI, API types, cache logic, and tests

## Root cause
The existing frontend and backend persisted `session.reset.mode =
"off"`, but OpenClaw 6.11 accepts only `daily` or `idle`. FastClaw's
deep-merge update also cannot remove stale `idleMinutes` or `atHour`
fields when switching modes, so the reset object must be replaced
canonically.

## Rollout preconditions
- this is a coordinated cutover: claw-interface and the settings
frontend must be deployed together
- all OpenClaw pods must be upgraded to 6.11
- persisted `mode: "off"` values in FastClaw and Kubernetes ConfigMaps
must be migrated to canonical 6.11 reset objects before cutover
- old request payloads and legacy `off` reads are intentionally
unsupported after cutover, as required by the approved design

## Test plan
- [x] `pytest tests/unit/test_openclaw_session_reset.py
tests/unit/test_openclaw_settings_routes.py -q` (305 passed)
- [x] pyright on all touched backend modules and tests (0 errors)
- [x] `pnpm --dir web test` (734 files, 8615 passed, 1 skipped, 1 todo)
- [x] `pnpm exec tsc --noEmit` in `web/app`
- [x] `pnpm --dir web lint` (0 errors; 22 pre-existing enterprise-app
warnings)
- [x] Python pre-commit ruff, formatting, import contracts, dependency
checks, and pyright hooks
- [x] GitHub backend tests, backend lint/typecheck, Web tests, Web
lint/typecheck, Web build, CodeQL, and duplication checks

## Known constraints
- OpenClaw 6.11 stores only an integer `atHour`; 30- and 45-minute
UTC-offset timezones cannot preserve the selected local hour exactly,
and future DST offset changes require recalculation.
- FastClaw has no config version or conditional update API. Same-process
updates are serialized, but concurrent full replacements across
claw-interface replicas still have a race window.
```

### PR body

## Summary
- replace the legacy `off` contract with strict `disabled | daily | idle` product modes mapped to valid OpenClaw 6.11 config
- replace the complete `session.reset` object while preserving unrelated FastClaw config, with fail-closed reads and same-process per-bot serialization
- convert daily reset hours between the user's configured IANA timezone and UTC, and update the settings UI, API types, cache logic, and tests

## Root cause
The existing frontend and backend persisted `session.reset.mode = "off"`, but OpenClaw 6.11 accepts only `daily` or `idle`. FastClaw's deep-merge update also cannot remove stale `idleMinutes` or `atHour` fields when switching modes, so the reset object must be replaced canonically.

## Rollout preconditions
- this is a coordinated cutover: claw-interface and the settings frontend must be deployed together
- all OpenClaw pods must be upgraded to 6.11
- persisted `mode: "off"` values in FastClaw and Kubernetes ConfigMaps must be migrated to canonical 6.11 reset objects before cutover
- old request payloads and legacy `off` reads are intentionally unsupported after cutover, as required by the approved design

## Test plan
- [x] `pytest tests/unit/test_openclaw_session_reset.py tests/unit/test_openclaw_settings_routes.py -q` (305 passed)
- [x] pyright on all touched backend modules and tests (0 errors)
- [x] `pnpm --dir web test` (734 files, 8615 passed, 1 skipped, 1 todo)
- [x] `pnpm exec tsc --noEmit` in `web/app`
- [x] `pnpm --dir web lint` (0 errors; 22 pre-existing enterprise-app warnings)
- [x] Python pre-commit ruff, formatting, import contracts, dependency checks, and pyright hooks
- [x] GitHub backend tests, backend lint/typecheck, Web tests, Web lint/typecheck, Web build, CodeQL, and duplication checks

## Known constraints
- OpenClaw 6.11 stores only an integer `atHour`; 30- and 45-minute UTC-offset timezones cannot preserve the selected local hour exactly, and future DST offset changes require recalculation.
- FastClaw has no config version or conditional update API. Same-process updates are serialized, but concurrent full replacements across claw-interface replicas still have a race window.


## feat(dashboard-console): sell catalog plans from the offline-order create dialog (#2811)

- **sha**: `0a5104b755a3059878eb01f84ba310c667d96478`
- **author**: bill-srp
- **date**: 2026-07-10T06:58:20Z

### Commit message

```
feat(dashboard-console): sell catalog plans from the offline-order create dialog (#2811)

## Linear
<!-- 无对应 Linear issue；如需追溯可补充 -->

## Summary

Frontend half of the offline-order plan-purchase feature (split from
#2809; backend service PR #2810 must merge/deploy first). The
offline-order create picker previously listed only vertical-pack
packages the uid already owns, so a never-purchased user couldn't be
sold to offline. Now the picker also lists the plan catalog, and picking
a plan drives the backend's new first-purchase provisioning path.

Design spec + implementation plan ship in the backend PR
(`docs/superpowers/specs/2026-07-09-offline-order-plan-purchase-design.md`).

- Create-dialog picker gains two optgroups: **Owned packages** (existing
flow, values `pkg:<id>`) and **Plans (new purchase)** (values
`plan:<id>`); "Load packages" now fetches owned packages and the
non-deleted plan catalog in parallel.
- Selecting a plan pre-fills the amount from the plan price (admin can
overwrite — negotiated pricing stays representable).
- `org_ambiguous` create errors reveal an inline org selector (fed by
the new `GET /internal/users/{uid}/orgs` lookup) and resubmit with
`org_id`; `no_org` / `plan_not_found` / `org_membership_invalid` map to
actionable messages via `friendlyCreateErrorMessage`.
- `CreateOfflineOrderInput` is now a `package_id` xor `plan_id` union;
picker values parse via the pure `parsePickerValue` helper; new
`listUserOrgs` client + `userOrgsUrl` builder.

**Dependency / rollout:** consumes the backend's extended create
contract and orgs lookup — release ordering is `service-v*-release`
**before** `dashboard-console-v*-release` (same as #2801/#2802). Until
the backend deploys, plan selections would 422 on the old schema; the
owned-package path is unaffected.

## Test plan
- [x] 314 vitest tests pass on this branch standalone, including new
coverage: grouped picker rendering, plan payload (`plan_id`, no
`package_id`), amount prefill, org-disambiguation branch (selector
appears, resubmit carries `org_id`, hidden for package selections),
error-code mapping, packages+plans parallel load with deleted-plan
filtering
- [x] `pnpm typecheck` + `pnpm lint` clean
- [ ] Staging smoke (post-deploy, after the service release): plan-path
create → confirm with a fresh single-org uid (confirm grants real
staging credits — user-driven)
```

### PR body

## Linear
<!-- 无对应 Linear issue；如需追溯可补充 -->

## Summary

Frontend half of the offline-order plan-purchase feature (split from #2809; backend service PR #2810 must merge/deploy first). The offline-order create picker previously listed only vertical-pack packages the uid already owns, so a never-purchased user couldn't be sold to offline. Now the picker also lists the plan catalog, and picking a plan drives the backend's new first-purchase provisioning path.

Design spec + implementation plan ship in the backend PR (`docs/superpowers/specs/2026-07-09-offline-order-plan-purchase-design.md`).

- Create-dialog picker gains two optgroups: **Owned packages** (existing flow, values `pkg:<id>`) and **Plans (new purchase)** (values `plan:<id>`); "Load packages" now fetches owned packages and the non-deleted plan catalog in parallel.
- Selecting a plan pre-fills the amount from the plan price (admin can overwrite — negotiated pricing stays representable).
- `org_ambiguous` create errors reveal an inline org selector (fed by the new `GET /internal/users/{uid}/orgs` lookup) and resubmit with `org_id`; `no_org` / `plan_not_found` / `org_membership_invalid` map to actionable messages via `friendlyCreateErrorMessage`.
- `CreateOfflineOrderInput` is now a `package_id` xor `plan_id` union; picker values parse via the pure `parsePickerValue` helper; new `listUserOrgs` client + `userOrgsUrl` builder.

**Dependency / rollout:** consumes the backend's extended create contract and orgs lookup — release ordering is `service-v*-release` **before** `dashboard-console-v*-release` (same as #2801/#2802). Until the backend deploys, plan selections would 422 on the old schema; the owned-package path is unaffected.

## Test plan
- [x] 314 vitest tests pass on this branch standalone, including new coverage: grouped picker rendering, plan payload (`plan_id`, no `package_id`), amount prefill, org-disambiguation branch (selector appears, resubmit carries `org_id`, hidden for package selections), error-code mapping, packages+plans parallel load with deleted-plan filtering
- [x] `pnpm typecheck` + `pnpm lint` clean
- [ ] Staging smoke (post-deploy, after the service release): plan-path create → confirm with a fresh single-org uid (confirm grants real staging credits — user-driven)



## feat(dashboard-console): add users admin page (read surface) (#2815)

- **sha**: `f2680f1fe1d2fe4cafa8d597599e10fdee4c9528`
- **author**: bill-srp
- **date**: 2026-07-10T06:39:36Z

### Commit message

```
feat(dashboard-console): add users admin page (read surface) (#2815)

# Purpose

Plan 4c-reads of the staff-admin relocation ([design
spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)):
the **Users** console page, read surface — the third and largest admin
page, split so mutations review separately. Sits on the
`/internal/users` read endpoints (#2781) and follows the page pattern
from #2807/#2813.

# Approach

- **`/users` page** (`routes/users/`, AdminOnly-gated): the legacy
`UsersTab`'s six filters (user type, UID, email partial, phone partial,
subscription status incl. the `trial,active,past_due` combo preset,
created-before date → unix), 50-per-page pagination with
`keepPreviousData` (no table blanking on page flips, matching legacy),
user table (UID mono, profile stack, plan badge, status, sub-end,
created/updated, row actions Orders / Events).
- **Order history dialog** — `GET /{uid}/orders` (latest 20, caption
when more exist); legacy label maps ported to English (product type,
channel, status tones; "Free" for admin grants / daily bonuses / trials;
`amount/100` + currency).
- **Customer events dialog** — `GET /{uid}/events`; 24h / 7d / 30d /
custom range presets, Lago usage table (code, model,
prompt/completion/total tokens, cost), pager driven by
`meta.prev_page`/`next_page`, empty-envelope handling for users without
a billing customer.
- **Fetchers** `listAdminUsers` / `listUserOrders` / `listUserEvents`
reuse the existing `INTERNAL_USERS_PATH`; subset types (extra wire
fields ignored, per app convention).
- **Deliberately NOT in this PR** (4c-mutations, next): Grant Credits
dialog + credits panel, Boost dialog, batch grant, row checkboxes + bulk
bar (they exist solely to feed batch grant), and the
stable-idempotency-key generation the new mutation endpoints require.
Zero mutation code here — pure GETs, so no in-flight locks needed.

# Tests

- [x] 50 files / 375 tests green (10 new test files): URL builder;
fetcher contracts (only-set filters in query string, uid URI-encoding,
range params omitted when absent, `ApiError`); query hooks
(enabled-gating on null uid, param passthrough); view-model (filter trim
+ date→unix conversion + empty-dropping + offset reset, prev clamp,
dialog open/close); both dialogs (closed → no render/fetch, label maps,
preset refetch, pager bounds); route (rows, non-admin gate, filter
commit → query params, dialog opening, pagination)
- [x] `pnpm lint`, `pnpm typecheck`, `pnpm test` — all green (what
`dashboard-quality` runs)

# Notes

- Implementation plan:
`docs/superpowers/plans/2026-07-10-console-users-reads.md`
- Adaptation: order-status column uses `StatusPill` with explicit tones
(`StatusBadge` derives tone from a fixed lifecycle map and takes no tone
prop).
- Next: 4c-mutations (grant/boost dialogs with required stable
`idempotency_key` per #2783/#2788 — legacy sent `admin_uid` and no key;
the new backend ignores body `admin_uid` and 422s without a key), then
Plan 5 teardown.
```

### PR body

# Purpose

Plan 4c-reads of the staff-admin relocation ([design spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)): the **Users** console page, read surface — the third and largest admin page, split so mutations review separately. Sits on the `/internal/users` read endpoints (#2781) and follows the page pattern from #2807/#2813.

# Approach

- **`/users` page** (`routes/users/`, AdminOnly-gated): the legacy `UsersTab`'s six filters (user type, UID, email partial, phone partial, subscription status incl. the `trial,active,past_due` combo preset, created-before date → unix), 50-per-page pagination with `keepPreviousData` (no table blanking on page flips, matching legacy), user table (UID mono, profile stack, plan badge, status, sub-end, created/updated, row actions Orders / Events).
- **Order history dialog** — `GET /{uid}/orders` (latest 20, caption when more exist); legacy label maps ported to English (product type, channel, status tones; "Free" for admin grants / daily bonuses / trials; `amount/100` + currency).
- **Customer events dialog** — `GET /{uid}/events`; 24h / 7d / 30d / custom range presets, Lago usage table (code, model, prompt/completion/total tokens, cost), pager driven by `meta.prev_page`/`next_page`, empty-envelope handling for users without a billing customer.
- **Fetchers** `listAdminUsers` / `listUserOrders` / `listUserEvents` reuse the existing `INTERNAL_USERS_PATH`; subset types (extra wire fields ignored, per app convention).
- **Deliberately NOT in this PR** (4c-mutations, next): Grant Credits dialog + credits panel, Boost dialog, batch grant, row checkboxes + bulk bar (they exist solely to feed batch grant), and the stable-idempotency-key generation the new mutation endpoints require. Zero mutation code here — pure GETs, so no in-flight locks needed.

# Tests

- [x] 50 files / 375 tests green (10 new test files): URL builder; fetcher contracts (only-set filters in query string, uid URI-encoding, range params omitted when absent, `ApiError`); query hooks (enabled-gating on null uid, param passthrough); view-model (filter trim + date→unix conversion + empty-dropping + offset reset, prev clamp, dialog open/close); both dialogs (closed → no render/fetch, label maps, preset refetch, pager bounds); route (rows, non-admin gate, filter commit → query params, dialog opening, pagination)
- [x] `pnpm lint`, `pnpm typecheck`, `pnpm test` — all green (what `dashboard-quality` runs)

# Notes

- Implementation plan: `docs/superpowers/plans/2026-07-10-console-users-reads.md`
- Adaptation: order-status column uses `StatusPill` with explicit tones (`StatusBadge` derives tone from a fixed lifecycle map and takes no tone prop).
- Next: 4c-mutations (grant/boost dialogs with required stable `idempotency_key` per #2783/#2788 — legacy sent `admin_uid` and no key; the new backend ignores body `admin_uid` and 422s without a key), then Plan 5 teardown.



## feat(web): render agent interactive cards in webapp chat (#2816)

- **sha**: `dabe11c55c1e9dce5acab2610dc3ff542c2b3a03`
- **author**: bill-srp
- **date**: 2026-07-10T06:34:12Z

### Commit message

```
feat(web): render agent interactive cards in webapp chat (#2816)

## Summary

Renders agent-sent **interactive cards** (action buttons, confirm
presets, single-select dropdowns) natively in the webapp chat.

The agent emits cards via the `message` tool `card` param
(zooclaw-extras
[#171](https://github.com/SerendipityOneInc/zooclaw-extras/pull/171)
`@zooclaw/card-kit` +
[#169](https://github.com/SerendipityOneInc/zooclaw-extras/pull/169)
`@zooclaw/mattermost`). The Mattermost plugin renders them as native
interactive attachments (`props.attachments`, HMAC-signed actions). The
webapp is a Mattermost client on the same server but ignored those
attachments — cards were invisible in the webapp while working in the
native MM client.

**Click path is the native Mattermost round-trip:** the webapp calls
`POST /api/v4/posts/{post_id}/actions/{action_id}` (with
`selected_option` for selects); the MM server invokes the plugin's
HMAC-verified webhook; the plugin dispatches the canonical value to the
agent and edits the post into a completion banner, which re-renders over
the existing `post_edited` WebSocket path. **No backend or plugin
changes.**

## What's in this PR

- `src/lib/mattermost/interactive-attachments.ts` — pure parser
recognizing exactly the three PR #169 wire shapes (button row, single
select, text-only completion banner); everything else ignored by design
- `MattermostAPIService.doPostAction(postId, actionId, selectedOption?)`
— native post-action execution
- Pipeline: `OpenClawMessage.interactiveCards` populated in
`mmDisplayMessages`, survives `filterMessages` (card-only posts stay
visible), exposed via runtime `metadata.custom`
- `InteractiveCards` chat component — shadcn semantic tokens,
pending/disabled state during dispatch, failure toast + re-enable,
read-only disable guard, immediate-dispatch select (no submit button)
- Compact chat variant (subagent panel) renders cards too — card-only
posts don't degrade to an empty bubble
- Wired into `OpenClawAssistantMessage` (normal + tool-group branches,
emptiness guard)
- Design spec + implementation plan docs

Design decisions (from spec): card-kit shapes only (not generic MM
attachment rendering); new self-contained module rather than reusing the
ERMP renderer (ERMP clicks are `[ACTION:…]` text-postbacks; these are MM
post actions — same look via shared tokens, different wire protocol).

## Dependencies / sequencing

Independently shippable: until zooclaw-extras #171 + #169 merge,
publish, and deploy, the parser simply finds no card-shaped attachments
and nothing changes. End-to-end behavior activates once the plugin
ships.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (7,556
passed) + eslint, all green
- [x] Unit: parser (8 tests, fixtures copied from plugin wire output),
`doPostAction` request shape (3), pipeline surfacing + card-only
visibility + `propsEqual` attachments-edit guard, `InteractiveCards`
component states (6), assistant-message wiring (2)
- [ ] Live staging validation after zooclaw-extras #171/#169 deploy:
send actions/confirm/select from a real agent, click each in the webapp,
verify canonical value reaches the agent and the completion banner
replaces the card (doubles as #169's pending live-select verification)

## Known limitation — replay

Shared-replay snapshots don't carry `props.attachments` (the backend
replay pipeline only copies `ermp_cards` etc., and backend changes are
explicitly out of scope per the spec), so interactive cards are
**omitted from replays** rather than shown disabled. The component's
`useIsReplayReadOnly()` guard is defensive for any future read-only
Mattermost-backed surface. Copying `attachments` through `chat_replay`
is a possible backend follow-up.

## Docs

- Spec:
`docs/superpowers/specs/2026-07-10-webapp-interactive-cards-design.md`
- Plan: `docs/superpowers/plans/2026-07-10-webapp-interactive-cards.md`

No Linear issue exists for this feature (requested directly in session).
```

### PR body

## Summary

Renders agent-sent **interactive cards** (action buttons, confirm presets, single-select dropdowns) natively in the webapp chat.

The agent emits cards via the `message` tool `card` param (zooclaw-extras [#171](https://github.com/SerendipityOneInc/zooclaw-extras/pull/171) `@zooclaw/card-kit` + [#169](https://github.com/SerendipityOneInc/zooclaw-extras/pull/169) `@zooclaw/mattermost`). The Mattermost plugin renders them as native interactive attachments (`props.attachments`, HMAC-signed actions). The webapp is a Mattermost client on the same server but ignored those attachments — cards were invisible in the webapp while working in the native MM client.

**Click path is the native Mattermost round-trip:** the webapp calls `POST /api/v4/posts/{post_id}/actions/{action_id}` (with `selected_option` for selects); the MM server invokes the plugin's HMAC-verified webhook; the plugin dispatches the canonical value to the agent and edits the post into a completion banner, which re-renders over the existing `post_edited` WebSocket path. **No backend or plugin changes.**

## What's in this PR

- `src/lib/mattermost/interactive-attachments.ts` — pure parser recognizing exactly the three PR #169 wire shapes (button row, single select, text-only completion banner); everything else ignored by design
- `MattermostAPIService.doPostAction(postId, actionId, selectedOption?)` — native post-action execution
- Pipeline: `OpenClawMessage.interactiveCards` populated in `mmDisplayMessages`, survives `filterMessages` (card-only posts stay visible), exposed via runtime `metadata.custom`
- `InteractiveCards` chat component — shadcn semantic tokens, pending/disabled state during dispatch, failure toast + re-enable, read-only disable guard, immediate-dispatch select (no submit button)
- Compact chat variant (subagent panel) renders cards too — card-only posts don't degrade to an empty bubble
- Wired into `OpenClawAssistantMessage` (normal + tool-group branches, emptiness guard)
- Design spec + implementation plan docs

Design decisions (from spec): card-kit shapes only (not generic MM attachment rendering); new self-contained module rather than reusing the ERMP renderer (ERMP clicks are `[ACTION:…]` text-postbacks; these are MM post actions — same look via shared tokens, different wire protocol).

## Dependencies / sequencing

Independently shippable: until zooclaw-extras #171 + #169 merge, publish, and deploy, the parser simply finds no card-shaped attachments and nothing changes. End-to-end behavior activates once the plugin ships.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (7,556 passed) + eslint, all green
- [x] Unit: parser (8 tests, fixtures copied from plugin wire output), `doPostAction` request shape (3), pipeline surfacing + card-only visibility + `propsEqual` attachments-edit guard, `InteractiveCards` component states (6), assistant-message wiring (2)
- [ ] Live staging validation after zooclaw-extras #171/#169 deploy: send actions/confirm/select from a real agent, click each in the webapp, verify canonical value reaches the agent and the completion banner replaces the card (doubles as #169's pending live-select verification)

## Known limitation — replay

Shared-replay snapshots don't carry `props.attachments` (the backend replay pipeline only copies `ermp_cards` etc., and backend changes are explicitly out of scope per the spec), so interactive cards are **omitted from replays** rather than shown disabled. The component's `useIsReplayReadOnly()` guard is defensive for any future read-only Mattermost-backed surface. Copying `attachments` through `chat_replay` is a possible backend follow-up.

## Docs

- Spec: `docs/superpowers/specs/2026-07-10-webapp-interactive-cards-design.md`
- Plan: `docs/superpowers/plans/2026-07-10-webapp-interactive-cards.md`

No Linear issue exists for this feature (requested directly in session).



## fix(ci): pin iOS release notes model (#2817)

- **sha**: `51151ca451f7c6d6daa89affdca0e3c9bf325f65`
- **author**: bill-srp
- **date**: 2026-07-10T06:01:48Z

### Commit message

```
fix(ci): pin iOS release notes model (#2817)

## Summary

- pin the iOS App Store release-notes Codex model to `gpt-5.5`
- avoid inheriting newer Codex CLI defaults that are not deployed on the
configured Azure OpenAI resource

## Context

The iOS 1.8.1 release workflow inherited the Codex CLI default
`gpt-5.6-sol` and failed with an Azure deployment 404. The preceding
successful iOS release used `gpt-5.5`.

## Validation

- `ruby -e 'require "yaml"; YAML.load_file(ARGV[0]); puts "yaml-ok"'
.github/workflows/ios-deploy.yml`
- `git diff --check`
- `bash scripts/verify-changed.sh` (no locally verifiable surfaces for
this workflow-only change)
```

### PR body

## Summary

- pin the iOS App Store release-notes Codex model to `gpt-5.5`
- avoid inheriting newer Codex CLI defaults that are not deployed on the configured Azure OpenAI resource

## Context

The iOS 1.8.1 release workflow inherited the Codex CLI default `gpt-5.6-sol` and failed with an Azure deployment 404. The preceding successful iOS release used `gpt-5.5`.

## Validation

- `ruby -e 'require "yaml"; YAML.load_file(ARGV[0]); puts "yaml-ok"' .github/workflows/ios-deploy.yml`
- `git diff --check`
- `bash scripts/verify-changed.sh` (no locally verifiable surfaces for this workflow-only change)



## feat(billing): create offline orders from catalog plans (#2810)

- **sha**: `32d95e5ec21365bf4e56ed07b0d5bf0556663e7b`
- **author**: bill-srp
- **date**: 2026-07-10T05:54:00Z

### Commit message

```
feat(billing): create offline orders from catalog plans (#2810)

## Linear
<!-- 无对应 Linear issue；如需追溯可补充 -->

## Summary

Backend half of the offline-order plan-purchase feature (split from
#2809; frontend console PR: #2811). Lets admins record a user's
**first** offline enterprise payment: `create_offline_order` now accepts
a catalog **plan** and provisions the vertical-pack package as part of
order creation, mirroring the online `purchase_plan` semantics (draft
package before payment) minus Stripe checkout.

Design spec:
`docs/superpowers/specs/2026-07-09-offline-order-plan-purchase-design.md`
· Implementation plan:
`docs/superpowers/plans/2026-07-09-offline-order-plan-purchase.md` (both
included here).

- `POST /internal/offline-order/create` accepts exactly one of
`package_id` / `plan_id` (+ optional `org_id`, only with `plan_id`);
schema-level `model_validator` plus service-level `_validate_target`
enforce the contract. The existing `package_id` path is unchanged.
- New `offline_order_plan_purchase.py`: plan lookup, org resolution
(auto-bind single active org; distinct `no_org` / `org_ambiguous` /
`org_membership_invalid` error codes — multi-org is Phase-2
forward-compat), draft-package provisioning with the plan's
price/credits/agents, no add-ons (per spec).
- Conflict checks (active offline agreement, pending order) run
**before** any package insert; any create failure after provisioning
best-effort soft-deletes the draft (both the duplicate-pending-order and
agreement-failure paths). A best-effort
`offline_order.created_from_plan` audit event records plan provenance
without being able to fail the committed order.
- `create_offline_order` moved verbatim to `offline_order_creation.py` —
`offline_orders.py` was at the 500-line CI cap; follows the
`offline_order_cancellations.py` precedent, re-exported so route callers
are unchanged.
- New admin lookup `GET /internal/users/{uid}/orgs` (active memberships
+ org names, for the console's org disambiguation) backed by new
`account_org_repo.list_active_by_uid`.

**Consumer:** the dashboard-console picker PR consumes the new create
contract and orgs lookup — merge/release this PR first
(`service-v*-release` before `dashboard-console-v*-release`, same
ordering as #2801/#2802).

## Test plan
- [x] 116 focused unit tests pass (`test_offline_orders_service` /
`test_offline_orders_routes` / `test_offline_order_plan_purchase` /
`test_internal_users_orgs` / `test_account_org_repo_list_active`),
including the org matrix (0/1/n orgs, explicit org
valid/inactive/missing-doc), conflict-before-provision ordering, draft
cleanup on both create-failure paths, request-shape rejections, and
audit best-effort behavior
- [x] Existing offline-order suite passes with the module move (patch
targets migrated to `offline_order_creation`)
- [x] ruff + ruff-format + pyright (`app/ tests/`) + import-linter (8
contracts kept) via `scripts/verify-changed.sh`
- [ ] Staging smoke (post-deploy, with the console PR): plan-path create
→ confirm with a fresh single-org uid (confirm grants real staging
credits — user-driven)
```

### PR body

## Linear
<!-- 无对应 Linear issue；如需追溯可补充 -->

## Summary

Backend half of the offline-order plan-purchase feature (split from #2809; frontend console PR: #2811). Lets admins record a user's **first** offline enterprise payment: `create_offline_order` now accepts a catalog **plan** and provisions the vertical-pack package as part of order creation, mirroring the online `purchase_plan` semantics (draft package before payment) minus Stripe checkout.

Design spec: `docs/superpowers/specs/2026-07-09-offline-order-plan-purchase-design.md` · Implementation plan: `docs/superpowers/plans/2026-07-09-offline-order-plan-purchase.md` (both included here).

- `POST /internal/offline-order/create` accepts exactly one of `package_id` / `plan_id` (+ optional `org_id`, only with `plan_id`); schema-level `model_validator` plus service-level `_validate_target` enforce the contract. The existing `package_id` path is unchanged.
- New `offline_order_plan_purchase.py`: plan lookup, org resolution (auto-bind single active org; distinct `no_org` / `org_ambiguous` / `org_membership_invalid` error codes — multi-org is Phase-2 forward-compat), draft-package provisioning with the plan's price/credits/agents, no add-ons (per spec).
- Conflict checks (active offline agreement, pending order) run **before** any package insert; any create failure after provisioning best-effort soft-deletes the draft (both the duplicate-pending-order and agreement-failure paths). A best-effort `offline_order.created_from_plan` audit event records plan provenance without being able to fail the committed order.
- `create_offline_order` moved verbatim to `offline_order_creation.py` — `offline_orders.py` was at the 500-line CI cap; follows the `offline_order_cancellations.py` precedent, re-exported so route callers are unchanged.
- New admin lookup `GET /internal/users/{uid}/orgs` (active memberships + org names, for the console's org disambiguation) backed by new `account_org_repo.list_active_by_uid`.

**Consumer:** the dashboard-console picker PR consumes the new create contract and orgs lookup — merge/release this PR first (`service-v*-release` before `dashboard-console-v*-release`, same ordering as #2801/#2802).

## Test plan
- [x] 116 focused unit tests pass (`test_offline_orders_service` / `test_offline_orders_routes` / `test_offline_order_plan_purchase` / `test_internal_users_orgs` / `test_account_org_repo_list_active`), including the org matrix (0/1/n orgs, explicit org valid/inactive/missing-doc), conflict-before-provision ordering, draft cleanup on both create-failure paths, request-shape rejections, and audit best-effort behavior
- [x] Existing offline-order suite passes with the module move (patch targets migrated to `offline_order_creation`)
- [x] ruff + ruff-format + pyright (`app/ tests/`) + import-linter (8 contracts kept) via `scripts/verify-changed.sh`
- [ ] Staging smoke (post-deploy, with the console PR): plan-path create → confirm with a fresh single-org uid (confirm grants real staging credits — user-driven)



## fix(agent-builder): publish submitted pack avatars (#2814)

- **sha**: `0616fdf4f68a952edee3545f98a3a0306077341e`
- **author**: kaka-srp
- **date**: 2026-07-10T03:28:19Z

### Commit message

```
fix(agent-builder): publish submitted pack avatars (#2814)

## Summary
- Publish Agent Builder-submitted pack avatars when listing metadata
references `artifacts/avatar.png` inside the pack archive.
- Add deterministic public R2 avatar uploads and server-side R2 object
reads for backend-owned archives.
- Validate avatar size/type and reject missing or duplicate archive
avatar entries.

## Root cause
Agent Studio writes `avatar_url: "artifacts/avatar.png"` into listing
metadata and packages the image inside the archive. The Agent Builder
submit path only accepted `http(s)` avatar URLs, so the relative path
was filtered to `None` and Pack Store submissions were created without a
valid avatar.

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] `pytest
services/claw-interface/tests/unit/test_agent_builder_service.py
services/claw-interface/tests/unit/test_r2_storage.py`

Linear:
https://linear.app/srpone/issue/ECA-1205/investigate-missing-agent-pack-avatar
```

### PR body

## Summary
- Publish Agent Builder-submitted pack avatars when listing metadata references `artifacts/avatar.png` inside the pack archive.
- Add deterministic public R2 avatar uploads and server-side R2 object reads for backend-owned archives.
- Validate avatar size/type and reject missing or duplicate archive avatar entries.

## Root cause
Agent Studio writes `avatar_url: "artifacts/avatar.png"` into listing metadata and packages the image inside the archive. The Agent Builder submit path only accepted `http(s)` avatar URLs, so the relative path was filtered to `None` and Pack Store submissions were created without a valid avatar.

## Test plan
- [x] `bash scripts/verify-py.sh`
- [x] `pytest services/claw-interface/tests/unit/test_agent_builder_service.py services/claw-interface/tests/unit/test_r2_storage.py`

Linear: https://linear.app/srpone/issue/ECA-1205/investigate-missing-agent-pack-avatar



## feat(dashboard-console): add releases admin page (#2813)

- **sha**: `2f3cb7907fced9b84bb31fbfd8af28b9de21d501`
- **author**: bill-srp
- **date**: 2026-07-10T02:51:01Z

### Commit message

```
feat(dashboard-console): add releases admin page (#2813)

# Purpose

Plan 4b of the staff-admin relocation ([design
spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)):
the second admin page in `web/dashboard-console` — **Releases**
(`/releases`), replacing the web/app admin tab. Sits on the
`/internal/releases` endpoints (#2774) and follows the page pattern
established by the subscription-codes page (#2807).

# Approach

- **Page** (`routes/releases/`): `route.tsx` wrapped in `AdminOnly`,
`use-releases-query.ts` (newest-first list; backend caps 50 — no
pagination, matching legacy), `use-view-model.ts` (create form + row
actions).
- **Features (faithful port of the legacy `ReleasesTab`)**: inline
create (version — "matches the image tag, no v prefix" — plus optional
notification message + release notes); table with Latest / Published /
Draft badges; row actions: Set latest (hidden on the current latest),
Publish/Unpublish toggle, Delete.
- **Wire-shape shift handled**: the legacy BFF used HTTP `DELETE
/openclaw/admin/releases/{version}`; the new backend is GET/POST-only —
all mutations go through `POST
/internal/releases/{version}/{delete|set-latest|publish|unpublish}`
(`releaseAction` fetcher, version URI-encoded), consuming `{ok,
version}`.
- **Documented deltas from legacy**: English copy; **delete now requires
a confirmation dialog** (legacy fired destructive deletes with zero
confirmation); **sync `useRef` in-flight locks on create and row
actions** (the double-submit class Codex flagged on #2807, baked in from
the start); full date+time formatting (`created_at` is an ISO string —
local `formatIsoDateTime`, not the unix-based `formatUnixDate`).
- **Discoverability, admin-gated**: Releases entry in the Administration
sidebar group, `PAGE_TITLE`, second admin home `EntryCard` — all behind
`useIsAdmin()`; backend independently enforces `require_srp_account` +
`require_admin_user`.

# Tests

- [x] 45 files / 341 tests green (6 new/extended test files): URL
builder; fetchers (list `{releases}` unwrap, create body, action path
URI-encoding via a `"1.2/3"` version, POST-only, `ApiError`); query
hook; view-model (create+action locks via double synchronous invocation,
empty-version guard, payload omits empty optionals, failure surfaces +
keeps fields, confirm-delete flow — `requestDelete` never calls the API,
only `confirmDelete` does); route (badges incl. conditional Set-latest,
non-admin gate, publish call, delete dialog flow, create payload)
- [x] `pnpm lint`, `pnpm typecheck` (typegen picks up the new route),
`pnpm test` — all green (what `dashboard-quality` runs)

# Notes

- Implementation plan:
`docs/superpowers/plans/2026-07-09-console-releases-page.md`
- Known backend caveat (out of scope, tracked): no unique index on
`version` (create TOCTOU) + non-transactional `is_latest` singleton —
the release_repo hardening follow-up from #2774. The UI surfaces the 409
`release.already_exists` for the common case.
- Next: Plan 4c Users page (grant/boost modals with stable idempotency
keys per #2783/#2788), then Plan 5 web/app `/admin` teardown.
```

### PR body

# Purpose

Plan 4b of the staff-admin relocation ([design spec](../blob/main/docs/superpowers/specs/2026-07-08-relocate-staff-admin-to-dashboard-console-design.md)): the second admin page in `web/dashboard-console` — **Releases** (`/releases`), replacing the web/app admin tab. Sits on the `/internal/releases` endpoints (#2774) and follows the page pattern established by the subscription-codes page (#2807).

# Approach

- **Page** (`routes/releases/`): `route.tsx` wrapped in `AdminOnly`, `use-releases-query.ts` (newest-first list; backend caps 50 — no pagination, matching legacy), `use-view-model.ts` (create form + row actions).
- **Features (faithful port of the legacy `ReleasesTab`)**: inline create (version — "matches the image tag, no v prefix" — plus optional notification message + release notes); table with Latest / Published / Draft badges; row actions: Set latest (hidden on the current latest), Publish/Unpublish toggle, Delete.
- **Wire-shape shift handled**: the legacy BFF used HTTP `DELETE /openclaw/admin/releases/{version}`; the new backend is GET/POST-only — all mutations go through `POST /internal/releases/{version}/{delete|set-latest|publish|unpublish}` (`releaseAction` fetcher, version URI-encoded), consuming `{ok, version}`.
- **Documented deltas from legacy**: English copy; **delete now requires a confirmation dialog** (legacy fired destructive deletes with zero confirmation); **sync `useRef` in-flight locks on create and row actions** (the double-submit class Codex flagged on #2807, baked in from the start); full date+time formatting (`created_at` is an ISO string — local `formatIsoDateTime`, not the unix-based `formatUnixDate`).
- **Discoverability, admin-gated**: Releases entry in the Administration sidebar group, `PAGE_TITLE`, second admin home `EntryCard` — all behind `useIsAdmin()`; backend independently enforces `require_srp_account` + `require_admin_user`.

# Tests

- [x] 45 files / 341 tests green (6 new/extended test files): URL builder; fetchers (list `{releases}` unwrap, create body, action path URI-encoding via a `"1.2/3"` version, POST-only, `ApiError`); query hook; view-model (create+action locks via double synchronous invocation, empty-version guard, payload omits empty optionals, failure surfaces + keeps fields, confirm-delete flow — `requestDelete` never calls the API, only `confirmDelete` does); route (badges incl. conditional Set-latest, non-admin gate, publish call, delete dialog flow, create payload)
- [x] `pnpm lint`, `pnpm typecheck` (typegen picks up the new route), `pnpm test` — all green (what `dashboard-quality` runs)

# Notes

- Implementation plan: `docs/superpowers/plans/2026-07-09-console-releases-page.md`
- Known backend caveat (out of scope, tracked): no unique index on `version` (create TOCTOU) + non-transactional `is_latest` singleton — the release_repo hardening follow-up from #2774. The UI surfaces the 409 `release.already_exists` for the common case.
- Next: Plan 4c Users page (grant/boost modals with stable idempotency keys per #2783/#2788), then Plan 5 web/app `/admin` teardown.



## refactor(ios): split agent view model responsibilities (#2812)

- **sha**: `59d4c1aedca5d859676fbfc1958d393f1dfad5e9`
- **author**: bill-srp
- **date**: 2026-07-10T02:38:07Z

### Commit message

```
refactor(ios): split agent view model responsibilities (#2812)

## Summary
- Split `AgentViewModel` lifecycle and settings responsibilities into
dedicated extensions.
- Shared the install -> poll -> refresh path used by hire/install while
preserving private-pack identity after refresh.
- Added an architecture regression test for issue #2554 so the main file
cannot reintroduce the file/type-body SwiftLint suppression.

## Test plan
- [x] `xcodebuild test -project ZooClaw.xcodeproj -scheme ZooClaw
-destination 'platform=iOS Simulator,name=iPhone 17 Pro'
-parallel-testing-enabled NO
-maximum-concurrent-test-simulator-destinations 1
-only-testing:ZooClawTests/AgentViewModelArchitectureTests`
- [x] `xcodebuild test -project ZooClaw.xcodeproj -scheme ZooClaw
-destination 'platform=iOS Simulator,name=iPhone 17 Pro'
-parallel-testing-enabled NO
-maximum-concurrent-test-simulator-destinations 1
-only-testing:ZooClawTests/AgentViewModelInstallTests
-only-testing:ZooClawTests/AgentViewModelUpdateTests
-only-testing:ZooClawTests/AgentViewModelArchitectureTests`
- [x] `swiftlint`
- [x] `git diff --check`

Fixes #2554
```

### PR body

## Summary
- Split `AgentViewModel` lifecycle and settings responsibilities into dedicated extensions.
- Shared the install -> poll -> refresh path used by hire/install while preserving private-pack identity after refresh.
- Added an architecture regression test for issue #2554 so the main file cannot reintroduce the file/type-body SwiftLint suppression.

## Test plan
- [x] `xcodebuild test -project ZooClaw.xcodeproj -scheme ZooClaw -destination 'platform=iOS Simulator,name=iPhone 17 Pro' -parallel-testing-enabled NO -maximum-concurrent-test-simulator-destinations 1 -only-testing:ZooClawTests/AgentViewModelArchitectureTests`
- [x] `xcodebuild test -project ZooClaw.xcodeproj -scheme ZooClaw -destination 'platform=iOS Simulator,name=iPhone 17 Pro' -parallel-testing-enabled NO -maximum-concurrent-test-simulator-destinations 1 -only-testing:ZooClawTests/AgentViewModelInstallTests -only-testing:ZooClawTests/AgentViewModelUpdateTests -only-testing:ZooClawTests/AgentViewModelArchitectureTests`
- [x] `swiftlint`
- [x] `git diff --check`

Fixes #2554

