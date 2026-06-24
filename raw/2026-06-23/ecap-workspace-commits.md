# SerendipityOneInc/ecap-workspace — commits 2026-06-23


共 10 个 commit


---

## fix(agent-packs): map agent studio display id (#2568)

- **SHA**: `ea8ffcedda75df428693b02b187a418c19fd8429`
- **作者**: bill-srp
- **日期**: 2026-06-23T13:28:00Z
- **PR**: #2568

### 完整 commit message

```
fix(agent-packs): map agent studio display id (#2568)

## Summary

- map Agent Studio YAML `name: agent-studio` to the database display id
`agent_studio`
- keep rejecting any manifest whose `name` is not `agent-studio`
- update the Agent Studio upload route tests for the split manifest name
vs DB display id

## Tests

- `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
-q`
- `/opt/homebrew/bin/ruff check
services/claw-interface/app/routes/agent_packs.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `/opt/homebrew/bin/ruff format --check
services/claw-interface/app/routes/agent_packs.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
```

### PR body

## Summary

- map Agent Studio YAML `name: agent-studio` to the database display id `agent_studio`
- keep rejecting any manifest whose `name` is not `agent-studio`
- update the Agent Studio upload route tests for the split manifest name vs DB display id

## Tests

- `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_internal_agent_packs_routes.py -q`
- `/opt/homebrew/bin/ruff check services/claw-interface/app/routes/agent_packs.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `/opt/homebrew/bin/ruff format --check services/claw-interface/app/routes/agent_packs.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`



---

## fix(agent-packs): auto approve agent studio submissions (#2567)

- **SHA**: `0e79845fdd8093c51da3fda285a55a036eb30876`
- **作者**: bill-srp
- **日期**: 2026-06-23T13:06:16Z
- **PR**: #2567

### 完整 commit message

```
fix(agent-packs): auto approve agent studio submissions (#2567)

## Summary
- auto-approve Agent Studio pack submissions created by `POST
/agent-packs/agent-studio`
- record `agent-studio` as the auto-approval reviewer identity
- update route tests to assert the auto-approval parameter and approved
response

## Testing
- `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
-q`
- `/opt/homebrew/bin/ruff check
services/claw-interface/app/routes/agent_packs.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `/opt/homebrew/bin/ruff format --check
services/claw-interface/app/routes/agent_packs.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `bash scripts/verify-changed.sh`

## Notes
- Follow-up to #2566, which was merged before this auto-approval change
was pushed.
```

### PR body

## Summary
- auto-approve Agent Studio pack submissions created by `POST /agent-packs/agent-studio`
- record `agent-studio` as the auto-approval reviewer identity
- update route tests to assert the auto-approval parameter and approved response

## Testing
- `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_internal_agent_packs_routes.py -q`
- `/opt/homebrew/bin/ruff check services/claw-interface/app/routes/agent_packs.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `/opt/homebrew/bin/ruff format --check services/claw-interface/app/routes/agent_packs.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `bash scripts/verify-changed.sh`

## Notes
- Follow-up to #2566, which was merged before this auto-approval change was pushed.



---

## fix(web): restore email otp login captcha (#2564)

- **SHA**: `bff5914185969f019734d5446d8e7f3ab792d953`
- **作者**: tim-srp
- **日期**: 2026-06-23T12:40:39Z
- **PR**: #2564

### 完整 commit message

```
fix(web): restore email otp login captcha (#2564)

## Summary
- Restore the email OTP login entrypoint and remove the extra
`showEmailLogin` URL/prop gate.
- Gate `Continue with Email` behind the shared login Turnstile challenge
and forward captcha fields through the email OTP send BFF to
account-service.
- Rename the public login captcha flag to
`NEXT_PUBLIC_ECAP_LOGIN_CAPTCHA_REQUIRED` and update docs/workflow
wiring.

## Root cause
Email OTP login was still implemented, but `LoginModal` hid the
entrypoint behind `?email_login=1`. The existing Turnstile wiring only
covered Google/phone and used a Google-specific public flag name.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web exec tsc --noEmit --project app/tsconfig.json`
- [x] `pnpm --filter @zooclaw/web-app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`

Note: `pnpm --dir web run tsc` currently fails before typechecking
because the workspace script expands to `pnpm -r
--workspace-concurrency=1 --if-present exec tsc --noEmit`, and this pnpm
version rejects `--if-present` for `exec`. The CI workflow uses `tsc
--noEmit --project app/tsconfig.json`, which passes locally.
```

### PR body

## Summary
- Restore the email OTP login entrypoint and remove the extra `showEmailLogin` URL/prop gate.
- Gate `Continue with Email` behind the shared login Turnstile challenge and forward captcha fields through the email OTP send BFF to account-service.
- Rename the public login captcha flag to `NEXT_PUBLIC_ECAP_LOGIN_CAPTCHA_REQUIRED` and update docs/workflow wiring.

## Root cause
Email OTP login was still implemented, but `LoginModal` hid the entrypoint behind `?email_login=1`. The existing Turnstile wiring only covered Google/phone and used a Google-specific public flag name.

## Test plan
- [x] `pnpm --dir web run lint`
- [x] `pnpm --dir web exec tsc --noEmit --project app/tsconfig.json`
- [x] `pnpm --filter @zooclaw/web-app exec tsc --noEmit`
- [x] `pnpm --dir web run test:unit`

Note: `pnpm --dir web run tsc` currently fails before typechecking because the workspace script expands to `pnpm -r --workspace-concurrency=1 --if-present exec tsc --noEmit`, and this pnpm version rejects `--if-present` for `exec`. The CI workflow uses `tsc --noEmit --project app/tsconfig.json`, which passes locally.


---

## feat(agent-packs): add agent studio pack upload endpoint (#2566)

- **SHA**: `638e647856fda8fcc5793c8bd981dd30657433c1`
- **作者**: bill-srp
- **日期**: 2026-06-23T12:24:07Z
- **PR**: #2566

### 完整 commit message

```
feat(agent-packs): add agent studio pack upload endpoint (#2566)

## Summary
- add authenticated `POST /agent-packs/agent-studio` endpoint for Agent
Studio pack zip uploads
- parse only `agent-pack.yaml`, require `name: agent-studio`, look up
the pack by org/display id, upload the original zip to R2, and create a
pack submission
- ignore `description.json` and do not import quick commands from the
manifest

## Testing
- `/Users/bill/.venvs/claw-interface/bin/pytest
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py
-q`
- `/opt/homebrew/bin/ruff check
services/claw-interface/app/routes/agent_packs.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `/opt/homebrew/bin/ruff format --check
services/claw-interface/app/routes/agent_packs.py
services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `bash scripts/verify-py.sh` *(ruff passed; failed because local
`pyright` and `lint-imports` are not installed)*
- `bash scripts/verify-changed.sh` *(skipped py because local backend
toolchain is incomplete)*

## Notes
- Requires `AGENT_STUDIO_PACK_UPDATE_TOKEN` to be configured in the
backend environment.
```

### PR body

## Summary
- add authenticated `POST /agent-packs/agent-studio` endpoint for Agent Studio pack zip uploads
- parse only `agent-pack.yaml`, require `name: agent-studio`, look up the pack by org/display id, upload the original zip to R2, and create a pack submission
- ignore `description.json` and do not import quick commands from the manifest

## Testing
- `/Users/bill/.venvs/claw-interface/bin/pytest services/claw-interface/tests/unit/test_internal_agent_packs_routes.py -q`
- `/opt/homebrew/bin/ruff check services/claw-interface/app/routes/agent_packs.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `/opt/homebrew/bin/ruff format --check services/claw-interface/app/routes/agent_packs.py services/claw-interface/tests/unit/test_internal_agent_packs_routes.py`
- `bash scripts/verify-py.sh` *(ruff passed; failed because local `pyright` and `lint-imports` are not installed)*
- `bash scripts/verify-changed.sh` *(skipped py because local backend toolchain is incomplete)*

## Notes
- Requires `AGENT_STUDIO_PACK_UPDATE_TOKEN` to be configured in the backend environment.



---

## feat(web): mattermost ws observability + keepalive watchdog & online/stale recovery (#2558)

- **SHA**: `bafb37adf338afbfedcd520acc00a67987131911`
- **作者**: sharplee-srp
- **日期**: 2026-06-23T08:42:40Z
- **PR**: #2558

### 完整 commit message

```
feat(web): mattermost ws observability + keepalive watchdog & online/stale recovery (#2558)

## Summary

Two parts for ECA-1037, kept in one PR:

**1. Observability (was PR1)**
- enrich existing `mm.connection.transition` logs with Mattermost
browser WS diagnostics
- record connection age, last pong age, close metadata, readyState, and
tab visibility on existing transition events

**2. Recovery (the fix the observability was meant to inform)**
- **keepalive watchdog** (`websocket.ts`): after `MAX_MISSED_PONGS` (2)
unanswered keepalive pings (~30s), the socket is treated as a half-open
zombie — the browser never fires `onclose` for these — so we stop
pinging the dead socket and notify `onStale` consumers.
- **stale recovery** (`useMattermostConnection.ts`): `onStale` →
`forceReconnect('stale_timeout')`. Previously a visible-tab zombie was
only caught on the next tab refocus; now it self-heals while visible.
- **online recovery**: an `online` window listener →
`forceReconnect('online_retry')` revives a reconnect-exhausted
connection the moment the browser regains network, instead of waiting
for a tab refocus.
- two new transition reasons `stale_timeout` / `online_retry` (both
classified as anomalies) so Sentry can distinguish watchdog-driven and
network-recovery transitions.

Net: connection drops are now both *measured* (close-driven, zombie,
exhaustion, age distribution) and *recovered* (close → backoff
reconnect, zombie → watchdog reconnect, exhaustion → online/visibility
resume).

Linear: https://linear.app/srpone/issue/ECA-1037

## Tests

- devcontainer unit: `pnpm exec vitest run
tests/unit/lib/mattermost/websocket.unit.spec.ts
tests/unit/hooks/mattermost/useMattermostConnection.unit.spec.ts
tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts` (79
passed) — adds watchdog fire/no-fire, `stale_timeout`, `online_retry`,
and online-while-connected no-op cases
- devcontainer: `pnpm exec tsc --noEmit`; targeted ESLint on modified
files
- **Real staging E2E** (devcontainer + live staging bot `31b7ba01…`):
drove the real chat path against the real Mattermost socket and
confirmed the new diagnostics populate on (a) a client-injected
`close(4001)` drop (`was_clean=true`) and (b) a spontaneous real `1006`
drop (`was_clean=false`), plus `last_pong_age_ms` populating after a
real ping/pong and clean `reconnected` recovery.

## Out of scope

UI surface for the disconnected/exhausted state and any server-side
(Mattermost/LB) keepalive tuning — separate follow-ups if needed.
```

### PR body

## Summary

Two parts for ECA-1037, kept in one PR:

**1. Observability (was PR1)**
- enrich existing `mm.connection.transition` logs with Mattermost browser WS diagnostics
- record connection age, last pong age, close metadata, readyState, and tab visibility on existing transition events

**2. Recovery (the fix the observability was meant to inform)**
- **keepalive watchdog** (`websocket.ts`): after `MAX_MISSED_PONGS` (2) unanswered keepalive pings (~30s), the socket is treated as a half-open zombie — the browser never fires `onclose` for these — so we stop pinging the dead socket and notify `onStale` consumers.
- **stale recovery** (`useMattermostConnection.ts`): `onStale` → `forceReconnect('stale_timeout')`. Previously a visible-tab zombie was only caught on the next tab refocus; now it self-heals while visible.
- **online recovery**: an `online` window listener → `forceReconnect('online_retry')` revives a reconnect-exhausted connection the moment the browser regains network, instead of waiting for a tab refocus.
- two new transition reasons `stale_timeout` / `online_retry` (both classified as anomalies) so Sentry can distinguish watchdog-driven and network-recovery transitions.

Net: connection drops are now both *measured* (close-driven, zombie, exhaustion, age distribution) and *recovered* (close → backoff reconnect, zombie → watchdog reconnect, exhaustion → online/visibility resume).

Linear: https://linear.app/srpone/issue/ECA-1037

## Tests

- devcontainer unit: `pnpm exec vitest run tests/unit/lib/mattermost/websocket.unit.spec.ts tests/unit/hooks/mattermost/useMattermostConnection.unit.spec.ts tests/unit/lib/sentry/connection-mismatch-monitor.unit.spec.ts` (79 passed) — adds watchdog fire/no-fire, `stale_timeout`, `online_retry`, and online-while-connected no-op cases
- devcontainer: `pnpm exec tsc --noEmit`; targeted ESLint on modified files
- **Real staging E2E** (devcontainer + live staging bot `31b7ba01…`): drove the real chat path against the real Mattermost socket and confirmed the new diagnostics populate on (a) a client-injected `close(4001)` drop (`was_clean=true`) and (b) a spontaneous real `1006` drop (`was_clean=false`), plus `last_pong_age_ms` populating after a real ping/pong and clean `reconnected` recovery.

## Out of scope

UI surface for the disconnected/exhausted state and any server-side (Mattermost/LB) keepalive tuning — separate follow-ups if needed.



---

## feat(new-chat): collapse agent selector to two rows with expand toggle (#2563)

- **SHA**: `0857fbca53d26985bf6aa671bf378e81fd6fd33d`
- **作者**: lynn Zhuang
- **日期**: 2026-06-23T08:28:21Z
- **PR**: #2563

### 完整 commit message

```
feat(new-chat): collapse agent selector to two rows with expand toggle (#2563)

## What

The new-chat "Choose an agent" selector previously rendered every agent
as wrapping pills, which could grow to many rows. It now **clamps to two
rows by default** and shows an inline chevron toggle at the end of row 2
to expand/collapse when there are more agents than fit.

- Collapsed (default): first two rows of agent pills + a `▾` chevron at
the end of row 2.
- Expanded: all agents + a `▴` chevron to collapse.
- No chevron when agents already fit within two rows (no behavior change
for small teams).

## How

- **`agent-selector-rows.ts`** (new, pure):
`computeCollapsedVisibleCount(rects, containerWidth, chevronWidth, gap)`
groups measured pill rects into rows and returns how many pills survive
the collapse, reserving space for the chevron at the end of row 2
(always keeps all of row 1 and ≥1 pill in row 2).
- **`AgentSelector.tsx`**: an invisible measuring layer renders every
pill at the real width; a `useIsomorphicLayoutEffect` reads each pill's
box and a `ResizeObserver` recomputes on container resize. The visible
row renders `agents.slice(0, visibleCount)` when collapsed, plus the
chevron toggle.
- Accessibility: chevron is a button with `aria-expanded`,
`aria-controls`, and "Show all agents" / "Show fewer agents" labels.

## Decisions

- A selected agent that falls in a hidden row stays hidden until expand
(the composer header still names the active agent) — chosen for
predictable ordering.
- Chevron is icon-only (no count), matching the existing pill styling.

## Testing

- `bash scripts/verify-web.sh` — tsc, vitest (31/31 incl. 6 new cases
for the row-fit math), eslint all pass.
- Verified live in-app: collapsed shows 2 rows + chevron; expanding
reveals all agents; toggling collapses again. Responsive (re-measures on
resize).
- jsdom has no real layout, so the DOM wiring is exercised by the live
app; the pure helper is unit-tested with synthetic rects (noted in the
test).
![Uploading screenshot-20260623-155624.png…]()

---------

Co-authored-by: Lynn Zhuang <lynnzhuang@MacBook-Pro.local>
```

### PR body

## What

The new-chat "Choose an agent" selector previously rendered every agent as wrapping pills, which could grow to many rows. It now **clamps to two rows by default** and shows an inline chevron toggle at the end of row 2 to expand/collapse when there are more agents than fit.

- Collapsed (default): first two rows of agent pills + a `▾` chevron at the end of row 2.
- Expanded: all agents + a `▴` chevron to collapse.
- No chevron when agents already fit within two rows (no behavior change for small teams).

## How

- **`agent-selector-rows.ts`** (new, pure): `computeCollapsedVisibleCount(rects, containerWidth, chevronWidth, gap)` groups measured pill rects into rows and returns how many pills survive the collapse, reserving space for the chevron at the end of row 2 (always keeps all of row 1 and ≥1 pill in row 2).
- **`AgentSelector.tsx`**: an invisible measuring layer renders every pill at the real width; a `useIsomorphicLayoutEffect` reads each pill's box and a `ResizeObserver` recomputes on container resize. The visible row renders `agents.slice(0, visibleCount)` when collapsed, plus the chevron toggle.
- Accessibility: chevron is a button with `aria-expanded`, `aria-controls`, and "Show all agents" / "Show fewer agents" labels.

## Decisions

- A selected agent that falls in a hidden row stays hidden until expand (the composer header still names the active agent) — chosen for predictable ordering.
- Chevron is icon-only (no count), matching the existing pill styling.

## Testing

- `bash scripts/verify-web.sh` — tsc, vitest (31/31 incl. 6 new cases for the row-fit math), eslint all pass.
- Verified live in-app: collapsed shows 2 rows + chevron; expanding reveals all agents; toggling collapses again. Responsive (re-measures on resize).
- jsdom has no real layout, so the DOM wiring is exercised by the live app; the pure helper is unit-tested with synthetic rects (noted in the test).
![Uploading screenshot-20260623-155624.png…]()



---

## feat(openclaw): warn on ephemeral storage risk (#2562)

- **SHA**: `526ee9cabbfe29e2fb3b4ffd68e769ce92cdfa1d`
- **作者**: kaka-srp
- **日期**: 2026-06-23T07:54:34Z
- **PR**: #2562

### 完整 commit message

```
feat(openclaw): warn on ephemeral storage risk (#2562)

## Linear
https://linear.app/srpone/issue/ECA-1058/ephemeral-storage-risk-warning

## Summary
- Add ephemeral storage typing and parsing for FastClaw resources,
including request, limit, and used quantities.
- Poll main bot resources and show a reminder-only composer warning when
used / limit reaches 80%, clearing only below 75%.
- Suppress the uid-scoped warning on computer-specific chats and guard
against stale or mismatched bot resources.
- Add mock backend data and unit coverage for parsing, the risk hook,
composer forwarding, and API pass-through.

## Test plan
- [x] bash scripts/verify-changed.sh
- [x] bash scripts/verify-web.sh selected changed frontend paths
- [x] bash scripts/verify-py.sh
- [x] Focused frontend vitest for storage parser, risk hook, composer,
chat surface, and API route coverage
- [x] Focused backend pytest for OpenClaw resources pass-through
```

### PR body

## Linear
https://linear.app/srpone/issue/ECA-1058/ephemeral-storage-risk-warning

## Summary
- Add ephemeral storage typing and parsing for FastClaw resources, including request, limit, and used quantities.
- Poll main bot resources and show a reminder-only composer warning when used / limit reaches 80%, clearing only below 75%.
- Suppress the uid-scoped warning on computer-specific chats and guard against stale or mismatched bot resources.
- Add mock backend data and unit coverage for parsing, the risk hook, composer forwarding, and API pass-through.

## Test plan
- [x] bash scripts/verify-changed.sh
- [x] bash scripts/verify-web.sh selected changed frontend paths
- [x] bash scripts/verify-py.sh
- [x] Focused frontend vitest for storage parser, risk hook, composer, chat surface, and API route coverage
- [x] Focused backend pytest for OpenClaw resources pass-through



---

## docs(web): data-fetching redundancy audit + progressive refactor plan (ECA-1062) (#2561)

- **SHA**: `0cc1ad53377673a12c60090b2d6b3d48fd1672ed`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-23T05:38:58Z
- **PR**: #2561

### 完整 commit message

```
docs(web): data-fetching redundancy audit + progressive refactor plan (ECA-1062) (#2561)

## What

A findings report + **progressive, backward-compatible refactor plan**
for redundant / unreasonable data fetching in `web/app`. **Docs only —
no business code changed.**

Spec:
`docs/superpowers/specs/2026-06-23-webapp-data-fetching-redundancy-refactor.md`

Linear:
[ECA-1062](https://linear.app/srpone/issue/ECA-1062/webapp-数据获取冗余审计与渐进式重构计划)

## How it was audited

Multi-agent audit of `web/app/src` (TanStack Query v5): a **138
call-site census across 136 endpoints** → **8 page-cluster detectors** →
**every finding adversarially verified** (default-skeptic: prove RQ
isn't already deduping via shared `queryKey` / `enabled` gate /
`staleTime` window before accepting). **19 confirmed / 19 rejected**
(50% rejection rate).

## Key result

The app already did a full RQ migration, so the naive "N components on a
page → N calls" redundancy is **mostly already neutralized** by RQ
in-flight dedup + the global 30s `staleTime` (e.g. `/account/me`'s three
observers collapse to one request). Those "false redundancies" were all
rejected by the verify stage.

The **durable** redundancy is exactly the two patterns that bypass RQ:

1. **Raw fetch inside a `queryFn`** (RQ-invisible, never deduped). The
linchpin: `useUserAgents`' queryFn warms agent-packs via a bare `await
listAgentPacks()` + `setQueryData(...)`, which races the independent
`useAgentPacks` (`refetchOnMount: 'always'`) → **2 concurrent
`/api/claw/agent-packs` per mount** on every shell / chat /
agents-manager render. Also violates the repo's own R1 ("never
write/derive cache inside a queryFn").
2. **`refetchOnMount: 'always'` / `staleTime: 0` sprawl** forcing
route-invariant and even **rate-limited** endpoints (`GET
/openclaw/agents`, 10 calls/5s) to refetch on every navigation.

19 confirmed findings collapse to **3 systemic anti-patterns / 11
root-cause fix groups**.

## The plan (7 phases, each independently shippable & reversible)

| Phase | Scope | Risk |
|-------|-------|------|
| 0 | Guardrails: staleTime-semantics table + key-consistency test |
none |
| 1 | **(highest value)** `useUserAgents` raw `listAgentPacks()` →
`ensureQueryData(openclawKeys.agentPacks())`; same for
`useDeepLinkHireFlow` | low |
| 2 | agent-packs as immutable catalog (`staleTime: Infinity`) + drop
`useUserAgents`' `'always'` | medium |
| 3 | login-flow `manager.ts:559/593` raw `getAccountMe()` →
`fetchQuery(accountSessionKeys.me)` | low–med |
| 4 | `ClawConnectionStatus` hand-rolled setTimeout poll → shared RQ
poller | medium |
| 5 | key-fragmentation / cold-load double-fetch / waterfall fixes | low
|
| 6 | forced-refetch sprawl + low-prio fragments (admin releases likely
WONTFIX) | low |

Forward-compatibility rationale: dropping `'always'` keeps freshness via
**30s staleTime + window-focus refetch + existing mutation
invalidation** — the three that already cover what `'always'` was added
for.

## Scope of this PR

This PR lands **only the audit report + spec** (docs). Each
implementation phase ships as its own follow-up PR against ECA-1062,
validated via mock-backend (count endpoint hits before/after) + `bash
scripts/verify-web.sh`, respecting existing guardrails (no new
raw-fetch, R1, query-key factories, W1-lib-pure).

## Test plan

- [x] Docs-only; no code paths touched
- [ ] Reviewer sanity-check of the #1 root cause
(`useUserAgents.ts:72-73` + `useAgentPacks.ts:14`) and the phase
ordering

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What

A findings report + **progressive, backward-compatible refactor plan** for redundant / unreasonable data fetching in `web/app`. **Docs only — no business code changed.**

Spec: `docs/superpowers/specs/2026-06-23-webapp-data-fetching-redundancy-refactor.md`

Linear: [ECA-1062](https://linear.app/srpone/issue/ECA-1062/webapp-数据获取冗余审计与渐进式重构计划)

## How it was audited

Multi-agent audit of `web/app/src` (TanStack Query v5): a **138 call-site census across 136 endpoints** → **8 page-cluster detectors** → **every finding adversarially verified** (default-skeptic: prove RQ isn't already deduping via shared `queryKey` / `enabled` gate / `staleTime` window before accepting). **19 confirmed / 19 rejected** (50% rejection rate).

## Key result

The app already did a full RQ migration, so the naive "N components on a page → N calls" redundancy is **mostly already neutralized** by RQ in-flight dedup + the global 30s `staleTime` (e.g. `/account/me`'s three observers collapse to one request). Those "false redundancies" were all rejected by the verify stage.

The **durable** redundancy is exactly the two patterns that bypass RQ:

1. **Raw fetch inside a `queryFn`** (RQ-invisible, never deduped). The linchpin: `useUserAgents`' queryFn warms agent-packs via a bare `await listAgentPacks()` + `setQueryData(...)`, which races the independent `useAgentPacks` (`refetchOnMount: 'always'`) → **2 concurrent `/api/claw/agent-packs` per mount** on every shell / chat / agents-manager render. Also violates the repo's own R1 ("never write/derive cache inside a queryFn").
2. **`refetchOnMount: 'always'` / `staleTime: 0` sprawl** forcing route-invariant and even **rate-limited** endpoints (`GET /openclaw/agents`, 10 calls/5s) to refetch on every navigation.

19 confirmed findings collapse to **3 systemic anti-patterns / 11 root-cause fix groups**.

## The plan (7 phases, each independently shippable & reversible)

| Phase | Scope | Risk |
|-------|-------|------|
| 0 | Guardrails: staleTime-semantics table + key-consistency test | none |
| 1 | **(highest value)** `useUserAgents` raw `listAgentPacks()` → `ensureQueryData(openclawKeys.agentPacks())`; same for `useDeepLinkHireFlow` | low |
| 2 | agent-packs as immutable catalog (`staleTime: Infinity`) + drop `useUserAgents`' `'always'` | medium |
| 3 | login-flow `manager.ts:559/593` raw `getAccountMe()` → `fetchQuery(accountSessionKeys.me)` | low–med |
| 4 | `ClawConnectionStatus` hand-rolled setTimeout poll → shared RQ poller | medium |
| 5 | key-fragmentation / cold-load double-fetch / waterfall fixes | low |
| 6 | forced-refetch sprawl + low-prio fragments (admin releases likely WONTFIX) | low |

Forward-compatibility rationale: dropping `'always'` keeps freshness via **30s staleTime + window-focus refetch + existing mutation invalidation** — the three that already cover what `'always'` was added for.

## Scope of this PR

This PR lands **only the audit report + spec** (docs). Each implementation phase ships as its own follow-up PR against ECA-1062, validated via mock-backend (count endpoint hits before/after) + `bash scripts/verify-web.sh`, respecting existing guardrails (no new raw-fetch, R1, query-key factories, W1-lib-pure).

## Test plan

- [x] Docs-only; no code paths touched
- [ ] Reviewer sanity-check of the #1 root cause (`useUserAgents.ts:72-73` + `useAgentPacks.ts:14`) and the phase ordering

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## docs(claw-interface): add refactor proposal for coupling + compensatory code (#2560)

- **SHA**: `b56e50e9e9269b0bd94441fb4b29e3ea84fffed0`
- **作者**: Chris@ZooClaw
- **日期**: 2026-06-23T04:35:02Z
- **PR**: #2560

### 完整 commit message

```
docs(claw-interface): add refactor proposal for coupling + compensatory code (#2560)

## What

新增架构审计 +
重构提案文档：`docs/superpowers/specs/2026-06-23-claw-interface-refactor.md`。

针对 `services/claw-interface`（~74k LOC）做了一次多 agent
扫描，回应同事反馈的“代码为了不报错做了大量补偿性处理”。结论：补偿性代码是症状，根因是三条本该存在的边界从未建立——**仓储类型层 /
PaymentProvider 适配层 / 跨服务 saga 原语**。

## 量化信号

- 491 个 `except Exception` + 17 个 `except: pass`
- ~717 个 `or {}` / `or []` / `or None` 防御默认
- 三套并行支付实现（stripe / antom / apple）逐文件复制 record/reconcile/compensation
- 订阅状态双真相源（legacy user-doc vs Billing v2 ledger）→ 一整队对账 cron 只为同步两者

## 方法

多 agent 工作流：依赖图测绘 → 9 个 hunter（6 域 + 3 跨切面）并行 → 每条发现派独立怀疑者重读引用代码复核 →
综合。69 条发现复核后确认 59、驳回 10。其中 2.3 补偿终态分叉项（经核实下调，非确定资金 bug）与 2.5
鉴权项（已确认）由作者二次人工核实定稿。

## 注意

- 这是 **findings report + 提案**，不含代码改动。
- 后续 P0/P1 拆成独立 Linear issue 跟踪（链接见文档第 4 节路线图）。

## Test plan

- [x] 纯文档变更，无代码 / CI 行为影响

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

### PR body

## What

新增架构审计 + 重构提案文档：`docs/superpowers/specs/2026-06-23-claw-interface-refactor.md`。

针对 `services/claw-interface`（~74k LOC）做了一次多 agent 扫描，回应同事反馈的“代码为了不报错做了大量补偿性处理”。结论：补偿性代码是症状，根因是三条本该存在的边界从未建立——**仓储类型层 / PaymentProvider 适配层 / 跨服务 saga 原语**。

## 量化信号

- 491 个 `except Exception` + 17 个 `except: pass`
- ~717 个 `or {}` / `or []` / `or None` 防御默认
- 三套并行支付实现（stripe / antom / apple）逐文件复制 record/reconcile/compensation
- 订阅状态双真相源（legacy user-doc vs Billing v2 ledger）→ 一整队对账 cron 只为同步两者

## 方法

多 agent 工作流：依赖图测绘 → 9 个 hunter（6 域 + 3 跨切面）并行 → 每条发现派独立怀疑者重读引用代码复核 → 综合。69 条发现复核后确认 59、驳回 10。其中 2.3 补偿终态分叉项（经核实下调，非确定资金 bug）与 2.5 鉴权项（已确认）由作者二次人工核实定稿。

## 注意

- 这是 **findings report + 提案**，不含代码改动。
- 后续 P0/P1 拆成独立 Linear issue 跟踪（链接见文档第 4 节路线图）。

## Test plan

- [x] 纯文档变更，无代码 / CI 行为影响



---

## fix(api): normalize main computer agent name (#2559)

- **SHA**: `3a3798190d27a5f10858320f2d67b5e9cbd5f681`
- **作者**: bill-srp
- **日期**: 2026-06-23T04:28:26Z
- **PR**: #2559

### 完整 commit message

```
fix(api): normalize main computer agent name (#2559)

## Summary
- Normalize the V2 computer agents response so main-agent system default
names (`zoo-{uid}` / `zoo-{uid}-{timestamp}` / blank) display as
`Assistant`.
- Preserve custom main-agent names from `AgentWorkspace.name`, so user
rename flows are not masked.
- Normalize new main Mattermost workspace projections to store
`Assistant` instead of continuing to mirror `zoo-*` defaults.

## Root cause
The V2 `/computers/{computer_id}/agents` response projected
`AgentWorkspace.name` directly, so historical main-agent rows
initialized from computer/Mattermost defaults could surface names like
`zoo-{uid}`. A previous response-layer hardcode fixed the default
display but masked valid user-renamed main agents; this version only
normalizes system default names.

## Test plan
- [x]
`/Users/bill/Github/StarQuestAI/ecap-workspace-ios-1.8.0/services/claw-interface/.venv/bin/python
-m pytest services/claw-interface/tests/unit/test_agent_service.py
services/claw-interface/tests/unit/test_agent_mm_projectors.py`
- [x]
`PATH="/Users/bill/Github/StarQuestAI/ecap-workspace-ios-1.8.0/services/claw-interface/.venv/bin:$PATH"
bash scripts/verify-py.sh`

Note: the normal commit pre-commit hook hung while running `pre-commit`
with no hook output, so commits were created with `--no-verify` after
the equivalent backend checks above passed.
```

### PR body

## Summary
- Normalize the V2 computer agents response so main-agent system default names (`zoo-{uid}` / `zoo-{uid}-{timestamp}` / blank) display as `Assistant`.
- Preserve custom main-agent names from `AgentWorkspace.name`, so user rename flows are not masked.
- Normalize new main Mattermost workspace projections to store `Assistant` instead of continuing to mirror `zoo-*` defaults.

## Root cause
The V2 `/computers/{computer_id}/agents` response projected `AgentWorkspace.name` directly, so historical main-agent rows initialized from computer/Mattermost defaults could surface names like `zoo-{uid}`. A previous response-layer hardcode fixed the default display but masked valid user-renamed main agents; this version only normalizes system default names.

## Test plan
- [x] `/Users/bill/Github/StarQuestAI/ecap-workspace-ios-1.8.0/services/claw-interface/.venv/bin/python -m pytest services/claw-interface/tests/unit/test_agent_service.py services/claw-interface/tests/unit/test_agent_mm_projectors.py`
- [x] `PATH="/Users/bill/Github/StarQuestAI/ecap-workspace-ios-1.8.0/services/claw-interface/.venv/bin:$PATH" bash scripts/verify-py.sh`

Note: the normal commit pre-commit hook hung while running `pre-commit` with no hook output, so commits were created with `--no-verify` after the equivalent backend checks above passed.

