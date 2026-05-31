# ecap-workspace — 2026-05-30

共 49 条 commits

## [ab7328c4](https://github.com/SerendipityOneInc/ecap-workspace/commit/ab7328c4fc3dd0f070fc5a8e5953eb370db9c3c6)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T18:08:25Z
- **PR**: #2130

### Commit Message

```
refactor(web): extract resetCheckoutState in SubscriptionPanel (#2130)

## What

Extract the repeated subscription-checkout reset triplet in
`handlePaymentMethodSelect` into a single `resetCheckoutState` helper.

```ts
const resetCheckoutState = () => {
  setPaymentMethodPending(null)
  setCheckoutProcessingChannel(null)
  setIsLoading(null)
}
```

## Why

The handler cleared those exact three state pieces on **all three** exit
paths — Stripe success, Antom success, and the `catch`. Three copies of
the same reset drift apart easily (a future "also clear X on cancel" fix
can miss a path). One helper = one definition the three paths share.

**Scope:** subscription path only. The topup handler
(`handleTopupPurchase`) clears a different first setter
(`setTopupPending` instead of `setPaymentMethodPending`) and its
success-reset paths aren't covered by the same characterization tests,
so it's intentionally left untouched. (A unified "reset to idle" across
both flows could be a future follow-up once topup's success paths are
locked.)

## Behavior preserved

No functional change (net +3 lines — the helper + comment slightly
exceed the 6 lines saved; the value is the single source of truth, not
line count). Pinned by `SubscriptionPanel.unit.spec.tsx`:
- **stripe-success** and **antom-success** assert the PaymentMethodModal
closes + plan loading clears (added in #2127 specifically to guard this
extraction)
- `createOrder fail → … idle` and `no userInfo.uid → … idle (#1102)`
already locked the error / early-return resets

## Verification

- `pnpm test:unit …/SubscriptionPanel.unit.spec.tsx` → 47 passed
- full-repo `tsc --noEmit` clean; `eslint` clean; `pnpm dup:src` under
threshold

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Extract the repeated subscription-checkout reset triplet in `handlePaymentMethodSelect` into a single `resetCheckoutState` helper.

```ts
const resetCheckoutState = () => {
  setPaymentMethodPending(null)
  setCheckoutProcessingChannel(null)
  setIsLoading(null)
}
```

## Why

The handler cleared those exact three state pieces on **all three** exit paths — Stripe success, Antom success, and the `catch`. Three copies of the same reset drift apart easily (a future "also clear X on cancel" fix can miss a path). One helper = one definition the three paths share.

**Scope:** subscription path only. The topup handler (`handleTopupPurchase`) clears a different first setter (`setTopupPending` instead of `setPaymentMethodPending`) and its success-reset paths aren't covered by the same characterization tests, so it's intentionally left untouched. (A unified "reset to idle" across both flows could be a future follow-up once topup's success paths are locked.)

## Behavior preserved

No functional change (net +3 lines — the helper + comment slightly exceed the 6 lines saved; the value is the single source of truth, not line count). Pinned by `SubscriptionPanel.unit.spec.tsx`:
- **stripe-success** and **antom-success** assert the PaymentMethodModal closes + plan loading clears (added in #2127 specifically to guard this extraction)
- `createOrder fail → … idle` and `no userInfo.uid → … idle (#1102)` already locked the error / early-return resets

## Verification

- `pnpm test:unit …/SubscriptionPanel.unit.spec.tsx` → 47 passed
- full-repo `tsc --noEmit` clean; `eslint` clean; `pnpm dup:src` under threshold

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [867e60c6](https://github.com/SerendipityOneInc/ecap-workspace/commit/867e60c6b6f08adeb262d9535c8b80bcc6776c67)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T18:07:34Z
- **PR**: #2129

### Commit Message

```
refactor(web): replace setMounted hydration flags with useIsHydrated; drop two reset/sync effects (#2129)

## What & why

Removes a cluster of `useEffect`-based React anti-patterns surfaced by
an audit of **all 293 `useEffect` call sites** in `web/`, applying
React's [You Might Not Need an
Effect](https://react.dev/learn/you-might-not-need-an-effect) guidance.
All changes are **behavior-preserving**.

> The audit found ~67% of effects are legitimate external-system
synchronization (good cleanup/race-guard discipline). This PR fixes only
the highest-confidence, lowest-risk subset; structural refactors
(OnboardingProvider modal/step sync, enterprise-admin routing,
canvas/GenClawInput FSMs) are deliberately **out of scope** — they need
characterization tests first.

## Changes

**Tier A — synchronization anti-patterns**
- **New `useIsHydrated()` hook** (`app/src/hooks/useIsHydrated.ts`) —
`useSyncExternalStore`-based, mirroring the server/client-snapshot shape
already used in `useStableConnectionStatus`. Replaces **6** identical
`const [mounted] = useState(false); useEffect(() => setMounted(true),
[])` hydration-flag pairs:
- `ThemeToggle`, `settings/GeneralTab`, `providers/FeedbackProvider`,
`landing/LandingClient`, `pricing/PublicPricingClient`,
`userguide/UserGuideClient`
- A lazy `useState` initializer can't be used here — it would desync the
server (`false`) and client-first (`true`) renders.
`useSyncExternalStore`'s server snapshot reproduces the exact `false →
true` post-hydration transition with no mismatch.
- **`chat/ConfirmModal`** — split the `open` gate from the stateful body
so the body remounts on each open, resetting `typed` naturally; drops
the `useEffect(() => { if (!open) setTyped('') }, [open])` reset effect.
Adds a characterization test locking the reset-on-reopen contract.

**Tier B — robustness**
- **`chat/useChatPaymentReturn`** — depend on extracted primitive query
params instead of the `URLSearchParams` object (identity changes each
parent render). Already idempotent via `paymentProcessedRef`; this just
stops the effect re-running on unrelated renders.
- **`user/verify` magic-link effect** — hoist the 3s post-success
redirect timer to a ref and clear it in cleanup, so it can't
`router.push` after unmount.

**Net:** −6 `useEffect`, −6 `useState`, −1 effect (ConfirmModal), +1
reusable hook.

## Verification
- `tsc --noEmit`: all changed files type-clean (the 2 remaining repo
errors are a pre-existing `searchParams` null issue in
`ComposioConnectorsClient.tsx`, untouched here).
- `eslint`: all changed + new files clean.
- Unit tests (existing + 1 new spec): **87 pass** —
`ThemeToggle`/`GeneralTab`/`DowngradeConfirmModal` (41), new
`ConfirmModal` (4), `userguide-client`/`FeedbackProvider` (24),
`useChatPaymentReturn` + 3 `user-verify` specs (18).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What & why

Removes a cluster of `useEffect`-based React anti-patterns surfaced by an audit of **all 293 `useEffect` call sites** in `web/`, applying React's [You Might Not Need an Effect](https://react.dev/learn/you-might-not-need-an-effect) guidance. All changes are **behavior-preserving**.

> The audit found ~67% of effects are legitimate external-system synchronization (good cleanup/race-guard discipline). This PR fixes only the highest-confidence, lowest-risk subset; structural refactors (OnboardingProvider modal/step sync, enterprise-admin routing, canvas/GenClawInput FSMs) are deliberately **out of scope** — they need characterization tests first.

## Changes

**Tier A — synchronization anti-patterns**
- **New `useIsHydrated()` hook** (`app/src/hooks/useIsHydrated.ts`) — `useSyncExternalStore`-based, mirroring the server/client-snapshot shape already used in `useStableConnectionStatus`. Replaces **6** identical `const [mounted] = useState(false); useEffect(() => setMounted(true), [])` hydration-flag pairs:
  - `ThemeToggle`, `settings/GeneralTab`, `providers/FeedbackProvider`, `landing/LandingClient`, `pricing/PublicPricingClient`, `userguide/UserGuideClient`
  - A lazy `useState` initializer can't be used here — it would desync the server (`false`) and client-first (`true`) renders. `useSyncExternalStore`'s server snapshot reproduces the exact `false → true` post-hydration transition with no mismatch.
- **`chat/ConfirmModal`** — split the `open` gate from the stateful body so the body remounts on each open, resetting `typed` naturally; drops the `useEffect(() => { if (!open) setTyped('') }, [open])` reset effect. Adds a characterization test locking the reset-on-reopen contract.

**Tier B — robustness**
- **`chat/useChatPaymentReturn`** — depend on extracted primitive query params instead of the `URLSearchParams` object (identity changes each parent render). Already idempotent via `paymentProcessedRef`; this just stops the effect re-running on unrelated renders.
- **`user/verify` magic-link effect** — hoist the 3s post-success redirect timer to a ref and clear it in cleanup, so it can't `router.push` after unmount.

**Net:** −6 `useEffect`, −6 `useState`, −1 effect (ConfirmModal), +1 reusable hook.

## Verification
- `tsc --noEmit`: all changed files type-clean (the 2 remaining repo errors are a pre-existing `searchParams` null issue in `ComposioConnectorsClient.tsx`, untouched here).
- `eslint`: all changed + new files clean.
- Unit tests (existing + 1 new spec): **87 pass** — `ThemeToggle`/`GeneralTab`/`DowngradeConfirmModal` (41), new `ConfirmModal` (4), `userguide-client`/`FeedbackProvider` (24), `useChatPaymentReturn` + 3 `user-verify` specs (18).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [3662a2a4](https://github.com/SerendipityOneInc/ecap-workspace/commit/3662a2a4cff0aedf9c5803d4698bcb5ea179480f)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T17:55:17Z
- **PR**: #2124

### Commit Message

```
refactor(web): simplify UserMenu redeem error mapping and plan UI (#2124)

## What

Two render-time simplifications in `UserMenu.tsx`, no behavior change:

1. **Redeem error mapping** — replace the four-branch `if/else if
(errorCode === …)` chain with a `REDEEM_ERROR_KEYS` lookup map. Unmapped
codes still fall back to the server-provided `message` (or the generic
`giftCode.errorInvalid` key) exactly as before.

2. **Plan UI** — the plan label, plan sub-label, and action button each
had their own `switch (status)` IIFE (two of them repeating an `if
(isLoading) return null` skeleton). They all key off the same
subscription status, so they now resolve in a single pass that returns
`{ label, subLabel, button }`.

## Why

Three parallel switches over the same discriminant drift apart over time
and triple the edit cost of any status-handling change. A lookup map and
a single status switch make the contract obvious and keep each status's
three outputs co-located.

Kept as render-time computation — no `useMemo` — per `web/app/CLAUDE.md`
("Avoid useCallback/useMemo unless clearly necessary").

## Behavior preserved

No functional change (net −10 lines). Already fully locked by the
existing `UserMenu.unit.spec.tsx` (66 tests):
- every gift-code error path: `already_participated` / `code_exhausted`
/ `no_subscription` / `plan_downgrade_not_allowed`, the
unknown-code-with-message fallback, the empty fallback, and the
thrown-error path
- the plan-label ×status matrix (active/PLAN_INFO hit, unknown plan,
null plan, trialing, trial, asleep, unknown→asleep) and
sub-label/trial-urgency
- the action-button ×status matrix (upgrade/subscribe/activate/manage,
isLoading hides)

No test changes were needed — the behavior was already pinned.

## Verification

- `pnpm test:unit …/UserMenu.unit.spec.tsx` → 66 passed
- full-repo `tsc --noEmit` clean; `eslint` clean; `pnpm dup:src` under
threshold

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Two render-time simplifications in `UserMenu.tsx`, no behavior change:

1. **Redeem error mapping** — replace the four-branch `if/else if (errorCode === …)` chain with a `REDEEM_ERROR_KEYS` lookup map. Unmapped codes still fall back to the server-provided `message` (or the generic `giftCode.errorInvalid` key) exactly as before.

2. **Plan UI** — the plan label, plan sub-label, and action button each had their own `switch (status)` IIFE (two of them repeating an `if (isLoading) return null` skeleton). They all key off the same subscription status, so they now resolve in a single pass that returns `{ label, subLabel, button }`.

## Why

Three parallel switches over the same discriminant drift apart over time and triple the edit cost of any status-handling change. A lookup map and a single status switch make the contract obvious and keep each status's three outputs co-located.

Kept as render-time computation — no `useMemo` — per `web/app/CLAUDE.md` ("Avoid useCallback/useMemo unless clearly necessary").

## Behavior preserved

No functional change (net −10 lines). Already fully locked by the existing `UserMenu.unit.spec.tsx` (66 tests):
- every gift-code error path: `already_participated` / `code_exhausted` / `no_subscription` / `plan_downgrade_not_allowed`, the unknown-code-with-message fallback, the empty fallback, and the thrown-error path
- the plan-label ×status matrix (active/PLAN_INFO hit, unknown plan, null plan, trialing, trial, asleep, unknown→asleep) and sub-label/trial-urgency
- the action-button ×status matrix (upgrade/subscribe/activate/manage, isLoading hides)

No test changes were needed — the behavior was already pinned.

## Verification

- `pnpm test:unit …/UserMenu.unit.spec.tsx` → 66 passed
- full-repo `tsc --noEmit` clean; `eslint` clean; `pnpm dup:src` under threshold

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [51112ee8](https://github.com/SerendipityOneInc/ecap-workspace/commit/51112ee88920d9df12e4cda45b236274e200e74a)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T17:53:45Z
- **PR**: #2127

### Commit Message

```
test(web): lock SubscriptionPanel checkout-state reset on success (#2127)

## What

Characterization tests (test-first, no production change) pinning that a
**successful** Stripe or Antom subscription checkout closes the
`PaymentMethodModal` and clears the per-plan loading state — ahead of a
follow-up that extracts the repeated checkout-reset triplet into a
shared helper.

## Why

`handlePaymentMethodSelect` resets three pieces of state on every exit
path:

```
setPaymentMethodPending(null)
setCheckoutProcessingChannel(null)
setIsLoading(null)
```

This triplet appears three times — Stripe success, Antom success, and
the `catch`. The existing suite already locks the reset on the **error**
path (`createOrder fail → … idle`) and the **early-return** path (`no
userInfo.uid … idle (#1102)`), but the two **success** paths only
asserted `window.open` — not the modal close + loading clear. This PR
adds those two assertions so the upcoming extraction is guarded on all
three exit paths (payment path → no behavior drift tolerated).

## Verification

- `pnpm test:unit …/SubscriptionPanel.unit.spec.tsx` → 47 passed (45
existing + 2 new)
- `eslint` clean on the changed file; full-repo `tsc --noEmit` clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Characterization tests (test-first, no production change) pinning that a **successful** Stripe or Antom subscription checkout closes the `PaymentMethodModal` and clears the per-plan loading state — ahead of a follow-up that extracts the repeated checkout-reset triplet into a shared helper.

## Why

`handlePaymentMethodSelect` resets three pieces of state on every exit path:

```
setPaymentMethodPending(null)
setCheckoutProcessingChannel(null)
setIsLoading(null)
```

This triplet appears three times — Stripe success, Antom success, and the `catch`. The existing suite already locks the reset on the **error** path (`createOrder fail → … idle`) and the **early-return** path (`no userInfo.uid … idle (#1102)`), but the two **success** paths only asserted `window.open` — not the modal close + loading clear. This PR adds those two assertions so the upcoming extraction is guarded on all three exit paths (payment path → no behavior drift tolerated).

## Verification

- `pnpm test:unit …/SubscriptionPanel.unit.spec.tsx` → 47 passed (45 existing + 2 new)
- `eslint` clean on the changed file; full-repo `tsc --noEmit` clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [4827c673](https://github.com/SerendipityOneInc/ecap-workspace/commit/4827c6737524ba4d6733bad3666882d087eef546)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T17:51:23Z
- **PR**: #2123

### Commit Message

```
refactor(web): consolidate Composio connector action handlers into runAction (#2123)

## What

Replace the five near-identical Composio connector action handlers
(`connectProvider` / `disconnectProvider` / `enableProvider` /
`disableProvider` / `refreshStatus`) with one `runAction` helper plus
five intent-only wrappers.

## Why

All five handlers were copies of the same lifecycle:

```
setActionError(null)
setPendingAction({ provider, action })
try { await <api call>; setLastSyncState(...) }
catch { setActionError(t('composioConnectors.errors.<key>', { error: errorMessage(error, t('common.error')) })) }
finally { setPendingAction(c => c?.provider === provider && c.action === action ? null : c) }
```

Five copies of that block are drift-prone — a fix to the pending-reset
or error-formatting logic has to be applied five times. `runAction` owns
the shape; each handler now declares only what is unique: its API call,
its error key, and — for `connect` — the OAuth popup it must `close()`
on failure (`onError`) and the `pendingOAuth` sync state.

This is a structural DRY change, not a line-count play (net ≈ −5 lines;
the helper's type signature offsets the raw savings). The value is a
single source of truth for the action lifecycle.

## Behavior preserved

No functional change. Ordering, the `'__refresh__'` pending sentinel,
the connect popup teardown, and every `composioConnectors.errors.*` key
are identical. Pinned by `ComposioConnectorsClient.unit.spec.tsx`:
- per-action success (enable/disable/disconnect, connect OAuth open,
refresh refetch)
- pending-button feedback while an action is in flight
- per-action error messages (connect / disconnect / disable / enable) —
the error-key mapping landed in #2121 specifically to guard this
refactor

## Verification

- `pnpm test:unit …/ComposioConnectorsClient.unit.spec.tsx` → 17 passed
- full-repo `tsc --noEmit` clean; `eslint` clean; `pnpm dup:src` under
threshold

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Replace the five near-identical Composio connector action handlers (`connectProvider` / `disconnectProvider` / `enableProvider` / `disableProvider` / `refreshStatus`) with one `runAction` helper plus five intent-only wrappers.

## Why

All five handlers were copies of the same lifecycle:

```
setActionError(null)
setPendingAction({ provider, action })
try { await <api call>; setLastSyncState(...) }
catch { setActionError(t('composioConnectors.errors.<key>', { error: errorMessage(error, t('common.error')) })) }
finally { setPendingAction(c => c?.provider === provider && c.action === action ? null : c) }
```

Five copies of that block are drift-prone — a fix to the pending-reset or error-formatting logic has to be applied five times. `runAction` owns the shape; each handler now declares only what is unique: its API call, its error key, and — for `connect` — the OAuth popup it must `close()` on failure (`onError`) and the `pendingOAuth` sync state.

This is a structural DRY change, not a line-count play (net ≈ −5 lines; the helper's type signature offsets the raw savings). The value is a single source of truth for the action lifecycle.

## Behavior preserved

No functional change. Ordering, the `'__refresh__'` pending sentinel, the connect popup teardown, and every `composioConnectors.errors.*` key are identical. Pinned by `ComposioConnectorsClient.unit.spec.tsx`:
- per-action success (enable/disable/disconnect, connect OAuth open, refresh refetch)
- pending-button feedback while an action is in flight
- per-action error messages (connect / disconnect / disable / enable) — the error-key mapping landed in #2121 specifically to guard this refactor

## Verification

- `pnpm test:unit …/ComposioConnectorsClient.unit.spec.tsx` → 17 passed
- full-repo `tsc --noEmit` clean; `eslint` clean; `pnpm dup:src` under threshold

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [f69c5b35](https://github.com/SerendipityOneInc/ecap-workspace/commit/f69c5b35e68f243aaa2de7ca316474ddf5c132fa)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T17:38:51Z
- **PR**: #2071

### Commit Message

```
test(web): unit-test layout hooks + un-exclude AppLayout/ClientLayout + ratchet (#2071) (#2126)

## What

PR **3 of 3 — closes #2071**. Adds direct unit tests for the units PR 2
extracted, removes the two layout shells from `coverage.exclude`,
deletes two stale dead exclude lines, and ratchets thresholds.

### Tests
- **`tests/unit/hooks/useResponsiveLayout.unit.spec.tsx`** — mount
state, 768/1280 breakpoint behaviour, resize transitions, canvas
auto-collapse, setters, resize-listener teardown. Explicit `cleanup()`
(no testing-library auto-cleanup here — otherwise the hook's resize
listener leaks onto `window` and contaminates later specs).
- **`tests/unit/lib/env.unit.spec.ts`** — `isBillingMockEnabled` across
development / staging / production / test via `vi.stubEnv` (the inline
`NODE_ENV` branch is dead under vitest and any test of it would be
vacuous).
- **`tests/unit/lib/i18n/config.unit.spec.ts`** — `isLandingPagePath` +
`isGuideTourSuppressedPath` edge cases (locale prefixes, trailing slash,
null pathname → both non-landing / not-suppressed, matching the real
null-coalescing behaviour).

### `vitest.config.mts`
- **Un-exclude** `AppLayout.tsx` / `ClientLayout.tsx` — their logic now
lives in tested hooks/helpers, so the render layer belongs in the
coverage pool.
- **Delete two stale dead lines** `SideMenu.tsx` / `PageHeader.tsx` —
neither file exists (confirmed via `git log --all`); governance rot. See
the [#2071
comment](https://github.com/SerendipityOneInc/ecap-workspace/issues/2071#issuecomment-4583378814)
documenting the stale issue description.
- **Ratchet** `floor(observed − 1.5)`: branches 75→**76**, functions
81→**82** (statements/lines unchanged). Observed: stmts 85.30 / branches
77.62 / funcs 83.60 / lines 87.20.

## Verification
- Full suite **447 files / 6704 tests pass** with `--coverage` (exit 0)
at the new thresholds
- New specs: 28 tests, green standalone and in-suite
- `npx tsc --noEmit`: clean · `pnpm exec eslint`: clean

## Series recap
- #2119 — PR 1 characterize (merged)
- #2120 — PR 2 extract hooks (merged)
- this — PR 3 test + un-exclude + ratchet → closes #2071

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [ccbba162](https://github.com/SerendipityOneInc/ecap-workspace/commit/ccbba162c2bbcbdb885323daeeb2c71e8dee667b)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T17:20:12Z
- **PR**: #1524

### Commit Message

```
test(web): lock react-hooks lint rules at error via config regression test (#1524) (#2122)

## What

Adds a config-level regression test
(`web/app/tests/unit/lint/react-hooks-config.unit.spec.ts`) that
resolves the project's effective ESLint flat config via
`ESLint#calculateConfigForFile` and asserts:

- `react-hooks/rules-of-hooks` + `react-hooks/exhaustive-deps` resolve
to **error** for `src/**`
- `react-hooks/exhaustive-deps` resolves to **error** for `tests/**`

## Why (#1524)

`eslint.config.mjs` already re-declares these rules at `error` so the
contract is *explicit*. But an explicit declaration can still be
silently undone — a later override block, an upstream
`next/core-web-vitals` default flip, or a preset swap could drop
coverage with **no signal** (unlike a mistyped rule name, which fails
loudly as "rule not found"). This test turns the explicit contract into
an **enforced contract**: disabling or downgrading either rule turns the
build red.

### Context: #1524 was almost entirely already shipped
Investigating #1524 showed its issue body is stale — nearly every
checklist item already landed via other PRs:

| #1524 item | current state |
|---|---|
| `.vscode/extensions.json` recommends eslint ext | ✅ present
(`dbaeumer.vscode-eslint`) |
| `.vscode/settings.json` eslint fields | ✅
`eslint.workingDirectories→web/app` + `validate` + `codeActionsOnSave:
fixAll` |
| `rules-of-hooks: error` explicit | ✅ `eslint.config.mjs` src override
|
| `exhaustive-deps: error` (src + tests) | ✅ both overrides |
| `eslint-plugin-react-hooks` direct dep | ✅ pinned `5.2.0` |
| pre-commit lint | ✅ husky `pre-commit` runs `pnpm lint` |
| **tests 覆盖 (config regression test)** | ❌ → **this PR** |
| `react-hooks/react-compiler` rule | ⏸ deferred by design (tied to the
`eslint-config-next@16` / ~150-site note in `web/app/CLAUDE.md`) |

This PR closes the last open item from #1524's own title.

## Verification

- `pnpm test:unit tests/unit/lint/react-hooks-config.unit.spec.ts` → 2
passed
- **Falsification**: temporarily downgraded `rules-of-hooks` to `warn` →
test failed (`expected 1 to be 2`); reverted → green
- `npx tsc --noEmit` → clean
- `pnpm --filter @zooclaw/web-app lint` → clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [c8e2bc24](https://github.com/SerendipityOneInc/ecap-workspace/commit/c8e2bc24e07ba5c11667a36e753f3cbbee01e237)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T17:18:55Z
- **PR**: #2121

### Commit Message

```
test(web): lock Composio connector per-action error messages (#2121)

## What

Characterization tests (test-first, no production change) that pin the
**per-action error message** for the Composio connectors page, ahead of
a follow-up refactor that consolidates the five near-identical async
action handlers (`connectProvider` / `disconnectProvider` /
`enableProvider` / `disableProvider` / `refreshStatus`) into one shared
`runAction` helper.

## Why

The five handlers share an identical skeleton (`setActionError(null)` →
`setPendingAction` → try/`setLastSyncState` →
catch/`setActionError(t('composioConnectors.errors.<key>', …))` →
finally/reset). The riskiest surface when extracting a shared helper is
the **error-key mapping** — each action maps to a different translation
key (`createConnectLink`, `disconnect`, `enable`, `disable`,
`refreshStatus`), and `createConnectLink` notably does *not* match its
method name. This PR locks that mapping so the refactor can't silently
mis-route an error message.

## Coverage added

- `connect` → `创建 Connect Link 失败：…` (+ popup is closed on failure)
- `disconnect` → `断开 connector 失败：…`
- `disable` → `停用 connector 失败：…`

`enable`'s error path was already covered. `refresh` resolves through
`invalidateQueries` (no rejectable path to assert deterministically);
its success path is covered by the existing "refreshes both provider
catalog and connection state" test.

## Verification

- `pnpm test:unit …/ComposioConnectorsClient.unit.spec.tsx` → 17 passed
(14 existing + 3 new)
- `eslint` clean on the changed file; full-repo `tsc --noEmit` clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Characterization tests (test-first, no production change) that pin the **per-action error message** for the Composio connectors page, ahead of a follow-up refactor that consolidates the five near-identical async action handlers (`connectProvider` / `disconnectProvider` / `enableProvider` / `disableProvider` / `refreshStatus`) into one shared `runAction` helper.

## Why

The five handlers share an identical skeleton (`setActionError(null)` → `setPendingAction` → try/`setLastSyncState` → catch/`setActionError(t('composioConnectors.errors.<key>', …))` → finally/reset). The riskiest surface when extracting a shared helper is the **error-key mapping** — each action maps to a different translation key (`createConnectLink`, `disconnect`, `enable`, `disable`, `refreshStatus`), and `createConnectLink` notably does *not* match its method name. This PR locks that mapping so the refactor can't silently mis-route an error message.

## Coverage added

- `connect` → `创建 Connect Link 失败：…` (+ popup is closed on failure)
- `disconnect` → `断开 connector 失败：…`
- `disable` → `停用 connector 失败：…`

`enable`'s error path was already covered. `refresh` resolves through `invalidateQueries` (no rejectable path to assert deterministically); its success path is covered by the existing "refreshes both provider catalog and connection state" test.

## Verification

- `pnpm test:unit …/ComposioConnectorsClient.unit.spec.tsx` → 17 passed (14 existing + 3 new)
- `eslint` clean on the changed file; full-repo `tsc --noEmit` clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [9d193aa2](https://github.com/SerendipityOneInc/ecap-workspace/commit/9d193aa2f318670f2546fd00d4af03bf15948da2)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T17:17:49Z
- **PR**: #2071

### Commit Message

```
refactor(web): extract AppLayout/ClientLayout logic into hooks (#2071) (#2120)

## What

PR **2 of 3** for #2071. Extracts the testable logic out of `AppLayout`
and `ClientLayout` (coverage-excluded as "Pure UI") into hooks + pure
helpers, so PR 3 can un-exclude them and ratchet thresholds. **Behaviour
unchanged** — the PR-1 characterization tests are the zero-change gate
and stay green (23/23).

### New units
- **`src/hooks/useResponsiveLayout.ts`** — sidebar collapse /
mobile-menu state + the single resize listener coupling the **768**
(mobile force-collapse) and **1280** (auto-expand) breakpoints. Kept
hand-rolled on purpose: `useMediaQuery` returns one boolean per query
and can't express the coupled transition in one listener (forcing it
would be a behaviour change).
- **`src/lib/i18n/config.ts`** — `isLandingPagePath` +
`isGuideTourSuppressedPath`, pure path predicates next to the existing
`isAppPath`. Server-safe (no `'use client'`).
- **`src/lib/env.ts`** — `isBillingMockEnabled`, pure env gate. Isolated
so the dev/staging branch is unit-testable — an inline `NODE_ENV` check
is dead under vitest (`NODE_ENV==='test'`) and any test of it would be
vacuous.

### Left intentionally inline
The module-level `ReactQueryDevtools` `dynamic()` gate stays as-is: it
runs at **import time**, and hookifying it would re-trigger the dynamic
import per render and defeat the documented production-bundle exclusion.

## Verification
- PR-1 characterization specs: **23 passed** (stable x3) — zero
behaviour change
- `npx tsc --noEmit`: clean
- `pnpm exec eslint` (all changed files): clean
- `pnpm dup:src`: pass (3.68%)

## Next
- **PR 3** — direct unit tests for the new hook + pure helpers; remove
`AppLayout`/`ClientLayout` from `coverage.exclude`; delete the 2 stale
dead lines (`SideMenu.tsx` / `PageHeader.tsx`); ratchet thresholds
`floor(observed-1.5)`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [a5bbafb8](https://github.com/SerendipityOneInc/ecap-workspace/commit/a5bbafb8c4fbec02f939d4b8fadb01401a073774)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T17:01:39Z
- **PR**: #2071

### Commit Message

```
test(web): characterize AppLayout/ClientLayout before hook extraction (#2071) (#2119)

## What

PR **1 of 3** for #2071 (test-lock-first → extract →
un-exclude+ratchet). Adds render-level characterization tests that pin
the **current** behavior of `AppLayout` and `ClientLayout` — two layout
shells currently blanket-excluded from coverage as "Pure UI" but which
actually carry logic. No `src/` changes.

- **AppLayout** (`tests/unit/components/AppLayout.unit.spec.tsx`):
landing-page vs app-page branch; responsive `isMobile` + canvas
auto-collapse; `>=1280` auto-expand; mobile drawer toggle; 768/1280
resize transitions; resize-listener teardown on unmount.
- **ClientLayout** (`tests/unit/components/ClientLayout.unit.spec.tsx`):
`BillingMockSelector` env gate across development / staging /
production; `GuideTourGlobal` public-path suppression.

## ⚠️ Issue description is partly stale (see [#2071
comment](https://github.com/SerendipityOneInc/ecap-workspace/issues/2071#issuecomment-4583378814))

Verified against the real tree:
- `src/components/SideMenu.tsx` and `src/components/PageHeader.tsx`
**don't exist** (no git history) — they're dead `coverage.exclude`
lines, to be deleted in PR 3.
- `ClientLayout` has **no auth gate** (no `PUBLIC_PATHS` / redirect /
`useUser`); it's a provider-tree wrapper.

So the corrected scope targets the two real logic-bearing files:
`AppLayout` + `ClientLayout`. Design spec:
`docs/superpowers/specs/2026-05-30-issue-2071-layout-hooks-extraction.md`.

## Next PRs
- **PR 2** — extract `useResponsiveLayout` + pure `isLandingPagePath` /
`isBillingMockEnabled` / `isGuideTourSuppressedPath`; slim the two
components. These tests are the zero-behavior-change gate.
- **PR 3** — direct hook/pure-fn unit tests; remove
`AppLayout`/`ClientLayout` from `coverage.exclude`; delete the 2 stale
lines; ratchet thresholds `floor(observed-1.5)`.

## Verification
- `pnpm exec vitest run` both specs: **23 passed** (stable across 3
runs)
- `npx tsc --noEmit`: clean
- `pnpm exec eslint` both files: clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [0bc2b4c9](https://github.com/SerendipityOneInc/ecap-workspace/commit/0bc2b4c966b4463e38e39ea99068b0ef519cde75)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T16:47:28Z
- **PR**: #2118

### Commit Message

```
refactor(web): replace ImagePreview prop-sync effect with render-time adjustment (#2118)

## 背景

usehooks-ts DOM-listener 清理收尾后，扫描这批 touched 文件里残留的反模式 `useEffect`。绝大多数
touched 代码是干净的（`ModelSelector` 的 render-time tab
调整、`useMattermostConnection` 的 getter-ref 都是**正确**模式，非反模式）。**唯一**一处真正的
`useEffect` 反模式在 `ImagePreview`。

## 问题：reset-state-on-prop-change via effect

```tsx
// before — post-paint effect resets load state on controlled currentIndex change
useEffect(() => {
  if (currentIndex !== undefined) {
    setInternalIndex(currentIndex)
    setImageLoaded(false)
    setImageError(false)
  }
}, [currentIndex])
```

这是 React [You Might Not Need an Effect — "adjusting state when a prop
changes"](https://react.dev/learn/you-might-not-need-an-effect#adjusting-some-state-when-a-prop-changes)
点名的反模式：effect 在 paint 之后才跑，父组件切到新图的那一帧会闪现「上一张已 loaded」（preview img 不
hidden），下一帧才 reset。

## 改法：render-time adjustment（与 ModelSelector 一致）

```tsx
const [lastCurrentIndex, setLastCurrentIndex] = useState(currentIndex)
if (currentIndex !== undefined && currentIndex !== lastCurrentIndex) {
  setLastCurrentIndex(currentIndex)
  setInternalIndex(currentIndex)
  setImageLoaded(false)
  setImageError(false)
}
```

触发条件与原 effect 完全一致（currentIndex 变化且 defined），动作一致，只是渲染期完成 → 无
effect、无闪烁。不动 goPrev/goNext handler。

## test-first

新增 characterizing test：load image 0 → rerender `currentIndex={1}` → 断言新图
preview `<img>` 重新 `hidden`（loaded 已 reset）。先对**当前 effect
代码**跑过，转换后仍全绿（**33 测**）。`tsc` / `eslint` 0。

## 扫描结论（为何只有这一处）

- `ModelSelector` render-time tab 调整 / `ClawPageHeader` closeConfirm
handler → 已是正确模式（reject 误报）
- `useMattermostConnection` 顶部 `xxxRef.current = state` → WS 异步回调
live-read 的 getter 模式，by-design（reject）
- `LoginModal` transition
state-machine、`ArtifactPreview`/`ConnectorsSection` 的 `useMemo` → 非
`useEffect` / 动画时序 / 属既有逻辑，本次不动
- frozen 模块（`canvas/`、`example-showcase/`）不动

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

usehooks-ts DOM-listener 清理收尾后，扫描这批 touched 文件里残留的反模式 `useEffect`。绝大多数 touched 代码是干净的（`ModelSelector` 的 render-time tab 调整、`useMattermostConnection` 的 getter-ref 都是**正确**模式，非反模式）。**唯一**一处真正的 `useEffect` 反模式在 `ImagePreview`。

## 问题：reset-state-on-prop-change via effect

```tsx
// before — post-paint effect resets load state on controlled currentIndex change
useEffect(() => {
  if (currentIndex !== undefined) {
    setInternalIndex(currentIndex)
    setImageLoaded(false)
    setImageError(false)
  }
}, [currentIndex])
```

这是 React [You Might Not Need an Effect — "adjusting state when a prop changes"](https://react.dev/learn/you-might-not-need-an-effect#adjusting-some-state-when-a-prop-changes) 点名的反模式：effect 在 paint 之后才跑，父组件切到新图的那一帧会闪现「上一张已 loaded」（preview img 不 hidden），下一帧才 reset。

## 改法：render-time adjustment（与 ModelSelector 一致）

```tsx
const [lastCurrentIndex, setLastCurrentIndex] = useState(currentIndex)
if (currentIndex !== undefined && currentIndex !== lastCurrentIndex) {
  setLastCurrentIndex(currentIndex)
  setInternalIndex(currentIndex)
  setImageLoaded(false)
  setImageError(false)
}
```

触发条件与原 effect 完全一致（currentIndex 变化且 defined），动作一致，只是渲染期完成 → 无 effect、无闪烁。不动 goPrev/goNext handler。

## test-first

新增 characterizing test：load image 0 → rerender `currentIndex={1}` → 断言新图 preview `<img>` 重新 `hidden`（loaded 已 reset）。先对**当前 effect 代码**跑过，转换后仍全绿（**33 测**）。`tsc` / `eslint` 0。

## 扫描结论（为何只有这一处）

- `ModelSelector` render-time tab 调整 / `ClawPageHeader` closeConfirm handler → 已是正确模式（reject 误报）
- `useMattermostConnection` 顶部 `xxxRef.current = state` → WS 异步回调 live-read 的 getter 模式，by-design（reject）
- `LoginModal` transition state-machine、`ArtifactPreview`/`ConnectorsSection` 的 `useMemo` → 非 `useEffect` / 动画时序 / 属既有逻辑，本次不动
- frozen 模块（`canvas/`、`example-showcase/`）不动

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [0bed8054](https://github.com/SerendipityOneInc/ecap-workspace/commit/0bed8054662db981bd923445beb9f70695fc788f)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T16:47:06Z
- **PR**: #2116

### Commit Message

```
refactor(web): converge OnboardingLayout Escape to useEscapeKey (test-first) (#2116)

## 背景

issue #2072 follow-up（DOM `addEventListener`，纯 ergonomics）**收尾 PR**。接续
#2106 / #2108 / #2111 / #2112 / #2115。#2072 主线已由 Zustand epic #2113
CLOSED。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md`（已标
DONE）。

## 本 PR：OnboardingLayout entangled-Escape → `useEscapeKey`（test-first）

`OnboardingLayout` 的 keydown Escape（`handleKeyDown` `useCallback` 只做
`Escape→onClose`，可干净分离）抽成 `useEscapeKey(onClose)`；原本和 keydown 合并的 effect
收成**纯 body-lock**（单一职责）：

```diff
-  const handleKeyDown = useCallback((e) => { if (e.key === 'Escape') onClose() }, [onClose])
-  useEffect(() => {
-    window.addEventListener('keydown', handleKeyDown)
-    document.documentElement.classList.add('overflow-hidden')
-    return () => { window.removeEventListener('keydown', handleKeyDown); document.documentElement.classList.remove('overflow-hidden') }
-  }, [handleKeyDown])
+  useEscapeKey(onClose)
+  useEffect(() => {
+    document.documentElement.classList.add('overflow-hidden')
+    return () => document.documentElement.classList.remove('overflow-hidden')
+  }, [])
```

window→document 同 `LoginModal`（生产无差异，真实 Escape 在两者都触发）。

## test-first

新增 `OnboardingLayout.unit.spec.tsx`（framer-motion mock + matchMedia
stub），**3 测**：Escape closes / 非 Escape 忽略 / body-lock
mount+unmount。先对**当前 window-based 代码**跑过（`fireEvent.keyDown` 冒泡到
window），迁移后仍全绿 → 锁定行为零漂移。

## ExamplePreviewModal 为何不迁（spec 记）

在 frozen 模块 `example-showcase/`（knip ignore + coverage exclude，无测试网），且
Escape 埋在 **dual-return**（else 分支 `clearTimeout` + 底部 return）的
body-overflow/transition effect 里——frozen 模块做纯 ergonomics 手术风险 > 收益，与
`canvas/` 同策略保留手写。

## 验证
- ✅ `OnboardingLayout.unit.spec.tsx` 3/3
- ✅ `tsc` / `eslint` 0

## 收尾
至此 usehooks-ts DOM-listener 清理 **6 PR 闭环**。merge 后我在 #2072 补 follow-up
完结 comment（对齐 createObjectURL follow-up 格式）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

issue #2072 follow-up（DOM `addEventListener`，纯 ergonomics）**收尾 PR**。接续 #2106 / #2108 / #2111 / #2112 / #2115。#2072 主线已由 Zustand epic #2113 CLOSED。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md`（已标 DONE）。

## 本 PR：OnboardingLayout entangled-Escape → `useEscapeKey`（test-first）

`OnboardingLayout` 的 keydown Escape（`handleKeyDown` `useCallback` 只做 `Escape→onClose`，可干净分离）抽成 `useEscapeKey(onClose)`；原本和 keydown 合并的 effect 收成**纯 body-lock**（单一职责）：

```diff
-  const handleKeyDown = useCallback((e) => { if (e.key === 'Escape') onClose() }, [onClose])
-  useEffect(() => {
-    window.addEventListener('keydown', handleKeyDown)
-    document.documentElement.classList.add('overflow-hidden')
-    return () => { window.removeEventListener('keydown', handleKeyDown); document.documentElement.classList.remove('overflow-hidden') }
-  }, [handleKeyDown])
+  useEscapeKey(onClose)
+  useEffect(() => {
+    document.documentElement.classList.add('overflow-hidden')
+    return () => document.documentElement.classList.remove('overflow-hidden')
+  }, [])
```

window→document 同 `LoginModal`（生产无差异，真实 Escape 在两者都触发）。

## test-first

新增 `OnboardingLayout.unit.spec.tsx`（framer-motion mock + matchMedia stub），**3 测**：Escape closes / 非 Escape 忽略 / body-lock mount+unmount。先对**当前 window-based 代码**跑过（`fireEvent.keyDown` 冒泡到 window），迁移后仍全绿 → 锁定行为零漂移。

## ExamplePreviewModal 为何不迁（spec 记）

在 frozen 模块 `example-showcase/`（knip ignore + coverage exclude，无测试网），且 Escape 埋在 **dual-return**（else 分支 `clearTimeout` + 底部 return）的 body-overflow/transition effect 里——frozen 模块做纯 ergonomics 手术风险 > 收益，与 `canvas/` 同策略保留手写。

## 验证
- ✅ `OnboardingLayout.unit.spec.tsx` 3/3
- ✅ `tsc` / `eslint` 0

## 收尾
至此 usehooks-ts DOM-listener 清理 **6 PR 闭环**。merge 后我在 #2072 补 follow-up 完结 comment（对齐 createObjectURL follow-up 格式）。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [8483d790](https://github.com/SerendipityOneInc/ecap-workspace/commit/8483d79084c3c024976c326785d91da07e42e294)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T16:44:10Z
- **PR**: #2117

### Commit Message

```
refactor(web): single-source billing query key + extract tick-counter store factory (#2117)

## Summary

Post-merge follow-up to PR #2113 (the #2072 Zustand store migration epic
finale). Two small refactors found during a code-quality pass over the
merged epic.

### A. Single-source `creditsQueryKey` via `lib/query/keys.ts`

`lib/billing-credits.ts::triggerCreditsRefresh` inlined a literal copy
of the credits query key to avoid the W1 import boundary (`lib/` →
`hooks/` forbidden), with a comment flagging the silent-drift hazard
against `billingKeys.credits` in `hooks/queries/billing/keys.ts`. The
existing repo convention for this exact situation is
`*_QUERY_KEY_PREFIX` consts in `lib/query/keys.ts` (see
`AGENTS_QUERY_KEY_PREFIX` / `CRON_JOBS_QUERY_KEY_PREFIX` / etc.), which
both Layer 2 imperative code and Layer 3 key factories can consume.

- `lib/query/keys.ts` — adds `BILLING_CREDITS_QUERY_KEY_PREFIX`
- `hooks/queries/billing/keys.ts` — `credits: (uid) => [...PREFIX, uid]`
- `lib/billing-credits.ts` — drops the inline + the W1-workaround
comment

Eliminates the documented silent-drift hazard.

### B. `createTickCounterStore` factory

The epic ended with three near-identical tick-counter stores — same
shape (`{tick: number}`), same `bump` setter, only differing on
file/exported names and 3-4 lines of contextual docstring:

| File | Setter |
|---|---|
| `lib/login-modal-store.ts` | `requestShowLoginModal` |
| `lib/guide-tour-store.ts` | `requestOpenGuideTour` |
| `lib/credits-refresh-tick-store.ts` | `bumpCreditsRefreshTick` |

Two of them stored their counter as `requestCount` and the third as
`tick` — that mixed naming itself was an artifact of the migration
order. Collapsed onto a shared `createTickCounterStore()` factory; field
name normalized to `tick` everywhere; consumer hooks
(`useShowLoginModalRequest` / `useOpenGuideTourRequest`) and 4 affected
unit specs updated.

- `lib/create-tick-counter-store.ts` (NEW) — ~30-line factory
- `tests/unit/lib/create-tick-counter-store.unit.spec.ts` (NEW) — pins
the shared contract
- Three concrete store files each shrink to ~10 lines (factory call +
use-case comment)

Net LOC: -10 (3 thick docstrings replaced by 2-line use-case notes,
factory absorbs the shared docstring).

### Not changed: ESLint config

User asked whether any ESLint whitelist could be removed post-epic.
Audited `web/app/eslint.config.mjs` end-to-end:
- Rule 12 (added in PR #2113) is a must-be-zero regression guard, not a
temporary exemption — **keep**
- `react/forbid-dom-props` ignores list, complexity overrides, etc. are
all pre-existing items unrelated to the epic — **keep**
- No `TODO remove after #2072` markers anywhere

No ESLint changes in this PR.

## Test plan

- [x] `pnpm test:unit` — 6650 passed | 1 skipped | 1 todo (was 6633
before; +17 from new tests across factory spec + the 3 existing
tick-counter store specs that now exercise the factory through the
wrappers)
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `bash web/scripts/check-no-react-in-stores.sh` ✅ (10 files audited
— factory included)
- [x] `grep -rn "requestCount" web/app/src web/app/tests` → 0 matches
- [ ] CI green (`code-quality`, Claude/Codex review, CodeQL)

Follow-up to: #2113 (closed #2072).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Description

## Summary

Post-merge follow-up to PR #2113 (the #2072 Zustand store migration epic finale). Two small refactors found during a code-quality pass over the merged epic.

### A. Single-source `creditsQueryKey` via `lib/query/keys.ts`

`lib/billing-credits.ts::triggerCreditsRefresh` inlined a literal copy of the credits query key to avoid the W1 import boundary (`lib/` → `hooks/` forbidden), with a comment flagging the silent-drift hazard against `billingKeys.credits` in `hooks/queries/billing/keys.ts`. The existing repo convention for this exact situation is `*_QUERY_KEY_PREFIX` consts in `lib/query/keys.ts` (see `AGENTS_QUERY_KEY_PREFIX` / `CRON_JOBS_QUERY_KEY_PREFIX` / etc.), which both Layer 2 imperative code and Layer 3 key factories can consume.

- `lib/query/keys.ts` — adds `BILLING_CREDITS_QUERY_KEY_PREFIX`
- `hooks/queries/billing/keys.ts` — `credits: (uid) => [...PREFIX, uid]`
- `lib/billing-credits.ts` — drops the inline + the W1-workaround comment

Eliminates the documented silent-drift hazard.

### B. `createTickCounterStore` factory

The epic ended with three near-identical tick-counter stores — same shape (`{tick: number}`), same `bump` setter, only differing on file/exported names and 3-4 lines of contextual docstring:

| File | Setter |
|---|---|
| `lib/login-modal-store.ts` | `requestShowLoginModal` |
| `lib/guide-tour-store.ts` | `requestOpenGuideTour` |
| `lib/credits-refresh-tick-store.ts` | `bumpCreditsRefreshTick` |

Two of them stored their counter as `requestCount` and the third as `tick` — that mixed naming itself was an artifact of the migration order. Collapsed onto a shared `createTickCounterStore()` factory; field name normalized to `tick` everywhere; consumer hooks (`useShowLoginModalRequest` / `useOpenGuideTourRequest`) and 4 affected unit specs updated.

- `lib/create-tick-counter-store.ts` (NEW) — ~30-line factory
- `tests/unit/lib/create-tick-counter-store.unit.spec.ts` (NEW) — pins the shared contract
- Three concrete store files each shrink to ~10 lines (factory call + use-case comment)

Net LOC: -10 (3 thick docstrings replaced by 2-line use-case notes, factory absorbs the shared docstring).

### Not changed: ESLint config

User asked whether any ESLint whitelist could be removed post-epic. Audited `web/app/eslint.config.mjs` end-to-end:
- Rule 12 (added in PR #2113) is a must-be-zero regression guard, not a temporary exemption — **keep**
- `react/forbid-dom-props` ignores list, complexity overrides, etc. are all pre-existing items unrelated to the epic — **keep**
- No `TODO remove after #2072` markers anywhere

No ESLint changes in this PR.

## Test plan

- [x] `pnpm test:unit` — 6650 passed | 1 skipped | 1 todo (was 6633 before; +17 from new tests across factory spec + the 3 existing tick-counter store specs that now exercise the factory through the wrappers)
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `bash web/scripts/check-no-react-in-stores.sh` ✅ (10 files audited — factory included)
- [x] `grep -rn "requestCount" web/app/src web/app/tests` → 0 matches
- [ ] CI green (`code-quality`, Claude/Codex review, CodeQL)

Follow-up to: #2113 (closed #2072).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [008f7369](https://github.com/SerendipityOneInc/ecap-workspace/commit/008f7369339130398985b0dff1b3200fd01d30fd)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T16:23:14Z
- **PR**: #2069

### Commit Message

```
test(web): extract PublicPricingClient pure logic to pricing/lib + unit tests (#2069) (#2114)

## What & why

`PublicPricingClient.tsx` (~700 LoC) sat fully in `vitest.config.mts`
`coverage.exclude` as a "branded page". The #2068 exclusion audit
flagged this: **branded is a styling constraint, unrelated to logic
tests** — the file's price math and plan-selection branches had zero
unit-test protection.

This PR extracts the genuinely pure, regression-prone logic into
`pricing/lib/` and unit-tests it. The render layer **stays excluded**
(branded standalone palette is jsdom-incompatible; that part of the
rationale still holds).

Closes #2069.

## Changes

- **`pricing/lib/pricingHelpers.ts`** — `getPrice` (the billing-cycle
branch), `formatPrice`, `getYearlyTotalLabel`, `getStarterDisplayPrice`
(+ `STARTER_OLD_PRICE`). State the component used to read from a closure
is now passed in explicitly.
- **`pricing/lib/planSelection.ts`** — `getChoosePlanAction` (the
plan-selection CTA decision, split out as a pure discriminated union
from the side-effectful `handleChoosePlan`) and `isCurrentPlan`.
- **`PublicPricingClient.tsx`** — closures now delegate to the lib fns;
**all JSX is byte-identical** (behavior unchanged). `PLAN_PRICING`
import dropped (moved to lib).
- **15 unit specs** in `tests/unit/pricing/` covering the two
acceptance-named branches (billing-cycle + plan-selection); both lib
files report **100%** on all metrics.
- **`vitest.config.mts`** — exclude comment updated to: *"helpers
extracted to pricing/lib, render layer stays excluded for branded
styling reasons (#2069)"*.

## Verification

- `tsc --noEmit` clean; `eslint` clean.
- New specs: 15/15 pass. Full suite passes with coverage above the
ratchet floor (stmts 84.55 ≥ 83 / branches 76.95 ≥ 75 / funcs 83.43 ≥ 81
/ lines 86.67 ≥ 85). Thresholds left unchanged — 100%-covered helpers
only lift the numbers.
- Falsifiability check: mutating `Math.ceil`→`Math.floor` in `getPrice`
turns the two rounding-contract specs red; restored → green.

## Out of scope (per issue)

No whole-component render test, no styling rewrite (#796/#894), no
nav-links / timing-constant / `getPlanInfo` extraction (render-config /
vacuous-test territory).

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

---

## [5bf86997](https://github.com/SerendipityOneInc/ecap-workspace/commit/5bf869979a88915a7ee21952ed8529c648cba85f)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T16:22:08Z
- **PR**: #2115

### Commit Message

```
refactor(web): migrate matchMedia hooks to usehooks-ts useMediaQuery (#2115)

## 背景

issue #2072 follow-up（DOM `addEventListener`，纯 ergonomics）。接续 PR1 #2106
/ PR2 #2108 / PR3 #2111 /
#2112。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md`（matchMedia
节）。

## 本 PR：2 个 matchMedia change-listener → `useMediaQuery`

| hook | query |
|---|---|
| `ReplayPlayer.usePrefersReducedMotion` | `(prefers-reduced-motion:
reduce)` |
| `OnboardingLayout.useIsDesktop` | `(min-width: 1024px)` |

每个 ~10 行 `useState + mount effect + add/removeEventListener` → 1 行。

### `{ initializeWithValue: false }`（关键）

两个 hook 原本是 `useState(false) + mount effect` **惰性**模式：首屏返回 `false`、mount
后才读 matchMedia。`useMediaQuery` 默认 `initializeWithValue: true` 会在 client
首屏**同步**读真值，与 SSR 渲染的 `false` 不一致 → **hydration mismatch**。传 `{
initializeWithValue: false }` 精确复刻原惰性行为、SSR 安全。

## 排除（非 listener / 非站点，见 spec）

- `layout.tsx`（defensive inline-script 字符串）、`ChatErrorBoundary`（一次性
`.matches` 读）—— 非 React change listener
- `useReplayPlayer.ts` —— `reducedMotion` 当**入参**接收，不自调 matchMedia

## 验证

- ✅ `ReplayPlayer` 既有 spec 已 `vi.stubGlobal('matchMedia', ...)`（mql mock
含 `matches`/`addEventListener`/`removeEventListener`，与 `useMediaQuery`
兼容），**24 测全绿**作 oracle。
- 注：`useMediaQuery` effect 直接 `window.matchMedia(query)`（无 guard，不同于原
hook 的 `if(!window.matchMedia)return`），jsdom 下必须 stub —— 既有 spec 已满足。
- ✅ `tsc` / `eslint` 0。

## 剩余（最后一项）

仅剩 **entangled-Escape**（`ExamplePreviewModal` / `OnboardingLayout`
keydown，与 body-overflow effect 同体且无 spec）→ test-first 收尾 PR，之后在 issue
#2072 补 follow-up 完结 comment。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

issue #2072 follow-up（DOM `addEventListener`，纯 ergonomics）。接续 PR1 #2106 / PR2 #2108 / PR3 #2111 / #2112。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md`（matchMedia 节）。

## 本 PR：2 个 matchMedia change-listener → `useMediaQuery`

| hook | query |
|---|---|
| `ReplayPlayer.usePrefersReducedMotion` | `(prefers-reduced-motion: reduce)` |
| `OnboardingLayout.useIsDesktop` | `(min-width: 1024px)` |

每个 ~10 行 `useState + mount effect + add/removeEventListener` → 1 行。

### `{ initializeWithValue: false }`（关键）

两个 hook 原本是 `useState(false) + mount effect` **惰性**模式：首屏返回 `false`、mount 后才读 matchMedia。`useMediaQuery` 默认 `initializeWithValue: true` 会在 client 首屏**同步**读真值，与 SSR 渲染的 `false` 不一致 → **hydration mismatch**。传 `{ initializeWithValue: false }` 精确复刻原惰性行为、SSR 安全。

## 排除（非 listener / 非站点，见 spec）

- `layout.tsx`（defensive inline-script 字符串）、`ChatErrorBoundary`（一次性 `.matches` 读）—— 非 React change listener
- `useReplayPlayer.ts` —— `reducedMotion` 当**入参**接收，不自调 matchMedia

## 验证

- ✅ `ReplayPlayer` 既有 spec 已 `vi.stubGlobal('matchMedia', ...)`（mql mock 含 `matches`/`addEventListener`/`removeEventListener`，与 `useMediaQuery` 兼容），**24 测全绿**作 oracle。
  - 注：`useMediaQuery` effect 直接 `window.matchMedia(query)`（无 guard，不同于原 hook 的 `if(!window.matchMedia)return`），jsdom 下必须 stub —— 既有 spec 已满足。
- ✅ `tsc` / `eslint` 0。

## 剩余（最后一项）

仅剩 **entangled-Escape**（`ExamplePreviewModal` / `OnboardingLayout` keydown，与 body-overflow effect 同体且无 spec）→ test-first 收尾 PR，之后在 issue #2072 补 follow-up 完结 comment。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [bd411195](https://github.com/SerendipityOneInc/ecap-workspace/commit/bd4111954557f8b6259229a533c3ac6d69962c32)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T16:21:16Z
- **PR**: #2072

### Commit Message

```
refactor(web): replace credits/login-modal/guide-tour events with zustand + lint guard (#2072) (#2113)

## Summary

PR #2072 epic finale — collapses the remaining 4 `window.dispatchEvent`
broadcast channels into direct calls and adds an ESLint guard against
the 8 retired event names.

### What changed

- **`credits-refresh` / `credits-refresh-data` →
`triggerCreditsRefresh()`** invalidates the uid-scoped billing-credits
RQ key directly; mock-billing takes the `cancelQueries` path to avoid
touching real `/credits/check`. The listener-side path in
`useBillingCredits` is removed.
- **`show-login-modal` → `requestShowLoginModal()`** increments a
Zustand tick counter (`loginModalStore`); `LoginCheckProvider`
subscribes via `useShowLoginModalRequest()` + `useEffect` keyed on the
count.
- **`open-guide-tour` → `requestOpenGuideTour()`** mirrors the same
tick-counter pattern (`guideTourStore` / `useOpenGuideTourRequest`);
`GuideTourModal` consumes it.
- **`user-message-sent` deleted outright** (0 production listeners — was
a vestige).
- **ESLint `no-restricted-syntax` rule 12** blocks any new
`window.dispatchEvent(new CustomEvent('<retired-name>'))` for the full
set of 8 epic-deprecated events:
- `auth-state-changed`, `credits-refresh`, `credits-refresh-data`,
`onboarding-backend-status`, `onboarding-retry-sync`,
`show-login-modal`, `open-guide-tour`, `user-message-sent`

### Architectural note: W1 boundary fix

The credits cache mirror was extracted from `hooks/useBillingCredits.ts`
into a new `lib/billing-credits-mirror.ts` module so
`lib/billing-credits.ts` can clear it eagerly before invalidating RQ —
without crossing the `lib → hooks` import boundary enforced by
dependency-cruiser.

The mirror is intentionally NOT named `*-store.ts` (it's a plain
module-level cache, not a Zustand store), so the
`check-no-react-in-stores.sh` CI guard doesn't apply.

### Files

**New:**
- `web/app/src/lib/login-modal-store.ts` + `useShowLoginModalRequest.ts`
(vanilla split)
- `web/app/src/lib/guide-tour-store.ts` + `useOpenGuideTourRequest.ts`
(vanilla split)
- `web/app/src/lib/billing-credits-mirror.ts` (extracted from
useBillingCredits)
-
`web/app/tests/unit/lib/{login-modal-store,guide-tour-store,billing-credits-mirror}.unit.spec.ts`
(19 new tests)

**Modified:**
- `web/app/src/lib/billing-credits.ts` — `triggerCreditsRefresh` now
invalidates RQ + clears mirror (no more dispatch)
- `web/app/src/lib/auth/manager.ts` — dispatches
`requestShowLoginModal()`
- `web/app/src/components/providers/LoginCheckProvider.tsx` — subscribes
via hook
- `web/app/src/components/GuideTourModal.tsx` — subscribes via hook
- `web/app/src/components/UserMenu.tsx` — dispatches
`requestOpenGuideTour()`
- `web/app/src/components/agent-chat-client/hooks/useSendMessage.ts` —
`triggerCreditsRefresh()` + deleted `user-message-sent` dispatch
- `web/app/src/app/[locale]/canvas/hooks/useCanvasChat.ts`,
`web/app/src/lib/billing/mock-billing-data.ts` —
`triggerCreditsRefresh()`
- `web/app/src/hooks/useBillingCredits.ts` — removed listeners +
module-level mirror
- `web/app/eslint.config.mjs` — Rule 12 (no-restricted-syntax)

### Spec / Issue

- Spec: `docs/superpowers/specs/2026-05-28-zustand-store-migration.md`
- Closes #2072

## Test plan

- [x] `pnpm test:unit` — 6594 passed | 1 skipped | 1 todo (post-rebase)
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `bash web/scripts/check-no-react-in-stores.sh` ✅ 8 files audited
- [x] `grep` audit confirms no `dispatchEvent` of the 8 retired event
names remain in `web/app/src/` (only doc-comments)
- [ ] CI green (`code-quality / lint-and-test`, `auto-review`, etc.)
- [ ] Smoke: invalid login triggers global login modal; "What's New" in
user menu opens guide tour; sending a message refreshes credits

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [e1056bb8](https://github.com/SerendipityOneInc/ecap-workspace/commit/e1056bb8f8018ee02815ebfa8d010ff048537016)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T16:00:04Z
- **PR**: #2112

### Commit Message

```
refactor(web): migrate 3 document-target listeners to useEventListener (#2112)

## 背景

issue #2072 follow-up（DOM `addEventListener`，纯 ergonomics）。接续 PR1 #2106
/ PR2 #2108 / PR3
#2111。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md`
§7。

## 本 PR：3 个 document-target 监听 → `useEventListener`

统一 `useEventListener('...', handler,
useRef<Document>(globalThis.document))`：

| 文件 | 事件 |
|---|---|
| `ImagePreview` | keydown（Esc + 方向键，useEscapeKey 不够） |
| `UploadPopover` | keydown（⌘U / Ctrl+U 快捷键） |
| `useMattermostConnection` | visibilitychange（drain backfill + revive
僵尸 socket） |

**为何 document ref**：keydown 在 jsdom `fireEvent` 下 bubble、window 也能收，但
**visibilitychange 不冒泡**、window 收不到（测试 `document.dispatchEvent(new
Event('visibilitychange'))`），必须 document target；为与历史
`document.addEventListener` 一致且三处统一，keydown 也走 document ref。

## 明确 skip（理由见 spec §7）

- **canvas/ frozen**：`CanvasArea`(⌘Z) / `LayerEditorNode`(⌘C, capture) 在
`src/app/[locale]/canvas/**`——该模块被 vitest coverage exclude + knip
ignore（frozen，无测试）。纯 ergonomics 动 frozen 模块是无谓 churn。
- **生命周期纠缠**：`useOpenClawWebSocket`（visibilitychange 埋在 mount/unmount 大
effect）/ `useOpenClawVisibilityRecovery`（onVisible 内 setTimeout 由 effect
cleanup 清，useEventListener 接管会漏清）。

## 验证

- ✅ 3 个既有 spec（keydown/visibilitychange dispatch 均在 `document`）作
oracle，**59 测全绿**。
- ✅ `tsc` / `eslint` 0。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

issue #2072 follow-up（DOM `addEventListener`，纯 ergonomics）。接续 PR1 #2106 / PR2 #2108 / PR3 #2111。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md` §7。

## 本 PR：3 个 document-target 监听 → `useEventListener`

统一 `useEventListener('...', handler, useRef<Document>(globalThis.document))`：

| 文件 | 事件 |
|---|---|
| `ImagePreview` | keydown（Esc + 方向键，useEscapeKey 不够） |
| `UploadPopover` | keydown（⌘U / Ctrl+U 快捷键） |
| `useMattermostConnection` | visibilitychange（drain backfill + revive 僵尸 socket） |

**为何 document ref**：keydown 在 jsdom `fireEvent` 下 bubble、window 也能收，但 **visibilitychange 不冒泡**、window 收不到（测试 `document.dispatchEvent(new Event('visibilitychange'))`），必须 document target；为与历史 `document.addEventListener` 一致且三处统一，keydown 也走 document ref。

## 明确 skip（理由见 spec §7）

- **canvas/ frozen**：`CanvasArea`(⌘Z) / `LayerEditorNode`(⌘C, capture) 在 `src/app/[locale]/canvas/**`——该模块被 vitest coverage exclude + knip ignore（frozen，无测试）。纯 ergonomics 动 frozen 模块是无谓 churn。
- **生命周期纠缠**：`useOpenClawWebSocket`（visibilitychange 埋在 mount/unmount 大 effect）/ `useOpenClawVisibilityRecovery`（onVisible 内 setTimeout 由 effect cleanup 清，useEventListener 接管会漏清）。

## 验证

- ✅ 3 个既有 spec（keydown/visibilitychange dispatch 均在 `document`）作 oracle，**59 测全绿**。
- ✅ `tsc` / `eslint` 0。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [09e06bee](https://github.com/SerendipityOneInc/ecap-workspace/commit/09e06bee0e837a309a1499148ebf2a18e3a08a45)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T09:52:21Z
- **PR**: #2111

### Commit Message

```
refactor(web): converge 5 pure-Escape keydown handlers to useEscapeKey (#2111)

## 背景

issue #2072 的 out-of-scope follow-up（DOM `addEventListener`，纯
ergonomics）PR3 —— **keydown 批次的「纯 Escape → `useEscapeKey` 语义收敛」**。接续已合并的
PR1 #2106、PR2
#2108。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md`（§7
记录全部 keydown 分流决策）。

## 本 PR：5 个纯 Escape raw keydown → `useEscapeKey`

| 文件 | 改法 |
|---|---|
| `PaymentMethodModal` / `AgentSettingsPopover` | whole-effect 即
keydown，直接换 `useEscapeKey`；handler 逻辑（`!isProcessing` /
`showRestartPrompt`）原样保留 |
| `AgentsManagerClient` / `AgentDetailClient` | 原本用
`escapeStateRef`/`modalStateRef` 的 **ref-once 模式**（attach 一次 + ref 读最新
state，#1275）规避 cleanup/re-attach gap。`useEscapeKey` 内部 callbackRef +
监听只挂一次 同样保证「读最新 + 无空窗」→ **删掉外部 ref**，行为等价且彻底消除空窗 |
| `LoginModal` | Escape 原本和 transition timer / overflow-class 同
effect，**抽出**成独立 `useEscapeKey(onClose, isOpen)`，effect 只管
transition（单一职责） |

## 测试

- **oracle**：`AgentsManagerClient`(11) / `AgentDetailClient`(6) /
`LoginModal`(4) 既有 Escape 断言迁移后全绿。
- **target 影响**：`useEscapeKey` 监听 `document`，原 `LoginModal` 监听
`window`；既有测试 `fireEvent.keyDown(window,...)` 改成 `document`（**生产无差异**，真实
Escape 在两者都触发，仅合成事件需 dispatch 到监听所在）。
- **补测**：`PaymentMethodModal` / `AgentSettingsPopover` 原本 0 Escape 断言，本
PR 补 Escape 行为测试（含 PaymentMethodModal 的 `isProcessing` 守卫 → **非
vacuous**）。
- ✅ 5 spec 共 **91 测全绿**；`tsc` / `eslint` 0。

## 明确 skip（理由见 spec §7）

- `UserMenu`（mousedown+keydown+setTimeout，PR2 已说明）/
`useModalStackEscape`（已是良构 ref-once hook + 栈优先级逻辑）
- `ExamplePreviewModal` · `OnboardingLayout`（Escape 与 body-overflow 同
effect 且暂无 spec）→ test-first follow-up
- 多键/快捷键类 `ImagePreview`(Esc+方向键) · `UploadPopover`(⌘U) ·
`CanvasArea`(⌘Z) · `LayerEditorNode`(⌘C, capture) → `useEventListener`
follow-up
- 带 rAF 节流闭包 + 初始调用的
`scroll`/`resize`（`LandingClient`/`PublicPricingClient`/`AppLayout` 等）→
不是纯监听，迁移属行为风险重构而非 ergonomics，**保留手写**

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

issue #2072 的 out-of-scope follow-up（DOM `addEventListener`，纯 ergonomics）PR3 —— **keydown 批次的「纯 Escape → `useEscapeKey` 语义收敛」**。接续已合并的 PR1 #2106、PR2 #2108。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md`（§7 记录全部 keydown 分流决策）。

## 本 PR：5 个纯 Escape raw keydown → `useEscapeKey`

| 文件 | 改法 |
|---|---|
| `PaymentMethodModal` / `AgentSettingsPopover` | whole-effect 即 keydown，直接换 `useEscapeKey`；handler 逻辑（`!isProcessing` / `showRestartPrompt`）原样保留 |
| `AgentsManagerClient` / `AgentDetailClient` | 原本用 `escapeStateRef`/`modalStateRef` 的 **ref-once 模式**（attach 一次 + ref 读最新 state，#1275）规避 cleanup/re-attach gap。`useEscapeKey` 内部 callbackRef + 监听只挂一次 同样保证「读最新 + 无空窗」→ **删掉外部 ref**，行为等价且彻底消除空窗 |
| `LoginModal` | Escape 原本和 transition timer / overflow-class 同 effect，**抽出**成独立 `useEscapeKey(onClose, isOpen)`，effect 只管 transition（单一职责） |

## 测试

- **oracle**：`AgentsManagerClient`(11) / `AgentDetailClient`(6) / `LoginModal`(4) 既有 Escape 断言迁移后全绿。
- **target 影响**：`useEscapeKey` 监听 `document`，原 `LoginModal` 监听 `window`；既有测试 `fireEvent.keyDown(window,...)` 改成 `document`（**生产无差异**，真实 Escape 在两者都触发，仅合成事件需 dispatch 到监听所在）。
- **补测**：`PaymentMethodModal` / `AgentSettingsPopover` 原本 0 Escape 断言，本 PR 补 Escape 行为测试（含 PaymentMethodModal 的 `isProcessing` 守卫 → **非 vacuous**）。
- ✅ 5 spec 共 **91 测全绿**；`tsc` / `eslint` 0。

## 明确 skip（理由见 spec §7）

- `UserMenu`（mousedown+keydown+setTimeout，PR2 已说明）/ `useModalStackEscape`（已是良构 ref-once hook + 栈优先级逻辑）
- `ExamplePreviewModal` · `OnboardingLayout`（Escape 与 body-overflow 同 effect 且暂无 spec）→ test-first follow-up
- 多键/快捷键类 `ImagePreview`(Esc+方向键) · `UploadPopover`(⌘U) · `CanvasArea`(⌘Z) · `LayerEditorNode`(⌘C, capture) → `useEventListener` follow-up
- 带 rAF 节流闭包 + 初始调用的 `scroll`/`resize`（`LandingClient`/`PublicPricingClient`/`AppLayout` 等）→ 不是纯监听，迁移属行为风险重构而非 ergonomics，**保留手写**

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [15668827](https://github.com/SerendipityOneInc/ecap-workspace/commit/1566882732f61e299968fdbab637899a2df21762)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T09:39:28Z
- **PR**: #894

### Commit Message

```
test(web): Phase 5 finale — useMattermost orchestrator spec + ratchet (#894) (#2110)

## Summary

Closes Phase 5 of the web coverage epic (issue #894). Two changes:

1. **`useMattermost` orchestrator spec** — covers the 4-sub-hook
composition logic that PRs 1-7 deferred
2. **Ratchet thresholds** — lock the +1.76pp Phase 5 gains as the floor

## Why this is the finale (not a PR continuing toward 90%)

After PR 7 you asked: is the marginal value of each new spec actually
still worth it? Honest answer was yes (it's diminishing). Option 2 of
our discussion was: do the two architecturally important targets
(`auth/manager.ts` + `useMattermost.ts`) then ratchet.

In execution:
- **`useMattermost.ts` landed cleanly** — 26 tests, 13 of the 20 uncov
LOC covered, the orchestrator's state machine + event dispatch +
verification timeout logic now has falsifiable contracts.
- **`auth/manager.ts` deeper coverage was scoped OUT.** The 65 uncov
lines are spread across private methods (`_doSyncBusinessData`,
`_ensurePersonalOrg`, `_syncLocale`, login retry paths) where each test
requires 100+ LOC of mock setup for marginal coverage gain on
**defensive nets** rather than hot paths. The existing 78.8% baseline
already covers the critical login/logout flow. This matches the honest
assessment from the earlier discussion — the engineering cost crossed
the test contract value threshold.

So Phase 5 closes at **86.67%** rather than 90%. The original target
wasn't reached, and the ratchet locks the real gains so future PRs can't
silently regress them.

## What's in this PR

**`tests/unit/hooks/useMattermost.unit.spec.tsx`** (26 tests, ~470 LOC):

- `handlePostedEvent` guards: null post, no userId, non-posted event
- `selectChannel` state machine: no-api / same-channel early returns,
success with waiting-flag derivation, throw error path with finally
cleanup, non-Error default label
- `sendMessage` + post-send verification setTimeout: success, verify
finds no post → `captureMMDataIssue` + `removePost`, verify throw →
`logger.warn`, sendPost throw → setError + rethrow, empty post
- `loadMoreHistory`: no-api early return, error → setError
- Typewriter gating: clearOnPost for others, skip tool_status,
post_edited → markStreamingEdit
- `handleTypingEvent`: non-typing ignored, self-typing skipped,
malformed payload guarded
- `clearWaitingForBotReply`: active channel happy path, no-channel no-op

**`vitest.config.mts`** — threshold bump:

| Metric     | Old | New | Observed |
|------------|-----|-----|----------|
| Lines      | 83  | **85**  | 86.67%   |
| Statements | 81  | **83**  | 84.55%   |
| Functions  | 80  | **81**  | 83.41%   |
| Branches   | 73  | **75**  | 76.94%   |

Following the `floor(observed - 1.5%)` rule.

## Phase 5 trajectory (8 PRs)

| PR | Δ lines | Cumulative | Notes |
|---|---|---|---|
| PR 1 (#2090) | +0.21 | 85.13% | queries hooks |
| PR 2 (#2094) | +0.13 | 85.26% | lib pure-fn |
| PR 3 (#2100) | +0.01 | 85.27% | utility hooks (transitively covered) |
| PR 4 (#2101) | +0.24 | 85.51% | Sentry monitors + integrations API
(pivot start) |
| PR 5 (#2102) | +0.65 | 86.16% | 7 BFF routes batched |
| PR 6 (#2105) | +0.28 | 86.44% | 2 more routes + useChatIdentity |
| PR 7 (#2107) | +0.21 | 86.65% | clawhub polling + SessionResetSection
|
| **PR 8** (this) | **+0.07** | **86.67%** + ratchet | useMattermost
orchestrator + threshold lock |

**Phase 5 total: lines 84.92% → 86.67% (+1.76pp).**

## Lessons cemented for future coverage work

1. **`coverage-summary.json` parse beats spec inventory** — PR 4-5
pivoted from the original Tier-B/C lists to parsing the actual uncov LOC
counts; +0.93pp of the +1.76pp Phase 5 gain came from those 2 PRs alone.
2. **Batched-routes pattern is the default for BFF/similar-shape file
groups** — PRs 5/6/7 reused it three times, kept jscpd duplication under
6%.
3. **There IS a ROI ceiling** — utility hooks already exercised
transitively give ~+0.01pp per spec; orchestrators needing 250+ LOC of
mocks for ~15 uncov LOC are net-loss in the
contract-value-per-engineering-hour sense.
4. **Honest framing of small-delta PRs is fine** — PR 3 and PR 8 both
shipped at < +0.1pp with explicit explanation; both got Codex 'No
findings'.
5. **Two flavors of jsdom Request → NextRequest stubbing** depending on
whether the route uses `new URL(request.url).searchParams` (PR 5
pattern) or `request.nextUrl.searchParams` (PR 7 pattern — needs
`Object.defineProperty(req, 'nextUrl', { value: new URL(url) })`).

## Test plan

- [x] `pnpm test:unit` — 26 new tests pass
- [x] `pnpm test:unit:coverage` — all 4 columns ≥ new thresholds (lines
86.67% ≥ 85, etc.)
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup:tests` — 5.8% lines (under 7% gate)
- [x] `pnpm lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [9da8ce03](https://github.com/SerendipityOneInc/ecap-workspace/commit/9da8ce039c2dbeeff0a020957434ecf834b32a6f)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T09:28:02Z
- **PR**: #2109

### Commit Message

```
refactor(web): replace onboarding-* events with zustand store (#2109)

## Summary

PR 5 of the [#2072
epic](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072).
Collapses the two remaining onboarding-prefixed window-event channels
into the Zustand template established by PRs 2-4:

### 1. `onboarding-backend-status` (status broadcast)
- 2 dispatchers in `auth/manager.ts` + 1 `useSyncExternalStore` consumer
in `OnboardingProvider`
- Replaced by **new `onboarding-status-store.ts`** Zustand vanilla store
+ `useOnboardingStatus()` hook
- The module-level `let lastBackendStatus` variable in `auth/manager.ts`
becomes the store's `state.lastStatus`. `_dispatchBackendStatus` calls
`setLastBackendStatus(...)` instead of `window.dispatchEvent`. Mid-app
readers still get the cached snapshot via `getLastBackendStatus()` (now
a thin store accessor).

### 2. `onboarding-retry-sync` (imperative command)
- 1 dispatcher in `OnboardingModal.tsx::handleRetry` + 1 listener in
`AuthManager`'s constructor
- Replaced by **exported `triggerOnboardingRetrySync()`** from
`auth/manager.ts` that directly invokes
`authManager.retryBusinessDataSync()`. The constructor's
`window.addEventListener` is gone. OnboardingModal calls the function
directly.

### New modules
- `lib/onboarding-status-store.ts` — Zustand vanilla store.
Server-bundle-safe (no react / no top-level zustand). Exports
`getLastBackendStatus` / `setLastBackendStatus` /
`resetOnboardingStatusForLogout`. `ScopedBackendOnboardingStatus` type
moved here to break the auth/manager ↔ store import cycle.
- `lib/useOnboardingStatus.ts` — `'use client'` selector hook.

### Cleanup
- `auth/storage.ts::clearUserStorage` finally block now calls
`resetOnboardingStatusForLogout()` alongside the other Tier D resets
(established pattern from PR 2/3/4 —
[[feedback-zustand-migration-read-through-corners]]).
- `auth/manager.ts::clearLastBackendStatus` — removed. Pre-PR-#2072 it
was an exported helper with zero production callers (verified via knip
dep-health audit). The new store-level reset path covers the only
remaining clear case.
- `OnboardingProvider` drops `useSyncExternalStore` — replaced by
`useOnboardingStatus()`. Uid filter at consumer layer preserved.

### 关键引用
- Epic spec:
[`docs/superpowers/specs/2026-05-28-zustand-store-migration.md`](../blob/main/docs/superpowers/specs/2026-05-28-zustand-store-migration.md)
§5 PR 5
- Parent epic PRs: #2074 (infra) / #2088 (PR 2) / #2099 (PR 3) / #2104
(PR 4)

## Test plan

- [x] +11 tests in new `onboarding-status-store.unit.spec.ts` (INITIAL /
set / reset / cross-account leak regression / hook subscription)
- [x] `OnboardingProvider.unit.spec` 49/49 — 3 backend-status-event
tests rewritten to push state through real store
- [x] `auth/manager.unit.spec` 39/39 — 2 retry-sync listener tests
rewritten to call `triggerOnboardingRetrySync()` directly
- [x] 6539/6540 web unit tests pass (1 todo)
- [x] `bash web/scripts/check-no-react-in-stores.sh` — 6 files audited,
passed
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint:deadcode` (knip) clean (also dropped the dead
`clearLastBackendStatus` export)
- [ ] CI 全绿 — 待 reviewer 等
- [ ] reviewer 确认后,启动 PR 6 (`credits-refresh` → RQ `invalidateQueries` +
长尾 command-style events + `no-restricted-syntax` guard,~400 LOC,epic 收尾)

### 不在本 PR 范围
- 不动 `credits-refresh` / `credits-refresh-data` event listeners — PR 6 走
RQ `invalidateQueries`
- 不动 `show-login-modal` / `open-guide-tour` / `user-message-sent` 三个
command-style 长尾 event — PR 6
- 不加 `eslint.config.mjs` `no-restricted-syntax` 拦
`window.dispatchEvent(new Event())` — PR 6 收尾时一起加(现在加会让 PR 6 dispatcher
提前报错)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

PR 5 of the [#2072 epic](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072). Collapses the two remaining onboarding-prefixed window-event channels into the Zustand template established by PRs 2-4:

### 1. `onboarding-backend-status` (status broadcast)
- 2 dispatchers in `auth/manager.ts` + 1 `useSyncExternalStore` consumer in `OnboardingProvider`
- Replaced by **new `onboarding-status-store.ts`** Zustand vanilla store + `useOnboardingStatus()` hook
- The module-level `let lastBackendStatus` variable in `auth/manager.ts` becomes the store's `state.lastStatus`. `_dispatchBackendStatus` calls `setLastBackendStatus(...)` instead of `window.dispatchEvent`. Mid-app readers still get the cached snapshot via `getLastBackendStatus()` (now a thin store accessor).

### 2. `onboarding-retry-sync` (imperative command)
- 1 dispatcher in `OnboardingModal.tsx::handleRetry` + 1 listener in `AuthManager`'s constructor
- Replaced by **exported `triggerOnboardingRetrySync()`** from `auth/manager.ts` that directly invokes `authManager.retryBusinessDataSync()`. The constructor's `window.addEventListener` is gone. OnboardingModal calls the function directly.

### New modules
- `lib/onboarding-status-store.ts` — Zustand vanilla store. Server-bundle-safe (no react / no top-level zustand). Exports `getLastBackendStatus` / `setLastBackendStatus` / `resetOnboardingStatusForLogout`. `ScopedBackendOnboardingStatus` type moved here to break the auth/manager ↔ store import cycle.
- `lib/useOnboardingStatus.ts` — `'use client'` selector hook.

### Cleanup
- `auth/storage.ts::clearUserStorage` finally block now calls `resetOnboardingStatusForLogout()` alongside the other Tier D resets (established pattern from PR 2/3/4 — [[feedback-zustand-migration-read-through-corners]]).
- `auth/manager.ts::clearLastBackendStatus` — removed. Pre-PR-#2072 it was an exported helper with zero production callers (verified via knip dep-health audit). The new store-level reset path covers the only remaining clear case.
- `OnboardingProvider` drops `useSyncExternalStore` — replaced by `useOnboardingStatus()`. Uid filter at consumer layer preserved.

### 关键引用
- Epic spec: [`docs/superpowers/specs/2026-05-28-zustand-store-migration.md`](../blob/main/docs/superpowers/specs/2026-05-28-zustand-store-migration.md) §5 PR 5
- Parent epic PRs: #2074 (infra) / #2088 (PR 2) / #2099 (PR 3) / #2104 (PR 4)

## Test plan

- [x] +11 tests in new `onboarding-status-store.unit.spec.ts` (INITIAL / set / reset / cross-account leak regression / hook subscription)
- [x] `OnboardingProvider.unit.spec` 49/49 — 3 backend-status-event tests rewritten to push state through real store
- [x] `auth/manager.unit.spec` 39/39 — 2 retry-sync listener tests rewritten to call `triggerOnboardingRetrySync()` directly
- [x] 6539/6540 web unit tests pass (1 todo)
- [x] `bash web/scripts/check-no-react-in-stores.sh` — 6 files audited, passed
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint:deadcode` (knip) clean (also dropped the dead `clearLastBackendStatus` export)
- [ ] CI 全绿 — 待 reviewer 等
- [ ] reviewer 确认后,启动 PR 6 (`credits-refresh` → RQ `invalidateQueries` + 长尾 command-style events + `no-restricted-syntax` guard,~400 LOC,epic 收尾)

### 不在本 PR 范围
- 不动 `credits-refresh` / `credits-refresh-data` event listeners — PR 6 走 RQ `invalidateQueries`
- 不动 `show-login-modal` / `open-guide-tour` / `user-message-sent` 三个 command-style 长尾 event — PR 6
- 不加 `eslint.config.mjs` `no-restricted-syntax` 拦 `window.dispatchEvent(new Event())` — PR 6 收尾时一起加(现在加会让 PR 6 dispatcher 提前报错)

---

## [74b2dedf](https://github.com/SerendipityOneInc/ecap-workspace/commit/74b2dedf102294b89abc2276a2dc34bf93bfa39b)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T09:26:02Z
- **PR**: #2108

### Commit Message

```
refactor(web): migrate 8 click-outside sites to usehooks-ts useOnClickOutside (#2108)

## 背景

issue #2072 的 out-of-scope follow-up（DOM `addEventListener` 子类，纯
ergonomics）PR2，接续已合并的 PR1
#2106。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md`。

## 本 PR 内容

把 **8 个** `document.addEventListener('mousedown')` + `ref.contains` 的
click-outside effect 收敛为 \`useOnClickOutside\`（默认监听 mousedown，与原实现一致）。每处
~12 行 effect → 1 行，**净减 75 行**（29 insertions / 104 deletions）。

迁移站点：\`ModelSelector\` / \`SelectField\` / \`SizeSelector\` /
\`ClawPageHeader\` / \`ArtifactPreview\` / \`ImageActionMenu\` /
\`ConnectorsSection\` / \`ScheduleWeekView\`。

## UserMenu 为何 deferred（9 → 8）

\`UserMenu\` 把 click-outside 的 \`mousedown\` 与 \`keydown\`(Escape) 合在一个
effect，且用 \`setTimeout(0)\` **延迟挂载**（避免打开它的那次 toggle
点击立即触发关闭）。\`useOnClickOutside\` 同步挂载、无延迟语义，强行迁移有「打开即关闭」回归风险，而它本就是 shadcn
\`DropdownMenu\` 候选——保留手写，留待 shadcn 迁移一并处理。

## 类型说明（React 19 × usehooks-ts）

usehooks-ts@3.1.1 的 \`useOnClickOutside\` ref 参数类型是 React 18 风格的
\`RefObject<HTMLElement>\`（非空 \`current\`）。React 19 把 \`RefObject<T>\`
改成 \`{ current: T }\`，\`useRef<HTMLDivElement>(null)\` 产出
\`RefObject<HTMLDivElement | null>\`，与之不兼容。每个 call site 用 \`as
React.RefObject<HTMLDivElement>\` 断言桥接——lib 内部已做 \`r.current &&
!r.current.contains(...)\` null-check，运行时安全。**不引 wrapper
shim**（避免兼容转发层）。

## 验证

- ✅ 回归 oracle：8 个组件**既有单测**已含 \`mousedown outside → closes\` /
\`mousedown inside → stays open\` / \`Escape → closes\` 的 click-outside
断言，迁移后 **204 测全绿**，证明行为零漂移 → 本 PR 不新增测试。
- ✅ \`tsc --noEmit\` exit 0
- ✅ \`eslint\` 0 errors（pre-commit 通过）

## 后续 PR

PR3a/b/c 普通监听（keydown / scroll+resize / visibilitychange）→
\`useEventListener\`；PR4 matchMedia → \`useMediaQuery\`。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

issue #2072 的 out-of-scope follow-up（DOM `addEventListener` 子类，纯 ergonomics）PR2，接续已合并的 PR1 #2106。spec：`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md`。

## 本 PR 内容

把 **8 个** `document.addEventListener('mousedown')` + `ref.contains` 的 click-outside effect 收敛为 \`useOnClickOutside\`（默认监听 mousedown，与原实现一致）。每处 ~12 行 effect → 1 行，**净减 75 行**（29 insertions / 104 deletions）。

迁移站点：\`ModelSelector\` / \`SelectField\` / \`SizeSelector\` / \`ClawPageHeader\` / \`ArtifactPreview\` / \`ImageActionMenu\` / \`ConnectorsSection\` / \`ScheduleWeekView\`。

## UserMenu 为何 deferred（9 → 8）

\`UserMenu\` 把 click-outside 的 \`mousedown\` 与 \`keydown\`(Escape) 合在一个 effect，且用 \`setTimeout(0)\` **延迟挂载**（避免打开它的那次 toggle 点击立即触发关闭）。\`useOnClickOutside\` 同步挂载、无延迟语义，强行迁移有「打开即关闭」回归风险，而它本就是 shadcn \`DropdownMenu\` 候选——保留手写，留待 shadcn 迁移一并处理。

## 类型说明（React 19 × usehooks-ts）

usehooks-ts@3.1.1 的 \`useOnClickOutside\` ref 参数类型是 React 18 风格的 \`RefObject<HTMLElement>\`（非空 \`current\`）。React 19 把 \`RefObject<T>\` 改成 \`{ current: T }\`，\`useRef<HTMLDivElement>(null)\` 产出 \`RefObject<HTMLDivElement | null>\`，与之不兼容。每个 call site 用 \`as React.RefObject<HTMLDivElement>\` 断言桥接——lib 内部已做 \`r.current && !r.current.contains(...)\` null-check，运行时安全。**不引 wrapper shim**（避免兼容转发层）。

## 验证

- ✅ 回归 oracle：8 个组件**既有单测**已含 \`mousedown outside → closes\` / \`mousedown inside → stays open\` / \`Escape → closes\` 的 click-outside 断言，迁移后 **204 测全绿**，证明行为零漂移 → 本 PR 不新增测试。
- ✅ \`tsc --noEmit\` exit 0
- ✅ \`eslint\` 0 errors（pre-commit 通过）

## 后续 PR

PR3a/b/c 普通监听（keydown / scroll+resize / visibilitychange）→ \`useEventListener\`；PR4 matchMedia → \`useMediaQuery\`。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [94fc3ff3](https://github.com/SerendipityOneInc/ecap-workspace/commit/94fc3ff3cc3894a59a7e069ddeb331d1ca393dc1)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T09:18:08Z
- **PR**: #894

### Commit Message

```
test(web): Phase 5 PR 7 — clawhub polling loop + SessionResetSection (#894) (#2107)

## Summary

PR 7 of the Phase 5 web coverage push (issue #894). Two specs targeting
modules that earlier PRs deferred.

## What's in this PR

**`clawhub-polling.unit.spec.ts` (26 tests)** — covers
`/api/openclaw/clawhub/[action]`, was 70.9% covered. The uncovered 23
lines were the init-then-poll branches in `resolveReadyBotId` that PR 5
deferred because they needed fake timers + sequenced proxy responses.

Coverage areas:
- GET `/list` query validation (uid required, non-list action → 400)
- GET happy path + workdir URL-encoding
- Status-check error branches (`error` / `detail` / fallback labels)
- Status not ready → init responds ready (no poll)
- Status not ready → init non-ok (`error` field wins over `detail`)
- **Polling: poll resolves ready** → returns botId after a few intervals
- **Polling: poll status non-ok** → returns the poll error
- **Polling: poll status='error'** → 409 with message
- **Polling: timeout after BOT_READY_TIMEOUT_MS** → 409
- POST install/uninstall: action allowlist, body validation
- POST install: optional fields (`version`/`registry`/`workdir`/`force`)
forwarded
- POST uninstall: only `slug` + `workdir` forwarded (the
install-specific fields dropped)

`vi.useFakeTimers()` + `vi.advanceTimersByTimeAsync(3500)` drives the
`await sleep(BOT_POLL_INTERVAL_MS)` between polls. **Notable**: this
route reads `request.nextUrl.searchParams` (not `new URL(request.url)`
like the routes-batch ones), so the test helpers stub `.nextUrl` with
the native `URL` object — added a comment so future readers don't repeat
my debug cycle. This is a different jsdom Request → NextRequest gotcha
from the one PR 5 documented.

**`SessionResetSection.unit.spec.tsx` (12 tests)** — covers the
`/[locale]/claw-settings/components/SessionResetSection` component (was
0% covered):

- Renders 3 mode radios (off/daily/idle)
- `off` mode hides number inputs
- `idle` mode shows BOTH idle-minutes + reset-at-hour
- `daily` mode shows ONLY reset-at-hour (no idle-minutes)
- Switching mode reveals/hides inputs
- `handleSave` payload shape per mode (off → mode only; daily → at_hour;
idle → idle_minutes + at_hour)
- `showSaveToast` fires on success, NOT on failure
- Save button disabled when state matches props (no diff to save)
- Save button disabled while `saving` prop is true (double-submit guard)

## Coverage delta

| Metric     | Before (post PR 6) | After  | Δ        |
|------------|--------------------|--------|----------|
| Lines      | 86.44%             | 86.65% | +0.21pp  |
| Statements | 84.31%             | 84.51% | +0.20pp  |
| Functions  | 83.25%             | 83.43% | +0.18pp  |
| Branches   | 76.50%             | 76.86% | +0.36pp  |

All four columns remain above existing thresholds (lines=83 / stmts=81 /
funcs=80 / branches=73). Branches got the largest bump this PR thanks to
the polling-loop conditional explosion.

## Phase 5 trajectory

| PR | Δ lines | Cumulative |
|---|---|---|
| PR 1 | +0.21 | 85.13% |
| PR 2 | +0.13 | 85.26% |
| PR 3 | +0.01 | 85.27% |
| PR 4 | +0.24 | 85.51% |
| PR 5 | +0.65 | 86.16% |
| PR 6 | +0.28 | 86.44% |
| **PR 7** | **+0.21** | **86.65%** |

Remaining gap to 90%: **3.35pp**.

## What's left

- `lib/auth/manager.ts` (55 uncov @ 78.8%) — already specced, deep
branches uncov; would need careful targeted tests
- `MMAttachments.tsx` (48 uncov @ 55%) — but pre-existing flaky test on
main needs `afterEach(cleanup)` first
- `ChatGateStates.tsx` (39 uncov @ 15%), `DataPermissionsSection.tsx`
(28 uncov @ 67%), other UI components
- `useMattermost.ts` orchestrator (~50 uncov, needs ~250 LOC of mocks)
- More admin tab components

## Test plan

- [x] `pnpm test:unit` — 38 new tests pass (2 specs)
- [x] `pnpm test:unit:coverage` — all 4 columns ≥ thresholds
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup:tests` — 5.84% lines (under 7% gate)
- [x] `pnpm lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [5f66b633](https://github.com/SerendipityOneInc/ecap-workspace/commit/5f66b633d9d98e9950dd2d08297934af4039ec55)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T09:11:26Z
- **PR**: #2106

### Commit Message

```
refactor(web): introduce usehooks-ts + reimplement useEscapeKey over useEventListener (#2106)

## 背景

issue #2072 的 out-of-scope follow-up（issue 表格 row「DOM
\`addEventListener\` ~60 文件」，定性 ★ 纯 ergonomics）首个 PR。分支
\`feature/usehook-ts\` 即此选型。

完整方案见随本 PR 落地的
spec：\`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md\`。

## 本 PR 内容

1. **引入 \`usehooks-ts@3.1.1\`**（exact pin，入 \`web/app\`
\`dependencies\`）。React 19 peer 支持；单依赖 \`lodash.debounce\`；lockfile diff
仅新增这两个包，无其它 re-resolve。
2. **\`useEscapeKey\` 内部改写**为委托 \`useEventListener\`。公共签名 \`(onEscape,
enabled=true)\` **不变** → 18 个 caller 零改动。
3. **落地迁移 spec**（范围表 / out-of-scope 边界 / shadcn 张力 / 不加 lint guard 决策）。

## keystone 设计（为何先做这个）

- 现有 \`tests/unit/hooks/useEscapeKey.unit.spec.ts\` 的 **6 条断言保持不变**，作为
lib 语义的回归 oracle。若任何一条挂，说明 usehooks-ts 的 ref 语义与手写不一致，迁移在此叫停——风险隔离在单文件而非
30 个文件。
- 显式传 \`useRef<Document>(globalThis.document)\` 保持监听
\`document\`：\`useEventListener\` 默认 target 是 \`window\`，收不到测试里 dispatch
在 \`document\` 上的**非冒泡**事件。
- 第 6 条断言（callback 身份变化时 \`document.removeEventListener\`
**从不**被调用）保持绿，即证明 lib 的 \`savedHandler\` ref 模式与原手写 \`callbackRef\` 等价。
- \`enabled\` 用 handler 内 early-return 表达（lib 无 enable
flag）；行为差异（disabled 时保持挂载 vs 原版 detach）对 oracle 断言（行为而非 attach 计数）透明。

## 验证

- ✅ \`tests/unit/hooks/useEscapeKey.unit.spec.ts\` 6/6 通过（未改动）
- ✅ \`tsc --noEmit\` exit 0
- ✅ \`eslint\` exit 0
- ✅ \`knip\` dep-health hard gate exit 0（usehooks-ts 未被标 unused）

## 后续 PR（串行）

PR2 click-outside → \`useOnClickOutside\`（9 站点）→ PR3a/b/c 普通监听 →
\`useEventListener\` → PR4 matchMedia → \`useMediaQuery\`。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

issue #2072 的 out-of-scope follow-up（issue 表格 row「DOM \`addEventListener\` ~60 文件」，定性 ★ 纯 ergonomics）首个 PR。分支 \`feature/usehook-ts\` 即此选型。

完整方案见随本 PR 落地的 spec：\`docs/superpowers/specs/2026-05-30-usehooks-ts-dom-listener-migration.md\`。

## 本 PR 内容

1. **引入 \`usehooks-ts@3.1.1\`**（exact pin，入 \`web/app\` \`dependencies\`）。React 19 peer 支持；单依赖 \`lodash.debounce\`；lockfile diff 仅新增这两个包，无其它 re-resolve。
2. **\`useEscapeKey\` 内部改写**为委托 \`useEventListener\`。公共签名 \`(onEscape, enabled=true)\` **不变** → 18 个 caller 零改动。
3. **落地迁移 spec**（范围表 / out-of-scope 边界 / shadcn 张力 / 不加 lint guard 决策）。

## keystone 设计（为何先做这个）

- 现有 \`tests/unit/hooks/useEscapeKey.unit.spec.ts\` 的 **6 条断言保持不变**，作为 lib 语义的回归 oracle。若任何一条挂，说明 usehooks-ts 的 ref 语义与手写不一致，迁移在此叫停——风险隔离在单文件而非 30 个文件。
- 显式传 \`useRef<Document>(globalThis.document)\` 保持监听 \`document\`：\`useEventListener\` 默认 target 是 \`window\`，收不到测试里 dispatch 在 \`document\` 上的**非冒泡**事件。
- 第 6 条断言（callback 身份变化时 \`document.removeEventListener\` **从不**被调用）保持绿，即证明 lib 的 \`savedHandler\` ref 模式与原手写 \`callbackRef\` 等价。
- \`enabled\` 用 handler 内 early-return 表达（lib 无 enable flag）；行为差异（disabled 时保持挂载 vs 原版 detach）对 oracle 断言（行为而非 attach 计数）透明。

## 验证

- ✅ \`tests/unit/hooks/useEscapeKey.unit.spec.ts\` 6/6 通过（未改动）
- ✅ \`tsc --noEmit\` exit 0
- ✅ \`eslint\` exit 0
- ✅ \`knip\` dep-health hard gate exit 0（usehooks-ts 未被标 unused）

## 后续 PR（串行）

PR2 click-outside → \`useOnClickOutside\`（9 站点）→ PR3a/b/c 普通监听 → \`useEventListener\` → PR4 matchMedia → \`useMediaQuery\`。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [5e5d49a1](https://github.com/SerendipityOneInc/ecap-workspace/commit/5e5d49a1f63eb10c0c16a60c2db366e8510e771f)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T09:06:23Z
- **PR**: #2104

### Commit Message

```
refactor(web): replace auth-state-changed broadcast with Zustand snapshot (#2104)

## Summary

PR 4 of the [#2072
epic](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072) —
the main course. Replaces the `window.dispatchEvent(new
CustomEvent('auth-state-changed'))` broadcast pattern (4 dispatchers +
10 consumers + the cross-tab `storage` event re-broadcast in SideNav)
with a single Zustand vanilla store + `useAuthSnapshot` hook.

### New modules
- **`lib/auth-snapshot-store.ts`** — vanilla Zustand store mirroring
`getUserInfo()` + `getSubscriptionInfo()`. `notifyAuthChange()` re-reads
both and pushes a fresh snapshot. Server-bundle-safe (no `react`, no
top-level `zustand`); enforced by the PR #2074 CI guard. Exports
`resetAuthSnapshotForLogout()` for `clearUserStorage` hookup
([[feedback-zustand-migration-read-through-corners]]).
- **`lib/useAuthSnapshot.ts`** — `'use client'` hook with selector
overload. First-mount auto-seed (idempotent via module-singleton flag)
so consumer renders that happen before `AuthProvider`'s shell-level seed
(or in unit-test `renderHook`) still read fresh data.
`resetUseAuthSnapshotForTests()` clears the flag for isolation.

### Dispatchers replaced (4 sites → `notifyAuthChange()`)
- `lib/auth/manager.ts::dispatchAuthStateChanged`
- `components/providers/AuthProvider.tsx` (Firebase listener) +
mount-time seed call
- `lib/billing/mock-billing-data.ts` (2 sites — restore + sync paths)

Plus `lib/auth/storage.ts::clearUserStorage` finally-block adds
`resetAuthSnapshotForLogout()` alongside `clearAgentDescriptions` +
`clearAllCustomAgentPublishDraftsInMemory` (the established Tier D
cleanup pattern from PR 2/3).

### Consumers migrated (10 files)
- `hooks/useAuth.ts` — `userInfo` via snapshot; `isLoading` + `deviceId`
stay local for the existing loading-transition contract.
- `hooks/useBillingCredits.ts` — `subscriptionInfo.uid` +
`billing_initialized` drive a snapshot-derived effect (logout /
account-switch / billing-init flips). `credits-refresh` +
`credits-refresh-data` window listeners preserved (PR 6 will route them
to RQ).
- `hooks/useFreeStatus.ts` — full snapshot subscription replaces the
manual `addEventListener` + `setState` pair.
- `components/sidenav/hooks/useNavAuthState.ts` — `userInfo` +
`subscriptionInfo` via snapshot. Cross-tab `storage` event handler
centralised here, calls `notifyAuthChange()` to re-broadcast.
- `contexts/UserBusinessDataContext.tsx` — uid from snapshot; Layer-3
contract preserved (no `hooks/` import).
- `components/UserMenu.tsx` / `UserCard.tsx` — userInfo via snapshot.
- `components/providers/LoginCheckProvider.tsx` — auto-close on
`userInfo.type === '1'` via dependent useEffect.
- `app/[locale]/pricing/PublicPricingClient.tsx` — auth-derived state on
snapshot deps.
- `app/landing/hooks/useLandingAuthRedirect.ts` — transition detect on
`userInfoType` flip; mount-time vs transition split via `hasMountedRef`
so userInfoType changes don't re-fire the already-authenticated
`router.replace`.

### Tests
- **+1 new** spec for `auth-snapshot-store` + `useAuthSnapshot` (11
tests, covers INITIAL state / notifyAuthChange /
resetAuthSnapshotForLogout / cross-account leak regression / selector
ref-equality).
- **+10 retargeted** specs: tests that asserted
`addEventListener('auth-state-changed', ...)` lifecycle (implementation
detail) were removed; tests that dispatched the event to trigger a
re-fetch now call `notifyAuthChange()`; tests that subscribed to verify
dispatch use `authSnapshotStore.subscribe()`. Tests that drive snapshot
transitions reset the module-singleton snapshot + first-mount seed flag
in `beforeEach`.

### 关键引用
- Epic spec:
[`docs/superpowers/specs/2026-05-28-zustand-store-migration.md`](../blob/main/docs/superpowers/specs/2026-05-28-zustand-store-migration.md)
§5 PR 4
- Parent epic PRs: #2074 (infra) / #2088 (PR 2) / #2099 (PR 3)

## Test plan

- [x] +11 tests in new `auth-snapshot-store.unit.spec.ts`
- [x] 6460/6461 web unit tests pass (1 todo)
- [x] `bash web/scripts/check-no-react-in-stores.sh` — 5 file(s)
audited, passed
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint:deadcode` (knip) clean
- [ ] CI 全绿 — 待 reviewer 等
- [ ] reviewer 确认后,启动 PR 5 (`onboarding-backend-status` +
`onboarding-retry-sync` 两个 onboarding event 合并)

### 不在本 PR 范围
- 不动 `credits-refresh` / `credits-refresh-data` event listeners — PR 6 走
RQ `invalidateQueries`
- 不动 `show-login-modal` / `open-guide-tour` / `user-message-sent` 三个
command-style 长尾 event — PR 6
- 跨 tab `storage` event 仍走 `window.addEventListener`(centralised in
useNavAuthState),只是同 tab fan-out 改为 Zustand 通过 `notifyAuthChange()` 重新广播

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

PR 4 of the [#2072 epic](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072) — the main course. Replaces the `window.dispatchEvent(new CustomEvent('auth-state-changed'))` broadcast pattern (4 dispatchers + 10 consumers + the cross-tab `storage` event re-broadcast in SideNav) with a single Zustand vanilla store + `useAuthSnapshot` hook.

### New modules
- **`lib/auth-snapshot-store.ts`** — vanilla Zustand store mirroring `getUserInfo()` + `getSubscriptionInfo()`. `notifyAuthChange()` re-reads both and pushes a fresh snapshot. Server-bundle-safe (no `react`, no top-level `zustand`); enforced by the PR #2074 CI guard. Exports `resetAuthSnapshotForLogout()` for `clearUserStorage` hookup ([[feedback-zustand-migration-read-through-corners]]).
- **`lib/useAuthSnapshot.ts`** — `'use client'` hook with selector overload. First-mount auto-seed (idempotent via module-singleton flag) so consumer renders that happen before `AuthProvider`'s shell-level seed (or in unit-test `renderHook`) still read fresh data. `resetUseAuthSnapshotForTests()` clears the flag for isolation.

### Dispatchers replaced (4 sites → `notifyAuthChange()`)
- `lib/auth/manager.ts::dispatchAuthStateChanged`
- `components/providers/AuthProvider.tsx` (Firebase listener) + mount-time seed call
- `lib/billing/mock-billing-data.ts` (2 sites — restore + sync paths)

Plus `lib/auth/storage.ts::clearUserStorage` finally-block adds `resetAuthSnapshotForLogout()` alongside `clearAgentDescriptions` + `clearAllCustomAgentPublishDraftsInMemory` (the established Tier D cleanup pattern from PR 2/3).

### Consumers migrated (10 files)
- `hooks/useAuth.ts` — `userInfo` via snapshot; `isLoading` + `deviceId` stay local for the existing loading-transition contract.
- `hooks/useBillingCredits.ts` — `subscriptionInfo.uid` + `billing_initialized` drive a snapshot-derived effect (logout / account-switch / billing-init flips). `credits-refresh` + `credits-refresh-data` window listeners preserved (PR 6 will route them to RQ).
- `hooks/useFreeStatus.ts` — full snapshot subscription replaces the manual `addEventListener` + `setState` pair.
- `components/sidenav/hooks/useNavAuthState.ts` — `userInfo` + `subscriptionInfo` via snapshot. Cross-tab `storage` event handler centralised here, calls `notifyAuthChange()` to re-broadcast.
- `contexts/UserBusinessDataContext.tsx` — uid from snapshot; Layer-3 contract preserved (no `hooks/` import).
- `components/UserMenu.tsx` / `UserCard.tsx` — userInfo via snapshot.
- `components/providers/LoginCheckProvider.tsx` — auto-close on `userInfo.type === '1'` via dependent useEffect.
- `app/[locale]/pricing/PublicPricingClient.tsx` — auth-derived state on snapshot deps.
- `app/landing/hooks/useLandingAuthRedirect.ts` — transition detect on `userInfoType` flip; mount-time vs transition split via `hasMountedRef` so userInfoType changes don't re-fire the already-authenticated `router.replace`.

### Tests
- **+1 new** spec for `auth-snapshot-store` + `useAuthSnapshot` (11 tests, covers INITIAL state / notifyAuthChange / resetAuthSnapshotForLogout / cross-account leak regression / selector ref-equality).
- **+10 retargeted** specs: tests that asserted `addEventListener('auth-state-changed', ...)` lifecycle (implementation detail) were removed; tests that dispatched the event to trigger a re-fetch now call `notifyAuthChange()`; tests that subscribed to verify dispatch use `authSnapshotStore.subscribe()`. Tests that drive snapshot transitions reset the module-singleton snapshot + first-mount seed flag in `beforeEach`.

### 关键引用
- Epic spec: [`docs/superpowers/specs/2026-05-28-zustand-store-migration.md`](../blob/main/docs/superpowers/specs/2026-05-28-zustand-store-migration.md) §5 PR 4
- Parent epic PRs: #2074 (infra) / #2088 (PR 2) / #2099 (PR 3)

## Test plan

- [x] +11 tests in new `auth-snapshot-store.unit.spec.ts`
- [x] 6460/6461 web unit tests pass (1 todo)
- [x] `bash web/scripts/check-no-react-in-stores.sh` — 5 file(s) audited, passed
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint:deadcode` (knip) clean
- [ ] CI 全绿 — 待 reviewer 等
- [ ] reviewer 确认后,启动 PR 5 (`onboarding-backend-status` + `onboarding-retry-sync` 两个 onboarding event 合并)

### 不在本 PR 范围
- 不动 `credits-refresh` / `credits-refresh-data` event listeners — PR 6 走 RQ `invalidateQueries`
- 不动 `show-login-modal` / `open-guide-tour` / `user-message-sent` 三个 command-style 长尾 event — PR 6
- 跨 tab `storage` event 仍走 `window.addEventListener`(centralised in useNavAuthState),只是同 tab fan-out 改为 Zustand 通过 `notifyAuthChange()` 重新广播

---

## [649962c1](https://github.com/SerendipityOneInc/ecap-workspace/commit/649962c1898833c4c7e4e2fb41217aac8ae88c59)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T09:02:03Z
- **PR**: #894

### Commit Message

```
test(web): Phase 5 PR 6 — 2 more BFF routes + useChatIdentity (#894) (#2105)

## Summary

PR 6 of the Phase 5 web coverage push (issue #894). Continues PR 5's
batched-routes pattern with 2 more BFF API routes, plus a dedicated spec
for `useChatIdentity` (the chat-page identity orchestration hook).

## What's in this PR

**Routes added to `routes-batch.unit.spec.ts` (+13 tests, now 55
total)**

| Route | Tests | Highlights |
|---|---|---|
| `/api/openclaw/settings/channels/[platform]/pairing` (POST) | 6 |
`uid` + `code` body required, `encodeURIComponent` platform path guard,
ok/non-ok/throw |
| `/api/chat-replays` (POST + GET) | 7 | body forwarding on POST,
backend detail vs 'Backend returned N' fallback, both verbs |

**`useChatIdentity.unit.spec.tsx` (new file, 13 tests)**

Covers the chat-page identity orchestration hook (was 0% covered). Tests
assert composition logic against mocked `useClawIdentityQuery` /
`useAgentSettingsQuery` / `useAgentDescription` / `captureChatWarning`:

- Returns resolved identity + presentation from helpers
- Empty-identity fallback `{}` when query has no data yet (the `useMemo`
stability fix)
- Identity data threaded into `resolveChatIdentity` once query resolves
- `agentSettings` derived from query → `resolveChatIdentity`
- `settingsAgentId` defaults to `'main'` when agentId is null
- `captureChatWarning` fires on `identityQuery.isError` and on
`activeAgentSettingsQuery.error`
- No warning on happy path
- `handleAgentIdentitySaved` override takes precedence over query
settings
- Override with name-only doesn't clobber prior avatar (the
partial-update guard)
- Override is keyed by `settingsAgentId` — switching agent drops it
- `useAgentDescription` called with `activeAgent.id`; null activeAgent →
undefined

## Coverage delta

| Metric     | Before (post PR 5) | After  | Δ        |
|------------|--------------------|--------|----------|
| Lines      | 86.16%             | 86.44% | +0.28pp  |
| Statements | 84.05%             | 84.31% | +0.26pp  |
| Functions  | 83.02%             | 83.25% | +0.23pp  |
| Branches   | 76.29%             | 76.50% | +0.21pp  |

All four columns remain above existing thresholds (lines=83 / stmts=81 /
funcs=80 / branches=73).

## Phase 5 trajectory

| PR | Δ lines | Cumulative | Notes |
|---|---|---|---|
| PR 1 | +0.21 | 85.13% | queries hooks |
| PR 2 | +0.13 | 85.26% | lib pure-fn |
| PR 3 | +0.01 | 85.27% | utility hooks |
| PR 4 | +0.24 | 85.51% | Sentry monitors + integrations API |
| PR 5 | +0.65 | 86.16% | 7 BFF routes batched |
| **PR 6** | **+0.28** | **86.44%** | 2 more routes + useChatIdentity
hook |

Remaining gap to 90% = 3.56pp.

## What's left

The remaining high-uncov candidates from the fresh coverage report:
- `lib/auth/manager.ts` (55 uncov @ 78.8%, already has a spec — the gaps
are deep branches in login/logout error/retry paths)
- `MMAttachments.tsx` (48 uncov @ 55%), `ChatGateStates.tsx` (39 uncov @
15%) — components, harder to test
- `clawhub/[action]/route.ts` (23 uncov @ 70.9%) — polling loop, needs
fake timers
- `useMattermost.ts` (249 LOC orchestrator) — needs ~250 LOC of mocks
- Various admin tab components at 15-30%

## Test plan

- [x] `pnpm test:unit` — 26 new tests pass
- [x] `pnpm test:unit:coverage` — all 4 columns ≥ thresholds
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup:tests` — 5.83% lines (under 7% gate)
- [x] `pnpm lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [86e4d91a](https://github.com/SerendipityOneInc/ecap-workspace/commit/86e4d91a2e506d6ea72632408ba6107e9077766a)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T08:49:50Z
- **PR**: #2103

### Commit Message

```
chore(web): use triggerDownload in 2 remaining REVOKE_INLINE callers + archive shipped spec (#2103)

## Summary

#2072 createObjectURL series 收尾两件小事:

1. **2 处 inline `URL.createObjectURL`+ click + revoke 换成
`triggerDownload`**(`MarkdownContent.tsx` 和 `ArtifactPreview.tsx`)。原
inline 代码跟 `lib/download.ts::triggerDownload` 字节级一样,但少了
`document.body.appendChild + removeChild` 包裹 —— 某些浏览器(Firefox)要求 anchor
在 DOM 里才能触发下载,inline 版本潜在不工作。换成 helper 顺手修。
2. **归档 spec**
`docs/superpowers/specs/2026-05-28-object-url-hook-rollout.md` →
`docs/archive/plans/2026-05-28-object-url-hook-rollout-plan.md` —— 4 PR
全 merged。

## 不在 scope 的剩 7 处 inline disable

`useObjectUrl.ts` (canonical wrapper) / `pptx-parser.ts` (pure function
with per-parse accumulator) / `MmPendingAttachmentChip.tsx` (imperative
click handler, callback pattern) / `useMmAttachments.ts × 3`
(REVOKE_ON_CHANGE in state updater) / `UploadsFeed.tsx` +
`MyUploadsTab.tsx` (imperative click handler with overlay-scoped URL
lifetime) —— 架构上 `useObjectUrl`(render-only)和
`triggerDownload`(fire-and-forget)都不适配,各自 inline disable + per-line
lifecycle 注释是正确状态。

## Test plan

- [x] `pnpm lint` 全绿
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 6456 测试通过(修了 1 个测试,assert 改到 `triggerDownload`
helper boundary)
- [ ] CI: web-quality 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

#2072 createObjectURL series 收尾两件小事:

1. **2 处 inline `URL.createObjectURL`+ click + revoke 换成 `triggerDownload`**(`MarkdownContent.tsx` 和 `ArtifactPreview.tsx`)。原 inline 代码跟 `lib/download.ts::triggerDownload` 字节级一样,但少了 `document.body.appendChild + removeChild` 包裹 —— 某些浏览器(Firefox)要求 anchor 在 DOM 里才能触发下载,inline 版本潜在不工作。换成 helper 顺手修。
2. **归档 spec** `docs/superpowers/specs/2026-05-28-object-url-hook-rollout.md` → `docs/archive/plans/2026-05-28-object-url-hook-rollout-plan.md` —— 4 PR 全 merged。

## 不在 scope 的剩 7 处 inline disable

`useObjectUrl.ts` (canonical wrapper) / `pptx-parser.ts` (pure function with per-parse accumulator) / `MmPendingAttachmentChip.tsx` (imperative click handler, callback pattern) / `useMmAttachments.ts × 3` (REVOKE_ON_CHANGE in state updater) / `UploadsFeed.tsx` + `MyUploadsTab.tsx` (imperative click handler with overlay-scoped URL lifetime) —— 架构上 `useObjectUrl`(render-only)和 `triggerDownload`(fire-and-forget)都不适配,各自 inline disable + per-line lifecycle 注释是正确状态。

## Test plan

- [x] `pnpm lint` 全绿
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 6456 测试通过(修了 1 个测试,assert 改到 `triggerDownload` helper boundary)
- [ ] CI: web-quality 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [59b7846b](https://github.com/SerendipityOneInc/ecap-workspace/commit/59b7846b512c3377ef76ab5baffb6f547dd719cf)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T08:46:51Z
- **PR**: #894

### Commit Message

```
test(web): Phase 5 PR 5 — batched BFF route handlers (#894) (#2102)

## Summary

PR 5 of the Phase 5 web coverage push (issue #894). Adds a single
batched unit spec covering **7 BFF proxy routes** across 6 route files.
Continues the coverage-summary.json pivot strategy from PR 4.

## What's in this PR

All 6 routes follow the same shape — `try → parse → proxyToBackend →
check .ok → JSON | createErrorResponse | catch → 500` — so batching them
in **one** spec file shares the proxy / logger / createErrorResponse
mocks and avoids 7 copies of the same `vi.hoisted` boilerplate (would
push jscpd duplication over the 7% gate).

| Route | Tests |
|---|---|
| `/api/orders/get` (GET) | 6 — query validation, ok/non-ok, throw,
fallback labels |
| `/api/openclaw/agents` (GET + POST) | 7 — body forwarding on POST,
non-Error throw value, 'Backend returned N' fallback |
| `/api/openclaw/admin/releases` (GET + POST) | 5 — same shape, no
required params |
| `/api/openclaw/settings/usage` (GET) | 4 — uid + startDate/endDate
required, backend URL builder, 30s timeout |
| `/api/openclaw/settings/resources` (GET) | 4 — **special-case 409 →
200 + `bot_not_ready: true`** so the UI shows a hint not an error; other
non-409 errors pass through |
| `/api/openclaw/cron/runs` (GET) | 5 — jobId required, default
`limit=20/offset=0/sortDir=desc`, `encodeURIComponent` guard on jobId
path segment |
| `/api/openclaw/admin/bots/[botId]/[action]` (POST) | 11 —
**path-traversal regex rejection** (slash + shell metachars),
`start/stop/restart/delete` allowlist via `it.each`, user_id required,
ok/non-ok/throw |

**42 tests total** in one spec file (~500 LOC).

## Coverage delta — biggest PR of Phase 5

| Metric     | Before (post PR 4) | After  | Δ        |
|------------|--------------------|--------|----------|
| Lines      | 85.51%             | 86.16% | **+0.65pp** |
| Statements | 83.44%             | 84.05% | +0.61pp  |
| Functions  | 82.68%             | 83.02% | +0.34pp  |
| Branches   | 75.85%             | 76.29% | +0.44pp  |

All four columns remain above existing thresholds (lines=83 / stmts=81 /
funcs=80 / branches=73).

## Phase 5 trajectory

| PR | Δ lines | Cumulative | Notes |
|---|---|---|---|
| PR 1 | +0.21 | 85.13% | queries hooks |
| PR 2 | +0.13 | 85.26% | lib pure-fn |
| PR 3 | +0.01 | 85.27% | utility hooks (transitively covered) |
| PR 4 | +0.24 | 85.51% | Sentry monitors + integrations API (pivot to
coverage-summary) |
| **PR 5** | **+0.65** | **86.16%** | BFF route handlers (batched) |

## What's left to 90%

Remaining gap: ~3.84pp. Realistic 2 more PRs of similar size:

- `lib/auth/manager.ts` (55 uncov LOC at 78.8%, login/logout state
machine)
- `useMattermost.ts` orchestrator (249 LOC, ~50 uncov, but needs ~250
LOC of mocks)
- `MMAttachments.tsx` (48 uncov at 55%), `ChatGateStates.tsx` (39 uncov
at 15%), `ChatDragDropContainer.tsx` (23 uncov at 11%)
- `useChatIdentity.ts` (22 uncov at 0%)
- `clawhub/[action]/route.ts` (23 uncov at 70.9%, polling loop needs
fake timers)
- Various admin tab components at 15-30%

## Plan deviation note

The original Phase 5 plan called PR 5 a 'ratchet bump'. The pivot to
coverage-driven targeting (started in PR 4) means the ratchet PR shifts
to whenever observed lines stabilizes near 90%. With the trajectory
above, that's still 2-3 PRs away — better to defer the ratchet than
artificially lock a sub-90% threshold.

## Test plan

- [x] `pnpm test:unit` — 42 new tests pass
- [x] `pnpm test:unit:coverage` — all 4 columns ≥ thresholds
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup:tests` — 5.84% lines (under 7% gate)
- [x] `pnpm lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [5a2ca980](https://github.com/SerendipityOneInc/ecap-workspace/commit/5a2ca9802957149f105b1497c6f87652fe79c8ac)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T08:04:42Z
- **PR**: #2095

### Commit Message

```
refactor(web): add ImagePreviewProvider onClose + no-restricted-syntax guard for URL.createObjectURL (#2095)

## Summary

#2072 createObjectURL follow-up — 把 3-PR 系列(#2075/#2076/#2089)留的两个
deferred 项合在一个 PR 里。

**ImagePreviewProvider.open() — 加 optional `onClose` callback**

provider 在 close() 或被另一次 open() 替换时 invoke callback;gallery navigate()
内不 invoke(URL 是 overlay 的,不是单张图的)。

**UploadsFeed / MyUploadsTab — 删手维护 blob URL Map**

- MyUploadsTab: 直接把 per-click URL + revoke 通过 `onClose` 传给
openImagePreview,删 `blobCacheRef` + cleanup useEffect
- UploadsFeed: 因为用 `<ImagePreview>` 直接渲染(保留 `fileName` UX),走
useEffect-on-`previewUrl` revoke;非图片 `window.open()` 路径用 ref 跟踪最近一次 blob
URL,下次 click 前/unmount 时 revoke

**Lint guard — `no-restricted-syntax` 拦 `URL.createObjectURL(...)`
直接调用**

Block 1 selector 匹配 `URL.createObjectURL` 和
`window.URL.createObjectURL`。`lib/upload.ts` / `lib/download.ts` 已在
`SRC_BLOCK1_IGNORES` 自动豁免;其余 8 处合法 caller 加 inline `//
eslint-disable-next-line no-restricted-syntax` 配 per-line lifecycle 注释。新
`src/**` 文件直接调用会被 reject,error 信息引导走 `useObjectUrl` / `triggerDownload`。

手测验证: 临时 ts 文件加 `URL.createObjectURL` lint 立刻报错。

## Test plan

- [x] `pnpm lint` 全绿(含手测 lint guard 真拦)
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 6330 测试通过(含新增 3 case for Provider.onClose + 改写
MyUploadsTab cache test 成 callback-flow test + 调整 2 处 assertion shape)
- [ ] CI: code-quality / lint-and-test 绿

## 后续

至此 #2072 createObjectURL 14 文件 follow-up 全部完成(4 PR: #2075/#2076/#2089/本
PR)。#2072 主线(event-bridge 7 个 event → `useSyncExternalStore`)仍 open,本 PR
不动。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

#2072 createObjectURL follow-up — 把 3-PR 系列(#2075/#2076/#2089)留的两个 deferred 项合在一个 PR 里。

**ImagePreviewProvider.open() — 加 optional `onClose` callback**

provider 在 close() 或被另一次 open() 替换时 invoke callback;gallery navigate() 内不 invoke(URL 是 overlay 的,不是单张图的)。

**UploadsFeed / MyUploadsTab — 删手维护 blob URL Map**

- MyUploadsTab: 直接把 per-click URL + revoke 通过 `onClose` 传给 openImagePreview,删 `blobCacheRef` + cleanup useEffect
- UploadsFeed: 因为用 `<ImagePreview>` 直接渲染(保留 `fileName` UX),走 useEffect-on-`previewUrl` revoke;非图片 `window.open()` 路径用 ref 跟踪最近一次 blob URL,下次 click 前/unmount 时 revoke

**Lint guard — `no-restricted-syntax` 拦 `URL.createObjectURL(...)` 直接调用**

Block 1 selector 匹配 `URL.createObjectURL` 和 `window.URL.createObjectURL`。`lib/upload.ts` / `lib/download.ts` 已在 `SRC_BLOCK1_IGNORES` 自动豁免;其余 8 处合法 caller 加 inline `// eslint-disable-next-line no-restricted-syntax` 配 per-line lifecycle 注释。新 `src/**` 文件直接调用会被 reject,error 信息引导走 `useObjectUrl` / `triggerDownload`。

手测验证: 临时 ts 文件加 `URL.createObjectURL` lint 立刻报错。

## Test plan

- [x] `pnpm lint` 全绿(含手测 lint guard 真拦)
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 6330 测试通过(含新增 3 case for Provider.onClose + 改写 MyUploadsTab cache test 成 callback-flow test + 调整 2 处 assertion shape)
- [ ] CI: code-quality / lint-and-test 绿

## 后续

至此 #2072 createObjectURL 14 文件 follow-up 全部完成(4 PR: #2075/#2076/#2089/本 PR)。#2072 主线(event-bridge 7 个 event → `useSyncExternalStore`)仍 open,本 PR 不动。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [58fdbb19](https://github.com/SerendipityOneInc/ecap-workspace/commit/58fdbb19845e7d2f1163ac4da9ddb5d993bf5ced)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T08:00:52Z
- **PR**: #894

### Commit Message

```
test(web): Phase 5 PR 4 — under-covered Sentry monitors + integrations API (#894) (#2101)

## Summary

PR 4 of the Phase 5 web coverage push (issue #894). Pivots from the
spec's original exclude-trim plan to targeting the highest-yield
under-covered lib modules — surfaced by parsing `coverage-summary.json`
for `(uncovered LOC × testable-logic)` descending.

## Plan deviation (intentional)

The spec called for PR 4 to be an exclude-trim per the three-audit rule,
projected +0.5-1.0pp. Given:
- PR 2 delivered +0.13pp vs projected 1.5-2.0pp (inventory inflated by
flat-name false positives)
- PR 3 delivered +0.01pp vs projected 0.8-1.2pp (utility hooks were
transitively covered already)

…exclude trim with thin happy-path specs on UI shells would have
inherited the same false-positive risk. Targeting lib modules with known
low line coverage and clear contracts gives a real delta without
regressing E2E coverage.

## What's in this PR

- **`lib/sentry/mattermost-monitor.ts`** (37.93% → ~100%) — covers
`captureMMDataIssue`, the second exported function (the
connection-failure half is already covered by
`connectionDedup.unit.spec.ts`):
  - `seq_gap` → warning + `captureMessage`
- `backfill_failed` + `post_verification_failed` → error +
`captureException`
  - Per-type 30-min dedup window with reset
  - `MAX_CAPTURES_PER_SESSION` cap (4th call silently dropped)
- Scope tag + context shape (`monitor=mattermost_data`,
`mm_data_issue=<type>`)
  - Breadcrumb level mirrors capture level
- **`lib/sentry/openclaw-monitor.ts`** (78.5% → ~100%) — covers
`startMessageLatencyTrace`:
  - User-sent breadcrumb at start
  - Fast first-delta (<15s) breadcrumb-only path
  - Warn (15-30s) + error (>30s) `captureMessage` thresholds
  - `markFirstDelta` / `markComplete` / `markError` idempotency
  - `cancel()` guard suppresses all subsequent calls
- `ttfd_ms` carried into the complete breadcrumb when `markFirstDelta`
was called
  - `elapsed()` is monotonic from start time
- **`lib/api/integrations.ts`** (16.66% → ~100%) — covers all 5 API
client functions with fetch mocking:
- URL construction (`/connections?uid=`, `/connect`,
`/connections/<provider>?uid=`, `?action=enable|disable`)
  - Method + body shape per function
  - `authHeaders` + `throwIfNotOk` wiring
- URL-encoding of uid + provider path segments (special chars / slashes)
  - `PROVIDER_CATEGORIES` canonical 6-id order
- `AVAILABLE_PROVIDERS` slug uniqueness — the picker UI relies on
`Map<slug, provider>` so a dup silently drops one
- Per-function error label (`'Failed to load integrations'`, `'Failed to
initiate connection'`, etc.)

## Coverage delta — biggest of Phase 5 so far

| Metric     | Before (post PR 3) | After  | Δ        |
|------------|--------------------|--------|----------|
| Lines      | 85.27%             | 85.51% | +0.24pp  |
| Statements | 83.19%             | 83.44% | +0.25pp  |
| Functions  | 82.44%             | 82.68% | +0.24pp  |
| Branches   | 75.69%             | 75.85% | +0.16pp  |

All four columns remain above existing thresholds (lines=83 / stmts=81 /
funcs=80 / branches=73). No threshold bump in this PR — final ratchet
lands as PR 5.

## What's still left

To hit 90% from here (~4.5pp gap), follow-up needs to target either:
- `useMattermost.ts` orchestrator (249 LOC, deferred from PR 3, would
need ~250 LOC of mocks)
- `lib/auth/manager.ts` (55 uncovered LOC at 78.8%, but heavy —
login/logout flow)
- Per-route API handlers under `src/app/api/**/route.ts` (multiple at
0%, ~18-23 LOC each)
- A few under-tested components (MMAttachments 55%, ChatGateStates 15%)

## Test plan

- [x] `pnpm test:unit` — 41 new tests pass (3 specs)
- [x] `pnpm test:unit:coverage` — all 4 columns ≥ thresholds
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup:tests` — 5.9% lines (under 7% gate)
- [x] `pnpm lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [191e9282](https://github.com/SerendipityOneInc/ecap-workspace/commit/191e9282dace0b734e90692b6704cbd1aba714c5)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T07:52:03Z
- **PR**: #2099

### Commit Message

```
refactor(web): migrate custom-agent-publish-draft-store to zustand (#2099)

## Summary

PR 3 of the [#2072
epic](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072).
Replaces the hand-rolled `useSyncExternalStore` + snapshot-cache +
module-level listeners Set in
`web/app/src/lib/custom-agent-publish-draft-store.ts` (279 lines) with a
Map of per-uid Zustand vanilla stores, each with its own `persist`
middleware backed by a uid-scoped localStorage key.

- **Backward-compatible API**: all 6 exported function helpers (`get` /
`set` / `remove` / `clear` / `subscribe` / `refresh*FromStorage`) +
`getCustomAgentPublishDraftsStorageKey` +
`CUSTOM_AGENT_PUBLISH_DRAFTS_STORAGE_KEY_PREFIX` keep their signatures.
The single production consumer (`hooks/useCustomAgentPublishes.ts`)
needs zero edits.
- **Server-bundle-safe**: store file imports only `zustand/vanilla` +
`zustand/middleware` — enforced by the must-be-zero CI guard from PR
#2074. `useCustomAgentPublishDrafts.ts` now uses
`useStore(getDraftsStoreForUid(uid), s => s.records)`.
- **Wire format intentionally preserved as flat JSON array** (NOT
Zustand envelope). Phase-0 spec #2049 contract; the cross-tab `storage`
event consumer and 4 integration tests seed localStorage directly with
flat arrays. Custom `PersistStorage` adapter unwraps the envelope on
write and wraps the flat array back on read. **No legacy data drop on
rollout** (vs. PR 2 where wire format changed).
- **Per-uid factory** (`getDraftsStoreForUid`): lazily instantiates one
Zustand store per `uid || 'anonymous'` with its own `persist.name`.
Module-level listener Set fans all per-uid stores' `subscribe` into one
global notification path — preserves the "one
`subscribeCustomAgentPublishDrafts` notifies on mutations across ALL
uids" contract.
- **`refreshCustomAgentPublishDraftsFromStorage(uid)`** now delegates to
`store.persist.rehydrate()` (was: drop snapshot cache entry + notify).
The snapshot cache is gone — Zustand selector ref equality replaces it.
- **`clearCustomAgentPublishDrafts`** uses a fresh `[]` literal (not
`EMPTY_RECORDS`) so Zustand's `Object.is` short-circuit always fires
subscribers (memory `feedback-zustand-setstate-object-is` from PR
#2088).

### 关键引用
- Epic spec:
[`docs/superpowers/specs/2026-05-28-zustand-store-migration.md`](../blob/main/docs/superpowers/specs/2026-05-28-zustand-store-migration.md)
§5 PR 3
- Parent epic PRs: #2074 (merged → infrastructure + CI guard + spec) /
#2088 (merged → PR 2 agent-description-store template)
- Phase-0 spec #2049 (wire format contract)
- PR
[#2013](https://github.com/SerendipityOneInc/ecap-workspace/pull/2013)
staging-deploy regression (server-bundle-safety hard guard)

## Test plan

- [x] All 22 existing store unit tests pass (wire format / ref-equality
/ subscriber Set / per-uid isolation / `removeCustomAgentPublishDraft`
no-op-no-notify / cross-tab refresh contracts preserved)
- [x] Updated 3 existing specs to async + `await persist.rehydrate()` so
the malformed-JSON / non-array / Storage-API-failure paths actually
exercise hydration (per memory `feedback-zustand-persist-hydration-test`
lesson from PR #2088)
- [x] +2 new hydration tests in `describe('hydration')` block — closes
the falsifiability gap Codex flagged on PR #2088 round 1 (would catch
`persist` middleware silently removed; would catch per-uid storage key
collision)
- [x] All 4 storage-boundary integration tests in
`useCustomAgentPublishes-storage.unit.spec.tsx` pass unchanged (per-uid
bucket / anonymous bucket / wire format / cross-tab event dispatch)
- [x] All 18 hook tests in `useCustomAgentPublishes.unit.spec.ts` pass
unchanged
- [x] All 21 `agent-description-store` tests + 26 `auth.storage` + 53
`auth.manager` tests pass (no consumer regression)
- [x] `bash web/scripts/check-no-react-in-stores.sh` — 4 file(s)
audited, passed
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean (with `Mutate<StoreApi,
[['zustand/persist', ...]]>` type for `.persist` accessor)
- [x] `pnpm lint:deadcode` (knip) clean
- [ ] CI 全绿(待 reviewer 等)
- [ ] reviewer 确认后,PR 4 启动 (`auth-state-changed` 15 文件迁
`useAuthSnapshot`,~600 LOC)

### 不在本 PR 范围
- 不动 `useCustomAgentPublishes.ts` 的 RQ + `useAuth` 逻辑(本 PR 只换底层 store)
- 不动 `useCustomAgentPublishes.unit.spec.ts` 的业务测试 — 仅加 reset 调用避免
Map<uid, Store> 跨 test 泄漏
- 不动 `useCustomAgentPublishes.ts` 的 cross-tab `storage` event handler —
现在它调 `refreshCustomAgentPublishDraftsFromStorage` 内部桥接到
`store.persist.rehydrate()`

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

PR 3 of the [#2072 epic](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072). Replaces the hand-rolled `useSyncExternalStore` + snapshot-cache + module-level listeners Set in `web/app/src/lib/custom-agent-publish-draft-store.ts` (279 lines) with a Map of per-uid Zustand vanilla stores, each with its own `persist` middleware backed by a uid-scoped localStorage key.

- **Backward-compatible API**: all 6 exported function helpers (`get` / `set` / `remove` / `clear` / `subscribe` / `refresh*FromStorage`) + `getCustomAgentPublishDraftsStorageKey` + `CUSTOM_AGENT_PUBLISH_DRAFTS_STORAGE_KEY_PREFIX` keep their signatures. The single production consumer (`hooks/useCustomAgentPublishes.ts`) needs zero edits.
- **Server-bundle-safe**: store file imports only `zustand/vanilla` + `zustand/middleware` — enforced by the must-be-zero CI guard from PR #2074. `useCustomAgentPublishDrafts.ts` now uses `useStore(getDraftsStoreForUid(uid), s => s.records)`.
- **Wire format intentionally preserved as flat JSON array** (NOT Zustand envelope). Phase-0 spec #2049 contract; the cross-tab `storage` event consumer and 4 integration tests seed localStorage directly with flat arrays. Custom `PersistStorage` adapter unwraps the envelope on write and wraps the flat array back on read. **No legacy data drop on rollout** (vs. PR 2 where wire format changed).
- **Per-uid factory** (`getDraftsStoreForUid`): lazily instantiates one Zustand store per `uid || 'anonymous'` with its own `persist.name`. Module-level listener Set fans all per-uid stores' `subscribe` into one global notification path — preserves the "one `subscribeCustomAgentPublishDrafts` notifies on mutations across ALL uids" contract.
- **`refreshCustomAgentPublishDraftsFromStorage(uid)`** now delegates to `store.persist.rehydrate()` (was: drop snapshot cache entry + notify). The snapshot cache is gone — Zustand selector ref equality replaces it.
- **`clearCustomAgentPublishDrafts`** uses a fresh `[]` literal (not `EMPTY_RECORDS`) so Zustand's `Object.is` short-circuit always fires subscribers (memory `feedback-zustand-setstate-object-is` from PR #2088).

### 关键引用
- Epic spec: [`docs/superpowers/specs/2026-05-28-zustand-store-migration.md`](../blob/main/docs/superpowers/specs/2026-05-28-zustand-store-migration.md) §5 PR 3
- Parent epic PRs: #2074 (merged → infrastructure + CI guard + spec) / #2088 (merged → PR 2 agent-description-store template)
- Phase-0 spec #2049 (wire format contract)
- PR [#2013](https://github.com/SerendipityOneInc/ecap-workspace/pull/2013) staging-deploy regression (server-bundle-safety hard guard)

## Test plan

- [x] All 22 existing store unit tests pass (wire format / ref-equality / subscriber Set / per-uid isolation / `removeCustomAgentPublishDraft` no-op-no-notify / cross-tab refresh contracts preserved)
- [x] Updated 3 existing specs to async + `await persist.rehydrate()` so the malformed-JSON / non-array / Storage-API-failure paths actually exercise hydration (per memory `feedback-zustand-persist-hydration-test` lesson from PR #2088)
- [x] +2 new hydration tests in `describe('hydration')` block — closes the falsifiability gap Codex flagged on PR #2088 round 1 (would catch `persist` middleware silently removed; would catch per-uid storage key collision)
- [x] All 4 storage-boundary integration tests in `useCustomAgentPublishes-storage.unit.spec.tsx` pass unchanged (per-uid bucket / anonymous bucket / wire format / cross-tab event dispatch)
- [x] All 18 hook tests in `useCustomAgentPublishes.unit.spec.ts` pass unchanged
- [x] All 21 `agent-description-store` tests + 26 `auth.storage` + 53 `auth.manager` tests pass (no consumer regression)
- [x] `bash web/scripts/check-no-react-in-stores.sh` — 4 file(s) audited, passed
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean (with `Mutate<StoreApi, [['zustand/persist', ...]]>` type for `.persist` accessor)
- [x] `pnpm lint:deadcode` (knip) clean
- [ ] CI 全绿(待 reviewer 等)
- [ ] reviewer 确认后,PR 4 启动 (`auth-state-changed` 15 文件迁 `useAuthSnapshot`,~600 LOC)

### 不在本 PR 范围
- 不动 `useCustomAgentPublishes.ts` 的 RQ + `useAuth` 逻辑(本 PR 只换底层 store)
- 不动 `useCustomAgentPublishes.unit.spec.ts` 的业务测试 — 仅加 reset 调用避免 Map<uid, Store> 跨 test 泄漏
- 不动 `useCustomAgentPublishes.ts` 的 cross-tab `storage` event handler — 现在它调 `refreshCustomAgentPublishDraftsFromStorage` 内部桥接到 `store.persist.rehydrate()`

---

## [a99f5808](https://github.com/SerendipityOneInc/ecap-workspace/commit/a99f5808eaa563f1ea170fb540f48afcf6328a0f)

- **作者**: dependabot[bot]
- **日期**: 2026-05-30T07:40:43Z
- **PR**: #2097

### Commit Message

```
chore(deps): bump litellm from 1.82.3 to 1.82.6 in /services/claw-interface in the minor-and-patch group (#2097)

Bumps the minor-and-patch group in /services/claw-interface with 1
update: [litellm](https://github.com/BerriAI/litellm).

Updates `litellm` from 1.82.3 to 1.82.6
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/BerriAI/litellm/releases">litellm's
releases</a>.</em></p>
<blockquote>
<h2>v1.83.14-stable.patch.3</h2>
<h2>Verify Docker Image Signature</h2>
<p>All LiteLLM Docker images are signed with <a
href="https://docs.sigstore.dev/cosign/overview/">cosign</a>. Every
release is signed with the same key introduced in <a
href="https://github.com/BerriAI/litellm/commit/0112e53046018d726492c814b3644b7d376029d0">commit
<code>0112e53</code></a>.</p>
<p><strong>Verify using the pinned commit hash
(recommended):</strong></p>
<p>A commit hash is cryptographically immutable, so this is the
strongest way to ensure you are using the original signing key:</p>
<pre lang="bash"><code>cosign verify \
--key
https://raw.githubusercontent.com/BerriAI/litellm/0112e53046018d726492c814b3644b7d376029d0/cosign.pub
\
  ghcr.io/berriai/litellm:v1.83.14-stable.patch.3
</code></pre>
<p><strong>Verify using the release tag (convenience):</strong></p>
<p>Tags are protected in this repository and resolve to the same key.
This option is easier to read but relies on tag protection rules:</p>
<pre lang="bash"><code>cosign verify \
--key
https://raw.githubusercontent.com/BerriAI/litellm/v1.83.14-stable.patch.3/cosign.pub
\
  ghcr.io/berriai/litellm:v1.83.14-stable.patch.3
</code></pre>
<p>Expected output:</p>
<pre><code>The following checks were performed on each of these
signatures:
  - The cosign claims were validated
  - The signatures were verified against the specified public key
</code></pre>
<hr />
<p><strong>Full Changelog</strong>: <a
href="https://github.com/BerriAI/litellm/compare/v1.83.14-stable.patch.2...v1.83.14-stable.patch.3">https://github.com/BerriAI/litellm/compare/v1.83.14-stable.patch.2...v1.83.14-stable.patch.3</a></p>
<h2>v1.83.10-stable.patch.1</h2>
<h2>Verify Docker Image Signature</h2>
<p>All LiteLLM Docker images are signed with <a
href="https://docs.sigstore.dev/cosign/overview/">cosign</a>. Every
release is signed with the same key introduced in <a
href="https://github.com/BerriAI/litellm/commit/0112e53046018d726492c814b3644b7d376029d0">commit
<code>0112e53</code></a>.</p>
<p><strong>Verify using the pinned commit hash
(recommended):</strong></p>
<p>A commit hash is cryptographically immutable, so this is the
strongest way to ensure you are using the original signing key:</p>
<pre lang="bash"><code>cosign verify \
--key
https://raw.githubusercontent.com/BerriAI/litellm/0112e53046018d726492c814b3644b7d376029d0/cosign.pub
\
  ghcr.io/berriai/litellm:v1.83.10-stable.patch.1
</code></pre>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li>See full diff in <a
href="https://github.com/BerriAI/litellm/commits">compare view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility
score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=litellm&package-manager=pip&previous-version=1.82.3&new-version=1.82.6)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't
alter it yourself. You can also trigger a rebase manually by commenting
`@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits
that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all
of the ignore conditions of the specified dependency
- `@dependabot ignore <dependency name> major version` will close this
group update PR and stop Dependabot creating any more for the specific
dependency's major version (unless you unignore this specific
dependency's major version or upgrade to it yourself)
- `@dependabot ignore <dependency name> minor version` will close this
group update PR and stop Dependabot creating any more for the specific
dependency's minor version (unless you unignore this specific
dependency's minor version or upgrade to it yourself)
- `@dependabot ignore <dependency name>` will close this group update PR
and stop Dependabot creating any more for the specific dependency
(unless you unignore this specific dependency or upgrade to it yourself)
- `@dependabot unignore <dependency name>` will remove all of the ignore
conditions of the specified dependency
- `@dependabot unignore <dependency name> <ignore condition>` will
remove the ignore condition of the specified dependency and ignore
conditions


</details>

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Description

Bumps the minor-and-patch group in /services/claw-interface with 1 update: [litellm](https://github.com/BerriAI/litellm).

Updates `litellm` from 1.82.3 to 1.82.6
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/BerriAI/litellm/releases">litellm's releases</a>.</em></p>
<blockquote>
<h2>v1.83.14-stable.patch.3</h2>
<h2>Verify Docker Image Signature</h2>
<p>All LiteLLM Docker images are signed with <a href="https://docs.sigstore.dev/cosign/overview/">cosign</a>. Every release is signed with the same key introduced in <a href="https://github.com/BerriAI/litellm/commit/0112e53046018d726492c814b3644b7d376029d0">commit <code>0112e53</code></a>.</p>
<p><strong>Verify using the pinned commit hash (recommended):</strong></p>
<p>A commit hash is cryptographically immutable, so this is the strongest way to ensure you are using the original signing key:</p>
<pre lang="bash"><code>cosign verify \
  --key https://raw.githubusercontent.com/BerriAI/litellm/0112e53046018d726492c814b3644b7d376029d0/cosign.pub \
  ghcr.io/berriai/litellm:v1.83.14-stable.patch.3
</code></pre>
<p><strong>Verify using the release tag (convenience):</strong></p>
<p>Tags are protected in this repository and resolve to the same key. This option is easier to read but relies on tag protection rules:</p>
<pre lang="bash"><code>cosign verify \
  --key https://raw.githubusercontent.com/BerriAI/litellm/v1.83.14-stable.patch.3/cosign.pub \
  ghcr.io/berriai/litellm:v1.83.14-stable.patch.3
</code></pre>
<p>Expected output:</p>
<pre><code>The following checks were performed on each of these signatures:
  - The cosign claims were validated
  - The signatures were verified against the specified public key
</code></pre>
<hr />
<p><strong>Full Changelog</strong>: <a href="https://github.com/BerriAI/litellm/compare/v1.83.14-stable.patch.2...v1.83.14-stable.patch.3">https://github.com/BerriAI/litellm/compare/v1.83.14-stable.patch.2...v1.83.14-stable.patch.3</a></p>
<h2>v1.83.10-stable.patch.1</h2>
<h2>Verify Docker Image Signature</h2>
<p>All LiteLLM Docker images are signed with <a href="https://docs.sigstore.dev/cosign/overview/">cosign</a>. Every release is signed with the same key introduced in <a href="https://github.com/BerriAI/litellm/commit/0112e53046018d726492c814b3644b7d376029d0">commit <code>0112e53</code></a>.</p>
<p><strong>Verify using the pinned commit hash (recommended):</strong></p>
<p>A commit hash is cryptographically immutable, so this is the strongest way to ensure you are using the original signing key:</p>
<pre lang="bash"><code>cosign verify \
  --key https://raw.githubusercontent.com/BerriAI/litellm/0112e53046018d726492c814b3644b7d376029d0/cosign.pub \
  ghcr.io/berriai/litellm:v1.83.10-stable.patch.1
</code></pre>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li>See full diff in <a href="https://github.com/BerriAI/litellm/commits">compare view</a></li>
</ul>
</details>
<br />


[![Dependabot compatibility score](https://dependabot-badges.githubapp.com/badges/compatibility_score?dependency-name=litellm&package-manager=pip&previous-version=1.82.3&new-version=1.82.6)](https://docs.github.com/en/github/managing-security-vulnerabilities/about-dependabot-security-updates#about-compatibility-scores)

Dependabot will resolve any conflicts with this PR as long as you don't alter it yourself. You can also trigger a rebase manually by commenting `@dependabot rebase`.

[//]: # (dependabot-automerge-start)
[//]: # (dependabot-automerge-end)

---

<details>
<summary>Dependabot commands and options</summary>
<br />

You can trigger Dependabot actions by commenting on this PR:
- `@dependabot rebase` will rebase this PR
- `@dependabot recreate` will recreate this PR, overwriting any edits that have been made to it
- `@dependabot show <dependency name> ignore conditions` will show all of the ignore conditions of the specified dependency
- `@dependabot ignore <dependency name> major version` will close this group update PR and stop Dependabot creating any more for the specific dependency's major version (unless you unignore this specific dependency's major version or upgrade to it yourself)
- `@dependabot ignore <dependency name> minor version` will close this group update PR and stop Dependabot creating any more for the specific dependency's minor version (unless you unignore this specific dependency's minor version or upgrade to it yourself)
- `@dependabot ignore <dependency name>` will close this group update PR and stop Dependabot creating any more for the specific dependency (unless you unignore this specific dependency or upgrade to it yourself)
- `@dependabot unignore <dependency name>` will remove all of the ignore conditions of the specified dependency
- `@dependabot unignore <dependency name> <ignore condition>` will remove the ignore condition of the specified dependency and ignore conditions


</details>

---

## [74441e99](https://github.com/SerendipityOneInc/ecap-workspace/commit/74441e991a40e46b840f26fe93f471f4f262b6a3)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T07:39:56Z
- **PR**: #894

### Commit Message

```
test(web): Phase 5 PR 3 — utility-hook contract specs (#894) (#2100)

## Summary

PR 3 of the Phase 5 web coverage push (issue #894). Adds dedicated unit
specs for the 3 truly-untested utility hooks. Spec:
`docs/superpowers/specs/2026-05-30-web-coverage-phase5.md` §4b (Tier C).

## What's in this PR

- **`useLatestRef.ts`** (16 LOC) — stable ref identity across renders;
latest-value mirroring via effect; the mid-flight pattern (async closure
reads latest after rerender). Every cross-uid / cross-session guard in
the codebase depends on this contract.
- **`useSavingState.ts`** (42 LOC) — idle defaults, `savingKey ↔ saving`
derivation, `withSave` success (returns `true`, clears error),
`withSave` error (returns `false`, sets message, restores `savingKey`),
non-Error thrown value falls back to `'Failed to save'`, `setError` for
caller-managed load errors, `withSave` is stable across renders. Uses
`afterEach(cleanup)` per `feedback_vitest_no_auto_cleanup`.
- **`mattermost/useStableCallback.ts`** (22 LOC) — stable identity
across renders, always invokes latest closure (never a stale snapshot),
forwards args + return, third-party-captured handlers still call the
latest callback (the originating dispatchEvent use case from
`useMattermost`).

## Coverage delta is small — and that's the honest finding

| Metric     | Before (post PR 2) | After  | Δ        |
|------------|--------------------|--------|----------|
| Lines      | 85.26%             | 85.27% | +0.01pp  |
| Statements | 83.18%             | 83.19% | +0.01pp  |
| Functions  | 82.42%             | 82.44% | +0.02pp  |
| Branches   | 75.68%             | 75.69% | +0.01pp  |

These 3 hooks are heavily executed transitively through their callers
(`useAgentSettingsQuery`, `useClawSettings`, `useMattermost`), so
dedicated specs barely move the line%. The value is the **contract
lock** — falsifiable regression coverage for hooks that until now had no
spec asserting their guarantees.

## Scope notes

- The original Tier C list (per spec §4b) had 13 hooks; the import-path
audit revealed only **3 truly untested** (+ `useMattermost.ts` itself, a
249-LOC orchestrator that needs ~250 LOC of mocks across 5 modules →
deferred to a follow-up PR).
- `useFreeStatus` / `useUserAgents` / `useArtifactAvailability` /
`useAuthBlob` false-negatived in the first flat-name pass because they
use `vi.hoisted` / `vi.mock` lazy imports — refined the audit to grep
the hook name across `tests/unit/`, confirming each had a spec.
- Other under-covered modules (`lib/sentry/mattermost-monitor.ts`
37.93%, `lib/api/integrations.ts` 16.66%, several admin tab UIs at <
30%) are better picked up in PR 4 (the exclude-trim audit) than mixed
into PR 3.

## Test plan

- [x] `pnpm test:unit` — 18 new tests pass (3 specs)
- [x] `pnpm test:unit:coverage` — all 4 columns ≥ thresholds
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup:tests` — 5.91% lines (under 7% gate)
- [x] `pnpm lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [8a93226a](https://github.com/SerendipityOneInc/ecap-workspace/commit/8a93226a9eeb4b6ec14acd9cd63bad024902cd21)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T07:28:52Z
- **PR**: #2096

### Commit Message

```
chore(deps): tighten litellm ignore to >=1.83.0 (#2096)

## What
Change the litellm Dependabot ignore boundary from `>=1.84.0` to
`>=1.83.0`.

## Why
The `>=1.84.0` boundary (from #2086) let Dependabot offer the latest
1.83.x — **#2091** (litellm → 1.83.14), which fails to resolve.
litellm's openai pin **regresses across 1.83.x patches**:

| litellm | result against current main (openai>=2.38) |
|---|---|
| 1.82.3 (current) | ✅ OK |
| 1.83.0 | ✅ OK |
| 1.83.5 | ❌ hard-pins `openai==2.30.0` |
| 1.83.10 / 1.83.14 | ❌ hard-pins `openai==2.24.0` |
| 1.84+ | ❌ needs `importlib-metadata>=8` (favie-common's opentelemetry
caps `<=7.1`) |

Dependabot always offers the *latest* in the allowed range (1.83.14), so
any allowance above 1.82.3 re-introduces a `No solution found`. Blocking
`>=1.83.0` keeps it on the working 1.82.3 instead of re-opening a broken
PR every cycle.

Closes **#2091**.

## Lift condition
When favie-common relaxes its `opentelemetry-api` pin **and** litellm
stops back-pinning openai.

## Test plan
- [x] `uv pip compile` matrix run: 1.83.0 OK, 1.83.5/1.83.10/1.83.14
conflict (openai pin), 1.84+ conflict (importlib-metadata)
- [x] dependabot.yml valid YAML; litellm ignore `>=1.83.0`

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What
Change the litellm Dependabot ignore boundary from `>=1.84.0` to `>=1.83.0`.

## Why
The `>=1.84.0` boundary (from #2086) let Dependabot offer the latest 1.83.x — **#2091** (litellm → 1.83.14), which fails to resolve. litellm's openai pin **regresses across 1.83.x patches**:

| litellm | result against current main (openai>=2.38) |
|---|---|
| 1.82.3 (current) | ✅ OK |
| 1.83.0 | ✅ OK |
| 1.83.5 | ❌ hard-pins `openai==2.30.0` |
| 1.83.10 / 1.83.14 | ❌ hard-pins `openai==2.24.0` |
| 1.84+ | ❌ needs `importlib-metadata>=8` (favie-common's opentelemetry caps `<=7.1`) |

Dependabot always offers the *latest* in the allowed range (1.83.14), so any allowance above 1.82.3 re-introduces a `No solution found`. Blocking `>=1.83.0` keeps it on the working 1.82.3 instead of re-opening a broken PR every cycle.

Closes **#2091**.

## Lift condition
When favie-common relaxes its `opentelemetry-api` pin **and** litellm stops back-pinning openai.

## Test plan
- [x] `uv pip compile` matrix run: 1.83.0 OK, 1.83.5/1.83.10/1.83.14 conflict (openai pin), 1.84+ conflict (importlib-metadata)
- [x] dependabot.yml valid YAML; litellm ignore `>=1.83.0`

---

## [250d94b0](https://github.com/SerendipityOneInc/ecap-workspace/commit/250d94b088a06b4ce2cdc9e2eacf42b152a89d41)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T07:23:06Z
- **PR**: #894

### Commit Message

```
test(web): Phase 5 PR 2 — lib pure-fn coverage (#894) (#2094)

## Summary

PR 2 of the Phase 5 web coverage push (84% → 90%, issue #894). Adds unit
specs for the 3 truly-untested pure-function modules under `src/lib/`.
Spec: `docs/superpowers/specs/2026-05-30-web-coverage-phase5.md` §4b
(Tier B).

## What's in this PR

- **`agent-install-state.ts`** (145 LOC) — 7 exported helpers:
- `getAgentWorkspace` / `hasAgentWorkspace`: workspace resolution with
the main-only default fallback
- `buildInstalledAgentsLookup`: slug-keyed (lowercased, trimmed, dedup,
empty-slug skip), preserves workspace into entries
- `getInstalledAgentsForSkill`: slug/id/name match keys with dedup
across keys
- `syncCommunitySkillWithInstalledAgents`: non-community early-out,
`official_installed` clear, managed promotion/demotion
  - `getCommunitySkillActionLabel`: Install vs Manage selection
- `getInstalledAgentsSummary`: zero / single-name / count-based
pluralization

- **`snapshot-to-open-claw-messages.ts`** (82 LOC, was 0% covered) —
inverse of the backend's MM-post normalization used by the chat-replay
page. Covers id-fallback (`sourcePostId` → replay id), `isSystem: false`
→ `undefined` normalization, attachment shape mapping with
width/height/size defaults, reaction-bucket expansion (`Math.max(1,
count)`), tool-step pass-through, and message order preservation.

- **`post-store.ts`** (50 LOC) — `EMPTY_STORE`, `propsEqual` edge cases
(undefined/empty/ref-equal/different key counts/JSON.stringify deep
compare), `postToMessage` role assignment + `Date` conversion +
`metadata.files` default.

## Coverage delta (local `pnpm test:unit:coverage`)

| Metric     | Before (post PR 1) | After  | Δ        |
|------------|--------------------|--------|----------|
| Lines      | 85.13%             | 85.26% | +0.13pp  |
| Statements | 83.03%             | 83.18% | +0.15pp  |
| Functions  | 82.34%             | 82.42% | +0.08pp  |
| Branches   | 75.45%             | 75.68% | +0.23pp  |

All four columns remain above existing thresholds (lines=83 / stmts=81 /
funcs=80 / branches=73). No threshold bump yet — final ratchet lands as
PR 5.

## Why the delta is smaller than the Tier B projection (1.5-2.0pp)

The original Tier B inventory included many modules that, on closer
audit, already had unit specs (`url-utils`, `rich-text-utils`,
`format-url`, `admin-helpers`, `product-utils`, `agent-config`,
`landing-context`, `custom-agent-publish-draft-store`, `connect-reducer`
× 2, `store-state`, `download`/`download-toast`). After the import-path
audit, only 3 modules under Tier B were truly untested. The bigger lift
remains in PR 3 (single-point hooks + mattermost sub-hooks + openclaw
watchdogs) and PR 4 (exclude trim).

Most of `agent-install-state.ts` was already indirectly covered through
skill-store callers; `snapshot-to-open-claw-messages.ts` (0% → near
100%) and `post-store.ts` (53% → near 100%) were the bigger nominal
wins.

## Test plan

- [x] `pnpm test:unit` — all tests pass (6321 + 54 new = 6375)
- [x] `pnpm test:unit:coverage` — all 4 columns ≥ thresholds
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup:tests` — 5.93% lines (under 7% gate)
- [x] `pnpm lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [82961cc3](https://github.com/SerendipityOneInc/ecap-workspace/commit/82961cc3202d68d1ce258595e3b4283bd2f6dc76)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T07:21:37Z
- **PR**: #2092

### Commit Message

```
fix(claw-interface): bump openai to 2.38, inject test api_key for ASRService (#2092)

## What
Lift the `openai<2.34` pin to `>=2.38.0,<2.39.0` by injecting a dummy
`LITELLM_PROXY_API_KEY` in the unit-test env — no production code
change.

## Why
`routes/asr.py` instantiates `ASRService` at **module import**
(`_asr_service = ASRService()`), which builds
`openai.AsyncOpenAI(api_key=SETTINGS.LITELLM_PROXY_API_KEY)`. Since
openai 2.34, `AsyncOpenAI()` rejects an **empty** api_key at
construction. The claw-interface unit-test job doesn't set
`LITELLM_PROXY_API_KEY` (defaults to `""`), so importing the app crashed
there — the documented reason openai was pinned `<2.34.0`, and why
Dependabot **#2084** (openai → 2.38) failed with `openai.OpenAIError:
Missing credentials` cascading through `test_warm_pool` /
`test_admin_cron` / `test_errors` / `test_enterprise_wiring` /
`test_storage`.

Production always injects a real key, so the construction is only empty
in CI. Fix it where the gap is: set a dummy key in `tests/conftest.py`,
using the same `os.environ.setdefault(...)` pattern already there for
`DAILY_REGISTRATION_LIMIT`. pytest imports the root conftest before
collecting (and thus before any app import), so the key is in place by
the time `ASRService()` runs.

## Changes
- `tests/conftest.py`: `os.environ.setdefault("LITELLM_PROXY_API_KEY",
"test-litellm-key")`.
- `requirements.txt`: `openai>=2.33.0,<2.34.0` → `>=2.38.0,<2.39.0`
(comment updated).

No production code changed.

## Supersedes
Carries Dependabot **#2084**'s openai bump plus the test-env fix that
makes it pass; #2084 will be closed once this merges.

## Test plan
- [x] Fresh venv with `openai==2.38.0`; affected suites pass with the
key supplied **only** by conftest (`env -u LITELLM_PROXY_API_KEY`) — 70+
passed, no import crash
- [x] `ruff` + `pyright` + import-linter clean (pre-commit all green)
- [ ] CI `claw-interface-quality` green

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What
Lift the `openai<2.34` pin to `>=2.38.0,<2.39.0` by injecting a dummy `LITELLM_PROXY_API_KEY` in the unit-test env — no production code change.

## Why
`routes/asr.py` instantiates `ASRService` at **module import** (`_asr_service = ASRService()`), which builds `openai.AsyncOpenAI(api_key=SETTINGS.LITELLM_PROXY_API_KEY)`. Since openai 2.34, `AsyncOpenAI()` rejects an **empty** api_key at construction. The claw-interface unit-test job doesn't set `LITELLM_PROXY_API_KEY` (defaults to `""`), so importing the app crashed there — the documented reason openai was pinned `<2.34.0`, and why Dependabot **#2084** (openai → 2.38) failed with `openai.OpenAIError: Missing credentials` cascading through `test_warm_pool` / `test_admin_cron` / `test_errors` / `test_enterprise_wiring` / `test_storage`.

Production always injects a real key, so the construction is only empty in CI. Fix it where the gap is: set a dummy key in `tests/conftest.py`, using the same `os.environ.setdefault(...)` pattern already there for `DAILY_REGISTRATION_LIMIT`. pytest imports the root conftest before collecting (and thus before any app import), so the key is in place by the time `ASRService()` runs.

## Changes
- `tests/conftest.py`: `os.environ.setdefault("LITELLM_PROXY_API_KEY", "test-litellm-key")`.
- `requirements.txt`: `openai>=2.33.0,<2.34.0` → `>=2.38.0,<2.39.0` (comment updated).

No production code changed.

## Supersedes
Carries Dependabot **#2084**'s openai bump plus the test-env fix that makes it pass; #2084 will be closed once this merges.

## Test plan
- [x] Fresh venv with `openai==2.38.0`; affected suites pass with the key supplied **only** by conftest (`env -u LITELLM_PROXY_API_KEY`) — 70+ passed, no import crash
- [x] `ruff` + `pyright` + import-linter clean (pre-commit all green)
- [ ] CI `claw-interface-quality` green

---

## [d7dc1799](https://github.com/SerendipityOneInc/ecap-workspace/commit/d7dc1799210d47bbeabf21a796899d9faf21b04d)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T07:10:59Z
- **PR**: #2093

### Commit Message

```
chore(ci-lint): use array for scan paths in no-collection-names script (#2093)

## 背景

PR #939（`refactor(scheduler): cleanup_stale_jobs 改走 session_job_repo`，已
merge）的 review 中提了一个 ci-lint 脚本的隐患，但对应的修正 commit 一直没有进入 main——它停留在已合并分支
`feature/scheduler-use-session-job-repo` 上、从未单独开过 PR。本 PR 把这个遗留改动重新基于最新
main 提出来。

## 改动


`services/claw-interface/scripts/ci-lint/05-no-collection-name-constants.sh`：

把空格分隔的字符串 `SCAN_DIRS` / `SCAN_FILES` 改成 bash 数组 `SCAN_PATHS=(...)`，并用
`"${SCAN_PATHS[@]}"` 展开。

**为什么**：当前单条目下空格分隔字符串能工作，但一旦新增包含空格的路径或更多条目，会因 word-splitting
静默出错。改用数组后扩展是安全的。纯加固，扫描行为不变。

## 验证

- `bash -n` 语法检查通过
- 直接运行脚本：`exit=0`，输出 `No COLLECTION_NAME aliases ...`（行为与改动前一致）

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### PR Description

## 背景

PR #939（`refactor(scheduler): cleanup_stale_jobs 改走 session_job_repo`，已 merge）的 review 中提了一个 ci-lint 脚本的隐患，但对应的修正 commit 一直没有进入 main——它停留在已合并分支 `feature/scheduler-use-session-job-repo` 上、从未单独开过 PR。本 PR 把这个遗留改动重新基于最新 main 提出来。

## 改动

`services/claw-interface/scripts/ci-lint/05-no-collection-name-constants.sh`：

把空格分隔的字符串 `SCAN_DIRS` / `SCAN_FILES` 改成 bash 数组 `SCAN_PATHS=(...)`，并用 `"${SCAN_PATHS[@]}"` 展开。

**为什么**：当前单条目下空格分隔字符串能工作，但一旦新增包含空格的路径或更多条目，会因 word-splitting 静默出错。改用数组后扩展是安全的。纯加固，扫描行为不变。

## 验证

- `bash -n` 语法检查通过
- 直接运行脚本：`exit=0`，输出 `No COLLECTION_NAME aliases ...`（行为与改动前一致）

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [9edc2ef8](https://github.com/SerendipityOneInc/ecap-workspace/commit/9edc2ef8246c784c902ca9da1f9f6ab6ba269e2f)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T06:49:30Z
- **PR**: #894

### Commit Message

```
test(web): Phase 5 spec + queries hook coverage (#894) (#2090)

## Summary

Combined Phase 5 PR 0 + PR 1 of the 84% → 90% Vitest coverage push
(issue #894). Adds the spec doc and unit tests for the 5 query-hook
modules under `src/hooks/queries/` that had no co-located spec.

## What's in this PR

- **Spec doc**:
`docs/superpowers/specs/2026-05-30-web-coverage-phase5.md` — phase goal,
PR breakdown, three-audit flow for the exclude trim PR, and the Tier X
don't-test list (`useSSEStream` deprecation, `useOpenClawInit` dead-end,
`agent-chat-client/**` excluded, etc.).
- **`tests/unit/hooks/queries/keys.unit.spec.ts`** (232 lines) — locks
the cache-key contract across **all 10 factories** (`artifact / assets /
billing / connectors / cron / integrations / mm / openclaw / sessions /
skills`); one file to avoid jscpd duplication.
- **`useArchivedSessions.unit.spec.ts`** — both `useArchivedSessions` +
`useArchivedSessionHistory`, covering enabled gate / success /
`success:false` / missing data.
- **`useClawIdentityQuery.unit.spec.ts`** — empty-string +
empty-channels normalization, enabled gate, cross-uid bucket isolation.
- **`useAgentSettingsQuery.unit.spec.ts`** — load, `saveIdentity` happy
+ cross-bucket `agentSettingsBatch` patch, `saveModel` `main`-vs-extra
dual-write, `savingError`, `reload`.
- **`useIntegrationsQuery.unit.spec.ts`** — 4 mutations × happy/error,
`pollUntilConnected` start/stop/cancel/unmount cleanup, `refresh`,
`queryError`, mutation-pending aggregation.

## Coverage delta (local `pnpm test:unit:coverage`)

| Metric     | Before  | After   | Δ        |
|------------|---------|---------|----------|
| Lines      | 84.92%  | 85.13%  | +0.21pp  |
| Statements | 82.82%  | 83.03%  | +0.21pp  |
| Functions  | 82.13%  | 82.36%  | +0.23pp  |
| Branches   | 75.24%  | 75.45%  | +0.21pp  |

All four columns remain above existing thresholds (lines=83 / stmts=81 /
funcs=80 / branches=73); **no threshold bump in this PR** — the final
ratchet lands as Phase 5 PR 5 after PRs 2-4.

## Why this PR is small (modest delta)

The truly-untested query-hook surface turned out to be narrower than the
initial inventory suggested (most of `useArtifactAvailability` /
`useCronJobs` / `useAuthBlob` / `useClawResources` / `useRuntimeSkills`
already have specs). The bigger Phase 5 lift comes from PRs 2 (lib
reducer/store/pure-fn) and 3 (single-point hooks / mattermost sub-hooks
/ openclaw watchdogs) — see the spec doc.

## Test plan

- [x] `pnpm test:unit` — all 6321 tests pass
- [x] `pnpm test:unit:coverage` — all 4 columns ≥ thresholds
- [x] `npx tsc --noEmit` — clean
- [x] `pnpm dup:tests` — 5.97% lines (under 7% gate)
- [x] `pnpm lint` — clean

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

## [7c8a3f6d](https://github.com/SerendipityOneInc/ecap-workspace/commit/7c8a3f6dca54d1a4af02c51b9312a2a617e52246)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T06:47:04Z
- **PR**: #2089

### Commit Message

```
refactor(web): converge UploadsFeed/MyUploadsTab Blob fetch to RQ cache (#2089)

## Summary

#2072 follow-up(createObjectURL 14 文件 → useObjectUrl,**不在 #2072 自身
scope**)的 PR 3 / 3。

`UploadsFeed.AssetCard` 的点击 handler 和 `MyUploadsTab.UploadRow` 的点击
handler 之前都跟 `useAuthBlob`(渲染缩略图用)并行维护一份 `Map<key, ObjectURL>` ref ——
同一个 MM 文件被 fetch 两次(一次缩略图,一次预览点击)。

本 PR 把点击 handler 的 Blob fetch 改走 `queryClient.fetchQuery({ queryKey:
mmKeys.blob(url, token), queryFn: () => fetchMmBlob(...) })`,跟
`useAuthBlob` 共享 RQ cache。点击一个缩略图已渲染的文件现在直接 hit cache,不会走网络。

## 故意保留

- **per-component URL Map + cleanup useEffect on mmToken**: 这层缓存的是**每次点击
mint 的 ObjectURL**,让用户重复点同一文件时复用 URL,并在 token rotation / unmount 时
revoke。是预览 overlay 的正确生命周期(preview 持 URL 超过点击 handler scope,无法同步
revoke)。
- **ImagePreview / ImagePreviewProvider 不动**: 给 provider 加 per-call
`onClose` callback 是更大的 API surface change;现有 Map cleanup 已经覆盖核心 leak
vectors。

## 后续可选

加 `no-restricted-syntax` lint guard 拦截 allowlist 外的
`URL.createObjectURL` 直接调用(useObjectUrl / lib/upload / lib/download /
pptx-parser 内部 helper 等)。本 series 不做以保持 diff focus,需要时单独开 PR。

## 三 PR 系列

- PR 1 #2075 (merged): `useObjectUrl` helper + spec + 迁
`useAuthBlob`/`useResolvedUrl`
- PR 2 #2076 (merged): 修 `MMAttachments` `setTimeout` race +
`pptx-parser` partial-failure leak
- PR 3 (本 PR): UploadsFeed/MyUploadsTab Blob fetch 收敛到 RQ cache

## Test plan

- [x] `pnpm lint` 全绿
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 全 6249 测试通过(含新增 1 case 锁 RQ cache 收敛 + 既有
MyUploadsTab 测试改 QueryClient wrapper)
- [ ] CI: code-quality / lint-and-test 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

#2072 follow-up(createObjectURL 14 文件 → useObjectUrl,**不在 #2072 自身 scope**)的 PR 3 / 3。

`UploadsFeed.AssetCard` 的点击 handler 和 `MyUploadsTab.UploadRow` 的点击 handler 之前都跟 `useAuthBlob`(渲染缩略图用)并行维护一份 `Map<key, ObjectURL>` ref —— 同一个 MM 文件被 fetch 两次(一次缩略图,一次预览点击)。

本 PR 把点击 handler 的 Blob fetch 改走 `queryClient.fetchQuery({ queryKey: mmKeys.blob(url, token), queryFn: () => fetchMmBlob(...) })`,跟 `useAuthBlob` 共享 RQ cache。点击一个缩略图已渲染的文件现在直接 hit cache,不会走网络。

## 故意保留

- **per-component URL Map + cleanup useEffect on mmToken**: 这层缓存的是**每次点击 mint 的 ObjectURL**,让用户重复点同一文件时复用 URL,并在 token rotation / unmount 时 revoke。是预览 overlay 的正确生命周期(preview 持 URL 超过点击 handler scope,无法同步 revoke)。
- **ImagePreview / ImagePreviewProvider 不动**: 给 provider 加 per-call `onClose` callback 是更大的 API surface change;现有 Map cleanup 已经覆盖核心 leak vectors。

## 后续可选

加 `no-restricted-syntax` lint guard 拦截 allowlist 外的 `URL.createObjectURL` 直接调用(useObjectUrl / lib/upload / lib/download / pptx-parser 内部 helper 等)。本 series 不做以保持 diff focus,需要时单独开 PR。

## 三 PR 系列

- PR 1 #2075 (merged): `useObjectUrl` helper + spec + 迁 `useAuthBlob`/`useResolvedUrl`
- PR 2 #2076 (merged): 修 `MMAttachments` `setTimeout` race + `pptx-parser` partial-failure leak
- PR 3 (本 PR): UploadsFeed/MyUploadsTab Blob fetch 收敛到 RQ cache

## Test plan

- [x] `pnpm lint` 全绿
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 全 6249 测试通过(含新增 1 case 锁 RQ cache 收敛 + 既有 MyUploadsTab 测试改 QueryClient wrapper)
- [ ] CI: code-quality / lint-and-test 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [05cd14ce](https://github.com/SerendipityOneInc/ecap-workspace/commit/05cd14cea6880a3f97d8f47610dd859bcb4b77eb)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T06:44:08Z
- **PR**: #2088

### Commit Message

```
refactor(web): migrate agent-description-store to zustand (#2088)

## Summary

PR 2 of the [#2072
epic](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072).
Replaces the hand-rolled `useSyncExternalStore` template in
`web/app/src/lib/agent-description-store.ts` (listeners `Set` +
localStorage try/catch wrappers + 3-leg Sentry capture) with a Zustand 5
vanilla store + `persist` middleware.

- **Backward-compatible API**: all 4 exported functions
(`getAgentDescription` / `setAgentDescription` /
`clearAgentDescriptions` / `subscribeAgentDescriptions`) + the
`AGENT_DESCRIPTION_STORAGE_KEY` constant keep their signatures. The 4
consumers (`auth/storage.ts`, `auth/manager.ts`,
`components/agent-settings/AgentIdentitySection.tsx`,
`hooks/useNavIdentity.ts`) work with zero edits.
- **Server-bundle-safe**: store file imports only `zustand/vanilla` +
`zustand/middleware` (no `react`, no top-level `zustand`). Enforced by
the must-be-zero CI guard `web/scripts/check-no-react-in-stores.sh`
introduced in PR #2074.
- **`useAgentDescription.ts`** now uses `useStore(agentDescriptionStore,
selector)` instead of `useSyncExternalStore(subscribe, getSnapshot,
getServerSnapshot)`. Surface unchanged.
- **Custom `PersistStorage` adapter** wraps localStorage with try/catch
+ Sentry capture on all three legs so the existing observability
contract (`agent_description_store_{read,write,clear}_failed` tags)
survives unchanged. **Net behavior change**: `read_failed` now fires
once at hydration instead of once per `getAgentDescription` call —
strict improvement (less Sentry noise, same diagnostic signal).
- **`clearAgentDescriptions`** does both `setState({byId:{}}, true)` AND
`persist.clearStorage()` (see
[[feedback-app-shell-provider-session-boundary]] memory — storage-only
clear would leak in-memory state across same-tab account switches). Uses
a fresh `{byId:{}}` literal (NOT a reused `INITIAL_STATE` constant) so
Zustand's `Object.is` short-circuit fires subscribers on every clear,
matching the hand-rolled `notify()` contract.
- **Wire format**: pre-Zustand flat `{[agentId]: description}` JSON →
Zustand persist envelope `{state: {byId: {...}}, version: 0}`. Existing
users' descriptions written in the legacy shape silently drop on first
hydration after rollout — acceptable for Tier C/D client-only UI
niceties (re-typing is the recovery path).
- **`knip.config.ts`**: drops the temporary `zustand`
`ignoreDependencies` entry added in PR #2074 (this PR introduces the
first consumer).

### 关键引用
- Epic spec:
[`docs/superpowers/specs/2026-05-28-zustand-store-migration.md`](../blob/main/docs/superpowers/specs/2026-05-28-zustand-store-migration.md)
§5 PR 2
- Parent epic PR: #2074 (merged 2026-05-30 → `dd1d5a293`)
- PR
[#2013](https://github.com/SerendipityOneInc/ecap-workspace/pull/2013)
staging deploy regression (server-bundle-safety contract)
- PR
[#1974](https://github.com/SerendipityOneInc/ecap-workspace/pull/1974)
5-round Codex (session-epoch reset pattern)

## Test plan

- [x] All 19 existing `agent-description-store.unit.spec.ts` tests pass
- [x] "Sentry on read failure" rewritten as "Sentry on hydration
failure" using `agentDescriptionStore.persist.rehydrate()` (reflects
architectural shift; behavior is strict improvement)
- [x] New regression test: `clearAgentDescriptions` clears in-memory
state independently of localStorage (Zustand singleton can leak across
same-tab logout/login without this contract)
- [x] 4 consumer specs pass with zero edits (77 tests:
AgentIdentitySection / auth.storage / auth.manager / useNavIdentity)
- [x] `bash web/scripts/check-no-react-in-stores.sh` → 4 file(s)
audited, passed
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint:deadcode` (knip) clean — zustand is now consumed
- [ ] CI `code-quality / lint-and-test` 全绿(待 reviewer 等)
- [ ] reviewer 确认后,PR 3 启动 (`custom-agent-publish-draft-store.ts`
迁移,~400 行)

### 不在本 PR 范围
- 不动 `custom-agent-publish-draft-store.ts` (PR 3)
- 不动 `OnboardingProvider.tsx`'s `useSyncExternalStore` 用法 (现状稳定,纯
ergonomics defer)
- 不加 lint rule 拦未来手写 `useSyncExternalStore` style store —— epic 完成后(PR
6)整体加

---------

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

PR 2 of the [#2072 epic](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072). Replaces the hand-rolled `useSyncExternalStore` template in `web/app/src/lib/agent-description-store.ts` (listeners `Set` + localStorage try/catch wrappers + 3-leg Sentry capture) with a Zustand 5 vanilla store + `persist` middleware.

- **Backward-compatible API**: all 4 exported functions (`getAgentDescription` / `setAgentDescription` / `clearAgentDescriptions` / `subscribeAgentDescriptions`) + the `AGENT_DESCRIPTION_STORAGE_KEY` constant keep their signatures. The 4 consumers (`auth/storage.ts`, `auth/manager.ts`, `components/agent-settings/AgentIdentitySection.tsx`, `hooks/useNavIdentity.ts`) work with zero edits.
- **Server-bundle-safe**: store file imports only `zustand/vanilla` + `zustand/middleware` (no `react`, no top-level `zustand`). Enforced by the must-be-zero CI guard `web/scripts/check-no-react-in-stores.sh` introduced in PR #2074.
- **`useAgentDescription.ts`** now uses `useStore(agentDescriptionStore, selector)` instead of `useSyncExternalStore(subscribe, getSnapshot, getServerSnapshot)`. Surface unchanged.
- **Custom `PersistStorage` adapter** wraps localStorage with try/catch + Sentry capture on all three legs so the existing observability contract (`agent_description_store_{read,write,clear}_failed` tags) survives unchanged. **Net behavior change**: `read_failed` now fires once at hydration instead of once per `getAgentDescription` call — strict improvement (less Sentry noise, same diagnostic signal).
- **`clearAgentDescriptions`** does both `setState({byId:{}}, true)` AND `persist.clearStorage()` (see [[feedback-app-shell-provider-session-boundary]] memory — storage-only clear would leak in-memory state across same-tab account switches). Uses a fresh `{byId:{}}` literal (NOT a reused `INITIAL_STATE` constant) so Zustand's `Object.is` short-circuit fires subscribers on every clear, matching the hand-rolled `notify()` contract.
- **Wire format**: pre-Zustand flat `{[agentId]: description}` JSON → Zustand persist envelope `{state: {byId: {...}}, version: 0}`. Existing users' descriptions written in the legacy shape silently drop on first hydration after rollout — acceptable for Tier C/D client-only UI niceties (re-typing is the recovery path).
- **`knip.config.ts`**: drops the temporary `zustand` `ignoreDependencies` entry added in PR #2074 (this PR introduces the first consumer).

### 关键引用
- Epic spec: [`docs/superpowers/specs/2026-05-28-zustand-store-migration.md`](../blob/main/docs/superpowers/specs/2026-05-28-zustand-store-migration.md) §5 PR 2
- Parent epic PR: #2074 (merged 2026-05-30 → `dd1d5a293`)
- PR [#2013](https://github.com/SerendipityOneInc/ecap-workspace/pull/2013) staging deploy regression (server-bundle-safety contract)
- PR [#1974](https://github.com/SerendipityOneInc/ecap-workspace/pull/1974) 5-round Codex (session-epoch reset pattern)

## Test plan

- [x] All 19 existing `agent-description-store.unit.spec.ts` tests pass
- [x] "Sentry on read failure" rewritten as "Sentry on hydration failure" using `agentDescriptionStore.persist.rehydrate()` (reflects architectural shift; behavior is strict improvement)
- [x] New regression test: `clearAgentDescriptions` clears in-memory state independently of localStorage (Zustand singleton can leak across same-tab logout/login without this contract)
- [x] 4 consumer specs pass with zero edits (77 tests: AgentIdentitySection / auth.storage / auth.manager / useNavIdentity)
- [x] `bash web/scripts/check-no-react-in-stores.sh` → 4 file(s) audited, passed
- [x] `pnpm lint` clean
- [x] `npx tsc --noEmit` clean
- [x] `pnpm lint:deadcode` (knip) clean — zustand is now consumed
- [ ] CI `code-quality / lint-and-test` 全绿(待 reviewer 等)
- [ ] reviewer 确认后,PR 3 启动 (`custom-agent-publish-draft-store.ts` 迁移,~400 行)

### 不在本 PR 范围
- 不动 `custom-agent-publish-draft-store.ts` (PR 3)
- 不动 `OnboardingProvider.tsx`'s `useSyncExternalStore` 用法 (现状稳定,纯 ergonomics defer)
- 不加 lint rule 拦未来手写 `useSyncExternalStore` style store —— epic 完成后(PR 6)整体加

---

## [e45d42e4](https://github.com/SerendipityOneInc/ecap-workspace/commit/e45d42e4c9d370d5d31bc476d6736493cd6d7e67)

- **作者**: dependabot[bot]
- **日期**: 2026-05-30T06:37:10Z
- **PR**: #2082

### Commit Message

```
chore(deps): update cachetools requirement from >=7.1.1 to >=7.1.4 in /services/claw-interface (#2082)

Updates the requirements on
[cachetools](https://github.com/tkem/cachetools) to permit the latest
version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's
changelog</a>.</em></p>
<blockquote>
<h1>v7.1.4 (2026-05-22)</h1>
<ul>
<li>
<p>Minor unit test improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.3 (2026-05-18)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.2 (2026-05-16)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Minor documentation improvements.</p>
</li>
<li>
<p>Modernize build environment.</p>
</li>
</ul>
<h1>v7.1.1 (2026-05-03)</h1>
<ul>
<li>Various type stub improvements.</li>
</ul>
<h1>v7.1.0 (2026-05-01)</h1>
<ul>
<li>
<p>Add type stubs based on the work of the good people at <code>typeshed
&lt;https://github.com/python/typeshed/tree/main/stubs/cachetools/&gt;</code>__.</p>
</li>
<li>
<p>Update unit tests.</p>
</li>
</ul>
<h1>v7.0.6 (2026-04-20)</h1>
<ul>
<li>
<p>Minor code improvements.</p>
</li>
<li>
<p>Update project URLs.</p>
</li>
<li>
<p>Update CI environment.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/tkem/cachetools/commit/48284d73d0a8834c9c50f8d41bb99e6f93b2dfed"><code>48284d7</code></a>
Release v7.1.4.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/55ea96b88a485fca9effae0f838186274f00897c"><code>55ea96b</code></a>
Update build environment.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/c5439fe5dc883220b59469e450dbcbf9f4c2e52d"><code>c5439fe</code></a>
Add threading tests for lock-only decorators.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/91828fccd629d426157a165d38563614ba06a875"><code>91828fc</code></a>
Run threading tests unconditionally with timeout.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/16952edb1eb2d2ced7601e12db722008e5156912"><code>16952ed</code></a>
Release v7.1.3.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/92dd756b93813d1ddfe70893e9c219342a52e19a"><code>92dd756</code></a>
Prepare v7.1.3.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/ced08f52ef792a010b8171715c7842da4e11b9ac"><code>ced08f5</code></a>
Improve cachetools.func type stubs.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/d809d7be5a222effd3663c33baaaee3802972daa"><code>d809d7b</code></a>
Update build environment.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/c84b5e5be3d33a32d33f0988b524fb86de1e44f2"><code>c84b5e5</code></a>
Release v7.1.2.</li>
<li><a
href="https://github.com/tkem/cachetools/commit/39ad61c1db56600fe903f3c4216996c491e775bf"><code>39ad61c</code></a>
Prepare v7.1.2.</li>
<li>Additional commits viewable in <a
href="https://github.com/tkem/cachetools/compare/v7.1.1...v7.1.4">compare
view</a></li>
</ul>
</details>
<br />

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Description

Updates the requirements on [cachetools](https://github.com/tkem/cachetools) to permit the latest version.
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/tkem/cachetools/blob/master/CHANGELOG.rst">cachetools's changelog</a>.</em></p>
<blockquote>
<h1>v7.1.4 (2026-05-22)</h1>
<ul>
<li>
<p>Minor unit test improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.3 (2026-05-18)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Update build environment.</p>
</li>
</ul>
<h1>v7.1.2 (2026-05-16)</h1>
<ul>
<li>
<p>Minor type stub improvements.</p>
</li>
<li>
<p>Minor documentation improvements.</p>
</li>
<li>
<p>Modernize build environment.</p>
</li>
</ul>
<h1>v7.1.1 (2026-05-03)</h1>
<ul>
<li>Various type stub improvements.</li>
</ul>
<h1>v7.1.0 (2026-05-01)</h1>
<ul>
<li>
<p>Add type stubs based on the work of the good people at <code>typeshed &lt;https://github.com/python/typeshed/tree/main/stubs/cachetools/&gt;</code>__.</p>
</li>
<li>
<p>Update unit tests.</p>
</li>
</ul>
<h1>v7.0.6 (2026-04-20)</h1>
<ul>
<li>
<p>Minor code improvements.</p>
</li>
<li>
<p>Update project URLs.</p>
</li>
<li>
<p>Update CI environment.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/tkem/cachetools/commit/48284d73d0a8834c9c50f8d41bb99e6f93b2dfed"><code>48284d7</code></a> Release v7.1.4.</li>
<li><a href="https://github.com/tkem/cachetools/commit/55ea96b88a485fca9effae0f838186274f00897c"><code>55ea96b</code></a> Update build environment.</li>
<li><a href="https://github.com/tkem/cachetools/commit/c5439fe5dc883220b59469e450dbcbf9f4c2e52d"><code>c5439fe</code></a> Add threading tests for lock-only decorators.</li>
<li><a href="https://github.com/tkem/cachetools/commit/91828fccd629d426157a165d38563614ba06a875"><code>91828fc</code></a> Run threading tests unconditionally with timeout.</li>
<li><a href="https://github.com/tkem/cachetools/commit/16952edb1eb2d2ced7601e12db722008e5156912"><code>16952ed</code></a> Release v7.1.3.</li>
<li><a href="https://github.com/tkem/cachetools/commit/92dd756b93813d1ddfe70893e9c219342a52e19a"><code>92dd756</code></a> Prepare v7.1.3.</li>
<li><a href="https://github.com/tkem/cachetools/commit/ced08f52ef792a010b8171715c7842da4e11b9ac"><code>ced08f5</code></a> Improve cachetools.func type stubs.</li>
<li><a href="https://github.com/tkem/cachetools/commit/d809d7be5a222effd3663c33baaaee3802972daa"><code>d809d7b</code></a> Update build environment.</li>
<li><a href="https://github.com/tkem/cachetools/commit/c84b5e5be3d33a32d33f0988b524fb86de1e44f2"><code>c84b5e5</code></a> Release v7.1.2.</li>
<li><a href="https://github.com/tkem/cachetools/commit/39ad61c1db56600fe903f3c4216996c491e775bf"><code>39ad61c</code></a> Prepare v7.1.2.</li>
<li>Additional commits viewable in <a href="https://github.com/tkem/cachetools/compare/v7.1.1...v7.1.4">compare view</a></li>
</ul>
</details>
<br />


---

## [9b85f7f4](https://github.com/SerendipityOneInc/ecap-workspace/commit/9b85f7f419b43120ed2fb99db0aff4b3e7ac0f93)

- **作者**: dependabot[bot]
- **日期**: 2026-05-30T06:32:21Z
- **PR**: #2081

### Commit Message

```
chore(deps-dev): update ruff requirement from >=0.15.12 to >=0.15.14 in /services/claw-interface (#2081)

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to
permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/releases">ruff's
releases</a>.</em></p>
<blockquote>
<h2>0.15.14</h2>
<h2>Release Notes</h2>
<p>Released on 2026-05-21.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>airflow</code>] Implement
<code>airflow-task-implicit-multiple-outputs</code>
(<code>AIR202</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25152">#25152</a>)</li>
<li>[<code>flake8-use-pathlib</code>] Mark <code>PTH101</code> fix as
unsafe when first argument is a class attribute annotated as
<code>int</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25086">#25086</a>)</li>
<li>[<code>pylint</code>] Implement <code>too-many-try-statements</code>
(<code>W0717</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/23970">#23970</a>)</li>
<li>[<code>ruff</code>] Add <code>incorrect-decorator-order</code>
(<code>RUF074</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/23461">#23461</a>)</li>
<li>[<code>ruff</code>] Add <code>fallible-context-manager</code>
(<code>RUF075</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/22844">#22844</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix lambda formatting in interpolated string expressions (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25144">#25144</a>)</li>
<li>Treat generic <code>frozenset</code> annotations as immutable (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25251">#25251</a>)</li>
<li>[<code>flake8-type-checking</code>] Avoid <code>strict</code>
behavior when <code>future-annotations</code> are enabled
(<code>TC001</code>, <code>TC002</code>, <code>TC003</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25035">#25035</a>)</li>
<li>[<code>pylint</code>] Avoid false positives in <code>else</code>
clause (<code>PLR1733</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25177">#25177</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-comprehensions</code>] Skip <code>C417</code> for
lambdas with positional-only parameters (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25272">#25272</a>)</li>
<li>[<code>flake8-simplify</code>] Preserve f-string source verbatim in
<code>SIM101</code> fix (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25061">#25061</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid unnecessary parser lookahead for operators (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25290">#25290</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Update code example setting Neovim LSP log level (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25284">#25284</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Add full PEP 798 support (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25104">#25104</a>)</li>
<li>Add a parser recursion limit (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24810">#24810</a>)</li>
<li>Update various <code>ruff_python_stdlib</code> APIs (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25273">#25273</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/ocaballeror"><code>@​ocaballeror</code></a></li>
<li><a
href="https://github.com/lerebear"><code>@​lerebear</code></a></li>
<li><a
href="https://github.com/samuelcolvin"><code>@​samuelcolvin</code></a></li>
<li><a
href="https://github.com/baltasarblanco"><code>@​baltasarblanco</code></a></li>
<li><a
href="https://github.com/aconal-com"><code>@​aconal-com</code></a></li>
<li><a
href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a
href="https://github.com/JelleZijlstra"><code>@​JelleZijlstra</code></a></li>
<li><a
href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's
changelog</a>.</em></p>
<blockquote>
<h2>0.15.14</h2>
<p>Released on 2026-05-21.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>airflow</code>] Implement
<code>airflow-task-implicit-multiple-outputs</code>
(<code>AIR202</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25152">#25152</a>)</li>
<li>[<code>flake8-use-pathlib</code>] Mark <code>PTH101</code> fix as
unsafe when first argument is a class attribute annotated as
<code>int</code> (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25086">#25086</a>)</li>
<li>[<code>pylint</code>] Implement <code>too-many-try-statements</code>
(<code>W0717</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/23970">#23970</a>)</li>
<li>[<code>ruff</code>] Add <code>incorrect-decorator-order</code>
(<code>RUF074</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/23461">#23461</a>)</li>
<li>[<code>ruff</code>] Add <code>fallible-context-manager</code>
(<code>RUF075</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/22844">#22844</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix lambda formatting in interpolated string expressions (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25144">#25144</a>)</li>
<li>Treat generic <code>frozenset</code> annotations as immutable (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25251">#25251</a>)</li>
<li>[<code>flake8-type-checking</code>] Avoid <code>strict</code>
behavior when <code>future-annotations</code> are enabled
(<code>TC001</code>, <code>TC002</code>, <code>TC003</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25035">#25035</a>)</li>
<li>[<code>pylint</code>] Avoid false positives in <code>else</code>
clause (<code>PLR1733</code>) (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25177">#25177</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-comprehensions</code>] Skip <code>C417</code> for
lambdas with positional-only parameters (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25272">#25272</a>)</li>
<li>[<code>flake8-simplify</code>] Preserve f-string source verbatim in
<code>SIM101</code> fix (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25061">#25061</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid unnecessary parser lookahead for operators (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25290">#25290</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Update code example setting Neovim LSP log level (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25284">#25284</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Add full PEP 798 support (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25104">#25104</a>)</li>
<li>Add a parser recursion limit (<a
href="https://redirect.github.com/astral-sh/ruff/pull/24810">#24810</a>)</li>
<li>Update various <code>ruff_python_stdlib</code> APIs (<a
href="https://redirect.github.com/astral-sh/ruff/pull/25273">#25273</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a
href="https://github.com/ocaballeror"><code>@​ocaballeror</code></a></li>
<li><a
href="https://github.com/lerebear"><code>@​lerebear</code></a></li>
<li><a
href="https://github.com/samuelcolvin"><code>@​samuelcolvin</code></a></li>
<li><a
href="https://github.com/baltasarblanco"><code>@​baltasarblanco</code></a></li>
<li><a
href="https://github.com/aconal-com"><code>@​aconal-com</code></a></li>
<li><a
href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a
href="https://github.com/JelleZijlstra"><code>@​JelleZijlstra</code></a></li>
<li><a
href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a
href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/astral-sh/ruff/commit/9ad2da3015e5faf73bdc5f1d09df3e47238e3edf"><code>9ad2da3</code></a>
Bump 0.15.14 (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25295">#25295</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/c714e84952510696c05ec21b0158a3548898f594"><code>c714e84</code></a>
[ty] Modernize setup of union types in mdtests (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25291">#25291</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/8a8e35ebfe318e2467a0f276e5d1a3a9032a55ad"><code>8a8e35e</code></a>
[<code>flake8-comprehensions</code>] Skip <code>C417</code> for lambdas
with positional-only parame...</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/aea5ed4d278017057c2e842c6c3a2e92ad71495f"><code>aea5ed4</code></a>
Avoid unnecessary parser lookahead for operators (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25290">#25290</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/e9d72bb420f26c23e6660bfce4dfa0028b931bff"><code>e9d72bb</code></a>
[ty] Allow enum member accesses on <code>self</code> (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25077">#25077</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/6cbd59b511a92d5f408db57bde33367c0d47b672"><code>6cbd59b</code></a>
Set <code>exclude-newer = &quot;7 days&quot;</code> in our PEP-723
scripts (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25285">#25285</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/9999a3967ae28fe3295131e8883b6947f272a076"><code>9999a39</code></a>
Update code example on how to update Neovim LSP log level (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25284">#25284</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/67d8c544f0d1c526a2fc60d4bb1358fd7956d178"><code>67d8c54</code></a>
[ty] Retain recursively-defined state in binary expressions (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25277">#25277</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/25a3191140dc0467f9d196f35c128fefde269261"><code>25a3191</code></a>
[ty] Refine Callable class-decorator fallback for unknown results (<a
href="https://redirect.github.com/astral-sh/ruff/issues/25250">#25250</a>)</li>
<li><a
href="https://github.com/astral-sh/ruff/commit/c423054dc09e5b644c926b6b527b6accfbe693e9"><code>c423054</code></a>
Add a recursion limit to the parser (<a
href="https://redirect.github.com/astral-sh/ruff/issues/24810">#24810</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/astral-sh/ruff/compare/0.15.12...0.15.14">compare
view</a></li>
</ul>
</details>
<br />

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Description

Updates the requirements on [ruff](https://github.com/astral-sh/ruff) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/releases">ruff's releases</a>.</em></p>
<blockquote>
<h2>0.15.14</h2>
<h2>Release Notes</h2>
<p>Released on 2026-05-21.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>airflow</code>] Implement <code>airflow-task-implicit-multiple-outputs</code> (<code>AIR202</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25152">#25152</a>)</li>
<li>[<code>flake8-use-pathlib</code>] Mark <code>PTH101</code> fix as unsafe when first argument is a class attribute annotated as <code>int</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/25086">#25086</a>)</li>
<li>[<code>pylint</code>] Implement <code>too-many-try-statements</code> (<code>W0717</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/23970">#23970</a>)</li>
<li>[<code>ruff</code>] Add <code>incorrect-decorator-order</code> (<code>RUF074</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/23461">#23461</a>)</li>
<li>[<code>ruff</code>] Add <code>fallible-context-manager</code> (<code>RUF075</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/22844">#22844</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix lambda formatting in interpolated string expressions (<a href="https://redirect.github.com/astral-sh/ruff/pull/25144">#25144</a>)</li>
<li>Treat generic <code>frozenset</code> annotations as immutable (<a href="https://redirect.github.com/astral-sh/ruff/pull/25251">#25251</a>)</li>
<li>[<code>flake8-type-checking</code>] Avoid <code>strict</code> behavior when <code>future-annotations</code> are enabled (<code>TC001</code>, <code>TC002</code>, <code>TC003</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25035">#25035</a>)</li>
<li>[<code>pylint</code>] Avoid false positives in <code>else</code> clause (<code>PLR1733</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25177">#25177</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-comprehensions</code>] Skip <code>C417</code> for lambdas with positional-only parameters (<a href="https://redirect.github.com/astral-sh/ruff/pull/25272">#25272</a>)</li>
<li>[<code>flake8-simplify</code>] Preserve f-string source verbatim in <code>SIM101</code> fix (<a href="https://redirect.github.com/astral-sh/ruff/pull/25061">#25061</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid unnecessary parser lookahead for operators (<a href="https://redirect.github.com/astral-sh/ruff/pull/25290">#25290</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Update code example setting Neovim LSP log level (<a href="https://redirect.github.com/astral-sh/ruff/pull/25284">#25284</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Add full PEP 798 support (<a href="https://redirect.github.com/astral-sh/ruff/pull/25104">#25104</a>)</li>
<li>Add a parser recursion limit (<a href="https://redirect.github.com/astral-sh/ruff/pull/24810">#24810</a>)</li>
<li>Update various <code>ruff_python_stdlib</code> APIs (<a href="https://redirect.github.com/astral-sh/ruff/pull/25273">#25273</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/ocaballeror"><code>@​ocaballeror</code></a></li>
<li><a href="https://github.com/lerebear"><code>@​lerebear</code></a></li>
<li><a href="https://github.com/samuelcolvin"><code>@​samuelcolvin</code></a></li>
<li><a href="https://github.com/baltasarblanco"><code>@​baltasarblanco</code></a></li>
<li><a href="https://github.com/aconal-com"><code>@​aconal-com</code></a></li>
<li><a href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/JelleZijlstra"><code>@​JelleZijlstra</code></a></li>
<li><a href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/astral-sh/ruff/blob/main/CHANGELOG.md">ruff's changelog</a>.</em></p>
<blockquote>
<h2>0.15.14</h2>
<p>Released on 2026-05-21.</p>
<h3>Preview features</h3>
<ul>
<li>[<code>airflow</code>] Implement <code>airflow-task-implicit-multiple-outputs</code> (<code>AIR202</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25152">#25152</a>)</li>
<li>[<code>flake8-use-pathlib</code>] Mark <code>PTH101</code> fix as unsafe when first argument is a class attribute annotated as <code>int</code> (<a href="https://redirect.github.com/astral-sh/ruff/pull/25086">#25086</a>)</li>
<li>[<code>pylint</code>] Implement <code>too-many-try-statements</code> (<code>W0717</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/23970">#23970</a>)</li>
<li>[<code>ruff</code>] Add <code>incorrect-decorator-order</code> (<code>RUF074</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/23461">#23461</a>)</li>
<li>[<code>ruff</code>] Add <code>fallible-context-manager</code> (<code>RUF075</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/22844">#22844</a>)</li>
</ul>
<h3>Bug fixes</h3>
<ul>
<li>Fix lambda formatting in interpolated string expressions (<a href="https://redirect.github.com/astral-sh/ruff/pull/25144">#25144</a>)</li>
<li>Treat generic <code>frozenset</code> annotations as immutable (<a href="https://redirect.github.com/astral-sh/ruff/pull/25251">#25251</a>)</li>
<li>[<code>flake8-type-checking</code>] Avoid <code>strict</code> behavior when <code>future-annotations</code> are enabled (<code>TC001</code>, <code>TC002</code>, <code>TC003</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25035">#25035</a>)</li>
<li>[<code>pylint</code>] Avoid false positives in <code>else</code> clause (<code>PLR1733</code>) (<a href="https://redirect.github.com/astral-sh/ruff/pull/25177">#25177</a>)</li>
</ul>
<h3>Rule changes</h3>
<ul>
<li>[<code>flake8-comprehensions</code>] Skip <code>C417</code> for lambdas with positional-only parameters (<a href="https://redirect.github.com/astral-sh/ruff/pull/25272">#25272</a>)</li>
<li>[<code>flake8-simplify</code>] Preserve f-string source verbatim in <code>SIM101</code> fix (<a href="https://redirect.github.com/astral-sh/ruff/pull/25061">#25061</a>)</li>
</ul>
<h3>Performance</h3>
<ul>
<li>Avoid unnecessary parser lookahead for operators (<a href="https://redirect.github.com/astral-sh/ruff/pull/25290">#25290</a>)</li>
</ul>
<h3>Documentation</h3>
<ul>
<li>Update code example setting Neovim LSP log level (<a href="https://redirect.github.com/astral-sh/ruff/pull/25284">#25284</a>)</li>
</ul>
<h3>Other changes</h3>
<ul>
<li>Add full PEP 798 support (<a href="https://redirect.github.com/astral-sh/ruff/pull/25104">#25104</a>)</li>
<li>Add a parser recursion limit (<a href="https://redirect.github.com/astral-sh/ruff/pull/24810">#24810</a>)</li>
<li>Update various <code>ruff_python_stdlib</code> APIs (<a href="https://redirect.github.com/astral-sh/ruff/pull/25273">#25273</a>)</li>
</ul>
<h3>Contributors</h3>
<ul>
<li><a href="https://github.com/ocaballeror"><code>@​ocaballeror</code></a></li>
<li><a href="https://github.com/lerebear"><code>@​lerebear</code></a></li>
<li><a href="https://github.com/samuelcolvin"><code>@​samuelcolvin</code></a></li>
<li><a href="https://github.com/baltasarblanco"><code>@​baltasarblanco</code></a></li>
<li><a href="https://github.com/aconal-com"><code>@​aconal-com</code></a></li>
<li><a href="https://github.com/anishgirianish"><code>@​anishgirianish</code></a></li>
<li><a href="https://github.com/JelleZijlstra"><code>@​JelleZijlstra</code></a></li>
<li><a href="https://github.com/AlexWaygood"><code>@​AlexWaygood</code></a></li>
<li><a href="https://github.com/ntBre"><code>@​ntBre</code></a></li>
<li><a href="https://github.com/adityasingh2400"><code>@​adityasingh2400</code></a></li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/astral-sh/ruff/commit/9ad2da3015e5faf73bdc5f1d09df3e47238e3edf"><code>9ad2da3</code></a> Bump 0.15.14 (<a href="https://redirect.github.com/astral-sh/ruff/issues/25295">#25295</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/c714e84952510696c05ec21b0158a3548898f594"><code>c714e84</code></a> [ty] Modernize setup of union types in mdtests (<a href="https://redirect.github.com/astral-sh/ruff/issues/25291">#25291</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/8a8e35ebfe318e2467a0f276e5d1a3a9032a55ad"><code>8a8e35e</code></a> [<code>flake8-comprehensions</code>] Skip <code>C417</code> for lambdas with positional-only parame...</li>
<li><a href="https://github.com/astral-sh/ruff/commit/aea5ed4d278017057c2e842c6c3a2e92ad71495f"><code>aea5ed4</code></a> Avoid unnecessary parser lookahead for operators (<a href="https://redirect.github.com/astral-sh/ruff/issues/25290">#25290</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/e9d72bb420f26c23e6660bfce4dfa0028b931bff"><code>e9d72bb</code></a> [ty] Allow enum member accesses on <code>self</code> (<a href="https://redirect.github.com/astral-sh/ruff/issues/25077">#25077</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/6cbd59b511a92d5f408db57bde33367c0d47b672"><code>6cbd59b</code></a> Set <code>exclude-newer = &quot;7 days&quot;</code> in our PEP-723 scripts (<a href="https://redirect.github.com/astral-sh/ruff/issues/25285">#25285</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/9999a3967ae28fe3295131e8883b6947f272a076"><code>9999a39</code></a> Update code example on how to update Neovim LSP log level (<a href="https://redirect.github.com/astral-sh/ruff/issues/25284">#25284</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/67d8c544f0d1c526a2fc60d4bb1358fd7956d178"><code>67d8c54</code></a> [ty] Retain recursively-defined state in binary expressions (<a href="https://redirect.github.com/astral-sh/ruff/issues/25277">#25277</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/25a3191140dc0467f9d196f35c128fefde269261"><code>25a3191</code></a> [ty] Refine Callable class-decorator fallback for unknown results (<a href="https://redirect.github.com/astral-sh/ruff/issues/25250">#25250</a>)</li>
<li><a href="https://github.com/astral-sh/ruff/commit/c423054dc09e5b644c926b6b527b6accfbe693e9"><code>c423054</code></a> Add a recursion limit to the parser (<a href="https://redirect.github.com/astral-sh/ruff/issues/24810">#24810</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/astral-sh/ruff/compare/0.15.12...0.15.14">compare view</a></li>
</ul>
</details>
<br />


---

## [c445d358](https://github.com/SerendipityOneInc/ecap-workspace/commit/c445d3584bd58759f985d46c939594ae8336b40e)

- **作者**: dependabot[bot]
- **日期**: 2026-05-30T06:31:55Z
- **PR**: #2083

### Commit Message

```
chore(deps): update pyjwt requirement from >=2.12.1 to >=2.13.0 in /services/claw-interface (#2083)

Updates the requirements on [pyjwt](https://github.com/jpadilla/pyjwt)
to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/jpadilla/pyjwt/releases">pyjwt's
releases</a>.</em></p>
<blockquote>
<h2>2.13.0</h2>
<h1>PyJWT 2.13.0 — Security Release</h1>
<p>This release bundles five security fixes plus three additional
hardening / spec-compliance changes. We recommend all users upgrade.</p>
<h2>Security</h2>
<ul>
<li>
<p><strong><a
href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-xgmm-8j9v-c9wx"><code>GHSA-xgmm-8j9v-c9wx</code></a>
— JWK JSON accepted as HMAC secret (algorithm confusion).</strong>
<code>HMACAlgorithm.prepare_key</code> previously rejected PEM- and
SSH-formatted asymmetric keys but did not catch a JWK passed as a raw
JSON string. In a verifier configured with both symmetric and asymmetric
algorithms in <code>algorithms=[…]</code> and a raw-JSON JWK as the key,
an attacker could forge HS256 tokens using the JWK text as the HMAC
secret. The guard has been extended to reject any JWK-shaped JSON.
<em>Reported by <a
href="https://github.com/aradona91"><code>@​aradona91</code></a>.</em></p>
</li>
<li>
<p><strong><a
href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-jq35-7prp-9v3f"><code>GHSA-jq35-7prp-9v3f</code></a>
— Algorithm allow-list bypass with <code>PyJWK</code> /
<code>PyJWKClient</code>.</strong> When verifying with a
<code>PyJWK</code>, the caller's <code>algorithms=[…]</code> allow-list
was checked against the token header <code>alg</code> as a string only;
actual verification used the algorithm bound to the <code>PyJWK</code>.
An attacker who controlled a registered JWKS key could sign with one
algorithm and advertise another on the header. PyJWT now requires the
token header <code>alg</code> to match the <code>PyJWK</code>'s
algorithm before verification. <em>Reported by <a
href="https://github.com/sushi-gif"><code>@​sushi-gif</code></a>.</em></p>
</li>
<li>
<p><strong><a
href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-w7vc-732c-9m39"><code>GHSA-w7vc-732c-9m39</code></a>
— DoS via base64 decode of unused payload segment when
<code>b64=false</code>.</strong> For detached-payload JWS
(<code>b64=false</code>), the compact-form payload segment was
base64-decoded before being discarded in favor of the caller-supplied
<code>detached_payload</code>. An attacker could inflate the unused
segment to force CPU + memory cost without holding a valid signature.
The segment is now required to be empty per RFC 7515 Appendix F, and is
no longer decoded. <em>Reported by <a
href="https://github.com/thesmartshadow"><code>@​thesmartshadow</code></a>.</em></p>
</li>
<li>
<p><strong><a
href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-993g-76c3-p5m4"><code>GHSA-993g-76c3-p5m4</code></a>
— <code>PyJWKClient</code> accepts non-HTTP(S) URIs.</strong>
<code>PyJWKClient.fetch_data</code> passed its URI to
<code>urllib.request.urlopen</code>, which by default also handles
<code>file://</code>, <code>ftp://</code>, and <code>data:</code>
schemes. An application that fed an attacker-influenced URI into
<code>PyJWKClient</code> could be coerced into reading local files or
reaching other unintended schemes. <code>PyJWKClient</code> now rejects
any URI whose scheme isn't <code>http</code> or <code>https</code>.
<em>Reported by <a
href="https://github.com/KEIJOT"><code>@​KEIJOT</code></a>.</em></p>
</li>
<li>
<p><strong><a
href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-fhv5-28vv-h8m8"><code>GHSA-fhv5-28vv-h8m8</code></a>
— <code>PyJWKClient</code> cache wiped on fetch error.</strong> A
<code>finally</code>-block <code>put(jwk_set=None)</code> cleared the
JWK Set cache whenever a fetch raised, turning a transient JWKS-endpoint
outage into application-wide auth failure. The cache write was moved
into the success path; transient errors no longer evict valid cached
keys. <em>Reported by <a
href="https://github.com/eddieran"><code>@​eddieran</code></a>.</em></p>
</li>
</ul>
<h2>Fixed</h2>
<ul>
<li>Reject empty HMAC keys outright in
<code>HMACAlgorithm.prepare_key</code> with <code>InvalidKeyError</code>
instead of accepting them with only a warning. Defends against the
<code>os.getenv(&quot;JWT_SECRET&quot;, &quot;&quot;)</code> footgun.
<em>Thanks to <a
href="https://github.com/SnailSploit"><code>@​SnailSploit</code></a> and
<a href="https://github.com/spartan8806"><code>@​spartan8806</code></a>
for the reports.</em></li>
<li>Forward per-call <code>options</code> (including
<code>enforce_minimum_key_length</code>) from <code>PyJWT.decode</code>
through to <code>PyJWS._verify_signature</code>. The option was
previously silently dropped between the two layers, so it only took
effect when set on the <code>PyJWT</code> instance. <em>Thanks to <a
href="https://github.com/WLUB"><code>@​WLUB</code></a> for the
report.</em></li>
<li><strong>RFC 7797 §3 compliance for <code>b64=false</code>:</strong>
the encoder now auto-adds <code>&quot;b64&quot;</code> to
<code>crit</code>, and the decoder rejects tokens that set
<code>b64=false</code> without listing it in <code>crit</code>.
<em>Thanks to <a
href="https://github.com/MachineLearning-Nerd"><code>@​MachineLearning-Nerd</code></a>
for the report.</em></li>
</ul>
<h2>Changed</h2>
<ul>
<li>Migrate the <code>dev</code>, <code>docs</code>, and
<code>tests</code> package extras to dependency groups, by <a
href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in <a
href="https://redirect.github.com/jpadilla/pyjwt/pull/1152">#1152</a>.</li>
</ul>
<h2>Upgrade notes</h2>
<p>Most fixes are invisible to correctly-configured callers. A few
behavioral changes you may encounter:</p>
<ul>
<li><strong>Empty HMAC keys now raise.</strong> If your app passed
<code>&quot;&quot;</code> or <code>b&quot;&quot;</code> as a secret
(often via a missing env var, e.g.
<code>os.getenv(&quot;JWT_SECRET&quot;, &quot;&quot;)</code>),
<code>encode</code>/<code>decode</code> will now raise
<code>InvalidKeyError</code>. This is the intended behavior — fix the
configuration.</li>
<li><strong><code>PyJWK</code> decoding now requires the token's
<code>alg</code> to match the JWK's algorithm.</strong> Previously a
mismatch was silently honored if the header <code>alg</code> appeared in
the allow-list. Tokens that relied on this mismatch will now fail with
<code>InvalidAlgorithmError</code>.</li>
<li><strong><code>PyJWKClient</code> now rejects non-HTTP(S) URIs at
construction time.</strong> Tests or dev environments that fetched JWKS
from <code>file://</code> URIs need to switch to a local HTTP server or
load the JWKS by other means (e.g. construct
<code>PyJWKSet.from_dict(...)</code> directly).</li>
<li><strong><code>b64=false</code> tokens are now strictly RFC 7515 /
7797 compliant.</strong> Tokens with a non-empty compact-form payload
segment, or that omit <code>&quot;b64&quot;</code> from
<code>crit</code>, will be rejected. PyJWT-produced tokens always
satisfy both invariants, so round-trips through PyJWT are
unaffected.</li>
<li><strong><code>enforce_minimum_key_length</code> set per-call now
takes effect.</strong> Callers who passed
<code>options={&quot;enforce_minimum_key_length&quot;: True}</code> to
<code>jwt.decode()</code> previously got no enforcement; they will now
get <code>InvalidKeyError</code> on undersized keys, as documented.</li>
</ul>
<p><strong>Full changelog:</strong> <a
href="https://github.com/jpadilla/pyjwt/compare/2.12.1...2.13.0">https://github.com/jpadilla/pyjwt/compare/2.12.1...2.13.0</a></p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/jpadilla/pyjwt/blob/master/CHANGELOG.rst">pyjwt's
changelog</a>.</em></p>
<blockquote>
<h2><code>v2.13.0
&lt;https://github.com/jpadilla/pyjwt/compare/2.12.1...2.13.0&gt;</code>__</h2>
<p>Security</p>
<pre><code>
- Reject JWK JSON documents passed as raw HMAC secrets in
  ``HMACAlgorithm.prepare_key`` to close an algorithm-confusion gap that
  the existing PEM/SSH guard did not cover. Reported by @aradona91 in
`GHSA-xgmm-8j9v-c9wx
&lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-xgmm-8j9v-c9wx&gt;`__.
- Bind the JWT header ``alg`` to ``PyJWK.algorithm_name`` during
  verification so the caller's ``algorithms=[...]`` allow-list cannot be
bypassed when decoding with a ``PyJWK`` / ``PyJWKClient`` key. Reported
by @sushi-gif in `GHSA-jq35-7prp-9v3f
&lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-jq35-7prp-9v3f&gt;`__.
- Reject non-``http(s)`` URI schemes in ``PyJWKClient`` so attacker-
influenced URIs cannot read local files or reach unintended schemes via
urllib's default ``file://`` / ``ftp://`` / ``data:`` handlers. Reported
by @KEIJOT in `GHSA-993g-76c3-p5m4
&lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-993g-76c3-p5m4&gt;`__.
- Preserve the cached JWK Set on fetch errors in
``PyJWKClient.fetch_data``.
  The previous ``finally``-block ``put(None)`` pattern cleared the cache
on any transient outage, turning one bad JWKS request into application-
wide auth failure. Reported by @eddieran in `GHSA-fhv5-28vv-h8m8
&lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-fhv5-28vv-h8m8&gt;`__.
- Skip the unconditional base64 decode of the compact-form payload
segment
  when ``b64=false`` is set in the protected header, and require that
  segment to be empty (RFC 7515 Appendix F detached form). Closes an
  unauthenticated DoS amplifier. Reported by @thesmartshadow in
`GHSA-w7vc-732c-9m39
&lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-w7vc-732c-9m39&gt;`__.
<p>Fixed</p>
<pre><code>
- Reject empty HMAC keys outright in ``HMACAlgorithm.prepare_key`` with
  ``InvalidKeyError`` instead of accepting them with only a warning.
  Thanks to @SnailSploit and @spartan8806 for independently flagging the
  footgun.
- Forward per-call ``options`` (including
``enforce_minimum_key_length``)
  from ``PyJWT.decode`` through to ``PyJWS._verify_signature`` so the
option actually takes effect when set at the call site rather than only
  on the ``PyJWT`` instance. Thanks to @WLUB for the report.
- RFC 7797 §3 compliance for ``b64=false``: the encoder now auto-adds
``&amp;quot;b64&amp;quot;`` to the ``crit`` header parameter, and the
decoder rejects
tokens that set ``b64=false`` without listing it in ``crit``. Thanks to
  @MachineLearning-Nerd for the report.

Changed
</code></pre>
<ul>
<li>Migrate the <code>dev</code>, <code>docs</code>, and
<code>tests</code> package extras to dependency groups by <a
href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in
<code>[#1152](https://github.com/jpadilla/pyjwt/issues/1152)
&amp;lt;https://github.com/jpadilla/pyjwt/pull/1152&amp;gt;</code>__</li>
</ul>
<p><code>v2.12.1
&amp;lt;https://github.com/jpadilla/pyjwt/compare/2.12.0...2.12.1&amp;gt;</code>__
&lt;/tr&gt;&lt;/table&gt;
</code></pre></p>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/7144e4534c34810f4525dc4578a32addd8212cff"><code>7144e45</code></a>
Apply ruff format</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/d2f4bec4963897c0ef96ef64a875894f2c8542ab"><code>d2f4bec</code></a>
Restore <code>cast()</code> calls with cross-version <code>type:
ignore</code> for <code>prepare_key</code></li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/22f478cebddd8294259c30f037ecb92b0b348774"><code>22f478c</code></a>
Remove redundant casts in <code>RSAAlgorithm.prepare_key</code> and
`ECAlgorithm.prepare...</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/95791b1759b8aa4f2203575d344d5c78564cdc81"><code>95791b1</code></a>
Bundle security fixes and hardening into 2.13.0</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/dcc27a9d3182a2349c30b160758785c6ce7a6508"><code>dcc27a9</code></a>
[pre-commit.ci] pre-commit autoupdate (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1155">#1155</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/9d08a9a1896845ed8eaf88e6f6ac61e5800c3e7a"><code>9d08a9a</code></a>
[pre-commit.ci] pre-commit autoupdate (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1146">#1146</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/b87c10014d4109f0214fea188d00faaaf8a80e64"><code>b87c100</code></a>
Bump codecov/codecov-action from 5 to 6 (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1154">#1154</a>)</li>
<li><a
href="https://github.com/jpadilla/pyjwt/commit/40e3147eb5f790d8d041772e5fc00728a176c812"><code>40e3147</code></a>
Migrate development extras to dependency groups (<a
href="https://redirect.github.com/jpadilla/pyjwt/issues/1152">#1152</a>)</li>
<li>See full diff in <a
href="https://github.com/jpadilla/pyjwt/compare/2.12.1...2.13.0">compare
view</a></li>
</ul>
</details>
<br />

Signed-off-by: dependabot[bot] <support@github.com>
Co-authored-by: dependabot[bot] <49699333+dependabot[bot]@users.noreply.github.com>
```

### PR Description

Updates the requirements on [pyjwt](https://github.com/jpadilla/pyjwt) to permit the latest version.
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/jpadilla/pyjwt/releases">pyjwt's releases</a>.</em></p>
<blockquote>
<h2>2.13.0</h2>
<h1>PyJWT 2.13.0 — Security Release</h1>
<p>This release bundles five security fixes plus three additional hardening / spec-compliance changes. We recommend all users upgrade.</p>
<h2>Security</h2>
<ul>
<li>
<p><strong><a href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-xgmm-8j9v-c9wx"><code>GHSA-xgmm-8j9v-c9wx</code></a> — JWK JSON accepted as HMAC secret (algorithm confusion).</strong> <code>HMACAlgorithm.prepare_key</code> previously rejected PEM- and SSH-formatted asymmetric keys but did not catch a JWK passed as a raw JSON string. In a verifier configured with both symmetric and asymmetric algorithms in <code>algorithms=[…]</code> and a raw-JSON JWK as the key, an attacker could forge HS256 tokens using the JWK text as the HMAC secret. The guard has been extended to reject any JWK-shaped JSON. <em>Reported by <a href="https://github.com/aradona91"><code>@​aradona91</code></a>.</em></p>
</li>
<li>
<p><strong><a href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-jq35-7prp-9v3f"><code>GHSA-jq35-7prp-9v3f</code></a> — Algorithm allow-list bypass with <code>PyJWK</code> / <code>PyJWKClient</code>.</strong> When verifying with a <code>PyJWK</code>, the caller's <code>algorithms=[…]</code> allow-list was checked against the token header <code>alg</code> as a string only; actual verification used the algorithm bound to the <code>PyJWK</code>. An attacker who controlled a registered JWKS key could sign with one algorithm and advertise another on the header. PyJWT now requires the token header <code>alg</code> to match the <code>PyJWK</code>'s algorithm before verification. <em>Reported by <a href="https://github.com/sushi-gif"><code>@​sushi-gif</code></a>.</em></p>
</li>
<li>
<p><strong><a href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-w7vc-732c-9m39"><code>GHSA-w7vc-732c-9m39</code></a> — DoS via base64 decode of unused payload segment when <code>b64=false</code>.</strong> For detached-payload JWS (<code>b64=false</code>), the compact-form payload segment was base64-decoded before being discarded in favor of the caller-supplied <code>detached_payload</code>. An attacker could inflate the unused segment to force CPU + memory cost without holding a valid signature. The segment is now required to be empty per RFC 7515 Appendix F, and is no longer decoded. <em>Reported by <a href="https://github.com/thesmartshadow"><code>@​thesmartshadow</code></a>.</em></p>
</li>
<li>
<p><strong><a href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-993g-76c3-p5m4"><code>GHSA-993g-76c3-p5m4</code></a> — <code>PyJWKClient</code> accepts non-HTTP(S) URIs.</strong> <code>PyJWKClient.fetch_data</code> passed its URI to <code>urllib.request.urlopen</code>, which by default also handles <code>file://</code>, <code>ftp://</code>, and <code>data:</code> schemes. An application that fed an attacker-influenced URI into <code>PyJWKClient</code> could be coerced into reading local files or reaching other unintended schemes. <code>PyJWKClient</code> now rejects any URI whose scheme isn't <code>http</code> or <code>https</code>. <em>Reported by <a href="https://github.com/KEIJOT"><code>@​KEIJOT</code></a>.</em></p>
</li>
<li>
<p><strong><a href="https://github.com/jpadilla/pyjwt/security/advisories/GHSA-fhv5-28vv-h8m8"><code>GHSA-fhv5-28vv-h8m8</code></a> — <code>PyJWKClient</code> cache wiped on fetch error.</strong> A <code>finally</code>-block <code>put(jwk_set=None)</code> cleared the JWK Set cache whenever a fetch raised, turning a transient JWKS-endpoint outage into application-wide auth failure. The cache write was moved into the success path; transient errors no longer evict valid cached keys. <em>Reported by <a href="https://github.com/eddieran"><code>@​eddieran</code></a>.</em></p>
</li>
</ul>
<h2>Fixed</h2>
<ul>
<li>Reject empty HMAC keys outright in <code>HMACAlgorithm.prepare_key</code> with <code>InvalidKeyError</code> instead of accepting them with only a warning. Defends against the <code>os.getenv(&quot;JWT_SECRET&quot;, &quot;&quot;)</code> footgun. <em>Thanks to <a href="https://github.com/SnailSploit"><code>@​SnailSploit</code></a> and <a href="https://github.com/spartan8806"><code>@​spartan8806</code></a> for the reports.</em></li>
<li>Forward per-call <code>options</code> (including <code>enforce_minimum_key_length</code>) from <code>PyJWT.decode</code> through to <code>PyJWS._verify_signature</code>. The option was previously silently dropped between the two layers, so it only took effect when set on the <code>PyJWT</code> instance. <em>Thanks to <a href="https://github.com/WLUB"><code>@​WLUB</code></a> for the report.</em></li>
<li><strong>RFC 7797 §3 compliance for <code>b64=false</code>:</strong> the encoder now auto-adds <code>&quot;b64&quot;</code> to <code>crit</code>, and the decoder rejects tokens that set <code>b64=false</code> without listing it in <code>crit</code>. <em>Thanks to <a href="https://github.com/MachineLearning-Nerd"><code>@​MachineLearning-Nerd</code></a> for the report.</em></li>
</ul>
<h2>Changed</h2>
<ul>
<li>Migrate the <code>dev</code>, <code>docs</code>, and <code>tests</code> package extras to dependency groups, by <a href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in <a href="https://redirect.github.com/jpadilla/pyjwt/pull/1152">#1152</a>.</li>
</ul>
<h2>Upgrade notes</h2>
<p>Most fixes are invisible to correctly-configured callers. A few behavioral changes you may encounter:</p>
<ul>
<li><strong>Empty HMAC keys now raise.</strong> If your app passed <code>&quot;&quot;</code> or <code>b&quot;&quot;</code> as a secret (often via a missing env var, e.g. <code>os.getenv(&quot;JWT_SECRET&quot;, &quot;&quot;)</code>), <code>encode</code>/<code>decode</code> will now raise <code>InvalidKeyError</code>. This is the intended behavior — fix the configuration.</li>
<li><strong><code>PyJWK</code> decoding now requires the token's <code>alg</code> to match the JWK's algorithm.</strong> Previously a mismatch was silently honored if the header <code>alg</code> appeared in the allow-list. Tokens that relied on this mismatch will now fail with <code>InvalidAlgorithmError</code>.</li>
<li><strong><code>PyJWKClient</code> now rejects non-HTTP(S) URIs at construction time.</strong> Tests or dev environments that fetched JWKS from <code>file://</code> URIs need to switch to a local HTTP server or load the JWKS by other means (e.g. construct <code>PyJWKSet.from_dict(...)</code> directly).</li>
<li><strong><code>b64=false</code> tokens are now strictly RFC 7515 / 7797 compliant.</strong> Tokens with a non-empty compact-form payload segment, or that omit <code>&quot;b64&quot;</code> from <code>crit</code>, will be rejected. PyJWT-produced tokens always satisfy both invariants, so round-trips through PyJWT are unaffected.</li>
<li><strong><code>enforce_minimum_key_length</code> set per-call now takes effect.</strong> Callers who passed <code>options={&quot;enforce_minimum_key_length&quot;: True}</code> to <code>jwt.decode()</code> previously got no enforcement; they will now get <code>InvalidKeyError</code> on undersized keys, as documented.</li>
</ul>
<p><strong>Full changelog:</strong> <a href="https://github.com/jpadilla/pyjwt/compare/2.12.1...2.13.0">https://github.com/jpadilla/pyjwt/compare/2.12.1...2.13.0</a></p>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/jpadilla/pyjwt/blob/master/CHANGELOG.rst">pyjwt's changelog</a>.</em></p>
<blockquote>
<h2><code>v2.13.0 &lt;https://github.com/jpadilla/pyjwt/compare/2.12.1...2.13.0&gt;</code>__</h2>
<p>Security</p>
<pre><code>
- Reject JWK JSON documents passed as raw HMAC secrets in
  ``HMACAlgorithm.prepare_key`` to close an algorithm-confusion gap that
  the existing PEM/SSH guard did not cover. Reported by @aradona91 in
  `GHSA-xgmm-8j9v-c9wx &lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-xgmm-8j9v-c9wx&gt;`__.
- Bind the JWT header ``alg`` to ``PyJWK.algorithm_name`` during
  verification so the caller's ``algorithms=[...]`` allow-list cannot be
  bypassed when decoding with a ``PyJWK`` / ``PyJWKClient`` key. Reported
  by @sushi-gif in `GHSA-jq35-7prp-9v3f &lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-jq35-7prp-9v3f&gt;`__.
- Reject non-``http(s)`` URI schemes in ``PyJWKClient`` so attacker-
  influenced URIs cannot read local files or reach unintended schemes via
  urllib's default ``file://`` / ``ftp://`` / ``data:`` handlers. Reported
  by @KEIJOT in `GHSA-993g-76c3-p5m4 &lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-993g-76c3-p5m4&gt;`__.
- Preserve the cached JWK Set on fetch errors in ``PyJWKClient.fetch_data``.
  The previous ``finally``-block ``put(None)`` pattern cleared the cache
  on any transient outage, turning one bad JWKS request into application-
  wide auth failure. Reported by @eddieran in `GHSA-fhv5-28vv-h8m8 &lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-fhv5-28vv-h8m8&gt;`__.
- Skip the unconditional base64 decode of the compact-form payload segment
  when ``b64=false`` is set in the protected header, and require that
  segment to be empty (RFC 7515 Appendix F detached form). Closes an
  unauthenticated DoS amplifier. Reported by @thesmartshadow in
  `GHSA-w7vc-732c-9m39 &lt;https://github.com/jpadilla/pyjwt/security/advisories/GHSA-w7vc-732c-9m39&gt;`__.
<p>Fixed</p>
<pre><code>
- Reject empty HMAC keys outright in ``HMACAlgorithm.prepare_key`` with
  ``InvalidKeyError`` instead of accepting them with only a warning.
  Thanks to @SnailSploit and @spartan8806 for independently flagging the
  footgun.
- Forward per-call ``options`` (including ``enforce_minimum_key_length``)
  from ``PyJWT.decode`` through to ``PyJWS._verify_signature`` so the
  option actually takes effect when set at the call site rather than only
  on the ``PyJWT`` instance. Thanks to @WLUB for the report.
- RFC 7797 §3 compliance for ``b64=false``: the encoder now auto-adds
  ``&amp;quot;b64&amp;quot;`` to the ``crit`` header parameter, and the decoder rejects
  tokens that set ``b64=false`` without listing it in ``crit``. Thanks to
  @MachineLearning-Nerd for the report.

Changed
</code></pre>
<ul>
<li>Migrate the <code>dev</code>, <code>docs</code>, and <code>tests</code> package extras to dependency groups by <a href="https://github.com/kurtmckee"><code>@​kurtmckee</code></a> in <code>[#1152](https://github.com/jpadilla/pyjwt/issues/1152) &amp;lt;https://github.com/jpadilla/pyjwt/pull/1152&amp;gt;</code>__</li>
</ul>
<p><code>v2.12.1 &amp;lt;https://github.com/jpadilla/pyjwt/compare/2.12.0...2.12.1&amp;gt;</code>__
&lt;/tr&gt;&lt;/table&gt;
</code></pre></p>
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/jpadilla/pyjwt/commit/7144e4534c34810f4525dc4578a32addd8212cff"><code>7144e45</code></a> Apply ruff format</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/d2f4bec4963897c0ef96ef64a875894f2c8542ab"><code>d2f4bec</code></a> Restore <code>cast()</code> calls with cross-version <code>type: ignore</code> for <code>prepare_key</code></li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/22f478cebddd8294259c30f037ecb92b0b348774"><code>22f478c</code></a> Remove redundant casts in <code>RSAAlgorithm.prepare_key</code> and `ECAlgorithm.prepare...</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/95791b1759b8aa4f2203575d344d5c78564cdc81"><code>95791b1</code></a> Bundle security fixes and hardening into 2.13.0</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/dcc27a9d3182a2349c30b160758785c6ce7a6508"><code>dcc27a9</code></a> [pre-commit.ci] pre-commit autoupdate (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1155">#1155</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/9d08a9a1896845ed8eaf88e6f6ac61e5800c3e7a"><code>9d08a9a</code></a> [pre-commit.ci] pre-commit autoupdate (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1146">#1146</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/b87c10014d4109f0214fea188d00faaaf8a80e64"><code>b87c100</code></a> Bump codecov/codecov-action from 5 to 6 (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1154">#1154</a>)</li>
<li><a href="https://github.com/jpadilla/pyjwt/commit/40e3147eb5f790d8d041772e5fc00728a176c812"><code>40e3147</code></a> Migrate development extras to dependency groups (<a href="https://redirect.github.com/jpadilla/pyjwt/issues/1152">#1152</a>)</li>
<li>See full diff in <a href="https://github.com/jpadilla/pyjwt/compare/2.12.1...2.13.0">compare view</a></li>
</ul>
</details>
<br />


---

## [2708ec1e](https://github.com/SerendipityOneInc/ecap-workspace/commit/2708ec1ed272b5cef635b0f5ad3367ea7efda37f)

- **作者**: dependabot[bot]
- **日期**: 2026-05-30T06:31:34Z
- **PR**: #2085

### Commit Message

```
chore(deps): bump the minor-and-patch group across 1 directory with 20 updates (#2085)

[//]: # (dependabot-start)
⚠️  **Dependabot is rebasing this PR** ⚠️ 

Rebasing might not happen immediately, so don't worry if this takes some
time.

Note: if you make any changes to this PR yourself, they will take
precedence over the rebase.

---

[//]: # (dependabot-end)

Bumps the minor-and-patch group with 20 updates in the /web directory:

| Package | From | To |
| --- | --- | --- |
|
[@assistant-ui/react](https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react)
| `0.12.28` | `0.14.7` |
|
[@opennextjs/cloudflare](https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare)
| `1.19.9` | `1.19.11` |
|
[@tanstack/query-sync-storage-persister](https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister)
| `5.100.11` | `5.100.13` |
|
[@tanstack/react-query](https://github.com/TanStack/query/tree/HEAD/packages/react-query)
| `5.100.11` | `5.100.13` |
|
[@tanstack/react-query-persist-client](https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client)
| `5.100.11` | `5.100.13` |
| [dompurify](https://github.com/cure53/DOMPurify) | `3.4.3` | `3.4.5` |
| [framer-motion](https://github.com/motiondivision/motion) | `12.38.0`
| `12.40.0` |
| [marked](https://github.com/markedjs/marked) | `18.0.3` | `18.0.4` |
| [shiki](https://github.com/shikijs/shiki/tree/HEAD/packages/shiki) |
`4.0.2` | `4.1.0` |
|
[@tanstack/react-query-devtools](https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools)
| `5.100.11` | `5.100.13` |
|
[@types/react](https://github.com/DefinitelyTyped/DefinitelyTyped/tree/HEAD/types/react)
| `19.2.14` | `19.2.15` |
|
[@vitest/coverage-v8](https://github.com/vitest-dev/vitest/tree/HEAD/packages/coverage-v8)
| `4.1.6` | `4.1.7` |
|
[@vitest/expect](https://github.com/vitest-dev/vitest/tree/HEAD/packages/expect)
| `4.1.6` | `4.1.7` |
| [firebase](https://github.com/firebase/firebase-js-sdk) | `12.12.1` |
`12.13.0` |
| [jscpd](https://github.com/kucherenko/jscpd) | `4.2.2` | `4.2.3` |
| [knip](https://github.com/webpro-nl/knip/tree/HEAD/packages/knip) |
`6.10.0` | `6.14.2` |
| [postcss](https://github.com/postcss/postcss) | `8.5.14` | `8.5.15` |
| [tsx](https://github.com/privatenumber/tsx) | `4.22.0` | `4.22.3` |
|
[vitest](https://github.com/vitest-dev/vitest/tree/HEAD/packages/vitest)
| `4.1.6` | `4.1.7` |
|
[wrangler](https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler)
| `4.90.0` | `4.94.0` |


Updates `@assistant-ui/react` from 0.12.28 to 0.14.7
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/assistant-ui/assistant-ui/releases">@​assistant-ui/react's
releases</a>.</em></p>
<blockquote>
<h2><code>@​assistant-ui/react</code><a
href="https://github.com/0"><code>@​0</code></a>.14.7</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4073">#4073</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/44ac45910cf49960ea0910cce32167d726a03ed1"><code>44ac459</code></a>
- fix(react|useSmooth): render-phase resync of displayed text on part
change (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<p>Drop one frame of stale text after a thread switch by resyncing
<code>displayedText</code> in render when the part instance flips or
<code>text</code>
breaks its streaming-append continuity, instead of waiting for
the post-commit effect.</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/assistant-ui/assistant-ui/commit/221d320cee987a4cd464c9cbae152d918197499e"><code>221d320</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.2.4</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react-langgraph</code><a
href="https://github.com/0"><code>@​0</code></a>.14.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3925">#3925</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/53cdc51665a48dfeb0220455f6c32a34981e0b0e"><code>53cdc51</code></a>
- feat(react-langgraph): track streaming timing via
<code>useLangGraphStreamingTiming</code> so
<code>useMessageTiming()</code> works on LangGraph assistant messages
(<a
href="https://github.com/shashank-100"><code>@​shashank-100</code></a>)</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/assistant-ui/assistant-ui/commit/845c7c12fecbb448da7f1135c33163b653a50710"><code>845c7c1</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/db721df32434296ac14eab27030628107975b71c"><code>db721df</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/179895fdcb56edee2e8d9efb4b38cd3859eeecdd"><code>179895f</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/3b2bbce1589b44a13b8b7a570c19bf35a2266fbd"><code>3b2bbce</code></a>]:</p>
<ul>
<li>assistant-cloud@0.1.28</li>
<li><code>@​assistant-ui/store</code><a
href="https://github.com/0"><code>@​0</code></a>.2.11</li>
<li>assistant-stream@0.3.15</li>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.2.3</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react</code><a
href="https://github.com/0"><code>@​0</code></a>.14.6</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4023">#4023</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>
- docs: add React JSDoc and deprecation notices for primitive and tool
APIs (<a
href="https://github.com/AVGVSTVS96"><code>@​AVGVSTVS96</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3513">#3513</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a>
- fix: guard <code>navigator.clipboard</code> availability and swallow
write rejections in <code>ActionBarPrimitive.Copy</code>. Previously,
copy clicks in SSR, non-HTTPS contexts, or older browsers without the
Clipboard API threw a <code>ReferenceError</code>, and permission-denied
rejections surfaced as unhandled promise rejections. The web
copyToClipboard implementation in <code>@assistant-ui/react</code> now
early-rejects when the API is unavailable, and
<code>useActionBarCopy</code> in <code>@assistant-ui/core</code>
silently absorbs the rejection so the rest of the UI is unaffected. (<a
href="https://github.com/JustAnOkapi"><code>@​JustAnOkapi</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4040">#4040</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/b481ec5129e6c1ae6de2683cdafdeecff1d8ed6b"><code>b481ec5</code></a>
- fix: <code>useExternalStoreRuntime</code> no longer leaves phantom
assistant siblings when the external store swaps a message id between
syncs (e.g. AI SDK v6 <code>useChat</code> replacing a client-generated
id with a server-provided id mid-stream, surfacing as
<code>BranchPicker</code> showing <code>2/2</code> on a turn the user
never branched). The <code>messages</code>-array sync path now diffs
against the previous sync and removes ids that disappeared, matching the
<code>messageRepository</code> path's snapshot semantics. Closes <a
href="https://redirect.github.com/assistant-ui/assistant-ui/issues/4037">#4037</a>.
(<a href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4063">#4063</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/8f0dbb80a0c89c7406bad1ad397e75831b9b8fa7"><code>8f0dbb8</code></a>
- fix thread initialization timing race which caused
<code>scrollToBottomOnInitialize</code> to fail in
<code>useLocalRuntime</code> (<a
href="https://github.com/AVGVSTVS96"><code>@​AVGVSTVS96</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3958">#3958</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a>
- refactor: hoist <code>MessagePartPrimitiveInProgress</code> to
<code>@assistant-ui/core/react</code> so
<code>@assistant-ui/react</code>, <code>@assistant-ui/react-ink</code>,
and other distributions can share the same implementation.
<code>@assistant-ui/react</code>'s
<code>MessagePartPrimitive.InProgress</code> is unchanged for callers;
it now re-exports from core. (<a
href="https://github.com/ShobhitPatra"><code>@​ShobhitPatra</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4050">#4050</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/693922b182b876b28d986f528b21d33da7c5bb51"><code>693922b</code></a>
- fix(x-buildutils): include local <code>types/</code> in
<code>typeRoots</code> so x-buildutils itself can resolve its ambient
<code>browser-process</code> types (<a
href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<p>feat(react): re-export <code>Unstable_DirectiveFormatter</code>,
<code>Unstable_DirectiveSegment</code>,
<code>Unstable_TriggerItem</code>, and
<code>unstable_defaultDirectiveFormatter</code> from
<code>@assistant-ui/core</code> so downstream packages don't need to
depend on <code>@assistant-ui/core</code> directly</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/assistant-ui/assistant-ui/commit/845c7c12fecbb448da7f1135c33163b653a50710"><code>845c7c1</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/db721df32434296ac14eab27030628107975b71c"><code>db721df</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/179895fdcb56edee2e8d9efb4b38cd3859eeecdd"><code>179895f</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/3b2bbce1589b44a13b8b7a570c19bf35a2266fbd"><code>3b2bbce</code></a>]:</p>
<ul>
<li>assistant-cloud@0.1.28</li>
<li><code>@​assistant-ui/store</code><a
href="https://github.com/0"><code>@​0</code></a>.2.11</li>
<li>assistant-stream@0.3.15</li>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.2.3</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react-langgraph</code><a
href="https://github.com/0"><code>@​0</code></a>.14.0</h2>
<h3>Minor Changes</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/assistant-ui/assistant-ui/blob/main/packages/react/CHANGELOG.md">@​assistant-ui/react's
changelog</a>.</em></p>
<blockquote>
<h2>0.14.7</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4073">#4073</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/44ac45910cf49960ea0910cce32167d726a03ed1"><code>44ac459</code></a>
- fix(react|useSmooth): render-phase resync of displayed text on part
change (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<p>Drop one frame of stale text after a thread switch by resyncing
<code>displayedText</code> in render when the part instance flips or
<code>text</code>
breaks its streaming-append continuity, instead of waiting for
the post-commit effect.</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/assistant-ui/assistant-ui/commit/221d320cee987a4cd464c9cbae152d918197499e"><code>221d320</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.2.4</li>
</ul>
</li>
</ul>
<h2>0.14.6</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4023">#4023</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>
- docs: add React JSDoc and deprecation notices for primitive and tool
APIs (<a
href="https://github.com/AVGVSTVS96"><code>@​AVGVSTVS96</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3513">#3513</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a>
- fix: guard <code>navigator.clipboard</code> availability and swallow
write rejections in <code>ActionBarPrimitive.Copy</code>. Previously,
copy clicks in SSR, non-HTTPS contexts, or older browsers without the
Clipboard API threw a <code>ReferenceError</code>, and permission-denied
rejections surfaced as unhandled promise rejections. The web
copyToClipboard implementation in <code>@assistant-ui/react</code> now
early-rejects when the API is unavailable, and
<code>useActionBarCopy</code> in <code>@assistant-ui/core</code>
silently absorbs the rejection so the rest of the UI is unaffected. (<a
href="https://github.com/JustAnOkapi"><code>@​JustAnOkapi</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4040">#4040</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/b481ec5129e6c1ae6de2683cdafdeecff1d8ed6b"><code>b481ec5</code></a>
- fix: <code>useExternalStoreRuntime</code> no longer leaves phantom
assistant siblings when the external store swaps a message id between
syncs (e.g. AI SDK v6 <code>useChat</code> replacing a client-generated
id with a server-provided id mid-stream, surfacing as
<code>BranchPicker</code> showing <code>2/2</code> on a turn the user
never branched). The <code>messages</code>-array sync path now diffs
against the previous sync and removes ids that disappeared, matching the
<code>messageRepository</code> path's snapshot semantics. Closes <a
href="https://redirect.github.com/assistant-ui/assistant-ui/issues/4037">#4037</a>.
(<a href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4063">#4063</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/8f0dbb80a0c89c7406bad1ad397e75831b9b8fa7"><code>8f0dbb8</code></a>
- fix thread initialization timing race which caused
<code>scrollToBottomOnInitialize</code> to fail in
<code>useLocalRuntime</code> (<a
href="https://github.com/AVGVSTVS96"><code>@​AVGVSTVS96</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3958">#3958</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a>
- refactor: hoist <code>MessagePartPrimitiveInProgress</code> to
<code>@assistant-ui/core/react</code> so
<code>@assistant-ui/react</code>, <code>@assistant-ui/react-ink</code>,
and other distributions can share the same implementation.
<code>@assistant-ui/react</code>'s
<code>MessagePartPrimitive.InProgress</code> is unchanged for callers;
it now re-exports from core. (<a
href="https://github.com/ShobhitPatra"><code>@​ShobhitPatra</code></a>)</p>
</li>
<li>
<p><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4050">#4050</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/693922b182b876b28d986f528b21d33da7c5bb51"><code>693922b</code></a>
- fix(x-buildutils): include local <code>types/</code> in
<code>typeRoots</code> so x-buildutils itself can resolve its ambient
<code>browser-process</code> types (<a
href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<p>feat(react): re-export <code>Unstable_DirectiveFormatter</code>,
<code>Unstable_DirectiveSegment</code>,
<code>Unstable_TriggerItem</code>, and
<code>unstable_defaultDirectiveFormatter</code> from
<code>@assistant-ui/core</code> so downstream packages don't need to
depend on <code>@assistant-ui/core</code> directly</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/assistant-ui/assistant-ui/commit/845c7c12fecbb448da7f1135c33163b653a50710"><code>845c7c1</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/db721df32434296ac14eab27030628107975b71c"><code>db721df</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/179895fdcb56edee2e8d9efb4b38cd3859eeecdd"><code>179895f</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a>,
<a
href="https://github.com/assistant-ui/assistant-ui/commit/3b2bbce1589b44a13b8b7a570c19bf35a2266fbd"><code>3b2bbce</code></a>]:</p>
<ul>
<li>assistant-cloud@0.1.28</li>
<li><code>@​assistant-ui/store</code><a
href="https://github.com/0"><code>@​0</code></a>.2.11</li>
<li>assistant-stream@0.3.15</li>
<li><code>@​assistant-ui/core</code><a
href="https://github.com/0"><code>@​0</code></a>.2.3</li>
</ul>
</li>
</ul>
<h2>0.14.5</h2>
<h3>Patch Changes</h3>
<ul>
<li>Accept the MCP-UI <code>2026-01-26</code> method names in the MCP
App bridge (e.g. <code>ui/notifications/size-changed</code>,
<code>ui/request-display-mode</code>, <code>ui/open-link</code>,
<code>ui/message</code>). Widgets built with the current xmcp
host-bridge emit these names; previously the host silently ignored them,
leaving features like auto-resize broken (iframe never received a height
change from <code>onSizeChange</code>).</li>
</ul>
<h2>0.14.4</h2>
<h3>Patch Changes</h3>
<ul>
<li><a
href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4033">#4033</a>
<a
href="https://github.com/assistant-ui/assistant-ui/commit/552ffb0ed145f2e2a57db910b99dac5d5b834626"><code>552ffb0</code></a>
- feat(react): export <code>getMcpAppFromToolPart</code> so hosts can
detect MCP-app tool parts (<a
href="https://github.com/Yonom"><code>@​Yonom</code></a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/a5c3b5433d002c6bd9db46d9416549a7c3728706"><code>a5c3b54</code></a>
chore: update versions (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4074">#4074</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/44ac45910cf49960ea0910cce32167d726a03ed1"><code>44ac459</code></a>
fix(react): resync useSmooth displayedText on part change (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4073">#4073</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/e926633f806954e07fc289c9fb12e5032ed8ff9d"><code>e926633</code></a>
chore: update versions (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4034">#4034</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/8f0dbb80a0c89c7406bad1ad397e75831b9b8fa7"><code>8f0dbb8</code></a>
fix(react): thread initialization timing race (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4063">#4063</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/179895fdcb56edee2e8d9efb4b38cd3859eeecdd"><code>179895f</code></a>
fix(core): fire streamCall for already-resolved tool calls observed live
(<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4057">#4057</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a>
fix: guard clipboard availability before calling writeText (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3513">#3513</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a>
feat(react-ink): add message part primitives (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3958">#3958</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/693922b182b876b28d986f528b21d33da7c5bb51"><code>693922b</code></a>
fix(tsconfig): TS 6.0 deprecation prep + latent dep fixes (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4050">#4050</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/612396167e28eb2500c58956038a95b6cad36624"><code>6123961</code></a>
chore: update model names throughout monorepo (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4043">#4043</a>)</li>
<li><a
href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>
docs: expand public API JSDoc and message part deprecations (<a
href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4023">#4023</a>)</li>
<li>Additional commits viewable in <a
href="https://github.com/assistant-ui/assistant-ui/commits/@assistant-ui/react@0.14.7/packages/react">compare
view</a></li>
</ul>
</details>
<br />

Updates `@opennextjs/cloudflare` from 1.19.9 to 1.19.11
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/opennextjs/opennextjs-cloudflare/releases">@​opennextjs/cloudflare's
releases</a>.</em></p>
<blockquote>
<h2><code>@​opennextjs/cloudflare</code><a
href="https://github.com/1"><code>@​1</code></a>.19.11</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1270">#1270</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/802047e7fd30c5533d5b4f754f281bc7a3fd4720"><code>802047e</code></a>
Thanks <a
href="https://github.com/alex-all3dp"><code>@​alex-all3dp</code></a>! -
fix: skip non-upload-triggered worker versions when building
skew-protection deployment mapping</p>
<p>Worker versions created by metadata-only operations (e.g. Cloudflare
API secret updates) do not include the static assets bundle. Previously,
such versions could become the &quot;latest&quot; target in the
skew-protection mapping, causing <code>/_next/static/*</code> requests
to return 404 on past deployments. Versions are now filtered to those
with <code>workers/triggered_by</code> in <code>{upload,
version_upload}</code>.</p>
<p>Closes <a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1230">#1230</a></p>
</li>
</ul>
<h2><code>@​opennextjs/cloudflare</code><a
href="https://github.com/1"><code>@​1</code></a>.19.10</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1261">#1261</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/780dd4f09c2090f1d955c90b6ddd1d6b25920850"><code>780dd4f</code></a>
Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! -
Allow populating R2 when the domain is protected by Cloudflare
Access</p>
<p>You need to:</p>
<ul>
<li>create a &quot;Service Auth&quot; policy for
&quot;open-next-cache-populate.<!-- raw HTML omitted
-->.workers.dev&quot;</li>
<li>add an &quot;Include&quot; rule for &quot;Any Access Service
Token&quot; or for a given service token (&quot;Service
Token&quot;)</li>
<li>populate the env variables CLOUDFLARE_ACCESS_CLIENT_ID and
CLOUDFLARE_ACCESS_CLIENT_SECRET</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/opennextjs/opennextjs-cloudflare/blob/main/packages/cloudflare/CHANGELOG.md">@​opennextjs/cloudflare's
changelog</a>.</em></p>
<blockquote>
<h2>1.19.11</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1270">#1270</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/802047e7fd30c5533d5b4f754f281bc7a3fd4720"><code>802047e</code></a>
Thanks <a
href="https://github.com/alex-all3dp"><code>@​alex-all3dp</code></a>! -
fix: skip non-upload-triggered worker versions when building
skew-protection deployment mapping</p>
<p>Worker versions created by metadata-only operations (e.g. Cloudflare
API secret updates) do not include the static assets bundle. Previously,
such versions could become the &quot;latest&quot; target in the
skew-protection mapping, causing <code>/_next/static/*</code> requests
to return 404 on past deployments. Versions are now filtered to those
with <code>workers/triggered_by</code> in <code>{upload,
version_upload}</code>.</p>
<p>Closes <a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1230">#1230</a></p>
</li>
</ul>
<h2>1.19.10</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1261">#1261</a>
<a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/780dd4f09c2090f1d955c90b6ddd1d6b25920850"><code>780dd4f</code></a>
Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! -
Allow populating R2 when the domain is protected by Cloudflare
Access</p>
<p>You need to:</p>
<ul>
<li>create a &quot;Service Auth&quot; policy for
&quot;open-next-cache-populate.<!-- raw HTML omitted
-->.workers.dev&quot;</li>
<li>add an &quot;Include&quot; rule for &quot;Any Access Service
Token&quot; or for a given service token (&quot;Service
Token&quot;)</li>
<li>populate the env variables CLOUDFLARE_ACCESS_CLIENT_ID and
CLOUDFLARE_ACCESS_CLIENT_SECRET</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/596f924597bd6739009004f099e975997b62240a"><code>596f924</code></a>
Version Packages (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1271">#1271</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/802047e7fd30c5533d5b4f754f281bc7a3fd4720"><code>802047e</code></a>
fix: skip non-upload-triggered worker versions in skew-protection (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1270">#1270</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/dd78941f97683dcb38ca5f2b275624c575bcec4c"><code>dd78941</code></a>
docs: clarify Cloudflare Access setup in populate-cache comment (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1267">#1267</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/49eade5577d7f31d1753f95f68a448b48bb93dd7"><code>49eade5</code></a>
Version Packages (<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1266">#1266</a>)</li>
<li><a
href="https://github.com/opennextjs/opennextjs-cloudflare/commit/780dd4f09c2090f1d955c90b6ddd1d6b25920850"><code>780dd4f</code></a>
Allow populating R2 when the domain is protected by Cloudflare Access
(<a
href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1261">#1261</a>)</li>
<li>See full diff in <a
href="https://github.com/opennextjs/opennextjs-cloudflare/commits/@opennextjs/cloudflare@1.19.11/packages/cloudflare">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/query-sync-storage-persister` from 5.100.11 to
5.100.13
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases">@​tanstack/query-sync-storage-persister's
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/query-sync-storage-persister</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/query-sync-storage-persister</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/query-sync-storage-persister/CHANGELOG.md">@​tanstack/query-sync-storage-persister's
changelog</a>.</em></p>
<blockquote>
<h2>5.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2>5.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/05cf2bc0a4eae64959dc8a40152e2878190c971b"><code>05cf2bc</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister/issues/10758">#10758</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/5ff4f6936bb66a64267eb4413430f956eecf7248"><code>5ff4f69</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister/issues/10755">#10755</a>)</li>
<li>See full diff in <a
href="https://github.com/TanStack/query/commits/@tanstack/query-sync-storage-persister@5.100.13/packages/query-sync-storage-persister">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query` from 5.100.11 to 5.100.13
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases">@​tanstack/react-query's
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/react-query/CHANGELOG.md">@​tanstack/react-query's
changelog</a>.</em></p>
<blockquote>
<h2>5.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a
href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2>5.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/05cf2bc0a4eae64959dc8a40152e2878190c971b"><code>05cf2bc</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10758">#10758</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a>
fix(query-core): use built-in NoInfer for generic indexed-access types
(<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10593">#10593</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/5ff4f6936bb66a64267eb4413430f956eecf7248"><code>5ff4f69</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10755">#10755</a>)</li>
<li>See full diff in <a
href="https://github.com/TanStack/query/commits/@tanstack/react-query@5.100.13/packages/react-query">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query-persist-client` from 5.100.11 to 5.100.13
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases">@​tanstack/react-query-persist-client's
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/react-query-persist-client/CHANGELOG.md">@​tanstack/react-query-persist-client's
changelog</a>.</em></p>
<blockquote>
<h2>5.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2>5.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/05cf2bc0a4eae64959dc8a40152e2878190c971b"><code>05cf2bc</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client/issues/10758">#10758</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/5ff4f6936bb66a64267eb4413430f956eecf7248"><code>5ff4f69</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client/issues/10755">#10755</a>)</li>
<li>See full diff in <a
href="https://github.com/TanStack/query/commits/@tanstack/react-query-persist-client@5.100.13/packages/react-query-persist-client">compare
view</a></li>
</ul>
</details>
<br />

Updates `dompurify` from 3.4.3 to 3.4.5
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/cure53/DOMPurify/releases">dompurify's
releases</a>.</em></p>
<blockquote>
<h2>DOMPurify 3.4.5</h2>
<ul>
<li>Fixed a bypass caused by the new HTML element
<code>selectedcontent</code> added in 3.4.4, thanks <a
href="https://github.com/KabirAcharya"><code>@​KabirAcharya</code></a></li>
</ul>
<p><strong>Note that this is a security release for an issue introduced
in 3.4.4 and should be upgraded to immediately.</strong></p>
<h2>DOMPurify 3.4.4</h2>
<ul>
<li>Added the <code>selectedcontent</code> element to default
allow-list, thanks <a
href="https://github.com/lukewarlow"><code>@​lukewarlow</code></a></li>
<li>Added the <code>command</code> and <code>commandfor</code>
attributes to default allowed-list, thanks <a
href="https://github.com/lukewarlow"><code>@​lukewarlow</code></a></li>
<li>Added better template scrubbing for <code>IN_PLACE</code>
operations, thanks <a
href="https://github.com/DEMON1A"><code>@​DEMON1A</code></a></li>
<li>Added stronger checks for cross-realm windows, thanks <a
href="https://github.com/DEMON1A"><code>@​DEMON1A</code></a> &amp; <a
href="https://github.com/fg0x0"><code>@​fg0x0</code></a></li>
<li>Updated demo website and made sure it uses the latest from main</li>
<li>Updated existing workflows, fuzzer, dependabot, etc., added more
tests</li>
<li>Bumped several dependencies where possible</li>
</ul>
<p>🚨 <strong>This release had been flagged as deprecated, please use
DOMPurify 3.4.5 instead</strong> 🚨</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/cure53/DOMPurify/commit/011b0c78f2a0f57ee54f5fcccb697a46ca6e63ea"><code>011b0c7</code></a>
release: 3.4.5 (<a
href="https://redirect.github.com/cure53/DOMPurify/issues/1382">#1382</a>)</li>
<li><a
href="https://github.com/cure53/DOMPurify/commit/5817ad969c15e67dfcd6cb37248d6e9c1553e7c3"><code>5817ad9</code></a>
release: 3.4.4 (<a
href="https://redirect.github.com/cure53/DOMPurify/issues/1374">#1374</a>)</li>
<li>See full diff in <a
href="https://github.com/cure53/DOMPurify/compare/3.4.3...3.4.5">compare
view</a></li>
</ul>
</details>
<br />

Updates `framer-motion` from 12.38.0 to 12.40.0
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/motiondivision/motion/blob/main/CHANGELOG.md">framer-motion's
changelog</a>.</em></p>
<blockquote>
<h2>[12.40.0] 2026-05-21</h2>
<h3>Added</h3>
<ul>
<li><code>path</code> option to <code>transition</code>.</li>
<li><code>arc()</code> for motion along an arc.</li>
</ul>
<h2>[12.39.0] 2026-05-18</h2>
<h3>Added</h3>
<ul>
<li>Support for <code>repeatType</code> and <code>repeatDelay</code> in
animation sequences.</li>
</ul>
<h3>Fixed</h3>
<ul>
<li>Variants: Re-run keyframe animations when switching between variant
labels even when they share identical keyframe arrays.</li>
<li>Drag: Preserve in-flight motion value animations across React 19
reorder unmount/remount so <code>dragSnapToOrigin</code> no longer
leaves the drag transform stranded after a layout swap.</li>
<li><code>LazyMotion</code>: Share React contexts between the
<code>framer-motion</code> and <code>framer-motion/m</code> (and
therefore <code>motion/react</code> and <code>motion/react-m</code>) CJS
bundles so that <code>&lt;m.div&gt;</code> from the <code>/m</code>
subpath picks up features loaded by <code>&lt;LazyMotion&gt;</code> from
the main entry point.</li>
<li><code>useScroll</code>: Support hydrating <code>target</code> and
<code>container</code> refs from anywhere in the tree.</li>
<li>Drag: Gesture no longer starts from incorrect start point when
rendered inside <code>&lt;AnimatePresence initial={false}
/&gt;</code>.</li>
<li>Drag: <code>dragConstraints</code>, when set as viewport-relative
ref, no longer break on scroll.§</li>
<li>Updated <code>visualElement</code> hydration order.</li>
<li><code>useAnimate</code>: Now respects
<code>skipAnimations</code>.</li>
<li><code>AnimatePresence</code>: Fix object-form <code>initial</code>
values not applied on re-entry after exit completes.</li>
<li><code>scroll</code>: Fixed callback progress when tracking an
element.</li>
<li><code>useScroll</code>: Fix hardware acceleration when tracking an
element.</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/motiondivision/motion/commit/38ebb9480e5b25a51e09e2ec866c101d01d82c60"><code>38ebb94</code></a>
v12.40.0</li>
<li><a
href="https://github.com/motiondivision/motion/commit/b1f766c7221cfdbf868e2f66675d6d2e2ff8f50e"><code>b1f766c</code></a>
Latest</li>
<li><a
href="https://github.com/motiondivision/motion/commit/bca554401519e8ef45db1dcc8c52580998251c73"><code>bca5544</code></a>
Merge pull request <a
href="https://redirect.github.com/motiondivision/motion/issues/3699">#3699</a>
from motiondivision/lochie/arcs-injectable</li>
<li><a
href="https://github.com/motiondivision/motion/commit/f1a96cfaff8de87712539bf250205134c8e121d9"><code>f1a96cf</code></a>
arc(): rename amp/rotate, expose MotionPath, fix explicit cw/ccw</li>
<li><a
href="https://github.com/motiondivision/motion/commit/b4aaba0d161cce6db7b2070ec3fd141e1dbcda95"><code>b4aaba0</code></a>
pathRotation: non-destructive orientToPath rotation channel</li>
<li><a
href="https://github.com/motiondivision/motion/commit/8604ef3d9048127d61a8bbd94698e56368e70926"><code>8604ef3</code></a>
Make arcs injectable via <code>transition.path = arc()</code></li>
<li><a
href="https://github.com/motiondivision/motion/commit/f90fe294c559c3bd7b13e762b0b2aefe837dc000"><code>f90fe29</code></a>
add <code>orientToPath</code></li>
<li><a
href="https://github.com/motiondivision/motion/commit/9ebe999fe93e6431ce026a998cb2aeabe690d03b"><code>9ebe999</code></a>
fix: test</li>
<li><a
href="https://github.com/motiondivision/motion/commit/bc2107e8963b35c0f264810d8dcb8b7b96ac7cb5"><code>bc2107e</code></a>
Revert &quot;no should&quot;</li>
<li><a
href="https://github.com/motiondivision/motion/commit/6eeb92dc2228419a1d2ba33bec5df36c3357683a"><code>6eeb92d</code></a>
no should</li>
<li>Additional commits viewable in <a
href="https://github.com/motiondivision/motion/compare/v12.38.0...v12.40.0">compare
view</a></li>
</ul>
</details>
<br />

Updates `marked` from 18.0.3 to 18.0.4
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/markedjs/marked/releases">marked's
releases</a>.</em></p>
<blockquote>
<h2>v18.0.4</h2>
<h2><a
href="https://github.com/markedjs/marked/compare/v18.0.3...v18.0.4">18.0.4</a>
(2026-05-19)</h2>
<h3>Bug Fixes</h3>
<ul>
<li>cache list indentation regexes (<a
href="https://redirect.github.com/markedjs/marked/issues/3969">#3969</a>)
(<a
href="https://github.com/markedjs/marked/commit/a37983f188d697fe98d350554dc95c49eaac6edd">a37983f</a>)</li>
<li>fix cli not reading stdin (<a
href="https://redirect.github.com/markedjs/marked/issues/3967">#3967</a>)
(<a
href="https://github.com/markedjs/marked/commit/11adb697eeee2b0fa6da3a38d5146626347592dc">11adb69</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/markedjs/marked/commit/0a2cd54cbe91911890e4460ae4fd7b9966e05654"><code>0a2cd54</code></a>
chore(release): 18.0.4 [skip ci]</li>
<li><a
href="https://github.com/markedjs/marked/commit/11adb697eeee2b0fa6da3a38d5146626347592dc"><code>11adb69</code></a>
fix: fix cli not reading stdin (<a
href="https://redirect.github.com/markedjs/marked/issues/3967">#3967</a>)</li>
<li><a
href="https://github.com/markedjs/marked/commit/a37983f188d697fe98d350554dc95c49eaac6edd"><code>a37983f</code></a>
fix: cache list indentation regexes (<a
href="https://redirect.github.com/markedjs/marked/issues/3969">#3969</a>)</li>
<li><a
href="https://github.com/markedjs/marked/commit/d38b8c27e75a0d64fa2ff233a81a8b976210f1f1"><code>d38b8c2</code></a>
chore(deps-dev): bump eslint from 10.3.0 to 10.4.0 (<a
href="https://redirect.github.com/markedjs/marked/issues/3976">#3976</a>)</li>
<li><a
href="https://github.com/markedjs/marked/commit/7d9b17e8cd13af580fa404d114401043b5510344"><code>7d9b17e</code></a>
chore(docs): fix typo in package links (<a
href="https://redirect.github.com/markedjs/marked/issues/3975">#3975</a>)</li>
<li><a
href="https://github.com/markedjs/marked/commit/a7affc3b8ba7fc99481b6582ab5baa860228ec86"><code>a7affc3</code></a>
chore(deps-dev): bump
<code>@​semantic-release/release-notes-generator</code> from 14.1.0
t...</li>
<li><a
href="https://github.com/markedjs/marked/commit/47d6ba1898437d913affd87180e157e47bf5c101"><code>47d6ba1</code></a>
chore(deps-dev): bump <code>@​semantic-release/github</code> from 12.0.6
to 12.0.8 (<a
href="https://redirect.github.com/markedjs/marked/issues/3972">#3972</a>)</li>
<li><a
href="https://github.com/markedjs/marked/commit/69257e455e599e9c9ddedcaf913569279b12c20c"><code>69257e4</code></a>
chore(deps-dev): bump eslint from 10.2.1 to 10.3.0 (<a
href="https://redirect.github.com/markedjs/marked/issues/3966">#3966</a>)</li>
<li><a
href="https://github.com/markedjs/marked/commit/1731d387f76ac98601a83504b217c2d7f5643898"><code>1731d38</code></a>
refactor(test): move task list output coverage to specs (<a
href="https://redirect.github.com/markedjs/marked/issues/3963">#3963</a>)</li>
<li>See full diff in <a
href="https://github.com/markedjs/marked/compare/v18.0.3...v18.0.4">compare
view</a></li>
</ul>
</details>
<br />

Updates `shiki` from 4.0.2 to 4.1.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/shikijs/shiki/releases">shiki's
releases</a>.</em></p>
<blockquote>
<h2>v4.1.0</h2>
<h3>   🐞 Bug Fixes</h3>
<ul>
<li><strong>twoslash</strong>: Forward <code>tsModule</code> to
<code>createTwoslasher</code>  -  by <a
href="https://github.com/arthurfiorette"><code>@​arthurfiorette</code></a>
in <a
href="https://redirect.github.com/shikijs/shiki/issues/1271">shikijs/shiki#1271</a>
<a href="https://github.com/shikijs/shiki/commit/be89afcf"><!-- raw HTML
omitted -->(be89a)<!-- raw HTML omitted --></a></li>
</ul>
<h5>    <a
href="https://github.com/shikijs/shiki/compare/v4.0.2...v4.1.0">View
changes on GitHub</a></h5>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/shikijs/shiki/commit/c809af96f1907877c5cebfeee98ac5d55193140b"><code>c809af9</code></a>
chore: release v4.1.0</li>
<li><a
href="https://github.com/shikijs/shiki/commit/95371cb1b3c00ced5b437a11f603939002f9ecae"><code>95371cb</code></a>
chore: lint</li>
<li>See full diff in <a
href="https://github.com/shikijs/shiki/commits/v4.1.0/packages/shiki">compare
view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query-devtools` from 5.100.11 to 5.100.13
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/releases">@​tanstack/react-query-devtools's
releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a
href="https://github.com/TanStack/query/blob/main/packages/react-query-devtools/CHANGELOG.md">@​tanstack/react-query-devtools's
changelog</a>.</em></p>
<blockquote>
<h2>5.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2>5.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a
href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/TanStack/query/commit/05cf2bc0a4eae64959dc8a40152e2878190c971b"><code>05cf2bc</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools/issues/10758">#10758</a>)</li>
<li><a
href="https://github.com/TanStack/query/commit/5ff4f6936bb66a64267eb4413430f956eecf7248"><code>5ff4f69</code></a>
ci: Version Packages (<a
href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools/issues/10755">#10755</a>)</li>
<li>See full diff in <a
href="https://github.com/TanStack/query/commits/@tanstack/react-query-devtools@5.100.13/packages/react-query-devtools">compare
view</a></li>
</ul>
</details>
<br />

Updates `@types/react` from 19.2.14 to 19.2.15
<details>
<summary>Commits</summary>
<ul>
<li>See full diff in <a
href="https://github.com/DefinitelyTyped/DefinitelyTyped/commits/HEAD/types/react">compare
view</a></li>
</ul>
</details>
<br />

Updates `@vitest/coverage-v8` from 4.1.6 to 4.1.7
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/vitest-dev/vitest/releases">@​vitest/coverage-v8's
releases</a>.</em></p>
<blockquote>
<h2>v4.1.7</h2>
<h3>   🐞 Bug Fixes</h3>
<ul>
<li><strong>runner</strong>: Limit concurrency per task branch in
addition to per leaf callbacks (backport)  -  by <a
href="https://github.com/hi-ogawa"><code>@​hi-ogawa</code></a> in <a
href="https://redirect.github.com/vitest-dev/vitest/issues/10384">vitest-dev/vitest#10384</a>
<a href="https://github.com/vitest-dev/vitest/commit/4f0f2a1ee"><!-- raw
HTML omitted -->(4f0f2)<!-- raw HTML omitted --></a></li>
</ul>
<h5>    <a
href="https://github.com/vitest-dev/vitest/compare/v4.1.6...v4.1.7">View
changes on GitHub</a></h5>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/vitest-dev/vitest/commit/a09d47236e19fd3151351080c667036ca6164dc4"><code>a09d472</code></a>
chore: release v4.1.7</li>
<li>See full diff in <a
href="https://github.com/vitest-dev/vitest/commits/v4.1.7/packages/coverage-v8">compare
view</a></li>
</ul>
</details>
<br />

Updates `@vitest/expect` from 4.1.6 to 4.1.7
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/vitest-dev/vitest/releases">@​vitest/expect's
releases</a>.</em></p>
<blockquote>
<h2>v4.1.7</h2>
<h3>   🐞 Bug Fixes</h3>
<ul>
<li><strong>runner</strong>: Limit concurrency per task branch in
addition to per leaf callbacks (backport)  -  by <a
href="https://github.com/hi-ogawa"><code>@​hi-ogawa</code></a> in <a
href="https://redirect.github.com/vitest-dev/vitest/issues/10384">vitest-dev/vitest#10384</a>
<a href="https://github.com/vitest-dev/vitest/commit/4f0f2a1ee"><!-- raw
HTML omitted -->(4f0f2)<!-- raw HTML omitted --></a></li>
</ul>
<h5>    <a
href="https://github.com/vitest-dev/vitest/compare/v4.1.6...v4.1.7">View
changes on GitHub</a></h5>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/vitest-dev/vitest/commit/a09d47236e19fd3151351080c667036ca6164dc4"><code>a09d472</code></a>
chore: release v4.1.7</li>
<li>See full diff in <a
href="https://github.com/vitest-dev/vitest/commits/v4.1.7/packages/expect">compare
view</a></li>
</ul>
</details>
<br />

Updates `firebase` from 12.12.1 to 12.13.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/firebase/firebase-js-sdk/releases">firebase's
releases</a>.</em></p>
<blockquote>
<h2>firebase@12.13.0</h2>
<p>For more detailed release notes, see <a
href="https://firebase.google.com/support/release-notes/js">Firebase
JavaScript SDK Release Notes</a>.</p>
<h1>What's Changed</h1>
<h2><code>@​firebase/ai</code><a
href="https://github.com/2"><code>@​2</code></a>.12.0</h2>
<h3>Minor Changes</h3>
<ul>
<li>
<p><a
href="https://github.com/firebase/firebase-js-sdk/commit/ffa39f61c36e9d90a26573f042863e0086ee01e2"><code>ffa39f6</code></a>
<a
href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9795">#9795</a>
- Added <code>LiveSession.resumeSession()</code> to allow resuming a
previous <code>LiveSession</code>. Also added
<code>contextWindowCompression</code> feature.</p>
</li>
<li>
<p><a
href="https://github.com/firebase/firebase-js-sdk/commit/86dc0db9218d9ae52282d595007fc60b40c98b6e"><code>86dc0db</code></a>
<a
href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9819">#9819</a>
- Added support for <code>ImageConfig</code> (aspect ratio and size).
Expanded <code>FinishReason</code> values to include all currently
available values provided by the models.</p>
</li>
<li>
<p><a
href="https://github.com/firebase/firebase-js-sdk/commit/345c5f6235492b45e84034f364fd95280bd6e428"><code>345c5f6</code></a>
<a
href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9458">#9458</a>
- AI Logic : Feature : Added support for Grounding with Google Maps.</p>
</li>
</ul>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://github.com/firebase/firebase-js-sdk/commit/8e384c947de73c7f74346b1c01640f3515a4ef0e"><code>8e384c9</code></a>
<a
href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9883">#9883</a>
- Updated dependencies.</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/firebase/firebase-js-sdk/commit/8e384c947de73c7f74346b1c01640f3515a4ef0e"><code>8e384c9</code></a>]:</p>
</li>
<li>
<p><code>@​firebase/app-check-interop-types</code><a
href="https://github.com/0"><code>@​0</code></a>.3.4</p>
</li>
<li>
<p><code>@​firebase/component</code><a
href="https://github.com/0"><code>@​0</code></a>.7.3</p>
</li>
<li>
<p><code>@​firebase/logger</code><a
href="https://github.com/0"><code>@​0</code></a>.5.1</p>
</li>
<li>
<p><code>@​firebase/util</code><a
href="https://github.com/1"><code>@​1</code></a>.15.1</p>
</li>
</ul>
<h2><code>@​firebase/data-connect</code><a
href="https://github.com/0"><code>@​0</code></a>.7.0</h2>
<h3>Minor Changes</h3>
<ul>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/714b41dcc55339f94f904558ff190c5bdc9ac49f"><code>714b41d</code></a>
<a
href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9905">#9905</a>
- Hardened the Firebase SQL Connect streaming transport with intelligent
reconnection, query de-duplication, and resume optimizations.</li>
</ul>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a
href="https://github.com/firebase/firebase-js-sdk/commit/8e384c947de73c7f74346b1c01640f3515a4ef0e"><code>8e384c9</code></a>
<a
href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9883">#9883</a>
- Updated dependencies.</p>
</li>
<li>
<p>Updated dependencies [<a
href="https://github.com/firebase/firebase-js-sdk/commit/8e384c947de73c7f74346b1c01640f3515a4ef0e"><code>8e384c9</code></a>]:</p>
</li>
<li>
<p><code>@​firebase/auth-interop-types</code><a
href="https://github.com/0"><code>@​0</code></a>.2.5</p>
</li>
<li>
<p><code>@​firebase/component</code><a
href="https://github.com/0"><code>@​0</code></a>.7.3</p>
</li>
<li>
<p><code>@​firebase/logger</code><a
href="https://github.com/0"><code>@​0</code></a>.5.1</p>
</li>
<li>
<p><code>@​firebase/util</code><a
href="https://github.com/1"><code>@​1</code></a>.15.1</p>
</li>
</ul>
<h2>firebase@12.13.0</h2>
<h3>Minor Changes</h3>
<ul>
<li>
<p><a
href="https://github.com/firebase/firebase-js-sdk/commit/ffa39f61c36e9d90a26573f042863e0086ee01e2"><code>ffa39f6</code></a>
<a
href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9795">#9795</a>
- Added <code>LiveSession.resumeSession()</code> to allow resuming a
previous <code>LiveSession</code>. Also added
<code>contextWindowCompression</code> feature.</p>
</li>
<li>
<p><a
href="https://github.com/firebase/firebase-js-sdk/commit/714b41dcc55339f94f904558ff190c5bdc9ac49f"><code>714b41d</code></a>
<a
href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9905">#9905</a>
- Hardened the Firebase SQL Connect streaming transport with intelligent
reconnection, query de-duplication, and resume optimizations.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/1adfd640e779ee0d89e62404c6823ca9f5a80ec0"><code>1adfd64</code></a>
Version Packages (<a
href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9923">#9923</a>)</li>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/50d5b6a6c350189c2cf13fdd7324fe022860de28"><code>50d5b6a</code></a>
Merge main into release</li>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/714b41dcc55339f94f904558ff190c5bdc9ac49f"><code>714b41d</code></a>
feat(data-connect): add de-duplication, resume, and intelligent
reconnection ...</li>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/f80895f550dcb005b447504e3536e7fa231b3ae3"><code>f80895f</code></a>
Merge main into release</li>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/330a387df59fbe23b5c32bbd120f7c5dce138a14"><code>330a387</code></a>
chore: migrate test functions to v2 (<a
href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9910">#9910</a>)</li>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/3b8713433d96eb05ef7cab3a549f4d536cc1927e"><code>3b87134</code></a>
build(deps): bump axios from 1.13.5 to 1.15.2 (<a
href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9860">#9860</a>)</li>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/402b1f01e67441c51701153031b6e645b71d4875"><code>402b1f0</code></a>
fix(firestore): Assertion ID: ca9 (pendingResponses less than 0) caused
by ta...</li>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/86dc0db9218d9ae52282d595007fc60b40c98b6e"><code>86dc0db</code></a>
feat(ai): ImageConfig and FinishReasons (<a
href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9819">#9819</a>)</li>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/62ae2e203aa1720aa192967340f70f2872c8442e"><code>62ae2e2</code></a>
chore: Update picomatch and rollup-plugin-typescript2 (<a
href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9892">#9892</a>)</li>
<li><a
href="https://github.com/firebase/firebase-js-sdk/commit/96e81ffe9a6efd557685eea7db9d78e5594f43aa"><code>96e81ff</code></a>
feat(firestore): Added search stage support for languageCode, offset,
limit, ...</li>
<li>Additional commits viewable in <a
href="https://github.com/firebase/firebase-js-sdk/compare/firebase@12.12.1...firebase@12.13.0">compare
view</a></li>
</ul>
</details>
<br />

Updates `jscpd` from 4.2.2 to 4.2.3
<details>
<summary>Commits</summary>
<ul>
<li>See full diff in <a
href="https://github.com/kucherenko/jscpd/commits">compare view</a></li>
</ul>
</details>
<br />

Updates `knip` from 6.10.0 to 6.14.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a
href="https://github.com/webpro-nl/knip/releases">knip's
releases</a>.</em></p>
<blockquote>
<h2>Release 6.14.2</h2>
<ul>
<li>Fix vscode-knip build: pin native oxc bindings to bundled JS version
(1b45a4103312c9c059560ae2e1eac25d86b4e2ac)</li>
<li>Release vscode-knip@2.1.5
(328892eb04e65b4702e1ef2303db3156b8f2e1a3)</li>
<li>Fix Astro plugin to support both possible middleware entry points
(<a
href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1749">#1749</a>)
(33e0cc1a530a8cf5b6b05c8b3a3ca55f8fce8a75) - thanks <a
href="https://github.com/schmalz-dmi"><code>@​schmalz-dmi</code></a>!</li>
<li>Fix LICENSE link (<a
href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1760">#1760</a>)
(829620f9077ddea086a610c279c7c1250dd66e11) - thanks <a
href="https://github.com/vortispy"><code>@​vortispy</code></a>!</li>
<li>Fix GraphQL Codegen script config dependencies (<a
href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1756">#1756</a>)
(e841c6355e7eff240e74010bfd2be8bbb22ff2b6) - thanks <a
href="https://github.com/jakeleventhal"><code>@​jakeleventhal</code></a>!</li>
<li>Set pnpm config via env vars, disable verify-deps in ecosystem tests
(53c12248cc3e79fd79f3efde691d463fc795c40f)</li>
<li>Update slonik ecosystem snapshot
(f18410b34c8554364a9f003660bebae5e826de57)</li>
<li>Fix Serverless TypeScript plugin dependencies (<a
href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1757">#1757</a>)
(ebde7f8f3e3004db7f51fb5d60a0bdc2452116ef) - thanks <a
href="https://github.com/jakeleventhal"><code>@​jakeleventhal</code></a>!</li>
<li>Fix extended tsconfig type dependency attribution (<a
href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1758">#1758</a>)
(f600b09e562317a37844ed8cdf1b9b46e06c9405) - thanks <a
href="https://github.com/jakeleventhal"><code>@​jakeleventhal…
```

### PR Description

Bumps the minor-and-patch group with 20 updates in the /web directory:

| Package | From | To |
| --- | --- | --- |
| [@assistant-ui/react](https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react) | `0.12.28` | `0.14.7` |
| [@opennextjs/cloudflare](https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare) | `1.19.9` | `1.19.11` |
| [@tanstack/query-sync-storage-persister](https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister) | `5.100.11` | `5.100.13` |
| [@tanstack/react-query](https://github.com/TanStack/query/tree/HEAD/packages/react-query) | `5.100.11` | `5.100.13` |
| [@tanstack/react-query-persist-client](https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client) | `5.100.11` | `5.100.13` |
| [dompurify](https://github.com/cure53/DOMPurify) | `3.4.3` | `3.4.5` |
| [framer-motion](https://github.com/motiondivision/motion) | `12.38.0` | `12.40.0` |
| [marked](https://github.com/markedjs/marked) | `18.0.3` | `18.0.4` |
| [shiki](https://github.com/shikijs/shiki/tree/HEAD/packages/shiki) | `4.0.2` | `4.1.0` |
| [@tanstack/react-query-devtools](https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools) | `5.100.11` | `5.100.13` |
| [@types/react](https://github.com/DefinitelyTyped/DefinitelyTyped/tree/HEAD/types/react) | `19.2.14` | `19.2.15` |
| [@vitest/coverage-v8](https://github.com/vitest-dev/vitest/tree/HEAD/packages/coverage-v8) | `4.1.6` | `4.1.7` |
| [@vitest/expect](https://github.com/vitest-dev/vitest/tree/HEAD/packages/expect) | `4.1.6` | `4.1.7` |
| [firebase](https://github.com/firebase/firebase-js-sdk) | `12.12.1` | `12.13.0` |
| [jscpd](https://github.com/kucherenko/jscpd) | `4.2.2` | `4.2.3` |
| [knip](https://github.com/webpro-nl/knip/tree/HEAD/packages/knip) | `6.10.0` | `6.14.2` |
| [postcss](https://github.com/postcss/postcss) | `8.5.14` | `8.5.15` |
| [tsx](https://github.com/privatenumber/tsx) | `4.22.0` | `4.22.3` |
| [vitest](https://github.com/vitest-dev/vitest/tree/HEAD/packages/vitest) | `4.1.6` | `4.1.7` |
| [wrangler](https://github.com/cloudflare/workers-sdk/tree/HEAD/packages/wrangler) | `4.90.0` | `4.94.0` |


Updates `@assistant-ui/react` from 0.12.28 to 0.14.7
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/assistant-ui/assistant-ui/releases">@​assistant-ui/react's releases</a>.</em></p>
<blockquote>
<h2><code>@​assistant-ui/react</code><a href="https://github.com/0"><code>@​0</code></a>.14.7</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4073">#4073</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/44ac45910cf49960ea0910cce32167d726a03ed1"><code>44ac459</code></a> - fix(react|useSmooth): render-phase resync of displayed text on part change (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<p>Drop one frame of stale text after a thread switch by resyncing
<code>displayedText</code> in render when the part instance flips or <code>text</code>
breaks its streaming-append continuity, instead of waiting for
the post-commit effect.</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/assistant-ui/assistant-ui/commit/221d320cee987a4cd464c9cbae152d918197499e"><code>221d320</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.2.4</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react-langgraph</code><a href="https://github.com/0"><code>@​0</code></a>.14.1</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3925">#3925</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/53cdc51665a48dfeb0220455f6c32a34981e0b0e"><code>53cdc51</code></a> - feat(react-langgraph): track streaming timing via <code>useLangGraphStreamingTiming</code> so <code>useMessageTiming()</code> works on LangGraph assistant messages (<a href="https://github.com/shashank-100"><code>@​shashank-100</code></a>)</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/assistant-ui/assistant-ui/commit/845c7c12fecbb448da7f1135c33163b653a50710"><code>845c7c1</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/db721df32434296ac14eab27030628107975b71c"><code>db721df</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/179895fdcb56edee2e8d9efb4b38cd3859eeecdd"><code>179895f</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/3b2bbce1589b44a13b8b7a570c19bf35a2266fbd"><code>3b2bbce</code></a>]:</p>
<ul>
<li>assistant-cloud@0.1.28</li>
<li><code>@​assistant-ui/store</code><a href="https://github.com/0"><code>@​0</code></a>.2.11</li>
<li>assistant-stream@0.3.15</li>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.2.3</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react</code><a href="https://github.com/0"><code>@​0</code></a>.14.6</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4023">#4023</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a> - docs: add React JSDoc and deprecation notices for primitive and tool APIs (<a href="https://github.com/AVGVSTVS96"><code>@​AVGVSTVS96</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3513">#3513</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a> - fix: guard <code>navigator.clipboard</code> availability and swallow write rejections in <code>ActionBarPrimitive.Copy</code>. Previously, copy clicks in SSR, non-HTTPS contexts, or older browsers without the Clipboard API threw a <code>ReferenceError</code>, and permission-denied rejections surfaced as unhandled promise rejections. The web copyToClipboard implementation in <code>@assistant-ui/react</code> now early-rejects when the API is unavailable, and <code>useActionBarCopy</code> in <code>@assistant-ui/core</code> silently absorbs the rejection so the rest of the UI is unaffected. (<a href="https://github.com/JustAnOkapi"><code>@​JustAnOkapi</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4040">#4040</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/b481ec5129e6c1ae6de2683cdafdeecff1d8ed6b"><code>b481ec5</code></a> - fix: <code>useExternalStoreRuntime</code> no longer leaves phantom assistant siblings when the external store swaps a message id between syncs (e.g. AI SDK v6 <code>useChat</code> replacing a client-generated id with a server-provided id mid-stream, surfacing as <code>BranchPicker</code> showing <code>2/2</code> on a turn the user never branched). The <code>messages</code>-array sync path now diffs against the previous sync and removes ids that disappeared, matching the <code>messageRepository</code> path's snapshot semantics. Closes <a href="https://redirect.github.com/assistant-ui/assistant-ui/issues/4037">#4037</a>. (<a href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4063">#4063</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/8f0dbb80a0c89c7406bad1ad397e75831b9b8fa7"><code>8f0dbb8</code></a> - fix thread initialization timing race which caused <code>scrollToBottomOnInitialize</code> to fail in <code>useLocalRuntime</code> (<a href="https://github.com/AVGVSTVS96"><code>@​AVGVSTVS96</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3958">#3958</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a> - refactor: hoist <code>MessagePartPrimitiveInProgress</code> to <code>@assistant-ui/core/react</code> so <code>@assistant-ui/react</code>, <code>@assistant-ui/react-ink</code>, and other distributions can share the same implementation. <code>@assistant-ui/react</code>'s <code>MessagePartPrimitive.InProgress</code> is unchanged for callers; it now re-exports from core. (<a href="https://github.com/ShobhitPatra"><code>@​ShobhitPatra</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4050">#4050</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/693922b182b876b28d986f528b21d33da7c5bb51"><code>693922b</code></a> - fix(x-buildutils): include local <code>types/</code> in <code>typeRoots</code> so x-buildutils itself can resolve its ambient <code>browser-process</code> types (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<p>feat(react): re-export <code>Unstable_DirectiveFormatter</code>, <code>Unstable_DirectiveSegment</code>, <code>Unstable_TriggerItem</code>, and <code>unstable_defaultDirectiveFormatter</code> from <code>@assistant-ui/core</code> so downstream packages don't need to depend on <code>@assistant-ui/core</code> directly</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/assistant-ui/assistant-ui/commit/845c7c12fecbb448da7f1135c33163b653a50710"><code>845c7c1</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/db721df32434296ac14eab27030628107975b71c"><code>db721df</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/179895fdcb56edee2e8d9efb4b38cd3859eeecdd"><code>179895f</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/3b2bbce1589b44a13b8b7a570c19bf35a2266fbd"><code>3b2bbce</code></a>]:</p>
<ul>
<li>assistant-cloud@0.1.28</li>
<li><code>@​assistant-ui/store</code><a href="https://github.com/0"><code>@​0</code></a>.2.11</li>
<li>assistant-stream@0.3.15</li>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.2.3</li>
</ul>
</li>
</ul>
<h2><code>@​assistant-ui/react-langgraph</code><a href="https://github.com/0"><code>@​0</code></a>.14.0</h2>
<h3>Minor Changes</h3>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/assistant-ui/assistant-ui/blob/main/packages/react/CHANGELOG.md">@​assistant-ui/react's changelog</a>.</em></p>
<blockquote>
<h2>0.14.7</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4073">#4073</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/44ac45910cf49960ea0910cce32167d726a03ed1"><code>44ac459</code></a> - fix(react|useSmooth): render-phase resync of displayed text on part change (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<p>Drop one frame of stale text after a thread switch by resyncing
<code>displayedText</code> in render when the part instance flips or <code>text</code>
breaks its streaming-append continuity, instead of waiting for
the post-commit effect.</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/assistant-ui/assistant-ui/commit/221d320cee987a4cd464c9cbae152d918197499e"><code>221d320</code></a>]:</p>
<ul>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.2.4</li>
</ul>
</li>
</ul>
<h2>0.14.6</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4023">#4023</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a> - docs: add React JSDoc and deprecation notices for primitive and tool APIs (<a href="https://github.com/AVGVSTVS96"><code>@​AVGVSTVS96</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3513">#3513</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a> - fix: guard <code>navigator.clipboard</code> availability and swallow write rejections in <code>ActionBarPrimitive.Copy</code>. Previously, copy clicks in SSR, non-HTTPS contexts, or older browsers without the Clipboard API threw a <code>ReferenceError</code>, and permission-denied rejections surfaced as unhandled promise rejections. The web copyToClipboard implementation in <code>@assistant-ui/react</code> now early-rejects when the API is unavailable, and <code>useActionBarCopy</code> in <code>@assistant-ui/core</code> silently absorbs the rejection so the rest of the UI is unaffected. (<a href="https://github.com/JustAnOkapi"><code>@​JustAnOkapi</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4040">#4040</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/b481ec5129e6c1ae6de2683cdafdeecff1d8ed6b"><code>b481ec5</code></a> - fix: <code>useExternalStoreRuntime</code> no longer leaves phantom assistant siblings when the external store swaps a message id between syncs (e.g. AI SDK v6 <code>useChat</code> replacing a client-generated id with a server-provided id mid-stream, surfacing as <code>BranchPicker</code> showing <code>2/2</code> on a turn the user never branched). The <code>messages</code>-array sync path now diffs against the previous sync and removes ids that disappeared, matching the <code>messageRepository</code> path's snapshot semantics. Closes <a href="https://redirect.github.com/assistant-ui/assistant-ui/issues/4037">#4037</a>. (<a href="https://github.com/okisdev"><code>@​okisdev</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4063">#4063</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/8f0dbb80a0c89c7406bad1ad397e75831b9b8fa7"><code>8f0dbb8</code></a> - fix thread initialization timing race which caused <code>scrollToBottomOnInitialize</code> to fail in <code>useLocalRuntime</code> (<a href="https://github.com/AVGVSTVS96"><code>@​AVGVSTVS96</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/3958">#3958</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a> - refactor: hoist <code>MessagePartPrimitiveInProgress</code> to <code>@assistant-ui/core/react</code> so <code>@assistant-ui/react</code>, <code>@assistant-ui/react-ink</code>, and other distributions can share the same implementation. <code>@assistant-ui/react</code>'s <code>MessagePartPrimitive.InProgress</code> is unchanged for callers; it now re-exports from core. (<a href="https://github.com/ShobhitPatra"><code>@​ShobhitPatra</code></a>)</p>
</li>
<li>
<p><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4050">#4050</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/693922b182b876b28d986f528b21d33da7c5bb51"><code>693922b</code></a> - fix(x-buildutils): include local <code>types/</code> in <code>typeRoots</code> so x-buildutils itself can resolve its ambient <code>browser-process</code> types (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</p>
<p>feat(react): re-export <code>Unstable_DirectiveFormatter</code>, <code>Unstable_DirectiveSegment</code>, <code>Unstable_TriggerItem</code>, and <code>unstable_defaultDirectiveFormatter</code> from <code>@assistant-ui/core</code> so downstream packages don't need to depend on <code>@assistant-ui/core</code> directly</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/assistant-ui/assistant-ui/commit/845c7c12fecbb448da7f1135c33163b653a50710"><code>845c7c1</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/db721df32434296ac14eab27030628107975b71c"><code>db721df</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/179895fdcb56edee2e8d9efb4b38cd3859eeecdd"><code>179895f</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a>, <a href="https://github.com/assistant-ui/assistant-ui/commit/3b2bbce1589b44a13b8b7a570c19bf35a2266fbd"><code>3b2bbce</code></a>]:</p>
<ul>
<li>assistant-cloud@0.1.28</li>
<li><code>@​assistant-ui/store</code><a href="https://github.com/0"><code>@​0</code></a>.2.11</li>
<li>assistant-stream@0.3.15</li>
<li><code>@​assistant-ui/core</code><a href="https://github.com/0"><code>@​0</code></a>.2.3</li>
</ul>
</li>
</ul>
<h2>0.14.5</h2>
<h3>Patch Changes</h3>
<ul>
<li>Accept the MCP-UI <code>2026-01-26</code> method names in the MCP App bridge (e.g. <code>ui/notifications/size-changed</code>, <code>ui/request-display-mode</code>, <code>ui/open-link</code>, <code>ui/message</code>). Widgets built with the current xmcp host-bridge emit these names; previously the host silently ignored them, leaving features like auto-resize broken (iframe never received a height change from <code>onSizeChange</code>).</li>
</ul>
<h2>0.14.4</h2>
<h3>Patch Changes</h3>
<ul>
<li><a href="https://redirect.github.com/assistant-ui/assistant-ui/pull/4033">#4033</a> <a href="https://github.com/assistant-ui/assistant-ui/commit/552ffb0ed145f2e2a57db910b99dac5d5b834626"><code>552ffb0</code></a> - feat(react): export <code>getMcpAppFromToolPart</code> so hosts can detect MCP-app tool parts (<a href="https://github.com/Yonom"><code>@​Yonom</code></a>)</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/a5c3b5433d002c6bd9db46d9416549a7c3728706"><code>a5c3b54</code></a> chore: update versions (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4074">#4074</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/44ac45910cf49960ea0910cce32167d726a03ed1"><code>44ac459</code></a> fix(react): resync useSmooth displayedText on part change (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4073">#4073</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/e926633f806954e07fc289c9fb12e5032ed8ff9d"><code>e926633</code></a> chore: update versions (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4034">#4034</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/8f0dbb80a0c89c7406bad1ad397e75831b9b8fa7"><code>8f0dbb8</code></a> fix(react): thread initialization timing race (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4063">#4063</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/179895fdcb56edee2e8d9efb4b38cd3859eeecdd"><code>179895f</code></a> fix(core): fire streamCall for already-resolved tool calls observed live (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4057">#4057</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/8b6fc8836871e62efc2fd8c131c6783e12c5fc47"><code>8b6fc88</code></a> fix: guard clipboard availability before calling writeText (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3513">#3513</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/7a8bf26eda76f5f8490f96b3ff9dce1ccd072917"><code>7a8bf26</code></a> feat(react-ink): add message part primitives (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/3958">#3958</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/693922b182b876b28d986f528b21d33da7c5bb51"><code>693922b</code></a> fix(tsconfig): TS 6.0 deprecation prep + latent dep fixes (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4050">#4050</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/612396167e28eb2500c58956038a95b6cad36624"><code>6123961</code></a> chore: update model names throughout monorepo (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4043">#4043</a>)</li>
<li><a href="https://github.com/assistant-ui/assistant-ui/commit/94548fa8d587962d8ab0338a9609a9ff21240c33"><code>94548fa</code></a> docs: expand public API JSDoc and message part deprecations (<a href="https://github.com/assistant-ui/assistant-ui/tree/HEAD/packages/react/issues/4023">#4023</a>)</li>
<li>Additional commits viewable in <a href="https://github.com/assistant-ui/assistant-ui/commits/@assistant-ui/react@0.14.7/packages/react">compare view</a></li>
</ul>
</details>
<br />

Updates `@opennextjs/cloudflare` from 1.19.9 to 1.19.11
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/opennextjs/opennextjs-cloudflare/releases">@​opennextjs/cloudflare's releases</a>.</em></p>
<blockquote>
<h2><code>@​opennextjs/cloudflare</code><a href="https://github.com/1"><code>@​1</code></a>.19.11</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1270">#1270</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/802047e7fd30c5533d5b4f754f281bc7a3fd4720"><code>802047e</code></a> Thanks <a href="https://github.com/alex-all3dp"><code>@​alex-all3dp</code></a>! - fix: skip non-upload-triggered worker versions when building skew-protection deployment mapping</p>
<p>Worker versions created by metadata-only operations (e.g. Cloudflare API secret updates) do not include the static assets bundle. Previously, such versions could become the &quot;latest&quot; target in the skew-protection mapping, causing <code>/_next/static/*</code> requests to return 404 on past deployments. Versions are now filtered to those with <code>workers/triggered_by</code> in <code>{upload, version_upload}</code>.</p>
<p>Closes <a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1230">#1230</a></p>
</li>
</ul>
<h2><code>@​opennextjs/cloudflare</code><a href="https://github.com/1"><code>@​1</code></a>.19.10</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1261">#1261</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/780dd4f09c2090f1d955c90b6ddd1d6b25920850"><code>780dd4f</code></a> Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! - Allow populating R2 when the domain is protected by Cloudflare Access</p>
<p>You need to:</p>
<ul>
<li>create a &quot;Service Auth&quot; policy for &quot;open-next-cache-populate.<!-- raw HTML omitted -->.workers.dev&quot;</li>
<li>add an &quot;Include&quot; rule for &quot;Any Access Service Token&quot; or for a given service token (&quot;Service Token&quot;)</li>
<li>populate the env variables CLOUDFLARE_ACCESS_CLIENT_ID and CLOUDFLARE_ACCESS_CLIENT_SECRET</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/opennextjs/opennextjs-cloudflare/blob/main/packages/cloudflare/CHANGELOG.md">@​opennextjs/cloudflare's changelog</a>.</em></p>
<blockquote>
<h2>1.19.11</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1270">#1270</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/802047e7fd30c5533d5b4f754f281bc7a3fd4720"><code>802047e</code></a> Thanks <a href="https://github.com/alex-all3dp"><code>@​alex-all3dp</code></a>! - fix: skip non-upload-triggered worker versions when building skew-protection deployment mapping</p>
<p>Worker versions created by metadata-only operations (e.g. Cloudflare API secret updates) do not include the static assets bundle. Previously, such versions could become the &quot;latest&quot; target in the skew-protection mapping, causing <code>/_next/static/*</code> requests to return 404 on past deployments. Versions are now filtered to those with <code>workers/triggered_by</code> in <code>{upload, version_upload}</code>.</p>
<p>Closes <a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1230">#1230</a></p>
</li>
</ul>
<h2>1.19.10</h2>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://redirect.github.com/opennextjs/opennextjs-cloudflare/pull/1261">#1261</a> <a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/780dd4f09c2090f1d955c90b6ddd1d6b25920850"><code>780dd4f</code></a> Thanks <a href="https://github.com/vicb"><code>@​vicb</code></a>! - Allow populating R2 when the domain is protected by Cloudflare Access</p>
<p>You need to:</p>
<ul>
<li>create a &quot;Service Auth&quot; policy for &quot;open-next-cache-populate.<!-- raw HTML omitted -->.workers.dev&quot;</li>
<li>add an &quot;Include&quot; rule for &quot;Any Access Service Token&quot; or for a given service token (&quot;Service Token&quot;)</li>
<li>populate the env variables CLOUDFLARE_ACCESS_CLIENT_ID and CLOUDFLARE_ACCESS_CLIENT_SECRET</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/596f924597bd6739009004f099e975997b62240a"><code>596f924</code></a> Version Packages (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1271">#1271</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/802047e7fd30c5533d5b4f754f281bc7a3fd4720"><code>802047e</code></a> fix: skip non-upload-triggered worker versions in skew-protection (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1270">#1270</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/dd78941f97683dcb38ca5f2b275624c575bcec4c"><code>dd78941</code></a> docs: clarify Cloudflare Access setup in populate-cache comment (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1267">#1267</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/49eade5577d7f31d1753f95f68a448b48bb93dd7"><code>49eade5</code></a> Version Packages (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1266">#1266</a>)</li>
<li><a href="https://github.com/opennextjs/opennextjs-cloudflare/commit/780dd4f09c2090f1d955c90b6ddd1d6b25920850"><code>780dd4f</code></a> Allow populating R2 when the domain is protected by Cloudflare Access (<a href="https://github.com/opennextjs/opennextjs-cloudflare/tree/HEAD/packages/cloudflare/issues/1261">#1261</a>)</li>
<li>See full diff in <a href="https://github.com/opennextjs/opennextjs-cloudflare/commits/@opennextjs/cloudflare@1.19.11/packages/cloudflare">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/query-sync-storage-persister` from 5.100.11 to 5.100.13
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases">@​tanstack/query-sync-storage-persister's releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/query-sync-storage-persister</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/query-sync-storage-persister</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/query-sync-storage-persister/CHANGELOG.md">@​tanstack/query-sync-storage-persister's changelog</a>.</em></p>
<blockquote>
<h2>5.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2>5.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/05cf2bc0a4eae64959dc8a40152e2878190c971b"><code>05cf2bc</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister/issues/10758">#10758</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/5ff4f6936bb66a64267eb4413430f956eecf7248"><code>5ff4f69</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/query-sync-storage-persister/issues/10755">#10755</a>)</li>
<li>See full diff in <a href="https://github.com/TanStack/query/commits/@tanstack/query-sync-storage-persister@5.100.13/packages/query-sync-storage-persister">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query` from 5.100.11 to 5.100.13
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases">@​tanstack/react-query's releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-next-experimental</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/react-query/CHANGELOG.md">@​tanstack/react-query's changelog</a>.</em></p>
<blockquote>
<h2>5.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies [<a href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a>]:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2>5.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/05cf2bc0a4eae64959dc8a40152e2878190c971b"><code>05cf2bc</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10758">#10758</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/d423168f6261a5cb3d353e53b27c8150cc271151"><code>d423168</code></a> fix(query-core): use built-in NoInfer for generic indexed-access types (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10593">#10593</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/5ff4f6936bb66a64267eb4413430f956eecf7248"><code>5ff4f69</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query/issues/10755">#10755</a>)</li>
<li>See full diff in <a href="https://github.com/TanStack/query/commits/@tanstack/react-query@5.100.13/packages/react-query">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query-persist-client` from 5.100.11 to 5.100.13
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases">@​tanstack/react-query-persist-client's releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-persist-client</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/react-query-persist-client/CHANGELOG.md">@​tanstack/react-query-persist-client's changelog</a>.</em></p>
<blockquote>
<h2>5.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2>5.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-persist-client-core</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/05cf2bc0a4eae64959dc8a40152e2878190c971b"><code>05cf2bc</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client/issues/10758">#10758</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/5ff4f6936bb66a64267eb4413430f956eecf7248"><code>5ff4f69</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-persist-client/issues/10755">#10755</a>)</li>
<li>See full diff in <a href="https://github.com/TanStack/query/commits/@tanstack/react-query-persist-client@5.100.13/packages/react-query-persist-client">compare view</a></li>
</ul>
</details>
<br />

Updates `dompurify` from 3.4.3 to 3.4.5
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/cure53/DOMPurify/releases">dompurify's releases</a>.</em></p>
<blockquote>
<h2>DOMPurify 3.4.5</h2>
<ul>
<li>Fixed a bypass caused by the new HTML element <code>selectedcontent</code> added in 3.4.4, thanks <a href="https://github.com/KabirAcharya"><code>@​KabirAcharya</code></a></li>
</ul>
<p><strong>Note that this is a security release for an issue introduced in 3.4.4 and should be upgraded to immediately.</strong></p>
<h2>DOMPurify 3.4.4</h2>
<ul>
<li>Added the <code>selectedcontent</code> element to default allow-list, thanks <a href="https://github.com/lukewarlow"><code>@​lukewarlow</code></a></li>
<li>Added the <code>command</code> and <code>commandfor</code> attributes to default allowed-list, thanks <a href="https://github.com/lukewarlow"><code>@​lukewarlow</code></a></li>
<li>Added better template scrubbing for <code>IN_PLACE</code> operations, thanks <a href="https://github.com/DEMON1A"><code>@​DEMON1A</code></a></li>
<li>Added stronger checks for cross-realm windows, thanks <a href="https://github.com/DEMON1A"><code>@​DEMON1A</code></a> &amp; <a href="https://github.com/fg0x0"><code>@​fg0x0</code></a></li>
<li>Updated demo website and made sure it uses the latest from main</li>
<li>Updated existing workflows, fuzzer, dependabot, etc., added more tests</li>
<li>Bumped several dependencies where possible</li>
</ul>
<p>🚨 <strong>This release had been flagged as deprecated, please use DOMPurify 3.4.5 instead</strong> 🚨</p>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/cure53/DOMPurify/commit/011b0c78f2a0f57ee54f5fcccb697a46ca6e63ea"><code>011b0c7</code></a> release: 3.4.5 (<a href="https://redirect.github.com/cure53/DOMPurify/issues/1382">#1382</a>)</li>
<li><a href="https://github.com/cure53/DOMPurify/commit/5817ad969c15e67dfcd6cb37248d6e9c1553e7c3"><code>5817ad9</code></a> release: 3.4.4 (<a href="https://redirect.github.com/cure53/DOMPurify/issues/1374">#1374</a>)</li>
<li>See full diff in <a href="https://github.com/cure53/DOMPurify/compare/3.4.3...3.4.5">compare view</a></li>
</ul>
</details>
<br />

Updates `framer-motion` from 12.38.0 to 12.40.0
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/motiondivision/motion/blob/main/CHANGELOG.md">framer-motion's changelog</a>.</em></p>
<blockquote>
<h2>[12.40.0] 2026-05-21</h2>
<h3>Added</h3>
<ul>
<li><code>path</code> option to <code>transition</code>.</li>
<li><code>arc()</code> for motion along an arc.</li>
</ul>
<h2>[12.39.0] 2026-05-18</h2>
<h3>Added</h3>
<ul>
<li>Support for <code>repeatType</code> and <code>repeatDelay</code> in animation sequences.</li>
</ul>
<h3>Fixed</h3>
<ul>
<li>Variants: Re-run keyframe animations when switching between variant labels even when they share identical keyframe arrays.</li>
<li>Drag: Preserve in-flight motion value animations across React 19 reorder unmount/remount so <code>dragSnapToOrigin</code> no longer leaves the drag transform stranded after a layout swap.</li>
<li><code>LazyMotion</code>: Share React contexts between the <code>framer-motion</code> and <code>framer-motion/m</code> (and therefore <code>motion/react</code> and <code>motion/react-m</code>) CJS bundles so that <code>&lt;m.div&gt;</code> from the <code>/m</code> subpath picks up features loaded by <code>&lt;LazyMotion&gt;</code> from the main entry point.</li>
<li><code>useScroll</code>: Support hydrating <code>target</code> and <code>container</code> refs from anywhere in the tree.</li>
<li>Drag: Gesture no longer starts from incorrect start point when rendered inside <code>&lt;AnimatePresence initial={false} /&gt;</code>.</li>
<li>Drag: <code>dragConstraints</code>, when set as viewport-relative ref, no longer break on scroll.§</li>
<li>Updated <code>visualElement</code> hydration order.</li>
<li><code>useAnimate</code>: Now respects <code>skipAnimations</code>.</li>
<li><code>AnimatePresence</code>: Fix object-form <code>initial</code> values not applied on re-entry after exit completes.</li>
<li><code>scroll</code>: Fixed callback progress when tracking an element.</li>
<li><code>useScroll</code>: Fix hardware acceleration when tracking an element.</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/motiondivision/motion/commit/38ebb9480e5b25a51e09e2ec866c101d01d82c60"><code>38ebb94</code></a> v12.40.0</li>
<li><a href="https://github.com/motiondivision/motion/commit/b1f766c7221cfdbf868e2f66675d6d2e2ff8f50e"><code>b1f766c</code></a> Latest</li>
<li><a href="https://github.com/motiondivision/motion/commit/bca554401519e8ef45db1dcc8c52580998251c73"><code>bca5544</code></a> Merge pull request <a href="https://redirect.github.com/motiondivision/motion/issues/3699">#3699</a> from motiondivision/lochie/arcs-injectable</li>
<li><a href="https://github.com/motiondivision/motion/commit/f1a96cfaff8de87712539bf250205134c8e121d9"><code>f1a96cf</code></a> arc(): rename amp/rotate, expose MotionPath, fix explicit cw/ccw</li>
<li><a href="https://github.com/motiondivision/motion/commit/b4aaba0d161cce6db7b2070ec3fd141e1dbcda95"><code>b4aaba0</code></a> pathRotation: non-destructive orientToPath rotation channel</li>
<li><a href="https://github.com/motiondivision/motion/commit/8604ef3d9048127d61a8bbd94698e56368e70926"><code>8604ef3</code></a> Make arcs injectable via <code>transition.path = arc()</code></li>
<li><a href="https://github.com/motiondivision/motion/commit/f90fe294c559c3bd7b13e762b0b2aefe837dc000"><code>f90fe29</code></a> add <code>orientToPath</code></li>
<li><a href="https://github.com/motiondivision/motion/commit/9ebe999fe93e6431ce026a998cb2aeabe690d03b"><code>9ebe999</code></a> fix: test</li>
<li><a href="https://github.com/motiondivision/motion/commit/bc2107e8963b35c0f264810d8dcb8b7b96ac7cb5"><code>bc2107e</code></a> Revert &quot;no should&quot;</li>
<li><a href="https://github.com/motiondivision/motion/commit/6eeb92dc2228419a1d2ba33bec5df36c3357683a"><code>6eeb92d</code></a> no should</li>
<li>Additional commits viewable in <a href="https://github.com/motiondivision/motion/compare/v12.38.0...v12.40.0">compare view</a></li>
</ul>
</details>
<br />

Updates `marked` from 18.0.3 to 18.0.4
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/markedjs/marked/releases">marked's releases</a>.</em></p>
<blockquote>
<h2>v18.0.4</h2>
<h2><a href="https://github.com/markedjs/marked/compare/v18.0.3...v18.0.4">18.0.4</a> (2026-05-19)</h2>
<h3>Bug Fixes</h3>
<ul>
<li>cache list indentation regexes (<a href="https://redirect.github.com/markedjs/marked/issues/3969">#3969</a>) (<a href="https://github.com/markedjs/marked/commit/a37983f188d697fe98d350554dc95c49eaac6edd">a37983f</a>)</li>
<li>fix cli not reading stdin (<a href="https://redirect.github.com/markedjs/marked/issues/3967">#3967</a>) (<a href="https://github.com/markedjs/marked/commit/11adb697eeee2b0fa6da3a38d5146626347592dc">11adb69</a>)</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/markedjs/marked/commit/0a2cd54cbe91911890e4460ae4fd7b9966e05654"><code>0a2cd54</code></a> chore(release): 18.0.4 [skip ci]</li>
<li><a href="https://github.com/markedjs/marked/commit/11adb697eeee2b0fa6da3a38d5146626347592dc"><code>11adb69</code></a> fix: fix cli not reading stdin (<a href="https://redirect.github.com/markedjs/marked/issues/3967">#3967</a>)</li>
<li><a href="https://github.com/markedjs/marked/commit/a37983f188d697fe98d350554dc95c49eaac6edd"><code>a37983f</code></a> fix: cache list indentation regexes (<a href="https://redirect.github.com/markedjs/marked/issues/3969">#3969</a>)</li>
<li><a href="https://github.com/markedjs/marked/commit/d38b8c27e75a0d64fa2ff233a81a8b976210f1f1"><code>d38b8c2</code></a> chore(deps-dev): bump eslint from 10.3.0 to 10.4.0 (<a href="https://redirect.github.com/markedjs/marked/issues/3976">#3976</a>)</li>
<li><a href="https://github.com/markedjs/marked/commit/7d9b17e8cd13af580fa404d114401043b5510344"><code>7d9b17e</code></a> chore(docs): fix typo in package links (<a href="https://redirect.github.com/markedjs/marked/issues/3975">#3975</a>)</li>
<li><a href="https://github.com/markedjs/marked/commit/a7affc3b8ba7fc99481b6582ab5baa860228ec86"><code>a7affc3</code></a> chore(deps-dev): bump <code>@​semantic-release/release-notes-generator</code> from 14.1.0 t...</li>
<li><a href="https://github.com/markedjs/marked/commit/47d6ba1898437d913affd87180e157e47bf5c101"><code>47d6ba1</code></a> chore(deps-dev): bump <code>@​semantic-release/github</code> from 12.0.6 to 12.0.8 (<a href="https://redirect.github.com/markedjs/marked/issues/3972">#3972</a>)</li>
<li><a href="https://github.com/markedjs/marked/commit/69257e455e599e9c9ddedcaf913569279b12c20c"><code>69257e4</code></a> chore(deps-dev): bump eslint from 10.2.1 to 10.3.0 (<a href="https://redirect.github.com/markedjs/marked/issues/3966">#3966</a>)</li>
<li><a href="https://github.com/markedjs/marked/commit/1731d387f76ac98601a83504b217c2d7f5643898"><code>1731d38</code></a> refactor(test): move task list output coverage to specs (<a href="https://redirect.github.com/markedjs/marked/issues/3963">#3963</a>)</li>
<li>See full diff in <a href="https://github.com/markedjs/marked/compare/v18.0.3...v18.0.4">compare view</a></li>
</ul>
</details>
<br />

Updates `shiki` from 4.0.2 to 4.1.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/shikijs/shiki/releases">shiki's releases</a>.</em></p>
<blockquote>
<h2>v4.1.0</h2>
<h3>   🐞 Bug Fixes</h3>
<ul>
<li><strong>twoslash</strong>: Forward <code>tsModule</code> to <code>createTwoslasher</code>  -  by <a href="https://github.com/arthurfiorette"><code>@​arthurfiorette</code></a> in <a href="https://redirect.github.com/shikijs/shiki/issues/1271">shikijs/shiki#1271</a> <a href="https://github.com/shikijs/shiki/commit/be89afcf"><!-- raw HTML omitted -->(be89a)<!-- raw HTML omitted --></a></li>
</ul>
<h5>    <a href="https://github.com/shikijs/shiki/compare/v4.0.2...v4.1.0">View changes on GitHub</a></h5>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/shikijs/shiki/commit/c809af96f1907877c5cebfeee98ac5d55193140b"><code>c809af9</code></a> chore: release v4.1.0</li>
<li><a href="https://github.com/shikijs/shiki/commit/95371cb1b3c00ced5b437a11f603939002f9ecae"><code>95371cb</code></a> chore: lint</li>
<li>See full diff in <a href="https://github.com/shikijs/shiki/commits/v4.1.0/packages/shiki">compare view</a></li>
</ul>
</details>
<br />

Updates `@tanstack/react-query-devtools` from 5.100.11 to 5.100.13
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/releases">@​tanstack/react-query-devtools's releases</a>.</em></p>
<blockquote>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2><code>@​tanstack/react-query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Changelog</summary>
<p><em>Sourced from <a href="https://github.com/TanStack/query/blob/main/packages/react-query-devtools/CHANGELOG.md">@​tanstack/react-query-devtools's changelog</a>.</em></p>
<blockquote>
<h2>5.100.13</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.13</li>
</ul>
</li>
</ul>
<h2>5.100.12</h2>
<h3>Patch Changes</h3>
<ul>
<li>Updated dependencies []:
<ul>
<li><code>@​tanstack/query-devtools</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
<li><code>@​tanstack/react-query</code><a href="https://github.com/5"><code>@​5</code></a>.100.12</li>
</ul>
</li>
</ul>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/TanStack/query/commit/05cf2bc0a4eae64959dc8a40152e2878190c971b"><code>05cf2bc</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools/issues/10758">#10758</a>)</li>
<li><a href="https://github.com/TanStack/query/commit/5ff4f6936bb66a64267eb4413430f956eecf7248"><code>5ff4f69</code></a> ci: Version Packages (<a href="https://github.com/TanStack/query/tree/HEAD/packages/react-query-devtools/issues/10755">#10755</a>)</li>
<li>See full diff in <a href="https://github.com/TanStack/query/commits/@tanstack/react-query-devtools@5.100.13/packages/react-query-devtools">compare view</a></li>
</ul>
</details>
<br />

Updates `@types/react` from 19.2.14 to 19.2.15
<details>
<summary>Commits</summary>
<ul>
<li>See full diff in <a href="https://github.com/DefinitelyTyped/DefinitelyTyped/commits/HEAD/types/react">compare view</a></li>
</ul>
</details>
<br />

Updates `@vitest/coverage-v8` from 4.1.6 to 4.1.7
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/vitest-dev/vitest/releases">@​vitest/coverage-v8's releases</a>.</em></p>
<blockquote>
<h2>v4.1.7</h2>
<h3>   🐞 Bug Fixes</h3>
<ul>
<li><strong>runner</strong>: Limit concurrency per task branch in addition to per leaf callbacks (backport)  -  by <a href="https://github.com/hi-ogawa"><code>@​hi-ogawa</code></a> in <a href="https://redirect.github.com/vitest-dev/vitest/issues/10384">vitest-dev/vitest#10384</a> <a href="https://github.com/vitest-dev/vitest/commit/4f0f2a1ee"><!-- raw HTML omitted -->(4f0f2)<!-- raw HTML omitted --></a></li>
</ul>
<h5>    <a href="https://github.com/vitest-dev/vitest/compare/v4.1.6...v4.1.7">View changes on GitHub</a></h5>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/vitest-dev/vitest/commit/a09d47236e19fd3151351080c667036ca6164dc4"><code>a09d472</code></a> chore: release v4.1.7</li>
<li>See full diff in <a href="https://github.com/vitest-dev/vitest/commits/v4.1.7/packages/coverage-v8">compare view</a></li>
</ul>
</details>
<br />

Updates `@vitest/expect` from 4.1.6 to 4.1.7
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/vitest-dev/vitest/releases">@​vitest/expect's releases</a>.</em></p>
<blockquote>
<h2>v4.1.7</h2>
<h3>   🐞 Bug Fixes</h3>
<ul>
<li><strong>runner</strong>: Limit concurrency per task branch in addition to per leaf callbacks (backport)  -  by <a href="https://github.com/hi-ogawa"><code>@​hi-ogawa</code></a> in <a href="https://redirect.github.com/vitest-dev/vitest/issues/10384">vitest-dev/vitest#10384</a> <a href="https://github.com/vitest-dev/vitest/commit/4f0f2a1ee"><!-- raw HTML omitted -->(4f0f2)<!-- raw HTML omitted --></a></li>
</ul>
<h5>    <a href="https://github.com/vitest-dev/vitest/compare/v4.1.6...v4.1.7">View changes on GitHub</a></h5>
</blockquote>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/vitest-dev/vitest/commit/a09d47236e19fd3151351080c667036ca6164dc4"><code>a09d472</code></a> chore: release v4.1.7</li>
<li>See full diff in <a href="https://github.com/vitest-dev/vitest/commits/v4.1.7/packages/expect">compare view</a></li>
</ul>
</details>
<br />

Updates `firebase` from 12.12.1 to 12.13.0
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/firebase/firebase-js-sdk/releases">firebase's releases</a>.</em></p>
<blockquote>
<h2>firebase@12.13.0</h2>
<p>For more detailed release notes, see <a href="https://firebase.google.com/support/release-notes/js">Firebase JavaScript SDK Release Notes</a>.</p>
<h1>What's Changed</h1>
<h2><code>@​firebase/ai</code><a href="https://github.com/2"><code>@​2</code></a>.12.0</h2>
<h3>Minor Changes</h3>
<ul>
<li>
<p><a href="https://github.com/firebase/firebase-js-sdk/commit/ffa39f61c36e9d90a26573f042863e0086ee01e2"><code>ffa39f6</code></a> <a href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9795">#9795</a> - Added <code>LiveSession.resumeSession()</code> to allow resuming a previous <code>LiveSession</code>. Also added <code>contextWindowCompression</code> feature.</p>
</li>
<li>
<p><a href="https://github.com/firebase/firebase-js-sdk/commit/86dc0db9218d9ae52282d595007fc60b40c98b6e"><code>86dc0db</code></a> <a href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9819">#9819</a> - Added support for <code>ImageConfig</code> (aspect ratio and size).
Expanded <code>FinishReason</code> values to include all currently available values provided by the models.</p>
</li>
<li>
<p><a href="https://github.com/firebase/firebase-js-sdk/commit/345c5f6235492b45e84034f364fd95280bd6e428"><code>345c5f6</code></a> <a href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9458">#9458</a> - AI Logic : Feature : Added support for Grounding with Google Maps.</p>
</li>
</ul>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://github.com/firebase/firebase-js-sdk/commit/8e384c947de73c7f74346b1c01640f3515a4ef0e"><code>8e384c9</code></a> <a href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9883">#9883</a> - Updated dependencies.</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/firebase/firebase-js-sdk/commit/8e384c947de73c7f74346b1c01640f3515a4ef0e"><code>8e384c9</code></a>]:</p>
</li>
<li>
<p><code>@​firebase/app-check-interop-types</code><a href="https://github.com/0"><code>@​0</code></a>.3.4</p>
</li>
<li>
<p><code>@​firebase/component</code><a href="https://github.com/0"><code>@​0</code></a>.7.3</p>
</li>
<li>
<p><code>@​firebase/logger</code><a href="https://github.com/0"><code>@​0</code></a>.5.1</p>
</li>
<li>
<p><code>@​firebase/util</code><a href="https://github.com/1"><code>@​1</code></a>.15.1</p>
</li>
</ul>
<h2><code>@​firebase/data-connect</code><a href="https://github.com/0"><code>@​0</code></a>.7.0</h2>
<h3>Minor Changes</h3>
<ul>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/714b41dcc55339f94f904558ff190c5bdc9ac49f"><code>714b41d</code></a> <a href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9905">#9905</a> - Hardened the Firebase SQL Connect streaming transport with intelligent reconnection, query de-duplication, and resume optimizations.</li>
</ul>
<h3>Patch Changes</h3>
<ul>
<li>
<p><a href="https://github.com/firebase/firebase-js-sdk/commit/8e384c947de73c7f74346b1c01640f3515a4ef0e"><code>8e384c9</code></a> <a href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9883">#9883</a> - Updated dependencies.</p>
</li>
<li>
<p>Updated dependencies [<a href="https://github.com/firebase/firebase-js-sdk/commit/8e384c947de73c7f74346b1c01640f3515a4ef0e"><code>8e384c9</code></a>]:</p>
</li>
<li>
<p><code>@​firebase/auth-interop-types</code><a href="https://github.com/0"><code>@​0</code></a>.2.5</p>
</li>
<li>
<p><code>@​firebase/component</code><a href="https://github.com/0"><code>@​0</code></a>.7.3</p>
</li>
<li>
<p><code>@​firebase/logger</code><a href="https://github.com/0"><code>@​0</code></a>.5.1</p>
</li>
<li>
<p><code>@​firebase/util</code><a href="https://github.com/1"><code>@​1</code></a>.15.1</p>
</li>
</ul>
<h2>firebase@12.13.0</h2>
<h3>Minor Changes</h3>
<ul>
<li>
<p><a href="https://github.com/firebase/firebase-js-sdk/commit/ffa39f61c36e9d90a26573f042863e0086ee01e2"><code>ffa39f6</code></a> <a href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9795">#9795</a> - Added <code>LiveSession.resumeSession()</code> to allow resuming a previous <code>LiveSession</code>. Also added <code>contextWindowCompression</code> feature.</p>
</li>
<li>
<p><a href="https://github.com/firebase/firebase-js-sdk/commit/714b41dcc55339f94f904558ff190c5bdc9ac49f"><code>714b41d</code></a> <a href="https://redirect.github.com/firebase/firebase-js-sdk/pull/9905">#9905</a> - Hardened the Firebase SQL Connect streaming transport with intelligent reconnection, query de-duplication, and resume optimizations.</p>
</li>
</ul>
<!-- raw HTML omitted -->
</blockquote>
<p>... (truncated)</p>
</details>
<details>
<summary>Commits</summary>
<ul>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/1adfd640e779ee0d89e62404c6823ca9f5a80ec0"><code>1adfd64</code></a> Version Packages (<a href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9923">#9923</a>)</li>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/50d5b6a6c350189c2cf13fdd7324fe022860de28"><code>50d5b6a</code></a> Merge main into release</li>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/714b41dcc55339f94f904558ff190c5bdc9ac49f"><code>714b41d</code></a> feat(data-connect): add de-duplication, resume, and intelligent reconnection ...</li>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/f80895f550dcb005b447504e3536e7fa231b3ae3"><code>f80895f</code></a> Merge main into release</li>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/330a387df59fbe23b5c32bbd120f7c5dce138a14"><code>330a387</code></a> chore: migrate test functions to v2 (<a href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9910">#9910</a>)</li>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/3b8713433d96eb05ef7cab3a549f4d536cc1927e"><code>3b87134</code></a> build(deps): bump axios from 1.13.5 to 1.15.2 (<a href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9860">#9860</a>)</li>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/402b1f01e67441c51701153031b6e645b71d4875"><code>402b1f0</code></a> fix(firestore): Assertion ID: ca9 (pendingResponses less than 0) caused by ta...</li>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/86dc0db9218d9ae52282d595007fc60b40c98b6e"><code>86dc0db</code></a> feat(ai): ImageConfig and FinishReasons (<a href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9819">#9819</a>)</li>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/62ae2e203aa1720aa192967340f70f2872c8442e"><code>62ae2e2</code></a> chore: Update picomatch and rollup-plugin-typescript2 (<a href="https://redirect.github.com/firebase/firebase-js-sdk/issues/9892">#9892</a>)</li>
<li><a href="https://github.com/firebase/firebase-js-sdk/commit/96e81ffe9a6efd557685eea7db9d78e5594f43aa"><code>96e81ff</code></a> feat(firestore): Added search stage support for languageCode, offset, limit, ...</li>
<li>Additional commits viewable in <a href="https://github.com/firebase/firebase-js-sdk/compare/firebase@12.12.1...firebase@12.13.0">compare view</a></li>
</ul>
</details>
<br />

Updates `jscpd` from 4.2.2 to 4.2.3
<details>
<summary>Commits</summary>
<ul>
<li>See full diff in <a href="https://github.com/kucherenko/jscpd/commits">compare view</a></li>
</ul>
</details>
<br />

Updates `knip` from 6.10.0 to 6.14.2
<details>
<summary>Release notes</summary>
<p><em>Sourced from <a href="https://github.com/webpro-nl/knip/releases">knip's releases</a>.</em></p>
<blockquote>
<h2>Release 6.14.2</h2>
<ul>
<li>Fix vscode-knip build: pin native oxc bindings to bundled JS version (1b45a4103312c9c059560ae2e1eac25d86b4e2ac)</li>
<li>Release vscode-knip@2.1.5 (328892eb04e65b4702e1ef2303db3156b8f2e1a3)</li>
<li>Fix Astro plugin to support both possible middleware entry points (<a href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1749">#1749</a>) (33e0cc1a530a8cf5b6b05c8b3a3ca55f8fce8a75) - thanks <a href="https://github.com/schmalz-dmi"><code>@​schmalz-dmi</code></a>!</li>
<li>Fix LICENSE link (<a href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1760">#1760</a>) (829620f9077ddea086a610c279c7c1250dd66e11) - thanks <a href="https://github.com/vortispy"><code>@​vortispy</code></a>!</li>
<li>Fix GraphQL Codegen script config dependencies (<a href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1756">#1756</a>) (e841c6355e7eff240e74010bfd2be8bbb22ff2b6) - thanks <a href="https://github.com/jakeleventhal"><code>@​jakeleventhal</code></a>!</li>
<li>Set pnpm config via env vars, disable verify-deps in ecosystem tests (53c12248cc3e79fd79f3efde691d463fc795c40f)</li>
<li>Update slonik ecosystem snapshot (f18410b34c8554364a9f003660bebae5e826de57)</li>
<li>Fix Serverless TypeScript plugin dependencies (<a href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1757">#1757</a>) (ebde7f8f3e3004db7f51fb5d60a0bdc2452116ef) - thanks <a href="https://github.com/jakeleventhal"><code>@​jakeleventhal</code></a>!</li>
<li>Fix extended tsconfig type dependency attribution (<a href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1758">#1758</a>) (f600b09e562317a37844ed8cdf1b9b46e06c9405) - thanks <a href="https://github.com/jakeleventhal"><code>@​jakeleventhal</code></a>!</li>
<li>Fix Bun binary dependency tracking (<a href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1759">#1759</a>) (1b289239f35ff2912195b7e39a96c667c54c1fc5) - thanks <a href="https://github.com/jakeleventhal"><code>@​jakeleventhal</code></a>!</li>
<li>Detect Babel plugins/presets in Vite plugin options (resolve <a href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1761">#1761</a>) (2753d6910743a12a207fca81cb8325c00803963a)</li>
</ul>
<h2>Release 6.14.1</h2>
<ul>
<li>Detect dynamic imports in Svelte compiler (<a href="https://github.com/webpro-nl/knip/tree/HEAD/packages/knip/issues/1747">#1747</a>) (e1c1b1705f96ed7d6ac537a7969cbd07d238246a) - thanks <a href="https://github.com/jinhyuk9714"><code>@​jinhyuk9714</code><...

_Description has been truncated_

---

## [a43b9333](https://github.com/SerendipityOneInc/ecap-workspace/commit/a43b9333b941a9c7b558eaf65ef00fe007fd0b13)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T06:26:56Z
- **PR**: #2086

### Commit Message

```
fix(claw-interface): keep fastapi on starlette-0.x line, ignore litellm 1.84+ (#2086)

## What

Two small backend dependency-resolution hardening changes that complete
the cleanup of the open Dependabot PRs.

### 1. Pin `fastapi<0.137` (`requirements.txt`)
#2079 hard-pinned `starlette==0.52.1` (pre-1.0 — retains
`app.add_event_handler` and httpx `TestClient`) but left `fastapi`
**unpinned**. That's an asymmetric pin: the day `fastapi` raises its
starlette floor to `>=1.0`, the resolver collides with the frozen
`starlette==0.52.1` and fails with `No solution found`.

Capping `fastapi<0.137` keeps it on the known-good 0.136.x line.
Verified in a clean-room install that `fastapi==0.136.3` +
`starlette==0.52.1` + `httpx==0.28.1` resolves cleanly **and runs** —
the `test_warm_pool` / `test_admin_cron` suites that broke on the
transient `starlette==1.2.0` resolution (35 failed + 37 errors,
`'FastAPI' object has no attribute 'add_event_handler'`) all pass again
(23 passed).

### 2. Ignore `litellm >=1.84.0` (`dependabot.yml`)
litellm 1.84+ raised its floor to `importlib-metadata>=8.0`, but
favie-common (git-pinned v0.3.58) pulls `opentelemetry-api==1.25.0`
which caps `importlib-metadata<=7.1` → hard `No solution found`. This
**closes #2080** (which bumped litellm to 1.85.1). Same pattern as the
existing motor/pymongo/Pillow/redis ignores.

Boundary verified against the real favie-common constraint: 1.82.3 and
**1.83.x resolve fine** (importlib-metadata 7.1.0); 1.84.0 is the first
to conflict — so the ignore is `>=1.84.0`, not `>=1.85.0`.

## Why now
The 5 red Python Dependabot PRs (#2080-2084) all failed on a stale
`refs/pull/N/merge` from before #2079's starlette pin. #2081-2084
(ruff/cachetools/pyjwt/openai) just need a rebase onto current main — no
code change. #2080 is the only genuine conflict and is handled here.

## Follow-up
Starlette 1.x migration (lifespan context manager in `app/lifetime.py` +
httpx2 TestClient, then lift both fastapi/starlette pins) is tracked
separately as tech debt.

## Test plan
- [x] `uv pip compile requirements.txt` → fastapi 0.136.3 / starlette
0.52.1 / httpx 0.28.1, no conflict
- [x] Fresh venv install + `pytest test_warm_pool.py test_admin_cron.py`
→ 23 passed
- [x] `dependabot.yml` valid YAML, litellm `>=1.84.0` ignore present
- [ ] CI `claw-interface-quality` green

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Two small backend dependency-resolution hardening changes that complete the cleanup of the open Dependabot PRs.

### 1. Pin `fastapi<0.137` (`requirements.txt`)
#2079 hard-pinned `starlette==0.52.1` (pre-1.0 — retains `app.add_event_handler` and httpx `TestClient`) but left `fastapi` **unpinned**. That's an asymmetric pin: the day `fastapi` raises its starlette floor to `>=1.0`, the resolver collides with the frozen `starlette==0.52.1` and fails with `No solution found`.

Capping `fastapi<0.137` keeps it on the known-good 0.136.x line. Verified in a clean-room install that `fastapi==0.136.3` + `starlette==0.52.1` + `httpx==0.28.1` resolves cleanly **and runs** — the `test_warm_pool` / `test_admin_cron` suites that broke on the transient `starlette==1.2.0` resolution (35 failed + 37 errors, `'FastAPI' object has no attribute 'add_event_handler'`) all pass again (23 passed).

### 2. Ignore `litellm >=1.84.0` (`dependabot.yml`)
litellm 1.84+ raised its floor to `importlib-metadata>=8.0`, but favie-common (git-pinned v0.3.58) pulls `opentelemetry-api==1.25.0` which caps `importlib-metadata<=7.1` → hard `No solution found`. This **closes #2080** (which bumped litellm to 1.85.1). Same pattern as the existing motor/pymongo/Pillow/redis ignores.

Boundary verified against the real favie-common constraint: 1.82.3 and **1.83.x resolve fine** (importlib-metadata 7.1.0); 1.84.0 is the first to conflict — so the ignore is `>=1.84.0`, not `>=1.85.0`.

## Why now
The 5 red Python Dependabot PRs (#2080-2084) all failed on a stale `refs/pull/N/merge` from before #2079's starlette pin. #2081-2084 (ruff/cachetools/pyjwt/openai) just need a rebase onto current main — no code change. #2080 is the only genuine conflict and is handled here.

## Follow-up
Starlette 1.x migration (lifespan context manager in `app/lifetime.py` + httpx2 TestClient, then lift both fastapi/starlette pins) is tracked separately as tech debt.

## Test plan
- [x] `uv pip compile requirements.txt` → fastapi 0.136.3 / starlette 0.52.1 / httpx 0.28.1, no conflict
- [x] Fresh venv install + `pytest test_warm_pool.py test_admin_cron.py` → 23 passed
- [x] `dependabot.yml` valid YAML, litellm `>=1.84.0` ignore present
- [ ] CI `claw-interface-quality` green

---

## [03d37ebc](https://github.com/SerendipityOneInc/ecap-workspace/commit/03d37ebc54199b99f4c2fb8b4338d1846afd1e8a)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T05:53:50Z
- **PR**: #2076

### Commit Message

```
fix(web): createObjectURL leaks in MMAttachments download + pptx-parser partial failure (#2076)

## Summary

#2072 follow-up(createObjectURL 14 文件 → useObjectUrl,**不在 #2072 自身
scope**)的 PR 2 / 3。修两个真实 lifecycle bug,跟 PR #2075 独立可平行。

**Bug 1 —
`MMAttachments.tsx::FileAttachment.handleDownload`**(`setTimeout(revoke,
1000)` race)
- unmount race / double-click race / timing fragility 三连
- 改用 `lib/download.ts::triggerDownload`(已 battle-tested 同步 click + 同步
revoke)
- `triggerDownload` 由 module-local 改 export

**Bug 2 — `pptx-parser.ts::fileToBlobUrl`**(部分失败 leak)
- parse 中途 throw 时,已 mint 的 ObjectURL 永不进 `slides` state → 永不 revoke
- 累计 `createdUrls: string[]` + `try/catch` 包裹 slide 循环,throw 路径统一 revoke
- 抽 `parseOneSlide` helper 保持 nesting ≤ max-depth=5

## 测试

- **MMAttachments**: 锁两条 invariant —— 单点击后 revoke 在同 tick 触发(无 timer);1s
内连点两次,两个 URL 都被 revoke(不再因 ref 被覆盖而 leak URL #1)
- **pptx-parser**: 成功路径 0 revoke(所有权交 slides[]);partial-failure 时 throw
前每个 mint 都被 revoke(用 `vi.spyOn(DOMParser.prototype, 'parseFromString')`
在第 4 次调用触发 throw,精准 land 在 slide 1 minted URL 之后)

## Test plan

- [x] `pnpm lint` 全绿
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 全 6234 测试通过(含新增 2 case for MMAttachments + 2 case
for pptx-parser)
- [ ] CI: code-quality / lint-and-test 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

#2072 follow-up(createObjectURL 14 文件 → useObjectUrl,**不在 #2072 自身 scope**)的 PR 2 / 3。修两个真实 lifecycle bug,跟 PR #2075 独立可平行。

**Bug 1 — `MMAttachments.tsx::FileAttachment.handleDownload`**(`setTimeout(revoke, 1000)` race)
- unmount race / double-click race / timing fragility 三连
- 改用 `lib/download.ts::triggerDownload`(已 battle-tested 同步 click + 同步 revoke)
- `triggerDownload` 由 module-local 改 export

**Bug 2 — `pptx-parser.ts::fileToBlobUrl`**(部分失败 leak)
- parse 中途 throw 时,已 mint 的 ObjectURL 永不进 `slides` state → 永不 revoke
- 累计 `createdUrls: string[]` + `try/catch` 包裹 slide 循环,throw 路径统一 revoke
- 抽 `parseOneSlide` helper 保持 nesting ≤ max-depth=5

## 测试

- **MMAttachments**: 锁两条 invariant —— 单点击后 revoke 在同 tick 触发(无 timer);1s 内连点两次,两个 URL 都被 revoke(不再因 ref 被覆盖而 leak URL #1)
- **pptx-parser**: 成功路径 0 revoke(所有权交 slides[]);partial-failure 时 throw 前每个 mint 都被 revoke(用 `vi.spyOn(DOMParser.prototype, 'parseFromString')` 在第 4 次调用触发 throw,精准 land 在 slide 1 minted URL 之后)

## Test plan

- [x] `pnpm lint` 全绿
- [x] `npx tsc --noEmit` 全绿
- [x] `pnpm test:unit` 全 6234 测试通过(含新增 2 case for MMAttachments + 2 case for pptx-parser)
- [ ] CI: code-quality / lint-and-test 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [fc220c6d](https://github.com/SerendipityOneInc/ecap-workspace/commit/fc220c6d3af1b1d59b764faf5976c7d4f951fe32)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T05:53:26Z
- **PR**: #2075

### Commit Message

```
refactor(web): add useObjectUrl helper + collapse inline blob lifecycle (#2075)

## Summary

#2072 follow-up (createObjectURL 14 文件 → useObjectUrl,**不在 #2072 自身
scope**)的 PR 1 / 3:

- 新 `web/app/src/hooks/useObjectUrl.ts` (~25 行 + JSDoc) —— 封装 `useEffect
→ create → revoke + gate-on-current-blob` 这套 5 行 pattern
- 迁移 `useAuthBlob` + `useResolvedUrl` 用新 hook;`useResolvedUrl` 的
MIME-retag 步骤搬进 `useMemo` 输出 `Blob | null`
- 新 unit test 覆盖:null/undefined blob、mount/unmount lifecycle、blob
change、**gate-on-current-blob regression**(防止 swap 后一帧 stale URL
暴露)、same-reference 幂等
- 落 spec
`docs/superpowers/specs/2026-05-28-object-url-hook-rollout.md`,详述 14
文件审计 + 3-PR 拆分

## Why gate-on-current-blob 必须保留

`useState` 在 prop change 后比 `useEffect` cleanup 慢一拍。如果不在返回时 gate(`blob ?
url : null`),swap blob 的那一帧会返回上个 blob 的 URL —— 在 `useAuthBlob` 里就是上个
auth identity 下的内容。这是 `useAuthBlob` 经 5 轮 Codex review
才到位的细节,`@react-hookz/web` 的 `useObjectURL` 没这个语义,所以选择 inline 而非引 dep。

## 后续

- PR 2(独立可平行): 修两个真 lifecycle bug —— `MMAttachments.tsx` 下载
`setTimeout(revoke, 1000)` race + `pptx-parser.ts` partial-failure leak
- PR 3(依赖本 PR merge): 把 `UploadsFeed` / `MyUploadsTab` 的手维护 token-scoped
`Map<key, ObjectURL>` 并行缓存改 `queryClient.fetchQuery` + 加
`no-restricted-syntax` lint guard

## Test plan

- [x] `pnpm lint` (web/app) 全绿
- [x] `npx tsc --noEmit` (web/app) 全绿  
- [x] `pnpm test:unit` 全 6237 测试通过(含新增 7 case + 修改的
useAuthBlob/useResolvedUrl 既有 spec)
- [ ] CI: code-quality / lint-and-test 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

#2072 follow-up (createObjectURL 14 文件 → useObjectUrl,**不在 #2072 自身 scope**)的 PR 1 / 3:

- 新 `web/app/src/hooks/useObjectUrl.ts` (~25 行 + JSDoc) —— 封装 `useEffect → create → revoke + gate-on-current-blob` 这套 5 行 pattern
- 迁移 `useAuthBlob` + `useResolvedUrl` 用新 hook;`useResolvedUrl` 的 MIME-retag 步骤搬进 `useMemo` 输出 `Blob | null`
- 新 unit test 覆盖:null/undefined blob、mount/unmount lifecycle、blob change、**gate-on-current-blob regression**(防止 swap 后一帧 stale URL 暴露)、same-reference 幂等
- 落 spec `docs/superpowers/specs/2026-05-28-object-url-hook-rollout.md`,详述 14 文件审计 + 3-PR 拆分

## Why gate-on-current-blob 必须保留

`useState` 在 prop change 后比 `useEffect` cleanup 慢一拍。如果不在返回时 gate(`blob ? url : null`),swap blob 的那一帧会返回上个 blob 的 URL —— 在 `useAuthBlob` 里就是上个 auth identity 下的内容。这是 `useAuthBlob` 经 5 轮 Codex review 才到位的细节,`@react-hookz/web` 的 `useObjectURL` 没这个语义,所以选择 inline 而非引 dep。

## 后续

- PR 2(独立可平行): 修两个真 lifecycle bug —— `MMAttachments.tsx` 下载 `setTimeout(revoke, 1000)` race + `pptx-parser.ts` partial-failure leak
- PR 3(依赖本 PR merge): 把 `UploadsFeed` / `MyUploadsTab` 的手维护 token-scoped `Map<key, ObjectURL>` 并行缓存改 `queryClient.fetchQuery` + 加 `no-restricted-syntax` lint guard

## Test plan

- [x] `pnpm lint` (web/app) 全绿
- [x] `npx tsc --noEmit` (web/app) 全绿  
- [x] `pnpm test:unit` 全 6237 测试通过(含新增 7 case + 修改的 useAuthBlob/useResolvedUrl 既有 spec)
- [ ] CI: code-quality / lint-and-test 绿

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [dd1d5a29](https://github.com/SerendipityOneInc/ecap-workspace/commit/dd1d5a2935fe84a7a98d470565ec12fbf03a650e)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T05:51:40Z
- **PR**: #2074

### Commit Message

```
chore(web): introduce zustand + spec for client-only store template (#2074)

## Summary

为 client-only store template 迁移 epic 做基础设施铺垫。**本 PR 不动任何生产代码**——只装依赖、加
CI guard、改规则文档、落 spec,把"决策"与"实施"分离,让 review 集中在方向上。

实际的存储迁移在后续 PR 2-6 推进(详见 spec §5)。

### 改动
- **新增 spec**:
`docs/superpowers/specs/2026-05-28-zustand-store-migration.md` — 评估了 5
个候选库,决定引入 Zustand 5.x(vanilla split),拆 6 PR
- **装依赖**: `web/app/package.json` 加 `zustand@^5.0.13`
- **新增 CI guard**: `web/scripts/check-no-react-in-stores.sh` —
must-be-zero 规则,拦截 `web/app/src/lib/*-store.ts` 内的 `react` / 非 vanilla
`zustand` import。接入 `code-quality.yml::pre_lint_scripts`
- **更新 `web/app/AGENTS.md`** Tier C/D 段落: 从"useSyncExternalStore
template"改为"Zustand vanilla split",带 4 条强制约束(react-free / use* 文件分离 /
`persist` middleware / logout reset)
- **knip 临时 ignore**: `zustand` 暂入 `ignoreDependencies`,标 TODO 指向
spec;PR 2 引入首个 consumer 后即删

### Epic 关系
- 本 epic **supersets**
[#2072](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072)(`window.dispatchEvent`
broadcast 收编)
- #2072 的 7 个 event 落到本 epic 的 PR 4-6
- 同时收编现存 2 个手维护 store (`agent-description-store.ts` 115 行 +
`custom-agent-publish-draft-store.ts` 279 行)到 Zustand 模板,合并节省 ~400 行手维护
layer

### 关键引用
- PR
[#2013](https://github.com/SerendipityOneInc/ecap-workspace/pull/2013)
staging deploy 事故 — 新 CI guard 直接防它复发
- PR
[#1974](https://github.com/SerendipityOneInc/ecap-workspace/pull/1974)
(5 轮 Codex 才到位)— 跨 session reset 模板来源
- PR
[#1689](https://github.com/SerendipityOneInc/ecap-workspace/pull/1689) —
即将被 Zustand 模板替代的 `useSyncExternalStore` 原型
- spec
[`2026-05-27-rq-persist-client-evaluation.md`](../blob/main/docs/superpowers/specs/2026-05-27-rq-persist-client-evaluation.md)
— 同期姊妹 spec,本 spec 跟它对称(server data → RQ;client-only data → Zustand)

## Test plan

- [x] `pnpm install` 成功(Zustand 5.0.13 自动选,无 `minimumReleaseAge` 阻塞)
- [x] `bash web/scripts/check-no-react-in-stores.sh` 本地通过(4 file(s)
audited;agent-description-store / custom-agent-publish-draft-store /
api/skills-store / mattermost/post-store 全无 react import)
- [x] False-positive smoke test:注入 `import { useState } from 'react'` 到
store → exit 1 + 报具体行号;`zustand/vanilla` + `zustand/middleware` 不被误伤
- [x] `cd web/app && pnpm lint && npx tsc --noEmit` 通过
- [x] `pnpm lint:deadcode`(knip)通过(zustand 已 ignore)
- [x] `pnpm lint:imports` 通过(只有 pre-existing warning)
- [ ] CI `code-quality / lint-and-test` 全绿(待 reviewer 等)
- [ ] reviewer 确认 epic 方向 + Zustand vanilla split 模板规则 OK 后,启动 PR
2(`agent-description-store.ts` 迁移)

### 不在本 PR 范围
- 任何生产 `*.ts` / `*.tsx` 改动(`package.json` 除外)
- `eslint.config.mjs` 加 `no-restricted-syntax` 拦
`window.dispatchEvent(new Event())` —— 等 PR 6 收尾时加(现在加会立刻让 13 个现存
dispatcher 报错)
- `agent-description-store.ts` / `custom-agent-publish-draft-store.ts`
任何改动 —— PR 2/3 的主菜
- 关闭 #2072 —— 等 PR 4-6 验收时再关

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

为 client-only store template 迁移 epic 做基础设施铺垫。**本 PR 不动任何生产代码**——只装依赖、加 CI guard、改规则文档、落 spec,把"决策"与"实施"分离,让 review 集中在方向上。

实际的存储迁移在后续 PR 2-6 推进(详见 spec §5)。

### 改动
- **新增 spec**: `docs/superpowers/specs/2026-05-28-zustand-store-migration.md` — 评估了 5 个候选库,决定引入 Zustand 5.x(vanilla split),拆 6 PR
- **装依赖**: `web/app/package.json` 加 `zustand@^5.0.13`
- **新增 CI guard**: `web/scripts/check-no-react-in-stores.sh` — must-be-zero 规则,拦截 `web/app/src/lib/*-store.ts` 内的 `react` / 非 vanilla `zustand` import。接入 `code-quality.yml::pre_lint_scripts`
- **更新 `web/app/AGENTS.md`** Tier C/D 段落: 从"useSyncExternalStore template"改为"Zustand vanilla split",带 4 条强制约束(react-free / use* 文件分离 / `persist` middleware / logout reset)
- **knip 临时 ignore**: `zustand` 暂入 `ignoreDependencies`,标 TODO 指向 spec;PR 2 引入首个 consumer 后即删

### Epic 关系
- 本 epic **supersets** [#2072](https://github.com/SerendipityOneInc/ecap-workspace/issues/2072)(`window.dispatchEvent` broadcast 收编)
- #2072 的 7 个 event 落到本 epic 的 PR 4-6
- 同时收编现存 2 个手维护 store (`agent-description-store.ts` 115 行 + `custom-agent-publish-draft-store.ts` 279 行)到 Zustand 模板,合并节省 ~400 行手维护 layer

### 关键引用
- PR [#2013](https://github.com/SerendipityOneInc/ecap-workspace/pull/2013) staging deploy 事故 — 新 CI guard 直接防它复发
- PR [#1974](https://github.com/SerendipityOneInc/ecap-workspace/pull/1974) (5 轮 Codex 才到位)— 跨 session reset 模板来源
- PR [#1689](https://github.com/SerendipityOneInc/ecap-workspace/pull/1689) — 即将被 Zustand 模板替代的 `useSyncExternalStore` 原型
- spec [`2026-05-27-rq-persist-client-evaluation.md`](../blob/main/docs/superpowers/specs/2026-05-27-rq-persist-client-evaluation.md) — 同期姊妹 spec,本 spec 跟它对称(server data → RQ;client-only data → Zustand)

## Test plan

- [x] `pnpm install` 成功(Zustand 5.0.13 自动选,无 `minimumReleaseAge` 阻塞)
- [x] `bash web/scripts/check-no-react-in-stores.sh` 本地通过(4 file(s) audited;agent-description-store / custom-agent-publish-draft-store / api/skills-store / mattermost/post-store 全无 react import)
- [x] False-positive smoke test:注入 `import { useState } from 'react'` 到 store → exit 1 + 报具体行号;`zustand/vanilla` + `zustand/middleware` 不被误伤
- [x] `cd web/app && pnpm lint && npx tsc --noEmit` 通过
- [x] `pnpm lint:deadcode`(knip)通过(zustand 已 ignore)
- [x] `pnpm lint:imports` 通过(只有 pre-existing warning)
- [ ] CI `code-quality / lint-and-test` 全绿(待 reviewer 等)
- [ ] reviewer 确认 epic 方向 + Zustand vanilla split 模板规则 OK 后,启动 PR 2(`agent-description-store.ts` 迁移)

### 不在本 PR 范围
- 任何生产 `*.ts` / `*.tsx` 改动(`package.json` 除外)
- `eslint.config.mjs` 加 `no-restricted-syntax` 拦 `window.dispatchEvent(new Event())` —— 等 PR 6 收尾时加(现在加会立刻让 13 个现存 dispatcher 报错)
- `agent-description-store.ts` / `custom-agent-publish-draft-store.ts` 任何改动 —— PR 2/3 的主菜
- 关闭 #2072 —— 等 PR 4-6 验收时再关

---

## [8cfa7f36](https://github.com/SerendipityOneInc/ecap-workspace/commit/8cfa7f361e8a39276bdba51f62de462622a7c01f)

- **作者**: Chris@ZooClaw
- **日期**: 2026-05-30T05:50:38Z
- **PR**: #2073

### Commit Message

```
chore(docs): bulk archive 48 shipped docs (sweep before 2026-05-15) (#2073)

## Summary

Auto-generated sweep via `/bulk-archive-shipped-docs --before
2026-05-15`.

- **Scanned**: 57 docs (filename date prefix < 2026-05-15)
- **Archived**: 48 — 38 to `docs/archive/specs/`, 10 to
`docs/archive/plans/`
- **Skipped**: 9 (PARTIAL or NOT_SHIPPED; see bottom)

This is a substantially larger sweep than PR #2065 (which did 5).
Reviewer should spot-check 5-10 of the archived rows below; do NOT
auto-merge.

## Verdict inconsistencies to flag

| Doc | Issue | Disposition |
|---|---|---|
| `2026-03-03-gen-claw-design.md` | NOT_SHIPPED in last sweep (PR #2065
skipped). DESIGN_ONLY_VERIFIED this sweep. | **Archived** based on the
more thorough re-read: design intent shipped under renamed paths
(`/gen-claw/` → `/chat/`, `web/` → `web/app/`). |
| `2026-04-30-last-chatted-agent-persistence` (plan + design pair) |
Plan SHIPPED 9/9 (archived this sweep). Design NOT_SHIPPED — subagent
reported iOS files unfindable. | **Plan archived, design skipped.**
Subagent error suspected; re-run when subagents have iOS visibility. |
| `2026-05-06-eca-616-bot-leak-reconciliation` (plan + spec pair) | Plan
PARTIAL (cron + backfill endpoint dropped). Spec SHIPPED (those drops
are documented design pivots in the spec itself). | **Spec archived,
plan skipped.** Defensible split — different framings of same feature. |

## Archived (48 rows)

### To `docs/archive/specs/` (38)

| Source → Target | Verdict | Signals |
|---|---|---|
| `plans/2026-03-03-gen-claw-design.md` →
`archive/specs/2026-03-03-gen-claw-design.md` | DESIGN_ONLY_VERIFIED |
7/9 |
| `specs/2026-04-09-sentry-feedback-system-design.md` →
`archive/specs/...` (no rename) | SHIPPED | 11/11 |
| `specs/2026-04-11-stripe-routes-refactor.md` →
`archive/specs/...-design.md` | SHIPPED | 9/9 |
| `specs/2026-04-15-branded-modules-login.md` → `archive/specs/...` (no
rename) | SHIPPED | 7/7 |
| `specs/2026-04-16-apple-subscription-status.md` →
`archive/specs/...-design.md` | SHIPPED | 7/7 |
| `specs/2026-04-16-merge-queue-rollout.md` →
`archive/specs/...-design.md` | SHIPPED | 6/6 |
| `specs/2026-04-16-service-layer-exceptions.md` →
`archive/specs/...-design.md` | SHIPPED | 7/7 |
| `specs/2026-04-17-web-dedup.md` → `archive/specs/...-design.md` |
SHIPPED | 10/10 |
| `specs/2026-04-20-degraded-banner-iq-bar-design.md` →
`archive/specs/...` | DESIGN_ONLY_VERIFIED | 7/7 |
| `specs/2026-04-20-mm-attachment-preview.md` →
`archive/specs/...-design.md` | DESIGN_ONLY_VERIFIED | 11/11 |
| `specs/2026-04-20-web-dead-code.md` → `archive/specs/...-design.md` |
SHIPPED | 7/7 |
| `specs/2026-04-20-web-import-boundaries.md` →
`archive/specs/...-design.md` | SHIPPED | 9/9 |
| `specs/2026-04-21-custom-chat-list-view.md` →
`archive/specs/...-design.md` | DESIGN_ONLY_VERIFIED | 5/5 |
| `specs/2026-04-22-ci-acceleration.md` → `archive/specs/...-design.md`
| SHIPPED | 12/12 |
| `specs/2026-04-23-subscription-code-design.md` → `archive/specs/...`
(no rename) | SHIPPED | 9/9 |
| `specs/2026-04-24-chat-replay-share-design.md` → `archive/specs/...`
(no rename) | DESIGN_ONLY_VERIFIED | 9/9 |
| `specs/2026-04-24-react-query-migration.md` →
`archive/specs/...-design.md` | SHIPPED | 9/10 |
| `specs/2026-04-24-zooclaw-main-chat-drop-ws-fallback.md` →
`archive/specs/...-design.md` | SHIPPED | 8/8 |
| `specs/2026-04-25-chat-list-scroll-stability.md` →
`archive/specs/...-design.md` | SHIPPED *(then superseded by
UICollectionView; deletions persist)* | 7/7 |
| `specs/2026-04-25-heroicons-tier3-decisions.md` → `archive/specs/...`
(no rename, `-decisions` preserved) | SHIPPED | 5/5 |
| `specs/2026-04-25-provider-logo-svg-migration.md` →
`archive/specs/...-design.md` | SHIPPED | 6/6 |
| `specs/2026-04-25-react-query-migration-v2.md` → `archive/specs/...`
(no rename) | SHIPPED | 8/8 |
| `specs/2026-04-27-web-refactor-status.md` → `archive/specs/...` (no
rename, `-status` preserved) | SHIPPED | 8/8 |
| `specs/2026-04-28-eca-579-admin-customer-events.md` →
`archive/specs/...-design.md` | SHIPPED | 10/10 |
| `specs/2026-04-29-eca-555-feishu-session-redis.md` →
`archive/specs/...-design.md` | SHIPPED | 15/15 |
| `specs/2026-04-30-asr-audio-persistence-design.md` →
`archive/specs/...` (no rename) | SHIPPED | 12/12 |
| `specs/2026-04-30-eca-583-weixin-channel-qr.md` →
`archive/specs/...-design.md` | SHIPPED | 7/7 |
| `specs/2026-05-02-replay-context-relocation.md` →
`archive/specs/...-design.md` | SHIPPED | 6/6 |
| `specs/2026-05-02-web-layered-structure-audit.md` →
`archive/specs/...` (no rename, `-audit` preserved) | SHIPPED | 4/4 |
| `specs/2026-05-04-ios-media-download-design.md` → `archive/specs/...`
(no rename) | DESIGN_ONLY_VERIFIED | 5/5 |
| `specs/2026-05-06-eca-616-bot-leak-reconciliation.md` →
`archive/specs/...` (no rename, `-rca`-like) | SHIPPED | 13/14 |
| `specs/2026-05-06-i18n-url-redesign-design.md` → `archive/specs/...`
(no rename) | DESIGN_ONLY_VERIFIED | 7/8 |
| `specs/2026-05-07-eca-625-wecom-channel.md` →
`archive/specs/...-design.md` | SHIPPED | 9/9 |
| `specs/2026-05-07-ios-document-preview-design.md` →
`archive/specs/...` (no rename) | DESIGN_ONLY_VERIFIED | 8/8 |
| `specs/2026-05-08-stripe-mongo-drift-rca.md` → `archive/specs/...` (no
rename, `-rca` preserved) | SHIPPED | 13/13 |
| `specs/2026-05-09-antom-payment-refactor.md` →
`archive/specs/...-design.md` | SHIPPED | 11/11 |
| `specs/2026-05-13-eca-669-invoice-download.md` →
`archive/specs/...-design.md` | SHIPPED | 8/8 |
| `specs/2026-05-14-eca-675-skip-onboarding-design.md` →
`archive/specs/...` (no rename) | SHIPPED | 10/10 |

### To `docs/archive/plans/` (10)

| Source → Target | Verdict | Signals |
|---|---|---|
| `plans/2026-04-09-sentry-feedback-system.md` →
`archive/plans/...-plan.md` | SHIPPED | 9/9 |
| `plans/2026-04-16-apple-subscription-status.md` →
`archive/plans/...-plan.md` | SHIPPED | 7/7 |
| `plans/2026-04-30-asr-audio-persistence.md` →
`archive/plans/...-plan.md` | SHIPPED | 18/20 |
| `plans/2026-04-30-last-chatted-agent-persistence.md` →
`archive/plans/...-plan.md` | SHIPPED | 9/9 |
| `plans/2026-05-04-ios-media-download.md` → `archive/plans/...-plan.md`
| SHIPPED | 8/8 |
| `plans/2026-05-06-i18n-url-redesign.md` → `archive/plans/...-plan.md`
| SHIPPED | 13/13 |
| `plans/2026-05-14-eca-675-skip-onboarding.md` →
`archive/plans/...-plan.md` | SHIPPED | 8/9 |
| `specs/2026-04-14-landing-client-decomposition.md` →
`archive/plans/...-plan.md` ⚠️ bucket changed | SHIPPED | 6/6 |
| `specs/2026-04-16-reduce-file-length-python.md` →
`archive/plans/...-plan.md` ⚠️ bucket changed | SHIPPED | 6/7 |
| `specs/2026-04-25-heroicons-migration.md` →
`archive/plans/...-plan.md` ⚠️ bucket changed | SHIPPED | 9/9 |

⚠️ rows: subagent classified content as execution plan (numbered PR/Step
structure) despite being filed under `specs/`. Bucket reclassified per
skill's "trust content, not filename" rule.

## Link rewrites

**Live docs (4 files)** — these stayed in active dirs but had inbound
references to archived docs rewritten:

- `docs/ci-review-and-merge-queue.md` — 3 occurrences
(merge-queue-rollout, ci-acceleration)
- `docs/superpowers/specs/2026-04-27-uicollectionview-chat-layout.md` —
`Supersedes:` line (chat-list-scroll-stability) — this doc itself stays
live (PARTIAL — BottomAnchoredLayout replaced by ChatLayout lib)
- `docs/superpowers/specs/2026-05-27-rq-persist-client-evaluation.md` —
preamble citing v1/v2 react-query migration specs
- `web/app/AGENTS.md` (via `CLAUDE.md` symlink) — 2 occurrences
(heroicons-migration, react-query-migration). Both are backtick text
citations; not clickable links but kept accurate.

**Moved docs (cross-batch)** — 7 moved docs had basename references to
other moved docs rewritten via bulk sed. Sed substitutions are
basename-only (`OLD.md` → `NEW.md`); relative path prefixes in some
cases may need a manual touch-up if reviewers spot them. One known case
fixed explicitly: `eca-675-skip-onboarding-design.md`'s link to
`onboarding-status-resolution-design` (archived in PR #2065) rewritten
from `../../archive/specs/...` to `./...` since both now live in
`docs/archive/specs/`.

**Known sed ambiguity**: `2026-04-16-apple-subscription-status.md`
exists as both plan (→ `-plan.md`) and spec (→ `-design.md`) with
identical source basename. Sed picks the first matching rule
(`-plan.md`); references intending the design may now incorrectly point
at `-plan.md`. Spot-check if reviewing.

## Skipped (kept in active dirs)

| Source | Verdict | Reason |
|---|---|---|
| `docs/superpowers/plans/2026-03-11-tasks-page.md` | PARTIAL | `/tasks`
page shipped then reverted in PR #114; backend kept |
| `docs/plans/2026-04-01-litellm-decomposition.md` | PARTIAL | 1/7 PRs
landed |
| `docs/superpowers/plans/2026-04-27-uicollectionview-chat-layout.md` |
PARTIAL | BottomAnchoredLayout replaced by `ChatLayout` lib |
| `docs/superpowers/specs/2026-04-27-uicollectionview-chat-layout.md` |
PARTIAL | same as above |
| `docs/superpowers/plans/2026-05-06-eca-616-bot-leak-reconciliation.md`
| PARTIAL | reconciliation cron + backfill endpoint dropped (companion
spec was archived — see "Verdict inconsistencies") |
| `docs/superpowers/plans/2026-05-13-backend-vulture-dead-code.md` |
PARTIAL | PR1 (informational) shipped; PR2 (hard-gate flip) pending |
|
`docs/superpowers/specs/2026-04-30-last-chatted-agent-persistence-design.md`
| NOT_SHIPPED | subagent couldn't locate iOS files; likely false
negative (companion plan SHIPPED 9/9) |
| `docs/superpowers/specs/2026-05-02-python-dependency-locking.md` |
NOT_SHIPPED | PRs 2-6 of plan never executed |
|
`docs/superpowers/specs/2026-05-14-subscription-system-hardening-plan.md`
| PARTIAL | Phase 3 (provider-neutral entitlement service) not shipped |

## Test plan

- [ ] Spot-check 5-10 archived rows above — does the verdict feel right?
The skill assumed each subagent could see code paths; misjudgments are
likely on iOS docs (ZooClaw repo) and Phase-3-style multi-phase plans
- [ ] Verify the 3 ⚠️ bucket reclassifications (specs → plans) feel
right
- [ ] Verify the verdict inconsistencies in the table at top —
particularly whether `last-chatted-agent-persistence-design` should also
be archived (i.e., the design subagent was wrong)
- [ ] Spot-check the 4 live-doc link rewrites — navigate the links to
ensure they resolve
- [ ] Skim 2-3 moved docs to confirm cross-batch basename substitutions
didn't garble any text
- [ ] **Do not auto-merge** — false-positive archive of an active doc is
the worst-case failure

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Auto-generated sweep via `/bulk-archive-shipped-docs --before 2026-05-15`.

- **Scanned**: 57 docs (filename date prefix < 2026-05-15)
- **Archived**: 48 — 38 to `docs/archive/specs/`, 10 to `docs/archive/plans/`
- **Skipped**: 9 (PARTIAL or NOT_SHIPPED; see bottom)

This is a substantially larger sweep than PR #2065 (which did 5). Reviewer should spot-check 5-10 of the archived rows below; do NOT auto-merge.

## Verdict inconsistencies to flag

| Doc | Issue | Disposition |
|---|---|---|
| `2026-03-03-gen-claw-design.md` | NOT_SHIPPED in last sweep (PR #2065 skipped). DESIGN_ONLY_VERIFIED this sweep. | **Archived** based on the more thorough re-read: design intent shipped under renamed paths (`/gen-claw/` → `/chat/`, `web/` → `web/app/`). |
| `2026-04-30-last-chatted-agent-persistence` (plan + design pair) | Plan SHIPPED 9/9 (archived this sweep). Design NOT_SHIPPED — subagent reported iOS files unfindable. | **Plan archived, design skipped.** Subagent error suspected; re-run when subagents have iOS visibility. |
| `2026-05-06-eca-616-bot-leak-reconciliation` (plan + spec pair) | Plan PARTIAL (cron + backfill endpoint dropped). Spec SHIPPED (those drops are documented design pivots in the spec itself). | **Spec archived, plan skipped.** Defensible split — different framings of same feature. |

## Archived (48 rows)

### To `docs/archive/specs/` (38)

| Source → Target | Verdict | Signals |
|---|---|---|
| `plans/2026-03-03-gen-claw-design.md` → `archive/specs/2026-03-03-gen-claw-design.md` | DESIGN_ONLY_VERIFIED | 7/9 |
| `specs/2026-04-09-sentry-feedback-system-design.md` → `archive/specs/...` (no rename) | SHIPPED | 11/11 |
| `specs/2026-04-11-stripe-routes-refactor.md` → `archive/specs/...-design.md` | SHIPPED | 9/9 |
| `specs/2026-04-15-branded-modules-login.md` → `archive/specs/...` (no rename) | SHIPPED | 7/7 |
| `specs/2026-04-16-apple-subscription-status.md` → `archive/specs/...-design.md` | SHIPPED | 7/7 |
| `specs/2026-04-16-merge-queue-rollout.md` → `archive/specs/...-design.md` | SHIPPED | 6/6 |
| `specs/2026-04-16-service-layer-exceptions.md` → `archive/specs/...-design.md` | SHIPPED | 7/7 |
| `specs/2026-04-17-web-dedup.md` → `archive/specs/...-design.md` | SHIPPED | 10/10 |
| `specs/2026-04-20-degraded-banner-iq-bar-design.md` → `archive/specs/...` | DESIGN_ONLY_VERIFIED | 7/7 |
| `specs/2026-04-20-mm-attachment-preview.md` → `archive/specs/...-design.md` | DESIGN_ONLY_VERIFIED | 11/11 |
| `specs/2026-04-20-web-dead-code.md` → `archive/specs/...-design.md` | SHIPPED | 7/7 |
| `specs/2026-04-20-web-import-boundaries.md` → `archive/specs/...-design.md` | SHIPPED | 9/9 |
| `specs/2026-04-21-custom-chat-list-view.md` → `archive/specs/...-design.md` | DESIGN_ONLY_VERIFIED | 5/5 |
| `specs/2026-04-22-ci-acceleration.md` → `archive/specs/...-design.md` | SHIPPED | 12/12 |
| `specs/2026-04-23-subscription-code-design.md` → `archive/specs/...` (no rename) | SHIPPED | 9/9 |
| `specs/2026-04-24-chat-replay-share-design.md` → `archive/specs/...` (no rename) | DESIGN_ONLY_VERIFIED | 9/9 |
| `specs/2026-04-24-react-query-migration.md` → `archive/specs/...-design.md` | SHIPPED | 9/10 |
| `specs/2026-04-24-zooclaw-main-chat-drop-ws-fallback.md` → `archive/specs/...-design.md` | SHIPPED | 8/8 |
| `specs/2026-04-25-chat-list-scroll-stability.md` → `archive/specs/...-design.md` | SHIPPED *(then superseded by UICollectionView; deletions persist)* | 7/7 |
| `specs/2026-04-25-heroicons-tier3-decisions.md` → `archive/specs/...` (no rename, `-decisions` preserved) | SHIPPED | 5/5 |
| `specs/2026-04-25-provider-logo-svg-migration.md` → `archive/specs/...-design.md` | SHIPPED | 6/6 |
| `specs/2026-04-25-react-query-migration-v2.md` → `archive/specs/...` (no rename) | SHIPPED | 8/8 |
| `specs/2026-04-27-web-refactor-status.md` → `archive/specs/...` (no rename, `-status` preserved) | SHIPPED | 8/8 |
| `specs/2026-04-28-eca-579-admin-customer-events.md` → `archive/specs/...-design.md` | SHIPPED | 10/10 |
| `specs/2026-04-29-eca-555-feishu-session-redis.md` → `archive/specs/...-design.md` | SHIPPED | 15/15 |
| `specs/2026-04-30-asr-audio-persistence-design.md` → `archive/specs/...` (no rename) | SHIPPED | 12/12 |
| `specs/2026-04-30-eca-583-weixin-channel-qr.md` → `archive/specs/...-design.md` | SHIPPED | 7/7 |
| `specs/2026-05-02-replay-context-relocation.md` → `archive/specs/...-design.md` | SHIPPED | 6/6 |
| `specs/2026-05-02-web-layered-structure-audit.md` → `archive/specs/...` (no rename, `-audit` preserved) | SHIPPED | 4/4 |
| `specs/2026-05-04-ios-media-download-design.md` → `archive/specs/...` (no rename) | DESIGN_ONLY_VERIFIED | 5/5 |
| `specs/2026-05-06-eca-616-bot-leak-reconciliation.md` → `archive/specs/...` (no rename, `-rca`-like) | SHIPPED | 13/14 |
| `specs/2026-05-06-i18n-url-redesign-design.md` → `archive/specs/...` (no rename) | DESIGN_ONLY_VERIFIED | 7/8 |
| `specs/2026-05-07-eca-625-wecom-channel.md` → `archive/specs/...-design.md` | SHIPPED | 9/9 |
| `specs/2026-05-07-ios-document-preview-design.md` → `archive/specs/...` (no rename) | DESIGN_ONLY_VERIFIED | 8/8 |
| `specs/2026-05-08-stripe-mongo-drift-rca.md` → `archive/specs/...` (no rename, `-rca` preserved) | SHIPPED | 13/13 |
| `specs/2026-05-09-antom-payment-refactor.md` → `archive/specs/...-design.md` | SHIPPED | 11/11 |
| `specs/2026-05-13-eca-669-invoice-download.md` → `archive/specs/...-design.md` | SHIPPED | 8/8 |
| `specs/2026-05-14-eca-675-skip-onboarding-design.md` → `archive/specs/...` (no rename) | SHIPPED | 10/10 |

### To `docs/archive/plans/` (10)

| Source → Target | Verdict | Signals |
|---|---|---|
| `plans/2026-04-09-sentry-feedback-system.md` → `archive/plans/...-plan.md` | SHIPPED | 9/9 |
| `plans/2026-04-16-apple-subscription-status.md` → `archive/plans/...-plan.md` | SHIPPED | 7/7 |
| `plans/2026-04-30-asr-audio-persistence.md` → `archive/plans/...-plan.md` | SHIPPED | 18/20 |
| `plans/2026-04-30-last-chatted-agent-persistence.md` → `archive/plans/...-plan.md` | SHIPPED | 9/9 |
| `plans/2026-05-04-ios-media-download.md` → `archive/plans/...-plan.md` | SHIPPED | 8/8 |
| `plans/2026-05-06-i18n-url-redesign.md` → `archive/plans/...-plan.md` | SHIPPED | 13/13 |
| `plans/2026-05-14-eca-675-skip-onboarding.md` → `archive/plans/...-plan.md` | SHIPPED | 8/9 |
| `specs/2026-04-14-landing-client-decomposition.md` → `archive/plans/...-plan.md` ⚠️ bucket changed | SHIPPED | 6/6 |
| `specs/2026-04-16-reduce-file-length-python.md` → `archive/plans/...-plan.md` ⚠️ bucket changed | SHIPPED | 6/7 |
| `specs/2026-04-25-heroicons-migration.md` → `archive/plans/...-plan.md` ⚠️ bucket changed | SHIPPED | 9/9 |

⚠️ rows: subagent classified content as execution plan (numbered PR/Step structure) despite being filed under `specs/`. Bucket reclassified per skill's "trust content, not filename" rule.

## Link rewrites

**Live docs (4 files)** — these stayed in active dirs but had inbound references to archived docs rewritten:

- `docs/ci-review-and-merge-queue.md` — 3 occurrences (merge-queue-rollout, ci-acceleration)
- `docs/superpowers/specs/2026-04-27-uicollectionview-chat-layout.md` — `Supersedes:` line (chat-list-scroll-stability) — this doc itself stays live (PARTIAL — BottomAnchoredLayout replaced by ChatLayout lib)
- `docs/superpowers/specs/2026-05-27-rq-persist-client-evaluation.md` — preamble citing v1/v2 react-query migration specs
- `web/app/AGENTS.md` (via `CLAUDE.md` symlink) — 2 occurrences (heroicons-migration, react-query-migration). Both are backtick text citations; not clickable links but kept accurate.

**Moved docs (cross-batch)** — 7 moved docs had basename references to other moved docs rewritten via bulk sed. Sed substitutions are basename-only (`OLD.md` → `NEW.md`); relative path prefixes in some cases may need a manual touch-up if reviewers spot them. One known case fixed explicitly: `eca-675-skip-onboarding-design.md`'s link to `onboarding-status-resolution-design` (archived in PR #2065) rewritten from `../../archive/specs/...` to `./...` since both now live in `docs/archive/specs/`.

**Known sed ambiguity**: `2026-04-16-apple-subscription-status.md` exists as both plan (→ `-plan.md`) and spec (→ `-design.md`) with identical source basename. Sed picks the first matching rule (`-plan.md`); references intending the design may now incorrectly point at `-plan.md`. Spot-check if reviewing.

## Skipped (kept in active dirs)

| Source | Verdict | Reason |
|---|---|---|
| `docs/superpowers/plans/2026-03-11-tasks-page.md` | PARTIAL | `/tasks` page shipped then reverted in PR #114; backend kept |
| `docs/plans/2026-04-01-litellm-decomposition.md` | PARTIAL | 1/7 PRs landed |
| `docs/superpowers/plans/2026-04-27-uicollectionview-chat-layout.md` | PARTIAL | BottomAnchoredLayout replaced by `ChatLayout` lib |
| `docs/superpowers/specs/2026-04-27-uicollectionview-chat-layout.md` | PARTIAL | same as above |
| `docs/superpowers/plans/2026-05-06-eca-616-bot-leak-reconciliation.md` | PARTIAL | reconciliation cron + backfill endpoint dropped (companion spec was archived — see "Verdict inconsistencies") |
| `docs/superpowers/plans/2026-05-13-backend-vulture-dead-code.md` | PARTIAL | PR1 (informational) shipped; PR2 (hard-gate flip) pending |
| `docs/superpowers/specs/2026-04-30-last-chatted-agent-persistence-design.md` | NOT_SHIPPED | subagent couldn't locate iOS files; likely false negative (companion plan SHIPPED 9/9) |
| `docs/superpowers/specs/2026-05-02-python-dependency-locking.md` | NOT_SHIPPED | PRs 2-6 of plan never executed |
| `docs/superpowers/specs/2026-05-14-subscription-system-hardening-plan.md` | PARTIAL | Phase 3 (provider-neutral entitlement service) not shipped |

## Test plan

- [ ] Spot-check 5-10 archived rows above — does the verdict feel right? The skill assumed each subagent could see code paths; misjudgments are likely on iOS docs (ZooClaw repo) and Phase-3-style multi-phase plans
- [ ] Verify the 3 ⚠️ bucket reclassifications (specs → plans) feel right
- [ ] Verify the verdict inconsistencies in the table at top — particularly whether `last-chatted-agent-persistence-design` should also be archived (i.e., the design subagent was wrong)
- [ ] Spot-check the 4 live-doc link rewrites — navigate the links to ensure they resolve
- [ ] Skim 2-3 moved docs to confirm cross-batch basename substitutions didn't garble any text
- [ ] **Do not auto-merge** — false-positive archive of an active doc is the worst-case failure

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [390dfaa5](https://github.com/SerendipityOneInc/ecap-workspace/commit/390dfaa5ef39b6291957eda3c088cbd39e9ce5d4)

- **作者**: bill-srp
- **日期**: 2026-05-30T04:09:42Z
- **PR**: #2079

### Commit Message

```
feat(bot-state): dual-write core bot state to normalized ZooClawComputer store (#2079)

## Linear

https://linear.app/srpone/issue/ECA-863/fixbot-state-scope-legacy-mirror-cleanup-for-service-agents-branch

## Summary

ZooClaw computer dual-write (iteration 1). Every legacy
`Account.openclaw_bots` mutation now also mirrors **core** bot/computer
state into the normalized `ecap-zooclaw-computers` store via a new
`bot_state_service`, so V2 becomes a complete reflection of legacy and
core-field reads can flip from "legacy union" to "V2 only".

- **New `app/services/computer/bot_state_service.py`** — the
contract-compliant (import-linter **C4**: repos stay independent) home
for cross-repo orchestration. Ops: `set_bot_status`, `set_bot_field`
(core-field gate), `replace_bot_list` (reconcile-set semantics),
`clear_bot_state`, `mirror_created_bot`, `clear_v2_mirror`, plus the
pure `bot_ids_of(Account | None)` helper.
- **Projectors** (`app/services/computer/_projectors.py`) —
`project_bot_to_computer` + the `CORE_BOT_FIELDS` frozenset map a legacy
bot dict → `ZooClawComputer`. Non-core fields (Mattermost,
`access_token`) stay legacy-only and are deferred to iteration 2.
- **Call-site routing** — `bot_init`, `bot_lifecycle`, `bot_config`,
`bot_stop`, `openclaw_admin`, `openclaw_settings`, and warm-pool
materialization route their core-state writes through
`bot_state_service`.
- **Legacy stays canonical** — the legacy write happens first; V2 mirror
failures are logged but never propagated. An admin reconcile endpoint
backfills/repairs drift.
- **`computer_repo`** — soft-delete (`deleted_at`) instead of hard
delete, with `{deleted_at: None}` read guards; write-once create
semantics on upsert.

The mirror is best-effort and tightly scoped. `ensure_app`'s app-create
path writes legacy atomically via CAS, then `clear_v2_mirror` drops only
the pre-reset `computer_id`s **without** re-touching `openclaw_app` —
fixing a regression where a post-CAS reset re-opened the CAS guard
(race). `bot_init`'s CAS-win path mirrors the new bot via
`mirror_created_bot` (no redundant second legacy write).

Design + plan:
`docs/superpowers/specs/2026-05-28-zooclaw-computer-dual-write-design.md`.

## Test plan

- [x] Full unit suite green in devcontainer — **3960 passed**
- [x] BDD `bot_state_dual_write.feature` scenarios pass (dual-write +
reconcile + error-swallow)
- [x] New coverage: `test_bot_state_service.py`,
`test_bot_state_projectors.py`, `test_computer_repo_extensions.py`,
updated `test_openclaw_routes.py` / `test_openclaw_endpoints_extra.py`
- [x] ruff + pyright clean on changed files
- [ ] CI `build-and-test` + `auto-review` green

> Note: a single pre-existing, order-dependent failure
(`test_litellm_video::test_reframe_params`, passes in isolation) is
unrelated to this branch and exists on `main` — tracked separately, not
introduced here.

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-863/fixbot-state-scope-legacy-mirror-cleanup-for-service-agents-branch

## Summary

ZooClaw computer dual-write (iteration 1). Every legacy `Account.openclaw_bots` mutation now also mirrors **core** bot/computer state into the normalized `ecap-zooclaw-computers` store via a new `bot_state_service`, so V2 becomes a complete reflection of legacy and core-field reads can flip from "legacy union" to "V2 only".

- **New `app/services/computer/bot_state_service.py`** — the contract-compliant (import-linter **C4**: repos stay independent) home for cross-repo orchestration. Ops: `set_bot_status`, `set_bot_field` (core-field gate), `replace_bot_list` (reconcile-set semantics), `clear_bot_state`, `mirror_created_bot`, `clear_v2_mirror`, plus the pure `bot_ids_of(Account | None)` helper.
- **Projectors** (`app/services/computer/_projectors.py`) — `project_bot_to_computer` + the `CORE_BOT_FIELDS` frozenset map a legacy bot dict → `ZooClawComputer`. Non-core fields (Mattermost, `access_token`) stay legacy-only and are deferred to iteration 2.
- **Call-site routing** — `bot_init`, `bot_lifecycle`, `bot_config`, `bot_stop`, `openclaw_admin`, `openclaw_settings`, and warm-pool materialization route their core-state writes through `bot_state_service`.
- **Legacy stays canonical** — the legacy write happens first; V2 mirror failures are logged but never propagated. An admin reconcile endpoint backfills/repairs drift.
- **`computer_repo`** — soft-delete (`deleted_at`) instead of hard delete, with `{deleted_at: None}` read guards; write-once create semantics on upsert.

The mirror is best-effort and tightly scoped. `ensure_app`'s app-create path writes legacy atomically via CAS, then `clear_v2_mirror` drops only the pre-reset `computer_id`s **without** re-touching `openclaw_app` — fixing a regression where a post-CAS reset re-opened the CAS guard (race). `bot_init`'s CAS-win path mirrors the new bot via `mirror_created_bot` (no redundant second legacy write).

Design + plan: `docs/superpowers/specs/2026-05-28-zooclaw-computer-dual-write-design.md`.

## Test plan

- [x] Full unit suite green in devcontainer — **3960 passed**
- [x] BDD `bot_state_dual_write.feature` scenarios pass (dual-write + reconcile + error-swallow)
- [x] New coverage: `test_bot_state_service.py`, `test_bot_state_projectors.py`, `test_computer_repo_extensions.py`, updated `test_openclaw_routes.py` / `test_openclaw_endpoints_extra.py`
- [x] ruff + pyright clean on changed files
- [ ] CI `build-and-test` + `auto-review` green

> Note: a single pre-existing, order-dependent failure (`test_litellm_video::test_reframe_params`, passes in isolation) is unrelated to this branch and exists on `main` — tracked separately, not introduced here.


---

