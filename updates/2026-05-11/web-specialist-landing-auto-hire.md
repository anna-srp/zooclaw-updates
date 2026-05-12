---
title: "从 Specialist 落地页进入聊天，自动激活并投递初始问题"
type: "产品基础功能更新"
priority: "中"
date: "2026-05-11"
status: "待审核"
channels: "Discord, changelog"
---

# 从 Specialist 落地页进入聊天，自动激活并投递初始问题

## 核心宣传点

点击 Specialist 推广页面的「立即体验」进入聊天后，系统自动切换到对应 AI 角色并发出你在落地页输入的问题，一键直达。

## 原始内容

Commit message:
feat(web): Landing-page auto-hire and initial-query delivery flow (#1584)

## Summary

Implements the chat-side of
[ECA-641](https://linear.app/srpone/issue/ECA-641/web-specialist-落地页用户信息延续与初始-query-投递):
when a user arrives at `/chat?sp=<specialist_id>` from a Specialist
landing page with matching localStorage context, the chat client
auto-hires the specialist (if needed), switches to it, and delivers the
initial query — all gated behind auth + onboarding + chat-ready, with an
explicit Main-Agent fallback for failure paths.

The producer side (landing-page `writeLandingContext` caller, E1–E9
instrumentation, send success/failure telemetry) is out of scope for
this PR — see [Deferred](#deferred) below.

## Files

- **`web/src/lib/landing-context.ts`** — context schema + storage
helpers
- `localStorage` (not session) so context survives any new-tab/window
hop in the auth flow per ECA-641 §2's "全程延续" target
- 24h TTL via `created_at` field — drops zombie contexts from abandoned
flows; missing `created_at` is treated as fresh for backwards-compat
with older landing-page writes
- Cross-validates URL `?sp=` against stored `specialist_id` (mismatch →
discard)
- Sanitizes nested fields (`initial_query.text`, `source`, `created_at`)
on read — localStorage is user-tamperable, so a malformed payload like
`{ initial_query: { text: 123 } }` is coerced to `{ text: '' }` instead
of crashing Phase 5 at `.trim()`
- Idempotency via `markLandingDelivered(landing_session_id)` — also in
localStorage so the marker follows the user across tabs

- **`web/src/app/[locale]/chat/hooks/useLandingContextFlow.ts`** —
6-phase state machine
  ```
idle → awaiting_auth → awaiting_chat_ready → hiring → delivering →
completed
  ```
- **Phase 3 catalog gates** — holds while `catalogLoading`; holds while
`catalogItems.length === 0` (`useOfficialAgentCatalog` swallows fetch
errors and surfaces them as `items=[] + isLoading=false`,
indistinguishable from a genuinely-empty catalog at read time); **Phase
3b** schedules an 8s safety-net timeout so we don't hang forever on a
persistent catalog outage. Mirrors `useDeepLinkHireFlow`'s pattern.
- **Phase 4 hire** — `installOpenClawAgentAsync` +
`waitForOpenClawAgentOperation` are part of the hire transaction;
`refreshUserAgentsCache` is wrapped in its own try/catch so a transient
`/users/me/agents` GET failure doesn't get misclassified as install
failure (would otherwise route the prompt to Main Agent even though the
specialist IS hired server-side).
- **Phase 5 delivery gate** — `currentAgentId !== state.resolvedAgentId`
blocks delivery until `router.replace` propagates and
`handleSendMessage`'s closure rebuilds with the new
`agentId`/`sessionKey`. Treating `null` as "main agent" on both sides
means fallback paths also wait for the URL to switch before sending.
- **ECA-641 §4.2 Main-Agent fallback** — fallback paths (specialist not
in catalog, hire failure, catalog-empty timeout) all call
`onSwitchAgent(null)` explicitly, which routes through
`router.replace('/chat')`. This both routes the user to a working chat
surface AND strips `?sp=` from the URL.
- **Best-effort delivery** — both `.then` and `.catch` branches mark
delivered + clear context. Intentional: `handleSendMessage` swallows
errors and surfaces them via toast, so the auto-flow doesn't retry; the
user manually retries via the chat input. Prevents retry loops in
degenerate failure modes.
- **Latched `canUseChatEver` / `isChatReadyEver`** — both signals
oscillate during post-login resolution and may never both be `true` at
the same instant; latching converts the gate to a monotonic "has been
true at least once this session" predicate. Mirrors
`useDeepLinkHireFlow`.

- **`web/src/app/[locale]/chat/GenClawClient.tsx`** — integration
- Wires the hook with `searchParams`, `agentId` (as `currentAgentId`),
and existing handlers
- `handleLandingSwitchAgent(agentId | null)` — `null` ⇒ Main Agent ⇒
`router.replace('/chat')`; non-null ⇒
`router.replace('/chat?agent_id=...')`. Either way the entire query
string is overwritten, so `?sp=` is stripped on completion.
- Coexists with existing `useDeepLinkHireFlow` (different URL param:
`sp` vs `agent_id`).

## ECA-641 spec coverage

| Spec section | Status |
|---|---|
| §1 specialist_id + initial_query.text + source + landing_session_id |
✅ |
| §1 initial_query.attachments | ⏭️ Embedded as URLs in `text` per
direction (no separate field; chat input renders markdown) |
| §2 cross-stage persistence (登录前 / 注册中 / 注册后 / Onboarding) | ✅
localStorage + 24h TTL |
| §3.1 Specialist hire prerequisite | ✅ Phase 4 |
| §3.2 Auto-land on Specialist chat | ✅ `onSwitchAgent` + URL switch |
| §3.3 Auto-send initial query | ✅ Phase 5 |
| §3.3 Idempotency (refresh / re-click / reconnect) | ✅
`landing_session_id` + `markLandingDelivered` |
| §4.1 No-query, specialist alive | ✅ Phase 5 empty-text branch (no
send, still lands on chat page) |
| §4.2 Specialist missing / unavailable / hire failure | ✅ Explicit
`onSwitchAgent(null)` on every fallback path |
| Defensive: malformed localStorage shape | ✅ Read-time sanitization |
| Defensive: catalog fetch failure | ✅ 8s timeout fallback |
| Defensive: `refreshUserAgentsCache` transient failure | ✅ Isolated;
doesn't trigger main-agent fallback |

## Deferred

These ECA-641 requirements are NOT in this PR — tracked separately:

- **Producer side (`writeLandingContext` caller)** — landing page must
write context on CTA click. No caller currently in `web/src/`; landing
page lives in a different bundle/repo or is unwired.
- **E1–E9 instrumentation** — 9 events with `landing_session_id`
correlation key. Hook has the data; emission needs the events lib wired.
- **Send success/failure telemetry (E7 `initial_query_sent` with
`send_success` / `error_type`)** — `handleSendMessage` currently
swallows errors and shows a toast; needs a contract change to return
success status without breaking call sites that depend on the
swallow-and-toast behavior.

## Test plan

CI gates (all green on `8d059dc0b`):
- ✅ `web-quality / web-quality` (lint + tsc + vitest, 305 tests
including 17 new in `useLandingContextFlow.unit.spec.ts` and 23 in
`landing-context.unit.spec.ts`)
- ✅ `auto-review / auto-review`
- ✅ `codex-review`

Manual smoke (recommended before merge):
- [ ] Land on `/chat?sp=<known_specialist>` with seeded localStorage
context → specialist auto-hired, URL becomes `?agent_id=<sp>`, initial
query appears as a sent user message in that specialist's chat
- [ ] Revisit same URL after delivery → idempotency guard skips re-send
(no duplicate message)
- [ ] `?sp=<unknown_specialist>` (in catalog but not hireable / hire
fails) → URL becomes `/chat` (no agent_id, `?sp=` stripped), Main Agent
receives the prompt
- [ ] `?sp=<X>` with empty/whitespace `initial_query.text` → user lands
on Specialist chat, no message sent
- [ ] Open landing-context tab, then a 2nd tab on same origin during
flow → only one delivers; the other reads delivered marker and skips
- [ ] Tamper localStorage with `{ initial_query: { text: 123 } }` →
context discarded, no crash

## Landing-page integration guide

> This is what a Specialist landing page needs to do for the auto-flow
to pick up its context.

### TL;DR

On the CTA click that sends the user to ZooClaw:

1. Write a `LandingContext` to `localStorage` under the key
`ecap:landingContext`.
2. Navigate to `/chat?sp=<specialist_id>` on the same origin.

That's it. The chat client handles everything else (auth gating, hire,
switch, deliver, cleanup).

### Schema

```ts
// Same-origin write — the chat client reads back from localStorage.
const ctx = {
  specialist_id: 'sp-resume-coach',          // required, must match ?sp= in URL
  initial_query: {
    text: 'Help me draft a resume for ...',  // required, even if empty
                                              // attachments: embed as URLs in `text`
                                              // (markdown image syntax / plain links — chat input renders both)
  },
  source: 'landing-resume-coach-v1',         // free-form; appears in telemetry
  landing_session_id: crypto.randomUUID(),   // MUST be unique per CTA click — drives idempotency
  created_at: Date.now(),                    // epoch ms; 24h TTL applies
}

localStorage.setItem('ecap:landingContext', JSON.stringify(ctx))
window.location.assign('/chat?sp=sp-resume-coach')
```

### Field-by-field contract

| Field | Type | Required | Notes |
|---|---|---|---|
| `specialist_id` | string | ✅ | Must equal the `?sp=` query param on
the destination URL. Mismatch → context discarded. |
| `initial_query.text` | string | ✅ | The full prompt to auto-send.
Variable substitution is **landing-side only** — the chat client
receives it as a finished string. Empty string is allowed: the user
lands on the Specialist chat with no auto-send. |
| `source` | string | recommended | Free-form identifier for the landing
page / variant. Surfaced in telemetry events (E1–E9). Use stable
identifiers like `landing-resume-coach-v1`, not URLs. |
| `landing_session_id` | string | ✅ | Must be **unique per CTA click**.
Drives idempotency: the same `landing_session_id` will only deliver once
across refreshes / re-clicks / reconnects. Use `crypto.randomUUID()` or
a server-generated UUID. **Do NOT reuse** the user's session ID, account
ID, or anything else with non-1:1 cardinality to the click event. |
| `created_at` | number | ✅ | Epoch ms (`Date.now()`). Used as a 24h TTL
safety net to drop zombie contexts from abandoned flows. Stale entries
are silently dropped on read. |

### Attachments

Out of scope for this PR's schema. **Embed as URLs in the `text` field**
— the chat input renders markdown image syntax (`![alt](https://...)`)
inline and shows other URLs as previewable links. If you need a true
file attachment with metadata, that's a follow-up; for now URLs are the
path.

### Behavior the chat client handles for you

- ✅ Gates on auth + onboarding + WebSocket-ready before doing anything
- ✅ Hires the specialist if not already hired (auto-installs, waits for
completion, refreshes user-agents cache)
- ✅ Switches the chat URL to `?agent_id=<specialist_id>` (and strips
`?sp=`) before sending
- ✅ Auto-sends `initial_query.text` as a normal user message in that
specialist's chat
- ✅ Marks the `landing_session_id` delivered in `localStorage` so
refresh / re-click is a no-op
- ✅ Falls back to Main Agent if specialist is missing from catalog, hire
fails, or catalog fetch persistently fails (8s timeout)
- ✅ Clears `ecap:landingContext` after the flow completes — landing page
does NOT need to clean up

### What landing-page code should NOT do

- ❌ Don't read or clear `ecap:landingContext` after writing it — that's
the chat client's job.
- ❌ Don't reuse a `landing_session_id` across CTA clicks — generate a
fresh one each time, or all subsequent clicks will be silently skipped
as "already delivered."
- ❌ Don't put attachment metadata in a separate field — schema only
carries `text` for now. Inline URLs into the text.
- ❌ Don't write to a different storage backend (cookie, sessionStorage,
IndexedDB) — the chat client only reads
`localStorage['ecap:landingContext']`.
- ❌ Don't navigate cross-origin between the write and the read —
`localStorage` is per-origin.

### Telemetry events the producer is expected to emit (out of scope
here, see Deferred)

