---
title: "开发者平台首充赠送 $10 Bonus credits：实付金额大于零即可拿，每个账号和每张卡各一次"
type: "新功能"
priority: "高"
date: "2026-10-04"
status: "待审核"
channels: ""
---

# 开发者平台首充赠送 $10 Bonus credits：实付金额大于零即可拿，每个账号和每张卡各一次

## 核心宣传点

开发者平台的新账号第一次成功充值 credits 之后，会额外收到一笔独立的 $10 Bonus credits，和你买到的 credits 分开记账、分别显示。拿到赠送的条件是折扣之后的实付金额必须大于零：如果用优惠码把这笔充值全额抵扣掉、实际没付钱，这次充值仍然算用掉了「新账号」资格，但不会发赠送额度。每个账号只能拿一次，每张符合条件的银行卡也只能拿一次——如果这张卡之前已经在开发者平台做过普通充值，那它就不再有资格，换账号用同一张卡也拿不到。

充值本身的到账不受赠送流程影响：系统先把你买的 credits 稳稳记上，再去单独判断和发放赠送，赠送环节出问题不会连累你已付款的额度。赠送的 $10 是独立投递的，即使中途状态不明也只会对账、不会重复发放。侧边栏和 Add funds 的界面、文案、付款历史的表现都保持原样；赠送资格还在核对时，概览和付款历史会显示 Processing，页面会按节奏自动刷新（结算中每 3 秒、需要等待核对或投递时每 5 分钟），最终状态确定后停止刷新。正在进行的其他付款不受影响，仍然保持快速刷新。

## 分级

- 内部：P1
- 外部：A
- toB 相关：是
- 发布状态：已合并待发版

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `30684428801f1dd8263ad4ee2e38b6754e0273b4`
- PR: #4018
- 作者：ericma-srp
- 日期：2026-10-04T21:51:04Z

### Commit Message

```
feat(platform): first credit purchase bonus with shared payment facts (#4018)

New Platform accounts receive a separate $10 Bonus credits entry after
their first eligible credit purchase. Actual payment after discounts
must be positive; zero-cash purchases consume account newness but do not
earn a bonus. Each account and each eligible card can receive one award,
and prior ordinary Platform card purchases also exclude that card.

### Implementation
- Persist successful purchase confirmation first, then reserve an
optional reward without blocking purchased-credit delivery. First
purchase follows Platform durable confirmation order; Stripe webhook
delivery does not require reconstructing a global provider event
timeline.
- Prepare verified Stripe purchase facts once on each successful order,
in a bounded shared job. Rewards read local account/card facts and use
unique account/card claims. Unknown same-account confirmation ordering
defers reservation completely, with no false reward in summary/history,
while a confirmed earlier account purchase excludes a returning account
immediately. Incomplete history stays recoverable; one malformed
historical order cannot exhaust every customer's retry budget.
Historical preparation preserves the principal recovery clock. Repeated
unchanged checks update timestamps without growing embedded audit
history; meaningful state/error transitions remain audited. Evidence
contradictions pause automatic source retries and escalate through the
existing payment Sentry reporter. The source remains an eligibility
barrier until an operator recheck records verified proof; the same
bounded path records the actual operator and incident reason.
- Post the $10 independently with a durable posting marker. Unknown
external outcomes reconcile the ledger without repeating the credit
POST. Principal, fact preparation and reward recovery run in separate
scheduler slots. Unevaluated reward sources rotate by a separate durable
check time; changed reservation failures are audited, identical retries
do not grow history or postpone principal recovery. A failed/timed-out
unlinked-source query cannot abort selected bonus delivery.
- Preserve the approved sidebar/Add funds design, exact copy and
payment-history behavior. Offers appear before eligible purchases;
internal recovery appears only as a brief payment-history delay. Normal
initial fact preparation stays Processing during a three-minute grace
covering the recovery cutoff and scheduling tick; actual source
verification failures delay immediately, and a stalled worker cannot
prolong that grace. The summary and history share the same delayed hint:
active settlement polls every 3 seconds, delayed
verification/delivery/reconciliation rewards every 5 minutes, and
terminal rewards stop; independent active payments retain fast polling.

### Validation
- 519 relevant backend tests passed (Platform, scheduler, Stripe client,
payment monitoring and local CSFLE query contracts).
- Ruff, formatting, Pyright (app + tests), all 8 import contracts, and
commit hooks passed.
- Platform: 238 tests, lint and production build passed.
- Actual BSON encode/decode round trips cover nested purchase-fact and
audit datetimes through repository reads and write-return parsing. React
Query timer tests cover balance/history polling stopping when recovery
becomes terminal, pending-to-delayed backoff from either response, and
fast polling resuming after repair.
- Regression coverage includes the normal paid Checkout webhook →
Processing summary/history → independently credited bonus →
Granted/Added response flow (with mocked provider/storage boundaries),
account/card competition, prior ordinary card use, zero-cash and
one-cent payments, immutable confirmation, shared-history failure
recovery, unknown same-account ordering hiding false reward rows and
recovering after repair, twenty held/failing source reservations not
starving later purchases, unlinked-query failure/timeout isolation,
delayed ledger/ready error responses, principal continuity, lost
reservation responses ambiguous/canceled bonus POSTs, source
incident/audit deduplication, bounded no-op/failure/recovery history,
scoped operator rechecks retaining the hold on failure, and positive
paid rewards surviving an intervening refund during reservation
recovery.

### Activation boundary
The campaign remains disabled by default; this PR does not enable or
deploy it. Before activation, complete the backend rollout, prepare
existing successful history through the audited bounded job, and
validate real Stripe Sandbox → Lago settlement, deployed encrypted
Mongo/CSFLE indexes/queries/concurrency, and representative historical
volume. Local mocks and query-contract tests do not establish these
external guarantees. No staging credentials/context are available on
this host.

Design and operating bounds:
`docs/superpowers/specs/2026-10-04-platform-first-topup-bonus.md` and
`services/claw-interface/docs/cron-triggers.md`.
```

来源：SerendipityOneInc/ecap-workspace @ 30684428，PR #4018，作者 ericma-srp。
