---
title: "开发者平台登录切换到 ZooWork 账号：邮箱验证码与 Google 登录，每个账号自带一个个人组织隔离项目和 API Key"
type: "Feature"
priority: "中"
date: "2026-09-29"
status: "待审核"
channels: ""
---

# 开发者平台登录切换到 ZooWork 账号：邮箱验证码与 Google 登录，每个账号自带一个个人组织隔离项目和 API Key

## 核心宣传点

开发者平台把原来的第三方登录组件换成了 ZooWork 自家账号体系，走统一接口的邮箱验证码和 Google 登录，接口侧校验账号令牌并使用校验过的用户 ID。每个用户 ID 会自动获得一个个人的平台组织，用来隔离项目和 API Key，沿用已有的平台用户与平台组织数据集合名；上线前需要先清掉旧登录体系遗留的一次性预发记录和唯一索引。以组织钱包为主体的账单路由这次仍然保持关闭，账单页显示为待开放状态，按用户 ID 计费、充值、计量和 API Key 运行时访问都留作后续工作。部署流程同步改为使用新的账号、接口与浏览器端配置。旧的认证回调路由被移除；由于平台此前只发布到预发环境，这次登录切换不为缓存中的旧客户端保留兼容，预发环境里停留在旧页面的标签页刷新后会进入新的入口页。

## 分级

- 内部：P1
- 外部：B
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

- Replace Platform Clerk login with user-interface email OTP and Google login using `business=ecap-platform`. Interface verifies the account JWT and uses the verified UID.
- Give each UID one personal Platform Organization for Project and API key isolation. Reuse the existing `platform_users` and `platform_organizations` collection names. The disposable Clerk-era staging records and unique indexes must be cleaned before rollout.
- Keep the previous Organization-wallet billing routes disabled and show a pending Billing page. UID billing, top-ups, metering and API key runtime access remain follow-up work.
- Update the Platform deployment workflow to use the account, Interface and Firebase browser configuration.
- Remove the old `/auth/callback` route. Platform was only released to staging, so the login cutover does not preserve compatibility for cached Clerk clients; a stale staging tab can reload the new entry page.

## Validation

- Dev login was tested by the requester. A local `/bootstrap` 500 seen during testing came from a temporary test adapter missing `read`; it was unrelated to legacy Project ownership.
- Platform on Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (19 passed), `pnpm build` all passed.
- Interface: `ecap-verify-py-ci` passed with 13,041 tests passed, 5 skipped and 89.83% coverage; dependency, lint and duplication checks passed.

## Rollout

- Deploy backend and frontend together after staging cleanup of the old Platform Clerk data and unique indexes. This PR does not run that cleanup or deploy either service.
- Keep `PLATFORM_UID_BILLING_ENABLED=false`; this PR does not enable Platform API keys for runtime requests.

## Review note

The PR changes 3,940 lines under the repository size rule, including 3,160 deleted lines from the old Clerk UI and tests. `size-override` is requested for this single login migration.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `30366148b1950766181418125e30f03ef5fef01f`
- PR: #3937
- 作者：finn-srp
- 日期：2026-09-29T16:13:06Z

### Commit Message

```
feat(platform): migrate login to ZooWork account (#3937)

## Summary

- Replace Platform Clerk login with user-interface email OTP and Google
login using `business=ecap-platform`. Interface verifies the account JWT
and uses the verified UID.
- Give each UID one personal Platform Organization for Project and API
key isolation. Reuse the existing `platform_users` and
`platform_organizations` collection names. The disposable Clerk-era
staging records and unique indexes must be cleaned before rollout.
- Keep the previous Organization-wallet billing routes disabled and show
a pending Billing page. UID billing, top-ups, metering and API key
runtime access remain follow-up work.
- Update the Platform deployment workflow to use the account, Interface
and Firebase browser configuration.
- Remove the old `/auth/callback` route. Platform was only released to
staging, so the login cutover does not preserve compatibility for cached
Clerk clients; a stale staging tab can reload the new entry page.

## Validation

- Dev login was tested by the requester. A local `/bootstrap` 500 seen
during testing came from a temporary test adapter missing `read`; it was
unrelated to legacy Project ownership.
- Platform on Node 24: `pnpm lint`, `pnpm typecheck`, `pnpm test` (19
passed), `pnpm build` all passed.
- Interface: `ecap-verify-py-ci` passed with 13,041 tests passed, 5
skipped and 89.83% coverage; dependency, lint and duplication checks
passed.

## Rollout

- Deploy backend and frontend together after staging cleanup of the old
Platform Clerk data and unique indexes. This PR does not run that
cleanup or deploy either service.
- Keep `PLATFORM_UID_BILLING_ENABLED=false`; this PR does not enable
Platform API keys for runtime requests.

## Review note

The PR changes 3,940 lines under the repository size rule, including
3,160 deleted lines from the old Clerk UI and tests. `size-override` is
requested for this single login migration.
```

来源：SerendipityOneInc/ecap-workspace @ 30366148，PR #3937，作者 finn-srp。
