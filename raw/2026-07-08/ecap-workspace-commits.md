# SerendipityOneInc/ecap-workspace — 2026-07-08

共 22 个 commit

## `12ae4ce1` refactor(web): extract useChatSSE from useSendMessage (F1 slice 2) (#2785)

- **作者**: bill-srp
- **日期**: 2026-07-08T13:21:54Z
- **SHA**: 12ae4ce14fed87a5f566954f2324bb9e35096063

### 完整 Commit Message

```
refactor(web): extract useChatSSE from useSendMessage (F1 slice 2) (#2785)

## Summary

**Slice 2 of the F1 split** from arch-review issue #2553 (follows #2784,
which extracted `useMessageQueue`). This slice extracts the **SSE stream
lifecycle** from `useSendMessage.ts` (547 → 200 lines) into a co-located
`useChatSSE.ts` (383 lines).

Moved into `useChatSSE`:

- `useSSEStream` setup, callback wiring, `closeSSE` / `recoverSSE`
- stream state (`streamStateRef`: content accumulation, has-received
flag)
- SSE message parsing (function calls/responses, thinking states, text
accumulation)
- stream completion handling (empty-response capture + refresh fallback,
progress cleanup)
- stream error handling
- insufficient-credit SSE fallback lifecycle cleanup + optimistic
rollback (via the injected `messageQueue`)
- `startChatStream` (lifecycle reset + Sentry trace start +
`startStream`)
- Sentry tracing refs (`chatTraceRef`, `latencyTraceRef`) — trace start
/ first delta / complete / empty-capture / error are all
stream-lifecycle events, so the refs live with the stream

Credit/auth logic **stays in `useSendMessage`** (slice 3 target),
connected through two callback seams:

- `onStreamComplete` → `triggerCreditsRefresh()` + Billing Gateway log
- `onInsufficientCredits` → warning log +
`setShowInsufficientCreditsModal(true)`

Auth/credit pre-checks, `interrupt`, and the progress-timer setup remain
in `useSendMessage`. Its public API is unchanged (`sendMessage`,
`closeSSE`, `recoverSSE`, `interrupt`, `currentJobId`, `isInterrupting`
— verified against the `index.tsx` consumer). `useMessageQueue.ts`
untouched. Handler internals (completion ordering, error flags, rollback
conditions) reviewed line-for-line against the pre-refactor code — no
drift.

Remaining slices: `useCreditDeduction` (slice 3), `useSession` split
(slice 4).

## Test plan

- [x] New unit spec: `useChatSSE.unit.spec.ts` (written red-first
against the missing hook)
- [x] All 14 spec files exercising `agent-chat-client` pass (158 tests),
including existing `useSendMessage.unit.spec.ts` and
`useMessageQueue.unit.spec.ts`
- [x] `bash scripts/verify-web.sh` on touched paths — guards + `tsc` +
vitest + `eslint` pass
- [ ] CI `code-quality / lint-and-test`
```

### PR Description

## Summary

**Slice 2 of the F1 split** from arch-review issue #2553 (follows #2784, which extracted `useMessageQueue`). This slice extracts the **SSE stream lifecycle** from `useSendMessage.ts` (547 → 200 lines) into a co-located `useChatSSE.ts` (383 lines).

Moved into `useChatSSE`:

- `useSSEStream` setup, callback wiring, `closeSSE` / `recoverSSE`
- stream state (`streamStateRef`: content accumulation, has-received flag)
- SSE message parsing (function calls/responses, thinking states, text accumulation)
- stream completion handling (empty-response capture + refresh fallback, progress cleanup)
- stream error handling
- insufficient-credit SSE fallback lifecycle cleanup + optimistic rollback (via the injected `messageQueue`)
- `startChatStream` (lifecycle reset + Sentry trace start + `startStream`)
- Sentry tracing refs (`chatTraceRef`, `latencyTraceRef`) — trace start / first delta / complete / empty-capture / error are all stream-lifecycle events, so the refs live with the stream

Credit/auth logic **stays in `useSendMessage`** (slice 3 target), connected through two callback seams:

- `onStreamComplete` → `triggerCreditsRefresh()` + Billing Gateway log
- `onInsufficientCredits` → warning log + `setShowInsufficientCreditsModal(true)`

Auth/credit pre-checks, `interrupt`, and the progress-timer setup remain in `useSendMessage`. Its public API is unchanged (`sendMessage`, `closeSSE`, `recoverSSE`, `interrupt`, `currentJobId`, `isInterrupting` — verified against the `index.tsx` consumer). `useMessageQueue.ts` untouched. Handler internals (completion ordering, error flags, rollback conditions) reviewed line-for-line against the pre-refactor code — no drift.

Remaining slices: `useCreditDeduction` (slice 3), `useSession` split (slice 4).

## Test plan

- [x] New unit spec: `useChatSSE.unit.spec.ts` (written red-first against the missing hook)
- [x] All 14 spec files exercising `agent-chat-client` pass (158 tests), including existing `useSendMessage.unit.spec.ts` and `useMessageQueue.unit.spec.ts`
- [x] `bash scripts/verify-web.sh` on touched paths — guards + `tsc` + vitest + `eslint` pass
- [ ] CI `code-quality / lint-and-test`


---

## `24a848f2` refactor(web): extract useMessageQueue from useSendMessage (F1 slice 1) (#2784)

- **作者**: bill-srp
- **日期**: 2026-07-08T12:53:52Z
- **SHA**: 24a848f26e15c2d46cc48c0e334683d3895ff0ba

### 完整 Commit Message

```
refactor(web): extract useMessageQueue from useSendMessage (F1 slice 1) (#2784)

## Summary

**Slice 1 of the F1 split** from arch-review issue #2553
(`agent-chat-client` core hooks stack multiple async state machines in
single files). This slice extracts only the **message-queue concern**
from `useSendMessage.ts` (699 → 547 lines) into a co-located
`useMessageQueue.ts` (224 lines). SSE lifecycle and credit logic stay in
place for later slices.

Moved into `useMessageQueue`:

- throttled assistant-message updates (250ms batching) —
`updateAssistantMessage` (was `throttledUpdateMessage`)
- optimistic user + assistant append on send — `enqueueOutgoingMessage`
- recover-path assistant placeholder — `ensureAssistantMessage`
- insufficient-credit optimistic rollback —
`rollbackLastOptimisticExchange`
- function-call append / finish / 10s auto-collapse timers —
`appendFunctionCalls`, `markFunctionCallsFinished`,
`scheduleFunctionCallCollapse`
- associated refs and unmount timer cleanup (`pendingUpdateRef`,
`updateTimerRef`, `collapseTimerRefs`, `lastUpdateTimeRef`)

Public API of `useSendMessage` is unchanged.

**One deliberate seam improvement**: at stream start,
`resetAssistantUpdateQueue()` now also cancels an in-flight throttled
update from the previous stream. Previously only the throttle timestamp
was reset, leaving a ≤250ms window where stale pending content could
leak into the new assistant message. All other logic (throttle
thresholds, timer bookkeeping, rollback conditions, collapse timing) is
line-for-line equivalent — reviewed against the pre-refactor code.

Seams left for later slices: SSE stream
parsing/recover/interrupt/completion handling (`useChatSSE` candidate),
credit pre-check + insufficient-credit modal + post-complete refresh
(`useCreditDeduction` candidate); `isMountedRef` remains owned by
`useSendMessage` since both SSE callbacks and queue timers share it.

## Test plan

- [x] New unit spec for the extracted hook:
`useMessageQueue.unit.spec.ts` (fake-timer throttle behavior)
- [x] All 13 spec files exercising `agent-chat-client` pass (155 tests),
including the existing `useSendMessage.unit.spec.ts` against the
refactored code
- [x] `bash scripts/verify-web.sh` on touched paths — guards + `tsc` +
`eslint` pass
- [ ] CI `code-quality / lint-and-test`
```

### PR Description

## Summary

**Slice 1 of the F1 split** from arch-review issue #2553 (`agent-chat-client` core hooks stack multiple async state machines in single files). This slice extracts only the **message-queue concern** from `useSendMessage.ts` (699 → 547 lines) into a co-located `useMessageQueue.ts` (224 lines). SSE lifecycle and credit logic stay in place for later slices.

Moved into `useMessageQueue`:

