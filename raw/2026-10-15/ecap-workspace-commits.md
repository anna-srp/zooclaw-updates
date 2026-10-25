# SerendipityOneInc/ecap-workspace — commits 2026-10-15

## fix(billing): reuse enterprise checkout and surface workspace errors (#4081)

- **SHA**: `bc96db72666333ddb003a971e05b85c9f3782261`
- **作者**: kaka-srp
- **日期**: 2026-10-15T09:23:39Z
- **PR**: #4081

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

### PR Body

## Summary
- Reuse the original order and open, unpaid Stripe Checkout for the same enterprise/vertical-pack purchase. Serialize attempts with the existing buyer checkout lease, and recover lost responses with the original persisted request and idempotency key.
- Preserve conversation/history error messages in Agent Workspace and stop showing the chat loading surface after a load failure. Existing query retries and successful reopening continue to work.

Fixes #4060.
Related to #3728: this PR addresses only frontend error propagation and loading presentation. Legacy direct/thread binding compatibility remains outside this change, so #3728 stays open.

## Root cause
Enterprise Checkout previously generated a fresh order/key on every attempt and only checked active agreements. Repeated clicks, parallel requests, or a lost Stripe response could leave multiple payable Sessions. Nested workspace view models also discarded already-normalized error strings while history remained unavailable.

## Implementation boundaries
- Reuse existing bounded order scans, payment audit events, checkout uncertainty/expiry handling, and guarded state transitions. Unknown or changed purchases block another Checkout; provider-confirmed expiration allows a fresh purchase.
- Compare addon sets independently of order without modifying the original saved snapshot or Stripe parameters, including timeout recovery.
- Checkout serialization is scoped to the same buyer. Cross-administrator team concurrency and live billing repairs are outside this PR.

## Test plan
- [x] 339 relevant backend tests passed before the final addon-order fix; 77 focused enterprise checkout, subscription, and Managed Payments tests passed after the final fixes, including both new addon-order regressions.
- [x] 87 relevant frontend tests passed; frontend TypeScript and ESLint passed.
- [x] Backend Ruff, formatting, full Pyright and import-linter passed after the final fix.
- [x] Adapted the existing Managed Payments fixture to the extracted checkout module and real persisted-order/audit flow after CI exposed stale patch targets.
- [x] Astra local review completed; its P2 addon-order finding was fixed and targeted re-review found no new issues.
- [ ] Real Stripe, encrypted MongoDB client, and deployed browser end-to-end validation were not run.

## Review follow-up
- The suggested agreement-check race does not establish a new same-buyer duplicate: an older unfinished/paid-unfulfilled order is scanned before the agreement read; a matching recovery reuses its original Session/key. Another team administrator creating an agreement is the explicitly excluded cross-administrator case.
- `scheduled_for_subscription_agreement_id` is explicitly written when reserving a scheduled package-change target. A target without provider-attempt markers is not a live Checkout; ordinary legacy Stripe purchases without that marker remain blocked for reconciliation.
- Workspace `loadError` and `status.error` intentionally derive from the same transport error. The reviewer did not identify a current failure from that wiring, so no additional frontend refactor was added.


---

## fix(agents): make definition deletion safely retryable (#4080)

- **SHA**: `030cc4a4164a2305dadf3b425fe5d3be8851b179`
- **作者**: kaka-srp
- **日期**: 2026-10-15T07:35:20Z
- **PR**: #4080

### Commit Message

