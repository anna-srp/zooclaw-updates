---
title: "线下合同付款的 Platform 组织，现在可由员工在 Console 手动充值并留痕"
type: "新功能"
priority: "高"
date: "2026-10-12"
status: "待审核"
channels: ""
---

# 线下合同付款的 Platform 组织，现在可由员工在 Console 手动充值并留痕

## 核心宣传点

通过线下合同付费使用 Platform 的客户，现在可由员工在 Console 后台直接发放其购买的余额。员工在可搜索、可翻页的列表里找到生效中的 Platform 组织，填写美元金额和内部备注后确认充值；详情页展示当前余额和逐条充值记录，充值历史与余额查询独立加载，钱包故障时仍可查阅。接口要求 SRP 员工身份并命中超管白名单，先记录订单与审计再发货，持久化认领保证只写一次钱包。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## 备注

Console 会生成并保留操作参考号用于同次重试和页面重载；充值结果不确定时需人工对账，不会自动重发。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `f2b0205e377afb4913133ffc997d77c22089b5d5`
- PR: #4059
- 作者：finn-srp
- 日期：2026-10-12T12:54:48Z

### Commit Message

```
feat(platform): add audited manual organization top-ups (#4059)

## Summary
Customers who pay for Platform usage through an offline contract can now
receive the purchased balance through the staff Console. Staff find an
active Platform Organization in a paginated, searchable list, enter a
USD amount and internal note, and confirm the recharge. The Org detail
view shows its current balance and individual recharge records. Recharge
history loads independently of the balance lookup, so staff can inspect
manual-review records during a wallet or gateway failure; recharge
controls remain hidden until the first balance lookup succeeds.

The API requires verified SRP staff identity plus the current superadmin
email allowlist. Manual credits use the existing Org wallet and durable
fulfillment flow: the order and operator audit are recorded before
delivery, a persisted claim allows only one wallet POST, and an
uncertain result is reconciled rather than reposted. The Console
generates and retains the operation reference for same-attempt retries
and reloads. Offline paid credits count as prior paid purchases without
starting Stripe Checkout or granting a card reward; complimentary
credits remain a separate API/storage source.

Customer billing displays both online and offline purchases as
**Top-up**. Internal source, operator, reference and note remain
separate; staff details are not returned to customers. No commercial
subscription or changes to Billing Gateway/account-service APIs are
introduced.

## Test plan
- [x] Rebase onto current `origin/main`; run local `ecap-verify-py-ci`:
12,213 passed / 5 skipped, 89.57% coverage; Linux dependency resolution,
static checks, ci-lint and source/test duplication checks passed.
- [x] Console: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test` (685
passed), `pnpm build`.
- [x] Platform: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test` (283
passed), `pnpm build`. Two render-wait failures during concurrent local
verification passed on targeted and full reruns without code or timeout
changes.
- [x] Verify actual repository operations through staging CSFLE:
manual-order insert/read/CAS/history/list in an isolated disposable
fixture, plus read-only Org pagination and literal name/ID/owner search.
- [x] Devcontainer integration: authenticated staff lookup, isolated
test Org with its real staging wallet, customer top-up history, and
desktop/mobile Console flow. The tester confirmed a $1 offline top-up
and its customer balance/history.

## Rollout
Deploy the backend on every API replica and recovery worker before
exposing the Console action: older strict order readers cannot decode
manual-credit fields. New Stripe orders retain their existing persisted
shape. No deployment or production data write is included in this PR.

## Review disposition
Previous GitHub CI checks passed. Codex review reported no findings.
Claude noted that a concurrent `updated_at` change can prevent the
redundant order-local `manual.repeated_confirmation` history entry from
being appended. This is left unchanged: every `grant()` invocation
separately appends global requested/outcome audit events with distinct
audit IDs, so the retry operator, target, reference and outcome remain
durably recorded even on that CAS miss; delivery also re-reads current
state and retains the one-POST guarantee. The order-local history caveat
is retained for human review.


Tim's first-load balance failure finding is fixed in `0b0916eb0`:
history is mounted directly from the selected Org ID, while the balance
error and reload action remain visible and the recharge form is withheld
without account data. Added a regression test returning
`wallet_changed_before_credit` history alongside a rejected initial
lookup; all 685 Console tests and lint/typecheck/build pass in the Node
24 devcontainer.
```