- throttled assistant-message updates (250ms batching) — `updateAssistantMessage` (was `throttledUpdateMessage`)
- optimistic user + assistant append on send — `enqueueOutgoingMessage`
- recover-path assistant placeholder — `ensureAssistantMessage`
- insufficient-credit optimistic rollback — `rollbackLastOptimisticExchange`
- function-call append / finish / 10s auto-collapse timers — `appendFunctionCalls`, `markFunctionCallsFinished`, `scheduleFunctionCallCollapse`
- associated refs and unmount timer cleanup (`pendingUpdateRef`, `updateTimerRef`, `collapseTimerRefs`, `lastUpdateTimeRef`)

Public API of `useSendMessage` is unchanged.

**One deliberate seam improvement**: at stream start, `resetAssistantUpdateQueue()` now also cancels an in-flight throttled update from the previous stream. Previously only the throttle timestamp was reset, leaving a ≤250ms window where stale pending content could leak into the new assistant message. All other logic (throttle thresholds, timer bookkeeping, rollback conditions, collapse timing) is line-for-line equivalent — reviewed against the pre-refactor code.

Seams left for later slices: SSE stream parsing/recover/interrupt/completion handling (`useChatSSE` candidate), credit pre-check + insufficient-credit modal + post-complete refresh (`useCreditDeduction` candidate); `isMountedRef` remains owned by `useSendMessage` since both SSE callbacks and queue timers share it.

## Test plan

- [x] New unit spec for the extracted hook: `useMessageQueue.unit.spec.ts` (fake-timer throttle behavior)
- [x] All 13 spec files exercising `agent-chat-client` pass (155 tests), including the existing `useSendMessage.unit.spec.ts` against the refactored code
- [x] `bash scripts/verify-web.sh` on touched paths — guards + `tsc` + `eslint` pass
- [ ] CI `code-quality / lint-and-test`


---

## `1cca2cba` refactor(web): split pptx-parser into types, extract, styles, and render modules (#2782)

- **作者**: bill-srp
- **日期**: 2026-07-08T12:18:48Z
- **SHA**: 1cca2cba86e85dc93874cc300c72761948a21753

### 完整 Commit Message

```
refactor(web): split pptx-parser into types, extract, styles, and render modules (#2782)

## Summary

Resolves **F2** of arch-review issue #2553 (`pptx-parser.ts` single-file
bulk with no internal layering).

Behavior-preserving split of the 1,198-line `pptx-parser.ts` by concern,
co-located under `web/app/src/components/artifacts/renderers/`:

- `pptx-types.ts` (132 lines) — type declarations
- `pptx-extract.ts` (212 lines) — PPTX XML → data model extraction
- `pptx-styles.ts` (175 lines) — theme color / font mapping (also hosts
shared OOXML namespace constants and small attr helpers, avoiding a
fifth utility module)
- `pptx-render.ts` (742 lines) — shape → output rendering
- `pptx-parser.ts` (3 lines) — public entry point re-exporting the same
API (`parsePptx`, `EMU_PER_PX`, `TextParagraph`, `ShapeTransform`,
`SlideShape`, `SlideData`)

No import sites change — a repo-wide search found no external imports of
the new modules; everything still goes through `pptx-parser.ts`. No
functional changes.

## Test plan

- [x] `bash scripts/verify-web.sh
web/app/src/components/artifacts/renderers` — guards + `tsc` + vitest +
`eslint` pass
- [x] Targeted unit tests: `pptx-parser.unit.spec.ts`,
`ArtifactPreview.unit.spec.tsx`, `ArtifactPreview-extras.unit.spec.tsx`,
`AssetPreviewArea.unit.spec.tsx` — 58 tests pass
- [ ] CI `code-quality / lint-and-test`
```

### PR Description

## Summary

Resolves **F2** of arch-review issue #2553 (`pptx-parser.ts` single-file bulk with no internal layering).

Behavior-preserving split of the 1,198-line `pptx-parser.ts` by concern, co-located under `web/app/src/components/artifacts/renderers/`:

- `pptx-types.ts` (132 lines) — type declarations
- `pptx-extract.ts` (212 lines) — PPTX XML → data model extraction
- `pptx-styles.ts` (175 lines) — theme color / font mapping (also hosts shared OOXML namespace constants and small attr helpers, avoiding a fifth utility module)
- `pptx-render.ts` (742 lines) — shape → output rendering
- `pptx-parser.ts` (3 lines) — public entry point re-exporting the same API (`parsePptx`, `EMU_PER_PX`, `TextParagraph`, `ShapeTransform`, `SlideShape`, `SlideData`)

