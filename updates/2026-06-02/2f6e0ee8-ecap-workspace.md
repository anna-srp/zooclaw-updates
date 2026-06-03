---
title: "[平台] canonicalize mattermost user on account root"
type: "Bug Fix"
priority: "中"
date: "2026-06-02"
status: "待审核"
channels: ""
---
# [平台] canonicalize mattermost user on account root

## 核心宣传点
来自 ecap-workspace 仓库的更新：fix(claw-interface): canonicalize mattermost user on account root

## 原始内容
**Commit**: 2f6e0ee878dd8d897f303b27a9dd2561b875b036
**Title**: fix(claw-interface): canonicalize mattermost user on account root (#2149)
**Author**: bill-srp
**Date**: 2026-06-02T06:56:00Z

**PR**: #2149

### Commit Message
```
fix(claw-interface): canonicalize mattermost user on account root (#2149)

## Summary
- Add root-level `mattermost_user` field on the account schema as the
canonical location for the human user's Mattermost identity (design:
`docs/superpowers/specs/2026-06-02-account-mattermost-user-root-design.md`).
- Update OpenClaw bot init and warm-pool bot init to write
`mattermost_user` at the account root; new bot records no longer include
`mattermost_user`.
- Read path (`user/enrichment.py`, `openclaw_agents/core.py`) prefers
root `account.mattermost_user` and falls back to legacy
`openclaw_bots[0].mattermost_user` for backwards compatibility.
- Add one-off migration `migrate_mattermost_user_to_account_root.py`
that copies legacy nested data to the account root.

## Root cause
`mattermost_user` previously lived inside `openclaw_bots[*]`, but it
describes the human user's Mattermost account, not a bot. Bot records
stay bot-scoped (`mattermost_bots`); the human Mattermost identity
belongs on the account root.

## Test plan
- [x] `tests/unit/test_openclaw_routes.py` / `test_openclaw_agents.py` —
bot init writes root `mattermost_user`, omits it from the bot record.
- [x] `tests/unit/test_warm_pool_openclaw_assets.py` — warm-pool
materialization writes root `mattermost_user`.
- [x] `tests/unit/test_user_enrichment_service.py` / `test_user_repo.py`
— read prefers root, falls back to legacy nested value.
- [x] `tests/unit/test_migrate_mattermost_user_to_account_root.py` —
migration covers nested→root copy, skip-if-already-root, and dry-run.
```

### PR Description
## Summary
- Add root-level `mattermost_user` field on the account schema as the canonical location for the human user's Mattermost identity (design: `docs/superpowers/specs/2026-06-02-account-mattermost-user-root-design.md`).
- Update OpenClaw bot init and warm-pool bot init to write `mattermost_user` at the account root; new bot records no longer include `mattermost_user`.
- Read path (`user/enrichment.py`, `openclaw_agents/core.py`) prefers root `account.mattermost_user` and falls back to legacy `openclaw_bots[0].mattermost_user` for backwards compatibility.
- Add one-off migration `migrate_mattermost_user_to_account_root.py` that copies legacy nested data to the account root.

## Root cause
`mattermost_user` previously lived inside `openclaw_bots[*]`, but it describes the human user's Mattermost account, not a bot. Bot records stay bot-scoped (`mattermost_bots`); the human Mattermost identity belongs on the account root.

## Test plan
- [x] `tests/unit/test_openclaw_routes.py` / `test_openclaw_agents.py` — bot init writes root `mattermost_user`, omits it from the bot record.
- [x] `tests/unit/test_warm_pool_openclaw_assets.py` — warm-pool materialization writes root `mattermost_user`.
- [x] `tests/unit/test_user_enrichment_service.py` / `test_user_repo.py` — read prefers root, falls back to legacy nested value.
- [x] `tests/unit/test_migrate_mattermost_user_to_account_root.py` — migration covers nested→root copy, skip-if-already-root, and dry-run.

