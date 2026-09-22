# SerendipityOneInc/ecap-workspace — commits 2026-09-21

## feat(platform): refine organization and project settings (#3847)

- **SHA**: `dd71e532ac698d23126941ddbc020f179290582b`
- **作者**: finn-srp
- **日期**: 2026-09-21T13:27:30Z
- **PR**: #3847

### Commit Message

```
feat(platform): refine organization and project settings (#3847)

## Linear

N/A

## Summary

- unify personal profile and Organization settings behind one settings
entry while keeping Clerk profile management visible
- add Organization People and Projects preview flows without enabling
invitation or Project membership mutations
- keep Project management inside the main Project shell, with Settings
in the sidebar and General, Members, and Limits tabs in the page
- simplify the Projects list to a single Manage action and preserve the
selected Project across settings navigation

## Test plan

- [x] `fnm exec --using=24 pnpm --dir web/platform lint`
- [x] `fnm exec --using=24 pnpm --dir web/platform typecheck`
- [x] `fnm exec --using=24 pnpm --dir web/platform test`
- [x] `fnm exec --using=24 pnpm --dir web/platform build`
- [x] `cd web/app && fnm exec --using=24 pnpm test:unit`
- [x] Manually verified the Projects → Manage → Project Settings →
Members flow with the local app, real Clerk session, Organization, and
Project data
```

### PR Body

## Linear

N/A

## Summary

- unify personal profile and Organization settings behind one settings entry while keeping Clerk profile management visible
- add Organization People and Projects preview flows without enabling invitation or Project membership mutations
- keep Project management inside the main Project shell, with Settings in the sidebar and General, Members, and Limits tabs in the page
- simplify the Projects list to a single Manage action and preserve the selected Project across settings navigation

## Test plan

- [x] `fnm exec --using=24 pnpm --dir web/platform lint`
- [x] `fnm exec --using=24 pnpm --dir web/platform typecheck`
- [x] `fnm exec --using=24 pnpm --dir web/platform test`
- [x] `fnm exec --using=24 pnpm --dir web/platform build`
- [x] `cd web/app && fnm exec --using=24 pnpm test:unit`
- [x] Manually verified the Projects → Manage → Project Settings → Members flow with the local app, real Clerk session, Organization, and Project data


---

## fix(models): guide users without access to billing (#3839)

- **SHA**: `73a53d8d543d258263aba4ea5409e2ae758b7013`
- **作者**: tim-srp
- **日期**: 2026-09-21T09:59:50Z
- **PR**: #3839

### Commit Message

```
fix(models): guide users without access to billing (#3839)

## Problem

The model catalog returns an unhandled 500 when Billing Gateway reports
`no_active_subscription`. Users with confirmed missing access see a raw
server error rather than a useful Billing link.

## Behavior

- Return HTTP 402 with `{code:
"billing.subscription_or_credits_required", detail: ...}` only when
neither effective subscription/grant/team access nor available credits
exists. Frontend branches on the code, suppresses expected-error
retries/reporting, and gates submission and model replacement prompts.
- Both “Unlock models” and “Explore options” open the canonical
`/identity?tab=account-billing` page in a new tab, with no checkout
modal. Keeping the original composer mounted preserves input, pending
files, and model selection in New Task, Agent Builder, and chat.
Returning to the tab refreshes the catalog without auto-submitting.
- Keep shared credit authorization behavior unchanged. Extract only the
existing customer-ID resolution for reuse; model synchronization and
runtime recovery still use the gateway credit check, without any wallet
fallback.
- Handle billing exceptions in a catalog-only adapter. The exact
`400/no_active_subscription` response permits reading the wallet only to
establish an empty/nonpositive balance. Positive settled wallet balance
is not authorization: if the gateway cannot confirm availability, return
retryable `billing.balance_unavailable` (502), not full model access or
purchase guidance. Actual gateway-confirmed positive available credits
retain existing full model access.
- Invalid balances return `billing.invalid_balance` (502). Model catalog
dependency errors retain `models.catalog_unavailable` (503).

## Validation

- Backend: 86 targeted tests passed, including shared authorization
isolation, confirmed available versus settled balance, malformed
wallet/check payloads, subscription/team states, and the 402 route
contract.
- Frontend: 186 targeted tests passed, including English/Chinese new-tab
destinations through the canonical locale-free app route, submission
gating, return-to-tab access refresh, New Task composer, and Agent
Builder dialogs.
- Backend static checks passed: ruff, format, pyright, import contracts.
- Frontend TypeScript passed; ESLint formatting correction applied and
verified.

## Deployment and limits

Requires both claw-interface and web deployment. Deploy web before or
alongside the backend for the new guidance. No live
billing/configuration data changed.

Gateway-independent top-up spending is not implemented here: the current
gateway still requires an active subscription for its authoritative
credit check. Settled wallet balance alone cannot safely establish
spendability. This change preserves that boundary and reports
uncertainty as a retryable error.

## Review adjudication

Fixed the malformed-wallet-response finding with shape validation and
regression tests. The follow-up review identified a broader
authorization effect from placing fallback in the shared helper; moved
diagnostics to the catalog-only adapter and pinned the original shared
behavior. Fixed navigation-related draft loss by opening Billing in a
new tab rather than unmounting draft-owning surfaces.

PAST_DUE remains effective under the current-access resolver.
MANUAL_REVIEW remains unresolved and is not presented as a confirmed
need to purchase again. Tests retain both cases.

Follow-up validation exercises the real billing client methods against
malformed HTTP responses, covering JSON decode failures and client-side
non-mapping errors. The catalog maps these to `billing.invalid_balance`
(502), without changing the shared client. CI-exposed Agent Builder and
chat test regressions were fixed by reusing `LocaleLink` inside the
billing notice; 148 tests across the affected suites and composer passed
locally.
```

### PR Body

## Problem

The model catalog returns an unhandled 500 when Billing Gateway reports `no_active_subscription`. Users with confirmed missing access see a raw server error rather than a useful Billing link.

## Behavior

- Return HTTP 402 with `{code: "billing.subscription_or_credits_required", detail: ...}` only when neither effective subscription/grant/team access nor available credits exists. Frontend branches on the code, suppresses expected-error retries/reporting, and gates submission and model replacement prompts.
- Both “Unlock models” and “Explore options” open the canonical `/identity?tab=account-billing` page in a new tab, with no checkout modal. Keeping the original composer mounted preserves input, pending files, and model selection in New Task, Agent Builder, and chat. Returning to the tab refreshes the catalog without auto-submitting.
- Keep shared credit authorization behavior unchanged. Extract only the existing customer-ID resolution for reuse; model synchronization and runtime recovery still use the gateway credit check, without any wallet fallback.
- Handle billing exceptions in a catalog-only adapter. The exact `400/no_active_subscription` response permits reading the wallet only to establish an empty/nonpositive balance. Positive settled wallet balance is not authorization: if the gateway cannot confirm availability, return retryable `billing.balance_unavailable` (502), not full model access or purchase guidance. Actual gateway-confirmed positive available credits retain existing full model access.
- Invalid balances return `billing.invalid_balance` (502). Model catalog dependency errors retain `models.catalog_unavailable` (503).

## Validation

- Backend: 86 targeted tests passed, including shared authorization isolation, confirmed available versus settled balance, malformed wallet/check payloads, subscription/team states, and the 402 route contract.
- Frontend: 186 targeted tests passed, including English/Chinese new-tab destinations through the canonical locale-free app route, submission gating, return-to-tab access refresh, New Task composer, and Agent Builder dialogs.
- Backend static checks passed: ruff, format, pyright, import contracts.
- Frontend TypeScript passed; ESLint formatting correction applied and verified.

## Deployment and limits

Requires both claw-interface and web deployment. Deploy web before or alongside the backend for the new guidance. No live billing/configuration data changed.

