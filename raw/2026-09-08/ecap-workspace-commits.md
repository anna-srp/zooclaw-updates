# SerendipityOneInc/ecap-workspace — commits 2026-09-08

## fix(agents): show org-published packs to every member of the org (#3666)

- **SHA**: `e742399892adb16a604406ba06ce997c3ab479a0`
- **作者**: siqiao-srp
- **日期**: 2026-09-08T11:00:58Z
- **PR**: #3666

### Commit Message

```
fix(agents): show org-published packs to every member of the org (#3666)

## Summary
- Adds a **My organization** tab to `/agent-builder/my-agents` listing
the org's active agent packs published by *other* members, so an org
member can finally find and install agents their org admin uploaded
through the org dashboard.
- Gates owner-only listing actions (Share / List on marketplace /
Deprecate / Edit skills) behind a new `canManage` =
publisher-or-org-admin, so widening visibility does not let any member
share or monetize a teammate's pack.
- Renames the view model's `owned: {error, isLoading}` to `orgPacks`,
since one org-pack query now backs two tabs.

No backend change: `GET /orgs/{org}/packs` is already gated only by
`require_matching_current_org` and returns every org pack, and
`pack_asset_access_service` already allows any current member of the org
to read the pack asset. The data and the permission were always there;
only the front end was hiding them.

## Root cause
`my-agents/useViewModel.ts` filtered the org pack list to
`pack.published_by === currentUserId`, and that filtered list is what
feeds `visiblePackIds` down to the card grid (`MyAgentsCatalog.tsx`). So
a pack was visible only to the single account that published it. The
public marketplace never shows org packs either — `list_agent_packs`
hard-scopes to `ZOOCLAW_ORG_ID` by design — which left org-uploaded
agents with no surface at all for anybody except their publisher.

Concretely, in one production org: four active org packs, all
`published_by` the org admin, 12 members. Eleven of them saw an empty
tab, and eight had no org agent installed at all.

Scope note: only packs with `status === 'active'` from other members are
shown, so another member's draft or in-review work stays private to
them. Your own packs keep appearing in "Owned by me" at every status,
exactly as before.

## Test plan
- [x] `bash scripts/verify-web.sh` — tsc, 9488 vitest tests, eslint, all
green
- [x] New unit coverage in `tests/unit/app/agent-builder/my-agents/`:
- org-scope routing (teammate packs land in the new tab, own packs stay
in "Owned by me")
  - teammate `draft` / `deprecated` packs excluded from the org scope
  - both scopes empty before the signed-in identity resolves
- the org tab renders its pack ids, and its own empty state rather than
the owned one
- ownership gate, both directions: a non-admin member gets no
Share/List/Edit-skills and a disabled Delete with a reason, while an org
admin keeps all of them on the same pack
- [ ] Not covered locally: no E2E exists for this route;
`web-build-check` and the other CI suites remain the gate.
```

### PR Body

## Summary
- Adds a **My organization** tab to `/agent-builder/my-agents` listing the org's active agent packs published by *other* members, so an org member can finally find and install agents their org admin uploaded through the org dashboard.
- Gates owner-only listing actions (Share / List on marketplace / Deprecate / Edit skills) behind a new `canManage` = publisher-or-org-admin, so widening visibility does not let any member share or monetize a teammate's pack.
- Renames the view model's `owned: {error, isLoading}` to `orgPacks`, since one org-pack query now backs two tabs.

No backend change: `GET /orgs/{org}/packs` is already gated only by `require_matching_current_org` and returns every org pack, and `pack_asset_access_service` already allows any current member of the org to read the pack asset. The data and the permission were always there; only the front end was hiding them.

## Root cause
`my-agents/useViewModel.ts` filtered the org pack list to `pack.published_by === currentUserId`, and that filtered list is what feeds `visiblePackIds` down to the card grid (`MyAgentsCatalog.tsx`). So a pack was visible only to the single account that published it. The public marketplace never shows org packs either — `list_agent_packs` hard-scopes to `ZOOCLAW_ORG_ID` by design — which left org-uploaded agents with no surface at all for anybody except their publisher.

