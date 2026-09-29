---
title: "开发者平台新增组织账单：按组织查看余额与消费流水，并支持 Stripe 充值"
type: "Feature"
priority: "高"
date: "2026-09-28"
status: "待审核"
channels: ""
---

# 开发者平台新增组织账单：按组织查看余额与消费流水，并支持 Stripe 充值

## 核心宣传点

开发者平台补上了以组织为主体的账单能力：可以按组织查看余额和消费历史，并通过 Stripe Checkout 给组织钱包充值。充值订单和支付事件落在平台专属的数据集合里，复用现有的 Stripe 账号、商品、Webhook、计费网关连接和钱包流水接口，不新增一套支付基建。带平台标记的支付事件走一条持久化的本地收件箱加后台补偿链路，ZooWork 侧的事件继续走原有处理器、Webhook 里不额外发起远程查询。对结果不确定的入账，系统会先读钱包流水做对账再决定是否需要人工介入，后台补偿不会重复入账第二笔。首次使用时会幂等地创建客户并开一个充值钱包，开钱包前校验客户归属、币种为美元、状态有效、未过期和汇率，已有绑定只做读取与校验、不会自动替换，并发写入必须对同一客户和钱包达成一致。

## 分级

- 内部：P0
- 外部：A
- toB 相关：是
- 发布状态：已上线

## PR 说明

## Summary

- Add Organization-scoped Platform billing, balance/history reads, and Stripe Checkout top-ups in claw-interface and web/platform.
- Persist Platform top-up orders and Stripe events in dedicated Platform Mongo collections. Reuse the existing Stripe account, product, webhook, Gateway connection, and Lago wallet transaction API.
- Route marked Platform events through a durable local inbox and background recovery. ZooWork events continue through the existing billing handler without a new remote Stripe lookup in the webhook.
- Reconcile uncertain Lago submissions by reading the wallet ledger before any manual action; the automatic worker does not post a second credit transaction.

## Customer and wallet initialization

- Gateway exposes one customer-only idempotent `POST /billing/customers/{customer_id}/ensure`; wallet creation reuses the existing `POST /billing/customers/{customer_id}/wallets`.
- Platform ensures the customer, creates a `topup` wallet through the existing client, or reads the explicit `wallet_already_exists` conflict's wallet ID. It validates customer ownership, USD, active status, non-expiry, and rate before storing the organization association.
- Existing associations only read and validate their original wallet. Invalid associations are not replaced automatically. A failed association write can retry with the same customer and wallet; concurrent association writes must agree on customer, wallet, and rate.
- No new wallet creation endpoint or public wallet `code` field is added. Existing wallet and ledger GET APIs remain available.

## Boundary and rollout

