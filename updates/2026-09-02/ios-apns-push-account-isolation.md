---
title: "修复：iPhone 上切换账号后，推送还会串到上一个账号"
type: "Bug Fix"
priority: "高"
date: "2026-09-02"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：iPhone 上切换账号后，推送还会串到上一个账号

## 核心宣传点

同一台 iPhone、同一个 App 安装只有一个 APNs 推送令牌。以前客户端把这个令牌单独缓存下来，只要令牌没变就跳过注册——于是在设备上退出旧账号、登录新账号后，令牌仍然挂在旧账号名下，推送会继续按旧身份投递。

现在推送注册按「身份三元组」缓存（令牌 + ECAP uid + Mattermost 用户 id），存进新的 Keychain 记录 `mm_push_registration.v2`，旧的只存令牌的缓存会被删除，保证它再也无法满足跳过检查；换账号时令牌会在新用户名下重新注册一次。

注册时机也提前了：以前要等 WebSocket 连上才注册，凭证有效但机器人连不上的账号就一直注册不上；现在 Mattermost 令牌校验通过后就用服务端权威的用户 id 立刻注册，失败最多重试 3 次并带短退避，只有成功才落盘。退出登录时会在旧凭证还有效的窗口内尽力调用一次禁用推送的接口（2 秒超时，4xx 视为服务端不支持），再断连并清掉本地注册记录；这一步失败绝不会阻塞退出登录。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `e2688c2af518ca076b1ce5a51e3adb4632415659`
- PR: #3621
- 作者: bill-srp
- 日期: 2026-09-02T10:24:23Z

### Commit Message

```
fix(ios): stop APNs pushes leaking across signed-in accounts (#3621)

## Summary
- Cache the APNs push registration as an identity tuple (`tokenHex` +
ECAP uid + Mattermost user id) in a new Keychain record
(`mm_push_registration.v2`), deleting the legacy token-only cache so it
can never satisfy the skip check; switching accounts on the same device
now re-registers the token under the new Mattermost user.
- Register the device token immediately after Mattermost token
validation succeeds (using the server-authoritative user id) instead of
waiting for the WebSocket to reach connected; accounts with valid
credentials but no connectable bot now still validate and register.
Registration retries up to 3 times with short backoff, and only persists
the record on success.
- On sign-out, while the old credentials are still valid, make a
best-effort `PUT /api/v4/users/sessions/device` with
`device_notification_disabled: "true"` (2s timeout; 4xx treated as
server-unsupported) before disconnecting and clearing the local
registration record. Failures never block sign-out.

## Root cause
One iPhone/app install shares a single APNs token across every signed-in
ECAP account, but Mattermost delivers pushes per logical user: it reads
that user's sessions and sends to each saved DeviceId. ZooClaw cached
only the bare token hex, so after an account switch the "token
unchanged, skipping registration" guard left the token bound to the
previous account's session — and sign-out only cleared local state,
never the server-side DeviceId. Registration was also gated behind
WebSocket connect (and skipped entirely for no-bot accounts), so some
accounts never claimed the token at all while a stale account kept
receiving that phone's notifications.

Client-side fix covers normal sign-in/sign-out flows. Repairing
already-leaked tokens (kill/uninstall/legacy cases) needs a backend
token-owner registry — tracked as a follow-up phase.

## Test plan
- [x] New/updated Swift Testing coverage: identity-tuple skip vs.
re-register on ECAP-uid or MM-user change, no persistence on failure +
bounded retry, legacy key migration/cleanup, disable-device API payload
and 4xx compatibility, no-bot validation ordering, sign-out disables
device notifications before dropping credentials and survives a failing
disable call
- [x] Full simulator suite: 892/892 passed (`xcodebuild test`, iPhone 17
Pro)
- [x] `swiftlint --strict`: 0 violations
```

### PR Body

```
## Summary
- Cache the APNs push registration as an identity tuple (`tokenHex` + ECAP uid + Mattermost user id) in a new Keychain record (`mm_push_registration.v2`), deleting the legacy token-only cache so it can never satisfy the skip check; switching accounts on the same device now re-registers the token under the new Mattermost user.
- Register the device token immediately after Mattermost token validation succeeds (using the server-authoritative user id) instead of waiting for the WebSocket to reach connected; accounts with valid credentials but no connectable bot now still validate and register. Registration retries up to 3 times with short backoff, and only persists the record on success.
- On sign-out, while the old credentials are still valid, make a best-effort `PUT /api/v4/users/sessions/device` with `device_notification_disabled: "true"` (2s timeout; 4xx treated as server-unsupported) before disconnecting and clearing the local registration record. Failures never block sign-out.

## Root cause
One iPhone/app install shares a single APNs token across every signed-in ECAP account, but Mattermost delivers pushes per logical user: it reads that user's sessions and sends to each saved DeviceId. ZooClaw cached only the bare token hex, so after an account switch the "token unchanged, skipping registration" guard left the token bound to the previous account's session — and sign-out only cleared local state, never the server-side DeviceId. Registration was also gated behind WebSocket connect (and skipped entirely for no-bot accounts), so some accounts never claimed the token at all while a stale account kept receiving that phone's notifications.

Client-side fix covers normal sign-in/sign-out flows. Repairing already-leaked tokens (kill/uninstall/legacy cases) needs a backend token-owner registry — tracked as a follow-up phase.

## Test plan
- [x] New/updated Swift Testing coverage: identity-tuple skip vs. re-register on ECAP-uid or MM-user change, no persistence on failure + bounded retry, legacy key migration/cleanup, disable-device API payload and 4xx compatibility, no-bot validation ordering, sign-out disables device notifications before dropping credentials and survives a failing disable call
- [x] Full simulator suite: 892/892 passed (`xcodebuild test`, iPhone 17 Pro)
- [x] `swiftlint --strict`: 0 violations

```

