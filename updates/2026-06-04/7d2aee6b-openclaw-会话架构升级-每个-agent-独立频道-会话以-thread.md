---
title: "OpenClaw 会话架构升级：每个 Agent 独立频道，会话以 Thread 形式组织"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-04"
status: "待审核"
channels: ""
sha: "7d2aee6b7464abe17a1be641a01e0de0e18da1ca"
repo: "ecap-workspace"
pr: "2218"
---

# OpenClaw 会话架构升级：每个 Agent 独立频道，会话以 Thread 形式组织

## 核心宣传点

ZooClaw 内部 OpenClaw 的会话组织方式升级，每个 Agent 拥有独立频道，每次对话作为独立 Thread，未来对话历史管理更清晰。

## 原始内容

### Commit Message

```
feat(claw-interface): make OpenClaw sessions Mattermost threads in a per-agent channel (#2218)

## Linear

https://linear.app/srpone/issue/ECA-896/openclaw-session-threads-per-agent-channel-root-post-id

## Summary
Migrate OpenClaw chat sessions from "one private Mattermost channel per
session" to **one reusable per-agent channel with a thread (root post)
per session**. Backend-only (`services/claw-interface`); ships
independently of `web/`.

- `root_post_id` added to `OpenClawSessionChannelRecord` /
`OpenClawSessionChannelResponse`.
- `session_channel_id` added to `AgentMattermostRuntime` — the dedicated
per-agent channel, created lazily on first session and persisted back
via `agent_workspace_repo.update_fields`.
- `Account.resolve_mattermost_user_token()` (schema-level, so the
service can author the seed post as the user).
- Mattermost client: `get_channel_by_name` (create-race adoption) +
`delete_post` (orphan-post cleanup).
- Repo index migration: drop unique `mm_channel_id` → **sparse-unique**
`root_post_id`; `ensure_indexes` drop is idempotent.
- `create_session_channel` now resolves/creates the per-agent channel
(`_ensure_agent_channel`, deterministic `zc-a-{sha1}` name, race-safe),
posts a **user→bot→admin**-authored seed root post, and stores
`{mm_channel_id=channel, root_post_id}`. On DB-insert failure it deletes
the orphan **post** (never the shared channel) and re-raises.

The first commit is a precursor typed-repo refactor (extract the
session-channel schema into its own module; repo accepts/returns
`OpenClawSessionChannelRecord` instead of `dict`).

**Backward compatible:** legacy per-session-channel records read
unchanged (`root_post_id=None`); the index drop is guarded for
fresh/already-migrated DBs.

**Out of scope (follow-up):** the frontend/agent reply path must post
conversation messages with `root_id = root_post_id` so they land in the
thread (lives in `web/` + the bot runtime).

**Deploy note:** `ensure_indexes` drops `unique_mm_channel_id` at
startup on first deploy — safe (legacy rows have distinct channels; the
sparse index excludes rows without `root_post_id`), but it is the one
change that touches an existing prod index.

## Split note
This PR is the **backend half** of the original combined branch. The
frontend sidebar restructure + "New Chat" entry was split into **#2216**
(`feat/openclaw-session-threads`), now frontend-only. The two ship
independently; this backend PR carries no `web/` changes.

## Test plan
- [ ] CI `python-code-quality / build-and-test` green (ruff + pyright +
pytest)
- [ ] Local verified: 98 unit tests across the touched files pass;
pyright 0 errors; ruff clean; import-linter 8/8 contracts kept
- [ ] New session creates-or-reuses the per-agent channel and persists
`session_channel_id` on the workspace (no extra MM call on reuse)
- [ ] Session record carries `(mm_channel_id, root_post_id)`; the seed
root post appears in the channel
- [ ] Legacy per-session-channel records still list/read without error

---------

Co-authored-by: Claude Sonnet 4.6 <noreply@anthropic.com>
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-896/openclaw-session-threads-per-agent-channel-root-post-id

## Summary
Migrate OpenClaw chat sessions from "one private Mattermost channel per session" to **one reusable per-agent channel with a thread (root post) per session**. Backend-only (`services/claw-interface`); ships independently of `web/`.

- `root_post_id` added to `OpenClawSessionChannelRecord` / `OpenClawSessionChannelResponse`.
- `session_channel_id` added to `AgentMattermostRuntime` — the dedicated per-agent channel, created lazily on first session and persisted back via `agent_workspace_repo.update_fields`.
- `Account.resolve_mattermost_user_token()` (schema-level, so the service can author the seed post as the user).
- Mattermost client: `get_channel_by_name` (create-race adoption) + `delete_post` (orphan-post cleanup).
- Repo index migration: drop unique `mm_channel_id` → **sparse-unique** `root_post_id`; `ensure_indexes` drop is idempotent.
- `create_session_channel` now resolves/creates the per-agent channel (`_ensure_agent_channel`, deterministic `zc-a-{sha1}` name, race-safe), posts a **user→bot→admin**-authored seed root post, and stores `{mm_channel_id=channel, root_post_id}`. On DB-insert failure it deletes the orphan **post** (never the shared channel) and re-raises.

The first commit is a precursor typed-repo refactor (extract the session-channel schema into its own module; repo accepts/returns `OpenClawSessionChannelRecord` instead of `dict`).

**Backward compatible:** legacy per-session-channel records read unchanged (`root_post_id=None`); the index drop is guarded for fresh/already-migrated DBs.

**Out of scope (follow-up):** the frontend/agent reply path must post conversation messages with `root_id = root_post_id` so they land in the thread (lives in `web/` + the bot runtime).

**Deploy note:** `ensure_indexes` drops `unique_mm_channel_id` at startup on first deploy — safe (legacy rows have distinct channels; the sparse index excludes rows without `root_post_id`), but it is the one change that touches an existing prod index.

## Split note
This PR is the **backend half** of the original combined branch. The frontend sidebar restructure + "New Chat" entry was split into **#2216** (`feat/openclaw-session-threads`), now frontend-only. The two ship independently; this backend PR carries no `web/` changes.

## Test plan
- [ ] CI `python-code-quality / build-and-test` green (ruff + pyright + pytest)
- [ ] Local verified: 98 unit tests across the touched files pass; pyright 0 errors; ruff clean; import-linter 8/8 contracts kept
- [ ] New session creates-or-reuses the per-agent channel and persists `session_channel_id` on the workspace (no extra MM call on reuse)
- [ ] Session record carries `(mm_channel_id, root_post_id)`; the seed root post appears in the channel
- [ ] Legacy per-session-channel records still list/read without error

