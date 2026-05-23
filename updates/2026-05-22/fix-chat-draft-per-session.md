---
title: "修复聊天草稿混乱：不同 Agent 对话的草稿不再互相覆盖"
type: "Bug Fix"
priority: "中"
date: "2026-05-22"
status: "待审核"
channels: ""
---

# 修复聊天草稿混乱：不同 Agent 对话的草稿不再互相覆盖

## 核心宣传点

修复了切换不同 Agent 时聊天输入框草稿互相覆盖的问题，现在每个 Agent 对话都有独立的草稿保存，不会丢失正在输入的内容。

## 原始内容

**Commit**: c41cbef9b77919d1b57ce8cb4c6b0af93013e922
**Author**: Chris@ZooClaw
**Date**: 2026-05-22T11:27:31Z
**PR**: #1853

### Commit Message
```
fix(chat): scope chat input draft by agent session (ECA-727) (#1853)

Linear:
https://linear.app/srpone/issue/ECA-727/web-切换-agent-时输入框内容被带到新-agent-会话

## Summary

The desktop chat composer persisted its draft keyed by `userId` only, so
a half-typed message under Agent A would resurface in Agent B's input
after switching — the message thread itself remounts cleanly on agent
boundary (`AssistantRuntimeProvider key={sessionKey}` in
`ChatBody.tsx`), but the composer kept reading from the same uid-only
`sessionStorage` slot.

Fix: rename the helper to
`STORAGE_KEYS.CHAT_INPUT_DRAFT_FOR_SESSION(uid, sessionId)` and feed in
the `sessionId` prop that was already wired into `GenClawInput` for
uploads / SSE. The existing `useEffect` watching `draftStorageKey`
re-reads `sessionStorage` whenever the key changes, so:

- Switching to a different Agent now shows that Agent's slot (empty or
its own prior draft).
- Switching back restores the original Agent's draft from its own slot.
- Same-Agent refresh / unmount / remount keeps the draft, as before.

No migration: stale uid-only `sessionStorage` entries from prior
versions are simply ignored (sessionStorage is per-tab anyway, so the
blast radius is "one draft lost on the first switch after deploy").

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit tests/unit/app/chat/GenClawInput.unit.spec.tsx` —
51/51 pass
- [x] Falsifiability proof: reverted the storage helper to uid-only and
re-ran — both new regression tests fail with the expected leak messages
("legacy uid-only leak" and "main draft" appearing in input after
switch). Restored, tests green.

## Regression tests added

1. `ignores the pre-fix uid-only draft key shape so old leaked drafts
cannot resurface` — seeds the literal `ecap:chat:input-draft:user-1` key
(what pre-fix code wrote), renders with `sessionId='main'`, asserts
input is empty.
2. `swaps and restores the visible draft when sessionId changes between
agents` — types under `main`, switches to `agent:foo:main` (expects
empty), types under foo, switches back to `main` (expects original draft
restored), asserts both `sessionStorage` slots remain independently
populated.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description
Linear: https://linear.app/srpone/issue/ECA-727/web-切换-agent-时输入框内容被带到新-agent-会话

## Summary

The desktop chat composer persisted its draft keyed by `userId` only, so a half-typed message under Agent A would resurface in Agent B's input after switching — the message thread itself remounts cleanly on agent boundary (`AssistantRuntimeProvider key={sessionKey}` in `ChatBody.tsx`), but the composer kept reading from the same uid-only `sessionStorage` slot.

Fix: rename the helper to `STORAGE_KEYS.CHAT_INPUT_DRAFT_FOR_SESSION(uid, sessionId)` and feed in the `sessionId` prop that was already wired into `GenClawInput` for uploads / SSE. The existing `useEffect` watching `draftStorageKey` re-reads `sessionStorage` whenever the key changes, so:

- Switching to a different Agent now shows that Agent's slot (empty or its own prior draft).
- Switching back restores the original Agent's draft from its own slot.
- Same-Agent refresh / unmount / remount keeps the draft, as before.

No migration: stale uid-only `sessionStorage` entries from prior versions are simply ignored (sessionStorage is per-tab anyway, so the blast radius is "one draft lost on the first switch after deploy").

## Test plan

- [x] `npx tsc --noEmit` — clean
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit tests/unit/app/chat/GenClawInput.unit.spec.tsx` — 51/51 pass
- [x] Falsifiability proof: reverted the storage helper to uid-only and re-ran — both new regression tests fail with the expected leak messages ("legacy uid-only leak" and "main draft" appearing in input after switch). Restored, tests green.

## Regression tests added

1. `ignores the pre-fix uid-only draft key shape so old leaked drafts cannot resurface` — seeds the literal `ecap:chat:input-draft:user-1` key (what pre-fix code wrote), renders with `sessionId='main'`, asserts input is empty.
2. `swaps and restores the visible draft when sessionId changes between agents` — types under `main`, switches to `agent:foo:main` (expects empty), types under foo, switches back to `main` (expects original draft restored), asserts both `sessionStorage` slots remain independently populated.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

