---
title: "Agent Builder 校验失败可直接在对话中修复"
type: "体验优化"
priority: "中"
date: "2026-07-06"
status: "待审核"
channels: ""
---

# Agent Builder 校验失败可直接在对话中修复

## 核心宣传点

Agent 打包前校验如果没通过，问题会直接回到构建对话里让你继续修改，而不是弹出一个错误就中断，构建流程不再被打断。

## 原始内容

[dcb28a42] fix(agent-builder): keep validation failures repairable (#2748)

## Summary
- send Agent Builder preflight validation failures back into the builder
conversation thread
- keep validation failures repairable by returning the project to
drafting instead of surfacing them as UI errors
- preserve internal iteration failure details for diagnostics

## Tests
- `/home/node/.venvs/claw-interface/bin/python -m pytest
services/claw-interface/tests/unit/test_agent_builder_service.py::test_run_test_iteration_background_stops_when_preflight_validation_fails
-q`
- `bash scripts/verify-py.sh`

--- PR #2748 body ---
## Summary
- send Agent Builder preflight validation failures back into the builder conversation thread
- keep validation failures repairable by returning the project to drafting instead of surfacing them as UI errors
- preserve internal iteration failure details for diagnostics

## Tests
- `/home/node/.venvs/claw-interface/bin/python -m pytest services/claw-interface/tests/unit/test_agent_builder_service.py::test_run_test_iteration_background_stops_when_preflight_validation_fails -q`
- `bash scripts/verify-py.sh`

