---
title: "修复：高负载下登录校验、订阅状态与 Builder 轮询的重复请求大幅减少"
type: "Bug Fix"
priority: "中"
date: "2026-09-24"
status: "待审核"
channels: ""
---

# 修复：高负载下登录校验、订阅状态与 Builder 轮询的重复请求大幅减少

## 核心宣传点

一轮针对 CPU 负载放大的治理，用户侧的体感是高峰期不再那么容易卡顿或偶发失败。同一个 token 的并发缓存穿透在单进程内被合并成一次验证，某个调用方断开不会把其他等待者的验证一起取消，验证失败也不写缓存。订阅状态判定只把 Billing Gateway 明确的 400 且 detail.error == "no_active_subscription" 当作「确实没有权益」，其他失败保留原状并给延迟重查加抖动、恢复日志做聚合，避免把网络抖动误判成掉权益。Builder 线程读取失败后会退避、读成功后重置，同一帖子在单进程内不会起重复的监控。Billing 客户端只在 GET 请求上复用共享连接并随应用关闭一起释放，GET 在连接类错误上重试一次；全部 12 个写操作入口仍然各自持有客户端并关掉 keepalive，传输层失败绝不会导致写请求被重放。这条也一并合入并取代了 #3878 的 auth single-flight 改动。

## 分级

- 内部：P1
- 外部：C
- toB 相关：否
- 发布状态：已上线

## PR 说明

## Summary

Reduce duplicate authentication, recovery and Builder polling work while preserving normal billing behavior. This PR includes the auth single-flight change from #3878, which it supersedes.

- Coalesce concurrent cache misses for the same token within one process. A disconnected caller cannot cancel verification for other waiters; failed verifications are not cached.
- Classify only Billing Gateway's exact `400` / `detail.error == "no_active_subscription"` response as a settled absence of access. Preserve other failures, jitter deferred rechecks and aggregate recovery logs.
- Back off failed Builder thread reads, reset backoff after successful reads and prevent duplicate monitors for the same post within one process.
- Reuse a shared Billing client **only for GET requests**, and close it through application shutdown. GET retries once on connection failures, `RemoteProtocolError`, `ReadError` or `WriteError`.
- Keep all 12 Billing mutation entry points on caller-owned clients with keepalive disabled. Existing HTTP-status retries and compatibility fallbacks remain unchanged; transport failures never introduce a mutation replay.

## Review fixes

The latest P1/P2 findings identified two genuine gaps in the previous revision:

1. Sharing idle connections with non-idempotent writes introduced peer-disconnect failures. Writes now use fresh connections, including attempts within existing status-code retry loops, avoiding the need to guess whether a failed write executed upstream.
2. GET disconnect retries omitted `ReadError` and `WriteError`. Both are now covered by the existing one-retry limit; cancellation and repeated failures still propagate.

No payment, subscription, authorization or quota API contract was changed. The existing HTTP client library is retained; an aiohttp migration is outside this repair.

## Validation

- 804 relevant billing, model-catalog and recovery tests passed.
- `bash scripts/verify-py.sh` passed: Ruff, formatting, Pyright and all 8 import contracts.
- Regression coverage checks all 12 mutation entry points, client closure, no mutation transport replay, bounded GET retries and cancellation.
- Real loopback TCP test confirms GET reuse and distinct connections for writes, including an existing HTTP 500 retry.
- The repaired working tree was exercised against real staging dependencies under source fingerprint `PR-working-fix-e8e9ae419c6e`:
  - 44/44 query requests succeeded. At concurrency 30, one actual upstream auth call and P95 3817.47 ms.
  - Builder creation, both runtime-recovery paths and actual post-recovery conversations succeeded.
  - Two actual Billing duplicate-wallet POST requests returned the expected 409s on two independent connections; both clients closed, wallet inventory remained unchanged, and surrounding GETs reused one connection.
  - Temporary subscription/free-access expiry changes were restored. The test project was archived and cleaned; the original six instances remained running.

[Staging report](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/cpu-remediation-followup/docs/validation/2026-09-24-pr3885/rerun-after-review-fix.md) · [Sanitized measurements and source hashes](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/cpu-remediation-followup/docs/validation/2026-09-24-pr3885/rerun-after-review-fix.json)

Staging validation used isolated processes loading the changed modules over the deployed staging image, not a deployment of the complete PR image. No production mutation or deployment was performed. Wallet-conflict checks are not successful topup/payment-flow validation.

## Remaining validation limits

