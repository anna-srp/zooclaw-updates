# SerendipityOneInc/ecap-workspace — 2026-06-08 commits

共 32 个 commit

## [3fc8301] feat(claw-interface): ECA-516 aiohttp unclosed-session leak canary (#2279)

- **SHA**: 3fc8301833435de73bc0a4a146efc7421aca448c
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T14:28:11Z
- **PR**: #2279
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3fc8301833435de73bc0a4a146efc7421aca448c

### 完整 Commit Message

```
feat(claw-interface): ECA-516 aiohttp unclosed-session leak canary (#2279)

**Linear:** https://linear.app/srpone/issue/ECA-516

## What
Canary diagnostic for **ECA-516** — claw-interface `Unclosed client
session` warnings. Real & growing post-fix: ~10/day at the 2026-05-20
release → ~52/day on 2026-06-07.

## Why the prior fix (#1445/#1482) didn't hold
- App's own `aiohttp.ClientSession()` calls are all `async with`
(audited); the earlier fix touched only those + the Apple SDK.
- Its instrumentation hooks the **warnings** channel, which is **silent
in prod** (ResourceWarning is filtered by default). The warning actually
fires via the **asyncio loop exception handler**
(`python_logger=asyncio`), carrying no stack.

## Root cause (from log shape)
Even per-hour, per-pod constant, **~5-min cadence, traffic-independent**
→ a periodic in-process **APScheduler** job (5 jobs, all `interval
minutes=5`) leaks an aiohttp session created **inside a dependency**.
Not FAL, not request-driven litellm (both idle). Exact frame needs the
creation stack — hence this canary.

## How
- New `app/aiohttp_leak_debug.py`: `loop.set_debug(True)` so aiohttp
records `source_traceback`, plus an **additive** exception handler
logging `[AIOHTTP_LEAK] … created at: <stack>` (chains to the previous
handler; nothing else changes).
- Gated by env **`AIOHTTP_LEAK_DEBUG=1`** — off by default → zero
overhead.
- Wired into `startup()` before any background session is created.
- 7 unit tests (green locally on py3.11; full suite runs in CI on
py3.12).

## Deploy / usage
1. Set `AIOHTTP_LEAK_DEBUG=1` on **ONE** pod only, restart it.
2. Wait ~15 min (≈3 job cycles + GC).
3. `gcloud logging read 'labels."k8s-pod/app"="claw-interface" AND
"[AIOHTTP_LEAK]" AND "created at"' --project=srpproduct-dc37e
--freshness=1h --limit=5 --format='value(textPayload)'`
4. Fix the named call site → unset the env → remove this module.

⚠️ **Do NOT enable fleet-wide.** asyncio debug adds per-task
stack-extraction (CPU/mem/latency) across all traffic; the per-pod 5-min
job reproduces on any single pod, so one canary suffices.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

**Linear:** https://linear.app/srpone/issue/ECA-516

## What
Canary diagnostic for **ECA-516** — claw-interface `Unclosed client session` warnings. Real & growing post-fix: ~10/day at the 2026-05-20 release → ~52/day on 2026-06-07.

## Why the prior fix (#1445/#1482) didn't hold
- App's own `aiohttp.ClientSession()` calls are all `async with` (audited); the earlier fix touched only those + the Apple SDK.
- Its instrumentation hooks the **warnings** channel, which is **silent in prod** (ResourceWarning is filtered by default). The warning actually fires via the **asyncio loop exception handler** (`python_logger=asyncio`), carrying no stack.

## Root cause (from log shape)
Even per-hour, per-pod constant, **~5-min cadence, traffic-independent** → a periodic in-process **APScheduler** job (5 jobs, all `interval minutes=5`) leaks an aiohttp session created **inside a dependency**. Not FAL, not request-driven litellm (both idle). Exact frame needs the creation stack — hence this canary.

## How
- New `app/aiohttp_leak_debug.py`: `loop.set_debug(True)` so aiohttp records `source_traceback`, plus an **additive** exception handler logging `[AIOHTTP_LEAK] … created at: <stack>` (chains to the previous handler; nothing else changes).
- Gated by env **`AIOHTTP_LEAK_DEBUG=1`** — off by default → zero overhead.
- Wired into `startup()` before any background session is created.
- 7 unit tests (green locally on py3.11; full suite runs in CI on py3.12).

## Deploy / usage
1. Set `AIOHTTP_LEAK_DEBUG=1` on **ONE** pod only, restart it.
2. Wait ~15 min (≈3 job cycles + GC).
3. `gcloud logging read 'labels."k8s-pod/app"="claw-interface" AND "[AIOHTTP_LEAK]" AND "created at"' --project=srpproduct-dc37e --freshness=1h --limit=5 --format='value(textPayload)'`
4. Fix the named call site → unset the env → remove this module.

⚠️ **Do NOT enable fleet-wide.** asyncio debug adds per-task stack-extraction (CPU/mem/latency) across all traffic; the per-pod 5-min job reproduces on any single pod, so one canary suffices.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [70cd098] refactor(web): extract FeedbackHost into GlobalOverlays (provider-tree Phase 2d) (#2278)

- **SHA**: 70cd0987f10617cd35924b66ecb9fb1b22ac60a0
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T14:26:28Z
- **PR**: #2278
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/70cd0987f10617cd35924b66ecb9fb1b22ac60a0

### 完整 Commit Message

```
refactor(web): extract FeedbackHost into GlobalOverlays (provider-tree Phase 2d) (#2278)

## What

**Final phase** of the [provider-tree Phase 2
refactor](../blob/main/docs/superpowers/specs/2026-06-06-provider-tree-refactor.md).
Follows #2275 / #2276 / #2277. Moves the Feedback FAB + dialog out of
`FeedbackProvider` into `<GlobalOverlays/>`.

## How — simpler than Toast/SupportTicket

`FeedbackProvider` already `createPortal`s to `document.body`, and its
context already exposed `healthStatus` / `isDialogOpen` / `openDialog` /
`closeDialog`. So **no dual-context split is needed** — only `crashInfo`
had to join the context value.

- Add `crashInfo` to `FeedbackContextValue` (changes only on crash/close
— no new cascade).
- New exported **`<FeedbackHost/>`** owns the `useIsHydrated()` gate +
`createPortal` block (dialog + FAB); `GlobalOverlays` mounts it.
- `FeedbackProvider` now returns just the context provider around
`children` — pure state/effects (HealthMonitor, Sentry identity, window
error listeners, crash bridge).
- **DOM landing point is unchanged** (still `document.body` via portal);
only the React owner subtree moves.

## Tests

- `FeedbackProvider.unit.spec`: new `renderWithHost()` helper; the 9
dialog/FAB-asserting tests mount `<FeedbackHost/>` alongside their
trigger. Added `crashInfo` to the context-shape assertion + a
`FeedbackHost`-outside-provider guard (23 tests pass).
- `ClientLayout.unit.spec`: mock exports `FeedbackHost` (renders the
real `GlobalOverlays`).
- `GlobalOverlays.unit.spec`: asserts the host mounts.
- `tsc --noEmit`, `eslint`, `pnpm dup` clean — 71 tests pass across the
4 affected specs.

## Phase 2 complete

All overlays now mount flat in `<GlobalOverlays/>`; Toast /
SupportTicket / Feedback providers are pure state/context layers. (Per
the spec note, this does not shrink the provider pyramid depth — that's
Phase 3's route-group split.)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

**Final phase** of the [provider-tree Phase 2 refactor](../blob/main/docs/superpowers/specs/2026-06-06-provider-tree-refactor.md). Follows #2275 / #2276 / #2277. Moves the Feedback FAB + dialog out of `FeedbackProvider` into `<GlobalOverlays/>`.

## How — simpler than Toast/SupportTicket

`FeedbackProvider` already `createPortal`s to `document.body`, and its context already exposed `healthStatus` / `isDialogOpen` / `openDialog` / `closeDialog`. So **no dual-context split is needed** — only `crashInfo` had to join the context value.

- Add `crashInfo` to `FeedbackContextValue` (changes only on crash/close — no new cascade).
- New exported **`<FeedbackHost/>`** owns the `useIsHydrated()` gate + `createPortal` block (dialog + FAB); `GlobalOverlays` mounts it.
- `FeedbackProvider` now returns just the context provider around `children` — pure state/effects (HealthMonitor, Sentry identity, window error listeners, crash bridge).
- **DOM landing point is unchanged** (still `document.body` via portal); only the React owner subtree moves.

## Tests

- `FeedbackProvider.unit.spec`: new `renderWithHost()` helper; the 9 dialog/FAB-asserting tests mount `<FeedbackHost/>` alongside their trigger. Added `crashInfo` to the context-shape assertion + a `FeedbackHost`-outside-provider guard (23 tests pass).
- `ClientLayout.unit.spec`: mock exports `FeedbackHost` (renders the real `GlobalOverlays`).
- `GlobalOverlays.unit.spec`: asserts the host mounts.
- `tsc --noEmit`, `eslint`, `pnpm dup` clean — 71 tests pass across the 4 affected specs.

## Phase 2 complete

All overlays now mount flat in `<GlobalOverlays/>`; Toast / SupportTicket / Feedback providers are pure state/context layers. (Per the spec note, this does not shrink the provider pyramid depth — that's Phase 3's route-group split.)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [96bb253] refactor(web): split SupportTicket action/state contexts + move host to GlobalOverlays (Phase 2c) (#2277)

- **SHA**: 96bb253d59976c8bd34e263b7ef995d386df0241
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T14:02:14Z
- **PR**: #2277
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/96bb253d59976c8bd34e263b7ef995d386df0241

### 完整 Commit Message

```
refactor(web): split SupportTicket action/state contexts + move host to GlobalOverlays (Phase 2c) (#2277)

## What

Phase 2c of the [provider-tree
refactor](../blob/main/docs/superpowers/specs/2026-06-06-provider-tree-refactor.md).
Follows #2275 / #2276. Same **action/state context split** pattern as
the Toast PR, applied to `SupportTicketModal`, so the modal mounts in
`<GlobalOverlays/>` without re-rendering the action consumers on
open/close.

## How

- Context → **`SupportTicketActionContext`** (`{ openSupportTicket }`) +
**`SupportTicketStateContext`** (`{ isOpen, defaultCategory, close }`).
- `useSupportTicket()` reads the action context — **signature/behavior
unchanged** for all 6 consumers.
- New exported **`<SupportTicketHost/>`** reads state and renders the
modal when open; `GlobalOverlays` mounts it.
- `SupportTicketProvider` renders no modal — just the two context
providers around `children`.

## Tests

- `support-ticket-modal.unit.spec`: harness renders
`<SupportTicketHost/>` alongside the opener; **new** action-stability
regression test + host-outside-provider guard.
- `ClientLayout.unit.spec`: mock now exports `SupportTicketHost`
(renders real `GlobalOverlays`).
- `GlobalOverlays.unit.spec`: asserts the host mounts.
- `tsc --noEmit`, `eslint`, `pnpm dup` clean — 31 tests pass across the
3 affected specs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Phase 2c of the [provider-tree refactor](../blob/main/docs/superpowers/specs/2026-06-06-provider-tree-refactor.md). Follows #2275 / #2276. Same **action/state context split** pattern as the Toast PR, applied to `SupportTicketModal`, so the modal mounts in `<GlobalOverlays/>` without re-rendering the action consumers on open/close.

## How

- Context → **`SupportTicketActionContext`** (`{ openSupportTicket }`) + **`SupportTicketStateContext`** (`{ isOpen, defaultCategory, close }`).
- `useSupportTicket()` reads the action context — **signature/behavior unchanged** for all 6 consumers.
- New exported **`<SupportTicketHost/>`** reads state and renders the modal when open; `GlobalOverlays` mounts it.
- `SupportTicketProvider` renders no modal — just the two context providers around `children`.

## Tests

- `support-ticket-modal.unit.spec`: harness renders `<SupportTicketHost/>` alongside the opener; **new** action-stability regression test + host-outside-provider guard.
- `ClientLayout.unit.spec`: mock now exports `SupportTicketHost` (renders real `GlobalOverlays`).
- `GlobalOverlays.unit.spec`: asserts the host mounts.
- `tsc --noEmit`, `eslint`, `pnpm dup` clean — 31 tests pass across the 3 affected specs.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [d4b541b] feat(claw-interface): wire request-context logging (favie-common v0.3.61) (#2273)

- **SHA**: d4b541bb896381be6a0ca3b2fb8a18e8c325434d
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T13:52:05Z
- **PR**: #2273
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d4b541bb896381be6a0ca3b2fb8a18e8c325434d

### 完整 Commit Message

```
feat(claw-interface): wire request-context logging (favie-common v0.3.61) (#2273)

## Summary

Wires the ECA-922 request-context logging feature into
**claw-interface** using the `favie_common` v0.3.61 API.

- **Bump pin** (`requirements.txt` line 14): `favie-common.git@v0.3.58`
→ `@v0.3.61`
- **Logging** (`app/app_logging.py`): replace the bespoke
google/file/stdout handler-installation branches inside
`configure_logging()` with a single `configure_structured_logging()`
call (installs a stdout `StructuredLogHandler` with a request-context
filter; GCP `jsonPayload.*`-compatible). All auxiliary behaviour is
preserved: `_suppress_noisy_loggers()`,
`_route_resource_warnings_to_logger()`, and the `_logging_configured`
idempotency guard.
- **Middleware** (`app/create_app.py`): import
`RequestContextMiddleware` and call
`app.add_middleware(RequestContextMiddleware)` immediately after the
existing `app.add_middleware(HttpLoggingMiddleware)` line, making it
outermost relative to `HttpLoggingMiddleware` so every log line
(including `HttpLoggingMiddleware`'s own lines) carries the
request-context fields.
- **Tests** (`tests/unit/test_app_logging.py`): remove the three
deleted-backend test cases and add new tests verifying delegation to
`configure_structured_logging()`, idempotency, and the configured-flag;
all `TestSuppressNoisyLoggers` and `TestRouteResourceWarningsToLogger`
tests are retained and pass.

Linear: https://linear.app/srpone/issue/ECA-922

## Test plan
- [x] `python -m py_compile app/app_logging.py app/create_app.py` —
clean
- [x] `favie_common.logging` and
`favie_common.middleware.request_context` import successfully from
v0.3.61
- [x] `tests/unit/test_app_logging.py` — all 14 tests pass
- [x] App factory import fails only on missing `MONGODB_USER` env var
(pre-existing; unrelated to this change)
- [ ] CI `python-code-quality / build-and-test` (ruff + pyright +
pytest)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

Wires the ECA-922 request-context logging feature into **claw-interface** using the `favie_common` v0.3.61 API.

- **Bump pin** (`requirements.txt` line 14): `favie-common.git@v0.3.58` → `@v0.3.61`
- **Logging** (`app/app_logging.py`): replace the bespoke google/file/stdout handler-installation branches inside `configure_logging()` with a single `configure_structured_logging()` call (installs a stdout `StructuredLogHandler` with a request-context filter; GCP `jsonPayload.*`-compatible). All auxiliary behaviour is preserved: `_suppress_noisy_loggers()`, `_route_resource_warnings_to_logger()`, and the `_logging_configured` idempotency guard.
- **Middleware** (`app/create_app.py`): import `RequestContextMiddleware` and call `app.add_middleware(RequestContextMiddleware)` immediately after the existing `app.add_middleware(HttpLoggingMiddleware)` line, making it outermost relative to `HttpLoggingMiddleware` so every log line (including `HttpLoggingMiddleware`'s own lines) carries the request-context fields.
- **Tests** (`tests/unit/test_app_logging.py`): remove the three deleted-backend test cases and add new tests verifying delegation to `configure_structured_logging()`, idempotency, and the configured-flag; all `TestSuppressNoisyLoggers` and `TestRouteResourceWarningsToLogger` tests are retained and pass.

Linear: https://linear.app/srpone/issue/ECA-922

## Test plan
- [x] `python -m py_compile app/app_logging.py app/create_app.py` — clean
- [x] `favie_common.logging` and `favie_common.middleware.request_context` import successfully from v0.3.61
- [x] `tests/unit/test_app_logging.py` — all 14 tests pass
- [x] App factory import fails only on missing `MONGODB_USER` env var (pre-existing; unrelated to this change)
- [ ] CI `python-code-quality / build-and-test` (ruff + pyright + pytest)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [5cea66a] refactor(web): split Toast action/state contexts + move ToastViewport to GlobalOverlays (Phase 2b) (#2276)

- **SHA**: 5cea66a6d42525f0ac9e599271855af1dab87703
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T13:50:29Z
- **PR**: #2276
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/5cea66a6d42525f0ac9e599271855af1dab87703

### 完整 Commit Message

```
refactor(web): split Toast action/state contexts + move ToastViewport to GlobalOverlays (Phase 2b) (#2276)

## What

Phase 2b of the [provider-tree
refactor](../blob/main/docs/superpowers/specs/2026-06-06-provider-tree-refactor.md).
Follows #2275. Decouples the toast **viewport** from `ToastProvider` so
the visual layer lives in `<GlobalOverlays/>` with the other overlays —
without reintroducing the re-render cascade Phase 1 eliminated.

## How — action/state context split

`ToastProvider` deliberately exposed **only `showToast`** so its 44
consumers don't re-render when the toast list changes. Naively adding
`toasts` to that context to feed a relocated viewport would undo that.
Instead:

- `ToastContext` → **`ToastActionContext`** (`{ showToast }`) +
**`ToastStateContext`** (`{ toasts, removeToast }`).
- `useToast()` reads the action context — **signature and behavior
unchanged** for all 44 consumers.
- New exported **`<ToastViewport/>`** reads the state context and
renders the stack; `GlobalOverlays` mounts it (it's within
`ToastProvider` in the tree).
- `ToastProvider` renders no viewport — just the two context providers
around `children`.

Net: the toast view relocates, render isolation is preserved.

## Tests

- `Toast.unit.spec`: harness renders `<ToastViewport/>` alongside
children; **new** regression test that the action value stays
referentially stable across a toast add (the split's core contract) + a
`ToastViewport`-outside-provider guard.
- `ClientLayout.unit.spec`: Toast mock now exports `ToastViewport` (it
renders the real `GlobalOverlays`) — caught a cross-file mock drift.
- `GlobalOverlays.unit.spec`: asserts the viewport mounts.
- `tsc --noEmit`, `eslint`, `pnpm dup` all clean (25 tests pass across
the 3 affected specs).

## Note
Moving the view out does **not** shrink the provider pyramid
(`ToastProvider` still owns the state and nests in the tree); the payoff
is a pure state-only provider + all overlays discoverable in one
component.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Phase 2b of the [provider-tree refactor](../blob/main/docs/superpowers/specs/2026-06-06-provider-tree-refactor.md). Follows #2275. Decouples the toast **viewport** from `ToastProvider` so the visual layer lives in `<GlobalOverlays/>` with the other overlays — without reintroducing the re-render cascade Phase 1 eliminated.

## How — action/state context split

`ToastProvider` deliberately exposed **only `showToast`** so its 44 consumers don't re-render when the toast list changes. Naively adding `toasts` to that context to feed a relocated viewport would undo that. Instead:

- `ToastContext` → **`ToastActionContext`** (`{ showToast }`) + **`ToastStateContext`** (`{ toasts, removeToast }`).
- `useToast()` reads the action context — **signature and behavior unchanged** for all 44 consumers.
- New exported **`<ToastViewport/>`** reads the state context and renders the stack; `GlobalOverlays` mounts it (it's within `ToastProvider` in the tree).
- `ToastProvider` renders no viewport — just the two context providers around `children`.

Net: the toast view relocates, render isolation is preserved.

## Tests

- `Toast.unit.spec`: harness renders `<ToastViewport/>` alongside children; **new** regression test that the action value stays referentially stable across a toast add (the split's core contract) + a `ToastViewport`-outside-provider guard.
- `ClientLayout.unit.spec`: Toast mock now exports `ToastViewport` (it renders the real `GlobalOverlays`) — caught a cross-file mock drift.
- `GlobalOverlays.unit.spec`: asserts the viewport mounts.
- `tsc --noEmit`, `eslint`, `pnpm dup` all clean (25 tests pass across the 3 affected specs).

## Note
Moving the view out does **not** shrink the provider pyramid (`ToastProvider` still owns the state and nests in the tree); the payoff is a pure state-only provider + all overlays discoverable in one component.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [a87fa79] hotfix(openclaw): bootstrap billing before bot create (#2274)

- **SHA**: a87fa794b0a46ee8c157032740323282eb430c6f
- **作者**: kaka-srp
- **日期**: 2026-06-08T13:35:04Z
- **PR**: #2274
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/a87fa794b0a46ee8c157032740323282eb430c6f

### 完整 Commit Message

```
hotfix(openclaw): bootstrap billing before bot create (#2274)

## Summary
- Allow /openclaw/init to refresh Billing v2 profile state even when the
legacy account subscription status is terminal.
- Add a regression test for active Billing v2 access with stale legacy
expired account state and no existing V2 computer.
- Update OpenClaw unit-test billing mocks to accept the new bootstrap
keyword.

## Root cause
The OpenClaw subscription gate correctly allowed active Billing v2
access, but the no-bot creation path then called
ensure_billing_initialized without terminal-subscription bootstrap
enabled. For users whose legacy ecap-account state was still expired,
billing initialization skipped the Billing v2 profile overlay, so bot
creation saw no LiteLLM billing key and failed.

## Test plan
- [x] /home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] /home/node/.venvs/claw-interface/bin/python -m pyright app tests
- [x] /home/node/.venvs/claw-interface/bin/python -m pytest
tests/unit/test_openclaw_subscription_gate.py
tests/unit/test_openclaw_routes.py
tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_create_bot_401_retries_with_new_app
tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_start_bot_failure_sets_error_status
tests/unit/test_openclaw_endpoints_extra.py::TestRedeployOpenclaw::test_redeploy_no_bot_delegates_to_init
-q — 99 passed
```

### PR Description

## Summary
- Allow /openclaw/init to refresh Billing v2 profile state even when the legacy account subscription status is terminal.
- Add a regression test for active Billing v2 access with stale legacy expired account state and no existing V2 computer.
- Update OpenClaw unit-test billing mocks to accept the new bootstrap keyword.

## Root cause
The OpenClaw subscription gate correctly allowed active Billing v2 access, but the no-bot creation path then called ensure_billing_initialized without terminal-subscription bootstrap enabled. For users whose legacy ecap-account state was still expired, billing initialization skipped the Billing v2 profile overlay, so bot creation saw no LiteLLM billing key and failed.

## Test plan
- [x] /home/node/.venvs/claw-interface/bin/python -m ruff check .
- [x] /home/node/.venvs/claw-interface/bin/python -m pyright app tests
- [x] /home/node/.venvs/claw-interface/bin/python -m pytest tests/unit/test_openclaw_subscription_gate.py tests/unit/test_openclaw_routes.py tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_create_bot_401_retries_with_new_app tests/unit/test_openclaw_endpoints_extra.py::TestInitOpenclawCreateBot::test_start_bot_failure_sets_error_status tests/unit/test_openclaw_endpoints_extra.py::TestRedeployOpenclaw::test_redeploy_no_bot_delegates_to_init -q — 99 passed


---

## [b7b0627] refactor(web): extract GlobalOverlays from ClientLayout (provider-tree Phase 2a) (#2275)

- **SHA**: b7b0627a10b407eb5ebe0f850da1ad756cf31b8e
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T13:33:58Z
- **PR**: #2275
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/b7b0627a10b407eb5ebe0f850da1ad756cf31b8e

### 完整 Commit Message

```
refactor(web): extract GlobalOverlays from ClientLayout (provider-tree Phase 2a) (#2275)

## What

Phase 2a of the [provider-tree
refactor](../blob/main/docs/superpowers/specs/2026-06-06-provider-tree-refactor.md).
Collects the **six scattered overlay sibling nodes** that lived directly
inside `ClientLayout`'s `<ErrorBoundary>` into a single flat
`<GlobalOverlays/>`:

`GiftPaywallFab` · `GuideTourGlobal` · `DomainMigrationBanner` ·
`WelcomeRewardToast` · `CompensationPopup` · `BillingMockSelector`
(dev-only)

The `GuideTourGlobal` wrapper (the `canUseChat` + suppressed-path gate)
moves with them.

## Why

`ClientLayout` mixed a 16-deep provider pyramid with six loose overlay
nodes at the bottom, making the layout hard to scan. These overlays
render via `position: fixed` / their own portals, so their tree position
only matters for **context availability** — not structure.

`<GlobalOverlays/>` stays mounted at the **same spot** (inside
`ErrorBoundary`, after `AppLayout`), so every consumed context
(Onboarding / BillingCredits / Language / the guide-tour Zustand store)
is still in scope. **Pure structural move — zero behavior change.**

## Scope note / spec correction

The spec originally described `Toast` / `Feedback` / `SupportTicket` as
portal-ized scattered nodes too. Reading the source showed only
`Feedback` actually portals; `Toast`/`SupportTicket` render their view
*inside their own provider*. This PR corrects the Phase 2 prose and
splits Phase 2 into 4 serial sub-PRs (2a here; 2b–2d move those three
provider views out via an action/state context split — follow-ups).

## Tests

- New `GlobalOverlays.unit.spec.tsx`: asserts the always-on overlays
mount, the `isBillingMockEnabled` gate, and the guide-tour
enable/suppress/hide gates.
- `tsc --noEmit`, `eslint`, `pnpm dup` all clean locally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Phase 2a of the [provider-tree refactor](../blob/main/docs/superpowers/specs/2026-06-06-provider-tree-refactor.md). Collects the **six scattered overlay sibling nodes** that lived directly inside `ClientLayout`'s `<ErrorBoundary>` into a single flat `<GlobalOverlays/>`:

`GiftPaywallFab` · `GuideTourGlobal` · `DomainMigrationBanner` · `WelcomeRewardToast` · `CompensationPopup` · `BillingMockSelector` (dev-only)

The `GuideTourGlobal` wrapper (the `canUseChat` + suppressed-path gate) moves with them.

## Why

`ClientLayout` mixed a 16-deep provider pyramid with six loose overlay nodes at the bottom, making the layout hard to scan. These overlays render via `position: fixed` / their own portals, so their tree position only matters for **context availability** — not structure.

`<GlobalOverlays/>` stays mounted at the **same spot** (inside `ErrorBoundary`, after `AppLayout`), so every consumed context (Onboarding / BillingCredits / Language / the guide-tour Zustand store) is still in scope. **Pure structural move — zero behavior change.**

## Scope note / spec correction

The spec originally described `Toast` / `Feedback` / `SupportTicket` as portal-ized scattered nodes too. Reading the source showed only `Feedback` actually portals; `Toast`/`SupportTicket` render their view *inside their own provider*. This PR corrects the Phase 2 prose and splits Phase 2 into 4 serial sub-PRs (2a here; 2b–2d move those three provider views out via an action/state context split — follow-ups).

## Tests

- New `GlobalOverlays.unit.spec.tsx`: asserts the always-on overlays mount, the `isBillingMockEnabled` gate, and the guide-tour enable/suppress/hide gates.
- `tsc --noEmit`, `eslint`, `pnpm dup` all clean locally.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [e975d49] fix(web): align session chat and new chat actions (#2272)

- **SHA**: e975d498f27d9a6debee195a7b394bf28303fc9d
- **作者**: bill-srp
- **日期**: 2026-06-08T13:25:25Z
- **PR**: #2272
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e975d498f27d9a6debee195a7b394bf28303fc9d

### 完整 Commit Message

```
fix(web): align session chat and new chat actions (#2272)

## Summary
- enable session chat topbar Files and Settings panels
- align session main-agent topbar identity with the sidebar main
identity
- source /new-chat Start with a task cards from agent catalog
quick_commands

## Root cause
Session chat reused the shared header but had no-op panel handlers and
treated the main session route as a pack agent. /new-chat still used
local cold-start defaults instead of catalog quick_commands.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false
--noErrorTruncation
- [x] pnpm --dir web run test:unit

Note: pnpm --dir web run tsc currently fails because the repo script
expands to pnpm -r --workspace-concurrency=1 --if-present exec tsc
--noEmit, and this pnpm rejects --if-present for exec.
```

### PR Description

## Summary
- enable session chat topbar Files and Settings panels
- align session main-agent topbar identity with the sidebar main identity
- source /new-chat Start with a task cards from agent catalog quick_commands

## Root cause
Session chat reused the shared header but had no-op panel handlers and treated the main session route as a pack agent. /new-chat still used local cold-start defaults instead of catalog quick_commands.

## Test plan
- [x] pnpm --dir web run lint
- [x] pnpm --dir web/app exec tsc --noEmit --pretty false --noErrorTruncation
- [x] pnpm --dir web run test:unit

Note: pnpm --dir web run tsc currently fails because the repo script expands to pnpm -r --workspace-concurrency=1 --if-present exec tsc --noEmit, and this pnpm rejects --if-present for exec.

---

## [c271635] fix(chat): add session thread typing parity (#2268)

- **SHA**: c271635c37ba402e1e695739ea8415086fad06c8
- **作者**: bill-srp
- **日期**: 2026-06-08T12:01:47Z
- **PR**: #2268
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c271635c37ba402e1e695739ea8415086fad06c8

### 完整 Commit Message

```
fix(chat): add session thread typing parity (#2268)

## Summary
- reuse the main `/chat` Mattermost typewriter pipeline in
session-thread chat
- rename the session-thread seed command from `/zooclaw-thread` to
`/zoo-thread`
- extract session-thread display message derivation to keep the page
under lint complexity limits

## Local checks
- `pnpm --dir web run lint` passed (enterprise-app warnings only)
- `pnpm --dir web run tsc` failed before typechecking because the root
script passes unsupported `--if-present` to `pnpm exec`
- `pnpm --dir web/app exec tsc --noEmit` passed
- `pnpm --dir web run test:unit` passed: 485 files, 6955 tests passed, 1
skipped, 1 todo
- `ruff check .` passed in `services/claw-interface`
- host `pyright app tests` unavailable: `pyright` not installed
- host backend pytest blocked by host Pydantic warning config mismatch
- devcontainer `pyright app tests` passed
- devcontainer focused `pytest
tests/unit/test_openclaw_session_channel_service.py -q` passed: 29 tests
- devcontainer full `pytest --cov=app --cov-report=term-missing
--cov-fail-under=90 -q` failed on unrelated environment/baseline issues:
deptry tests cannot resolve the host git worktree path inside the
container, and total coverage is 88.10% under the 90% gate
```

### PR Description

## Summary
- reuse the main `/chat` Mattermost typewriter pipeline in session-thread chat
- rename the session-thread seed command from `/zooclaw-thread` to `/zoo-thread`
- extract session-thread display message derivation to keep the page under lint complexity limits

## Local checks
- `pnpm --dir web run lint` passed (enterprise-app warnings only)
- `pnpm --dir web run tsc` failed before typechecking because the root script passes unsupported `--if-present` to `pnpm exec`
- `pnpm --dir web/app exec tsc --noEmit` passed
- `pnpm --dir web run test:unit` passed: 485 files, 6955 tests passed, 1 skipped, 1 todo
- `ruff check .` passed in `services/claw-interface`
- host `pyright app tests` unavailable: `pyright` not installed
- host backend pytest blocked by host Pydantic warning config mismatch
- devcontainer `pyright app tests` passed
- devcontainer focused `pytest tests/unit/test_openclaw_session_channel_service.py -q` passed: 29 tests
- devcontainer full `pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` failed on unrelated environment/baseline issues: deptry tests cannot resolve the host git worktree path inside the container, and total coverage is 88.10% under the 90% gate


---

## [9c3f846] fix(api): disable no-card trial grants (#2263)

- **SHA**: 9c3f8467cf8563be865de7353d75c2e2f9a890bd
- **作者**: tim-srp
- **日期**: 2026-06-08T11:58:56Z
- **PR**: #2263
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/9c3f8467cf8563be865de7353d75c2e2f9a890bd

### 完整 Commit Message

```
fix(api): disable no-card trial grants (#2263)

## Summary
- Set invite/open-registration trial constants to 0 while leaving Stripe
checkout trial credits unchanged.
- Add an early guard so disabled invite trials skip Billing v1/v2
lookup, entitlement recording, wallet topup, and user trial updates.
- Cover warm-pool benefit finalization so claiming a pre-provisioned bot
does not grant no-card credits when invite trials are disabled.
- Add the Chinese design spec under docs/superpowers/specs.

## Local validation
- PASS: cd services/claw-interface && pytest
tests/unit/test_user_trial_credits_service.py
tests/unit/test_warm_pool_additional_coverage.py
tests/unit/test_orders_trial_logic.py -q
- PASS: cd services/claw-interface && ruff check .
- PASS: cd services/claw-interface && ruff format --check
app/services/user/trial_credits.py app/settings.py
tests/unit/test_user_trial_credits_service.py
tests/unit/test_warm_pool_additional_coverage.py
- PASS: cd services/claw-interface && pyright --pythonpath
/Users/shiqi/miniconda3/bin/python app/services/user/trial_credits.py
app/settings.py tests/unit/test_user_trial_credits_service.py
tests/unit/test_warm_pool_additional_coverage.py

## Local check notes
- Full local pyright against app/tests reports pre-existing Mongo
wrapper typing issues outside this PR.
- Full local pytest with coverage is blocked in this machine by
google.cloud.logging/protobuf DeprecationWarning during
tests/unit/test_app_logging.py collection, before this PR's tests are
reached; targeted relevant pytest passes.
- Linear CLI is not installed locally, so no ECA issue was created from
this machine.
```

### PR Description

## Summary
- Set invite/open-registration trial constants to 0 while leaving Stripe checkout trial credits unchanged.
- Add an early guard so disabled invite trials skip Billing v1/v2 lookup, entitlement recording, wallet topup, and user trial updates.
- Cover warm-pool benefit finalization so claiming a pre-provisioned bot does not grant no-card credits when invite trials are disabled.
- Add the Chinese design spec under docs/superpowers/specs.

## Local validation
- PASS: cd services/claw-interface && pytest tests/unit/test_user_trial_credits_service.py tests/unit/test_warm_pool_additional_coverage.py tests/unit/test_orders_trial_logic.py -q
- PASS: cd services/claw-interface && ruff check .
- PASS: cd services/claw-interface && ruff format --check app/services/user/trial_credits.py app/settings.py tests/unit/test_user_trial_credits_service.py tests/unit/test_warm_pool_additional_coverage.py
- PASS: cd services/claw-interface && pyright --pythonpath /Users/shiqi/miniconda3/bin/python app/services/user/trial_credits.py app/settings.py tests/unit/test_user_trial_credits_service.py tests/unit/test_warm_pool_additional_coverage.py

## Local check notes
- Full local pyright against app/tests reports pre-existing Mongo wrapper typing issues outside this PR.
- Full local pytest with coverage is blocked in this machine by google.cloud.logging/protobuf DeprecationWarning during tests/unit/test_app_logging.py collection, before this PR's tests are reached; targeted relevant pytest passes.
- Linear CLI is not installed locally, so no ECA issue was created from this machine.

---

## [f539ec8] fix(ci): avoid sudo drop in iOS release notes job (#2267)

- **SHA**: f539ec80319a54433a079f2c1b581da61ea34c9a
- **作者**: bill-srp
- **日期**: 2026-06-08T11:32:13Z
- **PR**: #2267
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/f539ec80319a54433a079f2c1b581da61ea34c9a

### 完整 Commit Message

```
fix(ci): avoid sudo drop in iOS release notes job (#2267)

## Summary
- Configure the Codex release-notes step to use read-only sandboxing and
safety strategy
- Avoid the Blacksmith runner sudo-drop verification failure before App
Store submission starts

## Testing
- ruby -e 'require "yaml";
YAML.load_file(".github/workflows/ios-deploy.yml"); puts "yaml ok"'

## Notes
- Web and backend checks are not applicable; this PR only changes a
GitHub Actions workflow.
```

### PR Description

## Summary
- Configure the Codex release-notes step to use read-only sandboxing and safety strategy
- Avoid the Blacksmith runner sudo-drop verification failure before App Store submission starts

## Testing
- ruby -e 'require "yaml"; YAML.load_file(".github/workflows/ios-deploy.yml"); puts "yaml ok"'

## Notes
- Web and backend checks are not applicable; this PR only changes a GitHub Actions workflow.

---

## [aa2efdb] style(ios): ZooClaw chat Lora typography skin + app background unification (#2141)

- **SHA**: aa2efdb7d05388351a59da9708f4609449f9e82b
- **作者**: shana-srp
- **日期**: 2026-06-08T11:08:48Z
- **PR**: #2141
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/aa2efdb7d05388351a59da9708f4609449f9e82b

### 完整 Commit Message

```
style(ios): ZooClaw chat Lora typography skin + app background unification (#2141)

## 概述
完善 ZooClaw iOS 聊天页的 Lora 排版皮肤，并统一全 App 纯色页底色。本分支也一并包含早前的 Lora 字体安装、Web 端
Lora 皮肤、以及若干 Mattermost 修复提交。

## 排版（Chat / MarkdownTextView）
- **字重三层**：正文 / H3 / 列表 / 引文 = Medium 500；H1 / H2 / strong = SemiBold
600；行内代码 = Regular 400（系统等宽）
- 新增 `.strong`(SemiBold) / `.emphasis`(italic) 样式；em 继承正文 Medium
- 禁用 Bold 700（Lora 700 过粗）

## 表格
- 表头行 + 首列 SemiBold；其余数据列 Medium
- **仅横线**（行间 + 上下边线），无竖线、无外框
- **2:1:1 自适应列宽**：首列固定占表宽 50%，其余列平分剩余（`MeasuredLoraTable` +
`LoraTableColumnWidth`）

## 颜色 / 背景
- AI 消息气泡底色 → `#F8F8F7 @ 40%`（对齐设计稿）
- 导航标题 → 系统字体 17pt Regular
- 全 App 纯色页底色统一 `#F8F8F7`：设置 / 技能商店 / Paywall / 侧边栏 / Onboarding 流程
- 替换聊天背景图 `chat_background.png`（Onboarding 注册页共用）

## 文档
- 新增 `docs/design/zooclaw-lora-typography-spec-ios.md`（iOS 实现规范，字重原则 +
完整代码 + 表格/背景规则）
- 删除旧 `zooclaw5:26-lora-typography-spec.md`（Web CSS 版）

## 测试
- `xcodebuild` iOS Simulator 编译通过（0 错误）
- 模拟器真机验证聊天页：字体 / 字重 / 表格 / AI 气泡底色 / 背景图
- 非聊天页（设置/Paywall/侧边栏/Onboarding）底色为编译验证，建议登录后人工过一遍

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: bill-srp <bill@srp.one>
Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
Co-authored-by: Claude Opus 4.8 <noreply@anthropic.com>
```

### PR Description

## 概述
完善 ZooClaw iOS 聊天页的 Lora 排版皮肤，并统一全 App 纯色页底色。本分支也一并包含早前的 Lora 字体安装、Web 端 Lora 皮肤、以及若干 Mattermost 修复提交。

## 排版（Chat / MarkdownTextView）
- **字重三层**：正文 / H3 / 列表 / 引文 = Medium 500；H1 / H2 / strong = SemiBold 600；行内代码 = Regular 400（系统等宽）
- 新增 `.strong`(SemiBold) / `.emphasis`(italic) 样式；em 继承正文 Medium
- 禁用 Bold 700（Lora 700 过粗）

## 表格
- 表头行 + 首列 SemiBold；其余数据列 Medium
- **仅横线**（行间 + 上下边线），无竖线、无外框
- **2:1:1 自适应列宽**：首列固定占表宽 50%，其余列平分剩余（`MeasuredLoraTable` + `LoraTableColumnWidth`）

## 颜色 / 背景
- AI 消息气泡底色 → `#F8F8F7 @ 40%`（对齐设计稿）
- 导航标题 → 系统字体 17pt Regular
- 全 App 纯色页底色统一 `#F8F8F7`：设置 / 技能商店 / Paywall / 侧边栏 / Onboarding 流程
- 替换聊天背景图 `chat_background.png`（Onboarding 注册页共用）

## 文档
- 新增 `docs/design/zooclaw-lora-typography-spec-ios.md`（iOS 实现规范，字重原则 + 完整代码 + 表格/背景规则）
- 删除旧 `zooclaw5:26-lora-typography-spec.md`（Web CSS 版）

## 测试
- `xcodebuild` iOS Simulator 编译通过（0 错误）
- 模拟器真机验证聊天页：字体 / 字重 / 表格 / AI 气泡底色 / 背景图
- 非聊天页（设置/Paywall/侧边栏/Onboarding）底色为编译验证，建议登录后人工过一遍

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [89f2c6f] ci: enrich docs-merge notification (summary + explicit broadcast) (#2266)

- **SHA**: 89f2c6f939729f0329e28309e9c4f585a08e7825
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T11:03:42Z
- **PR**: #2266
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/89f2c6f939729f0329e28309e9c4f585a08e7825

### 完整 Commit Message

```
ci: enrich docs-merge notification (summary + explicit broadcast) (#2266)

## What
Two improvements to the ZooClaw 开发小组 Lark notification sent when a
sync-docs PR merges:

1. **Change summary** — the message previously had only a title + commit
URL; `prep-notify` now queries the squash commit and adds a one-line
summary (doc count, +/- lines, names):
   ```
   ✅ 文档维护 PR 已合并到 main
   docs: sync-docs weekly sweep (2026-06-08) (#2264)
   📄 改动 2 个文档（+2 / -1）：AGENTS.md、README.md
   🔗 https://…/commit/<sha>
   ```
2. **Explicit `broadcast: true`** — calls `lark-notify-user` with the
new explicit broadcast input (srp-actions #98) so the group message has
no `[未提供 GitHub 用户]` prefix, instead of relying on an empty
`github_login`.

## How
`prep-notify` derives `{file count, additions, deletions, filenames}`
via `gh api repos/…/commits/$SHA` and assembles the full message
(summary omitted if the API call fails); `notify-on-merge` forwards it
and passes `broadcast: true`.

## ⚠️ Merge order
**Merge srp-actions #98 first** — it defines the `broadcast` input. If
this lands on `main` before #98, the next sweep's notify job would fail
with an unknown-input error when it resolves
`lark-notify-user.yml@main`.

## Verification
- YAML parses; `prep-notify` build script is `shellcheck`-clean.
- Summary logic run against the real #2264 merge commit → renders
exactly the block above.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What
Two improvements to the ZooClaw 开发小组 Lark notification sent when a sync-docs PR merges:

1. **Change summary** — the message previously had only a title + commit URL; `prep-notify` now queries the squash commit and adds a one-line summary (doc count, +/- lines, names):
   ```
   ✅ 文档维护 PR 已合并到 main
   docs: sync-docs weekly sweep (2026-06-08) (#2264)
   📄 改动 2 个文档（+2 / -1）：AGENTS.md、README.md
   🔗 https://…/commit/<sha>
   ```
2. **Explicit `broadcast: true`** — calls `lark-notify-user` with the new explicit broadcast input (srp-actions #98) so the group message has no `[未提供 GitHub 用户]` prefix, instead of relying on an empty `github_login`.

## How
`prep-notify` derives `{file count, additions, deletions, filenames}` via `gh api repos/…/commits/$SHA` and assembles the full message (summary omitted if the API call fails); `notify-on-merge` forwards it and passes `broadcast: true`.

## ⚠️ Merge order
**Merge srp-actions #98 first** — it defines the `broadcast` input. If this lands on `main` before #98, the next sweep's notify job would fail with an unknown-input error when it resolves `lark-notify-user.yml@main`.

## Verification
- YAML parses; `prep-notify` build script is `shellcheck`-clean.
- Summary logic run against the real #2264 merge commit → renders exactly the block above.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [b089a89] feat(web): activate New Chat from sidebar (#2247)

- **SHA**: b089a8950908f2f7db7c38fcb274231ba6d5d473
- **作者**: bill-srp
- **日期**: 2026-06-08T10:58:18Z
- **PR**: #2247
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/b089a8950908f2f7db7c38fcb274231ba6d5d473

### 完整 Commit Message

```
feat(web): activate New Chat from sidebar (#2247)

## Linear

https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Final activation split from #2216, stacked on #2246. This is the PR that
puts the New Chat/session-thread feature online through sidebar and
redirect entry points.

- Add visible New Chat nav entry and localized nav label.
- Restructure sidebar into top nav, scrollable agent/session zone, and
pinned footer.
- Add expandable agent rows with per-agent New chat and past session
links.
- Auto-expand/highlight the active session route's agent.
- Change default logged-in landing/post-auth destinations to /new-chat
while preserving valid specialist landing redirects.

## Production exposure
This is intentionally the activation PR. Earlier stack PRs add hidden
route, API plumbing, and thread behavior without normal navigation
exposure.

## Test plan
- pnpm --dir web/app exec vitest run
tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts
tests/unit/app/onboarding/OnboardingSuccessClient.unit.spec.tsx
tests/unit/app/subscription/SuccessClient.unit.spec.tsx
tests/unit/app/user-verify-email-otp.unit.spec.tsx
tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx
tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx
tests/unit/components/sidenav/SideNavBottomNav.unit.spec.tsx
tests/unit/components/sidenav/SideNavUserSection.unit.spec.tsx
tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts
tests/unit/components/sidenav/session-route.unit.spec.ts
tests/unit/lib/landing-context.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- #2244 hidden /new-chat launcher
- #2245 OpenClaw conversation API plumbing
- #2246 session-thread route and hidden send behavior
- This PR: sidebar + redirect activation
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Final activation split from #2216, stacked on #2246. This is the PR that puts the New Chat/session-thread feature online through sidebar and redirect entry points.

- Add visible New Chat nav entry and localized nav label.
- Restructure sidebar into top nav, scrollable agent/session zone, and pinned footer.
- Add expandable agent rows with per-agent New chat and past session links.
- Auto-expand/highlight the active session route's agent.
- Change default logged-in landing/post-auth destinations to /new-chat while preserving valid specialist landing redirects.

## Production exposure
This is intentionally the activation PR. Earlier stack PRs add hidden route, API plumbing, and thread behavior without normal navigation exposure.

## Test plan
- pnpm --dir web/app exec vitest run tests/unit/app/landing/hooks/useLandingRedirect.unit.spec.ts tests/unit/app/onboarding/OnboardingSuccessClient.unit.spec.tsx tests/unit/app/subscription/SuccessClient.unit.spec.tsx tests/unit/app/user-verify-email-otp.unit.spec.tsx tests/unit/components/sidenav/SideNavAgentList.unit.spec.tsx tests/unit/components/sidenav/SideNavAgentSessions.unit.spec.tsx tests/unit/components/sidenav/SideNavBottomNav.unit.spec.tsx tests/unit/components/sidenav/SideNavUserSection.unit.spec.tsx tests/unit/components/sidenav/build-bottom-nav-items.unit.spec.ts tests/unit/components/sidenav/session-route.unit.spec.ts tests/unit/lib/landing-context.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- #2244 hidden /new-chat launcher
- #2245 OpenClaw conversation API plumbing
- #2246 session-thread route and hidden send behavior
- This PR: sidebar + redirect activation

---

## [4440663] docs: sync-docs weekly sweep (2026-06-08) (#2264)

- **SHA**: 4440663f94d1654ff444dfc079b8d866ec9d4dba
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-06-08T10:37:33Z
- **PR**: #2264
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4440663f94d1654ff444dfc079b8d866ec9d4dba

### 完整 Commit Message

```
docs: sync-docs weekly sweep (2026-06-08) (#2264)

## Tier 1 — Deterministic fixes

_None — `drift-probe.sh` reported clean._

## Tier 2 — Semantic fixes (evidence-grounded)

- **`AGENTS.md` — stale file paths in "Related repos"** (`web/src/app/…`
→ `web/app/src/app/…`)
Evidence: files confirmed at
`web/app/src/app/landing/LandingClient.tsx`,
`web/app/src/app/[locale]/userguide/UserGuideClient.tsx`,
`web/app/src/app/[locale]/pricing/PublicPricingClient.tsx`; the old
`web/src/app/` prefix does not exist. The `web/src/*` → `web/app/src/*`
rename was already captured as a known drift source in
`.claude/skills/sync-docs/references/drift-sources.md` (A1) but had not
been applied to the AGENTS.md "Related repos" paragraph.

- **`README.md` CI table — `docs-auto-merge.yml` not listed**
Evidence: `.github/workflows/docs-auto-merge.yml` added in commit
`0e8d1403` (`ci: auto-merge sync-docs PRs + notify dev group`). The
workflow gates, auto-approves, and squash-merges sync-docs doc-only PRs;
notifies ZooClaw 开发小组 on merge. Added a row alongside `auto-merge.yml`
in the CI table.

## Tier 3 — Suggestions (not applied)

_None identified in this window._

---

**Docs changed:** `README.md`, `AGENTS.md`
**Review window:** `bb9534a4..HEAD` (1 commit: `0e8d1403 ci: auto-merge
sync-docs PRs + notify dev group`)

Co-authored-by: ecap-bot <ecap-bot@users.noreply.github.com>
```

### PR Description

## Tier 1 — Deterministic fixes

_None — `drift-probe.sh` reported clean._

## Tier 2 — Semantic fixes (evidence-grounded)

- **`AGENTS.md` — stale file paths in "Related repos"** (`web/src/app/…` → `web/app/src/app/…`)
  Evidence: files confirmed at `web/app/src/app/landing/LandingClient.tsx`, `web/app/src/app/[locale]/userguide/UserGuideClient.tsx`, `web/app/src/app/[locale]/pricing/PublicPricingClient.tsx`; the old `web/src/app/` prefix does not exist. The `web/src/*` → `web/app/src/*` rename was already captured as a known drift source in `.claude/skills/sync-docs/references/drift-sources.md` (A1) but had not been applied to the AGENTS.md "Related repos" paragraph.

- **`README.md` CI table — `docs-auto-merge.yml` not listed**
  Evidence: `.github/workflows/docs-auto-merge.yml` added in commit `0e8d1403` (`ci: auto-merge sync-docs PRs + notify dev group`). The workflow gates, auto-approves, and squash-merges sync-docs doc-only PRs; notifies ZooClaw 开发小组 on merge. Added a row alongside `auto-merge.yml` in the CI table.

## Tier 3 — Suggestions (not applied)

_None identified in this window._

---

**Docs changed:** `README.md`, `AGENTS.md`
**Review window:** `bb9534a4..HEAD` (1 commit: `0e8d1403 ci: auto-merge sync-docs PRs + notify dev group`)

---

## [8e56e9b] fix(observability): upload web sourcemaps to Sentry and split hooks-violation grouping (ECA-874) (#2262)

- **SHA**: 8e56e9bf1b546c02757f473b7143f5b3358d321a
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T10:35:42Z
- **PR**: #2262
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8e56e9bf1b546c02757f473b7143f5b3358d321a

### 完整 Commit Message

```
fix(observability): upload web sourcemaps to Sentry and split hooks-violation grouping (ECA-874) (#2262)

## Summary

ECA-874 ("Rendered more hooks than during the previous render") could
not be root-caused because **the deploy builds the web app without
`SENTRY_AUTH_TOKEN`**, so `@sentry/nextjs` (`withSentryConfig`) silently
no-ops its sourcemap/debug-ID upload. Every ecap-website client error
reaches Sentry as a minified, React-internal-only stack with **no app
frames**.

Investigation also showed `ECAP-WEBSITE-MZ` is **not a single bug** —
it's a Sentry grouping bucket. Its two retained events are different
pages, releases, and domains:

| | oldest (2026-04-28) | latest (2026-06-01) |
|---|---|---|
| transaction | `/:locale/chat` | `/:locale/integrations/connector` |
| url | `zooclaw.ai/zh/chat` | `…/en/composio-connectors` |
| release | `9455b9e4` | `8376b387` |

The generic message + identical minified React-internal stack made
Sentry merge unrelated rules-of-hooks violations across pages into one
un-actionable issue.

## Changes

- **`deploy.yml`** — pass `SENTRY_AUTH_TOKEN` to the `Build OpenNext`
step (the build that emits the deployed `.next/static` chunks) so the
upload actually runs. Secret already exists in the repo (used by
`ios-deploy.yml`).
- **`sentry.client.config.ts`** — fingerprint React rules-of-hooks
violations by `transaction`/route so `/chat` and
`/integrations/connector` stop merging. Lands beside the existing
hydration / chunk-load grouping. +3 unit tests.

## Code-audit note

The `/integrations/connector` component tree at the erroring release
(`ComposioConnectorsClient` + `useComposioConnectors` +
`useEnableOAuthReturnAfterConnect` + shared `useAuth` /
`useAuthSnapshot` / `useTranslation` / `useLoginCheck`) has **no
conditional hooks** — all hooks sit above the early returns. There is no
static defect there to fix; this PR unblocks future triage rather than
patching a single call site.

## Expectation

Go-forward only — the 3 existing events were built without the token and
won't be retroactively symbolicated. The next hooks violation after this
deploys will carry an app stack + component name
(`reactComponentAnnotation` is enabled).

## Verification
- `pnpm vitest run tests/unit/config/sentry-client-config.unit.spec.ts`
→ 17 passed
- `deploy.yml` validated as well-formed YAML

Linear:
https://linear.app/srpone/issue/ECA-874/react-rendered-more-hooks-than-during-the-previous-render

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## Follow-up commits (review feedback + observability hardening)

- **`d5f8985`** — rate-limit hooks-violation events per route (Codex
finding): the global `beforeSend` limiter keyed on `fingerprint[0]`
only, so all routes shared one 5/5min bucket. Now keys on the full
fingerprint, giving the route key its own bucket while single-element
fingerprints are unchanged.
- **`9166b96`** — (1) set Sentry `environment` on both client
(`NEXT_PUBLIC_APP_ENV`) and server/edge (`APP_ENV` wrangler var) inits,
so production vs staging are distinguishable — previously every deploy
reported as `production`. (2) Add `SENTRY_AUTH_TOKEN` to the deploy
"Validate required variables" gate: a missing token makes the
@sentry/nextjs plugin *silently* skip the upload (no error → green
build), so the gate now fails the deploy red instead.

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

ECA-874 ("Rendered more hooks than during the previous render") could not be root-caused because **the deploy builds the web app without `SENTRY_AUTH_TOKEN`**, so `@sentry/nextjs` (`withSentryConfig`) silently no-ops its sourcemap/debug-ID upload. Every ecap-website client error reaches Sentry as a minified, React-internal-only stack with **no app frames**.

Investigation also showed `ECAP-WEBSITE-MZ` is **not a single bug** — it's a Sentry grouping bucket. Its two retained events are different pages, releases, and domains:

| | oldest (2026-04-28) | latest (2026-06-01) |
|---|---|---|
| transaction | `/:locale/chat` | `/:locale/integrations/connector` |
| url | `zooclaw.ai/zh/chat` | `…/en/composio-connectors` |
| release | `9455b9e4` | `8376b387` |

The generic message + identical minified React-internal stack made Sentry merge unrelated rules-of-hooks violations across pages into one un-actionable issue.

## Changes

- **`deploy.yml`** — pass `SENTRY_AUTH_TOKEN` to the `Build OpenNext` step (the build that emits the deployed `.next/static` chunks) so the upload actually runs. Secret already exists in the repo (used by `ios-deploy.yml`).
- **`sentry.client.config.ts`** — fingerprint React rules-of-hooks violations by `transaction`/route so `/chat` and `/integrations/connector` stop merging. Lands beside the existing hydration / chunk-load grouping. +3 unit tests.

## Code-audit note

The `/integrations/connector` component tree at the erroring release (`ComposioConnectorsClient` + `useComposioConnectors` + `useEnableOAuthReturnAfterConnect` + shared `useAuth` / `useAuthSnapshot` / `useTranslation` / `useLoginCheck`) has **no conditional hooks** — all hooks sit above the early returns. There is no static defect there to fix; this PR unblocks future triage rather than patching a single call site.

## Expectation

Go-forward only — the 3 existing events were built without the token and won't be retroactively symbolicated. The next hooks violation after this deploys will carry an app stack + component name (`reactComponentAnnotation` is enabled).

## Verification
- `pnpm vitest run tests/unit/config/sentry-client-config.unit.spec.ts` → 17 passed
- `deploy.yml` validated as well-formed YAML

Linear: https://linear.app/srpone/issue/ECA-874/react-rendered-more-hooks-than-during-the-previous-render

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## Follow-up commits (review feedback + observability hardening)

- **`d5f8985`** — rate-limit hooks-violation events per route (Codex finding): the global `beforeSend` limiter keyed on `fingerprint[0]` only, so all routes shared one 5/5min bucket. Now keys on the full fingerprint, giving the route key its own bucket while single-element fingerprints are unchanged.
- **`9166b96`** — (1) set Sentry `environment` on both client (`NEXT_PUBLIC_APP_ENV`) and server/edge (`APP_ENV` wrangler var) inits, so production vs staging are distinguishable — previously every deploy reported as `production`. (2) Add `SENTRY_AUTH_TOKEN` to the deploy "Validate required variables" gate: a missing token makes the @sentry/nextjs plugin *silently* skip the upload (no error → green build), so the gate now fails the deploy red instead.

---

## [0e8d140] ci: auto-merge sync-docs PRs + notify dev group (#2261)

- **SHA**: 0e8d14032feddd46c6a06f156206d71666ff3767
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T10:29:32Z
- **PR**: #2261
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0e8d14032feddd46c6a06f156206d71666ff3767

### 完整 Commit Message

```
ci: auto-merge sync-docs PRs + notify dev group (#2261)

## What

Add `.github/workflows/docs-auto-merge.yml` — auto-merge for the
documentation PRs the `sync-docs` skill opens, plus a Lark notification
to **ZooClaw 开发小组** on merge.

## Gates (all must hold to auto-merge)

A PR qualifies only if it's a sync-docs PR — branch `chore/sync-docs-*`,
title `docs: sync-docs …`, authored by the docs bot, same-repo (forks
excluded) — **and**:

1. **Docs-only (no code)** — every changed file is in the strict 7-file
allowlist (`README.md`, `architecture.md`, `architecture.zh-CN.md`, and
the four `AGENTS.md`). Any other path ⇒ not merged. This is the
strongest "no code changed" guarantee.
2. **No blocking review label** — `cc:need-human-review` /
`gpt:need-human-review` (the user-mandated gate), plus
`cc:request-changes` / `gpt:request-changes` as defense (those already
turn the required `auto-review` gate red via the fail-closed parser).
3. **No already-failed check** (one-time snapshot, mirrors
`auto-merge.yml`).

Then `gh pr merge --auto --squash` hands off to GitHub: native
auto-merge waits for **all required checks + the merge queue
(ALLGREEN)** before squash-merging — satisfying "all checks pass first".
`labeled`/`unlabeled`/`synchronize` re-evaluate, and `--disable-auto`
revokes if a blocking label arrives after auto-merge was enabled (the
late-codex-label race).

## Notify

On `push` to `main`, when the squash subject starts with `docs:
sync-docs`, a job calls
`srp-actions/.github/workflows/lark-notify-user.yml@main` with an
**empty `github_login`** — the reusable's empty-login path posts
directly to `fallback_chat_id` = `vars.LARK_CHAT_DEV_GROUP` (ZooClaw
开发小组). Using `push` (not `pull_request: closed`) keeps the workflow
version pinned to main's, since the squash-merge deletes the PR head
branch. A small `prep-notify` job extracts just the commit subject so
the message stays a one-liner.

## Reuses
- `auto-merge.yml` — App token + failed-check snapshot + `--auto
--squash`.
- `code-quality.yml` `notify-ios-author-on-failure` — exact
`lark-notify-user.yml@main` interface (`fallback_chat_id`,
`user_mapping_json`, `enabled`, `secrets: inherit`).

## Verification
- YAML parses; gate logic `shellcheck`-clean.
- Offline gate matrix against #2255's real data — 7 cases all correct:
docs-only→ENABLE, +code→REJECT, +need-human-review→REJECT,
+request-changes→REJECT, README-subset→ENABLE, wrong-title→SKIP,
human-author→SKIP.
- Resolved an author-login footgun: event payload is
`srp-claude-assistant[bot]` (not `gh`'s `app/…` display); gate matches
the slug substring.

## Rollout (after merge)
1. Existing #2255 won't auto-trigger (its head branch predates this
workflow; `pull_request` uses the head branch's workflow copy) — merge
it manually as the baseline.
2. End-to-end: `gh workflow run docs-maintenance.yml -f dry_run=false`
opens a fresh sync-docs PR (branched from main, which now contains this
workflow) → observe auto-merge + the dev-group notification.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Add `.github/workflows/docs-auto-merge.yml` — auto-merge for the documentation PRs the `sync-docs` skill opens, plus a Lark notification to **ZooClaw 开发小组** on merge.

## Gates (all must hold to auto-merge)

A PR qualifies only if it's a sync-docs PR — branch `chore/sync-docs-*`, title `docs: sync-docs …`, authored by the docs bot, same-repo (forks excluded) — **and**:

1. **Docs-only (no code)** — every changed file is in the strict 7-file allowlist (`README.md`, `architecture.md`, `architecture.zh-CN.md`, and the four `AGENTS.md`). Any other path ⇒ not merged. This is the strongest "no code changed" guarantee.
2. **No blocking review label** — `cc:need-human-review` / `gpt:need-human-review` (the user-mandated gate), plus `cc:request-changes` / `gpt:request-changes` as defense (those already turn the required `auto-review` gate red via the fail-closed parser).
3. **No already-failed check** (one-time snapshot, mirrors `auto-merge.yml`).

Then `gh pr merge --auto --squash` hands off to GitHub: native auto-merge waits for **all required checks + the merge queue (ALLGREEN)** before squash-merging — satisfying "all checks pass first". `labeled`/`unlabeled`/`synchronize` re-evaluate, and `--disable-auto` revokes if a blocking label arrives after auto-merge was enabled (the late-codex-label race).

## Notify

On `push` to `main`, when the squash subject starts with `docs: sync-docs`, a job calls `srp-actions/.github/workflows/lark-notify-user.yml@main` with an **empty `github_login`** — the reusable's empty-login path posts directly to `fallback_chat_id` = `vars.LARK_CHAT_DEV_GROUP` (ZooClaw 开发小组). Using `push` (not `pull_request: closed`) keeps the workflow version pinned to main's, since the squash-merge deletes the PR head branch. A small `prep-notify` job extracts just the commit subject so the message stays a one-liner.

## Reuses
- `auto-merge.yml` — App token + failed-check snapshot + `--auto --squash`.
- `code-quality.yml` `notify-ios-author-on-failure` — exact `lark-notify-user.yml@main` interface (`fallback_chat_id`, `user_mapping_json`, `enabled`, `secrets: inherit`).

## Verification
- YAML parses; gate logic `shellcheck`-clean.
- Offline gate matrix against #2255's real data — 7 cases all correct: docs-only→ENABLE, +code→REJECT, +need-human-review→REJECT, +request-changes→REJECT, README-subset→ENABLE, wrong-title→SKIP, human-author→SKIP.
- Resolved an author-login footgun: event payload is `srp-claude-assistant[bot]` (not `gh`'s `app/…` display); gate matches the slug substring.

## Rollout (after merge)
1. Existing #2255 won't auto-trigger (its head branch predates this workflow; `pull_request` uses the head branch's workflow copy) — merge it manually as the baseline.
2. End-to-end: `gh workflow run docs-maintenance.yml -f dry_run=false` opens a fresh sync-docs PR (branched from main, which now contains this workflow) → observe auto-merge + the dev-group notification.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [bb9534a] docs: sync-docs weekly sweep (2026-06-08) (#2255)

- **SHA**: bb9534a4a23cb6c8d22d6dbf6407c6961cc29054
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-06-08T10:12:40Z
- **PR**: #2255
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/bb9534a4a23cb6c8d22d6dbf6407c6961cc29054

### 完整 Commit Message

```
docs: sync-docs weekly sweep (2026-06-08) (#2255)

## Tier 1 — Deterministic fixes

_Probe found no Tier-1 hits (all README assertions + versions were
clean)._

## Tier 2 — Semantic fixes (evidence-grounded)

- **`architecture.md` + `architecture.zh-CN.md` — stale `web/src/…` code
refs**
- Evidence: files
`web/app/src/components/providers/MattermostProvider.tsx` and
`web/app/src/lib/mattermost/blob.ts` exist at `web/app/src/…` path; the
old `web/src/…` prefix no longer exists (the `web/` sub-workspace
restructure moved source under `web/app/src/`).
- Fix: updated both code-ref bullets in the Chat data plane section (EN
+ 中文).

- **`web/AGENTS.md` layout tree and `pnpm-workspace.yaml` comment —
missing apps and packages**
- Evidence: `web/pnpm-workspace.yaml` currently lists `app`,
`enterprise-admin`, `enterprise-app`, `dashboard-console`, and
`packages/*`; `web/` directory contains all four app subdirs plus a live
`packages/` (with `auth-client`, `chat-ui`). The old layout tree showed
only `app/` and marked `packages/` as "(future)".
- Fix: expanded the layout tree to include all four apps; updated the
`pnpm-workspace.yaml` comment to drop the now-stale `['app']` literal;
updated the `packages/` comment to reflect real packages.

- **`web/AGENTS.md` Package naming — missing
`@zooclaw/dashboard-console`**
- Evidence: `web/dashboard-console/package.json` declares `"name":
"@zooclaw/dashboard-console"`.
  - Fix: added `@zooclaw/dashboard-console` to the deployable-apps list.

- **`services/claw-interface/AGENTS.md` — stale env var
`NEXT_PUBLIC_GATEWAY_URL`**
- Evidence: `NEXT_PUBLIC_GATEWAY_URL` was renamed to
`CLAW_INTERFACE_URL` (confirmed in `web/app/AGENTS.md` mock-backend
section and `drift-sources.md` worked examples); no reference to
`NEXT_PUBLIC_GATEWAY_URL` in current frontend code.
- Fix: updated the Monorepo Context wiring note to
`CLAW_INTERFACE_URL=http://localhost:8000`.

## Tier 3 — Suggestions (not applied)

- `services/claw-interface/AGENTS.md` Monorepo Context table still lists
`ecap-agent-platform (external) | 8001` — this external service still
has a code reference (`AGENT_PLATFORM_URL` in `settings.py` and
`session/chat.py`), so it is technically still used. Whether it deserves
a more detailed description (or removal if fully deprecated) is a
judgment call for the team.

---

**Docs changed:** `architecture.md`, `architecture.zh-CN.md`,
`web/AGENTS.md`, `services/claw-interface/AGENTS.md`

**Window reviewed:** `e1e9995f..HEAD` (~1848 commits; anchor = commit
just before the last 90-day window, no prior sync-docs commit found)

Co-authored-by: ecap-bot <ecap-bot@users.noreply.github.com>
```

### PR Description

## Tier 1 — Deterministic fixes

_Probe found no Tier-1 hits (all README assertions + versions were clean)._

## Tier 2 — Semantic fixes (evidence-grounded)

- **`architecture.md` + `architecture.zh-CN.md` — stale `web/src/…` code refs**
  - Evidence: files `web/app/src/components/providers/MattermostProvider.tsx` and `web/app/src/lib/mattermost/blob.ts` exist at `web/app/src/…` path; the old `web/src/…` prefix no longer exists (the `web/` sub-workspace restructure moved source under `web/app/src/`).
  - Fix: updated both code-ref bullets in the Chat data plane section (EN + 中文).

- **`web/AGENTS.md` layout tree and `pnpm-workspace.yaml` comment — missing apps and packages**
  - Evidence: `web/pnpm-workspace.yaml` currently lists `app`, `enterprise-admin`, `enterprise-app`, `dashboard-console`, and `packages/*`; `web/` directory contains all four app subdirs plus a live `packages/` (with `auth-client`, `chat-ui`). The old layout tree showed only `app/` and marked `packages/` as "(future)".
  - Fix: expanded the layout tree to include all four apps; updated the `pnpm-workspace.yaml` comment to drop the now-stale `['app']` literal; updated the `packages/` comment to reflect real packages.

- **`web/AGENTS.md` Package naming — missing `@zooclaw/dashboard-console`**
  - Evidence: `web/dashboard-console/package.json` declares `"name": "@zooclaw/dashboard-console"`.
  - Fix: added `@zooclaw/dashboard-console` to the deployable-apps list.

- **`services/claw-interface/AGENTS.md` — stale env var `NEXT_PUBLIC_GATEWAY_URL`**
  - Evidence: `NEXT_PUBLIC_GATEWAY_URL` was renamed to `CLAW_INTERFACE_URL` (confirmed in `web/app/AGENTS.md` mock-backend section and `drift-sources.md` worked examples); no reference to `NEXT_PUBLIC_GATEWAY_URL` in current frontend code.
  - Fix: updated the Monorepo Context wiring note to `CLAW_INTERFACE_URL=http://localhost:8000`.

## Tier 3 — Suggestions (not applied)

- `services/claw-interface/AGENTS.md` Monorepo Context table still lists `ecap-agent-platform (external) | 8001` — this external service still has a code reference (`AGENT_PLATFORM_URL` in `settings.py` and `session/chat.py`), so it is technically still used. Whether it deserves a more detailed description (or removal if fully deprecated) is a judgment call for the team.

---

**Docs changed:** `architecture.md`, `architecture.zh-CN.md`, `web/AGENTS.md`, `services/claw-interface/AGENTS.md`

**Window reviewed:** `e1e9995f..HEAD` (~1848 commits; anchor = commit just before the last 90-day window, no prior sync-docs commit found)

---

## [b923970] fix: avoid stale websocket close race (#2260)

- **SHA**: b9239706a8dfb8a548ba29021b7042561553ba39
- **作者**: kaka-srp
- **日期**: 2026-06-08T09:49:21Z
- **PR**: #2260
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/b9239706a8dfb8a548ba29021b7042561553ba39

### 完整 Commit Message

```
fix: avoid stale websocket close race (#2260)

## Summary
- ignore lifecycle-cleared OpenClaw handshake requests so local
reconnect/close cleanup does not get reported as `handshake_rejected`
- guard `onclose` against stale WebSocket instances so a late close from
a replaced socket cannot clear the active connection state
- keep heartbeat force-close routed through the current socket `onclose`
handler so reconnect scheduling remains consistent

## Context
Sentry event `ECAP-WEBSITE-8W` showed `handshake_rejected / Connection
reset` around 2026-06-08 14:50 BJT for user `7300435809222098944`.
Runtime logs point to an OpenClaw/Mattermost stall and reset, but the
frontend was also classifying local cleanup paths as handshake
rejection. During review, the stale socket `onclose` race was confirmed
as real and fixed here.

Linear: ECA-914

## Validation
- `./node_modules/.bin/tsc --noEmit` from `web/app`
- `corepack pnpm --filter @zooclaw/web-app test:unit --
useOpenClawWebSocket`
```

### PR Description

## Summary
- ignore lifecycle-cleared OpenClaw handshake requests so local reconnect/close cleanup does not get reported as `handshake_rejected`
- guard `onclose` against stale WebSocket instances so a late close from a replaced socket cannot clear the active connection state
- keep heartbeat force-close routed through the current socket `onclose` handler so reconnect scheduling remains consistent

## Context
Sentry event `ECAP-WEBSITE-8W` showed `handshake_rejected / Connection reset` around 2026-06-08 14:50 BJT for user `7300435809222098944`. Runtime logs point to an OpenClaw/Mattermost stall and reset, but the frontend was also classifying local cleanup paths as handshake rejection. During review, the stale socket `onclose` race was confirmed as real and fixed here.

Linear: ECA-914

## Validation
- `./node_modules/.bin/tsc --noEmit` from `web/app`
- `corepack pnpm --filter @zooclaw/web-app test:unit -- useOpenClawWebSocket`


---

## [6e3162d] fix(billing): cap subscription trial credits (#2259)

- **SHA**: 6e3162d328302be3a6f7c1dc27692808f7e2d1b5
- **作者**: kaka-srp
- **日期**: 2026-06-08T09:45:50Z
- **PR**: #2259
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6e3162d328302be3a6f7c1dc27692808f7e2d1b5

### 完整 Commit Message

```
fix(billing): cap subscription trial credits (#2259)

## Summary
- Cap Stripe subscription trial entitlements at the configured trial
credit grant instead of plan credits.
- Make Stripe and Antom subscription payment-order credits
service-authoritative, ignoring client or stale order `credits_amount`
for trial and paid subscription flows.
- Keep paid subscription credits plan-based.

## Root cause
Stripe trial entitlement used `credits_for_plan(plan)`, so a starter
trial could grant 4800 credits instead of the configured 1000 trial
credits. Stripe and Antom subscription payment-order recording also
preserved existing `credits_amount` from local order data when present,
so client-provided or stale order values could drift from server-side
billing policy.

## Test plan
- [x] `cd services/claw-interface && ruff check
app/services/antom/billing_v2_records.py
app/services/stripe/billing_v2_entitlements.py
app/services/stripe/billing_v2_records.py
tests/unit/test_antom_billing_v2.py
tests/unit/test_billing_v2_entitlement_helpers.py
tests/unit/test_stripe_billing_v2.py`
- [x] `cd services/claw-interface && python -m pytest
tests/unit/test_billing_v2_entitlement_helpers.py
tests/unit/test_stripe_billing_v2.py tests/unit/test_antom_billing_v2.py
-q`
- [x] `cd services/claw-interface && ruff check .`
- [x] `cd services/claw-interface && pyright app tests`
- [ ] `cd services/claw-interface && python -m pytest --cov=app
--cov-report=term-missing --cov-fail-under=90 -q` was started and
stopped at the user's request because it was too slow; it reached 43%
with no failures before termination.

Note: this fixes future grants/records. Existing over-granted Stripe
trial entitlements or wallet balances need a separate operational
remediation if we decide to correct historical data.
```

### PR Description

## Summary
- Cap Stripe subscription trial entitlements at the configured trial credit grant instead of plan credits.
- Make Stripe and Antom subscription payment-order credits service-authoritative, ignoring client or stale order `credits_amount` for trial and paid subscription flows.
- Keep paid subscription credits plan-based.

## Root cause
Stripe trial entitlement used `credits_for_plan(plan)`, so a starter trial could grant 4800 credits instead of the configured 1000 trial credits. Stripe and Antom subscription payment-order recording also preserved existing `credits_amount` from local order data when present, so client-provided or stale order values could drift from server-side billing policy.

## Test plan
- [x] `cd services/claw-interface && ruff check app/services/antom/billing_v2_records.py app/services/stripe/billing_v2_entitlements.py app/services/stripe/billing_v2_records.py tests/unit/test_antom_billing_v2.py tests/unit/test_billing_v2_entitlement_helpers.py tests/unit/test_stripe_billing_v2.py`
- [x] `cd services/claw-interface && python -m pytest tests/unit/test_billing_v2_entitlement_helpers.py tests/unit/test_stripe_billing_v2.py tests/unit/test_antom_billing_v2.py -q`
- [x] `cd services/claw-interface && ruff check .`
- [x] `cd services/claw-interface && pyright app tests`
- [ ] `cd services/claw-interface && python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` was started and stopped at the user's request because it was too slow; it reached 43% with no failures before termination.

Note: this fixes future grants/records. Existing over-granted Stripe trial entitlements or wallet balances need a separate operational remediation if we decide to correct historical data.


---

## [df6d932] fix(ci): 拆分 CI 通知 fallback 群并命名化 chat id (#2258)

- **SHA**: df6d93219472e4833cd932e6171b02a26975aafc
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T09:01:56Z
- **PR**: #2258
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/df6d93219472e4833cd932e6171b02a26975aafc

### 完整 Commit Message

```
fix(ci): 拆分 CI 通知 fallback 群并命名化 chat id (#2258)

## 背景

当前所有 CI/CD 飞书通知共用同一个硬编码群 `oc_213291d2715a9d02bf5b0bb18b847e3c`（真实群名
**ZooClaw Launch Tracking**）：它既是 `release-notify-lark.yml` 的发版群，又是所有
code-quality / deploy 通知的 `fallback_chat_id`。

两个问题：
1. **可读性**：yml 里只能看到一串 `oc_...` id，看不出对应哪个群。
2. **路由错误**：lint 等 PR 过程检查失败、且找不到对应飞书用户时，错误降级进了**发版群**，不该打扰发版群。

## 改动

- **`code-quality.yml`（5 处 lint/PR fallback）** →
`vars.LARK_CHAT_DEV_GROUP`，回退到 **ZooClaw
开发小组**（`oc_59e29ffc2ed677c28f915dcaac47a3ed`），不再进发版群。
- **`deploy.yml` / `service-deploy.yml` / `release-notify-lark.yml`** →
`vars.LARK_CHAT_RELEASE_GROUP`，群不变（仍 **ZooClaw Launch Tracking**），仅命名化。
- 机制：`${{ vars.<NAME> || 'oc_...字面量'
}}`——变量名给语义、字面量给兜底。**变量未建也能跑**（走字面量），合并即生效；之后建变量即可不改代码换群。

群名均经 lark-cli 核实（`im +chat-search` / `chats.get`）。

## 变量（可选，集中管理）

字面量兜底已保证合并即生效，变量为可选覆盖：

```bash
gh variable set LARK_CHAT_DEV_GROUP     -b oc_59e29ffc2ed677c28f915dcaac47a3ed
gh variable set LARK_CHAT_RELEASE_GROUP -b oc_213291d2715a9d02bf5b0bb18b847e3c
```

## 不做

- 不改 `srp-actions`（`fallback_chat_id` 已是入参）。
- 不动 `e2e.yml`（走自定义机器人 webhook，与 chat_id 回退无关）。
- 不改 deploy/service-deploy 的回退**路由**（仅命名化）。

## 验证

- grep 自检：开发小组 id 仅出现在 code-quality 5 处兜底；发版群 id 仅出现在
deploy/service-deploy/release 兜底；无裸 id。
- 4 个 workflow YAML 解析通过。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景

当前所有 CI/CD 飞书通知共用同一个硬编码群 `oc_213291d2715a9d02bf5b0bb18b847e3c`（真实群名 **ZooClaw Launch Tracking**）：它既是 `release-notify-lark.yml` 的发版群，又是所有 code-quality / deploy 通知的 `fallback_chat_id`。

两个问题：
1. **可读性**：yml 里只能看到一串 `oc_...` id，看不出对应哪个群。
2. **路由错误**：lint 等 PR 过程检查失败、且找不到对应飞书用户时，错误降级进了**发版群**，不该打扰发版群。

## 改动

- **`code-quality.yml`（5 处 lint/PR fallback）** → `vars.LARK_CHAT_DEV_GROUP`，回退到 **ZooClaw 开发小组**（`oc_59e29ffc2ed677c28f915dcaac47a3ed`），不再进发版群。
- **`deploy.yml` / `service-deploy.yml` / `release-notify-lark.yml`** → `vars.LARK_CHAT_RELEASE_GROUP`，群不变（仍 **ZooClaw Launch Tracking**），仅命名化。
- 机制：`${{ vars.<NAME> || 'oc_...字面量' }}`——变量名给语义、字面量给兜底。**变量未建也能跑**（走字面量），合并即生效；之后建变量即可不改代码换群。

群名均经 lark-cli 核实（`im +chat-search` / `chats.get`）。

## 变量（可选，集中管理）

字面量兜底已保证合并即生效，变量为可选覆盖：

```bash
gh variable set LARK_CHAT_DEV_GROUP     -b oc_59e29ffc2ed677c28f915dcaac47a3ed
gh variable set LARK_CHAT_RELEASE_GROUP -b oc_213291d2715a9d02bf5b0bb18b847e3c
```

## 不做

- 不改 `srp-actions`（`fallback_chat_id` 已是入参）。
- 不动 `e2e.yml`（走自定义机器人 webhook，与 chat_id 回退无关）。
- 不改 deploy/service-deploy 的回退**路由**（仅命名化）。

## 验证

- grep 自检：开发小组 id 仅出现在 code-quality 5 处兜底；发版群 id 仅出现在 deploy/service-deploy/release 兜底；无裸 id。
- 4 个 workflow YAML 解析通过。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [d5311bd] ci(ios): pin simulator runtime to iOS 18.6 (#2257)

- **SHA**: d5311bd3f1905490a342d050616417068919050d
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T08:53:53Z
- **PR**: #2257
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/d5311bd3f1905490a342d050616417068919050d

### 完整 Commit Message

```
ci(ios): pin simulator runtime to iOS 18.6 (#2257)

## 问题

承接 #2256。#2256 修好了 SwiftPM 解析的 artifact-cache 冲突后，iOS CI 又在
**Build for testing** 暴露出第二个 Blacksmith 迁移（#2227）遗留问题：

```
xcodebuild: error: Unable to find a device matching the provided destination specifier:
  { platform:iOS Simulator, OS:latest, name:iPhone 16 }
```

## 根因

`ios-quality` 的 `DESTINATION` 只 pin 了机型（`name=iPhone 16`），没 pin OS，
xcodebuild 取 `OS:latest`。Blacksmith 的 macOS 镜像除 iOS 18.x 外还预装了
**iOS 26.x** 运行时，而 `iPhone 16` 这个机型只在 **18.5 / 18.6** 下存在
（26.x 只有 iPhone 17 / Air / 16e）。于是 `OS:latest` = 26.2 → 找不到
iPhone 16 → build 挂。

旧的 GitHub macos-15 镜像 latest 还是 18.x，所以不写 OS 也能跑——迁到
Blacksmith 才暴露。

## 修复

```yaml
DESTINATION: 'platform=iOS Simulator,name=iPhone 16,OS=18.6'
```

Pin `OS=18.6`（镜像里稳定存在且带 iPhone 16）。这与 PR #2141 当初为了跑绿
用的 pin 一致，现在落到 main。

## 验证

通过 `workflow_dispatch` run 27126256275 实测：#2256 让 **Resolve SPM
packages 通过**，随后正是这个 destination 错误挂在 Build for testing。本 PR
合并后会再跑一次 dispatch 实测确认全绿。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 问题

承接 #2256。#2256 修好了 SwiftPM 解析的 artifact-cache 冲突后，iOS CI 又在
**Build for testing** 暴露出第二个 Blacksmith 迁移（#2227）遗留问题：

```
xcodebuild: error: Unable to find a device matching the provided destination specifier:
  { platform:iOS Simulator, OS:latest, name:iPhone 16 }
```

## 根因

`ios-quality` 的 `DESTINATION` 只 pin 了机型（`name=iPhone 16`），没 pin OS，
xcodebuild 取 `OS:latest`。Blacksmith 的 macOS 镜像除 iOS 18.x 外还预装了
**iOS 26.x** 运行时，而 `iPhone 16` 这个机型只在 **18.5 / 18.6** 下存在
（26.x 只有 iPhone 17 / Air / 16e）。于是 `OS:latest` = 26.2 → 找不到
iPhone 16 → build 挂。

旧的 GitHub macos-15 镜像 latest 还是 18.x，所以不写 OS 也能跑——迁到
Blacksmith 才暴露。

## 修复

```yaml
DESTINATION: 'platform=iOS Simulator,name=iPhone 16,OS=18.6'
```

Pin `OS=18.6`（镜像里稳定存在且带 iPhone 16）。这与 PR #2141 当初为了跑绿
用的 pin 一致，现在落到 main。

## 验证

通过 `workflow_dispatch` run 27126256275 实测：#2256 让 **Resolve SPM
packages 通过**，随后正是这个 destination 错误挂在 Build for testing。本 PR
合并后会再跑一次 dispatch 实测确认全绿。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [55b68e4] ci(ios): clear Blacksmith pre-seeded SwiftPM artifact cache (#2256)

- **SHA**: 55b68e48fa721cb2177ed6cd461250b369b0e82c
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T08:46:15Z
- **PR**: #2256
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/55b68e48fa721cb2177ed6cd461250b369b0e82c

### 完整 Commit Message

```
ci(ios): clear Blacksmith pre-seeded SwiftPM artifact cache (#2256)

## 问题

Blacksmith 迁移（#2227）把 iOS quality job 从 `macos-15` 切到
`blacksmith-6vcpu-macos-15` 之后，iOS CI 间歇性挂在 **Build for testing**，
报错：

```
xcodebuild: error: Could not resolve package dependencies:
  failed downloading '.../Sentry.xcframework.zip' which is required by binary
  target 'Sentry': /Users/runner/Library/Caches/org.swift.swiftpm/artifacts/
  https___..._Sentry_xcframework_zip already exists in file system
```

用户报告的失败例子：runs/27124241833（PR #2141）。

## 根因

1. Blacksmith 的 macOS 镜像出厂自带一份**预热**的全局 SwiftPM 缓存
   （`~/Library/Caches/org.swift.swiftpm`），其中 `artifacts/` 已解压好若干
   二进制 target 的 xcframework（Sentry / AppsFlyer / Firebase measurement /
   grpc / abseil）。当我们 pin 的版本与镜像里的对不上时，SwiftPM 在「下载」
   阶段发现目标目录已存在却又对不上账本，直接 `already exists in file system`。
2. **间歇性**：Blacksmith 从 VM 池分配机器，有的快照带这份冲突缓存、有的不带——
   同一份配置 `540d0f7e5`/`de3b849`/`11e5828` 过、`cec78be` 挂。
3. xcodebuild 内置的 SwiftPM 按**真实用户目录**（getpwuid → `/Users/runner`）
   算缓存路径，不读 `$HOME` env——所以 PR #2141 里靠覆盖 `HOME` 重定向缓存
   （+retry）治标不治本，仍有 ~25% 概率全 3 次 retry 一起挂。

## 修复

在解析 SwiftPM 包之前，直接清掉真实路径下的 `artifacts` 目录，让解析每次都从
干净状态开始：

```yaml
- name: Clear pre-seeded SwiftPM artifact cache (Blacksmith)
  run: rm -rf "$HOME/Library/Caches/org.swift.swiftpm/artifacts"
```

确定性消除冲突，无需 `HOME` 重定向 / retry hack。

## 取舍

每次清 `artifacts/` 会让二进制 xcframework 重新下载（约几十秒）。源码包
（git clone）仍由 DerivedData Actions 缓存 + `-clonedSourcePackagesDirPath`
命中，编译产物缓存不受影响。后续若想省掉这次下载，可以再用 `actions/cache`
按 `Package.resolved` hash 单独缓存这个目录——但那会重新引入冲突风险，本 PR
先求正确与稳定。

## 验证

iOS CI 只能在 Blacksmith macOS 上验证；合并后由 ios-quality job 跑实测。
本地已校验 workflow YAML 合法。

## 与 PR #2141 的关系

PR #2141（`fix/ios-1.7.2`）的 8 个 `ci(ios): ...` commit 是同一问题的另一套
（HOME 覆盖 + retry）尝试，方向不对。本 PR 落 main 后，建议 #2141 rebase 并
丢掉那 8 个 CI commit，只保留它的 style 改动。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 问题

Blacksmith 迁移（#2227）把 iOS quality job 从 `macos-15` 切到
`blacksmith-6vcpu-macos-15` 之后，iOS CI 间歇性挂在 **Build for testing**，
报错：

```
xcodebuild: error: Could not resolve package dependencies:
  failed downloading '.../Sentry.xcframework.zip' which is required by binary
  target 'Sentry': /Users/runner/Library/Caches/org.swift.swiftpm/artifacts/
  https___..._Sentry_xcframework_zip already exists in file system
```

用户报告的失败例子：runs/27124241833（PR #2141）。

## 根因

1. Blacksmith 的 macOS 镜像出厂自带一份**预热**的全局 SwiftPM 缓存
   （`~/Library/Caches/org.swift.swiftpm`），其中 `artifacts/` 已解压好若干
   二进制 target 的 xcframework（Sentry / AppsFlyer / Firebase measurement /
   grpc / abseil）。当我们 pin 的版本与镜像里的对不上时，SwiftPM 在「下载」
   阶段发现目标目录已存在却又对不上账本，直接 `already exists in file system`。
2. **间歇性**：Blacksmith 从 VM 池分配机器，有的快照带这份冲突缓存、有的不带——
   同一份配置 `540d0f7e5`/`de3b849`/`11e5828` 过、`cec78be` 挂。
3. xcodebuild 内置的 SwiftPM 按**真实用户目录**（getpwuid → `/Users/runner`）
   算缓存路径，不读 `$HOME` env——所以 PR #2141 里靠覆盖 `HOME` 重定向缓存
   （+retry）治标不治本，仍有 ~25% 概率全 3 次 retry 一起挂。

## 修复

在解析 SwiftPM 包之前，直接清掉真实路径下的 `artifacts` 目录，让解析每次都从
干净状态开始：

```yaml
- name: Clear pre-seeded SwiftPM artifact cache (Blacksmith)
  run: rm -rf "$HOME/Library/Caches/org.swift.swiftpm/artifacts"
```

确定性消除冲突，无需 `HOME` 重定向 / retry hack。

## 取舍

每次清 `artifacts/` 会让二进制 xcframework 重新下载（约几十秒）。源码包
（git clone）仍由 DerivedData Actions 缓存 + `-clonedSourcePackagesDirPath`
命中，编译产物缓存不受影响。后续若想省掉这次下载，可以再用 `actions/cache`
按 `Package.resolved` hash 单独缓存这个目录——但那会重新引入冲突风险，本 PR
先求正确与稳定。

## 验证

iOS CI 只能在 Blacksmith macOS 上验证；合并后由 ios-quality job 跑实测。
本地已校验 workflow YAML 合法。

## 与 PR #2141 的关系

PR #2141（`fix/ios-1.7.2`）的 8 个 `ci(ios): ...` commit 是同一问题的另一套
（HOME 覆盖 + retry）尝试，方向不对。本 PR 落 main 后，建议 #2141 rebase 并
丢掉那 8 个 CI commit，只保留它的 style 改动。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [ba88e3a] fix(ci): grant Bash to docs-maintenance workflow (#2254)

- **SHA**: ba88e3ade1cb127352a9ec65016121389eee6adb
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T08:38:31Z
- **PR**: #2254
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/ba88e3ade1cb127352a9ec65016121389eee6adb

### 完整 Commit Message

```
fix(ci): grant Bash to docs-maintenance workflow (#2254)

## What

Add `claude_args: --allowedTools "Bash,Edit,Write,Read,Glob,Grep"` to
the `docs-maintenance.yml` workflow's `claude-code-action` step.

## Why

The first dispatched run of the merged workflow ([run
27125097277](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/27125097277),
`dry_run=true`) reported `permission_denials_count: 4` and never
actually ran. Root cause: `claude-code-action` does **not** allow `Bash`
by default — only file operations and read-only git. The `sync-docs`
skill needs Bash for:
- `drift-probe.sh` (the Tier-1 deterministic probe),
- the `git log`/`git diff` history anchor (Step 2),
- on a real run: `git commit`/`git push` + `gh pr create` (Step 7).

So the dry-run "succeeded" but was a no-op — the probe and anchor were
blocked.

## Scope choice

`Bash` is allowed broadly rather than scoped (`Bash(git:*)` etc.)
because the skill's compound commands — pipes, `$(...)` substitutions,
`[ -z ... ]` guards — don't pattern-match narrow allowlist entries
reliably. Blast radius is contained: ephemeral runner, scoped GitHub App
token, and the resulting PR is human-reviewed and never auto-merged.
This is the same effective capability `claude-develop` runs with.

## Verification
- Workflow YAML parses.
- After merge: re-dispatch `dry_run=true` and confirm
`permission_denials_count: 0` and a real drift report in the step
summary, then a `dry_run=false` run end-to-end.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Add `claude_args: --allowedTools "Bash,Edit,Write,Read,Glob,Grep"` to the `docs-maintenance.yml` workflow's `claude-code-action` step.

## Why

The first dispatched run of the merged workflow ([run 27125097277](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/27125097277), `dry_run=true`) reported `permission_denials_count: 4` and never actually ran. Root cause: `claude-code-action` does **not** allow `Bash` by default — only file operations and read-only git. The `sync-docs` skill needs Bash for:
- `drift-probe.sh` (the Tier-1 deterministic probe),
- the `git log`/`git diff` history anchor (Step 2),
- on a real run: `git commit`/`git push` + `gh pr create` (Step 7).

So the dry-run "succeeded" but was a no-op — the probe and anchor were blocked.

## Scope choice

`Bash` is allowed broadly rather than scoped (`Bash(git:*)` etc.) because the skill's compound commands — pipes, `$(...)` substitutions, `[ -z ... ]` guards — don't pattern-match narrow allowlist entries reliably. Blast radius is contained: ephemeral runner, scoped GitHub App token, and the resulting PR is human-reviewed and never auto-merged. This is the same effective capability `claude-develop` runs with.

## Verification
- Workflow YAML parses.
- After merge: re-dispatch `dry_run=true` and confirm `permission_denials_count: 0` and a real drift report in the step summary, then a `dry_run=false` run end-to-end.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [0237ab6] feat(web): add session thread chat route (#2246)

- **SHA**: 0237ab67be9506f628323a4a80e3f918f168d258
- **作者**: bill-srp
- **日期**: 2026-06-08T08:23:08Z
- **PR**: #2246
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/0237ab67be9506f628323a4a80e3f918f168d258

### 完整 Commit Message

```
feat(web): add session thread chat route (#2246)

## Linear

https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Split 3 from #2216, stacked on #2245. Adds path-based session thread UI
and upgrades hidden /new-chat sends to create a conversation and
redirect into the thread route.

- Add /chat/{computerId}/{agentId}/{sessionId} route and thread client.
- Share chat rendering via OpenClawChatSurface and mmDisplayMessages.
- Add Mattermost get-thread/post fanout support for live thread updates.
- Update hidden /new-chat submit to create a conversation, post the
first message, then route to the session thread.
- Add focused unit coverage for thread route, live thread updates,
shared chat rendering, and new-chat submit behavior.

## Production exposure
This still does not add a sidebar entry, sidebar sessions, landing
redirect, or other visible activation path. /new-chat remains hidden
unless directly visited.

## Test plan
- pnpm --dir web/app exec vitest run
tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx
tests/unit/app/chat-thread/ThreadPostBubble.unit.spec.tsx
tests/unit/app/chat-thread/useConversationThread.unit.spec.tsx
tests/unit/app/chat-thread/useLiveThread.unit.spec.ts
tests/unit/app/chat/OpenClawChatSurface.unit.spec.tsx
tests/unit/app/chat/useChatMessaging.unit.spec.ts
tests/unit/app/chat/useChatPageDerivations.unit.spec.ts
tests/unit/app/chat/useMmChannelSync.unit.spec.ts
tests/unit/app/new-chat/NewChatClient.unit.spec.tsx
tests/unit/hooks/useMmChannelSync.unit.spec.ts
tests/unit/lib/api/openclaw-conversation-threads.unit.spec.ts
tests/unit/lib/api/openclaw-thread-reply.unit.spec.ts
tests/unit/lib/chat/agent-chat-href.unit.spec.ts
tests/unit/lib/mattermost/api-fetch-thread.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- #2244 hidden /new-chat launcher
- #2245 OpenClaw conversation API plumbing
- This PR: session-thread route and hidden send behavior
- Next: sidebar sessions
- Last: sidebar layout/nav activation
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Split 3 from #2216, stacked on #2245. Adds path-based session thread UI and upgrades hidden /new-chat sends to create a conversation and redirect into the thread route.

- Add /chat/{computerId}/{agentId}/{sessionId} route and thread client.
- Share chat rendering via OpenClawChatSurface and mmDisplayMessages.
- Add Mattermost get-thread/post fanout support for live thread updates.
- Update hidden /new-chat submit to create a conversation, post the first message, then route to the session thread.
- Add focused unit coverage for thread route, live thread updates, shared chat rendering, and new-chat submit behavior.

## Production exposure
This still does not add a sidebar entry, sidebar sessions, landing redirect, or other visible activation path. /new-chat remains hidden unless directly visited.

## Test plan
- pnpm --dir web/app exec vitest run tests/unit/app/chat-thread/SessionThreadClient.unit.spec.tsx tests/unit/app/chat-thread/ThreadPostBubble.unit.spec.tsx tests/unit/app/chat-thread/useConversationThread.unit.spec.tsx tests/unit/app/chat-thread/useLiveThread.unit.spec.ts tests/unit/app/chat/OpenClawChatSurface.unit.spec.tsx tests/unit/app/chat/useChatMessaging.unit.spec.ts tests/unit/app/chat/useChatPageDerivations.unit.spec.ts tests/unit/app/chat/useMmChannelSync.unit.spec.ts tests/unit/app/new-chat/NewChatClient.unit.spec.tsx tests/unit/hooks/useMmChannelSync.unit.spec.ts tests/unit/lib/api/openclaw-conversation-threads.unit.spec.ts tests/unit/lib/api/openclaw-thread-reply.unit.spec.ts tests/unit/lib/chat/agent-chat-href.unit.spec.ts tests/unit/lib/mattermost/api-fetch-thread.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- #2244 hidden /new-chat launcher
- #2245 OpenClaw conversation API plumbing
- This PR: session-thread route and hidden send behavior
- Next: sidebar sessions
- Last: sidebar layout/nav activation

---

## [e504922] refactor(claw-interface): stop account openclaw bot writes (#2242)

- **SHA**: e5049226f7f55eed06a17b706d371d9612e78500
- **作者**: bill-srp
- **日期**: 2026-06-08T08:18:48Z
- **PR**: #2242
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/e5049226f7f55eed06a17b706d371d9612e78500

### 完整 Commit Message

```
refactor(claw-interface): stop account openclaw bot writes (#2242)

## Summary
- move the backend implementation from #2229 into a backend-only PR
- stop persisting OpenClaw bot state to account openclaw_bots while
keeping V2 computer/workspace collections as the write target
- leave existing legacy account data untouched and ignore openclaw_bots
during warm-pool account materialization
- remove stale tests for deleted account-level OpenClaw bot write
helpers

## Test plan
- [x] carried forward from #2229: CI green on the same backend diff
before split
- [ ] new split PR CI pending
```

### PR Description

## Summary
- move the backend implementation from #2229 into a backend-only PR
- stop persisting OpenClaw bot state to account openclaw_bots while keeping V2 computer/workspace collections as the write target
- leave existing legacy account data untouched and ignore openclaw_bots during warm-pool account materialization
- remove stale tests for deleted account-level OpenClaw bot write helpers

## Test plan
- [x] carried forward from #2229: CI green on the same backend diff before split
- [ ] new split PR CI pending

---

## [852ae14] chore: add sync-docs skill + weekly docs-maintenance CI (#2253)

- **SHA**: 852ae147d97d6a86a5b0f18d9a751ad83a89613a
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T08:22:33Z
- **PR**: #2253
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/852ae147d97d6a86a5b0f18d9a751ad83a89613a

### 完整 Commit Message

```
chore: add sync-docs skill + weekly docs-maintenance CI (#2253)

## What

Turns the manual doc-drift fix we just did on `README.md` into a
reusable **`sync-docs` skill**, and wires a **weekly CI workflow** that
runs it and opens a documentation PR for human review. No auto-merge.

## Why

Doc-relevant infrastructure in this repo changes every ~2–4 weeks (dir
restructures, workflow renames, dependency bumps, new apps/services),
and `README` / `architecture` / `AGENTS.md` drift silently. The README
sync alone was 88/50 lines by hand.

## How it works — layered-hybrid autonomy

The skill isn't a dumb checklist; it explores to find what's stale, but
contains risk in three tiers:

- **Tier 1 — deterministic drift** (`drift-probe.sh`): `path / workflow
/ version / structure / env`. Auto-fixed. Precision-first: it asserts on
**README only** (root-relative, in-repo, tabular); the version check
runs across all docs. AGENTS/architecture use doc-relative paths, code
symbols, illustrative examples and cross-repo refs that a grep can't
disambiguate — deliberately left to Tier 2.
- **Tier 2 — evidence-grounded semantic drift**: stale prose, a new
app/service/convention/feature that an onboarding doc should mention.
Anchored on `git diff <last-sync>..HEAD` so it reviews real changes, not
the whole repo. **Every Tier-2 fix must cite a file / commit / symbol**
— no evidence → downgraded to Tier 3.
- **Tier 3 — suggestions**: listed in the PR body, never applied.

### Guardrails
- **Write scope = 7 target docs only** (README,
`architecture.md`/`.zh-CN.md`, 4 top-level `AGENTS.md`); explores
anywhere for evidence but edits nowhere else.
- Bilingual architecture edited as a pair; `docs:` PR title (passes
`pr-title-check`); **`--disable-auto`**; **silent when no drift**;
`dry_run` mode for dress-rehearsals.

## Reuses existing repo patterns
- Skill shape ← `bulk-archive-shipped-docs` (enumerate → fix →
branch/commit/PR, no-op silent, no auto-merge).
- Workflow ← `claude-arch-review.yaml` (weekly cron + dispatch, App
token, Bedrock, pinned `claude-code-action@v1.0.88`, `ANTHROPIC_MODEL:
us.anthropic.claude-sonnet-4-6`).
- Command ← `arch-review.md` positional-arg convention.

## Files
- `.claude/skills/sync-docs/{SKILL.md, references/drift-sources.md,
scripts/drift-probe.sh}`
- `.claude/commands/sync-docs.md`
- `.github/workflows/docs-maintenance.yml`

## Verification
- `drift-probe.sh` returns **clean / exit 0** on current main; injecting
each drift class (stale path, renamed workflow, wrong env var,
undocumented service, `Next.js 14`/`Python 3.11`) is caught and exits 1.
Version probe is multi-major aware (`have: 15 16`).
- `shellcheck -S warning` clean; workflow YAML parses.
- Security: the only user input (`language`) is a constrained `choice`
routed through `env:`; `dry_run` is a typed boolean; no free-form text
reaches a shell.

## Rollout (after merge)
1. `gh workflow run docs-maintenance.yml -f dry_run=true` to
dress-rehearse against live main.
2. Review the step-summary drift report, then let the Monday cron open
the first real PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Turns the manual doc-drift fix we just did on `README.md` into a reusable **`sync-docs` skill**, and wires a **weekly CI workflow** that runs it and opens a documentation PR for human review. No auto-merge.

## Why

Doc-relevant infrastructure in this repo changes every ~2–4 weeks (dir restructures, workflow renames, dependency bumps, new apps/services), and `README` / `architecture` / `AGENTS.md` drift silently. The README sync alone was 88/50 lines by hand.

## How it works — layered-hybrid autonomy

The skill isn't a dumb checklist; it explores to find what's stale, but contains risk in three tiers:

- **Tier 1 — deterministic drift** (`drift-probe.sh`): `path / workflow / version / structure / env`. Auto-fixed. Precision-first: it asserts on **README only** (root-relative, in-repo, tabular); the version check runs across all docs. AGENTS/architecture use doc-relative paths, code symbols, illustrative examples and cross-repo refs that a grep can't disambiguate — deliberately left to Tier 2.
- **Tier 2 — evidence-grounded semantic drift**: stale prose, a new app/service/convention/feature that an onboarding doc should mention. Anchored on `git diff <last-sync>..HEAD` so it reviews real changes, not the whole repo. **Every Tier-2 fix must cite a file / commit / symbol** — no evidence → downgraded to Tier 3.
- **Tier 3 — suggestions**: listed in the PR body, never applied.

### Guardrails
- **Write scope = 7 target docs only** (README, `architecture.md`/`.zh-CN.md`, 4 top-level `AGENTS.md`); explores anywhere for evidence but edits nowhere else.
- Bilingual architecture edited as a pair; `docs:` PR title (passes `pr-title-check`); **`--disable-auto`**; **silent when no drift**; `dry_run` mode for dress-rehearsals.

## Reuses existing repo patterns
- Skill shape ← `bulk-archive-shipped-docs` (enumerate → fix → branch/commit/PR, no-op silent, no auto-merge).
- Workflow ← `claude-arch-review.yaml` (weekly cron + dispatch, App token, Bedrock, pinned `claude-code-action@v1.0.88`, `ANTHROPIC_MODEL: us.anthropic.claude-sonnet-4-6`).
- Command ← `arch-review.md` positional-arg convention.

## Files
- `.claude/skills/sync-docs/{SKILL.md, references/drift-sources.md, scripts/drift-probe.sh}`
- `.claude/commands/sync-docs.md`
- `.github/workflows/docs-maintenance.yml`

## Verification
- `drift-probe.sh` returns **clean / exit 0** on current main; injecting each drift class (stale path, renamed workflow, wrong env var, undocumented service, `Next.js 14`/`Python 3.11`) is caught and exits 1. Version probe is multi-major aware (`have: 15 16`).
- `shellcheck -S warning` clean; workflow YAML parses.
- Security: the only user input (`language`) is a constrained `choice` routed through `env:`; `dry_run` is a typed boolean; no free-form text reaches a shell.

## Rollout (after merge)
1. `gh workflow run docs-maintenance.yml -f dry_run=true` to dress-rehearse against live main.
2. Review the step-summary drift report, then let the Monday cron open the first real PR.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [8404cd5] fix(sentry): downgrade browser-injected-script noise to warning (ECA-684) (#2250)

- **SHA**: 8404cd543b92436c35ce6a63f9ac46077c623d77
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T07:48:14Z
- **PR**: #2250
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/8404cd543b92436c35ce6a63f9ac46077c623d77

### 完整 Commit Message

```
fix(sentry): downgrade browser-injected-script noise to warning (ECA-684) (#2250)

## Summary

A React-probing browser extension injects a `/scripts/injectedScript.js`
into the page whose `findReactComponents()` dereferences a `null` DOM
node, throwing `TypeError: Cannot read properties of null (reading
'children')`. The file is **not** served by us (`GET
https://zooclaw.ai/scripts/injectedScript.js` → 404), but Sentry
rewrites its frames to `app:///scripts/injectedScript.js` and the global
`onerror` handler captures it as if it were our code. This surfaced as a
High-priority false-positive:
[ECA-684](https://linear.app/srpone/issue/ECA-684).

This adds a `beforeSend` rule that **downgrades** (rather than drops)
any event whose **throwing frame** originates from `injectedScript.js`
or a browser-extension URL:

- **`level = 'warning'`** — no longer pages as a High-severity error,
but stays visible. A foreign script failing *might* signal a
compatibility regression we caused (a markup/API change that breaks an
extension's assumptions), so we keep the signal instead of discarding
it.
- **`fingerprint = ['browser-injected-script']`** — collapses all of
them into a single issue, so a post-deploy spike is the signal. The
existing per-fingerprint rate limit caps volume.

### Throw-site-only matching (not "any frame")
Sentry orders `stacktrace.frames` oldest-call-first, so the **last**
frame is the throw site. We match only that frame. Browser extensions
monkeypatch DOM/browser APIs and leave their frames deeper in otherwise
app-originated stacks — matching *any* frame would mislabel **real bugs
from our own bundle** as injected-script noise. Matching only the throw
site keeps real app errors at `error` level.

The extension-URL match covers Chrome/Edge (`chrome-extension://`),
Firefox (`moz-extension://`) and Safari (`safari-web-extension://`).

## Test plan

- [x] Unit tests in
`web/app/tests/unit/config/sentry-client-config.unit.spec.ts`: throwing
frame from `injectedScript.js` / each extension scheme → downgraded to
`warning` + grouped fingerprint; throw site is foreign even with app
callers preceding it → downgraded; **real app bug whose throw site is
ours but with an extension frame deeper in the stack → stays at `error`
level**; unrelated filenames containing the token are untouched.
- [x] CI type-check / lint passes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## Summary

A React-probing browser extension injects a `/scripts/injectedScript.js` into the page whose `findReactComponents()` dereferences a `null` DOM node, throwing `TypeError: Cannot read properties of null (reading 'children')`. The file is **not** served by us (`GET https://zooclaw.ai/scripts/injectedScript.js` → 404), but Sentry rewrites its frames to `app:///scripts/injectedScript.js` and the global `onerror` handler captures it as if it were our code. This surfaced as a High-priority false-positive: [ECA-684](https://linear.app/srpone/issue/ECA-684).

This adds a `beforeSend` rule that **downgrades** (rather than drops) any event whose **throwing frame** originates from `injectedScript.js` or a browser-extension URL:

- **`level = 'warning'`** — no longer pages as a High-severity error, but stays visible. A foreign script failing *might* signal a compatibility regression we caused (a markup/API change that breaks an extension's assumptions), so we keep the signal instead of discarding it.
- **`fingerprint = ['browser-injected-script']`** — collapses all of them into a single issue, so a post-deploy spike is the signal. The existing per-fingerprint rate limit caps volume.

### Throw-site-only matching (not "any frame")
Sentry orders `stacktrace.frames` oldest-call-first, so the **last** frame is the throw site. We match only that frame. Browser extensions monkeypatch DOM/browser APIs and leave their frames deeper in otherwise app-originated stacks — matching *any* frame would mislabel **real bugs from our own bundle** as injected-script noise. Matching only the throw site keeps real app errors at `error` level.

The extension-URL match covers Chrome/Edge (`chrome-extension://`), Firefox (`moz-extension://`) and Safari (`safari-web-extension://`).

## Test plan

- [x] Unit tests in `web/app/tests/unit/config/sentry-client-config.unit.spec.ts`: throwing frame from `injectedScript.js` / each extension scheme → downgraded to `warning` + grouped fingerprint; throw site is foreign even with app callers preceding it → downgraded; **real app bug whose throw site is ours but with an extension frame deeper in the stack → stays at `error` level**; unrelated filenames containing the token are untouched.
- [x] CI type-check / lint passes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## [6f4360e] docs: refresh README for web sub-workspace and CI changes (#2252)

- **SHA**: 6f4360e8b3a97251fbc36b65c45d812c6448b640
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-08T07:44:22Z
- **PR**: #2252
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/6f4360e8b3a97251fbc36b65c45d812c6448b640

### 完整 Commit Message

```
docs: refresh README for web sub-workspace and CI changes (#2252)

## What

Refresh the root `README.md`, which still described the old two-package
(`web/` + `services/claw-interface/`) layout. Every claim below was
verified against the actual repo.

### Structural drift
- `web/` is now a pnpm **sub-workspace** hosting four apps: `web/app`
(`@zooclaw/web-app`, Next 15), `enterprise-admin` & `enterprise-app`
(Next 16), `dashboard-console` (React Router v7). `services/` gained
`oauth-worker` and `r2-access-worker`.
- Source moved `web/src/*` → `web/app/src/*` — fixed in the structure
tree, the `.env.local` symlink, and the dev/test commands.

### Broken commands fixed
- Frontend commands now run from `web/` (the repo root has no
`package.json`); dropped the bogus `pnpm --filter web dev`.
- `test:unit:watch` and all `test:e2e*` scripts live only in `web/app`,
so the Testing section now `cd web/app`.
- Symlink corrected: `web/.env.local → ../.env` → `web/app/.env.local →
../../.env`.

### CI/CD
- Removed `python-code-quality.yml` (folded into `code-quality.yml`),
renamed `claude-review.yaml` → `auto-review.yaml`.
- Added the missing user-facing workflows: `e2e`, `pr-title-check`,
`deploy-enterprise-admin`, `deploy-dashboard-console`, `ios-deploy`, the
auto-tag trio.
- Tag-conventions and deployment-targets tables now cover all five
surfaces.

### Facts
- Env var `NEXT_PUBLIC_GATEWAY_URL` → `CLAW_INTERFACE_URL`.
- Dropped stale private package `claude-code-ui` (only `favie-common`
remains).

## Verification
- Every referenced path and workflow file confirmed to exist.
- No stale tokens remain (`web/src/`, `NEXT_PUBLIC_GATEWAY_URL`,
`python-code-quality`, `claude-code-ui`, `claude-review.yaml`, `--filter
web dev`).
- All markdown tables have consistent column counts.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## What

Refresh the root `README.md`, which still described the old two-package (`web/` + `services/claw-interface/`) layout. Every claim below was verified against the actual repo.

### Structural drift
- `web/` is now a pnpm **sub-workspace** hosting four apps: `web/app` (`@zooclaw/web-app`, Next 15), `enterprise-admin` & `enterprise-app` (Next 16), `dashboard-console` (React Router v7). `services/` gained `oauth-worker` and `r2-access-worker`.
- Source moved `web/src/*` → `web/app/src/*` — fixed in the structure tree, the `.env.local` symlink, and the dev/test commands.

### Broken commands fixed
- Frontend commands now run from `web/` (the repo root has no `package.json`); dropped the bogus `pnpm --filter web dev`.
- `test:unit:watch` and all `test:e2e*` scripts live only in `web/app`, so the Testing section now `cd web/app`.
- Symlink corrected: `web/.env.local → ../.env` → `web/app/.env.local → ../../.env`.

### CI/CD
- Removed `python-code-quality.yml` (folded into `code-quality.yml`), renamed `claude-review.yaml` → `auto-review.yaml`.
- Added the missing user-facing workflows: `e2e`, `pr-title-check`, `deploy-enterprise-admin`, `deploy-dashboard-console`, `ios-deploy`, the auto-tag trio.
- Tag-conventions and deployment-targets tables now cover all five surfaces.

### Facts
- Env var `NEXT_PUBLIC_GATEWAY_URL` → `CLAW_INTERFACE_URL`.
- Dropped stale private package `claude-code-ui` (only `favie-common` remains).

## Verification
- Every referenced path and workflow file confirmed to exist.
- No stale tokens remain (`web/src/`, `NEXT_PUBLIC_GATEWAY_URL`, `python-code-quality`, `claude-code-ui`, `claude-review.yaml`, `--filter web dev`).
- All markdown tables have consistent column counts.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [50e2caa] feat(web): add OpenClaw conversation API plumbing (#2245)

- **SHA**: 50e2caa323bcc6043af389046b4232eb7f5d5ec8
- **作者**: bill-srp
- **日期**: 2026-06-08T07:27:15Z
- **PR**: #2245
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/50e2caa323bcc6043af389046b4232eb7f5d5ec8

### 完整 Commit Message

```
feat(web): add OpenClaw conversation API plumbing (#2245)

## Linear

https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Split 2 from #2216, stacked on #2244. Adds the additive web
BFF/client/query plumbing needed for OpenClaw computers and
conversations, without exposing new UI.

- Add /api/openclaw computer and conversation BFF routes.
- Add OpenClaw V2 computer-agent types and client functions.
- Add react-query keys/hooks for computers, conversations, and
conversation creation.
- Add focused unit coverage for route handlers, API clients, and query
keys/hooks.

## Production exposure
No sidebar, landing redirect, or visible route activation is added in
this PR.

## Test plan
- pnpm --dir web/app exec vitest run
tests/unit/app/api/openclaw/computer-agents.unit.spec.ts
tests/unit/app/api/openclaw/computers.unit.spec.ts
tests/unit/app/api/openclaw/conversations.unit.spec.ts
tests/unit/hooks/queries/openclaw-conversations.unit.spec.tsx
tests/unit/hooks/queries/openclaw-keys.unit.spec.ts
tests/unit/lib/api/openclaw-computer-agents.unit.spec.ts
tests/unit/lib/api/openclaw-conversations.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- Base: #2244 hidden /new-chat launcher
- Next: session-thread route and thread behavior
- Last: sidebar/nav activation
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-898/sidebar-restructure-three-zone-layout-new-chat-entry

## Summary
Split 2 from #2216, stacked on #2244. Adds the additive web BFF/client/query plumbing needed for OpenClaw computers and conversations, without exposing new UI.

- Add /api/openclaw computer and conversation BFF routes.
- Add OpenClaw V2 computer-agent types and client functions.
- Add react-query keys/hooks for computers, conversations, and conversation creation.
- Add focused unit coverage for route handlers, API clients, and query keys/hooks.

## Production exposure
No sidebar, landing redirect, or visible route activation is added in this PR.

## Test plan
- pnpm --dir web/app exec vitest run tests/unit/app/api/openclaw/computer-agents.unit.spec.ts tests/unit/app/api/openclaw/computers.unit.spec.ts tests/unit/app/api/openclaw/conversations.unit.spec.ts tests/unit/hooks/queries/openclaw-conversations.unit.spec.tsx tests/unit/hooks/queries/openclaw-keys.unit.spec.ts tests/unit/lib/api/openclaw-computer-agents.unit.spec.ts tests/unit/lib/api/openclaw-conversations.unit.spec.ts
- pnpm --dir web/app exec tsc --noEmit

## Stack
- Base: #2244 hidden /new-chat launcher
- Next: session-thread route and thread behavior
- Last: sidebar/nav activation

---

## [4aa3fe3] fix(billing): 用量明细按时间倒序展示（最近窗口在最前） (#2249)

- **SHA**: 4aa3fe380b7a6aee69ae1c3c61665d130a16c016
- **作者**: david-srp
- **日期**: 2026-06-08T07:08:40Z
- **PR**: #2249
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/4aa3fe380b7a6aee69ae1c3c61665d130a16c016

### 完整 Commit Message

```
fix(billing): 用量明细按时间倒序展示（最近窗口在最前） (#2249)

## 背景 / 问题

账户用量页（`/claw-settings?tab=account-usage`）底部「时间窗口明细」表格此前直接沿用后端返回的时间**升序**排列（最早的窗口在最前），用户需要滚动到列表底部才能看到最近的用量。

## 改动
在 `UsageRecord.tsx` 的 `nonZeroBuckets` 过滤后追加按 `start`
时间的**降序排序**，使最近的时间窗口排在最前面。

```tsx
const nonZeroBuckets = useMemo(
  () =>
    data?.buckets
      .filter((bucket) => bucket.requests > 0)
      .sort((a, b) => new Date(b.start).getTime() - new Date(a.start).getTime()) ?? [],
  [data],
)
```

## 实现要点
- `.filter()` 返回新数组，`.sort()` 不会原地修改 React Query 缓存中的 `data.buckets`。
- `maxCredits` / `peakBucket` 等统计仍读取原始 `data.buckets`，与展示顺序解耦，不受影响。
- 用 `new Date(start).getTime()` 解析，与 `formatWindow` 中既有的时间解析方式一致。

## 影响范围
仅前端展示顺序，无 API / 数据结构变更。现有单测（`UsageRecord.unit.spec.tsx`）mock 中仅含一个非零
bucket，不依赖行顺序，不受影响。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: David Lu <davidlu@Daviddebijibendiannao.local>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR Description

## 背景 / 问题
账户用量页（`/claw-settings?tab=account-usage`）底部「时间窗口明细」表格此前直接沿用后端返回的时间**升序**排列（最早的窗口在最前），用户需要滚动到列表底部才能看到最近的用量。

## 改动
在 `UsageRecord.tsx` 的 `nonZeroBuckets` 过滤后追加按 `start` 时间的**降序排序**，使最近的时间窗口排在最前面。

```tsx
const nonZeroBuckets = useMemo(
  () =>
    data?.buckets
      .filter((bucket) => bucket.requests > 0)
      .sort((a, b) => new Date(b.start).getTime() - new Date(a.start).getTime()) ?? [],
  [data],
)
```

## 实现要点
- `.filter()` 返回新数组，`.sort()` 不会原地修改 React Query 缓存中的 `data.buckets`。
- `maxCredits` / `peakBucket` 等统计仍读取原始 `data.buckets`，与展示顺序解耦，不受影响。
- 用 `new Date(start).getTime()` 解析，与 `formatWindow` 中既有的时间解析方式一致。

## 影响范围
仅前端展示顺序，无 API / 数据结构变更。现有单测（`UsageRecord.unit.spec.tsx`）mock 中仅含一个非零 bucket，不依赖行顺序，不受影响。

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## [3aacb85] feat(claw-interface): split session thread backend follow-up (#2243)

- **SHA**: 3aacb85968b5b7918dfb32089e932243491f30b8
- **作者**: bill-srp
- **日期**: 2026-06-08T07:04:09Z
- **PR**: #2243
- **URL**: https://github.com/SerendipityOneInc/ecap-workspace/commit/3aacb85968b5b7918dfb32089e932243491f30b8

### 完整 Commit Message

```
feat(claw-interface): split session thread backend follow-up (#2243)

## Linear

https://linear.app/srpone/issue/ECA-896/openclaw-session-threads-per-agent-channel-root-post-id

## Summary
Backend-first split from feat/openclaw-session-threads. This PR carries
the session-thread backend route/provisioning work plus the minimal web
BFF compatibility update needed to keep existing browser-facing
conversation asset/workspace endpoints working after the backend route
move.

- Move OpenClaw conversation asset/workspace backend routes under
`/openclaw/conversation/*` and add the
`/conversations/{computer_id}/{agent_id}` route surface.
- Preserve session-thread behavior, including `root_post_id` and
per-agent `session_channel_id` handling.
- Add deterministic `zoo-session-` Mattermost channel names for
per-agent session channels.
- Add Mattermost org team provisioning/backfill support for session
channel creation.
- Update the existing web BFF `/api/conversation/*` routes to proxy to
`/openclaw/conversation/*` so current frontend callers do not depend on
removed backend `/conversation/*` mounts.

## Rollout / Compatibility
This PR is part of a coordinated stacked rollout, not a user-visible
launch by itself.

Deployment/order contract:
1. Merge/deploy this backend and BFF compatibility PR first.
2. Merge/deploy the web API plumbing PR (#2245) after this backend
surface exists.
3. Merge/deploy the session-thread chat route and sidebar activation PRs
only after the route plumbing is deployed.

Compatibility notes:
- `/openclaw/conversation/sessions` intentionally has no compatibility
shim because it was not used by prior clients before session-channel
conversations moved to `/conversations/{computer_id}/{agent_id}`.
- Existing browser-facing asset/workspace APIs remain stable at
`/api/conversation/assets` and `/api/conversation/workspace/files`;
their BFF proxy target changes to `/openclaw/conversation/*` in this PR.
- The new session UI remains hidden until the later activation PR, so
this change can land before navigation/sidebar exposure.

## Stacked PRs
- #2244 hidden `/new-chat` launcher/route infrastructure.
- #2245 OpenClaw conversation web API plumbing.
- #2246 session-thread chat route.
- #2247 sidebar activation; should be the last user-visible rollout PR.

## Test plan
- [x] .venv/bin/python -m pytest -q
tests/unit/test_agent_workspace_schema.py
tests/unit/test_backfill_mattermost_org_teams.py
tests/unit/test_conversation_routes.py tests/unit/test_conversations.py
tests/unit/test_mattermost_client.py
tests/unit/test_openclaw_conversation.py
tests/unit/test_openclaw_session_channel_repo.py
tests/unit/test_openclaw_session_channel_schema.py
tests/unit/test_openclaw_session_channel_service.py
tests/unit/test_schema_org.py (140 passed)
- [x] .venv/bin/ruff check .
- [x] services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_openclaw_session_channel_service.py
(29 passed)
- [x] services/claw-interface/.venv/bin/python -m pytest
services/claw-interface/tests/unit/test_conversations.py (5 passed)
- [x] pnpm --dir web/app exec eslint
src/app/api/conversation/assets/route.ts
src/app/api/conversation/workspace/files/route.ts
src/lib/api/conversation-assets.ts
tests/unit/app/api/conversation-assets.unit.spec.ts
tests/unit/app/api/conversation-workspace-files.unit.spec.ts --quiet
--cache --cache-location .eslintcache --cache-strategy content
- [x] pnpm --dir web/app run test:unit --
tests/unit/app/api/conversation-assets.unit.spec.ts
tests/unit/app/api/conversation-workspace-files.unit.spec.ts (broad
Vitest config: 462 passed)
- [ ] pyright app tests (not available locally in this shell; expected
in CI)
```

### PR Description

## Linear
https://linear.app/srpone/issue/ECA-896/openclaw-session-threads-per-agent-channel-root-post-id

## Summary
Backend-first split from feat/openclaw-session-threads. This PR carries the session-thread backend route/provisioning work plus the minimal web BFF compatibility update needed to keep existing browser-facing conversation asset/workspace endpoints working after the backend route move.

- Move OpenClaw conversation asset/workspace backend routes under `/openclaw/conversation/*` and add the `/conversations/{computer_id}/{agent_id}` route surface.
- Preserve session-thread behavior, including `root_post_id` and per-agent `session_channel_id` handling.
- Add deterministic `zoo-session-` Mattermost channel names for per-agent session channels.
- Add Mattermost org team provisioning/backfill support for session channel creation.
- Update the existing web BFF `/api/conversation/*` routes to proxy to `/openclaw/conversation/*` so current frontend callers do not depend on removed backend `/conversation/*` mounts.

## Rollout / Compatibility
This PR is part of a coordinated stacked rollout, not a user-visible launch by itself.

Deployment/order contract:
1. Merge/deploy this backend and BFF compatibility PR first.
2. Merge/deploy the web API plumbing PR (#2245) after this backend surface exists.
3. Merge/deploy the session-thread chat route and sidebar activation PRs only after the route plumbing is deployed.

Compatibility notes:
- `/openclaw/conversation/sessions` intentionally has no compatibility shim because it was not used by prior clients before session-channel conversations moved to `/conversations/{computer_id}/{agent_id}`.
- Existing browser-facing asset/workspace APIs remain stable at `/api/conversation/assets` and `/api/conversation/workspace/files`; their BFF proxy target changes to `/openclaw/conversation/*` in this PR.
- The new session UI remains hidden until the later activation PR, so this change can land before navigation/sidebar exposure.

## Stacked PRs
- #2244 hidden `/new-chat` launcher/route infrastructure.
- #2245 OpenClaw conversation web API plumbing.
- #2246 session-thread chat route.
- #2247 sidebar activation; should be the last user-visible rollout PR.

## Test plan
- [x] .venv/bin/python -m pytest -q tests/unit/test_agent_workspace_schema.py tests/unit/test_backfill_mattermost_org_teams.py tests/unit/test_conversation_routes.py tests/unit/test_conversations.py tests/unit/test_mattermost_client.py tests/unit/test_openclaw_conversation.py tests/unit/test_openclaw_session_channel_repo.py tests/unit/test_openclaw_session_channel_schema.py tests/unit/test_openclaw_session_channel_service.py tests/unit/test_schema_org.py (140 passed)
- [x] .venv/bin/ruff check .
- [x] services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_openclaw_session_channel_service.py (29 passed)
- [x] services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_conversations.py (5 passed)
- [x] pnpm --dir web/app exec eslint src/app/api/conversation/assets/route.ts src/app/api/conversation/workspace/files/route.ts src/lib/api/conversation-assets.ts tests/unit/app/api/conversation-assets.unit.spec.ts tests/unit/app/api/conversation-workspace-files.unit.spec.ts --quiet --cache --cache-location .eslintcache --cache-strategy content
- [x] pnpm --dir web/app run test:unit -- tests/unit/app/api/conversation-assets.unit.spec.ts tests/unit/app/api/conversation-workspace-files.unit.spec.ts (broad Vitest config: 462 passed)
- [ ] pyright app tests (not available locally in this shell; expected in CI)

---

