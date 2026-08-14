---
title: "微信通道掉线可一键重新授权，频道权限设置更明确"
type: "体验优化"
priority: "中"
date: "2026-08-13"
status: "待审核"
channels: ""
---

## 核心宣传点

微信通道登录过期时会明确提示「登录已失效」，并随时可以扫码重新授权恢复收发消息；Mattermost 频道的私信权限配置也统一规范，不再出现显示与实际不符。

## 原始内容

仓库：SerendipityOneInc/ecap-workspace
commit：0985af06d0ec7a100a81110e3a3bd84efd3c0726
作者：kaka-srp
日期：2026-08-13T08:31:49Z

**Commit message**

```
fix(channels): normalize access and reconnect Weixin (#3363)

## Summary

- create managed Mattermost channels with the currently supported `open`
DM policy and `allow_from=["*"]`
- reconcile existing Mattermost rows from the legacy effective-open
configuration through ACS update after a strict create conflict
- add an always-available Weixin reauthorization action for Engine
channels using the existing in-place QR refresh flow
- pass through ACS `status_code`; display the explicit “login expired”
prompt only when ACS reports `SESSION_EXPIRED`
- pair with SerendipityOneInc/agent-channel-service#72, which validates
outbound results and exposes structured gateway status

This implements the narrowed conclusions recorded on
SerendipityOneInc/agent-channel-service#53 and
SerendipityOneInc/agent-channel-service#54. Pairing, allowlist,
plugin-native command parity, directory listing, and mention aliases
remain demand-driven follow-ups.

## Root cause

Mattermost provisioning omitted DM policy fields and inherited ACS's
`pairing + ["*"]` defaults. The wildcard made the runtime effectively
open, but the persisted policy was misleading. Existing rows also
require reconciliation because ACS create is intentionally strict and
rejects configuration drift.

The Weixin provider already detects `errcode=-14` as `SESSION_EXPIRED`,
and the ECAP backend already updates an existing default channel after a
successful QR scan. Previously ACS reduced the provider status to
`health=unhealthy`, so ECAP could neither distinguish token expiry nor
explain the required action. The linked ACS PR preserves the structured
code; this PR passes it through and maps it to the user-facing
reauthorization prompt.

## Test plan

- [x] 93 related claw-interface tests passed
- [x] `bash scripts/verify-py.sh`
- [x] channel-targeted frontend suite: 19 passed
- [x] TypeScript and ESLint passed
- [x] pre-commit and pre-push changed-surface gates passed

An incidental broad Vitest selection hit one unrelated `MarkdownContent`
hydration timeout while 5,142 tests passed; the channel-targeted tests
and static gates passed, and CI remains authoritative for the full
suite.
```

**PR #3363 body**

## Summary

- create managed Mattermost channels with the currently supported `open` DM policy and `allow_from=["*"]`
- reconcile existing Mattermost rows from the legacy effective-open configuration through ACS update after a strict create conflict
- add an always-available Weixin reauthorization action for Engine channels using the existing in-place QR refresh flow
- pass through ACS `status_code`; display the explicit “login expired” prompt only when ACS reports `SESSION_EXPIRED`
- pair with SerendipityOneInc/agent-channel-service#72, which validates outbound results and exposes structured gateway status

This implements the narrowed conclusions recorded on SerendipityOneInc/agent-channel-service#53 and SerendipityOneInc/agent-channel-service#54. Pairing, allowlist, plugin-native command parity, directory listing, and mention aliases remain demand-driven follow-ups.

## Root cause

Mattermost provisioning omitted DM policy fields and inherited ACS's `pairing + ["*"]` defaults. The wildcard made the runtime effectively open, but the persisted policy was misleading. Existing rows also require reconciliation because ACS create is intentionally strict and rejects configuration drift.

The Weixin provider already detects `errcode=-14` as `SESSION_EXPIRED`, and the ECAP backend already updates an existing default channel after a successful QR scan. Previously ACS reduced the provider status to `health=unhealthy`, so ECAP could neither distinguish token expiry nor explain the required action. The linked ACS PR preserves the structured code; this PR passes it through and maps it to the user-facing reauthorization prompt.

## Test plan

- [x] 93 related claw-interface tests passed
- [x] `bash scripts/verify-py.sh`
- [x] channel-targeted frontend suite: 19 passed
- [x] TypeScript and ESLint passed
- [x] pre-commit and pre-push changed-surface gates passed

An incidental broad Vitest selection hit one unrelated `MarkdownContent` hydration timeout while 5,142 tests passed; the channel-targeted tests and static gates passed, and CI remains authoritative for the full suite.


