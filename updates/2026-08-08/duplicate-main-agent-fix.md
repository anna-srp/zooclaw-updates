---
title: "修复老用户助手列表出现重复「Assistant」的问题"
type: "Bug Fix"
priority: "中"
date: "2026-08-08"
status: "待审核"
channels: ""
---

## 核心宣传点

从旧版本迁移过来的用户，打开助手列表时不会再被凭空多塞一个重复的默认助手；默认助手只在注册时创建一次，新用户若首次安装失败也会自动重试修复。

## 原始内容

Commit: 82e95571e837b2921250460447fb070e6a629214
作者: bill-srp / 日期: 2026-08-08T10:38:57Z

### Commit Message

feat(agents): Provision default main agent only at registration (#3306)

## Linear
<!-- No dedicated Linear issue — follow-up scope decision on the v2
default main agent rollout (PR #3287). -->

## Summary
- Fresh-install the v2 default main agent (`Assistant`) **only at
registration**: the three register handlers in `app/routes/account.py`
(personal, team-org, invite) are the only paths that can create the
workspace row.
- **Why**: migrated v1 main agents carry `migration_v1_to_v2` metadata /
legacy `agent_id` but no `internal_role`, so the previous lazy list-time
install (`get_by_internal_role` lookup) could not see them and would
install a duplicate v2 Assistant for existing v1 users on their next
agents-list load.
- The agents list route keeps a **retry-only** best-effort call
(`ensure_default_main_agent(..., retry_only=True)`): it never creates a
row, it only reclaims an `install_failed` row that registration itself
created — so a new registrant whose install hit a transient engine
failure self-heals on next page load (the persisted "Please retry"
message stays true), while migrated/existing users remain invisible to
it by design.

## Test plan
- [x] Route: list calls ensure with `retry_only=True` and survives
ensure failure (best-effort)
- [x] Service: `retry_only=True` + no row → `None`, no claim/engine
calls (duplicate-prevention for migrated v1 users); + `install_failed`
row → reclaims and reinstalls; + `active` row → returned untouched
- [x] `pytest tests/unit/test_agents_v2_routes.py
tests/unit/test_engine_main_agent_service.py
tests/unit/test_routes_account.py
tests/unit/test_account_team_org_route.py` — 85 passed
- [x] `ruff check` / `ruff format --check` clean
- [x] `pyright app/ tests/` — 0 errors
- [x] `lint-imports` — 8 contracts kept

### PR Body

## Linear
<!-- No dedicated Linear issue — follow-up scope decision on the v2 default main agent rollout (PR #3287). -->

## Summary
- Fresh-install the v2 default main agent (`Assistant`) **only at registration**: the three register handlers in `app/routes/account.py` (personal, team-org, invite) are the only paths that can create the workspace row.
- **Why**: migrated v1 main agents carry `migration_v1_to_v2` metadata / legacy `agent_id` but no `internal_role`, so the previous lazy list-time install (`get_by_internal_role` lookup) could not see them and would install a duplicate v2 Assistant for existing v1 users on their next agents-list load.
- The agents list route keeps a **retry-only** best-effort call (`ensure_default_main_agent(..., retry_only=True)`): it never creates a row, it only reclaims an `install_failed` row that registration itself created — so a new registrant whose install hit a transient engine failure self-heals on next page load (the persisted "Please retry" message stays true), while migrated/existing users remain invisible to it by design.

## Test plan
- [x] Route: list calls ensure with `retry_only=True` and survives ensure failure (best-effort)
- [x] Service: `retry_only=True` + no row → `None`, no claim/engine calls (duplicate-prevention for migrated v1 users); + `install_failed` row → reclaims and reinstalls; + `active` row → returned untouched
- [x] `pytest tests/unit/test_agents_v2_routes.py tests/unit/test_engine_main_agent_service.py tests/unit/test_routes_account.py tests/unit/test_account_team_org_route.py` — 85 passed
- [x] `ruff check` / `ruff format --check` clean
- [x] `pyright app/ tests/` — 0 errors
- [x] `lint-imports` — 8 contracts kept

