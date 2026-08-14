---
title: "已有账号也能接受企业邀请并切换到企业组织"
type: "新功能上线"
priority: "中"
date: "2026-08-13"
status: "待审核"
channels: ""
---

## 核心宣传点

已经有个人账号的用户可以在确认后加入企业组织，个人订阅续费会自动停掉、企业权益无缝接管；误建的组织也允许唯一管理员退出，来回切换个人/企业身份都不会丢数据。

## 原始内容

仓库：SerendipityOneInc/ecap-workspace
commit：ca3563a9dcbd189b0abeb99c3974abcd19b22681
作者：kaka-srp
日期：2026-08-13T02:57:31Z

**Commit message**

```
feat(org): support existing-account enterprise org switching (#3354)

## Summary

- Unify personal-account and enterprise-account invitation handoff into
one V2 flow with explicit user confirmation.
- Stop all source V2 Agents, schedules, and managed channels before
switching; stop every non-terminal personal subscription renewal while
preserving enterprise package agreements.
- Rebind and verify the canonical Billing V2 key before atomically
swapping the active membership.
- Allow the first/only or last administrator to leave a mistakenly
created organization without changing that organization subscription or
promoting another member.
- Support inactive former-member reinvitation and B → C → B, plus
authenticated invite preview and enterprise-admin confirmation UX.
- Add owner-renewed transition leases, stale-owner fencing, key-bind
crash recovery, compensation, and retry-safe invite handling.

## Scope and safety

- V2 architecture only; no OpenClaw/V1 or iOS changes.
- No new collection, index, migration, or backfill.
- Source enterprise subscriptions remain unchanged.
- Personal subscriptions in pending/manual-review/unknown states fail
closed.
- Lost lease owners cannot mutate the canonical key or invitation
checkpoint.

## Verification

- Backend focused regression: 350 passed.
- Enterprise-admin test suite: 365 passed; ESLint passed.
- `verify-py.sh`: Ruff, Pyright, and all import contracts passed.
- All Python pre-commit/CI custom lint guards passed.
- Real Mongo org lifecycle BDD: 4 passed.
- Real Mongo B → C → B membership transaction and multiple historical
personal-subscription lookup verified.
- Final agent code review: no findings.

## Size override

This cohesive end-to-end change spans the backend coordinator, Billing
V2 cancellation adapters, invitation API, admin confirmation UI,
documentation, and failure-injection tests. Splitting it would create
intermediate revisions where the wire contract or safety invariants are
incomplete, so this PR intentionally uses the repository size override.
```

**PR #3354 body**

## Summary

- Unify personal-account and enterprise-account invitation handoff into one V2 flow with explicit user confirmation.
- Stop all source V2 Agents, schedules, and managed channels before switching; stop every non-terminal personal subscription renewal while preserving enterprise package agreements.
- Rebind and verify the canonical Billing V2 key before atomically swapping the active membership.
- Allow the first/only or last administrator to leave a mistakenly created organization without changing that organization subscription or promoting another member.
- Support inactive former-member reinvitation and B → C → B, plus authenticated invite preview and enterprise-admin confirmation UX.
- Add owner-renewed transition leases, stale-owner fencing, key-bind crash recovery, compensation, and retry-safe invite handling.

## Scope and safety

- V2 architecture only; no OpenClaw/V1 or iOS changes.
- No new collection, index, migration, or backfill.
- Source enterprise subscriptions remain unchanged.
- Personal subscriptions in pending/manual-review/unknown states fail closed.
- Lost lease owners cannot mutate the canonical key or invitation checkpoint.

## Verification

- Backend focused regression: 350 passed.
- Enterprise-admin test suite: 365 passed; ESLint passed.
- `verify-py.sh`: Ruff, Pyright, and all import contracts passed.
- All Python pre-commit/CI custom lint guards passed.
- Real Mongo org lifecycle BDD: 4 passed.
- Real Mongo B → C → B membership transaction and multiple historical personal-subscription lookup verified.
- Final agent code review: no findings.

## Size override

This cohesive end-to-end change spans the backend coordinator, Billing V2 cancellation adapters, invitation API, admin confirmation UI, documentation, and failure-injection tests. Splitting it would create intermediate revisions where the wire contract or safety invariants are incomplete, so this PR intentionally uses the repository size override.

