# SerendipityOneInc/ecap-workspace — commits 2026-10-16

## feat(claw-interface): accept audience-bound resource tokens on ASR routes (#4082)

- **SHA**: `85eedd826d90f2a1c3c0cfdb385ce81a0111ea16`
- **作者**: sharplee-srp
- **日期**: 2026-10-16T08:35:01Z
- **PR**: #4082

### Commit Message

```
feat(claw-interface): accept audience-bound resource tokens on ASR routes (#4082)

## Linear
None.

## Summary
Lets the ASR routes accept a short-lived, audience-bound resource token
from the account service's RFC 8693 exchange (`POST
/auth/token-exchange`), besides the session JWT, so native clients such
as the recorder app never send the long-lived session JWT here. Mirrors
ecap-proxy-service PR #212 (`TRANSCRIPTION_RESOURCE_AUDIENCE`).

- **Settings**: `ASR_RESOURCE_AUDIENCE` (batch,
`https://<host>/asr/v1/audio/transcriptions`) and
`ASR_REALTIME_RESOURCE_AUDIENCE` (realtime,
`https://<host>/asr/v1/realtime`; an https URL even though clients use
wss, because the account-service allow-list takes HTTPS URLs). Validated
at settings load: empty disables; otherwise exactly
`https://host[:port]<route path>`. Rejects http/wss, uppercase scheme,
query, fragment, userinfo, whitespace, bad port, trailing slash, any
other path; the two must differ. This service has no MCP
resource-audience setting, so there is nothing else to compare against;
the exact path check already keeps an MCP audience out.
- **Auth**: new `require_asr_token` / `require_asr_realtime_token` in
`app/middleware/auth.py` (L0, return `VerifiedToken`). A bearer whose
unverified payload says `token_use: "resource"` goes only to `GET
/auth/verify-resource?audience=<route URL>` (new
`verify_resource_token`, own per-audience cache, same retry and 401/503
semantics as `verify_user_token`); every other bearer goes to
`/auth/verify`. No fallback between the two. Feature off = exactly the
old behavior.
- **Other routes refuse resource tokens**: `verify_user_token` now
rejects a bearer claiming `token_use=resource` locally with 401 before
calling the account service (which also rejects it, since PyJWT refuses
an `aud`-bearing token when no audience is expected). This is a
deliberate tightening over #212.
- **uid-only callers**: the ASR routes use only the uid (record
persistence); no quota, billing, or user lookups. The account service's
`/auth/verify-resource` already requires a registered user, so no extra
account read is added, matching the session path here (zero DB reads).
- **Refactors**: ASR moves off the legacy `get_current_user` stack; the
router-level `Depends(get_current_user)` is removed (it would refuse
resource tokens), and each endpoint declares its own dependency.
`schedule_ws_persist` and the WS helpers take `uid: str` instead of a
`current_user` dict. The account-service GET + retry is shared by both
verifiers (`_get_with_retry`), keeping the `/auth/verify` call shape
unchanged.

Deliberate choices reviewers may ask about:
- WebSocket auth runs before `accept()`, so a failure is an HTTP
handshake denial (401, or 503 when the account service is unavailable),
not an accepted socket closed with 1008. That is the existing behavior
and the safer one.
- Tokens come from the `Authorization` header only. The route never
supported query-string tokens and still does not.
- The new dependency's missing/malformed-header detail is the L0
contract string (`Missing authentication token`) rather than the legacy
`get_current_user` strings.

Deployment (per environment): add both URLs, byte for byte, to the
account service's `RESOURCE_TOKEN_ALLOWED_AUDIENCES`, then set the two
env vars here. Details in
`services/claw-interface/docs/asr-resource-tokens.md`. Backend-only; no
web change.

