# ecap-workspace Commits — 2026-05-12

## 0e081954ad8c
- **Author:** bill-srp
- **Date:** 2026-05-12T12:37:39Z

### Commit Message

```
fix(web): normalize locale prefix in login modal pathname guard (#1600)

## Summary

Login modal opened by `LandingScreen` on unauth `/chat?sp=…` deep links
flashed closed because `usePathname()` oscillates between `/chat` and
`/{locale}/chat` during the middleware locale rewrite, and the existing
close-on-navigation guard in `LoginCheckProvider` only covered the `null
→ real` transition. The guard treated `/en/chat → /chat` as cross-route
navigation and closed the just-opened modal.

The reproduction is DevTools-sensitive: with DevTools closed (cache
enabled), the prefetched/cached JS path through the rewrite reliably
oscillates; with DevTools open + "Disable cache" enabled, the bug masks
because fresh chunks load past the race.

## Fix

Normalize both stored and incoming pathname via
`removeLocaleFromPathname` from `@/lib/i18n/config` before comparing —
locale-equivalent paths now compare equal, so the close only fires on
actual cross-route navigation.

## Test plan

- [x] 3 new regression tests in `LoginCheckProvider.unit.spec.tsx`:
- `does NOT close modal when pathname oscillates between /en/chat and
/chat (locale rewrite)`
- `does NOT close modal when pathname oscillates from /chat to /en/chat
(locale rewrite, reverse)`
- `closes modal on real navigation across distinct routes despite locale
prefix asymmetry` — pins the positive case so a future regression that
disables the close effect can't slip through
- [x] Existing 12 tests in the file remain green (15/15 total)
- [x] `pnpm lint` clean
- [x] `pnpm tsc --noEmit` clean
- [ ] Manual: visit `/chat?sp=test-id` logged out, modal stays open
- [ ] Manual: navigate `/canvas → /chat` while modal open, modal closes
(real navigation contract preserved)

## Related

Extends the guard introduced in #1020 (which fixed the `null → /en/chat`
half of the same bug class for `?agent_id=` deep links). PR #1020's
regression test left the `real → real` locale oscillation uncovered;
this PR closes that gap.
```

### PR #1600 Body

## Summary

Login modal opened by `LandingScreen` on unauth `/chat?sp=…` deep links flashed closed because `usePathname()` oscillates between `/chat` and `/{locale}/chat` during the middleware locale rewrite, and the existing close-on-navigation guard in `LoginCheckProvider` only covered the `null → real` transition. The guard treated `/en/chat → /chat` as cross-route navigation and closed the just-opened modal.

The reproduction is DevTools-sensitive: with DevTools closed (cache enabled), the prefetched/cached JS path through the rewrite reliably oscillates; with DevTools open + "Disable cache" enabled, the bug masks because fresh chunks load past the race.

## Fix

Normalize both stored and incoming pathname via `removeLocaleFromPathname` from `@/lib/i18n/config` before comparing — locale-equivalent paths now compare equal, so the close only fires on actual cross-route navigation.

## Test plan

- [x] 3 new regression tests in `LoginCheckProvider.unit.spec.tsx`:
  - `does NOT close modal when pathname oscillates between /en/chat and /chat (locale rewrite)`
  - `does NOT close modal when pathname oscillates from /chat to /en/chat (locale rewrite, reverse)`
  - `closes modal on real navigation across distinct routes despite locale prefix asymmetry` — pins the positive case so a future regression that disables the close effect can't slip through
- [x] Existing 12 tests in the file remain green (15/15 total)
- [x] `pnpm lint` clean
- [x] `pnpm tsc --noEmit` clean
- [ ] Manual: visit `/chat?sp=test-id` logged out, modal stays open
- [ ] Manual: navigate `/canvas → /chat` while modal open, modal closes (real navigation contract preserved)

## Related

Extends the guard introduced in #1020 (which fixed the `null → /en/chat` half of the same bug class for `?agent_id=` deep links). PR #1020's regression test left the `real → real` locale oscillation uncovered; this PR closes that gap.

---

## cd7c76fc8d78
- **Author:** sam-srp
- **Date:** 2026-05-12T09:01:20Z

### Commit Message

