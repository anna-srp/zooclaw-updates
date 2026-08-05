---
title: "安装 Agent 后不再自动发送「Hi」打招呼消息"
type: "体验优化"
priority: "中"
date: "2026-08-04"
status: "待审核"
channels: ""
commit: "941ed9e59a60aab8fa363685dca7f47863ffee09"
repo: "SerendipityOneInc/ecap-workspace"
---

## 核心宣传点

安装或雇佣 Agent 后，系统不再自动替你发送一条「Hi」触发开场白；Agent 会在你第一条真实消息时才开始引导流程，聊天记录更干净、开场更自然。

## 原始内容

```
feat(agents): remove auto Hi greeting after agent install (#3214)

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Remove the automatic "Hi" activation message sent to an agent's
Mattermost DM channel after every install, across all three
computer-runtime install flows (the engine runtime never auto-messaged):
- V2 background install: `agent_install_service.install_agent` no longer
runs the post-commit activation stage; the now-unused
`skip_mattermost_activation` parameter is removed from `install_agent` /
`run_agent_install_background` and its `agent_builder.py` caller.
- Legacy install route (`routes/openclaw_agents/install.py`): activation
block and `activate_agent` stage marks removed.
- Hire flow (`lifecycle.py`): `_activate_hired_agents` removed from
`shared.py`.
- Delete the now-dead helpers
`ensure_agent_mattermost_ready_and_activate`,
`wait_for_agent_mattermost_ready`, and `_account_ready` (vulture
dead-code guard scans `app/`). `post_agent_mattermost_message` and
`get_agent_mattermost_bot_entry` are kept — still used by
`/agents/{agent_id}/reset-session`.
- Keep the `InstallAgentRequest.skip_mattermost_activation` API field:
it still gates deploy-time Mattermost readiness
(`require_mattermost_ready`); only its description changed.

Product note: the auto "Hi" previously triggered `BOOTSTRAP.md`
onboarding right after install/hire. With this change, an agent
bootstraps on the user's first real message instead.

## Test plan
- [x] Unit: 269 tests pass across `test_agent_install_service.py`,
`test_openclaw_agents.py`, `test_agent_builder_routes.py` (install/hire
paths assert no activation message is posted; tests for deleted helpers
removed)
- [x] BDD: 19 scenarios pass in
`tests/bdd/step_defs/test_openclaw_custom_agents.py` against local Mongo
- [x] `bash scripts/verify-py.sh`: ruff + ruff-format + pyright +
import-linter clean (8/8 contracts kept)
- [x] No residual references to removed symbols in `app/`, `tests/`, or
the vulture whitelist

---

### PR Body

<!-- PR 标题：feat(scope): description —— 必须遵循 Conventional Commits -->

## Linear
<!-- 无对应 Linear issue -->

## Summary
- Remove the automatic "Hi" activation message sent to an agent's Mattermost DM channel after every install, across all three computer-runtime install flows (the engine runtime never auto-messaged):
  - V2 background install: `agent_install_service.install_agent` no longer runs the post-commit activation stage; the now-unused `skip_mattermost_activation` parameter is removed from `install_agent` / `run_agent_install_background` and its `agent_builder.py` caller.
  - Legacy install route (`routes/openclaw_agents/install.py`): activation block and `activate_agent` stage marks removed.
  - Hire flow (`lifecycle.py`): `_activate_hired_agents` removed from `shared.py`.
- Delete the now-dead helpers `ensure_agent_mattermost_ready_and_activate`, `wait_for_agent_mattermost_ready`, and `_account_ready` (vulture dead-code guard scans `app/`). `post_agent_mattermost_message` and `get_agent_mattermost_bot_entry` are kept — still used by `/agents/{agent_id}/reset-session`.
- Keep the `InstallAgentRequest.skip_mattermost_activation` API field: it still gates deploy-time Mattermost readiness (`require_mattermost_ready`); only its description changed.

Product note: the auto "Hi" previously triggered `BOOTSTRAP.md` onboarding right after install/hire. With this change, an agent bootstraps on the user's first real message instead.

## Test plan
- [x] Unit: 269 tests pass across `test_agent_install_service.py`, `test_openclaw_agents.py`, `test_agent_builder_routes.py` (install/hire paths assert no activation message is posted; tests for deleted helpers removed)
- [x] BDD: 19 scenarios pass in `tests/bdd/step_defs/test_openclaw_custom_agents.py` against local Mongo
- [x] `bash scripts/verify-py.sh`: ruff + ruff-format + pyright + import-linter clean (8/8 contracts kept)
- [x] No residual references to removed symbols in `app/`, `tests/`, or the vulture whitelist

```
