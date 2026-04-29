# ecap-workspace commits — 2026-04-28

**共 22 个 commit**

---

## fix(api): remove debug endpoints that expose sensitive system data (#1449)

- **SHA**: `351f0e3d44c4103bedd713a26d8ea8d810683bc6`

- **作者**: tim-srp

- **时间**: 2026-04-28T13:24:33Z


### 完整 Commit Message
```
fix(api): remove debug endpoints that expose sensitive system data (#1449)

## Summary
- Remove `/admin/settings`, `/admin/manifest`, `/admin/sysinfo`
endpoints that expose sensitive data (env vars, config secrets, system
metadata) without authentication
- Clean up unused `PrettyJSONResponse` class and commented-out GPU code
- Remove corresponding unit tests for deleted endpoints

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify `/` heartbeat still responds with `{"status": "ok"}`
- [ ] Confirm `/admin/sysinfo`, `/admin/settings`, `/admin/manifest`
return 404

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```


### PR #1449 Body
## Summary
- Remove `/admin/settings`, `/admin/manifest`, `/admin/sysinfo` endpoints that expose sensitive data (env vars, config secrets, system metadata) without authentication
- Clean up unused `PrettyJSONResponse` class and commented-out GPU code
- Remove corresponding unit tests for deleted endpoints

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify `/` heartbeat still responds with `{"status": "ok"}`
- [ ] Confirm `/admin/sysinfo`, `/admin/settings`, `/admin/manifest` return 404

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## fix(web): add gift-codes to ADMIN_ROUTES middleware guard (#1448)

- **SHA**: `3e036047d76cb9d0a4009799962da92e0ab775bb`

- **作者**: tim-srp

- **时间**: 2026-04-28T12:53:41Z


### 完整 Commit Message
```
fix(web): add gift-codes to ADMIN_ROUTES middleware guard (#1448)

## Summary
- Same byte-for-byte twin pattern as #1442 (subscription-codes):
`/api/admin/gift-codes/{list,create}` BFF handlers proxy to
`/admin/gift-codes`, whose backend `Depends(require_admin_user)` rejects
non-admins, but the BFF middleware was silently letting requests through
because the routes weren't whitelisted in `ADMIN_ROUTES` /
`UID_VALIDATION_EXEMPT`.
- Adds 4 lines (2 in each list) so the BFF returns a deterministic 403
for non-admins / CF-Access-rejected requests instead of falling through
to a `response.json()` parse failure caught as 500.

## Why this was missed in #1442
There's no enforcement that `ADMIN_ROUTES` stays in sync with
`web/src/app/api/admin/**/route.ts` — each new admin page has to
remember to update the whitelist by hand, and the existing
`isAdminRoute` unit tests only spot-check 4 specific routes rather than
asserting the full file-tree ↔ list parity. A follow-up to add that
guard would prevent the next occurrence; tracked separately.

## Test plan
- [ ] Manual: log in as a non-admin user, hit the admin gift-codes page
→ expect BFF 403 "Admin access required" (previously: 500 "Failed to
list gift codes" via the JSON-parse-error path)
- [ ] Admin user: page continues to work (BFF now performs an extra
`/users/get` permission check before proxying)
- [ ] CI: `code-quality / lint-and-test` passes (lint already green
locally)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```


### PR #1448 Body
## Summary
- Same byte-for-byte twin pattern as #1442 (subscription-codes): `/api/admin/gift-codes/{list,create}` BFF handlers proxy to `/admin/gift-codes`, whose backend `Depends(require_admin_user)` rejects non-admins, but the BFF middleware was silently letting requests through because the routes weren't whitelisted in `ADMIN_ROUTES` / `UID_VALIDATION_EXEMPT`.
- Adds 4 lines (2 in each list) so the BFF returns a deterministic 403 for non-admins / CF-Access-rejected requests instead of falling through to a `response.json()` parse failure caught as 500.

## Why this was missed in #1442
There's no enforcement that `ADMIN_ROUTES` stays in sync with `web/src/app/api/admin/**/route.ts` — each new admin page has to remember to update the whitelist by hand, and the existing `isAdminRoute` unit tests only spot-check 4 specific routes rather than asserting the full file-tree ↔ list parity. A follow-up to add that guard would prevent the next occurrence; tracked separately.

## Test plan
- [ ] Manual: log in as a non-admin user, hit the admin gift-codes page → expect BFF 403 "Admin access required" (previously: 500 "Failed to list gift codes" via the JSON-parse-error path)
- [ ] Admin user: page continues to work (BFF now performs an extra `/users/get` permission check before proxying)
- [ ] CI: `code-quality / lint-and-test` passes (lint already green locally)

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## refactor(ios): Replace ScrollView chat with UICollectionView and fix recording panel navigation (#1423)

- **SHA**: `3b2122200984913186ab27370de61433eca505b6`

- **作者**: bill-srp

- **时间**: 2026-04-28T12:25:19Z


### 完整 Commit Message
```
refactor(ios): Replace ScrollView chat with UICollectionView and fix recording panel navigation (#1423)

## Summary

**Scope after split:** the ASR cancel flow (recording panel UX, WS
cancel event, late-frame guards, audio serialization) was extracted to
**#1443** to keep this PR under the 2000-line review limit. This PR is
now solely the chat-list migration plus its surrounding fixes.

- **UICollectionView chat migration**: Replace `ScrollView` +
`LazyVStack` with a `UICollectionView`-backed `ChatMessageList` using
the ChatLayout library for bottom-anchored chat scroll. Fixes scroll
jank, prepend jumps, and keyboard inset issues.
- **Streaming hygiene**: clear `streamingPostId` on new posts, on user
`sendMessage`, and after an idle timeout (Mattermost's `post_edited` has
no terminal frame). Refresh just-finished streaming cells so URL
preprocessing runs and links become clickable.
- **Pagination guards**: add `isLoadingMore` reentry guard and
`hasReachedHistoryStart` exhaustion guard to `loadMoreHistory`,
preventing scroll-near-top from re-firing the same empty cursor.
- **Scroll-to-bottom coalescing**: drop the early-return on
`scrollToBottomTrigger` so SwiftUI-coalesced (messages + trigger)
updates don't skip the snapshot apply.
- **UIHostingConfiguration env trapdoor**: re-apply `\.mattermostToken`
inside the cell's hosting block — the outer SwiftUI environment does NOT
propagate, so image/audio loaders were running unauthenticated.
- **Reaction cell fix**: suppress animation on reaction cell reload to
prevent layout jumps.
- **Version bump**: 1.6.0 (build 1).

## Companion PR

- **#1443** — `feat(ios): add ASR cancel flow with late-frame and
audio-race guards` (extracted from this PR; depends on backend #1428).

## Test plan

- [ ] Chat scroll loads at bottom, auto-scrolls on new messages
- [ ] Scroll-to-bottom button works (including coalesced send + tap)
- [ ] Pagination loads older messages without scroll jump
- [ ] Keyboard dismiss on tap and scroll
- [ ] Reaction add/remove updates without animation glitch
- [ ] Streamed bot reply: links become clickable after stream ends
- [ ] Images/audio in bot replies load (auth token reaches the cell)
- [ ] After last `post_edited`, `streamingPostId` clears within ~2s even
if no follow-up post arrives
```


### PR #1423 Body
## Summary

