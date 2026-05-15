# ecap-workspace - 2026-05-14 Commits
共 27 条 commit

---
## [1] 2db112c9
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T18:20:09Z
- **SHA**: 2db112c91279897b6158fccb3f99df9a0b6cbd03
- **PR**: #1649

### Commit Message

```
refactor(web): RQ v2 PR-c2 — claw resources shared via useClawResources (#1649)

## Why this instead of PR-e2 (SubscriptionPanel)?

The v2 spec listed SubscriptionPanel as PR-e2, but a fresh audit of
\`web/src/components/billing/SubscriptionPanel.tsx\` found:
- **Zero** \`useEffect + setState(data)\` patterns. The only
\`useEffect\` is an entry animation (\`requestAnimationFrame\` →
\`setVisible(true)\`).
- All 11 \`useState\` slots are **UI/form state** (modal flags, loading
flags, selections, animation visibility), not data state.
- Subscription data already comes from PR-b3's RQ-backed
\`useBillingCredits\`.
- Mutation flows (\`createOrder\`,
\`callAPI('/stripe/customer-portal')\`) are one-shot redirects —
wrapping in \`useMutation\` would be
boilerplate-without-behavior-change.

So PR-e2 isn't a useQuery candidate. Picked the **next clean PR-c
claw-settings candidate** instead: two duplicate
\`getClawResources(uid)\` fetchers sharing a hook.

## Summary

Two callers fetched claw bot resources independently before this PR:
- \`UsageTab.PlanResourcesCard\` — \`useEffect + setResources(data)\` on
uid change
- \`ClawSettingsClient\` — \`fetchResources\` callback +
\`useEffect([uid, botRunning])\` + passed as \`onRefresh\` to
\`DiagnosticsSection.ResourcesCard\`

Now both consume the same uid-scoped RQ bucket via the new
\`useClawResources(uid, botRunning)\` hook.

## Behavior delta

| Scenario | Before | After |
|---|---|---|
| Mount on Usage tab (cold) | 1 fetch | Same |
| Navigate Usage → Status within 30s | 2 fetches (re-fired by each
useEffect) | 1 fetch (shared bucket) |
| \`onRefresh\` click | \`fetchResources()\` | \`refetch()\` (same
backend call) |
| Logged-out / bot-not-ready | Fetch attempted, caught silently | Fetch
never fires (gated) |

## Tests

- \`useClawResources.unit.spec.ts\` — **6 new tests**: gates (uid=null,
botRunning=false), happy path, error path, two-consumer dedup,
production-like \`retry:1\` safeguard. Verify-first: stash \`retry:
false\` from source → safeguard test fails (5 of 6 pass).
- \`ClawSettingsClient.unit.spec.tsx\` — wrapped the \`render\` helper
in \`createQueryWrapper()\` (single-point edit covering 22 callsites).
All 27 existing tests pass without behavioral changes.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm vitest run
tests/unit/hooks/queries/openclaw/useClawResources.unit.spec.ts\` — 6/6
- [x] \`pnpm vitest run
tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx\` — 27/27
- [x] Verify-first: stash \`retry: false\` → safeguard fails; restore →
all pass
- [ ] CI: \`code-quality / lint-and-test\` green

## Part of

React Query migration v2 —
\`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Why this instead of PR-e2 (SubscriptionPanel)?

The v2 spec listed SubscriptionPanel as PR-e2, but a fresh audit of \`web/src/components/billing/SubscriptionPanel.tsx\` found:
- **Zero** \`useEffect + setState(data)\` patterns. The only \`useEffect\` is an entry animation (\`requestAnimationFrame\` → \`setVisible(true)\`).
- All 11 \`useState\` slots are **UI/form state** (modal flags, loading flags, selections, animation visibility), not data state.
- Subscription data already comes from PR-b3's RQ-backed \`useBillingCredits\`.
- Mutation flows (\`createOrder\`, \`callAPI('/stripe/customer-portal')\`) are one-shot redirects — wrapping in \`useMutation\` would be boilerplate-without-behavior-change.

So PR-e2 isn't a useQuery candidate. Picked the **next clean PR-c claw-settings candidate** instead: two duplicate \`getClawResources(uid)\` fetchers sharing a hook.

## Summary

Two callers fetched claw bot resources independently before this PR:
- \`UsageTab.PlanResourcesCard\` — \`useEffect + setResources(data)\` on uid change
- \`ClawSettingsClient\` — \`fetchResources\` callback + \`useEffect([uid, botRunning])\` + passed as \`onRefresh\` to \`DiagnosticsSection.ResourcesCard\`

Now both consume the same uid-scoped RQ bucket via the new \`useClawResources(uid, botRunning)\` hook.

## Behavior delta

| Scenario | Before | After |
|---|---|---|
| Mount on Usage tab (cold) | 1 fetch | Same |
| Navigate Usage → Status within 30s | 2 fetches (re-fired by each useEffect) | 1 fetch (shared bucket) |
| \`onRefresh\` click | \`fetchResources()\` | \`refetch()\` (same backend call) |
| Logged-out / bot-not-ready | Fetch attempted, caught silently | Fetch never fires (gated) |

## Tests

- \`useClawResources.unit.spec.ts\` — **6 new tests**: gates (uid=null, botRunning=false), happy path, error path, two-consumer dedup, production-like \`retry:1\` safeguard. Verify-first: stash \`retry: false\` from source → safeguard test fails (5 of 6 pass).
- \`ClawSettingsClient.unit.spec.tsx\` — wrapped the \`render\` helper in \`createQueryWrapper()\` (single-point edit covering 22 callsites). All 27 existing tests pass without behavioral changes.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm vitest run tests/unit/hooks/queries/openclaw/useClawResources.unit.spec.ts\` — 6/6
- [x] \`pnpm vitest run tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx\` — 27/27
- [x] Verify-first: stash \`retry: false\` → safeguard fails; restore → all pass
- [ ] CI: \`code-quality / lint-and-test\` green

## Part of

React Query migration v2 — \`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [2] c7020d07
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T18:14:34Z
- **SHA**: c7020d073f1144aed1b38899adf846475d859fd6
- **PR**: #1648

### Commit Message

```
chore(web): ratchet vitest coverage thresholds to floor(observed - 1.5%) (Phase 3) (#1648)

## Summary

**Phase 3** of the 71% → 78% coverage roadmap. Locks in the Phase 2
gains by ratcheting the vitest coverage thresholds up to `floor(observed
- 1.5%)` so any subsequent regression below the new floor fails CI
immediately.

## Coverage progression

| metric | 2026-04-22 baseline | 2026-05-14 post-Phase 2 | delta |
|---|---|---|---|
| lines | 71.45% | **77.24%** | +5.79pp |
| statements | 69.61% | 75.24% | +5.63pp |
| functions | 67.38% | 73.51% | +6.13pp |
| branches | 63.10% | 68.71% | +5.61pp |

## Threshold change

`floor(observed - 1.5%)` formula — 1.5pp buffer for run-to-run flake.

| metric | old | new | delta |
|---|---|---|---|
| lines | 69 | **75** | +6 |
| statements | 68 | 73 | +5 |
| functions | 65 | 72 | +7 |
| branches | 61 | 67 | +6 |

## Phase 2 PRs included in the new baseline

- PR #1635 — Phase 1 exclude legacy GenClawClient
- PR #1639 — RichTextInput tests (57 tests, +1.70pp lines)
- PR #1640 — OnboardingProvider tests (42 tests, +0.70pp lines)
- PR #1641 — AgentsManagerClient tests (28 tests, +0.22pp lines)
- PR #1643 — PublishAgentsClient incremental (4 tests, +0.04pp)
- PR #1644 — UploadsFeed (rebased to main's #1646 spec) +
WeixinSetupModal (16 tests, ~+0.5pp)
- PR #1645 — useBatchGrant (16 tests) + useChatReplayShare (18 tests,
+0.76pp)

## Test plan
- [x] `pnpm test:unit:coverage` — all 4 thresholds pass (lines 77.24 ≥
75 etc.)
- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

## Follow-up

The 78% aspirational target was not quite reached (77.24% lines). Two
deferred PRs from Phase 2 — SubagentChatPanel + MMAttachments — were
skipped due to heavy mock surface (assistant-ui runtime + Mattermost SDK
respectively). Those would close the remaining 0.7-1pp gap to 78%+ but
warrant their own dedicated PRs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

**Phase 3** of the 71% → 78% coverage roadmap. Locks in the Phase 2 gains by ratcheting the vitest coverage thresholds up to `floor(observed - 1.5%)` so any subsequent regression below the new floor fails CI immediately.

## Coverage progression

| metric | 2026-04-22 baseline | 2026-05-14 post-Phase 2 | delta |
|---|---|---|---|
| lines | 71.45% | **77.24%** | +5.79pp |
| statements | 69.61% | 75.24% | +5.63pp |
| functions | 67.38% | 73.51% | +6.13pp |
| branches | 63.10% | 68.71% | +5.61pp |

## Threshold change

`floor(observed - 1.5%)` formula — 1.5pp buffer for run-to-run flake.

| metric | old | new | delta |
|---|---|---|---|
| lines | 69 | **75** | +6 |
| statements | 68 | 73 | +5 |
| functions | 65 | 72 | +7 |
| branches | 61 | 67 | +6 |

## Phase 2 PRs included in the new baseline

- PR #1635 — Phase 1 exclude legacy GenClawClient
- PR #1639 — RichTextInput tests (57 tests, +1.70pp lines)
- PR #1640 — OnboardingProvider tests (42 tests, +0.70pp lines)
- PR #1641 — AgentsManagerClient tests (28 tests, +0.22pp lines)
- PR #1643 — PublishAgentsClient incremental (4 tests, +0.04pp)
- PR #1644 — UploadsFeed (rebased to main's #1646 spec) + WeixinSetupModal (16 tests, ~+0.5pp)
- PR #1645 — useBatchGrant (16 tests) + useChatReplayShare (18 tests, +0.76pp)

## Test plan
- [x] `pnpm test:unit:coverage` — all 4 thresholds pass (lines 77.24 ≥ 75 etc.)
- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

## Follow-up

The 78% aspirational target was not quite reached (77.24% lines). Two deferred PRs from Phase 2 — SubagentChatPanel + MMAttachments — were skipped due to heavy mock surface (assistant-ui runtime + Mattermost SDK respectively). Those would close the remaining 0.7-1pp gap to 78%+ but warrant their own dedicated PRs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [3] 645b8ed0
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T18:05:22Z
- **SHA**: 645b8ed0f43ddf992e0332b76ea0aaa6ccd4f91d
- **PR**: #1644

### Commit Message

```
test(web): UploadsFeed + WeixinSetupModal coverage (Phase 2 PR-E) (#1644)

## Summary

Two new specs targeting previously 0%-covered medium components —
**Phase 2 PR-E** of the 71% → 78% coverage roadmap (originally planned
as a "0% triplet" with SubagentChatPanel; that one rolls to a
follow-up).

## Coverage delta (measured locally 2026-05-14)

**File-level**

| file | before | after | delta |
|---|---|---|---|
| UploadsFeed.tsx | 0% (0/73) | **86.3%** (63/73) | +86pp |
| WeixinSetupModal.tsx | 0% (0/94) | **98.93%** (93/94) | +99pp |

**Global** (vs Phase-1 baseline of 72.69% lines)

| metric | before | after | delta |
|---|---|---|---|
| lines | 72.69% | **73.53%** | +0.84pp |

## What it covers

### UploadsFeed.unit.spec.tsx (17 tests)

Conversation-assets gallery in `/assets`:
- **initial render** (5) — loading spinner, empty state, populated grid,
error banner with Retry, generic-error fallback when reject is non-Error
- **agent filter** (3) — unique sorted agent list from `agent:<slug>`
session_ids, refetch on selection, `agentId=undefined` when "all" is
selected
- **pagination** (3) — Load More button visibility (>= PAGE_SIZE),
partial-page hides it, click appends next page with offset
- **preview interaction** (3) — image → `ImagePreview`, non-image →
`window.open`, close clears preview
- **AssetCard variants** (3) — extension placeholder, slug under
filename, mm-hosted spinner while auth blob is pending

### WeixinSetupModal.unit.spec.tsx (16 tests)

WeChat-binding QR-code modal — phase state machine (`loading` → `qr` →
`success` / `error`). Uses `vi.useFakeTimers` +
`advanceTimersByTimeAsync` per `web/CLAUDE.md` fake-timer/`waitFor`
rule:

- **initial loading and start** (4) — loading phase before resolve, qr
phase on resolve, error phase on reject (Error + non-Error)
- **poll status transitions** (5) — `success` → success phase, `expired`
→ error, `error` with/without server message, three consecutive poll
errors escalation
- **countdown expiry** (1) — flips to error when 1Hz countdown reaches 0
- **user actions** (4) — handleCancel cancels session + onClose,
handleSuccess calls onSuccess + onClose, handleRetry recreates session,
error-phase Close button
- **cleanup on unmount** (2) — cancels in-flight session, no-op when
never started

## SubagentChatPanel deferral

The planned third 0% target depends on `@assistant-ui/react`
`AssistantRuntimeProvider` + `useSubagentChat` WebSocket hook +
`useOpenClawRuntime`. Mocking that surface for jsdom is a much heavier
lift than the other two and warrants its own PR. The follow-up PR has
been left in the plan progress table.

## Test plan
- [x] `npx vitest run` on both new specs — 33/33 pass locally
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit:coverage` — global lines 72.69% → 73.53%
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Two new specs targeting previously 0%-covered medium components — **Phase 2 PR-E** of the 71% → 78% coverage roadmap (originally planned as a "0% triplet" with SubagentChatPanel; that one rolls to a follow-up).

## Coverage delta (measured locally 2026-05-14)

**File-level**

| file | before | after | delta |
|---|---|---|---|
| UploadsFeed.tsx | 0% (0/73) | **86.3%** (63/73) | +86pp |
| WeixinSetupModal.tsx | 0% (0/94) | **98.93%** (93/94) | +99pp |

**Global** (vs Phase-1 baseline of 72.69% lines)

| metric | before | after | delta |
|---|---|---|---|
| lines | 72.69% | **73.53%** | +0.84pp |

## What it covers

### UploadsFeed.unit.spec.tsx (17 tests)

Conversation-assets gallery in `/assets`:
- **initial render** (5) — loading spinner, empty state, populated grid, error banner with Retry, generic-error fallback when reject is non-Error
- **agent filter** (3) — unique sorted agent list from `agent:<slug>` session_ids, refetch on selection, `agentId=undefined` when "all" is selected
- **pagination** (3) — Load More button visibility (>= PAGE_SIZE), partial-page hides it, click appends next page with offset
- **preview interaction** (3) — image → `ImagePreview`, non-image → `window.open`, close clears preview
- **AssetCard variants** (3) — extension placeholder, slug under filename, mm-hosted spinner while auth blob is pending

### WeixinSetupModal.unit.spec.tsx (16 tests)

WeChat-binding QR-code modal — phase state machine (`loading` → `qr` → `success` / `error`). Uses `vi.useFakeTimers` + `advanceTimersByTimeAsync` per `web/CLAUDE.md` fake-timer/`waitFor` rule:

- **initial loading and start** (4) — loading phase before resolve, qr phase on resolve, error phase on reject (Error + non-Error)
- **poll status transitions** (5) — `success` → success phase, `expired` → error, `error` with/without server message, three consecutive poll errors escalation
- **countdown expiry** (1) — flips to error when 1Hz countdown reaches 0
- **user actions** (4) — handleCancel cancels session + onClose, handleSuccess calls onSuccess + onClose, handleRetry recreates session, error-phase Close button
- **cleanup on unmount** (2) — cancels in-flight session, no-op when never started

## SubagentChatPanel deferral

The planned third 0% target depends on `@assistant-ui/react` `AssistantRuntimeProvider` + `useSubagentChat` WebSocket hook + `useOpenClawRuntime`. Mocking that surface for jsdom is a much heavier lift than the other two and warrants its own PR. The follow-up PR has been left in the plan progress table.