- [Billing Gateway PR #75](https://github.com/SerendipityOneInc/billing-gateway/pull/75) provides customer-only ensure, concurrency-safe existing wallet creation, and generic wallet/ledger reads. It has no Platform-specific database or configuration. Deploy it before this PR.
- ZooWork's existing billing routes and data remain in place. The shared webhook classifies Platform events from Stripe metadata; unmarked ZooWork events keep their existing path.
- Platform-only state is in `platform_topup_orders`, `platform_payment_events`, and the billing association on `platform_organizations`. Startup creates the indexes.

## PR size

This change spans the billing API, durable payment worker, Platform UI, and their tests. The repository's 3,000-line size gate has a `size-override` label so reviewers can evaluate the paid-order lifecycle end to end.

## Verification

- Final commit `93e6b6cd4177212dc8acfa65437e08205331598b`: Node 24 root `bash scripts/verify-py.sh --full` ran the complete suite: **12,732 passed, 5 skipped**, coverage **89.78%**. The command exited nonzero solely because the local script still requires 90%; the existing CI workflow explicitly uses 89.5% and documents its baseline. No coverage threshold was changed. All other full-check steps passed; the actual supplemental jscpd scan is detailed below.
- Billing integration correction: Ruff, Pyright, import boundaries and CI lint guards passed. Actual jscpd scans: source 1.89% (991 files, limit 3%); tests 5.79% (718 files, limit 7.5%). A temporary config disabled Git ignore filtering to ensure the ignored worktree parent did not exclude all files; project exclusions and thresholds were preserved.
- Local HTTP contract smoke passed using the real Platform client and Gateway FastAPI routes with fake Lago/Redis: customer-only ensure, first wallet creation, duplicate-wallet conflict/readback, policy validation, and ledger pagination. This does not exercise live Lago or Stripe.

- `web/platform`: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test`, and `pnpm build`.
- Local Platform test uses the default API base URL because this worktree has a developer-only `.env.local` override.

## Staging CSFLE validation

Passed on 2026-09-28 through the staging Pod's configured encrypted Mongo client. The exact PR repository source exercised Platform billing indexes, organization billing association, order and event writes, keyset/recovery queries, and atomic updates. All three isolated records were removed and independently rechecked as absent. [Validation record](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/billing-topup-review/docs/staging-validation/2026-09-28-platform-billing-csfle.md).

This validates the MongoDB CSFLE boundary, not the deployed Platform API, Stripe webhook, Gateway/Lago integration, or a real payment. Those are separate staging acceptance checks before rollout; this PR does not authorize deployment.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `2ec70d04f86a1073c977a5a29c4ee6195a91c463`
- PR: #3907
- 作者：finn-srp
- 日期：2026-09-28T08:13:32Z

### Commit Message

```
feat(platform): add organization billing and Stripe top-ups (#3907)

## Summary

- Add Organization-scoped Platform billing, balance/history reads, and
Stripe Checkout top-ups in claw-interface and web/platform.
- Persist Platform top-up orders and Stripe events in dedicated Platform
Mongo collections. Reuse the existing Stripe account, product, webhook,
Gateway connection, and Lago wallet transaction API.
- Route marked Platform events through a durable local inbox and
background recovery. ZooWork events continue through the existing
billing handler without a new remote Stripe lookup in the webhook.
- Reconcile uncertain Lago submissions by reading the wallet ledger
before any manual action; the automatic worker does not post a second
credit transaction.

## Customer and wallet initialization

- Gateway exposes one customer-only idempotent `POST
/billing/customers/{customer_id}/ensure`; wallet creation reuses the
existing `POST /billing/customers/{customer_id}/wallets`.
- Platform ensures the customer, creates a `topup` wallet through the
existing client, or reads the explicit `wallet_already_exists`
conflict's wallet ID. It validates customer ownership, USD, active
status, non-expiry, and rate before storing the organization
association.
- Existing associations only read and validate their original wallet.
Invalid associations are not replaced automatically. A failed
association write can retry with the same customer and wallet;
concurrent association writes must agree on customer, wallet, and rate.
- No new wallet creation endpoint or public wallet `code` field is
added. Existing wallet and ledger GET APIs remain available.

## Boundary and rollout

- [Billing Gateway PR
#75](https://github.com/SerendipityOneInc/billing-gateway/pull/75)
provides customer-only ensure, concurrency-safe existing wallet
creation, and generic wallet/ledger reads. It has no Platform-specific
database or configuration. Deploy it before this PR.
- ZooWork's existing billing routes and data remain in place. The shared
webhook classifies Platform events from Stripe metadata; unmarked
ZooWork events keep their existing path.
- Platform-only state is in `platform_topup_orders`,
`platform_payment_events`, and the billing association on
`platform_organizations`. Startup creates the indexes.

## PR size

This change spans the billing API, durable payment worker, Platform UI,
and their tests. The repository's 3,000-line size gate has a
`size-override` label so reviewers can evaluate the paid-order lifecycle
end to end.

## Verification

- Final commit `93e6b6cd4177212dc8acfa65437e08205331598b`: Node 24 root
`bash scripts/verify-py.sh --full` ran the complete suite: **12,732
passed, 5 skipped**, coverage **89.78%**. The command exited nonzero
solely because the local script still requires 90%; the existing CI
workflow explicitly uses 89.5% and documents its baseline. No coverage
threshold was changed. All other full-check steps passed; the actual
supplemental jscpd scan is detailed below.
- Billing integration correction: Ruff, Pyright, import boundaries and
CI lint guards passed. Actual jscpd scans: source 1.89% (991 files,
limit 3%); tests 5.79% (718 files, limit 7.5%). A temporary config
disabled Git ignore filtering to ensure the ignored worktree parent did
not exclude all files; project exclusions and thresholds were preserved.
- Local HTTP contract smoke passed using the real Platform client and
Gateway FastAPI routes with fake Lago/Redis: customer-only ensure, first
wallet creation, duplicate-wallet conflict/readback, policy validation,
and ledger pagination. This does not exercise live Lago or Stripe.

- `web/platform`: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test`,
and `pnpm build`.
- Local Platform test uses the default API base URL because this
worktree has a developer-only `.env.local` override.

## Staging CSFLE validation

Passed on 2026-09-28 through the staging Pod's configured encrypted
Mongo client. The exact PR repository source exercised Platform billing
indexes, organization billing association, order and event writes,
keyset/recovery queries, and atomic updates. All three isolated records
were removed and independently rechecked as absent. [Validation
record](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/billing-topup-review/docs/staging-validation/2026-09-28-platform-billing-csfle.md).

This validates the MongoDB CSFLE boundary, not the deployed Platform
API, Stripe webhook, Gateway/Lago integration, or a real payment. Those
are separate staging acceptance checks before rollout; this PR does not
authorize deployment.
```

来源：SerendipityOneInc/ecap-workspace @ 2ec70d04，PR #3907，作者 finn-srp。
