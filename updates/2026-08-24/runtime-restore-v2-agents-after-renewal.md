---
title: "修复：订阅续费后 v2 Agent 不会自动恢复，仍处于停用状态"
type: "Bug Fix"
priority: "高"
date: "2026-08-24"
status: "待审核"
channels: ""
---

# 修复：订阅续费后 v2 Agent 不会自动恢复，仍处于停用状态

## 核心宣传点

订阅到期时系统会停掉 Engine v2 工作空间、关掉定时任务和已绑定的消息渠道；但续费成功后，额度、模型权限都恢复了，Agent 却仍旧躺在停用状态，需要人工介入。现在续费后系统会按停用时保存的快照精确恢复：只把当初因到期而关掉的生命周期状态、定时任务和渠道重新打开，不会误开用户自己关掉的东西。同时补齐了中途崩溃、回调丢失等异常情况的重试与续期机制，人工审核、团队/企业和历史 FastClaw 资源不受影响。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `2ba43d8ce927824ec5b7a7ffbd0ea724a8c90a54`
- PR: #3491
- 作者: kaka-srp
- 日期: 2026-08-24T08:06:54Z

### Commit Message

```
fix(runtime): restore v2 agents after subscription renewal (#3491)

## Summary

- restore subscription-expired Engine v2 workspaces when effective
personal subscription access returns
- persist cleanup provenance for lifecycle state, enabled schedules, and
enabled channels so recovery restores only state disabled by expiry
- resume stale expiry cleanup while access remains absent, preventing
crashed cleanup attempts from leaving runtime triggers active
- scan non-restorable stale cleanup rows without allowing them into
inverse recovery
- fence and renew cleanup/recovery leases between bounded remote calls
- reconcile missed callbacks and crashed cleanup/recovery attempts with
bounded retry scheduling
- preserve Engine startup semantics where `desired_state=running`,
`render_ok=true`, and `actual_state=activating` is a successful accepted
start
- keep manual-review, team-org, enterprise handoff, and legacy FastClaw
resources outside destructive personal-expiry reconciliation

## Root cause

Subscription expiry correctly stopped Engine lifecycle execution,
disabled ACS channels and user schedules, and marked Engine workspaces
disabled. Billing v2 renewal fulfillment restored entitlement, credits,
model access, and resource class, but it had no inverse operation for
the v2 runtime cleanup. The account therefore became entitled while its
Engine workspace remained disabled.

The fix records a durable cleanup snapshot before remote mutation and
restores it after access returns. Cleanup and recovery use independent
renewable leases, handle stale or unleased `suspending` rows, capture
shared migrated Computer lifecycle intent before any stop, and defer
failed eligibility lookups so one owner cannot starve the bounded
reconciler page. If access is confirmed `EXPIRED` or `FREE/NONE` in the
same current personal org, reconciliation resumes strict expiry cleanup
before deferring completed recovery candidates. Ambiguous/manual-review
access and org mismatches never enter destructive cleanup.

The affected production user was restored manually before this code is
deployed.

## Test plan

- [x] 103 focused unit tests covering cleanup, recovery, billing
fulfillment, enterprise handoff, scheduler, repository fencing, indexes,
manual-review/team guards, non-restorable stale cleanup, and lost-lease
behavior
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] independent agent review after each correction: no remaining P0-P2
findings
```

### PR Body

## Summary

- restore subscription-expired Engine v2 workspaces when effective personal subscription access returns
- persist cleanup provenance for lifecycle state, enabled schedules, and enabled channels so recovery restores only state disabled by expiry
- resume stale expiry cleanup while access remains absent, preventing crashed cleanup attempts from leaving runtime triggers active
- scan non-restorable stale cleanup rows without allowing them into inverse recovery
- fence and renew cleanup/recovery leases between bounded remote calls
- reconcile missed callbacks and crashed cleanup/recovery attempts with bounded retry scheduling
- preserve Engine startup semantics where `desired_state=running`, `render_ok=true`, and `actual_state=activating` is a successful accepted start
- keep manual-review, team-org, enterprise handoff, and legacy FastClaw resources outside destructive personal-expiry reconciliation

## Root cause

Subscription expiry correctly stopped Engine lifecycle execution, disabled ACS channels and user schedules, and marked Engine workspaces disabled. Billing v2 renewal fulfillment restored entitlement, credits, model access, and resource class, but it had no inverse operation for the v2 runtime cleanup. The account therefore became entitled while its Engine workspace remained disabled.

The fix records a durable cleanup snapshot before remote mutation and restores it after access returns. Cleanup and recovery use independent renewable leases, handle stale or unleased `suspending` rows, capture shared migrated Computer lifecycle intent before any stop, and defer failed eligibility lookups so one owner cannot starve the bounded reconciler page. If access is confirmed `EXPIRED` or `FREE/NONE` in the same current personal org, reconciliation resumes strict expiry cleanup before deferring completed recovery candidates. Ambiguous/manual-review access and org mismatches never enter destructive cleanup.

The affected production user was restored manually before this code is deployed.

## Test plan

- [x] 103 focused unit tests covering cleanup, recovery, billing fulfillment, enterprise handoff, scheduler, repository fencing, indexes, manual-review/team guards, non-restorable stale cleanup, and lost-lease behavior
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`
- [x] independent agent review after each correction: no remaining P0-P2 findings