```
fix(agents): make definition deletion safely retryable (#4080)

## Summary
- Make interrupted native Agent-definition deletions retryable against
the same Agent/Computer identity. Persist deletion intent and a
renewable lease, and fence success/failure writes with the current
operation/token so late callbacks cannot overwrite a newer attempt or a
terminal state.
- Reject new Build, settings, start and runtime-recovery writes once
deletion begins. Preserve existing read-only source/history access and
the existing integration cleanup mechanism.
- Allow organization shutdown to stop Agents whose deletion failed,
without overwriting their deletion state, lease or integration cleanup.
Keep those Agents non-restorable and preserve the shared-Computer
isolation branch.

## Root cause
Deletion entry points and claims rejected retained `uninstalling` rows,
while finalization and failure writes were not bound to an execution
attempt. Authoring entry points also applied inconsistent lifecycle
checks. Shutdown and recovery share persistence helpers, so deletion
guards must block reactivation while still allowing shutdown to finish
safely.

## Test plan
- [x] 747 focused regression tests passed across Agent development,
authoring, deletion, lifecycle, integration cleanup and runtime
shutdown/recovery.
- [x] 23 additional enterprise-invite handoff tests passed.
- [x] 151 affected ChangeSet read/write, authoring, apply,
route-boundary and repository contract tests passed after review
corrections.
- [x] Real local MongoDB tests: concurrent claims/takeovers, stale
callbacks, failure retries, organization shutdown with a failed
deletion, repeated shutdown, and deletion starting/completing during
shutdown.
- [x] Backend static verification: Ruff, formatting, Pyright and
import-linter; complexity and source duplication checks passed.
- [x] Local code review and regression coverage for deletion/shutdown
interaction.
- [x] Staging encrypted-client compatibility: 5 deletion statements and
8 shutdown/recovery statements executed with randomly generated
nonexistent identities. Encryption remained enabled; no documents
matched or were modified. This validates query compatibility, not full
business E2E.
- [ ] Full business-resource cross-service kill/restart E2E was not
performed.

Real Mongo tests require an explicit local
`TEST_AGENT_DELETION_MONGO_URI`; they skip when it is unset.

## Rollout
Backend only. `AGENT_DELETION_RECOVERY_ENABLED` defaults to `false`;
enable after all relevant writers are upgraded and old requests have
drained. Disabling the flag prevents new operations but existing
deletion records continue through the leased path. Do not roll back to
writers that ignore retained deletion intent while operations remain
pending.

Recovery is triggered by retrying the existing delete endpoint; no new
background scanner or client response contract is introduced. Creation
recovery and strict fencing of already-in-flight remote writes remain
outside this change.


## Related issues
- Related to #3963: adds deletion-time write admission for new authoring
operations. Strict fencing of already-in-flight remote
skill/Environment/config side effects remains outside this PR; this
issue stays open.
- Related to #3960: this PR covers interrupted definition deletion only.
Recovery of interrupted creation stuck in `installing` remains outside
this PR; this issue stays open.
```

### PR Body

## Summary
- Make interrupted native Agent-definition deletions retryable against the same Agent/Computer identity. Persist deletion intent and a renewable lease, and fence success/failure writes with the current operation/token so late callbacks cannot overwrite a newer attempt or a terminal state.
- Reject new Build, settings, start and runtime-recovery writes once deletion begins. Preserve existing read-only source/history access and the existing integration cleanup mechanism.
- Allow organization shutdown to stop Agents whose deletion failed, without overwriting their deletion state, lease or integration cleanup. Keep those Agents non-restorable and preserve the shared-Computer isolation branch.

## Root cause
Deletion entry points and claims rejected retained `uninstalling` rows, while finalization and failure writes were not bound to an execution attempt. Authoring entry points also applied inconsistent lifecycle checks. Shutdown and recovery share persistence helpers, so deletion guards must block reactivation while still allowing shutdown to finish safely.

## Test plan
- [x] 747 focused regression tests passed across Agent development, authoring, deletion, lifecycle, integration cleanup and runtime shutdown/recovery.
- [x] 23 additional enterprise-invite handoff tests passed.
- [x] 151 affected ChangeSet read/write, authoring, apply, route-boundary and repository contract tests passed after review corrections.
- [x] Real local MongoDB tests: concurrent claims/takeovers, stale callbacks, failure retries, organization shutdown with a failed deletion, repeated shutdown, and deletion starting/completing during shutdown.
- [x] Backend static verification: Ruff, formatting, Pyright and import-linter; complexity and source duplication checks passed.
- [x] Local code review and regression coverage for deletion/shutdown interaction.
- [x] Staging encrypted-client compatibility: 5 deletion statements and 8 shutdown/recovery statements executed with randomly generated nonexistent identities. Encryption remained enabled; no documents matched or were modified. This validates query compatibility, not full business E2E.
- [ ] Full business-resource cross-service kill/restart E2E was not performed.

Real Mongo tests require an explicit local `TEST_AGENT_DELETION_MONGO_URI`; they skip when it is unset.

## Rollout
Backend only. `AGENT_DELETION_RECOVERY_ENABLED` defaults to `false`; enable after all relevant writers are upgraded and old requests have drained. Disabling the flag prevents new operations but existing deletion records continue through the leased path. Do not roll back to writers that ignore retained deletion intent while operations remain pending.

Recovery is triggered by retrying the existing delete endpoint; no new background scanner or client response contract is introduced. Creation recovery and strict fencing of already-in-flight remote writes remain outside this change.


