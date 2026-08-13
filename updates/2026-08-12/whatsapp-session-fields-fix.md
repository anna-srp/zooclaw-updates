---
title: "修复：WhatsApp 消息因会话字段不兼容而无法送达"
type: "Bug Fix"
priority: "中"
date: "2026-08-12"
status: "待审核"
channels: ""
---

# 修复：WhatsApp 消息因会话字段不兼容而无法送达

## 核心宣传点

WhatsApp 收到的消息一度因为后端会话接口字段变化而报错、无法转给 Agent 处理，现已兼容新旧两种字段，消息可正常送达。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `4c7c085715069170e23fa90e2d8011c01d75a704`
- PR: #3343

### Commit Message

```
fix(whatsapp): accept engine session lifecycle fields (#3343)

## Summary
- accept the current ZooClaw Engine session lifecycle fields
(`run_status` and `archived`) at the Claw Interface boundary
- preserve compatibility with the legacy `status` field for
mixed-version rollouts
- keep malformed responses fail-closed when no lifecycle field is
present

## Root cause
The staging Engine Session API returns HTTP 200 session rows with
`run_status` and `archived`, while Claw Interface required a `status`
string. Pydantic rejected the otherwise valid list response, so
`/whatsapp/sessions/messages` returned `502 service.unavailable` before
posting the inbound WhatsApp event to the Agent session.

## Test plan
- [x] `./.venv/bin/pytest tests/unit/test_engine_client_sessions.py
tests/unit/test_whatsapp_sessions_routes.py -q` (22 passed)
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, and
import-linter passed; pyright used the project virtualenv explicitly to
work around local interpreter discovery)
- [x] `git diff --check`
```

### PR Body

## Summary
- accept the current ZooClaw Engine session lifecycle fields (`run_status` and `archived`) at the Claw Interface boundary
- preserve compatibility with the legacy `status` field for mixed-version rollouts
- keep malformed responses fail-closed when no lifecycle field is present

## Root cause
The staging Engine Session API returns HTTP 200 session rows with `run_status` and `archived`, while Claw Interface required a `status` string. Pydantic rejected the otherwise valid list response, so `/whatsapp/sessions/messages` returned `502 service.unavailable` before posting the inbound WhatsApp event to the Agent session.

## Test plan
- [x] `./.venv/bin/pytest tests/unit/test_engine_client_sessions.py tests/unit/test_whatsapp_sessions_routes.py -q` (22 passed)
- [x] `bash scripts/verify-py.sh` (ruff, format, pyright, and import-linter passed; pyright used the project virtualenv explicitly to work around local interpreter discovery)
- [x] `git diff --check`


---
