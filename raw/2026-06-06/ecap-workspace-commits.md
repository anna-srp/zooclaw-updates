# ecap-workspace commits for 2026-06-06

## d8c1b103 - bill-srp - 2026-06-06T14:24:59Z
```
fix(openclaw): extract webchat hash token (#2239)

## Summary
- Extract OpenClaw runtime token from webchat URL hash fragments like
`#token=...` when stored bot token fields are empty.
- Keep existing token precedence for `access_token` and `token`, and
retain query-token support for legacy URLs.
- Add regression coverage for hash/query token parsing and ready-bot
fallback.

## Root cause
OpenClaw connect responses can provide the runtime token in
`webchat_url` as a hash fragment. The backend stripped `ws_url`
query/fragment and only persisted tokens already present on the bot
record, so the frontend websocket handshake could receive no token and
stay disconnected.

## Test plan
- [x] `ruff check .`
- [x] `uv run pytest
services/claw-interface/tests/unit/test_openclaw_routes.py -q`
- [x] `uv run ruff check
services/claw-interface/app/services/openclaw/bot_lifecycle.py
services/claw-interface/tests/unit/test_openclaw_routes.py`
- [ ] `uv run pyright app tests` blocked locally: uv could not fetch
`setuptools>=61` from PyPI after retry.
- [ ] `uv run pytest --cov=app --cov-report=term-missing
--cov-fail-under=90 -q` blocked locally for same dependency-resolution
failure; `--no-sync` fallback also lacked local test deps such as
`pytest_bdd` and `litellm`.
```
**PR Body:**
## Summary
- Extract OpenClaw runtime token from webchat URL hash fragments like `#token=...` when stored bot token fields are empty.
- Keep existing token precedence for `access_token` and `token`, and retain query-token support for legacy URLs.
- Add regression coverage for hash/query token parsing and ready-bot fallback.

## Root cause
OpenClaw connect responses can provide the runtime token in `webchat_url` as a hash fragment. The backend stripped `ws_url` query/fragment and only persisted tokens already present on the bot record, so the frontend websocket handshake could receive no token and stay disconnected.

## Test plan
- [x] `ruff check .`
- [x] `uv run pytest services/claw-interface/tests/unit/test_openclaw_routes.py -q`
- [x] `uv run ruff check services/claw-interface/app/services/openclaw/bot_lifecycle.py services/claw-interface/tests/unit/test_openclaw_routes.py`
- [ ] `uv run pyright app tests` blocked locally: uv could not fetch `setuptools>=61` from PyPI after retry.
- [ ] `uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` blocked locally for same dependency-resolution failure; `--no-sync` fallback also lacked local test deps such as `pytest_bdd` and `litellm`.

## b6daade5 - bill-srp - 2026-06-06T13:32:30Z
```
fix(web): allow OpenClaw connect without token (#2238)

## Summary
- Allow OpenClawProvider to initiate the gateway/control websocket when
init returns a gateway ws_url even if bot.token is empty.
- Fall back to token= from legacy gateway websocket URLs during the
connect.challenge handshake when no explicit token is available.
- Add regression tests for ready bot + gateway URL + empty token and
websocket URL token fallback.

## Root cause
OpenClawProvider required both bot.ws_url and a truthy bot.token before
dispatching BOT_READY and before calling wsConnect. When init returned a
gateway websocket URL without a separate token, the provider stayed
disconnected. Removing that guard also required aligning the websocket
hook, because the hook previously rejected missing explicit tokens even
when legacy ws_url already carried token=.

## Test plan
- [x] pnpm --dir web/app exec vitest run
tests/unit/components/providers/OpenClawProvider.behavior.unit.spec.tsx
- [x] pnpm --dir web/app exec vitest run
tests/unit/hooks/useOpenClawWebSocket.unit.spec.ts
- [ ] pnpm --dir web run lint (blocked locally: ESLint/Next config
schema error: Unexpected top-level property "name")
- [ ] pnpm --dir web run tsc (blocked locally: script passes unsupported
--if-present to pnpm exec)
- [ ] pnpm --dir web/app exec tsc --noEmit (blocked locally: unresolved
installed deps/types such as usehooks-ts, motion/react, zustand,
TanStack persist packages)
- [ ] pnpm --dir web run test:unit (blocked locally: broad unresolved
imports for usehooks-ts/zustand/TanStack persist plus jsdom navigation
errors)
```
**PR Body:**
## Summary
- Allow OpenClawProvider to initiate the gateway/control websocket when init returns a gateway ws_url even if bot.token is empty.
- Fall back to token= from legacy gateway websocket URLs during the connect.challenge handshake when no explicit token is available.
- Add regression tests for ready bot + gateway URL + empty token and websocket URL token fallback.

## Root cause
OpenClawProvider required both bot.ws_url and a truthy bot.token before dispatching BOT_READY and before calling wsConnect. When init returned a gateway websocket URL without a separate token, the provider stayed disconnected. Removing that guard also required aligning the websocket hook, because the hook previously rejected missing explicit tokens even when legacy ws_url already carried token=.

## Test plan
- [x] pnpm --dir web/app exec vitest run tests/unit/components/providers/OpenClawProvider.behavior.unit.spec.tsx
- [x] pnpm --dir web/app exec vitest run tests/unit/hooks/useOpenClawWebSocket.unit.spec.ts
- [ ] pnpm --dir web run lint (blocked locally: ESLint/Next config schema error: Unexpected top-level property "name")
- [ ] pnpm --dir web run tsc (blocked locally: script passes unsupported --if-present to pnpm exec)
- [ ] pnpm --dir web/app exec tsc --noEmit (blocked locally: unresolved installed deps/types such as usehooks-ts, motion/react, zustand, TanStack persist packages)
- [ ] pnpm --dir web run test:unit (blocked locally: broad unresolved imports for usehooks-ts/zustand/TanStack persist plus jsdom navigation errors)
