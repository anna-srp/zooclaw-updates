---
title: "修复：新注册用户的默认主 Agent 现在会自动启动"
type: Bug Fix
priority: 中
date: 2026-08-17
status: "待审核"
channels: ""
---

## 核心宣传点

以前新用户注册完成后，系统里的默认主 Agent 虽然装好了却没有真正跑起来，需要额外一步才能用。现在安装完成后会立即自动启动，注册完就能直接开始对话，开箱即用。

## 原始内容

**Commit**: `17892c22` — fix(agents): start default main agent after install (#3406)
**作者**: bill-srp ｜ **日期**: 2026-08-17T04:01:01Z

```
fix(agents): start default main agent after install (#3406)

# What

Start the V2 default main agent on the engine immediately after a fresh install, instead of leaving it provisioned-but-stopped.

`_install_bare_main_agent` (in `app/services/agents/engine_main_agent_service.py`) previously called `client.start_agent(...)` only when reviving a `disabled` workspace row (`restart_existing`). A brand-new registration created the engine agent, seeded credentials, bound the Mattermost channel, and marked the row `active` — but never started the agent. The 2026-07-14 engine design spec's "active = provisioned, NOT running; no auto-start" behavior is intentionally changed here for the default main agent per product decision.

# How

- `start_agent` is now awaited unconditionally after `seed_engine_agent_credentials` (credentials are seeded right before, so the engine's `platform_credentials_required` 409 gate is satisfied).
- `restart_existing` keeps its one remaining job: skipping the Mattermost channel re-bind on revival.
- A start failure propagates unchanged: the row is marked `install_failed` (reclaimable) and the agents-list `retry_only` path retries it on the next `GET /agents`, so registration is never blocked.

# Tests (TDD)

- `test_fresh_create_is_bare_and_activates` now asserts `start_agent` is awaited with the created agent id, and pins seed → start ordering via an events list.
- `test_reclaimed_engine_row_skips_create_and_starts` (renamed) asserts a reclaimed installing row is also started.
- New `test_start_failure_marks_install_failed_and_raises` mirrors the create-failure test for the start step.
- `test_disabled_existing_main_agent_is_started_before_reactivation` unchanged and passing.

# Test plan

- [x] `bash scripts/verify-py.sh` — ruff, ruff-format, pyright, import-linter all green
- [x] `pytest tests/unit/test_engine_main_agent_service.py -q` — 12 passed
- [ ] CI (`claw-interface-quality`) green
- [ ] Staging smoke after backend release: register a fresh user, confirm the main agent reports running without manual start
```
