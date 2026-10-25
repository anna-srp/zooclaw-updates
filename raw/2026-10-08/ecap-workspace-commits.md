# SerendipityOneInc/ecap-workspace — commits 2026-10-08

## fix(platform): separate bonus attempts from redemption and accept Link cards (#4036)

- **SHA**: `13da07ddb5ce3905d5db145c09feb018004c0e25`
- **作者**: ericma-srp
- **日期**: 2026-10-08T14:09:55Z
- **PR**: #4036

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

### PR Body

## Summary
A Staging tester completed a zero-cash coupon checkout and then a $20 Link payment. Principal reached the wallet, but no $10 bonus row appeared and the offer disappeared. The public API confirmed `ineligible`/no bonus; the exact persisted rejection was not exposed. Reproduction traced the matching path: all wallets were rejected and only duplicate-card failures were retryable.

- Accept Stripe-verified Link credit/debit cards in the existing card integration, retaining positive-payment proof and the same account/card redemption uniqueness. Opaque Link, bank funding, prepaid/unknown funding and other wallets do not automatically qualify.
- Unify definitive qualification failures as **order-owned failed attempts**, separate from the account's one-time redemption. Save the failure before reassignment; use the same classification for Failed history, retry permission and offer visibility. Submitted/uncertain/credited rewards remain occupied. No new business status, collection, global history scan or repair loop.
- Existing safe `ineligible_card` records regain their conditional offer and visible failure without writes on GET. Persist their immutable snapshot before a later attempt. This does not retroactively credit old purchases or manually alter any balance.
- Keep immutable failure explanations separate from current eligibility: both failure types show retry guidance only when billing confirms an eligible, available offer. Legacy rejection plus an intervening ordinary paid purchase keeps its failure row but does not invite another payment; guidance also disappears after a successful redemption.
- Preserve legacy snapshots/strict storage readers and negotiate history v3 with cached v1/v2 clients. New verification holds are ignored by old workers until backend rollout completes. Both backend and frontend deploys are required.