## Test plan
- [x] `tests/unit/test_settings_asr_resource_audience.py`: settings
matrix for both fields
- [x] `tests/unit/test_asr_resource_token_auth.py`: auth matrix for both
routes (resource token with exact audience, session token, other
audiences incl. MCP refused without fallback, invalid session token
without resource fallback, 503 on verifier outage, missing/malformed
header, query-string token ignored, WS denial statuses and `ready` on
success), feature off, other routes (L0 and legacy) refuse resource
tokens, `verify_resource_token` HTTP behavior (exact URL/params,
per-audience cache, 401/503, unconfigured), local refusal in
`verify_user_token`
- [x] Existing `test_asr_routes.py`, `test_auth.py`,
`test_middleware_auth_and_org.py`, `test_auth_level_dedup.py` pass
- [x] `bash scripts/verify-py.sh --full` static gates (ruff, ruff
format, pyright, import-linter, ci-lint guards) pass
- [ ] Staging: exchange a token for each audience and call both routes
(needs the account-service allow-list change)
```

### PR Body

## Linear
None.

## Summary
Lets the ASR routes accept a short-lived, audience-bound resource token from the account service's RFC 8693 exchange (`POST /auth/token-exchange`), besides the session JWT, so native clients such as the recorder app never send the long-lived session JWT here. Mirrors ecap-proxy-service PR #212 (`TRANSCRIPTION_RESOURCE_AUDIENCE`).

- **Settings**: `ASR_RESOURCE_AUDIENCE` (batch, `https://<host>/asr/v1/audio/transcriptions`) and `ASR_REALTIME_RESOURCE_AUDIENCE` (realtime, `https://<host>/asr/v1/realtime`; an https URL even though clients use wss, because the account-service allow-list takes HTTPS URLs). Validated at settings load: empty disables; otherwise exactly `https://host[:port]<route path>`. Rejects http/wss, uppercase scheme, query, fragment, userinfo, whitespace, bad port, trailing slash, any other path; the two must differ. This service has no MCP resource-audience setting, so there is nothing else to compare against; the exact path check already keeps an MCP audience out.
- **Auth**: new `require_asr_token` / `require_asr_realtime_token` in `app/middleware/auth.py` (L0, return `VerifiedToken`). A bearer whose unverified payload says `token_use: "resource"` goes only to `GET /auth/verify-resource?audience=<route URL>` (new `verify_resource_token`, own per-audience cache, same retry and 401/503 semantics as `verify_user_token`); every other bearer goes to `/auth/verify`. No fallback between the two. Feature off = exactly the old behavior.
- **Other routes refuse resource tokens**: `verify_user_token` now rejects a bearer claiming `token_use=resource` locally with 401 before calling the account service (which also rejects it, since PyJWT refuses an `aud`-bearing token when no audience is expected). This is a deliberate tightening over #212.
- **uid-only callers**: the ASR routes use only the uid (record persistence); no quota, billing, or user lookups. The account service's `/auth/verify-resource` already requires a registered user, so no extra account read is added, matching the session path here (zero DB reads).
- **Refactors**: ASR moves off the legacy `get_current_user` stack; the router-level `Depends(get_current_user)` is removed (it would refuse resource tokens), and each endpoint declares its own dependency. `schedule_ws_persist` and the WS helpers take `uid: str` instead of a `current_user` dict. The account-service GET + retry is shared by both verifiers (`_get_with_retry`), keeping the `/auth/verify` call shape unchanged.

Deliberate choices reviewers may ask about:
- WebSocket auth runs before `accept()`, so a failure is an HTTP handshake denial (401, or 503 when the account service is unavailable), not an accepted socket closed with 1008. That is the existing behavior and the safer one.
- Tokens come from the `Authorization` header only. The route never supported query-string tokens and still does not.
- The new dependency's missing/malformed-header detail is the L0 contract string (`Missing authentication token`) rather than the legacy `get_current_user` strings.

Deployment (per environment): add both URLs, byte for byte, to the account service's `RESOURCE_TOKEN_ALLOWED_AUDIENCES`, then set the two env vars here. Details in `services/claw-interface/docs/asr-resource-tokens.md`. Backend-only; no web change.

## Test plan
- [x] `tests/unit/test_settings_asr_resource_audience.py`: settings matrix for both fields
- [x] `tests/unit/test_asr_resource_token_auth.py`: auth matrix for both routes (resource token with exact audience, session token, other audiences incl. MCP refused without fallback, invalid session token without resource fallback, 503 on verifier outage, missing/malformed header, query-string token ignored, WS denial statuses and `ready` on success), feature off, other routes (L0 and legacy) refuse resource tokens, `verify_resource_token` HTTP behavior (exact URL/params, per-audience cache, 401/503, unconfigured), local refusal in `verify_user_token`
- [x] Existing `test_asr_routes.py`, `test_auth.py`, `test_middleware_auth_and_org.py`, `test_auth_level_dedup.py` pass
- [x] `bash scripts/verify-py.sh --full` static gates (ruff, ruff format, pyright, import-linter, ci-lint guards) pass
- [ ] Staging: exchange a token for each audience and call both routes (needs the account-service allow-list change)