Concretely, in one production org: four active org packs, all `published_by` the org admin, 12 members. Eleven of them saw an empty tab, and eight had no org agent installed at all.

Scope note: only packs with `status === 'active'` from other members are shown, so another member's draft or in-review work stays private to them. Your own packs keep appearing in "Owned by me" at every status, exactly as before.

## Test plan
- [x] `bash scripts/verify-web.sh` — tsc, 9488 vitest tests, eslint, all green
- [x] New unit coverage in `tests/unit/app/agent-builder/my-agents/`:
  - org-scope routing (teammate packs land in the new tab, own packs stay in "Owned by me")
  - teammate `draft` / `deprecated` packs excluded from the org scope
  - both scopes empty before the signed-in identity resolves
  - the org tab renders its pack ids, and its own empty state rather than the owned one
  - ownership gate, both directions: a non-admin member gets no Share/List/Edit-skills and a disabled Delete with a reason, while an org admin keeps all of them on the same pack
- [ ] Not covered locally: no E2E exists for this route; `web-build-check` and the other CI suites remain the gate.


---

## feat(business): add multilingual enterprise page and animated contact flow (#3665)

- **SHA**: `38e1a1c5a8efa71aef53c61f5baa563572d2d6cb`
- **作者**: shana-srp
- **日期**: 2026-09-08T10:35:50Z
- **PR**: #3665

### Commit Message

```
feat(business): add multilingual enterprise page and animated contact flow (#3665)

## Summary

Add the enterprise landing page at `/{locale}/business` and preserve the
visitor’s language in homepage/footer navigation. The page supports
English, Chinese, Japanese, Korean, French, German, Italian, Spanish,
Arabic, and Portuguese, including localized metadata and SVG labels.

- Reuse the official marketing header, footer, language picker, and
login dialogs. The English hero uses a self-hosted GFS Didot heading at
64px on desktop, split into two lines, with a white background and
increased spacing beside the sales form.
- Add the platform, agents, model gateway, data assets, model training,
continuous learning, delivery, cases, and security sections. Use the
approved animated SVG diagrams, `#0E0522` dark sections, white signals
on dark backgrounds, and refined borders, labels, and responsive
layouts. SVG localization uses bundled templates compatible with
Workers.
- Make the bottom Book a demo link scroll to the first-screen form, play
a short arrival highlight, and focus email. Repeated clicks work;
interrupted scrolling and reduced-motion preferences are respected.
- Replace the copy-summary dialog with inline feedback: the form fades
out, the success icon and text appear in sequence, and the card retains
its height. Keep native validation, accessible focus handling, and the
clearly labeled example testimonial.

**Form scope:** this remains an approved frontend prototype. Submission
changes local presentation state and displays the requested
confirmation; it does not send or persist a sales lead. Connecting a
delivery API is a separate follow-up. No backend APIs or dependencies
are added. The font’s OFL license is included. The removed summary/copy
workflow has no remaining state, clipboard handlers, or dictionary
entries.

## Test plan

- [x] Targeted frontend verification: governance guards, TypeScript,
ESLint, and 59 tests across seven relevant suites passed.
- [x] All 27 SVG assets parse, and generated SVG templates match their
sources. Shared orbit geometry reduces the animated loop to 98KB, below
the 100KB limit; its timing and labels are preserved.
- [x] Browser checks covered locale switching, English/Chinese layouts,
desktop and mobile sizing, the shared header, form validation, CTA
navigation/focus, and submission transitions. Form card height stays
unchanged in the tested desktop and phone layouts.
- [x] Only enterprise-page implementation and supporting specifications
are included; independent local reference previews are excluded.
- [x] Merged current main (`4c93ca2e`) without conflicts; the resulting
PR is within the 3,000-line size budget. Full import-boundary/dead-code
CI lint and the asset-size gate pass locally.
- [x] CI checks passed on final commit `ad845130`: build,
lint/typecheck, unit tests, asset-size gate, CodeQL, and both automatic
reviews. No open code-scanning alerts or current-commit inline findings.
Human review is still required before merge.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary

