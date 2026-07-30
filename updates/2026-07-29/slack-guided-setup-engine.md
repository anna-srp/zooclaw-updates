---
title: "Engine 版 Agent 接入 Slack 也有完整向导了：一步步照做即可，不再面对空白密钥框"
type: "体验优化"
priority: "中"
date: "2026-07-29"
status: "待审核"
channels: ""
---

## 核心宣传点

之前给 Engine（v2）版工作区接入 Slack 会直接丢给你两个没有任何说明的密钥输入框；现在复用了完整的 Slack 引导向导，带分步说明和跳转 Slack 后台的直达链接，接入门槛大幅降低。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- commit：b50c82ebb849a5e5075fbe267b509ffd813780f2
- PR：#3131
- 日期：2026-07-29T14:37:49Z

### Commit message

```
feat(channels): reuse the v1 guided Slack setup for engine agents (#3131)

## Linear
<!-- none — surfaced from a code review of the channels page, no ticket
-->

## Summary

Engine (v2) channel targets were gated out of the guided setup render
path. Picking Slack for an engine workspace dropped the user straight
onto two unlabeled `xoxb-…` / `xapp-…` boxes, while the same platform on
a v1 bot target got the full manifest wizard with step-by-step
instructions and a deep link to the Slack app console.

Two expressions in `useAddChannelForm.ts` did the gating:

```ts
const effectiveShowAdvanced = showAdvanced || isEngineTarget          // forced manual mode
guidedCapable: !isEngineTarget && flags.guidedCapable                 // killed the method cards
```

`SlackSetupWizard` is pure UI over an `onAdd` callback — no `uid`, no
backend session, no v1-only endpoint — so it needed target threading
rather than a rewrite.

- **`ENGINE_GUIDED_PLATFORMS`** allowlists which engine platforms get
the guided method cards. **Feishu and WeCom deliberately stay on manual
entry**: their guided flow is a backend QR session that resolves the
target via `get_user_bot_and_token(uid)` and writes with
`client.add_channel(bot_id, …)` (`openclaw_settings/feishu.py:276`,
`wecom.py:194`). There is no workspace parameter anywhere in that path,
so offering it for an engine target would provision the channel onto the
user's **bot** instead of the selected workspace. A test pins this.
- Threads the selected target through `onSlackSetup` → `ChannelsSection`
→ `SlackSetupWizard`, so wizard completion routes to `onEngineAdd`.
- Omits `agent_id` for engine targets — engine channels have no
per-channel agent binding.
- Excludes `pairing` from the engine DM-policy list; the backend rejects
it with `channel.pairing_unsupported`
(`engine_agent_channels_service.py:166`).
- Derives the account-id and Slack app-name defaults from the selected
workspace's channels rather than the bot's.

### Relationship to the design of record

`docs/superpowers/specs/2026-07-20-engine-agent-channels-design.md`
lists as a v1 non-goal:

> No QR/guided auto-provision wizard for engine Slack/Feishu/WeCom in v1
(manual entry only; the auto-provision convenience can follow later).

This is that follow-up, **for Slack only** — the one platform whose
wizard is runtime-agnostic today. Feishu and WeCom remain deferred, and
this PR keeps them explicitly excluded rather than leaving it to drift.

### Scope

Frontend only (`web/app`). No backend change, no schema change, no new
endpoint — the engine `POST /agents/{workspace_id}/channels` path this
routes to already exists and is already used by the manual form. No
deploy ordering constraint; `pnpm-lock.yaml` untouched.

## Test plan

- [x] TDD. Six new assertions in
`tests/unit/app/claw-settings/ChannelsSection-engine.unit.spec.tsx`:
  - guided **and** manual method cards render for an engine Slack target
  - the wizard opens with the engine workspace as its `target`
- completion calls `onEngineAdd` with the `workspaceId`, sends **no**
`agent_id`, and does **not** call `onAdd`
- engine **Feishu and WeCom** still render no method cards (guards the
deliberate exclusion)
- the real wizard — not a stub — excludes `pairing` from its DM-policy
options
- account-id and app-name defaults derive from the selected workspace's
channels (`slack` → `slack-2`, app name suffixed off the workspace name)
- [x] One pre-existing assertion in `useAddChannelForm.unit.spec.tsx`
flipped from `guidedCapable: false` / `showAdvanced: true` to `true` /
`false`. That test encoded the old gate; the flip is an honest
re-encoding of the intended behavior change, not removed coverage. No
v1/bot expectation was altered.
- [x] `bash scripts/verify-web.sh` — **PASS** (exit 0): 7 governance
guards, `tsc`, vitest **550 files / 7404 passed / 1 skipped / 1 todo**,
eslint.
- [ ] Not exercised against a live Slack workspace. The meaningful
post-deploy check is connecting Slack to an **engine** agent through the
step-by-step path and confirming a message round-trip.

## Note for reviewers

`handleAddChannel` falls back to the bot path when `onEngineAdd` is
undefined, so a missing prop would send an engine channel to the bot.
This is **pre-existing and not live** — `ChannelsPageClient` always
passes it — and is unchanged here. Flagged for awareness since the
wizard can now reach that function; worth a follow-up guard rather than
a fix in this PR.
```

