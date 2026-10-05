# SerendipityOneInc/ecap-workspace — commits 2026-10-04

## feat(platform): first credit purchase bonus with shared payment facts (#4018)

- **SHA**: `30684428801f1dd8263ad4ee2e38b6754e0273b4`
- **作者**: ericma-srp
- **日期**: 2026-10-04T21:51:04Z

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

## fix(platform): Usage 金额统一保留两位小数 (#4016)

- **SHA**: `22d17ae272264d05cc711af4a18e400339464b35`
- **作者**: david-srp
- **日期**: 2026-10-04T05:12:04Z

### Commit Message

```
fix(platform): Usage 金额统一保留两位小数 (#4016)

## Summary

- Platform → Usage → Activity 的 Spend 明细统一四舍五入到两位小数，例如 `$0.01123 →
$0.01`、`$0.127756 → $0.13`；极小金额按同一规则显示为 `$0.00`。
- Total spend 和明细共用 `formatUsageSpend`，总额保持现有的两位小数展示。原始
credits、服务端汇总、扣费和分页逻辑不变，不涉及后端或时间/Session 聚合。

## Root cause

总额与明细此前使用不同的格式化入口：总额固定两位小数，明细最多保留六位。此次统一展示规则，并移除不再需要的独立总额格式化函数。

## Test plan

- [x] `pnpm exec vitest run src/routes/usage.test.tsx`：11/11
通过；同步现有测试的明细金额预期。
- [x] `pnpm typecheck`、`pnpm lint`、`git diff --check` 通过。
- [x] 本地示例数据预览：桌面与 390px 手机视口的金额均为两位小数；Load more、Refresh 正常，手机页面无整体横向溢出。
- [x] 浏览器核对截图中的八个金额示例，以及零值和极小金额的显示。
```