- Full-image deployment, startup/shutdown lifecycle, browser flows, successful topup and payment callbacks were not exercised in the staging run.
- No-entitlement/no-credit behavior and transport-fault paths have unit/local fault-injection evidence, not complete live failure scenarios.
- The shared GET pool retains default capacity (100 total / 20 keepalive); production peak capacity and CPU improvements remain unmeasured. The staging concurrency sample is not a performance benchmark.
- Cross-process deduplication, progressive recovery intervals, incremental thread reads and request-scoped read deduplication remain outside scope.

Deploy `claw-interface` after merge. New-commit CI and review results are authoritative and must settle before merge.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `500f68e29a1ccea9334fbb9132b96a8dae18780c`
- PR: #3885
- 作者：tim-srp
- 日期：2026-09-24T07:10:07Z

### Commit Message

```
fix(perf): cut CPU-load amplification across auth, recovery, builder and billing (#3885)

## Summary

Reduce duplicate authentication, recovery and Builder polling work while
preserving normal billing behavior. This PR includes the auth
single-flight change from #3878, which it supersedes.

- Coalesce concurrent cache misses for the same token within one
process. A disconnected caller cannot cancel verification for other
waiters; failed verifications are not cached.
- Classify only Billing Gateway's exact `400` / `detail.error ==
"no_active_subscription"` response as a settled absence of access.
Preserve other failures, jitter deferred rechecks and aggregate recovery
logs.
- Back off failed Builder thread reads, reset backoff after successful
reads and prevent duplicate monitors for the same post within one
process.
- Reuse a shared Billing client **only for GET requests**, and close it
through application shutdown. GET retries once on connection failures,
`RemoteProtocolError`, `ReadError` or `WriteError`.
- Keep all 12 Billing mutation entry points on caller-owned clients with
keepalive disabled. Existing HTTP-status retries and compatibility
fallbacks remain unchanged; transport failures never introduce a
mutation replay.

## Review fixes

The latest P1/P2 findings identified two genuine gaps in the previous
revision:

1. Sharing idle connections with non-idempotent writes introduced
peer-disconnect failures. Writes now use fresh connections, including
attempts within existing status-code retry loops, avoiding the need to
guess whether a failed write executed upstream.
2. GET disconnect retries omitted `ReadError` and `WriteError`. Both are
now covered by the existing one-retry limit; cancellation and repeated
failures still propagate.

No payment, subscription, authorization or quota API contract was
changed. The existing HTTP client library is retained; an aiohttp
migration is outside this repair.

## Validation

- 804 relevant billing, model-catalog and recovery tests passed.
- `bash scripts/verify-py.sh` passed: Ruff, formatting, Pyright and all
8 import contracts.
- Regression coverage checks all 12 mutation entry points, client
closure, no mutation transport replay, bounded GET retries and
cancellation.
- Real loopback TCP test confirms GET reuse and distinct connections for
writes, including an existing HTTP 500 retry.
- The repaired working tree was exercised against real staging
dependencies under source fingerprint `PR-working-fix-e8e9ae419c6e`:
- 44/44 query requests succeeded. At concurrency 30, one actual upstream
auth call and P95 3817.47 ms.
- Builder creation, both runtime-recovery paths and actual post-recovery
conversations succeeded.
- Two actual Billing duplicate-wallet POST requests returned the
expected 409s on two independent connections; both clients closed,
wallet inventory remained unchanged, and surrounding GETs reused one
connection.
- Temporary subscription/free-access expiry changes were restored. The
test project was archived and cleaned; the original six instances
remained running.

[Staging
report](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/cpu-remediation-followup/docs/validation/2026-09-24-pr3885/rerun-after-review-fix.md)
· [Sanitized measurements and source
hashes](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/cpu-remediation-followup/docs/validation/2026-09-24-pr3885/rerun-after-review-fix.json)

Staging validation used isolated processes loading the changed modules
over the deployed staging image, not a deployment of the complete PR
image. No production mutation or deployment was performed.
Wallet-conflict checks are not successful topup/payment-flow validation.

## Remaining validation limits

- Full-image deployment, startup/shutdown lifecycle, browser flows,
successful topup and payment callbacks were not exercised in the staging
run.
- No-entitlement/no-credit behavior and transport-fault paths have
unit/local fault-injection evidence, not complete live failure
scenarios.
- The shared GET pool retains default capacity (100 total / 20
keepalive); production peak capacity and CPU improvements remain
unmeasured. The staging concurrency sample is not a performance
benchmark.
- Cross-process deduplication, progressive recovery intervals,
incremental thread reads and request-scoped read deduplication remain
outside scope.

Deploy `claw-interface` after merge. New-commit CI and review results
are authoritative and must settle before merge.

---------

Co-authored-by: chris-srp <chris@srp.one>
```

来源：SerendipityOneInc/ecap-workspace @ 500f68e2，PR #3885，作者 tim-srp。