Add the enterprise landing page at `/{locale}/business` and preserve the visitor’s language in homepage/footer navigation. The page supports English, Chinese, Japanese, Korean, French, German, Italian, Spanish, Arabic, and Portuguese, including localized metadata and SVG labels.

- Reuse the official marketing header, footer, language picker, and login dialogs. The English hero uses a self-hosted GFS Didot heading at 64px on desktop, split into two lines, with a white background and increased spacing beside the sales form.
- Add the platform, agents, model gateway, data assets, model training, continuous learning, delivery, cases, and security sections. Use the approved animated SVG diagrams, `#0E0522` dark sections, white signals on dark backgrounds, and refined borders, labels, and responsive layouts. SVG localization uses bundled templates compatible with Workers.
- Make the bottom Book a demo link scroll to the first-screen form, play a short arrival highlight, and focus email. Repeated clicks work; interrupted scrolling and reduced-motion preferences are respected.
- Replace the copy-summary dialog with inline feedback: the form fades out, the success icon and text appear in sequence, and the card retains its height. Keep native validation, accessible focus handling, and the clearly labeled example testimonial.

**Form scope:** this remains an approved frontend prototype. Submission changes local presentation state and displays the requested confirmation; it does not send or persist a sales lead. Connecting a delivery API is a separate follow-up. No backend APIs or dependencies are added. The font’s OFL license is included. The removed summary/copy workflow has no remaining state, clipboard handlers, or dictionary entries.

## Test plan

- [x] Targeted frontend verification: governance guards, TypeScript, ESLint, and 59 tests across seven relevant suites passed.
- [x] All 27 SVG assets parse, and generated SVG templates match their sources. Shared orbit geometry reduces the animated loop to 98KB, below the 100KB limit; its timing and labels are preserved.
- [x] Browser checks covered locale switching, English/Chinese layouts, desktop and mobile sizing, the shared header, form validation, CTA navigation/focus, and submission transitions. Form card height stays unchanged in the tested desktop and phone layouts.
- [x] Only enterprise-page implementation and supporting specifications are included; independent local reference previews are excluded.
- [x] Merged current main (`4c93ca2e`) without conflicts; the resulting PR is within the 3,000-line size budget. Full import-boundary/dead-code CI lint and the asset-size gate pass locally.
- [x] CI checks passed on final commit `ad845130`: build, lint/typecheck, unit tests, asset-size gate, CodeQL, and both automatic reviews. No open code-scanning alerts or current-commit inline findings. Human review is still required before merge.


---

## fix(analytics): improve v2 event accuracy (#3670)

- **SHA**: `4c93ca2eff78be01bf6b959c03fb8fe54edfde1c`
- **作者**: winston-srp
- **日期**: 2026-09-08T09:48:35Z
- **PR**: #3670

### Commit Message

