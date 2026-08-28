---
title: "iOS App 全面切换到新版 Agent 运行时（V2），手机上终于能连上你的 Agent 聊天"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-27"
status: "待审核"
channels: ""
---

# iOS App 全面切换到新版 Agent 运行时（V2），手机上终于能连上你的 Agent 聊天

## 核心宣传点

此前 iOS App 完全不认识新版（V2）Agent 运行时：启动时仍去创建一台旧版「电脑」，聊天也只肯连名字叫 main 的旧版 Agent——结果是已经迁移到新版运行时的账号，在手机上既多出一台无用的旧资源，聊天也永远连不上。这次 iOS 端整体切换为 V2 专用：直接读取账号的 Agent 列表并识别主 Agent，雇佣 Agent、查看运行状态、聊天全部走新版接口，不再创建任何旧版资源；同时移除了「重建 Bot」等已失效的旧入口。手机端和网页端的 Agent 能力自此保持一致。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5be94784978d3379b316b6f651309574e42e0d78`
- PR: #3526
- 作者: bill-srp
- 日期: 2026-08-27T03:02:17Z

### Commit Message

```
feat(ios): cut over to v2 engine agent runtime and remove v1 computer code (#3526)

## Linear
<!-- no Linear issue for this task -->

## Summary
- **iOS becomes V2-only.** The ZooClaw app had zero awareness of the
engine (V2) runtime: every agent call was gated on a "primary computer",
boot did `POST /computers`, and Mattermost connect required an agent
literally named `main`. For an AGENTS_V2 user this created a stray V1
computer and never connected chat (`/account/me.mattermost_bots` is
projected from the primary *computer's* workspaces → `[]`; the engine
main agent id is `agt_*`). Design:
`docs/superpowers/specs/2026-08-26-ios-v2-engine-cutover.md`.
- **Removed V1:** `BotService`, `BotViewModel(+Provisioning)`,
`ComputerModels`, `BotInfo/*Response`, `SkillsStatusReport`, untyped
cron parsing, Settings "Redeploy/Recreate Bot", agent identity/avatar
editing (no engine endpoint), `StorageService`, and every `/computers/*`
+ `/openclaw/*` call (grep is empty).
- **Runtime readiness** (`AgentRuntimeViewModel`): `GET
/agents/install-capability` → non-`engine` ⇒ `.notEligible`; else poll
`GET /agents` (2s, ≤300s) until the `is_main` row is `active` with a DM
channel ⇒ `.ready`. Never creates a computer. Retries on foreground
after `.error`; cancellation returns to `.idle`.
- **Identity rule:** every installed-agent key in the app is the
`workspace_id`; main agent = `is_main` (no string compares). Persisted
caches move to `.v2` keys so V1-shaped caches are ignored; a cached bot
list without a main bot is treated as V1 and dropped.
- **Agents:** `GET /agents` (paginated, both runtimes); hire =
duplicate-by-pack guard → `POST /agents {pack_id}` (409
`already_installed`/`operation_in_progress` ⇒ re-list and reuse) → poll
until `active` (terminal on
`install_failed|error|disabled|uninstalling|uninstall_failed|deleting`,
fail-fast if the row disappears) → `POST /agents/{ws}/start` only for
fresh installs; fire = `POST …/uninstall`; update = `POST …/update` +
poll. Failure detail comes from `engine.status_message` (backend
`AgentPublic` has no `error_message`). `hasUpdate` merges official + org
catalogs.
- **Chat:** still Mattermost — the whole `MattermostViewModel` stack is
unchanged; the per-agent channel map is now built from `/agents` rows
(best-effort: an `/agents` failure no longer fails `/account/me` or
ejects the session). Connect gate = any bot with a DM channel, main
preferred.
- **Settings sheet:** model picker only, via `GET /models` + `GET/PUT
/agents/{ws}/model` (disabled when `model_managed`).
- **Conversations:** `/agents/{ws}/conversations`; create uses the
SSE-only `…/conversations/stream` (new `NetworkService.streamLines` with
termination cleanup) — resolves on `conversation_created`, applies
`title_ready` asynchronously.
- **Skills / Schedules:** `GET /agents/{ws}/skills` (scope `global|pack`
= official, `org|personal` = community); read-only schedules fan-out
over `GET /agents/{ws}/schedules` (≤3 concurrent), typed models, error
state surfaced when every fetch fails.
- Out of scope (follow-up PR): V2 chat semantics — `assistant_segment`
terminal marker, `tool_status` activity label, hidden `/stop` control
post, `zooclaw_artifacts` envelope; schedule create/trigger/runs; engine
channels; artifact library.

## Rollout
- Legacy (computer-runtime) accounts see an explicit "not enabled for
the new runtime" state — there is no V1 fallback in this build. Ship to
TestFlight/App Store **before** the production `AGENTS_V2_ENABLED` flip;
staging is open-rollout for smoke.

## Test plan
- [x] `swiftlint --strict` — 0 violations
- [x] `xcodebuild build` (iPhone 17 Pro simulator) — BUILD SUCCEEDED
- [x] Whole `ZooClawTests` + UI bundle — all passing (counts in the PR
checks); coverage restored for install decision (POST → poll → start
ordering, 409 reuse, duplicate reuse, terminal statuses, missing row),
fire/update, runtime readiness negatives, cancellation, cache migration,
`/account/me.mattermost_bots` ignored, connect gate without literal
`main`, SSE parser, model save gating, skills scope filter, schedule
mapping/batching/failure
- [ ] Staging smoke with a fresh account: register → onboarding agent
select → main agent ready → chat round-trip → hire a pack → model picker
→ skills store → schedule tab
- [ ] Staging smoke with an existing V2 account upgrading from the
shipping build (cache migration path)
```

### PR Description

```
## Linear
<!-- no Linear issue for this task -->

## Summary
- **iOS becomes V2-only.** The ZooClaw app had zero awareness of the engine (V2) runtime: every agent call was gated on a "primary computer", boot did `POST /computers`, and Mattermost connect required an agent literally named `main`. For an AGENTS_V2 user this created a stray V1 computer and never connected chat (`/account/me.mattermost_bots` is projected from the primary *computer's* workspaces → `[]`; the engine main agent id is `agt_*`). Design: `docs/superpowers/specs/2026-08-26-ios-v2-engine-cutover.md`.
- **Removed V1:** `BotService`, `BotViewModel(+Provisioning)`, `ComputerModels`, `BotInfo/*Response`, `SkillsStatusReport`, untyped cron parsing, Settings "Redeploy/Recreate Bot", agent identity/avatar editing (no engine endpoint), `StorageService`, and every `/computers/*` + `/openclaw/*` call (grep is empty).
- **Runtime readiness** (`AgentRuntimeViewModel`): `GET /agents/install-capability` → non-`engine` ⇒ `.notEligible`; else poll `GET /agents` (2s, ≤300s) until the `is_main` row is `active` with a DM channel ⇒ `.ready`. Never creates a computer. Retries on foreground after `.error`; cancellation returns to `.idle`.
- **Identity rule:** every installed-agent key in the app is the `workspace_id`; main agent = `is_main` (no string compares). Persisted caches move to `.v2` keys so V1-shaped caches are ignored; a cached bot list without a main bot is treated as V1 and dropped.
- **Agents:** `GET /agents` (paginated, both runtimes); hire = duplicate-by-pack guard → `POST /agents {pack_id}` (409 `already_installed`/`operation_in_progress` ⇒ re-list and reuse) → poll until `active` (terminal on `install_failed|error|disabled|uninstalling|uninstall_failed|deleting`, fail-fast if the row disappears) → `POST /agents/{ws}/start` only for fresh installs; fire = `POST …/uninstall`; update = `POST …/update` + poll. Failure detail comes from `engine.status_message` (backend `AgentPublic` has no `error_message`). `hasUpdate` merges official + org catalogs.
- **Chat:** still Mattermost — the whole `MattermostViewModel` stack is unchanged; the per-agent channel map is now built from `/agents` rows (best-effort: an `/agents` failure no longer fails `/account/me` or ejects the session). Connect gate = any bot with a DM channel, main preferred.
- **Settings sheet:** model picker only, via `GET /models` + `GET/PUT /agents/{ws}/model` (disabled when `model_managed`).
- **Conversations:** `/agents/{ws}/conversations`; create uses the SSE-only `…/conversations/stream` (new `NetworkService.streamLines` with termination cleanup) — resolves on `conversation_created`, applies `title_ready` asynchronously.
- **Skills / Schedules:** `GET /agents/{ws}/skills` (scope `global|pack` = official, `org|personal` = community); read-only schedules fan-out over `GET /agents/{ws}/schedules` (≤3 concurrent), typed models, error state surfaced when every fetch fails.
- Out of scope (follow-up PR): V2 chat semantics — `assistant_segment` terminal marker, `tool_status` activity label, hidden `/stop` control post, `zooclaw_artifacts` envelope; schedule create/trigger/runs; engine channels; artifact library.

## Rollout
- Legacy (computer-runtime) accounts see an explicit "not enabled for the new runtime" state — there is no V1 fallback in this build. Ship to TestFlight/App Store **before** the production `AGENTS_V2_ENABLED` flip; staging is open-rollout for smoke.

## Test plan
- [x] `swiftlint --strict` — 0 violations
- [x] `xcodebuild build` (iPhone 17 Pro simulator) — BUILD SUCCEEDED
- [x] Whole `ZooClawTests` + UI bundle — all passing (counts in the PR checks); coverage restored for install decision (POST → poll → start ordering, 409 reuse, duplicate reuse, terminal statuses, missing row), fire/update, runtime readiness negatives, cancellation, cache migration, `/account/me.mattermost_bots` ignored, connect gate without literal `main`, SSE parser, model save gating, skills scope filter, schedule mapping/batching/failure
- [ ] Staging smoke with a fresh account: register → onboarding agent select → main agent ready → chat round-trip → hire a pack → model picker → skills store → schedule tab
- [ ] Staging smoke with an existing V2 account upgrading from the shipping build (cache migration path)

```

---
