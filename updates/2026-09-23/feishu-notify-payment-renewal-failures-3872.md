---
title: "内部：Stripe 充值/订阅支付与自动续费失败时推送飞书通知"
type: "新功能上线"
priority: "中"
date: "2026-09-23"
status: "内部-跳过"
channels: ""
---

# 内部：Stripe 充值/订阅支付与自动续费失败时推送飞书通知

## 核心宣传点

新增仅针对 Stripe 的飞书通知：充值或订阅支付失败、自动续费尝试失败时告警。Antom 和 Airwallex 不变。通知会把签名校验过的失败事件与本地的渠道、环境、身份核对过的账单事实关联起来，同时兼容老版和新版发票的订阅引用方式，并对事件重放做去重（不会把真正的新一次失败误当重放吞掉）。属于内部运营告警，用户侧无感知。

## 分级

- 内部：P1
- 外部：内部
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
- Add Stripe-only Feishu notifications for failed top-up/subscription payments and automatic renewal attempts. Antom and Airwallex are unchanged.
- Correlate signed failure events with local provider/environment/identity-checked billing facts. Support legacy and modern invoice subscription references; deduplicate event replays without suppressing a new failed attempt.
- Keep all notification-only lookups and rendering in the existing capped background queue, with a 5-second preparation deadline and the existing 5-second HTTP deadline. Notification errors never change billing state or webhook responses.
- Update Stripe setup documentation. Cards explicitly describe an attempt failure rather than final subscription termination.

## Test plan
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8 import contracts passed.
- [x] 183 focused Feishu/Stripe tests passed, including 48 new async-preparation and Stripe failure cases.
- [x] Independent specification and code-quality reviews passed; original notification regression tests passed.
- [x] CI backend suite: 12,221 passed, 5 skipped; coverage 89.77% (89.5% gate).
- [x] Both automated reviewers approved with no correctness findings.
- [ ] GitHub still reports `python-duplication-check` in progress, although all its steps completed successfully and its parent Code Quality workflow concluded success. Waiting on final check-state synchronization; not claiming all PR checks are green yet.
- Local validation limits: the untouched `test_stripe_billing_v2.py` crashes local Python 3.12.3 even during standalone compilation; that file is deferred to CI. Coverage-instrumented local collection also fails in the existing `AppSettings` initialization (`is_instance_of`), while the same focused tests pass without coverage. No runtime/dependency or old test changes are bundled.
- No real payments or live Feishu sends were performed.

## Review disposition
- Kept the call-site `notification_boundary()` despite the optional simplification suggestion. It explicitly protects the payment handler if the notification entrypoint itself ever raises; a regression test injects that failure and pins the successful webhook response. No business changes were needed after review.

## Rollout / limitations
- Backend-only change; no deployment is part of this PR.
- Confirm the Stripe webhook subscribes to `payment_intent.payment_failed` and `invoice.payment_failed` and `FEISHU_NOTIFY_WEBHOOK_URL` is configured. This PR does not modify live Stripe/Vault configuration.
- Delivery is best effort: disabled/full queues and lookup/network failures may drop alerts; process restarts, multiple workers, and dedup TTL expiry may produce duplicates. Business processing remains authoritative and independent.
- No new Mongo query forms, collections, dependencies, or public APIs.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `605a9eb99865100a6e0f5e11a6ee0ae7e3e3e0ee`
- PR: #3872
- 作者：tim-srp
- 日期：2026-09-23T03:33:29Z

### Commit Message

```
feat(feishu): notify Stripe payment and renewal failures (#3872)

## Summary
- Add Stripe-only Feishu notifications for failed top-up/subscription
payments and automatic renewal attempts. Antom and Airwallex are
unchanged.
- Correlate signed failure events with local
provider/environment/identity-checked billing facts. Support legacy and
modern invoice subscription references; deduplicate event replays
without suppressing a new failed attempt.
- Keep all notification-only lookups and rendering in the existing
capped background queue, with a 5-second preparation deadline and the
existing 5-second HTTP deadline. Notification errors never change
billing state or webhook responses.
- Update Stripe setup documentation. Cards explicitly describe an
attempt failure rather than final subscription termination.

## Test plan
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8
import contracts passed.
- [x] 183 focused Feishu/Stripe tests passed, including 48 new
async-preparation and Stripe failure cases.
- [x] Independent specification and code-quality reviews passed;
original notification regression tests passed.
- [x] CI backend suite: 12,221 passed, 5 skipped; coverage 89.77% (89.5%
gate).
- [x] Both automated reviewers approved with no correctness findings.
- [ ] GitHub still reports `python-duplication-check` in progress,
although all its steps completed successfully and its parent Code
Quality workflow concluded success. Waiting on final check-state
synchronization; not claiming all PR checks are green yet.
- Local validation limits: the untouched `test_stripe_billing_v2.py`
crashes local Python 3.12.3 even during standalone compilation; that
file is deferred to CI. Coverage-instrumented local collection also
fails in the existing `AppSettings` initialization (`is_instance_of`),
while the same focused tests pass without coverage. No
runtime/dependency or old test changes are bundled.
- No real payments or live Feishu sends were performed.

## Review disposition
- Kept the call-site `notification_boundary()` despite the optional
simplification suggestion. It explicitly protects the payment handler if
the notification entrypoint itself ever raises; a regression test
injects that failure and pins the successful webhook response. No
business changes were needed after review.

## Rollout / limitations
- Backend-only change; no deployment is part of this PR.
- Confirm the Stripe webhook subscribes to
`payment_intent.payment_failed` and `invoice.payment_failed` and
`FEISHU_NOTIFY_WEBHOOK_URL` is configured. This PR does not modify live
Stripe/Vault configuration.
- Delivery is best effort: disabled/full queues and lookup/network
failures may drop alerts; process restarts, multiple workers, and dedup
TTL expiry may produce duplicates. Business processing remains
authoritative and independent.
- No new Mongo query forms, collections, dependencies, or public APIs.
```

来源：SerendipityOneInc/ecap-workspace @ 605a9eb9，PR #3872，作者 tim-srp。