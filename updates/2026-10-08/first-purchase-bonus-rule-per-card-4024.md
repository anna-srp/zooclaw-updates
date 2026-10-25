---
title: "修复：首充赠金规则改为「每张卡可领一次」，历史普通消费不再误伤新账号"
type: "Bug Fix"
priority: "高"
date: "2026-10-08"
status: "待审核"
channels: ""
---

# 修复：首充赠金规则改为「每张卡可领一次」，历史普通消费不再误伤新账号

## 核心宣传点

首充赠金的判定口径按产品负责人确认的规则做了简化：从「这张卡从未在平台消费过」改为「每张卡可以领取一次该奖励」。也就是说，一张卡过去只是普通消费、没领过奖励，不再把另一个本该符合条件的账号挡在门外。账户侧的资格仍以首笔正向付费为准，金额维持 10 美元，账户与卡片各自只能领一次；经确认的 0 元订单既不产生也不消耗资格，金额不明不算 0 元；账户此前有过普通正向消费则该账户不再符合条件。明确的重复卡失败记录不可更改，但允许换一张符合条件的新卡再试；发放中或结果不确定的记录继续占用名额，退款不会重新打开资格。本金发放逻辑完全独立，不受影响。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 备注

同时下线了全局卡片历史扫描、事实队列与后台 worker，已部署的索引保留不删。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `3c32605e4abee878f33590ca0459beb036e1ea9b`
- PR: #4024
- 作者：ericma-srp
- 日期：2026-10-08T09:24:33Z

### Commit Message

