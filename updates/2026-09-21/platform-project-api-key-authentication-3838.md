---
title: "feat(platform): add project API key authentication (#3838)"
type: "新功能"
priority: "中"
date: "2026-09-21"
status: "待审核"
channels: ""
---

# 开发者平台：项目 API Key 可以作为机器身份鉴权了

## 核心宣传点

此前平台已经能创建和吊销项目 API Key，但 claw-interface 还不认这些 Key，没法把它当成机器身份。这次在 claw-interface 里加上了项目级 API Key 鉴权：一个有效 Key 能解析出组织、项目和 Key 本身的标识。不过平台身份到 Interface 边界就会被拦住，返回 503 platform.engine_access_not_ready，不会真的往 Engine 发请求——因为平台到 Engine 的边界还没设计完，先不复用 Work 的归属假设。实现上统一了平台密钥的生成、校验和 SHA-256 哈希，只认活跃组织下的活跃 Key，最后使用时间异步更新且 60 秒节流，并新增 legacy / platform / disabled 三种服务鉴权模式（默认仍是 legacy、不做回退）。失效、已吊销、信息不全、被禁用、存储不可用等情况都有覆盖，且不会泄露具体是哪一层关系没通过。

## 分级

- 内部：P1
- 外部：B
- 发布状态：已合并待发版

## PR 说明

## Problem and behavior

Platform can create and revoke Project API keys, but `claw-interface` could not authenticate those keys as a machine identity. Sending them directly into the existing Engine proxy would also reuse Work ownership assumptions before the Platform-to-Engine boundary has been designed.

This PR adds Project-scoped API key authentication in `claw-interface`. A valid key resolves to `organization_id`, `project_id`, and `api_key_id`. Platform principals are then stopped at the Interface boundary with `503 platform.engine_access_not_ready`, so no Engine request is made.

## Changes

- centralize Platform secret generation, validation, and SHA-256 hashing
- resolve active keys through Project and active Organization records
- update `last_used_at` asynchronously with a 60-second throttle
- add explicit `legacy`, `platform`, and `disabled` service API authentication modes with no fallback; `legacy` remains the default
- cover invalid, revoked, incomplete, disabled, and unavailable-storage cases without leaking which relationship failed
- keep every Platform `/service/v1` resource path closed before Engine dispatch
- consolidate Platform identity, data ownership, API contracts, and release boundaries into one spec
- record [zooclaw-engine#1573](https://github.com/SerendipityOneInc/zooclaw-engine/issues/1573) as the SDK/runtime dependency while leaving the Engine contract in the Engine repository
- rename the Interface runbook to `platform-operations.md` and remove stale phase-based guidance from docs and UI

No `zooclaw-engine` code or schema is changed. This PR does not enable Platform SDK runtime access or change deployed authentication mode.

## Validation

- 55 targeted Platform authentication, repository, proxy, bootstrap, and schema tests passed
- Platform frontend: lint, typecheck, 27 tests, and production build passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`


## 原始内容

- 仓库：SerendipityOneInc/ecap-workspace
- SHA: `4de3138bcfa30f8fb94fdcf24e059774a7ad345d`
- PR: #3838
- 作者：finn-srp
- 日期：2026-09-21T08:24:44Z

### Commit Message

```
feat(platform): add project API key authentication (#3838)

## Problem and behavior

Platform can create and revoke Project API keys, but `claw-interface`
could not authenticate those keys as a machine identity. Sending them
directly into the existing Engine proxy would also reuse Work ownership
assumptions before the Platform-to-Engine boundary has been designed.

This PR adds Project-scoped API key authentication in `claw-interface`.
A valid key resolves to `organization_id`, `project_id`, and
`api_key_id`. Platform principals are then stopped at the Interface
boundary with `503 platform.engine_access_not_ready`, so no Engine
request is made.

## Changes

- centralize Platform secret generation, validation, and SHA-256 hashing
- resolve active keys through Project and active Organization records
- update `last_used_at` asynchronously with a 60-second throttle
- add explicit `legacy`, `platform`, and `disabled` service API
authentication modes with no fallback; `legacy` remains the default
- cover invalid, revoked, incomplete, disabled, and unavailable-storage
cases without leaking which relationship failed
- keep every Platform `/service/v1` resource path closed before Engine
dispatch
- consolidate Platform identity, data ownership, API contracts, and
release boundaries into one spec
- record
[zooclaw-engine#1573](https://github.com/SerendipityOneInc/zooclaw-engine/issues/1573)
as the SDK/runtime dependency while leaving the Engine contract in the
Engine repository
- rename the Interface runbook to `platform-operations.md` and remove
stale phase-based guidance from docs and UI

No `zooclaw-engine` code or schema is changed. This PR does not enable
Platform SDK runtime access or change deployed authentication mode.

## Validation

- 55 targeted Platform authentication, repository, proxy, bootstrap, and
schema tests passed
- Platform frontend: lint, typecheck, 27 tests, and production build
passed
- `bash scripts/verify-py.sh`
- `bash scripts/verify-changed.sh`
```

来源：SerendipityOneInc/ecap-workspace @ 4de3138b，PR #3838，作者 finn-srp。