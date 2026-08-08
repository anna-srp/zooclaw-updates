---
title: "新引擎用户自动获得默认助手"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-07"
status: "待审核"
channels: ""
---

## 核心宣传点

使用新一代引擎的用户注册后自动拥有一个默认「Assistant」助手，不占套餐名额也不会被误删，开箱即可对话。

## 原始内容

### feat(claw-interface): provision default main agent for v2 engine users (#3287)

- SHA: `ec5d2abcd0acd5df0702e17e3dad3afd9112f596`
- 仓库: 见 raw/2026-08-07

**Commit Message:**

```
feat(claw-interface): provision default main agent for v2 engine users (#3287)

# Description

Under the AGENTS_V2 no-computer onboarding cutover, eligible new users
start with zero agents — the v1 computer runtime auto-provisioned a
"main" Assistant, but the engine runtime had no equivalent. This PR
gives every AGENTS_V2-eligible user a default pack-less **"Assistant"**
engine agent: no persona docs, no environment, no skills.

Design spec:
`docs/superpowers/specs/2026-08-06-v2-default-main-agent-design.md`
(included in this PR, with the implementation plan).

## What changed

- **New service**
`engine_main_agent_service.ensure_default_main_agent()` —
eligibility-gated; reuses the engine-workspace CAS claim machinery keyed
by a new `internal_role="main"`; calls `create_agent` with
`persona_docs=[]` and no environment; then seeds LiteLLM/user-token
credentials and binds the Mattermost channel exactly like pack installs.
Failures mark the row `install_failed` (reclaimable) and re-raise for
callers to catch.
- **Schema**: `AgentWorkspaceInternalRole` gains `"main"`;
`AgentWorkspace.is_main` is true for it, so `AgentPublic.is_main` and
the existing frontend sidebar "Assistant" row work with zero FE changes.
- **Trigger 1 — registration (best-effort)**: `POST
/account/personal-org`, `/team-org`, `/invite` provision the main agent
after org membership exists; failures log and never fail registration.
Bare `POST /account` is untouched (no org yet).
- **Trigger 2 — lazy ensure on `GET /agents`**: repairs
registration-time failures and organically backfills existing v2 users.
Steady-state cost is one indexed read; ineligible users cost nothing.
- **Quota-free**: `count_install_quota_usage` excludes
`internal_role="main"` rows, so the default agent never consumes a plan
slot.
- **Protected**: `uninstall_engine_agent` rejects the main agent with
`agent.main_agent_protected`.
- **Repo**: `claim_install_state` accepts pack-less claims when
`internal_role` is set (insert seeds `agent_id` from the claim's
`agent_id`, which equals `pack_id` on every pack-install insert —
behavior-preserving).
- **Refactor**: `_engine_channels_enabled` → shared
`install_shared.engine_channels_enabled()`.

## Concurrency & idempotency

The pre-existing unique partial index
`unique_internal_engine_agent_role` on `(uid, org_id, runtime,
internal_role)` makes concurrent ensures safe (loser gets duplicate-key
→ `None`), and `idempotency_key=workspace_id` dedupes engine-side
creates on reclaimed rows.

## Rollout

Backend-only, no migration, no new settings. Dark for prod users until
AGENTS_V2 eligibility opens (email allowlist); staging (open rollout)
exercises it immediately — new registrations get the agent, existing v2
users get it on their next agents-list load.

# Test Plan

- [x] New unit suites: service (8 cases: eligibility gate, fast path,
in-progress, claim loser, bare-create contract incl. no-environment
kwargs, reclaim skip-create, channel-bind persistence, failure marking),
pack-less claim, quota query, schema `is_main`, uninstall guard,
list-route ensure, register-route hooks (success + failure-survival per
handler)
- [x] 270 tests across the 11 touched suites pass locally
- [x] `ruff check` + `ruff format --check` clean; `pyright app/ tests/`
0 errors; `lint-imports` 8/8 contracts kept
- [x] Pre-existing quota-query assertion updated for the new
`internal_role` exclusion
- [ ] CI whole-suite coverage gate (`--cov-fail-under=90`) — enforced by
`claw-interface-quality`; the full local run was not completed
(implementation session stalled mid-run; only failures seen were the
since-fixed stale quota assertion and pre-existing local-env deptry
breakage)
- [ ] Staging smoke after backend release: register a fresh user → main
agent appears in `GET /agents` and the sidebar; verify uninstall is
rejected

Note: local full-suite coverage was skipped in favor of CI (slow serial
run); the local pre-push verifier was bypassed for this push because the
checkout's project-local `.venv` has pre-existing bad-interpreter
corruption — all equivalent checks were run manually from the host venv.
```

