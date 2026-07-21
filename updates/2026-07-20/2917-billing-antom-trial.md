---
title: "修复计费：Antom 试用转付费不再卡住权益开通"
type: "Bug Fix"
priority: "高"
date: "2026-07-20"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了通过 Antom 支付从试用转为付费时，权益可能未正确开通的问题。现在付费成功后会按可靠顺序开通会员权益，试用转付费更稳定，避免已付费却无法使用的情况。

### 原始内容

**Commit message:**

```
fix(billing): recover Antom paid trial handoff (#2917)

## Summary
- fix only the write path for new Antom trial-to-paid handoffs
- enforce the durable order: validated paid-period evidence → Billing
Gateway grant → active Entitlement → linked PaymentOrder →
active/canceling Agreement
- retry only Entitlements explicitly marked with
`trial_paid_handoff_pending`, reusing the deterministic Entitlement and
skipping a second grant once BG evidence exists
- keep due trial-boundary scheduled downgrades inside the same ordered
handoff; a downgrade scheduled after early payment reprojects the
pending Entitlement before grant
- preserve an already-recorded cancel-at-period-end state and reject
terminal Agreement/provider evidence before grant
- validate Antom ownership by subscription id, with the existing
request-id identity as the fallback

## Scope
This PR handles new webhook handoffs and their bounded idempotent retry
only.

Explicitly out of scope:
- discovering or repairing historical affected users online
- Reconcile reconstruction or expired/current=false scans
- Current Access fallbacks or diagnostics expansion
- cross-subscription replacement/cancellation changes
- synchronous provider queries

Known affected users will be handled by a one-time offline repair. No
production data was modified by this PR.

Issue: [ECA-1244](https://linear.app/srpone/issue/ECA-1244)

## Test plan
- [x] focused handoff/retry/repository suite: 139 passed
- [x] `bash scripts/verify-local.sh --py-static` (ruff, format, pyright,
import-linter)
- [x] regression coverage for early-payment pending handoff, ordered
writes, deterministic retry without regrant, later scheduled downgrade,
request-id fallback, cancel-at-period-end preservation, terminal
evidence rejection, and projection retry

---------

Co-authored-by: kaka-srp <kaka@srp.one>
```

**PR body:**

## Summary
- fix only the write path for new Antom trial-to-paid handoffs
- enforce the durable order: validated paid-period evidence → Billing Gateway grant → active Entitlement → linked PaymentOrder → active/canceling Agreement
- retry only Entitlements explicitly marked with `trial_paid_handoff_pending`, reusing the deterministic Entitlement and skipping a second grant once BG evidence exists
- keep due trial-boundary scheduled downgrades inside the same ordered handoff; a downgrade scheduled after early payment reprojects the pending Entitlement before grant
- preserve an already-recorded cancel-at-period-end state and reject terminal Agreement/provider evidence before grant
- validate Antom ownership by subscription id, with the existing request-id identity as the fallback

## Scope
This PR handles new webhook handoffs and their bounded idempotent retry only.

Explicitly out of scope:
- discovering or repairing historical affected users online
- Reconcile reconstruction or expired/current=false scans
- Current Access fallbacks or diagnostics expansion
- cross-subscription replacement/cancellation changes
- synchronous provider queries

Known affected users will be handled by a one-time offline repair. No production data was modified by this PR.

Issue: [ECA-1244](https://linear.app/srpone/issue/ECA-1244)

## Test plan
- [x] focused handoff/retry/repository suite: 139 passed
- [x] `bash scripts/verify-local.sh --py-static` (ruff, format, pyright, import-linter)
- [x] regression coverage for early-payment pending handoff, ordered writes, deterministic retry without regrant, later scheduled downgrade, request-id fallback, cancel-at-period-end preservation, terminal evidence rejection, and projection retry

