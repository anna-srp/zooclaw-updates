---
title: "修复：企业版/垂类包重复下单不再产生多笔待支付订单，工作区加载失败会直接显示原因"
type: "Bug Fix"
priority: "高"
date: "2026-10-15"
status: "待审核"
channels: ""
---

# 修复：企业版/垂类包重复下单不再产生多笔待支付订单，工作区加载失败会直接显示原因

## 核心宣传点

企业版与垂类包购买现在会复用同一笔订单和已打开但未支付的 Stripe Checkout，多次点击、并发请求或 Stripe 响应丢失都不会再留下多笔可支付的订单；购买尝试通过已有的买家结账租约串行化，响应丢失时用原始持久化请求和幂等键恢复。同时 Agent 工作区会保留会话与历史的错误信息，加载失败后不再卡在加载态假装还在转圈，已有的查询重试和重新打开成功的路径不受影响。修复 #4060。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## 备注

仅处理前端错误透传与加载态呈现，#3728 涉及的旧版直连/会话绑定兼容仍未闭环，该 issue 保持 open。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `bc96db72666333ddb003a971e05b85c9f3782261`
- PR: #4081
- 作者：kaka-srp
- 日期：2026-10-15T09:23:39Z

### Commit Message

```
fix(billing): reuse enterprise checkout and surface workspace errors (#4081)

## Summary
- Reuse the original order and open, unpaid Stripe Checkout for the same
enterprise/vertical-pack purchase. Serialize attempts with the existing
buyer checkout lease, and recover lost responses with the original
persisted request and idempotency key.
- Preserve conversation/history error messages in Agent Workspace and
stop showing the chat loading surface after a load failure. Existing
query retries and successful reopening continue to work.

Fixes #4060.
Related to #3728: this PR addresses only frontend error propagation and
loading presentation. Legacy direct/thread binding compatibility remains
outside this change, so #3728 stays open.

## Root cause
Enterprise Checkout previously generated a fresh order/key on every
attempt and only checked active agreements. Repeated clicks, parallel
requests, or a lost Stripe response could leave multiple payable
Sessions. Nested workspace view models also discarded already-normalized
error strings while history remained unavailable.

## Implementation boundaries
- Reuse existing bounded order scans, payment audit events, checkout
uncertainty/expiry handling, and guarded state transitions. Unknown or
changed purchases block another Checkout; provider-confirmed expiration
allows a fresh purchase.
- Compare addon sets independently of order without modifying the
original saved snapshot or Stripe parameters, including timeout
recovery.
- Checkout serialization is scoped to the same buyer.
Cross-administrator team concurrency and live billing repairs are
outside this PR.

## Test plan
- [x] 339 relevant backend tests passed before the final addon-order
fix; 77 focused enterprise checkout, subscription, and Managed Payments
tests passed after the final fixes, including both new addon-order
regressions.
- [x] 87 relevant frontend tests passed; frontend TypeScript and ESLint
passed.
- [x] Backend Ruff, formatting, full Pyright and import-linter passed
after the final fix.
- [x] Adapted the existing Managed Payments fixture to the extracted
checkout module and real persisted-order/audit flow after CI exposed
stale patch targets.
- [x] Astra local review completed; its P2 addon-order finding was fixed
and targeted re-review found no new issues.
- [ ] Real Stripe, encrypted MongoDB client, and deployed browser
end-to-end validation were not run.

## Review follow-up
- The suggested agreement-check race does not establish a new same-buyer
duplicate: an older unfinished/paid-unfulfilled order is scanned before
the agreement read; a matching recovery reuses its original Session/key.
Another team administrator creating an agreement is the explicitly
excluded cross-administrator case.
- `scheduled_for_subscription_agreement_id` is explicitly written when
reserving a scheduled package-change target. A target without
provider-attempt markers is not a live Checkout; ordinary legacy Stripe
purchases without that marker remain blocked for reconciliation.
- Workspace `loadError` and `status.error` intentionally derive from the
same transport error. The reviewer did not identify a current failure
from that wiring, so no additional frontend refactor was added.
```