---

## fix(chat-ui): stop clipping descenders in model picker and turn status labels (#4076)

- **SHA**: `77b995c967b49b584f66a02fc269a2bb021e2125`
- **作者**: Nemo Feng
- **日期**: 2026-10-16T06:22:20Z
- **PR**: #4076

### Commit Message

```
fix(chat-ui): stop clipping descenders in model picker and turn status labels (#4076)

## Summary
Fix chat-ui text that cut off the bottom of descender letters
(`g`/`p`/`y`/`q`/`j`):
- **Model picker** — composer trigger and dropdown rows (e.g. "Gemini 4
Ar**g**on"). `DropdownMenuModelTrigger` / `DropdownMenuModelItem`:
`leading-none` → `leading-4`.
- **User-message turn status** — the status line under a sent message
(e.g. "Thinkin**g**", "Usin**g** web_search"). `UserMessage.tsx` status
row: `leading-none` → `leading-4`.

## Root cause
Both places set `text-xs leading-none` (a 12px line box for 12px text)
on a container whose label clips overflow for ellipsis truncation
(`truncate` / `overflow-hidden text-ellipsis`). Inter's glyph extent
exceeds 1.0em, so descenders render below the 12px box and are clipped
by `overflow: hidden`. `leading-4` gives a 16px line box.

Layout impact:
- Model picker: none — trigger is fixed `h-8`, items are `min-h-8` with
`py-1.5` (12 + 16 = 28 < 32), both `items-center`. Badges keep their own
`leading-none`.
- Turn status: the row has no fixed height, so it grows 12px → 16px (4px
taller line under the message).

A repo-wide sweep for the same pattern (tight line-height + clipping)
found these two plus one marketing-page case (landing rotating role
word, ~0.8px at 52px), which is intentionally left out of this PR. Other
matches (emoji avatars, 1.25-ratio menu rows, badges, display headings)
were measured and do not clip.

## Test plan
- [x] Standalone Chromium repro using the deployed production CSS bundle
+ Inter, exact class strings from source, old vs new; glyph ink measured
against the clip box:
- Model picker, `leading-none`: label `clientHeight` 12 / `scrollHeight`
13 → clipped; `leading-4`: 16 / 16 → not clipped, row/trigger height
unchanged at 32px
- Turn status ("Thinking", "Using web_search", "Failed: typing
pipeline"), `leading-none`: descenders overflow the 12px box by 1px;
`leading-4`: 1px clearance in a 16px box
- [x] `@zooclaw/chat-ui`: vitest (536 passed), eslint, tsc
- [x] `web/app` `OpenClawUserMessage.unit.spec.tsx` (31 passed)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5.5 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
Fix chat-ui text that cut off the bottom of descender letters (`g`/`p`/`y`/`q`/`j`):
- **Model picker** — composer trigger and dropdown rows (e.g. "Gemini 4 Ar**g**on"). `DropdownMenuModelTrigger` / `DropdownMenuModelItem`: `leading-none` → `leading-4`.
- **User-message turn status** — the status line under a sent message (e.g. "Thinkin**g**", "Usin**g** web_search"). `UserMessage.tsx` status row: `leading-none` → `leading-4`.

## Root cause
Both places set `text-xs leading-none` (a 12px line box for 12px text) on a container whose label clips overflow for ellipsis truncation (`truncate` / `overflow-hidden text-ellipsis`). Inter's glyph extent exceeds 1.0em, so descenders render below the 12px box and are clipped by `overflow: hidden`. `leading-4` gives a 16px line box.

Layout impact:
- Model picker: none — trigger is fixed `h-8`, items are `min-h-8` with `py-1.5` (12 + 16 = 28 < 32), both `items-center`. Badges keep their own `leading-none`.
- Turn status: the row has no fixed height, so it grows 12px → 16px (4px taller line under the message).

A repo-wide sweep for the same pattern (tight line-height + clipping) found these two plus one marketing-page case (landing rotating role word, ~0.8px at 52px), which is intentionally left out of this PR. Other matches (emoji avatars, 1.25-ratio menu rows, badges, display headings) were measured and do not clip.

## Test plan
- [x] Standalone Chromium repro using the deployed production CSS bundle + Inter, exact class strings from source, old vs new; glyph ink measured against the clip box:
  - Model picker, `leading-none`: label `clientHeight` 12 / `scrollHeight` 13 → clipped; `leading-4`: 16 / 16 → not clipped, row/trigger height unchanged at 32px
  - Turn status ("Thinking", "Using web_search", "Failed: typing pipeline"), `leading-none`: descenders overflow the 12px box by 1px; `leading-4`: 1px clearance in a 16px box
- [x] `@zooclaw/chat-ui`: vitest (536 passed), eslint, tsc
- [x] `web/app` `OpenClawUserMessage.unit.spec.tsx` (31 passed)

🤖 Generated with [Claude Code](https://claude.com/claude-code)


---

## fix(landing): align homepage hero and update social links (#4038)

- **SHA**: `15024b1669afff68ef5aecdba43df9b78b26c6a5`
- **作者**: shana-srp
- **日期**: 2026-10-16T04:14:11Z
- **PR**: #4038

### Commit Message

```
fix(landing): align homepage hero and update social links (#4038)

## Summary
Align the homepage hero with the supplied Figma layout: increase top
spacing, position the headline beside the description and CTA buttons,
and frame the product screenshot with a continuous white border. Remove
the hero Product Hunt badge; the footer badge remains.

Keep the original light background image and static background crop.
Bound the artwork height on wide screens so the screenshot remains
cropped at the bottom. On phones and small tablets below 760px, keep the
full screenshot visible with a complete bottom border and rounded inner
and outer corners. Preserve responsive layouts and existing CTA
behavior.

Update the footer social links to the official ZooWork X, YouTube, and
Product Hunt profiles. Manage the Product Hunt product-page URL
separately from the awards badge URL.

Design:
https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1198-3992

## Validation
- Web governance guards, full TypeScript checking, changed-file ESLint,
and `git diff --check` passed after syncing the branch with current
main.
- All 9 landing-page Playwright scenarios passed against the local mock
preview.
- The mobile regression verifies complete bottom borders and rounded
inner/outer corners at 320, 375, 640, and 759px, with no horizontal
overflow. It reproduced the original zero-radius bottom edge before the
fix.
- The desktop crop regression passes at 761, 1024, 1505, 2048, 2560, and
3440px. Together with the 759px mobile case, this covers both sides of
the mobile breakpoint and the previously reported ultrawide sizes.
- Visually checked the actual hero at 320, 640, and 1505px; the original
light background and completed mobile frame render correctly.
- The standard local unit-test run remains affected by duplicate React
installations in the reused dependency setup. Unit tests are not
reported as passing locally; CI remains the clean-environment gate.

---------

Co-authored-by: shana-srp <shana-maker@users.noreply.github.com>
```

### PR Body

## Summary
Align the homepage hero with the supplied Figma layout: increase top spacing, position the headline beside the description and CTA buttons, and frame the product screenshot with a continuous white border. Remove the hero Product Hunt badge; the footer badge remains.

Keep the original light background image and static background crop. Bound the artwork height on wide screens so the screenshot remains cropped at the bottom. On phones and small tablets below 760px, keep the full screenshot visible with a complete bottom border and rounded inner and outer corners. Preserve responsive layouts and existing CTA behavior.

Update the footer social links to the official ZooWork X, YouTube, and Product Hunt profiles. Manage the Product Hunt product-page URL separately from the awards badge URL.

Design: https://www.figma.com/design/IgzHI9jcrXpME6PVaZJRJs/zoowork?node-id=1198-3992

## Validation
- Web governance guards, full TypeScript checking, changed-file ESLint, and `git diff --check` passed after syncing the branch with current main.
- All 9 landing-page Playwright scenarios passed against the local mock preview.
- The mobile regression verifies complete bottom borders and rounded inner/outer corners at 320, 375, 640, and 759px, with no horizontal overflow. It reproduced the original zero-radius bottom edge before the fix.
- The desktop crop regression passes at 761, 1024, 1505, 2048, 2560, and 3440px. Together with the 759px mobile case, this covers both sides of the mobile breakpoint and the previously reported ultrawide sizes.
- Visually checked the actual hero at 320, 640, and 1505px; the original light background and completed mobile frame render correctly.
- The standard local unit-test run remains affected by duplicate React installations in the reused dependency setup. Unit tests are not reported as passing locally; CI remains the clean-environment gate.


---
