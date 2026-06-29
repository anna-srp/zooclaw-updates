---
title: "微信渠道设置不再重启机器人、会话不中断"
type: "体验优化"
priority: "中"
date: "2026-06-28"
status: "待审核"
channels: ""
---
# 微信渠道设置不再重启机器人、会话不中断

## 核心宣传点
现在添加或移除微信渠道时，机器人不再重启，正在进行的对话和会话不会被中断——配置即时生效，体验更顺滑。

## 原始内容
```
fix(openclaw-settings): reload WeChat channel without rollout (#2610)

## What

`trigger_index_reload` (WeChat channel setup/remove) no longer rolls out
the bot's Kubernetes Deployment. It now patches the running pod's
`/home/node/.openclaw/openclaw.json` directly via `runtime_exec`, so
OpenClaw's config watcher hot-reloads `openclaw-weixin` in place.

This is **PR 1** of a planned 3-PR rollout-remediation series.

## Why

The old path bumped top-level
`channels.openclaw-weixin.channelConfigUpdatedAt` via
`update_bot_config`. FastClaw treats a `channels` write as
`needsRollout`, so every WeChat setup/remove restarted the bot pod (new
ReplicaSet, dropped sessions). The credential/index writes and the
FastClaw channel API already sync to the running pod without a rollout —
only this reload marker forced one.

## Change

- `weixin_helpers.py::trigger_index_reload`: replace
`update_bot_config({"channels": {...}})` with a `runtime_exec(["node",
"-e", <script>])` that atomically (temp-file + rename) sets
`channels.openclaw-weixin.enabled` + `channelConfigUpdatedAt`,
preserving unknown fields.
- Unit tests asserting the no-rollout call path (`runtime_exec` used,
`update_bot_config` not awaited, the Node script targets `openclaw.json`
at `channels.openclaw-weixin.*`).

## Non-goals (separate follow-up PRs)

- Cross-process mutation lock / compensation for concurrent reloads (PR
2).
- Custom-agent binding order and remaining non-WeChat rollout paths (PR
3).
- No change to FastClaw's generic `channels`/`plugins` rollout guard.

## Validation

Local (claw-interface):
- `ruff check` + `ruff format --check` clean; `pyright` 0 errors on
changed files; `import-linter` 8/8 contracts kept.
- `pytest -k weixin` → 32 passed.

End-to-end against the staging bot (modified backend in the request
path, real WeChat scan):
- **Add** (real QR scan + authorize) → OpenClaw logs `config hot reload
applied (channels.openclaw-weixin.*)`, `openclaw.json` patched in place;
Deployment `generation` unchanged, same pod, `restartCount=0`.
- **Bidirectional message round-trip** through the channel (inbound →
`agent:main` → `text sent OK`).
- **Custom-agent bind** (`soulmate`) → binding written, routing
confirmed (`agent:soulmate:openclaw-weixin:…`), no rollout.
- **Pod restart persistence** → channel record (ConfigMap) + credentials
(JuiceFS PVC) survive, session resumes without re-scan.
- **Remove** → channel-API delete + `runtime_exec` cleanup, no
`update_bot_config`, no rollout.

The only rollout observed during testing came from an unrelated
concurrent actor on the shared staging bot using the old `PUT /bots`
path — i.e. exactly the behavior this PR removes.
```

PR Description:
## What

`trigger_index_reload` (WeChat channel setup/remove) no longer rolls out the bot's Kubernetes Deployment. It now patches the running pod's `/home/node/.openclaw/openclaw.json` directly via `runtime_exec`, so OpenClaw's config watcher hot-reloads `openclaw-weixin` in place.

This is **PR 1** of a planned 3-PR rollout-remediation series.

## Why

The old path bumped top-level `channels.openclaw-weixin.channelConfigUpdatedAt` via `update_bot_config`. FastClaw treats a `channels` write as `needsRollout`, so every WeChat setup/remove restarted the bot pod (new ReplicaSet, dropped sessions). The credential/index writes and the FastClaw channel API already sync to the running pod without a rollout — only this reload marker forced one.

## Change

- `weixin_helpers.py::trigger_index_reload`: replace `update_bot_config({"channels": {...}})` with a `runtime_exec(["node", "-e", <script>])` that atomically (temp-file + rename) sets `channels.openclaw-weixin.enabled` + `channelConfigUpdatedAt`, preserving unknown fields.
- Unit tests asserting the no-rollout call path (`runtime_exec` used, `update_bot_config` not awaited, the Node script targets `openclaw.json` at `channels.openclaw-weixin.*`).

## Non-goals (separate follow-up PRs)

- Cross-process mutation lock / compensation for concurrent reloads (PR 2).
- Custom-agent binding order and remaining non-WeChat rollout paths (PR 3).
- No change to FastClaw's generic `channels`/`plugins` rollout guard.

## Validation

Local (claw-interface):
- `ruff check` + `ruff format --check` clean; `pyright` 0 errors on changed files; `import-linter` 8/8 contracts kept.
- `pytest -k weixin` → 32 passed.

End-to-end against the staging bot (modified backend in the request path, real WeChat scan):
- **Add** (real QR scan + authorize) → OpenClaw logs `config hot reload applied (channels.openclaw-weixin.*)`, `openclaw.json` patched in place; Deployment `generation` unchanged, same pod, `restartCount=0`.
- **Bidirectional message round-trip** through the channel (inbound → `agent:main` → `text sent OK`).
- **Custom-agent bind** (`soulmate`) → binding written, routing confirmed (`agent:soulmate:openclaw-weixin:…`), no rollout.
- **Pod restart persistence** → channel record (ConfigMap) + credentials (JuiceFS PVC) survive, session resumes without re-scan.
- **Remove** → channel-API delete + `runtime_exec` cleanup, no `update_bot_config`, no rollout.

The only rollout observed during testing came from an unrelated concurrent actor on the shared staging bot using the old `PUT /bots` path — i.e. exactly the behavior this PR removes.

