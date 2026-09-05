---
title: "修复：换套餐或换支付方式后，付款页还停在旧的那一单"
type: "Bug Fix"
priority: "高"
date: "2026-09-04"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：换套餐或换支付方式后，付款页还停在旧的那一单

## 核心宣传点

订阅结账以前被当成一把「全局 45 分钟锁」来管：只要你有一个待支付的订单没走完，这 45 分钟内前端就只会把那条存下来的服务商付款链接原样再给你一次，界面上也只剩「重新打开付款页」这一个动作。问题是它没把**支付渠道、套餐、计费周期**这三样当成一个完整的「结账意图」来看——你关掉支付宝的 Starter 收银台改选 Pro，新订单抢不到这把锁，界面还是把旧的 Starter 链接推给你；想从一个渠道换到另一个渠道也换不动。更麻烦的是链接过期的情况：旧逻辑只看域名是不是官方主机，从不看链接自带的过期时间，于是订单一直挂着待支付，你每点一次都拿到同一条已经打不开的链接。

现在改成：选定支付渠道时自动解算当前的结账状态；只有当渠道、套餐、计费周期三者**全部一致**时才复用那个还活着的收银台，否则先把上一个 Antom 或 Airwallex 收银台取消掉，再创建一条新的。「结账进行中 / 重新打开付款页」这个交互被整体移除，不再有那种你明明改了主意、界面却拽着你回旧订单的体验。

链接时效上，Airwallex 收银台链接的 JWT 过期时间解析被收敛成一处公共实现，并保留五分钟的复用安全窗口；Antom 侧新增了结账截止时间、安全重放规则、取消前后各做一次支付查询，以及一次性的卡支付充值重试。安全边界维持保守：服务商查询或变更结果不明确时一律按失败处理（fail closed）；Antom 替换会在取消前后都确认一遍是否其实已经付款成功；本地取消要先通过待定状态与服务商身份的 CAS 校验才释放结账锁；过期的服务商请求会被丢弃。既不会重复扣款，也不会把还活着的订单误杀。

## 原始内容

### fix(billing): resolve subscription checkout changes safely (#3642)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `d10b224cd446b3d2a96e68e84b94663d57b155c2`
- PR: #3642
- 作者: tim-srp
- 日期: 2026-09-04T12:10:33Z

### Commit Message

```
fix(billing): resolve subscription checkout changes safely (#3642)

## Summary
- resolve subscription checkout state automatically when the user
selects a payment channel
- reopen a live checkout only when channel, plan, and billing cycle all
match
- otherwise cancel the previous Antom or Airwallex checkout before
creating a replacement
- remove the checkout-in-progress / Reopen payment page interaction

## Root cause
The frontend treated the subscription checkout lease as a global
45-minute lock and only offered the stored provider URL. It did not
model the selected channel, plan, and billing cycle as one checkout
intent, so users could not safely switch payment channels and could
reopen a checkout for an outdated plan.

The replacement flow now fails closed: if provider cancellation fails or
its outcome is unknown, the old lease remains held and no second
checkout is created.

## Test plan
- [x] Antom request-ID cancellation succeeds before Card checkout
creation
- [x] Airwallex cancellation succeeds before Antom checkout creation
- [x] unknown cancellation outcome keeps the old order and lease
- [x] identical channel, plan, and billing cycle resumes the live URL
- [x] changed plan, billing cycle, or channel replaces the old checkout
- [x] frontend automatically resolves checkout conflicts and opens the
returned URL without a Reopen button
- [x] backend related tests: 78 passed
- [x] frontend billing tests: 102 passed
- [x] backend ruff, formatting, Pyright, and import-linter passed
- [x] targeted frontend ESLint passed with one pre-existing test warning

## Local validation note
`verify-changed.sh` passed backend verification but skipped its web
phase because the worktree does not have `web/node_modules`. The
directly relevant frontend ESLint and Vitest commands were run from
`web/app` and passed. Full frontend TypeScript validation remains
blocked by pre-existing chat/design-system/SEO dependency errors outside
the files changed by this PR.
```

### PR Body

```
## Summary
- resolve subscription checkout state automatically when the user selects a payment channel
- reopen a live checkout only when channel, plan, and billing cycle all match
- otherwise cancel the previous Antom or Airwallex checkout before creating a replacement
- remove the checkout-in-progress / Reopen payment page interaction

## Root cause
The frontend treated the subscription checkout lease as a global 45-minute lock and only offered the stored provider URL. It did not model the selected channel, plan, and billing cycle as one checkout intent, so users could not safely switch payment channels and could reopen a checkout for an outdated plan.

The replacement flow now fails closed: if provider cancellation fails or its outcome is unknown, the old lease remains held and no second checkout is created.

## Test plan
- [x] Antom request-ID cancellation succeeds before Card checkout creation
- [x] Airwallex cancellation succeeds before Antom checkout creation
- [x] unknown cancellation outcome keeps the old order and lease
- [x] identical channel, plan, and billing cycle resumes the live URL
- [x] changed plan, billing cycle, or channel replaces the old checkout
- [x] frontend automatically resolves checkout conflicts and opens the returned URL without a Reopen button
- [x] backend related tests: 78 passed
- [x] frontend billing tests: 102 passed
- [x] backend ruff, formatting, Pyright, and import-linter passed
- [x] targeted frontend ESLint passed with one pre-existing test warning

## Local validation note
`verify-changed.sh` passed backend verification but skipped its web phase because the worktree does not have `web/node_modules`. The directly relevant frontend ESLint and Vitest commands were run from `web/app` and passed. Full frontend TypeScript validation remains blocked by pre-existing chat/design-system/SEO dependency errors outside the files changed by this PR.

```

