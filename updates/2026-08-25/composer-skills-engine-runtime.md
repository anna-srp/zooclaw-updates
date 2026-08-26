---
title: "修复：升级到新版 Agent 后，聊天输入框里的 Skills 菜单一直报「无法加载 Skills」"
type: "Bug Fix"
priority: "高"
date: "2026-08-25"
status: "待审核"
channels: ""
---

# 修复：升级到新版 Agent 后，聊天输入框里的 Skills 菜单一直报「无法加载 Skills」

## 核心宣传点

已经迁移到新版 Engine Agent 的用户，在聊天框和新会话里点开 Skills 菜单时会一直卡在「Could not load Skills」，等于完全没法在对话里挑技能用——因为菜单还在按老版本的方式去找一个早就不存在的运行时。现在 Skills 列表会按你这个 Agent 实际的运行版本去取：新版 Agent 读它自己工作空间里生效的技能清单，老版 Agent 保持原样，两边的安装/卸载操作仍然会即时刷新菜单。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `a0015785f1aaf7acb766c03829a9e4c1e9513a17`
- PR: #3504
- 作者: sharplee-srp
- 日期: 2026-08-25T03:05:43Z

### Commit Message

```
feat(web): route composer skills by agent runtime for engine workspaces (#3504)

## Linear

[ECA-1394](https://linear.app/srpone/issue/ECA-1394/) — Skill Store:
composer 'Could not load Skills' when bot not ready + no search in
composer Skill Store dialog

## Summary

**Problem.** The Composer Skills menu always called the uid-scoped V1
`/openclaw/runtime-skills` endpoint. For users migrated to a V2 Engine
Agent there is no V1 bot behind that uid, so the Session and New-Chat
composers rendered "Could not load Skills".

**Fix.** Route the Composer's Skills read by the Agent's runtime.

- **`ComposerSkillContext { runtime, workspaceId }`**
(`src/models/skill.ts`) is resolved from the already-known Agent
identity by `resolveComposerSkillContext()` and threaded
`SessionThreadClient` / `ChatBody` / `NewChatClient` → `GenClawInput` /
`OpenClawChatSurface` → `UnifiedChatComposer` → `ComposerAddMenu` →
`ComposerSkillsMenu`. It is kept parallel to — never merged with — the
existing `modelSettings*` props: Model and Skills are independent
capability contracts. Runtime is never guessed from an allowlist or a
catalog card; anything that is not `engine` + a real `workspace_id` (no
Agent, draft Agent, Engine Agent not yet installed into a workspace)
falls back to V1.
- **`useComposerSkills`** is runtime-neutral: one `useQuery` over a
precomputed descriptor, so the two runtimes never conditionally call two
different hooks.
- **computer branch** reuses the newly factored
`runtimeSkillsQueryOptions(uid)` verbatim, so the Composer keeps sharing
the `skillsKeys.runtime(uid)` cache bucket with the Skill Store —
install/uninstall invalidation of that key still updates the Composer
list.
- **engine branch** adds `skillsKeys.engineWorkspace(uid, workspaceId)`
over `GET /agents/{workspaceId}/skills` through the generic
claw-interface proxy (ownership, the `runtime === 'engine'` check, and
the workspace → Engine `agt_*` id mapping are all enforced downstream;
the browser never sees a bare Engine id). Deliberately **not** added to
`PERSIST_ALLOWLIST_PREFIXES`: effective Skills follow the Agent's
rendered config version, so a sessionStorage snapshot could outlive what
it describes.
- **Adapters** normalize V1 `RuntimeSkill` and V2 `EngineWorkspaceSkill`
into a shared `ComposerSkill` display model. The `disabled !== true &&
eligible !== false` filter stays V1-only — the V2 response is already an
effective set; V2 only dedupes by `name` (defensive, because the shared
`SkillsSubMenuItem` keys rows by name).
- **No cross-runtime fallback.** A failed Engine query shows the error
state; it never retries against `/openclaw/runtime-skills` and never
wakes a stopped V1 bot.
- Selection behavior is unchanged (still inserts `Use <name> to…`);
`onSelectSkill` is retyped from `RuntimeSkill` to `ComposerSkill`.
**`@zooclaw/chat-ui` is untouched** — the shared package never learns
about runtimes or APIs.

**Dependency / rollout.** Requires the backend PR
*"feat(claw-interface): add workspace-owned engine agent skills
listing"* — #3505. **That endpoint must deploy before this frontend
change**; until then Engine sessions keep the same failure they have
today, and the V1 path is unaffected either way.

## Test plan

- [x] `bash scripts/verify-web.sh <30 changed paths>` — guards + `tsc
--noEmit` + targeted `vitest` (36 files / 750 tests) + `eslint`, all
green
- [x] `pnpm lint:deadcode`, `pnpm lint:imports`, `pnpm dup` — clean
- [x] `TZ=UTC pnpm test:unit:coverage` — 9182 pass (8 pre-existing
timezone-dependent failures without `TZ=UTC` in
`agent-builder-home-model` / `agent-builder-production-home` /
`UserMenu` / `billing/SubscriptionPanel`; untouched by this PR)
- [x] New unit specs: `composer-skills` adapters + context resolution,
`useComposerSkills` runtime split (key/queryFn/adapter per branch, no
fallback), `useEngineWorkspaceSkills`, plus persist-allowlist assertions
that the engine family is never dehydrated
- [x] Updated specs assert the context is threaded through every
intermediate component and that V2 skips the V1 eligibility filter
- [ ] Post-deploy manual check on a migrated V2 Agent (blocked on the
backend endpoint shipping)
```

