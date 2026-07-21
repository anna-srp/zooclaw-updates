# SerendipityOneInc/ecap-workspace commits (2026-07-20)

共 21 个 commit

---

## docs(agents): revise engine channels design to ACS passthrough + weixin QR reuse (#2972)

- **SHA**: b5cd25c41f5a80e6caa274cfa57868f72dc99ca1
- **作者**: bill-srp
- **日期**: 2026-07-20T14:45:36Z
- **PR**: 2972

### 完整 commit message

```
docs(agents): revise engine channels design to ACS passthrough + weixin QR reuse (#2972)

## Summary

Revises the engine-agent-channels design (ECA-1279) after reading the
ACS codebase. **Docs only.** The merged spec + plans described a
channel-sink design built on a wrong assumption; this corrects them.

Linear: https://linear.app/srpone/issue/ECA-1279

## Why

The plans assumed claw-interface owns the Feishu/Weixin/WeCom QR/OAuth
handshake and only writes the final channel to ACS via a sink. Reading
`SerendipityOneInc/agent-channel-service` showed the opposite:

- ACS exposes **only agent-scoped CRUD** — `GET/POST
/v1/computers/{cid}/agents/{aid}/channels`, `PUT/DELETE .../{platform}`.
**No setup/poll/QR/device-auth endpoint exists.**
- ACS expects **fully-formed credentials** in `config` (Feishu
`{appId,appSecret}`, Slack `{botToken,appToken}`, WeCom
`{botId,secret}`, WeChat `{botToken,baseUrl}`).
- ACS's own integration doc
(`docs/claw-interface-channel-api-design.md:7,29`) states claw-interface
**keeps** the platform setup flow.

Both former "engine-team dependencies" are resolved directly from the
ACS source: the single-writer contract, and the status/health enum
(`status: configured|disabled|running|error`, `health:
unknown|healthy|degraded|unhealthy`).

## What changed

- **Removed the entire channel-sink design**:
`BotChannelSink`/`AcsChannelSink`, sink threading through `feishu.py`,
and the `boss_channel_setup_job` unique-index migration — none of it is
needed.
- **Slack / Feishu / WeCom → pure passthrough.** The frontend already
has manual credential fields (`PLATFORM_FIELDS`) that are exactly ACS's
config keys. E1 (#2957, merged) already accepts them
(`normalize_channel_config` passes Feishu/WeCom through) → ACS
`create_channel`. **No new backend.**
- **Weixin → the one exception.** A personal WeChat has no static
credential — the QR scan *is* the auth. The ilinkai helpers
(`_wx_get_qrcode`/`_wx_get_qrcode_status`) are bot-independent and the
scan yields `{botToken, baseUrl}` = ACS's WeChat config. So the engine
Weixin flow reuses those helpers and swaps only the terminal write from
the OpenClaw bot to ACS. One small backend slice, no compensation saga,
no shared lock.

## Superseded plans → two new ones

- Deleted `e2-sink-feishu`, `e3-weixin-wecom`, `e4-frontend-hub` (the
sink approach).
- Added `weixin-backend` (Weixin QR → ACS) and `frontend-hub` (engine
targets: manual entry for Slack/Feishu/WeCom, QR for Weixin).

E1 (#2957) is unchanged and remains correct.

## Review asks

- Sanity of the passthrough claim (manual entry → E1 CRUD → ACS) for
Slack/Feishu/WeCom.
- The Weixin ilinkai-reuse (bot-independent helpers,
`{botToken,baseUrl}` → ACS, workspace-keyed session with no shared
`boss_channel_setup_watcher` lock).
- Frontend target-mode `ChannelCard` (no `bound_agent_id` for engine) +
`StatusBadge` ACS enum mapping.
```

### PR body

## Summary

Revises the engine-agent-channels design (ECA-1279) after reading the ACS codebase. **Docs only.** The merged spec + plans described a channel-sink design built on a wrong assumption; this corrects them.

Linear: https://linear.app/srpone/issue/ECA-1279

## Why

The plans assumed claw-interface owns the Feishu/Weixin/WeCom QR/OAuth handshake and only writes the final channel to ACS via a sink. Reading `SerendipityOneInc/agent-channel-service` showed the opposite:

- ACS exposes **only agent-scoped CRUD** — `GET/POST /v1/computers/{cid}/agents/{aid}/channels`, `PUT/DELETE .../{platform}`. **No setup/poll/QR/device-auth endpoint exists.**
- ACS expects **fully-formed credentials** in `config` (Feishu `{appId,appSecret}`, Slack `{botToken,appToken}`, WeCom `{botId,secret}`, WeChat `{botToken,baseUrl}`).
- ACS's own integration doc (`docs/claw-interface-channel-api-design.md:7,29`) states claw-interface **keeps** the platform setup flow.

Both former "engine-team dependencies" are resolved directly from the ACS source: the single-writer contract, and the status/health enum (`status: configured|disabled|running|error`, `health: unknown|healthy|degraded|unhealthy`).

## What changed

- **Removed the entire channel-sink design**: `BotChannelSink`/`AcsChannelSink`, sink threading through `feishu.py`, and the `boss_channel_setup_job` unique-index migration — none of it is needed.
- **Slack / Feishu / WeCom → pure passthrough.** The frontend already has manual credential fields (`PLATFORM_FIELDS`) that are exactly ACS's config keys. E1 (#2957, merged) already accepts them (`normalize_channel_config` passes Feishu/WeCom through) → ACS `create_channel`. **No new backend.**
- **Weixin → the one exception.** A personal WeChat has no static credential — the QR scan *is* the auth. The ilinkai helpers (`_wx_get_qrcode`/`_wx_get_qrcode_status`) are bot-independent and the scan yields `{botToken, baseUrl}` = ACS's WeChat config. So the engine Weixin flow reuses those helpers and swaps only the terminal write from the OpenClaw bot to ACS. One small backend slice, no compensation saga, no shared lock.

## Superseded plans → two new ones

- Deleted `e2-sink-feishu`, `e3-weixin-wecom`, `e4-frontend-hub` (the sink approach).
- Added `weixin-backend` (Weixin QR → ACS) and `frontend-hub` (engine targets: manual entry for Slack/Feishu/WeCom, QR for Weixin).

