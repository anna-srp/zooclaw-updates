---
title: "route connectors through integrations"
type: "新功能上线"
priority: "高"
date: "2026-05-29"
status: "待审核"
channels: "Discord,changelog"
---

# route connectors through integrations

## 核心宣传点
新增 route connectors through integrations，让您可以完成更多任务

## 原始内容
feat(web): route connectors through integrations (#2078)

## Linear
https://linear.app/srpone/issue/ECA-864

## Summary
- rename the Settings connectors tab to Integrations/Connectors
- make that Settings tab navigate directly to /integrations/connector
- add the localized /integrations/connector page and redirect the old
/composio-connectors page
- remove the Composio connector page feature flags from frontend and
backend
- keep the legacy connectors section available by deep link while
removing its Composio entry

## Tests
- pnpm --dir web run lint
- pnpm --dir web --filter @zooclaw/web-app test --
tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx
tests/unit/app/claw-settings/ConnectorsSection.unit.spec.tsx
tests/unit/app/composio-connectors/ComposioConnectorsClient.unit.spec.tsx
- pnpm --filter @zooclaw/web-app exec tsc --noEmit
- pytest services/claw-interface/tests/unit/test_composio_connectors.py
- ruff check services/claw-interface/app/settings.py
services/claw-interface/app/routes/composio_connectors.py
services/claw-interface/tests/unit/test_composio_connectors.py
- pyright --pythonpath /Users/shiqi/miniconda3/bin/python
services/claw-interface/app/settings.py
services/claw-interface/app/routes/composio_connectors.py
services/claw-interface/tests/unit/test_composio_connectors.py

---

**PR #2078 Description**:
## Linear
https://linear.app/srpone/issue/ECA-864

## Summary
- rename the Settings connectors tab to Integrations/Connectors
- make that Settings tab navigate directly to /integrations/connector
- add the localized /integrations/connector page and redirect the old /composio-connectors page
- remove the Composio connector page feature flags from frontend and backend
- keep the legacy connectors section available by deep link while removing its Composio entry

## Tests
- pnpm --dir web run lint
- pnpm --dir web --filter @zooclaw/web-app test -- tests/unit/app/claw-settings/ClawSettingsClient.unit.spec.tsx tests/unit/app/claw-settings/ConnectorsSection.unit.spec.tsx tests/unit/app/composio-connectors/ComposioConnectorsClient.unit.spec.tsx
- pnpm --filter @zooclaw/web-app exec tsc --noEmit
- pytest services/claw-interface/tests/unit/test_composio_connectors.py
- ruff check services/claw-interface/app/settings.py services/claw-interface/app/routes/composio_connectors.py services/claw-interface/tests/unit/test_composio_connectors.py
- pyright --pythonpath /Users/shiqi/miniconda3/bin/python services/claw-interface/app/settings.py services/claw-interface/app/routes/composio_connectors.py services/claw-interface/tests/unit/test_composio_connectors.py
