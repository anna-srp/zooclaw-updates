# SerendipityOneInc/ecap-workspace — commits 2026-09-09

## fix(agents): use CSFLE-compatible shared install lookup (#3681)

- **SHA**: `489305861efb5b6da57365780d7a085c3270183b`
- **作者**: kaka-srp
- **日期**: 2026-09-09T12:47:22Z
- **PR**: #3681

### Commit Message

```
fix(agents): use CSFLE-compatible shared install lookup (#3681)

## Summary

Fix shared-Agent install preview and installation failing with `Internal
Server Error` after #3678. The deployed CSFLE client rejects its
cross-collection `$lookup` aggregation before MongoDB executes it, even
though the ordinary MongoDB CI tests passed.

- Replace only the source-install lookup with owner/org-scoped, bounded
single-collection reads and batched association. Preserve source
identity across regenerated links, prefer the newest retained copy, and
retain the latest removed record for reinstallation. Continue across
batches instead of silently checking only the first N records; no
per-record N+1 queries.
- Add pagination/ownership regression coverage and a small syntax guard
for known unsupported cross-collection stages and directly specified
aggregation-pipeline updates. The guard is explicitly not a substitute
for real CSFLE validation.
- Record the repeated encrypted-client compatibility lesson in
root/backend `AGENTS.md`: no encryption bypass, and new query forms
require actual encrypted-client verification rather than plain-Mongo CI
alone.

## Verification

- 61 targeted unit tests passed (query contract, install lookup,
sharing, creation claims, avatars, deletion).
- `bash scripts/verify-local.sh --py-static` passed: Ruff, formatting,
Pyright, import contracts.
- The new syntax guard failed on the old query's two `$lookup` stages
and passed after the fix.
- Read-only validation in the existing staging backend pod, using its
actual encrypted client (`_enable_encryption=True`): the deployed query
reproduced `EncryptionError`; the candidate repository operation for the
incident recipient and current organization succeeded in about 20 ms.
The link and workspace single-collection query forms also passed with
existing records. No live data, configuration, deployed files, or
running service process was modified.
- Eight repository BDD scenarios are locally skipped because local test
MongoDB is unavailable; CI must execute them against its MongoDB. This
is separate from the staging encrypted-client check above.
- CI completed successfully on `90b733b79`: backend full suite **10,720
passed / 5 skipped**, static/import checks, duplication checks, CodeQL,
and required gates all passed. CI provisions MongoDB and runs the entire
`tests` tree. Automated code review reported no findings; human approval
is still required.

## Scope and rollout

Backend hotfix only. No frontend, Engine, ACS, driver upgrades, database
migrations, new indexes, encryption configuration changes, or changes to
copy/edit/installation identity semantics. Existing share links need not
be recreated.

Normal staging deployment after merge, followed by a backend-only
release. Browser end-to-end installation has not yet been validated on a
deployed fixed version; the staging check exercised the candidate read
path, not an installation mutation.
```

### PR Body

## Summary

Fix shared-Agent install preview and installation failing with `Internal Server Error` after #3678. The deployed CSFLE client rejects its cross-collection `$lookup` aggregation before MongoDB executes it, even though the ordinary MongoDB CI tests passed.

- Replace only the source-install lookup with owner/org-scoped, bounded single-collection reads and batched association. Preserve source identity across regenerated links, prefer the newest retained copy, and retain the latest removed record for reinstallation. Continue across batches instead of silently checking only the first N records; no per-record N+1 queries.
- Add pagination/ownership regression coverage and a small syntax guard for known unsupported cross-collection stages and directly specified aggregation-pipeline updates. The guard is explicitly not a substitute for real CSFLE validation.
- Record the repeated encrypted-client compatibility lesson in root/backend `AGENTS.md`: no encryption bypass, and new query forms require actual encrypted-client verification rather than plain-Mongo CI alone.

## Verification

- 61 targeted unit tests passed (query contract, install lookup, sharing, creation claims, avatars, deletion).
- `bash scripts/verify-local.sh --py-static` passed: Ruff, formatting, Pyright, import contracts.
- The new syntax guard failed on the old query's two `$lookup` stages and passed after the fix.
- Read-only validation in the existing staging backend pod, using its actual encrypted client (`_enable_encryption=True`): the deployed query reproduced `EncryptionError`; the candidate repository operation for the incident recipient and current organization succeeded in about 20 ms. The link and workspace single-collection query forms also passed with existing records. No live data, configuration, deployed files, or running service process was modified.
- Eight repository BDD scenarios are locally skipped because local test MongoDB is unavailable; CI must execute them against its MongoDB. This is separate from the staging encrypted-client check above.
- CI completed successfully on `90b733b79`: backend full suite **10,720 passed / 5 skipped**, static/import checks, duplication checks, CodeQL, and required gates all passed. CI provisions MongoDB and runs the entire `tests` tree. Automated code review reported no findings; human approval is still required.

## Scope and rollout

Backend hotfix only. No frontend, Engine, ACS, driver upgrades, database migrations, new indexes, encryption configuration changes, or changes to copy/edit/installation identity semantics. Existing share links need not be recreated.

Normal staging deployment after merge, followed by a backend-only release. Browser end-to-end installation has not yet been validated on a deployed fixed version; the staging check exercised the candidate read path, not an installation mutation.


---

## fix(agents): fix initial Build, shared installs and launch notices (#3678)

- **SHA**: `6d1d49a24d050fedd1098322b345cbbcbe7a73e4`
- **作者**: kaka-srp
- **日期**: 2026-09-09T12:00:36Z
- **PR**: #3678

### Commit Message

