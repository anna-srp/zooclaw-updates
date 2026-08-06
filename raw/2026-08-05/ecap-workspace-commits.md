# SerendipityOneInc/ecap-workspace — commits 2026-08-05

## feat(billing): add staged Card checkout (#3265)

- **SHA**: `461ab48d555e0fdfa838f2c57049e141a306cabf`
- **作者**: tim-srp
- **日期**: 2026-08-05T16:23:01Z
- **PR**: #3265

### Commit Message

```
feat(billing): add staged Card checkout (#3265)
```

### PR Body

## Linear

N/A — this is the final frontend slice of the existing staged Creem Card rollout.

## Summary

- expose the new payment path to users only as `Card`; no Creem provider branding leaks into the UI
- in staging/development only, route a paid subscription to Billing v2 Card checkout when the authenticated backend capability is explicitly available
- support active, same-cycle Card upgrades through the already-merged `checkout_intent=upgrade` backend contract
- poll the local Billing v2 order after Card checkout and report success only after both a successful order status and `entitlement_granted=true`
- make Card subscription management provider-safe: generic cancellation, no Stripe portal/Edit billing/download leakage, and fail-closed unsupported Card downgrade or cycle/provider changes
- preserve the existing Stripe, Antom, Apple, trial, and top-up flows

## Rollout safety

- frontend Card routing is enabled only when `NEXT_PUBLIC_APP_ENV=staging` (or local development) and `/billing/card-checkout-capability` returns `card_available=true`
- production does not query the capability and cannot enter the new Card checkout branch through this change
- PR #3263 already provides the required backend upgrade contract
- merge PR #3264 before final staging validation so Creem yearly agreements participate in the existing annual credit-reset lifecycle and the rollout checklist is available

## Test plan

- [x] local `bash scripts/verify-web.sh` after rebase onto current `main`: governance guards, TypeScript, and ESLint passed; 603/603 Vitest files passed with 8272 passed, 67 skipped, and 1 todo
- [x] a102 devcontainer: governance guards, TypeScript, and ESLint passed
- [x] a102 Card-focused suite: 6/6 files and 182/182 tests passed
- [x] a102 full Vitest run: 602/603 files and 8271 tests passed; one unrelated existing `MarkdownContent` hydration test exceeded its 5-second timeout under full parallel load
- [x] reran that unrelated `MarkdownContent` file three times in isolation on a102: 48/48 passed on each run
- [x] independent specification and code-quality reviews approved after Card downgrade, refund-status display, and success-state conflict tests were added
- [x] push gate: PR size, changed-surface guards, TypeScript, and ESLint passed

## Deferred until staging deployment

Real Creem Test Mode browser E2E is intentionally performed after this PR and PR #3264 are merged and the automatic staging deployment finishes. The final staging pass covers new monthly/yearly subscription checkout, same-cycle upgrade, signed webhook fulfillment/idempotency, local order return polling, cancellation, annual credit state, and rollback gating.


---

## fix(billing): include Creem in annual credit resets (#3264)

- **SHA**: `0370d42564f034e70fc62cc193ffe7cf8a88ccfd`
- **作者**: tim-srp
- **日期**: 2026-08-05T16:22:42Z
- **PR**: #3264

### Commit Message

```
fix(billing): include Creem in annual credit resets (#3264)
```

### PR Body

## Summary

- include current active Creem yearly agreements in the existing monthly credit reset flow
- document the controlled Billing v2 index sequence and the staging-only Creem rollout checklist
- add safe example configuration values; Creem Card remains disabled by default

## Root cause

The ordinary yearly credit-reset query and its runtime predicate allowed only Stripe and Antom agreements. A valid current, active Creem yearly agreement would therefore be skipped even though it uses the same Billing v2 reset lifecycle.

## Scope and safety

- runtime behavior changes only by adding `creem` to the two existing yearly-reset provider allowlists
- no scheduler, index implementation, reconciliation, workflow, frontend, Stripe, Antom, Apple, or top-up behavior changes
- production remains disabled unless `CREEM_CARD_CHECKOUT_ENABLED=true` is explicitly configured
- the runbook requires an approved staging operations context, read-only duplicate preflight, controlled index migration, fresh pods after Secret updates, and an explicit rollback check

## Test plan

- [x] `python -m pytest tests/unit/test_billing_v2_repos.py tests/unit/test_billing_v2_yearly_credits_reset.py -q` — 80 passed locally and 80 passed in the a102 devcontainer
- [x] `bash scripts/verify-py.sh` in the a102 devcontainer — Ruff, Ruff format, Pyright (0 errors), and all 8 import-linter contracts passed
- [x] independent specification review — approved
- [x] independent code-quality review — approved after rollout lifecycle clarifications
- [x] `git diff origin/main...HEAD --check`

## Post-merge staging validation

The checked-in runbook intentionally records no unperformed staging result. Catalog/index validation, signed webhook acceptance/rejection/replay, UI gating, real Creem Test Mode checkout, yearly lifecycle, and rollback evidence must be recorded after the merged revision is deployed to staging.


---

## feat(billing): support Creem card subscription upgrades (#3263)

- **SHA**: `5e86235dc2a7c1dec434849d436cef61134e4f23`
- **作者**: tim-srp
- **日期**: 2026-08-05T15:13:09Z
- **PR**: #3263

### Commit Message

```
feat(billing): support Creem card subscription upgrades (#3263)
```

### PR Body

## Linear

Not linked.

## Summary

- Add an explicit Creem Card `upgrade` checkout intent for same-cycle, strictly higher-tier changes.
- Keep the current subscription and entitlement active until Creem reports the replacement Checkout as paid.
- Atomically promote the new Agreement, supersede the old Agreement, and schedule the old Creem subscription for cancellation.
- Preserve the existing fresh checkout default and leave Stripe, Antom, Apple, frontend visibility, and other subscription flows unchanged.

## Scope

- Backend-only dark capability; this PR does not expose a new production UI entry.
- No new collections, indexes, background workers, or provider abstraction changes.
- Creem moderation and cross-provider migration remain out of scope.

## Test plan

- [x] a102 full related regression suite: 1,014 passed.
- [x] a102 real Mongo transaction suite: 4 passed, covering replay, rollback, audit failure, and concurrent handoff.
- [x] a102 full Ruff, formatting, Pyright, and import-contract verification.
- [x] Focused review suites and independent scope review passed.
- [x] Real Creem Test Mode Starter Monthly to Pro Monthly Hosted Checkout completed through the signed public webhook route.
- [x] Creem recorded the new Pro subscription as Active, the old Starter subscription as Scheduled Cancel, and the USD 100.00 test payment as Paid.
- [x] Staging MongoDB recorded one current Pro Agreement, one non-current canceling Starter Agreement, one active 20,000-credit entitlement, and processed checkout/paid/scheduled-cancel Provider Events.
- [x] GitHub build, backend tests, static analysis, CodeQL, title, duplication, and size checks passed.
- [ ] Required human review remains; the automated P1 interpretation is addressed in a separate technical comment.

## Rollout safety

- The request defaults to `new_subscription`; only callers that explicitly send `checkout_intent=upgrade` enter the new path.
- Existing Card UI remains unchanged, so merging this backend PR does not enable the flow in production.



---

## fix(billing): preserve enterprise access after Stripe cutover (#3251)

- **SHA**: `e8d9f34d6c0f98a6ee775167713a7f862bf843f7`
- **作者**: tim-srp
- **日期**: 2026-08-05T12:43:19Z
- **PR**: #3251

### Commit Message

```
fix(billing): preserve enterprise access after Stripe cutover (#3251)

## Summary

- preserve enterprise model, OpenClaw, billing-summary, and Vertical
package access for the exact legacy Stripe account-cutover recovery
state
- prefer ordinary effective enterprise agreements and fail closed for
expired, ambiguous, near-match, or successor-owned recovery records
- extend the Vertical reconciliation migration to cover retained cutover
agreements and verify production-shaped LiteLLM team responses
- keep stored subscription status, credits, Stripe identifiers, and Lago
state unchanged

## Root cause

The Stripe account cutover intentionally retained some
enterprise-package agreements as non-current manual-review records.
Existing access surfaces only recognized current agreements in normal
provider statuses, so those teams fell back to Starter/free behavior
even though their retained enterprise period and team billing remained
valid.

## Test plan

- [x] Project backend static gate: ruff check, ruff format, pyright, and
import-linter
- [x] Targeted unit suite: 147 passed
- [x] Pre-commit backend checks, including dependency consistency and
architecture contracts
- [x] Diff and PR-size checks
```

### PR Body

## Summary

- preserve enterprise model, OpenClaw, billing-summary, and Vertical package access for the exact legacy Stripe account-cutover recovery state
- prefer ordinary effective enterprise agreements and fail closed for expired, ambiguous, near-match, or successor-owned recovery records
- extend the Vertical reconciliation migration to cover retained cutover agreements and verify production-shaped LiteLLM team responses
- keep stored subscription status, credits, Stripe identifiers, and Lago state unchanged

## Root cause

The Stripe account cutover intentionally retained some enterprise-package agreements as non-current manual-review records. Existing access surfaces only recognized current agreements in normal provider statuses, so those teams fell back to Starter/free behavior even though their retained enterprise period and team billing remained valid.

## Test plan

- [x] Project backend static gate: ruff check, ruff format, pyright, and import-linter
- [x] Targeted unit suite: 147 passed
- [x] Pre-commit backend checks, including dependency consistency and architecture contracts
- [x] Diff and PR-size checks


---

## fix(web): keep v2 stop available until terminal reply (#3261)

- **SHA**: `0c96ce4ad077340861b15e3f42ba74611136e15f`
- **作者**: kaka-srp
- **日期**: 2026-08-05T12:23:25Z
- **PR**: #3261

### Commit Message

```
fix(web): keep v2 stop available until terminal reply (#3261)

## Summary
- keep the v2 session composer in generating/Stop state through
intermediate assistant segments
- clear generation only on the same validated terminal assistant-segment
contract used by Agent Builder (`final`/`error`, `terminal=true`)
- reconcile the waiting state from persisted Mattermost thread history
after WebSocket reconnects, while keeping button-triggered `/stop`
hidden

## Root cause
The session page cleared `isWaitingForBotReply` on every ordinary bot
`posted` event. Engine v2 publishes intermediate assistant segments
before tool execution finishes, so the first segment replaced Stop with
the disabled send arrow even though the run was still active. A fixed
60-second fallback also expired during healthy long-running turns.

## Performance
- no polling, network request, or new timer
- ordinary event classification is constant-time metadata parsing
- history reconciliation is skipped while idle and reverse-scans only
back to the latest user post while waiting

## Test plan
- [x] `bash scripts/verify-web.sh <changed paths>` (TypeScript, 263
related tests, ESLint)
- [x] targeted state-machine and Agent Builder tests (203 tests)
- [x] `pnpm dup:tests`
- [x] `bash scripts/verify-changed.sh` after rebasing onto latest
`origin/main`
- [x] local `$code-review`: no findings
```

### PR Body

## Summary
- keep the v2 session composer in generating/Stop state through intermediate assistant segments
- clear generation only on the same validated terminal assistant-segment contract used by Agent Builder (`final`/`error`, `terminal=true`)
- reconcile the waiting state from persisted Mattermost thread history after WebSocket reconnects, while keeping button-triggered `/stop` hidden

## Root cause
The session page cleared `isWaitingForBotReply` on every ordinary bot `posted` event. Engine v2 publishes intermediate assistant segments before tool execution finishes, so the first segment replaced Stop with the disabled send arrow even though the run was still active. A fixed 60-second fallback also expired during healthy long-running turns.

## Performance
- no polling, network request, or new timer
- ordinary event classification is constant-time metadata parsing
- history reconciliation is skipped while idle and reverse-scans only back to the latest user post while waiting

## Test plan
- [x] `bash scripts/verify-web.sh <changed paths>` (TypeScript, 263 related tests, ESLint)
- [x] targeted state-machine and Agent Builder tests (203 tests)
- [x] `pnpm dup:tests`
- [x] `bash scripts/verify-changed.sh` after rebasing onto latest `origin/main`
- [x] local `$code-review`: no findings


---

## refactor(web): agents-manager MVVM cleanup — view-model contract, purchase controller, dead branches (#3249)

- **SHA**: `a9adca1e8e0c26be7ef29e0ef77d24336b88085b`
- **作者**: bill-srp
- **日期**: 2026-08-05T11:49:38Z
- **PR**: #3249

### Commit Message