Gateway-independent top-up spending is not implemented here: the current gateway still requires an active subscription for its authoritative credit check. Settled wallet balance alone cannot safely establish spendability. This change preserves that boundary and reports uncertainty as a retryable error.

## Review adjudication

Fixed the malformed-wallet-response finding with shape validation and regression tests. The follow-up review identified a broader authorization effect from placing fallback in the shared helper; moved diagnostics to the catalog-only adapter and pinned the original shared behavior. Fixed navigation-related draft loss by opening Billing in a new tab rather than unmounting draft-owning surfaces.

PAST_DUE remains effective under the current-access resolver. MANUAL_REVIEW remains unresolved and is not presented as a confirmed need to purchase again. Tests retain both cases.

Follow-up validation exercises the real billing client methods against malformed HTTP responses, covering JSON decode failures and client-side non-mapping errors. The catalog maps these to `billing.invalid_balance` (502), without changing the shared client. CI-exposed Agent Builder and chat test regressions were fixed by reusing `LocaleLink` inside the billing notice; 148 tests across the affected suites and composer passed locally.


---

## feat(platform): add project API key authentication (#3838)

- **SHA**: `4de3138bcfa30f8fb94fdcf24e059774a7ad345d`
- **作者**: finn-srp
- **日期**: 2026-09-21T08:24:44Z
- **PR**: #3838

### Commit Message

```
feat(platform): add project API key authentication (#3838)

## Problem and behavior

Platform can create and revoke Project API keys, but `claw-interface`
could not authenticate those keys as a machine identity. Sending them
directly into the existing Engine proxy would also reuse Work ownership
assumptions before the Platform-to-Engine boundary has been designed.

This PR adds Project-scoped API key authentication in `claw-interface`.
A valid key resolves to `organization_id`, `project_id`, and
`api_key_id`. Platform principals are then stopped at the Interface
boundary with `503 platform.engine_access_not_ready`, so no Engine
request is made.

## Changes

- centralize Platform secret generation, validation, and SHA-256 hashing
- resolve active keys through Project and active Organization records
- update `last_used_at` asynchronously with a 60-second throttle
- add explicit `legacy`, `platform`, and `disabled` service API
authentication modes with no fallback; `legacy` remains the default
- cover invalid, revoked, incomplete, disabled, and unavailable-storage
cases without leaking which relationship failed
- keep every Platform `/service/v1` resource path closed before Engine
dispatch
- consolidate Platform identity, data ownership, API contracts, and
release boundaries into one spec
- record
[zooclaw-engine#1573](https://github.com/SerendipityOneInc/zooclaw-engine/issues/1573)
as the SDK/runtime dependency while leaving the Engine contract in the
Engine repository
- rename the Interface runbook to `platform-operations.md` and remove
stale phase-based guidance from docs and UI

No `zooclaw-engine` code or schema is changed. This PR does not enable
Platform SDK runtime access or change deployed authentication mode.

## Validation

- 55 targeted Platform authentication, repository, proxy, bootstrap, and
schema tests passed
- Platform frontend: lint, typecheck, 27 tests, and production build
passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`
```

### PR Body

## Problem and behavior

Platform can create and revoke Project API keys, but `claw-interface` could not authenticate those keys as a machine identity. Sending them directly into the existing Engine proxy would also reuse Work ownership assumptions before the Platform-to-Engine boundary has been designed.

This PR adds Project-scoped API key authentication in `claw-interface`. A valid key resolves to `organization_id`, `project_id`, and `api_key_id`. Platform principals are then stopped at the Interface boundary with `503 platform.engine_access_not_ready`, so no Engine request is made.

## Changes

- centralize Platform secret generation, validation, and SHA-256 hashing
- resolve active keys through Project and active Organization records
- update `last_used_at` asynchronously with a 60-second throttle
- add explicit `legacy`, `platform`, and `disabled` service API authentication modes with no fallback; `legacy` remains the default
- cover invalid, revoked, incomplete, disabled, and unavailable-storage cases without leaking which relationship failed
- keep every Platform `/service/v1` resource path closed before Engine dispatch
- consolidate Platform identity, data ownership, API contracts, and release boundaries into one spec
- record [zooclaw-engine#1573](https://github.com/SerendipityOneInc/zooclaw-engine/issues/1573) as the SDK/runtime dependency while leaving the Engine contract in the Engine repository
- rename the Interface runbook to `platform-operations.md` and remove stale phase-based guidance from docs and UI

No `zooclaw-engine` code or schema is changed. This PR does not enable Platform SDK runtime access or change deployed authentication mode.

## Validation

- 55 targeted Platform authentication, repository, proxy, bootstrap, and schema tests passed
- Platform frontend: lint, typecheck, 27 tests, and production build passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`


---

## feat(mcp): require confirmation for Feishu approval writes (#3801)

- **SHA**: `697b685ee43e88817728fdc391678b5b6907f176`
- **作者**: sharplee-srp
- **日期**: 2026-09-21T07:36:54Z
- **PR**: #3801

### Commit Message

