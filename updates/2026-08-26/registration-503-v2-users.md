---
title: "修复：新用户注册时报 503，创建个人空间失败"
type: "Bug Fix"
priority: "高"
date: "2026-08-26"
status: "待审核"
channels: ""
---

# 修复：新用户注册时报 503，创建个人空间失败

## 核心宣传点

新用户注册创建个人空间时会因为依赖一套已经不再使用的旧版 Agent 资源而报 503 失败——旧版服务一旦缩容或抖动，注册就整条断掉。现在符合新版运行时条件的账号在注册时会完全跳过这套旧依赖，注册流程不再受它影响；仍在老版本上的账号保持原有流程不变。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `466df714fcb9757f996ff55f07a39e57e87f957c`
- PR: #3532
- 作者: tim-srp
- 日期: 2026-08-26T11:27:29Z

### Commit Message

```
fix(registration): skip warm pool and V1 app creation for V2-eligible users (#3532)

## Problem

Staging `POST /account/personal-org` fails for new users with 503
`account.openclaw_app_initialization_failed`. Root-cause chain:

```
node-pool scale-down (infra-pool -> 0) -> V1 FastClaw has no instances
-> Envoy overload 503 -> register() unconditionally calls V1 create_app in its fallback -> registration 503
```

Even with `AGENTS_V2_ENABLED=true`, `register()` has no V2 branch:
warm-pool claims require V1-provisioned `openclaw_app` assets, and the
fallback always creates a V1 app.

## Fix

`register()` now judges V2 eligibility with the same
`get_agents_v2_eligibility` gate engine agent install uses
(`engine_main_agent_service`):

- **V2-eligible**: skip `claim_warm_pool_account` and
`create_openclaw_app_record` entirely; `openclaw_app` stays `None`.
Billing init + upsert unchanged — the proven fallback path minus the V1
app. A FastClaw outage (or an empty/disabled warm pool) no longer blocks
registration.
- **Non-eligible**: legacy warm-pool → V1-app flow untouched (safe for
future production partial rollout).

Downstream is already decoupled: org creation only needs the billing
`team_id`, billing keys come from `ensure_billing_initialized`, and
default-main-agent provisioning only reads `(uid, org_id, token)` with
the same eligibility gate as its first check. The register response
schema never serialized `openclaw_app`, so there is no API-compat
impact.

Complements the already-merged frontend BossClaw V2 migration (#3501)
and route rename (#3528): the frontend runs engine-only, and
registration no longer drags V1 in.

## Tests

- New: V2-eligible registration skips warm-pool claim and V1 app
creation (zero-call assertions, `openclaw_app=None`, billing intact)
- New: V2-eligible registration succeeds when FastClaw app creation
fails (simulates the staging outage)
- Existing 13 register tests, route tests, and eligibility tests all
pass; `verify-py.sh` (ruff + format + pyright + import-linter) clean

Design spec:
`docs/superpowers/specs/2026-08-26-v2-registration-drop-v1-app-dependency.md`

Co-authored-by: Claude <noreply@anthropic.com>
```

### PR Description

```
## Problem

Staging `POST /account/personal-org` fails for new users with 503 `account.openclaw_app_initialization_failed`. Root-cause chain:

```
node-pool scale-down (infra-pool -> 0) -> V1 FastClaw has no instances
-> Envoy overload 503 -> register() unconditionally calls V1 create_app in its fallback -> registration 503
```

Even with `AGENTS_V2_ENABLED=true`, `register()` has no V2 branch: warm-pool claims require V1-provisioned `openclaw_app` assets, and the fallback always creates a V1 app.

## Fix

`register()` now judges V2 eligibility with the same `get_agents_v2_eligibility` gate engine agent install uses (`engine_main_agent_service`):

- **V2-eligible**: skip `claim_warm_pool_account` and `create_openclaw_app_record` entirely; `openclaw_app` stays `None`. Billing init + upsert unchanged — the proven fallback path minus the V1 app. A FastClaw outage (or an empty/disabled warm pool) no longer blocks registration.
- **Non-eligible**: legacy warm-pool → V1-app flow untouched (safe for future production partial rollout).

Downstream is already decoupled: org creation only needs the billing `team_id`, billing keys come from `ensure_billing_initialized`, and default-main-agent provisioning only reads `(uid, org_id, token)` with the same eligibility gate as its first check. The register response schema never serialized `openclaw_app`, so there is no API-compat impact.

Complements the already-merged frontend BossClaw V2 migration (#3501) and route rename (#3528): the frontend runs engine-only, and registration no longer drags V1 in.

## Tests

- New: V2-eligible registration skips warm-pool claim and V1 app creation (zero-call assertions, `openclaw_app=None`, billing intact)
- New: V2-eligible registration succeeds when FastClaw app creation fails (simulates the staging outage)
- Existing 13 register tests, route tests, and eligibility tests all pass; `verify-py.sh` (ruff + format + pyright + import-linter) clean

Design spec: `docs/superpowers/specs/2026-08-26-v2-registration-drop-v1-app-dependency.md`

```
