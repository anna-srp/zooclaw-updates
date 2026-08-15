---
title: "修复 Agent Builder 一直提示「项目忙碌中」无法继续的问题"
type: "Bug Fix"
priority: "高"
date: "2026-08-14"
status: "待审核"
channels: ""
---

## 核心宣传点

预览运行槽位在异常后无法释放，会让项目长期卡在「忙碌中」；现已修复并能自动恢复。

## 原始内容

fix(agent-builder): recover preview runtime slots under CSFLE (#3388)

## Summary

- replace the Agent Builder package-to-turn aggregation-pipeline update
with a CSFLE-compatible classic update
- preserve the package/turn handoff with exact activity, post, and fence
CAS guards
- skip the transfer path when no Builder turn exists and retry once when
a turn races with cooldown
- add regression coverage for the production-incompatible update shape
and both recovery paths

## Root cause

Staging Mongo's CSFLE analyzer rejects aggregation-pipeline updates on
`ecap-agent-builder-runtime-slots`. `transfer_package_to_active_turn`
used a pipeline even when no active turn matched, so package-test
completion and the recovery cron failed before the slot could enter
cooldown. Expired slots remained in `recovery_required`, and later
requests received the misleading `agent_builder.project_busy` response
indefinitely.

The affected reporter's stale slot was separately released with exact
project/activity/fence preconditions after confirming that the Project
had no workspace operation, TestRun, or active Builder turn.

## Test plan

- [x] `pytest tests/unit/test_agent_builder_runtime_slot_repo.py
tests/unit/test_agent_builder_runtime_capacity_service.py
tests/unit/test_agent_builder_runtime_recovery_service.py -q` — 26
passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`

---
### PR Body

## Summary

- replace the Agent Builder package-to-turn aggregation-pipeline update with a CSFLE-compatible classic update
- preserve the package/turn handoff with exact activity, post, and fence CAS guards
- skip the transfer path when no Builder turn exists and retry once when a turn races with cooldown
- add regression coverage for the production-incompatible update shape and both recovery paths

## Root cause

Staging Mongo's CSFLE analyzer rejects aggregation-pipeline updates on `ecap-agent-builder-runtime-slots`. `transfer_package_to_active_turn` used a pipeline even when no active turn matched, so package-test completion and the recovery cron failed before the slot could enter cooldown. Expired slots remained in `recovery_required`, and later requests received the misleading `agent_builder.project_busy` response indefinitely.

The affected reporter's stale slot was separately released with exact project/activity/fence preconditions after confirming that the Project had no workspace operation, TestRun, or active Builder turn.

## Test plan

- [x] `pytest tests/unit/test_agent_builder_runtime_slot_repo.py tests/unit/test_agent_builder_runtime_capacity_service.py tests/unit/test_agent_builder_runtime_recovery_service.py -q` — 26 passed
- [x] `bash scripts/verify-py.sh`
- [x] `bash scripts/verify-changed.sh`