```
feat(mcp): require confirmation for Feishu approval writes (#3801)

## Behavior

Official staging/production Feishu approval MCP endpoints use a fixed
policy: `approval_list_cc`, `approval_list_pending`,
`approval_list_done` and `approval_get` execute automatically;
`approval_comment` and `approval_decide` require confirmation for every
invocation. Other MCP endpoints retain existing behavior.

Both Agent Settings saves and personal MCP sync use `server_for()`. The
six-tool policy is declared before catalog discovery; tool
enable/disable remains supported. User permission overrides/reset
settings are absent, and catalog metadata or historical per-tool choices
cannot override the fixed policy.

The two writes now include `requireConfirmation: true`. Depends on
[Engine
#1565](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1565):
its existing approval chain enforces the per-call requirement despite
ordinary allow rules, permission sugar and prior session grants; only
allow-once/deny are valid. Companion channel confirmation behavior is
[ACS
#139](https://github.com/SerendipityOneInc/agent-channel-service/pull/139).

## Rollout

Deploy Engine worker first, controld second, then ECAP. This release
covers new Agents and existing Agents at their next successful Settings
save or MCP create/edit/enable/disable/test synchronization, plus the
existing pending/error reconciliation paths. Connections already at
`sync_status=ok` are not automatically queued: **deployment alone does
not immediately protect all existing Agents**. No fleet backfill or
live-data mutation is included. New snapshots do not rewrite
already-pinned turns.

## Validation

- 21 targeted ECAP tests and the backend static gate passed; CI passed.
Engine companion tests cover rendered configuration, parser/evaluator
precedence, prior grants and repeated confirmation.
- Earlier real Feishu validation was superseded by run
`approval-short-final-20260920134833`, documented in [ACS
#139](https://github.com/SerendipityOneInc/agent-channel-service/pull/139):
ACS `c3c6016`, Engine `8bceb74f`, ECAP materialization `0598e030a`, MCP
`9d75157`. Five automatic real-model/Feishu API scenarios passed. Manual
confirmation then cancellation wrote exactly one comment, left the
cancelled comment absent, completed both turns, and
delivered/acknowledged each approval prompt and resolution receipt once.
- The earlier cancellation-follow-up failure is superseded for that
isolated local lane: no automatic retry or new approval occurred; the
user accepted wording that requires an explicit new request to retry.
Internal tool-name display was shortened. This real-channel result
covers Engine `8bceb74f`; the latest Engine head is covered by the
supplemental tests below.
- That Feishu lane exported ECAP materialization rather than exercising
the complete UI save/sync path. It is not a deployed-staging/production
verdict.

## Stored URL canonicalization follow-up

At `d8f8c2bd5`, `fixed_tool_permissions()` now normalizes URLs with the
existing `HttpUrl` adapter before policy matching. This directly
addresses the Codex dot-segment finding even for raw persisted records
that did not pass through today's write boundary. Literal/encoded dot
segments normalize, then the actual MCP router's single percent-decoding
rule applies. Persisted URLs are not rewritten; only the two official
Feishu approval hosts receive fixed rules. Invalid HTTP URLs return no
fixed policy.

- **10 new raw-record cases failed before the fix**; **90 related tests
pass after the fix and rebase**, including both official hosts,
runtime/public agreement and negative cases for encoded separators,
double encoding and traversal to another endpoint.
- Claude's cross-repository evidence request is addressed in the
checked-in spec's **Router contract evidence** section: actual MCP
package `9d751573`, isolated Go handler, exact HTTP results, no external
API writes. It is not a deployed-ingress verdict.
- This supersedes the earlier decision to leave the classification
boundary unchanged. Both review labels are left to the new automated
review; they will not be removed manually. CI passed at this head:
11,880 backend tests passed (5 skipped), coverage 89.69%; lint/typecheck
passed. Both Codex and Claude now report APPROVE / no new findings.
Claude reassessed the completed CI evidence in [its updated
review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3801#issuecomment-5755280388);
both need-human-review labels were removed by the review workflow. No
labels were manually removed in this follow-up.
- No full local model/channel E2E rerun: the change is confined to
endpoint classification. Existing rollout limits and earlier E2E commit
pins below still apply.

## Percent-encoded approval path fix — 2026-09-21 UTC

Follow-up boundary audit found that the actual approval MCP router
accepts percent-encoded equivalents of `/mcp`, while ECAP previously
compared the raw path. At `0b337257a`, the fixed-policy classifier
decodes the path exactly once before comparison. The policy still
applies only to the official Feishu approval endpoints; other MCP
endpoints and ordinary approval/session-grant behavior are unchanged.

- Regression reproduced before the fix: **12 failed, 27 passed**. After
the fix and rebase: **77 tests passed** across fixed permissions,
resource runtime, MCP sync and MCP service.
- Both official hosts are covered through
`McpConnectionWrite`/`HttpUrl`, runtime policy, public metadata and
sync. Encoded equivalents (`/%6dcp`, `/%6Dcp`, `/m%63p`, `/mc%70`,
`/%6d%63%70`) retain the mandatory confirmation policy; double encoding,
encoded separators, extra segments, NUL and malformed escapes do not
broaden the match.
- A local `httptest` probe against the actual approval MCP package at
`9d751573` confirmed HTTP 200 and both write-tool definitions for all
five equivalent paths, and HTTP 404 for the tested non-equivalent paths.
This used a dummy API key and `tools/list` only, with no Feishu API
calls or writes; it is handler-level evidence, not a deployed ingress
verdict.
- Repository-venv Ruff, formatting, Pyright and import contracts passed.
CI passed on `0b337257a`, including backend tests/lint/typecheck,
duplication and CodeQL. Review adjudication is recorded below; green
review jobs are not being represented as finding-free reviews.
- Review adjudication at this head: Codex raised dot-segment
canonicalization. The cited `/mcp/.` and `/mcp/%2e` inputs normalize to
`/mcp/` in the actual `McpConnectionWrite` boundary; `/x/../mcp` and
`/x/%2e%2e/mcp` normalize to `/mcp`. All four retain both fixed
`always_ask` rules in a direct boundary/classifier probe.
`mcp_service.py` persists `str(resource.server_url)` on create/update,
so the claimed user-input bypass was not reproduced. Additionally, the
actual MCP handler returns 404 for `/mcp/`; this review did not
establish an executable bypass. This earlier decision is superseded by
the stored-URL canonicalization follow-up above.
- Claude reported no blocking code findings and requested evidence of
router decoding and rollout scope. The actual-package handler probe
above supplies the former; the documented no-backfill rollout remains
unchanged. An empty fixed-policy result is **not** fail-closed: ordinary
permissions would apply, which is why the encoded-path mismatch was
fixed.
- No new full model/channel local E2E was run. The focused
classifier/sync regressions and real-handler probe cover this change;
prior E2E remains valid only for its recorded heads and scope. Full
browser/auth/Mongo and deployed channel acceptance remain separate
follow-ups.

## Terminal-dot hostname review fix — 2026-09-21 UTC

Addresses [kaka's hostname canonicalization
finding](https://github.com/SerendipityOneInc/ecap-workspace/pull/3801#issuecomment-5754928556).
`fixed_tool_permissions()` removes one terminal DNS root dot before
matching the official hostname. HTTPS, exact official-host allowlist,
default/443 port and `/mcp` path checks remain in place; persisted URLs
and other MCP permissions are unchanged. This protects both existing
stored dotted URLs and newly validated input without a data rewrite.

- Regression confirmed before the fix: five failing cases (both official
hosts, upper/lowercase variants through `McpConnectionWrite`/`HttpUrl`,
and personal MCP sync).
- After the fix: **59 tests passed** across fixed permissions, resource
runtime, MCP sync and MCP service. Tests also reject lookalike domains
with a terminal dot, HTTP, nonstandard ports and other paths; runtime
policy and public permission metadata agree.
- Repository-venv Ruff check/format, Pyright and import contracts
passed, as did pre-commit checks. Initial global-Ruff and test-typing
setup failures were corrected; no unrelated files changed.
- CI on `124c33ac9` passed, including backend tests/lint/typecheck,
duplication and CodeQL. Both Codex and Claude reviews reported no
findings.
- The earlier local E2E below remains evidence for its explicitly pinned
heads, not a rerun at this follow-up commit. This classifier-only fix is
covered by reproducing boundary/sync regressions; no new full local
model/channel E2E was run. Deployment/UI acceptance limits below remain
unchanged.

## Latest supplemental validation — 2026-09-21 UTC

Frozen heads: ECAP `0598e030a`, ACS `c3c6016`, Engine `b829ca478`. Fresh
isolated A102 rootless run `approval-compat-20260921023553`; no product
source changes or production/staging data mutations.

- **Six runtime scenarios passed** using real controld HTTP, PostgreSQL,
Redis, Temporal, worker and an authorized real model, with a local
synthetic non-Feishu MCP write-count fixture:
  - Ordinary automatic tool: no approval prompt, exactly one execution.
- Ordinary `allow-always`: first call approved; the next turn in the
same session executes once without another prompt.
- Duplicate `allow-once` confirmations: exactly one execution and one
resolution event.
  - Duplicate denials: zero executions and one resolution event.
- Required confirmation: an `allow-always` batch containing another
valid event returns HTTP 400 with no partial event delivery; a later
valid `allow-once` still completes.
- **ECAP → real Engine service integration passed**: actual
`runtime_bindings()` plus `EngineClient` config-version
creation/activation and readback; personal MCP sync restores the fixed
policy on a disposable Agent; unrelated MCP configuration and direct
exposure remain intact. Ownership/catalog repositories are isolated
fixtures and Mongo access is explicitly prohibited. This is not full
browser/auth/Mongo Settings transaction E2E.
- **Engine: 276 tests passed in four targeted files** (`approvals`,
`sessions-api`, `agents-service`, `tool-hooks`), including Temporal
grant carryover, denial/timeout and resolver validation.
- **ACS: 194 tests passed in four targeted files**
(`channel-approval-event`, `chat-command-service`,
`inbound-runtime-service`, `receiver-input-worker`). Test-tool caveat:
used Vitest **4.1.10**, mounted read-only from the isolated Engine tools
volume, rather than ACS-declared 4.1.11, after npm 10.9.8 failed
installing test tools with `edgesOut` before any tests ran. ACS product
dependency manifests/lock and pinned runtime dependencies were
unchanged.

Verdicts: environment valid for this isolated scope with the test-tool
caveat above; workflow completion PASS; deterministic QA PASS; API/tool
execution acceptance PASS. No regression observed in the tested
non-Feishu automatic execution or ordinary session grants. This round
did not send real channel messages or establish a
deployed-staging/production verdict.

All task-owned containers are stopped; evidence and volumes retained
privately. No workers, tmux sessions or sidebar workspaces were created.

**Further testing:** another identical local E2E round is not needed
while these heads and configuration remain unchanged. Full
browser/auth/Mongo save-transaction coverage remains unverified; use a
dedicated safe profile or staging canary, then validate the newly
deployed channel chain. Re-run affected scenarios if relevant
code/configuration changes. These remaining checks are not implied by
the local PASS above.
```

