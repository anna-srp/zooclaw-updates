---
title: "账单页可以直接下载发票了：Stripe 跳托管发票页，Airwallex 直接给 PDF"
type: "产品基础功能更新"
priority: "高"
date: "2026-09-04"
status: "待审核"
channels: "站内弹窗+Discord+changelog"
---

# 账单页可以直接下载发票了：Stripe 跳托管发票页，Airwallex 直接给 PDF

## 核心宣传点

付完钱想拿发票，以前在账单页是没有直接出口的，「最近活动」里只有订单记录，旁边挂着一个早就名不副实的「查看全部发票」链接。

现在「最近活动」新增了一列「下载发票」（含多语言文案），老的「查看全部发票」入口一并移除，Stripe 的支付方式管理仍然保留在原处。点下载时按支付渠道分流：已付款的 Stripe 订单跳转到 Stripe 托管的发票页面；已付款的 Airwallex 订单直接给服务商出具的 PDF；支付宝 / Antom 渠道暂不支持，会显示明确的本地化提示而不是报错；未付款或未完成的订单则依然不可下载。此后新的 Airwallex 付款会把服务商侧的发票标识持久化下来，另外提供了一个默认 dry-run 的脚本，用来安全地回填历史上已成功的 Airwallex 订单。

顺带修了两处让发票「看得见却拿不到」的问题：

一是**历史发票回填匹配错了对象**。Airwallex 的发票列表/详情接口其实根本不返回 `checkout_id`、账期起止这些字段，而旧的回填逻辑正是拿它们来做匹配的——测试夹具里手工塞了这些字段，所以测试一直是绿的，真实数据上却匹配不到。现在改为使用服务商侧真实支持的 `subscription_id` 和 `billing_customer_id` 做精确过滤，并且回填、每小时的对账维护、下载时的按需补齐三条路径共用同一套保守匹配器，口径统一。同时开始处理 `invoice.payment.paid` 事件，并防止「已开具但未付款」的发票被当成已结清而变得可下载。

二是**能救回来的发票被前端提前藏了**。下载接口本身是可以在你点击的当下按订阅或客户身份把缺失的 Airwallex 发票 ID 现场找回来的，但订单历史接口在 ID 尚未落库前一律返回 `invoice_available=false`，前端于是把唯一能触发这个补救动作的按钮给隐藏了，形成死锁。现在对这类可恢复的 Airwallex 成功订单如实放出下载入口；Stripe 侧仍然严格依赖已持久化的发票 ID，已付款状态和渠道限制照旧。

## 原始内容

### feat(billing): add provider invoice downloads (#3650)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `8481672b4717c01bae7a7e264df303c00cfe1903`
- PR: #3650
- 作者: tim-srp
- 日期: 2026-09-04T10:22:52Z

### Commit Message

```
feat(billing): add provider invoice downloads (#3650)

## Linear

N/A

## Summary

- Add a localized Download invoice column to Billing recent activity and
remove the obsolete View all invoices link while preserving Stripe
payment-method management.
- Route paid Stripe orders to their hosted invoice page, paid Airwallex
orders to the provider PDF, and show localized unsupported messaging for
Alipay/Antom; unpaid or incomplete orders remain unavailable.
- Persist provider invoice identities for future Airwallex payments and
add a dry-run-by-default script to safely backfill historical successful
Airwallex orders.

## Test plan

- [x] Backend focused unit tests: 425 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8
import-linter contracts passed.
- [x] Frontend targeted verification: TypeScript, ESLint, and Vitest
passed (379 passed, 1 skipped).
- [x] Backfill CLI help succeeds without database initialization and
documents dry-run as the default.
- [x] Final branch review found no critical, important, or minor issues.

## Rollout notes

- Deploy the backend before or together with the frontend because the UI
uses the new per-order invoice download endpoint.
- Run `scripts/backfill_airwallex_invoice_ids.py` in dry-run mode first,
review its counters and conflicts, and only then rerun with `--write` in
the intended environment.
- No production backfill was executed as part of this PR.
```

### PR Body

```
## Linear

N/A

## Summary

- Add a localized Download invoice column to Billing recent activity and remove the obsolete View all invoices link while preserving Stripe payment-method management.
- Route paid Stripe orders to their hosted invoice page, paid Airwallex orders to the provider PDF, and show localized unsupported messaging for Alipay/Antom; unpaid or incomplete orders remain unavailable.
- Persist provider invoice identities for future Airwallex payments and add a dry-run-by-default script to safely backfill historical successful Airwallex orders.

## Test plan

- [x] Backend focused unit tests: 425 passed.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright, and all 8 import-linter contracts passed.
- [x] Frontend targeted verification: TypeScript, ESLint, and Vitest passed (379 passed, 1 skipped).
- [x] Backfill CLI help succeeds without database initialization and documents dry-run as the default.
- [x] Final branch review found no critical, important, or minor issues.

## Rollout notes

- Deploy the backend before or together with the frontend because the UI uses the new per-order invoice download endpoint.
- Run `scripts/backfill_airwallex_invoice_ids.py` in dry-run mode first, review its counters and conflicts, and only then rerun with `--write` in the intended environment.
- No production backfill was executed as part of this PR.

```