```
refactor(web): agents-manager MVVM cleanup — view-model contract, purchase controller, dead branches (#3249)

## Summary

Makes `agents-manager` the reference MVVM implementation and codifies
the pattern in `web/app/AGENTS.md`.

- **New AGENTS.md rules**: (1) Page ViewModel (MVVM) — `page.tsx` /
`*Client.tsx` shells hold no state, effects, or derived values;
everything lives in a co-located `useViewModel.ts` (mirrors
enterprise-admin's "pages hold zero logic"). (2) Filename rule —
page-colocated hook modules are named after their primary hook.
- **`useViewModel` exposes `catalog.cards`**: per-card derived render
state (`hired` / `installedAgent` / `engineInstalled` / `isLocked` /
`isMenuOpen` / `isPurchased` / `isPurchasing` / `isUpdating`), removing
the inline derivation from `AgentsManagerClient`'s render loop.
- **`usePackPurchase` controller extraction** (renamed from
`purchaseFlow.ts`): owns all purchase state — checkout popup lifecycle,
BroadcastChannel purchase-return protocol, sessionStorage attempt
persistence, compat purchased-ids merge. Keeps `useViewModel.ts` inside
the 600/300 line-limit gates.
- **`useRovingTabList`**: dedupes the two identical roving-tabindex
keyboard handlers (Arrow/Home/End + focus) for the category and view
tablists.
- **Contract trims**: both view models now return exactly what their
pages consume (list VM: −7 fields; detail VM: −3 fields incl. the unused
`openInstalledEngineChat` engine-chat path). Specs migrated to assert
through `catalog.cards`, the same surface the page renders from.
- **Dead-branch removal**: 21 unreachable `t('key') || 'literal'`
fallbacks across both clients — `t()` never returns falsy (missing keys
return the key path; dictionaries pre-merge English), and all keys exist
in `en.ts`.
- **`_components/` → `components/`**: plain colocation; the `_` opt-out
prefix was unnecessary.

One behavior-affecting fix caught in review and locked by a new
regression test: closing any modal still clears the purchase error
banner (`clearPurchaseMessages` composed into the VM-level
`closeModal`).

Rebased on latest `main`, preserving #3244 (start-chat routing →
`buildWorkspaceNewChatHref`, AgentCard `stopPropagation` fix).

## Test plan

- [x] `bash scripts/verify-web.sh` — 7 CI guards + tsc + eslint + full
vitest: 595 files / 8151 passed
- [x] `tests/unit/app/agents-manager/` — 168 passed (4 new/extended
specs: `catalog.cards` derivation ×2, purchase-error-cleared-on-close
regression, spec migration to cards)
- [x] Coverage gate pre-flighted: 88.75 / 81.98 / 87.45 / 91.23 vs
thresholds 83 / 75 / 81 / 85
- [x] `pnpm lint:imports` (dependency-cruiser, 0 errors) + `pnpm
lint:deadcode` (knip clean)
- [ ] `web-build-check` (`next build`) — CI-only

## Update: publish page extraction (second slice)

- **`publish/PublishAgentsClient.tsx`: 1049 → 213 lines**, render-only.
Its 21 `useState` cells + mutation + 18 callbacks moved into
`publish/useViewModel.ts` (composer, `{ actions, cards, modals, status,
view }`), controller hooks `publish/hooks/usePackListingActions.ts`
(list/share/unshare/delete/hide-market lifecycle) +
`usePackListingActions`-composed `usePublishMutationActions.ts`, and
pure modules under `publish/lib/` (`card-model`, `card-actions`,
`install-action`, `listing-cache-patches` — named to dodge the R2
`*-cache` pathname glob, which is also now documented).
- New specs for the VM (cards derivation incl. deprecated-hiding +
highlight, modal/install wiring) and the listing controller (lifecycle
incl. RQ cache-patch assertions + error mapping); the 4 pre-existing
publish specs pass unedited.
- Drift review: close-handler in-flight guards, `bannerMessage`
precedence, auth early-return, and the 7-entry `useModalStackEscape`
stack all byte-identical to the original.
- AGENTS.md: new "Route directory structure" convention (shell →
`useViewModel` → `hooks/` → `lib/` → `components/`), reference
implementation = `agents-manager/publish/`.
- Re-verified after fold-in: full `verify-web.sh` green (597 files /
8157 tests), coverage 88.78/82.08/87.55/91.27.
```

### PR Body

## Summary

Makes `agents-manager` the reference MVVM implementation and codifies the pattern in `web/app/AGENTS.md`.