### PR Body

## Behavior

Official staging/production Feishu approval MCP endpoints use a fixed policy: `approval_list_cc`, `approval_list_pending`, `approval_list_done` and `approval_get` execute automatically; `approval_comment` and `approval_decide` require confirmation for every invocation. Other MCP endpoints retain existing behavior.

Both Agent Settings saves and personal MCP sync use `server_for()`. The six-tool policy is declared before catalog discovery; tool enable/disable remains supported. User permission overrides/reset settings are absent, and catalog metadata or historical per-tool choices cannot override the fixed policy.

The two writes now include `requireConfirmation: true`. Depends on [Engine #1565](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1565): its existing approval chain enforces the per-call requirement despite ordinary allow rules, permission sugar and prior session grants; only allow-once/deny are valid. Companion channel confirmation behavior is [ACS #139](https://github.com/SerendipityOneInc/agent-channel-service/pull/139).

## Rollout

Deploy Engine worker first, controld second, then ECAP. This release covers new Agents and existing Agents at their next successful Settings save or MCP create/edit/enable/disable/test synchronization, plus the existing pending/error reconciliation paths. Connections already at `sync_status=ok` are not automatically queued: **deployment alone does not immediately protect all existing Agents**. No fleet backfill or live-data mutation is included. New snapshots do not rewrite already-pinned turns.

## Validation

- 21 targeted ECAP tests and the backend static gate passed; CI passed. Engine companion tests cover rendered configuration, parser/evaluator precedence, prior grants and repeated confirmation.
- Earlier real Feishu validation was superseded by run `approval-short-final-20260920134833`, documented in [ACS #139](https://github.com/SerendipityOneInc/agent-channel-service/pull/139): ACS `c3c6016`, Engine `8bceb74f`, ECAP materialization `0598e030a`, MCP `9d75157`. Five automatic real-model/Feishu API scenarios passed. Manual confirmation then cancellation wrote exactly one comment, left the cancelled comment absent, completed both turns, and delivered/acknowledged each approval prompt and resolution receipt once.
- The earlier cancellation-follow-up failure is superseded for that isolated local lane: no automatic retry or new approval occurred; the user accepted wording that requires an explicit new request to retry. Internal tool-name display was shortened. This real-channel result covers Engine `8bceb74f`; the latest Engine head is covered by the supplemental tests below.
- That Feishu lane exported ECAP materialization rather than exercising the complete UI save/sync path. It is not a deployed-staging/production verdict.

## Stored URL canonicalization follow-up

At `d8f8c2bd5`, `fixed_tool_permissions()` now normalizes URLs with the existing `HttpUrl` adapter before policy matching. This directly addresses the Codex dot-segment finding even for raw persisted records that did not pass through today's write boundary. Literal/encoded dot segments normalize, then the actual MCP router's single percent-decoding rule applies. Persisted URLs are not rewritten; only the two official Feishu approval hosts receive fixed rules. Invalid HTTP URLs return no fixed policy.

- **10 new raw-record cases failed before the fix**; **90 related tests pass after the fix and rebase**, including both official hosts, runtime/public agreement and negative cases for encoded separators, double encoding and traversal to another endpoint.
- Claude's cross-repository evidence request is addressed in the checked-in spec's **Router contract evidence** section: actual MCP package `9d751573`, isolated Go handler, exact HTTP results, no external API writes. It is not a deployed-ingress verdict.
- This supersedes the earlier decision to leave the classification boundary unchanged. Both review labels are left to the new automated review; they will not be removed manually. CI passed at this head: 11,880 backend tests passed (5 skipped), coverage 89.69%; lint/typecheck passed. Both Codex and Claude now report APPROVE / no new findings. Claude reassessed the completed CI evidence in [its updated review](https://github.com/SerendipityOneInc/ecap-workspace/pull/3801#issuecomment-5755280388); both need-human-review labels were removed by the review workflow. No labels were manually removed in this follow-up.
- No full local model/channel E2E rerun: the change is confined to endpoint classification. Existing rollout limits and earlier E2E commit pins below still apply.

## Percent-encoded approval path fix — 2026-09-21 UTC

Follow-up boundary audit found that the actual approval MCP router accepts percent-encoded equivalents of `/mcp`, while ECAP previously compared the raw path. At `0b337257a`, the fixed-policy classifier decodes the path exactly once before comparison. The policy still applies only to the official Feishu approval endpoints; other MCP endpoints and ordinary approval/session-grant behavior are unchanged.

- Regression reproduced before the fix: **12 failed, 27 passed**. After the fix and rebase: **77 tests passed** across fixed permissions, resource runtime, MCP sync and MCP service.
- Both official hosts are covered through `McpConnectionWrite`/`HttpUrl`, runtime policy, public metadata and sync. Encoded equivalents (`/%6dcp`, `/%6Dcp`, `/m%63p`, `/mc%70`, `/%6d%63%70`) retain the mandatory confirmation policy; double encoding, encoded separators, extra segments, NUL and malformed escapes do not broaden the match.
- A local `httptest` probe against the actual approval MCP package at `9d751573` confirmed HTTP 200 and both write-tool definitions for all five equivalent paths, and HTTP 404 for the tested non-equivalent paths. This used a dummy API key and `tools/list` only, with no Feishu API calls or writes; it is handler-level evidence, not a deployed ingress verdict.
- Repository-venv Ruff, formatting, Pyright and import contracts passed. CI passed on `0b337257a`, including backend tests/lint/typecheck, duplication and CodeQL. Review adjudication is recorded below; green review jobs are not being represented as finding-free reviews.
- Review adjudication at this head: Codex raised dot-segment canonicalization. The cited `/mcp/.` and `/mcp/%2e` inputs normalize to `/mcp/` in the actual `McpConnectionWrite` boundary; `/x/../mcp` and `/x/%2e%2e/mcp` normalize to `/mcp`. All four retain both fixed `always_ask` rules in a direct boundary/classifier probe. `mcp_service.py` persists `str(resource.server_url)` on create/update, so the claimed user-input bypass was not reproduced. Additionally, the actual MCP handler returns 404 for `/mcp/`; this review did not establish an executable bypass. This earlier decision is superseded by the stored-URL canonicalization follow-up above.
- Claude reported no blocking code findings and requested evidence of router decoding and rollout scope. The actual-package handler probe above supplies the former; the documented no-backfill rollout remains unchanged. An empty fixed-policy result is **not** fail-closed: ordinary permissions would apply, which is why the encoded-path mismatch was fixed.
- No new full model/channel local E2E was run. The focused classifier/sync regressions and real-handler probe cover this change; prior E2E remains valid only for its recorded heads and scope. Full browser/auth/Mongo and deployed channel acceptance remain separate follow-ups.

## Terminal-dot hostname review fix — 2026-09-21 UTC

Addresses [kaka's hostname canonicalization finding](https://github.com/SerendipityOneInc/ecap-workspace/pull/3801#issuecomment-5754928556). `fixed_tool_permissions()` removes one terminal DNS root dot before matching the official hostname. HTTPS, exact official-host allowlist, default/443 port and `/mcp` path checks remain in place; persisted URLs and other MCP permissions are unchanged. This protects both existing stored dotted URLs and newly validated input without a data rewrite.

- Regression confirmed before the fix: five failing cases (both official hosts, upper/lowercase variants through `McpConnectionWrite`/`HttpUrl`, and personal MCP sync).
- After the fix: **59 tests passed** across fixed permissions, resource runtime, MCP sync and MCP service. Tests also reject lookalike domains with a terminal dot, HTTP, nonstandard ports and other paths; runtime policy and public permission metadata agree.
- Repository-venv Ruff check/format, Pyright and import contracts passed, as did pre-commit checks. Initial global-Ruff and test-typing setup failures were corrected; no unrelated files changed.
- CI on `124c33ac9` passed, including backend tests/lint/typecheck, duplication and CodeQL. Both Codex and Claude reviews reported no findings.
- The earlier local E2E below remains evidence for its explicitly pinned heads, not a rerun at this follow-up commit. This classifier-only fix is covered by reproducing boundary/sync regressions; no new full local model/channel E2E was run. Deployment/UI acceptance limits below remain unchanged.

## Latest supplemental validation — 2026-09-21 UTC

Frozen heads: ECAP `0598e030a`, ACS `c3c6016`, Engine `b829ca478`. Fresh isolated A102 rootless run `approval-compat-20260921023553`; no product source changes or production/staging data mutations.

- **Six runtime scenarios passed** using real controld HTTP, PostgreSQL, Redis, Temporal, worker and an authorized real model, with a local synthetic non-Feishu MCP write-count fixture:
  - Ordinary automatic tool: no approval prompt, exactly one execution.
  - Ordinary `allow-always`: first call approved; the next turn in the same session executes once without another prompt.
  - Duplicate `allow-once` confirmations: exactly one execution and one resolution event.
  - Duplicate denials: zero executions and one resolution event.
  - Required confirmation: an `allow-always` batch containing another valid event returns HTTP 400 with no partial event delivery; a later valid `allow-once` still completes.
- **ECAP → real Engine service integration passed**: actual `runtime_bindings()` plus `EngineClient` config-version creation/activation and readback; personal MCP sync restores the fixed policy on a disposable Agent; unrelated MCP configuration and direct exposure remain intact. Ownership/catalog repositories are isolated fixtures and Mongo access is explicitly prohibited. This is not full browser/auth/Mongo Settings transaction E2E.
- **Engine: 276 tests passed in four targeted files** (`approvals`, `sessions-api`, `agents-service`, `tool-hooks`), including Temporal grant carryover, denial/timeout and resolver validation.
- **ACS: 194 tests passed in four targeted files** (`channel-approval-event`, `chat-command-service`, `inbound-runtime-service`, `receiver-input-worker`). Test-tool caveat: used Vitest **4.1.10**, mounted read-only from the isolated Engine tools volume, rather than ACS-declared 4.1.11, after npm 10.9.8 failed installing test tools with `edgesOut` before any tests ran. ACS product dependency manifests/lock and pinned runtime dependencies were unchanged.

Verdicts: environment valid for this isolated scope with the test-tool caveat above; workflow completion PASS; deterministic QA PASS; API/tool execution acceptance PASS. No regression observed in the tested non-Feishu automatic execution or ordinary session grants. This round did not send real channel messages or establish a deployed-staging/production verdict.

All task-owned containers are stopped; evidence and volumes retained privately. No workers, tmux sessions or sidebar workspaces were created.

**Further testing:** another identical local E2E round is not needed while these heads and configuration remain unchanged. Full browser/auth/Mongo save-transaction coverage remains unverified; use a dedicated safe profile or staging canary, then validate the newly deployed channel chain. Re-run affected scenarios if relevant code/configuration changes. These remaining checks are not implied by the local PASS above.


---

## feat(agents): make build guidance clear and support necessary onboarding (#3837)

- **SHA**: `725b54e3423992cc3d46bde1a18b603573cf8eff`
- **作者**: kaka-srp
- **日期**: 2026-09-21T06:58:48Z
- **PR**: #3837

### Commit Message

```
feat(agents): make build guidance clear and support necessary onboarding (#3837)

## Summary

- 为 Agent Build 提供按需读取的可信 Product Action：页面入口、执行路径、前置条件及完成标志，区分账号资源连接与当前
Agent 绑定。
- 支持 Build 根据实际功能声明必要的一次性
onboarding；复用已有实例资料，只补必要缺口，不把可选偏好或每次任务输入变成初始化门槛。
- 补齐 onboarding 源码校验、创建/修订应用及提交重试恢复；不重启已完成的 onboarding。
- 提供中文设计说明和本地真实模型行为评测。评审读取完整可见交互，源码使用生产校验器；移除强制分阶段返回等过严断言，避免测试驱动行为过拟合。

## Scope and rollout

- 配套 Engine
PR：https://github.com/SerendipityOneInc/zooclaw-engine/pull/1580 。
- Engine 的 onboarding lifecycle endpoint 必须先部署，再部署本 PR 的
claw-interface；完整 Build 指导需要两边一起生效。
- 无前端页面改动、无数据库迁移、不批量改写存量 Agent；不恢复旧 Agent Pack 的多阶段审批流程。
- 未部署线上，未执行生产数据变更。

## Test plan

- [x] 定向后端回归：174 项通过（onboarding / authoring / service / source artifacts
/ Product Action / Engine client / eval harness）。
- [x] CI 首轮发现两处历史摘要测试 fixture 漏排除新增可选字段；已修正并补充显式声明/清除摘要回归，相关 34
项测试通过，未修改生产摘要行为。
- [x] Ruff、格式、Pyright、import-linter 和提交 hooks 通过。
- [x] 本地真实模型评测：20 个行为场景及 1 个新增已有资料复用场景通过；执行模型 `gpt-5.6-terra`，评审模型
`claude-sonnet-5`，指定的 Council Skill 使用真实内容。
- [x] 人工检查新增 onboarding 产物：先读当前实例配置，只补问必需缺项，不把实例值硬编码到共享 Skill。
- [ ] 部署后的跨服务及真实渠道端到端验收（本 PR 未执行）。

评测边界：LLM 调用是真实的，源码校验复用生产实现；authoring 应用/外部资源/渠道仍为本地测试替身。评测不是线上 Build
流程，不给用户增加评审步骤，也不构成线上交付成功证明。
```

### PR Body

## Summary

- 为 Agent Build 提供按需读取的可信 Product Action：页面入口、执行路径、前置条件及完成标志，区分账号资源连接与当前 Agent 绑定。
- 支持 Build 根据实际功能声明必要的一次性 onboarding；复用已有实例资料，只补必要缺口，不把可选偏好或每次任务输入变成初始化门槛。
- 补齐 onboarding 源码校验、创建/修订应用及提交重试恢复；不重启已完成的 onboarding。
- 提供中文设计说明和本地真实模型行为评测。评审读取完整可见交互，源码使用生产校验器；移除强制分阶段返回等过严断言，避免测试驱动行为过拟合。

## Scope and rollout

- 配套 Engine PR：https://github.com/SerendipityOneInc/zooclaw-engine/pull/1580 。
- Engine 的 onboarding lifecycle endpoint 必须先部署，再部署本 PR 的 claw-interface；完整 Build 指导需要两边一起生效。
- 无前端页面改动、无数据库迁移、不批量改写存量 Agent；不恢复旧 Agent Pack 的多阶段审批流程。
- 未部署线上，未执行生产数据变更。

## Test plan

- [x] 定向后端回归：174 项通过（onboarding / authoring / service / source artifacts / Product Action / Engine client / eval harness）。
- [x] CI 首轮发现两处历史摘要测试 fixture 漏排除新增可选字段；已修正并补充显式声明/清除摘要回归，相关 34 项测试通过，未修改生产摘要行为。
- [x] Ruff、格式、Pyright、import-linter 和提交 hooks 通过。
- [x] 本地真实模型评测：20 个行为场景及 1 个新增已有资料复用场景通过；执行模型 `gpt-5.6-terra`，评审模型 `claude-sonnet-5`，指定的 Council Skill 使用真实内容。
- [x] 人工检查新增 onboarding 产物：先读当前实例配置，只补问必需缺项，不把实例值硬编码到共享 Skill。
- [ ] 部署后的跨服务及真实渠道端到端验收（本 PR 未执行）。

评测边界：LLM 调用是真实的，源码校验复用生产实现；authoring 应用/外部资源/渠道仍为本地测试替身。评测不是线上 Build 流程，不给用户增加评审步骤，也不构成线上交付成功证明。


---

## fix(billing): remove credit expiration promises from UI copy (#3836)

- **SHA**: `9901b22e4609fb1fac17bd8880426389d86b22a6`
- **作者**: sam-srp
- **日期**: 2026-09-21T06:31:49Z
- **PR**: #3836

### Commit Message

```
fix(billing): remove credit expiration promises from UI copy (#3836)

Remove credit-expiration promises from billing UI copy. Account cards
now only explain that top-up credits can be used without a subscription,
across all 10 supported locales. Remove the no-expiration bullet and
translation keys from the purchase success page, and remove the
equivalent claim in the older Stripe purchase component.

Clean up the contradictory one-year validity and expired-credit
restoration wording in About Credits. Monthly subscription credit reset
wording remains. Wallet expiration, credit grants, and all payment
behavior are unchanged.

Validation: existing billing card, Stripe purchase and purchase-success
tests; TypeScript, ESLint and repository frontend checks. Not deployed.
```

### PR Body

Remove credit-expiration promises from billing UI copy. Account cards now only explain that top-up credits can be used without a subscription, across all 10 supported locales. Remove the no-expiration bullet and translation keys from the purchase success page, and remove the equivalent claim in the older Stripe purchase component.

Clean up the contradictory one-year validity and expired-credit restoration wording in About Credits. Monthly subscription credit reset wording remains. Wallet expiration, credit grants, and all payment behavior are unchanged.

Validation: existing billing card, Stripe purchase and purchase-success tests; TypeScript, ESLint and repository frontend checks. Not deployed.


---

## fix(billing): show Add Credits for all eligible personal users (#3835)

- **SHA**: `bb0c9cc85fa3177cb6ec5b02daa4f2e59300cefb`
- **作者**: sam-srp
- **日期**: 2026-09-21T05:58:25Z
- **PR**: #3835

### Commit Message

```
fix(billing): show Add Credits for all eligible personal users (#3835)

Personal accounts whose subscriptions expired only saw Activate and
could not find Add Credits, despite top-ups being available without a
subscription. Render Add Credits independently of subscription display
status, using the existing personal-billing eligibility check. Team
users keep their current Manage-only actions, and loading/error states
remain guarded.

Validation: 36 SharedPlanCard component tests pass, covering personal
subscription states, Team restrictions, and unresolved billing
eligibility. No backend, configuration, or payment-processing changes.
Not deployed.
```

### PR Body

Personal accounts whose subscriptions expired only saw Activate and could not find Add Credits, despite top-ups being available without a subscription. Render Add Credits independently of subscription display status, using the existing personal-billing eligibility check. Team users keep their current Manage-only actions, and loading/error states remain guarded.

Validation: 36 SharedPlanCard component tests pass, covering personal subscription states, Team restrictions, and unresolved billing eligibility. No backend, configuration, or payment-processing changes. Not deployed.


---

## fix(billing): unblock subscriptions with legacy pending orders (#3832)

- **SHA**: `8cbcad1ffdc766cf9c359da73cbcd3c516c03090`
- **作者**: sam-srp
- **日期**: 2026-09-21T05:04:00Z
- **PR**: #3832

### Commit Message

```
fix(billing): unblock subscriptions with legacy pending orders (#3832)

## Problem and change
Users with unfinished Antom, Airwallex, or Creem subscription orders
cannot purchase the current Stripe Pro plan, even after their previous
subscription has ended. Ignore pending orders from these retired
providers when checking purchase eligibility. Keep active-subscription
and created/manual-review protections.

Stripe pending orders retain the existing provider checks: expired
Checkout sessions do not block, open current-plan sessions can be
resumed, and completed or uncertain sessions must be resolved before
another purchase. Keep the original checkout lease lifecycle; this PR
does not release the lease early or allow multiple payable Stripe
sessions.

Historical orders are not deleted or rewritten. No environment variables
or data migration are required.

## Validation
- 159 focused tests passed; 5 existing retired-trial tests skipped.
- Regression tests cover the catalog guard and new Stripe checkout with
pending Antom/Airwallex/Creem orders, plus retained Stripe
open/completed/expired session handling and timeout recovery.
- Backend Ruff, formatting, Pyright and import-contract checks.

Not deployed; no production data modified by this PR.
```

### PR Body

## Problem and change
Users with unfinished Antom, Airwallex, or Creem subscription orders cannot purchase the current Stripe Pro plan, even after their previous subscription has ended. Ignore pending orders from these retired providers when checking purchase eligibility. Keep active-subscription and created/manual-review protections.

Stripe pending orders retain the existing provider checks: expired Checkout sessions do not block, open current-plan sessions can be resumed, and completed or uncertain sessions must be resolved before another purchase. Keep the original checkout lease lifecycle; this PR does not release the lease early or allow multiple payable Stripe sessions.

Historical orders are not deleted or rewritten. No environment variables or data migration are required.

## Validation
- 159 focused tests passed; 5 existing retired-trial tests skipped.
- Regression tests cover the catalog guard and new Stripe checkout with pending Antom/Airwallex/Creem orders, plus retained Stripe open/completed/expired session handling and timeout recovery.
- Backend Ruff, formatting, Pyright and import-contract checks.

Not deployed; no production data modified by this PR.


---

## fix(platform): preserve selected project after refresh (#3825)

- **SHA**: `df48d5a71a571187c9389cbe6508289a2f96bc2b`
- **作者**: finn-srp
- **日期**: 2026-09-21T04:19:38Z
- **PR**: #3825

### Commit Message

```
fix(platform): preserve selected project after refresh (#3825)

## Summary

- preserve the active Project across a full page refresh
- scope the saved selection by Clerk user and active Organization
- add an Organization-scoped GET /platform/v1/projects/{project_id}
endpoint
- restore a saved Project directly by ID instead of scanning paginated
lists
- fall back to Default Project when the saved Project returns 404
- keep cursor pagination dedicated to Project selector browsing
- add regression coverage for reload, direct retrieval, stale
selections, and cross-Organization isolation

Closes #3823.

## Root cause

The active Project existed only in React component state. A full page
refresh rebuilt the provider with no selected Project, so it always fell
back to the bootstrap Default Project. The first fix persisted the ID
but had to scan every Project page because the backend did not expose a
single-Project read endpoint.

## API addition

GET /platform/v1/projects/{project_id} reads one Project using both the
requested Project ID and the current Clerk Organization scope. Missing
and cross-Organization Projects return the same 404 contract.

## Test plan

- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit/component tests (18 passed)
- [x] Platform production build
- [x] claw-interface ruff, format, pyright, and import-linter
- [x] Platform route unit tests (5 passed)
- [x] Real MongoDB Platform repository/lifecycle tests (6 passed)
```

### PR Body

## Summary

- preserve the active Project across a full page refresh
- scope the saved selection by Clerk user and active Organization
- add an Organization-scoped GET /platform/v1/projects/{project_id} endpoint
- restore a saved Project directly by ID instead of scanning paginated lists
- fall back to Default Project when the saved Project returns 404
- keep cursor pagination dedicated to Project selector browsing
- add regression coverage for reload, direct retrieval, stale selections, and cross-Organization isolation

Closes #3823.

## Root cause

The active Project existed only in React component state. A full page refresh rebuilt the provider with no selected Project, so it always fell back to the bootstrap Default Project. The first fix persisted the ID but had to scan every Project page because the backend did not expose a single-Project read endpoint.

## API addition

GET /platform/v1/projects/{project_id} reads one Project using both the requested Project ID and the current Clerk Organization scope. Missing and cross-Organization Projects return the same 404 contract.

## Test plan

- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit/component tests (18 passed)
- [x] Platform production build
- [x] claw-interface ruff, format, pyright, and import-linter
- [x] Platform route unit tests (5 passed)
- [x] Real MongoDB Platform repository/lifecycle tests (6 passed)


---

## fix(billing): remove unused Airwallex pricing and report payment failures (#3831)

- **SHA**: `112fcc76ce03ba9e0db253d8979db2ce6f8dac81`
- **作者**: sam-srp
- **日期**: 2026-09-21T03:56:26Z
- **PR**: #3831

### Commit Message

```
fix(billing): remove unused Airwallex pricing and report payment failures (#3831)

## Summary
New purchases are Stripe-only, but the backend still required unused
Airwallex USD30 settings. Payment failures also had gaps in explicit
Sentry reporting, especially catalog/checkout requests and caught
reconciliation or refund failures.

- Remove the two Airwallex USD30 settings and unused provider-price
lookup/checkout validator; restore the original historical price
mappings and update their regression tests.
- Report frontend catalog, order, checkout, portal, subscription
management, and invoice failures with operation, UID and available
order/session/provider identifiers.
- Enable allowlisted backend payment Sentry events for webhook
processing, credit fulfillment, subscription operations, reconciliation,
and refund retries. Retain existing confirmation monitoring.
- Strip arbitrary provider payloads/credentials; deduplicate nested
backend exceptions and repeated frontend incidents. Monitoring failures
preserve the original payment results, errors, and retries. Reuse
existing Sentry DSNs without adding environment variables.

Historical Airwallex USD20 first payments, renewals, trial settlement,
and scheduled-downgrade cancellation remain supported. Payment and
subscription business rules are unchanged.

## Validation
- Airwallex cleanup regression suite: 686 unique cases passing after
updating the obsolete fixture.
- Payment monitoring and billing regressions: 219 distinct backend cases
passed across focused suites, including the final 34-case monitor/refund
rerun. Five existing cases skipped.
- Frontend focused suite: 69 passed, including
catalog/order/checkout/navigation failure reporting and unchanged retry
behavior.
- Backend ruff, formatting, pyright and import contracts passed;
frontend governance guards, TypeScript and targeted ESLint passed.
- No deployment or live Sentry delivery verification performed.
```

### PR Body

## Summary
New purchases are Stripe-only, but the backend still required unused Airwallex USD30 settings. Payment failures also had gaps in explicit Sentry reporting, especially catalog/checkout requests and caught reconciliation or refund failures.

- Remove the two Airwallex USD30 settings and unused provider-price lookup/checkout validator; restore the original historical price mappings and update their regression tests.
- Report frontend catalog, order, checkout, portal, subscription management, and invoice failures with operation, UID and available order/session/provider identifiers.
- Enable allowlisted backend payment Sentry events for webhook processing, credit fulfillment, subscription operations, reconciliation, and refund retries. Retain existing confirmation monitoring.
- Strip arbitrary provider payloads/credentials; deduplicate nested backend exceptions and repeated frontend incidents. Monitoring failures preserve the original payment results, errors, and retries. Reuse existing Sentry DSNs without adding environment variables.

Historical Airwallex USD20 first payments, renewals, trial settlement, and scheduled-downgrade cancellation remain supported. Payment and subscription business rules are unchanged.

## Validation
- Airwallex cleanup regression suite: 686 unique cases passing after updating the obsolete fixture.
- Payment monitoring and billing regressions: 219 distinct backend cases passed across focused suites, including the final 34-case monitor/refund rerun. Five existing cases skipped.
- Frontend focused suite: 69 passed, including catalog/order/checkout/navigation failure reporting and unchanged retry behavior.
- Backend ruff, formatting, pyright and import contracts passed; frontend governance guards, TypeScript and targeted ESLint passed.
- No deployment or live Sentry delivery verification performed.


---

## feat(platform): separate project and organization settings (#3830)

- **SHA**: `162a9e988d68c8466b9955a3343104c7fedd743e`
- **作者**: finn-srp
- **日期**: 2026-09-21T03:54:57Z
- **PR**: #3830

### Commit Message

```
feat(platform): separate project and organization settings (#3830)

## Summary

Platform settings now separate Project-scoped navigation from
Organization settings. The account menu opens a dedicated settings shell
with General and Organization pages, while Members and Billing remain
visible but disabled until their product models are implemented.

The main sidebar reserves the Organization credit balance position
without presenting a fake value. Usage stays Project-scoped, and the
legacy Billing route redirects to the Organization Billing route.

## Validation

- `pnpm test` — 20 tests passed
- `pnpm typecheck`
- `pnpm lint`
- `pnpm build`
- visually checked the local Organization settings layout
```

### PR Body

## Summary

Platform settings now separate Project-scoped navigation from Organization settings. The account menu opens a dedicated settings shell with General and Organization pages, while Members and Billing remain visible but disabled until their product models are implemented.

The main sidebar reserves the Organization credit balance position without presenting a fake value. Usage stays Project-scoped, and the legacy Billing route redirects to the Organization Billing route.

## Validation

- `pnpm test` — 20 tests passed
- `pnpm typecheck`
- `pnpm lint`
- `pnpm build`
- visually checked the local Organization settings layout


---

## fix(landing): improve responsive layout and unify signup menus (#3820)

- **SHA**: `ce681320f669b509145d63593600c847e0279efa`
- **作者**: shana-srp
- **日期**: 2026-09-21T03:38:51Z
- **PR**: #3820

### Commit Message

```
fix(landing): improve responsive layout and unify signup menus (#3820)

## Summary
- Fix homepage headline/CTA overlap with a fluid hero grid, wrapping
copy, and mobile spacing. Increase mobile touch targets and keep
agent-card content readable at iPhone widths.
- Replace the restaurant-agent screenshot/overlay with the supplied
**2087 × 1398 PNG**, copied byte-for-byte without AI reconstruction,
resizing, or lossy re-encoding. Limit the displayed image to **1043 CSS
px** and its centered canvas to 1252 px, so the source covers desktop 2×
density. Refresh the loading placeholder and all 10 locale alt texts.
- Reuse the same signup dropdown and **Managed Agent API** label for
header, hero, and footer. Preserve distinct source context:
`header_sign_up`, `landing_hero`, and `marketing_cta`.

## Root cause
Fixed hero grid widths, non-wrapping copy, and positional offsets
allowed the headline to overlap the adjacent actions. Mobile agent cards
relied on independent absolute text positions. The footer bypassed the
shared menu.

The mobile rotating title now reserves the tallest role in the current
language using an invisible, accessibility-hidden CSS grid layer. All
translated roles fit without fixed line limits or height changes during
rotation. Desktop indicator bars retain their original 26 px bottom
offset while their button hit areas remain 44 px tall.

## Test plan
- [x] Frontend governance guards, TypeScript type-check, ESLint,
formatting, and `git diff --check`.
- [x] Homepage, header, and login-page unit tests: **78 passed**;
verifies separate CTA source context and accessible active headings
across 10 locales.
- [x] Spanish and Italian at **320, 375, and 430 px**; every role
measured within its container, no horizontal page overflow. At 375 px
all six role transitions retain a stable 112 px title height.
- [x] Desktop checks at **1024, 1440, and 1920 px**: image loads at its
original 2087 × 1398 dimensions, displayed width never exceeds 1043 px,
source covers 2× rendering, indicator visual bottom is 26 px, and touch
targets remain 44 px tall.
- [x] All three menus open/close with the keyboard and produce the
expected distinct source parameters; shared menu labels and interaction
remain consistent.
- [x] Original implementation also checked across 16 Chromium/WebKit
responsive configurations, including iPhone layouts.

Frontend-only change. The final asset is the original supplied
screenshot; no higher-resolution source or AI-enhanced output is
claimed. Retaining a wider-than-1043 px image at 2× density would
require a larger native export.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
- Fix homepage headline/CTA overlap with a fluid hero grid, wrapping copy, and mobile spacing. Increase mobile touch targets and keep agent-card content readable at iPhone widths.
- Replace the restaurant-agent screenshot/overlay with the supplied **2087 × 1398 PNG**, copied byte-for-byte without AI reconstruction, resizing, or lossy re-encoding. Limit the displayed image to **1043 CSS px** and its centered canvas to 1252 px, so the source covers desktop 2× density. Refresh the loading placeholder and all 10 locale alt texts.
- Reuse the same signup dropdown and **Managed Agent API** label for header, hero, and footer. Preserve distinct source context: `header_sign_up`, `landing_hero`, and `marketing_cta`.

## Root cause
Fixed hero grid widths, non-wrapping copy, and positional offsets allowed the headline to overlap the adjacent actions. Mobile agent cards relied on independent absolute text positions. The footer bypassed the shared menu.

The mobile rotating title now reserves the tallest role in the current language using an invisible, accessibility-hidden CSS grid layer. All translated roles fit without fixed line limits or height changes during rotation. Desktop indicator bars retain their original 26 px bottom offset while their button hit areas remain 44 px tall.

## Test plan
- [x] Frontend governance guards, TypeScript type-check, ESLint, formatting, and `git diff --check`.
- [x] Homepage, header, and login-page unit tests: **78 passed**; verifies separate CTA source context and accessible active headings across 10 locales.
- [x] Spanish and Italian at **320, 375, and 430 px**; every role measured within its container, no horizontal page overflow. At 375 px all six role transitions retain a stable 112 px title height.
- [x] Desktop checks at **1024, 1440, and 1920 px**: image loads at its original 2087 × 1398 dimensions, displayed width never exceeds 1043 px, source covers 2× rendering, indicator visual bottom is 26 px, and touch targets remain 44 px tall.
- [x] All three menus open/close with the keyboard and produce the expected distinct source parameters; shared menu labels and interaction remain consistent.
- [x] Original implementation also checked across 16 Chromium/WebKit responsive configurations, including iPhone layouts.

Frontend-only change. The final asset is the original supplied screenshot; no higher-resolution source or AI-enhanced output is claimed. Retaining a wider-than-1043 px image at 2× density would require a larger native export.


---

## test(e2e): stabilize chat, settings, schedule, and accessibility coverage (#3827)

- **SHA**: `468a3f9c1490e6398ebcdff0469148a57ef4d88f`
- **作者**: rayhuang198212
- **日期**: 2026-09-21T02:40:14Z
- **PR**: #3827

### Commit Message

```
test(e2e): stabilize chat, settings, schedule, and accessibility coverage (#3827)

## Summary

Stabilize the ECAP Playwright E2E suite against the current staging UI
and chat routing behavior.

This PR updates page objects and affected specs only; it does not change
product behavior.

## Changes

- Resolve the active main Agent workspace before opening the `/home`
chat launcher.
- Improve assistant response extraction using the dedicated response
body locator.
- Support native audio elements when detecting generated audio.
- Update Settings and Profile navigation locators to use accessible
navigation and link roles.
- Update the Schedule status filter assertion for the current select
implementation.
- Strengthen keyboard accessibility coverage:
  - require the user menu to open and close with Escape;
  - use stable chat input and side-navigation locators;
  - remove conditional assertions that could silently skip coverage.

## Validation

Validated the affected E2E flows against staging, including:

- Basic Usage
- Tool scenarios
- Chat lifecycle and session features
- Settings
- Schedule / Cron
- Profile
- Keyboard Accessibility

## Scope

- E2E tests and page objects only
- No production application behavior changes
```

### PR Body

## Summary

Stabilize the ECAP Playwright E2E suite against the current staging UI and chat routing behavior.

This PR updates page objects and affected specs only; it does not change product behavior.

## Changes

- Resolve the active main Agent workspace before opening the `/home` chat launcher.
- Improve assistant response extraction using the dedicated response body locator.
- Support native audio elements when detecting generated audio.
- Update Settings and Profile navigation locators to use accessible navigation and link roles.
- Update the Schedule status filter assertion for the current select implementation.
- Strengthen keyboard accessibility coverage:
  - require the user menu to open and close with Escape;
  - use stable chat input and side-navigation locators;
  - remove conditional assertions that could silently skip coverage.

## Validation

Validated the affected E2E flows against staging, including:

- Basic Usage
- Tool scenarios
- Chat lifecycle and session features
- Settings
- Schedule / Cron
- Profile
- Keyboard Accessibility

## Scope

- E2E tests and page objects only
- No production application behavior changes

---

## fix(schedule): translate dispatched / awaiting_approval / unknown engine run statuses (#3829)

- **SHA**: `7069ae4929621f3928feaaf56c4e98d77e418728`
- **作者**: Chris@ZooClaw
- **日期**: 2026-09-21T02:15:30Z
- **PR**: #3829

### Commit Message

```
fix(schedule): translate dispatched / awaiting_approval / unknown engine run statuses (#3829)

## Summary
-
`RunStatusBadge`（`web/app/src/components/agent-schedules/DailyTaskList.tsx`）补上
engine run 行的三个状态映射：`dispatched` →
`schedule.runDispatched`、`awaiting_approval` →
`schedule.runAwaitingApproval`、`unknown` →
`schedule.runUnknown`；`awaiting_approval` 用和 `running` 一样的 info 色调。
- `en.ts` / `zh.ts` 各加三条文案（Dispatched / Awaiting approval / Unknown；已派发
/ 等待审批 / 未知）。其余 8 种语言按 `locales/README.md` 的约定回退英文。

## Root cause
zooclaw-engine
[#1499](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1499) 让
`GET …/schedules/{id}/runs` 的每个关联行都带显式 `status`（turn 未结束时是 `dispatched`
/ `running` / `awaiting_approval`，无法归因时是 `unknown`，结束后是 schedule 自己的
verdict）。claw-interface 的 `engine_run_entry_to_model` 直接透传字符串（schema 是
`str | None`），前端 badge 只有 `running` 等几个 key
的翻译，新值以原始字符串灰色显示。`dispatched` 是 claw 对无 status 行的既有合成值，此前也一直是原始字符串，一并补上。

## Test plan
- [x] `bash scripts/verify-web.sh` 对三个文件：guards / tsc / vitest（480 文件
6112 例）/ eslint 全过
- [ ] staging 上打开一个正在跑或等审批的 engine schedule 的运行历史，badge 显示"运行中 / 等待审批 /
已派发"而不是原始字符串

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Q5ZYBmHaNT8LvcEazcXv7i

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- `RunStatusBadge`（`web/app/src/components/agent-schedules/DailyTaskList.tsx`）补上 engine run 行的三个状态映射：`dispatched` → `schedule.runDispatched`、`awaiting_approval` → `schedule.runAwaitingApproval`、`unknown` → `schedule.runUnknown`；`awaiting_approval` 用和 `running` 一样的 info 色调。
- `en.ts` / `zh.ts` 各加三条文案（Dispatched / Awaiting approval / Unknown；已派发 / 等待审批 / 未知）。其余 8 种语言按 `locales/README.md` 的约定回退英文。

## Root cause
zooclaw-engine [#1499](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1499) 让 `GET …/schedules/{id}/runs` 的每个关联行都带显式 `status`（turn 未结束时是 `dispatched` / `running` / `awaiting_approval`，无法归因时是 `unknown`，结束后是 schedule 自己的 verdict）。claw-interface 的 `engine_run_entry_to_model` 直接透传字符串（schema 是 `str | None`），前端 badge 只有 `running` 等几个 key 的翻译，新值以原始字符串灰色显示。`dispatched` 是 claw 对无 status 行的既有合成值，此前也一直是原始字符串，一并补上。

## Test plan
- [x] `bash scripts/verify-web.sh` 对三个文件：guards / tsc / vitest（480 文件 6112 例）/ eslint 全过
- [ ] staging 上打开一个正在跑或等审批的 engine schedule 的运行历史，badge 显示"运行中 / 等待审批 / 已派发"而不是原始字符串

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_01Q5ZYBmHaNT8LvcEazcXv7i


---