**PR Body:**

# Description

Under the AGENTS_V2 no-computer onboarding cutover, eligible new users start with zero agents — the v1 computer runtime auto-provisioned a "main" Assistant, but the engine runtime had no equivalent. This PR gives every AGENTS_V2-eligible user a default pack-less **"Assistant"** engine agent: no persona docs, no environment, no skills.

Design spec: `docs/superpowers/specs/2026-08-06-v2-default-main-agent-design.md` (included in this PR, with the implementation plan).

## What changed

- **New service** `engine_main_agent_service.ensure_default_main_agent()` — eligibility-gated; reuses the engine-workspace CAS claim machinery keyed by a new `internal_role="main"`; calls `create_agent` with `persona_docs=[]` and no environment; then seeds LiteLLM/user-token credentials and binds the Mattermost channel exactly like pack installs. Failures mark the row `install_failed` (reclaimable) and re-raise for callers to catch.
- **Schema**: `AgentWorkspaceInternalRole` gains `"main"`; `AgentWorkspace.is_main` is true for it, so `AgentPublic.is_main` and the existing frontend sidebar "Assistant" row work with zero FE changes.
- **Trigger 1 — registration (best-effort)**: `POST /account/personal-org`, `/team-org`, `/invite` provision the main agent after org membership exists; failures log and never fail registration. Bare `POST /account` is untouched (no org yet).
- **Trigger 2 — lazy ensure on `GET /agents`**: repairs registration-time failures and organically backfills existing v2 users. Steady-state cost is one indexed read; ineligible users cost nothing.
- **Quota-free**: `count_install_quota_usage` excludes `internal_role="main"` rows, so the default agent never consumes a plan slot.
- **Protected**: `uninstall_engine_agent` rejects the main agent with `agent.main_agent_protected`.
- **Repo**: `claim_install_state` accepts pack-less claims when `internal_role` is set (insert seeds `agent_id` from the claim's `agent_id`, which equals `pack_id` on every pack-install insert — behavior-preserving).
- **Refactor**: `_engine_channels_enabled` → shared `install_shared.engine_channels_enabled()`.

## Concurrency & idempotency

The pre-existing unique partial index `unique_internal_engine_agent_role` on `(uid, org_id, runtime, internal_role)` makes concurrent ensures safe (loser gets duplicate-key → `None`), and `idempotency_key=workspace_id` dedupes engine-side creates on reclaimed rows.

## Rollout

Backend-only, no migration, no new settings. Dark for prod users until AGENTS_V2 eligibility opens (email allowlist); staging (open rollout) exercises it immediately — new registrations get the agent, existing v2 users get it on their next agents-list load.

# Test Plan

- [x] New unit suites: service (8 cases: eligibility gate, fast path, in-progress, claim loser, bare-create contract incl. no-environment kwargs, reclaim skip-create, channel-bind persistence, failure marking), pack-less claim, quota query, schema `is_main`, uninstall guard, list-route ensure, register-route hooks (success + failure-survival per handler)
- [x] 270 tests across the 11 touched suites pass locally
- [x] `ruff check` + `ruff format --check` clean; `pyright app/ tests/` 0 errors; `lint-imports` 8/8 contracts kept
- [x] Pre-existing quota-query assertion updated for the new `internal_role` exclusion
- [ ] CI whole-suite coverage gate (`--cov-fail-under=90`) — enforced by `claw-interface-quality`; the full local run was not completed (implementation session stalled mid-run; only failures seen were the since-fixed stale quota assertion and pre-existing local-env deptry breakage)
- [ ] Staging smoke after backend release: register a fresh user → main agent appears in `GET /agents` and the sidebar; verify uninstall is rejected

Note: local full-suite coverage was skipped in favor of CI (slow serial run); the local pre-push verifier was bypassed for this push because the checkout's project-local `.venv` has pre-existing bad-interpreter corruption — all equivalent checks were run manually from the host venv.


