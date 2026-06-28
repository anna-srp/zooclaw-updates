# SerendipityOneInc/ecap-workspace — 2026-06-27 commits

共 7 个 commit

---

## ci(e2e): expand daily production coverage (#2532)
- **SHA**: `198e8ff2371e234008538543bd3a9dc0b2e8577d`
- **作者**: rayhuang198212 <ray.huang@mktech.tech>
- **日期**: 2026-06-27T13:23:02Z
- **PR**: #2532

### 完整 Commit Message

```
ci(e2e): expand daily production coverage (#2532)

## Summary

- Expand the daily production E2E workflow from the original
smoke/scenario subset to the broader Playwright project set.
- Increase the E2E job timeout from 120 to 360 minutes to account for
the larger serial test suite.
- Remove stale Playwright projects for specs that no longer exist
(`home`, `assets-gallery`).
```

### PR 描述

## Summary

- Expand the daily production E2E workflow from the original smoke/scenario subset to the broader Playwright project set.
- Increase the E2E job timeout from 120 to 360 minutes to account for the larger serial test suite.
- Remove stale Playwright projects for specs that no longer exist (`home`, `assets-gallery`).

---

## chore(deps): consolidate open dependabot dependency updates (#2631)
- **SHA**: `f66c847b1e439edb7bb114ba6918765616a649b4`
- **作者**: Chris@ZooClaw <chris@srp.one>
- **日期**: 2026-06-27T13:22:21Z
- **PR**: #2631

### 完整 Commit Message

