---
title: "Agent 安装激活稳定性提升"
type: "Bug Fix"
priority: "低"
date: "2026-05-23"
status: "待审核"
channels: ""
---

# Agent 安装激活稳定性提升

## 核心宣传点

修复了 Agent 安装后偶尔无法正常激活连接的问题，提升安装成功率

## 原始内容

### Commit: d0f171e — fix(openclaw): wait for agent activation readiness (#1883)

```
fix(openclaw): wait for agent activation readiness (#1883)

## Summary
- wait for the target Mattermost account to be running and connected
before sending post-install activation
- keep legacy runtime compatibility when channelAccounts is absent
- apply the same per-agent readiness wait to hired agent activation and
skip activation when readiness times out

## Tests
- ruff check app/routes/openclaw_agents/core.py
app/routes/openclaw_agents/shared.py tests/unit/test_openclaw_agents.py
- ruff check .
- pytest -W 'ignore::PendingDeprecationWarning'
tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_waits_for_specific_mattermost_account
tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_skips_post_when_specific_mattermost_account_times_out
tests/unit/test_openclaw_agents.py::TestUpdateUserAgentsMMProvisioning::test_rehire_uses_hi_activation_message
tests/unit/test_openclaw_agents.py::TestHireAgent::test_hire_agent_rehire_uses_hi_activation

## Notes
- pyright app tests was attempted locally, but this shell cannot resolve
backend dependencies such as fastapi, pytest, and favie_common outside
the devcontainer/CI environment.
```

### PR #1883 描述

## Summary
- wait for the target Mattermost account to be running and connected before sending post-install activation
- keep legacy runtime compatibility when channelAccounts is absent
- apply the same per-agent readiness wait to hired agent activation and skip activation when readiness times out

## Tests
- ruff check app/routes/openclaw_agents/core.py app/routes/openclaw_agents/shared.py tests/unit/test_openclaw_agents.py
- ruff check .
- pytest -W 'ignore::PendingDeprecationWarning' tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_waits_for_specific_mattermost_account tests/unit/test_openclaw_agents.py::TestCustomAgentInstallUninstall::test_activation_skips_post_when_specific_mattermost_account_times_out tests/unit/test_openclaw_agents.py::TestUpdateUserAgentsMMProvisioning::test_rehire_uses_hi_activation_message tests/unit/test_openclaw_agents.py::TestHireAgent::test_hire_agent_rehire_uses_hi_activation

## Notes
- pyright app tests was attempted locally, but this shell cannot resolve backend dependencies such as fastapi, pytest, and favie_common outside the devcontainer/CI environment.
