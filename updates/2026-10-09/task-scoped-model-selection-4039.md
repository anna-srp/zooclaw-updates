---
title: "任务内可单独换模型：只影响当前这条任务，不改 Agent 默认设置"
type: "新功能"
priority: "高"
date: "2026-10-09"
status: "待审核"
channels: ""
---

# 任务内可单独换模型：只影响当前这条任务，不改 Agent 默认设置

## 核心宣传点

现在可以在 Web 端的某条任务里直接为后续对话切换平台模型，而不用去改 Agent 本身。编辑 Agent 时保存的仍然是 Agent 默认模型（走 Revision），任务内的选择则记在该任务对应的 Engine 会话上，刷新页面依然生效，也不会影响同一个 Agent 的其他任务或 Agent 定义本身。如果你显式选中当前这个默认模型，等于把它钉在这条任务上，菜单里不再额外提供「恢复默认」项。权限方面，任务访问与模型权益都会在后端校验后再把选择同步给 Engine。首次发送时会先建会话、保存选择再发消息，失败重试沿用同一会话与幂等键。继承自 Agent 的 Auto 模式保持只读展示。

## 分级

- 内部：P1
- 外部：A
- toB 相关：否
- 发布状态：已合并待发版

## 备注

本次不含 iOS 端改动，也未开放任务级 Auto 与个人订阅相关能力。

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `542b009578d5a95cb4466111b37263250e84ae42`
- PR: #4039
- 作者：kaka-srp
- 日期：2026-10-09T09:42:47Z

### Commit Message

```
feat(agents): allow task-scoped platform model selection (#4039)

## Summary

Allow users to choose a platform model for the current Web Task's
subsequent turns while Edit continues to save the Agent default through
a Revision. Task selection is persisted on the canonical Engine Session,
survives refresh, and does not change another Task or the Agent
definition. Choosing the currently checked default explicitly pins that
model for the Task; there is no new reset/default menu item.

Authorize Task access and model entitlement in claw-interface, then
forward Engine's selection/config CAS. Wire existing Task and new-chat
composers to the Task controller. On first send, create the Session,
save the choice, bind the conversation, and only then send; failures
retain the same Session/idempotency key for retry.

Preserve the latest main's model retirement/missing-model sending gates
and read-only inherited Agent Auto, without adding Task Auto or personal
subscription functionality. No iOS change.

## Review and CI follow-up

The first CI Web test run found three older test files still asserting
Revision writes or missing the Task hook seam. Updated those contracts
and verified 114 focused Web tests, including the real composer
selecting a Task draft and passing it on first send without any
Revision/default write. Scoped the launcher Task controller to Engine
Agents and omitted an absent model draft from creation parameters.
Corrected the design error table to the existing public `400
agent.model_unavailable` and `409 agent_session.task_model_changed`; 18
backend Task model tests include actual FastAPI/shared-handler HTTP
assertions for missing, withdrawn, and ambiguous catalog models. Both
review agents completed a targeted re-review with no new actionable
findings.

## Dependencies and rollout

Depends on [zooclaw-engine
#1921](https://github.com/SerendipityOneInc/zooclaw-engine/pull/1921).
Deploy its controld and all relevant workers first, then deploy this
backend and Web together. No new migration or Vault setting is needed.
Do not roll the workers back while stored Task selections still require
the new runtime behavior.

## Test plan

- [x] Web Task hook, first-send orchestration, Revision/composer
regression suites: 95 tests passed.
- [x] Backend Task/default-model/retirement metadata suites: 102 tests
passed.
- [x] Web CI guards, tsc, ESLint and import boundaries passed; Python
ruff/format, pyright and import-linter passed.
- [x] Real local Next.js/FastAPI against staging CSFLE plus shared
zooclaw-dev ACS/Engine and real LiteLLM: existing Task switch/refresh;
selected model on first send; checked-default pinning after Edit changes
the default; unaffected Task follows the new default; an in-progress
reply stays on its original model and the next turn changes; first-save
failure sends nothing and retry reuses the Session without duplicate
chat messages; 403/409 leave selection unchanged. Actual Engine records
verified Anthropic/Responses model execution and visible replies.
- [x] Two review agents completed review and targeted re-review.
Confirmed dependency-boundary and retirement integration findings were
fixed. Removing Task model guards makes the retirement/withdrawal tests
fail; restoring them returns the suite to green.
- [x] Test resources were independent and cleaned through the existing
flows. Engine adds real PostgreSQL contention tests and `/new`
regression coverage in its companion PR.
- [ ] CI and deployed staging acceptance remain separate from these
local results. Personal subscription operations, every catalog model,
and image/very-long-context execution were not claimed as live coverage.

Design and validation details:
`docs/superpowers/specs/2026-10-09-agent-task-platform-model-override.md`.

Lifecycle clarification: Engine follows its existing model-lifecycle
contract. Expiry blocks new selections; existing Task choices/default
references continue during drain until formal retirement. This does not
introduce automatic substitution. The companion Engine PR adds
execution/projection/admission regression coverage for that distinction.

Draining same-choice retry now passes the public entitlement/catalog
layer only when Engine reports that exact explicit choice as available
and writable. New references, retired/unavailable/read-only choices and
ambiguous aliases remain rejected; expected versions are still passed
unchanged for authoritative Engine CAS. Six additional tests cover
retention/rejection and stale-CAS behavior; Task model plus
route-boundary suites pass 63 tests.
```