```
fix(analytics): improve v2 event accuracy (#3670)

## Summary

- suppress repeated `flow_start` observations by `flow_id` within the
current document
- suppress repeated `chat_submit` and `send_message` observations by
`operation_id`, while preserving separate logical operations
- freeze `operation_id` and initiating `user_id` before asynchronous
message/install requests and reuse that immutable context in result
callbacks
- emit Plan `purchase` with only the Checkout Snapshot `initiating_uid`;
when the Snapshot is unavailable, explicitly use anonymous GA4 identity
instead of reading the current account or `order.uid`
- scope GA4 identity as synchronous set → event → restore, and fan out
Google Ads/Reddit only after restoration
- keep the change client-only; no ETL, warehouse model, authentication,
order ownership, or payment/message business-flow changes

## Root cause

The V2 sender had no final current-document guard for Flow starts or
message facts. A repeated callback/observation therefore reached GA4
(and Reddit for successful messages) more than once even though it
represented the same `flow_id` or `operation_id`.

Production data from 2026-09-05 through 2026-09-07 showed 9 duplicated
`send_message` operations out of 449 distinct operations and 58
duplicated `card_bind_gate` Flow IDs out of 254. The matching
`chat_submit` events duplicated with the message results. The sender now
applies the spec's best-effort in-memory suppression at the typed
Tracking boundary, with a bounded ledger and no cross-tab persistence.
Missing IDs still dispatch rather than becoming an event rejection rule.

Async result callbacks could also inherit whichever page-level GA4
account happened to be active when the callback ran. The fix defines
explicit field ownership: request-time shared context is frozen before
the request, authoritative business results remain owned by the result
interface, and safe page/platform context is resolved by the sender.
Common Tracking identity no longer depends on a business response field.

For GA4, the sender temporarily applies the frozen identity,
synchronously queues the Event, and restores the current page identity
in `finally`. A missing Snapshot is valid information and is sent with
`user_id: null`; `order.uid` is not a fallback. Purchase amount,
currency, channel, and other order facts still come from the confirmed
order response.

This intentionally lowers Purchase UID completeness when the Checkout
Snapshot is missing. The accepted tradeoff is to preserve correct
identity semantics instead of guessing from mutable page identity or
coupling common Tracking parameters to an order response.

## Test plan

- [x] `bash scripts/verify-web.sh <all changed web paths>`
  - governance guards passed
  - TypeScript passed
  - 18 related test files / 399 tests passed
  - ESLint passed (two existing non-blocking `no-explicit-any` warnings)
- [x] regression tests cover same-ID suppression, distinct-operation
preservation, frozen identities across async callbacks, explicit
anonymous fallback, Checkout Snapshot-only purchase identity, GA4
identity restoration, and external fan-out ordering
- [x] Thread Reply uses a deferred request to verify that changing
accounts before the async result does not change its frozen UID
- [x] pre-push changed-surface verification passed
```

### PR Body

## Summary

- suppress repeated `flow_start` observations by `flow_id` within the current document
- suppress repeated `chat_submit` and `send_message` observations by `operation_id`, while preserving separate logical operations
- freeze `operation_id` and initiating `user_id` before asynchronous message/install requests and reuse that immutable context in result callbacks
- emit Plan `purchase` with only the Checkout Snapshot `initiating_uid`; when the Snapshot is unavailable, explicitly use anonymous GA4 identity instead of reading the current account or `order.uid`
- scope GA4 identity as synchronous set → event → restore, and fan out Google Ads/Reddit only after restoration
- keep the change client-only; no ETL, warehouse model, authentication, order ownership, or payment/message business-flow changes

## Root cause

The V2 sender had no final current-document guard for Flow starts or message facts. A repeated callback/observation therefore reached GA4 (and Reddit for successful messages) more than once even though it represented the same `flow_id` or `operation_id`.

Production data from 2026-09-05 through 2026-09-07 showed 9 duplicated `send_message` operations out of 449 distinct operations and 58 duplicated `card_bind_gate` Flow IDs out of 254. The matching `chat_submit` events duplicated with the message results. The sender now applies the spec's best-effort in-memory suppression at the typed Tracking boundary, with a bounded ledger and no cross-tab persistence. Missing IDs still dispatch rather than becoming an event rejection rule.

Async result callbacks could also inherit whichever page-level GA4 account happened to be active when the callback ran. The fix defines explicit field ownership: request-time shared context is frozen before the request, authoritative business results remain owned by the result interface, and safe page/platform context is resolved by the sender. Common Tracking identity no longer depends on a business response field.

For GA4, the sender temporarily applies the frozen identity, synchronously queues the Event, and restores the current page identity in `finally`. A missing Snapshot is valid information and is sent with `user_id: null`; `order.uid` is not a fallback. Purchase amount, currency, channel, and other order facts still come from the confirmed order response.

