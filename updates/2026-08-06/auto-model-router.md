---
title: "Auto 智能模型路由上线：让系统自动为每次对话挑最合适的模型"
type: "新功能上线"
priority: "高"
date: "2026-08-06"
status: "待审核"
channels: ""
---

## 核心宣传点

模型选择新增「Auto」选项：开启后系统会按每次任务自动路由到最合适的模型，不用再手动纠结选哪个；该开关为账号级全局设置，Agent 内的模型选择器不再显示 Auto，避免选了不生效的困惑。

## 原始内容

**fix(model-router): drive Auto via routingMode (not model.primary=auto) (#3191)**

- sha: `ddd03d2b2243a339333058e6122ff39698932b3e`
- PR: #3191

```
fix(model-router): drive Auto via routingMode (not model.primary=auto) (#3191)

## What

Adds an **"Auto"** chat-model option that engages the
`@zooclaw/model-router` (per-run routing) instead of pinning a fixed
model. This is the **claw-interface** half of the feature; it pairs with
the model-router plugin change in **zooclaw-extras PR #210**.

### Reversed verdict: "Auto" is a routing *flag*, not a model id

The original design stored `model.primary = "auto"` as a sentinel and
expected the router to treat that as standing routing consent. **A live
staging test proved this does NOTHING**: OpenClaw core resolves `"auto"`
to a real fallback model *before* the model-router hook ever sees the
run, so the hook never observes an `"auto"` model.

The plugin (zooclaw-extras #210) now routes on the **bot-wide**
`plugins.entries.model-router.config.routingMode == "auto"` flag
instead. So this PR reworks the backend to drive that flag:

- **Picking "Auto"** sets
`plugins.entries.model-router.config.routingMode = "auto"` (via a
section-level `update_bot_config` merge) and **leaves the configured
model as a real model** — the base/fallback used when routing is off. It
does **not** write `"auto"` into `agents.defaults.model.primary`.
- **Picking a real model** writes it via the existing defaults path
**and** sets `routingMode = "default"`, so switching away from Auto
turns routing off.
- **Reading settings**: when `routingMode == "auto"`, the reported
current/primary model is surfaced as `"auto"` so the picker still shows
"Auto"; otherwise the real model is reported. `"auto"` stays in
`available_models` and keeps its plan-403 bypass.

The model-router is a single **bot-level** plugin, so `routingMode` is
bot-wide (v1: the per-agent path flips the same bot-wide flag — noted
below).

## Backend (`services/claw-interface`)

- **`services/openclaw/bot_config_payload.py`** — new read helpers
`extract_model_router_routing_mode` / `is_routing_mode_auto` and write
helper `build_routing_mode_patch`. These centralize the config-shape
knowledge (`config.plugins.entries.model-router.config.routingMode`,
handling nested-vs-flat payloads and non-string values). Also gains
`resolve_agent_ids` (moved here — see note).
- **`services/openclaw/model_routing.py`** (new) — owns the write
translation so route/service bodies stay thin:
- `apply_primary_model_selection` — the `PUT /model` write: `"auto"` →
`routingMode="auto"` only (model.primary untouched); a real model →
defaults write + `routingMode="default"`.
- `resolve_agent_model_write` / `write_agent_routing_mode` — the
agent-settings equivalents.
- **`routes/openclaw_settings/core.py`** — `update_model` delegates to
`apply_primary_model_selection` (keeps the plan-403 bypass for
`"auto"`); `get_settings` overrides the reported `primary_model` to
`"auto"` when `routingMode` is auto.
- **`services/openclaw/agent_settings_service.py`** —
`update_agent_settings` translates a `model == "auto"` patch into the
bot-wide `routingMode="auto"` flip **without pinning `"auto"` as the
agent model** (the configured model stays as the fallback); a real model
sets the model **and** `routingMode="default"`. Read paths report
`"auto"` for every agent when `routingMode` is auto.
- **`services/agents/agent_model_service.py` /
`services/model_catalog.py`** — behavior unchanged: the engine runtime
still rejects `"auto"` with an accurate `agent.model_unavailable` domain
error (no per-run routing hook there); the `/models` catalog keeps its
`"Auto"` entry.

> **File-length note:** the routingMode threading pushed `core.py` and
`agent_settings_service.py` over the 500-line CI guard, so two pure
helpers were moved to their natural homes — `resolve_agent_ids` →
`bot_config_payload.py`, `get_agent_available_channels` →
`agent_settings_channels.py`. No behavior change.

## Frontend (`web/app`)

**No frontend change needed.** The API wire contract is unchanged from
the frontend's perspective: it still sends `openai/auto` and still
receives `"auto"` / `"openai/auto"` back, both of which normalize to
"Auto". Verified end-to-end — `AgentModelSection` canonicalizes the
picker value and dirty-check, `backend-model-label` maps both forms to
"Auto", and the composer's `normalizeAgentModelId` round-trips `auto ↔
openai/auto`. The backend just does something different internally
(routingMode flag instead of a stored model id).

## Tests

Backend (all pass):
- `update_model` with `"auto"` / `"openai/auto"` writes
`routingMode="auto"` and does **not** call `update_bot_config_defaults`
(model.primary is NOT set to "auto"); a real model writes the model
**and** `routingMode="default"`.
- `get_settings` reports `primary_model == "auto"` when `routingMode` is
auto, and the real model otherwise.
- per-agent `update_agent_settings` flips the bot-wide `routingMode` and
leaves the agent model unpinned for `"auto"`; reports `"auto"` for the
agent; real models clear routing to `"default"`.
- new focused unit tests for the read/write payload helpers
(`test_bot_config_payload_routing_mode.py`).
- `agent_model_service` / `model_catalog` tests updated only for the
routingMode translation contract.

## Verification

- `bash scripts/verify-py.sh` — ruff + ruff-format + import-linter
clean; all changed source files are **pyright-clean** (0 errors). The
residual pyright failures are pre-existing local-env `favie_common` /
`pytest_bdd` / stripe-SDK / FastAPI-stub import-resolution errors in
files this PR does not touch; CI has the correct env.
- `bash scripts/verify-web.sh` — tsc + eslint clean. The 2 vitest
failures (`AssetLibraryContent`, `LegacyWorkspaceBrowser`) are
pre-existing main-line issues unrelated to this PR (backend-only
change).
- CI file-length guard passes (touched files back under 500 lines).

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

**PR Body:**

## What

Adds an **"Auto"** chat-model option that engages the `@zooclaw/model-router` (per-run routing) instead of pinning a fixed model. This is the **claw-interface** half of the feature; it pairs with the model-router plugin change in **zooclaw-extras PR #210**.

### Reversed verdict: "Auto" is a routing *flag*, not a model id

The original design stored `model.primary = "auto"` as a sentinel and expected the router to treat that as standing routing consent. **A live staging test proved this does NOTHING**: OpenClaw core resolves `"auto"` to a real fallback model *before* the model-router hook ever sees the run, so the hook never observes an `"auto"` model.

The plugin (zooclaw-extras #210) now routes on the **bot-wide** `plugins.entries.model-router.config.routingMode == "auto"` flag instead. So this PR reworks the backend to drive that flag:

- **Picking "Auto"** sets `plugins.entries.model-router.config.routingMode = "auto"` (via a section-level `update_bot_config` merge) and **leaves the configured model as a real model** — the base/fallback used when routing is off. It does **not** write `"auto"` into `agents.defaults.model.primary`.
- **Picking a real model** writes it via the existing defaults path **and** sets `routingMode = "default"`, so switching away from Auto turns routing off.
- **Reading settings**: when `routingMode == "auto"`, the reported current/primary model is surfaced as `"auto"` so the picker still shows "Auto"; otherwise the real model is reported. `"auto"` stays in `available_models` and keeps its plan-403 bypass.

The model-router is a single **bot-level** plugin, so `routingMode` is bot-wide (v1: the per-agent path flips the same bot-wide flag — noted below).

## Backend (`services/claw-interface`)

- **`services/openclaw/bot_config_payload.py`** — new read helpers `extract_model_router_routing_mode` / `is_routing_mode_auto` and write helper `build_routing_mode_patch`. These centralize the config-shape knowledge (`config.plugins.entries.model-router.config.routingMode`, handling nested-vs-flat payloads and non-string values). Also gains `resolve_agent_ids` (moved here — see note).
- **`services/openclaw/model_routing.py`** (new) — owns the write translation so route/service bodies stay thin:
  - `apply_primary_model_selection` — the `PUT /model` write: `"auto"` → `routingMode="auto"` only (model.primary untouched); a real model → defaults write + `routingMode="default"`.
  - `resolve_agent_model_write` / `write_agent_routing_mode` — the agent-settings equivalents.
- **`routes/openclaw_settings/core.py`** — `update_model` delegates to `apply_primary_model_selection` (keeps the plan-403 bypass for `"auto"`); `get_settings` overrides the reported `primary_model` to `"auto"` when `routingMode` is auto.
- **`services/openclaw/agent_settings_service.py`** — `update_agent_settings` translates a `model == "auto"` patch into the bot-wide `routingMode="auto"` flip **without pinning `"auto"` as the agent model** (the configured model stays as the fallback); a real model sets the model **and** `routingMode="default"`. Read paths report `"auto"` for every agent when `routingMode` is auto.
- **`services/agents/agent_model_service.py` / `services/model_catalog.py`** — behavior unchanged: the engine runtime still rejects `"auto"` with an accurate `agent.model_unavailable` domain error (no per-run routing hook there); the `/models` catalog keeps its `"Auto"` entry.

> **File-length note:** the routingMode threading pushed `core.py` and `agent_settings_service.py` over the 500-line CI guard, so two pure helpers were moved to their natural homes — `resolve_agent_ids` → `bot_config_payload.py`, `get_agent_available_channels` → `agent_settings_channels.py`. No behavior change.

## Frontend (`web/app`)

**No frontend change needed.** The API wire contract is unchanged from the frontend's perspective: it still sends `openai/auto` and still receives `"auto"` / `"openai/auto"` back, both of which normalize to "Auto". Verified end-to-end — `AgentModelSection` canonicalizes the picker value and dirty-check, `backend-model-label` maps both forms to "Auto", and the composer's `normalizeAgentModelId` round-trips `auto ↔ openai/auto`. The backend just does something different internally (routingMode flag instead of a stored model id).

## Tests

Backend (all pass):
- `update_model` with `"auto"` / `"openai/auto"` writes `routingMode="auto"` and does **not** call `update_bot_config_defaults` (model.primary is NOT set to "auto"); a real model writes the model **and** `routingMode="default"`.
- `get_settings` reports `primary_model == "auto"` when `routingMode` is auto, and the real model otherwise.
- per-agent `update_agent_settings` flips the bot-wide `routingMode` and leaves the agent model unpinned for `"auto"`; reports `"auto"` for the agent; real models clear routing to `"default"`.
- new focused unit tests for the read/write payload helpers (`test_bot_config_payload_routing_mode.py`).
- `agent_model_service` / `model_catalog` tests updated only for the routingMode translation contract.

## Verification

- `bash scripts/verify-py.sh` — ruff + ruff-format + import-linter clean; all changed source files are **pyright-clean** (0 errors). The residual pyright failures are pre-existing local-env `favie_common` / `pytest_bdd` / stripe-SDK / FastAPI-stub import-resolution errors in files this PR does not touch; CI has the correct env.
- `bash scripts/verify-web.sh` — tsc + eslint clean. The 2 vitest failures (`AssetLibraryContent`, `LegacyWorkspaceBrowser`) are pre-existing main-line issues unrelated to this PR (backend-only change).
- CI file-length guard passes (touched files back under 500 lines).


---

**feat(web): bot-level Auto model control + hide Auto from agent-scoped pickers (#3258)**

- sha: `c772f87ae87df61a86579181dc36f431207222d7`
- PR: #3258

```
feat(web): bot-level Auto model control + hide Auto from agent-scoped pickers (#3258)

## What

Hide the **"Auto"** router option from the agent-scoped unified chat
composer on **every** runtime.

Addresses the P1a review finding on the Auto model-router work (backend
counterpart in #3191): *"Auto is still selectable from the
computer-agent composer, but its save path is now intentionally a
no-op."*

## Why

"Auto" is a **bot-wide routing toggle** owned by the global model
setting, not an agent-scoped choice:

- On the **engine** runtime, the per-agent model save path rejects
`auto` (`agent.model_unavailable`).
- On the **computer** runtime, a per-agent `auto` write is intentionally
a **no-op** (turning Auto on is a global-settings action only).

So selecting "Auto" in the composer never does what the user expects.
Previously the composer only dropped the sentinel on the **engine**
runtime, so it was still offered — and silently a no-op — on computer
workspaces.

## Change

- Replace `filterModelsForRuntime(models, runtime)` with
`filterComposerModels(models)`, which drops the `openai/auto` sentinel
from the composer picker on **every** runtime (both the bare and
provider-qualified forms).
- The **global settings** model picker is a separate surface and still
offers "Auto" — `buildModelPickerOptions` is unchanged.

## Tests

- `composer-model-presentations.unit.spec.ts`: `filterComposerModels`
drops `auto` (bare + `openai/auto`) and leaves a plain catalog
untouched.
- `UnifiedChatComposer.unit.spec.tsx`: composer hides `auto` on **both**
computer and engine workspaces.
- Local: `tsc --noEmit` clean, `eslint` clean, composer vitest suite 112
passed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 4.8 (1M context) <noreply@anthropic.com>
```

**PR Body:**

## What

Hide the **"Auto"** router option from the agent-scoped unified chat composer on **every** runtime.

Addresses the P1a review finding on the Auto model-router work (backend counterpart in #3191): *"Auto is still selectable from the computer-agent composer, but its save path is now intentionally a no-op."*

## Why

"Auto" is a **bot-wide routing toggle** owned by the global model setting, not an agent-scoped choice:

- On the **engine** runtime, the per-agent model save path rejects `auto` (`agent.model_unavailable`).
- On the **computer** runtime, a per-agent `auto` write is intentionally a **no-op** (turning Auto on is a global-settings action only).

So selecting "Auto" in the composer never does what the user expects. Previously the composer only dropped the sentinel on the **engine** runtime, so it was still offered — and silently a no-op — on computer workspaces.

## Change

- Replace `filterModelsForRuntime(models, runtime)` with `filterComposerModels(models)`, which drops the `openai/auto` sentinel from the composer picker on **every** runtime (both the bare and provider-qualified forms).
- The **global settings** model picker is a separate surface and still offers "Auto" — `buildModelPickerOptions` is unchanged.

## Tests

- `composer-model-presentations.unit.spec.ts`: `filterComposerModels` drops `auto` (bare + `openai/auto`) and leaves a plain catalog untouched.
- `UnifiedChatComposer.unit.spec.tsx`: composer hides `auto` on **both** computer and engine workspaces.
- Local: `tsc --noEmit` clean, `eslint` clean, composer vitest suite 112 passed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

