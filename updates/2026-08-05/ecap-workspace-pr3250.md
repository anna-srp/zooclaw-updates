---
title: "修复 Agent 测试会话残留旧上下文"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# 修复 Agent 测试会话残留旧上下文

## 核心宣传点

重复运行 Package & Test 时会自动开新会话，测试结果不再被上一轮的对话干扰。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`34c115304425d270008d2f15376ee0f727cdbf19`
- 作者：kaka-srp
- 日期：2026-08-05T09:11:34Z
- PR：#3250

### Commit Message

```
fix(agent-builder): restore v1 test session resets (#3250)

## Summary

- restore the automatic `/new` handshake for reused Agent Builder v1
Pack Test sessions
- keep Engine v2 test runs on their fresh per-run sessions and correct
runtime-specific regression fixtures

## Root cause

The Engine-backed Agent Builder v2 rollout removed the shared preview
chat's reset state machine because v2 creates a fresh Engine session for
every test run. The same component still serves `computer_v1`, whose
Mattermost test bot session can be reused, so v1 lost its session
boundary and could inherit stale context from an earlier Package & Test
run.

## Test plan

- [x] `bash scripts/verify-web.sh
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx'
'web/app/src/app/[locale]/(app)/(chat)/agent-builder/useAgentBuilderTestAutoReset.ts'
'web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push frontend checks
```

### PR Body

## Summary

- restore the automatic `/new` handshake for reused Agent Builder v1 Pack Test sessions
- keep Engine v2 test runs on their fresh per-run sessions and correct runtime-specific regression fixtures

## Root cause

The Engine-backed Agent Builder v2 rollout removed the shared preview chat's reset state machine because v2 creates a fresh Engine session for every test run. The same component still serves `computer_v1`, whose Mattermost test bot session can be reused, so v1 lost its session boundary and could inherit stale context from an earlier Package & Test run.

## Test plan

- [x] `bash scripts/verify-web.sh 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/AgentBuilderTestChat.tsx' 'web/app/src/app/[locale]/(app)/(chat)/agent-builder/useAgentBuilderTestAutoReset.ts' 'web/app/tests/unit/app/agent-builder-test-chat.unit.spec.tsx'`
- [x] `bash scripts/verify-changed.sh`
- [x] pre-commit and pre-push frontend checks

