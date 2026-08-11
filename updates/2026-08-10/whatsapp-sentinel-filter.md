---
title: "修复：WhatsApp 每次回复后多出一条 NO_REPLY 消息"
type: "Bug Fix"
priority: "高"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 修复：WhatsApp 每次回复后多出一条 NO_REPLY 消息

## 核心宣传点

WhatsApp 用户在每条正常回复之后会额外收到一条 "NO_REPLY" 系统噪声消息，现已彻底过滤干净。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `9f5da286799faf35dba50e8481bf14a1c0bc56ba`
- PR: #3309

### Commit Message

```
fix(whatsapp): filter engine sentinel acks from WhatsApp outbound delivery (#3309)

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary
- Skip standalone `NO_REPLY` / `HEARTBEAT_OK` sentinel posts in
Mattermost→WhatsApp outbound delivery, reported as a new
`sentinel_message` result reason. The check runs before the Claw
Interface target resolve, so pure-sentinel posts make zero network
calls.
- Strip a glued trailing sentinel token (`"reply text\nNO_REPLY"`) from
otherwise-real replies before sending to WhatsApp, mirroring the web
client's `stripSentinelTokens`.

## Root cause
The engine's agent policy ends turns with a literal `NO_REPLY` post when
the real reply was already delivered via the message tool (and heartbeat
runs post `HEARTBEAT_OK`). Both existing user-facing surfaces filter
these sentinels — web chat (`web/app/src/lib/chat/message-filters.ts`)
and chat replay
(`services/claw-interface/app/services/chat_replay/visibility.py`) — but
the WhatsApp bridge forwarded every non-empty, non-preview bot post, so
WhatsApp users received a separate "NO_REPLY" message alongside every
agent reply.

Before #3308 the sentinel was buried in streaming-preview fragment
noise; with previews filtered it arrives whole on every turn, which is
the "extra NO_REPLY message" users now see.

The new `SENTINEL_SUFFIX_RE` in `mattermost-outbound.ts` is the same
expression the web client uses, so all three surfaces share one
filtering contract.

## Test plan
- [x] `pnpm typecheck` — clean
- [x] `pnpm test` — 92/92 passing; 5 new cases in
`mattermost-outbound.test.ts`: standalone `NO_REPLY`, whitespace-padded
`NO_REPLY \n`, and standalone `HEARTBEAT_OK` all return
`sentinel_message` with no fetch calls; a trailing glued token is
stripped from the delivered Graph API body; text where the token is not
a trailing suffix is delivered unchanged
- Live dev/staging validation intentionally not run — code-only
verification requested for this change

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Fable 5 <noreply@anthropic.com>
```

### PR Body

<!-- PR 标题：fix(scope): description —— 必须遵循 Conventional Commits -->

## Summary
- Skip standalone `NO_REPLY` / `HEARTBEAT_OK` sentinel posts in Mattermost→WhatsApp outbound delivery, reported as a new `sentinel_message` result reason. The check runs before the Claw Interface target resolve, so pure-sentinel posts make zero network calls.
- Strip a glued trailing sentinel token (`"reply text\nNO_REPLY"`) from otherwise-real replies before sending to WhatsApp, mirroring the web client's `stripSentinelTokens`.

## Root cause
The engine's agent policy ends turns with a literal `NO_REPLY` post when the real reply was already delivered via the message tool (and heartbeat runs post `HEARTBEAT_OK`). Both existing user-facing surfaces filter these sentinels — web chat (`web/app/src/lib/chat/message-filters.ts`) and chat replay (`services/claw-interface/app/services/chat_replay/visibility.py`) — but the WhatsApp bridge forwarded every non-empty, non-preview bot post, so WhatsApp users received a separate "NO_REPLY" message alongside every agent reply.

Before #3308 the sentinel was buried in streaming-preview fragment noise; with previews filtered it arrives whole on every turn, which is the "extra NO_REPLY message" users now see.

The new `SENTINEL_SUFFIX_RE` in `mattermost-outbound.ts` is the same expression the web client uses, so all three surfaces share one filtering contract.

## Test plan
- [x] `pnpm typecheck` — clean
- [x] `pnpm test` — 92/92 passing; 5 new cases in `mattermost-outbound.test.ts`: standalone `NO_REPLY`, whitespace-padded `NO_REPLY \n`, and standalone `HEARTBEAT_OK` all return `sentinel_message` with no fetch calls; a trailing glued token is stripped from the delivered Graph API body; text where the token is not a trailing suffix is delivered unchanged
- Live dev/staging validation intentionally not run — code-only verification requested for this change

🤖 Generated with [Claude Code](https://claude.com/claude-code)