No import sites change — a repo-wide search found no external imports of the new modules; everything still goes through `pptx-parser.ts`. No functional changes.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/src/components/artifacts/renderers` — guards + `tsc` + vitest + `eslint` pass
- [x] Targeted unit tests: `pptx-parser.unit.spec.ts`, `ArtifactPreview.unit.spec.tsx`, `ArtifactPreview-extras.unit.spec.tsx`, `AssetPreviewArea.unit.spec.tsx` — 58 tests pass
- [ ] CI `code-quality / lint-and-test`


---

## `b57f6815` style(ios): simplify Zooclaw chat and sidebar UI (#2776)

- **作者**: shana-srp
- **日期**: 2026-07-08T12:10:28Z
- **SHA**: b57f68158b7f057ee0a040a085aa07d951ba0c07

### 完整 Commit Message

```
style(ios): simplify Zooclaw chat and sidebar UI (#2776)

Summary:
- Remove the My Specialist Team header and add button from the left
sidebar.
- Set the sidebar brand logo height to 40pt.
- Replace chat wallpaper rendering with a solid #F8F8F7 background.

Tests:
- git diff --check origin/main...HEAD
- xcodebuild Release simulator build for ZooClaw on iPhone 17 Pro iOS
26.5: passed

Notes:
- Build still emits existing Swift 6 actor-isolation and
dSYM/module-cache warnings unrelated to this UI change.

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR Description

Summary:
- Remove the My Specialist Team header and add button from the left sidebar.
- Set the sidebar brand logo height to 40pt.
- Replace chat wallpaper rendering with a solid #F8F8F7 background.

Tests:
- git diff --check origin/main...HEAD
- xcodebuild Release simulator build for ZooClaw on iPhone 17 Pro iOS 26.5: passed

Notes:
- Build still emits existing Swift 6 actor-isolation and dSYM/module-cache warnings unrelated to this UI change.

---

## `2eea979a` feat(claw-interface): add /internal/users admin read routes (list, orders, events) (#2781)

- **作者**: bill-srp
- **日期**: 2026-07-08T12:02:26Z
- **SHA**: 2eea979a378babef005ef7a63bb822688be3a575

### 完整 Commit Message

```
feat(claw-interface): add /internal/users admin read routes (list, orders, events) (#2781)

## Linear
<!-- Internal staff-admin relocation; no dedicated Linear issue. -->

## Summary

Second backend slice of the **staff-admin relocation** program (Plan 1 =
`/internal/subscription-codes` + `/internal/releases`, merged in #2774).
This is **Plan 2a — the read-only Users endpoints** for the
`dashboard-console` Users page:

- **`GET /internal/users`** — list users with the same filters as the
legacy `/users/list` (uid / user_type / email / phone /
subscription_status / created_before / limit / offset).
- **`GET /internal/users/{uid}/orders`** — a user's order history.
- **`GET /internal/users/{uid}/events`** — a user's billing events (Lago
passthrough).

All three follow the merged Plan 1 pattern: thin route handlers under
the `@srp.one`-gated `/internal` router (this sub-router adds
`Depends(require_admin_user)`), delegating to **FastAPI-free services**
(`app/services/user/list_service.py`, `order_history.py`,
`customer_events.py`) that raise `app.errors` domain errors — routes
never touch repos or raise `HTTPException`. `import-linter` confirms
**C2 (layering)** and **C3 (services never import FastAPI)**.

**Scope:** reads only. The credits-balance read + `grant credits` +
`boost subscription` mutations are **Plan 2b** (billing-critical —
entitlement idempotency / double-grant — handled in a separate focused
PR). Legacy routes (`/users/list`, `/orders/list`,
`/admin/users/{uid}/events`) are **untouched** and retire at the web/app
teardown phase.

## Test plan

- [x] 8 unit tests (`tests/unit/test_internal_users_routes.py`) — list
happy-path + bad-subscription-status → `DomainValidationError`; orders
happy-path + missing-user → `NotFoundError`; events passthrough +
missing-gateway → `DependencyNotReadyError` + missing-user →
`NotFoundError` + no-customer → empty envelope.
- [x] `ruff check` + `ruff format --check` clean
- [x] `pyright` clean — 0 errors (app **and** tests)
- [x] `import-linter` — 8/8 contracts kept (C2 + C3)
- [ ] CI: whole-app `pytest` + 90% coverage gate, `web-build-check`,
CodeQL (run on PR)
```

### PR Description

## Linear
<!-- Internal staff-admin relocation; no dedicated Linear issue. -->

## Summary

Second backend slice of the **staff-admin relocation** program (Plan 1 = `/internal/subscription-codes` + `/internal/releases`, merged in #2774). This is **Plan 2a — the read-only Users endpoints** for the `dashboard-console` Users page:

- **`GET /internal/users`** — list users with the same filters as the legacy `/users/list` (uid / user_type / email / phone / subscription_status / created_before / limit / offset).
- **`GET /internal/users/{uid}/orders`** — a user's order history.
- **`GET /internal/users/{uid}/events`** — a user's billing events (Lago passthrough).

All three follow the merged Plan 1 pattern: thin route handlers under the `@srp.one`-gated `/internal` router (this sub-router adds `Depends(require_admin_user)`), delegating to **FastAPI-free services** (`app/services/user/list_service.py`, `order_history.py`, `customer_events.py`) that raise `app.errors` domain errors — routes never touch repos or raise `HTTPException`. `import-linter` confirms **C2 (layering)** and **C3 (services never import FastAPI)**.

**Scope:** reads only. The credits-balance read + `grant credits` + `boost subscription` mutations are **Plan 2b** (billing-critical — entitlement idempotency / double-grant — handled in a separate focused PR). Legacy routes (`/users/list`, `/orders/list`, `/admin/users/{uid}/events`) are **untouched** and retire at the web/app teardown phase.

## Test plan

- [x] 8 unit tests (`tests/unit/test_internal_users_routes.py`) — list happy-path + bad-subscription-status → `DomainValidationError`; orders happy-path + missing-user → `NotFoundError`; events passthrough + missing-gateway → `DependencyNotReadyError` + missing-user → `NotFoundError` + no-customer → empty envelope.
- [x] `ruff check` + `ruff format --check` clean
- [x] `pyright` clean — 0 errors (app **and** tests)
- [x] `import-linter` — 8/8 contracts kept (C2 + C3)
- [ ] CI: whole-app `pytest` + 90% coverage gate, `web-build-check`, CodeQL (run on PR)


---

## `a9afd247` fix(whatsapp): add root health route (#2780)

- **作者**: bill-srp
- **日期**: 2026-07-08T11:49:11Z
- **SHA**: a9afd2479fac2ee3deb5cd9762eb258c0a138b87

### 完整 Commit Message

```
fix(whatsapp): add root health route (#2780)

## Summary
- Add `GET /` to `whatsapp-business-service` so external card checks
receive HTTP 200.
- Reuse the existing service status response for both `/` and
`/healthz`.
- Document the new root route in the service README.

## Root cause
External card checks hit the service root path, but the Fastify app only
exposed `/healthz` and webhook routes. `GET /` fell through to the
not-found handler and returned 404.

## Test plan
- [x] `./node_modules/.bin/vitest run src/app.test.ts`
- [x] `./node_modules/.bin/tsc --noEmit`
- [x] `bash scripts/verify-changed.sh`
```

### PR Description

## Summary
- Add `GET /` to `whatsapp-business-service` so external card checks receive HTTP 200.
- Reuse the existing service status response for both `/` and `/healthz`.
- Document the new root route in the service README.

## Root cause
External card checks hit the service root path, but the Fastify app only exposed `/healthz` and webhook routes. `GET /` fell through to the not-found handler and returned 404.

## Test plan
- [x] `./node_modules/.bin/vitest run src/app.test.ts`
- [x] `./node_modules/.bin/tsc --noEmit`
- [x] `bash scripts/verify-changed.sh`


---

## `c43445a5` refactor(web): extract AddChannelModal logic into useAddChannelForm hook (#2779)

- **作者**: bill-srp
- **日期**: 2026-07-08T11:40:17Z
- **SHA**: c43445a55e0d032b30e8d813e5bf80aadf4d78a1

### 完整 Commit Message

```
refactor(web): extract AddChannelModal logic into useAddChannelForm hook (#2779)

## Summary

Resolves **F3** of arch-review issue #2553 (`AddChannelModal` business
logic coupled to the rendering layer).

- Extract all data/business logic from `AddChannelModal.tsx` (716 → 72
lines) into a co-located `useAddChannelForm.ts` hook:
  - platform / account / agent / policy form state
  - guided / manual / QR step state machine
  - validation and required-field derivation
  - submit payload construction and `onAdd` handling
  - setup dispatch handlers and MS Teams endpoint copy state
- Move presentational sub-sections into `AddChannelModalParts.tsx`; the
modal component itself keeps only JSX composition.
- Add a dedicated unit spec for the hook
(`useAddChannelForm.unit.spec.tsx`), addressing the "logic can't be
tested in isolation" half of the finding.

Note: the finding's mention of `useQuery`/`useMutation` inside the modal
is stale — current code already receives `onAdd` from callers; that API
boundary is preserved. Behavior-preserving refactor, no functional
changes.

## Test plan

- [x] `bash scripts/verify-web.sh` on touched paths — guards + `tsc` +
`eslint` pass
- [x] Targeted vitest run: 29 files / 570 tests pass (includes new
`useAddChannelForm.unit.spec.tsx` plus existing `ChannelsSection`
behavior specs)
- [ ] CI `code-quality / lint-and-test`
```

### PR Description

## Summary

Resolves **F3** of arch-review issue #2553 (`AddChannelModal` business logic coupled to the rendering layer).

- Extract all data/business logic from `AddChannelModal.tsx` (716 → 72 lines) into a co-located `useAddChannelForm.ts` hook:
  - platform / account / agent / policy form state
  - guided / manual / QR step state machine
  - validation and required-field derivation
  - submit payload construction and `onAdd` handling
  - setup dispatch handlers and MS Teams endpoint copy state
- Move presentational sub-sections into `AddChannelModalParts.tsx`; the modal component itself keeps only JSX composition.
- Add a dedicated unit spec for the hook (`useAddChannelForm.unit.spec.tsx`), addressing the "logic can't be tested in isolation" half of the finding.

Note: the finding's mention of `useQuery`/`useMutation` inside the modal is stale — current code already receives `onAdd` from callers; that API boundary is preserved. Behavior-preserving refactor, no functional changes.

## Test plan

- [x] `bash scripts/verify-web.sh` on touched paths — guards + `tsc` + `eslint` pass
- [x] Targeted vitest run: 29 files / 570 tests pass (includes new `useAddChannelForm.unit.spec.tsx` plus existing `ChannelsSection` behavior specs)
- [ ] CI `code-quality / lint-and-test`


---

## `7340c9f3` feat(claw-interface): add admin /internal subscription-codes and releases routes (#2774)

- **作者**: bill-srp
- **日期**: 2026-07-08T11:12:35Z
- **SHA**: 7340c9f3020d12c3e6655587bcd9f7267cb0f94f

### 完整 Commit Message

```
feat(claw-interface): add admin /internal subscription-codes and releases routes (#2774)

## Linear
<!-- Internal cleanup/relocation; no dedicated Linear issue. -->

## Summary

First backend slice of **relocating staff admin from the `web/app`
`/admin` dashboard into the `dashboard-console` staff console** (design
spec + full plan included in this PR under `docs/superpowers/`).

Adds two admin-only routers under the existing `/internal` router
(already gated to `@srp.one` via `require_srp_account`); each new
sub-router adds `Depends(require_admin_user)`. Handlers are thin and
reuse existing repos — no business logic duplicated into routes.

- **`/internal/subscription-codes`** — `GET` (paginated list) + `POST`
(create). Reuses `gift_code_repo` (subscription codes live in the
gift-code collection with `category="subscription"`).
- **`/internal/releases`** — `GET` (list), `POST` (create), and action
sub-paths `POST /{version}/delete`, `/set-latest`, `/publish`,
`/unpublish`. Reuses `release_repo`.

Conventions:
- **GET/POST only** — no `DELETE`/`PUT`/`PATCH`;
deletes/state-transitions are `POST` action sub-paths (spec decision
#8).
- These new `/internal/*` endpoints are how the browser-only console (no
BFF) reaches the backend directly under the staff gate; the existing
`/admin/*` + `/openclaw/admin/releases` routes are **not** touched here
and are retired in a later teardown phase.

Also bundles two earlier `claw-interface-cleanup` commits already on
this branch: remove unused web api routes, remove unused internal
catalog routes.

## Test plan

- [x] 15 new unit tests pass
(`test_internal_subscription_codes_routes.py`,
`test_internal_releases_routes.py`) —
list/create/delete/set-latest/publish/unpublish happy paths +
404/409/400/duplicate cases, admin-gated.
- [x] `ruff check` + `ruff format --check` clean
- [x] `pyright` clean (0 errors)
- [x] `import-linter` — 8/8 architecture contracts kept
- [ ] CI: whole-app `pytest` + 90% coverage gate, `web-build-check`,
CodeQL (run on PR)

> Note: branch is behind `origin/main`; if CI's merge preview drifts,
reconcile by merging `origin/main` in (force-push is blocked on this
branch).
```

### PR Description

## Linear
<!-- Internal cleanup/relocation; no dedicated Linear issue. -->

## Summary

First backend slice of **relocating staff admin from the `web/app` `/admin` dashboard into the `dashboard-console` staff console** (design spec + full plan included in this PR under `docs/superpowers/`).

Adds two admin-only routers under the existing `/internal` router (already gated to `@srp.one` via `require_srp_account`); each new sub-router adds `Depends(require_admin_user)`. Handlers are thin and reuse existing repos — no business logic duplicated into routes.

- **`/internal/subscription-codes`** — `GET` (paginated list) + `POST` (create). Reuses `gift_code_repo` (subscription codes live in the gift-code collection with `category="subscription"`).
- **`/internal/releases`** — `GET` (list), `POST` (create), and action sub-paths `POST /{version}/delete`, `/set-latest`, `/publish`, `/unpublish`. Reuses `release_repo`.

Conventions:
- **GET/POST only** — no `DELETE`/`PUT`/`PATCH`; deletes/state-transitions are `POST` action sub-paths (spec decision #8).
- These new `/internal/*` endpoints are how the browser-only console (no BFF) reaches the backend directly under the staff gate; the existing `/admin/*` + `/openclaw/admin/releases` routes are **not** touched here and are retired in a later teardown phase.

Also bundles two earlier `claw-interface-cleanup` commits already on this branch: remove unused web api routes, remove unused internal catalog routes.

## Test plan

- [x] 15 new unit tests pass (`test_internal_subscription_codes_routes.py`, `test_internal_releases_routes.py`) — list/create/delete/set-latest/publish/unpublish happy paths + 404/409/400/duplicate cases, admin-gated.
- [x] `ruff check` + `ruff format --check` clean
- [x] `pyright` clean (0 errors)
- [x] `import-linter` — 8/8 architecture contracts kept
- [ ] CI: whole-app `pytest` + 90% coverage gate, `web-build-check`, CodeQL (run on PR)

> Note: branch is behind `origin/main`; if CI's merge preview drifts, reconcile by merging `origin/main` in (force-push is blocked on this branch).


---

## `b3ea7646` feat(claw-interface): expose agent pack versions route (#2773)

- **作者**: bill-srp
- **日期**: 2026-07-08T11:10:53Z
- **SHA**: b3ea764623542f5acb66a46ff0391ea720c8d2c2

### 完整 Commit Message

```
feat(claw-interface): expose agent pack versions route (#2773)

## Linear

N/A

## Summary
- Add `GET /agent-packs/{pack_id}/versions` for authenticated public
ZooClaw agent-pack version history.
- Return a public allowlist DTO for approved versions only, scoped to
active catalog-visible ZooClaw packs.
- Cover route wiring, auth dependency, response model, visibility
filtering, and sensitive-field exclusion in public agent-pack route
tests.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_public_agent_packs_routes.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-changed.sh`
```

### PR Description

## Linear

N/A

## Summary
- Add `GET /agent-packs/{pack_id}/versions` for authenticated public ZooClaw agent-pack version history.
- Return a public allowlist DTO for approved versions only, scoped to active catalog-visible ZooClaw packs.
- Cover route wiring, auth dependency, response model, visibility filtering, and sensitive-field exclusion in public agent-pack route tests.

## Test plan
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_public_agent_packs_routes.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-changed.sh`


---

## `c5dceb46` refactor(web): decompose useSubscriptionActions into focused sub-hooks (#2778)

- **作者**: bill-srp
- **日期**: 2026-07-08T10:58:25Z
- **SHA**: c5dceb46ca5833b24d6d62f6c75bcb4214c44d17

### 完整 Commit Message

```
refactor(web): decompose useSubscriptionActions into focused sub-hooks (#2778)

## Summary
- Decompose the 631-line `useSubscriptionActions` hook into three
focused sub-hooks, resolving arch-review finding **F5** from #2648
(Complexity):
- `useCheckoutFlow.ts` (313 lines) — checkout/topup/upgrade mutations,
payment-method modal state machine
- `useSubscriptionLifecycle.ts` (225 lines) — renew, downgrade,
cancel-downgrade, cancel-subscription mutations
- `useCustomerPortal.ts` (71 lines) — customer-portal mutation
(previously an internal function)
- `useSubscriptionActions.ts` (now 174 lines) remains as the composing
hook with an **identical public API**. All shared state
(`paymentMethodPending`, `topupPending`, `downgradeTarget`, cancel modal
state) stays in the composing hook and is passed to sub-hooks explicitly
— nothing duplicated.
- Pure structural refactor of payment code (Stripe + Antom): mutation
logic moved verbatim (`mutationFn`/`mutate`/`mutateAsync` counts
identical before/after), every onSuccess/onError/invalidation path
preserved. `SubscriptionPanel.tsx` and all test files are byte-for-byte
unchanged.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/components/billing` — tsc,
eslint, vitest all pass (232 passed, 1 skipped) with zero test-file
modifications
- [x] `SubscriptionPanel.tsx` unmodified (`git diff --quiet` clean) —
existing panel tests exercise the composed hook unchanged
- [ ] CI green
```

### PR Description

## Summary
- Decompose the 631-line `useSubscriptionActions` hook into three focused sub-hooks, resolving arch-review finding **F5** from #2648 (Complexity):
  - `useCheckoutFlow.ts` (313 lines) — checkout/topup/upgrade mutations, payment-method modal state machine
  - `useSubscriptionLifecycle.ts` (225 lines) — renew, downgrade, cancel-downgrade, cancel-subscription mutations
  - `useCustomerPortal.ts` (71 lines) — customer-portal mutation (previously an internal function)
- `useSubscriptionActions.ts` (now 174 lines) remains as the composing hook with an **identical public API**. All shared state (`paymentMethodPending`, `topupPending`, `downgradeTarget`, cancel modal state) stays in the composing hook and is passed to sub-hooks explicitly — nothing duplicated.
- Pure structural refactor of payment code (Stripe + Antom): mutation logic moved verbatim (`mutationFn`/`mutate`/`mutateAsync` counts identical before/after), every onSuccess/onError/invalidation path preserved. `SubscriptionPanel.tsx` and all test files are byte-for-byte unchanged.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/components/billing` — tsc, eslint, vitest all pass (232 passed, 1 skipped) with zero test-file modifications
- [x] `SubscriptionPanel.tsx` unmodified (`git diff --quiet` clean) — existing panel tests exercise the composed hook unchanged
- [ ] CI green


---

## `47952e8c` refactor(web): split cronHelpers into types, format, and schedule modules (#2777)

- **作者**: bill-srp
- **日期**: 2026-07-08T10:57:24Z
- **SHA**: 47952e8cfe5246844ce5d8e92c63aa92b86948bb

### 完整 Commit Message

```
refactor(web): split cronHelpers into types, format, and schedule modules (#2777)

## Summary
- Split the 624-line mixed-concern `schedule/cronHelpers.ts` into three
focused modules in the same directory, resolving arch-review finding
**F7** from #2648 (Separation of Concerns):
- `cron-types.ts` — all exported type/interface declarations (`CronJob`,
`FormState`, …), dependency-free
- `cron-format.ts` — formatting, token/cost, form conversion, and
calendar helpers
- `cron-schedule.ts` — cron expression parsing and fire-time computation
- Pure mechanical move: code transferred verbatim, zero behavior
changes. All consumers (5 schedule components, `useCronJobs`, and unit
tests) now import from the new modules directly; `cronHelpers.ts` is
deleted with zero remaining references.
- The legacy complexity override for the deleted file in
`eslint.config.mjs` follows the moved runtime code (one entry → two);
two doc comments in `lib/query/` that referenced `cronHelpers` were
updated.

## Test plan
- [x] `bash scripts/verify-web.sh
"web/app/src/app/[locale]/(app)/(chat)/schedule" ...` — tsc, eslint,
vitest all pass (221 passed, 1 todo)
- [x] `rg cronHelpers web/app` returns zero matches
- [ ] CI green
```

### PR Description

## Summary
- Split the 624-line mixed-concern `schedule/cronHelpers.ts` into three focused modules in the same directory, resolving arch-review finding **F7** from #2648 (Separation of Concerns):
  - `cron-types.ts` — all exported type/interface declarations (`CronJob`, `FormState`, …), dependency-free
  - `cron-format.ts` — formatting, token/cost, form conversion, and calendar helpers
  - `cron-schedule.ts` — cron expression parsing and fire-time computation
- Pure mechanical move: code transferred verbatim, zero behavior changes. All consumers (5 schedule components, `useCronJobs`, and unit tests) now import from the new modules directly; `cronHelpers.ts` is deleted with zero remaining references.
- The legacy complexity override for the deleted file in `eslint.config.mjs` follows the moved runtime code (one entry → two); two doc comments in `lib/query/` that referenced `cronHelpers` were updated.

## Test plan
- [x] `bash scripts/verify-web.sh "web/app/src/app/[locale]/(app)/(chat)/schedule" ...` — tsc, eslint, vitest all pass (221 passed, 1 todo)
- [x] `rg cronHelpers web/app` returns zero matches
- [ ] CI green


---

## `d03c61d4` refactor(web): migrate openclaw api clients to callClawInterfaceAPI (#2775)

- **作者**: bill-srp
- **日期**: 2026-07-08T10:56:34Z
- **SHA**: d03c61d43a7245feb9de45b292c79c4c1b89f2a5

### 完整 Commit Message

```
refactor(web): migrate openclaw api clients to callClawInterfaceAPI (#2775)

## Summary
- Migrate the remaining bare `fetch('/api/openclaw/...')` calls in
`web/app/src/lib/api/openclaw.ts` and `openclaw-settings.ts` to the
shared `callClawInterfaceAPI` helper, resolving arch-review finding
**F6** from #2648 (dual-track HTTP call patterns).
- Each call keeps its previous semantics: endpoint mappings mirror what
the bypassed Next proxy routes forwarded to
(`/openclaw/conversation/tasks`, `/openclaw/cron/jobs/{jobId}/runs`,
`/openclaw/settings/...`), and per-call timeouts are preserved (e.g.
3-minute agent deployment, 15s task clearing).
- Intentional exception: `updateClawLocale` stays on its Next route
`/api/openclaw/settings/locale` because that route enriches a missing
`country` from Cloudflare's `cf-ipcountry` header, which a direct
backend call cannot replicate. A comment in the code documents this.
- Unit tests updated to assert the new `/api/claw/openclaw/...` request
URLs, methods, query params, and JSON bodies; test intent
(success/error/timeout paths) unchanged.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/openclaw.ts
web/app/src/lib/api/openclaw-settings.ts` — tsc, eslint, vitest all pass
(617/617 tests, 52 files)
- [x] Endpoint remappings cross-checked against the corresponding
`web/app/src/app/api/openclaw/*` route handlers
- [ ] CI green (`code-quality / lint-and-test`)
```

### PR Description

## Summary
- Migrate the remaining bare `fetch('/api/openclaw/...')` calls in `web/app/src/lib/api/openclaw.ts` and `openclaw-settings.ts` to the shared `callClawInterfaceAPI` helper, resolving arch-review finding **F6** from #2648 (dual-track HTTP call patterns).
- Each call keeps its previous semantics: endpoint mappings mirror what the bypassed Next proxy routes forwarded to (`/openclaw/conversation/tasks`, `/openclaw/cron/jobs/{jobId}/runs`, `/openclaw/settings/...`), and per-call timeouts are preserved (e.g. 3-minute agent deployment, 15s task clearing).
- Intentional exception: `updateClawLocale` stays on its Next route `/api/openclaw/settings/locale` because that route enriches a missing `country` from Cloudflare's `cf-ipcountry` header, which a direct backend call cannot replicate. A comment in the code documents this.
- Unit tests updated to assert the new `/api/claw/openclaw/...` request URLs, methods, query params, and JSON bodies; test intent (success/error/timeout paths) unchanged.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/lib/api/openclaw.ts web/app/src/lib/api/openclaw-settings.ts` — tsc, eslint, vitest all pass (617/617 tests, 52 files)
- [x] Endpoint remappings cross-checked against the corresponding `web/app/src/app/api/openclaw/*` route handlers
- [ ] CI green (`code-quality / lint-and-test`)


---

## `1d72abcd` fix(app): improve chat status dropdown readability (#2772)

- **作者**: lynn Zhuang
- **日期**: 2026-07-08T09:13:45Z
- **SHA**: 1d72abcd7dbe07ae3d1419afe68104b721aea576

### 完整 Commit Message

```
fix(app): improve chat status dropdown readability (#2772)

## Summary
- Make the chat header connection dropdown use a readable frosted
popover surface.
- Add unit coverage that pins the dropdown background, blur, and
foreground color contract.

## Root cause
The connection dropdown used a plain opaque-token class without the
frosted surface treatment needed on liquid-glass chat pages. When the
panel overlapped chat content, background text could visually bleed
through and make dropdown text hard to read.

## Test plan
- [x] `bash scripts/verify-local.sh --web-static
web/app/src/components/ClawConnectionStatus.tsx
web/app/tests/unit/components/ClawPageHeader-extras.unit.spec.tsx`
- [x] Local mock preview at `http://localhost:3002/chat`; captured the
opened dropdown and confirmed `bg-popover/95` computes to 95% light
popover background with `blur(24px) saturate(1.5)`.

![Uploading screenshot-20260708-170224.png…]()

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro-2.local>
```

### PR Description

## Summary
- Make the chat header connection dropdown use a readable frosted popover surface.
- Add unit coverage that pins the dropdown background, blur, and foreground color contract.

## Root cause
The connection dropdown used a plain opaque-token class without the frosted surface treatment needed on liquid-glass chat pages. When the panel overlapped chat content, background text could visually bleed through and make dropdown text hard to read.

## Test plan
- [x] `bash scripts/verify-local.sh --web-static web/app/src/components/ClawConnectionStatus.tsx web/app/tests/unit/components/ClawPageHeader-extras.unit.spec.tsx`
- [x] Local mock preview at `http://localhost:3002/chat`; captured the opened dropdown and confirmed `bg-popover/95` computes to 95% light popover background with `blur(24px) saturate(1.5)`.

![Uploading screenshot-20260708-170224.png…]()



---

## `080f0e41` feat(billing): expose offline admin expiry flow (#2767)

- **作者**: bill-srp
- **日期**: 2026-07-08T09:01:45Z
- **SHA**: 080f0e4133ab515a8f5ecbf3fa6b096e9fdacba1

### 完整 Commit Message

```
feat(billing): expose offline admin expiry flow (#2767)

## Summary

- split admin/expiry integration layer out of PR #2753
- expose admin offline order routes after the foundation and lifecycle
service are present
- wire offline agreement expiry into subscription maintenance and
current-access projection

## Stack

1. `feat/offline-payment-foundation`: foundation
2. `feat/offline-payment-core`: lifecycle service
3. This PR: admin routes and expiry integration, base
`feat/offline-payment-core`

## Local verification

- `/Users/bill/.venvs/claw-interface/bin/pytest
tests/unit/test_offline_expiry.py
tests/unit/test_offline_orders_routes.py
tests/unit/test_billing_summary_v2.py
tests/unit/test_billing_v2_subscription_cron.py`
- `env VIRTUAL_ENV=/Users/bill/.venvs/claw-interface
PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
```

### PR Description

## Summary

- split admin/expiry integration layer out of PR #2753
- expose admin offline order routes after the foundation and lifecycle service are present
- wire offline agreement expiry into subscription maintenance and current-access projection

## Stack

1. `feat/offline-payment-foundation`: foundation
2. `feat/offline-payment-core`: lifecycle service
3. This PR: admin routes and expiry integration, base `feat/offline-payment-core`

## Local verification

- `/Users/bill/.venvs/claw-interface/bin/pytest tests/unit/test_offline_expiry.py tests/unit/test_offline_orders_routes.py tests/unit/test_billing_summary_v2.py tests/unit/test_billing_v2_subscription_cron.py`
- `env VIRTUAL_ENV=/Users/bill/.venvs/claw-interface PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`


---

## `e6d5801d` ci(whatsapp): split whatsapp-business deploy into its own workflow (#2771)

- **作者**: bill-srp
- **日期**: 2026-07-08T07:52:50Z
- **SHA**: e6d5801db132d68c95dd365f8a12c33e234c7655

### 完整 Commit Message

```
ci(whatsapp): split whatsapp-business deploy into its own workflow (#2771)

<!-- PR 标题：type(scope): description -->

## Summary

- Split the WhatsApp Business bridge deploy out of `service-deploy.yml`
into its own **`.github/workflows/deploy-whatsapp-business.yml`**, so
`whatsapp-business-service` deploys independently of `claw-interface`.
- **Behavior is unchanged** — the 6 WhatsApp jobs were moved verbatim
(verified byte-identical to the originals):
  - `build-and-push-whatsapp-business-image` (tag-driven)
- `whatsapp-business-staging-changes` +
`build-and-push-whatsapp-business-staging-image` (main-push, gated by
the `services/whatsapp-business-service/**` paths-filter)
  - `deploy-whatsapp-business-to-{dev,staging,production}`
- Same triggers (`whatsapp-business-service-v*.*.*-{alpha,beta,release}`
tags + `main`-push staging), same GKE targets, image, deployment name,
and best-effort restart-recovery semantics.
- `service-deploy.yml` is now **claw-interface-only** (dropped the
WhatsApp tag patterns, the `WHATSAPP_BUSINESS_IMAGE_NAME` env var, and
the 6 jobs — 269 pure deletions, no claw-interface job touched). Its
notify / release / badge jobs never referenced WhatsApp and are
untouched.
- Docs: updated `architecture.md`, `architecture.zh-CN.md`, and the
README workflow/tag tables to point at the new workflow.

### Expected, intentional side effect

Every `main` push now shows **two** deploy runs — `Service Build and
Deploy` and `WhatsApp Business Build and Deploy` — instead of one run
with skipped jobs. The WhatsApp run still gates its build behind the
paths-filter, so when nothing under
`services/whatsapp-business-service/**` changed it just skips. Net
deploy behavior is identical.

### No manual dispatch (by design)

The WhatsApp jobs were already guarded `github.event_name !=
'workflow_dispatch'`, so they never responded to manual dispatch. The
new workflow omits `workflow_dispatch` to preserve that exact behavior.
(Adding a manual-redeploy button was considered and deliberately left
out to keep this a pure, no-behavior-change split.)

## Test plan

- [x] Both workflows parse as valid YAML; no dangling `needs`; all
`env.*` references satisfied.
- [x] `actionlint` clean — the only diagnostics are the pre-existing
`blacksmith-*` self-hosted runner-label false-positives that fire
identically on the unchanged `service-deploy.yml`.
- [x] Byte-compared each of the 6 moved jobs against the originals
removed from `service-deploy.yml` — identical.
- [ ] After merge: confirm a `main` push triggers `WhatsApp Business
Build and Deploy`, and that it skips build/deploy when no
`services/whatsapp-business-service/**` change is present.
- [ ] After merge: confirm a `whatsapp-business-service-v*.*.*-beta` tag
runs the new workflow end-to-end to staging.
```

### PR Description

<!-- PR 标题：type(scope): description -->

## Summary

- Split the WhatsApp Business bridge deploy out of `service-deploy.yml` into its own **`.github/workflows/deploy-whatsapp-business.yml`**, so `whatsapp-business-service` deploys independently of `claw-interface`.
- **Behavior is unchanged** — the 6 WhatsApp jobs were moved verbatim (verified byte-identical to the originals):
  - `build-and-push-whatsapp-business-image` (tag-driven)
  - `whatsapp-business-staging-changes` + `build-and-push-whatsapp-business-staging-image` (main-push, gated by the `services/whatsapp-business-service/**` paths-filter)
  - `deploy-whatsapp-business-to-{dev,staging,production}`
- Same triggers (`whatsapp-business-service-v*.*.*-{alpha,beta,release}` tags + `main`-push staging), same GKE targets, image, deployment name, and best-effort restart-recovery semantics.
- `service-deploy.yml` is now **claw-interface-only** (dropped the WhatsApp tag patterns, the `WHATSAPP_BUSINESS_IMAGE_NAME` env var, and the 6 jobs — 269 pure deletions, no claw-interface job touched). Its notify / release / badge jobs never referenced WhatsApp and are untouched.
- Docs: updated `architecture.md`, `architecture.zh-CN.md`, and the README workflow/tag tables to point at the new workflow.

### Expected, intentional side effect

Every `main` push now shows **two** deploy runs — `Service Build and Deploy` and `WhatsApp Business Build and Deploy` — instead of one run with skipped jobs. The WhatsApp run still gates its build behind the paths-filter, so when nothing under `services/whatsapp-business-service/**` changed it just skips. Net deploy behavior is identical.

### No manual dispatch (by design)

The WhatsApp jobs were already guarded `github.event_name != 'workflow_dispatch'`, so they never responded to manual dispatch. The new workflow omits `workflow_dispatch` to preserve that exact behavior. (Adding a manual-redeploy button was considered and deliberately left out to keep this a pure, no-behavior-change split.)

## Test plan

- [x] Both workflows parse as valid YAML; no dangling `needs`; all `env.*` references satisfied.
- [x] `actionlint` clean — the only diagnostics are the pre-existing `blacksmith-*` self-hosted runner-label false-positives that fire identically on the unchanged `service-deploy.yml`.
- [x] Byte-compared each of the 6 moved jobs against the originals removed from `service-deploy.yml` — identical.
- [ ] After merge: confirm a `main` push triggers `WhatsApp Business Build and Deploy`, and that it skips build/deploy when no `services/whatsapp-business-service/**` change is present.
- [ ] After merge: confirm a `whatsapp-business-service-v*.*.*-beta` tag runs the new workflow end-to-end to staging.


---

## `63fa5b5e` feat(billing): add offline order lifecycle service (#2766)

- **作者**: bill-srp
- **日期**: 2026-07-08T07:10:17Z
- **SHA**: 63fa5b5e56f843da53fcc6395f0180c8b4a3dd75

### 完整 Commit Message

```
feat(billing): add offline order lifecycle service (#2766)

## Summary

- split lifecycle service layer out of PR #2753
- add offline order create/confirm/cancel/recovery helpers behind
service APIs
- add offline fulfillment compensation coverage without exposing admin
routes yet

## Stack

1. `feat/offline-payment-foundation`: foundation — **merged (#2765)**
2. This PR: lifecycle service, base `main`
3. `feat/offline-payment-admin-expiry`: admin routes and expiry
integration (#2767)

## PR size (`size-override`)

Over the 3000-line budget (~3513 lines), but ~60% is a single cohesive
unit-test file
(`tests/unit/test_offline_orders_service.py`, 2127 lines). The
production code is already split
into small `offline_order_*.py` modules; the overage is test coverage
for the offline-order
lifecycle, which the whole-app 90% coverage gate requires to ship
together with its code.
Splitting further would only insert artificial seams into one lifecycle
service. Applying
`size-override` rather than fragmenting the slice.

## Local verification

- `/Users/bill/.venvs/claw-interface/bin/pytest
tests/unit/test_offline_orders_service.py
tests/unit/test_billing_v2_fulfillment.py
tests/unit/test_billing_revoke.py`
- `env VIRTUAL_ENV=/Users/bill/.venvs/claw-interface
PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
```

### PR Description

## Summary

- split lifecycle service layer out of PR #2753
- add offline order create/confirm/cancel/recovery helpers behind service APIs
- add offline fulfillment compensation coverage without exposing admin routes yet

## Stack

1. `feat/offline-payment-foundation`: foundation — **merged (#2765)**
2. This PR: lifecycle service, base `main`
3. `feat/offline-payment-admin-expiry`: admin routes and expiry integration (#2767)

## PR size (`size-override`)

Over the 3000-line budget (~3513 lines), but ~60% is a single cohesive unit-test file
(`tests/unit/test_offline_orders_service.py`, 2127 lines). The production code is already split
into small `offline_order_*.py` modules; the overage is test coverage for the offline-order
lifecycle, which the whole-app 90% coverage gate requires to ship together with its code.
Splitting further would only insert artificial seams into one lifecycle service. Applying
`size-override` rather than fragmenting the slice.

## Local verification

- `/Users/bill/.venvs/claw-interface/bin/pytest tests/unit/test_offline_orders_service.py tests/unit/test_billing_v2_fulfillment.py tests/unit/test_billing_revoke.py`
- `env VIRTUAL_ENV=/Users/bill/.venvs/claw-interface PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`



---

## `03606021` ci(whatsapp): remove service deploy gates (#2770)

- **作者**: bill-srp
- **日期**: 2026-07-08T06:52:04Z
- **SHA**: 03606021275e23cec4e92dc14ffb63ec0c311c6f

### 完整 Commit Message

```
ci(whatsapp): remove service deploy gates (#2770)

## Summary

- Remove the `WHATSAPP_BUSINESS_SERVICE_DEPLOY_ENABLED` gate from the
WhatsApp Business Service deploy jobs.
- Remove the `WHATSAPP_BUSINESS_LISTENER_BOOTSTRAP_READY` gate from the
dev/staging/production deploy jobs. Restart-time reply-listener recovery
is intentionally best-effort (no durable bootstrap): a restart drops
in-flight Mattermost reply sockets until the user's next inbound
WhatsApp message re-arms them, and the user retries.
- Keep the existing tag/main trigger conditions for dev, staging, and
production deploys unchanged.
- Document the accepted tradeoffs in `architecture.md` /
`architecture.zh-CN.md` (new "Restart & multi-pod tradeoffs (reply
listeners)" note).

## Tradeoff / review note

This deliberately reverses the earlier "keep listener bootstrap deploy
gate" commit on this branch. Removing the bootstrap gate at production
`replicas: 2` means two failure modes are now **accepted, documented**
best-effort tradeoffs rather than blocked:

- **Restart loss** — synchronous turn-based chat self-heals on the
user's next message; the unrecovered case is delayed/proactive agent
replies (the user is passively waiting, gets no failure signal, won't
know to retry).
- **Multi-pod duplicate delivery** — `replicas: 2`, no Service
`sessionAffinity`, and no outbound idempotency guard mean a multi-turn
conversation can be delivered the same reply once per watching pod. This
exists on normal traffic today, independent of restarts.

Remediations are recorded in the architecture note for follow-up if
either becomes unacceptable at launch: run the bridge at `replicas: 1`
(eliminates duplicates) and/or add an atomic `mattermost_post_id`
delivery claim for exactly-once outbound (reusing the
`claim_inbound_message` pattern), which then makes a durable `onStart`
token-restore safe to add.

## Testing

- Confirmed `WHATSAPP_BUSINESS_LISTENER_BOOTSTRAP_READY` is fully
removed repo-wide (grep).
- Reviewed `git diff`: the three deploy `if:` blocks remain well-formed
(`always() && …`); only the gate line and stale comments changed.
- `bash scripts/verify-changed.sh` (changed surface is CI workflow +
root docs only — no `web/app` / `claw-interface` code).
```

### PR Description

## Summary

- Remove the `WHATSAPP_BUSINESS_SERVICE_DEPLOY_ENABLED` gate from the WhatsApp Business Service deploy jobs.
- Remove the `WHATSAPP_BUSINESS_LISTENER_BOOTSTRAP_READY` gate from the dev/staging/production deploy jobs. Restart-time reply-listener recovery is intentionally best-effort (no durable bootstrap): a restart drops in-flight Mattermost reply sockets until the user's next inbound WhatsApp message re-arms them, and the user retries.
- Keep the existing tag/main trigger conditions for dev, staging, and production deploys unchanged.
- Document the accepted tradeoffs in `architecture.md` / `architecture.zh-CN.md` (new "Restart & multi-pod tradeoffs (reply listeners)" note).

## Tradeoff / review note

This deliberately reverses the earlier "keep listener bootstrap deploy gate" commit on this branch. Removing the bootstrap gate at production `replicas: 2` means two failure modes are now **accepted, documented** best-effort tradeoffs rather than blocked:

- **Restart loss** — synchronous turn-based chat self-heals on the user's next message; the unrecovered case is delayed/proactive agent replies (the user is passively waiting, gets no failure signal, won't know to retry).
- **Multi-pod duplicate delivery** — `replicas: 2`, no Service `sessionAffinity`, and no outbound idempotency guard mean a multi-turn conversation can be delivered the same reply once per watching pod. This exists on normal traffic today, independent of restarts.

Remediations are recorded in the architecture note for follow-up if either becomes unacceptable at launch: run the bridge at `replicas: 1` (eliminates duplicates) and/or add an atomic `mattermost_post_id` delivery claim for exactly-once outbound (reusing the `claim_inbound_message` pattern), which then makes a durable `onStart` token-restore safe to add.

## Testing

- Confirmed `WHATSAPP_BUSINESS_LISTENER_BOOTSTRAP_READY` is fully removed repo-wide (grep).
- Reviewed `git diff`: the three deploy `if:` blocks remain well-formed (`always() && …`); only the gate line and stale comments changed.
- `bash scripts/verify-changed.sh` (changed surface is CI workflow + root docs only — no `web/app` / `claw-interface` code).


---

## `60fd4f1c` feat(web): improve tool status display (#2768)

- **作者**: sam-srp
- **日期**: 2026-07-08T06:12:54Z
- **SHA**: 60fd4f1c46fe990e8d065db1d36545d590a4f9cc

### 完整 Commit Message

```
feat(web): improve tool status display (#2768)

## Summary
- Parse Mattermost tool status props into richer tool step display data,
including tool args, item metadata, status, summaries, and progress
text.
- Format tool arguments with official-style concise previews, including
multiline update_plan step/status output.
- Let users click an individual tool row to expand full long content and
click again to collapse, while keeping update_plan multiline by default.

## Impact
- Tool rows stay compact by default but remain inspectable when
command/path/url details are long.
- update_plan no longer exposes raw JSON in the chat UI.
- Same tool_call_id updates merge into the original tool row instead of
creating duplicate rows.

## Validation
- Passed: git diff --check.
- Blocked: CI=true pnpm --dir web/app test:unit --
tests/unit/app/chat/toolStatusParser.unit.spec.ts
tests/unit/app/chat/ToolGroup.unit.spec.tsx fails before running tests
because pnpm reports ERR_PNPM_LOCKFILE_CONFIG_MISMATCH for the current
lockfile overrides config.
```

### PR Description

## Summary
- Parse Mattermost tool status props into richer tool step display data, including tool args, item metadata, status, summaries, and progress text.
- Format tool arguments with official-style concise previews, including multiline update_plan step/status output.
- Let users click an individual tool row to expand full long content and click again to collapse, while keeping update_plan multiline by default.

## Impact
- Tool rows stay compact by default but remain inspectable when command/path/url details are long.
- update_plan no longer exposes raw JSON in the chat UI.
- Same tool_call_id updates merge into the original tool row instead of creating duplicate rows.

## Validation
- Passed: git diff --check.
- Blocked: CI=true pnpm --dir web/app test:unit -- tests/unit/app/chat/toolStatusParser.unit.spec.ts tests/unit/app/chat/ToolGroup.unit.spec.tsx fails before running tests because pnpm reports ERR_PNPM_LOCKFILE_CONFIG_MISMATCH for the current lockfile overrides config.

---

## `cd47add4` fix(whatsapp): remove uidless resolve rollout flag (#2769)

- **作者**: bill-srp
- **日期**: 2026-07-08T05:40:21Z
- **SHA**: cd47add49d345a7765ba7e4903b8b94acbf4c0a9

### 完整 Commit Message

```
fix(whatsapp): remove uidless resolve rollout flag (#2769)

## Summary

- Remove the `WHATSAPP_ENABLE_UIDLESS_MATTERMOST_RESOLVE` rollout flag
from WhatsApp Business Service config.
- Always resolve Mattermost agent replies through Claw Interface
channel+author lookup before sending back to WhatsApp.
- Update tests and README to reflect the now-required deployed contract.

## Testing

- `./node_modules/.bin/vitest run`
- `./node_modules/.bin/tsc --noEmit`
- `./node_modules/.bin/tsc -p tsconfig.build.json`
- `git diff --check -- services/whatsapp-business-service`
- `bash scripts/verify-changed.sh`
```

### PR Description

## Summary

- Remove the `WHATSAPP_ENABLE_UIDLESS_MATTERMOST_RESOLVE` rollout flag from WhatsApp Business Service config.
- Always resolve Mattermost agent replies through Claw Interface channel+author lookup before sending back to WhatsApp.
- Update tests and README to reflect the now-required deployed contract.

## Testing

- `./node_modules/.bin/vitest run`
- `./node_modules/.bin/tsc --noEmit`
- `./node_modules/.bin/tsc -p tsconfig.build.json`
- `git diff --check -- services/whatsapp-business-service`
- `bash scripts/verify-changed.sh`


---

## `e245145d` feat(billing): add offline payment foundation (#2765)

- **作者**: bill-srp
- **日期**: 2026-07-08T04:28:22Z
- **SHA**: e245145db128888cbfbc799a706abac826bc1606

### 完整 Commit Message

```
feat(billing): add offline payment foundation (#2765)

## Summary

- split foundation layer out of PR #2753
- add offline Billing v2 provider/source fields and payment-order
persistence primitives
- add the offline enterprise payment design spec and focused repo/schema
tests

## Stack

1. This PR: foundation, base `main`
2. `feat/offline-payment-core`: offline order lifecycle service
3. `feat/offline-payment-admin-expiry`: admin routes and expiry
integration

## Local verification

- `/Users/bill/.venvs/claw-interface/bin/pytest
tests/unit/test_billing_v2_repos.py tests/unit/test_payment_ownership.py
tests/unit/test_routes_account.py`
- `bash scripts/verify-py.sh --imports-only`
- `env VIRTUAL_ENV=/Users/bill/.venvs/claw-interface
PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
```

### PR Description

## Summary

- split foundation layer out of PR #2753
- add offline Billing v2 provider/source fields and payment-order persistence primitives
- add the offline enterprise payment design spec and focused repo/schema tests

## Stack

1. This PR: foundation, base `main`
2. `feat/offline-payment-core`: offline order lifecycle service
3. `feat/offline-payment-admin-expiry`: admin routes and expiry integration

## Local verification

- `/Users/bill/.venvs/claw-interface/bin/pytest tests/unit/test_billing_v2_repos.py tests/unit/test_payment_ownership.py tests/unit/test_routes_account.py`
- `bash scripts/verify-py.sh --imports-only`
- `env VIRTUAL_ENV=/Users/bill/.venvs/claw-interface PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`


---

## `8e7136e3` feat(whatsapp): activate Oura replies after binding (#2759)

- **作者**: bill-srp
- **日期**: 2026-07-08T03:42:23Z
- **SHA**: 8e7136e3cf5b227ff7b2c9fa46a430caee439661

### 完整 Commit Message

```
feat(whatsapp): activate Oura replies after binding (#2759)

## Summary

- Auto-create/get WhatsApp account-service users and bind unknown
WhatsApp senders into claw-interface.
- Ensure WhatsApp-bound users get a personal org, then bind to a uid
through `/whatsapp/users/bind`.
- Return a non-routable `mattermost_listener_token` so the bridge can
listen while Oura Ring is still installing.
- Let WhatsApp-triggered Oura Ring installs send the existing Mattermost
activation `Hi`, so bridge can forward the agent reply back to WhatsApp.

## Tests

- `./node_modules/.bin/vitest run`
- `./node_modules/.bin/tsc --noEmit`
- `./node_modules/.bin/tsc -p tsconfig.build.json`
- `PYTHONPATH=services/claw-interface
/Users/bill/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_whatsapp_service.py
services/claw-interface/tests/unit/test_whatsapp_schema.py
services/claw-interface/tests/unit/test_whatsapp_routes.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- `git diff --check`

## Notes

- Bridge listener bootstrap is still process-local; durable restart
bootstrap remains a follow-up.
```

### PR Description

## Summary

- Auto-create/get WhatsApp account-service users and bind unknown WhatsApp senders into claw-interface.
- Ensure WhatsApp-bound users get a personal org, then bind to a uid through `/whatsapp/users/bind`.
- Return a non-routable `mattermost_listener_token` so the bridge can listen while Oura Ring is still installing.
- Let WhatsApp-triggered Oura Ring installs send the existing Mattermost activation `Hi`, so bridge can forward the agent reply back to WhatsApp.

## Tests

- `./node_modules/.bin/vitest run`
- `./node_modules/.bin/tsc --noEmit`
- `./node_modules/.bin/tsc -p tsconfig.build.json`
- `PYTHONPATH=services/claw-interface /Users/bill/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_whatsapp_service.py services/claw-interface/tests/unit/test_whatsapp_schema.py services/claw-interface/tests/unit/test_whatsapp_routes.py -q`
- `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- `git diff --check`

## Notes

- Bridge listener bootstrap is still process-local; durable restart bootstrap remains a follow-up.


---

## `b88f2794` fix(dashboard-console): gate metadata avatar refresh (#2764)

- **作者**: bill-srp
- **日期**: 2026-07-08T02:56:30Z
- **SHA**: b88f2794043212b379aab1af4afc3b52e7deaea7

### 完整 Commit Message

```
fix(dashboard-console): gate metadata avatar refresh (#2764)

## Summary
- Add an opt-in archive avatar checkbox to dashboard-console metadata
refresh.
- Keep the existing pack avatar by default and upload the parsed archive
avatar only when selected.
- Cover the dialog opt-in and metadata refresh request behavior with
targeted tests.

## Root cause
The metadata refresh path could parse an avatar from the downloaded
archive, but avatar replacement should follow the same operator opt-in
model as submitting a new version instead of overwriting automatically.

## Test plan
- [x] `./node_modules/.bin/vitest run
app/routes/agent-packs/route.test.tsx --pool=threads`
- [x] `./node_modules/.bin/vitest run
app/routes/agent-packs/metadata-refresh.test.ts --pool=threads`
- [x] `npm run typecheck`
- [x] `./node_modules/.bin/tsc -b`
- [x] `./node_modules/.bin/eslint
app/routes/agent-packs/metadata-refresh-dialog.tsx
app/routes/agent-packs/metadata-refresh.ts
app/routes/agent-packs/metadata-refresh.test.ts
app/routes/agent-packs/route.tsx app/routes/agent-packs/route.test.tsx
app/routes/agent-packs/use-view-model.ts
app/routes/agent-packs/use-view-model.test.tsx`
- [x] `git diff --check`

Note: used dashboard-console local binaries for targeted checks to avoid
triggering the known pnpm `xlsx` tarball integrity blocker. `npm run
typecheck` logged a sandbox-only Wrangler log-file EPERM warning under
`~/Library/Preferences/.wrangler/logs`, but exited 0 and `tsc -b`
passed.
```

### PR Description

## Summary
- Add an opt-in archive avatar checkbox to dashboard-console metadata refresh.
- Keep the existing pack avatar by default and upload the parsed archive avatar only when selected.
- Cover the dialog opt-in and metadata refresh request behavior with targeted tests.

## Root cause
The metadata refresh path could parse an avatar from the downloaded archive, but avatar replacement should follow the same operator opt-in model as submitting a new version instead of overwriting automatically.

## Test plan
- [x] `./node_modules/.bin/vitest run app/routes/agent-packs/route.test.tsx --pool=threads`
- [x] `./node_modules/.bin/vitest run app/routes/agent-packs/metadata-refresh.test.ts --pool=threads`
- [x] `npm run typecheck`
- [x] `./node_modules/.bin/tsc -b`
- [x] `./node_modules/.bin/eslint app/routes/agent-packs/metadata-refresh-dialog.tsx app/routes/agent-packs/metadata-refresh.ts app/routes/agent-packs/metadata-refresh.test.ts app/routes/agent-packs/route.tsx app/routes/agent-packs/route.test.tsx app/routes/agent-packs/use-view-model.ts app/routes/agent-packs/use-view-model.test.tsx`
- [x] `git diff --check`

Note: used dashboard-console local binaries for targeted checks to avoid triggering the known pnpm `xlsx` tarball integrity blocker. `npm run typecheck` logged a sandbox-only Wrangler log-file EPERM warning under `~/Library/Preferences/.wrangler/logs`, but exited 0 and `tsc -b` passed.

---
