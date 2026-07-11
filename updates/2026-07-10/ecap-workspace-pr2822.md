---
title: "Agent Builder 版本冲突可自动修复并反馈"
type: "Agent 上架/更新"
priority: "中"
date: "2026-07-10"
status: "待审核"
channels: ""
---

## 核心宣传点

在 Agent Builder 中打包测试时，如果遇到版本号重复等可修复的错误，现在会把清晰的错误说明直接反馈到 Builder 对话里，并把项目退回草稿状态，方便你直接修改，不再卡在失败状态。

## 原始内容

**fix(agent-builder): return version conflicts to builder (#2822)**

SHA: `2294916920112f8909586839fe92d3b304a3746a` | 作者: kaka-srp | PR #2822

```
fix(agent-builder): return version conflicts to builder (#2822)

## Summary
- classify Agent Builder validation failures and duplicate Pack Test
versions as repairable preflight errors
- send repairable error summaries to the Builder thread, return the
project to `drafting`, and retain iteration diagnostics
- report repaired duplicate-version iterations as warnings in
operational diagnostics
- accept structured repairable error codes from `publish.py` when a
future Agent Studio release provides them

## Root cause
The Package & Test background handler only considered the exact code
`agent_builder.validation_failed` repairable. The duplicate-version
preflight introduced `agent_builder.pack_version_exists`, so its summary
was stored in the UI error fields without ever being posted to the Agent
Studio Builder thread. The project therefore remained `failed` even
though updating `agent/agent-pack.yaml` was a workspace-repairable
action.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pytest
services/claw-interface/tests/unit/test_agent_builder_service.py
services/claw-interface/tests/unit/test_agent_builder_diagnostics.py -q`
— 119 passed
- [x] pre-commit Python guards: ruff, format, pyright, complexity,
dependency consistency, import contracts, dead code

## Follow-up boundary
The reproduced issue is caught by claw-interface preflight and is fully
fixed here. A separate Agent Studio pack change would only be needed to
preserve the structured error code for the rare race where the version
becomes occupied after preflight but before the Pack Test create
request; that defensive follow-up is intentionally not required for this
PR.
```

### PR body

## Summary
- classify Agent Builder validation failures and duplicate Pack Test versions as repairable preflight errors
- send repairable error summaries to the Builder thread, return the project to `drafting`, and retain iteration diagnostics
- report repaired duplicate-version iterations as warnings in operational diagnostics
- accept structured repairable error codes from `publish.py` when a future Agent Studio release provides them

## Root cause
The Package & Test background handler only considered the exact code `agent_builder.validation_failed` repairable. The duplicate-version preflight introduced `agent_builder.pack_version_exists`, so its summary was stored in the UI error fields without ever being posted to the Agent Studio Builder thread. The project therefore remained `failed` even though updating `agent/agent-pack.yaml` was a workspace-repairable action.

## Test plan
- [x] `bash scripts/verify-changed.sh`
- [x] `pytest services/claw-interface/tests/unit/test_agent_builder_service.py services/claw-interface/tests/unit/test_agent_builder_diagnostics.py -q` — 119 passed
- [x] pre-commit Python guards: ruff, format, pyright, complexity, dependency consistency, import contracts, dead code

## Follow-up boundary
The reproduced issue is caught by claw-interface preflight and is fully fixed here. A separate Agent Studio pack change would only be needed to preserve the structured error code for the rare race where the version becomes occupied after preflight but before the Pack Test create request; that defensive follow-up is intentionally not required for this PR.