### fix(billing): replace superseded Antom checkouts (#3646)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `fc51f977c4845e0fea277d4d68c4560f274bf5bb`
- PR: #3646
- 作者: tim-srp
- 日期: 2026-09-04T07:51:52Z

### Commit Message

```
fix(billing): replace superseded Antom checkouts (#3646)

## Summary
- allow a personal Antom checkout to replace an unpaid live checkout
when the selected plan or billing cycle changes
- preserve reuse behavior for the same complete checkout intent
- reuse the existing provider inquiry, cancellation verification,
payment recheck, and guarded local cancellation flow

## Root cause
The subscription checkout lease treated every pending personal checkout
as equivalent for 45 minutes. When a user closed an Alipay Starter
checkout and selected Pro, the new order could not claim the lease and
the UI could only reopen the old Starter URL. Expiry retirement handled
dead URLs but did not consider a still-live checkout that no longer
matched the user's selected plan or billing cycle.

## Test plan
- [x] `pytest tests/unit/test_antom_billing_v2_checkout.py
tests/unit/test_antom_checkout_expiry.py -q` (29 passed)
- [x] `bash scripts/verify-py.sh`
- [x] pre-push changed-surface verification

## Safety
- replacement only applies when both old and new intents have complete
`plan` and `billing_cycle` fields and they differ
- provider payment state is checked before and after cancellation
- local cancellation is guarded by pending status and provider
identifiers; ambiguous or paid states remain fail-closed
```

### PR Body

```
## Summary
- allow a personal Antom checkout to replace an unpaid live checkout when the selected plan or billing cycle changes
- preserve reuse behavior for the same complete checkout intent
- reuse the existing provider inquiry, cancellation verification, payment recheck, and guarded local cancellation flow

## Root cause
The subscription checkout lease treated every pending personal checkout as equivalent for 45 minutes. When a user closed an Alipay Starter checkout and selected Pro, the new order could not claim the lease and the UI could only reopen the old Starter URL. Expiry retirement handled dead URLs but did not consider a still-live checkout that no longer matched the user's selected plan or billing cycle.

## Test plan
- [x] `pytest tests/unit/test_antom_billing_v2_checkout.py tests/unit/test_antom_checkout_expiry.py -q` (29 passed)
- [x] `bash scripts/verify-py.sh`
- [x] pre-push changed-surface verification

## Safety
- replacement only applies when both old and new intents have complete `plan` and `billing_cycle` fields and they differ
- provider payment state is checked before and after cancellation
- local cancellation is guarded by pending status and provider identifiers; ambiguous or paid states remain fail-closed

```

### fix(billing): refresh expired checkout links across providers (#3645)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `991a21da377a3509020830b802e32d69df5b4a9b`
- PR: #3645
- 作者: tim-srp
- 日期: 2026-09-04T05:47:20Z

### Commit Message

```
fix(billing): refresh expired checkout links across providers (#3645)

## Summary

- centralize Airwallex checkout URL JWT expiry parsing with a
five-minute reuse safety window
- refresh stale Airwallex subscription and top-up checkouts only after
provider-confirmed terminal state, including cancellation races
- add Antom checkout deadlines, safe replay rules, pre/post-cancel
payment inquiry, guarded local retirement, and one-shot card top-up
retry

## Safety

- unknown provider inquiry or mutation outcomes fail closed
- Antom replacement checks for successful payment both before and after
cancellation
- local Antom cancellation uses a pending-state and provider-identity
CAS before releasing the checkout lease
- stale provider requests are never recreated with the same Antom
idempotency key

## Test plan

- [x] 187 focused backend unit tests
- [x] 2 frontend retry unit tests
- [x] `bash scripts/verify-changed.sh`
- [x] independent `origin/main...HEAD` code review: no findings

## Deployment

- deploy both `claw-interface` and `web/app`
```

### PR Body

```
## Summary

- centralize Airwallex checkout URL JWT expiry parsing with a five-minute reuse safety window
- refresh stale Airwallex subscription and top-up checkouts only after provider-confirmed terminal state, including cancellation races
- add Antom checkout deadlines, safe replay rules, pre/post-cancel payment inquiry, guarded local retirement, and one-shot card top-up retry

## Safety

- unknown provider inquiry or mutation outcomes fail closed
- Antom replacement checks for successful payment both before and after cancellation
- local Antom cancellation uses a pending-state and provider-identity CAS before releasing the checkout lease
- stale provider requests are never recreated with the same Antom idempotency key

## Test plan

- [x] 187 focused backend unit tests
- [x] 2 frontend retry unit tests
- [x] `bash scripts/verify-changed.sh`
- [x] independent `origin/main...HEAD` code review: no findings

## Deployment

- deploy both `claw-interface` and `web/app`

```
