---
title: "修复 Ultra 套餐磁盘容量未生效问题"
type: "Bug Fix"
priority: "中"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# 修复 Ultra 套餐磁盘容量未生效问题

## 核心宣传点
修复了套餐升级后机器人磁盘容量未同步更新的问题，Ultra 等套餐的磁盘容量现在能正确生效。

## 原始内容
```
fix(claw-interface): sync plan disk limits to bots (#2338)

## Summary
- Include plan disk limits in bot resource deployment sync payloads.
- Add regression coverage for Starter/Free, Pro, and Ultra disk limits.
- Add coverage that /resources overrides Ultra disk display to the plan
limit.

## Root cause
`sync_bot_resources()` reused `PLAN_RESOURCES` but only copied CPU and
memory into `deployment.resources.limits`, so plan upgrades could leave
the running bot disk limit behind even though creation and /resources
display knew about `disk_limit`.

Linear:
https://linear.app/srpone/issue/ECA-953/ultra-%E7%94%A8%E6%88%B7%E7%A3%81%E7%9B%98%E5%AE%B9%E9%87%8F%E6%98%BE%E7%A4%BA%E4%B8%BA-40gb%E9%9C%80%E4%B8%8E%E8%AE%A2%E9%98%85%E9%9D%A2%E6%9D%BF%E5%B1%95%E7%A4%BA%E4%BF%9D%E6%8C%81%E4%B8%80%E8%87%B4

## Test plan
- [x] `pytest -W ignore::PendingDeprecationWarning
services/claw-interface/tests/unit/test_bot_resources.py
services/claw-interface/tests/unit/test_openclaw_settings_routes.py -q
-k "bot_resources or GetBotResources"`
- [x] `ruff check app/services/bot_resources.py
tests/unit/test_bot_resources.py
tests/unit/test_openclaw_settings_routes.py`
- [x] `pyright -p pyproject.toml app/services/bot_resources.py`
- [x] `ruff check .`

## Notes
- Full `pyright -p pyproject.toml app tests` is blocked in this local
environment by unresolved third-party imports such as `fastapi`,
`pytest`, and `favie_common`; scoped pyright for the changed app module
passes.
- Full `pytest --cov=app --cov-report=term-missing --cov-fail-under=90
-q` was stopped after unrelated existing failures appeared
(`test_unauthenticated_websocket_rejected_e2e`, CORS preflight tests)
and it continued running beyond 35%.

---

### PR Description

## Summary
- Include plan disk limits in bot resource deployment sync payloads.
- Add regression coverage for Starter/Free, Pro, and Ultra disk limits.
- Add coverage that /resources overrides Ultra disk display to the plan limit.

## Root cause
`sync_bot_resources()` reused `PLAN_RESOURCES` but only copied CPU and memory into `deployment.resources.limits`, so plan upgrades could leave the running bot disk limit behind even though creation and /resources display knew about `disk_limit`.

Linear: https://linear.app/srpone/issue/ECA-953/ultra-%E7%94%A8%E6%88%B7%E7%A3%81%E7%9B%98%E5%AE%B9%E9%87%8F%E6%98%BE%E7%A4%BA%E4%B8%BA-40gb%E9%9C%80%E4%B8%8E%E8%AE%A2%E9%98%85%E9%9D%A2%E6%9D%BF%E5%B1%95%E7%A4%BA%E4%BF%9D%E6%8C%81%E4%B8%80%E8%87%B4

## Test plan
- [x] `pytest -W ignore::PendingDeprecationWarning services/claw-interface/tests/unit/test_bot_resources.py services/claw-interface/tests/unit/test_openclaw_settings_routes.py -q -k "bot_resources or GetBotResources"`
- [x] `ruff check app/services/bot_resources.py tests/unit/test_bot_resources.py tests/unit/test_openclaw_settings_routes.py`
- [x] `pyright -p pyproject.toml app/services/bot_resources.py`
- [x] `ruff check .`

## Notes
- Full `pyright -p pyproject.toml app tests` is blocked in this local environment by unresolved third-party imports such as `fastapi`, `pytest`, and `favie_common`; scoped pyright for the changed app module passes.
- Full `pytest --cov=app --cov-report=term-missing --cov-fail-under=90 -q` was stopped after unrelated existing failures appeared (`test_unauthenticated_websocket_rejected_e2e`, CORS preflight tests) and it continued running beyond 35%.
```
