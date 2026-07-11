---
title: "修复聊天连接状态显示不准确的问题"
type: "Bug Fix"
priority: "中"
date: "2026-07-10"
status: "待审核"
channels: ""
---

## 核心宣传点

修复了聊天连接状态标识有时错误显示“正在初始化”的问题——即使对话其实已经可用；现在会更准确地显示“重新连接中”等真实状态。

## 原始内容

**fix(web): align chat status with usable transport (#2792)**

SHA: `b6a98c196af22aa194e23a8f8ec963525e405c81` | 作者: sharplee-srp | PR #2792

```
fix(web): align chat status with usable transport (#2792)

## Summary
- Treat usable chat/MM transport as authoritative for the connection
pill so init phases do not override a working conversation.
- Use known computer IDs and FastClaw ready status to show
`Reconnecting...` instead of `Initializing...` while OpenClaw provider
hydration is still catching up.
- Keep shared chat gating semantics intact: composer-facing status still
treats init phases as non-connected, while only the pill display layer
suppresses misleading init text.
- Preserve explicit error/retry states when init fails or non-Mattermost
OpenClaw transport errors, even if FastClaw `/status` is still ready.
- Scope the “usable transport beats init lifecycle” override to
Mattermost chat routes; non-chat OpenClaw pages still show FastClaw
pending/restarting lifecycle states.
- Fix the missing initializing i18n key so raw `genClaw.*` keys do not
leak into the UI.

## Root cause
The pill mixed three different signals with the wrong priority: OpenClaw
init status, FastClaw platform readiness, and the interactive chat
transport. `oc.initStatus=loading/starting` could win even when the
backend computer was already ready or Mattermost chat was usable. The
header also did not pass the known current computer id into the pill, so
during page hydration the pill could not poll FastClaw status yet and
fell back to init loading. Separately, the label used
`genClaw.initializing`, but the locale key is
`genClaw.initializingClaw`.

Refs: https://linear.app/srpone/issue/ECA-1195

## Test plan
- [x] `pnpm exec vitest run
tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx
--config ./vitest.config.mts`
- [x] `pnpm exec vitest run
tests/unit/hooks/useStableConnectionStatus.unit.spec.ts --config
./vitest.config.mts`
- [x] `pnpm exec vitest run
tests/unit/components/ClawPageHeader.unit.spec.ts --config
./vitest.config.mts`
- [x] Added deterministic recorder regression coverage for
`oc.initStatus=loading` + OpenClaw WS disconnected +
Mattermost/interactive transport connected + FastClaw ready, asserting
the visible status stays `connected` and no degraded display episode
starts.
- [x] Added regressions for the review P1 cases: shared hook keeps init
phases gated, init errors keep the pill in `error` with retry, and
non-Mattermost OpenClaw WS errors are not masked by FastClaw ready.
- [x] Added regressions for non-Mattermost FastClaw pending/restarting
states and true cold-start `loading` with no computer id.
- [x] Added regression for preserved-bot init errors with FastClaw
`status=stopped`, keeping the pill in `error` with retry instead of
downgrading to plain disconnected.
- [x] Added regression for non-Mattermost pages with connected OpenClaw
transport while the first FastClaw `/status` poll is still pending,
preserving the old healthy first-poll behavior without hiding later
pending/restarting lifecycle states.
- [x] Added regression that shared composer status stays `connected` for
`initStatus=error` when WS/MM are still connected, while the pill
independently keeps showing `error`/retry from raw init state.
- [x] `bash scripts/verify-web.sh
web/app/src/components/ClawConnectionStatus.tsx
web/app/src/hooks/useOpenClawInit.ts
web/app/src/hooks/useStableConnectionStatus.ts
'web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx'
web/app/tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx
web/app/tests/unit/components/ClawPageHeader.unit.spec.ts
web/app/tests/unit/components/ClawPageHeader-extras.unit.spec.tsx
web/app/tests/unit/hooks/useStableConnectionStatus.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`
- [x] Devcontainer staging E2E against bot
`31b7ba01-5b22-4c7c-a3aa-45f0e4def472`: backend ready, agent `main` has
a Mattermost DM channel, page pill displayed `Reconnecting...` with no
raw `genClaw.*` and no initializing/starting/pending text. The run did
not observe a Mattermost websocket hello, so the real staging run
covered the backend-ready/chat-unavailable branch; connected transport
behavior is covered by deterministic unit tests.
```

### PR body

## Summary
- Treat usable chat/MM transport as authoritative for the connection pill so init phases do not override a working conversation.
- Use known computer IDs and FastClaw ready status to show `Reconnecting...` instead of `Initializing...` while OpenClaw provider hydration is still catching up.
- Keep shared chat gating semantics intact: composer-facing status still treats init phases as non-connected, while only the pill display layer suppresses misleading init text.
- Preserve explicit error/retry states when init fails or non-Mattermost OpenClaw transport errors, even if FastClaw `/status` is still ready.
- Scope the “usable transport beats init lifecycle” override to Mattermost chat routes; non-chat OpenClaw pages still show FastClaw pending/restarting lifecycle states.
- Fix the missing initializing i18n key so raw `genClaw.*` keys do not leak into the UI.

## Root cause
The pill mixed three different signals with the wrong priority: OpenClaw init status, FastClaw platform readiness, and the interactive chat transport. `oc.initStatus=loading/starting` could win even when the backend computer was already ready or Mattermost chat was usable. The header also did not pass the known current computer id into the pill, so during page hydration the pill could not poll FastClaw status yet and fell back to init loading. Separately, the label used `genClaw.initializing`, but the locale key is `genClaw.initializingClaw`.

Refs: https://linear.app/srpone/issue/ECA-1195

## Test plan
- [x] `pnpm exec vitest run tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx --config ./vitest.config.mts`
- [x] `pnpm exec vitest run tests/unit/hooks/useStableConnectionStatus.unit.spec.ts --config ./vitest.config.mts`
- [x] `pnpm exec vitest run tests/unit/components/ClawPageHeader.unit.spec.ts --config ./vitest.config.mts`
- [x] Added deterministic recorder regression coverage for `oc.initStatus=loading` + OpenClaw WS disconnected + Mattermost/interactive transport connected + FastClaw ready, asserting the visible status stays `connected` and no degraded display episode starts.
- [x] Added regressions for the review P1 cases: shared hook keeps init phases gated, init errors keep the pill in `error` with retry, and non-Mattermost OpenClaw WS errors are not masked by FastClaw ready.
- [x] Added regressions for non-Mattermost FastClaw pending/restarting states and true cold-start `loading` with no computer id.
- [x] Added regression for preserved-bot init errors with FastClaw `status=stopped`, keeping the pill in `error` with retry instead of downgrading to plain disconnected.
- [x] Added regression for non-Mattermost pages with connected OpenClaw transport while the first FastClaw `/status` poll is still pending, preserving the old healthy first-poll behavior without hiding later pending/restarting lifecycle states.
- [x] Added regression that shared composer status stays `connected` for `initStatus=error` when WS/MM are still connected, while the pill independently keeps showing `error`/retry from raw init state.
- [x] `bash scripts/verify-web.sh web/app/src/components/ClawConnectionStatus.tsx web/app/src/hooks/useOpenClawInit.ts web/app/src/hooks/useStableConnectionStatus.ts 'web/app/src/app/[locale]/(app)/(chat)/chat/GenClawClient.tsx' web/app/tests/unit/components/ClawConnectionStatus-recorder.unit.spec.tsx web/app/tests/unit/components/ClawPageHeader.unit.spec.ts web/app/tests/unit/components/ClawPageHeader-extras.unit.spec.tsx web/app/tests/unit/hooks/useStableConnectionStatus.unit.spec.ts`
- [x] `bash scripts/verify-changed.sh`
- [x] Devcontainer staging E2E against bot `31b7ba01-5b22-4c7c-a3aa-45f0e4def472`: backend ready, agent `main` has a Mattermost DM channel, page pill displayed `Reconnecting...` with no raw `genClaw.*` and no initializing/starting/pending text. The run did not observe a Mattermost websocket hello, so the real staging run covered the backend-ready/chat-unavailable branch; connected transport behavior is covered by deterministic unit tests.

