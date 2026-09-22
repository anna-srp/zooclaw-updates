---
title: "fix(billing): remove unused Airwallex pricing and report payment failures (#3831)"
type: "产品基础功能更新"
priority: "低"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 清理未使用的 Airwallex 价格配置，并补齐支付失败上报

## 核心宣传点

新购买已经全部走 Stripe，但后端还强制要求配置两项没用的 Airwallex USD30 设置，这次删掉，同时移除未使用的渠道价格查询和结账校验器，恢复原有的历史价格映射。另一半是可观测性：前端的目录、订单、结账、门户、订阅管理和发票失败现在都会带上操作名、用户标识以及可得的订单/会话/渠道标识上报；后端则对 webhook 处理、积分发放、订阅操作、对账和退款重试开启白名单内的支付事件上报。上报会剥掉任意渠道载荷和凭据，嵌套异常和前端重复事件都会去重，并且监控本身失败不会影响原来的支付结果、错误和重试。历史 Airwallex USD20 的首付、续费、试用结算和预约降级取消继续支持，支付与订阅业务规则没有变化。

## 分级

- 内部：P2
- 外部：C
- 发布状态：已上线

## PR 说明

## Summary
New purchases are Stripe-only, but the backend still required unused Airwallex USD30 settings. Payment failures also had gaps in explicit Sentry reporting, especially catalog/checkout requests and caught reconciliation or refund failures.

- Remove the two Airwallex USD30 settings and unused provider-price lookup/checkout validator; restore the original historical price mappings and update their regression tests.
- Report frontend catalog, order, checkout, portal, subscription management, and invoice failures with operation, UID and available order/session/provider identifiers.
- Enable allowlisted backend payment Sentry events for webhook processing, credit fulfillment, subscription operations, reconciliation, and refund retries. Retain existing confirmation monitoring.
- Strip arbitrary provider payloads/credentials; deduplicate nested backend exceptions and repeated frontend incidents. Monitoring failures preserve the original payment results, errors, and retries. Reuse existing Sentry DSNs without adding environment variables.

Historical Airwallex USD20 first payments, renewals, trial settlement, and scheduled-downgrade cancellation remain supported. Payment and subscription business rules are unchanged.

## Validation
- Airwallex cleanup regression suite: 686 unique cases passing after updating the obsolete fixture.
- Payment monitoring and billing regressions: 219 distinct backend cases passed across focused suites, including the final 34-case monitor/refund rerun. Five existing cases skipped.
- Frontend focused suite: 69 passed, including catalog/order/checkout/navigation failure reporting and unchanged retry behavior.
- Backend ruff, formatting, pyright and import contracts passed; frontend governance guards, TypeScript and targeted ESLint passed.
- No deployment or live Sentry delivery verification performed.


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `112fcc76ce03ba9e0db253d8979db2ce6f8dac81`
- PR: #3831
- 作者：sam-srp
- 日期：2026-09-21T03:56:26Z

### Commit Message

```
fix(billing): remove unused Airwallex pricing and report payment failures (#3831)

## Summary
New purchases are Stripe-only, but the backend still required unused
Airwallex USD30 settings. Payment failures also had gaps in explicit
Sentry reporting, especially catalog/checkout requests and caught
reconciliation or refund failures.

- Remove the two Airwallex USD30 settings and unused provider-price
lookup/checkout validator; restore the original historical price
mappings and update their regression tests.
- Report frontend catalog, order, checkout, portal, subscription
management, and invoice failures with operation, UID and available
order/session/provider identifiers.
- Enable allowlisted backend payment Sentry events for webhook
processing, credit fulfillment, subscription operations, reconciliation,
and refund retries. Retain existing confirmation monitoring.
- Strip arbitrary provider payloads/credentials; deduplicate nested
backend exceptions and repeated frontend incidents. Monitoring failures
preserve the original payment results, errors, and retries. Reuse
existing Sentry DSNs without adding environment variables.

Historical Airwallex USD20 first payments, renewals, trial settlement,
and scheduled-downgrade cancellation remain supported. Payment and
subscription business rules are unchanged.

## Validation
- Airwallex cleanup regression suite: 686 unique cases passing after
updating the obsolete fixture.
- Payment monitoring and billing regressions: 219 distinct backend cases
passed across focused suites, including the final 34-case monitor/refund
rerun. Five existing cases skipped.
- Frontend focused suite: 69 passed, including
catalog/order/checkout/navigation failure reporting and unchanged retry
behavior.
- Backend ruff, formatting, pyright and import contracts passed;
frontend governance guards, TypeScript and targeted ESLint passed.
- No deployment or live Sentry delivery verification performed.
```

来源：SerendipityOneInc/ecap-workspace @ 112fcc76，PR #3831，作者 sam-srp。