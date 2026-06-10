---
title: "连接状态更准、消息延迟更低"
type: "产品基础功能更新"
priority: "中"
date: "2026-06-09"
status: "待审核"
channels: ""
---

# 连接状态更准、消息延迟更低

## 核心宣传点

页面顶部的「机器人在线/连接」状态现在更准确、更及时，配合后端改造缓解了偶发的连接未就绪和消息延迟。

## 原始内容

完整 commit message：

```
feat(computers): proxy FastClaw status (#2288)

## Summary
- add claw-interface computer status proxy backed by FastClaw bot status
- expose Next.js API route and client helper for computer status
- update ClawPageHeader to use FastClaw readiness plus Mattermost
instead of OpenClaw websocket status

## Linear

https://linear.app/srpone/issue/ECA-913/mitigate-openclaw-pod-notready-and-message-latency

## Test plan
- pnpm --dir web run lint
- pnpm --dir web run test:unit
- pnpm --dir web/app exec eslint
'src/app/api/openclaw/computers/[computerId]/status/route.ts'
src/lib/api/openclaw.ts src/components/ClawPageHeader.tsx
tests/unit/components/ClawPageHeader.unit.spec.ts
- pnpm --dir web/app exec vitest run
tests/unit/components/ClawPageHeader.unit.spec.ts
tests/unit/components/ClawPageHeader-extras.unit.spec.tsx
- ruff check .
- PYTHONPATH=. .venv/bin/python -m pytest
tests/unit/test_computer_routes.py tests/unit/test_computer_service.py
-q

## Notes
- pnpm --dir web run tsc currently fails before this change because
web/app/.next/types contains stale generated route references.
- pyright app tests only fails on missing
favie_common.logging/request_context in the local venv.
- full backend pytest coverage is blocked locally by sandboxed Mongo DNS
and missing favie_common request_context modules.
```

PR 描述：

## Summary
- add claw-interface computer status proxy backed by FastClaw bot status
- expose Next.js API route and client helper for computer status
- update ClawPageHeader to use FastClaw readiness plus Mattermost instead of OpenClaw websocket status

## Linear
https://linear.app/srpone/issue/ECA-913/mitigate-openclaw-pod-notready-and-message-latency

## Test plan
- pnpm --dir web run lint
- pnpm --dir web run test:unit
- pnpm --dir web/app exec eslint 'src/app/api/openclaw/computers/[computerId]/status/route.ts' src/lib/api/openclaw.ts src/components/ClawPageHeader.tsx tests/unit/components/ClawPageHeader.unit.spec.ts
- pnpm --dir web/app exec vitest run tests/unit/components/ClawPageHeader.unit.spec.ts tests/unit/components/ClawPageHeader-extras.unit.spec.tsx
- ruff check .
- PYTHONPATH=. .venv/bin/python -m pytest tests/unit/test_computer_routes.py tests/unit/test_computer_service.py -q

## Notes
- pnpm --dir web run tsc currently fails before this change because web/app/.next/types contains stale generated route references.
- pyright app tests only fails on missing favie_common.logging/request_context in the local venv.
- full backend pytest coverage is blocked locally by sandboxed Mongo DNS and missing favie_common request_context modules.

