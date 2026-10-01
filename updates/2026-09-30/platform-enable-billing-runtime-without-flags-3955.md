---
title: "开发者平台的账单与 Project Key 运行能力正式开启：API Key 现在能跑 Agent 了"
type: "Feature"
priority: "高"
date: "2026-09-30"
status: "待审核"
channels: ""
---

# 开发者平台的账单与 Project Key 运行能力正式开启：API Key 现在能跑 Agent 了

## 核心宣传点

开发者平台的账单和 Project Key 运行时其实早就做完了，但默认的开关设置一直把它们藏着。这次把 PLATFORM_BILLING_ENABLED 和 SERVICE_API_AUTH_MODE 两个开关彻底去掉，/service/v1 现在同时接受 Work 的 zct_ 令牌和平台的 zwp_live_ Key，两者走各自独立的校验通道、不互相兜底。界面上原先那句「API Key 不能运行 Agent」的提示被移除，用量接口已经可用（用量页面本身还是占位）。Work 令牌的创建、存储、哈希、JWT 加密、成员校验、计费凭据、算力策略和引擎归属全部保持不变，缺少服务凭据时的原有错误码也照旧。发布按先去开关、再部署预发、预发端到端验证通过后再考虑生产的顺序推进。

## 分级

- 内部：P0
- 外部：A
- toB 相关：是
- 发布状态：已随正式 release 上线

## PR 说明

## Summary

Platform billing and Project-key runtime are implemented, but default
activation settings still hide them. Remove `PLATFORM_BILLING_ENABLED`
and `SERVICE_API_AUTH_MODE`; `/service/v1` now accepts both Work `zct_`
tokens and Platform `zwp_live_` keys through separate namespace-selected
authenticators. Fix the Platform account business to `ecap-platform` and
remove the redundant `API_PLATFORM_BUSINESS` setting.

Keep existing Work token creation, storage, hashing, JWT encryption,
membership checks, billing credentials, compute policy and Engine
attribution unchanged. Preserve the original Work error code for
missing/non-service credentials. Keep Platform storage readiness,
ownership, credits and payment checks. Existing frontend URL,
encryption, billing and Engine configuration remains required.

Remove UI notices claiming API keys cannot run Agents, and update the
current operations documentation. Usage APIs are available; the frontend
Usage page remains a placeholder.

## Root cause

The old rollout settings defaulted billing off and service
authentication to Work-only, even after Platform Org billing and runtime
integration landed. They were also configurable across both products, so
replacing them must preserve the existing Work authentication path.

Rollout follows the requested sequence: remove the flags, deploy
staging, then complete staging end-to-end validation before considering
production. The current Service and Platform workflows deploy main
pushes to staging; production requires a separate release tag or
explicit production workflow dispatch. This PR does not initiate
production promotion. The automatic review's rollout-sequencing note
does not require restoring a flag or changing Work key configuration.

## Test plan

- [x] Work compatibility checks through HTTP and the real
dispatch/authentication functions, with real token hashing and JWT
encryption: existing-key Agent creation and credential seeding, Work
usage attribution, revoked/unknown keys, suspended membership and
tampered ciphertext. Database and Engine calls are mocked.
- [x] 65 targeted Work/Platform authentication and proxy tests.
- [x] Node 24 Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (27
tests), and `pnpm build` on the final rebased commit.
- [x] Final rebased commit: local `ecap-verify-py-ci` (Linux
dependencies, static checks, all ci-lint guards, both duplication
checks, full pytest and coverage): 13,347 passed, 5 skipped; 89.89%
coverage against the 89.5% CI threshold.
- [ ] Staging end-to-end login, top-up and billable Agent execution
after deployment; this PR does not run live billing tests or modify
deployed secrets.

## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `6de207c9d52992028b913254520bf04728da2059`
- PR: #3955
- 作者：finn-srp
- 日期：2026-09-30T13:19:57Z

### Commit Message

```
fix(platform): enable billing and runtime without activation flags (#3955)

## Summary

Platform billing and Project-key runtime are implemented, but default
activation settings still hide them. Remove `PLATFORM_BILLING_ENABLED`
and `SERVICE_API_AUTH_MODE`; `/service/v1` now accepts both Work `zct_`
tokens and Platform `zwp_live_` keys through separate namespace-selected
authenticators. Fix the Platform account business to `ecap-platform` and
remove the redundant `API_PLATFORM_BUSINESS` setting.

Keep existing Work token creation, storage, hashing, JWT encryption,
membership checks, billing credentials, compute policy and Engine
attribution unchanged. Preserve the original Work error code for
missing/non-service credentials. Keep Platform storage readiness,
ownership, credits and payment checks. Existing frontend URL,
encryption, billing and Engine configuration remains required.

Remove UI notices claiming API keys cannot run Agents, and update the
current operations documentation. Usage APIs are available; the frontend
Usage page remains a placeholder.

## Root cause

The old rollout settings defaulted billing off and service
authentication to Work-only, even after Platform Org billing and runtime
integration landed. They were also configurable across both products, so
replacing them must preserve the existing Work authentication path.

Rollout follows the requested sequence: remove the flags, deploy
staging, then complete staging end-to-end validation before considering
production. The current Service and Platform workflows deploy main
pushes to staging; production requires a separate release tag or
explicit production workflow dispatch. This PR does not initiate
production promotion. The automatic review's rollout-sequencing note
does not require restoring a flag or changing Work key configuration.

## Test plan

- [x] Work compatibility checks through HTTP and the real
dispatch/authentication functions, with real token hashing and JWT
encryption: existing-key Agent creation and credential seeding, Work
usage attribution, revoked/unknown keys, suspended membership and
tampered ciphertext. Database and Engine calls are mocked.
- [x] 65 targeted Work/Platform authentication and proxy tests.
- [x] Node 24 Platform `pnpm lint`, `pnpm typecheck`, `pnpm test` (27
tests), and `pnpm build` on the final rebased commit.
- [x] Final rebased commit: local `ecap-verify-py-ci` (Linux
dependencies, static checks, all ci-lint guards, both duplication
checks, full pytest and coverage): 13,347 passed, 5 skipped; 89.89%
coverage against the 89.5% CI threshold.
- [ ] Staging end-to-end login, top-up and billable Agent execution
after deployment; this PR does not run live billing tests or modify
deployed secrets.
```

来源：SerendipityOneInc/ecap-workspace @ 6de207c9，PR #3955，作者 finn-srp。
