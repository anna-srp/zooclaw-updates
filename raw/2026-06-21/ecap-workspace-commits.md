# ecap-workspace commits — 2026-06-21

共 2 个 commit

---

## `c76fd5ae6f`

- **作者**: Chris@ZooClaw
- **日期**: 2026-06-22T00:07:00Z
- **PR**: #2543
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/c76fd5ae6f5c287430ede40c65495becea9c981f

### 完整 commit message

```
test(openclaw): cover untested rate-limit branches (#2543)

## What

Adds 4 branch-coverage tests to `test_rate_limit.py` for
`check_rate_limit`, closing gaps where existing tests only exercised one
side of a conditional:

| Test | Guards |
|------|--------|
| `test_rejected_call_does_not_consume_budget` | A 429'd request must
not append to the window (raise precedes `window.append`); consecutive
rejections keep the window at the cap, not 31/32/33 |
| `test_cleanup_skipped_within_interval` | The periodic-cleanup guard's
**False** branch — when the cleanup interval has not elapsed, stale
users are left in place (GC is best-effort) |
| `test_cleanup_purges_empty_window_users` | The `not v` half of the
cleanup predicate — a UID left with an empty window is treated as stale
and removed |
| `test_partial_window_expiry_keeps_recent` | Mixed timestamps: only
entries older than the window are pruned; recent ones survive and still
count toward the limit (prior tests only covered full expiry) |

## Why

Line coverage on this module read high, but several **branches** were
untested — notably the False side of the cleanup-interval guard and the
`not v` half of the cleanup predicate. Each new assertion is falsifiable
(mutating the corresponding source line turns it red).

## Testing

- `pytest tests/unit/test_rate_limit.py` — 11 passed
- `ruff check` + `ruff format --check` clean

---------

Co-authored-by: chris-srp <xuwenhao@msn.com>
Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

```
## What

Adds 4 branch-coverage tests to `test_rate_limit.py` for `check_rate_limit`, closing gaps where existing tests only exercised one side of a conditional:

| Test | Guards |
|------|--------|
| `test_rejected_call_does_not_consume_budget` | A 429'd request must not append to the window (raise precedes `window.append`); consecutive rejections keep the window at the cap, not 31/32/33 |
| `test_cleanup_skipped_within_interval` | The periodic-cleanup guard's **False** branch — when the cleanup interval has not elapsed, stale users are left in place (GC is best-effort) |
| `test_cleanup_purges_empty_window_users` | The `not v` half of the cleanup predicate — a UID left with an empty window is treated as stale and removed |
| `test_partial_window_expiry_keeps_recent` | Mixed timestamps: only entries older than the window are pruned; recent ones survive and still count toward the limit (prior tests only covered full expiry) |

## Why

Line coverage on this module read high, but several **branches** were untested — notably the False side of the cleanup-interval guard and the `not v` half of the cleanup predicate. Each new assertion is falsifiable (mutating the corresponding source line turns it red).

## Testing

- `pytest tests/unit/test_rate_limit.py` — 11 passed
- `ruff check` + `ruff format --check` clean

