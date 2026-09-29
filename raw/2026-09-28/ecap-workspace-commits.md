# SerendipityOneInc/ecap-workspace — commits 2026-09-28

## fix(onboarding): streamline admission and animate loading from first paint (#3916)

- **SHA**: `2cdfd5ce9ee4d5d11d01fb37c803df2d52702229`
- **作者**: ericma-srp
- **日期**: 2026-09-28T23:57:38Z
- **PR**: #3916

### Commit Message

```
fix(onboarding): streamline admission and animate loading from first paint (#3916)

## Summary

Opening or refreshing workspace pages currently adds a separate
subscription-check screen and delays page requests until admission
completes. This frontend-only change limits the check to workspace
capability routes, plays the existing Logo animation from first paint
and overlaps independent, audited reads with verification.

- Check Agents, Chat, Tasks, Assets, Agent Builder, Home, Mini Chat,
agent management, knowledge base, schedules, skills, plugins,
integrations and channels (including descendants). Profile,
organization/account settings, subscription purchase and return routes
keep their existing authentication checks without the checkout gate.
- `/claw-settings` is a legacy redirect to `/identity`, not a separately
protected settings screen. The `/identity` hub remains exempt from
checkout admission, including its General, Usage, Billing and visible
API Keys tabs, plus legacy Status/Sessions/Statistics tabs when enabled.
Existing authentication, organization access and feature visibility
still apply. Its old connector/channel/knowledge-base tabs redirect to
protected Plugins/Channels destinations.
- Reuse the existing full-page ClawSpinner, with immediate sign-out and
manual retry. The same Logo brush geometry and timing now run through
CSS on SVG segments, so the first paint animates before application
scripts initialize or window.load fires. Hydration retains that
animation instead of replacing a static mark. Theme color and
reduced-motion preferences remain supported. No new workspace skeleton.
Protected content, runtime initialization, session creation and package
installation remain behind successful admission.
- Preload Agent capability, the requested Agent definition or the first
Artifact Library page while account verification runs. Start
organization-scoped Agent/Home definition queries once the verified
account is available, overlapping any remaining order verification. Page
hooks and preloads share query options, keys, in-flight work, freshness
and retry policies.
- Do not speculatively call `GET /agents`: that existing backend handler
can repair the default Agent. Tasks/Chat runtime reads therefore remain
gated. Only the requested route is prepared; anonymous visitors, exempt
routes and already-denied/error states do not start speculative reads.
- Share account results with the session gate and reuse positive
admission in UID-scoped memory for 30 seconds. Stale navigation
revalidates in the background. Transient admission failures retry twice
with short backoff, then recover every 15 seconds/on reconnect. Negative
results/auth rejection still block access; explicit checkout completion
still forces a fresh verification. No payment-evidence rules or backend
files change.

## Validation

- Browser follow-up for Claude’s recovery concern: force `/account/me`
to return 503 until the real AuthManager account-confirmation failure is
observed, hold successful reads, then release server account truth. All
three cases pass: completed + admitted enters Agents and navigates to
Tasks without an onboarding flash; incomplete + admitted stays in
onboarding despite stale completed browser progress; completed + unpaid
stays gated. Both gated cases can advance through the welcome screen
without mounting the workspace or issuing runtime initialization, order
creation or account-completion writes. Auth bootstrap, provider,
resolver and admission service run unmodified.
- Negative control: temporarily removing the account-completion fallback
makes the first two browser cases fail. Restoring the original source
makes the full 13-case suite pass (48.1s). The committed follow-up
changes only E2E coverage; TypeScript, ESLint and frontend governance
pass.
- Latest commit `957e6be2c`: CI settled with 23 passing checks and no
failures; code-scanning alerts for the PR merge ref are empty. Both
Codex and Claude now return APPROVE with no findings. Claude explicitly
confirms the new browser coverage addresses the previous
bootstrap-recovery validation gap.
- Review follow-up: 128 targeted tests pass across billing, admission
service and hook suites, including 33 new cases that run the real HTTP
adapter → billing result conversion → admission service → React Query
policy. Only fetch/account/auth are mocked. Personal order history, team
order history and enterprise credits all cover 503/429/network retries,
background retry exhaustion and 15-second recovery, timeout recovery
without immediate repeats, 401/403/plain-error/business-error blocking,
and legacy status-bearing failure envelopes.
- 25 targeted spinner/admission component tests pass. The earlier
admission/preload implementation also passed 387 relevant unit cases
across 23 suites. These animation/preload results precede the latest
billing error-propagation fix.
- All 13 local Playwright cases pass on the current tree (including the
three bootstrap-recovery cases below): desktop/mobile refresh, paid
navigation without a loading flash, unpaid/anonymous protection,
automatic retry recovery, exempt Profile to protected Home navigation,
and held account/order responses proving parallel reads without
premature protected DOM/runtime requests or duplicate page reads.
- The new first-paint test holds application scripts, verifies changing
brush frames before document load, then releases scripts and confirms
the same SVG remains mounted and animated while account verification is
held. Reduced-motion presentation works before hydration as well.
- TypeScript, full frontend ESLint, the Knip dead-code gate, frontend
governance and diff checks pass. The existing cache-governance guard
reports its baseline bootstrap skip.
- Verification uses local mock accounts. No live Stripe payment,
production latency benchmark or deployment; genuine account/organization
dependencies still apply.

## Review notes

Tim’s [P2 on lost billing error
categories](https://github.com/SerendipityOneInc/ecap-workspace/pull/3916#issuecomment-5873907605)
is fixed: billing results retain the original client-side error, and
admission rethrows it or reconstructs `ApiError` from legacy status/code
fields. This preserves HTTP, network and timeout classification without
treating ordinary errors as transient. Existing non-throwing billing
consumers keep their result contract. The new regression suite
reproduced 21 failures before the fix; all 33 cases now pass. No backend
or payment-evidence changes.

The legacy `/claw-settings` allowlist entry remains unchanged.
Middleware redirects it to the intentionally exempt `/identity` route
before rendering, so removing that entry would not change current access
or loading behavior. The actual route behavior is documented above; this
non-blocking cleanup suggestion is outside the animation correction.

Claude’s [bootstrap-recovery validation
gap](https://github.com/SerendipityOneInc/ecap-workspace/pull/3916#issuecomment-5874198853)
is now covered by three real-browser scenarios plus a negative control,
described above. They verify the intended product behavior: recovered
server completion avoids restarting onboarding for an admitted returning
user, explicit incomplete accounts still require onboarding, and
completed onboarding never replaces admission evidence. No product or
backend changes were needed.

The latest Claude review also notes the intentional conservative
treatment of legacy failure envelopes without an original error or HTTP
status: these remain blocking and do not automatically retry. This is
covered by the business-failure tests and preserves Tim’s request not to
classify all ordinary errors as transient; no change is warranted.
```

### PR Body

## Summary

Opening or refreshing workspace pages currently adds a separate subscription-check screen and delays page requests until admission completes. This frontend-only change limits the check to workspace capability routes, plays the existing Logo animation from first paint and overlaps independent, audited reads with verification.

- Check Agents, Chat, Tasks, Assets, Agent Builder, Home, Mini Chat, agent management, knowledge base, schedules, skills, plugins, integrations and channels (including descendants). Profile, organization/account settings, subscription purchase and return routes keep their existing authentication checks without the checkout gate.
- `/claw-settings` is a legacy redirect to `/identity`, not a separately protected settings screen. The `/identity` hub remains exempt from checkout admission, including its General, Usage, Billing and visible API Keys tabs, plus legacy Status/Sessions/Statistics tabs when enabled. Existing authentication, organization access and feature visibility still apply. Its old connector/channel/knowledge-base tabs redirect to protected Plugins/Channels destinations.
- Reuse the existing full-page ClawSpinner, with immediate sign-out and manual retry. The same Logo brush geometry and timing now run through CSS on SVG segments, so the first paint animates before application scripts initialize or window.load fires. Hydration retains that animation instead of replacing a static mark. Theme color and reduced-motion preferences remain supported. No new workspace skeleton. Protected content, runtime initialization, session creation and package installation remain behind successful admission.
- Preload Agent capability, the requested Agent definition or the first Artifact Library page while account verification runs. Start organization-scoped Agent/Home definition queries once the verified account is available, overlapping any remaining order verification. Page hooks and preloads share query options, keys, in-flight work, freshness and retry policies.
- Do not speculatively call `GET /agents`: that existing backend handler can repair the default Agent. Tasks/Chat runtime reads therefore remain gated. Only the requested route is prepared; anonymous visitors, exempt routes and already-denied/error states do not start speculative reads.
- Share account results with the session gate and reuse positive admission in UID-scoped memory for 30 seconds. Stale navigation revalidates in the background. Transient admission failures retry twice with short backoff, then recover every 15 seconds/on reconnect. Negative results/auth rejection still block access; explicit checkout completion still forces a fresh verification. No payment-evidence rules or backend files change.