### PR Description

```
## Linear

[ECA-1394](https://linear.app/srpone/issue/ECA-1394/) — Skill Store: composer 'Could not load Skills' when bot not ready + no search in composer Skill Store dialog

## Summary

**Problem.** The Composer Skills menu always called the uid-scoped V1 `/openclaw/runtime-skills` endpoint. For users migrated to a V2 Engine Agent there is no V1 bot behind that uid, so the Session and New-Chat composers rendered "Could not load Skills".

**Fix.** Route the Composer's Skills read by the Agent's runtime.

- **`ComposerSkillContext { runtime, workspaceId }`** (`src/models/skill.ts`) is resolved from the already-known Agent identity by `resolveComposerSkillContext()` and threaded `SessionThreadClient` / `ChatBody` / `NewChatClient` → `GenClawInput` / `OpenClawChatSurface` → `UnifiedChatComposer` → `ComposerAddMenu` → `ComposerSkillsMenu`. It is kept parallel to — never merged with — the existing `modelSettings*` props: Model and Skills are independent capability contracts. Runtime is never guessed from an allowlist or a catalog card; anything that is not `engine` + a real `workspace_id` (no Agent, draft Agent, Engine Agent not yet installed into a workspace) falls back to V1.
- **`useComposerSkills`** is runtime-neutral: one `useQuery` over a precomputed descriptor, so the two runtimes never conditionally call two different hooks.
  - **computer branch** reuses the newly factored `runtimeSkillsQueryOptions(uid)` verbatim, so the Composer keeps sharing the `skillsKeys.runtime(uid)` cache bucket with the Skill Store — install/uninstall invalidation of that key still updates the Composer list.
  - **engine branch** adds `skillsKeys.engineWorkspace(uid, workspaceId)` over `GET /agents/{workspaceId}/skills` through the generic claw-interface proxy (ownership, the `runtime === 'engine'` check, and the workspace → Engine `agt_*` id mapping are all enforced downstream; the browser never sees a bare Engine id). Deliberately **not** added to `PERSIST_ALLOWLIST_PREFIXES`: effective Skills follow the Agent's rendered config version, so a sessionStorage snapshot could outlive what it describes.
- **Adapters** normalize V1 `RuntimeSkill` and V2 `EngineWorkspaceSkill` into a shared `ComposerSkill` display model. The `disabled !== true && eligible !== false` filter stays V1-only — the V2 response is already an effective set; V2 only dedupes by `name` (defensive, because the shared `SkillsSubMenuItem` keys rows by name).
- **No cross-runtime fallback.** A failed Engine query shows the error state; it never retries against `/openclaw/runtime-skills` and never wakes a stopped V1 bot.
- Selection behavior is unchanged (still inserts `Use <name> to…`); `onSelectSkill` is retyped from `RuntimeSkill` to `ComposerSkill`. **`@zooclaw/chat-ui` is untouched** — the shared package never learns about runtimes or APIs.

**Dependency / rollout.** Requires the backend PR *"feat(claw-interface): add workspace-owned engine agent skills listing"* — #3505. **That endpoint must deploy before this frontend change**; until then Engine sessions keep the same failure they have today, and the V1 path is unaffected either way.

## Test plan

- [x] `bash scripts/verify-web.sh <30 changed paths>` — guards + `tsc --noEmit` + targeted `vitest` (36 files / 750 tests) + `eslint`, all green
- [x] `pnpm lint:deadcode`, `pnpm lint:imports`, `pnpm dup` — clean
- [x] `TZ=UTC pnpm test:unit:coverage` — 9182 pass (8 pre-existing timezone-dependent failures without `TZ=UTC` in `agent-builder-home-model` / `agent-builder-production-home` / `UserMenu` / `billing/SubscriptionPanel`; untouched by this PR)
- [x] New unit specs: `composer-skills` adapters + context resolution, `useComposerSkills` runtime split (key/queryFn/adapter per branch, no fallback), `useEngineWorkspaceSkills`, plus persist-allowlist assertions that the engine family is never dehydrated
- [x] Updated specs assert the context is threaded through every intermediate component and that V2 skips the V1 eligibility filter
- [ ] Post-deploy manual check on a migrated V2 Agent (blocked on the backend endpoint shipping)



```