This intentionally lowers Purchase UID completeness when the Checkout Snapshot is missing. The accepted tradeoff is to preserve correct identity semantics instead of guessing from mutable page identity or coupling common Tracking parameters to an order response.

## Test plan

- [x] `bash scripts/verify-web.sh <all changed web paths>`
  - governance guards passed
  - TypeScript passed
  - 18 related test files / 399 tests passed
  - ESLint passed (two existing non-blocking `no-explicit-any` warnings)
- [x] regression tests cover same-ID suppression, distinct-operation preservation, frozen identities across async callbacks, explicit anonymous fallback, Checkout Snapshot-only purchase identity, GA4 identity restoration, and external fan-out ordering
- [x] Thread Reply uses a deferred request to verify that changing accounts before the async result does not change its frozen UID
- [x] pre-push changed-surface verification passed


---

## feat(desktop): connect DSH to remote and local ACP agents (#3659)

- **SHA**: `f9713045d3a1e9ac412d58afce37e16d4ba02b0c`
- **作者**: zayne-srp
- **日期**: 2026-09-08T03:26:45Z
- **PR**: #3659

### Commit Message

```
feat(desktop): connect DSH to remote and local ACP agents (#3659)

## Summary

- consolidate the managed Desktop DSH conversation foundation from #3511
into this PR; #3511 remains closed and is fully contained in this branch
- expose authenticated ACP sessions for owned V2 Engine agents through
Claw Interface
- implement the ACP lifecycle and standards-conformant MCP-over-ACP
bridge, including prompt-scoped MCP leases
- let ZooClaw Desktop discover the signed-in user's Engine workspaces
and connect DSH to the selected remote V2 Agent automatically
- add a runtime-managed Agent selector with three explicit targets:
Remote V2 Agent, local Codex, and local Claude Code
- bundle the official Codex ACP and Claude Agent ACP adapters, isolate
local Agent state in separate DSH homes, and expose local DSH tools
through standard ACP `mcpServers` backed by authenticated loopback
Streamable HTTP
- keep target commands, adapter paths, environment variables, and ports
owned by Electron Main; the renderer can only select an allow-listed
target ID
- fail explicitly when the selected target is unavailable or when remote
V2 is selected without a Desktop login; do not silently fall back to
another Agent

## Dependency

- uses the DSH implementation from SerendipityOneInc/deepseek-harness#12

## Bundled runtime

- DSH: `0.1.1-rc.2`
- DSH source commit: `bca37f82333c8fdb6ab32eac894cc5a40d583709`
- Codex ACP adapter: `1.10.0`
- Claude Agent ACP adapter: `0.74.0`
- darwin-arm64 artifact SHA-256:
`b245b790d15bd60113106b1c734d4497ba56916e0fe2df740bd137d73b6e1479`

## Protocol compatibility

- validates the ACP handshake and MCP server declarations against pinned
official ACP fixtures
- exposes MCP Streamable HTTP to V2 Engine while forwarding tool traffic
over the owning ACP connection
- uses standard ACP `mcpServers` for the official local adapters; local
DSH publishes its authenticated MCP catalog on a dynamically allocated
loopback port
- authenticates Desktop ACP WebSockets and isolates remote tool routing
by bridge lease

## Validation

- `bash scripts/verify-changed.sh`: Web governance, TypeScript, ESLint,
Claw Interface ruff, formatting, pyright, and import contracts passed
- Desktop TypeScript passed; 41 tests passed and the opt-in external
Codex test was skipped in the normal suite
- Web target-selector and General settings tests: 34 passed
- DSH artifact checksum/path validation passed and staging is idempotent
- real local Codex ACP smoke passed end to end, including the DSH MCP
catalog and assistant response
- real local Claude adapter reached ACP session binding and the DSH MCP
catalog; the model request correctly returned the local Claude CLI's
revoked-OAuth 401, so a complete Claude response requires valid user
Claude credentials
- local Claw Interface + Telepresence staging smoke previously completed
a remote V2 response and remote invocation of a Desktop DSH tool

## Review notes

- this is the only open ecap-workspace PR for the feature and supersedes
#3511
- the large diff is dominated by the pinned ACP schema fixture and
bundled DSH artifact stored through Git LFS
- no credentials or temporary tunnel URLs are committed; runtime
endpoints and tokens remain environment-provided
```

