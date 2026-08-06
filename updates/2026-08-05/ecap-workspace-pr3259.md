---
title: "会话回复等待时立即显示「停止」"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 会话回复等待时立即显示「停止」

## 核心宣传点

在会话里发出消息后立刻就能看到「停止」按钮，不用等状态回传才出现。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`f3839cb8066f518caba71edbe94145406dffc75d`
- 作者：kaka-srp
- 日期：2026-08-05T11:20:59Z
- PR：#3259

### Commit Message

```
fix(chat): expose stop while session reply is pending (#3259)

## Summary

- Mark the Mattermost channel as waiting as soon as a standalone
session-thread reply starts, so the composer immediately replaces Send
with Stop.
- Clear the optimistic waiting state when the post fails; hidden
button-generated `/stop` behavior is unchanged.
- Reuse the existing Mattermost waiting state and timeout without adding
network requests, polling, or persistence.

## Root cause

The v2 session-thread route sends replies through a standalone
Mattermost API client instead of the shared `sendMessage` path. That
bypassed the existing `markUserSent` transition, so `isGenerating` could
remain false until a later turn-status event and the composer kept
showing a disabled Send button rather than Stop.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to the changed hook,
Mattermost state/provider, and related unit tests
- [x] TypeScript type-check
- [x] ESLint and web governance guards
- [x] 261 related Vitest tests
- [x] Local code review completed

## Review follow-up

- Fixed the verified cross-channel races reported by Codex review:
delayed failures cancel only their own channel's timeout, and channel
navigation no longer drops another pending reply's fallback cleanup.
- Waiting fallbacks are now independently scoped by Mattermost channel,
including concurrent pending replies and inactive-channel bot posts.

## Performance

No additional API, database, or polling work. The change performs
existing in-memory waiting-state updates only. Concurrent pending
channels can each hold one existing 60-second fallback timer, which is
cleared on reply, failure, timeout, reset, or unmount.
```

### PR Body

## Summary

- Mark the Mattermost channel as waiting as soon as a standalone session-thread reply starts, so the composer immediately replaces Send with Stop.
- Clear the optimistic waiting state when the post fails; hidden button-generated `/stop` behavior is unchanged.
- Reuse the existing Mattermost waiting state and timeout without adding network requests, polling, or persistence.

## Root cause

The v2 session-thread route sends replies through a standalone Mattermost API client instead of the shared `sendMessage` path. That bypassed the existing `markUserSent` transition, so `isGenerating` could remain false until a later turn-status event and the composer kept showing a disabled Send button rather than Stop.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to the changed hook, Mattermost state/provider, and related unit tests
- [x] TypeScript type-check
- [x] ESLint and web governance guards
- [x] 261 related Vitest tests
- [x] Local code review completed

## Review follow-up

- Fixed the verified cross-channel races reported by Codex review: delayed failures cancel only their own channel's timeout, and channel navigation no longer drops another pending reply's fallback cleanup.
- Waiting fallbacks are now independently scoped by Mattermost channel, including concurrent pending replies and inactive-channel bot posts.

## Performance

No additional API, database, or polling work. The change performs existing in-memory waiting-state updates only. Concurrent pending channels can each hold one existing 60-second fallback timer, which is cleared on reply, failure, timeout, reset, or unmount.

