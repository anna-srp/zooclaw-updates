---
title: "Agent Builder 模型列表补全与运行时对齐"
type: "Bug Fix"
priority: "中"
date: "2026-08-05"
status: "待审核"
channels: ""
---

# Agent Builder 模型列表补全与运行时对齐

## 核心宣传点

Agent Builder 里能选到完整的模型清单，选择失败可重试，运行环境也会自动升级到最新版本。

## 原始内容

- 仓库：`SerendipityOneInc/ecap-workspace`
- Commit：`aa83b9d3ce93607b076868304b7816890cfa189e`
- 作者：kaka-srp
- 日期：2026-08-05T02:56:04Z
- PR：#3239

### Commit Message

```
fix(agent-builder): converge v2 runtime and models (#3239)

## Summary

- [x] expose the complete Agent Builder v2 model set in the composer and
make pending model application retryable
- [x] converge the hidden Agent Studio Agent on the current runtime
asset and exact Engine Environment pin
- [x] move slow Agent Studio setup convergence to the existing
background setup owner
- [x] keep V1 Builder, ordinary Agent Environment updates, and Pack Test
model behavior unchanged
- [x] add the cross-repository design and release order

## Root cause

Three staging failures had separate causes:

1. The v2 composer intersected the Builder model list with the generic
chat catalog, so Builder-only model IDs appeared unavailable and a
pending desired model could not be retried reliably.
2. Agent Studio readiness compared submission provenance but did not
require the installed Agent's runtime asset and resolved Environment to
match the latest Pack asset. The Engine Environment lock then prevented
convergence.
3. Builder activation could synchronously wait for the long Agent Studio
update path instead of allowing the single background setup owner to
converge and report state.

Companion changes:

- Engine locked Environment lifecycle:
https://github.com/SerendipityOneInc/zooclaw-engine/pull/616
- Agent Channel Service terminal Artifact projection:
https://github.com/SerendipityOneInc/agent-channel-service/pull/59

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 289 focused backend tests passed with `AGENTS_V2_ENABLED=false` so
the legacy test matrix uses its intended gate state
- [x] `bash scripts/verify-web.sh <changed paths>`: TypeScript, 399 unit
tests, and ESLint passed
- [x] pre-commit and pre-push changed-surface gates passed
- [x] file-length, complexity, import-contract, and pyright hooks passed

## Deployment order

1. Engine
2. Agent Channel Service
3. ECAP backend
4. ECAP web
```

### PR Body

## Summary

- [x] expose the complete Agent Builder v2 model set in the composer and make pending model application retryable
- [x] converge the hidden Agent Studio Agent on the current runtime asset and exact Engine Environment pin
- [x] move slow Agent Studio setup convergence to the existing background setup owner
- [x] keep V1 Builder, ordinary Agent Environment updates, and Pack Test model behavior unchanged
- [x] add the cross-repository design and release order

## Root cause

Three staging failures had separate causes:

1. The v2 composer intersected the Builder model list with the generic chat catalog, so Builder-only model IDs appeared unavailable and a pending desired model could not be retried reliably.
2. Agent Studio readiness compared submission provenance but did not require the installed Agent's runtime asset and resolved Environment to match the latest Pack asset. The Engine Environment lock then prevented convergence.
3. Builder activation could synchronously wait for the long Agent Studio update path instead of allowing the single background setup owner to converge and report state.

Companion changes:

- Engine locked Environment lifecycle: https://github.com/SerendipityOneInc/zooclaw-engine/pull/616
- Agent Channel Service terminal Artifact projection: https://github.com/SerendipityOneInc/agent-channel-service/pull/59

## Test plan

- [x] `bash scripts/verify-py.sh`
- [x] 289 focused backend tests passed with `AGENTS_V2_ENABLED=false` so the legacy test matrix uses its intended gate state
- [x] `bash scripts/verify-web.sh <changed paths>`: TypeScript, 399 unit tests, and ESLint passed
- [x] pre-commit and pre-push changed-surface gates passed
- [x] file-length, complexity, import-contract, and pyright hooks passed

## Deployment order

1. Engine
2. Agent Channel Service
3. ECAP backend
4. ECAP web