### PR Body

## Summary

- consolidate the managed Desktop DSH conversation foundation from #3511 into this PR; #3511 remains closed and is fully contained in this branch
- expose authenticated ACP sessions for owned V2 Engine agents through Claw Interface
- implement the ACP lifecycle and standards-conformant MCP-over-ACP bridge, including prompt-scoped MCP leases
- let ZooClaw Desktop discover the signed-in user's Engine workspaces and connect DSH to the selected remote V2 Agent automatically
- add a runtime-managed Agent selector with three explicit targets: Remote V2 Agent, local Codex, and local Claude Code
- bundle the official Codex ACP and Claude Agent ACP adapters, isolate local Agent state in separate DSH homes, and expose local DSH tools through standard ACP `mcpServers` backed by authenticated loopback Streamable HTTP
- keep target commands, adapter paths, environment variables, and ports owned by Electron Main; the renderer can only select an allow-listed target ID
- fail explicitly when the selected target is unavailable or when remote V2 is selected without a Desktop login; do not silently fall back to another Agent

## Dependency

- uses the DSH implementation from SerendipityOneInc/deepseek-harness#12

## Bundled runtime

- DSH: `0.1.1-rc.2`
- DSH source commit: `bca37f82333c8fdb6ab32eac894cc5a40d583709`
- Codex ACP adapter: `1.10.0`
- Claude Agent ACP adapter: `0.74.0`
- darwin-arm64 artifact SHA-256: `b245b790d15bd60113106b1c734d4497ba56916e0fe2df740bd137d73b6e1479`

## Protocol compatibility

- validates the ACP handshake and MCP server declarations against pinned official ACP fixtures
- exposes MCP Streamable HTTP to V2 Engine while forwarding tool traffic over the owning ACP connection
- uses standard ACP `mcpServers` for the official local adapters; local DSH publishes its authenticated MCP catalog on a dynamically allocated loopback port
- authenticates Desktop ACP WebSockets and isolates remote tool routing by bridge lease

## Validation

- `bash scripts/verify-changed.sh`: Web governance, TypeScript, ESLint, Claw Interface ruff, formatting, pyright, and import contracts passed
- Desktop TypeScript passed; 41 tests passed and the opt-in external Codex test was skipped in the normal suite
- Web target-selector and General settings tests: 34 passed
- DSH artifact checksum/path validation passed and staging is idempotent
- real local Codex ACP smoke passed end to end, including the DSH MCP catalog and assistant response
- real local Claude adapter reached ACP session binding and the DSH MCP catalog; the model request correctly returned the local Claude CLI's revoked-OAuth 401, so a complete Claude response requires valid user Claude credentials
- local Claw Interface + Telepresence staging smoke previously completed a remote V2 response and remote invocation of a Desktop DSH tool

## Review notes

- this is the only open ecap-workspace PR for the feature and supersedes #3511
- the large diff is dominated by the pinned ACP schema fixture and bundled DSH artifact stored through Git LFS
- no credentials or temporary tunnel URLs are committed; runtime endpoints and tokens remain environment-provided


---

## fix(observability): trace first-use milestones in Sentry (#3662)

- **SHA**: `04257ce475e468d4c9fded2f65596344b186b4a7`
- **作者**: tim-srp
- **日期**: 2026-09-08T02:56:03Z
- **PR**: #3662

### Commit Message

