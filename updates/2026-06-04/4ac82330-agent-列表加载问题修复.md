---
title: "Agent 列表加载问题修复"
type: "Bug Fix"
priority: "中"
date: "2026-06-04"
status: "待审核"
channels: ""
sha: "4ac823306b65da2194831de69c04c2c0509ada1e"
repo: "ecap-workspace"
pr: "2210"
---

# Agent 列表加载问题修复

## 核心宣传点

修复了部分用户 Agent 列表展示不完整的问题，确保所有已配置 Agent 能正确显示，不遗漏。

## 原始内容

### Commit Message

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
