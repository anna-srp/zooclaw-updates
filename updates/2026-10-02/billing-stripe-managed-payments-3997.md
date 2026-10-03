---
title: "Stripe Managed Payments 接入与含税履约能力就位（默认关闭，暂不影响线上）"
type: "产品基础功能更新"
priority: "中"
date: "2026-10-02"
status: "内部-跳过"
channels: ""
---

# Stripe Managed Payments 接入与含税履约能力就位（默认关闭，暂不影响线上）

## 核心宣传点

为 Pro 月订阅和 credits 充值接入可选的 Stripe Managed Payments，并把结算改造成能正确处理税费：以前的零税校验会把带税的成功支付判为非法订单，现在结算按「标价 − 折扣 + 价外税」核对，税额单独记账，到账 credits 仍按用户购买的原始额度发放。开关 STRIPE_MANAGED_PAYMENTS_ENABLED 默认关闭，普通 Checkout 参数不变，生产路由不受影响，所以本次对用户暂时不可感知。每笔订单的 Checkout 模式会在下单前的审计 CAS 里钉死，超时、并发请求或开关变更都不会让一笔已发起的支付中途换模式。发票身份与周期校验、余额、小额延迟、支付排序、零现金保护和退款幂等全部保留，退款后税额在支付审计历史里仍可见。

## 分级

- 内部：P1
- 外部：内部
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary

Adds opt-in Stripe Managed Payments for current Pro monthly subscriptions and credit topups. Managed Checkout can add tax to a USD 30 subscription or a topup; the previous zero-tax validators rejected those successful payments. Settlement now verifies list price minus discount plus exclusive tax, records tax separately, and grants the original purchased credits.

- `STRIPE_MANAGED_PAYMENTS_ENABLED` defaults to `false`. Ordinary Checkout retains its existing parameters. Managed requests omit unsupported payment-method/invoice parameters and require tax-exclusive pricing.
- Pin each order's Checkout mode in the existing audited pre-request CAS so timeouts, concurrent requests and flag changes cannot switch an attempted payment's mode. Pre-migration uncertain requests and existing sessions keep their original behavior.
- Preserve invoice identity/period/price checks, customer balance and verified small-amount deferrals, payment ordering, zero-cash guards and refund/credit idempotency. Tax remains visible in payment audit history after refunds.

## Validation

- 769 targeted Stripe/payment tests passed; 5 existing removed-trial tests skipped.
- 95.95% combined coverage for the six Checkout/tax/settlement modules; new invoice tax parser and Checkout recovery both 100%.
- `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8 import contracts passed.
- Independent read-only code review: no confirmed blockers; added the suggested taxed full-refund/replay regression.
- Local Python 3.12.3 crashed compiling a pre-existing large test module; the same tests passed with the installed Python 3.12.9 and existing dependencies. No runtime/dependency change in this PR.

## Rollout and limits

Backend-only deployment; the default-off flag does not change production routing. Before enabling, enroll the Stripe account, configure eligible product tax codes, and ensure the existing Pro Price is explicitly `exclusive` without replacing the Price ID still used by subscriptions. Topup inline prices explicitly set `exclusive`.

Real Stripe Sandbox payment/renewal/refund/local-currency testing has **not** been performed. The runbook includes paid/zero-tax, promotion, balance, async webhook and flag rollback scenarios. The repository change only adds a nullable field equality to the existing atomic update (no new aggregation/query form); no live CSFLE validation was performed.

Disable the flag to stop new managed checkouts. Keep tax-capable fulfillment deployed while any managed subscriptions exist. Existing subscriptions are not migrated.

Design: `docs/superpowers/specs/2026-10-02-stripe-managed-payments.md`.
Runbook: `services/claw-interface/docs/stripe-credits-v1.md`.


## Follow-up review (2026-10-02)

Kept this as the sole Managed Payments PR after comparison with a separate Claude Code implementation. Commit `bfbd76bc7` preserves the legacy zero-tax contract on non-Managed top-ups and Pro renewals, while continuing to accept verified tax on Managed orders. It pins only Managed Checkout creation and tax-bearing subscription lookups to Stripe API `2026-04-22.dahlia`; the repository's Stripe SDK defaults to `2026-02-25.clover`, where the stable `managed_payments` parameter is unavailable. Ordinary Checkout and other Stripe calls keep the existing version. The flag remains default-off.

Focused regression verification after the follow-up: 547 passed, 5 skipped; Ruff, formatting, Pyright, import contracts, file-length/complexity/dead-code guards passed. Tests include SDK-level HTTP-header/body checks for the per-request version and idempotency retry, plus legacy-versus-Managed tax settlement. No live Stripe Sandbox payment has been run.

Scope: Pro subscriptions and billing-v2 credit top-ups. API Platform top-ups remain on their separate card-only path. Failed asynchronous Managed payments remain unfulfilled and pending for manual review; the buyer can create a new top-up order. The runbook no longer claims automatic handling. Before enabling, confirm Stripe account enrollment/terms, eligible tax codes for both products, the current Pro Price's exclusive tax behavior, and run the Sandbox checklist (including taxed payment, renewal, refund, and delayed-method failure). Do not enable the flag until these checks pass.

Stripe API version evidence: https://docs.stripe.com/changelog/dahlia/2026-04-22/managed-payments


## Opus 5.5 end-to-end review

Reviewed the frontend purchase action, order creation, pending-order guards, Checkout retries, webhooks, settlement and user retry path. A pending top-up does **not** prevent a new top-up order; the suggested async-failure state-machine patch was reverted as unnecessary and disproportionate. A failed delayed-payment subscription could block a new subscription order, but the current USD-only Pro Price should not expose the recurring delayed Pix/UPI methods because they require local-currency presentment and do not support Adaptive Pricing. This is a **Sandbox rollout gate**, not a verified production incident: confirm with Brazil/India test addresses that those methods are absent before enabling the flag, and do not add BRL/INR Price currency options without implementing a safe subscription-failure recovery. Opus 5.5 ran 1,726 related unit tests (5 skipped), plus backend static gates; no live Stripe calls. Details in the runbook.

Managed Payments payment-method matrix: https://docs.stripe.com/payments/managed-payments/how-it-works#payment-method-availability

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `eb9a503f1e3d1fc516ab643bf34fefaf93213b60`
- PR: #3997
- 作者：tim-srp
- 日期：2026-10-02T04:14:44Z

### Commit Message

```
feat(billing): integrate Stripe Managed Payments with tax-safe fulfillment (#3997)
```

来源：SerendipityOneInc/ecap-workspace @ eb9a503f，PR #3997，作者 tim-srp。
