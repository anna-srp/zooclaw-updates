# ecap-workspace - 2026-06-02
共 9 个 commit

---
## chore(claw-interface): add internal agent packs routes (#2154)
- **SHA**: fa0773f351058c6b17bf8986b8b89079c94ebfed
- **Author**: bill-srp
- **Date**: 2026-06-02T14:21:30Z
- **PR**: #2154

### Commit Message
```
chore(claw-interface): add internal agent packs routes (#2154)

## Summary
- Add an internal route package for zooclaw agent-pack management at
/internal/agent-packs
- Reuse the existing pack-store services directly from the route with
org_id fixed to zooclaw
- Place internal agent-pack request/response models under
app/schema/internal/agent_packs.py
- Use POST /internal/agent-packs/{pack_id} for internal pack metadata
updates
- Use POST /internal/agent-packs/{pack_id}/submissions to create
validated submissions without publishing
- Add POST
/internal/agent-packs/{pack_id}/submissions/{submission_id}/approve for
internal approval without admin auth
- Return the existing pack-store status values directly, including
deprecated
- Handle idempotent metadata updates and duplicate metadata conflicts
safely

## Test plan
- [x] cd services/claw-interface && ./.venv/bin/python -m pytest
tests/unit/test_internal_agent_packs_routes.py
tests/unit/test_admin_route_wiring.py tests/unit/test_schema_pack.py -q
- [x] cd services/claw-interface && ./.venv/bin/python -m ruff check
app/routes/internal app/schema/internal app/database/pack_repo.py
tests/unit/test_internal_agent_packs_routes.py
tests/unit/test_admin_route_wiring.py app/create_app.py
- [x] cd services/claw-interface && ./.venv/bin/python -m ruff format
--check app/routes/internal app/schema/internal
app/database/pack_repo.py tests/unit/test_internal_agent_packs_routes.py
tests/unit/test_admin_route_wiring.py app/create_app.py
```

### PR Description
## Summary
- Add an internal route package for zooclaw agent-pack management at /internal/agent-packs
- Reuse the existing pack-store services directly from the route with org_id fixed to zooclaw
- Place internal agent-pack request/response models under app/schema/internal/agent_packs.py
- Use POST /internal/agent-packs/{pack_id} for internal pack metadata updates
- Use POST /internal/agent-packs/{pack_id}/submissions to create validated submissions without publishing
- Add POST /internal/agent-packs/{pack_id}/submissions/{submission_id}/approve for internal approval without admin auth
- Return the existing pack-store status values directly, including deprecated
- Handle idempotent metadata updates and duplicate metadata conflicts safely

## Test plan
- [x] cd services/claw-interface && ./.venv/bin/python -m pytest tests/unit/test_internal_agent_packs_routes.py tests/unit/test_admin_route_wiring.py tests/unit/test_schema_pack.py -q
- [x] cd services/claw-interface && ./.venv/bin/python -m ruff check app/routes/internal app/schema/internal app/database/pack_repo.py tests/unit/test_internal_agent_packs_routes.py tests/unit/test_admin_route_wiring.py app/create_app.py
- [x] cd services/claw-interface && ./.venv/bin/python -m ruff format --check app/routes/internal app/schema/internal app/database/pack_repo.py tests/unit/test_internal_agent_packs_routes.py tests/unit/test_admin_route_wiring.py app/create_app.py

---
## feat(settings): add Microsoft Teams channel option (#1992)
- **SHA**: 831d746a36efdbff231c933241acd9ad52ac3db4
- **Author**: kaka-srp
- **Date**: 2026-06-02T13:15:28Z
- **PR**: #1992

### Commit Message
```
feat(settings): add Microsoft Teams channel option (#1992)

## Linear

https://linear.app/srpone/issue/ECA-845/add-microsoft-teams-channel-integration

## Summary
- Add Microsoft Teams to the channel picker and display existing
`msteams` channels as Microsoft Teams.
- Reuse the existing manual channel credential flow with App ID, App
Password, and optional Tenant ID.
- Add unit coverage for the platform picker, card label, and optional
Tenant ID payload.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`
- [ ] Real Microsoft Teams end-to-end messaging test, blocked locally by
no Microsoft 365 Teams tenant/account.
```

### PR Description
## Linear
https://linear.app/srpone/issue/ECA-845/add-microsoft-teams-channel-integration

## Summary
- Add Microsoft Teams to the channel picker and display existing `msteams` channels as Microsoft Teams.
- Reuse the existing manual channel credential flow with App ID, App Password, and optional Tenant ID.
- Add unit coverage for the platform picker, card label, and optional Tenant ID payload.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web/app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`
- [ ] Real Microsoft Teams end-to-end messaging test, blocked locally by no Microsoft 365 Teams tenant/account.