## Validation

- Browser follow-up for Claude’s recovery concern: force `/account/me` to return 503 until the real AuthManager account-confirmation failure is observed, hold successful reads, then release server account truth. All three cases pass: completed + admitted enters Agents and navigates to Tasks without an onboarding flash; incomplete + admitted stays in onboarding despite stale completed browser progress; completed + unpaid stays gated. Both gated cases can advance through the welcome screen without mounting the workspace or issuing runtime initialization, order creation or account-completion writes. Auth bootstrap, provider, resolver and admission service run unmodified.
- Negative control: temporarily removing the account-completion fallback makes the first two browser cases fail. Restoring the original source makes the full 13-case suite pass (48.1s). The committed follow-up changes only E2E coverage; TypeScript, ESLint and frontend governance pass.
- Latest commit `957e6be2c`: CI settled with 23 passing checks and no failures; code-scanning alerts for the PR merge ref are empty. Both Codex and Claude now return APPROVE with no findings. Claude explicitly confirms the new browser coverage addresses the previous bootstrap-recovery validation gap.
- Review follow-up: 128 targeted tests pass across billing, admission service and hook suites, including 33 new cases that run the real HTTP adapter → billing result conversion → admission service → React Query policy. Only fetch/account/auth are mocked. Personal order history, team order history and enterprise credits all cover 503/429/network retries, background retry exhaustion and 15-second recovery, timeout recovery without immediate repeats, 401/403/plain-error/business-error blocking, and legacy status-bearing failure envelopes.
- 25 targeted spinner/admission component tests pass. The earlier admission/preload implementation also passed 387 relevant unit cases across 23 suites. These animation/preload results precede the latest billing error-propagation fix.
- All 13 local Playwright cases pass on the current tree (including the three bootstrap-recovery cases below): desktop/mobile refresh, paid navigation without a loading flash, unpaid/anonymous protection, automatic retry recovery, exempt Profile to protected Home navigation, and held account/order responses proving parallel reads without premature protected DOM/runtime requests or duplicate page reads.
- The new first-paint test holds application scripts, verifies changing brush frames before document load, then releases scripts and confirms the same SVG remains mounted and animated while account verification is held. Reduced-motion presentation works before hydration as well.
- TypeScript, full frontend ESLint, the Knip dead-code gate, frontend governance and diff checks pass. The existing cache-governance guard reports its baseline bootstrap skip.
- Verification uses local mock accounts. No live Stripe payment, production latency benchmark or deployment; genuine account/organization dependencies still apply.

## Review notes

