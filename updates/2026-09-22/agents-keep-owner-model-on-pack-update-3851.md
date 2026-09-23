---
title: "修复：更新 Agent Pack 时不再覆盖你自己选的模型"
type: "Bug Fix"
priority: "高"
date: "2026-09-22"
status: "待审核"
channels: ""
---

# 修复：更新 Agent Pack 时不再覆盖你自己选的模型

## 核心宣传点

原地更新 Agent Pack 以前会顺手把这个 Agent 的模型改掉——你手动选的模型会被 Pack 的默认模型（或者平台默认模型）冲掉，而且大部分 Pack 本身没写默认模型，于是每次更新都会退回平台默认。现在更新时会先读当前的模型设置，只要引擎目录里还提供这个模型就原样保留；只有在模型为空或者已经被下架时，才按老逻辑回退到 Pack 默认值。

## 分级

- 内部：P0
- 外部：B
- toB 相关：否
- 发布状态：已合并待发版

## PR 说明

## Summary
- An in-place Pack update (`update_engine_agent`) no longer overwrites
the agent's model. It reads the current `model_primary` and leaves it
untouched when the engine catalog still offers it; only a blank or
withdrawn model falls back to the Pack default, as before.
- New pure helper `model_primary_for_update` in
`engine_model_resolution.py`, plus `catalog_has_model` (full id or
provider-free alias).

## Root cause
`update_engine_agent` unconditionally sent `model_primary =
resolve_engine_model(pack.default_model, catalog,
fallback=ZOOCLAW_ENGINE_DEFAULT_MODEL)`. Packs without a `default_model`
(all eight astock packs, for example) resolve to the platform default,
so every update silently reset the owner's choice. On 2026-09-22 all 30
agents updated across five tenants went from `deepseek-v4-pro` /
`deepseek-flash` / `claude-sonnet-5` to `gpt-5.6-terra` and had to be
restored by hand via `PUT /agents/{ws}/model`. The unconditional send
dates from the original engine services PR (#2883); nothing in history
marks it as intentional.

Behaviour now:

| current model | catalog | update sends |
|---|---|---|
| offered (full id or alias) | non-empty | nothing — model kept |
| any non-blank | empty | nothing — an empty catalog is no evidence of
withdrawal |
| withdrawn / de-entitled | non-empty | Pack default, else platform
default (unchanged) |
| blank | any | Pack default, else platform default (unchanged) |

Auto routing was already safe: update never sends `model_routing`.

## Test plan
- [x] New: keeps the model by full id and by alias, and asserts no
resolution happens; keeps it with an empty catalog; replaces a withdrawn
model with the default
- [x] Existing fallback test
(`test_update_uses_engine_default_when_pack_model_is_unavailable`) still
passes
- [x] 202 passed across the lifecycle, pack-skill update, agent-builder
runtime and v2 route suites
- [x] `verify-py.sh`: ruff, ruff-format, pyright, import-linter all
pass; pre-commit (file length ≤ 500, C901) passes
- [ ] After deploy: update one pack agent whose model differs from the
platform default and confirm `GET /agents/{ws}/model` is unchanged

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `8a60dcce13434a7fac75a6c8765c655bd6edb540`
- PR: #3851
- 作者：siqiao-srp
- 日期：2026-09-22T07:01:35Z

### Commit Message

```
fix(agents): keep the owner's model when updating an engine agent (#3851)

## Summary
- An in-place Pack update (`update_engine_agent`) no longer overwrites
the agent's model. It reads the current `model_primary` and leaves it
untouched when the engine catalog still offers it; only a blank or
withdrawn model falls back to the Pack default, as before.
- New pure helper `model_primary_for_update` in
`engine_model_resolution.py`, plus `catalog_has_model` (full id or
provider-free alias).

## Root cause
`update_engine_agent` unconditionally sent `model_primary =
resolve_engine_model(pack.default_model, catalog,
fallback=ZOOCLAW_ENGINE_DEFAULT_MODEL)`. Packs without a `default_model`
(all eight astock packs, for example) resolve to the platform default,
so every update silently reset the owner's choice. On 2026-09-22 all 30
agents updated across five tenants went from `deepseek-v4-pro` /
`deepseek-flash` / `claude-sonnet-5` to `gpt-5.6-terra` and had to be
restored by hand via `PUT /agents/{ws}/model`. The unconditional send
dates from the original engine services PR (#2883); nothing in history
marks it as intentional.

Behaviour now:

| current model | catalog | update sends |
|---|---|---|
| offered (full id or alias) | non-empty | nothing — model kept |
| any non-blank | empty | nothing — an empty catalog is no evidence of
withdrawal |
| withdrawn / de-entitled | non-empty | Pack default, else platform
default (unchanged) |
| blank | any | Pack default, else platform default (unchanged) |

Auto routing was already safe: update never sends `model_routing`.

## Test plan
- [x] New: keeps the model by full id and by alias, and asserts no
resolution happens; keeps it with an empty catalog; replaces a withdrawn
model with the default
- [x] Existing fallback test
(`test_update_uses_engine_default_when_pack_model_is_unavailable`) still
passes
- [x] 202 passed across the lifecycle, pack-skill update, agent-builder
runtime and v2 route suites
- [x] `verify-py.sh`: ruff, ruff-format, pyright, import-linter all
pass; pre-commit (file length ≤ 500, C901) passes
- [ ] After deploy: update one pack agent whose model differs from the
platform default and confirm `GET /agents/{ws}/model` is unchanged

🤖 Generated with [Claude Code](https://claude.com/claude-code)

---------

Co-authored-by: Claude Opus 5 (1M context) <noreply@anthropic.com>
```

来源：SerendipityOneInc/ecap-workspace @ 8a60dcce，PR #3851，作者 siqiao-srp。
