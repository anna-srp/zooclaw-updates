---
title: "开发者平台 Project API Key 建立独立身份：按组织和项目隔离，与 Work 令牌分别校验"
type: "Feature"
priority: "中"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 开发者平台 Project API Key 建立独立身份：按组织和项目隔离，与 Work 令牌分别校验

## 核心宣传点

这次为开发者平台的 Project API Key 建立了独立的身份体系。Project API Key 查询会排除归属于其他组织的记录，同时保留没有组织 ID 的历史命名 Key 通过所属项目仍可读取。平台机器身份新增 owner_uid 字段，从当前生效的个人平台组织和平台用户解析得到，Key 上的创建者字段继续作为审计元数据。/service/v1 新增一种可选开启的混合认证模式，把 zct_ Work 令牌和 zwp_live_ 平台 Key 分别路由到各自的校验器、不做兜底；已部署的默认模式仍是旧模式。Key 的创建、列举、重复吊销、用户与项目隔离、混合路由和既有引擎准入都补了测试。此阶段平台 Key 虽可完成认证，但访问引擎资源和用量仍返回未就绪错误，SDK 运行时、用户维度计费与用量留作后续。

## 分级

- 内部：P1
- 外部：C
- toB 相关：是
- 发布状态：已合并待发版

## PR 说明

## Summary

- Tighten Project API key queries to exclude rows assigned to another
Organization while keeping legacy named-key rows without an Organization
ID readable through their Project.
- Add `owner_uid` to the validated Platform machine principal, resolved
from the active personal Platform Organization and active Platform user.
The key's `created_by` remains audit metadata.
- Add an opt-in `mixed` `/service/v1` auth mode. It routes `zct_` Work
tokens and `zwp_live_` Platform keys to their separate verifiers without
fallback. The deployed default stays `legacy`.
- Cover Key creation, listing, repeated revocation, UID/Project
isolation, mixed routing and the existing Engine gate. Document the
identity boundary and remaining runtime contract.

## Validation

- Focused service and repository tests: 158 passed; the final
no-fallback test is included in the full suite.
- Full local Python CI-equivalent gate: 13,053 passed, 5 skipped,
coverage 89.83%. Dependency resolution, static checks, CI lint and both
duplication checks passed.

## Scope and rollout

- Builds on merged login PR #3937 and supersedes closed PR #3938.
- A Platform Key can authenticate in opt-in mode but still receives
`platform.engine_access_not_ready` for Engine resources and Usage. This
PR does not issue durable Agent credentials, enable SDK runtime,
implement UID Billing or Usage, deploy, clean existing staging data, or
run a billable live test.
- The named-key filter first passed a [read-only staging CSFLE
check](docs/staging-validation/2026-09-30-platform-key-query-csfle-readonly.md).
With approved isolated staging fixtures, the current PR repository code
then passed [actual encrypted-client list, lookup, and revoke
operations](docs/staging-validation/2026-09-30-platform-key-csfle-fixture.md)
for Organization-bound and legacy missing-Organization rows. Each revoke
changed one row, repeats changed none, and both fixture rows were
deleted and verified absent. No deploy or billable request was
performed.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `84cd82b18cdb93a9a749285ad5303f49b6ddd42f`
- PR: #3939
- 作者：finn-srp
- 日期：2026-09-30T03:10:47Z

### Commit Message

```
feat(platform): establish Project key identity alongside Work tokens (#3939)

## Summary

- Tighten Project API key queries to exclude rows assigned to another
Organization while keeping legacy named-key rows without an Organization
ID readable through their Project.
- Add `owner_uid` to the validated Platform machine principal, resolved
from the active personal Platform Organization and active Platform user.
The key's `created_by` remains audit metadata.
- Add an opt-in `mixed` `/service/v1` auth mode. It routes `zct_` Work
tokens and `zwp_live_` Platform keys to their separate verifiers without
fallback. The deployed default stays `legacy`.
- Cover Key creation, listing, repeated revocation, UID/Project
isolation, mixed routing and the existing Engine gate. Document the
identity boundary and remaining runtime contract.

## Validation

- Focused service and repository tests: 158 passed; the final
no-fallback test is included in the full suite.
- Full local Python CI-equivalent gate: 13,053 passed, 5 skipped,
coverage 89.83%. Dependency resolution, static checks, CI lint and both
duplication checks passed.

## Scope and rollout

- Builds on merged login PR #3937 and supersedes closed PR #3938.
- A Platform Key can authenticate in opt-in mode but still receives
`platform.engine_access_not_ready` for Engine resources and Usage. This
PR does not issue durable Agent credentials, enable SDK runtime,
implement UID Billing or Usage, deploy, clean existing staging data, or
run a billable live test.
- The named-key filter first passed a [read-only staging CSFLE
check](docs/staging-validation/2026-09-30-platform-key-query-csfle-readonly.md).
With approved isolated staging fixtures, the current PR repository code
then passed [actual encrypted-client list, lookup, and revoke
operations](docs/staging-validation/2026-09-30-platform-key-csfle-fixture.md)
for Organization-bound and legacy missing-Organization rows. Each revoke
changed one row, repeats changed none, and both fixture rows were
deleted and verified absent. No deploy or billable request was
performed.
```

来源：SerendipityOneInc/ecap-workspace @ 84cd82b1，PR #3939，作者 finn-srp。
