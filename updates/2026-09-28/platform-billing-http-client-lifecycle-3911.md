---
title: "修复：开发者平台账单页在并发请求下返回 500，钱包与流水读取恢复正常"
type: "Bug Fix"
priority: "高"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 修复：开发者平台账单页在并发请求下返回 500，钱包与流水读取恢复正常

## 核心宣传点

此前只要有另一个账单请求先把共享的 HTTP 连接打开，开发者平台的账单页就会直接 500。根因是性能治理那次改动把取连接的方法改成返回共享连接后，平台侧的几个方法还在用「每次重新打开」的写法，对一个已经打开的连接再打开会直接抛错。现在平台的钱包余额和流水读取改为复用共享连接、不再重开也不关闭它；建客户和提交积分这两个写操作各自持有独立连接并关掉长连接复用，传输层失败绝不重放，避免重复扣款或重复入账。

## 分级

- 内部：P0
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

Fix staging Platform Billing returning HTTP 500 after another Billing request opens the shared HTTP client. Platform wallet and ledger reads now reuse the client without reopening or closing it. Customer ensure and credit submission use independent clients with keepalive disabled; mutation transport failures are never replayed.

## Root cause

The Platform methods retained `async with self._get_client()` after #3885 changed `_get_client()` to return the shared GET client. An already-open client raises `RuntimeError: Cannot open a client instance more than once`. The old transport test replaced `_get_client()` with a new client on every call and missed this integration bug.

## Test plan

- [x] Added regressions that fail on the previous code with the staging exception (5 failed), then pass with this fix.
- [x] Warm the shared client through a normal Billing read, then interleave repeated concurrent Platform wallet/ledger reads with ordinary reads; verify the pool remains open until shutdown.
- [x] Verify both Platform writes use independent clients, close on success and lost responses, make one POST only, and leave the shared read client usable.
- [x] Route/payload test now preserves the real `_get_client()` behavior and replaces only HTTP transport.
- [x] 73 targeted Billing and Platform tests passed.
- [x] Final-commit `bash scripts/verify-py.sh --full` executed: all static/architecture/duplication checks passed; 12,753 tests passed, 5 skipped.
- [x] Coverage is 89.77% overall and 100% for the changed production module; it passes the existing CI threshold of 89.5%. The local verify script still hardcodes 90%, so its final exit code is 1 solely for that stale threshold. This PR does not change any coverage threshold.

Backend-only change. A claw-interface staging deployment is required for the browser fix to take effect.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `233cc0248b1de9fef07fea5bed93370bae6c2664`
- PR: #3911
- 作者：finn-srp
- 日期：2026-09-28T10:20:53Z

### Commit Message

```
fix(platform): respect billing HTTP client lifecycle (#3911)

## Summary

Fix staging Platform Billing returning HTTP 500 after another Billing
request opens the shared HTTP client. Platform wallet and ledger reads
now reuse the client without reopening or closing it. Customer ensure
and credit submission use independent clients with keepalive disabled;
mutation transport failures are never replayed.

## Root cause

The Platform methods retained `async with self._get_client()` after
#3885 changed `_get_client()` to return the shared GET client. An
already-open client raises `RuntimeError: Cannot open a client instance
more than once`. The old transport test replaced `_get_client()` with a
new client on every call and missed this integration bug.

## Test plan

- [x] Added regressions that fail on the previous code with the staging
exception (5 failed), then pass with this fix.
- [x] Warm the shared client through a normal Billing read, then
interleave repeated concurrent Platform wallet/ledger reads with
ordinary reads; verify the pool remains open until shutdown.
- [x] Verify both Platform writes use independent clients, close on
success and lost responses, make one POST only, and leave the shared
read client usable.
- [x] Route/payload test now preserves the real `_get_client()` behavior
and replaces only HTTP transport.
- [x] 73 targeted Billing and Platform tests passed.
- [x] Final-commit `bash scripts/verify-py.sh --full` executed: all
static/architecture/duplication checks passed; 12,753 tests passed, 5
skipped.
- [x] Coverage is 89.77% overall and 100% for the changed production
module; it passes the existing CI threshold of 89.5%. The local verify
script still hardcodes 90%, so its final exit code is 1 solely for that
stale threshold. This PR does not change any coverage threshold.

Backend-only change. A claw-interface staging deployment is required for
the browser fix to take effect.
```

来源：SerendipityOneInc/ecap-workspace @ 233cc024，PR #3911，作者 finn-srp。