```
fix(agents): fix initial Build, shared installs and launch notices (#3678)

## Summary
- Start the first Build turn from the creation intent through the
existing Mattermost conversation transport before navigating to Build.
Typed intents and example prompts use the same path; blank creation
remains blank.
- Retain the creation idempotency key on failures and reconcile thread
history before retrying a send, including lost POST responses.
- Validate the shared Mattermost message-length limit before
provisioning, so overlong prompts cannot create an Agent whose initial
message cannot be sent.
- Switch ECAP frontend/backend Launch release-note generation to Azure
Responses with GPT-5.6 Terra, matching the verified Engine notification
path.
- Reuse existing organization endpoint/key, release bot, target chat and
shared workflow. No service deployment, secret changes or new
notification pipeline.
- Resolve annotated release tags to their commit SHA on manual
notification dispatch, matching Engine and avoiding false rollback
announcements.

## Root cause
Creating an Agent only persisted its initial configuration. No first
user message was posted to the Build conversation, so users had to
re-enter their intent after navigation.

The notifications for `ecap-v0.19.0-release` and
`service-v0.18.0-release` failed when Claude returned `is_error: true`
without producing release notes. Production deployment succeeded; Lark
sending was never reached.

Engine fixed the same failure in
[#1315](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1315).
Shared Azure generation support is already merged in [srp-actions
#136](https://github.com/SerendipityOneInc/srp-actions/pull/136).
Engine's v0.2.0 [generation and delivery
run](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/34332195703)
succeeded.

Dry-run verification also exposed an existing manual-resend issue:
resolving an annotated tag without `^{commit}` used a tag-object SHA,
allowing the current deployment to be selected as its own baseline and
announced as a rollback. No incorrect announcement was sent.

## Test plan
- [x] Focused creation/service/flow tests: 28 tests passed, including
4,000-character success and 4,001/8,000-character rejection before
provisioning. Broader selected frontend tests: 117 tests passed;
TypeScript and ESLint passed.
- [x] Parse workflow YAML and execute the actual resolve step against
both production annotated tags; each resolves to deployed commit
`83c21054e9f9bcb58f4c8594a537ffe109166e40`, with recipient routing
preserved.
- [x] Verify existing organization endpoint and required secret names
are available to ECAP without reading secret values.
- [x] `git diff --check` and changed-surface verification passed for the
original frontend changes; shared-install checks are listed below.
- [x] Notification-only dry runs passed for both production tags with
correct release baselines:
[frontend](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34334945038),
[backend](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34334946796).
- [x] Both formal resends succeeded to the existing Launch group using
the existing bot:
[frontend](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34335114512),
[backend](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34335116803).
Lark returned success and message IDs for both; no application
deployment was retriggered.

The first-Build-message fix requires a frontend release after merge. The
shared-install follow-up below also requires a claw-interface release.
Engine and ACS application code remain unchanged. Replaying the two
existing release notifications does not redeploy any service or announce
this unshipped fix.

## Shared Agent follow-up (owner-approved scope)
- Deduplicate by recipient UID + destination organization + source
Agent, across page visits, request keys and regenerated sharing links.
Different users in the same organization still have independent copies.
- Repeated installs open the retained copy without changing its
configuration, revisions or user edits. Installed copies remain editable
in Build; author/recipient changes do not synchronize.
- Concurrent fresh requests use the existing durable creation/quota
claim with a source-scoped identity. Removed copies seed a fresh
identity for reinstallation, instead of reviving deleted
runtime/history. Installation-in-progress returns the existing retryable
conflict.
- Recover reinstallation even if runtime creation succeeded but writing
its installation record failed: consult the existing workspace
tombstones when selecting the next identity. Live unrecorded copies are
still reused, and concurrent retries still share one creation claim.
- The install page displays **Open installed Agent** when the recipient
already has a copy. The POST rechecks the server state before
navigation.
- Reuse existing share/install/workspace records; add a recipient lookup
index. No new tables, migration/backfill, Engine/ACS changes, or
automatic cleanup of pre-existing duplicates.

### Follow-up validation
- 57 focused backend unit cases (sharing, creation concurrency, avatar
and deletion) and 16 frontend cases cover copy reuse, edited-copy
preservation, user/org isolation, regenerated links, deletion/reinstall,
concurrent requests, first Build messages and install-page actions.
- Fault-injection regressions failed on the old implementation and pass
after the narrow recovery fix, including three consecutive failed audit
writes followed by deletion/reinstallation, retained-copy retries, and
concurrent reinstallation after removal.
- Real MongoDB regression scenarios were added for cross-link lookup,
recipient isolation, retained/deleted-copy selection and duplicate audit
records. Local MongoDB execution was skipped because no local server is
running; the Mongo-backed CI suite passed on `809899dca` (10,714 passed,
5 skipped).
- Ruff/format, Python type-check, import boundaries, frontend
TypeScript/ESLint and all commit/push hooks passed. [CI on
`809899dca`](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34348074649)
passed, including frontend tests/build, backend tests, quality gates and
CodeQL. All reported checks settled without failures; the latest Codex
review has no findings.

No application deployment or production/staging data mutation is part of
this follow-up. Existing duplicate user copies are not deleted.
```

### PR Body

## Summary
- Start the first Build turn from the creation intent through the existing Mattermost conversation transport before navigating to Build. Typed intents and example prompts use the same path; blank creation remains blank.
- Retain the creation idempotency key on failures and reconcile thread history before retrying a send, including lost POST responses.
- Validate the shared Mattermost message-length limit before provisioning, so overlong prompts cannot create an Agent whose initial message cannot be sent.
- Switch ECAP frontend/backend Launch release-note generation to Azure Responses with GPT-5.6 Terra, matching the verified Engine notification path.
- Reuse existing organization endpoint/key, release bot, target chat and shared workflow. No service deployment, secret changes or new notification pipeline.
- Resolve annotated release tags to their commit SHA on manual notification dispatch, matching Engine and avoiding false rollback announcements.

## Root cause
Creating an Agent only persisted its initial configuration. No first user message was posted to the Build conversation, so users had to re-enter their intent after navigation.

The notifications for `ecap-v0.19.0-release` and `service-v0.18.0-release` failed when Claude returned `is_error: true` without producing release notes. Production deployment succeeded; Lark sending was never reached.

