---
title: "修复：Agent Builder 偶发卡死 / 工作区被长期占用，并支持测试时切换模型"
type: "Bug Fix"
priority: "中"
date: "2026-08-10"
status: "待审核"
channels: ""
---

# 修复：Agent Builder 偶发卡死 / 工作区被长期占用，并支持测试时切换模型

## 核心宣传点

解决了 Agent Builder 并发操作时工作区被锁住、对话卡住无法继续的问题；同时在测试 Agent 时可以自行选择模型。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `a7d7cc5ca1876aa22d0ac188fb8530e7a5cfb9e7`
- PR: #3320

### Commit Message

```
fix(agent-builder): guard v2 initialization and test models (#3320)

## Summary

- serialize all Agent Builder v2 workspace mutations with one
server-authoritative, fenced lease per shared Builder runtime
- require a confirmed activation before turns, keep uncertain mutations
fail-closed, and reconcile only ambiguous turn posts from Mattermost's
authoritative thread state
- make turn stop/finish/recovery transitions atomic, including
cross-project page acquisition and concurrent stop dispatch
- keep the turn POST path bounded and let the client reconcile a
timed-out response by `pending_post_id`
- add Engine v2 Test Agent model selection with project/test-run-scoped
authorization
- keep the legacy v1 route, Model API, and backend runtime unchanged

## Root cause

The previous v2 lock mixed page ownership and background mutations
without a single fenced operation state. That allowed
initialization/renewal races, synchronous activation in the turn
request, and ambiguous Mattermost POST failures that could either
release too early or leave the shared workspace permanently locked. Test
Agent model selection also lacked an API scoped to the hidden Pack Test
workspace.

## Recovery policy

- explicit validation/rejection: release the operation
- uncertain activate/package/runtime mutation: retain
`recovery_required`
- uncertain turn POST: persist `pending_post_id`, read the authoritative
Mattermost thread, and use an exact operation/fence CAS
  - terminal matching post: release
- active matching post: bind its real post id and retain recovery
ownership
- no matching post: release only after the post timeout plus a
conservative 60-second grace
- unreadable/malformed thread or concurrent stop dispatch: make no
change

## Validation

- Agent Builder backend unit suite: 386 passed
- Mattermost client unit suite: 41 passed
- focused frontend unit suite: 131 passed across 7 files
- Ruff formatting/lint, Pyright, targeted ESLint/TypeScript, import
lint, and complexity gate
- `git diff --check`

## Size override justification

This is one cohesive concurrency correction across the lease schema,
Mongo CAS transitions, route/service handoff, client reconciliation, and
behavioral race tests. Splitting it would leave intermediate PRs with
incompatible state transitions or unprotected callers. The
implementation itself remains scoped to Agent Builder v2; the extra
lines are primarily explicit race coverage, and v1 is unchanged.
```

### PR Body

## Summary

- serialize all Agent Builder v2 workspace mutations with one server-authoritative, fenced lease per shared Builder runtime
- require a confirmed activation before turns, keep uncertain mutations fail-closed, and reconcile only ambiguous turn posts from Mattermost's authoritative thread state
- make turn stop/finish/recovery transitions atomic, including cross-project page acquisition and concurrent stop dispatch
- keep the turn POST path bounded and let the client reconcile a timed-out response by `pending_post_id`
- add Engine v2 Test Agent model selection with project/test-run-scoped authorization
- keep the legacy v1 route, Model API, and backend runtime unchanged

## Root cause

The previous v2 lock mixed page ownership and background mutations without a single fenced operation state. That allowed initialization/renewal races, synchronous activation in the turn request, and ambiguous Mattermost POST failures that could either release too early or leave the shared workspace permanently locked. Test Agent model selection also lacked an API scoped to the hidden Pack Test workspace.

## Recovery policy

- explicit validation/rejection: release the operation
- uncertain activate/package/runtime mutation: retain `recovery_required`
- uncertain turn POST: persist `pending_post_id`, read the authoritative Mattermost thread, and use an exact operation/fence CAS
  - terminal matching post: release
  - active matching post: bind its real post id and retain recovery ownership
  - no matching post: release only after the post timeout plus a conservative 60-second grace
  - unreadable/malformed thread or concurrent stop dispatch: make no change

## Validation

- Agent Builder backend unit suite: 386 passed
- Mattermost client unit suite: 41 passed
- focused frontend unit suite: 131 passed across 7 files
- Ruff formatting/lint, Pyright, targeted ESLint/TypeScript, import lint, and complexity gate
- `git diff --check`

## Size override justification

This is one cohesive concurrency correction across the lease schema, Mongo CAS transitions, route/service handoff, client reconciliation, and behavioral race tests. Splitting it would leave intermediate PRs with incompatible state transitions or unprotected callers. The implementation itself remains scoped to Agent Builder v2; the extra lines are primarily explicit race coverage, and v1 is unchanged.