---
## fix(web): reload subagent chat history after reconnect (#2152)
- **SHA**: 4ac676c4a24453082bb7d69312f5289754d9d51f
- **Author**: sharplee-srp
- **Date**: 2026-06-02T13:00:24Z
- **PR**: #2152

### Commit Message
```
fix(web): reload subagent chat history after reconnect (#2152)

## Summary
- Re-sync subagent chat history whenever the OpenClaw WebSocket
`connectionGeneration` changes, including silent reconnects where
`ws.status` stays `connected`.
- Ignore stale `chat.history` responses from older generations so late
responses cannot overwrite newer history.
- Extend component/test WebSocket stubs with `connectionGeneration` and
add reconnect regression coverage.

## Root cause
`useOpenClawWebSocket` increments `connectionGeneration` on every
successful handshake, and `useSubagentSessions` already depends on that
value to resubscribe after silent reconnects. `useSubagentChat` only
watched `ws.status` and used a one-shot `historyLoadedRef`, so a
reconnect that did not transition away from `connected` could leave the
chat panel with stale local state. If the socket dropped right after a
streamed assistant response completed, the persisted final message could
be absent from the visible panel until a later full history load.

## Test plan
- [x] `pnpm -C web/app run test:unit
tests/unit/app/chat/useSubagentChat.unit.spec.ts
tests/unit/hooks/useSubagentChat.unit.spec.ts
tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx`
- [x] `pnpm -C web/app exec eslint
'src/app/[locale]/chat/hooks/useSubagentChat.ts'
'src/app/[locale]/chat/components/SubagentChatPanel.tsx'
'tests/unit/app/chat/useSubagentChat.unit.spec.ts'
'tests/unit/hooks/useSubagentChat.unit.spec.ts'
'tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx' --quiet`
- [x] `pnpm -C web/app exec tsc --noEmit --project tsconfig.json`
- [x] Devcontainer replay using `ecap-skills/.devcontainer`: ran `node
/workspace/lcm-stale-recovery-test.mjs` inside `ecap-skills-sharp-app-1`
and confirmed stale backup recovery imported the missing JSONL tail
(`recoveredCount=12`, `boot2.reason=reconciled missing session
messages`).
- [x] Devcontainer gateway reconnect simulation: inserted a temporary
session, confirmed initial `chat.history` returned only
`PR_2152_BEFORE_RECONNECT_*`, appended `PR_2152_AFTER_RECONNECT_*`
directly to the transcript to mimic a dropped final event, then
confirmed a new WebSocket `chat.history` returned
`PR_2152_AFTER_RECONNECT_ASSISTANT`; restored the temporary session
afterward.
```

### PR Description
## Summary
- Re-sync subagent chat history whenever the OpenClaw WebSocket `connectionGeneration` changes, including silent reconnects where `ws.status` stays `connected`.
- Ignore stale `chat.history` responses from older generations so late responses cannot overwrite newer history.
- Extend component/test WebSocket stubs with `connectionGeneration` and add reconnect regression coverage.

## Root cause
`useOpenClawWebSocket` increments `connectionGeneration` on every successful handshake, and `useSubagentSessions` already depends on that value to resubscribe after silent reconnects. `useSubagentChat` only watched `ws.status` and used a one-shot `historyLoadedRef`, so a reconnect that did not transition away from `connected` could leave the chat panel with stale local state. If the socket dropped right after a streamed assistant response completed, the persisted final message could be absent from the visible panel until a later full history load.

## Test plan
- [x] `pnpm -C web/app run test:unit tests/unit/app/chat/useSubagentChat.unit.spec.ts tests/unit/hooks/useSubagentChat.unit.spec.ts tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx`
- [x] `pnpm -C web/app exec eslint 'src/app/[locale]/chat/hooks/useSubagentChat.ts' 'src/app/[locale]/chat/components/SubagentChatPanel.tsx' 'tests/unit/app/chat/useSubagentChat.unit.spec.ts' 'tests/unit/hooks/useSubagentChat.unit.spec.ts' 'tests/unit/app/chat/SubagentChatPanel.unit.spec.tsx' --quiet`
- [x] `pnpm -C web/app exec tsc --noEmit --project tsconfig.json`
- [x] Devcontainer replay using `ecap-skills/.devcontainer`: ran `node /workspace/lcm-stale-recovery-test.mjs` inside `ecap-skills-sharp-app-1` and confirmed stale backup recovery imported the missing JSONL tail (`recoveredCount=12`, `boot2.reason=reconciled missing session messages`).
- [x] Devcontainer gateway reconnect simulation: inserted a temporary session, confirmed initial `chat.history` returned only `PR_2152_BEFORE_RECONNECT_*`, appended `PR_2152_AFTER_RECONNECT_*` directly to the transcript to mimic a dropped final event, then confirmed a new WebSocket `chat.history` returned `PR_2152_AFTER_RECONNECT_ASSISTANT`; restored the temporary session afterward.

