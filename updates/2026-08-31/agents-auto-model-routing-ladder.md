---
title: "Engine 工作区可以选「Auto」模型了：按任务难度自动在模型梯队里挑"
type: "产品基础功能更新"
priority: "高"
date: "2026-08-31"
status: "待审核"
channels: "站内弹窗+Use Case+Discord+changelog"
---

# Engine 工作区可以选「Auto」模型了：按任务难度自动在模型梯队里挑

## 核心宣传点

Engine 工作区的模型选择器里现在能选「Auto」了。选了之后不再是固定用某一个模型，而是交给引擎按任务难度在一条模型梯队里路由——轻量任务走 gemini-3-flash-preview，中等任务走 claude-haiku-4-5。

梯队会和你套餐里已验证可用的模型取交集：套餐不允许的模型根本不会被写进路由声明里，不是靠一个上限值让路由器自觉遵守，所以不存在被绕过的可能。

选择逻辑也理顺了：只要你手动挑了一个具体模型，就等于明确表示「我不要路由」，系统会关掉 Auto 并清空梯队；反过来开着路由时，界面显示的就是 Auto 本身，而不是底下那个仅在不路由时才生效的兜底模型——以前那样显示会让你看到一个自己从没选过的模型名。Auto 的作用范围在 Engine 工作区是整个会话，在 V1 仍然只作用于子任务，文案也照此改正了（旧文案说的是 V1 的「只路由委派出去的任务」，对 Engine 来说是错的）。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `0a6b5e95bdf3e538f442c08b035cb24ff0c655a0`
- PR: #3568
- 作者: siqiao-srp
- 日期: 2026-08-31T10:26:31Z

### Commit Message

```
feat(agents): offer Auto on engine workspaces and route to a model ladder (#3568)

Depends on zooclaw-engine#846 + #988 being deployed. Without them this
writes a routing block no engine acts on: the turn keeps
`model.primary`, which is the intended degradation, not a break.

## What this does

Makes **Auto** selectable on engine workspaces and translates it into
the engine's `model.routing` contract.

- `engine_model_routing.py` — builds the block: `mode: auto`, the policy
ref, and a tier ladder (`low: gemini-3-flash-preview`, `mid:
claude-haiku-4-5`) **intersected with `resolve_verified_chat_models`**.
Plan enforcement is expressed by *which targets are declared*, not by a
ceiling the router has to honour, so a model the plan forbids is never
declared. The LiteLLM virtual key remains the hard backstop.
- `agent_model_service.py` — the engine read reports the `auto` sentinel
when routing is on (the stored primary is only the unrouted fallback, so
reporting it would show a model the user never chose). Picking a
concrete model writes `mode: off` and clears the targets, because
choosing a model is choosing not to route.
- `auto_model_scope` — new field on the response, `"session"` for engine
and `"subagents"` for V1.

## The frontend change is the copy, not the wiring

The composer already shows Auto as soon as the backend reports
`auto_model_available`. What was wrong is the description: *"Keep this
Agent's conversation on its configured model and route only tasks it
delegates"* is V1's subagent-only behaviour and is simply false for the
engine, which routes the conversation turn itself. One sentence cannot
be true for both runtimes, so the picker now chooses its wording from
`auto_model_scope`. A backend that reports no scope is a V1 backend, so
the default is the V1 wording.

## Contract doc reconciled

`services/claw-interface/AGENTS.md` required V2 to advertise a
fail-closed runtime capability before offering Auto. That was written
when routing was imagined as a plugin the runtime loads and a model
pinned at `sessions_spawn`. V2 routing is engine-native — no plugin to
install, version or negotiate with — so the clause is retired rather
than quietly violated. What replaces it is the part that still matters:
a stale control plane degrades to "Auto is on, every turn uses the
fallback", that degradation is **silent to the user**, and it is
detected from `session_events` `routing_decision` reason codes.

## Verified against a real engine

The write path was previously covered only by mocks, so the routing
block that had been validated was hand-written JSON rather than the
payload this code produces. Driven against a live controld:

- selecting Auto → rendered `mode: auto` with both targets, and a
per-alias route for each (no `MODEL_ROUTE_INVALID`);
- selecting a concrete model → rendered `mode: off`, `targets: {}`, and
the target's route dropped from the render.

Unit tests: 12 in `test_agent_model_service.py`, plus the frontend spec
asserting each runtime's wording.

---------

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

### PR Description

```
Depends on zooclaw-engine#846 + #988 being deployed. Without them this writes a routing block no engine acts on: the turn keeps `model.primary`, which is the intended degradation, not a break.

## What this does

Makes **Auto** selectable on engine workspaces and translates it into the engine's `model.routing` contract.

- `engine_model_routing.py` — builds the block: `mode: auto`, the policy ref, and a tier ladder (`low: gemini-3-flash-preview`, `mid: claude-haiku-4-5`) **intersected with `resolve_verified_chat_models`**. Plan enforcement is expressed by *which targets are declared*, not by a ceiling the router has to honour, so a model the plan forbids is never declared. The LiteLLM virtual key remains the hard backstop.
- `agent_model_service.py` — the engine read reports the `auto` sentinel when routing is on (the stored primary is only the unrouted fallback, so reporting it would show a model the user never chose). Picking a concrete model writes `mode: off` and clears the targets, because choosing a model is choosing not to route.
- `auto_model_scope` — new field on the response, `"session"` for engine and `"subagents"` for V1.

## The frontend change is the copy, not the wiring

The composer already shows Auto as soon as the backend reports `auto_model_available`. What was wrong is the description: *"Keep this Agent's conversation on its configured model and route only tasks it delegates"* is V1's subagent-only behaviour and is simply false for the engine, which routes the conversation turn itself. One sentence cannot be true for both runtimes, so the picker now chooses its wording from `auto_model_scope`. A backend that reports no scope is a V1 backend, so the default is the V1 wording.

## Contract doc reconciled

`services/claw-interface/AGENTS.md` required V2 to advertise a fail-closed runtime capability before offering Auto. That was written when routing was imagined as a plugin the runtime loads and a model pinned at `sessions_spawn`. V2 routing is engine-native — no plugin to install, version or negotiate with — so the clause is retired rather than quietly violated. What replaces it is the part that still matters: a stale control plane degrades to "Auto is on, every turn uses the fallback", that degradation is **silent to the user**, and it is detected from `session_events` `routing_decision` reason codes.

## Verified against a real engine

The write path was previously covered only by mocks, so the routing block that had been validated was hand-written JSON rather than the payload this code produces. Driven against a live controld:

- selecting Auto → rendered `mode: auto` with both targets, and a per-alias route for each (no `MODEL_ROUTE_INVALID`);
- selecting a concrete model → rendered `mode: off`, `targets: {}`, and the target's route dropped from the render.

Unit tests: 12 in `test_agent_model_service.py`, plus the frontend spec asserting each runtime's wording.

```

## 备注

依赖 zooclaw-engine#846 与 #988 上线。若引擎侧未部署，此改动只是写入一个引擎不识别的路由块，本轮对话仍走 model.primary——属于预期内的降级，不是故障。LiteLLM 虚拟密钥仍是最后一道硬性兜底。
