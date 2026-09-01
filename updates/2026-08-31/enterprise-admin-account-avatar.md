---
title: "修复：企业管理后台的账号菜单里不显示头像"
type: "Bug Fix"
priority: "低"
date: "2026-08-31"
status: "待审核"
channels: "Discord+changelog"
---

# 修复：企业管理后台的账号菜单里不显示头像

## 核心宣传点

企业管理后台右上角的账号菜单一直不显示你设置过的头像。问题出在接口层：GET /account/me 没有把已保存的头像返回出来，共享的账号客户端和企业管理后台的解析逻辑也没有保留这个字段。现在三处都补齐了，头像能正常渲染出来。

## 原始内容

- 仓库: SerendipityOneInc/ecap-workspace
- SHA: `5dc25a16e1fc200854d22651a7a3e3556dd8eec4`
- PR: #3600
- 作者: tim-srp
- 日期: 2026-08-31T12:16:45Z

### Commit Message

```
fix(team): align account avatar display (#3600)

## Summary

- return the persisted account avatar from `GET /account/me`
- preserve the avatar in the shared account client and Enterprise Admin
parser
- render the returned avatar in the Enterprise Admin account menu

## Validation

- `pytest services/claw-interface/tests/unit/test_routes_account.py -q`
- `pnpm --filter @zooclaw/auth-client test`
- `pnpm --filter @zooclaw/enterprise-admin test --
lib/__tests__/auth.test.ts`
- `pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit`
- `bash scripts/verify-changed.sh`

## Deployment

This change requires both the claw-interface backend and Enterprise
Admin frontend to be deployed.
```

### PR Description

```
## Summary

- return the persisted account avatar from `GET /account/me`
- preserve the avatar in the shared account client and Enterprise Admin parser
- render the returned avatar in the Enterprise Admin account menu

## Validation

- `pytest services/claw-interface/tests/unit/test_routes_account.py -q`
- `pnpm --filter @zooclaw/auth-client test`
- `pnpm --filter @zooclaw/enterprise-admin test -- lib/__tests__/auth.test.ts`
- `pnpm --filter @zooclaw/enterprise-admin exec tsc --noEmit`
- `bash scripts/verify-changed.sh`

## Deployment

This change requires both the claw-interface backend and Enterprise Admin frontend to be deployed.

```

## 备注

该修复需要 claw-interface 后端与企业管理后台前端同时部署才生效。