---
## refactor(claw-interface): add V2 official agent uninstall service (#2153)
- **SHA**: 2c9f441ce87ba67ad77d089d06fb542368209337
- **Author**: bill-srp
- **Date**: 2026-06-02T11:39:27Z
- **PR**: #2153

### Commit Message
```
refactor(claw-interface): add V2 official agent uninstall service (#2153)

## Summary
- Add `app.services.computer.agent_uninstall_service` mirroring the V2
install service (#2148) in reverse order: remove from `agents.list` →
wipe workspace contents → remove Mattermost channel → mirror legacy
`mm_state` → tombstone the workspace row.
- Match V1 `_cleanup_removed_agents` (agent_deploy_phases.py:144-165)
semantics — workspace wipe and MM channel removal are non-blocking (log
+ continue); the `agents.list` write stays strict.
- Preserve `mattermost.*` runtime fields on the tombstoned row so
reinstall reuses the existing bot via `provision_mattermost_for_agent`'s
`existing_workspace` path (avoids orphan bots in Mattermost).
- Defense-in-depth: validate `agent_id` against `CUSTOM_AGENT_ID_RE`
before reaching any shell argv, and pass `--` to `find` to neutralize
agent_ids that could be parsed as flags.

## Test plan
- [x] `pytest tests/unit/test_agent_uninstall_service.py` — 23/23 pass
(orchestration, validation, regex hardening parametrized over 8
malformed inputs, non-blocking workspace wipe failure, non-blocking MM
channel removal failure, strict `remove_agent_from_agents_list` failure,
preserved Mattermost runtime, idempotent and failure paths for the
`remove_agent_from_agents_list` helper)
- [x] `pytest tests/unit/test_agent_install_service.py
tests/unit/test_agent_uninstall_service.py` — 50/50 pass (no regression
on install)
- [x] `pyright` clean on both new files
- [x] `ruff check` + `ruff format --check` clean
- [x] `lint-imports` — 8 contracts kept, 0 broken
```

