---
title: "分享的对话回放正确显示 Agent 真实头像"
type: "Bug Fix"
priority: "中"
date: "2026-07-13"
status: "待审核"
channels: ""
---

## 核心宣传点

修复分享对话回放时头像丢失、显示默认品牌头像的问题，现在能正确展示 Agent 真实头像。

## 原始内容

### [ecap-workspace] fix(chat-replay): preserve agent avatars in shared replays (#2826)
SHA: 92c9f12df5b12d504365208fb476f6966577abe1 | PR #2826 | 2026-07-13T03:17:47Z

**Commit message:**
```
fix(chat-replay): preserve agent avatars in shared replays (#2826)

## Summary

- Preserve the real agent avatar when sharing replays from the main chat
and session thread.
- Fall back to the ownership-validated `AgentWorkspace.avatar_url` for
legacy clients, loading races, and Agent Builder shares.
- Keep client-provided identity avatars as the highest priority and
handle the 1024-character avatar URL limit consistently.

## Root cause

Replay snapshots only persisted `resolvedChatIdentity.avatar`. When that
value had not loaded yet, the live chat could still render
`activeAgentAvatarUrl`, but replay creation stored no avatar and the
public viewer fell back to the default brand avatar. The backend already
resolved the owning workspace but discarded its avatar URL.

Existing immutable replay snapshots are unchanged; newly created shares
use the corrected avatar resolution.

Linear:
https://linear.app/srpone/issue/ECA-1214/agent-%E5%88%86%E4%BA%AB-replay-%E7%9A%84%E5%A4%B4%E5%83%8F%E6%94%B9%E6%88%90%E7%9C%9F%E5%AE%9E-agent-%E5%A4%B4%E5%83%8F

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Targeted frontend Vitest: 3 files, 88 tests passed
- [x] `pytest -q
services/claw-interface/tests/unit/test_chat_replay_create.py`: 36
passed
- [x] Commit and pre-push hooks: frontend lint/typecheck and backend
Ruff/Pyright/import contracts passed
```
**PR body:**

## Summary

- Preserve the real agent avatar when sharing replays from the main chat and session thread.
- Fall back to the ownership-validated `AgentWorkspace.avatar_url` for legacy clients, loading races, and Agent Builder shares.
- Keep client-provided identity avatars as the highest priority and handle the 1024-character avatar URL limit consistently.

## Root cause

Replay snapshots only persisted `resolvedChatIdentity.avatar`. When that value had not loaded yet, the live chat could still render `activeAgentAvatarUrl`, but replay creation stored no avatar and the public viewer fell back to the default brand avatar. The backend already resolved the owning workspace but discarded its avatar URL.

Existing immutable replay snapshots are unchanged; newly created shares use the corrected avatar resolution.

Linear: https://linear.app/srpone/issue/ECA-1214/agent-%E5%88%86%E4%BA%AB-replay-%E7%9A%84%E5%A4%B4%E5%83%8F%E6%94%B9%E6%88%90%E7%9C%9F%E5%AE%9E-agent-%E5%A4%B4%E5%83%8F

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] Targeted frontend Vitest: 3 files, 88 tests passed
- [x] `pytest -q services/claw-interface/tests/unit/test_chat_replay_create.py`: 36 passed
- [x] Commit and pre-push hooks: frontend lint/typecheck and backend Ruff/Pyright/import contracts passed