```
fix(platform): simplify first-purchase bonus redemption and retry (#4024)

## Business rule and simplification

The product owner approved **each card may receive this reward once**,
replacing “the card has never purchased on Platform.” Ordinary earlier
card purchases without a reward do not exclude another eligible account.
Account eligibility remains the first positive paid purchase, with the
existing $10 amount and once-only account/scoped-card redemption.
Verified $0 purchases neither earn nor consume eligibility; unknown cash
is not zero. Ordinary prior positive purchases disqualify that account.
Explicit duplicate-card failures remain immutable and allow an eligible
new-card attempt. Uncertain/submitted delivery retains occupancy;
refunds do not reopen it. Principal stays independent.

The global card-history/completeness queries, fact queue, worker and
creation of four dedicated indexes are removed (existing deployed
indexes are not dropped). Only the reward candidate’s own Stripe payment
is verified. Existing uniqueness, ledger identity, reconciliation,
source CAS, old-reader compatibility and failure snapshots remain. No
new reward state, stored field, general campaign engine or budget
subsystem; UI/Checkout unchanged in this update.

## Latest fix: Tim P3, review 5453069113

**Confirmed issue:** an older successful order lacking reliable
payment-time evidence silently kept a newer candidate in
`PurchaseOrderingPending`. The candidate had an audit, but the blocking
historical order had no operator incident identifying it.

**Fix:** the shared account-ordering helper now calls the existing
purchase-fact failure recorder on the blocking historical order. It
reuses the existing fact-review flag/error, audited snapshot CAS and
privacy-minimal Sentry payment reporter. Concurrent observers and
subsequent recovery attempts produce one durable error transition and
one incident carrying the blocking order ID/UID. Identical retries only
advance the existing check timestamp. The warning log now follows the
same deduplication result. No new database query shape, index, reward
state or eligibility exception is introduced; the principal timestamp
and unresolved eligibility hold remain unchanged.

The runbook now explicitly says **recover reliable payment-time evidence
through an audited correction first, then recheck the identified
historical order; recheck alone cannot invent the missing confirmation
time**. Operator, reason, before/after and incident correlation must be
retained. Unrecoverable evidence leaves rewards delayed; no invented
grant, denial or balance adjustment.

The real-Mongo missing-history regression now runs two concurrent
ordering observers followed by three recovery rounds and asserts one
incident, the correct blocking order identity, one durable fact-review
audit, retained hold, null confirmation and unchanged principal clock.
The later-payment control produces no incident.

## Previous P2 and retained design

Tim’s latest review confirms the disabled-offer ordering defect is
resolved for durable successful-payment history. New successful payments
record the pre-existing confirmation field independently of the offer
switch. Missing legacy confirmations are restored from existing audited
payment times in bounded batches of 20 within the candidate’s
account/environment, with snapshot CAS and actual before/after audit.
Both earlier-purchase and all-unresolved checks run again after each
batch; truncation never establishes completeness. No historical
Stripe/card calls or global worker return.

The offer switch controls new participation; frozen rewards still
recover when it is off. Claude’s prior non-blocking latency observation
is an intentional tradeoff: the existing one-second immediate window
remains, committed partial repairs are durable, and the existing
recovery job handles remaining backlog. Staging must measure actual
recovery latency; local tests are not a timing guarantee.

## Current-head automated review response

Codex review 5453771583 and Claude comment 6055811409 report no new code
defect; Claude explicitly confirms the P3 fix and regression coverage.
Both leave the actual runtime evidence and the requested
merge/acceptance sequence for authorized human review, not automated
approval.

Claude’s non-blocking correlation observation is accepted without
another state/field: the incident is deliberately deduplicated per
**blocking historical order**, whose ID/UID and audit identify the
repair target. It does not carry a direct candidate-order link; Sentry
is not claimed to supply that link. Candidate ordering-pending audits
remain available within the same account/environment. Adding a different
correlation per observing candidate would not improve the underlying
evidence repair and is unnecessary for this P3.

## Validation

This P3 update: **157 targeted backend/contract checks and 8 actual
local MongoDB ordering scenarios passed**. Ruff, formatting, types and
import contracts passed. Normal commit/push/CI gates remain in place.
The isolated local MongoDB instance and fixtures were cleaned up.

Earlier head `20d1f1875` passed 562 Platform/backend contract checks and
33 real-Mongo scenarios. Actual historical strict schemas at `bf8d0b791`
and `17fae8b101` accept the ordinary confirmation field; no new
serialized field is added. Source-hashed index measurements used 20,051
synthetic orders and 20,000 rewards: all seven current read paths used
indexes; confirmation/error CAS uses unique order ID. Previous 82
frontend checks are not claimed as rerun. Local Mongo is unencrypted:
none of this substitutes for deployed CSFLE or real Stripe Sandbox →
staging Lago evidence.

Current contract, execution and evidence:
- `docs/superpowers/specs/2026-10-08-platform-bonus-redemption.md`
- `services/claw-interface/docs/cron-triggers.md`
- `docs/staging-validation/2026-10-05-platform-bonus-retry-csfle.md`
-
`docs/staging-validation/2026-10-08-platform-bonus-query-index-audit.md`
-
`docs/staging-validation/2026-10-08-platform-bonus-redemption-index-results.json`

## Explicit decision requested from Tim: PM-owned acceptance after
staging rollout

The product manager asks you to approve this sequence: **formal review
approval → normal merge → complete Staging rollout/index builds →
immediate PM-owned Staging acceptance → production only after recorded
passing evidence**. Please state explicitly whether you accept this
sequence now that the P3 is fixed. This is a request to move the
outstanding runtime acceptance to the deployed Staging version, not to
waive it or to declare it already passed.

The reason is practical: the PM needs the complete deployed application
to exercise Checkout through Stripe Sandbox and actual staging Lago,
including webhook/recovery/concurrency behavior. Merging for Staging
acceptance does not constitute production sign-off. PM-owned acceptance
includes authenticated technical execution and retained evidence, not
just clicking the UI:

1. Run the exact-source encrypted probe through the real staging client:
seven surviving reads, deployed index inventory, four no-match writes,
isolated matched/duplicate confirmation restoration, source CAS/stale
rejection, durable audit and precise cleanup. Preserve sanitized
source/runtime hashes, operator/time, results and correlations.
2. Execute real Sandbox → staging Lago scenarios: first positive
purchase, zero then positive, ordinary previous card purchase without
reward, rewarded/reserved-card rejection and eligible new-card retry,
concurrent/replayed once-only delivery, uncertain occupancy, delayed
recovery, offer-off → on ordering and the newly signalled
missing-evidence case. Record ledger/DB outcomes and observed timing.
3. Any failed or missing evidence blocks production activation;
investigate and repair before sign-off. No real charges, manual balance
edits, encryption bypass or production deployment is authorized by this
request.

**Tim review 5453899989 (2026-10-08 08:35:51 UTC, exact head
`c6d2e62d0`) confirms the P3 resolved and no new concrete code defect,
but explicitly does not approve the proposed merge-before-staging
sequence. He requires the authenticated CSFLE and real Stripe/Lago
evidence before approval. Current evidence is still missing.** Required
CI/reviews and Auto Merge remain enabled. An authenticated operator can
alternatively run exact PR sources in an existing staging Pod before
merge, but the author has no authenticated execution route. If your
agent cannot approve the proposed sequence, please identify the specific
required human decision or an available authenticated
operator/job/access route, or explicitly say none is available. Please
distinguish an unresolved code defect from this acceptance-order
decision in your response.
```

