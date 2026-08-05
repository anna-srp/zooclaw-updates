---
title: "安装自定义专家不再误报「Bot 必须在运行中」"
type: "Bug Fix"
priority: "中"
date: "2026-08-04"
status: "待审核"
channels: ""
commit: "6f18d4fd45f449c65ab229544065a00016654bf7"
repo: "SerendipityOneInc/ecap-workspace"
---

## 核心宣传点

在 My Custom Specialists 安装上传的 Pack 时，不再要求 Bot 必须在线：走引擎运行时的安装（以及没有 Bot 的用户）现在可以直接安装成功，只有真正的旧版计算机运行时安装才需要 Bot，且由服务端准确判断。

## 原始内容

```
fix(agents): resolve install computer in BFF instead of per-click bot probe (#3233)

# 🔧 Fix

## Summary

Installing an uploaded pack on **My Custom Specialists** demanded a
running bot even when the install would route to the engine runtime and
never touch the bot. The page's per-click gate (`useEnsureBotReady`) ran
a 3-request probe (`/computers`, `/computers/{id}`,
`/computers/{id}/status`) before every install/uninstall and threw "Bot
must be running before install or uninstall" unless the bot was fully
ready — a leftover from the pre-engine (v1 computer runtime) world.

This PR removes the client-side computer detection entirely and moves
computer resolution into the install BFF:

- **BFF** (`/api/agents/install`): when the request routes to the
computer runtime without a `computer_id`, the route now resolves the
user's computer server-side (one `GET /computers`, excluding
`pack_test`, requiring `status === 'ready'`). No ready computer → `409
agent.computer_not_ready` (fail-fast preserved). Engine-eligible
installs never touch the computer path at all. `agent_id` missing
remains a 400.
- **Frontend**: `useEnsureBotReady.ts` deleted. Install sends
`computerId: null` and lets the BFF decide; computer-runtime polling
uses the `computer_id` returned on the created workspace.
Computer-runtime uninstall/update take the `computer_id` already present
on the installed agent row (threaded through `PublishAgentCardItem` and
the toggle/update targets) with a missing-id guard.
- **UX**: the existing `botNotReady` toast is preserved by mapping the
BFF's `agent.computer_not_ready` ApiError code in `PublishAgentsClient`.

Net effect: engine-eligible users (and users with no bot) can install
custom specialists without a running bot; only genuine legacy
computer-runtime installs still require one, enforced server-side with a
single call. The marketplace hire flow (`useAgentActions`, untouched)
automatically gains the same server-side fallback when it has no cached
computer id.

## Root cause

`useAgentInstallToggle` called `ensureBotReady()` unconditionally before
`installAgentViaBff`, but the BFF's routing decision
(`install-decision.ts`) only needs a computer for the legacy
computer-runtime path — engine installs go to `POST /agents` with just
`pack_id`. The marketplace hire flow already treated the computer id as
optional for pack installs; the specialists page never got the same
update.

## Changes

- `web/app/src/app/api/agents/_lib/install-decision.ts` — new
`computer-resolve` route kind when `agent_id` is present but
`computer_id` is missing
- `web/app/src/app/api/agents/install/route.ts` — server-side
ready-computer resolution + `409 agent.computer_not_ready`
-
`web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useAgentInstallToggle.ts`
— bot probe removed; BFF-resolved install; uninstall uses target
`computerId`
-
`web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useAgentUpdateAction.ts`
— bot probe removed; update uses target `computerId`
-
`web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useEnsureBotReady.ts`
— deleted
-
`web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/PublishAgentsClient.tsx`
+ `components/types.ts` — thread `computerId` from installed rows; map
`agent.computer_not_ready` to the bot-not-ready toast
- Unit tests updated across the BFF decision/route and publish
hooks/page specs

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (593 files,
8073 passed) + eslint, all green
- [x] BFF specs: resolves `/computers` when `computer_id` omitted; `409
agent.computer_not_ready` when no ready computer; engine path unchanged
- [x] Hook specs: install without bot probe; computer-runtime
uninstall/update use row `computerId`; missing-id guards surface the
existing failure toasts
- [ ] Staging smoke after deploy: install an uploaded pack as an
engine-eligible user with no running bot

---

### PR Body

# 🔧 Fix

## Summary

Installing an uploaded pack on **My Custom Specialists** demanded a running bot even when the install would route to the engine runtime and never touch the bot. The page's per-click gate (`useEnsureBotReady`) ran a 3-request probe (`/computers`, `/computers/{id}`, `/computers/{id}/status`) before every install/uninstall and threw "Bot must be running before install or uninstall" unless the bot was fully ready — a leftover from the pre-engine (v1 computer runtime) world.

This PR removes the client-side computer detection entirely and moves computer resolution into the install BFF:

- **BFF** (`/api/agents/install`): when the request routes to the computer runtime without a `computer_id`, the route now resolves the user's computer server-side (one `GET /computers`, excluding `pack_test`, requiring `status === 'ready'`). No ready computer → `409 agent.computer_not_ready` (fail-fast preserved). Engine-eligible installs never touch the computer path at all. `agent_id` missing remains a 400.
- **Frontend**: `useEnsureBotReady.ts` deleted. Install sends `computerId: null` and lets the BFF decide; computer-runtime polling uses the `computer_id` returned on the created workspace. Computer-runtime uninstall/update take the `computer_id` already present on the installed agent row (threaded through `PublishAgentCardItem` and the toggle/update targets) with a missing-id guard.
- **UX**: the existing `botNotReady` toast is preserved by mapping the BFF's `agent.computer_not_ready` ApiError code in `PublishAgentsClient`.

Net effect: engine-eligible users (and users with no bot) can install custom specialists without a running bot; only genuine legacy computer-runtime installs still require one, enforced server-side with a single call. The marketplace hire flow (`useAgentActions`, untouched) automatically gains the same server-side fallback when it has no cached computer id.

## Root cause

`useAgentInstallToggle` called `ensureBotReady()` unconditionally before `installAgentViaBff`, but the BFF's routing decision (`install-decision.ts`) only needs a computer for the legacy computer-runtime path — engine installs go to `POST /agents` with just `pack_id`. The marketplace hire flow already treated the computer id as optional for pack installs; the specialists page never got the same update.

## Changes

- `web/app/src/app/api/agents/_lib/install-decision.ts` — new `computer-resolve` route kind when `agent_id` is present but `computer_id` is missing
- `web/app/src/app/api/agents/install/route.ts` — server-side ready-computer resolution + `409 agent.computer_not_ready`
- `web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useAgentInstallToggle.ts` — bot probe removed; BFF-resolved install; uninstall uses target `computerId`
- `web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useAgentUpdateAction.ts` — bot probe removed; update uses target `computerId`
- `web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/hooks/useEnsureBotReady.ts` — deleted
- `web/app/src/app/[locale]/(app)/(chat)/agents-manager/publish/PublishAgentsClient.tsx` + `components/types.ts` — thread `computerId` from installed rows; map `agent.computer_not_ready` to the bot-not-ready toast
- Unit tests updated across the BFF decision/route and publish hooks/page specs

## Test plan

- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (593 files, 8073 passed) + eslint, all green
- [x] BFF specs: resolves `/computers` when `computer_id` omitted; `409 agent.computer_not_ready` when no ready computer; engine path unchanged
- [x] Hook specs: install without bot probe; computer-runtime uninstall/update use row `computerId`; missing-id guards surface the existing failure toasts
- [ ] Staging smoke after deploy: install an uploaded pack as an engine-eligible user with no running bot

```
