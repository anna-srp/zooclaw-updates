---
title: "会话重置设置升级：支持“关闭/每日/空闲”三种模式"
type: "产品基础功能更新"
priority: "中"
date: "2026-07-10"
status: "待审核"
channels: ""
---

## 核心宣传点

会话自动重置设置更清晰：现在提供“关闭 / 每日定时 / 空闲重置”三种模式，每日重置时间会按你所在时区自动换算，设置更直观可靠。

## 原始内容

**fix(openclaw): align session reset settings with 6.11 (#2818)**

SHA: `d6ba6fba31461e8d2de08daacfb803590f248378` | 作者: tim-srp | PR #2818

```
fix(openclaw): align session reset settings with 6.11 (#2818)

## Summary
- replace the legacy `off` contract with strict `disabled | daily |
idle` product modes mapped to valid OpenClaw 6.11 config
- replace the complete `session.reset` object while preserving unrelated
FastClaw config, with fail-closed reads and same-process per-bot
serialization
- convert daily reset hours between the user's configured IANA timezone
and UTC, and update the settings UI, API types, cache logic, and tests

## Root cause
The existing frontend and backend persisted `session.reset.mode =
"off"`, but OpenClaw 6.11 accepts only `daily` or `idle`. FastClaw's
deep-merge update also cannot remove stale `idleMinutes` or `atHour`
fields when switching modes, so the reset object must be replaced
canonically.

## Rollout preconditions
- this is a coordinated cutover: claw-interface and the settings
frontend must be deployed together
- all OpenClaw pods must be upgraded to 6.11
- persisted `mode: "off"` values in FastClaw and Kubernetes ConfigMaps
must be migrated to canonical 6.11 reset objects before cutover
- old request payloads and legacy `off` reads are intentionally
unsupported after cutover, as required by the approved design

## Test plan
- [x] `pytest tests/unit/test_openclaw_session_reset.py
tests/unit/test_openclaw_settings_routes.py -q` (305 passed)
- [x] pyright on all touched backend modules and tests (0 errors)
- [x] `pnpm --dir web test` (734 files, 8615 passed, 1 skipped, 1 todo)
- [x] `pnpm exec tsc --noEmit` in `web/app`
- [x] `pnpm --dir web lint` (0 errors; 22 pre-existing enterprise-app
warnings)
- [x] Python pre-commit ruff, formatting, import contracts, dependency
checks, and pyright hooks
- [x] GitHub backend tests, backend lint/typecheck, Web tests, Web
lint/typecheck, Web build, CodeQL, and duplication checks

## Known constraints
- OpenClaw 6.11 stores only an integer `atHour`; 30- and 45-minute
UTC-offset timezones cannot preserve the selected local hour exactly,
and future DST offset changes require recalculation.
- FastClaw has no config version or conditional update API. Same-process
updates are serialized, but concurrent full replacements across
claw-interface replicas still have a race window.
```

### PR body

## Summary
- replace the legacy `off` contract with strict `disabled | daily | idle` product modes mapped to valid OpenClaw 6.11 config
- replace the complete `session.reset` object while preserving unrelated FastClaw config, with fail-closed reads and same-process per-bot serialization
- convert daily reset hours between the user's configured IANA timezone and UTC, and update the settings UI, API types, cache logic, and tests

## Root cause
The existing frontend and backend persisted `session.reset.mode = "off"`, but OpenClaw 6.11 accepts only `daily` or `idle`. FastClaw's deep-merge update also cannot remove stale `idleMinutes` or `atHour` fields when switching modes, so the reset object must be replaced canonically.

## Rollout preconditions
- this is a coordinated cutover: claw-interface and the settings frontend must be deployed together
- all OpenClaw pods must be upgraded to 6.11
- persisted `mode: "off"` values in FastClaw and Kubernetes ConfigMaps must be migrated to canonical 6.11 reset objects before cutover
- old request payloads and legacy `off` reads are intentionally unsupported after cutover, as required by the approved design

## Test plan
- [x] `pytest tests/unit/test_openclaw_session_reset.py tests/unit/test_openclaw_settings_routes.py -q` (305 passed)
- [x] pyright on all touched backend modules and tests (0 errors)
- [x] `pnpm --dir web test` (734 files, 8615 passed, 1 skipped, 1 todo)
- [x] `pnpm exec tsc --noEmit` in `web/app`
- [x] `pnpm --dir web lint` (0 errors; 22 pre-existing enterprise-app warnings)
- [x] Python pre-commit ruff, formatting, import contracts, dependency checks, and pyright hooks
- [x] GitHub backend tests, backend lint/typecheck, Web tests, Web lint/typecheck, Web build, CodeQL, and duplication checks

## Known constraints
- OpenClaw 6.11 stores only an integer `atHour`; 30- and 45-minute UTC-offset timezones cannot preserve the selected local hour exactly, and future DST offset changes require recalculation.
- FastClaw has no config version or conditional update API. Same-process updates are serialized, but concurrent full replacements across claw-interface replicas still have a race window.
