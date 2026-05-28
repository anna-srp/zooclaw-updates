---
title: "主 Agent 可以创建子 Agent 了"
type: "产品基础功能更新"
priority: "高"
date: "2026-05-27"
status: "待审核"
channels: ""
---

# 主 Agent 可以创建子 Agent 了

## 核心宣传点

主 Agent 现在支持在任务执行过程中动态创建子 Agent，让复杂多步骤任务执行更加流畅高效。

## 原始内容

**仓库**: SerendipityOneInc/ecap-workspace  
**SHA**: [17f14df9](https://github.com/SerendipityOneInc/ecap-workspace/commit/17f14df94ce6847e5762fb32bbf69ad03ebcb65e)
**PR**: [#1978](https://github.com/SerendipityOneInc/ecap-workspace/pull/1978)  
**作者**: tim-srp  
**日期**: 2026-05-27T10:11:12Z

**Commit Message:**

```
fix(claw-interface): allow main agent to spawn subagents (#1978)

## Summary
- Add default subagent allowlist config to the main agent during
agents.list sync.
- Keep existing specialist agent allowAgents behavior unchanged.
- Cover the generated main agent config in unit tests.

## Behavior
When claw-interface writes agents.list for selected team agents, the
main agent now gets subagents.allowAgents set to ["*"].

This makes future bot syncs and new bot configs allow Main to spawn
installed team agents by default. Non-main agents already had the same
allowAgents setting and continue to keep it.

## Testing
- pytest -W "ignore:Please use import python_multipart
instead.:PendingDeprecationWarning"
tests/unit/test_openclaw_agents.py::TestApplyAgentsList
- ruff check app/services/openclaw/agent_deploy.py
tests/unit/test_openclaw_agents.py

## Notes
- pyright app/services/openclaw/agent_deploy.py
tests/unit/test_openclaw_agents.py could not run cleanly in my local
environment because pyright could not resolve local test dependencies
pytest and fastapi.
```


**PR Description:**

## Summary
- Add default subagent allowlist config to the main agent during agents.list sync.
- Keep existing specialist agent allowAgents behavior unchanged.
- Cover the generated main agent config in unit tests.

## Behavior
When claw-interface writes agents.list for selected team agents, the main agent now gets subagents.allowAgents set to ["*"].

This makes future bot syncs and new bot configs allow Main to spawn installed team agents by default. Non-main agents already had the same allowAgents setting and continue to keep it.

## Testing
- pytest -W "ignore:Please use import python_multipart instead.:PendingDeprecationWarning" tests/unit/test_openclaw_agents.py::TestApplyAgentsList
- ruff check app/services/openclaw/agent_deploy.py tests/unit/test_openclaw_agents.py

## Notes
- pyright app/services/openclaw/agent_deploy.py tests/unit/test_openclaw_agents.py could not run cleanly in my local environment because pyright could not resolve local test dependencies pytest and fastapi.