## Test plan
- [x] `npx vitest run` on both new specs — 33/33 pass locally
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit:coverage` — global lines 72.69% → 73.53%
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [4] eb8012fe
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T18:05:02Z
- **SHA**: eb8012fed5d5890b4225c425d2387b9930e7347f
- **PR**: #1640

### Commit Message

```
test(web): unit tests for OnboardingProvider (coverage Phase 2 PR-B) (#1640)

## Summary

Adds a 42-test spec for `components/providers/OnboardingProvider` — the
global onboarding context provider mounted in `ClientLayout`. This is
**Phase 2 PR-B** of the 71% → 78% coverage roadmap.

The provider orchestrates state from five inputs (auth, billing-credits,
agent-catalog, backend-status events, uid-scoped localStorage progress)
and seven outputs (modal open / current step / progress / phase /
companion / canUseChat / mutation callbacks). Pure resolver logic in
`lib/onboarding/resolve-status.ts` is tested separately; this spec
covers the provider's wiring of inputs to state, modal auto-open/close,
step mutations, and side effects on `completeOnboarding`.

## Coverage delta (measured locally 2026-05-14)

**File-level (`components/providers/OnboardingProvider.tsx`)**

| metric | before | after | delta |
|---|---|---|---|
| lines | 0% (0/181) | **90.05%** (163/181) | +90pp |
| functions | ~0% | **95.12%** (39/41) | +95pp |
| branches | ~0% | **75.73%** (128/169) | +76pp |

**Global** (vs Phase-1 baseline of 72.69% lines)

| metric | before | after | delta |
|---|---|---|---|
| lines | 72.69% | **73.39%** | +0.70pp |
| statements | 70.84% | 71.55% | +0.71pp |
| functions | 69.71% | 70.48% | +0.77pp |
| branches | 65.10% | 65.71% | +0.61pp |

All four threshold metrics remain above existing CI gates (`lines 69 /
statements 68 / functions 65 / branches 61`), so **no threshold change
in this PR**.

## What it covers (8 describe blocks, 42 tests)

- **render & context exposure** (5) — children + modal mount, context
shape, `canUseChat` for various auth states
- **modal open/close** (6) — auto-open on non-public pages, suppression
on `/`, `/en`, `/pricing`, manual `showOnboarding` / `hideOnboarding`,
auto-close on resolution settle
- **backend-status event subscription** (3) —
`onboarding-backend-status` CustomEvent updates state,
`getLastBackendStatus()` queried during init, uid change clears cached
status
- **credit signals forwarded to resolver** (2) — `creditsFetched` and
`availableCredits` reach the resolver via top-level signals (not via
`backendStatus` merge — see "Notes" below)
- **uid-scoped progress load/save** (3) — `loadProgress(uid)` seeds
state, `null` falls back to `DEFAULT_PROGRESS`, no `loadProgress` call
when uid is undefined
- **step navigation** (5) — initial step is `inviteCode`, `nextStep` /
`skipStep` / `prevStep` mark progress and skip hidden steps backwards
- **hidden steps auto-skip** (1) — `reminder` / `channel` flipped to
`true` post-mount
- **completeOnboarding side effects** (5) — `triggerCreditsRefresh`
called, welcome event dispatched only for first-time users, `recreate`
flag cleared, completed progress persisted, modal closes after
completion
- **companion selection** (3) — read from `localStorage`, `null` when
absent, malformed JSON doesn't crash
- **onboarding phase** (2) — starts at `intro`,
`setOnboardingPhase('steps')` transitions
- **preload links** (2) — base image preloads + agent-avatar preloads
from catalog (filters out `agent_studio` and non-pack types)
- **pending state** (3) — `isPending` true while resolver returns
`pending` or auth is loading; `isSettled` flips when both settle

## Notes

Three test design choices documented inline in the spec:

1. **`next/navigation` mocked with explicit refs**, not via
`nextNavigationDefaults()`. The helper snapshots the mock at module-mock
time so per-test pathname overrides aren't possible — this provider
needs that to verify public-page guards.

2. **The cached `backendStatus` useState seed isn't asserted directly**:
the uid-change effect immediately clears it (anti-leak guard for
cross-user state). The spec verifies `getLastBackendStatus` IS called
rather than asserting the resolver received the cache.

3. **The credit-merge effect only refires when `useBillingCredits` hook
values change** between renders, which jsdom can't drive
deterministically. The spec verifies `creditsFetched` flows through to
the resolver as a top-level signal — that's the actual contract used by
the resolver to gate `isActiveUser` independently.

## Test plan
- [x] `npx vitest run
tests/unit/components/providers/OnboardingProvider.unit.spec.tsx` —
42/42 pass locally
- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup` — under threshold
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Adds a 42-test spec for `components/providers/OnboardingProvider` — the global onboarding context provider mounted in `ClientLayout`. This is **Phase 2 PR-B** of the 71% → 78% coverage roadmap.

The provider orchestrates state from five inputs (auth, billing-credits, agent-catalog, backend-status events, uid-scoped localStorage progress) and seven outputs (modal open / current step / progress / phase / companion / canUseChat / mutation callbacks). Pure resolver logic in `lib/onboarding/resolve-status.ts` is tested separately; this spec covers the provider's wiring of inputs to state, modal auto-open/close, step mutations, and side effects on `completeOnboarding`.

## Coverage delta (measured locally 2026-05-14)

**File-level (`components/providers/OnboardingProvider.tsx`)**

| metric | before | after | delta |
|---|---|---|---|
| lines | 0% (0/181) | **90.05%** (163/181) | +90pp |
| functions | ~0% | **95.12%** (39/41) | +95pp |
| branches | ~0% | **75.73%** (128/169) | +76pp |

**Global** (vs Phase-1 baseline of 72.69% lines)

| metric | before | after | delta |
|---|---|---|---|
| lines | 72.69% | **73.39%** | +0.70pp |
| statements | 70.84% | 71.55% | +0.71pp |
| functions | 69.71% | 70.48% | +0.77pp |
| branches | 65.10% | 65.71% | +0.61pp |

All four threshold metrics remain above existing CI gates (`lines 69 / statements 68 / functions 65 / branches 61`), so **no threshold change in this PR**.

## What it covers (8 describe blocks, 42 tests)

- **render & context exposure** (5) — children + modal mount, context shape, `canUseChat` for various auth states
- **modal open/close** (6) — auto-open on non-public pages, suppression on `/`, `/en`, `/pricing`, manual `showOnboarding` / `hideOnboarding`, auto-close on resolution settle
- **backend-status event subscription** (3) — `onboarding-backend-status` CustomEvent updates state, `getLastBackendStatus()` queried during init, uid change clears cached status
- **credit signals forwarded to resolver** (2) — `creditsFetched` and `availableCredits` reach the resolver via top-level signals (not via `backendStatus` merge — see "Notes" below)
- **uid-scoped progress load/save** (3) — `loadProgress(uid)` seeds state, `null` falls back to `DEFAULT_PROGRESS`, no `loadProgress` call when uid is undefined
- **step navigation** (5) — initial step is `inviteCode`, `nextStep` / `skipStep` / `prevStep` mark progress and skip hidden steps backwards
- **hidden steps auto-skip** (1) — `reminder` / `channel` flipped to `true` post-mount
- **completeOnboarding side effects** (5) — `triggerCreditsRefresh` called, welcome event dispatched only for first-time users, `recreate` flag cleared, completed progress persisted, modal closes after completion
- **companion selection** (3) — read from `localStorage`, `null` when absent, malformed JSON doesn't crash
- **onboarding phase** (2) — starts at `intro`, `setOnboardingPhase('steps')` transitions
- **preload links** (2) — base image preloads + agent-avatar preloads from catalog (filters out `agent_studio` and non-pack types)
- **pending state** (3) — `isPending` true while resolver returns `pending` or auth is loading; `isSettled` flips when both settle

## Notes

Three test design choices documented inline in the spec:

1. **`next/navigation` mocked with explicit refs**, not via `nextNavigationDefaults()`. The helper snapshots the mock at module-mock time so per-test pathname overrides aren't possible — this provider needs that to verify public-page guards.

2. **The cached `backendStatus` useState seed isn't asserted directly**: the uid-change effect immediately clears it (anti-leak guard for cross-user state). The spec verifies `getLastBackendStatus` IS called rather than asserting the resolver received the cache.

3. **The credit-merge effect only refires when `useBillingCredits` hook values change** between renders, which jsdom can't drive deterministically. The spec verifies `creditsFetched` flows through to the resolver as a top-level signal — that's the actual contract used by the resolver to gate `isActiveUser` independently.

## Test plan
- [x] `npx vitest run tests/unit/components/providers/OnboardingProvider.unit.spec.tsx` — 42/42 pass locally
- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup` — under threshold
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [5] 0658ba40
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T17:56:41Z
- **SHA**: 0658ba4088c0835032ed29d25035641a47c9963b
- **PR**: #1647

### Commit Message

```
refactor(web): RQ v2 PR-f4 — CronClient jobs list switches to useQuery (#1647)

## Summary

Migrates the **cron-jobs list fetch** in
\`/[locale]/schedule/CronClient.tsx\` from imperative \`useState +
loadCronData()\` + wsStatus-watching useEffect onto a single
\`useQuery\`. Last large migration in the v2 spec.

### What changed

- Replaced 3 state slots (\`rawJobs\`, \`jobsLoading\`, \`jobsError\`) +
\`dataLoadedRef\` + wsStatus useEffect → one \`useQuery\`
- 5 imperative \`loadCronData()\` call sites (mutation handlers +
Refresh button + history removal) → stable \`refetchJobs\` wrapping
\`queryClient.refetchQueries(cronKeys.jobs(authToken))\`
- \`fetchCronJobs\` REST + \`cron.list\` WS fallback preserved inside
the queryFn (try/catch unchanged)
- Dropped underscore-prefixed \`_cronStatus\` state slot;
fire-and-forget \`cron.status\` call preserved inside queryFn so any
backend-side wake-up effect is unchanged

### What's NOT changed

- **Runs list** (\`loadRuns\` + selectedJobId-gated fetch) — separate
concern, deferred
- **CUD mutations** (\`cron.add\` / \`cron.update\` / \`cron.remove\` /
\`cron.run\`) — WS-transport, not HTTP. Wrapping in \`useMutation\`
would be boilerplate-without-behavior-change. They invoke
\`refetchJobs\` on success to refresh the list, identical pre-RQ
semantics.
- **Hover tooltip lastRun cache** — lazy, ref-backed, fine as-is

### New domain

\`src/hooks/queries/cron/keys.ts\` with \`cronKeys.jobs(authToken)\`.
Token-scoped, same pattern as \`openclawKeys.agents\` / PR-f3's
\`assetsKeys.list\`.

### Per-query overrides (same playbook as PR-f3)

| Override | Why |
|---|---|
| \`retry: false\` | Pre-RQ never retried — app-wide \`retry: 1\` would
double the call count on failure |
| \`staleTime: 0\` + \`refetchOnMount: 'always'\` | Cron-job state is
user-mutated; need fresh data on every visit |
| \`enabled: !!authToken && wsStatus === 'connected'\` | Preserves
pre-RQ "wait for WS connect" gate; token in queryKey |
| \`jobsLoading = ... && (isPending \|\| isFetching)\` | Gates v5's
disabled-stays-pending trap (PR-f2 / PR-f3 pattern) |
| \`useMemo(() => data ?? [], [data])\` | Keeps the empty-array
reference stable for downstream filter useEffect |

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm vitest run
tests/unit/app/schedule/cron-client.unit.spec.tsx\` — **61 + 1 todo / 62
pass** (60 pre-existing + 1 new safeguard)
- [x] Verify-first: stashed \`retry: false\` from source, rerun
production-default safeguard test → fails. With override → passes.
- [x] Mock added for \`@/lib/auth/storage.getUserInfo\` (jsdom default
has no localStorage, would disable the query)
- [ ] CI: \`code-quality / lint-and-test\` green

## Test wrapper change

Single \`render()\` call in the 1553-line test file (line 127 helper) —
wrapped in \`createQueryWrapper()\`. No per-test plumbing.

## Part of

React Query migration v2 — see
\`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Migrates the **cron-jobs list fetch** in \`/[locale]/schedule/CronClient.tsx\` from imperative \`useState + loadCronData()\` + wsStatus-watching useEffect onto a single \`useQuery\`. Last large migration in the v2 spec.

### What changed

- Replaced 3 state slots (\`rawJobs\`, \`jobsLoading\`, \`jobsError\`) + \`dataLoadedRef\` + wsStatus useEffect → one \`useQuery\`
- 5 imperative \`loadCronData()\` call sites (mutation handlers + Refresh button + history removal) → stable \`refetchJobs\` wrapping \`queryClient.refetchQueries(cronKeys.jobs(authToken))\`
- \`fetchCronJobs\` REST + \`cron.list\` WS fallback preserved inside the queryFn (try/catch unchanged)
- Dropped underscore-prefixed \`_cronStatus\` state slot; fire-and-forget \`cron.status\` call preserved inside queryFn so any backend-side wake-up effect is unchanged

### What's NOT changed

- **Runs list** (\`loadRuns\` + selectedJobId-gated fetch) — separate concern, deferred
- **CUD mutations** (\`cron.add\` / \`cron.update\` / \`cron.remove\` / \`cron.run\`) — WS-transport, not HTTP. Wrapping in \`useMutation\` would be boilerplate-without-behavior-change. They invoke \`refetchJobs\` on success to refresh the list, identical pre-RQ semantics.
- **Hover tooltip lastRun cache** — lazy, ref-backed, fine as-is

### New domain

\`src/hooks/queries/cron/keys.ts\` with \`cronKeys.jobs(authToken)\`. Token-scoped, same pattern as \`openclawKeys.agents\` / PR-f3's \`assetsKeys.list\`.

### Per-query overrides (same playbook as PR-f3)

| Override | Why |
|---|---|
| \`retry: false\` | Pre-RQ never retried — app-wide \`retry: 1\` would double the call count on failure |
| \`staleTime: 0\` + \`refetchOnMount: 'always'\` | Cron-job state is user-mutated; need fresh data on every visit |
| \`enabled: !!authToken && wsStatus === 'connected'\` | Preserves pre-RQ "wait for WS connect" gate; token in queryKey |
| \`jobsLoading = ... && (isPending \|\| isFetching)\` | Gates v5's disabled-stays-pending trap (PR-f2 / PR-f3 pattern) |
| \`useMemo(() => data ?? [], [data])\` | Keeps the empty-array reference stable for downstream filter useEffect |

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm vitest run tests/unit/app/schedule/cron-client.unit.spec.tsx\` — **61 + 1 todo / 62 pass** (60 pre-existing + 1 new safeguard)
- [x] Verify-first: stashed \`retry: false\` from source, rerun production-default safeguard test → fails. With override → passes.
- [x] Mock added for \`@/lib/auth/storage.getUserInfo\` (jsdom default has no localStorage, would disable the query)
- [ ] CI: \`code-quality / lint-and-test\` green

## Test wrapper change

Single \`render()\` call in the 1553-line test file (line 127 helper) — wrapped in \`createQueryWrapper()\`. No per-test plumbing.

## Part of

React Query migration v2 — see \`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [6] 1846ddb6
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T17:56:18Z
- **SHA**: 1846ddb6779c540c9b8e9e1c260ccc6ef779650e
- **PR**: #1634

### Commit Message

```
refactor(web): RQ v2 PR-e1 — InvoiceHistory order list switches to useQuery (#1634)

## Summary

PR-e1 lands the first half of the spec's "billing surface" (high-risk
series — affects paid users). `InvoiceHistory`'s order list moves from
`useEffect + useState(orders) + loadOrders()` to a single `useQuery`
keyed on uid via the new `billingKeys.orders(uid)` factory.

## Why this PR is narrower than spec PR-e

Spec PR-e estimates 3 components (`PaywallContent` / `InvoiceHistory` /
`SubscriptionPanel`). Audit found:

| Component | Lines | Reality | Decision |
|---|---:|---|---|
| **InvoiceHistory** | 310 | useEffect + setOrders for `getOrdersList`
read | **This PR (e1)** |
| **SubscriptionPanel** | 856 | multi-mutation + 12+ useState + 2 read
effects | **PR-e2** (split for size) |
| **PaywallContent** | 200 | One useEffect is a setTimeout promo-price
transition; rest is mutation form (`createOrder`) | **Skip** (not
anti-pattern) |

PaywallContent is skipped (mutation-only). SubscriptionPanel lands
separately to keep each diff reviewable. spec's high-risk
staging-regression discipline applies to **both** e1 and e2.

## Pattern checklist

- [x] `refetchOnMount: 'always'` — fresh fetch on every mount so a
post-checkout return to the invoice tab shows the new order
- [x] uid-scoped queryKey via new `billingKeys.orders(uid)` (sibling to
PR-b3's `billingKeys.credits`)
- [x] `orders` derived via `useMemo` (referentially stable empty
fallback)
- [x] `loading = !!uid && query.isPending` — gates against v5's
disabled-pending state
- N/A `cancelQueries / invalidateQueries` — this component doesn't
mutate the orders cache. Future order-creating mutations (e.g.
`SubscriptionPanel.createOrder` in PR-e2) should invalidate
`billingKeys.orders(uid)` so a successful checkout reflects back here.

## What's *not* changed

- `openCustomerPortal` (Stripe billing portal redirect) stays imperative
— pure redirect, no cache.
- `downloadInvoice` (popup-then-navigate dance for ECA-669 Safari
popup-blocker workaround) stays imperative.
- Order pagination is currently hardcoded `(1, 10)`. When pagination
ships, page + limit should lift into the queryKey tuple — noted in
`keys.ts` comment.

## Test plan

- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `npx vitest run
tests/unit/components/billing/InvoiceHistory.unit.spec.tsx` — 18/18 pass
(no behavior change, just wrapper threading)
- [ ] **Staging visual regression** (per spec PR-e discipline):
`/claw-settings/billing` tab → invoice list renders, Stripe portal
redirect works, invoice download popup opens
- [ ] **Staging functional**: complete a test checkout → return to
invoice tab → new order appears (verifies `refetchOnMount: 'always'`)

Refs: \`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`
PR series: PR-a / b / c1 / d1 / d2 merged → this (PR-e1) → PR-e2
(`SubscriptionPanel`) → PR-f

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

PR-e1 lands the first half of the spec's "billing surface" (high-risk series — affects paid users). `InvoiceHistory`'s order list moves from `useEffect + useState(orders) + loadOrders()` to a single `useQuery` keyed on uid via the new `billingKeys.orders(uid)` factory.

## Why this PR is narrower than spec PR-e

Spec PR-e estimates 3 components (`PaywallContent` / `InvoiceHistory` / `SubscriptionPanel`). Audit found:

| Component | Lines | Reality | Decision |
|---|---:|---|---|
| **InvoiceHistory** | 310 | useEffect + setOrders for `getOrdersList` read | **This PR (e1)** |
| **SubscriptionPanel** | 856 | multi-mutation + 12+ useState + 2 read effects | **PR-e2** (split for size) |
| **PaywallContent** | 200 | One useEffect is a setTimeout promo-price transition; rest is mutation form (`createOrder`) | **Skip** (not anti-pattern) |

PaywallContent is skipped (mutation-only). SubscriptionPanel lands separately to keep each diff reviewable. spec's high-risk staging-regression discipline applies to **both** e1 and e2.

## Pattern checklist

- [x] `refetchOnMount: 'always'` — fresh fetch on every mount so a post-checkout return to the invoice tab shows the new order
- [x] uid-scoped queryKey via new `billingKeys.orders(uid)` (sibling to PR-b3's `billingKeys.credits`)
- [x] `orders` derived via `useMemo` (referentially stable empty fallback)
- [x] `loading = !!uid && query.isPending` — gates against v5's disabled-pending state
- N/A `cancelQueries / invalidateQueries` — this component doesn't mutate the orders cache. Future order-creating mutations (e.g. `SubscriptionPanel.createOrder` in PR-e2) should invalidate `billingKeys.orders(uid)` so a successful checkout reflects back here.

## What's *not* changed

- `openCustomerPortal` (Stripe billing portal redirect) stays imperative — pure redirect, no cache.
- `downloadInvoice` (popup-then-navigate dance for ECA-669 Safari popup-blocker workaround) stays imperative.
- Order pagination is currently hardcoded `(1, 10)`. When pagination ships, page + limit should lift into the queryKey tuple — noted in `keys.ts` comment.

## Test plan

- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `npx vitest run tests/unit/components/billing/InvoiceHistory.unit.spec.tsx` — 18/18 pass (no behavior change, just wrapper threading)
- [ ] **Staging visual regression** (per spec PR-e discipline): `/claw-settings/billing` tab → invoice list renders, Stripe portal redirect works, invoice download popup opens
- [ ] **Staging functional**: complete a test checkout → return to invoice tab → new order appears (verifies `refetchOnMount: 'always'`)

Refs: \`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`
PR series: PR-a / b / c1 / d1 / d2 merged → this (PR-e1) → PR-e2 (`SubscriptionPanel`) → PR-f

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [7] d840f2dc
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T17:51:06Z
- **SHA**: d840f2dc8166275770269cd87396eca71729fdd4
- **PR**: #1643

### Commit Message

```
test(web): cover Escape state machine + error catches in PublishAgentsClient (Phase 2 PR-D) (#1643)

## Summary

Appends 4 tests to the existing focused install/uninstall spec
(`agents-manager-publish.unit.spec.tsx`) targeting the residual ~58
uncovered lines after the install-state CTA describe — specifically the
Escape key state machine and two error-catch branches.

This is **Phase 2 PR-D** (incremental targeting) of the 71% → 78%
coverage roadmap. PublishAgentsClient was already 77% covered going in;
this PR is intentionally small because the higher-ROI 0%-coverage
targets are handled by **Phase 2 PR-E** (WeixinSetupModal +
SubagentChatPanel + UploadsFeed triplet) and **Phase 2 PR-F** (admin
hook + chat hook + mattermost).

## Coverage delta (measured locally 2026-05-14)

| metric | before | after | delta |
|---|---|---|---|
| PublishAgentsClient.tsx lines | 77.25% (197/255) | **80.39%**
(205/255) | +3pp |
| Global lines (vs Phase-1 baseline) | 72.69% | 72.73% | +0.04pp |

## What's added

- **Escape state machine**: `Escape` closes the create modal when only
it is open; non-Escape keys (`Enter`, `a`) do not affect modal state.
- **Error catch in `refreshInstalledState`**: a rejection from
`getOpenClawAgents` surfaces the `installStateLoadFailed` translation
key in the error banner.
- **Error catch in zip-package fetch**: a rejection from
`getCustomAgentZipPackages` is swallowed by the `.catch()`, leaving
`zipPackageOptions: []`, which the select renders with the
`noAgentPackages` placeholder option.

## Test plan
- [x] `npx vitest run
tests/unit/app/agents-manager-publish.unit.spec.tsx` — 19/19 pass
locally
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit:coverage` — file lines 77.25% → 80.39%
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Appends 4 tests to the existing focused install/uninstall spec (`agents-manager-publish.unit.spec.tsx`) targeting the residual ~58 uncovered lines after the install-state CTA describe — specifically the Escape key state machine and two error-catch branches.

This is **Phase 2 PR-D** (incremental targeting) of the 71% → 78% coverage roadmap. PublishAgentsClient was already 77% covered going in; this PR is intentionally small because the higher-ROI 0%-coverage targets are handled by **Phase 2 PR-E** (WeixinSetupModal + SubagentChatPanel + UploadsFeed triplet) and **Phase 2 PR-F** (admin hook + chat hook + mattermost).

## Coverage delta (measured locally 2026-05-14)

| metric | before | after | delta |
|---|---|---|---|
| PublishAgentsClient.tsx lines | 77.25% (197/255) | **80.39%** (205/255) | +3pp |
| Global lines (vs Phase-1 baseline) | 72.69% | 72.73% | +0.04pp |

## What's added

- **Escape state machine**: `Escape` closes the create modal when only it is open; non-Escape keys (`Enter`, `a`) do not affect modal state.
- **Error catch in `refreshInstalledState`**: a rejection from `getOpenClawAgents` surfaces the `installStateLoadFailed` translation key in the error banner.
- **Error catch in zip-package fetch**: a rejection from `getCustomAgentZipPackages` is swallowed by the `.catch()`, leaving `zipPackageOptions: []`, which the select renders with the `noAgentPackages` placeholder option.

## Test plan
- [x] `npx vitest run tests/unit/app/agents-manager-publish.unit.spec.tsx` — 19/19 pass locally
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit:coverage` — file lines 77.25% → 80.39%
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [8] d94849ba
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T17:39:39Z
- **SHA**: d94849ba949aacbede809f0ccf3d545c54be2872
- **PR**: #1639

### Commit Message

```
test(web): comprehensive unit tests for RichTextInput (coverage Phase 2 PR-A) (#1639)

## Summary

Adds a comprehensive 56-test main spec for
`components/RichTextInput.tsx` that complements the focused
`RichTextInput.paste.unit.spec.tsx` (large-paste-to-file branch only).
This is **Phase 2 PR-A** of the 71% → 78% coverage roadmap.

The spec covers the rest of the component's surface — markdown↔editor
sync, chip rendering, keyboard handling, drag/drop, IME composition,
click handlers, and uploading-chip lifecycle. RichTextInput is a hot
spot: 4 importers across chat / canvas / agent inputs, recent activity
(#1631 large-paste auto-attach), and the largest single source of
uncovered lines in the codebase.

## Coverage delta (measured locally 2026-05-14)

**File-level (`components/RichTextInput.tsx`)**

| metric | before | after | delta |
|---|---|---|---|
| lines | 15.4% (67/435) | **85.4%** (380/445) | +70pp |
| functions | ~20% (28/138) | **94.9%** (37/39) | +75pp |
| branches | ~11% (54/472) | **76.7%** (243/317) | +66pp |

**Global**

| metric | before (post-PR-#1635) | after | delta |
|---|---|---|---|
| lines | 72.69% (13331/18338) | **74.39%** (13639/18333) | +1.70pp |
| statements | 70.84% | 72.44% | +1.60pp |
| functions | 69.71% | 70.36% | +0.65pp |
| branches | 65.10% | 66.46% | +1.36pp |

All four threshold metrics remain above existing CI gates (`lines 69 /
statements 68 / functions 65 / branches 61`), so **no threshold change
in this PR**. The threshold ratchet is deferred to a separate PR after
Phase 2 is fully landed.

## What it covers

- **render basics**: contenteditable, placeholder data-attribute toggle,
disabled state, className, outline:none style
- **markdown → editor sync**: image / video / link chip rendering, alt
fallback (image1, image2…), mixed text+chips, BR newlines, empty-URL
placeholder (📷), uploading chip animate-pulse + label
- **editor → markdown round-trip**: text input, image / video / link
chip serialization, BR → \n
- **paste branches**: file routing, MIME / extension / wildcard accept
rules, HTML chip extraction, bare-URL → link chip, plain-text markdown
re-insert, plain-text inline
- **drag & drop**: file routing, type filtering, dragOver
preventDefault, no-onFileDrop guard
- **keyboard**: Enter → onSubmit (Shift+Enter passthrough),
Backspace-before-chip / Delete-after-chip removal, Cmd/Ctrl+A
select-all, arbitrary-key forwarding
- **IME composition**: start/end forwarding, Enter ignored while
composing
- **focus & click**: anchor preventDefault, image-chip preview /
empty-chip upload / uploading-chip no-op
- **uploading chip lifecycle**: replace on URL settle, remove on failure

## Notes

- jsdom contentEditable + Selection API quirks: tests that exercise
`insertMediaMarkdown` / `detectAndConvertUrls` need `editor.focus() +
placeCursorAtEnd(editor)` before firing the paste, since these helpers
bail when `selection.rangeCount === 0` (a real browser sets up a Range
on the focus click; jsdom doesn't).
- Did not assert full Tailwind class strings (per `web/CLAUDE.md`
Testing rule) — assertions target structural contract: `data-url` /
`data-alt` / `data-type` attributes, presence of `<img>`, presence of
icon emoji in chip text content.

## Test plan
- [x] `npx vitest run tests/unit/components/RichTextInput.unit.spec.tsx`
— 57/57 pass locally
- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup` — 6.24% (under 7.5% threshold)
- [ ] CI `code-quality / lint-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Adds a comprehensive 56-test main spec for `components/RichTextInput.tsx` that complements the focused `RichTextInput.paste.unit.spec.tsx` (large-paste-to-file branch only). This is **Phase 2 PR-A** of the 71% → 78% coverage roadmap.

The spec covers the rest of the component's surface — markdown↔editor sync, chip rendering, keyboard handling, drag/drop, IME composition, click handlers, and uploading-chip lifecycle. RichTextInput is a hot spot: 4 importers across chat / canvas / agent inputs, recent activity (#1631 large-paste auto-attach), and the largest single source of uncovered lines in the codebase.

## Coverage delta (measured locally 2026-05-14)

**File-level (`components/RichTextInput.tsx`)**

| metric | before | after | delta |
|---|---|---|---|
| lines | 15.4% (67/435) | **85.4%** (380/445) | +70pp |
| functions | ~20% (28/138) | **94.9%** (37/39) | +75pp |
| branches | ~11% (54/472) | **76.7%** (243/317) | +66pp |

**Global**

| metric | before (post-PR-#1635) | after | delta |
|---|---|---|---|
| lines | 72.69% (13331/18338) | **74.39%** (13639/18333) | +1.70pp |
| statements | 70.84% | 72.44% | +1.60pp |
| functions | 69.71% | 70.36% | +0.65pp |
| branches | 65.10% | 66.46% | +1.36pp |

All four threshold metrics remain above existing CI gates (`lines 69 / statements 68 / functions 65 / branches 61`), so **no threshold change in this PR**. The threshold ratchet is deferred to a separate PR after Phase 2 is fully landed.

## What it covers

- **render basics**: contenteditable, placeholder data-attribute toggle, disabled state, className, outline:none style
- **markdown → editor sync**: image / video / link chip rendering, alt fallback (image1, image2…), mixed text+chips, BR newlines, empty-URL placeholder (📷), uploading chip animate-pulse + label
- **editor → markdown round-trip**: text input, image / video / link chip serialization, BR → \n
- **paste branches**: file routing, MIME / extension / wildcard accept rules, HTML chip extraction, bare-URL → link chip, plain-text markdown re-insert, plain-text inline
- **drag & drop**: file routing, type filtering, dragOver preventDefault, no-onFileDrop guard
- **keyboard**: Enter → onSubmit (Shift+Enter passthrough), Backspace-before-chip / Delete-after-chip removal, Cmd/Ctrl+A select-all, arbitrary-key forwarding
- **IME composition**: start/end forwarding, Enter ignored while composing
- **focus & click**: anchor preventDefault, image-chip preview / empty-chip upload / uploading-chip no-op
- **uploading chip lifecycle**: replace on URL settle, remove on failure

## Notes

- jsdom contentEditable + Selection API quirks: tests that exercise `insertMediaMarkdown` / `detectAndConvertUrls` need `editor.focus() + placeCursorAtEnd(editor)` before firing the paste, since these helpers bail when `selection.rangeCount === 0` (a real browser sets up a Range on the focus click; jsdom doesn't).
- Did not assert full Tailwind class strings (per `web/CLAUDE.md` Testing rule) — assertions target structural contract: `data-url` / `data-alt` / `data-type` attributes, presence of `<img>`, presence of icon emoji in chip text content.

## Test plan
- [x] `npx vitest run tests/unit/components/RichTextInput.unit.spec.tsx` — 57/57 pass locally
- [x] `pnpm lint` — clean
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup` — 6.24% (under 7.5% threshold)
- [ ] CI `code-quality / lint-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [9] 9285f357
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T17:36:11Z
- **SHA**: 9285f3571cc60e2ae8f2f993155299950a936b42
- **PR**: #1641

### Commit Message

```
test(web): comprehensive unit tests for AgentsManagerClient (coverage Phase 2 PR-C) (#1641)

## Summary

Adds a 28-test spec for
`app/[locale]/agents-manager/AgentsManagerClient` covering hire / fire /
update flows + filter UI + escape state machine. Complements the
existing focused spec
(`tests/unit/app/agents-manager-client.unit.spec.tsx`, 4 tests on legacy
filtering + happy-path update flow) without overlap. **Phase 2 PR-C** of
the 71% → 78% coverage roadmap.

## Coverage delta (measured locally 2026-05-14)

**File-level (`AgentsManagerClient.tsx`)**

| metric | before | after | delta |
|---|---|---|---|
| lines | 56.33% (80/142) | **85.21%** (121/142) | +29pp |
| functions | ~50% | **70.37%** (38/54) | +20pp |
| branches | ~50% | **71.32%** (102/143) | +21pp |

**Global** (vs Phase-1 baseline of 72.69% lines)

| metric | before | after | delta |
|---|---|---|---|
| lines | 72.69% | **72.91%** | +0.22pp |

Smaller global delta than PR-A / PR-B because this file already had ~80
lines covered indirectly by other tests. The new spec brings the last
~40 uncovered lines (mostly modal JSX branches + escape state) into
coverage.

## What it covers

- **render basics** (5) — title/subtitle, publish button auth gate,
loading skeletons, error banner, default catalog
- **category filter** (3) — productivity / lifestyle / all toggle
visibility
- **publish entry** (1) — navigation to publish route
- **hire flow** (5) — open confirm modal, confirm calls hireAgent +
success modal, cancel guard, hide button when already hired, isLocked
guards (disabled + modal-doesn't-open)
- **fire flow** (4) — more-menu dropdown, fire-confirm modal, "type FIRE
to enable" gating, success modal
- **chat-redirect** (1) — hired-agent startChat navigates with agent_id
- **escape state machine** (5) — closes more-menu / confirm-hire /
hire-success / fire-confirm; non-Escape ignored
- **syncing modal** (1) — visibility flag
- **has_update badge** (2) — New badge + "Updating…" label

## Test plan
- [x] `npx vitest run
tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx` — 28/28
pass locally
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit:coverage` — file lines 56.33% → 85.21%
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Adds a 28-test spec for `app/[locale]/agents-manager/AgentsManagerClient` covering hire / fire / update flows + filter UI + escape state machine. Complements the existing focused spec (`tests/unit/app/agents-manager-client.unit.spec.tsx`, 4 tests on legacy filtering + happy-path update flow) without overlap. **Phase 2 PR-C** of the 71% → 78% coverage roadmap.

## Coverage delta (measured locally 2026-05-14)

**File-level (`AgentsManagerClient.tsx`)**

| metric | before | after | delta |
|---|---|---|---|
| lines | 56.33% (80/142) | **85.21%** (121/142) | +29pp |
| functions | ~50% | **70.37%** (38/54) | +20pp |
| branches | ~50% | **71.32%** (102/143) | +21pp |

**Global** (vs Phase-1 baseline of 72.69% lines)

| metric | before | after | delta |
|---|---|---|---|
| lines | 72.69% | **72.91%** | +0.22pp |

Smaller global delta than PR-A / PR-B because this file already had ~80 lines covered indirectly by other tests. The new spec brings the last ~40 uncovered lines (mostly modal JSX branches + escape state) into coverage.

## What it covers

- **render basics** (5) — title/subtitle, publish button auth gate, loading skeletons, error banner, default catalog
- **category filter** (3) — productivity / lifestyle / all toggle visibility
- **publish entry** (1) — navigation to publish route
- **hire flow** (5) — open confirm modal, confirm calls hireAgent + success modal, cancel guard, hide button when already hired, isLocked guards (disabled + modal-doesn't-open)
- **fire flow** (4) — more-menu dropdown, fire-confirm modal, "type FIRE to enable" gating, success modal
- **chat-redirect** (1) — hired-agent startChat navigates with agent_id
- **escape state machine** (5) — closes more-menu / confirm-hire / hire-success / fire-confirm; non-Escape ignored
- **syncing modal** (1) — visibility flag
- **has_update badge** (2) — New badge + "Updating…" label

## Test plan
- [x] `npx vitest run tests/unit/app/agents-manager/AgentsManagerClient.unit.spec.tsx` — 28/28 pass locally
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit:coverage` — file lines 56.33% → 85.21%
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [10] 5eef4d42
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T17:33:44Z
- **SHA**: 5eef4d42fb3bd1de9e65463205e4e943e9b6bebc
- **PR**: #1645

### Commit Message

```
test(web): hook tests — useBatchGrant + useChatReplayShare (Phase 2 PR-F) (#1645)

## Summary

Two renderHook-based specs covering previously-uncovered hooks — **Phase
2 PR-F** of the 71% → 78% coverage roadmap. (Originally planned as a
triplet with MMAttachments; that one rolls to follow-up — Mattermost SDK
mock surface is heavy and warrants its own PR.)

## Coverage delta (measured locally 2026-05-14)

**File-level**

| file | before | after | delta |
|---|---|---|---|
| useBatchGrant.ts | 22% (22/101) | **99%** (100/101) | +77pp |
| useChatReplayShare.ts | 0% (0/61) | **100%** (61/61) | +100pp |

**Global** (vs Phase-1 baseline of 72.69% lines)

| metric | before | after | delta |
|---|---|---|---|
| lines | 72.69% | **73.45%** | +0.76pp |

## What it covers

### useBatchGrant.unit.spec.ts (16 tests)

Admin batch credit-grant orchestration:
- **initial state** (2) — modal closed / progress empty / defaults
- **modal lifecycle** (3) — open seeds pending progress, close clears
state when not running, "stopping" toast + stays open when in-flight
- **runBatchGrant happy path** (4) — success / failure / Error rejection
/ non-Error rejection paths
- **guard rails** (3) — admin uid missing, invalid amount, zero/negative
- **pause/resume/retry** (4) — pause flag toggle, skips already-success
uids, retry-only-failed re-runs the failed subset, mixed-result toast
formatting

### useChatReplayShare.unit.spec.ts (18 tests)

Chat "share-as-replay" selection state machine + create/revoke:
- **initial state** (2) — disabled, empty selection, no created share;
selectableIds derived from getShareableMessages
- **selection actions** (6) — enter/exit/toggle/selectVisible/clear;
toggle ignores ids outside the selectable set
- **create flow** (5) — guards (no channelId, empty selection);
display-order ids; Error / non-Error rejection paths; creating flag
transitions
- **revoke / dismiss** (4) — revokeCreated updates status, no-op when no
share, captures rejection error; dismissCreatedDialog resets all state

## MMAttachments deferral

The planned third target imports multiple Mattermost SDK pieces
(`fetchMmBlob`, `MmFileMeta`, etc.) and would need a much heavier mock
surface than the two hook tests above. Worth its own follow-up PR.

## Test plan
- [x] `npx vitest run` on both new specs — 34/34 pass locally
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit:coverage` — global lines 72.69% → 73.45%
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Two renderHook-based specs covering previously-uncovered hooks — **Phase 2 PR-F** of the 71% → 78% coverage roadmap. (Originally planned as a triplet with MMAttachments; that one rolls to follow-up — Mattermost SDK mock surface is heavy and warrants its own PR.)

## Coverage delta (measured locally 2026-05-14)

**File-level**

| file | before | after | delta |
|---|---|---|---|
| useBatchGrant.ts | 22% (22/101) | **99%** (100/101) | +77pp |
| useChatReplayShare.ts | 0% (0/61) | **100%** (61/61) | +100pp |

**Global** (vs Phase-1 baseline of 72.69% lines)

| metric | before | after | delta |
|---|---|---|---|
| lines | 72.69% | **73.45%** | +0.76pp |

## What it covers

### useBatchGrant.unit.spec.ts (16 tests)

Admin batch credit-grant orchestration:
- **initial state** (2) — modal closed / progress empty / defaults
- **modal lifecycle** (3) — open seeds pending progress, close clears state when not running, "stopping" toast + stays open when in-flight
- **runBatchGrant happy path** (4) — success / failure / Error rejection / non-Error rejection paths
- **guard rails** (3) — admin uid missing, invalid amount, zero/negative
- **pause/resume/retry** (4) — pause flag toggle, skips already-success uids, retry-only-failed re-runs the failed subset, mixed-result toast formatting

### useChatReplayShare.unit.spec.ts (18 tests)

Chat "share-as-replay" selection state machine + create/revoke:
- **initial state** (2) — disabled, empty selection, no created share; selectableIds derived from getShareableMessages
- **selection actions** (6) — enter/exit/toggle/selectVisible/clear; toggle ignores ids outside the selectable set
- **create flow** (5) — guards (no channelId, empty selection); display-order ids; Error / non-Error rejection paths; creating flag transitions
- **revoke / dismiss** (4) — revokeCreated updates status, no-op when no share, captures rejection error; dismissCreatedDialog resets all state

## MMAttachments deferral

The planned third target imports multiple Mattermost SDK pieces (`fetchMmBlob`, `MmFileMeta`, etc.) and would need a much heavier mock surface than the two hook tests above. Worth its own follow-up PR.

## Test plan
- [x] `npx vitest run` on both new specs — 34/34 pass locally
- [x] `pnpm lint` — clean
- [x] `pnpm test:unit:coverage` — global lines 72.69% → 73.45%
- [ ] CI `web-quality / lint-and-typecheck` + `web-quality / test` pass

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [11] 683bdf84
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T17:32:05Z
- **SHA**: 683bdf84a8bc59a8d66dda4f7f9edd19d433dcba
- **PR**: #1646

### Commit Message

```
refactor(web): RQ v2 PR-f3 — UploadsFeed switches to useInfiniteQuery (#1646)

## Summary

Migrates \`[locale]/assets/components/UploadsFeed\` from the imperative
\`useState + useRef(offset) + fetchAssets()\` pagination loop onto
\`useInfiniteQuery\`. Largest single migration in the v2 spec —
pagination + agent filter + retry + agents-dropdown derived state, all
in one file.

### New domain

- \`src/hooks/queries/assets/keys.ts\` with \`assetsKeys.list(authToken,
agentFilter)\`. Token-scoped (mirrors \`openclawKeys.agents\` / PR-f2's
\`sessionsKeys.archived\`); filter included so each \`agentId\` value
addresses its own paginated bucket.

### Behavior preservation

| Aspect | Pre-RQ | Post-RQ |
|---|---|---|
| Pagination | \`offsetRef.current\` + \`fetchAssets(filter, true)\` |
\`useInfiniteQuery\` + \`fetchNextPage()\` |
| \"Load more\" gate | \`hasMore = list.length >= PAGE_SIZE\` |
\`getNextPageParam\` returns \`undefined\` on short page |
| Agent filter | imperative refetch on change | queryKey-driven bucket
swap |
| Retry | \`<button onClick={fetchAssets}>\` | \`<button
onClick={feedQuery.refetch}>\` |
| Agents dropdown | derived once per 'all'-filter load | derived via
small \`useEffect\` from the 'all' bucket's pages |
| Retry count | none (single attempt) | \`retry: false\` override
(without it, app-wide \`retry: 1\` would double calls) |

### Tests (new file, 12 tests)

UploadsFeed had no prior test. Coverage:
- auth gating (logged-out → no API call, empty state)
- initial load + agents dropdown derivation
- empty state
- pagination: full-page → \"Load more\" visible; short page → hidden;
click → offset advances + pages concatenate
- filter change: new bucket fetched with \`agentId\` param, dropdown
preserved
- error banner + retry button
- production-default safeguard: \`retry: false\` override beats client
\`retry: 1\` (same pattern as PR-f2 ChangelogClient round 3)
- image preview modal opens

### Drive-by

- Stale comment in \`DiaryCards.unit.spec.tsx\` (flagged in PR-f2 #1638
review): \`enabled: !!uid\` → \`enabled: !!access_token\` to match
round-3 token-gating.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm vitest run
tests/unit/app/assets/UploadsFeed.unit.spec.tsx\` — 12/12
- [x] \`pnpm vitest run
tests/unit/components/settings/DiaryCards.unit.spec.tsx\` — 19/19
(drive-by safe)
- [x] Verify-first: stash component change, rerun → 11/12 pass (behavior
preserved), 1 fail (new auth-gating contract); pop → 12/12
- [ ] CI: \`code-quality / lint-and-test\` green

## Part of

React Query migration v2 — see
\`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Migrates \`[locale]/assets/components/UploadsFeed\` from the imperative \`useState + useRef(offset) + fetchAssets()\` pagination loop onto \`useInfiniteQuery\`. Largest single migration in the v2 spec — pagination + agent filter + retry + agents-dropdown derived state, all in one file.

### New domain

- \`src/hooks/queries/assets/keys.ts\` with \`assetsKeys.list(authToken, agentFilter)\`. Token-scoped (mirrors \`openclawKeys.agents\` / PR-f2's \`sessionsKeys.archived\`); filter included so each \`agentId\` value addresses its own paginated bucket.

### Behavior preservation

| Aspect | Pre-RQ | Post-RQ |
|---|---|---|
| Pagination | \`offsetRef.current\` + \`fetchAssets(filter, true)\` | \`useInfiniteQuery\` + \`fetchNextPage()\` |
| \"Load more\" gate | \`hasMore = list.length >= PAGE_SIZE\` | \`getNextPageParam\` returns \`undefined\` on short page |
| Agent filter | imperative refetch on change | queryKey-driven bucket swap |
| Retry | \`<button onClick={fetchAssets}>\` | \`<button onClick={feedQuery.refetch}>\` |
| Agents dropdown | derived once per 'all'-filter load | derived via small \`useEffect\` from the 'all' bucket's pages |
| Retry count | none (single attempt) | \`retry: false\` override (without it, app-wide \`retry: 1\` would double calls) |

### Tests (new file, 12 tests)

UploadsFeed had no prior test. Coverage:
- auth gating (logged-out → no API call, empty state)
- initial load + agents dropdown derivation
- empty state
- pagination: full-page → \"Load more\" visible; short page → hidden; click → offset advances + pages concatenate
- filter change: new bucket fetched with \`agentId\` param, dropdown preserved
- error banner + retry button
- production-default safeguard: \`retry: false\` override beats client \`retry: 1\` (same pattern as PR-f2 ChangelogClient round 3)
- image preview modal opens

### Drive-by

- Stale comment in \`DiaryCards.unit.spec.tsx\` (flagged in PR-f2 #1638 review): \`enabled: !!uid\` → \`enabled: !!access_token\` to match round-3 token-gating.

## Test plan

- [x] \`npx tsc --noEmit\` clean
- [x] \`pnpm lint\` clean
- [x] \`pnpm vitest run tests/unit/app/assets/UploadsFeed.unit.spec.tsx\` — 12/12
- [x] \`pnpm vitest run tests/unit/components/settings/DiaryCards.unit.spec.tsx\` — 19/19 (drive-by safe)
- [x] Verify-first: stash component change, rerun → 11/12 pass (behavior preserved), 1 fail (new auth-gating contract); pop → 12/12
- [ ] CI: \`code-quality / lint-and-test\` green

## Part of

React Query migration v2 — see \`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [12] b3c5e75a
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T16:31:53Z
- **SHA**: b3c5e75a3626ee7b115c082dcfb6c922073339d4
- **PR**: #1638

### Commit Message

```
refactor(web): RQ v2 PR-f2 — ChangelogClient + DiaryCards switch to useQuery (#1638)

## Summary

Bundles two trivial wrapper-bound `useEffect + setState` fetchers onto
React Query. Both are single-fetch, non-paginated consumers — the
simplest migration shape in the spec.

### ChangelogClient (`/[locale]/changelog`)

- Adds `openclawKeys.releases(authToken)` to the existing openclaw
domain.
- Drops the `mounted` flag — RQ handles unmount safely.
- Same empty-on-failure UX (admin endpoint 401s for non-admin viewers →
`data ?? []` → empty state).
- **New test file** (4 tests): loading / populated / empty / rejected
paths. No prior test existed for this file.

### DiaryCards (`settings.diary`)

- New `src/hooks/queries/sessions/` domain with
`sessionsKeys.archived(uid)`. uid-scoped because the backend resolves
the caller from the auth header — different accounts must not share the
cache bucket.
- Sort + slice-to-10 moved into the queryFn so the cache holds the
shaped payload (no re-sort per render).
- Errors are caught inside the queryFn and return `[]`. Trade-off: RQ
thinks the query \"succeeded\" with empty data, so it caches the empty
result and doesn't retry. Matches the pre-RQ \"empty on failure, no
retry\" UX from #1127. The `logger.warn` contract is preserved (test
still asserts it).
- Test rewrite: `unmount race (cancelled flag)` → `auth gating (RQ
enabled flag)` — the race is gone with RQ's observer, replaced with a
test that confirms `enabled: !!uid` prevents the API call for logged-out
renders.

### Domain split rationale

| File | Domain | Key shape | Reason |
|---|---|---|---|
| ChangelogClient | `openclaw` (existing) | `releases(authToken)` | API
lives in `openclaw-releases.ts`; consistent with siblings |
| DiaryCards | `sessions` (new) | `archived(uid)` | First
session-related query; future `getArchivedSessionHistory` etc. land here
too |

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `pnpm vitest run
tests/unit/components/settings/DiaryCards.unit.spec.tsx` — 19/19
- [x] `pnpm vitest run
tests/unit/app/changelog/ChangelogClient.unit.spec.tsx` — 4/4 (new file)
- [x] Verify-first: stash source changes, rerun → 1 test fails (new
\"auth gating\" contract) + 22 still pass (behavior preserved); pop →
23/23 pass
- [ ] CI: \`code-quality / lint-and-test\` green

## Out of scope

- **UploadsFeed** — deferred to PR-f3. The pagination + agent filter +
retry + blob cache shape is closer to PR-d1's \`useInfiniteQuery\` than
a trivial single-fetch case.
- **CronClient** — deferred to PR-f4. 522 lines, multi-mutation.

## Part of

React Query migration v2 — see
\`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Bundles two trivial wrapper-bound `useEffect + setState` fetchers onto React Query. Both are single-fetch, non-paginated consumers — the simplest migration shape in the spec.

### ChangelogClient (`/[locale]/changelog`)

- Adds `openclawKeys.releases(authToken)` to the existing openclaw domain.
- Drops the `mounted` flag — RQ handles unmount safely.
- Same empty-on-failure UX (admin endpoint 401s for non-admin viewers → `data ?? []` → empty state).
- **New test file** (4 tests): loading / populated / empty / rejected paths. No prior test existed for this file.

### DiaryCards (`settings.diary`)

- New `src/hooks/queries/sessions/` domain with `sessionsKeys.archived(uid)`. uid-scoped because the backend resolves the caller from the auth header — different accounts must not share the cache bucket.
- Sort + slice-to-10 moved into the queryFn so the cache holds the shaped payload (no re-sort per render).
- Errors are caught inside the queryFn and return `[]`. Trade-off: RQ thinks the query \"succeeded\" with empty data, so it caches the empty result and doesn't retry. Matches the pre-RQ \"empty on failure, no retry\" UX from #1127. The `logger.warn` contract is preserved (test still asserts it).
- Test rewrite: `unmount race (cancelled flag)` → `auth gating (RQ enabled flag)` — the race is gone with RQ's observer, replaced with a test that confirms `enabled: !!uid` prevents the API call for logged-out renders.

### Domain split rationale

| File | Domain | Key shape | Reason |
|---|---|---|---|
| ChangelogClient | `openclaw` (existing) | `releases(authToken)` | API lives in `openclaw-releases.ts`; consistent with siblings |
| DiaryCards | `sessions` (new) | `archived(uid)` | First session-related query; future `getArchivedSessionHistory` etc. land here too |

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `pnpm vitest run tests/unit/components/settings/DiaryCards.unit.spec.tsx` — 19/19
- [x] `pnpm vitest run tests/unit/app/changelog/ChangelogClient.unit.spec.tsx` — 4/4 (new file)
- [x] Verify-first: stash source changes, rerun → 1 test fails (new \"auth gating\" contract) + 22 still pass (behavior preserved); pop → 23/23 pass
- [ ] CI: \`code-quality / lint-and-test\` green

## Out of scope

- **UploadsFeed** — deferred to PR-f3. The pagination + agent filter + retry + blob cache shape is closer to PR-d1's \`useInfiniteQuery\` than a trivial single-fetch case.
- **CronClient** — deferred to PR-f4. 522 lines, multi-mutation.

## Part of

React Query migration v2 — see \`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [13] 5ccca5f1
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T16:11:27Z
- **SHA**: 5ccca5f1b98740c70063429d919739578eac411c
- **PR**: #1636

### Commit Message

```
chore(web): expand local mock backend with session + user + lint gate (#1636)

## 概要

`web/scripts/mock-backend.mjs` 扩展计划的 **PR 1 / 3**。把 #1626 引入的
skills-store 流程 mock(7 个 endpoint)扩展到覆盖 **Session + User 共 ~20 个
endpoint**,并把 mock-backend.mjs 纳入 `pnpm lint` gate。目标:让大部分非 admin
前端页面可以本地纯前端运行,不用启 Python backend stack。

后续:
- PR 2 → Admin 域(users/list, gift-codes, invite-codes,
subscription-codes, orders)
- PR 3 → Chat SSE (`/session/chat/subscribe`) + `web/CLAUDE.md` "Local
mock backend" 章节扩写

## 改动

### `web/scripts/mock-backend.mjs` (+485 / -128)

**Helper 抽象**
- `route(method, pathOrPred, handle)` factory 替代 `{ match, handle }` 字面量
- `paginate(list, url)` 处理标准 `?limit&offset` list endpoint
- `urlOf(req)` 减少 `new URL(...)` 噪声

**State 集中**
所有 in-memory 可变状态收敛到文件头一个 `state` object,跨 handler 共享:
- `state.user` — 当前 mock user(profile + billing 字段全集)
- `state.sessions` — 会话列表
- `state.chatMessages` — sessionId → 消息历史
- `state.canvasState` — sessionId → { nodes, edges, viewport, version }
- `state.giftCodes` / `orders` / `creditUsage`
- `state.installedRuntimeSkills`(蓝本已有,保留)

**Mutation 真改 state** — end-to-end 验证 React Query `invalidateQueries`:
- `POST /gift-code/redeem` 改 `state.user.available_credits` +
`state.giftCodes[].current_activations`
- `POST /session/create` 推入 `state.sessions`,`GET /session/list` 立刻反映
- `POST /session/canvas/save` 自增 `version`,`load` 读到最新
- `POST /session/chat` (record) 推入 `state.chatMessages[sessionId]`

**新覆盖 endpoint**

Session (11):
\`\`\`
POST /session/create               | GET  /session/list
GET  /session/get                  | POST /session/update
POST /session/chat (record path)   | GET  /session/chat/get
POST /session/chat/terminate       | GET  /session/canvas/load
POST /session/canvas/save          | GET  /session/archived/list
GET  /session/archived/history
\`\`\`

User (9):
\`\`\`
GET  /users/get / /users/info       | GET  /users/credits
GET  /users/credits/usage           | GET  /users/invite-status
POST /users/bind-invite-code        | POST /users/subscription/update
POST /subscription/cancel           | POST /subscription/downgrade
GET  /orders/list                   | POST /gift-code/redeem
\`\`\`

### Lint gate

- `web/package.json:27` `lint` script 显式加
`scripts/mock-backend.mjs`(精确文件路径,不展开 `scripts/`,避免拉进存量 .js 工具脚本的违规)
- `web/eslint.config.mjs:106` 现有 `scripts/**/*.js` no-console 豁免 glob 扩到
`{js,mjs}` —— 给 dev-tool 的反向发现 `console.log` 留出口,**未使用 `/*
eslint-disable */` inline**

## Test plan

- [x] `pnpm lint` 通过(0 error, 0 warning)
- [x] `node scripts/mock-backend.mjs` 启动无报错
- [x] curl 验证:
  - [x] `/users/me`, `/users/credits` 返回正确 shape
  - [x] `/session/create` → push 到 list,`/session/list` 反映新会话
- [x] `/gift-code/redeem MOCKGIFT100` 后 `/users/credits` 显示 9750 →
9850(state 共享 ✓)
- [x] `/session/canvas/save` → `/session/canvas/load` round-trip,version
自增
  - [x] catch-all `/unhandled/path` 返 200 `{}` + log
- [ ] 浏览器手测(merge 前依赖 reviewer 或后续验收):
- [ ] 配 `.env.local` `NEXT_PUBLIC_ACCOUNT_URL=http://localhost:8000` +
localStorage 注入 mock token
  - [ ] 访问会话列表页 / 用户页 / 兑换码页能渲染

## 不在 scope

- Admin 域 endpoints(PR 2)
- Chat SSE 流式(PR 3)
- LiteLLM / Stripe / Antom webhook
- `web/CLAUDE.md` "Local mock backend" 章节扩写(PR 3 跟 SSE 一起更新)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## 概要

`web/scripts/mock-backend.mjs` 扩展计划的 **PR 1 / 3**。把 #1626 引入的 skills-store 流程 mock(7 个 endpoint)扩展到覆盖 **Session + User 共 ~20 个 endpoint**,并把 mock-backend.mjs 纳入 `pnpm lint` gate。目标:让大部分非 admin 前端页面可以本地纯前端运行,不用启 Python backend stack。

后续:
- PR 2 → Admin 域(users/list, gift-codes, invite-codes, subscription-codes, orders)
- PR 3 → Chat SSE (`/session/chat/subscribe`) + `web/CLAUDE.md` "Local mock backend" 章节扩写

## 改动

### `web/scripts/mock-backend.mjs` (+485 / -128)

**Helper 抽象**
- `route(method, pathOrPred, handle)` factory 替代 `{ match, handle }` 字面量
- `paginate(list, url)` 处理标准 `?limit&offset` list endpoint
- `urlOf(req)` 减少 `new URL(...)` 噪声

**State 集中**
所有 in-memory 可变状态收敛到文件头一个 `state` object,跨 handler 共享:
- `state.user` — 当前 mock user(profile + billing 字段全集)
- `state.sessions` — 会话列表
- `state.chatMessages` — sessionId → 消息历史
- `state.canvasState` — sessionId → { nodes, edges, viewport, version }
- `state.giftCodes` / `orders` / `creditUsage`
- `state.installedRuntimeSkills`(蓝本已有,保留)

**Mutation 真改 state** — end-to-end 验证 React Query `invalidateQueries`:
- `POST /gift-code/redeem` 改 `state.user.available_credits` + `state.giftCodes[].current_activations`
- `POST /session/create` 推入 `state.sessions`,`GET /session/list` 立刻反映
- `POST /session/canvas/save` 自增 `version`,`load` 读到最新
- `POST /session/chat` (record) 推入 `state.chatMessages[sessionId]`

**新覆盖 endpoint**

Session (11):
\`\`\`
POST /session/create               | GET  /session/list
GET  /session/get                  | POST /session/update
POST /session/chat (record path)   | GET  /session/chat/get
POST /session/chat/terminate       | GET  /session/canvas/load
POST /session/canvas/save          | GET  /session/archived/list
GET  /session/archived/history
\`\`\`

User (9):
\`\`\`
GET  /users/get / /users/info       | GET  /users/credits
GET  /users/credits/usage           | GET  /users/invite-status
POST /users/bind-invite-code        | POST /users/subscription/update
POST /subscription/cancel           | POST /subscription/downgrade
GET  /orders/list                   | POST /gift-code/redeem
\`\`\`

### Lint gate

- `web/package.json:27` `lint` script 显式加 `scripts/mock-backend.mjs`(精确文件路径,不展开 `scripts/`,避免拉进存量 .js 工具脚本的违规)
- `web/eslint.config.mjs:106` 现有 `scripts/**/*.js` no-console 豁免 glob 扩到 `{js,mjs}` —— 给 dev-tool 的反向发现 `console.log` 留出口,**未使用 `/* eslint-disable */` inline**

## Test plan

- [x] `pnpm lint` 通过(0 error, 0 warning)
- [x] `node scripts/mock-backend.mjs` 启动无报错
- [x] curl 验证:
  - [x] `/users/me`, `/users/credits` 返回正确 shape
  - [x] `/session/create` → push 到 list,`/session/list` 反映新会话
  - [x] `/gift-code/redeem MOCKGIFT100` 后 `/users/credits` 显示 9750 → 9850(state 共享 ✓)
  - [x] `/session/canvas/save` → `/session/canvas/load` round-trip,version 自增
  - [x] catch-all `/unhandled/path` 返 200 `{}` + log
- [ ] 浏览器手测(merge 前依赖 reviewer 或后续验收):
  - [ ] 配 `.env.local` `NEXT_PUBLIC_ACCOUNT_URL=http://localhost:8000` + localStorage 注入 mock token
  - [ ] 访问会话列表页 / 用户页 / 兑换码页能渲染

## 不在 scope

- Admin 域 endpoints(PR 2)
- Chat SSE 流式(PR 3)
- LiteLLM / Stripe / Antom webhook
- `web/CLAUDE.md` "Local mock backend" 章节扩写(PR 3 跟 SSE 一起更新)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [14] f063cc06
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T15:40:25Z
- **SHA**: f063cc060ed1968c754631e34dfca06a00f80981
- **PR**: #1635

### Commit Message

```
chore(web): exclude legacy GenClawClient from coverage scope (#1635)

## Summary

GenClawClient is the class component holdout flagged in `web/CLAUDE.md`
as `legacy class holdouts: ErrorBoundary, chat/GenClawClient`. Its
runtime stack — `AssistantRuntimeProvider` + WebSocket + Mattermost SDK
— is jsdom-incompatible. End-to-end coverage already lives in 7 E2E
specs (`chat-smoke` / `chat-lifecycle` / `chat-streaming` /
`chat-actions` / `chat-errors` / `chat-subagent` / `mini-chat-embed`).
Keeping it in unit-coverage scope only depresses the percentage without
adding unit-test signal.

This is **Phase 1** of a planned 6-7 PR series to lift web unit-test
coverage from 71.37% → 78%+ (plan revised down from original 90% target
after measuring real v8 executable-line baseline). See plan note at the
bottom.

## Coverage delta (measured locally 2026-05-14)

| metric | before | after | delta |
|---|---|---|---|
| lines | 71.37% (13398/18771) | **72.69%** (13331/18338) | +1.32pp |
| statements | 69.53% | 70.84% | +1.31pp |
| functions | 68.17% | 69.71% | +1.54pp |
| branches | 63.40% | 65.10% | +1.70pp |

All metrics remain above existing thresholds (`lines 69 / statements 68
/ functions 65 / branches 61`), so **no threshold change in this PR**. A
threshold ratchet will follow as a separate PR after the planned
expansion lands.

## Why not also exclude `src/locales/**` / `userguide-*.ts` /
`CronClient.tsx`?

These were initially considered but ruled out after measuring real v8
coverage:

- **`src/locales/*.ts`**: each file is a single `export const en = {...}
as const`. v8 sees it as 1 executable line, hit by any importer →
already 100% covered. Excluding would shift indicator by ~0pp.
- **`userguide-css.ts` / `userguide-html.ts`**: 1-2 executable lines
each, same story.
- **`CronClient.tsx`**: already **90.36% covered** (197/218 lines) after
the #520-#571 6-PR refactor extracted business logic into
`cronHelpers.ts`. Excluding would *lower* the indicator by removing
already-covered lines.

GenClawClient is the only candidate where exclusion both has a real
effect and rests on an independent justification (legacy class holdout +
jsdom-incompatible deps + already E2E-covered).

## Test plan
- [x] `pnpm test:unit:coverage --coverage.reportOnFailure` locally —
coverage report generated, GenClawClient.tsx no longer appears in
`coverage-summary.json`
- [x] All four threshold metrics still pass after exclude
- [ ] CI `code-quality / lint-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

GenClawClient is the class component holdout flagged in `web/CLAUDE.md` as `legacy class holdouts: ErrorBoundary, chat/GenClawClient`. Its runtime stack — `AssistantRuntimeProvider` + WebSocket + Mattermost SDK — is jsdom-incompatible. End-to-end coverage already lives in 7 E2E specs (`chat-smoke` / `chat-lifecycle` / `chat-streaming` / `chat-actions` / `chat-errors` / `chat-subagent` / `mini-chat-embed`). Keeping it in unit-coverage scope only depresses the percentage without adding unit-test signal.

This is **Phase 1** of a planned 6-7 PR series to lift web unit-test coverage from 71.37% → 78%+ (plan revised down from original 90% target after measuring real v8 executable-line baseline). See plan note at the bottom.

## Coverage delta (measured locally 2026-05-14)

| metric | before | after | delta |
|---|---|---|---|
| lines | 71.37% (13398/18771) | **72.69%** (13331/18338) | +1.32pp |
| statements | 69.53% | 70.84% | +1.31pp |
| functions | 68.17% | 69.71% | +1.54pp |
| branches | 63.40% | 65.10% | +1.70pp |

All metrics remain above existing thresholds (`lines 69 / statements 68 / functions 65 / branches 61`), so **no threshold change in this PR**. A threshold ratchet will follow as a separate PR after the planned expansion lands.

## Why not also exclude `src/locales/**` / `userguide-*.ts` / `CronClient.tsx`?

These were initially considered but ruled out after measuring real v8 coverage:

- **`src/locales/*.ts`**: each file is a single `export const en = {...} as const`. v8 sees it as 1 executable line, hit by any importer → already 100% covered. Excluding would shift indicator by ~0pp.
- **`userguide-css.ts` / `userguide-html.ts`**: 1-2 executable lines each, same story.
- **`CronClient.tsx`**: already **90.36% covered** (197/218 lines) after the #520-#571 6-PR refactor extracted business logic into `cronHelpers.ts`. Excluding would *lower* the indicator by removing already-covered lines.

GenClawClient is the only candidate where exclusion both has a real effect and rests on an independent justification (legacy class holdout + jsdom-incompatible deps + already E2E-covered).

## Test plan
- [x] `pnpm test:unit:coverage --coverage.reportOnFailure` locally — coverage report generated, GenClawClient.tsx no longer appears in `coverage-summary.json`
- [x] All four threshold metrics still pass after exclude
- [ ] CI `code-quality / lint-and-test` passes

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [15] f8077bd1
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T15:30:58Z
- **SHA**: f8077bd18e09a5ba6a762053a9797e01b9c87bfc
- **PR**: #1637

### Commit Message

```
refactor(web): RQ v2 PR-f1 — AgentDetailClient reuses useOfficialAgentCatalog (#1637)

## Summary

Migrates `[locale]/agents-manager/[id]/AgentDetailClient` off the
wrapper-bound `useEffect + setAgent(null)` + `mounted` guard onto a
synchronous `useMemo` derivation off `useOfficialAgentCatalog().items` —
the RQ hook PR-b1 already established around the same
`getOpenClawAgentCatalog({ scope: 'official' })` endpoint.

**Zero new infrastructure** — uses the existing hook, cache key
(`openclawKeys.agentCatalogOfficial`), and storage-event mirror. No new
`queries/<domain>/keys.ts`, no new queryFn, no new mutation. The detail
page becomes a pure consumer of an already-cached query.

### Behavior delta

| Scenario | Before | After |
|---|---|---|
| Cold mount, no warm cache | Spinner → fetch → render | Spinner
(items=[] from initialData) → fetch → render |
| Cross-page nav from agents-manager hub | Refetch on every entry |
Instant render from shared RQ cache |
| Cross-tab catalog update / storage event | Stale until reload |
Auto-reflects (hook already wires storage event → setQueryData) |

The cold-start spinner is unchanged: the hook returns `items=[]` and
`useMemo` derives `agent=null`, which the component renders as
`common.loading` — same code path as pre-RQ. Tests verify both
directions.

### Test changes

- **Mocking layer moved up**:
`@/lib/api/openclaw.getOpenClawAgentCatalog` →
`@/hooks/useOfficialAgentCatalog`. Tests now set the hook return shape
`{ items, isLoading }` directly instead of resolving a promise.
- **One test removed, one added**: the old `unmount before catalog
resolves → mounted guard prevents setAgent` test guarded a race that no
longer exists (synchronous `useMemo` derivation has no unmount window).
Replaced with `catalog populates after mount → hero renders on
re-render` — the equivalent invariant for the new flow.
- **32/32 tests pass**. Verify-first: 29/32 fail when component change
is reverted.

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `pnpm vitest run
tests/unit/app/agents-manager/AgentDetailClient.unit.spec.tsx` — 32/32
- [x] `pnpm vitest run
tests/unit/hooks/useOfficialAgentCatalog.unit.spec.ts` — 10/10 (no hook
changes)
- [x] Verify-first: stash component change, rerun → 29/32 fail; pop,
rerun → 32/32 pass
- [ ] CI: `code-quality / lint-and-test` green

## Part of

React Query migration v2 — see
`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

Migrates `[locale]/agents-manager/[id]/AgentDetailClient` off the wrapper-bound `useEffect + setAgent(null)` + `mounted` guard onto a synchronous `useMemo` derivation off `useOfficialAgentCatalog().items` — the RQ hook PR-b1 already established around the same `getOpenClawAgentCatalog({ scope: 'official' })` endpoint.

**Zero new infrastructure** — uses the existing hook, cache key (`openclawKeys.agentCatalogOfficial`), and storage-event mirror. No new `queries/<domain>/keys.ts`, no new queryFn, no new mutation. The detail page becomes a pure consumer of an already-cached query.

### Behavior delta

| Scenario | Before | After |
|---|---|---|
| Cold mount, no warm cache | Spinner → fetch → render | Spinner (items=[] from initialData) → fetch → render |
| Cross-page nav from agents-manager hub | Refetch on every entry | Instant render from shared RQ cache |
| Cross-tab catalog update / storage event | Stale until reload | Auto-reflects (hook already wires storage event → setQueryData) |

The cold-start spinner is unchanged: the hook returns `items=[]` and `useMemo` derives `agent=null`, which the component renders as `common.loading` — same code path as pre-RQ. Tests verify both directions.

### Test changes

- **Mocking layer moved up**: `@/lib/api/openclaw.getOpenClawAgentCatalog` → `@/hooks/useOfficialAgentCatalog`. Tests now set the hook return shape `{ items, isLoading }` directly instead of resolving a promise.
- **One test removed, one added**: the old `unmount before catalog resolves → mounted guard prevents setAgent` test guarded a race that no longer exists (synchronous `useMemo` derivation has no unmount window). Replaced with `catalog populates after mount → hero renders on re-render` — the equivalent invariant for the new flow.
- **32/32 tests pass**. Verify-first: 29/32 fail when component change is reverted.

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `pnpm vitest run tests/unit/app/agents-manager/AgentDetailClient.unit.spec.tsx` — 32/32
- [x] `pnpm vitest run tests/unit/hooks/useOfficialAgentCatalog.unit.spec.ts` — 10/10 (no hook changes)
- [x] Verify-first: stash component change, rerun → 29/32 fail; pop, rerun → 32/32 pass
- [ ] CI: `code-quality / lint-and-test` green

## Part of

React Query migration v2 — see `docs/superpowers/specs/2026-04-25-react-query-migration-v2.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [16] d82918ca
- **Author**: bill-srp
- **Date**: 2026-05-14T14:29:10Z
- **SHA**: d82918ca87371403f567811135b5a558078623ff
- **PR**: #1633

### Commit Message

```
feat(web): Show date prefix on chat timestamps not from today (#1633)

## Summary

- `formatMessageTime` now renders `HH:MM` for messages sent today and
`MMM D, HH:MM` for messages from any other day, locale-aware via `Intl`.
- Extracted the previously-duplicated helper out of
`OpenClawUserMessage` and `OpenClawAssistantMessage` into
`web/src/app/[locale]/chat/lib/formatMessageTime.ts`.
- Threaded the app locale (`useLanguage().locale`) into the helper so
the rendered date/time respects the user-selected app locale instead of
the browser's default. E.g. a user with an English browser who picked
Chinese UI now sees `5月10日, 09:05` instead of `May 10, 09:05`.
- Added a focused unit test covering the today / not-today / locale /
seconds-vs-ms branches.

## Test plan

- [x] `pnpm lint` clean
- [x] `tsc --noEmit` clean
- [x] `pnpm test:unit` — all 4599 tests pass (1 todo unrelated)
- [ ] Manual: hover an old chat message — confirm date prefix renders
before the time
- [ ] Manual: switch app locale to `zh` — confirm the date renders in
localized form (`5月10日, ...`)
```

### PR Body

## Summary

- `formatMessageTime` now renders `HH:MM` for messages sent today and `MMM D, HH:MM` for messages from any other day, locale-aware via `Intl`.
- Extracted the previously-duplicated helper out of `OpenClawUserMessage` and `OpenClawAssistantMessage` into `web/src/app/[locale]/chat/lib/formatMessageTime.ts`.
- Threaded the app locale (`useLanguage().locale`) into the helper so the rendered date/time respects the user-selected app locale instead of the browser's default. E.g. a user with an English browser who picked Chinese UI now sees `5月10日, 09:05` instead of `May 10, 09:05`.
- Added a focused unit test covering the today / not-today / locale / seconds-vs-ms branches.

## Test plan

- [x] `pnpm lint` clean
- [x] `tsc --noEmit` clean
- [x] `pnpm test:unit` — all 4599 tests pass (1 todo unrelated)
- [ ] Manual: hover an old chat message — confirm date prefix renders before the time
- [ ] Manual: switch app locale to `zh` — confirm the date renders in localized form (`5月10日, ...`)

---
## [17] 7df24aba
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T14:20:17Z
- **SHA**: 7df24abaee68586766030bd1d62736644601586a
- **PR**: #1632

### Commit Message

```
refactor(web): RQ v2 PR-d2 — SkillDetailClient runtime + community detail switch to RQ (#1632)

## Summary

PR-d2 lands the second half of the spec's "skills" scope.
`SkillDetailClient.tsx` (563 lines) now uses React Query for both read
paths and **shares the runtime cache bucket with `SkillsSearchClient`**
(PR-d1):

- **Runtime skills** → `useQuery` keyed on `skillsKeys.runtime(uid)`
(identical key to PR-d1 → search ↔ detail navigation is a cache hit)
- **Community detail** → `useQuery` keyed on
`skillsKeys.communityDetail(slug)` (the stub PR-d1 created), seeded from
`readCachedCommunitySkillDetail`
- **`detail` + `isLoading`** are now derived (`useMemo`) instead of
`setDetail` from inside two effects
- **Install/uninstall mutations** invalidate the **shared** runtime key
so the search page picks up the install state without a manual reload

## Pattern checklist (carried over from PR-a / b / c / d1)

- [x] `refetchOnMount: 'always'` on both queries
- [x] `cancelQueries` before mutation-triggered invalidate
- [x] uid-scoped runtime key (shared with d1)
- [x] error derived from `query.isError`; mutation errors stored
separately and take precedence
- [x] `runtimeSkills` wrapped in `useMemo`, **isError-clamped to `[]`**
(PR-d1 round 2 lesson)

## Stacked on PR-d1

This branch is stacked on `feature/rq-v2-prd1-skills-search` because it
consumes `skillsKeys` from PR-d1's new
`web/src/hooks/queries/skills/keys.ts`. **Once d1 merges to main, this
branch needs a rebase/merge from main** — files are otherwise
file-disjoint.

## Test plan

- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `npx vitest run
tests/unit/app/skills/detail/SkillDetailClient.unit.spec.tsx` — 46/46
pass (45 existing + 1 new spy regression)
- [x] `npx vitest run tests/unit/app/skills` — 104/104 pass (4 files)
- [ ] Smoke: `/skills/community/<slug>` → install from detail modal →
navigate to `/skills/search` → install badge reflects without reload
- [ ] Smoke: `/skills/official/<slug>` and `/skills/builtin/<slug>`
(runtime-only paths, no community fetch)

## Not in scope

- `useAgentInstalledSkills` (per-agent installed-skills hook) still
effect-based — could migrate in a follow-up, currently shared between
search + detail clients
- AbortSignal forwarding to `listRuntimeSkills` /
`getCommunitySkillDetail` — follow-up #1618

Refs: `docs/superpowers/specs/2026-04-25-react-query-migration-v2.md`
PR series: PR-a / b / c1 merged → PR-d1 (in merge queue) → this (PR-d2)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

PR-d2 lands the second half of the spec's "skills" scope. `SkillDetailClient.tsx` (563 lines) now uses React Query for both read paths and **shares the runtime cache bucket with `SkillsSearchClient`** (PR-d1):

- **Runtime skills** → `useQuery` keyed on `skillsKeys.runtime(uid)` (identical key to PR-d1 → search ↔ detail navigation is a cache hit)
- **Community detail** → `useQuery` keyed on `skillsKeys.communityDetail(slug)` (the stub PR-d1 created), seeded from `readCachedCommunitySkillDetail`
- **`detail` + `isLoading`** are now derived (`useMemo`) instead of `setDetail` from inside two effects
- **Install/uninstall mutations** invalidate the **shared** runtime key so the search page picks up the install state without a manual reload

## Pattern checklist (carried over from PR-a / b / c / d1)

- [x] `refetchOnMount: 'always'` on both queries
- [x] `cancelQueries` before mutation-triggered invalidate
- [x] uid-scoped runtime key (shared with d1)
- [x] error derived from `query.isError`; mutation errors stored separately and take precedence
- [x] `runtimeSkills` wrapped in `useMemo`, **isError-clamped to `[]`** (PR-d1 round 2 lesson)

## Stacked on PR-d1

This branch is stacked on `feature/rq-v2-prd1-skills-search` because it consumes `skillsKeys` from PR-d1's new `web/src/hooks/queries/skills/keys.ts`. **Once d1 merges to main, this branch needs a rebase/merge from main** — files are otherwise file-disjoint.

## Test plan

- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `npx vitest run tests/unit/app/skills/detail/SkillDetailClient.unit.spec.tsx` — 46/46 pass (45 existing + 1 new spy regression)
- [x] `npx vitest run tests/unit/app/skills` — 104/104 pass (4 files)
- [ ] Smoke: `/skills/community/<slug>` → install from detail modal → navigate to `/skills/search` → install badge reflects without reload
- [ ] Smoke: `/skills/official/<slug>` and `/skills/builtin/<slug>` (runtime-only paths, no community fetch)

## Not in scope

- `useAgentInstalledSkills` (per-agent installed-skills hook) still effect-based — could migrate in a follow-up, currently shared between search + detail clients
- AbortSignal forwarding to `listRuntimeSkills` / `getCommunitySkillDetail` — follow-up #1618

Refs: `docs/superpowers/specs/2026-04-25-react-query-migration-v2.md`
PR series: PR-a / b / c1 merged → PR-d1 (in merge queue) → this (PR-d2)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [18] bc4cac31
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T14:01:40Z
- **SHA**: bc4cac317eb3cdf31769fe75583f5d8ddc2baf92
- **PR**: #1626

### Commit Message

```
refactor(web): RQ v2 PR-d1 — SkillsSearchClient runtime + community feeds switch to RQ (#1626)

## Summary

- Migrate `SkillsSearchClient` from two ad-hoc `useEffect + useState`
read paths to React Query.
- **Runtime skills** (per-user installed catalog): `useQuery` uid-keyed,
seeds from existing `readCachedRuntimeSkills` localStorage cache via
`initialData`, `refetchOnMount: 'always'`.
- **Community skills** (paginated): `useInfiniteQuery` —
`IntersectionObserver` triggers `fetchNextPage()` instead of
`loadCommunitySkills({ cursor, replace })` setState chain.
- `installSkill` / `uninstallSkill` stay imperative in
`mutateSkillForAgent` but now `await cancelQueries + invalidateQueries`
for the runtime key after the API call.
- New `web/src/hooks/queries/skills/keys.ts` with `runtime(uid)` /
`community(limit)` / `communityDetail(slug)` factories (PR-d2 will
consume the detail key).

## Why this PR is different from spec PR-d

Spec PR-d's "chat 资源面板 + onboarding + skills" candidates audit revealed:

- `useLandingContextFlow` (344 lines) — finite state machine, 5
useEffects are phase transitions, only one API call wrapped in
`hireActiveRef` guard. **Not anti-pattern.**
- `useDeepLinkHireFlow` (310 lines) — sibling state machine. **Not
anti-pattern.**
- `useMattermostIntegration` (366 lines) — file upload + WebSocket +
AbortController state. **Not anti-pattern.**
- `SkillsSearchClient.tsx` (602 lines) — **real** fetch + cache +
paginate + mutations. **This PR.**

This PR jumps to the true anti-pattern; chat hooks are skipped (filed
for a separate decision).

## Pattern checklist (PR-b3 round 6 lessons applied up-front)

- [x] `refetchOnMount: 'always'` on both queries — matches PR-a / b1 /
b2 / b3 / c1
- [x] `cancelQueries` before mutation-triggered invalidate
- [x] uid-scoped queryKey for runtime
- [x] error derived from `query.isError`
- [x] `runtimeSkills` and `communitySkills` wrapped in `useMemo` for
referential stability
- [x] dedup by id when flattening `useInfiniteQuery` pages
(useInfiniteQuery just concatenates page items as-is)

## Test plan

- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `npx vitest run
tests/unit/app/skills/search/SkillsSearchClient.unit.spec.tsx` — 34/34
pass
- [x] `npx vitest run tests/unit/app/skills` — 99/99 pass (4 files)
- [ ] Smoke: `/skills/search` → community tab triggers infinite scroll
- [ ] Smoke: install/uninstall flow from search page (via
SkillAgentManagerModal)
- [ ] Smoke: cross-account uid switch (runtime cache misses + refetch)

## Not in scope

- `SkillDetailClient.tsx` (563 lines, same runtime key + per-slug
detail) — PR-d2
- `useAgentInstalledSkills` — used by both Search and Detail clients,
PR-d2 may share the migration
- AbortSignal forwarding to `listRuntimeSkills` / `listCommunitySkills`
— follow-up #1618
- `useLandingContextFlow` / `useDeepLinkHireFlow` /
`useMattermostIntegration` — not RQ anti-pattern (state machines, not
fetch-and-cache)

Refs: `docs/superpowers/specs/2026-04-25-react-query-migration-v2.md`
PR series: PR-a / b1 / b2 / b3 / c1 merged → this (PR-d1)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

- Migrate `SkillsSearchClient` from two ad-hoc `useEffect + useState` read paths to React Query.
- **Runtime skills** (per-user installed catalog): `useQuery` uid-keyed, seeds from existing `readCachedRuntimeSkills` localStorage cache via `initialData`, `refetchOnMount: 'always'`.
- **Community skills** (paginated): `useInfiniteQuery` — `IntersectionObserver` triggers `fetchNextPage()` instead of `loadCommunitySkills({ cursor, replace })` setState chain.
- `installSkill` / `uninstallSkill` stay imperative in `mutateSkillForAgent` but now `await cancelQueries + invalidateQueries` for the runtime key after the API call.
- New `web/src/hooks/queries/skills/keys.ts` with `runtime(uid)` / `community(limit)` / `communityDetail(slug)` factories (PR-d2 will consume the detail key).

## Why this PR is different from spec PR-d

Spec PR-d's "chat 资源面板 + onboarding + skills" candidates audit revealed:

- `useLandingContextFlow` (344 lines) — finite state machine, 5 useEffects are phase transitions, only one API call wrapped in `hireActiveRef` guard. **Not anti-pattern.**
- `useDeepLinkHireFlow` (310 lines) — sibling state machine. **Not anti-pattern.**
- `useMattermostIntegration` (366 lines) — file upload + WebSocket + AbortController state. **Not anti-pattern.**
- `SkillsSearchClient.tsx` (602 lines) — **real** fetch + cache + paginate + mutations. **This PR.**

This PR jumps to the true anti-pattern; chat hooks are skipped (filed for a separate decision).

## Pattern checklist (PR-b3 round 6 lessons applied up-front)

- [x] `refetchOnMount: 'always'` on both queries — matches PR-a / b1 / b2 / b3 / c1
- [x] `cancelQueries` before mutation-triggered invalidate
- [x] uid-scoped queryKey for runtime
- [x] error derived from `query.isError`
- [x] `runtimeSkills` and `communitySkills` wrapped in `useMemo` for referential stability
- [x] dedup by id when flattening `useInfiniteQuery` pages (useInfiniteQuery just concatenates page items as-is)

## Test plan

- [x] `./node_modules/.bin/tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `npx vitest run tests/unit/app/skills/search/SkillsSearchClient.unit.spec.tsx` — 34/34 pass
- [x] `npx vitest run tests/unit/app/skills` — 99/99 pass (4 files)
- [ ] Smoke: `/skills/search` → community tab triggers infinite scroll
- [ ] Smoke: install/uninstall flow from search page (via SkillAgentManagerModal)
- [ ] Smoke: cross-account uid switch (runtime cache misses + refetch)

## Not in scope

- `SkillDetailClient.tsx` (563 lines, same runtime key + per-slug detail) — PR-d2
- `useAgentInstalledSkills` — used by both Search and Detail clients, PR-d2 may share the migration
- AbortSignal forwarding to `listRuntimeSkills` / `listCommunitySkills` — follow-up #1618
- `useLandingContextFlow` / `useDeepLinkHireFlow` / `useMattermostIntegration` — not RQ anti-pattern (state machines, not fetch-and-cache)

Refs: `docs/superpowers/specs/2026-04-25-react-query-migration-v2.md`
PR series: PR-a / b1 / b2 / b3 / c1 merged → this (PR-d1)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [19] eaf23e78
- **Author**: bill-srp
- **Date**: 2026-05-14T13:59:00Z
- **SHA**: eaf23e78b90758117c8c6665e6facfe3bc44dc0f
- **PR**: #1631

### Commit Message

```
feat(web): large-paste auto-attach + click-to-preview pending chips (#1631)

## Summary

Two related composer features for the Mattermost-backed chat surface:

- **Large pasted text auto-converts to a `.txt` attachment** instead of
being inserted inline. Trigger: `bytes > 5KB || chars >
MM_MAX_MESSAGE_LENGTH (4000)`. The byte rule catches CJK/emoji-heavy
pastes; the char rule catches ASCII pastes that would otherwise hit
Mattermost's send-time length check. Gated by `isFileTypeAccepted` so
canvas's media-only composer falls back to the existing inline behavior
with zero parent-side changes.
- **Pending attachment chips become clickable** for previewable
text-like files (`.txt`, `.md`, `.json`, code) in the existing artifact
sidebar — previously users had no way to inspect content before send.
Implementation extracts `MmPendingAttachmentChip` as a standalone
component, adds a `blob` variant to `PreviewSource` carrying a `revoke`
thunk, and wires a single `useEffect` in `useArtifactsSidebar` that
releases the blob URL on file swap / panel close / unmount.

## Why

- Pasting 6KB+ of code or a CJK article lagged the contentEditable and
only surfaced the 4000-char Mattermost cap as a vague error at send
time.
- Once paste-to-file landed, users had a chip with no way to verify what
was in it before sending.

## Commits

```
chore(web): apply lint autofix to paste-feature tests
refactor(web): tighten paste-feature comments and reuse extFromName
test(web):  cover MmPendingAttachmentChip rendering + click-to-preview
feat(web):  click-to-preview pending Mattermost attachment chips
test(web):  cover paste-to-file branch in RichTextInput
feat(web):  convert large pasted text to .txt attachment
```

## Test plan

- [x] `vitest` — 17 new unit tests for paste-feature, all passing
- [x] `vitest` — 481/481 in the broader chat sweep stays green (no
regressions)
- [x] `tsc --noEmit` — clean
- [x] `next lint` — clean (after autofix)
- [ ] Manual: paste 6KB ASCII into the chat composer → chip appears with
`TXT` badge → click → artifact sidebar renders content → close → confirm
no leaked blob via DevTools Memory
- [ ] Manual: paste 1700 Chinese characters → triggers byte rule → same
flow
- [ ] Manual: paste 4500 ASCII chars → triggers char rule → same flow
- [ ] Manual: in canvas chat panel (`acceptFileTypes="image/*,video/*"`)
paste 6KB text → confirm falls back to inline (not converted), since
`.txt` isn't accepted there
```

### PR Body

## Summary

Two related composer features for the Mattermost-backed chat surface:

- **Large pasted text auto-converts to a `.txt` attachment** instead of being inserted inline. Trigger: `bytes > 5KB || chars > MM_MAX_MESSAGE_LENGTH (4000)`. The byte rule catches CJK/emoji-heavy pastes; the char rule catches ASCII pastes that would otherwise hit Mattermost's send-time length check. Gated by `isFileTypeAccepted` so canvas's media-only composer falls back to the existing inline behavior with zero parent-side changes.
- **Pending attachment chips become clickable** for previewable text-like files (`.txt`, `.md`, `.json`, code) in the existing artifact sidebar — previously users had no way to inspect content before send. Implementation extracts `MmPendingAttachmentChip` as a standalone component, adds a `blob` variant to `PreviewSource` carrying a `revoke` thunk, and wires a single `useEffect` in `useArtifactsSidebar` that releases the blob URL on file swap / panel close / unmount.

## Why

- Pasting 6KB+ of code or a CJK article lagged the contentEditable and only surfaced the 4000-char Mattermost cap as a vague error at send time.
- Once paste-to-file landed, users had a chip with no way to verify what was in it before sending.

## Commits

```
chore(web): apply lint autofix to paste-feature tests
refactor(web): tighten paste-feature comments and reuse extFromName
test(web):  cover MmPendingAttachmentChip rendering + click-to-preview
feat(web):  click-to-preview pending Mattermost attachment chips
test(web):  cover paste-to-file branch in RichTextInput
feat(web):  convert large pasted text to .txt attachment
```

## Test plan

- [x] `vitest` — 17 new unit tests for paste-feature, all passing
- [x] `vitest` — 481/481 in the broader chat sweep stays green (no regressions)
- [x] `tsc --noEmit` — clean
- [x] `next lint` — clean (after autofix)
- [ ] Manual: paste 6KB ASCII into the chat composer → chip appears with `TXT` badge → click → artifact sidebar renders content → close → confirm no leaked blob via DevTools Memory
- [ ] Manual: paste 1700 Chinese characters → triggers byte rule → same flow
- [ ] Manual: paste 4500 ASCII chars → triggers char rule → same flow
- [ ] Manual: in canvas chat panel (`acceptFileTypes="image/*,video/*"`) paste 6KB text → confirm falls back to inline (not converted), since `.txt` isn't accepted there

---
## [20] e07e2b5e
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T13:54:04Z
- **SHA**: e07e2b5efc02cc930fe06d75441da5b28c45feb4
- **PR**: #1630

### Commit Message

```
docs(architecture): add ecap-pm-agent to inventory (EN + 中文) (#1630)

## Summary

- Adds `SerendipityOneInc/ecap-pm-agent` to **Section B** (External
repository inventory) — clarifies it's off the request data path, with
two roles: (1) `apps/pm-agent/` Cloudflare Worker for Linear / Feishu /
GitHub webhook ingest, (2) `design-docs/` as the source of truth for
**Zooclaw** product PRDs + Enterprise V1 PRD + ops design docs, rendered
to a GitHub Pages site via mkdocs.
- Adds it to **Section D** ("not in gcp-foundation" exceptions) —
deployed by its own `deploy.yml` on `ecap-pm-agent-v*-release` tags;
workers `ecap-pm-webhook` / `ecap-pm-webhook-staging`; design-docs site
auto-deploys via `gh-pages.yml`.
- Both EN and 中文 files updated.

The corresponding ecap-pm-agent PR
([SerendipityOneInc/ecap-pm-agent#67](https://github.com/SerendipityOneInc/ecap-pm-agent/pull/67))
adds a **link** to this doc in its design-docs site (mkdocs nav + README
callout) rather than mirroring the file — single source stays here, no
risk of two copies drifting.

## Test plan

- [ ] Read both files end-to-end to confirm new rows / bullets render
cleanly in GitHub Markdown
- [ ] Check Section B table row alignment (long cell)
- [ ] Verify the Section D bullet links back to Section B correctly

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

- Adds `SerendipityOneInc/ecap-pm-agent` to **Section B** (External repository inventory) — clarifies it's off the request data path, with two roles: (1) `apps/pm-agent/` Cloudflare Worker for Linear / Feishu / GitHub webhook ingest, (2) `design-docs/` as the source of truth for **Zooclaw** product PRDs + Enterprise V1 PRD + ops design docs, rendered to a GitHub Pages site via mkdocs.
- Adds it to **Section D** ("not in gcp-foundation" exceptions) — deployed by its own `deploy.yml` on `ecap-pm-agent-v*-release` tags; workers `ecap-pm-webhook` / `ecap-pm-webhook-staging`; design-docs site auto-deploys via `gh-pages.yml`.
- Both EN and 中文 files updated.

The corresponding ecap-pm-agent PR ([SerendipityOneInc/ecap-pm-agent#67](https://github.com/SerendipityOneInc/ecap-pm-agent/pull/67)) adds a **link** to this doc in its design-docs site (mkdocs nav + README callout) rather than mirroring the file — single source stays here, no risk of two copies drifting.

## Test plan

- [ ] Read both files end-to-end to confirm new rows / bullets render cleanly in GitHub Markdown
- [ ] Check Section B table row alignment (long cell)
- [ ] Verify the Section D bullet links back to Section B correctly

---
## [21] 452fee4f
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T11:38:28Z
- **SHA**: 452fee4fb04684d1f2685dafb3ea325d3d1946c1
- **PR**: #1627

### Commit Message

```
docs: add claw-steward to architecture guide (EN + 中文) (#1627)

## Summary
- Document the previously-missing `claw-steward` service in
`architecture.md` and `architecture.zh-CN.md` — it sits parallel to
`fastclaw` as the ops/observability counterpart.
- New Section A subsection **"Ops / observability plane"** with its own
mini mermaid covering the 3-min async probe loop
(`PROBE_INTERVAL_SECONDS=180`), PagerDuty HARD/SOFT thresholds, and the
explicit "no auto-restart" contract.
- New inventory row in Section B (after `fastclaw`); new
deployment-exception bullet in Section D (`build-and-deploy.yml` →
`ghcr.io/serendipityoneinc/claw-steward`; `gcp-foundation` only carries
the MCI ingress patch).
- Roadmap note: future user-session analysis code is planned to live in
`claw-steward` — no such code today (`app/` has no `session/` /
`transcript/` / `analytics/` modules; `mysql-init/` only `CREATE
DATABASE demo`).

Section E (env var → service map) intentionally untouched —
`claw-steward` is not reached via any env var from this repo, so adding
a row would mislead.

## Test plan
- [ ] Render `architecture.md` and `architecture.zh-CN.md` on GitHub and
confirm both mermaid diagrams (main + new ops sub-diagram) render
correctly.
- [ ] Click through the existing in-doc anchors (`#a-architecture`,
`#c-data-flows`, `#e-env-var--service-map` and Chinese equivalents) to
confirm they still resolve.
- [ ] Spot-check EN ↔ 中文 stay symmetric (same three insertions on each
side).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- Document the previously-missing `claw-steward` service in `architecture.md` and `architecture.zh-CN.md` — it sits parallel to `fastclaw` as the ops/observability counterpart.
- New Section A subsection **"Ops / observability plane"** with its own mini mermaid covering the 3-min async probe loop (`PROBE_INTERVAL_SECONDS=180`), PagerDuty HARD/SOFT thresholds, and the explicit "no auto-restart" contract.
- New inventory row in Section B (after `fastclaw`); new deployment-exception bullet in Section D (`build-and-deploy.yml` → `ghcr.io/serendipityoneinc/claw-steward`; `gcp-foundation` only carries the MCI ingress patch).
- Roadmap note: future user-session analysis code is planned to live in `claw-steward` — no such code today (`app/` has no `session/` / `transcript/` / `analytics/` modules; `mysql-init/` only `CREATE DATABASE demo`).

Section E (env var → service map) intentionally untouched — `claw-steward` is not reached via any env var from this repo, so adding a row would mislead.

## Test plan
- [ ] Render `architecture.md` and `architecture.zh-CN.md` on GitHub and confirm both mermaid diagrams (main + new ops sub-diagram) render correctly.
- [ ] Click through the existing in-doc anchors (`#a-architecture`, `#c-data-flows`, `#e-env-var--service-map` and Chinese equivalents) to confirm they still resolve.
- [ ] Spot-check EN ↔ 中文 stay symmetric (same three insertions on each side).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [22] d1d4fb5d
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T10:47:59Z
- **SHA**: d1d4fb5df686e936921ca605b609ed75228e89bc
- **PR**: #1625

### Commit Message

```
docs(architecture): color flowchart for dark/light theme (#1625)

## Summary
- Adds Mermaid `classDef` + `linkStyle` blocks to `architecture.md` and
`architecture.zh-CN.md` so the topology diagram is readable on both
GitHub light and dark themes.
- Color groups follow the conceptual boundaries the doc already uses:
user / this-repo apps / control plane / chat / LLM / billing /
integration / external.
- Fills are Tailwind-600 mid-tones with white text — keeps WCAG AA
contrast on both `#ffffff` (light) and GitHub's `#0d1117` (dark). The
previous pastel palette (merged in #1624) was too bright on dark
backgrounds.
- Two key edges are highlighted via `linkStyle`: the WS chat edges in
saturated amber (matching the `mm` node) and the native `LiteLLM → Lago`
cost-reporting edge in thick emerald.

## Test plan
- [ ] Open `architecture.md` on GitHub web UI — confirm Mermaid renders
with the new colored nodes
- [ ] Toggle GitHub theme between light and dark (top-right user menu)
and confirm:
  - all 8 color groups remain distinguishable
  - white node text stays readable on both backgrounds
- the amber `WS chat` edges and the thick green `LiteLLM → Lago` edge
are visible on both
- [ ] Same checks for `architecture.zh-CN.md`
- [ ] Optional: paste the Mermaid block into https://mermaid.live to
inspect rendering at higher zoom

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- Adds Mermaid `classDef` + `linkStyle` blocks to `architecture.md` and `architecture.zh-CN.md` so the topology diagram is readable on both GitHub light and dark themes.
- Color groups follow the conceptual boundaries the doc already uses: user / this-repo apps / control plane / chat / LLM / billing / integration / external.
- Fills are Tailwind-600 mid-tones with white text — keeps WCAG AA contrast on both `#ffffff` (light) and GitHub's `#0d1117` (dark). The previous pastel palette (merged in #1624) was too bright on dark backgrounds.
- Two key edges are highlighted via `linkStyle`: the WS chat edges in saturated amber (matching the `mm` node) and the native `LiteLLM → Lago` cost-reporting edge in thick emerald.

## Test plan
- [ ] Open `architecture.md` on GitHub web UI — confirm Mermaid renders with the new colored nodes
- [ ] Toggle GitHub theme between light and dark (top-right user menu) and confirm:
  - all 8 color groups remain distinguishable
  - white node text stays readable on both backgrounds
  - the amber `WS chat` edges and the thick green `LiteLLM → Lago` edge are visible on both
- [ ] Same checks for `architecture.zh-CN.md`
- [ ] Optional: paste the Mermaid block into https://mermaid.live to inspect rendering at higher zoom

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [23] 1957a14b
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T10:33:51Z
- **SHA**: 1957a14bd129e465ead843db52ab3504ec2ac86b
- **PR**: #1623

### Commit Message

```
refactor(web): RQ v2 PR-c1 — ConnectorsSection switches status fetch to useQuery (#1623)

## Summary

- Migrate Google Workspace connector status read in `ConnectorsSection`
from `useEffect + useCallback + useState` to `useQuery`. uid-scoped
queryKey via new `web/src/hooks/queries/connectors/keys.ts`.
- 3 imperative mutations (`handleConnect` / `handleDisconnect` /
`handleReconnect`) keep their shape but switch the `await fetchStatus()`
tail to `cancelQueries + refetchQueries` — prevents a stale focus
refetch from landing post-mutation with pre-change data.
- All PR-b1/b2/b3 pattern checklist items applied up-front:
`refetchOnMount: 'always'`, `cancelQueries` before refetch, uid-scoped
key, derived error.

## Why this PR is narrower than spec PR-c

Spec PR-c estimates 10 files / 600-900 lines. I audited
`claw-settings/`'s 18 components for actual RQ anti-pattern (useEffect +
lib/api + setState):

| Component | Lines | Reality | Decision |
|---|---:|---|---|
| **ConnectorsSection** | 426 | 1 read + 3 mutations | **This PR** |
| FeishuSetupModal / WecomSetupModal / WeixinSetupModal | 245-254 each |
start + setInterval poll | Deferred — modal-bound setInterval, no
cross-instance share, RQ marginal value |
| ChannelsSection (1030 lines) | — | useEffect = form-state sync from
`initialData`, no API | Not anti-pattern |
| 14 others | ~2900 | only `import type` from `@/lib/api/*` or pure UI |
Not anti-pattern |

PR-c1 lands the only true anti-pattern in `claw-settings/`. Setup modals
stay imperative (`setInterval` in modal lifecycle is already clean —
RQ's `refetchInterval` with a stop condition would be more code for the
same correctness).

## Pattern checklist (PR-b3 round 6 lessons applied up-front)

- [x] `refetchOnMount: 'always'` — matches PR-a / b1 / b2 / b3
- [x] `cancelQueries` before each mutation's `refetchQueries` —
defensive even though `refetchQueries` would also dedup
- [x] uid-scoped queryKey (cross-account swap = cache miss)
- [x] error derived from `query.error`, not stored; mutation errors
stored separately and take precedence
- [x] `loading = !!uid && query.isPending` — gates against v5's
disabled-pending state

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `npx vitest run
tests/unit/app/claw-settings/ConnectorsSection.unit.spec.tsx` — 27/27
pass
- [x] `npx vitest run tests/unit/app/claw-settings` — 330/330 pass (14
files, full sweep)
- [ ] Smoke: `/claw-settings` → Connectors tab, Connect → OAuth flow,
Disconnect → returns to default state
- [ ] Smoke: Reconnect path (mock `token_stored=true, gog_alive=false`)
- [ ] Smoke: cross-account switch (verify cache miss + fresh fetch on
uid change)

## Not in scope

- Setup modals (Feishu / Wecom / Weixin) — deferred as evaluated above
- `useSendMessage` reads `getCachedCreditsCheck` — see PR-b3 follow-up
#1618
- `lib/api/connectors.ts` AbortSignal forwarding — follow-up #1618 will
cover this whole API surface

Refs: \`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`
PR series: PR-a / b1 / b2 / b3 merged → this (PR-c1)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary

- Migrate Google Workspace connector status read in `ConnectorsSection` from `useEffect + useCallback + useState` to `useQuery`. uid-scoped queryKey via new `web/src/hooks/queries/connectors/keys.ts`.
- 3 imperative mutations (`handleConnect` / `handleDisconnect` / `handleReconnect`) keep their shape but switch the `await fetchStatus()` tail to `cancelQueries + refetchQueries` — prevents a stale focus refetch from landing post-mutation with pre-change data.
- All PR-b1/b2/b3 pattern checklist items applied up-front: `refetchOnMount: 'always'`, `cancelQueries` before refetch, uid-scoped key, derived error.

## Why this PR is narrower than spec PR-c

Spec PR-c estimates 10 files / 600-900 lines. I audited `claw-settings/`'s 18 components for actual RQ anti-pattern (useEffect + lib/api + setState):

| Component | Lines | Reality | Decision |
|---|---:|---|---|
| **ConnectorsSection** | 426 | 1 read + 3 mutations | **This PR** |
| FeishuSetupModal / WecomSetupModal / WeixinSetupModal | 245-254 each | start + setInterval poll | Deferred — modal-bound setInterval, no cross-instance share, RQ marginal value |
| ChannelsSection (1030 lines) | — | useEffect = form-state sync from `initialData`, no API | Not anti-pattern |
| 14 others | ~2900 | only `import type` from `@/lib/api/*` or pure UI | Not anti-pattern |

PR-c1 lands the only true anti-pattern in `claw-settings/`. Setup modals stay imperative (`setInterval` in modal lifecycle is already clean — RQ's `refetchInterval` with a stop condition would be more code for the same correctness).

## Pattern checklist (PR-b3 round 6 lessons applied up-front)

- [x] `refetchOnMount: 'always'` — matches PR-a / b1 / b2 / b3
- [x] `cancelQueries` before each mutation's `refetchQueries` — defensive even though `refetchQueries` would also dedup
- [x] uid-scoped queryKey (cross-account swap = cache miss)
- [x] error derived from `query.error`, not stored; mutation errors stored separately and take precedence
- [x] `loading = !!uid && query.isPending` — gates against v5's disabled-pending state

## Test plan

- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint` clean
- [x] `npx vitest run tests/unit/app/claw-settings/ConnectorsSection.unit.spec.tsx` — 27/27 pass
- [x] `npx vitest run tests/unit/app/claw-settings` — 330/330 pass (14 files, full sweep)
- [ ] Smoke: `/claw-settings` → Connectors tab, Connect → OAuth flow, Disconnect → returns to default state
- [ ] Smoke: Reconnect path (mock `token_stored=true, gog_alive=false`)
- [ ] Smoke: cross-account switch (verify cache miss + fresh fetch on uid change)

## Not in scope

- Setup modals (Feishu / Wecom / Weixin) — deferred as evaluated above
- `useSendMessage` reads `getCachedCreditsCheck` — see PR-b3 follow-up #1618
- `lib/api/connectors.ts` AbortSignal forwarding — follow-up #1618 will cover this whole API surface

Refs: \`docs/superpowers/specs/2026-04-25-react-query-migration-v2.md\`
PR series: PR-a / b1 / b2 / b3 merged → this (PR-c1)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [24] 966741ea
- **Author**: Chris@ZooClaw
- **Date**: 2026-05-14T10:35:43Z
- **SHA**: 966741eaae036aca06312d604d342aab73137282
- **PR**: #1624

### Commit Message

```
docs: add architecture & external dependencies guide (EN + 中文) (#1624)

## Summary
- New `architecture.md` (and Chinese mirror `architecture.zh-CN.md`) at
repo root mapping the runtime topology, external repo inventory, data
flows, deployment source-of-truth, and env-var → service table.
- `AGENTS.md` and `README.md` cross-link to the new doc.
- Notable clarifications surfaced by cross-repo verification
(`fastclaw`, `ecap-proxy-service`, `openclaw-docker`, `gcp-foundation`):
- Mattermost is the chat transport: web ↔ Mattermost server ↔ bot pod;
`claw-interface` is **not** on the chat path, it only provisions
accounts.
- Nango has two access paths: `claw-interface` calls Nango directly for
OAuth/connection management; bot-pod skills call Nango via
`ecap-proxy-service`, which adds per-user auth (Nango itself has no
per-user auth model).
- LiteLLM routing for bot pods is **declarative** (lives in each bot's
`openclaw.json`), not injected via pod env — fastclaw only injects
`BOT_ID`/`BOT_SLUG`/`BOT_TOKEN`/`PUBLIC_BASE_URL`.
- Lago is only ever called via `billing-gateway`; no `services/` code
imports a Lago client.
- `gcp-foundation` is the source of truth for deployed versions, but
**not** everything is there: `billing-gateway` deploys via its own
repo's CI/CD; `ecap-skills` and `ecap-agent-pack` are bot-runtime
packages, not deployed services; `web` deploys to Cloudflare Workers via
this repo's workflows.

## Test plan
- [ ] Open `architecture.md` on GitHub — confirm Mermaid diagram renders
- [ ] Same for `architecture.zh-CN.md`
- [ ] Click EN ↔ 中文 language links at the top of each doc
- [ ] Click the cross-link from `AGENTS.md` "Related repos" section
- [ ] Click the `architecture.md` / `中文` links from `README.md`
runtime-dependencies blockquote
- [ ] Spot-check the cited file:line refs in `services/claw-interface/`
and `web/` (e.g. `NANGO_SERVER_URL` direct path,
`NEXT_PUBLIC_MATTERMOST_URL` web client, `OPENCLAW_PLATFORM_URL` →
fastclaw)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-authored-by: claude[bot] <41898282+claude[bot]@users.noreply.github.com>
Co-authored-by: Chris@ZooClaw <undefined@users.noreply.github.com>
```

### PR Body

## Summary
- New `architecture.md` (and Chinese mirror `architecture.zh-CN.md`) at repo root mapping the runtime topology, external repo inventory, data flows, deployment source-of-truth, and env-var → service table.
- `AGENTS.md` and `README.md` cross-link to the new doc.
- Notable clarifications surfaced by cross-repo verification (`fastclaw`, `ecap-proxy-service`, `openclaw-docker`, `gcp-foundation`):
  - Mattermost is the chat transport: web ↔ Mattermost server ↔ bot pod; `claw-interface` is **not** on the chat path, it only provisions accounts.
  - Nango has two access paths: `claw-interface` calls Nango directly for OAuth/connection management; bot-pod skills call Nango via `ecap-proxy-service`, which adds per-user auth (Nango itself has no per-user auth model).
  - LiteLLM routing for bot pods is **declarative** (lives in each bot's `openclaw.json`), not injected via pod env — fastclaw only injects `BOT_ID`/`BOT_SLUG`/`BOT_TOKEN`/`PUBLIC_BASE_URL`.
  - Lago is only ever called via `billing-gateway`; no `services/` code imports a Lago client.
  - `gcp-foundation` is the source of truth for deployed versions, but **not** everything is there: `billing-gateway` deploys via its own repo's CI/CD; `ecap-skills` and `ecap-agent-pack` are bot-runtime packages, not deployed services; `web` deploys to Cloudflare Workers via this repo's workflows.

## Test plan
- [ ] Open `architecture.md` on GitHub — confirm Mermaid diagram renders
- [ ] Same for `architecture.zh-CN.md`
- [ ] Click EN ↔ 中文 language links at the top of each doc
- [ ] Click the cross-link from `AGENTS.md` "Related repos" section
- [ ] Click the `architecture.md` / `中文` links from `README.md` runtime-dependencies blockquote
- [ ] Spot-check the cited file:line refs in `services/claw-interface/` and `web/` (e.g. `NANGO_SERVER_URL` direct path, `NEXT_PUBLIC_MATTERMOST_URL` web client, `OPENCLAW_PLATFORM_URL` → fastclaw)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [25] 142c94b6
- **Author**: bill-srp
- **Date**: 2026-05-14T09:19:07Z
- **SHA**: 142c94b6675ae5c7e88117b8d6e449778672cbf4
- **PR**: #1597

### Commit Message

```
refactor(claw-interface): decommission tool-execution + skills cleanup (tracking) (#1597)

## Status

**Tracking PR — will not merge directly.** This PR originally bundled
three concerns (~4,200 lines); being split into focused PRs as agreed
during review. This PR carries the **remaining work** for reference and
will be closed once the follow-ups land.

| Slice | Status | PR |
|---|---|---|
| **PR-1**: typed `IntegrationConnection` + lean `NangoProvider` | ✅
Merged | #1620 (squash `44744af7`) |
| **PR-2**: decommission tool-execution plane | TODO | _branch:
`refactor/decommission-tool-execution`_ |
| **PR-3**: skills module cleanup + provider gate | TODO | _branch:
`refactor/skills-cleanup` (planned)_ |

## What's left on this branch

After rebasing `feat/connectors` onto post-#1620 main: **+109 / −2930
across 20 files** — almost entirely deletions. The +109 additions are:

| Lines | What |
|---|---|
| ~30 | Docstrings/comments explaining what was removed
(`NangoProvider`, flattened `openclaw_integrations.py` module doc,
"Nango owns provider validation" comment) |
| ~84 | Two replacement tests for the surviving enable/disable endpoints
— `test_enable_flips_enabled_flag_with_optimistic_lock` and
`test_disable_flips_enabled_flag_with_optimistic_lock`. These replace
**1,038 lines** of `/execute` / skill-injection test code being deleted.
|
| 5 | `pyproject.toml` cleanup: drop `app/skills/loader.py` from ruff
per-file-ignores; update importlinter C6 contract from "skills/tasks are
extension-point leaves" → "tasks are an extension-point leaf" (skills/
is gone) |
| 1 | `NangoProvider._request` signature simplification after dropping
the unused `headers` kwarg |

No new behavior. No new features. The work is pure deletion + cleanup +
focused regression tests for what survives.

## Re: codex review — "Breaking change without a migration path"

This finding (`REQUEST_CHANGES`, "high" risk) will recur on PR-2 because
the surface is the same. Pre-empting it here so it stays settled:

> **Context not visible in the diff:** tool execution has been moved to
a **separate service**. claw-interface is no longer the destination for
bot tool-call callbacks — the new service owns them. So the `/execute` +
`/execute/confirm` removal on claw-interface is correct; there is no pod
fleet still calling claw-interface for tool execution.

The dangling env-var injection (`bot_config.py:280-284`,
`_bot_lifecycle.py:83-87`) is intentionally **left for the new service's
own env-var setup PR**. Those vars are inert from claw-interface's
perspective (no code here reads them); cleaning them up here without the
matching setup over there would create a coordination gap. Scoping this
PR-set to "remove claw-interface's side of the contract" is deliberate.

## Commits remaining on this branch (post-rebase)

**Decommission group (→ PR-2):**
1. `cfacf130` — remove connector skill injection path
2. `d64ee3fb` — decommission `/execute`, `/execute/confirm`,
`executor.py`,
`proxy_request`/`get_connection_config`/`get_integration_client_id` on
`NangoProvider`, `ExecuteTool*` schemas
3. `884e79fd` — drop unused `headers` kwarg on `NangoProvider._request`
4. `560982a8` — shrink `skills/loader` to provider discovery
5. `da653183` — vendor SKILL.md files + remove external sync (will be
**split** when carving PR-2 — only the external-sync removal portion
lands; SKILL.md vendoring is dropped since PR-3 deletes them anyway)

**Skills cleanup group (→ PR-3):**
6. `313e17c4` — remove all connector SKILL.md files
7. `571c46a1` — remove `/connect` endpoint + `app/skills/` module
8. `1f7a137b` — Revert of the two preceding (broke the web Connect
button pinned by `ConnectorsSection.unit.spec.tsx:391`)
9. `5e51a573` — replace skills/loader with hardcoded provider whitelist
10. `773878c7` — drop `VALID_PROVIDERS`, defer to Nango as the provider
gate
11. `6eda6b48` — flatten `openclaw_integrations/` package back to a
single file

The `1f7a137b` revert + redo churn (commits 6–9) will be **collapsed**
when PR-3 is carved — final state on `main` is the net effect, not the
intermediate flip-flop.

## What survives in claw-interface

OAuth lifecycle only:
- `POST /openclaw/integrations/connect` — initiate OAuth (returns Nango
auth URL)
- `GET /openclaw/integrations/connections` — list connections,
auto-promote pending → connected via Nango poll
- `DELETE /openclaw/integrations/connections/{provider}` — disconnect
- `PUT /openclaw/integrations/connections/{provider}/enable|disable` —
toggle the ``enabled`` flag (now bookkeeping only — no side-effects on
bot workspace, since tool execution moved to the new service)
- `POST /openclaw/integrations/webhooks/nango` — receive Nango status
updates

## Why kept open

PR-2 and PR-3 will each carry a clean slice of the diff above; this PR
is the **integration check** — once both follow-ups merge,
`feat/connectors` should be a no-op vs `main`. If it isn't, something
was missed in the split. Close after both follow-ups land.
```

### PR Body

## Status

**Tracking PR — will not merge directly.** This PR originally bundled three concerns (~4,200 lines); being split into focused PRs as agreed during review. This PR carries the **remaining work** for reference and will be closed once the follow-ups land.

| Slice | Status | PR |
|---|---|---|
| **PR-1**: typed `IntegrationConnection` + lean `NangoProvider` | ✅ Merged | #1620 (squash `44744af7`) |
| **PR-2**: decommission tool-execution plane | TODO | _branch: `refactor/decommission-tool-execution`_ |
| **PR-3**: skills module cleanup + provider gate | TODO | _branch: `refactor/skills-cleanup` (planned)_ |

## What's left on this branch

After rebasing `feat/connectors` onto post-#1620 main: **+109 / −2930 across 20 files** — almost entirely deletions. The +109 additions are:

| Lines | What |
|---|---|
| ~30 | Docstrings/comments explaining what was removed (`NangoProvider`, flattened `openclaw_integrations.py` module doc, "Nango owns provider validation" comment) |
| ~84 | Two replacement tests for the surviving enable/disable endpoints — `test_enable_flips_enabled_flag_with_optimistic_lock` and `test_disable_flips_enabled_flag_with_optimistic_lock`. These replace **1,038 lines** of `/execute` / skill-injection test code being deleted. |
| 5 | `pyproject.toml` cleanup: drop `app/skills/loader.py` from ruff per-file-ignores; update importlinter C6 contract from "skills/tasks are extension-point leaves" → "tasks are an extension-point leaf" (skills/ is gone) |
| 1 | `NangoProvider._request` signature simplification after dropping the unused `headers` kwarg |

No new behavior. No new features. The work is pure deletion + cleanup + focused regression tests for what survives.

## Re: codex review — "Breaking change without a migration path"

This finding (`REQUEST_CHANGES`, "high" risk) will recur on PR-2 because the surface is the same. Pre-empting it here so it stays settled:

> **Context not visible in the diff:** tool execution has been moved to a **separate service**. claw-interface is no longer the destination for bot tool-call callbacks — the new service owns them. So the `/execute` + `/execute/confirm` removal on claw-interface is correct; there is no pod fleet still calling claw-interface for tool execution.

The dangling env-var injection (`bot_config.py:280-284`, `_bot_lifecycle.py:83-87`) is intentionally **left for the new service's own env-var setup PR**. Those vars are inert from claw-interface's perspective (no code here reads them); cleaning them up here without the matching setup over there would create a coordination gap. Scoping this PR-set to "remove claw-interface's side of the contract" is deliberate.

## Commits remaining on this branch (post-rebase)

**Decommission group (→ PR-2):**
1. `cfacf130` — remove connector skill injection path
2. `d64ee3fb` — decommission `/execute`, `/execute/confirm`, `executor.py`, `proxy_request`/`get_connection_config`/`get_integration_client_id` on `NangoProvider`, `ExecuteTool*` schemas
3. `884e79fd` — drop unused `headers` kwarg on `NangoProvider._request`
4. `560982a8` — shrink `skills/loader` to provider discovery
5. `da653183` — vendor SKILL.md files + remove external sync (will be **split** when carving PR-2 — only the external-sync removal portion lands; SKILL.md vendoring is dropped since PR-3 deletes them anyway)

**Skills cleanup group (→ PR-3):**
6. `313e17c4` — remove all connector SKILL.md files
7. `571c46a1` — remove `/connect` endpoint + `app/skills/` module
8. `1f7a137b` — Revert of the two preceding (broke the web Connect button pinned by `ConnectorsSection.unit.spec.tsx:391`)
9. `5e51a573` — replace skills/loader with hardcoded provider whitelist
10. `773878c7` — drop `VALID_PROVIDERS`, defer to Nango as the provider gate
11. `6eda6b48` — flatten `openclaw_integrations/` package back to a single file

The `1f7a137b` revert + redo churn (commits 6–9) will be **collapsed** when PR-3 is carved — final state on `main` is the net effect, not the intermediate flip-flop.

## What survives in claw-interface

OAuth lifecycle only:
- `POST /openclaw/integrations/connect` — initiate OAuth (returns Nango auth URL)
- `GET /openclaw/integrations/connections` — list connections, auto-promote pending → connected via Nango poll
- `DELETE /openclaw/integrations/connections/{provider}` — disconnect
- `PUT /openclaw/integrations/connections/{provider}/enable|disable` — toggle the ``enabled`` flag (now bookkeeping only — no side-effects on bot workspace, since tool execution moved to the new service)
- `POST /openclaw/integrations/webhooks/nango` — receive Nango status updates

## Why kept open

PR-2 and PR-3 will each carry a clean slice of the diff above; this PR is the **integration check** — once both follow-ups merge, `feat/connectors` should be a no-op vs `main`. If it isn't, something was missed in the split. Close after both follow-ups land.

---
## [26] de5589f4
- **Author**: kaka-srp
- **Date**: 2026-05-14T07:44:51Z
- **SHA**: de5589f471c6718e94d4b186cbf78da6bb0fd8a0
- **PR**: #1609

### Commit Message

```
refactor(web): subagent sessions event subscription (ECA-662) (#1609)

## Summary

Replace the 3s `sessions.list` polling loop with `sessions.subscribe` +
`sessions.changed` push events to stop overwhelming OpenClaw bot
gateways. Drop three defensive `chat.history` reloads that were
redundant with the streaming/event path. All review-cycle follow-ups
(epoch counter, fallback polling, closure-leak guard) included.

- **Root cause**: clients polled `sessions.list` every 3s while bot
generated; JuiceFS lock contention spiked, Node event loop blocked,
liveness probes timed out → kubelet SIGKILL (Exit 137). See
[ECA-662](https://linear.app/srpone/issue/ECA-662).
- **Mechanism**: OpenClaw 2026.4.2+ emits `sessions.changed` on subagent
create / status-change / message; verified in production via `openclaw
gateway call sessions.subscribe --params '{}' --json` → `{"subscribed":
true}`.
- **Impact**: per-client RPC traffic for a 5min active session drops
from ~105 (100 list polls + 5 history reloads) to ~3 (1 list snapshot +
1 subscribe + 1 lifecycle-end reload). 35x reduction; bot event-loop
pressure eliminated.

## What's in the diff

**改动 1 — `useSubagentSessions.ts`**
([`bd3194654`](../commit/bd3194654)):
- Drop `setInterval(fetchSessions, 3000)` polling
- Subscribe to `sessions.changed` on connect, handle `reason: delete`
(remove) / others (upsert)
- Keep placeholder injection from `agent.*` events (UI immediate
feedback before push arrives)

**改动 2 — `useOpenClawChat.ts`** ([`bc274962e`](../commit/bc274962e)):
- Drop post-error reload (error message already in state via
`setMessages`)
- Drop cache-remount reload (MM is primary display source; OpenClaw
`messages` state is fallback only)
- Drop visibility reload (WS layer already detects zombie connections
via `STALE_CONNECTION_THRESHOLD_MS`)
- Keep first-connect / post-lifecycle-end / follow-up `loadHistory`

**Review-cycle robustness fixes:**
- [`534022c7f`](../commit/534022c7f) `logger.warn` on subscribe
rejection (prod rollout signal) + reduce onEvent callback complexity
- [`ad19283c6`](../commit/ad19283c6) `connectionGeneration` counter on
`useOpenClawWebSocket` — silent reconnect doesn't flip `ws.status`, so
deps on `[ws.status]` miss epoch changes; new counter binds subscribe to
actual connection lifecycle. Plus 30s fallback polling when subscribe
rejects (old bot < 2026.4.2 compatibility).
- [`8d2e2869f`](../commit/8d2e2869f) effect-scoped `active` flag —
guards `.catch` microtask against firing after teardown, preventing
leaked `setInterval` timers from late-arriving rejections (e.g. user
navigates away mid-RPC, or epoch flips before old subscribe rejects).

## What's intentionally NOT in scope

- **Backend changes** — none. `services/claw-interface` untouched.
- **bot livenessProbe tuning** — Linear's 改动 3 was explicitly deferred;
once polling pressure drops, probe failures should self-resolve.
Re-evaluate after deployment.
- **Removing post-lifecycle-end `loadHistory` (2s)** — kept as defensive
backstop for tool-result / system-injected messages that may not be in
the delta stream. Re-evaluate after staging soak.

## Verified manually on staging

WS frames inspected directly in DevTools:
- `sessions.subscribe` outgoing → `{"subscribed": true}` response ✅
- `sessions.changed` push events with `reason: create / patch / send`
flow during subagent runs ✅
- `sessions.list` called once on connect, zero subsequent polls ✅
- `chat.history` only at first connect + 2s post-lifecycle-end (no error
/ cache-remount / visibility reloads) ✅

## Test plan

- [x] Unit: `tests/unit/hooks/useSubagentSessions.unit.spec.ts` +
`tests/unit/app/chat/useSubagentSessions.unit.spec.ts` +
`tests/unit/hooks/useOpenClawChat.unit.spec.ts` — 80 tests, all passing
- [x] Local: `pnpm test:unit` + `tsc --noEmit` + `eslint` all green
- [x] Manual staging: WS frame inspection as above
- [ ] Staging deployment 24-48h soak: monitor `kubectl get events
--field-selector reason=Unhealthy -n openclaw` count drop + bot pod
restart counter
- [ ] Production canary: deploy to one web instance, watch 24h, verify
bot SIGKILL rate reaches zero
```

### PR Body

## Summary

Replace the 3s `sessions.list` polling loop with `sessions.subscribe` + `sessions.changed` push events to stop overwhelming OpenClaw bot gateways. Drop three defensive `chat.history` reloads that were redundant with the streaming/event path. All review-cycle follow-ups (epoch counter, fallback polling, closure-leak guard) included.

- **Root cause**: clients polled `sessions.list` every 3s while bot generated; JuiceFS lock contention spiked, Node event loop blocked, liveness probes timed out → kubelet SIGKILL (Exit 137). See [ECA-662](https://linear.app/srpone/issue/ECA-662).
- **Mechanism**: OpenClaw 2026.4.2+ emits `sessions.changed` on subagent create / status-change / message; verified in production via `openclaw gateway call sessions.subscribe --params '{}' --json` → `{"subscribed": true}`.
- **Impact**: per-client RPC traffic for a 5min active session drops from ~105 (100 list polls + 5 history reloads) to ~3 (1 list snapshot + 1 subscribe + 1 lifecycle-end reload). 35x reduction; bot event-loop pressure eliminated.

## What's in the diff

**改动 1 — `useSubagentSessions.ts`** ([`bd3194654`](../commit/bd3194654)):
- Drop `setInterval(fetchSessions, 3000)` polling
- Subscribe to `sessions.changed` on connect, handle `reason: delete` (remove) / others (upsert)
- Keep placeholder injection from `agent.*` events (UI immediate feedback before push arrives)

**改动 2 — `useOpenClawChat.ts`** ([`bc274962e`](../commit/bc274962e)):
- Drop post-error reload (error message already in state via `setMessages`)
- Drop cache-remount reload (MM is primary display source; OpenClaw `messages` state is fallback only)
- Drop visibility reload (WS layer already detects zombie connections via `STALE_CONNECTION_THRESHOLD_MS`)
- Keep first-connect / post-lifecycle-end / follow-up `loadHistory`

**Review-cycle robustness fixes:**
- [`534022c7f`](../commit/534022c7f) `logger.warn` on subscribe rejection (prod rollout signal) + reduce onEvent callback complexity
- [`ad19283c6`](../commit/ad19283c6) `connectionGeneration` counter on `useOpenClawWebSocket` — silent reconnect doesn't flip `ws.status`, so deps on `[ws.status]` miss epoch changes; new counter binds subscribe to actual connection lifecycle. Plus 30s fallback polling when subscribe rejects (old bot < 2026.4.2 compatibility).
- [`8d2e2869f`](../commit/8d2e2869f) effect-scoped `active` flag — guards `.catch` microtask against firing after teardown, preventing leaked `setInterval` timers from late-arriving rejections (e.g. user navigates away mid-RPC, or epoch flips before old subscribe rejects).

## What's intentionally NOT in scope

- **Backend changes** — none. `services/claw-interface` untouched.
- **bot livenessProbe tuning** — Linear's 改动 3 was explicitly deferred; once polling pressure drops, probe failures should self-resolve. Re-evaluate after deployment.
- **Removing post-lifecycle-end `loadHistory` (2s)** — kept as defensive backstop for tool-result / system-injected messages that may not be in the delta stream. Re-evaluate after staging soak.

## Verified manually on staging

WS frames inspected directly in DevTools:
- `sessions.subscribe` outgoing → `{"subscribed": true}` response ✅
- `sessions.changed` push events with `reason: create / patch / send` flow during subagent runs ✅
- `sessions.list` called once on connect, zero subsequent polls ✅
- `chat.history` only at first connect + 2s post-lifecycle-end (no error / cache-remount / visibility reloads) ✅

## Test plan

- [x] Unit: `tests/unit/hooks/useSubagentSessions.unit.spec.ts` + `tests/unit/app/chat/useSubagentSessions.unit.spec.ts` + `tests/unit/hooks/useOpenClawChat.unit.spec.ts` — 80 tests, all passing
- [x] Local: `pnpm test:unit` + `tsc --noEmit` + `eslint` all green
- [x] Manual staging: WS frame inspection as above
- [ ] Staging deployment 24-48h soak: monitor `kubectl get events --field-selector reason=Unhealthy -n openclaw` count drop + bot pod restart counter
- [ ] Production canary: deploy to one web instance, watch 24h, verify bot SIGKILL rate reaches zero

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
## [27] 44744af7
- **Author**: bill-srp
- **Date**: 2026-05-14T07:25:32Z
- **SHA**: 44744af71b4b04fa9ef6ebd832ff3b8a7079503d
- **PR**: #1620

### Commit Message

```
refactor(claw-interface): typed IntegrationConnection + lean NangoProvider (#1620)

## Summary

First slice of #1597, scoped to the **typing pass only**. Introduces a
typed `IntegrationConnection` (mirroring #1574 / #1585 for `Account`)
and trims `NangoProvider` to a lean async surface. No behavior changes;
no API surface changes.

This is **PR 1 of 3** in the planned split of #1597:
- **PR 1 (this PR)** — typed `IntegrationConnection` + lean
`NangoProvider`
- **PR 2** — decommission tool-execution plane (`/execute`,
`/execute/confirm`, `executor.py`, skill-injection path)
- **PR 3** — skills module cleanup + provider gate

### Commits

1. `5688e056` introduce typed `IntegrationConnection` + retype
`integration_repo`
2. `8bc5a38c` trim `NangoProvider` (drop ABC, retry loop, dead code)
3. `935f76b6` align BDD feature with `IntegrationStatus` literal + ruff
format
4. `e5c98a59` address earlier codex review on #1597

### What this changes

- `app/schema/integration.py` — new typed `IntegrationConnection` model
+ `IntegrationStatus` literal
- `app/database/integration_repo.py` — repo returns/accepts the typed
model (no more dict ferrying)
- `app/services/integration_provider.py` — drops unused ABC, retry loop,
and `_request` dead code paths
- Tests — new `test_integration_schema.py`; existing tests updated for
the typed contract

### What this does NOT change

- `/execute` and `/execute/confirm` endpoints still exist (removed in PR
2)
- `executor.py` still exists (removed in PR 2)
- `app/skills/` module still exists (removed in PR 3)
- All public API surfaces preserved

### Validated locally

- Cherry-pick onto current `origin/main` applied cleanly (no conflicts)
- Python suite + ruff/pyright **not** run locally on this slice —
relying on CI (`python-code-quality / build-and-test`). On the original
branch the full suite was 2957/2957 green at `e5c98a59`.

## Test plan

- [ ] CI `python-code-quality / build-and-test` passes
- [ ] CI `code-quality / lint-and-test` is a no-op (no `web/**` changes)
- [ ] No manual smoke needed — typing pass only, no API surface change
```

### PR Body

## Summary

First slice of #1597, scoped to the **typing pass only**. Introduces a typed `IntegrationConnection` (mirroring #1574 / #1585 for `Account`) and trims `NangoProvider` to a lean async surface. No behavior changes; no API surface changes.

This is **PR 1 of 3** in the planned split of #1597:
- **PR 1 (this PR)** — typed `IntegrationConnection` + lean `NangoProvider`
- **PR 2** — decommission tool-execution plane (`/execute`, `/execute/confirm`, `executor.py`, skill-injection path)
- **PR 3** — skills module cleanup + provider gate

### Commits

1. `5688e056` introduce typed `IntegrationConnection` + retype `integration_repo`
2. `8bc5a38c` trim `NangoProvider` (drop ABC, retry loop, dead code)
3. `935f76b6` align BDD feature with `IntegrationStatus` literal + ruff format
4. `e5c98a59` address earlier codex review on #1597

### What this changes

- `app/schema/integration.py` — new typed `IntegrationConnection` model + `IntegrationStatus` literal
- `app/database/integration_repo.py` — repo returns/accepts the typed model (no more dict ferrying)
- `app/services/integration_provider.py` — drops unused ABC, retry loop, and `_request` dead code paths
- Tests — new `test_integration_schema.py`; existing tests updated for the typed contract

### What this does NOT change

- `/execute` and `/execute/confirm` endpoints still exist (removed in PR 2)
- `executor.py` still exists (removed in PR 2)
- `app/skills/` module still exists (removed in PR 3)
- All public API surfaces preserved

### Validated locally

- Cherry-pick onto current `origin/main` applied cleanly (no conflicts)
- Python suite + ruff/pyright **not** run locally on this slice — relying on CI (`python-code-quality / build-and-test`). On the original branch the full suite was 2957/2957 green at `e5c98a59`.

## Test plan

- [ ] CI `python-code-quality / build-and-test` passes
- [ ] CI `code-quality / lint-and-test` is a no-op (no `web/**` changes)
- [ ] No manual smoke needed — typing pass only, no API surface change

---
