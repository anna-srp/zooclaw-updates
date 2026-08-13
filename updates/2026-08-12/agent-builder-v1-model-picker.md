---
title: "修复：Agent Builder v1 项目里永远选不动的模型下拉"
type: "Bug Fix"
priority: "中"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# 修复：Agent Builder v1 项目里永远选不动的模型下拉

## 核心宣传点

v1 版 Agent Builder 输入框里那个一直显示「Select model」、点了也没反应的模型下拉已隐藏；其他场景若模型来源不可用，也会直接说明原因而不是装作可选。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `8a3b185f6bb574bffc62f3b61358dab89e444677`
- PR: #3340

### Commit Message

```
fix(agent-builder): hide unusable model picker on v1 builder projects (#3340)

## Summary
- Hide the composer model picker on **v1** Agent Builder projects, where
it was permanently stuck on "Select model" and could never resolve a
value.
- Make `ModelPicker` surface the `readOnlyReason` it already computes,
instead of showing a "Select model" prompt that invites a selection
which cannot work.

Reported from the Agent Builder page (`/agent-builder/abp_…`): the
dropdown always read "Select model" even though the model catalog was
healthy.

## Root cause

`AgentBuilderClient` passes `modelController` only for `engine_v2`, and
never passes `modelSettingsWorkspaceId` at all — but
`UnifiedChatComposer` defaults `showModelPicker` to `true`. So on v1 the
picker renders with no model source behind it.

From there the empty label is forced:

1. `useAgentModelQuery(uid, null)` → `enabled: Boolean(uid &&
workspaceId)` is **false**, so the query never runs.
2. It then reports `ready: false` (never succeeded), `loading: false`
(that flag is itself guarded by `workspaceId`), `loadError: null` (never
errored) — a **limbo state**.
3. `useComposerModelState` gates its catalog-default fallback behind
`controller.ready || controller.loadError`, both false, so
`useCatalogDefault` stays `false`.
4. `resolveComposerSelectedModel('', models, false)` returns `''`.
5. `ModelPicker` receives a full option list and `value: ''` → no match
→ `'Select model'`, forever.

Confirmed against the live API: the catalog is fine — it returns 24
models with `claude-sonnet-4-6` correctly flagged `is_default`. Step 3
is why that default is never consulted.

v1 is being deprecated, so this hides the control rather than wiring a
model source into it. Deliberately a one-liner with no v1-specific
abstraction — it gets deleted with v1.

The second change is the part that outlives v1. `UnifiedChatComposer`
already detects exactly this combination and computes an accurate
message:

```ts
(!modelController && !modelSettingsWorkspaceId && !composerModel.canSelectDraftModel
  ? 'Current model is unavailable.'
  : null)
```

…but `readOnlyReason` only drove a tooltip and never reached the trigger
label. Now any surface wired without a model source says why, instead of
failing silently as a dead dropdown. Behaviour is unchanged when
`readOnlyReason` is null (a genuine "nothing picked yet" still reads
"Select model") and when the inventory is empty ("No models available"
still wins).

## Test plan
- [x] `web/packages/chat-ui`: `pnpm test` — 354 passed (3 new: reason
surfaced, null-reason still prompts, empty-inventory label preserved)
- [x] `web/packages/chat-ui`: `pnpm tsc` + `pnpm lint` clean
- [x] `web/app`: `agent-builder-client.unit.spec.tsx` — 62 passed (v1
asserts `showModelPicker: false`; new test asserts `engine_v2` keeps it)
- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (645 files /
8657 tests) + eslint all pass

## Notes for review
- Not fixed here: the underlying limbo in `useAgentModelQuery`, where a
*disabled* query is indistinguishable from "loaded, no model" and
silently suppresses the catalog-default fallback. Any future surface
that forgets to pass a workspace id inherits the same dead dropdown. The
label change makes that self-diagnosing rather than invisible, but the
state modelling is still worth a follow-up.
- If v1 model switching was ever intended as a product behaviour, this
is the wrong fix and we should wire `modelSettingsWorkspaceId` instead.
This was checked before implementing: v1 is being deprecated.

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

### PR Body

## Summary
- Hide the composer model picker on **v1** Agent Builder projects, where it was permanently stuck on "Select model" and could never resolve a value.
- Make `ModelPicker` surface the `readOnlyReason` it already computes, instead of showing a "Select model" prompt that invites a selection which cannot work.

Reported from the Agent Builder page (`/agent-builder/abp_…`): the dropdown always read "Select model" even though the model catalog was healthy.

## Root cause

`AgentBuilderClient` passes `modelController` only for `engine_v2`, and never passes `modelSettingsWorkspaceId` at all — but `UnifiedChatComposer` defaults `showModelPicker` to `true`. So on v1 the picker renders with no model source behind it.

From there the empty label is forced:

1. `useAgentModelQuery(uid, null)` → `enabled: Boolean(uid && workspaceId)` is **false**, so the query never runs.
2. It then reports `ready: false` (never succeeded), `loading: false` (that flag is itself guarded by `workspaceId`), `loadError: null` (never errored) — a **limbo state**.
3. `useComposerModelState` gates its catalog-default fallback behind `controller.ready || controller.loadError`, both false, so `useCatalogDefault` stays `false`.
4. `resolveComposerSelectedModel('', models, false)` returns `''`.
5. `ModelPicker` receives a full option list and `value: ''` → no match → `'Select model'`, forever.

Confirmed against the live API: the catalog is fine — it returns 24 models with `claude-sonnet-4-6` correctly flagged `is_default`. Step 3 is why that default is never consulted.

v1 is being deprecated, so this hides the control rather than wiring a model source into it. Deliberately a one-liner with no v1-specific abstraction — it gets deleted with v1.

The second change is the part that outlives v1. `UnifiedChatComposer` already detects exactly this combination and computes an accurate message:

```ts
(!modelController && !modelSettingsWorkspaceId && !composerModel.canSelectDraftModel
  ? 'Current model is unavailable.'
  : null)
```

…but `readOnlyReason` only drove a tooltip and never reached the trigger label. Now any surface wired without a model source says why, instead of failing silently as a dead dropdown. Behaviour is unchanged when `readOnlyReason` is null (a genuine "nothing picked yet" still reads "Select model") and when the inventory is empty ("No models available" still wins).

## Test plan
- [x] `web/packages/chat-ui`: `pnpm test` — 354 passed (3 new: reason surfaced, null-reason still prompts, empty-inventory label preserved)
- [x] `web/packages/chat-ui`: `pnpm tsc` + `pnpm lint` clean
- [x] `web/app`: `agent-builder-client.unit.spec.tsx` — 62 passed (v1 asserts `showModelPicker: false`; new test asserts `engine_v2` keeps it)
- [x] `bash scripts/verify-web.sh` — guards + tsc + vitest (645 files / 8657 tests) + eslint all pass

## Notes for review
- Not fixed here: the underlying limbo in `useAgentModelQuery`, where a *disabled* query is indistinguishable from "loaded, no model" and silently suppresses the catalog-default fallback. Any future surface that forgets to pass a workspace id inherits the same dead dropdown. The label change makes that self-diagnosing rather than invisible, but the state modelling is still worth a follow-up.
- If v1 model switching was ever intended as a product behaviour, this is the wrong fix and we should wire `modelSettingsWorkspaceId` instead. This was checked before implementing: v1 is being deprecated.


---