Engine fixed the same failure in [#1315](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1315). Shared Azure generation support is already merged in [srp-actions #136](https://github.com/SerendipityOneInc/srp-actions/pull/136). Engine's v0.2.0 [generation and delivery run](https://github.com/SerendipityOneInc/zooclaw-engine/actions/runs/34332195703) succeeded.

Dry-run verification also exposed an existing manual-resend issue: resolving an annotated tag without `^{commit}` used a tag-object SHA, allowing the current deployment to be selected as its own baseline and announced as a rollback. No incorrect announcement was sent.

## Test plan
- [x] Focused creation/service/flow tests: 28 tests passed, including 4,000-character success and 4,001/8,000-character rejection before provisioning. Broader selected frontend tests: 117 tests passed; TypeScript and ESLint passed.
- [x] Parse workflow YAML and execute the actual resolve step against both production annotated tags; each resolves to deployed commit `83c21054e9f9bcb58f4c8594a537ffe109166e40`, with recipient routing preserved.
- [x] Verify existing organization endpoint and required secret names are available to ECAP without reading secret values.
- [x] `git diff --check` and changed-surface verification passed for the original frontend changes; shared-install checks are listed below.
- [x] Notification-only dry runs passed for both production tags with correct release baselines: [frontend](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34334945038), [backend](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34334946796).
- [x] Both formal resends succeeded to the existing Launch group using the existing bot: [frontend](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34335114512), [backend](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34335116803). Lark returned success and message IDs for both; no application deployment was retriggered.

The first-Build-message fix requires a frontend release after merge. The shared-install follow-up below also requires a claw-interface release. Engine and ACS application code remain unchanged. Replaying the two existing release notifications does not redeploy any service or announce this unshipped fix.

## Shared Agent follow-up (owner-approved scope)
- Deduplicate by recipient UID + destination organization + source Agent, across page visits, request keys and regenerated sharing links. Different users in the same organization still have independent copies.
- Repeated installs open the retained copy without changing its configuration, revisions or user edits. Installed copies remain editable in Build; author/recipient changes do not synchronize.
- Concurrent fresh requests use the existing durable creation/quota claim with a source-scoped identity. Removed copies seed a fresh identity for reinstallation, instead of reviving deleted runtime/history. Installation-in-progress returns the existing retryable conflict.
- Recover reinstallation even if runtime creation succeeded but writing its installation record failed: consult the existing workspace tombstones when selecting the next identity. Live unrecorded copies are still reused, and concurrent retries still share one creation claim.
- The install page displays **Open installed Agent** when the recipient already has a copy. The POST rechecks the server state before navigation.
- Reuse existing share/install/workspace records; add a recipient lookup index. No new tables, migration/backfill, Engine/ACS changes, or automatic cleanup of pre-existing duplicates.

### Follow-up validation
- 57 focused backend unit cases (sharing, creation concurrency, avatar and deletion) and 16 frontend cases cover copy reuse, edited-copy preservation, user/org isolation, regenerated links, deletion/reinstall, concurrent requests, first Build messages and install-page actions.
- Fault-injection regressions failed on the old implementation and pass after the narrow recovery fix, including three consecutive failed audit writes followed by deletion/reinstallation, retained-copy retries, and concurrent reinstallation after removal.
- Real MongoDB regression scenarios were added for cross-link lookup, recipient isolation, retained/deleted-copy selection and duplicate audit records. Local MongoDB execution was skipped because no local server is running; the Mongo-backed CI suite passed on `809899dca` (10,714 passed, 5 skipped).
- Ruff/format, Python type-check, import boundaries, frontend TypeScript/ESLint and all commit/push hooks passed. [CI on `809899dca`](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34348074649) passed, including frontend tests/build, backend tests, quality gates and CodeQL. All reported checks settled without failures; the latest Codex review has no findings.

No application deployment or production/staging data mutation is part of this follow-up. Existing duplicate user copies are not deleted.


---

## fix(enterprise-admin): Cookie-only identity and show purchaser on Vertical Pack checkout (#3676)

- **SHA**: `ae1740fc2e9964a7686bb7adb343433d41b3b563`
- **作者**: bill-srp
- **日期**: 2026-09-09T11:28:40Z
- **PR**: #3676

### Commit Message

```
fix(enterprise-admin): Cookie-only identity and show purchaser on Vertical Pack checkout (#3676)

## Summary
- Business (enterprise-admin) no longer reads the legacy localStorage
account token (`zooclaw:auth:account_token`). Identity and every
`/api/claw/*`, `/api/auth/me`, and `/api/r2/*` call now rely solely on
the `zc_session` cookie. Any browser still holding the legacy key has it
purged on the next identity load.
- The Vertical Pack checkout page now shows who is purchasing — avatar,
name, email, organization and a Business / Personal badge — in both the
payment state and the "Only enterprise accounts can purchase" gate, plus
a "Not you? Switch account" action in the payment state.

## Root cause
A customer reported the enterprise-only gate although both of their
Business accounts are team admins in production and the backend accepted
their checkouts (`POST /vertical-pack/plan/…/purchase` → 201 for both on
2026-09-09). The gate had to have been evaluated for a different
identity: Business shares the session cookie with the main site, and a
stale legacy bearer token in localStorage could additionally override
the cookie on API calls because the BFF prefers the `Authorization`
header. The page never showed which account it was acting as, so neither
the customer nor support could tell from a screenshot. PR #3674 fixed
the identity refresh and logout race; this PR removes the second
identity source on the client and makes the acting identity visible.

## Changes
- `services/api.ts` — no `Authorization` header; requests are
cookie-authenticated same-origin.
- `lib/auth.ts` — `fetchAccountUser` cookie-only; `fetchLegacyUserMe`
and the `getStoredAccountToken()` fallbacks removed; `loadCurrentUser`
purges the legacy key before fetching.
- `lib/legacy-auth-header.ts` — deleted; `lib/r2/upload.ts`,
`components/packs/SubmissionList.tsx`,
`components/onboarding/OrgLogoField.tsx` stop attaching it.
- `app/vertical-pack-plan/[planId]/checkout/useCheckoutViewModel.ts` —
new `identity` (`CheckoutIdentity`) derived from `useAuth()`.
- `app/vertical-pack-plan/[planId]/checkout/CheckoutPageClient.tsx` —
`CheckoutIdentityBlock` (`data-testid="checkout-identity"`) rendered
under the eyebrow in both states; switch-account calls the existing
awaited `logout`.
- `lib/initials.ts` — `initialsFromEmail(email, displayName)` extracted
from `AccountMenu.tsx`, which now imports it.
- `lib/i18n-zh.ts` — `checkout.purchasingAs`, `checkout.switchAccount`,
`checkout.orgTypeTeam`, `checkout.orgTypePersonal`.
- `AGENTS.md` — API-access note updated to cookie-only client auth.
- Tests: checkout page (identity in team and personal states,
switch-account flow, no block when signed out),
`lib/__tests__/auth.test.ts` (legacy token purged with and without a
valid cookie, no `/api/claw/account/me` fallback),
`services/__tests__/api.test.ts` (no bearer even when a token is
stored), R2 / pack / logo tests, and dashboard page tests migrated from
legacy `/account/me` bearer mocks to the `/api/auth/me` cookie shape.

## Not in scope
- Server-side header-over-cookie precedence in
`lib/auth-session-cookie.ts` / `app/api/**` is unchanged (bearer
compatibility for non-browser callers). Follow-up candidate.
- Main web app (`web/app`) keeps its localStorage token as its primary
auth transport.
- Network-failure → `null` semantics in `loadCurrentUser` unchanged (see
review nit on #3674).

## Test plan
- [x] `pnpm exec vitest run` in `web/enterprise-admin`: 59 files, 447
tests passed
- [x] `pnpm exec tsc --noEmit`: clean
- [x] `pnpm run lint` (`eslint . --max-warnings=0`): clean
- [x] `grep -rn "legacyAuthorizationHeader\|getStoredAccountToken"
web/enterprise-admin` returns only test lines asserting the purge /
absent header
- [ ] Manual after deploy: sign into Business as a team admin, open a
plan checkout → identity block shows the admin email + "Business
account"; sign into zoowork.ai with a personal account in another tab,
refocus the checkout → identity block flips to the personal email +
"Personal account" gate

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_015xJSn7ZuFstN6ZnjP3CwKS

---------

Co-authored-by: Claude Fable 5.1 <noreply@anthropic.com>
```

### PR Body

## Summary
- Business (enterprise-admin) no longer reads the legacy localStorage account token (`zooclaw:auth:account_token`). Identity and every `/api/claw/*`, `/api/auth/me`, and `/api/r2/*` call now rely solely on the `zc_session` cookie. Any browser still holding the legacy key has it purged on the next identity load.
- The Vertical Pack checkout page now shows who is purchasing — avatar, name, email, organization and a Business / Personal badge — in both the payment state and the "Only enterprise accounts can purchase" gate, plus a "Not you? Switch account" action in the payment state.

## Root cause
A customer reported the enterprise-only gate although both of their Business accounts are team admins in production and the backend accepted their checkouts (`POST /vertical-pack/plan/…/purchase` → 201 for both on 2026-09-09). The gate had to have been evaluated for a different identity: Business shares the session cookie with the main site, and a stale legacy bearer token in localStorage could additionally override the cookie on API calls because the BFF prefers the `Authorization` header. The page never showed which account it was acting as, so neither the customer nor support could tell from a screenshot. PR #3674 fixed the identity refresh and logout race; this PR removes the second identity source on the client and makes the acting identity visible.

## Changes
- `services/api.ts` — no `Authorization` header; requests are cookie-authenticated same-origin.
- `lib/auth.ts` — `fetchAccountUser` cookie-only; `fetchLegacyUserMe` and the `getStoredAccountToken()` fallbacks removed; `loadCurrentUser` purges the legacy key before fetching.
- `lib/legacy-auth-header.ts` — deleted; `lib/r2/upload.ts`, `components/packs/SubmissionList.tsx`, `components/onboarding/OrgLogoField.tsx` stop attaching it.
- `app/vertical-pack-plan/[planId]/checkout/useCheckoutViewModel.ts` — new `identity` (`CheckoutIdentity`) derived from `useAuth()`.
- `app/vertical-pack-plan/[planId]/checkout/CheckoutPageClient.tsx` — `CheckoutIdentityBlock` (`data-testid="checkout-identity"`) rendered under the eyebrow in both states; switch-account calls the existing awaited `logout`.
- `lib/initials.ts` — `initialsFromEmail(email, displayName)` extracted from `AccountMenu.tsx`, which now imports it.
- `lib/i18n-zh.ts` — `checkout.purchasingAs`, `checkout.switchAccount`, `checkout.orgTypeTeam`, `checkout.orgTypePersonal`.
- `AGENTS.md` — API-access note updated to cookie-only client auth.
- Tests: checkout page (identity in team and personal states, switch-account flow, no block when signed out), `lib/__tests__/auth.test.ts` (legacy token purged with and without a valid cookie, no `/api/claw/account/me` fallback), `services/__tests__/api.test.ts` (no bearer even when a token is stored), R2 / pack / logo tests, and dashboard page tests migrated from legacy `/account/me` bearer mocks to the `/api/auth/me` cookie shape.

## Not in scope
- Server-side header-over-cookie precedence in `lib/auth-session-cookie.ts` / `app/api/**` is unchanged (bearer compatibility for non-browser callers). Follow-up candidate.
- Main web app (`web/app`) keeps its localStorage token as its primary auth transport.
- Network-failure → `null` semantics in `loadCurrentUser` unchanged (see review nit on #3674).

## Test plan
- [x] `pnpm exec vitest run` in `web/enterprise-admin`: 59 files, 447 tests passed
- [x] `pnpm exec tsc --noEmit`: clean
- [x] `pnpm run lint` (`eslint . --max-warnings=0`): clean
- [x] `grep -rn "legacyAuthorizationHeader\|getStoredAccountToken" web/enterprise-admin` returns only test lines asserting the purge / absent header
- [ ] Manual after deploy: sign into Business as a team admin, open a plan checkout → identity block shows the admin email + "Business account"; sign into zoowork.ai with a personal account in another tab, refocus the checkout → identity block flips to the personal email + "Personal account" gate

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_015xJSn7ZuFstN6ZnjP3CwKS


---

## fix(agents): use runtime identity for self-evolving artifacts (#3677)

- **SHA**: `83c21054e9f9bcb58f4c8594a537ffe109166e40`
- **作者**: kaka-srp
- **日期**: 2026-09-09T08:13:22Z
- **PR**: #3677

### Commit Message

```
fix(agents): use runtime identity for self-evolving artifacts (#3677)

## Summary
- Resolve the runtime ownership scope of an already-authorized
self-evolving workspace with the existing `runtime_actor` helper.
- Apply it to Artifact Library pagination, per-Agent artifact
list/get/download/delete, and workspace file list/content.
- Keep ordinary Engine and legacy runtime behavior, business ownership
checks, and V2 eligibility checks unchanged. No database, Engine, UI, or
deployment configuration changes.

## Root cause
The new Agents store opaque runtime ownership anchors in Engine.
Artifact adapters still passed the caller's business UID/org. In
staging, the same Agent artifact-list request returned `404
agent_not_found` with the business actor and `200` with the definition's
runtime actor. ECAP mapped the former to `Agent runtime state could not
be verified`.

## Test plan
- Regression tests reproduced nine failures before the fix; all 89
targeted Artifact, Files, Library, route, and workspace tests now pass.
- Covers six operations for ordinary/self-evolving Agents and
owner/foreign-user/foreign-org scopes, mixed-Agent library results, both
pagination fetches, and the Agent-scoped library page.
- Full backend Ruff, format, Pyright (`app/ tests/`), and import-linter
checks passed. Pyright was run with the existing Python interpreter
explicitly because this new worktree has no local `.venv` link.
- Only read-only staging probes were performed; no real artifacts,
sessions, configuration, or database records were changed.

## Rollout
Backend-only: merge to main deploys claw-interface to staging. Recheck
the affected Agent's Artifacts page after deployment. No Engine release
or migration is needed.
```

### PR Body

## Summary
- Resolve the runtime ownership scope of an already-authorized self-evolving workspace with the existing `runtime_actor` helper.
- Apply it to Artifact Library pagination, per-Agent artifact list/get/download/delete, and workspace file list/content.
- Keep ordinary Engine and legacy runtime behavior, business ownership checks, and V2 eligibility checks unchanged. No database, Engine, UI, or deployment configuration changes.

## Root cause
The new Agents store opaque runtime ownership anchors in Engine. Artifact adapters still passed the caller's business UID/org. In staging, the same Agent artifact-list request returned `404 agent_not_found` with the business actor and `200` with the definition's runtime actor. ECAP mapped the former to `Agent runtime state could not be verified`.

## Test plan
- Regression tests reproduced nine failures before the fix; all 89 targeted Artifact, Files, Library, route, and workspace tests now pass.
- Covers six operations for ordinary/self-evolving Agents and owner/foreign-user/foreign-org scopes, mixed-Agent library results, both pagination fetches, and the Agent-scoped library page.
- Full backend Ruff, format, Pyright (`app/ tests/`), and import-linter checks passed. Pyright was run with the existing Python interpreter explicitly because this new worktree has no local `.venv` link.
- Only read-only staging probes were performed; no real artifacts, sessions, configuration, or database records were changed.

## Rollout
Backend-only: merge to main deploys claw-interface to staging. Recheck the affected Agent's Artifacts page after deployment. No Engine release or migration is needed.


---

## feat(claw-interface): default V1/V2 chat and catalog to terra (#3675)

- **SHA**: `72d3a0028615c99c3ee8581b031ff2d80daec32f`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-09T07:15:35Z
- **PR**: #3675

### Commit Message

```
feat(claw-interface): default V1/V2 chat and catalog to terra (#3675)

新建 Bot 的默认模型需要切到 GPT-5.6 Terra。原改动只覆盖 V1 套餐默认值，目录默认标记及 V2 创建入口仍有独立配置；本
PR 将这些默认值一并对齐。

## 改动

- 四个套餐及未知套餐 fallback 使用 `gpt-5.6-terra`，V1 创建/缺失配置回填派生为
`openai/gpt-5.6-terra`。
- `CHAT_MODEL_DEFAULT_MODEL=gpt-5.6-terra`，目录即使先列 Claude，也将 Terra
标记为默认；保留默认模型不可用时选择首个有权限模型的现有行为。
- `ZOOCLAW_ENGINE_DEFAULT_MODEL=litellm/gpt-5.6-terra`，V2 主
Agent、没有可解析默认模型的 Pack 安装显式传入 Terra；保留有效 Pack 显式选择及部署配置覆盖。
- `.env.example` 同步两个设置，防止示例中的 Claude/空字符串覆盖新的代码默认值。
-
添加发布核查说明：`docs/staging-validation/2026-09-09-default-terra-rollout.md`。

## 配套与验收边界


[zooclaw-engine#1303](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1303)
已合并（`7bec0c6dd7053ddd190490a55eb1da74babae394`），覆盖 Engine primary/PDF
默认值及 wire API 兼容路径。部署前仍需确认运行版本包含该改动、Terra
路由和套餐权限可用，并核对两个设置的实际环境覆盖值；本次没有执行部署或线上 smoke。

已有 V1/V2 Agent、会话固定模型和可用的 Pack 显式模型保持原值。此 PR **不代表存量 Claude
故障已全部解除**，也不全局隐藏 Claude。评论中要求的存量修复、Claude
可用性调整、Auto/子任务/PDF/后台任务核查，已明确列入发布说明；线上历史数据修复需独立清单、备份、并发保护和回滚，并由人确认执行。V2
Auto 的 Claude Haiku 候选仍是其中一个待核查入口。

## 验证

基于 main `f8d4e4abc` 合并后的修复提交 `e9222fcb3`，Python 3.12.3，本地结果：

- `pytest -q --no-cov`：748 passed，覆盖 plan models、model catalog、V1
client/config、V2 main/install/lifecycle、Agent Builder
model/service/routes/runtime 和 Pack test runtime，共 12 个测试文件。
- `PATH="$PWD/services/claw-interface/.venv/bin:$PATH" bash
scripts/verify-py.sh`：ruff check/format、pyright（0 errors / 0 warnings）、8
项 import-linter 合约全部通过。
- 新回归验证目录默认选择、V2 创建显式传入 Terra、空/缺失/不可解析 Pack 默认值，以及有效 Pack 选择和环境覆盖保持不变。


本地日志：`/tmp/ecap-3675-tests.log`、`/tmp/ecap-3675-additional-tests.log`、`/tmp/ecap-3675-verify.log`。线上部署和存量迁移不在上述单测证据内。
```

### PR Body

新建 Bot 的默认模型需要切到 GPT-5.6 Terra。原改动只覆盖 V1 套餐默认值，目录默认标记及 V2 创建入口仍有独立配置；本 PR 将这些默认值一并对齐。

## 改动

- 四个套餐及未知套餐 fallback 使用 `gpt-5.6-terra`，V1 创建/缺失配置回填派生为 `openai/gpt-5.6-terra`。
- `CHAT_MODEL_DEFAULT_MODEL=gpt-5.6-terra`，目录即使先列 Claude，也将 Terra 标记为默认；保留默认模型不可用时选择首个有权限模型的现有行为。
- `ZOOCLAW_ENGINE_DEFAULT_MODEL=litellm/gpt-5.6-terra`，V2 主 Agent、没有可解析默认模型的 Pack 安装显式传入 Terra；保留有效 Pack 显式选择及部署配置覆盖。
- `.env.example` 同步两个设置，防止示例中的 Claude/空字符串覆盖新的代码默认值。
- 添加发布核查说明：`docs/staging-validation/2026-09-09-default-terra-rollout.md`。

## 配套与验收边界

[zooclaw-engine#1303](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1303) 已合并（`7bec0c6dd7053ddd190490a55eb1da74babae394`），覆盖 Engine primary/PDF 默认值及 wire API 兼容路径。部署前仍需确认运行版本包含该改动、Terra 路由和套餐权限可用，并核对两个设置的实际环境覆盖值；本次没有执行部署或线上 smoke。

已有 V1/V2 Agent、会话固定模型和可用的 Pack 显式模型保持原值。此 PR **不代表存量 Claude 故障已全部解除**，也不全局隐藏 Claude。评论中要求的存量修复、Claude 可用性调整、Auto/子任务/PDF/后台任务核查，已明确列入发布说明；线上历史数据修复需独立清单、备份、并发保护和回滚，并由人确认执行。V2 Auto 的 Claude Haiku 候选仍是其中一个待核查入口。

## 验证

基于 main `f8d4e4abc` 合并后的修复提交 `e9222fcb3`，Python 3.12.3，本地结果：

- `pytest -q --no-cov`：748 passed，覆盖 plan models、model catalog、V1 client/config、V2 main/install/lifecycle、Agent Builder model/service/routes/runtime 和 Pack test runtime，共 12 个测试文件。
- `PATH="$PWD/services/claw-interface/.venv/bin:$PATH" bash scripts/verify-py.sh`：ruff check/format、pyright（0 errors / 0 warnings）、8 项 import-linter 合约全部通过。
- 新回归验证目录默认选择、V2 创建显式传入 Terra、空/缺失/不可解析 Pack 默认值，以及有效 Pack 选择和环境覆盖保持不变。

本地日志：`/tmp/ecap-3675-tests.log`、`/tmp/ecap-3675-additional-tests.log`、`/tmp/ecap-3675-verify.log`。线上部署和存量迁移不在上述单测证据内。


---

## feat(agents): build self-evolving agents in a unified task workspace (#3673)

- **SHA**: `7c4249923978ffa71c4d8da2515797e0a1d64870`
- **作者**: kaka-srp
- **日期**: 2026-09-09T06:56:52Z
- **PR**: #3673

### Commit Message

```
feat(agents): build self-evolving agents in a unified task workspace (#3673)

## Summary

Complete self-evolving Agent development feature and its full-review
repairs. Companion PRs: [Engine
#1297](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1297)
and [ACS
#117](https://github.com/SerendipityOneInc/agent-channel-service/pull/117).

- Create a real runnable Agent; Build upgrades that same Agent through
source Revisions. No Pack/archive build pipeline or separate builder
Agent.
- Reuse the full normal chat UI and ACS/Engine message, history and
attachment transport. Build has a dedicated session; normal task threads
use the latest settings on their next user turn.
- Commit/apply source changes automatically. Remove Preview/Activate/My
Team publication from this feature. Agent-scoped navigation includes
tasks, Build, artifacts, schedules and connected channels.
- Support source-file and skill editing, avatar authoring, share-link
installation into an independent editable copy, and fast bulk 14-day
activity/conversation statistics.
- Retire global marketplace/legacy Builder navigation and legacy project
creation; retain existing project editing through Agents → Legacy agent
projects.

## Review and fixes

Three independent agents reviewed Web, business/backend and Engine/ACS.
Findings were adjudicated against current source and approved product
decisions before repair:

- Bind authoring turns to exact runtime configuration including latest
channel/MCP credentials; retries and committed tool receipts keep their
original snapshot.
- Add durable quota reservations under the existing short shared install
lock, same-key single execution and failed-runtime cleanup; enforce
normal plan model permissions for creation, share installation and
source commits.
- Initialize personal MCP through the existing install path; validate
initial source and secret prefixes; prevent normalized skill-name
collisions without renaming existing bindings.
- Fetch current full Revisions by immutable ID. Load source-free history
summaries only when opened, eliminating repeated full-history source
polling.
- Isolate share preview caches per capability/open without putting
bearer tokens in query keys. Reset creation idempotency when the
requested input changes.
- Preserve Engine skill context in shared chat and restore
scheduled-result navigation to the existing result reader.
- Surface dependency rebuild conflicts explicitly: saved but not
applied, no implicit interruption of running tasks.

## Test plan

- [x] Integrated changed frontend regression selection: 52 files, 788
passed / 69 skipped / 1 todo.
- [x] Integrated changed backend selection: 381 tests passed.
- [x] Focused runtime client/apply tests: 80 passed.
- [x] Final integrated changed-surface gates: frontend guards,
typecheck, ESLint; backend ruff, format, pyright and all 8 import
contracts.
- [x] Design and implementation documents consolidated from 2,069 to
about 560 lines, with only current decisions and explicit acceptance
boundaries.
- [x] Previous full ECAP CI passed on `8c878a2a4`: Web 728 files / 9,694
passed (70 skipped, 1 todo); backend 10,625 passed (5 skipped), coverage
89.52% against the unchanged 89.50% requirement. Web build, all
applicable quality/type/lint jobs, CodeQL and required aggregate checks
passed.
- [ ] Coordinated feature/staging acceptance and required human approval
remain outstanding; no live rollout performed in this review pass.

## Latest follow-up verification (2026-09-09)

- Pushed follow-up commit `3c3879042`: preserve channel-owned read-only
history and bindings, hide edit history outside Build, and handle
successful HTTP 204 deletion without attempting JSON decoding. The user
approved the existing `size-override` mechanism for all three companion
PRs; the label is applied, all normal pre-push type/static checks
passed, and the commit is now on the PR.
- Local regression selection passed: Web 41 files / 309 tests, backend
31 tests, shared chat UI 8 tests. Changed-surface type/static checks and
the complete commit hooks passed.
- This pass also verified a real local Feishu inbound message through
the intended Agent run and successful ACS outbound delivery. This is a
scoped channel smoke test, not full feature acceptance or a staging
rollout.
- Engine and ACS code CI passed on their then-current heads. Claude
produced no valid review verdict; per user direction this execution
failure is excluded from code-defect assessment, not relabeled as a
successful review or bypassed in repository protections.
- The first full size-overridden ECAP CI exposed unused legacy-create
source, an outdated staff-only assertion for the two
machine-authenticated authoring routes, and backend coverage of 89.40%
against the unchanged 89.50% gate. Follow-up commit `8c878a2a4` removes
only unused legacy-create source/exports, retains existing project
editing/recovery, explicitly asserts each internal route's proper auth
boundary, and adds
HTTP/tool-dispatch/source-diff/dependency-materialization regression
tests. No authentication implementation or coverage threshold was
changed.
- Follow-up local verification: 41 Web test files / 498 passing tests,
an additional legacy-entry selection of 4 files / 61 passing tests,
backend auth/boundary selection 94 passing tests, focused coverage
selection 92 passing tests, knip, full commit hooks and changed-surface
static gates all passed. Selections overlap and are not summed as unique
tests.
- Previous full CI passed on `8c878a2a4`: [Code Quality
Check](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34319336886).
This is baseline evidence; the configuration-simplification follow-up
below has its own CI run. Skipped path-filtered jobs and the oversized
automated Codex review are not counted as executed tests or review
approval. Required human approval remains outstanding.

## Deployment / rollback

Engine additive schema/runtime must precede ACS's runtime_mode reads;
then deploy ACS and ECAP backend/Web. The feature follows existing V2
eligibility without a separate switch, so its prerequisites must be
ready before the ECAP deployment. Current migration files already
published on staging must remain immutable; this ECAP PR only adds
business fields/collections in MongoDB and does not change Engine
migration contents or execute migrations. Coordinate the worker and ECAP
gateway update: both now derive authentication from the existing Engine
service secret with the same purpose string; mixed old/new derivations
reject Build callbacks until the pair matches. No dedicated token
setting is required. Application rollback retains the additive Engine
schema and restores matching gateway authentication on both sides.

## Deliberate boundaries / remaining decisions

- Ready for review; no merge/deploy authorization. This is the entire
feature, not only the most recent UI diff; its size exceeds the normal
budget. The user approved a one-PR `size-override` exception on
2026-09-09; no global size threshold or code-quality gate was changed.
- The approved `size-override` now allows full quality/build jobs to
run; it does not bypass those checks. Automated Codex review skipped the
oversized diff and is not counted as a completed code review. The
repository already had Claude review disabled; a stale
`cc:request-changes` label from a confirmed initialization failure with
no verdict was removed, and the existing aggregate gate re-evaluated
successfully. No repository variable, check status or human approval was
overridden.
- Dependency changes on an already locked task sandbox require an
explicit rebuild decision because interruption is possible. The safe
refusal/error path is implemented; a confirmation/rebuild UI is not
claimed as implemented.
- Unknown failed creation/cleanup retains its quota reservation.
Retrying the same operation key can recover; losing that key in an
uncertain failure still requires operator recovery. No cross-key alias
registry or additional recovery state machine was introduced.
- Business state stays in ECAP. Engine owns runs/configuration, and a
registered product integration retains the synchronous authoring gateway
without a generic plugin framework or new reconciliation worker.

## Design and implementation

-
`docs/superpowers/specs/2026-09-04-self-evolving-agent-development-design.md`
-
`docs/superpowers/plans/2026-09-04-self-evolving-agent-development-implementation.md`

No Linear issue was created, as requested.


## Size exception

The user explicitly approved `size-override` on all three companion PRs
on 2026-09-09. The existing label has been applied to this PR only; no
repository-wide limit, test requirement or review protection was
changed.

## Configuration simplification (2026-09-09)

User-approved follow-up `158b4d793` removes `AGENT_DEVELOPMENT_ENABLED`
and `AGENT_AUTHORING_GATEWAY_SERVICE_TOKEN` from application settings,
examples and deployment overlays. Agent Development reuses existing V2
eligibility, V1-only exceptions, ownership and quota enforcement.

ECAP derives the lowercase hex HMAC-SHA256 bearer over
`zooclaw:agent-authoring:v1` from `ZOOCLAW_ENGINE_SERVICE_TOKEN`; worker
[Engine
#1297](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1297)
derives the same value from its matching `CONTROLD_SERVICE_TOKEN`. Every
environment uses this path. Missing/wrong/raw service bearers, retired
staging-purpose bearers and stale keys are rejected; there is no
anonymous bypass or additional service.

Verification: 109 focused backend tests passed, including both
authenticated callback routes, shared ASCII/UTF-8 vectors, V2
eligibility, creation, deployment wiring, source ownership and turn
pinning. Full backend static gates, commit hooks and pre-push
frontend/backend checks passed. Full CI passed on `158b4d793`: [Code
Quality
Check](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34321054050).
Backend: 10,649 passed, 5 skipped; coverage 89.52% against the unchanged
89.50% requirement. Web tests/build, applicable static checks, CodeQL
and required aggregate checks passed. ECAP's oversized automated Codex
review remains skipped, not a review approval. No live rollout or
migration was performed. Historical staging evidence is explicitly
marked as predating this change.
```

### PR Body

## Summary

Complete self-evolving Agent development feature and its full-review repairs. Companion PRs: [Engine #1297](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1297) and [ACS #117](https://github.com/SerendipityOneInc/agent-channel-service/pull/117).

- Create a real runnable Agent; Build upgrades that same Agent through source Revisions. No Pack/archive build pipeline or separate builder Agent.
- Reuse the full normal chat UI and ACS/Engine message, history and attachment transport. Build has a dedicated session; normal task threads use the latest settings on their next user turn.
- Commit/apply source changes automatically. Remove Preview/Activate/My Team publication from this feature. Agent-scoped navigation includes tasks, Build, artifacts, schedules and connected channels.
- Support source-file and skill editing, avatar authoring, share-link installation into an independent editable copy, and fast bulk 14-day activity/conversation statistics.
- Retire global marketplace/legacy Builder navigation and legacy project creation; retain existing project editing through Agents → Legacy agent projects.

## Review and fixes

Three independent agents reviewed Web, business/backend and Engine/ACS. Findings were adjudicated against current source and approved product decisions before repair:

- Bind authoring turns to exact runtime configuration including latest channel/MCP credentials; retries and committed tool receipts keep their original snapshot.
- Add durable quota reservations under the existing short shared install lock, same-key single execution and failed-runtime cleanup; enforce normal plan model permissions for creation, share installation and source commits.
- Initialize personal MCP through the existing install path; validate initial source and secret prefixes; prevent normalized skill-name collisions without renaming existing bindings.
- Fetch current full Revisions by immutable ID. Load source-free history summaries only when opened, eliminating repeated full-history source polling.
- Isolate share preview caches per capability/open without putting bearer tokens in query keys. Reset creation idempotency when the requested input changes.
- Preserve Engine skill context in shared chat and restore scheduled-result navigation to the existing result reader.
- Surface dependency rebuild conflicts explicitly: saved but not applied, no implicit interruption of running tasks.

## Test plan

- [x] Integrated changed frontend regression selection: 52 files, 788 passed / 69 skipped / 1 todo.
- [x] Integrated changed backend selection: 381 tests passed.
- [x] Focused runtime client/apply tests: 80 passed.
- [x] Final integrated changed-surface gates: frontend guards, typecheck, ESLint; backend ruff, format, pyright and all 8 import contracts.
- [x] Design and implementation documents consolidated from 2,069 to about 560 lines, with only current decisions and explicit acceptance boundaries.
- [x] Previous full ECAP CI passed on `8c878a2a4`: Web 728 files / 9,694 passed (70 skipped, 1 todo); backend 10,625 passed (5 skipped), coverage 89.52% against the unchanged 89.50% requirement. Web build, all applicable quality/type/lint jobs, CodeQL and required aggregate checks passed.
- [ ] Coordinated feature/staging acceptance and required human approval remain outstanding; no live rollout performed in this review pass.

## Latest follow-up verification (2026-09-09)

- Pushed follow-up commit `3c3879042`: preserve channel-owned read-only history and bindings, hide edit history outside Build, and handle successful HTTP 204 deletion without attempting JSON decoding. The user approved the existing `size-override` mechanism for all three companion PRs; the label is applied, all normal pre-push type/static checks passed, and the commit is now on the PR.
- Local regression selection passed: Web 41 files / 309 tests, backend 31 tests, shared chat UI 8 tests. Changed-surface type/static checks and the complete commit hooks passed.
- This pass also verified a real local Feishu inbound message through the intended Agent run and successful ACS outbound delivery. This is a scoped channel smoke test, not full feature acceptance or a staging rollout.
- Engine and ACS code CI passed on their then-current heads. Claude produced no valid review verdict; per user direction this execution failure is excluded from code-defect assessment, not relabeled as a successful review or bypassed in repository protections.
- The first full size-overridden ECAP CI exposed unused legacy-create source, an outdated staff-only assertion for the two machine-authenticated authoring routes, and backend coverage of 89.40% against the unchanged 89.50% gate. Follow-up commit `8c878a2a4` removes only unused legacy-create source/exports, retains existing project editing/recovery, explicitly asserts each internal route's proper auth boundary, and adds HTTP/tool-dispatch/source-diff/dependency-materialization regression tests. No authentication implementation or coverage threshold was changed.
- Follow-up local verification: 41 Web test files / 498 passing tests, an additional legacy-entry selection of 4 files / 61 passing tests, backend auth/boundary selection 94 passing tests, focused coverage selection 92 passing tests, knip, full commit hooks and changed-surface static gates all passed. Selections overlap and are not summed as unique tests.
- Previous full CI passed on `8c878a2a4`: [Code Quality Check](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34319336886). This is baseline evidence; the configuration-simplification follow-up below has its own CI run. Skipped path-filtered jobs and the oversized automated Codex review are not counted as executed tests or review approval. Required human approval remains outstanding.

## Deployment / rollback

Engine additive schema/runtime must precede ACS's runtime_mode reads; then deploy ACS and ECAP backend/Web. The feature follows existing V2 eligibility without a separate switch, so its prerequisites must be ready before the ECAP deployment. Current migration files already published on staging must remain immutable; this ECAP PR only adds business fields/collections in MongoDB and does not change Engine migration contents or execute migrations. Coordinate the worker and ECAP gateway update: both now derive authentication from the existing Engine service secret with the same purpose string; mixed old/new derivations reject Build callbacks until the pair matches. No dedicated token setting is required. Application rollback retains the additive Engine schema and restores matching gateway authentication on both sides.

## Deliberate boundaries / remaining decisions

- Ready for review; no merge/deploy authorization. This is the entire feature, not only the most recent UI diff; its size exceeds the normal budget. The user approved a one-PR `size-override` exception on 2026-09-09; no global size threshold or code-quality gate was changed.
- The approved `size-override` now allows full quality/build jobs to run; it does not bypass those checks. Automated Codex review skipped the oversized diff and is not counted as a completed code review. The repository already had Claude review disabled; a stale `cc:request-changes` label from a confirmed initialization failure with no verdict was removed, and the existing aggregate gate re-evaluated successfully. No repository variable, check status or human approval was overridden.
- Dependency changes on an already locked task sandbox require an explicit rebuild decision because interruption is possible. The safe refusal/error path is implemented; a confirmation/rebuild UI is not claimed as implemented.
- Unknown failed creation/cleanup retains its quota reservation. Retrying the same operation key can recover; losing that key in an uncertain failure still requires operator recovery. No cross-key alias registry or additional recovery state machine was introduced.
- Business state stays in ECAP. Engine owns runs/configuration, and a registered product integration retains the synchronous authoring gateway without a generic plugin framework or new reconciliation worker.

## Design and implementation

- `docs/superpowers/specs/2026-09-04-self-evolving-agent-development-design.md`
- `docs/superpowers/plans/2026-09-04-self-evolving-agent-development-implementation.md`

No Linear issue was created, as requested.


## Size exception

The user explicitly approved `size-override` on all three companion PRs on 2026-09-09. The existing label has been applied to this PR only; no repository-wide limit, test requirement or review protection was changed.

## Configuration simplification (2026-09-09)

User-approved follow-up `158b4d793` removes `AGENT_DEVELOPMENT_ENABLED` and `AGENT_AUTHORING_GATEWAY_SERVICE_TOKEN` from application settings, examples and deployment overlays. Agent Development reuses existing V2 eligibility, V1-only exceptions, ownership and quota enforcement.

ECAP derives the lowercase hex HMAC-SHA256 bearer over `zooclaw:agent-authoring:v1` from `ZOOCLAW_ENGINE_SERVICE_TOKEN`; worker [Engine #1297](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1297) derives the same value from its matching `CONTROLD_SERVICE_TOKEN`. Every environment uses this path. Missing/wrong/raw service bearers, retired staging-purpose bearers and stale keys are rejected; there is no anonymous bypass or additional service.

Verification: 109 focused backend tests passed, including both authenticated callback routes, shared ASCII/UTF-8 vectors, V2 eligibility, creation, deployment wiring, source ownership and turn pinning. Full backend static gates, commit hooks and pre-push frontend/backend checks passed. Full CI passed on `158b4d793`: [Code Quality Check](https://github.com/SerendipityOneInc/ecap-workspace/actions/runs/34321054050). Backend: 10,649 passed, 5 skipped; coverage 89.52% against the unchanged 89.50% requirement. Web tests/build, applicable static checks, CodeQL and required aggregate checks passed. ECAP's oversized automated Codex review remains skipped, not a review approval. No live rollout or migration was performed. Historical staging evidence is explicitly marked as predating this change.


---

## fix(billing): classify compute usage across billing dashboards (#3672)

- **SHA**: `bfb00080ab042cd4e06b86628e4473f89a898e7b`
- **作者**: sam-srp
- **日期**: 2026-09-09T06:33:26Z
- **PR**: #3672

### Commit Message

```
fix(billing): classify compute usage across billing dashboards (#3672)

Sandbox compute events have a `usage_type` but no model, so the usage
dashboards group their credits under `Unknown`. Classify
`usage_type=sandbox_compute` when reading Lago events and display
**Compute / 运行环境计算** in the main app and enterprise admin, including
chart tooltips. Existing events benefit without rewriting or
republishing billing data.

Update headings, empty states, and summaries to include models and
services. Show event counts as **usage records / 计费记录数**, since a
compute event represents a completed execution segment. Preserve the
existing API fields, credit calculation, event counts, time buckets,
model display-name fallback, and genuinely unknown usage. Fix the main
app's summary fallback so decimal amounts no longer discard Chinese
translations.

## Validation
- Backend usage aggregation: 7 tests passed, including mixed
compute/tool/unknown/zero-cost model events across two buckets with
exact amounts and counts.
- Main app usage component: 8 tests passed, using real English/Chinese
catalogs and preserving unknown entries alongside compute.
- Enterprise usage components and view model: 40 tests passed, including
localized tooltips, server-provided names, and legacy identifier
fallback.
- Backend: Ruff, Pyright, and all 8 import-layer contracts passed.
- Both frontend apps: TypeScript and focused ESLint checks passed; main
app governance guards passed.
- `git diff --check` passed. Live account billing reconciliation and
browser smoke testing were not run.

## Rollout
Deploy `claw-interface`, `web/app`, and `web/enterprise-admin` for the
full display update. No Engine or billing-gateway deployment, billing
migration, or charge replay is required.

---------

Co-authored-by: kaka-srp <kaka@srp.one>
```

### PR Body

Sandbox compute events have a `usage_type` but no model, so the usage dashboards group their credits under `Unknown`. Classify `usage_type=sandbox_compute` when reading Lago events and display **Compute / 运行环境计算** in the main app and enterprise admin, including chart tooltips. Existing events benefit without rewriting or republishing billing data.

Update headings, empty states, and summaries to include models and services. Show event counts as **usage records / 计费记录数**, since a compute event represents a completed execution segment. Preserve the existing API fields, credit calculation, event counts, time buckets, model display-name fallback, and genuinely unknown usage. Fix the main app's summary fallback so decimal amounts no longer discard Chinese translations.

## Validation
- Backend usage aggregation: 7 tests passed, including mixed compute/tool/unknown/zero-cost model events across two buckets with exact amounts and counts.
- Main app usage component: 8 tests passed, using real English/Chinese catalogs and preserving unknown entries alongside compute.
- Enterprise usage components and view model: 40 tests passed, including localized tooltips, server-provided names, and legacy identifier fallback.
- Backend: Ruff, Pyright, and all 8 import-layer contracts passed.
- Both frontend apps: TypeScript and focused ESLint checks passed; main app governance guards passed.
- `git diff --check` passed. Live account billing reconciliation and browser smoke testing were not run.

## Rollout
Deploy `claw-interface`, `web/app`, and `web/enterprise-admin` for the full display update. No Engine or billing-gateway deployment, billing migration, or charge replay is required.


---

## fix(enterprise-admin): refresh shared session identity and await logout (#3674)

- **SHA**: `daba44cf2f81288b7dba2cc9810314c06a91c5ab`
- **作者**: sam-srp
- **日期**: 2026-09-09T06:17:32Z
- **PR**: #3674

### Commit Message

```
fix(enterprise-admin): refresh shared session identity and await logout (#3674)

## Summary
- Refresh Business identity on tab focus/reconnect and on entry to
Vertical Pack checkout instead of retaining an indefinitely fresh
identity after the shared cookie changes.
- Disable HTTP caching for identity fetches and `/api/auth/me`
responses.
- Await successful server-side cookie deletion before clearing client
queries or navigating to login; show a localized error if logout fails.
- Preserve the existing shared cookie name/domain, legacy token
compatibility, and backend purchase authorization.

## Root cause
Business shares a session cookie with the main site, but its identity
query used `staleTime: Infinity`. A cookie change outside the tab could
therefore leave the purchase page using an old organization. Separately,
logout previously fired cookie deletion without awaiting its result and
navigated immediately, creating a race and hiding failures.

These are verified code-level risks. This PR does not claim that they
conclusively explain the reported customer incident: the failing page's
exact identity was not captured. It does not change customer
organization data or payment services.

## Test plan
- [x] Enterprise Admin suite: 59 files, 438 tests passed
(`NODE_OPTIONS=--no-experimental-webstorage pnpm exec vitest run
--config vitest.config.mts`; option avoids local Node 25 Web
Storage/jsdom interference).
- [x] TypeScript: `pnpm exec tsc --noEmit`.
- [x] ESLint on all changed TypeScript files; `git diff --check`.
- [x] Regression coverage: Personal-to-Team and Team-to-Personal focus
refresh, pending/failed logout, navigation ordering, and no-store
identity responses.
- [ ] Live multi-tab main-site/Business verification after deployment
(not performed; no production changes).
```

### PR Body

## Summary
- Refresh Business identity on tab focus/reconnect and on entry to Vertical Pack checkout instead of retaining an indefinitely fresh identity after the shared cookie changes.
- Disable HTTP caching for identity fetches and `/api/auth/me` responses.
- Await successful server-side cookie deletion before clearing client queries or navigating to login; show a localized error if logout fails.
- Preserve the existing shared cookie name/domain, legacy token compatibility, and backend purchase authorization.

## Root cause
Business shares a session cookie with the main site, but its identity query used `staleTime: Infinity`. A cookie change outside the tab could therefore leave the purchase page using an old organization. Separately, logout previously fired cookie deletion without awaiting its result and navigated immediately, creating a race and hiding failures.

These are verified code-level risks. This PR does not claim that they conclusively explain the reported customer incident: the failing page's exact identity was not captured. It does not change customer organization data or payment services.

## Test plan
- [x] Enterprise Admin suite: 59 files, 438 tests passed (`NODE_OPTIONS=--no-experimental-webstorage pnpm exec vitest run --config vitest.config.mts`; option avoids local Node 25 Web Storage/jsdom interference).
- [x] TypeScript: `pnpm exec tsc --noEmit`.
- [x] ESLint on all changed TypeScript files; `git diff --check`.
- [x] Regression coverage: Personal-to-Team and Team-to-Personal focus refresh, pending/failed logout, navigation ordering, and no-store identity responses.
- [ ] Live multi-tab main-site/Business verification after deployment (not performed; no production changes).


---

## fix(acp): stabilize Desktop MCP-over-ACP sessions (#3669)

- **SHA**: `f8d4e4abc6a61772090d17c2abe0814dcd43c573`
- **作者**: zayne-srp
- **日期**: 2026-09-09T03:21:56Z
- **PR**: #3669

### Commit Message

```
fix(acp): stabilize Desktop MCP-over-ACP sessions (#3669)

## Summary
- keep Desktop MCP-over-ACP tool names, public routes, and credentials
stable when DSH rotates its temporary ACP `serverId`
- route each stable Engine MCP server to the currently connected Desktop
peer while rejecting duplicate declarations and preserving conflicting
personal MCP configuration
- convert oversized local MCP responses into bounded JSON-RPC errors
without disconnecting ACP, including mixed response/notification batches
- end MCP SSE streams cleanly after bridge teardown
- disable the legacy FastClaw Desktop node auto-connect and renderer IPC
surface while retaining Desktop working-directory controls

## Root cause
The Engine persisted MCP catalogs by Agent configuration version, but
Claw Interface previously generated the Engine server name and
credential from a random bridge ID on every prompt. A resumed Engine
session could therefore call an old tool name after its temporary route
had been removed, producing `Invalid MCP bridge credential`. Separately,
the Desktop relay treated every response above the 1 MiB transport limit
as fatal, so one large local tool result terminated the whole ACP
connection.

The legacy FastClaw Desktop node connector was also started
unconditionally even though the available Desktop Agent targets now use
Mattermost or DSH. This caused continuous
`/openclaw/settings/desktop-pair` retries and duplicated the local tool
path already provided by MCP-over-ACP.

## Test plan
- [x] Desktop TypeScript typecheck
- [x] Desktop tests: 46 passed; 1 opt-in Codex integration test skipped
- [x] Claw Interface ACP/MCP tests: 58 passed
- [x] Ruff, formatting, Pyright, import-linter, changed-surface gate,
and diff checks
- [x] Telepresence staging smoke test: reused one V2 Engine session
across Claw Interface and Desktop restarts; `mcp__acp-dsh-tools__read`
kept the same name and route and completed without 401 or credential
errors
- [x] oversized MCP replay: bounded error returned, mixed-batch
notification preserved, and the following request succeeded on the same
ACP connection
- [x] installed Desktop smoke test: Remote V2 DSH connected and
completed a local MCP file read; no `desktop-pair` request appeared
after the former retry interval

No new environment variable is required. Stable route credentials are
domain-separated HMAC values derived from the existing `SECRET_KEY`.
```

### PR Body

## Summary
- keep Desktop MCP-over-ACP tool names, public routes, and credentials stable when DSH rotates its temporary ACP `serverId`
- route each stable Engine MCP server to the currently connected Desktop peer while rejecting duplicate declarations and preserving conflicting personal MCP configuration
- convert oversized local MCP responses into bounded JSON-RPC errors without disconnecting ACP, including mixed response/notification batches
- end MCP SSE streams cleanly after bridge teardown
- disable the legacy FastClaw Desktop node auto-connect and renderer IPC surface while retaining Desktop working-directory controls

## Root cause
The Engine persisted MCP catalogs by Agent configuration version, but Claw Interface previously generated the Engine server name and credential from a random bridge ID on every prompt. A resumed Engine session could therefore call an old tool name after its temporary route had been removed, producing `Invalid MCP bridge credential`. Separately, the Desktop relay treated every response above the 1 MiB transport limit as fatal, so one large local tool result terminated the whole ACP connection.

The legacy FastClaw Desktop node connector was also started unconditionally even though the available Desktop Agent targets now use Mattermost or DSH. This caused continuous `/openclaw/settings/desktop-pair` retries and duplicated the local tool path already provided by MCP-over-ACP.

## Test plan
- [x] Desktop TypeScript typecheck
- [x] Desktop tests: 46 passed; 1 opt-in Codex integration test skipped
- [x] Claw Interface ACP/MCP tests: 58 passed
- [x] Ruff, formatting, Pyright, import-linter, changed-surface gate, and diff checks
- [x] Telepresence staging smoke test: reused one V2 Engine session across Claw Interface and Desktop restarts; `mcp__acp-dsh-tools__read` kept the same name and route and completed without 401 or credential errors
- [x] oversized MCP replay: bounded error returned, mixed-batch notification preserved, and the following request succeeded on the same ACP connection
- [x] installed Desktop smoke test: Remote V2 DSH connected and completed a local MCP file read; no `desktop-pair` request appeared after the former retry interval

No new environment variable is required. Stable route credentials are domain-separated HMAC values derived from the existing `SECRET_KEY`.


---