## Related issues
- Related to #3963: adds deletion-time write admission for new authoring operations. Strict fencing of already-in-flight remote skill/Environment/config side effects remains outside this PR; this issue stays open.
- Related to #3960: this PR covers interrupted definition deletion only. Recovery of interrupted creation stuck in `installing` remains outside this PR; this issue stays open.


---

## fix(chat): combine model and thinking effort controls (#4079)

- **SHA**: `a8f86c12f57b8f1b0bb2270471bb6aed5de15dc3`
- **作者**: kaka-srp
- **日期**: 2026-10-15T04:00:21Z
- **PR**: #4079

### Commit Message

```
fix(chat): combine model and thinking effort controls (#4079)

## Summary
- Combine model and thinking effort into one compact composer control,
with a muted effort label and one dropdown arrow.
- Keep model search and common/more models in the same menu; put
model-specific effort choices below the list and retain distinct Model
default and Follow Agent actions.
- Display the current runtime default, including inherited native
overrides, while explicit Task drafts use their own model default.

## Root cause
The composer rendered model and effort as two independent controls. The
combined picker now exposes recovery actions even when the model catalog
fails or is empty, and preserves sticky search for existing picker
consumers.

## Test plan
- App and shared chat-ui TypeScript/ESLint; frontend governance guards.
- 106 targeted app tests (composer, Task model, launcher and runtime
model query), plus 38 shared model picker tests; the affected suite was
rerun after correcting its fixed-Task fixture.
- Real staging-backed browser checks: effort save and reload, Model
default, Follow Agent, Chinese/dark theme and 390px viewport.
- Real Agent Settings menu: scrolling 100px preserves the search input
position.
- Astra local review: fixed two P2 findings (recovery actions and actual
default labels) and one P3 finding (sticky search); targeted re-review
confirmed all three addressed.

Related issue: #4073. This PR covers the agreed Agent/Web scope; iOS and
Schedule configuration/UI were excluded from this iteration.
```

### PR Body

## Summary
- Combine model and thinking effort into one compact composer control, with a muted effort label and one dropdown arrow.
- Keep model search and common/more models in the same menu; put model-specific effort choices below the list and retain distinct Model default and Follow Agent actions.
- Display the current runtime default, including inherited native overrides, while explicit Task drafts use their own model default.

## Root cause
The composer rendered model and effort as two independent controls. The combined picker now exposes recovery actions even when the model catalog fails or is empty, and preserves sticky search for existing picker consumers.

## Test plan
- App and shared chat-ui TypeScript/ESLint; frontend governance guards.
- 106 targeted app tests (composer, Task model, launcher and runtime model query), plus 38 shared model picker tests; the affected suite was rerun after correcting its fixed-Task fixture.
- Real staging-backed browser checks: effort save and reload, Model default, Follow Agent, Chinese/dark theme and 390px viewport.
- Real Agent Settings menu: scrolling 100px preserves the search input position.
- Astra local review: fixed two P2 findings (recovery actions and actual default labels) and one P3 finding (sticky search); targeted re-review confirmed all three addressed.

Related issue: #4073. This PR covers the agreed Agent/Web scope; iOS and Schedule configuration/UI were excluded from this iteration.


---

## feat(agents): add model-bound agent and task thinking controls (#4075)

- **SHA**: `816320a0e083948c796eca00c5723409be132da5`
- **作者**: kaka-srp
- **日期**: 2026-10-15T02:38:04Z
- **PR**: #4075

### Commit Message

