---
title: "修复通过 API 调用 Agent 动作接口返回 404 的问题"
type: "Bug Fix"
priority: "中"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

用服务令牌调用形如 /agents/{id}:action 的接口时会被误判为 Agent 不存在，现已修复，脚本和集成可正常调用。

## 原始内容

fix(claw): proxy agent action ownership checks (#3387)

## Summary
- make the service-token Agent proxy understand controld's
`{agent_id}:action` route grammar
- preserve the complete action path, query parameters, and request body
when forwarding
- keep tenant-hiding behavior for actions targeting Agents owned by
another org

## Root cause
The service API extracted the ownership-check Agent id by splitting only
on `/`. For top-level controld actions such as `POST
/v1/agents/{agent_id}:upgrade-system-prompt`, the `:action` suffix
became part of the Agent id used by the ownership prefetch. The prefetch
therefore queried a nonexistent Agent and failed closed with 404 before
the real action could be forwarded.

## Test plan
- [x] `services/claw-interface/.venv/bin/pytest
services/claw-interface/tests/unit/test_service_proxy_agents.py -q` (22
passed)
- [x] `bash scripts/verify-changed.sh`
- [x] `git diff --check`

---
### PR Body

## Summary
- make the service-token Agent proxy understand controld's `{agent_id}:action` route grammar
- preserve the complete action path, query parameters, and request body when forwarding
- keep tenant-hiding behavior for actions targeting Agents owned by another org

## Root cause
The service API extracted the ownership-check Agent id by splitting only on `/`. For top-level controld actions such as `POST /v1/agents/{agent_id}:upgrade-system-prompt`, the `:action` suffix became part of the Agent id used by the ownership prefetch. The prefetch therefore queried a nonexistent Agent and failed closed with 404 before the real action could be forwarded.

## Test plan
- [x] `services/claw-interface/.venv/bin/pytest services/claw-interface/tests/unit/test_service_proxy_agents.py -q` (22 passed)
- [x] `bash scripts/verify-changed.sh`
- [x] `git diff --check`

