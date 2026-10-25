---
title: "修复：用 Link 银行卡支付也能拿到首充赠金，失败尝试不再占掉唯一领取资格"
type: "Bug Fix"
priority: "高"
date: "2026-10-08"
status: "待审核"
channels: ""
---

# 修复：用 Link 银行卡支付也能拿到首充赠金，失败尝试不再占掉唯一领取资格

## 核心宣传点

此前有用户先用零现金优惠券完成一笔结账，再用 Link 支付 20 美元，本金正常到账，10 美元首充赠金却没发放，活动入口还消失，接口只返回「不符合条件」。本次把经 Stripe 验证的 Link 信用卡/借记卡纳入正常银行卡识别，仍要求有真实正向付款记录，并保留账户与卡片各自只能领一次的唯一性；不透明的 Link、银行扣款、预付卡和其他钱包不会自动过关。同时把「本次下单资格判定失败」与「账户一次性领取」拆开记录，Failed 历史、可否重试、活动入口是否显示都用同一套判定，已提交或已发放的奖励仍占用名额。历史上被误判为 ineligible_card 的记录会重新获得重试机会。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 备注

问题由 Staging 测试复现，正式环境需确认历史误判记录的回放范围。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `13da07ddb5ce3905d5db145c09feb018004c0e25`
- PR: #4036
- 作者：ericma-srp
- 日期：2026-10-08T14:09:55Z

### Commit Message

```
fix(platform): separate bonus attempts from redemption and accept Link cards (#4036)

## Summary
A Staging tester completed a zero-cash coupon checkout and then a $20
Link payment. Principal reached the wallet, but no $10 bonus row
appeared and the offer disappeared. The public API confirmed
`ineligible`/no bonus; the exact persisted rejection was not exposed.
Reproduction traced the matching path: all wallets were rejected and
only duplicate-card failures were retryable.

- Accept Stripe-verified Link credit/debit cards in the existing card
integration, retaining positive-payment proof and the same account/card
redemption uniqueness. Opaque Link, bank funding, prepaid/unknown
funding and other wallets do not automatically qualify.
- Unify definitive qualification failures as **order-owned failed
attempts**, separate from the account's one-time redemption. Save the
failure before reassignment; use the same classification for Failed
history, retry permission and offer visibility.
Submitted/uncertain/credited rewards remain occupied. No new business
status, collection, global history scan or repair loop.
- Existing safe `ineligible_card` records regain their conditional offer
and visible failure without writes on GET. Persist their immutable
snapshot before a later attempt. This does not retroactively credit old
purchases or manually alter any balance.
- Keep immutable failure explanations separate from current eligibility:
both failure types show retry guidance only when billing confirms an
eligible, available offer. Legacy rejection plus an intervening ordinary
paid purchase keeps its failure row but does not invite another payment;
guidance also disappears after a successful redemption.
- Preserve legacy snapshots/strict storage readers and negotiate history
v3 with cached v1/v2 clients. New verification holds are ignored by old
workers until backend rollout completes. Both backend and frontend
deploys are required.

The canonical [Platform product
rules](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/bonus-attempt-redemption/web/platform/PRODUCT.md#first-top-up-reward)
now describe the same eligibility contract: ordinary paid purchases
disqualify, explicit rejected reward attempts do not consume
eligibility, positively verified Link credit/debit cards are supported,
and retry guidance always depends on current account eligibility.

## Test plan
- [x] 611 Platform backend regressions + CSFLE syntax guard; final
focused purchase-proof/mixed-worker tests: 63 passed after adding the
opaque-Link boundary.
- [x] 35 isolated real ordinary-Mongo tests: rejection exclusion,
matched snapshot/duplicate guard, source reassignment, unique
account/card reservation, ordering and old snapshots. No skipped tests.
- [x] Updated CSFLE probe tests, including matched new-reason
snapshot/readback/conflict/cleanup; **these local tests are not
encrypted-runtime proof**.
- [x] Actual main strict order reader round-trip retains the new audit
snapshot; legacy verification reason list excludes the new hold.
- [x] 103 frontend tests across billing/router/client/preview; lint,
typecheck, production build; real local-browser preview shows Failed +
correct reason + retry offer with no console error on a fresh page.
- [x] Python static/architecture/complexity checks and all commit/push
hooks. Product wording/layout and $10 amount unchanged except the
necessary payment-method failure explanation.
- [x] Tim P2 regression: seven frontend cases fail before the
correction; after it, 88 router/client tests and 22 backend
attempt/retry tests pass. Includes legacy method rejection + intervening
ordinary paid order -> ineligible offer, retained Failed reason, next
purchase with no reward/ledger submission. Platform lint/typecheck/build
and Python static checks pass. No backend production query or state
change in this correction.
- [x] Tim P3 documentation correction: cross-checked PRODUCT.md against
the account-history predicates, safe rejection rules, Stripe card proof
and current-eligibility UI gate; relative acceptance link and diff
whitespace verified. This follow-up changes documentation only; no new
runtime behavior or tests.
- [ ] Actual Staging encrypted-client operations, real Stripe-to-Lago
delivery, and direct-card/Link cross-account fingerprint equivalence
after both deploys.

## Tim review / Staging acceptance request
Please review the code change and approve normal merge into main for
Staging deployment, then the product manager will immediately accept the
real encrypted/Stripe-to-Lago paths. This follows the requested Staging
acceptance sequence; **merge is not production release authorization**.
Keep required review and CI. Production release stays gated on recorded
Staging acceptance.

Critical checks: zero-cash does not consume; verified Link card ->
exactly one $10; rejected method/redeemed card -> Failed reason plus
offer/retry guidance only while account eligibility remains; qualifying
retry -> one credit with old failures retained; another account cannot
redeem the same rewarded card, testing both direct-card -> Link and Link
-> direct-card under the same Stripe account/environment; uncertain
delivery never reopens. Engineering should retain encrypted probe
results/audit correlation/cleanup and actual ledger evidence alongside
PM screenshots. Compare the actual Charge card fingerprints securely;
presence of a fingerprint is not proof that direct-card and Link
identities are equivalent. If they differ or a second reward posts, stop
production release and investigate. Current local tooling has no
authenticated staging Pod access; no encrypted-runtime pass, actual
Charge inspection, manual credit or deployment is claimed. An authorized
operator may also run the exact source bundle before merge.


[Design](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/bonus-attempt-redemption/docs/superpowers/specs/2026-10-08-platform-bonus-attempt-redemption.md)
· [Acceptance and evidence
boundaries](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/bonus-attempt-redemption/docs/staging-validation/2026-10-08-bonus-attempt-redemption.md)
· [Stripe Link card integration
contract](https://docs.stripe.com/payments/link/link-payment-integrations)

Follow-up to merged #4024. Query changes remain bounded
single-collection reads/classic CAS with existing account/environment
and unique-ID indexes; the updated probe exercises the new two-action
exclusion. Deployed index/query-plan and CSFLE checks remain part of
Staging acceptance.
```