```

---

## `f27d797747`

- **作者**: Chris@ZooClaw
- **日期**: 2026-06-22T00:03:22Z
- **PR**: #2512
- **链接**: https://github.com/SerendipityOneInc/ecap-workspace/commit/f27d79774792774a2ea6a0a252f8df785401414b

### 完整 commit message

```
fix(sentry): cut ecap-website 4xx/RQ noise at the source (ECA-1025) (#2512)

## What & why

ECA-1025 aimed to cut ecap-website Sentry noise. Triage of **live Sentry
data** (org `serendipity-one-inc`) showed two of the issue's premises
were stale and one proposal was unsafe:

- `httpClientIntegration` is **already** customized
(`failedRequestStatusCodes: [400, [402,408], [410,599]]`) with a
per-endpoint `EXPECTED_HTTP_ERRORS` allowlist + infra-5xx drop — not the
default.
- The 4xx are **not** generic client noise: they're concentrated on app
code paths with high user counts (e.g. a 400 on `getAgentSettingsBatch`
hit 480 prod users). Blanket-dropping all 4xx (the original #1) would
hide real defects, so we **fix the source and filter only
confirmed-expected endpoints**, keeping unexpected 4xx visible.
- The `React Query query failed: .../<id>` grouping explosion is caused
by un-collapsed entity IDs in the key, not "all 4xx".
- Inbound Filters (#4) were already fully enabled and are orthogonal to
this noise — no-op.

## Changes

**Grouping / SDK config**
- `react-query-monitor.ts`: collapse snowflake/UUID/ObjectId key
segments to `:id` for the message, fingerprint, and `rq.key` tag, so
per-entity failures roll into one issue. Raw key kept in the event
context for debugging.
- `sentry.client.config.ts`: surgical `EXPECTED_HTTP_ERRORS` additions —
the `@srp.one`-gated image-version 403 (always expected for non-internal
users) and the `computers/{id}/status` poll-after-gone 404. Narrow
`ignoreErrors` (AbortError family / ResizeObserver loop) + `denyUrls`
(third-party analytics only). Deliberately **not** blanket-dropping 4xx,
**not** denying extension schemes (keeps the ECA-684 downgrade visible),
**not** ignoring bare `Failed to fetch`.

**Source-defect fixes (remove noise at origin)**
- `getAgentSettingsBatch` 400 (prod, 480 users): the batch endpoint is a
cosmetic sidebar identity prefetch — when the bot isn't initialized yet
it now returns an empty list (200) instead of 400. The single-agent GET
keeps its 400.
- `getOpenClawStatus` 400 (`/subscription/success`, `/user/verify`):
fail fast without the doomed request when `uid` is unresolved during the
post-payment auth transition.

## Tests
- web: 662 unit tests pass (new coverage for ID-collapse grouping, the
new beforeSend filters, and the uid fail-fast guard — incl. assertions
that unexpected 4xx and own-domain 400s stay visible).
- backend: 239 unit tests pass (batch endpoint returns empty on
`bot_not_initialized`, re-raises other 400s, keeps the success path).

## Deliberately NOT in this PR
- `agents-manager` publish `/api/claw/*` 404: verified to be an
**orphaned/desynced org** (one org 404s across all its endpoints), not a
route bug. Kept visible (it's a real access signal); needs a separate
cross-service follow-up.
- `checkVersion` 404: held for discussion (is account-not-found benign
or a real desync?). Not filtered, not changed.

Linear: https://linear.app/srpone/issue/ECA-1025

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### 完整 PR body

```
## What & why

ECA-1025 aimed to cut ecap-website Sentry noise. Triage of **live Sentry data** (org `serendipity-one-inc`) showed two of the issue's premises were stale and one proposal was unsafe:

- `httpClientIntegration` is **already** customized (`failedRequestStatusCodes: [400, [402,408], [410,599]]`) with a per-endpoint `EXPECTED_HTTP_ERRORS` allowlist + infra-5xx drop — not the default.
- The 4xx are **not** generic client noise: they're concentrated on app code paths with high user counts (e.g. a 400 on `getAgentSettingsBatch` hit 480 prod users). Blanket-dropping all 4xx (the original #1) would hide real defects, so we **fix the source and filter only confirmed-expected endpoints**, keeping unexpected 4xx visible.
- The `React Query query failed: .../<id>` grouping explosion is caused by un-collapsed entity IDs in the key, not "all 4xx".
- Inbound Filters (#4) were already fully enabled and are orthogonal to this noise — no-op.

## Changes

**Grouping / SDK config**
- `react-query-monitor.ts`: collapse snowflake/UUID/ObjectId key segments to `:id` for the message, fingerprint, and `rq.key` tag, so per-entity failures roll into one issue. Raw key kept in the event context for debugging.
- `sentry.client.config.ts`: surgical `EXPECTED_HTTP_ERRORS` additions — the `@srp.one`-gated image-version 403 (always expected for non-internal users) and the `computers/{id}/status` poll-after-gone 404. Narrow `ignoreErrors` (AbortError family / ResizeObserver loop) + `denyUrls` (third-party analytics only). Deliberately **not** blanket-dropping 4xx, **not** denying extension schemes (keeps the ECA-684 downgrade visible), **not** ignoring bare `Failed to fetch`.

**Source-defect fixes (remove noise at origin)**
- `getAgentSettingsBatch` 400 (prod, 480 users): the batch endpoint is a cosmetic sidebar identity prefetch — when the bot isn't initialized yet it now returns an empty list (200) instead of 400. The single-agent GET keeps its 400.
- `getOpenClawStatus` 400 (`/subscription/success`, `/user/verify`): fail fast without the doomed request when `uid` is unresolved during the post-payment auth transition.

## Tests
- web: 662 unit tests pass (new coverage for ID-collapse grouping, the new beforeSend filters, and the uid fail-fast guard — incl. assertions that unexpected 4xx and own-domain 400s stay visible).
- backend: 239 unit tests pass (batch endpoint returns empty on `bot_not_initialized`, re-raises other 400s, keeps the success path).

## Deliberately NOT in this PR
- `agents-manager` publish `/api/claw/*` 404: verified to be an **orphaned/desynced org** (one org 404s across all its endpoints), not a route bug. Kept visible (it's a real access signal); needs a separate cross-service follow-up.
- `checkVersion` 404: held for discussion (is account-not-found benign or a real desync?). Not filtered, not changed.

Linear: https://linear.app/srpone/issue/ECA-1025

🤖 Generated with [Claude Code](https://claude.com/claude-code)

```