**Scope after split:** the ASR cancel flow (recording panel UX, WS cancel event, late-frame guards, audio serialization) was extracted to **#1443** to keep this PR under the 2000-line review limit. This PR is now solely the chat-list migration plus its surrounding fixes.

- **UICollectionView chat migration**: Replace `ScrollView` + `LazyVStack` with a `UICollectionView`-backed `ChatMessageList` using the ChatLayout library for bottom-anchored chat scroll. Fixes scroll jank, prepend jumps, and keyboard inset issues.
- **Streaming hygiene**: clear `streamingPostId` on new posts, on user `sendMessage`, and after an idle timeout (Mattermost's `post_edited` has no terminal frame). Refresh just-finished streaming cells so URL preprocessing runs and links become clickable.
- **Pagination guards**: add `isLoadingMore` reentry guard and `hasReachedHistoryStart` exhaustion guard to `loadMoreHistory`, preventing scroll-near-top from re-firing the same empty cursor.
- **Scroll-to-bottom coalescing**: drop the early-return on `scrollToBottomTrigger` so SwiftUI-coalesced (messages + trigger) updates don't skip the snapshot apply.
- **UIHostingConfiguration env trapdoor**: re-apply `\.mattermostToken` inside the cell's hosting block — the outer SwiftUI environment does NOT propagate, so image/audio loaders were running unauthenticated.
- **Reaction cell fix**: suppress animation on reaction cell reload to prevent layout jumps.
- **Version bump**: 1.6.0 (build 1).

## Companion PR

- **#1443** — `feat(ios): add ASR cancel flow with late-frame and audio-race guards` (extracted from this PR; depends on backend #1428).

## Test plan

- [ ] Chat scroll loads at bottom, auto-scrolls on new messages
- [ ] Scroll-to-bottom button works (including coalesced send + tap)
- [ ] Pagination loads older messages without scroll jump
- [ ] Keyboard dismiss on tap and scroll
- [ ] Reaction add/remove updates without animation glitch
- [ ] Streamed bot reply: links become clickable after stream ends
- [ ] Images/audio in bot replies load (auth token reaches the cell)
- [ ] After last `post_edited`, `streamingPostId` clears within ~2s even if no follow-up post arrives



---

## fix(web): redirect after /new in agent update flow (#1447)

- **SHA**: `9455b9e43a94527a98f66696e2638e3eb63bbd31`

- **作者**: nolan-srp

- **时间**: 2026-04-28T12:12:21Z


### 完整 Commit Message
```
fix(web): redirect after /new in agent update flow (#1447)

## Summary
- navigate to the agent chat page after the update success modal sends
/new
- align both agents manager entry points on the same post-reset behavior
- keep the update flow focused on the refreshed agent session
```


### PR #1447 Body
## Summary
- navigate to the agent chat page after the update success modal sends /new
- align both agents manager entry points on the same post-reset behavior
- keep the update flow focused on the refreshed agent session



---

## fix(claw-interface): close Apple clients on shutdown (#1445)

- **SHA**: `0a916b37e1dc2edae8319a06ef7e930a1a226cac`

- **作者**: nolan-srp

- **时间**: 2026-04-28T11:40:46Z


### 完整 Commit Message
```
fix(claw-interface): close Apple clients on shutdown (#1445)

## Summary
- close AppleService API clients during application shutdown so
underlying aiohttp sessions are released
- add AppleService close helpers that handle SDK close methods and
session fallbacks
- cover the shutdown path and client cleanup behavior with focused unit
coverage
```


### PR #1445 Body
## Summary
- close AppleService API clients during application shutdown so underlying aiohttp sessions are released
- add AppleService close helpers that handle SDK close methods and session fallbacks
- cover the shutdown path and client cleanup behavior with focused unit coverage




---

## fix(claw-interface): remove ending_at from subscription code billing call (#1444)

- **SHA**: `d985a34016459cf1983bcc8d4c1d66343176f39a`

- **作者**: bryce-srp

- **时间**: 2026-04-28T11:22:57Z


### 完整 Commit Message
```
fix(claw-interface): remove ending_at from subscription code billing call (#1444)

## Summary
- Remove `ending_at` parameter from `billing_client.subscribe()` call in
subscription code redemption path
- Aligns with all other subscribe call sites (billing init, subscription
manager, Stripe entitlement) which already omit `ending_at`
- Subscription expiry is managed by cron terminate via MongoDB
`subscription_end_time` — passing `ending_at` to BG caused redundant
auto-termination

## Context
All 21 BG subscriptions with `ending_at` set (April 24-28) were traced
to subscription code redemptions (`ZC-*` codes, mostly ultra tier). This
was the last call site still passing `ending_at` to Billing Gateway.

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify existing subscription code tests still pass
- [ ] Redeem a test subscription code on staging — confirm BG
subscription is created without `ending_at`

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```


### PR #1444 Body
## Summary
- Remove `ending_at` parameter from `billing_client.subscribe()` call in subscription code redemption path
- Aligns with all other subscribe call sites (billing init, subscription manager, Stripe entitlement) which already omit `ending_at`
- Subscription expiry is managed by cron terminate via MongoDB `subscription_end_time` — passing `ending_at` to BG caused redundant auto-termination

## Context
All 21 BG subscriptions with `ending_at` set (April 24-28) were traced to subscription code redemptions (`ZC-*` codes, mostly ultra tier). This was the last call site still passing `ending_at` to Billing Gateway.

## Test plan
- [ ] CI passes (ruff, pyright, pytest)
- [ ] Verify existing subscription code tests still pass
- [ ] Redeem a test subscription code on staging — confirm BG subscription is created without `ending_at`

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## fix(claw-interface): ensure billing initialized before bot creation (#1432)

- **SHA**: `ee2f2abee20b8e02a67c3f06221037d163ceaf49`

- **作者**: bryce-srp

- **时间**: 2026-04-28T11:22:51Z


### 完整 Commit Message
```
fix(claw-interface): ensure billing initialized before bot creation (#1432)

## Summary
- Bot creation fails with "team_key missing in MongoDB" when billing
init silently failed during signup
- Added `ensure_billing_initialized()` call before Case 3 (no bot →
create) in `/openclaw/init`
- Same pattern already used in `/user/get`, `/user/create`,
`/credits/*`, `/orders/*`

## Root cause
- `POST /user/create` calls `ensure_billing_initialized()` but
fail-opens on Billing Gateway errors
- User ends up with `billing_initialized=False`, `team_key=None`
- Frontend immediately calls `POST /openclaw/init` → bot creation needs
`team_key` → fails
- 3 users affected in 14 days (4/23 and 4/27)

## Test plan
- [ ] CI passes (pyright + pytest)
- [ ] New user signup → bot creation should work even if first billing
init was slow

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```


### PR #1432 Body
## Summary
- Bot creation fails with "team_key missing in MongoDB" when billing init silently failed during signup
- Added `ensure_billing_initialized()` call before Case 3 (no bot → create) in `/openclaw/init`
- Same pattern already used in `/user/get`, `/user/create`, `/credits/*`, `/orders/*`

## Root cause
- `POST /user/create` calls `ensure_billing_initialized()` but fail-opens on Billing Gateway errors
- User ends up with `billing_initialized=False`, `team_key=None`
- Frontend immediately calls `POST /openclaw/init` → bot creation needs `team_key` → fails
- 3 users affected in 14 days (4/23 and 4/27)

## Test plan
- [ ] CI passes (pyright + pytest)
- [ ] New user signup → bot creation should work even if first billing init was slow

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## fix(web): add subscription-codes to ADMIN_ROUTES middleware guard (#1442)

- **SHA**: `af5acef7637753d9f7da21ebe95945d2e6afb85a`

- **作者**: tim-srp

- **时间**: 2026-04-28T11:25:32Z


### 完整 Commit Message
```
fix(web): add subscription-codes to ADMIN_ROUTES middleware guard (#1442)

## Summary
- Add `/api/admin/subscription-codes/list` and
`/api/admin/subscription-codes/create` to `ADMIN_ROUTES` and
`UID_VALIDATION_EXEMPT` in `auth-middleware.ts`

## Root Cause
These two endpoints were missing from the middleware's admin route guard
list. When the BFF's `proxyToBackend` call fails (e.g. transient network
issue to backend), routes **in** `ADMIN_ROUTES` fail with a clean 403
JSON from the middleware's fail-closed admin check, while routes **not**
in the list bypass that check entirely — the BFF handler's catch block
returns a 500, which Cloudflare's edge replaces with an HTML error page,
causing the frontend JSON parse to fail with `Unexpected token '<'`.

## Test plan
- [ ] CI passes
- [ ] Deploy to staging → open Admin Dashboard → Subscription Code tab
loads correctly
- [ ] Verify non-admin users get 403 (not 500) when accessing these
endpoints

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```


### PR #1442 Body
## Summary
- Add `/api/admin/subscription-codes/list` and `/api/admin/subscription-codes/create` to `ADMIN_ROUTES` and `UID_VALIDATION_EXEMPT` in `auth-middleware.ts`

## Root Cause
These two endpoints were missing from the middleware's admin route guard list. When the BFF's `proxyToBackend` call fails (e.g. transient network issue to backend), routes **in** `ADMIN_ROUTES` fail with a clean 403 JSON from the middleware's fail-closed admin check, while routes **not** in the list bypass that check entirely — the BFF handler's catch block returns a 500, which Cloudflare's edge replaces with an HTML error page, causing the frontend JSON parse to fail with `Unexpected token '<'`.

## Test plan
- [ ] CI passes
- [ ] Deploy to staging → open Admin Dashboard → Subscription Code tab loads correctly
- [ ] Verify non-admin users get 403 (not 500) when accessing these endpoints

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## fix(claw-interface): exclude pending orders from billing history (#1438)

- **SHA**: `dd7ff269b0ad81e9118eb001431ab2742db07fdc`

- **作者**: bryce-srp

- **时间**: 2026-04-28T11:18:51Z


### 完整 Commit Message
```
fix(claw-interface): exclude pending orders from billing history (#1438)

## Summary
- Abandoned checkout sessions leave `status=pending` orders in MongoDB
that were never paid
- These showed up in the billing page as real charges (e.g. $240 for a
yearly starter plan)
- Added `exclude_pending` flag to `count_for_uid` and `list_for_uid`
repo methods
- `list_orders` route now uses `exclude_pending=True` so pending orders
don't appear in billing history
- Admin endpoints are unaffected (they don't use these methods)

## Root cause
User clicked "Subscribe Starter Yearly" → order created (pending) →
Stripe checkout never completed → order stuck as pending → billing page
showed $240 charge that doesn't exist in Stripe

## Test plan
- [ ] CI passes (pyright + pytest)
- [ ] Verify billing page no longer shows pending/abandoned orders
- [ ] Verify paid orders still appear correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```


### PR #1438 Body
## Summary
- Abandoned checkout sessions leave `status=pending` orders in MongoDB that were never paid
- These showed up in the billing page as real charges (e.g. $240 for a yearly starter plan)
- Added `exclude_pending` flag to `count_for_uid` and `list_for_uid` repo methods
- `list_orders` route now uses `exclude_pending=True` so pending orders don't appear in billing history
- Admin endpoints are unaffected (they don't use these methods)

## Root cause
User clicked "Subscribe Starter Yearly" → order created (pending) → Stripe checkout never completed → order stuck as pending → billing page showed $240 charge that doesn't exist in Stripe

## Test plan
- [ ] CI passes (pyright + pytest)
- [ ] Verify billing page no longer shows pending/abandoned orders
- [ ] Verify paid orders still appear correctly

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## feat(ios): add ASR cancel flow with late-frame and audio-race guards (#1443)

- **SHA**: `57606deb1c9102fabd4757e92d16462615a70a7f`

- **作者**: bill-srp

- **时间**: 2026-04-28T11:14:19Z


### 完整 Commit Message
```
feat(ios): add ASR cancel flow with late-frame and audio-race guards (#1443)

## Summary

Wires up the iOS side of the ASR cancel flow that pairs with the backend
cancel control message added in #1428. Cancel now reaches the ASR
WebSocket, late frames after cancel no longer leak into the input, and
the recording UI returns to wherever the user came from.

### Changes

- **UX:** `Cancel` from the recording panel now returns to the
originating panel (text input vs. voice idle) instead of always dropping
back to voice idle. Recording UI extracted from `VoiceInputPanel` into a
new `RecordingPanel` to make ownership of recording-state explicit.
- **Protocol:** When the user cancels, the client sends a `cancel` event
over the ASR WebSocket so the server stops billing/processing
immediately (consumes #1428).
- **Late-frame guard:** Final-text frames that arrive after a cancel —
or while the user has already started a new recording — are dropped
instead of being committed to the input.
- **Audio race fix:** Outgoing ASR audio is now serialized behind any
in-flight cancel so the very first audio chunk of a new recording can't
be sent on the previous (cancelling) socket and lost.
- **Tests:** New `VoiceInputCoordinatorTests` covering the cancel paths
plus updated edge-case test for the tightened transcribing-only guard.

## How to test

1. Open chat, tap voice → start recording → **Cancel** while transcript
is still streaming. Expect: returned to whichever panel started the
recording (text or voice idle), no transcript text committed.
2. Cancel mid-recording, then immediately start a new recording. Expect:
no leading audio dropped, no late text from the previous session
appearing in the new transcript.
3. Server side: confirm a `cancel` event is observed on the ASR
WebSocket when the user cancels (via #1428).

## Related

- Backend counterpart: #1428 (ASR realtime WebSocket cancel control
message)

## Checklist

- [x] Conventional commit format on title and commits
- [x] Unit tests added for new behavior (`VoiceInputCoordinatorTests`,
edge cases updated)
- [ ] Manual device verification of golden + race paths
```


### PR #1443 Body
## Summary

Wires up the iOS side of the ASR cancel flow that pairs with the backend cancel control message added in #1428. Cancel now reaches the ASR WebSocket, late frames after cancel no longer leak into the input, and the recording UI returns to wherever the user came from.

### Changes

- **UX:** `Cancel` from the recording panel now returns to the originating panel (text input vs. voice idle) instead of always dropping back to voice idle. Recording UI extracted from `VoiceInputPanel` into a new `RecordingPanel` to make ownership of recording-state explicit.
- **Protocol:** When the user cancels, the client sends a `cancel` event over the ASR WebSocket so the server stops billing/processing immediately (consumes #1428).
- **Late-frame guard:** Final-text frames that arrive after a cancel — or while the user has already started a new recording — are dropped instead of being committed to the input.
- **Audio race fix:** Outgoing ASR audio is now serialized behind any in-flight cancel so the very first audio chunk of a new recording can't be sent on the previous (cancelling) socket and lost.
- **Tests:** New `VoiceInputCoordinatorTests` covering the cancel paths plus updated edge-case test for the tightened transcribing-only guard.

## How to test

1. Open chat, tap voice → start recording → **Cancel** while transcript is still streaming. Expect: returned to whichever panel started the recording (text or voice idle), no transcript text committed.
2. Cancel mid-recording, then immediately start a new recording. Expect: no leading audio dropped, no late text from the previous session appearing in the new transcript.
3. Server side: confirm a `cancel` event is observed on the ASR WebSocket when the user cancels (via #1428).

## Related

- Backend counterpart: #1428 (ASR realtime WebSocket cancel control message)

## Checklist

- [x] Conventional commit format on title and commits
- [x] Unit tests added for new behavior (`VoiceInputCoordinatorTests`, edge cases updated)
- [ ] Manual device verification of golden + race paths



---

## fix(web): escape non-whitelisted chat slash commands (#1440)

- **SHA**: `cf64ac7e70a5a909525ab933e77c45abb6e418c4`

- **作者**: nolan-srp

- **时间**: 2026-04-28T09:32:26Z


### 完整 Commit Message
```
fix(web): escape non-whitelisted chat slash commands (#1440)

## Summary
- escape slash-prefixed chat input by default so plain messages like
`/foo` are sent literally instead of being interpreted as chat commands
- preserve the existing behavior for the supported slash commands
`/new`, `/stop`, and `/reset`
- apply the same normalization when composing a quoted reply
- add focused unit coverage for escaped slash input, whitelisted
commands, whitespace trimming, and quoted replies
```


### PR #1440 Body
## Summary
- escape slash-prefixed chat input by default so plain messages like `/foo` are sent literally instead of being interpreted as chat commands
- preserve the existing behavior for the supported slash commands `/new`, `/stop`, and `/reset`
- apply the same normalization when composing a quoted reply
- add focused unit coverage for escaped slash input, whitelisted commands, whitespace trimming, and quoted replies



---

## revert(web): hide Google Nango connectors in prod + restore gog card; fix Notion category (#1441)

- **SHA**: `ae6868b5fcf5c5d67093cb598a8e037fe09c8f6e`

- **作者**: Leo-srp

- **时间**: 2026-04-28T09:28:57Z


### 完整 Commit Message
```
revert(web): hide Google Nango connectors in prod + restore gog card; fix Notion category (#1441)

## Summary
Two connector-settings adjustments bundled together (both touch the same
UI surface):

### 1. Roll back Google Nango exposure (#1294 partial revert)
- Remove `google-mail`, `google-calendar`, `google-drive`,
`google-sheet`, `youtube` from `PROD_ENABLED_PROVIDERS` so the Nango
cards are hidden in prod again (still visible in non-prod for testing).
- Unwrap the `{!IS_PROD && (…)}` around the **Google Workspace** (legacy
gog CLI) card so it renders in production again.
- Instagram and Facebook (#1434) stay enabled in prod — only the
Google/YouTube portion is rolled back.

### 2. Move Notion from Communication → Productivity (was #1437)
- Notion is a docs/wiki/knowledge tool, but in `AVAILABLE_PROVIDERS` it
was tagged `category: 'communication'`, so the connectors panel rendered
it under **Communication** alongside Slack and Microsoft Teams.
- Reclassify it as `productivity` and move it next to Asana / Airtable /
Figma so the source ordering and category field stay consistent.
- Supersedes #1437 (closing as duplicate).

## Test plan
- [ ] Prod: Google Workspace card (gog CLI) is visible; Gmail / Google
Calendar / Google Drive / Google Sheets / YouTube cards are hidden under
the Connectors section.
- [ ] Non-prod: all Google Nango cards remain visible and connectable
for ongoing testing.
- [ ] In claw-settings, browse connectors by category — Notion now
appears under **Productivity**, not **Communication**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```


### PR #1441 Body
## Summary
Two connector-settings adjustments bundled together (both touch the same UI surface):

### 1. Roll back Google Nango exposure (#1294 partial revert)
- Remove `google-mail`, `google-calendar`, `google-drive`, `google-sheet`, `youtube` from `PROD_ENABLED_PROVIDERS` so the Nango cards are hidden in prod again (still visible in non-prod for testing).
- Unwrap the `{!IS_PROD && (…)}` around the **Google Workspace** (legacy gog CLI) card so it renders in production again.
- Instagram and Facebook (#1434) stay enabled in prod — only the Google/YouTube portion is rolled back.

### 2. Move Notion from Communication → Productivity (was #1437)
- Notion is a docs/wiki/knowledge tool, but in `AVAILABLE_PROVIDERS` it was tagged `category: 'communication'`, so the connectors panel rendered it under **Communication** alongside Slack and Microsoft Teams.
- Reclassify it as `productivity` and move it next to Asana / Airtable / Figma so the source ordering and category field stay consistent.
- Supersedes #1437 (closing as duplicate).

## Test plan
- [ ] Prod: Google Workspace card (gog CLI) is visible; Gmail / Google Calendar / Google Drive / Google Sheets / YouTube cards are hidden under the Connectors section.
- [ ] Non-prod: all Google Nango cards remain visible and connectable for ongoing testing.
- [ ] In claw-settings, browse connectors by category — Notion now appears under **Productivity**, not **Communication**.

🤖 Generated with [Claude Code](https://claude.com/claude-code)




---

## feat(ios): wire tracking user identity into auth flow (#1439)

- **SHA**: `d81500cfb699946c52ac84b9b155ac5a7f04ad98`

- **作者**: Fangmiao-srp

- **时间**: 2026-04-28T09:17:04Z


### 完整 Commit Message
```
feat(ios): wire tracking user identity into auth flow (#1439)

## Summary
- Set AppsFlyer ID as GA4 user property at app launch (device-level,
login-independent)
- Set GA4 + AppsFlyer user ID on session restore and onboarding login
- Clear user ID on sign-out

Depends on #1422 (merged).

## Test plan
- [ ] CI build passes
- [ ] App launch → verify GA4 user property `appsflyer_id` is set
(Firebase DebugView)
- [ ] Login → verify GA4 user_id is set (Firebase DebugView)
- [ ] Login → verify AppsFlyer customerUserID is set (AppsFlyer debug
log)
- [ ] Logout → verify GA4 user_id is cleared
- [ ] Logout → verify AppsFlyer customerUserID is cleared
- [ ] Cold start with existing session → verify user_id is re-set
- [ ] Onboarding new signup → verify user_id is set

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```


### PR #1439 Body
## Summary
- Set AppsFlyer ID as GA4 user property at app launch (device-level, login-independent)
- Set GA4 + AppsFlyer user ID on session restore and onboarding login
- Clear user ID on sign-out

Depends on #1422 (merged).

## Test plan
- [ ] CI build passes
- [ ] App launch → verify GA4 user property `appsflyer_id` is set (Firebase DebugView)
- [ ] Login → verify GA4 user_id is set (Firebase DebugView)
- [ ] Login → verify AppsFlyer customerUserID is set (AppsFlyer debug log)
- [ ] Logout → verify GA4 user_id is cleared
- [ ] Logout → verify AppsFlyer customerUserID is cleared
- [ ] Cold start with existing session → verify user_id is re-set
- [ ] Onboarding new signup → verify user_id is set

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## feat(web): enable Instagram + Facebook connectors in production (#1434)

- **SHA**: `3b23fa862a742b435b877f2a2215bd3f763c21d0`

- **作者**: Leo-srp

- **时间**: 2026-04-28T08:51:04Z


### 完整 Commit Message
```
feat(web): enable Instagram + Facebook connectors in production (#1434)

## Summary
- Add `instagram` and `facebook` to `PROD_ENABLED_PROVIDERS` in
`ConnectorsSection.tsx` so the Nango cards render in claw-settings on
prod.
- Mirrors the Google connector rollout pattern from #1294.

## Pre-deploy check
- Confirm Instagram + Facebook providers are configured in the
**production** Nango instance (OAuth app, scopes, callback URL). Without
that, users clicking *Connect* will hit an OAuth error.

## Test plan
- [ ] Smoke check on staging: Instagram + Facebook cards render in
claw-settings and OAuth flow succeeds end-to-end
- [ ] After deploy, verify the same on production with a test account

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```


### PR #1434 Body
## Summary
- Add `instagram` and `facebook` to `PROD_ENABLED_PROVIDERS` in `ConnectorsSection.tsx` so the Nango cards render in claw-settings on prod.
- Mirrors the Google connector rollout pattern from #1294.

## Pre-deploy check
- Confirm Instagram + Facebook providers are configured in the **production** Nango instance (OAuth app, scopes, callback URL). Without that, users clicking *Connect* will hit an OAuth error.

## Test plan
- [ ] Smoke check on staging: Instagram + Facebook cards render in claw-settings and OAuth flow succeeds end-to-end
- [ ] After deploy, verify the same on production with a test account

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## chore(claw-interface): remove unused fastapi-mcp integration (#1431)

- **SHA**: `791dd37dbc0fc3a026b91d4ccc7eb05e9e7a9727`

- **作者**: tim-srp

- **时间**: 2026-04-28T07:21:56Z


### 完整 Commit Message
```
chore(claw-interface): remove unused fastapi-mcp integration (#1431)

## Summary
- Remove `fastapi-mcp` dependency and all related MCP SSE endpoint logic
- Delete `app/routes/mcp.py` (dead code with only commented-out demo
route) and its tests
- Remove `tags=["mcp"]` from status routes, `include_mcp` param from
`create_app()`, and `.cursor/mcp.json`

## Context
The `/mcp/sse` endpoint was a zero-config demo setup via `fastapi-mcp`,
exposing only 4 read-only admin routes (heartbeat, settings, manifest,
sysinfo) as MCP tools. **No external consumers depend on this endpoint**
— the `.cursor/mcp.json` contained placeholder URLs
(`<YOUR_CLOUDRUN_SERVER_ID>`) that were never configured for production
use. This is intentional removal of unused code, not an API migration.

## Test plan
- [ ] CI `python-code-quality` passes (ruff + pyright + pytest)
- [ ] Verify `/admin/docs` still loads (no missing routes)
- [ ] Confirm heartbeat `/` endpoint still works

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```


### PR #1431 Body
## Summary
- Remove `fastapi-mcp` dependency and all related MCP SSE endpoint logic
- Delete `app/routes/mcp.py` (dead code with only commented-out demo route) and its tests
- Remove `tags=["mcp"]` from status routes, `include_mcp` param from `create_app()`, and `.cursor/mcp.json`

## Context
The `/mcp/sse` endpoint was a zero-config demo setup via `fastapi-mcp`, exposing only 4 read-only admin routes (heartbeat, settings, manifest, sysinfo) as MCP tools. **No external consumers depend on this endpoint** — the `.cursor/mcp.json` contained placeholder URLs (`<YOUR_CLOUDRUN_SERVER_ID>`) that were never configured for production use. This is intentional removal of unused code, not an API migration.

## Test plan
- [ ] CI `python-code-quality` passes (ruff + pyright + pytest)
- [ ] Verify `/admin/docs` still loads (no missing routes)
- [ ] Confirm heartbeat `/` endpoint still works

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## fix(claw-interface): normalize openclaw agent activation (#1433)

- **SHA**: `63fa7ffc0d604d1087ae831779bb9695522b329b`

- **作者**: nolan-srp

- **时间**: 2026-04-28T07:17:58Z


### 完整 Commit Message
```
fix(claw-interface): normalize openclaw agent activation (#1433)

## Summary
- send `Hi` for both newly hired and re-hired OpenClaw agents so
onboarding runs consistently
- allow custom agent archive downloads in pod runtime to follow HTTP
redirects for signed object storage URLs
- add focused unit coverage for the activation message and
redirect-enabled download script behavior
```


### PR #1433 Body
## Summary
- send `Hi` for both newly hired and re-hired OpenClaw agents so onboarding runs consistently
- allow custom agent archive downloads in pod runtime to follow HTTP redirects for signed object storage URLs
- add focused unit coverage for the activation message and redirect-enabled download script behavior



---

## fix(web): reduce backfill_failed Sentry noise — skip hidden tabs, add… (#1424)

- **SHA**: `c4c3a55ba9fc5bdbd7920826e1f8530da9fcd447`

- **作者**: peter-srp

- **时间**: 2026-04-28T06:59:57Z


### 完整 Commit Message
```
fix(web): reduce backfill_failed Sentry noise — skip hidden tabs, add… (#1424)

… timeout, more retries

Addresses ECAP-WEBSITE-AC (122 events, 37 users): "Failed to fetch
(im.ecap.gsmo.ai)" during message backfill after WS reconnect.

Most failures come from backgrounded tabs where the browser throttles
network requests. Three changes:

1. Skip fetchMissedMessages() when tab is hidden — the WS reconnect
handler (onHello) will trigger it again when the tab becomes visible and
the WS re-establishes.

2. Only report backfill_failed to Sentry when navigator.onLine is true —
offline users will recover naturally on reconnect, no need to create
Sentry noise.

3. Increase retry count from 3 to 5 (with exponential backoff up to 8s)
to ride out transient network issues.

4. Add 15s AbortController timeout to MattermostAPIService.request() to
prevent hanging fetches from blocking the retry loop.

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```


### PR #1424 Body
… timeout, more retries

Addresses ECAP-WEBSITE-AC (122 events, 37 users): "Failed to fetch (im.ecap.gsmo.ai)" during message backfill after WS reconnect.

Most failures come from backgrounded tabs where the browser throttles network requests. Three changes:

1. Skip fetchMissedMessages() when tab is hidden — the WS reconnect handler (onHello) will trigger it again when the tab becomes visible and the WS re-establishes.

2. Only report backfill_failed to Sentry when navigator.onLine is true — offline users will recover naturally on reconnect, no need to create Sentry noise.

3. Increase retry count from 3 to 5 (with exponential backoff up to 8s) to ride out transient network issues.

4. Add 15s AbortController timeout to MattermostAPIService.request() to prevent hanging fetches from blocking the retry loop.



---

## fix(web): stop reporting TypeError upload failures to Sentry (#1426)

- **SHA**: `8569f569af1ccae7fa9c396391a771cff5fa0147`

- **作者**: peter-srp

- **时间**: 2026-04-28T06:58:26Z


### 完整 Commit Message
```
fix(web): stop reporting TypeError upload failures to Sentry (#1426)

The Sentry issue "TypeError: Failed to fetch (im.ecap.gsmo.ai)" (122
events, 37 users) is caused by transient network failures during MM file
uploads. The upload path already retries once (api.ts uploadFile) and
the UI shows a retry button on failure — no action needed from the
on-call team.

Skip captureChatError for TypeError (network-level failures). Only
report MattermostError (server/auth issues that indicate real problems).

---------

Co-authored-by: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
```


### PR #1426 Body
The Sentry issue "TypeError: Failed to fetch (im.ecap.gsmo.ai)" (122 events, 37 users) is caused by transient network failures during MM file uploads. The upload path already retries once (api.ts uploadFile) and the UI shows a retry button on failure — no action needed from the on-call team.

Skip captureChatError for TypeError (network-level failures). Only report MattermostError (server/auth issues that indicate real problems).



---

## feat(claw-interface): Add cancel control message to ASR realtime WebSocket (#1428)

- **SHA**: `6b75dff917361f01a15ab5255b5521fcac27abcc`

- **作者**: bill-srp

- **时间**: 2026-04-28T06:54:47Z


### 完整 Commit Message
```
feat(claw-interface): Add cancel control message to ASR realtime WebSocket (#1428)

## Summary

iOS can now abandon an in-flight realtime ASR recording by sending
`{"type":"cancel"}` over the WebSocket. The server commits the upstream
buffer to keep the persistent vllm-asr session in sync (vllm-asr does
not implement `input_audio_buffer.clear`), drops the resulting
transcript, replies with `{"type":"cancelled"}`, and resets so the next
audio chunk opens a fresh buffer on the same upstream connection.

**Protocol**
- New control: `{"type":"cancel"}` from client → `{"type":"cancelled"}`
ack from server
- No `final` is sent; `enhance`/`rewrite` are not invoked
- Subsequent audio chunks reuse the open upstream WS and start a new
`input_audio_buffer.commit` (without `final`) — same lazy-buffer-start
path the first recording uses

**Implementation**
- `UpstreamASRClient.cancel()` — sends `input_audio_buffer.commit,
final: true`, drains the response stream via the existing
`_collect_transcription` helper, discards the text, swallows
`UpstreamError` (best-effort)
- `_handle_cancel` route handler — calls `upstream.cancel()`, acks
client, then `session.reset()` + `upstream.reset()`
- WS docstring updated with the new control message

**Tests**
- 6 unit tests for `UpstreamASRClient.cancel()` covering commit-frame
emission, transcript discard, buffer-state reset, error swallow, and
no-op cases
- 6 unit tests for the route's cancel branch covering ack, no-`final`
guarantee, no enhance/rewrite call, upstream `cancel`+`reset`, no-audio
cancel, and follow-up recording producing a fresh result
- 2 BDD scenarios in `tests/bdd/features/asr.feature` driven through a
real WebSocket via starlette `TestClient` with an in-memory
`_FakeUpstream`

## Test plan

- [ ] CI green: `python-code-quality / build-and-test` (ruff + pyright +
pytest)
- [ ] BDD: with MongoDB up, `TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER=
MONGODB_PASSWORD= pytest tests/bdd/step_defs/test_asr_realtime.py`
- [ ] iOS smoke: start a recording, send `{"type":"cancel"}` mid-stream,
verify `{"type":"cancelled"}` is received and the next recording
produces only the new transcript
- [ ] Idempotent cancel: send `cancel` before any audio chunks, verify
single `cancelled` ack

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```


### PR #1428 Body
## Summary

iOS can now abandon an in-flight realtime ASR recording by sending `{"type":"cancel"}` over the WebSocket. The server commits the upstream buffer to keep the persistent vllm-asr session in sync (vllm-asr does not implement `input_audio_buffer.clear`), drops the resulting transcript, replies with `{"type":"cancelled"}`, and resets so the next audio chunk opens a fresh buffer on the same upstream connection.

**Protocol**
- New control: `{"type":"cancel"}` from client → `{"type":"cancelled"}` ack from server
- No `final` is sent; `enhance`/`rewrite` are not invoked
- Subsequent audio chunks reuse the open upstream WS and start a new `input_audio_buffer.commit` (without `final`) — same lazy-buffer-start path the first recording uses

**Implementation**
- `UpstreamASRClient.cancel()` — sends `input_audio_buffer.commit, final: true`, drains the response stream via the existing `_collect_transcription` helper, discards the text, swallows `UpstreamError` (best-effort)
- `_handle_cancel` route handler — calls `upstream.cancel()`, acks client, then `session.reset()` + `upstream.reset()`
- WS docstring updated with the new control message

**Tests**
- 6 unit tests for `UpstreamASRClient.cancel()` covering commit-frame emission, transcript discard, buffer-state reset, error swallow, and no-op cases
- 6 unit tests for the route's cancel branch covering ack, no-`final` guarantee, no enhance/rewrite call, upstream `cancel`+`reset`, no-audio cancel, and follow-up recording producing a fresh result
- 2 BDD scenarios in `tests/bdd/features/asr.feature` driven through a real WebSocket via starlette `TestClient` with an in-memory `_FakeUpstream`

## Test plan

- [ ] CI green: `python-code-quality / build-and-test` (ruff + pyright + pytest)
- [ ] BDD: with MongoDB up, `TEST_MONGODB_HOST=127.0.0.1 MONGODB_USER= MONGODB_PASSWORD= pytest tests/bdd/step_defs/test_asr_realtime.py`
- [ ] iOS smoke: start a recording, send `{"type":"cancel"}` mid-stream, verify `{"type":"cancelled"}` is received and the next recording produces only the new transcript
- [ ] Idempotent cancel: send `cancel` before any audio chunks, verify single `cancelled` ack

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## feat(billing): retry Lago 5xx + orphan-entitlement monitor (ECA-572) (#1425)

- **SHA**: `edff7b86269967faa92498ca775f287a6552cb52`

- **作者**: kaka-srp

- **时间**: 2026-04-28T06:30:31Z


### 完整 Commit Message
```
feat(billing): retry Lago 5xx + orphan-entitlement monitor (ECA-572) (#1425)

## Summary

Two-layer defense for the silent revenue leak documented in
[ECA-572](https://linear.app/srpone/issue/ECA-572): customer paid
Stripe, claw-interface never granted entitlement, no alarm fires. Root
cause is a Lago internal Postgres deadlock between concurrent
\`subscribe\` and \`wallet_transactions\` calls on the same customer's
wallets — reachable on every paid upgrade.

- **P1 — Retry on Lago 5xx** in \`billing_client.subscribe\` and
\`billing_client.topup_wallet\`. 4 attempts (0.2/0.8/2.0s backoffs),
only on response status 500/502/503/504. Eliminates ~all
deadlock-induced abandonments because PG resolves the deadlock by
killing the loser transaction; the next attempt finds the rows free.
- **P2 — Orphan-entitlement monitor cron** at \`POST
/admin/cron/check-orphaned-entitlements\`. Detects \`status=paid AND
entitlement_granted!=True AND created_time<now-5min\` and pages
PagerDuty (deduped by \`order_id\`). Detection-only; does NOT
auto-reconcile.
- **Foundation — PagerDuty wrapper** at
\`app/services/pagerduty_client.py\`. Generic Events API V2 client;
empty integration key → no-op for local/CI. Never raises — alerting
failure must not propagate.

## Why retry, why no auto-reconcile

- Retry is safe on **5xx response** (definitive rollback signal — Lago
has no idempotency key but PG already killed the txn). Retry is **NOT
safe on ConnectError / ReadTimeout** because the request might have
committed; the orphan cron is the safety net for that case.
- Auto-reconciling from cron would require the same Stripe/MongoDB
context the webhook handler had. Getting that wrong risks duplicate
grants; doing it right is a followup.

## Files

| Layer | Files |
|---|---|
| PagerDuty wrapper | \`app/services/pagerduty_client.py\`,
\`tests/unit/test_pagerduty_client.py\` |
| Retry (P1) | \`app/services/billing_client.py\`,
\`tests/unit/test_billing_client.py\` |
| Orphan cron (P2) | \`app/cron/orphaned_entitlements.py\`,
\`tests/unit/test_orphaned_entitlements_cron.py\`,
\`app/database/orders_repo.py\`, \`tests/unit/test_orders_repo.py\` |
| Endpoint | \`app/routes/admin_cron.py\`,
\`tests/unit/test_admin_cron.py\` |
| Config | \`app/settings.py\` (\`PAGERDUTY_INTEGRATION_KEY\`) |
| Docs | \`docs/cron-triggers.md\` |

## Deployment requirement (NOT in this PR)

\`PAGERDUTY_INTEGRATION_KEY\` must be added to the prod k8s secret and
wired into \`claw-interface-deployment\`. Without it the cron will
detect orphans but pages will be silently dropped (a WARNING is logged
once at startup). See
\`services/claw-interface/kustomize/overlays/production/\`.

External cron scheduler must also be configured to call \`POST
/admin/cron/check-orphaned-entitlements\` every 5 minutes.

## Test plan

- [x] \`ruff check\` + \`ruff format --check\` clean
- [x] \`pyright\` clean
- [x] \`lint-imports\` — 8/8 contracts kept
- [x] All 6 \`scripts/ci-lint/\` guards pass (file length ≤500,
complexity ≤20, deptry, no-collection-strings, importlinter sync)
- [x] 102 unit tests pass across the impacted files: 14 PD wrapper + 13
retry + 16 orders_repo + 7 cron + 8 admin endpoint + 44 existing billing
client
- [x] Pre-commit hooks all pass
- [ ] Smoke test on staging: \`POST
/admin/cron/check-orphaned-entitlements\` returns 202 + cron-run record
visible in \`ecap-cron-runs\`
- [ ] Verify a synthetic 500 from BG triggers exactly 4 attempts in
staging logs

## Followups (separate work)

- Manually remediate \`ORD-20260427-F99576E7\` (\$200 ultra, customer
\`10c458c0-eef7-4ca9-8397-b230aceedea8\`) — refund vs grant decision is
outside this PR's scope.
- Run historical sweep since 4-1 for \`wallet_transactions\` 5xx +
orphan orders to size impact.
- File upstream Lago issue against \`Customers::RefreshWalletsService\`
for deterministic wallet lock order (eliminates deadlock for all
callers).
- Add auto-reconcile to the orphan cron once the manual remediation flow
is well-understood.
```


### PR #1425 Body
## Summary

Two-layer defense for the silent revenue leak documented in [ECA-572](https://linear.app/srpone/issue/ECA-572): customer paid Stripe, claw-interface never granted entitlement, no alarm fires. Root cause is a Lago internal Postgres deadlock between concurrent \`subscribe\` and \`wallet_transactions\` calls on the same customer's wallets — reachable on every paid upgrade.

- **P1 — Retry on Lago 5xx** in \`billing_client.subscribe\` and \`billing_client.topup_wallet\`. 4 attempts (0.2/0.8/2.0s backoffs), only on response status 500/502/503/504. Eliminates ~all deadlock-induced abandonments because PG resolves the deadlock by killing the loser transaction; the next attempt finds the rows free.
- **P2 — Orphan-entitlement monitor cron** at \`POST /admin/cron/check-orphaned-entitlements\`. Detects \`status=paid AND entitlement_granted!=True AND created_time<now-5min\` and pages PagerDuty (deduped by \`order_id\`). Detection-only; does NOT auto-reconcile.
- **Foundation — PagerDuty wrapper** at \`app/services/pagerduty_client.py\`. Generic Events API V2 client; empty integration key → no-op for local/CI. Never raises — alerting failure must not propagate.

## Why retry, why no auto-reconcile

- Retry is safe on **5xx response** (definitive rollback signal — Lago has no idempotency key but PG already killed the txn). Retry is **NOT safe on ConnectError / ReadTimeout** because the request might have committed; the orphan cron is the safety net for that case.
- Auto-reconciling from cron would require the same Stripe/MongoDB context the webhook handler had. Getting that wrong risks duplicate grants; doing it right is a followup.

## Files

| Layer | Files |
|---|---|
| PagerDuty wrapper | \`app/services/pagerduty_client.py\`, \`tests/unit/test_pagerduty_client.py\` |
| Retry (P1) | \`app/services/billing_client.py\`, \`tests/unit/test_billing_client.py\` |
| Orphan cron (P2) | \`app/cron/orphaned_entitlements.py\`, \`tests/unit/test_orphaned_entitlements_cron.py\`, \`app/database/orders_repo.py\`, \`tests/unit/test_orders_repo.py\` |
| Endpoint | \`app/routes/admin_cron.py\`, \`tests/unit/test_admin_cron.py\` |
| Config | \`app/settings.py\` (\`PAGERDUTY_INTEGRATION_KEY\`) |
| Docs | \`docs/cron-triggers.md\` |

## Deployment requirement (NOT in this PR)

\`PAGERDUTY_INTEGRATION_KEY\` must be added to the prod k8s secret and wired into \`claw-interface-deployment\`. Without it the cron will detect orphans but pages will be silently dropped (a WARNING is logged once at startup). See \`services/claw-interface/kustomize/overlays/production/\`.

External cron scheduler must also be configured to call \`POST /admin/cron/check-orphaned-entitlements\` every 5 minutes.

## Test plan

- [x] \`ruff check\` + \`ruff format --check\` clean
- [x] \`pyright\` clean
- [x] \`lint-imports\` — 8/8 contracts kept
- [x] All 6 \`scripts/ci-lint/\` guards pass (file length ≤500, complexity ≤20, deptry, no-collection-strings, importlinter sync)
- [x] 102 unit tests pass across the impacted files: 14 PD wrapper + 13 retry + 16 orders_repo + 7 cron + 8 admin endpoint + 44 existing billing client
- [x] Pre-commit hooks all pass
- [ ] Smoke test on staging: \`POST /admin/cron/check-orphaned-entitlements\` returns 202 + cron-run record visible in \`ecap-cron-runs\`
- [ ] Verify a synthetic 500 from BG triggers exactly 4 attempts in staging logs

## Followups (separate work)

- Manually remediate \`ORD-20260427-F99576E7\` (\$200 ultra, customer \`10c458c0-eef7-4ca9-8397-b230aceedea8\`) — refund vs grant decision is outside this PR's scope.
- Run historical sweep since 4-1 for \`wallet_transactions\` 5xx + orphan orders to size impact.
- File upstream Lago issue against \`Customers::RefreshWalletsService\` for deterministic wallet lock order (eliminates deadlock for all callers).
- Add auto-reconcile to the orphan cron once the manual remediation flow is well-understood.

🤖 Generated with [Claude Code](https://claude.com/claude-code)



---

## fix(chat-replay): use chat-page identity for replay bot name (#1429)

- **SHA**: `08ef4009b73f93115356981ccc77331f4e87c912`

- **作者**: kaka-srp

- **时间**: 2026-04-28T06:25:01Z


### 完整 Commit Message
```
fix(chat-replay): use chat-page identity for replay bot name (#1429)

## Summary

Replay viewers were seeing the bot's frozen MM `display_name`, which can
diverge from what the creator sees in chat. Chat-page identity
resolution factors in **user identity**, **per-agent settings** and
**locale** (via
[`resolveChatIdentity`](web/src/lib/chat/chatIdentity.ts#L34)) — none of
which the backend has direct access to. For renamed bots, customized
user identity, or non-English locales, replay would show a different
name than chat.

## Changes

### Backend
-
[`_resolve_bot()`](services/claw-interface/app/services/chat_replay/create.py#L289):
flip priority so `client_snapshot_meta.bot_name` wins, with user-doc
`display_name` as fallback for legacy clients and ``"Assistant"`` as
terminal fallback. Whitespace-only client names treated as empty.
-
[`ClientSnapshotMeta`](services/claw-interface/app/schema/chat_replay.py#L164):
add Pydantic `max_length` caps (name 80, avatar URL 1024, emoji 64, path
512) — schema-layer 422 is cheaper than service-layer guards. Updated
docstring to reflect display-only role.

### Frontend
-
[`GenClawClient.tsx`](web/src/app/[locale]/chat/GenClawClient.tsx#L567):
plumb `resolvedChatIdentity.{name,avatar}` through `useChatReplayShare`
so the snapshot captures the same string the creator sees.
- Relocated `shareFlow` and its `createError` toast effect to after
`resolvedChatIdentity` is computed (TS scoping).

## Trust model

`client_snapshot_meta.bot_name` is **display-only** metadata — it does
not affect channel ownership, post visibility, or file proxying (all
enforced server-side from refetched MM data). The creator owns the share
and is trusted to label it; length caps limit blast radius.

## Test plan

- [x] 5 new backend tests cover priority flip, fallback chain,
whitespace handling, and length-cap enforcement
- [x] `pytest tests/unit/test_chat_replay_create.py` — 22/22 passing
locally
- [x] All 6 `scripts/ci-lint/0?-*.sh` clean (file-length, import-linter,
complexity, deptry, collection-strings, repo-sync)
- [x] `pnpm tsc --noEmit` and `pnpm eslint GenClawClient.tsx` clean
- [ ] After merge: smoke-test on staging by creating a share with a
renamed bot or non-English locale and confirming the public viewer shows
the same name as chat
```


### PR #1429 Body
## Summary

Replay viewers were seeing the bot's frozen MM `display_name`, which can diverge from what the creator sees in chat. Chat-page identity resolution factors in **user identity**, **per-agent settings** and **locale** (via [`resolveChatIdentity`](web/src/lib/chat/chatIdentity.ts#L34)) — none of which the backend has direct access to. For renamed bots, customized user identity, or non-English locales, replay would show a different name than chat.

## Changes

### Backend
- [`_resolve_bot()`](services/claw-interface/app/services/chat_replay/create.py#L289): flip priority so `client_snapshot_meta.bot_name` wins, with user-doc `display_name` as fallback for legacy clients and ``"Assistant"`` as terminal fallback. Whitespace-only client names treated as empty.
- [`ClientSnapshotMeta`](services/claw-interface/app/schema/chat_replay.py#L164): add Pydantic `max_length` caps (name 80, avatar URL 1024, emoji 64, path 512) — schema-layer 422 is cheaper than service-layer guards. Updated docstring to reflect display-only role.

### Frontend
- [`GenClawClient.tsx`](web/src/app/[locale]/chat/GenClawClient.tsx#L567): plumb `resolvedChatIdentity.{name,avatar}` through `useChatReplayShare` so the snapshot captures the same string the creator sees.
- Relocated `shareFlow` and its `createError` toast effect to after `resolvedChatIdentity` is computed (TS scoping).

## Trust model

`client_snapshot_meta.bot_name` is **display-only** metadata — it does not affect channel ownership, post visibility, or file proxying (all enforced server-side from refetched MM data). The creator owns the share and is trusted to label it; length caps limit blast radius.

## Test plan

- [x] 5 new backend tests cover priority flip, fallback chain, whitespace handling, and length-cap enforcement
- [x] `pytest tests/unit/test_chat_replay_create.py` — 22/22 passing locally
- [x] All 6 `scripts/ci-lint/0?-*.sh` clean (file-length, import-linter, complexity, deptry, collection-strings, repo-sync)
- [x] `pnpm tsc --noEmit` and `pnpm eslint GenClawClient.tsx` clean
- [ ] After merge: smoke-test on staging by creating a share with a renamed bot or non-English locale and confirming the public viewer shows the same name as chat



---

## feat(ios): add TrackingService infrastructure + env isolation (#1422)

- **SHA**: `56523bcc1b10e67eb8c135e32ae4351fdf665ffe`

- **作者**: Fangmiao-srp

- **时间**: 2026-04-28T05:38:13Z


### 完整 Commit Message
```
feat(ios): add TrackingService infrastructure + env isolation (#1422)

## Summary
- Add `TrackingService` with swappable `TrackingBackend` protocol for
GA4 + AppsFlyer dispatch
- Includes `LiveTrackingBackend` (production) and `SpyBackend` (tests)
implementations
- Base params (`app_name`, `platform`, `event_version`) auto-merged into
every GA4 event
- User identity methods: `setUserId` / `clearUserId` /
`setAppsFlyerIdAsUserProperty`
- Skip AppsFlyer SDK init in staging builds (`#if !STAGING`)

This is the infrastructure-only PR. Event functions and their call sites
will follow in a separate PR.

## Test plan
- [x] 3 unit tests for user identity methods (setUserId, clearUserId,
setAppsFlyerIdAsUserProperty)
- [ ] CI build passes
- [ ] Verify staging build does not init AppsFlyer

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.6 <noreply@anthropic.com>
```


### PR #1422 Body
## Summary
- Add `TrackingService` with swappable `TrackingBackend` protocol for GA4 + AppsFlyer dispatch
- Includes `LiveTrackingBackend` (production) and `SpyBackend` (tests) implementations
- Base params (`app_name`, `platform`, `event_version`) auto-merged into every GA4 event
- User identity methods: `setUserId` / `clearUserId` / `setAppsFlyerIdAsUserProperty`
- Skip AppsFlyer SDK init in staging builds (`#if !STAGING`)

This is the infrastructure-only PR. Event functions and their call sites will follow in a separate PR.

## Test plan
- [x] 3 unit tests for user identity methods (setUserId, clearUserId, setAppsFlyerIdAsUserProperty)
- [ ] CI build passes
- [ ] Verify staging build does not init AppsFlyer

🤖 Generated with [Claude Code](https://claude.com/claude-code)


