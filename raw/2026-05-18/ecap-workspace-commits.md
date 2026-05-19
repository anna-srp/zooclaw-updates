# ecap-workspace — 2026-05-18 Commits

## Commit 1: b4ac4d5c — fix(weixin): preserve account index from runtime fallback (#1730)

- **SHA**: b4ac4d5c4ca9f000a0b4d1be183046e6ad4a8cd2
- **Author**: tim-srp
- **Date**: 2026-05-18T14:36:30Z
- **PR**: #1730

### PR #1730 Body

**Summary**
- read the Weixin account index directly through runtime exec instead of the mismatched file API read path
- preserve existing accounts by parsing both raw JSON strings and FastClaw-decoded JSON arrays
- add regression coverage for runtime exec returning `accounts.json` as an already-decoded JSON array

---

## Commit 2: d4452cd2 — fix(web): Await composer resolution before completing landing handoff (#1728)

- **SHA**: d4452cd23916a27d8f11edf55e1249f1ef8c1cd1
- **Author**: bill-srp
- **Date**: 2026-05-18T13:18:14Z
- **PR**: #1728

### PR #1728 Body

**Summary**

- Adds a "composer resolved the prefill" gate to `useLandingContextFlow.ts`. The poll now waits for `GenClawInput` to either *apply* the prefill into its editable state OR *explicitly drop* it before firing `[LandingContextPoll] hand-off complete`.
- Annotates the completion log with `prefillStatus: 'applied' | 'dropped'` so production telemetry distinguishes "user saw their prefill" from "we intentionally preserved their draft".

**Why**: Follow-up to prod traces added in #1724. The traces revealed that `[LandingContextPoll] hand-off complete` fires *before* the textarea visually populates — a user reported seeing the completion log assert success while the composer was still empty.

---

## Commit 3: 7190c28b — feat(ios): 1.7.0 release (#1710)

- **SHA**: 7190c28bf1f7b3e76f0ac1d3abcbdde8e6a73831
- **Author**: bill-srp
- **Date**: 2026-05-18T11:31:52Z
- **PR**: #1710

### PR #1710 Body

**Summary**

iOS v1.7.0 release branch. Mixed UX polish (onboarding hero, sidebar layout, inline document preview), chat reliability fixes.

**Onboarding & sidebar**
- Redesigned onboarding hero with full-bleed welcome video
- Sidebar bottom-nav layout tightened and leading-aligned
- Sidebar agent rows show the last channel message as subtitle
- Content panel gets a hairline outline when the sidebar is open

**Chat**
- Inline document preview via `QLPreviewController` for Mattermost file attachments
- In-content artifact links now route through `QLPreviewController` (Office formats now render)
- Fixed Mattermost chat author filtering (server-side `from_webhook` mismatch)
- Force fresh SwiftUI identity per message to stop cell-recycle bug (assistant bubbles inheriting user text)

---

## Commit 4: 7df6a686 — fix(subscription): decouple topup modal + apple renew + backend gate (#1727)

- **SHA**: 7df6a686bd5b7afaebf24bf92d9055a1cebb0d66
- **Author**: kaka-srp
- **Date**: 2026-05-18T11:26:46Z
- **PR**: #1727

### PR #1727 Body

**Summary**

Three coupled gating bugs in the billing/topup flow:

- **PaymentMethodModal cross-flow leak** — For a Stripe subscriber clicking "Buy Tokens", Alipay was greyed out. Fix: gate disable rules on `Boolean(paymentMethodPending)` so the topup path leaves both methods open.
- **Apple Renew bypass** — An Apple cancel-pending user would see in-app Renew button → Stripe clickable → dual subscription. Fix: mirror the App Store toast.
- **Backend topup gate** — `POST /orders/create` accepted any user, frontend gate bypassable. Fix: mirror the frontend allowed-state set, return 403 when not satisfied.

---

## Commit 5: 12dc9ba6 — fix(web): persist permanent CDN URL for bot avatar uploads (#1725)

- **SHA**: 12dc9ba675fbd54592d3b104c29bf88bd8ad1fba
- **Author**: siqiao-srp
- **Date**: 2026-05-18T10:22:56Z
- **PR**: #1725

### PR #1725 Body

**Summary**
- Bot avatar uploads were persisted as 7-day presigned GET URLs (expiring weekly, leaving broken avatars).
- Introduce a dedicated `bot_avatar` purpose that returns a permanent CDN URL instead.
- Chat-session uploads keep the existing 7-day signed-access behavior.

**Root cause**: `purpose: 'user_upload'` since #245 returns a 7-day presigned URL. Once expired, R2 returns `<Code>ExpiredRequest</Code>`.

---

## Commit 6: 9e10ace4 — feat(web): trace landing prefill flow with prod-visible logs (#1724)

- **SHA**: 9e10ace48740624db7f8fc97970efe6106c6fe8d
- **Author**: bill-srp
- **Date**: 2026-05-18T08:20:00Z
- **PR**: #1724

### PR #1724 Body

**Summary**
- Adds throttled poll-loop traces in `useLandingContextFlow.ts` (gate state, context-read result, decision inputs, URL-strip wait)
- Promotes all landing-context flow `console.log` → `console.warn` so the traces survive Terser's `drop_console` in production builds

**Why**: When a user reports "prefill didn't fire", there's currently no console trail. This PR closes that visibility gap in production.

---

## Commit 7: 7d1fd441 — fix(web): Poll localStorage for landing context prefill (#1723)

- **SHA**: 7d1fd441af2c0b314f5e2b8a011cdaae5bf1bdbf
- **Author**: bill-srp
- **Date**: 2026-05-18T06:43:01Z
- **PR**: #1723

### PR #1723 Body

**Summary**: Replace the event-driven FSM in `useLandingContextFlow` with a 500ms `setInterval` that reads the landing context directly from `localStorage`. The previous hook gated Phase 1 on `?sp=` in the URL, which the new-user redirect chain (OTP verify → onboarding success → payment success) strips along the way; that left first-time visitors with a valid context in storage and a silent no-op in the chat composer.

---

## Commit 8: 970599ba — fix(web): Preserve landing context after delivery (#1708)

- **SHA**: 970599ba3f232a81c7ccccc60cbfb0bee1e2ea47
- **Author**: bill-srp
- **Date**: 2026-05-18T03:00:15Z
- **PR**: #1708

### PR #1708 Body

**Summary**: Stop clearing the localStorage landing context in `useLandingContextFlow`'s Phase 5 cleanup. The `delivered` marker is already the idempotency guard. To prevent a stale post-delivery context from blocking a brand-new visit, `useLandingRedirect.seedLandingContextFromUrl` now re-seeds a fresh context when the existing same-specialist context was already delivered.