Per ECA-641 §埋点需求, the landing page is responsible for E1
(`landing_page_view`) and E2 (`landing_cta_click`); the chat client owns
E3–E9. The `landing_session_id` is the correlation key that joins them.

---------

Co-authored-by: vincent-srp <vincent@srp.one>
Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>

PR Description:
## Summary

Implements the chat-side of [ECA-641](https://linear.app/srpone/issue/ECA-641/web-specialist-落地页用户信息延续与初始-query-投递): when a user arrives at `/chat?sp=<specialist_id>` from a Specialist landing page with matching localStorage context, the chat client auto-hires the specialist (if needed), switches to it, and delivers the initial query — all gated behind auth + onboarding + chat-ready, with an explicit Main-Agent fallback for failure paths.

The producer side (landing-page `writeLandingContext` caller, E1–E9 instrumentation, send success/failure telemetry) is out of scope for this PR — see [Deferred](#deferred) below.

## Files

- **`web/src/lib/landing-context.ts`** — context schema + storage helpers
  - `localStorage` (not session) so context survives any new-tab/window hop in the auth flow per ECA-641 §2's "全程延续" target
  - 24h TTL via `created_at` field — drops zombie contexts from abandoned flows; missing `created_at` is treated as fresh for backwards-compat with older landing-page writes
  - Cross-validates URL `?sp=` against stored `specialist_id` (mismatch → discard)
  - Sanitizes nested fields (`initial_query.text`, `source`, `created_at`) on read — localStorage is user-tamperable, so a malformed payload like `{ initial_query: { text: 123 } }` is coerced to `{ text: '' }` instead of crashing Phase 5 at `.trim()`
  - Idempotency via `markLandingDelivered(landing_session_id)` — also in localStorage so the marker follows the user across tabs

- **`web/src/app/[locale]/chat/hooks/useLandingContextFlow.ts`** — 6-phase state machine
  ```
  idle → awaiting_auth → awaiting_chat_ready → hiring → delivering → completed
  ```
  - **Phase 3 catalog gates** — holds while `catalogLoading`; holds while `catalogItems.length === 0` (`useOfficialAgentCatalog` swallows fetch errors and surfaces them as `items=[] + isLoading=false`, indistinguishable from a genuinely-empty catalog at read time); **Phase 3b** schedules an 8s safety-net timeout so we don't hang forever on a persistent catalog outage. Mirrors `useDeepLinkHireFlow`'s pattern.
  - **Phase 4 hire** — `installOpenClawAgentAsync` + `waitForOpenClawAgentOperation` are part of the hire transaction; `refreshUserAgentsCache` is wrapped in its own try/catch so a transient `/users/me/agents` GET failure doesn't get misclassified as install failure (would otherwise route the prompt to Main Agent even though the specialist IS hired server-side).
  - **Phase 5 delivery gate** — `currentAgentId !== state.resolvedAgentId` blocks delivery until `router.replace` propagates and `handleSendMessage`'s closure rebuilds with the new `agentId`/`sessionKey`. Treating `null` as "main agent" on both sides means fallback paths also wait for the URL to switch before sending.
  - **ECA-641 §4.2 Main-Agent fallback** — fallback paths (specialist not in catalog, hire failure, catalog-empty timeout) all call `onSwitchAgent(null)` explicitly, which routes through `router.replace('/chat')`. This both routes the user to a working chat surface AND strips `?sp=` from the URL.
  - **Best-effort delivery** — both `.then` and `.catch` branches mark delivered + clear context. Intentional: `handleSendMessage` swallows errors and surfaces them via toast, so the auto-flow doesn't retry; the user manually retries via the chat input. Prevents retry loops in degenerate failure modes.
  - **Latched `canUseChatEver` / `isChatReadyEver`** — both signals oscillate during post-login resolution and may never both be `true` at the same instant; latching converts the gate to a monotonic "has been true at least once this session" predicate. Mirrors `useDeepLinkHireFlow`.

- **`web/src/app/[locale]/chat/GenClawClient.tsx`** — integration
  - Wires the hook with `searchParams`, `agentId` (as `currentAgentId`), and existing handlers
  - `handleLandingSwitchAgent(agentId | null)` — `null` ⇒ Main Agent ⇒ `router.replace('/chat')`; non-null ⇒ `router.replace('/chat?agent_id=...')`. Either way the entire query string is overwritten, so `?sp=` is stripped on completion.
  - Coexists with existing `useDeepLinkHireFlow` (different URL param: `sp` vs `agent_id`).

## ECA-641 spec coverage

| Spec section | Status |
|---|---|
| §1 specialist_id + initial_query.text + source + landing_session_id | ✅ |
| §1 initial_query.attachments | ⏭️ Embedded as URLs in `text` per direction (no separate field; chat input renders markdown) |
| §2 cross-stage persistence (登录前 / 注册中 / 注册后 / Onboarding) | ✅ localStorage + 24h TTL |
| §3.1 Specialist hire prerequisite | ✅ Phase 4 |
| §3.2 Auto-land on Specialist chat | ✅ `onSwitchAgent` + URL switch |
| §3.3 Auto-send initial query | ✅ Phase 5 |
| §3.3 Idempotency (refresh / re-click / reconnect) | ✅ `landing_session_id` + `markLandingDelivered` |
| §4.1 No-query, specialist alive | ✅ Phase 5 empty-text branch (no send, still lands on chat page) |
| §4.2 Specialist missing / unavailable / hire failure | ✅ Explicit `onSwitchAgent(null)` on every fallback path |
| Defensive: malformed localStorage shape | ✅ Read-time sanitization |
| Defensive: catalog fetch failure | ✅ 8s timeout fallback |
| Defensive: `refreshUserAgentsCache` transient failure | ✅ Isolated; doesn't trigger main-agent fallback |

## Deferred

These ECA-641 requirements are NOT in this PR — tracked separately:

- **Producer side (`writeLandingContext` caller)** — landing page must write context on CTA click. No caller currently in `web/src/`; landing page lives in a different bundle/repo or is unwired.
- **E1–E9 instrumentation** — 9 events with `landing_session_id` correlation key. Hook has the data; emission needs the events lib wired.
- **Send success/failure telemetry (E7 `initial_query_sent` with `send_success` / `error_type`)** — `handleSendMessage` currently swallows errors and shows a toast; needs a contract change to return success status without breaking call sites that depend on the swallow-and-toast behavior.

## Test plan

CI gates (all green on `8d059dc0b`):
- ✅ `web-quality / web-quality` (lint + tsc + vitest, 305 tests including 17 new in `useLandingContextFlow.unit.spec.ts` and 23 in `landing-context.unit.spec.ts`)
- ✅ `auto-review / auto-review`
- ✅ `codex-review`

Manual smoke (recommended before merge):
- [ ] Land on `/chat?sp=<known_specialist>` with seeded localStorage context → specialist auto-hired, URL becomes `?agent_id=<sp>`, initial query appears as a sent user message in that specialist's chat
- [ ] Revisit same URL after delivery → idempotency guard skips re-send (no duplicate message)
- [ ] `?sp=<unknown_specialist>` (in catalog but not hireable / hire fails) → URL becomes `/chat` (no agent_id, `?sp=` stripped), Main Agent receives the prompt
- [ ] `?sp=<X>` with empty/whitespace `initial_query.text` → user lands on Specialist chat, no message sent
- [ ] Open landing-context tab, then a 2nd tab on same origin during flow → only one delivers; the other reads delivered marker and skips
- [ ] Tamper localStorage with `{ initial_query: { text: 123 } }` → context discarded, no crash

## Landing-page integration guide

> This is what a Specialist landing page needs to do for the auto-flow to pick up its context.

### TL;DR

On the CTA click that sends the user to ZooClaw:

1. Write a `LandingContext` to `localStorage` under the key `ecap:landingContext`.
2. Navigate to `/chat?sp=<specialist_id>` on the same origin.

That's it. The chat client handles everything else (auth gating, hire, switch, deliver, cleanup).

### Schema

```ts
// Same-origin write — the chat client reads back from localStorage.
const ctx = {
  specialist_id: 'sp-resume-coach',          // required, must match ?sp= in URL
  initial_query: {
    text: 'Help me draft a resume for ...',  // required, even if empty
                                              // attachments: embed as URLs in `text`
                                              // (markdown image syntax / plain links — chat input renders both)
  },
  source: 'landing-resume-coach-v1',         // free-form; appears in telemetry
  landing_session_id: crypto.randomUUID(),   // MUST be unique per CTA click — drives idempotency
  created_at: Date.now(),                    // epoch ms; 24h TTL applies
}

localStorage.setItem('ecap:landingContext', JSON.stringify(ctx))
window.location.assign('/chat?sp=sp-resume-coach')
```

### Field-by-field contract

| Field | Type | Required | Notes |
|---|---|---|---|
| `specialist_id` | string | ✅ | Must equal the `?sp=` query param on the destination URL. Mismatch → context discarded. |
| `initial_query.text` | string | ✅ | The full prompt to auto-send. Variable substitution is **landing-side only** — the chat client receives it as a finished string. Empty string is allowed: the user lands on the Specialist chat with no auto-send. |
| `source` | string | recommended | Free-form identifier for the landing page / variant. Surfaced in telemetry events (E1–E9). Use stable identifiers like `landing-resume-coach-v1`, not URLs. |
| `landing_session_id` | string | ✅ | Must be **unique per CTA click**. Drives idempotency: the same `landing_session_id` will only deliver once across refreshes / re-clicks / reconnects. Use `crypto.randomUUID()` or a server-generated UUID. **Do NOT reuse** the user's session ID, account ID, or anything else with non-1:1 cardinality to the click event. |
| `created_at` | number | ✅ | Epoch ms (`Date.now()`). Used as a 24h TTL safety net to drop zombie contexts from abandoned flows. Stale entries are silently dropped on read. |

### Attachments

Out of scope for this PR's schema. **Embed as URLs in the `text` field** — the chat input renders markdown image syntax (`![alt](https://...)`) inline and shows other URLs as previewable links. If you need a true file attachment with metadata, that's a follow-up; for now URLs are the path.

### Behavior the chat client handles for you

- ✅ Gates on auth + onboarding + WebSocket-ready before doing anything
- ✅ Hires the specialist if not already hired (auto-installs, waits for completion, refreshes user-agents cache)
- ✅ Switches the chat URL to `?agent_id=<specialist_id>` (and strips `?sp=`) before sending
- ✅ Auto-sends `initial_query.text` as a normal user message in that specialist's chat
- ✅ Marks the `landing_session_id` delivered in `localStorage` so refresh / re-click is a no-op
- ✅ Falls back to Main Agent if specialist is missing from catalog, hire fails, or catalog fetch persistently fails (8s timeout)
- ✅ Clears `ecap:landingContext` after the flow completes — landing page does NOT need to clean up

### What landing-page code should NOT do

- ❌ Don't read or clear `ecap:landingContext` after writing it — that's the chat client's job.
- ❌ Don't reuse a `landing_session_id` across CTA clicks — generate a fresh one each time, or all subsequent clicks will be silently skipped as "already delivered."
- ❌ Don't put attachment metadata in a separate field — schema only carries `text` for now. Inline URLs into the text.
- ❌ Don't write to a different storage backend (cookie, sessionStorage, IndexedDB) — the chat client only reads `localStorage['ecap:landingContext']`.
- ❌ Don't navigate cross-origin between the write and the read — `localStorage` is per-origin.

### Telemetry events the producer is expected to emit (out of scope here, see Deferred)

Per ECA-641 §埋点需求, the landing page is responsible for E1 (`landing_page_view`) and E2 (`landing_cta_click`); the chat client owns E3–E9. The `landing_session_id` is the correlation key that joins them.