```
feat(agents): add model-bound agent and task thinking controls (#4075)

Selecting thinking effort now saves it with the selected model. Agent
defaults live in Revision source and follow publish/share/rollback. Task
overrides persist from the next turn: choosing an effort fixes the
displayed model, switching models resets effort, Model default retains
the fixed model, and Follow Agent clears the complete pair.

Scope is Agent Settings and Web Task controls only. iOS and Schedule
configuration/UI are unchanged. ECAP explicitly saves or clears the
complete Agent pair, including old model-only clients and
personal-subscription exit. Engine global Agent merging,
Auto/fallback/subagent/Schedule default inheritance remain unchanged;
companion #2002 only adds Task support. Ship companion Engine
controld/workers before ECAP backend and Web. No merge/deployment is
included.

Validation:
- Python: 184 relevant tests (182 original cases plus 2 legacy Auto
alignment cases), plus 13 ownership/Environment fixture cases; ruff,
format, pyright, 8 import contracts and file-length gate pass.
- Web: 8 files / 158 tests; governance, tsc and changed-file ESLint
pass. Actual Chrome mock interactions verify Low, Model default and
Follow Agent persistence across reload, with 0 page errors.
- Real existing owned local Agent: 12 successful provider turns through
the actual ECAP service layer, staging encrypted Mongo/Billing, shared
local PostgreSQL/Temporal/Engine and staging LiteLLM. Transcript
metadata confirms effort, persistent/isolation behavior, model-switch
defaults, Agent updates and restored source. Real concurrent CAS
produces one success and one 409; stale config is rejected.
- This round uses service-layer authentication context from the existing
owned Account; browser bearer and real ACS/Mattermost delivery were not
rerun. Browser validation is explicitly mock. No wire interceptor was
used.
- Original source/model/effort/Environment 14 restored; 2
successful-test and 6 debug Tasks independently confirmed archived;
original shared application lane restored. 3 additional real debug turns
are recorded separately.
- Astra's reset response entitlement drift and legacy Auto baseline
conflict were fixed. Targeted Astra re-review marked both ADDRESSED with
no new blockers; regression cases cover POST/GET equality and preserved
direct-edit conflicts.

Design and reproducible evidence:
docs/superpowers/specs/2026-10-14-agent-thinking-levels.md,
docs/validation/2026-10-14-agent-thinking-real.md and
docs/validation/2026-10-14-thinking-pair-real.json. Earlier validation
is marked superseded.

Dependency:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/2002

CI fixture follow-up: subscription runtime-grant fixtures now
distinguish the authorized connection GET from the Agent-state GET,
preserving opaque runtime ownership assertions. Environment isolation
fixtures assert the atomic thinking:null alongside the model switch.
Production behavior is unchanged by this follow-up.
```

### PR Body

Selecting thinking effort now saves it with the selected model. Agent defaults live in Revision source and follow publish/share/rollback. Task overrides persist from the next turn: choosing an effort fixes the displayed model, switching models resets effort, Model default retains the fixed model, and Follow Agent clears the complete pair.

Scope is Agent Settings and Web Task controls only. iOS and Schedule configuration/UI are unchanged. ECAP explicitly saves or clears the complete Agent pair, including old model-only clients and personal-subscription exit. Engine global Agent merging, Auto/fallback/subagent/Schedule default inheritance remain unchanged; companion #2002 only adds Task support. Ship companion Engine controld/workers before ECAP backend and Web. No merge/deployment is included.

Validation:
- Python: 184 relevant tests (182 original cases plus 2 legacy Auto alignment cases), plus 13 ownership/Environment fixture cases; ruff, format, pyright, 8 import contracts and file-length gate pass.
- Web: 8 files / 158 tests; governance, tsc and changed-file ESLint pass. Actual Chrome mock interactions verify Low, Model default and Follow Agent persistence across reload, with 0 page errors.
- Real existing owned local Agent: 12 successful provider turns through the actual ECAP service layer, staging encrypted Mongo/Billing, shared local PostgreSQL/Temporal/Engine and staging LiteLLM. Transcript metadata confirms effort, persistent/isolation behavior, model-switch defaults, Agent updates and restored source. Real concurrent CAS produces one success and one 409; stale config is rejected.
- This round uses service-layer authentication context from the existing owned Account; browser bearer and real ACS/Mattermost delivery were not rerun. Browser validation is explicitly mock. No wire interceptor was used.
- Original source/model/effort/Environment 14 restored; 2 successful-test and 6 debug Tasks independently confirmed archived; original shared application lane restored. 3 additional real debug turns are recorded separately.
- Astra's reset response entitlement drift and legacy Auto baseline conflict were fixed. Targeted Astra re-review marked both ADDRESSED with no new blockers; regression cases cover POST/GET equality and preserved direct-edit conflicts.

Design and reproducible evidence: docs/superpowers/specs/2026-10-14-agent-thinking-levels.md, docs/validation/2026-10-14-agent-thinking-real.md and docs/validation/2026-10-14-thinking-pair-real.json. Earlier validation is marked superseded.

Dependency: https://github.com/SerendipityOneInc/zooclaw-engine/pull/2002

CI fixture follow-up: subscription runtime-grant fixtures now distinguish the authorized connection GET from the Agent-state GET, preserving opaque runtime ownership assertions. Environment isolation fixtures assert the atomic thinking:null alongside the model switch. Production behavior is unchanged by this follow-up.

Related issue: #4073. This PR covers the agreed Agent/Web scope; iOS and Schedule configuration/UI were excluded from this iteration.


---
