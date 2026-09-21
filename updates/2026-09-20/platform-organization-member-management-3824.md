---
title: "feat(platform): add organization member management (#3824)"
type: "新功能"
priority: "中"
date: "2026-09-20"
status: "待审核"
channels: ""
---

# Platform 支持组织成员与邀请管理

## 核心宣传点

Platform 账号菜单新增 Organization 设置入口，点进去直接打开 Clerk 自带的组织资料页，用来管理成员和邀请。成员关系与邀请仍然以 Clerk 为准，没有新增 Platform 侧的表或接口，也就不存在两套数据不一致的问题。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已合并待发版

## PR 说明

## Linear

N/A

## Summary

- add an Organization settings entry to the Platform account menu
- open Clerk's built-in Organization profile for member and invitation management
- keep Clerk authoritative for memberships and invitations; no Platform table or API is added
- update the phase-one product and architecture notes to reflect the supported Clerk-managed flow

## Test plan

- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit/component tests (15 passed)
- [x] Platform production build



## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `faa2ddca9acedada2683145799c731e05b133e2e`
- PR: #3824
- 作者：finn-srp
- 日期：2026-09-20T14:24:49Z

### Commit Message

```
feat(platform): add organization member management (#3824)

## Linear

N/A

## Summary

- add an Organization settings entry to the Platform account menu
- open Clerk's built-in Organization profile for member and invitation
management
- keep Clerk authoritative for memberships and invitations; no Platform
table or API is added
- update the phase-one product and architecture notes to reflect the
supported Clerk-managed flow

## Test plan

- [x] Platform lint
- [x] Platform typecheck
- [x] Platform unit/component tests (15 passed)
- [x] Platform production build
```

来源：SerendipityOneInc/ecap-workspace @ faa2ddca，PR #3824，作者 finn-srp。