E1 (#2957) is unchanged and remains correct.

## Review asks

- Sanity of the passthrough claim (manual entry → E1 CRUD → ACS) for Slack/Feishu/WeCom.
- The Weixin ilinkai-reuse (bot-independent helpers, `{botToken,baseUrl}` → ACS, workspace-keyed session with no shared `boss_channel_setup_watcher` lock).
- Frontend target-mode `ChannelCard` (no `bound_agent_id` for engine) + `StatusBadge` ACS enum mapping.


---

## fix(auth): scope login captcha to email (#2970)

- **SHA**: fe47fe75bf398921a1c39f1d173c4b6fab4bd8d1
- **作者**: tim-srp
- **日期**: 2026-07-20T14:20:27Z
- **PR**: 2970

### 完整 commit message

```
fix(auth): scope login captcha to email (#2970)

## Summary

- scope the shared login Turnstile challenge to email OTP only
- let Google and phone authentication proceed without forwarding or
persisting the email captcha token
- keep Firebase phone reCAPTCHA intact and add regressions for both
login layouts, widget lifecycle, and phone OTP exchange

## Root cause

`LoginForm` treated one Turnstile token as a prerequisite for Google,
phone, and email login. Google and phone buttons looked enabled, but
their click handlers returned before starting authentication while the
challenge was unresolved. Those flows also forwarded the shared token
through `/auth/exchange`, coupling unrelated login methods to the email
OTP protection.

This change gives the captcha an email-only state and visual boundary.
It removes the Google/phone token handoffs, keeps the email OTP payload
unchanged, and ignores script-load failures that arrive after the widget
has unmounted.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/src/components/LoginForm.tsx
web/app/src/components/TurnstileWidget.tsx
'web/app/src/app/[locale]/(app)/user/verify/page.tsx'
web/app/src/lib/auth/captcha.ts
web/app/tests/unit/components/LoginForm.unit.spec.tsx
web/app/tests/unit/components/TurnstileWidget.unit.spec.tsx
web/app/tests/unit/app/user-verify-phone.unit.spec.tsx` — 12 files, 178
tests; TypeScript, ESLint, and frontend guards passed
- [x] `bash scripts/verify-changed.sh`
- [x] pre-push PR size and changed-surface gates
- [x] regression test observed RED before the stale Turnstile callback
guard and GREEN afterward

## Known limitation

This PR intentionally does not change
`SerendipityOneInc/user-interface`. Environments that still enforce
Turnstile for Google or phone `/auth/exchange` require separate backend
configuration or implementation coordination before deploying this
frontend behavior.
```

### PR body

## Summary

- scope the shared login Turnstile challenge to email OTP only
- let Google and phone authentication proceed without forwarding or persisting the email captcha token
- keep Firebase phone reCAPTCHA intact and add regressions for both login layouts, widget lifecycle, and phone OTP exchange

## Root cause

`LoginForm` treated one Turnstile token as a prerequisite for Google, phone, and email login. Google and phone buttons looked enabled, but their click handlers returned before starting authentication while the challenge was unresolved. Those flows also forwarded the shared token through `/auth/exchange`, coupling unrelated login methods to the email OTP protection.

This change gives the captcha an email-only state and visual boundary. It removes the Google/phone token handoffs, keeps the email OTP payload unchanged, and ignores script-load failures that arrive after the widget has unmounted.

## Test plan

- [x] `bash scripts/verify-web.sh web/app/src/components/LoginForm.tsx web/app/src/components/TurnstileWidget.tsx 'web/app/src/app/[locale]/(app)/user/verify/page.tsx' web/app/src/lib/auth/captcha.ts web/app/tests/unit/components/LoginForm.unit.spec.tsx web/app/tests/unit/components/TurnstileWidget.unit.spec.tsx web/app/tests/unit/app/user-verify-phone.unit.spec.tsx` — 12 files, 178 tests; TypeScript, ESLint, and frontend guards passed
- [x] `bash scripts/verify-changed.sh`
- [x] pre-push PR size and changed-surface gates
- [x] regression test observed RED before the stale Turnstile callback guard and GREEN afterward

## Known limitation

This PR intentionally does not change `SerendipityOneInc/user-interface`. Environments that still enforce Turnstile for Google or phone `/auth/exchange` require separate backend configuration or implementation coordination before deploying this frontend behavior.


---

## refactor(web): replace message renderers with @zooclaw/chat-ui (#2971)

- **SHA**: 18c3652df7b09902368d8c76e37c9b00b92da121
- **作者**: bill-srp
- **日期**: 2026-07-20T14:14:52Z
- **PR**: 2971

### 完整 commit message

```
refactor(web): replace message renderers with @zooclaw/chat-ui (#2971)

## Summary

PR **2b** of the chat-UI extraction Phase 2 — the **replace** step.
Rewrites the two message renderers as thin **data-mapping containers**
that consume the `@zooclaw/chat-ui` components merged in PR 2a (#2969).
**Zero call-site changes** — `OpenClawThread.tsx` is untouched, and the
containers keep their paths, export names, and prop signatures. The
existing app renderer/thread specs are the **protected regression
harness** and pass **unchanged**.

Completes the Phase 2 chain: docs #2965 → extract #2969 → this replace
PR.

Spec:
`docs/superpowers/specs/2026-07-20-chat-ui-extraction-phase2-messages-design.md`
Plan: `docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase2.md`
(PR 2b = Tasks 6–9)

## What changed (9 files, all `web/app`)

- **Bridge** (`ChatUiAppProvider.tsx`): `renderMarkdown(content, ctx)`
maps the rich markdown context onto `MarkdownContent`'s props; supplies
`locale` from `useLanguage()`.
- **Containers** (`OpenClawUserMessage.tsx`,
`OpenClawAssistantMessage.tsx`): read the assistant-ui runtime, unpack
`metadata.custom`, compute derived content (ermp parsing / artifact
dedup / image split / avatar / reactions), then render the package
component inside `ChatUiAppProvider` with view + slots + callbacks. They
keep importing the app wrappers `./ToolGroup`, `./InteractiveCards`,
`./MessageActions` and pass them into the package slots — so the
protected specs' module mocks stay live. `isConsecutive` is threaded
from `OpenClawThread` into the package `AssistantMessage`.
- **Re-exports** (Phase-1 pattern): `chat/lib/formatMessageTime.ts`,
`chat/lib/turnStatusParser.ts` (the two moved fns),
`lib/openclaw/types.ts` (turn-status types) now re-export from
`@zooclaw/chat-ui`; all existing importers keep working.
- **Two dependent test mocks**: `ToolGroup.unit.spec.tsx` and
`ModelDegradationBanner.unit.spec.tsx` gain a `useLanguage` mock (the
bridge now reads locale) — mock-only additions, no assertion changes.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + `tsc` + vitest (**516
files / 6957 tests pass**, 1 skipped, 1 todo) + eslint, all green.
- [x] **Three protected specs pass with zero edits**:
`OpenClawAssistantMessage` (28/28), `OpenClawUserMessage` (20/20),
`OpenClawThread` — the regression harness for byte-identical DOM.
- [x] `OpenClawThread.tsx` unchanged; scope confined to `web/app` (9
files).
- [x] Coverage ratchet holds: statements 87.74 / branches 80.87 /
functions 86.44 / lines 90.09 (thresholds 83 / 75 / 81 / 85).
- [ ] CI `web-build-check` (`next build`) — runs on this PR.
- [ ] `/chat` browser mount check — see PR comment.
```

### PR body

## Summary

PR **2b** of the chat-UI extraction Phase 2 — the **replace** step. Rewrites the two message renderers as thin **data-mapping containers** that consume the `@zooclaw/chat-ui` components merged in PR 2a (#2969). **Zero call-site changes** — `OpenClawThread.tsx` is untouched, and the containers keep their paths, export names, and prop signatures. The existing app renderer/thread specs are the **protected regression harness** and pass **unchanged**.

Completes the Phase 2 chain: docs #2965 → extract #2969 → this replace PR.

Spec: `docs/superpowers/specs/2026-07-20-chat-ui-extraction-phase2-messages-design.md`
Plan: `docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase2.md` (PR 2b = Tasks 6–9)

## What changed (9 files, all `web/app`)

- **Bridge** (`ChatUiAppProvider.tsx`): `renderMarkdown(content, ctx)` maps the rich markdown context onto `MarkdownContent`'s props; supplies `locale` from `useLanguage()`.
- **Containers** (`OpenClawUserMessage.tsx`, `OpenClawAssistantMessage.tsx`): read the assistant-ui runtime, unpack `metadata.custom`, compute derived content (ermp parsing / artifact dedup / image split / avatar / reactions), then render the package component inside `ChatUiAppProvider` with view + slots + callbacks. They keep importing the app wrappers `./ToolGroup`, `./InteractiveCards`, `./MessageActions` and pass them into the package slots — so the protected specs' module mocks stay live. `isConsecutive` is threaded from `OpenClawThread` into the package `AssistantMessage`.
- **Re-exports** (Phase-1 pattern): `chat/lib/formatMessageTime.ts`, `chat/lib/turnStatusParser.ts` (the two moved fns), `lib/openclaw/types.ts` (turn-status types) now re-export from `@zooclaw/chat-ui`; all existing importers keep working.
- **Two dependent test mocks**: `ToolGroup.unit.spec.tsx` and `ModelDegradationBanner.unit.spec.tsx` gain a `useLanguage` mock (the bridge now reads locale) — mock-only additions, no assertion changes.

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + `tsc` + vitest (**516 files / 6957 tests pass**, 1 skipped, 1 todo) + eslint, all green.
- [x] **Three protected specs pass with zero edits**: `OpenClawAssistantMessage` (28/28), `OpenClawUserMessage` (20/20), `OpenClawThread` — the regression harness for byte-identical DOM.
- [x] `OpenClawThread.tsx` unchanged; scope confined to `web/app` (9 files).
- [x] Coverage ratchet holds: statements 87.74 / branches 80.87 / functions 86.44 / lines 90.09 (thresholds 83 / 75 / 81 / 85).
- [ ] CI `web-build-check` (`next build`) — runs on this PR.
- [ ] `/chat` browser mount check — see PR comment.


---

## refactor(chat-ui): extract message renderers into @zooclaw/chat-ui (#2969)

- **SHA**: 7ee3aceb4973310b10c04aaa4d66b5fe4b318ccb
- **作者**: bill-srp
- **日期**: 2026-07-20T12:59:55Z
- **PR**: 2969

### 完整 commit message

```
refactor(chat-ui): extract message renderers into @zooclaw/chat-ui (#2969)

## Summary

PR **2a** of the chat-UI extraction Phase 2 (message renderers) —
**package-only**. Extracts the two message renderers into
`@zooclaw/chat-ui` as **view-model + slots** components. `web/app` is
untouched; the app-side container rewrites land in PR 2b.

Follows the merged Phase 1 chain (#2949 / #2953 / #2955) and the Phase 2
docs (#2965).

Spec:
`docs/superpowers/specs/2026-07-20-chat-ui-extraction-phase2-messages-design.md`
Plan: `docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase2.md`
(PR 2a = Tasks 1–5)

## What's in it

- **Provider extension** (backward compatible): `renderMarkdown(content,
ctx?)` gains an optional `ChatUiMarkdownContext` second arg;
`ChatUiConfig.locale` added (default `'en'`). Phase 1 single-arg callers
and the default renderer keep working.
- **Moved pure helpers + types** (`messages/helpers.ts`):
`formatMessageTime`, `formatTurnStatusLabel`,
`shouldShowTurnStatusOnUserMessage`, `parseQuoteAndReply`,
`emojiNameToChar` (+ `REACTION_EMOJI_MAP`), `turnStatusDotClass`,
`buildCardActionMessage`, `buildFormSubmitMessage`; turn-status types
`TurnStatusPhase` / `TurnStatusState` / `TurnStatusView` (`types.ts`);
package-local `ReplyArrowIcon`.
- **`UserMessage`** and **`AssistantMessage`** — presentational
components rendered from a plain-data view-model plus app-rendered
ReactNode slots (avatar / ermp cards / attachments / share checkbox /
tool-group / interactive-cards / trailing actions). `toolGroup` /
`interactiveCards` / `trailingActions` are slots with package defaults,
and `onCopy` defaults to the package `copyToClipboard`, so an external
consumer gets a complete message with zero wiring.
- **Barrel exports** from the package root for consumption in PR 2b.

## Design notes

- **No new package dependencies** — runtime deps stay exactly
`@heroicons/react` + `clsx`. No `@assistant-ui/react`, no react-query,
no `@/` / Next.js imports inside the package. The assistant-ui runtime
reads, ermp/Mattermost subsystems, and avatar identity stay app-side
(extracted in the PR 2b containers).
- All Tailwind class strings, `data-testid` values, translation keys,
and rendered DOM are copied **byte-identically** from the app renderers
(verified: distinctive class strings and testids match 1:1); only the
enumerated view-model/slot seam edits differ.
- Tests follow the package's existing **native-DOM assertion
convention** (no jest-dom in this package by design).

## Test plan

- [x] Package gate green: `pnpm test` (17 files, **207 tests**), `pnpm
lint` (0 warnings), `pnpm tsc` — all pass.
- [x] Scope confined to `web/packages/chat-ui/` — `git diff
origin/main...HEAD -- web/app docs` is empty.
- [ ] CI `web-build-check` (`next build`) — runs on this PR.
- PR 2b will re-verify end-to-end against the existing app
renderer/thread specs (the protected regression harness) plus a `/chat`
browser mount check.
```

### PR body

## Summary

PR **2a** of the chat-UI extraction Phase 2 (message renderers) — **package-only**. Extracts the two message renderers into `@zooclaw/chat-ui` as **view-model + slots** components. `web/app` is untouched; the app-side container rewrites land in PR 2b.

Follows the merged Phase 1 chain (#2949 / #2953 / #2955) and the Phase 2 docs (#2965).

Spec: `docs/superpowers/specs/2026-07-20-chat-ui-extraction-phase2-messages-design.md`
Plan: `docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase2.md` (PR 2a = Tasks 1–5)

## What's in it

- **Provider extension** (backward compatible): `renderMarkdown(content, ctx?)` gains an optional `ChatUiMarkdownContext` second arg; `ChatUiConfig.locale` added (default `'en'`). Phase 1 single-arg callers and the default renderer keep working.
- **Moved pure helpers + types** (`messages/helpers.ts`): `formatMessageTime`, `formatTurnStatusLabel`, `shouldShowTurnStatusOnUserMessage`, `parseQuoteAndReply`, `emojiNameToChar` (+ `REACTION_EMOJI_MAP`), `turnStatusDotClass`, `buildCardActionMessage`, `buildFormSubmitMessage`; turn-status types `TurnStatusPhase` / `TurnStatusState` / `TurnStatusView` (`types.ts`); package-local `ReplyArrowIcon`.
- **`UserMessage`** and **`AssistantMessage`** — presentational components rendered from a plain-data view-model plus app-rendered ReactNode slots (avatar / ermp cards / attachments / share checkbox / tool-group / interactive-cards / trailing actions). `toolGroup` / `interactiveCards` / `trailingActions` are slots with package defaults, and `onCopy` defaults to the package `copyToClipboard`, so an external consumer gets a complete message with zero wiring.
- **Barrel exports** from the package root for consumption in PR 2b.

## Design notes

- **No new package dependencies** — runtime deps stay exactly `@heroicons/react` + `clsx`. No `@assistant-ui/react`, no react-query, no `@/` / Next.js imports inside the package. The assistant-ui runtime reads, ermp/Mattermost subsystems, and avatar identity stay app-side (extracted in the PR 2b containers).
- All Tailwind class strings, `data-testid` values, translation keys, and rendered DOM are copied **byte-identically** from the app renderers (verified: distinctive class strings and testids match 1:1); only the enumerated view-model/slot seam edits differ.
- Tests follow the package's existing **native-DOM assertion convention** (no jest-dom in this package by design).

## Test plan

- [x] Package gate green: `pnpm test` (17 files, **207 tests**), `pnpm lint` (0 warnings), `pnpm tsc` — all pass.
- [x] Scope confined to `web/packages/chat-ui/` — `git diff origin/main...HEAD -- web/app docs` is empty.
- [ ] CI `web-build-check` (`next build`) — runs on this PR.
- PR 2b will re-verify end-to-end against the existing app renderer/thread specs (the protected regression harness) plus a `/chat` browser mount check.


---

## feat(claw-interface): unified agent channels routes with ACS engine leg (#2957)

- **SHA**: ce6ad1473703e85b286e5d81e1cf93bc4c4cae29
- **作者**: bill-srp
- **日期**: 2026-07-20T12:47:53Z
- **PR**: 2957

### 完整 commit message

```
feat(claw-interface): unified agent channels routes with ACS engine leg (#2957)

## Summary

Slice **E1** of engine agent channels (ECA-1279): the unified
`/agents/{workspace_id}/channels*` route family in claw-interface,
engine leg backed by the agent-channel-service (ACS), Slack working
end-to-end, the computer leg rejected cleanly, and mock-backend handlers
for frontend development. **No DB collection** — ACS is the sole record;
claw-interface reads/writes through per-agent.

Linear: https://linear.app/srpone/issue/ECA-1279
Spec:
`docs/superpowers/specs/2026-07-20-engine-agent-channels-design.md`
Plan:
`docs/superpowers/plans/2026-07-20-engine-channels-e1-backend-slack.md`

### What's new

- `app/schema/agent_channels.py` — `AddAgentChannelRequest` /
`UpdateAgentChannelRequest` / `RemoveAgentChannelRequest` /
`AgentChannelPublic` (hand-written, drops ACS-internal ids) /
`AgentChannelListResponse`.
- `app/services/agents/engine_agent_channels_service.py` — ACS-backed
list/add/update/remove. Resolves the workspace via
**`agent_workspace_repo.get_by_workspace_id`** (workspace IDs are
globally unique), then enforces UID/org ownership before applying
runtime and status guards. Install-managed `mattermost` rows are
filtered from list. `allow_from` mirrors the bot leg exactly: `dm_policy
== "open"` always sends `["*"]`; non-open policies always omit it,
regardless of the client value.
- `app/routes/agents/channels.py` — `GET
/agents/{workspace_id}/channels`, `POST .../channels` (201), `POST
.../channels/{platform}/update`, `POST .../channels/{platform}/remove`.
GET/POST only; `require_agents_v2` first-line; runtime-compatible
account IDs are validated locally. Platform names and platform-specific
config, including nested JSON values, are forwarded unchanged because
ACS owns platform support and config validation.
- `scripts/mock-backend` — per-workspace channel handlers matching the
interface contract, including workspace lifecycle, required-platform,
and account-ID validation. The mock stays platform-neutral like
claw-interface.
- ACS failures preserve typed channel-domain errors, including
dependency-not-ready configuration failures and stale update/remove
responses. Diagnostic error bodies redact credential-key variants and
fully mask non-JSON bodies before logging context.

### Deferred to later slices (per plan)

- Feishu / Weixin / WeCom setup flows → E2/E3 (channel-sink refactor).
- Frontend hub extension → E4.

## Test plan

- [x] 87 focused Python unit tests: schema, ACS client, service, routes.
- [x] BDD: Slack add → list → remove → empty against real Mongo — 10
passed.
- [x] Python static gates: ruff, ruff-format, pyright, deptry, vulture,
import-linter.
- [x] Web/mock gates: governance guards, tsc, 21 focused Vitest tests,
ESLint.
- [x] CI `python-code-quality / build-and-test` and `code-quality /
lint-and-test` on the latest head (40/40 checks passed).

## Rollout / risk

Additive, gated behind `AGENTS_V2_ENABLED`; no existing route touched.
Computer workspaces return `channel.runtime_not_supported` and continue
using the existing OpenClaw settings routes, so the bot leg's
legacy-account compatibility policy does not apply to this engine-only
interface. Because CRUD is platform-neutral, rejecting writes to
runtime-managed Mattermost bindings is an ACS invariant rather than a
claw-interface platform allowlist. **Not shippable end-to-end alone** —
a real Slack round-trip to an engine agent depends on the two
engine-team confirmations tracked on ECA-1279 (zooclaw-engine runs these
platforms from ACS-managed config; ACS channel status semantics). E1 is
fully testable against mocks/stubs without them.
```

### PR body

## Summary

Slice **E1** of engine agent channels (ECA-1279): the unified `/agents/{workspace_id}/channels*` route family in claw-interface, engine leg backed by the agent-channel-service (ACS), Slack working end-to-end, the computer leg rejected cleanly, and mock-backend handlers for frontend development. **No DB collection** — ACS is the sole record; claw-interface reads/writes through per-agent.

Linear: https://linear.app/srpone/issue/ECA-1279
Spec: `docs/superpowers/specs/2026-07-20-engine-agent-channels-design.md`
Plan: `docs/superpowers/plans/2026-07-20-engine-channels-e1-backend-slack.md`

### What's new

- `app/schema/agent_channels.py` — `AddAgentChannelRequest` / `UpdateAgentChannelRequest` / `RemoveAgentChannelRequest` / `AgentChannelPublic` (hand-written, drops ACS-internal ids) / `AgentChannelListResponse`.
- `app/services/agents/engine_agent_channels_service.py` — ACS-backed list/add/update/remove. Resolves the workspace via **`agent_workspace_repo.get_by_workspace_id`** (workspace IDs are globally unique), then enforces UID/org ownership before applying runtime and status guards. Install-managed `mattermost` rows are filtered from list. `allow_from` mirrors the bot leg exactly: `dm_policy == "open"` always sends `["*"]`; non-open policies always omit it, regardless of the client value.
- `app/routes/agents/channels.py` — `GET /agents/{workspace_id}/channels`, `POST .../channels` (201), `POST .../channels/{platform}/update`, `POST .../channels/{platform}/remove`. GET/POST only; `require_agents_v2` first-line; runtime-compatible account IDs are validated locally. Platform names and platform-specific config, including nested JSON values, are forwarded unchanged because ACS owns platform support and config validation.
- `scripts/mock-backend` — per-workspace channel handlers matching the interface contract, including workspace lifecycle, required-platform, and account-ID validation. The mock stays platform-neutral like claw-interface.
- ACS failures preserve typed channel-domain errors, including dependency-not-ready configuration failures and stale update/remove responses. Diagnostic error bodies redact credential-key variants and fully mask non-JSON bodies before logging context.

### Deferred to later slices (per plan)

- Feishu / Weixin / WeCom setup flows → E2/E3 (channel-sink refactor).
- Frontend hub extension → E4.

## Test plan

- [x] 87 focused Python unit tests: schema, ACS client, service, routes.
- [x] BDD: Slack add → list → remove → empty against real Mongo — 10 passed.
- [x] Python static gates: ruff, ruff-format, pyright, deptry, vulture, import-linter.
- [x] Web/mock gates: governance guards, tsc, 21 focused Vitest tests, ESLint.
- [x] CI `python-code-quality / build-and-test` and `code-quality / lint-and-test` on the latest head (40/40 checks passed).

## Rollout / risk

Additive, gated behind `AGENTS_V2_ENABLED`; no existing route touched. Computer workspaces return `channel.runtime_not_supported` and continue using the existing OpenClaw settings routes, so the bot leg's legacy-account compatibility policy does not apply to this engine-only interface. Because CRUD is platform-neutral, rejecting writes to runtime-managed Mattermost bindings is an ACS invariant rather than a claw-interface platform allowlist. **Not shippable end-to-end alone** — a real Slack round-trip to an engine agent depends on the two engine-team confirmations tracked on ECA-1279 (zooclaw-engine runs these platforms from ACS-managed config; ACS channel status semantics). E1 is fully testable against mocks/stubs without them.


---

## refactor(web): remove retired API routes (#2967)

- **SHA**: 763bf466adac3d478055c5052cdbdb3f0b3e53b0
- **作者**: bill-srp
- **日期**: 2026-07-20T12:04:56Z
- **PR**: 2967

### 完整 commit message

```
refactor(web): remove retired API routes (#2967)

## Summary

- remove the dedicated Next.js API routes whose consumers were migrated
in #2966
- remove the previously confirmed unused session and debug API routes
- delete route-only tests and stale mock/auth-middleware entries
together with those files

## Rollout blocker

**Do not merge this PR yet.** It is stacked on #2966 and intentionally
remains Draft. Mark it ready only after #2966 has merged, the migrated
frontend has been deployed, and the compatibility window for
already-open tabs using the old bundle has elapsed. After #2966 merges,
rebase this branch onto `main` and change this PR's base to `main`.

## Size override

The diff is 10 additions and 4010 deletions across 66 files. Almost all
volume is whole route files and their route-only tests; splitting these
mechanical deletions by domain would not improve rollout safety, which
is governed by the single compatibility window above.

## Verification

- `bash scripts/verify-web.sh`
  - TypeScript passed
  - 515 Vitest files passed (6935 tests passed, 1 skipped, 1 todo)
  - ESLint and governance guards passed
```

### PR body

## Summary

- remove the dedicated Next.js API routes whose consumers were migrated in #2966
- remove the previously confirmed unused session and debug API routes
- delete route-only tests and stale mock/auth-middleware entries together with those files

## Rollout blocker

**Do not merge this PR yet.** It is stacked on #2966 and intentionally remains Draft. Mark it ready only after #2966 has merged, the migrated frontend has been deployed, and the compatibility window for already-open tabs using the old bundle has elapsed. After #2966 merges, rebase this branch onto `main` and change this PR's base to `main`.

## Size override

The diff is 10 additions and 4010 deletions across 66 files. Almost all volume is whole route files and their route-only tests; splitting these mechanical deletions by domain would not improve rollout safety, which is governed by the single compatibility window above.

## Verification

- `bash scripts/verify-web.sh`
  - TypeScript passed
  - 515 Vitest files passed (6935 tests passed, 1 skipped, 1 todo)
  - ESLint and governance guards passed


---

## feat(landing): refresh homepage prompts and specialists (#2964)

- **SHA**: 67f64e9163077d9ed81ea575e80d85173f81492d
- **作者**: shana-srp
- **日期**: 2026-07-20T11:57:59Z
- **PR**: 2964

### 完整 commit message

```
feat(landing): refresh homepage prompts and specialists (#2964)

## Summary

- refresh the homepage hero/footer typography and English sample prompt
titles
- include PPT template requirements in the login handoff for PPT Master
- expand the specialist picker with official agents, IDs, and avatars
- keep the picker inside the viewport with a measured responsive height
and an independently scrolling option list

## Testing

- `vitest run --config ./vitest.config.mts
tests/unit/app/landing-hero-prompt-editing.unit.spec.tsx` — 11 passed
- targeted ESLint for all changed frontend files — passed
- `git diff --check` — passed
- `bash scripts/verify-web.sh ...` — governance checks and ESLint
passed; full run is blocked locally because the shared dependency tree
is missing `recharts`, and the script's default Node 20 runtime is
incompatible with Vitest 4 (`node:util.styleText`). The same targeted
test passes under the bundled Node 24 runtime.

## Preview

- Local mock preview verified with HTTP 200 at
`http://localhost:3001/en`

---------

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR body

## Summary

- refresh the homepage hero/footer typography and English sample prompt titles
- include PPT template requirements in the login handoff for PPT Master
- expand the specialist picker with official agents, IDs, and avatars
- keep the picker inside the viewport with a measured responsive height and an independently scrolling option list

## Testing

- `vitest run --config ./vitest.config.mts tests/unit/app/landing-hero-prompt-editing.unit.spec.tsx` — 11 passed
- targeted ESLint for all changed frontend files — passed
- `git diff --check` — passed
- `bash scripts/verify-web.sh ...` — governance checks and ESLint passed; full run is blocked locally because the shared dependency tree is missing `recharts`, and the script's default Node 20 runtime is incompatible with Vitest 4 (`node:util.styleText`). The same targeted test passes under the bundled Node 24 runtime.

## Preview

- Local mock preview verified with HTTP 200 at `http://localhost:3001/en`


---

## refactor(web): migrate API calls to claw proxy services (#2966)

- **SHA**: e27ad2d6250e33f16c7475ec30539c51e40dec9c
- **作者**: bill-srp
- **日期**: 2026-07-20T11:53:15Z
- **PR**: 2966

### 完整 commit message

```
refactor(web): migrate API calls to claw proxy services (#2966)

## Summary

- migrate eligible frontend API consumers to typed domain services over
the authenticated claw proxy
- move shared service contracts into `src/models`
- keep the legacy Next.js API routes and route tests during the frontend
rollout compatibility window
- preserve the existing 60-second timeout for runtime skill listing

## Rollout

This is PR 1 of 2 and must deploy before the route-cleanup PR is merged.
Keeping the old routes here allows already-open tabs running the
previous frontend bundle to continue calling them during rollout.

Replaces the migration portion of #2963.

Follow-up route cleanup: #2967 (Draft).

## Size override

The local size gate reports 3777 non-generated lines. Most of the volume
is paired deletion/addition from moving the same domain clients and
tests from `lib/api` into `services` and `models`. This PR stays atomic
because all migrated consumers must land while the old route
compatibility layer remains intact; the route deletions are already
isolated in the follow-up PR.

## Verification

- `bash scripts/verify-web.sh`
  - TypeScript passed
  - 528 Vitest files passed (7040 tests passed, 1 skipped, 1 todo)
  - ESLint and governance guards passed
- confirmed no diff under `web/app/src/app/api` or
`web/app/tests/unit/app/api` versus `origin/main`
```

### PR body

## Summary

- migrate eligible frontend API consumers to typed domain services over the authenticated claw proxy
- move shared service contracts into `src/models`
- keep the legacy Next.js API routes and route tests during the frontend rollout compatibility window
- preserve the existing 60-second timeout for runtime skill listing

## Rollout

This is PR 1 of 2 and must deploy before the route-cleanup PR is merged. Keeping the old routes here allows already-open tabs running the previous frontend bundle to continue calling them during rollout.

Replaces the migration portion of #2963.

Follow-up route cleanup: #2967 (Draft).

## Size override

The local size gate reports 3777 non-generated lines. Most of the volume is paired deletion/addition from moving the same domain clients and tests from `lib/api` into `services` and `models`. This PR stays atomic because all migrated consumers must land while the old route compatibility layer remains intact; the route deletions are already isolated in the follow-up PR.

## Verification

- `bash scripts/verify-web.sh`
  - TypeScript passed
  - 528 Vitest files passed (7040 tests passed, 1 skipped, 1 todo)
  - ESLint and governance guards passed
- confirmed no diff under `web/app/src/app/api` or `web/app/tests/unit/app/api` versus `origin/main`


---

## fix(agent-builder): serialize workspace updates (#2948)

- **SHA**: 5dc2cb0e94e8eb1148df1862eec3c4a637e5593e
- **作者**: sharplee-srp
- **日期**: 2026-07-20T11:38:25Z
- **PR**: 2948

### 完整 commit message

```
fix(agent-builder): serialize workspace updates (#2948)

## Summary
- serialize Agent Studio archive workspace mutation with Agent Builder's
existing `.agent-builder-projects/.workspace.lock`
- keep archive download/extraction outside the critical section, then
bound lock acquisition to 120 seconds
- map `WORKSPACE_BUSY` to a 409-style conflict and surface that retry
hint from failed background updates
- preserve project snapshots during the normal `preserve` update path; a
`clean` overwrite keeps only the lock inode and invalidates stale
snapshots

## Root cause
Agent Builder project materialization already held a workspace lock
while it captured, cleared, and restored live project files. Agent
Studio archive deployment did not participate in that lock. An update
could therefore recreate `scripts/` after materialization cleared the
live workspace but before its restore copied the project snapshot,
causing `FileExistsError` and leaving the project in `failed` state.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] production `preserve`, `clean`, timeout, and workspace-busy
mapping regression selection: 4 passed
- [x] full `test_agent_install_service.py`: 94 passed
- [x] `agent-workspaces.unit.spec.ts`: 11 passed
- [x] backend Ruff, Pyright, and import contracts
- [x] frontend TypeScript, ESLint, and targeted Vitest verification

## Staging validation
An earlier targeted runtime integration was run from a fresh ECAP
devcontainer on A102 against a real staging bot through FastClaw runtime
exec and JuiceFS. It validated the shared lock but used `clean` mode, so
it is not presented as parity coverage for the final production
`preserve` update path or as a browser/UI `Finish update` E2E.

- materialize held the lock first: update waited 1.892s, then completed
successfully
- materialize held the lock beyond the test timeout: update returned
`WORKSPACE_BUSY` with no partial write
- update held the lock first: the materializer observed the lock and
waited 1.717s before entering
- all cases preserved the lock inode and temporary staging
workspace/A102 resources were removed

## Tracking
-
[ECA-1273](https://linear.app/srpone/issue/ECA-1273/agent-builder-%E6%9B%B4%E6%96%B0%E5%90%8E%E5%86%8D%E7%BC%96%E8%BE%91%E5%A4%B1%E8%B4%A5workspace-materialization-errno-17)
```

### PR body

## Summary
- serialize Agent Studio archive workspace mutation with Agent Builder's existing `.agent-builder-projects/.workspace.lock`
- keep archive download/extraction outside the critical section, then bound lock acquisition to 120 seconds
- map `WORKSPACE_BUSY` to a 409-style conflict and surface that retry hint from failed background updates
- preserve project snapshots during the normal `preserve` update path; a `clean` overwrite keeps only the lock inode and invalidates stale snapshots

## Root cause
Agent Builder project materialization already held a workspace lock while it captured, cleared, and restored live project files. Agent Studio archive deployment did not participate in that lock. An update could therefore recreate `scripts/` after materialization cleared the live workspace but before its restore copied the project snapshot, causing `FileExistsError` and leaving the project in `failed` state.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] production `preserve`, `clean`, timeout, and workspace-busy mapping regression selection: 4 passed
- [x] full `test_agent_install_service.py`: 94 passed
- [x] `agent-workspaces.unit.spec.ts`: 11 passed
- [x] backend Ruff, Pyright, and import contracts
- [x] frontend TypeScript, ESLint, and targeted Vitest verification

## Staging validation
An earlier targeted runtime integration was run from a fresh ECAP devcontainer on A102 against a real staging bot through FastClaw runtime exec and JuiceFS. It validated the shared lock but used `clean` mode, so it is not presented as parity coverage for the final production `preserve` update path or as a browser/UI `Finish update` E2E.

- materialize held the lock first: update waited 1.892s, then completed successfully
- materialize held the lock beyond the test timeout: update returned `WORKSPACE_BUSY` with no partial write
- update held the lock first: the materializer observed the lock and waited 1.717s before entering
- all cases preserved the lock inode and temporary staging workspace/A102 resources were removed

## Tracking
- [ECA-1273](https://linear.app/srpone/issue/ECA-1273/agent-builder-%E6%9B%B4%E6%96%B0%E5%90%8E%E5%86%8D%E7%BC%96%E8%BE%91%E5%A4%B1%E8%B4%A5workspace-materialization-errno-17)


---

## docs: add chat UI extraction phase 2 design spec and plan (#2965)

- **SHA**: 478e886df820166a0aefb1ae77ea4d636b6b66c7
- **作者**: bill-srp
- **日期**: 2026-07-20T11:30:01Z
- **PR**: 2965

### 完整 commit message

```
docs: add chat UI extraction phase 2 design spec and plan (#2965)

## Summary
- Phase 2 design spec
(`docs/superpowers/specs/2026-07-20-chat-ui-extraction-phase2-messages-design.md`):
extract the message renderers (`OpenClawAssistantMessage` 458L,
`OpenClawUserMessage` 338L) into `@zooclaw/chat-ui` using the
**view-model + content slots** approach — the package renders complete
messages from plain typed data + a few app-rendered ReactNode slots
(avatar / ermp cards / attachments / share checkbox). No new package
dependencies: no `@assistant-ui/react`, no react-query. Provider gains a
backward-compatible `renderMarkdown(content, ctx?)` (for the 6-prop rich
`MarkdownContent` call) and `locale`. Data-layer stays app-side:
assistant-ui reads, ermp parsing + artifact dedup, avatar identity
(firebase/replay), specialist navigation, turn-status parsing machinery.
- Phase 2 implementation plan
(`docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase2.md`): 9
TDD tasks across the proven extract-then-replace split — PR 2a
(package-only: provider extension, moved pure helpers + turn-status
types, `UserMessage`, `AssistantMessage`, barrel/gate) and PR 2b (bridge
ctx mapping, two container rewrites with zero call-site changes —
`OpenClawThread` untouched, three re-export files, full gates + `/chat`
browser check). The three existing renderer/thread app specs are the
protected regression harness (must pass unchanged).

Follows the merged Phase 1 chain (#2949 spec/plan → #2953 extract →
#2955 replace). Docs only — no code changes; review gate before
implementation starts.

## Test plan
- [ ] N/A (docs only); implementation PRs carry package vitest suites,
`verify-web.sh`, coverage ratchet, `web-build-check`, and a `/chat`
browser mount check
```

### PR body

## Summary
- Phase 2 design spec (`docs/superpowers/specs/2026-07-20-chat-ui-extraction-phase2-messages-design.md`): extract the message renderers (`OpenClawAssistantMessage` 458L, `OpenClawUserMessage` 338L) into `@zooclaw/chat-ui` using the **view-model + content slots** approach — the package renders complete messages from plain typed data + a few app-rendered ReactNode slots (avatar / ermp cards / attachments / share checkbox). No new package dependencies: no `@assistant-ui/react`, no react-query. Provider gains a backward-compatible `renderMarkdown(content, ctx?)` (for the 6-prop rich `MarkdownContent` call) and `locale`. Data-layer stays app-side: assistant-ui reads, ermp parsing + artifact dedup, avatar identity (firebase/replay), specialist navigation, turn-status parsing machinery.
- Phase 2 implementation plan (`docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase2.md`): 9 TDD tasks across the proven extract-then-replace split — PR 2a (package-only: provider extension, moved pure helpers + turn-status types, `UserMessage`, `AssistantMessage`, barrel/gate) and PR 2b (bridge ctx mapping, two container rewrites with zero call-site changes — `OpenClawThread` untouched, three re-export files, full gates + `/chat` browser check). The three existing renderer/thread app specs are the protected regression harness (must pass unchanged).

Follows the merged Phase 1 chain (#2949 spec/plan → #2953 extract → #2955 replace). Docs only — no code changes; review gate before implementation starts.

## Test plan
- [ ] N/A (docs only); implementation PRs carry package vitest suites, `verify-web.sh`, coverage ratchet, `web-build-check`, and a `/chat` browser mount check


---

## refactor(web): replace chat leaf components with @zooclaw/chat-ui (#2955)

- **SHA**: 739fc566135bbb926117dca25585937d22f3085e
- **作者**: bill-srp
- **日期**: 2026-07-20T09:15:08Z
- **PR**: 2955

### 完整 commit message

```
refactor(web): replace chat leaf components with @zooclaw/chat-ui (#2955)

## Summary
Phase 1 (b) of the chat UI extraction — swaps the five app-side chat
leaves to consume `@zooclaw/chat-ui` (merged in #2953), each rewritten
as a thin container **at its existing path with its existing export
shape, so there are zero call-site changes**. Net −848 lines: the
component bodies now live in the package; the app keeps only the
data/service wiring.

Implements Tasks 8–12 of
`docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase1.md`.

What changed in `web/app`:
- **New** `components/chat-ui/ChatUiAppProvider.tsx` — bridges app
services (i18n `t`, `logger`, `MarkdownContent`) into the package's
`ChatUiProvider`. Wrap-per-container for now; hoisting to one provider
is deferred to Phase 3.
- `ToolGroup.tsx` → container over the package `ToolGroup` (i18n via the
bridge).
- `MessageActions.tsx` → re-exports `ActionTooltip` + `copyToClipboard`
from the package (wiring the app `logger`); the hidden null
`MessageActions` stays app-side.
- `QuickActionCards.tsx` → container mapping use-cases to
`QuickActionItem[]`.
- `ModelDegradationBanner.tsx` → container keeping the billing-credit
gating (+ECA-440 comment); passes `variant`/`daysLeft`/`onUpgradeClick`.
- `InteractiveCards.tsx` → container wiring the Mattermost
`doPostAction` transport, replay read-only, and toast.
- `lib/openclaw/types.ts` and
`lib/mattermost/interactive-attachments.ts` now re-export the moved
types from the package (so existing app imports don't churn).

### Deviation (worth a look)
`ChatUiAppProvider` gained a `withTranslation` prop (default `true`).
`InteractiveCards` consumes `renderMarkdown` but never `t`, and its
protected unit spec has no `LanguageProvider`; passing
`withTranslation={false}` wires markdown+logger while skipping the
language-context dependency — functionally identical in prod (it never
translates) and it keeps the protected spec unchanged. The other three
translating containers use the default. The opt-out branch is exercised
indirectly by `InteractiveCards.unit.spec.tsx`; it has no dedicated unit
assertion yet.

## Test plan
- [x] `bash scripts/verify-web.sh`: guards + tsc + vitest (**524 files /
7058 pass**) + eslint — all green
- [x] `pnpm test:unit:coverage`: thresholds hold (stmts 86.82/83,
branches 80.11/75, funcs 85.65/81, lines 89.14/85)
- [x] dependency-cruiser + knip: clean
- [x] Three protected specs (QuickActionCards / ModelDegradationBanner /
InteractiveCards) pass **unchanged**; ToolGroup spec rewritten to a
container-integration test that asserts app `t` flows through the bridge
- [x] Browser mount check on `/chat` (mock stack): app compiles, serves,
and mounts with **no React/provider/component console errors** (only
harness auth-401s from mock-backend port contention in the worktree).
Deep authenticated `/chat` render with seeded chat data not completed
locally — CI `web-build-check` (`next build`) exercises the real tree.
```

### PR body

## Summary
Phase 1 (b) of the chat UI extraction — swaps the five app-side chat leaves to consume `@zooclaw/chat-ui` (merged in #2953), each rewritten as a thin container **at its existing path with its existing export shape, so there are zero call-site changes**. Net −848 lines: the component bodies now live in the package; the app keeps only the data/service wiring.

Implements Tasks 8–12 of `docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase1.md`.

What changed in `web/app`:
- **New** `components/chat-ui/ChatUiAppProvider.tsx` — bridges app services (i18n `t`, `logger`, `MarkdownContent`) into the package's `ChatUiProvider`. Wrap-per-container for now; hoisting to one provider is deferred to Phase 3.
- `ToolGroup.tsx` → container over the package `ToolGroup` (i18n via the bridge).
- `MessageActions.tsx` → re-exports `ActionTooltip` + `copyToClipboard` from the package (wiring the app `logger`); the hidden null `MessageActions` stays app-side.
- `QuickActionCards.tsx` → container mapping use-cases to `QuickActionItem[]`.
- `ModelDegradationBanner.tsx` → container keeping the billing-credit gating (+ECA-440 comment); passes `variant`/`daysLeft`/`onUpgradeClick`.
- `InteractiveCards.tsx` → container wiring the Mattermost `doPostAction` transport, replay read-only, and toast.
- `lib/openclaw/types.ts` and `lib/mattermost/interactive-attachments.ts` now re-export the moved types from the package (so existing app imports don't churn).

### Deviation (worth a look)
`ChatUiAppProvider` gained a `withTranslation` prop (default `true`). `InteractiveCards` consumes `renderMarkdown` but never `t`, and its protected unit spec has no `LanguageProvider`; passing `withTranslation={false}` wires markdown+logger while skipping the language-context dependency — functionally identical in prod (it never translates) and it keeps the protected spec unchanged. The other three translating containers use the default. The opt-out branch is exercised indirectly by `InteractiveCards.unit.spec.tsx`; it has no dedicated unit assertion yet.

## Test plan
- [x] `bash scripts/verify-web.sh`: guards + tsc + vitest (**524 files / 7058 pass**) + eslint — all green
- [x] `pnpm test:unit:coverage`: thresholds hold (stmts 86.82/83, branches 80.11/75, funcs 85.65/81, lines 89.14/85)
- [x] dependency-cruiser + knip: clean
- [x] Three protected specs (QuickActionCards / ModelDegradationBanner / InteractiveCards) pass **unchanged**; ToolGroup spec rewritten to a container-integration test that asserts app `t` flows through the bridge
- [x] Browser mount check on `/chat` (mock stack): app compiles, serves, and mounts with **no React/provider/component console errors** (only harness auth-401s from mock-backend port contention in the worktree). Deep authenticated `/chat` render with seeded chat data not completed locally — CI `web-build-check` (`next build`) exercises the real tree.


---

## fix: stabilize ZooClaw desktop runtime and CWD UI (#2952)

- **SHA**: ebb46ff079a6c08c41969c432abdc19ca8029d2f
- **作者**: zayne-srp
- **日期**: 2026-07-20T08:42:08Z
- **PR**: 2952

### 完整 commit message

```
fix: stabilize ZooClaw desktop runtime and CWD UI (#2952)

## Summary
- flatten staged pnpm dependencies and assert critical Next.js runtime
modules resolve
- persist and migrate the desktop global CWD, and expose the localized
CWD control on new chat
- keep the latest main UI while applying desktop-only ZooClaw logo
assets

## Root cause fixed
The production DMG from zooclaw-desktop v0.1.2 started with a white
screen because the packaged Next.js server could not resolve
`styled-jsx/package.json`. The flattening fix makes that dependency
top-level and fails staging when required runtime packages are
unavailable.

## Verification
- production CI run:
https://github.com/SerendipityOneInc/zooclaw-desktop/actions/runs/29723308516
- macOS and Windows packaging passed
- packaged Next.js runtime smoke gate passed
- Apple Silicon DMG installed locally
- Electron CDP verified a non-empty rendered page (78 body children),
title `ZooClaw — Your Proactive Agent Team`, and no startup exception

Supersedes #2913, whose branch conflicts with current main and would
restore deleted web components.
```

### PR body

## Summary
- flatten staged pnpm dependencies and assert critical Next.js runtime modules resolve
- persist and migrate the desktop global CWD, and expose the localized CWD control on new chat
- keep the latest main UI while applying desktop-only ZooClaw logo assets

## Root cause fixed
The production DMG from zooclaw-desktop v0.1.2 started with a white screen because the packaged Next.js server could not resolve `styled-jsx/package.json`. The flattening fix makes that dependency top-level and fails staging when required runtime packages are unavailable.

## Verification
- production CI run: https://github.com/SerendipityOneInc/zooclaw-desktop/actions/runs/29723308516
- macOS and Windows packaging passed
- packaged Next.js runtime smoke gate passed
- Apple Silicon DMG installed locally
- Electron CDP verified a non-empty rendered page (78 body children), title `ZooClaw — Your Proactive Agent Team`, and no startup exception

Supersedes #2913, whose branch conflicts with current main and would restore deleted web components.

---

## docs: sync-docs weekly sweep (2026-07-20) (#2954)

- **SHA**: f5f63135a25fd85b88cce7d215b8e364cab59c6a
- **作者**: srp-claude-assistant[bot]
- **日期**: 2026-07-20T08:10:35Z
- **PR**: 2954

### 完整 commit message

```
docs: sync-docs weekly sweep (2026-07-20) (#2954)

## Tier 1 — Deterministic fixes
None — drift-probe reported clean before and after.

## Tier 2 — Semantic fixes (evidence-grounded)

### 1. `code-quality.yml` description missing WhatsApp Business Service
**Evidence**: `.github/workflows/code-quality.yml` — trigger `paths:`
now includes `services/whatsapp-business-service/**` and a new
`whatsapp-business-service-quality` job was added (commit `e6d5801db`,
CI diff in anchor window).
**Fix**: Updated the CI/CD workflows table description to include
`services/whatsapp-business-service/**` in trigger paths and WhatsApp
Business Service (TypeScript) in the "What it does" column.

### 2. Missing `deploy-r2-access-worker.yml` in CI/CD workflows table
**Evidence**: `.github/workflows/deploy-r2-access-worker.yml` was added
in the anchor window (commit `034060212` added
`deploy-r2-access-worker.yml` to diff stat). The workflow deploys
`r2-access-worker` on tag `r2-access-worker-v*-release` or push to
`main`. It was absent from the CI/CD Workflows Overview table.
**Fix**: Added a row for `deploy-r2-access-worker.yml` to the CI/CD
workflows table.

### 3. Missing `r2-access-worker` in Tag Conventions table
**Evidence**: Same — `deploy-r2-access-worker.yml` introduces a new
`r2-access-worker-v*-release` tag convention. This surface is listed in
the Services table and Deployment Targets table but was absent from the
Tag Conventions table.
**Fix**: Added `R2 Access Worker` row to the Tag Conventions table with
its `r2-access-worker-v*` prefix.

## Tier 3 — Suggestions (not applied)

- **`desktop/` app not documented** — A `desktop/` (Electron,
`zooclaw-desktop`) directory exists with its own `electron-builder.yml`,
`main/`, `build/` and active CI changes in this window. It is not
mentioned in the README web-apps table, project structure tree, or any
AGENTS.md. This is likely an onboarding-relevant surface but the scope
is unclear (is it GA? internal? how does it deploy?). Suggest a
dedicated pass to add the desktop app once its status is confirmed.
- **`services/claw-interface/AGENTS.md` Monorepo Context table** —
references `ecap-agent-platform (external)` at port 8001.
`AGENT_PLATFORM_URL` is still used in `app/settings.py` and test code.
This may be outdated (no production evidence either way) but not
definitively wrong — downgrading to Tier 3.
- **`web/AGENTS.md` packages list** — mentions `auth-client, chat-ui`
but a third package `zooclaw-design-system` (commit `9d021a487` — expand
zooclaw preview foundations) now exists at
`web/packages/zooclaw-design-system/`. The parenthetical `(auth-client,
chat-ui, …)` already uses `…` so this is not wrong, just incomplete. Low
onboarding impact given the `…` placeholder.

---

**Docs changed:** `README.md`  
**Anchor window reviewed:** `c69e3bd..HEAD` (~90 days, 160+ commits)

Co-authored-by: ecap-bot <ecap-bot@users.noreply.github.com>
```

### PR body

## Tier 1 — Deterministic fixes
None — drift-probe reported clean before and after.

## Tier 2 — Semantic fixes (evidence-grounded)

### 1. `code-quality.yml` description missing WhatsApp Business Service
**Evidence**: `.github/workflows/code-quality.yml` — trigger `paths:` now includes `services/whatsapp-business-service/**` and a new `whatsapp-business-service-quality` job was added (commit `e6d5801db`, CI diff in anchor window).  
**Fix**: Updated the CI/CD workflows table description to include `services/whatsapp-business-service/**` in trigger paths and WhatsApp Business Service (TypeScript) in the "What it does" column.

### 2. Missing `deploy-r2-access-worker.yml` in CI/CD workflows table
**Evidence**: `.github/workflows/deploy-r2-access-worker.yml` was added in the anchor window (commit `034060212` added `deploy-r2-access-worker.yml` to diff stat). The workflow deploys `r2-access-worker` on tag `r2-access-worker-v*-release` or push to `main`. It was absent from the CI/CD Workflows Overview table.  
**Fix**: Added a row for `deploy-r2-access-worker.yml` to the CI/CD workflows table.

### 3. Missing `r2-access-worker` in Tag Conventions table
**Evidence**: Same — `deploy-r2-access-worker.yml` introduces a new `r2-access-worker-v*-release` tag convention. This surface is listed in the Services table and Deployment Targets table but was absent from the Tag Conventions table.  
**Fix**: Added `R2 Access Worker` row to the Tag Conventions table with its `r2-access-worker-v*` prefix.

## Tier 3 — Suggestions (not applied)

- **`desktop/` app not documented** — A `desktop/` (Electron, `zooclaw-desktop`) directory exists with its own `electron-builder.yml`, `main/`, `build/` and active CI changes in this window. It is not mentioned in the README web-apps table, project structure tree, or any AGENTS.md. This is likely an onboarding-relevant surface but the scope is unclear (is it GA? internal? how does it deploy?). Suggest a dedicated pass to add the desktop app once its status is confirmed.
- **`services/claw-interface/AGENTS.md` Monorepo Context table** — references `ecap-agent-platform (external)` at port 8001. `AGENT_PLATFORM_URL` is still used in `app/settings.py` and test code. This may be outdated (no production evidence either way) but not definitively wrong — downgrading to Tier 3.
- **`web/AGENTS.md` packages list** — mentions `auth-client, chat-ui` but a third package `zooclaw-design-system` (commit `9d021a487` — expand zooclaw preview foundations) now exists at `web/packages/zooclaw-design-system/`. The parenthetical `(auth-client, chat-ui, …)` already uses `…` so this is not wrong, just incomplete. Low onboarding impact given the `…` placeholder.

---

**Docs changed:** `README.md`  
**Anchor window reviewed:** `c69e3bd..HEAD` (~90 days, 160+ commits)


---

## docs(agents): engine agent channels v1 spec and E1-E4 plans (#2951)

- **SHA**: 419b5a7acfa7b3a5b91a37463a42bff070241133
- **作者**: bill-srp
- **日期**: 2026-07-20T07:57:28Z
- **PR**: 2951

### 完整 commit message

```
docs(agents): engine agent channels v1 spec and E1-E4 plans (#2951)

## Summary

Design spec + four slice plans for **engine agent channels v1**
(ECA-1279) — giving installed engine agents external IM channel parity
(Slack, Feishu, Weixin, WeCom), managed per-workspace through the
agent-channel-service (ACS). **Docs only — no implementation in this
PR.** Review gate before any code is written.

Linear: https://linear.app/srpone/issue/ECA-1279
Roadmap: sequenced immediately after the agents-v2 phase-2 PRs
(#2934/#2935), before the web release + allowlist widening.

## What's here

- `docs/superpowers/specs/2026-07-20-engine-agent-channels-design.md` —
the spec.
-
`docs/superpowers/plans/2026-07-20-engine-channels-e1-backend-slack.md`
— backend route family + ACS-backed service + Slack end-to-end +
computer-leg 400 + mock handlers.
- `...-e2-sink-feishu.md` — channel-sink refactor
(`BotChannelSink`/`AcsChannelSink`) + Feishu on the engine leg.
- `...-e3-weixin-wecom.md` — WeCom + Weixin engine leg (Weixin's
compensation saga collapses to one step on the ACS side).
- `...-e4-frontend-hub.md` — claw-settings hub extension: engine
workspaces as channel targets, allowlist-gated BFF proxies,
target-branched wizards.

## Locked decisions (from brainstorming)

- **Full channel parity via ACS. No new DB collection** — ACS is the
sole system of record; claw-interface reads through per-agent
(`list_agent_channels`) and writes through
(`create/update/delete_channel`). Redis keeps setup sessions.
- **Unified `/agents/{workspace_id}/channels*` route family** (GET/POST
only), engine leg first; computer leg returns
`channel.runtime_not_supported` (400) in v1.
- **Platforms v1: Slack, Feishu, Weixin, WeCom.** Deferred: WhatsApp,
Telegram, Discord, DingTalk, Teams.
- **UI extends the claw-settings Channels hub** — no new surface; engine
workspaces become first-class targets. BFF gated by the existing
`AGENTS_V2_EMAIL_ALLOWLIST`.
- **Channel-sink abstraction** cuts at the one openclaw-coupled seam
(terminal channel write); the Feishu/Weixin/WeCom QR+session dances
already live in claw-interface and are reused unchanged, with a
zero-bot-leg-test-edits invariant as reviewable evidence.

## Blocking dependencies (engine team, before implementation)

1. zooclaw-engine actually runs Slack/Feishu/Weixin/WeCom channels from
ACS-managed config (the Mattermost bind proves the mechanism, not these
four platforms).
2. ACS channel status semantics (field/values/transitions) — feeds
`StatusBadge` and the P2-5 status chips.

## Review asks

- Slicing / sequencing sanity (E1 unblocks E4-Slack; E2/E3 light up
platforms behind the same target branch).
- The Weixin compensation-collapse rationale (multi-write saga → single
`delete_channel` on the ACS leg).
- The BFF gate extraction (install route + channels routes share one
`requireChannelsAllowlisted` helper).
```

### PR body

## Summary

Design spec + four slice plans for **engine agent channels v1** (ECA-1279) — giving installed engine agents external IM channel parity (Slack, Feishu, Weixin, WeCom), managed per-workspace through the agent-channel-service (ACS). **Docs only — no implementation in this PR.** Review gate before any code is written.

Linear: https://linear.app/srpone/issue/ECA-1279
Roadmap: sequenced immediately after the agents-v2 phase-2 PRs (#2934/#2935), before the web release + allowlist widening.

## What's here

- `docs/superpowers/specs/2026-07-20-engine-agent-channels-design.md` — the spec.
- `docs/superpowers/plans/2026-07-20-engine-channels-e1-backend-slack.md` — backend route family + ACS-backed service + Slack end-to-end + computer-leg 400 + mock handlers.
- `...-e2-sink-feishu.md` — channel-sink refactor (`BotChannelSink`/`AcsChannelSink`) + Feishu on the engine leg.
- `...-e3-weixin-wecom.md` — WeCom + Weixin engine leg (Weixin's compensation saga collapses to one step on the ACS side).
- `...-e4-frontend-hub.md` — claw-settings hub extension: engine workspaces as channel targets, allowlist-gated BFF proxies, target-branched wizards.

## Locked decisions (from brainstorming)

- **Full channel parity via ACS. No new DB collection** — ACS is the sole system of record; claw-interface reads through per-agent (`list_agent_channels`) and writes through (`create/update/delete_channel`). Redis keeps setup sessions.
- **Unified `/agents/{workspace_id}/channels*` route family** (GET/POST only), engine leg first; computer leg returns `channel.runtime_not_supported` (400) in v1.
- **Platforms v1: Slack, Feishu, Weixin, WeCom.** Deferred: WhatsApp, Telegram, Discord, DingTalk, Teams.
- **UI extends the claw-settings Channels hub** — no new surface; engine workspaces become first-class targets. BFF gated by the existing `AGENTS_V2_EMAIL_ALLOWLIST`.
- **Channel-sink abstraction** cuts at the one openclaw-coupled seam (terminal channel write); the Feishu/Weixin/WeCom QR+session dances already live in claw-interface and are reused unchanged, with a zero-bot-leg-test-edits invariant as reviewable evidence.

## Blocking dependencies (engine team, before implementation)

1. zooclaw-engine actually runs Slack/Feishu/Weixin/WeCom channels from ACS-managed config (the Mattermost bind proves the mechanism, not these four platforms).
2. ACS channel status semantics (field/values/transitions) — feeds `StatusBadge` and the P2-5 status chips.

## Review asks

- Slicing / sequencing sanity (E1 unblocks E4-Slack; E2/E3 light up platforms behind the same target branch).
- The Weixin compensation-collapse rationale (multi-write saga → single `delete_channel` on the ACS leg).
- The BFF gate extraction (install route + channels routes share one `requireChannelsAllowlisted` helper).


---

## refactor(chat-ui): extract chat leaf components into @zooclaw/chat-ui (#2953)

- **SHA**: 8c19af1800e2036ca88b6f2cd91fc77e6e982ab6
- **作者**: bill-srp
- **日期**: 2026-07-20T07:46:46Z
- **PR**: 2953

### 完整 commit message

```
refactor(chat-ui): extract chat leaf components into @zooclaw/chat-ui (#2953)

## Summary
Phase 1 (a) of the chat UI extraction — **package-only, `web/app` is
untouched**. Adds prop-driven chat components to `@zooclaw/chat-ui`
behind a new `ChatUiProvider`; app call sites are swapped in the
follow-up PR 1b.

Implements Tasks 1–7 of
`docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase1.md`
(design:
`docs/superpowers/specs/2026-07-20-chat-ui-extraction-design.md`).

What's added to `web/packages/chat-ui`:
- `ChatUiProvider` / `useChatUiConfig` — config context for `t` (i18n),
`logger`, and `renderMarkdown`, each with standalone defaults so the
package renders without an app harness.
- `ToolGroup` (+ `ToolStep` type) — prop-driven; `t` now comes from the
provider.
- `InteractiveCards` (+ card view types + a package-local `CardSelect`)
— transport injected via `onAction`/`onActionError`; a resolved action
keeps controls disabled (post-edit is the done-state), a rejected one
re-enables.
- `QuickActionCards` — items-as-props; use-case selection stays
app-side.
- `ModelDegradationBanner` — `variant`/`daysLeft` as props;
billing-credit gating stays app-side.
- `ActionTooltip` primitive + `copyToClipboard(content, logger?)` util
(extracted from `MessageActions.tsx`; the hidden null `MessageActions`
component stays app-side).
- Barrel exports + extended module-structure test.

Components were copied from the app sources with only the prescribed
provider/prop edits — Tailwind class strings, `data-testid`s,
translation keys, and rendered DOM are preserved so PR 1b's containers
are drop-in.

## Test plan
- [x] Package gate: `pnpm tsc` clean, `pnpm lint` zero warnings, `pnpm
test` **187/187** (14 files; +52 new tests)
- [x] `git diff origin/main..HEAD --stat -- web/app` empty
(package-only)
- [x] Ported components diffed against app sources — only the documented
provider/prop edits differ
- [ ] PR 1b will wire these into `web/app` containers and run
`verify-web.sh` + a `/chat` mock-stack smoke
```

### PR body

## Summary
Phase 1 (a) of the chat UI extraction — **package-only, `web/app` is untouched**. Adds prop-driven chat components to `@zooclaw/chat-ui` behind a new `ChatUiProvider`; app call sites are swapped in the follow-up PR 1b.

Implements Tasks 1–7 of `docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase1.md` (design: `docs/superpowers/specs/2026-07-20-chat-ui-extraction-design.md`).

What's added to `web/packages/chat-ui`:
- `ChatUiProvider` / `useChatUiConfig` — config context for `t` (i18n), `logger`, and `renderMarkdown`, each with standalone defaults so the package renders without an app harness.
- `ToolGroup` (+ `ToolStep` type) — prop-driven; `t` now comes from the provider.
- `InteractiveCards` (+ card view types + a package-local `CardSelect`) — transport injected via `onAction`/`onActionError`; a resolved action keeps controls disabled (post-edit is the done-state), a rejected one re-enables.
- `QuickActionCards` — items-as-props; use-case selection stays app-side.
- `ModelDegradationBanner` — `variant`/`daysLeft` as props; billing-credit gating stays app-side.
- `ActionTooltip` primitive + `copyToClipboard(content, logger?)` util (extracted from `MessageActions.tsx`; the hidden null `MessageActions` component stays app-side).
- Barrel exports + extended module-structure test.

Components were copied from the app sources with only the prescribed provider/prop edits — Tailwind class strings, `data-testid`s, translation keys, and rendered DOM are preserved so PR 1b's containers are drop-in.

## Test plan
- [x] Package gate: `pnpm tsc` clean, `pnpm lint` zero warnings, `pnpm test` **187/187** (14 files; +52 new tests)
- [x] `git diff origin/main..HEAD --stat -- web/app` empty (package-only)
- [x] Ported components diffed against app sources — only the documented provider/prop edits differ
- [ ] PR 1b will wire these into `web/app` containers and run `verify-web.sh` + a `/chat` mock-stack smoke


---

## fix(chat): group ordered assistant reply segments (#2950)

- **SHA**: 462ae45974faaa5a4a537132676673865ea59867
- **作者**: kaka-srp
- **日期**: 2026-07-20T07:28:41Z
- **PR**: 2950

### 完整 commit message

```
fix(chat): group ordered assistant reply segments (#2950)

## 背景

Mattermost 按真实顺序分别投递中间文本、工具状态和最终文本。前端此前把这些物理消息渲染成多次独立 agent
回复，重复展示头像和名称；仅比较紧邻消息还会让 tool-first 回复完全没有 agent 身份。当前仍有部署在 K8s、尚未切换
ZooClaw Engine 的旧 OpenClaw bot，因此新归组规则必须保留无 run_id 消息的原有展示行为。

## 改动

- 从 Mattermost post props 读取 run_id、turn 和 segment，并传入 assistant-ui
message metadata。
- 有 run_id 时，在同一 run 内向前跨过 tool group 查找已有文本段，只在已经展示过 assistant
身份时隐藏后续头像和名称。
- tool → text 保留最终文本的头像和名称。
- text → tool → text 只展示一次 assistant 身份，同时保持三段消息的真实顺序。
- 没有 run_id 时保留旧 OpenClaw 的紧邻 assistant 归组行为，tool group 仍作为边界。
- 新旧消息格式交界、不同 run 之间均不归组，避免误合并。

## 验证

- bash scripts/verify-web.sh 相关文件
- 原实现相关 133 tests passed
- 兼容加固后 OpenClawThread 38 tests passed
- TypeScript、eslint 和全部治理 guards 通过
- agent review 最终无剩余 actionable finding

## 关联

- Linear:
https://linear.app/srpone/issue/ECA-1278/fix-mattermost-reply-grouping-and-output-ack-delay
- ACS 配套 PR:
https://github.com/SerendipityOneInc/agent-channel-service/pull/34
```

### PR body

## 背景

Mattermost 按真实顺序分别投递中间文本、工具状态和最终文本。前端此前把这些物理消息渲染成多次独立 agent 回复，重复展示头像和名称；仅比较紧邻消息还会让 tool-first 回复完全没有 agent 身份。当前仍有部署在 K8s、尚未切换 ZooClaw Engine 的旧 OpenClaw bot，因此新归组规则必须保留无 run_id 消息的原有展示行为。

## 改动

- 从 Mattermost post props 读取 run_id、turn 和 segment，并传入 assistant-ui message metadata。
- 有 run_id 时，在同一 run 内向前跨过 tool group 查找已有文本段，只在已经展示过 assistant 身份时隐藏后续头像和名称。
- tool → text 保留最终文本的头像和名称。
- text → tool → text 只展示一次 assistant 身份，同时保持三段消息的真实顺序。
- 没有 run_id 时保留旧 OpenClaw 的紧邻 assistant 归组行为，tool group 仍作为边界。
- 新旧消息格式交界、不同 run 之间均不归组，避免误合并。

## 验证

- bash scripts/verify-web.sh 相关文件
- 原实现相关 133 tests passed
- 兼容加固后 OpenClawThread 38 tests passed
- TypeScript、eslint 和全部治理 guards 通过
- agent review 最终无剩余 actionable finding

## 关联

- Linear: https://linear.app/srpone/issue/ECA-1278/fix-mattermost-reply-grouping-and-output-ack-delay
- ACS 配套 PR: https://github.com/SerendipityOneInc/agent-channel-service/pull/34

---

## docs: add chat UI extraction design spec and phase 1 plan (#2949)

- **SHA**: 985dc6bcf6c3f3a2d214c5328d37687ba969a377
- **作者**: bill-srp
- **日期**: 2026-07-20T06:47:22Z
- **PR**: 2949

### 完整 commit message

```
docs: add chat UI extraction design spec and phase 1 plan (#2949)

## Summary
- Design spec
(`docs/superpowers/specs/2026-07-20-chat-ui-extraction-design.md`): make
the chat UI reusable by other surfaces by growing the existing
`@zooclaw/chat-ui` package — props in / callbacks out, data layer stays
in `web/app`. Cross-cutting adapters (i18n `t`, logger,
`renderMarkdown`) go through a new `ChatUiProvider`. Migration is
extract-first-then-replace: each phase is an (a) package-only extract PR
followed immediately by a (b) app-side replace PR.
- Phase 1 implementation plan
(`docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase1.md`): 13
bite-sized TDD tasks covering PR 1a (ChatUiProvider + ToolGroup +
InteractiveCards + QuickActionCards + ModelDegradationBanner +
ActionTooltip/copyToClipboard, with ported/new vitest suites) and PR 1b
(app files rewritten as thin containers at their existing paths with
unchanged export shapes — zero call-site changes; existing app specs
stay as the regression harness).

Docs only — no code changes. Review gate before implementation starts.

## Test plan
- [ ] N/A (docs only); implementation PRs carry their own package vitest
suites, `verify-web.sh`, coverage ratchet check, and a mock-stack visual
smoke of `/chat`
```

### PR body

## Summary
- Design spec (`docs/superpowers/specs/2026-07-20-chat-ui-extraction-design.md`): make the chat UI reusable by other surfaces by growing the existing `@zooclaw/chat-ui` package — props in / callbacks out, data layer stays in `web/app`. Cross-cutting adapters (i18n `t`, logger, `renderMarkdown`) go through a new `ChatUiProvider`. Migration is extract-first-then-replace: each phase is an (a) package-only extract PR followed immediately by a (b) app-side replace PR.
- Phase 1 implementation plan (`docs/superpowers/plans/2026-07-20-chat-ui-extraction-phase1.md`): 13 bite-sized TDD tasks covering PR 1a (ChatUiProvider + ToolGroup + InteractiveCards + QuickActionCards + ModelDegradationBanner + ActionTooltip/copyToClipboard, with ported/new vitest suites) and PR 1b (app files rewritten as thin containers at their existing paths with unchanged export shapes — zero call-site changes; existing app specs stay as the regression harness).

Docs only — no code changes. Review gate before implementation starts.

## Test plan
- [ ] N/A (docs only); implementation PRs carry their own package vitest suites, `verify-web.sh`, coverage ratchet check, and a mock-stack visual smoke of `/chat`


---

## fix(web): align landing header with footer (#2947)

- **SHA**: 89f1d9ecc38fa14a71e954ab0c96071fc4fe3ae5
- **作者**: shana-srp
- **日期**: 2026-07-20T06:29:31Z
- **PR**: 2947

### 完整 commit message

```
fix(web): align landing header with footer (#2947)

## Summary
- keep the landing header background full-width on wide viewports
- align the header logo and actions with the footer's centered content
grid
- reuse the footer's responsive horizontal padding at desktop, tablet,
and mobile widths

## Root cause
The header element doubled as both the full-width background and the
constrained content container. Its previous 1600px maximum width exposed
the page background on wider screens; removing that constraint alone
moved the header content out of alignment with the footer.

## Test plan
- [x] `bash scripts/verify-web.sh
web/app/src/app/landing/components/LandingHeader.tsx`
- [x] `pnpm exec vitest run --config ./vitest.config.mts
tests/unit/app/landing-header.unit.spec.tsx` (3 tests)
- [x] local mock preview returned HTTP 200 and was visually reviewed at
wide viewport width

Co-authored-by: shiyang <shiyang@shiyangdeMacBook-Pro.local>
```

### PR body

## Summary
- keep the landing header background full-width on wide viewports
- align the header logo and actions with the footer's centered content grid
- reuse the footer's responsive horizontal padding at desktop, tablet, and mobile widths

## Root cause
The header element doubled as both the full-width background and the constrained content container. Its previous 1600px maximum width exposed the page background on wider screens; removing that constraint alone moved the header content out of alignment with the footer.

## Test plan
- [x] `bash scripts/verify-web.sh web/app/src/app/landing/components/LandingHeader.tsx`
- [x] `pnpm exec vitest run --config ./vitest.config.mts tests/unit/app/landing-header.unit.spec.tsx` (3 tests)
- [x] local mock preview returned HTTP 200 and was visually reviewed at wide viewport width


---

## refactor(web): route installed agent chats by workspace id (#2935)

- **SHA**: f268e2f9911335e798f245f8f869bfb1d4ddf9f9
- **作者**: bill-srp
- **日期**: 2026-07-20T06:12:56Z
- **PR**: 2935

### 完整 commit message

```
refactor(web): route installed agent chats by workspace id (#2935)

## Summary

Reworks the chat routing model so first-party navigation no longer
depends on runtime `agent_id` values or Agent Pack catalog availability.

### Route contracts

- New in-app links use the installed Agent row's `workspace_id`:
  - `/chat?workspace_id=<workspace_id>`
  - `/new-chat?workspace_id=<workspace_id>`
- Legacy external `/chat?agent_id=<public-pack-reference>` links remain
supported, but resolve only through:
  - Agent Pack catalog lookup by `display_id` or immutable `pack_id`
  - canonical `pack_id`
  - the current user's installed Agent row with that `pack_id`
- A legacy query value is never matched directly against a runtime
`agent_id`.
- If both parameters are present, `workspace_id` wins and the legacy
hire flow is not started.

### First-party migration

- Side navigation chat, Session History, and New Task links
- New Chat preselection and Engine post-send navigation
- Agents Manager list/detail Start Chat actions
- Agents Manager and Publish install-success actions

Plain Main Agent routes and path-based conversation URLs remain
unchanged. External landing/share handoffs and assistant specialist-card
payloads remain on the legacy `agent_id` compatibility boundary.

### Lifecycle behavior

Existing Engine transient/terminal gates are preserved after the
installed row resolves. An unknown first-party `workspace_id` no longer
falls back to Main: it remains transient while Agent rows load and
becomes terminal once loading settles.

The detailed contract is documented in
`docs/superpowers/specs/2026-07-17-chat-workspace-route-identity-design.md`.

## Test plan

- [x] RED → GREEN coverage for workspace routing, legacy Pack
resolution, parameter precedence, and runtime-ID rejection
- [x] Link/component coverage for SideNav, New Chat, Agents Manager,
Agent Detail, and Publish
- [x] Runtime-conflict regression: Engine navigation selects the Engine
row even when a stale same-pack Computer row precedes it
- [x] `bash scripts/verify-web.sh` — 529 files passed, 7054 tests
passed, TypeScript and ESLint passed
- [x] Merged latest `origin/main`
- [x] `bash scripts/verify-changed.sh`
- [x] Post-merge targeted regression — 11 files, 325 tests passed
```

### PR body

## Summary

Reworks the chat routing model so first-party navigation no longer depends on runtime `agent_id` values or Agent Pack catalog availability.

### Route contracts

- New in-app links use the installed Agent row's `workspace_id`:
  - `/chat?workspace_id=<workspace_id>`
  - `/new-chat?workspace_id=<workspace_id>`
- Legacy external `/chat?agent_id=<public-pack-reference>` links remain supported, but resolve only through:
  - Agent Pack catalog lookup by `display_id` or immutable `pack_id`
  - canonical `pack_id`
  - the current user's installed Agent row with that `pack_id`
- A legacy query value is never matched directly against a runtime `agent_id`.
- If both parameters are present, `workspace_id` wins and the legacy hire flow is not started.

### First-party migration

- Side navigation chat, Session History, and New Task links
- New Chat preselection and Engine post-send navigation
- Agents Manager list/detail Start Chat actions
- Agents Manager and Publish install-success actions

Plain Main Agent routes and path-based conversation URLs remain unchanged. External landing/share handoffs and assistant specialist-card payloads remain on the legacy `agent_id` compatibility boundary.

### Lifecycle behavior

Existing Engine transient/terminal gates are preserved after the installed row resolves. An unknown first-party `workspace_id` no longer falls back to Main: it remains transient while Agent rows load and becomes terminal once loading settles.

The detailed contract is documented in `docs/superpowers/specs/2026-07-17-chat-workspace-route-identity-design.md`.

## Test plan

- [x] RED → GREEN coverage for workspace routing, legacy Pack resolution, parameter precedence, and runtime-ID rejection
- [x] Link/component coverage for SideNav, New Chat, Agents Manager, Agent Detail, and Publish
- [x] Runtime-conflict regression: Engine navigation selects the Engine row even when a stale same-pack Computer row precedes it
- [x] `bash scripts/verify-web.sh` — 529 files passed, 7054 tests passed, TypeScript and ESLint passed
- [x] Merged latest `origin/main`
- [x] `bash scripts/verify-changed.sh`
- [x] Post-merge targeted regression — 11 files, 325 tests passed


---

## feat(web): branch agent uninstall and update on workspace runtime (#2934)

- **SHA**: 0194f81197df810a324eebc0348710f755d096ed
- **作者**: bill-srp
- **日期**: 2026-07-20T04:06:17Z
- **PR**: 2934

### 完整 commit message

```
feat(web): branch agent uninstall and update on workspace runtime (#2934)

## Summary

**Agents v2 phase 2, P2-3** — lifecycle branching. Uninstall and update
now work for engine agents: the lifecycle initiators branch on the
workspace row's `runtime` — engine rows use the existing authenticated
claw proxy for `/agents/{workspace_id}/uninstall|update`, while computer
rows keep the v1 leg byte-for-byte. This also delivers the error-row
recovery flagged by #2927's review: a stuck engine row (`error` /
`install_failed`) is now removable from the UI.

Spec: `docs/superpowers/specs/2026-07-16-agents-v2-install-phase2.md`
(locked decision: lifecycle branches on row `runtime`, client-passed as
routing info — wrong routing fails safe via ownership-scoped 404; no
allowlist involvement)
Plan:
`docs/superpowers/plans/2026-07-17-agents-v2-p2-3-lifecycle-branching.md`
Linear: https://linear.app/srpone/issue/ECA-1259/... (phase-2 successor
work)

### Backend semantics (verified read-only before implementation)

Engine uninstall/update are SYNCHRONOUS — uninstall returns terminal
`uninstalled`/`deleted`, update returns `active` — so the engine leg
needs no polling. Uninstall is accepted from `error` and post-creation
`install_failed` rows (the recovery case); update only from `active`.
Early `install_failed` rows without a persisted identity are excluded
from the unified list and can't reach this path.

### What's in it

- **Shared claw proxy lifecycle calls**: `uninstallEngineAgent` /
`updateEngineAgent` call
`/api/claw/agents/{workspaceId}/uninstall|update` through
`callClawInterfaceAPI`; the two redundant one-line lifecycle BFF routes
and their route-only tests were removed. The install start route keeps
its dedicated BFF because it owns install-specific policy.
- **Client helpers** (`src/services/agent-install.ts`): no polling (sync
backend), with best-effort unified-cache refresh scoped to the
initiating uid. The claw proxy's 30s timeout is intentional; work that
cannot meet it must become async rather than approach Cloudflare's 100s
synchronous connection ceiling.
- **Branching**: `useAgentActions.fireAgent`/`updateAgent` and publish's
`useAgentInstallToggle`/`useAgentUpdateAction` branch on the row's
runtime — engine ops use the exact unified-row `workspace_id`, fail fast
with domain errors, and ignore unrelated computer/WebSocket readiness;
computer flows (waits, refreshes, sentinels) are byte-identical.
- **Lifecycle UI gates lifted** on manager/detail/publish: engine rows
expose uninstall from `error` and addressable post-creation
`install_failed` rows, and update only from `active` rows. Fire/update
confirmation revalidates against the latest workspace row; engine update
never routes into the computer-only `/new`-chat flow.
- **Stateful mock**: engine uninstall/update lifecycle in the mock
backend (update advances `submission_id`, clears stale errors; recovery
statuses covered).

### Deliberately out

Start/stop UI (spec-deferred; `startEngineAgent` exists from P2-2),
AgentBuilderClient (dedicated builder computer — always v1), bossclaw +
landing (deferred initiators), vertical-pack, engine settings panel
(P2-5).

### Rollout

Frontend only; backend routes already live (#2871/#2923). Engine legs
only trigger for rows that already exist as engine installs (allowlisted
dogfood). Concurrent-PR note: developed in parallel with #2932 (engine
chat) on disjoint function surfaces of the shared files; whichever
merges second absorbs main normally.

Size override rationale: after consolidating duplicate review tests,
this coherent lifecycle slice is 3,104 counted lines, 104 lines (3.5%)
over the 3,000-line threshold. Splitting it would separate the shared
selector/action-eligibility/cache-scope contracts from their
manager/detail/publish consumers and regression coverage.

## Test plan

- [x] Task-1 read-only backend semantics verification (report
in-worktree)
- [x] TDD review regression run: 5 spec files / 218 tests green (6
targeted failures observed before implementation)
- [x] `bash scripts/verify-web.sh` — full guards + tsc + 523 unit files
(7021 passed, 1 skipped, 1 todo) + eslint
- [x] Coverage over thresholds; knip clean; jscpd (`--no-gitignore` real
runs) under thresholds
- [ ] CI `code-quality / lint-and-test`
- [ ] Staging: engine uninstall of an `error` row + update of an
`active` row (recovery + happy path)
```

### PR body

## Summary

**Agents v2 phase 2, P2-3** — lifecycle branching. Uninstall and update now work for engine agents: the lifecycle initiators branch on the workspace row's `runtime` — engine rows use the existing authenticated claw proxy for `/agents/{workspace_id}/uninstall|update`, while computer rows keep the v1 leg byte-for-byte. This also delivers the error-row recovery flagged by #2927's review: a stuck engine row (`error` / `install_failed`) is now removable from the UI.

Spec: `docs/superpowers/specs/2026-07-16-agents-v2-install-phase2.md` (locked decision: lifecycle branches on row `runtime`, client-passed as routing info — wrong routing fails safe via ownership-scoped 404; no allowlist involvement)
Plan: `docs/superpowers/plans/2026-07-17-agents-v2-p2-3-lifecycle-branching.md`
Linear: https://linear.app/srpone/issue/ECA-1259/... (phase-2 successor work)

### Backend semantics (verified read-only before implementation)

Engine uninstall/update are SYNCHRONOUS — uninstall returns terminal `uninstalled`/`deleted`, update returns `active` — so the engine leg needs no polling. Uninstall is accepted from `error` and post-creation `install_failed` rows (the recovery case); update only from `active`. Early `install_failed` rows without a persisted identity are excluded from the unified list and can't reach this path.

### What's in it

- **Shared claw proxy lifecycle calls**: `uninstallEngineAgent` / `updateEngineAgent` call `/api/claw/agents/{workspaceId}/uninstall|update` through `callClawInterfaceAPI`; the two redundant one-line lifecycle BFF routes and their route-only tests were removed. The install start route keeps its dedicated BFF because it owns install-specific policy.
- **Client helpers** (`src/services/agent-install.ts`): no polling (sync backend), with best-effort unified-cache refresh scoped to the initiating uid. The claw proxy's 30s timeout is intentional; work that cannot meet it must become async rather than approach Cloudflare's 100s synchronous connection ceiling.
- **Branching**: `useAgentActions.fireAgent`/`updateAgent` and publish's `useAgentInstallToggle`/`useAgentUpdateAction` branch on the row's runtime — engine ops use the exact unified-row `workspace_id`, fail fast with domain errors, and ignore unrelated computer/WebSocket readiness; computer flows (waits, refreshes, sentinels) are byte-identical.
- **Lifecycle UI gates lifted** on manager/detail/publish: engine rows expose uninstall from `error` and addressable post-creation `install_failed` rows, and update only from `active` rows. Fire/update confirmation revalidates against the latest workspace row; engine update never routes into the computer-only `/new`-chat flow.
- **Stateful mock**: engine uninstall/update lifecycle in the mock backend (update advances `submission_id`, clears stale errors; recovery statuses covered).

### Deliberately out

Start/stop UI (spec-deferred; `startEngineAgent` exists from P2-2), AgentBuilderClient (dedicated builder computer — always v1), bossclaw + landing (deferred initiators), vertical-pack, engine settings panel (P2-5).

### Rollout

Frontend only; backend routes already live (#2871/#2923). Engine legs only trigger for rows that already exist as engine installs (allowlisted dogfood). Concurrent-PR note: developed in parallel with #2932 (engine chat) on disjoint function surfaces of the shared files; whichever merges second absorbs main normally.

Size override rationale: after consolidating duplicate review tests, this coherent lifecycle slice is 3,104 counted lines, 104 lines (3.5%) over the 3,000-line threshold. Splitting it would separate the shared selector/action-eligibility/cache-scope contracts from their manager/detail/publish consumers and regression coverage.

## Test plan

- [x] Task-1 read-only backend semantics verification (report in-worktree)
- [x] TDD review regression run: 5 spec files / 218 tests green (6 targeted failures observed before implementation)
- [x] `bash scripts/verify-web.sh` — full guards + tsc + 523 unit files (7021 passed, 1 skipped, 1 todo) + eslint
- [x] Coverage over thresholds; knip clean; jscpd (`--no-gitignore` real runs) under thresholds
- [ ] CI `code-quality / lint-and-test`
- [ ] Staging: engine uninstall of an `error` row + update of an `active` row (recovery + happy path)


---

## fix(billing): recover Antom paid trial handoff (#2917)

- **SHA**: 2d5e20f5344f46f58319437bd8c94be3cf6751bc
- **作者**: sharplee-srp
- **日期**: 2026-07-20T04:03:44Z
- **PR**: 2917

### 完整 commit message

```
fix(billing): recover Antom paid trial handoff (#2917)

## Summary
- fix only the write path for new Antom trial-to-paid handoffs
- enforce the durable order: validated paid-period evidence → Billing
Gateway grant → active Entitlement → linked PaymentOrder →
active/canceling Agreement
- retry only Entitlements explicitly marked with
`trial_paid_handoff_pending`, reusing the deterministic Entitlement and
skipping a second grant once BG evidence exists
- keep due trial-boundary scheduled downgrades inside the same ordered
handoff; a downgrade scheduled after early payment reprojects the
pending Entitlement before grant
- preserve an already-recorded cancel-at-period-end state and reject
terminal Agreement/provider evidence before grant
- validate Antom ownership by subscription id, with the existing
request-id identity as the fallback

## Scope
This PR handles new webhook handoffs and their bounded idempotent retry
only.

Explicitly out of scope:
- discovering or repairing historical affected users online
- Reconcile reconstruction or expired/current=false scans
- Current Access fallbacks or diagnostics expansion
- cross-subscription replacement/cancellation changes
- synchronous provider queries

Known affected users will be handled by a one-time offline repair. No
production data was modified by this PR.

Issue: [ECA-1244](https://linear.app/srpone/issue/ECA-1244)

## Test plan
- [x] focused handoff/retry/repository suite: 139 passed
- [x] `bash scripts/verify-local.sh --py-static` (ruff, format, pyright,
import-linter)
- [x] regression coverage for early-payment pending handoff, ordered
writes, deterministic retry without regrant, later scheduled downgrade,
request-id fallback, cancel-at-period-end preservation, terminal
evidence rejection, and projection retry

---------

Co-authored-by: kaka-srp <kaka@srp.one>
```

### PR body

## Summary
- fix only the write path for new Antom trial-to-paid handoffs
- enforce the durable order: validated paid-period evidence → Billing Gateway grant → active Entitlement → linked PaymentOrder → active/canceling Agreement
- retry only Entitlements explicitly marked with `trial_paid_handoff_pending`, reusing the deterministic Entitlement and skipping a second grant once BG evidence exists
- keep due trial-boundary scheduled downgrades inside the same ordered handoff; a downgrade scheduled after early payment reprojects the pending Entitlement before grant
- preserve an already-recorded cancel-at-period-end state and reject terminal Agreement/provider evidence before grant
- validate Antom ownership by subscription id, with the existing request-id identity as the fallback

## Scope
This PR handles new webhook handoffs and their bounded idempotent retry only.

Explicitly out of scope:
- discovering or repairing historical affected users online
- Reconcile reconstruction or expired/current=false scans
- Current Access fallbacks or diagnostics expansion
- cross-subscription replacement/cancellation changes
- synchronous provider queries

Known affected users will be handled by a one-time offline repair. No production data was modified by this PR.

Issue: [ECA-1244](https://linear.app/srpone/issue/ECA-1244)

## Test plan
- [x] focused handoff/retry/repository suite: 139 passed
- [x] `bash scripts/verify-local.sh --py-static` (ruff, format, pyright, import-linter)
- [x] regression coverage for early-payment pending handoff, ordered writes, deterministic retry without regrant, later scheduled downgrade, request-id fallback, cancel-at-period-end preservation, terminal evidence rejection, and projection retry


