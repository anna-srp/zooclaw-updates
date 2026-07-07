---
title: "Agent Builder 打包测试流程更可靠"
type: "Bug Fix"
priority: "中"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# Agent Builder 打包测试流程更可靠

## 核心宣传点

修复了 Agent Builder 在校验未通过时仍可能继续进入打包测试的问题，并在首次安装后确认运行环境真正就绪才打开对话，做 Agent 的过程更稳不踩坑。

## 原始内容

[fadb1927] fix(agent-builder): harden package test gates (#2744)

## Summary
- Enforce Agent Builder managed Pack & Test ownership at the
`/pack-test-runs` endpoint with a CAS claim/finalize/release flow.
- Add backend preflight validation before packaging, including
`validate.py --skip-online-validation --pack-test-gate`, metadata
parsing, and duplicate pack version checks.
- Add first-install Agent Studio runtime routing verification with retry
and recoverable reopen behavior.

Linear: https://linear.app/srpone/issue/ECA-1177

## Root cause
Agent Builder could proceed into Pack Test after local validation
errors, and the generic Pack Test endpoint could create runs without
atomically writing `current_test_run_id` back to the Agent Builder
project. Separately, Agent Studio install success did not verify that
the runtime Mattermost routing config was actually active before opening
the builder conversation.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_agent_builder_service.py
services/claw-interface/tests/unit/test_pack_test_routes.py -q`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`

--- PR #2744 body ---
## Summary
- Enforce Agent Builder managed Pack & Test ownership at the `/pack-test-runs` endpoint with a CAS claim/finalize/release flow.
- Add backend preflight validation before packaging, including `validate.py --skip-online-validation --pack-test-gate`, metadata parsing, and duplicate pack version checks.
- Add first-install Agent Studio runtime routing verification with retry and recoverable reopen behavior.

Linear: https://linear.app/srpone/issue/ECA-1177

## Root cause
Agent Builder could proceed into Pack Test after local validation errors, and the generic Pack Test endpoint could create runs without atomically writing `current_test_run_id` back to the Agent Builder project. Separately, Agent Studio install success did not verify that the runtime Mattermost routing config was actually active before opening the builder conversation.

## Test plan
- [x] `/home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_agent_builder_service.py services/claw-interface/tests/unit/test_pack_test_routes.py -q`
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`

