---
title: "Agent Pack 市场支持隐藏上架"
type: "产品基础功能更新"
priority: "低"
date: "2026-06-10"
status: "待审核"
channels: ""
---
# Agent Pack 市场支持隐藏上架

## 核心宣传点
后台新增「市场隐藏」开关，可将指定 Agent Pack 从公开市场目录中隐藏，公开列表展示更可控。

## 原始内容
```
fix(agent-packs): hide market packs from catalog (#2346)

## Summary
- Add hide_market to agent-pack schemas, create/update payloads, and
dashboard-console form state.
- Add a dashboard-console Hide market toggle and Hidden market badge for
agent packs.
- Filter public /agent-packs market results at the pack list query layer
with hide_market=false, while leaving internal/admin lists unfiltered.

## Local checks
- pnpm --dir web/dashboard-console test -- app/lib/claw-api.test.ts
tests/packs.test.ts app/routes/agent-packs/route.test.tsx
tests/agent-packs-data.test.ts
- pnpm --dir web/dashboard-console run typecheck
- services/claw-interface/.venv/bin/pytest
tests/unit/test_internal_agent_packs_routes.py
tests/unit/test_public_agent_packs_routes.py
tests/unit/test_pack_services.py tests/unit/test_pack_repo.py
tests/unit/test_routes_pack_store.py tests/unit/test_schema_pack.py
- services/claw-interface/.venv/bin/ruff format --check targeted backend
files
- services/claw-interface/.venv/bin/ruff check targeted backend files
- git diff --check

## Notes
- Local pyright is not available in services/claw-interface/.venv (also
unavailable via python -m pyright).
- wrangler prints a sandbox EPERM warning while trying to write its log
file under ~/Library/Preferences, but dashboard-console typecheck exits
0.

---

### PR Description

## Summary
- Add hide_market to agent-pack schemas, create/update payloads, and dashboard-console form state.
- Add a dashboard-console Hide market toggle and Hidden market badge for agent packs.
- Filter public /agent-packs market results at the pack list query layer with hide_market=false, while leaving internal/admin lists unfiltered.

## Local checks
- pnpm --dir web/dashboard-console test -- app/lib/claw-api.test.ts tests/packs.test.ts app/routes/agent-packs/route.test.tsx tests/agent-packs-data.test.ts
- pnpm --dir web/dashboard-console run typecheck
- services/claw-interface/.venv/bin/pytest tests/unit/test_internal_agent_packs_routes.py tests/unit/test_public_agent_packs_routes.py tests/unit/test_pack_services.py tests/unit/test_pack_repo.py tests/unit/test_routes_pack_store.py tests/unit/test_schema_pack.py
- services/claw-interface/.venv/bin/ruff format --check targeted backend files
- services/claw-interface/.venv/bin/ruff check targeted backend files
- git diff --check

## Notes
- Local pyright is not available in services/claw-interface/.venv (also unavailable via python -m pyright).
- wrangler prints a sandbox EPERM warning while trying to write its log file under ~/Library/Preferences, but dashboard-console typecheck exits 0.

```