- **New AGENTS.md rules**: (1) Page ViewModel (MVVM) — `page.tsx` / `*Client.tsx` shells hold no state, effects, or derived values; everything lives in a co-located `useViewModel.ts` (mirrors enterprise-admin's "pages hold zero logic"). (2) Filename rule — page-colocated hook modules are named after their primary hook.
- **`useViewModel` exposes `catalog.cards`**: per-card derived render state (`hired` / `installedAgent` / `engineInstalled` / `isLocked` / `isMenuOpen` / `isPurchased` / `isPurchasing` / `isUpdating`), removing the inline derivation from `AgentsManagerClient`'s render loop.
- **`usePackPurchase` controller extraction** (renamed from `purchaseFlow.ts`): owns all purchase state — checkout popup lifecycle, BroadcastChannel purchase-return protocol, sessionStorage attempt persistence, compat purchased-ids merge. Keeps `useViewModel.ts` inside the 600/300 line-limit gates.
- **`useRovingTabList`**: dedupes the two identical roving-tabindex keyboard handlers (Arrow/Home/End + focus) for the category and view tablists.
- **Contract trims**: both view models now return exactly what their pages consume (list VM: −7 fields; detail VM: −3 fields incl. the unused `openInstalledEngineChat` engine-chat path). Specs migrated to assert through `catalog.cards`, the same surface the page renders from.
- **Dead-branch removal**: 21 unreachable `t('key') || 'literal'` fallbacks across both clients — `t()` never returns falsy (missing keys return the key path; dictionaries pre-merge English), and all keys exist in `en.ts`.
- **`_components/` → `components/`**: plain colocation; the `_` opt-out prefix was unnecessary.

One behavior-affecting fix caught in review and locked by a new regression test: closing any modal still clears the purchase error banner (`clearPurchaseMessages` composed into the VM-level `closeModal`).

Rebased on latest `main`, preserving #3244 (start-chat routing → `buildWorkspaceNewChatHref`, AgentCard `stopPropagation` fix).

## Test plan

- [x] `bash scripts/verify-web.sh` — 7 CI guards + tsc + eslint + full vitest: 595 files / 8151 passed
- [x] `tests/unit/app/agents-manager/` — 168 passed (4 new/extended specs: `catalog.cards` derivation ×2, purchase-error-cleared-on-close regression, spec migration to cards)
- [x] Coverage gate pre-flighted: 88.75 / 81.98 / 87.45 / 91.23 vs thresholds 83 / 75 / 81 / 85
- [x] `pnpm lint:imports` (dependency-cruiser, 0 errors) + `pnpm lint:deadcode` (knip clean)
- [ ] `web-build-check` (`next build`) — CI-only

## Update: publish page extraction (second slice)

- **`publish/PublishAgentsClient.tsx`: 1049 → 213 lines**, render-only. Its 21 `useState` cells + mutation + 18 callbacks moved into `publish/useViewModel.ts` (composer, `{ actions, cards, modals, status, view }`), controller hooks `publish/hooks/usePackListingActions.ts` (list/share/unshare/delete/hide-market lifecycle) + `usePackListingActions`-composed `usePublishMutationActions.ts`, and pure modules under `publish/lib/` (`card-model`, `card-actions`, `install-action`, `listing-cache-patches` — named to dodge the R2 `*-cache` pathname glob, which is also now documented).
- New specs for the VM (cards derivation incl. deprecated-hiding + highlight, modal/install wiring) and the listing controller (lifecycle incl. RQ cache-patch assertions + error mapping); the 4 pre-existing publish specs pass unedited.
- Drift review: close-handler in-flight guards, `bannerMessage` precedence, auth early-return, and the 7-entry `useModalStackEscape` stack all byte-identical to the original.
- AGENTS.md: new "Route directory structure" convention (shell → `useViewModel` → `hooks/` → `lib/` → `components/`), reference implementation = `agents-manager/publish/`.
- Re-verified after fold-in: full `verify-web.sh` green (597 files / 8157 tests), coverage 88.78/82.08/87.55/91.27.


---

## feat(council): synthesis report tab and quoted dispatch settings (#3255)

- **SHA**: `ce505b8f75f3200b9689e58c0bc98960c8861fa7`
- **作者**: bill-srp
- **日期**: 2026-08-05T11:43:10Z
- **PR**: #3255

### Commit Message

```
feat(council): synthesis report tab and quoted dispatch settings (#3255)

## Linear
<!-- 无对应 Linear issue：会话内 UX 改进需求 -->

## Summary
- **Final report moves into the Synthesis panel.** When the synthesis
summary carries a stable-host report link, the Synthesis card renders
`Summary` / `Full report` tabs: the Full report tab fetches the artifact
and renders the markdown inline (shared `MarkdownRenderer`), and
clicking the report's file card inside the Summary switches to that tab
— a capture-phase handler intercepts the click before
`MarkdownContent`'s container listener can open the artifact drawer. Any
other file card keeps the drawer behavior, and summaries without a
report link keep the existing single view. (First pass authored by
Codex; click-to-switch refinement applied on top after the Codex runtime
lost write access.)
- **Dispatch message quotes tier and depth.** `/council <topic>` now
sends `tier: "standard"` / `depth: "deep"` so the agent reads the
settings as literal values rather than words continuing the topic. The
council control-reply filter accepts the quoted form too, keeping
manually typed quoted replies out of the synthesis-brief selection.

## Test plan
- [x] `CouncilClient.unit.spec.tsx`: four synthesis-tab cases (tabs
appear with a report link, Full report renders inline with the report
URL, clicking the summary's report card switches tabs without opening
the drawer, no tabs without a link) — click-to-switch written RED-first;
dispatch assertions flipped to the quoted form RED-first
- [x] `thread-messages.unit.spec.ts`: quoted `tier:`/`depth:` control
replies filtered like unquoted ones
- [x] All council suites green (122 tests) + `bash scripts/verify-web.sh
--no-test` (guards + tsc + eslint)
- [x] Browser-verified on a real staging done run via local dev: tabs
render, full report displays inline, summary card click switches tabs
with no drawer
```

### PR Body

## Linear
<!-- 无对应 Linear issue：会话内 UX 改进需求 -->

## Summary
- **Final report moves into the Synthesis panel.** When the synthesis summary carries a stable-host report link, the Synthesis card renders `Summary` / `Full report` tabs: the Full report tab fetches the artifact and renders the markdown inline (shared `MarkdownRenderer`), and clicking the report's file card inside the Summary switches to that tab — a capture-phase handler intercepts the click before `MarkdownContent`'s container listener can open the artifact drawer. Any other file card keeps the drawer behavior, and summaries without a report link keep the existing single view. (First pass authored by Codex; click-to-switch refinement applied on top after the Codex runtime lost write access.)
- **Dispatch message quotes tier and depth.** `/council <topic>` now sends `tier: "standard"` / `depth: "deep"` so the agent reads the settings as literal values rather than words continuing the topic. The council control-reply filter accepts the quoted form too, keeping manually typed quoted replies out of the synthesis-brief selection.

## Test plan
- [x] `CouncilClient.unit.spec.tsx`: four synthesis-tab cases (tabs appear with a report link, Full report renders inline with the report URL, clicking the summary's report card switches tabs without opening the drawer, no tabs without a link) — click-to-switch written RED-first; dispatch assertions flipped to the quoted form RED-first
- [x] `thread-messages.unit.spec.ts`: quoted `tier:`/`depth:` control replies filtered like unquoted ones
- [x] All council suites green (122 tests) + `bash scripts/verify-web.sh --no-test` (guards + tsc + eslint)
- [x] Browser-verified on a real staging done run via local dev: tabs render, full report displays inline, summary card click switches tabs with no drawer


---

## feat(billing): support Creem subscription downgrades (#3260)

- **SHA**: `a6346f314e4743f33bb73327969056d2a1b20726`
- **作者**: tim-srp
- **日期**: 2026-08-05T11:39:06Z
- **PR**: #3260

### Commit Message

```
feat(billing): support Creem subscription downgrades (#3260)

## Linear

N/A

## Summary

- Add same-cycle Creem subscription downgrade and downgrade cancellation
through the existing provider-neutral subscription endpoints. Product
IDs remain server-owned and Creem uses `proration-none`, so the current
ZooClaw plan stays active until the next paid period.
- Converge Creem Product update webhooks and paid renewal settlement
with the durable scheduled change, using the existing management lease
and owner/schedule-fenced CAS for idempotency and race safety.
- Preserve whole-subscription cancel/resume while a Creem downgrade is
pending by accepting only the exact current Product or the exact
persisted pending-downgrade Product.
- Keep the scope Creem-only: no frontend changes, no Stripe/Antom/Apple
behavior changes, and no new collections, indexes, jobs, Provider
registry, or environment variables.

## Test plan

- [x] a102 clean detached worktree at commit `62baa017b`: `bash
scripts/verify-py.sh` — Ruff check/format, Pyright (`0 errors, 0
warnings`), and all 8 import contracts passed.
- [x] 380 targeted tests passed: 270 Creem/route tests plus 110 Stripe
and Antom regression tests.
- [x] TDD regression for pending downgrade → whole-subscription
cancel/resume: 5 expected failures before the fix, then 5/5 passed after
the Creem-only Product-state fix.
- [x] Real Creem Test Mode E2E on subscription
`sub_46vKxhvaAq6o0QVI35kd48`: Pro → schedule Starter → cancel whole
subscription → resume automatic renewal → cancel downgrade; all four API
calls returned HTTP 200.
- [x] Final state verified independently: Mongo Agreement is
current/active Pro with no management lease; Creem reports active Pro
with `canceled_at=null` and the original period unchanged.
- [x] PR size gate passed at 2,997/3,000 lines after removing repeated
test fixtures/calls without removing scenarios or assertions.
- [ ] Natural next-period settlement was not time-accelerated because
Creem Test Mode does not provide a test clock. It is covered by
deterministic renewal, race, and idempotency unit tests; no Mongo
timestamps were modified.

## Rollout safety

- Backend-only change. The existing Card/Creem frontend entry remains
controlled by the previously shipped staging-only environment gate, so
production UI behavior is unchanged until that existing flag is enabled
separately.
- Existing Stripe and Antom dispatch paths remain unchanged and are
covered by the regression suite above.
```

### PR Body

## Linear

N/A

## Summary

- Add same-cycle Creem subscription downgrade and downgrade cancellation through the existing provider-neutral subscription endpoints. Product IDs remain server-owned and Creem uses `proration-none`, so the current ZooClaw plan stays active until the next paid period.
- Converge Creem Product update webhooks and paid renewal settlement with the durable scheduled change, using the existing management lease and owner/schedule-fenced CAS for idempotency and race safety.
- Preserve whole-subscription cancel/resume while a Creem downgrade is pending by accepting only the exact current Product or the exact persisted pending-downgrade Product.
- Keep the scope Creem-only: no frontend changes, no Stripe/Antom/Apple behavior changes, and no new collections, indexes, jobs, Provider registry, or environment variables.

## Test plan

- [x] a102 clean detached worktree at commit `62baa017b`: `bash scripts/verify-py.sh` — Ruff check/format, Pyright (`0 errors, 0 warnings`), and all 8 import contracts passed.
- [x] 380 targeted tests passed: 270 Creem/route tests plus 110 Stripe and Antom regression tests.
- [x] TDD regression for pending downgrade → whole-subscription cancel/resume: 5 expected failures before the fix, then 5/5 passed after the Creem-only Product-state fix.
- [x] Real Creem Test Mode E2E on subscription `sub_46vKxhvaAq6o0QVI35kd48`: Pro → schedule Starter → cancel whole subscription → resume automatic renewal → cancel downgrade; all four API calls returned HTTP 200.
- [x] Final state verified independently: Mongo Agreement is current/active Pro with no management lease; Creem reports active Pro with `canceled_at=null` and the original period unchanged.
- [x] PR size gate passed at 2,997/3,000 lines after removing repeated test fixtures/calls without removing scenarios or assertions.
- [ ] Natural next-period settlement was not time-accelerated because Creem Test Mode does not provide a test clock. It is covered by deterministic renewal, race, and idempotency unit tests; no Mongo timestamps were modified.

## Rollout safety

- Backend-only change. The existing Card/Creem frontend entry remains controlled by the previously shipped staging-only environment gate, so production UI behavior is unchanged until that existing flag is enabled separately.
- Existing Stripe and Antom dispatch paths remain unchanged and are covered by the regression suite above.


---

## fix(chat): expose stop while session reply is pending (#3259)

- **SHA**: `f3839cb8066f518caba71edbe94145406dffc75d`
- **作者**: kaka-srp
- **日期**: 2026-08-05T11:20:59Z
- **PR**: #3259

### Commit Message

```
fix(chat): expose stop while session reply is pending (#3259)

## Summary

- Mark the Mattermost channel as waiting as soon as a standalone
session-thread reply starts, so the composer immediately replaces Send
with Stop.
- Clear the optimistic waiting state when the post fails; hidden
button-generated `/stop` behavior is unchanged.
- Reuse the existing Mattermost waiting state and timeout without adding
network requests, polling, or persistence.

## Root cause

The v2 session-thread route sends replies through a standalone
Mattermost API client instead of the shared `sendMessage` path. That
bypassed the existing `markUserSent` transition, so `isGenerating` could
remain false until a later turn-status event and the composer kept
showing a disabled Send button rather than Stop.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to the changed hook,
Mattermost state/provider, and related unit tests
- [x] TypeScript type-check
- [x] ESLint and web governance guards
- [x] 261 related Vitest tests
- [x] Local code review completed

## Review follow-up

- Fixed the verified cross-channel races reported by Codex review:
delayed failures cancel only their own channel's timeout, and channel
navigation no longer drops another pending reply's fallback cleanup.
- Waiting fallbacks are now independently scoped by Mattermost channel,
including concurrent pending replies and inactive-channel bot posts.

## Performance

No additional API, database, or polling work. The change performs
existing in-memory waiting-state updates only. Concurrent pending
channels can each hold one existing 60-second fallback timer, which is
cleared on reply, failure, timeout, reset, or unmount.
```

### PR Body

## Summary

- Mark the Mattermost channel as waiting as soon as a standalone session-thread reply starts, so the composer immediately replaces Send with Stop.
- Clear the optimistic waiting state when the post fails; hidden button-generated `/stop` behavior is unchanged.
- Reuse the existing Mattermost waiting state and timeout without adding network requests, polling, or persistence.

## Root cause

The v2 session-thread route sends replies through a standalone Mattermost API client instead of the shared `sendMessage` path. That bypassed the existing `markUserSent` transition, so `isGenerating` could remain false until a later turn-status event and the composer kept showing a disabled Send button rather than Stop.

## Test plan

- [x] `bash scripts/verify-web.sh` scoped to the changed hook, Mattermost state/provider, and related unit tests
- [x] TypeScript type-check
- [x] ESLint and web governance guards
- [x] 261 related Vitest tests
- [x] Local code review completed

## Review follow-up

- Fixed the verified cross-channel races reported by Codex review: delayed failures cancel only their own channel's timeout, and channel navigation no longer drops another pending reply's fallback cleanup.
- Waiting fallbacks are now independently scoped by Mattermost channel, including concurrent pending replies and inactive-channel bot posts.

## Performance

No additional API, database, or polling work. The change performs existing in-memory waiting-state updates only. Concurrent pending channels can each hold one existing 60-second fallback timer, which is cleared on reply, failure, timeout, reset, or unmount.


---

## fix(web): render modal overlays at viewport root (#3257)

- **SHA**: `447c285de36416c8153a4fe95d41eeea12739d2b`
- **作者**: lynn Zhuang
- **日期**: 2026-08-05T10:20:53Z
- **PR**: #3257

### Commit Message

```
fix(web): render modal overlays at viewport root (#3257)

## Summary
- add a hydration-safe `ViewportPortal` that renders full-screen
overlays under `document.body`
- migrate chat, publish, settings, preview, billing, and drag-capture
overlays to the shared viewport-root boundary
- keep the redeem gift artwork visible from the first animation frame
while preserving the drop, lid, and confetti motion
- add portal-boundary and gift-animation regression coverage

## Root cause
Several overlays were rendered inside application panel subtrees.
Ancestors that establish a containing block can constrain `position:
fixed`, so the backdrop covered only the right panel instead of the
viewport. Rendering these layers through a shared body portal restores
viewport-relative geometry consistently.

The redeem gift SVG also started its drop animation with `opacity: 0`,
which left an empty icon slot when the modal was opened or captured on
the first frame.

## Test plan
- [x] `bash scripts/verify-web.sh` — TypeScript, 599 test files / 8171
passing tests, and ESLint
- [x] `bash scripts/verify-changed.sh`
- [x] focused UserMenu, MobileAppModal, and AnimatedGiftDropIcon unit
tests
- [x] local Playwright validation at 1600x900: overlay parent is `BODY`,
overlay bounds match the viewport, and the gift artwork is visible at
animation frame zero
```

### PR Body

## Summary
- add a hydration-safe `ViewportPortal` that renders full-screen overlays under `document.body`
- migrate chat, publish, settings, preview, billing, and drag-capture overlays to the shared viewport-root boundary
- keep the redeem gift artwork visible from the first animation frame while preserving the drop, lid, and confetti motion
- add portal-boundary and gift-animation regression coverage

## Root cause
Several overlays were rendered inside application panel subtrees. Ancestors that establish a containing block can constrain `position: fixed`, so the backdrop covered only the right panel instead of the viewport. Rendering these layers through a shared body portal restores viewport-relative geometry consistently.

The redeem gift SVG also started its drop animation with `opacity: 0`, which left an empty icon slot when the modal was opened or captured on the first frame.

## Test plan
- [x] `bash scripts/verify-web.sh` — TypeScript, 599 test files / 8171 passing tests, and ESLint
- [x] `bash scripts/verify-changed.sh`
- [x] focused UserMenu, MobileAppModal, and AnimatedGiftDropIcon unit tests
- [x] local Playwright validation at 1600x900: overlay parent is `BODY`, overlay bounds match the viewport, and the gift artwork is visible at animation frame zero


---

## fix(chat): show No chats for empty agent history (#3253)

- **SHA**: `9e4df1d8f1061f2ffd419db5bf43050f7cf01edc`
- **作者**: lynn Zhuang
- **日期**: 2026-08-05T10:16:00Z
- **PR**: #3253

### Commit Message

```
fix(chat): show No chats for empty agent history (#3253)

## Summary

- derive Session History visibility from an explicit default-DM history
fact instead of session-row count
- show a non-interactive `No chats` empty state when both DM history and
session rows are empty
- remove the expanded child `New Task` fallback while keeping the
agent-row pencil action as the creation entry point
- treat any stored DM post as history; no author, `Hi`, or `/new`
filtering
- preserve the legacy session-derived UI only when an older backend
omits `has_dm_history`, so independent frontend/backend rollout is safe

## Root cause

The sidebar used session-channel rows to infer whether the independent
default Mattermost DM had history. Those data sources can diverge, so
Session History appeared inconsistently. The zero-session fallback also
rendered a clickable New Task child that looked like a history record.

## Test plan

- [x] Backend DM-history and workspace-conversation tests: 36 passed
- [x] Frontend sidebar/query/council tests: 61 passed
- [x] Frontend TypeScript and ESLint checks
- [x] Backend Ruff check and format check
- [x] Backend Pyright with the worktree Python environment: 0 errors
- [x] Backend import-linter contracts: 8 kept
- [x] Synchronized the branch with `origin/main`; GitHub's merge-preview
checks also passed against current main
- [x] Added a regression test preserving cached `No chats` during a
failed background refresh
- [x] Added a regression test for a frontend-first rollout against an
older backend response

## Manual verification

1. Expand a new agent with no DM posts and no session rows; confirm `No
chats` is shown.
2. Confirm the empty state is not clickable and no child New Task row is
present.
3. Click the pencil icon, send a message, then confirm Session History
appears.
4. Confirm real session rows remain visible independently of default-DM
history.
```

### PR Body

## Summary

- derive Session History visibility from an explicit default-DM history fact instead of session-row count
- show a non-interactive `No chats` empty state when both DM history and session rows are empty
- remove the expanded child `New Task` fallback while keeping the agent-row pencil action as the creation entry point
- treat any stored DM post as history; no author, `Hi`, or `/new` filtering
- preserve the legacy session-derived UI only when an older backend omits `has_dm_history`, so independent frontend/backend rollout is safe

## Root cause

The sidebar used session-channel rows to infer whether the independent default Mattermost DM had history. Those data sources can diverge, so Session History appeared inconsistently. The zero-session fallback also rendered a clickable New Task child that looked like a history record.

## Test plan

- [x] Backend DM-history and workspace-conversation tests: 36 passed
- [x] Frontend sidebar/query/council tests: 61 passed
- [x] Frontend TypeScript and ESLint checks
- [x] Backend Ruff check and format check
- [x] Backend Pyright with the worktree Python environment: 0 errors
- [x] Backend import-linter contracts: 8 kept
- [x] Synchronized the branch with `origin/main`; GitHub's merge-preview checks also passed against current main
- [x] Added a regression test preserving cached `No chats` during a failed background refresh
- [x] Added a regression test for a frontend-first rollout against an older backend response

## Manual verification

1. Expand a new agent with no DM posts and no session rows; confirm `No chats` is shown.
2. Confirm the empty state is not clickable and no child New Task row is present.
3. Click the pencil icon, send a message, then confirm Session History appears.
4. Confirm real session rows remain visible independently of default-DM history.


---

## fix(chat): stop v2 session thread generation (#3256)

- **SHA**: `95ff913000b24275338e4417aa123d4906729a4c`
- **作者**: kaka-srp
- **日期**: 2026-08-05T09:46:27Z
- **PR**: #3256

### Commit Message

```
fix(chat): stop v2 session thread generation (#3256)

## Summary

- wire the v2 session-thread Stop button to a tagged Mattermost `/stop`
reply
- hide only button-generated control posts from the ECAP transcript
while keeping manually typed `/stop` messages visible
- latch a successful stop request for the current generation so repeated
UI or runtime abort calls do not create duplicate posts; failed sends
remain retryable

## Root cause

The v2 session-thread page passed a no-op abort handler to the shared
chat runtime and input. Unlike the direct-chat page, it therefore never
emitted the `/stop` command consumed by the channel control path.

## Performance

- the hidden-post check stays inside the existing memoized single-pass
post filter
- stop deduplication is an in-memory ref with no timer, polling, or
additional read request
- ACS authorization uses the already loaded managed-v2 session tuple and
adds no Mattermost or database call

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] related Vitest suite — 4 files and 80 tests passed
- [x] TypeScript and ESLint checks
- [x] `git diff --check`

## Companion change

- https://github.com/SerendipityOneInc/agent-channel-service/pull/60
```

### PR Body

## Summary

- wire the v2 session-thread Stop button to a tagged Mattermost `/stop` reply
- hide only button-generated control posts from the ECAP transcript while keeping manually typed `/stop` messages visible
- latch a successful stop request for the current generation so repeated UI or runtime abort calls do not create duplicate posts; failed sends remain retryable

## Root cause

The v2 session-thread page passed a no-op abort handler to the shared chat runtime and input. Unlike the direct-chat page, it therefore never emitted the `/stop` command consumed by the channel control path.

## Performance

- the hidden-post check stays inside the existing memoized single-pass post filter
- stop deduplication is an in-memory ref with no timer, polling, or additional read request
- ACS authorization uses the already loaded managed-v2 session tuple and adds no Mattermost or database call

## Test plan

- [x] `bash scripts/verify-changed.sh`
- [x] related Vitest suite — 4 files and 80 tests passed
- [x] TypeScript and ESLint checks
- [x] `git diff --check`

## Companion change

- https://github.com/SerendipityOneInc/agent-channel-service/pull/60


---

## fix(agent-builder): recover V2 runtime and model selection (#3254)

- **SHA**: `1f41a285f3d3a42a43bc7dfe67f74a4261fd415f`
- **作者**: kaka-srp
- **日期**: 2026-08-05T09:31:12Z
- **PR**: #3254

### Commit Message

```
fix(agent-builder): recover V2 runtime and model selection (#3254)

## Summary

- keep Agent Builder V2 workspace access recoverable when a lease
renewal or runtime activation is temporarily unavailable
- make V2 model selection use the ordinary Engine-agent model catalog
and resolve public aliases to Engine provider IDs
- preserve activation compatibility for projects that already persisted
the historical Agent Studio model aliases, without exposing those
aliases for new selection
- hide the unsupported `auto` option in the V2 Builder composer by using
the same Engine runtime contract as ordinary Engine-agent chat

## Why

Returning to a backgrounded Builder page could leave it stuck in a
preparing/error state until a manual refresh. V2 Builder model selection
had also drifted from ordinary Engine-agent chat, while existing
projects still carried historical Agent Studio aliases. This change
restores automatic recovery and aligns new selections with the shared
catalog while keeping old projects usable during the catalog transition.

The two missing historical provider aliases were synchronized into the
staging Engine model catalog separately as operational data. This PR
does not introduce a second catalog source of truth.

## Scope

- Agent Builder V2 paths only
- Agent Builder V1 model resolution and runtime behavior are unchanged
- no changes to submitted-agent installation or post-submit workflows

## Validation

- `bash scripts/verify-web.sh` for the changed Builder files
- targeted frontend unit tests: 62 passed
- `bash scripts/verify-py.sh`
- targeted backend unit tests: 29 passed
- pre-push changed-surface verification passed after rebasing onto
current `origin/main`

## Design

-
`docs/superpowers/specs/2026-08-05-agent-builder-v2-recovery-model-artifact.md`
```

### PR Body

## Summary

- keep Agent Builder V2 workspace access recoverable when a lease renewal or runtime activation is temporarily unavailable
- make V2 model selection use the ordinary Engine-agent model catalog and resolve public aliases to Engine provider IDs
- preserve activation compatibility for projects that already persisted the historical Agent Studio model aliases, without exposing those aliases for new selection
- hide the unsupported `auto` option in the V2 Builder composer by using the same Engine runtime contract as ordinary Engine-agent chat

## Why

Returning to a backgrounded Builder page could leave it stuck in a preparing/error state until a manual refresh. V2 Builder model selection had also drifted from ordinary Engine-agent chat, while existing projects still carried historical Agent Studio aliases. This change restores automatic recovery and aligns new selections with the shared catalog while keeping old projects usable during the catalog transition.

The two missing historical provider aliases were synchronized into the staging Engine model catalog separately as operational data. This PR does not introduce a second catalog source of truth.

## Scope

- Agent Builder V2 paths only
- Agent Builder V1 model resolution and runtime behavior are unchanged
- no changes to submitted-agent installation or post-submit workflows

## Validation

- `bash scripts/verify-web.sh` for the changed Builder files
- targeted frontend unit tests: 62 passed
- `bash scripts/verify-py.sh`
- targeted backend unit tests: 29 passed
- pre-push changed-surface verification passed after rebasing onto current `origin/main`

## Design

- `docs/superpowers/specs/2026-08-05-agent-builder-v2-recovery-model-artifact.md`


---

## fix(agent-builder): restore v1 test session resets (#3250)

- **SHA**: `34c115304425d270008d2f15376ee0f727cdbf19`
- **作者**: kaka-srp
- **日期**: 2026-08-05T09:11:34Z
- **PR**: #3250

### Commit Message

```
fix(agent-builder): restore v1 test session resets (#3250)

## Summary

- restore the automatic `/new` handshake for reused Agent Builder v1
Pack Test sessions
- keep Engine v2 test runs on their fresh per-run sessions and correct
runtime-specific regression fixtures

## Root cause

The Engine-backed Agent Builder v2 rollout removed the shared preview
chat's reset state machine because v2 creates a fresh Engine session for
every test run. The same component still serves `computer_v1`, whose
Mattermost test bot session can be reused, so v1 lost its session
boundary and could inherit stale context from an earlier Package & Test
run.

## Test plan

- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/useAgentBuilderTestAutoReset.ts'
'web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push frontend checks
```

### PR Body

## Summary

- restore the automatic `/new` handshake for reused Agent Builder v1 Pack Test sessions
- keep Engine v2 test runs on their fresh per-run sessions and correct runtime-specific regression fixtures

## Root cause

The Engine-backed Agent Builder v2 rollout removed the shared preview chat's reset state machine because v2 creates a fresh Engine session for every test run. The same component still serves `computer_v1`, whose Mattermost test bot session can be reused, so v1 lost its session boundary and could inherit stale context from an earlier Package & Test run.

## Test plan

- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/useAgentBuilderTestAutoReset.ts' 'web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push frontend checks


---

## fix(tracking): set GA4 user id after login (#3224)

- **SHA**: `2c3d357a3bff23bc021d7f7fcc41b28d78f37dd0`
- **作者**: Mori-srp
- **日期**: 2026-08-05T09:01:57Z
- **PR**: #3224

### Commit Message

```
fix(tracking): set GA4 user id after login (#3224)

## Summary

- set GA4 User-ID with the page-level `gtag('set', { user_id })` command
after Account confirmation
- clear the identity with `gtag('set', { user_id: null })` on logout /
auth reset
- preserve the existing `dataLayer` compatibility objects
- prove the real Account `created=true` path sets User-ID before
`account_created`
- keep GA4 User-ID active when the direct Google Ads destination is
enabled, per the Owner-approved V1 boundary

## Root cause

The Google tag is initialized before the frontend knows the
authenticated Account. The previous implementation tried to add late
identity by issuing a second GA4 `config` command. Production BigQuery
then showed `account_created` and later events without top-level
`user_id`.

Google's late-login contract uses a page-level `set` so subsequent
events inherit User-ID, and uses `null` when the user signs out:
https://developers.google.com/analytics/devguides/collection/ga4/user-id

## Scope and known boundaries

- refreshed onto `main@405e42090`; the final PR diff remains limited to
`tracking.ts` and two unit-test files
- no authentication business-flow, GTM, Consent, Page View, source
handoff, backend, or GA4-admin changes
- no email, phone, OTP, token, or chat content is added to analytics
- Owner explicitly prioritizes GA4 Account identity for this V1 even
when `NEXT_PUBLIC_GOOGLE_ADS_ENABLED=true`
- because `gtag('set')` is page-global, a same-page Google Ads
destination may inherit the Account UID; this is an accepted, disclosed
V1 risk requiring human review and later destination isolation
- this PR does not claim that Ads payloads are UID-free
- a pre-existing low-probability race between anonymous bootstrap and
extremely fast popup login remains outside this minimal fix
- Draft only; no merge or deployment is requested by this update

## Test plan

- [x] latest-main sync with no semantic conflicts
- [x] repository governance guards
- [x] TypeScript
- [x] focused tracking + auth-manager tests: 129 / 129
- [x] repository matcher gate: 17 files, 402 / 402
- [x] targeted and commit-hook ESLint: 0 errors
- [x] source / test duplication gates
- [x] `git diff --check`
- [x] independent read-only adversarial review: P0-P3 no findings
- [x] explicit regression: Ads enabled still sets GA4 User-ID
- [x] refreshed CI / CodeQL / Codex / Claude review; both AI reviewers
request human sign-off only for the disclosed Ads inheritance boundary
- [ ] human review of the disclosed Ads inheritance boundary
- [ ] Staging Network / DebugView: `login_succeeded` has User-ID
- [ ] Staging: later events keep the same User-ID and logout clears it
- [ ] Staging new-account receipt, only after a separately approved
fresh alias
- [ ] Production BigQuery / Account present-missing reconciliation
```

### PR Body

## Summary

- set GA4 User-ID with the page-level `gtag('set', { user_id })` command after Account confirmation
- clear the identity with `gtag('set', { user_id: null })` on logout / auth reset
- preserve the existing `dataLayer` compatibility objects
- prove the real Account `created=true` path sets User-ID before `account_created`
- keep GA4 User-ID active when the direct Google Ads destination is enabled, per the Owner-approved V1 boundary

## Root cause

The Google tag is initialized before the frontend knows the authenticated Account. The previous implementation tried to add late identity by issuing a second GA4 `config` command. Production BigQuery then showed `account_created` and later events without top-level `user_id`.

Google's late-login contract uses a page-level `set` so subsequent events inherit User-ID, and uses `null` when the user signs out: https://developers.google.com/analytics/devguides/collection/ga4/user-id

## Scope and known boundaries

- refreshed onto `main@405e42090`; the final PR diff remains limited to `tracking.ts` and two unit-test files
- no authentication business-flow, GTM, Consent, Page View, source handoff, backend, or GA4-admin changes
- no email, phone, OTP, token, or chat content is added to analytics
- Owner explicitly prioritizes GA4 Account identity for this V1 even when `NEXT_PUBLIC_GOOGLE_ADS_ENABLED=true`
- because `gtag('set')` is page-global, a same-page Google Ads destination may inherit the Account UID; this is an accepted, disclosed V1 risk requiring human review and later destination isolation
- this PR does not claim that Ads payloads are UID-free
- a pre-existing low-probability race between anonymous bootstrap and extremely fast popup login remains outside this minimal fix
- Draft only; no merge or deployment is requested by this update

## Test plan

- [x] latest-main sync with no semantic conflicts
- [x] repository governance guards
- [x] TypeScript
- [x] focused tracking + auth-manager tests: 129 / 129
- [x] repository matcher gate: 17 files, 402 / 402
- [x] targeted and commit-hook ESLint: 0 errors
- [x] source / test duplication gates
- [x] `git diff --check`
- [x] independent read-only adversarial review: P0-P3 no findings
- [x] explicit regression: Ads enabled still sets GA4 User-ID
- [x] refreshed CI / CodeQL / Codex / Claude review; both AI reviewers request human sign-off only for the disclosed Ads inheritance boundary
- [ ] human review of the disclosed Ads inheritance boundary
- [ ] Staging Network / DebugView: `login_succeeded` has User-ID
- [ ] Staging: later events keep the same User-ID and logout clears it
- [ ] Staging new-account receipt, only after a separately approved fresh alias
- [ ] Production BigQuery / Account present-missing reconciliation


---

## feat(council): report preview overlay and live run progress feedback (#3248)

- **SHA**: `7ae7cc3be843d88ac60fd65065e2d8a51b8c0873`
- **作者**: bill-srp
- **日期**: 2026-08-05T08:16:42Z
- **PR**: #3248

### Commit Message

```
feat(council): report preview overlay and live run progress feedback (#3248)

## Linear
<!-- 无对应 Linear issue：会话内 UX 改进需求 -->

## Summary
- **Report preview overlays the page instead of resizing it.** The
artifacts sidebar on the council page was a flex sibling of the run
content, so opening the complete report squeezed the 900px column. It is
now an absolutely-positioned overlay anchored to the workspace root
(`relative isolate`): the page keeps full width behind it, drag-resize
still caps at 2/3 viewport, and the wrapper only mounts while a preview
is open. Chat's push-aside behavior is unchanged.
- **Live progress feedback while a run is in flight**, three layers:
- Design-system `Spinner` beside the status heading and on actively
working cast rows (`aria-hidden`, `motion-reduce:animate-none`). Hidden
while explicit approval is pending — the run is waiting on the user
then, and motion would promise progress that isn't happening.
- Claude Code-style rotating status phrases (`CouncilStatusPhrase`):
each in-flight state cycles a short phrase set every 60s with a motion
crossfade (text still rotates under reduced motion; only the transition
is dropped). Phrase sets live in `council-state.ts` with index 0 as the
canonical heading, replacing `CouncilStatus`'s private headings map so
static and animated headings cannot drift.
- Elapsed + ETA line (`CouncilStatusElapsed`): "Running for 5m ·
estimated ~12m", flipping to "longer than the ~12m estimate" on overrun.
Suffix-less backend timestamps are parsed as UTC so browser-local clocks
don't skew the elapsed label (Codex-authored fix).
- **Mock backend**: council runs now seed the `mode` field the real
backend always sends (its absence silently disabled the reports fetch
locally), and the done run's report carries a stable-host file link so
the preview flow is reachable with `dev-mock.sh`.

## Test plan
- [x] `CouncilClient.unit.spec.tsx`: preview renders inside the new
`council-artifact-overlay` wrapper and unmounts with it; live-indicator
spec asserts spinner in the status card and on the working member row
only (63 page tests green)
- [x] `CouncilStatusPhrase.unit.spec.tsx` (new): rotation at 60s,
wrap-around, state-change reset, fallback — written RED-first
- [x] `CouncilStatusElapsed.unit.spec.tsx` (new): elapsed/ETA
formatting, overrun copy, sub-minute + hour granularity, ticking,
suffix-less-UTC regression, unparseable input
- [x] `bash scripts/verify-web.sh --no-test` (guards + tsc + eslint)
green
- [x] Browser-verified via Chrome on dev-mock (overlay open/resize/close
with no page reflow; GIF captured) and on a real staging run (phrases
rotating with spinner during synthesizing)
```

### PR Body

## Linear
<!-- 无对应 Linear issue：会话内 UX 改进需求 -->

## Summary
- **Report preview overlays the page instead of resizing it.** The artifacts sidebar on the council page was a flex sibling of the run content, so opening the complete report squeezed the 900px column. It is now an absolutely-positioned overlay anchored to the workspace root (`relative isolate`): the page keeps full width behind it, drag-resize still caps at 2/3 viewport, and the wrapper only mounts while a preview is open. Chat's push-aside behavior is unchanged.
- **Live progress feedback while a run is in flight**, three layers:
  - Design-system `Spinner` beside the status heading and on actively working cast rows (`aria-hidden`, `motion-reduce:animate-none`). Hidden while explicit approval is pending — the run is waiting on the user then, and motion would promise progress that isn't happening.
  - Claude Code-style rotating status phrases (`CouncilStatusPhrase`): each in-flight state cycles a short phrase set every 60s with a motion crossfade (text still rotates under reduced motion; only the transition is dropped). Phrase sets live in `council-state.ts` with index 0 as the canonical heading, replacing `CouncilStatus`'s private headings map so static and animated headings cannot drift.
  - Elapsed + ETA line (`CouncilStatusElapsed`): "Running for 5m · estimated ~12m", flipping to "longer than the ~12m estimate" on overrun. Suffix-less backend timestamps are parsed as UTC so browser-local clocks don't skew the elapsed label (Codex-authored fix).
- **Mock backend**: council runs now seed the `mode` field the real backend always sends (its absence silently disabled the reports fetch locally), and the done run's report carries a stable-host file link so the preview flow is reachable with `dev-mock.sh`.

## Test plan
- [x] `CouncilClient.unit.spec.tsx`: preview renders inside the new `council-artifact-overlay` wrapper and unmounts with it; live-indicator spec asserts spinner in the status card and on the working member row only (63 page tests green)
- [x] `CouncilStatusPhrase.unit.spec.tsx` (new): rotation at 60s, wrap-around, state-change reset, fallback — written RED-first
- [x] `CouncilStatusElapsed.unit.spec.tsx` (new): elapsed/ETA formatting, overrun copy, sub-minute + hour granularity, ticking, suffix-less-UTC regression, unparseable input
- [x] `bash scripts/verify-web.sh --no-test` (guards + tsc + eslint) green
- [x] Browser-verified via Chrome on dev-mock (overlay open/resize/close with no page reflow; GIF captured) and on a real staging run (phrases rotating with spinner during synthesizing)


---

## fix(web): align chat user avatar with profile card (#3247)

- **SHA**: `19841fff6ee205bba69244e9ef9e0df3d045dde8`
- **作者**: ericma-srp
- **日期**: 2026-08-05T07:58:15Z
- **PR**: #3247

### Commit Message

```
fix(web): align chat user avatar with profile card (#3247)

## Summary
- Align chat user-message avatars with the bottom-right profile card
avatar source.
- Reuse the same display-name fallback order and green gradient
presentation when no image is set.
- Keep replay-mode anonymity, reveal the matching fallback on image
errors, and recover when the reactive avatar URL changes.

## Root cause
The chat message avatar only read the Firebase `photoURL` and used a
separate email/phone fallback style. The profile card also reads the
reactive cached `userInfo.photoURL`, prefers the current display name,
and renders a branded gradient fallback, so the same user could appear
with different avatars on one page.

## Test plan
- [x] `vitest run tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx`
— 24 tests passed
- [x] `tsc --noEmit`
- [x] ESLint on the changed component and test
- [ ] `scripts/verify-web.sh` wrapper — local pnpm supply-chain
preflight is blocked by the existing `xlsx@0.20.3` lockfile entry
without integrity metadata; equivalent checks above passed using the
matching existing dependency tree

---------

Co-authored-by: eric <eric.ma@creatibi.com>
```

### PR Body

## Summary
- Align chat user-message avatars with the bottom-right profile card avatar source.
- Reuse the same display-name fallback order and green gradient presentation when no image is set.
- Keep replay-mode anonymity, reveal the matching fallback on image errors, and recover when the reactive avatar URL changes.

## Root cause
The chat message avatar only read the Firebase `photoURL` and used a separate email/phone fallback style. The profile card also reads the reactive cached `userInfo.photoURL`, prefers the current display name, and renders a branded gradient fallback, so the same user could appear with different avatars on one page.

## Test plan
- [x] `vitest run tests/unit/app/chat/OpenClawUserMessage.unit.spec.tsx` — 24 tests passed
- [x] `tsc --noEmit`
- [x] ESLint on the changed component and test
- [ ] `scripts/verify-web.sh` wrapper — local pnpm supply-chain preflight is blocked by the existing `xlsx@0.20.3` lockfile entry without integrity metadata; equivalent checks above passed using the matching existing dependency tree


---

## feat(model-router): Auto model-picker UI handling (#3246)

- **SHA**: `c0dd1e73376b808fa08bfb0a2241d6d5230bbbd5`
- **作者**: siqiao-srp
- **日期**: 2026-08-05T07:35:07Z
- **PR**: #3246

### Commit Message

```
feat(model-router): Auto model-picker UI handling (#3246)

## What

Frontend handling for the **"Auto"** model-router option, **split out of
#3191** so the UI layer lands and is reviewed independently of the
backend `routingMode` work (which is being reworked separately).

## Why split

The full Auto feature has a hard external gate — it only routes once
`zooclaw-extras` #210 is bundled in the openclaw image — and its backend
is under active rework. This PR is the **frontend half** and is **inert
on its own**: nothing surfaces "Auto" until the backend adds it to the
`/models` catalog, so it is safe to merge anytime and de-risks review.

## Changes (`web/app` only)

- **Canonicalize** `auto` <-> `openai/auto` in the model pickers;
**label** `auto` as **"Auto"** (`backend-model-label`).
- **Hide "Auto" where the runtime/flow cannot honor it:**
- engine-runtime chat composer (its save path rejects `auto`) — via
`filterModelsForRuntime` in `useComposerModelState`
- Agent Builder default-model dropdown (submit validator rejects `auto`)
- per-agent picker (`AgentModelSection`) — Auto is a **bot-wide**
toggle, so it is not offered as a *new* per-agent choice; kept visible
only when an agent already reflects global Auto (forward-compatible:
hides entirely once the backend stops reporting per-agent `auto`).
- `autoModelHint` copy in the 7 locales that define an `agentSettings`
block (others fall back to English).

## Not here (the backend PR)

`routingMode` read/write plumbing, `model_routing`, the agent-settings
write path, the `/models` catalog exposure of `auto`, and the enablement
flag. The feature only goes **live** when that PR's flag flips — after
#210 is confirmed in the openclaw image.

## Testing

- `bash scripts/verify-web.sh` on the changed set: tsc + eslint clean,
**vitest 75/75**.
- Covers: engine composer hides Auto / computer shows it; Agent Builder
never offers Auto; per-agent picker does not offer Auto as a new choice
but shows it when already active; `auto` <-> `openai/auto` round-trip +
labeling.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Body

## What

Frontend handling for the **"Auto"** model-router option, **split out of #3191** so the UI layer lands and is reviewed independently of the backend `routingMode` work (which is being reworked separately).

## Why split

The full Auto feature has a hard external gate — it only routes once `zooclaw-extras` #210 is bundled in the openclaw image — and its backend is under active rework. This PR is the **frontend half** and is **inert on its own**: nothing surfaces "Auto" until the backend adds it to the `/models` catalog, so it is safe to merge anytime and de-risks review.

## Changes (`web/app` only)

- **Canonicalize** `auto` <-> `openai/auto` in the model pickers; **label** `auto` as **"Auto"** (`backend-model-label`).
- **Hide "Auto" where the runtime/flow cannot honor it:**
  - engine-runtime chat composer (its save path rejects `auto`) — via `filterModelsForRuntime` in `useComposerModelState`
  - Agent Builder default-model dropdown (submit validator rejects `auto`)
  - per-agent picker (`AgentModelSection`) — Auto is a **bot-wide** toggle, so it is not offered as a *new* per-agent choice; kept visible only when an agent already reflects global Auto (forward-compatible: hides entirely once the backend stops reporting per-agent `auto`).
- `autoModelHint` copy in the 7 locales that define an `agentSettings` block (others fall back to English).

## Not here (the backend PR)

`routingMode` read/write plumbing, `model_routing`, the agent-settings write path, the `/models` catalog exposure of `auto`, and the enablement flag. The feature only goes **live** when that PR's flag flips — after #210 is confirmed in the openclaw image.

## Testing

- `bash scripts/verify-web.sh` on the changed set: tsc + eslint clean, **vitest 75/75**.
- Covers: engine composer hides Auto / computer shows it; Agent Builder never offers Auto; per-agent picker does not offer Auto as a new choice but shows it when already active; `auto` <-> `openai/auto` round-trip + labeling.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## feat(billing): manage Creem subscription cancellation (#3240)

- **SHA**: `c03c9ee32c0a8cc1bd2c0c9c8f732b12de156fd3`
- **作者**: tim-srp
- **日期**: 2026-08-05T07:27:46Z
- **PR**: #3240

### Commit Message

```
feat(billing): manage Creem subscription cancellation (#3240)

## Linear

No dedicated Linear issue was found for this split delivery PR.

## Summary

- route the existing subscription cancel and renew endpoints to Creem
for Creem-owned agreements only
- call Creem's scheduled-cancel and resume APIs with strict typed
response and ownership validation
- process cancel/resume webhook confirmations, recover
provider-success/local-write failures, and reject stale lifecycle
rollback
- acknowledge prior-period cancellation callbacks only when their
provider timestamp is already behind the stored watermark
- serialize Creem cancel/resume mutations with a short agreement-scoped
lease so concurrent opposite actions cannot report success from stale
state
- keep Stripe and Antom services and their existing route branches
unchanged

## Scope

This is the next split PR after the Creem foundation, checkout, webhook,
first-payment, and renewal PRs. It intentionally excludes provider
registries, plan changes, refunds, billing portal work, moderation, and
frontend changes.

## Test plan

- [x] local focused and legacy-provider regression: 441 passed
- [x] a102 devcontainer `bash scripts/verify-py.sh`: Ruff, format,
Pyright, and 8 import contracts passed
- [x] a102 devcontainer focused and legacy-provider regression: 441
passed
- [x] stale prior-period cancellation regression: failed with
`provider_period_mismatch` before the fix, then passed after the minimal
ordering fix
- [x] cancel/resume concurrency regressions: both opposite-operation
races failed before the lease fix, then passed; provider failures also
release the lease
- [x] final a102 Creem and existing subscription-route regression: 366
passed
- [x] Creem Test Mode checkout: $20/month Starter order
`ORD-19FCFD60FE210001` completed successfully
- [x] final Creem Test Mode lifecycle: local/provider `active` →
`canceling`/`scheduled_cancel` → `active`; cancel and resume webhooks
processed without errors and the management lease was released

## Risk controls

- Provider dispatch is additive and only runs for `provider == "creem"`.
- Provider response identity, environment, status, and billing period
must match the local agreement before any local projection.
- Resume cleanup uses an active-status CAS so a concurrent newer cancel
cannot be overwritten.
- Provider `updated_at` is used as the lifecycle watermark so a delayed
cancel event cannot roll back a newer resume.
- The lease is stored only on the existing Creem agreement, is
owner-guarded on release, and expires after 60 seconds; no table or
index was added.
```

### PR Body

## Linear

No dedicated Linear issue was found for this split delivery PR.

## Summary

- route the existing subscription cancel and renew endpoints to Creem for Creem-owned agreements only
- call Creem's scheduled-cancel and resume APIs with strict typed response and ownership validation
- process cancel/resume webhook confirmations, recover provider-success/local-write failures, and reject stale lifecycle rollback
- acknowledge prior-period cancellation callbacks only when their provider timestamp is already behind the stored watermark
- serialize Creem cancel/resume mutations with a short agreement-scoped lease so concurrent opposite actions cannot report success from stale state
- keep Stripe and Antom services and their existing route branches unchanged

## Scope

This is the next split PR after the Creem foundation, checkout, webhook, first-payment, and renewal PRs. It intentionally excludes provider registries, plan changes, refunds, billing portal work, moderation, and frontend changes.

## Test plan

- [x] local focused and legacy-provider regression: 441 passed
- [x] a102 devcontainer `bash scripts/verify-py.sh`: Ruff, format, Pyright, and 8 import contracts passed
- [x] a102 devcontainer focused and legacy-provider regression: 441 passed
- [x] stale prior-period cancellation regression: failed with `provider_period_mismatch` before the fix, then passed after the minimal ordering fix
- [x] cancel/resume concurrency regressions: both opposite-operation races failed before the lease fix, then passed; provider failures also release the lease
- [x] final a102 Creem and existing subscription-route regression: 366 passed
- [x] Creem Test Mode checkout: $20/month Starter order `ORD-19FCFD60FE210001` completed successfully
- [x] final Creem Test Mode lifecycle: local/provider `active` → `canceling`/`scheduled_cancel` → `active`; cancel and resume webhooks processed without errors and the management lease was released

## Risk controls

- Provider dispatch is additive and only runs for `provider == "creem"`.
- Provider response identity, environment, status, and billing period must match the local agreement before any local projection.
- Resume cleanup uses an active-status CAS so a concurrent newer cancel cannot be overwritten.
- Provider `updated_at` is used as the lifecycle watermark so a delayed cancel event cannot roll back a newer resume.
- The lease is stored only on the existing Creem agreement, is owner-guarded on release, and expires after 60 seconds; no table or index was added.


---

## fix(chat): 统一聊天输入框样式与连接器交互 (#3226)

- **SHA**: `3d39daf86a857ce4b1a0c0df2008aa0b4692f9ad`
- **作者**: lynn Zhuang
- **日期**: 2026-08-05T07:20:17Z
- **PR**: #3226

### Commit Message

```
fix(chat): 统一聊天输入框样式与连接器交互 (#3226)

## 改动说明

- 基于共享的 `UnifiedChatComposer`，统一 New Task、Chat Session 和 Agent Builder
中的聊天输入框样式
- 将 Chat Session 的发送按钮图标和输入框卡片样式与 New Task 对齐，并将输入框距页面底部的间距从 48px 减少到
24px
- 点击输入框的添加菜单后，以懒加载的 Skill Store 尺寸弹窗打开 Connectors，并复用 #3220 的响应式布局
- 修复暗色模式下部分模型厂商图标不可见的问题，同时保留不同输入框场景所需的发送按钮样式
- 移除从 #3230 迁入、但与本任务无关的 Agent Builder 布局改动

## 问题原因

New Task、Chat Session 和 Agent Builder
原先分别使用不同的输入框变体和局部样式覆盖，导致输入框高度、底部间距、发送按钮图标与模型展示逐渐不一致。Connectors
入口原先还采用独立页面跳转，没有复用已有的弹窗交互。

## 验证结果

- [x] 共享输入框与 Connector 相关定向测试通过：6 个测试文件，共 140 个测试
- [x] Agent Builder 输入框相关定向测试通过：2 个测试文件，共 45 个测试
- [x] 合并最新 `main` 后运行 `bash
scripts/verify-changed.sh`，TypeScript、代码治理检查与 ESLint 均通过
- [x] 已手动预览 `/new-chat` 和
`/chat/mock-workspace-main/sessions/main-session-1`，确认输入框、添加菜单与
Connectors 入口样式
- [ ] Agent Builder 项目页的浏览器预览受仓库 mock 后端限制：mock 尚未实现最新的
`/agent-builder/entry/*` 接口；相关单元测试与静态检查均已通过

## 预览效果

输入框点击“添加”后，Connector 以弹窗形式打开：

<img width="2570" height="1842" alt="Connector 弹窗预览"
src="https://github.com/user-attachments/assets/09ce9881-879d-464d-8473-d82caa2a2ef7"
/>
```

### PR Body

## 改动说明

- 基于共享的 `UnifiedChatComposer`，统一 New Task、Chat Session 和 Agent Builder 中的聊天输入框样式
- 将 Chat Session 的发送按钮图标和输入框卡片样式与 New Task 对齐，并将输入框距页面底部的间距从 48px 减少到 24px
- 点击输入框的添加菜单后，以懒加载的 Skill Store 尺寸弹窗打开 Connectors，并复用 #3220 的响应式布局
- 修复暗色模式下部分模型厂商图标不可见的问题，同时保留不同输入框场景所需的发送按钮样式
- 移除从 #3230 迁入、但与本任务无关的 Agent Builder 布局改动

## 问题原因

New Task、Chat Session 和 Agent Builder 原先分别使用不同的输入框变体和局部样式覆盖，导致输入框高度、底部间距、发送按钮图标与模型展示逐渐不一致。Connectors 入口原先还采用独立页面跳转，没有复用已有的弹窗交互。

## 验证结果

- [x] 共享输入框与 Connector 相关定向测试通过：6 个测试文件，共 140 个测试
- [x] Agent Builder 输入框相关定向测试通过：2 个测试文件，共 45 个测试
- [x] 合并最新 `main` 后运行 `bash scripts/verify-changed.sh`，TypeScript、代码治理检查与 ESLint 均通过
- [x] 已手动预览 `/new-chat` 和 `/chat/mock-workspace-main/sessions/main-session-1`，确认输入框、添加菜单与 Connectors 入口样式
- [ ] Agent Builder 项目页的浏览器预览受仓库 mock 后端限制：mock 尚未实现最新的 `/agent-builder/entry/*` 接口；相关单元测试与静态检查均已通过

## 预览效果

输入框点击“添加”后，Connector 以弹窗形式打开：

<img width="2570" height="1842" alt="Connector 弹窗预览" src="https://github.com/user-attachments/assets/09ce9881-879d-464d-8473-d82caa2a2ef7" />



---

## fix(agent-builder): stabilize builder test layout (#3230)

- **SHA**: `405e420909ee0b28a3a31dfac3c6e9f2eccc3b0c`
- **作者**: lynn Zhuang
- **日期**: 2026-08-05T06:14:58Z
- **PR**: #3230

### Commit Message

```
fix(agent-builder): stabilize builder test layout (#3230)

## Summary
- keep the Agent Builder chat and test preview side by side in an
equal-width, 1120px-minimum workspace
- compact the model selector while the test panel is open so header
controls do not crowd the split view
- hide the Auto review control row while preserving automatic feedback
and the manual fallback after failures

## Root cause
The workspace switched to a vertical stack below the desktop breakpoint
and used asymmetric pane widths above it. The model status and Auto
review row also consumed scarce space, which made the builder chat
dominate while the test preview appeared squeezed or displaced.

## Test plan
- [x] `bash scripts/verify-web.sh <changed Agent Builder files>`
- [x] `bash scripts/verify-changed.sh`
- [x] verified the local preview uses a 1120px canvas with two 560px
panes sharing the same top position
```

### PR Body

## Summary
- keep the Agent Builder chat and test preview side by side in an equal-width, 1120px-minimum workspace
- compact the model selector while the test panel is open so header controls do not crowd the split view
- hide the Auto review control row while preserving automatic feedback and the manual fallback after failures

## Root cause
The workspace switched to a vertical stack below the desktop breakpoint and used asymmetric pane widths above it. The model status and Auto review row also consumed scarce space, which made the builder chat dominate while the test preview appeared squeezed or displaced.

## Test plan
- [x] `bash scripts/verify-web.sh <changed Agent Builder files>`
- [x] `bash scripts/verify-changed.sh`
- [x] verified the local preview uses a 1120px canvas with two 560px panes sharing the same top position


---

## fix(tracking): restore generic Tips attribution in Chat (#3245)

- **SHA**: `2388adfc1672e3668fde16864387dec35c17e488`
- **作者**: Mori-srp
- **日期**: 2026-08-05T06:03:35Z
- **PR**: #3245

### Commit Message

```
fix(tracking): restore generic Tips attribution in Chat (#3245)

## Supersedes

This PR transparently supersedes #3223. The production code and tests
are unchanged and point to the same reviewed commit
(`13267fb4dc04927802e28aaea56cf04b88806dd7`). A replacement PR is used
so Codex and Claude can perform a full review against the final,
corrected product contract instead of the stale PR-description snapshot
that triggered the previous `need-human-review` verdicts.

Paired producer PR SerendipityOneInc/zooclaw-tips#64 has been merged and
deployed to Production.

## Owner decision

V1 intentionally accepts analytics-only attribution handoffs from any
current or future same-origin `/tips` or `/tips/**` page. No `source`,
specialist, or fixed-page allowlist is required. KOL, SEM, and EDM
campaigns can land on Compare, Cases, User Guide, Prompt Gallery, and
future Tips pages, so adding a consumer allowlist entry for every page
would create avoidable attribution loss.

This client-side attribution signal has the same diagnostic trust
boundary as ordinary URL UTM parameters. A browser user can alter their
own attribution, but the signal is not used for authentication,
authorization, billing, permissions, or Account identity.

## Summary

- consume the generic attribution-only envelope produced by ZooClaw Tips
- require `version=1`, `producer=zooclaw-tips`, exact `lcid` /
`landing_session_id` match, a same-origin `/tips` or `/tips/**` landing
URL, and valid 24-hour timestamps
- re-sanitize all URL, UTM, click-ID, and referrer fields before writing
the existing registration attribution snapshot
- keep current Chat URL UTM authoritative and prevent an untagged Tips
handoff from erasing an existing campaign
- use the envelope click time for precedence, so an older valid
acquisition can still replace a newer Direct snapshot when the user
clicks Chat later
- consume the matching envelope after adoption without changing
authentication, onboarding, specialist delivery, or backend registration
behavior

## Root cause

Tips and Chat use different tabs. A Chat-side session snapshot could
therefore replace or miss the actual acquisition that happened on Tips.
The earlier candidate tied attribution to two exact specialist pages,
which did not cover Compare, User Guide, Cases, Prompt Gallery, or
future campaign landing pages.

The final contract is analytics-only. It does not read or mutate
specialist hire/switch, prompt delivery, onboarding, authentication,
backend registration, or Account identity state.

## Scope and known boundaries

- final net diff is limited to `web/app/src/lib/attribution-snapshot.ts`
and its unit test
- no auth-state-machine, onboarding, GTM, Ads, Page View producer,
backend, or Account DB changes
- current raw `page_location` behavior remains unchanged
- client-side attribution is diagnostic analytics, not authenticated
provenance
- only same-origin `/tips` and `/tips/**` are accepted; cross-origin
Preview/Staging to Production is intentionally rejected
- current single-slot envelope is fail-closed under simultaneous clicks:
the older tab can lose attribution but cannot receive the newer tab's
source
- ready for automated and human review; no deployment or merge is
requested by creating this PR

## Test plan

- [x] related Vitest files: 103 / 103
- [x] envelope schema, producer, ID, origin, path, TTL, future-skew,
replay, and compare-before-delete cases
- [x] arbitrary nested same-origin Tips pages accepted without consumer
allowlist updates
- [x] non-Tips same-origin paths and external origins rejected
- [x] organic/no-UTM, current URL override, weak-source preservation,
and sensitive-field re-sanitization
- [x] old acquisition T1 + newer Direct T2 + latest CTA T3 precedence
regression
- [x] TypeScript
- [x] focused and pre-push ESLint
- [x] repository governance / changed-surface pre-push checks
- [x] PR size gate: 561 / 3000 lines
- [x] paired Tips PR #64 merged and deployed
- [ ] same-origin Production canary: Tips CTA -> Chat -> registration ->
GA4 / BigQuery receipt
```

### PR Body

## Supersedes

This PR transparently supersedes #3223. The production code and tests are unchanged and point to the same reviewed commit (`13267fb4dc04927802e28aaea56cf04b88806dd7`). A replacement PR is used so Codex and Claude can perform a full review against the final, corrected product contract instead of the stale PR-description snapshot that triggered the previous `need-human-review` verdicts.

Paired producer PR SerendipityOneInc/zooclaw-tips#64 has been merged and deployed to Production.

## Owner decision

V1 intentionally accepts analytics-only attribution handoffs from any current or future same-origin `/tips` or `/tips/**` page. No `source`, specialist, or fixed-page allowlist is required. KOL, SEM, and EDM campaigns can land on Compare, Cases, User Guide, Prompt Gallery, and future Tips pages, so adding a consumer allowlist entry for every page would create avoidable attribution loss.

This client-side attribution signal has the same diagnostic trust boundary as ordinary URL UTM parameters. A browser user can alter their own attribution, but the signal is not used for authentication, authorization, billing, permissions, or Account identity.

## Summary

- consume the generic attribution-only envelope produced by ZooClaw Tips
- require `version=1`, `producer=zooclaw-tips`, exact `lcid` / `landing_session_id` match, a same-origin `/tips` or `/tips/**` landing URL, and valid 24-hour timestamps
- re-sanitize all URL, UTM, click-ID, and referrer fields before writing the existing registration attribution snapshot
- keep current Chat URL UTM authoritative and prevent an untagged Tips handoff from erasing an existing campaign
- use the envelope click time for precedence, so an older valid acquisition can still replace a newer Direct snapshot when the user clicks Chat later
- consume the matching envelope after adoption without changing authentication, onboarding, specialist delivery, or backend registration behavior

## Root cause

Tips and Chat use different tabs. A Chat-side session snapshot could therefore replace or miss the actual acquisition that happened on Tips. The earlier candidate tied attribution to two exact specialist pages, which did not cover Compare, User Guide, Cases, Prompt Gallery, or future campaign landing pages.

The final contract is analytics-only. It does not read or mutate specialist hire/switch, prompt delivery, onboarding, authentication, backend registration, or Account identity state.

## Scope and known boundaries

- final net diff is limited to `web/app/src/lib/attribution-snapshot.ts` and its unit test
- no auth-state-machine, onboarding, GTM, Ads, Page View producer, backend, or Account DB changes
- current raw `page_location` behavior remains unchanged
- client-side attribution is diagnostic analytics, not authenticated provenance
- only same-origin `/tips` and `/tips/**` are accepted; cross-origin Preview/Staging to Production is intentionally rejected
- current single-slot envelope is fail-closed under simultaneous clicks: the older tab can lose attribution but cannot receive the newer tab's source
- ready for automated and human review; no deployment or merge is requested by creating this PR

## Test plan

- [x] related Vitest files: 103 / 103
- [x] envelope schema, producer, ID, origin, path, TTL, future-skew, replay, and compare-before-delete cases
- [x] arbitrary nested same-origin Tips pages accepted without consumer allowlist updates
- [x] non-Tips same-origin paths and external origins rejected
- [x] organic/no-UTM, current URL override, weak-source preservation, and sensitive-field re-sanitization
- [x] old acquisition T1 + newer Direct T2 + latest CTA T3 precedence regression
- [x] TypeScript
- [x] focused and pre-push ESLint
- [x] repository governance / changed-surface pre-push checks
- [x] PR size gate: 561 / 3000 lines
- [x] paired Tips PR #64 merged and deployed
- [ ] same-origin Production canary: Tips CTA -> Chat -> registration -> GA4 / BigQuery receipt


---

## fix(web): agents-manager fire click propagation and start-chat routing (#3244)

- **SHA**: `60aee159390d8031d9c0273412e4d0221a81c92b`
- **作者**: bill-srp
- **日期**: 2026-08-05T05:59:26Z
- **PR**: #3244

### Commit Message

```
fix(web): agents-manager fire click propagation and start-chat routing (#3244)

## Summary
Two agents-manager fixes:
1. **Fire menu click no longer triggers the card click.** Firing an
agent opened the confirm-fire modal *and* navigated to
`/agents-manager/{packId}` at the same time. Fixed with
`onClick={(event) => event.stopPropagation()}` on the card dropdown's
`DropdownMenuContent`.
2. **Start Chat CTAs now route to the New Task launcher.** After
installing an agent, Start Chat (hire-success modal, card Chat button,
detail page, publish flow, post-update session reset) landed on
`/chat?workspace_id=` — the workspace's "Session History" DM, which is
empty for a fresh install and is exactly the surface the sidenav hides
as a "navigation dead end" for session-less agents
(`SideNavAgentSessions.tsx`). All of these now go through
`buildWorkspaceNewChatHref` (`/new-chat?workspace_id=`), landing on the
New Task launcher pre-selected with the agent.

## Root cause
**Fix 1:** The whole agent card is a `LocaleLink` (Next.js `<Link>`),
and the Fire action is a Radix `DropdownMenuItem` nested inside it. The
existing `event.preventDefault()` in `onSelect` only cancels Radix's
menu auto-close — it does nothing to the underlying click. Although
`DropdownMenuContent` renders in a portal (native DOM bubbling never
reaches the anchor), **React synthetic events bubble through the JSX
tree, not the DOM tree**: the item click propagated up to the Link's
navigation `onClick` and Next.js client-navigated. The fix deliberately
uses `stopPropagation()` only, **without** `preventDefault()`: Radix
dispatches the item's select event from a composed click handler that
bails when `defaultPrevented` is set, so preventing default at the
content level would suppress `onSelect` and make Fire a no-op.

**Fix 2:** `openChat`/`pushWorkspaceChat` used `buildWorkspaceChatHref`,
which targets the engine agent's Mattermost DM surface ("Session
History"). For a freshly installed agent that surface has zero sessions;
the sidenav model already treats it as a dead end and offers "New Task"
instead. Per owner decision (New Task everywhere), all agents-manager
start-chat entry points now route to the launcher regardless of runtime.

## Test plan
- [x] Fix 1 regression test: `fire menu click requests fire without
bubbling to the card link` — mocked `LocaleLink` carries a click spy
standing in for Next Link's navigation handler; failed before the fix
(spy called), passes after, and asserts `onRequestFire` still fires
- [x] Fix 2: flipped all 15 destination assertions across the 4
agents-manager specs from `/chat?workspace_id=` to
`/new-chat?workspace_id=` first (RED: exactly those 15 failed), then
switched the 4 call sites (GREEN: 176/176)
- [x] `bash scripts/verify-web.sh` on changed files: guards + `tsc` +
`vitest` + `eslint` all green
- [x] Browser-validated against the mock stack (`scripts/dev-mock.sh`,
install handlers mutate real state): install → hire-success "Start Chat"
lands on `/new-chat?workspace_id=workspace_mock_4`; hired card "Chat"
lands on `/new-chat?workspace_id=workspace_mock_1` with the New Task
composer pre-selected to the agent; no stray card navigation
```

### PR Body

## Summary
Two agents-manager fixes:
1. **Fire menu click no longer triggers the card click.** Firing an agent opened the confirm-fire modal *and* navigated to `/agents-manager/{packId}` at the same time. Fixed with `onClick={(event) => event.stopPropagation()}` on the card dropdown's `DropdownMenuContent`.
2. **Start Chat CTAs now route to the New Task launcher.** After installing an agent, Start Chat (hire-success modal, card Chat button, detail page, publish flow, post-update session reset) landed on `/chat?workspace_id=` — the workspace's "Session History" DM, which is empty for a fresh install and is exactly the surface the sidenav hides as a "navigation dead end" for session-less agents (`SideNavAgentSessions.tsx`). All of these now go through `buildWorkspaceNewChatHref` (`/new-chat?workspace_id=`), landing on the New Task launcher pre-selected with the agent.

## Root cause
**Fix 1:** The whole agent card is a `LocaleLink` (Next.js `<Link>`), and the Fire action is a Radix `DropdownMenuItem` nested inside it. The existing `event.preventDefault()` in `onSelect` only cancels Radix's menu auto-close — it does nothing to the underlying click. Although `DropdownMenuContent` renders in a portal (native DOM bubbling never reaches the anchor), **React synthetic events bubble through the JSX tree, not the DOM tree**: the item click propagated up to the Link's navigation `onClick` and Next.js client-navigated. The fix deliberately uses `stopPropagation()` only, **without** `preventDefault()`: Radix dispatches the item's select event from a composed click handler that bails when `defaultPrevented` is set, so preventing default at the content level would suppress `onSelect` and make Fire a no-op.

**Fix 2:** `openChat`/`pushWorkspaceChat` used `buildWorkspaceChatHref`, which targets the engine agent's Mattermost DM surface ("Session History"). For a freshly installed agent that surface has zero sessions; the sidenav model already treats it as a dead end and offers "New Task" instead. Per owner decision (New Task everywhere), all agents-manager start-chat entry points now route to the launcher regardless of runtime.

## Test plan
- [x] Fix 1 regression test: `fire menu click requests fire without bubbling to the card link` — mocked `LocaleLink` carries a click spy standing in for Next Link's navigation handler; failed before the fix (spy called), passes after, and asserts `onRequestFire` still fires
- [x] Fix 2: flipped all 15 destination assertions across the 4 agents-manager specs from `/chat?workspace_id=` to `/new-chat?workspace_id=` first (RED: exactly those 15 failed), then switched the 4 call sites (GREEN: 176/176)
- [x] `bash scripts/verify-web.sh` on changed files: guards + `tsc` + `vitest` + `eslint` all green
- [x] Browser-validated against the mock stack (`scripts/dev-mock.sh`, install handlers mutate real state): install → hire-success "Start Chat" lands on `/new-chat?workspace_id=workspace_mock_4`; hired card "Chat" lands on `/new-chat?workspace_id=workspace_mock_1` with the New Task composer pre-selected to the agent; no stray card navigation


---

## fix(agent-builder): prevent same-page workspace self-lock (#3243)

- **SHA**: `0dd04f7454c7dfe16cf84f0babef52ec459c11fc`
- **作者**: kaka-srp
- **日期**: 2026-08-05T04:13:45Z
- **PR**: #3243

### Commit Message

```
fix(agent-builder): prevent same-page workspace self-lock (#3243)

## Summary
- Reuse the retained V1 workspace coordinator when the same `uid` /
computer / project / session remounts in one page.
- Carry an in-flight activation promise and its error state across that
handoff, avoiding duplicate Web Lock and activation requests.
- Add regression coverage for remounts during both a retained Agent turn
and a pending project activation.

This is intentionally limited to the retiring V1 Agent Builder hook. It
does not change V2, backend APIs, or cross-project workspace
exclusivity.

## Root cause
V1 holds a computer-scoped Web Lock while a workspace operation is still
active. If the React workspace hook unmounted and remounted during that
lifetime, the old hook retained the lock but the new hook created a
separate coordinator and requested the same lock. After five seconds it
incorrectly showed the shared-workspace waiting state even though no
other ZooClaw page was open.

The same self-contention could happen while project activation was
pending because aborting the lock request does not release a lock that
has already been granted. The coordinator is now retained before
activation starts and can be adopted only by the exact same page
context.

## Test plan
- [x] `pnpm exec vitest run
tests/unit/app/agent-builder-workspace-activation.unit.spec.tsx` (10/10)
- [x] `bash scripts/verify-local.sh --web-static ...` (TypeScript,
targeted tests, ESLint, governance guards)
- [x] `bash scripts/verify-changed.sh`
- [x] Independent read-only review: no findings; related tests 70/70
```

### PR Body

## Summary
- Reuse the retained V1 workspace coordinator when the same `uid` / computer / project / session remounts in one page.
- Carry an in-flight activation promise and its error state across that handoff, avoiding duplicate Web Lock and activation requests.
- Add regression coverage for remounts during both a retained Agent turn and a pending project activation.

This is intentionally limited to the retiring V1 Agent Builder hook. It does not change V2, backend APIs, or cross-project workspace exclusivity.

## Root cause
V1 holds a computer-scoped Web Lock while a workspace operation is still active. If the React workspace hook unmounted and remounted during that lifetime, the old hook retained the lock but the new hook created a separate coordinator and requested the same lock. After five seconds it incorrectly showed the shared-workspace waiting state even though no other ZooClaw page was open.

The same self-contention could happen while project activation was pending because aborting the lock request does not release a lock that has already been granted. The coordinator is now retained before activation starts and can be adopted only by the exact same page context.

## Test plan
- [x] `pnpm exec vitest run tests/unit/app/agent-builder-workspace-activation.unit.spec.tsx` (10/10)
- [x] `bash scripts/verify-local.sh --web-static ...` (TypeScript, targeted tests, ESLint, governance guards)
- [x] `bash scripts/verify-changed.sh`
- [x] Independent read-only review: no findings; related tests 70/70


---

## feat(skills): add review and ZooClaw diagnostics (#3242)

- **SHA**: `336d810c87633c2efaed2034f8846ea5ccb3e050`
- **作者**: kaka-srp
- **日期**: 2026-08-05T04:10:30Z
- **PR**: #3242

### Commit Message

```
feat(skills): add review and ZooClaw diagnostics (#3242)

## Linear

N/A

## Summary

- Add a high-signal `code-review` skill that reviews design and scope,
implementation completeness and reliability, and regressions or side
effects while emitting only evidence-backed actionable findings.
- Add the read-only `zooclaw-diagnose` handbook and toolkit: bounded
evidence workflows, fixed parameterized SQL, redacted collectors,
failure decision trees, and deterministic tests.
- Update the `pr` skill to inspect CI, code-scanning, PR review, and
inline feedback; verify whether each finding is real and worth fixing
before changing code.
- Add the shared Claude skill projections and the ZooClaw diagnostic
design spec.
- Harden ZooClaw collection so `textPayload`, raw request/response
snapshots, memory, tool arguments, and unknown `jsonPayload` fields
cannot leak user content while diagnostic metadata remains available.
- Keep the Nomad token out of `curl` process arguments and redact
camel-case `apiKey` fields in query output.

## Automated review adjudication

- Accepted the Nomad argv finding as real and worth fixing; the
documented request now supplies the header through curl's stdin
configuration.
- Rejected the claim that the current config query emits arbitrary
plugin objects: the engine contract validates `rendered.plugins.enabled`
as `string[]`. Added a no-capability-loss defense anyway: SQL now
retains only string array elements, so current output is unchanged while
future schema drift cannot expose objects.
- Accepted the narrower defense-in-depth issue exposed by that finding:
the query sanitizer now redacts `apiKey`, `api_key`, `api-key`, and
`authorization`, with regression tests.
- Accepted Claude's narrower HTTP-error finding without dropping
diagnostic branches: free-text `message`/`detail` is omitted, while
stable `type`/`code`, bounded error signals, and length metadata remain
available. This path runs only after an HTTP error.
- Accepted Claude's collector-normalization follow-up: the collector now
strips all non-alphanumeric key separators before secret matching,
closing the `api-key` sibling gap without changing collected fields or
remote work.

## Test plan

- [x] Validate all three skills with `quick_validate.py`.
- [x] Run `scripts/sync-agent-skills.sh --check` and
`scripts/sync-agent-skills.test.sh`.
- [x] Run 14 deterministic ZooClaw diagnostic unit tests.
- [x] Run Ruff check and format check over the ZooClaw Python scripts
and tests.
- [x] Compile all ZooClaw Python scripts and tests.
- [x] Exercise CLI help plus staging and production dry-runs for the
collector and fixed query runners.
- [x] Run `scripts/verify-changed.sh`.
- [x] Verify referenced engine and ACS schemas, routes, deployment
names, and source paths against their current `origin/main` trees.

## Size override

The combined change is 3,658 counted lines versus the 3,000-line default
budget. Most of the diff is the requested self-contained
`zooclaw-diagnose` handbook, redacted collector, fixed SQL catalog, and
tests; splitting those pieces would leave the skill incomplete. This PR
therefore requires the `size-override` label.
```

### PR Body

## Linear

N/A

## Summary

- Add a high-signal `code-review` skill that reviews design and scope, implementation completeness and reliability, and regressions or side effects while emitting only evidence-backed actionable findings.
- Add the read-only `zooclaw-diagnose` handbook and toolkit: bounded evidence workflows, fixed parameterized SQL, redacted collectors, failure decision trees, and deterministic tests.
- Update the `pr` skill to inspect CI, code-scanning, PR review, and inline feedback; verify whether each finding is real and worth fixing before changing code.
- Add the shared Claude skill projections and the ZooClaw diagnostic design spec.
- Harden ZooClaw collection so `textPayload`, raw request/response snapshots, memory, tool arguments, and unknown `jsonPayload` fields cannot leak user content while diagnostic metadata remains available.
- Keep the Nomad token out of `curl` process arguments and redact camel-case `apiKey` fields in query output.

## Automated review adjudication

- Accepted the Nomad argv finding as real and worth fixing; the documented request now supplies the header through curl's stdin configuration.
- Rejected the claim that the current config query emits arbitrary plugin objects: the engine contract validates `rendered.plugins.enabled` as `string[]`. Added a no-capability-loss defense anyway: SQL now retains only string array elements, so current output is unchanged while future schema drift cannot expose objects.
- Accepted the narrower defense-in-depth issue exposed by that finding: the query sanitizer now redacts `apiKey`, `api_key`, `api-key`, and `authorization`, with regression tests.
- Accepted Claude's narrower HTTP-error finding without dropping diagnostic branches: free-text `message`/`detail` is omitted, while stable `type`/`code`, bounded error signals, and length metadata remain available. This path runs only after an HTTP error.
- Accepted Claude's collector-normalization follow-up: the collector now strips all non-alphanumeric key separators before secret matching, closing the `api-key` sibling gap without changing collected fields or remote work.

## Test plan

- [x] Validate all three skills with `quick_validate.py`.
- [x] Run `scripts/sync-agent-skills.sh --check` and `scripts/sync-agent-skills.test.sh`.
- [x] Run 14 deterministic ZooClaw diagnostic unit tests.
- [x] Run Ruff check and format check over the ZooClaw Python scripts and tests.
- [x] Compile all ZooClaw Python scripts and tests.
- [x] Exercise CLI help plus staging and production dry-runs for the collector and fixed query runners.
- [x] Run `scripts/verify-changed.sh`.
- [x] Verify referenced engine and ACS schemas, routes, deployment names, and source paths against their current `origin/main` trees.

## Size override

The combined change is 3,658 counted lines versus the 3,000-line default budget. Most of the diff is the requested self-contained `zooclaw-diagnose` handbook, redacted collector, fixed SQL catalog, and tests; splitting those pieces would leave the skill incomplete. This PR therefore requires the `size-override` label.


---

## feat(web): run the vertical-pack installer for engine-mode users (#3241)

- **SHA**: `aa0294a8bf722265e57c99ad2bba2b8b64c6a61d`
- **作者**: bill-srp
- **日期**: 2026-08-05T03:09:24Z
- **PR**: #3241

### Commit Message

```
feat(web): run the vertical-pack installer for engine-mode users (#3241)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven:
docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md, Phase
4 (frontend leg) -->

## Summary
Frontend leg of Phase 4 (backend = #3235, merged): the vertical-pack
package auto-installer works for engine-mode users with no computer.

- `VerticalPackPackageInstaller`: enables on v1 init readiness **or**
engine mode (uid-scoped `botStatus === 'engine'` from the onboarding
store — the Phase 2 signal).
- `useVerticalPackPackageInstaller` engine branch: computer
lookup/status queries fully disabled; package query enables without a
computer; once-per-session install key scoped to `'engine'`; pre-install
dedup reads the unified agent list across **all runtimes** (mirroring
the backend's cross-runtime dedup); and because #3235 installs + starts
engine agents inline, the engine path skips the 5-minute
`waitForAgentWorkspaceStatus` polling entirely — it just invalidates the
agent cache when the install call returns.
- v1 computer path byte-for-byte unchanged (resolution refactored into a
pure helper, same semantics, existing tests still pass).

## Test plan
- [x] TDD (RED first): engine-mode user with no computer → package
fetched, missing packs installed, no computer queries, cache
invalidated, no polling; cross-runtime dedup skips engine-held packs;
uid-scoped component enablement; v1 path unchanged (15 targeted tests
green)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc +
vitest + eslint — green
- [x] `pnpm lint:imports`: 0 errors
- [ ] CI (`web-quality` + `web-build-check`)
```

### PR Body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven: docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md, Phase 4 (frontend leg) -->

## Summary
Frontend leg of Phase 4 (backend = #3235, merged): the vertical-pack package auto-installer works for engine-mode users with no computer.

- `VerticalPackPackageInstaller`: enables on v1 init readiness **or** engine mode (uid-scoped `botStatus === 'engine'` from the onboarding store — the Phase 2 signal).
- `useVerticalPackPackageInstaller` engine branch: computer lookup/status queries fully disabled; package query enables without a computer; once-per-session install key scoped to `'engine'`; pre-install dedup reads the unified agent list across **all runtimes** (mirroring the backend's cross-runtime dedup); and because #3235 installs + starts engine agents inline, the engine path skips the 5-minute `waitForAgentWorkspaceStatus` polling entirely — it just invalidates the agent cache when the install call returns.
- v1 computer path byte-for-byte unchanged (resolution refactored into a pure helper, same semantics, existing tests still pass).

## Test plan
- [x] TDD (RED first): engine-mode user with no computer → package fetched, missing packs installed, no computer queries, cache invalidated, no polling; cross-runtime dedup skips engine-held packs; uid-scoped component enablement; v1 path unchanged (15 targeted tests green)
- [x] Full local gate `bash scripts/verify-web.sh`: guards + tsc + vitest + eslint — green
- [x] `pnpm lint:imports`: 0 errors
- [ ] CI (`web-quality` + `web-build-check`)


---

## fix(agent-builder): converge v2 runtime and models (#3239)

- **SHA**: `aa83b9d3ce93607b076868304b7816890cfa189e`
- **作者**: kaka-srp
- **日期**: 2026-08-05T02:56:04Z
- **PR**: #3239

### Commit Message

```
fix(agent-builder): converge v2 runtime and models (#3239)

## Summary

- [x] expose the complete Agent Builder v2 model set in the composer and
make pending model application retryable
- [x] converge the hidden Agent Studio Agent on the current runtime
asset and exact Engine Environment pin
- [x] move slow Agent Studio setup convergence to the existing
background setup owner
- [x] keep V1 Builder, ordinary Agent Environment updates, and Pack Test
model behavior unchanged
- [x] add the cross-repository design and release order

## Root cause

Three staging failures had separate causes:

1. The v2 composer intersected the Builder model list with the generic
chat catalog, so Builder-only model IDs appeared unavailable and a
pending desired model could not be retried reliably.
2. Agent Studio readiness compared submission provenance but did not
require the installed Agent's runtime asset and resolved Environment to
match the latest Pack asset. The Engine Environment lock then prevented
convergence.
3. Builder activation could synchronously wait for the long Agent Studio
update path instead of allowing the single background setup owner to
converge and report state.

Companion changes:

- Engine locked Environment lifecycle:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/616
- Agent Channel Service terminal Artifact projection:
https://github.com/SerendipityOneInc/agent-channel-service/pull/59

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 289 focused backend tests passed with `AGENTS_V2_ENABLED=false` so
the legacy test matrix uses its intended gate state
- [x] `bash scripts/verify-web.sh <changed paths>`: TypeScript, 399 unit
tests, and ESLint passed
- [x] pre-commit and pre-push changed-surface gates passed
- [x] file-length, complexity, import-contract, and pyright hooks passed

## Deployment order

1. Engine
2. Agent Channel Service
3. ECAP backend
4. ECAP web
```

### PR Body

## Summary

- [x] expose the complete Agent Builder v2 model set in the composer and make pending model application retryable
- [x] converge the hidden Agent Studio Agent on the current runtime asset and exact Engine Environment pin
- [x] move slow Agent Studio setup convergence to the existing background setup owner
- [x] keep V1 Builder, ordinary Agent Environment updates, and Pack Test model behavior unchanged
- [x] add the cross-repository design and release order

## Root cause

Three staging failures had separate causes:

1. The v2 composer intersected the Builder model list with the generic chat catalog, so Builder-only model IDs appeared unavailable and a pending desired model could not be retried reliably.
2. Agent Studio readiness compared submission provenance but did not require the installed Agent's runtime asset and resolved Environment to match the latest Pack asset. The Engine Environment lock then prevented convergence.
3. Builder activation could synchronously wait for the long Agent Studio update path instead of allowing the single background setup owner to converge and report state.

Companion changes:

- Engine locked Environment lifecycle: https://github.com/SerendipityOneInc/zooclaw-engine/pull/616
- Agent Channel Service terminal Artifact projection: https://github.com/SerendipityOneInc/agent-channel-service/pull/59

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 289 focused backend tests passed with `AGENTS_V2_ENABLED=false` so the legacy test matrix uses its intended gate state
- [x] `bash scripts/verify-web.sh <changed paths>`: TypeScript, 399 unit tests, and ESLint passed
- [x] pre-commit and pre-push changed-surface gates passed
- [x] file-length, complexity, import-contract, and pyright hooks passed

## Deployment order

1. Engine
2. Agent Channel Service
3. ECAP backend
4. ECAP web


---

## feat(vertical-pack): install package agents on the engine runtime for v2-eligible users (#3235)

- **SHA**: `4ecfcff7631b4bca135f924cce4da7e99d917911`
- **作者**: bill-srp
- **日期**: 2026-08-05T02:50:18Z
- **PR**: #3235

### Commit Message

```
feat(vertical-pack): install package agents on the engine runtime for v2-eligible users (#3235)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven:
docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md, Phase
4 -->

## Summary
Phase 4 (backend leg) of the v2 onboarding spec: vertical-pack package
installs support the engine runtime. Per the runtime-agnostic API rule
this stays one endpoint that branches internally — no engine-specific
route.

- `POST /vertical-pack/package/{id}/install` branches on
`agents_v2_access.get_agents_v2_eligibility` (the same signal as
`/agents/install-capability`). Eligible users: no bot/computer lookup;
each official pack in the package is resolved with the same 404
semantics as the computer leg, cross-runtime deduped (skip when any
non-reinstallable workspace holds the pack — reinstallable =
deleted/install_failed/uninstalled, matching the install BFF), and
installed as an engine agent in a FastAPI background task that installs
**and starts** each agent with per-pack failure isolation. Non-eligible
users: the computer leg is byte-for-byte unchanged.
- Response contract unchanged: `results: [{agent_id: display_id, status:
installing|skipped}]`.
- The cross-runtime workspace lookup is a new method on the existing
`agent_workspace_repo` (no new repo module, no import-linter contract
churn).

The frontend leg (installer enabled in engine mode, unified-list dedup,
no computer queries) follows in a separate web PR.

## Test plan
- [x] TDD (RED first): engine-eligible install starts engine installs
with no bot lookup; cross-runtime dedup skips held packs; non-eligible
path unchanged; unknown pack 404s (`test_vertical_pack_plans_routes.py`,
`test_agent_multi_install_service.py`)
- [x] Host gate: ruff check + ruff format --check + pyright (0 errors) +
import-linter (8/8 contracts kept)
- [x] `pytest tests/unit` full tier: 7,761 passed; only pre-existing
local-env failures in `test_ci_lint_deptry.py` (reproduce on clean main,
deptry binary/local setup — CI runs deptry with its own toolchain)
- [ ] CI `claw-interface-quality` (authoritative: pytest + Mongo + 90%
coverage gate — no local Mongo available this session)
```

### PR Body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- spec-driven: docs/superpowers/specs/2026-08-04-v2-onboarding-engine-install.md, Phase 4 -->

## Summary
Phase 4 (backend leg) of the v2 onboarding spec: vertical-pack package installs support the engine runtime. Per the runtime-agnostic API rule this stays one endpoint that branches internally — no engine-specific route.

- `POST /vertical-pack/package/{id}/install` branches on `agents_v2_access.get_agents_v2_eligibility` (the same signal as `/agents/install-capability`). Eligible users: no bot/computer lookup; each official pack in the package is resolved with the same 404 semantics as the computer leg, cross-runtime deduped (skip when any non-reinstallable workspace holds the pack — reinstallable = deleted/install_failed/uninstalled, matching the install BFF), and installed as an engine agent in a FastAPI background task that installs **and starts** each agent with per-pack failure isolation. Non-eligible users: the computer leg is byte-for-byte unchanged.
- Response contract unchanged: `results: [{agent_id: display_id, status: installing|skipped}]`.
- The cross-runtime workspace lookup is a new method on the existing `agent_workspace_repo` (no new repo module, no import-linter contract churn).

The frontend leg (installer enabled in engine mode, unified-list dedup, no computer queries) follows in a separate web PR.

## Test plan
- [x] TDD (RED first): engine-eligible install starts engine installs with no bot lookup; cross-runtime dedup skips held packs; non-eligible path unchanged; unknown pack 404s (`test_vertical_pack_plans_routes.py`, `test_agent_multi_install_service.py`)
- [x] Host gate: ruff check + ruff format --check + pyright (0 errors) + import-linter (8/8 contracts kept)
- [x] `pytest tests/unit` full tier: 7,761 passed; only pre-existing local-env failures in `test_ci_lint_deptry.py` (reproduce on clean main, deptry binary/local setup — CI runs deptry with its own toolchain)
- [ ] CI `claw-interface-quality` (authoritative: pytest + Mongo + 90% coverage gate — no local Mongo available this session)


---

## feat(billing): settle Creem subscription renewals (#3238)

- **SHA**: `cc92bdf9879082dcf3842a8dece48e4581395869`
- **作者**: tim-srp
- **日期**: 2026-08-05T01:26:45Z
- **PR**: #3238

### Commit Message

```
feat(billing): settle Creem subscription renewals (#3238)
```

### PR Body

## Linear

No Linear issue was created for this incremental PR.

## Summary

- settle standard paid Creem subscription renewals after the initial Card checkout payment
- create one deterministic Billing v2 Payment Order and Entitlement per paid renewal period without overwriting the initial checkout order
- atomically bind each Creem renewal phase to immutable provider transaction facts and keep entitlement grants replay-safe
- advance the Subscription Agreement only after the renewal entitlement is active; exact replays do not rewrite the Agreement

This PR is intentionally limited to the Creem renewal path. It does not change Stripe, Antom, Apple, frontend entry visibility, Trial, cancellation/resume, upgrade/downgrade, refunds/disputes, Portal, or provider routing.

## Test plan

- [x] TDD coverage for a distinct renewal order, exact replay, stale/invalid facts, amount/customer conflicts, phase transaction conflicts, Billing Gateway failure, GRANTING recovery, concurrent ACTIVE recovery, and incomplete projections
- [x] Local related regression: 332 Creem/Card tests
- [x] Local legacy regression: 316 Stripe/Antom tests
- [x] Local shared Billing v2 regression: 140 tests
- [x] a102 exact-commit core tests: 47 passed
- [x] a102 exact-commit combined regression: 788 passed
- [x] a102 `scripts/verify-py.sh`: Ruff, format, Pyright (0 errors / 0 warnings), and 8/8 import contracts passed
- [x] repository file-length, complexity, dependency, database-contract, and dead-code pre-commit checks passed

Exact candidate commit verified on a102: `fef36f848`.


---
