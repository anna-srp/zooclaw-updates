---
title: "IM 渠道（微信、飞书等）可绑定指定 Agent"
type: "新功能上线"
priority: "高"
date: "2026-05-20"
status: "待审核"
channels: ""
repo: "ecap-workspace"
sha: "666d5cc30c5573e0d34f8da8a7d1f3d2db936cc8"
pr: 1750
---
# IM 渠道（微信、飞书等）可绑定指定 Agent

## 核心宣传点

用户现在可以将微信、飞书等 IM 渠道绑定到特定 Agent，实现精准分发，不同渠道可使用不同的 AI 助手。

## 原始内容

### Commit Message

```
ECA-714 bind IM channels to agents (#1750)

## Summary
- Add target-agent selection for IM channel add/edit/setup flows and
persist channel bindings in OpenClaw config.
- Make per-agent channel bindings read-only while keeping global IM
Channels as the write surface.
- Fix restart/runtime refresh behavior after channel binding changes.
- Migrate Claude command workflows into compact Codex `.agents/skills`
commands.
- Address review consistency risks: clear in-flight agent settings
cache, avoid treating initial loading as restart, and make post-mutation
binding writes best-effort with warning.

## Size override
- This PR intentionally includes ECA-714 channel binding, the requested
Codex skills migration, and follow-up review fixes/tests, which pushes
the diff over the 2000-line size gate.

## Testing
- `pnpm --dir web run lint`
- `pnpm --dir web run tsc`
- `pnpm --dir web/app exec vitest run
tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx
tests/unit/lib/api/openclaw-agent-settings.unit.spec.ts
tests/unit/components/agent-settings/AgentBindingsSection.unit.spec.tsx
tests/unit/components/AgentSettingsPopover.unit.spec.tsx
tests/unit/hooks/useAgentSettings.unit.spec.ts
tests/unit/lib/api/openclaw-settings-extras.unit.spec.ts --config
./vitest.config.mts`
- `pnpm --dir web/app exec vitest run
tests/unit/lib/api/openclaw-agent-settings.unit.spec.ts --config
./vitest.config.mts`
- `pnpm --dir web run test:unit`
- `/home/node/.venvs/claw-interface/bin/ruff check .`
- `/home/node/.venvs/claw-interface/bin/ruff check
app/routes/openclaw_settings/core.py
app/routes/openclaw_settings/feishu.py
app/routes/openclaw_settings/helpers.py
app/routes/openclaw_settings/wecom.py
app/routes/openclaw_settings/weixin.py
tests/unit/test_openclaw_settings_routes.py`
- `/home/node/.venvs/claw-interface/bin/pyright --pythonpath
/home/node/.venvs/claw-interface/bin/python app tests`
- `env PYTHON_DOTENV_DISABLED=1 REDIS_URL= REDIS_AUTH_STRING=
MATTERMOST_URL= MATTERMOST_OPENCLAW_URL= MATTERMOST_ADMIN_TOKEN=
OPENCLAW_PLATFORM_URL=https://claw.example.com
OPENCLAW_PLATFORM_ADMIN_TOKEN=admin-token
OPENCLAW_PLATFORM_LLM_URL=http://llm
/home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_openclaw_settings_routes.py
tests/unit/test_openclaw_settings_wecom.py -q`
- `env PYTHON_DOTENV_DISABLED=1 REDIS_URL= REDIS_AUTH_STRING=
MATTERMOST_URL= MATTERMOST_OPENCLAW_URL= MATTERMOST_ADMIN_TOKEN=
OPENCLAW_PLATFORM_URL= OPENCLAW_PLATFORM_ADMIN_TOKEN=
OPENCLAW_PLATFORM_LLM_URL= /home/node/.venvs/claw-interface/bin/pytest
tests/unit/test_openclaw_settings_routes.py
tests/unit/test_openclaw_settings_wecom.py -q`
```

### PR Description

## Summary
- Add target-agent selection for IM channel add/edit/setup flows and persist channel bindings in OpenClaw config.
- Make per-agent channel bindings read-only while keeping global IM Channels as the write surface.
- Fix restart/runtime refresh behavior after channel binding changes.
- Migrate Claude command workflows into compact Codex `.agents/skills` commands.
- Address review consistency risks: clear in-flight agent settings cache, avoid treating initial loading as restart, and make post-mutation binding writes best-effort with warning.

## Size override
- This PR intentionally includes ECA-714 channel binding, the requested Codex skills migration, and follow-up review fixes/tests, which pushes the diff over the 2000-line size gate.

## Testing
- `pnpm --dir web run lint`
- `pnpm --dir web run tsc`
- `pnpm --dir web/app exec vitest run tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx tests/unit/lib/api/openclaw-agent-settings.unit.spec.ts tests/unit/components/agent-settings/AgentBindingsSection.unit.spec.tsx tests/unit/components/AgentSettingsPopover.unit.spec.tsx tests/unit/hooks/useAgentSettings.unit.spec.ts tests/unit/lib/api/openclaw-settings-extras.unit.spec.ts --config ./vitest.config.mts`
- `pnpm --dir web/app exec vitest run tests/unit/lib/api/openclaw-agent-settings.unit.spec.ts --config ./vitest.config.mts`
- `pnpm --dir web run test:unit`
- `/home/node/.venvs/claw-interface/bin/ruff check .`
- `/home/node/.venvs/claw-interface/bin/ruff check app/routes/openclaw_settings/core.py app/routes/openclaw_settings/feishu.py app/routes/openclaw_settings/helpers.py app/routes/openclaw_settings/wecom.py app/routes/openclaw_settings/weixin.py tests/unit/test_openclaw_settings_routes.py`
- `/home/node/.venvs/claw-interface/bin/pyright --pythonpath /home/node/.venvs/claw-interface/bin/python app tests`
- `env PYTHON_DOTENV_DISABLED=1 REDIS_URL= REDIS_AUTH_STRING= MATTERMOST_URL= MATTERMOST_OPENCLAW_URL= MATTERMOST_ADMIN_TOKEN= OPENCLAW_PLATFORM_URL=https://claw.example.com OPENCLAW_PLATFORM_ADMIN_TOKEN=admin-token OPENCLAW_PLATFORM_LLM_URL=http://llm /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_openclaw_settings_routes.py tests/unit/test_openclaw_settings_wecom.py -q`
- `env PYTHON_DOTENV_DISABLED=1 REDIS_URL= REDIS_AUTH_STRING= MATTERMOST_URL= MATTERMOST_OPENCLAW_URL= MATTERMOST_ADMIN_TOKEN= OPENCLAW_PLATFORM_URL= OPENCLAW_PLATFORM_ADMIN_TOKEN= OPENCLAW_PLATFORM_LLM_URL= /home/node/.venvs/claw-interface/bin/pytest tests/unit/test_openclaw_settings_routes.py tests/unit/test_openclaw_settings_wecom.py -q`