```
chore(deps): consolidate open dependabot dependency updates (#2631)

## What

Consolidates the **Python-side Dependabot updates** into one PR. The
web-side updates are no longer here — `main` #2608 ("refresh web minor
dependencies") already landed that consolidation, so this PR was
rebased/merged onto it and the now-redundant web changes were dropped.

Final diff is **2 files** (`requirements.txt`, `requirements-dev.txt`) —
no production or test code, no lockfile.

| Dependabot PR | Update | Handling |
|----|--------|----------|
| #2622 | cryptography `>=49.0.0` | ✅ bumped |
| #2626 | openai `>=2.43.0,<2.44.0` | ✅ bumped |
| #2624 | ruff `>=0.15.18` | ✅ bumped |
| #2625 | fastapi `<0.138` | 🔒 **locked at `<0.137`** |
| #2623 | pytest `<9.2` | 🔒 **locked at `<9.1`** |
| #2536 / #2538 | web group / vite | ➡️ handled on main by #2608 |

## Locked instead of bumped (no code changes)

Per review, when a bump only passes CI if we change our own code, we
lock the version instead:

- **fastapi** — 0.137 turns `APIRoute.methods` into `set[str] | None`,
which would force `Optional` guards in the route tests. Held at
`<0.137`; `requirements.txt` comment records why.
- **pytest** — 9.1 makes pytest-bdd 8.1.0's `_register_fixture(nodeid)`
raise `PytestRemovedIn10Warning` under `filterwarnings=error`; 8.1.0 is
the latest pytest-bdd. Held at `<9.1`; `requirements-dev.txt` comment
records why. Revisit once pytest-bdd ships a fix.

## Web side

Already shipped on `main` via #2608, which refreshed the safe web deps,
held `@assistant-ui/react` back (dodging the `@assistant-ui/tap` /
`useEffectEvent` build break), and intentionally left the Vitest ranges
unchanged to avoid pnpm importer/override drift. Nothing left to do here
— this PR merged that in and dropped its own (redundant) web bumps.

Supersedes the Python Dependabot PRs #2622, #2623, #2624, #2625, #2626.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR 描述

## What

Consolidates the **Python-side Dependabot updates** into one PR. The web-side updates are no longer here — `main` #2608 ("refresh web minor dependencies") already landed that consolidation, so this PR was rebased/merged onto it and the now-redundant web changes were dropped.

Final diff is **2 files** (`requirements.txt`, `requirements-dev.txt`) — no production or test code, no lockfile.

| Dependabot PR | Update | Handling |
|----|--------|----------|
| #2622 | cryptography `>=49.0.0` | ✅ bumped |
| #2626 | openai `>=2.43.0,<2.44.0` | ✅ bumped |
| #2624 | ruff `>=0.15.18` | ✅ bumped |
| #2625 | fastapi `<0.138` | 🔒 **locked at `<0.137`** |
| #2623 | pytest `<9.2` | 🔒 **locked at `<9.1`** |
| #2536 / #2538 | web group / vite | ➡️ handled on main by #2608 |

## Locked instead of bumped (no code changes)

Per review, when a bump only passes CI if we change our own code, we lock the version instead:

- **fastapi** — 0.137 turns `APIRoute.methods` into `set[str] | None`, which would force `Optional` guards in the route tests. Held at `<0.137`; `requirements.txt` comment records why.
- **pytest** — 9.1 makes pytest-bdd 8.1.0's `_register_fixture(nodeid)` raise `PytestRemovedIn10Warning` under `filterwarnings=error`; 8.1.0 is the latest pytest-bdd. Held at `<9.1`; `requirements-dev.txt` comment records why. Revisit once pytest-bdd ships a fix.

## Web side

Already shipped on `main` via #2608, which refreshed the safe web deps, held `@assistant-ui/react` back (dodging the `@assistant-ui/tap` / `useEffectEvent` build break), and intentionally left the Vitest ranges unchanged to avoid pnpm importer/override drift. Nothing left to do here — this PR merged that in and dropped its own (redundant) web bumps.

Supersedes the Python Dependabot PRs #2622, #2623, #2624, #2625, #2626.

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## chore(deps): refresh web minor dependencies (#2608)
- **SHA**: `2429f0f75192e4c195c84b5136e54d3c9d2b0838`
- **作者**: Chris@ZooClaw <chris@srp.one>
- **日期**: 2026-06-27T12:09:46Z
- **PR**: #2608

### 完整 Commit Message

```
chore(deps): refresh web minor dependencies (#2608)

## Summary
- Refresh safe web minor/patch dependencies from the Dependabot batch
while leaving `@assistant-ui/react` on the current compatible range.
- Also leave Vitest-related manifest ranges unchanged to avoid pnpm
importer/override drift called out by automated review.
- Avoid the `@assistant-ui/tap` / React `useEffectEvent` build
regression seen in Dependabot PR #2536.
- Regenerate `web/pnpm-lock.yaml` from current `main`.

## Verification
- `cd web && pnpm install --frozen-lockfile`
- `cd web/app && APP_ENV=staging NODE_ENV=production
NODE_OPTIONS=--max-old-space-size=8192 pnpm exec next build
--experimental-build-mode=compile`
- `cd web && pnpm --filter @zooclaw/web-app run lint:ci && pnpm --filter
@zooclaw/web-app run test:unit`

Supersedes the failing Dependabot batch PR #2536.
```

### PR 描述

## Summary
- Refresh safe web minor/patch dependencies from the Dependabot batch while leaving `@assistant-ui/react` on the current compatible range.
- Also leave Vitest-related manifest ranges unchanged to avoid pnpm importer/override drift called out by automated review.
- Avoid the `@assistant-ui/tap` / React `useEffectEvent` build regression seen in Dependabot PR #2536.
- Regenerate `web/pnpm-lock.yaml` from current `main`.

## Verification
- `cd web && pnpm install --frozen-lockfile`
- `cd web/app && APP_ENV=staging NODE_ENV=production NODE_OPTIONS=--max-old-space-size=8192 pnpm exec next build --experimental-build-mode=compile`
- `cd web && pnpm --filter @zooclaw/web-app run lint:ci && pnpm --filter @zooclaw/web-app run test:unit`

Supersedes the failing Dependabot batch PR #2536.

---

## ci: raise PR size limit to 3000 lines (#2630)
- **SHA**: `1b155a77d7864612cf5111d0132bbbe531928f5f`
- **作者**: Chris@ZooClaw <chris@srp.one>
- **日期**: 2026-06-27T11:03:54Z
- **PR**: #2630

### 完整 Commit Message

```
ci: raise PR size limit to 3000 lines (#2630)

## Summary
- raise the reusable PR size gate limit from 2000 to 3000 lines
- keep code-quality, required PR size check, and label-refresh paths
aligned

## Validation
- parsed changed workflow YAML with Psych
- ran git diff --check
- scanned workflow max_lines/default values for remaining 2000 entries
```

### PR 描述

## Summary
- raise the reusable PR size gate limit from 2000 to 3000 lines
- keep code-quality, required PR size check, and label-refresh paths aligned

## Validation
- parsed changed workflow YAML with Psych
- ran git diff --check
- scanned workflow max_lines/default values for remaining 2000 entries

---

## fix(knowledge-base): proxy /knowledge-base/* through claw-interface to ecap-proxy-service (#2629)
- **SHA**: `cbeb0e04e9c23a120aed66bc0429a72109cfa785`
- **作者**: kevin <kevin@srp.one>
- **日期**: 2026-06-27T04:06:37Z
- **PR**: #2629

### 完整 Commit Message

```
fix(knowledge-base): proxy /knowledge-base/* through claw-interface to ecap-proxy-service (#2629)

## What & why

The knowledge-base upload page (shipped in #2617) loads in deployed
**staging** but the document list fails with **"Could not load
documents"** (and upload would fail too).

**Root cause:** the page's data layer calls
`callClawInterfaceAPI('/knowledge-base/*')` → web BFF `/api/claw/*` →
`CLAW_INTERFACE_URL` (**claw-interface**). But the `/knowledge-base/*`
endpoints live only in **`ecap-proxy-service`** (separate repo +
separate ingress). `services/claw-interface` had no kb route and no
forwarding, so it 404'd. The frontend is correct — the established
pattern for reaching ecap-proxy-service from the web app is *through*
claw-interface (exactly what `composio_connectors` does); this feature's
backend half was simply missing.

## Change (backend-only, frontend unchanged)

Add `app/routes/knowledge_base.py`, mirroring
`composio_connectors._proxy_request`:

- `GET /knowledge-base/documents` → forward to
`SETTINGS.ECAP_PROXY_SERVICE_URL` with the caller's `Authorization:
Bearer <token>`.
- `POST /knowledge-base/upload` → forward the multipart body
**verbatim** (original `Content-Type`/boundary preserved — transparent
passthrough, no re-encoding); reject `>50MB` early with `413` (mirrors
the web soft-check and `VERTEX_SEARCH_MAX_UPLOAD_BYTES`).
- Reuse composio's error handling: `401` (missing token), `502`
(upstream `RequestError`), upstream status/detail propagation,
`retries=1` connect-retry transport.

`CLAW_INTERFACE_URL` stays pointed at claw-interface; no web change.

## Testing

### Static + unit
- `bash scripts/verify-py.sh` — ruff + ruff-format + pyright +
import-linter all pass.
- `pytest tests/unit/test_knowledge_base.py` — 8 passed (forwarding +
headers, multipart passthrough, 413 via content-length and via body
length, retries=1 transport, 502 on RequestError, upstream status/detail
propagation, 401 on missing token).

### Local integration vs the REAL ecap-proxy-service
Exercised the route handlers directly against the real staging
`ecap-proxy-service` over a Telepresence connection (no deploy, no mongo
needed), with a real staging user bearer token:

- `GET /knowledge-base/documents` → **200**, returned the user's real
org documents (2 `indexed`).
- `POST /knowledge-base/upload` (small `text/plain` multipart) →
**200**, `success: true`, `status: pending` (file really written to the
org's knowledge base + indexing queued).
- Re-`GET` → the uploaded file appears as `pending` (the same end-to-end
propagation the page's React Query invalidate-on-success surfaces).
- Invalid/dummy token → **401** with the upstream detail propagated.

This confirms the forward path, URL construction, bearer forwarding,
multipart passthrough, and upstream error/status propagation against the
real backend — i.e. the exact path that previously 404'd now works.

## Deployment

Requires deploying **claw-interface** to staging for the fix to take
effect in the deployed site. No frontend deploy needed.

Closes #2627

Co-authored-by: Developer <dev@srp.one>
```

### PR 描述

## What & why

The knowledge-base upload page (shipped in #2617) loads in deployed **staging** but the document list fails with **"Could not load documents"** (and upload would fail too).

**Root cause:** the page's data layer calls `callClawInterfaceAPI('/knowledge-base/*')` → web BFF `/api/claw/*` → `CLAW_INTERFACE_URL` (**claw-interface**). But the `/knowledge-base/*` endpoints live only in **`ecap-proxy-service`** (separate repo + separate ingress). `services/claw-interface` had no kb route and no forwarding, so it 404'd. The frontend is correct — the established pattern for reaching ecap-proxy-service from the web app is *through* claw-interface (exactly what `composio_connectors` does); this feature's backend half was simply missing.

## Change (backend-only, frontend unchanged)

Add `app/routes/knowledge_base.py`, mirroring `composio_connectors._proxy_request`:

- `GET /knowledge-base/documents` → forward to `SETTINGS.ECAP_PROXY_SERVICE_URL` with the caller's `Authorization: Bearer <token>`.
- `POST /knowledge-base/upload` → forward the multipart body **verbatim** (original `Content-Type`/boundary preserved — transparent passthrough, no re-encoding); reject `>50MB` early with `413` (mirrors the web soft-check and `VERTEX_SEARCH_MAX_UPLOAD_BYTES`).
- Reuse composio's error handling: `401` (missing token), `502` (upstream `RequestError`), upstream status/detail propagation, `retries=1` connect-retry transport.

`CLAW_INTERFACE_URL` stays pointed at claw-interface; no web change.

## Testing

### Static + unit
- `bash scripts/verify-py.sh` — ruff + ruff-format + pyright + import-linter all pass.
- `pytest tests/unit/test_knowledge_base.py` — 8 passed (forwarding + headers, multipart passthrough, 413 via content-length and via body length, retries=1 transport, 502 on RequestError, upstream status/detail propagation, 401 on missing token).

### Local integration vs the REAL ecap-proxy-service
Exercised the route handlers directly against the real staging `ecap-proxy-service` over a Telepresence connection (no deploy, no mongo needed), with a real staging user bearer token:

- `GET /knowledge-base/documents` → **200**, returned the user's real org documents (2 `indexed`).
- `POST /knowledge-base/upload` (small `text/plain` multipart) → **200**, `success: true`, `status: pending` (file really written to the org's knowledge base + indexing queued).
- Re-`GET` → the uploaded file appears as `pending` (the same end-to-end propagation the page's React Query invalidate-on-success surfaces).
- Invalid/dummy token → **401** with the upstream detail propagated.

This confirms the forward path, URL construction, bearer forwarding, multipart passthrough, and upstream error/status propagation against the real backend — i.e. the exact path that previously 404'd now works.

## Deployment

Requires deploying **claw-interface** to staging for the fix to take effect in the deployed site. No frontend deploy needed.

Closes #2627


---

## fix(claw-interface): use billing v2 plan for agent quota (#2628)
- **SHA**: `92895b6b2851f591df84aeeb50599b15e6cd0039`
- **作者**: bill-srp <bill@srp.one>
- **日期**: 2026-06-27T03:47:52Z
- **PR**: #2628

### 完整 Commit Message

```
fix(claw-interface): use billing v2 plan for agent quota (#2628)

## Summary
- Use Billing v2 current access as the source of truth for agent install
quota plan checks.
- Keep vertical/enterprise package bypass behavior unchanged.
- Add regression coverage for stale `ecap-account.plan` on single and
batch agent installs.

## Root cause
Agent install quota checks used the cached compatibility field
`ecap-account.plan`. That field can drift from the current Billing v2
subscription agreement, so users with a higher active subscription could
still be capped by a stale lower plan.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-py.sh`
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_agent_install_service.py
services/claw-interface/tests/unit/test_agent_multi_install_service.py
-q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash
scripts/verify-changed.sh`
```

### PR 描述

## Summary
- Use Billing v2 current access as the source of truth for agent install quota plan checks.
- Keep vertical/enterprise package bypass behavior unchanged.
- Add regression coverage for stale `ecap-account.plan` on single and batch agent installs.

## Root cause
Agent install quota checks used the cached compatibility field `ecap-account.plan`. That field can drift from the current Billing v2 subscription agreement, so users with a higher active subscription could still be capped by a stale lower plan.

## Test plan
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-py.sh`
- [x] `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_agent_install_service.py services/claw-interface/tests/unit/test_agent_multi_install_service.py -q`
- [x] `PATH=/Users/bill/.venvs/claw-interface/bin:$PATH bash scripts/verify-changed.sh`


---

## feat(knowledge-base): org knowledge-base upload page (#2617)
- **SHA**: `4e65f7a91758a0ef0abd6da7795b0391c15e1e19`
- **作者**: kevin <kevin@srp.one>
- **日期**: 2026-06-27T02:53:59Z
- **PR**: #2617

### 完整 Commit Message

```
feat(knowledge-base): org knowledge-base upload page (#2617)

## What

Admartels a standalone **org knowledge-base** page to `web-app` at
`/<locale>/knowledge-base`. It lists the organization's documents with
their index status and lets a member upload new documents — backed by
the existing `ecap-proxy-service` `/knowledge-base/*` endpoints.

The page lives under the `(app)` route group (so it inherits login +
`AccountSessionGate`) but is **not** registered in any nav menu — it's
reachable only at its own URL, as requested.

## How

- **Service** `src/services/knowledge-base.ts` — typed wrappers over the
existing `callClawInterfaceAPI` (routes through the `/api/claw` BFF →
proxy service, auto-attaches the JWT). Upload is `multipart/form-data`
(field `file`) with a 120s timeout.
- **Hook** `hooks/useKnowledgeBase.ts` — React Query: uid-scoped
documents query + upload mutation that **invalidates the list on
success** (no polling; new docs appear as `pending`).
- **Components** — `UploadDropzone` (click + drag-drop with client-side
type/size validation), `DocumentList` (rows + empty state),
`StatusBadge` (indexed/pending/failed via semantic `ecap-*` tokens).
- **Page** — `KnowledgeBaseClient` composes them with
success/warning/error toasts; `page.tsx` is a server component wrapping
it in `<Suspense>`.
- **i18n** — new `knowledgeBase` namespace in `en.ts` + `zh.ts` (other
locales fall back to English).

## Tenancy / security

Org is resolved **server-side from the JWT**; the client never sends
uid/org in the request body (upload sends only the file; list is a bare
GET). The uid only scopes the React Query cache key, so switching
accounts can't leak another org's cached list.

## Scope

List + basic single-file upload. Intentionally **no** polling, batch
upload, or delete/rename (none were requested; the backend exposes no
delete).

## Tests

14 unit tests across service, hook, and the three components (Vitest).
`pnpm tsc --noEmit` and `pnpm eslint` over the feature both pass clean.

⚠️ **Not yet done** (needs a live backend + auth, infeasible in the dev
sandbox): manual smoke test of `/en/knowledge-base` against a running
proxy service — please verify the live list-load + a real upload before
merge.

Design + plan:
`docs/superpowers/specs/2026-06-26-knowledge-base-upload-page-design.md`,
`docs/superpowers/plans/2026-06-26-knowledge-base-upload-page.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
Co-authored-by: Developer <dev@srp.one>
```

### PR 描述

## What

Admartels a standalone **org knowledge-base** page to `web-app` at `/<locale>/knowledge-base`. It lists the organization's documents with their index status and lets a member upload new documents — backed by the existing `ecap-proxy-service` `/knowledge-base/*` endpoints.

The page lives under the `(app)` route group (so it inherits login + `AccountSessionGate`) but is **not** registered in any nav menu — it's reachable only at its own URL, as requested.

## How

- **Service** `src/services/knowledge-base.ts` — typed wrappers over the existing `callClawInterfaceAPI` (routes through the `/api/claw` BFF → proxy service, auto-attaches the JWT). Upload is `multipart/form-data` (field `file`) with a 120s timeout.
- **Hook** `hooks/useKnowledgeBase.ts` — React Query: uid-scoped documents query + upload mutation that **invalidates the list on success** (no polling; new docs appear as `pending`).
- **Components** — `UploadDropzone` (click + drag-drop with client-side type/size validation), `DocumentList` (rows + empty state), `StatusBadge` (indexed/pending/failed via semantic `ecap-*` tokens).
- **Page** — `KnowledgeBaseClient` composes them with success/warning/error toasts; `page.tsx` is a server component wrapping it in `<Suspense>`.
- **i18n** — new `knowledgeBase` namespace in `en.ts` + `zh.ts` (other locales fall back to English).

## Tenancy / security

Org is resolved **server-side from the JWT**; the client never sends uid/org in the request body (upload sends only the file; list is a bare GET). The uid only scopes the React Query cache key, so switching accounts can't leak another org's cached list.

## Scope

List + basic single-file upload. Intentionally **no** polling, batch upload, or delete/rename (none were requested; the backend exposes no delete).

## Tests

14 unit tests across service, hook, and the three components (Vitest). `pnpm tsc --noEmit` and `pnpm eslint` over the feature both pass clean.

⚠️ **Not yet done** (needs a live backend + auth, infeasible in the dev sandbox): manual smoke test of `/en/knowledge-base` against a running proxy service — please verify the live list-load + a real upload before merge.

Design + plan: `docs/superpowers/specs/2026-06-26-knowledge-base-upload-page-design.md`, `docs/superpowers/plans/2026-06-26-knowledge-base-upload-page.md`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
