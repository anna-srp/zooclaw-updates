---
title: "修复：网络抖动或刷新被打断时不再把已登录用户踢回登录页"
type: "Bug Fix"
priority: "高"
date: "2026-10-01"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：网络抖动或刷新被打断时不再把已登录用户踢回登录页

## 核心宣传点

开发者平台原先只要账号恢复请求失败就会清掉已保存的会话，结果刷新被打断、网络故障、请求超时或响应体异常这些情况，都会把本来登录正常的用户直接甩回登录页。现在这些可恢复的失败不再清除会话，登录状态能稳定保留。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

Platform currently clears its saved session whenever the account restoration request rejects. Interrupted refreshes, network failures, timeouts, and invalid response bodies can therefore send a signed-in user back to the login page.

Preserve credentials on recoverable failures and show a shared recovery screen at the original route. Only explicit logout, expiry, or confirmed Account authentication errors clear the session and private cache.

## Root cause and changes

- Replace the catch-all logout handler with explicit signed-out, restoring, authenticated, and recovery-error states. Business bootstrap remains gated until `/user/me` verifies the identity.
- Manage restoration with TanStack Query, forward cancellation to fetch, time out requests after 8 seconds, and retry network/timeout/5xx failures once. Manual retries honor browser-readable `Retry-After` headers.
- Recognize Account's existing authentication `403` detail responses while preserving unknown `403` errors. Business API permission errors do not trigger logout.
- Give each in-memory session a non-secret query ID and guard pending login attempts against logout/unmount. Seed the verified login result to avoid a duplicate `/user/me` request.
- Extend the shared Account client with optional cancellation and error metadata while retaining existing call signatures.

Preserve the Console UI and sign-in changes from #3978. The merged login page keeps the recovery gate; PreviewAuthProvider now implements the expanded auth contract, and recovery route tests include the new InterfaceProvider and Account Settings path.

No backend or storage migration is required.

## Test plan

- [x] Node 24: Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (127 tests), `pnpm build` against the resolved merge with current main.
- [x] Auth client `pnpm test` (48 tests) and `pnpm lint`.
- [x] Main web app `pnpm test:unit` (11,124 passed; 70 skipped; 1 todo).
- [x] Regression coverage for network, cancellation, timeout, server/response errors, unknown and recognized 403s, expiry, offline reconnect, rate limiting, StrictMode remounts, and stale restoration/login results.
- [x] Local Chromium with mocked Account/business endpoints: 25 rapid reloads while account requests were pending retained credentials and did not start business bootstrap. Network, timeout, unknown 403, and Retry-After recovered at the original URL; recognized authentication 403 cleared the session. No live business requests or writes were made.

Deployment and verification against the hosted staging site remain pending.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `73cffba7f42e83be29c269cfa8e03d88ca11ef86`
- PR: #3979
- 作者：finn-srp
- 日期：2026-10-01T10:38:33Z

### Commit Message

```
fix(platform): preserve sessions during interrupted restoration (#3979)

## Summary

Platform currently clears its saved session whenever the account
restoration request rejects. Interrupted refreshes, network failures,
timeouts, and invalid response bodies can therefore send a signed-in
user back to the login page.

Preserve credentials on recoverable failures and show a shared recovery
screen at the original route. Only explicit logout, expiry, or confirmed
Account authentication errors clear the session and private cache.

## Root cause and changes

- Replace the catch-all logout handler with explicit signed-out,
restoring, authenticated, and recovery-error states. Business bootstrap
remains gated until `/user/me` verifies the identity.
- Manage restoration with TanStack Query, forward cancellation to fetch,
time out requests after 8 seconds, and retry network/timeout/5xx
failures once. Manual retries honor browser-readable `Retry-After`
headers.
- Recognize Account's existing authentication `403` detail responses
while preserving unknown `403` errors. Business API permission errors do
not trigger logout.
- Give each in-memory session a non-secret query ID and guard pending
login attempts against logout/unmount. Seed the verified login result to
avoid a duplicate `/user/me` request.
- Extend the shared Account client with optional cancellation and error
metadata while retaining existing call signatures.

Preserve the Console UI and sign-in changes from #3978. The merged login
page keeps the recovery gate; PreviewAuthProvider now implements the
expanded auth contract, and recovery route tests include the new
InterfaceProvider and Account Settings path.

No backend or storage migration is required.

## Test plan

- [x] Node 24: Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (127
tests), `pnpm build` against the resolved merge with current main.
- [x] Auth client `pnpm test` (48 tests) and `pnpm lint`.
- [x] Main web app `pnpm test:unit` (11,124 passed; 70 skipped; 1 todo).
- [x] Regression coverage for network, cancellation, timeout,
server/response errors, unknown and recognized 403s, expiry, offline
reconnect, rate limiting, StrictMode remounts, and stale
restoration/login results.
- [x] Local Chromium with mocked Account/business endpoints: 25 rapid
reloads while account requests were pending retained credentials and did
not start business bootstrap. Network, timeout, unknown 403, and
Retry-After recovered at the original URL; recognized authentication 403
cleared the session. No live business requests or writes were made.

Deployment and verification against the hosted staging site remain
pending.
```

来源：SerendipityOneInc/ecap-workspace @ 73cffba7，PR #3979，作者 finn-srp。
