---
title: "修复：网络抖一下就整页白屏，已登录用户被踢回验证页"
type: "Bug Fix"
priority: "高"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 修复：网络抖一下就整页白屏，已登录用户被踢回验证页

## 核心宣传点

之前只要账号信息刷新请求遇到一次网络抖动，整个页面就会被一块「会话校验失败」挡板替换掉，甚至直接白屏——哪怕你本来就已经登录、会话完全有效。现在这类临时性网络故障会在后台静默重试，界面照常留在你正在用的页面上；只有真正的登录过期（401/403）或账号确实没初始化好，才会拦下来让你重试。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `2b17d0f8ec7522cfea9e2176c6c21c18acd8bd90`
- PR: #3527
- 作者: sharplee-srp
- 日期: 2026-08-26T09:25:29Z

### Commit Message

```
fix(web): preserve app on transient account refresh errors (#3527)

## Summary
- Keep the current app mounted when `/account/me` has a transient
non-auth failure and a local or cached session is already usable.
- Preserve the existing Retry gate when no usable session exists or
account bootstrap remains incomplete.
- Cover both the pending transport-retry window and the exhausted
account-bootstrap path with focused regression tests.

## Root cause
`AccountSessionGate` replaced the entire app with a session-verification
error for every non-401/403 `/account/me` failure. During React Query's
automatic transport retries, the final `error` is still empty and the
active `TypeError` is exposed through `failureReason`; the gate
therefore fell through to `return null`, producing a blank screen for an
already signed-in user.

The fix only changes those non-auth paths: a pending `TypeError` retry
or another terminal non-auth failure may continue rendering when a local
or cached session is already usable, while anonymous/first-load
failures, 401/403 responses, and exhausted `account.not_found` bootstrap
retries retain the current gate behavior.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/components/AccountSessionGate.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh
web/app/src/components/AccountSessionGate.tsx
web/app/tests/unit/components/AccountSessionGate.unit.spec.tsx`
- [x] `bash scripts/verify-changed.sh`
```

### PR Description

```
## Summary
- Keep the current app mounted when `/account/me` has a transient non-auth failure and a local or cached session is already usable.
- Preserve the existing Retry gate when no usable session exists or account bootstrap remains incomplete.
- Cover both the pending transport-retry window and the exhausted account-bootstrap path with focused regression tests.

## Root cause
`AccountSessionGate` replaced the entire app with a session-verification error for every non-401/403 `/account/me` failure. During React Query's automatic transport retries, the final `error` is still empty and the active `TypeError` is exposed through `failureReason`; the gate therefore fell through to `return null`, producing a blank screen for an already signed-in user.

The fix only changes those non-auth paths: a pending `TypeError` retry or another terminal non-auth failure may continue rendering when a local or cached session is already usable, while anonymous/first-load failures, 401/403 responses, and exhausted `account.not_found` bootstrap retries retain the current gate behavior.

## Test plan
- [x] `pnpm exec vitest run tests/unit/components/AccountSessionGate.unit.spec.tsx`
- [x] `bash scripts/verify-web.sh web/app/src/components/AccountSessionGate.tsx web/app/tests/unit/components/AccountSessionGate.unit.spec.tsx`
- [x] `bash scripts/verify-changed.sh`

```