### PR body

## Linear
<!-- none — surfaced from a code review of the channels page, no ticket -->

## Summary

Engine (v2) channel targets were gated out of the guided setup render path. Picking Slack for an engine workspace dropped the user straight onto two unlabeled `xoxb-…` / `xapp-…` boxes, while the same platform on a v1 bot target got the full manifest wizard with step-by-step instructions and a deep link to the Slack app console.

Two expressions in `useAddChannelForm.ts` did the gating:

```ts
const effectiveShowAdvanced = showAdvanced || isEngineTarget          // forced manual mode
guidedCapable: !isEngineTarget && flags.guidedCapable                 // killed the method cards
```

`SlackSetupWizard` is pure UI over an `onAdd` callback — no `uid`, no backend session, no v1-only endpoint — so it needed target threading rather than a rewrite.

- **`ENGINE_GUIDED_PLATFORMS`** allowlists which engine platforms get the guided method cards. **Feishu and WeCom deliberately stay on manual entry**: their guided flow is a backend QR session that resolves the target via `get_user_bot_and_token(uid)` and writes with `client.add_channel(bot_id, …)` (`openclaw_settings/feishu.py:276`, `wecom.py:194`). There is no workspace parameter anywhere in that path, so offering it for an engine target would provision the channel onto the user's **bot** instead of the selected workspace. A test pins this.
- Threads the selected target through `onSlackSetup` → `ChannelsSection` → `SlackSetupWizard`, so wizard completion routes to `onEngineAdd`.
- Omits `agent_id` for engine targets — engine channels have no per-channel agent binding.
- Excludes `pairing` from the engine DM-policy list; the backend rejects it with `channel.pairing_unsupported` (`engine_agent_channels_service.py:166`).
- Derives the account-id and Slack app-name defaults from the selected workspace's channels rather than the bot's.

### Relationship to the design of record

`docs/superpowers/specs/2026-07-20-engine-agent-channels-design.md` lists as a v1 non-goal:

> No QR/guided auto-provision wizard for engine Slack/Feishu/WeCom in v1 (manual entry only; the auto-provision convenience can follow later).

This is that follow-up, **for Slack only** — the one platform whose wizard is runtime-agnostic today. Feishu and WeCom remain deferred, and this PR keeps them explicitly excluded rather than leaving it to drift.

### Scope

Frontend only (`web/app`). No backend change, no schema change, no new endpoint — the engine `POST /agents/{workspace_id}/channels` path this routes to already exists and is already used by the manual form. No deploy ordering constraint; `pnpm-lock.yaml` untouched.

## Test plan

- [x] TDD. Six new assertions in `tests/unit/app/claw-settings/ChannelsSection-engine.unit.spec.tsx`:
  - guided **and** manual method cards render for an engine Slack target
  - the wizard opens with the engine workspace as its `target`
  - completion calls `onEngineAdd` with the `workspaceId`, sends **no** `agent_id`, and does **not** call `onAdd`
  - engine **Feishu and WeCom** still render no method cards (guards the deliberate exclusion)
  - the real wizard — not a stub — excludes `pairing` from its DM-policy options
  - account-id and app-name defaults derive from the selected workspace's channels (`slack` → `slack-2`, app name suffixed off the workspace name)
- [x] One pre-existing assertion in `useAddChannelForm.unit.spec.tsx` flipped from `guidedCapable: false` / `showAdvanced: true` to `true` / `false`. That test encoded the old gate; the flip is an honest re-encoding of the intended behavior change, not removed coverage. No v1/bot expectation was altered.
- [x] `bash scripts/verify-web.sh` — **PASS** (exit 0): 7 governance guards, `tsc`, vitest **550 files / 7404 passed / 1 skipped / 1 todo**, eslint.
- [ ] Not exercised against a live Slack workspace. The meaningful post-deploy check is connecting Slack to an **engine** agent through the step-by-step path and confirming a message round-trip.

## Note for reviewers

`handleAddChannel` falls back to the bot path when `onEngineAdd` is undefined, so a missing prop would send an engine channel to the bot. This is **pre-existing and not live** — `ChannelsPageClient` always passes it — and is unchanged here. Flagged for awareness since the wizard can now reach that function; worth a follow-up guard rather than a fix in this PR.

