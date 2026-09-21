---
title: "fix(billing): recognize Stripe scheduled cancellation dates (#3828)"
type: "Bug Fix"
priority: "高"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# 修复：Stripe 里预约取消的订阅会被正确识别

## 核心宣传点

在 Stripe 的 Customer Portal 里预约取消时，可能只设置了 cancel_at 而 cancel_at_period_end 仍然是 false。之前这类订阅即使 webhook 已经处理成功，系统仍然当成会继续续费，用户在账单页看到的状态是错的。现在会识别 cancel_at 这种预约取消日期，订阅状态和到期时间显示与 Stripe 一致。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已合并待发版

## PR 说明

## Summary
Stripe Customer Portal can schedule cancellation using `cancel_at` while leaving `cancel_at_period_end=false`. ZooWork previously treated these subscriptions as renewing even after successfully processing the webhook.

Normalize cancellation within the current billing period across webhook, paid-invoice, replacement, and reconciliation projections. Paid access remains available until the existing period ends. Cancel dates beyond the current period do not suppress intervening renewals. Resuming a custom scheduled cancellation now clears `cancel_at`; the existing end-of-period path continues to clear `cancel_at_period_end`.

## Root cause
The adapter only inspected the boolean flag. The staging subscription reproduced the issue with an active status, a cancellation timestamp matching its period end, and a false boolean flag. The update webhook was received and processed successfully.

Stripe reference: https://docs.stripe.com/billing/subscriptions/cancel#custom-cancel-date

## Test plan
- [x] 92 relevant unit tests passed; 5 pre-existing removed-trial tests skipped.
- [x] Regression cases cover Portal payloads, current-state retrieval on webhook, cancellation removal, reconciliation identity, paid-invoice projection, resume, and downgrade.
- [x] Ruff, formatting, Pyright, and import boundary checks.
- [ ] Deploy backend and retest cancellation/resume in staging. Existing affected agreements require a new provider update or reconciliation after deployment.

No schema, database query, frontend, or billing-gateway changes. The Stripe endpoint must subscribe to `customer.subscription.updated` (already enabled for the staging endpoint during diagnosis).


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8ce092eaa404d054254470ce30b030a3c72d3ce5`
- PR: #3828
- 作者：sam-srp
- 日期：2026-09-20T14:42:46Z

### Commit Message

```
fix(billing): recognize Stripe scheduled cancellation dates (#3828)

## Summary
Stripe Customer Portal can schedule cancellation using `cancel_at` while
leaving `cancel_at_period_end=false`. ZooWork previously treated these
subscriptions as renewing even after successfully processing the
webhook.

Normalize cancellation within the current billing period across webhook,
paid-invoice, replacement, and reconciliation projections. Paid access
remains available until the existing period ends. Cancel dates beyond
the current period do not suppress intervening renewals. Resuming a
custom scheduled cancellation now clears `cancel_at`; the existing
end-of-period path continues to clear `cancel_at_period_end`.

## Root cause
The adapter only inspected the boolean flag. The staging subscription
reproduced the issue with an active status, a cancellation timestamp
matching its period end, and a false boolean flag. The update webhook
was received and processed successfully.

Stripe reference:
https://docs.stripe.com/billing/subscriptions/cancel#custom-cancel-date

## Test plan
- [x] 92 relevant unit tests passed; 5 pre-existing removed-trial tests
skipped.
- [x] Regression cases cover Portal payloads, current-state retrieval on
webhook, cancellation removal, reconciliation identity, paid-invoice
projection, resume, and downgrade.
- [x] Ruff, formatting, Pyright, and import boundary checks.
- [ ] Deploy backend and retest cancellation/resume in staging. Existing
affected agreements require a new provider update or reconciliation
after deployment.

No schema, database query, frontend, or billing-gateway changes. The
Stripe endpoint must subscribe to `customer.subscription.updated`
(already enabled for the staging endpoint during diagnosis).
```

来源：SerendipityOneInc/ecap-workspace @ 8ce092ea，PR #3828，作者 sam-srp。