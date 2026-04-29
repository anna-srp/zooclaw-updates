---
title: "修复：聊天回放中 Bot 名称显示不正确"
type: "Bug Fix"
priority: "低"
date: "2026-04-28"
status: "待审核"
channels: ""
---

# 修复：聊天回放中 Bot 名称显示不正确

## 核心宣传点

修复了聊天回放页面中 Bot 显示名称与实际聊天页面不一致的问题。

## 原始内容

**Commit**: `08ef4009b73f93115356981ccc77331f4e87c912`
**仓库**: ecap-workspace
**作者**: kaka-srp
**时间**: 2026-04-28T06:25:01Z

### 完整 Commit Message

```
fix(chat-replay): use chat-page identity for replay bot name (#1429)

## Summary

Replay viewers were seeing the bot's frozen MM `display_name`, which can
diverge from what the creator sees in chat. Chat-page identity
resolution factors in **user identity**, **per-agent settings** and
**locale** (via
[`resolveChatIdentity`](web/src/lib/chat/chatIdentity.ts#L34)) — none of
which the backend has direct access to. For renamed bots, customized
user identity, or non-English locales, replay would show a different
name than chat.

## Changes

### Backend
-
[`_resolve_bot()`](services/claw-interface/app/services/chat_replay/create.py#L289):
flip priority so `client_snapshot_meta.bot_name` wins, with user-doc
`display_name` as fallback for legacy clients and ``"Assistant"`` as
terminal fallback. Whitespace-only client names treated as empty.
-
[`ClientSnapshotMeta`](services/claw-interface/app/schema/chat_replay.py#L164):
add Pydantic `max_length` caps (name 80, avatar URL 1024, emoji 64, path
512) — schema-layer 422 is cheaper than service-layer guards. Updated
docstring to reflect display-only role.

### Frontend
-
[`GenClawClient.tsx`](web/src/app/[locale]/chat/GenClawClient.tsx#L567):
plumb `resolvedChatIdentity.{name,avatar}` through `useChatReplayShare`
so the snapshot captures the same string the creator sees.
- Relocated `shareFlow` and its `createError` toast effect to after
`resolvedChatIdentity` is computed (TS scoping).

## Trust model

`client_snapshot_meta.bot_name` is **display-only** metadata — it does
not affect channel ownership, post visibility, or file proxying (all
enforced server-side from refetched MM data). The creator owns the share
and is trusted to label it; length caps limit blast radius.

## Test plan

- [x] 5 new backend tests cover priority flip, fallback chain,
whitespace handling, and length-cap enforcement
- [x] `pytest tests/unit/test_chat_replay_create.py` — 22/22 passing
locally
- [x] All 6 `scripts/ci-lint/0?-*.sh` clean (file-length, import-linter,
complexity, deptry, collection-strings, repo-sync)
- [x] `pnpm tsc --noEmit` and `pnpm eslint GenClawClient.tsx` clean
- [ ] After merge: smoke-test on staging by creating a share with a
renamed bot or non-English locale and confirming the public viewer shows
the same name as chat
```

### PR #1429 完整描述

## Summary

Replay viewers were seeing the bot's frozen MM `display_name`, which can diverge from what the creator sees in chat. Chat-page identity resolution factors in **user identity**, **per-agent settings** and **locale** (via [`resolveChatIdentity`](web/src/lib/chat/chatIdentity.ts#L34)) — none of which the backend has direct access to. For renamed bots, customized user identity, or non-English locales, replay would show a different name than chat.

## Changes

### Backend
- [`_resolve_bot()`](services/claw-interface/app/services/chat_replay/create.py#L289): flip priority so `client_snapshot_meta.bot_name` wins, with user-doc `display_name` as fallback for legacy clients and ``"Assistant"`` as terminal fallback. Whitespace-only client names treated as empty.
- [`ClientSnapshotMeta`](services/claw-interface/app/schema/chat_replay.py#L164): add Pydantic `max_length` caps (name 80, avatar URL 1024, emoji 64, path 512) — schema-layer 422 is cheaper than service-layer guards. Updated docstring to reflect display-only role.

### Frontend
- [`GenClawClient.tsx`](web/src/app/[locale]/chat/GenClawClient.tsx#L567): plumb `resolvedChatIdentity.{name,avatar}` through `useChatReplayShare` so the snapshot captures the same string the creator sees.
- Relocated `shareFlow` and its `createError` toast effect to after `resolvedChatIdentity` is computed (TS scoping).

## Trust model

`client_snapshot_meta.bot_name` is **display-only** metadata — it does not affect channel ownership, post visibility, or file proxying (all enforced server-side from refetched MM data). The creator owns the share and is trusted to label it; length caps limit blast radius.

## Test plan

- [x] 5 new backend tests cover priority flip, fallback chain, whitespace handling, and length-cap enforcement
- [x] `pytest tests/unit/test_chat_replay_create.py` — 22/22 passing locally
- [x] All 6 `scripts/ci-lint/0?-*.sh` clean (file-length, import-linter, complexity, deptry, collection-strings, repo-sync)
- [x] `pnpm tsc --noEmit` and `pnpm eslint GenClawClient.tsx` clean
- [ ] After merge: smoke-test on staging by creating a share with a renamed bot or non-English locale and confirming the public viewer shows the same name as chat
