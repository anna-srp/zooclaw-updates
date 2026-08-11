---
title: "修复：WhatsApp 只收到半截回复；新增「正在输入」提示"
type: "Bug Fix"
priority: "高"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 修复：WhatsApp 只收到半截回复；新增「正在输入」提示

## 核心宣传点

WhatsApp 此前会把流式生成的第一个片段（如 "N"、"Your"）当成正式回复发出，现在只发送完整的最终回复；同时在 Agent 思考时显示「正在输入…」，不再是长时间空白等待。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `0901f9eca0363da1e66e0672790a6066a41f868a`
- PR: #3308

### Commit Message

```
fix(whatsapp): deliver only final agent replies and show typing indicator (#3308)

## Summary
- Skip the engine's streaming **preview** posts in Mattermost→WhatsApp
outbound delivery, so WhatsApp users receive only final reply posts
instead of a truncated first fragment ("N", "Your", …).
- Send Meta's official [typing
indicator](https://developers.facebook.com/docs/whatsapp/cloud-api/typing-indicators/)
(which also marks the inbound message read) once an inbound message is
committed to Mattermost on the routable path, so the user sees "typing…"
while the agent generates instead of dead air.

## Root cause
The engine streams each reply into Mattermost via the Engine v2
preview-post protocol: a `posted` event creates a nearly-empty preview
post (measured first frame: 1 char; props `openclaw_streaming: "true"` /
`openclaw_stream_state: "preview"`), ~50 `post_edited` events grow it in
place (~74 chars / 1.24 s), then the final full message arrives as new
`posted` post(s) and the preview is deleted (protocol measured in
`docs/superpowers/specs/2026-07-21-chat-streaming-smoothness.md`).

The bridge (`src/mattermost-outbound.ts`) forwards every non-inbound
`posted` event and ignores `post_edited`/`post_deleted` — so WhatsApp
received the preview's first frame as a permanent message (WhatsApp
messages cannot be edited). When the user replied mid-stream the turn
aborted, the final post never arrived, and the fragment was all they
ever got.

The new filter mirrors the two existing consumers of the same contract:
claw-interface `_is_preview_post`
(`app/services/agent_builder_service.py:1628`) and the web client's
`isStreamingPreview` (`src/hooks/chat/useMmTypewriter.ts:91`). Comparing
**values** (not prop presence) is load-bearing: final posts carry the
same prop names with values `"false"` / `"final"` (v2 staging capture:
`docs/staging-validation/2026-07-31-v2-main-agent-model-and-stream-error-report.md`).

## Test plan
- [x] `pnpm typecheck` clean in `services/whatsapp-business-service`
- [x] `pnpm test` clean — 87/87 across 6 files (11 new tests)
- [x] `pnpm build` clean
- New unit coverage:
- preview post via `openclaw_streaming: "true"` → skipped (reason
`streaming_preview`), no resolve/send
  - preview post via `openclaw_stream_state: "preview"` → skipped
- regression guard: final post with `{openclaw_streaming: "false",
openclaw_stream_state: "final"}` → delivered
- typing indicator request shape (`status: "read"` + inbound
`message_id` + `typing_indicator: {type: "text"}`) on the routable path
- typing-indicator failure does not affect the webhook response; no
indicator on canned-reply paths
- Staging: send a WhatsApp message to the oura_ring number; verify the
reply arrives once, complete, with a typing indicator while generating.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

## Summary
- Skip the engine's streaming **preview** posts in Mattermost→WhatsApp outbound delivery, so WhatsApp users receive only final reply posts instead of a truncated first fragment ("N", "Your", …).
- Send Meta's official [typing indicator](https://developers.facebook.com/docs/whatsapp/cloud-api/typing-indicators/) (which also marks the inbound message read) once an inbound message is committed to Mattermost on the routable path, so the user sees "typing…" while the agent generates instead of dead air.

## Root cause
The engine streams each reply into Mattermost via the Engine v2 preview-post protocol: a `posted` event creates a nearly-empty preview post (measured first frame: 1 char; props `openclaw_streaming: "true"` / `openclaw_stream_state: "preview"`), ~50 `post_edited` events grow it in place (~74 chars / 1.24 s), then the final full message arrives as new `posted` post(s) and the preview is deleted (protocol measured in `docs/superpowers/specs/2026-07-21-chat-streaming-smoothness.md`).

The bridge (`src/mattermost-outbound.ts`) forwards every non-inbound `posted` event and ignores `post_edited`/`post_deleted` — so WhatsApp received the preview's first frame as a permanent message (WhatsApp messages cannot be edited). When the user replied mid-stream the turn aborted, the final post never arrived, and the fragment was all they ever got.

The new filter mirrors the two existing consumers of the same contract: claw-interface `_is_preview_post` (`app/services/agent_builder_service.py:1628`) and the web client's `isStreamingPreview` (`src/hooks/chat/useMmTypewriter.ts:91`). Comparing **values** (not prop presence) is load-bearing: final posts carry the same prop names with values `"false"` / `"final"` (v2 staging capture: `docs/staging-validation/2026-07-31-v2-main-agent-model-and-stream-error-report.md`).

## Test plan
- [x] `pnpm typecheck` clean in `services/whatsapp-business-service`
- [x] `pnpm test` clean — 87/87 across 6 files (11 new tests)
- [x] `pnpm build` clean
- New unit coverage:
  - preview post via `openclaw_streaming: "true"` → skipped (reason `streaming_preview`), no resolve/send
  - preview post via `openclaw_stream_state: "preview"` → skipped
  - regression guard: final post with `{openclaw_streaming: "false", openclaw_stream_state: "final"}` → delivered
  - typing indicator request shape (`status: "read"` + inbound `message_id` + `typing_indicator: {type: "text"}`) on the routable path
  - typing-indicator failure does not affect the webhook response; no indicator on canned-reply paths
- Staging: send a WhatsApp message to the oura_ring number; verify the reply arrives once, complete, with a typing indicator while generating.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