```
refactor(claw-interface): drop allowBots field from MM channel injection (#1599)

## Summary
- `build_mm_channel_config` (default bot init, account_id=\"default\")
and `inject_fastclaw_channel` (per-agent install, Phase 7 of
`deploy_selected_agents`) both hard-coded `allowBots: False` on the
FastClaw channel config.
- Drop the field from both code paths and rely on OpenClaw's default
bot-to-bot policy.

## Test plan
- [x] `pyright` + `ruff` clean (pre-commit)
- [ ] Manual: verify OpenClaw's default `allowBots` policy matches the
intended behavior on staging before merging
- [ ] Manual: confirm no bot-to-bot loop appears between freshly hired
agents

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1599 Body

## Summary
- `build_mm_channel_config` (default bot init, account_id=\"default\") and `inject_fastclaw_channel` (per-agent install, Phase 7 of `deploy_selected_agents`) both hard-coded `allowBots: False` on the FastClaw channel config.
- Drop the field from both code paths and rely on OpenClaw's default bot-to-bot policy.

## Test plan
- [x] `pyright` + `ruff` clean (pre-commit)
- [ ] Manual: verify OpenClaw's default `allowBots` policy matches the intended behavior on staging before merging
- [ ] Manual: confirm no bot-to-bot loop appears between freshly hired agents

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 164e6660e9be
- **Author:** sam-srp
- **Date:** 2026-05-12T07:46:33Z

### Commit Message

```
refactor(claw-interface): drop divergent blockStreaming MM channel config (#1598)

## Summary
- `build_mm_channel_config` (default bot init, account_id=\"default\")
and `inject_fastclaw_channel` (per-agent install, Phase 7 of
`deploy_selected_agents`) were writing **different** blockStreaming /
Coalesce / Chunk parameters:
- Default channel: `blockStreaming=true` + `Coalesce={minChars:800,
idleMs:500}`
- Per-agent channel: `blockStreaming=true` + `Coalesce={minChars:800,
maxChars:1200, idleMs:1000}` + `Chunk={minChars:150, maxChars:1000}`
- The drift meant main bot streamed visibly faster than hired agents
(500ms vs 1000ms idle window, different chunk sizing), and the
\`default\` channel didn't even have the `maxChars`/`Chunk` knobs the
per-agent path had.
- Cleanest fix: drop the whole block-streaming knob from both paths and
let OpenClaw stream tokens to Mattermost with its default behavior.
Restores a single, consistent cadence across main and per-agent
channels.

## Test plan
- [x] `pyright` + `ruff` clean (pre-commit)
- [x] `pytest tests/unit -k \"provisioner or mattermost or channel\"` —
124 passed
- [ ] Manual: create a new agent, send a message, verify streaming
cadence in MM DM
- [ ] Manual: confirm main bot streams identically to hired agents

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-authored-by: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

### PR #1598 Body

## Summary
- `build_mm_channel_config` (default bot init, account_id=\"default\") and `inject_fastclaw_channel` (per-agent install, Phase 7 of `deploy_selected_agents`) were writing **different** blockStreaming / Coalesce / Chunk parameters:
  - Default channel: `blockStreaming=true` + `Coalesce={minChars:800, idleMs:500}`
  - Per-agent channel: `blockStreaming=true` + `Coalesce={minChars:800, maxChars:1200, idleMs:1000}` + `Chunk={minChars:150, maxChars:1000}`
- The drift meant main bot streamed visibly faster than hired agents (500ms vs 1000ms idle window, different chunk sizing), and the \`default\` channel didn't even have the `maxChars`/`Chunk` knobs the per-agent path had.
- Cleanest fix: drop the whole block-streaming knob from both paths and let OpenClaw stream tokens to Mattermost with its default behavior. Restores a single, consistent cadence across main and per-agent channels.

## Test plan
- [x] `pyright` + `ruff` clean (pre-commit)
- [x] `pytest tests/unit -k \"provisioner or mattermost or channel\"` — 124 passed
- [ ] Manual: create a new agent, send a message, verify streaming cadence in MM DM
- [ ] Manual: confirm main bot streams identically to hired agents

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---

## 0308d8573e0f
- **Author:** kaka-srp
- **Date:** 2026-05-12T03:47:35Z

### Commit Message

```
fix(claw-interface): gate title generation to canvas (ECA-660) (#1596)

## Summary

- **What broke (ECA-660):** `generate_session_title` was firing on every
new chat session's first message for every agent, sending `gpt-5.2` to
LiteLLM with the user's `team_key`. Team keys are scoped to group
aliases (`pro-chat`, `pro-image_generation`, `pro-video_generation`),
not concrete model names — so every billing-initialized user hit
`litellm.AuthenticationError: team not allowed to access model`.
- **Why it was hidden:** the call is fire-and-forget with a truncation
fallback, so users just saw a "dumb" auto-truncated title.
`ecap-scanner` finally surfaced it on 2026-05-12 as ECA-660.
- **Why most of those calls were wasted work:** only `/canvas` actually
displays `task_title` in its UI. `/chat`, `/mini-chat`,
`/session-history` ignore it entirely; the `AgentChatClient` component
that would render it is orphaned (no page mounts it).

## Three-layer defense (so this can't quietly come back)

| Layer | Change |
| --- | --- |
| **Constant** | `TITLE_GENERATION_AGENTS = {"canvas"}` in
`services/claw-interface/app/routes/session/utils.py` — explicit set of
agents whose UI displays the generated title. |
| **Routing gate** | `chat.py` block 1 (canvas/fullstack_assistant
branch) gated by membership in that set. Block 2 (AGENT_PLATFORM branch)
was 100% dead code (no agent in that branch displays `task_title`) and
is **deleted**. |
| **Signature** | `generate_session_title()` loses its `api_key`
parameter — it now always uses `SETTINGS.LITELLM_PROXY_API_KEY` (system
key). Anyone trying to re-introduce a team_key path hits a `TypeError`,
not a silent 401. |

## Drive-by hygiene

Codex review flagged a Mattermost user token in
`.dev-logs/frontend.log:97` (untracked output from a previous
`scripts/dev.sh` run). Added `.dev-logs/` to `.gitignore` so the
directory can never be staged accidentally. **The leaked token should be
rotated separately** — this PR only prevents future leaks via git.

## Test plan

- [x] `pytest tests/unit/test_chat_validation.py
tests/unit/test_session_utils.py tests/unit/test_litellm_endpoints.py` →
92 passed
- [x] `ruff check` + `pyright` → clean on changed files (pre-commit
hooks all green)
- [x] New regression test `test_skips_title_for_non_canvas_agent`
confirms non-canvas agents do NOT spawn a title-gen task
- [x] Existing `test_auto_generates_title_when_missing` repurposed for
`agentName="canvas"` (positive path still covered)
- [ ] After deploy: confirm `[GENERATE_TITLE] Error generating title` in
GCP claw-interface logs drops to 0 → `ecap-scanner` auto-closes ECA-660
```

### PR #1596 Body

## Summary

- **What broke (ECA-660):** `generate_session_title` was firing on every new chat session's first message for every agent, sending `gpt-5.2` to LiteLLM with the user's `team_key`. Team keys are scoped to group aliases (`pro-chat`, `pro-image_generation`, `pro-video_generation`), not concrete model names — so every billing-initialized user hit `litellm.AuthenticationError: team not allowed to access model`.
- **Why it was hidden:** the call is fire-and-forget with a truncation fallback, so users just saw a "dumb" auto-truncated title. `ecap-scanner` finally surfaced it on 2026-05-12 as ECA-660.
- **Why most of those calls were wasted work:** only `/canvas` actually displays `task_title` in its UI. `/chat`, `/mini-chat`, `/session-history` ignore it entirely; the `AgentChatClient` component that would render it is orphaned (no page mounts it).

## Three-layer defense (so this can't quietly come back)

| Layer | Change |
| --- | --- |
| **Constant** | `TITLE_GENERATION_AGENTS = {"canvas"}` in `services/claw-interface/app/routes/session/utils.py` — explicit set of agents whose UI displays the generated title. |
| **Routing gate** | `chat.py` block 1 (canvas/fullstack_assistant branch) gated by membership in that set. Block 2 (AGENT_PLATFORM branch) was 100% dead code (no agent in that branch displays `task_title`) and is **deleted**. |
| **Signature** | `generate_session_title()` loses its `api_key` parameter — it now always uses `SETTINGS.LITELLM_PROXY_API_KEY` (system key). Anyone trying to re-introduce a team_key path hits a `TypeError`, not a silent 401. |

## Drive-by hygiene

Codex review flagged a Mattermost user token in `.dev-logs/frontend.log:97` (untracked output from a previous `scripts/dev.sh` run). Added `.dev-logs/` to `.gitignore` so the directory can never be staged accidentally. **The leaked token should be rotated separately** — this PR only prevents future leaks via git.

## Test plan

- [x] `pytest tests/unit/test_chat_validation.py tests/unit/test_session_utils.py tests/unit/test_litellm_endpoints.py` → 92 passed
- [x] `ruff check` + `pyright` → clean on changed files (pre-commit hooks all green)
- [x] New regression test `test_skips_title_for_non_canvas_agent` confirms non-canvas agents do NOT spawn a title-gen task
- [x] Existing `test_auto_generates_title_when_missing` repurposed for `agentName="canvas"` (positive path still covered)
- [ ] After deploy: confirm `[GENERATE_TITLE] Error generating title` in GCP claw-interface logs drops to 0 → `ecap-scanner` auto-closes ECA-660

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---