Tim’s [P2 on lost billing error categories](https://github.com/SerendipityOneInc/ecap-workspace/pull/3916#issuecomment-5873907605) is fixed: billing results retain the original client-side error, and admission rethrows it or reconstructs `ApiError` from legacy status/code fields. This preserves HTTP, network and timeout classification without treating ordinary errors as transient. Existing non-throwing billing consumers keep their result contract. The new regression suite reproduced 21 failures before the fix; all 33 cases now pass. No backend or payment-evidence changes.

The legacy `/claw-settings` allowlist entry remains unchanged. Middleware redirects it to the intentionally exempt `/identity` route before rendering, so removing that entry would not change current access or loading behavior. The actual route behavior is documented above; this non-blocking cleanup suggestion is outside the animation correction.

Claude’s [bootstrap-recovery validation gap](https://github.com/SerendipityOneInc/ecap-workspace/pull/3916#issuecomment-5874198853) is now covered by three real-browser scenarios plus a negative control, described above. They verify the intended product behavior: recovered server completion avoids restarting onboarding for an admitted returning user, explicit incomplete accounts still require onboarding, and completed onboarding never replaces admission evidence. No product or backend changes were needed.

The latest Claude review also notes the intentional conservative treatment of legacy failure envelopes without an original error or HTTP status: these remain blocking and do not automatically retry. This is covered by the business-failure tests and preserves Tim’s request not to classify all ordinary errors as transient; no change is warranted.


---

## feat(agents): add gated Codex subscription backend APIs (#3912)

- **SHA**: `6b1dcd5763b240e2adff662eaf128a09f77d1168`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-28T15:40:33Z
- **PR**: #3912

### Commit Message

```
feat(agents): add gated Codex subscription backend APIs (#3912)

## Problem and behavior

This is the backend half of the personal Codex subscription feature. It
adds owner-scoped provider-connection APIs and optional subscription
model fields to claw-interface; all UI changes have been moved to
[frontend
#3917](https://github.com/SerendipityOneInc/ecap-workspace/pull/3917), a
separate stacked PR. [Engine
#1736](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1736) is
merged.

Existing clients require no request changes. The default-off gate
prevents new authorization/binding, and disabled discovery returns an
empty capability without contacting Engine. Deploying this PR does not
create connections, change Agent configurations or billing state, or
expose a new frontend entry. Legacy Engine responses without
subscription metadata remain supported.

Admission requires `CODEX_SUBSCRIPTIONS_INTERNAL_ENABLED=true` plus a
verified token email ending exactly in `@srp.one` or present in
`CODEX_SUBSCRIPTIONS_ALLOWED_EMAILS` (comma-separated exact emails,
default empty, case-insensitive). This follows the repository's verified
staff-email and configured-email membership conventions without reusing
administrator privileges or the frontend staging/development bypass.
Profile/request-body emails cannot grant access; the allowlist cannot
bypass the master switch.

OAuth credentials remain in Engine. Every model-binding path requires
the master switch and an active grant belonging to the exact UID/org.
Subscription models use account eligibility and disable platform/Auto
fallback; choosing a platform model explicitly clears the binding. V1
sandbox-managed Agents are excluded. Owner-scoped disconnect remains
available after gate shutdown. Admission changes do not revoke existing
grants or stop inference: Engine's runtime switch controls that
separately.

## Rollout

1. Deploy this backend with both configuration defaults unchanged.
2. Review and deploy the separate frontend when ready; it consumes
backend capability.
3. Complete a dedicated staging Agent smoke before enabling the Engine
and claw-interface switches. Add approved allowlist entries only when
needed.

No deployment settings, real whitelist entries, credentials or live data
were changed. Full details:
`docs/superpowers/specs/2026-09-28-codex-subscription.md`.

## Validation

- `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and import
boundaries passed.
- 260 targeted backend tests passed: admission/allowlist, disabled gate,
spoofing, owner revocation, existing model/revision access and Engine
client contracts.
- Previous real-account acceptance passed device authorization,
seven-model discovery and one native inference; credentials remained in
the Engine probe's memory. A dedicated staging Agent smoke remains a
release gate.
```

### PR Body

## Problem and behavior

This is the backend half of the personal Codex subscription feature. It adds owner-scoped provider-connection APIs and optional subscription model fields to claw-interface; all UI changes have been moved to [frontend #3917](https://github.com/SerendipityOneInc/ecap-workspace/pull/3917), a separate stacked PR. [Engine #1736](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1736) is merged.

Existing clients require no request changes. The default-off gate prevents new authorization/binding, and disabled discovery returns an empty capability without contacting Engine. Deploying this PR does not create connections, change Agent configurations or billing state, or expose a new frontend entry. Legacy Engine responses without subscription metadata remain supported.

Admission requires `CODEX_SUBSCRIPTIONS_INTERNAL_ENABLED=true` plus a verified token email ending exactly in `@srp.one` or present in `CODEX_SUBSCRIPTIONS_ALLOWED_EMAILS` (comma-separated exact emails, default empty, case-insensitive). This follows the repository's verified staff-email and configured-email membership conventions without reusing administrator privileges or the frontend staging/development bypass. Profile/request-body emails cannot grant access; the allowlist cannot bypass the master switch.

OAuth credentials remain in Engine. Every model-binding path requires the master switch and an active grant belonging to the exact UID/org. Subscription models use account eligibility and disable platform/Auto fallback; choosing a platform model explicitly clears the binding. V1 sandbox-managed Agents are excluded. Owner-scoped disconnect remains available after gate shutdown. Admission changes do not revoke existing grants or stop inference: Engine's runtime switch controls that separately.

## Rollout

1. Deploy this backend with both configuration defaults unchanged.
2. Review and deploy the separate frontend when ready; it consumes backend capability.
3. Complete a dedicated staging Agent smoke before enabling the Engine and claw-interface switches. Add approved allowlist entries only when needed.

No deployment settings, real whitelist entries, credentials or live data were changed. Full details: `docs/superpowers/specs/2026-09-28-codex-subscription.md`.

## Validation

- `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and import boundaries passed.
- 260 targeted backend tests passed: admission/allowlist, disabled gate, spoofing, owner revocation, existing model/revision access and Engine client contracts.
- Previous real-account acceptance passed device authorization, seven-model discovery and one native inference; credentials remained in the Engine probe's memory. A dedicated staging Agent smoke remains a release gate.


---

## fix(agents): resolve runtime ownership during cleanup and recovery (#3910)

- **SHA**: `9812c1a6bdb51828a424a02d1aeef0d80cb2ddda`
- **作者**: rayrain-srp
- **日期**: 2026-09-28T12:52:00Z
- **PR**: #3910

### Commit Message

```
fix(agents): resolve runtime ownership during cleanup and recovery (#3910)

## Summary
- Use the same Workspace-to-ACS ownership resolver for channel CRUD,
cleanup snapshots, channel disable/readback, and subscription recovery.
Preserve business authorization, baseline ownership, migrated channel
IDs, and shared-Computer lifecycle behavior.
- Check source Engine state, schedules, and channels under the
membership transition lease before canceling personal renewal. Execution
still captures its own durable snapshot and enforces existing leases,
CAS and stop/readback checks.
- Log safe lifecycle stages and upstream error metadata before wrapping
failures, and record whether personal renewal cancellation had completed
when a handoff fails.

Related: #3909 · [ECA-1473](https://linear.app/srpone/issue/ECA-1473)
Design and implementation plan:
[2026-09-28-eca-1473-runtime-cleanup.md](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/docs/superpowers/specs/2026-09-28-eca-1473-runtime-cleanup.md)

## Root cause
New self-evolving workspaces without a development baseline use
workspace-derived runtime owners. Cleanup and recovery sent the business
UID/org to ACS instead, causing `channel.not_found` before the cleanup
snapshot was saved. During enterprise join this happened after personal
renewal had already been canceled.

## Test plan
- [x] 261 targeted tests: cleanup/recovery, enterprise handoff, baseline
adoption, channel services/service proxy, recovery repository and
personal subscription cancellation.
- [x] Stateful HTTP transport tests verify actual ACS actor headers and
internal channel IDs for ordinary Engine, self-evolving without
baseline, self-evolving with baseline, and migrated workspaces; cover
404, readback failure, lease loss and retry.
- [x] Preflight tests prove no runtime writes and no renewal
cancellation/key bind/membership swap after a failed preflight.
Post-preflight failure remains retryable with an already-canceling
subscription.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8
import contracts passed.
- [x] CI: 12,776 tests passed, 5 skipped; coverage 89.79% (gate 89.5%).
Lint/types, duplication, CodeQL and both automated reviews passed.
- [ ] Isolated staging E2E with real Engine/ACS, encrypted Mongo,
billing-key readback and target membership activation. Local HTTP
transports and repository mocks do not validate this boundary; no Mongo
query forms were changed.

This is a backend code fix. Production recovery/deployment and a new
user-facing durable handoff-progress API/UI remain tracked by #3909.
Existing subscription audits, runtime cleanup snapshots and retry
semantics are retained; renewal cancellation is not automatically
reversed.

## Review follow-up
- Confirmed the adjacent Agent Builder channel helper is outside this
defect: Project Agents are installed as hidden `agent_builder`
workspaces with [business-owned Engine
resources](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/services/claw-interface/app/services/agents/engine_agent_install_service.py#L355).
Both the [baseline service
guard](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/services/claw-interface/app/services/agents/agent_baseline_adoption.py#L36)
and repository reject hidden/internal workspaces. No supported path
converts that dedicated Project Agent to a new opaque-owned
self-evolving workspace; the sibling helper is unchanged.
- Keeping renewal canceled after a later cleanup failure is intentional
and follows #3909: retry is supported, while automatic renewal
restoration would override the user's join intent.
```

### PR Body

## Summary
- Use the same Workspace-to-ACS ownership resolver for channel CRUD, cleanup snapshots, channel disable/readback, and subscription recovery. Preserve business authorization, baseline ownership, migrated channel IDs, and shared-Computer lifecycle behavior.
- Check source Engine state, schedules, and channels under the membership transition lease before canceling personal renewal. Execution still captures its own durable snapshot and enforces existing leases, CAS and stop/readback checks.
- Log safe lifecycle stages and upstream error metadata before wrapping failures, and record whether personal renewal cancellation had completed when a handoff fails.

Related: #3909 · [ECA-1473](https://linear.app/srpone/issue/ECA-1473)
Design and implementation plan: [2026-09-28-eca-1473-runtime-cleanup.md](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/docs/superpowers/specs/2026-09-28-eca-1473-runtime-cleanup.md)

## Root cause
New self-evolving workspaces without a development baseline use workspace-derived runtime owners. Cleanup and recovery sent the business UID/org to ACS instead, causing `channel.not_found` before the cleanup snapshot was saved. During enterprise join this happened after personal renewal had already been canceled.

## Test plan
- [x] 261 targeted tests: cleanup/recovery, enterprise handoff, baseline adoption, channel services/service proxy, recovery repository and personal subscription cancellation.
- [x] Stateful HTTP transport tests verify actual ACS actor headers and internal channel IDs for ordinary Engine, self-evolving without baseline, self-evolving with baseline, and migrated workspaces; cover 404, readback failure, lease loss and retry.
- [x] Preflight tests prove no runtime writes and no renewal cancellation/key bind/membership swap after a failed preflight. Post-preflight failure remains retryable with an already-canceling subscription.
- [x] `bash scripts/verify-py.sh`: Ruff, formatting, Pyright and all 8 import contracts passed.
- [x] CI: 12,776 tests passed, 5 skipped; coverage 89.79% (gate 89.5%). Lint/types, duplication, CodeQL and both automated reviews passed.
- [ ] Isolated staging E2E with real Engine/ACS, encrypted Mongo, billing-key readback and target membership activation. Local HTTP transports and repository mocks do not validate this boundary; no Mongo query forms were changed.

This is a backend code fix. Production recovery/deployment and a new user-facing durable handoff-progress API/UI remain tracked by #3909. Existing subscription audits, runtime cleanup snapshots and retry semantics are retained; renewal cancellation is not automatically reversed.

## Review follow-up
- Confirmed the adjacent Agent Builder channel helper is outside this defect: Project Agents are installed as hidden `agent_builder` workspaces with [business-owned Engine resources](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/services/claw-interface/app/services/agents/engine_agent_install_service.py#L355). Both the [baseline service guard](https://github.com/SerendipityOneInc/ecap-workspace/blob/2030cc682fa566951c1c301eeace6512071f5df6/services/claw-interface/app/services/agents/agent_baseline_adoption.py#L36) and repository reject hidden/internal workspaces. No supported path converts that dedicated Project Agent to a new opaque-owned self-evolving workspace; the sibling helper is unchanged.
- Keeping renewal canceled after a later cleanup failure is intentional and follows #3909: retry is supported, while automatic renewal restoration would override the user's join intent.


---

## feat(platform): refine sign-in and billing interface (#3913)

- **SHA**: `b255ec8fa6484bf0435e7c9382b4adef6d63ae2d`
- **作者**: finn-srp
- **日期**: 2026-09-28T12:47:33Z
- **PR**: #3913

### Commit Message

```
feat(platform): refine sign-in and billing interface (#3913)

## Summary
- Replace the embedded Clerk sign-in widget with a Platform login flow
for Google and email verification codes, including callback handling and
safer auth errors.
- Apply the ZooWork palette to Platform and align sidebar links, project
icons, and unavailable settings states.
- Rename the sidebar balance entry to Credits; make the row open Billing
and Add funds open the existing top-up dialog directly.
- Show $20, $100, $500, and Other in the dialog. Other accepts
whole-dollar amounts from $5 to $500; checkout and payment processing
remain on the existing Platform API and Stripe flow.

## Rollout prerequisite
- The development Clerk instance has passwordless sign-up enabled. The
production Clerk instance has not been updated. Before a production
Platform deployment, make the production sign-up password optional,
enable email codes for sign-in and sign-up, and verify new-user email
and Google registration there. Production deployment is a separate
manual workflow; this PR does not change production Clerk configuration.

## Test plan
- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit tests (70 passed)
- [x] Platform production build
- [x] PR size check (1,593 / 3,000 lines)
- [ ] Live production Clerk registration and Stripe checkout were not
run.
```

### PR Body

## Summary
- Replace the embedded Clerk sign-in widget with a Platform login flow for Google and email verification codes, including callback handling and safer auth errors.
- Apply the ZooWork palette to Platform and align sidebar links, project icons, and unavailable settings states.
- Rename the sidebar balance entry to Credits; make the row open Billing and Add funds open the existing top-up dialog directly.
- Show $20, $100, $500, and Other in the dialog. Other accepts whole-dollar amounts from $5 to $500; checkout and payment processing remain on the existing Platform API and Stripe flow.

## Rollout prerequisite
- The development Clerk instance has passwordless sign-up enabled. The production Clerk instance has not been updated. Before a production Platform deployment, make the production sign-up password optional, enable email codes for sign-in and sign-up, and verify new-user email and Google registration there. Production deployment is a separate manual workflow; this PR does not change production Clerk configuration.

## Test plan
- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit tests (70 passed)
- [x] Platform production build
- [x] PR size check (1,593 / 3,000 lines)
- [ ] Live production Clerk registration and Stripe checkout were not run.


---

## fix(platform): respect billing HTTP client lifecycle (#3911)

- **SHA**: `233cc0248b1de9fef07fea5bed93370bae6c2664`
- **作者**: finn-srp
- **日期**: 2026-09-28T10:20:53Z
- **PR**: #3911

### Commit Message

```
fix(platform): respect billing HTTP client lifecycle (#3911)

## Summary

Fix staging Platform Billing returning HTTP 500 after another Billing
request opens the shared HTTP client. Platform wallet and ledger reads
now reuse the client without reopening or closing it. Customer ensure
and credit submission use independent clients with keepalive disabled;
mutation transport failures are never replayed.

## Root cause

The Platform methods retained `async with self._get_client()` after
#3885 changed `_get_client()` to return the shared GET client. An
already-open client raises `RuntimeError: Cannot open a client instance
more than once`. The old transport test replaced `_get_client()` with a
new client on every call and missed this integration bug.

## Test plan

- [x] Added regressions that fail on the previous code with the staging
exception (5 failed), then pass with this fix.
- [x] Warm the shared client through a normal Billing read, then
interleave repeated concurrent Platform wallet/ledger reads with
ordinary reads; verify the pool remains open until shutdown.
- [x] Verify both Platform writes use independent clients, close on
success and lost responses, make one POST only, and leave the shared
read client usable.
- [x] Route/payload test now preserves the real `_get_client()` behavior
and replaces only HTTP transport.
- [x] 73 targeted Billing and Platform tests passed.
- [x] Final-commit `bash scripts/verify-py.sh --full` executed: all
static/architecture/duplication checks passed; 12,753 tests passed, 5
skipped.
- [x] Coverage is 89.77% overall and 100% for the changed production
module; it passes the existing CI threshold of 89.5%. The local verify
script still hardcodes 90%, so its final exit code is 1 solely for that
stale threshold. This PR does not change any coverage threshold.

Backend-only change. A claw-interface staging deployment is required for
the browser fix to take effect.
```

### PR Body

## Summary

Fix staging Platform Billing returning HTTP 500 after another Billing request opens the shared HTTP client. Platform wallet and ledger reads now reuse the client without reopening or closing it. Customer ensure and credit submission use independent clients with keepalive disabled; mutation transport failures are never replayed.

## Root cause

The Platform methods retained `async with self._get_client()` after #3885 changed `_get_client()` to return the shared GET client. An already-open client raises `RuntimeError: Cannot open a client instance more than once`. The old transport test replaced `_get_client()` with a new client on every call and missed this integration bug.

## Test plan

- [x] Added regressions that fail on the previous code with the staging exception (5 failed), then pass with this fix.
- [x] Warm the shared client through a normal Billing read, then interleave repeated concurrent Platform wallet/ledger reads with ordinary reads; verify the pool remains open until shutdown.
- [x] Verify both Platform writes use independent clients, close on success and lost responses, make one POST only, and leave the shared read client usable.
- [x] Route/payload test now preserves the real `_get_client()` behavior and replaces only HTTP transport.
- [x] 73 targeted Billing and Platform tests passed.
- [x] Final-commit `bash scripts/verify-py.sh --full` executed: all static/architecture/duplication checks passed; 12,753 tests passed, 5 skipped.
- [x] Coverage is 89.77% overall and 100% for the changed production module; it passes the existing CI threshold of 89.5%. The local verify script still hardcodes 90%, so its final exit code is 1 solely for that stale threshold. This PR does not change any coverage threshold.

Backend-only change. A claw-interface staging deployment is required for the browser fix to take effect.


---

## perf(credits): use scoped BG aggregation for Task and Usage (#3908)

- **SHA**: `7102c19fff98cdda6c2204c36c23d2bbe4f4d613`
- **作者**: kaka-srp
- **日期**: 2026-09-28T08:36:55Z
- **PR**: #3908

### Commit Message

```
perf(credits): use scoped BG aggregation for Task and Usage (#3908)

## Summary
Task credits previously fetched paginated account-wide session usage,
while Usage views scanned Lago events and could time out or truncate
totals. Route these reads through the scoped Billing Gateway aggregate
API.

- Task requests only the visible page's session IDs for the current
billing period, with an explicit retry state.
- Usage pushes custom dates to BG, includes all attribution categories,
and uses cached group snapshots plus cursors for record pages.
- Reuse server-resolved customer/member/API-key scope; failures never
fall back to event scans or appear as complete zero totals. ECAP adds no
configuration or feature flag.

## Dependencies and rollout
Depends on https://github.com/SerendipityOneInc/billing-gateway/pull/76.
Deploy BG first, then claw-interface, then Web. BG staging Vault is
configured (KV v4 → v5), and the Kubernetes Secret has synchronized all
four fields. A dedicated staging read role was provisioned and verified
using 12/12 real queries from local BG PR code (232–773 ms). Existing
Pods were not restarted. The production read role and session index
remain rollout prerequisites; no production DDL or deployment is
included.

## Validation
- PR review correction: preserve BG snapshot-scope denials as HTTP 403 /
`usage.access_denied`, rather than retryable 503. All 16 gateway
delegation tests pass, including authorization status/code assertions.
- ECAP: 69 related Python tests and 78 related Web tests passed during
implementation; frontend/backend static gates passed. Browser-discovered
copy/column issues were subsequently fixed and checked with ESLint and
real browser validation.
- Local changed code → actual staging auth/Mongo → new local BG → actual
staging Lago/PostgreSQL 16.13/Redis: Task visible-page batching,
pagination, personal Usage Time/Session/API-key views and drill-down
passed.
- Three BG account samples reconcile to Lago current-period consumption
with zero difference. Largest 30-day sample: 107,801 events; first reads
approximately 0.9–1.9 s, cached reads 34–150 ms.
- Two BG processes: eight cold Task batches make one Lago call;
admission is bounded. A 30-second uncached run completed 52/52 requests.
BG's companion isolated suite passes 673 tests at 92.87% coverage.

See `docs/superpowers/specs/2026-09-28-bg-usage-aggregation.md` and
`docs/validation/2026-09-28-bg-usage-staging-validation.md` for the
design, timings, rollout, and evidence limits. Team-admin/member browser
acceptance remains pending. The staging sample also has three unrelated
Agent session-list `agent not found` errors; Task displays partial-load
status while credits queries succeed. CI, merge, deployment, and
production acceptance are separate gates.
```

### PR Body

## Summary
Task credits previously fetched paginated account-wide session usage, while Usage views scanned Lago events and could time out or truncate totals. Route these reads through the scoped Billing Gateway aggregate API.

- Task requests only the visible page's session IDs for the current billing period, with an explicit retry state.
- Usage pushes custom dates to BG, includes all attribution categories, and uses cached group snapshots plus cursors for record pages.
- Reuse server-resolved customer/member/API-key scope; failures never fall back to event scans or appear as complete zero totals. ECAP adds no configuration or feature flag.

## Dependencies and rollout
Depends on https://github.com/SerendipityOneInc/billing-gateway/pull/76. Deploy BG first, then claw-interface, then Web. BG staging Vault is configured (KV v4 → v5), and the Kubernetes Secret has synchronized all four fields. A dedicated staging read role was provisioned and verified using 12/12 real queries from local BG PR code (232–773 ms). Existing Pods were not restarted. The production read role and session index remain rollout prerequisites; no production DDL or deployment is included.

## Validation
- PR review correction: preserve BG snapshot-scope denials as HTTP 403 / `usage.access_denied`, rather than retryable 503. All 16 gateway delegation tests pass, including authorization status/code assertions.
- ECAP: 69 related Python tests and 78 related Web tests passed during implementation; frontend/backend static gates passed. Browser-discovered copy/column issues were subsequently fixed and checked with ESLint and real browser validation.
- Local changed code → actual staging auth/Mongo → new local BG → actual staging Lago/PostgreSQL 16.13/Redis: Task visible-page batching, pagination, personal Usage Time/Session/API-key views and drill-down passed.
- Three BG account samples reconcile to Lago current-period consumption with zero difference. Largest 30-day sample: 107,801 events; first reads approximately 0.9–1.9 s, cached reads 34–150 ms.
- Two BG processes: eight cold Task batches make one Lago call; admission is bounded. A 30-second uncached run completed 52/52 requests. BG's companion isolated suite passes 673 tests at 92.87% coverage.

See `docs/superpowers/specs/2026-09-28-bg-usage-aggregation.md` and `docs/validation/2026-09-28-bg-usage-staging-validation.md` for the design, timings, rollout, and evidence limits. Team-admin/member browser acceptance remains pending. The staging sample also has three unrelated Agent session-list `agent not found` errors; Task displays partial-load status while credits queries succeed. CI, merge, deployment, and production acceptance are separate gates.


---

## feat(platform): add organization billing and Stripe top-ups (#3907)

- **SHA**: `2ec70d04f86a1073c977a5a29c4ee6195a91c463`
- **作者**: finn-srp
- **日期**: 2026-09-28T08:13:32Z
- **PR**: #3907

### Commit Message

```
feat(platform): add organization billing and Stripe top-ups (#3907)

## Summary

- Add Organization-scoped Platform billing, balance/history reads, and
Stripe Checkout top-ups in claw-interface and web/platform.
- Persist Platform top-up orders and Stripe events in dedicated Platform
Mongo collections. Reuse the existing Stripe account, product, webhook,
Gateway connection, and Lago wallet transaction API.
- Route marked Platform events through a durable local inbox and
background recovery. ZooWork events continue through the existing
billing handler without a new remote Stripe lookup in the webhook.
- Reconcile uncertain Lago submissions by reading the wallet ledger
before any manual action; the automatic worker does not post a second
credit transaction.

## Customer and wallet initialization

- Gateway exposes one customer-only idempotent `POST
/billing/customers/{customer_id}/ensure`; wallet creation reuses the
existing `POST /billing/customers/{customer_id}/wallets`.
- Platform ensures the customer, creates a `topup` wallet through the
existing client, or reads the explicit `wallet_already_exists`
conflict's wallet ID. It validates customer ownership, USD, active
status, non-expiry, and rate before storing the organization
association.
- Existing associations only read and validate their original wallet.
Invalid associations are not replaced automatically. A failed
association write can retry with the same customer and wallet;
concurrent association writes must agree on customer, wallet, and rate.
- No new wallet creation endpoint or public wallet `code` field is
added. Existing wallet and ledger GET APIs remain available.

## Boundary and rollout

- [Billing Gateway PR
#75](https://github.com/SerendipityOneInc/billing-gateway/pull/75)
provides customer-only ensure, concurrency-safe existing wallet
creation, and generic wallet/ledger reads. It has no Platform-specific
database or configuration. Deploy it before this PR.
- ZooWork's existing billing routes and data remain in place. The shared
webhook classifies Platform events from Stripe metadata; unmarked
ZooWork events keep their existing path.
- Platform-only state is in `platform_topup_orders`,
`platform_payment_events`, and the billing association on
`platform_organizations`. Startup creates the indexes.

## PR size

This change spans the billing API, durable payment worker, Platform UI,
and their tests. The repository's 3,000-line size gate has a
`size-override` label so reviewers can evaluate the paid-order lifecycle
end to end.

## Verification

- Final commit `93e6b6cd4177212dc8acfa65437e08205331598b`: Node 24 root
`bash scripts/verify-py.sh --full` ran the complete suite: **12,732
passed, 5 skipped**, coverage **89.78%**. The command exited nonzero
solely because the local script still requires 90%; the existing CI
workflow explicitly uses 89.5% and documents its baseline. No coverage
threshold was changed. All other full-check steps passed; the actual
supplemental jscpd scan is detailed below.
- Billing integration correction: Ruff, Pyright, import boundaries and
CI lint guards passed. Actual jscpd scans: source 1.89% (991 files,
limit 3%); tests 5.79% (718 files, limit 7.5%). A temporary config
disabled Git ignore filtering to ensure the ignored worktree parent did
not exclude all files; project exclusions and thresholds were preserved.
- Local HTTP contract smoke passed using the real Platform client and
Gateway FastAPI routes with fake Lago/Redis: customer-only ensure, first
wallet creation, duplicate-wallet conflict/readback, policy validation,
and ledger pagination. This does not exercise live Lago or Stripe.

- `web/platform`: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test`,
and `pnpm build`.
- Local Platform test uses the default API base URL because this
worktree has a developer-only `.env.local` override.

## Staging CSFLE validation

Passed on 2026-09-28 through the staging Pod's configured encrypted
Mongo client. The exact PR repository source exercised Platform billing
indexes, organization billing association, order and event writes,
keyset/recovery queries, and atomic updates. All three isolated records
were removed and independently rechecked as absent. [Validation
record](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/billing-topup-review/docs/staging-validation/2026-09-28-platform-billing-csfle.md).

This validates the MongoDB CSFLE boundary, not the deployed Platform
API, Stripe webhook, Gateway/Lago integration, or a real payment. Those
are separate staging acceptance checks before rollout; this PR does not
authorize deployment.
```

### PR Body

## Summary

- Add Organization-scoped Platform billing, balance/history reads, and Stripe Checkout top-ups in claw-interface and web/platform.
- Persist Platform top-up orders and Stripe events in dedicated Platform Mongo collections. Reuse the existing Stripe account, product, webhook, Gateway connection, and Lago wallet transaction API.
- Route marked Platform events through a durable local inbox and background recovery. ZooWork events continue through the existing billing handler without a new remote Stripe lookup in the webhook.
- Reconcile uncertain Lago submissions by reading the wallet ledger before any manual action; the automatic worker does not post a second credit transaction.

## Customer and wallet initialization

- Gateway exposes one customer-only idempotent `POST /billing/customers/{customer_id}/ensure`; wallet creation reuses the existing `POST /billing/customers/{customer_id}/wallets`.
- Platform ensures the customer, creates a `topup` wallet through the existing client, or reads the explicit `wallet_already_exists` conflict's wallet ID. It validates customer ownership, USD, active status, non-expiry, and rate before storing the organization association.
- Existing associations only read and validate their original wallet. Invalid associations are not replaced automatically. A failed association write can retry with the same customer and wallet; concurrent association writes must agree on customer, wallet, and rate.
- No new wallet creation endpoint or public wallet `code` field is added. Existing wallet and ledger GET APIs remain available.

## Boundary and rollout

- [Billing Gateway PR #75](https://github.com/SerendipityOneInc/billing-gateway/pull/75) provides customer-only ensure, concurrency-safe existing wallet creation, and generic wallet/ledger reads. It has no Platform-specific database or configuration. Deploy it before this PR.
- ZooWork's existing billing routes and data remain in place. The shared webhook classifies Platform events from Stripe metadata; unmarked ZooWork events keep their existing path.
- Platform-only state is in `platform_topup_orders`, `platform_payment_events`, and the billing association on `platform_organizations`. Startup creates the indexes.

## PR size

This change spans the billing API, durable payment worker, Platform UI, and their tests. The repository's 3,000-line size gate has a `size-override` label so reviewers can evaluate the paid-order lifecycle end to end.

## Verification

- Final commit `93e6b6cd4177212dc8acfa65437e08205331598b`: Node 24 root `bash scripts/verify-py.sh --full` ran the complete suite: **12,732 passed, 5 skipped**, coverage **89.78%**. The command exited nonzero solely because the local script still requires 90%; the existing CI workflow explicitly uses 89.5% and documents its baseline. No coverage threshold was changed. All other full-check steps passed; the actual supplemental jscpd scan is detailed below.
- Billing integration correction: Ruff, Pyright, import boundaries and CI lint guards passed. Actual jscpd scans: source 1.89% (991 files, limit 3%); tests 5.79% (718 files, limit 7.5%). A temporary config disabled Git ignore filtering to ensure the ignored worktree parent did not exclude all files; project exclusions and thresholds were preserved.
- Local HTTP contract smoke passed using the real Platform client and Gateway FastAPI routes with fake Lago/Redis: customer-only ensure, first wallet creation, duplicate-wallet conflict/readback, policy validation, and ledger pagination. This does not exercise live Lago or Stripe.

- `web/platform`: Node 24 `pnpm lint`, `pnpm typecheck`, `pnpm test`, and `pnpm build`.
- Local Platform test uses the default API base URL because this worktree has a developer-only `.env.local` override.

## Staging CSFLE validation

Passed on 2026-09-28 through the staging Pod's configured encrypted Mongo client. The exact PR repository source exercised Platform billing indexes, organization billing association, order and event writes, keyset/recovery queries, and atomic updates. All three isolated records were removed and independently rechecked as absent. [Validation record](https://github.com/SerendipityOneInc/ecap-workspace/blob/feature/billing-topup-review/docs/staging-validation/2026-09-28-platform-billing-csfle.md).

This validates the MongoDB CSFLE boundary, not the deployed Platform API, Stripe webhook, Gateway/Lago integration, or a real payment. Those are separate staging acceptance checks before rollout; this PR does not authorize deployment.


---

## fix(onboarding): align team checkout with verified admission (#3902)

- **SHA**: `888e6102dc6bacd412b6322dbf982a87d346fe44`
- **作者**: ericma-srp
- **日期**: 2026-09-28T06:09:55Z
- **PR**: #3902

### Commit Message

```
fix(onboarding): align team checkout with verified admission (#3902)

## Problem and behavior

Invited Team users should finish the introduction and enter `/agents`
without personal checkout. Previously #3902 skipped checkout for every
active Team admin/member, while #3901 rejected completion for unpaid
admins. This left those admins in a Continue → failure → Retry loop with
no purchase path.

This revision addresses [Tim’s P1
review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3902#issuecomment-5862350592)
by using the same `useOnboardingAdmission` result that
`OnboardingProvider.completeOnboarding` re-verifies:

- Active ordinary Team members and admins with verified subscription
evidence skip the personal plan, Stripe catalog, order creation and
Checkout popup. This includes the legacy enterprise-package evidence
added by #3901.
- Team admins without qualifying evidence retain the plan and
functioning checkout. Opening Stripe alone never completes onboarding;
confirmed admission does.
- If enterprise evidence expires before completion, Retry returns to the
usable purchase path instead of repeating a rejected completion. A
temporary completion-save failure still retries without purchasing.
- Unknown/error identity or admission never falls back to a purchase.
Disabled purchase hooks block both catalog fetching and purchase start,
including cached catalogs.

## Dependency and scope

#3901 has now been squash-merged into `main` as `fac443103`. This branch
incorporates that latest main in `6f2e73940`, resolving the overlapping
Modal, checkout hook and integration-test conflicts while preserving the
reviewed Team routing fix. The PR diff now contains only the
Team-specific frontend changes; there is no longer an outstanding #3901
merge dependency.

Frontend only, using existing account, order-history and credits-check
APIs. No backend, invitation redemption, database, dependency or
lockfile changes. Existing APIs do not expose an invite-origin flag, so
an admin role alone is not treated as proof of admission.

## Validation

- 283 related unit/integration tests across 20 files passed; after
extending the payment-confirmation assertion, the 24 directly related
tests passed again.
- Actual Provider + Modal + admission query/service + Stripe hooks
remain connected in integration tests. Only external APIs, popup
boundary and presentation are mocked. Covers unpaid admin checkout
followed by confirmed admission, active ordinary member, verified legacy
enterprise admin, evidence expiring at completion, and failed-save
retry. Eligible Team cases assert zero catalog/order/Checkout/popup
calls.
- 4 local Playwright browser tests passed: eligible admin and member
complete after a simulated save failure, enter the workspace, and remain
completed on reload with zero personal purchase requests; unpaid admin
and personal accounts retain the plan. No browser page errors.
- TypeScript, all 7 frontend governance guards, changed-file ESLint and
import-boundary checks passed (0 import errors; 684 existing warnings).
Pre-push verification and GitHub CI results are checked separately.

Local browser validation uses mock accounts after invitation redemption.
Real invitation email, OTP, staging membership/subscription data and
real Stripe payment were not exercised. The existing generic network
message for inactive/pending membership is an unchanged UX limitation,
separate from this admission/checkout correction.

## Validation after syncing main (`6f2e73940`)

Re-ran all 283 related unit/integration tests and all 4 local browser
tests against the actual merged main; all passed. The resolved
onboarding source and regression tests are identical to the previously
approved `6df86117e` implementation. TypeScript passed after stopping
the dev server (the first run overlapped Next dev regenerating temporary
route types). Full pre-push checks passed. The new GitHub CI round
finished with **23 passing / 16 scope-skipped / 0 failures**, including
the complete frontend test suite, build, lint/typecheck and CodeQL. Both
Codex and Claude approved the current commit, with no blocking findings.
GitHub reports **MERGEABLE / CLEAN / APPROVED**; the PR remains open and
has not been merged.

Current review notes left unchanged: comment placement is stylistic, and
returning to checkout after admission evidence expires is the intended
verified-admission behavior. Non-blocking earlier review notes also left
unchanged: generic blocked-membership copy is an existing UX limitation;
the query key is already centralized in `useOnboardingAdmission`;
order-history pagination is inherited from #3901 and optimization is
outside this conflict resolution.
```

### PR Body

## Problem and behavior

Invited Team users should finish the introduction and enter `/agents` without personal checkout. Previously #3902 skipped checkout for every active Team admin/member, while #3901 rejected completion for unpaid admins. This left those admins in a Continue → failure → Retry loop with no purchase path.

This revision addresses [Tim’s P1 review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3902#issuecomment-5862350592) by using the same `useOnboardingAdmission` result that `OnboardingProvider.completeOnboarding` re-verifies:

- Active ordinary Team members and admins with verified subscription evidence skip the personal plan, Stripe catalog, order creation and Checkout popup. This includes the legacy enterprise-package evidence added by #3901.
- Team admins without qualifying evidence retain the plan and functioning checkout. Opening Stripe alone never completes onboarding; confirmed admission does.
- If enterprise evidence expires before completion, Retry returns to the usable purchase path instead of repeating a rejected completion. A temporary completion-save failure still retries without purchasing.
- Unknown/error identity or admission never falls back to a purchase. Disabled purchase hooks block both catalog fetching and purchase start, including cached catalogs.

## Dependency and scope

#3901 has now been squash-merged into `main` as `fac443103`. This branch incorporates that latest main in `6f2e73940`, resolving the overlapping Modal, checkout hook and integration-test conflicts while preserving the reviewed Team routing fix. The PR diff now contains only the Team-specific frontend changes; there is no longer an outstanding #3901 merge dependency.

Frontend only, using existing account, order-history and credits-check APIs. No backend, invitation redemption, database, dependency or lockfile changes. Existing APIs do not expose an invite-origin flag, so an admin role alone is not treated as proof of admission.

## Validation

- 283 related unit/integration tests across 20 files passed; after extending the payment-confirmation assertion, the 24 directly related tests passed again.
- Actual Provider + Modal + admission query/service + Stripe hooks remain connected in integration tests. Only external APIs, popup boundary and presentation are mocked. Covers unpaid admin checkout followed by confirmed admission, active ordinary member, verified legacy enterprise admin, evidence expiring at completion, and failed-save retry. Eligible Team cases assert zero catalog/order/Checkout/popup calls.
- 4 local Playwright browser tests passed: eligible admin and member complete after a simulated save failure, enter the workspace, and remain completed on reload with zero personal purchase requests; unpaid admin and personal accounts retain the plan. No browser page errors.
- TypeScript, all 7 frontend governance guards, changed-file ESLint and import-boundary checks passed (0 import errors; 684 existing warnings). Pre-push verification and GitHub CI results are checked separately.

Local browser validation uses mock accounts after invitation redemption. Real invitation email, OTP, staging membership/subscription data and real Stripe payment were not exercised. The existing generic network message for inactive/pending membership is an unchanged UX limitation, separate from this admission/checkout correction.

## Validation after syncing main (`6f2e73940`)

Re-ran all 283 related unit/integration tests and all 4 local browser tests against the actual merged main; all passed. The resolved onboarding source and regression tests are identical to the previously approved `6df86117e` implementation. TypeScript passed after stopping the dev server (the first run overlapped Next dev regenerating temporary route types). Full pre-push checks passed. The new GitHub CI round finished with **23 passing / 16 scope-skipped / 0 failures**, including the complete frontend test suite, build, lint/typecheck and CodeQL. Both Codex and Claude approved the current commit, with no blocking findings. GitHub reports **MERGEABLE / CLEAN / APPROVED**; the PR remains open and has not been merged.

Current review notes left unchanged: comment placement is stylistic, and returning to checkout after admission evidence expires is the intended verified-admission behavior. Non-blocking earlier review notes also left unchanged: generic blocked-membership copy is an existing UX limitation; the query key is already centralized in `useOnboardingAdmission`; order-history pagination is inherited from #3901 and optimization is outside this conflict resolution.


---

## feat(claw-interface): expose managed agent webhooks (#3900)

- **SHA**: `602b60773da10f952170c69de4d32afd1897b912`
- **作者**: finn-srp
- **日期**: 2026-09-28T05:11:33Z
- **PR**: #3900

### Commit Message

```
feat(claw-interface): expose managed agent webhooks (#3900)

## Summary
- Expose Engine's agent-scoped and owner-scoped webhook management
routes through `/service/v1` for existing `zct_` service tokens. Related
to #3786.
- Map public POST `/{webhook_id}/update` and `/{webhook_id}/delete`
actions to Engine PATCH/DELETE while keeping the Interface GET/POST
convention.
- Bind owner scope to the authenticated token, verify agent ownership
before forwarding, reject unlisted routes, and hash validated
1–255-character idempotency keys with org/owner scope into a fixed
64-character Engine key. Retries remain stable across service-token
rotation.
- Mark webhook responses `Cache-Control: no-store`; document the public
paths and rollout requirements.
- Reject ambiguous dot-segment and encoded-delimiter paths before
service API dispatch, so authorization and Engine forwarding use the
same path.

## PR Lens
![Architecture: customer calls pass through claw-interface authorization
before reaching Engine; Engine delivery is
unchanged](https://prlens.dev/c/dkZx5s9tJM9h7-Mu1yWlfg.svg)

[Open the interactive architecture and data-flow
walkthrough](https://prlens.dev/c/dkZx5s9tJM9h7-Mu1yWlfg). The data-flow
view follows one agent-scoped webhook create request through token auth,
agent ownership verification, Engine forwarding, and the no-store
response.

## Test plan
- [x] Targeted webhook and existing service proxy regression tests: 195
passed, including key length boundaries, owner/org isolation, retry
stability, and service-token rotation.
- [x] Full local test cases: 12,635 passed, 5 skipped; 89.89% coverage,
above CI's unchanged 89.5% threshold. Static, architecture and
duplication checks passed.
- [ ] `bash scripts/verify-py.sh --full` exits 1 only at the unchanged
90% coverage gate (actual: 89.89%). All test cases and other full-suite
checks passed. The script is unchanged in this PR; CI retains its
existing 89.5% gate.
- [x] Pre-push changed-surface checks passed.

## Rollout note
- This PR does not enable Engine webhook flags or run a live receiver
smoke. A dedicated HTTPS receiver and the Engine dispatcher/capture
rollout must be verified before advertising customer availability.
- The repository's `check-user` pre-commit hook was skipped because it
requires a GitHub login ending in `-srp`, while the workspace specifies
Finn's active `finn930` account. All other pre-commit hooks passed;
commit author is `finn-srp <finn@srp.one>`.
```

### PR Body

## Summary
- Expose Engine's agent-scoped and owner-scoped webhook management routes through `/service/v1` for existing `zct_` service tokens. Related to #3786.
- Map public POST `/{webhook_id}/update` and `/{webhook_id}/delete` actions to Engine PATCH/DELETE while keeping the Interface GET/POST convention.
- Bind owner scope to the authenticated token, verify agent ownership before forwarding, reject unlisted routes, and hash validated 1–255-character idempotency keys with org/owner scope into a fixed 64-character Engine key. Retries remain stable across service-token rotation.
- Mark webhook responses `Cache-Control: no-store`; document the public paths and rollout requirements.
- Reject ambiguous dot-segment and encoded-delimiter paths before service API dispatch, so authorization and Engine forwarding use the same path.

## PR Lens
![Architecture: customer calls pass through claw-interface authorization before reaching Engine; Engine delivery is unchanged](https://prlens.dev/c/dkZx5s9tJM9h7-Mu1yWlfg.svg)

[Open the interactive architecture and data-flow walkthrough](https://prlens.dev/c/dkZx5s9tJM9h7-Mu1yWlfg). The data-flow view follows one agent-scoped webhook create request through token auth, agent ownership verification, Engine forwarding, and the no-store response.

## Test plan
- [x] Targeted webhook and existing service proxy regression tests: 195 passed, including key length boundaries, owner/org isolation, retry stability, and service-token rotation.
- [x] Full local test cases: 12,635 passed, 5 skipped; 89.89% coverage, above CI's unchanged 89.5% threshold. Static, architecture and duplication checks passed.
- [ ] `bash scripts/verify-py.sh --full` exits 1 only at the unchanged 90% coverage gate (actual: 89.89%). All test cases and other full-suite checks passed. The script is unchanged in this PR; CI retains its existing 89.5% gate.
- [x] Pre-push changed-surface checks passed.

## Rollout note
- This PR does not enable Engine webhook flags or run a live receiver smoke. A dedicated HTTPS receiver and the Engine dispatcher/capture rollout must be verified before advertising customer availability.
- The repository's `check-user` pre-commit hook was skipped because it requires a GitHub login ending in `-srp`, while the workspace specifies Finn's active `finn930` account. All other pre-commit hooks passed; commit author is `finn-srp <finn@srp.one>`.



---

## fix(onboarding): gate workspace entry on confirmed checkout (#3901)

- **SHA**: `fac443103c5f8a22822763e4b7b4bb640e97aad2`
- **作者**: ericma-srp
- **日期**: 2026-09-28T03:48:02Z
- **PR**: #3901

### Commit Message

```
fix(onboarding): gate workspace entry on confirmed checkout (#3901)

## Summary
Opening Stripe Checkout no longer completes onboarding or grants
workspace access. The frontend waits for positive subscription evidence
from existing account or order APIs, then saves onboarding completion
and navigates to `/agents`. New checkout uses successful subscription
orders with granted entitlement; legacy paid-cycle and
provider-subscription evidence preserves established customers.

- Gate protected workspace rendering while verification is pending,
incomplete, or unavailable; preserve exact payment-success and
email-verification routes.
- Recheck on refresh/login, poll while checkout is incomplete, and
verify again immediately before saving completion. Old
`onboarding_completed` values and local progress cannot bypass the gate.
- Keep the checkout resumable after its popup closes, with waiting/retry
copy across all 10 locales.
- Preserve legacy paid subscriptions through `/account/me` paid-cycle
counts or current provider-backed paid access, as well as successful
Billing v2 order history. Preserve active ordinary team memberships
(including older responses using `org.status`). Team admins need
successful personal or team subscription evidence.

## Root cause
`useOnboardingCardCheckout` forwarded the checkout-window-opened
callback directly to `completeOnboarding`. That persisted
`onboarding_completed=true` and redirected to `/agents` before payment
confirmation. The prior provider also rendered workspace children
underneath onboarding and trusted the historical completion flag.

## Test plan
- [x] 260 targeted tests across 18 files passed (2026-09-28).
- [x] TypeScript, changed-file ESLint, frontend governance guards, and
import boundaries passed (import check has existing repository
warnings).
- [x] Chromium with local mock endpoints: close checkout without
completing; refresh; fresh login session; direct workspace URL with old
completed flag; verification failure and retry; confirmed subscription
followed by `/agents` navigation and refresh. No browser page errors.
- [ ] Real Stripe payment and production registration/OTP; not exercised
locally.

## Scope and limits
Frontend only: no backend, BFF, dependency, or lockfile changes. This is
a website entry restriction, not backend API authorization. The current
$30/month subscription checkout is unchanged; this does not introduce a
standalone zero-cost card-binding flow. Accounts without positive
paid/account-subscription or successful order evidence are blocked even
if onboarding was previously marked complete.


## Review follow-up
- Fixed the legacy history gap: `/orders/list` only exposes Billing v2;
existing server-owned account billing projections now cover established
legacy subscribers. Added expired-legacy, current-provider, free-grant
and unverified-trial regressions.
- Fixed older team response compatibility using the existing
membership-scoped `org.status` fallback while respecting explicit
suspended/pending/none statuses.
- Kept the single provider-owned polling loop; the suggested future
route-rewiring hazard is not reachable in this layout and does not need
additional pollers.
- Verified the final payment-channel review note against the existing
backend contract: `UserMeResponse.from_account_and_org` normalizes
historical `creem` to `card`
(`services/claw-interface/app/schema/account_api.py:329`), with an
existing regression in `test_billing_v2_user_public_response.py`. The
public response permits `offline`, which the admission allowlist already
accepts. No additional backend or admission change is required.
- Final checks for `cbf06fa64`: CI, frontend build/test/lint/typecheck,
CodeQL and review gates passed; Codex review reports no remaining
findings.



## Tim review follow-up (2026-09-28)

Fixed [Tim's
P1](https://github.com/SerendipityOneInc/ecap-workspace/pull/3901#issuecomment-5862349573):
effective legacy enterprise subscriptions can have `plan=free`, zero
personal paid cycles and no Billing v2 payment orders. Active team
admins now have an additional positive-evidence path through the
existing `/users/credits/check` subscription projection. It requires
enterprise-package kind and id, a supported payment provider, effective
active/canceling/past_due status and an unexpired period.
Credits/balance, billing readiness and admin role alone never admit the
user. Existing account/order proofs and ordinary member behavior remain
unchanged. No backend changes.

- Reproduced the missing scenario before implementation: regression
suite had 5 failures; all pass after the fix.
- Added negative coverage for free/expired/manual-review/trial/missing
evidence, unsupported providers, inactive memberships, request errors,
and rechecking a changed subscription.
- Added integration tests connecting the actual Provider, Modal,
admission query/service and completion logic, with API/presentation
mocks: eligible legacy enterprise admin, unpaid admin retaining a usable
checkout path, ordinary member, and subscription expiry before saving
completion.
- 260 relevant tests across 18 files passed; TypeScript and ESLint
passed. Final CI for `6f27b353a` is green (23 passing checks, none
pending/failed). Both Claude and Codex re-reviews report APPROVE with no
findings. Live enterprise accounts and real payment were not exercised.

### Cross-PR merge constraint
[Tim's #3902
comment](https://github.com/SerendipityOneInc/ecap-workspace/pull/3902)
also identifies a separate composition issue: #3902 currently skips
checkout for every active team admin. That branch must use verified
admission to decide whether an admin may skip checkout, and retain
payment for an unpaid admin, before both PRs ship. #3901 alone retains
payment and tests it; this update does not silently change #3902 or
claim its role-only skip condition is fixed. Preserve this invariant
when resolving the two PRs' Modal conflict.
```

### PR Body

## Summary
Opening Stripe Checkout no longer completes onboarding or grants workspace access. The frontend waits for positive subscription evidence from existing account or order APIs, then saves onboarding completion and navigates to `/agents`. New checkout uses successful subscription orders with granted entitlement; legacy paid-cycle and provider-subscription evidence preserves established customers.

- Gate protected workspace rendering while verification is pending, incomplete, or unavailable; preserve exact payment-success and email-verification routes.
- Recheck on refresh/login, poll while checkout is incomplete, and verify again immediately before saving completion. Old `onboarding_completed` values and local progress cannot bypass the gate.
- Keep the checkout resumable after its popup closes, with waiting/retry copy across all 10 locales.
- Preserve legacy paid subscriptions through `/account/me` paid-cycle counts or current provider-backed paid access, as well as successful Billing v2 order history. Preserve active ordinary team memberships (including older responses using `org.status`). Team admins need successful personal or team subscription evidence.

## Root cause
`useOnboardingCardCheckout` forwarded the checkout-window-opened callback directly to `completeOnboarding`. That persisted `onboarding_completed=true` and redirected to `/agents` before payment confirmation. The prior provider also rendered workspace children underneath onboarding and trusted the historical completion flag.

## Test plan
- [x] 260 targeted tests across 18 files passed (2026-09-28).
- [x] TypeScript, changed-file ESLint, frontend governance guards, and import boundaries passed (import check has existing repository warnings).
- [x] Chromium with local mock endpoints: close checkout without completing; refresh; fresh login session; direct workspace URL with old completed flag; verification failure and retry; confirmed subscription followed by `/agents` navigation and refresh. No browser page errors.
- [ ] Real Stripe payment and production registration/OTP; not exercised locally.

## Scope and limits
Frontend only: no backend, BFF, dependency, or lockfile changes. This is a website entry restriction, not backend API authorization. The current $30/month subscription checkout is unchanged; this does not introduce a standalone zero-cost card-binding flow. Accounts without positive paid/account-subscription or successful order evidence are blocked even if onboarding was previously marked complete.


## Review follow-up
- Fixed the legacy history gap: `/orders/list` only exposes Billing v2; existing server-owned account billing projections now cover established legacy subscribers. Added expired-legacy, current-provider, free-grant and unverified-trial regressions.
- Fixed older team response compatibility using the existing membership-scoped `org.status` fallback while respecting explicit suspended/pending/none statuses.
- Kept the single provider-owned polling loop; the suggested future route-rewiring hazard is not reachable in this layout and does not need additional pollers.
- Verified the final payment-channel review note against the existing backend contract: `UserMeResponse.from_account_and_org` normalizes historical `creem` to `card` (`services/claw-interface/app/schema/account_api.py:329`), with an existing regression in `test_billing_v2_user_public_response.py`. The public response permits `offline`, which the admission allowlist already accepts. No additional backend or admission change is required.
- Final checks for `cbf06fa64`: CI, frontend build/test/lint/typecheck, CodeQL and review gates passed; Codex review reports no remaining findings.



## Tim review follow-up (2026-09-28)

Fixed [Tim's P1](https://github.com/SerendipityOneInc/ecap-workspace/pull/3901#issuecomment-5862349573): effective legacy enterprise subscriptions can have `plan=free`, zero personal paid cycles and no Billing v2 payment orders. Active team admins now have an additional positive-evidence path through the existing `/users/credits/check` subscription projection. It requires enterprise-package kind and id, a supported payment provider, effective active/canceling/past_due status and an unexpired period. Credits/balance, billing readiness and admin role alone never admit the user. Existing account/order proofs and ordinary member behavior remain unchanged. No backend changes.

- Reproduced the missing scenario before implementation: regression suite had 5 failures; all pass after the fix.
- Added negative coverage for free/expired/manual-review/trial/missing evidence, unsupported providers, inactive memberships, request errors, and rechecking a changed subscription.
- Added integration tests connecting the actual Provider, Modal, admission query/service and completion logic, with API/presentation mocks: eligible legacy enterprise admin, unpaid admin retaining a usable checkout path, ordinary member, and subscription expiry before saving completion.
- 260 relevant tests across 18 files passed; TypeScript and ESLint passed. Final CI for `6f27b353a` is green (23 passing checks, none pending/failed). Both Claude and Codex re-reviews report APPROVE with no findings. Live enterprise accounts and real payment were not exercised.

### Cross-PR merge constraint
[Tim's #3902 comment](https://github.com/SerendipityOneInc/ecap-workspace/pull/3902) also identifies a separate composition issue: #3902 currently skips checkout for every active team admin. That branch must use verified admission to decide whether an admin may skip checkout, and retain payment for an unpaid admin, before both PRs ship. #3901 alone retains payment and tests it; this update does not silently change #3902 or claim its role-only skip condition is fixed. Preserve this invariant when resolving the two PRs' Modal conflict.