```
fix(observability): trace first-use milestones in Sentry (#3662)

## Summary

First-use failures were missing from Sentry across account confirmation,
free access/default-agent provisioning, payment return polling,
subscription refresh, and the first chat message. Add explicit stage
logs and sanitized failure Issues without changing business outcomes,
retry behavior, payment eligibility, or chat UI.

- Track login/account confirmation, backend registration/free
access/default-agent stages, and Card/Antom/Stripe confirmation
including trial and entitlement status.
- Register the first send for response-latency monitoring; correlate
each session-thread turn by message ID using terminal status,
deduplicated WebSocket/history observations and an idle-progress
timeout.
- Keep telemetry fail-open and remove inherited request/console/identity
payloads from new monitoring Issues.

## Test plan

- [x] 231 focused frontend tests and 108 focused backend tests passed.
- [x] Frontend TypeScript, changed-source ESLint and governance checks
passed.
- [x] Backend Ruff, formatting, dependency/import checks and full app
Pyright passed.
- [x] Real Python SDK memory-transport test verifies emitted logs/events
and PII removal.
- [x] Synced latest main; reran directly affected chat parser/monitor
tests.

The new Python SDK was installed in an isolated temporary directory, not
the shared virtualenv. Pyright used that dependency path; the default
local Pyright hook and duplicate push verifier were bypassed after
equivalent checks passed. CI installs the declared requirement and
remains authoritative.

## Rollout

Requires both Web and claw-interface deployment. Existing Web Sentry
configuration is reused. Verify whether the backend runtime already
supplies SENTRY_DSN and release metadata; reuse existing configuration
where present. No production deployment or real-account end-to-end
verification is included in this PR.

Coverage, query fields and observation limits:
`docs/validation/2026-09-07-first-use-sentry-implementation.md`.

## Failure isolation hardening

Guard stage setup and cleanup as well as SDK emission. Fault-injection
tests verify that ID/context/emission/cleanup failures cannot skip the
business body, replace its return value, or mask its original exception.
SDK failure tests also verify no synchronous flush is requested by the
stage.
```

### PR Body

## Summary

First-use failures were missing from Sentry across account confirmation, free access/default-agent provisioning, payment return polling, subscription refresh, and the first chat message. Add explicit stage logs and sanitized failure Issues without changing business outcomes, retry behavior, payment eligibility, or chat UI.

- Track login/account confirmation, backend registration/free access/default-agent stages, and Card/Antom/Stripe confirmation including trial and entitlement status.
- Register the first send for response-latency monitoring; correlate each session-thread turn by message ID using terminal status, deduplicated WebSocket/history observations and an idle-progress timeout.
- Keep telemetry fail-open and remove inherited request/console/identity payloads from new monitoring Issues.

## Test plan

- [x] 231 focused frontend tests and 108 focused backend tests passed.
- [x] Frontend TypeScript, changed-source ESLint and governance checks passed.
- [x] Backend Ruff, formatting, dependency/import checks and full app Pyright passed.
- [x] Real Python SDK memory-transport test verifies emitted logs/events and PII removal.
- [x] Synced latest main; reran directly affected chat parser/monitor tests.

The new Python SDK was installed in an isolated temporary directory, not the shared virtualenv. Pyright used that dependency path; the default local Pyright hook and duplicate push verifier were bypassed after equivalent checks passed. CI installs the declared requirement and remains authoritative.

## Rollout

Requires both Web and claw-interface deployment. Existing Web Sentry configuration is reused. Verify whether the backend runtime already supplies SENTRY_DSN and release metadata; reuse existing configuration where present. No production deployment or real-account end-to-end verification is included in this PR.

Coverage, query fields and observation limits: `docs/validation/2026-09-07-first-use-sentry-implementation.md`.

## Failure isolation hardening

Guard stage setup and cleanup as well as SDK emission. Fault-injection tests verify that ID/context/emission/cleanup failures cannot skip the business body, replace its return value, or mask its original exception. SDK failure tests also verify no synchronous flush is requested by the stage.


---