The canonical [Platform product rules](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/bonus-attempt-redemption/web/platform/PRODUCT.md#first-top-up-reward) now describe the same eligibility contract: ordinary paid purchases disqualify, explicit rejected reward attempts do not consume eligibility, positively verified Link credit/debit cards are supported, and retry guidance always depends on current account eligibility.

## Test plan
- [x] 611 Platform backend regressions + CSFLE syntax guard; final focused purchase-proof/mixed-worker tests: 63 passed after adding the opaque-Link boundary.
- [x] 35 isolated real ordinary-Mongo tests: rejection exclusion, matched snapshot/duplicate guard, source reassignment, unique account/card reservation, ordering and old snapshots. No skipped tests.
- [x] Updated CSFLE probe tests, including matched new-reason snapshot/readback/conflict/cleanup; **these local tests are not encrypted-runtime proof**.
- [x] Actual main strict order reader round-trip retains the new audit snapshot; legacy verification reason list excludes the new hold.
- [x] 103 frontend tests across billing/router/client/preview; lint, typecheck, production build; real local-browser preview shows Failed + correct reason + retry offer with no console error on a fresh page.
- [x] Python static/architecture/complexity checks and all commit/push hooks. Product wording/layout and $10 amount unchanged except the necessary payment-method failure explanation.
- [x] Tim P2 regression: seven frontend cases fail before the correction; after it, 88 router/client tests and 22 backend attempt/retry tests pass. Includes legacy method rejection + intervening ordinary paid order -> ineligible offer, retained Failed reason, next purchase with no reward/ledger submission. Platform lint/typecheck/build and Python static checks pass. No backend production query or state change in this correction.
- [x] Tim P3 documentation correction: cross-checked PRODUCT.md against the account-history predicates, safe rejection rules, Stripe card proof and current-eligibility UI gate; relative acceptance link and diff whitespace verified. This follow-up changes documentation only; no new runtime behavior or tests.
- [ ] Actual Staging encrypted-client operations, real Stripe-to-Lago delivery, and direct-card/Link cross-account fingerprint equivalence after both deploys.

## Tim review / Staging acceptance request
Please review the code change and approve normal merge into main for Staging deployment, then the product manager will immediately accept the real encrypted/Stripe-to-Lago paths. This follows the requested Staging acceptance sequence; **merge is not production release authorization**. Keep required review and CI. Production release stays gated on recorded Staging acceptance.

Critical checks: zero-cash does not consume; verified Link card -> exactly one $10; rejected method/redeemed card -> Failed reason plus offer/retry guidance only while account eligibility remains; qualifying retry -> one credit with old failures retained; another account cannot redeem the same rewarded card, testing both direct-card -> Link and Link -> direct-card under the same Stripe account/environment; uncertain delivery never reopens. Engineering should retain encrypted probe results/audit correlation/cleanup and actual ledger evidence alongside PM screenshots. Compare the actual Charge card fingerprints securely; presence of a fingerprint is not proof that direct-card and Link identities are equivalent. If they differ or a second reward posts, stop production release and investigate. Current local tooling has no authenticated staging Pod access; no encrypted-runtime pass, actual Charge inspection, manual credit or deployment is claimed. An authorized operator may also run the exact source bundle before merge.

[Design](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/bonus-attempt-redemption/docs/superpowers/specs/2026-10-08-platform-bonus-attempt-redemption.md) · [Acceptance and evidence boundaries](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/bonus-attempt-redemption/docs/staging-validation/2026-10-08-bonus-attempt-redemption.md) · [Stripe Link card integration contract](https://docs.stripe.com/payments/link/link-payment-integrations)

Follow-up to merged #4024. Query changes remain bounded single-collection reads/classic CAS with existing account/environment and unique-ID indexes; the updated probe exercises the new two-action exclusion. Deployed index/query-plan and CSFLE checks remain part of Staging acceptance.




---

## fix(platform): simplify first-purchase bonus redemption and retry (#4024)

- **SHA**: `3c32605e4abee878f33590ca0459beb036e1ea9b`
- **作者**: ericma-srp
- **日期**: 2026-10-08T09:24:33Z
- **PR**: #4024

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

### PR Body

## Business rule and simplification

The product owner approved **each card may receive this reward once**, replacing “the card has never purchased on Platform.” Ordinary earlier card purchases without a reward do not exclude another eligible account. Account eligibility remains the first positive paid purchase, with the existing $10 amount and once-only account/scoped-card redemption. Verified $0 purchases neither earn nor consume eligibility; unknown cash is not zero. Ordinary prior positive purchases disqualify that account. Explicit duplicate-card failures remain immutable and allow an eligible new-card attempt. Uncertain/submitted delivery retains occupancy; refunds do not reopen it. Principal stays independent.

The global card-history/completeness queries, fact queue, worker and creation of four dedicated indexes are removed (existing deployed indexes are not dropped). Only the reward candidate’s own Stripe payment is verified. Existing uniqueness, ledger identity, reconciliation, source CAS, old-reader compatibility and failure snapshots remain. No new reward state, stored field, general campaign engine or budget subsystem; UI/Checkout unchanged in this update.

## Latest fix: Tim P3, review 5453069113

**Confirmed issue:** an older successful order lacking reliable payment-time evidence silently kept a newer candidate in `PurchaseOrderingPending`. The candidate had an audit, but the blocking historical order had no operator incident identifying it.

**Fix:** the shared account-ordering helper now calls the existing purchase-fact failure recorder on the blocking historical order. It reuses the existing fact-review flag/error, audited snapshot CAS and privacy-minimal Sentry payment reporter. Concurrent observers and subsequent recovery attempts produce one durable error transition and one incident carrying the blocking order ID/UID. Identical retries only advance the existing check timestamp. The warning log now follows the same deduplication result. No new database query shape, index, reward state or eligibility exception is introduced; the principal timestamp and unresolved eligibility hold remain unchanged.

The runbook now explicitly says **recover reliable payment-time evidence through an audited correction first, then recheck the identified historical order; recheck alone cannot invent the missing confirmation time**. Operator, reason, before/after and incident correlation must be retained. Unrecoverable evidence leaves rewards delayed; no invented grant, denial or balance adjustment.

The real-Mongo missing-history regression now runs two concurrent ordering observers followed by three recovery rounds and asserts one incident, the correct blocking order identity, one durable fact-review audit, retained hold, null confirmation and unchanged principal clock. The later-payment control produces no incident.

## Previous P2 and retained design

Tim’s latest review confirms the disabled-offer ordering defect is resolved for durable successful-payment history. New successful payments record the pre-existing confirmation field independently of the offer switch. Missing legacy confirmations are restored from existing audited payment times in bounded batches of 20 within the candidate’s account/environment, with snapshot CAS and actual before/after audit. Both earlier-purchase and all-unresolved checks run again after each batch; truncation never establishes completeness. No historical Stripe/card calls or global worker return.

The offer switch controls new participation; frozen rewards still recover when it is off. Claude’s prior non-blocking latency observation is an intentional tradeoff: the existing one-second immediate window remains, committed partial repairs are durable, and the existing recovery job handles remaining backlog. Staging must measure actual recovery latency; local tests are not a timing guarantee.

## Current-head automated review response

Codex review 5453771583 and Claude comment 6055811409 report no new code defect; Claude explicitly confirms the P3 fix and regression coverage. Both leave the actual runtime evidence and the requested merge/acceptance sequence for authorized human review, not automated approval.

Claude’s non-blocking correlation observation is accepted without another state/field: the incident is deliberately deduplicated per **blocking historical order**, whose ID/UID and audit identify the repair target. It does not carry a direct candidate-order link; Sentry is not claimed to supply that link. Candidate ordering-pending audits remain available within the same account/environment. Adding a different correlation per observing candidate would not improve the underlying evidence repair and is unnecessary for this P3.

## Validation

This P3 update: **157 targeted backend/contract checks and 8 actual local MongoDB ordering scenarios passed**. Ruff, formatting, types and import contracts passed. Normal commit/push/CI gates remain in place. The isolated local MongoDB instance and fixtures were cleaned up.

Earlier head `20d1f1875` passed 562 Platform/backend contract checks and 33 real-Mongo scenarios. Actual historical strict schemas at `bf8d0b791` and `17fae8b101` accept the ordinary confirmation field; no new serialized field is added. Source-hashed index measurements used 20,051 synthetic orders and 20,000 rewards: all seven current read paths used indexes; confirmation/error CAS uses unique order ID. Previous 82 frontend checks are not claimed as rerun. Local Mongo is unencrypted: none of this substitutes for deployed CSFLE or real Stripe Sandbox → staging Lago evidence.

Current contract, execution and evidence:
- `docs/superpowers/specs/2026-10-08-platform-bonus-redemption.md`
- `services/claw-interface/docs/cron-triggers.md`
- `docs/staging-validation/2026-10-05-platform-bonus-retry-csfle.md`
- `docs/staging-validation/2026-10-08-platform-bonus-query-index-audit.md`
- `docs/staging-validation/2026-10-08-platform-bonus-redemption-index-results.json`

## Explicit decision requested from Tim: PM-owned acceptance after staging rollout

The product manager asks you to approve this sequence: **formal review approval → normal merge → complete Staging rollout/index builds → immediate PM-owned Staging acceptance → production only after recorded passing evidence**. Please state explicitly whether you accept this sequence now that the P3 is fixed. This is a request to move the outstanding runtime acceptance to the deployed Staging version, not to waive it or to declare it already passed.

The reason is practical: the PM needs the complete deployed application to exercise Checkout through Stripe Sandbox and actual staging Lago, including webhook/recovery/concurrency behavior. Merging for Staging acceptance does not constitute production sign-off. PM-owned acceptance includes authenticated technical execution and retained evidence, not just clicking the UI:

1. Run the exact-source encrypted probe through the real staging client: seven surviving reads, deployed index inventory, four no-match writes, isolated matched/duplicate confirmation restoration, source CAS/stale rejection, durable audit and precise cleanup. Preserve sanitized source/runtime hashes, operator/time, results and correlations.
2. Execute real Sandbox → staging Lago scenarios: first positive purchase, zero then positive, ordinary previous card purchase without reward, rewarded/reserved-card rejection and eligible new-card retry, concurrent/replayed once-only delivery, uncertain occupancy, delayed recovery, offer-off → on ordering and the newly signalled missing-evidence case. Record ledger/DB outcomes and observed timing.
3. Any failed or missing evidence blocks production activation; investigate and repair before sign-off. No real charges, manual balance edits, encryption bypass or production deployment is authorized by this request.

**Tim review 5453899989 (2026-10-08 08:35:51 UTC, exact head `c6d2e62d0`) confirms the P3 resolved and no new concrete code defect, but explicitly does not approve the proposed merge-before-staging sequence. He requires the authenticated CSFLE and real Stripe/Lago evidence before approval. Current evidence is still missing.** Required CI/reviews and Auto Merge remain enabled. An authenticated operator can alternatively run exact PR sources in an existing staging Pod before merge, but the author has no authenticated execution route. If your agent cannot approve the proposed sequence, please identify the specific required human decision or an available authenticated operator/job/access route, or explicitly say none is available. Please distinguish an unresolved code defect from this acceptance-order decision in your response.


---

## fix(web): preserve appearance across loading boundaries (#4033)

- **SHA**: `706c9df8a81a754db23d8a207032b4a9386b4eba`
- **作者**: sharplee-srp
- **日期**: 2026-10-08T08:56:29Z
- **PR**: #4033

### Commit Message

```
fix(web): preserve appearance across loading boundaries (#4033)

## Summary
Keep the selected appearance when page content enters and leaves a
loading state. Move the shared `loading.tsx` into `[locale]`, below the
layout that owns the document and theme providers. Keep the dynamic
public replay fallback under `share/loading.tsx`, inside its own
document layout.

## Root cause
The root loading boundary wrapped the locale layout's `<html>`. In the
production browser, suspending that boundary caused React to remove the
document's theme class and `color-scheme`; reappearance restored only
the layout's font classes. The saved `dark` / `system` preference
remained intact, but the page rendered light.

The confirmed production trigger was navigating from Identity to Home. A
hard reload of Identity alone did not reproduce the reported symptom in
the diagnostic runs.

## Test plan
- Regression renders the actual locale layout with loading boundaries
derived from the route files, then suspends and resumes page content for
explicit dark and system-dark preferences.
- Confirmed both dark/system regression cases fail with the old root
loading placement and pass with the new placement.
- Passed 103 relevant tests across 14 files, TypeScript, ESLint, and web
governance checks. The pre-push changed-surface gate passed.

- Local browser E2E passed on `8baf36571`: local Next.js with real
staging APIs/account, Chromium on the browser host. Tested explicit dark
with OS light and system mode with OS dark.
- Explicit dark and system-dark modes survived Identity refresh,
Identity → Home navigation with the Home chunk delayed by 3 seconds, and
Home refresh. The actual loading fallback appeared in both runs; a DOM
observer recorded zero losses of the dark class or color-scheme. Stored
preferences and dark body colors remained correct.
- System mode also followed light → dark OS changes after refresh. No
page errors or failed API responses were observed. Identity/Home
screenshots were visually checked.

- Supplemental light-mode browser E2E passed on the same commit with OS
dark: select Light in settings, refresh Identity, navigate to Home with
its chunk delayed by 3 seconds, and refresh Home. The actual loading
fallback appeared; `html.light`, `color-scheme: light`, the stored light
preference and light body background persisted, with no dark class or
missing-theme mutations. No page errors or failed API responses were
observed. The Home screenshot was visually checked.

This validates local Web against staging APIs. Deployed production
validation still requires release; this PR does not deploy the change.
```

### PR Body

## Summary
Keep the selected appearance when page content enters and leaves a loading state. Move the shared `loading.tsx` into `[locale]`, below the layout that owns the document and theme providers. Keep the dynamic public replay fallback under `share/loading.tsx`, inside its own document layout.

## Root cause
The root loading boundary wrapped the locale layout's `<html>`. In the production browser, suspending that boundary caused React to remove the document's theme class and `color-scheme`; reappearance restored only the layout's font classes. The saved `dark` / `system` preference remained intact, but the page rendered light.

The confirmed production trigger was navigating from Identity to Home. A hard reload of Identity alone did not reproduce the reported symptom in the diagnostic runs.

## Test plan
- Regression renders the actual locale layout with loading boundaries derived from the route files, then suspends and resumes page content for explicit dark and system-dark preferences.
- Confirmed both dark/system regression cases fail with the old root loading placement and pass with the new placement.
- Passed 103 relevant tests across 14 files, TypeScript, ESLint, and web governance checks. The pre-push changed-surface gate passed.

- Local browser E2E passed on `8baf36571`: local Next.js with real staging APIs/account, Chromium on the browser host. Tested explicit dark with OS light and system mode with OS dark.
- Explicit dark and system-dark modes survived Identity refresh, Identity → Home navigation with the Home chunk delayed by 3 seconds, and Home refresh. The actual loading fallback appeared in both runs; a DOM observer recorded zero losses of the dark class or color-scheme. Stored preferences and dark body colors remained correct.
- System mode also followed light → dark OS changes after refresh. No page errors or failed API responses were observed. Identity/Home screenshots were visually checked.

- Supplemental light-mode browser E2E passed on the same commit with OS dark: select Light in settings, refresh Identity, navigate to Home with its chunk delayed by 3 seconds, and refresh Home. The actual loading fallback appeared; `html.light`, `color-scheme: light`, the stored light preference and light body background persisted, with no dark class or missing-theme mutations. No page errors or failed API responses were observed. The Home screenshot was visually checked.

This validates local Web against staging APIs. Deployed production validation still requires release; this PR does not deploy the change.


---

## fix(agents): validate environment using runtime resource class (#4032)

- **SHA**: `789e9b4226dbdbe29938b961838ff4573e807875`
- **作者**: kaka-srp
- **日期**: 2026-10-08T07:54:16Z
- **PR**: #4032

### Commit Message

```
fix(agents): validate environment using runtime resource class (#4032)

## Summary

Applying a saved self-evolving Agent Revision could fail with an
environment-build 404 for Pro or Ultra Agents even when their exact
environment version was ready. Validate the environment using the
Agent's Engine-reported Sandbox resource class, matching environment
materialization and preview; retain the existing Starter fallback when
the projection is absent.

## Root cause

The application readiness gate always queried the Starter build.
Environment materialization builds only the actual Agent class, so the
requested Starter variant could be missing. The Revision was already
saved while the active runtime configuration remained unchanged.

## Test plan

- [x] New regressions run through the real readiness gate and
application path. Before the fix, the selected tests produced 6 failures
and 2 passes; after the fix they pass.
- [x] Cover Starter, Pro, Ultra and the absent-class fallback; a missing
unrelated class must not block a ready environment. Reapplying a
successful Revision remains idempotent.
- [x] Cover building/failed dependencies blocking activation and an
empty-operations Settings retry applying the same saved Revision after
readiness recovers.
- [x] Six related test files: 101 passed.
- [x] `bash scripts/verify-local.sh --py-static`: Ruff, formatting,
Pyright and all eight import contracts passed.
- [ ] Staging and production recovery after backend deployment; no live
Agent was modified during implementation.
```

### PR Body

## Summary

Applying a saved self-evolving Agent Revision could fail with an environment-build 404 for Pro or Ultra Agents even when their exact environment version was ready. Validate the environment using the Agent's Engine-reported Sandbox resource class, matching environment materialization and preview; retain the existing Starter fallback when the projection is absent.

## Root cause

The application readiness gate always queried the Starter build. Environment materialization builds only the actual Agent class, so the requested Starter variant could be missing. The Revision was already saved while the active runtime configuration remained unchanged.

## Test plan

- [x] New regressions run through the real readiness gate and application path. Before the fix, the selected tests produced 6 failures and 2 passes; after the fix they pass.
- [x] Cover Starter, Pro, Ultra and the absent-class fallback; a missing unrelated class must not block a ready environment. Reapplying a successful Revision remains idempotent.
- [x] Cover building/failed dependencies blocking activation and an empty-operations Settings retry applying the same saved Revision after readiness recovers.
- [x] Six related test files: 101 passed.
- [x] `bash scripts/verify-local.sh --py-static`: Ruff, formatting, Pyright and all eight import contracts passed.
- [ ] Staging and production recovery after backend deployment; no live Agent was modified during implementation.


---

## chore(skills): strengthen design review and targeted re-review (#4030)

- **SHA**: `9a5e1b3d0d8c72b5313729c5b90f787f23a80968`
- **作者**: kaka-srp
- **日期**: 2026-10-08T06:51:57Z
- **PR**: #4030

### Commit Message

```
chore(skills): strengthen design review and targeted re-review (#4030)

## Summary

- Strengthen the existing code-review skill's checks for
overimplementation, premature generalization, and unnecessary scope
expansion while preserving required safety and compatibility work.
- Assess architectural ownership, existing mechanisms, real complexity
reduction, and plan defects using concrete evidence and bounded
alternatives with tradeoffs.
- Add targeted re-review: recover the exact reviewed baseline, verify
each prior finding, preserve rejected/deferred dispositions, inspect
fixes for regressions, and broaden only when the affected design
requires it.
- Keep this a one-file skill change; no new review framework,
dependencies, or production code changes.
- Follow-up review fix: targeted re-review includes uncommitted edits
only when the explicit review scope includes the working tree; a
selected PR/revision remains authoritative.

## Test plan

- [x] Skill structure: `python3
/home/node/.codex/skills/.system/skill-creator/scripts/quick_validate.py
.agents/skills/code-review`
- [x] Shared skill wiring: `bash scripts/sync-agent-skills.sh --check`
- [x] Skill regression checks: `bash scripts/sync-agent-skills.test.sh`
- [x] Changed-surface gate: `bash scripts/verify-changed.sh`
- [x] `git diff --check`
- [x] Manually inspected the full skill and diff for evidence
thresholds, read-only boundaries, scope control, and re-review closure
semantics.

Validation limitation: these checks verify skill structure and
repository integration, not model review quality. No independent
model-behavior evaluation was run.
```

### PR Body

## Summary

- Strengthen the existing code-review skill's checks for overimplementation, premature generalization, and unnecessary scope expansion while preserving required safety and compatibility work.
- Assess architectural ownership, existing mechanisms, real complexity reduction, and plan defects using concrete evidence and bounded alternatives with tradeoffs.
- Add targeted re-review: recover the exact reviewed baseline, verify each prior finding, preserve rejected/deferred dispositions, inspect fixes for regressions, and broaden only when the affected design requires it.
- Keep this a one-file skill change; no new review framework, dependencies, or production code changes.
- Follow-up review fix: targeted re-review includes uncommitted edits only when the explicit review scope includes the working tree; a selected PR/revision remains authoritative.

## Test plan

- [x] Skill structure: `python3 /home/node/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/code-review`
- [x] Shared skill wiring: `bash scripts/sync-agent-skills.sh --check`
- [x] Skill regression checks: `bash scripts/sync-agent-skills.test.sh`
- [x] Changed-surface gate: `bash scripts/verify-changed.sh`
- [x] `git diff --check`
- [x] Manually inspected the full skill and diff for evidence thresholds, read-only boundaries, scope control, and re-review closure semantics.

Validation limitation: these checks verify skill structure and repository integration, not model review quality. No independent model-behavior evaluation was run.


---