### fix(billing): converge Airwallex invoice identities (#3651)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `78d26c7e7decc0a65c92938be31d38c41edd7ce1`
- PR: #3651
- 作者: tim-srp
- 日期: 2026-09-04T11:41:00Z

### Commit Message

```
fix(billing): converge Airwallex invoice identities (#3651)

## Summary

- replace the Airwallex historical invoice backfill's unsupported
checkout/period matching with exact provider-side `subscription_id` and
`billing_customer_id` filters
- handle `invoice.payment.paid` and prevent finalized-but-unpaid
invoices from settling or becoming downloadable
- reconcile missing invoice IDs hourly and recover one missing ID on
demand before download
- share one conservative matcher across backfill, maintenance
reconciliation, and download recovery

## Root cause

Airwallex invoice list/detail responses do not contain `checkout_id`,
`period_starts_at`, or `period_ends_at`. The previous backfill fixtures
supplied those fields, so its tests passed while all real staging
candidates remained unmatched.

The replacement requires exactly one server-filtered invoice with
`payment_status=PAID`, matching amount, and matching currency.
Ambiguous, unpaid, or mismatched records remain unchanged. Three known
staging orders whose test amounts differ from their Airwallex invoices
are intentionally skipped.

## Verification

- 295 targeted Airwallex lifecycle, reconciliation, backfill, download,
client, schema, and repository tests passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

## Related

- follows #3650
```

### PR Body

```
## Summary

- replace the Airwallex historical invoice backfill's unsupported checkout/period matching with exact provider-side `subscription_id` and `billing_customer_id` filters
- handle `invoice.payment.paid` and prevent finalized-but-unpaid invoices from settling or becoming downloadable
- reconcile missing invoice IDs hourly and recover one missing ID on demand before download
- share one conservative matcher across backfill, maintenance reconciliation, and download recovery

## Root cause

Airwallex invoice list/detail responses do not contain `checkout_id`, `period_starts_at`, or `period_ends_at`. The previous backfill fixtures supplied those fields, so its tests passed while all real staging candidates remained unmatched.

The replacement requires exactly one server-filtered invoice with `payment_status=PAID`, matching amount, and matching currency. Ambiguous, unpaid, or mismatched records remain unchanged. Three known staging orders whose test amounts differ from their Airwallex invoices are intentionally skipped.

## Verification

- 295 targeted Airwallex lifecycle, reconciliation, backfill, download, client, schema, and repository tests passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

## Related

- follows #3650

```

### fix(billing): expose recoverable Airwallex invoices (#3653)

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5376f5bdb51f202be9874275c45b24eea56de76a`
- PR: #3653
- 作者: tim-srp
- 日期: 2026-09-04T13:24:25Z

### Commit Message

```
fix(billing): expose recoverable Airwallex invoices (#3653)

## Summary

- expose the invoice download action for successful Airwallex orders
that can recover an invoice by subscription or customer identity
- keep Stripe invoice availability dependent on a persisted provider
invoice ID
- preserve the existing paid-status and provider restrictions

## Root cause

The download endpoint can safely recover a missing Airwallex invoice ID
on demand, but the order history response reported
`invoice_available=false` until that ID was already persisted. The
frontend therefore hid the only action capable of triggering recovery.

## Tests

- `services/claw-interface/.venv/bin/pytest
tests/unit/test_billing_v2_order_requests.py -q --disable-warnings`
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

## Staging evidence

UID `7501615744291966976` has a successful Airwallex order without a
persisted invoice ID. Its exact subscription filter returns one
FINALIZED, PAID, amount-matching invoice with a PDF.
```

### PR Body

```
## Summary

- expose the invoice download action for successful Airwallex orders that can recover an invoice by subscription or customer identity
- keep Stripe invoice availability dependent on a persisted provider invoice ID
- preserve the existing paid-status and provider restrictions

## Root cause

The download endpoint can safely recover a missing Airwallex invoice ID on demand, but the order history response reported `invoice_available=false` until that ID was already persisted. The frontend therefore hid the only action capable of triggering recovery.

## Tests

- `services/claw-interface/.venv/bin/pytest tests/unit/test_billing_v2_order_requests.py -q --disable-warnings`
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`

## Staging evidence

UID `7501615744291966976` has a successful Airwallex order without a persisted invoice ID. Its exact subscription filter returns one FINALIZED, PAID, amount-matching invoice with a PDF.

```
