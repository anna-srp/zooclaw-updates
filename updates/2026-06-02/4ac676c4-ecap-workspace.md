---
title: "[平台] reload subagent chat history after reconnect"
type: "Bug Fix"
priority: "中"
date: "2026-06-02"
status: "待审核"
channels: ""
---
# [平台] reload subagent chat history after reconnect

## 核心宣传点
来自 ecap-workspace 仓库的更新：fix(web): reload subagent chat history after reconnect

## 原始内容
**Commit**: 4ac676c4a24453082bb7d69312f5289754d9d51f
**Title**: fix(web): reload subagent chat history after reconnect (#2152)
**Author**: sharplee-srp
**Date**: 2026-06-02T13:00:24Z

**PR**: #2152

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