### PR Description
## Summary
- Add `app.services.computer.agent_uninstall_service` mirroring the V2 install service (#2148) in reverse order: remove from `agents.list` → wipe workspace contents → remove Mattermost channel → mirror legacy `mm_state` → tombstone the workspace row.
- Match V1 `_cleanup_removed_agents` (agent_deploy_phases.py:144-165) semantics — workspace wipe and MM channel removal are non-blocking (log + continue); the `agents.list` write stays strict.
- Preserve `mattermost.*` runtime fields on the tombstoned row so reinstall reuses the existing bot via `provision_mattermost_for_agent`'s `existing_workspace` path (avoids orphan bots in Mattermost).
- Defense-in-depth: validate `agent_id` against `CUSTOM_AGENT_ID_RE` before reaching any shell argv, and pass `--` to `find` to neutralize agent_ids that could be parsed as flags.

## Test plan
- [x] `pytest tests/unit/test_agent_uninstall_service.py` — 23/23 pass (orchestration, validation, regex hardening parametrized over 8 malformed inputs, non-blocking workspace wipe failure, non-blocking MM channel removal failure, strict `remove_agent_from_agents_list` failure, preserved Mattermost runtime, idempotent and failure paths for the `remove_agent_from_agents_list` helper)
- [x] `pytest tests/unit/test_agent_install_service.py tests/unit/test_agent_uninstall_service.py` — 50/50 pass (no regression on install)
- [x] `pyright` clean on both new files
- [x] `ruff check` + `ruff format --check` clean
- [x] `lint-imports` — 8 contracts kept, 0 broken

---
## feat(billing): add time-grouped usage records (#2151)
- **SHA**: bc0f659dcd41681ab26bd590b54df9c0b16cab9d
- **Author**: kaka-srp
- **Date**: 2026-06-02T09:43:24Z
- **PR**: #2151

### Commit Message
```
feat(billing): add time-grouped usage records (#2151)

## Linear
https://linear.app/srpone/issue/ECA-873/usage-records

## Summary
- Add authenticated LLM credits usage record aggregation from Billing
Gateway events.
- Add Next BFF proxy and account usage UI with range switcher, summary
cards, credits chart, top models, and detail table.
- Keep token details and credits conversion metadata out of the
user-facing API and UI.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app run test:unit
tests/unit/app/api/user-usage-records.unit.spec.ts
tests/unit/components/billing/UsageRecord.unit.spec.tsx
tests/unit/hooks/queries/keys.unit.spec.ts
tests/unit/lib/api/user.unit.spec.ts
- [x] pnpm --dir web/app run test:unit
tests/unit/lint/react-hooks-config.unit.spec.ts --testTimeout=30000
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright app tests
- [x] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_billing_usage_records.py tests/unit/test_user_credits.py
-q
- [ ] pnpm --dir web run tsc (local workspace script fails before
typechecking with `ERROR Unknown option: if-present`; app-level `tsc
--noEmit` passed)
- [ ] pnpm --dir web run test:unit (local full run: 6740/6741 tests
passed; existing `tests/unit/lint/react-hooks-config.unit.spec.ts` hit
default 10s timeout; isolated run passes with higher timeout)
- [ ] cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pytest --cov=app
--cov-report=term-missing --cov-fail-under=90 -q (local full run failed
in unrelated openclaw_agents/org_invite tests and repo total coverage
was 88.51%; usage focused tests pass)
```

### PR Description
## Linear
https://linear.app/srpone/issue/ECA-873/usage-records

## Summary
- Add authenticated LLM credits usage record aggregation from Billing Gateway events.
- Add Next BFF proxy and account usage UI with range switcher, summary cards, credits chart, top models, and detail table.
- Keep token details and credits conversion metadata out of the user-facing API and UI.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit
- [x] pnpm --dir web/app run test:unit tests/unit/app/api/user-usage-records.unit.spec.ts tests/unit/components/billing/UsageRecord.unit.spec.tsx tests/unit/hooks/queries/keys.unit.spec.ts tests/unit/lib/api/user.unit.spec.ts
- [x] pnpm --dir web/app run test:unit tests/unit/lint/react-hooks-config.unit.spec.ts --testTimeout=30000
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright app tests
- [x] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_billing_usage_records.py tests/unit/test_user_credits.py -q
- [ ] pnpm --dir web run tsc (local workspace script fails before typechecking with `ERROR Unknown option: if-present`; app-level `tsc --noEmit` passed)
- [ ] pnpm --dir web run test:unit (local full run: 6740/6741 tests passed; existing `tests/unit/lint/react-hooks-config.unit.spec.ts` hit default 10s timeout; isolated run passes with higher timeout)
- [ ] cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q (local full run failed in unrelated openclaw_agents/org_invite tests and repo total coverage was 88.51%; usage focused tests pass)


---
## refactor(claw-interface): add V2 official agent install service (#2148)
- **SHA**: 3dacfc0e518412119403fca428a7fffc49b7d24e
- **Author**: bill-srp
- **Date**: 2026-06-02T08:25:02Z
- **PR**: #2148

### Commit Message
```
refactor(claw-interface): add V2 official agent install service (#2148)

## Summary
- Add `app.services.computer.agent_install_service` that installs one
official agent into the normalized V2 workspace store (`provision MM →
deploy pack archive → inject policy → register in agents.list → atomic
upsert workspace row`)
- Move `mattermost_client.py` under `app/services/mattermost/` and split
the per-agent provisioner into its own module; type all Mattermost API
responses as Pydantic models (no more `dict.get`)
- New `OFFICIAL_AGENT_PACK_DEPLOY_SCRIPT` runs in the agent runtime:
downloads the pack archive, extracts safely (tar + zip paths both
validated against traversal), preserves `MEMORY.md / USER.md / SOUL.md /
IDENTITY.md` and `data / artifacts / zip / memory / media` across
re-installs
- Remove unused `emoji` / `description` fields from `AgentWorkspace` and
`Pack` schemas
- Add `R2_AGENT_PACKS_DOMAIN` setting (falls back to `R2_PUBLIC_DOMAIN`)

## Test plan
- [x] `pytest tests/unit/test_agent_install_service.py` — 25/25 pass
(install happy path, MM failure abort, atomic reactivate, missing token,
empty / unknown / inactive agent, tar traversal, **new zip traversal**,
runtime script wiring, build_pack_archive_source error paths,
apply_agent_to_agents_list failure logging)
- [x] `pytest tests/unit/test_mattermost_agent_provisioner.py` —
provisioner extract verified
- [x] Pyright clean on changed files
- [x] CI: `claude-review / auto-review` ✓, `size / size-check` ✓
(size-override applied), `claw-interface-quality` re-running

## Notes on `emoji` / `description` removal (response to AI review)
The earlier commit `refactor(claw-interface): remove agent workspace
description` dropped these fields from `AgentPublic`, `Pack*`, and
`AgentWorkspace*`. Both AI reviewers flagged this as a potential
wire-contract break. **Confirmed safe in this codebase:**
- `AgentPublic.emoji` / `description`: searched `web/`,
`enterprise-admin/`, `ios/` — no consumer reads either field. The agent
list UI uses pack metadata via `pack_repo`, not the V1 agent response.
- `PackCreateRequest.emoji`: the pack creation form on the enterprise
admin already moved to `avatar_url` for visual identity. No live client
sends `emoji` today.
- `Pack.emoji`: only persisted; no read sites.

This is the right time to drop these — before the V2 install route lands
and bakes them deeper. If new clients need an emoji, `avatar_url`
already covers it.

## Notes for reviewers
- `install_official_agent` is **not yet wired to a route** — the entry
handler will land in a follow-up PR alongside `asset_id` URL validation
at the pack-submission boundary (currently a pack admin could submit an
arbitrary HTTPS asset URL; the runtime fetcher accepts whatever passes
through, so this needs locking down before the install route is exposed)
- The deploy script catches `BaseException` to ensure workspace cleanup
on cancel/SystemExit; pre-existing pattern. Claude review flagged this
as risky for re-install of an existing workspace — agreed worth a
follow-up to scope cleanup to "this run only" before the install route
ships
```

### PR Description
## Summary
- Add `app.services.computer.agent_install_service` that installs one official agent into the normalized V2 workspace store (`provision MM → deploy pack archive → inject policy → register in agents.list → atomic upsert workspace row`)
- Move `mattermost_client.py` under `app/services/mattermost/` and split the per-agent provisioner into its own module; type all Mattermost API responses as Pydantic models (no more `dict.get`)
- New `OFFICIAL_AGENT_PACK_DEPLOY_SCRIPT` runs in the agent runtime: downloads the pack archive, extracts safely (tar + zip paths both validated against traversal), preserves `MEMORY.md / USER.md / SOUL.md / IDENTITY.md` and `data / artifacts / zip / memory / media` across re-installs
- Remove unused `emoji` / `description` fields from `AgentWorkspace` and `Pack` schemas
- Add `R2_AGENT_PACKS_DOMAIN` setting (falls back to `R2_PUBLIC_DOMAIN`)

## Test plan
- [x] `pytest tests/unit/test_agent_install_service.py` — 25/25 pass (install happy path, MM failure abort, atomic reactivate, missing token, empty / unknown / inactive agent, tar traversal, **new zip traversal**, runtime script wiring, build_pack_archive_source error paths, apply_agent_to_agents_list failure logging)
- [x] `pytest tests/unit/test_mattermost_agent_provisioner.py` — provisioner extract verified
- [x] Pyright clean on changed files
- [x] CI: `claude-review / auto-review` ✓, `size / size-check` ✓ (size-override applied), `claw-interface-quality` re-running

## Notes on `emoji` / `description` removal (response to AI review)
The earlier commit `refactor(claw-interface): remove agent workspace description` dropped these fields from `AgentPublic`, `Pack*`, and `AgentWorkspace*`. Both AI reviewers flagged this as a potential wire-contract break. **Confirmed safe in this codebase:**
- `AgentPublic.emoji` / `description`: searched `web/`, `enterprise-admin/`, `ios/` — no consumer reads either field. The agent list UI uses pack metadata via `pack_repo`, not the V1 agent response.
- `PackCreateRequest.emoji`: the pack creation form on the enterprise admin already moved to `avatar_url` for visual identity. No live client sends `emoji` today.
- `Pack.emoji`: only persisted; no read sites.

This is the right time to drop these — before the V2 install route lands and bakes them deeper. If new clients need an emoji, `avatar_url` already covers it.

## Notes for reviewers
- `install_official_agent` is **not yet wired to a route** — the entry handler will land in a follow-up PR alongside `asset_id` URL validation at the pack-submission boundary (currently a pack admin could submit an arbitrary HTTPS asset URL; the runtime fetcher accepts whatever passes through, so this needs locking down before the install route is exposed)
- The deploy script catches `BaseException` to ensure workspace cleanup on cancel/SystemExit; pre-existing pattern. Claude review flagged this as risky for re-install of an existing workspace — agreed worth a follow-up to scope cleanup to "this run only" before the install route ships

---
## fix(claw-interface): canonicalize mattermost user on account root (#2149)
- **SHA**: 2f6e0ee878dd8d897f303b27a9dd2561b875b036
- **Author**: bill-srp
- **Date**: 2026-06-02T06:56:00Z
- **PR**: #2149

### Commit Message
```
fix(claw-interface): canonicalize mattermost user on account root (#2149)

## Summary
- Add root-level `mattermost_user` field on the account schema as the
canonical location for the human user's Mattermost identity (design:
`docs/superpowers/specs/2026-06-02-account-mattermost-user-root-design.md`).
- Update OpenClaw bot init and warm-pool bot init to write
`mattermost_user` at the account root; new bot records no longer include
`mattermost_user`.
- Read path (`user/enrichment.py`, `openclaw_agents/core.py`) prefers
root `account.mattermost_user` and falls back to legacy
`openclaw_bots[0].mattermost_user` for backwards compatibility.
- Add one-off migration `migrate_mattermost_user_to_account_root.py`
that copies legacy nested data to the account root.

## Root cause
`mattermost_user` previously lived inside `openclaw_bots[*]`, but it
describes the human user's Mattermost account, not a bot. Bot records
stay bot-scoped (`mattermost_bots`); the human Mattermost identity
belongs on the account root.

## Test plan
- [x] `tests/unit/test_openclaw_routes.py` / `test_openclaw_agents.py` —
bot init writes root `mattermost_user`, omits it from the bot record.
- [x] `tests/unit/test_warm_pool_openclaw_assets.py` — warm-pool
materialization writes root `mattermost_user`.
- [x] `tests/unit/test_user_enrichment_service.py` / `test_user_repo.py`
— read prefers root, falls back to legacy nested value.
- [x] `tests/unit/test_migrate_mattermost_user_to_account_root.py` —
migration covers nested→root copy, skip-if-already-root, and dry-run.
```

### PR Description
## Summary
- Add root-level `mattermost_user` field on the account schema as the canonical location for the human user's Mattermost identity (design: `docs/superpowers/specs/2026-06-02-account-mattermost-user-root-design.md`).
- Update OpenClaw bot init and warm-pool bot init to write `mattermost_user` at the account root; new bot records no longer include `mattermost_user`.
- Read path (`user/enrichment.py`, `openclaw_agents/core.py`) prefers root `account.mattermost_user` and falls back to legacy `openclaw_bots[0].mattermost_user` for backwards compatibility.
- Add one-off migration `migrate_mattermost_user_to_account_root.py` that copies legacy nested data to the account root.

## Root cause
`mattermost_user` previously lived inside `openclaw_bots[*]`, but it describes the human user's Mattermost account, not a bot. Bot records stay bot-scoped (`mattermost_bots`); the human Mattermost identity belongs on the account root.

## Test plan
- [x] `tests/unit/test_openclaw_routes.py` / `test_openclaw_agents.py` — bot init writes root `mattermost_user`, omits it from the bot record.
- [x] `tests/unit/test_warm_pool_openclaw_assets.py` — warm-pool materialization writes root `mattermost_user`.
- [x] `tests/unit/test_user_enrichment_service.py` / `test_user_repo.py` — read prefers root, falls back to legacy nested value.
- [x] `tests/unit/test_migrate_mattermost_user_to_account_root.py` — migration covers nested→root copy, skip-if-already-root, and dry-run.

---
## fix(billing): expire providerless v2 entitlements (#2150)
- **SHA**: d74d617fa9fdb8cda8faa34bc0d267319ae65448
- **Author**: kaka-srp
- **Date**: 2026-06-02T06:09:14Z
- **PR**: #2150

### Commit Message
```
fix(billing): expire providerless v2 entitlements (#2150)

## Summary
- Add Billing v2 providerless subscription entitlement expiry for
trial/subscription-code/manual entitlements.
- Wire the job into existing Billing v2 subscription maintenance under
`/admin/cron/check-subscription-sync`.
- Add lease-based claiming, Billing Profile overlay for cleanup, and
tests for cleanup/retry/superseded-access behavior.

## Root cause
Provider-backed v2 subscriptions had period-end cleanup, but
providerless v2 entitlements only expired in read-time access
resolution. Pure v2 trial/code users could be blocked by access checks
after expiry while BG wallets, model/resource state, and OpenClaw bots
were not reclaimed by v2 cron.

## Rollout notes
- Requires the new `entitlement_due_providerless_expiry` index to be
created via the Billing v2 index script before/with production rollout.
- Controlled by `BILLING_V2_WRITES_ENABLED`; with writes disabled the
new job returns zero counts.

## Test plan
- [x] `ruff check app/database/entitlement_ledger_repo.py
app/services/billing_v2/expiry.py app/cron/billing_v2_subscription.py
tests/unit/test_billing_v2_expiry.py
tests/unit/test_billing_v2_subscription_cron.py
tests/unit/test_billing_v2_repos.py`
- [x] `pyright app/database/entitlement_ledger_repo.py
app/services/billing_v2/expiry.py app/cron/billing_v2_subscription.py
tests/unit/test_billing_v2_expiry.py
tests/unit/test_billing_v2_subscription_cron.py
tests/unit/test_billing_v2_repos.py`
- [x] `pytest tests/unit/test_billing_v2_expiry.py
tests/unit/test_billing_v2_subscription_cron.py
tests/unit/test_billing_v2_repos.py -q`
```

### PR Description
## Summary
- Add Billing v2 providerless subscription entitlement expiry for trial/subscription-code/manual entitlements.
- Wire the job into existing Billing v2 subscription maintenance under `/admin/cron/check-subscription-sync`.
- Add lease-based claiming, Billing Profile overlay for cleanup, and tests for cleanup/retry/superseded-access behavior.

## Root cause
Provider-backed v2 subscriptions had period-end cleanup, but providerless v2 entitlements only expired in read-time access resolution. Pure v2 trial/code users could be blocked by access checks after expiry while BG wallets, model/resource state, and OpenClaw bots were not reclaimed by v2 cron.

## Rollout notes
- Requires the new `entitlement_due_providerless_expiry` index to be created via the Billing v2 index script before/with production rollout.
- Controlled by `BILLING_V2_WRITES_ENABLED`; with writes disabled the new job returns zero counts.

## Test plan
- [x] `ruff check app/database/entitlement_ledger_repo.py app/services/billing_v2/expiry.py app/cron/billing_v2_subscription.py tests/unit/test_billing_v2_expiry.py tests/unit/test_billing_v2_subscription_cron.py tests/unit/test_billing_v2_repos.py`
- [x] `pyright app/database/entitlement_ledger_repo.py app/services/billing_v2/expiry.py app/cron/billing_v2_subscription.py tests/unit/test_billing_v2_expiry.py tests/unit/test_billing_v2_subscription_cron.py tests/unit/test_billing_v2_repos.py`
- [x] `pytest tests/unit/test_billing_v2_expiry.py tests/unit/test_billing_v2_subscription_cron.py tests/unit/test_billing_v2_repos.py -q`

---
## fix(billing): handle apple renewal status webhooks (#2145)
- **SHA**: e7bc9180520607a50f7f8bf43954f5dfd4aea40a
- **Author**: kaka-srp
- **Date**: 2026-06-02T02:33:01Z
- **PR**: #2145

### Commit Message
```
fix(billing): handle apple renewal status webhooks (#2145)

## Summary
- Read Apple notification environment from the real App Store Server
Notification v2 shape (`data.environment`) and normalize SDK enum
strings before routing.
- Handle `DID_CHANGE_RENEWAL_STATUS` for Apple Billing v2 so
`AUTO_RENEW_DISABLED` marks the agreement canceling and
`AUTO_RENEW_ENABLED` restores active renewal.
- Decode `data.signedRenewalInfo` and process renewal-status webhooks
even when Apple omits `signedTransactionInfo`, using the existing
Billing v2 agreement as the owner/period context.
- Prevent Billing v2 current access from falling back to providerless
trial after a paid provider subscription has started and later reaches
period end. Trial credits remain active/auditable and can still be
included in credit balance; this only fixes subscription state
resolution.
- Split Apple paid transaction fact recording into `billing_v2_facts.py`
to keep notification routing small and under the app file-size guard.

## Root cause
Apple sends the notification environment under `data.environment`, but
the route only checked a top-level `environment`. The cancellation
webhook was acknowledged but rejected as `received=unknown`. Billing v2
also only handled the old legacy Apple webhook set and ignored
renewal-status changes.

During staging iOS sandbox testing, a second state-resolution issue was
found: after a paid provider subscription period ends, an earlier active
providerless trial entitlement could make `current_access` fall back to
`trial`. That is incorrect for subscription state once a paid provider
subscription has started, even though the trial credit ledger entry
itself should remain active.

CI review also correctly pointed out that Apple renewal-status
notifications can rely on `signedRenewalInfo`; this PR now decodes that
payload and covers the no-transaction renewal-status path.

## Test plan
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff format --check
app/routes/apple.py app/services/apple/billing_v2.py
app/services/apple/billing_v2_facts.py
app/services/apple/billing_v2_notifications.py
app/services/billing_summary/current_access.py
tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py
tests/unit/test_billing_summary_v2.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m ruff check
app/routes/apple.py app/services/apple/billing_v2.py
app/services/apple/billing_v2_facts.py
app/services/apple/billing_v2_notifications.py
app/services/billing_summary/current_access.py
tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py
tests/unit/test_billing_summary_v2.py`
- [x] `cd services/claw-interface &&
/home/node/.venvs/claw-interface/bin/python -m pyright
app/routes/apple.py app/services/apple/billing_v2.py
app/services/apple/billing_v2_facts.py
app/services/apple/billing_v2_notifications.py
app/services/billing_summary/current_access.py
tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py
tests/unit/test_billing_summary_v2.py`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_billing_summary_v2.py
services/claw-interface/tests/unit/test_apple_routes.py
services/claw-interface/tests/unit/test_apple_billing_v2.py`
- [x] Staging iOS sandbox: subscribe, restore auto-renew, cancel
auto-renew; verified Apple `DID_CHANGE_RENEWAL_STATUS` events process
and agreement transitions active/canceling correctly.
- [x] Staging data simulation: current access before Apple period end
resolves to `canceling`; after period end resolves to `expired/free`
instead of trial fallback.

## Staging beta
- `service-v0.7.3-beta.4` deployed initial Apple webhook fix.
- `service-v0.7.3-beta.5` was cut for the trial-fallback fix; staging
deploy monitoring is intentionally not required for this PR gate.
```

### PR Description
## Summary
- Read Apple notification environment from the real App Store Server Notification v2 shape (`data.environment`) and normalize SDK enum strings before routing.
- Handle `DID_CHANGE_RENEWAL_STATUS` for Apple Billing v2 so `AUTO_RENEW_DISABLED` marks the agreement canceling and `AUTO_RENEW_ENABLED` restores active renewal.
- Decode `data.signedRenewalInfo` and process renewal-status webhooks even when Apple omits `signedTransactionInfo`, using the existing Billing v2 agreement as the owner/period context.
- Prevent Billing v2 current access from falling back to providerless trial after a paid provider subscription has started and later reaches period end. Trial credits remain active/auditable and can still be included in credit balance; this only fixes subscription state resolution.
- Split Apple paid transaction fact recording into `billing_v2_facts.py` to keep notification routing small and under the app file-size guard.

## Root cause
Apple sends the notification environment under `data.environment`, but the route only checked a top-level `environment`. The cancellation webhook was acknowledged but rejected as `received=unknown`. Billing v2 also only handled the old legacy Apple webhook set and ignored renewal-status changes.

During staging iOS sandbox testing, a second state-resolution issue was found: after a paid provider subscription period ends, an earlier active providerless trial entitlement could make `current_access` fall back to `trial`. That is incorrect for subscription state once a paid provider subscription has started, even though the trial credit ledger entry itself should remain active.

CI review also correctly pointed out that Apple renewal-status notifications can rely on `signedRenewalInfo`; this PR now decodes that payload and covers the no-transaction renewal-status path.

## Test plan
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff format --check app/routes/apple.py app/services/apple/billing_v2.py app/services/apple/billing_v2_facts.py app/services/apple/billing_v2_notifications.py app/services/billing_summary/current_access.py tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py tests/unit/test_billing_summary_v2.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m ruff check app/routes/apple.py app/services/apple/billing_v2.py app/services/apple/billing_v2_facts.py app/services/apple/billing_v2_notifications.py app/services/billing_summary/current_access.py tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py tests/unit/test_billing_summary_v2.py`
- [x] `cd services/claw-interface && /home/node/.venvs/claw-interface/bin/python -m pyright app/routes/apple.py app/services/apple/billing_v2.py app/services/apple/billing_v2_facts.py app/services/apple/billing_v2_notifications.py app/services/billing_summary/current_access.py tests/unit/test_apple_routes.py tests/unit/test_apple_billing_v2.py tests/unit/test_billing_summary_v2.py`
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_billing_summary_v2.py services/claw-interface/tests/unit/test_apple_routes.py services/claw-interface/tests/unit/test_apple_billing_v2.py`
- [x] Staging iOS sandbox: subscribe, restore auto-renew, cancel auto-renew; verified Apple `DID_CHANGE_RENEWAL_STATUS` events process and agreement transitions active/canceling correctly.
- [x] Staging data simulation: current access before Apple period end resolves to `canceling`; after period end resolves to `expired/free` instead of trial fallback.

## Staging beta
- `service-v0.7.3-beta.4` deployed initial Apple webhook fix.
- `service-v0.7.3-beta.5` was cut for the trial-fallback fix; staging deploy monitoring is intentionally not required for this PR gate.
